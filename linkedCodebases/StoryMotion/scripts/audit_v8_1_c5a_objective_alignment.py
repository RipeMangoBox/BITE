#!/usr/bin/env python3
"""Audit whether a multi-horizon Human surrogate aligns better with the C3-25 evaluator failure."""
from __future__ import annotations

import argparse
from functools import partial
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader, Subset


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.calibrate_v8_1_c4_geometry_aux import (  # noqa: E402
    cosine,
    encoder_parameter_groups,
    objective_gradients,
)
from scripts.render_stage1_joint_separate_3d_reconstructions import (  # noqa: E402
    build_model,
    parse_model_spec,
)
from storymotion.training.joint_data import (  # noqa: E402
    OFFICIAL_FEATURE_CONTRACT,
    PairedPulpMotionHumanCameraDataset,
    _load_official_stats,
    collate_human_camera_batch,
)


ANCHOR_FRACTIONS = (0.25, 0.50, 0.75, 1.00)
HUMAN_YAW_WEIGHT = 0.001
HUMAN_ROOT_WEIGHT = 0.003
CAMERA_CENTER_WEIGHT = 0.0010166945703219975
TARGET_GRADIENT_FRACTION = 0.0125
MIN_CORRELATION_DELTA = 0.02
CAMERA_COSINE_DELTA_FLOOR = -0.05
PRIMARY_METRIC = "human_global_mpjpe"
METRICS = (
    "human_global_mpjpe",
    "human_root_ade",
    "human_root_fde",
    "human_integrated_yaw_geodesic",
)
LENGTH_BINS = (("1-64", 1, 64), ("65-128", 65, 128), ("129-192", 129, 192), ("193+", 193, None))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_ids_sha256(sample_ids: list[str]) -> str:
    return hashlib.sha256(("\n".join(sample_ids) + "\n").encode("utf-8")).hexdigest()


def evaluator_order_indices(manifest_ids: list[str], evaluator_ids: list[str]) -> list[int]:
    if len(manifest_ids) != len(set(manifest_ids)) or len(evaluator_ids) != len(set(evaluator_ids)):
        raise RuntimeError("manifest and evaluator sample IDs must each be unique")
    if set(manifest_ids) != set(evaluator_ids):
        raise RuntimeError("manifest and evaluator sample ID sets differ")
    manifest_index = {sample_id: index for index, sample_id in enumerate(manifest_ids)}
    return [manifest_index[sample_id] for sample_id in evaluator_ids]


def anchor_indices(length: int) -> tuple[int, ...]:
    if length <= 0:
        raise ValueError("length must be positive")
    return tuple(math.floor((length - 1) * fraction) for fraction in ANCHOR_FRACTIONS)


