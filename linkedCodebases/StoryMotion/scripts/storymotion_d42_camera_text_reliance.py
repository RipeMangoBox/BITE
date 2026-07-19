#!/usr/bin/env python3
"""D4.2 matched Direct-C camera-text reliance screen.

This diagnostic compares aligned camera text with a deterministic one-step
cyclic shuffle over the same ordered N64 cache slice.  Both conditions reuse
the exact same per-sample noise and x_t tensor for each timestep.  It is
read-only with respect to models, checkpoints, and caches.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch

import storymotion_official_full_eval as full_eval
from storymotion.per_sample_quality import paired_geometry_batch
from storymotion_d4_raw_residual import (
    DEFAULT_TIMESTEPS,
    FIELDS,
    GEOMETRY_FIELDS,
    RELATIVE_EPS,
    camera_residual_records,
    correlation,
    reference_audit,
    scalar_summary,
    sha256_file,
    sha256_ids,
    summarize_geometry,
    summarize_residual_records,
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
ARTIFACT_DIR_NAME = "camera_text_reliance_20260719"
CONDITIONS = ("aligned", "cyclic_shuffled_camera_text")


def sha256_tensor(tensor: torch.Tensor) -> str:
    array = tensor.detach().contiguous().cpu().numpy()
    import hashlib

    return hashlib.sha256(array.tobytes()).hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def cyclic_shuffle_camera_text(text: torch.Tensor) -> tuple[torch.Tensor, list[int]]:
    """Target i receives camera text from (i + 1) mod N; human text stays aligned."""
    if text.ndim != 2 or text.shape[0] < 2 or text.shape[1] % 2:
        raise ValueError("text must be [N,even D] with N >= 2")
    half = text.shape[1] // 2
    source_indices = [(index + 1) % text.shape[0] for index in range(text.shape[0])]
    shuffled = text.clone()
    shuffled[:, :half] = text[source_indices, :half]
    if not torch.equal(shuffled[:, half:], text[:, half:]):
        raise RuntimeError("cyclic camera-text shuffle changed the human-text half")
    return shuffled, source_indices


@torch.no_grad()
def predict_shared_xt_conditions(
    model: torch.nn.Module,
    diffusion: Any,
    train_mod: Any,
    z: torch.Tensor,
    condition_text: dict[str, torch.Tensor],
    valid: torch.Tensor,
    task_id: int,
    sample_indices: list[int],
    seed: int,
    timestep: int,
    *,
    task_routing: str,
) -> tuple[dict[str, torch.Tensor], torch.Tensor, torch.Tensor]:
    """Mirror official single-step x0 while sharing one noise/x_t across conditions."""
    if set(condition_text) != set(CONDITIONS):
        raise ValueError(f"expected exactly conditions {CONDITIONS}")
    if not 0 <= timestep < diffusion.num_timesteps:
        raise ValueError("timestep is outside the process")
    task = torch.full((z.shape[0],), task_id, dtype=torch.long, device=z.device)
    obs_mask, _ = train_mod.make_branch_masks(z, valid, task, task_routing=task_routing)
    valid_bc = valid[:, None, :].expand_as(z)
    expected_human_obs = valid[:, None, :].expand(-1, train_mod.HUM_DIM, -1)
    if not torch.equal(obs_mask[:, : train_mod.HUM_DIM], expected_human_obs):
        raise RuntimeError("Direct-C must observe the valid GT human latent")
    if obs_mask[:, train_mod.HUM_DIM :].any():
        raise RuntimeError("Direct-C camera target must remain unobserved")
    noise = full_eval.deterministic_noise(tuple(z.shape), sample_indices, seed, z.device, z.dtype)
    if getattr(diffusion, "name", "diffusion") == "rectified_flow":
        t_value = float(timestep) / float(max(diffusion.num_timesteps - 1, 1))
        t = torch.full((z.shape[0],), t_value, dtype=z.dtype, device=z.device)
    else:
        t = torch.full((z.shape[0],), timestep, dtype=torch.long, device=z.device)
    x_t = diffusion.q_sample(z, t, noise)
    source_meta = train_mod.build_source_meta(obs_mask, train_mod.SOURCE_GT)
    outputs: dict[str, torch.Tensor] = {}
    for condition in CONDITIONS:
        pred = train_mod.predict_with_joint_coupling(
            model,
            x_t,
            diffusion.model_t(t),
            condition_text[condition],
            z,
            obs_mask,
            task,
            source_meta,
            1.0,
            "symmetric",
        )
        pred_x0 = diffusion.prediction_to_x0(pred, x_t, t)
        completion = torch.where(obs_mask, z, pred_x0)
        outputs[condition] = torch.where(valid_bc, completion, z)
    return outputs, noise, x_t


def difference_record(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    """Return first-minus-second for residual statistics."""
    return {
        "channel": {
            field: (
                np.asarray(first["channel"][field], dtype=np.float64)
                - np.asarray(second["channel"][field], dtype=np.float64)
            ).tolist()
            for field in FIELDS
        },
        "sample": {
            field: float(first["sample"][field] - second["sample"][field])
            for field in FIELDS
        },
    }


def summarize_advantage(records: list[dict[str, Any]], key: str) -> dict[str, Any]:
    output: dict[str, Any] = {"sample": {}, "channel": {}}
    for field in FIELDS:
        values = np.asarray(
            [record["reliance_advantage"][key]["sample"][field] for record in records],
            dtype=np.float64,
        )
        output["sample"][field] = {
            **scalar_summary(values),
            "positive_fraction": float((values > 0).mean()),
        }
        channels = np.asarray(
            [record["reliance_advantage"][key]["channel"][field] for record in records],
            dtype=np.float64,
        )
        output["channel"][field] = {
            "mean_across_samples": channels.mean(axis=0).tolist(),
            "median_across_samples": np.median(channels, axis=0).tolist(),
        }
    return output


def summarize_geometry_advantage(records: list[dict[str, Any]]) -> dict[str, Any]:
    output = {}
    for field in GEOMETRY_FIELDS:
        values = np.asarray(
            [record["reliance_advantage"]["decoded_geometry"][field] for record in records],
            dtype=np.float64,
        )
        output[field] = {
            **scalar_summary(values),
            "positive_fraction": float((values > 0).mean()),
        }
    return output


def _resolve_contract_path(story_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else story_root / path


def init_contract(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite contract: {output}")
    story_root = args.story_root.resolve()
    source_contract_path = args.source_contract.resolve()
    source_contract = json.loads(source_contract_path.read_text(encoding="utf-8"))
    diagnostic = source_contract["diagnostic_evals"]["d4_directc_single_step_n64"]
    checkpoint = (args.checkpoint or args.run_dir / "last.pt").resolve()
    cache_path = (args.cache_dir / args.cache_file).resolve()
    if sha256_file(checkpoint) != diagnostic["checkpoint"]["sha256"]:
        raise RuntimeError("checkpoint hash differs from the audited D4 source contract")
    if sha256_file(cache_path) != source_contract["cache"]["eval_sha256"]:
        raise RuntimeError("eval-cache hash differs from the audited D4 source contract")
    raw_cache = torch.load(cache_path, map_location="cpu")
    cache_meta = dict(raw_cache.get("meta", {}))
    train_mod = load_module(
        "train_stage2_condmdi_pulp_d42_contract",
        story_root / "scripts/train_stage2_condmdi_pulp.py",
    )
    train_mod.assert_non_causal_cache_meta(cache_meta)
    if not args.allow_nondefault_tokenizer_contract:
        train_mod.assert_default_cache_meta(cache_meta)
    sample_ids = [str(value) for value in raw_cache["sample_id"][:64]]
    if sha256_ids(sample_ids) != diagnostic["ordered_ids_sha256"]:
        raise RuntimeError("first-N64 ordered IDs differ from the audited D4 source contract")
    reference_raw = args.reference_raw_artifact.resolve()
    if not reference_raw.is_file():
        raise FileNotFoundError(reference_raw)
    output_dir = args.output_dir.resolve()
    payload = {
        "schema_version": 1,
        "stage": "stage2",
        "kind": "D4.2_Direct-C_camera_text_reliance_child_contract",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "run_id": source_contract["run_id"],
        "version": source_contract["version"],
        "diagnostic_only": True,
        "promotion_eligible": False,
        "parent_experiment_contract": {
            "path": str(source_contract_path),
            "sha256": sha256_file(source_contract_path),
        },
        "source_stage2": {
            "run_dir": str(args.run_dir.resolve()),
            "checkpoint": str(checkpoint),
            "checkpoint_sha256": sha256_file(checkpoint),
            "checkpoint_step": int(diagnostic["checkpoint"]["step"]),
        },
        "cache": {
            "path": str(cache_path),
            "sha256": sha256_file(cache_path),
            "train_sha256": source_contract["cache"]["train_sha256"],
            "z_norm_source_train_sha256": source_contract["cache"]["z_norm_source_train_sha256"],
            "tokenizer_checkpoint_sha256": source_contract["cache"]["tokenizer_checkpoint_sha256"],
            "is_causal": False,
        },
        "parent_stage1": source_contract["parent_stage1"],
        "eval": {
            "task": "camera",
            "task_contract": "Direct-C with clean observed GT human latent plus camera text",
            "split": "test",
            "set_name": "pure_",
            "sample_count": 64,
            "ordered_ids_sha256": sha256_ids(sample_ids),
            "seed": 17,
            "noise_seed_base": 8026,
            "per_sample_noise_formula": "noise_seed_base + sample_index * 1000003",
            "timesteps": [50, 500, 950],
            "batch_size": 16,
            "decode_batch_size": 8,
            "conditions": list(CONDITIONS),
            "condition_contract": {
                "text_layout": "camera first half; human second half",
                "aligned": "original paired camera and human text",
                "cyclic_shuffled_camera_text": (
                    "target ordered index i receives camera-text half from (i+1) mod 64; "
                    "human-text half remains target-aligned"
                ),
                "shared_state": "one deterministic noise tensor and one q(z_gt,t) x_t tensor reused by both forwards",
            },
        },
        "reference_raw_artifact": {
            "path": str(reference_raw),
            "sha256": sha256_file(reference_raw),
        },
        "implementation": {
            "recorder": str(Path(__file__).resolve()),
            "recorder_sha256": sha256_file(Path(__file__).resolve()),
            "official_full_eval_sha256": sha256_file(story_root / "scripts/storymotion_official_full_eval.py"),
            "stage2_model_sha256": sha256_file(story_root / "scripts/train_stage2_condmdi_pulp.py"),
        },
        "output_dir": str(output_dir),
        "restrictions": [
            "no training",
            "no checkpoint or cache write",
            "no cascade",
            "no blank-text arm",
            "no N256",
            "no 105K continuation",
            "diagnostic screen only",
        ],
        "status": "preregistered",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output, payload)
    print(json.dumps({"ok": True, "contract": str(output), "sha256": sha256_file(output)}, sort_keys=True))


def validate_diagnostic_contract(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    path = args.diagnostic_contract.resolve()
    contract = json.loads(path.read_text(encoding="utf-8"))
    failures = []

    def check(label: str, actual: Any, expected: Any) -> None:
        if actual != expected:
            failures.append({"field": label, "actual": actual, "expected": expected})

    check("kind", contract.get("kind"), "D4.2_Direct-C_camera_text_reliance_child_contract")
    check("promotion_eligible", contract.get("promotion_eligible"), False)
    check("recorder_sha256", contract["implementation"]["recorder_sha256"], sha256_file(Path(__file__).resolve()))
    check("checkpoint_sha256", contract["source_stage2"]["checkpoint_sha256"], sha256_file((args.checkpoint or args.run_dir / "last.pt").resolve()))
    check("cache_sha256", contract["cache"]["sha256"], sha256_file((args.cache_dir / args.cache_file).resolve()))
    check("is_causal", contract["cache"]["is_causal"], False)
    if not args.preflight:
        check("output_dir", Path(contract["output_dir"]).resolve(), args.output_dir.resolve())
        check("sample_count", contract["eval"]["sample_count"], args.samples)
        check("timesteps", contract["eval"]["timesteps"], list(args.timesteps))
        check("batch_size", contract["eval"]["batch_size"], args.batch_size)
        check("decode_batch_size", contract["eval"]["decode_batch_size"], args.decode_batch_size)
    if failures:
        raise RuntimeError(f"D4.2 contract audit failed: {json.dumps(failures, sort_keys=True)}")
    return contract, {
        "status": "passed" if not args.preflight else "preflight",
        "contract": str(path),
        "contract_sha256": sha256_file(path),
        "checked_fields": [
            "kind",
            "promotion_eligible",
            "recorder_sha256",
            "checkpoint_sha256",
            "cache_sha256",
            "is_causal",
            "output/sample/timestep/batch contract" if not args.preflight else "preflight subset",
        ],
    }


def reference_raw_audit(
    artifact_path: Path,
    timestep: int,
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    record_path = artifact_path.parent / artifact["files"][str(timestep)]["records"]
    reference = _read_jsonl(record_path)
    expected_ids = [record["sample_id"] for record in records]
    if [record["sample_id"] for record in reference[: len(records)]] != expected_ids:
        raise RuntimeError("D4 raw reference ordered IDs differ")
    maxima = {"model_space": 0.0, "decoder_input_space": 0.0, "decoded_geometry": 0.0}
    for current, prior in zip(records, reference):
        for space in ("model_space", "decoder_input_space"):
            for field in FIELDS:
                maxima[space] = max(
                    maxima[space],
                    abs(current["aligned"][space]["sample"][field] - prior[space]["sample"][field]),
                )
        for field in GEOMETRY_FIELDS:
            maxima["decoded_geometry"] = max(
                maxima["decoded_geometry"],
                abs(current["aligned"]["decoded_geometry"][field] - prior["decoded_geometry"][field]),
            )
    # The preflight may use a smaller batch than the audited N64 source.  CUDA
    # convolution/decoder kernels then differ at low floating-point bits even
    # with identical x_t.  These bounds are far below a changed-noise result;
    # formal N64 retains the original batch topology and is typically tighter.
    tolerances = {
        "model_space": 1.0e-4,
        "decoder_input_space": 1.0e-4,
        "decoded_geometry": 1.0e-2,
    }
    failures = {key: value for key, value in maxima.items() if value > tolerances[key]}
    if failures:
        raise RuntimeError(f"aligned path does not reproduce D4 raw artifact: {failures}")
    return {
        "status": "passed",
        "artifact": str(artifact_path),
        "artifact_sha256": sha256_file(artifact_path),
        "records": str(record_path),
        "records_sha256": sha256_file(record_path),
        "max_abs_delta": maxima,
        "tolerance": tolerances,
    }


def _decode_geometry(
    completion_decoder: torch.Tensor,
    sample_ids: list[str],
    dataset: Any,
    owning_decoder: dict[str, Any],
    train_mod: Any,
    device: torch.device,
    decode_batch_size: int,
) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for decode_slice in full_eval.iter_slices(len(sample_ids), decode_batch_size):
        chunk_ids = sample_ids[decode_slice]
        pulp_batch = batch_from_sample_ids(dataset, chunk_ids, device)
        intrinsics = pulp_batch["x_raw"]["intrinsics"]
        _, raw_input = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
        _, raw_output = decode_with_owning_decoder(
            owning_decoder,
            dataset,
            train_mod,
            completion_decoder[decode_slice],
            intrinsics,
            pulp_batch["padding_mask"],
        )
        geometry = paired_geometry_batch(
            {"raw_input": raw_input, "raw_output": raw_output}, pulp_batch, chunk_ids
        )
        output.update({str(record["sample_id"]): record for record in geometry})
    return output


def record(args: argparse.Namespace) -> None:
    if not args.preflight:
        if args.output_dir.name != ARTIFACT_DIR_NAME:
            raise ValueError(f"formal output directory must be named {ARTIFACT_DIR_NAME}")
        if args.samples != 64 or tuple(args.timesteps) != DEFAULT_TIMESTEPS:
            raise ValueError("formal D4.2 requires N64 and t=50,500,950")
    if args.samples <= 1:
        if not args.preflight:
            raise ValueError("formal cyclic shuffle needs N64")
    if len(set(args.timesteps)) != len(args.timesteps):
        raise ValueError("timesteps must be unique")
    contract, contract_audit = validate_diagnostic_contract(args)
    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"refusing to overwrite artifact directory: {output_dir}")
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
        train_mod = load_module(
            "train_stage2_condmdi_pulp_d42_record", story_root / "scripts/train_stage2_condmdi_pulp.py"
        )
        cache_mod = load_module(
            "build_stage2_pulp_latent_cache_d42_record",
            story_root / "scripts/build_stage2_pulp_latent_cache.py",
        )
        model, diffusion, run_info = load_stage2(
            args.run_dir.resolve(), train_mod, device, checkpoint_path=args.checkpoint
        )
        if getattr(diffusion, "prediction_type", None) != "START_X":
            raise RuntimeError("D4.2 requires START_X")
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
        if not args.preflight and sha256_ids(selected_ids) != contract["eval"]["ordered_ids_sha256"]:
            raise RuntimeError("formal ordered IDs differ from D4.2 contract")
        selected_text = cache.text[: args.samples].clone()
        shuffled_text, shuffled_source_indices = cyclic_shuffle_camera_text(selected_text)
        shuffled_source_ids = [selected_ids[index] for index in shuffled_source_indices]
        half = selected_text.shape[1] // 2
        text_audit = {
            "aligned_camera_text_sha256": sha256_tensor(selected_text[:, :half]),
            "shuffled_camera_text_sha256": sha256_tensor(shuffled_text[:, :half]),
            "aligned_human_text_sha256": sha256_tensor(selected_text[:, half:]),
            "shuffled_human_text_sha256": sha256_tensor(shuffled_text[:, half:]),
            "human_text_exactly_unchanged": bool(torch.equal(selected_text[:, half:], shuffled_text[:, half:])),
            "camera_text_exactly_unchanged_count": int(
                torch.all(selected_text[:, :half] == shuffled_text[:, :half], dim=1).sum().item()
            ),
            "source_index_formula": "(target_index + 1) mod N",
            "mapping_sha256": sha256_ids(
                f"{target_id}\t{source_id}" for target_id, source_id in zip(selected_ids, shuffled_source_ids)
            ),
        }
        loader, end = full_eval.collate_cache(cache, 0, args.samples, args.batch_size, args.workers)
        if end != args.samples:
            raise RuntimeError("cache slice is shorter than requested")
        task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}["camera"]
        task_routing = str(run_info.get("task_routing", "symmetric"))
        by_timestep: dict[int, list[dict[str, Any]]] = {timestep: [] for timestep in args.timesteps}
        started = time.time()
        processed = 0
        with torch.no_grad():
            for batch_index, batch in enumerate(loader):
                z = batch["z"].to(device)
                valid = batch["valid"].to(device)
                sample_ids = [str(value) for value in batch["sample_id"]]
                sample_indices = list(range(processed, processed + len(sample_ids)))
                aligned_text = selected_text[processed : processed + len(sample_ids)].to(device)
                cyclic_text = shuffled_text[processed : processed + len(sample_ids)].to(device)
                if not torch.equal(batch["text"], aligned_text.cpu()):
                    raise RuntimeError("loader text differs from the ordered selected text")
                target_decoder = train_mod.denormalize_latent(z, valid, znorm_stats)
                for timestep in args.timesteps:
                    completions, shared_noise, shared_x_t = predict_shared_xt_conditions(
                        model,
                        diffusion,
                        train_mod,
                        z,
                        {
                            "aligned": aligned_text,
                            "cyclic_shuffled_camera_text": cyclic_text,
                        },
                        valid,
                        task_id,
                        sample_indices,
                        args.seed + 8009,
                        timestep,
                        task_routing=task_routing,
                    )
                    condition_payload: dict[str, Any] = {}
                    per_condition_stats: dict[str, Any] = {}
                    for condition in CONDITIONS:
                        completion = completions[condition]
                        completion_decoder = train_mod.denormalize_latent(
                            completion, valid, znorm_stats
                        )
                        model_stats = camera_residual_records(
                            completion, z, valid, train_mod.HUM_DIM
                        )
                        decoder_stats = camera_residual_records(
                            completion_decoder, target_decoder, valid, train_mod.HUM_DIM
                        )
                        geometry = _decode_geometry(
                            completion_decoder,
                            sample_ids,
                            dataset,
                            owning_decoder,
                            train_mod,
                            device,
                            args.decode_batch_size,
                        )
                        per_condition_stats[condition] = {
                            "model": model_stats,
                            "decoder": decoder_stats,
                            "geometry": geometry,
                        }
                        condition_payload[condition] = completion
                    effect_model = camera_residual_records(
                        condition_payload["cyclic_shuffled_camera_text"],
                        condition_payload["aligned"],
                        valid,
                        train_mod.HUM_DIM,
                    )
                    aligned_decoder = train_mod.denormalize_latent(
                        condition_payload["aligned"], valid, znorm_stats
                    )
                    shuffled_decoder = train_mod.denormalize_latent(
                        condition_payload["cyclic_shuffled_camera_text"], valid, znorm_stats
                    )
                    effect_decoder = camera_residual_records(
                        shuffled_decoder, aligned_decoder, valid, train_mod.HUM_DIM
                    )
                    for local_index, sample_id in enumerate(sample_ids):
                        aligned_geometry = per_condition_stats["aligned"]["geometry"][sample_id]
                        shuffled_geometry = per_condition_stats["cyclic_shuffled_camera_text"]["geometry"][sample_id]
                        aligned = {
                            "model_space": per_condition_stats["aligned"]["model"][local_index],
                            "decoder_input_space": per_condition_stats["aligned"]["decoder"][local_index],
                            "decoded_geometry": {
                                field: float(aligned_geometry[field]) for field in GEOMETRY_FIELDS
                            },
                        }
                        shuffled = {
                            "model_space": per_condition_stats["cyclic_shuffled_camera_text"]["model"][local_index],
                            "decoder_input_space": per_condition_stats["cyclic_shuffled_camera_text"]["decoder"][local_index],
                            "decoded_geometry": {
                                field: float(shuffled_geometry[field]) for field in GEOMETRY_FIELDS
                            },
                        }
                        by_timestep[timestep].append(
                            {
                                "sample_id": sample_id,
                                "sample_index": sample_indices[local_index],
                                "shuffled_camera_text_source_index": shuffled_source_indices[sample_indices[local_index]],
                                "shuffled_camera_text_source_id": shuffled_source_ids[sample_indices[local_index]],
                                "per_sample_noise_seed": args.seed + 8009 + sample_indices[local_index] * 1_000_003,
                                "shared_noise_sha256": sha256_tensor(shared_noise[local_index]),
                                "shared_x_t_sha256": sha256_tensor(shared_x_t[local_index]),
                                "valid_latent_frames": int(valid[local_index].sum().item()),
                                "valid_decoded_frames": int(aligned_geometry["valid_frames"]),
                                "aligned": aligned,
                                "cyclic_shuffled_camera_text": shuffled,
                                "condition_effect_shuffled_minus_aligned": {
                                    "model_space": effect_model[local_index],
                                    "decoder_input_space": effect_decoder[local_index],
                                },
                                "reliance_advantage": {
                                    "model_space": difference_record(
                                        shuffled["model_space"], aligned["model_space"]
                                    ),
                                    "decoder_input_space": difference_record(
                                        shuffled["decoder_input_space"], aligned["decoder_input_space"]
                                    ),
                                    "decoded_geometry": {
                                        field: float(
                                            shuffled["decoded_geometry"][field]
                                            - aligned["decoded_geometry"][field]
                                        )
                                        for field in GEOMETRY_FIELDS
                                    },
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

        files: dict[str, Any] = {}
        reference_raw_artifact = Path(contract["reference_raw_artifact"]["path"])
        for timestep, records in by_timestep.items():
            if [record["sample_id"] for record in records] != selected_ids:
                raise RuntimeError("record order changed")
            records_name = f"t{timestep:03d}.records.jsonl"
            summary_name = f"t{timestep:03d}.summary.json"
            records_path = temp_dir / records_name
            summary_path = temp_dir / summary_name
            _write_jsonl(records_path, records)
            aligned_flat = [
                {
                    "model_space": record["aligned"]["model_space"],
                    "decoder_input_space": record["aligned"]["decoder_input_space"],
                    "decoded_geometry": record["aligned"]["decoded_geometry"],
                }
                for record in records
            ]
            shuffled_flat = [
                {
                    "model_space": record["cyclic_shuffled_camera_text"]["model_space"],
                    "decoder_input_space": record["cyclic_shuffled_camera_text"]["decoder_input_space"],
                    "decoded_geometry": record["cyclic_shuffled_camera_text"]["decoded_geometry"],
                }
                for record in records
            ]
            summary = {
                "schema_version": 1,
                "kind": "D4.2_Direct-C_camera_text_reliance_timestep",
                "timestep": timestep,
                "samples": len(records),
                "ordered_ids_sha256": sha256_ids(selected_ids),
                "aligned": {
                    "model_space": summarize_residual_records(aligned_flat, "model_space"),
                    "decoder_input_space": summarize_residual_records(aligned_flat, "decoder_input_space"),
                    "decoded_geometry": summarize_geometry(aligned_flat),
                },
                "cyclic_shuffled_camera_text": {
                    "model_space": summarize_residual_records(shuffled_flat, "model_space"),
                    "decoder_input_space": summarize_residual_records(shuffled_flat, "decoder_input_space"),
                    "decoded_geometry": summarize_geometry(shuffled_flat),
                },
                "condition_effect_shuffled_minus_aligned": {
                    space: summarize_residual_records(
                        [
                            {
                                space: record["condition_effect_shuffled_minus_aligned"][space]
                            }
                            for record in records
                        ],
                        space,
                    )
                    for space in ("model_space", "decoder_input_space")
                },
                "reliance_advantage_shuffled_error_minus_aligned_error": {
                    "model_space": summarize_advantage(records, "model_space"),
                    "decoder_input_space": summarize_advantage(records, "decoder_input_space"),
                    "decoded_geometry": summarize_geometry_advantage(records),
                },
                "aligned_official_geometry_reproduction": reference_audit(
                    args.reference_eval_dir.resolve(), timestep, aligned_flat, selected_ids
                ),
                "aligned_raw_residual_reproduction": reference_raw_audit(
                    reference_raw_artifact, timestep, records
                ),
                "records": records_name,
                "records_sha256": sha256_file(records_path),
            }
            _write_json(summary_path, summary)
            files[str(timestep)] = {
                "records": records_name,
                "records_sha256": sha256_file(records_path),
                "summary": summary_name,
                "summary_sha256": sha256_file(summary_path),
            }

        artifact = {
            "schema_version": 1,
            "kind": "D4.2_Direct-C_camera_text_reliance",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "diagnostic_only": True,
            "promotion_eligible": False,
            "preflight": bool(args.preflight),
            "scientific_boundary": (
                "Paired teacher-forced one-step Direct-C camera-text reliance screen. "
                "It tests whether changing camera text changes x0 error/geometry under fixed GT-H "
                "and shared x_t; it does not measure full-reverse semantic generation or prove why training learned that reliance."
            ),
            "run": run_info,
            "diagnostic_contract": {
                "path": str(args.diagnostic_contract.resolve()),
                "sha256": sha256_file(args.diagnostic_contract.resolve()),
                "audit": contract_audit,
            },
            "identity_audit": {
                "status": "passed" if not args.preflight else "preflight",
                "checkpoint_sha256": run_info["checkpoint_sha256"],
                "checkpoint_step": run_info["step"],
                "cache_path": str(cache_path),
                "cache_sha256": sha256_file(cache_path),
                "cache_sample_ids_sha256": cache_meta["sample_ids_sha256"],
                "selected_ordered_ids_sha256": sha256_ids(selected_ids),
                "selected_ordered_ids": selected_ids,
                "latent_znorm": znorm_record,
                "owning_decoder": owning_decoder_record,
                "is_causal": False,
                "text": text_audit,
                "implementation_sha256": {
                    "recorder": sha256_file(Path(__file__).resolve()),
                    "official_full_eval": sha256_file(story_root / "scripts/storymotion_official_full_eval.py"),
                    "stage2_model": sha256_file(story_root / "scripts/train_stage2_condmdi_pulp.py"),
                },
            },
            "eval": {
                "task": "camera",
                "samples": args.samples,
                "timesteps": list(args.timesteps),
                "seed": args.seed,
                "noise_seed_base": args.seed + 8009,
                "per_sample_noise_formula": "noise_seed_base + sample_index * 1000003",
                "conditions": list(CONDITIONS),
                "shared_state": "one noise and x_t tensor reused for aligned and shuffled forwards",
                "batch_size": args.batch_size,
                "decode_batch_size": args.decode_batch_size,
                "task_routing": task_routing,
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


def _load_artifact_records(artifact_path: Path, timestep: int) -> list[dict[str, Any]]:
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
    record = artifact["files"][str(timestep)]
    path = artifact_path.parent / record["records"]
    if sha256_file(path) != record["records_sha256"]:
        raise RuntimeError(f"records hash mismatch: {path}")
    return _read_jsonl(path)


def compare(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"refusing to overwrite comparison: {output}")
    baseline_path = args.baseline.resolve()
    candidate_path = args.candidate.resolve()
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
    for name, artifact in (("baseline", baseline), ("candidate", candidate)):
        if artifact.get("kind") != "D4.2_Direct-C_camera_text_reliance":
            raise ValueError(f"{name} artifact kind is wrong")
        if artifact.get("preflight") or artifact["identity_audit"]["status"] != "passed":
            raise ValueError(f"{name} is not a passed formal artifact")
    equality = {
        "ordered_ids_sha256": (
            baseline["identity_audit"]["selected_ordered_ids_sha256"],
            candidate["identity_audit"]["selected_ordered_ids_sha256"],
        ),
        "timesteps": (baseline["eval"]["timesteps"], candidate["eval"]["timesteps"]),
        "seed": (baseline["eval"]["seed"], candidate["eval"]["seed"]),
        "noise_seed_base": (baseline["eval"]["noise_seed_base"], candidate["eval"]["noise_seed_base"]),
        "conditions": (baseline["eval"]["conditions"], candidate["eval"]["conditions"]),
        "samples": (baseline["eval"]["samples"], candidate["eval"]["samples"]),
        "text_mapping_sha256": (
            baseline["identity_audit"]["text"]["mapping_sha256"],
            candidate["identity_audit"]["text"]["mapping_sha256"],
        ),
    }
    mismatches = {key: values for key, values in equality.items() if values[0] != values[1]}
    if mismatches:
        raise RuntimeError(f"matched D4.2 identity failed: {mismatches}")

    comparisons: dict[str, Any] = {}
    ordered_ids = baseline["identity_audit"]["selected_ordered_ids"]
    for timestep in baseline["eval"]["timesteps"]:
        base_rows = _load_artifact_records(baseline_path, int(timestep))
        cand_rows = _load_artifact_records(candidate_path, int(timestep))
        if [row["sample_id"] for row in base_rows] != ordered_ids or [row["sample_id"] for row in cand_rows] != ordered_ids:
            raise RuntimeError("comparison record order differs")
        row: dict[str, Any] = {
            "matched_samples": len(ordered_ids),
            "condition_effect_rms": {},
            "reliance_advantage_shuffled_error_minus_aligned_error": {},
        }
        for space in ("model_space", "decoder_input_space"):
            base_effect = np.asarray(
                [r["condition_effect_shuffled_minus_aligned"][space]["sample"]["rms"] for r in base_rows]
            )
            cand_effect = np.asarray(
                [r["condition_effect_shuffled_minus_aligned"][space]["sample"]["rms"] for r in cand_rows]
            )
            row["condition_effect_rms"][space] = {
                "baseline": scalar_summary(base_effect),
                "candidate": scalar_summary(cand_effect),
                "candidate_minus_baseline": scalar_summary(cand_effect - base_effect),
                "candidate_to_baseline_mean_ratio": float(
                    cand_effect.mean() / max(base_effect.mean(), RELATIVE_EPS)
                ),
                "candidate_larger_fraction": float((cand_effect > base_effect).mean()),
            }
            row["reliance_advantage_shuffled_error_minus_aligned_error"][space] = {}
            for field in ("rms", "mae", "relative_error"):
                base_adv = np.asarray(
                    [r["reliance_advantage"][space]["sample"][field] for r in base_rows]
                )
                cand_adv = np.asarray(
                    [r["reliance_advantage"][space]["sample"][field] for r in cand_rows]
                )
                row["reliance_advantage_shuffled_error_minus_aligned_error"][space][field] = {
                    "baseline": {**scalar_summary(base_adv), "positive_fraction": float((base_adv > 0).mean())},
                    "candidate": {**scalar_summary(cand_adv), "positive_fraction": float((cand_adv > 0).mean())},
                    "candidate_minus_baseline": scalar_summary(cand_adv - base_adv),
                }
        row["reliance_advantage_shuffled_error_minus_aligned_error"]["decoded_geometry"] = {}
        for field in GEOMETRY_FIELDS:
            base_adv = np.asarray([r["reliance_advantage"]["decoded_geometry"][field] for r in base_rows])
            cand_adv = np.asarray([r["reliance_advantage"]["decoded_geometry"][field] for r in cand_rows])
            row["reliance_advantage_shuffled_error_minus_aligned_error"]["decoded_geometry"][field] = {
                "baseline": {**scalar_summary(base_adv), "positive_fraction": float((base_adv > 0).mean())},
                "candidate": {**scalar_summary(cand_adv), "positive_fraction": float((cand_adv > 0).mean())},
                "candidate_minus_baseline": scalar_summary(cand_adv - base_adv),
            }
        for space in ("model_space", "decoder_input_space"):
            row.setdefault("advantage_geometry_association", {})[space] = {}
            for field in GEOMETRY_FIELDS:
                row["advantage_geometry_association"][space][field] = {
                    "baseline": correlation(
                        (r["reliance_advantage"][space]["sample"]["rms"] for r in base_rows),
                        (r["reliance_advantage"]["decoded_geometry"][field] for r in base_rows),
                    ),
                    "candidate": correlation(
                        (r["reliance_advantage"][space]["sample"]["rms"] for r in cand_rows),
                        (r["reliance_advantage"]["decoded_geometry"][field] for r in cand_rows),
                    ),
                }
        comparisons[str(timestep)] = row

    payload = {
        "schema_version": 1,
        "kind": "D4.2_Direct-C_camera_text_reliance_matched_comparison",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "diagnostic_only": True,
        "promotion_eligible": False,
        "baseline": {"artifact": str(baseline_path), "sha256": sha256_file(baseline_path), "run": baseline["run"]},
        "candidate": {"artifact": str(candidate_path), "sha256": sha256_file(candidate_path), "run": candidate["run"]},
        "matched_identity_audit": {"status": "passed", **{key: values[0] for key, values in equality.items()}},
        "interpretation_contract": {
            "condition_effect": "RMS of shuffled-x0 minus aligned-x0; magnitude only, not correctness",
            "reliance_advantage": (
                "shuffled condition error minus aligned condition error; positive means aligned camera text improves paired recovery"
            ),
            "boundary": (
                "A weak/negative one-step advantage supports missing or misdirected semantic reliance under GT-H, "
                "but does not identify whether the cause is representation, optimizer, loss weighting, or full-reverse sampling."
            ),
        },
        "timesteps": comparisons,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    _write_json(output, payload)
    print(json.dumps({"ok": True, "comparison": str(output)}, sort_keys=True))


def _add_source_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--story-root", type=Path, default=ROOT)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--cache-dir", type=Path, required=True)
    parser.add_argument("--cache-file", default="val.pt")
    parser.add_argument("--allow-nondefault-tokenizer-contract", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init-contract")
    _add_source_args(init_parser)
    init_parser.add_argument("--source-contract", type=Path, required=True)
    init_parser.add_argument("--reference-raw-artifact", type=Path, required=True)
    init_parser.add_argument("--output-dir", type=Path, required=True)
    init_parser.add_argument("--output", type=Path, required=True)
    init_parser.set_defaults(func=init_contract)

    record_parser = subparsers.add_parser("record")
    _add_source_args(record_parser)
    record_parser.add_argument("--diagnostic-contract", type=Path, required=True)
    record_parser.add_argument("--reference-eval-dir", type=Path, required=True)
    record_parser.add_argument("--output-dir", type=Path, required=True)
    record_parser.add_argument("--preflight", action="store_true")
    record_parser.add_argument("--samples", type=int, default=64)
    record_parser.add_argument("--timesteps", nargs="+", type=int, default=list(DEFAULT_TIMESTEPS))
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

    compare_parser = subparsers.add_parser("compare")
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
