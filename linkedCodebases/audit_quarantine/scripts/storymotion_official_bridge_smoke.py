#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset


class DummyModule:
    def __init__(self, device: torch.device) -> None:
        self.device = device
        self.eval_metrics: dict[str, Any] = {}


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, torch.Tensor):
        return {
            "shape": list(value.shape),
            "dtype": str(value.dtype),
            "device": str(value.device),
        }
    if hasattr(value, "joints"):
        return {"type": type(value).__name__, "joints": jsonable(value.joints)}
    return value


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def add_pulp_import_paths(pulp_root: Path) -> None:
    paths = [pulp_root.resolve(), (pulp_root / "src").resolve()]
    for path in reversed(paths):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


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


def parse_dim_mults(value: Any) -> tuple[int, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(int(v) for v in value)
    import ast

    return tuple(int(v) for v in ast.literal_eval(str(value)))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


def load_stage2(run_dir: Path, train_mod: Any, device: torch.device):
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    args = meta.get("args", {})
    model = train_mod.TemporalObsUNet(
        int(args.get("width", 384)),
        parse_dim_mults(args.get("dim_mults", [1, 2, 2])),
        float(args.get("cond_mask_prob", 0.1)),
        parse_bool(args.get("zero_final", True)),
    ).to(device)
    ckpt_path = run_dir / "last.pt"
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    diffusion = train_mod.CondMDIDiffusion(
        int(args.get("diffusion_steps", 1000)),
        str(args.get("noise_schedule", "cosine")),
        device,
    )
    return model, diffusion, {
        "run_dir": str(run_dir),
        "checkpoint": str(ckpt_path),
        "step": int(ckpt.get("step", -1)),
        "joint_loss_mode": args.get("joint_loss_mode") or meta.get("joint_loss_mode") or "element_mean",
    }


def build_pulp(cache_mod: Any, story_root: Path, args: argparse.Namespace, device: torch.device):
    pulp_args = argparse.Namespace(
        pulp_root=args.pulp_root or story_root / "linked/PulpMotion",
        data_root=args.data_root or story_root / "linked/pulpmotion-data",
        model_dir=args.model_dir,
        config_name=args.config_name,
        set_name=args.set_name,
        train_split="train",
        val_split=args.split,
        out_dir=Path("/tmp/storymotion_bridge_smoke"),
        device=str(device),
        batch_size=args.batch_size,
        num_workers=args.workers,
        limit_train=None,
        limit_val=None,
        dtype="float16",
        seed=args.seed,
        progress_every=0,
    )
    cfg = cache_mod.build_config(pulp_args)
    dataset = cache_mod.make_dataset(cfg, args.split)
    autoencoder = cache_mod.make_autoencoder(cfg, device)
    return cfg, dataset, autoencoder


def to_official_order(z_hum_cam: torch.Tensor, train_mod: Any) -> torch.Tensor:
    return torch.cat([z_hum_cam[:, train_mod.HUM_DIM :], z_hum_cam[:, : train_mod.HUM_DIM]], dim=1)


def decode_feature_and_raw(
    autoencoder: torch.nn.Module,
    dataset: Any,
    train_mod: Any,
    z_hum_cam: torch.Tensor,
    intrinsics: torch.Tensor,
):
    x_output = autoencoder.decode(to_official_order(z_hum_cam, train_mod))
    raw_output = dataset.get_raw(x_output, intrinsics)
    return x_output, raw_output


def reference_feature_and_raw(dataset: Any, batch: dict[str, Any], intrinsics: torch.Tensor):
    x_input = dataset.get_feat(batch["x_raw"], batch["padding_mask"])
    raw_input = dataset.get_raw(x_input, intrinsics)
    return x_input, raw_input


def make_completion(
    model: torch.nn.Module,
    diffusion: Any,
    train_mod: Any,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task_id: int,
    timestep: int,
) -> torch.Tensor:
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, _ = train_mod.make_branch_masks(z, valid, task)
    t = torch.full((z.shape[0],), timestep, dtype=torch.long, device=z.device)
    noise = torch.randn_like(z)
    x_t = diffusion.q_sample(z, t, noise)
    pred = model(x_t, t, text, obs_x0=z, obs_mask=obs_mask)
    valid_bc = valid[:, None, :].expand_as(z)
    completion = torch.where(obs_mask, z, pred)
    return torch.where(valid_bc, completion, z)


def collate_values(values: list[Any], device: torch.device) -> Any:
    first = values[0]
    if torch.is_tensor(first):
        return torch.stack(values).to(device)
    if isinstance(first, dict):
        keys = set().union(*(set(value.keys()) for value in values))
        return {key: collate_values([value[key] for value in values], device) for key in sorted(keys)}
    return values


def batch_from_sample_ids(dataset: Any, sample_ids: list[str], device: torch.device) -> dict[str, Any]:
    samples = [dataset.get_sample(sample_id) for sample_id in sample_ids]
    keys = set().union(*(set(sample.keys()) for sample in samples))
    batch: dict[str, Any] = {"sample_id": sample_ids}
    for key in sorted(keys):
        batch[key] = collate_values([sample[key] for sample in samples], device)
    return batch


def validate_contract(outputs: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    required_batch = [
        "padding_mask",
        "camera_segments",
        "clatr_caption",
        "clatr_mask",
        "tmr_caption",
        "tmr_mask",
        "proj_joints",
    ]
    required_output = ["raw_input", "raw_output", "x_output"]
    missing_batch = [key for key in required_batch if key not in batch]
    missing_output = [key for key in required_output if key not in outputs]
    checks["missing_batch_keys"] = missing_batch
    checks["missing_output_keys"] = missing_output
    checks["callback_contract_keys_ok"] = not missing_batch and not missing_output

    raw_input = outputs.get("raw_input", {})
    raw_output = outputs.get("raw_output", {})
    x_output = outputs.get("x_output", {})
    checks["raw_input_keys"] = sorted(raw_input) if isinstance(raw_input, dict) else []
    checks["raw_output_keys"] = sorted(raw_output) if isinstance(raw_output, dict) else []
    checks["x_output_keys"] = sorted(x_output) if isinstance(x_output, dict) else []

    try:
        padding = batch["padding_mask"]
        checks["padding_mask_shape"] = list(padding.shape)
        checks["raw_output_camera_shape"] = list(raw_output["camera"].shape)
        checks["raw_output_human_joints_shape"] = list(raw_output["human"].joints.shape)
        checks["raw_output_intrinsics_shape"] = list(raw_output["intrinsics"].shape)
        checks["camera_shape_matches_padding"] = raw_output["camera"].shape[:2] == padding.shape
        checks["human_shape_matches_padding"] = raw_output["human"].joints.shape[:2] == padding.shape
        checks["intrinsics_shape_matches_padding"] = raw_output["intrinsics"].shape[:2] == padding.shape
    except Exception as exc:
        checks["shape_error"] = repr(exc)
    return checks


def metric_checkpoint_status(model_dir: Path) -> dict[str, Any]:
    return {
        "model_dir": str(model_dir),
        "autoencoder_ckpts": sorted(str(path) for path in (model_dir / "autoencoder").glob("*.ckpt")),
        "clatr_files": sorted(str(path) for path in (model_dir / "clatr").glob("*")) if (model_dir / "clatr").exists() else [],
        "tmr_files": sorted(str(path) for path in (model_dir / "tmr").glob("*")) if (model_dir / "tmr").exists() else [],
    }


def instantiate_official_metrics(cfg: Any, pulp_root: Path, task_name: str, device: torch.device):
    from hydra.utils import instantiate

    add_pulp_import_paths(pulp_root)
    if task_name == "camera":
        metrics = instantiate(cfg.metrics.camera)
    elif task_name == "human":
        metrics = instantiate(cfg.metrics.human)
    elif task_name == "joint":
        metrics = instantiate(cfg.metrics)
    else:
        raise ValueError(f"unknown task name: {task_name}")
    module = DummyModule(device)
    metrics.on_test_start(None, module)
    return metrics, module


def official_outputs_for_task(outputs: dict[str, Any], task_name: str) -> dict[str, Any]:
    if task_name == "camera":
        return {
            "raw_input": outputs["raw_input"]["camera"],
            "raw_output": outputs["raw_output"]["camera"],
        }
    if task_name == "human":
        return {
            "raw_input": outputs["raw_input"]["human"],
            "raw_output": outputs["raw_output"]["human"],
        }
    if task_name == "joint":
        return outputs
    raise ValueError(f"unknown task name: {task_name}")


def metric_values(metrics: dict[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key, value in metrics.items():
        if torch.is_tensor(value):
            values[key] = value.detach().cpu().item() if value.numel() == 1 else value.detach().cpu().tolist()
        elif isinstance(value, np.generic):
            values[key] = value.item()
        else:
            values[key] = value
    return values


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Smoke-test StoryMotion -> PulpMotion official callback input contract.")
    p.add_argument("--story-root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--cache-dir", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--split", default="test")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    p.add_argument("--pulp-root", type=Path)
    p.add_argument("--data-root", type=Path)
    p.add_argument("--samples", type=int, default=4)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--workers", type=int, default=0)
    p.add_argument("--seed", type=int, default=20260613)
    p.add_argument("--timestep", type=int, default=500)
    p.add_argument("--run-metrics", action="store_true", help="Instantiate and run PulpMotion official metric callbacks on the smoke outputs.")
    return p


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device(args.device)

    story_root = args.story_root.resolve()
    pulp_root = (args.pulp_root or story_root / "linked/PulpMotion").resolve()
    train_mod = load_module("train_stage2_condmdi_pulp", story_root / "scripts/train_stage2_condmdi_pulp.py")
    cache_mod = load_module("build_stage2_pulp_latent_cache", story_root / "scripts/build_stage2_pulp_latent_cache.py")

    model, diffusion, run_info = load_stage2(args.run_dir, train_mod, device)
    cfg, dataset, autoencoder = build_pulp(cache_mod, story_root, args, device)
    cache = train_mod.PulpLatentCache(args.cache_dir / "val.pt")
    end = min(len(cache), args.start + args.samples)
    if args.start < 0 or args.start >= len(cache) or end <= args.start:
        raise ValueError(f"bad sample range start={args.start}, end={end}, cache_len={len(cache)}")
    loader = DataLoader(Subset(cache, range(args.start, end)), batch_size=args.batch_size, shuffle=False, num_workers=args.workers)

    start_time = time.time()
    mode_checks: dict[str, list[dict[str, Any]]] = {name: [] for name in train_mod.TASK_NAMES.values()}
    metric_callbacks: dict[str, Any] = {}
    metric_modules: dict[str, DummyModule] = {}
    metric_errors: dict[str, str] = {}
    if args.run_metrics:
        for task_name in train_mod.TASK_NAMES.values():
            try:
                metric_callbacks[task_name], metric_modules[task_name] = instantiate_official_metrics(cfg, pulp_root, task_name, device)
            except Exception as exc:
                metric_errors[task_name] = repr(exc)
    first_output_summary: dict[str, Any] | None = None
    with torch.no_grad():
        for batch in loader:
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            sample_ids = [str(value) for value in batch["sample_id"]]
            pulp_batch = batch_from_sample_ids(dataset, sample_ids, device)
            intrinsics = pulp_batch["x_raw"]["intrinsics"]
            x_input, raw_input = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
            for task_id, task_name in train_mod.TASK_NAMES.items():
                completion = make_completion(model, diffusion, train_mod, z, text, valid, task_id, args.timestep)
                x_output, raw_output = decode_feature_and_raw(autoencoder, dataset, train_mod, completion, intrinsics)
                outputs = {"raw_input": raw_input, "raw_output": raw_output, "x_output": x_output}
                check = validate_contract(outputs, pulp_batch)
                check["sample_ids"] = sample_ids
                check["mode"] = task_name
                mode_checks[task_name].append(check)
                if task_name in metric_callbacks:
                    try:
                        official_outputs = official_outputs_for_task(outputs, task_name)
                        metric_callbacks[task_name].on_test_batch_end(None, metric_modules[task_name], official_outputs, pulp_batch, len(mode_checks[task_name]) - 1)
                    except Exception as exc:
                        metric_errors[task_name] = repr(exc)
                        metric_callbacks.pop(task_name, None)
                if first_output_summary is None:
                    first_output_summary = {
                        "batch": jsonable({key: pulp_batch[key] for key in sorted(pulp_batch) if key != "x_raw"}),
                        "outputs": jsonable(outputs),
                        "x_input": jsonable(x_input),
                    }
    metric_results: dict[str, Any] = {}
    for task_name, callback in metric_callbacks.items():
        if task_name in metric_errors:
            continue
        try:
            callback.on_test_epoch_end(None, metric_modules[task_name])
            metrics = metric_values(metric_modules[task_name].eval_metrics)
            metric_results[task_name] = {
                "ok": True,
                "metric_keys": sorted(metrics),
                "metrics": metrics,
            }
        except Exception as exc:
            metric_errors[task_name] = repr(exc)

    payload = {
        "mode": "official_bridge_smoke",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "run": run_info,
        "cache_dir": str(args.cache_dir),
        "sample_range": [args.start, end],
        "samples": end - args.start,
        "timestep": args.timestep,
        "contract": {
            task: {
                "batches": len(checks),
                "all_keys_ok": all(check.get("callback_contract_keys_ok", False) for check in checks),
                "all_shapes_ok": all(
                    check.get("camera_shape_matches_padding", False)
                    and check.get("human_shape_matches_padding", False)
                    and check.get("intrinsics_shape_matches_padding", False)
                    for check in checks
                ),
                "checks": checks,
            }
            for task, checks in mode_checks.items()
        },
        "metric_checkpoint_status": metric_checkpoint_status(args.model_dir),
        "metric_status": "run" if args.run_metrics else "not_run; this smoke validates callback input contract only",
        "metric_results": metric_results,
        "metric_errors": metric_errors,
        "first_output_summary": first_output_summary,
        "elapsed_sec": time.time() - start_time,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "mode": payload["mode"], "samples": payload["samples"]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
