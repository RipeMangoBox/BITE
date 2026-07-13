---
title: "SeeGroup: Multi-Layer Depth Estimation of Transparent Surfaces via Self-Determined Grouping"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SeeGroup_Multi_Layer_Depth_Estimation_of_Transparent_Surfaces_via_Self_Determined_Grouping.pdf
project_link: null
code_link: null
aliases:
- SeeGroup
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过置换不变损失和递归分解模块，让模型自确定跨像素的深度层分组方式（而非强制预排序），从而学习更连贯、更锐利的多层深度图。
primary_logic: 将每个像素的多层深度建模为关于深度的强度函数（max-mixture of Laplace），利用该表示的置换不变性，使模型能够自确定深度层的分组，避免了预排序分组带来的不规则结构，同时强度函数天然编码不确定性，有利于处理透明区域的弱视觉证据。
claims:
- 在LayeredDepth真实场景基准上，SeeGroup将四元组相对深度准确率（Q, All）从61.34%大幅提升至70.09%，且在15个指标中的14个指标上取得了最优。
- 消融实验表明，自确定的递归分解模块（RD）在验证集上达到了71.50%的四元组准确率，显著优于其他固定分组架构。
- max-mixture强度参数化与双向匹配损失（强度损失+覆盖损失+梯度匹配损失）的组合实现了最佳性能，证实了置换不变训练和组件覆盖约束的有效性。
- LayeredDepth benchmark test set 上 四元组相对深度准确率 Q (All) = 70.09%
---

# SeeGroup: Multi-Layer Depth Estimation of Transparent Surfaces via Self-Determined Grouping

> [!tip] 核心洞察
> 将每个像素的多层深度建模为关于深度的强度函数（max-mixture of Laplace），利用该表示的置换不变性，使模型能够自确定深度层的分组，避免了预排序分组带来的不规则结构，同时强度函数天然编码不确定性，有利于处理透明区域的弱视觉证据。

| 字段 | 内容 |
|------|------|
| 中文题名 | SeeGroup：基于自确定分组的透明表面多层深度估计 |
| 英文题名 | SeeGroup: Multi-Layer Depth Estimation of Transparent Surfaces via Self-Determined Grouping |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wen_SeeGroup_Multi-Layer_Depth_Estimation_of_Transparent_Surfaces_via_Self-Determined_Grouping_CVPR_2026_paper.html) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | SeeGroup |
| Dataset | LayeredDepth benchmark test set |

> [!tip] 效果简介
> - LayeredDepth benchmark test set 上，四元组相对深度准确率 Q (All) 70.09% vs 61.34% (Multi-head DA v2) (+8.75%)；三元组相对深度准确率 T (Mixed) 76.94% vs 62.32% (Multi-head DA v2) (+14.62%)。

## 概要

### 问题瓶颈

透明表面（玻璃、窗户等）在单个像素位置会同时呈现多个处于不同深度的表面——例如玻璃本身的深度及其背后反射/透射场景的深度。现有深度估计方法只能为每个像素预测一个深度值，无法处理这种“一对多”的内在歧义。近期出现的多层深度估计方法虽然尝试为每个像素预测多个深度值，但它们普遍采用**预定义的深度排序分组策略**（如按深度从小到大将各层深度图排列），这种固定顺序并非场景普适，会在不同区域产生不规则的几何和语义结构（见图2）。

### 核心洞察与因果机制

SeeGroup 的核心洞察在于：将每个像素的多层深度建模为**关于深度的强度函数**（max-mixture of Laplace），而非直接回归有序的深度值序列。这一表示具有天然的**置换不变性**——强度函数的峰值位置不依赖于层的排列顺序，从而使模型能够**自确定**跨像素的深度层分组方式，避免了强制预排序带来的不规则结构。同时，强度函数天然编码了预测的不确定性，有利于处理透明区域弱视觉证据下的深度推断。

基于这一表示，SeeGroup 设计了**递归分解模块**（Recurrent Decomposition Module），从骨干网络提取的特征图中迭代分离出主导特征组件，每个组件对应一个深度层，分组顺序完全由模型在训练中自学习确定。训练目标采用**置换不变损失**（强度似然损失 + 组件覆盖损失 + 梯度匹配损失），不强制层序，仅约束预测的强度分布与真实深度的一致性。

### 主要结果

在 LayeredDepth 真实场景基准测试集上，SeeGroup 将**四元组相对深度准确率**（Q, All）从 61.34% 大幅提升至 **70.09%**（+8.75%），在 15 项指标中的 14 项取得了最优（Table 1）。消融实验证实，自确定的递归分解模块在验证集上达到 71.50% 的四元组准确率，显著优于 Multi-head、Index Concat、Recurrent 等固定分组架构；max-mixture 强度参数化与双向匹配损失的组合是实现最佳性能的关键（Table 2）。

