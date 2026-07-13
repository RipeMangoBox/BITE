---
title: Open-Set Semantic Gaussian Splatting SLAM with Expandable Representation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Open_Set_Semantic_Gaussian_Splatting_SLAM_with_Expandable_Representation_fa5af39ce6a2.pdf
project_link: "https://cvg.cit.tum.de/data/datasets/rgbd-dataset"
code_link: "https://github.com/facebookresearch/"
aliases:
- OSSGSS
- OSSGSSER
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入一个可动态扩展的语义特征池，将场景级语义与3D高斯解耦，并通过低维索引向量实现轻量级语义检索。
primary_logic: 通过将全局语义浓缩到一个小规模的可扩展特征池中，并使用软聚合的索引向量为每个高斯分配语义，可以大幅降低内存开销，支持语义的持续更新和拓展；同时，引入帧内-帧间一致性目标和语义稳定性引导机制，有效解决跨视角语义不一致问题。
claims:
- 在Replica数据集上，SplaTAM+Ours相比SplaTAM在PSNR上提升3.50，ATE RMSE降低0.07，Depth L1降低0.38，大幅超越Strong Baseline。
- 在Replica闭集语义分割上，SplaTAM+Ours的mIoU达96.76%，显著优于GS³LAM（87.22%）等现有语义SLAM方法。
- 消融实验证实，可扩展语义池（+7.59 mIoU）、一致性目标（+4.08 mIoU）和稳定性引导（+3.06 mIoU）均对性能有重要贡献，且池设计避免内存爆炸。
- Replica 上 PSNR = 37.61 (SplaTAM+Ours)
---

# Open-Set Semantic Gaussian Splatting SLAM with Expandable Representation

