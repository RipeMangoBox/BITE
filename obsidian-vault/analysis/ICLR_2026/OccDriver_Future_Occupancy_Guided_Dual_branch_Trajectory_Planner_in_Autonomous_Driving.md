---
title: "OccDriver: Future Occupancy Guided Dual-branch Trajectory Planner in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OccDriver_Future_Occupancy_Guided_Dual_branch_Trajectory_Planner_in_Autonomous_D_fbeed04774ba.pdf
project_link: null
code_link: null
aliases:
- OccDriver
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用未来占用作为条件世界模型，通过粗到细的迭代解码将未来场景演化信息注入轨迹规划，从而改善交互感知。
primary_logic: 通过双分支架构在占用空间中预测未来场景演化，并以显式和隐式方式将该预测作为先验指导轨迹生成，同时结合边际占用分布实现应急规划，平衡安全与效率。
claims:
- OccDriver 在 nuPlan Val14 上达到 0.896 NR-S 和 0.838 R-S，显著优于 PlanTF、PLUTO 等主流方法，且在安全指标（Collisions 0.971, TTC 0.938）上表现最佳。
- 消融实验证明，逐步加入占用干扰损失、碰撞损失和对齐损失以及应急规划策略，能够持续提升安全性和驾驶评分，验证了所提损失函数和规划策略的有效性。
- nuPlan Val14 上 NR-S = 0.896
- nuPlan Val14 上 R-S = 0.838
---

# OccDriver: Future Occupancy Guided Dual-branch Trajectory Planner in Autonomous Driving

