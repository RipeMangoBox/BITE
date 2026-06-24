---
title: "MoDebug MoLingo 272D Diagnostic Eval Status"
created: 2026-06-02T20:55:00+08:00
updated: 2026-06-02T21:20:00+08:00
status: completed
hypothesis: "MoLingo 272D official eval can serve as the first real MoDebug MVP baseline, but repeat=1 results remain diagnostic only."
tags:
  - MoDebug
  - molingo
  - diagnostic
  - eval
  - status/completed
source_papers:
  - "[[paperAnalysis/CVPR_2026/MoLingo_Motion-Language_Alignment_for_Text-to-Human_Motion_Generation|MoLingo]]"
---

# MoLingo 272D Diagnostic Eval Status

> [!abstract] 接力结论
> 2026-06-02 已完成 MoLingo 272D 官方 eval MVP：两个 cfg run 均使用真实 `mogen/eval_mogen.py`、full 272D HumanML3D test split、真实 checkpoint/evaluator，`exit_code=0`。这些结果只能作为 `repeat=1` diagnostic，不是 paper-level formal。

## Run Summary

| Run | GPU | FID | TOP1 | TOP2 | TOP3 | Matching Score |
|-----|-----|-----|------|------|------|----------------|
| cfg=7.0 step=32 acc=5 repeat=1 | GPU0 | 3.564 | 0.771 | 0.900 | 0.937 | 14.718 |
| cfg=4.0 step=32 acc=5 repeat=1 | GPU1 | 3.794 | 0.763 | 0.892 | 0.938 | 14.820 |

## Provenance

| Field | Value |
|------|-------|
| Remote repo | `/data/public/ripemangobox/Motion/MoLingo` |
| Git branch | `TPA` |
| Git head | `86e21b24784e36c3bb6d43d0d5c1de4de6224768` |
| Script | `mogen/eval_mogen.py` |
| Data | `/data/public/ripemangobox/Motion/datasets/272-dim-HumanML3D` |
| Evaluator | `/data/public/ripemangobox/Motion/MotionStreamer/Evaluator_272/epoch=99.ckpt` |
| Evaluator SHA256 | `f45b844034e7942ab2c32f52449a4c08e0511ce33694602f70b93a4862a4f51f` |

## Evidence Paths

Canonical remote run directories:

- `/data/public/ripemangobox/Motion/experiments/MoDebug/modebug_real_runs/modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg7_g0`
- `/data/public/ripemangobox/Motion/experiments/MoDebug/modebug_real_runs/modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg4_g1`

Legacy compatibility path:

- `/data/public/ripemangobox/Motion/MoLingo/artifacts/modebug_real_runs/modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg7_g0`
- `/data/public/ripemangobox/Motion/MoLingo/artifacts/modebug_real_runs/modebug_molingo272_eval_diagnostic_20260602-170502_86e21b2_cfg4_g1`

Local cache:

- `linkedCodebases/MoDebug/remote4090/modebug_molingo272_eval_20260602/modebug_molingo272_eval_20260602_203736/`

Each run contains `manifest.json`, `command.sh`, `stdout_stderr.log`, `runtime_status.txt`, `nvidia_smi_start_end.txt`, and `metrics_eval_res.txt`.

## Limitations

- `repeat=1` makes printed confidence values zero by construction; they are not statistical confidence intervals.
- The cfg comparison is an MVP parameter probe, not a final hyperparameter sweep.
- The run only covers the 272D HumanML3D test split. It does not imply 263D, MotionCLR, visualization, or training conclusions.
- MoLingo eval-related files were clean, but the remote repo had unrelated dirty/untracked training artifacts recorded in `manifest.json`.

## Visualization Blocker

MoLingo visualization was not started. The real entry is `/data/public/ripemangobox/Motion/MoLingo/mogen/demo.py`, but it requires a valid SMPLH body model path via `-b`.

Preflight results:

| Dependency | Result |
|------------|--------|
| MoGenTS length estimator `/data/public/ripemangobox/Motion/mogents/checkpoints/humanml3d/length_estimator/model/finest.tar` | Strictly loads into MoLingo `LengthEstimator(512, 50)`, epoch 11 |
| EventT2M Guo `text_mot_match/model/finest.tar` | Not a length estimator checkpoint; missing `estimator` key |
| DART SMPLH candidate `/data/public/ripemangobox/Motion/DART/data/smplx_lockedhead_20230207/models_lockedhead` | Fails `smplx.create(..., model_type='smplh')` with missing `hands_componentsl` attribute |

If prompt lines include explicit seconds, e.g. `<caption>#3`, the demo can avoid the missing `mogen/checkpoints/t2m/length_estimator/model/finest.tar`, but it still cannot avoid the SMPLH rendering dependency. The current blocker is therefore the body model load failure, not the length estimator.

Safe next step for visualization:

1. Verify `smplx.create(<path>, model_type='smplh', gender='neutral')` loads on 4090.
2. Run `mogen/demo.py` with explicit durations and `repeat=1`.
3. Record command, SMPLH path, checkpoint hashes, output MP4 paths, and any failures without patching around them.
