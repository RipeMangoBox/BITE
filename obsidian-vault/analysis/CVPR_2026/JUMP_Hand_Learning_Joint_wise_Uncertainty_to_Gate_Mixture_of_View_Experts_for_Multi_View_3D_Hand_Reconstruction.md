---
title: "JUMP-Hand: Learning Joint-wise Uncertainty to Gate Mixture of View Experts for Multi-View 3D Hand Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/JUMP_Hand_Learning_Joint_wise_Uncertainty_to_Gate_Mixture_of_View_Experts_for_Multi_View_3D_Hand_Reconstruction.pdf
project_link: null
code_link: "https://github.com/HaohongKuang/JUMP-Hand"
aliases:
- JH
- JUMP-Hand
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入关节级的概率不确定性作为显式门控信号，在粗到细的重建流程中动态地按关节加权各个视图专家的贡献。
primary_logic: 预测的不确定性能够显式量化各视图对每个关节的观测可靠性，从而将多视图融合自然地转化为MoE路由问题，无需依赖黑盒注意力。
claims:
- JUMP-Hand 首次引入概率性的关节级不确定性作为显式、可物理解释的门控信号。
- 在 HO3D-MV 全量测试集上，JUMP-Hand 的 MPVPE 为 13.39 mm，相较 POEM 的 17.20 mm 降低 22.2%。
- 在 HO3D-MV 挑战子集上，JUMP-Hand 的 MPVPE 为 24.91 mm，对比 POEM 的 35.52 mm 实现了 29.9% 的提升。
- 消融实验表明，移除粗阶段或细化阶段均导致显著性能下降（粗阶段移除 +8.45 mm），证明了粗到细的不确定性门控设计的有效性。
---

# JUMP-Hand: Learning Joint-wise Uncertainty to Gate Mixture of View Experts for Multi-View 3D Hand Reconstruction

> [!tip] 核心洞察
> 预测的不确定性能够显式量化各视图对每个关节的观测可靠性，从而将多视图融合自然地转化为MoE路由问题，无需依赖黑盒注意力。

