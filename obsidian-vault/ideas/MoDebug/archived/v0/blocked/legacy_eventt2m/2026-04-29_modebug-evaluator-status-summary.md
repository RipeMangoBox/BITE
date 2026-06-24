---
created: 2026-04-29T13:46
updated: 2026-05-01T15:05:48+08:00
title: MoDebug Evaluator Status Summary
status: active
tags:
  - MoDebug
  - evaluator
  - summary
  - ChronAccRet
  - AToM
  - TMR
  - EventT2M
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
  - "[[2026-04-28_tamr-core-materials-and-temporal-semantic-evaluator-review]]"
---

# MoDebug Evaluator Status Summary

> [!abstract] **TL;DR**
> - 当前正式 evaluator 栈为：`Event-T2M self eval` + `native TMR omission / semantic side signal` + `ChronAccRet formal ordering evidence / omission cross-check`。
> - 多事件主数据口径固定为 `HumanML3D-E`；`ChronAccRet event_texts` 只作为 ChronAccRet runner 的输入适配层。
> - 已将原 `4` 样本 TMR Phase 1 诊断替换为 dataset-level native TMR omission eval：`HumanML3D-E` multi-event test `N = 3799`。
> - `ChronAccRet` ordering full `4068` 结果为 `chron_subset_ord_shuffle_car = 0.6473616473616474`，有效样本 `2331 / 2333`；omission protocol 已补齐，`chron_subset_pres_full_vs_drop_paired_acc = 0.7299614230604372`，`chron_subset_pres_full_vs_replace_paired_acc = 0.8551221603086155`。
> - sample-level consistency 当前支持 safe-drop 与 aligned-replace：safe-drop `1179 / 1608 = 73.32%`，`5plus = 51 / 80 = 63.75%`；aligned-replace `1313 / 1608 = 81.65%`，`5plus = 63 / 80 = 78.75%`，但只覆盖 TMR rows 的 `42.33%`。
> - lexical hard-replace 512-row pilot 显示 easy-negative 膨胀风险：`tmr_gt_pres_hard_replace_lexical_paired_acc = 0.65234375`，比 aligned-replace `0.835820895522388` 低 `0.18347714552238803`，`5plus = 0.5555555555555556`。
> - 当前不需要自建 evaluator；omission 已有 native TMR 与 ChronAccRet 两条 retrieval-side 信号，duration 仍无正式 evaluator。

## 1. 数据口径

| Question | Decision |
| --- | --- |
| 多事件数据集用什么 | `HumanML3D-E` 是 MoDebug 的主数据源，因为它同时提供 motion、caption、ordered event decomposition，并且与 `Event-T2M` 主任务对齐 |
| `ChronAccRet event_texts` 是什么 | 只作为 `ChronAccRet` 代码读取的 runner-side event-text input，不替代 `HumanML3D-E` 主数据口径 |
| 当前可复现数据规模 | `Event-T2M / TMR` 侧使用 `HumanML3D-E data_test.npy`，multi-event `N = 3799`；`ChronAccRet` 侧使用其 `humanml3d_subset` loader，ordering full `4068` 中可判别 multi-event `N = 2331`，omission protocol `N = 2333` |

## 2. Evidence Table

