#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storymotion_official_bridge_smoke import (
    batch_from_sample_ids,
    build_pulp,
    instantiate_official_metrics,
    jsonable,
    load_module,
    load_stage2,
    metric_checkpoint_status,
    metric_values,
    official_outputs_for_task,
    patch_numpy_aliases,
    reference_feature_and_raw,
)
from storymotion_official_full_eval import (
    apply_observed_latent_intervention,
    apply_text_intervention,
    collate_cache,
    human_motion_stats_for_batch,
    sample_start_x,
    sha256_file,
    sha256_tensor,
    summarize_human_motion_stats,
    write_records,
)
from scripts.build_stage2_joint_tokenizer_latent_cache import build_model as build_source_tokenizer
from storymotion.training.camera_data import camera_features_to_poses
from storymotion.training.joint_data import (
    LEGACY_FEATURE_CONTRACT,
    OFFICIAL_FEATURE_CONTRACT,
    RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
    RAW_OFFICIAL_FEATURE_CONTRACT,
    _load_official_stats,
    official_raw_to_normalized,
)
from storymotion.training.human200 import (  # noqa: E402
    HUMAN200_FEATURE_CONTRACT,
    human200_to_official_human199,
)


def _torch_load(path: Path) -> Any:
    try:
        return torch.load(path, map_location="cpu", weights_only=False)
    except TypeError:
        return torch.load(path, map_location="cpu")


def load_cache_meta(path: Path) -> dict[str, Any]:
    data = _torch_load(path)
    meta = data.get("meta", {}) if isinstance(data, dict) else {}
    return jsonable(meta)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"1", "true", "yes", "on"}


def load_run_meta(run_dir: Path) -> dict[str, Any]:
    meta_path = run_dir / "meta.json"
    if not meta_path.exists():
        return {}
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return meta if isinstance(meta, dict) else {}


def load_run_args(run_dir: Path) -> dict[str, Any]:
    meta = load_run_meta(run_dir)
    return meta.get("args", {}) if isinstance(meta, dict) else {}


