---
title: "Video Diffusion Models are Training-free Motion Interpreter and Controller"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controller.pdf
aliases:
- MGTFMC
- VDMATFMIC
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "运动特征 MOFT：通过内容相关性移除（减去帧均值）和运动通道滤波（PCA 选择高贡献通道）从视频扩散特征中提取，能编码纯净的运动信息，并能直接作为训练无关的潜在优化引导信号。"
primary_logic: "视频扩散模型的中间特征天然存在运动感知通道，只需剔除共享内容信息并聚焦对运动主成分贡献大的通道，即可获得鲁棒、通用的训练无关运动特征 MOFT，从而实现对生成视频的运动方向和点拖拽的精细控制。"
claims:
- "PCA 分析显示，移除内容相关性后的扩散特征能按不同运动方向清晰分离。"
- "运动通道的数值变化与视频平移方向高度吻合，非运动通道则无此对应。"
- "MOFT 相似度热力图与光流运动高度对齐，且在 AnimateDiff、ModelScope、ZeroScope、SVD 等不同架构上均有效。"
- "MOFT 引导的无训练运动控制在运动保真度上达到 84.0，并在用户评价中同时兼顾运动保真度与自然度。"
---

# Video Diffusion Models are Training-free Motion Interpreter and Controller

> [!tip] 核心洞察
> 视频扩散模型的中间特征天然存在运动感知通道，只需剔除共享内容信息并聚焦对运动主成分贡献大的通道，即可获得鲁棒、通用的训练无关运动特征 MOFT，从而实现对生成视频的运动方向和点拖拽的精细控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视频扩散模型作为无需训练的运动解释器与控制器 |
| 英文题名 | Video Diffusion Models are Training-free Motion Interpreter and Controller |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2405.14864); [Project](https://xizaoqu.github.io/moft/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MOFT-guided training-free motion control |
| Dataset | 点拖拽精度, 用户偏好研究 |

> [!tip] 效果简介
> - 点拖拽精度 上，Mean Distance (↓) 为 0.175，对比 DragNUWA（精确值未报告，但差距较大），变化 显著接近目标点。
> - 用户偏好研究 上，Motion Faithfulness / Naturalness (1-5) 为 3.21 / 3.49，对比 Gen-2（高保真低自然度） / DragNUWA（高自然度低保真），变化 在保真度和自然度之间取得更均衡的结果。

## 概述

**瓶颈与动机**：视频扩散模型在生成过程中蕴含丰富的跨帧运动信息，但现有运动控制方法（如 **DragNUWA**、**MotionCtrl**、**VideoComposer**）依赖大量训练来定制运动行为，缺乏可解释、可跨架构泛化的运动特征提取机制，导致运动控制不透明且资源消耗大。同时，商业方案（如 **Gen-2** 的 Motion Brush）虽提供交互式运动控制，但同样需要专有训练流程，难以迁移到开源模型。

**核心发现**：本文揭示了一个关键现象——视频扩散模型的中间特征天然存在“运动感知通道”。通过对扩散特征进行简单的内容相关性移除（减去帧均值）和运动通道滤波（基于 PCA 主成分权重选择高贡献通道），即可获得一种纯净、鲁棒且无需训练的**运动特征 MOFT**（MOtion FeaTure）。该特征在相似度热力图上与光流运动高度对齐，且在 **AnimateDiff**、**ModelScope**、**ZeroScope**、**SVD** 等多种架构上均表现出跨模型的通用性。

**方法与定位**：基于 MOFT，本文提出了一套**训练无关的运动控制框架**。该方法属于“特征提取 + 潜在优化”范式：从预训练视频扩散模型的 U-Net 中间层提取 MOFT，将其作为引导信号，通过优化去噪过程中的潜在向量实现对生成视频的运动方向控制和点拖拽操作。与需要训练附加条件模块的 **MotionCtrl**、**DragNUWA** 等方法相比，本方法无需任何微调，仅通过损失函数设计（MOFT 对齐损失与 DIFT 点拖拽损失的组合）即可实现精细控制。在方法谱系中，该工作位于扩散特征重用与训练无关可控生成的交叉点，与 **DIFT**（Tang et al., NeurIPS 2024）等基于扩散特征的操作一脉相承，但将应用从语义对应拓展到了运动维度。

**关键结果**：实验表明，MOFT 引导的运动控制在运动保真度上达到 84.0，在用户偏好研究中同时兼顾了运动保真度（3.21/5）与自然度（3.49/5），相较于 Gen-2（高保真低自然度）和 DragNUWA（高自然度低保真）取得了更均衡的表现。在点拖拽精度上，Mean Distance 降至 0.175，显著优于基线方法。消融实验证实，保留前 4% 的运动通道时性能最优，内容相关性移除和运动通道滤波各自对运动对应性有独立贡献。

**局限性**：当前方法依赖 DDIM 反转技术，对真实视频的适用性有限；仅能控制运动方向，无法精确控制运动幅度；生成速度较慢（单样本约 3 分钟）；复杂运动模式（旋转、缩放等）的泛化能力尚未验证。

## 背景与动机

视频生成领域近年来取得了显著进展，扩散模型已成为主流范式。然而，对生成视频的运动进行精细控制仍是一个核心挑战。现有的运动控制方法大致可分为两类：一类是商业闭源方案，如 Runway 的 **Gen-2**（Runway, 2023），提供运动笔刷（Motion Brush）功能，但用户无法控制运动保真度与自然度之间的权衡；另一类是基于训练的方法，如 **DragNUWA**（Yin et al., arXiv 2023）通过点轨迹实现运动控制，**MotionCtrl**（Wang et al., arXiv 2023）统一控制相机与物体运动，**VideoComposer**（Wang et al., NeurIPS 2024）则通过额外运动矢量进行视频合成。这些方法虽然在各自场景下有效，但均需大量训练来定制运动控制模块，计算资源消耗大，且缺乏可解释、可跨架构泛化的运动特征提取手段。

根本瓶颈在于：视频扩散模型的中间特征中天然蕴含着丰富的跨帧运动信息，但如何从中提取纯净的运动表征，并将其直接用于训练无关的控制，此前未被有效探索。现有工作要么使用完整的扩散特征（如 **DIFT**（Tang et al., NeurIPS 2024）用于语义对应），但这些特征混杂了语义和结构等共享内容信息，无法直接编码运动；要么依赖额外训练的特征提取器，缺乏通用性。

本文的核心动机正是填补这一空白：**视频扩散模型本身是否可以作为训练无关的运动解释器与控制器？** 作者通过初步分析发现，对扩散特征进行主成分分析（PCA）时，原始特征无法按运动方向清晰分离，但若先移除内容相关性，则不同运动方向的视频在 PCA 投影空间中呈现出显著的可分性（Figure 2）。进一步观察表明，仅有少数通道对运动主成分有高贡献，且这些通道的跨帧数值变化与视频平移方向高度吻合，而非运动通道则无此对应关系（Figure 3）。这揭示了一个关键洞察：**视频扩散模型的中间特征中存在运动感知通道，只需剔除共享内容信息并聚焦对运动主成分贡献大的通道，即可获得鲁棒、通用的训练无关运动特征。** 基于此，本文提出 MOFT（MOtion FeaTure），并构建了一套无需训练的潜在优化框架，将 MOFT 作为引导信号，实现对生成视频的运动方向和点拖拽的精细控制。

## 核心创新

本文的核心贡献在于发现并利用视频扩散模型中间特征中天然存在的运动感知通道，提出了一种**无需训练**的运动特征提取与运动控制框架。其关键创新可归结为三个层面的“changed slots”，相对于现有训练依赖型方法形成了根本性的范式转变。

### 1. 运动特征提取：从完整特征到内容解耦与通道筛选

现有方法通常直接使用完整的扩散特征（如 **DIFT**，Tang et al., NeurIPS 2024）用于语义对应，或训练专用的运动特征提取器。这些方法面临一个根本性瓶颈：扩散特征同时编码了语义、结构和运动信息，直接使用会导致运动控制不透明且易受内容干扰。

本文的核心发现是：**通过移除内容相关性并筛选运动敏感通道，可以从通用视频扩散特征中提取出纯净的运动特征 MOFT**。这一发现建立在两个关键观察之上：

- **内容相关性移除**（Eq. 1）：对扩散特征 $\mathcal{X} \in \mathbb{R}^{H \times W \times F \times D}$，减去各帧特征的均值 $\mathcal{X}^{\mathrm{norm}} = \mathcal{X} - \frac{1}{F}\sum_{i=1}^{F} \mathcal{X}_i$，可消除跨帧共享的语义与结构信息。Figure 2 的 PCA 可视化提供了决定性证据：原始特征在 PCA 投影下无法按运动方向分离（Figure 2a），而去除内容相关性后，不同平移方向的特征在主成分空间中清晰分离（Figure 2b），置信度达 0.95。

- **运动通道滤波**（Eq. 2）：PCA 分析进一步揭示，仅少数通道对主成分有显著贡献（Figure 3a 的权重直方图）。这些“运动通道”的跨帧数值变化与视频平移方向高度吻合——右移时数值下降，左移时数值上升（Figure 3b-c），而非运动通道则无此对应关系（Figure 3d）。通过筛选这些通道 $\mathcal{C}$，MOFT 被定义为 $\mathcal{M} = (\mathcal{X}_{[j]} - \frac{1}{F}\sum_{i=1}^{F} \mathcal{X}_{i,[j]}), \quad j \in \mathcal{C}$。

这一特征提取策略的 changed slot 在于：**从“使用完整特征或训练专用提取器”转变为“无训练的内容解耦 + 通道筛选”**。Figure 4 的消融证实，单独的内容移除已能改善运动对应，而叠加运动通道滤波后，相似度热力图与光流运动高度对齐，且这一特性在 AnimateDiff、ModelScope、ZeroScope、SVD 等不同架构上均成立（Figure 4i-l），置信度 0.95。

### 2. 运动控制机制：从训练条件模块到潜在优化引导

现有运动控制方法（如 **DragNUWA**，Yin et al., arXiv 2023；**MotionCtrl**，Wang et al., arXiv 2023；**VideoComposer**，Wang et al., NeurIPS 2024）普遍依赖训练附加的条件模块来注入运动信号，资源消耗大且难以跨模型泛化。

本文的 changed slot 在于：**将运动控制重新定义为基于 MOFT 相似度的潜在向量优化问题**，完全避免了训练。具体而言：

- **参考 MOFT 构建**：通过 DDIM 反转从参考视频中提取 MOFT，或按运动规律（如平移方向）直接合成参考 MOFT。
- **潜在优化控制**（Alg. 1, Eq. 3）：在去噪过程中，定义运动控制损失 $\mathcal{L}^{c} = \frac{1}{|\mathcal{R}|}\sum_{(i,j)\in\mathcal{R}} ||\mathcal{M}_{i,j} - \mathcal{M}_{i,j}^{r}||$，对齐当前生成的 MOFT 与参考 MOFT，并通过梯度 $\frac{\partial\mathcal{L}}{\partial z_t}$ 更新潜在向量 $z_t^{\mathrm{new}} = z_t - \eta\frac{\partial\mathcal{L}}{\partial z_t}$（Eq. 7）。

这一机制的关键优势在于：MOFT 在去噪早期步骤即可提供有效的运动信息（Figure 6，相比 DIFT 在早期步骤的相似度热力图更清晰），使得运动控制能在生成过程的早期阶段介入，从根本上塑造视频的运动轨迹。

### 3. 生成一致性保持：从无特殊处理到共享 K&V 与遮罩梯度裁剪

训练无关的潜在优化面临一个固有挑战：运动引导可能破坏未指定区域的生成一致性。本文通过两项技术解决了这一问题：

- **共享参考分支的 K&V**（Figure 11）：在去噪过程中，将参考生成分支的空间注意力 Key 和 Value 插入运动引导分支，保持内容信息的一致性。
- **遮罩梯度裁剪**（Eq. 8）：将运动引导的梯度 $g$ 在遮罩区域 $\mathcal{R}$ 外裁剪为零 $g^{\mathrm{clip}}$，防止非目标区域受运动损失影响。

Figure 12 的消融显示，共享 K&V 有效维持了整体视频的一致性，而梯度裁剪进一步保护了背景内容（尽管会略微减小运动幅度）。这些技术使得无训练的运动控制能够在不牺牲生成质量的前提下实现精确的局部运动引导。

### 4. 点拖拽的联合优化策略

对于更精细的点拖拽操作，本文提出了一种时变组合损失（Eq. 9）：在去噪早期（$t \ge t_1$）仅使用 MOFT 引导粗运动，中期（$t_1 > t \ge t_2$）结合 MOFT 与 DIFT 的逐点特征对齐损失 $\mathcal{L}^{p}$，后期（$t_2 > t \ge t_3$）仅使用 DIFT 进行精确点定位。Figure 14 的消融证实，单独使用 DIFT 的点拖拽效果有限，单独使用 MOFT 则缺乏精确点控制，二者组合可实现精细的点拖拽效果。

**总结**：本文的核心创新在于将视频扩散模型从“需要训练定制的运动控制器”重新定位为“天然蕴含可提取运动特征的通用基础模型”，通过内容解耦、通道筛选和潜在优化的组合，在完全无需训练的前提下实现了运动方向控制和点拖拽操作，在运动保真度上达到 84.0（Table 1），并在用户评价中同时兼顾运动保真度（3.21）与自然度（3.49）（Table 3）。

## 整体框架

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/006_Figure_5.jpg]]
*Figure 5: Motion Control Pipeline. We use reference MOFT as guidance and optimize latents to alter the sampling process. In one denoising step, we get the intermediate features and extract MOFT from it with content correlation removal and motion channel filter. We optimize the latents to alter the sampling process with the loss of masked MOFT and reference MOFT*

