#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import importlib.util
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
from torch.utils.data import DataLoader, Dataset, Subset

try:
    import yaml
except ImportError:  # pragma: no cover - config can still be JSON.
    yaml = None

try:
    from tensorboardX import SummaryWriter
except ImportError:  # pragma: no cover - fallback depends on env.
    try:
        from torch.utils.tensorboard import SummaryWriter
    except ImportError:  # pragma: no cover
        SummaryWriter = None  # type: ignore[assignment]


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


bridge = load_module("storymotion_official_bridge_smoke", SCRIPT_DIR / "storymotion_official_bridge_smoke.py")

HUM_DIM = 128
CAM_DIM = 64
LATENT_DIM = HUM_DIM + CAM_DIM
LATENT_FRAMES = 75
TEXT_DIM = 1024

SOURCE_CLEAN = 0
SOURCE_NOISY = 1
SOURCE_REPLAY = 2
SOURCE_NAMES = {SOURCE_CLEAN: "clean", SOURCE_NOISY: "noisy", SOURCE_REPLAY: "replay"}


class DecodeShim:
    HUM_DIM = HUM_DIM


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def timestep_embedding(t: torch.Tensor, dim: int, max_period: int = 10000) -> torch.Tensor:
    half = dim // 2
    freqs = torch.exp(
        -math.log(max_period) * torch.arange(0, half, dtype=torch.float32, device=t.device) / half
    )
    args = t.float()[:, None] * freqs[None]
    emb = torch.cat([torch.cos(args), torch.sin(args)], dim=-1)
    if dim % 2:
        emb = torch.cat([emb, torch.zeros_like(emb[:, :1])], dim=-1)
    return emb


def jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, torch.Tensor):
        if value.numel() == 1:
            return value.detach().cpu().item()
        return {"shape": list(value.shape), "dtype": str(value.dtype), "device": str(value.device)}
    return value


def to_jsonable_args(args: argparse.Namespace) -> dict[str, Any]:
    return {key: jsonable(value) for key, value in vars(args).items()}


def flatten_config(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in data.items():
        name = f"{prefix}_{key}" if prefix else str(key)
        name = name.replace("-", "_")
        if isinstance(value, dict):
            out.update(flatten_config(value, name))
        else:
            out[name] = value
    return out


def load_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    raw = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(raw)
    else:
        if yaml is None:
            raise RuntimeError("PyYAML is required for YAML config files; use JSON or install pyyaml")
        data = yaml.safe_load(raw)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"config must contain a mapping at top level: {path}")
    return flatten_config(data)


def coerce_config_value(value: Any, default: Any) -> Any:
    if isinstance(default, Path):
        return Path(value)
    if isinstance(default, tuple):
        return tuple(value)
    return value