def resolve_eval_znorm_stats(
    args: argparse.Namespace,
    run_meta: dict[str, Any],
    train_mod: Any,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    run_znorm = run_meta.get("latent_znorm", {}) if isinstance(run_meta, dict) else {}
    requested = bool(args.znorm or args.znorm_stats_path is not None or run_znorm.get("enabled", False))
    if not requested:
        return None, {"enabled": False}

    path_value = args.znorm_stats_path or run_znorm.get("stats_path") or train_mod.latent_znorm_default_stats_path(args.cache_dir)
    stats_path = Path(path_value)
    if not stats_path.exists() and not stats_path.is_absolute():
        run_relative = args.run_dir / stats_path
        if run_relative.exists():
            stats_path = run_relative
    stats = train_mod.load_latent_znorm_stats(stats_path)
    record = train_mod.latent_znorm_meta(True, stats, stats_path, args.cache_dir / "train.pt")
    record["requested_by"] = {
        "arg_znorm": bool(args.znorm),
        "arg_stats_path": str(args.znorm_stats_path) if args.znorm_stats_path else None,
        "run_meta_enabled": bool(run_znorm.get("enabled", False)),
    }
    return stats, record


def load_tokenizer_from_cache_meta(
    cache_meta: dict[str, Any],
    args: argparse.Namespace,
    device: torch.device,
) -> torch.nn.Module:
    checkpoint = args.tokenizer_checkpoint or cache_meta.get("tokenizer_checkpoint")
    preset = args.tokenizer_preset or cache_meta.get("tokenizer_preset")
    if not checkpoint or not preset:
        raise ValueError("cache meta must provide tokenizer_checkpoint and tokenizer_preset, or pass overrides")
    namespace = argparse.Namespace(
        checkpoint=Path(checkpoint),
        preset=str(preset),
        tokenizer=None,
        drop_camera_z=parse_bool(cache_meta.get("drop_camera_z", False)),
        human_dim=int(cache_meta.get("human_feature_dim", 0) or 0) or None,
        camera_dim=int(cache_meta.get("camera_feature_dim", 0) or 0) or None,
        human_latent_dim=int(cache_meta.get("human_latent_dim", 0) or 0) or None,
        camera_latent_dim=int(cache_meta.get("camera_latent_dim", 0) or 0) or None,
        hidden_dim=None,
        downsample=None,
        feature_contract=str(cache_meta.get("feature_contract", LEGACY_FEATURE_CONTRACT)),
        human200_stats=(
            getattr(args, "human200_stats", None)
            or (cache_meta.get("human200_normalization") or {}).get("path")
        ),
    )
    model = build_source_tokenizer(namespace).to(device)
    model.eval()
    for param in model.parameters():
        param.requires_grad_(False)
    return model


def source_latent_to_native(z_hum_cam: torch.Tensor, train_mod: Any) -> torch.Tensor:
    if z_hum_cam.ndim != 3:
        raise ValueError(f"expected stage2 latent [B,C,T], got {tuple(z_hum_cam.shape)}")
    human = z_hum_cam[:, : train_mod.HUM_DIM].transpose(1, 2).contiguous()
    camera = z_hum_cam[:, train_mod.HUM_DIM :].transpose(1, 2).contiguous()
    return torch.cat([camera, human], dim=-1)


def joint_feature_dataset(dataset: Any) -> Any:
    return getattr(dataset, "joint_dataset", None) or dataset


def source_camera_to_raw(
    camera_feat: torch.Tensor,
    raw_input: dict[str, Any],
    padding_mask: torch.Tensor,
    no_z_depth_mode: str,
    task_name: str,
) -> tuple[torch.Tensor, str]:
    dim = int(camera_feat.shape[-1])
    policy = "source_camera_9d_translation_rot6d_to_c2w"
    if dim == 9:
        full = camera_feat
    elif dim == 8:
        if task_name == "human" and no_z_depth_mode == "error":
            return raw_input["camera"], "not_evaluated_gt_camera_passthrough_for_human_task"
        if no_z_depth_mode == "error":
            raise ValueError(
                "no-z source tokenizer emits 8D camera features; camera/joint official eval needs an explicit z-depth policy"
            )
        xy = camera_feat[..., :2]
        rot6d = camera_feat[..., 2:8]
        if no_z_depth_mode == "gt":
            z = raw_input["camera"][..., 2, 3:4].to(device=camera_feat.device, dtype=camera_feat.dtype)
            policy = "source_noz_xy_rot6d_with_gt_z_passthrough_diagnostic"
        elif no_z_depth_mode == "zero":
            z = torch.zeros_like(xy[..., :1])
            policy = "source_noz_xy_rot6d_with_zero_z_diagnostic"
        else:
            raise ValueError(f"unknown no_z_depth_mode: {no_z_depth_mode}")
        full = torch.cat([xy, z, rot6d], dim=-1)
    else:
        raise ValueError(f"expected camera feature dim 8 or 9, got {dim}")

    full = full.detach().float().cpu()
    masks = padding_mask.detach().bool().cpu().numpy()
    poses = []
    for index in range(full.shape[0]):
        arr = full[index].numpy()
        pose = camera_features_to_poses(arr)
        if not bool(masks[index].all()):
            gt_pose = raw_input["camera"][index].detach().float().cpu().numpy()
            pose[~masks[index]] = gt_pose[~masks[index]]
        poses.append(pose)
    raw = torch.from_numpy(np.stack(poses, axis=0)).to(device=camera_feat.device, dtype=camera_feat.dtype)
    return raw, policy


def decode_source_feature_and_raw(
    tokenizer: torch.nn.Module,
    dataset: Any,
    train_mod: Any,
    z_hum_cam: torch.Tensor,
    raw_input: dict[str, Any],
    intrinsics: torch.Tensor,
    padding_mask: torch.Tensor,
    task_name: str,
    no_z_depth_mode: str,
    feature_contract: str = LEGACY_FEATURE_CONTRACT,
    feature_stats: dict[str, torch.Tensor] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    native = source_latent_to_native(z_hum_cam, train_mod)
    human_feat, camera_feat = tokenizer.decode(native, target_len=int(padding_mask.shape[1]))
    human_feat = human_feat.float()
    camera_feat = camera_feat.float()
    human_feat = human_feat.masked_fill(~padding_mask[..., None], 0.0)
    camera_feat = camera_feat.masked_fill(~padding_mask[..., None], 0.0)

    feature_dataset = joint_feature_dataset(dataset)
    if feature_contract == HUMAN200_FEATURE_CONTRACT:
        if feature_stats is None or not hasattr(tokenizer, "human200_stats"):
            raise ValueError("v8.2 source decoding requires matched official and human200 statistics")
        human_normalized = torch.zeros(
            (*human_feat.shape[:-1], 199),
            device=human_feat.device,
            dtype=human_feat.dtype,
        )
        for index in range(human_feat.shape[0]):
            frames = int(padding_mask[index].sum().item())
            human_normalized[index, :frames] = human200_to_official_human199(
                human_feat[index, :frames],
                tokenizer.human200_stats,
                feature_stats["human_mean"],
                feature_stats["human_std"],
            )
        decoded = feature_dataset.get_raw(
            {"human": human_normalized, "camera": camera_feat}, intrinsics
        )
        human_raw = decoded["human"]
        camera_raw = decoded["camera"]
        camera_policy = "v8_2_human200_owning_inverse_plus_pulpmotion_official_camera14_joint_decoder"
        callback_human_feat = human_normalized
    elif feature_contract == OFFICIAL_FEATURE_CONTRACT:
        decoded = feature_dataset.get_raw({"human": human_feat, "camera": camera_feat}, intrinsics)
        human_raw = decoded["human"]
        camera_raw = decoded["camera"]
        camera_policy = "pulpmotion_official_camera14_joint_decoder"
        callback_human_feat = human_feat
    elif feature_contract == RAW_OFFICIAL_FEATURE_CONTRACT:
        if feature_stats is None:
            raise ValueError("raw official feature decoding requires official modality statistics")
        human_normalized, camera_normalized = official_raw_to_normalized(human_feat, camera_feat, feature_stats)
        decoded = feature_dataset.get_raw({"human": human_normalized, "camera": camera_normalized}, intrinsics)
        human_raw = decoded["human"]
        camera_raw = decoded["camera"]
        camera_policy = "raw_pulpmotion_camera14_inverse_normalization_then_joint_decoder"
        callback_human_feat = human_normalized
    elif feature_contract == RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT:
        if feature_stats is None:
            raise ValueError("raw-human official-camera decoding requires official modality statistics")
        human_mean = feature_stats["human_mean"].to(device=human_feat.device, dtype=human_feat.dtype)
        human_std = feature_stats["human_std"].to(device=human_feat.device, dtype=human_feat.dtype)
        human_normalized = (human_feat - human_mean) / human_std
        decoded = feature_dataset.get_raw({"human": human_normalized, "camera": camera_feat}, intrinsics)
        human_raw = decoded["human"]
        camera_raw = decoded["camera"]
        camera_policy = "raw_human_inverse_normalization_official_camera14_joint_decoder"
        callback_human_feat = human_normalized
    else:
        human_raw = feature_dataset.human_dataset.get_raw(feature_dataset.human_dataset.normalize(human_feat))
        camera_raw, camera_policy = source_camera_to_raw(camera_feat, raw_input, padding_mask, no_z_depth_mode, task_name)
        callback_human_feat = human_feat
    raw_output = {
        "human": human_raw,
        "camera": camera_raw,
        "intrinsics": intrinsics,
    }
    x_output = {
        "human": callback_human_feat,
        "camera_source": camera_feat,
    }
    decode_info = {
        "stage2_latent_order": "concat([z_hum,z_cam]) [B,192,T]",
        "tokenizer_native_order": "concat([z_cam,z_hum]) [B,T,192]",
        "source_human_feature_dim": int(human_feat.shape[-1]),
        "callback_human_feature_dim": int(callback_human_feat.shape[-1]),
        "human_feature_dim": int(callback_human_feat.shape[-1]),
        "camera_feature_dim": int(camera_feat.shape[-1]),
        "camera_raw_policy": camera_policy,
        "feature_contract": feature_contract,
        "intrinsics_policy": "gt_passthrough_from_official_batch; source tokenizer does not generate fov/intrinsics",
    }
    return x_output, raw_output, decode_info


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="StoryMotion source-tokenizer-aware full eval with PulpMotion official metric callbacks.")
    p.add_argument("--story-root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--run-dir", type=Path, required=True)
    p.add_argument("--cache-dir", type=Path, required=True)
    p.add_argument("--cache-file", default="val.pt")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--records", type=Path)
    p.add_argument("--task", choices=["camera", "human", "joint"], required=True)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--split", default="test")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    p.add_argument("--pulp-root", type=Path)
    p.add_argument("--data-root", type=Path)
    p.add_argument("--samples", type=int, default=0)
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--workers", type=int, default=0)
    p.add_argument("--seed", type=int, default=20260613)
    p.add_argument("--num-steps", type=int, default=50)
    p.add_argument("--cfg-scale", type=float, default=1.0)
    p.add_argument("--cfg-human", type=float, default=None)
    p.add_argument("--cfg-camera", type=float, default=None)
    p.add_argument("--eta", type=float, default=0.0)
    p.add_argument("--channel-gated-cfg", action="store_true")
    p.add_argument("--text-intervention", choices=["none", "zero_all", "zero_camera", "zero_human", "shuffle_all", "shuffle_camera", "shuffle_human"], default="none")
    p.add_argument("--observed-latent-intervention", choices=["none", "zero", "shuffle", "noise_matched"], default="none")
    p.add_argument("--camera-latent-intervention", choices=["none", "zero", "shuffle", "noise_matched"], default="none")
    p.add_argument("--tokenizer-checkpoint", type=Path)
    p.add_argument("--tokenizer-preset")
    p.add_argument("--human200-stats", type=Path)
    p.add_argument("--no-z-depth-mode", choices=["error", "gt", "zero"], default="error")
    p.add_argument("--znorm", action="store_true")
    p.add_argument("--znorm-stats-path", type=Path)
    p.add_argument("--progress-every", type=int, default=10)
    return p


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    device = torch.device(args.device)
    story_root = args.story_root.resolve()
    pulp_root = (args.pulp_root or story_root / "linked/PulpMotion").resolve()
    feature_stats = _load_official_stats(pulp_root)

    train_mod = load_module("train_stage2_condmdi_pulp", story_root / "scripts/train_stage2_condmdi_pulp.py")
    cache_mod = load_module("build_stage2_pulp_latent_cache", story_root / "scripts/build_stage2_pulp_latent_cache.py")
    model, diffusion, run_info = load_stage2(args.run_dir, train_mod, device)
    run_meta = load_run_meta(args.run_dir)
    run_args = run_meta.get("args", {}) if isinstance(run_meta, dict) else {}
    cfg, dataset, _autoencoder = build_pulp(cache_mod, story_root, args, device)
    cache_path = args.cache_dir / args.cache_file
    znorm_stats, znorm_record = resolve_eval_znorm_stats(args, run_meta, train_mod)
    cache = train_mod.PulpLatentCache(cache_path, znorm_stats=znorm_stats)
    cache_meta = load_cache_meta(cache_path)
    tokenizer = load_tokenizer_from_cache_meta(cache_meta, args, device)
    loader, end = collate_cache(cache, args.start, args.samples, args.batch_size, args.workers)

    task_name = args.task
    if args.camera_latent_intervention != "none" and args.observed_latent_intervention != "none":
        raise ValueError("use only one of --camera-latent-intervention or --observed-latent-intervention")
    latent_intervention = args.observed_latent_intervention
    latent_intervention_arg = "observed_latent_intervention"
    if args.camera_latent_intervention != "none":
        if task_name != "human":
            raise ValueError("--camera-latent-intervention is valid only for task=human")
        latent_intervention = args.camera_latent_intervention
        latent_intervention_arg = "camera_latent_intervention"
    if task_name == "joint" and latent_intervention != "none":
        raise ValueError("observed latent intervention is not defined for task=joint")
    if bool(cache_meta.get("drop_camera_z", False)) and task_name in {"camera", "joint"} and args.no_z_depth_mode == "error":
        raise ValueError("no-z camera/joint eval is not fair without a z-depth policy; use human task or pass a diagnostic mode")

    observed_latent_branch = {"camera": "human", "human": "camera", "joint": "none"}[task_name]
    task_id = {name: task for task, name in train_mod.TASK_NAMES.items()}[task_name]
    callback, module = instantiate_official_metrics(cfg, pulp_root, task_name, device)
    records_path = args.records or args.output.with_suffix(".records.jsonl")
    records_path.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if records_path.exists():
        records_path.unlink()

    sampler = {
        "name": "ddim_start_x",
        "num_steps": args.num_steps,
        "time_grid": "round(linspace(T-1,0,num_steps)) unique_consecutive, includes 0",
        "prediction_type": "START_X",
        "observed_branch_policy": "inject q(z_gt,t,per_sample_noise) at every step; final merge gt observed branch",
        "padding_policy": "inject q(z_gt,t,per_sample_noise) at every step; final merge gt padded frames",
        "eta": args.eta,
        "cfg_scale": args.cfg_scale,
        "cfg_human": args.cfg_human,
        "cfg_camera": args.cfg_camera,
        "cfg_channel_gated": bool(args.channel_gated_cfg),
        "cfg_mode": ("bilateral_textspace_3pass_channel_gated" if args.channel_gated_cfg else "bilateral_textspace_3pass") if (args.cfg_human is not None and args.cfg_camera is not None) else ("standard_single_cfg" if args.cfg_scale != 1.0 else "conditional_only"),
        "observed_latent_intervention": latent_intervention,
        "observed_latent_branch": observed_latent_branch,
    }

    start_time = time.time()
    processed = 0
    first_batch_summary: dict[str, Any] | None = None
    first_decode_info: dict[str, Any] | None = None
    human_motion_records: list[dict[str, Any]] = []
    with records_path.open("a", encoding="utf-8") as records_handle, torch.no_grad():
        for batch_index, batch in enumerate(loader):
            z = batch["z"].to(device)
            text = batch["text"].to(device)
            valid = batch["valid"].to(device)
            sample_ids = [str(value) for value in batch["sample_id"]]
            sample_indices = list(range(args.start + processed, args.start + processed + len(sample_ids)))
            batch_generator = torch.Generator(device=device)
            batch_generator.manual_seed(args.seed + args.start + processed * 1009 + batch_index * 9176)
            text_for_sampling = apply_text_intervention(text, args.text_intervention, generator=batch_generator)
            z_for_sampling = apply_observed_latent_intervention(
                z,
                task_name,
                latent_intervention,
                train_mod,
                generator=batch_generator,
            )
            pulp_batch = batch_from_sample_ids(dataset, sample_ids, device)
            intrinsics = pulp_batch["x_raw"]["intrinsics"]
            x_input, raw_input = reference_feature_and_raw(dataset, pulp_batch, intrinsics)
            completion = sample_start_x(
                model,
                diffusion,
                train_mod,
                z_for_sampling,
                text_for_sampling,
                valid,
                task_id,
                sample_indices,
                args.seed + {"camera": 11, "human": 23, "joint": 37}[task_name],
                args.num_steps,
                cfg_scale=args.cfg_scale,
                cfg_human=args.cfg_human,
                cfg_camera=args.cfg_camera,
                eta=args.eta,
                channel_gated_cfg=args.channel_gated_cfg,
            )
            completion_decode = train_mod.denormalize_latent(completion, valid, znorm_stats)
            x_output, raw_output, decode_info = decode_source_feature_and_raw(
                tokenizer,
                dataset,
                train_mod,
                completion_decode,
                raw_input,
                raw_input["intrinsics"],
                pulp_batch["padding_mask"],
                task_name,
                args.no_z_depth_mode,
                str(cache_meta.get("feature_contract", LEGACY_FEATURE_CONTRACT)),
                feature_stats,
            )
            outputs = {"raw_input": raw_input, "raw_output": raw_output, "x_output": x_output}
            human_motion_records.extend(human_motion_stats_for_batch(raw_output, raw_input, pulp_batch["padding_mask"], sample_ids))
            official_outputs = official_outputs_for_task(outputs, task_name)
            callback.on_test_batch_end(None, module, official_outputs, pulp_batch, batch_index)
            write_records(
                records_handle,
                task_name=task_name,
                sample_ids=sample_ids,
                sample_indices=sample_indices,
                seed=args.seed,
                run_info=run_info,
                sampler=sampler,
            )
            processed += len(sample_ids)
            if first_batch_summary is None:
                first_decode_info = decode_info
                first_batch_summary = {
                    "sample_ids": sample_ids,
                    "cache_z_shape": list(z.shape),
                    "completion_shape": list(completion.shape),
                    "completion_decode_shape": list(completion_decode.shape),
                    "x_input": jsonable(x_input),
                    "outputs": jsonable(outputs),
                    "decode_info": decode_info,
                }
            if args.progress_every > 0 and ((batch_index + 1) % args.progress_every == 0 or processed == end - args.start):
                elapsed = time.time() - start_time
                rate = processed / max(elapsed, 1e-9)
                remaining = max(0, (end - args.start) - processed)
                print(json.dumps({"task": task_name, "processed": processed, "target": end - args.start, "elapsed_sec": elapsed, "eta_sec": remaining / max(rate, 1e-9)}, sort_keys=True), flush=True)

    callback.on_test_epoch_end(None, module)
    metrics = metric_values(module.eval_metrics)
    payload = {
        "mode": "storymotion_source_tokenizer_generated_eval_with_pulpmotion_official_callbacks",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "task": task_name,
        "scope_note": "Stage2 completion latent is decoded with the matching frozen Stage1 source tokenizer, then raw outputs are passed to PulpMotion official metric callbacks.",
        "fairness_notes": [
            "with-z camera uses source 9D translation+rot6d -> c2w conversion",
            "source tokenizer does not generate fov/intrinsics; official callbacks receive GT intrinsics passthrough",
            "no-z camera/joint eval is refused unless a diagnostic z-depth policy is explicitly selected",
        ],
        "run": run_info,
        "stage2_task_probs_camera_human_joint": run_args.get("task_probs"),
        "latent_znorm": znorm_record,
        "cache_dir": str(args.cache_dir),
        "cache_file": args.cache_file,
        "sample_range": [args.start, end],
        "evaluated_samples": processed,
        "split": args.split,
        "set_name": args.set_name,
        "config_name": args.config_name,
        "pulp_root": str(pulp_root),
        "data_root": str(args.data_root or story_root / "linked/pulpmotion-data"),
        "model_dir": str(args.model_dir),
        "metric_checkpoint_status": metric_checkpoint_status(args.model_dir),
        "sampler": sampler,
        "decode_contract": first_decode_info,
        "interventions": {
            "text_intervention": args.text_intervention,
            "observed_latent_intervention": latent_intervention,
            "observed_latent_intervention_arg": latent_intervention_arg,
            "camera_latent_intervention": args.camera_latent_intervention,
            "text_layout": "first 512 dims camera text, last 512 dims human text",
        },
        "human_motion_stats": summarize_human_motion_stats(human_motion_records, task_name),
        "diffusion_schedule": {
            "num_train_timesteps": diffusion.num_timesteps,
            "sqrt_alphas_cumprod_sha256": sha256_tensor(diffusion.sqrt_alphas_cumprod),
            "sqrt_one_minus_alphas_cumprod_sha256": sha256_tensor(diffusion.sqrt_one_minus_alphas_cumprod),
        },
        "training_conditioning_contract": {
            "forward_policy": "TemporalObsUNet.forward replaces observed x_t positions with clean obs_x0 before concatenating obs_mask.",
            "code_expression": "x = torch.where(obs_mask.bool(), obs_x0, x_t)",
        },
        "seed": args.seed,
        "batch_size": args.batch_size,
        "device": str(device),
        "cache_meta": cache_meta,
        "script_hashes": {
            "storymotion_source_tokenizer_full_eval.py": sha256_file(Path(__file__).resolve()),
            "storymotion_official_full_eval.py": sha256_file(story_root / "scripts/storymotion_official_full_eval.py"),
            "storymotion_official_bridge_smoke.py": sha256_file(story_root / "scripts/storymotion_official_bridge_smoke.py"),
            "train_stage2_condmdi_pulp.py": sha256_file(story_root / "scripts/train_stage2_condmdi_pulp.py"),
            "build_stage2_joint_tokenizer_latent_cache.py": sha256_file(story_root / "scripts/build_stage2_joint_tokenizer_latent_cache.py"),
        },
        "torch": {
            "version": torch.__version__,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        },
        "metric_keys": sorted(metrics),
        "metrics": metrics,
        "records_path": str(records_path),
        "first_batch_summary": first_batch_summary,
        "elapsed_sec": time.time() - start_time,
    }
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "records": str(records_path), "task": task_name, "samples": processed, "keys": len(metrics), "elapsed_sec": payload["elapsed_sec"]}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