MOFT 引导的运动控制框架是一种**无需训练**的视频生成控制方案。其核心思想是：从视频扩散模型中间层提取的运动特征 MOFT 能够编码纯净的跨帧运动信息，该特征可直接作为潜在优化过程中的引导信号，驱动生成视频按照指定的运动方向或点轨迹运动。

### 基本流水线

框架采用**双分支结构**，整体流程如 Figure 5 和 Figure 11 所示：

1. **参考分支**：对参考视频执行 DDIM 反演（DDIM Inversion），在去噪过程中提取中间层扩散特征，经内容相关性移除和运动通道滤波后得到**参考 MOFT**（$\mathcal{M}^r$）。若无可用的参考视频，也可根据运动方向信号直接合成参考 MOFT。

2. **运动引导分支**：在目标视频的生成去噪过程中，同样提取中间特征并计算 MOFT（$\mathcal{M}$），以参考 MOFT 为监督目标，通过运动控制损失

   $$\mathcal{L}^c = \frac{1}{|\mathcal{R}|} \sum_{(i,j) \in \mathcal{R}} || \mathcal{M}_{i,j} - \mathcal{M}^r_{i,j} ||$$

   对当前去噪步的潜在向量 $z_t$ 执行梯度优化：

   $$z_t^{new} = z_t - \eta \frac{\partial \mathcal{L}}{\partial z_t}$$

   其中 $\mathcal{R}$ 为用户指定的运动控制区域掩码，$\eta$ 为优化学习率。

