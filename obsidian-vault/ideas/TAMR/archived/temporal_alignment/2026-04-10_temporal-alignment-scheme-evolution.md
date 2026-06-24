---
created: 2026-04-10
updated: 2026-04-11T10:30
status: summary-consolidated
title: TAMR Temporal Alignment Scheme Evolution Log
model_name: TAMR
tags:
  - tamr
  - temporal-alignment
  - patch-event-alignment
  - scheme-evolution
source:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-06_tamr-v3-event-abstraction-centered-design.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v3.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v4-narrow-scope-execution.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/eval_summary/2026-04-10_tamr-motionpatches-stage4-first-pass-eval-summary.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md
merged_from:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-10_tamr-stage4-1-alignment-first-execution-plan.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v1-review-claude-sonnet.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v1.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v1-review-gpt52.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v1-review-gpt54.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v2.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_temporal-alignment-scheme-evolution-claude_revision.md
---
# TAMR Temporal Alignment Scheme Evolution Log

> Consolidation note:
> 从 `2026-04-11` 起，这份文档是 Stage4.1 历史收敛的唯一保留总结。
> `V1 / V2 / review / 临时执行稿` 的有效结论已并入本文与 `V4`，原草稿已从目录中清理。

## 0. 记录目的

这份表格用于记录 `patch-event / diag` 对齐机制从 V1 到 V4 的收敛过程，明确：

1. 每一版在解决什么问题；
2. 为什么要改；
3. 引入了什么新机制；
4. 哪些风险被 reviewer 指出；
5. 为什么 full mechanism 停在 `BASMA+`，而当前执行口径转向 `V4 narrow scope`。

## 1. 方案演化总表

| 阶段 | 当前状态 | 触发原因 | 核心机制 | 相对前版的主要增量 | 暴露的问题 / 风险 | 当前结论 |
| --- | --- | --- | --- | --- | --- | --- |
| Stage4.1 初始问题定义 | 已并入 `V4` 与本文 | Stage4 首轮 `No-Go`，现有 `independent softmax + summed target` 太弱 | `14x5 -> 14 time bins`，event soft alignment，adapter guidance | 明确只做 alignment-first，不碰 Step5 evidence head | patch 维过早平均，event 身份被压缩，adapter guidance 容易 confound | 需要新方案 |
| V1 | 已并入本文，原草稿已删除 | 先把“单点对齐”升级成“带状对齐” | `BMSA`：time-band + patch-support，event-aware pooling | 保留 diag 归纳偏置；恢复 patch-support；提出 train-only auxiliary branch | 强制覆盖整段时间轴；顺序偏置写得过硬；不存在/no-evidence 难表达；event contrastive 负例口径不清 | 方向对，但不能直接实现 |
| Review 1 | 已并入本文，原草稿已删除 | 独立模型审稿 | 严格质疑 V1 的结构假设 | 指出 `hard partition`、`prior shortcut`、`masked InfoNCE` 缺失、诊断不可证伪 | 如果不引入 background / abstain，热图可能只是“好看但假” | 推动 V2 改成 background-aware |
| Review 2 | 已并入本文，原草稿已删除 | 第二个独立模型交叉审核 | 审稿式找机制硬伤 | 强调强覆盖、强顺序、patch regularizer 冲突、对照实验不足 | 如果顺序和覆盖被结构锁死，diag 指标会失真 | 推动 V2 / V3 把 soft monotonic 和 sanity checks 写清 |
| V2 | 已并入本文与 `V3`，原中间稿已删除 | 回应双 reviewer | `BASMA`：background-aware + soft monotonic + content-first | 引入 background gate、abstain、soft order regularizer、null-event abstention、target entropy patch gating | patch-support 解释力虽保留，但文档重心转向 time support，执行版还缺“当前必做 vs future upgrade”切分 | 历史中间稿，已不单独保留 |
| V3 | 保留：full blueprint | 第三个 agent 统筹优化 | `BASMA+`：content-first time support + weak order bias + background-aware abstention + controlled multi-patch support + masked InfoNCE | 同时保留 V1 的 `time-band + patch-support`，吸收 V2 的 `background-aware + falsifiable diagnostics`，补齐 go/no-go 与实验顺序 | 仍未直接实现到代码；复杂度高，容易在无实验反馈时过度设计 | 降级为 full blueprint |
| Claude 项目级复查 | 已并入 `V4` 与本文，原复查稿已删除 | 对“整个项目目标 + 当前 Stage4.1 聚焦”做总审稿 | 不是新机制，而是对阶段目标的纠偏 | 明确指出问题是“设计循环快于实验循环”；建议 `Go with Narrow Scope` | 若继续直接上 V3，全套 8-loss / 多超参机制会让归因恶化 | 触发 V4 收缩执行范围 |
| V4 | 保留：当前执行稿 | 反思项目级复查后重设阶段目标，并吸收后续执行评审 | 不直接实现 full `BASMA+`，改成 `D0-D1-D1.5-D2-D3` 的最小实验闭环：事件统计 gate -> frozen minimal head -> uniform pooling control -> unfrozen control -> BASMA-lite | 把 `V3` 从 immediate implementation 改为 blueprint；把当前真正问题收敛为“auxiliary branch 为什么伤主表征”，并补上 quantitative gate、masked InfoNCE 伪代码、D1.5 必要控制组、D2 解冻范围 | 把执行范围收窄并把最小实现口径锁死 | 当前执行建议稿 |
| D0 result | 保留：最新执行结果 | 按 `V4` 先做数据层 quantitative gate | HumanML3D-E 事件统计 | 给出 `K` 分布、单事件占比、规则 overlap 占比，并实际触发/不触发 gate | 只解决“是否值得继续 D1”，还未回答最小 head 是否可行 | 当前状态为 `GO -> D1` |