| 字段 | 内容 |
|------|------|
| 中文题名 | JUMP-Hand：学习关节级不确定性以门控混合视图专家的多视角三维手部重建 |
| 英文题名 | JUMP-Hand: Learning Joint-wise Uncertainty to Gate Mixture of View Experts for Multi-View 3D Hand Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kuang_JUMP-Hand_Learning_Joint-wise_Uncertainty_to_Gate_Mixture_of_View_Experts_CVPR_2026_paper.html) · [Code](https://github.com/HaohongKuang/JUMP-Hand) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | JUMP-Hand |
| Dataset | HO3D-MV, DexYCB-MV 挑战子集, OakInk-MV 挑战子集 |

> [!tip] 效果简介
> - HO3D-MV 上，MPVPE (mm) 13.39 vs 17.20 (POEM) (-3.81 (-22.2%))；MPJPE (mm) 13.10 vs 17.28 (POEM) (-4.18 (-24.2%))。
> - HO3D-MV 挑战子集 上，MPVPE (mm) 24.91 vs 35.52 (POEM) (-10.61 (-29.9%))。
> - DexYCB-MV 挑战子集 上，MPVPE (mm) 10.37 vs 13.88 (POEM) (-3.51 (-25.3%))。

## 概述

多视角三维手部重建的核心挑战在于如何有效融合来自不同视角的特征。现有方法普遍采用平均池化或隐式注意力对所有视图进行无差别聚合，忽略了一个关键事实：**同一手部关节在不同视图中的可见性与观测可靠性存在显著差异**。当部分视图因遮挡、运动模糊或手部缺失而产生不可靠信息时，无差别融合会将这些噪声注入最终重建结果，形成性能瓶颈。

针对这一瓶颈，JUMP-Hand 提出了一种可物理诠释的解决方案——**将概率性的关节级不确定性作为显式门控信号**，动态调控各视图对每个关节的贡献。该方法将多视图融合重新定义为混合专家（Mixture-of-Experts, MoE）路由问题：每个视图被视为一个独立专家，网络预测的关节级不确定性量化了各专家对特定关节的观测可靠性，进而指导特征聚合与三角化过程。这一设计使融合机制从黑盒注意力转向透明、可解释的不确定性驱动门控。

JUMP-Hand 的整体架构遵循**粗到细两阶段流程**：粗阶段通过不确定性引导的直接线性变换（UG-DLT）生成稳健的三维初始化；细化阶段以迭代 Transformer 解码器逐层精修，其核心模块——不确定性门控交叉注意力（UGCA）——在每个解码层中按关节加权融合多视图专家特征。

在 HO3D-MV、DexYCB-MV 和 OakInk-MV 三个多视图手部重建基准上，JUMP-Hand 均以显著优势超越现有方法。在 HO3D-MV 全量测试集上，MPVPE 达到 13.39 mm，相较此前最优方法 **POEM**（Yang et al., CVPR 2023）的 17.20 mm 降低 22.2%；在更具挑战性的子集上，提升幅度扩大至 29.9%（24.91 mm vs. 35.52 mm）。消融实验进一步验证了不确定性门控与粗到细设计的必要性：移除粗阶段导致 MPJPE 从 13.10 mm 升至 21.55 mm（+8.45 mm），而无门控的平均池化方案同样造成显著退化。定性结果表明，JUMP-Hand 在运动模糊、严重遮挡和缺失视图等极端条件下仍能恢复准确、完整的手部几何。

**方法谱系与知识库定位**：JUMP-Hand 处于多视图三维手部重建与概率建模的交汇点。相较于依赖确定性热图回归与等权三角化的 **Zhang et al.**（NeurIPS 2021）、**Spectral Graphormer**（Tse et al., ICCV 2023）以及 **MLPHand**（Yang et al., ECCV 2024），JUMP-Hand 的核心创新在于将二维关节观测建模为高斯分布，并利用预测方差驱动整个融合管线。与通用 MoE 路由中常见的 Top-k 硬选择不同，JUMP-Hand 的软门控机制保留所有视图专家的加权贡献，实验证明这一策略在所有数据集上均优于硬门控。该方法的不确定性建模目前基于单模态高斯假设，处理严重遮挡引起的多模态歧义性仍是待探索的开放问题。

## 背景与动机

### 问题背景

从多视角图像中恢复精确的三维手部几何是计算机视觉中的一个核心问题，在虚拟现实、人机交互和机器人遥操作等领域具有广泛的应用需求。与单目重建相比，多视角设置提供了互补的观测信息，理论上可以缓解深度歧义和自遮挡等固有挑战。然而，如何有效整合多个视角的信息以产生一致且准确的三维重建，仍然是一个开放性问题。

### 现有方法的瓶颈

现有多视图手部重建方法（如 **POEM** Yang et al., CVPR 2023；**MLPHand** Yang et al., ECCV 2024；**Spectral Graphormer** Tse et al., ICCV 2023）通常采用无差别的特征聚合策略——平均池化或隐式注意力——将所有视图的特征等权或黑盒地融合。这一做法隐含了一个不成立的假设：每个手部关节在所有视图中具有同等的可见性和可靠性。

然而，在实际多视角设置中，不同手部关节在不同视图中的观测质量存在显著差异：某些关节可能因自遮挡、物体遮挡或视角边缘化而严重退化，甚至完全不可见。无差别地聚合这些不可靠视图的信息，会导致其污染整体融合结果，使重建精度受限于最差观测视图的质量。这一瓶颈构成了现有多视图手部重建方法性能上限的核心制约因素。

### 核心动机与研究直觉

本文的核心动机源于一个关键观察：多视图融合的本质问题可以自然地重新表述为**混合专家（Mixture-of-Experts, MoE）问题**。在此框架下：

- 每个相机视图被视为一个独立的“专家”，对每个手部关节提供特定的观测信息；
- 不同视图专家对同一关节的贡献应当根据其观测可靠性进行差异化加权；
- 需要一个显式、可物理解释的路由信号来动态调控各专家的参与程度。

Figure 1 直观展示了这一研究直觉：(a) 手部关节在不同视图中的可靠性存在显著差异；(b) 将多视图三维手部重建任务重新定义为 MoE 任务，将不同视图视为不同专家；(c) 利用预测的不确定性作为门控信号来调控视图专家之间的融合。

### 方法核心思路

基于上述动机，本文提出 **JUMP-Hand**，首次引入**概率性的关节级不确定性**作为显式、可物理解释的门控信号。具体而言：

1. **关节级不确定性建模**：将每个二维关节观测建模为高斯变量，联合预测其位置均值和协方差，从而显式量化各视图对每个关节的观测可靠性；
2. **不确定性引导的粗到细重建**：将预测的不确定性作为门控信号，贯穿粗初始化（不确定性引导三角化）和细化阶段（不确定性门控交叉注意力），实现按关节、按视图的动态加权融合。

这一设计的核心优势在于：预测的不确定性能够显式量化各视图对每个关节的观测可靠性，从而将多视图融合自然地转化为 MoE 路由问题，无需依赖黑盒注意力机制。通过这种方式，JUMP-Hand 能够在保持高计算效率的同时，显著提升对遮挡、运动模糊和缺失视图等挑战性条件的鲁棒性。

## 核心创新

### 瓶颈重定义：从无差别融合到关节级可靠性感知

现有多视图手部重建方法（如 **POEM** (Yang et al., CVPR 2023)、**MLPHand** (Yang et al., ECCV 2024)）在融合多视图特征时，通常采用平均池化或隐式注意力机制，无差别地聚合所有视图的信息。这一范式忽略了一个关键物理事实：**手部各关节在不同视图中的可见性和观测可靠性存在显著差异**。当某一视图中特定关节被遮挡或处于极端视角时，该视图对该关节的观测是不可靠的，强行将其纳入融合反而会污染整体重建结果。JUMP-Hand 的核心洞察在于：**将多视图融合天然地重新定义为混合专家（Mixture-of-Experts, MoE）路由问题**——每个视图被视为一个“专家”，而融合的关键在于为每个关节动态地决定各专家的贡献权重（Figure 1）。

### 因果旋钮：概率不确定性作为显式门控信号

JUMP-Hand 的核心技术贡献是**首次引入概率性的关节级不确定性作为显式、可物理解释的门控信号**（论文明确声明 `"the first method to introduce probabilistic, joint-wise uncertainty as an explicit, physically-interpretable gating signal"`）。这一设计构成了三个紧密耦合的 changed slots：

**1. 2D关节表示：从确定性热图到概率高斯建模**

传统方法将2D关节位置建模为确定性热图回归。JUMP-Hand 将其替换为概率高斯建模，每个关节的2D观测被表示为：
$$\mathbf{p}_{j,n}^{2D} \sim \mathcal{N}(\pmb{\mu}_{j,n}, \pmb{\Sigma}_{j,n})$$
其中均值 $\pmb{\mu}_{j,n}$ 由热力图头预测，对角协方差 $\pmb{\Sigma}_{j,n}$ 由方差头预测。方差 $\sigma_{j,n}^2$ 直接量化了该视图对该关节的观测不确定性——高方差意味着该视图对该关节的定位不可靠。这一设计使得不确定性具有明确的物理含义，而非黑盒学习出的抽象权重。

**2. 三角化方法：从等权DLT到不确定性引导DLT (UG-DLT)**

标准直接线性变换（DLT）假设所有视图的2D观测等权贡献。JUMP-Hand 从概率视角重新形式化三角化过程，提出 UG-DLT：
$$(\mathbf{w}_j \circ \mathbf{A}_j) \mathbf{J}_j^{3D,(0)} = \mathbf{0}$$
其中权重 $\mathbf{w}_j$ 由不确定性转换而来：$\alpha_{j,n} = \frac{\exp(-\sigma_{j,n}^2)}{\sum_{m=1}^N \exp(-\sigma_{j,m}^2)}$。高不确定性视图的约束被显式抑制，使得粗3D初始化对遮挡和噪声更加鲁棒。

**3. 多视图特征融合：从隐式注意力到不确定性门控交叉注意力 (UGCA)**

在细化阶段，JUMP-Hand 以 UGCA 替代传统的隐式注意力融合。各视图通过可变形注意力提取关节附近的特征 $y_{j,n}$，然后使用不确定性权重进行加权融合：
$$y_j = \sum_{n=1}^N \alpha_{j,n} \cdot y_{j,n}$$
这一设计将不确定性信号从2D观测端一致地传递到3D特征融合端，实现了**粗到细两阶段的不确定性门控**。

### 设计逻辑链

三个 changed slots 形成了一条因果闭环：**概率2D建模产生不确定性 → UG-DLT利用不确定性生成鲁棒粗初始化 → UGCA利用不确定性门控细化特征融合**。消融实验提供了强因果证据：移除粗阶段导致 MPJPE 从 13.10 mm 升至 21.55 mm（+8.45 mm），移除细化阶段升至 16.61 mm（+3.51 mm），验证了粗到细不确定性门控设计的必要性（Table 3）。软门控（使用所有视图专家）在所有数据集上优于硬门控（Top-k选择），证明保留低置信度视图的部分信息比完全丢弃更有益（Table 4）。

### 与现有方法的本质差异

与依赖黑盒注意力学习融合权重的方法（如 **Spectral Graphormer** (Tse et al., ICCV 2023)）不同，JUMP-Hand 的门控信号来自显式的概率建模，具有可解释性——可视化的不确定性椭圆与门控权重直接对应（Figure 3）。这种设计使得方法在运动模糊、严重遮挡和缺失视图等极端条件下仍能恢复准确的3D手部几何（Figure 5），在 HO3D-MV 挑战子集上相较 POEM 实现了 29.9% 的 MPVPE 提升（24.91 mm vs 35.52 mm）。

## 整体框架

JUMP-Hand 将多视角三维手部重建重新定义为**粗到细的混合视图专家（Mixture-of-Experts, MoE）架构**，其核心创新在于将每个视角视为一个独立的“专家”，并通过**关节级概率不确定性**作为显式门控信号来动态融合各视图专家的贡献。整体流程如图2所示。

**输入与输出**：给定 $N$ 个同步的多视角RGB图像 $\boldsymbol{\mathcal{T}} = \{ \mathbf{I}_i \}_{i=1}^{N}$，方法的目标是恢复MANO手部模型的21个三维关节坐标 $\mathbf{J}_{3D} \in \mathbb{R}^{21 \times 3}$ 及对应的网格顶点。

**Pipeline 三阶段**：

1. **关节级不确定性建模（Joint-wise Uncertainty Modeling）**：每个视图通过共享的ResNet-34骨干网络提取多尺度特征，经FPN后分别由热力图头和方差头预测各关节的二维位置均值 $\pmb{\mu}_{j,n}$ 与对角协方差 $\pmb{\Sigma}_{j,n}$，显式量化每个视角对每个关节的观测可靠性。这一概率建模是后续所有门控信号的数据来源。

2. **不确定性引导三角化（Uncertainty-Guided DLT, UG-DLT）**：将预测的方差转换为归一化权重 $\alpha_{j,n}$，对标准DLT约束矩阵进行逐元素加权，抑止低可靠性视图对三角化的影响，生成稳健的粗三维关节初始化 $\hat{\mathbf{J}}^{3D,(0)}$。这是**粗阶段**的核心。

3. **不确定性门控迭代精修（Uncertainty-Gated Iterative Refinement）**：以粗三维关节和顶点作为初始查询，通过 $L$ 层堆叠的Transformer解码器迭代精修。每层中，**不确定性门控交叉注意力（UGCA）** 是细化的核心模块——它利用多尺度可变形注意力从各视图的二维投影点附近采样特征，再以关节级不确定性权重 $\alpha_{j,n}$ 对各视图专家响应进行加权求和，实现按关节、按视图的自适应特征融合。融合特征经FFN和MLP回归头预测坐标更新量，逐层逼近精确三维结构。

**数据流与模块关系**：不确定性估计分支的输出同时服务于粗阶段的UG-DLT和细阶段的UGCA，形成统一的“概率建模→门控信号→几何推理”闭环。这种设计避免了黑盒注意力机制，使得多视图融合过程在物理上可解释：高不确定性的视图对特定关节的贡献被自动抑制，而可靠的视图信息被保留和增强。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of JUMP-Hand. (a) Joint-wise uncertainty modeling: each view independently predicts 2D joint locations and uncertainties*

## 核心模块与公式推导

JUMP-Hand 的核心创新在于将多视图融合重新表述为**混合视图专家（Mixture of View Experts）**问题，并通过**关节级概率不确定性**作为显式门控信号来驱动整个粗到细的重建流程。整个流水线（Figure 2）包含五个关键模块，按信息流顺序展开如下。

### 3.1 关节级不确定性建模

与传统的确定性热图回归不同，JUMP-Hand 将每个视图 $n$ 中每个关节 $j$ 的 2D 观测建模为**高斯随机变量**：

$$\mathbf{p}_{j,n}^{2D} \sim \mathcal{N}(\pmb{\mu}_{j,n}, \pmb{\Sigma}_{j,n})$$

其中 $\pmb{\mu}_{j,n} \in \mathbb{R}^2$ 为预测均值（代表最可能的位置），$\pmb{\Sigma}_{j,n} = \text{diag}(\sigma_{j,n,x}^2, \sigma_{j,n,y}^2)$ 为对角协方差矩阵（量化该视图对该关节的观测不确定性）。这一概率建模使得网络能够显式输出每个视图对每个关节的**可靠性置信度**，而非依赖黑盒注意力隐式学习。

具体实现上，共享 CNN 骨干网络（ResNet-34）从各视图提取多尺度特征 $\mathbf{F}_n$ 后，通过 FPN 增强特征表达，再分别送入两个独立分支：

$$\pmb{\mu}_{j,n} = \mathcal{H}(\text{FPN}(\mathbf{F}_n)), \quad \pmb{\Sigma}_{j,n} = \mathcal{V}(\text{FPN}(\mathbf{F}_n))$$

其中 $\mathcal{H}$ 为热力图头（预测均值），$\mathcal{V}$ 为方差头（预测对角线方差）。**Figure 3** 以椭圆形式可视化了各关节的不确定性分布，直观展示了不同视图对同一关节的观测可靠性差异——这正是门控信号设计的物理依据。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/003_Figure_3.jpg]]
*Figure 3: (a) Visualization of uncertainty. The joint-wise ellipses display the standard deviation in two directions. (b) Corresponding joint-wise gating weights*