def apply_config_defaults(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    config = load_config(args.config)
    applied: dict[str, Any] = {}
    ignored: dict[str, Any] = {}
    for key, value in config.items():
        if not hasattr(args, key):
            ignored[key] = value
            continue
        current = getattr(args, key)
        default = parser.get_default(key)
        if current == default:
            value = coerce_config_value(value, default)
            setattr(args, key, value)
            applied[key] = value
    args.config_applied = applied
    args.config_ignored = ignored


class H2CDataset(Dataset):
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
        self.source_type = data.get("source_type")
        if self.source_type is not None:
            self.source_type = self.source_type.long()
            if self.source_type.shape != (z.shape[0],):
                raise ValueError(f"expected source_type [N], got {tuple(self.source_type.shape)}")
        self.sigma = data.get("sigma")
        if self.sigma is not None:
            self.sigma = self.sigma.float()
            if self.sigma.shape != (z.shape[0],):
                raise ValueError(f"expected sigma [N], got {tuple(self.sigma.shape)}")

    def __len__(self) -> int:
        return int(self.z.shape[0])

    def __getitem__(self, index: int) -> dict[str, Any]:
        z = self.z[index]
        item = {
            "human": z[:HUM_DIM],
            "camera": z[HUM_DIM:],
            "z": z,
            "text": self.text[index],
            "valid": self.valid[index],
            "sample_id": self.sample_id[index],
        }
        if self.source_type is not None:
            item["source_type"] = self.source_type[index]
        if self.sigma is not None:
            item["sigma"] = self.sigma[index]
        return item


class GroupNorm1d(nn.Module):
    def __init__(self, channels: int) -> None:
        super().__init__()
        groups = 8
        while channels % groups != 0 and groups > 1:
            groups //= 2
        self.norm = nn.GroupNorm(groups, channels)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.norm(x)


class FiLMResidualBlock(nn.Module):
    def __init__(self, channels: int, cond_dim: int, kernel_size: int = 5) -> None:
        super().__init__()
        padding = kernel_size // 2
        self.conv1 = nn.Conv1d(channels, channels, kernel_size=kernel_size, padding=padding)
        self.norm1 = GroupNorm1d(channels)
        self.conv2 = nn.Conv1d(channels, channels, kernel_size=kernel_size, padding=padding)
        self.norm2 = GroupNorm1d(channels)
        self.cond = nn.Linear(cond_dim, channels * 2)
        nn.init.zeros_(self.conv2.weight)
        nn.init.zeros_(self.conv2.bias)

    def forward(self, x: torch.Tensor, cond: torch.Tensor) -> torch.Tensor:
        scale, shift = self.cond(cond).chunk(2, dim=-1)
        h = self.norm1(self.conv1(x))
        h = h * (1.0 + scale[:, :, None]) + shift[:, :, None]
        h = F.mish(h)
        h = F.mish(self.norm2(self.conv2(h)))
        return x + h


class H2CCameraGenerator(nn.Module):
    """Minimal asymmetric H2C camera completion model.

    It deliberately avoids joint denoising: the human latent is an observed
    condition, and only camera latent channels are predicted.
    """

    def __init__(
        self,
        width: int,
        layers: int,
        cond_mask_prob: float,
        use_source_type: bool,
        use_human_stats: bool,
    ) -> None:
        super().__init__()
        self.cond_mask_prob = float(cond_mask_prob)
        self.use_source_type = bool(use_source_type)
        self.use_human_stats = bool(use_human_stats)
        self.in_conv = nn.Conv1d(HUM_DIM, width, kernel_size=1)
        self.blocks = nn.ModuleList(FiLMResidualBlock(width, width) for _ in range(layers))
        self.out = nn.Sequential(GroupNorm1d(width), nn.Mish(), nn.Conv1d(width, CAM_DIM, kernel_size=1))
        self.text_mlp = nn.Sequential(
            nn.LayerNorm(TEXT_DIM),
            nn.Linear(TEXT_DIM, width * 2),
            nn.Mish(),
            nn.Linear(width * 2, width),
        )
        self.source_embed = nn.Embedding(len(SOURCE_NAMES), width) if self.use_source_type else None
        self.sigma_mlp = nn.Sequential(nn.Linear(1, width), nn.Mish(), nn.Linear(width, width))
        self.human_stats_mlp = (
            nn.Sequential(nn.LayerNorm(4), nn.Linear(4, width), nn.Mish(), nn.Linear(width, width))
            if self.use_human_stats
            else None
        )

    def _mask_text(self, text: torch.Tensor) -> torch.Tensor:
        if self.training and self.cond_mask_prob > 0:
            keep = 1.0 - torch.bernoulli(torch.full((text.shape[0], 1), self.cond_mask_prob, device=text.device))
            return text * keep
        return text

    @staticmethod
    def human_stats(human: torch.Tensor, valid: torch.Tensor) -> torch.Tensor:
        valid_f = valid[:, None, :].float()
        denom = valid_f.sum(dim=-1).clamp_min(1.0)
        mean_abs = (human.abs() * valid_f).sum(dim=(1, 2)) / denom.squeeze(1).clamp_min(1.0)
        rms = ((human.square() * valid_f).sum(dim=(1, 2)) / (denom.squeeze(1) * human.shape[1]).clamp_min(1.0)).sqrt()
        if human.shape[-1] > 1:
            vel = human[..., 1:] - human[..., :-1]
            valid_vel = (valid[:, 1:] & valid[:, :-1])[:, None, :].float()
            vel_denom = valid_vel.sum(dim=-1).clamp_min(1.0)
            vel_rms = ((vel.square() * valid_vel).sum(dim=(1, 2)) / (vel_denom.squeeze(1) * human.shape[1]).clamp_min(1.0)).sqrt()
        else:
            vel_rms = torch.zeros_like(rms)
        valid_ratio = valid.float().mean(dim=1)
        return torch.stack([mean_abs, rms, vel_rms, valid_ratio], dim=1)

    def forward(
        self,
        human: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        source_type: torch.Tensor | None = None,
        sigma: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if human.shape[1:] != (HUM_DIM, LATENT_FRAMES):
            raise ValueError(f"expected human [B,{HUM_DIM},{LATENT_FRAMES}], got {tuple(human.shape)}")
        if text.shape != (human.shape[0], TEXT_DIM):
            raise ValueError(f"expected text [B,{TEXT_DIM}], got {tuple(text.shape)}")
        if valid.shape != (human.shape[0], LATENT_FRAMES):
            raise ValueError(f"expected valid [B,{LATENT_FRAMES}], got {tuple(valid.shape)}")
        if source_type is None:
            source_type = torch.full((human.shape[0],), SOURCE_CLEAN, dtype=torch.long, device=human.device)
        if sigma is None:
            sigma = torch.zeros((human.shape[0],), dtype=human.dtype, device=human.device)
        cond = self.text_mlp(self._mask_text(text))
        cond = cond + self.sigma_mlp(sigma.to(dtype=human.dtype).view(-1, 1))
        if self.source_embed is not None:
            cond = cond + self.source_embed(source_type.to(device=human.device, dtype=torch.long).clamp(0, len(SOURCE_NAMES) - 1))
        if self.human_stats_mlp is not None:
            cond = cond + self.human_stats_mlp(self.human_stats(human, valid).to(dtype=human.dtype))
        h = self.in_conv(human)
        for block in self.blocks:
            h = block(h, cond)
        return self.out(h)


class MoLingoFullRFH2C(nn.Module):
    """MoLingo-style rectified-flow H2C camera generator.

    This is intentionally not a direct copy of MoLingo's text-to-human model.
    It keeps StoryMotion's asymmetric contract and borrows the key mechanism:
    a transformer condition network predicts a velocity field for continuous
    camera latent tokens under rectified-flow training.
    """

    def __init__(
        self,
        width: int,
        layers: int,
        heads: int,
        ff_mult: float,
        dropout: float,
        cond_mask_prob: float,
        flow_steps: int,
        local_window: int,
        use_source_type: bool,
        use_human_stats: bool,
    ) -> None:
        super().__init__()
        self.width = int(width)
        self.cond_mask_prob = float(cond_mask_prob)
        self.flow_steps = int(flow_steps)
        self.local_window = int(local_window)
        self.use_source_type = bool(use_source_type)
        self.use_human_stats = bool(use_human_stats)
        self.camera_in = nn.Linear(CAM_DIM, width)
        self.human_in = nn.Linear(HUM_DIM, width)
        self.camera_pos = nn.Parameter(torch.zeros(1, LATENT_FRAMES, width))
        self.human_pos = nn.Parameter(torch.zeros(1, LATENT_FRAMES, width))
        layer = nn.TransformerDecoderLayer(
            d_model=width,
            nhead=heads,
            dim_feedforward=int(width * ff_mult),
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.decoder = nn.TransformerDecoder(layer, num_layers=layers)
        self.text_mlp = nn.Sequential(
            nn.LayerNorm(TEXT_DIM),
            nn.Linear(TEXT_DIM, width * 2),
            nn.GELU(),
            nn.Linear(width * 2, width),
        )
        self.time_mlp = nn.Sequential(nn.Linear(width, width), nn.SiLU(), nn.Linear(width, width))
        self.source_embed = nn.Embedding(len(SOURCE_NAMES), width) if self.use_source_type else None
        self.sigma_mlp = nn.Sequential(nn.Linear(1, width), nn.SiLU(), nn.Linear(width, width))
        self.human_stats_mlp = (
            nn.Sequential(nn.LayerNorm(4), nn.Linear(4, width), nn.SiLU(), nn.Linear(width, width))
            if self.use_human_stats
            else None
        )
        self.out = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, CAM_DIM))
        self.initialize_weights()

    def initialize_weights(self) -> None:
        nn.init.normal_(self.camera_pos, std=0.02)
        nn.init.normal_(self.human_pos, std=0.02)
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.LayerNorm):
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
                if module.weight is not None:
                    nn.init.ones_(module.weight)
        final = self.out[-1]
        if isinstance(final, nn.Linear):
            nn.init.zeros_(final.weight)
            nn.init.zeros_(final.bias)

    def _mask_text(self, text: torch.Tensor) -> torch.Tensor:
        if self.training and self.cond_mask_prob > 0:
            keep = 1.0 - torch.bernoulli(torch.full((text.shape[0], 1), self.cond_mask_prob, device=text.device))
            return text * keep
        return text

    def _local_tgt_mask(self, device: torch.device) -> torch.Tensor | None:
        if self.local_window <= 0:
            return None
        idx = torch.arange(LATENT_FRAMES, device=device)
        return (idx[:, None] - idx[None, :]).abs() > self.local_window

    def _global_cond(
        self,
        human: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        t: torch.Tensor,
        source_type: torch.Tensor | None,
        sigma: torch.Tensor | None,
    ) -> torch.Tensor:
        if source_type is None:
            source_type = torch.full((human.shape[0],), SOURCE_CLEAN, dtype=torch.long, device=human.device)
        if sigma is None:
            sigma = torch.zeros((human.shape[0],), dtype=human.dtype, device=human.device)
        cond = self.text_mlp(self._mask_text(text))
        cond = cond + self.time_mlp(timestep_embedding(t.to(human.device), self.width))
        cond = cond + self.sigma_mlp(sigma.to(dtype=human.dtype).view(-1, 1))
        if self.source_embed is not None:
            cond = cond + self.source_embed(source_type.to(device=human.device, dtype=torch.long).clamp(0, len(SOURCE_NAMES) - 1))
        if self.human_stats_mlp is not None:
            cond = cond + self.human_stats_mlp(H2CCameraGenerator.human_stats(human, valid).to(dtype=human.dtype))
        return cond

    def velocity(
        self,
        human: torch.Tensor,
        camera_t: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        t: torch.Tensor,
        source_type: torch.Tensor | None = None,
        sigma: torch.Tensor | None = None,
    ) -> torch.Tensor:
        if human.shape[1:] != (HUM_DIM, LATENT_FRAMES):
            raise ValueError(f"expected human [B,{HUM_DIM},{LATENT_FRAMES}], got {tuple(human.shape)}")
        if camera_t.shape[1:] != (CAM_DIM, LATENT_FRAMES):
            raise ValueError(f"expected camera_t [B,{CAM_DIM},{LATENT_FRAMES}], got {tuple(camera_t.shape)}")
        cond = self._global_cond(human, text, valid, t, source_type, sigma)
        tgt = self.camera_in(camera_t.transpose(1, 2)) + self.camera_pos + cond[:, None, :]
        memory = self.human_in(human.transpose(1, 2)) + self.human_pos
        padding_mask = ~valid.bool()
        if padding_mask.all(dim=1).any():
            padding_mask = padding_mask.clone()
            padding_mask[padding_mask.all(dim=1), 0] = False
        h = self.decoder(
            tgt=tgt,
            memory=memory,
            tgt_mask=self._local_tgt_mask(human.device),
            tgt_key_padding_mask=None,
            memory_key_padding_mask=padding_mask,
        )
        return self.out(h).transpose(1, 2)

    def training_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        source_type: torch.Tensor | None = None,
        sigma: torch.Tensor | None = None,
        generator: torch.Generator | None = None,
    ) -> tuple[torch.Tensor, dict[str, float]]:
        noise = torch.randn(camera.shape, generator=generator, device=camera.device, dtype=camera.dtype)
        t = torch.rand((camera.shape[0],), generator=generator, device=camera.device, dtype=camera.dtype)
        t_view = t[:, None, None]
        camera_t = (1.0 - t_view) * noise + t_view * camera
        target_velocity = camera - noise
        pred_velocity = self.velocity(human, camera_t, text, valid, t, source_type=source_type, sigma=sigma)
        mask = valid[:, None, :].float()
        denom = (mask.sum() * camera.shape[1]).clamp_min(1.0)
        loss = ((pred_velocity - target_velocity).pow(2) * mask).sum() / denom
        with torch.no_grad():
            euler_one_step = noise + pred_velocity
            recon_mse, recon_metrics = masked_camera_mse(euler_one_step, camera, valid)
        return loss, {
            "flow_mse": float(loss.detach().cpu()),
            "one_step_camera_mse": float(recon_mse.detach().cpu()),
            "one_step_camera_mae": recon_metrics["camera_mae"],
        }

    @torch.no_grad()
    def sample(
        self,
        human: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        source_type: torch.Tensor | None = None,
        sigma: torch.Tensor | None = None,
        generator: torch.Generator | None = None,
        steps: int | None = None,
    ) -> torch.Tensor:
        steps = int(steps or self.flow_steps)
        if steps <= 0:
            raise ValueError("RF sample steps must be positive")
        x = torch.randn((human.shape[0], CAM_DIM, LATENT_FRAMES), generator=generator, device=human.device, dtype=human.dtype)
        for index in range(steps):
            t = torch.full((human.shape[0],), index / steps, device=human.device, dtype=human.dtype)
            velocity = self.velocity(human, x, text, valid, t, source_type=source_type, sigma=sigma)
            x = x + velocity / steps
            x = x.masked_fill(~valid[:, None, :].bool(), 0.0)
        return x

    def forward(
        self,
        human: torch.Tensor,
        text: torch.Tensor,
        valid: torch.Tensor,
        source_type: torch.Tensor | None = None,
        sigma: torch.Tensor | None = None,
    ) -> torch.Tensor:
        return self.sample(human, text, valid, source_type=source_type, sigma=sigma)


