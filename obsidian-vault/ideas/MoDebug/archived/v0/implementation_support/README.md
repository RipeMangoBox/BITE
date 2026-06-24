---
title: "MoDebug Archive - Implementation Support"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - implementation
  - primer
---

# Implementation Support

> [!warning] Archive boundary
> These notes are learning and feasibility support. They are not current implementation tickets.

## Read Order

1. [[2026-04-29_modebug-rl-paper-oriented-primer]]
2. [[2026-04-28_modebug-planb-rl-primer]]
3. [[2026-04-30_modebug-render-video-mllm-sidecar-feasibility]]

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| RL concept bridge | MoDebug-era RL language was mainly used to reason about reward, policy optimization, advantage, DPO / GRPO-like families, and inference-time guidance. | both RL primers |
| paper-oriented framing | The shorter paper-oriented primer is the faster entry for writing and related-work positioning. | `2026-04-29_modebug-rl-paper-oriented-primer.md` |
| detailed primer | The longer primer is for zero-background ramp-up and contains more step-by-step explanation. | `2026-04-28_modebug-planb-rl-primer.md` |
| render-to-video / MLLM sidecar | Historical fallback for evidence routing and escalation; not a formal final evaluator and not the current first implementation path. | `2026-04-30_modebug-render-video-mllm-sidecar-feasibility.md` |

## Redundancy Handling

The two RL primers overlap heavily. Prefer the paper-oriented primer for quick review and the long primer only when terminology or mechanics are unclear.

The MLLM sidecar note depends on old EventT2M attention-filter assumptions. Treat it as a future sidecar feasibility note, not as active design.

## Current Boundary

Before using any implementation idea from this folder, check the active cross-generator plan and current codebase state. Do not import old EventT2M-specific implementation assumptions into MotionGPT / MoMask / MoGenTS work without revalidation.
