#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.train_stage2_condmdi_pulp import (  # noqa: E402
    CAM_DIM,
    HUM_DIM,
    TASK_CAMERA,
    TASK_HUMAN,
    TASK_JOINT,
    TASK_NAMES,
    CondMDIDiffusion,
    PulpLatentCache,
    TemporalObsUNet,
    make_branch_masks,
)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).lower() in {"1", "true", "yes", "on"}


def parse_dim_mults(value: Any) -> tuple[int, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(int(v) for v in value)
    return tuple(int(v) for v in ast.literal_eval(str(value)))


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer, np.floating)):
        return value.item()
    if isinstance(value, torch.Tensor):
        return jsonable(value.detach().cpu().numpy())
    if isinstance(value, float):
        return value if math.isfinite(value) else str(value)
    return value


def stats(values: list[float]) -> dict[str, float | int]:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return {"n": 0}
    return {
        "n": int(arr.size),
        "mean": float(arr.mean()),
        "std": float(arr.std()),
        "median": float(np.median(arr)),
        "p90": float(np.quantile(arr, 0.90)),
        "p95": float(np.quantile(arr, 0.95)),
        "p99": float(np.quantile(arr, 0.99)),
        "max": float(arr.max()),
    }


def rel_delta(base: list[float], changed: list[float]) -> dict[str, Any]:
    base_arr = np.asarray(base, dtype=np.float64)
    changed_arr = np.asarray(changed, dtype=np.float64)
    delta = changed_arr - base_arr
    denom = np.maximum(np.abs(base_arr), 1e-12)
    return {
        "delta": stats(delta.tolist()),
        "relative_delta": stats((delta / denom).tolist()),
    }


def branch_losses(pred: torch.Tensor, target: torch.Tensor, loss_mask: torch.Tensor, task_id: int) -> dict[str, torch.Tensor]:
    diff = (pred - target).pow(2)
    mask = loss_mask.float()
    element = (diff * mask).flatten(1).sum(dim=1) / mask.flatten(1).sum(dim=1).clamp_min(1.0)
    human_mask = mask[:, :HUM_DIM]
    camera_mask = mask[:, HUM_DIM:]
    human = (diff[:, :HUM_DIM] * human_mask).flatten(1).sum(dim=1) / human_mask.flatten(1).sum(dim=1).clamp_min(1.0)
    camera = (diff[:, HUM_DIM:] * camera_mask).flatten(1).sum(dim=1) / camera_mask.flatten(1).sum(dim=1).clamp_min(1.0)
    out = {"element": element}
    if task_id == TASK_JOINT:
        out["branch_mean"] = 0.5 * (human + camera)
        out["human_branch"] = human
        out["camera_branch"] = camera
    elif task_id == TASK_HUMAN:
        out["human_branch"] = human
    elif task_id == TASK_CAMERA:
        out["camera_branch"] = camera
    return out


def load_run(run_dir: Path, device: torch.device, weights: str) -> tuple[torch.nn.Module, CondMDIDiffusion, dict[str, Any]]:
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    args = meta.get("args", {})
    ckpt_path = run_dir / "last.pt"
    ckpt = torch.load(ckpt_path, map_location=device)
    if weights not in ckpt:
        raise KeyError(f"{weights!r} not found in {ckpt_path}; available keys: {sorted(ckpt.keys())}")
    state = ckpt[weights]
    reliability_cond_dim = 5 if parse_bool(args.get("p2b_enable", False)) else 0
    if reliability_cond_dim == 0 and "reliability_mlp.0.weight" in state:
        reliability_cond_dim = int(state["reliability_mlp.0.weight"].shape[0])
    model = TemporalObsUNet(
        int(args.get("width", 384)),
        parse_dim_mults(args.get("dim_mults", [1, 2, 2])),
        float(args.get("cond_mask_prob", 0.1)),
        parse_bool(args.get("zero_final", True)),
        float(args.get("cond_mask_prob_cam", 0.0)),
        float(args.get("cond_mask_prob_hum", 0.0)),
        reliability_cond_dim=reliability_cond_dim,
    ).to(device)
    model.load_state_dict(state)
    model.eval()
    diffusion = CondMDIDiffusion(
        int(args.get("diffusion_steps", 1000)),
        str(args.get("noise_schedule", "cosine")),
        device,
    )
    info = {
        "run_dir": str(run_dir),
        "checkpoint": str(ckpt_path),
        "weights": weights,
        "step": int(ckpt.get("step", -1)),
        "args": args,
        "reliability_cond_dim": reliability_cond_dim,
    }
    return model, diffusion, info


