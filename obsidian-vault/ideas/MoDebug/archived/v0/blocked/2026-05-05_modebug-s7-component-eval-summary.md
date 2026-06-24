---
created: 2026-05-05T23:20:00+08:00
updated: 2026-05-11T20:55:00+08:00
title: "MoDebug S7 Component Eval Summary"
status: diagnostic
tags:
  - MoDebug
  - S7
  - component-eval
  - diagnostics
  - EventT2M
  - blocked
---

# MoDebug S7 Component Eval Summary

> [!warning]
> This note summarizes EventT2M/TMR/ChronAccRet component assets only. The later 2026-05-11 EventT2M single-sample scale sanity repair does not turn this component inventory into an active S7 table. S7 table closure still needs a current active protocol, generated-motion manifest, evaluator coverage, and human-calibrated role boundaries.

## Scope

- EventT2M / native TMR omission dataset eval
- Generation observation condition manifest
- Aligned-replace manifest + TMR eval + TMR/ChronAccRet consistency
- Hard-replace lexical pilot
- Safe-drop consistency

## Machine-Complete Assets

| Component | Artifact | Key result | Role / boundary |
| --- | --- | --- | --- |
| Native TMR omission dataset eval | `linkedCodebases/EventT2M-codes-main/logs/planb_tmr_native_omission_dataset_eval/summary.json` | `num_samples=3799`; `paired_accuracy_full_gt_drop=0.7044`; `paired_accuracy_full_gt_replace=0.8363` | automatic side signal; not held-out final evaluator |
| Condition manifest | `linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/condition_manifest_summary.json` | `sample_count=64`; `condition_rows=256`; 4 conditions complete; `fixed_seed_complete=true` | generation observation input manifest only |
| Aligned-replace manifest | `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_manifest_summary.json` | `manifest_rows=1608`; `safe_drop_join_rows=1608` | evaluator-side cross-check asset |
| TMR aligned-replace eval | `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/tmr_aligned_replace_summary.json` | `full>replace paired_accuracy=0.8358` on `1608` rows | diagnostic / observation |
| TMR / ChronAccRet aligned-replace consistency | `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_consistency_summary.json` | agreement `0.8165` on `1608` joined rows | cross-evaluator diagnostic, not final judge |
| TMR hard-replace lexical pilot | `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json` | `full>replace paired_accuracy=0.6523` on `512` rows; vs old aligned-replace `-0.1835` | supports easy-negative inflation risk; not a formal hard-replace benchmark |
| Safe-drop consistency | `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/summary.json` | agreement `0.7332`; `5plus` bucket agreement `0.6375` | cross-evaluator diagnostic; human calibration still required |

## What Is Still Missing

1. A current active S7 protocol that names the route being tested: local-artifact debugging, cross-generator mechanism, negative-pair training, or adaptive failure-space routing.
2. Per-generator or per-route manifests with repo, checkpoint, prompt adapter, motion format, length protocol, seed, generated-motion artifact path, evaluator coverage, and limitations.
3. A single S7 orchestrator or per-baseline table builder that merges only route-approved outputs into one canonical diagnostic table.
4. Human calibration before any disagreement or bucket effect is treated as a true failure-rate statement.

## Decision

As of 2026-05-11, the safe next step is not to reuse this component inventory as an active claim table. Existing EventT2M component outputs remain useful as evaluator-side diagnostic inventory and historical provenance only.
