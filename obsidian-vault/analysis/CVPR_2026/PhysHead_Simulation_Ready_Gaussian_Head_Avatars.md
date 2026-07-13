---
title: "PhysHead: Simulation-Ready Gaussian Head Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhysHead_Simulation_Ready_Gaussian_Head_Avatars.pdf
project_link: "https://phys-head.github.io"
code_link: null
aliases:
- PhysHead
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 采用分层表示，将面部建模为附着在 FLAME 上的高斯原语，将头发建模为显式发丝并耦合物理引擎；通过 VLM 生成秃头图像以恢复遮挡区域，并引入发丝间颜色一致性损失来正则化不可见发丝的外观。
primary_logic: 通过 VLM 图像编辑与可微分渲染构建秃头外观代理，实现了头部与头发的彻底解耦；并利用相邻发丝的色差惩罚，确保了在物理模拟中隐藏区域的外观一致性，使得动态头发得以直接驱动。
claims:
- 分层表示允许面部表情与头发动力学的分别控制，避免了单层表示导致的皮肤剥落伪影。
- VLM 生成的秃头图像结合差分渲染和泊松混合，能恢复被头发遮挡的头部区域，并在多种肤色上泛化。
- 颜色一致性损失使隐藏发丝获得合理颜色，避免了随机外观，使物理动画成为可能。
- 用户研究显示 PhysHead 的头发物理真实性达 98.5%，结构一致性 88.5%，远超基线 (0-1.5% / 3.1-8.5%)。
---

# PhysHead: Simulation-Ready Gaussian Head Avatars

