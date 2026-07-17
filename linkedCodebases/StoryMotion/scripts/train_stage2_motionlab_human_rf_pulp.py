#!/usr/bin/env python3
"""Train a representation-matched MotionLab text-to-human baseline on v7.14 latents.

This is not an official MotionLab result. It keeps MotionLab's public MFT
denoiser and flow-matching objective, but replaces native HumanML3D motion with
the frozen non-causal StoryMotion v7.14 human latent. The cached 1024-D text is
``camera512 + human512``; this trainer hard-slices the human half so human
completion cannot consume camera text.
"""
from __future__ import annotations

import argparse
import json
import random
import socket
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterator

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import train_stage2_condmdi_pulp as base
from storymotion.experiment_invariants import assert_default_cache_meta
from scripts.storymotion_run_layout import run_paths


HUMAN_DIM = 128
LATENT_FRAMES = 75
HUMAN_TEXT_START = 512
HUMAN_TEXT_END = 1024
EXPECTED_MOTIONLAB_COMMIT = "8b2f7b35ae57bb0a7ef5985e6479148f5adcb11d"


def select_human_only(z: torch.Tensor, text: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Return the only two tensors the human specialist may consume."""
    if z.ndim != 3 or z.shape[1:] != (base.LATENT_DIM, LATENT_FRAMES):
        raise ValueError(f"expected full latent [N,{base.LATENT_DIM},{LATENT_FRAMES}], got {tuple(z.shape)}")
    if text.ndim != 2 or text.shape[1] != HUMAN_TEXT_END:
        raise ValueError(f"expected concatenated camera512+human512 text, got {tuple(text.shape)}")
    return (
        z[:, :HUMAN_DIM].contiguous(),
        text[:, HUMAN_TEXT_START:HUMAN_TEXT_END].contiguous(),
    )


class HumanLatentCache(torch.utils.data.Dataset):
    def __init__(self, path: Path, stats: dict[str, Any]) -> None:
        payload = torch.load(path, map_location="cpu")
        assert_default_cache_meta(payload["meta"])
        z = payload["z"].float()
        valid = payload["valid_mask"].bool()
        text = payload["text"].float()
        if valid.shape != (z.shape[0], LATENT_FRAMES):
            raise ValueError(f"unexpected valid-mask shape {tuple(valid.shape)}")
        normalized = base.normalize_latent(z, valid, stats)
        self.human, self.human_text = select_human_only(normalized, text)
        self.valid = valid
        self.sample_id = [str(value) for value in payload["sample_id"]]
        self.meta = dict(payload["meta"])

    def __len__(self) -> int:
        return len(self.sample_id)

    def __getitem__(self, index: int) -> dict[str, Any]:
        return {
            "human": self.human[index],
            "human_text": self.human_text[index],
            "valid": self.valid[index],
            "sample_id": self.sample_id[index],
        }


def git_commit(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def git_tracked_status(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain", "--untracked-files=no"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def verify_motionlab_source(
    motionlab_root: Path,
    contract: dict[str, Any],
) -> dict[str, str]:
    commit = git_commit(motionlab_root)
    expected_commit = contract["baseline"]["source_commit"]
    if commit != expected_commit:
        raise RuntimeError(f"MotionLab commit mismatch: {commit} != {expected_commit}")
    tracked_status = git_tracked_status(motionlab_root)
    if tracked_status:
        raise RuntimeError(f"MotionLab tracked worktree is dirty:\n{tracked_status}")
    config_path = motionlab_root / contract["baseline"]["source_config"]
    config_sha = base.sha256_file(config_path)
    expected_sha = contract["baseline"]["source_config_sha256"]
    if config_sha != expected_sha:
        raise RuntimeError(f"MotionLab source config hash mismatch: {config_sha} != {expected_sha}")
    return {
        "commit": commit,
        "source_config": str(config_path.resolve()),
        "source_config_sha256": config_sha,
        "tracked_worktree": "clean",
    }


def build_model(motionlab_root: Path, device: torch.device) -> nn.Module:
    commit = git_commit(motionlab_root)
    if commit != EXPECTED_MOTIONLAB_COMMIT:
        raise RuntimeError(f"MotionLab commit mismatch: {commit} != {EXPECTED_MOTIONLAB_COMMIT}")
    if str(motionlab_root) not in sys.path:
        sys.path.insert(0, str(motionlab_root))
    from rfmotion.models.architectures.rfmotion_denoiser_4path import RFMotionDenoiser

    model = RFMotionDenoiser(
        ablation=SimpleNamespace(VAE=False),
        nfeats=HUMAN_DIM,
        token_dim=512,
        num_layers=9,
        num_heads=8,
        text_encoded_dim=HUMAN_TEXT_END - HUMAN_TEXT_START,
    )
    model.is_causal = False
    assert model.is_causal is False
    return model.to(device)


def model_velocity(
    model: nn.Module,
    noisy: torch.Tensor,
    timesteps: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    text_drop_prob: float,
) -> torch.Tensor:
    batch_size = noisy.shape[0]
    if text_drop_prob:
        keep = (torch.rand(batch_size, 1, device=text.device) >= text_drop_prob).to(text.dtype)
        text = text * keep
    lengths = valid.sum(dim=1).to(torch.long).tolist()
    text_lengths = [1] * batch_size
    return model(
        instructions=None,
        timestep=timesteps,
        hidden_states=noisy,
        target_lengths=lengths,
        target_lengths_z=lengths,
        text=[text[:, None, :]],
        text_lengths=text_lengths,
        return_dict=False,
    )[0]


def flow_loss(
    model: nn.Module,
    scheduler: Any,
    human: torch.Tensor,
    text: torch.Tensor,
    valid: torch.Tensor,
    text_drop_prob: float,
) -> torch.Tensor:
    clean = human.transpose(1, 2).contiguous()
    noise = torch.randn_like(clean)
    timesteps = torch.randint(0, 1001, (clean.shape[0],), device=clean.device, dtype=torch.long)
    noisy = scheduler.scale_noise(sample=clean, noise=noise, timestep=timesteps)
    prediction = model_velocity(model, noisy, timesteps, text, valid, text_drop_prob)
    target = noise - clean
    mask = valid[:, :, None].to(prediction.dtype)
    # Official MotionLab masks prediction/target first, then applies an
    # unreduced-shape MSE mean. Padding therefore remains in the denominator.
    return (((prediction - target) * mask).square()).mean()


def endless(loader: DataLoader) -> Iterator[dict[str, Any]]:
    while True:
        yield from loader


class DeterministicEpochBatchSampler:
    """Index epoch permutations by global micro-step for exact restart."""

    def __init__(
        self,
        dataset_size: int,
        batch_size: int,
        seed: int,
        start_micro_step: int,
        stop_micro_step: int,
    ) -> None:
        self.dataset_size = int(dataset_size)
        self.batch_size = int(batch_size)
        self.seed = int(seed)
        self.start_micro_step = int(start_micro_step)
        self.stop_micro_step = int(stop_micro_step)
        self.batches_per_epoch = self.dataset_size // self.batch_size
        if self.batches_per_epoch <= 0:
            raise ValueError("dataset must contain at least one full micro batch")
        if not 0 <= self.start_micro_step <= self.stop_micro_step:
            raise ValueError("invalid micro-step range")

    def __len__(self) -> int:
        return self.stop_micro_step - self.start_micro_step

    def __iter__(self) -> Iterator[list[int]]:
        current = self.start_micro_step
        while current < self.stop_micro_step:
            epoch = current // self.batches_per_epoch
            batch_in_epoch = current % self.batches_per_epoch
            generator = torch.Generator(device="cpu")
            generator.manual_seed(self.seed + epoch)
            permutation = torch.randperm(self.dataset_size, generator=generator)
            while batch_in_epoch < self.batches_per_epoch and current < self.stop_micro_step:
                start = batch_in_epoch * self.batch_size
                yield permutation[start : start + self.batch_size].tolist()
                current += 1
                batch_in_epoch += 1


def capture_rng_state() -> dict[str, Any]:
    return {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else [],
    }


def restore_rng_state(state: dict[str, Any]) -> None:
    random.setstate(state["python"])
    np.random.set_state(state["numpy"])
    torch.set_rng_state(state["torch_cpu"])
    if torch.cuda.is_available():
        torch.cuda.set_rng_state_all(state["torch_cuda"])


def reconcile_train_log(log_path: Path, checkpoint_step: int) -> dict[str, Any]:
    """Atomically discard records newer than the resumable checkpoint."""
    if not log_path.exists():
        return {"records_before": 0, "records_after": 0, "truncated": False}
    lines = log_path.read_text(encoding="utf-8").splitlines()
    records: list[tuple[int, str]] = []
    previous = 0
    for line_number, line in enumerate(lines, 1):
        record = json.loads(line)
        step = int(record["step"])
        if step <= previous:
            raise RuntimeError(f"non-increasing train log at line {line_number}")
        previous = step
        records.append((step, line))
    kept = [line for step, line in records if step <= checkpoint_step]
    truncated = len(kept) != len(records)
    if truncated:
        temporary = log_path.with_suffix(log_path.suffix + ".tmp")
        temporary.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
        temporary.replace(log_path)
    return {
        "records_before": len(records),
        "records_after": len(kept),
        "truncated": truncated,
        "checkpoint_step": checkpoint_step,
    }


def _story_path(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def verify_mutable_boundaries(
    storymotion_root: Path,
    contract: dict[str, Any],
) -> dict[str, Any]:
    """Hard-fail every mutable representation/data boundary before GPU work."""
    parent = contract["parent_stage1"]
    cache = contract["cache"]
    data = contract["data"]
    if parent["checkpoint_sha256"] != cache["tokenizer_checkpoint_sha256"]:
        raise RuntimeError("Stage1/tokenizer checkpoint SHA mismatch in contract")
    checked: dict[str, Any] = {}
    for label, path_value, expected in (
        ("stage1_checkpoint", parent["checkpoint"], parent["checkpoint_sha256"]),
        ("owning_decoder", parent["owning_decoder"], parent["owning_decoder_sha256"]),
        ("train_cache", cache["train_path"], cache["train_sha256"]),
        ("eval_cache", cache["eval_path"], cache["eval_sha256"]),
        ("z_norm_stats", cache["z_norm_stats_path"], cache["z_norm_stats_sha256"]),
    ):
        path = _story_path(storymotion_root, path_value)
        actual = base.sha256_file(path)
        if actual != expected:
            raise RuntimeError(f"{label} hash mismatch: {actual} != {expected}")
        checked[label] = {"path": str(path.resolve()), "sha256": actual}
    for split in ("train", "eval"):
        path = _story_path(storymotion_root, cache[f"{split}_path"])
        payload = torch.load(path, map_location="cpu")
        assert_default_cache_meta(payload["meta"])
        meta = payload["meta"]
        if meta.get("tokenizer_checkpoint") != parent["checkpoint"]:
            raise RuntimeError(f"{split} cache tokenizer checkpoint path mismatch")
        expected_samples = data[f"{split}_samples"]
        sample_ids = [str(value) for value in payload["sample_id"]]
        if len(sample_ids) != expected_samples:
            raise RuntimeError(f"{split} cache sample count mismatch")
        actual_ids = base.sha256_sample_ids(sample_ids)
        if actual_ids != data[f"{split}_sample_ids_sha256"]:
            raise RuntimeError(f"{split} cache sample identity mismatch")
        checked[f"{split}_cache"].update(
            {"samples": len(sample_ids), "sample_ids_sha256": actual_ids}
        )
        del payload
    stats = base.load_latent_znorm_stats(
        _story_path(storymotion_root, cache["z_norm_stats_path"])
    )
    if stats.get("source_cache_sha256") != cache["z_norm_source_train_sha256"]:
        raise RuntimeError("z-normalization stats were not fit from contracted train cache")
    if cache["z_norm_source_train_sha256"] != cache["train_sha256"]:
        raise RuntimeError("z-normalization source SHA differs from train cache SHA")
    checked["z_norm_stats"]["source_cache_sha256"] = stats["source_cache_sha256"]
    return checked


def load_contract(path: Path) -> dict[str, Any]:
    contract = json.loads(path.read_text(encoding="utf-8"))
    if contract["baseline"]["source_commit"] != EXPECTED_MOTIONLAB_COMMIT:
        raise ValueError("contract MotionLab commit does not match trainer")
    if contract["implementation"]["is_causal"] is not False:
        raise ValueError("contract must assert non-causal implementation")
    if contract["parent_stage1"]["is_causal"] is not False:
        raise ValueError("parent Stage1 must assert is_causal=false")
    if contract["train"]["tokenizer_is_causal"] is not False:
        raise ValueError("training contract must assert tokenizer_is_causal=false")
    if contract["data"]["human_text_input_slice"] != [HUMAN_TEXT_START, HUMAN_TEXT_END]:
        raise ValueError("contract human text slice does not match trainer")
    if contract["tasks"] != ["human"] or contract["generation_modes"] != ["human_text_only"]:
        raise ValueError("this trainer accepts only the human-text specialist contract")
    return contract


def checkpoint_payload(
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    step: int,
    micro_steps_consumed: int,
    contract: dict[str, Any],
) -> dict[str, Any]:
    return {
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "step": step,
        "micro_steps_consumed": micro_steps_consumed,
        "rng_state": capture_rng_state(),
        "contract": contract,
        "is_causal": False,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def run_check(args: argparse.Namespace, contract: dict[str, Any]) -> None:
    base.set_seed(contract["train"]["seed"])
    boundary_audit = verify_mutable_boundaries(args.storymotion_root, contract)
    boundary_audit["motionlab_source"] = verify_motionlab_source(
        args.motionlab_root, contract
    )
    device = torch.device(args.device)
    torch.cuda.set_device(device)
    torch.cuda.reset_peak_memory_stats(device)
    stats = base.load_latent_znorm_stats(args.storymotion_root / contract["cache"]["z_norm_stats_path"])
    dataset = HumanLatentCache(args.storymotion_root / contract["cache"]["eval_path"], stats)
    check_batch_size = args.check_batch_size or contract["train"]["micro_batch_size"]
    accumulation = int(contract["train"]["gradient_accumulation_steps"])
    batch_sampler = DeterministicEpochBatchSampler(
        len(dataset), check_batch_size, contract["train"]["seed"], 0, accumulation
    )
    loader = DataLoader(dataset, batch_sampler=batch_sampler, num_workers=0)
    model = build_model(args.motionlab_root, device)
    from rfmotion.models.operator.scheduling_flow_match_euler_discrete import FlowMatchEulerDiscreteScheduler

    scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=contract["train"]["lr"],
        betas=tuple(contract["train"]["optimizer_betas"]),
        weight_decay=contract["train"]["weight_decay"],
    )
    optimizer.zero_grad(set_to_none=True)
    started = time.monotonic()
    loss_sum = 0.0
    for batch in loader:
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            loss = flow_loss(
                model,
                scheduler,
                batch["human"].to(device),
                batch["human_text"].to(device),
                batch["valid"].to(device),
                contract["train"]["text_drop_prob"],
            )
        (loss / accumulation).backward()
        loss_sum += float(loss.detach().cpu())
    grad_norm = float(
        nn.utils.clip_grad_norm_(model.parameters(), contract["train"]["grad_clip"])
        .detach()
        .cpu()
    )
    optimizer.step()
    elapsed = time.monotonic() - started
    print(
        json.dumps(
            {
                "mode": "check",
                "loss": loss_sum / accumulation,
                "finite": bool(np.isfinite(loss_sum)),
                "optimizer_step_completed": True,
                "micro_batch_size": check_batch_size,
                "gradient_accumulation_steps": accumulation,
                "effective_batch_size": check_batch_size * accumulation,
                "grad_norm": grad_norm,
                "elapsed_seconds": elapsed,
                "samples_per_second": check_batch_size * accumulation / elapsed,
                "mutable_boundary_audit": boundary_audit,
                "is_causal": model.is_causal,
                "motionlab_commit": git_commit(args.motionlab_root),
                "peak_cuda_memory_gib": torch.cuda.max_memory_allocated(device) / 1024**3,
                "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad),
            },
            indent=2,
            sort_keys=True,
        )
    )


def train(args: argparse.Namespace, contract: dict[str, Any], *, resume: bool) -> None:
    train_cfg = contract["train"]
    base.set_seed(train_cfg["seed"])
    device = torch.device(args.device)
    torch.cuda.set_device(device)
    boundary_audit = verify_mutable_boundaries(args.storymotion_root, contract)
    boundary_audit["motionlab_source"] = verify_motionlab_source(
        args.motionlab_root, contract
    )
    stats_path = _story_path(args.storymotion_root, contract["cache"]["z_norm_stats_path"])
    train_path = _story_path(args.storymotion_root, contract["cache"]["train_path"])
    stats = base.load_latent_znorm_stats(stats_path)
    dataset = HumanLatentCache(train_path, stats)
    if base.sha256_sample_ids(dataset.sample_id) != contract["data"]["train_sample_ids_sha256"]:
        raise RuntimeError("train sample identity mismatch")
    model = build_model(args.motionlab_root, device)
    from rfmotion.models.operator.scheduling_flow_match_euler_discrete import FlowMatchEulerDiscreteScheduler

    scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=train_cfg["lr"],
        betas=tuple(train_cfg["optimizer_betas"]),
        weight_decay=train_cfg["weight_decay"],
    )
    run_root = args.contract.resolve().parent
    paths = run_paths("stage2", contract["run_id"], args.storymotion_root / "runs")
    expected_run_root = paths["root"].resolve()
    if run_root != expected_run_root:
        raise RuntimeError(f"contract must live at {expected_run_root}, got {args.contract.resolve()}")
    if not run_root.is_dir():
        raise FileNotFoundError(run_root)
    train_dir = paths["train"]
    train_dir.mkdir(exist_ok=True)
    log_path = train_dir / "train_log.jsonl"
    checkpoint_path = train_dir / "last.pt"
    meta_path = train_dir / "meta.json"
    accumulation = int(train_cfg["gradient_accumulation_steps"])
    total_steps = int(train_cfg["optimizer_steps"])
    completed_step = 0
    log_reconciliation = {
        "records_before": 0,
        "records_after": 0,
        "truncated": False,
    }
    if resume:
        resume_path = args.resume or checkpoint_path
        if not resume_path.is_file():
            raise FileNotFoundError(resume_path)
        checkpoint = torch.load(resume_path, map_location="cpu")
        if checkpoint.get("contract") != contract or checkpoint.get("is_causal") is not False:
            raise RuntimeError("resume checkpoint contract/non-causal assertion mismatch")
        completed_step = int(checkpoint["step"])
        if checkpoint.get("micro_steps_consumed") != completed_step * accumulation:
            raise RuntimeError("resume checkpoint is not at an optimizer-step boundary")
        if not 0 <= completed_step < total_steps:
            raise RuntimeError("resume step is outside the contracted unfinished schedule")
        model.load_state_dict(checkpoint["model"], strict=True)
        optimizer.load_state_dict(checkpoint["optimizer"])
        restore_rng_state(checkpoint["rng_state"])
        log_reconciliation = reconcile_train_log(log_path, completed_step)
    elif checkpoint_path.exists() or log_path.exists() or meta_path.exists():
        raise FileExistsError("fresh train refuses existing train artifacts")

    total_micro_steps = total_steps * accumulation
    start_micro_step = completed_step * accumulation
    batch_sampler = DeterministicEpochBatchSampler(
        len(dataset),
        int(train_cfg["micro_batch_size"]),
        int(train_cfg["seed"]),
        start_micro_step,
        total_micro_steps,
    )
    loader_generator = torch.Generator(device="cpu")
    loader_generator.manual_seed(0)
    loader = DataLoader(
        dataset,
        batch_sampler=batch_sampler,
        num_workers=args.num_workers,
        pin_memory=True,
        generator=loader_generator,
    )
    batches = iter(loader)
    session = {
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "host": socket.gethostname(),
        "device": args.device,
        "resume": resume,
        "resume_from_step": completed_step,
        "train_log_reconciliation": log_reconciliation,
    }
    if resume and meta_path.is_file():
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
        metadata.setdefault("resume_history", []).append(session)
        metadata["last_session"] = session
    else:
        metadata = {
            **session,
            "motionlab_root": str(args.motionlab_root),
            "motionlab_commit": git_commit(args.motionlab_root),
            "is_causal": False,
            "trainable_parameters": sum(
                p.numel() for p in model.parameters() if p.requires_grad
            ),
            "mutable_boundary_audit": boundary_audit,
            "sampler": "deterministic_epoch_shuffle_without_replacement",
            "resume_history": [],
        }
    meta_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    model.train()
    started = time.monotonic()
    for step in range(completed_step + 1, total_steps + 1):
        optimizer.zero_grad(set_to_none=True)
        loss_sum = 0.0
        for _ in range(accumulation):
            batch = next(batches)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                loss = flow_loss(
                    model,
                    scheduler,
                    batch["human"].to(device, non_blocking=True),
                    batch["human_text"].to(device, non_blocking=True),
                    batch["valid"].to(device, non_blocking=True),
                    train_cfg["text_drop_prob"],
                )
                scaled_loss = loss / accumulation
            scaled_loss.backward()
            loss_sum += float(loss.detach().cpu())
        grad_norm = float(
            nn.utils.clip_grad_norm_(model.parameters(), train_cfg["grad_clip"])
            .detach()
            .cpu()
        )
        optimizer.step()
        if step == 1 or step % args.log_every == 0:
            record = {
                "step": step,
                "loss": loss_sum / accumulation,
                "grad_norm": grad_norm,
                "samples_exposed": step * int(train_cfg["effective_batch_size"]),
                "elapsed_seconds": time.monotonic() - started,
            }
            with log_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, sort_keys=True) + "\n")
        if step % args.save_every == 0 or step == total_steps:
            temporary_path = checkpoint_path.with_suffix(".pt.tmp")
            torch.save(
                checkpoint_payload(model, optimizer, step, step * accumulation, contract),
                temporary_path,
            )
            temporary_path.replace(checkpoint_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["check", "train", "resume"])
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--storymotion-root", type=Path, default=ROOT)
    parser.add_argument(
        "--motionlab-root",
        type=Path,
        default=Path("/data/public/ripemangobox/Motion/MotionLab"),
    )
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--check-batch-size", type=int)
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--log-every", type=int, default=10)
    parser.add_argument("--save-every", type=int, default=1000)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    contract = load_contract(args.contract)
    expected_batch = (
        contract["train"]["micro_batch_size"]
        * contract["train"]["gradient_accumulation_steps"]
    )
    if expected_batch != contract["train"]["effective_batch_size"]:
        raise ValueError("contract effective batch does not equal micro batch times accumulation")
    if args.mode == "check":
        run_check(args, contract)
    else:
        if args.mode == "train" and args.resume is not None:
            raise ValueError("--resume is valid only in resume mode")
        train(args, contract, resume=args.mode == "resume")


if __name__ == "__main__":
    main()
