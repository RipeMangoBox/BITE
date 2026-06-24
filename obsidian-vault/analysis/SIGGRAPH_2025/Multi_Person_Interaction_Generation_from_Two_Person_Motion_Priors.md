---
title: Multi Person Interaction Generation from Two Person Motion Priors
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors.pdf
aliases:
- GDIS
- MPIGFTPMP
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将多人交互分解为图结构上的双人交互（Pairwise Interaction Graph），并利用两个图引导的损失项（Proxemics loss 和 Gauss Linking Integral loss）对扩散采样过程进行优化，以此控制交互质量和减少穿透。
primary_logic: 多人交互可以建模为一个图，其中每个节点代表一个人，有向边表示条件依赖关系。这样即可利用现有的双人交互扩散模型作为运动先验，通过并行条件采样生成多人交互，并通过基于图的额外损失来约束空间关系，从而避免重新训练模型，同时保持交互的多样性和可控性。
claims:
- 在双人交互中，本方法相对于InterGen穿透深度减少了76.53%，相对于FreeMotion减少了85.38%。
- 在3人交互配置下，本方法在所有指标上均优于FreeMotion，且随着人数增加优势更为明显（如4人时Pair-FID更低）。
- 消融实验表明，移除Proxemics和GLI损失后，穿透深度和接触点数大幅增加（如4人时穿透增加96.33%），验证了损失项的有效性。
- InterHuman test set 上 PeneBone (m) = 0.211
---

# Multi Person Interaction Generation from Two Person Motion Priors

