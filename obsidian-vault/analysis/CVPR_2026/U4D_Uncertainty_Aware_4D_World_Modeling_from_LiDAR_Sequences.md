---
title: "U4D: Uncertainty-Aware 4D World Modeling from LiDAR Sequences"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/U4D_Uncertainty_Aware_4D_World_Modeling_from_LiDAR_Sequences.pdf
project_link: null
code_link: null
aliases:
- U4D
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用预训练LiDAR分割模型输出的逐点香农熵估计空间不确定度图，将其作为结构先验，驱动“由难到易”的两阶段扩散生成：首先生成高不确定度区域的精细几何，再以此为先验条件补全整个场景。这一显式的不确定度引导既改进了局部几何保真度，又提升了全局一致性。
primary_logic: 将不确定度建模嵌入生成框架，先难后易地重建场景，使高不确定度区域成为结构锚点，从而大幅提升几何保真度、时间连贯性和下游分割/校准性能。混合时空（MoST）模块进一步解耦并自适应融合空间与时序特征，保障4D序列的时间稳定性。
claims:
- U4D在nuScenes上的FRD为223.96，显著优于R2DM的253.80，相对提升约11.8%。
- U4D在SemanticKITTI上的FPD为10.92，优于R2DM的12.06。
- U4D在所有帧间隔上的TTCE均最低，表明时间连贯性最优。
- U4D生成的数据在1%标签的nuScenes分割任务上mIoU达到65.3%，超过R2DM的64.1%，提升下游泛化能力。
---

# U4D: Uncertainty-Aware 4D World Modeling from LiDAR Sequences

> [!tip] 核心洞察
> 将不确定度建模嵌入生成框架，先难后易地重建场景，使高不确定度区域成为结构锚点，从而大幅提升几何保真度、时间连贯性和下游分割/校准性能。混合时空（MoST）模块进一步解耦并自适应融合空间与时序特征，保障4D序列的时间稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | U4D：基于不确定度感知的LiDAR序列4D世界建模 |
| 英文题名 | U4D: Uncertainty-Aware 4D World Modeling from LiDAR Sequences |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02982) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | U4D |
| Dataset | nuScenes, SemanticKITTI, KITTI-360 |

> [!tip] 效果简介
> - nuScenes 上，FRD↓ 223.96 vs 253.80 (R2DM) (-11.8%)；FPD↓ 12.90 vs 14.35 (R2DM) (-10.1%)。
> - SemanticKITTI 上，FRD↓ 245.73 vs 262.85 (R2DM) (-6.5%)；FPD↓ 10.92 vs 12.06 (R2DM) (-9.5%)。
> - nuScenes (Temporal) 上，TTCE↓ (interval 3) 2.63 vs 2.65 (LiDARCrafter) (-0.02)。

## 概要

现有LiDAR场景生成方法（如**LiDARGen** (Zyrianov et al., ECCV 2022)、**R2DM** (Nakashima & Kurazume, ICRA 2024)、**LiDM** (Ran et al., CVPR 2024)等）在生成过程中对所有空间区域同等处理，忽视了真实场景中不同位置的不确定度差异——远距离点、遮挡边界、小物体和语义模糊区域天然具有更高的感知难度和几何歧义性。这种“均匀生成”假设导致高不确定度区域出现几何伪影和时间不稳定性，限制了生成数据的可靠性与下游感知任务的泛化能力。

U4D的核心洞察在于：**将不确定度建模显式嵌入生成框架，以“由难到易”的顺序重建场景**——先精细生成高不确定度区域作为结构锚点，再以此为先验条件补全整个场景。具体而言，U4D利用预训练LiDAR分割模型输出的逐点香农熵估计空间不确定度图，驱动一个两阶段扩散生成过程：(1) 第一阶段无条件生成高熵区域的精细几何；(2) 第二阶段以不确定区域为条件补全剩余场景，确保全局一致性。为保障4D序列的时间稳定性，U4D引入**混合时空（Mixture of Spatio-Temporal, MoST）模块**，将特征分解为空间卷积分支和时间卷积分支，通过带随机噪声的自适应门控机制动态融合，并辅以权重正则化防止偏向单一模态。

实验结果表明，U4D在多个基准上显著优于现有方法：在nuScenes数据集上，FRD达到223.96，相较R2DM的253.80相对提升约11.8%；在SemanticKITTI上，FPD为10.92，优于R2DM的12.06；时间一致性指标TTCE在所有帧间隔上均取得最优。更重要的是，U4D生成的数据能有效提升下游语义分割性能（1%标签设定下mIoU达65.3%，超过R2DM的64.1%），并显著降低分割模型的预期校准误差（ECE），提升预测置信度的可靠性。消融实验进一步证实了香农熵不确定度选择策略和MoST自适应融合设计的有效性。



