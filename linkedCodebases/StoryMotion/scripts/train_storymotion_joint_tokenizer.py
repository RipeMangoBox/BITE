#!/usr/bin/env python3
from __future__ import annotations

import argparse
from functools import partial
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import torch
from torch.utils.data import DataLoader, random_split

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from storymotion.tokenizers.factory import build_joint_human_camera_tokenizer
from storymotion.training import JointHumanCameraTokenizerTrainer, JointTrainerConfig
from storymotion.training.joint_data import (
    CAMERA_FEATURE_DIM,
    CAMERA_FEATURE_SPACE,
    HUMAN_FEATURE_DIM,
    HUMAN_FEATURE_SPACE,
    LEGACY_FEATURE_CONTRACT,
    RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
    RAW_OFFICIAL_FEATURE_CONTRACT,
    OFFICIAL_CAMERA_FEATURE_DIM,
    OFFICIAL_FEATURE_CONTRACT,
    _load_official_stats,
    PairedPulpMotionHumanCameraDataset,
    RandomHumanCameraDataset,
    collate_human_camera_batch,
)
from storymotion.training.human200 import (
    HUMAN200_DIM,
    HUMAN200_FEATURE_CONTRACT,
    HUMAN200_LAYOUT,
    load_human200_stats,
)
from scripts.storymotion_run_layout import init_run, run_paths, update_manifest