> [!tip] 核心洞察
> 多人交互可以建模为一个图，其中每个节点代表一个人，有向边表示条件依赖关系。这样即可利用现有的双人交互扩散模型作为运动先验，通过并行条件采样生成多人交互，并通过基于图的额外损失来约束空间关系，从而避免重新训练模型，同时保持交互的多样性和可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于双人运动先验的多人交互生成 |
| 英文题名 | Multi Person Interaction Generation from Two Person Motion Priors |
| 会议/期刊 | SIGGRAPH 2025 |
| Links |  [paper](https://arxiv.org/abs/2505.17860)|
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Graph-driven Interaction Sampling |
| Dataset | InterHuman test set, Close interaction subset, Multi-person interactions |

> [!tip] 效果简介
> - InterHuman test set 上，PeneBone (m) 0.211 vs 0.899 (-0.688 (-76.53%))；PeneBone (m) 0.211 vs 1.443 (-1.232 (-85.38%))。
> - Close interaction subset 上，PeneBone (m) 0.525 vs 2.335 (-1.810 (-77.52%))。
> - Multi-person interactions (3 chars) 上，Pair-FID 72.294 vs 81.621 (-9.327)。

## 概述

### 问题背景

生成高质量、无穿透的多人交互运动是当前运动生成领域的核心瓶颈之一。现有方法面临三重困难：**多人交互数据集稀缺**，使得直接训练大规模多人模型不可行；**双人交互模型无法直接扩展至可变人数**，缺乏对多人空间关系的有效建模；少数已有的多人生成方法（如 FreeMotion）往往产生**重复动作和严重的身体穿透**。

### 核心思路

本文提出 **Graph-driven Interaction Sampling**，其关键洞察是：**多人交互可以建模为一个图结构**，其中每个节点代表一个人物，有向边表示条件依赖关系。该方法将复杂的多人交互分解为图上的成对交互（Pairwise Interaction Graph），从而直接复用已有的双人交互扩散模型（如 InterGen）作为运动先验，无需重新训练。在此基础上，引入两个图引导的损失项——**Proxemics 损失**和 **Gauss Linking Integral (GLI) 损失**——在扩散采样过程中进行优化，约束非交互角色之间的空间距离与交互角色之间的穿透程度，在保持运动多样性的同时显著提升交互质量。

### 方法定位

该方法属于**免训练、基于图分解的扩散后验采样框架**。与 InterGen（Liang et al., IJCV 2024）等双人生成模型和 FreeMotion（Fan et al., ECCV 2024）等多人生成模型相比，其核心变化在于：
- **采样方案**：从同时生成两个人物运动改为基于 Pairwise Interaction Graph 的并行条件采样，支持可变人数和时变图结构；
- **损失函数**：在扩散采样过程中额外引入 Proxemics 损失和 GLI 损失，替代仅使用扩散模型原始损失的方案。

### 主要结果

在双人交互场景下，本方法相较 InterGen 穿透深度（PeneBone）降低 **76.53%**，相较 FreeMotion 降低 **85.38%**；在近距离交互子集上，穿透深度降低 **77.52%**（Table 1–2）。在多人交互（3–5人）场景下，本方法在所有指标上均优于 FreeMotion，且人数越多优势越明显（Table 3）。消融实验表明，移除 Proxemics 和 GLI 损失后，穿透深度大幅增加（4人时增加 **96.33%**），验证了损失项的核心作用（Table 4）。

### 局限与展望

本方法完全依赖双人模型，无法捕捉图中非直接连接节点之间的关系；优化过程增加了计算开销，且仍无法完全避免穿透。未来方向包括利用大语言模型自动生成图结构，以及引入物理模拟进一步消除残余穿透。

## 背景与动机

### 问题背景：多人交互生成的现实需求与核心挑战

生成逼真的人类运动交互是计算机视觉与图形学中长期存在的核心问题，其应用涵盖虚拟现实、游戏动画、人机交互与具身智能体训练等场景。随着扩散模型在单人与双人运动生成任务中取得显著进展，一个更具挑战性的方向浮现出来：**如何生成包含三人及以上角色的高质量多人交互运动？**

这一问题的本质困难在于**组合复杂性**与**数据稀缺性**的双重约束。多人交互不仅需要每个角色自身的运动自然流畅，更要求角色之间的空间关系——接触、避碰、协同——在时间维度上保持物理合理性。然而，现有的运动捕捉数据集中于单人动作或双人交互，三人及以上的密集交互数据极为稀少。这使得直接训练一个端到端的多人交互生成模型在数据层面几乎不可行。

### 现有方法的缺口：从双人到多人的扩展困境

当前最先进的双人交互生成方法，如 **InterGen**（Liang et al., IJCV 2024），利用扩散模型在双人交互数据集上取得了令人瞩目的结果，能够生成具有丰富接触与响应的双人运动。然而，这类模型**无法直接扩展至可变人数**的场景——其架构天然假设输入与输出均为固定数量的两个角色，缺乏处理任意人数交互的机制。

另一方面，少数尝试解决多人生成问题的方法，如 **FreeMotion**（Fan et al., ECCV 2024），虽然支持多人运动生成，但存在两个严重缺陷：**重复动作模式**——多个角色倾向于生成高度相似的运动，缺乏个体差异与角色分工；以及**严重穿透问题**——角色之间的身体网格频繁发生相互穿透，破坏了交互的物理可信度。这些问题根源于现有方法缺乏对多人空间关系的显式建模与约束机制。

### 本文动机：将多人交互分解为可控的双人交互图

面对上述困境，本文提出了一个关键的洞察：**复杂的多人交互可以在空间与时间上被分解为多个双人交互的图结构**。这一洞察源于对真实多人交互场景的观察——无论是三人打斗还是多人舞蹈，交互的本质往往表现为若干组角色对之间的接触与响应，而非所有角色同时与所有其他角色发生紧密交互。

基于这一洞察，本文的核心动机是：**充分利用现有双人交互扩散模型的强大先验能力，通过图结构将多人交互分解为并行条件采样的双人交互，从而在不重新训练模型的前提下，生成高质量、低穿透且可控的多人交互运动**。这一思路将“从零训练多人模型”的难题转化为“如何有效组合双人先验并施加空间约束”的优化问题，既规避了数据稀缺的瓶颈，又保持了双人模型已具备的交互多样性与运动质量。

## 核心创新

本工作提出 **Graph-driven Interaction Sampling**，其核心创新在于将多人交互生成问题转化为**图结构上的并行双人条件采样 + 扩散后验优化**，从而在无需重新训练模型的前提下，利用现有双人交互扩散模型生成可变人数的多人交互，并显著减少穿透。

### 1. 问题瓶颈与因果杠杆

现有方法的根本瓶颈在于：多人交互数据集稀缺，双人交互模型无法直接扩展至可变人数，而少数现有的多人生成方法（如 **FreeMotion**，Fan et al., ECCV 2024）会产生重复动作和严重穿透。本方法的**因果杠杆**是将多人交互分解为 **Pairwise Interaction Graph**（成对交互图）上的双人交互，并利用两个图引导的损失项——**Proxemics loss** 和 **Gauss Linking Integral (GLI) loss**——对扩散采样过程进行优化，以此控制交互质量和减少穿透。

### 2. Changed Slots：相对于基线的关键改动

#### Slot 1：采样方案——从同步生成到图驱动的并行条件采样

- **基线做法**：**InterGen**（Liang et al., IJCV 2024）等双人模型同时生成两个人物运动并相互条件，但无法直接处理三人及以上场景；**FreeMotion** 虽支持多人，但生成质量随人数增加而下降。
- **本方法**：基于 Pairwise Interaction Graph 的并行条件采样。用户定义多人之间的交互图结构（支持时间变化图），每个节点代表一个人，有向边表示条件依赖关系。采样时同时运行 $n$ 个去噪过程，每个节点的运动以图中指定的邻居为条件。这一设计将多人交互的联合分布建模为成对因子的乘积：
  $$p ( x ^ { 1 } , x ^ { 2 } , . . . , x ^ { n } ) = { \frac { 1 } { Z } } \prod _ { ( i , j ) \in \mathrm { e d g e s } } \phi _ { i  j } ( x _ { i } , x _ { j } )$$
  其中 $\phi_{ij}$ 由预训练的双人扩散模型提供。此方案无需额外训练，即可支持任意人数和动态变化的交互图结构（Sec. 4.1, Fig. 2, Fig. 3）。

#### Slot 2：损失函数——从简单重构损失到图引导的交互优化损失

- **基线做法**：扩散模型通常仅使用原始的重构损失进行采样，缺乏对多人空间关系的显式约束。
- **本方法**：在扩散采样过程中引入两个新的损失函数进行梯度下降优化（Sec. 4.2）：
  - **Proxemics Loss**：惩罚交互图中**非直接连接**的角色之间的包围盒重叠，避免非交互角色发生意外的空间侵入。
  - **Gauss Linking Integral (GLI) Loss**：惩罚交互角色之间的穿透。GLI 是衡量两条空间曲线缠绕程度的拓扑不变量，其连续形式为：
    $$G ( \gamma _ { 1 } , \gamma _ { 2 } ) = \frac { 1 } { 4 \pi } \int _ { \gamma _ { 1 } } \int _ { \gamma _ { 2 } } \frac { d \boldsymbol { r } _ { 1 } \times d \boldsymbol { r } _ { 2 } \cdot ( \boldsymbol { r } _ { 1 } - \boldsymbol { r } _ { 2 } ) } { \| \boldsymbol { r } _ { 1 } - \boldsymbol { r } _ { 2 } \| ^ { 3 } }$$
    本方法将人体骨骼表示为5条串行链，计算交互角色对应肢体链之间的 GLI 值，通过约束 GLI 随时间平滑变化来避免穿透。采样更新规则为：
    $$\boldsymbol { x } _ { t - 1 } ^ { i } \longleftarrow \boldsymbol { x } _ { t - 1 } ^ { i } - \lambda _ { t } \nabla _ { \boldsymbol { x } _ { t } ^ { i } } ( L _ { G } ( \hat { \boldsymbol { x } } _ { 0 } ^ { i } , \hat { \boldsymbol { x } } _ { 0 } ^ { j } ) )$$
    当存在第三个非交互角色 $k$ 时，更新规则扩展为：
    $$x _ { t - 1 } ^ { i } \longleftarrow x _ { t - 1 } ^ { i } - \lambda _ { t } \nabla _ { x _ { t } ^ { i } } ( L _ { G } ( \hat { x } _ { 0 } ^ { i } , \hat { x } _ { 0 } ^ { j } ) + L _ { P } ( \hat { x } _ { 0 } ^ { i } , \hat { x } _ { 0 } ^ { k } ) )$$

### 3. 创新效果的关键证据

- **双人交互**：本方法相对于 InterGen 穿透深度减少 **76.53%**，相对于 FreeMotion 减少 **85.38%**（Table 1）。在近距离交互子集上，穿透深度相对 InterGen 减少 **77.52%**，接触点数减少 **74.61%**（Table 2）。
- **多人交互**：在3人配置下，本方法在所有指标上均优于 FreeMotion，且随人数增加优势更明显（Table 3）。
- **消融验证**：移除 Proxemics 和 GLI 损失后，穿透深度和接触点数大幅增加——3人时穿透增加 **42.94%**，4人时增加 **96.33%**（Table 4）。GLI 损失相比简单的包围盒重叠损失在近距交互子集上减少穿透的效果更优（Table 5）。

### 4. 方法局限

- 完全依赖现有双人模型，无法捕捉图中非直接连接节点之间的关系。
- 优化过程增加了计算开销，不适合实时应用。
- 在人数较多且图结构复杂时仍无法完全避免穿透。
- 需要用户手动指定图结构，对复杂场景可能需要专业知识。

## 整体框架

本文提出 **Graph-driven Interaction Sampling**，其核心思路是将多人交互运动生成重新表述为：在成对交互图（Pairwise Interaction Graph）的约束下，同时生成多个单人运动，每个人的运动以图中指定的邻居为条件。整个框架由两个紧密耦合的部分构成：**图驱动的多人采样方案** 和 **交互采样优化过程**。

### 图驱动的多人采样方案

多人交互被分解为一个图结构 $G = (V, E)$，其中每个节点 $v_i \in V$ 代表一个人物，每条有向边 $(i, j) \in E$ 表示人物 $i$ 的运动以人物 $j$ 的运动为条件。这一分解允许用户通过定义图的拓扑结构来控制哪些人物之间存在紧密的成对交互，图结构本身可以是**时间变化的**——同一人物在不同时间段可以以不同的人物为条件。

基于该图，多人运动的联合概率分布被建模为成对因子的乘积：

$$p(x^1, x^2, ..., x^n) = \frac{1}{Z} \prod_{(i,j) \in \text{edges}} \phi_{ij}(x_i, x_j)$$

其中 $\phi_{ij}$ 来自预训练的双人交互扩散模型（如 **InterGen** (Liang et al., IJCV 2024) 或 **in2IN** (Ruiz-Ponce et al., CVPR 2024)）。在采样时，框架并行运行 $n$ 个去噪过程，每个节点的运动生成以其在图中的邻居为条件。这避免了为不同人数重新训练模型，同时保持了交互的多样性和可控性。

### 交互采样优化过程

仅靠图结构条件采样无法完全避免人物间的穿透，尤其对于图中非直接连接的角色。为此，在扩散采样的每一步中引入两个图引导的损失函数，通过梯度下降对预测的干净样本 $\hat{x}_0$ 进行优化：

- **Proxemics Loss ($L_P$)**：惩罚图中**无连接关系**的角色对之间的包围盒重叠，防止非交互角色发生意外碰撞。
- **Gauss Linking Integral (GLI) Loss ($L_G$)**：监控图中**有连接关系**的交互角色对的骨架链扭结积分，通过约束 GLI 值随时间平滑变化来避免穿透。

对于双人交互，更新规则为：

$$\boldsymbol{x}_{t-1}^i \longleftarrow \boldsymbol{x}_{t-1}^i - \lambda_t \nabla_{\boldsymbol{x}_t^i} \left( L_G(\hat{\boldsymbol{x}}_0^i, \hat{\boldsymbol{x}}_0^j) \right)$$

当引入第三个非直接连接的角色 $k$ 时，更新规则扩展为同时考虑交互损失和空间隔离损失：

$$x_{t-1}^i \longleftarrow x_{t-1}^i - \lambda_t \nabla_{x_t^i} \left( L_G(\hat{x}_0^i, \hat{x}_0^j) + L_P(\hat{x}_0^i, \hat{x}_0^k) \right)$$

### 输入输出流

- **输入**：文本描述 / 动作标签，以及用户定义的成对交互图（可含时间变化信息）。
- **处理**：图结构驱动并行条件去噪采样，每一步通过双人扩散模型预测干净样本，并施加 Proxemics 和 GLI 损失进行梯度优化。
- **输出**：多人物的 3D 运动序列，各人物运动在空间和时间上协调，且穿透显著减少。

整个 pipeline 的模块关系可概括为：**图定义 → 并行条件采样 → 损失引导优化 → 多人运动序列**。该框架无需针对多人交互进行额外训练，完全依赖现有双人模型作为运动先验。

### 补充图表

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/002_Figure_2.jpg]]
*Figure 2: Examples of interaction graph for decomposing a multi-person interaction into coupled pairwise interactions*

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/001_Figure_1.jpg]]
*Figure 1: Examples of multi-person close interactions generated using the proposed Graph-driven Interaction Sampling. Different graph topologies were used to represent different kinds of interaction patterns. Note the Pairwise Interaction Graph illustrated at the bottom-right in each example, which lets the user control which characters are taking part in close pairwise interactions*

