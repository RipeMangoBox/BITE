from __future__ import annotations

from .continuous_vae import ContinuousMotionVAE
from .fsq_vae import MotionFSQVAE, MotionHFSQVAE
from .joint_human_camera import (
    AAMMARDMResidualJointHumanCameraAE,
    JointHumanCameraAE,
    JointHumanCameraGRFSQVAE,
    JointHumanCameraHFSQVAE,
    JointHumanCameraVAE,
    JointHumanCameraVQVAE,
    SeparateHumanCameraAE,
    SeparateHumanCameraGRFSQVAE,
    SeparateHumanCameraHFSQVAE,
    SeparateHumanCameraVAE,
)
from .vq_vae import MotionVQVAE


def _parse_levels(levels: str | list[int] | tuple[int, ...] | None) -> tuple[int, ...]:
    if levels is None:
        return (8, 5, 5, 5)
    if isinstance(levels, str):
        return tuple(int(part) for part in levels.split(",") if part)
    return tuple(int(level) for level in levels)


def build_tokenizer(
    tokenizer: str,
    *,
    motion_dim: int,
    latent_dim: int,
    hidden_dim: int,
    downsample: int,
    codebook_size: int = 512,
    kl_weight: float = 1.0e-5,
    velocity_weight: float | None = None,
    commitment_weight: float = 0.02,
    ema_decay: float = 0.99,
    fsq_levels: str | list[int] | tuple[int, ...] | None = None,
    fsq_num_codebooks: int = 1,
    hfsq_groups: int = 8,
    hfsq_num_quantizers: int = 2,
    hfsq_quantize_dropout_prob: float = 0.0,
    hfsq_base_mask_rate: float = 0.0,
    hfsq_r_rand_scale: float = 0.0,
    hfsq_w_scale_division: bool = False,
    is_causal: bool = False,
):
    assert is_causal is False
    levels = _parse_levels(fsq_levels)
    if tokenizer == "vae":
        return ContinuousMotionVAE(
            motion_dim=motion_dim,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            kl_weight=kl_weight,
            velocity_weight=1.0 if velocity_weight is None else velocity_weight,
        )
    if tokenizer == "vqvae":
        return MotionVQVAE(
            motion_dim=motion_dim,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            codebook_size=codebook_size,
            downsample=downsample,
            commitment_weight=commitment_weight,
            velocity_weight=0.5 if velocity_weight is None else velocity_weight,
            ema_decay=ema_decay,
        )
    if tokenizer == "fsq":
        return MotionFSQVAE(
            motion_dim=motion_dim,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            num_codebooks=fsq_num_codebooks,
            commitment_weight=commitment_weight,
            velocity_weight=0.5 if velocity_weight is None else velocity_weight,
        )
    if tokenizer == "hfsq":
        return MotionHFSQVAE(
            motion_dim=motion_dim,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            groups=hfsq_groups,
            num_quantizers=hfsq_num_quantizers,
            commitment_weight=commitment_weight,
            velocity_weight=0.5 if velocity_weight is None else velocity_weight,
            quantize_dropout_prob=hfsq_quantize_dropout_prob,
            base_mask_rate=hfsq_base_mask_rate,
            r_rand_scale=hfsq_r_rand_scale,
            w_scale_division=hfsq_w_scale_division,
        )
    raise ValueError(f"unknown tokenizer: {tokenizer}")


def build_joint_human_camera_tokenizer(
    tokenizer: str,
    *,
    human_dim: int,
    camera_dim: int,
    human_latent_dim: int,
    camera_latent_dim: int,
    hidden_dim: int,
    downsample: int,
    codebook_size: int = 512,
    kl_weight: float = 1.0e-5,
    commitment_weight: float = 0.02,
    human_recon_weight: float = 1.0,
    camera_recon_weight: float = 1.0,
    velocity_weight: float = 0.5,
    ema_decay: float = 0.99,
    fsq_levels: str | list[int] | tuple[int, ...] | None = None,
    hfsq_groups: int = 8,
    hfsq_num_quantizers: int = 2,
    hfsq_quantize_dropout_prob: float = 0.0,
    hfsq_base_mask_rate: float = 0.0,
    hfsq_r_rand_scale: float = 0.0,
    hfsq_w_scale_division: bool = False,
    residual_depth: int = 2,
    dilation_growth_rate: int = 3,
    residual_activation: str = "relu",
    residual_dropout: float = 0.2,
    is_causal: bool = False,
):
    assert is_causal is False
    levels = _parse_levels(fsq_levels)
    if tokenizer == "joint_ae":
        return JointHumanCameraAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
    if tokenizer == "joint_residual_ae":
        return AAMMARDMResidualJointHumanCameraAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            residual_depth=residual_depth,
            dilation_growth_rate=dilation_growth_rate,
            residual_activation=residual_activation,
            residual_dropout=residual_dropout,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
    if tokenizer == "joint_vae":
        return JointHumanCameraVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            kl_weight=kl_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
    if tokenizer == "joint_vqvae":
        return JointHumanCameraVQVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            codebook_size=codebook_size,
            downsample=downsample,
            commitment_weight=commitment_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            ema_decay=ema_decay,
            is_causal=is_causal,
        )
    if tokenizer == "joint_hfsq":
        return JointHumanCameraHFSQVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            groups=hfsq_groups,
            num_quantizers=hfsq_num_quantizers,
            commitment_weight=commitment_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            quantize_dropout_prob=hfsq_quantize_dropout_prob,
            base_mask_rate=hfsq_base_mask_rate,
            r_rand_scale=hfsq_r_rand_scale,
            w_scale_division=hfsq_w_scale_division,
            is_causal=is_causal,
        )
    if tokenizer == "joint_grfsq":
        return JointHumanCameraGRFSQVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            groups=hfsq_groups,
            num_quantizers=hfsq_num_quantizers,
            commitment_weight=commitment_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            quantize_dropout_prob=hfsq_quantize_dropout_prob,
            is_causal=is_causal,
        )
    if tokenizer == "separate_vae":
        return SeparateHumanCameraVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            kl_weight=kl_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
    if tokenizer == "separate_ae":
        return SeparateHumanCameraAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
    if tokenizer == "separate_grfsq":
        return SeparateHumanCameraGRFSQVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            groups=hfsq_groups,
            num_quantizers=hfsq_num_quantizers,
            commitment_weight=commitment_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            quantize_dropout_prob=hfsq_quantize_dropout_prob,
            is_causal=is_causal,
        )
    if tokenizer == "separate_hfsq":
        return SeparateHumanCameraHFSQVAE(
            human_dim=human_dim,
            camera_dim=camera_dim,
            human_latent_dim=human_latent_dim,
            camera_latent_dim=camera_latent_dim,
            hidden_dim=hidden_dim,
            downsample=downsample,
            levels=levels,
            groups=hfsq_groups,
            num_quantizers=hfsq_num_quantizers,
            commitment_weight=commitment_weight,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            quantize_dropout_prob=hfsq_quantize_dropout_prob,
            base_mask_rate=hfsq_base_mask_rate,
            r_rand_scale=hfsq_r_rand_scale,
            w_scale_division=hfsq_w_scale_division,
            is_causal=is_causal,
        )
    raise ValueError(f"unknown joint tokenizer: {tokenizer}")