> [!tip] 核心洞察
> 通过 VLM 图像编辑与可微分渲染构建秃头外观代理，实现了头部与头发的彻底解耦；并利用相邻发丝的色差惩罚，确保了在物理模拟中隐藏区域的外观一致性，使得动态头发得以直接驱动。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhysHead：仿真就绪的高斯头部化身 |
| 英文题名 | PhysHead: Simulation-Ready Gaussian Head Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.06467) · [Project](https://phys-head.github.io) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | PhysHead |
| Dataset | Ava-256, User Study, Ava-256 dynamics |

> [!tip] 效果简介
> - Ava-256 上，PSNR (vs GaussianHaircut) 30.28 vs 30.55 (-0.27)；SSIM (vs GaussianHaircut) 0.946 vs 0.915 (+0.031)；LPIPS (vs GaussianHaircut) 0.061 vs 0.071 (-0.010)。
> - User Study 上，Physical Plausibility (%) 98.5 vs 0 / 1.5 (+97.0%)；Structural Coherence (%) 88.5 vs 8.5 / 3.1 (+80.0%)。
> - Ava-256 dynamics 上，Explained Variance PC1 (%) (lower = dynamic) 93.28 vs 95.42 / 96.16 (-2.14)。

## 概要

现有头部化身方法普遍假设头发与头部刚性绑定，无法解耦面部表情与头发运动，导致动态场景下头发运动不真实，且被头发遮挡的头部区域难以合理重建。**PhysHead** 的核心洞察在于：通过视觉语言模型（VLM）生成秃头图像并结合可微分渲染构建头部外观代理，实现头部与头发的彻底解耦；同时引入发丝间颜色一致性损失，使隐藏区域获得合理外观，从而让基于物理引擎的动态头发驱动成为可能。

方法上，PhysHead 采用分层表示：面部建模为附着在 FLAME 参数化网格上的 3D 高斯原语，由表情参数驱动；头发则表示为基于发丝的结构化 3D 高斯，并通过稀疏引导发丝耦合物理引擎进行动力学模拟。这一设计使得面部表情与头发物理可分别控制，避免了单层表示在动画时出现的皮肤剥落伪影。

实验表明，PhysHead 在保持与 GaussianHaircut 可比的外观重建质量（PSNR 30.28 vs 30.55，SSIM 0.946 vs 0.915）的同时，大幅提升了动态真实感：用户研究中头发物理合理性达 98.5%（基线 0–1.5%），结构一致性达 88.5%（基线 3.1–8.5%）；动力学指标上，主成分解释方差降至 93.28%（基线 95.42–96.16%），时序平滑度降至 0.863（基线 2.13–6.23），验证了动态头发运动的有效性。消融实验进一步证实，颜色一致性损失和分层优化策略是实现仿真就绪化身的关键。

真实感头部化身是沉浸式远程呈现与数字人应用的核心技术。现有方法在静态场景下已能取得令人印象深刻的渲染质量，但一旦进入动态驱动，一个关键瓶颈便暴露出来：**头发运动的物理真实感严重缺失**。无论是基于 3D 高斯泼溅的 **Gaussian Avatars (GA)** 还是 **Gaussian Head Avatars (GHA)**，其头发表示均附着在参数化头部模型（如 FLAME）上，随头部做刚性运动。这种假设在头部转动或点头时会导致头发与头部同步旋转，完全忽略了惯性、重力与碰撞等基本物理效应，产生“头盔式”的僵硬动画。

更深层的问题在于**头发与头部的耦合困境**。真实世界中，头发并非头部的附属品——它覆盖、遮挡头部表面，同时拥有独立的运动自由度。要构建一个既能精确控制面部表情、又能独立模拟头发动力学的化身，必须实现两者的彻底解耦。然而，解耦面临双重挑战：其一，被头发遮挡的头部区域在训练视图中不可见，缺乏合理的重建约束；其二，发丝内部隐藏区域（如被外层发丝遮挡的内层发丝）的外观同样缺乏监督信号。**GaussianHaircut (GH)** 虽引入了基于发丝的几何表示，但隐藏发丝的颜色呈随机分布，导致在物理模拟中这些发丝一旦暴露便产生视觉伪影，无法直接用于动画。**HairCUP** 尝试通过组合式架构分离头部与头发，但其依赖 Score Distillation Sampling (SDS) 来恢复遮挡区域，容易引入肤色偏差与伪影，且其非结构化的高斯头发表示仍无法与物理引擎对接。

上述缺口指向一个共同的技术诉求：**仿真就绪的头发表示**。这要求头发不仅要在静态渲染中逼真，更要在动态模拟中保持外观一致性与几何合理性。具体而言，需要解决三个子问题：

1. **分层重建**：如何从多视角视频中完整恢复被头发遮挡的头部外观，并构建独立的头部与头发层？
2. **结构化头发表示**：如何表示头发几何与外观，使其既能高保真渲染，又能与物理引擎无缝对接？
3. **隐藏区域外观正则化**：如何为不可见发丝赋予合理颜色，确保在物理模拟中外露时不会破坏视觉连贯性？

PhysHead 正是围绕这三个问题展开。其核心动机在于：通过视觉语言模型（VLM）构建秃头外观代理，实现头发的彻底剥离与头部的完整重建；采用基于发丝的结构化 3D 高斯表示，使头发几何天然兼容物理模拟管线；并引入发丝间颜色一致性损失，将外层可见发丝的颜色传播至内层隐藏区域。这一设计使得 PhysHead 首次实现了同时支持面部表情参数化控制与头发物理模拟的真实感头部化身，并在用户研究中取得了 98.5% 的物理真实感评分——相比之下，基线方法仅为 0–1.5%。

## 核心方法与创新机理

PhysHead 的核心创新在于通过**分层表示与物理耦合**，首次实现了仿真就绪的逼真动态头发头部化身。相较于现有方法将头发视为刚性附着或非结构化高斯的做法，PhysHead 在以下四个关键维度上实现了根本性突破。

### 1. 发丝级结构化头发表示与物理引擎耦合

现有方法（如 **Gaussian Avatars** 和 **Gaussian Head Avatars**）将头发建模为附着在 FLAME 网格上的非结构化 3D 高斯原语，导致头发只能随头部刚性移动，无法产生自然的动态效果。**GaussianHaircut** 虽然引入了基于发丝段的中点高斯表示，但其隐藏发丝的颜色随机，不具备物理模拟的可行性。**HairCUP** 虽实现了头部与头发的分离，但头发仍为非结构化高斯，无法接入物理引擎。

PhysHead 的关键创新在于采用**基于发丝的结构化 3D 高斯表示**：每根发丝的每个段被分配一个 3D 高斯原语，并利用 TNB 框架（切线-法线-副法线）进行对齐。这一表示天然兼容物理引擎——通过 700 根引导发丝构建质点-弹簧系统，使用半隐式欧拉方法求解运动方程：

$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{\mathbf{F}(t)}{m} \Delta t$$

$$\mathbf{x}(t+\Delta t) = \mathbf{x}(t) + \mathbf{v}(t+\Delta t) \Delta t$$

随后通过 KNN 插值（k=10）将引导发丝的运动传递给 60,000 根密集发丝，实现了头发在头部运动下的真实物理响应。

### 2. VLM 驱动的秃头外观代理与遮挡区域恢复

被头发遮挡的头部区域重建是分层表示的核心难题。现有方法或完全忽略该问题，或依赖 Score Distillation Sampling（SDS）（如 HairCUP），导致肤色偏差和伪影。PhysHead 创新性地引入**视觉语言模型（VLM）** 生成秃头图像：对多视角输入的第一帧使用 VLM 编辑去除头发，构建可微分渲染的 FLAME 纹理外观代理，再通过泊松图像编辑将代理纹理与动态序列的每帧面部区域融合，生成完整的无头发训练目标。

该方法在多种肤色上展现出良好的泛化能力（Fig 7, 12），相较于 SDS 方法显著减少了肤色偏差和伪影，为头部与头发的彻底解耦提供了可靠的外观监督。

### 3. 颜色一致性损失约束不可见发丝外观

基于发丝的高斯表示中，大量发丝段在训练视角下不可见，其颜色缺乏直接监督。**GaussianHaircut** 对此无约束，导致隐藏区域呈现随机颜色，无法用于物理动画（Fig 6）。PhysHead 提出**颜色一致性损失**，强制相邻发丝的颜色相似：

$$\mathcal{L}_{\mathrm{consistency}} = \sum_{i \in \mathcal{S}} \sum_{j \in \mathcal{N}(i)} \| \mathbf{c}_i - \mathbf{c}_j \|_2^2$$

该损失将外部可见发丝的颜色传播至内部隐藏发丝，确保在物理模拟中发丝发生位移和旋转时，暴露出的内部区域仍具有一致的外观。消融实验（Fig 8）证实，移除该损失后内部发丝呈现随机颜色，物理动画不可行。

### 4. 两阶段分层优化实现面部与头发的彻底解耦

PhysHead 采用**两阶段优化策略**：第一阶段仅优化附着在 FLAME 网格上的面部高斯，第二阶段优化发丝上的头发高斯。这一分层优化避免了单层表示在物理模拟时出现的皮肤剥落伪影（Fig 15），确保面部表情由 FLAME 参数化模型驱动，头发动力学由物理引擎独立控制，二者互不干扰。

**创新总结**：PhysHead 通过“发丝结构化高斯 + VLM 秃头代理 + 颜色一致性正则 + 分层优化”的技术组合，首次将静态外观重建与动态物理模拟统一在单一框架内。用户研究表明，其头发物理真实性达 98.5%，结构一致性达 88.5%，远超基线方法（0-1.5% / 3.1-8.5%），验证了该创新路径的有效性。

PhysHead 的整体设计遵循**分层解耦—代理重建—物理驱动**的流水线，将头部化身明确拆分为面部层与头发层，分别采用不同的表示与动力学机制，最终通过可微分渲染合成仿真就绪的动态头像。

### 输入与预处理

方法以**多视角视频**作为输入。首先利用视觉语言模型（VLM）对首帧进行头发去除编辑，生成秃头参考图像（Figure 3a）。以此为基础，结合可微分渲染与泊松图像编辑，将整个动态序列中的头发区域移除，为面部层的独立优化提供干净的训练目标（Figure 3b–c）。

### 分层表示与模块架构

PhysHead 的核心在于**双分支结构**（Figure 2）：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/002_Figure_2.jpg]]
*Figure 2: Overview. PhysHead reconstructs an animatable 3D human head avatar (e) from a multiview input video. It is based on a 3D Gaussian appearance representation that is split into a face (c) and a hair region (d). The face region uses 3D Gaussians that are attached to a 3DMM-based mesh (FLAME [43]), which allows for parametric facial expression as well as head pose control (a,c). To enable physicsbased animation of the hair region, we rely on a strand-based hair model (b). The appearance of the individual hair strands is represented as structured 3D Gaussians attached to each hair strand segment (d)*