## 核心模块与公式推导

### 图驱动的多人采样框架

本方法的核心思想是将多人交互运动建模为**成对交互图（Pairwise Interaction Graph）**上的并行条件生成问题。给定 $n$ 个角色，用户定义一个图结构 $\mathcal{G} = (\mathcal{V}, \mathcal{E})$，其中节点 $\mathcal{V} = \{1, 2, \ldots, n\}$ 表示各角色，有向边 $(i, j) \in \mathcal{E}$ 表示角色 $i$ 的运动以角色 $j$ 的运动为条件。

基于此图结构，多人运动的联合概率分布被定义为成对因子的乘积形式：

$$p ( x ^ { 1 } , x ^ { 2 } , . . . , x ^ { n } ) = { \frac { 1 } { Z } } \prod _ { ( i , j ) \in \mathrm { e d g e s } } \phi _ { i  j } ( x _ { i } , x _ { j } )$$

其中 $\phi_{ij}(x_i, x_j)$ 来自预训练的双人交互扩散模型，$Z$ 为归一化常数。该因式分解将多人任务转化为同时运行 $n$ 个去噪过程，每个节点的去噪以其在图中的父节点运动为条件。图结构支持**时变定义**，即不同时间窗口可指定不同的条件依赖关系（见 Figure 3），从而灵活表达“角色1先与角色2交互，再与角色3交互”等复杂时序模式。

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/003_Figure_3.jpg]]
*Figure 3: An example of time-varying interaction graph with character 1 is conditioned on both characters 2 and 3*