> [!tip] 核心洞察
> 通过将全局语义浓缩到一个小规模的可扩展特征池中，并使用软聚合的索引向量为每个高斯分配语义，可以大幅降低内存开销，支持语义的持续更新和拓展；同时，引入帧内-帧间一致性目标和语义稳定性引导机制，有效解决跨视角语义不一致问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 具有可扩展表示的开放集语义高斯泼溅SLAM |
| 英文题名 | Open-Set Semantic Gaussian Splatting SLAM with Expandable Representation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E68dgQUzrC) · [Code](https://github.com/facebookresearch/) · [Project](https://cvg.cit.tum.de/data/datasets/rgbd-dataset) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Open-Set Semantic Gaussian Splatting SLAM |
| Dataset | Replica |

> [!tip] 效果简介
> - Replica 上，PSNR 37.61 (SplaTAM+Ours) vs 34.11 (SplaTAM) (+3.50)；ATE RMSE 0.29 (SplaTAM+Ours) vs 0.36 (SplaTAM) (-0.07)；Depth L1 0.34 (SplaTAM+Ours) vs 0.72 (SplaTAM) (-0.38)。

## 概要

### 问题背景与瓶颈

同步定位与建图（SLAM）是具身智能与混合现实的核心能力。近年来，基于3D高斯泼溅（3DGS）的密集SLAM方法在重建质量和效率上取得了显著进展，但其语义理解能力仍局限于闭集设定——只能识别预定义的类别集合，无法应对开放世界中任意语义概念的感知需求。现有3DGS-SLAM方法面临三个根本性瓶颈：

1. **语义表示僵化**：每个3D高斯直接存储高维语义特征向量，或依赖渲染后的2D分类获取语义，无法在增量式场景建模中动态整合新的语义概念。
2. **内存消耗失控**：随着场景扩展，高斯数量和高维语义特征急剧增长，导致显存占用迅速膨胀，限制了大规模场景的适用性。
3. **跨视角语义不一致**：缺乏专门的多视角一致性处理，2D语义预测在不同视点下波动剧烈，难以构建连贯的3D语义场。

### 核心方法

本文提出**Open-Set Semantic Gaussian Splatting SLAM**，核心思想是将场景级语义浓缩到一个**可动态扩展的共享语义特征池**中，使每个3D高斯仅存储低维索引向量，通过近邻软聚合从池中检索语义。这一设计实现了语义与几何的解耦，大幅降低内存开销，并支持在线持续更新和拓展语义知识。

在此基础上，引入两个关键机制保障语义质量：
- **帧内-帧间语义一致性目标**：通过对比学习强化同一对象在不同像素和不同帧之间的语义特征稳定性。
- **语义稳定性引导**：利用历史帧的语义相似度计算置信度，自适应降低噪声语义的学习权重。

### 主要发现

在Replica数据集上，该方法基于SplaTAM框架实现了显著提升：PSNR提高3.50（37.61 vs. 34.11），ATE RMSE降低0.07 cm，Depth L1降低0.38 cm。在闭集语义分割上，mIoU达96.76%，大幅超越GS³LAM（87.22%）等现有语义SLAM方法。在开放集语义分割上，2D mIoU达66.5%，优于基于SfM的GOI方法（59.3%）。消融实验证实，可扩展语义池（+7.59 mIoU）、一致性目标（+4.08 mIoU）和稳定性引导（+3.06 mIoU）均对性能有独立且重要的贡献。

在大规模场景测试中，当其他语义SLAM方法因显存不足（>24 GB）而失败时，该方法仅需19.5 GB显存即可完成建图，验证了语义池设计的内存效率。

### 方法定位

该方法在现有3DGS-SLAM框架（如SplaTAM、LoopSplat）之上构建，保留了原有的RGB-D损失和相机追踪设置，仅添加语义模块。其核心创新在于将全局语义浓缩为可扩展的特征池，区别于每个高斯独立存储语义的SGS-SLAM和依赖渲染后分类的GS³LAM。在方法谱系上，该方法属于**基于3DGS的密集语义SLAM**，同时融合了开放集视觉基础模型（SAM、CLIP）的感知能力，实现了从闭集到开放集语义建图的跨越。

### 3D高斯泼溅SLAM的兴起与语义化的需求

同时定位与建图（SLAM）是机器人、增强现实和自动驾驶等领域的核心使能技术。近年来，以3DGS（3D Gaussian Splatting）为代表的辐射场表达方法，凭借其显式几何表示、高保真渲染质量和实时性能，在稠密视觉SLAM中展现出巨大潜力。相比于基于NeRF的隐式表达方法（如**Point-SLAM**），3DGS-SLAM方法（如**SplaTAM**、**LoopSplat**）能够更高效地处理场景几何与外观，同时支持动态增删高斯点以适应增量式场景扩展。

然而，仅重建场景的几何与外观已无法满足日益复杂的交互与理解需求。赋予SLAM系统语义理解能力——尤其是**开放集语义**（即不局限于预定义类别集合的语义概念）——成为推动该领域发展的关键方向。开放集语义SLAM的目标是：在未知环境中实时构建包含丰富语义信息的三维地图，使系统能够理解场景中任意物体的语义属性，而非仅识别有限的闭集类别。

### 现有方法的瓶颈：语义表达的内存爆炸与不一致性

当前，将语义信息融入3DGS-SLAM的尝试面临三个根本性挑战，构成制约该方向发展的核心瓶颈：

**1. 语义特征的内存开销随场景规模急剧膨胀。** 现有语义3DGS-SLAM方法（如**GS³LAM**、**SGS-SLAM**）通常为每个3D高斯直接存储高维语义特征向量。在增量式SLAM场景中，高斯数量随探索范围持续增长，导致语义特征存储的内存需求线性甚至超线性增长。对于大规模场景，这种“每高斯一特征”的朴素策略极易触发硬件显存上限——实验表明，**SGS-SLAM**和**GS³LAM**在超过24 GB显存的大规模场景中直接因显存不足而失败（Table 7）。

**2. 无法动态整合新的开放集语义。** 现有语义SLAM方法（如**SNI-SLAM**、**Hier-SLAM++**）多为闭集设计，其语义空间在训练前即已固定，无法在增量式建图过程中接纳新的语义概念。当系统在开放世界中遇到训练时未见过的物体类别时，缺乏动态扩展语义空间的能力导致语义信息丢失或错误归类。

**3. 跨视角语义一致性差。** 基于2D视觉模型（如CLIP、SAM）提取的逐帧语义标签，在不同视角下对同一物体的语义预测往往存在显著差异。现有方法缺乏专门的跨视角语义对齐机制，导致渲染出的三维语义场在视角切换时出现语义漂移或冲突，严重损害下游任务（如3D物体定位、场景编辑）的可靠性。

### 本文动机：解耦语义与几何，实现可扩展的开放集语义SLAM

针对上述瓶颈，本文提出**Open-Set Semantic Gaussian Splatting SLAM**，核心动机在于打破“语义与高斯强绑定”的传统范式，通过**语义特征与3D高斯的解耦**实现三个关键突破：

- **内存高效**：将全局场景语义浓缩到一个共享的、小规模的可扩展语义特征池中，每个高斯仅存储低维索引向量（键），通过软聚合从池中检索语义。这一设计将语义存储复杂度从 $\mathcal{O}(N \times D)$ 降至 $\mathcal{O}(N \times d + M \times D)$（其中 $N$ 为高斯数量，$D$ 为语义特征维度，$d \ll D$ 为键维度，$M \ll N$ 为池大小），从根本上遏制了内存爆炸。

- **动态可扩展**：语义特征池支持根据输入语义的新颖性判断动态插入或更新条目，使系统能够在增量式SLAM过程中持续接纳新的开放集语义概念，无需重新训练或预设类别空间。

- **跨视角一致**：引入帧内-帧间语义一致性对比损失，强制同一物体在不同视角下的语义特征保持一致；同时提出语义稳定性引导机制，利用历史帧语义相似度自适应调制损失权重，降低噪声语义对优化的干扰。

通过上述设计，本文方法在保持3DGS-SLAM几何与外观重建优势的同时，首次实现了高效、可扩展且语义一致的开放集语义三维建图，为日常设备（如智能手机）上的野外场景语义重建铺平了道路（Figure 1）。

## 核心方法与创新机理

本工作针对现有3DGS-SLAM在开放集语义建图中的根本瓶颈——**高维语义特征与3D高斯强绑定导致的内存爆炸、无法动态接纳新语义概念、以及跨视角语义不一致**——提出了三个关键创新点，构成一个可扩展的开放集语义高斯泼溅SLAM系统。

### 创新一：可扩展语义特征池（Expandable Semantic Feature Pool）

**核心思想**：将场景级语义从3D高斯中解耦，浓缩到一个全局共享、可动态扩展的语义特征池中。每个3D高斯仅维护一个低维键向量（key），通过近邻软聚合从池中检索语义，实现轻量级语义绑定。

**具体机制**：
- 语义高斯场定义为 $\mathcal { G } _ { S } : = \{ \mathcal { G } _ { S i } : ( \pmb { \mu } _ { i } , \pmb { \Sigma } _ { i } , o _ { i } , \pmb { c } _ { i } , \pmb { k } _ { i } ) , \pmb { K } _ { P } , \pmb { F } _ { P } \} _ { i = 1 } ^ { N }$（Eq.6），其中 $\pmb { K } _ { P }$ 为键池，$\pmb { F } _ { P }$ 为语义特征池。
- 每个高斯的语义特征 $\pmb { s } _ { i }$ 通过以下步骤获得：
  1. 在键池中通过余弦相似度找到 $m$ 个最近邻：$\mathrm { N N } _ { m } ( { k _ { i } } , K _ { P } ) = \mathrm { a r g } \operatorname* { m a x } _ { m } ( \cos ( { k _ { i } } , K _ { P } ) )$（Eq.7）
  2. 将相似度转换为软聚合权重：${\pmb w } _ { i } = \mathrm { s o f t m a x } ( \mathrm { N N } _ { m } ( { \pmb k } _ { i } \cdot { \pmb K } _ { P } ) )$（Eq.8）
  3. 加权聚合语义特征：${\pmb s } _ { i } = {\pmb w } _ { i } \cdot { \pmb F } _ { P } ^ { \prime }$（Eq.9）
- **动态扩展**：当输入语义与现有池的相似度低于阈值时，判定为新语义概念，自动插入新的键-值对到池中，实现持续语义更新（§3.2.1 Expansion, Algorithm 1）。

**对比基线**：现有方法（如SGS-SLAM、GS³LAM）每个高斯直接存储高维语义特征向量，内存随高斯数量线性增长；而本方法将语义存储压缩到共享池中，每个高斯仅存低维键，内存效率显著提升。消融实验证实，可扩展池相比固定大小的硬索引码本，mIoU高出3.83（Table 6）；在大规模场景中，基线方法因显存不足（>24GB）失败，而本方法仅需19.5GB（Table 7）。

### 创新二：帧内-帧间语义一致性目标（Intra-Inter Semantic Consistency Objective）

**核心思想**：通过对比学习，强制同一语义对象的像素在不同视角和不同时间帧下具有一致的语义特征，解决2D模型预测在多视点下的不一致问题。

**具体机制**：
- 损失函数为帧内与帧间对比损失的加权和（Eq.14）：$\mathcal { L } _ { C O } = \frac { 1 - \lambda _ { r } } { Q } \sum _ { i = 1 } ^ { Q } \mathcal { L } ( \pmb { p } _ { i } ^ { + } ) + \frac { \lambda _ { r } } { R } \sum _ { i = 1 } ^ { R } \mathcal { L } _ { r } ( \pmb { p } _ { i , r } ^ { + } )$
  - 帧内项：利用SAM分割掩码，拉近同一对象内像素的语义特征，推远不同对象间的特征。
  - 帧间项：利用历史帧的渲染语义作为正样本，增强时序一致性。
- 消融实验表明，添加该一致性目标带来 **+4.08 mIoU** 的提升（Table 4, +L_CO）。

**对比基线**：现有语义SLAM方法无专门的跨视角一致性处理，直接使用单帧2D语义预测作为监督信号，导致多视角下同一物体的语义标签漂移。

### 创新三：语义稳定性引导（Semantic Stability Guidance）

**核心思想**：利用历史帧的语义相似度计算每个像素的语义置信度，自适应调制语义损失的权重，降低噪声或不稳定语义对建图的负面影响。

**具体机制**（Figure 3）：
- 对当前帧的每个像素，计算其语义特征与历史帧中对应位置语义特征的相似度。
- 相似度高的像素赋予高置信度，在语义损失中权重更大；相似度低的像素（可能因遮挡、视角变化或2D模型错误）权重降低。
- 该机制作为损失调制器 $M_{SG}$ 作用于语义优化过程，消融实验证实带来 **+3.06 mIoU** 的提升（Table 4, +M_SG）。

**对比基线**：现有方法对所有像素的语义监督等权重处理，容易受2D模型预测噪声干扰。

### 创新协同效果

三个创新协同作用，形成完整的开放集语义SLAM方案：
- **可扩展池**解决了“存什么”的问题——高效、动态的语义表示；
- **一致性目标**解决了“如何对齐”的问题——跨视角语义一致性；
- **稳定性引导**解决了“信多少”的问题——自适应抑制噪声。

消融实验（Table 4）完整验证了协同效果：从无池基线（72.56 mIoU）开始，逐步添加一致性目标（+4.08）和稳定性引导（+3.06），最终达到完整模型的性能。在Replica数据集上，本方法（SplaTAM+Ours）的闭集语义分割mIoU达96.76%，显著优于GS³LAM（87.22%）等现有语义SLAM方法（Table 2）。

本工作提出 **Open-Set Semantic Gaussian Splatting SLAM**，在现有 3DGS-based SLAM 框架上构建了一套可扩展的开放集语义建图系统。整体 pipeline 由六个核心模块串联而成，形成从 RGB-D 输入到语义 3D 重建的完整数据流。

### 输入与追踪

系统接收连续的 RGB-D 流作为输入。在追踪阶段（§3.1.2），利用当前帧与已建好的 3D 高斯场景进行可微渲染比对，通过联合优化颜色、深度和语义损失来估计相机位姿。追踪损失定义为：

$$L_{tracking} = \sum_p (\lambda_{T,C} L_{T,C} + \lambda_{T,D} L_{T,D} + \lambda_{T,S} L_{T,S})$$

该损失在像素级别同时约束颜色、深度和语义三个模态，使位姿估计受益于多模态信号。

### 3D 高斯场景建图

场景几何与外观由一组 3D 高斯表示。每个高斯 $G_i$ 包含位置 $\mu_i$、协方差 $\Sigma_i$（由缩放和旋转矩阵构成）、不透明度 $o_i$ 和颜色 $c_i$：

$$\mathcal{G} := \{ \mathcal{G}_i : (\pmb{\mu}_i, \pmb{\Sigma}_i, o_i, \pmb{c}_i) \}_{i=1}^N$$

在建图过程中，系统动态增删高斯点以适应增量式场景探索，同时优化几何与外观参数。

### 开放集语义提取

为获取逐像素的开放集语义监督信号，系统利用 **SAM** 进行无类别分割，再通过 **CLIP** 提取每个分割区域的语义特征向量，作为 Ground Truth 语义监督（supp. §A.1）。这一前置模块将 2D 基础模型的开放集能力转化为可学习的 3D 语义目标。

### 可扩展语义特征池（核心创新）

语义模块的核心是一个**可扩展的语义特征池**（§3.2.1）。传统方法为每个高斯直接存储高维语义向量，导致内存随高斯数量线性膨胀。本文提出将全局语义浓缩到一个共享的、可动态扩展的特征池 $\pmb{F}_P$ 中，并维护对应的键池 $\pmb{K}_P$。每个高斯仅存储一个低维键向量 $\pmb{k}_i$，通过余弦相似度在键池中找到 $m$ 个最近邻：

$$\mathrm{NN}_m({k_i}, K_P) = \mathrm{arg\,max}_m (\cos({k_i}, K_P))$$

随后通过 softmax 得到聚合权重 $\pmb{w}_i$，从特征池中检索语义：

$$\pmb{s}_i = \pmb{w}_i \cdot \pmb{F}_P'$$

这一设计将语义存储开销从 $O(N \times D)$ 降至 $O(N \times d + M \times D)$（$d \ll D$，$M \ll N$），在保持表达能力的同时大幅压缩内存。

### 语义渲染

获得每个高斯的语义特征 $\pmb{s}_i$ 后，通过 alpha 混合渲染任意像素 $\pmb{p}$ 的语义特征：

$$\boldsymbol{S}(\boldsymbol{p}) = \sum_{j=1}^N \boldsymbol{s}_j \alpha_j \prod_{k=1}^{j-1} (1 - \alpha_k)$$

这构建了一个可微的 3D 语义场，使语义可以与颜色、深度一起通过渲染进行优化。

### 帧内-帧间一致性目标与稳定性引导

为解决 2D 模型预测在多视角下的不一致问题，系统引入**帧内-帧间语义一致性对比损失**（§3.3.2, Eq.13-14），强制同对象像素在不同视角和时序下保持语义特征一致。同时，**语义稳定性引导机制**（Figure 3）利用历史帧语义相似度计算置信度，对噪声语义赋予较低的学习权重，避免不可靠监督污染语义池。

### 联合损失优化

建图阶段的总损失联合优化颜色、深度和语义：

$$\mathcal{L}_{mapping} = \lambda_{M,C} \mathcal{L}_{M,C} + \lambda_{M,D} \mathcal{L}_{M,D} + \lambda_{M,S} \mathcal{L}_{M,S}$$

其中 $\mathcal{L}_{M,S}$ 包含语义渲染损失、帧内-帧间一致性损失，并受稳定性引导调制。

### 数据流总结

整体数据流为：**RGB-D → 追踪（位姿估计）→ 3D 高斯建图（几何/外观）→ SAM+CLIP 语义提取 → 可扩展语义池检索 → 语义渲染 → 一致性目标与稳定性引导 → 联合优化**。各模块协同工作，使系统在增量式 SLAM 过程中持续更新、扩展语义知识，最终输出具有开放集语义标注的完整 3D 场景重建。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/002_Figure_2.jpg]]
*Figure 2: Framework Overview. We enhance existing 3DGS-based SLAM with an expandable semantic representation, introducing a learnable semantic feature pool that stores condensed scene-level semantics and supports dynamic expansion. Each Gaussian retrieves its semantic feature via soft aggregation from the shared pool through a lightweight key. To improve cross-view and temporal consistency, we further introduce an Intra-Inter Semantic Consistency Objective and a Semantic Stability Guidance mechanism, enabling stable and coherent open-set semantic reconstruction during SLAM*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/001_Figure_1.jpg]]
*Figure 1: This work introduces Open-Set Semantic Gaussian Splatting SLAM, a system designed to enable everyday devices (e.g., smartphones) to capture and reconstruct in-the-wild 3D scenes with rich, open-set semantics on top of SLAM frameworks*

