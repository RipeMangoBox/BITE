---
created: 2026-04-29T22:10
updated: 2026-05-01T15:05:48+08:00
title: "MoDebug: Full-Level vs Event-Level Alignment 本质区别与设计引导"
status: archived
tags:
  - MoDebug
  - alignment
  - event-level
  - evaluator
  - generation
  - architecture
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-attention-filter-evaluator-pipeline-update]]"
  - "[[2026-04-29_modebug-heldout-eval-policy]]"
---

# Full-Level vs Event-Level Alignment 本质区别与设计引导

> [!warning] Archived
> This note is historical concept support. Current MoDebug entry, terms, and active file list are in [[ideas/MoDebug/README]].

> [!abstract] **TL;DR**
> - full text-full motion alignment 是整体语义匹配；event-level alignment 是结构化、时序敏感的局部对齐，二者不能互相替代。
> - event-level 新增约束：保留时序信息、不手动硬切 motion、以 text-side event decomposition 为主要入口、event-level 高分必须与 full-level sanity 一致。
> - MoDebug 当前已用 native `TMR` 与 `ChronAccRet` 接住 omission / ordering 的 retrieval-side evidence；safe-drop consistency、aligned-replace consistency、held-out eval policy、generation observation pool/schema 与 G1/G2 attention logging 已完成。
> - 主数据口径固定为 `HumanML3D-E`；`ChronAccRet event_texts` 只是 runner-side 输入适配层。
> - generation 与 evaluator 可以部分并行：eval 侧冻结 judge 与 held-out policy，generation 侧先做 attention / denoising / gradient sensitivity instrumentation 观测，再进入 reward guidance。

## 1. 数据口径：HumanML3D-E vs ChronAccRet Event Texts

两者不是两套独立标注，而是同源 event decomposition 的不同工程格式。

| 维度    | HumanML3D-E decomposed                                                                     | ChronAccRet event_texts                                                        |
| ----- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| 角色    | MoDebug 主数据口径                                                                              | ChronAccRet runner 输入格式                                                        |
| 格式    | `npy dict -> text[k].decomposed[i].caption`                                                | `{sample}_{annotation}.json -> events: [...]`                                  |
| 覆盖    | test split `4646` samples，含 single-event                                                   | `4068` unique sample IDs，是 HumanML3D-E 子集                                      |
| 多事件覆盖 | `2719` multi-event unique samples；TMR dataset eval 展开到 `N = 3799` annotation-level samples | ordering runner 可判别 `2331 / 2333` multi-event cases；omission runner `N = 2333` |
| 缺口    | 主口径完整                                                                                      | 相对 HumanML3D-E test 少 `578` 个 sample，其中 `386` 个是 multi-event                   |

正式结论：

1. `HumanML3D-E` 是 MoDebug 的唯一主数据源，因为它同时对齐 `Event-T2M` generation、full caption、ordered event decomposition。
2. `ChronAccRet event_texts` 只作为 ChronAccRet 代码读取的格式适配层，不替代 HumanML3D-E 的主数据口径。
3. ChronAccRet omission protocol 当前接受在 `4068` 子集上作为 independent retrieval-side cross-check；不把它误写成覆盖完整 HumanML3D-E test split。

## 2. Full-Level Alignment 做了什么

full text ↔ full motion alignment（如 HumanML3D R-Precision、标准 text-motion retrieval、FID 辅助报告）本质上是：

> 给定一段完整 caption 和一段完整 motion，判断它们是否整体语义匹配。

这个范式的隐含假设是 text 与 motion 都是不可分割整体。通常 text encoder 和 motion encoder 各自输出一个 global vector，再做 cosine、Euclidean distance 或 contrastive matching。

它天然适合回答：

1. motion 是否像 HumanML3D 分布中的合理动作。
2. full caption 与 full motion 是否大体语义相符。
3. backbone generation 是否发生数量级崩坏。

它不适合回答：

1. 第 `k` 个 event 是否被执行。
2. event 顺序是否与 caption 一致。
3. 某个 event 的持续时间是否异常。
4. 多个事件是否 collapse 到同一时间段。

因此 Event-T2M self eval 的 `R@3 = 0.8366379141807556` 只能证明 backbone-side generation sanity，不能证明 event-level correctness。

## 3. Event-Level Alignment 的新增约束