1. **面部层**：使用附着在 FLAME 参数化网格上的 3D 高斯原语表示。每个高斯原语由均值 $\mu_k$、尺度 $s_k$、旋转四元数 $q_k$、不透明度 $o_k$、颜色 $c_k$ 和球谐系数 $\mathrm{SH}_k$ 参数化，即 $\{ \mathcal{G}_k \} = \{ \mu_k, s_k, q_k, o_k, c_k, \mathrm{SH}_k \}$。面部表情与头部姿态由 FLAME 的形变场直接驱动，继承了 Gaussian Avatars 的刚体附着机制。

2. **头发层**：头发被表示为发丝集合 $H \in \mathbb{R}^{N_d \times N_{\mathrm{seg}} \times 3}$，其中 $N_d$ 为密集发丝数量（约 60,000 根），$N_{\mathrm{seg}}$ 为每根发丝的段数。发丝几何初始由 NeuralHaircut 提供，每段发丝上附着结构化的 3D 高斯原语，利用 TNB 框架对齐。这种基于发丝的表示与物理引擎天然兼容。

### 优化策略

面部层与头发层采用**两阶段优化**：第一阶段仅优化 FLAME 网格覆盖区域的高斯原语，第二阶段优化头发区域。这种分层优化避免了单层表示在动画时产生的皮肤剥落伪影。