自动驾驶系统对环境的精确感知依赖于高质量的LiDAR点云数据。然而，真实世界的数据采集不仅成本高昂，还面临长尾场景覆盖不足、标注稀缺等瓶颈。近年来，基于扩散模型的LiDAR场景生成方法（如**LiDARGen** (Zyrianov et al., ECCV 2022)、**R2DM** (Nakashima & Kurazume, ICRA 2024)、**LiDM** (Ran et al., CVPR 2024) 等）在合成静态场景方面取得了显著进展，但它们普遍存在一个根本性缺陷：**对所有空间区域同等处理，忽略了真实场景中不同位置的不确定度差异**。

这种“统一生成”假设在实际应用中暴露出严重问题。在距离传感器较远的区域、被部分遮挡的物体边界、小尺度实例以及语义模糊地带，点云的几何结构本身就具有高度不确定性。现有方法对这些区域与近处清晰区域施加相同的生成约束，导致两个关键后果：

1. **几何保真度不足**：高不确定度区域（如远距离点、物体边缘）出现明显的几何伪影和结构失真；
2. **时间稳定性差**：在4D序列生成中，这些区域的帧间一致性难以维持，产生抖动和漂移。

更深层的问题是，这些高不确定度区域恰恰是对下游感知任务（如语义分割、目标检测）最具挑战性的部分。如果生成模型不能在这些区域产生足够逼真且稳定的几何结构，那么合成数据对感知模型的训练增益将大打折扣。

U4D的动机正是源于这一观察：**将不确定度建模显式嵌入生成框架，以“由难到易”的策略重建场景**。其核心直觉在于，如果能让模型优先处理最不确定的区域，并将这些区域的精细几何作为结构锚点，再以此为先验补全整个场景，就能在提升局部保真度的同时增强全局一致性。这一思路将不确定度从需要回避的噪声转化为驱动生成的结构先验，从根本上改变了LiDAR场景生成的范式。



## 核心方法与创新机理

U4D 的核心创新在于将**空间不确定度显式建模**引入 LiDAR 序列生成框架，通过“由难到易”的两阶段扩散策略和混合时空特征融合，系统性地解决了现有方法对全场景同等处理所带来的几何伪影与时间不稳定问题。以下从三个 changed slots 展开其创新机制。

### 空间不确定度估计：从“同等对待”到“难易区分”

现有 LiDAR 生成框架（如 **LiDARGen** (Zyrianov et al., ECCV 2022)、**R2DM** (Nakashima & Kurazume, ICRA 2024)）对所有空间区域施加统一的生成假设，忽略了真实场景中由距离、遮挡、小物体和语义模糊引起的逐点不确定度差异。这种均质化处理使得高不确定度区域（如远距离稀疏点、物体边界）成为几何伪影的集中爆发区。

U4D 的关键突破在于利用预训练 LiDAR 分割模型（默认 RangeNet++）输出的逐点 softmax 概率，通过**香农熵**量化语义不确定度：

$$H(\mathbf{p}) = -\sum_{c=1}^{C} D_c(\mathbf{p}) \log D_c(\mathbf{p})$$

熵值越高，表示该点的语义归属越模糊，对感知任务越具挑战性。U4D 选取 top-K 高熵点构成稀疏不确定点云，再投影到距离图像作为结构先验。消融实验（Table 6）证实，基于香农熵的选择策略在 FRD（223.96）、FPD（12.90）和 ECE（2.72%）上均优于基于距离（Distance）或随机（Random）策略，证明语义不确定度比几何启发式规则更能精准定位生成难点。此外，U4D 对多种分割网络（RangeNet++、MinkUNet、SPVCNN）提取的不确定度均表现出鲁棒性（Table 11），表明该机制不依赖于特定分割模型。

### “由难到易”两阶段扩散：以不确定区域为结构锚点

传统方法采用单阶段扩散直接生成全场景，难以在高不确定度区域分配足够的建模容量。U4D 将生成过程解耦为两个顺序阶段：

1. **不确定区域建模（Stage 1）**：无条件扩散模型 $\epsilon_\theta^u$ 仅在高熵区域的距离图像上训练，专注学习这些“困难区域”的精细几何分布。损失函数在标准噪声预测损失基础上引入掩码监督 $\mathcal{L}_{\mathrm{mask}}$，确保生成的点云严格落在不确定区域内。

2. **不确定度条件补全（Stage 2）**：条件扩散模型 $\epsilon_\theta^c$ 以第一阶段生成的不确定区域 $\mathbf{x}_0^u$ 为输入条件，补全整个场景。通过将 $\mathbf{x}_t$ 与 $\mathbf{x}_0^u$ 沿特征维度拼接，网络将不确定区域作为**结构锚点**，在补全过程中保持全局一致性。

这种“先难后易”的设计使高不确定度区域从“生成负担”转变为“结构引导”，从根本上改变了扩散模型的容量分配方式。Table 1 显示，U4D 在 nuScenes 上的 FRD 达到 223.96，相较 R2DM 的 253.80 提升约 11.8%；在 SemanticKITTI 上 FPD 达到 10.92，优于 R2DM 的 12.06（Table 2），验证了两阶段策略对几何保真度的显著增益。

### 混合时空（MoST）模块：解耦融合保障 4D 一致性