### 方法谱系与知识库定位

SeeGroup 属于**多层深度估计**方法，直接对标 Wen et al.（ICCV 2025）提出的 LayeredDepth 基准及其中评估的多分支架构基线：**Multi-head (NeWCRFs)**、**Index Concat (NeWCRFs)**、**Recurrent (NeWCRFs)**，以及采用 Depth Anything V2 骨干的强基线 **Multi-head (DA v2)**。与这些基线强制固定层序的策略不同，SeeGroup 首次将多层深度分组问题形式化为**自确定分组**，并通过置换不变的强度函数表示和递归分解架构实现，在方法范式上与现有工作形成根本性区别。

### 局限与开放问题

在合成数据上，SeeGroup 的逐层深度指标（AbsRel, RMS）略弱于 Multi-head (DA v2)，可能影响单纯追求逐层精度的应用场景。模型在某些模糊区域仍可能预测出多余的不存在层（过度预测），覆盖损失仅能部分缓解。此外，当前训练仅基于合成数据集，对真实世界复杂光照和材质的泛化性能仍有待验证。如何动态决定各像素的实际层数（而非固定最大层数）也是值得探索的方向。



### 透明表面的多层深度歧义

透明物体（如玻璃窗、透明容器）广泛存在于日常和工业场景中，其光学特性对深度感知系统构成了根本性挑战。与不透明表面不同，透明表面不会完全遮挡其后的物体——来自不同深度的光线经透射、折射后同时进入相机，使得单个像素位置可能对应多个物理上有效的深度值。如图1所示，沿相机光轴的每一次介质转换（如空气-玻璃、玻璃-空气）都定义了一个独立的深度层，这些层共同构成了该像素的**多层深度**（multi-layer depth）。

这一物理事实意味着，传统的单目深度估计方法——无论是有监督回归还是自监督重建——在透明区域存在**内在歧义**：它们被设计为仅为每个像素预测一个深度值，而在透明表面处，任何单一深度值都无法完整描述场景的几何结构。这种“一对多”的映射关系是透明场景深度感知的核心瓶颈。

### 现有方法的局限：预定义分组策略

近期工作开始尝试解决多层深度估计问题，其基本思路是将场景的多层几何组织为若干张深度图（每张图对应一个“层”）。然而，如何将散落在不同像素位置的深度值**分组**到这些深度图中，是一个被严重忽视的关键问题。

现有方法（如 **LayeredDepth** 基准中采用的 Multi-head、Index Concat 等架构）普遍采用一种**预定义的深度排序分组策略**：将各层深度图按照深度值从小到大的顺序排列（即第1层总是最近表面，第n层总是最远表面）。这种策略看似自然，实则存在严重缺陷。如图2所示，最优的分组方式高度依赖于场景内容：在某些区域，按深度排序是合理的；但在另一些区域，按物体中心分组（如将同一玻璃杯的前后表面归入同一组）能产生更连贯的语义结构。强制全局统一的预排序策略会导致深度图出现不规则的几何断裂和语义混乱，尤其在不同物体交错遮挡的复杂场景中。

### 本文动机：自确定分组

上述分析揭示了一个根本性的方法缺口：**多层深度估计不仅需要预测深度值，还需要确定这些深度值在跨像素深度图中的分组方式**。理想情况下，分组策略应由模型根据场景内容自行决定，而非由人工规则预先指定。

基于这一洞察，本文提出 **SeeGroup**，其核心动机是让模型**自确定**（self-determine）深度层的分组方式。具体而言，SeeGroup 通过两个关键设计实现这一目标：

1. **置换不变的强度函数表示**：将每个像素的多层深度建模为关于深度的强度函数（max-mixture of Laplace），该表示天然对深度层的排列顺序不敏感，从而使模型免于被强制学习特定的层序。

2. **递归分解模块**：通过迭代地从特征图中分离主导组件，让网络自行学习如何将场景特征分配到不同的深度层，而非依赖固定的多分支结构。

通过消除预定义分组策略带来的归纳偏置，SeeGroup 能够学习到更连贯、更锐利的多层深度图，在真实场景基准上取得了显著的性能提升。



## 核心方法与创新机理

SeeGroup 的核心创新在于将透明表面多层深度估计从“强制排序回归”重构为“自确定分组下的强度函数学习”，通过三个关键槽位的改变，从根本上解耦了深度层分组与模型预测之间的刚性绑定。

### 瓶颈与因果杠杆

