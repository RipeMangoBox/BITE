#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import math
import random
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
TASK_NAMES = {TASK_CAMERA: "camera", TASK_HUMAN: "human", TASK_JOINT: "joint"}


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


class PulpLatentCache(Dataset):
    def __init__(self, path: Path) -> None:
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
        self.z = z
        self.text = text
        self.valid = valid
        self.sample_id = data.get("sample_id", [str(i) for i in range(z.shape[0])])

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
    """CondMDI-style temporal UNet: replace observed x_t with obs_x0, then append obs_mask."""

    def __init__(self, width: int, dim_mults: tuple[int, ...], cond_mask_prob: float, zero_final: bool,
                 cond_mask_prob_cam: float = 0.0, cond_mask_prob_hum: float = 0.0) -> None:
        super().__init__()
        self.cond_mask_prob = float(cond_mask_prob)
        self.cond_mask_prob_cam = float(cond_mask_prob_cam)
        self.cond_mask_prob_hum = float(cond_mask_prob_hum)
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
    ) -> torch.Tensor:
        if x_t.shape != obs_x0.shape or x_t.shape != obs_mask.shape:
            raise ValueError(f"x_t, obs_x0 and obs_mask must match, got {x_t.shape}, {obs_x0.shape}, {obs_mask.shape}")
        x = torch.where(obs_mask.bool(), obs_x0, x_t)
        x = torch.cat([x, obs_mask.float()], dim=1)
        cond = self.time_mlp(timestep_embedding(timesteps, self.time_mlp[0].in_features))
        cond = cond + self.text_mlp(self._mask_text(text))
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
    def __init__(self, steps: int, schedule: str, device: torch.device) -> None:
        betas = get_named_beta_schedule(schedule, steps)
        alphas = 1.0 - betas
        alphas_cumprod = np.cumprod(alphas, axis=0)
        self.num_timesteps = int(steps)
        self.sqrt_alphas_cumprod = torch.from_numpy(np.sqrt(alphas_cumprod).astype(np.float32)).to(device)
        self.sqrt_one_minus_alphas_cumprod = torch.from_numpy(np.sqrt(1.0 - alphas_cumprod).astype(np.float32)).to(device)

    def q_sample(self, x_start: torch.Tensor, t: torch.Tensor, noise: torch.Tensor) -> torch.Tensor:
        shape = (x_start.shape[0],) + (1,) * (x_start.ndim - 1)
        a = self.sqrt_alphas_cumprod[t].view(shape)
        b = self.sqrt_one_minus_alphas_cumprod[t].view(shape)
        return a * x_start + b * noise


def sample_tasks(batch_size: int, probs: torch.Tensor, device: torch.device) -> torch.Tensor:
    return torch.multinomial(probs.to(device), batch_size, replacement=True)


