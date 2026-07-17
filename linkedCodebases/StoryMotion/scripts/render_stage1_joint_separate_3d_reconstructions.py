#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import torch


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import render_stage1_3d_reconstructions as base_vis
from scripts.train_storymotion_joint_tokenizer import PRESETS
from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer
from storymotion.training.camera_data import camera_poses_to_features, read_kitti_camera_poses
from storymotion.training.joint_data import (
    LEGACY_FEATURE_CONTRACT,
    OFFICIAL_FEATURE_CONTRACT,
    _load_official_stats,
    _official_camera_features,
    _rifke_root_translation,
)
from storymotion.training.human200 import (
    HUMAN200_DIM,
    HUMAN200_FEATURE_CONTRACT,
    HUMAN200_LAYOUT,
    human199_raw_to_human200,
    human200_to_human199_raw,
    load_human200_stats,
)


FFMPEG_DIR = Path("/home/ripemangobox/miniconda3/bin")
if FFMPEG_DIR.exists():
    os.environ["PATH"] = f"{FFMPEG_DIR}:{os.environ.get('PATH', '')}"


@dataclass(frozen=True)
class ModelSpec:
    name: str
    preset: str
    checkpoint: Path
    drop_camera_z: bool = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Stage1 joint/separate human reconstructions with a shared GT camera.")
    parser.add_argument("--human-manifest", type=Path, default=Path("runs/train/pulpmotion_native_test_manifest_full_20260608.jsonl"))
    parser.add_argument("--camera-manifest", type=Path, default=Path("runs/train/pulpmotion_camera_test_manifest_full_20260610.jsonl"))
    parser.add_argument("--sample-ids", type=Path, help="Optional newline-separated sample_id allowlist.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--num-samples", type=int, default=8)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--fps", type=int, default=12)
    parser.add_argument(
        "--model",
        action="append",
        default=[],
        help="Model spec: name:preset:checkpoint[:dropz]. Use dropz for camera xy+rot6d checkpoints.",
    )
    parser.add_argument("--no-concat", action="store_true")
    parser.add_argument("--human200-stats", type=Path)
    return parser.parse_args()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def resolve(path: str | Path, root: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else root / value


def parse_model_spec(raw: str) -> ModelSpec:
    parts = raw.split(":")
    if len(parts) not in {3, 4}:
        raise ValueError(f"model spec must be name:preset:checkpoint[:dropz], got {raw!r}")
    name, preset, checkpoint = parts[:3]
    if preset not in PRESETS:
        raise KeyError(f"unknown preset {preset!r}")
    return ModelSpec(name=name, preset=preset, checkpoint=Path(checkpoint), drop_camera_z=(len(parts) == 4 and parts[3] == "dropz"))


def load_sample_ids(path: Path | None) -> set[str] | None:
    if path is None:
        return None
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def load_checkpoint_run_config(checkpoint: Path) -> dict[str, Any]:
    candidates = (
        checkpoint.parent.parent / "run_config.json",
        checkpoint.parent.parent.parent / "run_config.json",
    )
    for path in candidates:
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    return {}


def load_paired_rows(human_manifest: Path, camera_manifest: Path, sample_ids: set[str] | None, limit: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    camera_by_id = {str(row["sample_id"]): row for row in read_jsonl(camera_manifest)}
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for human_row in read_jsonl(human_manifest):
        sample_id = str(human_row.get("sample_id") or "")
        if sample_ids is not None and sample_id not in sample_ids:
            continue
        camera_row = camera_by_id.get(sample_id)
        if camera_row is None:
            continue
        if human_row.get("feature_space") != "pulpmotion_smpl_rifke":
            raise ValueError(f"unsupported human feature_space: {human_row.get('feature_space')!r}")
        if camera_row.get("feature_space") != "pulpmotion_camera_c2w_rot6d":
            raise ValueError(f"unsupported camera feature_space: {camera_row.get('feature_space')!r}")
        pairs.append((human_row, camera_row))
        if len(pairs) >= limit:
            break
    if not pairs:
        raise ValueError("no paired rows selected")
    return pairs


def model_kwargs(spec: ModelSpec) -> tuple[str, dict[str, Any]]:
    values = dict(PRESETS[spec.preset])
    run_config = load_checkpoint_run_config(spec.checkpoint)
    if "is_causal" in run_config:
        values["is_causal"] = bool(run_config["is_causal"])
    tokenizer = values.pop("tokenizer")
    values.pop("feature_contract", None)
    if spec.drop_camera_z:
        values["camera_dim"] = int(values["camera_dim"]) - 1
    return tokenizer, values


def feature_contract(spec: ModelSpec) -> str:
    run_config = load_checkpoint_run_config(spec.checkpoint)
    return str(run_config.get("feature_contract", PRESETS[spec.preset].get("feature_contract", LEGACY_FEATURE_CONTRACT)))


def build_model(
    spec: ModelSpec,
    device: str,
    human200_stats_path: str | Path | None = None,
) -> torch.nn.Module:
    tokenizer, kwargs = model_kwargs(spec)
    model = build_joint_human_camera_tokenizer(tokenizer, **kwargs)
    checkpoint = torch.load(spec.checkpoint, map_location="cpu", weights_only=False)
    contract = checkpoint.get("stage1_model_contract", {}) if isinstance(checkpoint, dict) else {}
    if feature_contract(spec) == HUMAN200_FEATURE_CONTRACT:
        if human200_stats_path is None:
            raise ValueError("v8.2 evaluation requires --human200-stats")
        stats = load_human200_stats(human200_stats_path)
        normalization = contract.get("normalization")
        representation = contract.get("human_representation")
        expected_native_order = f"camera{model.camera_latent_dim}+human{model.human_latent_dim}"
        mismatches = {
            "feature_contract": (contract.get("feature_contract"), HUMAN200_FEATURE_CONTRACT),
            "preset": (contract.get("preset"), spec.preset),
            "is_causal": (contract.get("is_causal"), False),
            "human_dim": (contract.get("human_dim"), HUMAN200_DIM),
            "native_latent_order": (contract.get("native_latent_order"), expected_native_order),
            "normalization.sha256": (
                normalization.get("sha256") if isinstance(normalization, dict) else None,
                stats["sha256"],
            ),
            "normalization.source_manifest_sha256": (
                normalization.get("source_manifest_sha256") if isinstance(normalization, dict) else None,
                stats["meta"]["source"]["manifest_sha256"],
            ),
            "normalization.source_sample_ids_sha256": (
                normalization.get("source_sample_ids_sha256") if isinstance(normalization, dict) else None,
                stats["meta"]["source"]["sample_ids_sha256"],
            ),
            "normalization.source_split": (
                normalization.get("source_split") if isinstance(normalization, dict) else None,
                "train",
            ),
            "human_representation.layout": (
                representation.get("layout") if isinstance(representation, dict) else None,
                HUMAN200_LAYOUT,
            ),
        }
        bad = {key: value for key, value in mismatches.items() if value[0] != value[1]}
        if bad:
            raise ValueError(f"v8.2 checkpoint/evaluation contract mismatch: {bad}")
        model.human200_stats = stats
    model.load_state_dict(checkpoint["model"], strict=True)
    model.to(device)
    model.eval()
    return model


def load_camera_features(camera_row: dict[str, Any], camera_manifest: Path, drop_camera_z: bool) -> torch.Tensor:
    raw_path = camera_row.get("camera_trajectory_path") or camera_row.get("traj_path")
    if not raw_path:
        raise KeyError(f"camera row is missing trajectory path for {camera_row.get('sample_id')}")
    path = resolve(raw_path, camera_manifest.parent)
    camera = torch.from_numpy(camera_poses_to_features(read_kitti_camera_poses(path))).float()
    if camera.ndim != 2 or camera.shape[1] != 9:
        raise ValueError(f"expected camera feature [T,9], got {tuple(camera.shape)} from {path}")
    if drop_camera_z:
        camera = torch.cat([camera[:, :2], camera[:, 3:]], dim=-1)
    return camera


def reconstruct(model: torch.nn.Module, spec: ModelSpec, human_rifke: torch.Tensor, camera_row: dict[str, Any], camera_manifest: Path, device: str) -> torch.Tensor:
    contract = feature_contract(spec)
    if contract in {OFFICIAL_FEATURE_CONTRACT, HUMAN200_FEATURE_CONTRACT}:
        raw_path = camera_row.get("camera_trajectory_path") or camera_row.get("traj_path")
        intrinsics_path = camera_row.get("intrinsics_path")
        if not raw_path or not intrinsics_path:
            raise KeyError(f"official camera14 reconstruction needs trajectory and intrinsics for {camera_row.get('sample_id')}")
        poses = torch.from_numpy(read_kitti_camera_poses(resolve(raw_path, camera_manifest.parent))).float()
        intrinsics = torch.from_numpy(np.load(resolve(intrinsics_path, camera_manifest.parent))).float()
        frames = min(int(human_rifke.shape[0]), int(poses.shape[0]), int(intrinsics.shape[0]))
        stats = _load_official_stats(REPO_ROOT / "linked/PulpMotion")
        human_raw = human_rifke[:frames]
        if contract == HUMAN200_FEATURE_CONTRACT:
            human = human199_raw_to_human200(human_raw, model.human200_stats).unsqueeze(0).to(device)
        else:
            human = ((human_raw - stats["human_mean"]) / stats["human_std"]).unsqueeze(0).to(device)
        camera = _official_camera_features(poses[:frames], intrinsics[:frames], _rifke_root_translation(human_raw), stats).unsqueeze(0).to(device)
    else:
        camera_raw = load_camera_features(camera_row, camera_manifest, spec.drop_camera_z)
        frames = min(int(human_rifke.shape[0]), int(camera_raw.shape[0]))
        human = human_rifke[:frames].unsqueeze(0).to(device)
        camera = camera_raw[:frames].unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(human, camera)
    recon = output.human_recon
    if recon.ndim != 3 or recon.shape[0] != 1 or recon.shape[2] != int(model.human_dim):
        raise ValueError(f"expected human reconstruction [1,T,{model.human_dim}], got {tuple(recon.shape)}")
    if recon.shape[1] < frames:
        raise ValueError(f"reconstruction is shorter than input: {recon.shape[1]} < {frames}")
    recon = recon[0, :frames].detach().cpu()
    if contract == OFFICIAL_FEATURE_CONTRACT:
        recon = recon * stats["human_std"] + stats["human_mean"]
    elif contract == HUMAN200_FEATURE_CONTRACT:
        recon = human200_to_human199_raw(recon, model.human200_stats)
    if not torch.isfinite(recon).all():
        raise ValueError("non-finite reconstruction values")
    return recon


def process_sample(
    index: int,
    human_row: dict[str, Any],
    camera_row: dict[str, Any],
    models: dict[str, torch.nn.Module],
    specs: dict[str, ModelSpec],
    args: argparse.Namespace,
) -> dict[str, Any]:
    sample_id = str(human_row["sample_id"])
    safe_id = base_vis.sanitize(sample_id)
    rifke_full = base_vis.load_rifke(human_row)
    camera_full = load_camera_features(camera_row, args.camera_manifest, drop_camera_z=False)
    frames = min(int(rifke_full.shape[0]), int(camera_full.shape[0]))
    rifke = rifke_full[:frames]
    camera_data = base_vis.load_camera_data(human_row)
    if camera_row.get("camera_trajectory_path"):
        camera_data["traj_path"] = str(resolve(camera_row["camera_trajectory_path"], args.camera_manifest.parent))
    if camera_row.get("intrinsics_path"):
        camera_data["intrinsics_path"] = str(resolve(camera_row["intrinsics_path"], args.camera_manifest.parent))

    model_names = ["gt"] + list(models)
    model_rifkes: dict[str, torch.Tensor] = {}
    model_joints: dict[str, np.ndarray] = {}
    for model_name in model_names:
        if model_name == "gt":
            model_rifke = rifke
        else:
            model_rifke = reconstruct(models[model_name], specs[model_name], rifke, camera_row, args.camera_manifest, args.device)
        model_rifkes[model_name] = model_rifke
        model_joints[model_name] = base_vis.rifke_to_joints_z_up(model_rifke)

    render_context = base_vis.render_context_from_joints(list(model_joints.values()))
    rendered_paths: dict[str, dict[str, Path]] = {}
    sample_record: dict[str, Any] = {
        "index": index,
        "sample_id": sample_id,
        "num_frames": frames,
        "feature_path": human_row["motion_feature_path"],
        "models": {},
    }
    gt_joints = model_joints["gt"]
    for model_name in model_names:
        model_rifke = model_rifkes[model_name]
        joints = model_joints[model_name]
        projection = base_vis.project_joints_camera(joints, camera_data)
        out_dir = args.output_dir / model_name / "test" / safe_id
        fixed = base_vis.render_3d_animation(
            joints,
            out_dir / "fixed_camera.mp4",
            args.fps,
            f"{model_name} | fixed global",
            "fixed",
            render_context,
        )
        orbit = base_vis.render_3d_animation(
            joints,
            out_dir / "orbiting_camera.mp4",
            args.fps,
            f"{model_name} | orbit global",
            "orbiting",
            render_context,
        )
        camera = base_vis.render_camera_trajectory_animation(
            projection,
            camera_data,
            out_dir / "camera_trajectory.mp4",
            args.fps,
            f"{model_name} | gt camera",
        )
        np.savez_compressed(out_dir / "rifke_joints.npz", rifke=model_rifke.numpy(), joints=joints, camera_projection=projection)
        rendered_paths[model_name] = {"fixed": fixed, "orbit": orbit, "camera": camera}
        model_record = {
            "fixed_camera_mp4": str(fixed),
            "orbiting_camera_mp4": str(orbit),
            "camera_trajectory_mp4": str(camera),
            "rifke_joints_npz": str(out_dir / "rifke_joints.npz"),
            "feature_stats": base_vis.feature_stats(model_rifke),
            "joint_stats": base_vis.joint_stats(joints),
            "projection_stats": base_vis.projection_stats(projection, camera_data),
        }
        if model_name != "gt":
            model_record["reconstruction"] = base_vis.reconstruction_stats(model_rifke, rifke, joints, gt_joints)
        sample_record["models"][model_name] = model_record

    if not args.no_concat:
        concat_dir = args.output_dir / "concat" / safe_id
        sample_record["concat"] = {
            "layout": " | ".join(model_names),
            "fixed_camera_mp4": str(base_vis.concat_videos([rendered_paths[name]["fixed"] for name in model_names], concat_dir / "fixed_camera.mp4") or ""),
            "orbiting_camera_mp4": str(base_vis.concat_videos([rendered_paths[name]["orbit"] for name in model_names], concat_dir / "orbiting_camera.mp4") or ""),
            "camera_trajectory_mp4": str(base_vis.concat_videos([rendered_paths[name]["camera"] for name in model_names], concat_dir / "camera_trajectory.mp4") or ""),
        }
    return sample_record


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    specs = {spec.name: spec for spec in (parse_model_spec(raw) for raw in args.model)}
    models = {name: build_model(spec, args.device, args.human200_stats) for name, spec in specs.items()}
    pairs = load_paired_rows(args.human_manifest, args.camera_manifest, load_sample_ids(args.sample_ids), args.num_samples)
    summary: dict[str, Any] = {
        "axis_convention": "PulpMotion z-up; decoded by utils.rifke_utils.smplrifkefeats_to_smpldata",
        "model_contract": "All models reconstruct human RIFKE from paired human RIFKE + camera features; visual projection uses the dataset GT camera to isolate human reconstruction quality.",
        "output_dir": str(args.output_dir),
        "human_manifest": str(args.human_manifest),
        "camera_manifest": str(args.camera_manifest),
        "sample_ids": str(args.sample_ids) if args.sample_ids else None,
        "fps": args.fps,
        "models": [{"name": spec.name, "preset": spec.preset, "checkpoint": str(spec.checkpoint), "drop_camera_z": spec.drop_camera_z} for spec in specs.values()],
        "samples": [],
    }
    for index, (human_row, camera_row) in enumerate(pairs):
        print(f"rendering test {index}: {human_row['sample_id']}", flush=True)
        summary["samples"].append(process_sample(index, human_row, camera_row, models, specs, args))
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "output_dir": str(args.output_dir), "samples": len(summary["samples"])}, indent=2))


if __name__ == "__main__":
    main()
