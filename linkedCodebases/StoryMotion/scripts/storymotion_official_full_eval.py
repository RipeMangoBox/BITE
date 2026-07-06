#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader, Subset

from storymotion_official_bridge_smoke import (
    batch_from_sample_ids,
    build_pulp,
    decode_feature_and_raw,
    instantiate_official_metrics,
    jsonable,
    load_module,
    load_stage2,
    metric_checkpoint_status,
    metric_values,
    official_outputs_for_task,
    patch_numpy_aliases,
    reference_feature_and_raw,
)


def make_timesteps(num_timesteps: int, num_steps: int, device: torch.device) -> torch.Tensor:
    if num_steps <= 0:
        raise ValueError(f"num_steps must be positive, got {num_steps}")
    ts = torch.linspace(num_timesteps - 1, 0, num_steps, device=device).round().long()
    ts = torch.unique_consecutive(ts)
    if ts.numel() == 0 or int(ts[-1].item()) != 0:
        ts = torch.cat([ts, torch.zeros(1, dtype=torch.long, device=device)])
    return ts


def deterministic_noise(
    shape: tuple[int, int, int],
    sample_indices: list[int],
    seed: int,
    device: torch.device,
    dtype: torch.dtype,
) -> torch.Tensor:
    if shape[0] != len(sample_indices):
        raise ValueError(f"batch shape {shape[0]} does not match sample_indices {len(sample_indices)}")
    parts = []
    for sample_index in sample_indices:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(int(seed) + int(sample_index) * 1_000_003)
        parts.append(torch.randn(shape[1:], generator=generator, dtype=torch.float32))
    return torch.stack(parts, dim=0).to(device=device, dtype=dtype)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_tensor(tensor: torch.Tensor) -> str:
    arr = tensor.detach().cpu().numpy()
    return hashlib.sha256(arr.tobytes()).hexdigest()


def load_h2c_camera_model(story_root: Path, run_dir: Path, device: torch.device):
    h2c_mod = load_module("train_stage2_model_switch_compose", story_root / "scripts/train_stage2_model_switch.py")
    model, run_info = h2c_mod.load_h2c(run_dir, device)
    model.eval()
    return model, h2c_mod, run_info


def load_cache_meta(path: Path) -> dict[str, Any]:
    data = torch.load(path, map_location="cpu")
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    return jsonable(meta)


