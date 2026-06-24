---
title: "MoDebug archived 索引"
created: 2026-04-28T00:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - index
---

# MoDebug Archived Index

This folder is historical context, not an active source of truth. It is organized by reuse purpose rather than by the original working folder names.

Current active MoDebug files:

1. [[ideas/MoDebug/README]]
2. [[paperIDEAs/MoDebug/2026-05-11_modebug-route-2-cross-generator-failure-mechanism]]

EventT2M-era blocked files live in [[ideas/MoDebug/blocked/README]].

## Current Structure

| Path | Role |
| --- | --- |
| `README.md` | this index |
| `archive_manifest.md` | complete category manifest and old-to-new provenance map |
| `dataset_and_annotation_evidence/` | dataset comparison, annotation readiness, HumanML3D family audit, FineMotion sidecar evidence |
| `related_work_and_backbone_comparison/` | old reading list, APPO / PRCO bridges, backbone and evaluator candidate comparison |
| `evaluation_policy_and_metrics/` | held-out policy and full-level vs event-level alignment explanation |
| `legacy_plans_and_pivots/` | pivot notes, old Paper A / Paper B split plans, future backlog |
| `implementation_support/` | RL primers and render-to-video / MLLM sidecar feasibility |
| `readiness_and_assets/` | baseline registry, missing assets, smoke logs, source PDFs |
| `review_reports_and_prompts/` | review prompts and group-meeting report |

Each category has its own `README.md` with a compressed summary and de-duplication guidance. Open the category README before reopening raw notes.

## Use Rule

Archived files may be used for:

1. historical context;
2. old prompt or review reconstruction;
3. provenance lookup;
4. paper/background inspiration after revalidation.

Archived files must not be used as:

1. current MoDebug plan;
2. current eval/backbone selection evidence;
3. final metric source;
4. claim support without rechecking the active README and migration plan.

If an archived note has `status: active` in frontmatter, treat that status as historical. Its current status is archived by folder boundary.

## 2026-05-07 Cleanup Note

The directory was compressed from many topic subfolders into `legacy_raw/`. No content was deleted in this cleanup. EventT2M-dependent roadmap / exec / evaluator-status / attention-support files were moved out of `archived/` into `blocked/legacy_eventt2m/` because their risk is not ordinary historical drift but blocked backbone dependency.

## 2026-05-08 Reclassification Note

The `legacy_raw/` compression has been replaced by content-purpose categories. Original files were moved into their closest category, with class-level README files added to reduce repeated reading and clarify redundant or superseded material. Provenance is preserved through [[archive_manifest]].