现有深度估计方法（包括单目深度估计和早期的多层深度方法）存在一个共同瓶颈：它们将多层深度建模为一个有序序列，强制模型按预定义规则（如深度从小到大）对输出深度图进行排序。这种预排序策略并非场景普适——同一像素在不同区域可能对应不同的物体分组逻辑（Figure 2），强制排序会导致深度图出现不规则的几何断裂和语义错乱。SeeGroup 的因果杠杆在于**置换不变性**：通过将每个像素的多层深度表示为关于深度的强度函数（max-mixture of Laplace），使得模型可以自由决定各深度层在输出中的分组方式，无需在训练或推理时强制指定层序。推理时仅通过峰值检测提取深度值，再按升序排列作为最终输出，从而在不损失信息的前提下实现了对传统排序范式的替代。

### 三个关键槽位改变

**槽位一：多层深度表示与输出形式——从有序深度回归到置换不变强度函数**

基线方法（如 **Multi-head (DA v2)**，Wen et al., ICCV 2025 + Depth Anything V2）直接回归各层深度图，并通过 L1 损失强制模型学习固定的层序。SeeGroup 则预测一个深度强度函数 $\pmb{\Lambda} = \max_{i=1}^{n} \mathbf{L}_i$，其中每个 Laplace 组件 $\mathbf{L}_i(x) = \frac{1}{2b_i} \exp\left(-\frac{|x - d_i|}{b_i}\right)$ 对应一个潜在深度层。该强度函数天然具备置换不变性：交换任意两个组件的顺序不改变 $\pmb{\Lambda}$ 的值。同时，强度函数在深度轴上的积分等于期望的层数（而非概率密度函数所要求的 1），使其能够自然地编码每个像素位置的实际层数不确定性——这对于透明区域中视觉证据薄弱的像素尤为重要。

**槽位二：特征分解架构——从多分支独立头到自确定递归分解**

基线架构采用多分支独立头（Multi-head）、通道拼接（Index Concat）或简单递归（Recurrent）来生成各层特征，这些设计隐含地强制了特征与输出层之间的固定对应关系。SeeGroup 提出**递归分解模块（Recurrent Decomposition Module）**，由 Decomposer $D$ 和 Remapper $R$ 组成，迭代地从残差特征中分离主导组件：

$$\mathbf{C}_i = D(\mathbf{F}_{i-1}), \quad \mathbf{F}_i = \mathbf{F}_{i-1} - \boldsymbol{\eta}_i \cdot R(\mathbf{C}_i)$$

