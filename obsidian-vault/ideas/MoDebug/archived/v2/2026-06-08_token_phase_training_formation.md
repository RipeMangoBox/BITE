---
title: "MoDebug Spatial-Temporal Training Formation"
created: 2026-06-08T01:53:44+08:00
updated: 2026-06-08T20:28:00+08:00
status: draft
hypothesis: "模型权重与 layer/stage 功能分工是在训练中由 text token、spatial joint group、temporal window 上的 loss、梯度竞争和梯度协作塑造的；因此可通过最小 spatial-temporal training intervention 来改善 text-motion alignment 与 motion generation quality。"
source_papers:
  - "[[analysis/ICCV_2023/TMR_Text-to-Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis]]"
  - "[[analysis/ICML_2024/HumanTOMATO_Text-Aligned_Whole-Body_Motion_Generation]]"
  - "[[analysis/CVPR_2026/MoLingo_Motion-Language_Alignment_for_Text-to-Human_Motion_Generation]]"
  - "[[analysis/ICLR_2026/AMPED_Adaptive_Multi-objective_Projection_for_balancing_Exploration_and_skill_Diversification]]"
  - "[[analysis/ICCV_2023/PoseFix_Correcting_3D_Human_Poses_with_Natural_Language]]"
  - "[[analysis/ICLR_2024/FLD_Fourier_Latent_Dynamics_for_Structured_Motion_Representation_and_Learning]]"
tags:
  - MoDebug
  - spatial_temporal_training
  - gradient_dynamics
  - functional_specialization
  - motion_generation
---

# MoDebug Spatial-Temporal Training Formation

> [!abstract] 第三视角
> 本 note 新增第三个视角：layer/stage 分工并不是训练后才出现的静态性质，而是在 training 中由 text token、spatial joint group、temporal window 的 loss 和梯度回传逐步塑造出来的。因此，优化 text-motion alignment 和 motion quality 不只可以从“事后干预”或“结构分工”入手，也可以直接从最小 spatial-temporal training dynamics 入手。

## 1. 与前两个视角的关系

MoDebug 当前可分成三个层级：

| 视角                             | 类型      | 主要问题                                               | 产出                                                 |
| ------------------------------ | ------- | -------------------------------------------------- | -------------------------------------------------- |
| Cross-baseline intervention    | 事后诊断    | 已训练模型哪些 layer/stage/module 对 alignment/quality 敏感？ | 敏感层、耦合区、架构对照                                       |
| Baseline-agnostic FSD          | 结构与归纳偏置 | 能否显式诱导 block/stage 功能分工来提升 alignment/quality？      | experts、router、functional losses                   |
| Spatial-temporal training formation | 训练形成机制  | loss 和 gradient 如何在 text/body/time 层面塑造权重与分工？       | spatial-temporal weighted loss、gradient attribution、后续 routing |

DS max 的判断是：第三视角不是简单重复前两个视角，也不应宣称完全替代它们。更准确的关系是：

- 它解释第一视角：某些层被 intervention 后更敏感，可能源于训练中这些层长期接收特定 text/body/time signal 的梯度压力。
- 它支撑第二视角：FSD 的 experts/router 本质上是在结构层面固定或显式化不同空间/时间学习信号的梯度流向。
- 它也可独立成方法：即使不加 experts/router，只改变 spatial-temporal loss weighting 和 gradient scaling，也可能诱导隐式功能分化。

因此，第三视角是更底层的 **training dynamics view**：前两个视角更多看“结果”和“结构”，第三视角看“分工如何被训练出来”。

## 2. 核心研究问题

> [!question] Core Question
> 在 text-to-motion generation 中，如何根据 text token、spatial joint group 和 temporal window 的梯度动态，主动控制模型权重形成过程，从而提升文本对齐、动作质量和干预鲁棒性？

这个问题可以拆成四个子问题：

1. Token/body/time competition：文本 token、身体部位 joint group、时间窗口的 loss 是否在训练中互相竞争，导致某些对齐或质量属性被牺牲？
2. Spatial-temporal imbalance：文本明确指向的身体部位和运动变化更集中的时间窗，是否在 uniform loss 下被平均掉？
3. Gradient-to-layer mapping：不同 text/body/time group 的梯度是否主要塑造不同 layer/stage？
4. Trainable intervention：能否通过 minimal spatial-temporal weighted loss 和后续 gradient balancing 让这种分工更稳定、更可控？