### 内容一致性保持机制

单纯的运动引导会破坏视频整体内容一致性，为此引入两项关键设计：

- **共享 K&V**：将参考分支空间注意力层中的 Key 和 Value 注入运动引导分支的对应层，使生成内容在结构上与原始生成保持一致。
- **遮罩梯度裁剪**：仅在控制区域 $\mathcal{R}$ 内保留优化梯度，区域外梯度置零：

  $$g^{clip} = \begin{cases} g, & (i,j,k) \in \mathcal{R} \land k \in \mathcal{F} \\ 0, & \text{else} \end{cases}$$

  这保证了非控制区域的背景内容不受运动优化干扰。消融实验（Figure 12）表明，共享 K&V 对维持整体视频一致性贡献显著，而梯度裁剪在保护背景的同时会略微减弱运动幅度。

### 点拖拽的联合优化

对于点拖拽任务，框架采用**时变组合损失**分阶段优化：

$$\mathcal{L}_t = w_t^c \mathcal{L}^c + w_t^p \mathcal{L}^p$$

其中 $\mathcal{L}^p$ 为基于 DIFT 特征的点对齐损失，权重按去噪步 $t$ 动态切换：早期（$t \ge t_1$）仅使用 MOFT 引导粗粒度运动方向；中期（$t_1 > t \ge t_2$）联合 MOFT 和 DIFT；后期（$t_2 > t \ge t_3$）仅用 DIFT 实现精确点定位。这一设计利用了 MOFT 在早期去噪步就能提供有效运动信息的特性（Figure 6），弥补了 DIFT 在早期阶段信息不足的缺陷。