其中缩放因子 $\eta_i = \frac{\|\mathbf{F}_{i-1}\|_2}{\|\mathbf{F}_{i-1}'\|_2}$ 用于稳定训练。该模块的核心特性在于：分离顺序完全由模型自确定，无需任何预定义的分组规则。每次迭代中，Decomposer 从当前残差特征中提取最显著的特征组件，Remapper 将其投影回特征空间并减去，使残差逐步剥离已建模的信息。这一设计与后续的置换不变损失函数协同工作，使模型能够学习场景自适应的分组策略。

**槽位三：训练目标——从固定层序 L1 损失到置换不变的强度似然损失组合**

基线方法对各层深度施加 L1 损失，要求预测深度与真值深度在固定顺序下一一对应。SeeGroup 的训练目标完全摒弃了层序假设，由三项损失构成：

- **强度损失** $\mathcal{L}_{\text{int}} = -\sum_{i=1}^{m} \log \max_j \mathbf{L}_j(d_i)$：最大化真实深度处的强度函数值，天然置换不变；
- **组件覆盖损失** $\mathcal{L}_{\text{cov}} = -\sum_{j=1}^{n} \log \max_{i=1}^{m} \mathbf{L}_j(d_i)$：确保每个预测的 Laplace 组件至少被一个真实深度支撑，抑制过度预测；
- **梯度匹配损失** $\mathcal{L}_{\text{gm}}$：在梯度域对齐预测强度函数与真值深度分布，进一步提升深度边界的锐利度。

总损失 $\mathcal{L} = \lambda_{\text{int}} \mathcal{L}_{\text{int}} + \lambda_{\text{cov}} \mathcal{L}_{\text{cov}} + \lambda_{\text{gm}} \mathcal{L}_{\text{gm}}$（超参 $\lambda_{\text{int}}=1.0$, $\lambda_{\text{cov}}=0.1$, $\lambda_{\text{gm}}=1.0$）。消融实验表明，单独使用强度损失时四元组准确率仅 55.90%，而三项损失组合可达 69.03%（Table 2），验证了覆盖约束和梯度匹配对置换不变训练的关键支撑作用。

### 创新验证

消融实验从三个维度验证了上述创新的有效性（Table 2）：

1. **架构消融**：递归分解模块（RD）在 All 子集上达到 71.50% 的四元组准确率，显著优于 Multi-head（62.36%）、Index Concat（62.37%）和 Recurrent（57.97%），且参数量最少（Table 4）。值得注意的是，Multi-head 架构在深层（Layer5）上退化严重（Q 仅 27.73%），而 RD 在该层仍保持 57.98%，表明自确定分组策略对深层结构的建模优势。

2. **参数化消融**：Max-Mixture 强度参数化优于加权混合（Weighted Mixture，65.30%）和直接回归，验证了取最大值操作在促进组件沿深度轴分工方面的有效性。

3. **损失消融**：强度损失 + 覆盖损失 + 梯度匹配损失的组合在大多数子集上取得最优，而单独使用强度损失性能大幅下降，证实了置换不变训练需要配套的组件覆盖约束和梯度域监督。

在 LayeredDepth 真实场景基准上，SeeGroup 将四元组相对深度准确率从 61.34% 提升至 70.09%（+14.26% 相对增益），且在 15 个评估指标中的 14 个上取得最优（Table 1），为多层深度估计建立了新的技术范式。



SeeGroup 的整体流程围绕一个核心设计展开：**让模型自确定多层深度的分组方式**，而非依赖预定义的深度排序或固定分支结构。图 3 展示了该流程的三个主要阶段。

**特征提取 → 递归分解 → 强度函数预测**

1. **骨干编码器（Backbone Encoder）**：以输入图像 $I \in \mathbb{R}^{H \times W \times 3}$ 为起点，经由预训练的骨干网络（默认采用基于 DINOv2-ViT-L 的 Depth Anything V2）提取初始特征图 $\mathbf{F}_0$。该特征图编码了场景的全局上下文与局部几何线索，为后续分解提供统一的表示基础。

2. **递归分解模块（Recurrent Decomposition Module）**：这是 SeeGroup 的核心架构创新。模块由**分解器 $D$** 和**重映射器 $R$** 组成，以迭代方式从残差特征中逐步分离出 $n$ 个特征组件 $\{\mathbf{C}_1, \mathbf{C}_2, \dots, \mathbf{C}_n\}$（$n$ 为预设的最大层数，实验中设为 4）。第 $i$ 步的更新规则为：
   $$\mathbf{C}_i = D(\mathbf{F}_{i-1}), \quad \mathbf{F}_i = \mathbf{F}_{i-1} - \boldsymbol{\eta}_i \cdot R(\mathbf{C}_i)$$
   其中 $\boldsymbol{\eta}_i = \frac{\|\mathbf{F}_{i-1}\|_2}{\|\mathbf{F}_{i-1}'\|_2}$ 为范数保持的缩放因子，用于稳定训练。分解器 $D$ 从当前残差 $\mathbf{F}_{i-1}$ 中提取主导特征组件 $\mathbf{C}_i$，重映射器 $R$ 将该组件投影回特征空间，经加权减去后更新残差。**组件的提取顺序完全由模型自确定**，不受深度大小或语义类别的先验约束——这是区别于 Multi-head 等固定分支架构的关键所在。

3. **强度预测器（Intensity Predictor）**：每个特征组件 $\mathbf{C}_i$ 被送入预测器 $P$，映射为一对参数：深度中心 $d_i$ 和尺度 $b_i$。这些参数定义了一个 Laplace 形强度贡献：
   $$\mathbf{L}_i(x) = \frac{1}{2b_i} \exp\left(-\frac{|x - d_i|}{b_i}\right)$$
   最终，逐像素的深度强度函数取各组件的逐点最大值：
   $$\pmb{\Lambda} = \max_{i=1}^{n} \mathbf{L}_i$$
   该 **max-mixture** 参数化具有天然置换不变性：无论组件以何种顺序被分解器提取，最终的强度函数 $\pmb{\Lambda}$ 保持不变。这一性质使得训练目标无需强制层序，模型可以自由学习最优分组。

**推理时的深度提取**：训练完成后，推理阶段从强度函数 $\pmb{\Lambda}$ 中检测峰值作为各层的预测深度，过滤间距小于 0.02 的重复峰值，最后按深度升序排列输出有序深度序列。需要注意的是，排序仅发生在推理后处理阶段，训练过程中完全不涉及层序约束。

**输入输出流总结**：输入单张 RGB 图像 → 骨干网络输出特征图 $\mathbf{F}_0$ → 递归分解模块迭代输出 $n$ 个特征组件 → 强度预测器输出 $n$ 组 Laplace 参数 → max-mixture 合成强度函数 → 峰值检测与排序输出多层深度图。整个流程端到端可微，训练仅依赖置换不变的强度损失、组件覆盖损失和梯度匹配损失（详见 3.4 节）。

### 补充图表

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/003_Figure_3.jpg]]
*Figure 3: The overall pipeline of SeeGroup. Starting from a feature map extracted by a backbone encoder, a recurrent decomposition module generate a sequence of self-determined feature components. Then these components are mapped to an intensity function over depth, which is parameterized as a max mixture of Laplace functions*



