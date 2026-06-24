---
title: "Spectral Unions of Partial Deformable 3D Shapes"
type: paper
paper_level: A
venue: Eurographics
year: 2022
pdf_ref: paperPDFs/EUROGRAPHICS_2022/Spectral_Unions_of_Partial_Deformable_3D_Shapes.pdf
project_link: https://github.com/lucmos/spectral-unions
aliases:
- SUNU
- SUPD3S
tags:
- EUROGRAPHICS_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "学习一个基于Transformer的谱并集算子U_Θ，直接在谱域中根据两个部分谱生成并集谱，无需显式三维重建或匹配。"
primary_logic: "通过仅操作特征值序列，并利用可交换的Transformer架构和偏移表示，可以高效地预测部分形状并集的内在几何属性（谱），从而支持谱域的下游任务，同时对不同采样、离散化和未知对应具有鲁棒性。"
claims:
- "在已知身份的人体模型上，预测谱与真实谱之间的MSE低至11.14，MAE为2.09"
- "区域定位任务中，单身份训练模型的IoU最高可达99.28%，准确率99.61%"
- "形状检索任务中，使用预测谱的top-1准确率达到86.14%，与ShapeDNA的86.59%相比具有竞争力"
- "方法在重新网格化的形状上仍保持性能，表明对离散化鲁棒"
---

# Spectral Unions of Partial Deformable 3D Shapes

> [!tip] 核心洞察
> 通过仅操作特征值序列，并利用可交换的Transformer架构和偏移表示，可以高效地预测部分形状并集的内在几何属性（谱），从而支持谱域的下游任务，同时对不同采样、离散化和未知对应具有鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 部分可变形3D形状的谱并集 |
| 英文题名 | Spectral Unions of Partial Deformable 3D Shapes |
| 会议/期刊 | Eurographics 2022 |
| Links | [paper](https://arxiv.org/abs/2104.00514); [GitHub](https://github.com/lucmos/spectral-unions) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Spectral Union Network (U_Θ) |
| Dataset | Human bodies (TEST A, known man), unknown woman re-meshed), Human bodies (region localization, single identity training), 6 identities training) |

> [!tip] 效果简介
> - Human bodies (TEST A, known man) 上，MSE (eigenvalues) 为 11.14，对比 N/A (only proposed)，变化 N/A。
> - Human bodies (TEST A, unknown woman re-meshed) 上，MAE (eigenvalues) 为 5.23，对比 N/A，变化 N/A。
> - Human bodies (region localization, single identity training) 上，IoU / Accuracy 为 83.69–99.28% / 91.08–99.61%，对比 N/A，变化 N/A。

## 概述

### 1. 问题背景与瓶颈

在三维形状分析中，从多个部分观测重建完整几何是一项基础任务。传统方法依赖显式的点对点对应或几何对齐，这在非刚性变形和未知姿态下极为困难。本文聚焦一个更抽象但更具挑战性的问题：**在不计算任何对应关系或空间变换的前提下，能否仅从部分形状的谱（Laplacian特征值序列）预测其并集的谱？**

核心瓶颈在于：谱仅捕获形状的等距等价类，因此从部分谱推断并集谱是一个**病态问题**——多个不同的并集形状可能共享相同的部分谱（图3）。然而，作者指出这一模糊性可以通过**数据驱动的先验**来缓解：在特定形状类（如人体、马）内部，部分形状的并集方式并非完全任意，而是受该类形状的内在几何约束。

### 2. 核心方法定位

本文提出**谱并集网络（Spectral Union Network, $\mathcal{U}_\Theta$）**，这是一个基于Transformer的神经算子，直接在谱域中执行“并集”操作：

- **输入**：两个部分形状的截断拉普拉斯特征值序列（偏移表示）
- **输出**：预测的并集形状的特征值序列
- **关键设计**：通过可交换的Transformer架构实现输入顺序不变性，无需任何几何对应

方法的核心洞察是：通过仅操作特征值序列这一紧凑的谱表示，可以高效地预测部分形状并集的内在几何属性，同时对不同采样密度、网格连通性和未知对应具有鲁棒性。这一定位使该方法区别于传统的显式几何重建管线（图1）。

### 3. 方法谱系与知识库定位

该方法处于**谱几何处理**与**学习式形状分析**的交叉点：

- **谱形状分析传统**：继承了“谱作为形状指纹”的思想（如**ShapeDNA**，Reuter et al., Computer-Aided Design 2006），但将谱从描述符提升为可操作的表示空间，直接在其中进行几何推理。
- **形状补全与融合**：区别于需要显式对齐、融合和重建的几何方法，本文的谱域操作完全绕过三维坐标，避免了对应性难题。
- **神经算子**：将并集建模为从谱到谱的映射，通过学习数据先验来正则化病态问题，这与物理仿真中的神经算子有方法论上的共鸣。