def make_branch_masks(z: torch.Tensor, valid: torch.Tensor, task: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    b, _, t = z.shape
    if z.shape[1:] != (LATENT_DIM, LATENT_FRAMES):
        raise RuntimeError(f"expected z [B,{LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
    if valid.shape != (b, t):
        raise RuntimeError(f"expected valid [B,{t}], got {tuple(valid.shape)}")
    if task.shape != (b,):
        raise RuntimeError(f"expected task [B], got {tuple(task.shape)}")
    valid_bc = valid[:, None, :].expand(b, LATENT_DIM, t)
    obs = torch.zeros_like(z, dtype=torch.bool)
    camera_task = task == TASK_CAMERA
    human_task = task == TASK_HUMAN
    joint_task = task == TASK_JOINT
    if not torch.all(camera_task | human_task | joint_task):
        raise RuntimeError("unknown task id")
    obs[camera_task, :HUM_DIM, :] = True
    obs[human_task, HUM_DIM:, :] = True
    obs = obs & valid_bc
    loss_mask = valid_bc & (~obs)
    if torch.any(obs & loss_mask):
        raise RuntimeError("observed and target masks overlap")
    if torch.any((obs | loss_mask) & (~valid_bc)):
        raise RuntimeError("mask extends beyond valid latent frames")
    valid_counts = valid.long().sum(dim=1)
    expected_obs = torch.zeros_like(valid_counts)
    expected_loss = valid_counts * LATENT_DIM
    expected_obs[camera_task] = valid_counts[camera_task] * HUM_DIM
    expected_loss[camera_task] = valid_counts[camera_task] * CAM_DIM
    expected_obs[human_task] = valid_counts[human_task] * CAM_DIM
    expected_loss[human_task] = valid_counts[human_task] * HUM_DIM
    obs_counts = obs.flatten(1).long().sum(dim=1)
    loss_counts = loss_mask.flatten(1).long().sum(dim=1)
    if not torch.equal(obs_counts.cpu(), expected_obs.cpu()):
        raise RuntimeError(f"unexpected obs counts: {obs_counts.tolist()} vs {expected_obs.tolist()}")
    if not torch.equal(loss_counts.cpu(), expected_loss.cpu()):
        raise RuntimeError(f"unexpected loss counts: {loss_counts.tolist()} vs {expected_loss.tolist()}")
    return obs, loss_mask


def masked_target_mse(
    pred: torch.Tensor,
    target: torch.Tensor,
    loss_mask: torch.Tensor,
    task: torch.Tensor,
    joint_loss_mode: str = "element_mean",
    joint_human_branch_weight: float = 1.0,
    joint_camera_branch_weight: float = 1.0,
) -> tuple[torch.Tensor, dict[str, float]]:
    if joint_human_branch_weight <= 0 or joint_camera_branch_weight <= 0:
        raise RuntimeError("joint branch weights must be positive")
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

    if joint_loss_mode != "element_mean":
        joint_selected = task == TASK_JOINT
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

    total = per_sample.mean()
    metrics: dict[str, float] = {"loss": float(total.detach().cpu())}
    if joint_loss_mode != "element_mean":
        metrics["loss_element_mean"] = float(per_sample_element.mean().detach().cpu())
    for task_id, name in TASK_NAMES.items():
        selected = task == task_id
        if selected.any():
            metrics[f"loss_{name}"] = float(per_sample[selected].mean().detach().cpu())
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
    x_t: torch.Tensor,
    t: torch.Tensor,
    z: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    obs_mask: torch.Tensor,
    prob: float,
    mode: str,
    noise_std: float,
) -> tuple[torch.Tensor, dict[str, float]]:
    if prob <= 0.0 or mode == "clean" or not obs_mask.any():
        return z, {}
    sample_use = (torch.rand(z.shape[0], device=z.device) < prob).view(-1, 1, 1)
    value_use = sample_use & obs_mask
    if not value_use.any():
        return z, {"obs_self_condition_sample_frac": 0.0, "obs_self_condition_value_frac": 0.0}

    noisy_candidate = z + noise_std * torch.randn_like(z)
    generated_candidate = None
    generated_sample = torch.zeros_like(sample_use)
    if mode in {"joint_pred", "mixed"}:
        generated_sample = torch.ones_like(sample_use, dtype=torch.bool)
        if mode == "mixed":
            generated_sample = torch.rand(z.shape[0], device=z.device).view(-1, 1, 1) < 0.5
        joint_task = torch.full((z.shape[0],), TASK_JOINT, dtype=torch.long, device=z.device)
        joint_obs_mask, _ = make_branch_masks(z, valid, joint_task)
        was_training = model.training
        model.eval()
        with torch.no_grad():
            generated_candidate = model(x_t.detach(), t.detach(), text.detach(), obs_x0=z, obs_mask=joint_obs_mask).detach()
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
    sample_frac = value_use.flatten(1).any(dim=1).float().mean()
    value_frac = value_use.float().mean()
    metrics = {
        "obs_self_condition_sample_frac": float(sample_frac.detach().cpu()),
        "obs_self_condition_value_frac": float(value_frac.detach().cpu()),
    }
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
    return obs_x0, metrics


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
    obs_self_condition_prob: float = 0.0,
    obs_self_condition_mode: str = "clean",
    obs_self_condition_noise_std: float = 0.0,
) -> tuple[torch.Tensor, dict[str, float], torch.Tensor]:
    if noise is None:
        noise = torch.randn_like(z)
    if t is None:
        t = torch.randint(0, diffusion.num_timesteps, (z.shape[0],), device=z.device)
    obs_mask, loss_mask = make_branch_masks(z, valid, task)
    x_t = diffusion.q_sample(z, t, noise)
    obs_x0, obs_metrics = make_observed_condition_x0(
        model,
        x_t,
        t,
        z,
        text,
        valid,
        obs_mask,
        obs_self_condition_prob,
        obs_self_condition_mode,
        obs_self_condition_noise_std,
    )
    pred_x0 = model(x_t, t, text, obs_x0=obs_x0, obs_mask=obs_mask)
    if pred_x0.shape != z.shape:
        raise RuntimeError(f"model output shape mismatch: {tuple(pred_x0.shape)} vs {tuple(z.shape)}")
    loss, metrics = masked_target_mse(
        pred_x0,
        z,
        loss_mask,
        task,
        joint_loss_mode=joint_loss_mode,
        joint_human_branch_weight=joint_human_branch_weight,
        joint_camera_branch_weight=joint_camera_branch_weight,
    )
    metrics.update(obs_metrics)
    return loss, metrics, pred_x0


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
            t = torch.randint(0, diffusion.num_timesteps, (z.shape[0],), device=device)
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
            )
            for key, value in metrics.items():
                totals.setdefault(f"{task_name}_{key}", []).append(value)
                totals.setdefault(key, []).append(value)
            if task_id in {TASK_CAMERA, TASK_HUMAN} and z.shape[0] > 1:
                obs_mask, loss_mask = make_branch_masks(z, valid, task)
                x_t = diffusion.q_sample(z, t, noise)
                base = model(x_t, t, text, obs_x0=z, obs_mask=obs_mask)
                perm = torch.randperm(z.shape[0], device=device)
                z_shuf = z.clone()
                if task_id == TASK_CAMERA:
                    z_shuf[:, :HUM_DIM] = z[perm, :HUM_DIM]
                else:
                    z_shuf[:, HUM_DIM:] = z[perm, HUM_DIM:]
                shuf = model(x_t, t, text, obs_x0=z_shuf, obs_mask=obs_mask)
                base_loss, _ = masked_target_mse(
                    base,
                    z,
                    loss_mask,
                    task,
                    joint_loss_mode=joint_loss_mode,
                    joint_human_branch_weight=joint_human_branch_weight,
                    joint_camera_branch_weight=joint_camera_branch_weight,
                )
                shuf_loss, _ = masked_target_mse(
                    shuf,
                    z,
                    loss_mask,
                    task,
                    joint_loss_mode=joint_loss_mode,
                    joint_human_branch_weight=joint_human_branch_weight,
                    joint_camera_branch_weight=joint_camera_branch_weight,
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


def build_loaders(args: argparse.Namespace) -> tuple[DataLoader, DataLoader, DataLoader, dict[str, int]]:
    train_ds = PulpLatentCache(args.cache_dir / "train.pt")
    heldout_ds = PulpLatentCache(args.cache_dir / "val.pt")
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
    return train_loader, eval_loader, test_loader, sizes


def train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    train_loader, eval_loader, test_loader, sizes = build_loaders(args)
    dim_mults = tuple(int(v) for v in args.dim_mults)
    model = TemporalObsUNet(args.width, dim_mults, args.cond_mask_prob, args.zero_final, args.cond_mask_prob_cam, args.cond_mask_prob_hum).to(device)
    diffusion = CondMDIDiffusion(args.diffusion_steps, args.noise_schedule, device)
    ema_model = copy.deepcopy(model).eval().requires_grad_(False) if args.ema_decay > 0 else None
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, args.adam_beta2))
    task_probs = torch.tensor(args.task_probs, dtype=torch.float32)
    task_probs = task_probs / task_probs.sum()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "train_log.jsonl"
    meta = {
        "args": to_jsonable(args),
        "diffusion_beta_schedule_source": "inline_openai_guided_diffusion_compatible",
        "pipeline": "CondMDI-style q_sample + obs_x0/obs_mask input replacement + zero-keyframe target loss",
        "model_mean_type": "START_X",
        "latent_order": "concat([z_hum,z_cam])",
        "human_slice": [0, HUM_DIM],
        "camera_slice": [HUM_DIM, LATENT_DIM],
        "loss": "per-sample MSE over target branch and valid latent frames only; observed branch excluded",
        "joint_loss_mode": args.joint_loss_mode,
        "joint_human_branch_weight": args.joint_human_branch_weight,
        "joint_camera_branch_weight": args.joint_camera_branch_weight,
        "obs_self_condition": {
            "mode": args.obs_self_condition_mode,
            "prob": args.obs_self_condition_prob,
            "noise_std": args.obs_self_condition_noise_std,
        },
        "selection_metric": args.selection_metric,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "params": sum(p.numel() for p in model.parameters()),
        **sizes,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")

    step = 0
    best_eval = best_eval_from_log(log_path, args.selection_metric)
    if args.resume:
        checkpoint = torch.load(args.resume, map_location=device)
        model.load_state_dict(checkpoint.get("raw_model", checkpoint["model"]))
        opt.load_state_dict(checkpoint["opt"])
        step = int(checkpoint.get("step", 0))
        if ema_model is not None:
            ema_state = checkpoint.get("ema_model", checkpoint.get("model"))
            ema_model.load_state_dict(ema_state)
        write_record(
            log_path,
            {
                "step": step,
                "split": "resume",
                "resume_path": str(args.resume),
                "target_steps": args.steps,
                "best_eval_loss": best_eval,
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
                obs_self_condition_prob=args.obs_self_condition_prob,
                obs_self_condition_mode=args.obs_self_condition_mode,
                obs_self_condition_noise_std=args.obs_self_condition_noise_std,
            )
            opt.zero_grad(set_to_none=True)
            loss.backward()
            grad_norm = float(nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip).detach().cpu())
            opt.step()
            if ema_model is not None:
                update_ema_model(ema_model, model, args.ema_decay)

            if step == 1 or step % args.log_every == 0:
                record = {"step": step, "split": "train", **metrics, "lr": opt.param_groups[0]["lr"], "grad_norm": grad_norm}
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
                    "eval",
                    args.joint_loss_mode,
                    args.joint_human_branch_weight,
                    args.joint_camera_branch_weight,
                )
                record = {"step": step, "split": "eval", **metrics_eval}
                write_record(log_path, record)
                write_scalars(writer, "eval", metrics_eval, step)
                if args.selection_metric not in metrics_eval:
                    available = ", ".join(sorted(metrics_eval))
                    raise RuntimeError(f"selection metric {args.selection_metric!r} not found in eval metrics; available: {available}")
                eval_loss = float(metrics_eval[args.selection_metric])
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
                    "test",
                    args.joint_loss_mode,
                    args.joint_human_branch_weight,
                    args.joint_camera_branch_weight,
                )
                record = {"step": step, "split": "test", **metrics_test}
                write_record(log_path, record)
                write_scalars(writer, "test", metrics_test, step)
                torch.save(checkpoint_state(model, opt, step, meta, ema_model), out / "last.pt")

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
                return

            writer.flush()
            if step >= args.steps:
                break
    torch.save(checkpoint_state(model, opt, step, meta, ema_model), out / "last.pt")
    writer.close()