def surrogate_values_from_decoded(
    target_yaw: torch.Tensor,
    target_root: torch.Tensor,
    recon_yaw: torch.Tensor,
    recon_root: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return current last-valid and candidate four-anchor values for one unpadded sample."""
    if target_yaw.ndim != 1 or recon_yaw.shape != target_yaw.shape:
        raise ValueError("yaw tensors must be matching [T]")
    if target_root.shape != recon_root.shape or target_root.ndim != 2 or target_root.shape[1] != 3:
        raise ValueError("root tensors must be matching [T,3]")
    indices = torch.tensor(anchor_indices(target_yaw.shape[0]), device=target_yaw.device)
    yaw_error = 1.0 - torch.cos(recon_yaw - target_yaw)
    current = (
        HUMAN_YAW_WEIGHT * yaw_error[-1]
        + HUMAN_ROOT_WEIGHT * F.smooth_l1_loss(recon_root[-1], target_root[-1])
    )
    candidate = (
        HUMAN_YAW_WEIGHT * yaw_error[indices].mean()
        + HUMAN_ROOT_WEIGHT * F.smooth_l1_loss(recon_root[indices], target_root[indices])
    )
    return current, candidate


def batch_surrogates(
    model: torch.nn.Module,
    human: torch.Tensor,
    human_recon: torch.Tensor,
    lengths: torch.Tensor,
) -> tuple[torch.Tensor, torch.Tensor]:
    target = model._decoded_human_yaw_root(human)
    recon = model._decoded_human_yaw_root(human_recon)
    if target is None or recon is None:
        raise RuntimeError("model has no decoded Human yaw/root geometry")
    target_yaw, target_root = target
    recon_yaw, recon_root = recon
    current_values = []
    candidate_values = []
    for index, length_value in enumerate(lengths.tolist()):
        length = int(length_value)
        current, candidate = surrogate_values_from_decoded(
            target_yaw[index, :length],
            target_root[index, :length],
            recon_yaw[index, :length],
            recon_root[index, :length],
        )
        current_values.append(current)
        candidate_values.append(candidate)
    return torch.stack(current_values).mean(), torch.stack(candidate_values).mean()


def rankdata(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all():
        raise ValueError("rankdata requires a non-empty finite vector")
    order = np.argsort(values, kind="mergesort")
    sorted_values = values[order]
    ranks = np.empty(values.size, dtype=np.float64)
    start = 0
    while start < values.size:
        end = start + 1
        while end < values.size and sorted_values[end] == sorted_values[start]:
            end += 1
        ranks[order[start:end]] = 0.5 * (start + end - 1)
        start = end
    return ranks


def correlation(first: np.ndarray, second: np.ndarray) -> float:
    first = np.asarray(first, dtype=np.float64)
    second = np.asarray(second, dtype=np.float64)
    if first.shape != second.shape or first.ndim != 1 or first.size < 2:
        raise ValueError("correlation requires matching vectors with at least two values")
    first = first - first.mean()
    second = second - second.mean()
    denominator = np.linalg.norm(first) * np.linalg.norm(second)
    if denominator == 0.0:
        raise ValueError("correlation is undefined for a constant vector")
    return float(np.dot(first, second) / denominator)


def spearman(first: np.ndarray, second: np.ndarray) -> float:
    return correlation(rankdata(first), rankdata(second))


def paired_rank_bootstrap(
    current: np.ndarray,
    candidate: np.ndarray,
    target: np.ndarray,
    *,
    seed: int,
    samples: int,
) -> dict[str, float]:
    if samples <= 0:
        raise ValueError("bootstrap samples must be positive")
    current_rank = rankdata(current)
    candidate_rank = rankdata(candidate)
    target_rank = rankdata(target)
    rng = np.random.default_rng(seed)
    deltas = np.empty(samples, dtype=np.float64)
    for index in range(samples):
        draw = rng.integers(0, current_rank.size, size=current_rank.size)
        deltas[index] = correlation(candidate_rank[draw], target_rank[draw]) - correlation(
            current_rank[draw], target_rank[draw]
        )
    point = spearman(candidate, target) - spearman(current, target)
    return {
        "point_delta": point,
        "ci95_lower": float(np.quantile(deltas, 0.025)),
        "ci95_upper": float(np.quantile(deltas, 0.975)),
        "samples": samples,
        "seed": seed,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--human-manifest", type=Path, required=True)
    parser.add_argument("--camera-manifest", type=Path, required=True)
    parser.add_argument("--human-root", type=Path)
    parser.add_argument("--camera-root", type=Path)
    parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--geometry-report", type=Path, required=True)
    parser.add_argument("--geometry-source", required=True)
    parser.add_argument("--preset", default="pulpmotion_joint_ae_official_199_14_pulp192")
    parser.add_argument("--expected-samples", type=int, default=4053)
    parser.add_argument("--gradient-samples", type=int, default=64)
    parser.add_argument("--gradient-batch-size", type=int, default=8)
    parser.add_argument("--bootstrap-samples", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--progress-every", type=int, default=200)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def configure_geometry(model: torch.nn.Module, pulp_root: Path) -> None:
    stats = _load_official_stats(pulp_root)
    model.human_yaw_weight = HUMAN_YAW_WEIGHT
    model.human_root_weight = HUMAN_ROOT_WEIGHT
    model.camera_center_weight = CAMERA_CENTER_WEIGHT
    model.camera_rotation_weight = 0.0
    model.human_horizon_weight = 0.0
    model.geometry_human_mean = stats["human_mean"]
    model.geometry_human_std = stats["human_std"]
    model.geometry_feature_contract = "human199_integrated_root_yaw"
    model.geometry_camera_velocity_mean = stats["velocity_mean"]
    model.geometry_camera_velocity_std = stats["velocity_std"]
    model.geometry_camera_distance_mean = stats["distance_mean"]
    model.geometry_camera_distance_std = stats["distance_std"]


def metric_correlations(records: list[dict[str, Any]], indices: np.ndarray) -> dict[str, dict[str, float]]:
    current = np.array([records[index]["surrogate"]["current_last_valid"] for index in indices])
    candidate = np.array([records[index]["surrogate"]["candidate_multi_horizon"] for index in indices])
    result: dict[str, dict[str, float]] = {}
    for metric in METRICS:
        target = np.array([records[index]["evaluator"][metric] for index in indices])
        current_value = spearman(current, target)
        candidate_value = spearman(candidate, target)
        result[metric] = {
            "current_last_valid_spearman": current_value,
            "candidate_multi_horizon_spearman": candidate_value,
            "candidate_minus_current": candidate_value - current_value,
        }
    return result


def main() -> int:
    args = parse_args()
    if args.expected_samples <= 0 or args.gradient_samples <= 0 or args.gradient_batch_size <= 0:
        raise ValueError("sample counts and gradient batch size must be positive")
    if args.gradient_samples % args.gradient_batch_size:
        raise ValueError("gradient-samples must be divisible by gradient-batch-size")
    for path in (args.human_manifest, args.camera_manifest, args.checkpoint, args.geometry_report):
        if not path.is_file():
            raise FileNotFoundError(path)

    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    device = torch.device(args.device)
    model_spec = parse_model_spec(f"{args.run_id}:{args.preset}:{args.checkpoint}")
    model = build_model(model_spec, str(device)).eval()
    if getattr(model, "is_causal", None) is not False:
        raise RuntimeError("C5-A requires a non-causal StoryMotion Stage1 checkpoint")
    configure_geometry(model, args.pulp_root)

    report = json.loads(args.geometry_report.read_text(encoding="utf-8"))
    evaluator_records = [record for record in report["records"] if record["source"] == args.geometry_source]
    if len(evaluator_records) != args.expected_samples:
        raise RuntimeError(
            f"geometry source has {len(evaluator_records)} records, expected {args.expected_samples}"
        )
    evaluator_ids = [str(record["sample_id"]) for record in evaluator_records]
    if len(evaluator_ids) != len(set(evaluator_ids)):
        raise RuntimeError("geometry source sample IDs are not unique")

    dataset = PairedPulpMotionHumanCameraDataset(
        args.human_manifest,
        args.camera_manifest,
        human_root=args.human_root,
        camera_root=args.camera_root,
        feature_contract=OFFICIAL_FEATURE_CONTRACT,
        pulp_root=args.pulp_root,
    )
    dataset_ids = [str(human.get("sample_id") or "") for human, _ in dataset.records]
    evaluator_dataset_indices = evaluator_order_indices(dataset_ids, evaluator_ids)

    records: list[dict[str, Any]] = []
    started = time.time()
    with torch.inference_mode():
        for index, dataset_index in enumerate(evaluator_dataset_indices):
            item = dataset[dataset_index]
            sample_id = str(item["sample_id"])
            expected = evaluator_records[index]
            length = int(item["lengths"])
            if sample_id != str(expected["sample_id"]) or length != int(expected["frames"]):
                raise RuntimeError(f"sample identity/length mismatch at index {index}")
            human = item["human"].unsqueeze(0).to(device)
            camera = item["camera"].unsqueeze(0).to(device)
            output = model(human, camera)
            target = model._decoded_human_yaw_root(human)
            recon = model._decoded_human_yaw_root(output.human_recon[:, :length])
            if target is None or recon is None:
                raise RuntimeError("model has no decoded Human geometry")
            current, candidate = surrogate_values_from_decoded(
                target[0][0, :length],
                target[1][0, :length],
                recon[0][0, :length],
                recon[1][0, :length],
            )
            records.append(
                {
                    "sample_id": sample_id,
                    "frames": length,
                    "anchors": list(anchor_indices(length)),
                    "surrogate": {
                        "current_last_valid": float(current.item()),
                        "candidate_multi_horizon": float(candidate.item()),
                    },
                    "evaluator": {metric: float(expected[metric]) for metric in METRICS},
                }
            )
            processed = index + 1
            if args.progress_every > 0 and (processed % args.progress_every == 0 or processed == len(dataset)):
                elapsed = time.time() - started
                eta = elapsed * (len(dataset) - processed) / processed
                print(json.dumps({"processed": processed, "target": len(dataset), "elapsed_sec": elapsed, "eta_sec": eta}), flush=True)

    all_indices = np.arange(len(records))
    group_indices: dict[str, np.ndarray] = {"all": all_indices}
    for label, lower, upper in LENGTH_BINS:
        group_indices[label] = np.array(
            [
                index
                for index, record in enumerate(records)
                if int(record["frames"]) >= lower and (upper is None or int(record["frames"]) <= upper)
            ],
            dtype=np.int64,
        )
    if group_indices["193+"].size != 381:
        raise RuntimeError(f"193+ subset has {group_indices['193+'].size} samples, expected 381")
    correlations = {name: metric_correlations(records, indices) for name, indices in group_indices.items()}

    alignment_gates = {}
    for name in ("all", "193+"):
        indices = group_indices[name]
        current = np.array([records[index]["surrogate"]["current_last_valid"] for index in indices])
        candidate = np.array([records[index]["surrogate"]["candidate_multi_horizon"] for index in indices])
        target = np.array([records[index]["evaluator"][PRIMARY_METRIC] for index in indices])
        bootstrap = paired_rank_bootstrap(
            current,
            candidate,
            target,
            seed=args.seed,
            samples=args.bootstrap_samples,
        )
        bootstrap["minimum_point_delta"] = MIN_CORRELATION_DELTA
        bootstrap["passed"] = (
            bootstrap["point_delta"] >= MIN_CORRELATION_DELTA and bootstrap["ci95_lower"] > 0.0
        )
        alignment_gates[name] = bootstrap

    long_ids = [records[index]["sample_id"] for index in group_indices["193+"][: args.gradient_samples]]
    id_to_index = {sample_id: index for index, sample_id in enumerate(dataset_ids)}
    gradient_subset = Subset(dataset, [id_to_index[sample_id] for sample_id in long_ids])
    gradient_loader = DataLoader(
        gradient_subset,
        batch_size=args.gradient_batch_size,
        shuffle=False,
        num_workers=0,
        collate_fn=partial(collate_human_camera_batch, fixed_max_frames=0),
    )
    parameter_groups = encoder_parameter_groups(model)
    objective_names = (
        "c3_25_parent",
        "human_geometry",
        "camera_center_weight_1",
        "camera_rotation_weight_1",
        "current_last_valid_weight_1",
        "candidate_multi_horizon_weight_1",
    )
    gradient_records = []
    for batch_index, batch in enumerate(gradient_loader):
        human = batch["human"].to(device)
        camera = batch["camera"].to(device)
        lengths = batch["lengths"].to(device)
        mask = torch.arange(human.shape[1], device=device)[None] < lengths[:, None]
        output = model(human, camera)
        losses = model._branch_reconstruction_losses(human, camera, output, mask)
        current, candidate = batch_surrogates(model, human, output.human_recon, lengths)
        human_geometry = losses["weighted_human_yaw_loss"] + losses["weighted_human_root_loss"]
        objectives = {
            "human_geometry": human_geometry,
            "camera_center_weight_1": model._camera_center_geometry_loss(
                human, camera, output.human_recon, output.camera_recon, mask
            ),
            "camera_rotation_weight_1": model._camera_rotation_geometry_loss(camera, output.camera_recon, mask),
            "current_last_valid_weight_1": current,
            "candidate_multi_horizon_weight_1": candidate,
        }
        objectives["c3_25_parent"] = (
            losses["weighted_human_recon_loss"]
            + losses["weighted_human_velocity_loss"]
            + losses["weighted_human_acceleration_loss"]
            + losses["weighted_camera_recon_loss"]
            + losses["weighted_camera_velocity_loss"]
            + losses["weighted_camera_acceleration_loss"]
            + human_geometry
            + losses["weighted_camera_center_loss"]
        )
        gradients = {
            name: objective_gradients(objectives[name], parameter_groups)
            for name in objective_names
        }
        aggregate_norms = {
            name: float(torch.linalg.vector_norm(gradients[name]["encoder.all"]).item())
            for name in objective_names
        }
        pairs = {}
        for surrogate_name in ("current_last_valid_weight_1", "candidate_multi_horizon_weight_1"):
            for reference_name in (
                "c3_25_parent",
                "human_geometry",
                "camera_center_weight_1",
                "camera_rotation_weight_1",
            ):
                pairs[f"{surrogate_name}__vs__{reference_name}"] = cosine(
                    gradients[surrogate_name]["encoder.all"], gradients[reference_name]["encoder.all"]
                )
        gradient_records.append(
            {
                "batch_index": batch_index,
                "sample_ids": [str(value) for value in batch["sample_id"]],
                "aggregate_gradient_norm": aggregate_norms,
                "aggregate_gradient_cosine": pairs,
            }
        )
        model.zero_grad(set_to_none=True)

    median_norms = {
        name: statistics.median(record["aggregate_gradient_norm"][name] for record in gradient_records)
        for name in objective_names
    }
    cosine_keys = tuple(gradient_records[0]["aggregate_gradient_cosine"])
    median_cosines = {
        key: statistics.median(record["aggregate_gradient_cosine"][key] for record in gradient_records)
        for key in cosine_keys
    }
    camera_guards = {}
    for reference in ("camera_center_weight_1", "camera_rotation_weight_1"):
        current_key = f"current_last_valid_weight_1__vs__{reference}"
        candidate_key = f"candidate_multi_horizon_weight_1__vs__{reference}"
        delta = median_cosines[candidate_key] - median_cosines[current_key]
        camera_guards[reference] = {
            "current_cosine": median_cosines[current_key],
            "candidate_cosine": median_cosines[candidate_key],
            "candidate_minus_current": delta,
            "minimum_delta": CAMERA_COSINE_DELTA_FLOOR,
            "passed": delta >= CAMERA_COSINE_DELTA_FLOOR,
        }
    gradient_finite = all(
        math.isfinite(value)
        for value in list(median_norms.values()) + list(median_cosines.values())
    )
    gradient_gate = {
        "finite": gradient_finite,
        "candidate_nonzero": median_norms["candidate_multi_horizon_weight_1"] > 0.0,
        "camera_guards": camera_guards,
    }
    gradient_gate["passed"] = (
        gradient_gate["finite"]
        and gradient_gate["candidate_nonzero"]
        and all(item["passed"] for item in camera_guards.values())
    )
    alignment_passed = all(item["passed"] for item in alignment_gates.values())
    supported = alignment_passed and gradient_gate["passed"]

    payload = {
        "schema_version": 1,
        "run_id": args.run_id,
        "status": "audited",
        "decision": "candidate_supported_for_screen_preregistration" if supported else "candidate_not_supported",
        "training_authorized": False,
        "representation": OFFICIAL_FEATURE_CONTRACT,
        "causality": "non_causal",
        "source": {
            "checkpoint": str(args.checkpoint.resolve()),
            "checkpoint_sha256": sha256_file(args.checkpoint),
            "geometry_report": str(args.geometry_report.resolve()),
            "geometry_report_sha256": sha256_file(args.geometry_report),
            "geometry_source": args.geometry_source,
            "human_manifest": str(args.human_manifest.resolve()),
            "human_manifest_sha256": sha256_file(args.human_manifest),
            "camera_manifest": str(args.camera_manifest.resolve()),
            "camera_manifest_sha256": sha256_file(args.camera_manifest),
            "manifest_ordered_sample_ids_sha256": ordered_ids_sha256(dataset_ids),
            "evaluator_ordered_sample_ids_sha256": ordered_ids_sha256(evaluator_ids),
            "identity_set_equal": True,
            "execution_order": "evaluator record order via explicit sample_id-to-manifest-index mapping",
            "script_sha256": sha256_file(Path(__file__)),
        },
        "method": {
            "anchor_fractions": list(ANCHOR_FRACTIONS),
            "anchor_index_rule": "floor((T - 1) * fraction), zero-based",
            "human_yaw_weight": HUMAN_YAW_WEIGHT,
            "human_root_weight": HUMAN_ROOT_WEIGHT,
            "primary_metric": PRIMARY_METRIC,
            "minimum_correlation_delta": MIN_CORRELATION_DELTA,
            "bootstrap": "paired resampling over within-group global rank scores",
            "camera_cosine_delta_floor": CAMERA_COSINE_DELTA_FLOOR,
        },
        "counts": {name: int(indices.size) for name, indices in group_indices.items()},
        "correlations": correlations,
        "alignment_gates": alignment_gates,
        "gradient": {
            "ordered_sample_ids": long_ids,
            "ordered_sample_ids_sha256": ordered_ids_sha256(long_ids),
            "batch_size": args.gradient_batch_size,
            "batches": len(gradient_records),
            "records": gradient_records,
            "median_aggregate_gradient_norm": median_norms,
            "median_aggregate_gradient_cosine": median_cosines,
            "candidate_weight_at_parent_fraction": (
                TARGET_GRADIENT_FRACTION
                * median_norms["c3_25_parent"]
                / median_norms["candidate_multi_horizon_weight_1"]
            ),
            "gate": gradient_gate,
        },
        "selection": {
            "alignment_passed": alignment_passed,
            "gradient_passed": gradient_gate["passed"],
            "supported_for_screen_preregistration": supported,
            "direct_training_authorized": False,
        },
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"decision": payload["decision"], "selection": payload["selection"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