### 4. 主要结果概览

实验在人体、马、飞机等多个类别上验证了方法的有效性：

- **谱预测精度**：在已知身份的人体模型上，预测谱与真实谱之间的MSE低至11.14，MAE为2.09（表1）；在未知身份的重新网格化形状上，MAE为5.23，表明对离散化具有鲁棒性。
- **区域定位**：以预测谱为输入，单身份训练的模型可达到最高99.28%的IoU和99.61%的准确率（表2）；跨6个身份训练后性能更为稳定（表3）。
- **形状检索**：使用预测谱的top-1准确率达到86.14%，与直接在完整形状上计算的ShapeDNA（86.59%）相比仅差0.45个百分点（表4），证明了预测谱在下游任务中的实用性。
- **泛化能力**：方法在重新网格化形状、不同数据集甚至点云输入上均保持性能（图6-8，图15-18），展现出对离散化方式和数据模态的鲁棒性。

### 5. 局限与开放问题

尽管结果令人鼓舞，该方法仍存在若干局限：预测的特征值序列缺乏是真实拉普拉斯谱的数学保证；迭代式处理多于两个部分形状时误差会逐步累积；对分布外并集模式的泛化能力有限；尚未在未处理的自然部分扫描数据上进行测试。开放问题包括：如何保证预测谱的可实现性（即存在一个流形以该序列为谱），以及如何处理谱并集的固有模糊性（如对称部分导致的多个有效解）。

## 背景与动机

三维形状分析的核心挑战之一是处理不完整的几何数据。在许多实际场景中，我们获得的并非完整的物体模型，而是多个部分扫描的集合——例如从不同视角捕获的深度图、遮挡下的激光雷达点云，或经过分割的CAD部件。这些部分形状各自携带有限的几何信息，但它们的并集可能覆盖一个完整物体的内在结构。如何从这些碎片化的观测中推断出完整形状的全局属性，构成了一个基础性问题。

**现有方法的瓶颈。** 传统上，从部分形状恢复完整几何信息的路径依赖于显式的对应关系计算或几何配准。这类方法需要建立部分形状之间、或部分形状与某个模板之间的点对点映射，然后通过融合、变形或重建来获得完整形状。然而，这一范式面临两个根本性困难：其一，当部分形状之间缺乏足够的重叠区域或纹理特征时，可靠的对应关系难以建立；其二，对于可变形物体（如人体、动物），不同部分可能处于不同的姿态，使得刚性配准方法失效。即便使用功能映射等更灵活的谱域对应方法，仍然需要部分形状之间共享某种结构信息。

**谱表示的机遇与挑战。** 拉普拉斯-贝尔特拉米算子的谱（特征值序列）提供了一种规避上述困难的表示形式。根据谱几何理论，特征值序列是等距变换的不变量——它不依赖于具体的嵌入姿态、网格采样密度或三角剖分方式，而是刻画了形状的内在度量结构。这一性质使得谱表示天然适合处理可变形形状：两个处于不同姿态的同一物体具有相同的特征值序列。然而，谱表示也引入了新的歧义性：特征值仅捕获等距等价类，因此多个几何上不同但等距的形状共享相同的谱（等谱性）。对于部分形状的并集问题，这种歧义性进一步放大：每个部分可能与其对称版本等谱，导致并集存在多个有效解（见Figure 3）。此外，在未知对应关系和完整几何信息的情况下，从部分形状的谱预测其并集的谱，本质上是一个病态问题——仅靠数学推导无法确定唯一解。

**数据驱动的突破口。** 尽管上述问题在纯几何框架下是病态的，但现实世界中的形状并非均匀分布在所有可能的等距类上。特定语义类别（如人体、四足动物、人造物）的形状遵循特定的结构先验，这些先验可以通过数据学习获得。本文的核心动机正是利用这一观察：我们提出学习一个神经算子，直接从两个部分形状的截断特征值序列预测其并集的特征值序列，无需显式的三维重建、对应关系计算或几何配准。这一思路将问题从几何推理转化为谱域上的序列到序列映射，通过数据先验来弥补信息的不足，同时保留谱表示对离散化和姿态变化的固有鲁棒性。

## 核心创新

本文的核心创新在于将部分形状的并集问题从三维几何域完全迁移至谱域，提出了**谱并集（Spectral Union）**这一新范式，并设计了相应的神经算子 $\mathcal{U}_\Theta$ 来实现。其关键突破体现在以下三个维度的表示与机制变革上。

### 从几何表示到谱表示的输入变革