PRESETS = {
    "storymotion_v8_2_joint_ae_human200_camera14": {
        "tokenizer": "joint_ae",
        "human_dim": HUMAN200_DIM,
        "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
        "feature_contract": HUMAN200_FEATURE_CONTRACT,
    },
    "storymotion_v8_1b_residual_joint_ae_199_14": {
        "tokenizer": "joint_residual_ae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 192,
        "downsample": 4,
        "residual_depth": 2,
        "dilation_growth_rate": 3,
        "residual_activation": "relu",
        "residual_dropout": 0.2,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
        "feature_contract": OFFICIAL_FEATURE_CONTRACT,
    },
    "pulpmotion_joint_ae_official_199_14_pulp192": {
        "tokenizer": "joint_ae", "human_dim": HUMAN_FEATURE_DIM, "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128, "camera_latent_dim": 64, "hidden_dim": 256, "downsample": 4,
        "human_recon_weight": 1.0, "camera_recon_weight": 1.0, "velocity_weight": 1.0,
        "feature_contract": OFFICIAL_FEATURE_CONTRACT,
    },
    "pulpmotion_joint_ae_raw_199_14_pulp192": {
        "tokenizer": "joint_ae", "human_dim": HUMAN_FEATURE_DIM, "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128, "camera_latent_dim": 64, "hidden_dim": 256, "downsample": 4,
        "human_recon_weight": 1.0, "camera_recon_weight": 1.0, "velocity_weight": 1.0,
        "feature_contract": RAW_OFFICIAL_FEATURE_CONTRACT,
    },
    "pulpmotion_joint_ae_rawhuman_normcam_199_14_pulp192": {
        "tokenizer": "joint_ae", "human_dim": HUMAN_FEATURE_DIM, "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128, "camera_latent_dim": 64, "hidden_dim": 256, "downsample": 4,
        "human_recon_weight": 1.0, "camera_recon_weight": 1.0, "velocity_weight": 1.0,
        "feature_contract": RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
    },
    "pulpmotion_joint_vae_official_199_14_pulp192": {
        "tokenizer": "joint_vae", "human_dim": HUMAN_FEATURE_DIM, "camera_dim": OFFICIAL_CAMERA_FEATURE_DIM,
        "human_latent_dim": 128, "camera_latent_dim": 64, "hidden_dim": 256, "downsample": 4, "kl_weight": 1.0e-5,
        "human_recon_weight": 1.0, "camera_recon_weight": 1.0, "velocity_weight": 1.0,
        "feature_contract": OFFICIAL_FEATURE_CONTRACT,
    },
    "pulpmotion_joint_ae_199_9_pulp192": {
        "tokenizer": "joint_ae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
    },
    "pulpmotion_joint_vae_199_9_pulp192": {
        "tokenizer": "joint_vae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "kl_weight": 1.0e-5,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
    },
    "pulpmotion_joint_vqvae_199_9": {
        "tokenizer": "joint_vqvae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 448,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "codebook_size": 512,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
        "ema_decay": 0.99,
    },
    "pulpmotion_joint_hfsq_199_9_pulp192": {
        "tokenizer": "joint_hfsq",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "fsq_levels": "8,5,5,5",
        "hfsq_groups": 8,
        "hfsq_num_quantizers": 2,
        "hfsq_quantize_dropout_prob": 0.0,
        "hfsq_base_mask_rate": 0.0,
        "hfsq_r_rand_scale": 0.0,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
    },
    "pulpmotion_joint_grfsq_199_9_pulp192": {
        "tokenizer": "joint_grfsq",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "fsq_levels": "8,5,5,5",
        "hfsq_groups": 8,
        "hfsq_num_quantizers": 2,
        "hfsq_quantize_dropout_prob": 0.0,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
    },
    "pulpmotion_separate_ae_199_9_pulp192": {
        "tokenizer": "separate_ae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
    },
    "pulpmotion_separate_vae_199_9_pulp192": {
        "tokenizer": "separate_vae",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "kl_weight": 1.0e-5,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 1.0,
    },
    "pulpmotion_separate_grfsq_199_9_pulp192": {
        "tokenizer": "separate_grfsq",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "fsq_levels": "8,5,5,5",
        "hfsq_groups": 8,
        "hfsq_num_quantizers": 2,
        "hfsq_quantize_dropout_prob": 0.0,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
    },
    "pulpmotion_separate_hfsq_199_9_pulp192": {
        "tokenizer": "separate_hfsq",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 128,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "fsq_levels": "8,5,5,5",
        "hfsq_groups": 8,
        "hfsq_num_quantizers": 2,
        "hfsq_quantize_dropout_prob": 0.0,
        "hfsq_base_mask_rate": 0.0,
        "hfsq_r_rand_scale": 0.0,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
    },
    "pulpmotion_joint_hfsq_199_9": {
        "tokenizer": "joint_hfsq",
        "human_dim": HUMAN_FEATURE_DIM,
        "camera_dim": CAMERA_FEATURE_DIM,
        "human_latent_dim": 448,
        "camera_latent_dim": 64,
        "hidden_dim": 256,
        "downsample": 4,
        "fsq_levels": "8,5,5,5",
        "hfsq_groups": 8,
        "hfsq_num_quantizers": 2,
        "hfsq_quantize_dropout_prob": 0.0,
        "hfsq_base_mask_rate": 0.0,
        "hfsq_r_rand_scale": 0.0,
        "commitment_weight": 0.02,
        "human_recon_weight": 1.0,
        "camera_recon_weight": 1.0,
        "velocity_weight": 0.5,
    },
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Train Pulp-style joint human-camera StoryMotion stage1 tokenizers.")
    parser.add_argument("--preset", choices=sorted(PRESETS), default="pulpmotion_joint_hfsq_199_9")
    parser.add_argument("--loss-config", type=Path, default=None, help="Optional YAML/JSON overrides for Stage1 loss weights and selected train args.")
    parser.add_argument("--tokenizer", choices=["joint_ae", "joint_residual_ae", "joint_vae", "joint_vqvae", "joint_hfsq", "joint_grfsq", "separate_ae", "separate_vae", "separate_grfsq", "separate_hfsq"], default=None)
    parser.add_argument("--human-manifest", type=Path, default=Path("runs/train/pulpmotion_native_train_manifest_full_fast_20260608.jsonl"))
    parser.add_argument("--camera-manifest", type=Path, default=Path("runs/train/pulpmotion_camera_train_manifest_full_20260610.jsonl"))
    parser.add_argument("--val-human-manifest", type=Path, default=Path("runs/train/pulpmotion_native_test_manifest_full_20260608.jsonl"))
    parser.add_argument("--val-camera-manifest", type=Path, default=Path("runs/train/pulpmotion_camera_test_manifest_full_20260610.jsonl"))
    parser.add_argument("--human-root", type=Path, default=None)
    parser.add_argument("--camera-root", type=Path, default=None)
    parser.add_argument("--required-human-feature-space", default=HUMAN_FEATURE_SPACE)
    parser.add_argument("--required-camera-feature-space", default=CAMERA_FEATURE_SPACE)
    parser.add_argument("--drop-camera-z", action="store_true", help="Use camera xy+rot6d features by dropping translation z from the 9D camera representation.")
    parser.add_argument(
        "--feature-contract",
        choices=[
            LEGACY_FEATURE_CONTRACT,
            OFFICIAL_FEATURE_CONTRACT,
            RAW_OFFICIAL_FEATURE_CONTRACT,
            RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
            HUMAN200_FEATURE_CONTRACT,
        ],
        default=LEGACY_FEATURE_CONTRACT,
    )
    parser.add_argument(
        "--raw-loss-normalized",
        action="store_true",
        help="For a raw human contract, compute the affected reconstruction/temporal losses after the fixed official affine normalization.",
    )
    parser.add_argument("--pulp-root", type=Path, default=REPO_ROOT / "linked/PulpMotion")
    parser.add_argument("--human200-stats", type=Path, default=None)
    parser.add_argument("--synthetic", action="store_true")
    parser.add_argument("--num-samples", type=int, default=16)
    parser.add_argument("--seq-len", type=int, default=64)
    parser.add_argument(
        "--fixed-max-frames",
        type=int,
        default=0,
        help="Right-pad every real-data batch to this length and truncate longer samples; 0 keeps dynamic padding.",
    )
    parser.add_argument("--human-dim", type=int, default=HUMAN_FEATURE_DIM)
    parser.add_argument("--camera-dim", type=int, default=CAMERA_FEATURE_DIM)
    parser.add_argument("--human-latent-dim", type=int, default=448)
    parser.add_argument("--camera-latent-dim", type=int, default=64)
    parser.add_argument("--hidden-dim", type=int, default=256)
    parser.add_argument("--downsample", type=int, default=4)
    parser.add_argument("--residual-depth", type=int, default=2)
    parser.add_argument("--dilation-growth-rate", type=int, default=3)
    parser.add_argument("--residual-activation", choices=["relu", "gelu", "silu"], default="relu")
    parser.add_argument("--residual-dropout", type=float, default=0.2)
    parser.add_argument("--codebook-size", type=int, default=512)
    parser.add_argument("--kl-weight", type=float, default=1e-5)
    parser.add_argument("--commitment-weight", type=float, default=0.02)
    parser.add_argument("--human-recon-weight", type=float, default=1.0)
    parser.add_argument("--camera-recon-weight", type=float, default=1.0)
    parser.add_argument("--velocity-weight", type=float, default=0.5)
    parser.add_argument("--human-velocity-weight", type=float, default=None)
    parser.add_argument("--camera-velocity-weight", type=float, default=None)
    parser.add_argument("--human-acceleration-weight", type=float, default=0.0)
    parser.add_argument("--camera-acceleration-weight", type=float, default=0.0)
    parser.add_argument("--human-yaw-weight", type=float, default=0.0)
    parser.add_argument("--human-root-weight", type=float, default=0.0)
    parser.add_argument("--camera-center-weight", type=float, default=0.0)
    parser.add_argument("--camera-rotation-weight", type=float, default=0.0)
    parser.add_argument("--human-horizon-weight", type=float, default=0.0)
    parser.add_argument("--human-multi-horizon-weight", type=float, default=0.0)
    parser.set_defaults(is_causal=False)
    parser.add_argument("--non-causal", dest="is_causal", action="store_false", help="Use symmetric temporal conv padding.")
    parser.add_argument("--ema-decay", type=float, default=0.99)
    parser.add_argument("--fsq-levels", default=None)
    parser.add_argument("--hfsq-groups", type=int, default=8)
    parser.add_argument("--hfsq-num-quantizers", type=int, default=2)
    parser.add_argument("--hfsq-quantize-dropout-prob", type=float, default=0.0)
    parser.add_argument("--hfsq-base-mask-rate", type=float, default=0.0)
    parser.add_argument("--hfsq-r-rand-scale", type=float, default=0.0)
    parser.add_argument("--hfsq-w-scale-division", action="store_true")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--eval-batch-size", type=int, default=0, help="Validation batch size; 0 reuses --batch-size.")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--expected-train-samples", type=int, default=0, help="Fail closed unless the ordered train set has this size; 0 disables the check.")
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--val-every-steps", type=int, default=2000)
    parser.add_argument("--eval-every-steps", type=int, default=5000)
    parser.add_argument("--save-every-steps", type=int, default=25000)
    parser.add_argument("--warmup-steps", type=int, default=1000)
    parser.add_argument("--min-lr", type=float, default=1e-6)
    parser.add_argument("--grad-clip", type=float, default=1.0)
    parser.add_argument("--weight-decay", type=float, default=0.0)
    parser.add_argument("--beta1", type=float, default=0.9)
    parser.add_argument("--beta2", type=float, default=0.999)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--pin-memory", action="store_true")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--runs-root", type=Path, default=REPO_ROOT / "runs")
    parser.add_argument("--run-id", help="Canonical Stage1 run id; derives train/checkpoints and tensorboard paths.")
    parser.add_argument("--log-dir", type=Path, default=None)
    parser.add_argument("--checkpoint", type=Path, default=None)
    parser.add_argument("--checkpoint-dir", type=Path, default=None)
    parser.add_argument("--checkpoint-prefix", default=None)
    parser.add_argument("--keep-best-checkpoints", type=int, default=3)
    parser.add_argument("--keep-step-checkpoints", type=int, default=3)
    return parser


