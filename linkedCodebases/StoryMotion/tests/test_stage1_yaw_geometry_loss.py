from __future__ import annotations

import torch

from storymotion.tokenizers.joint_human_camera import (
    AAMMARDMResidualJointHumanCameraAE,
    JointHumanCameraAE,
    JointHumanCameraTokenizerOutput,
)


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


def test_camera14_center_loss_uses_the_official_integrated_velocity_path() -> None:
    model = JointHumanCameraAE(199, 14, 8, 4, hidden_dim=16, downsample=1, velocity_weight=0.0)
    model.camera_center_weight = 2.0
    model.geometry_human_mean = torch.zeros(199)
    model.geometry_human_std = torch.ones(199)
    model.geometry_feature_contract = "human199_integrated_root_yaw"
    model.geometry_camera_velocity_mean = torch.zeros(3)
    model.geometry_camera_velocity_std = torch.ones(3)
    model.geometry_camera_distance_mean = torch.zeros(3)
    model.geometry_camera_distance_std = torch.ones(3)

    human = torch.zeros(1, 4, 199)
    camera = torch.zeros(1, 4, 14)
    camera_recon = camera.clone()
    camera_recon[:, 0, 11] = 0.25
    camera_recon[:, 3, 11] = 100.0
    camera_recon.requires_grad_()
    output = JointHumanCameraTokenizerOutput(
        human_recon=human.clone(),
        camera_recon=camera_recon,
        latent=torch.zeros(1, 4, 12),
        info={},
    )
    mask = torch.tensor([[True, True, True, False]])

    losses = model.compute_loss(human, camera, output, mask=mask)

    assert losses["camera_center_loss"] > 0
    assert torch.allclose(losses["weighted_camera_center_loss"], 2.0 * losses["camera_center_loss"])
    losses["total_loss"].backward()
    assert camera_recon.grad is not None
    assert camera_recon.grad[:, 0, 11].abs().sum() > 0
    assert camera_recon.grad[:, 3].abs().sum() == 0