> [!tip] 核心洞察
> 通过双分支架构在占用空间中预测未来场景演化，并以显式和隐式方式将该预测作为先验指导轨迹生成，同时结合边际占用分布实现应急规划，平衡安全与效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | OccDriver：面向自动驾驶的未来占用引导双分支轨迹规划器 |
| 英文题名 | OccDriver: Future Occupancy Guided Dual-branch Trajectory Planner in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=abJCjkIwi5) · [paper](https://arxiv.org/abs/2502.13144) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | OccDriver |
| Dataset | nuPlan Val14, nuPlan Test14-Hard |

> [!tip] 效果简介
> - nuPlan Val14 上，NR-S 0.896 vs 0.890 (PLUTO) (+0.006)；R-S 0.838 vs 0.828 (DiffusionPlanner) (+0.010)。
> - nuPlan Test14-Hard 上，NR-S 0.794 vs 0.787 (PLUTO) (+0.007)；R-S 0.759 vs 0.753 (PLUTO) (+0.006)。

## 概要

自动驾驶轨迹规划的核心瓶颈在于多智能体交互建模的表示能力不足：纯向量化方法以个体为中心，忽略了密集的未来占用场景演化信息，导致交互预测不准；纯栅格化方法虽能建模场景级联合动态，却丢失了个体精确语义。针对这一矛盾，OccDriver 提出了一种**栅格-向量双分支架构**，其核心洞察是：利用未来占用作为条件世界模型，通过粗到细的迭代解码将未来场景演化信息注入轨迹规划，从而在保持个体语义的同时获得场景级交互感知。

具体而言，OccDriver 通过双分支在占用空间中预测未来场景演化，并以显式（占用引导损失）和隐式（交叉注意力条件作用）两种方式将该预测作为先验指导轨迹生成；同时引入边际占用分布实现应急规划，在短期考虑交互代理的行为不确定性，长期依赖联合占用分布，以此平衡安全与效率。

在 nuPlan Val14 闭环基准上，OccDriver 达到 **0.896 NR-S** 和 **0.838 R-S**，显著优于 PlanTF、PLUTO 等主流方法，且在安全指标（Collisions 0.971, TTC 0.938）上表现最佳。消融实验进一步证实，逐步加入占用干扰损失、碰撞损失、对齐损失以及应急规划策略，能够持续提升安全性和驾驶评分，验证了所提损失函数与规划策略的有效性。在更具挑战性的 nuPlan Test14-Hard 上，OccDriver 同样取得领先的 NR-S（0.794）和 R-S（0.759），证明了方法的鲁棒性。



自动驾驶中的轨迹规划本质上是一个高维交互决策问题：自车必须在动态场景中预测其他交通参与者的未来行为，并据此生成安全、高效且符合交通规则的行驶轨迹。这一问题的核心挑战在于**多智能体交互建模的表示能力不足**——现有方法在“场景级联合动态”与“个体级精确语义”之间存在根本性的张力。

当前主流的规划表示范式可归纳为两类。**栅格化方法**（如 **RasterModel** (Caesar et al., 2021)）将场景离散化为时空栅格，以占用图或流场的形式建模场景级的联合动态演化。这种表示天然适合捕捉密集交互和未来场景结构，但不可避免地丢失了个体代理的身份、意图等精确语义信息。**向量化方法**（如 **PlanTF** (Cheng et al., 2024b)、**PLUTO** (Cheng et al., 2024a)）则将场景元素抽象为稀疏的向量化特征，在个体层面进行轨迹规划，保留了精细的代理语义，却难以显式表征场景级的密集未来占用演化，导致交互预测精度受限。

这一表示鸿沟带来了两个直接后果。其一，纯向量化方法在复杂交互场景（如密集车流中的变道、无保护左转）中容易产生过于乐观或过于保守的规划，因为模型缺乏对未来场景“空间-时间”占用的全局感知。其二，纯栅格化方法虽然能预测未来占用，但缺乏将占用信息有效转化为个体轨迹的机制，规划结果往往粗糙且缺乏对个体代理行为的精确响应。

**OccDriver** 的动机正是弥合这一鸿沟。其核心洞察是：未来占用预测可以作为“条件世界模型”，将场景级的未来演化信息以显式和隐式两种方式注入轨迹规划过程。具体而言，通过**栅格-向量双分支架构**，在占用空间中预测未来场景演化，并以该预测作为先验指导轨迹生成；同时，利用**边际占用分布**捕捉短期行为不确定性，实现应急规划，在安全与效率之间取得平衡。

图 Figure 1 示意了三种表示范式的差异：栅格化框架在时空栅格中建模场景级联合动态，向量化框架执行个体级轨迹规划，而 OccDriver 的双分支框架则整合了场景级与个体级信息，并进一步将未来场景作为规划引导。这一设计使得模型既能感知密集的未来占用演化，又能保留个体代理的精确语义，从而在复杂交互场景中实现更优的规划质量。



## 核心方法与创新机理

OccDriver 的核心创新在于通过**栅格-向量双分支迭代解码架构**，将未来占用预测显式地注入轨迹规划，从而突破现有方法在多智能体交互建模上的表示瓶颈。以下从架构范式、交互建模、损失函数和应急机制四个维度展开分析。

### 1. 架构范式：从单一表示到双分支迭代解码

现有学习方法在场景表示上呈现两极化：**栅格化方法**（如 RasterModel, Caesar et al., 2021）将场景离散化为时空网格，能建模联合动态但丢失个体语义精度；**向量化方法**（如 PLUTO, Cheng et al., 2024a）保留个体精确表示，却难以捕捉密集的未来场景演化信息。OccDriver 通过双分支架构同时保留两种表示的优势（Fig. 2）。

双分支协作的核心是**粗到细的迭代解码流程**：向量化分支首先从联合场景特征中解码粗轨迹查询 $Q_c$（Eq. 4），栅格化分支以 $Q_c$ 为条件预测未来占用和流场 $Q_s$（Eq. 5），随后细轨迹解码器利用 $Q_s$ 精炼轨迹 $Q_f$（Eq. 6）。这种迭代设计使得轨迹规划与未来场景预测相互增强，而非独立执行。

消融实验（Table 13）直接验证了双分支架构的增益：相比纯向量化分支，双分支在安全性和进度指标上均有提升，确认了栅格分支引入的未来场景信息对规划的贡献。

### 2. 交互建模：未来占用作为条件世界模型

传统规划器仅利用当前时刻的场景交互特征进行决策，缺乏对未来多智能体演化态势的感知。OccDriver 的关键突破在于**将未来占用预测作为条件世界模型**，在占用空间中推演场景的动态演化，并将该预测以隐式和显式两种方式注入轨迹生成：

- **隐式注入**：通过交叉注意力（Eq. 2）和自注意力（Eq. 3）在联合场景编码器中融合向量化个体特征与栅格场景特征，使轨迹解码器能够感知占用空间中的交互关系。
- **显式注入**：通过占用引导损失直接约束轨迹与占用预测的一致性（详见损失函数部分）。

可视化结果（Fig. 5）表明，规划轨迹点（绿色）与自车高占用区域对齐，同时远离其他智能体的高占用区域，验证了未来占用引导的有效性。

### 3. 损失函数扩展：从单一回归到占用感知的多目标约束

OccDriver 在标准轨迹回归/分类损失和占用预测损失的基础上，引入了三个关键损失函数，构成对轨迹规划的显式占用引导：

- **占用干扰损失** $\mathcal{L}_{oi}$（Eq. 8）：惩罚自车占用预测与对手真实占用、以及对手占用预测与自车真实占用的重叠区域，强化交互感知能力。
- **占用引导损失** $\mathcal{L}_{og}$（Eq. 12）：由两部分组成——**对齐损失** $\mathcal{L}_{align}$（Eq. 9）惩罚轨迹点落在低占用区域，确保规划路径与自车未来占用一致；**碰撞损失** $\mathcal{L}_{collision}$（Eq. 10）惩罚轨迹点与高占用区域距离小于安全边界 $\eta$，强制安全间距。

消融实验（Table 3）表明：逐步加入 $\mathcal{L}_{oi}$ 提升了碰撞和舒适度指标；$\mathcal{L}_{collision}$ 的加入使碰撞指标从 0.943 提升至 0.960；$\mathcal{L}_{align}$ 通过引导轨迹与占用对齐提升了进度指标。三项损失共同作用，使得安全性和驾驶评分持续提升。

### 4. 应急规划：边际占用分布应对行为不确定性

现有方法通常仅预测所有智能体的联合占用分布，忽略了个体行为的短期不确定性。OccDriver 引入了**边际占用分布预测**（Sec. 3.3），对剪枝后的交互代理 $N_m$ 分别预测短期占用 $\mathbf{O}_{m,i}$（Eq. 7），并在应急规划阶段将其与联合占用融合（Eq. 11）：

$$\tilde{\mathbf{O}}_{a}^{*} = \begin{cases} \max(O_{a}^{t*}, \max_{i=1}^{N_{m}}(O_{m,i}^{t})), & t \leq T_s \\ O_{a}^{t*}, & t > T_s \end{cases}$$

短期（$t \leq T_s$）取联合占用与边际占用的最大值，保守考虑每个交互代理的潜在行为偏差；长期（$t > T_s$）仅使用联合占用，避免过度保守影响效率。这一机制在占用空间中实现了安全与效率的平衡——消融实验（Table 3）显示应急规划进一步提升了安全性和驾驶评分，仅带来轻微的进度下降。

### 创新边界与局限

需要指出，OccDriver 的创新建立在占用预测的离散化栅格表示之上，可能引入离散化伪影，且长时间预测的累积不确定性会影响占用引导的一致性。此外，边际占用分布仅在训练阶段使用，推断时依赖代理剪枝，可能遗漏重要交互。双分支架构引入了约 7.9M 额外参数和约 23ms 推理延迟，虽可控但对于超低延迟部署场景仍需优化。



OccDriver 的核心设计动机源于自动驾驶轨迹规划中两种主流表示范式的互补与局限：**栅格化方法**（如 **RasterModel**, Caesar et al., 2021）在时空栅格中建模场景级联合动态，能自然捕获密集的未来占用演化，但丢失了智能体的精确个体语义；**向量化方法**（如 **PLUTO**, Cheng et al., 2024a）在个体层面进行轨迹规划，保留了精细的智能体特征，却难以有效建模多智能体间的密集交互与场景级演化。OccDriver 提出**栅格-向量双分支架构**，通过在未来占用空间中预测场景演化，并以该预测作为条件先验指导轨迹生成，从而在个体精确性与场景交互完整性之间建立桥梁。

### Pipeline 总览

整体框架由三个核心功能模块串联构成，其输入输出流遵循统一的映射关系：

$$ \mathbf{Y}, \mathbf{Y}_{occ} = f(\mathbf{X}, \mathbf{X}_{occ} \mid \theta) $$

其中 $\mathbf{X}$ 包含自车状态 $\mathbf{E}$、智能体状态 $\mathbf{A}$、静态地图 $\mathbf{S}$ 和动态约束 $\mathbf{M}$ 等异构输入，$\mathbf{X}_{occ}$ 为历史占用栅格和流场输入，$\mathbf{Y}$ 和 $\mathbf{Y}_{occ}$ 分别为输出的规划轨迹和未来占用预测。三个模块的职责与数据流如下：

1. **上下文编码（Context Encoding）**：将异构输入分别编码为向量化个体特征 $F_{vec}$ 和栅格化场景特征 $F_{occ}$，形成双分支表示的基础。
2. **双分支迭代解码（Dual-Branch Iterative Decoding）**：以 $F_{vec}$ 和 $F_{occ}$ 为初始化，通过粗轨迹解码 → 未来场景解码 → 精轨迹解码的循环，实现轨迹与未来占用的粗到细迭代精炼。
3. **预测头（Prediction Heads）**：从解码特征输出多模态轨迹、置信度分数、未来占用栅格和流场。

此外，框架还包含两个增强机制：**边际占用分布预测**（Marginal Occupancy Encoder）用于建模个体智能体的短期行为不确定性，以及**应急规划融合**（Contingency Planning Fusion）将边际占用与联合占用融合以提升安全性。

### 上下文编码：异构输入的双分支表示

上下文编码阶段将异构输入分为两条并行的处理流：

- **向量化分支**：对 $\{\mathbf{E}, \mathbf{A}, \mathbf{S}, \mathbf{M}\}$ 分别使用独立的编码器提取个体级特征，随后通过 Transformer 编码器的自注意力机制进行场景级特征融合，生成向量化场景特征 $F_{vec}$。
- **栅格化分支**：将占用栅格和流场输入通过卷积骨干网络编码为栅格场景特征图 $F_{occ}$，保留空间结构信息。

### 双分支迭代解码：粗到细的轨迹-占用协同精炼

这是 OccDriver 的核心创新模块，通过三个解码器的交替迭代实现轨迹规划与未来占用预测的相互增强：

1. **粗轨迹解码器 $D_c$**：以可学习的向量化查询 $Q_{vec}$ 为 Query，以占用特征 $F_{occ}$ 为 Key/Value，通过交叉注意力生成多模态粗轨迹查询 $Q_c$：
   $$ Q_{c} = D_{c}(\mathrm{Q}=Q_{vec}, \mathrm{K},\mathrm{V}=F_{occ}, \{F_{S},F_{M}\}) $$

2. **未来场景解码器 $D_s$**：以 $F_{occ}$ 为 Query，以粗轨迹查询 $Q_c$ 为 Key/Value，通过交叉注意力将粗轨迹信息注入场景特征，解码未来占用和流场 $Q_s$：
   $$ Q_{s} = D_{s}(\mathrm{Q}=F_{occ}, \mathrm{K},\mathrm{V}=Q_{c}, \{F_{S},F_{M}\}) $$

3. **精轨迹解码器 $D_f$**：以粗轨迹查询 $Q_c$ 为 Query，以未来场景特征 $Q_s$ 为 Key/Value，利用预测的未来场景演化信息精炼轨迹查询 $Q_f$：
   $$ Q_{f} = D_{f}(\mathrm{Q}=Q_{c}, \mathrm{K},\mathrm{V}=Q_{s}, \{F_{S},F_{M}\}) $$

这一迭代结构的关键在于：粗轨迹为未来占用预测提供了“意图条件”，使占用预测不再是盲目的外推；而精炼后的未来占用反过来为轨迹优化提供了“世界模型”式的反馈，使轨迹能够前瞻性地避开未来可能的高占用区域。消融实验证实，双分支架构相比纯向量分支在安全性和进度指标上均有显著提升（Table 13）。

### 边际占用与应急规划

在标准联合占用预测之外，OccDriver 引入**边际占用分布预测**来处理交互场景中的行为不确定性。具体流程为：首先通过 Agent Pruning 模块筛选出与自车存在潜在交互的 $N_m$ 个智能体，然后对每个交互智能体独立预测其短期边际占用 $\mathbf{O}_{m,i}$：

$$ \{ F_{i} \mid i = 1, 2, \ldots, N_{m}\} = \mathrm{Prune}(F_{A}), \quad F_{m,i} = f_{m}(F_{s}, F_{i}), \quad \mathbf{O}_{m,i} = \mathrm{Conv}(\mathrm{Upsample}(F_{m,i})) $$

在**应急规划**阶段，将短期（$t \leq T_s$）的联合占用与边际占用取最大值融合，以覆盖智能体可能的多模态行为；长期（$t > T_s$）则仅使用联合占用以保证一致性：

$$ \tilde{\mathbf{O}}_{a}^{*} = \begin{cases} \max(O_{a}^{t*}, \max_{i=1}^{N_{m}}(O_{m,i}^{t})), & t \leq T_{s} \\ O_{a}^{t*}, & t > T_{s} \end{cases} $$

这种设计在安全性与效率之间取得平衡：短期保守地考虑多种可能行为以防范突发风险，长期依赖稳定的联合预测以保持规划进度。

### 占用引导的损失函数体系

为确保未来占用预测能够有效指导轨迹规划，OccDriver 设计了三个互补的损失函数：

- **占用干扰损失 $\mathcal{L}_{oi}$**：惩罚自车占用预测与对手真实占用之间的重叠区域，增强占用预测的交互感知能力。
- **轨迹-占用对齐损失 $\mathcal{L}_{align}$**：惩罚轨迹点落在自车低占用概率区域的情况，确保轨迹与预测的可行区域一致。
- **轨迹-占用碰撞损失 $\mathcal{L}_{collision}$**：惩罚轨迹点与高占用区域距离小于安全边界 $\eta$ 的情况，显式地将安全约束注入轨迹优化。

总训练损失为上述损失与基础轨迹损失、占用预测损失的加权组合：

$$ \mathcal{L} = \mathcal{L}_{traj} + \mathcal{L}_{occ} + \mathcal{L}_{oi} + \mathcal{L}_{og} $$

其中 $\mathcal{L}_{og} = w_1 \mathcal{L}_{align} + w_2 \mathcal{L}_{collision}$ 为占用引导损失。消融实验表明，逐步加入各损失组件能持续提升安全性和驾驶评分（Table 3），验证了该损失函数体系的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of the OccDriver comprises three fundamentals. Context Encoding first encodes heterogeneous inputs into vectorized individual features*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of different representation paradigms: (a) rasterized framework models the scenelevel joint dynamics in spatiotemporal grids; (b) vectorized framework performs individual-level trajectory planning; (c) our proposed dual-branch framework integrates scene-level and individuallevel information, further leveraging future scene as planning guidance*



### 3.1 问题形式化

OccDriver 将轨迹规划建模为一个条件生成问题。给定异构输入 $\mathbf{X}$（包括自车状态、周围代理、静态地图和交通信号）以及占用与流输入 $\mathbf{X}_{occ}$，神经网络 $f$ 以参数 $\theta$ 同时输出自车轨迹 $\mathbf{Y}$ 和未来占用预测 $\mathbf{Y}_{occ}$：

$$\mathbf{Y}, \mathbf{Y}_{occ} = f(\mathbf{X}, \mathbf{X}_{occ} \mid \theta)$$

这一形式化将轨迹规划与未来场景演化预测统一在同一框架下，为后续的双分支迭代解码提供了数学基础。

### 3.2 双分支架构与迭代解码

OccDriver 的核心架构由三个基础模块构成：上下文编码（Context Encoding）、双分支迭代解码结构（Dual-Branch Iterative Decoding）和预测头（Prediction Heads），如 Figure 2 所示。

**上下文编码**分为两个并行的分支。向量化分支将异构输入 $\{E, A, S, M\}$（自车、代理、静态地图、交通信号）通过各自的编码器编码为个体级特征 $F_{vec}$。栅格化分支则将占用和流输入编码为联合场景特征图 $F_s$，随后通过交叉注意力将粗轨迹特征集成到场景特征图中：

$$F_{s} = \mathrm{CrossAttn}(F_{s}, F_{vec}, F_{vec})$$

接着通过自注意力在占用空间中融合特征，生成编码后的占用特征 $F_{occ}$：

$$F_{occ} = \mathrm{SelfAttn}(F_{s})$$

**双分支迭代解码结构**是方法的核心创新，通过粗到细的迭代过程实现轨迹与未来占用的相互增强。具体流程为：

1. **粗轨迹解码器 $D_c$**：以向量化查询 $Q_{vec}$ 为查询，以占用特征 $F_{occ}$ 以及静态地图和交通信号特征 $\{F_S, F_M\}$ 为键值，解码多模态粗轨迹查询 $Q_c$：

$$Q_{c} = D_{c}(\mathrm{Q}=Q_{vec}, \mathrm{K},\mathrm{V}=F_{occ}, \{F_{S},F_{M}\})$$

2. **未来场景解码器 $D_s$**：以粗轨迹 $Q_c$ 为条件，以占用特征 $F_{occ}$ 为查询，解码未来场景演化特征 $Q_s$（包括未来占用和流场）：

$$Q_{s} = D_{s}(\mathrm{Q}=F_{occ}, \mathrm{K},\mathrm{V}=Q_{c}, \{F_{S},F_{M}\})$$

3. **精轨迹解码器 $D_f$**：利用未来场景特征 $Q_s$ 精炼轨迹查询，生成最终的多模态轨迹查询 $Q_f$：

$$Q_{f} = D_{f}(\mathrm{Q}=Q_{c}, \mathrm{K},\mathrm{V}=Q_{s}, \{F_{S},F_{M}\})$$

这一迭代结构的设计动机在于：粗轨迹为未来占用预测提供空间先验，而预测的未来场景演化反过来为轨迹精炼提供交互感知信息，形成闭环增强。

### 3.3 边际占用分布与应急规划

为应对交互代理的行为不确定性，OccDriver 在联合占用分布之外，额外建模个体代理的短期边际占用分布。给定代理特征 $F_A$，首先通过剪枝操作 $\mathrm{Prune}(\cdot)$ 筛选出 $N_m$ 个交互代理，然后对每个代理 $i$ 独立预测其边际占用：

$$\{ F_{i} \mid i = 1, 2, \ldots, N_{m}\} = \mathrm{Prune}(F_{A})$$

$$F_{m,i} = f_{m}(F_{s}, F_{i})$$

$$\mathbf{O}_{m,i} = \mathrm{Conv}(\mathrm{Upsample}(F_{m,i}))$$

其中 $f_m$ 为边际占用编码器，$\mathbf{O}_{m,i}$ 为第 $i$ 个代理的边际占用预测。

在推理阶段，应急规划通过融合短期边际占用与长期联合占用来实现。对于时间步 $t \leq T_s$（短期），取联合占用与所有边际占用的逐元素最大值，以保守考虑潜在行为不确定性；对于 $t > T_s$（长期），仅使用联合占用预测：

$$\tilde{\mathbf{O}}_{a}^{*} = \begin{cases} \max(O_{a}^{t*}, \max_{i=1}^{N_{m}}(O_{m,i}^{t})), & t \leq T_{s} \\ O_{a}^{t*}, & t > T_{s} \end{cases}$$

### 3.4 损失函数设计

OccDriver 的总训练损失由四个部分组成：

$$\mathcal{L} = \mathcal{L}_{traj} + \mathcal{L}_{occ} + \mathcal{L}_{oi} + \mathcal{L}_{og}$$

**占用干扰损失 $\mathcal{L}_{oi}$** 用于增强自车与代理占用预测之间的交互感知。它惩罚预测占用与对手真实占用之间的重叠区域，由自车-代理干扰和代理-自车干扰两部分组成：

$$\mathcal{L}_{oe} = \mathrm{sum}(\mathbf{O}_{e}^{*} \cdot \mathbf{O}_{a}^{gt}) / \mathrm{sum}(\mathbf{O}_{a}^{gt})$$

$$\mathcal{L}_{oa} = \mathrm{sum}(\mathbf{O}_{a}^{*} \cdot \mathbf{O}_{e}^{gt}) / \mathrm{sum}(\mathbf{O}_{e}^{gt})$$

$$\mathcal{L}_{oi} = \mathcal{L}_{oe} + \mathcal{L}_{oa}$$

**占用引导损失 $\mathcal{L}_{og}$** 通过显式约束将未来占用预测作为轨迹规划的监督信号，由对齐损失和碰撞损失加权组成：

$$\mathcal{L}_{og} = w_{1} \mathcal{L}_{align} + w_{2} \mathcal{L}_{collision}$$

其中对齐损失 $\mathcal{L}_{align}$ 惩罚轨迹点落入低占用概率区域（低于阈值 $\varepsilon$）的情况，确保自车轨迹与预测的未来占用保持一致：

$$\mathcal{L}_{align} = \frac{1}{T_{f}} \sum_{t=1}^{T_{f}} \sum_{i=1}^{N_{v}} \max(0, \varepsilon - O_{i}^{t})$$

碰撞损失 $\mathcal{L}_{collision}$ 惩罚轨迹点与高占用区域的距离小于安全边界 $\eta$ 的情况，强制轨迹远离潜在碰撞区域：

$$\mathcal{L}_{collision} = \frac{1}{T_{f}} \sum_{t=1}^{T_{f}} \sum_{i=1}^{N_{v}} \max(0, \eta - d_{i}^{t})$$

其中 $d_i^t$ 为轨迹点 $i$ 在时间步 $t$ 到最近高占用区域的距离。

轨迹规划损失 $\mathcal{L}_{traj}$ 和占用预测损失 $\mathcal{L}_{occ}$ 的具体形式见附录（Eq. 14-15），分别由回归/分类/粗轨迹损失和自车/代理/边际/流损失加权组成。

### 3.5 关键设计决策

消融实验（Table 3）验证了各损失组件的因果贡献：逐步加入占用干扰损失 $\mathcal{L}_{oi}$ 提升了碰撞和舒适度指标；加入碰撞损失 $\mathcal{L}_{collision}$ 将碰撞指标从 0.943 提升至 0.960；对齐损失 $\mathcal{L}_{align}$ 通过引导机制提升进度指标；应急规划策略在提升安全性的同时，进度指标略有下降，体现了安全与效率的权衡。双分支架构相比纯向量分支在安全性和进度上均有提升（Table 13），验证了栅格-向量双分支迭代解码的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of closed-loop planning on nuPlan Test14 − Hard benchmark. All metrics are higher the better. Compared to vectorized-only, topology-guided and diffusion-based methods, OccDriver achieves top driving scores with desirable planning safety and progress*



## 实验与关键发现

### 主要结果：闭环规划性能

OccDriver 在 nuPlan Val14 基准上取得了领先的闭环规划性能。**Table 1** 给出了与其他学习型规划方法的全面对比。在非反应式评分（NR-S）上，OccDriver 达到 **0.896**，优于 PLUTO（0.890）和 DiffusionPlanner（0.889）；在反应式评分（R-S）上达到 **0.838**，同样超过 DiffusionPlanner（0.828）和 PLUTO（0.826）。更关键的是，OccDriver 在安全指标上表现最优：碰撞指标（Collisions）达到 0.971，碰撞时间（TTC）达到 0.938，表明该方法在高交互密度场景下仍能保持可靠的安全边界。

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of closed-loop planning on nuPlan Val14 benchmark. All metrics are higher the better. Among learning-based methods, OccDriver achieves SOTA in both nonereactive score (NR-S) and reactive score (R-S) with top safety performance (Collisions and TTC)*

在更具挑战性的 nuPlan Test14-Hard 基准上（**Table 2**），OccDriver 继续保持优势，NR-S 达到 0.794，R-S 达到 0.759，均优于 PLUTO（0.787/0.753）和 DiffusionPlanner（0.776/0.746）。值得注意的是，在进度指标（Progress）上 OccDriver 也达到 0.829，说明未来占用引导在保障安全的同时并未牺牲通行效率。

### 消融实验：组件有效性验证

**Table 3** 的系统消融揭示了各组件对性能的贡献机制：

1. **占用干扰损失（$L_{oi}$）**：在基础模型上加入 $L_{oi}$ 后，碰撞指标从 0.943 提升至 0.960，TTC 也有改善。该损失通过惩罚自车占用预测与对手真实占用之间的重叠区域，强化了模型对交互冲突的感知能力。

2. **占用引导损失（$L_{og}$）**：由对齐损失 $L_{align}$ 和碰撞损失 $L_{collision}$ 组成。$L_{align}$ 确保轨迹点落在自车高占用概率区域，主要提升进度指标；$L_{collision}$ 惩罚轨迹点与高占用区域距离小于安全边界 $\eta$ 的情况，是安全性提升的核心驱动力。

3. **应急规划（Contingency Planning）**：在短期预测窗口（$t \leq T_s$）内融合边际占用分布与联合占用分布，进一步将碰撞指标推至 0.971。这一机制显式建模了交互代理的行为不确定性，使规划器在密集交通中保留安全裕度。

4. **双分支架构**：**Table 13** 显示，相比纯向量化分支，双分支架构在碰撞（+0.021）和进度（+0.015）上均有显著提升，验证了栅格分支提供的未来场景演化信息对交互感知的不可替代性。

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/018_Table_13.jpg]]
*Table 13: Comparison between vector-only and dual-branch architectures*

