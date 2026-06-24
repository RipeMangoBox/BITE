#!/usr/bin/env python3
"""Render PulpMotion fair comparisons for StoryMotion bilateral renders."""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path("/data/public/ripemangobox/Motion/StoryMotion")
SCRIPT_DIR = ROOT / "scripts"
PULP_ROOT = ROOT / "linked/PulpMotion"


def load_local_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


rbr = load_local_module("render_bilateral_results", SCRIPT_DIR / "render_bilateral_results.py")


def patch_numpy_aliases() -> None:
    for name, value in {
        "bool": bool,
        "int": int,
        "float": float,
        "complex": complex,
        "object": object,
        "str": str,
        "unicode": str,
    }.items():
        if not hasattr(np, name):
            setattr(np, name, value)


def add_pulp_paths(pulp_root: Path) -> None:
    for path in [pulp_root.resolve(), (pulp_root / "src").resolve()]:
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))


def collate_values(values: list[Any], device: torch.device) -> Any:
    first = values[0]
    if torch.is_tensor(first):
        return torch.stack(values).to(device)
    if isinstance(first, np.ndarray):
        return torch.as_tensor(np.stack(values)).to(device)
    if isinstance(first, dict):
        keys = set().union(*(set(value.keys()) for value in values))
        return {key: collate_values([value[key] for value in values], device) for key in sorted(keys)}
    return values


def batch_from_sample_ids(dataset: Any, sample_ids: list[str], device: torch.device) -> dict[str, Any]:
    samples = [dataset.get_sample(sample_id) for sample_id in sample_ids]
    keys = set().union(*(set(sample.keys()) for sample in samples))
    batch: dict[str, Any] = {"sample_id": sample_ids}
    for key in sorted(keys):
        batch[key] = collate_values([sample[key] for sample in samples], device)
    return batch


def build_pulpmotion_model(args: argparse.Namespace, device: torch.device, cfg_rate_z: float):
    from hydra import compose, initialize_config_dir
    from hydra.utils import instantiate
    from omegaconf import OmegaConf

    try:
        OmegaConf.register_new_resolver("eval", eval)
    except ValueError:
        pass

    overrides = [
        f"checkpoint_dir={args.model_dir}",
        f"checkpoint_path={args.pulp_checkpoint}",
        f"dataset.dataset_dir={args.data_root}",
        f"dataset.joint.set_name={args.set_name}",
        "log_wandb=false",
        "compnode.batch_size=2",
        "compnode.num_workers=0",
        "compnode.num_gpus=1",
        f"model.sampler.generation_sampler.cfg_rate_c={args.pulp_cfg_c}",
        f"model.sampler.generation_sampler.cfg_rate_z={cfg_rate_z}",
        f"model.sampler.generation_sampler.num_steps={args.pulp_num_steps}",
    ]
    with initialize_config_dir(version_base="1.3", config_dir=str((args.pulp_root / "configs").resolve())):
        cfg = compose(config_name=args.config_name, overrides=overrides)

    model = instantiate(cfg.model)
    ckpt = torch.load(args.pulp_checkpoint, map_location="cpu", weights_only=False)
    model.load_state_dict(ckpt["state_dict"], strict=False)
    model.to(device)
    model.eval()
    return model, ckpt


def run_pulpmotion(model: torch.nn.Module, dataset: Any, sample_ids: list[str], device: torch.device, seed: int):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    batch = batch_from_sample_ids(dataset, sample_ids, device)
    model.raw_to_feat = dataset.get_feat
    model.feat_to_raw = dataset.get_raw
    with torch.no_grad():
        outputs = model.test_step(batch, 0)
    return outputs, batch


def np_joints(raw_human: Any, index: int, frames: int) -> np.ndarray:
    joints = raw_human.joints if hasattr(raw_human, "joints") else raw_human["joints"]
    return joints[index, :frames, :22, :3].detach().cpu().numpy()


def np_camera(raw_camera: torch.Tensor, index: int, frames: int) -> np.ndarray:
    return raw_camera[index, :frames, :3, 3].detach().cpu().numpy()


