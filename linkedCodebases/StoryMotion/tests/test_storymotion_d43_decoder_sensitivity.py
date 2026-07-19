from __future__ import annotations

import math
import sys
from pathlib import Path

import torch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from storymotion_d43_decoder_sensitivity import (  # noqa: E402
    camera_directions,
    camera_geometry_objectives,
    gradient_alignment,
    jvp_camera_metrics,
    latent_stats_file_audit,
    reproduction_failures,
)


def test_camera_directions_are_masked_unit_rms_and_orthogonal() -> None:
    residual = torch.arange(1, 17, dtype=torch.float32).reshape(1, 2, 8)
    valid = torch.tensor([[True, True, True, False, False, False, False, False]])

    directions, rms = camera_directions(residual, valid, [123])

    actual = directions["actual_residual"]
    random = directions["random_orthogonal"]
    assert torch.count_nonzero(actual[..., 3:]) == 0
    assert torch.count_nonzero(random[..., 3:]) == 0
    assert math.isclose(float(actual[..., :3].square().mean()), 1.0, rel_tol=1e-6)
    assert math.isclose(float(random[..., :3].square().mean()), 1.0, rel_tol=1e-6)
    assert abs(float((actual * random).sum())) < 1.0e-5
    assert float(rms[0]) > 0.0


def test_camera_geometry_objectives_use_valid_frames_and_geodesic_rotation() -> None:
    reference = torch.eye(4).reshape(1, 1, 4, 4).repeat(1, 3, 1, 1)
    prediction = reference.clone()
    prediction[0, :2, 0, 3] = torch.tensor([1.0, 3.0])
    prediction[0, 2, 0, 3] = 1000.0
    rotation = torch.tensor(
        [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    )
    prediction[0, :2, :3, :3] = rotation
    valid = torch.tensor([[True, True, False]])

    objectives = camera_geometry_objectives(prediction, reference, valid)

    assert math.isclose(float(objectives["camera_center_ade_m"]), 2.0)
    assert math.isclose(float(objectives["camera_center_fde_m"]), 3.0)
    assert math.isclose(
        float(objectives["camera_rotation_mean_rad"]), math.pi / 2, rel_tol=1e-6
    )


def test_jvp_metrics_report_center_and_rotation_tangent_gain() -> None:
    base = torch.eye(4).reshape(1, 1, 4, 4).repeat(1, 2, 1, 1)
    jvp = torch.zeros_like(base)
    jvp[0, :, 0, 3] = 1.0
    jvp[0, :, 0, 1] = -1.0
    jvp[0, :, 1, 0] = 1.0
    valid = torch.tensor([[True, True]])

    metrics = jvp_camera_metrics(base, jvp, valid)[0]

    assert math.isclose(metrics["camera_center_rms_gain_m"], 1.0)
    assert math.isclose(metrics["camera_center_fde_gain_m"], 1.0)
    assert math.isclose(
        metrics["camera_rotation_tangent_mean_deg"], 180.0 / math.pi, rel_tol=1.0e-6
    )


def test_gradient_alignment_cosine_tracks_actual_direction() -> None:
    gradient = torch.tensor([[[1.0, 2.0], [3.0, 4.0]]])
    direction = gradient.clone()
    valid = torch.tensor([[True, False]])

    record = gradient_alignment(gradient, direction, valid)[0]

    assert math.isclose(record["cosine_to_actual_residual"], 1.0, rel_tol=1e-6)
    assert record["directional_derivative"] == 10.0


def test_cross_host_reproduction_tolerance_is_predeclared() -> None:
    accepted = {
        "decoder_input_residual_rms": 1.998e-4,
        "camera_center_ade": 3.558e-3,
        "camera_center_fde": 3.558e-3,
        "camera_rotation_deg": 4.186e-2,
    }
    assert reproduction_failures(accepted) == {}

    rejected = dict(accepted)
    rejected["camera_center_ade"] = 5.001e-3
    assert reproduction_failures(rejected) == {"camera_center_ade": 5.001e-3}


def test_stats_reserialization_mismatch_requires_explicit_acceptance() -> None:
    try:
        latent_stats_file_audit("actual", "parent", False)
    except RuntimeError as error:
        assert "provenance amendment" in str(error)
    else:
        raise AssertionError("mismatched stats hashes must fail closed")

    audit = latent_stats_file_audit("actual", "parent", True)
    assert audit == {
        "path_status": "accepted_parent_reserialization_mismatch",
        "actual_sha256": "actual",
        "parent_expected_sha256": "parent",
    }