### 3.2 不确定性引导的粗重建（UG-DLT）

传统直接线性变换（DLT）假设所有视图等权贡献，在遮挡或模糊场景下容易受不可靠视图污染。JUMP-Hand 从概率视角重新推导了三角化过程，提出**不确定性引导 DLT（Uncertainty-Guided DLT）**。

首先将预测方差转换为归一化的门控权重：

$$\alpha_{j,n} = \frac{\exp(-\sigma_{j,n}^2)}{\sum_{m=1}^N \exp(-\sigma_{j,m}^2)}$$

其中 $\sigma_{j,n}^2 = \frac{1}{2}(\sigma_{j,n,x}^2 + \sigma_{j,n,y}^2)$ 为各向同性方差近似。该 softmax 归一化确保高方差（低可靠性）视图获得指数级衰减的权重，而低方差（高可靠性）视图主导融合。

随后将权重注入 DLT 约束矩阵的逐元素加权：

$$(\mathbf{w}_j \circ \mathbf{A}_j) \mathbf{J}_j^{3D,(0)} = \mathbf{0}$$

其中 $\mathbf{A}_j$ 为关节 $j$ 的标准 DLT 约束矩阵，$\mathbf{w}_j = [\alpha_{j,1}, \alpha_{j,1}, \alpha_{j,2}, \alpha_{j,2}, ..., \alpha_{j,N}, \alpha_{j,N}]^\top$ 为对应的逐行权重向量（每个视图贡献两个方程），$\circ$ 表示 Hadamard 积。通过加权 SVD 求解该齐次方程，得到粗 3D 关节位置 $\mathbf{J}^{3D,(0)}$，再通过 MANO 模型恢复粗网格顶点 $\mathbf{V}^{3D,(0)}$。