### 特征提取的位置选择

MOFT 从 U-Net 的 **upper block 1** 提取，该层特征空间分辨率较高（相对尺度 2×），能保留更精细的运动空间对应关系。Figure 4(e-h) 的跨层消融证实了该层在运动相似度热力图上表现最优。运动通道的选取通过 PCA 主成分权重确定，保留前约 4% 的通道即可在运动保真度和自然度之间取得最佳平衡（Table 4）。

## 核心模块与公式推导

### 3.1 内容相关性移除

视频扩散模型的中间特征 $\mathcal{X} \in \mathbb{R}^{H \times W \times F \times D}$（其中 $H$、$W$ 为空间维度，$F$ 为帧数，$D$ 为通道数）同时编码了语义结构信息和跨帧运动信息。直接使用原始特征无法有效分离运动信号，因为共享的语义与结构信息会在帧间产生强相关性，淹没运动成分。

为解决此问题，本文提出内容相关性移除操作：对每一帧的特征减去所有帧的均值，从而消除共享内容信息：

$$\mathcal{X}^{\mathrm{norm}} = \mathcal{X} - \frac{1}{F}\sum_{i=1}^{F} \mathcal{X}_i \tag{Eq. 1}$$

其中 $\mathcal{X}_i$ 表示第 $i$ 帧的特征张量。该操作的直觉在于：帧间共享的语义和结构信息在时间维度上近似恒定，减去帧均值后，剩余部分主要反映各帧相对于平均状态的偏离，即运动引起的变化。Figure 2 的 PCA 可视化直接验证了这一点——原始特征的 PCA 投影无法按运动方向分离，而经过内容相关性移除后，不同运动方向（如左移、右移）的特征在主成分空间中清晰可分。

### 3.2 运动通道滤波

内容相关性移除后，并非所有通道都对运动信息有同等贡献。本文通过对 $\mathcal{X}^{\mathrm{norm}}$ 进行 PCA 分析，发现第一主成分 $\mathcal{P}_1$ 的权重分布高度集中：仅有少数通道的权重显著高于其余通道（Figure 3a）。这些高权重通道的跨帧数值变化与视频平移方向高度吻合——例如右移时通道值递减，左移时递增（Figure 3b-c），而非运动通道则无此对应关系（Figure 3d）。

基于此观察，本文定义**运动通道**为对 PCA 主成分贡献最大的前 $k$ 个通道，并据此进行通道选择。设选出的运动通道索引集合为 $\mathcal{C}$，则运动通道滤波即仅保留这些通道的特征。

### 3.3 MOFT 提取

将内容相关性移除与运动通道滤波组合，得到运动特征 MOFT 的完整提取公式：

