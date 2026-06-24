---
title: "MotionClone: Training-Free Motion Cloning for Controllable Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generation.pdf
aliases:
- MotionClone
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过对参考视频的时序注意力权重进行稀疏化（保留每个空间位置上最强的 top-k 个帧间关联，k=1），构造稀疏掩码 M^t，并在扩散采样过程中通过能量函数强制生成视频的注意力图与稀疏参考表征对齐，从而传递主要运动模式。"
primary_logic: "时序注意力图中的主导成分驱动运动合成，其余成分主要捕捉噪声或细微运动；因此，仅对齐稀疏的主导成分即可高效地将参考视频的运动迁移到全新场景，且只需一次去噪步骤即可提取运动表征，无需视频反演或微调。"
claims:
- "时序注意力中的主导成分显著驱动运动合成，其余主要为噪声或细微运动。"
- "稀疏主控（primary control）显著提升运动对齐，强调与运动相关的线索并忽略无关因素。"
- "单步去噪提取的运动表征可提供一致且有效的运动引导，避免繁琐的反演过程。"
- "运动引导仅用于早期去噪步骤，为语义调整留出足够灵活性，实现运动保真与文本对齐的平衡。"
---

# MotionClone: Training-Free Motion Cloning for Controllable Video Generation

> [!tip] 核心洞察
> 时序注意力图中的主导成分驱动运动合成，其余成分主要捕捉噪声或细微运动；因此，仅对齐稀疏的主导成分即可高效地将参考视频的运动迁移到全新场景，且只需一次去噪步骤即可提取运动表征，无需视频反演或微调。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotionClone：面向可控视频生成的免训练运动克隆框架 |
| 英文题名 | MotionClone: Training-Free Motion Cloning for Controllable Video Generation |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2406.05338); [GitHub](https://github.com/LPengYang/MotionClone) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionClone |
| Dataset | 40 real videos (custom dataset), 40 real videos (user study) |

> [!tip] 效果简介
> - 40 real videos (custom dataset) 上，Textual Alignment (CLIP score) 为 0.3187，对比 N/A (best among baselines)，变化 N/A。
> - 40 real videos (custom dataset) 上，Temporal Consistency 为 0.9621，对比 N/A，变化 N/A。
> - 40 real videos (user study) 上，Motion Preservation (1-5 rating) 为 3.69，对比 N/A，变化 N/A。

## 概述

**核心问题**：在无需微调的条件下，如何将参考视频中的运动模式迁移到全新场景中生成可控视频，同时保持对文本提示的高保真度？

**瓶颈发现**：现有方法试图将参考视频的完整时序注意力图作为运动引导，但其中大量成分实为噪声或与运动无关的细微信息，严重稀释了主导运动的引导信号，导致运动克隆效果受限。

**核心方法**：MotionClone 提出**主控运动引导**策略——对参考视频的时序注意力权重进行稀疏化，仅保留每个空间位置上最强的 top-k 个帧间关联（k=1），构造稀疏掩码，并在扩散采样过程中通过能量函数强制生成视频的注意力图与稀疏参考表征对齐，从而精准传递主导运动模式。运动表征仅需对参考视频执行**单次去噪**即可提取，完全绕开了 DDIM 反演或模型微调。

**关键结论**：
- 时序注意力中的主导成分驱动运动合成，其余主要为噪声或细微运动；仅对齐稀疏主导成分即可显著提升运动对齐（Figure 2）。
- 运动引导仅在早期去噪步骤施加，为后期语义调整留出充分灵活性，在运动保真与文本对齐之间取得良好平衡。
- 在 40 个真实视频上的定量评估与用户研究表明，MotionClone 在运动保真度、文本对齐和时序一致性方面均表现优越（Table 1）。

**方法定位**：MotionClone 属于免训练的时序注意力操纵框架，基于预训练文本到视频扩散模型（如 AnimateDiff）的时序注意力层，通过能量函数梯度引导实现运动克隆。相比需要微调或反演的方法（如 Tune-A-Video、VMC），其运动表征提取成本极低；相比使用密集结构条件的 VideoComposer 或 Gen-1，其对参考视频原始结构的依赖更弱，场景泛化能力更强。

**主要局限**：对局部细微运动（如面部微表情）和交织重叠运动的处理能力不足（Figure 10）；定量评估样本量有限（40 个视频），泛化性尚需更大规模验证。

## 背景与动机

### 问题背景：视频生成中的运动控制困境

近年来，文本到视频（T2V）扩散模型在生成质量和多样性上取得了显著进展，但如何精确控制生成视频中的运动模式仍然是一个核心挑战。用户往往希望将一段参考视频中的特定运动——无论是物体运动（如“猎豹奔跑”）还是摄像机运动（如“从左到右的平移镜头”）——迁移到全新的视觉场景中，同时保持对新场景文本描述的忠实响应。这一需求催生了“运动克隆”（motion cloning）这一研究方向。

现有方法在处理运动克隆时面临两类主要瓶颈。第一类方法依赖显式的结构化运动表征，如**VideoComposer**（Wang et al., NeurIPS 2024）使用密集深度图或边缘图作为运动控制信号，**Gen-1**则借助参考视频的原始结构进行视频到视频翻译。这些方法虽然能保留一定的运动信息，但往往过度耦合了参考视频的外观特征，难以在迁移运动的同时彻底解耦场景内容。第二类方法通过微调预训练模型的参数来提取运动模式，如**Tune-A-Video**（Wu et al., ICCV 2023）对时空注意力进行微调以定制单视频运动，**VMC**（Jeong et al., arXiv 2023）则专门微调时序注意力层来提取运动模式。这类方法虽然能实现较好的运动保真度，但每次面对新的参考视频都需要重新训练，计算开销大且灵活性不足。

### 核心瓶颈：时序注意力中的信号污染

MotionClone 的出发点建立在一个关键观察之上：在预训练的 T2V 扩散模型（如 **AnimateDiff**，Guo et al., arXiv 2023b）中，时序注意力层天然编码了视频帧间的运动相关性。然而，直接使用完整的参考视频时序注意力图进行运动引导（即“plain control”）效果有限——这并非因为时序注意力本身缺乏运动信息，而是因为**完整的注意力权重中掺杂了大量与运动无关的噪声和细微运动信号，稀释了主导运动的引导能力**。

具体而言，当对时序注意力图的全部权重施加约束时，生成过程被迫同时对齐参考视频中的主要运动模式、背景噪声以及各种微小的局部抖动。这种“全量对齐”策略使得运动引导信号变得模糊，最终导致生成视频仅能部分恢复粗糙的运动模式，却无法精确复现参考视频中的主导运动轨迹（见 Figure 2）。这一发现揭示了运动克隆的核心瓶颈：**并非时序注意力缺乏运动表征能力，而是需要一种机制从充满噪声的注意力图中精准提取出驱动运动合成的主导成分**。

### 本文动机：稀疏主导运动引导

基于上述观察，MotionClone 的核心动机可以概括为：**时序注意力图中的主导成分驱动运动合成，其余成分主要捕捉噪声或细微运动；因此，仅对齐稀疏的主导成分即可高效地将参考视频的运动迁移到全新场景**。

这一动机直接导向了两个关键设计选择。首先，通过对时序注意力权重进行稀疏化处理——在每个空间位置上仅保留最强的 top-k 个帧间关联（k=1）——可以构造出一个稀疏掩码，将引导信号聚焦于真正驱动运动的主导注意力连接。其次，这种稀疏运动表征可以在单次去噪步骤中直接提取，无需繁琐的 DDIM 反演或模型微调，使得整个运动克隆流程保持“免训练”（training-free）的特性。

此外，MotionClone 还观察到运动引导只需作用于扩散采样的早期步骤，这为后期的语义调整留出了足够的灵活性，从而在运动保真度与文本对齐之间取得平衡。这一设计使得框架能够在不牺牲生成内容多样性的前提下，实现高质量的运动迁移，支持物体运动克隆、摄像机运动克隆，以及图像到视频、草图到视频等多种下游应用场景（Figure 1）。

## 核心创新

MotionClone 的核心创新在于揭示了**时序注意力图中的主导成分驱动运动合成**这一关键洞察，并据此设计了一套免训练的稀疏运动克隆框架。相比于现有方法，其关键改变体现在以下四个维度。

### 1. 稀疏主控替代全量对齐：从噪声中分离运动信号

现有方法（plain control）直接使用参考视频的完整时序注意力图 $\mathcal{A}_{ref}^t$ 进行引导，即令掩码 $\mathcal{M}^t \equiv 1$。这种做法隐含地将注意力图中的所有帧间关联——包括大量与运动无关的噪声和细微抖动——一并注入生成过程，稀释了主导运动的引导信号，导致运动克隆效果有限（Figure 2）。

MotionClone 的**核心因果操作**是引入稀疏掩码 $\mathcal{M}^t$，仅保留每个空间位置上 top-k 个最强帧间关联（k=1）：

$$
\mathcal{M}_{p,i,j}^t := \begin{cases} 1, & \text{if } [\mathcal{A}_{ref}^t]_{p,i,j} \in \Omega_{p,i}^t \\ 0, & \text{otherwise} \end{cases}
$$

其中 $\Omega_{p,i}^t$ 为每个空间位置 $(p,i)$ 上 $\mathcal{A}_{ref}^t$ 中 top-k 值的索引子集。这一操作将运动引导的能量函数从全量对齐：

$$g = \left\| \mathcal{A}_{ref}^t - \mathcal{A}_{gen}^t \right\|_2^2$$

转化为稀疏主控对齐：

$$g = \left\| \mathcal{M}^t \cdot (\mathcal{A}_{ref}^t - \mathcal{A}_{gen}^t) \right\|_2^2$$

消融实验证实，较低的 k 值有利于更好的主运动对齐，k=1 时效果最佳（Figure 8）。这表明**时序注意力中的主导成分显著驱动运动合成，其余成分主要为噪声或细微运动**（confidence: 0.95）。

### 2. 单步去噪运动表征：摆脱反演依赖

现有方法（如 **VMC**，Jeong et al., arXiv 2023）通常需要 DDIM 反演或微调来获取各时间步的时序注意力图，计算开销大且流程繁琐。MotionClone 的关键突破在于发现：**对参考视频仅需一次加噪后执行一次去噪（$t_\alpha = 400$），即可提取出足够有效的运动表征 $\mathcal{H}^{t_\alpha}$**。

具体而言，对于真实参考视频，直接加噪至 $t_\alpha$ 时刻的噪声潜变量，再执行单步去噪，从中提取稀疏运动表征 $\mathcal{L}^{t_\alpha} = \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{ref}^{t_\alpha}$。这一表征可固定用于引导全部采样步，将能量函数简化为时间无关形式：

$$g = \left\| \mathcal{L}^{t_\alpha} - \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{gen}^t \right\|_2^2$$

消融实验表明，单步去噪的运动表征在运动保真度上优于 DDIM 反演方法（Figure 9, “Inversion 1”与“Inversion 2”对比），且 $t_\alpha \in \{200, 400, 600\}$ 均可实现有效运动对齐，仅 $t_\alpha = 800$ 时因噪声过大导致运动信息大量丢失（Figure 8）。

### 3. 早期引导与语义解耦：运动保真与文本对齐的平衡

MotionClone 的另一个关键设计是将运动引导**仅施加于早期去噪步骤**。这一策略的因果逻辑是：扩散模型的早期步骤主要决定视频的全局结构和运动轨迹，后期步骤则负责细节生成和语义细化。通过仅在早期施加运动约束，框架为后期文本条件的语义调整留出足够灵活性，从而在运动保真度与文本对齐之间取得平衡（confidence: 0.9）。

### 4. 方法谱系与知识库定位

MotionClone 定位于**免训练的运动可控视频生成**，其方法谱系可沿两个轴定位：

- **运动控制范式**：不同于 **VideoComposer**（Wang et al., NeurIPS 2024）依赖密集深度或边缘图、**Gen-1** 依赖参考视频原始结构进行视频翻译，MotionClone 直接操作预训练模型内部的时序注意力权重，无需额外结构条件。
- **定制化程度**：不同于 **Tune-A-Video**（Wu et al., ICCV 2023）和 **VMC**（Jeong et al., arXiv 2023）需要针对特定视频微调时空注意力层，MotionClone 完全免训练，仅需一次前向传播即可提取运动表征。

其基础模型可灵活替换为 **AnimateDiff**（Guo et al., arXiv 2023b）或 **SparseCtrl** 等预训练 T2V/I2V 模型，运动表征提取与引导机制作为即插即用模块叠加于现有扩散采样流程之上（Figure 4）。

## 整体框架

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/004_Figure_4.jpg]]
*Figure 4: The pipeline of MotionClone, in which the motion representation $\mathcal { H } ^ { t _ { \alpha } }$ extracted from reference videos serves as motion guidance in novel video synthesis