def extract_alpha(diffusion: Any, t_scalar: int, like: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    a = diffusion.sqrt_alphas_cumprod[int(t_scalar)].to(device=like.device, dtype=like.dtype).view(1, 1, 1)
    b = diffusion.sqrt_one_minus_alphas_cumprod[int(t_scalar)].to(device=like.device, dtype=like.dtype).view(1, 1, 1)
    return a, b


def _make_partial_text(text: torch.Tensor, zero_half: str) -> torch.Tensor:
    """Zero out camera or human half of the text embedding.

    Text layout: first 512 dims = camera text, last 512 dims = human text.
    """
    half = text.shape[1] // 2
    t = text.clone()
    if zero_half == "human":
        t[:, half:] = 0
    elif zero_half == "camera":
        t[:, :half] = 0
    else:
        raise ValueError(f"zero_half must be 'camera' or 'human', got {zero_half!r}")
    return t


def apply_text_intervention(
    text: torch.Tensor,
    intervention: str,
    *,
    generator: torch.Generator,
) -> torch.Tensor:
    """Apply sample-level text interventions for condition-reliance probes."""
    if intervention == "none":
        return text
    half = text.shape[1] // 2
    out = text.clone()
    if intervention == "zero_all":
        return torch.zeros_like(text)
    if intervention == "zero_camera":
        out[:, :half] = 0
        return out
    if intervention == "zero_human":
        out[:, half:] = 0
        return out
    if text.shape[0] < 2 and intervention.startswith("shuffle_"):
        return out
    perm = torch.randperm(text.shape[0], generator=generator, device=text.device)
    if intervention == "shuffle_all":
        return text[perm]
    if intervention == "shuffle_camera":
        out[:, :half] = text[perm, :half]
        return out
    if intervention == "shuffle_human":
        out[:, half:] = text[perm, half:]
        return out
    raise ValueError(f"unknown text intervention: {intervention}")


def apply_observed_latent_intervention(
    z: torch.Tensor,
    task_name: str,
    intervention: str,
    train_mod: Any,
    *,
    generator: torch.Generator,
) -> torch.Tensor:
    """Perturb the observed latent branch for completion condition probes."""
    if intervention == "none" or task_name == "joint":
        return z
    if task_name == "human":
        sl = slice(train_mod.HUM_DIM, None)  # observed camera -> target human
    elif task_name == "camera":
        sl = slice(0, train_mod.HUM_DIM)  # observed human -> target camera
    else:
        raise ValueError(f"unsupported task for observed latent intervention: {task_name}")

    out = z.clone()
    if intervention == "zero":
        out[:, sl, :] = 0
        return out
    if intervention == "shuffle":
        if z.shape[0] < 2:
            return out
        perm = torch.randperm(z.shape[0], generator=generator, device=z.device)
        out[:, sl, :] = z[perm, sl, :]
        return out
    if intervention == "noise_matched":
        block = z[:, sl, :]
        mean = block.mean()
        std = block.std(unbiased=False).clamp_min(1e-6)
        noise = torch.randn(block.shape, generator=generator, device=z.device, dtype=z.dtype)
        out[:, sl, :] = noise * std + mean
        return out
    raise ValueError(f"unknown observed latent intervention: {intervention}")


def apply_joint_camera_latent_intervention(
    x: torch.Tensor,
    intervention: str,
    train_mod: Any,
    *,
    sample_indices: list[int],
    seed: int,
    step_idx: int,
) -> torch.Tensor:
    """Perturb the camera state seen by the JOINT denoiser.

    This is a causal probe for C -> H leakage. It does not change completion
    observed branches; it only changes the camera latent channels in the
    current JOINT sampler state before a model forward pass.
    """
    if intervention == "none":
        return x
    out = x.clone()
    sl = slice(train_mod.HUM_DIM, None)
    if intervention == "zero":
        out[:, sl, :] = 0
        return out
    if intervention == "shuffle":
        if x.shape[0] < 2:
            return out
        generator = torch.Generator(device=x.device)
        generator.manual_seed(int(seed) + 9_000_001 + int(step_idx) * 97)
        perm = torch.randperm(x.shape[0], generator=generator, device=x.device)
        out[:, sl, :] = x[perm, sl, :]
        return out
    if intervention == "noise_matched":
        block = x[:, sl, :]
        mean = block.mean()
        std = block.std(unbiased=False).clamp_min(1e-6)
        noise = deterministic_noise(
            tuple(block.shape),
            sample_indices,
            int(seed) + 9_000_001 + int(step_idx) * 97,
            x.device,
            x.dtype,
        )
        out[:, sl, :] = noise * std + mean
        return out
    raise ValueError(f"unknown joint camera latent intervention: {intervention}")


def apply_joint_human_camera_input_mode(
    x: torch.Tensor,
    mode: str,
    train_mod: Any,
    *,
    sample_indices: list[int],
    seed: int,
    step_idx: int,
) -> torch.Tensor:
    if mode == "normal":
        return x
    out = x.clone()
    sl = slice(train_mod.HUM_DIM, None)
    if mode == "zero":
        out[:, sl, :] = 0
        return out
    if mode == "shuffle":
        if x.shape[0] < 2:
            return out
        generator = torch.Generator(device=x.device)
        generator.manual_seed(int(seed) + 12_000_001 + int(step_idx) * 131)
        perm = torch.randperm(x.shape[0], generator=generator, device=x.device)
        out[:, sl, :] = x[perm, sl, :]
        return out
    if mode == "noise_matched":
        block = x[:, sl, :]
        mean = block.mean()
        std = block.std(unbiased=False).clamp_min(1e-6)
        noise = deterministic_noise(
            tuple(block.shape),
            sample_indices,
            int(seed) + 12_000_001 + int(step_idx) * 131,
            x.device,
            x.dtype,
        )
        out[:, sl, :] = noise * std + mean
        return out
    raise ValueError(f"unknown joint human camera input mode: {mode}")


@torch.no_grad()
def sample_start_x(
    model: torch.nn.Module,
    diffusion: Any,
    train_mod: Any,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task_id: int,
    sample_indices: list[int],
    seed: int,
    num_steps: int,
    *,
    cfg_scale: float = 1.0,
    cfg_human: float | None = None,
    cfg_camera: float | None = None,
    eta: float = 0.0,
    channel_gated_cfg: bool = False,
    joint_camera_latent_intervention: str = "none",
    joint_human_camera_input_mode: str = "normal",
) -> torch.Tensor:
    """DDIM START_X sampler with optional CFG and stochasticity.

    Supports two CFG modes:
    - Standard (single scale): pred = pred_uncond + cfg_scale * (pred_cond - pred_uncond)
    - Bilateral (independent scales): pred = pred_uncond + cfg_camera * (pred_cam - pred_uncond) + cfg_human * (pred_hum - pred_uncond)
      where pred_cam uses only camera text, pred_hum uses only human text.
      With channel_gated_cfg, the camera delta updates only camera latent channels and the human delta updates only human latent channels.

    Args:
        cfg_scale: classifier-free guidance scale (standard mode). 1.0 = no CFG.
        cfg_human: bilateral CFG scale for human text. When set with cfg_camera, enables bilateral mode.
        cfg_camera: bilateral CFG scale for camera text. When set with cfg_human, enables bilateral mode.
        eta: DDIM stochasticity. 0.0 = deterministic, 1.0 = DDPM-like variance.
    """
    if getattr(diffusion, "name", "diffusion") == "rectified_flow":
        return sample_rectified_flow(
            model,
            diffusion,
            train_mod,
            z,
            text,
            valid,
            task_id,
            sample_indices,
            seed,
            num_steps,
            cfg_scale=cfg_scale,
            cfg_human=cfg_human,
            cfg_camera=cfg_camera,
            channel_gated_cfg=channel_gated_cfg,
            joint_camera_latent_intervention=joint_camera_latent_intervention,
            joint_human_camera_input_mode=joint_human_camera_input_mode,
        )

    bilateral = cfg_human is not None and cfg_camera is not None
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, _ = train_mod.make_branch_masks(z, valid, task)
    source_meta = train_mod.build_source_meta(obs_mask, train_mod.SOURCE_GT)
    valid_bc = valid[:, None, :].expand_as(z)
    fixed_mask = obs_mask | (~valid_bc)
    base_noise = deterministic_noise(tuple(z.shape), sample_indices, seed, z.device, z.dtype)
    timesteps = make_timesteps(diffusion.num_timesteps, num_steps, z.device)

    # Prepare partial text embeddings for bilateral CFG or unconditional baseline.
    empty_text = torch.zeros_like(text) if (cfg_scale != 1.0 or bilateral) else None
    cam_text = _make_partial_text(text, "human") if bilateral else None  # zero human half
    hum_text = _make_partial_text(text, "camera") if bilateral else None  # zero camera half

    def rand_noise(step_idx: int) -> torch.Tensor:
        return deterministic_noise(
            tuple(z.shape), sample_indices,
            seed + 1_000_000 + step_idx * 97, z.device, z.dtype,
        )

    def q_gt(t_scalar: int) -> torch.Tensor:
        a, b = extract_alpha(diffusion, t_scalar, z)
        return a * z + b * base_noise

    def model_forward(x_t: torch.Tensor, t_scalar: int, cond_text: torch.Tensor, step_idx: int) -> torch.Tensor:
        t = torch.full((z.shape[0],), t_scalar, dtype=torch.long, device=z.device)
        model_t = diffusion.model_t(t)
        if joint_camera_latent_intervention != "none":
            x_t = apply_joint_camera_latent_intervention(
                x_t,
                joint_camera_latent_intervention,
                train_mod,
                sample_indices=sample_indices,
                seed=seed,
                step_idx=step_idx,
            )
        pred = model(x_t, model_t, cond_text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=source_meta)
        if task_id != train_mod.TASK_JOINT or joint_human_camera_input_mode == "normal":
            return pred
        human_x_t = apply_joint_human_camera_input_mode(
            x_t,
            joint_human_camera_input_mode,
            train_mod,
            sample_indices=sample_indices,
            seed=seed,
            step_idx=step_idx,
        )
        human_pred = model(human_x_t, model_t, cond_text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=source_meta)
        out = pred.clone()
        out[:, : train_mod.HUM_DIM, :] = human_pred[:, : train_mod.HUM_DIM, :]
        return out

    x = torch.where(fixed_mask, q_gt(int(timesteps[0].item())), base_noise)
    pred_x0 = z
    for idx, t_scalar_tensor in enumerate(timesteps):
        t_scalar = int(t_scalar_tensor.item())
        x = torch.where(fixed_mask, q_gt(t_scalar), x)

        if bilateral:
            pred_uncond = model_forward(x, t_scalar, empty_text, idx)
            pred_cam = model_forward(x, t_scalar, cam_text, idx)
            pred_hum = model_forward(x, t_scalar, hum_text, idx)
            delta_cam = pred_cam - pred_uncond
            delta_hum = pred_hum - pred_uncond
            if channel_gated_cfg:
                pred_x0 = pred_uncond.clone()
                pred_x0[:, :train_mod.HUM_DIM] = pred_uncond[:, :train_mod.HUM_DIM] + cfg_human * delta_hum[:, :train_mod.HUM_DIM]
                pred_x0[:, train_mod.HUM_DIM:] = pred_uncond[:, train_mod.HUM_DIM:] + cfg_camera * delta_cam[:, train_mod.HUM_DIM:]
            else:
                pred_x0 = pred_uncond + cfg_camera * delta_cam + cfg_human * delta_hum
        elif cfg_scale == 1.0:
            pred_x0 = model_forward(x, t_scalar, text, idx)
        else:
            pred_cond = model_forward(x, t_scalar, text, idx)
            pred_uncond = model_forward(x, t_scalar, empty_text, idx)
            pred_x0 = pred_uncond + cfg_scale * (pred_cond - pred_uncond)

        pred_for_step = torch.where(fixed_mask, z, pred_x0)
        if idx == timesteps.numel() - 1:
            break
        next_t = int(timesteps[idx + 1].item())
        a_t, b_t = extract_alpha(diffusion, t_scalar, z)
        a_next, b_next = extract_alpha(diffusion, next_t, z)
        eps = (x - a_t * pred_for_step) / b_t.clamp_min(1e-8)

        if eta > 0.0:
            alpha_t = a_t.square()
            alpha_next = a_next.square()
            sigma = eta * torch.sqrt((1.0 - alpha_next) / (1.0 - alpha_t).clamp_min(1e-8)) * torch.sqrt((1.0 - alpha_t / alpha_next).clamp_min(1e-8))
            noise = rand_noise(idx)
            x = a_next * pred_for_step + torch.sqrt((1.0 - alpha_next - sigma.square()).clamp_min(0.0)) * eps + sigma * noise
        else:
            x = a_next * pred_for_step + b_next * eps

        x = torch.where(fixed_mask, q_gt(next_t), x)
    return torch.where(fixed_mask, z, pred_x0)


@torch.no_grad()
def sample_rectified_flow(
    model: torch.nn.Module,
    diffusion: Any,
    train_mod: Any,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task_id: int,
    sample_indices: list[int],
    seed: int,
    num_steps: int,
    *,
    cfg_scale: float = 1.0,
    cfg_human: float | None = None,
    cfg_camera: float | None = None,
    channel_gated_cfg: bool = False,
    joint_camera_latent_intervention: str = "none",
    joint_human_camera_input_mode: str = "normal",
) -> torch.Tensor:
    if num_steps <= 0:
        raise ValueError(f"num_steps must be positive, got {num_steps}")
    bilateral = cfg_human is not None and cfg_camera is not None
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, _ = train_mod.make_branch_masks(z, valid, task)
    source_meta = train_mod.build_source_meta(obs_mask, train_mod.SOURCE_GT)
    valid_bc = valid[:, None, :].expand_as(z)
    fixed_mask = obs_mask | (~valid_bc)
    base_noise = deterministic_noise(tuple(z.shape), sample_indices, seed, z.device, z.dtype)
    times = torch.linspace(0.0, 1.0, num_steps + 1, device=z.device, dtype=z.dtype)

    empty_text = torch.zeros_like(text) if (cfg_scale != 1.0 or bilateral) else None
    cam_text = _make_partial_text(text, "human") if bilateral else None
    hum_text = _make_partial_text(text, "camera") if bilateral else None

    def q_gt(t_scalar: torch.Tensor) -> torch.Tensor:
        t = torch.full((z.shape[0],), float(t_scalar.item()), dtype=torch.float32, device=z.device)
        return diffusion.q_sample(z, t, base_noise)

    def model_forward(x_t: torch.Tensor, t_scalar: torch.Tensor, cond_text: torch.Tensor, step_idx: int) -> torch.Tensor:
        t = torch.full((z.shape[0],), float(t_scalar.item()), dtype=torch.float32, device=z.device)
        model_t = diffusion.model_t(t)
        if joint_camera_latent_intervention != "none":
            x_t = apply_joint_camera_latent_intervention(
                x_t,
                joint_camera_latent_intervention,
                train_mod,
                sample_indices=sample_indices,
                seed=seed,
                step_idx=step_idx,
            )
        pred = model(x_t, model_t, cond_text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=source_meta)
        if task_id != train_mod.TASK_JOINT or joint_human_camera_input_mode == "normal":
            return pred
        human_x_t = apply_joint_human_camera_input_mode(
            x_t,
            joint_human_camera_input_mode,
            train_mod,
            sample_indices=sample_indices,
            seed=seed,
            step_idx=step_idx,
        )
        human_pred = model(human_x_t, model_t, cond_text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=source_meta)
        out = pred.clone()
        out[:, : train_mod.HUM_DIM, :] = human_pred[:, : train_mod.HUM_DIM, :]
        return out

    x = torch.where(fixed_mask, q_gt(times[0]), base_noise)
    for idx in range(num_steps):
        t_scalar = times[idx]
        next_t = times[idx + 1]
        x = torch.where(fixed_mask, q_gt(t_scalar), x)

        if bilateral:
            pred_uncond = model_forward(x, t_scalar, empty_text, idx)
            pred_cam = model_forward(x, t_scalar, cam_text, idx)
            pred_hum = model_forward(x, t_scalar, hum_text, idx)
            delta_cam = pred_cam - pred_uncond
            delta_hum = pred_hum - pred_uncond
            if channel_gated_cfg:
                velocity = pred_uncond.clone()
                velocity[:, :train_mod.HUM_DIM] = pred_uncond[:, :train_mod.HUM_DIM] + cfg_human * delta_hum[:, :train_mod.HUM_DIM]
                velocity[:, train_mod.HUM_DIM:] = pred_uncond[:, train_mod.HUM_DIM:] + cfg_camera * delta_cam[:, train_mod.HUM_DIM:]
            else:
                velocity = pred_uncond + cfg_camera * delta_cam + cfg_human * delta_hum
        elif cfg_scale == 1.0:
            velocity = model_forward(x, t_scalar, text, idx)
        else:
            pred_cond = model_forward(x, t_scalar, text, idx)
            pred_uncond = model_forward(x, t_scalar, empty_text, idx)
            velocity = pred_uncond + cfg_scale * (pred_cond - pred_uncond)

        dt = next_t - t_scalar
        x = x + dt * velocity
        x = torch.where(fixed_mask, q_gt(next_t), x)
    return torch.where(fixed_mask, z, x)


@torch.no_grad()
def sample_composed_human_first_joint(
    human_model: torch.nn.Module,
    human_diffusion: Any,
    h2c_model: torch.nn.Module,
    h2c_mod: Any,
    train_mod: Any,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    sample_indices: list[int],
    seed: int,
    num_steps: int,
    *,
    human_source: str = "generated",
    human_task_name: str = "human_text",
    h2c_source: str = "replay",
    cfg_scale: float = 1.0,
    cfg_human: float | None = None,
    cfg_camera: float | None = None,
    eta: float = 0.0,
    channel_gated_cfg: bool = False,
) -> torch.Tensor:
    """Generate JOINT with explicit H -> C factorization.

    Human is generated first from a human-only task, then camera is generated
    by an asymmetric H2C model conditioned on the generated human latent.
    """
    if human_source == "gt":
        human = z[:, : train_mod.HUM_DIM]
    elif human_source == "generated":
        task_lookup = {name: task for task, name in train_mod.TASK_NAMES.items()}
        if human_task_name not in task_lookup:
            raise ValueError(f"human task {human_task_name!r} is not available in TASK_NAMES={train_mod.TASK_NAMES}")
        human_full = sample_start_x(
            human_model,
            human_diffusion,
            train_mod,
            z,
            text,
            valid,
            task_lookup[human_task_name],
            sample_indices,
            seed,
            num_steps,
            cfg_scale=cfg_scale,
            cfg_human=cfg_human,
            cfg_camera=cfg_camera,
            eta=eta,
            channel_gated_cfg=channel_gated_cfg,
        )
        human = human_full[:, : train_mod.HUM_DIM]
    else:
        raise ValueError(f"unknown composed human source: {human_source}")
    if h2c_source == "clean":
        source_id = h2c_mod.SOURCE_CLEAN
    elif h2c_source == "noisy":
        source_id = h2c_mod.SOURCE_NOISY
    elif h2c_source == "replay":
        source_id = h2c_mod.SOURCE_REPLAY
    else:
        raise ValueError(f"unknown H2C source: {h2c_source}")
    source_type = torch.full((human.shape[0],), source_id, dtype=torch.long, device=human.device)
    sigma = torch.zeros((human.shape[0],), dtype=human.dtype, device=human.device)
    camera = h2c_model(human, text, valid, source_type=source_type, sigma=sigma)
    return torch.cat([human, camera], dim=1)


def collate_cache(cache: Any, start: int, samples: int, batch_size: int, workers: int) -> tuple[DataLoader, int]:
    end = len(cache) if samples <= 0 else min(len(cache), start + samples)
    if start < 0 or start >= len(cache) or end <= start:
        raise ValueError(f"bad sample range start={start}, end={end}, cache_len={len(cache)}")
    loader = DataLoader(Subset(cache, range(start, end)), batch_size=batch_size, shuffle=False, num_workers=workers)
    return loader, end


def write_records(
    handle: Any,
    *,
    task_name: str,
    sample_ids: list[str],
    sample_indices: list[int],
    seed: int,
    run_info: dict[str, Any],
    sampler: dict[str, Any],
) -> None:
    observed = {"camera": "human", "human": "camera", "joint": "none", "human_text": "none"}[task_name]
    target = {"camera": "camera", "human": "human", "joint": "human+camera", "human_text": "human"}[task_name]
    for sample_id, sample_index in zip(sample_ids, sample_indices):
        record = {
            "sample_id": sample_id,
            "sample_index": sample_index,
            "mode": task_name,
            "observed_branch": observed,
            "target_branch": target,
            "seed": seed,
            "per_sample_noise_seed": int(seed) + int(sample_index) * 1_000_003,
            "checkpoint": run_info.get("checkpoint"),
            "checkpoint_step": run_info.get("step"),
            "run_dir": run_info.get("run_dir"),
            "sampler": sampler,
        }
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="StoryMotion full generated eval with PulpMotion official metric callbacks.")
    p.add_argument("--story-root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--cache-dir", type=Path, required=True)
    p.add_argument("--cache-file", default="val.pt")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--records", type=Path)
    p.add_argument("--task", choices=["camera", "human", "joint", "human_text"], required=True)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--split", default="test")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    p.add_argument("--pulp-root", type=Path)
    p.add_argument("--data-root", type=Path)
    p.add_argument("--samples", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--workers", type=int, default=0)
    p.add_argument("--seed", type=int, default=20260613)
    p.add_argument("--num-steps", type=int, default=50)
    p.add_argument("--cfg-scale", type=float, default=1.0, help="Classifier-free guidance scale on text (standard mode). 1.0 = no CFG.")
    p.add_argument("--cfg-human", type=float, default=None, help="Bilateral CFG scale for human text. Requires --cfg-camera. Enables independent bilateral mode.")
    p.add_argument("--cfg-camera", type=float, default=None, help="Bilateral CFG scale for camera text. Requires --cfg-human. Enables independent bilateral mode.")
    p.add_argument("--eta", type=float, default=0.0, help="DDIM stochasticity. 0.0 = deterministic, 1.0 ≈ DDPM variance.")
    p.add_argument("--channel-gated-cfg", action="store_true",
                   help="For bilateral CFG, apply human text guidance only to human latent channels and camera text guidance only to camera latent channels.")
    p.add_argument(
        "--text-intervention",
        choices=["none", "zero_all", "zero_camera", "zero_human", "shuffle_all", "shuffle_camera", "shuffle_human"],
        default="none",
        help="Perturb text embeddings before sampling for condition-reliance probes.",
    )
    p.add_argument(
        "--observed-latent-intervention",
        choices=["none", "zero", "shuffle", "noise_matched"],
        default="none",
        help="Perturb the observed latent branch for camera/human completion probes.",
    )
    p.add_argument(
        "--joint-camera-latent-intervention",
        choices=["none", "zero", "shuffle", "noise_matched"],
        default="none",
        help="For task=joint only, perturb camera latent channels in the sampler state before model forward passes.",
    )
    p.add_argument(
        "--joint-human-camera-input-mode",
        choices=["normal", "zero", "shuffle", "noise_matched"],
        default="normal",
        help="For task=joint only, combine camera prediction from the normal forward pass with human prediction from a forward pass whose camera input channels are perturbed.",
    )
    p.add_argument(
        "--joint-compose-camera-run-dir",
        type=Path,
        help="For task=joint, use explicit human-first composition: sample human with --run-dir, then sample camera with this H2C run.",
    )
    p.add_argument(
        "--joint-compose-human-task",
        choices=["human_text", "human"],
        default="human_text",
        help="Human task used by the --run-dir model during composed JOINT eval. human_text is the intended causal-asymmetric path.",
    )
    p.add_argument(
        "--joint-compose-human-source",
        choices=["generated", "gt"],
        default="generated",
        help="Use generated human for the real composed path, or GT human for pipeline/H2C sanity checks.",
    )
    p.add_argument(
        "--joint-compose-h2c-source",
        choices=["replay", "clean", "noisy"],
        default="replay",
        help="Source type passed to the H2C camera model for generated human latents.",
    )
    p.add_argument("--progress-every", type=int, default=10)
    return p


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    device = torch.device(args.device)
    story_root = args.story_root.resolve()
    pulp_root = (args.pulp_root or story_root / "linked/PulpMotion").resolve()

    train_mod = load_module("train_stage2_condmdi_pulp", story_root / "scripts/train_stage2_condmdi_pulp.py")
    cache_mod = load_module("build_stage2_pulp_latent_cache", story_root / "scripts/build_stage2_pulp_latent_cache.py")
    model, diffusion, run_info = load_stage2(args.run_dir, train_mod, device)
    metric_task_name = "human" if args.task == "human_text" else args.task
    compose_joint = args.task == "joint" and args.joint_compose_camera_run_dir is not None
    h2c_model = h2c_mod = h2c_run_info = None
    if args.joint_compose_camera_run_dir is not None and args.task != "joint":
        raise ValueError("--joint-compose-camera-run-dir is only valid with --task joint")
    if compose_joint:
        h2c_model, h2c_mod, h2c_run_info = load_h2c_camera_model(
            story_root,
            args.joint_compose_camera_run_dir.resolve(),
            device,
        )
    cfg, dataset, autoencoder = build_pulp(cache_mod, story_root, args, device)
    cache = train_mod.PulpLatentCache(args.cache_dir / args.cache_file)
    cache_path = args.cache_dir / args.cache_file
    cache_meta = load_cache_meta(cache_path)
    loader, end = collate_cache(cache, args.start, args.samples, args.batch_size, args.workers)
    task_name = args.task
    task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}[task_name]
    if task_id >= int(run_info.get("num_task_embeddings", 3)):
        raise ValueError(f"run {args.run_dir} does not support task {task_name!r}; num_task_embeddings={run_info.get('num_task_embeddings', 3)}")
    if compose_joint and args.joint_compose_human_source == "generated":
        human_task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}[args.joint_compose_human_task]
        if human_task_id >= int(run_info.get("num_task_embeddings", 3)):
            raise ValueError(
                f"run {args.run_dir} does not support composed human task {args.joint_compose_human_task!r}; "
                f"num_task_embeddings={run_info.get('num_task_embeddings', 3)}"
            )
    callback, module = instantiate_official_metrics(cfg, pulp_root, metric_task_name, device)
    records_path = args.records or args.output.with_suffix(".records.jsonl")
    records_path.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if records_path.exists():
        records_path.unlink()

    process_name = getattr(diffusion, "name", "diffusion")
    sampler = {
        "name": "rf_euler_velocity" if process_name == "rectified_flow" else "ddim_start_x",
        "num_steps": args.num_steps,
        "time_grid": "linspace(0,1,num_steps+1)" if process_name == "rectified_flow" else "round(linspace(T-1,0,num_steps)) unique_consecutive, includes 0",
        "prediction_type": getattr(diffusion, "prediction_type", "START_X"),
        "observed_branch_policy": "inject RF interpolation q(z_gt,t,per_sample_noise) at every step; final merge gt observed branch" if process_name == "rectified_flow" else "inject q(z_gt,t,per_sample_noise) at every step; final merge gt observed branch",
        "padding_policy": "inject RF interpolation q(z_gt,t,per_sample_noise) at every step; final merge gt padded frames" if process_name == "rectified_flow" else "inject q(z_gt,t,per_sample_noise) at every step; final merge gt padded frames",
        "eta": args.eta,
        "cfg_scale": args.cfg_scale,
        "cfg_human": args.cfg_human,
        "cfg_camera": args.cfg_camera,
        "cfg_channel_gated": bool(args.channel_gated_cfg),
        "cfg_mode": ("bilateral_textspace_3pass_channel_gated" if args.channel_gated_cfg else "bilateral_textspace_3pass") if (args.cfg_human is not None and args.cfg_camera is not None) else ("standard_single_cfg" if args.cfg_scale != 1.0 else "conditional_only"),
        "cfg_unconditional_text": "torch.zeros_like(text)" if (args.cfg_scale != 1.0 or (args.cfg_human is not None and args.cfg_camera is not None)) else "not used",
        "joint_camera_latent_intervention": args.joint_camera_latent_intervention,
        "joint_human_camera_input_mode": args.joint_human_camera_input_mode,
        "joint_compose_human_first": bool(compose_joint),
        "joint_compose_human_source": args.joint_compose_human_source if compose_joint else None,
        "joint_compose_human_task": args.joint_compose_human_task if compose_joint else None,
        "joint_compose_h2c_source": args.joint_compose_h2c_source if compose_joint else None,
        "joint_compose_camera_run_dir": str(args.joint_compose_camera_run_dir) if compose_joint else None,
    }
    start_time = time.time()
    processed = 0
    first_batch_summary: dict[str, Any] | None = None
    with records_path.open("a", encoding="utf-8") as records_handle, torch.no_grad():
        for batch_index, batch in enumerate(loader):
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            sample_ids = [str(value) for value in batch["sample_id"]]
            sample_indices = list(range(args.start + processed, args.start + processed + len(sample_ids)))
            batch_generator = torch.Generator(device=device)
            batch_generator.manual_seed(args.seed + args.start + processed * 1009 + batch_index * 9176)
            text_for_sampling = apply_text_intervention(text, args.text_intervention, generator=batch_generator)
            z_for_sampling = apply_observed_latent_intervention(
                z,
                task_name,
                args.observed_latent_intervention,
                train_mod,
                generator=batch_generator,
            )
            pulp_batch = batch_from_sample_ids(dataset, sample_ids, device)
            intrinsics = pulp_batch["x_raw"]["intrinsics"]
            x_input, raw_input = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
            if compose_joint:
                completion = sample_composed_human_first_joint(
                    model,
                    diffusion,
                    h2c_model,
                    h2c_mod,
                    train_mod,
                    z_for_sampling,
                    text_for_sampling,
                    valid,
                    sample_indices,
                    args.seed + 137,
                    args.num_steps,
                    human_source=args.joint_compose_human_source,
                    human_task_name=args.joint_compose_human_task,
                    h2c_source=args.joint_compose_h2c_source,
                    cfg_scale=args.cfg_scale,
                    cfg_human=args.cfg_human,
                    cfg_camera=args.cfg_camera,
                    eta=args.eta,
                    channel_gated_cfg=args.channel_gated_cfg,
                )
            else:
                completion = sample_start_x(
                    model,
                    diffusion,
                    train_mod,
                    z_for_sampling,
                    text_for_sampling,
                    valid,
                    task_id,
                    sample_indices,
                    args.seed + {"camera": 11, "human": 23, "joint": 37, "human_text": 41}[task_name],
                    args.num_steps,
                    cfg_scale=args.cfg_scale,
                    cfg_human=args.cfg_human,
                    cfg_camera=args.cfg_camera,
                    eta=args.eta,
                    channel_gated_cfg=args.channel_gated_cfg,
                    joint_camera_latent_intervention=args.joint_camera_latent_intervention if task_name == "joint" else "none",
                    joint_human_camera_input_mode=args.joint_human_camera_input_mode if task_name == "joint" else "normal",
                )
            x_output, raw_output = decode_feature_and_raw(autoencoder, dataset, train_mod, completion, intrinsics)
            outputs = {"raw_input": raw_input, "raw_output": raw_output, "x_output": x_output}
            official_outputs = official_outputs_for_task(outputs, metric_task_name)
            callback.on_test_batch_end(None, module, official_outputs, pulp_batch, batch_index)
            write_records(
                records_handle,
                task_name=task_name,
                sample_ids=sample_ids,
                sample_indices=sample_indices,
                seed=args.seed,
                run_info=run_info,
                sampler=sampler,
            )
            processed += len(sample_ids)
            if first_batch_summary is None:
                first_batch_summary = {
                    "sample_ids": sample_ids,
                    "cache_z_shape": list(z.shape),
                    "completion_shape": list(completion.shape),
                    "text_intervention": args.text_intervention,
                    "observed_latent_intervention": args.observed_latent_intervention,
                    "joint_compose_human_first": bool(compose_joint),
                    "x_input": jsonable(x_input),
                    "outputs": jsonable(outputs),
                }
            if args.progress_every > 0 and ((batch_index + 1) % args.progress_every == 0 or processed == end - args.start):
                elapsed = time.time() - start_time
                rate = processed / max(elapsed, 1e-9)
                remaining = max(0, (end - args.start) - processed)
                print(
                    json.dumps(
                        {
                            "task": task_name,
                            "processed": processed,
                            "target": end - args.start,
                            "elapsed_sec": elapsed,
                            "eta_sec": remaining / max(rate, 1e-9),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    callback.on_test_epoch_end(None, module)
    metrics = metric_values(module.eval_metrics)
    payload = {
        "mode": "storymotion_generated_eval_with_pulpmotion_official_callbacks",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "task": task_name,
        "metric_task": metric_task_name,
        "scope_note": "Uses PulpMotion official metric callbacks/evaluator components, but StoryMotion model and sampler are custom.",
        "run": run_info,
        "joint_compose": (
            {
                "enabled": True,
                "contract": "H = human generator from human text first; C = asymmetric H2C camera generator conditioned on generated H",
                "human_run": run_info,
                "camera_run": h2c_run_info,
                "human_source": args.joint_compose_human_source,
                "human_task": args.joint_compose_human_task,
                "h2c_source": args.joint_compose_h2c_source,
            }
            if compose_joint
            else {"enabled": False}
        ),
        "cache_dir": str(args.cache_dir),
        "cache_file": args.cache_file,
        "sample_range": [args.start, end],
        "evaluated_samples": processed,
        "split": args.split,
        "set_name": args.set_name,
        "config_name": args.config_name,
        "pulp_root": str(pulp_root),
        "data_root": str(args.data_root or story_root / "linked/pulpmotion-data"),
        "model_dir": str(args.model_dir),
        "metric_checkpoint_status": metric_checkpoint_status(args.model_dir),
        "sampler": sampler,
        "interventions": {
            "text_intervention": args.text_intervention,
            "observed_latent_intervention": args.observed_latent_intervention,
            "joint_camera_latent_intervention": args.joint_camera_latent_intervention if task_name == "joint" else "none",
            "joint_human_camera_input_mode": args.joint_human_camera_input_mode if task_name == "joint" else "normal",
            "joint_compose_human_source": args.joint_compose_human_source if compose_joint else None,
            "joint_compose_human_task": args.joint_compose_human_task if compose_joint else None,
            "joint_compose_h2c_source": args.joint_compose_h2c_source if compose_joint else None,
            "text_layout": "first half camera text, second half human text",
            "observed_latent_layout": "human channels [0,HUM_DIM), camera channels [HUM_DIM,end)",
            "completion_note": "observed latent intervention only changes the observed branch; joint task ignores it",
            "joint_note": "joint camera latent intervention perturbs camera channels in the sampler state before model forward passes; it is intended as a C -> H leakage probe",
        },
        "stage2_process": diffusion.metadata() if hasattr(diffusion, "metadata") else {"generative_process": "diffusion"},
        "diffusion_schedule": (
            {
                "num_train_timesteps": diffusion.num_timesteps,
                "sqrt_alphas_cumprod_sha256": sha256_tensor(diffusion.sqrt_alphas_cumprod),
                "sqrt_one_minus_alphas_cumprod_sha256": sha256_tensor(diffusion.sqrt_one_minus_alphas_cumprod),
                "source": "loaded from StoryMotion checkpoint run meta via modular stage2 process",
            }
            if hasattr(diffusion, "sqrt_alphas_cumprod")
            else {
                "num_train_timesteps": diffusion.num_timesteps,
                "source": "not a diffusion alpha schedule; see stage2_process",
            }
        ),
        "training_conditioning_contract": {
            "forward_policy": "TemporalObsUNet.forward replaces observed x_t positions with clean obs_x0 before concatenating obs_mask.",
            "code_expression": "x = torch.where(obs_mask.bool(), obs_x0, x_t)",
            "implication": "Observed branches are clean GT conditions inside the model, matching training-time CondMDI replacement.",
        },
        "seed": args.seed,
        "batch_size": args.batch_size,
        "device": str(device),
        "cache_meta": cache_meta,
        "script_hashes": {
            "storymotion_official_full_eval.py": sha256_file(Path(__file__).resolve()),
            "storymotion_official_bridge_smoke.py": sha256_file(story_root / "scripts/storymotion_official_bridge_smoke.py"),
            "train_stage2_condmdi_pulp.py": sha256_file(story_root / "scripts/train_stage2_condmdi_pulp.py"),
            "train_stage2_model_switch.py": sha256_file(story_root / "scripts/train_stage2_model_switch.py"),
            "build_stage2_pulp_latent_cache.py": sha256_file(story_root / "scripts/build_stage2_pulp_latent_cache.py"),
        },
        "torch": {
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        },
        "metric_keys": sorted(metrics),
        "metrics": metrics,
        "records_path": str(records_path),
        "first_batch_summary": first_batch_summary,
        "elapsed_sec": time.time() - start_time,
    }
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "wrote": str(args.output),
                "records": str(records_path),
                "task": task_name,
                "samples": processed,
                "keys": len(metrics),
                "elapsed_sec": payload["elapsed_sec"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
