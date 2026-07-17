#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.storymotion_run_layout import run_paths

from scripts.train_storymotion_joint_tokenizer import PRESETS
from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer
from storymotion.experiment_invariants import (
    DEFAULT_CAMERA_DIM,
    DEFAULT_CAMERA_LATENT_DIM,
    DEFAULT_FEATURE_CONTRACT,
    DEFAULT_HUMAN_DIM,
    DEFAULT_HUMAN_LATENT_DIM,
    DEFAULT_IS_CAUSAL,
    DEFAULT_TOKENIZER_KIND,
    assert_default_cache_meta,
)
from storymotion.training.joint_data import (
    CAMERA_FEATURE_DIM,
    HUMAN_FEATURE_DIM,
    LEGACY_FEATURE_CONTRACT,
    RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
    RAW_OFFICIAL_FEATURE_CONTRACT,
    OFFICIAL_FEATURE_CONTRACT,
    PairedPulpMotionHumanCameraDataset,
    collate_human_camera_batch,
)


HUM_DIM = 128
CAM_DIM = 64
LATENT_DIM = HUM_DIM + CAM_DIM
LATENT_FRAMES = 75
TEXT_DIM = 1024
DEFAULT_DATA_ROOT = Path("/data/public/ripemangobox/Motion/datasets/pulpmotion-data")