### 3.3 不确定性门控的迭代细化（UGCA）

细化阶段以粗 3D 查询为起点，通过 $L$ 层堆叠的 Transformer 解码器迭代精修。其核心是**不确定性门控交叉注意力（Uncertainty-Gated Cross-Attention, UGCA）**模块。

对于每层解码器，首先将当前 3D 关节估计投影回各视图的 2D 平面，然后通过**多尺度可变形注意力**从各视图特征中采样：

$$y_{j,n} = \sum_{s=1}^S \sum_{k=1}^K A_{nsk} \cdot \phi(\mathbf{F}_n^s, \mathbf{p}_{j,n}^{2D} + \Delta p_{nsk})$$

其中 $S$ 为特征尺度数，$K$ 为每尺度的采样点数，$\Delta p_{nsk}$ 为可学习的采样偏移，$A_{nsk}$ 为注意力权重。该操作从每个视图专家 $n$ 中提取关节 $j$ 的局部上下文特征 $y_{j,n}$。

随后，**复用粗阶段的不确定性权重**作为门控信号，对 $N$ 个视图专家响应进行加权融合：

$$y_j = \sum_{n=1}^N \alpha_{j,n} \cdot y_{j,n}$$

这一设计的核心洞察在于：不确定性权重 $\alpha_{j,n}$ 本身就是对视图专家可靠性的量化评估，自然地充当了 MoE 路由器的角色，无需额外学习门控网络。融合后的特征 $y_j$ 经 FFN 残差块和 MLP 回归头预测坐标更新量，完成一次迭代。