SeeGroup 的核心由三个紧密协作的模块构成：**递归分解模块**将骨干特征迭代分离为自确定的特征组件；**强度函数预测器**将每个组件映射为深度轴上的 Laplace 强度贡献，并通过 max-mixture 形成整体深度强度分布；**置换不变训练目标**则在不强制层序的前提下优化该分布，使模型学会自确定分组。

### 递归分解模块

给定骨干编码器提取的初始特征图 $\mathbf{F}_0 \in \mathbb{R}^{H \times W \times C}$，递归分解模块通过**分解器** $D$ 和**重映射器** $R$ 的交替作用，逐步从中剥离出 $n$ 个特征组件 $\{\mathbf{C}_1, \mathbf{C}_2, \dots, \mathbf{C}_n\}$。第 $i$ 步的更新规则为：

$$
\mathbf{C}_i = D(\mathbf{F}_{i-1}), \quad \mathbf{F}_i = \mathbf{F}_{i-1} - \boldsymbol{\eta}_i \cdot R(\mathbf{C}_i)
$$

其中 $\mathbf{F}_{i-1}$ 是上一步的残差特征，分解器 $D$ 从中提取当前主导组件 $\mathbf{C}_i$；重映射器 $R$ 将 $\mathbf{C}_i$ 投影回特征空间，得到 $\mathbf{F}_{i-1}' = R(\mathbf{C}_i)$，再通过缩放因子 $\boldsymbol{\eta}_i$ 加权后从残差中减去，迫使下一步分解关注剩余结构。缩放因子定义为：

$$
\eta_i = \frac{\|\mathbf{F}_{i-1}\|_2}{\|\mathbf{F}_{i-1}'\|_2}
$$

其作用是保持更新后特征图的范数与上一步匹配，避免特征尺度在迭代中逐渐衰减，从而稳定训练。整个分解过程不预设组件与深度层的对应关系，分组顺序完全由模型自确定——这是 SeeGroup 区别于固定分组架构（如 Multi-head 或 Index Concat）的根本设计。

### 强度函数参数化

每个特征组件 $\mathbf{C}_i$ 被送入强度预测器 $P$，输出两个空间分辨的标量场：深度中心 $d_i \in \mathbb{R}^{H \times W}$ 和尺度参数 $b_i \in \mathbb{R}^{H \times W}$，共同定义一个 Laplace 形强度贡献：

$$
\mathbf{L}_i(x) = \frac{1}{2b_i} \exp\left(-\frac{|x - d_i|}{b_i}\right)
$$

其中 $x$ 为深度轴上的连续坐标。$\mathbf{L}_i(x)$ 在 $x = d_i$ 处达到峰值，$b_i$ 控制峰的宽度，编码该组件深度预测的不确定性——透明区域视觉证据弱，对应 $b_i$ 较大，峰较平坦。

将所有 $n$ 个组件的 Laplace 函数沿深度轴逐点取最大值，得到整体的**深度强度函数**：

$$
\pmb{\Lambda} = \max_{i=1}^{n} \mathbf{L}_i
$$

这一 max-mixture 构造具有关键性质：**对组件索引的任意排列保持不变**（置换不变性）。这意味着无论分解器以何种顺序输出组件，最终的强度函数 $\pmb{\Lambda}$ 都相同，从而在表示层面消除了对固定层序的依赖。同时，max 操作促使不同组件在深度轴上自然分工——每个深度位置主要由最近的 Laplace 组件主导，避免了加权混合（Weighted Mixture）中各组件相互干扰的问题。

从概率视角看，强度函数 $\pmb{\Lambda}$ 可视为广义密度：其在深度轴上的积分等于期望的层数，而非 1。推理时，在每个像素位置对 $\pmb{\Lambda}$ 进行峰值检测，过滤间距小于 0.02 的重复峰，即可提取该像素的多层深度序列，最后按深度升序排列作为最终输出。

### 置换不变训练目标

训练目标是最大化真实深度在强度函数下的似然。对于像素 $(x, y)$ 处的真实深度集合 $\{d_1, d_2, \dots, d_m\}$（$m$ 为真实层数），似然正比于强度函数在各深度处的乘积：

$$
\mathcal{L}_{(x,y)}(\{d_i\}) \propto \prod_{i=1}^{m} \Lambda_{(x,y)}(d_i)
$$

该乘积对 $\{d_i\}$ 的输入顺序天然不变，与强度函数的置换不变性一致。取负对数得到**强度损失**：

$$
\mathcal{L}_{\text{int}} = -\sum_{i=1}^{m} \log \max_j \mathbf{L}_j(d_i)
$$

仅靠强度损失可能导致模型预测出多余的不存在层（过度预测）。为此引入**组件覆盖损失**：

$$
\mathcal{L}_{\text{cov}} = -\sum_{j=1}^{n} \log \max_{i=1}^{m} \mathbf{L}_j(d_i)
$$

该损失要求每个预测的 Laplace 组件至少被一个真实深度支撑，从而抑制冗余组件。此外，还引入**梯度匹配损失** $\mathcal{L}_{\text{gm}}$，约束预测深度图的梯度与真实深度图的梯度一致，以保持几何边缘的锐利度。总训练目标为三者的加权和：

$$
\mathcal{L} = \lambda_{\text{int}} \mathcal{L}_{\text{int}} + \lambda_{\text{cov}} \mathcal{L}_{\text{cov}} + \lambda_{\text{gm}} \mathcal{L}_{\text{gm}}
$$

其中超参数设置为 $\lambda_{\text{int}} = 1.0$、$\lambda_{\text{cov}} = 0.1$、$\lambda_{\text{gm}} = 1.0$。消融实验证实，三损失组合在验证集上达到 69.03% 的四元组准确率（All Q），而仅用强度损失时骤降至 55.90%（Table 2），验证了覆盖约束和梯度匹配对自确定分组训练的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/002_Figure_2.jpg]]
*Figure 2: Two example grouping strategies to group multi-layer depth into several depth maps. The best grouping strategy is highly scene-dependent and may very by regions of the image*

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/001_Figure_1.jpg]]
*Figure 1: Definition of multi-layer depth. Figure reproduced from [46]. (a) Each transition in medium along the camera ray defines a distinct layer. (b) Depth on i-th layer is the distance along the z-axis from the i-th layer to the camera*