def sha256_sample_ids(sample_ids: list[str]) -> str:
    digest = hashlib.sha256()
    for sample_id in sample_ids:
        digest.update(str(sample_id).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


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


def latent_valid_mask(lengths: torch.Tensor, downsample: int = 4) -> torch.Tensor:
    latent_lengths = torch.ceil(lengths.float() / float(downsample)).long().clamp(min=1, max=LATENT_FRAMES)
    positions = torch.arange(LATENT_FRAMES, device=lengths.device)
    return (positions[None, :] < latent_lengths[:, None]).cpu()


def load_caption_token(data_root: Path, dirname: str, sample_id: str) -> torch.Tensor:
    path = data_root / f"{dirname}_clip" / "token" / f"{sample_id}.npy"
    if not path.exists():
        raise FileNotFoundError(f"caption token not found: {path}")
    array = np.load(path, allow_pickle=True)
    token = np.asarray(array[0], dtype=np.float32)
    if token.shape != (512,):
        raise ValueError(f"expected {path} to contain [1,512] token embedding, got {array.shape} -> {token.shape}")
    return torch.from_numpy(token)


def load_direct_sidecar_batch(data_root: Path, sample_ids: list[str], lengths: torch.Tensor) -> dict[str, torch.Tensor]:
    text = torch.stack(
        [
            torch.cat(
                [
                    load_caption_token(data_root, "caption_cam", sample_id),
                    load_caption_token(data_root, "caption_char", sample_id),
                ]
            )
            for sample_id in sample_ids
        ],
        dim=0,
    ).float()
    if text.shape != (len(sample_ids), TEXT_DIM):
        raise ValueError(f"expected text [{len(sample_ids)},{TEXT_DIM}], got {tuple(text.shape)}")
    return {
        "text": text,
        "valid_mask": latent_valid_mask(lengths),
        "lengths": lengths.cpu().long(),
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

    checkpoint = torch_load(args.checkpoint)
    embedded_contract = checkpoint.get("stage1_model_contract", {}) if isinstance(checkpoint, dict) else {}
    checkpoint_args = checkpoint.get("args", {}) if isinstance(checkpoint, dict) else {}
    checkpoint_args = {**embedded_contract, **checkpoint_args}
    run_config_path = next(
        (parent / "run_config.json" for parent in args.checkpoint.parents if (parent / "run_config.json").exists()),
        None,
    )
    if run_config_path is not None:
        checkpoint_args = {**json.loads(run_config_path.read_text(encoding="utf-8")), **checkpoint_args}
    checkpoint_contract = str(checkpoint_args.get("feature_contract", LEGACY_FEATURE_CONTRACT))
    if checkpoint_contract != args.feature_contract:
        raise ValueError(
            f"checkpoint feature contract {checkpoint_contract!r} does not match requested {args.feature_contract!r}"
        )
    checkpoint_is_causal = bool(
        checkpoint_args.get("is_causal", checkpoint_args.get("is_casual", True))
    )
    assert checkpoint_is_causal is False
    human_latent_dim = int(args.human_latent_dim or config["human_latent_dim"])
    camera_latent_dim = int(args.camera_latent_dim or config["camera_latent_dim"])

    if args.feature_contract == DEFAULT_FEATURE_CONTRACT and tokenizer == DEFAULT_TOKENIZER_KIND:
        assert human_dim == DEFAULT_HUMAN_DIM
        assert camera_dim == DEFAULT_CAMERA_DIM
        assert human_latent_dim == DEFAULT_HUMAN_LATENT_DIM
        assert camera_latent_dim == DEFAULT_CAMERA_LATENT_DIM
        assert checkpoint_is_causal is DEFAULT_IS_CAUSAL

    model = build_joint_human_camera_tokenizer(
        tokenizer,
        human_dim=human_dim,
        camera_dim=camera_dim,
        human_latent_dim=human_latent_dim,
        camera_latent_dim=camera_latent_dim,
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
        residual_depth=int(config.get("residual_depth", 2)),
        dilation_growth_rate=int(config.get("dilation_growth_rate", 3)),
        residual_activation=str(config.get("residual_activation", "relu")),
        residual_dropout=float(config.get("residual_dropout", 0.2)),
        is_causal=False,
    )
    if args.preset.startswith("storymotion_v8_"):
        if not embedded_contract:
            raise ValueError("v8 Stage1 checkpoints require an embedded stage1_model_contract")
        expected_contract = {
            "tokenizer": tokenizer,
            "preset": args.preset,
            "feature_contract": args.feature_contract,
            "is_causal": False,
            "human_dim": human_dim,
            "camera_dim": camera_dim,
            "human_latent_dim": human_latent_dim,
            "camera_latent_dim": camera_latent_dim,
        }
        mismatches = {
            key: (embedded_contract.get(key), expected)
            for key, expected in expected_contract.items()
            if embedded_contract.get(key) != expected
        }
        if mismatches:
            raise ValueError(f"embedded v8 Stage1 checkpoint contract mismatch: {mismatches}")
    state = (
        checkpoint.get("model")
        or checkpoint.get("model_state_dict")
        or checkpoint.get("state_dict")
        or checkpoint
    )
    model.load_state_dict(state)
    model.eval()
    model.stage1_checkpoint_contract = {
        "feature_contract": checkpoint_contract,
        "is_causal": checkpoint_is_causal,
        "tokenizer": tokenizer,
        "human_dim": human_dim,
        "camera_dim": camera_dim,
        "human_latent_dim": human_latent_dim,
        "camera_latent_dim": camera_latent_dim,
        "native_latent_order": embedded_contract.get("native_latent_order", "camera64+human128"),
        "embedded_contract": embedded_contract,
    }
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
        feature_contract=args.feature_contract,
        pulp_root=args.pulp_root,
    )
    sidecar = load_official_sidecar(official_cache) if args.sidecar_source != "direct" else None
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

            human = batch["human"][: len(ids)].to(device)
            camera = batch["camera"][: len(ids)].to(device)
            latent, _ = model.encode(human, camera)
            z = reorder_and_align_latent(latent.detach().cpu(), model.camera_latent_dim)
            lengths = batch["lengths"][: len(ids)].cpu().long()
            missing = [] if sidecar is None else [sample_id for sample_id in ids if sample_id not in sidecar["index"]]
            use_direct = args.sidecar_source == "direct" or (args.sidecar_source == "auto" and missing)
            if args.sidecar_source == "official" and missing:
                raise KeyError(f"{split_name} official cache is missing sample ids: {missing[:5]}")
            if use_direct:
                batch_sidecar = load_direct_sidecar_batch(args.data_root, ids, lengths)
            else:
                if sidecar is None:
                    raise RuntimeError("official sidecar was not loaded")
                indices = torch.tensor([sidecar["index"][sample_id] for sample_id in ids], dtype=torch.long)
                batch_sidecar = {
                    "text": sidecar["text"].index_select(0, indices),
                    "valid_mask": sidecar["valid_mask"].index_select(0, indices),
                    "lengths": (
                        sidecar["lengths"].index_select(0, indices).long()
                        if sidecar["lengths"] is not None
                        else lengths
                    ),
                }
            z_parts.append(z)
            text_parts.append(batch_sidecar["text"])
            valid_parts.append(batch_sidecar["valid_mask"])
            length_parts.append(batch_sidecar["lengths"])
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
            "sample_ids_sha256": sha256_sample_ids(sample_ids),
            "source": "storymotion_joint_tokenizer",
            "tokenizer_checkpoint": str(args.checkpoint),
            "tokenizer_preset": args.preset,
            "tokenizer_is_causal": bool(getattr(model, "is_causal", False)),
            "drop_camera_z": bool(args.drop_camera_z),
            "human_manifest": str(human_manifest),
            "camera_manifest": str(camera_manifest),
            "official_sidecar_cache": str(official_cache),
            "sidecar_source": args.sidecar_source,
            "data_root": str(args.data_root),
            "latent_order": "concat([z_hum,z_cam])",
            "tokenizer_native_latent_order": "concat([z_cam,z_hum])",
            "human_slice": [0, HUM_DIM],
            "camera_slice": [HUM_DIM, LATENT_DIM],
            "latent_shape": [LATENT_DIM, LATENT_FRAMES],
            "camera_feature_dim": int(model.camera_dim),
            "human_feature_dim": int(model.human_dim),
            "feature_contract": args.feature_contract,
            "camera_latent_dim": int(model.camera_latent_dim),
            "human_latent_dim": int(model.human_latent_dim),
            "sidecar_meta": sidecar["meta"] if sidecar is not None else {},
        },
    }
    if (
        args.feature_contract == DEFAULT_FEATURE_CONTRACT
        and model.stage1_checkpoint_contract["tokenizer"] == DEFAULT_TOKENIZER_KIND
    ):
        assert_default_cache_meta(output["meta"])
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
    parser.add_argument(
        "--feature-contract",
        choices=[
            LEGACY_FEATURE_CONTRACT,
            OFFICIAL_FEATURE_CONTRACT,
            RAW_OFFICIAL_FEATURE_CONTRACT,
            RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
        ],
        required=True,
    )
    parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    parser.add_argument("--train-human-manifest", type=Path, required=True)
    parser.add_argument("--train-camera-manifest", type=Path, required=True)
    parser.add_argument("--val-human-manifest", type=Path, required=True)
    parser.add_argument("--val-camera-manifest", type=Path, required=True)
    parser.add_argument("--official-cache-dir", type=Path, required=True)
    parser.add_argument("--sidecar-source", choices=["auto", "official", "direct"], default="auto")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--runs-root", type=Path, default=ROOT / "runs")
    parser.add_argument("--cache-id", help="Canonical Stage2 run id; derives the cache path under runs/stage2/<run-id>/cache.")
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
    parser = build_parser()
    args = parser.parse_args()
    if args.out_dir is None:
        if not args.cache_id:
            parser.error("--out-dir is required unless --cache-id is supplied")
        args.out_dir = run_paths("stage2", args.cache_id, args.runs_root)["cache"]
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
