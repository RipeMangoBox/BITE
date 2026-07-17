#!/usr/bin/env python3
"""Measure full-sequence Stage1 reconstruction geometry as a function of length."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.eval_stage1_joint_tokenizer_official_recon import (  # noqa: E402
    build_config,
    load_rows_by_id,
    move_to_device,
    reconstruct_batch,
)
from scripts.render_stage1_joint_separate_3d_reconstructions import (  # noqa: E402
    build_model,
    load_checkpoint_run_config,
    parse_model_spec,
)
from storymotion_official_bridge_smoke import add_pulp_import_paths, patch_numpy_aliases  # noqa: E402
from storymotion.training.joint_data import OFFICIAL_FEATURE_CONTRACT, _load_official_stats  # noqa: E402
from storymotion.training.human200 import (  # noqa: E402
    HUMAN200_DIM,
    HUMAN200_FEATURE_CONTRACT,
    human200_to_official_human199,
    official_human199_to_human200,
)


LENGTH_BINS = ((1, 64), (65, 128), (129, 192), (193, None))
METRICS = (
    "human_root_aligned_mpjpe",
    "human_global_mpjpe",
    "human_root_ade",
    "human_root_fde",
    "human_integrated_yaw_geodesic",
    "camera_center_ade",
    "camera_center_fde",
    "camera_rotation_deg",
)

HUMAN199_CHANNEL_ORACLES = {
    "oracle_gt_root_height": (0, 1),
    "oracle_gt_root_xy_velocity": (1, 3),
    "oracle_gt_yaw_velocity": (3, 4),
    "oracle_gt_root_channels": (0, 4),
    "oracle_gt_local_joints": (136, 199),
    "oracle_gt_nonroot_channels": (4, 199),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--story-root", type=Path, default=ROOT)
    parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    parser.add_argument("--data-root", type=Path, default=ROOT / "linked/pulpmotion-data")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"),
    )
    parser.add_argument("--config-name", default="config_dit_xy")
    parser.add_argument(
        "--official-checkpoint-override",
        type=Path,
        help="Load this autoaligner state dict instead of the checkpoint declared by the Pulp config.",
    )
    parser.add_argument(
        "--official-source-label",
        default="pulp_official",
        help="Source prefix written to metric rows; required to be non-default for checkpoint overrides.",
    )
    parser.add_argument("--set-name", default="pure_", choices=["pure_", "mixed_"])
    parser.add_argument("--split", default="test")
    parser.add_argument("--human-manifest", type=Path, required=True)
    parser.add_argument("--camera-manifest", type=Path, required=True)
    parser.add_argument("--local-model", required=True, help="name:preset:checkpoint")
    parser.add_argument("--human200-stats", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--expected-samples", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--progress-every", type=int, default=25)
    parser.add_argument(
        "--fixed-max-frames",
        type=int,
        default=300,
        help="Fixed right-padded context used by the Pulp Stage1 input policy.",
    )
    parser.add_argument(
        "--human-channel-oracles",
        action="store_true",
        help=(
            "Replace selected reconstructed normalized human199 channels with their GT values before "
            "decoding, to attribute root integration and local-body reconstruction error."
        ),
    )
    return parser


def human_joints(value: Any) -> torch.Tensor:
    if isinstance(value, dict):
        value = value["joints"]
    else:
        value = getattr(value, "joints", value)
    if not torch.is_tensor(value):
        raise TypeError(f"expected human joints tensor, got {type(value)!r}")
    return value


def official_reconstruct_true_length(
    autoencoder: torch.nn.Module,
    x_input: dict[str, torch.Tensor],
    padding_mask: torch.Tensor,
) -> dict[str, torch.Tensor]:
    outputs: dict[str, torch.Tensor] = {}
    for index in range(padding_mask.shape[0]):
        frames = int(padding_mask[index].sum().item())
        single = {key: value[index : index + 1, :frames] for key, value in x_input.items()}
        z_scale = int(getattr(autoencoder, "z_scale", 1))
        aligned_frames = ((frames + z_scale - 1) // z_scale) * z_scale
        if aligned_frames != frames:
            single = {
                key: torch.nn.functional.pad(value, (0, 0, 0, aligned_frames - frames))
                for key, value in single.items()
            }
        latent = autoencoder.encode(single)
        reconstructed = autoencoder.decode(latent)
        for key, value in reconstructed.items():
            if key not in outputs:
                outputs[key] = torch.zeros_like(x_input[key])
            outputs[key][index, :frames] = reconstructed[key][0, :frames]
    return outputs


def reconstruct_fixed_length(
    model: torch.nn.Module,
    x_input: dict[str, torch.Tensor],
    padding_mask: torch.Tensor,
    fixed_max_frames: int,
    *,
    official: bool,
    feature_contract: str = OFFICIAL_FEATURE_CONTRACT,
    official_stats: dict[str, torch.Tensor] | None = None,
    human200_stats: dict[str, Any] | None = None,
) -> dict[str, torch.Tensor]:
    if fixed_max_frames <= 0:
        raise ValueError("fixed_max_frames must be positive")
    if int(padding_mask.sum(dim=1).max().item()) > fixed_max_frames:
        raise ValueError("a valid sequence is longer than fixed_max_frames; truncation is not allowed in this audit")

    fixed_input: dict[str, torch.Tensor] = {}
    for key, value in x_input.items():
        value = value[:, :fixed_max_frames]
        if value.shape[1] < fixed_max_frames:
            value = torch.nn.functional.pad(value, (0, 0, 0, fixed_max_frames - value.shape[1]))
        fixed_input[key] = value
    fixed_mask = torch.arange(fixed_max_frames, device=padding_mask.device)[None] < padding_mask.sum(dim=1)[:, None]
    fixed_input = {
        key: value.masked_fill(~fixed_mask[..., None], 0.0)
        for key, value in fixed_input.items()
    }

    if official:
        reconstructed = model.decode(model.encode(fixed_input))
        return {key: value[:, :fixed_max_frames] for key, value in reconstructed.items()}
    if feature_contract == HUMAN200_FEATURE_CONTRACT:
        if official_stats is None or human200_stats is None:
            raise ValueError("v8.2 fixed-length reconstruction requires matched statistics")
        human200 = torch.zeros(
            (fixed_input["human"].shape[0], fixed_max_frames, HUMAN200_DIM),
            device=fixed_input["human"].device,
            dtype=fixed_input["human"].dtype,
        )
        for index in range(fixed_input["human"].shape[0]):
            frames = int(fixed_mask[index].sum().item())
            human200[index, :frames] = official_human199_to_human200(
                fixed_input["human"][index, :frames],
                official_stats["human_mean"],
                official_stats["human_std"],
                human200_stats,
            )
        fixed_input["human"] = human200
    output = model(fixed_input["human"], fixed_input["camera"])
    human_recon = output.human_recon[:, :fixed_max_frames]
    if feature_contract == HUMAN200_FEATURE_CONTRACT:
        official_human = torch.zeros(
            (human_recon.shape[0], fixed_max_frames, 199),
            device=human_recon.device,
            dtype=human_recon.dtype,
        )
        for index in range(human_recon.shape[0]):
            frames = int(fixed_mask[index].sum().item())
            official_human[index, :frames] = human200_to_official_human199(
                human_recon[index, :frames],
                human200_stats,
                official_stats["human_mean"],
                official_stats["human_std"],
            )
        human_recon = official_human
    return {
        "human": human_recon,
        "camera": output.camera_recon[:, :fixed_max_frames],
    }


def integrated_yaw_from_official_human199(
    human: torch.Tensor,
    official_stats: dict[str, torch.Tensor],
) -> torch.Tensor:
    if human.ndim != 3 or human.shape[-1] != 199:
        raise ValueError(f"expected normalized Pulp human199 [B,T,199], got {tuple(human.shape)}")
    mean = official_stats["human_mean"].to(device=human.device, dtype=human.dtype)
    std = official_stats["human_std"].to(device=human.device, dtype=human.dtype)
    return torch.cumsum(human[..., 3] * std[3] + mean[3], dim=1)


def geometry_row(
    source: str,
    sample_id: str,
    frames: int,
    predicted: dict[str, Any],
    target: dict[str, Any],
    predicted_yaw: torch.Tensor,
    target_yaw: torch.Tensor,
    index: int,
) -> dict[str, Any]:
    pred_joints = human_joints(predicted["human"])[index, :frames].detach().float().cpu()
    gt_joints = human_joints(target["human"])[index, :frames].detach().float().cpu()
    pred_camera = predicted["camera"][index, :frames].detach().float().cpu()
    gt_camera = target["camera"][index, :frames].detach().float().cpu()

    pred_root = pred_joints[:, 0]
    gt_root = gt_joints[:, 0]
    root_aligned = (pred_joints - pred_root[:, None]) - (gt_joints - gt_root[:, None])
    global_error = torch.linalg.vector_norm(pred_joints - gt_joints, dim=-1)
    root_error = torch.linalg.vector_norm(pred_root - gt_root, dim=-1)

    pred_center = pred_camera[:, :3, 3]
    gt_center = gt_camera[:, :3, 3]
    camera_error = torch.linalg.vector_norm(pred_center - gt_center, dim=-1)
    relative_rotation = pred_camera[:, :3, :3].transpose(-1, -2) @ gt_camera[:, :3, :3]
    cosine = ((relative_rotation.diagonal(dim1=-2, dim2=-1).sum(-1) - 1.0) / 2.0).clamp(-1.0, 1.0)
    rotation_deg = torch.rad2deg(torch.acos(cosine))
    yaw_delta = predicted_yaw[index, :frames] - target_yaw[index, :frames]
    yaw_geodesic = torch.atan2(torch.sin(yaw_delta), torch.cos(yaw_delta)).abs()

    return {
        "source": source,
        "sample_id": sample_id,
        "frames": frames,
        "human_root_aligned_mpjpe": float(torch.linalg.vector_norm(root_aligned, dim=-1).mean().item()),
        "human_global_mpjpe": float(global_error.mean().item()),
        "human_root_ade": float(root_error.mean().item()),
        "human_root_fde": float(root_error[-1].item()),
        "human_integrated_yaw_geodesic": float(torch.rad2deg(yaw_geodesic).mean().item()),
        "camera_center_ade": float(camera_error.mean().item()),
        "camera_center_fde": float(camera_error[-1].item()),
        "camera_rotation_deg": float(rotation_deg.mean().item()),
    }


def mean_metrics(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {metric: float(np.mean([float(row[metric]) for row in rows])) for metric in METRICS}


def summarize_source(rows: list[dict[str, Any]]) -> dict[str, Any]:
    lengths = np.asarray([row["frames"] for row in rows], dtype=np.float64)
    summary: dict[str, Any] = {
        "samples": len(rows),
        "length": {
            "min": int(lengths.min()),
            "median": float(np.median(lengths)),
            "p90": float(np.quantile(lengths, 0.9)),
            "max": int(lengths.max()),
        },
        "overall": mean_metrics(rows),
        "bins": [],
        "length_dependence": {},
    }
    for lower, upper in LENGTH_BINS:
        selected = [row for row in rows if row["frames"] >= lower and (upper is None or row["frames"] <= upper)]
        summary["bins"].append(
            {
                "label": f"{lower}+" if upper is None else f"{lower}-{upper}",
                "samples": len(selected),
                "metrics": mean_metrics(selected) if selected else None,
            }
        )
    for metric in METRICS:
        values = np.asarray([row[metric] for row in rows], dtype=np.float64)
        slope = float(np.polyfit(lengths, values, 1)[0] * 100.0) if len(rows) > 1 else 0.0
        correlation = float(np.corrcoef(lengths, values)[0, 1]) if len(rows) > 1 else 0.0
        summary["length_dependence"][metric] = {
            "slope_per_100_frames": slope,
            "pearson_r": correlation,
        }
    return summary


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    add_pulp_import_paths(args.pulp_root)
    torch.set_float32_matmul_precision("medium")
    device = torch.device(args.device)

    from hydra.utils import instantiate

    cfg = build_config(args)
    dataset = instantiate(cfg.dataset).set_split(args.split, mode="test")
    if args.samples > 0:
        sample_ids = [str(value) for value in dataset.sample_ids[: args.samples]]
        dataset.sample_ids = sample_ids
        for attr in ("joint_dataset", "camera_dataset", "human_dataset", "caption_dataset"):
            sub = getattr(dataset, attr, None)
            if sub is not None and hasattr(sub, "sample_ids"):
                sub.sample_ids = sample_ids
    if args.expected_samples > 0 and len(dataset) != args.expected_samples:
        raise ValueError(f"evaluation split has {len(dataset)} samples, expected {args.expected_samples}")
    expected_ids = [str(value) for value in dataset.sample_ids]
    if len(expected_ids) != len(set(expected_ids)):
        raise ValueError("evaluation split sample IDs must be unique")

    local_spec = parse_model_spec(args.local_model)
    run_config = load_checkpoint_run_config(local_spec.checkpoint)
    if not run_config:
        raise FileNotFoundError(f"missing run_config.json for {local_spec.checkpoint}")
    local_feature_contract = str(run_config.get("feature_contract", ""))
    if local_feature_contract not in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}:
        raise ValueError(
            "long-sequence geometry requires an official camera14 checkpoint with human199 or v8.2 human200"
        )
    local_true_source = f"{local_spec.name}_true_length"
    local_fixed_source = f"{local_spec.name}_fixed_max"
    if args.official_checkpoint_override is not None and args.official_source_label == "pulp_official":
        raise ValueError("--official-source-label must identify a checkpoint override; do not label it pulp_official")
    if not args.official_source_label or not all(
        character.isalnum() or character in "_-" for character in args.official_source_label
    ):
        raise ValueError("--official-source-label must contain only letters, digits, underscores, or hyphens")
    official_true_source = f"{args.official_source_label}_true_length"
    official_fixed_source = f"{args.official_source_label}_fixed_max"
    local_model = build_model(local_spec, str(device), args.human200_stats).eval()
    if getattr(local_model, "is_causal", None) is not False:
        raise RuntimeError("long-sequence mainline diagnostic requires the non-causal local tokenizer")
    official_model = instantiate(cfg.model.autoencoder)
    if args.official_checkpoint_override is None:
        official_model.load_checkpoint()
        official_checkpoint = Path(official_model.autoaligner.checkpoint_path).resolve()
        official_checkpoint_policy = "cfg.model.autoencoder.load_checkpoint"
    else:
        official_checkpoint = args.official_checkpoint_override.resolve()
        if not official_checkpoint.is_file():
            raise FileNotFoundError(f"missing autoencoder checkpoint override: {official_checkpoint}")
        state_dict = torch.load(official_checkpoint, map_location="cpu", weights_only=True)
        official_model.autoaligner.load_state_dict(state_dict, strict=True)
        official_checkpoint_policy = "explicit autoaligner state_dict override"
    official_model.to(device).eval()
    if not official_checkpoint.is_file():
        raise FileNotFoundError(f"missing official autoencoder checkpoint: {official_checkpoint}")
    official_stats = _load_official_stats(args.pulp_root)
    human200_stats = getattr(local_model, "human200_stats", None)

    human_rows = load_rows_by_id(args.human_manifest)
    camera_rows = load_rows_by_id(args.camera_manifest)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=args.workers,
        pin_memory=device.type == "cuda",
    )
    feature_dataset = getattr(dataset, "joint_dataset", None) or dataset
    rows: list[dict[str, Any]] = []
    processed_ids: list[str] = []
    processed = 0
    started = time.time()
    with torch.inference_mode():
        for batch_index, batch in enumerate(loader):
            batch_device = {key: move_to_device(value, device) for key, value in batch.items() if key != "x_raw"}
            batch_device["x_raw"] = move_to_device(batch["x_raw"], device)
            padding_mask = batch_device["padding_mask"].bool()
            intrinsics = batch_device["x_raw"]["intrinsics"]
            x_input = dataset.get_feat(batch_device["x_raw"], padding_mask)
            raw_input = dataset.get_raw(x_input, intrinsics)
            sample_ids = [str(value) for value in batch["sample_id"]]
            processed_ids.extend(sample_ids)

            local_human, local_camera, _ = reconstruct_batch(
                local_model,
                local_spec,
                sample_ids,
                padding_mask,
                human_rows,
                camera_rows,
                args.camera_manifest,
                device,
                local_feature_contract,
                x_input,
                official_stats,
            )
            local_raw = feature_dataset.get_raw(
                {"human": local_human, "camera": local_camera},
                intrinsics,
            )
            oracle_raw: dict[str, dict[str, Any]] = {}
            oracle_human_features: dict[str, torch.Tensor] = {}
            if args.human_channel_oracles:
                if local_human.shape[-1] != 199 or x_input["human"].shape[-1] != 199:
                    raise RuntimeError("human channel oracle audit requires normalized Pulp human199 features")
                for oracle_name, (start, end) in HUMAN199_CHANNEL_ORACLES.items():
                    oracle_human = local_human.clone()
                    oracle_human[..., start:end] = x_input["human"][..., start:end]
                    oracle_human_features[oracle_name] = oracle_human
                    oracle_raw[oracle_name] = feature_dataset.get_raw(
                        {"human": oracle_human, "camera": local_camera},
                        intrinsics,
                    )
            official_features = official_reconstruct_true_length(official_model, x_input, padding_mask)
            official_raw = dataset.get_raw(official_features, intrinsics)
            local_fixed_features = reconstruct_fixed_length(
                local_model,
                x_input,
                padding_mask,
                args.fixed_max_frames,
                official=False,
                feature_contract=local_feature_contract,
                official_stats=official_stats,
                human200_stats=human200_stats,
            )
            local_fixed_raw = feature_dataset.get_raw(local_fixed_features, intrinsics)
            official_fixed_features = reconstruct_fixed_length(
                official_model,
                x_input,
                padding_mask,
                args.fixed_max_frames,
                official=True,
            )
            official_fixed_raw = dataset.get_raw(official_fixed_features, intrinsics)

            target_yaw = integrated_yaw_from_official_human199(x_input["human"], official_stats)
            local_true_yaw = integrated_yaw_from_official_human199(local_human, official_stats)
            local_fixed_yaw = integrated_yaw_from_official_human199(
                local_fixed_features["human"], official_stats
            )
            official_true_yaw = integrated_yaw_from_official_human199(
                official_features["human"], official_stats
            )
            official_fixed_yaw = integrated_yaw_from_official_human199(
                official_fixed_features["human"], official_stats
            )
            oracle_yaw = {
                name: integrated_yaw_from_official_human199(
                    oracle_human_features[name],
                    official_stats,
                )
                for name in HUMAN199_CHANNEL_ORACLES
            } if args.human_channel_oracles else {}

            for index, sample_id in enumerate(sample_ids):
                frames = int(padding_mask[index].sum().item())
                rows.append(
                    geometry_row(
                        local_true_source,
                        sample_id,
                        frames,
                        local_raw,
                        raw_input,
                        local_true_yaw,
                        target_yaw,
                        index,
                    )
                )
                for oracle_name, oracle_value in oracle_raw.items():
                    rows.append(
                        geometry_row(
                            oracle_name,
                            sample_id,
                            frames,
                            oracle_value,
                            raw_input,
                            oracle_yaw[oracle_name],
                            target_yaw,
                            index,
                        )
                    )
                rows.append(
                    geometry_row(
                        local_fixed_source,
                        sample_id,
                        frames,
                        local_fixed_raw,
                        raw_input,
                        local_fixed_yaw,
                        target_yaw,
                        index,
                    )
                )
                rows.append(
                    geometry_row(
                        official_true_source,
                        sample_id,
                        frames,
                        official_raw,
                        raw_input,
                        official_true_yaw,
                        target_yaw,
                        index,
                    )
                )
                rows.append(
                    geometry_row(
                        official_fixed_source,
                        sample_id,
                        frames,
                        official_fixed_raw,
                        raw_input,
                        official_fixed_yaw,
                        target_yaw,
                        index,
                    )
                )
            processed += len(sample_ids)
            if args.progress_every > 0 and ((batch_index + 1) % args.progress_every == 0 or processed == len(dataset)):
                elapsed = time.time() - started
                rate = processed / max(elapsed, 1e-9)
                print(
                    json.dumps(
                        {
                            "processed": processed,
                            "target": len(dataset),
                            "elapsed_sec": elapsed,
                            "eta_sec": (len(dataset) - processed) / max(rate, 1e-9),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    if processed_ids != expected_ids:
        raise RuntimeError("evaluation loader did not preserve the complete ordered split")
    if args.expected_samples > 0 and len(processed_ids) != args.expected_samples:
        raise RuntimeError(f"processed {len(processed_ids)} samples, expected {args.expected_samples}")

    sources = (
        local_true_source,
        *(HUMAN199_CHANNEL_ORACLES if args.human_channel_oracles else ()),
        local_fixed_source,
        official_true_source,
        official_fixed_source,
    )
    by_source = {source: [row for row in rows if row["source"] == source] for source in sources}

    def paired_delta(minuend: str, subtrahend: str) -> tuple[dict[str, float], dict[str, Any]]:
        left = {row["sample_id"]: row for row in by_source[minuend]}
        right = {row["sample_id"]: row for row in by_source[subtrahend]}
        delta_rows = [
            {
                "sample_id": sample_id,
                "frames": left[sample_id]["frames"],
                **{metric: left[sample_id][metric] - right[sample_id][metric] for metric in METRICS},
            }
            for sample_id in left
        ]
        return mean_metrics(delta_rows), summarize_source(delta_rows)

    comparisons = {}
    for label, minuend, subtrahend in (
        ("local_fixed_minus_true", local_fixed_source, local_true_source),
        ("official_fixed_minus_true", official_fixed_source, official_true_source),
        ("true_local_minus_official", local_true_source, official_true_source),
        ("fixed_local_minus_official", local_fixed_source, official_fixed_source),
    ):
        overall, summary = paired_delta(minuend, subtrahend)
        comparisons[label] = {
            "minuend": minuend,
            "subtrahend": subtrahend,
            "overall": overall,
            "summary": summary,
        }
    if args.human_channel_oracles:
        for oracle_name in HUMAN199_CHANNEL_ORACLES:
            overall, summary = paired_delta(oracle_name, local_true_source)
            comparisons[f"{oracle_name}_minus_local_true"] = {
                "minuend": oracle_name,
                "subtrahend": local_true_source,
                "overall": overall,
                "summary": summary,
            }
    payload = {
        "schema_version": 2,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "purpose": "full valid-length Stage1 reconstruction geometry versus sequence length",
        "data": {"set_name": args.set_name, "split": args.split, "samples": processed},
        "metric_units": {
            "human_root_aligned_mpjpe": "meters",
            "human_global_mpjpe": "meters",
            "human_root_ade": "meters",
            "human_root_fde": "meters",
            "human_integrated_yaw_geodesic": "degrees",
            "camera_center_ade": "meters",
            "camera_center_fde": "meters",
            "camera_rotation_deg": "degrees",
        },
        "inference_policy": {
            "true_length": (
                "Each sample is encoded and decoded once at its entire valid length; no crop, tiling, or "
                "sliding window is used. Pulp official inputs are right-padded only to the autoencoder stride."
            ),
            "fixed_max": (
                f"Each sample is right-padded with normalized-feature zeros to exactly {args.fixed_max_frames} "
                "frames before one encode/decode pass; metrics use only the original valid frames."
            ),
            "truncation": "forbidden; this audit fails if any valid sequence exceeds fixed_max_frames",
        },
        "human_channel_oracles": {
            "enabled": bool(args.human_channel_oracles),
            "feature_space": "normalized_pulpmotion_human199",
            "layout": "root_z[0], local_root_xy_velocity[1:3], yaw_velocity[3], pose6d[4:136], local_joints[136:199]",
            "replacement_ranges": {
                name: [start, end] for name, (start, end) in HUMAN199_CHANNEL_ORACLES.items()
            },
            "interpretation": (
                "Each oracle changes only the declared reconstructed feature channels before the owning decoder. "
                "It attributes error sensitivity and is not a trainable representation result."
            ),
        },
        "local": {
            "model": local_spec.name,
            "preset": local_spec.preset,
            "checkpoint": str(local_spec.checkpoint),
            "checkpoint_sha256": sha256_file(local_spec.checkpoint),
            "is_causal": False,
            "run_config": {
                "synthetic": run_config.get("synthetic"),
                "seq_len_field": run_config.get("seq_len"),
                "feature_contract": run_config.get("feature_contract"),
                "batch_size": run_config.get("batch_size"),
                "epochs": run_config.get("epochs"),
            },
            "human200_normalization": (
                {
                    "path": str(human200_stats["path"]),
                    "sha256": human200_stats["sha256"],
                    "source_manifest_sha256": human200_stats["meta"]["source"]["manifest_sha256"],
                    "source_sample_ids_sha256": human200_stats["meta"]["source"]["sample_ids_sha256"],
                    "source_split": human200_stats["meta"]["source"]["split"],
                }
                if human200_stats is not None
                else None
            ),
        },
        "official": {
            "source_label": args.official_source_label,
            "checkpoint_policy": official_checkpoint_policy,
            "model_dir": str(args.model_dir),
            "checkpoint": str(official_checkpoint),
            "checkpoint_sha256": sha256_file(official_checkpoint),
        },
        "summary": {source: summarize_source(source_rows) for source, source_rows in by_source.items()},
        "paired_comparisons": comparisons,
        "records": rows,
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "elapsed_sec": time.time() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "samples": processed}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