MotionClone 的整体流程围绕一个核心思想展开：从参考视频中提取稀疏化的时序注意力表征，并将其作为免训练的梯度引导信号，注入到预训练文本到视频扩散模型的采样过程中，从而实现无需微调的运动克隆。图 4 给出了该框架的完整管线。

**运动表征提取器**是管线的入口模块。对于给定的参考视频，框架首先将其加噪至时间步 $t_\alpha$（默认 $t_\alpha = 400$），随后执行**单步去噪**，从基础视频扩散模型（如 AnimateDiff 或 SparseCtrl）的指定时序注意力层中提取该时刻的注意力图 $\mathcal{A}_{ref}^{t_\alpha}$。这一设计直接绕过了传统方法所依赖的 DDIM 反演或逐帧微调，大幅降低了运动表征的获取成本。

**稀疏掩码生成器**紧接着对 $\mathcal{A}_{ref}^{t_\alpha}$ 进行稀疏化处理。具体而言，对于每个空间位置 $p$，仅保留其跨帧注意力权重中最大的 top-$k$ 个值（$k=1$），据此构造二值掩码 $\mathcal{M}^{t_\alpha}$。由此得到的稀疏运动表征 $\mathcal{L}^{t_\alpha} = \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{ref}^{t_\alpha}$ 只编码了参考视频中的主导运动成分，而将噪声和细微运动信息排除在外——这正是方法的核心洞察：时序注意力中的主导成分驱动运动合成，其余成分主要对应噪声或无关细节。