本方法在现有3DGS-SLAM框架上引入三个核心模块：(1) 可扩展语义特征池与键聚合机制，(2) 语义渲染管线，以及 (3) 帧内-帧间语义一致性目标与稳定性引导。以下逐一给出关键公式及其变量含义。

---

### 3D高斯场与语义高斯场

基础3D高斯场定义为：

$$
\mathcal { G } : = \{ \mathcal { G } _ { i } : ( \pmb { \mu } _ { i } , \pmb { \Sigma } _ { i } , o _ { i } , \pmb { c } _ { i } ) \} _ { i = 1 } ^ { N }
$$

其中 $\pmb{\mu}_i$ 为高斯中心位置，$\pmb{\Sigma}_i$ 为协方差矩阵，$o_i$ 为不透明度，$\pmb{c}_i$ 为颜色。协方差矩阵由缩放矩阵 $\pmb{S}_i$ 和旋转矩阵 $\pmb{R}_i$ 计算：

$$
\pmb { \Sigma } _ { i } = \pmb { R } _ { i } \pmb { S } _ { i } \pmb { S } _ { i } ^ { \top } \pmb { R } _ { i } ^ { \top }
$$

在此基础上，语义高斯场为每个高斯增加低维键向量 $\pmb{k}_i$，并维护共享的可学习键池 $\pmb{K}_P$ 与语义特征池 $\pmb{F}_P$：

