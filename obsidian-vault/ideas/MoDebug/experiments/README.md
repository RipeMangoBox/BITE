---
title: "MoDebug Experiments Index"
created: 2026-06-03T16:45:02+08:00
updated: 2026-06-16T02:30:00+08:00
status: active
tags:
  - MoDebug
  - experiments
  - index
---

# MoDebug Experiments Index

> [!abstract] Baseline-first 规则
> `experiments/` 第一级按 baseline 命名。历史 v2 实验入口已移到 `experiments/archived/v2/`；当前可执行进度主要集中在 MoLingo SLAD。

## Baselines

| Baseline | 当前状态 | 入口 |
|----------|----------|------|
| MotionCLR | Trace 1 formal diagnostic completed；Trace 3 real training archived | [[motionclr/README]] |
| MoLingo | SLAD v3 四轮实验完成：M0 → GDC → SLAD vs baselines → Ablation (三组件贡献为零)。简化版 SLAD multi-seed 验证进行中（2026-06-15）。 | [[molingo/2026-06-14_slad_history]] |
| MotionGPT | 本地 repo 存在；待确认是否有可比 CFG 与可 hook cross-attention | 待建 |
| MotionStreamer | 本地 repo 存在；待确认是否有可比 CFG 与可 hook cross-attention | 待建 |
| MotionAgent | 4090 `/data/public/ripemangobox/Motion` 下未发现本地 repo | 待定位 |

跨 baseline CA/CFG 门禁见 [[experiments/archived/v2/2026-06-03_cross_baseline_ca_cfg_gate]]。

## Cross-baseline summaries

- [[4090_dual_gpu_experiment_summary_20260604/report|2026-06-04 4090 双卡实验结果整理]]：GPU0 MotionCLR Trace3 训练候选、GPU1 MotionCLR/MoLingo Trace1 layer sweep 汇总，含 proxy 指标图表与 official evaluator 限制说明。

## Recent handoff

- [[molingo/2026-06-14_slad_history]]：2026-06-13~2026-06-14 的 MoLingo SLAD 接力记录，包含 M0 formal suites、diagnostic boundary 和下一步 GDC 校准。
- [[experiments/archived/v2/README]]：2026-06-03 以前的历史实验门禁、监督记录和分析页。

## 目录约定

- baseline 目录名使用小写：`motionclr/`、`molingo/`、`motiongpt/`、`motionstreamer/`。
- 诊断图、派生表格和短分析可以进入 vault；原始 `summary.json`、log、checkpoint、motion outputs 继续留在 4090 experiment 目录。
- 每个 baseline 的 CA/CFG 实验必须先有 DS 复核记录，再启动 GPU run。