### 3.1 约束 A：时序信息必须保留

event-level alignment 要区分"先走后跳"与"先跳后走"。如果 motion representation 只剩 global pooled vector，就很难对 ordering 或 duration 做可靠判断。

对 MoDebug 的含义：

1. `TMR` global score 只能做 omission / semantic side signal，不能单独做 ordering judge。
2. `ChronAccRet` 更适合 formal ordering evidence，因为它的 protocol 直接测试 ordered event text corruption。
3. generation 侧必须观察 Event-T2M 内部是否有 event-to-time 的隐式结构，否则 reward guidance 缺少可解释落点。

### 3.2 约束 B：motion 侧不能手动硬切

HumanML3D-E 只提供 event text decomposition，没有 event 的帧级起止标注。手动把 motion 切成 `K` 段再逐段匹配会遇到三个问题：

1. 边界未知。
2. 事件之间存在 transition、overlap、co-execution。
3. 硬切错误会直接污染 alignment score。

对 MoDebug 的含义：正式路线应坚持 **text-side corruption + full motion scoring**，不要把 MVP 改成 motion segmentation benchmark。

### 3.3 约束 C：text 侧划分是主要可控入口

当前最可靠的 event 单元来自 HumanML3D-E ordered event texts。MoDebug 可以通过 text 侧构造 counterfactual：

1. `drop`：删除一个 event，测试 scorer 是否认为 full text 更匹配同一 motion。
2. `replace`：替换一个 event，测试 scorer 是否能识别 presence mismatch。
3. `shuffle`：打乱 event 顺序，测试 scorer 是否对 ordering 敏感。

这正是 native TMR omission protocol 与 ChronAccRet ordering / omission protocol 的共同基础：不直接监督 event-motion 帧级对齐，而是测 evaluator 对 event-level corruption 的敏感性。

### 3.4 约束 D：Event-Level 高分必须蕴含 Full-Level Sanity

形式化地说：

```text
high event-level score -> acceptable full-level generation sanity
high full-level score  -/-> high event-level correctness
```

第一条必须成立。如果一个方法在 event-level judge 上高分，却显著破坏 Event-T2M self eval 的 FID / R-Precision，那么它更像 reward hacking，而不是更好的 motion generation。

第二条不一定成立。full-level 高分可能掩盖 omission / ordering violation，这正是 MoDebug 的问题来源。

## 4. 当前证据是否支持 MoDebug

| 维度 | 当前证据 | 判断 |
| --- | --- | --- |
| backbone sanity | Event-T2M on HumanML3D-E overall `FID = 0.049708280712366104`, `R@3 = 0.8366379141807556`; official HumanML3D reference `FID = 0.049953218549489975`, `R@3 = 0.8469827771186829` | generation backbone 可用 |
| omission side signal 1 | native TMR on HumanML3D-E multi-event `N = 3799`: `full > drop = 0.7043958936562253`, `full > replace = 0.836272703342985` | 可用但不能当 standalone final judge |
| omission side signal 2 | ChronAccRet omission on subset `N = 2333`: `full > drop = 0.7299614230604372`, `full > replace = 0.8551221603086155` | 可作为 TMR 的 independent retrieval-side cross-check |
| safe-drop consistency | comparable rows `1608`; agreement `1179 / 1608 = 73.32%`; `5plus = 51 / 80 = 63.75%`; coverage vs TMR `42.33%`, vs ChronAccRet `68.92%` | 支持 drop-side consistency；不是 standalone final judge |
| aligned-replace consistency | comparable rows `1608`; TMR `full > replace = 0.835820895522388`; ChronAccRet `full > replace = 0.8538557213930348`; agreement `1313 / 1608 = 81.65%`; `5plus = 63 / 80 = 78.75%` | replacement mismatch 缺口已补齐；仍只是 evaluator-side cross-check |
| ordering evidence | ChronAccRet full4068 `CAR = 0.6473616473616474`, evaluable `2331 / 2333`; subset256 `CAR = 0.673202614379085` | formal ordering evidence 已闭合 |
| high event-count risk | TMR `5plus` bucket: `drop = 0.6610878661087866`, `replace = 0.7573221757322176` | 高事件数 omission signal 更弱 |
| duration | 无正式 evaluator | 当前 sprint 外 |

