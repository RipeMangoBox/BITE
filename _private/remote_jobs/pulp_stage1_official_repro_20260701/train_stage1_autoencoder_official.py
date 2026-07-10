#!/usr/bin/env python
"""Standalone Pulp Motion stage-1 autoencoder reproduction runner.

The public Pulp Motion repo ships the autoencoder module and checkpoint config,
but not a dedicated stage-1 training entrypoint. This script keeps the official
repo untouched and reuses its dataset, normalization, and AAMMARDM module.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import random
import sys
import time
from typing import Any

import numpy as np


def patch_numpy_aliases() -> None:
    """Keep smplx/chumpy working with newer NumPy."""
    aliases = {
        "bool": bool,
        "int": int,
        "float": float,
        "complex": complex,
        "object": object,
        "str": str,
        "unicode": str,
    }
    for name, typ in aliases.items():
        if not hasattr(np, name):
            setattr(np, name, typ)


patch_numpy_aliases()

import torch
import torch.nn.functional as F
from hydra import compose, initialize_config_dir
from hydra.utils import instantiate
from omegaconf import OmegaConf
from torch.utils.data import DataLoader, Dataset


class AutoencoderFeatureDataset(Dataset):
    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.joint = dataset.joint_dataset
        self.sample_ids = dataset.sample_ids

    def __len__(self) -> int:
        return len(self.sample_ids)

    def _add_batch_dim(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {key: self._add_batch_dim(item) for key, item in value.items()}
        if hasattr(value, "unsqueeze"):
            return value.unsqueeze(0)
        return value

    def __getitem__(self, index: int) -> dict[str, Any]:
        camera = self.joint.camera_dataset[index]
        human = self.joint.human_dataset[index]
        projection = self.joint.projection_dataset[index]

        x_raw = {
            "camera": camera["camera_raw"],
            "human": human["human_raw"],
            "human_feat": human["human_feat"],
            "projection": projection["projection_raw"],
            "intrinsics": camera["camera_intrinsics"],
        }
        features = self.joint.get_feat(
            self._add_batch_dim(x_raw),
            camera["padding_mask"].unsqueeze(0),
        )

        return {
            "sample_id": camera["sample_id"],
            "camera": features["camera"].squeeze(0),
            "human": features["human"].squeeze(0),
            "projection": features["projection"].squeeze(0),
            "mask": camera["padding_mask"],
        }


class FastAutoencoderFeatureDataset(Dataset):
    """Feature-equivalent loader that skips caption/metric and SMPL reconstruction."""

    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self.joint = dataset.joint_dataset
        self.sample_ids = dataset.sample_ids
        self.num_frames = dataset.num_frames

        self.camera = self.joint.camera_dataset
        self.human = self.joint.human_dataset
        self.projection = self.joint.projection_dataset

        self.distance_mean = self.joint.distance_mean.float()
        self.distance_std = self.joint.distance_std.float()
        self.velocity_mean = self.camera.velocity_mean.float()
        self.velocity_std = self.camera.velocity_std.float()
        self.human_mean = self.human.feat_mean.float()
        self.human_std = self.human.feat_std.float()
        self.joint_indices = self.projection.joint_indices

    def __len__(self) -> int:
        return len(self.sample_ids)

    def _pad_time(self, tensor: torch.Tensor, value: float = 0.0) -> torch.Tensor:
        tensor = tensor[: self.num_frames]
        if tensor.shape[0] >= self.num_frames:
            return tensor
        out_shape = (self.num_frames, *tensor.shape[1:])
        out = torch.full(out_shape, value, dtype=tensor.dtype)
        out[: tensor.shape[0]] = tensor
        return out

    def _load_kitti_poses(self, path: Path) -> torch.Tensor:
        raw = np.loadtxt(path, dtype=np.float32)
        if raw.ndim == 1:
            raw = raw[None]
        if raw.shape[1] == 12:
            mats = np.tile(np.eye(4, dtype=np.float32), (raw.shape[0], 1, 1))
            mats[:, :3, :4] = raw.reshape(-1, 3, 4)
        elif raw.shape[1] == 16:
            mats = raw.reshape(-1, 4, 4)
        else:
            raise ValueError(f"Unsupported trajectory shape {raw.shape} for {path}")
        return torch.from_numpy(mats).float()

    def _camera_velocity_feat(self, camera_raw: torch.Tensor) -> torch.Tensor:
        trans_raw = camera_raw[..., :3, 3].clone()
        velocity = torch.diff(trans_raw, dim=0)
        velocity = (velocity - self.velocity_mean) / self.velocity_std
        velocity = torch.cat([torch.zeros(1, 3), velocity], dim=0)

        rot_raw = camera_raw[..., :3, :3].clone()
        rot6d = rot_raw[..., :, :2].permute(0, 2, 1).reshape(rot_raw.shape[0], 6)
        return torch.cat([rot6d, velocity], dim=-1)

    def _fov_feat(self, intrinsics: torch.Tensor) -> torch.Tensor:
        fov_h = 2 * torch.atan(intrinsics[..., 3] / intrinsics[..., 1])
        fov_w = 2 * torch.atan(intrinsics[..., 2] / intrinsics[..., 0])
        return torch.stack([fov_h, fov_w], dim=-1).nan_to_num(0.0)

    def _projection_feat(self, projection_raw: torch.Tensor, intrinsics: torch.Tensor) -> torch.Tensor:
        centers = intrinsics[..., None, [-2, -1]].clone()
        proj = projection_raw[..., self.joint_indices, :2].clone()
        proj[..., 0] = proj[..., 0] - centers[..., 0]
        proj[..., 1] = centers[..., 1] - proj[..., 1]
        proj[..., :2] = (proj[..., :2] / centers).nan_to_num(0.0)
        proj = torch.clamp(proj, -2.0, 2.0)
        return proj.reshape(proj.shape[0], -1).float()

    def __getitem__(self, index: int) -> dict[str, Any]:
        sample_id = self.sample_ids[index]
        filename = sample_id + ".npy"

        camera_raw = self._load_kitti_poses(self.camera.raw_dir / (sample_id + ".txt"))
        intrinsics = torch.from_numpy(np.load(self.camera.intrinsics_dir / filename)).float()
        human_feat_raw = torch.from_numpy(np.load(self.human.feat_dir / filename)).float()
        projection_raw = torch.from_numpy(np.load(self.projection.proj_dir / filename)).float()
        from utils.rifke_utils import smplrifkefeats_to_smpldata

        human_joints, _ = smplrifkefeats_to_smpldata(human_feat_raw, batch=False)

        valid_frames = min(
            camera_raw.shape[0],
            intrinsics.shape[0],
            human_feat_raw.shape[0],
            human_joints.shape[0],
            projection_raw.shape[0],
            self.num_frames,
        )
        mask = torch.zeros(self.num_frames, dtype=torch.bool)
        mask[:valid_frames] = True

        camera_raw = self._pad_time(camera_raw)
        intrinsics = self._pad_time(intrinsics)
        human_feat_raw = self._pad_time(human_feat_raw)
        human_joints = self._pad_time(human_joints)
        projection_raw = self._pad_time(projection_raw)

        distance = camera_raw[..., :3, 3] - human_joints[..., 0, :3]
        distance = (distance - self.distance_mean) / self.distance_std
        camera_feat = torch.cat(
            [self._fov_feat(intrinsics), distance, self._camera_velocity_feat(camera_raw)],
            dim=-1,
        )
        human_feat = (human_feat_raw - self.human_mean) / self.human_std
        projection_feat = self._projection_feat(projection_raw, intrinsics)

        camera_feat[~mask] = 0.0
        human_feat[~mask] = 0.0
        projection_feat[~mask] = 0.0

        return {
            "sample_id": sample_id,
            "camera": camera_feat,
            "human": human_feat,
            "projection": projection_feat,
            "mask": mask,
        }


def masked_mse(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    mask = mask.to(dtype=pred.dtype).unsqueeze(-1)
    denom = mask.sum().clamp_min(1.0) * target.shape[-1]
    return ((pred - target).pow(2) * mask).sum() / denom


def lr_factor(step: int, warmup_steps: int, decay_step: int, decay_factor: float) -> float:
    if step < warmup_steps:
        return float(step + 1) / float(max(1, warmup_steps))
    if step >= decay_step:
        return decay_factor
    return 1.0


def build_dataset(
    args: argparse.Namespace,
    split: str,
    split_prefix: str | None = None,
    num_frames: int = 64,
) -> AutoencoderFeatureDataset:
    repo_root = Path(args.repo_root).resolve()
    sys.path.insert(0, str(repo_root))
    os.chdir(repo_root)

    if not OmegaConf.has_resolver("eval"):
        OmegaConf.register_new_resolver("eval", eval)

    overrides = [
        f"dataset.dataset_dir={args.dataset_dir}",
        f"checkpoint_dir={args.checkpoint_dir}",
        f"dataset.num_frames={num_frames}",
        f"dataset.joint.projection.num_frames={num_frames}",
        f"dataset.joint.set_name={split_prefix or args.split_prefix}",
        "dataset.filter_missing=true",
    ]
    with initialize_config_dir(version_base="1.3", config_dir=str(repo_root / "configs")):
        config = compose(config_name="config_dit_xyz", overrides=overrides)
    dataset = instantiate(config.dataset).set_split(split)
    return AutoencoderFeatureDataset(dataset)


@torch.no_grad()
def evaluate(
    model: torch.nn.Module,
    loader: DataLoader,
    device: torch.device,
    max_batches: int,
) -> dict[str, float]:
    model.eval()
    totals = {"loss": 0.0, "camera": 0.0, "human": 0.0, "projection": 0.0}
    num_batches = 0
    for batch_index, batch in enumerate(loader, start=1):
        if max_batches and batch_index > max_batches:
            break
        camera = batch["camera"].to(device, non_blocking=True)
        human = batch["human"].to(device, non_blocking=True)
        projection = batch["projection"].to(device, non_blocking=True)
        mask = batch["mask"].to(device, non_blocking=True)

        z = model.encode(camera, human, projection)
        camera_hat, human_hat, projection_hat = model.decode(z)
        camera_loss = masked_mse(camera_hat, camera, mask)
        human_loss = masked_mse(human_hat, human, mask)
        projection_loss = masked_mse(projection_hat, projection, mask)
        loss = camera_loss + human_loss + projection_loss

        values = {
            "loss": float(loss.detach().cpu()),
            "camera": float(camera_loss.detach().cpu()),
            "human": float(human_loss.detach().cpu()),
            "projection": float(projection_loss.detach().cpu()),
        }
        for key, value in values.items():
            totals[key] += value
        num_batches += 1
    return {key: value / max(1, num_batches) for key, value in totals.items()}


def save_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default="/data/public/ripemangobox/Motion/PulpMotion")
    parser.add_argument("--dataset-dir", default="/data/public/ripemangobox/Motion/datasets/pulpmotion-data")
    parser.add_argument("--checkpoint-dir", default="/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models")
    parser.add_argument("--output-dir", default="/data/public/ripemangobox/Motion/PulpMotion/results/stage1_official_repro_20260701")
    parser.add_argument("--split-prefix", default="mixed_")
    parser.add_argument("--epochs", type=int, default=325)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=8)
    parser.add_argument("--lr", type=float, default=1.9e-4)
    parser.add_argument("--warmup-steps", type=int, default=1000)
    parser.add_argument("--decay-step", type=int, default=4000)
    parser.add_argument("--decay-factor", type=float, default=0.1)
    parser.add_argument("--weight-decay", type=float, default=1e-5)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--log-every", type=int, default=50)
    parser.add_argument("--save-every", type=int, default=5)
    parser.add_argument("--val-every", type=int, default=5)
    parser.add_argument("--val-batches", type=int, default=0)
    parser.add_argument("--eval-batch-size", type=int, default=64)
    parser.add_argument("--limit-train-batches", type=int, default=0)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--loader", choices=["fast", "official"], default="fast")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    torch.set_float32_matmul_precision("medium")

    output_dir = Path(args.output_dir)
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.jsonl"

    base_train_dataset = build_dataset(args, "train", args.split_prefix, num_frames=64)
    if args.loader == "official":
        train_dataset = base_train_dataset
    else:
        train_dataset = FastAutoencoderFeatureDataset(base_train_dataset.dataset)
    val_loaders = {}
    for prefix, name in [("mixed_", "mixed300"), ("pure_", "pure300")]:
        base_val_dataset = build_dataset(args, "test", prefix, num_frames=300)
        val_dataset = (
            base_val_dataset
            if args.loader == "official"
            else FastAutoencoderFeatureDataset(base_val_dataset.dataset)
        )
        val_loaders[name] = DataLoader(
            val_dataset,
            batch_size=args.eval_batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=True,
            persistent_workers=args.num_workers > 0,
            drop_last=False,
        )
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=True,
        persistent_workers=args.num_workers > 0,
        drop_last=True,
    )

    from src.models.autoencoders.modules.mmardm import AAMMARDM

    model = AAMMARDM(
        camera_latent_dim=64,
        human_latent_dim=128,
        projection_latent_dim=64,
        down_t=2,
        stride_t=2,
        width=192,
        depth=2,
        dilation_growth_rate=3,
        activation="relu",
        norm=None,
        do_projection=True,
        do_bias=False,
    )
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    model.to(device)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args.lr,
        betas=(0.9, 0.99),
        eps=1e-8,
        weight_decay=args.weight_decay,
    )

    metadata = {
        "source": "Pulp Motion official repo modules + paper Appendix E.1",
        "assumptions": [
            "public repo does not ship a stage-1 training entrypoint",
            "loss is equal-weight masked MSE over camera, human, and projection reconstructions",
            "full Pulp Motion dataset is mapped to mixed_train_split",
        ],
        "architecture": {
            "camera_latent_dim": 64,
            "human_latent_dim": 128,
            "projection_latent_dim": 64,
            "downsample_factor": 4,
            "resnet_blocks": 2,
            "width": 192,
        },
        "training": vars(args),
        "train_samples": len(train_dataset),
        "steps_per_epoch": len(train_loader),
        "validation": {
            "mixed300_samples": len(val_loaders["mixed300"].dataset),
            "pure300_samples": len(val_loaders["pure300"].dataset),
            "val_every": args.val_every,
            "val_batches": args.val_batches,
            "metrics": "masked feature-space reconstruction MSE; official TMR/CLaTr/projection evaluation remains a separate checkpoint evaluation",
        },
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)

    global_step = 0
    for epoch in range(1, args.epochs + 1):
        model.train()
        epoch_start = time.time()
        totals = {"loss": 0.0, "camera": 0.0, "human": 0.0, "projection": 0.0}
        num_batches = 0

        for batch_index, batch in enumerate(train_loader, start=1):
            if args.limit_train_batches and batch_index > args.limit_train_batches:
                break

            camera = batch["camera"].to(device, non_blocking=True)
            human = batch["human"].to(device, non_blocking=True)
            projection = batch["projection"].to(device, non_blocking=True)
            mask = batch["mask"].to(device, non_blocking=True)

            z = model.encode(camera, human, projection)
            camera_hat, human_hat, projection_hat = model.decode(z)

            camera_loss = masked_mse(camera_hat, camera, mask)
            human_loss = masked_mse(human_hat, human, mask)
            projection_loss = masked_mse(projection_hat, projection, mask)
            loss = camera_loss + human_loss + projection_loss

            factor = lr_factor(global_step, args.warmup_steps, args.decay_step, args.decay_factor)
            for group in optimizer.param_groups:
                group["lr"] = args.lr * factor

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
            global_step += 1

            values = {
                "loss": float(loss.detach().cpu()),
                "camera": float(camera_loss.detach().cpu()),
                "human": float(human_loss.detach().cpu()),
                "projection": float(projection_loss.detach().cpu()),
            }
            for key, value in values.items():
                totals[key] += value
            num_batches += 1

            if global_step == 1 or global_step % args.log_every == 0:
                record = {
                    "epoch": epoch,
                    "batch": batch_index,
                    "global_step": global_step,
                    "lr": optimizer.param_groups[0]["lr"],
                    **values,
                }
                print(json.dumps(record, sort_keys=True), flush=True)
                save_jsonl(metrics_path, record)

        epoch_record = {
            "epoch": epoch,
            "global_step": global_step,
            "seconds": round(time.time() - epoch_start, 3),
            "lr": optimizer.param_groups[0]["lr"],
            **{f"train_{key}": value / max(1, num_batches) for key, value in totals.items()},
        }
        print(json.dumps(epoch_record, sort_keys=True), flush=True)
        save_jsonl(metrics_path, epoch_record)

        if args.val_every and (epoch % args.val_every == 0 or epoch == args.epochs):
            for val_name, val_loader in val_loaders.items():
                val_start = time.time()
                val_metrics = evaluate(model, val_loader, device, args.val_batches)
                val_record = {
                    "epoch": epoch,
                    "global_step": global_step,
                    "split": val_name,
                    "seconds": round(time.time() - val_start, 3),
                    **{f"val_{key}": value for key, value in val_metrics.items()},
                }
                print(json.dumps(val_record, sort_keys=True), flush=True)
                save_jsonl(metrics_path, val_record)

        if epoch % args.save_every == 0 or epoch == args.epochs:
            torch.save(model.state_dict(), checkpoint_dir / f"aemmardm-repro-epoch{epoch:03d}.ckpt")
            torch.save(
                {
                    "epoch": epoch,
                    "global_step": global_step,
                    "model": model.state_dict(),
                    "optimizer": optimizer.state_dict(),
                    "args": vars(args),
                },
                checkpoint_dir / "latest.pt",
            )


if __name__ == "__main__":
    main()