$$
\mathcal { G } _ { S } : = \{ \mathcal { G } _ { S i } : ( \pmb { \mu } _ { i } , \pmb { \Sigma } _ { i } , o _ { i } , \pmb { c } _ { i } , \pmb { k } _ { i } ) , \pmb { K } _ { P } , \pmb { F } _ { P } \} _ { i = 1 } ^ { N }
$$

---

### 可扩展语义池与键聚合

每个高斯的语义特征不直接存储高维向量，而是通过从共享池中软聚合获得。具体流程如下：

**步骤1：近邻检索。** 对高斯 $i$ 的键 $\pmb{k}_i$，在键池 $\pmb{K}_P$ 中通过余弦相似度选取 $m$ 个最近邻：

$$
\mathrm { N N } _ { m } ( { k _ { i } } , K _ { P } ) = \mathrm { a r g } \operatorname* { m a x } _ { m } ( \cos ( { k _ { i } } , K _ { P } ) )
$$

**步骤2：Softmax加权。** 将相似度转换为聚合权重：

$$
{ \pmb w } _ { i } = \mathrm { s o f t m a x } ( \mathrm { N N } _ { m } ( { \pmb k } _ { i } \cdot { \pmb K } _ { P } ) )
$$

**步骤3：语义特征聚合。** 用权重从特征池 $\pmb{F}_P$ 的对应子集 $\pmb{F}_P'$ 中加权求和：

