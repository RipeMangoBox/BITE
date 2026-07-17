from __future__ import annotations

from dataclasses import dataclass
import math

import torch
import torch.nn.functional as F
from torch import nn

from .base import masked_mean, masked_smooth_l1_loss, temporal_accel_loss, temporal_diff_loss
from .fsq_vae import HierarchicalFSQ
from .vq_vae import EMAVectorQuantizer

try:
    from vector_quantize_pytorch import GroupedResidualFSQ
except ImportError:  # pragma: no cover - verified by the dependency smoke check.
    GroupedResidualFSQ = None


@dataclass
class JointHumanCameraTokenizerOutput:
    human_recon: torch.Tensor
    camera_recon: torch.Tensor
    latent: torch.Tensor
    info: dict[str, torch.Tensor]


def _temporal_conv1d(
    input_dim: int,
    output_dim: int,
    *,
    kernel_size: int = 3,
    stride: int = 1,
    is_causal: bool = False,
) -> nn.Conv1d:
    assert is_causal is False
    return nn.Conv1d(input_dim, output_dim, kernel_size=kernel_size, stride=stride, padding=kernel_size // 2)


def _make_decoder(latent_dim: int, hidden_dim: int, output_dim: int, downsample: int, is_causal: bool) -> nn.Sequential:
    return nn.Sequential(
        nn.ConvTranspose1d(latent_dim, hidden_dim, kernel_size=downsample, stride=downsample),
        nn.SiLU(),
        _temporal_conv1d(hidden_dim, hidden_dim, is_causal=is_causal),
        nn.SiLU(),
        nn.Conv1d(hidden_dim, output_dim, kernel_size=1),
    )


def _make_encoder(input_dim: int, latent_dim: int, hidden_dim: int, downsample: int, is_causal: bool) -> nn.Sequential:
    return nn.Sequential(
        _temporal_conv1d(input_dim, hidden_dim, is_causal=is_causal),
        nn.SiLU(),
        _temporal_conv1d(hidden_dim, latent_dim, stride=downsample, is_causal=is_causal),
    )


def _make_vae_encoder(input_dim: int, hidden_dim: int, downsample: int, is_causal: bool) -> nn.Sequential:
    return nn.Sequential(
        _temporal_conv1d(input_dim, hidden_dim, is_causal=is_causal),
        nn.SiLU(),
        _temporal_conv1d(hidden_dim, hidden_dim, stride=downsample, is_causal=is_causal),
        nn.SiLU(),
    )


def _residual_activation(name: str) -> nn.Module:
    if name == "relu":
        return nn.ReLU()
    if name == "gelu":
        return nn.GELU()
    if name in {"silu", "swish"}:
        return nn.SiLU()
    raise ValueError(f"unsupported residual activation: {name}")


class _ResidualConv1dBlock(nn.Module):
    """Non-causal MARDM-style dilated residual block."""

    def __init__(
        self,
        channels: int,
        *,
        dilation: int,
        activation: str,
        dropout: float,
        is_causal: bool,
    ) -> None:
        super().__init__()
        assert is_causal is False
        self.activation1 = _residual_activation(activation)
        self.activation2 = _residual_activation(activation)
        self.conv1 = nn.Conv1d(channels, channels, kernel_size=3, padding=dilation, dilation=dilation)
        self.conv2 = nn.Conv1d(channels, channels, kernel_size=1)
        self.dropout = nn.Dropout(dropout)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        residual = value
        value = self.conv1(self.activation1(value))
        value = self.conv2(self.activation2(value))
        return residual + self.dropout(value)


def _residual_stack(
    channels: int,
    *,
    depth: int,
    dilation_growth_rate: int,
    activation: str,
    dropout: float,
    is_causal: bool,
) -> nn.Sequential:
    blocks = [
        _ResidualConv1dBlock(
            channels,
            dilation=dilation_growth_rate**index,
            activation=activation,
            dropout=dropout,
            is_causal=is_causal,
        )
        for index in range(depth)
    ]
    return nn.Sequential(*reversed(blocks))


def _downsample_stages(downsample: int) -> int:
    if downsample <= 0 or downsample & (downsample - 1):
        raise ValueError("AAMMARDM-style downsample must be a positive power of two")
    return int(math.log2(downsample))


class _ResidualEncoder(nn.Module):
    def __init__(
        self,
        input_dim: int,
        latent_dim: int,
        width: int,
        downsample: int,
        depth: int,
        dilation_growth_rate: int,
        activation: str,
        dropout: float,
        is_causal: bool,
    ) -> None:
        super().__init__()
        assert is_causal is False
        self.in_conv = nn.Sequential(nn.Conv1d(input_dim, width, kernel_size=3, padding=1), _residual_activation(activation))
        self.down_blocks = nn.Sequential(
            *[
                nn.Sequential(
                    nn.Conv1d(width, width, kernel_size=4, stride=2, padding=1),
                    _residual_stack(
                        width,
                        depth=depth,
                        dilation_growth_rate=dilation_growth_rate,
                        activation=activation,
                        dropout=dropout,
                        is_causal=is_causal,
                    ),
                )
                for _ in range(_downsample_stages(downsample))
            ]
        )
        self.bottleneck = nn.Conv1d(width, latent_dim, kernel_size=3, padding=1)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.bottleneck(self.down_blocks(self.in_conv(value)))


class _ResidualDecoder(nn.Module):
    def __init__(
        self,
        latent_dim: int,
        output_dim: int,
        width: int,
        downsample: int,
        depth: int,
        dilation_growth_rate: int,
        activation: str,
        dropout: float,
        is_causal: bool,
    ) -> None:
        super().__init__()
        assert is_causal is False
        self.in_conv = nn.Sequential(nn.Conv1d(latent_dim, width, kernel_size=3, padding=1), nn.ReLU())
        self.up_blocks = nn.Sequential(
            *[
                nn.Sequential(
                    _residual_stack(
                        width,
                        depth=depth,
                        dilation_growth_rate=dilation_growth_rate,
                        activation=activation,
                        dropout=dropout,
                        is_causal=is_causal,
                    ),
                    nn.Upsample(scale_factor=2, mode="nearest"),
                    nn.Conv1d(width, width, kernel_size=3, padding=1),
                )
                for _ in range(_downsample_stages(downsample))
            ]
        )
        self.out_conv = nn.Sequential(
            nn.Conv1d(width, width, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(width, output_dim, kernel_size=3, padding=1),
        )

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.out_conv(self.up_blocks(self.in_conv(value)))


class _JointHumanCameraAE(nn.Module):
    """Pulp-style joint encoder with branch-specific human/camera decoders."""

    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int,
        camera_latent_dim: int,
        hidden_dim: int,
        downsample: int,
        commitment_weight: float,
        human_recon_weight: float,
        camera_recon_weight: float,
        velocity_weight: float,
        build_encoder: bool = True,
        is_causal: bool = False,
    ) -> None:
        super().__init__()
        if downsample <= 0:
            raise ValueError("downsample must be positive")
        if human_latent_dim <= 0 or camera_latent_dim <= 0:
            raise ValueError("human and camera latent dims must be positive")
        self.human_dim = int(human_dim)
        self.camera_dim = int(camera_dim)
        self.human_latent_dim = int(human_latent_dim)
        self.camera_latent_dim = int(camera_latent_dim)
        self.latent_dim = self.human_latent_dim + self.camera_latent_dim
        self.downsample = int(downsample)
        self.commitment_weight = float(commitment_weight)
        self.human_recon_weight = float(human_recon_weight)
        self.camera_recon_weight = float(camera_recon_weight)
        self.velocity_weight = float(velocity_weight)
        assert is_causal is False
        self.is_causal = False
        self.human_velocity_weight = float(velocity_weight)
        self.camera_velocity_weight = float(velocity_weight)
        self.human_acceleration_weight = 0.0
        self.camera_acceleration_weight = 0.0
        self.human_yaw_weight = 0.0
        self.human_root_weight = 0.0
        if build_encoder:
            self.encoder = _make_encoder(self.human_dim + self.camera_dim, self.latent_dim, hidden_dim, downsample, self.is_causal)
        self.human_decoder = _make_decoder(self.human_latent_dim, hidden_dim, self.human_dim, downsample, self.is_causal)
        self.camera_decoder = _make_decoder(self.camera_latent_dim, hidden_dim, self.camera_dim, downsample, self.is_causal)

    def _check_inputs(self, human: torch.Tensor, camera: torch.Tensor) -> None:
        if human.ndim != 3:
            raise ValueError(f"expected human [B,T,D], got {tuple(human.shape)}")
        if camera.ndim != 3:
            raise ValueError(f"expected camera [B,T,D], got {tuple(camera.shape)}")
        if human.shape[:2] != camera.shape[:2]:
            raise ValueError(f"human/camera batch-time mismatch: {tuple(human.shape)} vs {tuple(camera.shape)}")
        if human.shape[-1] != self.human_dim:
            raise ValueError(f"expected human dim {self.human_dim}, got {human.shape[-1]}")
        if camera.shape[-1] != self.camera_dim:
            raise ValueError(f"expected camera dim {self.camera_dim}, got {camera.shape[-1]}")

    def _encoder_latent(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        self._check_inputs(human, camera)
        x = torch.cat([human, camera], dim=-1)
        return self.encoder(x.transpose(1, 2)).transpose(1, 2)

    def _split_latent(self, latent: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if latent.ndim != 3:
            raise ValueError(f"expected latent [B,T,C], got {tuple(latent.shape)}")
        if latent.shape[-1] != self.latent_dim:
            raise ValueError(f"expected joint latent dim {self.latent_dim}, got {latent.shape[-1]}")
        # Match PulpMotion's camera-first joint latent layout while keeping branch-specific decoders.
        camera_latent = latent[..., : self.camera_latent_dim]
        human_latent = latent[..., self.camera_latent_dim :]
        return human_latent, camera_latent

    def decode(self, latent: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        human_latent, camera_latent = self._split_latent(latent)
        human = self.human_decoder(human_latent.transpose(1, 2)).transpose(1, 2)
        camera = self.camera_decoder(camera_latent.transpose(1, 2)).transpose(1, 2)
        if target_len is not None:
            human = human[:, :target_len]
            camera = camera[:, :target_len]
        return human, camera

    def forward(self, human: torch.Tensor, camera: torch.Tensor) -> JointHumanCameraTokenizerOutput:
        latent, info = self.encode(human, camera)
        human_recon, camera_recon = self.decode(latent, target_len=human.shape[1])
        return JointHumanCameraTokenizerOutput(human_recon=human_recon, camera_recon=camera_recon, latent=latent, info=info)

    def _branch_reconstruction_losses(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None,
    ) -> dict[str, torch.Tensor]:
        loss_human = human
        loss_human_recon = output.human_recon
        loss_camera = camera
        loss_camera_recon = output.camera_recon
        human_mean = getattr(self, "loss_human_mean", None)
        human_std = getattr(self, "loss_human_std", None)
        camera_mean = getattr(self, "loss_camera_mean", None)
        camera_std = getattr(self, "loss_camera_std", None)
        if human_mean is not None and human_std is not None:
            loss_human = (human - human_mean.to(human)) / human_std.to(human)
            loss_human_recon = (output.human_recon - human_mean.to(output.human_recon)) / human_std.to(output.human_recon)
        if camera_mean is not None and camera_std is not None:
            loss_camera = (camera - camera_mean.to(camera)) / camera_std.to(camera)
            loss_camera_recon = (output.camera_recon - camera_mean.to(output.camera_recon)) / camera_std.to(output.camera_recon)
            if loss_camera.ndim >= 3:
                loss_camera = loss_camera.clone()
                loss_camera_recon = loss_camera_recon.clone()
                loss_camera[..., 0, 11:14] = 0.0
                loss_camera_recon[..., 0, 11:14] = 0.0
            else:
                loss_camera = loss_camera.clone()
                loss_camera_recon = loss_camera_recon.clone()
                loss_camera[0, 11:14] = 0.0
                loss_camera_recon[0, 11:14] = 0.0
        human_recon_loss = masked_smooth_l1_loss(loss_human_recon, loss_human, mask)
        camera_recon_loss = masked_smooth_l1_loss(loss_camera_recon, loss_camera, mask)
        human_velocity_loss = temporal_diff_loss(loss_human_recon, loss_human, mask)
        camera_velocity_loss = temporal_diff_loss(loss_camera_recon, loss_camera, mask)
        human_acceleration_loss = temporal_accel_loss(loss_human_recon, loss_human, mask)
        camera_acceleration_loss = temporal_accel_loss(loss_camera_recon, loss_camera, mask)
        human_yaw_loss, human_root_loss = self._human_root_geometry_losses(human, output.human_recon, mask)
        weighted_human_recon_loss = self.human_recon_weight * human_recon_loss
        weighted_camera_recon_loss = self.camera_recon_weight * camera_recon_loss
        weighted_human_velocity_loss = self.human_velocity_weight * human_velocity_loss
        weighted_camera_velocity_loss = self.camera_velocity_weight * camera_velocity_loss
        weighted_human_acceleration_loss = self.human_acceleration_weight * human_acceleration_loss
        weighted_camera_acceleration_loss = self.camera_acceleration_weight * camera_acceleration_loss
        weighted_human_yaw_loss = self.human_yaw_weight * human_yaw_loss
        weighted_human_root_loss = self.human_root_weight * human_root_loss
        weighted_velocity_loss = weighted_human_velocity_loss + weighted_camera_velocity_loss
        weighted_acceleration_loss = weighted_human_acceleration_loss + weighted_camera_acceleration_loss
        return {
            "human_recon_loss": human_recon_loss,
            "camera_recon_loss": camera_recon_loss,
            "human_velocity_loss": human_velocity_loss,
            "camera_velocity_loss": camera_velocity_loss,
            "human_acceleration_loss": human_acceleration_loss,
            "camera_acceleration_loss": camera_acceleration_loss,
            "weighted_human_recon_loss": weighted_human_recon_loss,
            "weighted_camera_recon_loss": weighted_camera_recon_loss,
            "weighted_human_velocity_loss": weighted_human_velocity_loss,
            "weighted_camera_velocity_loss": weighted_camera_velocity_loss,
            "weighted_velocity_loss": weighted_velocity_loss,
            "weighted_human_acceleration_loss": weighted_human_acceleration_loss,
            "weighted_camera_acceleration_loss": weighted_camera_acceleration_loss,
            "weighted_acceleration_loss": weighted_acceleration_loss,
            "human_yaw_loss": human_yaw_loss,
            "human_root_loss": human_root_loss,
            "weighted_human_yaw_loss": weighted_human_yaw_loss,
            "weighted_human_root_loss": weighted_human_root_loss,
        }

    def _human_root_geometry_losses(
        self,
        human: torch.Tensor,
        human_recon: torch.Tensor,
        mask: torch.Tensor | None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        mean = getattr(self, "geometry_human_mean", None)
        std = getattr(self, "geometry_human_std", None)
        if mean is None or std is None:
            zero = human_recon.new_tensor(0.0)
            return zero, zero
        if human.shape[-1] != 199:
            raise ValueError("human root geometry loss requires Pulp human199 features")

        mean = mean.to(human)
        std = std.to(human)
        human_raw = human * std + mean
        recon_raw = human_recon * std + mean
        target_yaw = torch.cumsum(human_raw[..., 3], dim=1)
        recon_yaw = torch.cumsum(recon_raw[..., 3], dim=1)
        yaw_loss = masked_mean(1.0 - torch.cos(recon_yaw - target_yaw), mask)

        def root_xy(features: torch.Tensor, yaw: torch.Tensor) -> torch.Tensor:
            velocity = features[..., 1:3]
            cosine = torch.cos(yaw)
            sine = torch.sin(yaw)
            world_velocity = torch.stack(
                (
                    cosine * velocity[..., 0] - sine * velocity[..., 1],
                    sine * velocity[..., 0] + cosine * velocity[..., 1],
                ),
                dim=-1,
            )
            integrated = torch.cumsum(world_velocity[:, :-1], dim=1)
            return torch.cat((torch.zeros_like(world_velocity[:, :1]), integrated), dim=1)

        target_root = root_xy(human_raw, target_yaw)
        recon_root = root_xy(recon_raw, recon_yaw)
        root_loss = masked_smooth_l1_loss(recon_root, target_root, mask)
        return yaw_loss, root_loss

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **_: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        losses = self._branch_reconstruction_losses(human, camera, output, mask)
        commitment_loss = output.info["commitment_loss"]
        weighted_commitment_loss = self.commitment_weight * commitment_loss
        total = (
            losses["weighted_human_recon_loss"]
            + losses["weighted_camera_recon_loss"]
            + losses["weighted_velocity_loss"]
            + losses["weighted_acceleration_loss"]
            + losses["weighted_human_yaw_loss"]
            + losses["weighted_human_root_loss"]
            + weighted_commitment_loss
        )
        return {
            "total_loss": total,
            **losses,
            "weighted_commitment_loss": weighted_commitment_loss,
            "commitment_loss": commitment_loss,
            "perplexity": output.info["perplexity"],
            "active_codes": output.info["active_codes"],
            **{
                key: value
                for key, value in output.info.items()
                if key not in {"indices", "encoder_latent", "commitment_loss", "perplexity", "active_codes"}
                and isinstance(value, torch.Tensor)
                and value.ndim == 0
            },
        }


class JointHumanCameraVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        kl_weight: float = 1.0e-5,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 1.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight=0.0,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )
        self.kl_weight = float(kl_weight)
        self.encoder = _make_vae_encoder(self.human_dim + self.camera_dim, hidden_dim, downsample, self.is_causal)
        self.to_mu = nn.Conv1d(hidden_dim, self.latent_dim, kernel_size=1)
        self.to_logvar = nn.Conv1d(hidden_dim, self.latent_dim, kernel_size=1)

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        x = torch.cat([human, camera], dim=-1)
        h = self.encoder(x.transpose(1, 2))
        mu = self.to_mu(h).transpose(1, 2)
        logvar = self.to_logvar(h).transpose(1, 2).clamp(min=-20.0, max=20.0)
        if self.training:
            std = torch.exp(0.5 * logvar)
            latent = mu + torch.randn_like(std) * std
        else:
            latent = mu
        return latent, {"mu": mu, "logvar": logvar}

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **_: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        losses = self._branch_reconstruction_losses(human, camera, output, mask)
        mu = output.info["mu"]
        logvar = output.info["logvar"]
        kl_loss = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
        weighted_kl_loss = self.kl_weight * kl_loss
        total = (
            losses["weighted_human_recon_loss"]
            + losses["weighted_camera_recon_loss"]
            + losses["weighted_velocity_loss"]
            + losses["weighted_acceleration_loss"]
            + losses["weighted_human_yaw_loss"]
            + losses["weighted_human_root_loss"]
            + weighted_kl_loss
        )
        return {
            "total_loss": total,
            **losses,
            "kl_loss": kl_loss,
            "weighted_kl_loss": weighted_kl_loss,
        }

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        latent, info = self.encode(human, camera)
        return info["mu"] if not self.training else latent

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(tokens, target_len=target_len)


class JointHumanCameraAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 1.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight=0.0,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
        )

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        return self._encoder_latent(human, camera), {}

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **_: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        losses = self._branch_reconstruction_losses(human, camera, output, mask)
        total = (
            losses["weighted_human_recon_loss"]
            + losses["weighted_camera_recon_loss"]
            + losses["weighted_velocity_loss"]
            + losses["weighted_acceleration_loss"]
            + losses["weighted_human_yaw_loss"]
            + losses["weighted_human_root_loss"]
        )
        return {
            "total_loss": total,
            **losses,
        }

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        latent, _ = self.encode(human, camera)
        return latent

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(tokens, target_len=target_len)


class AAMMARDMResidualJointHumanCameraAE(_JointHumanCameraAE):
    """Projection-free AAMMARDM-style joint AE with branch-owning decoders."""

    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 192,
        downsample: int = 4,
        residual_depth: int = 2,
        dilation_growth_rate: int = 3,
        residual_activation: str = "relu",
        residual_dropout: float = 0.2,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 1.0,
        is_causal: bool = False,
    ) -> None:
        assert is_causal is False
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight=0.0,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            build_encoder=False,
            is_causal=is_causal,
        )
        common = {
            "width": hidden_dim,
            "downsample": downsample,
            "depth": residual_depth,
            "dilation_growth_rate": dilation_growth_rate,
            "activation": residual_activation,
            "dropout": residual_dropout,
            "is_causal": is_causal,
        }
        self.encoder = _ResidualEncoder(
            self.human_dim + self.camera_dim,
            self.latent_dim,
            **common,
        )
        self.human_decoder = _ResidualDecoder(
            self.human_latent_dim,
            self.human_dim,
            **common,
        )
        self.camera_decoder = _ResidualDecoder(
            self.camera_latent_dim,
            self.camera_dim,
            **common,
        )
        self.residual_depth = int(residual_depth)
        self.dilation_growth_rate = int(dilation_growth_rate)
        self.residual_activation = str(residual_activation)
        self.residual_dropout = float(residual_dropout)

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        value = torch.cat([human, camera], dim=-1).transpose(1, 2)
        right_pad = (-human.shape[1]) % self.downsample
        if right_pad:
            value = F.pad(value, (0, right_pad))
        return self.encoder(value).transpose(1, 2), {"right_pad_frames": human.new_tensor(right_pad)}

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **_: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        losses = self._branch_reconstruction_losses(human, camera, output, mask)
        total = (
            losses["weighted_human_recon_loss"]
            + losses["weighted_camera_recon_loss"]
            + losses["weighted_velocity_loss"]
            + losses["weighted_acceleration_loss"]
            + losses["weighted_human_yaw_loss"]
            + losses["weighted_human_root_loss"]
        )
        return {"total_loss": total, **losses}

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        latent, _ = self.encode(human, camera)
        return latent

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(tokens, target_len=target_len)


class JointHumanCameraVQVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 448,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        codebook_size: int = 512,
        downsample: int = 4,
        commitment_weight: float = 0.02,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 0.5,
        ema_decay: float = 0.99,
        is_causal: bool = False,
    ) -> None:
        super().__init__(human_dim, camera_dim, human_latent_dim, camera_latent_dim, hidden_dim, downsample, commitment_weight, human_recon_weight, camera_recon_weight, velocity_weight, is_causal=is_causal)
        self.quantizer = EMAVectorQuantizer(codebook_size, self.latent_dim, decay=ema_decay)

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        z_e = self._encoder_latent(human, camera)
        z_q, info = self.quantizer(z_e)
        info["encoder_latent"] = z_e
        return z_q, info

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        _, info = self.encode(human, camera)
        return info["indices"]

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(self.quantizer.lookup(tokens), target_len=target_len)


class JointHumanCameraHFSQVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 448,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        levels: tuple[int, ...] = (8, 5, 5, 5),
        groups: int = 8,
        num_quantizers: int = 2,
        commitment_weight: float = 0.02,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 0.5,
        quantize_dropout_prob: float = 0.0,
        base_mask_rate: float = 0.0,
        r_rand_scale: float = 0.0,
        w_scale_division: bool = False,
        is_causal: bool = False,
    ) -> None:
        super().__init__(human_dim, camera_dim, human_latent_dim, camera_latent_dim, hidden_dim, downsample, commitment_weight, human_recon_weight, camera_recon_weight, velocity_weight, is_causal=is_causal)
        self.quantizer = HierarchicalFSQ(
            dim=self.latent_dim,
            levels=levels,
            groups=groups,
            num_quantizers=num_quantizers,
            quantize_dropout_prob=quantize_dropout_prob,
            base_mask_rate=base_mask_rate,
            r_rand_scale=r_rand_scale,
            w_scale_division=w_scale_division,
        )

    def _usage_stats(self, indices: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        valid = indices.reshape(-1)
        valid = valid[valid >= 0]
        if valid.numel() == 0:
            zero = torch.tensor(0.0, device=indices.device)
            return zero, zero
        counts = torch.bincount(valid, minlength=self.quantizer.codebook_size).to(dtype=torch.float32)
        probs = counts / counts.sum().clamp_min(1.0)
        perplexity = torch.exp(-(probs * (probs + 1.0e-7).log()).sum())
        active_codes = (counts > 0).sum().to(dtype=torch.float32)
        return perplexity, active_codes

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        z_e = self._encoder_latent(human, camera)
        z_q, indices, commitment_loss, metrics = self.quantizer(z_e)
        perplexity, active_codes = self._usage_stats(indices)
        info = {
            "indices": indices,
            "encoder_latent": z_e,
            "commitment_loss": commitment_loss,
            "perplexity": perplexity,
            "active_codes": active_codes,
        }
        for key, value in metrics.items():
            info[f"hfsq_{key}"] = value.mean()
        return z_q, info

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        _, info = self.encode(human, camera)
        return info["indices"]

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(self.quantizer.indices_to_output(tokens), target_len=target_len)

class JointHumanCameraGRFSQVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 448,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        levels: tuple[int, ...] = (8, 5, 5, 5),
        groups: int = 8,
        num_quantizers: int = 2,
        commitment_weight: float = 0.02,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 0.5,
        quantize_dropout_prob: float = 0.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(human_dim, camera_dim, human_latent_dim, camera_latent_dim, hidden_dim, downsample, commitment_weight, human_recon_weight, camera_recon_weight, velocity_weight, is_causal=is_causal)
        if GroupedResidualFSQ is None:
            raise ImportError("joint_grfsq requires the official vector-quantize-pytorch package")
        self.quantizer = GroupedResidualFSQ(
            dim=self.latent_dim,
            groups=groups,
            levels=list(levels),
            num_quantizers=num_quantizers,
            quantize_dropout=quantize_dropout_prob > 0.0,
        )

    def _usage_stats(self, indices: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        valid = indices.reshape(-1)
        valid = valid[valid >= 0]
        if valid.numel() == 0:
            zero = torch.tensor(0.0, device=indices.device)
            return zero, zero
        counts = torch.bincount(valid, minlength=self.quantizer.codebook_size).to(dtype=torch.float32)
        probs = counts / counts.sum().clamp_min(1.0)
        perplexity = torch.exp(-(probs * (probs + 1.0e-7).log()).sum())
        active_codes = (counts > 0).sum().to(dtype=torch.float32)
        return perplexity, active_codes

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        z_e = self._encoder_latent(human, camera)
        z_q, indices = self.quantizer(z_e)
        commitment_loss = F.mse_loss(z_e, z_q.detach())
        perplexity, active_codes = self._usage_stats(indices)
        return z_q, {
            "indices": indices,
            "encoder_latent": z_e,
            "commitment_loss": commitment_loss,
            "perplexity": perplexity,
            "active_codes": active_codes,
        }

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        _, info = self.encode(human, camera)
        return info["indices"]

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(self.quantizer.get_output_from_indices(tokens), target_len=target_len)


class SeparateHumanCameraVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        kl_weight: float = 1.0e-5,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 1.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight=0.0,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
            build_encoder=False,
        )
        self.kl_weight = float(kl_weight)
        self.human_encoder = _make_vae_encoder(self.human_dim, hidden_dim, downsample, self.is_causal)
        self.camera_encoder = _make_vae_encoder(self.camera_dim, hidden_dim, downsample, self.is_causal)
        self.human_to_mu = nn.Conv1d(hidden_dim, self.human_latent_dim, kernel_size=1)
        self.human_to_logvar = nn.Conv1d(hidden_dim, self.human_latent_dim, kernel_size=1)
        self.camera_to_mu = nn.Conv1d(hidden_dim, self.camera_latent_dim, kernel_size=1)
        self.camera_to_logvar = nn.Conv1d(hidden_dim, self.camera_latent_dim, kernel_size=1)

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        human_h = self.human_encoder(human.transpose(1, 2))
        camera_h = self.camera_encoder(camera.transpose(1, 2))
        human_mu = self.human_to_mu(human_h).transpose(1, 2)
        human_logvar = self.human_to_logvar(human_h).transpose(1, 2).clamp(min=-20.0, max=20.0)
        camera_mu = self.camera_to_mu(camera_h).transpose(1, 2)
        camera_logvar = self.camera_to_logvar(camera_h).transpose(1, 2).clamp(min=-20.0, max=20.0)
        mu = torch.cat([camera_mu, human_mu], dim=-1)
        logvar = torch.cat([camera_logvar, human_logvar], dim=-1)
        if self.training:
            std = torch.exp(0.5 * logvar)
            latent = mu + torch.randn_like(std) * std
        else:
            latent = mu
        return latent, {"mu": mu, "logvar": logvar}

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **kwargs: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        return JointHumanCameraVAE.compute_loss(self, human, camera, output, mask=mask, **kwargs)

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        latent, info = self.encode(human, camera)
        return info["mu"] if not self.training else latent

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(tokens, target_len=target_len)


class SeparateHumanCameraAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 1.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight=0.0,
            human_recon_weight=human_recon_weight,
            camera_recon_weight=camera_recon_weight,
            velocity_weight=velocity_weight,
            is_causal=is_causal,
            build_encoder=False,
        )
        self.human_encoder = _make_encoder(self.human_dim, self.human_latent_dim, hidden_dim, downsample, self.is_causal)
        self.camera_encoder = _make_encoder(self.camera_dim, self.camera_latent_dim, hidden_dim, downsample, self.is_causal)

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        human_latent = self.human_encoder(human.transpose(1, 2)).transpose(1, 2)
        camera_latent = self.camera_encoder(camera.transpose(1, 2)).transpose(1, 2)
        return torch.cat([camera_latent, human_latent], dim=-1), {}

    def compute_loss(
        self,
        human: torch.Tensor,
        camera: torch.Tensor,
        output: JointHumanCameraTokenizerOutput,
        mask: torch.Tensor | None = None,
        **kwargs: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        return JointHumanCameraAE.compute_loss(self, human, camera, output, mask=mask, **kwargs)

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        latent, _ = self.encode(human, camera)
        return latent

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        return self.decode(tokens, target_len=target_len)


class SeparateHumanCameraGRFSQVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        levels: tuple[int, ...] = (8, 5, 5, 5),
        groups: int = 8,
        num_quantizers: int = 2,
        commitment_weight: float = 0.02,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 0.5,
        quantize_dropout_prob: float = 0.0,
        is_causal: bool = False,
    ) -> None:
        super().__init__(human_dim, camera_dim, human_latent_dim, camera_latent_dim, hidden_dim, downsample, commitment_weight, human_recon_weight, camera_recon_weight, velocity_weight, build_encoder=False, is_causal=is_causal)
        if GroupedResidualFSQ is None:
            raise ImportError("separate_grfsq requires the official vector-quantize-pytorch package")
        self.human_encoder = _make_encoder(self.human_dim, self.human_latent_dim, hidden_dim, downsample, self.is_causal)
        self.camera_encoder = _make_encoder(self.camera_dim, self.camera_latent_dim, hidden_dim, downsample, self.is_causal)
        self.human_quantizer = GroupedResidualFSQ(
            dim=self.human_latent_dim,
            groups=groups,
            levels=list(levels),
            num_quantizers=num_quantizers,
            quantize_dropout=quantize_dropout_prob > 0.0,
        )
        self.camera_quantizer = GroupedResidualFSQ(
            dim=self.camera_latent_dim,
            groups=groups,
            levels=list(levels),
            num_quantizers=num_quantizers,
            quantize_dropout=quantize_dropout_prob > 0.0,
        )
        self.codebook_size = self.human_quantizer.codebook_size

    def _usage_stats(self, human_indices: torch.Tensor, camera_indices: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        valid = torch.cat([human_indices.reshape(-1), camera_indices.reshape(-1)], dim=0)
        valid = valid[valid >= 0]
        if valid.numel() == 0:
            zero = torch.tensor(0.0, device=human_indices.device)
            return zero, zero
        counts = torch.bincount(valid, minlength=self.codebook_size).to(dtype=torch.float32)
        probs = counts / counts.sum().clamp_min(1.0)
        perplexity = torch.exp(-(probs * (probs + 1.0e-7).log()).sum())
        active_codes = (counts > 0).sum().to(dtype=torch.float32)
        return perplexity, active_codes

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        human_z_e = self.human_encoder(human.transpose(1, 2)).transpose(1, 2)
        camera_z_e = self.camera_encoder(camera.transpose(1, 2)).transpose(1, 2)
        human_z_q, human_indices = self.human_quantizer(human_z_e)
        camera_z_q, camera_indices = self.camera_quantizer(camera_z_e)
        z_e = torch.cat([camera_z_e, human_z_e], dim=-1)
        z_q = torch.cat([camera_z_q, human_z_q], dim=-1)
        commitment_loss = F.mse_loss(z_e, z_q.detach())
        perplexity, active_codes = self._usage_stats(human_indices, camera_indices)
        return z_q, {
            "indices": torch.stack([camera_indices, human_indices], dim=0),
            "encoder_latent": z_e,
            "commitment_loss": commitment_loss,
            "perplexity": perplexity,
            "active_codes": active_codes,
        }

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        _, info = self.encode(human, camera)
        return info["indices"]

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        if tokens.ndim < 2 or tokens.shape[0] != 2:
            raise ValueError(f"expected separate tokens [2,G,B,T,Q], got {tuple(tokens.shape)}")
        camera_latent = self.camera_quantizer.get_output_from_indices(tokens[0])
        human_latent = self.human_quantizer.get_output_from_indices(tokens[1])
        return self.decode(torch.cat([camera_latent, human_latent], dim=-1), target_len=target_len)


class SeparateHumanCameraHFSQVAE(_JointHumanCameraAE):
    def __init__(
        self,
        human_dim: int,
        camera_dim: int,
        human_latent_dim: int = 128,
        camera_latent_dim: int = 64,
        hidden_dim: int = 256,
        downsample: int = 4,
        levels: tuple[int, ...] = (8, 5, 5, 5),
        groups: int = 8,
        num_quantizers: int = 2,
        commitment_weight: float = 0.02,
        human_recon_weight: float = 1.0,
        camera_recon_weight: float = 1.0,
        velocity_weight: float = 0.5,
        quantize_dropout_prob: float = 0.0,
        base_mask_rate: float = 0.0,
        r_rand_scale: float = 0.0,
        w_scale_division: bool = False,
        is_causal: bool = False,
    ) -> None:
        super().__init__(
            human_dim,
            camera_dim,
            human_latent_dim,
            camera_latent_dim,
            hidden_dim,
            downsample,
            commitment_weight,
            human_recon_weight,
            camera_recon_weight,
            velocity_weight,
            build_encoder=False,
            is_causal=is_causal,
        )
        self.human_encoder = _make_encoder(self.human_dim, self.human_latent_dim, hidden_dim, downsample, self.is_causal)
        self.camera_encoder = _make_encoder(self.camera_dim, self.camera_latent_dim, hidden_dim, downsample, self.is_causal)
        self.human_quantizer = HierarchicalFSQ(
            dim=self.human_latent_dim,
            levels=levels,
            groups=groups,
            num_quantizers=num_quantizers,
            quantize_dropout_prob=quantize_dropout_prob,
            base_mask_rate=base_mask_rate,
            r_rand_scale=r_rand_scale,
            w_scale_division=w_scale_division,
        )
        self.camera_quantizer = HierarchicalFSQ(
            dim=self.camera_latent_dim,
            levels=levels,
            groups=groups,
            num_quantizers=num_quantizers,
            quantize_dropout_prob=quantize_dropout_prob,
            base_mask_rate=base_mask_rate,
            r_rand_scale=r_rand_scale,
            w_scale_division=w_scale_division,
        )
        self.codebook_size = self.human_quantizer.codebook_size

    def _usage_stats(self, human_indices: torch.Tensor, camera_indices: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        valid = torch.cat([human_indices.reshape(-1), camera_indices.reshape(-1)], dim=0)
        valid = valid[valid >= 0]
        if valid.numel() == 0:
            zero = torch.tensor(0.0, device=human_indices.device)
            return zero, zero
        counts = torch.bincount(valid, minlength=self.codebook_size).to(dtype=torch.float32)
        probs = counts / counts.sum().clamp_min(1.0)
        perplexity = torch.exp(-(probs * (probs + 1.0e-7).log()).sum())
        active_codes = (counts > 0).sum().to(dtype=torch.float32)
        return perplexity, active_codes

    def encode(self, human: torch.Tensor, camera: torch.Tensor) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        self._check_inputs(human, camera)
        human_z_e = self.human_encoder(human.transpose(1, 2)).transpose(1, 2)
        camera_z_e = self.camera_encoder(camera.transpose(1, 2)).transpose(1, 2)
        human_z_q, human_indices, _, human_metrics = self.human_quantizer(human_z_e)
        camera_z_q, camera_indices, _, camera_metrics = self.camera_quantizer(camera_z_e)
        z_e = torch.cat([camera_z_e, human_z_e], dim=-1)
        z_q = torch.cat([camera_z_q, human_z_q], dim=-1)
        commitment_loss = F.mse_loss(z_e, z_q.detach())
        perplexity, active_codes = self._usage_stats(human_indices, camera_indices)
        info = {
            "indices": torch.stack([camera_indices, human_indices], dim=0),
            "encoder_latent": z_e,
            "commitment_loss": commitment_loss,
            "perplexity": perplexity,
            "active_codes": active_codes,
        }
        for key, value in human_metrics.items():
            info[f"human_hfsq_{key}"] = value.mean()
        for key, value in camera_metrics.items():
            info[f"camera_hfsq_{key}"] = value.mean()
        return z_q, info

    def tokenize(self, human: torch.Tensor, camera: torch.Tensor) -> torch.Tensor:
        _, info = self.encode(human, camera)
        return info["indices"]

    def detokenize(self, tokens: torch.Tensor, target_len: int | None = None) -> tuple[torch.Tensor, torch.Tensor]:
        if tokens.ndim < 2 or tokens.shape[0] != 2:
            raise ValueError(f"expected separate HFSQ tokens [2,G,Q,B,T], got {tuple(tokens.shape)}")
        camera_latent = self.camera_quantizer.indices_to_output(tokens[0])
        human_latent = self.human_quantizer.indices_to_output(tokens[1])
        return self.decode(torch.cat([camera_latent, human_latent], dim=-1), target_len=target_len)