### 交互采样优化

仅靠图分解无法保证交互质量，尤其是穿透问题。为此，在扩散采样的每一步，引入两个图引导的损失函数对预测的干净运动 $\hat{x}_0$ 进行梯度优化。

#### Proxemics 损失

Proxemics 损失针对图中**非直接相连**的角色对，惩罚其包围盒的重叠体积。对于非交互角色对 $(i, k)$，该损失定义为两者包围盒的交集体积，通过梯度下降迫使它们在空间上保持合理距离，避免非预期的碰撞。

#### Gauss Linking Integral (GLI) 损失

GLI 损失针对图中**直接相连**的交互角色对，用于减少穿透。GLI 是衡量两条空间曲线缠绕程度的拓扑不变量，其连续形式为：

$$G ( \gamma _ { 1 } , \gamma _ { 2 } ) = \frac { 1 } { 4 \pi } \int _ { \gamma _ { 1 } } \int _ { \gamma _ { 2 } } \frac { d \boldsymbol { r } _ { 1 } \times d \boldsymbol { r } _ { 2 } \cdot ( \boldsymbol { r } _ { 1 } - \boldsymbol { r } _ { 2 } ) } { \| \boldsymbol { r } _ { 1 } - \boldsymbol { r } _ { 2 } \| ^ { 3 } }$$

