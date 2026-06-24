#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import math
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

from scripts.train_stage2_condmdi_pulp import (
    CAM_DIM,
    HUM_DIM,
    LATENT_DIM,
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
    parsed = ast.literal_eval(str(value))
    return tuple(int(v) for v in parsed)


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
        return jsonable(value.detach().cpu().numpy())
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        return str(value)
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(path), "mode": payload.get("mode")}, sort_keys=True), flush=True)


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


def rel_delta(base: list[float], changed: list[float]) -> dict[str, float | int]:
    base_arr = np.asarray(base, dtype=np.float64)
    changed_arr = np.asarray(changed, dtype=np.float64)
    delta = changed_arr - base_arr
    denom = np.maximum(np.abs(base_arr), 1e-12)
    return {
        "delta": stats(delta.tolist()),
        "relative_delta": stats((delta / denom).tolist()),
    }


def branch_losses(
    pred: torch.Tensor,
    target: torch.Tensor,
    loss_mask: torch.Tensor,
    task_id: int,
) -> dict[str, torch.Tensor]:
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


def load_run(run_dir: Path, device: torch.device) -> tuple[torch.nn.Module, CondMDIDiffusion, dict[str, Any]]:
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    args = meta.get("args", {})
    model = TemporalObsUNet(
        int(args.get("width", 384)),
        parse_dim_mults(args.get("dim_mults", [1, 2, 2])),
        float(args.get("cond_mask_prob", 0.1)),
        parse_bool(args.get("zero_final", True)),
    ).to(device)
    checkpoint_path = run_dir / "last.pt"
    ckpt = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    diffusion = CondMDIDiffusion(
        int(args.get("diffusion_steps", 1000)),
        str(args.get("noise_schedule", "cosine")),
        device,
    )
    run_info = {
        "run_dir": str(run_dir),
        "checkpoint": str(checkpoint_path),
        "joint_loss_mode": args.get("joint_loss_mode") or meta.get("joint_loss_mode") or "element_mean",
        "step": int(ckpt.get("step", -1)),
        "args": args,
    }
    return model, diffusion, run_info


def make_loader(cache_dir: Path, split: str, start: int, samples: int, batch_size: int, workers: int) -> DataLoader:
    dataset = PulpLatentCache(cache_dir / f"{split}.pt")
    if samples <= 0:
        end = len(dataset)
    else:
        end = min(len(dataset), start + samples)
    if start < 0 or start >= len(dataset) or end <= start:
        raise ValueError(f"bad subset start={start}, end={end}, len={len(dataset)}")
    subset = Subset(dataset, range(start, end))
    return DataLoader(subset, batch_size=batch_size, shuffle=False, num_workers=workers)


