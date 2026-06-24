---
title: "P1 Four-Baseline Skeleton Visualization"
created: 2026-05-21T22:00:00+08:00
updated: 2026-05-21T22:00:00+08:00
type: experiment_visualization_index
tags:
  - MoDebug
  - P1
  - visualization
  - remote4090
---

# P1 Four-Baseline Skeleton Visualization

This directory exposes the fetched skeleton mp4 outputs for all four diagnostic baselines:

| baseline | local entry | mp4 count |
|---|---|---:|
| MotionGPT | `motiongpt/` | 18 |
| MoLingo | `molingo/` | 18 |
| MoMask original | `momask_original/` | 18 |
| MoGenTS | `mogents/` | 18 |

Source artifact root:

- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_vis/vis`

Record:

- `artifacts/remote4090/modebug_p1_1e3_four_baseline_20260521_vis/vis/vis_record.json`

Boundary: these videos are qualitative diagnostic skeleton renders only. They are not held-out final evaluator evidence and should not be used as metric evidence.