def apply_preset(args: argparse.Namespace, parser: argparse.ArgumentParser) -> argparse.Namespace:
    defaults = {action.dest: action.default for action in parser._actions}
    for key, value in PRESETS[args.preset].items():
        if getattr(args, key, None) == defaults.get(key):
            setattr(args, key, value)
    return args


def _load_config(path: Path) -> dict[str, Any]:
    if path.suffix.lower() in {".yaml", ".yml"}:
        import yaml

        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError(f"loss config must be a mapping: {path}")
    return loaded


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"cannot parse boolean value: {value!r}")


def apply_loss_config(args: argparse.Namespace) -> argparse.Namespace:
    if args.loss_config is None:
        return args
    config = _load_config(args.loss_config)
    allowed = {
        "human_recon_weight",
        "camera_recon_weight",
        "velocity_weight",
        "human_velocity_weight",
        "camera_velocity_weight",
        "human_acceleration_weight",
        "camera_acceleration_weight",
        "human_yaw_weight",
        "human_root_weight",
        "camera_center_weight",
        "camera_rotation_weight",
        "human_horizon_weight",
        "human_multi_horizon_weight",
        "kl_weight",
        "commitment_weight",
    }
    if "stage1_loss" in config:
        loss = config["stage1_loss"]
    elif "loss" in config:
        loss = config["loss"]
    else:
        loss = {key: value for key, value in config.items() if str(key).replace("-", "_") in allowed}
    if not isinstance(loss, dict):
        raise ValueError("loss config 'stage1_loss' must be a mapping")
    for key, value in loss.items():
        normalized = str(key).replace("-", "_")
        if normalized not in allowed:
            raise ValueError(f"unsupported Stage1 loss config key: {key}")
        setattr(args, normalized, float(value))
    train = config.get("train", {})
    if train:
        if not isinstance(train, dict):
            raise ValueError("loss config 'train' must be a mapping")
        train_allowed = {"lr", "batch_size", "epochs", "warmup_steps", "min_lr", "grad_clip", "weight_decay"}
        for key, value in train.items():
            normalized = str(key).replace("-", "_")
            if normalized not in train_allowed:
                raise ValueError(f"unsupported train config key: {key}")
            current = getattr(args, normalized)
            setattr(args, normalized, type(current)(value))
    model_config = config.get("stage1_model", config.get("model", {}))
    if model_config:
        if not isinstance(model_config, dict):
            raise ValueError("loss config 'stage1_model' must be a mapping")
        model_allowed = {"is_causal", "is_casual"}
        for key, value in model_config.items():
            normalized = str(key).replace("-", "_")
            if normalized not in model_allowed:
                raise ValueError(f"unsupported model config key: {key}")
            if normalized in {"is_causal", "is_casual"}:
                setattr(args, "is_causal", parse_bool(value))
    return args


