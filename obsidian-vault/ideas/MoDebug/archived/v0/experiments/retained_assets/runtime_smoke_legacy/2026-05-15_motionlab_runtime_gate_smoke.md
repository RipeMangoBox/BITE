---
title: "MotionLab Runtime Gate Smoke"
created: 2026-05-15T22:00:20+08:00
updated: 2026-05-15T22:00:20+08:00
status: active
tags:
  - MoDebug
  - MotionLab
  - runtime-smoke
  - status/diagnostic
role: diagnostic
used_for: observation
---

# MotionLab Runtime Gate Smoke

## Summary

2026-05-15 接力 `019e2a83-cb6c-7751-9572-f4675a5e13bf`，继续 MotionLab official `train.py` / `test.py` / `demo.py` 的最小 runtime gate。

结论：MotionLab 还不能完成 train / test / demo smoke。`event-t2m` 是现有环境里最接近的 env；用临时 overlay 绕过 `psutil` / `roma` import gate 后，official train / test 已经能进入配置解析和 dataset 构造，但阻塞在 MotionLab-ready `datasets/all/new_joint_vecs/004822.npy` 缺失。demo 在可视化链路上先阻塞于 `h5py` 缺失。

这不是 MoDebug 方法结果，也不是 MotionLab 质量评估；它只是 runtime / asset readiness 诊断。

## Provenance

Remote host / repo:

```text
host: user-SYS-7049GP-TRT
repo: /data/public/ripemangobox/Motion/MotionLab
controller repo: /data/public/ripemangobox/Motion/EventT2M-codes
env: event-t2m
date: 2026-05-15
```

Remote git provenance was archived before this continuation:

```text
logs/remote4090/git_archive/continue_019e2a83_motionlab_smoke_20260515_$(date +%Y%m%d_%H%M%S)
```

Fetched local logs:

```text
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_direct_import_probe_0515c.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_direct_pip_0515c.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_env_pkg_matrix_0515c.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_overlay_smoke_0515c.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_overlay_smoke_0515d.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_overlay_smoke_0515e.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_train_test_overlay_0515f.log
artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_demo_gate_0515f.log
```

## Environment Finding

Existing env matrix:

- `event-t2m`: has `torch`, `pytorch_lightning`, `omegaconf`, `clip`, `smplx`, `scipy`, `sklearn`, `matplotlib`, `pandas`, `rich`; missing `psutil`, `trimesh`, `roma`.
- `rfmotion`: has `torch`, `pytorch_lightning`, `omegaconf`, `rich`; missing `clip`, `smplx`, `scipy`, `sklearn`, `matplotlib`, `pandas`, `psutil`, `trimesh`.
- `mogents-gpu1`: has `trimesh`, `clip`, `smplx`, `scipy`, `sklearn`, `matplotlib`; missing `pytorch_lightning`, `omegaconf`, `psutil`, `pandas`, `rich`.
- `MoPa`: has `psutil`, `torch`, `pytorch_lightning`, `omegaconf`, `scipy`, `sklearn`, `matplotlib`, `pandas`; missing `clip`, `smplx`, `trimesh`, `rich`.

`event-t2m` remains the least-bad env for MotionLab gate smoke because it already has CLIP / SMPLX / Lightning / OmegaConf.

Package install attempt:

- Aliyun mirror failed for `psutil` with `No matching distribution found`.
- Direct PyPI also did not complete quickly enough to be useful for this pass.
- No MotionLab source file was modified.

## Temporary Overlay

The train / test smoke used a temporary overlay under `/tmp/modebug_motionlab_overlay_0515f`:

- `psutil.virtual_memory().percent` stub, only for `ProgressLogger`.
- `roma.rotvec_to_rotmat` / `roma.rotmat_to_rotvec` compatibility layer backed by `scipy.spatial.transform.Rotation`.

The demo help smoke used a separate `trimesh` import stub under `/tmp/modebug_motionlab_demo_overlay_0515f`, only to expose the next visualization import gate.

These overlays are diagnostic only. They should not be treated as a reproducible MotionLab environment or a valid numeric training setup.

## Official Train / Test Gate

Command role: `diagnostic`

Protocol:

```text
official train.py / test.py
cfg: configs/config_rfmotion.yaml
cfg_assets: configs/assets.yaml
batch_size: 1
device: 0
timeout: 180s
```

Asset precheck:

```text
OK checkpoints/glove/our_vab_data.npy
OK checkpoints/t2m/text_mot_match/model/finest.tar
OK checkpoints/t2m/Comp_v6_KLD01/opt.txt
OK checkpoints/smpl/SMPL_NEUTRAL.pkl
MISS checkpoints/clip-vit-large-patch14
MISS checkpoints/mcm-ldm/motionclip.pth.tar
MISS checkpoints/mcm-ldm/motion_encoder.ckpt
MISS checkpoints/motionflow/motionflow.ckpt
MISS checkpoints/smplh/SMPLH_NEUTRAL.npz
MISS checkpoints/smplh/smplh.faces
MISS datasets/all/new_joint_vecs
MISS datasets/all/texts
MISS datasets/all/train.txt
MISS datasets/all/test.txt
```

Observed gate:

```text
train.py -> get_datasets -> HumanML3D Dataset -> FileNotFoundError:
./datasets/all/new_joint_vecs/004822.npy

test.py -> get_datasets -> HumanML3D Dataset -> FileNotFoundError:
./datasets/all/new_joint_vecs/004822.npy
```

This confirms the current first blocking layer for train / test is not the model checkpoint yet; it is the missing MotionLab-ready merged `datasets/all` content.

## Demo Gate

Command role: `diagnostic`

Protocol:

```text
official demo.py --help
timeout: 90s
```

Observed gate:

```text
demo.py -> visualize.vis_utils -> visualize.simplify_loc2rot -> ModuleNotFoundError: No module named 'h5py'
```

This is a visualization environment gate. Even after `h5py`, demo is still expected to require render / SMPLH / checkpoint assets.

## Metric Role

No model metric was produced.

Metric provenance:

- date: 2026-05-15
- artifact_path: `artifacts/remote4090/remote4090_logs_20260515_motionlab_smoke/modebug_motionlab_train_test_overlay_0515f.log`
- evaluator: none
- protocol: official MotionLab train / test entry gate smoke
- motion_source: none
- condition_pair: none
- n/evaluable: 0
- coverage: import, config parse, dataset constructor gate
- role: `diagnostic`
- used_for: observation
- limitations: no training step, no evaluation step, no generated motion, no MotionLab quality claim

## Next Action

To make MotionLab runnable beyond this gate, do not fabricate `datasets/all`. Required next setup is:

1. Build official MotionLab-ready `datasets/all` with `new_joint_vecs`, `texts`, and splits.
2. Add real `clip-vit-large-patch14`, `mcm-ldm/motionclip.pth.tar`, and `mcm-ldm/motion_encoder.ckpt` assets before model-init smoke.
3. Add `motionflow.ckpt` before eval / demo checkpoint smoke.
4. Add real SMPLH assets before demo / render smoke.
5. Build a real MotionLab env or install missing packages from a working wheel source; temporary overlays should not be used for actual numeric claims.
