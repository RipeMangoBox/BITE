#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch


def link(src: Path, dst: Path) -> None:
    if dst.exists() or dst.is_symlink():
        return
    dst.symlink_to(src)


def load_ids(cache_path: Path) -> list[str]:
    data = torch.load(cache_path, map_location="cpu")
    ids = data.get("sample_id")
    if ids is None:
        raise KeyError(f"{cache_path} has no sample_id")
    return [str(x) for x in ids]


def write_split(path: Path, ids: list[str]) -> None:
    # DIRECTOR uses raw split_text.split("\n"); a trailing newline becomes an empty sample id.
    path.write_text("\n".join(ids), encoding="utf-8")


def save_float_clip(src: Path, dst: Path) -> bool:
    if dst.exists():
        return False
    arr = np.load(src, allow_pickle=True)
    arr = coerce_clip_array(arr, is_seq=(src.parent.name == "seq"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    np.save(dst, arr.astype(np.float32, copy=False))
    return True


def collect_clip_blocks(value: object, blocks: list[np.ndarray]) -> None:
    try:
        arr = np.asarray(value, dtype=np.float32)
    except (TypeError, ValueError):
        if isinstance(value, (list, tuple)):
            for item in value:
                collect_clip_blocks(item, blocks)
        return
    if arr.ndim == 1 and arr.shape[0] == 512:
        blocks.append(arr[None, :])
    elif arr.ndim == 2 and arr.shape[-1] == 512:
        blocks.append(arr)
    elif arr.ndim == 3 and arr.shape[-1] == 512:
        blocks.append(arr.reshape(-1, 512))
    elif isinstance(value, (list, tuple)):
        for item in value:
            collect_clip_blocks(item, blocks)


def coerce_clip_array(arr: np.ndarray, is_seq: bool) -> np.ndarray:
    try:
        out = np.asarray(arr.tolist() if arr.dtype == object else arr, dtype=np.float32)
    except (TypeError, ValueError):
        blocks: list[np.ndarray] = []
        collect_clip_blocks(arr.tolist() if arr.dtype == object else arr, blocks)
        if not blocks:
            raise
        out = np.concatenate(blocks, axis=0)
    if out.ndim >= 1 and out.shape[0] == 1:
        out = out[0]
    if is_seq:
        out = out.reshape(-1, 512)[:77]
    else:
        out = out.reshape(-1, 512).mean(axis=0)
    return out.astype(np.float32, copy=False)


def export_clip_dirs(src_root: Path, dst_root: Path, ids: list[str]) -> int:
    if dst_root.is_symlink():
        dst_root.unlink()
    written = 0
    for sub in ["seq", "token"]:
        for sample_id in ids:
            src = src_root / sub / f"{sample_id}.npy"
            if not src.exists():
                continue
            dst = dst_root / sub / f"{sample_id}.npy"
            written += int(save_float_clip(src, dst))
    return written


def save_fixed_intrinsics(src: Path, dst: Path, num_cams: int = 300) -> bool:
    if dst.exists():
        return False
    arr = np.load(src).astype(np.float32, copy=False)
    out = np.zeros((num_cams, arr.shape[-1]), dtype=np.float32)
    n = min(num_cams, arr.shape[0])
    out[:n] = arr[:n]
    dst.parent.mkdir(parents=True, exist_ok=True)
    np.save(dst, out)
    return True


def export_intrinsics(src_root: Path, dst_root: Path, ids: list[str]) -> int:
    if dst_root.is_symlink():
        dst_root.unlink()
    written = 0
    for sample_id in ids:
        src = src_root / f"{sample_id}.npy"
        if not src.exists():
            continue
        written += int(save_fixed_intrinsics(src, dst_root / f"{sample_id}.npy"))
    return written


def load_smpl_transl(path: Path) -> np.ndarray:
    data = np.load(path, allow_pickle=True)
    smpl = data.item() if data.shape == () else data[()]
    transl = np.asarray(smpl["transl"], dtype=np.float32)
    if transl.ndim != 2 or transl.shape[1] != 3:
        raise ValueError(f"{path} transl must have shape (T, 3), got {transl.shape}")
    return transl


def save_char(src: Path, dst: Path) -> bool:
    if dst.exists():
        return False
    transl = load_smpl_transl(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    np.save(dst, transl.astype(np.float32, copy=False))
    return True


def export_char_dirs(src_root: Path, dst_root: Path, ids: list[str]) -> tuple[int, int]:
    char_dir = dst_root / "char"
    char_raw_dir = dst_root / "char_raw"
    if char_dir.is_symlink():
        char_dir.unlink()
    if char_raw_dir.is_symlink():
        char_raw_dir.unlink()
    char_written = 0
    char_raw_written = 0
    for sample_id in ids:
        src = src_root / f"{sample_id}.npy"
        if not src.exists():
            continue
        char_written += int(save_char(src, char_dir / f"{sample_id}.npy"))
        char_raw_written += int(save_char(src, char_raw_dir / f"{sample_id}.npy"))
    return char_written, char_raw_written


class RunningStats:
    def __init__(self) -> None:
        self.count = 0
        self.sum = np.zeros(3, dtype=np.float64)
        self.sum_sq = np.zeros(3, dtype=np.float64)

    def update(self, values: np.ndarray) -> None:
        values = np.asarray(values, dtype=np.float64).reshape(-1, 3)
        if values.size == 0:
            return
        self.count += values.shape[0]
        self.sum += values.sum(axis=0)
        self.sum_sq += np.square(values).sum(axis=0)

    def mean_std(self) -> tuple[np.ndarray, np.ndarray]:
        if self.count == 0:
            raise ValueError("cannot compute stats from zero values")
        mean = self.sum / self.count
        var = np.maximum(self.sum_sq / self.count - np.square(mean), 0.0)
        std = np.sqrt(var)
        std = np.maximum(std, 1.0e-8)
        return mean.astype(np.float64), std.astype(np.float64)


def load_kitti_translations(path: Path) -> np.ndarray:
    poses = np.loadtxt(path, dtype=np.float64)
    poses = np.atleast_2d(poses)
    if poses.shape[1] != 12:
        raise ValueError(f"{path} must contain KITTI 3x4 poses, got {poses.shape}")
    return poses.reshape(-1, 3, 4)[:, :, 3]


def compute_standardization(pulp_root: Path, ids: list[str]) -> dict[str, object]:
    cam_shift = RunningStats()
    cam_velocity = RunningStats()
    char_shift = RunningStats()
    char_velocity = RunningStats()

    for sample_id in ids:
        cam_trans = load_kitti_translations(pulp_root / "traj" / f"{sample_id}.txt")
        char_trans = load_smpl_transl(pulp_root / "smpl_raw" / f"{sample_id}.npy")
        cam_shift.update(cam_trans[:1])
        char_shift.update(char_trans[:1])
        if cam_trans.shape[0] > 1:
            cam_velocity.update(cam_trans[1:] - cam_trans[:-1])
        if char_trans.shape[0] > 1:
            char_velocity.update(char_trans[1:] - char_trans[:-1])

    cam_norm_mean, cam_norm_std = cam_velocity.mean_std()
    cam_shift_mean, cam_shift_std = cam_shift.mean_std()
    char_shift_mean, char_shift_std = char_shift.mean_std()
    char_velocity_mean, char_velocity_std = char_velocity.mean_std()

    return {
        "name": "pulp0300",
        "num_interframes": 0,
        "num_cams": 300,
        "num_total_frames": "${eval:'${dataset.standardization.num_interframes} * (${dataset.standardization.num_cams} - 1) + ${dataset.standardization.num_cams} '}",
        "norm_mean": cam_norm_mean.tolist(),
        "norm_std": cam_norm_std.tolist(),
        "shift_mean": cam_shift_mean.tolist(),
        "shift_std": cam_shift_std.tolist(),
        "norm_mean_h": np.concatenate([char_shift_mean, char_velocity_mean]).tolist(),
        "norm_std_h": np.concatenate([char_shift_std, char_velocity_std]).tolist(),
        "velocity": True,
    }


def yaml_list(values: list[float]) -> str:
    return "[" + ", ".join(f"{float(x):.8g}" for x in values) + "]"


def write_standardization_yaml(path: Path, stats: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(
        [
            "name: 'pulp0300'",
            "num_interframes: 0",
            "num_cams: 300",
            "num_total_frames: ${eval:'${dataset.standardization.num_interframes} * (${dataset.standardization.num_cams} - 1) + ${dataset.standardization.num_cams} '}",
            "",
            f"norm_mean: {yaml_list(stats['norm_mean'])}",
            f"norm_std: {yaml_list(stats['norm_std'])}",
            "",
            f"shift_mean: {yaml_list(stats['shift_mean'])}",
            f"shift_std: {yaml_list(stats['shift_std'])}",
            "",
            f"norm_mean_h: {yaml_list(stats['norm_mean_h'])}",
            f"norm_std_h: {yaml_list(stats['norm_std_h'])}",
            "",
            "velocity: true",
            "",
        ]
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser(description="Prepare PulpMotion data view for DIRECTOR from-scratch training.")
    p.add_argument("--pulp-root", type=Path, default=Path("/data/public/ripemangobox/Motion/datasets/pulpmotion-data"))
    p.add_argument("--cache-dir", type=Path, default=Path("/data/public/ripemangobox/Motion/StoryMotion/runs/train/stage2/pulp_official_full_mixed_20260611/cache_mixed_full_nw0_20260611_2110"))
    p.add_argument("--out", type=Path, default=Path("/data/public/ripemangobox/Motion/baselines/data/director_pulp_mixed"))
    p.add_argument("--set-name", default="mixed")
    p.add_argument("--standardization-out", type=Path, default=None)
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    for name in [
        "traj",
        "cam_segments",
        "caption_cam",
    ]:
        link((args.pulp_root / name).resolve(), args.out / name)

    # Use camera captions for the generic caption path if a config accidentally requests it.
    link((args.pulp_root / "caption_cam").resolve(), args.out / "caption")

    train_ids = load_ids(args.cache_dir / "train.pt")
    test_ids = load_ids(args.cache_dir / "val.pt")
    write_split(args.out / f"{args.set_name}_train_split.txt", train_ids)
    write_split(args.out / f"{args.set_name}_test_split.txt", test_ids)
    write_split(args.out / f"{args.set_name}_val_split.txt", test_ids)
    all_ids = train_ids + test_ids
    clip_written = export_clip_dirs(args.pulp_root / "caption_cam_clip", args.out / "caption_cam_clip", all_ids)
    intrinsics_written = export_intrinsics(args.pulp_root / "intrinsics", args.out / "intrinsics", all_ids)
    char_written, char_raw_written = export_char_dirs(args.pulp_root / "smpl_raw", args.out, all_ids)
    standardization_path = args.standardization_out or (args.out / "pulp0300.yaml")
    standardization = compute_standardization(args.pulp_root, train_ids)
    write_standardization_yaml(standardization_path, standardization)
    # DIRECTOR's CaptionDataset always reads caption_clip/seq for CLaTr text.
    if (args.out / "caption_clip").is_symlink():
        (args.out / "caption_clip").unlink()
    link((args.out / "caption_cam_clip").resolve(), args.out / "caption_clip")

    payload = {
        "mode": "director_pulp_data_view",
        "pulp_root": str(args.pulp_root),
        "cache_dir": str(args.cache_dir),
        "out": str(args.out),
        "set_name": args.set_name,
        "train_samples": len(train_ids),
        "test_samples": len(test_ids),
        "clip_float32_files_written": clip_written,
        "intrinsics_fixed_files_written": intrinsics_written,
        "char_files_written": char_written,
        "char_raw_files_written": char_raw_written,
        "standardization_out": str(standardization_path),
        "standardization_train_samples": len(train_ids),
        "links": sorted(x.name for x in args.out.iterdir() if x.is_symlink()),
    }
    (args.out / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