def check(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    ds = PulpLatentCache(args.cache_dir / "train.pt")
    batch = next(iter(DataLoader(ds, batch_size=min(args.batch_size, 8), shuffle=False, num_workers=0)))
    z = batch["z"].to(device)
    text = batch["text"].to(device)
    valid = batch["valid"].to(device)
    task = torch.tensor([TASK_CAMERA, TASK_HUMAN, TASK_JOINT, TASK_CAMERA, TASK_HUMAN, TASK_JOINT, TASK_CAMERA, TASK_HUMAN], device=device)[: z.shape[0]]
    obs_mask, loss_mask = make_branch_masks(z, valid, task)
    assert not torch.any(obs_mask & loss_mask)
    assert torch.all(obs_mask[:, HUM_DIM:] == 0) or True
    assert loss_mask.flatten(1).any(dim=1).all()
    pred = z.clone()
    pred[:, :HUM_DIM] += 1000.0
    camera_only = torch.full((z.shape[0],), TASK_CAMERA, dtype=torch.long, device=device)
    _, camera_loss_mask = make_branch_masks(z, valid, camera_only)
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
    _, joint_loss_mask = make_branch_masks(z, valid, joint_only)
    joint_branch_mean, branch_metrics = masked_target_mse(
        pred_camera,
        z,
        joint_loss_mask,
        joint_only,
        joint_loss_mode="branch_mean",
        joint_human_branch_weight=args.joint_human_branch_weight,
        joint_camera_branch_weight=args.joint_camera_branch_weight,
    )
    if not torch.isfinite(joint_branch_mean) or "loss_joint_element_mean" not in branch_metrics:
        raise RuntimeError("branch-normalized joint loss check failed")
    pred_human_obs = z.clone()
    pred_human_obs[:, HUM_DIM:] += 1000.0
    human_only = torch.full((z.shape[0],), TASK_HUMAN, dtype=torch.long, device=device)
    _, human_loss_mask = make_branch_masks(z, valid, human_only)
    human_base, _ = masked_target_mse(z, z, human_loss_mask, human_only)
    human_obs_perturbed, _ = masked_target_mse(pred_human_obs, z, human_loss_mask, human_only)
    if not torch.allclose(human_base, human_obs_perturbed):
        raise RuntimeError("human task loss changed when only observed camera branch was perturbed")
    model = TemporalObsUNet(args.width, tuple(int(v) for v in args.dim_mults), args.cond_mask_prob, args.zero_final, args.cond_mask_prob_cam, args.cond_mask_prob_hum).to(device)
    diffusion = CondMDIDiffusion(args.diffusion_steps, args.noise_schedule, device)
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
        obs_self_condition_prob=args.obs_self_condition_prob,
        obs_self_condition_mode=args.obs_self_condition_mode,
        obs_self_condition_noise_std=args.obs_self_condition_noise_std,
    )
    if pred_x0.shape != z.shape:
        raise RuntimeError(f"forward shape mismatch: {pred_x0.shape} vs {z.shape}")
    if not torch.isfinite(loss):
        raise RuntimeError("non-finite check loss")
    print(json.dumps({"ok": True, "loss": float(loss.detach().cpu()), "metrics": metrics, "shape": list(pred_x0.shape)}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["check", "train"])
    p.add_argument("--cache-dir", type=Path, default=ROOT / "runs/train/stage2/no_proj_pilot_20260610/cache_2048_gpu1")
    p.add_argument("--output-dir", type=Path, default=ROOT / "runs/train/stage2/condmdi_pulp_no_proj_20260611/gpu1_main")
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
    p.add_argument("--diffusion-steps", type=int, default=1000)
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
    p.add_argument("--task-probs", type=float, nargs=3, default=[1.0, 1.0, 1.0])
    p.add_argument("--joint-loss-mode", choices=["element_mean", "branch_mean", "branch_sum"], default="element_mean")
    p.add_argument("--joint-human-branch-weight", type=float, default=1.0)
    p.add_argument("--joint-camera-branch-weight", type=float, default=1.0)
    p.add_argument("--selection-metric", default="loss")
    p.add_argument("--obs-self-condition-prob", type=float, default=0.0)
    p.add_argument("--obs-self-condition-mode", choices=["clean", "noisy", "joint_pred", "mixed"], default="clean")
    p.add_argument("--obs-self-condition-noise-std", type=float, default=0.0)
    p.add_argument("--ema-decay", type=float, default=0.0)
    p.add_argument("--early-stop-patience", type=int, default=0)
    p.add_argument("--early-stop-min-delta", type=float, default=0.0)
    p.add_argument("--resume", type=Path)
    p.add_argument("--purge-step", type=int)
    return p


def main() -> None:
    args = build_parser().parse_args()
    if not (0.0 <= args.obs_self_condition_prob <= 1.0):
        raise ValueError("--obs-self-condition-prob must be in [0, 1]")
    if args.obs_self_condition_noise_std < 0.0:
        raise ValueError("--obs-self-condition-noise-std must be non-negative")
    if args.joint_human_branch_weight <= 0.0 or args.joint_camera_branch_weight <= 0.0:
        raise ValueError("--joint-*-branch-weight values must be positive")
    if args.mode == "check":
        check(args)
    else:
        train(args)


if __name__ == "__main__":
    main()
