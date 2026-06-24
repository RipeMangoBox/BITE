---
created: 2026-04-10
updated: 2026-04-11T10:30
status: proposal-v4-narrow-scope
title: TAMR Stage4.1 Patch-Event Diag Alignment Design V4 Narrow-Scope Execution Revision
model_name: TAMR
tags:
  - tamr
  - stage4.1
  - temporal-alignment
  - patch-event-alignment
  - narrow-scope
  - execution-revision
source:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_tamr-stage4-1-patch-event-diag-alignment-v3.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_temporal-alignment-scheme-evolution.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/eval_summary/2026-04-10_tamr-motionpatches-stage4-first-pass-eval-summary.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md
consolidates:
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/2026-04-10_tamr-stage4-1-alignment-first-execution-plan.md
  - /home/ripemangobox/Coding/Github/Motion/TMR/ResearchWY/paperIDEAs/TAMR/Temporal_Alignment/2026-04-10_temporal-alignment-scheme-evolution-claude_revision.md
---
# TAMR Stage4.1 Patch-Event Diag Alignment Design V4 Narrow-Scope Execution Revision

> Consolidation note:
> 本文吸收并取代 `2026-04-10_tamr-stage4-1-alignment-first-execution-plan.md` 与 `2026-04-10_temporal-alignment-scheme-evolution-claude_revision.md` 中仍有价值的当前执行结论。
> 从 `2026-04-11` 起，它应被视为 Stage4.1 的唯一执行稿。

## 0. 为什么需要 V4

Claude 的项目级复查指出了一个关键问题：

> 当前最大的风险不是 `BASMA+` 设计错误，而是我们在没有新增实验反馈的情况下，把一个 full alignment subsystem 当成了 immediate next step。

这个判断是成立的。

因此，V4 不再把 `V3 / BASMA+` 当作“马上整套实现”的执行稿，而是重新分层：

1. `V3` 保留为 **full mechanism hypothesis**；
2. `V4` 作为 **当前真正执行的 narrow-scope plan**；
3. 当前目标从“直接证明 BASMA+ 全套有效”改成“先回答 auxiliary temporal branch 为什么伤害主表征”。

## 1. V4 的核心结论

当前 verdict 不应是 `Strong Go` 去直接实现 `BASMA+`，而应是：

> `Go with Narrow Scope`

具体含义：

1. `temporal alignment` 这条线仍值得继续；
2. 但当前必须先做 **最小实验闭环**，而不是继续增加 loss、gate、sanity 体系；
3. 只有当最小版本给出正信号，`BASMA+` 才值得成为下一层复杂化方向。

## 2. 对 V3 的重新定位

V3 仍然有价值，但其价值更准确地说是：

1. 它定义了一个较完整的 target mechanism family；
2. 它把 reviewer 指出的结构性漏洞补得比较干净；
3. 它给出了足够好的 full design vocabulary。

但 V3 暂时 **不是** 当前应该一步落地的实现目标。

因为在当前阶段，它有三个现实问题：

1. loss 太多，归因会变差；
2. 超参数太多，HumanML3D 规模下很难高效调通；
3. 如果失败，很难判断是“alignment direction 不成立”还是“full mechanism 太复杂”。

所以现在最合理的关系是：

1. `V3 = full blueprint`
2. `V4 = executable minimal subset`

## 3. 当前真正该回答的问题

在 Stage4 首轮 `No-Go` 之后，当前最关键的问题不是：

1. 我们能否设计一个更漂亮的 patch-event diag alignment；

而是：

1. 为什么 training-time temporal auxiliary branch 会伤害 global retrieval 主表征？
2. 这种伤害来自 adapter 本身、梯度路径、loss 权重，还是 token-level temporal supervision 的方向不对？
3. 在最小 temporal head 下，这种伤害是否依然存在？

如果这三个问题没有先回答，直接上 `BASMA+` 全量版并不会让结论更清楚，只会让问题更难诊断。

## 4. V4 的新执行原则

V4 收缩为四条原则：

1. **先诊断伤害来源，再设计复杂机制**
2. **先做 time-only minimal head，再决定是否需要 patch-support**
3. **loss 数量控制到 3 个以内**
4. **每一步都要能在 1-2 天内给出 go/no-go 信号**

## 5. 立即执行的最小闭环

## 5.1 D0: HumanML3D-E 事件统计

先做数据层核查，明确 alignment 设计空间。

至少统计：

1. `K` 的分布
2. 单事件样本占比
3. 多事件样本占比
4. 是否存在明显并行 / overlap 事件口径
5. 每条 caption 的平均 event 长度

作用：

1. 判断当前是否真的需要复杂 multi-event alignment
2. 判断 `background / overlap / abstain` 在数据层是不是高频需求

这里不能只做“看一眼统计”，而必须给出 quantitative gate。