def corrupt_human(
    human: torch.Tensor,
    mode: str,
    sigma: float,
    *,
    generator: torch.Generator | None = None,
    replay_human: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    b = human.shape[0]
    device = human.device
    if mode == "clean":
        return human, torch.full((b,), SOURCE_CLEAN, dtype=torch.long, device=device), torch.zeros((b,), device=device)
    if mode == "noisy":
        noise = torch.randn(human.shape, generator=generator, device=device, dtype=human.dtype)
        return human + float(sigma) * noise, torch.full((b,), SOURCE_NOISY, dtype=torch.long, device=device), torch.full((b,), float(sigma), device=device)
    if mode == "replay":
        if replay_human is None:
            raise ValueError("replay mode requires replay_human")
        if replay_human.shape != human.shape:
            raise ValueError(f"replay_human shape {tuple(replay_human.shape)} does not match {tuple(human.shape)}")
        replay_sigma = (replay_human - human).flatten(1).std(dim=1, unbiased=False)
        return replay_human, torch.full((b,), SOURCE_REPLAY, dtype=torch.long, device=device), replay_sigma
    raise ValueError(f"unknown source mode: {mode}")


def corrupt_human_for_training(
    human: torch.Tensor,
    args: argparse.Namespace,
    generator: torch.Generator,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, str]:
    if args.train_source in {"clean", "noisy"}:
        human_cond, source_type, sigma_tensor = corrupt_human(
            human,
            args.train_source,
            args.train_noise_std,
            generator=generator,
        )
        return human_cond, source_type, sigma_tensor, args.train_source
    if args.train_source != "mixed-p2b":
        raise ValueError(f"unknown train source: {args.train_source}")
    b = human.shape[0]
    device = human.device
    probs = torch.tensor(args.p2b_noise_levels, device=device, dtype=human.dtype)
    if probs.numel() <= 0:
        raise ValueError("--p2b-noise-levels must not be empty")
    indices = torch.randint(probs.numel(), (b,), generator=generator, device=device)
    sigma_tensor = probs.index_select(0, indices)
    noise = torch.randn(human.shape, generator=generator, device=device, dtype=human.dtype)
    human_cond = human + sigma_tensor[:, None, None] * noise
    source_type = torch.where(
        sigma_tensor > 0,
        torch.full((b,), SOURCE_NOISY, dtype=torch.long, device=device),
        torch.full((b,), SOURCE_CLEAN, dtype=torch.long, device=device),
    )
    if args.p2b_missing_prob > 0:
        missing = torch.rand((b,), generator=generator, device=device) < float(args.p2b_missing_prob)
        human_cond = torch.where(missing[:, None, None], torch.zeros_like(human_cond), human_cond)
        source_type = torch.where(missing, torch.full_like(source_type, SOURCE_REPLAY), source_type)
        sigma_tensor = torch.where(missing, torch.ones_like(sigma_tensor), sigma_tensor)
    return human_cond, source_type, sigma_tensor, "mixed-p2b"


def cache_replay_condition(
    batch: dict[str, Any],
    human: torch.Tensor,
    device: torch.device,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, str]:
    b = human.shape[0]
    source_type = batch.get("source_type")
    sigma_tensor = batch.get("sigma")
    if source_type is None:
        source_type = torch.full((b,), SOURCE_REPLAY, dtype=torch.long)
    if sigma_tensor is None:
        sigma_tensor = torch.zeros((b,), dtype=human.dtype)
    return (
        human,
        source_type.to(device=device, dtype=torch.long),
        sigma_tensor.to(device=device, dtype=human.dtype),
        "cache-replay",
    )


def masked_camera_mse(pred: torch.Tensor, target: torch.Tensor, valid: torch.Tensor) -> tuple[torch.Tensor, dict[str, float]]:
    mask = valid[:, None, :].float()
    diff = (pred - target).pow(2) * mask
    denom = (mask.sum() * pred.shape[1]).clamp_min(1.0)
    mse = diff.sum() / denom
    mae = ((pred - target).abs() * mask).sum() / denom
    return mse, {"camera_mse": float(mse.detach().cpu()), "camera_mae": float(mae.detach().cpu())}


def training_camera_loss(
    model: nn.Module,
    human: torch.Tensor,
    camera: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    source_type: torch.Tensor,
    sigma_tensor: torch.Tensor,
    generator: torch.Generator,
) -> tuple[torch.Tensor, dict[str, float]]:
    if hasattr(model, "training_loss"):
        return model.training_loss(
            human,
            camera,
            text,
            valid,
            source_type=source_type,
            sigma=sigma_tensor,
            generator=generator,
        )
    pred = model(human, text, valid, source_type=source_type, sigma=sigma_tensor)
    return masked_camera_mse(pred, camera, valid)


def build_loaders(args: argparse.Namespace) -> tuple[DataLoader, DataLoader, DataLoader, dict[str, int]]:
    train_ds = H2CDataset(args.cache_dir / "train.pt")
    heldout_ds = H2CDataset(args.cache_dir / "val.pt")
    eval_count = min(args.eval_samples, len(heldout_ds))
    test_count = min(args.test_samples, max(0, len(heldout_ds) - eval_count))
    if eval_count <= 0 or test_count <= 0:
        raise RuntimeError(f"heldout cache must provide eval and test subsets, got {len(heldout_ds)}")
    eval_ds = Subset(heldout_ds, range(eval_count))
    test_ds = Subset(heldout_ds, range(eval_count, eval_count + test_count))
    return (
        DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.num_workers, drop_last=True),
        DataLoader(eval_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers),
        DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers),
        {"train_samples": len(train_ds), "eval_samples": len(eval_ds), "test_samples": len(test_ds)},
    )


