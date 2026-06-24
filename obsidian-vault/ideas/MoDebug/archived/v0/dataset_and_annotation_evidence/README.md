---
title: "MoDebug Archive - Dataset and Annotation Evidence"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - dataset
  - annotation
---

# Dataset and Annotation Evidence

> [!warning] Archive boundary
> This folder preserves old dataset and annotation evidence. Revalidate paths, coverage, and current active use before making any new claim.

## Read Order

1. [[2026-04-27_modebug-planb-open-event-temporal-dataset-audit]]
2. [[dataset_readiness_manifest_v1]]
3. [[2026-04-27_modebug-planb-finemotion-weak-supervision-audit]]
4. `humanml3d_family_audit_v1.json`

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| same-shape ordered-event data | Historical audit found no second open dataset matching HumanML3D-E's `prompt -> ordered event list` shape. | `2026-04-27_modebug-planb-open-event-temporal-dataset-audit.md` |
| HumanML3D family readiness | HumanML3D, HumanML3D-E, HumanML3D-E-MP and HumanML3D-272-self were recorded as ready; 272-dim-HumanML3D train was partial. | `dataset_readiness_manifest_v1.md` |
| FineMotion | Useful as body-part / local-evidence weak supervision sidecar; not a clean single-label GT and not a replacement for ordered-event data. | `2026-04-27_modebug-planb-finemotion-weak-supervision-audit.md` |
| FineMoGen / FrankenMotion / ActionPlan | Potential sidecar or future expansion material; not a direct HumanML3D-E replacement in these notes. | `2026-04-27_modebug-planb-open-event-temporal-dataset-audit.md` |
| BABEL / TEACH | Recorded as missing or not locally ready in the old readiness snapshot. | `dataset_readiness_manifest_v1.md` |

## Redundancy Handling

`dataset_readiness_manifest_v1.md` and the FineMotion audit overlap on FineMotion. Use the readiness manifest for local file status and counts; use the FineMotion audit for the role decision: BPMSD first, BPMP as reading support, no hard single-label claim.

The open temporal dataset audit and readiness manifest overlap on HumanML3D-E. Use the open temporal dataset audit for dataset comparison; use the readiness manifest for local asset status.

## Current Boundary

These notes were written during the EventT2M-era Plan B. They can still inform dataset search and sidecar design, but they do not make EventT2M active again and do not establish a final evaluator.