传统方法处理部分形状融合时，输入通常是三维点云或网格，需要在欧氏空间中显式地对齐、匹配和融合几何。然而，部分可变形形状之间的对应关系求解本身就是一个极具挑战的病态问题。本文的关键洞察是：**拉普拉斯特征值序列构成了整个等距类的紧凑描述符**，它不依赖于具体的嵌入姿态、网格连通性或顶点采样密度。

因此，方法将输入从三维几何彻底切换为截断的拉普拉斯特征值序列（偏移表示），即对于每个部分形状 $\mathcal{M}$，仅取其前 $k$ 个满足狄利克雷边界条件的特征值：

$$\Delta \Phi_i(x) = \lambda_i \Phi_i(x) \quad x \in \operatorname{int}(\mathcal{M}), \quad \phi_i(x) = 0 \quad x \in \partial \mathcal{M}$$

并将特征值转换为相邻差值的形式 $\mathrm{off}(\lambda_i) = \lambda_i - \lambda_{i-1}$，以保证预测序列的非递减性并稳定训练。这一输入变革使得方法天然免疫于网格重剖分、顶点密度变化和未知对应关系带来的干扰——Table 1 和 Figure 6 的实验表明，即使在移除30%顶点重新网格化后，预测性能仍保持稳定。

### 谱域神经并集算子替代显式几何融合

在并集操作的实现上，传统方法需要经过显式的几何对齐、融合和重建流水线。本文则直接学习一个谱域神经算子 $\mathcal{U}_\Theta$，其核心功能是：给定两个部分形状的特征值序列，直接输出它们并集的预测特征值序列：

$$\pmb{\lambda}(\mathcal{M}_1 \cup \mathcal{M}_2) = \mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2))$$

这一算子的架构设计精巧地解决了两个关键问题。首先，通过**可交换的Transformer架构**（Figure 4）保证输入顺序不变性：单一Transformer $\mathbf{T}_A$ 分别编码两个输入谱后求和，得到一个交换不变的并集隐含表示。其次，通过第二个Transformer $\mathbf{T}_B$ 结合线性降维层 $\rho$ 将隐含表示解码为预测的特征值序列。整个网络维度为32，$\mathbf{T}_A$ 具有8个注意力头和6层，$\mathbf{T}_B$ 具有8个注意力头和3层。

对于多于两个部分形状的场景，该方法通过成对谱并集的**可结合组合**实现：

$$\lambda(\mathcal{M}_1 \cup \mathcal{M}_2 \cup \dotsb \cup \mathcal{M}_m) = \mathcal{U}_\Theta(\dotsb(\mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2)), \dotsb), \pmb{\lambda}(\mathcal{M}_m))$$

这一设计避免了为不同数量的输入部分重新训练模型，但消融实验（Appendix A）也揭示了其局限性：迭代式谱并集会导致误差逐步累积，更深的迭代更加困难。

### 完全免除对应性需求

对应性需求是传统几何融合方法的核心瓶颈。无论是点对点匹配还是功能映射（functional map），都需要在部分形状之间建立显式的对应关系，这在部分重叠、不同姿态和未知连通性的场景下极易失效。本文的方法**完全不需要计算输入形状之间的任何对应或变换**——这一特性源于谱表示的内在属性：特征值序列仅编码形状的内蕴几何，而与外部嵌入无关。

这一变革使得方法能够处理 Figure 3 所示的歧义情形（如对称部分导致的多个有效并集解），因为网络可以通过数据先验学习到合理的解，而非依赖于可能不存在的唯一几何对应。实验证据（Table 1）表明，在已知身份的人体模型上，预测谱与真实谱之间的MSE低至11.14、MAE为2.09，验证了这一无对应范式的有效性。

### 方法谱系定位

在谱形状分析的方法谱系中，本文的工作处于一个独特的位置。与 **ShapeDNA**（Reuter et al., Computer-Aided Design 2006）将谱用作形状检索的描述符不同，本文的方法直接操作并生成谱，将其从被动描述符提升为主动计算对象。与 **Isospectralization / MRC*19**（Marin et al., 3DV 2019）从谱恢复三维形状的逆向问题不同，本文关注的是谱域内的正向并集运算，且无需经过显式的几何重建即可支持下游任务（如区域定位、形状检索）。这种“在谱域中计算、在谱域中应用”的范式，为谱方法在三维视觉中的应用开辟了新的可能性。

## 整体框架

本文提出一种名为**谱并集网络（Spectral Union Network）**的学习框架，其核心目标是：给定两个部分可变形三维形状，仅以各自的截断拉普拉斯特征值序列为输入，直接预测二者并集的谱，全程无需计算形状间的对应关系或几何变换。该框架将“部分形状的并集”这一几何操作转化为谱域上的神经算子学习问题。

### 问题形式化与输入输出