def apply_branch_loss_weights(model: torch.nn.Module, args: argparse.Namespace) -> None:
    base_model = model.module if hasattr(model, "module") else model
    base_model.human_velocity_weight = float(args.human_velocity_weight if args.human_velocity_weight is not None else args.velocity_weight)
    base_model.camera_velocity_weight = float(args.camera_velocity_weight if args.camera_velocity_weight is not None else args.velocity_weight)
    base_model.human_acceleration_weight = float(args.human_acceleration_weight)
    base_model.camera_acceleration_weight = float(args.camera_acceleration_weight)
    base_model.human_yaw_weight = float(args.human_yaw_weight)
    base_model.human_root_weight = float(args.human_root_weight)
    base_model.camera_center_weight = float(args.camera_center_weight)
    base_model.camera_rotation_weight = float(args.camera_rotation_weight)
    base_model.human_horizon_weight = float(args.human_horizon_weight)
    base_model.human_multi_horizon_weight = float(args.human_multi_horizon_weight)


def configure_human_geometry_loss(model: torch.nn.Module, args: argparse.Namespace) -> None:
    geometry_weights = (
        args.human_yaw_weight,
        args.human_root_weight,
        args.camera_center_weight,
        args.camera_rotation_weight,
        args.human_horizon_weight,
        args.human_multi_horizon_weight,
    )
    if any(weight < 0.0 for weight in geometry_weights):
        raise ValueError("Stage1 geometry loss weights must be non-negative")
    if args.human_horizon_weight != 0.0 and args.human_yaw_weight == 0.0 and args.human_root_weight == 0.0:
        raise ValueError("human-horizon loss requires a nonzero human yaw or root parent weight")
    if args.human_multi_horizon_weight != 0.0 and args.human_yaw_weight == 0.0 and args.human_root_weight == 0.0:
        raise ValueError("human-multi-horizon loss requires a nonzero human yaw or root parent weight")
    if args.human_horizon_weight != 0.0 and args.human_multi_horizon_weight != 0.0:
        raise ValueError("last-valid and multi-horizon Human auxiliaries are mutually exclusive")
    if args.feature_contract == HUMAN200_FEATURE_CONTRACT:
        if args.tokenizer != "joint_ae" or args.human_dim != HUMAN200_DIM:
            raise ValueError("v8.2 human200 geometry requires the matched non-causal joint AE")
        if args.human_yaw_weight != 0.001 or args.human_root_weight != 0.003:
            raise ValueError("v8.2 must keep the matched v8.1 yaw/root weights 0.001/0.003")
        if (
            args.camera_center_weight != 0.0
            or args.camera_rotation_weight != 0.0
            or args.human_horizon_weight != 0.0
            or args.human_multi_horizon_weight != 0.0
        ):
            raise ValueError("camera center/rotation and Human horizon supervision are not part of the v8.2 contract")
        stats = load_human200_stats(args.human200_stats, expected_train_manifest=args.human_manifest)
        base_model = model.module if hasattr(model, "module") else model
        base_model.geometry_human_mean = stats["mean"]
        base_model.geometry_human_std = stats["std"]
        base_model.geometry_feature_contract = "human200_direct_root_yaw"
        return
    if all(weight == 0.0 for weight in geometry_weights):
        return
    if args.tokenizer not in {"joint_ae", "joint_residual_ae"} or args.feature_contract != OFFICIAL_FEATURE_CONTRACT or args.human_dim != 199:
        raise ValueError("human yaw/root loss is restricted to a v8.1 normalized-human199 joint AE")
    stats = _load_official_stats(args.pulp_root)
    base_model = model.module if hasattr(model, "module") else model
    base_model.geometry_human_mean = stats["human_mean"]
    base_model.geometry_human_std = stats["human_std"]
    base_model.geometry_feature_contract = "human199_integrated_root_yaw"
    if args.camera_center_weight != 0.0:
        base_model.geometry_camera_velocity_mean = stats["velocity_mean"]
        base_model.geometry_camera_velocity_std = stats["velocity_std"]
        base_model.geometry_camera_distance_mean = stats["distance_mean"]
        base_model.geometry_camera_distance_std = stats["distance_std"]


