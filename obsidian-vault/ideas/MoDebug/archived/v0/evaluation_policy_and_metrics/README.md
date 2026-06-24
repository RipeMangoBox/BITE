---
title: "MoDebug Archive - Evaluation Policy and Metrics"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - evaluator
  - metrics
---

# Evaluation Policy and Metrics

> [!warning] Archive boundary
> These notes preserve old evaluator policy and conceptual framing. Current metric naming and evaluator boundaries are in [[ideas/MoDebug/README]].

## Read Order

1. [[2026-04-29_modebug-heldout-eval-policy]]
2. [[2026-04-29_modebug-full-vs-event-level-alignment-analysis]]

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| held-out separation | A scorer / protocol used for reward, reranking, selection, filtering or tuning cannot be the final main-table evaluator for the same claim. | `2026-04-29_modebug-heldout-eval-policy.md` |
| full-level safety | Full-level metrics are safety checks, not proof of event-level correctness. | `2026-04-29_modebug-full-vs-event-level-alignment-analysis.md` |
| TMR role | Semantic side signal, especially for omission / replacement diagnostics; not a standalone event-aware or ordering judge. | both notes |
| ChronAccRet role | Ordering / chronology side signal under reported coverage and event buckets; not a full event-correctness or duration evaluator. | both notes |
| MotionPatches / MLLM sidecars | Representation or evidence sidecars only unless revalidated under a separate protocol; not formal judge chains in these archived notes. | both notes |

## Redundancy Handling

The held-out policy gives the hard rule. The full-vs-event note gives motivation and old evaluator-stack context. If they conflict with [[ideas/MoDebug/README]], the active README wins.

## Current Boundary

These notes are policy background. They do not certify any archived metric as final evidence. Every metric reused from this archive must record date, artifact path, evaluator, protocol, data source, condition pair, evaluable n, coverage, role, used_for, and limitations.