$$
{ \pmb s } _ { i } = { \pmb w } _ { i } \cdot { \pmb F } _ { P } ^ { \prime }
$$

**动态扩展机制：** 当输入语义与现有池中所有键的相似度均低于阈值时，判定为新语义，在 $\pmb{K}_P$ 和 $\pmb{F}_P$ 中动态插入新条目；否则仅更新已有条目。这避免了为每个高斯存储独立高维特征，将内存复杂度从 $\mathcal{O}(N \cdot D_s)$ 降至 $\mathcal{O}(|\mathcal{P}| \cdot D_s + N \cdot d_k)$，其中 $|\mathcal{P}|$ 为池大小，$d_k$ 为键维度（文中 $d_k=3$，远小于语义特征维度 $D_s$）。

---

### 语义渲染

像素 $\pmb{p}$ 处的渲染语义特征 $\pmb{S}(\pmb{p})$ 通过 alpha 混合获得：

$$
\boldsymbol { S } ( \boldsymbol { p } ) = \sum _ { j = 1 } ^ { N } \boldsymbol { s } _ { j } \alpha _ { j } \prod _ { k = 1 } ^ { j - 1 } ( 1 - \alpha _ { k } )
$$

其中 $\alpha_j = o_j \cdot G_j(\pmb{p})$ 为高斯 $j$ 在像素 $\pmb{p}$ 处的有效不透明度，$G_j(\cdot)$ 为高斯核函数值。该公式与颜色渲染完全对称，保证了语义场与几何/外观场的空间一致性。