其中 $\gamma_1, \gamma_2$ 为两条有向空间曲线，$\boldsymbol{r}_1, \boldsymbol{r}_2$ 为曲线上点的位置向量。GLI 的符号和大小反映了曲线的缠绕方式与程度。

为应用于人体骨架，方法将每个角色的姿态表示为 5 条串行链（分别对应四肢和躯干，见 Figure 4d），对交互角色间的对应链对计算 GLI。GLI 被离散化为线段对的扭量求和：

$$GLI(S_1, S_2) = \sum_{i=1}^{m} \sum_{j=1}^{n} T_{i,j}$$

其中 $S_1, S_2$ 为两条骨架链，$T_{i,j}$ 为线段对 $(i, j)$ 的扭量，通过四面体顶点法向量解析计算：

$$T_{i,j} = \arcsin(n_a n_b) + \arcsin(n_b n_c) + \arcsin(n_c n_d) + \arcsin(n_d n_a)$$

#### 扩散后验采样更新

在每步去噪后，利用损失函数对当前噪声状态 $\boldsymbol{x}_t^i$ 进行梯度更新。对于双人交互场景，更新规则为：

$$\boldsymbol { x } _ { t - 1 } ^ { i } \longleftarrow \boldsymbol { x } _ { t - 1 } ^ { i } - \lambda _ { t } \nabla _ { \boldsymbol { x } _ { t } ^ { i } } ( L _ { G } ( \hat { \boldsymbol { x } } _ { 0 } ^ { i } , \hat { \boldsymbol { x } } _ { 0 } ^ { j } ) )$$