头发外观优化的总目标为：

$$\mathcal{L}_{\mathrm{hair}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{consistency}} \mathcal{L}_{\mathrm{consistency}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为组合 L1 与 D-SSIM 的 RGB 损失（$\lambda=0.2$），$\mathcal{L}_{\mathrm{consistency}}$ 为颜色一致性损失，强制相邻发丝颜色相似：

$$\mathcal{L}_{\mathrm{consistency}} = \sum_{i \in \mathcal{S}} \sum_{j \in \mathcal{N}(i)} \| \mathbf{c}_i - \mathbf{c}_j \|_2^2$$

该损失是使隐藏区域发丝获得合理外观的关键，直接决定了物理模拟的可用性。

### 物理模拟与驱动

头发动力学采用**引导发丝—密集插值**架构（Figure 4）：从密集发丝中选取约 700 根引导发丝构建质点系统，使用物理引擎以半隐式欧拉方法求解运动：

$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{\mathbf{F}(t)}{m} \Delta t$$
$$\mathbf{x}(t+\Delta t) = \mathbf{x}(t) + \mathbf{v}(t+\Delta t) \Delta t$$

密集发丝通过 KNN（$k=10$）插值跟随引导发丝运动，权重与距离成反比。头部姿态由 FLAME 追踪结果提供，作为头发质点系统的边界驱动条件。

### 输出与应用

最终输出为**仿真就绪的分层头部化身**：面部层响应 FLAME 的表情参数，头发层响应物理引擎的动力学解算。该分层架构天然支持头发几何编辑（Figure 9）与发型交换（Figure 10）等下游应用。

PhysHead 的核心架构围绕“分层表示-物理模拟-外观约束”三条主线展开，通过五个关键模块协同实现仿真就绪的动态头发化身。

### 分层高斯表示模块

PhysHead 将头部化身显式分解为面部层和头发层，分别采用不同的高斯原语附着策略。面部层沿用 **Gaussian Avatars** 的范式，将 3D 高斯原语附着在 FLAME 参数化网格上，每个高斯原语的参数定义为：

$$\{ \mathcal{G}_k \} = \{ \mu_k, s_k, q_k, o_k, c_k, \mathrm{SH}_k \}$$

其中 $\mu_k$ 为均值位置，$s_k$ 为缩放因子，$q_k$ 为旋转四元数，$o_k$ 为不透明度，$c_k$ 为基础颜色，$\mathrm{SH}_k$ 为球谐系数。面部表情和头部姿态通过 FLAME 的变形场直接驱动附着的高斯原语。

头发层采用基于发丝的结构化表示。给定由 **NeuralHaircut** 初始重建的密集发丝集合：

$$H \in \mathbb{R}^{N_d \times N_{\mathrm{seg}} \times 3}$$

其中 $N_d$ 为发丝数量，$N_{\mathrm{seg}}$ 为每根发丝的段数。每个发丝段分配一个 3D 高斯原语，其位置和方向由发丝几何的 TNB 框架（切向量-法向量-副法向量）对齐，使高斯表示与物理模拟所需的发丝结构天然兼容。

两阶段优化策略实现了面部与头发的彻底解耦：第一阶段仅优化 FLAME 网格覆盖区域的高斯原语，第二阶段在固定面部层后优化头发区域。这一设计避免了单层表示在动画时出现的皮肤剥落伪影（见 Figure 15）。

### VLM 秃头图像生成与头部外观代理模块

被头发遮挡的头部区域是分层重建的核心难点。PhysHead 利用视觉语言模型（VLM）从多视角视频的首帧中移除头发，生成秃头图像。基于这些秃头图像，通过可微分渲染优化附着在 FLAME 上的共享纹理图 $T$，构建头部外观代理。

对于动态序列的每一帧，将该外观代理以当前头部姿态和表情渲染，并通过泊松图像编辑与原始图像的面部区域融合，生成完整的秃头训练目标。这一流程避免了 **HairCUP** 使用 SDS 导致的肤色偏差和伪影问题，在多种肤色上展现出更好的泛化能力（见 Figure 7, 12）。

### 物理模拟模块

头发动力学通过稀疏引导发丝与物理引擎耦合实现。从密集发丝中选取约 700 根引导发丝，附着在头皮上构建质点-弹簧系统。物理引擎采用半隐式欧拉方法进行时间积分：

速度更新：
$$\mathbf{v}(t+\Delta t) = \mathbf{v}(t) + \frac{\mathbf{F}(t)}{m} \Delta t$$

位置更新：
$$\mathbf{x}(t+\Delta t) = \mathbf{x}(t) + \mathbf{v}(t+\Delta t) \Delta t$$

其中 $\mathbf{F}(t)$ 包含重力、弹簧力和阻尼力，$m$ 为质点质量，$\Delta t$ 为时间步长。引导发丝的运动通过 KNN 插值（$k=10$）驱动约 60,000 根密集发丝，插值权重与距离成反比（见 Figure 4）。物理模拟基于离线 Maya 引擎，参数需针对不同发型进行调整。

### 外观优化与颜色一致性约束

头发外观优化的核心挑战在于：大量发丝段在训练视角下不可见，缺乏外观监督信号。PhysHead 引入颜色一致性损失来解决这一问题：

$$\mathcal{L}_{\mathrm{consistency}} = \sum_{i \in \mathcal{S}} \sum_{j \in \mathcal{N}(i)} \| \mathbf{c}_i - \mathbf{c}_j \|_2^2$$

其中 $\mathcal{S}$ 为所有发丝段集合，$\mathcal{N}(i)$ 为段 $i$ 的相邻段集合，$\mathbf{c}_i$ 为段 $i$ 的颜色。该损失强制相邻发丝颜色相似，使得可见发丝的外观信息能够传播到不可见区域，确保隐藏发丝获得合理颜色而非随机值。

头发外观优化的总损失函数为：

$$\mathcal{L}_{\mathrm{hair}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{consistency}} \mathcal{L}_{\mathrm{consistency}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为掩码区域的组合 L1 和结构相似性损失：

$$\mathcal{L}_{\mathrm{rgb}} = (1-\lambda) \cdot \mathcal{L}_1 + \lambda \cdot \mathcal{L}_{\mathrm{D-SSIM}}, \quad \lambda = 0.2$$

消融实验表明，移除颜色一致性损失后，隐藏发丝呈现随机颜色，无法用于物理动画（见 Figure 8），验证了该约束对仿真就绪外观的关键作用。

## 实验与关键发现

### 实验设置

PhysHead 在 **Ava-256** 多视角视频数据集上进行评估，使用其提供的 16 个摄像机视图。实验选取了多个不同肤色和发型的演员（Table 3）。方法将面部建模为附着在 FLAME 参数化网格上的 3D 高斯原语，头发则采用基于发丝的结构化高斯表示。物理模拟参数（如引导发丝数量、刚度、阻尼等）针对不同发型进行微调（Table 4）。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/012_Table_3.jpg]]
*Table 3: Actors IDs. List of actors from the Ava-256 [51] dataset used in our experiments*