将两阶段扩散从单帧扩展到 4D 序列时，核心挑战在于同时保持帧内几何精度与帧间时间连贯性。U4D 提出**混合时空（Mixture of Spatio-Temporal, MoST）模块**，作为扩散网络的基础构建块。

MoST 将中间特征 $\mathbf{F}_i$ 分解为两个并行分支：**空间卷积分支**捕获帧内几何细节，产生 $\mathbf{F}_i^s$；**时间卷积分支**建模帧间运动与变化，产生 $\mathbf{F}_i^t$。两分支特征拼接后经 MLP 得到共享嵌入：

$$\mathbf{F}_i^{\mathrm{share}} = \mathbb{M}\mathrm{LP}\left( [\mathbf{F}_i^s; \mathbf{F}_i^t] \right)$$

融合权重的关键在于**随机噪声门控机制**：

$$(\alpha_i^s, \alpha_i^t) = \mathsf{Softmax}\big(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^g + \mathbb{I}(\chi \cdot \sigma(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^z))\big)$$

其中 $\chi \sim \mathcal{N}(0,1)$ 为随机噪声，$\mathbb{I}(\cdot)$ 为指示函数。该设计使门控在训练中动态探索不同的融合比例，避免过早陷入局部最优。最终融合特征为：

$$\mathbf{F}_i^{\mathrm{fuse}} = \alpha_i^s \odot \mathbf{F}_i^s + \alpha_i^t \odot \mathbf{F}_i^t$$

为防止门控退化至单一分支，MoST 引入**权重正则化**：

$$\mathcal{L}_{\mathrm{reg}, i} = \frac{\mathrm{Var}(\alpha_i^s)}{(\mathbb{E}[\alpha_i^s])^2} + \frac{\mathrm{Var}(\alpha_i^t)}{(\mathbb{E}[\alpha_i^t])^2}$$

通过惩罚权重的方差-均值比，鼓励空间与时间分支的均衡使用。消融实验（Table 7）表明，自适应融合（Adaptive Fusion）在 FRD（223.96）和 MMD（0.53）上均优于仅空间分支（Spatial-only）或仅时间分支（Temporal-only），且随机噪声和权重正则化各自带来正向贡献。Table 3 进一步证实，U4D 在所有帧间隔上的 TTCE 均最低（间隔 3 时为 2.63），时间连贯性显著优于 **LiDARCrafter** (Liang et al., AAAI 2026) 等 4D 生成方法。

### 创新协同效应

三个 changed slots 形成递进式协同：不确定度估计为生成提供“难易”先验，两阶段扩散利用该先验优化容量分配，MoST 模块则将这种优化从空间维度扩展到时序维度。Table 4 显示，U4D 生成的数据在 1% 标签的 nuScenes 分割任务上使 MinkUNet 的 mIoU 达到 65.3%，超过 R2DM 的 64.1%；Table 5 表明其使分割模型的预期校准误差（ECE）从 4.57% 降至 2.72%，证明不确定度感知的生成能够有效提升下游模型的置信度校准。



U4D 的整体设计围绕一个核心洞察展开：**真实 LiDAR 场景中不同空间位置的不确定度天然存在差异**——远距离点、遮挡边界、小物体和语义模糊区域对感知系统构成更大挑战，而现有生成框架（如 **R2DM** (Nakashima & Kurazume, ICRA 2024)、**LiDARGen** (Zyrianov et al., ECCV 2022) 等）对所有区域同等对待，导致高不确定度区域出现几何伪影和时间不稳定。

为解决这一问题，U4D 采用 **“由难到易”（hard-to-easy）的两阶段级联生成范式**，将不确定度建模显式嵌入生成流程，使高不确定度区域成为结构锚点，驱动全局场景的高保真重建。

### 框架总览

如图 2 所示，U4D 的完整 pipeline 由三个核心阶段串联构成：

1. **空间不确定度估计（Spatial Uncertainty Estimation）**：从预训练 LiDAR 分割模型（默认 RangeNet++）提取逐点语义预测，计算香农熵作为不确定度度量，选取 top-K 高熵点构成稀疏不确定点云，并投影至距离图像（range-view）表示。
2. **不确定区域扩散建模（Uncertainty-Region Diffusion, Stage 1）**：无条件扩散模型在距离图像上学习不确定区域的生成分布，重建高保真几何结构。
3. **不确定度条件补全（Uncertainty-Conditioned Completion, Stage 2）**：条件扩散模型以第一阶段生成的不确定区域为先验，补全剩余场景区域，确保全局结构一致性与空间连贯性。

在整个扩散网络中，U4D 引入 **混合时空模块（Mixture of Spatio-Temporal, MoST）** 作为核心计算单元，将特征分解为空间卷积分支和时间卷积分支，通过带随机噪声的自适应门控机制动态融合，同时配备权重正则化防止偏向单一模态，从而在单帧几何精度与多帧时间连贯性之间取得平衡。

### 输入输出流