其中 $L_G$ 为 GLI 损失，$\lambda_t$ 为步长参数，$\hat{\boldsymbol{x}}_0^i$ 为从 $\boldsymbol{x}_t^i$ 预测的干净运动。

当存在第三个非交互角色 $k$ 时，更新规则同时纳入 GLI 损失和 Proxemics 损失：

$$x _ { t - 1 } ^ { i } \longleftarrow x _ { t - 1 } ^ { i } - \lambda _ { t } \nabla _ { x _ { t } ^ { i } } ( L _ { G } ( \hat { x } _ { 0 } ^ { i } , \hat { x } _ { 0 } ^ { j } ) + L _ { P } ( \hat { x } _ { 0 } ^ { i } , \hat { x } _ { 0 } ^ { k } ) )$$

其中 $L_P$ 为 Proxemics 损失。该框架的关键优势在于**无需重新训练扩散模型**——优化过程仅作用于采样阶段，双人先验模型保持冻结，从而保留了原有模型的运动多样性和生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/005_Figure_4.jpg]]
*Figure 4: (a)-(c) Examples of GLI values computed from different configurations of a pair of serial chains representing the body parts. (d) Representing a skeletal pose by 5 serial chains*

## 实验与分析

### 双人交互生成结果

我们在InterHuman测试集上将本方法与两个代表性基线进行了比较：双人交互生成模型**InterGen**（Liang et al., IJCV 2024）和多人运动生成模型**FreeMotion**（Fan et al., ECCV 2024）。如Table 1所示，本方法在保持与基线可比的运动质量（FID指标）的同时，显著降低了穿透深度：相对于InterGen减少**76.53%**（0.211 vs 0.899），相对于FreeMotion减少**85.38%**（0.211 vs 1.443）。这一结果表明，基于图引导的采样优化能够在不牺牲运动多样性的前提下，有效缓解双人交互中的穿透问题。

在近距离交互子集上（Table 2），本方法的优势更为突出：穿透深度较InterGen降低**77.52%**（0.525 vs 2.335），接触点数减少**74.61%**。这说明Proxemics损失和GLI损失对于处理紧密身体接触场景尤为有效，而这类场景正是现有方法失效的主要瓶颈。

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on a subset with mostly close interactions*

### 多人交互生成结果