### 主结果

#### 静态外观质量

Table 1 给出了与 **GaussianHaircut** (GH) 的定量对比。PhysHead 在结构相似性指标上取得最优：

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/006_Table_1.jpg]]
*Table 1: Comparison to GaussianHaircut [100]. Green indicates the best and yellow indicates the second*

| 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|------|--------|--------|---------|
| GaussianHaircut | **30.55** | 0.915 | 0.071 |
| PhysHead (Ours) | 30.28 | **0.946** | **0.061** |

PhysHead 的 PSNR 略低于 GH（−0.27 dB），但在 SSIM 上提升 0.031，LPIPS 降低 0.010。这一结果表明，虽然 PhysHead 在像素级重建精度上略有损失，但其结构一致性和感知质量显著更优。PSNR 的轻微下降可归因于分层表示与物理模拟引入的额外约束，这些约束在静态帧中略微牺牲了逐像素拟合精度，但换取了动态场景下的物理真实感。

#### 动态物理真实性

Table 2 报告了用户研究与动态指标。PhysHead 在物理真实性上获得 **98.5%** 的用户偏好，而基线方法（GA/GHA）仅获得 0% 和 1.5%。结构一致性方面，PhysHead 达 **88.5%**，远超基线的 8.5% 和 3.1%。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/013_Table_2.jpg]]
*Table 2: E. Variance PC1 (%) shows how much of the motion of hair 3D Gaussians is captured by a single principle component. TS measures frame to frame change in PCA space*