- **输入**：真实 LiDAR 扫描序列（多帧点云）。
- **不确定度估计阶段**：输入单帧点云，经预训练分割模型输出逐点语义概率分布，计算香农熵得到不确定度图，选取 top-K 高熵点构成不确定点云 $P^u$，投影为距离图像表示 $\mathbf{x}_0^u$。
- **Stage 1（无条件扩散）**：以不确定区域的距离图像 $\mathbf{x}_0^u$ 为训练目标，从纯噪声 $\mathbf{x}_T^u$ 逐步去噪生成高保真不确定区域 $\hat{\mathbf{x}}_0^u$。
- **Stage 2（条件扩散）**：以完整场景距离图像 $\mathbf{x}_0$ 为目标，将 Stage 1 的输出 $\mathbf{x}_0^u$ 作为条件先验，与含噪输入 $\mathbf{x}_t$ 沿特征维度拼接，引导去噪网络补全整个场景，输出完整距离图像 $\hat{\mathbf{x}}_0$。
- **输出**：4D LiDAR 序列（多帧完整点云），保持几何保真度与时间一致性。

### 关键设计决策

- **不确定度度量的选择**：采用香农熵 $H(\mathbf{p}) = -\sum_{c=1}^{C} D_c(\mathbf{p}) \log D_c(\mathbf{p})$ 而非距离、随机或置信度等替代策略，消融实验证实该选择在 FRD、FPD 和 ECE 上均取得最优（Table 6）。
- **两阶段级联的必要性**：先难后易的生成顺序使不确定区域成为结构锚点，条件扩散模型得以利用这些高保真局部几何引导全局补全，避免统一生成中高不确定区域的伪影扩散。
- **时空解耦融合**：MoST 模块通过独立的空间和时间卷积分支分别捕获帧内几何细节与帧间运动过渡，自适应门控机制根据特征上下文动态调整融合权重，权重正则化项 $\mathcal{L}_{\mathrm{reg}, i} = \frac{\mathrm{Var}(\alpha_i^s)}{(\mathbb{E}[\alpha_i^s])^2} + \frac{\mathrm{Var}(\alpha_i^t)}{(\mathbb{E}[\alpha_i^t])^2}$ 防止门控退化至单一分支。

> **注意**：关于 MoST 模块在网络不同深度的空间/时间偏好分布（近输入输出端侧重空间线索，中间层侧重时间动态）的具体量化分析，原文仅在 Figure 3 的定性描述中提及，需进一步验证其统计显著性。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the U4D framework. U4D generates LiDAR scenes in a “hard-to-easy” manner through two stages. (1) It first estimates spatial uncertainty using a pretrained segmentation model G based on Shannon Entropy, and performs an unconditional diffusion process to reconstruct high-fidelity geometry within the uncertain regions (cf . Sec. 3.1). (2) It then conducts uncertainty-conditioned completion, synthesizing the remaining scene areas guided by the reconstructed structures to ensure global consistency (cf . Sec. 3.2)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the proposed U4D framework for uncertainty-aware LiDAR scene generation. (a) U4D first estimates the spatial uncertainty maps, highlighting regions that are challenging for perception, such as distant or partially occluded objects, smallscale instances, and semantically ambiguous areas. (b) Conditioned on these uncertainty regions, U4D performs scene completion in a “hard-to-easy” manner, progressively reconstructing the entire scene with enhanced fidelity in uncertain regions. (c) The generated uncertainty-aware scenes can further benefit downstream perception tasks by improving robustness and recognition performance*



U4D 的核心设计围绕三个关键模块展开：空间不确定度估计、由难到易的两阶段扩散生成、以及混合时空（MoST）特征融合。以下逐一拆解其公式与变量含义。

### 空间不确定度估计

U4D 利用预训练的 LiDAR 语义分割模型（默认 **RangeNet++**）为每个点输出类别概率分布 $\mathbf{p}$，并通过香农熵量化其语义不确定度：

$$H(\mathbf{p}) = -\sum_{c=1}^{C} D_c(\mathbf{p}) \log D_c(\mathbf{p}) \tag{Eq. 1}$$

其中 $D_c(\mathbf{p})$ 表示点属于类别 $c$ 的 softmax 概率，$C$ 为总类别数。熵值越高，意味着该点的语义归属越模糊——典型场景包括远距离稀疏点、被部分遮挡的物体边界、小尺度实例以及语义歧义区域。随后选取 top-$K$ 高熵点构成稀疏不确定点云 $\mathbf{P}^u$，并将其投影到距离图像（range-view）表示，作为后续扩散生成的结构先验。

### 第一阶段：不确定区域无条件扩散

第一阶段对不确定区域的距离图像 $\mathbf{x}_0^u$ 进行无条件扩散建模。前向加噪过程为标准高斯扩散：

$$q(\mathbf{x}_t^u \mid \mathbf{x}_0^u) = \mathcal{N}(\mathbf{x}_t^u; \sqrt{\bar{\alpha}_t} \mathbf{x}_0^u, (1 - \bar{\alpha}_t) \mathbf{I}) \tag{Eq. 2}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，$\mathbf{x}_t^u$ 为第 $t$ 步的加噪版本。训练目标为预测所加噪声 $\epsilon^u$，并附加掩码监督损失以约束有效区域：