## 实验与关键发现

SeeGroup 在真实场景多层深度基准 LayeredDepth 上进行了系统评估，并从架构设计、强度参数化和损失函数三个维度展开了消融实验，以验证自确定分组策略的有效性。

### 主实验结果

在 LayeredDepth 基准测试集上，SeeGroup 在 15 个评估指标中的 14 个上取得了最优结果，显著超越了所有基线方法（Table 1）。具体而言，SeeGroup 将四元组相对深度准确率 **Q (All)** 从 Multi-head (DA v2) 基线的 61.34% 提升至 **70.09%**，相对提升幅度达 14.26%；在三元组指标 **T (Mixed)** 上，提升更为显著，从 62.32% 跃升至 **76.94%**，增幅达 14.62 个百分点。这表明自确定分组策略在需要跨层推理的复杂场景中具有突出优势。

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/004_Table_1.jpg]]
*Table 1: Multi-layer depth estimation methods evaluated on LayeredDepth benchmark test set via tuple-wise accuracy. Best scores are in bold. Second best underlined*

定性结果（Figure 4）进一步印证了定量结论：SeeGroup 生成的多层深度图边缘更锐利、伪影更少，尤其在透明物体边界和反射重叠区域，其深度分层更为清晰连贯，而基线方法常出现层间混淆或深度跳变。

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on LayeredDepth benchmark. Our method produce sharper results with less artifacts*

### 消融实验

消融实验在 LayeredDepth 验证集上展开，覆盖架构、参数化方式和损失函数三个关键设计选择（Table 2）。

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/006_Table_2.jpg]]
*Table 2: Ablation results on LayeredDepth validation set via tuple-wise accuracy. Best scores are in bold. Second best underlined*

**架构消融**：对比了四种特征分解架构——Multi-head（多分支独立头）、Index Concat（通道拼接）、Recurrent（递归迭代）和本文提出的递归分解模块（RD）。RD 在 All 子集上取得了 **71.50%** 的四元组准确率，大幅领先 Multi-head（62.36%）、Index Concat（62.37%）和 Recurrent（57.97%）。值得注意的是，Multi-head 架构在深层（Layer5）上退化严重，Q 值仅 27.73%，而 RD 在同一层上保持 **57.98%**，说明自确定的递归分解能有效避免深层信息的丢失。此外，RD 的参数量最少（Table 4），实现了性能与效率的双重优势。