| Work / evaluator | Dataset-level evidence | Can evaluate event what | Cannot evaluate event what | Current role |
| --- | --- | --- | --- | --- |
| `Event-T2M self eval` | `HumanML3D-E overall`: `FID = 0.049708280712366104`, `R_precision_top_3 = 0.8366379141807556`; `HumanML3D-E condition3`: `FID = 0.13672851026058197`, `R_precision_top_3 = 0.7912946939468384`; official reference `HumanML3D`: `FID = 0.049953218549489975`, `R_precision_top_3 = 0.8469827771186829` | event-conditioned generation backbone sanity | ordering, omission, duration, judge-style temporal correctness | keep as backbone evidence only |
| native `TMR` | `HumanML3D-E` multi-event test `N = 3799`; `tmr_gt_pres_full_vs_drop_paired_acc = 0.7043958936562253`, mean delta `0.06684182584285736`, std `0.11925547569990158`; `tmr_gt_pres_full_vs_replace_paired_acc = 0.836272703342985`, mean delta `0.12040771543979645`, std `0.12934772670269012`; event buckets `{2: 1940, 3: 1185, 4: 435, 5plus: 239}` | omission / presence-style semantic side signal; global text-motion sanity | formal ordering, duration, localized temporal grounding, standalone final judge | use as frozen omission side signal |
| `ChronAccRet` | ordering full `4068`: `chron_subset_ord_shuffle_car = 0.6473616473616474`, evaluable `2331 / 2333`, skipped degenerate `2`; `subset256`: `CAR = 0.673202614379085`; omission protocol: `chron_subset_pres_full_vs_drop_paired_acc = 0.7299614230604372`, mean delta `0.16408133506774902`; `chron_subset_pres_full_vs_replace_paired_acc = 0.8551221603086155`, mean delta `0.2816697359085083`, `N = 2333` | formal ordering evidence; omission cross-check via full-vs-drop/replace retrieval scoring | duration; single-event and degenerate multi-event ordering | use as frozen ordering judge and omission cross-check |
| `AToM` native `MotionGPT` eval | `FID = 0.18319737911224365`; `Matching_score = 4.085436820983887`; `R_precision_top_3 = 0.6519396305084229`; `Diversity = 8.983773231506348`; `MultiModality = 4.019556999206543` | native `MotionGPT` generation eval reproducibility | current MoDebug event ordering, omission, duration, event-level judge | record as reproduction evidence only |

## 3. Retired Diagnostics

| Diagnostic | Old use | Current decision |
| --- | --- | --- |
| `Event-T2M Phase -1` prompt sensitivity | `4` hand-picked generated samples for `drop / replace / swap` motion-space change | debug-only; not used as reliable evaluator |
| `TMR Phase 0 / 1` PAPO-lite | `4` hand-picked samples with wrapper-defined `R_pres / R_ord` proxy | superseded for omission by native TMR dataset-level eval; `R_ord` proxy is not formal ordering evidence |

`TMR Phase 1` 不是 TMR 原生 evaluator，而是早期为了 PAPO-lite guidance 设计的 wrapper/proxy。它现在只保留为历史 debug 结果，不再写进正式 evaluator 栈。

## 4. TMR Clarification

原生 `TMR` 可以用，而且当前正式 omission 侧信号已经改成原生 `TMR`：在 dataset-level paired comparison（`N = 3799`）中，直接比较同一 GT motion 下 `full event text`、`drop event text`、`replace event text` 的 global text-motion score。

按 event count 拆分后，`5plus` 样本信号明显更弱：`tmr_gt_pres_full_vs_drop_paired_acc = 0.6610878661087866`，`tmr_gt_pres_full_vs_replace_paired_acc = 0.7573221757322176`。因此 native TMR 只作为 omission side signal，而不是 standalone final judge。

## 5. ChronAccRet Omission Protocol

`ChronAccRet` 已新增 `full` vs `drop / replace` scoring protocol，作为 omission 的第二条 retrieval-side 信号：

- artifact:
  - `[[linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_event.yaml]]`
  - `[[linkedCodebases/ChronAccRet/output/bert_orig/omission_eval/omission_rows.jsonl]]`
- `drop_paired_accuracy = 0.7299614230604372`
- `replace_paired_accuracy = 0.8551221603086155`
- `drop_mean_delta = 0.16408133506774902`
- `replace_mean_delta = 0.2816697359085083`
- `num_evaluable = 2333`

## 6. Final Decision