**运动引导能量函数**将上述稀疏表征转化为可微分的约束。在生成视频的采样过程中，该模块计算生成注意力图与固定参考表征之间的加权均方误差：

$$g = \left\| \mathcal{L}^{t_\alpha} - \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{gen}^t \right\|_2^2$$

值得注意的是，引导信号在整个采样过程中**始终使用 $t_\alpha$ 时刻的固定表征 $\mathcal{L}^{t_\alpha}$**，而非每个时间步各自对应的参考注意力图。这一时间无关的设计使得运动表征只需提取一次，即可为全部去噪步提供一致的引导。

**基础视频扩散模型**负责执行条件去噪采样。在每一步去噪中，模型除了接受文本条件的无分类器引导外，还通过能量函数的梯度对潜变量施加运动约束：

$$\epsilon_\theta = \epsilon_\theta(z_t, c, t) + s(\epsilon_\theta(z_t, c, t) - \epsilon_\theta(z_t, \phi, t)) - \lambda \sqrt{1 - \bar{\alpha}_t} \nabla_{z_t} g(z_t, y, t)$$

其中运动引导**仅在早期去噪步骤施加**，为后续步骤留出足够的灵活性，使文本条件能够完成语义调整，从而在运动保真度和文本对齐之间取得平衡。

**输入输出流总结**：参考视频经单步去噪提取 $\mathcal{L}^{t_\alpha}$ 后，与目标文本提示一同送入扩散采样循环。早期去噪步中，运动引导强制生成视频的稀疏时序注意力向参考表征对齐；后期去噪步中，文本引导主导语义生成。最终输出一段既保留参考运动模式、又遵循新文本描述的视频。该框架还支持以首帧图像或草图作为附加条件，拓展至 Image-to-Video 和 Sketch-to-Video 等应用场景。

