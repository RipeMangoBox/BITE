from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import Dataset

from .camera_data import CAMERA_FEATURE_DIM, CAMERA_FEATURE_SPACE, camera_poses_to_features, read_kitti_camera_poses
from .human200 import (
    HUMAN200_DIM,
    HUMAN200_FEATURE_CONTRACT,
    human199_raw_to_human200,
    load_human200_stats,
)


HUMAN_FEATURE_SPACE = "pulpmotion_smpl_rifke"
HUMAN_FEATURE_DIM = 199
LEGACY_FEATURE_CONTRACT = "legacy_raw_human199_absolute_camera9"
OFFICIAL_FEATURE_CONTRACT = "pulpmotion_official_normalized_human199_joint_camera14"
RAW_OFFICIAL_FEATURE_CONTRACT = "pulpmotion_raw_human199_joint_camera14"
RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT = "pulpmotion_raw_human199_normalized_joint_camera14"
OFFICIAL_CAMERA_FEATURE_DIM = 14


class RandomHumanCameraDataset(Dataset[dict[str, Any]]):
    """Deterministic paired data for closed-loop tokenizer smoke tests only."""

    def __init__(self, num_samples: int, seq_len: int, human_dim: int, camera_dim: int, seed: int = 0) -> None:
        gen = torch.Generator().manual_seed(seed)
        time = torch.linspace(0, 1, steps=seq_len).view(1, seq_len, 1)
        human_base = torch.randn(num_samples, 1, human_dim, generator=gen)
        camera_base = torch.randn(num_samples, 1, camera_dim, generator=gen)
        human_velocity = torch.randn(num_samples, 1, human_dim, generator=gen) * 0.1
        camera_velocity = torch.randn(num_samples, 1, camera_dim, generator=gen) * 0.1
        self.human = human_base + human_velocity * time + torch.randn(num_samples, seq_len, human_dim, generator=gen) * 0.02
        self.camera = camera_base + camera_velocity * time + torch.randn(num_samples, seq_len, camera_dim, generator=gen) * 0.02

    def __len__(self) -> int:
        return int(self.human.shape[0])

    def __getitem__(self, index: int) -> dict[str, Any]:
        return {"human": self.human[index].float(), "camera": self.camera[index].float(), "sample_id": f"synthetic_joint_{index:05d}"}


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _resolve(path: str | Path, root: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else root / value


def _load_feature_tensor(path: Path) -> torch.Tensor:
    if path.suffix == ".pt":
        value = torch.load(path, map_location="cpu")
    elif path.suffix == ".npy":
        import numpy as np

        value = torch.from_numpy(np.load(path))
    else:
        raise ValueError(f"unsupported feature format: {path}")
    if isinstance(value, dict):
        if "motion" in value:
            value = value["motion"]
        elif "features" in value:
            value = value["features"]
        else:
            raise KeyError(f"feature dict must contain 'motion' or 'features': {path}")
    tensor = torch.as_tensor(value, dtype=torch.float32)
    if tensor.ndim != 2:
        raise ValueError(f"expected feature tensor [T,D], got {tuple(tensor.shape)} from {path}")
    return tensor


def _load_official_stats(pulp_root: Path) -> dict[str, torch.Tensor]:
    import yaml

    modality_dir = pulp_root / "configs/dataset/modality"
    human = yaml.safe_load((modality_dir / "char_smplrifke.yaml").read_text(encoding="utf-8"))
    camera = yaml.safe_load((modality_dir / "traj_raw.yaml").read_text(encoding="utf-8"))
    joint = yaml.safe_load((modality_dir / "traj+char+proj.yaml").read_text(encoding="utf-8"))
    return {
        "human_mean": torch.tensor(human["feat_mean"], dtype=torch.float32),
        "human_std": torch.tensor(human["feat_std"], dtype=torch.float32),
        "velocity_mean": torch.tensor(camera["velocity_mean"], dtype=torch.float32),
        "velocity_std": torch.tensor(camera["velocity_std"], dtype=torch.float32),
        "distance_mean": torch.tensor(joint["distance_mean"], dtype=torch.float32),
        "distance_std": torch.tensor(joint["distance_std"], dtype=torch.float32),
    }


def _rifke_root_translation(human_raw: torch.Tensor) -> torch.Tensor:
    """Exact root joint reconstruction used by PulpMotion's RIFKE decoder."""
    root_z = human_raw[:, 0]
    velocity_local = human_raw[:, 1:3]
    angles = torch.cumsum(human_raw[:, 3], dim=0)
    cos, sin = torch.cos(angles), torch.sin(angles)
    velocity = torch.stack(
        [cos * velocity_local[:, 0] - sin * velocity_local[:, 1], sin * velocity_local[:, 0] + cos * velocity_local[:, 1]],
        dim=-1,
    )
    root_xy = torch.cat([torch.zeros_like(velocity[:1]), torch.cumsum(velocity[:-1], dim=0)], dim=0)
    return torch.cat([root_xy, root_z[:, None]], dim=-1)


def _official_camera_features(
    poses: torch.Tensor,
    intrinsics: torch.Tensor,
    human_root: torch.Tensor,
    stats: dict[str, torch.Tensor],
) -> torch.Tensor:
    fov_h = 2 * torch.atan(intrinsics[:, 3] / intrinsics[:, 1])
    fov_w = 2 * torch.atan(intrinsics[:, 2] / intrinsics[:, 0])
    fov = torch.stack([fov_h, fov_w], dim=-1).nan_to_num(0.0)
    distance = (poses[:, :3, 3] - human_root - stats["distance_mean"]) / stats["distance_std"]
    rotation = poses[:, :3, :3]
    rot6d = rotation[:, :, :2].permute(0, 2, 1).reshape(-1, 6)
    velocity = torch.diff(poses[:, :3, 3], dim=0)
    velocity = (velocity - stats["velocity_mean"]) / stats["velocity_std"]
    velocity = torch.cat([torch.zeros((1, 3), dtype=poses.dtype), velocity], dim=0)
    return torch.cat([fov, distance, rot6d, velocity], dim=-1)


def _raw_official_camera_features(
    poses: torch.Tensor,
    intrinsics: torch.Tensor,
    human_root: torch.Tensor,
) -> torch.Tensor:
    """Build the same 14D Pulp joint camera semantics without feature scaling."""
    fov_h = 2 * torch.atan(intrinsics[:, 3] / intrinsics[:, 1])
    fov_w = 2 * torch.atan(intrinsics[:, 2] / intrinsics[:, 0])
    fov = torch.stack([fov_h, fov_w], dim=-1).nan_to_num(0.0)
    distance = poses[:, :3, 3] - human_root
    rotation = poses[:, :3, :3]
    rot6d = rotation[:, :, :2].permute(0, 2, 1).reshape(-1, 6)
    velocity = torch.diff(poses[:, :3, 3], dim=0)
    velocity = torch.cat([torch.zeros((1, 3), dtype=poses.dtype), velocity], dim=0)
    return torch.cat([fov, distance, rot6d, velocity], dim=-1)


def official_raw_to_normalized(
    human: torch.Tensor,
    camera: torch.Tensor,
    stats: dict[str, torch.Tensor],
) -> tuple[torch.Tensor, torch.Tensor]:
    """Convert raw 199+14 features back to the official normalized contract."""
    human_mean = stats["human_mean"].to(device=human.device, dtype=human.dtype)
    human_std = stats["human_std"].to(device=human.device, dtype=human.dtype)
    distance_mean = stats["distance_mean"].to(device=camera.device, dtype=camera.dtype)
    distance_std = stats["distance_std"].to(device=camera.device, dtype=camera.dtype)
    velocity_mean = stats["velocity_mean"].to(device=camera.device, dtype=camera.dtype)
    velocity_std = stats["velocity_std"].to(device=camera.device, dtype=camera.dtype)
    human_normalized = (human - human_mean) / human_std
    camera_normalized = torch.cat(
        [
            camera[..., :2],
            (camera[..., 2:5] - distance_mean) / distance_std,
            camera[..., 5:11],
            (camera[..., 11:14] - velocity_mean) / velocity_std,
        ],
        dim=-1,
    )
    # The official feature builder defines the first velocity frame as zero
    # after normalization, rather than as -mean/std.
    if camera_normalized.ndim == 2:
        camera_normalized[0, 11:14] = 0.0
    else:
        camera_normalized[..., 0, 11:14] = 0.0
    return human_normalized, camera_normalized


class PairedPulpMotionHumanCameraDataset(Dataset[dict[str, Any]]):
    """Pairs PulpMotion RIFKE human features with camera trajectory features by sample_id."""

    def __init__(
        self,
        human_manifest_path: str | Path,
        camera_manifest_path: str | Path,
        human_root: str | Path | None = None,
        camera_root: str | Path | None = None,
        required_human_feature_space: str | None = HUMAN_FEATURE_SPACE,
        required_camera_feature_space: str | None = CAMERA_FEATURE_SPACE,
        drop_camera_z: bool = False,
        feature_contract: str = LEGACY_FEATURE_CONTRACT,
        pulp_root: str | Path | None = None,
        human200_stats_path: str | Path | None = None,
        human200_expected_train_manifest: str | Path | None = None,
    ) -> None:
        self.human_manifest_path = Path(human_manifest_path)
        self.camera_manifest_path = Path(camera_manifest_path)
        self.human_root = Path(human_root) if human_root is not None else self.human_manifest_path.parent
        self.camera_root = Path(camera_root) if camera_root is not None else self.camera_manifest_path.parent
        self.required_human_feature_space = required_human_feature_space
        self.required_camera_feature_space = required_camera_feature_space
        self.drop_camera_z = bool(drop_camera_z)
        self.feature_contract = str(feature_contract)
        if self.feature_contract not in {
            LEGACY_FEATURE_CONTRACT,
            OFFICIAL_FEATURE_CONTRACT,
            RAW_OFFICIAL_FEATURE_CONTRACT,
            RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
            HUMAN200_FEATURE_CONTRACT,
        }:
            raise ValueError(f"unsupported feature contract: {self.feature_contract}")
        if self.feature_contract in {
            OFFICIAL_FEATURE_CONTRACT,
            RAW_OFFICIAL_FEATURE_CONTRACT,
            RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
            HUMAN200_FEATURE_CONTRACT,
        }:
            if self.drop_camera_z:
                raise ValueError("drop_camera_z is incompatible with the official 14D camera contract")
            if pulp_root is None:
                raise ValueError("pulp_root is required for the official feature contract")
            self.official_stats = _load_official_stats(Path(pulp_root))
        if self.feature_contract == HUMAN200_FEATURE_CONTRACT:
            if human200_stats_path is None:
                raise ValueError("human200_stats_path is required for the v8.2 feature contract")
            if human200_expected_train_manifest is None:
                raise ValueError("v8.2 requires the train manifest used to build human200 statistics")
            self.human200_stats = load_human200_stats(
                human200_stats_path,
                expected_train_manifest=human200_expected_train_manifest,
            )
        camera_by_id: dict[str, dict[str, Any]] = {}
        for row in _read_jsonl(self.camera_manifest_path):
            sample_id = str(row.get("sample_id") or "")
            if sample_id and sample_id not in camera_by_id:
                camera_by_id[sample_id] = row
        self.records: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for human_row in _read_jsonl(self.human_manifest_path):
            sample_id = str(human_row.get("sample_id") or "")
            camera_row = camera_by_id.get(sample_id)
            if camera_row is not None:
                self.records.append((human_row, camera_row))
        if not self.records:
            raise ValueError(f"no paired sample_id records between {self.human_manifest_path} and {self.camera_manifest_path}")

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> dict[str, Any]:
        human_row, camera_row = self.records[index]
        sample_id = str(human_row.get("sample_id") or camera_row.get("sample_id") or index)
        human_feature_space = human_row.get("feature_space")
        camera_feature_space = camera_row.get("feature_space")
        if self.required_human_feature_space is not None and human_feature_space != self.required_human_feature_space:
            raise ValueError(f"human feature_space={human_feature_space!r} does not match {self.required_human_feature_space!r}")
        if self.required_camera_feature_space is not None and camera_feature_space != self.required_camera_feature_space:
            raise ValueError(f"camera feature_space={camera_feature_space!r} does not match {self.required_camera_feature_space!r}")
        human_path = human_row.get("motion_feature_path")
        if not human_path:
            raise KeyError(f"human manifest record is missing motion_feature_path for {sample_id}")
        camera_path = camera_row.get("camera_trajectory_path") or camera_row.get("traj_path")
        if not camera_path:
            raise KeyError(f"camera manifest record is missing camera_trajectory_path for {sample_id}")
        human_raw = _load_feature_tensor(_resolve(str(human_path), self.human_root))
        poses = torch.from_numpy(read_kitti_camera_poses(_resolve(str(camera_path), self.camera_root))).float()
        if self.feature_contract in {
            OFFICIAL_FEATURE_CONTRACT,
            RAW_OFFICIAL_FEATURE_CONTRACT,
            RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
            HUMAN200_FEATURE_CONTRACT,
        }:
            intrinsics_path = camera_row.get("intrinsics_path")
            if not intrinsics_path:
                raise KeyError(f"camera manifest record is missing intrinsics_path for {sample_id}")
            intrinsics = _load_feature_tensor(_resolve(str(intrinsics_path), self.camera_root))
            length = min(int(human_raw.shape[0]), int(poses.shape[0]), int(intrinsics.shape[0]))
            if length <= 0:
                raise ValueError(f"empty official human/camera sequence for {sample_id}")
            human_raw = human_raw[:length]
            poses = poses[:length]
            intrinsics = intrinsics[:length]
            human_root = _rifke_root_translation(human_raw)
            if self.feature_contract == OFFICIAL_FEATURE_CONTRACT:
                human = (human_raw - self.official_stats["human_mean"]) / self.official_stats["human_std"]
                camera = _official_camera_features(poses, intrinsics, human_root, self.official_stats)
            elif self.feature_contract == HUMAN200_FEATURE_CONTRACT:
                human = human199_raw_to_human200(human_raw, self.human200_stats)
                camera = _official_camera_features(poses, intrinsics, human_root, self.official_stats)
            elif self.feature_contract == RAW_OFFICIAL_FEATURE_CONTRACT:
                human = human_raw
                camera = _raw_official_camera_features(poses, intrinsics, human_root)
            else:
                human = human_raw
                camera = _official_camera_features(poses, intrinsics, human_root, self.official_stats)
        else:
            human = human_raw
            camera = torch.from_numpy(camera_poses_to_features(poses.numpy())).float()
            if self.drop_camera_z:
                camera = torch.cat([camera[:, :2], camera[:, 3:]], dim=-1)
        expected_human_dim = HUMAN200_DIM if self.feature_contract == HUMAN200_FEATURE_CONTRACT else HUMAN_FEATURE_DIM
        if human.shape[-1] != expected_human_dim:
            raise ValueError(f"expected human dim {expected_human_dim}, got {human.shape[-1]} for {sample_id}")
        expected_camera_dim = (
            OFFICIAL_CAMERA_FEATURE_DIM
            if self.feature_contract in {
                OFFICIAL_FEATURE_CONTRACT,
                RAW_OFFICIAL_FEATURE_CONTRACT,
                RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
                HUMAN200_FEATURE_CONTRACT,
            }
            else CAMERA_FEATURE_DIM - 1 if self.drop_camera_z else CAMERA_FEATURE_DIM
        )
        if camera.shape[-1] != expected_camera_dim:
            raise ValueError(f"expected camera dim {expected_camera_dim}, got {camera.shape[-1]} for {sample_id}")
        if human.shape[0] != camera.shape[0]:
            length = min(int(human.shape[0]), int(camera.shape[0]))
            if length <= 0:
                raise ValueError(f"empty human/camera sequence for {sample_id}: {human.shape[0]} vs {camera.shape[0]}")
            # PulpMotion exports occasionally disagree by a tail segment; keep the shared timeline.
            human = human[:length]
            camera = camera[:length]
        return {
            "human": human,
            "camera": camera,
            "lengths": int(human.shape[0]),
            "sample_id": sample_id,
            "human_feature_space": human_feature_space,
            "camera_feature_space": camera_feature_space,
            "feature_contract": self.feature_contract,
        }


def collate_human_camera_batch(
    batch: list[dict[str, Any]],
    *,
    fixed_max_frames: int = 0,
) -> dict[str, Any]:
    original_lengths = torch.tensor([item["human"].shape[0] for item in batch], dtype=torch.long)
    if fixed_max_frames < 0:
        raise ValueError("fixed_max_frames must be non-negative")
    lengths = original_lengths.clamp(max=fixed_max_frames) if fixed_max_frames else original_lengths
    max_len = fixed_max_frames or int(lengths.max().item())
    human_dim = int(batch[0]["human"].shape[1])
    camera_dim = int(batch[0]["camera"].shape[1])
    human = torch.zeros(len(batch), max_len, human_dim, dtype=torch.float32)
    camera = torch.zeros(len(batch), max_len, camera_dim, dtype=torch.float32)
    for i, item in enumerate(batch):
        human_seq = item["human"].float()
        camera_seq = item["camera"].float()
        if human_seq.shape[0] != camera_seq.shape[0]:
            raise ValueError(f"human/camera length mismatch in batch item {i}")
        valid_frames = int(lengths[i].item())
        human[i, :valid_frames] = human_seq[:valid_frames]
        camera[i, :valid_frames] = camera_seq[:valid_frames]
    return {
        "human": human,
        "camera": camera,
        "lengths": lengths,
        "original_lengths": original_lengths,
        "sample_id": [item.get("sample_id", "") for item in batch],
        "human_feature_space": [item.get("human_feature_space") for item in batch],
        "camera_feature_space": [item.get("camera_feature_space") for item in batch],
        "feature_contract": [item.get("feature_contract") for item in batch],
    }