$$\mathcal{M} = \left( \mathcal{X}_{[j]} - \frac{1}{F}\sum_{i=1}^{F} \mathcal{X}_{i,[j]} \right), \quad j \in \mathcal{C} \tag{Eq. 2}$$

其中 $\mathcal{X}_{[j]}$ 表示第 $j$ 个通道在所有帧上的特征，$\mathcal{C}$ 为运动通道索引集合。MOFT 的提取完全无需训练，仅依赖扩散模型前向传播的中间特征和轻量 PCA 分析。消融实验（Figure 4）表明：仅使用内容移除的特征已能改善运动对应性，而进一步叠加运动通道滤波后，相似度热力图更精准地聚焦于运动区域，且该特性在 AnimateDiff、ModelScope、ZeroScope、SVD 等多种视频扩散模型架构上均成立。

### 3.4 运动控制损失

为实现训练无关的运动控制，本文采用潜在优化策略：在去噪过程中，利用 MOFT 损失引导潜在向量的更新。给定参考 MOFT $\mathcal{M}^r$（可从参考视频通过 DDIM 反转提取，或根据运动方向信号合成），定义运动控制损失为：

$$\mathcal{L}^{c} = \frac{1}{|\mathcal{R}|} \sum_{(i,j) \in \mathcal{R}} ||\mathcal{M}_{i,j} - \mathcal{M}_{i,j}^{r}|| \tag{Eq. 3}$$

其中 $\mathcal{R}$ 为用户指定的运动控制区域（空间掩码），$\mathcal{M}_{i,j}$ 为当前生成过程中提取的 MOFT。该损失驱动受控区域内的运动特征向参考运动特征对齐。

### 3.5 点拖拽组合损失

对于点拖拽任务，本文采用分阶段组合损失，在去噪早期用 MOFT 引导粗粒度运动，后期结合 DIFT 特征实现精确点对齐：

$$\mathcal{L}_{t} = w_{t}^{c} \mathcal{L}^{c} + w_{t}^{p} \mathcal{L}^{p} \tag{Eq. 9}$$

其中 $\mathcal{L}^{p}$ 为点拖拽损失：

$$\mathcal{L}^{p} = \sum_{i=2}^{F} ||\mathcal{D}(p_i) - \mathrm{sg}(\mathcal{D}(p_1))|| \tag{Eq. 4}$$

$\mathcal{D}(\cdot)$ 表示 DIFT 特征提取，$\mathrm{sg}$ 为梯度截断操作。权重 $w_t^c$ 和 $w_t^p$ 按时序分段设置：在 $t \geq t_1$ 阶段仅使用 MOFT 损失进行粗运动控制；在 $t_1 > t \geq t_2$ 阶段联合使用两种损失；在 $t_2 > t \geq t_3$ 阶段仅使用点拖拽损失进行精细对齐；$t < t_3$ 后不再施加任何引导。

### 3.6 潜在优化与一致性保持

潜在向量的更新遵循梯度下降规则：

$$z_t^{\mathrm{new}} = z_t - \eta \frac{\partial \mathcal{L}}{\partial z_t} \tag{Eq. 7}$$

其中 $\eta$ 为优化步长。为在施加运动控制的同时保持非受控区域的内容一致性，本文引入两个关键技术：

**共享 K&V**：在参考分支（无运动引导的标准生成）与运动引导分支之间共享空间注意力层的 Key 和 Value，使受控生成保持与原始生成的内容一致性。

**遮罩梯度裁剪**：将运动控制损失的梯度限制在用户指定的区域 $\mathcal{R}$ 内，非受控区域的梯度直接置零：

$$g^{\mathrm{clip}} = \begin{cases} g, & (i,j,k) \in \mathcal{R} \text{ 且 } k \in \mathcal{F} \\ 0, & \text{否则} \end{cases} \tag{Eq. 8}$$

消融实验（Figure 12）证实共享 K&V 有效维持了整体视频一致性，梯度裁剪则保护了背景内容不受运动引导干扰，但会略微减小运动幅度——这是保真度与自然度之间的一个可控权衡。

## 实验与分析

### 运动特征设计的有效性验证

本方法的核心贡献在于提出了一种无需训练的运动特征提取策略——MOFT。为验证其设计的合理性，作者通过消融实验对比了不同特征设计对运动控制的影响（Table 1）。结果表明，仅使用原始扩散特征时，运动保真度（Motion Fidelity）较低；引入内容相关性移除（Content Correlation Removal）后，性能显著提升；进一步叠加运动通道滤波（Motion Channel Filter），即完整的 MOFT，达到了最高的运动保真度 **84.0**，同时图像质量（Image Quality）仅比原始无引导生成有轻微下降。这一趋势在 Figure 4 的相似度热力图中得到直观印证：原始特征的相似度分布散乱（Figure 4b），内容移除使相似度聚焦到运动区域（Figure 4c），而运动通道滤波则进一步强化了对运动相关区域的精准定位（Figure 4d）。

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/005_Figure_4.jpg]]
*Figure 4: Similarity heatmap between feature of the source point and target features. Given the red source point in (a), we plot the similarity heatmap on target videos. Yellow indicates regions with higher similarity. We normalize all similarity to 0-1 for better illustration. (b-d) Similarity heatmap of features with different designs. “CR” indicates “content removal”. “MCF” indicates motion channel filter. (e-h) Similarity heatmap of MOFT in different layers in the U-Net. (2x) means relative spatial resolution scale 2. (i-l) Similarity heatmap of MOFT in different video generation models*

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/012_Table_1.jpg]]
*Table 1: Experiments on Motion Feature Design Table 3: User Preference*