我们将方法扩展至3至5人的交互生成，并与FreeMotion进行对比。如Table 3所示，在3人配置下，本方法在所有指标上均优于FreeMotion：Pair-FID从81.621降至**72.294**，穿透深度从5.567降至**1.515**。随着人数增加，本方法的优势更加明显——在4人和5人场景下，Pair-FID和穿透深度指标均保持显著领先。这验证了Pairwise Interaction Graph分解策略的有效性：通过将多人交互解耦为成对条件采样，我们能够利用双人先验生成高质量的多人运动，而无需针对多人数据进行额外训练。

定性结果（Figure 5）进一步佐证了定量发现。在"三人互殴"和"四人舞蹈"等复杂场景中，FreeMotion生成的运动会重复相似的动作模式并伴随严重穿透，而本方法生成的交互更加自然多样，身体接触合理且无显著穿透。

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative results from FreeMotion and our method. The prompt used in (a) and (b) is “Three person attack each other with their punch”. The text used for generating (c) and (d) is “They initiate a dance routine that involves swaying shoulders and arms”*

### 消融实验

为验证两个损失项的贡献，我们进行了消融实验（Table 4）。移除Proxemics损失和GLI损失后，穿透深度和接触点数大幅增加：3人时穿透增加**42.94%**，4人时增加**96.33%**。这一结果表明，仅靠图结构分解不足以消除穿透，优化损失是保证交互物理合理性的关键组件。

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/008_Table_4.jpg]]
*Table 4: Quantitative results from the ablation study*

针对GLI损失的单独消融（Table 5）表明，与基于包围盒重叠体积的简单接触损失相比，GLI损失在近距离交互子集上能更有效地减少穿透深度。这是因为GLI通过计算空间曲线的扭结积分，能够更精确地捕捉身体部位之间的缠绕程度，从而在梯度优化中提供更准确的信号来避免穿透。

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/010_Table_5.jpg]]
*Table 5: Ablation study of GLI loss*

### 失败模式与局限性

尽管本方法在穿透减少方面取得了显著进展，但仍存在以下失败模式：

1. **残余穿透**：在人数较多（5人以上）且图结构复杂时，仍无法完全消除穿透。这是因为优化过程仅作用于图中直接连接的节点对，非直接连接的角色之间可能发生意外重叠。

2. **图结构依赖性**：方法完全基于用户指定的Pairwise Interaction Graph，无法自动捕捉图中非直接连接节点之间的关系。当实际交互超出图定义的依赖结构时，生成质量会下降。

3. **计算开销**：在扩散采样过程中引入梯度优化增加了计算成本，可能不适合实时应用场景。

4. **图设计负担**：需要用户手动指定交互图结构，对于复杂多人场景可能需要专业知识。如何利用大语言模型自动生成合理的图结构和文本描述，是一个值得探索的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on the InterHuman test set. ± indicates the 95% confidence interval. Bold face indicates the best result*

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/009_Table_3.jpg]]
*Table 3: Quantitative comparisons on multi-person interactions with 3 to 5 characters*

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/015_Figure_8.jpg]]
*Figure 8: Qualitative results of 2-person interactions. The prompt used is “one person embraces the other person and dances with joy.”*

![[assets/figures/papers/paper_list_l1804_Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors/figures/011_Figure.jpg]]
*Figure: (a) 3-person fighting generated by FreeMotion (b) 3-person fighting generated by ours (c) 4-person dancing generated by FreeMotion (d) 4-person dancing generated by ours*

## 方法谱系与知识库定位

### 核心定位与问题瓶颈

本工作（Graph-driven Interaction Sampling）处于**多人交互运动生成**的交叉点，其核心瓶颈在于：多人交互数据集稀缺，导致直接训练多人模型不可行；而现有的双人交互模型（如 **InterGen**, Liang et al., IJCV 2024）无法直接扩展至可变人数场景。少数已有的多人生成方法（如 **FreeMotion**, Fan et al., ECCV 2024）虽然支持多人，但会产生重复动作和严重的穿透伪影。

本方法的核心洞察是：**将多人交互建模为一个成对交互图（Pairwise Interaction Graph）**，其中每个节点代表一个人，有向边表示条件依赖关系。这样即可将现有的双人扩散模型作为运动先验，通过并行条件采样生成多人运动，并通过基于图的额外损失来约束空间关系——整个过程无需重新训练模型，同时保持了交互的多样性和可控性。