## 3. 可操作机制

### 3.1 Minimal spatial-temporal weighting

修订后的第一版不再从 `speed / acc / jerk / contact / transition / high_dynamic` 等细物理属性开始。这些规则太早绑定了对“什么是重要 phase”的强先验，容易把 MVP 变成一组难以审计的手工权重。路线三先退回最小问题：

> [!question] Minimal weighting question
> 在不引入复杂 physics attributes 的前提下，只根据 **text 指向哪些 joints/body chains** 和 **motion 哪些时间窗发生显著变化**，能否让训练信号更关注对齐与质量最可能出错的 spatial-temporal token？

统一 loss 仍可写成：

```text
L_motion = sum_{t,j} w_temporal(t) * w_spatial(j) * ||x_hat[t,j] - x[t,j]||^2
```

其中第一版只保留两个低自由度权重：

- `w_spatial(j)`：文本解析出的 body parts / limb chains 对应的 joint group 权重。
- `w_temporal(t)`：运动序列中需要更关注的 frame/window/segment 权重。

#### Spatial weighting

Spatial weighting 由文本先验驱动，但必须可审计。第一版流程：

1. 预定义 HumanML3D skeleton 的 joint ontology，例如 `root / torso / head / left_arm / right_arm / left_leg / right_leg / hands / feet`。
2. 第一版训练主线优先使用固定 keyword-to-joint-group mapping；LLM 只能离线输出 body-part phrase 候选，经过缓存、人工抽检和固定 ontology 映射后才能进入训练。
3. 若 text 未显式提到某个身体部位，不给该部位置零，只保持默认权重 `1.0`，避免自然协同关节欠约束。
4. 只对被显式提到或强相关的 joint group 小幅加权，例如 `1.2-1.5`；所有权重做均值归一化，保持 loss scale 不变。

```text
w_spatial[j] =
  1.0 + beta * text_joint_mask[j]
w_spatial = w_spatial / mean_j(w_spatial[j])
```

`text_joint_mask` 不是 label truth，只是低强度先验。它必须单独消融：keyword mapping、LLM joint extraction、fixed generic groups 三者分开对比。若 LLM 在 50 条典型 text 上 joint-group recall 低于 `70%`，LLM 输出不得进入主训练结论，只能作为 error analysis。

#### Temporal weighting

Temporal weighting 先从 motion-level 的窗口变化出发，而不是直接命名为 contact/high-dynamic/transition。第一版采用最稳的两类候选：

- **MVP temporal baseline**：按 window 内 joint displacement / velocity magnitude 找出运动量更高或变化更集中的片段，静止片段轻微降权，运动片段轻微加权。
- **候选 temporal signal**：滑窗 FFT / FLD-like frequency representation 只作为后续诊断或消融，用来观察相邻窗口频域表示是否发生突变；它不进入第一版主 pipeline。

```text
motion_energy[t] = mean_j ||x[t,j] - x[t-1,j]||
window_energy[k] = mean_{t in window k} motion_energy[t]
w_temporal[t] = 1.0 + alpha * normalize(window_energy[window(t)])
w_temporal = clip(w_temporal, w_min, w_max)
w_temporal = w_temporal / mean_t(w_temporal[t])
```

初始建议只用很小的权重范围，例如 `w_min=0.8`、`w_max=1.3`、`alpha in [0,0.3]`。这里的 `alpha` 只控制 temporal weight 偏离 uniform 的强度。默认窗口可从 `0.2s` 左右开始，stride 取半窗；具体帧数按 dataset loader 的 FPS 固化进脚本配置。这不是为了最大化单项属性，而是检查“空间/时间非均匀训练信号”是否有正向迹象。

#### PoseFix and FFT boundary

PoseFix 不作为第一版 temporal weighting 的主机制。它的价值在于说明自然语言可以表达 pose-level correction，也可作为后续构造 frame/segment 级文本差异描述的参考；但直接用 PoseFix 判断“哪些帧该加权”会引入静态姿态域到 motion sequence 的 domain gap。若使用，只能作为后验诊断或数据标注工具，而不是 MVP loss 权重来源。

