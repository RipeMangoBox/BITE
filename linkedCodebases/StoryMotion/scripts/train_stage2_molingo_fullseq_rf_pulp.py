#!/usr/bin/env python3
"""Train representation-matched MoLingo-derived Unified-3 RF Stage2 variants.

The full-sequence control conditions every temporal token on the same RF-noised
sequence. The masked-iterative screen follows official MoLingo's random mask
training with bidirectional attention while retaining StoryMotion's frozen
non-causal v7.14 tokenizer. Non-causal latents forbid streaming/causal claims;
they do not prevent offline masked latent generation.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
import os
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset, Subset
from transformers import AutoTokenizer, T5EncoderModel

try:
    from tensorboardX import SummaryWriter
except ImportError:
    SummaryWriter = None


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import train_stage2_condmdi_pulp as base
from storymotion.experiment_invariants import assert_default_cache_meta
from storymotion.stage2.processes import build_stage2_process
from storymotion_run_layout import init_run, run_paths, update_manifest


TASK_CAMERA = base.TASK_CAMERA
TASK_HUMAN = base.TASK_HUMAN
TASK_JOINT = base.TASK_JOINT
TASK_NAMES = tuple(base.TASK_NAMES[index] for index in range(3))
LATENT_DIM = base.LATENT_DIM
LATENT_FRAMES = base.LATENT_FRAMES
HUM_DIM = base.HUM_DIM


def active_task_pairs(task_scope: str) -> tuple[tuple[int, str], ...]:
    if task_scope == "human_only":
        return ((TASK_HUMAN, "human"),)
    if task_scope == "unified3":
        return tuple(enumerate(TASK_NAMES))
    raise ValueError(f"unknown task scope: {task_scope}")


class CaptionedLatentCache(Dataset):
    def __init__(
        self,
        cache_path: Path,
        stats: dict[str, Any],
        data_root: Path,
        caption_cache_path: Path,
        caption_workers: int,
    ) -> None:
        self.cache = base.PulpLatentCache(cache_path, znorm_stats=stats)
        assert_default_cache_meta(self.cache.meta)
        self.caption_cache_path = caption_cache_path
        sample_ids = [str(value) for value in self.cache.sample_id]
        if caption_cache_path.is_file():
            payload = torch.load(caption_cache_path, map_location="cpu")
            if payload.get("sample_id") != sample_ids:
                raise RuntimeError(f"caption cache sample IDs do not match {cache_path}")
        else:
            human_root = data_root / "caption_char"
            camera_root = data_root / "caption_cam"

            def read_pair(sample_id: str) -> tuple[str, str]:
                human = (human_root / f"{sample_id}.txt").read_text(encoding="utf-8").strip()
                camera = (camera_root / f"{sample_id}.txt").read_text(encoding="utf-8").strip()
                if not human or not camera:
                    raise ValueError(f"empty caption for {sample_id}")
                return human, camera

            with ThreadPoolExecutor(max_workers=caption_workers) as executor:
                pairs = list(executor.map(read_pair, sample_ids))
            payload = {
                "sample_id": sample_ids,
                "human_caption": [pair[0] for pair in pairs],
                "camera_caption": [pair[1] for pair in pairs],
                "human_root": str(human_root),
                "camera_root": str(camera_root),
            }
            caption_cache_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = caption_cache_path.with_suffix(caption_cache_path.suffix + ".tmp")
            torch.save(payload, temporary)
            temporary.replace(caption_cache_path)
        self.human_caption = payload["human_caption"]
        self.camera_caption = payload["camera_caption"]

    @property
    def sample_id(self) -> list[str]:
        return [str(value) for value in self.cache.sample_id]

    @property
    def meta(self) -> dict[str, Any]:
        return self.cache.meta

    def __len__(self) -> int:
        return len(self.cache)

    def __getitem__(self, index: int) -> dict[str, Any]:
        item = self.cache[index]
        item["human_caption"] = self.human_caption[index]
        item["camera_caption"] = self.camera_caption[index]
        return item


class TextAdapter(nn.Module):
    def __init__(self, width: int, heads: int, layers: int, dropout: float) -> None:
        super().__init__()
        layer = nn.TransformerEncoderLayer(
            d_model=width,
            nhead=heads,
            dim_feedforward=4 * width,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.blocks = nn.TransformerEncoder(layer, num_layers=layers)
        self.norm = nn.LayerNorm(width)

    def forward(self, x: torch.Tensor, padding_mask: torch.Tensor) -> torch.Tensor:
        return self.norm(self.blocks(x, src_key_padding_mask=padding_mask))


class TimestepEmbedder(nn.Module):
    def __init__(self, width: int, frequency_dim: int = 256) -> None:
        super().__init__()
        self.frequency_dim = frequency_dim
        self.mlp = nn.Sequential(nn.Linear(frequency_dim, width), nn.SiLU(), nn.Linear(width, width))

    def forward(self, timesteps: torch.Tensor) -> torch.Tensor:
        half = self.frequency_dim // 2
        frequencies = torch.exp(
            -math.log(10000.0)
            * torch.arange(half, device=timesteps.device, dtype=torch.float32)
            / half
        )
        angles = timesteps.float()[:, None] * frequencies[None]
        embedding = torch.cat([torch.cos(angles), torch.sin(angles)], dim=-1)
        if self.frequency_dim % 2:
            embedding = torch.cat([embedding, torch.zeros_like(embedding[:, :1])], dim=-1)
        return self.mlp(embedding)


def modulate(x: torch.Tensor, shift: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    return x * (1.0 + scale) + shift


class FlowResidualBlock(nn.Module):
    def __init__(self, width: int) -> None:
        super().__init__()
        self.norm = nn.LayerNorm(width, eps=1.0e-6)
        self.mlp = nn.Sequential(nn.Linear(width, width), nn.SiLU(), nn.Linear(width, width))
        self.cond = nn.Sequential(nn.SiLU(), nn.Linear(width, 3 * width))

    def forward(self, x: torch.Tensor, condition: torch.Tensor) -> torch.Tensor:
        shift, scale, gate = self.cond(condition).chunk(3, dim=-1)
        return x + gate * self.mlp(modulate(self.norm(x), shift, scale))


class TokenFlowHead(nn.Module):
    def __init__(self, condition_dim: int, width: int, depth: int) -> None:
        super().__init__()
        self.input_proj = nn.Linear(LATENT_DIM, width)
        self.condition_proj = nn.Linear(condition_dim, width)
        self.time = TimestepEmbedder(width)
        self.blocks = nn.ModuleList([FlowResidualBlock(width) for _ in range(depth)])
        self.final_norm = nn.LayerNorm(width, elementwise_affine=False, eps=1.0e-6)
        self.final_modulation = nn.Sequential(nn.SiLU(), nn.Linear(width, 2 * width))
        self.output = nn.Linear(width, LATENT_DIM)
        self._initialize()

    def _initialize(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
        for block in self.blocks:
            nn.init.zeros_(block.cond[-1].weight)
            nn.init.zeros_(block.cond[-1].bias)
        nn.init.zeros_(self.final_modulation[-1].weight)
        nn.init.zeros_(self.final_modulation[-1].bias)
        nn.init.zeros_(self.output.weight)
        nn.init.zeros_(self.output.bias)

    def forward(
        self,
        x: torch.Tensor,
        timesteps: torch.Tensor,
        condition: torch.Tensor,
    ) -> torch.Tensor:
        y = self.time(timesteps) + self.condition_proj(condition)
        h = self.input_proj(x)
        for block in self.blocks:
            h = block(h, y)
        shift, scale = self.final_modulation(y).chunk(2, dim=-1)
        return self.output(modulate(self.final_norm(h), shift, scale))


class MoLingoFullSequenceRF(nn.Module):
    def __init__(
        self,
        t5_path: Path,
        transformer_width: int,
        transformer_depth: int,
        transformer_heads: int,
        adapter_layers: int,
        flow_width: int,
        flow_depth: int,
        dropout: float,
        text_drop_prob: float,
        t5_max_length: int,
        temporal_mode: str,
    ) -> None:
        super().__init__()
        self.text_drop_prob = float(text_drop_prob)
        self.t5_max_length = int(t5_max_length)
        self.temporal_mode = temporal_mode
        if temporal_mode not in {"full_sequence_rf", "masked_iterative_rf"}:
            raise ValueError(f"unknown temporal mode: {temporal_mode}")
        self.tokenizer = AutoTokenizer.from_pretrained(t5_path, local_files_only=True, use_fast=True)
        self.t5_model = T5EncoderModel.from_pretrained(
            t5_path,
            local_files_only=True,
            torch_dtype=torch.bfloat16,
        )
        self.t5_model.requires_grad_(False).eval()
        if int(self.t5_model.config.d_model) != 1024:
            raise ValueError(f"expected T5 d_model=1024, got {self.t5_model.config.d_model}")
        self.text_proj = nn.Linear(1024, transformer_width)
        self.text_adapter = TextAdapter(
            transformer_width,
            transformer_heads,
            adapter_layers,
            dropout,
        )
        self.input_proj = nn.Linear(2 * LATENT_DIM, transformer_width)
        self.position = nn.Parameter(torch.zeros(1, LATENT_FRAMES, transformer_width))
        self.task_embedding = nn.Embedding(3, transformer_width)
        self.mask_token = (
            nn.Parameter(torch.zeros(1, LATENT_DIM, 1))
            if temporal_mode == "masked_iterative_rf"
            else None
        )
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=transformer_width,
            nhead=transformer_heads,
            dim_feedforward=4 * transformer_width,
            dropout=dropout,
            activation="gelu",
            batch_first=True,
        )
        self.transformer = nn.TransformerDecoder(decoder_layer, num_layers=transformer_depth)
        self.flow_head = TokenFlowHead(transformer_width, flow_width, flow_depth)
        nn.init.normal_(self.position, std=0.02)
        nn.init.normal_(self.task_embedding.weight, std=0.02)

    def train(self, mode: bool = True) -> "MoLingoFullSequenceRF":
        super().train(mode)
        self.t5_model.eval()
        return self

    def _drop_text(self, prompts: Sequence[str], force_drop: bool) -> list[str]:
        null_prompt = "This is a null prompt with no semantic meaning."
        if force_drop:
            return [null_prompt] * len(prompts)
        if not self.training or self.text_drop_prob <= 0.0:
            return list(prompts)
        drop = torch.rand(len(prompts)) < self.text_drop_prob
        return [null_prompt if bool(drop[index]) else prompt for index, prompt in enumerate(prompts)]

    def _encode_text(
        self,
        prompts: Sequence[str],
        device: torch.device,
        force_drop: bool,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        encoded = self.tokenizer(
            self._drop_text(prompts, force_drop),
            max_length=self.t5_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
            return_attention_mask=True,
        )
        input_ids = encoded["input_ids"].to(device)
        attention = encoded["attention_mask"].to(device)
        with torch.no_grad():
            hidden = self.t5_model(input_ids=input_ids, attention_mask=attention).last_hidden_state
        padding_mask = ~attention.bool()
        memory = self.text_adapter(self.text_proj(hidden), padding_mask)
        return memory, padding_mask

    def forward(
        self,
        x_t: torch.Tensor,
        timesteps: torch.Tensor,
        prompts: Sequence[str],
        valid: torch.Tensor,
        obs_x0: torch.Tensor,
        obs_mask: torch.Tensor,
        task: torch.Tensor,
        rf_mask: torch.Tensor | None = None,
        *,
        force_text_drop: bool = False,
        text_condition: tuple[torch.Tensor, torch.Tensor] | None = None,
    ) -> torch.Tensor:
        if x_t.shape != (valid.shape[0], LATENT_DIM, LATENT_FRAMES):
            raise ValueError(f"invalid latent shape: {tuple(x_t.shape)}")
        if obs_x0.shape != x_t.shape or obs_mask.shape != x_t.shape:
            raise ValueError("obs_x0/obs_mask must match x_t")
        if len(prompts) != x_t.shape[0] or task.shape != (x_t.shape[0],):
            raise ValueError("prompt/task batch mismatch")
        if rf_mask is None:
            x_model = torch.where(obs_mask, obs_x0, x_t)
            flow_input = x_model
            input_mask = obs_mask
        else:
            if self.mask_token is None or rf_mask.shape != x_t.shape:
                raise ValueError("masked iterative RF requires a matching rf_mask and mask token")
            x_model = torch.where(rf_mask, self.mask_token.to(x_t.dtype), obs_x0)
            flow_input = torch.where(rf_mask, x_t, x_model)
            input_mask = rf_mask
        human_only = task == TASK_HUMAN
        if human_only.any():
            x_model = x_model.clone()
            x_model[human_only, HUM_DIM:, :] = 0.0
            flow_input = flow_input.clone()
            flow_input[human_only, HUM_DIM:, :] = 0.0
        tokens = torch.cat([x_model, input_mask.to(x_model.dtype)], dim=1).transpose(1, 2)
        tokens = self.input_proj(tokens) + self.position + self.task_embedding(task)[:, None]
        if text_condition is None:
            memory, text_padding = self._encode_text(prompts, x_t.device, force_text_drop)
        else:
            memory, text_padding = text_condition
        condition = self.transformer(
            tgt=tokens,
            memory=memory,
            tgt_key_padding_mask=~valid,
            memory_key_padding_mask=text_padding,
        )
        flat_x = flow_input.transpose(1, 2).reshape(-1, LATENT_DIM)
        flat_condition = condition.reshape(-1, condition.shape[-1])
        flat_t = timesteps[:, None].expand(-1, LATENT_FRAMES).reshape(-1)
        velocity = self.flow_head(flat_x, flat_t, flat_condition)
        velocity = velocity.reshape(x_t.shape[0], LATENT_FRAMES, LATENT_DIM).transpose(1, 2)
        return velocity.masked_fill(~valid[:, None, :], 0.0)


def task_prompts(
    human_captions: Sequence[str],
    camera_captions: Sequence[str],
    task: torch.Tensor,
) -> list[str]:
    prompts: list[str] = []
    for human, camera, task_id in zip(human_captions, camera_captions, task.detach().cpu().tolist()):
        if task_id == TASK_CAMERA:
            prompts.append(f"Camera motion: {camera}")
        elif task_id == TASK_HUMAN:
            prompts.append(f"Human motion: {human}")
        elif task_id == TASK_JOINT:
            prompts.append(f"Human motion: {human} Camera motion: {camera}")
        else:
            raise ValueError(f"unknown task id {task_id}")
    return prompts


def diffusion_loss(
    model: MoLingoFullSequenceRF,
    process: Any,
    z: torch.Tensor,
    valid: torch.Tensor,
    prompts: Sequence[str],
    task: torch.Tensor,
    temporal_mode: str = "full_sequence_rf",
) -> tuple[torch.Tensor, dict[str, float]]:
    noise = torch.randn_like(z)
    t = process.sample_t(z.shape[0], z.device)
    x_t = process.q_sample(z, t, noise)
    target = process.training_target(z, noise, t)
    obs_mask, loss_mask = base.make_branch_masks(z, valid, task, task_routing="human_first")
    rf_mask = None
    if temporal_mode == "masked_iterative_rf":
        rand_time = torch.rand(z.shape[0], device=z.device)
        mask_ratio = torch.cos(rand_time * math.pi * 0.5)
        valid_counts = valid.sum(dim=1)
        num_masked = (valid_counts * mask_ratio).round().clamp(min=1)
        ranks = torch.rand_like(valid, dtype=torch.float32).masked_fill(~valid, 2.0).argsort(dim=1).argsort(dim=1)
        temporal_mask = (ranks < num_masked[:, None]) & valid
        rf_mask = temporal_mask[:, None, :].expand_as(loss_mask) & loss_mask
        loss_mask = rf_mask
    elif temporal_mode != "full_sequence_rf":
        raise ValueError(f"unknown temporal mode: {temporal_mode}")
    prediction = model(
        x_t,
        process.model_t(t),
        prompts,
        valid,
        obs_x0=z,
        obs_mask=obs_mask,
        task=task,
        rf_mask=rf_mask,
    )
    loss, metrics = base.masked_target_mse(
        prediction,
        target,
        loss_mask,
        task,
        joint_loss_mode="element_mean",
    )
    if rf_mask is not None:
        metrics["temporal_mask_ratio"] = float(
            (rf_mask.any(dim=1).sum(dim=1).float() / valid.sum(dim=1).clamp_min(1)).mean().detach().cpu()
        )
    return loss, metrics


def deterministic_sample_tensor(
    shape: tuple[int, ...],
    sample_indices: Sequence[int],
    seed: int,
    device: torch.device,
    dtype: torch.dtype,
    *,
    normal: bool,
) -> torch.Tensor:
    if shape[0] != len(sample_indices):
        raise ValueError(f"batch shape {shape[0]} does not match sample indices {len(sample_indices)}")
    parts = []
    for sample_index in sample_indices:
        generator = torch.Generator(device="cpu")
        generator.manual_seed(int(seed) + int(sample_index) * 1_000_003)
        sample = (
            torch.randn(shape[1:], generator=generator, dtype=torch.float32)
            if normal
            else torch.rand(shape[1:], generator=generator, dtype=torch.float32)
        )
        parts.append(sample)
    return torch.stack(parts).to(device=device, dtype=dtype)


@torch.no_grad()
def sample_stage2(
    model: MoLingoFullSequenceRF,
    process: Any,
    z: torch.Tensor,
    valid: torch.Tensor,
    human_captions: Sequence[str],
    camera_captions: Sequence[str],
    task_id: int,
    sample_indices: Sequence[int],
    seed: int,
    *,
    rf_steps: int,
    cfg_scale: float,
    unmask_steps: int,
) -> torch.Tensor:
    """Sample one Unified-3 task with the run's declared temporal mode."""
    if rf_steps <= 0 or unmask_steps <= 0:
        raise ValueError("rf_steps and unmask_steps must be positive")
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, loss_mask = base.make_branch_masks(z, valid, task, task_routing="human_first")
    prompts = task_prompts(human_captions, camera_captions, task)
    with torch.autocast(device_type=z.device.type, dtype=torch.bfloat16, enabled=z.is_cuda):
        conditional_text = model._encode_text(prompts, z.device, force_drop=False)
        unconditional_text = (
            model._encode_text(prompts, z.device, force_drop=True)
            if cfg_scale != 1.0
            else None
        )

    def integrate(active_mask: torch.Tensor, context: torch.Tensor, rf_mask: torch.Tensor | None, noise_seed: int) -> torch.Tensor:
        noise = deterministic_sample_tensor(
            tuple(z.shape), sample_indices, noise_seed, z.device, z.dtype, normal=True
        )
        x = torch.where(active_mask, noise, context)
        times = torch.linspace(0.0, 1.0, rf_steps + 1, device=z.device, dtype=torch.float32)
        for step_index in range(rf_steps):
            t = torch.full((z.shape[0],), float(times[step_index]), device=z.device)
            model_t = process.model_t(t)
            with torch.autocast(device_type=z.device.type, dtype=torch.bfloat16, enabled=z.is_cuda):
                conditional = model(
                    x,
                    model_t,
                    prompts,
                    valid,
                    obs_x0=context,
                    obs_mask=obs_mask,
                    task=task,
                    rf_mask=rf_mask,
                    text_condition=conditional_text,
                )
                if unconditional_text is None:
                    velocity = conditional
                else:
                    unconditional = model(
                        x,
                        model_t,
                        prompts,
                        valid,
                        obs_x0=context,
                        obs_mask=obs_mask,
                        task=task,
                        rf_mask=rf_mask,
                        text_condition=unconditional_text,
                    )
                    velocity = unconditional + cfg_scale * (conditional - unconditional)
            dt = times[step_index + 1] - times[step_index]
            x = torch.where(active_mask, x + dt * velocity, context)
        return x

    if model.temporal_mode == "full_sequence_rf":
        return integrate(loss_mask, z, None, seed)
    if model.temporal_mode != "masked_iterative_rf":
        raise ValueError(f"unknown temporal mode: {model.temporal_mode}")

    target_temporal = loss_mask.any(dim=1)
    valid_counts = target_temporal.sum(dim=1)
    if (valid_counts <= 0).any():
        raise RuntimeError("masked iterative sampling requires at least one target token per sample")
    rank_values = deterministic_sample_tensor(
        tuple(target_temporal.shape), sample_indices, seed + 40_000_019, z.device, torch.float32, normal=False
    ).masked_fill(~target_temporal, 2.0)
    ranks = rank_values.argsort(dim=1).argsort(dim=1)
    latents = torch.where(loss_mask, torch.zeros_like(z), z)
    for outer_index, schedule_t in enumerate(torch.linspace(0.0, 1.0, unmask_steps, device=z.device)):
        mask_ratio = math.cos(float(schedule_t) * math.pi * 0.5)
        num_masked = (valid_counts.float() * mask_ratio).round().long().clamp(min=1)
        temporal_mask = (ranks < num_masked[:, None]) & target_temporal
        rf_mask = temporal_mask[:, None, :].expand_as(loss_mask) & loss_mask
        sampled = integrate(rf_mask, latents, rf_mask, seed + (outer_index + 1) * 10_000_019)
        latents = torch.where(rf_mask, sampled, latents)
    return torch.where(loss_mask, latents, z)