$$\mathcal{L}_u = \mathbb{E}_{t, \mathbf{x}_0^u, \epsilon^u} \left[ \| \epsilon^u - \epsilon_\theta^u(\mathbf{x}_t^u, t) \|_2^2 \right] + \lambda \mathcal{L}_{\mathrm{mask}}(\mathbf{m}^u, \mathbf{m}^p) \tag{Eq. 3}$$

这里 $\epsilon_\theta^u$ 为无条件扩散模型，$\mathbf{m}^u$ 和 $\mathbf{m}^p$ 分别为不确定区域掩码与预测掩码，$\lambda$ 为平衡系数。该阶段的目标是让模型学会生成高保真的不确定区域几何，为后续补全提供“结构锚点”。

### 第二阶段：不确定度条件补全

第二阶段以第一阶段生成的不确定区域 $\mathbf{x}_0^u$ 为条件，补全完整场景 $\mathbf{x}_0$。条件扩散模型的训练损失为：

$$\mathcal{L}_c = \mathbb{E}_{t, \mathbf{x}_0, \epsilon^c} \left[ \lVert \epsilon^c - \epsilon_\theta^c(\mathbf{x}_t, t, \mathbf{x}_0^u) \rVert_2^2 \right] \tag{Eq. 5}$$

其中 $\epsilon_\theta^c$ 为条件扩散模型，$\mathbf{x}_t$ 为完整场景的加噪版本。条件信号 $\mathbf{x}_0^u$ 沿特征维度与 $\mathbf{x}_t$ 拼接，使网络能够同时利用不确定区域的全局结构线索与局部几何细节。通过以不确定区域为条件，模型将这些区域视为结构锚点，确保遮挡、远距离或小尺度物体的准确补全，同时维持全局场景一致性。

### 混合时空（MoST）模块

为在 4D 序列生成中同时保持单帧几何精度与多帧时间连贯性，U4D 在扩散网络内部署了 MoST 模块。该模块将中间特征 $\mathbf{F}_i$ 分解为两个并行分支：空间卷积分支产生 $\mathbf{F}_i^s$，捕获帧内几何细节；时间卷积分支产生 $\mathbf{F}_i^t$，建模帧间运动与演化。

首先通过 MLP 融合两支特征得到共享嵌入：

$$\mathbf{F}_i^{\mathrm{share}} = \mathbb{M}\mathrm{LP}\left( [\mathbf{F}_i^s; \mathbf{F}_i^t] \right) \tag{Eq. 6}$$

其中 $[\cdot;\cdot]$ 表示特征拼接。随后通过带随机噪声扰动的门控机制产生动态融合权重：

$$(\alpha_i^s, \alpha_i^t) = \mathsf{Softmax}\big(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^g + \mathbb{I}(\chi \cdot \sigma(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^z))\big) \tag{Eq. 7}$$

这里 $\mathbf{W}_i^g$ 和 $\mathbf{W}_i^z$ 为可学习权重矩阵，$\sigma$ 为激活函数，$\chi$ 为随机噪声系数，$\mathbb{I}(\cdot)$ 为指示函数控制噪声注入。随机噪声的引入增强了门控的鲁棒性，防止对特定模态的过拟合。

最终的自适应融合为逐元素加权求和：

$$\mathbf{F}_i^{\mathrm{fuse}} = \alpha_i^s \odot \mathbf{F}_i^s + \alpha_i^t \odot \mathbf{F}_i^t \tag{Eq. 8}$$

为防止门控权重过度偏向某一分支，引入方差-均值比正则项：

$$\mathcal{L}_{\mathrm{reg}, i} = \frac{\mathrm{Var}(\alpha_i^s)}{(\mathbb{E}[\alpha_i^s])^2} + \frac{\mathrm{Var}(\alpha_i^t)}{(\mathbb{E}[\alpha_i^t])^2} \tag{Eq. 9}$$

该正则项鼓励空间与时间权重的均衡使用。消融实验证实，自适应融合搭配权重正则化和随机噪声，在 FRD 和 MMD 指标上均优于仅空间或仅时间分支的固定融合方案（Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the Mixture of Spatio-Temporal (MoST) block. It decomposes features along spatial and temporal dimensions and adaptively fuses them to maintain both spatial fidelity and temporal coherence. Near the network input and output, MoST emphasizes spatial cues, while in intermediate layers it focuses more on temporal dynamics*



## 实验与关键发现

### 核心性能：场景级生成质量

U4D在两个主流自动驾驶LiDAR数据集上均取得了最优的场景级生成质量，其核心优势源于“由难到易”的两阶段扩散策略与显式不确定度先验的结合。

