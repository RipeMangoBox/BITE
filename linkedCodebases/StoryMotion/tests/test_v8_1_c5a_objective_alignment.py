from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import torch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from audit_v8_1_c5a_objective_alignment import (  # noqa: E402
    anchor_indices,
    batch_surrogates,
    evaluator_order_indices,
    paired_rank_bootstrap,
    rankdata,
    spearman,
    surrogate_values_from_decoded,
)


def test_evaluator_order_mapping_requires_equal_unique_identity_sets() -> None:
    assert evaluator_order_indices(["a", "b", "c"], ["c", "a", "b"]) == [2, 0, 1]
    for manifest, evaluator in ((["a", "a"], ["a", "b"]), (["a", "b"], ["a", "c"])):
        try:
            evaluator_order_indices(manifest, evaluator)
        except RuntimeError:
            pass
        else:
            raise AssertionError("identity mismatch must fail closed")


def test_anchor_indices_are_fixed_relative_horizons() -> None:
    assert anchor_indices(9) == (2, 4, 6, 8)
    assert anchor_indices(1) == (0, 0, 0, 0)


def test_surrogates_use_last_frame_or_all_four_anchors_and_are_differentiable() -> None:
    target_yaw = torch.zeros(9)
    target_root = torch.zeros(9, 3)
    recon_yaw = torch.zeros(9, requires_grad=True)
    recon_root = torch.zeros(9, 3)
    recon_root[2, 0] = 1.0
    recon_root[4, 0] = 2.0
    recon_root[6, 0] = 3.0
    recon_root[8, 0] = 4.0
    recon_root.requires_grad_()

    current, candidate = surrogate_values_from_decoded(
        target_yaw, target_root, recon_yaw, recon_root
    )

    assert current > 0
    assert candidate > 0
    candidate.backward()
    assert recon_root.grad is not None
    assert set(torch.nonzero(recon_root.grad[:, 0], as_tuple=False).flatten().tolist()) == {2, 4, 6, 8}
    assert torch.count_nonzero(recon_root.grad[:, 1:]) == 0


class _DecodedGeometry(torch.nn.Module):
    @staticmethod
    def _decoded_human_yaw_root(human: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        return human[..., 0], human[..., 1:4]


def test_batch_surrogates_ignore_padding_and_weight_samples_equally() -> None:
    model = _DecodedGeometry()
    target = torch.zeros(2, 9, 4)
    recon = target.clone()
    recon[0, 4, 1] = 1.0
    recon[0, 5:, 1] = 1000.0
    recon[1, 8, 1] = 1.0
    recon.requires_grad_()

    current, candidate = batch_surrogates(model, target, recon, torch.tensor([5, 9]))

    assert current > 0
    assert candidate > 0
    candidate.backward()
    assert recon.grad is not None
    assert torch.count_nonzero(recon.grad[0, 5:]) == 0


def test_rank_statistics_and_paired_bootstrap_support_a_better_candidate() -> None:
    values = np.array([3.0, 1.0, 1.0, 2.0])
    assert np.allclose(rankdata(values), np.array([3.0, 0.5, 0.5, 2.0]))
    target = np.arange(12, dtype=np.float64)
    current = np.array([0, 3, 1, 5, 2, 8, 4, 10, 6, 11, 7, 9], dtype=np.float64)
    candidate = target.copy()
    assert math.isclose(spearman(candidate, target), 1.0)

    result = paired_rank_bootstrap(current, candidate, target, seed=17, samples=200)

    assert result["point_delta"] > 0.02
    assert result["ci95_lower"] > 0.0