对于网格顶点，通过 MANO 蒙皮权重矩阵将关节不确定性传播到顶点：

$$\sigma_{v,n}^2 = \sum_{j=1}^{21} W_{v,j} \cdot \sigma_{j,n}^2$$

其中 $W_{v,j}$ 为顶点 $v$ 对关节 $j$ 的蒙皮权重，确保顶点级门控与关节级不确定性保持物理一致性。

### 3.4 训练目标

不确定性建模分支通过**高斯负对数似然损失**监督：

$$\mathcal{L}_{NLL} = \frac{1}{N} \sum_{n=1}^N \sum_{j=1}^{J} \left( \log \sigma_{j,n} + \frac{(\bar{\mathbf{J}}_{j,n}^{2D} - \boldsymbol{\mu}_{j,n})^2}{2\sigma_{j,n}^2} \right)$$

其中 $\bar{\mathbf{J}}_{j,n}^{2D}$ 为真值 2D 关节坐标。该损失同时优化均值预测精度和方差校准：当预测误差大时，网络被迫输出大方差以降低损失；当预测准确时，小方差更优。这自然地驱动网络学习可信的不确定性估计。

总训练目标组合多个几何一致性约束：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{NLL} + \lambda_2 \mathcal{L}_{3D} + \lambda_3 \mathcal{L}_{2D} + \lambda_4 \mathcal{L}_{DLT}$$

