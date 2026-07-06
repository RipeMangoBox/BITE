#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

import torch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


train_mod = load_module("storymotion_train_stage2_condmdi_pulp_replay_cache", SCRIPT_DIR / "train_stage2_condmdi_pulp.py")
eval_mod = load_module("storymotion_official_full_eval_replay_cache", SCRIPT_DIR / "storymotion_official_full_eval.py")
bridge = load_module("storymotion_official_bridge_replay_cache", SCRIPT_DIR / "storymotion_official_bridge_smoke.py")

HUM_DIM = int(train_mod.HUM_DIM)
LATENT_DIM = int(train_mod.LATENT_DIM)
LATENT_FRAMES = int(train_mod.LATENT_FRAMES)
TEXT_DIM = 1024
SOURCE_REPLAY = 2


def jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, torch.Tensor):
        return value.detach().cpu().tolist()
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    return value


def slice_sample_id(sample_id: Any, end: int) -> Any:
    if sample_id is None:
        return [str(i) for i in range(end)]
    if isinstance(sample_id, torch.Tensor):
        return sample_id[:end].clone()
    return list(sample_id[:end])


@torch.no_grad()
def build_cache_file(
    input_path: Path,
    output_path: Path,
    model: torch.nn.Module,
    diffusion: Any,
    device: torch.device,
    args: argparse.Namespace,
    file_index: int,
) -> dict[str, Any]:
    data = torch.load(input_path, map_location="cpu")
    z = data["z"].float()
    text = data["text"].float()
    valid = data["valid_mask"].bool()
    if z.ndim != 3 or z.shape[1:] != (LATENT_DIM, LATENT_FRAMES):
        raise ValueError(f"{input_path}: expected z [N,{LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
    if text.ndim != 2 or text.shape[1] != TEXT_DIM:
        raise ValueError(f"{input_path}: expected text [N,{TEXT_DIM}], got {tuple(text.shape)}")
    if valid.shape != (z.shape[0], LATENT_FRAMES):
        raise ValueError(f"{input_path}: expected valid_mask [N,{LATENT_FRAMES}], got {tuple(valid.shape)}")

    total = z.shape[0] if args.limit <= 0 else min(z.shape[0], args.limit)
    z_out = torch.empty((total, LATENT_DIM, LATENT_FRAMES), dtype=torch.float32)
    z_out[:, HUM_DIM:, :] = z[:total, HUM_DIM:, :]
    sigma = torch.empty((total,), dtype=torch.float32)
    source_type = torch.full((total,), SOURCE_REPLAY, dtype=torch.long)
    started = time.time()

    model.eval()
    for start in range(0, total, args.batch_size):
        end = min(total, start + args.batch_size)
        sample_indices = list(range(start, end))
        z_batch = z[start:end].to(device)
        text_batch = text[start:end].to(device)
        valid_batch = valid[start:end].to(device)
        pred = eval_mod.sample_start_x(
            model,
            diffusion,
            train_mod,
            z_batch,
            text_batch,
            valid_batch,
            train_mod.TASK_HUMAN_TEXT,
            sample_indices,
            args.seed + file_index * 100_003,
            args.num_steps,
            cfg_scale=args.cfg_scale,
            cfg_human=None,
            cfg_camera=None,
            eta=args.eta,
            channel_gated_cfg=False,
            joint_camera_latent_intervention="none",
            joint_human_camera_input_mode="normal",
        )
        human_syn = pred[:, :HUM_DIM, :].detach().cpu().float()
        human_gt = z[start:end, :HUM_DIM, :]
        z_out[start:end, :HUM_DIM, :] = human_syn
        sigma[start:end] = (human_syn - human_gt).flatten(1).std(dim=1, unbiased=False)
        if args.progress_every > 0 and (end == total or (end // args.batch_size) % args.progress_every == 0):
            elapsed = max(time.time() - started, 1e-6)
            print(
                json.dumps(
                    {
                        "file": input_path.name,
                        "done": end,
                        "total": total,
                        "samples_per_sec": end / elapsed,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

    payload = {
        "z": z_out,
        "text": text[:total].clone(),
        "valid_mask": valid[:total].clone(),
        "sample_id": slice_sample_id(data.get("sample_id"), total),
        "source_type": source_type,
        "sigma": sigma,
        "meta": {
            "kind": "stage2_human_text_replay_cache",
            "source_cache": str(input_path),
            "human_run_dir": str(args.human_run_dir),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "num_samples": int(total),
            "num_steps": int(args.num_steps),
            "seed": int(args.seed + file_index * 100_003),
            "cfg_scale": float(args.cfg_scale),
            "eta": float(args.eta),
            "human_slice": [0, HUM_DIM],
            "camera_slice": [HUM_DIM, LATENT_DIM],
            "camera_target": "ground_truth_from_source_cache",
            "human_source": "human_text_generator",
            "sigma_mean": float(sigma.mean().item()) if total else 0.0,
            "sigma_std": float(sigma.std(unbiased=False).item()) if total else 0.0,
            "upstream_meta": jsonable(data.get("meta", {})),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(payload, output_path)
    return payload["meta"]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Build H2C replay cache from a human_text generator and GT camera cache.")
    p.add_argument("--human-run-dir", type=Path, required=True)
    p.add_argument("--source-cache-dir", type=Path, required=True)
    p.add_argument("--output-cache-dir", type=Path, required=True)
    p.add_argument("--cache-files", nargs="+", default=["train.pt", "val.pt"])
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--num-steps", type=int, default=50)
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--cfg-scale", type=float, default=1.0)
    p.add_argument("--eta", type=float, default=0.0)
    p.add_argument("--limit", type=int, default=0, help="debug limit per cache file; <=0 means all samples")
    p.add_argument("--progress-every", type=int, default=10)
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.batch_size <= 0:
        raise ValueError("--batch-size must be positive")
    if args.num_steps <= 0:
        raise ValueError("--num-steps must be positive")
    if args.limit < 0:
        raise ValueError("--limit must be non-negative")
    device = torch.device(args.device)
    model, diffusion, run_info = bridge.load_stage2(args.human_run_dir, train_mod, device)
    metas = {}
    for file_index, name in enumerate(args.cache_files):
        input_path = args.source_cache_dir / name
        output_path = args.output_cache_dir / name
        metas[name] = build_cache_file(input_path, output_path, model, diffusion, device, args, file_index)
    summary = {
        "kind": "stage2_human_text_replay_cache_summary",
        "human_run": run_info,
        "source_cache_dir": str(args.source_cache_dir),
        "output_cache_dir": str(args.output_cache_dir),
        "cache_files": list(args.cache_files),
        "files": metas,
    }
    args.output_cache_dir.mkdir(parents=True, exist_ok=True)
    (args.output_cache_dir / "meta.json").write_text(json.dumps(jsonable(summary), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output_cache_dir), "files": list(args.cache_files)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
