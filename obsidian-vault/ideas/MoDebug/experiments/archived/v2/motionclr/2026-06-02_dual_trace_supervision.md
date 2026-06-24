---
title: "MoDebug Dual-Trace Supervision"
created: 2026-06-02T22:58:00+08:00
updated: 2026-06-03T16:45:02+08:00
status: superseded_by_formal_runs
tags:
  - MoDebug
  - supervision
  - dual-trace
---

# MoDebug Dual-Trace Supervision

## Scope

监督对象从旧 Track A/B 改为 Trace 3/1：

| Supervisor | Trace | 旧称 | Audit scope |
|------------|-------|------|-------------|
| Nietzsche (`019e88e6-79c4-7280-a1c3-f632d3d3f0bf`) | Trace 3 | Track A | GPU0 training-path records 是否会被误读为正式 DispLoss/augmentation 数据。 |
| Aquinas (`019e88e6-a27d-7d72-9ef4-a8113787f230`) | Trace 1 | Track B | GPU1 CA perturbation smoke 是否会被误读为正式 CA-only sweep。 |

## Current Verdict

| Trace | State | Evidence boundary |
|------|-------|-------------------|
| Trace 1 | formal diagnostic completed | 旧 GPU1 smoke 已废弃；当前结论以 [[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]] 为准。 |
| Trace 3 | formal real training running | 旧 GPU0 path-validation 已废弃；当前训练以 `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace3_formal_train_ds_review_20260603_gpu0/` 为准。 |

## Next

本页只保留早期监督边界，不再承载当前实验状态。当前状态见 [[2026-06-02_ds_formal_experiment_gate]]、[[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]] 和各 Trace README。
