from __future__ import annotations

import sys
from pathlib import Path

import torch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from storymotion_d42_camera_text_reliance import (  # noqa: E402
    cyclic_shuffle_camera_text,
    difference_record,
    predict_shared_xt_conditions,
)


def test_cyclic_shuffle_changes_only_camera_half_globally() -> None:
    text = torch.arange(4 * 6, dtype=torch.float32).reshape(4, 6)

    shuffled, indices = cyclic_shuffle_camera_text(text)

    assert indices == [1, 2, 3, 0]
    assert torch.equal(shuffled[:, :3], text[[1, 2, 3, 0], :3])
    assert torch.equal(shuffled[:, 3:], text[:, 3:])


class _Diffusion:
    num_timesteps = 1000
    name = "diffusion"

    def q_sample(self, z, t, noise):
        return z + noise

    def model_t(self, t):
        return t

    def prediction_to_x0(self, pred, x_t, t):
        return pred


class _Train:
    HUM_DIM = 1
    SOURCE_GT = 7

    def __init__(self):
        self.x_t_pointers = []

    def make_branch_masks(self, z, valid, task, task_routing):
        obs = torch.zeros_like(z, dtype=torch.bool)
        obs[:, :1] = valid[:, None]
        return obs, ~obs

    def build_source_meta(self, obs_mask, source):
        return torch.zeros((obs_mask.shape[0], 1))

    def predict_with_joint_coupling(
        self, model, x_t, model_t, text, z, obs_mask, task, source_meta, scale, mode
    ):
        self.x_t_pointers.append(x_t.data_ptr())
        return model(x_t, text)


def test_shared_condition_forward_reuses_exact_xt_tensor() -> None:
    train = _Train()
    z = torch.zeros((2, 3, 2))
    valid = torch.ones((2, 2), dtype=torch.bool)
    aligned = torch.zeros((2, 4))
    shuffled = torch.ones((2, 4))

    def model(x_t, text):
        return x_t + text[:, :1, None]

    outputs, noise, x_t = predict_shared_xt_conditions(
        model,
        _Diffusion(),
        train,
        z,
        {"aligned": aligned, "cyclic_shuffled_camera_text": shuffled},
        valid,
        task_id=1,
        sample_indices=[0, 1],
        seed=17,
        timestep=50,
        task_routing="human_first",
    )

    assert train.x_t_pointers == [x_t.data_ptr(), x_t.data_ptr()]
    assert torch.equal(outputs["aligned"][:, :1], z[:, :1])
    assert torch.equal(outputs["cyclic_shuffled_camera_text"][:, :1], z[:, :1])
    assert torch.allclose(
        outputs["cyclic_shuffled_camera_text"][:, 1:]
        - outputs["aligned"][:, 1:],
        torch.ones((2, 2, 2)),
    )
    assert noise.shape == z.shape


def test_difference_record_is_first_minus_second() -> None:
    first = {
        "channel": {field: [3.0, 5.0] for field in ("signed_mean", "rms", "mae", "target_rms", "relative_error")},
        "sample": {field: 7.0 for field in ("signed_mean", "rms", "mae", "target_rms", "relative_error")},
    }
    second = {
        "channel": {field: [1.0, 2.0] for field in ("signed_mean", "rms", "mae", "target_rms", "relative_error")},
        "sample": {field: 4.0 for field in ("signed_mean", "rms", "mae", "target_rms", "relative_error")},
    }

    result = difference_record(first, second)

    assert result["channel"]["rms"] == [2.0, 3.0]
    assert result["sample"]["rms"] == 3.0
