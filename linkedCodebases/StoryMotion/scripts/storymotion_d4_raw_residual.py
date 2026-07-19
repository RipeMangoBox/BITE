#!/usr/bin/env python3
"""Record D4 Direct-C single-step camera-latent residuals without mutation.

The recorder reuses the official teacher-forced ``predict_single_step_x0``
path, then relates valid-frame camera-latent errors to decoded camera geometry.
It is a diagnostic-only reader: it never trains, writes a cache, or modifies a
checkpoint.  Run ``record`` once per matched arm and ``compare`` on the two
resulting artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch

import storymotion_official_full_eval as full_eval
from storymotion.per_sample_quality import paired_geometry_batch
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
FIELDS = ("signed_mean", "rms", "mae", "target_rms", "relative_error")
GEOMETRY_FIELDS = ("camera_center_ade", "camera_center_fde", "camera_rotation_deg")
DEFAULT_TIMESTEPS = (50, 500, 950)
RELATIVE_EPS = 1.0e-8


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_ids(sample_ids: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for sample_id in sample_ids:
        digest.update(str(sample_id).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def scalar_summary(values: Iterable[float]) -> dict[str, float | int]:
    array = np.asarray(list(values), dtype=np.float64)
    if array.size == 0:
        raise ValueError("cannot summarize an empty sequence")
    if not np.isfinite(array).all():
        raise ValueError("summary input contains non-finite values")
    return {
        "count": int(array.size),
        "mean": float(array.mean()),
        "median": float(np.median(array)),
        "p90": float(np.percentile(array, 90)),
        "min": float(array.min()),
        "max": float(array.max()),
    }


def _average_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(values.size, dtype=np.float64)
    start = 0
    while start < values.size:
        end = start + 1
        while end < values.size and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = 0.5 * (start + end - 1)
        start = end
    return ranks


def correlation(first: Iterable[float], second: Iterable[float]) -> dict[str, float | int | None]:
    x = np.asarray(list(first), dtype=np.float64)
    y = np.asarray(list(second), dtype=np.float64)
    if x.shape != y.shape or x.ndim != 1:
        raise ValueError("correlation inputs must be equal-length vectors")
    finite = np.isfinite(x) & np.isfinite(y)
    x = x[finite]
    y = y[finite]
    if x.size < 2 or float(x.std()) == 0.0 or float(y.std()) == 0.0:
        return {"count": int(x.size), "pearson": None, "spearman": None}
    pearson = float(np.corrcoef(x, y)[0, 1])
    spearman = float(np.corrcoef(_average_ranks(x), _average_ranks(y))[0, 1])
    return {"count": int(x.size), "pearson": pearson, "spearman": spearman}


def camera_residual_records(
    prediction: torch.Tensor,
    target: torch.Tensor,
    valid: torch.Tensor,
    camera_start: int,
) -> list[dict[str, Any]]:
    """Return valid-frame residual statistics per sample and camera channel."""
    if prediction.shape != target.shape or prediction.ndim != 3:
        raise ValueError("prediction and target must have the same [B,C,T] shape")
    if valid.shape != (prediction.shape[0], prediction.shape[2]):
        raise ValueError("valid mask must have shape [B,T]")
    if not 0 <= camera_start < prediction.shape[1]:
        raise ValueError("camera_start is outside the latent channels")
    records: list[dict[str, Any]] = []
    for sample_index in range(prediction.shape[0]):
        sample_valid = valid[sample_index].bool()
        if int(sample_valid.sum().item()) <= 0:
            raise ValueError(f"sample {sample_index} has no valid latent frames")
        pred = prediction[sample_index, camera_start:, sample_valid].double()
        ref = target[sample_index, camera_start:, sample_valid].double()
        residual = pred - ref
        channel_rms = residual.square().mean(dim=1).sqrt()
        channel_target_rms = ref.square().mean(dim=1).sqrt()
        sample_rms = residual.square().mean().sqrt()
        sample_target_rms = ref.square().mean().sqrt()
        records.append(
            {
                "valid_latent_frames": int(sample_valid.sum().item()),
                "channel": {
                    "signed_mean": residual.mean(dim=1).cpu().tolist(),
                    "rms": channel_rms.cpu().tolist(),
                    "mae": residual.abs().mean(dim=1).cpu().tolist(),
                    "target_rms": channel_target_rms.cpu().tolist(),
                    "relative_error": (
                        channel_rms / channel_target_rms.clamp_min(RELATIVE_EPS)
                    ).cpu().tolist(),
                },
                "sample": {
                    "signed_mean": float(residual.mean().item()),
                    "rms": float(sample_rms.item()),
                    "mae": float(residual.abs().mean().item()),
                    "target_rms": float(sample_target_rms.item()),
                    "relative_error": float(
                        (sample_rms / sample_target_rms.clamp_min(RELATIVE_EPS)).item()
                    ),
                },
            }
        )
    return records


def summarize_residual_records(records: list[dict[str, Any]], space: str) -> dict[str, Any]:
    if not records:
        raise ValueError("residual records are empty")
    channel_count = len(records[0][space]["channel"]["rms"])
    channel_summary: dict[str, Any] = {}
    sample_summary: dict[str, Any] = {}
    for field in FIELDS:
        sample_summary[field] = scalar_summary(record[space]["sample"][field] for record in records)
        matrix = np.asarray([record[space]["channel"][field] for record in records], dtype=np.float64)
        if matrix.shape != (len(records), channel_count) or not np.isfinite(matrix).all():
            raise ValueError(f"invalid per-channel {field} matrix")
        channel_summary[field] = {
            "mean_across_samples": matrix.mean(axis=0).tolist(),
            "median_across_samples": np.median(matrix, axis=0).tolist(),
        }
    return {
        "samples": len(records),
        "camera_channels": channel_count,
        "sample": sample_summary,
        "channel": channel_summary,
    }


def summarize_geometry(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {field: scalar_summary(record["decoded_geometry"][field] for record in records) for field in GEOMETRY_FIELDS}


def residual_geometry_association(records: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for space in ("model_space", "decoder_input_space"):
        output[space] = {}
        for residual_field in ("rms", "mae", "relative_error"):
            output[space][residual_field] = {
                geometry_field: correlation(
                    (record[space]["sample"][residual_field] for record in records),
                    (record["decoded_geometry"][geometry_field] for record in records),
                )
                for geometry_field in GEOMETRY_FIELDS
            }
    output["decoded_error_per_decoder_input_rms"] = {
        geometry_field: scalar_summary(
            record["decoded_geometry"][geometry_field]
            / max(record["decoder_input_space"]["sample"]["rms"], RELATIVE_EPS)
            for record in records
        )
        for geometry_field in GEOMETRY_FIELDS
    }
    return output


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def _git_commit(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _contract_value(contract: dict[str, Any], *keys: str) -> Any:
    value: Any = contract
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            raise ValueError(f"contract is missing {'.'.join(keys)}")
        value = value[key]
    return value


def validate_contract(
    contract: dict[str, Any],
    run_info: dict[str, Any],
    cache_path: Path,
    cache_sha256: str,
    ordered_ids_sha256: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    diagnostic = _contract_value(contract, "diagnostic_evals", "d4_directc_single_step_n64")
    failures = []

    def check(label: str, actual: Any, expected: Any) -> None:
        if actual != expected:
            failures.append({"field": label, "actual": actual, "expected": expected})

    check("stage", contract.get("stage"), "stage2")
    check("promotion_eligible", bool(diagnostic.get("promotion_eligible")), False)
    check("checkpoint_sha256", run_info.get("checkpoint_sha256"), diagnostic["checkpoint"]["sha256"])
    check("checkpoint_step", int(run_info.get("step", -1)), int(diagnostic["checkpoint"]["step"]))
    check("eval_cache_sha256", cache_sha256, _contract_value(contract, "cache", "eval_sha256"))
    check("eval_cache_path_name", cache_path.name, Path(_contract_value(contract, "cache", "eval_path")).name)
    check("ordered_ids_sha256", ordered_ids_sha256, diagnostic["ordered_ids_sha256"])
    check("sample_count", args.samples, int(diagnostic["sample_count"]))
    check("batch_size", args.batch_size, int(diagnostic["batch_size"]))
    check("decode_batch_size", args.decode_batch_size, int(diagnostic["decode_batch_size"]))
    check("seed", args.seed, int(diagnostic["seed"]))
    check("split", args.split, diagnostic["split"])
    check("set_name", args.set_name, diagnostic["set_name"])
    check("timesteps", list(args.timesteps), list(diagnostic["timesteps"]))
    check("task", list(diagnostic["tasks"]), ["camera"])
    check("sampler", diagnostic["sampler"]["name"], "teacher_forced_single_step_x0")
    if failures:
        raise RuntimeError(f"D4 contract audit failed: {json.dumps(failures, sort_keys=True)}")
    return {
        "status": "passed",
        "checked_fields": [
            "stage",
            "promotion_eligible",
            "checkpoint_sha256",
            "checkpoint_step",
            "eval_cache_sha256",
            "ordered_ids_sha256",
            "sample_count",
            "batch_size",
            "decode_batch_size",
            "seed",
            "split",
            "set_name",
            "timesteps",
            "task",
            "sampler",
        ],
    }


def reference_audit(
    reference_eval_dir: Path,
    timestep: int,
    records: list[dict[str, Any]],
    expected_ids: list[str],
) -> dict[str, Any]:
    json_path = reference_eval_dir / f"camera_t{timestep:03d}.json"
    records_path = reference_eval_dir / f"camera_t{timestep:03d}.records.jsonl"
    if not json_path.is_file() or not records_path.is_file():
        raise FileNotFoundError(f"missing prior D4 artifact for t={timestep}: {reference_eval_dir}")
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    prior_records = _read_jsonl(records_path)
    prior_ids = [str(record["sample_id"]) for record in prior_records]
    if prior_ids[: len(expected_ids)] != expected_ids:
        raise RuntimeError(f"prior D4 ordered-ID prefix differs at t={timestep}")
    if payload.get("eval_source") != "single_step" or int(payload.get("single_step_timestep", -1)) != timestep:
        raise RuntimeError(f"prior D4 source/timestep mismatch at t={timestep}")
    current_mean = {
        field: float(np.mean([record["decoded_geometry"][field] for record in records]))
        for field in GEOMETRY_FIELDS
    }
    prior_geometry = payload["paired_geometry"]["records"]
    if [str(record["sample_id"]) for record in prior_geometry[: len(expected_ids)]] != expected_ids:
        raise RuntimeError(f"prior D4 geometry ordered-ID prefix differs at t={timestep}")
    prior_mean = {
        field: float(
            np.mean(
                [float(record[field]) for record in prior_geometry[: len(expected_ids)]]
            )
        )
        for field in GEOMETRY_FIELDS
    }
    deltas = {field: abs(current_mean[field] - float(prior_mean[field])) for field in GEOMETRY_FIELDS}
    tolerances = {
        "camera_center_ade": 1.0e-2,
        "camera_center_fde": 1.0e-2,
        "camera_rotation_deg": 5.0e-2,
    }
    failures = {
        field: delta for field, delta in deltas.items() if delta > tolerances[field]
    }
    max_delta = max(deltas.values())
    if failures:
        raise RuntimeError(f"decoded geometry does not reproduce prior D4 t={timestep}: {deltas}")
    return {
        "status": "passed",
        "json": str(json_path.resolve()),
        "json_sha256": sha256_file(json_path),
        "records": str(records_path.resolve()),
        "records_sha256": sha256_file(records_path),
        "ordered_ids_sha256": sha256_ids(expected_ids),
        "full_reference_ordered_ids_sha256": sha256_ids(prior_ids),
        "decoded_geometry_abs_delta": deltas,
        "decoded_geometry_max_abs_delta": max_delta,
        "decoded_geometry_abs_tolerance": tolerances,
    }


def record(args: argparse.Namespace) -> None:
    if args.samples <= 0:
        raise ValueError("--samples must be positive")
    if len(set(args.timesteps)) != len(args.timesteps):
        raise ValueError("--timesteps must be unique")
    if any(timestep < 0 or timestep >= 1000 for timestep in args.timesteps):
        raise ValueError("--timesteps must be in [0,1000)")
    if not args.preflight:
        if args.output_dir.name != "raw_residual_20260719":
            raise ValueError("formal output directory must be named raw_residual_20260719")
        if args.samples != 64 or tuple(args.timesteps) != DEFAULT_TIMESTEPS:
            raise ValueError("formal D4 recorder requires N64 and timesteps 50,500,950")
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"refusing to overwrite existing artifact directory: {output_dir}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.tmp-", dir=output_dir.parent))
    try:
        patch_numpy_aliases()
        np.random.seed(args.seed)
        torch.manual_seed(args.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(args.seed)
        device = torch.device(args.device)
        story_root = args.story_root.resolve()
        contract_path = args.contract.resolve()
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        train_mod = load_module("train_stage2_condmdi_pulp_d4_raw", story_root / "scripts/train_stage2_condmdi_pulp.py")
        cache_mod = load_module("build_stage2_pulp_latent_cache_d4_raw", story_root / "scripts/build_stage2_pulp_latent_cache.py")
        model, diffusion, run_info = load_stage2(
            args.run_dir.resolve(), train_mod, device, checkpoint_path=args.checkpoint
        )
        if getattr(diffusion, "prediction_type", "START_X") != "START_X":
            raise RuntimeError("D4 raw-residual recorder requires START_X prediction")
        if int(diffusion.num_timesteps) != 1000:
            raise RuntimeError(f"expected 1000 diffusion timesteps, got {diffusion.num_timesteps}")
        znorm_stats, znorm_record = full_eval.resolve_run_znorm(
            args.run_dir.resolve(), args.cache_dir.resolve(), train_mod
        )
        _, dataset, autoencoder = build_pulp(cache_mod, story_root, args, device)
        cache_path = (args.cache_dir / args.cache_file).resolve()
        cache_meta = full_eval.load_cache_meta(cache_path)
        cache = train_mod.PulpLatentCache(cache_path, znorm_stats=znorm_stats)
        cache_meta["sample_ids_sha256"] = train_mod.sha256_sample_ids(
            [str(value) for value in cache.sample_id]
        )
        train_mod.assert_non_causal_cache_meta(cache_meta)
        if not args.allow_nondefault_tokenizer_contract:
            train_mod.assert_default_cache_meta(cache_meta)
        owning_decoder, owning_decoder_record = resolve_owning_decoder(
            story_root, cache_meta, autoencoder, device
        )
        selected_ids = [str(value) for value in cache.sample_id[: args.samples]]
        ordered_ids_sha256 = sha256_ids(selected_ids)
        cache_sha256 = sha256_file(cache_path)
        contract_audit = validate_contract(
            contract, run_info, cache_path, cache_sha256, ordered_ids_sha256, args
        ) if not args.preflight else {"status": "preflight_not_formally_audited"}

        loader, end = full_eval.collate_cache(cache, 0, args.samples, args.batch_size, args.workers)
        if end != args.samples:
            raise RuntimeError(f"cache contains only {end} selected samples")
        task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}["camera"]
        task_routing = str(run_info.get("task_routing", "symmetric"))
        by_timestep: dict[int, list[dict[str, Any]]] = {timestep: [] for timestep in args.timesteps}
        started = time.time()
        processed = 0
        with torch.no_grad():
            for batch_index, batch in enumerate(loader):
                z = batch["z"].to(device)
                text = batch["text"].to(device)
                valid = batch["valid"].to(device)
                sample_ids = [str(value) for value in batch["sample_id"]]
                sample_indices = list(range(processed, processed + len(sample_ids)))
                target_decoder = train_mod.denormalize_latent(z, valid, znorm_stats)
                for timestep in args.timesteps:
                    completion = full_eval.predict_single_step_x0(
                        model,
                        diffusion,
                        train_mod,
                        z,
                        text,
                        valid,
                        task_id,
                        sample_indices,
                        args.seed + 8009,
                        timestep,
                        task_routing=task_routing,
                    )
                    prediction_decoder = train_mod.denormalize_latent(
                        completion, valid, znorm_stats
                    )
                    model_stats = camera_residual_records(
                        completion, z, valid, train_mod.HUM_DIM
                    )
                    decoder_stats = camera_residual_records(
                        prediction_decoder, target_decoder, valid, train_mod.HUM_DIM
                    )
                    geometry_by_id: dict[str, dict[str, Any]] = {}
                    for decode_slice in full_eval.iter_slices(len(sample_ids), args.decode_batch_size):
                        chunk_ids = sample_ids[decode_slice]
                        pulp_batch = batch_from_sample_ids(dataset, chunk_ids, device)
                        intrinsics = pulp_batch["x_raw"]["intrinsics"]
                        _, raw_input = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
                        _, raw_output = decode_with_owning_decoder(
                            owning_decoder,
                            dataset,
                            train_mod,
                            prediction_decoder[decode_slice],
                            intrinsics,
                            pulp_batch["padding_mask"],
                        )
                        geometry = paired_geometry_batch(
                            {"raw_input": raw_input, "raw_output": raw_output},
                            pulp_batch,
                            chunk_ids,
                        )
                        geometry_by_id.update({str(item["sample_id"]): item for item in geometry})
                    for local_index, sample_id in enumerate(sample_ids):
                        geometry = geometry_by_id[sample_id]
                        by_timestep[timestep].append(
                            {
                                "sample_id": sample_id,
                                "sample_index": sample_indices[local_index],
                                "per_sample_noise_seed": args.seed + 8009 + sample_indices[local_index] * 1_000_003,
                                "valid_latent_frames": model_stats[local_index]["valid_latent_frames"],
                                "valid_decoded_frames": int(geometry["valid_frames"]),
                                "model_space": model_stats[local_index],
                                "decoder_input_space": decoder_stats[local_index],
                                "decoded_geometry": {
                                    field: float(geometry[field]) for field in GEOMETRY_FIELDS
                                },
                            }
                        )
                processed += len(sample_ids)
                print(
                    json.dumps(
                        {
                            "batch": batch_index,
                            "processed": processed,
                            "target": args.samples,
                            "elapsed_sec": time.time() - started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

        file_records: dict[str, Any] = {}
        for timestep, records in by_timestep.items():
            if [record["sample_id"] for record in records] != selected_ids:
                raise RuntimeError(f"ordered IDs changed while recording t={timestep}")
            records_name = f"t{timestep:03d}.records.jsonl"
            summary_name = f"t{timestep:03d}.summary.json"
            records_path = temp_dir / records_name
            summary_path = temp_dir / summary_name
            _write_jsonl(records_path, records)
            prior_audit = reference_audit(
                args.reference_eval_dir.resolve(), timestep, records, selected_ids
            ) if args.reference_eval_dir is not None else None
            summary = {
                "schema_version": 1,
                "kind": "d4_directc_raw_x0_camera_latent_residual_timestep",
                "timestep": timestep,
                "samples": len(records),
                "ordered_ids_sha256": ordered_ids_sha256,
                "model_space": summarize_residual_records(records, "model_space"),
                "decoder_input_space": summarize_residual_records(records, "decoder_input_space"),
                "decoded_geometry": summarize_geometry(records),
                "residual_geometry_association": residual_geometry_association(records),
                "prior_d4_reproduction_audit": prior_audit,
                "records": records_name,
                "records_sha256": sha256_file(records_path),
            }
            _write_json(summary_path, summary)
            file_records[str(timestep)] = {
                "records": records_name,
                "records_sha256": sha256_file(records_path),
                "summary": summary_name,
                "summary_sha256": sha256_file(summary_path),
            }

        script_paths = {
            "recorder": Path(__file__).resolve(),
            "official_full_eval": story_root / "scripts/storymotion_official_full_eval.py",
            "official_bridge": story_root / "scripts/storymotion_official_bridge_smoke.py",
            "stage2_model": story_root / "scripts/train_stage2_condmdi_pulp.py",
        }
        artifact = {
            "schema_version": 1,
            "kind": "d4_directc_raw_x0_camera_latent_residual",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "diagnostic_only": True,
            "promotion_eligible": False,
            "preflight": bool(args.preflight),
            "scientific_boundary": (
                "Teacher-forced Direct-C one-step x0 diagnostic. It separates denoiser-space "
                "error from decoder-input-space error and decoded geometry association, but does "
                "not establish a training-factor causal effect or a full-reverse generation result."
            ),
            "run": run_info,
            "contract": {
                "path": str(contract_path),
                "sha256": sha256_file(contract_path),
                "run_id": contract.get("run_id"),
                "version": contract.get("version"),
            },
            "identity_audit": {
                "status": "passed" if not args.preflight else "preflight",
                "contract": contract_audit,
                "ordered_ids_sha256": ordered_ids_sha256,
                "ordered_ids": selected_ids,
                "cache": {
                    "path": str(cache_path),
                    "sha256": cache_sha256,
                    "meta_sample_ids_sha256": cache_meta["sample_ids_sha256"],
                    "tokenizer_checkpoint_sha256": cache_meta.get("tokenizer_checkpoint_sha256"),
                    "is_causal": cache_meta.get("tokenizer_is_causal", False),
                },
                "latent_znorm": znorm_record,
                "owning_decoder": owning_decoder_record,
                "checkpoint_sha256": run_info.get("checkpoint_sha256"),
                "checkpoint_step": run_info.get("step"),
                "git_commit": _git_commit(story_root),
                "implementation_sha256": {
                    name: sha256_file(path) for name, path in script_paths.items()
                },
            },
            "eval": {
                "task": "camera",
                "task_contract": "Direct-C with clean observed GT human latent plus camera text",
                "split": args.split,
                "set_name": args.set_name,
                "samples": args.samples,
                "timesteps": list(args.timesteps),
                "seed": args.seed,
                "noise_seed_base": args.seed + 8009,
                "per_sample_noise_formula": "noise_seed_base + sample_index * 1000003",
                "batch_size": args.batch_size,
                "decode_batch_size": args.decode_batch_size,
                "task_routing": task_routing,
                "prediction_type": getattr(diffusion, "prediction_type", None),
                "sampler": "one q(z_gt,t,deterministic_noise) -> one model x0 prediction",
            },
            "residual_contract": {
                "camera_slice": [int(train_mod.HUM_DIM), int(train_mod.LATENT_DIM)],
                "valid_frame_only": True,
                "fields": list(FIELDS),
                "relative_error": "RMS(pred-target) / max(RMS(target), 1e-8)",
                "model_space": "Stage2 model input/output after train-only z-normalization/whitening",
                "decoder_input_space": "Owning-decoder input after inverse train-only z-normalization/whitening",
            },
            "files": file_records,
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


def _artifact_records(artifact_path: Path, timestep: int) -> list[dict[str, Any]]:
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    record = artifact["files"][str(timestep)]
    path = artifact_path.parent / record["records"]
    if sha256_file(path) != record["records_sha256"]:
        raise RuntimeError(f"record hash mismatch: {path}")
    return _read_jsonl(path)


def compare(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite comparison: {output}")
    baseline_path = args.baseline.resolve()
    candidate_path = args.candidate.resolve()
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    for label, artifact in (("baseline", baseline), ("candidate", candidate)):
        if artifact.get("kind") != "d4_directc_raw_x0_camera_latent_residual":
            raise ValueError(f"{label} is not a D4 raw-residual artifact")
        if artifact.get("preflight"):
            raise ValueError(f"{label} is a preflight artifact")
        if artifact.get("identity_audit", {}).get("status") != "passed":
            raise ValueError(f"{label} identity audit did not pass")
    equality_fields = {
        "ordered_ids_sha256": (
            baseline["identity_audit"]["ordered_ids_sha256"],
            candidate["identity_audit"]["ordered_ids_sha256"],
        ),
        "timesteps": (baseline["eval"]["timesteps"], candidate["eval"]["timesteps"]),
        "seed": (baseline["eval"]["seed"], candidate["eval"]["seed"]),
        "noise_seed_base": (
            baseline["eval"]["noise_seed_base"],
            candidate["eval"]["noise_seed_base"],
        ),
        "samples": (baseline["eval"]["samples"], candidate["eval"]["samples"]),
        "split": (baseline["eval"]["split"], candidate["eval"]["split"]),
        "set_name": (baseline["eval"]["set_name"], candidate["eval"]["set_name"]),
    }
    mismatches = {key: values for key, values in equality_fields.items() if values[0] != values[1]}
    if mismatches:
        raise RuntimeError(f"matched comparison identity failed: {mismatches}")

    timestep_comparisons: dict[str, Any] = {}
    for timestep in baseline["eval"]["timesteps"]:
        baseline_records = _artifact_records(baseline_path, int(timestep))
        candidate_records = _artifact_records(candidate_path, int(timestep))
        baseline_by_id = {record["sample_id"]: record for record in baseline_records}
        candidate_by_id = {record["sample_id"]: record for record in candidate_records}
        ordered_ids = baseline["identity_audit"]["ordered_ids"]
        if list(baseline_by_id) != ordered_ids or list(candidate_by_id) != ordered_ids:
            raise RuntimeError(f"record order/identity mismatch at t={timestep}")
        comparisons: dict[str, Any] = {}
        paired_delta_association: dict[str, Any] = {}
        per_channel_topk: dict[str, Any] = {}
        for space in ("model_space", "decoder_input_space"):
            comparisons[space] = {}
            paired_delta_association[space] = {}
            for field in ("rms", "mae", "relative_error"):
                baseline_values = np.asarray(
                    [baseline_by_id[sample_id][space]["sample"][field] for sample_id in ordered_ids],
                    dtype=np.float64,
                )
                candidate_values = np.asarray(
                    [candidate_by_id[sample_id][space]["sample"][field] for sample_id in ordered_ids],
                    dtype=np.float64,
                )
                delta = candidate_values - baseline_values
                comparisons[space][field] = {
                    "baseline": scalar_summary(baseline_values),
                    "candidate": scalar_summary(candidate_values),
                    "candidate_minus_baseline": scalar_summary(delta),
                    "candidate_to_baseline_mean_ratio": float(
                        candidate_values.mean() / max(baseline_values.mean(), RELATIVE_EPS)
                    ),
                    "candidate_worse_fraction": float((candidate_values > baseline_values).mean()),
                }
                paired_delta_association[space][field] = {}
                for geometry_field in GEOMETRY_FIELDS:
                    geometry_delta = np.asarray(
                        [
                            candidate_by_id[sample_id]["decoded_geometry"][geometry_field]
                            - baseline_by_id[sample_id]["decoded_geometry"][geometry_field]
                            for sample_id in ordered_ids
                        ],
                        dtype=np.float64,
                    )
                    paired_delta_association[space][field][geometry_field] = correlation(
                        delta, geometry_delta
                    )
            baseline_channel_rms = np.asarray(
                [baseline_by_id[sample_id][space]["channel"]["rms"] for sample_id in ordered_ids],
                dtype=np.float64,
            ).mean(axis=0)
            candidate_channel_rms = np.asarray(
                [candidate_by_id[sample_id][space]["channel"]["rms"] for sample_id in ordered_ids],
                dtype=np.float64,
            ).mean(axis=0)
            channel_ratios = candidate_channel_rms / np.maximum(
                baseline_channel_rms, RELATIVE_EPS
            )
            top_indices = np.argsort(-channel_ratios, kind="mergesort")[:10]
            per_channel_topk[space] = [
                {
                    "camera_channel": int(channel),
                    "baseline_mean_rms": float(baseline_channel_rms[channel]),
                    "candidate_mean_rms": float(candidate_channel_rms[channel]),
                    "candidate_minus_baseline_mean_rms": float(
                        candidate_channel_rms[channel] - baseline_channel_rms[channel]
                    ),
                    "candidate_to_baseline_mean_rms_ratio": float(channel_ratios[channel]),
                }
                for channel in top_indices
            ]
        comparisons["decoded_geometry"] = {}
        for field in GEOMETRY_FIELDS:
            baseline_values = np.asarray(
                [baseline_by_id[sample_id]["decoded_geometry"][field] for sample_id in ordered_ids],
                dtype=np.float64,
            )
            candidate_values = np.asarray(
                [candidate_by_id[sample_id]["decoded_geometry"][field] for sample_id in ordered_ids],
                dtype=np.float64,
            )
            comparisons["decoded_geometry"][field] = {
                "baseline": scalar_summary(baseline_values),
                "candidate": scalar_summary(candidate_values),
                "candidate_minus_baseline": scalar_summary(candidate_values - baseline_values),
                "candidate_to_baseline_mean_ratio": float(
                    candidate_values.mean() / max(baseline_values.mean(), RELATIVE_EPS)
                ),
                "candidate_worse_fraction": float((candidate_values > baseline_values).mean()),
            }
        timestep_comparisons[str(timestep)] = {
            "matched_samples": len(ordered_ids),
            "metrics": comparisons,
            "per_channel_rms_candidate_to_baseline_top10": per_channel_topk,
            "paired_delta_association": paired_delta_association,
        }

    payload = {
        "schema_version": 1,
        "kind": "d4_directc_raw_x0_camera_latent_residual_matched_comparison",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "diagnostic_only": True,
        "promotion_eligible": False,
        "baseline": {
            "artifact": str(baseline_path),
            "artifact_sha256": sha256_file(baseline_path),
            "run": baseline["run"],
            "contract": baseline["contract"],
            "owning_decoder": baseline["identity_audit"]["owning_decoder"],
        },
        "candidate": {
            "artifact": str(candidate_path),
            "artifact_sha256": sha256_file(candidate_path),
            "run": candidate["run"],
            "contract": candidate["contract"],
            "owning_decoder": candidate["identity_audit"]["owning_decoder"],
        },
        "matched_identity_audit": {
            "status": "passed",
            **{key: values[0] for key, values in equality_fields.items()},
            "per_sample_noise_formula": baseline["eval"]["per_sample_noise_formula"],
        },
        "interpretation_contract": {
            "denoiser_or_stage2_mismatch_signal": (
                "candidate model-space relative/RMS error rises together with decoded error"
            ),
            "stage1_decoder_amplification_signal": (
                "model-space error is comparable but decoder-input or decoded error rises; "
                "association is descriptive, not a causal decoder intervention"
            ),
            "mixed_signal": (
                "both latent error and decoded-error-per-latent-error rise; requires a decoder "
                "perturbation-Jacobian or matched latent injection before causal attribution"
            ),
        },
        "timesteps": timestep_comparisons,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output, payload)
    print(json.dumps({"ok": True, "comparison": str(output)}, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    record_parser = subparsers.add_parser("record", help="record one matched D4 arm")
    record_parser.add_argument("--story-root", type=Path, default=ROOT)
    record_parser.add_argument("--run-dir", type=Path, required=True)
    record_parser.add_argument("--checkpoint", type=Path)
    record_parser.add_argument("--cache-dir", type=Path, required=True)
    record_parser.add_argument("--cache-file", default="val.pt")
    record_parser.add_argument("--contract", type=Path, required=True)
    record_parser.add_argument("--reference-eval-dir", type=Path)
    record_parser.add_argument("--output-dir", type=Path, required=True)
    record_parser.add_argument("--allow-nondefault-tokenizer-contract", action="store_true")
    record_parser.add_argument("--preflight", action="store_true")
    record_parser.add_argument("--timesteps", nargs="+", type=int, default=list(DEFAULT_TIMESTEPS))
    record_parser.add_argument("--samples", type=int, default=64)
    record_parser.add_argument("--batch-size", type=int, default=16)
    record_parser.add_argument("--decode-batch-size", type=int, default=8)
    record_parser.add_argument("--workers", type=int, default=0)
    record_parser.add_argument("--seed", type=int, default=17)
    record_parser.add_argument("--device", default="cuda:0")
    record_parser.add_argument("--split", default="test")
    record_parser.add_argument("--set-name", default="pure_")
    record_parser.add_argument("--config-name", default="config_dit_xy")
    record_parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"),
    )
    record_parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    record_parser.add_argument("--data-root", type=Path, default=ROOT / "linked/pulpmotion-data")
    record_parser.set_defaults(func=record)

    compare_parser = subparsers.add_parser("compare", help="compare two matched arm artifacts")
    compare_parser.add_argument("--baseline", type=Path, required=True)
    compare_parser.add_argument("--candidate", type=Path, required=True)
    compare_parser.add_argument("--output", type=Path, required=True)
    compare_parser.set_defaults(func=compare)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
