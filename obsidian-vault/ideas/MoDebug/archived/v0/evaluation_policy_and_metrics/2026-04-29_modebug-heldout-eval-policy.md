---
created: 2026-04-29T23:37
updated: 2026-05-01T15:05:48+08:00
title: MoDebug Held-Out Eval Policy
status: active
task_id: MDBG-HELDOUT-POLICY
tags:
  - MoDebug
  - evaluator
  - heldout_eval
  - reward_guidance
  - EventT2M
  - ChronAccRet
  - TMR
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
---

# MoDebug Held-Out Eval Policy

> [!abstract] **Policy TL;DR**
> - 硬规则：被用作 reward 的 scorer/protocol 不能同时作为 final main-table evaluator。
> - `Event-T2M self eval` 只作 full-level safety，不作 event-level reward scorer，也不作 event-level final judge。
> - `AToM` 只记录 MotionGPT native eval reproduction，不进入 MoDebug formal scorer / evaluator chain。
> - `MotionPatches` 不进入任何 formal chain。
> - 如果没有 independent final evaluator，则对应 reward 结果只能写作 development metric / ablation，不进入主表最终结论。

## 1. Scope

本 note 固定 MoDebug 的 held-out eval policy，服务于 [[ideas/MoDebug/README]]、[[2026-04-29_modebug-roadmap]]、[[2026-04-29_modebug-exec-plan]] 与 [[2026-04-29_modebug-evaluator-status-summary]]。

它只定义 evaluator / reward 的角色隔离规则。held-out 是实验卫生与公平性要求，不是 Paper A 或 Paper B 的独立贡献点。本 note 不新增实验，不整理 archived 文件，不修改现有 roadmap / exec。

## 2. Hard Separation Rule

MoDebug 的正式结论必须满足：

```text
reward scorer/protocol != final main-table evaluator/protocol
```

含义：

1. 如果某个 scorer 或 protocol 直接参与 inference-time reward、reranking、selection、filtering 或 reward-weight tuning，它只能作为 development metric。
2. 同一个 scorer 的同一个 corruption protocol 不能再作为 final main-table 的主 evaluator。
3. 可以报告 reward-side metric 作为 diagnostic，但必须明确标注为 development / reward-side。
4. final main-table 需要使用 held-out evaluator、human eval，或至少使用不同 scorer / 不同 protocol 的 cross-check。
5. 若 held-out evaluator 不可用，该 reward 分支不能写成主表最终提升，只能写 observation、ablation 或 failure analysis。

## 3. Formal Role Definitions

| Component | Allowed role | Forbidden role |
| --- | --- | --- |
| Event-T2M self eval | full-level safety: FID, R-Precision, matching score | event-level reward scorer; event-level final main-table evaluator |
| native TMR | omission / presence development metric or held-out omission evaluator when not used as reward | formal ordering judge; standalone all-purpose final judge |
| ChronAccRet omission | omission cross-check or held-out omission evaluator when not used as reward | full HumanML3D-E coverage claim; duration judge |
| ChronAccRet ordering | formal ordering evidence or R_ord development metric, but not both for the same final claim | final ordering main-table evaluator if used as R_ord reward |
| attention-derived signal | observation feature or reward candidate after sensitivity checks | raw attention final judge |
| AToM | MotionGPT native eval reproduction record | MoDebug main judge; event-level formal evaluator |
| MotionPatches | no formal role | reward scorer; dev metric; final evaluator; formal chain component |

## 4. Held-Out Configuration Matrix

| Reward case | Dev metric during tuning | Final evaluator for main-table claim | Full-level safety config | Policy status |
| --- | --- | --- | --- | --- |
| `R_pres = TMR` | native TMR full-vs-drop / full-vs-replace paired score; TMR bucket report; optional TMR and ChronAccRet consistency as diagnostic | ChronAccRet omission protocol or human omission eval; TMR cannot be the final omission main evaluator for this claim | Event-T2M self eval on the same generation set: FID, R-Precision, matching score; report delta vs baseline | allowed if ChronAccRet omission or human eval is held out |
| `R_pres = ChronAccRet` | ChronAccRet omission full-vs-drop / full-vs-replace paired score; ChronAccRet subset coverage report | native TMR omission protocol or human omission eval; ChronAccRet omission cannot be the final omission main evaluator for this claim | Event-T2M self eval on the same generation set: FID, R-Precision, matching score; report delta vs baseline | allowed if TMR or human eval is held out |
| `R_ord = ChronAccRet` | ChronAccRet shuffle / CAR-style ordering score; shuffle sensitivity diagnostics | human ordering eval or a separate independent ordering scorer; ChronAccRet cannot be the final ordering main evaluator for this claim | Event-T2M self eval on the same generation set: FID, R-Precision, matching score; report delta vs baseline | blocked for final main-table unless independent ordering eval exists |
| attention-derived reward | attention separation, entropy, temporal peak order, counterfactual sensitivity to drop / replace / shuffle; no raw attention final score | TMR for omission if attention reward targets presence; ChronAccRet omission for presence cross-check; ChronAccRet ordering or human eval for ordering, depending on target; attention itself cannot be final evaluator | Event-T2M self eval on the same generation set: FID, R-Precision, matching score; report delta vs baseline | allowed only as reward / observation feature, never as final judge |

## 5. Full-Level Safety Rule

`Event-T2M self eval` is reserved for full-level safety only.

Required reporting for any reward-guided generation:

1. Run the same Event-T2M self eval family as baseline and guidance output.
2. Report FID / R-Precision / matching score deltas.
3. If event-side score improves while full-level safety degrades clearly, the run is treated as reward hacking risk.
4. Full-level safety pass does not prove event-level correctness; it only permits event-level held-out evaluation to be interpreted.

Policy consequence:

```text
event-side gain + full-level safety fail -> no final main-table claim
event-side gain + full-level safety pass + held-out evaluator pass -> eligible for main-table claim
event-side reward metric gain only -> development result only
```

## 6. Specific Exclusions

1. `AToM` remains a MotionGPT native eval reproduction record only.
2. `AToM` must not be described as a MoDebug event-level judge for omission, ordering, or duration.
3. `MotionPatches` is excluded from reward scoring, development metrics, final evaluation, and formal judge chains.
4. `TMR Phase 1` / `PAPO-lite` historical diagnostics are not formal held-out evaluators.
5. Duration has no formal evaluator in the current policy and must not be claimed as covered.

## 7. Claim Wording

Allowed:

> MoDebug separates reward-side development metrics from final held-out evaluators. Any scorer used for reward guidance is excluded from serving as the final main-table evaluator for the same event-level claim.

Allowed with condition:

> A TMR-guided presence reward may be evaluated by ChronAccRet omission or human omission evaluation, while Event-T2M self eval is used only to verify full-level generation safety.

Not allowed:

1. "TMR reward improves TMR final eval, therefore omission is solved."
2. "ChronAccRet ordering reward improves ChronAccRet CAR, therefore ordering is solved."
3. "Event-T2M self eval proves event-level correctness."
4. "AToM is the MoDebug temporal judge."
5. "MotionPatches participates in the formal evaluation chain."

## 8. Paper-Safe Final Policy

For MoDebug, every reward branch must declare three separate slots before it can enter the main result table:

1. `reward_metric`: the scorer/protocol used for reward, reranking, selection, or tuning.
2. `heldout_final_evaluator`: an independent evaluator/protocol not used as the reward metric.
3. `full_level_safety`: Event-T2M self eval only.

If any slot is missing, the result remains a development ablation and cannot be written as a final event-level improvement.