设 $\mathcal{M}_1$ 和 $\mathcal{M}_2$ 为两个部分形状，它们来自某一完整形状的不同局部区域。对每个部分形状，首先计算其拉普拉斯-贝尔特拉米算子的特征分解：

$$\Delta \Phi_i(x) = \lambda_i \Phi_i(x) \quad x \in \operatorname{int}(\mathcal{M})$$

并施加齐次狄利克雷边界条件 $\phi_i(x) = 0 \; (x \in \partial \mathcal{M})$。取前 $k$ 个特征值构成截断谱向量：

$$\pmb{\lambda}(\mathcal{M}) = (\lambda_1, \ldots, \lambda_k)$$

框架的输入即为两个部分形状的截断谱 $\pmb{\lambda}(\mathcal{M}_1)$ 和 $\pmb{\lambda}(\mathcal{M}_2)$，输出为并集形状的预测谱 $\tilde{\pmb{\lambda}}(\mathcal{M}_1 \cup \mathcal{M}_2)$。整个映射由一个可学习的谱并集算子 $\mathcal{U}_\Theta$ 实现：

$$\mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2)) = \tilde{\pmb{\lambda}}(\mathcal{M}_1 \cup \mathcal{M}_2)$$

当需要处理多于两个部分形状时，框架通过成对谱并集的可结合组合实现：

$$\lambda(\mathcal{M}_1 \cup \cdots \cup \mathcal{M}_m) = \mathcal{U}_\Theta(\cdots(\mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2)), \cdots), \pmb{\lambda}(\mathcal{M}_m))$$

### Pipeline 模块与数据流

整个 pipeline 由以下四个核心模块串联构成（架构总览见 Figure 4，详细架构见 Figure 19）：

1. **拉普拉斯谱计算（预处理）**：对输入的原始部分网格或点云进行拉普拉斯特征分解，得到长度为 $k$ 的特征值序列。为稳定训练并保证预测序列的非递减性，将特征值转换为相邻差值的**偏移表示** $\mathrm{off}(\lambda_i) = \lambda_i - \lambda_{i-1}$。

2. **特征嵌入模块 $E$**：将每个偏移值映射到高维空间（维度 32），融合了可学习的位置编码和缩放后的数值信息：
   $$\mathrm{off}(\lambda_i) \mapsto \left( \vec{\Theta}_a^i, \quad \mathrm{off}(\lambda_i) \vec{\Theta}_b, \quad \mathrm{off}(\lambda_i) \right)$$

3. **可交换 Transformer $T_A$**：两个部分形状的嵌入序列分别通过**同一个** Transformer 编码器（8 头，6 层），得到各自的隐含表示后**逐元素求和**，从而获得与输入顺序无关的可交换并集表示。这是框架无需对应关系的核心设计——无论两个部分以何种顺序输入，求和操作保证了输出的置换不变性。

4. **解码器 $T_B + \rho$**：第二个 Transformer（8 头，3 层）将并集隐含表示解码为高维特征，再通过线性降维层 $\rho$（32 → 1）将其映射回标量偏移值，最终通过偏移的逆操作还原为预测的特征值序列 $\tilde{\pmb{\lambda}}(\mathcal{M}_1 \cup \mathcal{M}_2)$。

### 下游任务扩展

预测的并集谱可直接作为多种谱域下游任务的输入，无需显式三维重建：
- **形状重建**：将预测谱输入现有的“从谱恢复形状”方法（如 **Isospectralization / MRC\*19**，Marin et al., 3DV 2019）即可重建出并集形状（Figure 5, Figure 11）。
- **区域定位**：在谱并集网络后串联一个简单 MLP（Figure 20），以预测谱为输入，输出模板网格上的指示函数，标记部分形状的并集区域（Figure 6–8）。
- **形状检索**：直接将预测谱作为 **ShapeDNA**（Reuter et al., Computer-Aided Design 2006）等谱描述子的输入进行检索。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/008_Figure_5.jpg]]
*Figure 5: Given two partial shapes as input, we compare the reconstruction obtained by running the method of [MRC*19] only on a partial input (the green shape), yielding the fourth shape, with the reconstruction obtained from our predicted full spectrum, yielding the last shape*

### 关键设计权衡