### D0 quantitative gates

1. 若 `K>=2` 的样本占比 `< 40%`，则 **不进入 D1 的 alignment 主线**，而是把 Stage4.1 降级为 `Stage0-2 + minimal evidence head` 路线。
2. 若 `K=1` 的样本占比 `> 60%`，则必须在结论里明确写：event-time alignment 的潜在收益上限只存在于多事件子集，不能把它当成全数据主矛盾。
3. 若人工或规则判定的并行 / overlap event 占比 `> 15%`，则 D3 的 `soft monotonic` 假设只能视为局部成立；后续实验应优先在 `K>=2 且非 overlap` 子集验证。

也就是说，D0 的输出不只是统计表，而是一个明确的继续/收缩信号。

### D0 当前状态（2026-04-11）

1. 结果文档：`2026-04-11_tamr-stage4-1-d0-humanml3de-event-statistics-result.md`
2. 三个 quantitative gate 均未触发：
   - `K>=2 = 70.58%`
   - `K=1 = 29.42%`
   - overlap = `4.48%`
3. 当前结论：`GO -> D1`

## 5.2 D1: 冻结 backbone 的最小 event-time head

当前第一优先级实验不是 `BASMA+`，而是：

1. 从 `stage2_gt` warm-start
2. 冻结 motion backbone 主干
3. 冻结 text encoder，避免先把问题扩散到 text branch
4. 只训练一个最小 `event-time attention head`
5. 只做 `time-only`，不做 patch-support
6. 不加 background gate
7. 不加 adapter guidance
8. 不加 null-event abstention

最小机制可以非常简单：

1. `S_content(k,t) = <W_e E_k, W_t H_bar[t]>`
2. `A_time(k,t) = softmax_t(S_content(k,t))`
3. `Z_k = sum_t A_time(k,t) * H_bar[t]`
4. `L_evt_align = masked InfoNCE`

当前只保留不超过 3 个 loss：

1. `L_global`
2. `L_evt_align`
3. 可选 `L_cont`（若不用则更简单）

这个实验的目的不是追求最优，而是回答：

> 在不改动 backbone 表征的前提下，`stage2_gt` 的冻结特征里是否已经存在可提取的 event-time signal？

也就是说，D1 的目标不是“证明不伤主表征”。
在 frozen 设定下，主路径本来就基本不应被伤害；D1 真正回答的是：

1. 最小 event-time head 能否从冻结的 Stage2 表征中提取弱正信号；
2. 如果连 frozen features 都提不出信号，那么后面的复杂 alignment 设计就没有必要继续。

### D1 中 `masked InfoNCE` 先写死，不允许编码时再开设计讨论

最小实现伪代码固定如下：

```python
valid = event_mask.bool()                      # [B, K]
z = F.normalize(Z[valid], dim=-1)             # [N, D]
e = F.normalize(E[valid], dim=-1)             # [N, D]
sid = sample_id[valid]                        # [N]
logits = z @ e.T / tau
allow = (sid[:, None] != sid[None, :]) | torch.eye(len(z), dtype=torch.bool, device=z.device)
logits = logits.masked_fill(~allow, -1e4)
loss = F.cross_entropy(logits, torch.arange(len(z), device=z.device))
```

固定口径：

1. 正例是 `(i, i)`；
2. 负例只来自跨样本 event；
3. 同样本其他 event 不作为负例；
4. `tau` 在 D1 固定，不在这一步调温度超参。

### D1 评测口径

1. 主检索：`TMR-normal / TMR-nsim`
2. temporal retrieval：`EVT-normal / EVT-nsim`
3. `DIAG_*` 暂时只作为 **provisional secondary signal**，因为它们来自规则构造的 temporal negatives，不作为 D1 的决定性 gate

## 5.3 D1.5: 均匀池化对照（必要控制组）

在进入 D2 前，必须做一个更简单的控制组，回答：

> 收益或伤害到底来自“学了 event-time attention”，还是只是“多了一个 event-level contrastive loss”？

设定：

1. 仍从 `stage2_gt` warm-start
2. 仍冻结 motion backbone 与 text encoder
3. 不学习 attention
4. 对每个 event 直接使用相同的均匀池化 motion 表征：

`Z_k^{uniform} = mean_t H_bar[t]`

5. 仍然使用完全相同的 `masked InfoNCE`

解释：

1. 若 `uniform + InfoNCE` 就已经有正信号，则 attention head 不是当前必需组件；
2. 若只有 attention 版有信号，才说明 `event-time selection` 本身值得继续。

## 5.4 D2: 解冻 backbone 对照

如果 D1 或 D1.5 给出正向信号，才做第二步：

1. 保持同一个最小 head
2. 只改变解冻范围
3. 观察 retrieval 是否退化

这一步直接回答：