其中 $\mathcal{L}_{3D}$ 和 $\mathcal{L}_{2D}$ 分别为 3D 关节/顶点和重投影 2D 的 L1 损失，$\mathcal{L}_{DLT}$ 约束粗阶段 DLT 解的几何一致性。

### 设计要点总结

UGCA 模块的**关键因果机制**在于：不确定性权重 $\alpha_{j,n}$ 在粗阶段作为三角化加权因子，在细化阶段作为交叉注意力门控信号，实现了**单一可学习信号贯穿两阶段**的优雅设计。消融实验（Table 3）证实，移除粗阶段导致 MPJPE 从 13.10 mm 升至 21.55 mm（+8.45 mm），移除细化阶段升至 16.61 mm（+3.51 mm），验证了粗到细联合门控的必要性。此外，软门控（保留所有视图专家）在所有数据集上均优于硬门控（Top-k 选择，Table 4），说明即使低置信度视图仍包含可被不确定性权重自动抑制的微弱信号。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/001_Figure_1.jpg]]
*Figure 1: Our main research intuition and idea. (a) Since hand joints have varying reliability across different views, (b) we formulate the multi-view 3D hand reconstruction task into a MoE task, treating different views as different experts, and (c) using the predicted uncertainty to gate the fusion among view experts*

## 实验与分析

### 实验设置

所有输入RGB图像统一缩放并中心裁剪至256×256分辨率。多视图特征提取采用共享的ResNet-34骨干网络，并使用预训练权重初始化。优化器为Adam，初始学习率设为$1 \times 10^{-4}$。所有对比方法均使用相同的骨干网络、输入分辨率和训练超参数，确保公平比较。

### 主实验结果

**Table 1** 展示了JUMP-Hand在三个多视图手部数据集上与现有方法的全面对比。在HO3D-MV全量测试集上，JUMP-Hand的MPVPE达到**13.39 mm**，相较此前最优方法POEM（Yang et al., CVPR 2023）的17.20 mm降低了**22.2%**；MPJPE为**13.10 mm**，较POEM的17.28 mm降低**24.2%**。在DexYCB-MV上，MPVPE为5.45 mm，MPJPE为5.31 mm，均显著优于对比方法。

在更具挑战性的场景下，JUMP-Hand的优势进一步扩大。**Table 2** 汇报了三个挑战性子集的结果：在HO3D-MV挑战子集上，MPVPE为**24.91 mm**，对比POEM的35.52 mm实现**29.9%的提升**；在DexYCB-MV挑战子集上，MPVPE为10.37 mm（POEM为13.88 mm，提升25.3%）；在OakInk-MV挑战子集上，MPVPE为11.75 mm（POEM为13.85 mm，提升15.2%）。这些结果表明，JUMP-Hand在遮挡、视角受限等困难条件下具有更强的鲁棒性。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on 3 challenging subsets*