框架的核心取舍在于：放弃显式的三维几何表示（点云/网格），转而操作等距不变的谱表示。这带来了三个优势——（1）完全规避了点对点对应问题；（2）天然对网格离散化、采样密度鲁棒（Table 2, Table 3, Figure 6）；（3）可交换架构保证了输入顺序无关性。代价则是预测谱缺乏是真实拉普拉斯谱的数学保证，且迭代式多部分并集会导致误差累积（Appendix A）。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/020_Figure.jpg]]
*Figure: 1Figure 11: Comparison of the reconstruction obtained by running the state-of-the-art method of [MRC*19] on the green shape, yielding the fourth shape, and the reconstruction obtained from our predicted full spectrum, yielding the last shape*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/001_Figure_1.jpg]]
*Figure 1: Given a collection of partial deformable shapes $\{ \mathcal { M } _ { 1 } , \mathcal { M } _ { 2 } , \mathcal { M } _ { 3 } \}$ as input, our method predicts the Laplacian eigenvalues of their union without first having to compute a correspondence or a transformation between the input shapes. The resulting eigenvalues (top right plots, colors correspond to each surface) can be used to reconstruct the final shape if needed, up to isometry/pose (bottom right). In this example, the input shapes have different poses, varying overlap, and different mesh connectivity

## 核心模块与公式推导

### 问题形式化：谱并集算子

本方法的核心思想是将部分形状并集的几何推理从三维欧氏空间完全迁移到谱域。给定两个部分形状 $\mathcal{M}_1$ 和 $\mathcal{M}_2$，其拉普拉斯-贝尔特拉米算子的特征分解满足：

$$\Delta \Phi_i(x) = \lambda_i \Phi_i(x) \qquad x \in \operatorname{int}(\mathcal{M})$$

并配合齐次狄利克雷边界条件 $\phi_i(x) = 0 \ (x \in \partial \mathcal{M})$。每个形状被映射为其截断的前 $k$ 个特征值构成的向量：

$$\pmb{\lambda} : \mathcal{M} \mapsto (\lambda_1, \ldots, \lambda_k)$$

谱并集问题的目标是学习一个算子 $\mathcal{U}_\Theta$，使其直接从两个部分谱预测并集谱，完全绕开显式的点对点对应或几何对齐：

$$\pmb{\lambda}(\mathcal{M}_1 \cup \mathcal{M}_2) = \mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2))$$

对于多于两个部分形状的情形，该算子通过成对组合实现可结合性：

$$\lambda(\mathcal{M}_1 \cup \mathcal{M}_2 \cup \dotsb \cup \mathcal{M}_m) = \mathcal{U}_\Theta(\dotsb(\mathcal{U}_\Theta(\pmb{\lambda}(\mathcal{M}_1), \pmb{\lambda}(\mathcal{M}_2)), \dotsb), \pmb{\lambda}(\mathcal{M}_m))$$

这一形式化将并集操作从“需要对应关系的几何融合”转变为“仅依赖特征值序列的谱域映射”，是方法的核心创新。

### 偏移表示：保证非递减性与训练稳定性

直接预测原始特征值序列存在一个关键约束：拉普拉斯特征值天然满足 $\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_k$。若网络直接输出原始值，难以保证这一单调性。为此，方法引入**偏移表示**（offset representation），将特征值序列转换为相邻差值：

$$\mathrm{off}(\lambda_i) = \lambda_i - \lambda_{i-1}$$

其中约定 $\lambda_0 = 0$。由于所有偏移量非负，网络只需输出非负值即可自动保证预测序列的非递减性。这一简单的表示变换同时起到了稳定训练的作用——将无界的特征值范围转化为更易学习的局部增量模式。

### 特征嵌入模块 E

嵌入模块 $E$ 将每个偏移量映射到高维表示空间，融合了位置信息和数值信息。具体映射形式为：

$$\mathrm{off}(\lambda_i) \mapsto \left( \vec{\Theta}_a^i, \quad \mathrm{off}(\lambda_i) \vec{\Theta}_b, \quad \mathrm{off}(\lambda_i) \right)$$

其中 $\vec{\Theta}_a^i$ 是第 $i$ 个特征值位置的可学习位置编码，$\vec{\Theta}_b$ 是用于缩放数值的可学习向量。该嵌入同时编码了“第几个特征值”（通过位置编码）和“该特征值的偏移量大小”（通过缩放与原始值），为后续 Transformer 处理提供了结构化的输入表示。

### 可交换 Transformer T_A：实现输入顺序无关性

谱并集算子必须满足交换律：$\mathcal{U}_\Theta(\pmb{\lambda}_1, \pmb{\lambda}_2) = \mathcal{U}_\Theta(\pmb{\lambda}_2, \pmb{\lambda}_1)$。为获得这一性质，架构采用**单一 Transformer T_A** 分别处理两个嵌入序列，然后将变换后的表示逐元素求和，得到一个与输入顺序无关的并集隐含表示。这种设计避免了双分支网络需要显式对称化损失或数据增强的复杂性，天然保证了交换不变性。

T_A 的具体配置为：8 个注意力头、6 层，所有表示的维度为 32。

### 解码器 T_B + ρ：从隐含表示到预测特征值