**nuScenes数据集**（Table 1）：U4D在衡量几何保真度的FRD指标上达到**223.96**，相比最强基线**R2DM**（Nakashima & Kurazume, ICRA 2024）的253.80降低了约11.8%；在FPD指标上为12.90，优于R2DM的14.35（降低约10.1%）。这表明不确定度引导的生成策略有效减少了远距离、遮挡区域和小物体的几何伪影。与单帧生成器**LiDARGen**（Zyrianov et al., ECCV 2022）、**LiDM**（Ran et al., CVPR 2024）及序列生成器**UniScene**（Li et al., CVPR 2025）、**OpenDWM**（Ni et al., CVPR 2025）相比，U4D在所有指标上均表现领先。

**SemanticKITTI数据集**（Table 2）：U4D的FRD为245.73（R2DM为262.85，降低约6.5%），FPD为10.92（R2DM为12.06，降低约9.5%）。跨数据集的稳定提升验证了不确定度先验的泛化能力——该先验由预训练分割模型自动提取，不依赖数据集特定的手工设计。

**KITTI-360数据集**（Table 9）：U4D的FRD为142.53，显著优于R2DM的157.42（降低约9.5%），进一步支持上述结论。

### 时间一致性：4D序列生成的关键突破

LiDAR序列生成的核心挑战在于保持跨帧的时间连贯性。U4D通过混合时空（MoST）模块，在时间一致性指标TTCE上取得了最优结果（Table 3）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/008_Table_3.jpg]]
*Table 3: Comparison of temporal consistency in 4D LiDAR scene generation on the nuScenes [8] dataset. Metrics marked with ↓ indicate that lower values are better. The best and second-best scores are highlighted in bold and underline, respectively. Numbers denote frame intervals*

在帧间隔为3和4的设置下，U4D的TTCE分别为**2.63**和**3.51**，均低于**LiDARCrafter**（Liang et al., AAAI 2026）和R2DM。MoST模块将特征分解为空间卷积分支（捕获单帧几何细节）和时间卷积分支（建模跨帧动态），并通过带随机噪声的自适应门控机制动态融合。消融实验（Table 7）证实，自适应融合（Adaptive Fusion）在FRD和MMD上均优于仅空间分支（Spatial-only）或仅时间分支（Temporal-only）的设计，且权重正则化（$\mathcal{L}_{\mathrm{reg}}$）和随机噪声模块均有正面贡献。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/013_Table_7.jpg]]
*Table 7: Ablation study on the design of the MoST block on the nuScenes [8] dataset. Metrics marked with ↓ indicate that lower values are better. The MMD scores are reported in units of*

定性结果（Figure 4）显示，U4D生成的序列在远距离稀疏区域和动态物体（如行驶车辆）的跨帧运动轨迹上均与真实扫描高度一致，而基线方法在这些区域常出现点云抖动或几何断裂。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of sequence point cloud generation on the nuScenes dataset [8]. U4D preserves both geometric fidelity and temporal consistency, producing sequences most similar to the reference. It reliably reconstructs distant, sparse regions and captures dynamic objects across frames, maintaining coherent structure and motion. Frames are shown in temporal order from left to right. The ectory" : [ { "is_loop" :colors are rendered based on the height information of the point cloud. Best viewed in zoom*

### 下游任务泛化：从生成质量到感知增益

U4D生成的数据对下游语义分割任务具有显著的增强效果。

**半监督分割**（Table 4）：在nuScenes的1%标签设定下，使用U4D生成数据作为无标签扩充后，基于Voxel表示的MinkUNet mIoU达到**65.3%**，超过R2DM的64.1%和半监督方法**LaserMix**（Kong et al., CVPR 2023）的63.5%。在50%标签设定下，U4D的mIoU为76.4%，同样保持领先。这表明U4D生成的不确定度感知数据为分割模型提供了更有信息量的训练信号，尤其改善了原本难以标注或感知困难的区域。

**模型校准**（Table 5）：U4D生成的数据使RangeNet++在nuScenes上的预期校准误差（ECE）从无校准的4.57降至**2.72**，在SemanticKITTI上从5.19降至3.69。ECE的降低意味着分割模型的预测置信度更加可靠，这对安全关键的自动驾驶应用至关重要。

### 消融实验：不确定度策略与模块设计的因果验证

**不确定区域选择策略**（Table 6）：对比香农熵（Entropy）、基于距离（Distance）、随机选择（Random）和无不确定度（w/o Uncertainty）四种策略，香农熵在FRD（223.96）、FPD（12.90）和ECE（2.72）上均取得最优。基于距离的策略（选择远距离点）优于随机，但远不如香农熵有效，说明语义模糊性（而不仅仅是几何稀疏性）是生成困难的核心来源。

**不确定区域比例**（Table 10）：在nuScenes上选择top-20%熵最高点作为不确定区域达到最优FRD/FPD。比例过低则先验信息不足，过高则引入噪声。

**分割模型鲁棒性**（Table 11）：使用RangeNet++、MinkUNet和SPVCNN三种不同分割模型提取不确定度图，U4D的性能保持稳定，说明该方法对不确定度估计的具体实现不敏感。