## 核心模块与公式推导

### 3.1 运动克隆的因果瓶颈与主控策略

MotionClone 的核心发现是：参考视频的时序注意力图中，**主导成分（primary components）显著驱动运动合成，其余成分主要捕捉噪声或细微运动**。这一观察直接定义了方法设计的因果瓶颈——若不加区分地对齐全部时序注意力权重（plain control，即 $M^t \equiv 1$），大量运动无关信号会稀释引导效果，导致运动克隆能力有限（Figure 2）。

基于此，MotionClone 提出**主控（primary control）策略**：仅对齐时序注意力图中的稀疏主导成分，忽略噪声与细微运动。具体而言，对每个空间位置 $p$，从参考视频的时序注意力图 $\mathcal{A}_{ref}^t$ 中选取前 $k$ 个最强的帧间关联（$k=1$），构造稀疏掩码 $\mathcal{M}^t$：

$$
\mathcal{M}_{p,i,j}^t := \begin{cases} 1, & \text{if } [\mathcal{A}_{ref}^t]_{p,i,j} \in \Omega_{p,i}^t \\ 0, & \text{otherwise} \end{cases}
$$

其中 $\Omega_{p,i}^t = \{\tau_1, \tau_2, ..., \tau_k\}$ 是空间位置 $p$ 上 top-$k$ 时序注意力值的索引子集。该掩码将引导信号聚焦于真正驱动运动的主导帧间关联，从而显著提升运动对齐（Figure 2）。