---

### 帧内-帧间语义一致性目标

为解决跨视角语义不一致问题，引入对比损失 $\mathcal{L}_{CO}$：

$$
\mathcal { L } _ { C O } = \frac { 1 - \lambda _ { r } } { Q } \sum _ { i = 1 } ^ { Q } \mathcal { L } ( \pmb { p } _ { i } ^ { + } ) + \frac { \lambda _ { r } } { R } \sum _ { i = 1 } ^ { R } \mathcal { L } _ { r } ( \pmb { p } _ { i , r } ^ { + } )
$$

- 第一项为**帧内一致性**：对当前帧内属于同一SAM分割掩码的像素对 $(\pmb{p}, \pmb{p}^+)$，拉近其渲染语义特征，推远不同掩码的像素特征。
- 第二项为**帧间一致性**：对跨帧中通过几何投影匹配的像素对 $(\pmb{p}, \pmb{p}_r^+)$ 施加类似对比约束。
- $\lambda_r$ 平衡帧内与帧间权重，$Q$ 和 $R$ 分别为帧内和帧间的正样本对数量。

---

### 语义稳定性引导

利用历史帧中同一3D点投影的语义特征相似度计算置信度权重 $M_{SG}$，对语义损失 $\mathcal{L}_{M,S}$ 进行自适应调制（见 **Figure 3**）。高置信度区域（多帧语义一致）获得更大优化权重，低置信度区域（噪声或遮挡）权重降低，从而抑制2D模型预测噪声对3D语义场的污染。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/003_Figure_3.jpg]]
*Figure 3: Semantic Stability Guidance*

---

### 联合优化目标

建图阶段的总体损失为颜色、深度、语义三项的加权和：

$$
\mathcal { L } _ { m a p p i n g } = \lambda _ { M , C } \mathcal { L } _ { M , C } + \lambda _ { M , D } \mathcal { L } _ { M , D } + \lambda _ { M , S } \mathcal { L } _ { M , S }
$$

其中 $\mathcal{L}_{M,S}$ 已包含语义渲染损失、$\mathcal{L}_{CO}$ 及稳定性引导调制。追踪阶段损失 $\mathcal{L}_{tracking}$ 结构类似，仅优化相机位姿而冻结场景参数。

