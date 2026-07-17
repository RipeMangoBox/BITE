#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader, Dataset, Subset


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storymotion.stage2.processes import build_stage2_process
from storymotion.experiment_invariants import assert_default_cache_meta, assert_non_causal_cache_meta
from scripts.storymotion_run_layout import init_run, run_paths, update_manifest

for _name, _value in {
    "bool": bool,
    "int": int,
    "float": float,
    "complex": complex,
    "object": object,
    "str": str,
    "unicode": str,
}.items():
    if not hasattr(np, _name):
        setattr(np, _name, _value)

HUM_DIM = 128
CAM_DIM = 64
LATENT_DIM = HUM_DIM + CAM_DIM
LATENT_FRAMES = 75
TEXT_DIM = 1024

TASK_CAMERA = 0
TASK_HUMAN = 1
TASK_JOINT = 2
TASK_HUMAN_TEXT = 3
TASK_NAMES = {TASK_CAMERA: "camera", TASK_HUMAN: "human", TASK_JOINT: "joint", TASK_HUMAN_TEXT: "human_text"}
DEFAULT_TASK_INSTRUCTIONS = {
    TASK_CAMERA: "generate camera trajectory from the observed human motion and camera description",
    TASK_HUMAN: "generate human motion from the observed camera trajectory and human description",
    TASK_JOINT: "generate paired human motion and camera trajectory from human and camera descriptions",
    TASK_HUMAN_TEXT: "generate human motion from the human description without using camera trajectory",
}

SOURCE_GT = 0
SOURCE_NOISY_GT = 1
SOURCE_GENERATED = 2
SOURCE_MISSING = 3
SOURCE_NAMES = {
    SOURCE_GT: "gt",
    SOURCE_NOISY_GT: "noisy_gt",
    SOURCE_GENERATED: "generated",
    SOURCE_MISSING: "missing",
}

TEMPORAL_PATTERN_NAMES = ("span", "prefix", "suffix", "sparse", "mixed")
TEMPORAL_MISSING_RATIO = (0.2, 0.6)


def betas_for_alpha_bar(num_diffusion_timesteps: int, alpha_bar, max_beta: float = 0.999) -> np.ndarray:
    betas = []
    for i in range(num_diffusion_timesteps):
        t1 = i / num_diffusion_timesteps
        t2 = (i + 1) / num_diffusion_timesteps
        betas.append(min(1 - alpha_bar(t2) / alpha_bar(t1), max_beta))
    return np.array(betas, dtype=np.float64)


def get_named_beta_schedule(schedule_name: str, num_diffusion_timesteps: int, scale_betas: float = 1.0) -> np.ndarray:
    if schedule_name == "linear":
        scale = scale_betas * 1000 / num_diffusion_timesteps
        beta_start = scale * 0.0001
        beta_end = scale * 0.02
        return np.linspace(beta_start, beta_end, num_diffusion_timesteps, dtype=np.float64)
    if schedule_name == "cosine":
        return betas_for_alpha_bar(
            num_diffusion_timesteps,
            lambda t: math.cos((t + 0.008) / 1.008 * math.pi / 2) ** 2,
        )
    raise NotImplementedError(f"unknown beta schedule: {schedule_name}")


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def to_jsonable(args: argparse.Namespace) -> dict[str, str]:
    return {k: str(v) for k, v in vars(args).items()}


def timestep_embedding(timesteps: torch.Tensor, dim: int, max_period: int = 10000) -> torch.Tensor:
    half = dim // 2
    freqs = torch.exp(
        -math.log(max_period) * torch.arange(0, half, dtype=torch.float32, device=timesteps.device) / half
    )
    args = timesteps.float()[:, None] * freqs[None]
    emb = torch.cat([torch.cos(args), torch.sin(args)], dim=-1)
    if dim % 2:
        emb = torch.cat([emb, torch.zeros_like(emb[:, :1])], dim=-1)
    return emb