### 3.2 运动表征提取与时间无关引导

传统方法需通过 DDIM 反演或微调获取各时间步的时序注意力图，过程繁琐且引入额外误差。MotionClone 的关键简化在于：**运动表征可从单次去噪步骤中直接提取，无需反演**。

具体流程（Figure 4）：
1. 对参考视频加噪至 $t_\alpha$ 时刻（默认 $t_\alpha = 400$）；
2. 执行**一次去噪步骤**，提取该时刻的时序注意力图 $\mathcal{A}_{ref}^{t_\alpha}$ 及稀疏掩码 $\mathcal{M}^{t_\alpha}$；
3. 计算稀疏运动表征 $\mathcal{L}^{t_\alpha} = \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{ref}^{t_\alpha}$，作为后续全部采样步的固定引导目标。

运动引导通过能量函数 $g$ 实现，强制生成视频的时序注意力图与稀疏参考表征对齐：

$$
g = \left\| \mathcal{L}^{t_\alpha} - \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{gen}^t \right\|_2^2
$$

该式将原本依赖全时间步 $\mathcal{A}_{ref}^t$ 的引导，简化为仅依赖单个时刻 $t_\alpha$ 的固定表征 $\mathcal{L}^{t_\alpha}$。消融实验表明，$t_\alpha \in \{200, 400, 600\}$ 均可实现有效运动对齐，而 $t_\alpha = 800$ 会导致运动信息大量丢失（Figure 8）；DDIM 反演方法在运动保真度上不及单步去噪提取（Figure 9）。

### 3.3 引导采样与施加阶段

运动引导通过修改扩散模型的采样过程实现。在标准无分类器引导的基础上，引入能量函数的梯度项：

