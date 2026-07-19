#!/usr/bin/env python3
"""Audit shared-encoder gradients and calibrate independent v8.1 C4/C5 auxiliaries."""
from __future__ import annotations

import argparse
from functools import partial
import hashlib
import json
from pathlib import Path
import statistics
import sys

import torch
from torch.utils.data import DataLoader


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.train_storymotion_joint_tokenizer import PRESETS
from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer
from storymotion.training.joint_data import (
    OFFICIAL_FEATURE_CONTRACT,
    PairedPulpMotionHumanCameraDataset,
    _load_official_stats,
    collate_human_camera_batch,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample_ids_sha256(sample_ids: list[str]) -> str:
    return hashlib.sha256(("\n".join(sample_ids) + "\n").encode("utf-8")).hexdigest()


def encoder_parameter_groups(model: torch.nn.Module) -> dict[str, list[torch.nn.Parameter]]:
    groups: dict[str, list[torch.nn.Parameter]] = {}
    for name, parameter in model.named_parameters():
        if not name.startswith("encoder."):
            continue
        layer = ".".join(name.split(".")[:2])
        groups.setdefault(layer, []).append(parameter)
    if not groups:
        raise RuntimeError("model has no shared encoder parameters")
    groups["encoder.all"] = [parameter for name, parameter in model.named_parameters() if name.startswith("encoder.")]
    return groups


def objective_gradients(
    loss: torch.Tensor,
    groups: dict[str, list[torch.nn.Parameter]],
) -> dict[str, torch.Tensor]:
    unique_parameters = groups["encoder.all"]
    gradients = torch.autograd.grad(loss, unique_parameters, retain_graph=True, allow_unused=True)
    by_id = {id(parameter): gradient for parameter, gradient in zip(unique_parameters, gradients)}
    vectors: dict[str, torch.Tensor] = {}
    for layer, parameters in groups.items():
        pieces = []
        for parameter in parameters:
            gradient = by_id[id(parameter)]
            if gradient is None:
                pieces.append(torch.zeros_like(parameter).reshape(-1))
            else:
                pieces.append(gradient.detach().float().reshape(-1))
        vectors[layer] = torch.cat(pieces)
    return vectors


def cosine(first: torch.Tensor, second: torch.Tensor) -> float | None:
    denominator = torch.linalg.vector_norm(first) * torch.linalg.vector_norm(second)
    if float(denominator.item()) == 0.0:
        return None
    return float(torch.dot(first, second).div(denominator).item())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--human-manifest", type=Path, required=True)
    parser.add_argument("--camera-manifest", type=Path, required=True)
    parser.add_argument("--human-root", type=Path)
    parser.add_argument("--camera-root", type=Path)
    parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    parser.add_argument("--preset", default="pulpmotion_joint_ae_official_199_14_pulp192")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--batches", type=int, default=8)
    parser.add_argument("--fixed-max-frames", type=int, default=250)
    parser.add_argument("--human-yaw-weight", type=float, default=0.001)
    parser.add_argument("--human-root-weight", type=float, default=0.003)
    parser.add_argument("--camera-center-weight", type=float, default=0.0010166945703219975)
    parser.add_argument("--target-gradient-fraction", type=float, default=0.0125)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.preset not in PRESETS:
        raise KeyError(f"unknown preset: {args.preset}")
    if args.batch_size <= 0 or args.batches <= 0 or args.fixed_max_frames <= 0:
        raise ValueError("batch-size, batches, and fixed-max-frames must be positive")
    if not 0.0 < args.target_gradient_fraction <= 1.0:
        raise ValueError("target-gradient-fraction must be in (0, 1]")
    if min(args.human_yaw_weight, args.human_root_weight, args.camera_center_weight) < 0.0:
        raise ValueError("parent geometry weights must be non-negative")
    preset = dict(PRESETS[args.preset])
    if preset.pop("feature_contract", None) != OFFICIAL_FEATURE_CONTRACT:
        raise ValueError("C4 calibration requires normalized human199 plus official camera14")
    tokenizer = str(preset.pop("tokenizer"))
    if tokenizer != "joint_ae":
        raise ValueError("C4 calibration is restricted to the v8.1A joint AE")

    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    device = torch.device(args.device)
    stats = _load_official_stats(args.pulp_root)
    model = build_joint_human_camera_tokenizer(tokenizer, **preset).to(device).train()
    assert model.is_causal is False
    model.human_yaw_weight = float(args.human_yaw_weight)
    model.human_root_weight = float(args.human_root_weight)
    model.camera_center_weight = float(args.camera_center_weight)
    model.camera_rotation_weight = 0.0
    model.human_horizon_weight = 0.0
    model.human_multi_horizon_weight = 0.0
    model.geometry_human_mean = stats["human_mean"]
    model.geometry_human_std = stats["human_std"]
    model.geometry_feature_contract = "human199_integrated_root_yaw"
    model.geometry_camera_velocity_mean = stats["velocity_mean"]
    model.geometry_camera_velocity_std = stats["velocity_std"]
    model.geometry_camera_distance_mean = stats["distance_mean"]
    model.geometry_camera_distance_std = stats["distance_std"]
    parameter_groups = encoder_parameter_groups(model)

    dataset = PairedPulpMotionHumanCameraDataset(
        args.human_manifest,
        args.camera_manifest,
        human_root=args.human_root,
        camera_root=args.camera_root,
        feature_contract=OFFICIAL_FEATURE_CONTRACT,
        pulp_root=args.pulp_root,
    )
    collate = partial(collate_human_camera_batch, fixed_max_frames=args.fixed_max_frames)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False, num_workers=0, collate_fn=collate)
    objective_names = (
        "human_feature",
        "camera_reconstruction",
        "camera_velocity",
        "human_geometry",
        "camera_center_parent",
        "camera_rotation_weight_1",
        "human_horizon_weight_1",
        "human_multi_horizon_weight_1",
        "c3_25_parent",
    )
    records = []
    for batch_index, batch in enumerate(loader):
        if batch_index >= args.batches:
            break
        human = batch["human"].to(device)
        camera = batch["camera"].to(device)
        lengths = batch["lengths"].to(device)
        mask = torch.arange(human.shape[1], device=device)[None] < lengths[:, None]
        output = model(human, camera)
        losses = model._branch_reconstruction_losses(human, camera, output, mask)
        horizon_yaw, horizon_root = model._human_horizon_geometry_losses(human, output.human_recon, mask)
        multi_yaw, multi_root = model._human_multi_horizon_geometry_losses(human, output.human_recon, mask)
        objectives = {
            "human_feature": (
                losses["weighted_human_recon_loss"]
                + losses["weighted_human_velocity_loss"]
                + losses["weighted_human_acceleration_loss"]
            ),
            "camera_reconstruction": losses["weighted_camera_recon_loss"],
            "camera_velocity": (
                losses["weighted_camera_velocity_loss"] + losses["weighted_camera_acceleration_loss"]
            ),
            "human_geometry": losses["weighted_human_yaw_loss"] + losses["weighted_human_root_loss"],
            "camera_center_parent": losses["weighted_camera_center_loss"],
            "camera_rotation_weight_1": model._camera_rotation_geometry_loss(camera, output.camera_recon, mask),
            "human_horizon_weight_1": (
                args.human_yaw_weight * horizon_yaw + args.human_root_weight * horizon_root
            ),
            "human_multi_horizon_weight_1": (
                args.human_yaw_weight * multi_yaw + args.human_root_weight * multi_root
            ),
        }
        objectives["c3_25_parent"] = sum(
            objectives[name]
            for name in (
                "human_feature",
                "camera_reconstruction",
                "camera_velocity",
                "human_geometry",
                "camera_center_parent",
            )
        )
        gradients = {
            name: objective_gradients(objectives[name], parameter_groups)
            for name in objective_names
        }
        norms = {
            name: {layer: float(torch.linalg.vector_norm(vector).item()) for layer, vector in layers.items()}
            for name, layers in gradients.items()
        }
        cosines: dict[str, dict[str, float | None]] = {}
        for first_index, first in enumerate(objective_names):
            for second in objective_names[first_index + 1 :]:
                cosines[f"{first}__vs__{second}"] = {
                    layer: cosine(gradients[first][layer], gradients[second][layer])
                    for layer in parameter_groups
                }
        sample_ids = [str(value) for value in batch["sample_id"]]
        records.append(
            {
                "batch_index": batch_index,
                "sample_ids_sha256": sample_ids_sha256(sample_ids),
                "valid_frames": int(mask.sum().item()),
                "loss": {name: float(objectives[name].detach().item()) for name in objective_names},
                "encoder_gradient_norm": norms,
                "encoder_gradient_cosine": cosines,
            }
        )
        model.zero_grad(set_to_none=True)
    if len(records) != args.batches:
        raise RuntimeError(f"requested {args.batches} batches, found only {len(records)}")

    median_norms = {
        name: {
            layer: statistics.median(record["encoder_gradient_norm"][name][layer] for record in records)
            for layer in parameter_groups
        }
        for name in objective_names
    }
    cosine_keys = tuple(records[0]["encoder_gradient_cosine"])
    median_cosines = {
        pair: {
            layer: statistics.median(
                value
                for record in records
                if (value := record["encoder_gradient_cosine"][pair][layer]) is not None
            )
            for layer in parameter_groups
        }
        for pair in cosine_keys
    }
    parent_norm = median_norms["c3_25_parent"]["encoder.all"]
    rotation_norm = median_norms["camera_rotation_weight_1"]["encoder.all"]
    horizon_norm = median_norms["human_horizon_weight_1"]["encoder.all"]
    multi_horizon_norm = median_norms["human_multi_horizon_weight_1"]["encoder.all"]
    if rotation_norm == 0.0 or horizon_norm == 0.0 or multi_horizon_norm == 0.0:
        raise RuntimeError("a C4/C5 raw auxiliary produced a zero shared-encoder gradient")
    recommendations = {
        "target_fraction_of_c3_25_parent_shared_encoder": args.target_gradient_fraction,
        "camera_rotation_weight": args.target_gradient_fraction * parent_norm / rotation_norm,
        "human_horizon_weight": args.target_gradient_fraction * parent_norm / horizon_norm,
        "human_multi_horizon_weight": args.target_gradient_fraction * parent_norm / multi_horizon_norm,
        "rule": "each arm independently targets target_fraction * median(parent encoder norm) / median(raw auxiliary encoder norm)",
    }
    payload = {
        "schema_version": 1,
        "purpose": "v8.1 C4/C5 shared-encoder gradient audit and independent auxiliary dose calibration",
        "representation": OFFICIAL_FEATURE_CONTRACT,
        "causality": "non_causal",
        "parent": {
            "family": "v8.1C C3-25",
            "human_yaw_weight": args.human_yaw_weight,
            "human_root_weight": args.human_root_weight,
            "camera_center_weight": args.camera_center_weight,
        },
        "source": {
            "human_manifest": str(args.human_manifest.resolve()),
            "human_manifest_sha256": sha256_file(args.human_manifest),
            "camera_manifest": str(args.camera_manifest.resolve()),
            "camera_manifest_sha256": sha256_file(args.camera_manifest),
            "pulp_root": str(args.pulp_root.resolve()),
            "stats": {
                name: {
                    "path": str((args.pulp_root / "configs/dataset/modality" / name).resolve()),
                    "sha256": sha256_file(args.pulp_root / "configs/dataset/modality" / name),
                }
                for name in ("char_smplrifke.yaml", "traj_raw.yaml", "traj+char+proj.yaml")
            },
            "script_sha256": sha256_file(Path(__file__)),
        },
        "args": {key: str(value) if isinstance(value, Path) else value for key, value in vars(args).items()},
        "encoder_layers": list(parameter_groups),
        "records": records,
        "median_encoder_gradient_norm": median_norms,
        "median_encoder_gradient_cosine": median_cosines,
        "recommendation": recommendations,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(recommendations, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