可交换隐含表示随后被送入第二个 Transformer T_B（8 头、3 层），其任务是将并集的隐含编码解码为结构化的序列表示。T_B 的输出再通过一个线性降维层 $\rho$，将 32 维表示压缩为标量预测值，最终得到预测的偏移序列。将偏移序列累积求和即得到预测的特征值序列 $\tilde{\pmb{\Lambda}}_{\mathcal{M}_1 \cup \mathcal{M}_2}$。

整个流水线可概括为：**E（嵌入）→ T_A（可交换编码+求和）→ T_B（解码）→ ρ（降维）→ 累积求和（还原特征值）**。详细的架构图见 Figure 4 和 Figure 19。

### 训练损失与加权策略

网络使用预测特征值与真实特征值之间的均方误差（MSE）作为训练损失。论文指出，尝试根据特征值线性增长幅度对损失进行加权惩罚（即对较大特征值赋予更高权重）**并未带来显著改进**——这一消融发现表明，简单的均匀加权 MSE 已足以有效训练谱并集算子。

## 实验与分析

### 核心实验设置

本文在三个任务维度上验证谱并集算子 $\mathcal{U}_\Theta$ 的有效性：**特征值预测精度**、**区域定位**和**形状检索**。实验覆盖已知/未知身份、重网格化、不同数据集和点云输入等条件，以系统评估方法的泛化性和鲁棒性。

网络架构配置如第4节所述：表示维度为32，Transformer $\mathbf{T}_A$ 使用8头注意力、6层，$\mathbf{T}_B$ 使用8头注意力、3层，线性降维层 $\rho$ 将32维降至1维输出。输入为截断的 $k$ 个特征值的偏移表示，输出为并集谱的预测值。

### 特征值预测精度

Table 1 报告了不同实验设置下预测特征值与真实值之间的误差。在已知身份的人体模型（TEST A, known man）上，模型取得了 **MSE = 11.14，MAE = 2.09** 的优异结果。当测试对象为训练集中**未出现的女性身份**时，MAE 升至 4.34；若进一步对该未知身份进行**重网格化**（移除30%顶点后重新计算谱），MAE 为 5.23，MSE 为 62.33。这一性能保持表明方法对离散化变化具有较好的鲁棒性（confidence 0.9）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/009_Table_1.jpg]]
*Table 1: Error between the predicted and ground truth eigenvalues in different experimental settings. In each row, “known” denotes an identity included in the training set, “unknown” one not included, and “re-meshed” indicates that the shapes were re-meshed by removing 30% of their vertices before computing their spectrum*

对于训练集中**未出现的男性身份**，MAE 为 2.92，显著优于未知女性身份的结果，暗示训练数据的身份分布可能影响泛化性能。在更困难的 **TEST B** 设置（部分形状仅覆盖完整形状的子区域）中，误差整体上升，但仍保持在可用范围内。

### 区域定位任务

区域定位任务的目标是：给定两个部分形状的特征值，预测它们在固定模板上的并集指示函数。该任务通过在谱并集网络后级联一个简单 MLP 实现（Section 6.2）。

**单身份训练**（Table 2）：仅使用单个人体身份训练时，模型展现出令人惊讶的泛化能力。在已知身份上，IoU 最高达 **99.28%**，准确率 **99.61%**；在未知身份上，IoU 范围为 83.69%–97.40%，准确率为 91.08%–99.10%。即使在**重网格化**的未知身份上，IoU 仍可达 83.69%，准确率 91.08%，进一步验证了对离散化的鲁棒性。

**六身份训练**（Table 3）：当使用六个不同身份训练时，性能显著提升。在未知身份上，IoU 达到 90.85%–98.24%，准确率 97.63%–99.14%，说明增加训练身份的多样性有助于提升泛化能力。

**跨数据集泛化**（Figure 7）：模型在训练中未见过的数据集上仍能正确定位区域，表明学习到的谱并集映射具有一定的数据集无关性。

**点云输入**（Figure 8）：即使输入部分形状以点云形式给出（计算其拉普拉斯谱后输入网络），模型仍能正确预测区域定位，展示了方法对输入表示形式的灵活性。

### 形状检索任务

Table 4 在 SHREC'17 基准上对比了使用预测谱与原始 ShapeDNA 谱的形状检索性能。使用预测谱的 **top-1 准确率为 86.14%**，与直接在完整形状上计算谱的 ShapeDNA（86.59%）相比仅差 0.45%，表明预测谱在保持形状判别性方面具有竞争力。这一结果尤为值得注意，因为预测谱仅来自部分形状的信息，却几乎达到了完整形状谱的检索性能。

### 几何重建验证