def make_loader(cache_dir: Path, split: str, start: int, samples: int, batch_size: int, workers: int) -> DataLoader:
    dataset = PulpLatentCache(cache_dir / f"{split}.pt")
    end = len(dataset) if samples <= 0 else min(len(dataset), start + samples)
    if start < 0 or start >= len(dataset) or end <= start:
        raise ValueError(f"bad subset start={start}, end={end}, len={len(dataset)}")
    return DataLoader(Subset(dataset, range(start, end)), batch_size=batch_size, shuffle=False, num_workers=workers)


def per_sample_feature_shuffle(x: torch.Tensor, seed: int) -> torch.Tensor:
    gen = torch.Generator(device=x.device)
    gen.manual_seed(seed)
    out = x.clone()
    for i in range(x.shape[0]):
        perm = torch.randperm(x.shape[1], generator=gen, device=x.device)
        out[i] = x[i, perm]
    return out


def text_variants(text: torch.Tensor, seed: int) -> dict[str, torch.Tensor]:
    half = text.shape[-1] // 2
    variants = {"full": text}
    camera_zero = text.clone()
    camera_zero[:, :half] = 0
    variants["camera_zero"] = camera_zero
    human_zero = text.clone()
    human_zero[:, half:] = 0
    variants["human_zero"] = human_zero
    zero = text.clone()
    zero.zero_()
    variants["zero"] = zero
    camera_shuffle = text.clone()
    camera_shuffle[:, :half] = per_sample_feature_shuffle(text[:, :half], seed)
    variants["camera_shuffle_dims"] = camera_shuffle
    human_shuffle = text.clone()
    human_shuffle[:, half:] = per_sample_feature_shuffle(text[:, half:], seed + 1)
    variants["human_shuffle_dims"] = human_shuffle
    return variants


def append_losses(store: dict[str, dict[str, list[float]]], condition: str, losses: dict[str, torch.Tensor]) -> None:
    for key, value in losses.items():
        store.setdefault(condition, {}).setdefault(key, []).extend(value.detach().cpu().tolist())


def append_shift(
    store: dict[str, dict[str, list[float]]],
    condition: str,
    pred: torch.Tensor,
    base_pred: torch.Tensor,
    loss_mask: torch.Tensor,
) -> None:
    diff = (pred - base_pred).pow(2)
    mask = loss_mask.float()
    target_shift = (diff * mask).flatten(1).sum(dim=1) / mask.flatten(1).sum(dim=1).clamp_min(1.0)
    store.setdefault(condition, {}).setdefault("target_masked", []).extend(target_shift.detach().cpu().tolist())
    human_mask = mask[:, :HUM_DIM]
    if human_mask.flatten(1).any(dim=1).any():
        human_shift = (diff[:, :HUM_DIM] * human_mask).flatten(1).sum(dim=1) / human_mask.flatten(1).sum(dim=1).clamp_min(1.0)
        store.setdefault(condition, {}).setdefault("human_branch", []).extend(human_shift.detach().cpu().tolist())
    camera_mask = mask[:, HUM_DIM:]
    if camera_mask.flatten(1).any(dim=1).any():
        camera_shift = (diff[:, HUM_DIM:] * camera_mask).flatten(1).sum(dim=1) / camera_mask.flatten(1).sum(dim=1).clamp_min(1.0)
        store.setdefault(condition, {}).setdefault("camera_branch", []).extend(camera_shift.detach().cpu().tolist())