### 关键超参数分析

- **解码模态数 $M$**（**Table 12**）：$M=9$ 时 NR-S 和 R-S 达到最优（0.848/0.805）。模态过少导致覆盖不足，过多则引入噪声。
- **占用预测时域 $T_{occ}$**（**Table 10**）：$T_{occ}=6s$ 时碰撞和驾驶评分最佳。更长时域（8s）因累积不确定性导致性能退化。
- **碰撞损失权重 $w_2$**（**Table 11**）：$w_2=9$ 时碰撞和 TTC 最优。进一步增大权重会导致过惩罚，损害进度指标。
- **高占用区域阈值 $\zeta$**（**Table 5**）：影响碰撞损失的触发灵敏度，需与安全边界 $\eta$ 协同调节。

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/017_Table_12.jpg]]
*Table 12: Impact of different numbers M of decoding modalities*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/016_Table_10.jpg]]
*Table 10: Impact of different prediction horizons*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/009_Table_5.jpg]]
*Table 5: Impact of different threshold ζ of highoccupancy regions in*

### 粗到细轨迹解码的有效性

**Table 6** 对比了粗轨迹与精炼轨迹的规划性能。精炼轨迹在所有指标上均优于粗轨迹，尤其在碰撞指标上提升显著。**Figure 6** 的定性可视化进一步表明，粗轨迹提供了多模态候选，而精炼轨迹通过融合未来占用信息消除了不安全的候选，最终输出交互合规的平滑轨迹。

