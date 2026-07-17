from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import torch


HUMAN199_DIM = 199
HUMAN200_DIM = 200
HUMAN200_FEATURE_CONTRACT = "storymotion_v8_2_normalized_human200_absolute_root_yaw_joint_camera14"
HUMAN200_LAYOUT = "root_z1+root_xy_relative2+yaw_sin_cos2+pose6d132+local_joints63"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def integrated_yaw_from_human199(human199_raw: torch.Tensor) -> torch.Tensor:
    if human199_raw.ndim < 2 or human199_raw.shape[-1] != HUMAN199_DIM:
        raise ValueError(f"expected [...,T,{HUMAN199_DIM}], got {tuple(human199_raw.shape)}")
    return torch.cumsum(human199_raw[..., 3], dim=-1)


def _root_xy_from_human199(human199_raw: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
    velocity_local = human199_raw[..., 1:3]
    cosine = torch.cos(yaw)
    sine = torch.sin(yaw)
    velocity_world = torch.stack(
        (
            cosine * velocity_local[..., 0] - sine * velocity_local[..., 1],
            sine * velocity_local[..., 0] + cosine * velocity_local[..., 1],
        ),
        dim=-1,
    )
    integrated = torch.cumsum(velocity_world[..., :-1, :], dim=-2)
    root_xy = torch.cat((torch.zeros_like(velocity_world[..., :1, :]), integrated), dim=-2)
    return root_xy - root_xy[..., :1, :]


def human199_raw_to_human200_raw(human199_raw: torch.Tensor) -> torch.Tensor:
    """Replace integrative root channels with direct relative root/yaw channels."""
    if human199_raw.ndim < 2 or human199_raw.shape[-1] != HUMAN199_DIM:
        raise ValueError(f"expected [...,T,{HUMAN199_DIM}], got {tuple(human199_raw.shape)}")
    if human199_raw.shape[-2] <= 0:
        raise ValueError("human sequence must contain at least one frame")
    yaw = integrated_yaw_from_human199(human199_raw)
    root_xy = _root_xy_from_human199(human199_raw, yaw)
    human200 = torch.cat(
        (
            human199_raw[..., 0:1],
            root_xy,
            torch.sin(yaw)[..., None],
            torch.cos(yaw)[..., None],
            human199_raw[..., 4:136],
            human199_raw[..., 136:199],
        ),
        dim=-1,
    )
    if human200.shape[-1] != HUMAN200_DIM:
        raise AssertionError(f"bad human200 layout: {human200.shape[-1]}")
    return human200


def yaw_from_human200_raw(human200_raw: torch.Tensor, *, unwrap: bool = True) -> torch.Tensor:
    if human200_raw.ndim < 2 or human200_raw.shape[-1] != HUMAN200_DIM:
        raise ValueError(f"expected [...,T,{HUMAN200_DIM}], got {tuple(human200_raw.shape)}")
    yaw = torch.atan2(human200_raw[..., 3], human200_raw[..., 4])
    if not unwrap or yaw.shape[-1] <= 1:
        return yaw
    wrapped_delta = torch.atan2(torch.sin(yaw[..., 1:] - yaw[..., :-1]), torch.cos(yaw[..., 1:] - yaw[..., :-1]))
    return torch.cat((yaw[..., :1], yaw[..., :1] + torch.cumsum(wrapped_delta, dim=-1)), dim=-1)


def human200_raw_to_human199_raw(human200_raw: torch.Tensor) -> torch.Tensor:
    """Owning inverse for legacy Pulp geometry/render callbacks."""
    if human200_raw.ndim < 2 or human200_raw.shape[-1] != HUMAN200_DIM:
        raise ValueError(f"expected [...,T,{HUMAN200_DIM}], got {tuple(human200_raw.shape)}")
    if human200_raw.shape[-2] <= 0:
        raise ValueError("human sequence must contain at least one frame")
    yaw = yaw_from_human200_raw(human200_raw, unwrap=True)
    yaw_velocity = torch.cat((yaw[..., :1], yaw[..., 1:] - yaw[..., :-1]), dim=-1)
    root_xy = human200_raw[..., 1:3] - human200_raw[..., :1, 1:3]
    world_velocity = torch.cat(
        (root_xy[..., 1:, :] - root_xy[..., :-1, :], torch.zeros_like(root_xy[..., :1, :])),
        dim=-2,
    )
    cosine = torch.cos(yaw)
    sine = torch.sin(yaw)
    local_velocity = torch.stack(
        (
            cosine * world_velocity[..., 0] + sine * world_velocity[..., 1],
            -sine * world_velocity[..., 0] + cosine * world_velocity[..., 1],
        ),
        dim=-1,
    )
    human199 = torch.cat(
        (
            human200_raw[..., 0:1],
            local_velocity,
            yaw_velocity[..., None],
            human200_raw[..., 5:137],
            human200_raw[..., 137:200],
        ),
        dim=-1,
    )
    if human199.shape[-1] != HUMAN199_DIM:
        raise AssertionError(f"bad human199 inverse layout: {human199.shape[-1]}")
    return human199


def normalize_human200(human200_raw: torch.Tensor, stats: dict[str, Any]) -> torch.Tensor:
    mean = stats["mean"].to(device=human200_raw.device, dtype=human200_raw.dtype)
    std = stats["std"].to(device=human200_raw.device, dtype=human200_raw.dtype)
    return (human200_raw - mean) / std


def denormalize_human200(human200: torch.Tensor, stats: dict[str, Any]) -> torch.Tensor:
    mean = stats["mean"].to(device=human200.device, dtype=human200.dtype)
    std = stats["std"].to(device=human200.device, dtype=human200.dtype)
    return human200 * std + mean


def human199_raw_to_human200(human199_raw: torch.Tensor, stats: dict[str, Any]) -> torch.Tensor:
    return normalize_human200(human199_raw_to_human200_raw(human199_raw), stats)


def human200_to_human199_raw(human200: torch.Tensor, stats: dict[str, Any]) -> torch.Tensor:
    return human200_raw_to_human199_raw(denormalize_human200(human200, stats))


def official_human199_to_human200(
    human199: torch.Tensor,
    official_mean: torch.Tensor,
    official_std: torch.Tensor,
    human200_stats: dict[str, Any],
) -> torch.Tensor:
    mean = official_mean.to(device=human199.device, dtype=human199.dtype)
    std = official_std.to(device=human199.device, dtype=human199.dtype)
    return human199_raw_to_human200(human199 * std + mean, human200_stats)


def human200_to_official_human199(
    human200: torch.Tensor,
    human200_stats: dict[str, Any],
    official_mean: torch.Tensor,
    official_std: torch.Tensor,
) -> torch.Tensor:
    human199_raw = human200_to_human199_raw(human200, human200_stats)
    mean = official_mean.to(device=human199_raw.device, dtype=human199_raw.dtype)
    std = official_std.to(device=human199_raw.device, dtype=human199_raw.dtype)
    return (human199_raw - mean) / std


def load_human200_stats(
    path: str | Path,
    *,
    expected_train_manifest: str | Path | None = None,
) -> dict[str, Any]:
    path = Path(path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("human200 stats schema_version must be 1")
    if payload.get("feature_contract") != HUMAN200_FEATURE_CONTRACT:
        raise ValueError("human200 stats feature contract mismatch")
    if payload.get("layout") != HUMAN200_LAYOUT or payload.get("human_dim") != HUMAN200_DIM:
        raise ValueError("human200 stats layout/dimension mismatch")
    if payload.get("normalization") != "frame_weighted_population_mean_std":
        raise ValueError("human200 statistics must use frame-weighted population moments")
    source = payload.get("source")
    if not isinstance(source, dict) or source.get("split") != "train":
        raise ValueError("human200 statistics must declare a train-only source")
    if source.get("ordered_rows") is not True:
        raise ValueError("human200 statistics must preserve ordered train-manifest rows")
    for key in ("manifest_sha256", "sample_ids_sha256"):
        if not isinstance(source.get(key), str) or not SHA256_RE.fullmatch(source[key]):
            raise ValueError(f"human200 stats source.{key} must be a lowercase SHA256")
    if int(source.get("samples", 0)) <= 0 or int(source.get("frames", 0)) <= 0:
        raise ValueError("human200 stats source sample/frame counts must be positive")
    if expected_train_manifest is not None:
        expected_path = Path(expected_train_manifest)
        if sha256_file(expected_path) != source["manifest_sha256"]:
            raise ValueError("human200 stats were not built from the requested train manifest")
    mean = torch.tensor(payload.get("mean", []), dtype=torch.float32)
    std = torch.tensor(payload.get("std", []), dtype=torch.float32)
    if mean.shape != (HUMAN200_DIM,) or std.shape != (HUMAN200_DIM,):
        raise ValueError("human200 stats mean/std must each contain 200 values")
    if not torch.isfinite(mean).all() or not torch.isfinite(std).all() or not bool((std > 0).all()):
        raise ValueError("human200 stats must be finite with strictly positive std")
    if not math.isfinite(float(payload.get("min_std", 0.0))) or float(payload["min_std"]) <= 0.0:
        raise ValueError("human200 stats min_std must be finite and positive")
    builder = payload.get("builder")
    if (
        not isinstance(builder, dict)
        or not isinstance(builder.get("script_sha256"), str)
        or not SHA256_RE.fullmatch(builder["script_sha256"])
        or not isinstance(builder.get("argv"), list)
        or not builder["argv"]
    ):
        raise ValueError("human200 statistics must record builder script SHA256 and argv")
    return {
        "mean": mean,
        "std": std,
        "meta": payload,
        "path": path.resolve(),
        "sha256": sha256_file(path),
    }