def summarize_conditions(values: dict[str, dict[str, list[float]]]) -> dict[str, Any]:
    out = {cond: {key: stats(v) for key, v in by_key.items()} for cond, by_key in values.items()}
    if "full" in values:
        out["delta_vs_full"] = {
            cond: {key: rel_delta(values["full"][key], vals) for key, vals in by_key.items() if key in values["full"]}
            for cond, by_key in values.items()
            if cond != "full"
        }
    elif "base" in values:
        out["delta_vs_base"] = {
            cond: {key: rel_delta(values["base"][key], vals) for key, vals in by_key.items() if key in values["base"]}
            for cond, by_key in values.items()
            if cond != "base"
        }
    return out


def sampled_noise_like(x: torch.Tensor, seed: int) -> torch.Tensor:
    gen = torch.Generator(device=x.device)
    gen.manual_seed(seed)
    return torch.randn(x.shape, generator=gen, device=x.device, dtype=x.dtype)


def xt_noise_only(diffusion: CondMDIDiffusion, t: torch.Tensor, shape_like: torch.Tensor, seed: int) -> torch.Tensor:
    scale = diffusion.sqrt_one_minus_alphas_cumprod[t].view((shape_like.shape[0],) + (1,) * (shape_like.ndim - 1))
    return scale * sampled_noise_like(shape_like, seed)


def shuffle_channels_in_sample(x: torch.Tensor, start: int, end: int, seed: int) -> torch.Tensor:
    out = x.clone()
    out[:, start:end] = per_sample_feature_shuffle(x[:, start:end], seed)
    return out