FFT / FLD-like 表示适合捕捉周期性或准周期性运动的频率变化，但“频域突变”等于“语义变化”不是普遍成立的。它可以作为 temporal segmentation 的候选 probe，尤其用于 locomotion / dance / rhythm-dominated samples；在首版 MVP 中不作为主权重。

DS max 多轮审查后的边界，session `14134226d804`：

- 修订后的 spatial + temporal 分解比旧的多物理属性规则更 solid，因为自由度更低、耦合更少、消融更清楚。
- `LLM joint extraction` 可行，但必须输出 soft joint groups，并与人工/固定 group 对照；若 50 条典型 text 上 joint-group recall 低于 `70%`，不得进入训练结论。
- `FFT` 可作为 rhythm-dominated motion 的后续 probe，不进入第一版主 pipeline。
- `PoseFix` 可作为文本-姿态差异建模的参考，不推荐直接用于 temporal weighting。
- 如果 `spatial + temporal` 固定权重不优于 uniform weights，应回退 uniform，不继续叠加更复杂规则。

### 3.2 Gradient balancing and routing

3.2 暂时不做 gradient routing。当前阶段先回答更基础的问题：不同 text token、motion frame token、joint group token 是否真的产生了可区分的梯度贡献？如果没有，routing 没有依据。

第一阶段只做 gradient attribution。为避免伪指标，先固定梯度来源：

- `L_gen`：原始 diffusion / reconstruction / token CE generation loss。
- `L_align`：可选的低权重、可反传 text-motion alignment proxy；如果当前 backbone 没有稳定可反传 proxy，则 `L_align` 只用于 eval，不记录 `g_align`。
- `g_gen = grad(L_gen)`，`g_align = grad(L_align)`。若没有 `L_align`，只记录 group-wise gradient norm 与 group-wise gradient direction，不写 alignment-motion gradient conflict 结论。

具体记录项：

- 记录 `w_spatial` 覆盖的 joint group 与非覆盖 group 的 gradient norm。
- 记录 `w_temporal` 高权重窗口与低权重窗口的 gradient norm。
- 记录与 body-part phrase 对齐的 text token embedding 或 cross-attention key/value 的 gradient norm。
- 按 layer/stage 聚合，观察这些 token/group 的梯度主要塑造哪些 stage。

为避免不同参数尺度不可比，必须做标准化：

```text
normalized_grad_norm(group, layer) =
  ||grad(group, layer)||_2 / (||parameter(layer)||_2 + eps)
```

可选诊断：

- `g_spatial · g_temporal`：空间加权和时间加权是否梯度冲突。
- `cos(g_align, g_gen)`：仅当 `L_align` 可反传且实现稳定时，才检查 alignment proxy 和 generation loss 是否冲突。
- per-layer sensitivity 与 gradient attribution 排名的相关性：看训练梯度是否解释 intervention 中的敏感 stage。

只有当观测到稳定差异后，才进入 gradient balancing / routing：

- routing 不是训练中自动触发，而是观测后的独立 ablation。
- 若连续 `500` 个 update step 的 moving-average group-wise grad norm CV 仍不超过 `15%`，说明 spatial/temporal group 没有形成可用差异，不做 routing。
- 若 `cos(g_align, g_gen) < -0.1` 的 batch 比例超过 `20%`，再考虑 PCGrad-style conflict handling。
- 若某些 joint/window 对少数 stage 有稳定高梯度贡献，再考虑把这些梯度路由到 FSD adapters。
- 第一版不得做复杂 backward mask；最多记录统计并离线分析。

### 3.3 Curriculum

暂不处理。只有当 3.1 的 temporal weighting 在特定 segment 类型上有稳定收益，且 3.2 的梯度统计显示这些 segment 的学习动态确实不同，才考虑 curriculum。

当前只保留一个后续更新原则：curriculum 不能比 3.1 的权重规则更复杂，否则会掩盖 MVP 的归因。

### 3.4 Attribute-specific supervision

暂不处理。属性级监督必须等 3.1 的 spatial-temporal weighting 和 3.2 的 gradient attribution 跑出明确失败类型后再加。否则会重新回到“多个 physics attribute 同时上”的过重设计。

可保留为后续候选的属性包括 semantic alignment、global trajectory、tempo/rhythm、contact/plausibility、smoothness/diversity，但它们第一版只作为 eval/probe，不进入主 loss。