def configure_loss_space(model: torch.nn.Module, args: argparse.Namespace) -> None:
    if not args.raw_loss_normalized:
        return
    if args.feature_contract not in {
        RAW_OFFICIAL_FEATURE_CONTRACT,
        RAW_HUMAN_OFFICIAL_CAMERA_FEATURE_CONTRACT,
    }:
        raise ValueError("--raw-loss-normalized requires a raw-human official 14D feature contract")
    stats = _load_official_stats(args.pulp_root)
    base_model = model.module if hasattr(model, "module") else model
    base_model.loss_human_mean = stats["human_mean"]
    base_model.loss_human_std = stats["human_std"]
    if args.feature_contract == RAW_OFFICIAL_FEATURE_CONTRACT:
        camera_mean = torch.zeros(OFFICIAL_CAMERA_FEATURE_DIM, dtype=torch.float32)
        camera_std = torch.ones(OFFICIAL_CAMERA_FEATURE_DIM, dtype=torch.float32)
        camera_mean[2:5] = stats["distance_mean"]
        camera_std[2:5] = stats["distance_std"]
        camera_mean[11:14] = stats["velocity_mean"]
        camera_std[11:14] = stats["velocity_std"]
        base_model.loss_camera_mean = camera_mean
        base_model.loss_camera_std = camera_std