@torch.no_grad()
def run_for_model(
    model: torch.nn.Module,
    diffusion: CondMDIDiffusion,
    loader: DataLoader,
    device: torch.device,
    timesteps: list[int],
    seed: int,
    diagnostics: set[str],
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if "text" in diagnostics:
        out["text_ablation"] = {}
    if "joint" in diagnostics:
        out["joint_channel_intervention"] = {"losses": {}, "pred_shift_vs_base": {}}
    if "observed" in diagnostics:
        out["completion_observed_intervention"] = {}
    model_dtype = next(model.parameters()).dtype

    for batch_index, batch in enumerate(loader):
        z = batch["z"].to(device=device, dtype=model_dtype, non_blocking=True)
        text = batch["text"].to(device=device, dtype=model_dtype, non_blocking=True)
        valid = batch["valid"].to(device, non_blocking=True)
        for t_scalar in timesteps:
            t = torch.full((z.shape[0],), int(t_scalar), dtype=torch.long, device=z.device)
            noise = sampled_noise_like(z, seed + 100000 * batch_index + int(t_scalar))
            x_t = diffusion.q_sample(z, t, noise).to(dtype=model_dtype)

            if "text" in diagnostics:
                for task_id, task_name in TASK_NAMES.items():
                    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
                    obs_mask, loss_mask = make_branch_masks(z, valid, task)
                    losses_store = out["text_ablation"].setdefault(task_name, {}).setdefault("losses", {})
                    shift_store = out["text_ablation"].setdefault(task_name, {}).setdefault("pred_shift_vs_full", {})
                    base_pred = None
                    for name, variant_text in text_variants(text, seed + 7 * batch_index + int(t_scalar)).items():
                        pred = model(x_t, t, variant_text, obs_x0=z, obs_mask=obs_mask)
                        if name == "full":
                            base_pred = pred
                        append_losses(losses_store, name, branch_losses(pred, z, loss_mask, task_id))
                        if base_pred is not None and name != "full":
                            append_shift(shift_store, name, pred, base_pred, loss_mask)

            if "joint" in diagnostics:
                task = torch.full((z.shape[0],), TASK_JOINT, dtype=torch.long, device=z.device)
                obs_mask, loss_mask = make_branch_masks(z, valid, task)
                obs_x0 = torch.zeros_like(z)
                base_pred = model(x_t, t, text, obs_x0=obs_x0, obs_mask=obs_mask)
                append_losses(out["joint_channel_intervention"]["losses"], "base", branch_losses(base_pred, z, loss_mask, TASK_JOINT))
                interventions: dict[str, torch.Tensor] = {
                    "human_xt_shuffle_dims": shuffle_channels_in_sample(x_t, 0, HUM_DIM, seed + 1100000 + batch_index + int(t_scalar)),
                    "camera_xt_shuffle_dims": shuffle_channels_in_sample(x_t, HUM_DIM, x_t.shape[1], seed + 1200000 + batch_index + int(t_scalar)),
                }
                human_zero = x_t.clone()
                human_zero[:, :HUM_DIM] = 0
                interventions["human_xt_zero"] = human_zero
                camera_zero = x_t.clone()
                camera_zero[:, HUM_DIM:] = 0
                interventions["camera_xt_zero"] = camera_zero
                human_resample = x_t.clone()
                human_resample[:, :HUM_DIM] = xt_noise_only(diffusion, t, x_t[:, :HUM_DIM], seed + 2000000 + batch_index + int(t_scalar))
                interventions["human_xt_noise_only"] = human_resample
                camera_resample = x_t.clone()
                camera_resample[:, HUM_DIM:] = xt_noise_only(diffusion, t, x_t[:, HUM_DIM:], seed + 3000000 + batch_index + int(t_scalar))
                interventions["camera_xt_noise_only"] = camera_resample
                for name, x_mod in interventions.items():
                    pred = model(x_mod, t, text, obs_x0=obs_x0, obs_mask=obs_mask)
                    append_losses(out["joint_channel_intervention"]["losses"], name, branch_losses(pred, z, loss_mask, TASK_JOINT))
                    append_shift(out["joint_channel_intervention"]["pred_shift_vs_base"], name, pred, base_pred, loss_mask)

            if "observed" in diagnostics:
                for task_id in (TASK_CAMERA, TASK_HUMAN):
                    task_name = TASK_NAMES[task_id]
                    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
                    obs_mask, loss_mask = make_branch_masks(z, valid, task)
                    target = out["completion_observed_intervention"].setdefault(task_name, {})
                    losses_store = target.setdefault("losses", {})
                    shift_store = target.setdefault("pred_shift_vs_base", {})
                    base_pred = model(x_t, t, text, obs_x0=z, obs_mask=obs_mask)
                    append_losses(losses_store, "base", branch_losses(base_pred, z, loss_mask, task_id))
                    variants: dict[str, torch.Tensor] = {}
                    if z.shape[0] > 1:
                        perm = torch.randperm(z.shape[0], device=z.device)
                        shuffled = z.clone()
                        if task_id == TASK_CAMERA:
                            shuffled[:, :HUM_DIM] = z[perm, :HUM_DIM]
                        else:
                            shuffled[:, HUM_DIM:] = z[perm, HUM_DIM:]
                        variants["obs_shuffle_batch"] = shuffled
                    zeroed = z.clone()
                    if task_id == TASK_CAMERA:
                        zeroed[:, :HUM_DIM] = 0
                    else:
                        zeroed[:, HUM_DIM:] = 0
                    variants["obs_zero"] = zeroed
                    noised = z.clone()
                    if task_id == TASK_CAMERA:
                        branch = z[:, :HUM_DIM]
                        noised[:, :HUM_DIM] = sampled_noise_like(branch, seed + 4000000 + batch_index + int(t_scalar))
                    else:
                        branch = z[:, HUM_DIM:]
                        noised[:, HUM_DIM:] = sampled_noise_like(branch, seed + 5000000 + batch_index + int(t_scalar))
                    variants["obs_resample_standard"] = noised
                    for name, obs_x0 in variants.items():
                        pred = model(x_t, t, text, obs_x0=obs_x0, obs_mask=obs_mask)
                        append_losses(losses_store, name, branch_losses(pred, z, loss_mask, task_id))
                        append_shift(shift_store, name, pred, base_pred, loss_mask)

    if "text" in diagnostics:
        for task_name, payload in out["text_ablation"].items():
            payload["losses"] = summarize_conditions(payload["losses"])
            payload["pred_shift_vs_full"] = {
                cond: {key: stats(vals) for key, vals in by_key.items()}
                for cond, by_key in payload["pred_shift_vs_full"].items()
            }
    if "joint" in diagnostics:
        out["joint_channel_intervention"]["losses"] = summarize_conditions(out["joint_channel_intervention"]["losses"])
        out["joint_channel_intervention"]["pred_shift_vs_base"] = {
            cond: {key: stats(vals) for key, vals in by_key.items()}
            for cond, by_key in out["joint_channel_intervention"]["pred_shift_vs_base"].items()
        }
    if "observed" in diagnostics:
        for task_name, payload in out["completion_observed_intervention"].items():
            payload["losses"] = summarize_conditions(payload["losses"])
            payload["pred_shift_vs_base"] = {
                cond: {key: stats(vals) for key, vals in by_key.items()}
                for cond, by_key in payload["pred_shift_vs_base"].items()
            }
    return out


def parse_runs(values: list[str]) -> dict[str, Path]:
    runs = {}
    for value in values:
        name, path = value.split("=", 1)
        runs[name] = Path(path)
    return runs


def main() -> None:
    parser = argparse.ArgumentParser(description="StoryMotion v6.3 coupling diagnostics.")
    parser.add_argument("--run", action="append", required=True, help="name=run_dir")
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--split", default="val")
    parser.add_argument("--start", type=int, default=1024)
    parser.add_argument("--samples", type=int, default=1024)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260701)
    parser.add_argument("--timesteps", type=int, nargs="+", default=[50, 250, 500, 750, 950])
    parser.add_argument("--weights", choices=["model", "ema_model", "raw_model"], default="model")
    parser.add_argument("--diagnostics", choices=["all", "text", "joint", "observed"], nargs="+", default=["all"])
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    if device.type == "cuda":
        torch.cuda.set_device(device)
        torch.cuda.manual_seed_all(args.seed)

    selected = {"text", "joint", "observed"} if "all" in args.diagnostics else set(args.diagnostics)
    loader = make_loader(args.cache_dir, args.split, args.start, args.samples, args.batch_size, args.workers)
    output: dict[str, Any] = {
        "mode": "storymotion_v63_coupling_eval",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "cache_dir": str(args.cache_dir),
        "split": args.split,
        "start": args.start,
        "samples": args.samples,
        "batch_size": args.batch_size,
        "seed": args.seed,
        "timesteps": args.timesteps,
        "diagnostics": sorted(selected),
        "runs": {},
        "notes": [
            "All ablations are paired by batch, timestep, and diffusion noise.",
            "Text halves follow current Stage2 convention: first 512 camera text, last 512 human text.",
            "Text shuffle permutes dimensions within each sample; it does not swap text across samples.",
            "Joint x_t noise_only interventions use sqrt(1-alpha_bar_t) scaled fresh noise, not raw unit noise.",
            "This is a teacher-forced one-step latent diagnostic, not the official multi-step generation metric.",
        ],
    }
    for name, run_dir in parse_runs(args.run).items():
        model, diffusion, info = load_run(run_dir, device, args.weights)
        output["runs"][name] = {
            "run": info,
            "results": run_for_model(model, diffusion, loader, device, args.timesteps, args.seed, selected),
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(output), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "runs": sorted(output["runs"].keys())}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