结论：MoDebug 不是伪需求。full-level metric 确实不足以覆盖 omission / ordering；当前 counterfactual retrieval-side evaluator stack 足够支撑下一步 generation 观测与谨慎的 reward design，但不支持直接宣称已经有完整 event-level judge。

## 5. 对 Eval 设计的引导

当前 eval 侧应固定为三层：

1. **Backbone sanity**：Event-T2M self eval，只解释 FID / R-Precision / matching 级别的 full-level quality。
2. **Frozen retrieval-side event evidence**：native TMR omission、ChronAccRet ordering、ChronAccRet omission cross-check。
3. **Held-out final eval**：后续如果某个 scorer 被用作 reward，就不能用同一个 scorer 的同一个 protocol 作为最终主表。

近期 eval 侧状态：

1. **Consistency check**：已完成 safe-drop comparable rows 与 aligned-replace comparable rows；二者都只能写作 evaluator-side cross-check，不能写成 standalone final judge。
2. **Held-out split 设计**：已冻结在 [[2026-04-29_modebug-heldout-eval-policy|Held-Out Eval Policy]]；如果 `R_pres` reward 使用 TMR，最终 omission evidence 优先报告 ChronAccRet omission 或 human eval；如果 reward 使用 ChronAccRet，最终 omission evidence 优先报告 TMR 或 human eval。
3. **Full-level safety**：保留为 G4 后置检查；Event-T2M self eval 只作 full-level safety，不作 event-level final judge。

不做：

1. 不扩 ordering，ChronAccRet full4068 已闭合。
2. 不自建 evaluator，除非 TMR 与 ChronAccRet omission 都被证明不可用。
3. 不把 AToM native MotionGPT eval 写成当前 event-level judge。

## 6. 对 Generation 设计的引导

generation 侧可以与 eval 侧部分并行，但并行内容必须限制在不依赖最终 reward 的观测实验：

1. **attention map 对比**：观察 successful / failed samples 中 event text condition 是否对应不同 temporal regions。
2. **denoising trajectory**：观察 event evidence 在 diffusion steps 中何时 emerge，决定 guidance 插入时机。
3. **gradient sensitivity**：计算 event condition 对 motion frames 的梯度分布，确认 event condition 是否真的控制局部时间段。

这些实验只输出 evidence log，不作为正式 evaluator metric。只有当 attention / gradient signal 对 `drop / replace / shuffle` 表现出 counterfactual sensitivity，才允许进入 reward feature 或 guidance。

当前已完成支撑 artifact：

1. observation pool：`linkedCodebases/EventT2M-codes-main/logs/modebug_observation_pool/manifest.jsonl` 与 `summary.json`
2. generation observation schema：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/schema.yaml`
3. schema README：`linkedCodebases/EventT2M-codes-main/logs/modebug_generation_observation/README.md`
4. attention feasibility：[[2026-04-29_modebug-attention-extraction-feasibility]]

限制：G1/G2 已用 opt-in `need_weights=True` 完成 `256` condition rows / `10240` attention records，但 raw attention normalized entropy 高、condition-order peak match 低，因此当前仍是 observation，不是直接可跑 reward。G3 仍需要绕开默认 `@torch.no_grad()` sampling path 做 frozen-forward diagnostic。

## 7. Roadmap Implication

MoDebug 后续路线应从"先把 evaluator 全部做完再动 generation"调整为双线推进：

1. **Evaluator lane**：E1 join diagnostics + safe-drop consistency done；E2 held-out eval policy done；E3 aligned-replace consistency done；E4 full-level safety post-G4。
2. **Generation lane**：G0 observation pool done；G1/G2 attention logging done but raw signal weak；G3 diagnostic next；G4 blocked by G1/G2 filtering + G3。

两条线共享同一 corruption family：`drop / replace / shuffle`。这样 eval 结论能直接约束 reward 设计，而 generation observation 又能解释 evaluator 为什么敏感或不敏感。

## 8. Non-Goals

1. 不引入 MotionPatches 到任何正式 eval / scorer / judge 链路。
2. 不做 motion 显式切分。
3. 不把 `TMR Phase 1` / `PAPO-lite` debug 写成正式 evaluator。
4. 不在当前 sprint 中补 duration evaluator。
5. 不把 reward scorer 与最终主表 evaluator 混成同一个 protocol。