动态分析指标进一步量化了头发的运动特性：
- **Explained Variance PC1**：PhysHead 为 93.28%，低于 GA 的 95.42% 和 GHA 的 96.16%，表明 PhysHead 的头发运动具有更高的复杂度，无法被单一主成分充分解释。
- **Temporal Smoothness (TS)**：PhysHead 为 0.863，远低于 GA 的 6.23 和 GHA 的 2.13，说明 PhysHead 的头发运动帧间变化更丰富，而非刚性跟随头部。

Figure 11 的点头序列分析进一步印证了这一点：PhysHead 的头发几何标准差随头部运动动态变化，而其他方法的头发几何保持恒定，证实了物理模拟带来的真实动态响应。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/014_Figure_11.jpg]]
*Figure 11: Analysis of the riggidity of the hair geometry on a nodding sequence. Our method (green) handles dynamic effects, others are static resulting in a constant std. dev. of geometry*

#### 与 HairCUP 的定性对比

Figure 7 和 Figure 12 展示了与 **HairCUP** 的对比。HairCUP 使用 SDS 进行头发去除，在不同受试者上表现出肤色偏差和伪影，且其非结构化高斯无法支持物理模拟。PhysHead 采用 VLM 生成秃头图像，在多种肤色上泛化更好，分层表示也更干净。

