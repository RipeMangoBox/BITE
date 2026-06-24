#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.train_storymotion_joint_tokenizer import PRESETS
from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer
from storymotion.training.joint_data import (
    CAMERA_FEATURE_DIM,
    HUMAN_FEATURE_DIM,
    PairedPulpMotionHumanCameraDataset,
    collate_human_camera_batch,
)


HUM_DIM = 128
CAM_DIM = 64
LATENT_DIM = HUM_DIM + CAM_DIM
LATENT_FRAMES = 75


def torch_load(path: Path) -> Any:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def load_official_sidecar(path: Path) -> dict[str, Any]:
    data = torch.load(path, map_location="cpu")
    sample_ids = [str(value) for value in data["sample_id"]]
    return {
        "sample_id": sample_ids,
        "index": {sample_id: index for index, sample_id in enumerate(sample_ids)},
        "text": data["text"].float(),
        "valid_mask": data["valid_mask"].bool(),
        "lengths": data.get("lengths"),
        "meta": data.get("meta", {}),
    }


def build_model(args: argparse.Namespace) -> torch.nn.Module:
    if args.preset not in PRESETS:
        raise ValueError(f"unknown preset {args.preset!r}; available: {sorted(PRESETS)}")
    config = dict(PRESETS[args.preset])
    tokenizer = args.tokenizer or config["tokenizer"]
    human_dim = int(args.human_dim or config.get("human_dim", HUMAN_FEATURE_DIM))
    camera_dim = int(args.camera_dim or config.get("camera_dim", CAMERA_FEATURE_DIM))
    if args.drop_camera_z and camera_dim == CAMERA_FEATURE_DIM:
        camera_dim = CAMERA_FEATURE_DIM - 1

    model = build_joint_human_camera_tokenizer(
        tokenizer,
        human_dim=human_dim,
        camera_dim=camera_dim,
        human_latent_dim=int(args.human_latent_dim or config["human_latent_dim"]),
        camera_latent_dim=int(args.camera_latent_dim or config["camera_latent_dim"]),
        hidden_dim=int(args.hidden_dim or config["hidden_dim"]),
        downsample=int(args.downsample or config["downsample"]),
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

    checkpoint = torch_load(args.checkpoint)
    state = (
        checkpoint.get("model")
        or checkpoint.get("model_state_dict")
        or checkpoint.get("state_dict")
        or checkpoint
    )
    model.load_state_dict(state)
    model.eval()
    return model


def reorder_and_align_latent(latent: torch.Tensor, camera_latent_dim: int) -> torch.Tensor:
    if latent.ndim != 3 or latent.shape[-1] != LATENT_DIM:
        raise ValueError(f"expected tokenizer latent [B,T,{LATENT_DIM}], got {tuple(latent.shape)}")
    camera = latent[..., :camera_latent_dim]
    human = latent[..., camera_latent_dim:]
    if human.shape[-1] != HUM_DIM or camera.shape[-1] != CAM_DIM:
        raise ValueError(f"unexpected human/camera latent split: {tuple(human.shape)} {tuple(camera.shape)}")
    z = torch.cat([human, camera], dim=-1).transpose(1, 2).contiguous()
    if z.shape[-1] > LATENT_FRAMES:
        z = z[..., :LATENT_FRAMES]
    elif z.shape[-1] < LATENT_FRAMES:
        z = torch.nn.functional.pad(z, (0, LATENT_FRAMES - z.shape[-1]))
    return z


def save_split(
    *,
    split_name: str,
    human_manifest: Path,
    camera_manifest: Path,
    official_cache: Path,
    out_path: Path,
    model: torch.nn.Module,
    args: argparse.Namespace,
    device: torch.device,
    limit: int | None,
) -> dict[str, Any]:
    dataset = PairedPulpMotionHumanCameraDataset(
        human_manifest,
        camera_manifest,
        drop_camera_z=args.drop_camera_z,
    )
    sidecar = load_official_sidecar(official_cache)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.num_workers,
        pin_memory=args.num_workers > 0 and device.type == "cuda",
        collate_fn=collate_human_camera_batch,
    )

    z_parts: list[torch.Tensor] = []
    text_parts: list[torch.Tensor] = []
    valid_parts: list[torch.Tensor] = []
    length_parts: list[torch.Tensor] = []
    sample_ids: list[str] = []
    processed = 0

    with torch.no_grad():
        for batch_index, batch in enumerate(loader):
            ids = [str(value) for value in batch["sample_id"]]
            if limit is not None and processed >= limit:
                break
            if limit is not None and processed + len(ids) > limit:
                keep = limit - processed
                ids = ids[:keep]
                batch["human"] = batch["human"][:keep]
                batch["camera"] = batch["camera"][:keep]

            missing = [sample_id for sample_id in ids if sample_id not in sidecar["index"]]
            if missing:
                raise KeyError(f"{split_name} official cache is missing sample ids: {missing[:5]}")

            human = batch["human"][: len(ids)].to(device)
            camera = batch["camera"][: len(ids)].to(device)
            latent, _ = model.encode(human, camera)
            z = reorder_and_align_latent(latent.detach().cpu(), model.camera_latent_dim)
            indices = torch.tensor([sidecar["index"][sample_id] for sample_id in ids], dtype=torch.long)
            z_parts.append(z)
            text_parts.append(sidecar["text"].index_select(0, indices))
            valid_parts.append(sidecar["valid_mask"].index_select(0, indices))
            if sidecar["lengths"] is not None:
                length_parts.append(sidecar["lengths"].index_select(0, indices).long())
            else:
                length_parts.append(batch["lengths"][: len(ids)].cpu().long())
            sample_ids.extend(ids)
            processed += len(ids)
            if args.progress_every > 0 and (batch_index + 1) % args.progress_every == 0:
                print(json.dumps({"split": split_name, "processed": processed, "paired_samples": len(dataset)}), flush=True)

    dtype = torch.float16 if args.dtype == "float16" else torch.float32
    output = {
        "z": torch.cat(z_parts, dim=0).to(dtype),
        "text": torch.cat(text_parts, dim=0).to(dtype),
        "valid_mask": torch.cat(valid_parts, dim=0).bool(),
        "lengths": torch.cat(length_parts, dim=0).long(),
        "sample_id": sample_ids,
        "meta": {
            "split": split_name,
            "samples": len(sample_ids),
            "source": "storymotion_joint_tokenizer",
            "tokenizer_checkpoint": str(args.checkpoint),
            "tokenizer_preset": args.preset,
            "drop_camera_z": bool(args.drop_camera_z),
            "human_manifest": str(human_manifest),
            "camera_manifest": str(camera_manifest),
            "official_sidecar_cache": str(official_cache),
            "latent_order": "concat([z_hum,z_cam])",
            "tokenizer_native_latent_order": "concat([z_cam,z_hum])",
            "human_slice": [0, HUM_DIM],
            "camera_slice": [HUM_DIM, LATENT_DIM],
            "latent_shape": [LATENT_DIM, LATENT_FRAMES],
            "camera_feature_dim": int(model.camera_dim),
            "human_feature_dim": int(model.human_dim),
            "camera_latent_dim": int(model.camera_latent_dim),
            "human_latent_dim": int(model.human_latent_dim),
            "sidecar_meta": sidecar["meta"],
        },
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(output, out_path)
    return {
        "path": str(out_path),
        "samples": len(sample_ids),
        "z_shape": list(output["z"].shape),
        "text_shape": list(output["text"].shape),
        "valid_shape": list(output["valid_mask"].shape),
        "dtype": str(output["z"].dtype),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build Stage2 latent cache from a StoryMotion joint Stage1 tokenizer.")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--preset", required=True)
    parser.add_argument("--tokenizer")
    parser.add_argument("--drop-camera-z", action="store_true")
    parser.add_argument("--train-human-manifest", type=Path, required=True)
    parser.add_argument("--train-camera-manifest", type=Path, required=True)
    parser.add_argument("--val-human-manifest", type=Path, required=True)
    parser.add_argument("--val-camera-manifest", type=Path, required=True)
    parser.add_argument("--official-cache-dir", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--dtype", choices=["float16", "float32"], default="float16")
    parser.add_argument("--limit-train", type=int)
    parser.add_argument("--limit-val", type=int)
    parser.add_argument("--progress-every", type=int, default=50)
    parser.add_argument("--human-dim", type=int)
    parser.add_argument("--camera-dim", type=int)
    parser.add_argument("--human-latent-dim", type=int)
    parser.add_argument("--camera-latent-dim", type=int)
    parser.add_argument("--hidden-dim", type=int)
    parser.add_argument("--downsample", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    device = torch.device(args.device)
    model = build_model(args).to(device)
    summary = {
        "checkpoint": str(args.checkpoint),
        "preset": args.preset,
        "drop_camera_z": bool(args.drop_camera_z),
        "train": save_split(
            split_name="train",
            human_manifest=args.train_human_manifest,
            camera_manifest=args.train_camera_manifest,
            official_cache=args.official_cache_dir / "train.pt",
            out_path=args.out_dir / "train.pt",
            model=model,
            args=args,
            device=device,
            limit=args.limit_train,
        ),
        "val": save_split(
            split_name="val",
            human_manifest=args.val_human_manifest,
            camera_manifest=args.val_camera_manifest,
            official_cache=args.official_cache_dir / "val.pt",
            out_path=args.out_dir / "val.pt",
            model=model,
            args=args,
            device=device,
            limit=args.limit_val,
        ),
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
