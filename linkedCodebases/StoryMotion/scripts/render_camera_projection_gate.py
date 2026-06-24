#!/usr/bin/env python3
"""Render camera-view human motion for a small StoryMotion/PulpMotion gate.

The renderer uses PulpMotion's PyTorch3D camera conversion and updates the full
per-frame intrinsics. This matters for generated focal-length motion:
PulpMotion's original ``render_views`` reads only the first frame's focal length.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

os.environ.setdefault("PYOPENGL_PLATFORM", "egl")

import numpy as np
import torch
from PIL import Image, ImageDraw


ROOT = Path("/data/public/ripemangobox/Motion/StoryMotion")
SCRIPT_DIR = ROOT / "scripts"
PULP_ROOT = ROOT / "linked/PulpMotion"
BONES = [
    (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (3, 6),
    (4, 7), (5, 8), (6, 9), (7, 10), (8, 11), (9, 12),
    (9, 13), (9, 14), (12, 15), (13, 16), (14, 17),
    (16, 18), (17, 19), (18, 20), (19, 21),
]


def load_local_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fair = load_local_module("render_pulpmotion_fair_compare", SCRIPT_DIR / "render_pulpmotion_fair_compare.py")
rbr = fair.rbr


def json_float(value: Any) -> float:
    return float(np.asarray(value).item())


class DiskGuard:
    def __init__(self, mount: Path, errors_count: Path, stop_file: Path, max_used: float):
        self.mount = mount
        self.errors_count = errors_count
        self.stop_file = stop_file
        self.max_used = max_used
        self.baseline_errors = self._errors()

    def _errors(self) -> int:
        return int(self.errors_count.read_text(encoding="utf-8").strip())

    def check(self, stage: str) -> dict[str, float | int]:
        if self.stop_file.exists():
            raise RuntimeError(f"disk guard stop file exists at {stage}: {self.stop_file}")
        errors = self._errors()
        if errors != self.baseline_errors:
            raise RuntimeError(
                f"disk errors_count changed at {stage}: {self.baseline_errors} -> {errors}"
            )
        usage = shutil.disk_usage(self.mount)
        used_ratio = usage.used / usage.total
        if used_ratio >= self.max_used:
            raise RuntimeError(f"disk usage {used_ratio:.1%} reached limit {self.max_used:.1%} at {stage}")
        return {"errors_count": errors, "used_ratio": used_ratio, "free_bytes": usage.free}


class RawVideoWriter:
    def __init__(self, ffmpeg: str, path: Path, width: int, height: int, fps: int):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.width = width
        self.height = height
        self.proc = subprocess.Popen(
            [
                ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
                "-pix_fmt", "rgb24", "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
                "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path),
            ],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def write(self, frame: np.ndarray) -> None:
        if frame.shape != (self.height, self.width, 3):
            raise ValueError(f"bad frame shape {frame.shape}, expected {(self.height, self.width, 3)}")
        assert self.proc.stdin is not None
        self.proc.stdin.write(np.ascontiguousarray(frame, dtype=np.uint8).tobytes())

    def close(self) -> None:
        assert self.proc.stdin is not None and self.proc.stderr is not None
        self.proc.stdin.close()
        stderr = self.proc.stderr.read().decode("utf-8", errors="replace")
        code = self.proc.wait()
        if code:
            raise RuntimeError(f"ffmpeg failed for {self.path}: {stderr[-4000:]}")


class CameraViewRenderer:
    """PulpMotion PyTorch3D camera renderer with per-frame intrinsics."""

    def __init__(self, width: int, height: int, faces: np.ndarray):
        from pytorch3d.renderer import (
            BlendParams,
            HardPhongShader,
            MeshRasterizer,
            PointLights,
            RasterizationSettings,
            TexturesVertex,
        )
        from pytorch3d.structures import Meshes
        from utils.projection_utils import get_torch3d_cam

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.faces = torch.as_tensor(faces.astype(np.int64), device=self.device)
        self.raster_settings = RasterizationSettings(
            image_size=(height, width), blur_radius=0.0, faces_per_pixel=1
        )
        self.MeshRasterizer = MeshRasterizer
        self.HardPhongShader = HardPhongShader
        self.PointLights = PointLights
        self.TexturesVertex = TexturesVertex
        self.Meshes = Meshes
        self.BlendParams = BlendParams
        self.get_torch3d_cam = get_torch3d_cam

    def render(self, vertices: np.ndarray, camera: np.ndarray, intrinsics: np.ndarray):
        verts = torch.as_tensor(vertices, dtype=torch.float32, device=self.device).unsqueeze(0)
        faces = self.faces.unsqueeze(0)
        colors = torch.tensor([0.0390625, 0.4140625, 0.796875], device=self.device)
        textures = self.TexturesVertex(verts_features=colors.view(1, 1, 3).expand_as(verts))
        meshes = self.Meshes(verts=verts, faces=faces, textures=textures)
        camera_t = torch.as_tensor(camera, dtype=torch.float32, device=self.device).unsqueeze(0)
        intrinsics_t = torch.as_tensor(intrinsics, dtype=torch.float32, device=self.device).unsqueeze(0)
        cameras = self.get_torch3d_cam(camera_t, intrinsics_t)
        rasterizer = self.MeshRasterizer(cameras=cameras, raster_settings=self.raster_settings)
        fragments = rasterizer(meshes)
        lights = self.PointLights(device=self.device, location=camera_t[:, :3, 3])
        shader = self.HardPhongShader(
            device=self.device,
            cameras=cameras,
            lights=lights,
            blend_params=self.BlendParams(background_color=(1.0, 1.0, 1.0)),
        )
        image = shader(fragments, meshes, cameras=cameras, lights=lights)[0, ..., :3]
        rgb = (image.clamp(0, 1) * 255).byte().cpu().numpy()
        mask = (fragments.pix_to_face[0, ..., 0] >= 0).byte().cpu().numpy()
        return rgb, mask

    def close(self) -> None:
        return None


@dataclass
class Series:
    label: str
    camera: np.ndarray
    intrinsics: np.ndarray
    joints: np.ndarray
    vertices: np.ndarray


def infer_image_size(intrinsics: np.ndarray) -> tuple[int, int, dict[str, float]]:
    intr = np.asarray(intrinsics, dtype=np.float64)
    if intr.ndim != 2 or intr.shape[1] != 4 or not np.isfinite(intr).all():
        raise ValueError(f"invalid intrinsics shape/content: {intr.shape}")
    if np.any(intr[:, :2] <= 0):
        raise ValueError("fx/fy must be positive")
    widths = 2.0 * intr[:, 2]
    heights = 2.0 * intr[:, 3]
    width = int(round(float(np.median(widths))))
    height = int(round(float(np.median(heights))))
    integer_error = max(float(np.max(np.abs(widths - np.rint(widths)))), float(np.max(np.abs(heights - np.rint(heights)))))
    frame_variation = max(float(np.ptp(widths)), float(np.ptp(heights)))
    if integer_error >= 0.5 or frame_variation > 1.0:
        raise ValueError(f"image size is not stable integer: integer_error={integer_error}, variation={frame_variation}")
    if width < 2 or height < 2 or width % 2 or height % 2:
        raise ValueError(f"libx264 requires positive even dimensions, got {width}x{height}")
    return width, height, {"integer_error_px": integer_error, "frame_variation_px": frame_variation}


def camera_rotation_gate(camera: np.ndarray) -> dict[str, float]:
    rotations = np.asarray(camera)[:, :3, :3].astype(np.float64)
    identity = np.eye(3)[None]
    orth = np.max(np.abs(np.swapaxes(rotations, 1, 2) @ rotations - identity))
    det_error = np.max(np.abs(np.linalg.det(rotations) - 1.0))
    if orth >= 1e-3 or det_error >= 1e-3:
        raise ValueError(f"camera rotation gate failed: orth={orth}, det_error={det_error}")
    return {"orthogonality_max_abs": float(orth), "determinant_max_abs_error": float(det_error)}


def project_manual(joints: np.ndarray, c2w: np.ndarray, intrinsics: np.ndarray) -> np.ndarray:
    # Compare like-for-like with PulpMotion, whose official implementation
    # projects float32 tensors. Generated SMPL outputs can otherwise arrive as
    # float16 from inference and introduce multi-pixel quantization error.
    joints = np.asarray(joints, dtype=np.float32)
    c2w = np.asarray(c2w, dtype=np.float32)
    intrinsics = np.asarray(intrinsics, dtype=np.float32)
    rotations = c2w[:, :3, :3]
    translations = c2w[:, :3, 3]
    w2c_r = np.swapaxes(rotations, 1, 2)
    w2c_t = -np.einsum("fij,fj->fi", w2c_r, translations)
    camera_joints = np.einsum("fij,fkj->fki", w2c_r, joints) + w2c_t[:, None]
    z = np.maximum(camera_joints[..., 2], np.finfo(np.float32).eps)
    x = intrinsics[:, None, 0] * camera_joints[..., 0] / z + intrinsics[:, None, 2]
    y = intrinsics[:, None, 1] * camera_joints[..., 1] / z + intrinsics[:, None, 3]
    return np.stack([x, y, camera_joints[..., 2]], axis=-1)


def projection_parity(
    official_project: Any, joints: np.ndarray, camera: np.ndarray, intrinsics: np.ndarray
) -> tuple[np.ndarray, dict[str, float]]:
    # Do not share NumPy storage here. The generation stack retains views into
    # decoded buffers; a parity gate must compare immutable snapshots.
    camera_t = torch.tensor(np.array(camera, dtype=np.float32, copy=True), device="cpu")
    intrinsics_t = torch.tensor(np.array(intrinsics, dtype=np.float32, copy=True), device="cpu")
    joints_t = torch.tensor(np.array(joints, dtype=np.float32, copy=True), device="cpu")
    camera_before = camera_t.clone()
    intrinsics_before = intrinsics_t.clone()
    joints_before = joints_t.clone()
    # The sampling path uses medium matmul precision for throughput. Projection
    # validation must use highest precision: PyTorch otherwise quantizes the
    # official 4x4 and independent 3x3 einsums differently by several pixels.
    previous_matmul_precision = torch.get_float32_matmul_precision()
    torch.set_float32_matmul_precision("highest")
    try:
        with torch.no_grad(), torch.autocast("cpu", enabled=False), torch.autocast("cuda", enabled=False):
            official_t = official_project(camera_t, intrinsics_t, joints_t)
            rotation = camera_t[:, :3, :3]
            translation = camera_t[:, :3, 3]
            w2c_rotation = rotation.mT
            w2c_translation = -(w2c_rotation @ translation[..., None]).squeeze(-1)
            camera_joints = torch.einsum("fij,fkj->fki", w2c_rotation, joints_t) + w2c_translation[:, None]
            z = camera_joints[..., 2].clamp_min(torch.finfo(torch.float32).eps)
            manual_t = torch.stack(
                (
                    intrinsics_t[:, None, 0] * camera_joints[..., 0] / z + intrinsics_t[:, None, 2],
                    intrinsics_t[:, None, 1] * camera_joints[..., 1] / z + intrinsics_t[:, None, 3],
                    camera_joints[..., 2],
                ),
                dim=-1,
            )
            official_repeat_t = official_project(camera_t, intrinsics_t, joints_t)
    finally:
        torch.set_float32_matmul_precision(previous_matmul_precision)
    if not torch.equal(camera_t, camera_before) or not torch.equal(intrinsics_t, intrinsics_before) or not torch.equal(joints_t, joints_before):
        raise RuntimeError("official projection mutated an input tensor")
    repeat_error = torch.linalg.vector_norm(official_t[..., :2] - official_repeat_t[..., :2], dim=-1).max()
    if float(repeat_error) >= 1e-5:
        raise RuntimeError(f"official projection is not deterministic: max pixel error {float(repeat_error)}")
    official = official_t.cpu().numpy()
    manual = manual_t.cpu().numpy()
    valid = np.isfinite(official[..., :2]).all(-1) & np.isfinite(manual[..., :2]).all(-1) & (manual[..., 2] > 0)
    if not valid.any():
        raise ValueError("no positive-depth joints for projection parity")
    errors = np.linalg.norm(official[..., :2] - manual[..., :2], axis=-1)[valid]
    numpy_manual = project_manual(joints, camera, intrinsics)
    numpy_errors = np.linalg.norm(official[..., :2] - numpy_manual[..., :2], axis=-1)[valid]
    result = {
        "mean_pixel_error": float(errors.mean()),
        "max_pixel_error": float(errors.max()),
        "numpy_diagnostic_mean_pixel_error": float(numpy_errors.mean()),
        "numpy_diagnostic_max_pixel_error": float(numpy_errors.max()),
    }
    if result["mean_pixel_error"] >= 0.1 or result["max_pixel_error"] >= 0.5:
        official_invert = official_project.__globals__["invert_cam"]
        with torch.no_grad(), torch.autocast("cpu", enabled=False), torch.autocast("cuda", enabled=False):
            official_w2c = official_invert(camera_t)
            manual_w2c = torch.eye(4, dtype=torch.float32).repeat(len(camera_t), 1, 1)
            manual_w2c[:, :3, :3] = camera_t[:, :3, :3].mT
            manual_w2c[:, :3, 3] = -(camera_t[:, :3, :3].mT @ camera_t[:, :3, 3, None]).squeeze(-1)
            hom = torch.cat([joints_t, torch.ones(*joints_t.shape[:-1], 1)], dim=-1)
            recomputed_camera = torch.einsum("fij,fkj->fki", official_w2c, hom)[..., :3]
            recomputed_z = recomputed_camera[..., 2].clamp_min(torch.finfo(torch.float32).eps)
            recomputed = torch.stack(
                [
                    intrinsics_t[:, None, 0] * recomputed_camera[..., 0] / recomputed_z + intrinsics_t[:, None, 2],
                    intrinsics_t[:, None, 1] * recomputed_camera[..., 1] / recomputed_z + intrinsics_t[:, None, 3],
                    recomputed_camera[..., 2],
                ],
                dim=-1,
            )
        recomputed_error = torch.linalg.vector_norm(official_t[..., :2] - recomputed[..., :2], dim=-1)[torch.from_numpy(valid)]
        result.update(
            {
                "official_vs_manual_w2c_max_abs": float((official_w2c - manual_w2c).abs().max()),
                "official_vs_recomputed_mean_pixel_error": float(recomputed_error.mean()),
                "official_vs_recomputed_max_pixel_error": float(recomputed_error.max()),
                "camera_last_row_max_abs_error": float((camera_t[:, 3] - torch.tensor([0.0, 0.0, 0.0, 1.0])).abs().max()),
                "torch_autocast_enabled": bool(torch.is_autocast_enabled()),
                "torch_cpu_autocast_enabled": bool(torch.is_autocast_enabled("cpu")),
            }
        )
        np.savez(
            "/tmp/storymotion_projection_parity_failure.npz",
            camera=camera_t.numpy(), intrinsics=intrinsics_t.numpy(), joints=joints_t.numpy(),
            official=official, manual=manual,
        )
        raise ValueError(f"official/manual projection mismatch: {result}")
    return official, result


def visibility_mask(projection: np.ndarray, width: int, height: int) -> np.ndarray:
    return (
        np.isfinite(projection).all(-1)
        & (projection[..., 2] > 0)
        & (projection[..., 0] >= 0)
        & (projection[..., 0] < width)
        & (projection[..., 1] >= 0)
        & (projection[..., 1] < height)
    )


def projection_stats(
    projection: np.ndarray, width: int, height: int, gt_visibility: np.ndarray
) -> dict[str, float | int]:
    finite = np.isfinite(projection).all(-1)
    positive = finite & (projection[..., 2] > 0)
    visible = visibility_mask(projection, width, height)
    has_any = visible.any(-1)
    has_all = visible.all(-1)
    centers: list[np.ndarray] = []
    scales: list[float] = []
    for frame, valid in zip(projection, positive):
        if not valid.any():
            centers.append(np.array([np.nan, np.nan]))
            scales.append(np.nan)
            continue
        xy = frame[valid, :2]
        low, high = xy.min(0), xy.max(0)
        centers.append(((low + high) * 0.5) / np.array([width, height]))
        scales.append(float(np.max((high - low) / np.array([width, height]))))
    center = np.asarray(centers)
    scale = np.asarray(scales)
    center_valid = np.isfinite(center).all(-1)
    scale_valid = np.isfinite(scale)
    center_delta = np.diff(center[center_valid], axis=0) if center_valid.sum() > 1 else np.zeros((0, 2))
    scale_delta = np.diff(scale[scale_valid]) if scale_valid.sum() > 1 else np.zeros(0)
    if gt_visibility.shape != visible.shape:
        raise ValueError(f"GT visibility shape mismatch: {gt_visibility.shape} vs {visible.shape}")
    result: dict[str, float | int] = {
        "frames": int(projection.shape[0]),
        "positive_depth_joint_ratio": float(positive.mean()),
        "in_frame_joint_ratio": float(visible.mean()),
        "fully_in_frame_ratio": float(has_all.mean()),
        "missing_frame_ratio": float((~has_any).mean()),
        "partial_out_frame_ratio": float((has_any & ~has_all).mean()),
        "nonfinite_joint_ratio": float((~finite).mean()),
        "visibility_xor_vs_gt": float(np.logical_xor(visible, gt_visibility).mean()),
        "bbox_center_x_std_normalized": float(np.nanstd(center[:, 0])) if center_valid.any() else 0.0,
        "bbox_center_y_std_normalized": float(np.nanstd(center[:, 1])) if center_valid.any() else 0.0,
        "bbox_scale_mean_normalized": float(np.nanmean(scale)) if scale_valid.any() else 0.0,
        "bbox_scale_std_normalized": float(np.nanstd(scale)) if scale_valid.any() else 0.0,
        "bbox_center_jitter_mean_normalized": float(np.linalg.norm(center_delta, axis=-1).mean()) if center_delta.size else 0.0,
        "bbox_scale_jitter_mean_normalized": float(np.abs(scale_delta).mean()) if scale_delta.size else 0.0,
    }
    if result["nonfinite_joint_ratio"] != 0.0:
        raise ValueError(f"non-finite projection: {result['nonfinite_joint_ratio']}")
    return result


def draw_skeleton(
    canvas: np.ndarray,
    projection: np.ndarray,
    label: str,
    line_color: tuple[int, int, int] = (30, 90, 220),
    joint_color: tuple[int, int, int] = (225, 45, 45),
) -> np.ndarray:
    image = Image.fromarray(canvas)
    draw = ImageDraw.Draw(image)
    valid = np.isfinite(projection).all(-1) & (projection[:, 2] > 0)
    points = np.zeros((len(projection), 2), dtype=np.int32)
    safe_xy = np.clip(projection[valid, :2], -1_000_000.0, 1_000_000.0)
    points[valid] = np.rint(safe_xy).astype(np.int32, copy=False)
    for parent, child in BONES:
        if valid[parent] and valid[child]:
            draw.line([tuple(points[parent]), tuple(points[child])], fill=line_color, width=2)
    for point, is_valid in zip(points, valid):
        if is_valid:
            x, y = [int(value) for value in point]
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=joint_color)
    draw.rectangle((0, 0, min(canvas.shape[1], 420), 22), fill=(255, 255, 255))
    draw.text((6, 5), label, fill=(20, 20, 20))
    return np.asarray(image)


def stage_file(src: Path, dst: Path, guard: DiskGuard, video_probe: str | None = None) -> None:
    guard.check(f"before-copy:{dst.name}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    partial = dst.with_name(dst.name + ".partial")
    shutil.copyfile(src, partial)
    os.replace(partial, dst)
    guard.check(f"after-copy:{dst.name}")
    if video_probe:
        subprocess.run(
            [video_probe, "-v", "error", "-i", str(dst), "-f", "null", "-"],
            check=True,
            capture_output=True,
            text=True,
        )


def render_series(
    series: Series,
    projection: np.ndarray,
    faces: np.ndarray,
    out_dir: Path,
    scratch_dir: Path,
    fps: int,
    ffmpeg: str,
    ffprobe: str,
    guard: DiskGuard,
) -> dict[str, Any]:
    width, height, size_gate = infer_image_size(series.intrinsics)
    renderer = CameraViewRenderer(width, height, faces)
    scratch_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "skeleton": scratch_dir / f"{series.label}_camera_projection_skeleton.mp4",
        "mesh": scratch_dir / f"{series.label}_camera_view_mesh.mp4",
        "overlay": scratch_dir / f"{series.label}_camera_view_mesh_skeleton_overlay.mp4",
    }
    writers = {key: RawVideoWriter(ffmpeg, path, width, height, fps) for key, path in paths.items()}
    containment_hits = 0
    containment_total = 0
    nonempty_frames = 0
    visible_without_mesh_frames = 0
    screenshot_ids = sorted({0, len(projection) // 2, len(projection) - 1})
    screenshots: list[Path] = []
    try:
        for frame_idx in range(len(projection)):
            if frame_idx % 25 == 0:
                guard.check(f"render:{series.label}:{frame_idx}")
            mesh_rgb, mesh_mask = renderer.render(
                series.vertices[frame_idx], series.camera[frame_idx], series.intrinsics[frame_idx]
            )
            if np.any(mesh_mask):
                nonempty_frames += 1
            blank = np.full((height, width, 3), 255, dtype=np.uint8)
            skeleton = draw_skeleton(blank, projection[frame_idx], series.label)
            overlay = draw_skeleton(
                mesh_rgb,
                projection[frame_idx],
                series.label,
                line_color=(255, 220, 30),
                joint_color=(255, 70, 60),
            )
            writers["skeleton"].write(skeleton)
            writers["mesh"].write(mesh_rgb)
            writers["overlay"].write(overlay)
            visible = visibility_mask(projection[frame_idx:frame_idx + 1], width, height)[0]
            if visible.any() and not np.any(mesh_mask):
                visible_without_mesh_frames += 1
            xy = np.floor(projection[frame_idx, :, :2]).astype(np.int64)
            for joint_idx in np.flatnonzero(visible):
                x, y = xy[joint_idx]
                containment_total += 1
                containment_hits += int(mesh_mask[y, x] > 0)
            if frame_idx in screenshot_ids:
                shot = scratch_dir / f"{series.label}_frame_{frame_idx:04d}.png"
                Image.fromarray(overlay).save(shot)
                screenshots.append(shot)
    finally:
        renderer.close()
        for writer in writers.values():
            writer.close()
    if visible_without_mesh_frames:
        raise RuntimeError(
            f"{series.label}: projected joints are visible but mesh is absent in {visible_without_mesh_frames} frames"
        )
    containment = containment_hits / containment_total if containment_total else None
    if containment is not None and containment < 0.80:
        raise RuntimeError(f"{series.label}: only {containment:.1%} visible joints land inside mesh silhouette")
    final_videos: dict[str, str] = {}
    for key, src in paths.items():
        dst = out_dir / src.name
        stage_file(src, dst, guard, ffprobe)
        final_videos[key] = str(dst)
    final_shots: list[str] = []
    for src in screenshots:
        dst = out_dir / "screenshots" / src.name
        stage_file(src, dst, guard)
        final_shots.append(str(dst))
    shutil.rmtree(scratch_dir)
    return {
        "videos": final_videos,
        "screenshots": final_shots,
        "image_size": [width, height],
        "image_size_gate": size_gate,
        "mesh_nonempty_frame_ratio": nonempty_frames / len(projection),
        "visible_joint_without_mesh_frame_ratio": visible_without_mesh_frames / len(projection),
        "projected_joint_inside_mesh_ratio": containment,
        "projected_joint_inside_mesh_count": containment_hits,
        "projected_joint_checked_count": containment_total,
    }


def numpy_human(raw_human: Any, index: int, frames: int) -> tuple[np.ndarray, np.ndarray]:
    joints = raw_human.joints[index, :frames, :22, :3].detach().float().cpu().numpy()
    vertices = raw_human.vertices[index, :frames].detach().float().cpu().numpy()
    return joints, vertices


def extract_pulp_series(outputs: dict[str, Any], index: int, frames: int, label: str) -> Series:
    raw = outputs["raw_output"]
    joints, vertices = numpy_human(raw["human"], index, frames)
    return Series(
        label=label,
        camera=raw["camera"][index, :frames].detach().float().cpu().numpy(),
        intrinsics=raw["intrinsics"][index, :frames].detach().float().cpu().numpy(),
        joints=joints,
        vertices=vertices,
    )


def write_json_atomic(path: Path, value: Any, guard: DiskGuard) -> None:
    scratch = path.parent / (path.name + ".partial")
    scratch.parent.mkdir(parents=True, exist_ok=True)
    scratch.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(scratch, path)
    guard.check(f"json:{path.name}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--scratch-dir", type=Path, default=Path("/tmp/storymotion_camera_projection_gate"))
    p.add_argument("--story-ckpt", type=Path, default=ROOT / "runs/train/stage2/independent_dropout_ft_20260614/gpu0_indepdrop_b512_50000/last.pt")
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
    p.add_argument("--pulp-batch-size", type=int, default=2)
    p.add_argument("--story-num-steps", type=int, default=50)
    p.add_argument("--cfg-human", type=float, default=2.0)
    p.add_argument("--cfg-camera", type=float, default=2.0)
    p.add_argument("--eta", type=float, default=0.0)
    p.add_argument("--channel-gated-cfg", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--num-samples", type=int, default=12)
    p.add_argument("--start-index", type=int, default=0)
    p.add_argument("--sample-ids", nargs="*")
    p.add_argument("--max-sample-groups", type=int, default=15)
    p.add_argument("--fps", type=int, default=12)
    p.add_argument("--seed", type=int, default=20260620)
    p.add_argument("--device", default="cuda:0")
    p.add_argument("--ffmpeg", default=rbr.FFMPEG)
    p.add_argument("--ffprobe", default=rbr.FFMPEG, help="Video decoder used for post-copy integrity checks.")
    p.add_argument("--disk-mount", type=Path, default=Path("/data"))
    p.add_argument("--disk-errors-count", type=Path, default=Path("/sys/fs/ext4/sdh1/errors_count"))
    p.add_argument("--max-disk-used", type=float, default=0.90)
    return p


def main() -> None:
    args = build_parser().parse_args()
    if not args.out_dir.resolve().is_relative_to(Path("/data")):
        raise ValueError(f"output must be on /data, got {args.out_dir}")
    fair.patch_numpy_aliases()
    fair.add_pulp_paths(args.pulp_root)
    from utils.projection_utils import project_joints as official_project_joints

    expected_projection_source = (args.pulp_root / "utils/projection_utils.py").resolve()
    actual_projection_source = Path(official_project_joints.__code__.co_filename).resolve()
    if actual_projection_source != expected_projection_source:
        raise RuntimeError(f"wrong projection module: {actual_projection_source} != {expected_projection_source}")

    series_count = 1 + len(args.pulp_cfg_z) + 3
    if series_count >= 16:
        raise ValueError(f"render series must be <16, got {series_count}")
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.set_float32_matmul_precision("medium")
    device = torch.device(args.device)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.scratch_dir.mkdir(parents=True, exist_ok=True)
    guard = DiskGuard(args.disk_mount, args.disk_errors_count, args.out_dir / "STOP_DISK_ERROR", args.max_disk_used)
    guard.check("startup")

    print("Loading Pulp dataset/autoencoder/cache...", flush=True)
    _, dataset, autoencoder = rbr.build_pulp(args, device)
    cache = rbr.mod.PulpLatentCache(args.cache_dir / "val.pt")
    cache_index = {str(cache[i]["sample_id"]): i for i in range(len(cache))}
    if args.sample_ids:
        sample_ids = [str(value) for value in args.sample_ids]
    else:
        end = min(args.start_index + args.num_samples, len(cache))
        sample_ids = [str(cache[i]["sample_id"]) for i in range(args.start_index, end)]
    if not sample_ids:
        raise ValueError("no samples selected")
    if len(sample_ids) > args.max_sample_groups or len(sample_ids) >= 16:
        raise ValueError(f"sample groups must be <16 and <= {args.max_sample_groups}, got {len(sample_ids)}")
    missing = [sample_id for sample_id in sample_ids if sample_id not in cache_index]
    if missing:
        raise KeyError(f"sample ids missing from cache: {missing}")

    valid_frames = {
        sample_id: int(dataset.get_sample(sample_id)["padding_mask"].long().sum().item())
        for sample_id in sample_ids
    }
    pulp_by_sample: dict[str, dict[str, Series]] = {sample_id: {} for sample_id in sample_ids}
    for cfg_z in args.pulp_cfg_z:
        label = f"pulpmotion_wz{cfg_z:g}_wc{args.pulp_cfg_c:g}".replace(".", "p")
        print(f"Generating {label}...", flush=True)
        pulp_model, _ = fair.build_pulpmotion_model(args, device, cfg_z)
        for start in range(0, len(sample_ids), args.pulp_batch_size):
            chunk = sample_ids[start:start + args.pulp_batch_size]
            outputs, _ = fair.run_pulpmotion(
                pulp_model, dataset, chunk, device, args.seed + int(cfg_z * 1000) + 42 + start
            )
            for index, sample_id in enumerate(chunk):
                pulp_by_sample[sample_id][label] = extract_pulp_series(outputs, index, valid_frames[sample_id], label)
            del outputs
            guard.check(f"pulp:{label}:{start}")
        del pulp_model
        if device.type == "cuda":
            torch.cuda.empty_cache()

    print("Loading StoryMotion model...", flush=True)
    story_model, story_diffusion, story_ckpt = rbr.load_model(args.story_ckpt, device)
    faces = np.asarray(np.load(args.pulp_root / "utils/smpl.faces"), dtype=np.int32)
    records: list[dict[str, Any]] = []
    started = time.time()
    for sample_ord, sample_id in enumerate(sample_ids):
        print(f"[{sample_ord + 1}/{len(sample_ids)}] {sample_id}", flush=True)
        guard.check(f"sample-start:{sample_id}")
        n = valid_frames[sample_id]
        sample = dataset.get_sample(sample_id)
        gt_c2w, gt_intrinsics, _ = rbr.get_gt_tensors(sample, device)
        human_dataset = dataset.joint_dataset.human_dataset
        raw_human_feat = sample["x_raw"]["human_feat"].to(device)
        normalized_human_feat = human_dataset.normalize(raw_human_feat)
        roundtrip_human_feat = human_dataset.unnormalize(normalized_human_feat, "feat")
        feature_roundtrip_max_abs = float((roundtrip_human_feat - raw_human_feat).abs().max())
        if feature_roundtrip_max_abs >= 1e-5:
            raise RuntimeError(f"GT human feature roundtrip failed: {feature_roundtrip_max_abs}")
        gt_human_feat = normalized_human_feat.unsqueeze(0)
        with torch.no_grad():
            gt_body = human_dataset.get_raw(gt_human_feat)
        gt_joints = gt_body.joints[0, :n, :22].detach().float().cpu().numpy()
        gt_vertices = gt_body.vertices[0, :n].detach().float().cpu().numpy()
        if not np.isfinite(gt_joints).all() or not np.isfinite(gt_vertices).all():
            raise RuntimeError("GT SMPL reconstruction contains NaN/Inf")
        rifke_joints = sample["x_raw"]["human"]["joints"][:n, :22].detach().float().cpu().numpy()
        joint_definition_gap = np.linalg.norm(gt_joints - rifke_joints, axis=-1)
        gt_series = Series(
            "gt",
            gt_c2w[0, :n].detach().float().cpu().numpy(),
            gt_intrinsics[0, :n].detach().float().cpu().numpy(),
            gt_joints,
            gt_vertices,
        )

        item = cache[cache_index[sample_id]]
        z = item["z"].unsqueeze(0).to(device)
        text = item["text"].unsqueeze(0).to(device)
        valid = item["valid"].unsqueeze(0).to(device)
        story_series: dict[str, Series] = {}
        for task_id, task_name in rbr.mod.TASK_NAMES.items():
            completion = rbr.ddim_sample_bilateral(
                story_model, story_diffusion, z, text, valid, task_id,
                [args.seed + sample_ord * 1000 + task_id],
                args.seed + {"camera": 11, "human": 23, "joint": 37}[task_name],
                args.story_num_steps,
                cfg_human=args.cfg_human,
                cfg_camera=args.cfg_camera,
                eta=args.eta,
                channel_gated_cfg=args.channel_gated_cfg,
            )
            raw = rbr.decode_raw(autoencoder, dataset, completion, gt_intrinsics)
            pred_joints, pred_vertices = numpy_human(raw["human"], 0, n)
            if task_name == "camera":
                joints, vertices = gt_joints, gt_vertices
                camera = raw["camera"][0, :n].detach().float().cpu().numpy()
                intrinsics = raw["intrinsics"][0, :n].detach().float().cpu().numpy()
            elif task_name == "human":
                joints, vertices = pred_joints, pred_vertices
                camera = gt_series.camera
                intrinsics = gt_series.intrinsics
            else:
                joints, vertices = pred_joints, pred_vertices
                camera = raw["camera"][0, :n].detach().float().cpu().numpy()
                intrinsics = raw["intrinsics"][0, :n].detach().float().cpu().numpy()
            label = f"story_{task_name}"
            story_series[label] = Series(label, camera, intrinsics, joints, vertices)

        all_series: list[Series] = [gt_series, *pulp_by_sample[sample_id].values(), *story_series.values()]
        if len(all_series) != series_count:
            raise RuntimeError(f"expected {series_count} series, got {len(all_series)}")
        gt_projection, gt_parity = projection_parity(
            official_project_joints, gt_series.joints, gt_series.camera, gt_series.intrinsics
        )
        gt_width, gt_height, _ = infer_image_size(gt_series.intrinsics)
        gt_visibility = visibility_mask(gt_projection, gt_width, gt_height)
        sample_out = args.out_dir / sample_id
        sample_record: dict[str, Any] = {
            "sample_id": sample_id,
            "valid_frames": n,
            "gt_joint_source": "CharDataset.get_raw(CharDataset.normalize(x_raw.human_feat)).joints[:22]",
            "gt_mesh_source": "CharDataset.get_raw(CharDataset.normalize(x_raw.human_feat)).vertices",
            "gt_human_feature_roundtrip_max_abs": feature_roundtrip_max_abs,
            "rifke_vs_smpl_joint_definition_gap_m": {
                "mean": float(joint_definition_gap.mean()),
                "max": float(joint_definition_gap.max()),
                "gate": False,
                "reason": "diagnostic only: x_raw stores RIFKE 22-joint positions while get_raw returns SMPL body-model joints",
            },
            "series": {},
        }
        for series in all_series:
            print(f"  rendering {series.label}", flush=True)
            if not (len(series.camera) == len(series.intrinsics) == len(series.joints) == len(series.vertices) == n):
                raise ValueError(f"length mismatch for {series.label}")
            width, height, _ = infer_image_size(series.intrinsics)
            if (width, height) != (gt_width, gt_height):
                raise ValueError(f"{series.label}: image dimensions differ from GT")
            projection, parity = projection_parity(
                official_project_joints, series.joints, series.camera, series.intrinsics
            )
            stats = projection_stats(projection, width, height, gt_visibility)
            rendered = render_series(
                series, projection, faces, sample_out,
                args.scratch_dir / sample_id / series.label,
                args.fps, args.ffmpeg, args.ffprobe, guard,
            )
            sample_record["series"][series.label] = {
                "projection_parity_gate": parity,
                "camera_rotation_gate": camera_rotation_gate(series.camera),
                "projection_stats": stats,
                "render_gate": rendered,
            }
        sample_record["gt_projection_parity_gate"] = gt_parity
        sample_record["automatic_gate_pass"] = True
        write_json_atomic(sample_out / "summary.json", sample_record, guard)
        records.append(sample_record)

    manifest = {
        "mode": "camera_projection_human_skeleton_and_mesh_gate",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "sample_groups": len(sample_ids),
        "series_per_group": series_count,
        "sample_ids": sample_ids,
        "story_checkpoint": str(args.story_ckpt),
        "story_checkpoint_step": int(story_ckpt.get("step", -1)),
        "story_sampler": {
            "num_steps": args.story_num_steps,
            "cfg_human": args.cfg_human,
            "cfg_camera": args.cfg_camera,
            "eta": args.eta,
            "channel_gated_cfg": args.channel_gated_cfg,
        },
        "pulp_checkpoint": str(args.pulp_checkpoint),
        "pulp_sampler": {"num_steps": args.pulp_num_steps, "cfg_rate_c": args.pulp_cfg_c, "cfg_rate_z": args.pulp_cfg_z},
        "renderer": "PulpMotion get_torch3d_cam/project_meshes path adapted to shaded RGB with per-frame fx/fy/cx/cy; no fixed-view camera",
        "disk_guard": guard.check("manifest"),
        "elapsed_sec": time.time() - started,
        "automatic_gate_pass": True,
        "manual_visual_gate_pass": None,
        "samples": records,
    }
    write_json_atomic(args.out_dir / "manifest.json", manifest, guard)
    print(json.dumps({"ok": True, "samples": len(sample_ids), "series": series_count, "out_dir": str(args.out_dir)}), flush=True)


if __name__ == "__main__":
    main()