### 计算开销与扩展性

**Table 14** 显示，双分支架构和边际占用预测分别引入约 7.9M 额外参数和约 23ms 推理延迟。**Table 15** 表明，边际占用的内存占用随代理数量线性增长，代理剪枝（Agent Pruning）可有效控制计算开销，且 **Table 7** 证明剪枝对闭环性能影响极小。

### 失败模式与局限性

尽管 OccDriver 在基准测试中表现优异，分析揭示了以下潜在失败模式：

1. **离散化伪影**：占用预测基于离散栅格，边界区域可能出现概率断裂，导致 $L_{align}$ 在边缘情况下错误惩罚有效轨迹点。
2. **长时域退化**：$T_{occ} > 6s$ 时累积不确定性使未来占用预测与真实场景偏离，引导损失反而误导轨迹精炼。
3. **边际占用推断缺失**：应急规划仅在训练阶段使用边际占用分布，推断时依赖代理剪枝，可能遗漏长尾交互场景中的关键行为模式。
4. **端到端集成空白**：当前实现未集成感知模块，**Table 16** 的端到端实验虽展示了可行性，但与真实部署仍有差距。

### 开放问题

- 如何将离散占用分布扩展为统一的时空占用场，以获得更平滑的时间一致性？
- 能否开发无缝集成的端到端框架，在保持双分支信息优势的同时消除额外推理开销？
- 如何将占用引导范式适配到风险感知的安全强化学习框架（如 CVaR 约束）？
- 在大规模代理场景下，如何进一步降低边际占用的计算复杂度？