## 实验与关键发现

### 4.1 实验设置

实验在**Replica**数据集的8个场景上进行，所有方法均在配备**NVIDIA RTX 3090（24 GB显存）**的服务器上运行。为公平比较闭集语义分割性能，我们在所有方法（含基线）的语义特征上添加相同的分类头，并使用Ground Truth标签监督训练。本文方法基于SplaTAM和LoopSplat的公共代码构建，保留原有RGB-D损失与相机追踪设置，仅添加语义模块。

### 4.2 追踪与外观建图性能

Table 1展示了在Replica数据集上的定量结果。以SplaTAM为基座，**SplaTAM+Ours**在渲染质量上取得显著提升：PSNR达到**37.61**，较SplaTAM的34.11提升**+3.50**，较NeRF-based的Point-SLAM（35.17）亦有明显优势。在相机姿态估计上，ATE RMSE降至**0.29**，优于SplaTAM（0.36）和Point-SLAM（0.52）。深度重建方面，Depth L1降至**0.34**，较SplaTAM（0.72）降低0.38。这些结果表明，语义模块的引入不仅未损害几何与外观建图，反而通过语义约束增强了追踪与重建的稳定性。

Figure 4的定性对比进一步验证了渲染质量的提升，本文方法在细节保真度和边缘清晰度上均优于SplaTAM。

### 4.3 闭集语义分割对比

Table 2报告了与现有语义SLAM方法的闭集语义分割对比。**SplaTAM+Ours**以**96.76%**的mIoU大幅领先，较GS³LAM（87.22%）提升**+9.54%**，较SNI-SLAM、SGS-SLAM、Hier-SLAM++等方法均有显著优势。值得注意的是，该性能是在不增加额外分类网络、仅通过可扩展语义池与一致性目标实现的前提下取得的。

### 4.4 开放集语义与3D编辑

在开放集语义分割任务上（Table 3），本文方法取得**66.5%**的2D mIoU，优于基于SfM的GOI方法（59.3%）。Figure 5展示了3D物体定位的定性结果，Figure 6可视化了RGB、深度、开放集与闭集语义的渲染效果。Figure 7进一步展示了基于语义特征的3D编辑能力（颜色修改、平移、旋转、移除），验证了语义表示在场景编辑中的实用性。Figure 8展示了三个手机拍摄的自然场景重建结果，证明了系统在真实日常设备上的泛化能力。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/008_Table_3.jpg]]
*Table 3: Comparisons with SfM-based Open-Set Semantic Methods (§4.4)*

### 4.5 消融实验与分析

**关键组件分析**（Table 4）揭示了各模块的独立贡献：移除所有语义组件（w/o All）导致mIoU降至72.56%，降幅达**-24.20%**；添加帧内-帧间一致性目标（+L_CO）带来**+4.08** mIoU提升；语义稳定性引导（+M_SG）进一步贡献**+3.06** mIoU。三项组件叠加后，mIoU从72.56%恢复至96.76%，验证了设计的协同效应。

**语义特征维度**（Table 5）：当语义特征维度D_s=3时，mIoU已达96.76%，继续增大维度收益递减，表明低维表示足以编码丰富的语义信息。

**语义池设计**（Table 6）：可扩展语义池相比无池方案mIoU高出**+24.20**，相比固定大小的硬索引码本高出**+3.83**，同时训练时间和显存占用均在可接受范围内。这验证了软聚合与动态扩展机制的优越性。

**大规模场景**（Table 7）：在超过24 GB显存的场景中，SGS-SLAM和GS³LAM均因显存不足失败，而本文方法仅需**19.5 GB**显存即可完成建图。Table 12的存储占用分析进一步表明，可扩展池将Room 0的语义存储从直接存储高维特征的数百MB压缩至极小规模，从根本上避免了内存爆炸。

### 4.6 局限性与失败模式

尽管取得了显著进展，当前系统仍存在以下局限：

1. **动态场景鲁棒性不足**：系统主要针对静态场景设计，对物体明显移动等高度动态场景的鲁棒性有限。
2. **大规模场景的池增长**：语义池虽具有自限性（Table 17），但在极大场景中仍可能持续增长，硬件显存最终可能成为瓶颈。
3. **实时性差距**：Table 10的运行时分析显示，追踪和建图速度尚未达到实时要求，难以满足低延迟应用场景。

### 4.7 补充实验