### 3.5 Token-level CFG and attention control

暂不处理。只有在 3.1 证明 text-derived spatial groups 有用，且 3.2 证明 text token 与 motion token 的梯度贡献有稳定对应后，才考虑 token-level CFG 或 attention control。当前不把它写进 MVP。

## 4. 最小 MVP

### 4.1 原则

资源有限时，不应同时做所有机制。优先选择最少参数、最容易验证 training formation 假设的组合：

- 不改主干架构；
- 不先做复杂 gradient mask；
- 优先直接 post-train，而不是从头训练；
- 第一版只做 minimal spatial-temporal weighted loss + optional zero-init adapters；
- curriculum、FFT/PoseFix、细物理属性只作为后续诊断或第二阶段，不作为主 MVP；
- 成功后再加 learnable weighting、gradient routing 或 token-level CFG。

### 4.2 MVP 配置

| 项目       | 配置                                                                                         |
| -------- | ------------------------------------------------------------------------------------------ |
| Backbone | 一个已有 evaluator 和训练脚本的 T2M backbone；优先选当前最容易真训练的小规模设置                                       |
| 数据       | HumanML3D 子集 sanity，再扩到全量；优先复用已有 checkpoint 做短程 post-train |
| 方法       | Minimal spatial-temporal weighted generation loss + low-weight alignment proxy + preserve loss |
| Spatial 定义 | 固定 keyword mapping 把 text 中的 body-part phrase 映射到 soft joint group；LLM 只在审计通过后作为对照 |
| Temporal 定义 | 滑窗 motion energy / displacement 定义高低权重窗口；默认 `0.2s` 窗口、半窗 stride；FFT/FLD-like 只做后续 probe |
| Token 定义 | text body-part phrase、joint group、frame/window；MVP 先只用 joint group 与 temporal window |
| 参数       | 优先冻结 backbone；若与 0607 FSD 合并，则只训练 zero-init stage adapters |
| 训练       | 直接 post-train 2k-10k steps；只有 spatial parser、temporal window 或 evaluator 不可用时才补前提 eval |
| Eval     | FID/R-Precision/Matching + frozen TMR/CLIP similarity + text-mentioned joint error + high-weight window error + contact/smoothness probe |

### 4.3 对照组

| 对照                                | 目的                             |
| --------------------------------- | ------------------------------ |
| Baseline                          | 原始训练或原 checkpoint              |
| Same schedule, uniform weights | 排除只是 post-train schedule 有效    |
| Spatial-only weighting | 测试 text-derived joint group 是否足够 |
| Temporal-only weighting | 测试 motion-energy window 是否足够 |
| Spatial + temporal weighting | 主 MVP |
| Shuffled spatial groups / shuffled temporal windows | 排除只是 loss noise regularization |
| Old physics-attribute weights | 检查旧的细规则是否真的优于最小规则 |
| Keyword mapping vs LLM spatial groups vs fixed generic groups | 检查 text parsing 是否提供额外价值 |
| Minimal weights vs uniform weights with same adapters | 排除只是 adapters 带来收益 |
| Sensitive stage + uniform weights | 与 0607 合并时判断 stage selection 是否独立有效 |
| Sensitive stage + minimal weights | 与 0607 合并时判断最小加权是否进一步有效 |

### 4.4 成功标准

MVP 可以不追求 SOTA，但至少要出现：

- text-mentioned joint group error 下降；
- high-weight temporal window error 下降；
- contact/smoothness/root trajectory 至少一类 probe 不恶化，最好改善；
- R-Precision 或 Matching 不下降，最好小幅提升；
- FID/FID_TMR 不显著恶化；
- shuffled spatial groups / shuffled temporal windows 不复现主方法收益：若 permute 后局部 error 降幅相对真实 group/window 的降幅小于等于 `0.5%` 或统计不显著，则说明当前 group/window 设计无实际效果；
- gradient statistics 显示 text/body/time groups 的梯度范数或方向冲突具有稳定差异。
- 一针见血标准：text-mentioned joints 和 high-energy windows 的局部 error 下降，同时整体 FID/R-Precision 不坏；否则不能 claim spatial-temporal training formation 改善了生成。

## 5. 与 FSD 的关系