### 补充图表

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/008_Table_3.jpg]]
*Table 3: Ablation results of OccDriver’s planning performance with different components. All proposed components contribute to improvements in safety metrics and driving scores*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of future occupancy prediction and guidance. (a) ego’s (red) and agents’ (purple) occupancy predictions coincide with their GT bounding boxes; (b) planning trajectory (green point) aligns with ego’s occupancy while keeps away from agents’ occupancy*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/013_Figure_6.jpg]]
*Figure 6: Visualization of coarse trajectory and fine trajectory in nuPlan Test14 − Hard benchmark*

![[assets/figures/papers/paper_list_l71_https_openreview_net_forum_id_abJCjkIwi5/figures/011_Table_6.jpg]]
*Table 6: Planning performance comparison between coarse and fine trajectories*



## 定位与知识库关联

### 1. 表示范式的演进定位

自动驾驶规划方法的核心分歧在于场景表示的选择。OccDriver 的提出直接回应了当前两大范式的结构性缺陷：

- **纯栅格化范式**（如 **RasterModel** (Caesar et al., 2021)）将场景建模为时空栅格中的联合动态，能够捕获密集的占用演化信息，但丢失了个体智能体的精确语义和身份信息，导致规划难以区分关键交互对象。
- **纯向量化范式**（如 **PLUTO** (Cheng et al., 2024a)、**PlanTF** (Cheng et al., 2024b)、**DiffusionPlanner** (Zheng et al., 2025a)）以个体为中心进行轨迹规划，保留了精确的智能体语义，但忽略了场景级的联合未来演化，使得多智能体交互建模能力不足。