**Figure 4** 展示了精度-效率权衡曲线。在单张RTX 3090 GPU上，JUMP-Hand以合理的推理代价实现了最优的重建精度，验证了不确定性门控机制在计算效率上的可行性。

### 消融实验

**Table 3** 系统性地消融了门控信号与重建阶段的设计选择。完整模型（实验c）在HO3D-MV上达到13.10 mm MPJPE。移除细化阶段导致MPJPE升至16.61 mm（+3.51 mm），而移除粗阶段则导致严重退化至21.55 mm（**+8.45 mm**），证明了粗到细两阶段设计的必要性。使用不确定性作为门控信号显著优于无门控或简单平均池化，验证了不确定性是有效的可学习置信度指示器。

**Table 4** 对比了软门控与硬门控机制。软门控（使用所有视图专家）在所有数据集上均优于Top-k硬门控（仅选择最置信的k个视图），表明保留部分低置信度视图的信息对鲁棒融合是有益的——即使某视图对特定关节的观测不可靠，其提供的弱信号仍可能包含有价值的结构线索。

### 定性分析

**Figure 5** 展示了在运动模糊、严重遮挡和手部缺失等极端条件下的定性对比。当输入图像存在显著退化时，现有方法往往产生扭曲或不完整的手部几何，而JUMP-Hand仍能恢复准确、完整的3D手部姿态与形状。这归因于不确定性门控机制显式抑制了不可靠视图的污染，使模型能够依赖高置信度视图的信息进行重建。

### 失败模式与局限性

尽管JUMP-Hand在多数场景下表现优异，其基于高斯的不确定性建模为单模态，可能无法完全捕获严重遮挡引起的复杂多模态歧义性。当某个关节在所有视图中均被遮挡时，单模态高斯的不确定性估计可能不足以表达观测的完全缺失，导致重建结果偏向先验均值。未来工作可探索更具表达力的概率表示（如混合高斯或归一化流）以更好地处理极端条件下的不确定性。

> **注意：** 上述失败模式分析基于论文自述的局限性，具体的失败案例定量统计需查阅原文附录进行人工验证。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/004_Table_1.jpg]]
*Table 1: Comparison with the state-of-the-art on OakInk-MV, DexYCB-MV, and HO3D-MV datasets. ↓ indicates lower is better, ↑ indicates higher is better. All distance metrics are in millimeters (mm). AUC-V/J represent the area under the PCK curve for vertex and joint accuracy, respectively. Best in bold*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/007_Table_3.jpg]]
*Table 3: Ablation on gating signals and reconstruction stages. ‘C‘ and ‘R‘ denote the coarse and refinement stages. Experiment (c) is our full model with uncertainty-based gating in both stages. Metrics are reported on HO3D-MV (mm)*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/008_Table_4.jpg]]
*Table 4: Comparison of gating mechanisms. Soft gating uses all view experts, while Top-k selects the k most confident views for each joint and discards the rest. Metrics are reported in mm*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/006_Figure_4.jpg]]
*Figure 4: Accuracy-efficiency trade-off on HO3D-MV. Experiments are conducted on a single RTX 3090 GPU*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Kuang_JUMP_Hand_Learni/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative comparison. We visualized 2D images with challenges from multiple perspectives in the dataset, including (1) motion blur, (2) occlusion, and (3) hand missing. When 3D hand reconstruction is performed based on these images, our method achieves better reconstruction results compared with SOTA methods. This indicates that our explicit modeling approach has superior robustness*

## 方法谱系与知识库定位

### 多视图手部重建方法演进

多视图手部重建的核心挑战在于如何有效融合来自不同视角的互补信息。早期方法如 **Zhang et al.** (NeurIPS 2021) 和 **Spectral Graphormer** (Tse et al., ICCV 2023) 主要依赖图神经网络或Transformer架构进行特征聚合，但对各视图可靠性的差异缺乏显式建模。**POEM** (Yang et al., CVPR 2023) 和 **MLPHand** (Yang et al., ECCV 2024) 代表了近年来的主流范式，通过隐式注意力机制或平均池化无差别地聚合多视图特征。这种“平等对待”策略的根本问题在于：手部关节在不同视图中的可见性和观测质量存在显著差异，不可靠视图的信息会污染融合结果，构成当前方法的**核心瓶颈**。

