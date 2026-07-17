#!/usr/bin/env python3
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

from scripts.render_stage1_joint_separate_3d_reconstructions import (  # noqa: E402
    ModelSpec,
    build_model,
    feature_contract as checkpoint_feature_contract,
    load_camera_features,
    load_checkpoint_run_config,
    parse_model_spec,
    read_jsonl,
)
from storymotion_official_bridge_smoke import (  # noqa: E402
    DummyModule,
    add_pulp_import_paths,
    jsonable,
    metric_checkpoint_status,
    metric_values,
    official_outputs_for_task,
    patch_numpy_aliases,
)
from storymotion.training.camera_data import camera_features_to_poses  # noqa: E402
from storymotion.training.joint_data import (  # noqa: E402
    LEGACY_FEATURE_CONTRACT,
    OFFICIAL_FEATURE_CONTRACT,
    _load_official_stats,
)
from storymotion.training.human200 import (  # noqa: E402
    HUMAN200_FEATURE_CONTRACT,
    human200_to_official_human199,
    official_human199_to_human200,
)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate StoryMotion Stage1 joint/separate tokenizer reconstruction with PulpMotion official metric callbacks."
    )
    parser.add_argument("--story-root", type=Path, default=ROOT)
    parser.add_argument("--pulp-root", type=Path, default=ROOT / "linked/PulpMotion")
    parser.add_argument("--data-root", type=Path, default=ROOT / "linked/pulpmotion-data")
    parser.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    parser.add_argument("--config-name", default="config_dit_xy")
    parser.add_argument("--set-name", default="pure_", choices=["pure_", "mixed_"])
    parser.add_argument("--split", default="test")
    parser.add_argument("--human-manifest", type=Path, default=Path("runs/train/pulpmotion_native_test_manifest_full_20260608.jsonl"))
    parser.add_argument("--camera-manifest", type=Path, default=Path("runs/train/pulpmotion_camera_test_manifest_full_20260610.jsonl"))
    parser.add_argument("--model", required=True, help="Model spec: name:preset:checkpoint[:dropz].")
    parser.add_argument(
        "--feature-contract",
        choices=["auto", LEGACY_FEATURE_CONTRACT, OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT],
        default="auto",
    )
    parser.add_argument("--human200-stats", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--records", type=Path)
    parser.add_argument("--tasks", nargs="+", choices=["human", "camera", "joint"], default=["human", "camera", "joint"])
    parser.add_argument("--no-z-depth-mode", choices=["error", "gt", "zero"], default="error")
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--progress-every", type=int, default=10)
    return parser


def build_config(args: argparse.Namespace) -> Any:
    from hydra import compose, initialize_config_dir
    from omegaconf import OmegaConf

    try:
        OmegaConf.register_new_resolver("eval", eval)
    except ValueError:
        pass

    overrides = [
        f"checkpoint_dir={args.model_dir}",
        f"dataset.dataset_dir={args.data_root}",
        f"dataset.joint.set_name={args.set_name}",
        "log_wandb=false",
        f"compnode.batch_size={args.batch_size}",
        f"compnode.num_workers={args.workers}",
        "compnode.num_gpus=1",
    ]
    with initialize_config_dir(version_base="1.3", config_dir=str((args.pulp_root / "configs").resolve())):
        return compose(config_name=args.config_name, overrides=overrides)


def move_to_device(value: Any, device: torch.device) -> Any:
    if torch.is_tensor(value):
        return value.to(device)
    if isinstance(value, dict):
        return {key: move_to_device(item, device) for key, item in value.items()}
    if isinstance(value, list):
        return [move_to_device(item, device) for item in value]
    return value


def instantiate_metrics(cfg: Any, task_name: str, device: torch.device):
    from hydra.utils import instantiate

    if task_name == "camera":
        metrics = instantiate(cfg.metrics.camera)
    elif task_name == "human":
        metrics = instantiate(cfg.metrics.human)
    elif task_name == "joint":
        metrics = instantiate(cfg.metrics)
    else:
        raise ValueError(f"bad task: {task_name}")
    module = DummyModule(device)
    metrics.on_test_start(None, module)
    return metrics, module


def offload_manifold_metric_states(callback: Any) -> None:
    callbacks = [
        callback,
        getattr(callback, "camera_callback", None),
        getattr(callback, "human_callback", None),
    ]
    for cb in callbacks:
        if cb is None:
            continue
        for attr in ("tmr_prdc", "clatr_prdc", "projection_prdc"):
            metrics = getattr(cb, attr, None)
            if not isinstance(metrics, dict):
                continue
            for metric in metrics.values():
                for state_name in ("real_features", "fake_features"):
                    state = getattr(metric, state_name, None)
                    if isinstance(state, list):
                        setattr(
                            metric,
                            state_name,
                            [tensor.detach().cpu() if torch.is_tensor(tensor) else tensor for tensor in state],
                        )


def resolve(path: str | Path, root: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else root / value


def load_rows_by_id(path: Path) -> dict[str, dict[str, Any]]:
    rows = {}
    for row in read_jsonl(path):
        rows[str(row["sample_id"])] = row
    return rows


def source_camera_to_raw(
    camera_feat: torch.Tensor,
    raw_input: dict[str, Any],
    padding_mask: torch.Tensor,
    no_z_depth_mode: str,
    task_name: str,
) -> tuple[torch.Tensor, str]:
    dim = int(camera_feat.shape[-1])
    policy = "tokenizer_camera_9d_translation_rot6d_to_c2w"
    if dim == 9:
        full = camera_feat
    elif dim == 8:
        if task_name == "human" and no_z_depth_mode == "error":
            return raw_input["camera"], "not_evaluated_gt_camera_passthrough_for_human_task"
        if no_z_depth_mode == "error":
            raise ValueError("8D no-z camera reconstruction needs --no-z-depth-mode gt or zero for camera/joint official eval")
        xy = camera_feat[..., :2]
        rot6d = camera_feat[..., 2:8]
        if no_z_depth_mode == "gt":
            z = raw_input["camera"][..., 2, 3:4].to(device=camera_feat.device, dtype=camera_feat.dtype)
            policy = "tokenizer_noz_xy_rot6d_with_gt_z_passthrough_diagnostic"
        elif no_z_depth_mode == "zero":
            z = torch.zeros_like(xy[..., :1])
            policy = "tokenizer_noz_xy_rot6d_with_zero_z_diagnostic"
        else:
            raise ValueError(f"unknown no_z_depth_mode: {no_z_depth_mode}")
        full = torch.cat([xy, z, rot6d], dim=-1)
    else:
        raise ValueError(f"expected camera feature dim 8 or 9, got {dim}")

    full = full.detach().float().cpu()
    masks = padding_mask.detach().bool().cpu().numpy()
    poses = []
    for index in range(full.shape[0]):
        pose = camera_features_to_poses(full[index].numpy())
        if not bool(masks[index].all()):
            gt_pose = raw_input["camera"][index].detach().float().cpu().numpy()
            pose[~masks[index]] = gt_pose[~masks[index]]
        poses.append(pose)
    raw = torch.from_numpy(np.stack(poses, axis=0)).to(device=camera_feat.device, dtype=camera_feat.dtype)
    return raw, policy


def reconstruct_one(
    model: torch.nn.Module,
    spec: ModelSpec,
    human_row: dict[str, Any],
    camera_row: dict[str, Any],
    camera_manifest: Path,
    frames: int,
    device: torch.device,
    feature_contract: str,
    official_human: torch.Tensor | None = None,
    official_camera: torch.Tensor | None = None,
    official_stats: dict[str, torch.Tensor] | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    if feature_contract in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}:
        if official_human is None or official_camera is None:
            raise ValueError("official feature tensors are required for the official contract")
        camera = official_camera
        if feature_contract == HUMAN200_FEATURE_CONTRACT:
            if official_stats is None or not hasattr(model, "human200_stats"):
                raise ValueError("v8.2 reconstruction requires matched official and human200 statistics")
            human = official_human199_to_human200(
                official_human,
                official_stats["human_mean"],
                official_stats["human_std"],
                model.human200_stats,
            )
        else:
            human = official_human
    else:
        human_path = resolve(human_row["motion_feature_path"], Path("."))
        human = torch.from_numpy(np.load(human_path).astype(np.float32))
        camera = load_camera_features(camera_row, camera_manifest, spec.drop_camera_z)
    available = min(int(human.shape[0]), int(camera.shape[0]))
    if available != frames:
        raise ValueError(f"{human_row['sample_id']} length mismatch: official={frames}, paired={available}")
    with torch.no_grad():
        output = model(human[:frames].unsqueeze(0).to(device), camera[:frames].unsqueeze(0).to(device))
    human_recon = output.human_recon[0, :frames].float()
    if feature_contract == HUMAN200_FEATURE_CONTRACT:
        human_recon = human200_to_official_human199(
            human_recon,
            model.human200_stats,
            official_stats["human_mean"],
            official_stats["human_std"],
        )
    return human_recon, output.camera_recon[0, :frames].float()


def reconstruct_batch(
    model: torch.nn.Module,
    spec: ModelSpec,
    sample_ids: list[str],
    padding_mask: torch.Tensor,
    human_rows: dict[str, dict[str, Any]],
    camera_rows: dict[str, dict[str, Any]],
    camera_manifest: Path,
    device: torch.device,
    feature_contract: str,
    official_input: dict[str, torch.Tensor],
    official_stats: dict[str, torch.Tensor] | None = None,
) -> tuple[torch.Tensor, torch.Tensor, list[dict[str, Any]]]:
    batch_size, target_len = padding_mask.shape
    output_human_dim = (
        int(official_input["human"].shape[-1])
        if feature_contract == HUMAN200_FEATURE_CONTRACT
        else int(model.human_dim)
    )
    human_out = torch.zeros((batch_size, target_len, output_human_dim), device=device, dtype=torch.float32)
    camera_out = torch.zeros((batch_size, target_len, int(model.camera_dim)), device=device, dtype=torch.float32)
    records = []
    for index, sample_id in enumerate(sample_ids):
        if sample_id not in human_rows or sample_id not in camera_rows:
            raise KeyError(f"sample {sample_id} is missing from paired manifests")
        frames = int(padding_mask[index].sum().item())
        human_recon, camera_recon = reconstruct_one(
            model,
            spec,
            human_rows[sample_id],
            camera_rows[sample_id],
            camera_manifest,
            frames,
            device,
            feature_contract,
            official_input["human"][index, :frames].cpu()
            if feature_contract in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}
            else None,
            official_input["camera"][index, :frames].cpu()
            if feature_contract in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}
            else None,
            official_stats,
        )
        human_out[index, :frames] = human_recon
        camera_out[index, :frames] = camera_recon
        records.append({"sample_id": sample_id, "frames": frames})
    return human_out, camera_out, records


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    add_pulp_import_paths(args.pulp_root)
    torch.set_float32_matmul_precision("medium")
    device = torch.device(args.device)

    from hydra.utils import instantiate

    cfg = build_config(args)
    dataset = instantiate(cfg.dataset).set_split(args.split, mode="test")
    full_len = len(dataset)
    if args.samples > 0:
        sample_ids = [str(value) for value in dataset.sample_ids[: args.samples]]
        dataset.sample_ids = sample_ids
        for attr in ("joint_dataset", "camera_dataset", "human_dataset", "caption_dataset"):
            sub = getattr(dataset, attr, None)
            if sub is not None and hasattr(sub, "sample_ids"):
                sub.sample_ids = sample_ids

    spec = parse_model_spec(args.model)
    model = build_model(spec, str(device), args.human200_stats)
    for param in model.parameters():
        param.requires_grad_(False)
    run_config = load_checkpoint_run_config(spec.checkpoint)
    model_contract = checkpoint_feature_contract(spec)
    feature_contract = args.feature_contract
    if feature_contract == "auto":
        feature_contract = model_contract
    if feature_contract != model_contract:
        raise ValueError("requested feature contract does not match the checkpoint run_config")
    official_stats = _load_official_stats(args.pulp_root)

    human_rows = load_rows_by_id(args.human_manifest)
    camera_rows = load_rows_by_id(args.camera_manifest)
    official_ids = {str(value) for value in dataset.sample_ids}
    paired_ids = set(human_rows) & set(camera_rows)
    missing_from_manifest = sorted(official_ids - paired_ids)
    if missing_from_manifest:
        raise ValueError(f"official split has ids missing from paired manifests: {missing_from_manifest[:5]}")

    callbacks = {}
    modules = {}
    for task_name in args.tasks:
        callbacks[task_name], modules[task_name] = instantiate_metrics(cfg, task_name, device)

    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.workers, pin_memory=device.type == "cuda")
    records_path = args.records or args.output.with_suffix(".records.jsonl")
    records_path.parent.mkdir(parents=True, exist_ok=True)
    if records_path.exists():
        records_path.unlink()

    processed = 0
    first_batch_summary: dict[str, Any] | None = None
    camera_policy = None
    t0 = time.time()
    feature_dataset = getattr(dataset, "joint_dataset", None) or dataset
    with records_path.open("a", encoding="utf-8") as records_handle, torch.no_grad():
        for batch_idx, batch in enumerate(loader):
            batch_device = {key: move_to_device(value, device) for key, value in batch.items() if key != "x_raw"}
            batch_device["x_raw"] = move_to_device(batch["x_raw"], device)
            padding_mask = batch_device["padding_mask"].to(dtype=torch.bool)
            intrinsics = batch_device["x_raw"]["intrinsics"].to(device)
            x_input = dataset.get_feat(batch_device["x_raw"], padding_mask)
            raw_input = dataset.get_raw(x_input, intrinsics)
            sample_ids = [str(value) for value in batch["sample_id"]]

            human_feat, camera_feat, records = reconstruct_batch(
                model,
                spec,
                sample_ids,
                padding_mask,
                human_rows,
                camera_rows,
                args.camera_manifest,
                device,
                feature_contract,
                x_input,
                official_stats,
            )
            human_feat = human_feat.masked_fill(~padding_mask[..., None], 0.0)
            camera_feat = camera_feat.masked_fill(~padding_mask[..., None], 0.0)
            if feature_contract in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}:
                decoded = feature_dataset.get_raw({"human": human_feat, "camera": camera_feat}, intrinsics)
                human_raw = decoded["human"]
                camera_raw = decoded["camera"]
                output_intrinsics = decoded["intrinsics"]
                camera_policy = "pulpmotion_official_camera14_joint_decoder"
            else:
                # Legacy checkpoints reconstruct raw RIFKE, while PulpMotion get_raw expects normalized RIFKE.
                human_raw = feature_dataset.human_dataset.get_raw(feature_dataset.human_dataset.normalize(human_feat))
                camera_raw, camera_policy = source_camera_to_raw(camera_feat, raw_input, padding_mask, args.no_z_depth_mode, "joint")
                output_intrinsics = intrinsics
            outputs = {
                "raw_input": raw_input,
                "raw_output": {"human": human_raw, "camera": camera_raw, "intrinsics": output_intrinsics},
                "x_output": {"human": human_feat, "camera_source": camera_feat},
            }
            for task_name, callback in callbacks.items():
                callback.on_test_batch_end(None, modules[task_name], official_outputs_for_task(outputs, task_name), batch_device, batch_idx)
                offload_manifold_metric_states(callback)
            if device.type == "cuda":
                torch.cuda.empty_cache()
            for record in records:
                record["model"] = spec.name
                record["set_name"] = args.set_name
                records_handle.write(json.dumps(record, sort_keys=True) + "\n")
            processed += len(sample_ids)
            if first_batch_summary is None:
                first_batch_summary = {
                    "sample_ids": sample_ids,
                    "padding_mask": jsonable(padding_mask),
                    "human_feat": jsonable(human_feat),
                    "camera_feat": jsonable(camera_feat),
                    "raw_output": jsonable(outputs["raw_output"]),
                }
            if args.progress_every > 0 and ((batch_idx + 1) % args.progress_every == 0 or processed == len(dataset)):
                elapsed = time.time() - t0
                rate = processed / max(elapsed, 1e-9)
                print(
                    json.dumps(
                        {
                            "model": spec.name,
                            "processed": processed,
                            "target": len(dataset),
                            "elapsed_sec": elapsed,
                            "eta_sec": (len(dataset) - processed) / max(rate, 1e-9),
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )

    metric_results: dict[str, Any] = {}
    for task_name, callback in callbacks.items():
        callback.on_test_epoch_end(None, modules[task_name])
        metrics = metric_values(modules[task_name].eval_metrics)
        metric_results[task_name] = {"metric_keys": sorted(metrics), "metrics": metrics}

    payload = {
        "mode": "storymotion_stage1_tokenizer_reconstruction_official_metrics",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "set_name": args.set_name,
        "split": args.split,
        "full_split_samples": full_len,
        "evaluated_samples": processed,
        "model": {"name": spec.name, "preset": spec.preset, "checkpoint": str(spec.checkpoint), "drop_camera_z": spec.drop_camera_z},
        "tasks": args.tasks,
        "batch_size": args.batch_size,
        "reconstruction_policy": "Each sample is reconstructed at its real valid length, then padded back to the official metric batch. This avoids non-causal convolution seeing future padding zeros.",
        "camera_raw_policy": camera_policy,
        "feature_contract": feature_contract,
        "human200_normalization": (
            {
                "path": str(model.human200_stats["path"]),
                "sha256": model.human200_stats["sha256"],
                "source_manifest_sha256": model.human200_stats["meta"]["source"]["manifest_sha256"],
                "source_split": model.human200_stats["meta"]["source"]["split"],
            }
            if feature_contract == HUMAN200_FEATURE_CONTRACT
            else None
        ),
        "metric_checkpoint_status": metric_checkpoint_status(args.model_dir),
        "metric_memory_policy": "PulpMotion PRDC feature-list states are offloaded to CPU after each callback update to avoid GPU OOM; callback inputs and metric formulas are unchanged.",
        "script_hashes": {
            "eval_stage1_joint_tokenizer_official_recon.py": sha256_file(Path(__file__).resolve()),
        },
        "metric_results": metric_results,
        "records_path": str(records_path),
        "first_batch_summary": first_batch_summary,
        "elapsed_sec": time.time() - t0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(jsonable(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "records": str(records_path), "samples": processed}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
