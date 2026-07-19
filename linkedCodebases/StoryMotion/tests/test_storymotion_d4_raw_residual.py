from __future__ import annotations

import math
import sys
from pathlib import Path

import torch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from storymotion_d4_raw_residual import camera_residual_records, correlation  # noqa: E402


def test_camera_residual_records_excludes_invalid_frames() -> None:
    target = torch.tensor([[[99.0, 99.0, 99.0], [1.0, 2.0, 1000.0], [2.0, 4.0, -1000.0]]])
    prediction = target.clone()
    prediction[0, 1, :2] += torch.tensor([1.0, -1.0])
    prediction[0, 2, :2] += torch.tensor([2.0, -2.0])
    prediction[0, 1:, 2] += 1.0e6
    valid = torch.tensor([[True, True, False]])

    record = camera_residual_records(prediction, target, valid, camera_start=1)[0]

    assert record["valid_latent_frames"] == 2
    assert record["channel"]["signed_mean"] == [0.0, 0.0]
    assert record["channel"]["rms"] == [1.0, 2.0]
    assert math.isclose(record["sample"]["rms"], math.sqrt(2.5))
    assert math.isclose(record["sample"]["mae"], 1.5)


def test_correlation_reports_pearson_and_rank_association() -> None:
    result = correlation([1.0, 2.0, 3.0], [2.0, 4.0, 8.0])

    assert result["count"] == 3
    assert 0.9 < result["pearson"] < 1.0
    assert math.isclose(result["spearman"], 1.0)


def test_correlation_returns_null_for_constant_input() -> None:
    result = correlation([1.0, 1.0, 1.0], [1.0, 2.0, 3.0])

    assert result == {"count": 3, "pearson": None, "spearman": None}