$$
\epsilon_\theta = \epsilon_\theta(z_t, c, t) + s(\epsilon_\theta(z_t, c, t) - \epsilon_\theta(z_t, \phi, t)) - \lambda \sqrt{1 - \bar{\alpha}_t} \nabla_{z_t} g(z_t, y, t)
$$

其中 $g$ 即式(6)定义的运动引导能量函数，$\lambda$ 为引导强度。运动引导**仅在早期去噪步骤施加**，为后期语义调整留出足够灵活性，实现运动保真与文本对齐的平衡。

### 3.4 模块总结

MotionClone 的核心模块可归纳为：

| 模块 | 功能 | 关键操作 |
|------|------|----------|
| **运动表征提取器** | 从参考视频获取运动引导信号 | 加噪至 $t_\alpha$，单步去噪，提取 $\mathcal{A}_{ref}^{t_\alpha}$ |
| **稀疏掩码生成器** | 筛选主导运动成分 | top-$k$ 选择（$k=1$），生成 $\mathcal{M}^{t_\alpha}$ 和 $\mathcal{L}^{t_\alpha}$ |
| **运动引导能量函数** | 约束生成视频的运动模式 | 计算 $\|\mathcal{L}^{t_\alpha} - \mathcal{M}^{t_\alpha} \cdot \mathcal{A}_{gen}^t\|_2^2$ |
| **基础视频扩散模型** | 执行条件去噪采样 | AnimateDiff 等预训练 T2V 模型，施加梯度引导 |

消融实验进一步确认：在 `up block.1` 层施加运动引导表现最优，兼顾运动操纵与视觉质量（Figure 9）；使用与参考视频内容匹配的精确文本提示优于通用空文本提示（Figure 9）。

## 实验与分析

### 定量评估与用户研究

MotionClone 在包含 40 个真实视频的自定义基准上进行了评估，涵盖自动指标与用户偏好测试（Table 1）。在自动指标方面，该方法取得了 0.3187 的文本对齐分数（CLIP score）和 0.9621 的时序一致性得分，均优于对比基线。用户研究采用 1–5 分制，从运动保持性、外观多样性、文本对齐和时序一致性四个维度进行评价：MotionClone 在运动保持性上获得 3.69 分，外观多样性 4.31 分，文本对齐 4.15 分，在所有维度上均超过比较方法。

需要指出的是，定量比较仅基于 40 个真实视频，样本量有限，泛化性需进一步验证；用户研究评分具有主观性，论文未报告标准差和统计显著性检验；部分基线方法的详细定量指标未完整提供，难以计算精确提升幅度。

### 定性比较：摄像机运动与物体运动

在摄像机运动克隆场景中（Figure 5），MotionClone 通过更有效地抑制参考视频的原始结构信息，实现了优于对比方法的文本对齐能力——生成视频在保持参考摄像机运动轨迹的同时，更忠实地响应文本提示的语义内容。在物体运动克隆场景中（Figure 6），该方法在运动保真度和提示跟随能力之间取得了更好的平衡，生成的视频既保留了参考视频中的主导物体运动模式，又能根据新文本描述调整外观和场景。

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/007_Figure_6.jpg]]
*Figure 6: Visual comparison in object motion cloning, in which MotionClone performs preferable motion fidelity with improved prompt-following ability. Table 1: Quantitative comparison by using automotive metrics and user study*

### 消融实验

**稀疏度 k 的影响。** k 值决定了时序注意力掩码的稀疏程度（Eq. 5）。实验表明，较低的 k 值有利于更好的主运动对齐，其中 k=1 时效果最佳（Figure 8）。这一结果验证了核心洞察：时序注意力图中的主导成分驱动运动合成，其余成分主要为噪声或细微运动，因此仅对齐稀疏的主导成分即可高效传递运动模式。

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/009_Figure_8.jpg]]
*Figure 8: Influence of different k value and different time step tα*

