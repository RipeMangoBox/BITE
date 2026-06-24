---
created: 2026-05-07T00:12:59+08:00
updated: 2026-05-11T20:55:00+08:00
title: "MoDebug Blocked EventT2M Versions"
status: blocked
tags:
  - MoDebug
  - EventT2M
  - blocked
  - index
---

# MoDebug Blocked EventT2M Versions

This folder holds EventT2M-era MoDebug notes and the older non-MLLM local artifact debugging route. They are retained for provenance and route mining, not as the active execution entrance.

Current decision:

1. The old 2026-05-06 scale-abnormality blocker is superseded by the 2026-05-11 `2ac5ea8` revalidation: the `003245` epoch135 single-sample scale sanity returned to HumanML3D scale.
2. That result is still diagnostic only. It is not final evaluator evidence, backbone-selection evidence, or a full EventT2M safety claim.
3. Files here can be used as historical full-level reproducibility records, evaluator-side diagnostic inventory, implementation provenance, or local artifact route background.
4. Files here must not be used as current S7/S8/S10 backbone evidence without a new active note that records current provenance, protocol, evaluator role, `n/evaluable`, coverage, and limitations.
5. Current active planning starts from [[ideas/MoDebug/README]], [[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]], and the route comparison note [[paperIDEAs/MoDebug/2026-05-11_modebug-route-overview]].

## Core Blocked Notes

| File | Status | Allowed use |
| --- | --- | --- |
| [[2026-05-01_modebug-unified-ideas-progress]] | EventT2M-era long progress record | historical provenance and non-MLLM local artifact route source |
| [[2026-05-01_modebug-eventt2m-retrain-sanity-plan]] | EventT2M full-level sanity record | historical reproducibility and checkpoint provenance |
| [[2026-05-05_modebug-s7-component-eval-summary]] | EventT2M-era component inventory | schema and evaluator-side inventory reference only |

## Legacy EventT2M Support

`legacy_eventt2m/` contains old roadmap, exec-plan, evaluator-status and EventT2M-specific implementation-support notes that were previously under `archived/`.

These files are kept because they explain how the EventT2M-era route formed, but they are not current execution material.

| Group | Files |
| --- | --- |
| old roadmap / exec / status | `2026-04-29_modebug-roadmap.md`, `2026-04-29_modebug-exec-plan.md`, `2026-04-29_modebug-evaluator-status-summary.md` |
| local EventT2M evidence | `2026-04-27_modebug-planb-eventt2m-local-evidence-audit.md` |
| EventT2M-era sample / manifest support | `2026-04-27_modebug-planb-hard-negative-seed-pool.md`, `2026-04-27_modebug-planb-ordering-omission-manifest.md` |
| EventT2M-era attention support | `2026-04-29_modebug-attention-extraction-feasibility.md`, `2026-04-29_modebug-attention-filter-evaluator-pipeline-update.md` |

## Use Rule

If a future note cites this folder, it must state the role explicitly:

```text
role: historical_provenance | blocker_evidence | diagnostic_schema | failure_case_background
used_for: observation
```

Do not cite this folder as `backbone_selection`, `eval_selection`, `final_eval`, or active `formal_ordering_evidence`.