**推理效率**（Table 8）：U4D单帧推理时间为8.9秒，虽高于单帧生成器（如R2DM的0.3秒），但显著低于其他序列生成器（如UniScene的47.9秒）。在序列生成质量和推理效率之间取得了有利权衡。

### 失败模式与局限性

尽管U4D在多数场景下表现优异，论文明确指出以下局限：

1. **稀有事件复现困难**：训练集中极少出现的特殊车辆、罕见基础设施或高度复杂的动态场景（如多车交互、异常行人行为）难以准确生成。这是数据驱动生成模型的共性瓶颈。
2. **推理延迟较高**：两阶段扩散过程导致单帧8.9秒的推理时间，无法直接部署到实时或车载系统。可能的加速方向包括模型蒸馏、减少采样步数或稀疏化扩散过程。
3. **序列长度有限**：当前生成序列长度约为10帧，更长时域的几何和时间一致性保持需要进一步探索，特别是物体运动轨迹的长期稳定性。

这些局限为后续研究提供了明确方向：如何将生成跨度扩展至数十帧、如何通过联合学习优化不确定度估计、以及如何在保持生成质量的前提下实现近实时推理。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/004_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art LiDAR scene generation methods on the nuScenes [8] dataset. Metrics marked with ↓ indicate that lower values are better. The MMD scores are reported in units of*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/006_Table_2.jpg]]
*Table 2: Comparison of state-of-the-art LiDAR scene genera-324707 ], "boundingbtion methods on the SemanticKITTI [5] dataset. Metrics marked 9208984, -74.877586364746094, -4.26646566with ↓ indicate that lower values are better. The MMD scores are d_of_view" : 60.0, "froreported in units of 10−4. The best and second-best scores are highlighted in bold and underline, respectively*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/007_Table_4.jpg]]
*Table 4: Comparison of state-of-the-art methods on the downin" : [ -.785427093505859, 79.18359375, 11.9471302stream task of LiDAR semantic segmentation on the val set of the 99121 ], "boundingbox_min" : nuScenes [8] dataset. The voxel- and fusion-based representations are built upon MinkUNet [13] and SPVCNN [91] as backbones, respectively. The mIoU scores are reported in percentage (%). The "lookat" : 64656639099121 ],best and second-best results within each data split and representa-95075 ]"fi ld f i " 60 0tion are highlighted in bold and underline, respectively*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/010_Table_5.jpg]]
*Table 5: Expected calibration error (ECE, the lower the better) of various LiDAR semantic segmentation methods on the validation set of the nuScenes [5] and SemanticKITTI [5] datasets. The ECE scores are reported in percentage (%)*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/012_Table_6.jpg]]
*Table 6: Ablation study on the selection of uncertainty regions on nuScenes [8]. Metrics marked with ↓ indicate that lower values are better. The MMD scores are reported in units of*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2512_02982/figures/011_Table_8.jpg]]
*Table 8: Ablation study on the efficiency of generative models. The table reports the average inference time per frame (I.T., in seconds). “DM” refers to the diffusion model*



## 定位与知识库关联

### 问题谱系：从2D/3D生成到4D世界建模

自动驾驶场景的LiDAR点云生成经历了从单帧建模到序列生成的演进。早期工作聚焦于单帧LiDAR场景的生成式建模，如**LiDARGen**（Zyrianov et al., ECCV 2022）首次将去噪扩散概率模型引入距离图像生成，**R2DM**（Nakashima & Kurazume, ICRA 2024）通过距离-反射率联合扩散提升了场景保真度，**LiDM**（Ran et al., CVPR 2024）和**Text2LiDAR**（Wu et al., ECCV 2024）则分别从潜在空间建模和文本条件控制角度推进了生成质量。这些方法的共同假设是：场景中所有空间区域应被同等对待，生成过程不区分“难易”。

然而，真实LiDAR扫描存在显著的空间异质性——远距离点稀疏、遮挡区域几何缺失、小物体边界模糊、语义混淆区域（如行人-自行车）的类别不确定性高。统一生成策略在这些“高不确定度”区域容易产生几何伪影、缺失细节或引入时间不稳定性。**U4D**的核心洞察在于：将不确定度显式建模为结构先验，驱动“由难到易”的生成顺序，使高不确定度区域成为场景重建的锚点。

### 知识库定位：不确定度感知的4D生成

相较于现有工作，U4D在三个关键维度上进行了方法创新：

**（1）空间不确定度估计与先验注入。** 现有LiDAR生成框架（如R2DM、LiDM）不使用空间不确定度先验，对所有区域施加统一的扩散损失。U4D利用预训练分割模型（默认RangeNet++）输出的逐点香农熵 $H(\mathbf{p}) = -\sum_{c=1}^{C} D_c(\mathbf{p}) \log D_c(\mathbf{p})$ 估计空间不确定度图，选取top-K高熵点构成不确定区域。这一设计的合理性在于：语义熵天然捕获了感知模型在特定空间位置的“困惑度”，这些位置恰好是生成模型最容易失败的几何薄弱点。

