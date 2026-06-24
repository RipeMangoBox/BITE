---
title: "MoDebug DS Formal Experiment Gate"
created: 2026-06-02T23:20:00+08:00
updated: 2026-06-03T16:45:02+08:00
status: active
tags:
  - MoDebug
  - ds-review
  - formal-experiment-gate
---

# MoDebug DS Formal Experiment Gate

> [!note] 当前结论
> 2026-06-03 DS 复核已给出 `APPROVED_TO_START_FORMAL_CANDIDATE`。Trace 1 formal diagnostic sweep 已完成并经结论复核为 `APPROVED_WITH_CAVEATS`；Trace 3 formal candidate training 仍在 GPU0 运行。Trace 1 结果只支持机制诊断，Trace 3 在 official evaluator 完成前不得写 paper-level 指标。

## 用户硬约束

- 需要真实实验数据，不要 smoke。
- 所有正式实验代码和指令必须先经过 DS 复核。
- 禁止把 smoke/probe/path-validation 写成正式数据。
- 禁止伪造正式数据；所有指标必须来自真实 checkpoint、真实数据、真实 evaluator 和完整 provenance。

## 命名

| Trace | 旧称 | 方向 |
|------|------|------|
| Trace 1 | Track B | CA 层扰动诊断 |
| Trace 3 | Track A | 数据效率训练侧 |

## DS 复核结论

| 时间 | Trace | DS 状态 | 处理 |
|------|------|---------|------|
| 2026-06-03T15:24+08:00 | Trace 1 | `APPROVED_TO_START_FORMAL_CANDIDATE` | 已启动 `modebug_trace1_formal_20260603`，输出 `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_formal_layer_sweep_ds_review_20260603_gpu1/`。 |
| 2026-06-03T15:24+08:00 | Trace 3 | `APPROVED_TO_START_FORMAL_CANDIDATE` | 已启动 `modebug_trace3_train_formal_20260603`，输出 `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0/`；official evaluator 等训练 checkpoint 完成后运行。 |
| 2026-06-03T16:04+08:00 | Trace 1 analysis | `APPROVED_WITH_CAVEATS` | 36 个逐层 layer group 完成，controls passed；结论边界和折线图见 [[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。 |

历史阻塞记录：DS session `eda0968dad94` 的 `BLOCKED` 只作为过期门禁背景保留，不再作为当前状态；当前状态以上表和 Trace 1 分析页为准。

## 已降级的工程验证

| Trace | 路径 | 当前状态 |
|------|------|----------|
| setup | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/setup/20260602_motionclr_release_generate_no_fp16_cli_probe_v2/` | `engineering_validation_only` |
| Trace 1 | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/track_b_ca_perturbation/20260602_gpu1_track_b_ca_cfg_sweep_mvp/` | `engineering_validation_only` |
| Trace 3 | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/track_a_disploss/20260602_gpu0_track_a_minimal_real_ablation/` | `engineering_validation_only` |
| Trace 1 dev check | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dev_validation/trace1_formal_layer_sweep_min_step1_20260603/` | `dev_validation_only` |
| Trace 3 dev check | `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dev_validation/trace3_formal_candidates_variants_step1_20260603/` | `dev_validation_only` |

## Bounded Validation 边界

Bounded validation 可使用真实数据和真实 checkpoint，但只回答“代码和命令是否可控”。它不得进入正式指标表。

- Trace 1：验证 CA output scaling hook、`alpha=1` no-op、`alpha=0` positive control。
- Trace 3：验证真实 HumanML3D batch update、精确步数停止、可控 checkpoint 写盘。
- 所有 bounded validation run 目录必须标记 `engineering_validation_only`。

## 正式 Manifest 必填项

- repo URL、branch、HEAD commit。
- `git status --short` 和完整 dirty diff。
- 完整命令、环境变量、accelerate config、GPU 分配。
- seed、数据路径、split 文件、行数或 SHA256。
- checkpoint、`opt.txt`、mean/std、evaluator 的路径和 SHA256。
- 训练和评估超参。
- Trace 1 的 `alpha/layer` 或 Trace 3 的 DispLoss/augmentation 参数。
- checkpoint、metrics 文件、日志文件路径和 SHA256。
- 硬件/软件环境。

## 下一步

Trace 1/3 bounded validation 已获 DS 二次复核 `APPROVED_FOR_VALIDATION` 并完成，记录见 [[2026-06-02_dual_trace_bounded_validation_status]]。2026-06-03 正式候选代码和命令已获 DS 批准；Trace 1 diagnostic 已完成，Trace 3 继续等待四个训练 variant checkpoint。Trace 3 official evaluator 必须等训练 checkpoint 完成后再运行。