**时间步 t_α 的影响。** t_α 决定了用于提取运动表征的扩散特征分布。实验显示，t_α=800 时运动信息大量丢失，导致复杂场景（如“转头”）中的运动表征质量显著下降（Figure 3、Figure 8）；t_α∈{200, 400, 600} 均可实现有效的运动对齐，论文默认采用 t_α=400。

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of motion representation. The mean intensity of $\mathcal { L } ^ { t _ { \alpha } }$ in frame axis from “up blocks. . $1 ^ { \dag }$ (resized to the represented resolution) indicates the area and magnitude of motion. This performance encounters decline in complex “head turning” scenario when $t _ { \alpha }$ = 8 0 0

**注意力块的选择。** 将运动引导施加于不同层级的时序注意力块会产生显著差异。在“up block.1”层施加运动引导表现最优，能够在运动操纵能力与视觉质量之间取得最佳平衡（Figure 9）。

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/010_Figure_9.jpg]]
*Figure 9: Influence of different attention block, precise prompt, and DDIM inversion. “Prompt” denotes motion representation involves precise prompt (“Leopard, walks in the forest” for the left case and “Man, turns his head.” for the right case); “Inversion 1” represents the time-dependence $\left\{ \mathcal { A } _ { r e f } ^ { t } , \mathcal { M } ^ { t } \right\}$ from DDIM inversion; “Inversion 2” indicates {Ltα , Mtα } from DDIM inversion

**精确提示的影响。** 使用与参考视频内容匹配的精确文本提示（如“豹子，在森林中行走”）进行运动表征提取，优于使用通用空文本提示，进一步提升了运动克隆的准确性（Figure 9）。

**与 DDIM 反演的对比。** 单步去噪提取的运动表征在运动保真度上优于基于 DDIM 反演的方法——无论是使用时间依赖的 {A_ref^t, M^t} 还是时间无关的 {L^{t_α}, M^{t_α}}（Figure 9）。这表明所提出的单步提取策略不仅简化了流程，还提供了更有效的运动引导信号。

### 失败模式与局限性

MotionClone 在处理两类运动时存在明显不足（Figure 10）：一是局部细微运动（如面部微表情），稀疏注意力机制难以捕捉幅度小、空间范围有限的动作变化；二是交织重叠运动（overlapping motion），当多个运动模式在同一区域叠加时，主导成分的提取策略可能无法有效分离和传递各独立运动分量。

### 拓展应用

该方法可无缝扩展至图像到视频（I2V）和草图到视频（sketch-to-video）生成任务（Figure 7）。通过将第一帧图像或草图作为附加条件输入基础视频扩散模型，MotionClone 在保持参考运动模式的同时，生成与给定条件对齐的视频内容，展现了框架的通用性。

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/008_Figure_7.jpg]]
*Figure 7: MotionClone also supports I2V and sketch-to-video, facilitating versatile applications. The red arrows indicate the motion direction*

### 补充图表

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/011_Figure.jpg]]

![[assets/figures/papers/paper_list_l50_MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generati/figures/015_Figure.jpg]]
*Figure: Prompt: Blue car, runs on the beach. Prompt: Greek sculpture, walks in the forest. Prompt: Cat, turns its head in house*

## 方法谱系与知识库定位

### 与基线工作的关系

MotionClone 的核心贡献在于提出了**免训练的运动克隆范式**，其方法论定位可从运动表征提取、注意力对齐策略和引导机制三个维度与现有工作建立谱系关系。

**运动控制类方法**：**VideoComposer**（Wang et al., NeurIPS 2024）和 **Gen-1** 等通过密集深度图或边缘图等显式结构条件控制运动，需要额外的条件提取模块，且难以将运动与参考视频的原始外观解耦。MotionClone 直接操作时序注意力权重，避免了显式条件提取，实现了运动与外观的分离。

**单视频定制类方法**：**Tune-A-Video**（Wu et al., ICCV 2023）、**VMC**（Jeong et al., arXiv 2023）和 **Control-A-Video**（Chen et al., 2023b）通过对预训练模型的时空注意力层进行微调来提取运动模式。这类方法需要针对每个参考视频进行训练，计算开销大且灵活性受限。MotionClone 的关键突破在于**单步去噪即可提取运动表征**（$t_\alpha=400$），完全免除了微调和反演过程，显著降低了运动克隆的门槛。