第三视角和 FSD 不是互斥关系。

| 关系    | 说明                                                                      |
| ----- | ----------------------------------------------------------------------- |
| 上游解释  | FSD 的 experts/router 能有效，可能是因为它们改变了 text/body/time 梯度的长期分配 |
| 轻量替代  | 当不想加参数时，可只用 spatial-temporal weighted training 诱导隐式分工 |
| 细粒度实现 | FSD 中的 router 可由 joint/window 统计监督，experts 可由 group-specific gradient 塑造 |
| 压力测试  | 如果 FSD 只在整体指标提升但局部 joint/window error 不降，说明分工可能是伪解释 |

更清晰的统一表述：

> [!note] Unified View
> Cross-baseline intervention 发现哪里敏感；FSD 设计什么结构来承载功能；spatial-temporal training formation 解释这些功能如何通过 text/body/time loss 和 gradient 被训练出来。

## 6. 可能的主方案

可以把第三视角发展成 **Spatial-Temporal Guided Training (STGT)**：

- Spatial-temporal weighted reconstruction / diffusion loss
- Text body-part phrase 到 joint group 的可审计 grounding
- Motion-energy temporal window weighting
- Gradient attribution across text/body/time groups
- 后续 gradient balancing across stable groups
- Optional token-level CFG or attention regularization

STGT 的关键 claim 不是“我们发现某层负责某功能”，而是：

> 通过直接控制 text/body/time 级训练信号，可以让模型在不显式增加专家结构的情况下形成更稳定的隐式功能分化，并改善文本指向身体部位和关键时间窗上的生成质量，同时保持整体 text-motion alignment。

与 0607 FSD 合并后的更强主线是 **diagnostic-guided post-train**：

```text
layerwise intervention -> identify sensitive stage
spatial-temporal rules -> identify which frames/joints/phrases deserve stronger learning signal
zero-init stage adapters -> absorb post-train updates without damaging backbone
alignment/quality probes -> verify gains and prevent reward hacking
```

这说明 0607 与 0608 不是两套互斥方案。0607 解决“更新哪些 stage/parameters”，0608 解决“用哪些 spatial-temporal losses 和 gradients 更新它们”。最终 MVP 应合并为：**在敏感 stage 放 zero-init adapters，用 minimal spatial-temporal weighting 和低权重 alignment proxy 进行短程 post-train。**

DS max 多轮讨论后的更严格表述：

- 0608 自身第一优先验证 `minimal spatial-temporal weights` 是否优于 `uniform weights`，先确认加权本身有用。
- 若与 0607 合并，再验证 `sensitive stage + uniform weights` 是否优于 `neutral stage + uniform weights`，确认诊断选层可转化为 post-train 收益。
- 合并后的第二步才验证 `sensitive stage + minimal spatial-temporal weights` 是否进一步优于 `sensitive stage + uniform weights`。
- 若 0608 自身加权失败，说明 minimal spatial-temporal weighting 暂不成立，应回退 uniform；若 0607 选层失败，说明诊断到 post-train 转化不成立；若合并加权失败但选层成功，说明 stage-wise post-train 可保留、0608 加权需重设。

## 7. Top-tier 叙事

保守叙事：

> Existing T2M generators optimize mostly sequence-level or uniformly aggregated losses, which can hide spatial-temporal gradient imbalance. We show that alignment-quality failures are partly formed during training by imbalanced gradients over text body-part phrases, joint groups, and temporal motion windows. A spatial-temporal guided training strategy reweights these learning signals and first audits their gradients before introducing routing, improving local alignment-quality behavior while preserving global text-motion alignment.

中文版本：

> 现有 T2M 训练常用整体或均匀聚合的 loss，容易掩盖 text/body/time 学习信号之间的不均衡。STGT 把 MoDebug 的关注点从“训练后哪一层敏感”推进到“训练中哪些文本短语、关节组和时间窗在塑造这种敏感性”，并先用最小 spatial-temporal weighted loss 与梯度观测来改善对齐与动作质量。

这个叙事和 FSD 的区别：

- FSD 是结构诱导：用 experts/router 显式承载功能。
- STGT 是过程诱导：用 spatial-temporal loss 和 gradient dynamics 塑造功能。
- 两者最终可能引向相同结论：更好的 T2M 模型需要可控的 functional decomposition。
- 但它们的实验抓手不同，因此可以作为互补贡献，而不是互相重复。