| Question | Answer |
| --- | --- |
| 是否已经把小样本评估升级到 dataset 级别 | `TMR` omission 已升级到 `HumanML3D-E` multi-event test `N = 3799`; `ChronAccRet` ordering 已是 full `4068` eval；`ChronAccRet` omission protocol 已补齐到 `N = 2333`；aligned-replace consistency 已在 `1608` comparable rows 上闭合，但该 `1608` 只占 TMR rows 的 `42.33%` |
| 是否必须自建 evaluator | 现在不必须；omission 已有 native `TMR` 与 `ChronAccRet` 两条 retrieval-side 信号，ordering 使用 `ChronAccRet` |
| 还缺什么 | duration 仍无正式 split；native TMR 的高事件数 omission 信号较弱；hard-replace pilot 显示 replacement 难度会显著改变结论，应避免把 aligned-replace 高分写成 final judge |

## 7. Safe-Drop Consistency Addendum

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/join_diagnostics.json`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/summary.json`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/disagreement_cases.jsonl`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_consistency_eval/top_cases.md`

当前只报告 safe-drop row-level consistency：

1. join key：`sample_id/keyid + target_idx + event_count + dropped_event + full_text + drop_text`
2. comparable rows：`1608`
3. agreement：`1179 / 1608 = 73.32%`
4. `5plus` agreement：`51 / 80 = 63.75%`
5. coverage vs TMR：`42.33%`
6. coverage vs ChronAccRet：`68.92%`

该结果尤其限制 `5plus` bucket：`51 / 80 = 63.75%` 接近弱一致，只能支撑 side evidence，不能支撑 `5plus` reward guidance。

## 8. Aligned-Replace Consistency Addendum

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_manifest.jsonl`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/tmr_aligned_replace_summary.json`
3. `linkedCodebases/ChronAccRet/output/bert_orig/aligned_replace_eval/chronaccret_aligned_replace_event.yaml`
4. `linkedCodebases/EventT2M-codes-main/logs/modebug_aligned_replace_eval/aligned_replace_consistency_summary.json`

当前报告 aligned-replace row-level consistency：

1. join key：`sample_id/keyid + target_idx + event_count + replacement_event + replace_text`
2. comparable rows：`1608`
3. `tmr_safe_subset_pres_full_vs_aligned_replace_paired_acc = 0.835820895522388`
4. `chron_subset_pres_full_vs_aligned_replace_paired_acc = 0.8538557213930348`
5. agreement：`1313 / 1608 = 81.65%`
6. `5plus` agreement：`63 / 80 = 78.75%`

该结果修复了原 replacement mismatch 缺口，但仍只作为 evaluator-side cross-check，不是 standalone final judge。coverage 限制为 TMR rows 的 `42.33%` 与 ChronAccRet rows 的 `68.92%`，不能外推到全量 TMR omission rows。

## 8.1 Lexical Hard-Replace Pilot Addendum

已完成 artifact：

1. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/hard_replace_manifest_summary.json`
2. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_summary.json`
3. `linkedCodebases/EventT2M-codes-main/logs/modebug_hard_replace_eval/tmr_hard_replace_rows.jsonl`

当前报告 lexical hard-replace TMR diagnostic：

1. manifest rows：`512`
2. candidate backend：`lexical`
3. `tmr_gt_pres_hard_replace_lexical_paired_acc = 0.65234375`
4. aligned-replace TMR baseline：`0.835820895522388`
5. delta：`-0.18347714552238803`
6. `5plus` hard-replace：`15 / 27 = 0.5555555555555556`

该结果支持 easy-negative 膨胀风险：replacement 越接近原 event，TMR 越难区分 full 与 replace。它不是正式 evaluator，只是对 aligned-replace 解释边界的 stress test。

## 9. Held-Out Boundary

同步 [[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]]：

1. 被用作 reward 的 scorer/protocol 不能同时作为 final main-table evaluator/protocol。
2. Event-T2M self eval 只作 full-level safety。
3. native TMR 是 omission side signal，不是 standalone final judge。
4. ChronAccRet 是 formal ordering evidence 与 omission cross-check。
5. AToM 只作 MotionGPT native eval reproduction record。