1. 问题是否来自 auxiliary loss 通过共享编码器传导的梯度污染；
2. 如果冻结不伤、解冻就伤，那么当前核心矛盾不是“alignment design 不够复杂”，而是“共享表征被 auxiliary branch 错误整形”。

### D2 必须拆成两组

1. `D2a`: 只解冻 motion encoder 最后 2 个 block + 新 head
2. `D2b`: 解冻整个 motion encoder

保持 text encoder 继续冻结。

这样才能区分：

1. 问题是否只发生在深层共享表征；
2. 还是任何程度的 unfreeze 都会把 auxiliary 信号传坏。

## 5.5 D3: 再决定是否进入 `BASMA-lite`

只有在 D1、D1.5、D2 给出正向信号后，才进入下一层：

`BASMA-lite`

它只允许保留 V3 中最关键但最少的子集：

1. `content-first time support`
2. `masked InfoNCE`
3. `soft order regularizer`

此时仍然不做：

1. patch-support
2. background gate
3. null-event abstention
4. adapter guidance
5. DTW / coarse-to-fine

也就是说，真正的实验顺序应该变成：

1. `D0` 数据统计
2. `D1` frozen minimal head
3. `D1.5` uniform pooling control
4. `D2` unfrozen control
5. `D3` BASMA-lite
6. 只有 D3 正向后，才考虑 `D4 = BASMA+ subset`

## 6. 当前明确延后的内容

以下内容暂时不该进入 immediate execution：

1. full `BASMA+` 八损失联合训练
2. patch-support 分支
3. background gate / abstain 通道
4. `L_null_abstain`
5. adapter guidance
6. multi-span / overlap explicit modeling
7. DTW / coarse-to-fine / token compressor
8. B0-B7 全序列实验

这些内容不是错，而是 **时机不对**。

## 7. V4 对论文叙事的修正

Claude 还指出了一个更大的问题：

> 项目可能正在从 `retrieval-centered temporal understanding` 漂移到 `patch-event temporal grounding mechanism design`

这个提醒也成立。

因此 V4 明确重申：

1. TAMR 的主任务仍是 `temporal discriminative retrieval`
2. alignment branch 只是 retrieval 的训练期辅助机制候选
3. 若辅助机制不能稳定反哺 retrieval，就不应该继续膨胀成独立子系统
4. `grounding-like support map` 的价值在于 supporting evidence，不是当前主任务翻转

## 8. V4 的 go / no-go 定义

### 当前应该看的不是 full mechanism 指标，而是最小问题是否被回答

### Go

1. D0 quantitative gate 满足，说明多事件 alignment 确实值得进入下一步
2. `D1` 能从 frozen Stage2 特征中提取至少弱正 signal
3. `D1.5` 与 `D1` 的对比能说明 attention 是否真的提供额外价值
4. `D2` 能明确区分“冻结不伤 / 解冻才伤”或“冻结也伤”
5. 这使得下一步设计有明确归因方向

### No-Go

1. D0 quantitative gate 不满足，说明多事件 alignment 不是当前主需求
2. 最小 `time-only` head 在 frozen 设定下都提不出任何弱正信号
3. `D1` 与 `D1.5` 几乎无差别，说明 event-time attention 本身没有带来额外价值
4. `D2a / D2b` 一解冻就系统性伤主检索，且无法通过最小损失设定缓解

如果出现这些情况，就应该停止扩展对齐机制，回到 `Stage0-2 + minimal evidence head` 路线。

## 9. 当前建议的执行顺序

1. 先做 `D0`: HumanML3D-E 统计
2. 再做 `D1`: frozen minimal event-time head
3. 再做 `D1.5`: uniform pooling + masked InfoNCE
4. 再做 `D2`: unfrozen 对照（last-2-blocks vs full）
5. 若有信号，进入 `D3`: BASMA-lite
6. 若 D3 成立，才考虑恢复 V3 中的 patch / background / abstain 组件

## 10. 最终反思结论

这次新一轮评审最有价值的地方，不是它否定了 `BASMA+`，而是它进一步把 `V4` 收束成一个真正可执行的实验序列：

1. `BASMA+` 仍可作为 full mechanism hypothesis 保留；
2. 但当前真正该做的是 **最小实验诊断**，不是 full subsystem 实现；
3. 当前最值得优先回答的问题是“auxiliary temporal branch 为什么伤害主表征”；
4. 在这个问题没回答之前，继续扩机制会让项目更像在设计一个独立 grounding 子系统，而不是推进 retrieval-centered 主线。

一句话总结：

> 从现在开始，Stage4.1 的主线不再是“直接实现 BASMA+”，而是“用最小 event-time head 先验证 temporal auxiliary branch 是否值得存在”；V3 降级为 blueprint，V4 才是当前执行稿；而 V4 的最小路径应固定为 `D0 -> D1 -> D1.5 -> D2 -> D3`。