## 8. 必须否决的过强说法

- 不宣称第三视角完全取代 cross-baseline intervention 或 FSD。
- 不宣称所有 text/body/time group 都需要单独干预。
- 不宣称 spatial 或 temporal proxy 必须精确；MVP 应允许 soft weighting 和 proxy labels。
- 不宣称 gradient routing 一定优于 experts/router；它只是更接近训练动态的操作方式。
- 不宣称收益一定来自 layer 分工；也可能来自更好的 loss balancing 或 curriculum。
- 不宣称 uniform loss 一定错误；它只是可能掩盖文本指向身体部位或关键时间窗上的局部错误。

## 9. 路线图

| 阶段 | 目标 | 实验 | 成功标准 | Pivot |
|---|---|---|---|---|
| Phase 0 | 定义 spatial/temporal proxies | 50 条 text 的 joint group parser audit；motion-energy window 可视化抽检 | LLM joint-group recall `>=70%`；temporal windows 与人工观察基本一致 | spatial 改固定 group；temporal 回退 uniform |
| Phase 1 | Minimal weighting sanity | uniform、temporal-only、spatial-only 小规模 post-train 对照 | 任一局部 error 下降且整体 FID/R-Precision 不坏 | 降低权重范围；只保留 temporal 或 spatial |
| Phase 2 | Minimal spatial-temporal loss MVP | spatial-only、temporal-only、spatial+temporal、uniform、shuffle 对照 | text-mentioned joint error 和 high-weight window error 下降，permute 对照不复现，整体指标不坏 | 回退最有效单一路径或 uniform |
| Phase 3 | Gradient diagnostics | 记录 text/body/time group 的梯度范数、方向冲突、layer contribution | 梯度差异稳定，且能解释 layer sensitivity 或局部收益 | 转为诊断论文，暂缓训练改进 |
| Phase 4 | Gradient balancing / routing | 只在稳定冲突存在时测试 PCGrad 或 adapter-level scaling | 比 minimal weighting 更稳或更强 | 改回 soft weighting，避免训练不稳定 |
| Phase 5 | FFT/PoseFix/physics probes | 在 MVP 正向后测试 FFT/FLD-like 与 PoseFix-inspired annotation/probe | 只在特定 failure type 上提供额外解释或收益 | 不进入主 loss，保留为诊断 |
| Phase 6 | 与 0607 stage selection 合并 | sensitive stage + uniform/minimal weights vs neutral stage + uniform/minimal weights | 诊断选层与最小加权存在可分离增益 | 若失败，保留 0608 为 backbone-local loss balancing |
| Phase 7 | Cross-baseline validation | 在第二 backbone 上做小规模复核 | 至少趋势复现，允许幅度不同 | 收缩 claim 为 backbone-specific mechanism |

更新后的执行顺序：

1. Phase 0：先做 parser/window audit，不跑大实验。
2. Phase 1：做 post-train sanity：uniform、temporal-only、spatial-only。
3. Phase 2：做 minimal spatial-temporal MVP：spatial+temporal、uniform、shuffled/permute weights。
4. Phase 3：只观察 gradient attribution，不做 routing。
5. Phase 4：若存在稳定 `cos(g_align, g_gen) < -0.1` 或 group-specific 梯度集中，再加 PCGrad-style conflict handling 或 adapter-level scaling。
6. Phase 5：若最小方案有效，再把 FFT/FLD-like、PoseFix-inspired annotation 和更细 physics probes 作为诊断扩展。
7. Phase 6：再与 0607 的 sensitive stage / zero-init adapters 合并。

## 10. 最终判断

第三视角值得单独成文，但它不是一条完全分裂的新路线。它更像 MoDebug 的 **training formation layer**：

- 第一视角回答：哪里敏感？
- 第二视角回答：如何设计结构承载分工？
- 第三视角回答：这些分工如何在训练中由 text/body/time loss 与 gradient 形成，能否直接操控形成过程？

三者最终可能引向相同的大结论：提升 T2M alignment 和 quality 的关键不是单纯扩大模型或调 CFG，而是让文本、时间、空间和运动属性的学习信号在模型内部形成可控、可测、可训练的 functional decomposition。
