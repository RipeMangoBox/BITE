from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType, SimpleNamespace

import numpy as np
import torch
from torch import nn

from storymotion.training.human200 import (
    HUMAN200_FEATURE_CONTRACT,
    HUMAN200_LAYOUT,
    human199_raw_to_human200_raw,
    human200_raw_to_human199_raw,
    load_human200_stats,
)


ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stats_payload(manifest: Path, *, sample_ids_sha256: str = "1" * 64) -> dict:
    return {
        "schema_version": 1,
        "feature_contract": HUMAN200_FEATURE_CONTRACT,
        "layout": HUMAN200_LAYOUT,
        "human_dim": 200,
        "normalization": "frame_weighted_population_mean_std",
        "min_std": 1.0e-6,
        "source": {
            "split": "train",
            "manifest_sha256": _sha256(manifest),
            "sample_ids_sha256": sample_ids_sha256,
            "samples": 1,
            "frames": 2,
            "ordered_rows": True,
        },
        "builder": {"script_sha256": "2" * 64, "argv": ["builder.py"]},
        "mean": [0.0] * 200,
        "std": [1.0] * 200,
    }


def _extract_function(path: Path, name: str, globals_: dict):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name)
    future = ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0)
    namespace = dict(globals_)
    module = ast.fix_missing_locations(ast.Module(body=[future, function], type_ignores=[]))
    exec(compile(module, str(path), "exec"), namespace)
    return namespace[name]


def test_human200_codec_preserves_direct_root_yaw_and_pose() -> None:
    generator = torch.Generator().manual_seed(17)
    human199 = torch.randn(2, 37, 199, generator=generator) * 0.05
    human199[..., 0] += 1.0
    human199[..., 3] *= 0.2

    human200 = human199_raw_to_human200_raw(human199)
    inverse = human200_raw_to_human199_raw(human200)
    reencoded = human199_raw_to_human200_raw(inverse)

    assert human200.shape == (2, 37, 200)
    assert torch.allclose(human200[..., :3], reencoded[..., :3], atol=2.0e-6)
    assert torch.allclose(human200[..., 3:], reencoded[..., 3:], atol=2.0e-6)
    assert torch.allclose(inverse[..., 0], human199[..., 0], atol=1.0e-7)
    assert torch.allclose(inverse[..., 4:], human199[..., 4:], atol=1.0e-7)
    assert torch.allclose(inverse[..., 3], human199[..., 3], atol=2.0e-6)
    assert torch.allclose(human200[..., :1, 1:3], torch.zeros_like(human200[..., :1, 1:3]))


def test_stats_source_must_match_the_train_manifest(tmp_path: Path) -> None:
    train_manifest = tmp_path / "train.jsonl"
    eval_manifest = tmp_path / "eval.jsonl"
    train_manifest.write_text('{"sample_id":"train"}\n', encoding="utf-8")
    eval_manifest.write_text('{"sample_id":"eval"}\n', encoding="utf-8")
    stats_path = tmp_path / "stats.json"
    stats_path.write_text(json.dumps(_stats_payload(train_manifest)), encoding="utf-8")

    loaded = load_human200_stats(stats_path, expected_train_manifest=train_manifest)
    assert loaded["meta"]["source"]["split"] == "train"
    try:
        load_human200_stats(stats_path, expected_train_manifest=eval_manifest)
    except ValueError as error:
        assert "train manifest" in str(error)
    else:
        raise AssertionError("an eval manifest must never be accepted as the normalization source")


def test_parallel_stats_are_frame_weighted_ordered_and_immutable(tmp_path: Path) -> None:
    rows = []
    converted = []
    for index, frames in enumerate((2, 5, 3)):
        human199 = np.zeros((frames, 199), dtype=np.float32)
        human199[:, 0] = index + np.arange(frames) * 0.25
        human199[:, 1] = 0.1 * (index + 1)
        human199[:, 3] = 0.02 * (index + 1)
        human199[:, 4:] = index - 0.5
        path = tmp_path / f"motion_{index}.npy"
        np.save(path, human199)
        rows.append(
            {
                "sample_id": f"sample_{index}",
                "feature_space": "pulpmotion_smpl_rifke",
                "motion_feature_path": str(path),
            }
        )
        converted.append(human199_raw_to_human200_raw(torch.from_numpy(human199).double()))
    manifest = tmp_path / "train.jsonl"
    manifest.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    outputs = []
    for workers in (0, 2):
        output = tmp_path / f"stats_w{workers}.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/build_v8_2_human200_stats.py"),
                "--train-human-manifest",
                str(manifest),
                "--output",
                str(output),
                "--expected-samples",
                "3",
                "--num-workers",
                str(workers),
                "--chunk-size",
                "1",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        outputs.append(json.loads(output.read_text(encoding="utf-8")))

    expected = torch.cat(converted, dim=0)
    assert np.allclose(outputs[0]["mean"], expected.mean(dim=0).numpy(), atol=1.0e-12)
    assert np.allclose(outputs[0]["std"], expected.std(dim=0, correction=0).clamp_min(1.0e-6).numpy(), atol=1.0e-12)
    assert np.allclose(outputs[0]["mean"], outputs[1]["mean"], atol=1.0e-12)
    assert np.allclose(outputs[0]["std"], outputs[1]["std"], atol=1.0e-12)
    assert outputs[1]["source"]["ordered_rows"] is True
    assert outputs[1]["source"]["frames"] == 10
    assert outputs[1]["builder"]["script_sha256"] == _sha256(
        ROOT / "scripts/build_v8_2_human200_stats.py"
    )
    assert outputs[1]["builder"]["argv"]

    command = [
        sys.executable,
        str(ROOT / "scripts/build_v8_2_human200_stats.py"),
        "--train-human-manifest",
        str(manifest),
        "--output",
        str(tmp_path / "stats_w0.json"),
        "--expected-samples",
        "3",
        "--num-workers",
        "0",
    ]
    assert subprocess.run(command, cwd=ROOT, capture_output=True).returncode != 0
    subprocess.run([*command, "--reuse-existing"], cwd=ROOT, check=True, capture_output=True)