def plot_compare_png(
    out_path: Path,
    sample_id: str,
    gt_cam: np.ndarray,
    gt_joints: np.ndarray,
    series: dict[str, dict[str, np.ndarray]],
) -> None:
    n = gt_joints.shape[0]
    frame_ids = sorted({0, n // 2, n - 1})
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.2))

    axes[0].plot(gt_cam[:, 0], gt_cam[:, 2], color="black", linewidth=2, label="GT")
    axes[1].plot(gt_joints[:, 0, 0], gt_joints[:, 0, 2], color="black", linewidth=2, label="GT")
    for name, values in series.items():
        cam = values["camera"]
        joints = values["joints"]
        axes[0].plot(cam[:, 0], cam[:, 2], linewidth=1.3, label=name)
        axes[1].plot(joints[:, 0, 0], joints[:, 0, 2], linewidth=1.3, label=name)
        for frame in frame_ids:
            axes[2].scatter(joints[frame, :, 0], joints[frame, :, 2], s=8, alpha=0.6, label=name if frame == 0 else None)
    for frame in frame_ids:
        axes[2].scatter(gt_joints[frame, :, 0], gt_joints[frame, :, 2], s=9, color="black", alpha=0.45, label="GT" if frame == 0 else None)

    axes[0].set_title("camera trajectory XZ")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("z")
    axes[1].set_title("human root trajectory XZ")
    axes[1].set_xlabel("x")
    axes[2].set_title("human joints XZ frames")
    axes[2].set_xlabel("x")
    axes[2].set_ylabel("z")
    rbr._set_equal_aspect(axes[0], [gt_cam] + [values["camera"] for values in series.values()])
    rbr._set_equal_aspect(axes[1], [gt_joints[:, 0, :]] + [values["joints"][:, 0, :] for values in series.values()])
    rbr._set_equal_aspect(axes[2], [gt_joints.reshape(-1, 3)] + [values["joints"].reshape(-1, 3) for values in series.values()])
    axes[0].legend(fontsize=7)
    axes[1].legend(fontsize=7)
    axes[2].legend(fontsize=7)
    fig.suptitle(sample_id)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def motion_stats(joints: np.ndarray, gt_joints: np.ndarray) -> dict[str, float]:
    n = min(joints.shape[0], gt_joints.shape[0])
    joints = joints[:n]
    gt_joints = gt_joints[:n]
    root = joints[:, 0]
    gt_root = gt_joints[:, 0]
    rel = joints - root[:, None, :]
    gt_rel = gt_joints - gt_root[:, None, :]
    velocity = np.diff(joints, axis=0)
    accel = np.diff(velocity, axis=0)
    root_velocity = np.diff(root, axis=0)
    root_accel = np.diff(root_velocity, axis=0)
    foot_indices = [10, 11]
    foot_vel = np.linalg.norm(np.diff(joints[:, foot_indices, :], axis=0), axis=-1) if n > 1 else np.zeros((0, len(foot_indices)))
    foot_height = joints[:-1, foot_indices, 2] if n > 1 else np.zeros((0, len(foot_indices)))
    gt_foot_height = gt_joints[:-1, foot_indices, 2] if n > 1 else np.zeros((0, len(foot_indices)))
    gt_floor = float(np.nanpercentile(gt_joints[:, foot_indices, 2], 5)) if n > 0 else 0.0
    contact = foot_height <= gt_floor + 0.05
    gt_contact = gt_foot_height <= gt_floor + 0.05
    bone_cvs = []
    bone_errs = []
    for parent, child in rbr.BONE_CONNECTIONS:
        length = np.linalg.norm(joints[:, child] - joints[:, parent], axis=-1)
        gt_length = np.linalg.norm(gt_joints[:, child] - gt_joints[:, parent], axis=-1)
        mean_len = max(float(length.mean()), 1e-6)
        gt_mean_len = max(float(gt_length.mean()), 1e-6)
        bone_cvs.append(float(length.std() / mean_len))
        bone_errs.append(float(abs(mean_len - gt_mean_len) / gt_mean_len))
    return {
        "mpjpe_root_aligned": float(np.linalg.norm(rel - gt_rel, axis=-1).mean()),
        "joint_velocity_mean": float(np.linalg.norm(velocity, axis=-1).mean()) if velocity.size else 0.0,
        "joint_accel_mean": float(np.linalg.norm(accel, axis=-1).mean()) if accel.size else 0.0,
        "root_path_len": float(np.linalg.norm(root_velocity, axis=-1).sum()) if root_velocity.size else 0.0,
        "root_accel_mean": float(np.linalg.norm(root_accel, axis=-1).mean()) if root_accel.size else 0.0,
        "bone_len_cv_mean": float(np.mean(bone_cvs)),
        "bone_len_relerr_mean": float(np.mean(bone_errs)),
        "foot_contact_rate": float(contact.mean()) if contact.size else 0.0,
        "gt_foot_contact_rate": float(gt_contact.mean()) if gt_contact.size else 0.0,
        "foot_skate_speed_mean": float(foot_vel[contact].mean()) if contact.any() else 0.0,
        "foot_contact_rate_absdiff": float(abs(float(contact.mean()) - float(gt_contact.mean()))) if contact.size else 0.0,
    }


