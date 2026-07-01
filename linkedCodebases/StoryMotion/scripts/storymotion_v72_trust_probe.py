#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import train_stage2_condmdi_pulp as train_mod  # noqa: E402


def parse_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


def parse_dim_mults(value: Any) -> tuple[int, ...]:
    if value is None:
        return (1, 2, 2)
    if isinstance(value, (list, tuple)):
        return tuple(int(v) for v in value)
    parsed = ast.literal_eval(str(value))
    if isinstance(parsed, int):
        return (parsed,)
    return tuple(int(v) for v in parsed)


def build_model(checkpoint: dict[str, Any], device: torch.device) -> torch.nn.Module:
    meta_args = checkpoint.get("meta", {}).get("args", {})
    model = train_mod.TemporalObsUNet(
        width=int(meta_args.get("width", 384)),
        dim_mults=parse_dim_mults(meta_args.get("dim_mults", [1, 2, 2])),
        cond_mask_prob=float(meta_args.get("cond_mask_prob", 0.1)),
        zero_final=parse_bool(meta_args.get("zero_final"), True),
        cond_mask_prob_cam=float(meta_args.get("cond_mask_prob_cam", 0.0)),
        cond_mask_prob_hum=float(meta_args.get("cond_mask_prob_hum", 0.0)),
        v72_text_role_router=parse_bool(meta_args.get("v72_text_role_router"), True),
        v72_aux_text_scale=float(meta_args.get("v72_aux_text_scale", 0.35)),
        v72_soft_source=parse_bool(meta_args.get("v72_soft_source"), True),
        v72_trust_gate=parse_bool(meta_args.get("v72_trust_gate"), True),
        v72_relation_surrogate=parse_bool(meta_args.get("v72_relation_surrogate"), False),
        v72_gate_bias=float(meta_args.get("v72_gate_bias", 2.0)),
    ).to(device)
    model.load_state_dict(checkpoint.get("model", checkpoint.get("raw_model")), strict=True)
    model.eval()
    return model


@torch.no_grad()
def probe_task(
    model: torch.nn.Module,
    diffusion: train_mod.CondMDIDiffusion,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task_id: int,
    sigma: float,
    timestep: int,
    seed: int,
) -> dict[str, Any]:
    generator = torch.Generator(device=z.device)
    generator.manual_seed(seed + task_id * 1009 + int(timestep) * 917 + int(sigma * 1000) * 101)
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, loss_mask = train_mod.make_branch_masks(z, valid, task)
    noise = torch.randn(z.shape, generator=generator, device=z.device, dtype=z.dtype)
    t_value = max(0, min(int(timestep), diffusion.num_timesteps - 1))
    t = torch.full((z.shape[0],), t_value, dtype=torch.long, device=z.device)
    x_t = diffusion.q_sample(z, t, noise)

    variants = {
        "correct_gt": train_mod.build_source_meta(obs_mask, train_mod.SOURCE_GT),
        "wrong_noisy": train_mod.build_source_meta(obs_mask, train_mod.SOURCE_NOISY_GT, sigma=sigma, root_drift=sigma),
        "missing": train_mod.build_source_meta(obs_mask, train_mod.SOURCE_MISSING),
    }
    preds: dict[str, torch.Tensor] = {}
    losses: dict[str, float] = {}
    gates: dict[str, dict[str, float]] = {}
    for name, source_meta in variants.items():
        pred = model(x_t, t, text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=source_meta)
        loss, _ = train_mod.masked_target_mse(pred, z, loss_mask, task)
        preds[name] = pred
        losses[name] = float(loss.detach().cpu())
        gate = model._trust_gate(source_meta, z.shape[0], z.device, z.dtype)  # v7.2 diagnostic probe.
        gates[name] = {
            "mean": float(gate.mean().detach().cpu()),
            "min": float(gate.min().detach().cpu()),
            "max": float(gate.max().detach().cpu()),
        }
    correct = preds["correct_gt"]
    deltas = {
        name: float(((pred - correct).pow(2) * loss_mask.float()).flatten(1).mean().detach().cpu())
        for name, pred in preds.items()
        if name != "correct_gt"
    }
    return {
        "task": train_mod.TASK_NAMES[task_id],
        "timestep": t_value,
        "sigma": sigma,
        "loss": losses,
        "delta_from_correct": deltas,
        "gate": gates,
        "loss_missing_minus_correct": losses["missing"] - losses["correct_gt"],
        "loss_wrong_minus_correct": losses["wrong_noisy"] - losses["correct_gt"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--split", choices=["train", "val"], default="val")
    parser.add_argument("--diffusion-steps", type=int, default=1000)
    parser.add_argument("--noise-schedule", default="cosine")
    parser.add_argument("--sigmas", type=float, nargs="+", default=[0.05, 0.15, 0.30])
    parser.add_argument("--timesteps", type=int, nargs="+", default=[100, 500, 900])
    parser.add_argument("--seed", type=int, default=20260702)
    args = parser.parse_args()

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    cache_file = args.cache_dir / f"{args.split}.pt"
    ds = train_mod.PulpLatentCache(cache_file)
    batch = next(iter(DataLoader(ds, batch_size=args.batch_size, shuffle=False, num_workers=0)))
    z = batch["z"].to(device)
    text = batch["text"].to(device)
    valid = batch["valid"].to(device)

    checkpoint = torch.load(args.checkpoint, map_location=device)
    model = build_model(checkpoint, device)
    diffusion = train_mod.CondMDIDiffusion(args.diffusion_steps, args.noise_schedule, device)
    results = []
    for timestep in args.timesteps:
        for sigma in args.sigmas:
            results.append(probe_task(model, diffusion, z, text, valid, train_mod.TASK_CAMERA, sigma, timestep, args.seed))
            results.append(probe_task(model, diffusion, z, text, valid, train_mod.TASK_HUMAN, sigma, timestep, args.seed))
    payload = {
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "cache_file": str(cache_file),
        "checkpoint": str(args.checkpoint),
        "batch_size": int(z.shape[0]),
        "sigmas": args.sigmas,
        "timesteps": args.timesteps,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