def parse_eval_source(value: str) -> tuple[str, float]:
    if value == "clean":
        return "clean", 0.0
    if value == "replay":
        return "replay", 0.0
    if value == "cache-replay":
        return "cache-replay", 0.0
    if value.startswith("noisy:"):
        return "noisy", float(value.split(":", 1)[1])
    raise argparse.ArgumentTypeError(f"eval source must be clean, replay, cache-replay, or noisy:<sigma>, got {value!r}")


@torch.no_grad()
def evaluate_latent(
    model: nn.Module,
    loader: DataLoader,
    device: torch.device,
    max_batches: int,
    sources: list[tuple[str, float]],
    seed: int,
) -> dict[str, float]:
    was_training = model.training
    model.eval()
    totals: dict[str, list[float]] = {}
    clean_mse: float | None = None
    for source_index, (mode, sigma) in enumerate(sources):
        per_source: dict[str, list[float]] = {}
        for batch_index, batch in enumerate(loader):
            if batch_index >= max_batches:
                break
            human = batch["human"].to(device)
            camera = batch["camera"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            generator = torch.Generator(device=device)
            generator.manual_seed(seed + source_index * 10_007 + batch_index * 1_009)
            if mode == "cache-replay":
                human_cond, source_type, sigma_tensor, _ = cache_replay_condition(batch, human, device)
            else:
                human_cond, source_type, sigma_tensor = corrupt_human(human, mode, sigma, generator=generator)
            pred = model(human_cond, text, valid, source_type=source_type, sigma=sigma_tensor)
            _, metrics = masked_camera_mse(pred, camera, valid)
            if human.shape[0] > 1:
                perm = torch.randperm(human.shape[0], generator=generator, device=device)
                shuf_pred = model(human_cond[perm], text, valid, source_type=source_type, sigma=sigma_tensor)
                shuf_loss, _ = masked_camera_mse(shuf_pred, camera, valid)
                base_loss, _ = masked_camera_mse(pred, camera, valid)
                metrics["obs_shuffle_delta"] = float((shuf_loss - base_loss).detach().cpu())
            for key, value in metrics.items():
                per_source.setdefault(key, []).append(float(value))
        source_name = mode.replace("-", "_") if mode != "noisy" else f"noisy_{sigma:g}"
        source_metrics = {f"{source_name}_{key}": float(np.mean(values)) for key, values in per_source.items() if values}
        totals.update({key: [value] for key, value in source_metrics.items()})
        if mode == "clean":
            clean_mse = source_metrics.get(f"{source_name}_camera_mse")
    out = {key: values[0] for key, values in totals.items()}
    if clean_mse is not None and clean_mse > 0:
        for key, value in list(out.items()):
            if key.endswith("_camera_mse") and not key.startswith("clean_"):
                out[key.replace("_camera_mse", "_clean_retention_gap")] = (value - clean_mse) / clean_mse
    if was_training:
        model.train()
    return out


def checkpoint_state(
    model: nn.Module,
    opt: torch.optim.Optimizer,
    step: int,
    meta: dict[str, Any],
    ema_model: nn.Module | None,
) -> dict[str, Any]:
    eval_model = ema_model if ema_model is not None else model
    state = {"model": eval_model.state_dict(), "raw_model": model.state_dict(), "opt": opt.state_dict(), "step": step, "meta": meta}
    if ema_model is not None:
        state["ema_model"] = ema_model.state_dict()
    return state


@torch.no_grad()
def update_ema(ema_model: nn.Module, model: nn.Module, decay: float) -> None:
    for ema_param, param in zip(ema_model.parameters(), model.parameters()):
        ema_param.data.mul_(decay).add_(param.data, alpha=1.0 - decay)
    for ema_buffer, buffer in zip(ema_model.buffers(), model.buffers()):
        ema_buffer.copy_(buffer)


def write_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(jsonable(record), sort_keys=True) + "\n")
    print(json.dumps(jsonable(record), sort_keys=True), flush=True)