此外，Figure 4 还揭示了两个关键泛化特性：（1）MOFT 在 U-Net 的不同层（upper block 1 至 up block 2）中均能提取有效的运动对应关系，其中 upper block 1 的表现最为突出（Figure 4e–h）；（2）MOFT 在 **AnimateDiff**、**ModelScope**、**ZeroScope**、**SVD** 等不同架构的视频扩散模型上均展现出鲁棒的运动感知能力（Figure 4i–l），验证了其跨模型泛化性。

### 运动控制的主结果

**运动方向控制。** 在运动方向控制任务上，本方法以训练无关的方式实现了对生成视频运动方向的精细引导。定量评估采用运动保真度指标（Motion Fidelity），该指标通过计算生成视频中跟踪点轨迹与参考运动信号之间的相关性来衡量运动对齐程度。如 Table 1 所示，MOFT 引导的运动控制达到了 **84.0** 的运动保真度。定性结果（Figure 7）展示了多种参考运动信号（包括从参考视频提取和人工合成的方向信号）下的动画效果，生成视频的运动方向与控制信号高度一致，同时保持了自然的运动质感。该方法在 ModelScope 和 ZeroScope 等不同基座模型上同样有效（Figure 8）。

**点拖拽精度。** 在点拖拽任务上，本方法采用分阶段组合损失策略：早期去噪步骤（$t \ge t_1$）仅使用 MOFT 损失 $\mathcal{L}^c$ 进行粗粒度运动引导，中期（$t_1 > t \ge t_2$）联合 MOFT 与 DIFT 损失 $\mathcal{L}^p$，后期（$t_2 > t \ge t_3$）仅使用 DIFT 损失进行精确点对齐。Table 2 报告了点拖拽的平均距离（Mean Distance）为 **0.175**，显著优于仅使用 DIFT 的基线方法（**DIFT** 由 Tang et al., NeurIPS 2024 提出），并大幅缩小了与训练式方法 **DragNUWA**（Yin et al., arXiv 2023）的差距。Figure 14 的消融可视化进一步证实：仅使用 DIFT 时点拖拽效果有限，仅使用 MOFT 则缺乏精确的点级控制，而组合策略实现了精细的点轨迹跟随。

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/013_Table_2.jpg]]
*Table 2: Drag Precision*

**用户偏好研究。** 为评估运动质量的主观感受，作者进行了用户偏好研究（Table 3），对比了本方法与商业模型 **Gen-2**（Runway, 2023）的运动笔刷功能以及 **DragNUWA**。结果显示，Gen-2 的运动保真度极高但自然度较差（运动显得生硬），DragNUWA 的自然度较好但保真度不足。本方法在运动保真度（**3.21** / 5）和运动自然度（**3.49** / 5）之间取得了更均衡的表现，Figure 10 的可视化对比也佐证了这一结论。

### 关键消融实验

**运动通道数量的影响。** Table 4 报告了保留不同比例运动通道对性能的影响。当保留前 **4%** 的运动通道时，运动保真度（84.0）和自然度（0.693）均达到最优。进一步减少通道至 1% 会导致性能显著下降，说明极少数通道承载了核心运动信息，但过度压缩会丢失必要的运动细节。

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/017_Table_4.jpg]]
*Table 4: Motion Channel Ablation*

**视频内容一致性保持。** 为在施加运动控制的同时保持非控制区域的内容不变，本方法引入了两项技术：共享参考分支的 K&V（Key & Value）和遮罩梯度裁剪（Masked Gradient Clip）。Figure 12 的定性对比表明，共享 K&V 有效维持了整体视频内容与原始生成的一致性；梯度裁剪进一步保证了遮罩外区域的稳定性，但会略微减小运动幅度——这是一个保真度与一致性之间的权衡。

**去噪阶段的有效性。** Figure 6 对比了 DIFT 与 MOFT 在不同去噪时间步的相似度热力图。结果显示，在早期去噪阶段（$t=800$），DIFT 的相似度分布几乎无意义，而 MOFT 已能提供有区分度的运动信息。这解释了为何 MOFT 能在早期步骤有效引导粗粒度运动，而 DIFT 仅适用于后期精确对齐。

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/007_Figure_6.jpg]]
*Figure 6: Effects of DIFT and MOFT on different denoising time steps. Given the source point in (a) (for DIFT) and (e) (for MOFT), we plot the similarity heat map of DIFT (b-d) and MOFT (f-h) of different denoising steps. Yellow indicates higher similarity. The red point in (b-d) indicates the position with highest similarity. It suggests that MOFT can provide more valid information than DIFT at the early denoising stages*

