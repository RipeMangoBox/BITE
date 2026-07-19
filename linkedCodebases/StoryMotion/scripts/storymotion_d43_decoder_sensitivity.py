#!/usr/bin/env python3
"""Audit D4 residual directions with owning-decoder JVP/VJP probes.

This diagnostic reconstructs the frozen D4 Direct-C single-step predictions,
then measures local decoded-camera sensitivity along the observed camera-latent
residual and one deterministic RMS-matched random direction.  It never trains,
writes a cache, or mutates a checkpoint.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

import storymotion_official_full_eval as full_eval
from storymotion_d4_raw_residual import (
    DEFAULT_TIMESTEPS,
    _read_jsonl,
    _write_json,
    _write_jsonl,
    scalar_summary,
    sha256_file,
    sha256_ids,
)
from storymotion_official_bridge_smoke import (
    batch_from_sample_ids,
    build_pulp,
    decode_with_owning_decoder,
    load_module,
    load_stage2,
    patch_numpy_aliases,
    reference_feature_and_raw,
    resolve_owning_decoder,
)


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR_NAME = "decoder_sensitivity"
JVP_FIELDS = (
    "camera_center_ade_gain_m",
    "camera_center_rms_gain_m",
    "camera_center_fde_gain_m",
    "camera_rotation_tangent_mean_deg",
    "camera_rotation_tangent_rms_deg",
    "camera_rotation_matrix_fro_rms",
)
VJP_OBJECTIVES = (
    "camera_center_ade_m",
    "camera_center_fde_m",
    "camera_rotation_mean_rad",
)
EPS = 1.0e-12
REPRODUCTION_ABS_TOLERANCES = {
    "decoder_input_residual_rms": 3.0e-4,
    "camera_center_ade": 5.0e-3,
    "camera_center_fde": 5.0e-3,
    "camera_rotation_deg": 5.0e-2,
}


def reproduction_failures(deltas: dict[str, float]) -> dict[str, float]:
    """Return replay deltas outside the predeclared cross-host envelope."""
    return {
        key: value
        for key, value in deltas.items()
        if value > REPRODUCTION_ABS_TOLERANCES[key]
    }


def latent_stats_file_audit(
    actual_sha256: str,
    parent_expected_sha256: str,
    accept_reserialized: bool,
) -> dict[str, str]:
    """Bind the file used by D4.3 while preserving a stale parent-file hash."""
    if actual_sha256 == parent_expected_sha256:
        status = "exact_parent_file_hash"
    elif accept_reserialized:
        status = "accepted_parent_reserialization_mismatch"
    else:
        raise RuntimeError(
            "latent stats file hash differs from the parent contract; "
            "a provenance amendment is required"
        )
    return {
        "path_status": status,
        "actual_sha256": actual_sha256,
        "parent_expected_sha256": parent_expected_sha256,
    }


def camera_directions(
    residual: torch.Tensor,
    valid: torch.Tensor,
    seeds: list[int],
) -> tuple[dict[str, torch.Tensor], torch.Tensor]:
    """Return unit-RMS actual and orthogonal random directions per sample."""
    if residual.ndim != 3 or valid.shape != (residual.shape[0], residual.shape[2]):
        raise ValueError("expected residual [B,C,T] and valid [B,T]")
    if len(seeds) != residual.shape[0]:
        raise ValueError("one deterministic random seed is required per sample")
    mask = valid[:, None, :].to(device=residual.device, dtype=residual.dtype)
    masked = residual * mask
    count = valid.sum(dim=1).to(residual.dtype) * residual.shape[1]
    rms = (masked.square().sum(dim=(1, 2)) / count.clamp_min(1.0)).sqrt()
    if bool((rms <= EPS).any()):
        raise ValueError("camera residual direction has zero RMS")
    actual = masked / rms[:, None, None]

    controls = []
    for index, seed in enumerate(seeds):
        generator = torch.Generator(device="cpu")
        generator.manual_seed(int(seed))
        control = torch.randn(
            residual.shape[1:], generator=generator, dtype=torch.float32, device="cpu"
        ).to(device=residual.device, dtype=residual.dtype)
        sample_mask = mask[index]
        control = control * sample_mask
        actual_sample = actual[index]
        projection = (control * actual_sample).sum() / actual_sample.square().sum().clamp_min(EPS)
        control = (control - projection * actual_sample) * sample_mask
        control_rms = (
            control.square().sum() / count[index].clamp_min(1.0)
        ).sqrt()
        if float(control_rms) <= EPS:
            raise ValueError("orthogonal random control has zero RMS")
        controls.append(control / control_rms)
    random_control = torch.stack(controls, dim=0)
    return {"actual_residual": actual, "random_orthogonal": random_control}, rms


def camera_geometry_objectives(
    prediction: torch.Tensor,
    reference: torch.Tensor,
    padding_mask: torch.Tensor,
) -> dict[str, torch.Tensor]:
    """Differentiable per-sample decoded camera objectives."""
    if prediction.shape != reference.shape or prediction.ndim != 4:
        raise ValueError("camera tensors must have equal [B,T,4,4] shapes")
    if padding_mask.shape != prediction.shape[:2]:
        raise ValueError("padding_mask must have shape [B,T]")
    mask = padding_mask.to(device=prediction.device, dtype=prediction.dtype)
    count = mask.sum(dim=1).clamp_min(1.0)
    center_error = torch.linalg.vector_norm(
        prediction[..., :3, 3] - reference[..., :3, 3], dim=-1
    )
    center_ade = (center_error * mask).sum(dim=1) / count
    last = (padding_mask.sum(dim=1) - 1).clamp_min(0).long()
    center_fde = center_error.gather(1, last[:, None]).squeeze(1)

    relative = prediction[..., :3, :3].transpose(-1, -2) @ reference[..., :3, :3]
    cosine = ((relative.diagonal(dim1=-2, dim2=-1).sum(-1) - 1.0) / 2.0).clamp(
        -1.0 + 1.0e-7, 1.0 - 1.0e-7
    )
    rotation = (torch.acos(cosine) * mask).sum(dim=1) / count
    return {
        "camera_center_ade_m": center_ade,
        "camera_center_fde_m": center_fde,
        "camera_rotation_mean_rad": rotation,
    }


def jvp_camera_metrics(
    base_camera: torch.Tensor,
    camera_jvp: torch.Tensor,
    padding_mask: torch.Tensor,
) -> list[dict[str, float]]:
    """Convert a raw-camera JVP into task-space gain metrics per sample."""
    if base_camera.shape != camera_jvp.shape or base_camera.ndim != 4:
        raise ValueError("base camera and JVP must have equal [B,T,4,4] shapes")
    records = []
    for index in range(base_camera.shape[0]):
        valid = padding_mask[index].bool()
        if int(valid.sum()) <= 0:
            raise ValueError("sample has no valid decoded frames")
        center = camera_jvp[index, valid, :3, 3]
        center_norm = torch.linalg.vector_norm(center, dim=-1)
        rotation = base_camera[index, valid, :3, :3]
        rotation_jvp = camera_jvp[index, valid, :3, :3]
        local = rotation.transpose(-1, -2) @ rotation_jvp
        skew = 0.5 * (local - local.transpose(-1, -2))
        omega = torch.stack(
            [skew[..., 2, 1], skew[..., 0, 2], skew[..., 1, 0]], dim=-1
        )
        angular = torch.linalg.vector_norm(omega, dim=-1)
        rotation_fro = torch.linalg.matrix_norm(rotation_jvp, ord="fro")
        records.append(
            {
                "camera_center_ade_gain_m": float(center_norm.mean().detach().cpu()),
                "camera_center_rms_gain_m": float(center_norm.square().mean().sqrt().detach().cpu()),
                "camera_center_fde_gain_m": float(center_norm[-1].detach().cpu()),
                "camera_rotation_tangent_mean_deg": float(torch.rad2deg(angular.mean()).detach().cpu()),
                "camera_rotation_tangent_rms_deg": float(
                    torch.rad2deg(angular.square().mean().sqrt()).detach().cpu()
                ),
                "camera_rotation_matrix_fro_rms": float(
                    rotation_fro.square().mean().sqrt().detach().cpu()
                ),
            }
        )
    return records


def gradient_alignment(
    gradient: torch.Tensor,
    direction: torch.Tensor,
    valid: torch.Tensor,
) -> list[dict[str, float]]:
    if gradient.shape != direction.shape:
        raise ValueError("gradient and direction shapes differ")
    mask = valid[:, None, :].to(device=gradient.device, dtype=gradient.dtype)
    records = []
    for index in range(gradient.shape[0]):
        grad = gradient[index] * mask[index]
        direct = direction[index] * mask[index]
        count = float(valid[index].sum().item() * gradient.shape[1])
        dot = (grad * direct).sum()
        grad_l2 = torch.linalg.vector_norm(grad)
        direct_l2 = torch.linalg.vector_norm(direct)
        cosine = dot / (grad_l2 * direct_l2).clamp_min(EPS)
        records.append(
            {
                "gradient_rms": float((grad.square().sum() / count).sqrt().detach().cpu()),
                "directional_derivative": float(dot.detach().cpu()),
                "directional_derivative_per_latent_element": float((dot / count).detach().cpu()),
                "cosine_to_actual_residual": float(cosine.detach().cpu()),
            }
        )
    return records


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        raise ValueError("cannot summarize empty D4.3 records")
    jvp = {
        direction: {
            field: scalar_summary(record["jvp"][direction][field] for record in records)
            for field in JVP_FIELDS
        }
        for direction in ("actual_residual", "random_orthogonal")
    }
    ratios = {
        field: scalar_summary(
            record["jvp"]["actual_residual"][field]
            / max(record["jvp"]["random_orthogonal"][field], EPS)
            for record in records
        )
        for field in JVP_FIELDS
    }
    vjp = {}
    for objective in VJP_OBJECTIVES:
        vjp[objective] = {
            "value": scalar_summary(record["vjp"][objective]["value"] for record in records),
            **{
                field: scalar_summary(record["vjp"][objective][field] for record in records)
                for field in (
                    "gradient_rms",
                    "directional_derivative",
                    "directional_derivative_per_latent_element",
                    "cosine_to_actual_residual",
                )
            },
        }
    return {
        "samples": len(records),
        "decoder_input_residual_rms": scalar_summary(
            record["decoder_input_residual_rms"] for record in records
        ),
        "jvp": jvp,
        "actual_over_random_jvp": ratios,
        "vjp": vjp,
        "reproduction_max_abs_delta": {
            key: max(record["reproduction_abs_delta"][key] for record in records)
            for key in (
                "decoder_input_residual_rms",
                "camera_center_ade",
                "camera_center_fde",
                "camera_rotation_deg",
            )
        },
    }


def _resolve(story_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else story_root / path


def init_contract(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(output)
    raw_path = args.reference_raw_artifact.resolve()
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    if raw.get("kind") != "d4_directc_raw_x0_camera_latent_residual":
        raise ValueError("reference artifact is not a D4 raw-residual artifact")
    parent_path = Path(raw["contract"]["path"])
    parent = json.loads(parent_path.read_text(encoding="utf-8"))
    run_dir = Path(raw["run"]["run_dir"])
    run_meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
    stats_path = _resolve(args.story_root.resolve(), run_meta["latent_znorm"]["stats_path"])
    stats_file_audit = latent_stats_file_audit(
        sha256_file(stats_path),
        parent["cache"]["z_norm_stats_sha256"],
        args.accept_stats_reserialization,
    )
    stats_file_audit["path"] = str(stats_path)
    stats_file_audit["acceptance_boundary"] = (
        "An accepted mismatch binds the current file exactly and still requires the embedded "
        "source-cache hash plus the D4 raw-artifact latent summary to match. It does not amend "
        "or overwrite the immutable parent contract."
    )
    contract = copy.deepcopy(parent)
    contract["run_id"] = args.run_id
    contract["version"] = f"{parent['parent_stage1']['version']}-D4.3-diagnostic"
    contract["status"] = "preflight_ready_diagnostic_only"
    contract["generation_modes"] = ["camera_completion_single_step_decoder_sensitivity"]
    contract["data"]["eval_samples"] = 64
    contract["data"]["eval_sample_ids_sha256"] = raw["identity_audit"]["ordered_ids_sha256"]
    contract["eval"] = {
        "seed": 17,
        "batch_size": 16,
        "decode_batch_size": 8,
        "sample_count": 64,
        "sampler": {
            "name": "teacher_forced_single_step_x0_decoder_jvp_vjp",
            "steps": 1,
            "eta": 0.0,
            "cfg_scale": 1.0,
        },
    }
    contract["train"]["phase"] = "D4.3_decoder_sensitivity_no_training"
    contract["diagnostic_only"] = True
    contract["promotion_eligible"] = False
    contract["parent_evidence"] = {
        "experiment_contract": str(parent_path),
        "experiment_contract_sha256": sha256_file(parent_path),
        "raw_residual_artifact": str(raw_path),
        "raw_residual_artifact_sha256": sha256_file(raw_path),
    }
    contract["d43_decoder_sensitivity"] = {
        "question": (
            "Does the observed D4 camera residual align with owning-decoder directions that "
            "amplify decoded camera center or rotation more than an RMS-matched isotropic control?"
        ),
        "sample_count": 64,
        "ordered_ids_sha256": raw["identity_audit"]["ordered_ids_sha256"],
        "timesteps": [50, 500, 950],
        "direction_space": "owning-decoder camera-latent input after inverse train-only normalization",
        "direction_normalization": "per-sample valid-element RMS=1",
        "jvp_basepoint": "midpoint(target_decoder_input, predicted_decoder_input)",
        "random_controls_per_sample": 1,
        "random_control": "deterministic Gaussian projected orthogonal to actual residual and RMS matched",
        "vjp_basepoint": "predicted_decoder_input",
        "vjp_objectives": list(VJP_OBJECTIVES),
        "reproduction_abs_tolerances": REPRODUCTION_ABS_TOLERANCES,
        "reproduction_tolerance_basis": (
            "Fixed before the candidate probe from a v7.36 N64 cross-host replay: exact "
            "checkpoint/cache/decoder/code hashes, RTX 4090 torch-2.3.1+cu121 parent versus "
            "RTX 5090 torch-2.8.0+cu128 replay. The observed maxima were 1.998e-4 latent RMS, "
            "3.558e-3 m center, and 4.186e-2 deg rotation."
        ),
        "latent_stats_file_audit": stats_file_audit,
        "allow_nondefault_tokenizer_contract": parent["parent_stage1"]["version"] != "v7.14",
        "decision_rule": {
            "local_alignment_support": (
                "For camera-center or rotation JVP, candidate/baseline median gain >=1.10 and "
                "candidate actual/random median gain >=1.20 at t=50 or t=500."
            ),
            "otherwise": (
                "Do not justify a decoder-sensitivity-weighted Stage2 objective from D4.3; "
                "retain finite-path/nonlinear or inverse-normalization explanations."
            ),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output, contract)
    print(json.dumps({"ok": True, "contract": str(output)}, sort_keys=True))


def _validate_identity(
    contract: dict[str, Any],
    raw: dict[str, Any],
    raw_path: Path,
    parent_path: Path,
    run_info: dict[str, Any],
    cache_path: Path,
    selected_ids: list[str],
    owning_decoder_record: dict[str, Any],
) -> None:
    d43 = contract["d43_decoder_sensitivity"]
    checks = {
        "raw_artifact_sha256": (
            sha256_file(raw_path),
            contract["parent_evidence"]["raw_residual_artifact_sha256"],
        ),
        "parent_contract_sha256": (
            sha256_file(parent_path),
            contract["parent_evidence"]["experiment_contract_sha256"],
        ),
        "checkpoint_sha256": (
            run_info["checkpoint_sha256"],
            raw["identity_audit"]["checkpoint_sha256"],
        ),
        "checkpoint_step": (run_info["step"], raw["identity_audit"]["checkpoint_step"]),
        "cache_sha256": (sha256_file(cache_path), raw["identity_audit"]["cache"]["sha256"]),
        "ordered_ids_sha256": (sha256_ids(selected_ids), d43["ordered_ids_sha256"]),
        "owning_decoder_sha256": (
            owning_decoder_record.get("checkpoint_sha256"),
            raw["identity_audit"]["owning_decoder"].get("checkpoint_sha256"),
        ),
        "samples": (len(selected_ids), d43["sample_count"]),
        "timesteps": (d43["timesteps"], [50, 500, 950]),
    }
    failures = {
        key: {"actual": actual, "expected": expected}
        for key, (actual, expected) in checks.items()
        if actual != expected
    }
    if failures:
        raise RuntimeError(f"D4.3 identity audit failed: {json.dumps(failures, sort_keys=True)}")


def _raw_records(raw_path: Path, raw: dict[str, Any], timestep: int) -> list[dict[str, Any]]:
    record = raw["files"][str(timestep)]
    path = raw_path.parent / record["records"]
    if sha256_file(path) != record["records_sha256"]:
        raise RuntimeError(f"D4 raw records hash mismatch: {path}")
    return _read_jsonl(path)


def record(args: argparse.Namespace) -> None:
    contract_path = args.diagnostic_contract.resolve()
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    d43 = contract["d43_decoder_sensitivity"]
    if not args.preflight and args.output_dir.name != ARTIFACT_DIR_NAME:
        raise ValueError(f"formal output directory must be named {ARTIFACT_DIR_NAME}")
    if not args.preflight and (
        d43["sample_count"] != 64 or tuple(d43["timesteps"]) != DEFAULT_TIMESTEPS
    ):
        raise ValueError("formal D4.3 requires N64 and t=50,500,950")
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent))
    try:
        patch_numpy_aliases()
        np.random.seed(contract["eval"]["seed"])
        torch.manual_seed(contract["eval"]["seed"])
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(contract["eval"]["seed"])
        device = torch.device(args.device)
        story_root = args.story_root.resolve()
        raw_path = Path(contract["parent_evidence"]["raw_residual_artifact"])
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        parent_path = Path(contract["parent_evidence"]["experiment_contract"])
        parent_contract = json.loads(parent_path.read_text(encoding="utf-8"))
        train_mod = load_module(
            "train_stage2_condmdi_pulp_d43", story_root / "scripts/train_stage2_condmdi_pulp.py"
        )
        cache_mod = load_module(
            "build_stage2_pulp_latent_cache_d43",
            story_root / "scripts/build_stage2_pulp_latent_cache.py",
        )
        run_dir = Path(raw["run"]["run_dir"])
        checkpoint = Path(raw["run"]["checkpoint"])
        model, diffusion, run_info = load_stage2(run_dir, train_mod, device, checkpoint)
        model.requires_grad_(False)
        if getattr(diffusion, "prediction_type", None) != "START_X":
            raise RuntimeError("D4.3 requires START_X")
        cache_path = Path(raw["identity_audit"]["cache"]["path"])
        run_meta = json.loads((run_dir / "meta.json").read_text(encoding="utf-8"))
        znorm_meta = run_meta["latent_znorm"]
        stats_path = _resolve(story_root, znorm_meta["stats_path"])
        znorm_stats = train_mod.load_latent_znorm_stats(stats_path)
        stats_file_audit = d43["latent_stats_file_audit"]
        actual_stats_sha = sha256_file(stats_path)
        if actual_stats_sha != stats_file_audit["actual_sha256"]:
            raise RuntimeError("D4.3 latent z-normalization bound stats file changed")
        expected_stats_sha = parent_contract["cache"]["z_norm_stats_sha256"]
        if expected_stats_sha != stats_file_audit["parent_expected_sha256"]:
            raise RuntimeError("D4.3 parent stats hash changed after contract initialization")
        if (
            actual_stats_sha != expected_stats_sha
            and stats_file_audit["path_status"] != "accepted_parent_reserialization_mismatch"
        ):
            raise RuntimeError("D4.3 latent z-normalization stats hash mismatch")
        expected_source_sha = parent_contract["cache"]["z_norm_source_train_sha256"]
        if znorm_stats.get("source_cache_sha256") != expected_source_sha:
            raise RuntimeError("D4.3 latent z-normalization source-cache hash mismatch")
        stats_summary = train_mod.latent_znorm_summary(znorm_stats)
        if stats_summary != raw["identity_audit"]["latent_znorm"]["summary"]:
            raise RuntimeError("D4.3 latent z-normalization summary differs from D4 evidence")
        znorm_record = {
            "enabled": True,
            "stats_path": str(stats_path),
            "stats_sha256": actual_stats_sha,
            "parent_expected_stats_sha256": expected_stats_sha,
            "stats_file_path_status": stats_file_audit["path_status"],
            "source_cache": znorm_meta["source_cache"],
            "source_cache_sha256": expected_source_sha,
            "source_cache_parent_audit": "inherited from immutable D4 raw-residual artifact",
            "full_covariance": bool(znorm_stats.get("full_covariance")),
            "full_covariance_ridge": float(znorm_stats.get("full_covariance_ridge", 0.0)),
            "summary": stats_summary,
        }
        args.seed = int(contract["eval"]["seed"])
        args.batch_size = int(contract["eval"]["batch_size"])
        args.split = "test"
        args.set_name = "pure_"
        _, dataset, autoencoder = build_pulp(cache_mod, story_root, args, device)
        cache_meta = full_eval.load_cache_meta(cache_path)
        cache = train_mod.PulpLatentCache(cache_path, znorm_stats=znorm_stats)
        cache_meta["sample_ids_sha256"] = train_mod.sha256_sample_ids(
            [str(value) for value in cache.sample_id]
        )
        train_mod.assert_non_causal_cache_meta(cache_meta)
        if not d43["allow_nondefault_tokenizer_contract"]:
            train_mod.assert_default_cache_meta(cache_meta)
        owning_decoder, owning_decoder_record = resolve_owning_decoder(
            story_root, cache_meta, autoencoder, device
        )
        owning_decoder["model"].requires_grad_(False)
        samples = int(d43["sample_count"])
        selected_ids = [str(value) for value in cache.sample_id[:samples]]
        _validate_identity(
            contract,
            raw,
            raw_path,
            parent_path,
            run_info,
            cache_path,
            selected_ids,
            owning_decoder_record,
        )
        raw_by_timestep = {
            timestep: _raw_records(raw_path, raw, timestep)
            for timestep in d43["timesteps"]
        }
        for timestep, rows in raw_by_timestep.items():
            if [row["sample_id"] for row in rows] != selected_ids:
                raise RuntimeError(f"D4 raw ordered IDs differ at t={timestep}")

        loader, end = full_eval.collate_cache(
            cache, 0, samples, int(contract["eval"]["batch_size"]), args.workers
        )
        if end != samples:
            raise RuntimeError("cache is shorter than the D4.3 sample contract")
        task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}["camera"]
        task_routing = str(run_info.get("task_routing", "symmetric"))
        records_by_timestep: dict[int, list[dict[str, Any]]] = {
            timestep: [] for timestep in d43["timesteps"]
        }
        started = time.time()
        processed = 0
        for batch_index, batch in enumerate(loader):
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            sample_ids = [str(value) for value in batch["sample_id"]]
            sample_indices = list(range(processed, processed + len(sample_ids)))
            pulp_batch = batch_from_sample_ids(dataset, sample_ids, device)
            padding_mask = pulp_batch["padding_mask"].bool()
            intrinsics = pulp_batch["x_raw"]["intrinsics"]
            _, raw_reference = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
            with torch.no_grad():
                target_decoder = train_mod.denormalize_latent(z, valid, znorm_stats)
            for timestep in d43["timesteps"]:
                with torch.no_grad():
                    completion = full_eval.predict_single_step_x0(
                        model,
                        diffusion,
                        train_mod,
                        z,
                        text,
                        valid,
                        task_id,
                        sample_indices,
                        int(contract["eval"]["seed"]) + 8009,
                        timestep,
                        task_routing=task_routing,
                    )
                    prediction_decoder = train_mod.denormalize_latent(
                        completion, valid, znorm_stats
                    )
                human_delta = (
                    prediction_decoder[:, : train_mod.HUM_DIM]
                    - target_decoder[:, : train_mod.HUM_DIM]
                ).abs().max()
                if float(human_delta) > 1.0e-6:
                    raise RuntimeError(
                        f"Direct-C observed Human branch changed by {float(human_delta)}"
                    )
                target_camera_z = target_decoder[:, train_mod.HUM_DIM :].detach()
                prediction_camera_z = prediction_decoder[:, train_mod.HUM_DIM :].detach()
                residual = prediction_camera_z - target_camera_z
                seeds = [
                    int(contract["eval"]["seed"])
                    + 43_001
                    + timestep * 1_009
                    + sample_index * 1_000_003
                    for sample_index in sample_indices
                ]
                directions, residual_rms = camera_directions(residual, valid, seeds)
                fixed_human = target_decoder[:, : train_mod.HUM_DIM].detach()

                def decode_camera(camera_z: torch.Tensor) -> torch.Tensor:
                    full_z = torch.cat([fixed_human, camera_z], dim=1)
                    _, raw_output = decode_with_owning_decoder(
                        owning_decoder,
                        dataset,
                        train_mod,
                        full_z,
                        intrinsics,
                        padding_mask,
                    )
                    return raw_output["camera"]

                midpoint = 0.5 * (target_camera_z + prediction_camera_z)
                jvp_by_direction: dict[str, list[dict[str, float]]] = {}
                for direction_name, direction in directions.items():
                    base_raw, camera_jvp = torch.autograd.functional.jvp(
                        decode_camera,
                        (midpoint,),
                        (direction,),
                        create_graph=False,
                        strict=False,
                    )
                    jvp_by_direction[direction_name] = jvp_camera_metrics(
                        base_raw, camera_jvp, padding_mask
                    )

                prediction_variable = prediction_camera_z.clone().requires_grad_(True)
                raw_prediction = decode_camera(prediction_variable)
                objectives = camera_geometry_objectives(
                    raw_prediction, raw_reference["camera"], padding_mask
                )
                vjp_by_objective: dict[str, list[dict[str, float]]] = {}
                for objective_index, objective_name in enumerate(VJP_OBJECTIVES):
                    gradient = torch.autograd.grad(
                        objectives[objective_name].sum(),
                        prediction_variable,
                        retain_graph=objective_index + 1 < len(VJP_OBJECTIVES),
                    )[0]
                    vjp_by_objective[objective_name] = gradient_alignment(
                        gradient, directions["actual_residual"], valid
                    )

                reference_rows = raw_by_timestep[timestep][
                    processed : processed + len(sample_ids)
                ]
                for local_index, sample_id in enumerate(sample_ids):
                    reference_row = reference_rows[local_index]
                    current_geometry = {
                        "camera_center_ade": float(
                            objectives["camera_center_ade_m"][local_index].detach().cpu()
                        ),
                        "camera_center_fde": float(
                            objectives["camera_center_fde_m"][local_index].detach().cpu()
                        ),
                        "camera_rotation_deg": float(
                            torch.rad2deg(
                                objectives["camera_rotation_mean_rad"][local_index]
                            ).detach().cpu()
                        ),
                    }
                    deltas = {
                        "decoder_input_residual_rms": abs(
                            float(residual_rms[local_index].detach().cpu())
                            - float(reference_row["decoder_input_space"]["sample"]["rms"])
                        ),
                        **{
                            field: abs(
                                current_geometry[field]
                                - float(reference_row["decoded_geometry"][field])
                            )
                            for field in current_geometry
                        },
                    }
                    if d43["reproduction_abs_tolerances"] != REPRODUCTION_ABS_TOLERANCES:
                        raise RuntimeError("D4.3 reproduction tolerances differ from implementation")
                    failures = reproduction_failures(deltas)
                    if failures:
                        raise RuntimeError(
                            f"D4.3 reproduction failed for {sample_id} t={timestep}: {failures}"
                        )
                    records_by_timestep[timestep].append(
                        {
                            "sample_id": sample_id,
                            "sample_index": sample_indices[local_index],
                            "timestep": timestep,
                            "valid_latent_frames": int(valid[local_index].sum().item()),
                            "valid_decoded_frames": int(padding_mask[local_index].sum().item()),
                            "random_direction_seed": seeds[local_index],
                            "decoder_input_residual_rms": float(
                                residual_rms[local_index].detach().cpu()
                            ),
                            "jvp": {
                                name: values[local_index]
                                for name, values in jvp_by_direction.items()
                            },
                            "vjp": {
                                objective_name: {
                                    "value": float(
                                        objectives[objective_name][local_index].detach().cpu()
                                    ),
                                    **vjp_by_objective[objective_name][local_index],
                                }
                                for objective_name in VJP_OBJECTIVES
                            },
                            "reproduction_abs_delta": deltas,
                        }
                    )
            processed += len(sample_ids)
            print(
                json.dumps(
                    {
                        "batch": batch_index,
                        "processed": processed,
                        "target": samples,
                        "elapsed_sec": time.time() - started,
                    },
                    sort_keys=True,
                ),
                flush=True,
            )

        files = {}
        for timestep, rows in records_by_timestep.items():
            if [row["sample_id"] for row in rows] != selected_ids:
                raise RuntimeError(f"D4.3 record order changed at t={timestep}")
            records_name = f"t{timestep:03d}.records.jsonl"
            summary_name = f"t{timestep:03d}.summary.json"
            records_path = temp_dir / records_name
            summary_path = temp_dir / summary_name
            _write_jsonl(records_path, rows)
            _write_json(
                summary_path,
                {
                    "schema_version": 1,
                    "kind": "D4.3_owning_decoder_directional_sensitivity_timestep",
                    "timestep": timestep,
                    "ordered_ids_sha256": sha256_ids(selected_ids),
                    **summarize_records(rows),
                },
            )
            files[str(timestep)] = {
                "records": records_name,
                "records_sha256": sha256_file(records_path),
                "summary": summary_name,
                "summary_sha256": sha256_file(summary_path),
            }

        artifact = {
            "schema_version": 1,
            "kind": "D4.3_owning_decoder_directional_sensitivity",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "diagnostic_only": True,
            "promotion_eligible": False,
            "scientific_boundary": (
                "Local owning-decoder sensitivity along frozen D4 Direct-C residuals. "
                "It is not a full Jacobian, training result, full-reverse generation metric, "
                "or evidence that Stage1 alone caused the residual."
            ),
            "run": run_info,
            "contract": {
                "path": str(contract_path),
                "sha256": sha256_file(contract_path),
                "run_id": contract["run_id"],
            },
            "parent_evidence": contract["parent_evidence"],
            "identity_audit": {
                "status": "passed",
                "selected_ordered_ids": selected_ids,
                "selected_ordered_ids_sha256": sha256_ids(selected_ids),
                "cache_path": str(cache_path),
                "cache_sha256": sha256_file(cache_path),
                "checkpoint_sha256": run_info["checkpoint_sha256"],
                "checkpoint_step": run_info["step"],
                "latent_znorm": znorm_record,
                "owning_decoder": owning_decoder_record,
                "is_causal": False,
                "implementation_sha256": {
                    "d43": sha256_file(Path(__file__).resolve()),
                    "d4_raw": sha256_file(story_root / "scripts/storymotion_d4_raw_residual.py"),
                    "official_full_eval": sha256_file(
                        story_root / "scripts/storymotion_official_full_eval.py"
                    ),
                    "official_bridge": sha256_file(
                        story_root / "scripts/storymotion_official_bridge_smoke.py"
                    ),
                },
            },
            "eval": {
                "task": "camera",
                "task_contract": "Direct-C with observed GT Human latent plus camera text",
                "samples": samples,
                "timesteps": d43["timesteps"],
                "seed": contract["eval"]["seed"],
                "batch_size": contract["eval"]["batch_size"],
                "direction_normalization": d43["direction_normalization"],
                "jvp_basepoint": d43["jvp_basepoint"],
                "vjp_basepoint": d43["vjp_basepoint"],
                "random_controls_per_sample": 1,
                "reproduction_abs_tolerances": d43["reproduction_abs_tolerances"],
                "reproduction_tolerance_basis": d43["reproduction_tolerance_basis"],
            },
            "files": files,
            "elapsed_sec": time.time() - started,
            "device": str(device),
            "cuda_device": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        }
        _write_json(temp_dir / "artifact.json", artifact)
        temp_dir.rename(output_dir)
        print(json.dumps({"ok": True, "artifact": str(output_dir / "artifact.json")}, sort_keys=True))
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def _summary(artifact_path: Path, timestep: int) -> dict[str, Any]:
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    if artifact.get("kind") != "D4.3_owning_decoder_directional_sensitivity":
        raise ValueError(f"not a D4.3 artifact: {artifact_path}")
    entry = artifact["files"][str(timestep)]
    path = artifact_path.parent / entry["summary"]
    if sha256_file(path) != entry["summary_sha256"]:
        raise RuntimeError(f"D4.3 summary hash mismatch: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def compare(args: argparse.Namespace) -> None:
    baseline_path = args.baseline.resolve()
    candidate_path = args.candidate.resolve()
    baseline_artifact = json.loads(baseline_path.read_text(encoding="utf-8"))
    candidate_artifact = json.loads(candidate_path.read_text(encoding="utf-8"))
    baseline_ids = baseline_artifact["identity_audit"]["selected_ordered_ids_sha256"]
    candidate_ids = candidate_artifact["identity_audit"]["selected_ordered_ids_sha256"]
    if baseline_ids != candidate_ids:
        raise RuntimeError("D4.3 candidate and baseline ordered IDs differ")
    metrics = (
        "camera_center_rms_gain_m",
        "camera_rotation_tangent_rms_deg",
    )
    by_timestep = {}
    support = []
    for timestep in DEFAULT_TIMESTEPS:
        baseline = _summary(baseline_path, timestep)
        candidate = _summary(candidate_path, timestep)
        effects = {}
        for metric in metrics:
            base_actual = baseline["jvp"]["actual_residual"][metric]["median"]
            cand_actual = candidate["jvp"]["actual_residual"][metric]["median"]
            cand_random = candidate["jvp"]["random_orthogonal"][metric]["median"]
            effect = {
                "candidate_over_baseline_actual_median": cand_actual / max(base_actual, EPS),
                "candidate_actual_over_random_median": cand_actual / max(cand_random, EPS),
                "baseline_actual_median": base_actual,
                "candidate_actual_median": cand_actual,
                "candidate_random_median": cand_random,
            }
            effect["passes_local_alignment_rule"] = bool(
                timestep in (50, 500)
                and effect["candidate_over_baseline_actual_median"] >= 1.10
                and effect["candidate_actual_over_random_median"] >= 1.20
            )
            if effect["passes_local_alignment_rule"]:
                support.append({"timestep": timestep, "metric": metric})
            effects[metric] = effect
        by_timestep[str(timestep)] = {
            "jvp_effects": effects,
            "candidate_vjp_cosine_median": {
                objective: candidate["vjp"][objective]["cosine_to_actual_residual"]["median"]
                for objective in VJP_OBJECTIVES
            },
            "baseline_vjp_cosine_median": {
                objective: baseline["vjp"][objective]["cosine_to_actual_residual"]["median"]
                for objective in VJP_OBJECTIVES
            },
        }
    payload = {
        "schema_version": 1,
        "kind": "D4.3_owning_decoder_directional_sensitivity_matched_comparison",
        "baseline": {"path": str(baseline_path), "sha256": sha256_file(baseline_path)},
        "candidate": {"path": str(candidate_path), "sha256": sha256_file(candidate_path)},
        "ordered_ids_sha256": baseline_ids,
        "decision_rule": (
            "Support local alignment when candidate/baseline actual median >=1.10 and "
            "candidate actual/random median >=1.20 for center or rotation at t=50 or t=500."
        ),
        "decision": "local_alignment_supported" if support else "local_alignment_not_supported",
        "supporting_slices": support,
        "by_timestep": by_timestep,
        "scientific_boundary": (
            "Matched system-level comparison across two owning manifolds/decoders; it does not "
            "isolate Stage1 weights from the Stage2 residual that supplied each direction."
        ),
    }
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(args.output, payload)
    print(json.dumps({"ok": True, "comparison": str(args.output)}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init-contract")
    init.add_argument("--story-root", type=Path, default=ROOT)
    init.add_argument("--run-id", required=True)
    init.add_argument("--reference-raw-artifact", type=Path, required=True)
    init.add_argument("--output", type=Path, required=True)
    init.add_argument("--accept-stats-reserialization", action="store_true")
    init.set_defaults(func=init_contract)

    run = subparsers.add_parser("record")
    run.add_argument("--story-root", type=Path, default=ROOT)
    run.add_argument("--diagnostic-contract", type=Path, required=True)
    run.add_argument("--output-dir", type=Path, required=True)
    run.add_argument("--preflight", action="store_true")
    run.add_argument("--device", default="cuda:0")
    run.add_argument("--workers", type=int, default=0)
    run.add_argument("--config-name", default="config_dit_xy")
    run.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"),
    )
    run.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    run.add_argument("--data-root", type=Path, default=ROOT / "linked/pulpmotion-data")
    run.set_defaults(func=record)

    comparison = subparsers.add_parser("compare")
    comparison.add_argument("--baseline", type=Path, required=True)
    comparison.add_argument("--candidate", type=Path, required=True)
    comparison.add_argument("--output", type=Path, required=True)
    comparison.set_defaults(func=compare)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