OccDriver 的**栅格-向量双分支架构**（Figure 1c）在表示层面实现了两类范式的互补：向量化分支维护个体语义精确性，栅格化分支通过预测未来占用和流场来表征场景级联合演化，二者通过交叉注意力机制进行信息融合。这一设计使得方法既不同于纯栅格化的 **UrbanDriver** (Scheel et al., 2022)，也区别于拓扑引导的 **BeTopNet** (Liu et al., 2024a) 和端到端的 **UniAD**、**Transfuser**、**PARA-Drive** 等方法。

### 2. 核心机制差异：从“当前交互”到“未来演化注入”

OccDriver 的关键创新在于将**未来占用预测从辅助任务提升为规划的条件世界模型**。现有方法通常仅在当前时刻进行交互特征提取，而 OccDriver 通过粗到细的迭代解码结构，将未来场景演化信息显式注入轨迹生成过程：

- **粗轨迹解码器**（$D_c$）从联合场景特征生成多模态初始轨迹；
- **未来场景解码器**（$D_s$）以粗轨迹为条件预测未来占用和流场，形成“如果我这样走，世界将如何演化”的条件预测；
- **精轨迹解码器**（$D_f$）利用未来场景特征精炼轨迹。

这种条件预测机制使得规划不再是“盲目的轨迹采样+评分”，而是“预测-验证-精炼”的闭环过程，本质上是一种**隐式的模型预测控制**。

