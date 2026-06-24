#!/usr/bin/env python3
"""MoDebug SLAD diagnostics for MoLingo.

M0 is the first closed-loop experiment: token-unmasking trajectory swap with a
single seed. The script also includes the inner-flow GDC/SLAD sampler needed for
follow-up runs, but the default experiment keeps standard CFG active.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path


BASELINE_NAME = "MoLingo"
TRACE = "MoDebug SLAD"
SCOPE_M0 = "m0_token_unmasking_counterfactual_swap"
SCOPE_GDC = "gdc_detector_probe"
DEFAULT_PROMPT_A = "a person walks forward"
DEFAULT_PROMPT_B = "a person runs forward"

np = None
torch = None


def require_runtime_modules() -> None:
    global np, torch
    if np is None:
        import numpy as _np

        np = _np
    if torch is None:
        import torch as _torch

        torch = _torch


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def run_git(args: list[str], cwd: Path) -> str:
    try:
        return subprocess.check_output(args, cwd=str(cwd), text=True, stderr=subprocess.STDOUT).strip()
    except Exception as exc:
        return f"ERROR: {exc}"


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_record(path: str | Path) -> dict:
    p = Path(path).expanduser().resolve()
    return {"path": str(p), "sha256": sha256(p)}


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_int_list(value: str) -> list[int]:
    if not value.strip():
        return []
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def parse_seed_list(value: str) -> list[int]:
    seeds = parse_int_list(value)
    if not seeds:
        raise ValueError("--seeds must contain at least one integer")
    return seeds


def parse_float_list(value: str) -> list[float]:
    if not value.strip():
        return []
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def parse_directions(value: str) -> list[str]:
    directions = [item.strip() for item in value.split(",") if item.strip()]
    unknown = [item for item in directions if item not in {"a_to_b", "b_to_a"}]
    if unknown:
        raise ValueError(f"Unknown directions: {unknown}")
    if not directions:
        raise ValueError("--directions must contain at least one direction")
    return directions


def load_prompt_pairs(args: argparse.Namespace) -> list[dict]:
    rows: list[dict] = []
    if args.prompt_pair_file:
        path = Path(args.prompt_pair_file).expanduser()
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                raise ValueError(f"{path}:{line_no}: expected TSV columns prompt_a, prompt_b[, seconds]")
            seconds = float(parts[2]) if len(parts) >= 3 and parts[2].strip() else args.seconds
            rows.append({"prompt_a": parts[0].strip(), "prompt_b": parts[1].strip(), "seconds": seconds})
    else:
        rows.append({"prompt_a": args.prompt_a, "prompt_b": args.prompt_b, "seconds": args.seconds})

    if args.prompt_pair_limit:
        rows = rows[: args.prompt_pair_limit]
    if not rows:
        raise ValueError("No prompt pairs were provided")
    return rows


def lengths_from_seconds(rows: list[dict], device: str):
    require_runtime_modules()
    # Matches the validated MoLingo diagnostic script.
    token_lens = torch.LongTensor([int(float(row["seconds"]) * 20 // 4) for row in rows]).to(device)
    return (token_lens * 4 * 1.5).int()


def cfg_for_outer_step(base_cfg: float, schedule: str, timestep, **kw) -> object:
    import math

    if schedule == "linear":
        return 1.0 + (base_cfg - 1.0) * timestep
    if schedule == "constant":
        return base_cfg
    if schedule == "exponential":
        lam = float(kw.get("c2fg_lambda", 2.0))
        return base_cfg * math.exp(lam * (1.0 - float(timestep)))
    if schedule == "two_phase":
        split = float(kw.get("ant_split", 0.6))
        omega_high = float(kw.get("ant_omega_high", base_cfg))
        omega_low = float(kw.get("ant_omega_low", 1.5))
        return omega_high if float(timestep) < split else omega_low
    if schedule == "slad_simple":
        # Simplified SLAD: two-phase ω scheduling without GDC/decouple/project.
        # Ablation (Round 4) showed these components contribute nothing.
        # Pre-split: strong CFG to establish semantics → Post-split: weak CFG for quality.
        split = float(kw.get("slad_split", 0.5))
        omega_post = float(kw.get("slad_omega_post", 1.5))
        return base_cfg if float(timestep) < split else omega_post
    raise ValueError(f"Unsupported CFG schedule: {schedule}")


def flatten_batch(x):
    return x.detach().float().reshape(x.shape[0], -1)


def mean_cosine(a, b, eps: float = 1e-8) -> float:
    return float(cosine_per_row(a, b, eps=eps).mean().item())


def cosine_per_row(a, b, eps: float = 1e-8):
    af = flatten_batch(a)
    bf = flatten_batch(b)
    numerator = (af * bf).sum(dim=1)
    denom = torch.linalg.vector_norm(af, dim=1) * torch.linalg.vector_norm(bf, dim=1)
    return numerator / denom.clamp_min(eps)


def group_mean_list(values, groups, num_groups: int) -> list[float | None]:
    if groups is None or num_groups <= 0:
        return []
    result: list[float | None] = []
    for group_idx in range(num_groups):
        mask = groups == group_idx
        if bool(mask.any().item()):
            result.append(float(values[mask].detach().float().mean().item()))
        else:
            result.append(None)
    return result


def stability_scores(
    gdc_by_sample: list[float | None] | None,
    norm_by_sample: list[float | None] | None,
    prev_norm_by_sample: list[float | None] | None,
) -> list[float | None] | None:
    if gdc_by_sample is None or norm_by_sample is None or prev_norm_by_sample is None:
        return None
    scores: list[float | None] = []
    eps = 1e-8
    for gdc, norm, prev_norm in zip(gdc_by_sample, norm_by_sample, prev_norm_by_sample):
        if gdc is None or norm is None or prev_norm is None:
            scores.append(None)
            continue
        norm_ratio = (max(norm, 0.0) + eps) / (max(prev_norm, 0.0) + eps)
        score = max(gdc, 0.0) * math.exp(-abs(math.log(norm_ratio)))
        scores.append(float(score))
    return scores


def normalize_rows(x, eps: float = 1e-8):
    xf = flatten_batch(x)
    denom = torch.linalg.vector_norm(xf, dim=1, keepdim=True).clamp_min(eps)
    return (xf / denom).reshape_as(x)


def project_onto_direction(delta, direction):
    delta_f = flatten_batch(delta)
    direction_f = flatten_batch(direction)
    coeff = (delta_f * direction_f).sum(dim=1, keepdim=True)
    projected = coeff * direction_f
    return projected.reshape_as(delta)


def float_item(value) -> float:
    if hasattr(value, "detach"):
        return float(value.detach().float().mean().item())
    return float(value)


def sample_flow_with_guidance(
    flow_loss,
    z,
    cfg_scale,
    args: argparse.Namespace,
    sample_groups=None,
    num_groups: int = 0,
    outer_step: int = 0,
) -> tuple[object, dict]:
    """Run MoLingo inner rectified-flow sampling with optional GDC/SLAD tracing."""
    require_runtime_modules()
    net = flow_loss.net
    sampler = flow_loss.sampler
    num_samples = z.shape[0] // 2
    trace: list[dict] = []
    prev_delta = None
    semantic_direction = None
    locked = False
    lock_step = None
    stable_count = 0
    sample_stable_counts = [0 for _ in range(num_groups)]
    sample_lock_steps: list[int | None] = [None for _ in range(num_groups)]
    prev_delta_norm_by_sample = None

    def traced_sample_fn(x, t, c, cfg_scale):
        nonlocal prev_delta, semantic_direction, locked, lock_step, stable_count, prev_delta_norm_by_sample

        half = x[: len(x) // 2]
        combined = torch.cat([half, half], dim=0)
        model_out = net.forward(combined, t, c)
        eps, rest = model_out[:, : net.in_channels], model_out[:, net.in_channels :]
        cond_eps, uncond_eps = torch.split(eps, len(eps) // 2, dim=0)
        delta = cond_eps - uncond_eps
        delta_norm_rows = torch.linalg.vector_norm(flatten_batch(delta), dim=1)
        delta_norm_by_sample = (
            group_mean_list(delta_norm_rows, sample_groups, num_groups) if sample_groups is not None else None
        )

        gdc = None
        gdc_by_sample = None
        stability_by_sample = None
        if prev_delta is not None:
            gdc_rows = cosine_per_row(delta, prev_delta)
            gdc = float(gdc_rows.mean().item())
            if sample_groups is not None:
                gdc_by_sample = group_mean_list(gdc_rows, sample_groups, num_groups)
                stability_by_sample = stability_scores(gdc_by_sample, delta_norm_by_sample, prev_delta_norm_by_sample)
                for sample_idx, sample_gdc in enumerate(gdc_by_sample):
                    if sample_gdc is not None and sample_gdc >= args.lock_threshold:
                        sample_stable_counts[sample_idx] += 1
                    else:
                        sample_stable_counts[sample_idx] = 0
                    if sample_lock_steps[sample_idx] is None and sample_stable_counts[sample_idx] >= args.lock_patience:
                        sample_lock_steps[sample_idx] = len(trace)
            if gdc >= args.lock_threshold:
                stable_count += 1
            else:
                stable_count = 0
            if args.guidance_mode == "slad" and not locked and stable_count >= args.lock_patience:
                locked = True
                lock_step = len(trace)
                semantic_direction = normalize_rows(delta)

        # Ablation: fixed-step locking at a predetermined outer step
        if args.guidance_mode == "slad" and args.ablation == "fixed_step" and not locked and outer_step >= args.ablation_fixed_step:
            locked = True
            lock_step = len(trace)
            semantic_direction = normalize_rows(delta)

        if args.guidance_mode == "slad" and locked and semantic_direction is not None:
            if args.ablation == "no_decouple":
                # Post-lock: simple ω scaling, no direction decomposition
                guided_half = uncond_eps + args.ablation_omega_post * delta
            elif args.ablation == "no_project":
                # Post-lock: scale full Δv without projection
                guided_half = uncond_eps + args.omega_sem * delta
            else:
                # Full SLAD: project + decouple
                delta_sem = project_onto_direction(delta, semantic_direction)
                delta_qual = delta - delta_sem
                guided_half = uncond_eps + args.omega_sem * delta_sem + args.omega_qual * delta_qual
        else:
            guided_half = uncond_eps + cfg_scale * delta

        if args.trace_detail != "none":
            record = {
                "inner_step": len(trace),
                "t": float_item(t),
                "cfg_scale": float_item(cfg_scale),
                "gdc": gdc,
                "gdc_by_sample": gdc_by_sample,
                "delta_norm_mean": float(delta_norm_rows.mean().item()),
                "delta_norm_by_sample": delta_norm_by_sample,
                "stability_score_by_sample": stability_by_sample,
                "locked": locked,
            }
            if args.trace_detail == "inner":
                trace.append(record)
            elif args.trace_detail == "aggregate":
                trace.append(record)

        prev_delta = delta.detach()
        prev_delta_norm_by_sample = delta_norm_by_sample
        eps_out = torch.cat([guided_half, guided_half], dim=0)
        return torch.cat([eps_out, rest], dim=1)

    model_kwargs = {"c": z, "cfg_scale": cfg_scale}
    sampler.sample_loop_with_cfg(
        num_samples=num_samples,
        sample_fn=traced_sample_fn,
        num_steps=flow_loss.sample_steps,
        **model_kwargs,
    )
    return sampler.trajectories[-1], summarize_flow_trace(
        trace,
        lock_step,
        locked,
        stable_count,
        args.trace_detail,
        sample_lock_steps=sample_lock_steps,
        sample_stable_counts=sample_stable_counts,
    )


def series_stats_by_sample(trace: list[dict], key: str) -> dict:
    rows = [row.get(key) for row in trace if row.get(key) is not None]
    rows = [row for row in rows if isinstance(row, list)]
    if not rows:
        return {}
    num_groups = max(len(row) for row in rows)
    mean_values: list[float | None] = []
    min_values: list[float | None] = []
    max_values: list[float | None] = []
    last_values: list[float | None] = []
    for sample_idx in range(num_groups):
        values = [row[sample_idx] for row in rows if sample_idx < len(row) and row[sample_idx] is not None]
        if values:
            mean_values.append(float(sum(values) / len(values)))
            min_values.append(float(min(values)))
            max_values.append(float(max(values)))
            last_values.append(float(values[-1]))
        else:
            mean_values.append(None)
            min_values.append(None)
            max_values.append(None)
            last_values.append(None)
    return {"mean": mean_values, "min": min_values, "max": max_values, "last": last_values}


def summarize_flow_trace(
    trace: list[dict],
    lock_step: int | None,
    locked: bool,
    stable_count: int,
    detail: str,
    sample_lock_steps: list[int | None] | None = None,
    sample_stable_counts: list[int] | None = None,
) -> dict:
    gdc_values = [row["gdc"] for row in trace if row.get("gdc") is not None]
    delta_norms = [row["delta_norm_mean"] for row in trace if row.get("delta_norm_mean") is not None]
    gdc_by_sample = series_stats_by_sample(trace, "gdc_by_sample")
    delta_norm_by_sample = series_stats_by_sample(trace, "delta_norm_by_sample")
    stability_by_sample = series_stats_by_sample(trace, "stability_score_by_sample")
    summary = {
        "inner_steps": len(trace),
        "locked": bool(locked),
        "lock_step": lock_step,
        "stable_count_final": int(stable_count),
        "gdc_mean": float(sum(gdc_values) / len(gdc_values)) if gdc_values else None,
        "gdc_min": float(min(gdc_values)) if gdc_values else None,
        "gdc_max": float(max(gdc_values)) if gdc_values else None,
        "gdc_last": float(gdc_values[-1]) if gdc_values else None,
        "delta_norm_first": float(delta_norms[0]) if delta_norms else None,
        "delta_norm_last": float(delta_norms[-1]) if delta_norms else None,
        "sample_lock_steps": sample_lock_steps or [],
        "sample_stable_count_final": sample_stable_counts or [],
    }
    for prefix, stats in [
        ("gdc", gdc_by_sample),
        ("delta_norm", delta_norm_by_sample),
        ("stability_score", stability_by_sample),
    ]:
        for stat_name, values in stats.items():
            summary[f"{prefix}_{stat_name}_by_sample"] = values
    if detail == "inner":
        summary["inner_trace"] = trace
    return summary


def forward_with_guidance_trace(model, x, labels, mask, key_padding_mask, cfg, args: argparse.Namespace, outer_step: int = 0):
    z = model.forward_z(x, labels, key_padding_mask, force_mask=False)
    aux_z = model.forward_z(x, labels, key_padding_mask, force_mask=True)
    mixed_z = torch.cat([z, aux_z], dim=0)
    bsz, seq_len, embed_dim = mixed_z.size()
    num_prompt_samples = bsz // 2

    mask_cat = torch.cat([mask, mask], dim=0).reshape(bsz * seq_len)
    mixed_z = mixed_z.reshape(bsz * seq_len, embed_dim)
    mixed_z = mixed_z[mask_cat]
    sample_groups = (
        torch.arange(num_prompt_samples, device=mask.device)
        .unsqueeze(1)
        .expand(num_prompt_samples, seq_len)[mask]
        .reshape(-1)
    )

    sampled_token_latent, flow_trace = sample_flow_with_guidance(
        model.flow_loss,
        mixed_z,
        cfg,
        args,
        sample_groups=sample_groups,
        num_groups=num_prompt_samples,
        outer_step=outer_step,
    )
    sampled_token_latent, _ = sampled_token_latent.chunk(2, dim=0)
    mask_half, _ = mask_cat.chunk(2, dim=0)
    x_out = x.reshape(bsz // 2 * seq_len, model.token_embed_dim).clone()
    x_out[mask_half.reshape(bsz // 2 * seq_len)] = sampled_token_latent
    sampled_token_latent = x_out.reshape(bsz // 2, seq_len, model.token_embed_dim)
    return sampled_token_latent, flow_trace


def sample_tokens_with_prompt_swap(
    model,
    rows: list[dict],
    lengths,
    seed: int,
    direction: str,
    swap_iteration: int,
    args: argparse.Namespace,
    device: str,
) -> tuple[object, dict]:
    require_runtime_modules()
    from mogen.utils.fixseed import fixseed

    fixseed(seed)
    bsz = len(rows)
    m_lens = lengths // model.unit_length
    seq_len = model.seq_len
    steps = int(seq_len // args.acc)
    if swap_iteration < 0 or swap_iteration > steps:
        raise ValueError(f"swap_iteration must be in [0, {steps}], got {swap_iteration}")

    lengths_to_mask = model.__class__.__dict__["sample_tokens"].__globals__["lengths_to_mask"]
    key_padding_mask = ~lengths_to_mask(m_lens, seq_len).to(device)
    latents = torch.where(
        key_padding_mask.unsqueeze(-1),
        torch.zeros(bsz, seq_len, model.token_embed_dim).to(device),
        model.mask_token.repeat(bsz, seq_len, 1),
    )
    masked_rand_schedule = torch.where(key_padding_mask, 1e5, torch.rand_like(key_padding_mask, dtype=torch.float))

    outer_trace = []
    prompt_first = "prompt_a" if direction == "a_to_b" else "prompt_b"
    prompt_second = "prompt_b" if direction == "a_to_b" else "prompt_a"

    for outer_idx, timestep in enumerate(torch.linspace(0, 1, steps, device=device)):
        rand_mask_prob = torch.cos(timestep * math.pi * 0.5)
        num_masked = torch.round(rand_mask_prob * m_lens).clamp(min=1)
        sorted_indices = masked_rand_schedule.argsort(dim=1)
        ranks = sorted_indices.argsort(dim=1)
        is_mask = ranks < num_masked.unsqueeze(-1)
        latents_masked = torch.where(is_mask.unsqueeze(-1), model.mask_token.repeat(bsz, seq_len, 1), latents)

        # Discrete swap: first swap_iteration outer steps use the first prompt,
        # then all remaining masked-token updates use the second prompt.
        prompt_key = prompt_first if outer_idx < swap_iteration else prompt_second
        labels = [row[prompt_key] for row in rows]
        cfg_iter = cfg_for_outer_step(args.cfg, args.cfg_schedule, timestep, c2fg_lambda=args.c2fg_lambda, ant_split=args.ant_split, ant_omega_high=args.ant_omega_high, ant_omega_low=args.ant_omega_low, slad_split=args.slad_split, slad_omega_post=args.slad_omega_post)

        sampled_tokens, flow_trace = forward_with_guidance_trace(
            model,
            latents_masked,
            labels,
            is_mask,
            key_padding_mask=key_padding_mask,
            cfg=cfg_iter,
            args=args,
            outer_step=outer_idx,
        )
        latents = torch.where(is_mask.unsqueeze(-1), sampled_tokens, latents_masked)
        masked_rand_schedule = masked_rand_schedule.masked_fill(~is_mask, 1e5)

        outer_trace.append(
            {
                "outer_idx": outer_idx,
                "timestep": float_item(timestep),
                "prompt_key": prompt_key,
                "cfg": float_item(cfg_iter),
                "active_mask_tokens": int(is_mask.sum().item()),
                "active_mask_tokens_by_sample": [int(x) for x in is_mask.sum(dim=1).detach().cpu().tolist()],
                "active_mask_mean": float(is_mask.float().mean().item()),
                "flow": flow_trace,
            }
        )

    latents = torch.where(key_padding_mask.unsqueeze(-1), torch.zeros_like(latents), latents)
    trace = {
        "seed": seed,
        "direction": direction,
        "swap_iteration": swap_iteration,
        "outer_steps": steps,
        "seq_len": seq_len,
        "unit_length": int(model.unit_length),
        "trace": outer_trace,
    }
    return latents, trace


def decode_tokens(vae, tokens, std_factor: float):
    with torch.no_grad():
        return vae.decode(tokens / std_factor).detach().cpu().numpy()


def to_numpy_tokens(tokens):
    return tokens.detach().cpu().numpy()


def save_array(path: Path, array) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, array)
    return str(path)


def l2_per_sample(a, b) -> list[float]:
    diff = a - b
    return [float(x) for x in np.linalg.norm(diff.reshape(diff.shape[0], -1), axis=1)]


def mean_list(values: list[float]) -> float:
    return float(sum(values) / len(values)) if values else 0.0


def endpoint_metrics(candidate, endpoint_a, endpoint_b, prefix: str) -> dict:
    d_a = l2_per_sample(candidate, endpoint_a)
    d_b = l2_per_sample(candidate, endpoint_b)
    affinity = [0.5 if (da + db) < 1e-12 else float(db / (da + db)) for da, db in zip(d_a, d_b)]
    gap = l2_per_sample(endpoint_a, endpoint_b)
    return {
        f"{prefix}_l2_to_a_mean": mean_list(d_a),
        f"{prefix}_l2_to_b_mean": mean_list(d_b),
        f"{prefix}_endpoint_gap_l2_mean": mean_list(gap),
        f"{prefix}_affinity_to_a_mean": mean_list(affinity),
        f"{prefix}_l2_to_a": d_a,
        f"{prefix}_l2_to_b": d_b,
        f"{prefix}_affinity_to_a": affinity,
    }


def resolve_swap_iterations(value: str, steps: int) -> list[int]:
    if value.strip().lower() == "all":
        return list(range(steps + 1))
    iterations = parse_int_list(value)
    bad = [idx for idx in iterations if idx < 0 or idx > steps]
    if bad:
        raise ValueError(f"swap iterations out of range [0, {steps}]: {bad}")
    return sorted(set(iterations))


def load_model_bundle(args: argparse.Namespace, device: str) -> dict:
    require_runtime_modules()
    repo_dir = Path(args.repo_dir).expanduser().resolve()
    if str(repo_dir) not in sys.path:
        sys.path.insert(0, str(repo_dir))
    script_dir = Path(__file__).resolve().parent
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    from trace1_full_eval_attention_intervention import load_molingo_model

    model, vae, model_opt, vae_opt, unit_length = load_molingo_model(
        repo_dir, args.dim_pose, device, args.sample_steps, args.t5_path
    )
    return {
        "repo_dir": repo_dir,
        "model": model,
        "vae": vae,
        "model_opt": model_opt,
        "vae_opt": vae_opt,
        "unit_length": unit_length,
    }


def validate_cfg_equivalence(model, rows: list[dict], lengths, seed: int, args: argparse.Namespace, device: str) -> dict:
    from mogen.utils.fixseed import fixseed

    bsz = len(rows)
    m_lens = lengths // model.unit_length
    seq_len = model.seq_len
    lengths_to_mask = model.__class__.__dict__["sample_tokens"].__globals__["lengths_to_mask"]

    fixseed(seed)
    key_padding_mask = ~lengths_to_mask(m_lens, seq_len).to(device)
    latents = torch.where(
        key_padding_mask.unsqueeze(-1),
        torch.zeros(bsz, seq_len, model.token_embed_dim).to(device),
        model.mask_token.repeat(bsz, seq_len, 1),
    )
    masked_rand_schedule = torch.where(key_padding_mask, 1e5, torch.rand_like(key_padding_mask, dtype=torch.float))
    timestep = torch.linspace(0, 1, int(seq_len // args.acc), device=device)[0]
    rand_mask_prob = torch.cos(timestep * math.pi * 0.5)
    num_masked = torch.round(rand_mask_prob * m_lens).clamp(min=1)
    sorted_indices = masked_rand_schedule.argsort(dim=1)
    ranks = sorted_indices.argsort(dim=1)
    is_mask = ranks < num_masked.unsqueeze(-1)
    latents_masked = torch.where(is_mask.unsqueeze(-1), model.mask_token.repeat(bsz, seq_len, 1), latents)
    labels = [row["prompt_a"] for row in rows]
    cfg_iter = cfg_for_outer_step(args.cfg, args.cfg_schedule, timestep)

    old_mode = args.guidance_mode
    args.guidance_mode = "cfg"
    with torch.no_grad():
        fixseed(seed + 991)
        original = model.forward_with_cfg(latents_masked.clone(), labels, is_mask, key_padding_mask, cfg=cfg_iter)
        fixseed(seed + 991)
        custom, flow_trace = forward_with_guidance_trace(
            model, latents_masked.clone(), labels, is_mask, key_padding_mask, cfg_iter, args
        )
    args.guidance_mode = old_mode
    diff = (original - custom).detach().abs()
    return {
        "seed": seed,
        "max_abs": float(diff.max().item()),
        "mean_abs": float(diff.mean().item()),
        "allclose_atol_1e_5": bool(torch.allclose(original, custom, atol=1e-5, rtol=1e-5)),
        "flow_trace": flow_trace,
    }


def capture_rng_state() -> dict:
    return {
        "cpu": torch.random.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
    }


def restore_rng_state(state: dict) -> None:
    torch.random.set_rng_state(state["cpu"])
    if state.get("cuda") is not None:
        torch.cuda.set_rng_state_all(state["cuda"])


def build_manifest_base(args: argparse.Namespace, rows: list[dict], started: float) -> dict:
    repo_dir = Path(args.repo_dir).expanduser().resolve()
    command_script = os.environ.get("MODEBUG_COMMAND_SCRIPT", "")
    return {
        "baseline": BASELINE_NAME,
        "trace": TRACE,
        "scope": SCOPE_M0,
        "created_at": now_iso(),
        "elapsed_sec": time.time() - started,
        "repo_dir": str(repo_dir),
        "repo_git_head": run_git(["git", "rev-parse", "HEAD"], repo_dir) if repo_dir.exists() else "missing_repo",
        "repo_git_branch": run_git(["git", "branch", "--show-current"], repo_dir) if repo_dir.exists() else "missing_repo",
        "repo_git_status_short": (
            run_git(["git", "status", "--short"], repo_dir).splitlines() if repo_dir.exists() else ["missing_repo"]
        ),
        "command": " ".join(sys.argv),
        "wrapper_script": file_record(Path(__file__)),
        "command_script": file_record(command_script) if command_script else {"path": "", "sha256": None},
        "deployed_from": os.environ.get("MODEBUG_DEPLOYED_FROM", ""),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "environment": os.environ.get("CONDA_DEFAULT_ENV", "unknown"),
        "settings": {
            "experiment": args.experiment,
            "guidance_mode": args.guidance_mode,
            "dim_pose": args.dim_pose,
            "cfg": args.cfg,
            "cfg_schedule": args.cfg_schedule,
            "c2fg_lambda": args.c2fg_lambda if args.cfg_schedule == "exponential" else None,
            "ant_split": args.ant_split if args.cfg_schedule == "two_phase" else None,
            "ant_omega_high": args.ant_omega_high if args.cfg_schedule == "two_phase" else None,
            "ant_omega_low": args.ant_omega_low if args.cfg_schedule == "two_phase" else None,
            "slad_split": args.slad_split if args.cfg_schedule == "slad_simple" else None,
            "slad_omega_post": args.slad_omega_post if args.cfg_schedule == "slad_simple" else None,
            "sample_steps": args.sample_steps,
            "acc": args.acc,
            "seeds": parse_seed_list(args.seeds),
            "directions": parse_directions(args.directions),
            "swap_iterations": args.swap_iterations,
            "lock_threshold": args.lock_threshold if args.guidance_mode == "slad" else None,
            "lock_patience": args.lock_patience if args.guidance_mode == "slad" else None,
            "omega_sem": args.omega_sem if args.guidance_mode == "slad" else None,
            "omega_qual": args.omega_qual if args.guidance_mode == "slad" else None,
            "ablation": args.ablation if args.guidance_mode == "slad" else None,
            "ablation_fixed_step": args.ablation_fixed_step if args.ablation == "fixed_step" else None,
            "ablation_omega_post": args.ablation_omega_post if args.ablation == "no_decouple" else None,
            "trace_detail": args.trace_detail,
            "gdc_thresholds": parse_float_list(args.gdc_thresholds),
        },
        "prompt_pairs": rows,
        "t5_path": args.t5_path,
        "limitations": [
            "M0 uses endpoint-distance curves as a trajectory-level diagnostic, not official evaluator metrics.",
            "Semantic action-locking claims require follow-up evaluator or human inspection of saved decoded arrays.",
        ],
    }


def rows_from_gdc_trace(seed: int, prompt_key: str, prompt_rows: list[dict], trace: dict) -> list[dict]:
    metric_rows: list[dict] = []
    prompt_texts = [row[prompt_key] for row in prompt_rows]
    for outer in trace["trace"]:
        flow = outer["flow"]
        metric_rows.append(
            {
                "seed": seed,
                "prompt_key": prompt_key,
                "prompt_texts": prompt_texts,
                "outer_idx": outer["outer_idx"],
                "outer_steps": trace["outer_steps"],
                "timestep": outer["timestep"],
                "cfg": outer["cfg"],
                "num_prompt_pairs": len(prompt_rows),
                "prompt_pairs": prompt_rows,
                "active_mask_tokens": outer["active_mask_tokens"],
                "active_mask_tokens_by_sample": outer.get("active_mask_tokens_by_sample", []),
                "flow_inner_steps": flow.get("inner_steps"),
                "flow_locked": flow.get("locked"),
                "flow_lock_step": flow.get("lock_step"),
                "flow_stable_count_final": flow.get("stable_count_final"),
                "flow_gdc_mean": flow.get("gdc_mean"),
                "flow_gdc_min": flow.get("gdc_min"),
                "flow_gdc_max": flow.get("gdc_max"),
                "flow_gdc_last": flow.get("gdc_last"),
                "flow_gdc_mean_by_sample": flow.get("gdc_mean_by_sample", []),
                "flow_gdc_min_by_sample": flow.get("gdc_min_by_sample", []),
                "flow_gdc_max_by_sample": flow.get("gdc_max_by_sample", []),
                "flow_gdc_last_by_sample": flow.get("gdc_last_by_sample", []),
                "flow_delta_norm_first": flow.get("delta_norm_first"),
                "flow_delta_norm_last": flow.get("delta_norm_last"),
                "flow_delta_norm_mean_by_sample": flow.get("delta_norm_mean_by_sample", []),
                "flow_delta_norm_last_by_sample": flow.get("delta_norm_last_by_sample", []),
                "flow_stability_score_mean_by_sample": flow.get("stability_score_mean_by_sample", []),
                "flow_stability_score_min_by_sample": flow.get("stability_score_min_by_sample", []),
                "flow_stability_score_max_by_sample": flow.get("stability_score_max_by_sample", []),
                "flow_stability_score_last_by_sample": flow.get("stability_score_last_by_sample", []),
                "sample_lock_steps": flow.get("sample_lock_steps", []),
                "sample_stable_count_final": flow.get("sample_stable_count_final", []),
            }
        )
    return metric_rows


def first_outer_at_threshold(rows: list[dict], pair_idx: int, field: str, threshold: float) -> int | None:
    for row in sorted(rows, key=lambda item: item["outer_idx"]):
        values = row.get(field, [])
        if pair_idx < len(values) and values[pair_idx] is not None and values[pair_idx] >= threshold:
            return int(row["outer_idx"])
    return None


def summarize_gdc_metrics(metric_rows: list[dict], prompt_rows: list[dict], thresholds: list[float]) -> dict:
    seeds = sorted({row["seed"] for row in metric_rows})
    prompt_keys = sorted({row["prompt_key"] for row in metric_rows})
    threshold_rows = []
    for seed in seeds:
        for prompt_key in prompt_keys:
            scoped = [row for row in metric_rows if row["seed"] == seed and row["prompt_key"] == prompt_key]
            for pair_idx, pair in enumerate(prompt_rows):
                for threshold in thresholds:
                    threshold_rows.append(
                        {
                            "seed": seed,
                            "prompt_key": prompt_key,
                            "pair_index": pair_idx,
                            "prompt": pair[prompt_key],
                            "threshold": threshold,
                            "first_outer_gdc_mean_ge": first_outer_at_threshold(
                                scoped, pair_idx, "flow_gdc_mean_by_sample", threshold
                            ),
                            "first_outer_stability_mean_ge": first_outer_at_threshold(
                                scoped, pair_idx, "flow_stability_score_mean_by_sample", threshold
                            ),
                        }
                    )
    gdc_values = [row["flow_gdc_mean"] for row in metric_rows if row.get("flow_gdc_mean") is not None]
    stability_values = []
    for row in metric_rows:
        stability_values.extend(
            value for value in row.get("flow_stability_score_mean_by_sample", []) if value is not None
        )
    return {
        "num_metric_rows": len(metric_rows),
        "seeds": seeds,
        "prompt_keys": prompt_keys,
        "outer_steps": max((row["outer_steps"] for row in metric_rows), default=None),
        "thresholds": thresholds,
        "flow_gdc_mean_range": [float(min(gdc_values)), float(max(gdc_values))] if gdc_values else [None, None],
        "flow_stability_score_mean_range": (
            [float(min(stability_values)), float(max(stability_values))] if stability_values else [None, None]
        ),
        "threshold_rows": threshold_rows,
    }


def run_gdc_probe(args: argparse.Namespace) -> int:
    started = time.time()
    rows = load_prompt_pairs(args)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "gdc_metrics.jsonl"
    if metrics_path.exists() and not args.overwrite:
        raise FileExistsError(f"{metrics_path} already exists; pass --overwrite to replace")
    if metrics_path.exists():
        metrics_path.unlink()

    if args.dry_run:
        manifest = build_manifest_base(args, rows, started)
        manifest.update({"scope": SCOPE_GDC, "paper_level_status": "dry_run", "failures": [], "results": {}})
        write_json(out_dir / "manifest.json", manifest)
        print(json.dumps({"manifest": str(out_dir / "manifest.json"), "status": "dry_run"}, indent=2))
        return 0

    require_runtime_modules()
    device = "cuda"
    if not torch.cuda.is_available():
        raise RuntimeError("MoLingo SLAD diagnostics require CUDA because MoLingo hardcodes CUDA modules")

    bundle = load_model_bundle(args, device)
    model = bundle["model"]
    model_opt = bundle["model_opt"]
    vae_opt = bundle["vae_opt"]
    lengths = lengths_from_seconds(rows, device)
    seeds = parse_seed_list(args.seeds)
    steps = int(model.seq_len // args.acc)
    thresholds = parse_float_list(args.gdc_thresholds)

    failures: list[str] = []
    trace_dir = out_dir / "traces"
    all_metric_rows: list[dict] = []

    for seed in seeds:
        for prompt_key, swap_iteration in [("prompt_a", steps), ("prompt_b", 0)]:
            print(f"[GDC] seed={seed}: {prompt_key}", flush=True)
            with torch.no_grad():
                _, trace = sample_tokens_with_prompt_swap(
                    model, rows, lengths, seed, "a_to_b", swap_iteration, args, device
                )
            trace_path = trace_dir / f"seed_{seed}_{prompt_key}_trace.json"
            write_json(trace_path, trace)
            metric_rows = rows_from_gdc_trace(seed, prompt_key, rows, trace)
            append_jsonl(metrics_path, metric_rows)
            all_metric_rows.extend(metric_rows)

    summary = summarize_gdc_metrics(all_metric_rows, rows, thresholds)
    write_json(out_dir / "summary.json", summary)

    manifest = build_manifest_base(args, rows, started)
    dataset = "ms" if args.dim_pose == 272 else "t2m"
    model_dir = bundle["repo_dir"] / "mogen" / "checkpoints" / dataset / f"pretrained_model_{args.dim_pose}"
    vae_dir = bundle["repo_dir"] / "mogen" / "checkpoints" / dataset / model_opt.vae
    manifest.update(
        {
            "scope": SCOPE_GDC,
            "paper_level_status": "gdc_probe_metrics_computed" if not failures else "failed",
            "elapsed_sec": time.time() - started,
            "failures": failures,
            "runtime": {
                "actual_decoder_layers": len(model.seqTransDecoder.layers),
                "seq_len": int(model.seq_len),
                "unit_length": int(bundle["unit_length"]),
                "vae_down_t": int(vae_opt.down_t),
                "std_factor": float(model_opt.std_factor),
            },
            "artifacts": {
                "metrics_jsonl": file_record(metrics_path),
                "summary_json": file_record(out_dir / "summary.json"),
                "trace_dir": str(trace_dir),
                "model_opt": file_record(model_dir / "opt.txt"),
                "model_checkpoint": file_record(model_dir / "net_best_fid.pth"),
                "vae_opt": file_record(vae_dir / "opt.txt"),
                "vae_checkpoint": file_record(vae_dir / "model" / "net_best_fid.ckpt"),
            },
            "summary": summary,
        }
    )
    write_json(out_dir / "manifest.json", manifest)
    print(json.dumps({"manifest": str(out_dir / "manifest.json"), "summary": str(out_dir / "summary.json"), "failures": failures}, indent=2))
    return 2 if failures else 0


def run_m0_swap(args: argparse.Namespace) -> int:
    started = time.time()
    rows = load_prompt_pairs(args)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "swap_metrics.jsonl"
    if metrics_path.exists() and not args.overwrite:
        raise FileExistsError(f"{metrics_path} already exists; pass --overwrite to replace")
    if metrics_path.exists():
        metrics_path.unlink()

    if args.dry_run:
        manifest = build_manifest_base(args, rows, started)
        manifest.update({"paper_level_status": "dry_run", "failures": [], "results": {}})
        write_json(out_dir / "manifest.json", manifest)
        print(json.dumps({"manifest": str(out_dir / "manifest.json"), "status": "dry_run"}, indent=2))
        return 0

    require_runtime_modules()
    device = "cuda"
    if not torch.cuda.is_available():
        raise RuntimeError("MoLingo SLAD diagnostics require CUDA because MoLingo hardcodes CUDA modules")

    bundle = load_model_bundle(args, device)
    model = bundle["model"]
    vae = bundle["vae"]
    model_opt = bundle["model_opt"]
    vae_opt = bundle["vae_opt"]
    lengths = lengths_from_seconds(rows, device)
    seeds = parse_seed_list(args.seeds)
    directions = parse_directions(args.directions)
    steps = int(model.seq_len // args.acc)
    swap_iterations = resolve_swap_iterations(args.swap_iterations, steps)

    failures: list[str] = []
    equivalence = None
    if args.validate_cfg_equivalence:
        rng_state = capture_rng_state()
        equivalence = validate_cfg_equivalence(model, rows, lengths, seeds[0], args, device)
        restore_rng_state(rng_state)
        if not equivalence["allclose_atol_1e_5"]:
            failures.append(f"custom CFG sampler mismatch: {equivalence}")

    summaries = []
    trace_dir = out_dir / "traces"
    array_dir = out_dir / "arrays"

    for seed in seeds:
        print(f"[M0] seed={seed}: endpoint A", flush=True)
        tokens_a, trace_a = sample_tokens_with_prompt_swap(model, rows, lengths, seed, "a_to_b", steps, args, device)
        print(f"[M0] seed={seed}: endpoint B", flush=True)
        tokens_b, trace_b = sample_tokens_with_prompt_swap(model, rows, lengths, seed, "a_to_b", 0, args, device)

        tokens_a_np = to_numpy_tokens(tokens_a)
        tokens_b_np = to_numpy_tokens(tokens_b)
        decoded_a = decode_tokens(vae, tokens_a, model_opt.std_factor)
        decoded_b = decode_tokens(vae, tokens_b, model_opt.std_factor)

        if args.save_arrays:
            save_array(array_dir / f"seed_{seed}" / "endpoint_a_tokens.npy", tokens_a_np)
            save_array(array_dir / f"seed_{seed}" / "endpoint_b_tokens.npy", tokens_b_np)
            save_array(array_dir / f"seed_{seed}" / "endpoint_a_decoded.npy", decoded_a)
            save_array(array_dir / f"seed_{seed}" / "endpoint_b_decoded.npy", decoded_b)

        write_json(trace_dir / f"seed_{seed}_endpoint_a_trace.json", trace_a)
        write_json(trace_dir / f"seed_{seed}_endpoint_b_trace.json", trace_b)

        metric_rows = []
        for direction in directions:
            for swap_iteration in swap_iterations:
                name = f"seed_{seed}_{direction}_swap_{swap_iteration:03d}"
                print(f"[M0] {name}", flush=True)
                tokens_swap, trace_swap = sample_tokens_with_prompt_swap(
                    model, rows, lengths, seed, direction, swap_iteration, args, device
                )
                tokens_swap_np = to_numpy_tokens(tokens_swap)
                decoded_swap = decode_tokens(vae, tokens_swap, model_opt.std_factor)

                if args.save_arrays:
                    save_array(array_dir / f"seed_{seed}" / f"{direction}_swap_{swap_iteration:03d}_tokens.npy", tokens_swap_np)
                    save_array(array_dir / f"seed_{seed}" / f"{direction}_swap_{swap_iteration:03d}_decoded.npy", decoded_swap)
                write_json(trace_dir / f"{name}_trace.json", trace_swap)

                metrics = {
                    "seed": seed,
                    "direction": direction,
                    "swap_iteration": swap_iteration,
                    "outer_steps": steps,
                    "swap_fraction": float(swap_iteration / steps) if steps else 0.0,
                    "num_prompt_pairs": len(rows),
                    "prompt_pairs": rows,
                }
                metrics.update(endpoint_metrics(tokens_swap_np, tokens_a_np, tokens_b_np, "latent"))
                metrics.update(endpoint_metrics(decoded_swap, decoded_a, decoded_b, "decoded"))
                metric_rows.append(metrics)
                summaries.append(
                    {
                        "seed": seed,
                        "direction": direction,
                        "swap_iteration": swap_iteration,
                        "decoded_affinity_to_a_mean": metrics["decoded_affinity_to_a_mean"],
                        "latent_affinity_to_a_mean": metrics["latent_affinity_to_a_mean"],
                    }
                )
        append_jsonl(metrics_path, metric_rows)

    summary = {
        "num_metric_rows": len(summaries),
        "outer_steps": steps,
        "swap_iterations": swap_iterations,
        "decoded_affinity_range": [
            min(row["decoded_affinity_to_a_mean"] for row in summaries) if summaries else None,
            max(row["decoded_affinity_to_a_mean"] for row in summaries) if summaries else None,
        ],
        "latent_affinity_range": [
            min(row["latent_affinity_to_a_mean"] for row in summaries) if summaries else None,
            max(row["latent_affinity_to_a_mean"] for row in summaries) if summaries else None,
        ],
        "rows": summaries,
    }
    write_json(out_dir / "summary.json", summary)

    manifest = build_manifest_base(args, rows, started)
    dataset = "ms" if args.dim_pose == 272 else "t2m"
    model_dir = bundle["repo_dir"] / "mogen" / "checkpoints" / dataset / f"pretrained_model_{args.dim_pose}"
    vae_dir = bundle["repo_dir"] / "mogen" / "checkpoints" / dataset / model_opt.vae
    manifest.update(
        {
            "paper_level_status": "m0_swap_metrics_computed" if not failures else "failed",
            "elapsed_sec": time.time() - started,
            "failures": failures,
            "runtime": {
                "actual_decoder_layers": len(model.seqTransDecoder.layers),
                "seq_len": int(model.seq_len),
                "unit_length": int(bundle["unit_length"]),
                "vae_down_t": int(vae_opt.down_t),
                "std_factor": float(model_opt.std_factor),
            },
            "cfg_equivalence": equivalence,
            "artifacts": {
                "metrics_jsonl": file_record(metrics_path),
                "summary_json": file_record(out_dir / "summary.json"),
                "trace_dir": str(trace_dir),
                "array_dir": str(array_dir) if args.save_arrays else "",
                "model_opt": file_record(model_dir / "opt.txt"),
                "model_checkpoint": file_record(model_dir / "net_best_fid.pth"),
                "vae_opt": file_record(vae_dir / "opt.txt"),
                "vae_checkpoint": file_record(vae_dir / "model" / "net_best_fid.ckpt"),
            },
            "summary": summary,
        }
    )
    write_json(out_dir / "manifest.json", manifest)
    print(json.dumps({"manifest": str(out_dir / "manifest.json"), "summary": str(out_dir / "summary.json"), "failures": failures}, indent=2))
    return 2 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MoDebug SLAD diagnostics for MoLingo")
    parser.add_argument("--experiment", default="m0_swap", choices=["m0_swap", "gdc_probe"])
    parser.add_argument("--repo_dir", default="/data/public/ripemangobox/Motion/MoLingo")
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--prompt_a", default=DEFAULT_PROMPT_A)
    parser.add_argument("--prompt_b", default=DEFAULT_PROMPT_B)
    parser.add_argument("--prompt_pair_file", default="")
    parser.add_argument("--prompt_pair_limit", type=int, default=0)
    parser.add_argument("--seconds", type=float, default=6.0)
    parser.add_argument("--seeds", default="3407")
    parser.add_argument("--directions", default="a_to_b")
    parser.add_argument("--swap_iterations", default="all")
    parser.add_argument("--dim_pose", type=int, default=272)
    parser.add_argument("--cfg", type=float, default=5.5)
    parser.add_argument("--cfg_schedule", default="constant", choices=["constant", "linear", "exponential", "two_phase", "slad_simple"])
    parser.add_argument("--c2fg_lambda", type=float, default=2.0)
    parser.add_argument("--ant_split", type=float, default=0.6)
    parser.add_argument("--ant_omega_high", type=float, default=7.5)
    parser.add_argument("--ant_omega_low", type=float, default=1.5)
    parser.add_argument("--slad_split", type=float, default=0.5, help="Timestep fraction for simplified SLAD two-phase switch (default 0.5 = step 25/50)")
    parser.add_argument("--slad_omega_post", type=float, default=1.5, help="Post-split ω for simplified SLAD (default 1.5)")
    parser.add_argument("--sample_steps", type=int, default=32)
    parser.add_argument("--acc", type=int, default=3)
    parser.add_argument("--t5_path", default="/data/public/ripemangobox/Motion/Text-encoder/t5-large")
    parser.add_argument("--guidance_mode", default="cfg", choices=["cfg", "slad"])
    parser.add_argument("--lock_threshold", type=float, default=0.95)
    parser.add_argument("--lock_patience", type=int, default=3)
    parser.add_argument("--omega_sem", type=float, default=3.0)
    parser.add_argument("--omega_qual", type=float, default=1.0)
    parser.add_argument("--trace_detail", default="aggregate", choices=["none", "aggregate", "inner"])
    parser.add_argument("--gdc_thresholds", default="0.85,0.90,0.95")
    parser.add_argument("--ablation", default="none", choices=["none", "fixed_step", "no_decouple", "no_project"])
    parser.add_argument("--ablation_fixed_step", type=int, default=25)
    parser.add_argument("--ablation_omega_post", type=float, default=1.5)
    parser.add_argument("--validate_cfg_equivalence", action="store_true")
    parser.add_argument("--save_arrays", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry_run", action="store_true")
    args = parser.parse_args()

    if args.experiment == "m0_swap":
        return run_m0_swap(args)
    if args.experiment == "gdc_probe":
        return run_gdc_probe(args)
    raise ValueError(f"Unsupported experiment: {args.experiment}")


if __name__ == "__main__":
    raise SystemExit(main())