### 失败模式与局限性

尽管本方法在训练无关运动控制上取得了显著进展，但仍存在以下局限：

1. **真实视频控制受限。** 当前方法依赖 DDIM Inversion 从参考视频提取 MOFT，但现有视频反转技术的重建质量有限，导致难以直接对真实视频进行运动控制。这一瓶颈有待更强大的反转技术的出现。

2. **运动幅度不可控。** MOFT 仅编码运动方向信息，无法提供精确的运动幅度（scale）控制。这意味着用户只能指定“向哪个方向运动”，而无法精确控制“运动多快或多远”。

3. **生成速度较慢。** 单样本生成约需 **3 分钟**（RTX 3090 GPU），难以满足实时交互需求。这主要源于潜在优化过程需要在多个去噪步骤中进行梯度更新。

4. **复杂运动模式未验证。** 目前所有实验均基于简单平移运动（水平、垂直等），对于旋转、缩放、透视变换等复杂运动模式的泛化能力尚未得到验证，这构成了方法实用性的重要开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/001_Figure_1.jpg]]
*Figure 1: Characteristics of MOtion FeaTure (MOFT). (a-b) Rich Motion Information: We extract MOFT at the red point in the reference video in (a) and draw similarity heatmaps in (b) across various videos (yellow indicates higher similarity). The heatmap aligns well with the motion flow in the bottom left. (c) MOFT serves as guidance for controlling motion direction in the light-masked region, with the motion direction signal illustrated by red arrows in the first image*

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/002_Figure.jpg]]
*Figure: (a) PCA of vanilla feature (b) PCA of feature after correlation removal*

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/003_Figure_2.jpg]]
*Figure 2: Visualization of PCA on video diffusion features. The left side indicates the framewise panning direction, with each color representing a specific direction pattern. We apply PCA to diffusion features extracted from videos with different motion directions and plot their projections on the leading two principle components. (a) The result does not exhibit a distinguishable correlation with motion direction. (b) Features are clearly separated by their motion direction. (a) PC weight hist. on channels*

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/004_Figure_3.jpg]]
*Figure 3: Cross-frame Channel Value. (a) We plot the histogram of the weight of $\mathcal { P } _ { 1 }$ . It reveals that only a few channels significantly contribute to determining the principal components. (b-c) The motion channels exhibit a pronounced correlation with motion direction trends. (d) In contrast, the non-motion channels show little correspondence with motion direction*

![[assets/figures/papers/paper_list_l38_Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controll/figures/009_Figure.jpg]]
*Figure: ZeroScope: A lion lying on the grassland*

## 方法谱系与知识库定位

### 核心瓶颈与动机

视频扩散模型在生成过程中天然蕴含丰富的跨帧运动信息，但现有方法普遍依赖大量训练来定制运动控制（如插入额外的条件模块或运动编码器），导致控制过程不透明、资源消耗大，且缺乏可解释、可跨架构泛化的运动特征提取手段。本文的核心突破在于：**通过内容相关性移除和运动通道滤波，从视频扩散模型的中间特征中提取出纯净的运动特征 MOFT，并直接将其作为训练无关的潜在优化引导信号**，实现了对生成视频的运动方向和点拖拽的精细控制。

### 与现有方法的关系

#### 训练式运动控制方法

当前主流的视频运动控制方法几乎都依赖训练额外的条件模块：

- **Gen-2**（Runway，2023）提供运动笔刷（Motion Brush）功能，允许用户指定编辑区域和运动方向。该方法在运动保真度上表现出色，但以牺牲运动自然度为代价——生成的视频运动往往显得僵硬、不自然（见 Table 3 和 Figure 10 的对比分析）。
- **DragNUWA**（Yin et al.，arXiv 2023）通过训练实现基于点轨迹的运动控制，在点拖拽精度和运动自然度上表现良好，但需要针对特定模型架构进行训练，泛化性受限。
- **MotionCtrl**（Wang et al.，arXiv 2023）提出统一的训练式框架，分别控制相机运动和物体运动，同样面临训练成本高和跨模型迁移困难的问题。
- **VideoComposer**（Wang et al.，NeurIPS 2024）通过额外输入运动矢量作为条件进行训练式视频合成，虽然可控性强，但需要额外的运动矢量标注和模型训练。

本文方法的核心差异在于**完全摒弃训练**：MOFT 直接从预训练视频扩散模型的中间特征中提取，无需任何微调或额外模块训练。这一特性使得 MOFT 天然具备跨架构泛化能力——实验证明，MOFT 在 AnimateDiff、ModelScope、ZeroScope、SVD 等不同架构上均能有效提取运动信息（Figure 4）。

#### 基于扩散特征的语义对应方法