def projection_stats(projection: np.ndarray, intrinsics: np.ndarray) -> dict[str, float]:
    """Summarize 2D projected joints under a camera.

    Projection has shape [T, J, 3] with x, y, camera-depth. Intrinsics use
    [fx, fy, cx, cy], so width/height are inferred as 2*cx and 2*cy.
    """
    proj = np.asarray(projection, dtype=np.float64)
    intr = np.asarray(intrinsics, dtype=np.float64)
    frames = min(proj.shape[0], intr.shape[0])
    if frames <= 0:
        return {
            "frames": 0,
            "in_frame_joint_ratio": 0.0,
            "fully_in_frame_ratio": 0.0,
            "behind_camera_joint_ratio": 0.0,
            "projection_outlier_joint_ratio": 0.0,
            "bbox_center_x_std": 0.0,
            "bbox_center_y_std": 0.0,
            "bbox_scale_mean": 0.0,
            "bbox_scale_std": 0.0,
            "bbox_center_jitter_mean": 0.0,
            "bbox_scale_jitter_mean": 0.0,
        }

    proj = proj[:frames]
    intr = intr[:frames]
    widths = np.maximum(intr[:, 2] * 2.0, 1.0)
    heights = np.maximum(intr[:, 3] * 2.0, 1.0)
    finite_xy = np.isfinite(proj[..., :2]).all(axis=-1)
    positive_depth = np.isfinite(proj[..., 2]) & (proj[..., 2] > 0)
    in_bounds = (
        finite_xy
        & positive_depth
        & (proj[..., 0] >= 0)
        & (proj[..., 0] <= widths[:, None])
        & (proj[..., 1] >= 0)
        & (proj[..., 1] <= heights[:, None])
    )

    centers = []
    scales = []
    for frame in range(frames):
        valid = finite_xy[frame] & positive_depth[frame]
        if not valid.any():
            centers.append([np.nan, np.nan])
            scales.append(np.nan)
            continue
        xy = proj[frame, valid, :2]
        mins = xy.min(axis=0)
        maxs = xy.max(axis=0)
        center = (mins + maxs) * 0.5
        scale = max(float(maxs[0] - mins[0]), float(maxs[1] - mins[1]))
        centers.append(center.tolist())
        scales.append(scale)
    centers_np = np.asarray(centers, dtype=np.float64)
    scales_np = np.asarray(scales, dtype=np.float64)
    valid_center = np.isfinite(centers_np).all(axis=1)
    valid_scale = np.isfinite(scales_np)
    center_delta = np.diff(centers_np[valid_center], axis=0) if valid_center.sum() > 1 else np.zeros((0, 2))
    scale_delta = np.diff(scales_np[valid_scale], axis=0) if valid_scale.sum() > 1 else np.zeros((0,))

    return {
        "frames": int(frames),
        "in_frame_joint_ratio": float(in_bounds.mean()),
        "fully_in_frame_ratio": float(in_bounds.all(axis=1).mean()),
        "behind_camera_joint_ratio": float((~positive_depth).mean()),
        "projection_outlier_joint_ratio": float((~finite_xy).mean()),
        "bbox_center_x_std": float(np.nanstd(centers_np[:, 0])) if valid_center.any() else 0.0,
        "bbox_center_y_std": float(np.nanstd(centers_np[:, 1])) if valid_center.any() else 0.0,
        "bbox_scale_mean": float(np.nanmean(scales_np)) if valid_scale.any() else 0.0,
        "bbox_scale_std": float(np.nanstd(scales_np)) if valid_scale.any() else 0.0,
        "bbox_center_jitter_mean": float(np.linalg.norm(center_delta, axis=-1).mean()) if center_delta.size else 0.0,
        "bbox_scale_jitter_mean": float(np.abs(scale_delta).mean()) if scale_delta.size else 0.0,
    }