@torch.no_grad()
def sample_human_first_cascade(
    model: MoLingoFullSequenceRF,
    process: Any,
    z: torch.Tensor,
    valid: torch.Tensor,
    human_captions: Sequence[str],
    camera_captions: Sequence[str],
    sample_indices: Sequence[int],
    seed: int,
    *,
    rf_steps: int,
    cfg_scale: float,
    unmask_steps: int,
) -> torch.Tensor:
    human = sample_stage2(
        model,
        process,
        z,
        valid,
        human_captions,
        camera_captions,
        TASK_HUMAN,
        sample_indices,
        seed,
        rf_steps=rf_steps,
        cfg_scale=cfg_scale,
        unmask_steps=unmask_steps,
    )
    camera_context = z.clone()
    camera_context[:, :HUM_DIM] = human[:, :HUM_DIM]
    camera = sample_stage2(
        model,
        process,
        camera_context,
        valid,
        human_captions,
        camera_captions,
        TASK_CAMERA,
        sample_indices,
        seed + 20_000_033,
        rf_steps=rf_steps,
        cfg_scale=cfg_scale,
        unmask_steps=unmask_steps,
    )
    output = human.clone()
    output[:, HUM_DIM:] = camera[:, HUM_DIM:]
    return output


@torch.no_grad()
def evaluate(
    model: MoLingoFullSequenceRF,
    process: Any,
    loader: DataLoader,
    device: torch.device,
    max_batches: int,
    seed: int,
    temporal_mode: str,
    task_scope: str,
) -> dict[str, float]:
    was_training = model.training
    model.eval()
    rows: list[dict[str, float]] = []
    with torch.random.fork_rng(devices=[device.index]):
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        for batch_index, batch in enumerate(loader):
            if batch_index >= max_batches:
                break
            z = batch["z"].to(device)
            valid = batch["valid"].to(device)
            metrics: dict[str, float] = {}
            active_tasks = active_task_pairs(task_scope)
            for task_id, name in active_tasks:
                task = torch.full((z.shape[0],), task_id, device=device, dtype=torch.long)
                prompts = task_prompts(batch["human_caption"], batch["camera_caption"], task)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, task_metrics = diffusion_loss(
                        model, process, z, valid, prompts, task, temporal_mode=temporal_mode
                    )
                metrics.update({f"{name}_{key}": value for key, value in task_metrics.items()})
            rows.append(metrics)
    if was_training:
        model.train()
    if not rows:
        raise RuntimeError("evaluation loader produced no batches")
    result = {key: sum(row[key] for row in rows) / len(rows) for key in rows[0]}
    active_names = [name for _, name in active_task_pairs(task_scope)]
    result["loss_mean"] = sum(result[f"{name}_loss"] for name in active_names) / len(active_names)
    return result


