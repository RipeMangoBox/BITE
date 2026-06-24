---
title: "MoDebug Archive - Readiness and Assets"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - readiness
  - assets
---

# Readiness and Assets

> [!warning] Archive boundary
> This folder preserves old environment and asset status. Do not assume paths or blockers are current.

## Read Order

1. [[missing_assets_report_v1]]
2. [[baseline_readiness_manifest_v1]]
3. [[baseline_repo_registry_v1]]
4. [[smoke_logs_v1]]

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| missing assets | Old blockers were separated into baseline, dataset, paper-only, and process blockers. | `missing_assets_report_v1.md` |
| baseline readiness | Early baseline status snapshot, useful for reconstructing what was considered ready / partial / blocked. | `baseline_readiness_manifest_v1.md` |
| repo registry | Old local repository inventory and missing canonical repos. | `baseline_repo_registry_v1.md` |
| smoke logs | Early smoke status for EventT2M, ActionPlan, ReAlign, MotionFix and MotionReFit. | `smoke_logs_v1.md` |
| binary assets | `assets/Zoom in论文调研.pdf` and `assets/优势坍塌问题.pdf` are retained as source PDFs referenced by older notes. | `assets/` |

## Redundancy Handling

Use `missing_assets_report_v1.md` for blockers. Use the readiness manifest and registry only when you need the old status classification or repo inventory. Use smoke logs only for historical execution reconstruction.

## Current Boundary

This folder does not certify current environment readiness. For new remote or local experiments, create fresh provenance with current git status, command, log path, artifact path, evaluator role, protocol, and limitations.
