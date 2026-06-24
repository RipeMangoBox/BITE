---
title: "MoDebug Archive - Related Work and Backbone Comparison"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - related_work
  - backbone
---

# Related Work and Backbone Comparison

> [!warning] Archive boundary
> This folder is background for why older routes were considered. Current backbone and evaluator roles are defined in [[ideas/MoDebug/README]].

## Read Order

1. [[2026-05-07_modebug-backbone-comparison-archive]]
2. [[2026-04-26_modebug-plan-b-core-reading-list]]
3. [[2026-04-27_modebug-planb-appo-motion-bridge]]
4. [[2026-04-27_modebug-planb-prco-motion-bridge]]

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| backbone candidates | MotionGPT was prioritized as mechanism-probe candidate; MoGenTS was kept as structural temporal baseline / fallback; LaMP and DART were deferred; EventT2M was removed from active role. | `2026-05-07_modebug-backbone-comparison-archive.md` |
| evaluator / sidecar roles | TMR, ChronAccRet, MotionPatches / TAMR-style sidecars were separated by role; none was treated as a complete final judge. | `2026-05-07_modebug-backbone-comparison-archive.md` |
| Plan B reading route | AToM, ReAlign, MotionCritic, PAPO and EasyTune were old core mechanism references; APPO / PRCO / VideoZoomer / Perception-R1 were high-reference supplements. | `2026-04-26_modebug-plan-b-core-reading-list.md` |
| APPO bridge | Useful historical idea: use attention to mine key local intervals; do not make APPO the reward definition or full training route. | `2026-04-27_modebug-planb-appo-motion-bridge.md` |
| PRCO bridge | Useful historical idea: observer-style evidence sidecar; do not turn the MVP into a two-model agent pipeline. | `2026-04-27_modebug-planb-prco-motion-bridge.md` |

## Redundancy Handling

The reading list and APPO / PRCO bridge notes overlap. Use the reading list for paper ordering and broad competitive positioning; use the bridge notes only when you need the motion-domain mapping of APPO or PRCO.

The backbone archive overlaps with the active cross-generator plan, but only the active plan defines current execution. Use the archive to reconstruct why candidates were accepted, deferred, or excluded on 2026-05-07.

## Current Boundary

This folder is not a current backbone-selection source. Any candidate revived from here needs a new active note with current code provenance, asset status, evaluator role, protocol, and limitations.