def is_scalar_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float, np.integer, np.floating))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def build_summary_writer(args: argparse.Namespace) -> Any | None:
    if not args.tensorboard:
        return None
    if SummaryWriter is None:
        print("WARNING: TensorBoard SummaryWriter unavailable; continuing with JSONL logs only.", flush=True)
        return None
    log_dir = args.tensorboard_log_dir or (args.output_dir / "tensorboard")
    return SummaryWriter(str(log_dir), flush_secs=args.tensorboard_flush_secs)


def write_tensorboard_scalars(writer: Any | None, split: str, record: dict[str, Any], step: int) -> None:
    if writer is None:
        return
    for key, value in record.items():
        if key in {"step", "split"}:
            continue
        if is_scalar_number(value):
            writer.add_scalar(f"{split}/{key}", float(value), step)


def build_model_from_args(args: argparse.Namespace) -> nn.Module:
    if args.model_name == "conv_h2c":
        return H2CCameraGenerator(
            width=args.width,
            layers=args.layers,
            cond_mask_prob=args.cond_mask_prob,
            use_source_type=args.use_source_type,
            use_human_stats=args.use_human_stats,
        )
    if args.model_name == "molingo_fullrf_h2c":
        return MoLingoFullRFH2C(
            width=args.width,
            layers=args.layers,
            heads=args.rf_heads,
            ff_mult=args.rf_ff_mult,
            dropout=args.rf_dropout,
            cond_mask_prob=args.cond_mask_prob,
            flow_steps=args.rf_sample_steps,
            local_window=args.rf_local_window,
            use_source_type=args.use_source_type,
            use_human_stats=args.use_human_stats,
        )
    raise ValueError(f"unknown model name: {args.model_name}")


