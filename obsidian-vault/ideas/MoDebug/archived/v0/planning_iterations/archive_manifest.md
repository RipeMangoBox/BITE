---
created: 2026-05-07T00:30:45+08:00
updated: 2026-05-08T16:39:02+08:00
title: "MoDebug Archive Manifest"
status: archived
tags:
  - MoDebug
  - archived
  - manifest
---

# MoDebug Archive Manifest

This manifest indexes MoDebug archived files after the 2026-05-08 reclassification. These files are retained for provenance, not active planning.

## Active Source Boundary

Use active files first:

1. [[ideas/MoDebug/README]]
2. [[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]

Use blocked EventT2M files only through [[ideas/MoDebug/blocked/README]].

## Category Map

| Group | Path | Role | Current action |
| --- | --- | --- | --- |
| dataset and annotation evidence | `dataset_and_annotation_evidence/` | HumanML3D-E, FineMotion, open temporal annotation alternatives, dataset readiness | read the category README first; revalidate asset paths before reuse |
| related work and backbone comparison | `related_work_and_backbone_comparison/` | old Plan B reading list, APPO / PRCO bridges, backbone and evaluator candidate matrix | use for background and candidate history only |
| evaluation policy and metrics | `evaluation_policy_and_metrics/` | held-out separation policy and full-level vs event-level distinction | use as policy background; active README is canonical |
| legacy plans and pivots | `legacy_plans_and_pivots/` | old pivot, split-paper drafts, postponed spatiotemporal backlog | historical only; do not revive without a new active note |
| implementation support | `implementation_support/` | RL primers and render-to-video / MLLM sidecar feasibility | background only; not current implementation plan |
| readiness and assets | `readiness_and_assets/` | old baseline registry, missing assets, smoke logs, binary source PDFs | provenance and environment history only |
| review reports and prompts | `review_reports_and_prompts/` | review prompts and group-meeting report | useful for narrative reconstruction, not evidence promotion |

## Old-to-New Map

| Former location | Current location |
| --- | --- |
| root `2026-04-26_modebug-plan-b-core-reading-list.md` | `related_work_and_backbone_comparison/2026-04-26_modebug-plan-b-core-reading-list.md` |
| root `2026-04-29_modebug-heldout-eval-policy.md` | `evaluation_policy_and_metrics/2026-04-29_modebug-heldout-eval-policy.md` |
| root `2026-05-07_modebug-backbone-comparison-archive.md` | `related_work_and_backbone_comparison/2026-05-07_modebug-backbone-comparison-archive.md` |
| `legacy_raw/audits/` | `dataset_and_annotation_evidence/` |
| `legacy_raw/backlog/` | `legacy_plans_and_pivots/` |
| `legacy_raw/bridges/` | `related_work_and_backbone_comparison/` |
| `legacy_raw/concepts/` | `evaluation_policy_and_metrics/` |
| `legacy_raw/implementation-support/` | `implementation_support/` |
| `legacy_raw/readiness/dataset_readiness_manifest_v1.md` | `dataset_and_annotation_evidence/dataset_readiness_manifest_v1.md` |
| other `legacy_raw/readiness/` files | `readiness_and_assets/` |
| `legacy_raw/review-prompts/` | `review_reports_and_prompts/` |
| `legacy_raw/separate_paper/` | `legacy_plans_and_pivots/` |
| `legacy_raw/transition/` | `legacy_plans_and_pivots/` |
| `legacy_raw/assets/` | `readiness_and_assets/assets/` |

## Consolidation Rule

The category README files are the de-duplicated reading layer. Original notes remain intact for provenance. When two notes repeat a conclusion, cite the category README first, then cite the original note only when exact historical wording, artifact paths, or table values are needed.

## Do Not Promote

Do not promote any archived file into:

1. current backbone selection;
2. current evaluator selection;
3. final evaluation evidence;
4. claim wording;
5. active related notes.

If a raw archived file becomes relevant again, create a new active note with current provenance, evaluator role, protocol, and limitations instead of reviving the old file in place.