Figure 2 和 Figure 5 从定性角度验证了预测谱的几何保真度。使用预测谱通过 [MRC\*19] 方法重建的三维形状与使用真实谱重建的形状（白色参考）对比，误差以热力图编码。Figure 5 进一步对比了仅使用单个部分谱重建的结果（第四个形状）与使用预测完整谱重建的结果（最后一个形状），直观展示了谱并集对恢复完整几何的必要性。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/018_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/026_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/027_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/029_Figure.jpg]]

### 消融与失败模式

**损失函数设计**：在训练损失中引入与特征值线性增长成正比的惩罚项并未带来显著改进（Section 4），说明标准均方误差已足够引导网络学习谱并集映射。

**迭代式谱并集的误差累积**：当通过成对组合方式处理超过两个部分形状时，预测误差会在每次迭代中逐步放大（Appendix A）。更深层次的迭代并集更加困难，这是方法的一个内在局限。Figure 9 和 Figure 12 展示了可结合性的定性示例，但定量结果表明精度随迭代次数递减。

**跨类泛化有限**：模型的训练和评估主要限于同一语义类（如人体、马），虽然 Figure 16 展示了在马类上训练的模型对骆驼的部分泛化能力，但整体跨类泛化性能未经充分验证。

**谱的可实现性缺乏保证**：预测的特征值序列没有数学保证其对应某个真实流形的拉普拉斯谱，这是谱域方法的根本性局限。

### 关键图表结论总结

- **Table 1**：在已知身份上特征值预测 MSE 低至 11.14，重网格化后性能保持，证明方法对离散化鲁棒。
- **Table 2 & Table 3**：区域定位 IoU 最高达 99.28%，多身份训练显著提升泛化能力。
- **Table 4**：预测谱的形状检索准确率与完整谱的 ShapeDNA 几乎持平（86.14% vs 86.59%）。
- **Figure 5 & Figure 11**：预测谱能有效恢复完整几何，而仅使用部分谱的重建结果明显残缺。
- **Figure 9 & Figure 12**：成对谱并集可通过可结合性扩展至多部分形状，但存在误差累积问题。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/011_Table_2.jpg]]
*Table 2: Intersection over union (IoU) and accuracy in the region localization task, in different experimental settings. Model trained on a single identity, to show generalization*

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/010_Figure_6.jpg]]
*Figure 6: Region localization task, under the effect of different mesh connectivity. Given the eigenvalues of two partial shapes, we correctly predict an indicator function that represents the union of the two over a fixed template*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/025_Figure_17.jpg]]
*Figure 17: Region localization on aereoplanes. The model is trained and tested on point clouds*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2104_00514/figures/028_Figure_18.jpg]]
*Figure 18: Region localization on headphones, trained and tested on point clouds. In the examples on the right column, despite significant changes in the geometry of the partialities, the model localizes the same correct region*

## 方法谱系与知识库定位

### 1. 问题定位：谱域中的部分形状并集

本研究引入了一个此前未被显式形式化的新问题——**部分可变形3D形状的谱并集**（spectral unions of partial deformable 3D shapes）。核心任务是：给定两个部分形状的截断拉普拉斯特征值序列，直接预测其并集形状的特征值序列，而无需计算输入形状之间的对应关系或几何变换。

该问题的根本瓶颈在于其**病态性**（ill-posedness）：从部分形状的谱推断并集谱在数学上存在固有的歧义性。如图3所示，谱仅捕获等距等价类，因此存在多个有效解——当两个部分等距时，并集解在内在几何意义上是等价的；而当每个部分与其对称版本等谱（isospectral）时，两个部分的谱并集可能对应多达三种不同的有效解。论文通过引入数据先验（data prior）来缓解这一病态性，使模型学会从训练分布中选取最合理的解。

### 2. 与基线工作的关系

#### 2.1 谱形状检索基线：ShapeDNA

在形状检索任务（Section 6.3, Table 4）中，论文将所提方法与经典的谱形状描述子 **ShapeDNA**（Reuter et al., Computer-Aided Design 2006）进行了对比。ShapeDNA直接使用完整形状的特征值序列作为形状签名进行检索，而本文方法则从部分形状的谱出发，先预测并集谱，再将预测谱用于检索。

在SHREC'17基准上，使用预测谱的top-1准确率达到86.14%，与ShapeDNA在完整形状谱上的86.59%相比仅差0.45个百分点。这一结果表明：**谱并集算子预测的特征值序列在形状判别力上已接近真实完整谱**，验证了谱域操作在下游任务中的可行性。

#### 2.2 从谱恢复形状的基线：MRC*19

论文在几何重建应用中（Section 6.1）使用了 **Isospectralization / MRC\*19**（Marin et al., 3DV 2019）作为下游重建模块。MRC\*19是一个从拉普拉斯谱恢复三维形状的方法，论文将其作为“黑盒”工具来验证预测谱的几何保真度。