def load_task_instruction_embeddings(path: Path | None) -> tuple[torch.Tensor | None, dict[str, Any]]:
    if path is None:
        return None, {"enabled": False}
    data = torch.load(path, map_location="cpu")
    if isinstance(data, dict):
        tensor = data.get("embeddings", data.get("task_embeddings"))
        labels = data.get("labels", TASK_NAMES)
        texts = data.get("texts", DEFAULT_TASK_INSTRUCTIONS)
    else:
        tensor = data
        labels = TASK_NAMES
        texts = DEFAULT_TASK_INSTRUCTIONS
    if tensor is None:
        raise ValueError(f"{path} must contain an embeddings or task_embeddings tensor")
    tensor = torch.as_tensor(tensor, dtype=torch.float32)
    if tensor.ndim != 2 or tensor.shape[0] not in {3, 4}:
        raise ValueError(f"expected task instruction embeddings [3,D] or [4,D], got {tuple(tensor.shape)}")
    if tensor.shape[0] == 3:
        tensor = torch.cat([tensor, tensor[TASK_HUMAN : TASK_HUMAN + 1]], dim=0)
    return tensor, {
        "enabled": True,
        "path": str(path),
        "shape": list(tensor.shape),
        "labels": labels,
        "texts": texts,
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_sample_ids(sample_ids: list[str]) -> str:
    digest = hashlib.sha256()
    for sample_id in sample_ids:
        digest.update(str(sample_id).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def latent_znorm_default_stats_path(cache_dir: Path) -> Path:
    return cache_dir / "train_latent_znorm.pt"


def _znorm_stat_tensors(stats: dict[str, Any], device: torch.device, dtype: torch.dtype) -> tuple[torch.Tensor, torch.Tensor]:
    mean = torch.as_tensor(stats["mean"], device=device, dtype=dtype).view(1, LATENT_DIM, 1)
    std = torch.as_tensor(stats["std"], device=device, dtype=dtype).view(1, LATENT_DIM, 1)
    return mean, std


def normalize_latent(z: torch.Tensor, valid: torch.Tensor | None, stats: dict[str, Any] | None) -> torch.Tensor:
    if stats is None:
        return z
    mean, std = _znorm_stat_tensors(stats, z.device, z.dtype)
    out = (z - mean) / std
    covariance = stats.get("full_covariance")
    if covariance:
        for start, end, key in ((0, HUM_DIM, "human"), (HUM_DIM, LATENT_DIM, "camera")):
            record = covariance[key]
            chol = torch.as_tensor(record["chol"], device=z.device, dtype=z.dtype)
            cov_mean = torch.as_tensor(record["mean"], device=z.device, dtype=z.dtype)
            flat = out[:, start:end, :].transpose(1, 2).reshape(-1, end - start)
            centered = flat - cov_mean
            whitened = torch.linalg.solve_triangular(chol, centered.transpose(0, 1), upper=False).transpose(0, 1)
            out = out.clone()
            out[:, start:end, :] = whitened.reshape(z.shape[0], z.shape[-1], end - start).transpose(1, 2)
    return out if valid is None else out.masked_fill(~valid[:, None, :].to(out.device), 0.0)


def denormalize_latent(z: torch.Tensor, valid: torch.Tensor | None, stats: dict[str, Any] | None) -> torch.Tensor:
    if stats is None:
        return z
    mean, std = _znorm_stat_tensors(stats, z.device, z.dtype)
    out = z
    covariance = stats.get("full_covariance")
    if covariance:
        for start, end, key in ((0, HUM_DIM, "human"), (HUM_DIM, LATENT_DIM, "camera")):
            record = covariance[key]
            chol = torch.as_tensor(record["chol"], device=z.device, dtype=z.dtype)
            cov_mean = torch.as_tensor(record["mean"], device=z.device, dtype=z.dtype)
            flat = out[:, start:end, :].transpose(1, 2).reshape(-1, end - start)
            flat = flat @ chol.transpose(0, 1) + cov_mean
            out = out.clone()
            out[:, start:end, :] = flat.reshape(z.shape[0], z.shape[-1], end - start).transpose(1, 2)
    out = out * std + mean
    return out if valid is None else out.masked_fill(~valid[:, None, :].to(out.device), 0.0)


def latent_znorm_summary(stats: dict[str, Any]) -> dict[str, Any]:
    mean = torch.as_tensor(stats["mean"]).float().view(-1)
    std = torch.as_tensor(stats["std"]).float().view(-1)
    return {
        "channels": int(mean.numel()),
        "valid_frame_count": int(stats.get("count", 0)),
        "mean_abs_mean": float(mean.abs().mean()),
        "mean_min": float(mean.min()),
        "mean_max": float(mean.max()),
        "std_mean": float(std.mean()),
        "std_min": float(std.min()),
        "std_max": float(std.max()),
        "human_std_mean": float(std[:HUM_DIM].mean()),
        "camera_std_mean": float(std[HUM_DIM:].mean()),
    }


def validate_latent_znorm_stats(stats: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    mean = torch.as_tensor(stats.get("mean")).float().view(-1)
    std = torch.as_tensor(stats.get("std")).float().view(-1)
    where = f" in {path}" if path is not None else ""
    if mean.numel() != LATENT_DIM or std.numel() != LATENT_DIM:
        raise ValueError(f"expected {LATENT_DIM}-channel latent stats{where}")
    if not torch.isfinite(mean).all() or not torch.isfinite(std).all() or (std <= 0).any():
        raise ValueError(f"invalid latent stats{where}")
    result = dict(stats)
    result.update(mean=mean.cpu(), std=std.cpu())
    result["summary"] = latent_znorm_summary(result)
    return result


def compute_latent_znorm_stats(cache_path: Path, eps: float) -> dict[str, Any]:
    data = torch.load(cache_path, map_location="cpu")
    z = data["z"].float()
    valid = data["valid_mask"].bool()
    count = valid.sum()
    if z.shape[1:] != (LATENT_DIM, LATENT_FRAMES) or valid.shape != (z.shape[0], LATENT_FRAMES) or count <= 0:
        raise ValueError(f"invalid latent cache for stats: {cache_path}")
    mask = valid[:, None, :].float()
    mean = (z * mask).sum((0, 2)) / count
    var = ((z - mean[None, :, None]).square() * mask).sum((0, 2)) / count
    stats = {
        "mean": mean.cpu(),
        "std": var.clamp_min(0).sqrt().clamp_min(eps).cpu(),
        "count": int(count),
        "eps": float(eps),
        "source_cache": str(cache_path),
        "source_cache_sha256": sha256_file(cache_path),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }
    stats["summary"] = latent_znorm_summary(stats)
    return stats


def add_full_covariance_stats(cache_path: Path, stats: dict[str, Any], ridge: float) -> dict[str, Any]:
    if ridge <= 0.0:
        raise ValueError("full covariance ridge must be positive")
    data = torch.load(cache_path, map_location="cpu")
    z = data["z"]
    valid = data["valid_mask"].bool()
    mean = torch.as_tensor(stats["mean"], dtype=torch.float32).view(1, LATENT_DIM, 1)
    std = torch.as_tensor(stats["std"], dtype=torch.float32).view(1, LATENT_DIM, 1)
    sums = {"human": torch.zeros(HUM_DIM), "camera": torch.zeros(CAM_DIM)}
    seconds = {"human": torch.zeros(HUM_DIM, HUM_DIM), "camera": torch.zeros(CAM_DIM, CAM_DIM)}
    counts = {"human": 0, "camera": 0}
    chunk_size = 4096
    for start in range(0, z.shape[0], chunk_size):
        end = min(z.shape[0], start + chunk_size)
        normalized = (z[start:end].float() - mean) / std
        frames = normalized.transpose(1, 2)
        frame_valid = valid[start:end]
        for key, sl in (("human", slice(0, HUM_DIM)), ("camera", slice(HUM_DIM, LATENT_DIM))):
            values = frames[:, :, sl][frame_valid]
            sums[key] += values.sum(dim=0)
            seconds[key] += values.transpose(0, 1) @ values
            counts[key] += int(values.shape[0])
    covariance: dict[str, Any] = {}
    for key in ("human", "camera"):
        cov_mean = sums[key] / max(counts[key], 1)
        cov = seconds[key] / max(counts[key], 1) - torch.outer(cov_mean, cov_mean)
        eye = torch.eye(cov.shape[0])
        chol = torch.linalg.cholesky(cov + float(ridge) * eye)
        covariance[key] = {
            "mean": cov_mean,
            "chol": chol,
            "count": counts[key],
            "ridge": float(ridge),
        }
    result = dict(stats)
    result["full_covariance"] = covariance
    result["full_covariance_ridge"] = float(ridge)
    result["summary"] = {**latent_znorm_summary(result), "full_covariance": True, "full_covariance_ridge": float(ridge)}
    return result


def load_latent_znorm_stats(path: Path) -> dict[str, Any]:
    return validate_latent_znorm_stats(torch.load(path, map_location="cpu"), path)


def resolve_latent_znorm_stats(args: argparse.Namespace) -> tuple[dict[str, Any] | None, Path | None]:
    if not args.znorm:
        return None, None
    path = args.znorm_stats_path or latent_znorm_default_stats_path(args.cache_dir)
    if path.exists() and not args.znorm_recompute:
        stats = load_latent_znorm_stats(path)
    else:
        stats = compute_latent_znorm_stats(args.cache_dir / "train.pt", args.znorm_eps)
    if args.full_cov and not stats.get("full_covariance"):
        stats = add_full_covariance_stats(args.cache_dir / "train.pt", stats, args.cov_ridge)
    if not path.exists() or args.znorm_recompute or args.full_cov:
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(stats, path)
    return stats, path


def latent_znorm_meta(enabled: bool, stats: dict[str, Any] | None, path: Path | None, cache_path: Path) -> dict[str, Any]:
    if not enabled:
        return {"enabled": False}
    if stats is None or path is None:
        raise RuntimeError("z-normalization enabled without stats")
    expected_hash = str(stats.get("source_cache_sha256") or sha256_file(cache_path))
    actual_hash = sha256_file(cache_path)
    if expected_hash != actual_hash:
        raise RuntimeError(f"latent stats cache hash mismatch: {expected_hash} != {actual_hash}")
    return {
        "enabled": True,
        "stats_path": str(path),
        "source_cache": str(cache_path),
        "source_cache_sha256": actual_hash,
        "full_covariance": bool(stats.get("full_covariance")),
        "full_covariance_ridge": float(stats.get("full_covariance_ridge", 0.0)),
        "summary": latent_znorm_summary(stats),
    }


def build_geo_tokenizer(args: argparse.Namespace, device: torch.device) -> nn.Module | None:
    """Build the frozen decoder that owns the Stage2 cache contract."""
    if float(args.geo_loss_weight) <= 0.0:
        return None
    if args.geo_tokenizer_checkpoint is None:
        raise ValueError("--geo-tokenizer-checkpoint is required when --geo-loss-weight > 0")
    from scripts.train_storymotion_joint_tokenizer import PRESETS
    from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer

    try:
        config = dict(PRESETS[args.geo_tokenizer_preset])
    except KeyError as exc:
        raise ValueError(f"unknown geo tokenizer preset {args.geo_tokenizer_preset!r}") from exc
    model = build_joint_human_camera_tokenizer(
        str(config["tokenizer"]),
        human_dim=int(config["human_dim"]),
        camera_dim=int(config["camera_dim"]),
        human_latent_dim=int(config["human_latent_dim"]),
        camera_latent_dim=int(config["camera_latent_dim"]),
        hidden_dim=int(config["hidden_dim"]),
        downsample=int(config["downsample"]),
        codebook_size=int(config.get("codebook_size", 512)),
        kl_weight=float(config.get("kl_weight", 1.0e-5)),
        commitment_weight=float(config.get("commitment_weight", 0.02)),
        human_recon_weight=float(config.get("human_recon_weight", 1.0)),
        camera_recon_weight=float(config.get("camera_recon_weight", 1.0)),
        velocity_weight=float(config.get("velocity_weight", 0.5)),
        ema_decay=float(config.get("ema_decay", 0.99)),
        fsq_levels=config.get("fsq_levels"),
        hfsq_groups=int(config.get("hfsq_groups", 8)),
        hfsq_num_quantizers=int(config.get("hfsq_num_quantizers", 2)),
        hfsq_quantize_dropout_prob=float(config.get("hfsq_quantize_dropout_prob", 0.0)),
        hfsq_base_mask_rate=float(config.get("hfsq_base_mask_rate", 0.0)),
        hfsq_r_rand_scale=float(config.get("hfsq_r_rand_scale", 0.0)),
        hfsq_w_scale_division=bool(config.get("hfsq_w_scale_division", False)),
    )
    checkpoint = torch.load(args.geo_tokenizer_checkpoint, map_location=device)
    state = checkpoint.get("model") or checkpoint.get("model_state_dict") or checkpoint.get("state_dict") or checkpoint
    model.load_state_dict(state)
    model.to(device).eval().requires_grad_(False)
    return model


def stage2_to_tokenizer_latent(z: torch.Tensor) -> torch.Tensor:
    if z.ndim != 3 or z.shape[1:] != (LATENT_DIM, LATENT_FRAMES):
        raise RuntimeError(f"expected Stage2 latent [B,{LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
    # Stage2 stores human-first channels; the joint tokenizer decoder consumes camera-first channels.
    return torch.cat([z[:, HUM_DIM:, :], z[:, :HUM_DIM, :]], dim=1).transpose(1, 2).contiguous()


def branch_feature_mse(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    if pred.shape != target.shape:
        raise RuntimeError(f"decoded feature shapes differ: {tuple(pred.shape)} vs {tuple(target.shape)}")
    if mask.shape != pred.shape[:2]:
        raise RuntimeError(f"expected decoded feature mask [B,T], got {tuple(mask.shape)}")
    diff = (pred - target).square()
    denom = mask.float().sum(dim=1).clamp_min(1.0) * pred.shape[-1]
    return (diff * mask[:, :, None].float()).flatten(1).sum(dim=1) / denom


def decoded_geo_loss(
    tokenizer: nn.Module,
    pred_x0: torch.Tensor,
    target_z: torch.Tensor,
    valid: torch.Tensor,
    task: torch.Tensor,
    downsample: int,
    znorm_stats: dict[str, Any] | None,
    velocity_weight: float,
) -> tuple[torch.Tensor, dict[str, float]]:
    frame_mask = valid.repeat_interleave(int(downsample), dim=1)
    target_len = int(frame_mask.shape[1])
    pred_decode_z = denormalize_latent(pred_x0, valid, znorm_stats)
    target_decode_z = denormalize_latent(target_z, valid, znorm_stats)
    pred_human, pred_camera = tokenizer.decode(stage2_to_tokenizer_latent(pred_decode_z), target_len=target_len)
    with torch.no_grad():
        target_human, target_camera = tokenizer.decode(stage2_to_tokenizer_latent(target_decode_z), target_len=target_len)
    frame_mask = frame_mask[:, : pred_human.shape[1]]
    human_per_sample = branch_feature_mse(pred_human, target_human, frame_mask)
    camera_per_sample = branch_feature_mse(pred_camera, target_camera, frame_mask)
    pred_human_velocity = pred_human[:, 1:] - pred_human[:, :-1]
    target_human_velocity = target_human[:, 1:] - target_human[:, :-1]
    pred_camera_velocity = pred_camera[:, 1:] - pred_camera[:, :-1]
    target_camera_velocity = target_camera[:, 1:] - target_camera[:, :-1]
    velocity_mask = frame_mask[:, 1:] & frame_mask[:, :-1]
    human_velocity_per_sample = branch_feature_mse(pred_human_velocity, target_human_velocity, velocity_mask)
    camera_velocity_per_sample = branch_feature_mse(pred_camera_velocity, target_camera_velocity, velocity_mask)
    per_sample = torch.zeros_like(human_per_sample)
    camera_task = task == TASK_CAMERA
    human_task = (task == TASK_HUMAN) | (task == TASK_HUMAN_TEXT)
    joint_task = task == TASK_JOINT
    per_sample[camera_task] = camera_per_sample[camera_task]
    per_sample[human_task] = human_per_sample[human_task]
    per_sample[joint_task] = 0.5 * (human_per_sample[joint_task] + camera_per_sample[joint_task])
    feature_loss = per_sample
    velocity_per_sample = torch.zeros_like(human_velocity_per_sample)
    velocity_per_sample[camera_task] = camera_velocity_per_sample[camera_task]
    velocity_per_sample[human_task] = human_velocity_per_sample[human_task]
    velocity_per_sample[joint_task] = 0.5 * (
        human_velocity_per_sample[joint_task] + camera_velocity_per_sample[joint_task]
    )
    loss = (feature_loss + float(velocity_weight) * velocity_per_sample).mean()
    return loss, {
        "geo_loss": float(loss.detach().cpu()),
        "geo_loss_human_branch": float(human_per_sample.mean().detach().cpu()),
        "geo_loss_camera_branch": float(camera_per_sample.mean().detach().cpu()),
        "geo_feature_loss": float(feature_loss.mean().detach().cpu()),
        "geo_velocity_loss": float(velocity_per_sample.mean().detach().cpu()),
    }


class PulpLatentCache(Dataset):
    def __init__(self, path: Path, znorm_stats: dict[str, Any] | None = None) -> None:
        data = torch.load(path, map_location="cpu")
        z = data["z"].float()
        text = data["text"].float()
        valid = data["valid_mask"].bool()
        if z.ndim != 3 or z.shape[1:] != (LATENT_DIM, LATENT_FRAMES):
            raise ValueError(f"expected z [N,{LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
        if text.ndim != 2 or text.shape[1] != TEXT_DIM:
            raise ValueError(f"expected text [N,{TEXT_DIM}], got {tuple(text.shape)}")
        if valid.shape != (z.shape[0], LATENT_FRAMES):
            raise ValueError(f"expected valid_mask [N,{LATENT_FRAMES}], got {tuple(valid.shape)}")
        self.z = normalize_latent(z, valid, znorm_stats)
        self.text = text
        self.valid = valid
        self.sample_id = data.get("sample_id", [str(i) for i in range(z.shape[0])])
        self.meta = dict(data.get("meta", {}))

    def __len__(self) -> int:
        return int(self.z.shape[0])

    def __getitem__(self, index: int) -> dict[str, Any]:
        return {
            "z": self.z[index],
            "text": self.text[index],
            "valid": self.valid[index],
            "sample_id": self.sample_id[index],
        }


class GroupNorm1d(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        groups = 8
        while channels % groups != 0 and groups > 1:
            groups //= 2
        self.norm = nn.GroupNorm(groups, channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.norm(x)


class ResidualBlock(nn.Module):
    def __init__(self, in_ch: int, out_ch: int, cond_dim: int, zero_second: bool = False) -> None:
        super().__init__()
        self.conv1 = nn.Conv1d(in_ch, out_ch, kernel_size=5, padding=2)
        self.norm1 = GroupNorm1d(out_ch)
        self.conv2 = nn.Conv1d(out_ch, out_ch, kernel_size=5, padding=2)
        self.norm2 = GroupNorm1d(out_ch)
        self.cond = nn.Linear(cond_dim, out_ch * 2)
        self.skip = nn.Conv1d(in_ch, out_ch, kernel_size=1) if in_ch != out_ch else nn.Identity()
        if zero_second:
            nn.init.zeros_(self.conv2.weight)
            nn.init.zeros_(self.conv2.bias)

    def forward(self, x: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        scale, shift = self.cond(cond).chunk(2, dim=-1)
        h = self.norm1(self.conv1(x))
        h = h * (1 + scale[:, :, None]) + shift[:, :, None]
        h = F.mish(h)
        h = F.mish(self.norm2(self.conv2(h)))
        return h + self.skip(x)


class TemporalObsUNet(nn.Module):
    """CondMDI-style temporal UNet with optional v7.2 source/text routing.

    Default behavior is bit-compatible with the original path: replace observed
    x_t with obs_x0, append obs_mask, and condition on the full 1024-dim text.
    v7.2 options are opt-in and only affect runs launched with --v72-* flags.
    """

    def __init__(
        self,
        width: int,
        dim_mults: tuple[int, ...],
        cond_mask_prob: float,
        zero_final: bool,
        cond_mask_prob_cam: float = 0.0,
        cond_mask_prob_hum: float = 0.0,
        v72_text_role_router: bool = False,
        v72_aux_text_scale: float = 0.35,
        v72_soft_source: bool = False,
        v72_trust_gate: bool = False,
        v72_relation_surrogate: bool = False,
        v72_gate_bias: float = 2.0,
        reliability_cond_dim: int = 0,
        task_instruction_embeddings: torch.Tensor | None = None,
        task_instruction_scale: float = 1.0,
        num_task_embeddings: int = 3,
    ) -> None:
        super().__init__()
        self.cond_mask_prob = float(cond_mask_prob)
        self.cond_mask_prob_cam = float(cond_mask_prob_cam)
        self.cond_mask_prob_hum = float(cond_mask_prob_hum)
        self.v72_text_role_router = bool(v72_text_role_router)
        self.v72_aux_text_scale = float(v72_aux_text_scale)
        self.v72_soft_source = bool(v72_soft_source)
        self.v72_trust_gate_enabled = bool(v72_trust_gate)
        self.v72_relation_surrogate = bool(v72_relation_surrogate)
        self.task_instruction_scale = float(task_instruction_scale)
        self.time_mlp = nn.Sequential(
            nn.Linear(width, width * 4),
            nn.Mish(),
            nn.Linear(width * 4, width),
        )
        self.text_mlp = nn.Sequential(
            nn.LayerNorm(TEXT_DIM),
            nn.Linear(TEXT_DIM, width * 4),
            nn.Mish(),
            nn.Linear(width * 4, width),
        )
        self.reliability_cond_dim = int(reliability_cond_dim)
        self.reliability_mlp = (
            nn.Sequential(
                nn.LayerNorm(self.reliability_cond_dim),
                nn.Linear(self.reliability_cond_dim, width * 2),
                nn.Mish(),
                nn.Linear(width * 2, width),
            )
            if self.reliability_cond_dim > 0
            else None
        )
        self.num_task_embeddings = int(num_task_embeddings)
        if self.num_task_embeddings < 3:
            raise ValueError(f"num_task_embeddings must be >= 3, got {self.num_task_embeddings}")
        self.task_embed = (
            nn.Embedding(self.num_task_embeddings, width)
            if self.v72_text_role_router and task_instruction_embeddings is None
            else None
        )
        if task_instruction_embeddings is not None:
            task_instruction_embeddings = torch.as_tensor(task_instruction_embeddings, dtype=torch.float32)
            if task_instruction_embeddings.ndim != 2 or task_instruction_embeddings.shape[0] not in {3, 4}:
                raise ValueError(
                    "task_instruction_embeddings must be [3,D] or [4,D], "
                    f"got {tuple(task_instruction_embeddings.shape)}"
                )
            if task_instruction_embeddings.shape[0] == 3 and self.num_task_embeddings >= 4:
                task_instruction_embeddings = torch.cat(
                    [task_instruction_embeddings, task_instruction_embeddings[TASK_HUMAN : TASK_HUMAN + 1]],
                    dim=0,
                )
            self.register_buffer("task_instruction_embeddings", task_instruction_embeddings)
            self.task_instruction_mlp = nn.Sequential(
                nn.LayerNorm(task_instruction_embeddings.shape[1]),
                nn.Linear(task_instruction_embeddings.shape[1], width * 2),
                nn.Mish(),
                nn.Linear(width * 2, width),
            )
        else:
            self.task_instruction_embeddings = None
            self.task_instruction_mlp = None
        self.source_meta_mlp = nn.Sequential(
            nn.Linear(7, width),
            nn.Mish(),
            nn.Linear(width, width),
        ) if (self.v72_trust_gate_enabled or self.v72_relation_surrogate) else None
        self.source_pool_mlp = nn.Sequential(
            nn.LayerNorm(LATENT_DIM),
            nn.Linear(LATENT_DIM, width),
            nn.Mish(),
            nn.Linear(width, width),
        ) if self.v72_relation_surrogate else None
        self.v72_gate_net = nn.Sequential(
            nn.Linear(7, max(32, width // 4)),
            nn.Mish(),
            nn.Linear(max(32, width // 4), 1),
        ) if self.v72_trust_gate_enabled else None
        if self.v72_gate_net is not None:
            nn.init.constant_(self.v72_gate_net[-1].bias, float(v72_gate_bias))
        channels = [width * m for m in dim_mults]
        self.in_conv = nn.Conv1d(LATENT_DIM * 2, channels[0], kernel_size=1)
        self.downs = nn.ModuleList()
        for idx, ch in enumerate(channels):
            next_ch = channels[min(idx + 1, len(channels) - 1)]
            is_last = idx == len(channels) - 1
            self.downs.append(
                nn.ModuleDict(
                    {
                        "b1": ResidualBlock(ch, ch, width, zero_second=zero_final),
                        "b2": ResidualBlock(ch, ch, width, zero_second=zero_final),
                        "down": nn.Conv1d(ch, next_ch, kernel_size=3, stride=2, padding=1)
                        if not is_last
                        else nn.Identity(),
                    }
                )
            )
        self.mid1 = ResidualBlock(channels[-1], channels[-1], width, zero_second=zero_final)
        self.mid2 = ResidualBlock(channels[-1], channels[-1], width, zero_second=zero_final)
        self.ups = nn.ModuleList()
        for idx in reversed(range(len(channels) - 1)):
            high_ch = channels[idx + 1]
            low_ch = channels[idx]
            self.ups.append(
                nn.ModuleDict(
                    {
                        "up": nn.ConvTranspose1d(high_ch, low_ch, kernel_size=4, stride=2, padding=1),
                        "b1": ResidualBlock(low_ch * 2, low_ch, width, zero_second=zero_final),
                        "b2": ResidualBlock(low_ch, low_ch, width, zero_second=zero_final),
                    }
                )
            )
        self.out = nn.Sequential(GroupNorm1d(channels[0]), nn.Mish(), nn.Conv1d(channels[0], LATENT_DIM, kernel_size=1))
        if zero_final:
            nn.init.zeros_(self.out[-1].weight)
            nn.init.zeros_(self.out[-1].bias)

    def _mask_text(self, text_cond: torch.Tensor) -> torch.Tensor:
        """Apply independent per-modality text dropout for bilateral CFG training.

        Text layout: first 512 dims = camera text, last 512 dims = human text.
        Three independent dropout probabilities:
        - cond_mask_prob: joint dropout (zeros BOTH halves together, legacy behavior)
        - cond_mask_prob_cam: camera-only dropout (zeros only camera text half)
        - cond_mask_prob_hum: human-only dropout (zeros only human text half)

        All three are applied independently, so a sample can have:
        - Both texts intact: (1-p_joint)*(1-p_cam)*(1-p_hum)
        - Only camera text: p_hum but not p_joint or p_cam
        - Only human text: p_cam but not p_joint or p_hum
        - Neither text: any combination
        """
        has_joint = self.training and self.cond_mask_prob > 0
        has_cam = self.training and self.cond_mask_prob_cam > 0
        has_hum = self.training and self.cond_mask_prob_hum > 0

        if not (has_joint or has_cam or has_hum):
            return text_cond

        half = text_cond.shape[-1] // 2  # 512
        text_cam = text_cond[:, :half]
        text_hum = text_cond[:, half:]

        if has_joint:
            joint_keep = 1.0 - torch.bernoulli(
                torch.full((text_cond.shape[0], 1), self.cond_mask_prob, device=text_cond.device)
            )
            text_cam = text_cam * joint_keep
            text_hum = text_hum * joint_keep

        if has_cam:
            cam_keep = 1.0 - torch.bernoulli(
                torch.full((text_cond.shape[0], 1), self.cond_mask_prob_cam, device=text_cond.device)
            )
            text_cam = text_cam * cam_keep

        if has_hum:
            hum_keep = 1.0 - torch.bernoulli(
                torch.full((text_cond.shape[0], 1), self.cond_mask_prob_hum, device=text_cond.device)
            )
            text_hum = text_hum * hum_keep

        return torch.cat([text_cam, text_hum], dim=-1)

    def _route_text(self, text_cond: torch.Tensor, task: torch.Tensor | None) -> torch.Tensor:
        if not self.v72_text_role_router:
            return text_cond
        if task is None:
            return text_cond
        if task.shape != (text_cond.shape[0],):
            raise ValueError(f"expected task [B], got {tuple(task.shape)} for text {tuple(text_cond.shape)}")
        half = text_cond.shape[-1] // 2
        text_cam = text_cond[:, :half]
        text_hum = text_cond[:, half:]
        aux = self.v72_aux_text_scale
        cam_scale = torch.ones((text_cond.shape[0], 1), device=text_cond.device, dtype=text_cond.dtype)
        hum_scale = torch.ones_like(cam_scale)
        # H2C: camera text dominant, human text auxiliary.
        hum_scale = torch.where((task == TASK_CAMERA).view(-1, 1), torch.full_like(hum_scale, aux), hum_scale)
        # C2H: human text dominant, camera text auxiliary.
        human_like = ((task == TASK_HUMAN) | (task == TASK_HUMAN_TEXT)).view(-1, 1)
        cam_scale = torch.where(human_like, torch.full_like(cam_scale, aux), cam_scale)
        return torch.cat([cam_scale * text_cam, hum_scale * text_hum], dim=-1)

    def _source_pool(self, obs_x0: torch.Tensor, obs_mask: torch.Tensor) -> torch.Tensor:
        weight = obs_mask.float()
        denom = weight.sum(dim=-1).clamp_min(1.0)
        return (obs_x0 * weight).sum(dim=-1) / denom

    def _trust_gate(self, source_meta: torch.Tensor | None, batch_size: int, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
        if not self.v72_trust_gate_enabled:
            return torch.ones((batch_size, 1, 1), device=device, dtype=dtype)
        if source_meta is None:
            source_meta = torch.zeros((batch_size, 7), device=device, dtype=dtype)
            source_meta[:, 0] = 1.0  # clean gt by default for backward-compatible eval calls.
        logits = self.v72_gate_net(source_meta.to(device=device, dtype=dtype))
        return torch.sigmoid(logits).view(batch_size, 1, 1)

    @staticmethod
    def _align_time(x: torch.Tensor, target_len: int) -> torch.Tensor:
        if x.shape[-1] == target_len:
            return x
        if x.shape[-1] > target_len:
            return x[..., :target_len]
        return F.pad(x, (0, target_len - x.shape[-1]))

    def forward(
        self,
        x_t: torch.Tensor,
        timesteps: torch.Tensor,
        text: torch.Tensor,
        obs_x0: torch.Tensor,
        obs_mask: torch.Tensor,
        task: torch.Tensor | None = None,
        source_meta: torch.Tensor | None = None,
        reliability_cond: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if x_t.shape != obs_x0.shape or x_t.shape != obs_mask.shape:
            raise ValueError(f"x_t, obs_x0 and obs_mask must match, got {x_t.shape}, {obs_x0.shape}, {obs_mask.shape}")
        gate = self._trust_gate(source_meta, x_t.shape[0], x_t.device, x_t.dtype)
        if self.v72_soft_source:
            x = x_t + obs_mask.float() * gate * (obs_x0 - x_t)
        else:
            x = torch.where(obs_mask.bool(), obs_x0, x_t)
        x = torch.cat([x, obs_mask.float()], dim=1)
        cond = self.time_mlp(timestep_embedding(timesteps, self.time_mlp[0].in_features))
        routed_text = self._route_text(self._mask_text(text), task)
        cond = cond + self.text_mlp(routed_text)
        if self.reliability_mlp is not None:
            if reliability_cond is None:
                reliability_cond = torch.zeros(
                    x_t.shape[0],
                    self.reliability_cond_dim,
                    device=x_t.device,
                    dtype=x_t.dtype,
                )
            if reliability_cond.shape != (x_t.shape[0], self.reliability_cond_dim):
                raise ValueError(
                    f"reliability_cond must be [B,{self.reliability_cond_dim}], "
                    f"got {tuple(reliability_cond.shape)}"
                )
            cond = cond + self.reliability_mlp(reliability_cond.to(device=x_t.device, dtype=x_t.dtype))
        if self.task_embed is not None:
            if task is None:
                task = torch.full((x_t.shape[0],), TASK_JOINT, dtype=torch.long, device=x_t.device)
            cond = cond + self.task_embed(task)
        if self.task_instruction_mlp is not None:
            if task is None:
                task = torch.full((x_t.shape[0],), TASK_JOINT, dtype=torch.long, device=x_t.device)
            task_emb = self.task_instruction_embeddings[task.to(device=x_t.device, dtype=torch.long)]
            cond = cond + self.task_instruction_scale * self.task_instruction_mlp(task_emb.to(dtype=x_t.dtype))
        if self.source_meta_mlp is not None:
            if source_meta is None:
                source_meta = torch.zeros((x_t.shape[0], 7), device=x_t.device, dtype=x_t.dtype)
                source_meta[:, 0] = 1.0
            cond = cond + self.source_meta_mlp(source_meta.to(device=x_t.device, dtype=x_t.dtype))
        if self.source_pool_mlp is not None:
            cond = cond + gate.view(x_t.shape[0], 1) * self.source_pool_mlp(self._source_pool(obs_x0, obs_mask))
        h = self.in_conv(x)
        skips: list[torch.Tensor] = []
        for idx, block in enumerate(self.downs):
            h = block["b1"](h, cond)
            h = block["b2"](h, cond)
            if idx < len(self.downs) - 1:
                skips.append(h)
            h = block["down"](h)
        h = self.mid1(h, cond)
        h = self.mid2(h, cond)
        for block in self.ups:
            skip = skips.pop()
            h = block["up"](h)
            h = self._align_time(h, skip.shape[-1])
            h = torch.cat([h, skip], dim=1)
            h = block["b1"](h, cond)
            h = block["b2"](h, cond)
        return self.out(self._align_time(h, LATENT_FRAMES))


class CondMDIDiffusion:
    def __init__(self, steps: int, schedule: str, device: torch.device, prediction_type: str = "START_X") -> None:
        self._process = build_stage2_process("diffusion", steps, schedule, device, prediction_type)
        self.num_timesteps = self._process.num_timesteps
        self.sqrt_alphas_cumprod = self._process.sqrt_alphas_cumprod
        self.sqrt_one_minus_alphas_cumprod = self._process.sqrt_one_minus_alphas_cumprod
        self.name = self._process.name
        self.prediction_type = self._process.prediction_type

    def q_sample(self, x_start: torch.Tensor, t: torch.Tensor, noise: torch.Tensor) -> torch.Tensor:
        return self._process.q_sample(x_start, t, noise)

    def sample_t(self, batch_size: int, device: torch.device) -> torch.Tensor:
        return self._process.sample_t(batch_size, device)

    def model_t(self, t: torch.Tensor) -> torch.Tensor:
        return self._process.model_t(t)

    def training_target(self, x_start: torch.Tensor, noise: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        return self._process.training_target(x_start, noise, t)

    def prediction_to_x0(self, prediction: torch.Tensor, x_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        return self._process.prediction_to_x0(prediction, x_t, t)

    def metadata(self) -> dict[str, Any]:
        return self._process.metadata()


def sample_tasks(batch_size: int, probs: torch.Tensor, device: torch.device) -> torch.Tensor:
    return torch.multinomial(probs.to(device), batch_size, replacement=True)


def make_branch_masks(
    z: torch.Tensor,
    valid: torch.Tensor,
    task: torch.Tensor,
    task_routing: str = "symmetric",
) -> tuple[torch.Tensor, torch.Tensor]:
    b, _, t = z.shape
    if z.shape[1:] != (LATENT_DIM, LATENT_FRAMES):
        raise RuntimeError(f"expected z [B,{LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
    if valid.shape != (b, t):
        raise RuntimeError(f"expected valid [B,{t}], got {tuple(valid.shape)}")
    if task.shape != (b,):
        raise RuntimeError(f"expected task [B], got {tuple(task.shape)}")
    if task_routing not in {"symmetric", "human_first"}:
        raise RuntimeError(f"unknown task routing: {task_routing}")
    valid_bc = valid[:, None, :].expand(b, LATENT_DIM, t)
    obs = torch.zeros_like(z, dtype=torch.bool)
    camera_task = task == TASK_CAMERA
    human_task = task == TASK_HUMAN
    joint_task = task == TASK_JOINT
    human_text_task = task == TASK_HUMAN_TEXT
    if not torch.all(camera_task | human_task | joint_task | human_text_task):
        raise RuntimeError("unknown task id")
    obs[camera_task, :HUM_DIM, :] = True
    if task_routing == "symmetric":
        obs[human_task, HUM_DIM:, :] = True
    obs = obs & valid_bc
    loss_mask = valid_bc & (~obs)
    if task_routing == "human_first":
        loss_mask[human_task, HUM_DIM:, :] = False
    loss_mask[human_text_task, HUM_DIM:, :] = False
    if torch.any(obs & loss_mask):
        raise RuntimeError("observed and target masks overlap")
    if torch.any((obs | loss_mask) & (~valid_bc)):
        raise RuntimeError("mask extends beyond valid latent frames")
    valid_counts = valid.long().sum(dim=1)
    expected_obs = torch.zeros_like(valid_counts)
    expected_loss = valid_counts * LATENT_DIM
    expected_obs[camera_task] = valid_counts[camera_task] * HUM_DIM
    expected_loss[camera_task] = valid_counts[camera_task] * CAM_DIM
    if task_routing == "symmetric":
        expected_obs[human_task] = valid_counts[human_task] * CAM_DIM
    expected_loss[human_task] = valid_counts[human_task] * HUM_DIM
    expected_loss[human_text_task] = valid_counts[human_text_task] * HUM_DIM
    obs_counts = obs.flatten(1).long().sum(dim=1)
    loss_counts = loss_mask.flatten(1).long().sum(dim=1)
    if not torch.equal(obs_counts.cpu(), expected_obs.cpu()):
        raise RuntimeError(f"unexpected obs counts: {obs_counts.tolist()} vs {expected_obs.tolist()}")
    if not torch.equal(loss_counts.cpu(), expected_loss.cpu()):
        raise RuntimeError(f"unexpected loss counts: {loss_counts.tolist()} vs {expected_loss.tolist()}")
    return obs, loss_mask


def _sample_missing_frames(
    valid: torch.Tensor,
    pattern: torch.Tensor,
) -> torch.Tensor:
    """Sample a non-empty temporal target while keeping at least one valid context frame."""
    if valid.ndim != 2 or pattern.shape != (valid.shape[0],):
        raise RuntimeError(f"invalid temporal sampler shapes: valid={tuple(valid.shape)}, pattern={tuple(pattern.shape)}")
    batch, frames = valid.shape
    device = valid.device
    valid_counts = valid.long().sum(dim=1)
    ratio = torch.empty((batch,), device=device).uniform_(*TEMPORAL_MISSING_RATIO)
    missing_counts = torch.floor(valid_counts.float() * ratio).long()
    missing_counts = torch.maximum(missing_counts, torch.ones_like(missing_counts))
    missing_counts = torch.minimum(missing_counts, (valid_counts - 1).clamp_min(1))
    time = torch.arange(frames, device=device).view(1, frames)

    prefix = time < missing_counts[:, None]
    suffix = (time >= (valid_counts - missing_counts)[:, None]) & valid
    max_start = (valid_counts - missing_counts).clamp_min(0)
    has_interior = max_start >= 2
    interior_width = (max_start - 1).clamp_min(1)
    start_random = torch.rand((batch,), device=device)
    interior_start = 1 + torch.floor(start_random * interior_width.float()).long()
    boundary_start = torch.floor(start_random * (max_start + 1).float()).long()
    span_start = torch.where(has_interior, interior_start, boundary_start)
    span = (time >= span_start[:, None]) & (time < (span_start + missing_counts)[:, None]) & valid

    scores = torch.rand((batch, frames), device=device).masked_fill(~valid, float("inf"))
    order = scores.argsort(dim=1)
    ranks = order.argsort(dim=1)
    sparse = (ranks < missing_counts[:, None]) & valid

    missing = torch.where((pattern == 1)[:, None], prefix, span)
    missing = torch.where((pattern == 2)[:, None], suffix, missing)
    missing = torch.where((pattern == 3)[:, None], sparse, missing)
    return missing & valid


def make_temporal_training_masks(
    z: torch.Tensor,
    valid: torch.Tensor,
    task: torch.Tensor,
    task_routing: str,
    probability: float,
    task_weights: list[float] | tuple[float, float, float],
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict[str, float]]:
    """Mix whole-branch E0 tasks with E2 temporal completion slots.

    Temporal camera slots keep the full human branch and the camera context
    outside the target region. Human slots use only human temporal context.
    Joint slots use temporal context from both branches, with an optional
    independently sampled camera target in the ``mixed`` pattern.
    """
    obs, loss_mask = make_branch_masks(z, valid, task, task_routing=task_routing)
    sample_weight = torch.ones((z.shape[0],), device=z.device, dtype=z.dtype)
    if probability <= 0.0:
        return obs, loss_mask, sample_weight, {}
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"temporal mask probability must be in [0,1], got {probability}")
    if len(task_weights) != 3 or any(float(value) < 0.0 for value in task_weights):
        raise ValueError("temporal mask task weights must contain three non-negative values")

    valid_counts = valid.long().sum(dim=1)
    temporal_task = (task == TASK_CAMERA) | (task == TASK_HUMAN) | (task == TASK_JOINT)
    weight_table = torch.as_tensor(task_weights, device=z.device, dtype=z.dtype)
    temporal_enabled = temporal_task & (weight_table[task.clamp_max(TASK_JOINT)] > 0)
    selected = temporal_enabled & (valid_counts >= 2) & (
        torch.rand((z.shape[0],), device=z.device) < probability
    )
    base_pattern = torch.randint(0, 4, (z.shape[0],), device=z.device)
    mixed = selected & (task == TASK_JOINT) & (torch.rand((z.shape[0],), device=z.device) < 0.2)
    pattern = torch.where(mixed, torch.full_like(base_pattern, 4), base_pattern)
    human_missing = _sample_missing_frames(valid, base_pattern)
    camera_pattern = torch.randint(0, 4, (z.shape[0],), device=z.device)
    camera_missing_independent = _sample_missing_frames(valid, camera_pattern)
    camera_missing = torch.where(mixed[:, None], camera_missing_independent, human_missing)

    valid_bc = valid[:, None, :]
    for task_id in (TASK_CAMERA, TASK_HUMAN, TASK_JOINT):
        chosen = selected & (task == task_id)
        if not chosen.any():
            continue
        obs[chosen] = False
        loss_mask[chosen] = False
        if task_id == TASK_CAMERA:
            obs[chosen, :HUM_DIM, :] = valid_bc[chosen]
            obs[chosen, HUM_DIM:, :] = valid_bc[chosen] & (~camera_missing[chosen, None, :])
            loss_mask[chosen, HUM_DIM:, :] = valid_bc[chosen] & camera_missing[chosen, None, :]
        elif task_id == TASK_HUMAN:
            obs[chosen, :HUM_DIM, :] = valid_bc[chosen] & (~human_missing[chosen, None, :])
            loss_mask[chosen, :HUM_DIM, :] = valid_bc[chosen] & human_missing[chosen, None, :]
        else:
            obs[chosen, :HUM_DIM, :] = valid_bc[chosen] & (~human_missing[chosen, None, :])
            loss_mask[chosen, :HUM_DIM, :] = valid_bc[chosen] & human_missing[chosen, None, :]
            obs[chosen, HUM_DIM:, :] = valid_bc[chosen] & (~camera_missing[chosen, None, :])
            loss_mask[chosen, HUM_DIM:, :] = valid_bc[chosen] & camera_missing[chosen, None, :]

    sample_weight[selected] = weight_table[task[selected]]
    if torch.any(obs & loss_mask) or torch.any((obs | loss_mask) & (~valid_bc)):
        raise RuntimeError("invalid temporal observation/target masks")
    if selected.any() and not loss_mask[selected].flatten(1).any(dim=1).all():
        raise RuntimeError("temporal slot has no target values")

    task_counts = torch.stack([(selected & (task == task_id)).sum() for task_id in range(3)])
    pattern_counts = torch.stack([(selected & (pattern == pattern_id)).sum() for pattern_id in range(5)])
    count_values = torch.cat([task_counts, pattern_counts]).detach().cpu().tolist()
    metrics = {
        "temporal_mask_sample_frac": float(selected.float().mean().detach().cpu()),
        "temporal_mask_effective_sample_frac": float((selected & (sample_weight > 0)).float().mean().detach().cpu()),
        "temporal_mask_loss_weight_mean": float(sample_weight.detach().mean().cpu()),
    }
    for index, name in enumerate(("camera", "human", "joint")):
        metrics[f"_temporal_count_task_{name}"] = float(count_values[index])
    for index, name in enumerate(TEMPORAL_PATTERN_NAMES):
        metrics[f"_temporal_count_pattern_{name}"] = float(count_values[3 + index])
    return obs, loss_mask, sample_weight, metrics


def perturb_joint_camera_input_for_human(
    x: torch.Tensor,
    mode: str,
) -> torch.Tensor:
    if mode == "normal":
        return x
    out = x.clone()
    sl = slice(HUM_DIM, None)
    if mode == "zero":
        out[:, sl, :] = 0
        return out
    if mode == "shuffle":
        if x.shape[0] < 2:
            return out
        perm = torch.randperm(x.shape[0], device=x.device)
        out[:, sl, :] = x[perm, sl, :]
        return out
    if mode == "noise_matched":
        block = x[:, sl, :]
        mean = block.mean()
        std = block.std(unbiased=False).clamp_min(1e-6)
        out[:, sl, :] = torch.randn_like(block) * std + mean
        return out
    raise RuntimeError(f"unknown joint human camera input mode: {mode}")


def predict_with_joint_coupling(
    model: nn.Module,
    x_t: torch.Tensor,
    model_t: torch.Tensor,
    text: torch.Tensor,
    obs_x0: torch.Tensor,
    obs_mask: torch.Tensor,
    task: torch.Tensor,
    source_meta: torch.Tensor,
    coupling_scale: float = 1.0,
    coupling_mode: str = "symmetric",
) -> torch.Tensor:
    """Predict with explicit, bounded human-camera latent/text interaction.

    ``coupling_scale=1`` is exactly the legacy joint forward. At smaller
    scales, the human view attenuates camera latent/text inputs. In
    ``symmetric`` mode the camera view also attenuates human inputs; in
    ``c_to_h_blocked`` mode the camera branch keeps the full joint view so
    H->C interaction remains available while C->H is bounded.
    Non-JOINT tasks always keep the legacy forward because their observed
    branch is part of the task contract.
    """
    scale = float(coupling_scale)
    if not 0.0 <= scale <= 1.0:
        raise ValueError(f"joint coupling scale must be in [0,1], got {scale}")
    if coupling_mode not in {"symmetric", "c_to_h_blocked"}:
        raise ValueError(f"unknown joint coupling mode: {coupling_mode}")
    joint_selected = task == TASK_JOINT
    if scale == 1.0 or not joint_selected.any():
        return model(
            x_t,
            model_t,
            text,
            obs_x0=obs_x0,
            obs_mask=obs_mask,
            task=task,
            source_meta=source_meta,
        )

    text_half = text.shape[-1] // 2
    human_x = x_t.clone()
    human_x[joint_selected, HUM_DIM:, :] *= scale
    human_text = text.clone()
    human_text[joint_selected, :text_half] *= scale
    branch_rng_state = None
    if model.training:
        branch_rng_state = (
            torch.cuda.get_rng_state(x_t.device)
            if x_t.is_cuda
            else torch.get_rng_state()
        )
    human_pred = model(
        human_x,
        model_t,
        human_text,
        obs_x0=obs_x0,
        obs_mask=obs_mask,
        task=task,
        source_meta=source_meta,
    )

    if branch_rng_state is not None:
        if x_t.is_cuda:
            torch.cuda.set_rng_state(branch_rng_state, x_t.device)
        else:
            torch.set_rng_state(branch_rng_state)
    camera_x = x_t.clone()
    camera_text = text.clone()
    if coupling_mode == "symmetric":
        camera_x[joint_selected, :HUM_DIM, :] *= scale
        camera_text[joint_selected, text_half:] *= scale
    camera_pred = model(
        camera_x,
        model_t,
        camera_text,
        obs_x0=obs_x0,
        obs_mask=obs_mask,
        task=task,
        source_meta=source_meta,
    )

    pred = human_pred.clone()
    pred[joint_selected, HUM_DIM:, :] = camera_pred[joint_selected, HUM_DIM:, :]
    return pred


def build_source_meta(
    obs_mask: torch.Tensor,
    source_type: torch.Tensor | int,
    sigma: torch.Tensor | float = 0.0,
    root_drift: torch.Tensor | float = 0.0,
) -> torch.Tensor:
    """Build v7.2 source metadata: 4-way source one-hot + sigma + drift + mask ratio."""
    b = obs_mask.shape[0]
    device = obs_mask.device
    meta = torch.zeros((b, 7), device=device, dtype=torch.float32)
    if isinstance(source_type, int):
        source = torch.full((b,), source_type, dtype=torch.long, device=device)
    else:
        source = source_type.to(device=device, dtype=torch.long).view(b)
    meta.scatter_(1, source.clamp(0, 3).view(-1, 1), 1.0)
    if isinstance(sigma, torch.Tensor):
        meta[:, 4] = sigma.to(device=device, dtype=torch.float32).view(b)
    else:
        meta[:, 4] = float(sigma)
    if isinstance(root_drift, torch.Tensor):
        meta[:, 5] = root_drift.to(device=device, dtype=torch.float32).view(b)
    else:
        meta[:, 5] = float(root_drift)
    meta[:, 6] = obs_mask.float().flatten(1).mean(dim=1)
    return meta


def masked_target_mse(
    pred: torch.Tensor,
    target: torch.Tensor,
    loss_mask: torch.Tensor,
    task: torch.Tensor,
    joint_loss_mode: str = "element_mean",
    joint_human_branch_weight: float = 1.0,
    joint_camera_branch_weight: float = 1.0,
    joint_loss_weight: float = 1.0,
    sample_weights: torch.Tensor | None = None,
) -> tuple[torch.Tensor, dict[str, float]]:
    if joint_human_branch_weight <= 0 or joint_camera_branch_weight <= 0:
        raise RuntimeError("joint branch weights must be positive")
    if joint_loss_weight < 0:
        raise RuntimeError("joint loss weight must be non-negative")
    diff = (pred - target).pow(2)
    mask = loss_mask.float()
    flat_mask = mask.flatten(1)
    per_sample_element = (diff * mask).flatten(1).sum(dim=1) / flat_mask.sum(dim=1).clamp_min(1.0)
    per_sample = per_sample_element

    human_mask = mask[:, :HUM_DIM]
    cam_mask = mask[:, HUM_DIM:]
    human_valid = human_mask.flatten(1).any(dim=1)
    cam_valid = cam_mask.flatten(1).any(dim=1)
    human_loss = (diff[:, :HUM_DIM] * human_mask).flatten(1).sum(dim=1) / human_mask.flatten(1).sum(dim=1).clamp_min(1.0)
    cam_loss = (diff[:, HUM_DIM:] * cam_mask).flatten(1).sum(dim=1) / cam_mask.flatten(1).sum(dim=1).clamp_min(1.0)

    joint_selected = task == TASK_JOINT
    if joint_loss_mode != "element_mean":
        if joint_selected.any():
            per_sample = per_sample.clone()
            if joint_loss_mode == "branch_mean":
                denom = joint_human_branch_weight + joint_camera_branch_weight
                per_sample[joint_selected] = (
                    joint_human_branch_weight * human_loss[joint_selected]
                    + joint_camera_branch_weight * cam_loss[joint_selected]
                ) / denom
            elif joint_loss_mode == "branch_sum":
                per_sample[joint_selected] = (
                    joint_human_branch_weight * human_loss[joint_selected]
                    + joint_camera_branch_weight * cam_loss[joint_selected]
                )
            else:
                raise RuntimeError(f"unknown joint_loss_mode: {joint_loss_mode}")

    per_sample_unweighted = per_sample
    if joint_selected.any() and joint_loss_weight != 1.0:
        per_sample = per_sample.clone()
        per_sample[joint_selected] *= float(joint_loss_weight)
    if sample_weights is not None:
        if sample_weights.shape != per_sample.shape or (sample_weights < 0).any():
            raise RuntimeError(f"invalid sample loss weights: {tuple(sample_weights.shape)}")
        per_sample = per_sample * sample_weights.to(device=per_sample.device, dtype=per_sample.dtype)
    total = per_sample.mean()
    metrics: dict[str, float] = {"loss": float(total.detach().cpu())}
    if sample_weights is not None:
        metrics["sample_loss_weight_mean"] = float(sample_weights.detach().float().mean().cpu())
    if joint_loss_mode != "element_mean":
        metrics["loss_element_mean"] = float(per_sample_element.mean().detach().cpu())
    for task_id, name in TASK_NAMES.items():
        selected = task == task_id
        if selected.any():
            metrics[f"loss_{name}"] = float(per_sample[selected].mean().detach().cpu())
            if task_id == TASK_JOINT:
                metrics["loss_joint_unweighted"] = float(per_sample_unweighted[selected].mean().detach().cpu())
                metrics["joint_loss_weight"] = float(joint_loss_weight)
            if joint_loss_mode != "element_mean" and task_id == TASK_JOINT:
                metrics["loss_joint_element_mean"] = float(per_sample_element[selected].mean().detach().cpu())
                metrics["loss_joint_human_branch"] = float(human_loss[selected].mean().detach().cpu())
                metrics["loss_joint_camera_branch"] = float(cam_loss[selected].mean().detach().cpu())
                metrics["loss_joint_human_branch_weight"] = float(joint_human_branch_weight)
                metrics["loss_joint_camera_branch_weight"] = float(joint_camera_branch_weight)
    if human_mask.any():
        metrics["loss_human_branch"] = float(human_loss[human_valid].mean().detach().cpu())
    if cam_mask.any():
        metrics["loss_camera_branch"] = float(cam_loss[cam_valid].mean().detach().cpu())
    return total, metrics


def make_observed_condition_x0(
    model: nn.Module,
    process: Any,
    x_t: torch.Tensor,
    t: torch.Tensor,
    model_t: torch.Tensor,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    obs_mask: torch.Tensor,
    prob: float,
    mode: str,
    noise_std: float,
    task_routing: str = "symmetric",
    treatment_mask: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor, dict[str, float]]:
    clean_meta = build_source_meta(obs_mask, SOURCE_GT)
    eligible_mask = obs_mask if treatment_mask is None else (obs_mask & treatment_mask)
    if prob <= 0.0 or mode == "clean" or not eligible_mask.any():
        return z, clean_meta, {}
    sample_use = (torch.rand(z.shape[0], device=z.device) < prob).view(-1, 1, 1)
    value_use = sample_use & eligible_mask
    if not value_use.any():
        return z, clean_meta, {"obs_self_condition_sample_frac": 0.0, "obs_self_condition_value_frac": 0.0}

    noisy_candidate = z + noise_std * torch.randn_like(z)
    generated_candidate = None
    generated_sample = torch.zeros_like(sample_use)
    if mode in {"joint_pred", "mixed"}:
        generated_sample = torch.ones_like(sample_use, dtype=torch.bool)
        if mode == "mixed":
            generated_sample = torch.rand(z.shape[0], device=z.device).view(-1, 1, 1) < 0.5
        joint_task = torch.full((z.shape[0],), TASK_JOINT, dtype=torch.long, device=z.device)
        joint_obs_mask, _ = make_branch_masks(z, valid, joint_task, task_routing=task_routing)
        was_training = model.training
        model.eval()
        with torch.no_grad():
            joint_source_meta = build_source_meta(joint_obs_mask, SOURCE_MISSING)
            generated_pred = model(
                x_t.detach(),
                model_t.detach(),
                text.detach(),
                obs_x0=z,
                obs_mask=joint_obs_mask,
                task=joint_task,
                source_meta=joint_source_meta,
            ).detach()
            generated_candidate = process.prediction_to_x0(generated_pred, x_t.detach(), t.detach()).detach()
        model.train(was_training)

    if mode == "noisy":
        candidate = noisy_candidate
    elif mode == "joint_pred":
        candidate = generated_candidate
    elif mode == "mixed":
        if generated_candidate is None:
            raise RuntimeError("mixed observed self-conditioning expected generated candidate")
        candidate = torch.where(generated_sample, generated_candidate, noisy_candidate)
    else:
        raise RuntimeError(f"unknown obs_self_condition_mode: {mode}")

    obs_x0 = torch.where(value_use, candidate.detach(), z)
    source = torch.full((z.shape[0],), SOURCE_GT, dtype=torch.long, device=z.device)
    if mode == "noisy":
        source = torch.where(value_use.flatten(1).any(dim=1), torch.full_like(source, SOURCE_NOISY_GT), source)
    elif mode == "joint_pred":
        source = torch.where(value_use.flatten(1).any(dim=1), torch.full_like(source, SOURCE_GENERATED), source)
    elif mode == "mixed":
        used = value_use.flatten(1).any(dim=1)
        generated_used = (value_use & generated_sample).flatten(1).any(dim=1)
        noisy_used = used & (~generated_used)
        source = torch.where(generated_used, torch.full_like(source, SOURCE_GENERATED), source)
        source = torch.where(noisy_used, torch.full_like(source, SOURCE_NOISY_GT), source)
    sigma = torch.zeros((z.shape[0],), device=z.device)
    if mode in {"noisy", "mixed"}:
        noisy_used = value_use.flatten(1).any(dim=1)
        if mode == "mixed":
            noisy_used = (value_use & (~generated_sample)).flatten(1).any(dim=1)
        sigma = torch.where(noisy_used, torch.full_like(sigma, float(noise_std)), sigma)
    source_meta = build_source_meta(obs_mask, source, sigma=sigma, root_drift=sigma)
    sample_frac = value_use.flatten(1).any(dim=1).float().mean()
    value_frac = value_use.float().mean()
    metrics = {
        "obs_self_condition_sample_frac": float(sample_frac.detach().cpu()),
        "obs_self_condition_value_frac": float(value_frac.detach().cpu()),
        "source_sigma_mean": float(sigma.detach().cpu().mean()),
    }
    for source_id, source_name in SOURCE_NAMES.items():
        metrics[f"source_{source_name}_sample_frac"] = float((source == source_id).float().mean().detach().cpu())
    if mode in {"joint_pred", "mixed"}:
        generated_applied = value_use & generated_sample
        metrics["obs_self_condition_generated_sample_frac"] = float(
            generated_applied.flatten(1).any(dim=1).float().mean().detach().cpu()
        )
    if mode in {"noisy", "mixed"}:
        noisy_applied = value_use & (~generated_sample if mode == "mixed" else torch.ones_like(value_use, dtype=torch.bool))
        metrics["obs_self_condition_noisy_sample_frac"] = float(
            noisy_applied.flatten(1).any(dim=1).float().mean().detach().cpu()
        )
    return obs_x0, source_meta, metrics


def diffusion_loss(
    model: nn.Module,
    diffusion: CondMDIDiffusion,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    task: torch.Tensor,
    noise: torch.Tensor | None = None,
    t: torch.Tensor | None = None,
    joint_loss_mode: str = "element_mean",
    joint_human_branch_weight: float = 1.0,
    joint_camera_branch_weight: float = 1.0,
    joint_loss_weight: float = 1.0,
    task_routing: str = "symmetric",
    obs_self_condition_prob: float = 0.0,
    obs_self_condition_mode: str = "clean",
    obs_self_condition_noise_std: float = 0.0,
    temporal_mask_probability: float = 0.0,
    temporal_mask_task_weights: list[float] | tuple[float, float, float] = (1.0, 1.0, 1.0),
    joint_human_camera_input_mode: str = "normal",
    joint_coupling_scale: float = 1.0,
    joint_coupling_mode: str = "symmetric",
    geo_tokenizer: nn.Module | None = None,
    geo_loss_weight: float = 0.0,
    geo_downsample: int = 4,
    geo_velocity_weight: float = 0.25,
    znorm_stats: dict[str, Any] | None = None,
) -> tuple[torch.Tensor, dict[str, float], torch.Tensor]:
    if noise is None:
        noise = torch.randn_like(z)
    if t is None:
        t = diffusion.sample_t(z.shape[0], z.device)
    obs_mask, loss_mask = make_branch_masks(z, valid, task, task_routing=task_routing)
    sample_loss_weights = None
    temporal_metrics: dict[str, float] = {}
    if temporal_mask_probability > 0.0:
        obs_mask, loss_mask, sample_loss_weights, temporal_metrics = make_temporal_training_masks(
            z,
            valid,
            task,
            task_routing,
            temporal_mask_probability,
            temporal_mask_task_weights,
        )
    x_t = diffusion.q_sample(z, t, noise)
    model_t = diffusion.model_t(t)
    target = diffusion.training_target(z, noise, t)
    source_treatment_mask = torch.zeros_like(obs_mask)
    camera_task = task == TASK_CAMERA
    source_treatment_mask[camera_task, :HUM_DIM, :] = obs_mask[camera_task, :HUM_DIM, :]
    obs_x0, source_meta, obs_metrics = make_observed_condition_x0(
        model,
        diffusion,
        x_t,
        t,
        model_t,
        z,
        text,
        valid,
        obs_mask,
        obs_self_condition_prob,
        obs_self_condition_mode,
        obs_self_condition_noise_std,
        task_routing,
        source_treatment_mask,
    )
    pred = predict_with_joint_coupling(
        model,
        x_t,
        model_t,
        text,
        obs_x0,
        obs_mask,
        task,
        source_meta,
        joint_coupling_scale,
        joint_coupling_mode,
    )
    if pred.shape != z.shape:
        raise RuntimeError(f"model output shape mismatch: {tuple(pred.shape)} vs {tuple(z.shape)}")
    pred_for_loss = pred
    joint_selected = task == TASK_JOINT
    if joint_human_camera_input_mode != "normal" and joint_selected.any():
        x_t_human = perturb_joint_camera_input_for_human(x_t, joint_human_camera_input_mode)
        pred_human_view = model(
            x_t_human,
            model_t,
            text,
            obs_x0=obs_x0,
            obs_mask=obs_mask,
            task=task,
            source_meta=source_meta,
        )
        pred_for_loss = pred.clone()
        pred_for_loss[joint_selected, :HUM_DIM, :] = pred_human_view[joint_selected, :HUM_DIM, :]
    loss, metrics = masked_target_mse(
        pred_for_loss,
        target,
        loss_mask,
        task,
        joint_loss_mode=joint_loss_mode,
        joint_human_branch_weight=joint_human_branch_weight,
        joint_camera_branch_weight=joint_camera_branch_weight,
        joint_loss_weight=joint_loss_weight,
        sample_weights=sample_loss_weights,
    )
    if geo_tokenizer is not None and float(geo_loss_weight) > 0.0:
        latent_loss = loss
        geo_loss, geo_metrics = decoded_geo_loss(
            geo_tokenizer,
            diffusion.prediction_to_x0(pred_for_loss, x_t, t),
            z,
            valid,
            task,
            geo_downsample,
            znorm_stats,
            geo_velocity_weight,
        )
        loss = latent_loss + float(geo_loss_weight) * geo_loss
        metrics.update(
            {
                "loss_latent": float(latent_loss.detach().cpu()),
                **geo_metrics,
                "geo_loss_weight": float(geo_loss_weight),
                "geo_loss_weighted": float((float(geo_loss_weight) * geo_loss).detach().cpu()),
                "loss": float(loss.detach().cpu()),
            }
        )
    if joint_human_camera_input_mode != "normal":
        metrics["joint_human_camera_input_mode_active"] = float(joint_selected.float().mean().detach().cpu())
    metrics["joint_coupling_scale"] = float(joint_coupling_scale)
    metrics.update(obs_metrics)
    metrics.update(temporal_metrics)
    return loss, metrics, pred


@torch.no_grad()
def evaluate(
    model: nn.Module,
    diffusion: CondMDIDiffusion,
    loader: DataLoader,
    device: torch.device,
    max_batches: int,
    split: str,
    joint_loss_mode: str = "element_mean",
    joint_human_branch_weight: float = 1.0,
    joint_camera_branch_weight: float = 1.0,
    joint_loss_weight: float = 1.0,
    task_routing: str = "symmetric",
    joint_human_camera_input_mode: str = "normal",
    joint_coupling_scale: float = 1.0,
    joint_coupling_mode: str = "symmetric",
    geo_tokenizer: nn.Module | None = None,
    geo_loss_weight: float = 0.0,
    geo_downsample: int = 4,
    geo_velocity_weight: float = 0.25,
    znorm_stats: dict[str, Any] | None = None,
) -> dict[str, float]:
    was_training = model.training
    model.eval()
    totals: dict[str, list[float]] = {}
    for batch_index, batch in enumerate(loader):
        if batch_index >= max_batches:
            break
        z = batch["z"].to(device)
        text = batch["text"].to(device)
        valid = batch["valid"].to(device)
        for task_id, task_name in TASK_NAMES.items():
            task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=device)
            noise = torch.randn_like(z)
            t = diffusion.sample_t(z.shape[0], device)
            _, metrics, _ = diffusion_loss(
                model,
                diffusion,
                z,
                text,
                valid,
                task,
                noise=noise,
                t=t,
                joint_loss_mode=joint_loss_mode,
                joint_human_branch_weight=joint_human_branch_weight,
                joint_camera_branch_weight=joint_camera_branch_weight,
                joint_loss_weight=joint_loss_weight,
                task_routing=task_routing,
                joint_human_camera_input_mode=joint_human_camera_input_mode,
                joint_coupling_scale=joint_coupling_scale,
                joint_coupling_mode=joint_coupling_mode,
                geo_tokenizer=geo_tokenizer,
                geo_loss_weight=geo_loss_weight,
                geo_downsample=geo_downsample,
                geo_velocity_weight=geo_velocity_weight,
                znorm_stats=znorm_stats,
            )
            for key, value in metrics.items():
                totals.setdefault(f"{task_name}_{key}", []).append(value)
                totals.setdefault(key, []).append(value)
            if task_id in {TASK_CAMERA, TASK_HUMAN} and z.shape[0] > 1:
                obs_mask, loss_mask = make_branch_masks(z, valid, task, task_routing=task_routing)
                x_t = diffusion.q_sample(z, t, noise)
                model_t = diffusion.model_t(t)
                target = diffusion.training_target(z, noise, t)
                clean_source_meta = build_source_meta(obs_mask, SOURCE_GT)
                base = model(x_t, model_t, text, obs_x0=z, obs_mask=obs_mask, task=task, source_meta=clean_source_meta)
                perm = torch.randperm(z.shape[0], device=device)
                z_shuf = z.clone()
                if task_id == TASK_CAMERA:
                    z_shuf[:, :HUM_DIM] = z[perm, :HUM_DIM]
                else:
                    z_shuf[:, HUM_DIM:] = z[perm, HUM_DIM:]
                shuf = model(x_t, model_t, text, obs_x0=z_shuf, obs_mask=obs_mask, task=task, source_meta=clean_source_meta)
                base_loss, _ = masked_target_mse(
                    base,
                    target,
                    loss_mask,
                    task,
                    joint_loss_mode=joint_loss_mode,
                    joint_human_branch_weight=joint_human_branch_weight,
                    joint_camera_branch_weight=joint_camera_branch_weight,
                    joint_loss_weight=joint_loss_weight,
                )
                shuf_loss, _ = masked_target_mse(
                    shuf,
                    target,
                    loss_mask,
                    task,
                    joint_loss_mode=joint_loss_mode,
                    joint_human_branch_weight=joint_human_branch_weight,
                    joint_camera_branch_weight=joint_camera_branch_weight,
                    joint_loss_weight=joint_loss_weight,
                )
                totals.setdefault(f"{task_name}_obs_shuffle_delta", []).append(float((shuf_loss - base_loss).detach().cpu()))
    out = {key: float(np.mean(values)) for key, values in totals.items() if values}
    out["split_marker"] = {"eval": 0.0, "test": 1.0}.get(split, -1.0)
    if was_training:
        model.train()
    else:
        model.eval()
    return out


def write_record(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps(record, sort_keys=True), flush=True)


def write_scalars(writer: SummaryWriter, prefix: str, metrics: dict[str, Any], step: int) -> None:
    for key, value in metrics.items():
        if isinstance(value, (int, float)) and math.isfinite(float(value)):
            writer.add_scalar(f"{prefix}/{key}", float(value), step)


def best_eval_from_log(path: Path, metric_name: str = "loss") -> float:
    best = float("inf")
    if not path.exists():
        return best
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if record.get("split") != "eval":
                continue
            value = record.get(metric_name)
            if isinstance(value, (int, float)) and math.isfinite(float(value)):
                best = min(best, float(value))
    return best


def resolve_selection_metric(metric_name: str, task_probs: list[float]) -> str:
    if metric_name != "auto":
        return metric_name
    active = [index for index, value in enumerate(task_probs) if float(value) > 0.0]
    if len(active) != 1:
        return "loss"
    return f"{TASK_NAMES[active[0]]}_loss"


@torch.no_grad()
def update_ema_model(ema_model: nn.Module, model: nn.Module, decay: float) -> None:
    for ema_param, param in zip(ema_model.parameters(), model.parameters()):
        ema_param.data.mul_(decay).add_(param.data, alpha=1.0 - decay)
    for ema_buffer, buffer in zip(ema_model.buffers(), model.buffers()):
        ema_buffer.copy_(buffer)


def scheduled_lr(args: argparse.Namespace, step: int) -> float:
    lr = args.lr
    if args.lr_warmup_steps > 0:
        lr *= min(float(step) / float(args.lr_warmup_steps), 1.0)
    if args.lr_milestone > 0 and step >= args.lr_milestone:
        lr *= args.lr_gamma
    return lr


def set_optimizer_lr(opt: torch.optim.Optimizer, lr: float) -> None:
    for group in opt.param_groups:
        group["lr"] = lr


def checkpoint_state(
    model: nn.Module,
    opt: torch.optim.Optimizer,
    step: int,
    meta: dict[str, Any],
    ema_model: nn.Module | None = None,
) -> dict[str, Any]:
    eval_model = ema_model if ema_model is not None else model
    state = {
        "model": eval_model.state_dict(),
        "raw_model": model.state_dict(),
        "opt": opt.state_dict(),
        "step": step,
        "meta": meta,
    }
    if ema_model is not None:
        state["ema_model"] = ema_model.state_dict()
    return state


def canonicalize_official_pulp_cache_meta(meta: dict[str, Any]) -> dict[str, Any]:
    checkpoint = meta.get("pulp_checkpoint")
    if not checkpoint:
        raise ValueError("official Pulp AE control cache is missing pulp_checkpoint")
    if meta.get("feature_contract") != "pulpmotion_official_normalized_human199_joint_camera14":
        raise ValueError("official Pulp AE control cache has the wrong feature contract")
    if meta.get("latent_order") != "concat([z_hum,z_cam])":
        raise ValueError("official Pulp AE control cache has the wrong Stage2 latent order")
    canonical = dict(meta)
    canonical.update(
        {
            "tokenizer_checkpoint": str(checkpoint),
            "tokenizer_preset": "pulp_official_aemmardm",
            "tokenizer_is_causal": False,
            "human_feature_dim": 199,
            "camera_feature_dim": 14,
            "human_latent_dim": HUM_DIM,
            "camera_latent_dim": CAM_DIM,
            "representation_control": "frozen_pulp_official_ae",
        }
    )
    return canonical


def assert_cache_contract(
    dataset: PulpLatentCache,
    *,
    require_default: bool,
    official_pulp_ae_control: bool,
) -> None:
    if official_pulp_ae_control:
        dataset.meta = canonicalize_official_pulp_cache_meta(dataset.meta)
        assert_non_causal_cache_meta(dataset.meta)
        return
    assert_non_causal_cache_meta(dataset.meta)
    if require_default:
        assert_default_cache_meta(dataset.meta)


def build_loaders(
    args: argparse.Namespace,
    znorm_stats: dict[str, Any] | None = None,
) -> tuple[DataLoader, DataLoader, DataLoader, dict[str, int], dict[str, Any]]:
    train_ds = PulpLatentCache(args.cache_dir / "train.pt", znorm_stats=znorm_stats)
    heldout_ds = PulpLatentCache(args.cache_dir / "val.pt", znorm_stats=znorm_stats)
    assert_cache_contract(
        train_ds,
        require_default=args.require_default_tokenizer_contract,
        official_pulp_ae_control=args.official_pulp_ae_control,
    )
    assert_cache_contract(
        heldout_ds,
        require_default=args.require_default_tokenizer_contract,
        official_pulp_ae_control=args.official_pulp_ae_control,
    )
    if train_ds.meta.get("tokenizer_checkpoint") != heldout_ds.meta.get("tokenizer_checkpoint"):
        raise RuntimeError("train/val caches were built from different tokenizer checkpoints")
    train_sample_ids = [str(value) for value in train_ds.sample_id]
    heldout_sample_ids = [str(value) for value in heldout_ds.sample_id]
    if len(set(train_sample_ids)) != len(train_sample_ids):
        raise RuntimeError("train cache contains duplicate sample IDs")
    if len(set(heldout_sample_ids)) != len(heldout_sample_ids):
        raise RuntimeError("heldout cache contains duplicate sample IDs")
    overlap = set(train_sample_ids).intersection(heldout_sample_ids)
    if overlap:
        raise RuntimeError(f"train/heldout cache sample IDs overlap: {sorted(overlap)[:8]}")
    eval_count = min(args.eval_samples, len(heldout_ds))
    test_count = min(args.test_samples, max(0, len(heldout_ds) - eval_count))
    if eval_count <= 0 or test_count <= 0:
        raise RuntimeError(f"heldout cache must provide eval and test subsets, got {len(heldout_ds)} samples")
    eval_ds = Subset(heldout_ds, range(eval_count))
    test_ds = Subset(heldout_ds, range(eval_count, eval_count + test_count))
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers, drop_last=True)
    eval_loader = DataLoader(eval_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
    sizes = {"train_samples": len(train_ds), "eval_samples": len(eval_ds), "test_samples": len(test_ds)}
    cache_audit = {
        "train_path": str(args.cache_dir / "train.pt"),
        "heldout_path": str(args.cache_dir / "val.pt"),
        "train_sample_ids_sha256": sha256_sample_ids(train_sample_ids),
        "heldout_sample_ids_sha256": sha256_sample_ids(heldout_sample_ids),
        "eval_sample_ids_sha256": sha256_sample_ids(heldout_sample_ids[:eval_count]),
        "test_sample_ids_sha256": sha256_sample_ids(heldout_sample_ids[eval_count : eval_count + test_count]),
        "tokenizer_checkpoint": train_ds.meta.get("tokenizer_checkpoint"),
        "tokenizer_is_causal": train_ds.meta.get("tokenizer_is_causal"),
        "tokenizer_preset": train_ds.meta.get("tokenizer_preset"),
        "feature_contract": train_ds.meta.get("feature_contract"),
        "latent_order": train_ds.meta.get("latent_order"),
        "representation_control": train_ds.meta.get("representation_control"),
        "pulp_checkpoint": train_ds.meta.get("pulp_checkpoint"),
    }
    return train_loader, eval_loader, test_loader, sizes, cache_audit


def train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    znorm_stats, znorm_stats_path = resolve_latent_znorm_stats(args)
    train_loader, eval_loader, test_loader, sizes, cache_audit = build_loaders(args, znorm_stats)
    dim_mults = tuple(int(v) for v in args.dim_mults)
    task_instruction_embeddings, task_instruction_meta = load_task_instruction_embeddings(args.task_instruction_embeddings)
    num_task_embeddings = max(3, len(args.task_probs))
    model = TemporalObsUNet(
        args.width,
        dim_mults,
        args.cond_mask_prob,
        args.zero_final,
        args.cond_mask_prob_cam,
        args.cond_mask_prob_hum,
        v72_text_role_router=args.v72_text_role_router,
        v72_aux_text_scale=args.v72_aux_text_scale,
        v72_soft_source=args.v72_soft_source,
        v72_trust_gate=args.v72_trust_gate,
        v72_relation_surrogate=args.v72_relation_surrogate,
        v72_gate_bias=args.v72_gate_bias,
        task_instruction_embeddings=task_instruction_embeddings,
        task_instruction_scale=args.task_instruction_scale,
        num_task_embeddings=num_task_embeddings,
    ).to(device)
    diffusion = build_stage2_process(
        args.generative_process,
        args.diffusion_steps,
        args.noise_schedule,
        device,
        args.diffusion_prediction_type,
    )
    geo_tokenizer = build_geo_tokenizer(args, device)
    geo_downsample = int(args.geo_downsample)
    ema_model = copy.deepcopy(model).eval().requires_grad_(False) if args.ema_decay > 0 else None
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, args.adam_beta2))
    task_probs = torch.tensor(args.task_probs, dtype=torch.float32)
    task_probs = task_probs / task_probs.sum()
    selection_metric = resolve_selection_metric(args.selection_metric, args.task_probs)

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "train_log.jsonl"
    meta = {
        "args": to_jsonable(args),
        "stage2_process": diffusion.metadata(),
        "diffusion_beta_schedule_source": "modular_openai_guided_diffusion_compatible" if args.generative_process == "diffusion" else None,
        "pipeline": "CondMDI-style obs_x0/obs_mask input replacement + process-specific target loss",
        "model_mean_type": diffusion.prediction_type,
        "latent_order": "concat([z_hum,z_cam])",
        "human_slice": [0, HUM_DIM],
        "camera_slice": [HUM_DIM, LATENT_DIM],
        "loss": "per-sample MSE over target branch and valid latent frames only; observed branch excluded",
        "geo_loss": {
            "enabled": bool(geo_tokenizer is not None and args.geo_loss_weight > 0.0),
            "weight": float(args.geo_loss_weight),
            "definition": "decoded feature-space MSE through the frozen owning Stage1 decoder; target branch and valid frames only",
            "tokenizer_checkpoint": str(args.geo_tokenizer_checkpoint) if args.geo_tokenizer_checkpoint else None,
            "tokenizer_preset": args.geo_tokenizer_preset,
            "downsample": geo_downsample,
            "velocity_weight": float(args.geo_velocity_weight),
        },
        "joint_loss_mode": args.joint_loss_mode,
        "joint_human_branch_weight": args.joint_human_branch_weight,
        "joint_camera_branch_weight": args.joint_camera_branch_weight,
        "joint_loss_weight": args.joint_loss_weight,
        "task_routing": args.task_routing,
        "joint_human_camera_input_mode": args.joint_human_camera_input_mode,
        "joint_coupling_scale": args.joint_coupling_scale,
        "joint_coupling_mode": args.joint_coupling_mode,
        "task_names": TASK_NAMES,
        "task_probs_normalized": [float(v) for v in task_probs.tolist()],
        "cache_audit": cache_audit,
        "task_exposure_budget": {
            "unit": "sample_task_assignment",
            "total_planned": int(args.steps * args.batch_size),
            "expected_by_task": {
                TASK_NAMES[index]: float(args.steps * args.batch_size * probability)
                for index, probability in enumerate(task_probs.tolist())
            },
        },
        "task_exposure_counts": {TASK_NAMES[index]: 0 for index in range(len(task_probs))},
        "task_exposure_total": 0,
        "num_task_embeddings": num_task_embeddings,
        "obs_self_condition": {
            "mode": args.obs_self_condition_mode,
            "prob": args.obs_self_condition_prob,
            "noise_std": args.obs_self_condition_noise_std,
        },
        "temporal_mask": {
            "enabled": bool(args.temporal_mask_probability > 0.0),
            "probability": args.temporal_mask_probability,
            "task_weights": list(args.temporal_mask_task_weights),
            "patterns": list(TEMPORAL_PATTERN_NAMES),
            "missing_ratio": list(TEMPORAL_MISSING_RATIO),
            "semantics": "whole-branch E0 replay plus temporal H/C/joint completion; fixed batch denominator",
        },
        "temporal_mask_exposure_counts": {
            **{f"task_{name}": 0 for name in ("camera", "human", "joint")},
            **{f"pattern_{name}": 0 for name in TEMPORAL_PATTERN_NAMES},
        },
        "latent_znorm": latent_znorm_meta(
            bool(args.znorm), znorm_stats, znorm_stats_path, args.cache_dir / "train.pt"
        ),
        "task_instruction": {
            **task_instruction_meta,
            "scale": args.task_instruction_scale,
            "source": "precomputed CLIP text embedding; projected into denoiser condition",
            "motionlab_reference": "Task Instruction Modulation uses CLIP text embeddings rather than one-hot task ids.",
        },
        "v72_config": {
            "text_role_router": args.v72_text_role_router,
            "aux_text_scale": args.v72_aux_text_scale,
            "soft_source": args.v72_soft_source,
            "trust_gate": args.v72_trust_gate,
            "relation_surrogate": args.v72_relation_surrogate,
            "gate_bias": args.v72_gate_bias,
        },
        "selection_metric": selection_metric,
        "selection_metric_requested": args.selection_metric,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "params": sum(p.numel() for p in model.parameters()),
        **sizes,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")

    step = 0
    task_exposure_counts = torch.zeros(len(task_probs), dtype=torch.long, device=device)
    temporal_exposure_counts = dict(meta["temporal_mask_exposure_counts"])

    def sync_task_exposure_meta() -> dict[str, int]:
        counts = task_exposure_counts.detach().cpu().tolist()
        by_task = {TASK_NAMES[index]: int(value) for index, value in enumerate(counts)}
        meta["task_exposure_counts"] = by_task
        meta["task_exposure_total"] = int(sum(counts))
        meta["temporal_mask_exposure_counts"] = dict(temporal_exposure_counts)
        return {
            **{f"task_exposures_{name}": count for name, count in by_task.items()},
            **{f"temporal_exposures_{name}": count for name, count in temporal_exposure_counts.items()},
        }

    best_eval = best_eval_from_log(log_path, selection_metric)
    if args.resume:
        checkpoint = torch.load(args.resume, map_location=device)
        resume_strict = not bool(args.v72_relation_surrogate)
        load_info = model.load_state_dict(checkpoint.get("raw_model", checkpoint["model"]), strict=resume_strict)
        optimizer_loaded = True
        try:
            opt.load_state_dict(checkpoint["opt"])
        except ValueError as exc:
            optimizer_loaded = False
            optimizer_load_error = str(exc)
        else:
            optimizer_load_error = ""
        step = int(checkpoint.get("step", 0))
        resumed_counts = checkpoint.get("meta", {}).get("task_exposure_counts", {})
        for index in range(len(task_probs)):
            task_exposure_counts[index] = int(resumed_counts.get(TASK_NAMES[index], 0))
        resumed_temporal_counts = checkpoint.get("meta", {}).get("temporal_mask_exposure_counts", {})
        for name in temporal_exposure_counts:
            temporal_exposure_counts[name] = int(resumed_temporal_counts.get(name, 0))
        sync_task_exposure_meta()
        if ema_model is not None:
            ema_state = checkpoint.get("ema_model", checkpoint.get("model"))
            ema_model.load_state_dict(ema_state, strict=resume_strict)
        write_record(
            log_path,
            {
                "step": step,
                "split": "resume",
                "resume_path": str(args.resume),
                "target_steps": args.steps,
                "best_eval_loss": best_eval,
                "resume_strict": resume_strict,
                "resume_missing_keys": list(load_info.missing_keys),
                "resume_unexpected_keys": list(load_info.unexpected_keys),
                "optimizer_loaded": optimizer_loaded,
                "optimizer_load_error": optimizer_load_error,
            },
        )
    purge_step = args.purge_step
    if purge_step is None and args.resume:
        purge_step = step + 1
    writer = SummaryWriter(str(out / "tensorboard"), purge_step=purge_step)
    model.train()
    bad_eval_count = 0
    while step < args.steps:
        for batch in train_loader:
            step += 1
            set_optimizer_lr(opt, scheduled_lr(args, step))
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            task = sample_tasks(z.shape[0], task_probs, device)
            task_exposure_counts += torch.bincount(task, minlength=len(task_probs))
            loss, metrics, _ = diffusion_loss(
                model,
                diffusion,
                z,
                text,
                valid,
                task,
                joint_loss_mode=args.joint_loss_mode,
                joint_human_branch_weight=args.joint_human_branch_weight,
                joint_camera_branch_weight=args.joint_camera_branch_weight,
                joint_loss_weight=args.joint_loss_weight,
                task_routing=args.task_routing,
                obs_self_condition_prob=args.obs_self_condition_prob,
                obs_self_condition_mode=args.obs_self_condition_mode,
                obs_self_condition_noise_std=args.obs_self_condition_noise_std,
                temporal_mask_probability=args.temporal_mask_probability,
                temporal_mask_task_weights=args.temporal_mask_task_weights,
                joint_human_camera_input_mode=args.joint_human_camera_input_mode,
                joint_coupling_scale=args.joint_coupling_scale,
                joint_coupling_mode=args.joint_coupling_mode,
                geo_tokenizer=geo_tokenizer,
                geo_loss_weight=args.geo_loss_weight,
                geo_downsample=geo_downsample,
                geo_velocity_weight=args.geo_velocity_weight,
                znorm_stats=znorm_stats,
            )
            for key in tuple(metrics):
                if key.startswith("_temporal_count_"):
                    name = key.removeprefix("_temporal_count_")
                    temporal_exposure_counts[name] += int(metrics.pop(key))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad_norm = float(nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip).detach().cpu())
            opt.step()
            if ema_model is not None:
                update_ema_model(ema_model, model, args.ema_decay)

            if step == 1 or step % args.log_every == 0:
                exposure_fields = sync_task_exposure_meta()
                record = {
                    "step": step,
                    "split": "train",
                    **metrics,
                    **exposure_fields,
                    "task_exposures_total": meta["task_exposure_total"],
                    "lr": opt.param_groups[0]["lr"],
                    "grad_norm": grad_norm,
                }
                write_record(log_path, record)
                write_scalars(writer, "train", {**metrics, "lr": opt.param_groups[0]["lr"], "grad_norm": grad_norm}, step)

            if step == 1 or step % args.eval_every == 0:
                eval_model = ema_model if ema_model is not None else model
                metrics_eval = evaluate(
                    eval_model,
                    diffusion,
                    eval_loader,
                    device,
                    args.eval_batches,
                    split="eval",
                    joint_loss_mode=args.joint_loss_mode,
                    joint_human_branch_weight=args.joint_human_branch_weight,
                    joint_camera_branch_weight=args.joint_camera_branch_weight,
                    joint_loss_weight=args.joint_loss_weight,
                    task_routing=args.task_routing,
                    joint_human_camera_input_mode=args.joint_human_camera_input_mode,
                    joint_coupling_scale=args.joint_coupling_scale,
                    joint_coupling_mode=args.joint_coupling_mode,
                    geo_tokenizer=geo_tokenizer,
                    geo_loss_weight=args.geo_loss_weight,
                    geo_downsample=geo_downsample,
                    geo_velocity_weight=args.geo_velocity_weight,
                    znorm_stats=znorm_stats,
                )
                record = {"step": step, "split": "eval", **metrics_eval}
                write_record(log_path, record)
                write_scalars(writer, "eval", metrics_eval, step)
                if selection_metric not in metrics_eval:
                    available = ", ".join(sorted(metrics_eval))
                    raise RuntimeError(f"selection metric {selection_metric!r} not found in eval metrics; available: {available}")
                eval_loss = float(metrics_eval[selection_metric])
                sync_task_exposure_meta()
                state = checkpoint_state(model, opt, step, meta, ema_model)
                torch.save(state, out / "last.pt")
                if eval_loss + args.early_stop_min_delta < best_eval:
                    best_eval = eval_loss
                    bad_eval_count = 0
                    torch.save(state, out / "best_eval.pt")
                else:
                    bad_eval_count += 1

            if step == 1 or step % args.test_every == 0:
                eval_model = ema_model if ema_model is not None else model
                metrics_test = evaluate(
                    eval_model,
                    diffusion,
                    test_loader,
                    device,
                    args.test_batches,
                    split="test",
                    joint_loss_mode=args.joint_loss_mode,
                    joint_human_branch_weight=args.joint_human_branch_weight,
                    joint_camera_branch_weight=args.joint_camera_branch_weight,
                    joint_loss_weight=args.joint_loss_weight,
                    task_routing=args.task_routing,
                    joint_human_camera_input_mode=args.joint_human_camera_input_mode,
                    joint_coupling_scale=args.joint_coupling_scale,
                    joint_coupling_mode=args.joint_coupling_mode,
                    geo_tokenizer=geo_tokenizer,
                    geo_loss_weight=args.geo_loss_weight,
                    geo_downsample=geo_downsample,
                    geo_velocity_weight=args.geo_velocity_weight,
                    znorm_stats=znorm_stats,
                )
                record = {"step": step, "split": "test", **metrics_test}
                write_record(log_path, record)
                write_scalars(writer, "test", metrics_test, step)
                sync_task_exposure_meta()
                torch.save(checkpoint_state(model, opt, step, meta, ema_model), out / "last.pt")

            if step in args.snapshot_steps:
                sync_task_exposure_meta()
                torch.save(checkpoint_state(model, opt, step, meta, ema_model), out / f"step_{step}.pt")

            if args.early_stop_patience > 0 and bad_eval_count >= args.early_stop_patience:
                write_record(
                    log_path,
                    {
                        "step": step,
                        "split": "early_stop",
                        "best_eval_loss": best_eval,
                        "bad_eval_count": bad_eval_count,
                        "patience": args.early_stop_patience,
                    },
                )
                writer.flush()
                writer.close()
                sync_task_exposure_meta()
                (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
                return

            writer.flush()
            if step >= args.steps:
                break
    sync_task_exposure_meta()
    torch.save(checkpoint_state(model, opt, step, meta, ema_model), out / "last.pt")
    (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    writer.close()


def check(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    znorm_stats, znorm_stats_path = resolve_latent_znorm_stats(args)
    geo_tokenizer = build_geo_tokenizer(args, device)
    geo_downsample = int(args.geo_downsample)
    ds = PulpLatentCache(args.cache_dir / "train.pt", znorm_stats=znorm_stats)
    assert_cache_contract(
        ds,
        require_default=args.require_default_tokenizer_contract,
        official_pulp_ae_control=args.official_pulp_ae_control,
    )
    batch = next(iter(DataLoader(ds, batch_size=min(args.batch_size, 8), shuffle=False, num_workers=0)))
    z = batch["z"].to(device)
    text = batch["text"].to(device)
    valid = batch["valid"].to(device)
    task = torch.tensor(
        [TASK_CAMERA, TASK_HUMAN, TASK_JOINT, TASK_HUMAN_TEXT, TASK_CAMERA, TASK_HUMAN, TASK_JOINT, TASK_HUMAN_TEXT],
        device=device,
    )[: z.shape[0]]
    obs_mask, loss_mask = make_branch_masks(z, valid, task, task_routing=args.task_routing)
    assert not torch.any(obs_mask & loss_mask)
    assert torch.all(obs_mask[:, HUM_DIM:] == 0) or True
    assert loss_mask.flatten(1).any(dim=1).all()
    pred = z.clone()
    pred[:, :HUM_DIM] += 1000.0
    camera_only = torch.full((z.shape[0],), TASK_CAMERA, dtype=torch.long, device=device)
    _, camera_loss_mask = make_branch_masks(z, valid, camera_only, task_routing=args.task_routing)
    base_loss, _ = masked_target_mse(z, z, camera_loss_mask, camera_only)
    perturbed_loss, _ = masked_target_mse(pred, z, camera_loss_mask, camera_only)
    if not torch.allclose(base_loss, perturbed_loss):
        raise RuntimeError("camera task loss changed when only observed human branch was perturbed")
    pred_camera = z.clone()
    pred_camera[:, HUM_DIM:] += 1.0
    target_loss, _ = masked_target_mse(pred_camera, z, camera_loss_mask, camera_only)
    if not target_loss > base_loss:
        raise RuntimeError("camera task loss did not increase when target camera branch was perturbed")
    joint_only = torch.full((z.shape[0],), TASK_JOINT, dtype=torch.long, device=device)
    _, joint_loss_mask = make_branch_masks(z, valid, joint_only, task_routing=args.task_routing)
    joint_branch_mean, branch_metrics = masked_target_mse(
        pred_camera,
        z,
        joint_loss_mask,
        joint_only,
        joint_loss_mode="branch_mean",
        joint_human_branch_weight=args.joint_human_branch_weight,
        joint_camera_branch_weight=args.joint_camera_branch_weight,
        joint_loss_weight=args.joint_loss_weight,
    )
    if not torch.isfinite(joint_branch_mean) or "loss_joint_element_mean" not in branch_metrics:
        raise RuntimeError("branch-normalized joint loss check failed")
    pred_human_obs = z.clone()
    pred_human_obs[:, HUM_DIM:] += 1000.0
    human_only = torch.full((z.shape[0],), TASK_HUMAN, dtype=torch.long, device=device)
    human_obs, human_loss_mask = make_branch_masks(z, valid, human_only, task_routing=args.task_routing)
    if args.task_routing == "human_first" and human_obs.any():
        raise RuntimeError("human-first task must not observe camera or human latent branches")
    human_base, _ = masked_target_mse(z, z, human_loss_mask, human_only)
    human_obs_perturbed, _ = masked_target_mse(pred_human_obs, z, human_loss_mask, human_only)
    if not torch.allclose(human_base, human_obs_perturbed):
        raise RuntimeError("human task loss changed when only observed camera branch was perturbed")
    human_text_only = torch.full((z.shape[0],), TASK_HUMAN_TEXT, dtype=torch.long, device=device)
    obs_human_text, human_text_loss_mask = make_branch_masks(
        z, valid, human_text_only, task_routing=args.task_routing
    )
    if obs_human_text.any():
        raise RuntimeError("human_text task must not observe camera or human latent branches")
    if human_text_loss_mask[:, HUM_DIM:].any():
        raise RuntimeError("human_text task must not train camera latent channels")
    if not human_text_loss_mask[:, :HUM_DIM].flatten(1).any(dim=1).all():
        raise RuntimeError("human_text task must train human latent channels")
    task_instruction_embeddings, _ = load_task_instruction_embeddings(args.task_instruction_embeddings)
    num_task_embeddings = max(3, len(args.task_probs))
    model = TemporalObsUNet(
        args.width,
        tuple(int(v) for v in args.dim_mults),
        args.cond_mask_prob,
        args.zero_final,
        args.cond_mask_prob_cam,
        args.cond_mask_prob_hum,
        v72_text_role_router=args.v72_text_role_router,
        v72_aux_text_scale=args.v72_aux_text_scale,
        v72_soft_source=args.v72_soft_source,
        v72_trust_gate=args.v72_trust_gate,
        v72_relation_surrogate=args.v72_relation_surrogate,
        v72_gate_bias=args.v72_gate_bias,
        task_instruction_embeddings=task_instruction_embeddings,
        task_instruction_scale=args.task_instruction_scale,
        num_task_embeddings=num_task_embeddings,
    ).to(device)
    model.eval()
    joint_obs_mask, _ = make_branch_masks(z, valid, joint_only, task_routing=args.task_routing)
    joint_source_meta = build_source_meta(joint_obs_mask, SOURCE_GT)
    check_t = torch.zeros((z.shape[0],), dtype=torch.long, device=device)
    legacy_pred = model(
        z,
        check_t,
        text,
        obs_x0=z,
        obs_mask=joint_obs_mask,
        task=joint_only,
        source_meta=joint_source_meta,
    )
    scale_one_pred = predict_with_joint_coupling(
        model, z, check_t, text, z, joint_obs_mask, joint_only, joint_source_meta, 1.0
    )
    if not torch.equal(legacy_pred, scale_one_pred):
        raise RuntimeError("joint coupling scale=1 changed the legacy forward")
    isolated_pred = predict_with_joint_coupling(
        model, z, check_t, text, z, joint_obs_mask, joint_only, joint_source_meta, 0.0
    )
    camera_perturbed = z.clone()
    camera_perturbed[:, HUM_DIM:, :] += 1000.0
    camera_perturbed_pred = predict_with_joint_coupling(
        model,
        camera_perturbed,
        check_t,
        text,
        z,
        joint_obs_mask,
        joint_only,
        joint_source_meta,
        0.0,
    )
    if not torch.equal(isolated_pred[:, :HUM_DIM, :], camera_perturbed_pred[:, :HUM_DIM, :]):
        raise RuntimeError("isolated human prediction changed under camera latent perturbation")
    human_perturbed = z.clone()
    human_perturbed[:, :HUM_DIM, :] += 1000.0
    human_perturbed_pred = predict_with_joint_coupling(
        model,
        human_perturbed,
        check_t,
        text,
        z,
        joint_obs_mask,
        joint_only,
        joint_source_meta,
        0.0,
    )
    if not torch.equal(isolated_pred[:, HUM_DIM:, :], human_perturbed_pred[:, HUM_DIM:, :]):
        raise RuntimeError("isolated camera prediction changed under human latent perturbation")
    directed_pred = predict_with_joint_coupling(
        model,
        z,
        check_t,
        text,
        z,
        joint_obs_mask,
        joint_only,
        joint_source_meta,
        0.0,
        "c_to_h_blocked",
    )
    directed_camera_perturbed = predict_with_joint_coupling(
        model,
        camera_perturbed,
        check_t,
        text,
        z,
        joint_obs_mask,
        joint_only,
        joint_source_meta,
        0.0,
        "c_to_h_blocked",
    )
    if not torch.equal(directed_pred[:, :HUM_DIM, :], directed_camera_perturbed[:, :HUM_DIM, :]):
        raise RuntimeError("C->H-blocked human prediction changed under camera latent perturbation")
    camera_text_perturbed = text.clone()
    camera_text_perturbed[:, : text.shape[-1] // 2] += 1000.0
    directed_text_perturbed = predict_with_joint_coupling(
        model,
        z,
        check_t,
        camera_text_perturbed,
        z,
        joint_obs_mask,
        joint_only,
        joint_source_meta,
        0.0,
        "c_to_h_blocked",
    )
    if not torch.equal(directed_pred[:, :HUM_DIM, :], directed_text_perturbed[:, :HUM_DIM, :]):
        raise RuntimeError("C->H-blocked human prediction changed under camera text perturbation")
    if not torch.equal(directed_pred[:, HUM_DIM:, :], legacy_pred[:, HUM_DIM:, :]):
        raise RuntimeError("C->H-blocked camera prediction changed from the full joint forward")
    model.train()
    diffusion = build_stage2_process(
        args.generative_process,
        args.diffusion_steps,
        args.noise_schedule,
        device,
        args.diffusion_prediction_type,
    )
    loss, metrics, pred_x0 = diffusion_loss(
        model,
        diffusion,
        z,
        text,
        valid,
        task,
        joint_loss_mode=args.joint_loss_mode,
        joint_human_branch_weight=args.joint_human_branch_weight,
        joint_camera_branch_weight=args.joint_camera_branch_weight,
        joint_loss_weight=args.joint_loss_weight,
        task_routing=args.task_routing,
        obs_self_condition_prob=args.obs_self_condition_prob,
        obs_self_condition_mode=args.obs_self_condition_mode,
        obs_self_condition_noise_std=args.obs_self_condition_noise_std,
        temporal_mask_probability=args.temporal_mask_probability,
        temporal_mask_task_weights=args.temporal_mask_task_weights,
        joint_human_camera_input_mode=args.joint_human_camera_input_mode,
        joint_coupling_scale=args.joint_coupling_scale,
        joint_coupling_mode=args.joint_coupling_mode,
        geo_tokenizer=geo_tokenizer,
        geo_loss_weight=args.geo_loss_weight,
        geo_downsample=geo_downsample,
        geo_velocity_weight=args.geo_velocity_weight,
        znorm_stats=znorm_stats,
    )
    if pred_x0.shape != z.shape:
        raise RuntimeError(f"forward shape mismatch: {pred_x0.shape} vs {z.shape}")
    if not torch.isfinite(loss):
        raise RuntimeError("non-finite check loss")
    roundtrip = denormalize_latent(normalize_latent(
        denormalize_latent(z, valid, znorm_stats), valid, znorm_stats
    ), valid, znorm_stats)
    raw = denormalize_latent(z, valid, znorm_stats)
    valid_bc = valid[:, None, :].expand_as(raw)
    roundtrip_max_error = float((roundtrip - raw)[valid_bc].abs().max().detach().cpu())
    print(json.dumps({
        "ok": True,
        "loss": float(loss.detach().cpu()),
        "metrics": metrics,
        "shape": list(pred_x0.shape),
        "latent_znorm": latent_znorm_meta(bool(args.znorm), znorm_stats, znorm_stats_path, args.cache_dir / "train.pt"),
        "roundtrip_max_error": roundtrip_max_error,
    }, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["check", "train"])
    p.add_argument("--cache-dir", type=Path, default=ROOT / "runs/train/stage2/no_proj_pilot_20260610/cache_2048_gpu1")
    p.add_argument("--output-dir", type=Path, default=ROOT / "runs/train/stage2/condmdi_pulp_no_proj_20260611/gpu1_main")
    p.add_argument("--runs-root", type=Path, default=ROOT / "runs")
    p.add_argument("--run-id", help="Canonical Stage2 run id; derives the train output path under runs/train/stage2/<run-id>.")
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--steps", type=int, default=50000)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--num-workers", type=int, default=2)
    p.add_argument("--width", type=int, default=384)
    p.add_argument("--dim-mults", type=int, nargs="+", default=[1, 2, 2])
    p.add_argument("--cond-mask-prob", type=float, default=0.1, help="Joint cond mask prob (zeroes both camera and human text together)")
    p.add_argument("--cond-mask-prob-cam", type=float, default=0.0, help="Camera-only cond mask prob (zeroes only camera text half)")
    p.add_argument("--cond-mask-prob-hum", type=float, default=0.0, help="Human-only cond mask prob (zeroes only human text half)")
    p.add_argument("--zero-final", action="store_true", default=True)
    p.add_argument("--no-zero-final", action="store_false", dest="zero_final")
    p.add_argument("--generative-process", choices=["diffusion", "rectified_flow"], default="diffusion")
    p.add_argument("--diffusion-steps", type=int, default=1000)
    p.add_argument(
        "--diffusion-prediction-type",
        choices=["START_X", "EPSILON", "V_PREDICTION"],
        default="START_X",
        help="Diffusion training target; ignored by rectified_flow.",
    )
    p.add_argument("--noise-schedule", default="cosine")
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--lr-warmup-steps", type=int, default=0)
    p.add_argument("--lr-milestone", type=int, default=0)
    p.add_argument("--lr-gamma", type=float, default=0.1)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--adam-beta2", type=float, default=0.999)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--eval-every", type=int, default=500)
    p.add_argument("--eval-batches", type=int, default=8)
    p.add_argument("--eval-samples", type=int, default=128)
    p.add_argument("--test-every", type=int, default=2000)
    p.add_argument("--test-batches", type=int, default=8)
    p.add_argument("--test-samples", type=int, default=128)
    p.add_argument(
        "--task-probs",
        type=float,
        nargs="+",
        default=[1.0, 1.0, 1.0],
        help="Task sampling probabilities. Use 3 values for camera,human,joint or 4 values for camera,human,joint,human_text.",
    )
    p.add_argument("--joint-loss-mode", choices=["element_mean", "branch_mean", "branch_sum"], default="element_mean")
    p.add_argument("--joint-human-branch-weight", type=float, default=1.0)
    p.add_argument("--joint-camera-branch-weight", type=float, default=1.0)
    p.add_argument(
        "--joint-loss-weight",
        type=float,
        default=1.0,
        help="Multiplier applied to JOINT-task sample losses before the fixed batch mean; zero preserves exposure/denominator while removing joint gradients.",
    )
    p.add_argument(
        "--task-routing",
        choices=["symmetric", "human_first"],
        default="symmetric",
        help="human_first makes TASK_HUMAN text-only while TASK_CAMERA still observes human latent.",
    )
    p.add_argument("--geo-loss-weight", type=float, default=0.0, help="Frozen owning-decoder feature-space auxiliary loss weight")
    p.add_argument("--geo-tokenizer-checkpoint", type=Path)
    p.add_argument("--geo-tokenizer-preset", default="pulpmotion_joint_ae_official_199_14_pulp192")
    p.add_argument("--geo-downsample", type=int, default=4)
    p.add_argument("--geo-velocity-weight", type=float, default=0.25)
    p.add_argument("--znorm", action="store_true", help="Use per-channel train valid-frame latent z-normalization")
    p.add_argument("--znorm-stats-path", type=Path)
    p.add_argument("--znorm-eps", type=float, default=1.0e-6)
    p.add_argument("--znorm-recompute", action="store_true")
    p.add_argument("--full-cov", action="store_true", help="Whiten each human/camera branch with train-cache covariance")
    p.add_argument("--cov-ridge", type=float, default=1.0e-4)
    p.set_defaults(require_default_tokenizer_contract=True)
    p.add_argument(
        "--allow-nondefault-tokenizer-contract",
        action="store_false",
        dest="require_default_tokenizer_contract",
        help="Permit a representation control while still requiring a non-causal tokenizer.",
    )
    p.add_argument(
        "--official-pulp-ae-control",
        action="store_true",
        help="Use a frozen official Pulp AEMMARDM cache as an explicit non-causal representation control.",
    )
    p.add_argument(
        "--joint-human-camera-input-mode",
        choices=["normal", "zero", "shuffle", "noise_matched"],
        default="normal",
        help="For JOINT training, compute the human-branch loss from a second forward pass whose camera input channels are perturbed; camera loss keeps the normal forward pass.",
    )
    p.add_argument(
        "--joint-coupling-scale",
        type=float,
        default=1.0,
        help="JOINT-only latent/text interaction scale: 1 keeps the legacy coupled forward; 0 isolates human/camera views.",
    )
    p.add_argument(
        "--joint-coupling-mode",
        choices=["symmetric", "c_to_h_blocked"],
        default="symmetric",
        help="At scale<1, either attenuate both cross-branch directions or only camera-to-human while retaining human-to-camera.",
    )
    p.add_argument("--selection-metric", default="auto")
    p.add_argument(
        "--snapshot-steps",
        type=int,
        nargs="*",
        default=[],
        help="Training steps at which to save immutable step_<N>.pt checkpoints.",
    )
    p.add_argument("--obs-self-condition-prob", type=float, default=0.0)
    p.add_argument("--obs-self-condition-mode", choices=["clean", "noisy", "joint_pred", "mixed"], default="clean")
    p.add_argument("--obs-self-condition-noise-std", type=float, default=0.0)
    p.add_argument(
        "--temporal-mask-probability",
        type=float,
        default=0.0,
        help="Fraction of camera/human/joint task slots converted from whole-branch E0 to temporal completion.",
    )
    p.add_argument(
        "--temporal-mask-task-weights",
        type=float,
        nargs=3,
        default=[1.0, 1.0, 1.0],
        metavar=("CAMERA", "HUMAN", "JOINT"),
        help=(
            "Fixed-denominator loss weights for temporal camera/human/joint slots; "
            "zero disables temporal routing for that task and preserves whole-branch replay."
        ),
    )
    p.add_argument("--v72-text-role-router", action="store_true")
    p.add_argument("--v72-aux-text-scale", type=float, default=0.35)
    p.add_argument("--v72-soft-source", action="store_true")
    p.add_argument("--v72-trust-gate", action="store_true")
    p.add_argument("--v72-relation-surrogate", action="store_true")
    p.add_argument("--v72-gate-bias", type=float, default=2.0)
    p.add_argument(
        "--task-instruction-embeddings",
        type=Path,
        help="Path to precomputed CLIP task instruction embeddings [3,D] ordered as camera,human,joint.",
    )
    p.add_argument("--task-instruction-scale", type=float, default=1.0)
    p.add_argument("--ema-decay", type=float, default=0.0)
    p.add_argument("--early-stop-patience", type=int, default=0)
    p.add_argument("--early-stop-min-delta", type=float, default=0.0)
    p.add_argument("--resume", type=Path)
    p.add_argument("--purge-step", type=int)
    return p


def main() -> None:
    args = build_parser().parse_args()
    if args.run_id:
        paths = run_paths("stage2", args.run_id, args.runs_root)
        if args.mode == "train" and not paths["root"].exists():
            init_run(
                "stage2",
                args.run_id,
                runs_root=args.runs_root,
                description="StoryMotion Unified Stage2 training",
            )
        args.run_root = paths["root"]
        args.output_dir = paths["train"]
    else:
        args.run_root = None
    if not (0.0 <= args.obs_self_condition_prob <= 1.0):
        raise ValueError("--obs-self-condition-prob must be in [0, 1]")
    if args.obs_self_condition_noise_std < 0.0:
        raise ValueError("--obs-self-condition-noise-std must be non-negative")
    if not 0.0 <= args.temporal_mask_probability <= 1.0:
        raise ValueError("--temporal-mask-probability must be in [0, 1]")
    if any(value < 0.0 for value in args.temporal_mask_task_weights):
        raise ValueError("--temporal-mask-task-weights values must be non-negative")
    if args.joint_human_branch_weight <= 0.0 or args.joint_camera_branch_weight <= 0.0:
        raise ValueError("--joint-*-branch-weight values must be positive")
    if args.joint_loss_weight < 0.0:
        raise ValueError("--joint-loss-weight must be non-negative")
    if not 0.0 <= args.joint_coupling_scale <= 1.0:
        raise ValueError("--joint-coupling-scale must be in [0, 1]")
    if args.joint_coupling_scale != 1.0 and args.joint_human_camera_input_mode != "normal":
        raise ValueError("--joint-coupling-scale cannot be combined with --joint-human-camera-input-mode")
    if args.znorm_eps <= 0.0:
        raise ValueError("--znorm-eps must be positive")
    if args.cov_ridge <= 0.0:
        raise ValueError("--cov-ridge must be positive")
    if args.geo_loss_weight < 0.0:
        raise ValueError("--geo-loss-weight must be non-negative")
    if args.temporal_mask_probability > 0.0 and args.geo_loss_weight > 0.0:
        raise ValueError("temporal mask training does not support whole-branch --geo-loss-weight")
    if args.joint_loss_weight == 0.0 and args.geo_loss_weight > 0.0:
        raise ValueError("--joint-loss-weight 0 requires --geo-loss-weight 0 so JOINT samples have no gradient")
    if args.geo_downsample <= 0:
        raise ValueError("--geo-downsample must be positive")
    if args.geo_velocity_weight < 0.0:
        raise ValueError("--geo-velocity-weight must be non-negative")
    if any(step <= 0 for step in args.snapshot_steps):
        raise ValueError("--snapshot-steps values must be positive")
    if not (0.0 <= args.v72_aux_text_scale <= 1.0):
        raise ValueError("--v72-aux-text-scale must be in [0, 1]")
    if args.task_instruction_scale < 0.0:
        raise ValueError("--task-instruction-scale must be non-negative")
    if args.task_routing == "human_first":
        if not args.v72_text_role_router or args.v72_aux_text_scale != 0.0:
            raise ValueError("human_first requires --v72-text-role-router --v72-aux-text-scale 0")
        if args.joint_coupling_scale != 0.0 or args.joint_coupling_mode != "c_to_h_blocked":
            raise ValueError("human_first requires directed JOINT routing: --joint-coupling-scale 0 --joint-coupling-mode c_to_h_blocked")
    if args.task_instruction_embeddings is not None and not args.task_instruction_embeddings.exists():
        raise FileNotFoundError(args.task_instruction_embeddings)
    if len(args.task_probs) not in {3, 4}:
        raise ValueError("--task-probs must contain 3 values (camera,human,joint) or 4 values (camera,human,joint,human_text)")
    if sum(args.task_probs) <= 0.0:
        raise ValueError("--task-probs must have a positive sum")
    if args.generative_process == "rectified_flow" and args.obs_self_condition_mode in {"joint_pred", "mixed"}:
        raise ValueError("rectified_flow does not support generated observed self-conditioning in this trainer")
    if args.mode == "check":
        check(args)
    else:
        train(args)
        if args.run_id:
            update_manifest(
                "stage2",
                args.run_id,
                runs_root=args.runs_root,
                status="trained",
                artifacts={
                    "checkpoint": str((paths["train"] / "last.pt").relative_to(args.runs_root)),
                    "train_log": str((paths["train"] / "train_log.jsonl").relative_to(args.runs_root)),
                    "tensorboard": str((paths["train"] / "tensorboard").relative_to(args.runs_root)),
                },
            )


if __name__ == "__main__":
    main()