![[assets/figures/papers/paper_list_l16_https_arxiv_org_abs_2604_06467/figures/009_Figure_7.jpg]]
*Figure 7: HairCUP [32] comparison. Since haircup uses SDS, it exhibits artifacts and has tendency to generate the same type of skin color. In contrast, we use VLM model for image generation which is trained on a lot of data. This helps with generalization to different skin colors. Despite being compositional, it has unstructured gaussians which does not allow for physics simulation. For more results, see supp mat. HairCUP images taken from their original paper*

### 消融实验

#### 颜色一致性损失

Figure 8 展示了移除颜色一致性损失 $\mathcal{L}_{\mathrm{consistency}}$ 的效果。无该损失时，被外层发丝遮挡的内部高斯原语呈现随机颜色，在物理模拟导致发丝散开后暴露出不真实的外观。引入 $\mathcal{L}_{\mathrm{consistency}}$ 后，相邻发丝间颜色平滑传播，隐藏区域获得合理外观，使物理动画成为可能。

#### 单层表示 vs 分层表示

Figure 15 的消融表明，即使使用发丝表示，若将头发与头部作为单层联合优化，在动画时仍会出现皮肤剥落伪影——发丝移动时暴露出错误附着在发丝上的皮肤颜色高斯。分层两阶段优化（先优化头部层，再优化头发层）从根本上解决了这一问题。

#### VLM 秃头管线

Figure 7 和 Figure 12 间接消融了 VLM 管线的作用。与 HairCUP 的 SDS 方法相比，VLM 生成的秃头图像结合泊松混合，能更准确地恢复被头发遮挡的头部区域，且在不同肤色上保持一致性。**注意**：该结论基于与 HairCUP 的间接对比，文中未提供 VLM 管线的独立消融实验，VLM 方法相对于其他头发去除策略的绝对优势需进一步验证。

### 局限性

PhysHead 存在以下已知局限：

1. **掩码依赖**：外观优化质量依赖前景/头发分割掩码的精度，不完美的掩码可能导致头部与头发解耦错误。
2. **头发几何继承**：PhysHead 依赖 NeuralHaircut 提供的初始发丝几何，因此继承了其对卷发等复杂发型的处理局限（Figure 16）。
3. **VLM 多视角一致性**：VLM 生成秃头图像时可能改变头部姿态，需要人工过滤多视角不一致的视图，限制了全自动流程的鲁棒性。
4. **物理模拟离线**：当前物理模拟基于离线 Maya 引擎，尚未实时集成，且参数（如 Start Curve Attract，Table 4）需针对每个发型手动调整。

## 定位与知识库关联

### 一、工作定位与核心区分

PhysHead 处于**动态头部化身**与**可驱动头发建模**的交汇点，其核心贡献在于首次将物理仿真就绪的显式发丝表示与 3D 高斯外观模型相结合，实现了面部表情与头发动力学的彻底解耦。与已有工作的关键区分如下：

- **Gaussian Avatars (GA)**：将 3D 高斯原语附着在 FLAME 网格上，头发作为非结构化高斯随头部刚性移动，无法产生任何动态头发效果。PhysHead 继承了其面部高斯附着机制，但将头发替换为发丝结构并引入物理驱动。
- **Gaussian Head Avatars (GHA)**：采用两阶段优化和类似 BFM 的控制模型，但头发仍为静态非结构化高斯。PhysHead 的两阶段分层优化借鉴了其思路，但通过 VLM 秃头管线实现了更彻底的层间解耦。
- **GaussianHaircut (GH)**：首次将头发表示为基于发丝段的 3D 高斯，但仅关注静态外观重建，隐藏发丝颜色随机，无法用于物理模拟。PhysHead 在此基础上引入颜色一致性损失（Eq. 6），使隐藏区域获得合理外观，从而打通了从重建到模拟的关键瓶颈。
- **HairCUP**：组合式化身方法，分离头部和头发两层，但头发为非结构化高斯，无法模拟；且使用 SDS 生成头部层，导致肤色偏差和伪影（Fig. 7, 12）。PhysHead 用 VLM 编辑替代 SDS，在多种肤色上表现出更好的泛化性。