def parse_cfg_dir(cfg_dir: Path) -> dict[str, Any]:
    summary = json.loads((cfg_dir / "render_summary.json").read_text(encoding="utf-8"))
    return {
        "cfg_name": cfg_dir.name,
        "cfg_mode": summary.get("cfg_mode"),
        "cfg_scale": summary.get("cfg_scale"),
        "cfg_human": summary.get("cfg_human"),
        "cfg_camera": summary.get("cfg_camera"),
        "eta": summary.get("eta"),
        "sample_ids": [sample["sample_id"] for sample in summary["samples"]],
    }


def aggregate_projection_stats(samples: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    grouped: dict[str, dict[str, list[float]]] = {}
    for sample in samples:
        for label, stats in sample.get("projection_stats", {}).items():
            label_group = grouped.setdefault(label, {})
            for key, value in stats.items():
                if isinstance(value, (int, float)):
                    label_group.setdefault(key, []).append(float(value))
    aggregate: dict[str, dict[str, float]] = {}
    for label, values in grouped.items():
        aggregate[label] = {}
        for key, series in values.items():
            arr = np.asarray(series, dtype=np.float64)
            aggregate[label][f"{key}_mean"] = float(arr.mean()) if arr.size else 0.0
            aggregate[label][f"{key}_std"] = float(arr.std()) if arr.size else 0.0
    return aggregate


def render_one_story_config(
    args: argparse.Namespace,
    model: torch.nn.Module,
    diffusion: Any,
    autoencoder: torch.nn.Module,
    dataset: Any,
    cache: Any,
    cache_index: dict[str, int],
    device: torch.device,
    cfg: dict[str, Any],
    pulp_outputs: dict[str, Any],
) -> dict[str, Any]:
    cfg_out = args.out_dir / cfg["cfg_name"]
    cfg_out.mkdir(parents=True, exist_ok=True)
    metrics_cfg_out = (args.metrics_out_dir / cfg["cfg_name"]) if args.metrics_out_dir else cfg_out
    metrics_cfg_out.mkdir(parents=True, exist_ok=True)
    cfg_record: dict[str, Any] = {"config": cfg, "samples": []}

    for sample_ord, sample_id in enumerate(cfg["sample_ids"]):
        print(f"[{cfg['cfg_name']}] {sample_ord + 1}/{len(cfg['sample_ids'])} {sample_id}", flush=True)
        item = cache[cache_index[sample_id]]
        z = item["z"].unsqueeze(0).to(device)
        text = item["text"].unsqueeze(0).to(device)
        valid = item["valid"].unsqueeze(0).to(device)

        sample = dataset.get_sample(sample_id)
        gt_c2w, gt_intrinsics, gt_joints = rbr.get_gt_tensors(sample, device)
        frames = int(sample["padding_mask"].long().sum().item())
        gt_cam = gt_c2w[0, :frames, :3, 3].detach().cpu().numpy()
        gt_c2w_np = gt_c2w[0, :frames].detach().cpu().numpy()
        gt_intr_np = gt_intrinsics[0, :frames].detach().cpu().numpy()
        gt_joints_np = gt_joints[0, :frames].detach().cpu().numpy()

        story: dict[str, dict[str, np.ndarray]] = {}
        for task_id, task_name in rbr.mod.TASK_NAMES.items():
            sample_indices = [args.seed + sample_ord * 1000 + task_id]
            completion = rbr.ddim_sample_bilateral(
                model,
                diffusion,
                z,
                text,
                valid,
                task_id,
                sample_indices,
                args.seed + {"camera": 11, "human": 23, "joint": 37}[task_name],
                args.story_num_steps,
                cfg_scale=cfg["cfg_scale"],
                cfg_human=cfg["cfg_human"],
                cfg_camera=cfg["cfg_camera"],
                eta=cfg["eta"],
                channel_gated_cfg=args.story_channel_gated_cfg,
            )
            raw_output = rbr.decode_raw(autoencoder, dataset, completion, gt_intrinsics)
            raw_camera = raw_output["camera"][0, :frames].detach().cpu().numpy()
            pred_cam = raw_output["camera"][0, :frames, :3, 3].detach().cpu().numpy()
            pred_joints = raw_output["human"].joints[0, :frames, :22, :3].detach().cpu().numpy()
            story[task_name] = {
                "camera": pred_cam,
                "raw_camera": raw_camera,
                "joints": gt_joints_np if task_name == "camera" else pred_joints,
                "pred_joints": pred_joints,
            }

        sample_idx = pulp_outputs["sample_ids"].index(sample_id)
        pulp_series: dict[str, dict[str, np.ndarray]] = {}
        for label, outputs in pulp_outputs["outputs"].items():
            raw = outputs["raw_output"]
            pulp_series[label] = {
                "camera": np_camera(raw["camera"], sample_idx, frames),
                "joints": np_joints(raw["human"], sample_idx, frames),
            }

        context = rbr.render_context_from_joints(
            [gt_joints_np]
            + [values["joints"] for values in pulp_series.values()]
            + [story["human"]["joints"], story["joint"]["joints"]]
        )
        sample_out = cfg_out / sample_id
        sample_out.mkdir(parents=True, exist_ok=True)
        metrics_sample_out = metrics_cfg_out / sample_id
        metrics_sample_out.mkdir(parents=True, exist_ok=True)

        gt_video = sample_out / "gt_skeleton.mp4"
        rbr.render_3d_video(gt_joints_np, context, gt_video, args.fps, f"{sample_id} [GT]")
        video_paths = {"gt": gt_video}
        projection_video_paths: dict[str, Path] = {}
        projection_metrics: dict[str, dict[str, float]] = {}

        def render_projection(label: str, joints: np.ndarray, c2w: np.ndarray, intrinsics: np.ndarray) -> None:
            projection = rbr.project_joints(joints, c2w, intrinsics)
            path = sample_out / f"{label}_camera_projection.mp4"
            rbr.render_video(projection, intrinsics, path, args.fps, f"{sample_id} [{label} projection]")
            projection_video_paths[label] = path
            projection_metrics[label] = projection_stats(projection, intrinsics)

        render_projection("gt", gt_joints_np, gt_c2w_np, gt_intr_np)
        for label, values in pulp_series.items():
            path = sample_out / f"{label}_skeleton.mp4"
            rbr.render_3d_video(values["joints"], context, path, args.fps, f"{sample_id} [{label}]")
            video_paths[label] = path
            # PulpMotion camera and human are rendered together in the native
            # generated camera view, which is the reliability check missing
            # from fixed-view skeleton renders.
            raw = pulp_outputs["outputs"][label]["raw_output"]
            sample_idx = pulp_outputs["sample_ids"].index(sample_id)
            pulp_c2w = raw["camera"][sample_idx, :frames].detach().cpu().numpy()
            render_projection(label, values["joints"], pulp_c2w, gt_intr_np)
        for label in ["human", "joint"]:
            path = sample_out / f"story_{label}_skeleton.mp4"
            rbr.render_3d_video(story[label]["joints"], context, path, args.fps, f"{sample_id} [story_{label}]")
            video_paths[f"story_{label}"] = path
            story_camera = gt_c2w_np if label == "human" else story["joint"]["raw_camera"]
            render_projection(f"story_{label}", story[label]["joints"], story_camera, gt_intr_np)
        render_projection("story_camera", story["camera"]["joints"], story["camera"]["raw_camera"], gt_intr_np)

        joint_concat = sample_out / "joint_fair_concat.mp4"
        rbr.concat_videos(
            [video_paths["gt"]]
            + [video_paths[label] for label in pulp_series]
            + [video_paths["story_joint"]],
            joint_concat,
        )
        human_joint_concat = sample_out / "story_human_vs_joint_concat.mp4"
        rbr.concat_videos([video_paths["gt"], video_paths["story_human"], video_paths["story_joint"]], human_joint_concat)
        projection_concat = sample_out / "camera_projection_fair_concat.mp4"
        rbr.concat_videos(
            [projection_video_paths["gt"]]
            + [projection_video_paths[label] for label in pulp_series]
            + [
                projection_video_paths["story_camera"],
                projection_video_paths["story_human"],
                projection_video_paths["story_joint"],
            ],
            projection_concat,
        )

        png_path = sample_out / "fair_compare.png"
        plot_compare_png(
            png_path,
            sample_id,
            gt_cam,
            gt_joints_np,
            {
                **pulp_series,
                "story_human": story["human"],
                "story_joint": story["joint"],
            },
        )
        stats = {
            **{label: motion_stats(values["joints"], gt_joints_np) for label, values in pulp_series.items()},
            "story_human": motion_stats(story["human"]["joints"], gt_joints_np),
            "story_joint": motion_stats(story["joint"]["joints"], gt_joints_np),
        }
        sample_record = {
            "sample_id": sample_id,
            "valid_frames": frames,
            "render_context": {
                "center_xy": [float(x) for x in context["center_xy"]],
                "ground_z": float(context["ground_z"]),
                "xy_limit": float(context["xy_limit"]),
                "z_limit": float(context["z_limit"]),
            },
            "videos": {key: str(path) for key, path in video_paths.items()},
            "camera_projection_videos": {key: str(path) for key, path in projection_video_paths.items()},
            "joint_fair_concat": str(joint_concat),
            "story_human_vs_joint_concat": str(human_joint_concat),
            "camera_projection_fair_concat": str(projection_concat),
            "fair_compare_png": str(png_path),
            "motion_stats": stats,
            "projection_stats": projection_metrics,
        }
        (metrics_sample_out / "summary.json").write_text(json.dumps(sample_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        cfg_record["samples"].append(sample_record)

    cfg_record["projection_stats_aggregate"] = aggregate_projection_stats(cfg_record["samples"])
    (metrics_cfg_out / "render_summary.json").write_text(json.dumps(cfg_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cfg_record


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--source-render-dir", type=Path, default=ROOT / "runs/eval/stage2/bilateral_cfg_renders_20260614")
    p.add_argument("--out-dir", type=Path, default=ROOT / "runs/eval/stage2/bilateral_cfg_pulpmotion_fair_compare_20260615")
    p.add_argument("--metrics-out-dir", type=Path, default=None)
    p.add_argument("--story-ckpt", type=Path, default=ROOT / "runs/train/stage2/pulp_official_full_mixed_20260611/gpu3_branchmean_jointheavy6_ft_b512_102688_20260612_2151/last.pt")
    p.add_argument("--cache-dir", type=Path, default=ROOT / "runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110")
    p.add_argument("--pulp-root", type=Path, default=PULP_ROOT)
    p.add_argument("--data-root", type=Path, default=ROOT / "linked/pulpmotion-data")
    p.add_argument("--model-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models"))
    p.add_argument("--pulp-checkpoint", type=Path, default=Path("/data/public/ripemangobox/Motion/PulpMotion_official_eval/pulpmotion-models/runs/dit-xy-ddpm-4dlbunha-330750.ckpt"))
    p.add_argument("--config-name", default="config_dit_xy")
    p.add_argument("--set-name", default="mixed_")
    p.add_argument("--pulp-cfg-c", type=float, default=11.0)
    p.add_argument("--pulp-cfg-z", type=float, nargs="+", default=[0.0, 2.0])
    p.add_argument("--pulp-num-steps", type=int, default=50)
    p.add_argument("--story-num-steps", type=int, default=50)
    p.add_argument("--story-channel-gated-cfg", action="store_true")
    p.add_argument("--fps", type=int, default=12)
    p.add_argument("--seed", type=int, default=20260614)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--configs", nargs="*")
    return p


def main() -> None:
    args = build_parser().parse_args()
    patch_numpy_aliases()
    add_pulp_paths(args.pulp_root)
    torch.set_float32_matmul_precision("medium")
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device(args.device)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if args.metrics_out_dir:
        args.metrics_out_dir.mkdir(parents=True, exist_ok=True)

    print("Loading StoryMotion model and Pulp dataset...", flush=True)
    story_model, story_diffusion, story_ckpt = rbr.load_model(args.story_ckpt, device)
    pulp_args = copy.copy(args)
    _, dataset, autoencoder = rbr.build_pulp(pulp_args, device)
    cache = rbr.mod.PulpLatentCache(args.cache_dir / "val.pt")
    cache_index = {str(cache[i]["sample_id"]): i for i in range(len(cache))}

    cfg_dirs = sorted(path for path in args.source_render_dir.iterdir() if path.is_dir() and (path / "render_summary.json").exists())
    if args.configs:
        wanted = set(args.configs)
        cfg_dirs = [path for path in cfg_dirs if path.name in wanted]
    configs = [parse_cfg_dir(path) for path in cfg_dirs]
    sample_ids = sorted({sample_id for cfg in configs for sample_id in cfg["sample_ids"]})

    print(f"Loading PulpMotion official outputs for {len(sample_ids)} samples...", flush=True)
    pulp_outputs: dict[str, Any] = {"sample_ids": sample_ids, "outputs": {}}
    for cfg_z in args.pulp_cfg_z:
        label = f"pulpmotion_wz{cfg_z:g}_wc{args.pulp_cfg_c:g}".replace(".", "p")
        print(f"  PulpMotion {label}", flush=True)
        pulp_model, pulp_ckpt = build_pulpmotion_model(args, device, cfg_z)
        outputs, _ = run_pulpmotion(pulp_model, dataset, sample_ids, device, args.seed + int(cfg_z * 1000) + 42)
        pulp_outputs["outputs"][label] = outputs
        del pulp_model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    start = time.time()
    records = []
    for cfg in configs:
        records.append(
            render_one_story_config(
                args,
                story_model,
                story_diffusion,
                autoencoder,
                dataset,
                cache,
                cache_index,
                device,
                cfg,
                pulp_outputs,
            )
        )

    manifest = {
        "mode": "pulpmotion_fair_compare_for_bilateral_cfg_renders",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "source_render_dir": str(args.source_render_dir),
        "out_dir": str(args.out_dir),
        "metrics_out_dir": str(args.metrics_out_dir) if args.metrics_out_dir else str(args.out_dir),
        "story_checkpoint": str(args.story_ckpt),
        "story_checkpoint_step": int(story_ckpt.get("step", -1)),
        "story_sampler": {"num_steps": args.story_num_steps, "seed": args.seed, "channel_gated_cfg": bool(args.story_channel_gated_cfg)},
        "pulp_checkpoint": str(args.pulp_checkpoint),
        "pulp_sampler": {
            "num_steps": args.pulp_num_steps,
            "cfg_rate_c": args.pulp_cfg_c,
            "cfg_rate_z": args.pulp_cfg_z,
            "seed_base": args.seed,
        },
        "sample_ids": sample_ids,
        "configs": records,
        "elapsed_sec": time.time() - start,
    }
    manifest_dir = args.metrics_out_dir if args.metrics_out_dir else args.out_dir
    (manifest_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out_dir": str(args.out_dir), "configs": len(records), "samples": len(sample_ids)}, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