def predict_x0(
    model: torch.nn.Module,
    diffusion: CondMDIDiffusion,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task_id: int,
    obs_x0: torch.Tensor | None,
    t: torch.Tensor,
    noise: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, loss_mask = make_branch_masks(z, valid, task)
    x_t = diffusion.q_sample(z, t, noise)
    pred = model(x_t, t, text, obs_x0=z if obs_x0 is None else obs_x0, obs_mask=obs_mask)
    return pred, loss_mask


def run_modeb_gate(args: argparse.Namespace) -> None:
    device = torch.device(args.device)
    torch.manual_seed(args.seed)
    model, diffusion, run_info = load_run(args.run_dir, device)
    loader = make_loader(args.cache_dir, args.split, args.start, args.samples, args.batch_size, args.workers)
    records: dict[str, list[float]] = {}
    pred_shift: dict[str, list[float]] = {}
    with torch.no_grad():
        for batch_index, batch in enumerate(loader):
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            torch.manual_seed(args.seed + batch_index)
            t = torch.randint(0, diffusion.num_timesteps, (z.shape[0],), device=device)
            noise = torch.randn_like(z)
            base_pred, loss_mask = predict_x0(model, diffusion, z, text, valid, TASK_HUMAN, None, t, noise)
            base_loss = branch_losses(base_pred, z, loss_mask, TASK_HUMAN)["human_branch"]
            records.setdefault("base", []).extend(base_loss.detach().cpu().tolist())
            interventions: dict[str, torch.Tensor] = {}
            perm = torch.randperm(z.shape[0], device=device)
            z_shuffle = z.clone()
            z_shuffle[:, HUM_DIM:] = z[perm, HUM_DIM:]
            interventions["camera_shuffle"] = z_shuffle
            z_zero = z.clone()
            z_zero[:, HUM_DIM:] = 0
            interventions["camera_zero"] = z_zero
            z_noise = z.clone()
            cam = z[:, HUM_DIM:]
            z_noise[:, HUM_DIM:] = torch.randn_like(cam) * cam.std().clamp_min(1e-6) + cam.mean()
            interventions["camera_noise_matched"] = z_noise
            for name, obs in interventions.items():
                pred, _ = predict_x0(model, diffusion, z, text, valid, TASK_HUMAN, obs, t, noise)
                loss = branch_losses(pred, z, loss_mask, TASK_HUMAN)["human_branch"]
                records.setdefault(name, []).extend(loss.detach().cpu().tolist())
                shift = (pred[:, :HUM_DIM] - base_pred[:, :HUM_DIM]).pow(2).flatten(1).mean(dim=1)
                pred_shift.setdefault(name, []).extend(shift.detach().cpu().tolist())
    summary: dict[str, Any] = {
        "mode": "modeb_gate",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "run": run_info,
        "cache_dir": str(args.cache_dir),
        "scope": "Latent-level Mode B causal gate. Camera latent is treated as one block; distance/motion sub-slices are not available in this cache.",
        "loss_stats": {name: stats(values) for name, values in records.items()},
        "deltas_vs_base": {name: rel_delta(records["base"], values) for name, values in records.items() if name != "base"},
        "human_pred_shift_vs_base": {name: stats(values) for name, values in pred_shift.items()},
    }
    write_json(args.output, summary)


def run_full_eval(args: argparse.Namespace) -> None:
    device = torch.device(args.device)
    loader = make_loader(args.cache_dir, args.split, args.start, args.samples, args.batch_size, args.workers)
    summary: dict[str, Any] = {
        "mode": "full_eval",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "cache_dir": str(args.cache_dir),
        "runs": {},
    }
    for spec in args.run:
        name, path = spec.split("=", 1)
        model, diffusion, run_info = load_run(Path(path), device)
        run_out: dict[str, Any] = {"run": run_info, "tasks": {}}
        for task_id, task_name in TASK_NAMES.items():
            losses: dict[str, list[float]] = {"element": []}
            if task_id == TASK_JOINT:
                losses["branch_mean"] = []
                losses["human_branch"] = []
                losses["camera_branch"] = []
            elif task_id == TASK_HUMAN:
                losses["human_branch"] = []
            elif task_id == TASK_CAMERA:
                losses["camera_branch"] = []
            shuffle_losses: list[float] = []
            base_for_shuffle: list[float] = []
            with torch.no_grad():
                for batch_index, batch in enumerate(loader):
                    z = batch["z"].to(device)
                    text = batch["text"].to(device)
                    valid = batch["valid"].to(device)
                    torch.manual_seed(args.seed + 1000 * task_id + batch_index)
                    t = torch.randint(0, diffusion.num_timesteps, (z.shape[0],), device=device)
                    noise = torch.randn_like(z)
                    pred, loss_mask = predict_x0(model, diffusion, z, text, valid, task_id, None, t, noise)
                    batch_losses = branch_losses(pred, z, loss_mask, task_id)
                    for key, value in batch_losses.items():
                        losses.setdefault(key, []).extend(value.detach().cpu().tolist())
                    if task_id in {TASK_CAMERA, TASK_HUMAN} and z.shape[0] > 1:
                        obs = z.clone()
                        perm = torch.randperm(z.shape[0], device=device)
                        if task_id == TASK_CAMERA:
                            obs[:, :HUM_DIM] = z[perm, :HUM_DIM]
                            key = "camera_branch"
                        else:
                            obs[:, HUM_DIM:] = z[perm, HUM_DIM:]
                            key = "human_branch"
                        shuf_pred, _ = predict_x0(model, diffusion, z, text, valid, task_id, obs, t, noise)
                        shuf_loss = branch_losses(shuf_pred, z, loss_mask, task_id)[key]
                        shuffle_losses.extend(shuf_loss.detach().cpu().tolist())
                        base_for_shuffle.extend(batch_losses[key].detach().cpu().tolist())
            task_out = {key: stats(value) for key, value in losses.items()}
            if shuffle_losses:
                task_out["obs_shuffle_delta"] = rel_delta(base_for_shuffle, shuffle_losses)
            run_out["tasks"][task_name] = task_out
        summary["runs"][name] = run_out
    write_json(args.output, summary)


@torch.no_grad()
def ddim_joint_sample(
    model: torch.nn.Module,
    diffusion: CondMDIDiffusion,
    text: torch.Tensor,
    shape_like: torch.Tensor,
    steps: int,
    seed: int,
) -> torch.Tensor:
    generator = torch.Generator(device=shape_like.device)
    generator.manual_seed(seed)
    x = torch.randn(shape_like.shape, generator=generator, device=shape_like.device, dtype=shape_like.dtype)
    obs_x0 = torch.zeros_like(shape_like)
    obs_mask = torch.zeros_like(shape_like, dtype=torch.bool)
    ts = torch.linspace(diffusion.num_timesteps - 1, 0, steps, device=shape_like.device).round().long()
    ts = torch.unique_consecutive(ts)
    if ts.numel() == 0 or ts[-1].item() != 0:
        ts = torch.cat([ts, torch.zeros(1, dtype=torch.long, device=shape_like.device)])
    pred_x0 = x
    for idx, t_scalar in enumerate(ts):
        t = torch.full((shape_like.shape[0],), int(t_scalar.item()), dtype=torch.long, device=shape_like.device)
        pred_x0 = model(x, t, text, obs_x0=obs_x0, obs_mask=obs_mask)
        if idx == ts.numel() - 1:
            break
        next_t = int(ts[idx + 1].item())
        a_t = diffusion.sqrt_alphas_cumprod[int(t_scalar.item())].view(1, 1, 1)
        b_t = diffusion.sqrt_one_minus_alphas_cumprod[int(t_scalar.item())].view(1, 1, 1).clamp_min(1e-8)
        a_next = diffusion.sqrt_alphas_cumprod[next_t].view(1, 1, 1)
        b_next = diffusion.sqrt_one_minus_alphas_cumprod[next_t].view(1, 1, 1)
        eps = (x - a_t * pred_x0) / b_t
        x = a_next * pred_x0 + b_next * eps
    return pred_x0


def run_joint_sampler(args: argparse.Namespace) -> None:
    device = torch.device(args.device)
    loader = make_loader(args.cache_dir, args.split, args.start, args.samples, args.batch_size, args.workers)
    summary: dict[str, Any] = {
        "mode": "joint_sampler",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "cache_dir": str(args.cache_dir),
        "runs": {},
        "note": "DDIM-style latent sampler proxy from random noise. This is not the PulpMotion official sampler/evaluator.",
    }
    for spec in args.run:
        name, path = spec.split("=", 1)
        model, diffusion, run_info = load_run(Path(path), device)
        run_out: dict[str, Any] = {"run": run_info, "teacher_forced_x0": {}, "samples": {}}
        teacher_losses: dict[str, list[float]] = {"element": [], "branch_mean": [], "human_branch": [], "camera_branch": []}
        sample_losses: dict[int, dict[str, list[float]]] = {
            step_count: {"element": [], "branch_mean": [], "human_branch": [], "camera_branch": []}
            for step_count in args.steps
        }
        with torch.no_grad():
            for batch_index, batch in enumerate(loader):
                z = batch["z"].to(device)
                text = batch["text"].to(device)
                valid = batch["valid"].to(device)
                torch.manual_seed(args.seed + batch_index)
                t = torch.randint(0, diffusion.num_timesteps, (z.shape[0],), device=device)
                noise = torch.randn_like(z)
                pred, loss_mask = predict_x0(model, diffusion, z, text, valid, TASK_JOINT, None, t, noise)
                for key, value in branch_losses(pred, z, loss_mask, TASK_JOINT).items():
                    teacher_losses[key].extend(value.detach().cpu().tolist())
                for step_count in args.steps:
                    pred_sample = ddim_joint_sample(
                        model,
                        diffusion,
                        text,
                        z,
                        int(step_count),
                        seed=args.seed + 100000 * int(step_count) + batch_index,
                    )
                    for key, value in branch_losses(pred_sample, z, loss_mask, TASK_JOINT).items():
                        sample_losses[int(step_count)][key].extend(value.detach().cpu().tolist())
        run_out["teacher_forced_x0"] = {key: stats(value) for key, value in teacher_losses.items()}
        run_out["samples"] = {
            str(step_count): {key: stats(value) for key, value in values.items()}
            for step_count, values in sample_losses.items()
        }
        summary["runs"][name] = run_out
    write_json(args.output, summary)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="StoryMotion stage2 gated diagnostics.")
    sub = p.add_subparsers(dest="mode", required=True)
    for name in ("modeb-gate", "full-eval", "joint-sampler"):
        sp = sub.add_parser(name)
        sp.add_argument("--cache-dir", type=Path, required=True)
        sp.add_argument("--output", type=Path, required=True)
        sp.add_argument("--device", default="cuda:0")
        sp.add_argument("--split", default="val")
        sp.add_argument("--start", type=int, default=1024)
        sp.add_argument("--samples", type=int, default=2048)
        sp.add_argument("--batch-size", type=int, default=128)
        sp.add_argument("--workers", type=int, default=2)
        sp.add_argument("--seed", type=int, default=20260613)
    sub.choices["modeb-gate"].add_argument("--run-dir", type=Path, required=True)
    sub.choices["full-eval"].add_argument("--run", action="append", required=True, help="name=run_dir")
    sub.choices["joint-sampler"].add_argument("--run", action="append", required=True, help="name=run_dir")
    sub.choices["joint-sampler"].add_argument("--steps", type=int, nargs="+", default=[1, 20, 50])
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.mode == "modeb-gate":
        run_modeb_gate(args)
    elif args.mode == "full-eval":
        run_full_eval(args)
    elif args.mode == "joint-sampler":
        run_joint_sampler(args)
    else:
        raise RuntimeError(args.mode)


if __name__ == "__main__":
    main()
