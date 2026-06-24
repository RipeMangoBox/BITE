---
created: 2026-04-17
updated: 2026-04-17
status: active
title: TAMR Fair Baseline Eval Summary
tags:
  - tamr
  - motionpatches
  - baseline
  - eval
---
# TAMR Fair Baseline Eval Summary

## 1. Scope

本次 summary 只回答一个问题：在同一份 `HumanML3D-E-MP` retrieval gallery、同一份
`humanml3de` strict split 下，当前 fair baseline 的 seed42 起点到底在哪里。

Evaluated runs:

- `plain00_s42`
- `stage5_s2e_v2` `local_eval_2026-04-17_hmlemp`
- `ref00_s42` `local_eval_2026-04-17_hmlemp`

## 2. Shared Eval Protocol

- strict retrieval preset: `humanml3de`
- retrieval gallery root: `HumanML3D-E-MP`
- normal split size: `4646`
- nsim split size: `97`
- temporal GT source: `HumanML3D-E`
- offline HuggingFace / timm cache mode
## 3. PrimaryScore Table

PrimaryScore definition:

`mean(TMR-normal R@1/R@5 + TMR-nsim R@1/R@5 over t2m+m2t)`

| Run | PrimaryScore | TMR-normal t2m R@1 | TMR-normal m2t R@1 | TMR-normal t2m R@5 | TMR-normal m2t R@5 | TMR-nsim t2m R@1 | TMR-nsim m2t R@1 | TMR-nsim t2m R@5 | TMR-nsim m2t R@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| plain00_s42 | **43.8275** | 7.12 | 9.84 | 24.77 | 25.38 | 56.70 | 57.73 | 84.54 | 84.54 |
| stage5_s2e_v2 fair re-eval | **44.4487** | 7.00 | 9.75 | 24.82 | 26.39 | 53.61 | 54.64 | 89.69 | 89.69 |
| ref00_s42 fair re-eval | **43.8662** | 6.52 | 9.54 | 23.22 | 25.05 | 55.67 | 54.64 | 88.66 | 87.63 |

Seed42 deltas:

- `stage5_s2e_v2 fair - plain00_s42 = +0.6212`
- `ref00_s42 fair - plain00_s42 = +0.0387`
- `ref00_s42 fair - stage5_s2e_v2 fair = -0.5825`

## 4. Temporal Diagnostics Snapshot

| Run | EVT-normal t2m CAR@1 | EVT-normal t2m TAR@5 | EVT-nsim t2m CAR@1 | EVT-nsim t2m TAR@5 |
|---|---:|---:|---:|---:|
| plain00_s42 | 5.99 | 11.77 | 44.68 | 29.90 |
| stage5_s2e_v2 fair re-eval | 8.46 | 15.91 | 63.83 | 44.33 |
| ref00_s42 fair re-eval | 7.80 | 14.03 | 65.96 | 38.14 |

## 5. Interpretation

### 5.1 `plain00_s42` 是当前最干净的 fair baseline anchor

- 它满足 `humanml3de` 训练、无 `event_temporal` 分支、`HumanML3D-E-MP` gallery、
  `humanml3de` strict split。
- 因此后续所有“公平 baseline”表述都应该先以它为零点，而不是直接继承旧 `REF00`
  4-seed summary。

### 5.2 `stage5_s2e_v2` 在 fair eval 下仍保留正信号

- `PrimaryScore: 43.8275 -> 44.4487`，delta 为 `+0.6212`。
- normal retrieval 几乎持平，但 `nsim` 与 EVT 改善更明显：
  - `EVT-normal CAR@1/TAR@5: 5.99/11.77 -> 8.46/15.91`
  - `EVT-nsim CAR@1/TAR@5: 44.68/29.90 -> 63.83/44.33`

当前更稳妥的说法是：

- event-aware mainline 在 fair same-regime seed42 对照下仍优于 plain baseline；
- 但它仍只是 single-seed smoke，不足以直接冻结 paper baseline。

### 5.3 `ref00_s42` 在 fair eval 下不再显得明显更强

- `PrimaryScore: 43.8275 -> 43.8662`，只比 `plain00_s42` 高 `+0.0387`。
- temporal diagnostics 仍比 plain 更强，但主 retrieval 没有拉开。

这意味着：

- 旧 `REF00 4-seed mean = 44.7481 ± 0.7944` 不能再直接拿来当“当前 working fair baseline”；
- 在 packaged-root fair eval 没补完 `s41 / s43 / s44` 之前，`REF00` 只能算 rerun family
  的 historical / pending baseline。

## 6. Recommendation

Immediate next step priority:

1. 先补 `ref00_s41 / s43 / s44` 的 packaged-root fair re-eval。
2. 若 fair re-eval 后 event-aware 相对 plain 的增益量级仍接近 rerun variance，再补
   `plain00_s41 / s43 / s44`。
3. 在 packaged-root fair multi-seed audit 完成前，不再把旧 `REF00` 4-seed mean
   写成当前 baseline。

## 7. Artifact References

- `MotionPatches-main/checkpoints/plain00_s42/HumanML3D/contrastive_metrics/TMR-normal.yaml`
- `MotionPatches-main/checkpoints/plain00_s42/HumanML3D/contrastive_metrics/TMR-nsim.yaml`
- `MotionPatches-main/checkpoints/plain00_s42/HumanML3D/contrastive_metrics/EVT-normal.yaml`
- `MotionPatches-main/checkpoints/plain00_s42/HumanML3D/contrastive_metrics/EVT-nsim.yaml`
- `MotionPatches-main/checkpoints/stage5_s2e_v2/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/eval_metadata.yaml`
- `MotionPatches-main/checkpoints/stage5_s2e_v2/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/TMR-normal.yaml`
- `MotionPatches-main/checkpoints/stage5_s2e_v2/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/TMR-nsim.yaml`
- `MotionPatches-main/checkpoints/stage5_s2e_v2/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/EVT-normal.yaml`
- `MotionPatches-main/checkpoints/stage5_s2e_v2/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/EVT-nsim.yaml`
- `MotionPatches-main/checkpoints/ref00_s42/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/eval_metadata.yaml`
- `MotionPatches-main/checkpoints/ref00_s42/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/TMR-normal.yaml`
- `MotionPatches-main/checkpoints/ref00_s42/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/TMR-nsim.yaml`
- `MotionPatches-main/checkpoints/ref00_s42/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/EVT-normal.yaml`
- `MotionPatches-main/checkpoints/ref00_s42/HumanML3D/local_eval_2026-04-17_hmlemp/contrastive_metrics/EVT-nsim.yaml`
