#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader


def patch_numpy_aliases() -> None:
    for name, value in {
        "bool": bool,
        "int": int,
        "float": float,
        "complex": complex,
        "object": object,
        "str": str,
        "unicode": str,
    }.items():
        if not hasattr(np, name):
            setattr(np, name, value)


def add_pulp_paths(pulp_root: Path) -> None:
    for path in [pulp_root.resolve(), (pulp_root / "src").resolve()]:
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def truncate_dataset(dataset: Any, limit: int | None) -> Any:
    if limit is None or limit <= 0:
        return dataset
    sample_ids = list(dataset.sample_ids[:limit])
    dataset.sample_ids = sample_ids
    for attr in ("joint_dataset", "camera_dataset", "human_dataset", "caption_dataset"):
        sub = getattr(dataset, attr, None)
        if sub is not None and hasattr(sub, "sample_ids"):
            sub.sample_ids = sample_ids
    return dataset


def metric_values(metrics: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in metrics.items():
        if torch.is_tensor(value):
            out[key] = value.detach().cpu().item() if value.numel() == 1 else value.detach().cpu().tolist()
        elif isinstance(value, np.generic):
            out[key] = value.item()
        else:
            try:
                out[key] = float(value)
            except Exception:
                out[key] = str(value)
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run PulpMotion official baseline eval with explicit sampler settings.")
    p.add_argument("--pulp-root", type=Path, required=True)
    p.add_argument("--checkpoint-dir", type=Path, required=True)
    p.add_argument("--checkpoint-path", type=Path, required=True)
    p.add_argument("--data-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--split", default="test")
    p.add_argument("--limit-samples", type=int)
    p.add_argument(
        "--sample-ids-jsonl",
        type=Path,
        help="Optional JSONL records containing sample_id; evaluates in that exact order.",
    )
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--cfg-rate-c", type=float, default=11.0)
    p.add_argument("--cfg-rate-z", type=float, required=True)
    p.add_argument("--num-steps", type=int, default=50)
    return p


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    add_pulp_paths(args.pulp_root)
    torch.set_float32_matmul_precision("medium")

    from hydra import compose, initialize_config_dir
    from hydra.utils import instantiate
    from lightning.pytorch import seed_everything
    from omegaconf import OmegaConf

    try:
        OmegaConf.register_new_resolver("eval", eval)
    except ValueError:
        pass

    seed_everything(args.seed)
    overrides = [
        f"checkpoint_dir={args.checkpoint_dir}",
        f"checkpoint_path={args.checkpoint_path}",
        f"dataset.dataset_dir={args.data_root}",
        f"dataset.joint.set_name={args.set_name}",
        "log_wandb=false",
        f"compnode.batch_size={args.batch_size}",
        f"compnode.num_workers={args.workers}",
        "compnode.num_gpus=1",
        f"model.sampler.generation_sampler.cfg_rate_c={args.cfg_rate_c}",
        f"model.sampler.generation_sampler.cfg_rate_z={args.cfg_rate_z}",
        f"model.sampler.generation_sampler.num_steps={args.num_steps}",
    ]
    with initialize_config_dir(version_base="1.3", config_dir=str((args.pulp_root / "configs").resolve())):
        cfg = compose(config_name=args.config_name, overrides=overrides)

    metrics = [instantiate(cfg.metrics)]
    model = instantiate(cfg.model)
    checkpoint = torch.load(args.checkpoint_path, map_location="cpu", weights_only=False)
    load_keys = model.load_state_dict(checkpoint["state_dict"], strict=False)
    trainer = instantiate(cfg.trainer)(
        callbacks=metrics,
        logger=False,
        enable_checkpointing=False,
        enable_progress_bar=True,
    )

    dataset = instantiate(cfg.dataset)
    test_dataset = copy.deepcopy(dataset).set_split(args.split, mode="test")
    full_len = len(test_dataset)
    if args.sample_ids_jsonl is not None:
        requested_ids = [
            str(json.loads(line)["sample_id"])
            for line in args.sample_ids_jsonl.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        available_ids = set(test_dataset.sample_ids)
        missing_ids = [sample_id for sample_id in requested_ids if sample_id not in available_ids]
        if missing_ids:
            raise ValueError(f"{len(missing_ids)} requested sample IDs are absent; first={missing_ids[0]}")
        test_dataset.sample_ids = requested_ids
        for attr in ("joint_dataset", "camera_dataset", "human_dataset", "caption_dataset"):
            sub = getattr(test_dataset, attr, None)
            if sub is not None:
                sub.set_split(requested_ids, test_dataset.mode)
    test_dataset = truncate_dataset(test_dataset, args.limit_samples)
    dataloader = DataLoader(
        test_dataset,
        batch_size=cfg.compnode.batch_size,
        num_workers=cfg.compnode.num_workers,
        pin_memory=args.device.startswith("cuda"),
    )

    t0 = time.time()
    trainer.test(model=model, dataloaders=dataloader, verbose=False)
    metrics_out = metric_values(model.eval_metrics)
    payload = {
        "mode": "pulpmotion_official_baseline_eval",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "config_name": args.config_name,
        "set_name": args.set_name,
        "split": args.split,
        "full_split_samples": full_len,
        "evaluated_samples": len(test_dataset),
        "sample_ids": list(test_dataset.sample_ids),
        "sample_ids_jsonl": str(args.sample_ids_jsonl) if args.sample_ids_jsonl is not None else None,
        "pulp_root": str(args.pulp_root),
        "data_root": str(args.data_root),
        "checkpoint_dir": str(args.checkpoint_dir),
        "checkpoint_path": str(args.checkpoint_path),
        "checkpoint_sha256": sha256_file(args.checkpoint_path),
        "checkpoint_global_step": int(checkpoint.get("global_step", -1)),
        "sampler": {
            "num_steps": args.num_steps,
            "cfg_rate_c": args.cfg_rate_c,
            "cfg_rate_z": args.cfg_rate_z,
        },
        "load_state_dict": {
            "missing": list(load_keys.missing_keys),
            "unexpected": list(load_keys.unexpected_keys),
        },
        "metric_keys": sorted(metrics_out),
        "metrics": metrics_out,
        "elapsed_sec": time.time() - t0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "keys": len(metrics_out), "elapsed_sec": payload["elapsed_sec"]}, sort_keys=True))


if __name__ == "__main__":
    main()
