from __future__ import annotations

import torch

from storymotion.tokenizers.joint_human_camera import JointHumanCameraAE, JointHumanCameraTokenizerOutput


def test_human199_yaw_and_root_losses_are_masked_and_differentiable() -> None:
    model = JointHumanCameraAE(
        human_dim=199,
        camera_dim=14,
        human_latent_dim=8,
        camera_latent_dim=4,
        hidden_dim=16,
        downsample=1,
        velocity_weight=0.0,
    )
    model.human_yaw_weight = 2.0
    model.human_root_weight = 3.0
    model.geometry_human_mean = torch.zeros(199)
    model.geometry_human_std = torch.ones(199)

    human = torch.zeros(1, 4, 199)
    human[..., 1] = 1.0
    camera = torch.zeros(1, 4, 14)
    human_recon = human.clone()
    human_recon[..., 3] = 0.2
    human_recon[:, 3, 3] = 100.0
    human_recon.requires_grad_()
    output = JointHumanCameraTokenizerOutput(
        human_recon=human_recon,
        camera_recon=camera.clone(),
        latent=torch.zeros(1, 4, 12),
        info={},
    )
    mask = torch.tensor([[True, True, True, False]])

    losses = model.compute_loss(human, camera, output, mask=mask)

    assert losses["human_yaw_loss"] > 0
    assert losses["human_root_loss"] > 0
    assert torch.allclose(losses["weighted_human_yaw_loss"], 2.0 * losses["human_yaw_loss"])
    assert torch.allclose(losses["weighted_human_root_loss"], 3.0 * losses["human_root_loss"])
    losses["total_loss"].backward()
    assert human_recon.grad is not None
    assert torch.isfinite(human_recon.grad).all()
    assert human_recon.grad[:, :3, 3].abs().sum() > 0
    assert human_recon.grad[:, 3].abs().sum() == 0


def test_human199_geometry_losses_are_zero_for_exact_reconstruction() -> None:
    model = JointHumanCameraAE(199, 14, 8, 4, hidden_dim=16, downsample=1)
    model.human_yaw_weight = 1.0
    model.human_root_weight = 1.0
    model.geometry_human_mean = torch.zeros(199)
    model.geometry_human_std = torch.ones(199)
    human = torch.randn(2, 5, 199)
    camera = torch.randn(2, 5, 14)
    output = JointHumanCameraTokenizerOutput(
        human_recon=human.clone(),
        camera_recon=camera.clone(),
        latent=torch.zeros(2, 5, 12),
        info={},
    )

    losses = model.compute_loss(human, camera, output)

    assert losses["human_yaw_loss"] == 0
    assert losses["human_root_loss"] == 0


def test_default_zero_weights_preserve_the_existing_total() -> None:
    model = JointHumanCameraAE(199, 14, 8, 4, hidden_dim=16, downsample=1)
    human = torch.randn(2, 5, 199)
    camera = torch.randn(2, 5, 14)
    output = JointHumanCameraTokenizerOutput(
        human_recon=torch.randn_like(human),
        camera_recon=torch.randn_like(camera),
        latent=torch.zeros(2, 5, 12),
        info={},
    )

    losses = model.compute_loss(human, camera, output)
    previous_total = (
        losses["weighted_human_recon_loss"]
        + losses["weighted_camera_recon_loss"]
        + losses["weighted_velocity_loss"]
        + losses["weighted_acceleration_loss"]
    )

    assert losses["weighted_human_yaw_loss"] == 0
    assert losses["weighted_human_root_loss"] == 0
    assert torch.allclose(losses["total_loss"], previous_total)