### 与基线方法的关系

#### InterGen（Liang et al., IJCV 2024）

InterGen 是本方法所依赖的双人交互扩散模型骨干。它能够生成高质量的双人交互运动，但仅限于两人场景。本方法将其视为“运动先验”，通过图结构将其能力扩展至多人，而不修改其网络权重。在双人场景下，本方法在保持生成质量（FID）可比的前提下，将穿透深度降低了 **76.53%**（Table 1），表明图引导的采样优化有效弥补了原模型的物理合理性缺陷。

#### FreeMotion（Fan et al., ECCV 2024）

FreeMotion 是少数能够直接生成多人交互的方法之一，但其输出存在严重的穿透问题。在3人交互配置下，本方法的穿透深度（PeneBone）为 **1.515 m**，而 FreeMotion 为 **5.567 m**，降低了 **72.8%**；同时 Pair-FID 从 81.621 降至 72.294（Table 3）。随着人数增加，本方法的优势更为明显，表明图分解策略在复杂场景下具有更强的扩展性。

#### in2IN（Ruiz-Ponce et al., CVPR 2024）

in2IN 是另一种双人反应生成模型，可作为本方法的替代骨干。论文提及该方法可用于替换 InterGen，但未提供定量比较。这意味着本方法的图驱动采样框架具有**模型无关性**，可适配不同的双人扩散模型。

### 方法谱系中的位置

从技术路线看，本方法属于**扩散后验采样（Diffusion Posterior Sampling）**范式：利用预训练扩散模型作为先验，在采样过程中通过梯度引导引入额外的约束损失。这与利用物理模拟器、碰撞检测或判别器进行引导的方法属于同一家族，但本方法的创新在于：

1. **图结构引导**：将多人交互分解为图上的成对条件采样，而非同时生成所有人物；
2. **Gauss Linking Integral（GLI）损失**：引入拓扑不变量来度量身体部位的缠绕程度，比简单的包围盒重叠体积（接触损失）更能捕捉穿透的本质（Table 5 消融验证了GLI在近距交互子集上的优势）；
3. **Proxemics 损失**：专门惩罚图中非直接交互角色之间的空间重叠，这是现有方法未考虑的。

### 适用边界与局限

**适用场景**：
- 需要生成可变人数（2-5人）的交互运动，且希望利用现有双人模型；
- 交互模式可由图结构显式定义（如打斗、舞蹈、拥抱等）；
- 对物理合理性要求高，但可容忍少量残余穿透。

**不适用场景**：
- 需要捕捉图中非直接连接节点之间隐式关系的场景（方法本身无法建模这些高阶依赖）；
- 实时应用（优化过程增加了计算开销）；
- 需要自动推断交互图的场景（目前需用户手动指定图结构，对复杂场景可能需要专业知识）。

**已知局限**：
1. **无法完全消除穿透**：尤其在人数较多且图结构复杂时，残余穿透仍然存在；
2. **图结构依赖**：方法性能高度依赖用户提供的图结构是否合理；
3. **计算开销**：每次采样需进行梯度下降优化，增加了推理时间；
4. **非直接交互盲区**：图中未连接的节点之间可能发生意外交互，方法无法主动处理。

### 开放问题与未来方向

1. **可扩展性**：如何将方法扩展到包含更多人的复杂交互（如10人以上），同时保持计算效率？
2. **自动化图生成**：能否利用大语言模型（LLM）根据文本描述自动生成合理的图结构和时间变化模式？
3. **物理模拟集成**：引入物理模拟器作为后处理或联合优化，以进一步消除残余穿透和滑步问题；
4. **高阶关系建模**：如何处理非直接连接节点之间可能发生的意外交互（如三人同时接触的场景）？
5. **实时性能**：能否通过蒸馏或近似优化减少计算开销，使其适用于交互式应用？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Multi_Person_Interaction_Generation_from_Two_Person_Motion_Priors.pdf]]