- **DIFT**（Tang et al.，NeurIPS 2024）利用扩散特征进行语义对应，已被用于点拖拽等编辑任务。然而，DIFT 特征在去噪早期阶段缺乏有效的运动信息（Figure 6），导致仅使用 DIFT 的点拖拽效果有限（Figure 14 消融实验证实了这一点）。

MOFT 与 DIFT 的关系是**互补而非替代**：MOFT 在去噪早期阶段即可提供有效的运动信息（Figure 6），适合粗粒度的运动方向控制；DIFT 在去噪后期阶段能提供精确的语义对应，适合细粒度的点拖拽。本文通过时变组合损失（Eq. 9）将二者有机结合：早期用 MOFT 引导粗运动，后期结合 DIFT 实现精确点拖拽，充分发挥了两者的互补优势。

### 方法的关键改进槽位

| 改进槽位 | 基线方法 | 本文方法 | 证据锚点 |
|---------|---------|---------|---------|
| 运动特征提取 | 使用完整扩散特征或额外训练的运动特征提取器 | 无训练的内容相关性移除 + 运动通道滤波得到 MOFT | Eq. 2，Figure 4 |
| 运动控制机制 | 训练附加条件模块（如 MotionCtrl、DragNUWA） | 基于 MOFT 相似度损失，通过优化潜在向量实现训练无关控制 | Sec 4.1，Alg. 1 |
| 生成一致性保持 | 通常无特殊处理或需要额外训练 | 共享参考分支的 K&V 并结合遮罩梯度裁剪 | Sec 8.2，Eq. 8，Figure 12 |

### 适用边界与局限性

尽管 MOFT 在无训练运动控制上展现了显著优势，但其适用边界和局限性同样值得关注：

1. **依赖视频反转技术**：当前方法依赖 DDIM Inversion 从参考视频中提取参考 MOFT。然而，真实视频的反转质量有限，导致难以直接控制真实视频的运动。这意味着 MOFT 目前更适用于**从文本生成视频的运动控制**，而非真实视频的运动编辑。

2. **仅支持方向控制，缺乏幅度控制**：MOFT 能有效编码运动方向信息，但无法提供精确的运动幅度（scale）控制。用户只能指定“向哪个方向移动”，而无法精确指定“移动多快/多远”。这一限制源于 MOFT 本质上是对运动方向的编码，而非对运动矢量的完整建模。

3. **生成速度较慢**：单样本生成约需 3 分钟（RTX 3090 GPU），难以满足实时交互需求。这主要是因为在每个去噪步骤中都需要提取 MOFT 并进行潜在优化，计算开销较大。

4. **复杂运动模式未验证**：目前仅展示了对简单平移运动的控制。对于旋转、缩放、形变等更复杂的运动模式，MOFT 的泛化能力尚未得到验证。PCA 分析（Figure 2）显示特征可按平移方向分离，但复杂运动对应的特征结构可能更为复杂。

5. **运动通道选择依赖手动设定**：消融实验（Table 4）表明，保留前 4% 的运动通道时性能最佳（运动保真度 84.0，自然度 0.693），继续减少通道会导致性能显著下降。这一阈值目前是手动确定的，缺乏自适应选择机制。

### 开放问题

1. **复杂运动模式的扩展**：如何将无训练运动控制从平移扩展到旋转、缩放、仿射变换等更复杂的运动模式？这可能需要更精细的运动通道分析或新的特征分解方法。

2. **真实视频的运动控制**：能否通过改进视频反转技术（如更强的反演模型、更精确的噪声调度）实现真实视频的运动控制？这是将 MOFT 从生成任务扩展到编辑任务的关键。

3. **自适应通道选择**：运动通道滤波的通道数量和选择能否通过自适应或学习的方式优化？例如，是否可以设计一个轻量级的通道重要性预测器，根据输入视频的运动复杂度动态调整通道保留比例？

4. **长视频和高分辨率扩展**：当前实验在 512×512 分辨率、16 帧的设置下进行（生成时间约 3 分钟）。该方法在更长视频（如数百帧）和高分辨率场景下的扩展性如何？计算开销是否会随帧数和分辨率线性增长？

5. **与其他控制信号的融合**：MOFT 目前主要与运动方向和点拖拽信号配合使用。能否将 MOFT 与文本描述、深度图、光流等其他控制信号融合，实现更丰富的运动控制范式？

### 知识库定位总结

MOFT 的核心贡献在于**揭示了视频扩散模型中间特征天然存在的运动感知通道**，并提供了一套简洁高效的训练无关提取与利用方法。这一发现将视频扩散模型从“黑箱生成器”重新定位为“可解释的运动信息源”，为无训练运动控制开辟了新路径。与训练式方法（Gen-2、DragNUWA、MotionCtrl 等）相比，MOFT 在运动保真度上达到 84.0（Table 1），在用户评价中兼顾了运动保真度（3.21）与自然度（3.49）（Table 3），证明了无训练方法可以达到与训练方法竞争的性能水平，同时具备更强的泛化性和更低的部署成本。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/Video_Diffusion_Models_are_Training_free_Motion_Interpreter_and_Controller.pdf]]
