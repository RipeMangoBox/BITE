---
title: "Dual Trace Bounded Validation Status"
created: 2026-06-02T23:50:00+08:00
updated: 2026-06-03T16:45:02+08:00
status: validation_only
tags:
  - MoDebug
  - bounded-validation
  - trace_1
  - trace_3
---

# Dual Trace Bounded Validation Status

> [!warning] 非正式实验结果
> 本记录只说明 DS 批准的 bounded validation 是否跑通。所有产物均为 `engineering_validation_only`，不得作为正式实验指标、论文图表或性能 claim。
> 2026-06-03 接力更正：该 run 不满足用户要求的正式 Line 1/Line 3 实验定义；此前把它汇报成“双 Trace 测试完成”是不准确的。

## DS 批准

DS 二次复核结论：`APPROVED_FOR_VALIDATION`。允许 Trace 1 和 Trace 3 双卡并行启动，预估总耗时不超过 10 分钟。

## 远端根目录

`/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dual_trace_validation/20260602_trace1_trace3_ds_pending/`

## 运行结果（仅验证）

| Trace | GPU | 状态 | wall time | 关键检查 |
|------|-----|------|-----------|----------|
| Trace 1 | GPU1 | `exit_code=0` | 36 秒 | `alpha=1` no-op 与 baseline 精确一致；`alpha=0.5`、`alpha=0`、all-layer `alpha=0` 均非全等。 |
| Trace 3 | GPU0 | `exit_code=0` | 14 秒 | 真实 HumanML3D debug train path 跑满 3 step；loss 无 NaN/Inf；未保存 checkpoint。 |

## Trace 1 检查

- `summary.json`: `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dual_trace_validation/20260602_trace1_trace3_ds_pending/trace1_ca_gpu1/summary.json`
- `noop_alpha_1_selected`: `l2_vs_baseline = 0.0`，`max_abs_vs_baseline = 0.0`，`allclose_vs_baseline = true`
- `selected_layers_alpha_0p5`: `l2_vs_baseline = 153.4524688720703`
- `selected_layers_alpha_0p0`: `l2_vs_baseline = 182.4063720703125`
- `all_layers_alpha_0`: `l2_vs_baseline = 249.8477325439453`

限制：本次 prompt 文件实际只含 1 条 prompt（`a man jumps.`），因此只能验证 hook 可控性，不能验证层级重要性。

## Trace 3 检查

- `loss_steps.json`: `/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/dual_trace_validation/20260602_trace1_trace3_ds_pending/trace3_train_gpu0/loss_steps.json`
- step 1: `loss_mot_rec = 1.394436240196228`
- step 2: `loss_mot_rec = 1.6559072732925415`
- step 3: `loss_mot_rec = 1.4542244672775269`
- manifest `actual_steps = 3`
- checkpoint: `null`

限制：未实现 DispLoss 或 augmentation；不能作为训练收益证据。

## Provenance

| Artifact | SHA256 |
|----------|--------|
| Trace 1 script | `51a1d070c00c345061d36350fd5253c855b2946d277d796e2fc046eb9d778de8` |
| Trace 3 script | `b46934bc269888900021b275632ec135559dea45941c33fb2cc1d5d34b49d105` |
| Trace 1 command | `41f1c941e7fb17411b0c3acb6cf25064d777327af02504186a68d7b5799cd636` |
| Trace 3 command | `933529b934e895575dda3e1f277a22b3cc0d99461c80fc5bd1b96c53644075c5` |

## Superseded Status

本页的 Trace 1 下一步已由 formal diagnostic 完成并取代，结果见 [[trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。Trace 3 仍需真实训练消融；不得用本次 3-step validation 代替。