def train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    train_loader, eval_loader, test_loader, sizes = build_loaders(args)
    model = build_model_from_args(args).to(device)
    init_info: dict[str, Any] | None = None
    if args.init_run_dir is not None:
        init_model, init_info = load_h2c(args.init_run_dir, device)
        load_info = model.load_state_dict(init_model.state_dict(), strict=True)
        print(json.dumps({"init_run": init_info, "load_info": str(load_info)}, sort_keys=True), flush=True)
    ema_model = copy.deepcopy(model).eval().requires_grad_(False) if args.ema_decay > 0 else None
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, args.adam_beta2))
    sources = [parse_eval_source(value) for value in args.eval_sources]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    log_path = args.output_dir / "train_log.jsonl"
    meta = {
        "kind": "stage2_model_switch",
        "model_name": args.model_name,
        "contract": "asymmetric H2C: observed human latent condition -> target camera latent only",
        "args": to_jsonable_args(args),
        "source_names": SOURCE_NAMES,
        "human_slice": [0, HUM_DIM],
        "camera_slice": [HUM_DIM, LATENT_DIM],
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "params": sum(p.numel() for p in model.parameters()),
        "init_info": init_info,
        **sizes,
    }
    (args.output_dir / "meta.json").write_text(json.dumps(jsonable(meta), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    writer = build_summary_writer(args)

    step = 0
    best_eval = float("inf")
    model.train()
    try:
        while step < args.steps:
            for batch_index, batch in enumerate(train_loader):
                step += 1
                human = batch["human"].to(device)
                camera = batch["camera"].to(device)
                text = batch["text"].to(device)
                valid = batch["valid"].to(device)
                generator = torch.Generator(device=device)
                generator.manual_seed(args.seed + step * 1_000_003)
                if args.train_source == "cache-replay":
                    human_cond, source_type, sigma_tensor, source_label = cache_replay_condition(batch, human, device)
                else:
                    human_cond, source_type, sigma_tensor, source_label = corrupt_human_for_training(human, args, generator)
                loss, metrics = training_camera_loss(model, human_cond, camera, text, valid, source_type, sigma_tensor, generator)
                opt.zero_grad(set_to_none=True)
                loss.backward()
                grad_norm = float(nn.utils.clip_grad_norm_(model.parameters(), args.grad_clip).detach().cpu())
                opt.step()
                if ema_model is not None:
                    update_ema(ema_model, model, args.ema_decay)
                if step == 1 or step % args.log_every == 0:
                    record = {"step": step, "split": "train", **metrics, "lr": opt.param_groups[0]["lr"], "grad_norm": grad_norm, "source": source_label}
                    write_jsonl(log_path, record)
                    write_tensorboard_scalars(writer, "train", record, step)
                if step == 1 or step % args.eval_every == 0:
                    eval_model = ema_model if ema_model is not None else model
                    eval_metrics = evaluate_latent(eval_model, eval_loader, device, args.eval_batches, sources, args.seed + 123)
                    eval_loss = float(eval_metrics.get(args.selection_metric, eval_metrics.get("clean_camera_mse", float("inf"))))
                    record = {"step": step, "split": "eval", **eval_metrics, "selection_metric": args.selection_metric, "selection_value": eval_loss}
                    write_jsonl(log_path, record)
                    write_tensorboard_scalars(writer, "eval", record, step)
                    state = checkpoint_state(model, opt, step, meta, ema_model)
                    torch.save(state, args.output_dir / "last.pt")
                    if eval_loss < best_eval:
                        best_eval = eval_loss
                        torch.save(state, args.output_dir / "best_eval.pt")
                if step == 1 or step % args.test_every == 0:
                    eval_model = ema_model if ema_model is not None else model
                    test_metrics = evaluate_latent(eval_model, test_loader, device, args.test_batches, sources, args.seed + 456)
                    record = {"step": step, "split": "test", **test_metrics}
                    write_jsonl(log_path, record)
                    write_tensorboard_scalars(writer, "test", record, step)
                    torch.save(checkpoint_state(model, opt, step, meta, ema_model), args.output_dir / "last.pt")
                if step >= args.steps:
                    break
        torch.save(checkpoint_state(model, opt, step, meta, ema_model), args.output_dir / "last.pt")
    finally:
        if writer is not None:
            writer.flush()
            writer.close()


def load_h2c(run_dir: Path, device: torch.device) -> tuple[nn.Module, dict[str, Any]]:
    meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    raw_args = meta["args"]
    ns = argparse.Namespace(
        model_name=str(raw_args.get("model_name", meta.get("model_name", "conv_h2c"))),
        width=int(raw_args.get("width", 384)),
        layers=int(raw_args.get("layers", 6)),
        cond_mask_prob=float(raw_args.get("cond_mask_prob", 0.1)),
        use_source_type=bool(raw_args.get("use_source_type", True)),
        use_human_stats=bool(raw_args.get("use_human_stats", False)),
        rf_heads=int(raw_args.get("rf_heads", 8)),
        rf_ff_mult=float(raw_args.get("rf_ff_mult", 4.0)),
        rf_dropout=float(raw_args.get("rf_dropout", 0.0)),
        rf_sample_steps=int(raw_args.get("rf_sample_steps", 16)),
        rf_local_window=int(raw_args.get("rf_local_window", 0)),
    )
    model = build_model_from_args(ns).to(device)
    ckpt_path = run_dir / "best_eval.pt"
    if not ckpt_path.exists():
        ckpt_path = run_dir / "last.pt"
    ckpt = torch.load(ckpt_path, map_location=device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    return model, {"run_dir": str(run_dir), "checkpoint": str(ckpt_path), "step": int(ckpt.get("step", -1)), "meta": meta}


def check(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    ds = H2CDataset(args.cache_dir / "train.pt")
    batch = next(iter(DataLoader(ds, batch_size=min(args.batch_size, 8), shuffle=False, num_workers=0)))
    model = build_model_from_args(args).to(device)
    human = batch["human"].to(device)
    camera = batch["camera"].to(device)
    text = batch["text"].to(device)
    valid = batch["valid"].to(device)
    pred = model(human, text, valid)
    if pred.shape != camera.shape:
        raise RuntimeError(f"shape mismatch {tuple(pred.shape)} vs {tuple(camera.shape)}")
    loss, metrics = masked_camera_mse(pred, camera, valid)
    if not torch.isfinite(loss):
        raise RuntimeError("non-finite loss")
    noisy, source_type, sigma_tensor = corrupt_human(human, "noisy", 0.15)
    pred_noisy = model(noisy, text, valid, source_type=source_type, sigma=sigma_tensor)
    if pred_noisy.shape != camera.shape:
        raise RuntimeError("noisy forward shape mismatch")
    print(json.dumps({"ok": True, "loss": float(loss.detach().cpu()), "metrics": metrics, "pred_shape": list(pred.shape)}, sort_keys=True))


@torch.no_grad()
def eval_latent(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    model, run_info = load_h2c(args.run_dir, device)
    ds = H2CDataset(args.cache_dir / args.cache_file)
    end = len(ds) if args.samples <= 0 else min(len(ds), args.start + args.samples)
    loader = DataLoader(Subset(ds, range(args.start, end)), batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
    sources = [parse_eval_source(value) for value in args.eval_sources]
    metrics = evaluate_latent(model, loader, device, math.ceil((end - args.start) / args.batch_size), sources, args.seed)
    payload = {
        "mode": "h2c_latent_eval",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "run": run_info,
        "cache_dir": str(args.cache_dir),
        "cache_file": args.cache_file,
        "sample_range": [args.start, end],
        "evaluated_samples": end - args.start,
        "eval_sources": args.eval_sources,
        "metrics": metrics,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "samples": end - args.start, "metric_keys": sorted(metrics)}, sort_keys=True))


@torch.no_grad()
def eval_official_camera(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    device = torch.device(args.device)
    model, run_info = load_h2c(args.run_dir, device)
    cache_mod = load_module("build_stage2_pulp_latent_cache", SCRIPT_DIR / "build_stage2_pulp_latent_cache.py")
    bridge.patch_numpy_aliases()
    args.workers = args.num_workers
    pulp_root = (args.pulp_root or ROOT / "linked/PulpMotion").resolve()
    cfg, dataset, autoencoder = bridge.build_pulp(cache_mod, ROOT, args, device)
    callback, module = bridge.instantiate_official_metrics(cfg, pulp_root, "camera", device)
    cache = H2CDataset(args.cache_dir / args.cache_file)
    end = len(cache) if args.samples <= 0 else min(len(cache), args.start + args.samples)
    loader = DataLoader(Subset(cache, range(args.start, end)), batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)
    mode, sigma = parse_eval_source(args.official_source)
    records_path = args.records or args.output.with_suffix(".records.jsonl")
    records_path.parent.mkdir(parents=True, exist_ok=True)
    if records_path.exists():
        records_path.unlink()
    processed = 0
    first_batch_summary = None
    with records_path.open("a", encoding="utf-8") as records_handle:
        for batch_index, batch in enumerate(loader):
            human = batch["human"].to(device)
            camera = batch["camera"].to(device)
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            sample_ids = [str(value) for value in batch["sample_id"]]
            generator = torch.Generator(device=device)
            generator.manual_seed(args.seed + batch_index * 1_009)
            human_cond, source_type, sigma_tensor = corrupt_human(human, mode, sigma, generator=generator)
            pred_camera = model(human_cond, text, valid, source_type=source_type, sigma=sigma_tensor)
            completion = torch.cat([human, pred_camera], dim=1)
            valid_bc = valid[:, None, :].expand_as(z)
            completion = torch.where(valid_bc, completion, z)
            pulp_batch = bridge.batch_from_sample_ids(dataset, sample_ids, device)
            intrinsics = pulp_batch["x_raw"]["intrinsics"]
            x_input, raw_input = bridge.reference_feature_and_raw(dataset, pulp_batch, intrinsics)
            x_output, raw_output = bridge.decode_feature_and_raw(autoencoder, dataset, DecodeShim, completion, intrinsics)
            official_outputs = bridge.official_outputs_for_task({"raw_input": raw_input, "raw_output": raw_output, "x_output": x_output}, "camera")
            callback.on_test_batch_end(None, module, official_outputs, pulp_batch, batch_index)
            for local_index, sample_id in enumerate(sample_ids):
                records_handle.write(
                    json.dumps(
                        {
                            "sample_id": sample_id,
                            "sample_index": args.start + processed + local_index,
                            "mode": "camera",
                            "observed_branch": "human",
                            "target_branch": "camera",
                            "source": args.official_source,
                            "checkpoint": run_info["checkpoint"],
                            "checkpoint_step": run_info["step"],
                            "run_dir": run_info["run_dir"],
                        },
                        sort_keys=True,
                    )
                    + "\n"
                )
            processed += len(sample_ids)
            if first_batch_summary is None:
                first_batch_summary = {
                    "sample_ids": sample_ids,
                    "z_shape": list(z.shape),
                    "completion_shape": list(completion.shape),
                    "x_input": jsonable(x_input),
                }
            if args.progress_every > 0 and (batch_index + 1) % args.progress_every == 0:
                print(json.dumps({"processed": processed, "target": end - args.start}, sort_keys=True), flush=True)
    callback.on_test_epoch_end(None, module)
    metrics = bridge.metric_values(module.eval_metrics)
    payload = {
        "mode": "h2c_official_camera_eval",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "run": run_info,
        "cache_dir": str(args.cache_dir),
        "cache_file": args.cache_file,
        "sample_range": [args.start, end],
        "evaluated_samples": processed,
        "official_source": args.official_source,
        "metric_keys": sorted(metrics),
        "metrics": metrics,
        "records_path": str(records_path),
        "first_batch_summary": first_batch_summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "records": str(records_path), "samples": processed, "keys": len(metrics)}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Configurable asymmetric StoryMotion Stage2 H2C camera generator.")
    p.add_argument("mode", choices=["check", "train", "eval-latent", "eval-official-camera"])
    p.add_argument("--config", type=Path, help="YAML/JSON config whose keys act as defaults; CLI arguments override it")
    p.add_argument("--cache-dir", type=Path, default=ROOT / "runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110")
    p.add_argument("--cache-file", default="val.pt")
    p.add_argument("--run-dir", type=Path)
    p.add_argument("--init-run-dir", type=Path, help="optional H2C run used to initialize train mode")
    p.add_argument("--output-dir", type=Path, default=ROOT / "runs/train/stage2/stage2_h2c_minimal")
    p.add_argument("--output", type=Path, default=ROOT / "runs/eval/stage2/stage2_h2c_minimal/eval.json")
    p.add_argument("--records", type=Path)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--seed", type=int, default=17)
    p.add_argument("--steps", type=int, default=50000)
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--num-workers", type=int, default=2)
    p.add_argument("--width", type=int, default=384)
    p.add_argument("--layers", type=int, default=8)
    p.add_argument("--model-name", choices=["conv_h2c", "molingo_fullrf_h2c"], default="conv_h2c")
    p.add_argument("--rf-heads", type=int, default=8)
    p.add_argument("--rf-ff-mult", type=float, default=4.0)
    p.add_argument("--rf-dropout", type=float, default=0.0)
    p.add_argument("--rf-sample-steps", type=int, default=16)
    p.add_argument("--rf-local-window", type=int, default=0, help="0 uses full camera self-attention; positive values restrict target self-attention to +/- window")
    p.add_argument("--cond-mask-prob", type=float, default=0.1)
    p.add_argument("--use-source-type", action="store_true", default=True)
    p.add_argument("--no-use-source-type", action="store_false", dest="use_source_type")
    p.add_argument("--use-human-stats", action="store_true")
    p.add_argument("--train-source", choices=["clean", "noisy", "mixed-p2b", "cache-replay"], default="clean")
    p.add_argument("--train-noise-std", type=float, default=0.0)
    p.add_argument("--p2b-noise-levels", type=float, nargs="+", default=[0.0, 0.05, 0.10, 0.15, 0.30])
    p.add_argument("--p2b-missing-prob", type=float, default=0.0)
    p.add_argument("--eval-sources", nargs="+", default=["clean", "noisy:0.05", "noisy:0.1", "noisy:0.15", "noisy:0.2"])
    p.add_argument("--official-source", default="clean")
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--weight-decay", type=float, default=0.01)
    p.add_argument("--adam-beta2", type=float, default=0.999)
    p.add_argument("--grad-clip", type=float, default=1.0)
    p.add_argument("--ema-decay", type=float, default=0.999)
    p.add_argument("--log-every", type=int, default=100)
    p.add_argument("--eval-every", type=int, default=1000)
    p.add_argument("--test-every", type=int, default=5000)
    p.add_argument("--eval-batches", type=int, default=8)
    p.add_argument("--eval-samples", type=int, default=512)
    p.add_argument("--test-batches", type=int, default=8)
    p.add_argument("--test-samples", type=int, default=512)
    p.add_argument("--selection-metric", default="clean_camera_mse")
    p.add_argument("--tensorboard", action="store_true", default=True)
    p.add_argument("--no-tensorboard", action="store_false", dest="tensorboard")
    p.add_argument("--tensorboard-log-dir", type=Path)
    p.add_argument("--tensorboard-flush-secs", type=int, default=30)
    p.add_argument("--samples", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--split", default="test")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    p.add_argument("--pulp-root", type=Path)
    p.add_argument("--data-root", type=Path)
    p.add_argument("--progress-every", type=int, default=10)
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    apply_config_defaults(args, parser)
    if args.cond_mask_prob < 0 or args.cond_mask_prob > 1:
        raise ValueError("--cond-mask-prob must be in [0,1]")
    if args.train_noise_std < 0:
        raise ValueError("--train-noise-std must be non-negative")
    if args.rf_heads <= 0:
        raise ValueError("--rf-heads must be positive")
    if args.rf_sample_steps <= 0:
        raise ValueError("--rf-sample-steps must be positive")
    if args.rf_local_window < 0:
        raise ValueError("--rf-local-window must be non-negative")
    if args.p2b_missing_prob < 0 or args.p2b_missing_prob > 1:
        raise ValueError("--p2b-missing-prob must be in [0,1]")
    if any(float(level) < 0 for level in args.p2b_noise_levels):
        raise ValueError("--p2b-noise-levels must be non-negative")
    if args.mode == "check":
        check(args)
    elif args.mode == "train":
        train(args)
    elif args.mode == "eval-latent":
        if args.run_dir is None:
            raise ValueError("--run-dir is required for eval-latent")
        eval_latent(args)
    elif args.mode == "eval-official-camera":
        if args.run_dir is None:
            raise ValueError("--run-dir is required for eval-official-camera")
        eval_official_camera(args)
    else:
        raise RuntimeError(f"unknown mode {args.mode}")


if __name__ == "__main__":
    main()