def seed_everything(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np

        np.random.seed(seed)
    except ImportError:
        pass
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def seed_worker(worker_id: int) -> None:
    worker_seed = torch.initial_seed() % 2**32
    random.seed(worker_seed)
    try:
        import numpy as np

        np.random.seed(worker_seed)
    except ImportError:
        pass


def configure_human200_provenance(args: argparse.Namespace) -> None:
    if args.feature_contract != HUMAN200_FEATURE_CONTRACT:
        if args.human200_stats is not None:
            raise ValueError("--human200-stats is only valid with the v8.2 feature contract")
        return
    if args.human200_stats is None:
        raise ValueError("--human200-stats is required for the v8.2 feature contract")
    stats = load_human200_stats(args.human200_stats, expected_train_manifest=args.human_manifest)
    source = stats["meta"]["source"]
    args.human200_stats_resolved = str(stats["path"])
    args.human200_stats_sha256 = stats["sha256"]
    args.human200_stats_source_manifest_sha256 = source["manifest_sha256"]
    args.human200_stats_source_sample_ids_sha256 = source["sample_ids_sha256"]
    args.human200_stats_source_samples = int(source["samples"])
    args.human200_stats_source_frames = int(source["frames"])


def make_datasets(args: argparse.Namespace):
    if args.synthetic:
        dataset = RandomHumanCameraDataset(args.num_samples, args.seq_len, args.human_dim, args.camera_dim, seed=17)
        val_size = max(1, len(dataset) // 4)
        train_size = len(dataset) - val_size
        if train_size <= 0:
            raise ValueError("synthetic dataset must contain at least two samples")
        train_ds, val_ds = random_split(dataset, [train_size, val_size], generator=torch.Generator().manual_seed(19))
        return train_ds, val_ds, "val"
    train_ds = PairedPulpMotionHumanCameraDataset(
        args.human_manifest,
        args.camera_manifest,
        human_root=args.human_root,
        camera_root=args.camera_root,
        required_human_feature_space=args.required_human_feature_space,
        required_camera_feature_space=args.required_camera_feature_space,
        drop_camera_z=args.drop_camera_z,
        feature_contract=args.feature_contract,
        pulp_root=args.pulp_root,
        human200_stats_path=args.human200_stats,
        human200_expected_train_manifest=(
            args.human_manifest if args.feature_contract == HUMAN200_FEATURE_CONTRACT else None
        ),
    )
    val_ds = None
    val_split = ""
    if args.val_human_manifest is not None and args.val_camera_manifest is not None:
        val_ds = PairedPulpMotionHumanCameraDataset(
            args.val_human_manifest,
            args.val_camera_manifest,
            human_root=args.human_root,
            camera_root=args.camera_root,
            required_human_feature_space=args.required_human_feature_space,
            required_camera_feature_space=args.required_camera_feature_space,
            drop_camera_z=args.drop_camera_z,
            feature_contract=args.feature_contract,
            pulp_root=args.pulp_root,
            human200_stats_path=args.human200_stats,
            human200_expected_train_manifest=(
                args.human_manifest if args.feature_contract == HUMAN200_FEATURE_CONTRACT else None
            ),
        )
        val_split = "test"
    return train_ds, val_ds, val_split


def dataset_dims(dataset) -> tuple[int, int]:
    sample = dataset[0]
    return int(sample["human"].shape[1]), int(sample["camera"].shape[1])


def write_run_config(args: argparse.Namespace) -> None:
    if args.checkpoint_dir:
        args.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        config_path = (
            args.run_root / "run_config.json"
            if getattr(args, "run_root", None) is not None
            else args.checkpoint_dir.parent / "run_config.json"
        )
        config_path.write_text(
            json.dumps(vars(args), indent=2, sort_keys=True, default=str)
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample_ids(dataset) -> list[str]:
    if hasattr(dataset, "records"):
        return [str(human.get("sample_id") or camera.get("sample_id")) for human, camera in dataset.records]
    return [str(dataset[index].get("sample_id", index)) for index in range(len(dataset))]


def stage1_model_contract(args: argparse.Namespace) -> dict[str, Any]:
    native_latent_order = (
        f"camera{args.camera_latent_dim}+human{args.human_latent_dim}"
        if args.tokenizer == "joint_residual_ae" or args.feature_contract == HUMAN200_FEATURE_CONTRACT
        else f"human{args.human_latent_dim}+camera{args.camera_latent_dim}"
    )
    contract = {
        "tokenizer": args.tokenizer,
        "preset": args.preset,
        "feature_contract": args.feature_contract,
        "is_causal": False,
        "human_dim": args.human_dim,
        "camera_dim": args.camera_dim,
        "human_latent_dim": args.human_latent_dim,
        "camera_latent_dim": args.camera_latent_dim,
        "native_latent_order": native_latent_order,
        "hidden_dim": args.hidden_dim,
        "downsample": args.downsample,
        "residual_depth": args.residual_depth if args.tokenizer == "joint_residual_ae" else None,
        "dilation_growth_rate": args.dilation_growth_rate if args.tokenizer == "joint_residual_ae" else None,
        "residual_activation": args.residual_activation if args.tokenizer == "joint_residual_ae" else None,
        "residual_dropout": args.residual_dropout if args.tokenizer == "joint_residual_ae" else None,
        "initialization": "random_seeded_no_pretrained_stage1_checkpoint",
    }
    if args.feature_contract == HUMAN200_FEATURE_CONTRACT:
        contract["human_representation"] = {
            "layout": HUMAN200_LAYOUT,
            "owning_inverse": "human200_raw_to_human199_raw",
            "root_yaw_policy": "direct_relative_root_xy_and_atan2_yaw_without_integration",
        }
        contract["normalization"] = {
            "path": args.human200_stats_resolved,
            "sha256": args.human200_stats_sha256,
            "source_manifest_sha256": args.human200_stats_source_manifest_sha256,
            "source_sample_ids_sha256": args.human200_stats_source_sample_ids_sha256,
            "source_samples": args.human200_stats_source_samples,
            "source_frames": args.human200_stats_source_frames,
            "source_split": "train",
        }
    return contract


def write_stage1_contract(
    args: argparse.Namespace,
    train_ds,
    val_ds,
    *,
    checkpoint_sha256: str = "",
    status: str,
) -> None:
    if not args.run_id or args.run_root is None:
        return
    train_ids = sample_ids(train_ds)
    val_ids = sample_ids(val_ds) if val_ds is not None else []
    checkpoint = args.checkpoint_dir / f"{args.checkpoint_prefix or args.preset}_last.pt"

    def ids_hash(values: list[str]) -> str:
        return hashlib.sha256(("\n".join(values) + "\n").encode()).hexdigest()

    payload = {
        "schema_version": 1,
        "stage": "stage1",
        "version": ".".join(args.run_id.split("_")[:2]),
        "run_id": args.run_id,
        "status": status,
        "data": {
            "train_manifest": str(args.human_manifest),
            "train_camera_manifest": str(args.camera_manifest),
            "train_split": "train",
            "train_samples": len(train_ids),
            "train_sample_ids_sha256": ids_hash(train_ids),
            "eval_manifest": str(args.val_human_manifest),
            "eval_camera_manifest": str(args.val_camera_manifest),
            "eval_split": "pure_test",
            "eval_samples": len(val_ids),
            "eval_sample_ids_sha256": ids_hash(val_ids),
        },
        "model": {
            "tokenizer": args.tokenizer,
            "preset": args.preset,
            "feature_contract": args.feature_contract,
            "is_causal": False,
            "human_dim": args.human_dim,
            "camera_dim": args.camera_dim,
            "human_latent_dim": args.human_latent_dim,
            "camera_latent_dim": args.camera_latent_dim,
            "latent_order": stage1_model_contract(args)["native_latent_order"],
            "architecture": stage1_model_contract(args),
            "padding_policy": "fixed_right_zero_pad_and_loss_mask" if args.fixed_max_frames else "dynamic_batch_max_and_loss_mask",
            "fixed_max_frames": args.fixed_max_frames,
            **(
                {
                    "normalization": stage1_model_contract(args)["normalization"],
                    "human_representation": stage1_model_contract(args)["human_representation"],
                }
                if args.feature_contract == HUMAN200_FEATURE_CONTRACT
                else {}
            ),
        },
        "train": {
            "seed": args.seed,
            "batch_size": args.batch_size,
            "epochs": args.epochs,
            "optimizer_steps": ((len(train_ids) + args.batch_size - 1) // args.batch_size) * args.epochs,
            "sample_exposures": len(train_ids) * args.epochs,
            "lr": args.lr,
        },
        "eval": {
            "seed": args.seed,
            "batch_size": args.eval_batch_size or args.batch_size,
            "sample_count": len(val_ids),
        },
        "loss": {
            "human_recon_weight": args.human_recon_weight,
            "camera_recon_weight": args.camera_recon_weight,
            "human_velocity_weight": args.human_velocity_weight if args.human_velocity_weight is not None else args.velocity_weight,
            "camera_velocity_weight": args.camera_velocity_weight if args.camera_velocity_weight is not None else args.velocity_weight,
            "human_acceleration_weight": args.human_acceleration_weight,
            "camera_acceleration_weight": args.camera_acceleration_weight,
            "human_yaw_weight": args.human_yaw_weight,
            "human_root_weight": args.human_root_weight,
            "camera_center_weight": args.camera_center_weight,
            "camera_rotation_weight": args.camera_rotation_weight,
            "human_horizon_weight": args.human_horizon_weight,
            "human_multi_horizon_weight": args.human_multi_horizon_weight,
        },
        "checkpoint": {
            "path": str(checkpoint),
            "sha256": checkpoint_sha256,
            "owning_decoder": str(checkpoint),
            "owning_decoder_sha256": checkpoint_sha256,
        },
    }
    (args.run_root / "experiment_contract.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def apply_run_layout(args: argparse.Namespace) -> argparse.Namespace:
    """Resolve canonical Stage1 paths when a run id is supplied."""
    if args.run_id:
        paths = run_paths("stage1", args.run_id, args.runs_root)
        if not paths["root"].exists():
            init_run(
                "stage1",
                args.run_id,
                runs_root=args.runs_root,
                description="StoryMotion joint human-camera tokenizer training",
            )
        args.run_root = paths["root"]
        args.log_dir = args.log_dir or paths["tensorboard"]
        args.checkpoint_dir = args.checkpoint_dir or paths["checkpoints"]
    else:
        args.run_root = None
        args.log_dir = args.log_dir or Path("runs/storymotion_joint_tokenizer")
    return args


def main() -> None:
    parser = build_parser()
    args = apply_run_layout(apply_loss_config(apply_preset(parser.parse_args(), parser)))
    assert args.is_causal is False
    args.is_causal = False
    configure_human200_provenance(args)
    seed_everything(args.seed)
    if args.drop_camera_z and args.camera_dim == CAMERA_FEATURE_DIM:
        args.camera_dim = CAMERA_FEATURE_DIM - 1
    train_ds, val_ds, val_split = make_datasets(args)
    if args.expected_train_samples and len(train_ds) != args.expected_train_samples:
        raise ValueError(
            f"ordered train set has {len(train_ds)} samples, expected {args.expected_train_samples}"
        )
    human_dim, camera_dim = dataset_dims(train_ds)
    if human_dim != args.human_dim:
        raise ValueError(f"dataset human dim {human_dim} does not match --human-dim {args.human_dim}")
    if camera_dim != args.camera_dim:
        raise ValueError(f"dataset camera dim {camera_dim} does not match --camera-dim {args.camera_dim}")
    if val_ds is not None and dataset_dims(val_ds) != (args.human_dim, args.camera_dim):
        raise ValueError(f"{val_split} feature dims do not match requested dims")
    write_run_config(args)
    write_stage1_contract(args, train_ds, val_ds, status="training")
    if args.run_id:
        update_manifest("stage1", args.run_id, runs_root=args.runs_root, status="training")
    collate_fn = partial(collate_human_camera_batch, fixed_max_frames=args.fixed_max_frames)
    train_generator = torch.Generator()
    train_generator.manual_seed(args.seed)
    train_loader = DataLoader(
        train_ds,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        pin_memory=args.pin_memory,
        collate_fn=collate_fn,
        generator=train_generator,
        worker_init_fn=seed_worker,
    )
    val_loader = None
    if val_ds is not None:
        val_loader = DataLoader(
            val_ds,
            batch_size=args.eval_batch_size or args.batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            pin_memory=args.pin_memory,
            collate_fn=collate_fn,
            worker_init_fn=seed_worker,
        )
    model = build_joint_human_camera_tokenizer(
        args.tokenizer,
        human_dim=args.human_dim,
        camera_dim=args.camera_dim,
        human_latent_dim=args.human_latent_dim,
        camera_latent_dim=args.camera_latent_dim,
        hidden_dim=args.hidden_dim,
        downsample=args.downsample,
        codebook_size=args.codebook_size,
        kl_weight=args.kl_weight,
        commitment_weight=args.commitment_weight,
        human_recon_weight=args.human_recon_weight,
        camera_recon_weight=args.camera_recon_weight,
        velocity_weight=args.velocity_weight,
        ema_decay=args.ema_decay,
        fsq_levels=args.fsq_levels,
        hfsq_groups=args.hfsq_groups,
        hfsq_num_quantizers=args.hfsq_num_quantizers,
        hfsq_quantize_dropout_prob=args.hfsq_quantize_dropout_prob,
        hfsq_base_mask_rate=args.hfsq_base_mask_rate,
        hfsq_r_rand_scale=args.hfsq_r_rand_scale,
        hfsq_w_scale_division=args.hfsq_w_scale_division,
        residual_depth=args.residual_depth,
        dilation_growth_rate=args.dilation_growth_rate,
        residual_activation=args.residual_activation,
        residual_dropout=args.residual_dropout,
        is_causal=args.is_causal,
    )
    configure_loss_space(model, args)
    apply_branch_loss_weights(model, args)
    configure_human_geometry_loss(model, args)
    model.stage1_model_contract = stage1_model_contract(args)
    trainer = JointHumanCameraTokenizerTrainer(
        model,
        JointTrainerConfig(
            log_dir=args.log_dir,
            epochs=args.epochs,
            lr=args.lr,
            device=args.device,
            val_every_steps=args.val_every_steps,
            eval_every_steps=args.eval_every_steps,
            save_every_steps=args.save_every_steps,
            warmup_steps=args.warmup_steps,
            min_lr=args.min_lr,
            weight_decay=args.weight_decay,
            beta1=args.beta1,
            beta2=args.beta2,
            grad_clip=args.grad_clip,
            checkpoint_dir=args.checkpoint_dir,
            checkpoint_prefix=args.checkpoint_prefix or args.preset,
            keep_best_checkpoints=args.keep_best_checkpoints,
            keep_step_checkpoints=args.keep_step_checkpoints,
        ),
    )
    trainer.fit(train_loader, val_loader, val_split=val_split or "val")
    if args.run_id:
        last_checkpoint = args.checkpoint_dir / f"{args.checkpoint_prefix or args.preset}_last.pt"
        if not last_checkpoint.is_file():
            raise FileNotFoundError(f"missing final Stage1 checkpoint: {last_checkpoint}")
        checkpoint_sha = sha256_file(last_checkpoint)
        write_stage1_contract(
            args,
            train_ds,
            val_ds,
            checkpoint_sha256=checkpoint_sha,
            status="trained",
        )
        update_manifest(
            "stage1",
            args.run_id,
            runs_root=args.runs_root,
            status="trained",
            artifacts={
                "checkpoint": str(last_checkpoint.relative_to(args.runs_root)),
                "tensorboard": str(args.log_dir.relative_to(args.runs_root)),
            },
        )
    if args.checkpoint:
        args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
        torch.save(
            {
                "model": model.state_dict(),
                "args": vars(args),
                "tokenizer": args.tokenizer,
                "stage1_model_contract": stage1_model_contract(args),
            },
            args.checkpoint,
        )
    summary = {
        "preset": args.preset,
        "tokenizer": args.tokenizer,
        "train_samples": len(train_ds),
        "val_samples": len(val_ds) if val_ds is not None else 0,
        "val_split": val_split,
        "human_dim": args.human_dim,
        "camera_dim": args.camera_dim,
        "drop_camera_z": args.drop_camera_z,
        "feature_contract": args.feature_contract,
        "raw_loss_normalized": args.raw_loss_normalized,
        "human_latent_dim": args.human_latent_dim,
        "camera_latent_dim": args.camera_latent_dim,
        "kl_weight": args.kl_weight,
        "commitment_weight": args.commitment_weight,
        "human_recon_weight": args.human_recon_weight,
        "camera_recon_weight": args.camera_recon_weight,
        "velocity_weight": args.velocity_weight,
        "human_velocity_weight": args.human_velocity_weight if args.human_velocity_weight is not None else args.velocity_weight,
        "camera_velocity_weight": args.camera_velocity_weight if args.camera_velocity_weight is not None else args.velocity_weight,
        "human_acceleration_weight": args.human_acceleration_weight,
        "camera_acceleration_weight": args.camera_acceleration_weight,
        "human_yaw_weight": args.human_yaw_weight,
        "human_root_weight": args.human_root_weight,
        "camera_center_weight": args.camera_center_weight,
        "camera_rotation_weight": args.camera_rotation_weight,
        "human_horizon_weight": args.human_horizon_weight,
        "human_multi_horizon_weight": args.human_multi_horizon_weight,
        "is_causal": args.is_causal,
        "fixed_max_frames": args.fixed_max_frames,
        "padding_policy": "fixed_right_zero_pad_and_loss_mask" if args.fixed_max_frames else "dynamic_batch_max_and_loss_mask",
        "loss_config": str(args.loss_config) if args.loss_config else "",
        "seed": args.seed,
        "hfsq_w_scale_division": args.hfsq_w_scale_division,
        "log_dir": str(args.log_dir),
        "checkpoint": str(args.checkpoint) if args.checkpoint else "",
        "checkpoint_dir": str(args.checkpoint_dir) if args.checkpoint_dir else "",
        "run_id": args.run_id or "",
        "run_root": str(args.run_root) if args.run_root else "",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