**注意力引导类方法**：MotionClone 直接建立在 **AnimateDiff**（Guo et al., arXiv 2023b）等预训练文本到视频扩散模型的时序注意力层之上。与直接对齐全部注意力权重的朴素策略（plain control，$M^t \equiv 1$）相比，MotionClone 的**稀疏主控策略**（primary control，$k=1$）是决定性的改进：通过仅保留每个空间位置上最强的帧间关联，过滤掉噪声和细微运动成分，使运动引导信号更加纯粹有效。Figure 2 的对比实验证实，plain control 仅能部分恢复粗糙的运动模式，而 primary control 显著提升了运动对齐质量。

### 核心创新与因果机制

MotionClone 的方法论创新可归结为三个相互关联的因果节点：

1. **瓶颈识别**：论文发现时序注意力图中的主导成分驱动运动合成，其余成分主要为噪声或细微运动。这一观察（Figure 3 的运动表征可视化）构成了整个方法设计的理论基石。

2. **稀疏化操作**：基于上述观察，引入稀疏掩码 $M^{t_\alpha}$（式 5），通过 top-$k$ 选择（$k=1$）构造运动表征 $L^{t_\alpha} = M^{t_\alpha} \cdot A_{ref}^{t_\alpha}$。消融实验（Figure 8）表明，较低的 $k$ 值有利于更好的主运动对齐，$k=1$ 达到最优。

3. **时间无关引导**：运动引导被简化为固定使用 $t_\alpha$ 时刻的稀疏表征 $L^{t_\alpha}$ 约束全部采样步（式 6），且仅在早期去噪步施加（消融证实 $t_\alpha \in \{200, 400, 600\}$ 有效，$t_\alpha=800$ 导致运动信息大量丢失）。这为后期语义调整留出了足够灵活性，实现了运动保真与文本对齐的平衡。

### 适用边界与局限

**适用场景**：MotionClone 在摄像机运动克隆（Figure 5）和物体运动克隆（Figure 6）场景中表现突出，并支持拓展到图像到视频和草图到视频任务（Figure 7）。方法对预训练模型的时序注意力层有直接依赖，当前实现基于 AnimateDiff 和 SparseCtrl。

**已知局限**：
- **局部细微运动**：对微表情等局部细微运动处理能力不足（Figure 10 左侧案例）。
- **重叠运动**：当多个运动模式交织重叠时，稀疏注意力可能无法有效分离和传递各运动成分（Figure 10 右侧案例）。
- **定量验证规模有限**：主要定量比较仅基于 40 个真实视频，样本量有限，且用户研究未报告标准差和统计显著性检验，泛化性需更大规模验证。
- **伦理风险**：方法可能被滥用于生成深度伪造或误导性媒体内容，论文也明确指出了负责任的部署与监管需求。

### 开放问题

1. **复杂运动建模**：如何扩展稀疏注意力机制以更好地处理局部细微运动和重叠运动？是否需要引入多尺度或分区域的运动表征？
2. **反演策略改进**：消融实验（Figure 9）显示单步去噪的运动表征优于 DDIM 反演方法，但能否结合更精确的反演策略（如更优的时间步选择或噪声调度）进一步提升运动保真度？
3. **鲁棒性验证**：在更大规模、更多样化的参考视频集上，稀疏注意力方法的鲁棒性如何？$k=1$ 的极端稀疏设置是否在所有运动类型上都是最优选择？
4. **与微调方法的融合**：免训练范式提供了灵活性，但能否与轻量微调结合，在特定场景下进一步提升运动克隆的精度？

## 原文 PDF

![[paperPDFs/ICLR_2025/MotionClone_Training_Free_Motion_Cloning_for_Controllable_Video_Generation.pdf]]