JUMP-Hand 的关键突破在于**将多视图融合重新定义为混合专家（Mixture-of-Experts, MoE）路由问题**：每个视图被视为一个专家，而关节级不确定性则作为显式的、可物理解释的门控信号，动态决定各专家对最终预测的贡献权重。这一设计直接将观测可靠性量化为可学习的置信度指标，使融合过程从“黑盒注意力”转变为“白盒概率推理”。

### 核心差异点：不确定性作为显式门控

与现有方法的三个关键差异槽位对比如下：

| 设计维度 | 现有方法 | JUMP-Hand | 机制优势 |
|---------|---------|-----------|---------|
| **多视图特征融合** | 平均池化或隐式注意力（POEM, MLPHand） | 不确定性门控交叉注意力（UGCA），按关节加权融合视图专家 | 显式抑制不可靠视图，避免信息污染 |
| **三角化方法** | 标准DLT，各视图等权贡献 | 不确定性引导DLT（UG-DLT），基于方差权重抑止低可靠性视图 | 从概率角度重构三角化，粗初始化更稳健 |
| **2D关节表示** | 确定性热图回归 | 概率高斯建模，联合预测均值和对角协方差 | 量化视图依赖的观测不确定性，提供门控信号来源 |

这种设计的本质是：**预测的不确定性本身成为路由决策的依据**——高方差的视图在融合时自动获得低权重，无需额外学习路由网络。消融实验证实，使用不确定性作为门控信号显著优于无门控或简单平均池化（Table 3），且软门控（保留所有视图专家）在所有数据集上均优于硬门控（Top-k选择），证明即使低置信度视图仍可能携带有用信息（Table 4）。

### 粗到细MoE架构的合理性

JUMP-Hand 采用粗到细两阶段设计，其必要性由消融实验直接验证：移除细化阶段导致MPJPE从13.10 mm升至16.61 mm（+3.51 mm），而移除粗阶段则导致MPJPE急剧升至21.55 mm（+8.45 mm）。粗阶段的UG-DLT提供了稳健的3D初始化，使后续迭代Transformer解码器能够在正确的空间邻域内进行可变形注意力特征采样；若跳过粗阶段，细化模块缺乏可靠的几何先验，性能大幅退化。

### 适用边界与局限

**适用场景**：JUMP-Hand 在以下条件下表现突出：
- 多视图设置（≥2个同步视图），各视图间存在显著的重叠和互补关系
- 存在部分遮挡、运动模糊或个别视图缺失的挑战性场景（Figure 5定性结果，HO3D挑战子集29.9%提升）
- 需要显式可解释性融合权重的应用（如人机交互中的不确定性可视化）

**已知局限**：
1. **单模态高斯假设**：当前不确定性建模基于对角高斯分布，可能无法完全捕获严重遮挡引起的复杂多模态歧义性（如手指完全隐藏时，其位置存在多个合理假设）。论文明确指出这一局限，并建议未来探索更具表达力的概率表示。
2. **多视图依赖**：方法本身需要多视图输入，无法直接应用于单目场景。虽然理论上可扩展至任意视图数，但视图数过少时不确定性估计的统计意义减弱。
3. **计算开销**：Figure 4的精度-效率权衡曲线显示，JUMP-Hand在单张RTX 3090 GPU上的推理速度约为POEM的60-70%，额外的计算主要来自不确定性估计分支和迭代解码器。

### 开放问题

1. **多模态不确定性建模**：单模态高斯是否足以应对所有遮挡场景？引入混合高斯或归一化流等更复杂的概率模型能否进一步提高极端条件下的鲁棒性？这涉及表达能力与计算开销的权衡。
2. **不确定性传播的理论基础**：顶点不确定性通过MANO蒙皮权重矩阵线性传播（Eq. 7），这一简化假设在复杂手势（如手指交叉）下是否仍然成立？非线性传播机制是否必要？
3. **跨任务泛化**：关节级不确定性门控的思想是否可迁移至其他多视图任务（如人体姿态估计、物体6D位姿估计）？这需要验证不确定性建模在不同几何结构上的适应性。

## 原文 PDF

![[paperPDFs/CVPR_2026/JUMP_Hand_Learning_Joint_wise_Uncertainty_to_Gate_Mixture_of_View_Experts_for_Multi_View_3D_Hand_Reconstruction.pdf]]