### 3. 损失函数设计的独特贡献

OccDriver 在损失函数层面引入了三项关键扩展，与现有方法形成差异化：

| 损失组件 | 功能 | 与 baseline 的差异 |
|---------|------|-------------------|
| 占用干扰损失 $\mathcal{L}_{oi}$ | 惩罚自车预测占用与对手真实占用的重叠 | baseline 通常仅使用独立的占用预测损失，缺乏交互感知 |
| 占用引导损失 $\mathcal{L}_{og}$ | 包含对齐损失和碰撞损失，引导轨迹与占用空间一致 | 建立了轨迹空间与占用空间的显式约束桥梁 |
| 应急规划损失 | 融合边际占用分布处理行为不确定性 | baseline 未明确建模不确定性 |

消融实验（Table 3）证实，逐步加入这些损失组件能够持续提升安全性和驾驶评分：碰撞损失使碰撞指标从 0.943 提升至 0.960，对齐损失通过引导提升进度指标，应急规划进一步提升安全性。

### 4. 应急规划机制的定位

OccDriver 的应急规划策略通过**边际占用分布预测**来处理多智能体交互中的行为不确定性。与传统的多模态轨迹预测不同，该方法在占用空间中建模个体智能体的短期潜在行为，并在推理时通过 $\tilde{\mathbf{O}}_a^* = \max(O_a^{t*}, \max_{i=1}^{N_m}(O_{m,i}^t))$ 将边际占用与联合占用融合，实现保守的安全规划。这一机制与安全强化学习中的风险感知目标（如 CVaR）有概念上的关联，但实现方式更为直接和可解释。