**强度参数化消融**：比较了 Max-Mixture（本文方案）、Weighted Mixture（加权混合）和直接回归三种参数化方式。Max-Mixture 在 All 子集上达到 **69.03%** Q，优于 Weighted Mixture 的 65.30%，验证了取最大值操作在促进各组件沿深度轴分工方面的关键作用——max 操作天然鼓励不同 Laplace 组件覆盖不同的深度区间，从而形成更清晰的层分离。

**损失函数消融**：单独使用强度损失 $L_{int}$ 时，Q 值仅 55.90%；加入组件覆盖损失 $L_{cov}$ 后提升至 65.66%；进一步加入梯度匹配损失 $L_{gm}$ 达到最优 **69.03%**。这一阶梯式提升表明：$L_{int}$ 提供了置换不变的训练基础；$L_{cov}$ 通过约束每个预测组件至少被一个真实深度支撑，有效抑制了过度预测；$L_{gm}$ 则通过匹配强度函数的梯度结构，进一步增强了深度边界的锐度。

### 合成数据上的表现与失效模式

在 LayeredDepth-Syn 合成验证集上，SeeGroup 的标准逐层深度指标（AbsRel、RMS）略弱于 Multi-head (DA v2)（Table 3）。然而，定性分析（Figure 5）显示，这一差异主要源于合成数据中的噪声边界标注：SeeGroup 学到了更平滑、更合理的背景层，而 Multi-head 倾向于过拟合噪声边界，这在真实场景的元组准确率大幅领先中得到了印证——SeeGroup 的预测更适应实际应用中的弱纹理和模糊区域。

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/007_Table_3.jpg]]
*Table 3: Multi-layer depth estimation methods evaluated on our LayeredDepth-Syn validation set. Values are scaled by 100 for clearer comparison. Best scores are in bold. Second best underlined*

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative results on LayeredDepth-Syn validation set. Our model produces smooth, coherent background layers*