### 二、方法谱系中的继承与突破

PhysHead 的技术路线建立在对以下关键组件的继承与改造之上：

| 组件 | 继承来源 | PhysHead 的改造 |
|------|----------|-----------------|
| 面部高斯附着 | GA（FLAME 网格锚定） | 保留，作为头部层的基础 |
| 发丝几何重建 | NeuralHaircut | 继承初始发丝几何，作为物理模拟和外观附着的基础 |
| 发丝段高斯表示 | GaussianHaircut | 保留 TNB 框架对齐，但增加颜色一致性损失 |
| 物理模拟 | 离线物理引擎（Maya） | 采用半隐式欧拉积分（Eq. 1-2），700 根引导发丝通过 KNN 插值驱动 60,000 根密集发丝 |
| 秃头图像生成 | VLM 编辑（InstructPix2Pix 等） | 结合可微分渲染与泊松混合，构建头部外观代理 |

**瓶颈突破的因果链路**：现有方法的根本缺陷在于头发与头部的耦合——要么头发刚性附着于头部（GA/GHA），要么虽分离但头发表示不兼容物理模拟（HairCUP）或隐藏区域外观不可控（GH）。PhysHead 通过三步走打通了这条链路：(1) VLM 秃头管线恢复遮挡区域，实现层间彻底解耦；(2) 发丝结构使头发表示天然兼容物理引擎；(3) 颜色一致性损失确保隐藏发丝在模拟中外观合理。

### 三、适用边界

PhysHead 在以下条件下表现良好：
- **多视角视频输入**：依赖多视角数据重建发丝几何和高斯外观。
- **直发或轻度卷发**：继承 NeuralHaircut 的几何重建能力边界，极端卷发（如非洲式卷发）仍存在困难（Fig. 16 显示卷发结果有明显退化）。
- **前景掩码质量充足**：头部与头发解耦依赖准确的分割掩码，不完美的掩码可能导致解耦错误。
- **离线物理模拟场景**：当前物理模拟基于离线 Maya 引擎，尚未实现实时集成，且参数需针对每个发型手动调整。

### 四、局限与开放问题

**已知局限**（来自论文自述与消融证据）：
1. **掩码依赖**：外观质量和解耦效果对前景/头发掩码质量敏感，掩码不完善时可能出现分层错误。
2. **卷发处理**：继承 NeuralHaircut 的几何重建局限，极端卷发场景下重建质量下降。
3. **VLM 姿态偏差**：VLM 生成秃头图像时可能改变头部姿态，需人工过滤多视角不一致的视图。
4. **离线模拟**：物理模拟未实时集成，模拟参数需针对每个发型调整，限制了交互式应用。

**开放问题**（需进一步研究）：
1. 能否将分层表示和动态头发扩展到**全身化身**，包括服装动态？
2. 能否实现**端到端可微的头发物理模拟**，以替代离线 Maya 管线并提升动态真实性？
3. 如何更好地处理**极端卷发和复杂发型**？可能需要改进发丝几何重建或引入隐式表示。
4. VLM 生成图像的多视角一致性能否通过**多模态大模型**进一步提升，减少人工过滤需求？
5. **实时头发模拟与渲染**的集成能否在移动设备上实现？这对消费级应用至关重要。

### 五、知识库定位

PhysHead 在知识库中应定位于 **动态数字化身 → 头部化身 → 物理仿真就绪的高斯化身** 这一细分节点。其核心知识资产包括：
- **分层解耦策略**：VLM 辅助的遮挡区域恢复 + 可微分渲染代理
- **发丝-高斯混合表示**：结构化 3D 高斯附着于发丝段，兼容物理引擎
- **颜色一致性正则化**：相邻发丝色差惩罚，使隐藏区域获得可模拟外观

这些资产为后续工作（如全身动态化身、端到端可微物理模拟）提供了可复用的技术模板。

## 原文 PDF

![[paperPDFs/CVPR_2026/PhysHead_Simulation_Ready_Gaussian_Head_Avatars.pdf]]