### 5. 适用边界与局限

尽管 OccDriver 在 nuPlan 基准上取得了 SOTA 性能，但其设计存在明确的适用边界：

- **离散化伪影**：占用预测基于离散化栅格，可能引入空间离散化误差，且长时间预测的累积不确定性影响时间一致性。
- **边际占用的推理限制**：边际占用分布仅在训练阶段使用，推理时依赖代理剪枝，可能遗漏重要交互对象。
- **计算开销**：双分支架构增加了约 7.9M 参数和约 23ms 推理延迟（Table 14），虽可控但对于超低延迟嵌入式设备仍需优化。
- **感知集成缺失**：当前实施尚未在完整的端到端闭环系统中集成感知模块，向真实世界部署仍需扩展。

### 6. 开放问题与后续方向

基于 OccDriver 的设计框架，以下开放问题值得进一步探索：

1. **统一时空占用分布**：如何将离散的占用分布扩展为统一的时空占用分布，以获得更平滑的时间一致性？
2. **端到端无缝集成**：如何开发一个端到端框架，将双分支信息无缝集成，避免额外的计算开销？
3. **风险感知扩展**：如何将占用引导范式适配到带有风险感知目标（如 CVaR）的安全强化学习中？
4. **大规模场景优化**：如何进一步减少大规模智能体场景下的边际占用计算开销？
5. **意图交互建模**：如何将占用引导扩展到更复杂的交通参与者行为预测，如意向交互和博弈场景？



## 原文 PDF

![[paperPDFs/ICLR_2026/OccDriver_Future_Occupancy_Guided_Dual_branch_Trajectory_Planner_in_Autonomous_D_fbeed04774ba.pdf]]
