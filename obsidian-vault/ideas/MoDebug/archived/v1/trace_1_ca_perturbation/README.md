---
title: Trace 1 — CA Layer Perturbation
created: 2026-06-02
updated: 2026-06-14T00:00:00+08:00
status: diagnostic_completed
---

# Trace 1: CA Layer Perturbation

对应 Line 1，旧称 Track B。完整设计见 [[archived/v2/2026-06-02_modebug_reboot_plan#3 Trace 1 — CA 层扰动诊断]]。

## Status

- MotionCLR release checkpoint 已配置。
- MotionCLR float32 pipeline probe 和 official generate CLI probe 已通过，但均为工程验证。
- GPU1 `20260602_gpu1_track_b_ca_cfg_sweep_mvp/` 已降级为 engineering smoke；empty `cond_indices` 不是 CA-only。
- 2026-06-03 DS 已批准 formal candidate；`modebug_trace1_formal_20260603` 已完成 formal diagnostic layer sweep。
- 正式结果目录：`/data/public/ripemangobox/Motion/experiments/MoDebug/motionclr/formal_candidates/trace1_formal_layer_sweep_ds_review_20260603_gpu1/`。
- 36 个逐层 layer group 已完成，controls passed，分析和折线图见 [[experiments/motionclr/trace1_formal_layer_sweep/2026-06-03_trace1_formal_layer_sweep_analysis]]。

## Valid Entry Criteria

- 使用真实 release checkpoint 和真实 prompt。
- 扰动真实 `ResidualCLRAttentionLayer.cross_attention` 输出，而不是 empty `cond_indices`。
- `alpha=1` no-op 必须与未 hook baseline 逐位一致。
- 所有运行记录、命令、manifest 和 DS 复核记录写入 `experiments/` 或远端 experiment 目录。

## Next

- [x] 提交 CA output scaling hook、CFG hidden replacement hook、controls 和命令给 DS。
- [x] 运行 `dev_validation_only` 最小入口检查：18 层、2 个 no-op、2 个 positive control、36 个逐层组均通过。
- [x] 完成 formal diagnostic manifest/summary；`failures=[]`，no-op 与 positive controls 均符合预期。
- [ ] 下一轮只把 L0-L3 与 L12-L15 作为候选层；L2 结果不得直接写成质量或 paper-level 指标。