**（2）“由难到易”的两阶段扩散生成。** 传统方法采用单阶段全场景扩散（如LiDARGen、R2DM），U4D将其分解为两个顺序阶段：第一阶段无条件扩散在距离图像上学习不确定区域的生成分布 $q(\mathbf{x}_t^u \mid \mathbf{x}_0^u) = \mathcal{N}(\mathbf{x}_t^u; \sqrt{\bar{\alpha}_t} \mathbf{x}_0^u, (1 - \bar{\alpha}_t) \mathbf{I})$，生成高保真几何；第二阶段以不确定区域为条件 $\mathcal{L}_c = \mathbb{E}_{t, \mathbf{x}_0, \epsilon^c} [ \lVert \epsilon^c - \epsilon_\theta^c(\mathbf{x}_t, t, \mathbf{x}_0^u) \rVert_2^2 ]$ 补全整个场景。这种“先难后易”的策略使不确定区域成为结构锚点，约束全局一致性。

**（3）混合时空（MoST）自适应融合。** 4D序列生成需要同时保持单帧几何精度和多帧时间连贯性。U4D提出的MoST模块将特征分解为空间卷积分支 $\mathbf{F}_i^s$ 和时间卷积分支 $\mathbf{F}_i^t$，通过共享嵌入 $\mathbf{F}_i^{\mathrm{share}} = \mathbb{M}\mathrm{LP}( [\mathbf{F}_i^s; \mathbf{F}_i^t] )$ 和带随机噪声的门控机制 $(\alpha_i^s, \alpha_i^t) = \mathsf{Softmax}(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^g + \mathbb{I}(\chi \cdot \sigma(\mathbf{F}_i^{\mathrm{share}}\cdot\mathbf{W}_i^z)))$ 自适应融合，辅以权重正则化 $\mathcal{L}_{\mathrm{reg}, i} = \frac{\mathrm{Var}(\alpha_i^s)}{(\mathbb{E}[\alpha_i^s])^2} + \frac{\mathrm{Var}(\alpha_i^t)}{(\mathbb{E}[\alpha_i^t])^2}$ 防止偏向单一模态。这与同期4D生成方法**LiDARCrafter**（Liang et al., AAAI 2026）和**UniScene**（Li et al., CVPR 2025）形成差异化——后者未显式建模空间不确定度，也未采用自适应时空融合。

### 适用边界与局限

U4D的有效性依赖于以下前提条件，这些条件也划定了其适用边界：

1. **预训练分割模型的可用性。** 不确定度估计依赖预训练分割模型（如RangeNet++）的语义预测质量。当目标域与分割模型训练域存在显著分布偏移时（如极端天气、非结构化环境），香农熵可能无法准确反映真实的几何生成难度。消融实验（Table 11）表明U4D对多种分割网络（RangeNet++、MinkUNet、SPVCNN）具有鲁棒性，但该结论仅在nuScenes/KITTI等标准自动驾驶数据集上验证，泛化至域外场景需谨慎。

2. **稀有事件的生成保真度。** 论文明确指出U4D难以准确复现训练集中极端稀有事件（如特殊车辆、罕见基础设施）或高度复杂的动态场景。这是扩散模型基于数据分布建模的固有局限——低频模式的训练信号不足，导致生成样本偏向常见模式。

3. **推理效率与实时性。** 两阶段扩散过程导致单帧推理时间约8.9秒（Table 8），虽显著低于UniScene的47.9秒，但远高于单帧生成器R2DM的0.3秒。这一延迟使其难以直接部署到实时或车载系统，当前更适合离线数据增强场景。

4. **序列长度限制。** 当前生成序列长度约为10帧，更长时域的几何和时间一致性保持仍是开放问题。随着帧间隔增大，TTCE指标虽仍最优但绝对数值上升（Table 3：间隔3为2.63，间隔4为3.51），表明长时域建模的退化趋势。

### 开放问题

从U4D的局限出发，可识别以下值得探索的方向：

- **不确定度估计的端到端学习。** 当前不确定度来自固定的预训练分割模型，能否将不确定度估计与生成过程联合学习？这有望发现更有利于生成（而非仅感知）的不确定区域，突破语义熵的固有局限。

- **推理效率的实质性提升。** 能否通过模型蒸馏、减少扩散采样步数（如一致性模型）或稀疏化扩散过程，将推理延迟压缩至秒级以内？这对于U4D从离线数据增强走向在线应用至关重要。

- **长序列生成的稳定性。** 如何将生成跨度扩展至数十帧甚至更长，同时保持物体运动轨迹的物理合理性和场景演化的时间一致性？这可能需要在MoST模块中引入更显式的运动建模或循环一致性约束。

- **域外泛化与稀有事件生成。** 如何提升对训练分布尾部的覆盖能力？可考虑引入检索增强生成（从训练集中检索相似稀有事件作为条件）或物理仿真先验来补充数据驱动建模的不足。



## 原文 PDF

![[paperPDFs/CVPR_2026/U4D_Uncertainty_Aware_4D_World_Modeling_from_LiDAR_Sequences.pdf]]