已知的失效模式包括：模型在极端模糊或高透明度区域仍可能预测出多余的不存在层（过度预测）。尽管 $L_{cov}$ 已部分缓解该问题，但在视觉证据极弱的像素处，强度函数可能出现虚假峰值。此外，当前训练仅依赖合成数据，在真实世界复杂光照和材质多样性下的泛化边界尚需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2093_https_openaccess_thecvf_com_content_CVPR2026_html_Wen_SeeGroup_Multi_Lay/figures/008_Table_4.jpg]]
*Table 4: We report the total number of parameters (#Param), the number of parameters excluding the pretrained encoder (#Param w/o enc), CPU time and GPU time per forward pass, and FLOPs for all three architectures. Our Recurrent Decomposition Module (RD) uses the fewest parameters among them*



## 定位与知识库关联

### 问题定位：从单层深度到多层深度的范式跃迁

传统单目深度估计方法（包括基于ViT的强基线**Depth Anything V2**）均假设每个像素仅对应一个深度值。然而，透明表面（玻璃、窗户、透明容器等）使得相机光线穿越多个介质转换界面，单个像素同时“看见”反射层、折射背景层以及透明物体自身表面等多个处于不同深度的层。这一物理事实导致单层深度预测存在**内在歧义**——模型被迫在多个真实深度之间做出选择，无论输出哪个值都是错误的。

**LayeredDepth**（Wen et al., ICCV 2025）首次将透明表面深度估计形式化为多层深度预测问题，并构建了相应的基准数据集与元组准确率评估体系（Q/T/P）。该工作的核心贡献在于问题定义和评估框架，但其方法仍采用**预定义的深度排序分组策略**——将各层深度图按深度从小到大排列。如Figure 2所示，这种“一刀切”的排序方式并非场景普适：在物体中心分组策略下，同一物体不同部分的深度可能被错误地分配到不同层，产生不规则的几何和语义结构。

### 核心方法对比：自确定分组 vs. 固定排序

SeeGroup与现有方法的关键分水岭在于**深度层分组策略**。下表从三个核心维度对比方法谱系中的关键差异：

| 维度 | 固定排序方法（Multi-head等） | SeeGroup（本方法） |
|------|---------------------------|-------------------|
| **输出形式** | 直接回归有序深度图（多分支L1回归） | 预测深度强度函数（max-mixture of Laplace），推理时通过峰值检测提取深度序列 |
| **分组机制** | 强制按深度大小排列各层 | 递归分解模块自确定跨像素的分组方式，无需预定义顺序 |
| **训练目标** | 对各层深度施加L1损失（顺序固定） | 置换不变的强度似然损失 + 组件覆盖损失 + 梯度匹配损失 |

具体而言，现有基线包括：
- **Multi-head**（Wen et al., ICCV 2025）：多分支独立头直接回归各层深度，强制固定分组顺序
- **Index Concat**（Wen et al., ICCV 2025）：通道拼接作为各层特征，同样依赖固定分组
- **Recurrent**（Wen et al., ICCV 2025）：递归迭代预测各层深度，但输出仍按固定顺序排列
- **Multi-head (DA v2)**：采用Depth Anything V2骨干的强基线，是LayeredDepth基准上此前的最优方法

SeeGroup的突破在于**将分组顺序从“预设约束”转变为“学习目标”**。其递归分解模块（Decomposer + Remapper）通过迭代从残差特征中分离主导组件：

$$\mathbf{C}_i = D(\mathbf{F}_{i-1}), \quad \mathbf{F}_i = \mathbf{F}_{i-1} - \boldsymbol{\eta}_i \cdot R(\mathbf{C}_i)$$

这一过程使模型能够根据场景语义自确定哪些像素属于同一层，而非被深度数值大小所绑架。配合max-mixture强度函数 $\pmb{\Lambda} = \max_{i=1}^{n} \mathbf{L}_i$ 的置换不变性，训练目标不再强制层序对应：

$$\mathcal{L}_{\text{int}} = -\sum_{i=1}^{m} \log \max_j \mathbf{L}_j(d_i)$$

### 实验证据与性能边界

**主实验结果（Table 1）**：在LayeredDepth真实场景基准上，SeeGroup将四元组相对深度准确率（Q, All）从61.34%（Multi-head DA v2）大幅提升至70.09%（+8.75个百分点），且在15个评估指标中的14个上取得最优。三元组准确率（T, Mixed）的提升更为显著，从62.32%跃升至76.94%（+14.62个百分点）。

**消融实验（Table 2）**揭示了各组件的贡献：
- **架构层面**：递归分解模块（RD）在All Q上达到71.50%，显著优于Multi-head（62.36%）、Index Concat（62.37%）和Recurrent（57.97%），且参数量最少（Table 4：总计356M，去除预训练编码器后仅51M）
- **参数化层面**：Max-Mixture强度参数化（69.03% Q on All）优于加权混合（65.30%）和直接回归，验证了置换不变表示的有效性
- **损失函数层面**：强度损失+覆盖损失+梯度匹配损失的组合达到最优（69.03%），单独使用强度损失时性能骤降至55.90%，说明组件覆盖约束和梯度匹配对训练稳定性至关重要
- **深层性能**：Multi-head架构在深层（Layer5）上退化严重（Q=27.73%），而RD保持稳定（Q=57.98%），表明自确定分组对远距离层的歧义处理更具鲁棒性

### 适用边界与已知局限

**合成数据的逐层精度权衡**：在LayeredDepth-Syn合成验证集上，SeeGroup的标准逐层深度指标（AbsRel, RMS）略弱于Multi-head (DA v2)（Table 3）。原文作者认为该差异源自合成数据中的噪声边界标注——SeeGroup学到了更平滑、更合理的背景层（Figure 5），而固定排序方法可能过拟合到噪声标注。这一现象提示：**在追求精确逐层对齐的应用场景中，SeeGroup的优势可能被稀释**；但在真实世界场景的元组准确率大幅领先，表明其更适合实际部署。

**过度预测风险**：模型有概率预测出多余的不存在层，尤其在透明区域视觉证据薄弱时。尽管覆盖损失 $\mathcal{L}_{\text{cov}} = -\sum_{j=1}^{n} \log \max_{i=1}^{m} \mathbf{L}_j(d_i)$ 已部分缓解该问题，但仍是已知的失效模式。

**合成数据依赖**：当前训练仅基于合成数据集，真实世界场景中的复杂光照、材质多样性（如磨砂玻璃、渐变透明度）可能降低泛化性能。

### 开放问题与未来方向

1. **动态层数推理**：当前模型固定最大层数n=4，但不同像素的实际层数各异。如何使模型动态决定各像素的层数（例如通过强度积分阈值判断），以提升效率并减少过度预测？
2. **过度预测的根治**：覆盖损失仅能部分抑制虚假层，在高透明度或极端光照条件下仍可能失效。是否需要引入对抗训练或物理先验来更根本地约束组件数量？
3. **真实场景泛化**：如何将自确定分组策略扩展到更多样的真实世界透明场景（弯曲玻璃、多层叠加），并降低对合成数据的依赖？域适应或自监督微调可能是可行路径。
4. **与其他模态的融合**：偏振成像、ToF传感器等模态可提供额外的层分离线索，自确定分组框架是否能自然融合这些信号？



## 原文 PDF

![[paperPDFs/CVPR_2026/SeeGroup_Multi_Layer_Depth_Estimation_of_Transparent_Surfaces_via_Self_Determined_Grouping.pdf]]