关键对比出现在Figure 5和Figure 11中：若仅将单个部分形状的谱输入MRC\*19进行重建，得到的形状明显残缺或不正确；而使用本文预测的并集谱进行重建，则能恢复出接近完整形状的几何。这一对比直接证明了**谱并集算子成功编码了部分形状组合后的全局内在几何信息**。

#### 2.3 与显式几何融合方法的根本差异

传统处理部分形状并集的方法通常依赖以下管线：建立点对点对应 → 计算刚体或非刚体变换 → 在三维空间中对齐和融合几何 → 处理重叠和缝隙。这类方法面临三个核心困难：
- **对应性需求**：需要可靠的特征匹配或功能映射（functional maps），在部分重叠、大变形或不同离散化下容易失效。
- **几何表示的敏感性**：对网格分辨率、三角剖分、采样密度敏感。
- **计算复杂度**：显式几何操作通常代价高昂。

本文方法通过**完全迁移到谱域**绕开了上述所有困难：
- **输入表示**：从三维点云/网格切换为截断拉普拉斯特征值序列（偏移表示），后者是等距不变的紧凑描述子。
- **并集操作**：从显式几何对齐、融合、重建切换为谱域神经算子 $\mathcal{U}_\Theta$ 直接预测并集谱。
- **对应性需求**：完全不需要计算对应，仅依赖特征值序列的统计规律。

### 3. 方法适用的边界与条件

#### 3.1 适用前提

- **部分形状覆盖并集**：论文主要考虑部分形状的并集完全覆盖完整形状的简单情形（Figure 2）。这是方法有效性的基本假设。
- **同一语义类内的等距变形**：训练和测试主要在人体、马等同一语义类上进行，变形限于近似等距（isometric）范畴。
- **截断谱长度k固定**：网络输入和输出均为固定长度k的特征值序列，k的选择影响信息容量和计算效率。

#### 3.2 已验证的鲁棒性边界

- **离散化鲁棒性**：方法在重新网格化（移除30%顶点）的形状上仍保持性能（Tables 2, 3和Figure 6），表明对三角剖分和顶点密度不敏感。
- **未知身份泛化**：在已知身份上训练的模型可泛化到未知身份（Table 1中unknown woman），但误差有所上升（MSE从11.14升至62.33）。
- **跨数据集泛化**：Figure 7展示了在训练集之外的dataset上的区域定位结果，模型仍能合理预测。
- **点云输入**：Figure 8和Figure 17-18展示了从部分点云的谱出发进行区域定位的结果，方法对点云离散化同样适用。

#### 3.3 已知局限

1. **缺乏谱可实现性的数学保证**：预测的特征值序列未必对应某个真实流形的拉普拉斯谱，即不存在理论保证使得 $\exists \mathcal{M}: \lambda(\mathcal{M}) = \tilde{\lambda}$。

2. **迭代并集的误差累积**：当通过成对谱并集的可结合组合（associative composition, Eq. 5）处理多于两个部分形状时，每一步的预测误差会被放大，使得深层迭代更加困难（Appendix A）。

3. **区域定位的分布外泛化有限**：区域定位模型对训练中未见过的并集部分形状组合的泛化能力有限。

4. **未在自然部分扫描上验证**：方法未在未处理的自然部分扫描数据（如单视角深度图、遮挡扫描）上进行测试，对真实传感器数据的鲁棒性未知。

5. **跨类泛化有限**：谱并集模型的训练和评估主要限于同一语义类（人体、马）。Figure 16展示了在马类上训练的模型对骆驼的部分泛化能力，但系统性跨类评估缺失。

### 4. 开放问题

1. **谱可实现性保证**：能否从数学上约束网络输出，或设计后处理投影步骤，以确保预测的特征值序列对应某个真实流形？

2. **多部分并集的精度保持**：如何设计非迭代的、原生支持多输入部分的谱并集算子，以避免成对组合带来的误差累积？

3. **非等距变形的扩展**：方法能否扩展到非等距但保持形状类别的变形（如不同体型的动物），这需要谱表示捕获更丰富的几何变化。

4. **谱并集歧义性的显式建模**：如何让模型显式地表示并利用谱并集的多解性（如对称部分导致的歧义），而非仅依赖数据先验隐式选择？

5. **与谱域其他算子的组合**：谱并集算子能否与功能映射（functional maps）、谱距离（spectral distances）等其他谱算子无缝组合，以支持更复杂的几何处理管线？

6. **大规模形状集合上的可扩展性**：方法在更大规模、更多样化的形状集合上的训练效率和泛化能力如何？

## 原文 PDF

![[paperPDFs/EUROGRAPHICS_2022/Spectral_Unions_of_Partial_Deformable_3D_Shapes.pdf]]