def test_camera14_rotation_loss_is_masked_geodesic_and_differentiable() -> None:
    model = JointHumanCameraAE(
        199,
        14,
        8,
        4,
        hidden_dim=16,
        downsample=1,
        human_recon_weight=0.0,
        camera_recon_weight=0.0,
        velocity_weight=0.0,
    )
    model.camera_rotation_weight = 2.0
    human = torch.zeros(1, 4, 199)
    camera = torch.zeros(1, 4, 14)
    camera[..., 5:11] = torch.tensor([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    camera_recon = camera.clone()
    angle = torch.tensor(0.2)
    camera_recon[:, 1, 5:11] = torch.stack(
        (angle.cos(), angle.sin(), angle.new_tensor(0.0), -angle.sin(), angle.cos(), angle.new_tensor(0.0))
    )
    camera_recon[:, 3, 5:11] = 100.0
    camera_recon.requires_grad_()
    output = JointHumanCameraTokenizerOutput(
        human_recon=human.clone(),
        camera_recon=camera_recon,
        latent=torch.zeros(1, 4, 12),
        info={},
    )
    mask = torch.tensor([[True, True, True, False]])

    losses = model.compute_loss(human, camera, output, mask=mask)

    assert torch.allclose(losses["camera_rotation_loss"], angle / 3.0, atol=1.0e-6)
    assert torch.allclose(losses["weighted_camera_rotation_loss"], 2.0 * losses["camera_rotation_loss"])
    losses["total_loss"].backward()
    assert camera_recon.grad is not None
    assert torch.isfinite(camera_recon.grad).all()
    assert camera_recon.grad[:, 1, 5:11].abs().sum() > 0
    assert camera_recon.grad[:, 3].abs().sum() == 0


def test_human_horizon_loss_uses_each_samples_last_valid_frame() -> None:
    model = JointHumanCameraAE(
        199,
        14,
        8,
        4,
        hidden_dim=16,
        downsample=1,
        human_recon_weight=0.0,
        camera_recon_weight=0.0,
        velocity_weight=0.0,
    )
    model.human_yaw_weight = 1.0
    model.human_root_weight = 3.0
    model.human_horizon_weight = 2.0
    model.geometry_human_mean = torch.zeros(199)
    model.geometry_human_std = torch.ones(199)
    human = torch.zeros(1, 4, 199)
    camera = torch.zeros(1, 4, 14)
    human_recon = human.clone()
    human_recon[:, :3, 1] = 0.2
    human_recon[:, :3, 3] = 0.05
    human_recon[:, 3, :4] = 100.0
    human_recon.requires_grad_()
    output = JointHumanCameraTokenizerOutput(
        human_recon=human_recon,
        camera_recon=camera.clone(),
        latent=torch.zeros(1, 4, 12),
        info={},
    )
    mask = torch.tensor([[True, True, True, False]])

    losses = model.compute_loss(human, camera, output, mask=mask)

    expected = losses["human_horizon_yaw_loss"] + 3.0 * losses["human_horizon_root_loss"]
    assert losses["human_horizon_yaw_loss"] > 0
    assert losses["human_horizon_root_loss"] > 0
    assert torch.allclose(losses["human_horizon_loss"], expected)
    assert torch.allclose(losses["weighted_human_horizon_loss"], 2.0 * expected)
    losses["total_loss"].backward()
    assert human_recon.grad is not None
    assert torch.isfinite(human_recon.grad).all()
    assert human_recon.grad[:, :3, :4].abs().sum() > 0
    assert human_recon.grad[:, 3].abs().sum() == 0


def test_human_multi_horizon_loss_uses_relative_anchors_and_ignores_padding() -> None:
    model = JointHumanCameraAE(
        199,
        14,
        8,
        4,
        hidden_dim=16,
        downsample=1,
        human_recon_weight=0.0,
        camera_recon_weight=0.0,
        velocity_weight=0.0,
    )
    model.human_yaw_weight = 1.0
    model.human_root_weight = 3.0
    model.human_multi_horizon_weight = 2.0
    model.geometry_human_mean = torch.zeros(199)
    model.geometry_human_std = torch.ones(199)
    human = torch.zeros(2, 9, 199)
    camera = torch.zeros(2, 9, 14)
    human_recon = human.clone()
    human_recon[0, [1, 2, 3, 4], 0] = 0.5
    human_recon[0, 5:, 0] = 100.0
    human_recon[1, [2, 4, 6, 8], 0] = 0.5
    human_recon.requires_grad_()
    output = JointHumanCameraTokenizerOutput(
        human_recon=human_recon,
        camera_recon=camera.clone(),
        latent=torch.zeros(2, 9, 12),
        info={},
    )
    mask = torch.tensor(
        [[True, True, True, True, True, False, False, False, False], [True] * 9]
    )

    losses = model.compute_loss(human, camera, output, mask=mask)

    expected = (
        losses["human_multi_horizon_yaw_loss"]
        + 3.0 * losses["human_multi_horizon_root_loss"]
    )
    assert losses["human_multi_horizon_root_loss"] > 0
    assert losses["human_horizon_loss"] == 0
    assert torch.allclose(losses["human_multi_horizon_loss"], expected)
    assert torch.allclose(losses["weighted_human_multi_horizon_loss"], 2.0 * expected)
    expected_total = (
        losses["weighted_human_yaw_loss"]
        + losses["weighted_human_root_loss"]
        + losses["weighted_human_multi_horizon_loss"]
    )
    assert torch.allclose(losses["total_loss"], expected_total)
    losses["total_loss"].backward()
    assert human_recon.grad is not None
    assert torch.count_nonzero(human_recon.grad[0, 5:]) == 0
    assert set(torch.nonzero(human_recon.grad[0, :, 0], as_tuple=False).flatten().tolist()) == {1, 2, 3, 4}
    assert set(torch.nonzero(human_recon.grad[1, :, 0], as_tuple=False).flatten().tolist()) == {2, 4, 6, 8}


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
    assert losses["weighted_camera_center_loss"] == 0
    assert losses["weighted_camera_rotation_loss"] == 0
    assert losses["weighted_human_horizon_loss"] == 0
    assert losses["weighted_human_multi_horizon_loss"] == 0
    assert torch.allclose(losses["total_loss"], previous_total)


def test_v8_1b_residual_ae_preserves_non_multiple_sequence_lengths() -> None:
    for frames, expected_pad in ((65, 3), (67, 1)):
        model = AAMMARDMResidualJointHumanCameraAE(
            199,
            14,
            human_latent_dim=8,
            camera_latent_dim=4,
            hidden_dim=16,
            downsample=4,
        )
        human = torch.randn(2, frames, 199)
        camera = torch.randn(2, frames, 14)

        output = model(human, camera)
        losses = model.compute_loss(human, camera, output)

        assert model.is_causal is False
        assert output.human_recon.shape == human.shape
        assert output.camera_recon.shape == camera.shape
        assert output.latent.shape == (2, (frames + 3) // 4, 12)
        assert int(output.info["right_pad_frames"].item()) == expected_pad
        assert torch.isfinite(losses["total_loss"])


def test_v8_1b_residual_ae_rejects_causality() -> None:
    try:
        AAMMARDMResidualJointHumanCameraAE(199, 14, is_causal=True)
    except AssertionError:
        pass
    else:
        raise AssertionError("v8.1B must reject a causal tokenizer")