def trainable_state_dict(model: nn.Module) -> dict[str, torch.Tensor]:
    return {
        key: value.detach().cpu()
        for key, value in model.state_dict().items()
        if not key.startswith("t5_model.")
    }


def save_checkpoint(
    path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    step: int,
    meta: dict[str, Any],
) -> None:
    torch.save(
        {
            "model": trainable_state_dict(model),
            "optimizer": optimizer.state_dict(),
            "step": step,
            "meta": meta,
        },
        path,
    )


def write_record(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def write_scalars(writer: SummaryWriter, split: str, metrics: dict[str, Any], step: int) -> None:
    for name, value in metrics.items():
        if isinstance(value, (int, float)):
            writer.add_scalar(f"{split}/{name}", value, step)


def restore_exposure(log_path: Path, device: torch.device) -> torch.Tensor:
    exposure = torch.zeros(3, dtype=torch.long, device=device)
    if not log_path.is_file():
        return exposure
    for line in log_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("split") != "train":
            continue
        for index, name in enumerate(TASK_NAMES):
            exposure[index] = int(record.get(f"task_exposures_{name}", exposure[index]))
    return exposure


def backfill_tensorboard(log_path: Path, writer: SummaryWriter) -> None:
    if not log_path.is_file():
        return
    for line in log_path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        split = record.get("split")
        step = record.get("step")
        if split in {"train", "eval", "test"} and isinstance(step, int):
            write_scalars(writer, split, record, step)


def make_model(args: argparse.Namespace, device: torch.device) -> MoLingoFullSequenceRF:
    model = MoLingoFullSequenceRF(
        args.t5_path,
        args.transformer_width,
        args.transformer_depth,
        args.transformer_heads,
        args.adapter_layers,
        args.flow_width,
        args.flow_depth,
        args.dropout,
        args.text_drop_prob,
        args.t5_max_length,
        args.temporal_mode,
    ).to(device)
    return model


def build_contract(
    args: argparse.Namespace,
    train_ds: CaptionedLatentCache,
    heldout_ds: CaptionedLatentCache,
    stats: dict[str, Any],
) -> dict[str, Any]:
    train_cache = args.cache_dir / "train.pt"
    eval_cache = args.cache_dir / "val.pt"
    checkpoint = ROOT / str(train_ds.meta["tokenizer_checkpoint"])
    checkpoint_sha = base.sha256_file(checkpoint)
    train_ids = train_ds.sample_id
    eval_ids = heldout_ds.sample_id
    eval_count = min(args.eval_samples, len(eval_ids))
    test_count = min(args.test_samples, len(eval_ids) - eval_count)
    return {
        "schema_version": 1,
        "stage": "stage2",
        "version": "v7.45" if args.task_scope == "human_only" else "v7.41" if args.temporal_mode == "masked_iterative_rf" else "v7.40",
        "run_id": args.run_id,
        "tasks": [name for _, name in active_task_pairs(args.task_scope)],
        "generation_modes": (
            ["human_text_only_offline_masked_iteration"]
            if args.task_scope == "human_only"
            else ["human_text_only", "camera_from_human", "joint_parallel", "joint_human_first_cascade"]
        ),
        "data": {
            "train_manifest": str(train_ds.meta["human_manifest"]),
            "train_split": "train",
            "train_samples": len(train_ds),
            "train_sample_ids_sha256": base.sha256_sample_ids(train_ids),
            "eval_manifest": str(heldout_ds.meta["human_manifest"]),
            "eval_split": "test",
            "eval_samples": len(heldout_ds),
            "eval_sample_ids_sha256": base.sha256_sample_ids(eval_ids),
            "train_raw_caption_cache": str(train_ds.caption_cache_path),
            "train_raw_caption_cache_sha256": base.sha256_file(train_ds.caption_cache_path),
            "eval_raw_caption_cache": str(heldout_ds.caption_cache_path),
            "eval_raw_caption_cache_sha256": base.sha256_file(heldout_ds.caption_cache_path),
        },
        "parent_stage1": {
            "version": "v7.14",
            "run_id": "joint_ae_official_4090_gpu0_r2",
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": checkpoint_sha,
            "owning_decoder": str(checkpoint),
            "owning_decoder_sha256": checkpoint_sha,
        },
        "cache": {
            "train_path": str(train_cache),
            "train_sha256": str(stats["source_cache_sha256"]),
            "eval_path": str(eval_cache),
            "eval_sha256": base.sha256_file(eval_cache),
            "tokenizer_checkpoint_sha256": checkpoint_sha,
            "z_norm_source_train_sha256": str(stats["source_cache_sha256"]),
        },
        "train": {"seed": args.seed, "batch_size": args.batch_size},
        "eval": {
            "seed": args.seed,
            "batch_size": args.eval_batch_size,
            "decode_batch_size": args.eval_batch_size,
            "sample_count": len(heldout_ds),
            "sampler": {
                "name": "rf_euler_velocity",
                "steps": 50,
                "eta": 0.0,
                "cfg_scale": 4.0,
            },
        },
        "tracking": {
            "log_every": args.log_every,
            "eval_every": args.eval_every,
            "test_every": args.test_every,
            "eval_samples": eval_count,
            "eval_sample_ids_sha256": base.sha256_sample_ids(eval_ids[:eval_count]),
            "test_samples": test_count,
            "test_sample_ids_sha256": base.sha256_sample_ids(eval_ids[eval_count : eval_count + test_count]),
            "fixed_noise_seed_eval": args.seed + 1000,
            "fixed_noise_seed_test": args.seed + 2000,
            "note": "training diagnostics only; formal decoded evaluation remains the full declared eval boundary",
        },
        "adaptation": {
            "name": f"MoLingo-derived {args.temporal_mode} {args.task_scope}",
            "official_molingo_commit": "86e21b24784e36c3bb6d43d0d5c1de4de6224768",
            "retained": ["frozen T5-large multi-token text", "cross-attention", "token-wise AdaLN RF head"],
            "temporal_mode": args.temporal_mode,
            "task_scope": args.task_scope,
            "stage1_adaptation": "frozen v7.14 non-causal joint tokenizer; offline latent generation makes no streaming claim",
            "temporal_conditioning": (
                "random cosine-ratio masks; bidirectional clean unmasked latent context"
                if args.temporal_mode == "masked_iterative_rf"
                else "all target temporal tokens share the sampled RF-noise level"
            ),
            "internal_task_id_order": list(TASK_NAMES),
            "active_task_ids": [task_id for task_id, _ in active_task_pairs(args.task_scope)],
            "tokenizer_is_causal": False,
        },
    }


def train(args: argparse.Namespace) -> None:
    base.set_seed(args.seed)
    torch.set_float32_matmul_precision("high")
    device = torch.device(args.device)
    stats = base.load_latent_znorm_stats(args.znorm_stats_path)
    paths = run_paths("stage2", args.run_id, args.runs_root)
    if not paths["root"].exists():
        init_run(
            "stage2",
            args.run_id,
            runs_root=args.runs_root,
            parent_stage1_run="joint_ae_official_4090_gpu0_r2",
            description=f"MoLingo-derived {args.temporal_mode} {args.task_scope}",
        )
    train_ds = CaptionedLatentCache(
        args.cache_dir / "train.pt",
        stats,
        args.data_root,
        paths["cache"] / "train_raw_captions.pt",
        args.caption_workers,
    )
    heldout_ds = CaptionedLatentCache(
        args.cache_dir / "val.pt",
        stats,
        args.data_root,
        paths["cache"] / "val_raw_captions.pt",
        args.caption_workers,
    )
    if set(train_ds.sample_id).intersection(heldout_ds.sample_id):
        raise RuntimeError("train/eval sample IDs overlap")
    if str(stats["source_cache_sha256"]) != base.sha256_file(args.cache_dir / "train.pt"):
        raise RuntimeError("z-normalization source hash does not match train cache")

    contract = build_contract(args, train_ds, heldout_ds, stats)
    paths["contract"].write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    update_manifest("stage2", args.run_id, runs_root=args.runs_root, status="training")
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    manifest.update({"gpu": device.index, "host": socket.gethostname(), "train_pid": os.getpid()})
    paths["manifest"].write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        drop_last=True,
        pin_memory=True,
    )
    eval_count = min(args.eval_samples, len(heldout_ds))
    test_count = min(args.test_samples, len(heldout_ds) - eval_count)
    if eval_count <= 0 or test_count <= 0:
        raise RuntimeError(f"heldout cache cannot provide disjoint eval/test subsets: {len(heldout_ds)}")
    eval_loader = DataLoader(
        Subset(heldout_ds, range(eval_count)),
        batch_size=args.eval_batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True,
    )
    test_loader = DataLoader(
        Subset(heldout_ds, range(eval_count, eval_count + test_count)),
        batch_size=args.eval_batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=True,
    )
    model = make_model(args, device)
    process = build_stage2_process("rectified_flow", 1000, "cosine", device)
    parameters = [parameter for parameter in model.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=args.lr, weight_decay=args.weight_decay, betas=(0.9, 0.95))
    task_probs = torch.tensor(
        [0.0, 1.0, 0.0] if args.task_scope == "human_only" else args.task_probs,
        dtype=torch.float32,
        device=device,
    )
    task_probs /= task_probs.sum()
    meta = {
        "args": {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
        "model": contract["adaptation"],
        "stage2_process": process.metadata(),
        "latent_order": train_ds.meta["latent_order"],
        "human_slice": [0, HUM_DIM],
        "camera_slice": [HUM_DIM, LATENT_DIM],
        "task_routing": "human_first",
        "task_probs_normalized": task_probs.detach().cpu().tolist(),
        "loss": "RF velocity MSE over valid target branch only; observed branch excluded",
        "tracking": contract["tracking"],
        "trainable_params": sum(parameter.numel() for parameter in parameters),
        "frozen_t5_params": sum(parameter.numel() for parameter in model.t5_model.parameters()),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    paths["train"].mkdir(parents=True, exist_ok=True)
    meta_path = paths["train"] / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    log_path = paths["train"] / "train_log.jsonl"
    writer = SummaryWriter(str(paths["train"] / "tensorboard")) if SummaryWriter is not None else None
    if writer is not None:
        backfill_tensorboard(log_path, writer)

    step = 0
    if args.resume:
        checkpoint = torch.load(args.resume, map_location="cpu")
        missing, unexpected = model.load_state_dict(checkpoint["model"], strict=False)
        allowed_missing = [name for name in missing if name.startswith("t5_model.")]
        if len(allowed_missing) != len(missing) or unexpected:
            raise RuntimeError(f"resume state mismatch: missing={missing}, unexpected={unexpected}")
        optimizer.load_state_dict(checkpoint["optimizer"])
        step = int(checkpoint["step"])

    model.train()
    exposure = restore_exposure(log_path, device)
    while step < args.steps:
        for batch in train_loader:
            step += 1
            if args.warmup_steps > 0:
                lr_scale = min(1.0, step / args.warmup_steps)
                for group in optimizer.param_groups:
                    group["lr"] = args.lr * lr_scale
            z = batch["z"].to(device, non_blocking=True)
            valid = batch["valid"].to(device, non_blocking=True)
            task = torch.multinomial(task_probs, z.shape[0], replacement=True)
            exposure += torch.bincount(task, minlength=3)
            prompts = task_prompts(batch["human_caption"], batch["camera_caption"], task)
            optimizer.zero_grad(set_to_none=True)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                loss, metrics = diffusion_loss(
                    model, process, z, valid, prompts, task, temporal_mode=args.temporal_mode
                )
            loss.backward()
            grad_norm = float(nn.utils.clip_grad_norm_(parameters, args.grad_clip).detach().cpu())
            optimizer.step()

            if step == 1 or step % args.log_every == 0:
                train_record = {
                    "step": step,
                    "split": "train",
                    **metrics,
                    "grad_norm": grad_norm,
                    "lr": optimizer.param_groups[0]["lr"],
                    **{f"task_exposures_{name}": int(exposure[index]) for index, name in enumerate(TASK_NAMES)},
                    "task_exposures_total": int(exposure.sum()),
                }
                write_record(log_path, train_record)
                if writer is not None:
                    write_scalars(writer, "train", train_record, step)
            if step == 1 or step % args.eval_every == 0:
                eval_metrics = evaluate(
                    model, process, eval_loader, device, args.eval_batches, args.seed + 1000,
                    args.temporal_mode, args.task_scope,
                )
                best_eval = base.best_eval_from_log(log_path, "loss_mean")
                write_record(log_path, {"step": step, "split": "eval", **eval_metrics})
                if writer is not None:
                    write_scalars(writer, "eval", eval_metrics, step)
                meta["task_exposure_counts"] = {
                    name: int(exposure[index]) for index, name in enumerate(TASK_NAMES)
                }
                save_checkpoint(paths["train"] / "last.pt", model, optimizer, step, meta)
                if float(eval_metrics["loss_mean"]) < best_eval:
                    save_checkpoint(paths["train"] / "best_eval.pt", model, optimizer, step, meta)
            if step == 1 or step % args.test_every == 0:
                test_metrics = evaluate(
                    model, process, test_loader, device, args.test_batches, args.seed + 2000,
                    args.temporal_mode, args.task_scope,
                )
                write_record(log_path, {"step": step, "split": "test", **test_metrics})
                if writer is not None:
                    write_scalars(writer, "test", test_metrics, step)
            if step in args.snapshot_steps:
                save_checkpoint(paths["train"] / f"step_{step}.pt", model, optimizer, step, meta)
            if step >= args.steps:
                break
            if writer is not None:
                writer.flush()

    save_checkpoint(paths["train"] / "last.pt", model, optimizer, step, meta)
    meta["completed_at"] = datetime.now(timezone.utc).isoformat()
    meta["task_exposure_counts"] = {
        name: int(exposure[index]) for index, name in enumerate(TASK_NAMES)
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if writer is not None:
        writer.close()
    update_manifest(
        "stage2",
        args.run_id,
        runs_root=args.runs_root,
        status="trained",
        artifacts={
            "checkpoint": str((paths["train"] / "last.pt").relative_to(args.runs_root)),
            "best_eval_checkpoint": str((paths["train"] / "best_eval.pt").relative_to(args.runs_root)),
            "train_log": str((paths["train"] / "train_log.jsonl").relative_to(args.runs_root)),
            "tensorboard": str((paths["train"] / "tensorboard").relative_to(args.runs_root)),
        },
    )


def evaluate_checkpoint(args: argparse.Namespace) -> None:
    if args.resume is None:
        raise ValueError("evaluate mode requires --resume")
    base.set_seed(args.seed)
    device = torch.device(args.device)
    stats = base.load_latent_znorm_stats(args.znorm_stats_path)
    paths = run_paths("stage2", args.run_id, args.runs_root)
    heldout_ds = CaptionedLatentCache(
        args.cache_dir / "val.pt",
        stats,
        args.data_root,
        paths["cache"] / "val_raw_captions.pt",
        args.caption_workers,
    )
    eval_count = min(args.eval_samples, len(heldout_ds))
    test_count = min(args.test_samples, len(heldout_ds) - eval_count)
    if eval_count <= 0 or test_count <= 0:
        raise RuntimeError(f"heldout cache cannot provide disjoint eval/test subsets: {len(heldout_ds)}")

    def loader(start: int, count: int) -> DataLoader:
        return DataLoader(
            Subset(heldout_ds, range(start, start + count)),
            batch_size=args.eval_batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=True,
        )

    model = make_model(args, device)
    checkpoint = torch.load(args.resume, map_location="cpu")
    missing, unexpected = model.load_state_dict(checkpoint["model"], strict=False)
    if [name for name in missing if not name.startswith("t5_model.")] or unexpected:
        raise RuntimeError(f"checkpoint state mismatch: missing={missing}, unexpected={unexpected}")
    process = build_stage2_process("rectified_flow", 1000, "cosine", device)
    eval_metrics = evaluate(
        model, process, loader(0, eval_count), device, args.eval_batches, args.seed + 1000,
        args.temporal_mode, args.task_scope,
    )
    test_metrics = evaluate(
        model,
        process,
        loader(eval_count, test_count),
        device,
        args.test_batches,
        args.seed + 2000,
        args.temporal_mode,
        args.task_scope,
    )
    step = int(checkpoint["step"])
    payload = {
        "run_id": args.run_id,
        "step": step,
        "checkpoint": str(args.resume),
        "checkpoint_sha256": base.sha256_file(args.resume),
        "eval_samples": eval_count,
        "eval_sample_ids_sha256": base.sha256_sample_ids(heldout_ds.sample_id[:eval_count]),
        "test_samples": test_count,
        "test_sample_ids_sha256": base.sha256_sample_ids(
            heldout_ds.sample_id[eval_count : eval_count + test_count]
        ),
        "fixed_noise_seed_eval": args.seed + 1000,
        "fixed_noise_seed_test": args.seed + 2000,
        "eval": eval_metrics,
        "test": test_metrics,
        "cuda_device": torch.cuda.get_device_name(device),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    paths["eval"].mkdir(parents=True, exist_ok=True)
    output_path = paths["eval"] / f"training_diagnostics_step_{step}.json"
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), **payload}, indent=2, sort_keys=True))