在TUM-RGBD和ScanNet数据集上的补充实验（Table 18、Table 19）进一步验证了方法的泛化能力，在相机姿态估计和渲染性能上均保持了对基线的优势。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/029_Table_18.jpg]]
*Table 18: Quantitative Results on Camera Pose Estimation (supp. §B.2.2) on TUM-RGBD [121] and ScanNet [122] (ATE RMSE↓ [cm])*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_E68dgQUzrC/figures/030_Table_19.jpg]]
*Table 19: Quantitative Comparison on Rendering Performance (supp. §B.2.2) with baselines on TUM-RGBD [121] and ScanNet [122]*

## 定位与知识库关联

### 1. 在3DGS-SLAM与语义SLAM谱系中的位置

本工作处于**3D高斯泼溅SLAM（3DGS-SLAM）** 与**开放集语义建图**的交叉点，属于对现有稠密SLAM框架的语义增强型扩展。

**上游基础框架**：方法直接构建在两个3DGS-SLAM系统之上——**SplaTAM**和**LoopSplat**，保留了其RGB-D损失函数和相机追踪设置，仅在其上添加语义模块。相比更早的NeRF-based稠密SLAM（如**Point-SLAM**），3DGS-based管线在渲染质量和效率上已展现出显著优势。

**语义SLAM谱系定位**：现有语义SLAM方法可分为两类：
- **闭集语义SLAM**：如**GS³LAM**和**SGS-SLAM**（3DGS-based）、**SNI-SLAM**（NeRF-based）、**Hier-SLAM++**（层次化语义SLAM），这些方法将语义限定在预定义类别集合内，每个高斯直接存储高维语义特征向量，无法接纳训练时未见的新语义概念。
- **开放集语义方法**：基于SfM的开放集语义方法（如**GOI**等）虽能处理开放词汇，但缺乏在线SLAM的增量建图能力。

本工作**首次将开放集语义能力引入3DGS-SLAM**，通过可扩展语义特征池实现语义的动态接纳与持续更新，填补了上述两类方法之间的空白。

### 2. 核心差异机制

与传统语义3DGS-SLAM相比，本方法在三个关键维度上做出了结构性改变：

| 设计维度 | 基线方法（GS³LAM/SGS-SLAM等） | 本方法 |
|---------|---------------------------|--------|
| **语义特征表示** | 每个3D高斯直接存储高维语义特征向量 | 维护共享的可扩展语义特征池与键池，每个高斯仅存储低维键，通过近邻软聚合检索语义 |
| **语义更新策略** | 针对固定场景预训练语义，无法动态接纳新语义概念 | 根据输入语义与现有池的相似度判断新颖性，动态插入或扩展语义池 |
| **跨视角一致性** | 无专门处理，2D模型预测在多视点下不一致 | 帧内-帧间语义一致性对比损失 + 语义稳定性引导自适应调制损失权重 |

**关键因果机制**：将场景级语义浓缩到一个小规模的可扩展特征池中，使高斯的语义存储开销从$\mathcal{O}(N \times D)$降至$\mathcal{O}(N \times D_s + |\mathbf{F}_P|)$（其中$D_s \ll D$），这是支持大规模场景和动态语义扩展的底层使能条件。

### 3. 适用边界与局限

**适用场景**：
- 静态室内环境的开放集语义重建与定位
- 需要3D语义编辑（颜色/平移/旋转/移除）的应用
- 日常设备（手机等）采集的自然场景语义建图

**已确认的局限**（论文明确指出的）：
1. **动态场景鲁棒性不足**：当前系统主要针对静态场景设计，对高度动态的场景（如明显物体移动）鲁棒性不足。
2. **大规模场景的语义池增长**：在大规模环境中，语义池虽具有自限性（supp. Table 17），但仍可能持续增长，硬件限制最终可能成为瓶颈。
3. **实时性差距**：运行时效率虽优于部分方法，但追踪和建图不及实时（supp. Table 10），无法满足低延迟应用需求。

### 4. 开放问题与后续方向

1. **动态场景处理**：如何高效处理高度动态或大规模场景中的频繁物体运动？可能的路径包括结合动态感知建图、运动分割或时序语义关联。
2. **表示紧凑化**：能否利用更紧凑的高斯表示进一步降低计算负载，使语义池规模更大，从而覆盖更大场景？
3. **多智能体协作**：如何将系统扩展至多智能体协作SLAM，共享语义池或跨视角语义一致性？这是将开放集语义SLAM推向实际部署的重要方向。
4. **实时性优化**：当前系统的追踪和建图速度仍有较大提升空间，如何在保持语义质量的前提下实现实时或近实时性能，是工程落地需要解决的关键问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Open_Set_Semantic_Gaussian_Splatting_SLAM_with_Expandable_Representation_fa5af39ce6a2.pdf]]
