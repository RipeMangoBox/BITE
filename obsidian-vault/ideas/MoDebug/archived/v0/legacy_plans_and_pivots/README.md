---
title: "MoDebug Archive - Legacy Plans and Pivots"
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-08T16:39:02+08:00
status: archived
tags:
  - MoDebug
  - archived
  - plan
  - pivot
---

# Legacy Plans and Pivots

> [!warning] Archive boundary
> This folder preserves old plan shapes. Files with historical `status: active` are not active now.

## Read Order

1. [[2026-04-25_modebug-pivot-implicit-event-repair]]
2. [[2026-04-30_modebug-paper-a-eventprobe-plan]]
3. [[2026-04-30_modebug-paper-b-perceptguide-plan]]
4. [[2026-05-01_modebug-spatiotemporal-extension-backlog]]
5. [[separate_paper_README]]

## Consolidated Conclusions

| Topic | Compressed conclusion | Primary raw source |
| --- | --- | --- |
| pivot away from explicit localization | Old localization + repair chain was judged too brittle; implicit event-level reward / process-time guidance became the preferred historical direction. | `2026-04-25_modebug-pivot-implicit-event-repair.md` |
| split-paper shape | Paper A was EventProbe-style diagnosis; Paper B was PerceptGuide-style reward guidance. This split is historical, not current paper structure. | Paper A / Paper B plan notes |
| PerceptGuide gate | PerceptGuide should not become a method branch without mechanism evidence and go/no-go gates. | `2026-04-30_modebug-paper-b-perceptguide-plan.md` |
| spatiotemporal extension | Time-space parallel control was explicitly postponed until core B1/B2 stability. | `2026-05-01_modebug-spatiotemporal-extension-backlog.md` |

## Redundancy Handling

The pivot note and split-paper plans repeat the motivation for avoiding post-hoc repair. Use the pivot note for the historical reason; use Paper A / Paper B only if you need old contribution lists or old independent-writing gates.

## Current Boundary

Do not revive these plans in place. If any route becomes relevant, write a new active note with a drift note:

```text
old_plan -> new_plan -> evidence -> affected_docs -> next_action
```