def test_human200_geometry_loss_is_direct_not_cumulative() -> None:
    if "storymotion.tokenizers.fsq_vae" not in sys.modules:
        fsq_module = ModuleType("storymotion.tokenizers.fsq_vae")
        fsq_module.HierarchicalFSQ = type("HierarchicalFSQ", (nn.Module,), {})
        sys.modules[fsq_module.__name__] = fsq_module
    if "storymotion.tokenizers.vq_vae" not in sys.modules:
        vq_module = ModuleType("storymotion.tokenizers.vq_vae")
        vq_module.EMAVectorQuantizer = type("EMAVectorQuantizer", (nn.Module,), {})
        sys.modules[vq_module.__name__] = vq_module
    from storymotion.tokenizers.joint_human_camera import JointHumanCameraAE

    model = JointHumanCameraAE(200, 14, 8, 4, hidden_dim=16, downsample=1)
    model.geometry_human_mean = torch.zeros(200)
    model.geometry_human_std = torch.ones(200)
    model.geometry_feature_contract = "human200_direct_root_yaw"
    target = torch.zeros(1, 5, 200)
    target[..., 4] = 1.0
    reconstructed = target.clone()
    reconstructed[:, 0, 1] = 1.0
    reconstructed[:, 0, 3] = torch.sin(torch.tensor(0.2))
    reconstructed[:, 0, 4] = torch.cos(torch.tensor(0.2))
    reconstructed[:, 4, 1] = 100.0
    reconstructed.requires_grad_()
    mask = torch.tensor([[True, True, True, True, False]])

    yaw_loss, root_loss = model._human_root_geometry_losses(target, reconstructed, mask)
    (yaw_loss + root_loss).backward()

    assert yaw_loss > 0 and root_loss > 0
    assert reconstructed.grad is not None
    assert reconstructed.grad[:, 0, 1:5].abs().sum() > 0
    assert reconstructed.grad[:, 1:4].abs().sum() == 0
    assert reconstructed.grad[:, 4].abs().sum() == 0


def test_v8_2_contract_and_cache_reorder_match_camera_first_native_layout() -> None:
    contract_fn = _extract_function(
        ROOT / "scripts/train_storymotion_joint_tokenizer.py",
        "stage1_model_contract",
        {
            "Any": object,
            "HUMAN200_FEATURE_CONTRACT": HUMAN200_FEATURE_CONTRACT,
            "HUMAN200_LAYOUT": HUMAN200_LAYOUT,
        },
    )
    args = SimpleNamespace(
        tokenizer="joint_ae",
        preset="storymotion_v8_2_joint_ae_human200_camera14",
        feature_contract=HUMAN200_FEATURE_CONTRACT,
        human_dim=200,
        camera_dim=14,
        human_latent_dim=128,
        camera_latent_dim=64,
        hidden_dim=256,
        downsample=4,
        residual_depth=2,
        dilation_growth_rate=3,
        residual_activation="relu",
        residual_dropout=0.2,
        human200_stats=Path("stats.json"),
        human200_stats_resolved="/tmp/stats.json",
        human200_stats_sha256="a" * 64,
        human200_stats_source_manifest_sha256="b" * 64,
        human200_stats_source_sample_ids_sha256="c" * 64,
        human200_stats_source_samples=162760,
        human200_stats_source_frames=1000000,
    )
    contract = contract_fn(args)
    assert contract["native_latent_order"] == "camera64+human128"

    reorder = _extract_function(
        ROOT / "scripts/build_stage2_joint_tokenizer_latent_cache.py",
        "reorder_and_align_latent",
        {"torch": torch, "LATENT_DIM": 192, "HUM_DIM": 128, "CAM_DIM": 64, "LATENT_FRAMES": 75},
    )
    camera = torch.arange(64, dtype=torch.float32).view(1, 1, 64).expand(1, 2, 64)
    human = (1000 + torch.arange(128, dtype=torch.float32)).view(1, 1, 128).expand(1, 2, 128)
    stage2 = reorder(torch.cat([camera, human], dim=-1), camera_latent_dim=64)

    assert stage2.shape == (1, 192, 75)
    assert torch.equal(stage2[:, :128, :2], human.transpose(1, 2))
    assert torch.equal(stage2[:, 128:, :2], camera.transpose(1, 2))
    assert stage2[..., 2:].abs().sum() == 0


def test_long_geometry_contract_has_required_bins_and_yaw_metric() -> None:
    tree = ast.parse((ROOT / "scripts/eval_stage1_long_sequence_geometry.py").read_text(encoding="utf-8"))
    assignments = {
        node.targets[0].id: ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id in {"LENGTH_BINS", "METRICS"}
    }
    assert assignments["LENGTH_BINS"] == ((1, 64), (65, 128), (129, 192), (193, None))
    assert "human_integrated_yaw_geodesic" in assignments["METRICS"]
    assert {"camera_center_ade", "camera_center_fde", "camera_rotation_deg"} <= set(assignments["METRICS"])