## 2. 关键转折点表

| 转折 | 为什么发生 | 设计变化 |
| --- | --- | --- |
| `single-bin softmax -> time-band` | event 常跨多个连续时间 bin，单点对齐过硬 | 从点状权重变成带状支持 |
| `time-only -> time + patch-support` | event 会跨 patch，不能把 patch 维永久平均掉 | 恢复 patch-part 支持分配 |
| `hard partition -> background-aware soft assignment` | V1 强制覆盖整段时间轴，无法表达 transition / no-evidence | 引入 background gate、abstain、per-event normalization |
| `hard monotonic -> soft monotonic` | 硬顺序会让 reorder 诊断失真 | 顺序变成 weak bias + regularizer |
| `plain batch contrastive -> masked InfoNCE` | 同样本 event 互为强负例会自相残杀 | 负例以跨样本 event 为主 |
| `sparsity-only patch regularizer -> target entropy band` | event 可能合理依赖 2-3 个 patch-part | patch 约束改为受控多激活 |
| `看热图 -> 可证伪诊断` | reviewer 认为“图好看”不等于“真对齐” | 增加 `prior_copy_ratio`、`order_sensitivity_delta`、S1-S5 sanity checks |
| `full mechanism -> narrow-scope execution` | Claude 指出当前最大风险是“设计循环快于实验循环” | 把 `BASMA+` 降级为 blueprint，当前先做 `D0-D3` 最小实验诊断 |

## 3. 当前收敛结论

当前最稳的 **full mechanism hypothesis** 仍然是 V3 的 `BASMA+`：

1. `content-first` 保证对齐先看 motion evidence；
2. `weak order bias` 保留 diag 归纳偏置但不伪造顺序能力；
3. `background / abstain` 让模型能表达 no-evidence；
4. `multi-patch support` 保留 patch-event 可解释性；
5. `masked InfoNCE + sanity checks` 让 alignment-first 真正可验证。

但当前最稳的 **执行口径** 已不再是“直接实现 V3”，而是 V4 的 `Go with Narrow Scope`：

1. 先做 `D0` 数据统计；
2. 再做 `D1` frozen minimal event-time head；
3. 再做 `D2` unfrozen 对照；
4. 只有最小 head 给出正信号，才进入 `D3 = BASMA-lite`；
5. patch-support / background / abstain / adapter guidance 暂时后置。
6. 当前最小路径固定为 `D0 -> D1 -> D1.5 -> D2 -> D3`，不再回到 full mechanism 先行。
7. `2026-04-11` 的 `D0` 已完成并判定 `GO`，因此当前实际 next step 已更新为 `D1`。

## 4. 已并入并清理的旧稿要点

为了让 `Temporal_Alignment/` 目录只保留真正会继续维护的文档，以下结论已被吸收，不再单独保留原文件：

1. 初始 `alignment-first execution plan`
   - 保留了“Step4 首轮 `No-Go` 后不能前置 Step5”的边界；
   - 保留了“先对齐问题定位，再讨论更重机制”的执行顺序；
   - 具体执行口径已并入 `V4`。
2. `V1` 与三份 review
   - 保留了 `time-band + patch-support` 的原始价值；
   - 保留了 reviewer 对 `强覆盖`、`强顺序`、`负例污染`、`对照不足` 的关键质疑；
   - 这些问题现在统一体现在本文的演化表与 `V3/V4` 的定位里。
3. `V2`
   - 保留了 `background-aware`、`abstain`、`soft monotonic`、`target entropy patch gating` 等修正方向；
   - 这些修正已由 `V3` 作为 full blueprint 接手，不再需要保留单独中间稿。
4. `claude_revision`
   - 保留了“设计循环快于实验循环”这一核心纠偏；
   - 该判断已直接沉淀为 `V4` 的 `Go with Narrow Scope`。

## 5. 建议的执行与维护口径

若后续要进代码实现，建议采用双层口径：

1. `V4` 作为当前 immediate execution plan；
2. `V3` 作为 full mechanism blueprint；
3. 本文作为历史设计与 revision 轨迹的唯一保留总结。

更具体地说：

1. `V3`：当前完整机制蓝图；
2. `V4`：当前真正应执行的窄范围实验计划；
3. `2026-04-11 D0 result`：当前最近的实际执行结果；
4. 本文：替代已清理中间稿的历史判断链。