def check(args: argparse.Namespace) -> None:
    base.set_seed(args.seed)
    device = torch.device(args.device)
    torch.cuda.set_device(device)
    torch.cuda.reset_peak_memory_stats(device)
    raw = torch.load(args.cache_dir / "val.pt", map_location="cpu")
    assert_default_cache_meta(raw["meta"])
    stats = base.load_latent_znorm_stats(args.znorm_stats_path)
    count = min(args.check_batch_size, int(raw["z"].shape[0]))
    valid = raw["valid_mask"][:count].bool().to(device)
    z = base.normalize_latent(raw["z"][:count].float().to(device), valid, stats)
    sample_ids = [str(value) for value in raw["sample_id"][:count]]
    human = [(args.data_root / "caption_char" / f"{sample_id}.txt").read_text().strip() for sample_id in sample_ids]
    camera = [(args.data_root / "caption_cam" / f"{sample_id}.txt").read_text().strip() for sample_id in sample_ids]
    task = (
        torch.full((count,), TASK_HUMAN, device=device, dtype=torch.long)
        if args.task_scope == "human_only"
        else torch.arange(count, device=device, dtype=torch.long) % 3
    )
    prompts = task_prompts(human, camera, task)
    model = make_model(args, device)
    process = build_stage2_process("rectified_flow", 1000, "cosine", device)
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        loss, metrics = diffusion_loss(
            model, process, z, valid, prompts, task, temporal_mode=args.temporal_mode
        )
    loss.backward()
    payload = {
        "loss": float(loss.detach().cpu()),
        "metrics": metrics,
        "output_finite": bool(torch.isfinite(loss)),
        "trainable_params": sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad),
        "frozen_t5_params": sum(parameter.numel() for parameter in model.t5_model.parameters()),
        "cache_tokenizer_is_causal": raw["meta"]["tokenizer_is_causal"],
        "peak_cuda_memory_gib": torch.cuda.max_memory_allocated(device) / (1024**3),
        "adaptation": args.temporal_mode,
        "task_scope": args.task_scope,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["check", "evaluate", "train"])
    parser.add_argument("--run-id", default="v7_40_molingo_fullseq_rf_seed17_4090g1_20260715")
    parser.add_argument("--runs-root", type=Path, default=ROOT / "runs")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=ROOT / "runs/legacy/train/stage2/v7_17_corrected_cache_20260712/joint_ae_noncausal",
    )
    parser.add_argument(
        "--znorm-stats-path",
        type=Path,
        default=ROOT / "runs/stage2/v7_39_condmdi_rf_a30_seed17_4090g0_20260715/cache/train_latent_fullcov.pt",
    )
    parser.add_argument("--data-root", type=Path, default=Path("/data/public/ripemangobox/Motion/datasets/pulpmotion-data"))
    parser.add_argument("--t5-path", type=Path, default=Path("/data/public/ripemangobox/Motion/Text-encoder/t5-large"))
    parser.add_argument("--device", default="cuda:1")
    parser.add_argument(
        "--temporal-mode",
        choices=["full_sequence_rf", "masked_iterative_rf"],
        default="full_sequence_rf",
    )
    parser.add_argument("--task-scope", choices=["unified3", "human_only"], default="unified3")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--steps", type=int, default=30000)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--check-batch-size", type=int, default=64)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--caption-workers", type=int, default=64)
    parser.add_argument("--eval-samples", type=int, default=256)
    parser.add_argument("--eval-batches", type=int, default=4)
    parser.add_argument("--eval-every", type=int, default=1000)
    parser.add_argument("--test-samples", type=int, default=256)
    parser.add_argument("--test-batches", type=int, default=4)
    parser.add_argument("--test-every", type=int, default=3000)
    parser.add_argument("--log-every", type=int, default=100)
    parser.add_argument("--snapshot-steps", type=int, nargs="*", default=[30000])
    parser.add_argument("--task-probs", type=float, nargs=3, default=[1.0, 1.0, 1.0])
    parser.add_argument("--transformer-width", type=int, default=768)
    parser.add_argument("--transformer-depth", type=int, default=6)
    parser.add_argument("--transformer-heads", type=int, default=12)
    parser.add_argument("--adapter-layers", type=int, default=1)
    parser.add_argument("--flow-width", type=int, default=1024)
    parser.add_argument("--flow-depth", type=int, default=4)
    parser.add_argument("--dropout", type=float, default=0.1)
    parser.add_argument("--text-drop-prob", type=float, default=0.1)
    parser.add_argument("--t5-max-length", type=int, default=64)
    parser.add_argument("--lr", type=float, default=5.0e-5)
    parser.add_argument("--warmup-steps", type=int, default=2000)
    parser.add_argument("--weight-decay", type=float, default=0.02)
    parser.add_argument("--grad-clip", type=float, default=3.0)
    parser.add_argument("--resume", type=Path)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.transformer_width % args.transformer_heads:
        raise ValueError("transformer width must be divisible by head count")
    if not args.t5_path.is_dir():
        raise FileNotFoundError(args.t5_path)
    if args.mode == "check":
        check(args)
    elif args.mode == "evaluate":
        evaluate_checkpoint(args)
    else:
        train(args)


if __name__ == "__main__":
    main()
