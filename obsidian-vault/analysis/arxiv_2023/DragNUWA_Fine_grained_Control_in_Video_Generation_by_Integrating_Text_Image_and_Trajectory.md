---
title: "DragNUWA: Fine-grained Control in Video Generation by Integrating Text, Image, and Trajectory"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/DragNUWA_Fine_grained_Control_in_Video_Generation_by_Integrating_Text_Image_and_Trajectory.pdf
aliases:
- DragNUWA
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 同时引入文本、图像、轨迹三种互补控制，并通过轨迹采样（TS）、多尺度融合（MF）和自适应训练（AT）三个关键技术，使模型能从开放域视频中学习任意轨迹，并提供语义、空间、时间三个维度的精细可控性。
primary_logic: 文本、图像、轨迹分别对应视频的语义、空间、时间三个不可分割的方面；从开放域视频光流中直接采样轨迹并与文本、图像在多尺度下深度融和，配合先学习稠密光流再适应稀疏轨迹的训练策略，可以实现对任意对象、复杂运动轨迹和相机移动的细粒度控制。
claims:
- DragNUWA 能够同时接受文本、图像和轨迹输入，提供从语义、空间和时间角度的细粒度控制。
- 轨迹建模包含三个部分：Trajectory Sampler (TS) 实现开放域任意轨迹控制，Multiscale Fusion (MF) 在不同粒度上融合轨迹，Adaptive Training (AT) 生成一致跟随轨迹的视频。
- 通过改变拖拽轨迹，可以实现不同的相机运动效果（如缩放、平移）和复杂物体运动（曲线轨迹、多物体、变速）。
- 文本、图像、轨迹三种控制缺一不可，分别对应语义、空间、时间维度。
---

# DragNUWA: Fine-grained Control in Video Generation by Integrating Text, Image, and Trajectory

> [!tip] 核心洞察
> 文本、图像、轨迹分别对应视频的语义、空间、时间三个不可分割的方面；从开放域视频光流中直接采样轨迹并与文本、图像在多尺度下深度融和，配合先学习稠密光流再适应稀疏轨迹的训练策略，可以实现对任意对象、复杂运动轨迹和相机移动的细粒度控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | DragNUWA：融合文本、图像和轨迹的细粒度视频生成 |
| 英文题名 | DragNUWA: Fine-grained Control in Video Generation by Integrating Text, Image, and Trajectory |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2308.08089) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | DragNUWA |
| Dataset |  |

> [!tip] 效果简介
> - 轨迹建模包含三个部分：Trajectory Sampler (TS) 实现开放域任意轨迹控制，Multiscale Fusion (MF) 在不同粒度上融合轨迹，Adaptive Training (AT) 生成一致跟随轨迹的视频。

## 概述

**问题瓶颈**：现有视频生成方法对视频内容的控制粒度不足，无法同时从语义、空间和时间三个维度进行精细操控。纯文本控制难以精确表达物体运动轨迹，纯图像控制无法引入新的语义内容，而现有的轨迹控制方法（如 **MCDiff** (Chen et al., arXiv 2023)、**Video Composer** (Wang et al., 2023)）大多局限于特定域（如人体关键点）或简单运动，缺乏在开放域图像上处理复杂曲线轨迹的能力，更无法实现文本、图像、轨迹三者的协同控制。

**核心洞见**：文本、图像和轨迹分别对应视频不可分割的三个维度——语义、空间和时间。只有将三者同时作为控制条件，才能实现真正的细粒度视频生成。

**方法与定位**：**DragNUWA** 是一个端到端的视频生成扩散模型，首次同时引入文本、图像、轨迹三种互补控制模态。其核心创新集中在轨迹建模的三个关键技术组件上：

- **Trajectory Sampler (TS)**：从开放域视频的光流中直接采样稀疏跟踪点，使模型能学习任意轨迹，突破特定域限制。
- **Multiscale Fusion (MF)**：将轨迹和图像条件在多尺度下与文本的交叉注意力深度融合于 UNet 各层，实现不同粒度的控制。
- **Adaptive Training (AT)**：采用两阶段训练策略——先以稠密光流训练稳定视频生成，再以稀疏轨迹微调，使模型适应用户友好的拖拽输入。

**主要结果**：DragNUWA 能够通过改变拖拽轨迹，实现丰富的相机运动效果（如缩放、平移）和复杂的物体运动（如曲线轨迹、多物体并发、变速运动），同时保持文本和图像条件的语义与空间一致性。消融实验验证了三种控制缺一不可，分别对应语义、空间和时间维度（Figure 6）。

**局限与待验证点**：论文主要以定性示例展示能力，缺乏与基线方法在 FVD、用户偏好等定量指标上的系统比较；训练数据为 WebVid-10M 和自收集视频，可能存在域偏差；轨迹控制的精确性和超长轨迹场景下的鲁棒性尚未充分评估，需进一步验证。

## 背景与动机

### 视频生成的细粒度控制困境

视频生成领域近年取得了显著进展，扩散模型的出现使得生成高保真视频成为可能。然而，现有方法在**控制粒度**上存在根本性瓶颈：它们通常只能从单一维度对生成内容施加影响，无法同时兼顾视频的三个不可分割的属性——**语义**（画面中有什么）、**空间**（画面长什么样）和**时间**（画面如何运动）。

具体而言，现有控制范式存在以下缺口：

1.  **文本控制的局限**：以文本提示为唯一条件的生成模型（text-to-video）能够表达高级语义意图，但无法精确指定物体的空间布局和运动轨迹。一句“汽车左转”无法传达转弯的曲率、速度或相机的同步运动。

2.  **图像控制的局限**：以首帧图像为条件的模型（image-to-video）锁定了空间内容和风格，但缺乏对后续帧中物体运动和场景变化的细粒度引导。模型往往只能生成“合理”的运动，而非用户指定的精确运动。

3.  **轨迹控制的局限**：早期尝试引入轨迹作为控制信号的工作，如基于人体关键点的 **MCDiff**（Chen et al., arXiv 2023）或使用运动向量的 **Video Composer**（Wang et al., 2023），大多局限于特定域（如人体动作数据集 Human3.6M）或简单物体运动。这些方法的轨迹来源于特定域的关键点检测器（如 HRNet 提取人体 17 点），无法泛化到开放域图像中的任意对象和复杂曲线轨迹。更重要的是，它们将轨迹视为孤立控制信号，未与文本、图像形成协同，导致生成的视频在语义一致性或空间保真度上存在缺陷。

### 核心动机：语义、空间、时间的统一

DragNUWA 的核心动机源于一个直接洞察：**文本、图像、轨迹分别天然对应视频的语义、空间、时间三个维度，三者缺一不可**。要实现真正意义上的细粒度可控视频生成，必须同时引入这三种互补的控制模态，并让它们深度协同工作。

这一动机驱动了三个关键技术挑战的解决：

-   **如何从开放域视频中获取任意轨迹？** 必须摆脱对特定域关键点检测器的依赖，设计一种通用的轨迹采样机制，使其能处理任意对象和复杂曲线。
-   **如何将轨迹与文本、图像深度融合？** 简单的条件串联或单尺度注入无法让模型理解轨迹在不同空间粒度上的含义（从像素级位移到全局相机运动），需要一种多尺度的融合架构。
-   **如何弥合训练与推理的轨迹分布差异？** 训练时可用的稠密光流与推理时用户提供的稀疏拖拽轨迹之间存在巨大鸿沟，直接使用稀疏轨迹训练会导致生成不稳定，需要一种自适应的训练策略来平滑过渡。

### 本文目标

针对上述困境，DragNUWA 旨在构建一个统一的视频生成框架，**同时接受文本、图像和轨迹作为控制条件**，使模型能够从语义、空间和时间三个角度对生成内容进行细粒度控制。其核心设计围绕**轨迹建模**展开，通过**轨迹采样器（Trajectory Sampler, TS）**实现开放域任意轨迹控制，通过**多尺度融合（Multiscale Fusion, MF）**在不同粒度上融合轨迹，并通过**自适应训练（Adaptive Training, AT）**策略生成一致跟随轨迹的视频。最终，该框架能够处理开放域中多物体、复杂曲线轨迹以及相机运动的并发控制。

## 核心创新

DragNUWA 的核心创新在于将视频生成的**控制范式从单一/双模态扩展为文本-图像-轨迹三模态协同**，并通过三个紧耦合的技术组件——轨迹采样器（Trajectory Sampler, TS）、多尺度融合（Multiscale Fusion, MF）和自适应训练（Adaptive Training, AT）——首次在开放域视频生成中实现了语义、空间、时间三个维度的细粒度可控性。

### 1. 控制模态的根本性扩展：从单模态到语义-空间-时间三元协同

现有视频生成方法在控制粒度上存在根本性瓶颈。文本条件（如 Stable Video Diffusion 系列）仅提供语义层面的粗粒度引导，无法精确指定物体的空间布局与运动轨迹；图像条件（如 Video Composer, Wang et al., 2023）固化了首帧的空间信息，但对后续帧的动态演变缺乏直接约束；轨迹条件（如 MCDiff, Chen et al., arXiv 2023）虽能刻画运动，却局限于人体关键点等特定域，且不与文本、图像深度协同。

DragNUWA 的**核心因果机制**在于认识到：文本、图像、轨迹三者分别对应视频不可分割的语义、空间、时间三个维度，缺一不可。消融实验（Figure 6）通过对比不同控制组合（仅图像 s2v、仅文本 p2v、轨迹+图像 gs2v、文本+图像 ps2v、三者结合 pgs2v）的生成结果，直接验证了这一论断：仅当三模态同时作为条件时，模型才能在保持语义一致性的同时，精确控制物体的空间位置与运动轨迹。

**关键 changed slot**：控制模态从“单一或双模态”跃迁为“文本+图像+轨迹三模态同时注入”，对应证据锚点为摘要中“*we simultaneously introduce text, image, and trajectory information to provide fine-grained control over video content from semantic, spatial, and temporal perspectives*”（置信度 0.95）。

### 2. 轨迹建模的三项关键技术突破

为实现开放域任意轨迹控制，DragNUWA 针对轨迹条件设计了三个相互依存的创新组件，形成了“采样-融合-适应”的完整闭环。

#### 2.1 轨迹采样器（TS）：从特定域关键点到开放域任意轨迹

基线方法（如 MCDiff）依赖 HRNet 等特定域关键点检测器提取人体 17 点，无法泛化至任意对象和场景。DragNUWA 的 **Trajectory Sampler** 直接利用通用光流估计器（Unimatch）从开放域视频中提取稠密光流，再通过**均匀锚点采样**策略动态获取稀疏跟踪点：在空间维度上以间隔 $\lambda$ 均匀分布锚点，并施加 $[-\lambda/2, \lambda/2]$ 的随机偏移 $\delta$ 以覆盖全图区域。这一设计使得模型在训练阶段即可接触到任意对象、任意形状的运动轨迹，从根本上突破了轨迹控制的数据域限制。

**关键公式**——稀疏锚点光流定义：
$$f_{0,i,j}^a = \begin{cases} 0, & \text{else} \\ f_{0,i,j}, & (i+\delta) \% \lambda = 0 \ \& \ (j+\delta) \% \lambda = 0 \end{cases}$$
该公式表明，仅在满足均匀网格条件的空间位置保留光流值，其余位置置零，从而将稠密光流稀疏化为可控数量的跟踪点。随后对稀疏轨迹施加高斯滤波（核大小 99，$\sigma=10$）以增强轨迹图的鲁棒性，便于模型学习。

**关键 changed slot**：轨迹来源从“特定域关键点检测器”变为“通用光流估计器 + 均匀锚点采样”，置信度 0.95。

#### 2.2 多尺度融合（MF）：从简单串联到深层多粒度注入

基线方法通常将轨迹条件与图像/文本简单串联或仅在单一尺度上融合，导致控制信号在 UNet 深层传播时衰减。DragNUWA 的 **Multiscale Fusion** 将图像和轨迹条件下采样到多个尺度，在 UNet 的**每个 block** 内通过零初始化卷积预测缩放参数 $w$ 和平移参数 $b$，以残差形式融入隐藏状态 $h$：
$$h := w_g^{(l)} \cdot h + b_g^{(l)} + h$$
文本条件则通过 Prompt Cross-Attention 机制注入。这种设计确保轨迹控制信号在不同空间粒度上均能有效引导生成过程，使模型既能响应粗粒度的相机运动，也能精确追踪细粒度的物体局部移动。

**关键 changed slot**：条件融合方式从“简单串联/单尺度融合”变为“多尺度深层融合 + 零初始化残差注入”，置信度 0.95。

#### 2.3 自适应训练（AT）：从稠密光流到稀疏轨迹的课程式适应

直接使用稀疏轨迹训练视频扩散模型面临严重的不稳定性问题——稀疏信号难以提供足够的运动约束。DragNUWA 提出**两阶段自适应训练策略**：
- **阶段一**：以稠密光流 $f$ 为条件，使用标准 MSE 损失 $\mathcal{L}_{\theta} = || \epsilon - \epsilon_{\theta}(x_t, p, s, f) ||_2^2$ 训练模型，确保视频生成的动态一致性和稳定性；
- **阶段二**：切换为 Trajectory Sampler 从同一光流中采样得到的稀疏轨迹 $g$ 继续训练，损失函数变为 $\mathcal{L}_{\theta} = || \epsilon - \epsilon_{\theta}(x_t, p, s, g) ||_2^2$，使模型从稠密光流平滑适应到推理时用户提供的稀疏拖拽轨迹。

这一课程式训练策略是 DragNUWA 能够在推理阶段接受用户友好的稀疏轨迹输入、同时保持生成质量的关键。

**关键 changed slot**：训练策略从“直接使用稀疏轨迹或稠密光流”变为“两阶段课程式适应：先稠密后稀疏”，置信度 0.95。

### 3. 创新点的协同效应

上述三项技术并非孤立存在，而是形成紧密的因果链条：**TS 提供了开放域轨迹的获取能力**，使模型能够学习任意运动模式；**MF 确保轨迹信号在多尺度上有效传导**，使控制精度不随网络深度衰减；**AT 弥合了训练信号（稠密光流）与推理信号（稀疏轨迹）之间的分布差异**，使模型在用户友好性和生成质量之间取得平衡。三者共同作用，使得 DragNUWA 能够同时处理相机运动（Figure 4：缩放、平移）、复杂曲线轨迹（Figure 5：曲线、变速、多物体）等此前方法难以统一的控制需求。

### 4. 需要注意的局限性

尽管 DragNUWA 在控制维度上实现了显著扩展，但论文**缺乏与基线方法的定量比较**（如 FVD、用户偏好研究），实验评估主要依赖定性展示。此外，轨迹控制效果的评估缺少客观的运动一致性度量，对超长轨迹或极密集多物体场景下的失败模式未进行系统分析。这些方面需要后续工作进一步验证。

## 整体框架

DragNUWA 的整体框架围绕一个核心设计展开：将文本、图像、轨迹三种互补的控制模态同时注入视频扩散模型，以分别对应视频的语义、空间和时间三个不可分割的维度。该框架以预训练的视频扩散 UNet 为骨干，在其基础上构建了三个关键模块——轨迹采样器（Trajectory Sampler, TS）、多尺度融合（Multiscale Fusion, MF）和自适应训练（Adaptive Training, AT）——以解决开放域任意轨迹控制的核心瓶颈。

### 输入模态与编码

模型接受三种可选输入（Figure 3）：
- **文本 $p$**：通过 CLIP Text Encoder 编码为文本嵌入，用于控制视频的语义内容。
- **图像 $s$**：将视频的首帧重复 $L$ 次后，由预训练的 VQ-GAN 图像自编码器编码为潜在表示，作为空间控制条件。
- **轨迹 $g$**：用户提供的拖拽轨迹或从开放域视频光流中采样得到的稀疏轨迹图，经高斯滤波处理后作为时间控制条件。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_08089/figures/003_Figure_3.jpg]]
*Figure 3: Overview of DragNUWA’s Training Process. DragNUWA supports three optional inputs: text p, image s, and trajectory g, and focuses on designing the trajectory from three aspects. First, the Trajectory Sampler (TS) dynamically samples trajectories from open-domain video flow. Second, Multiscale Fusion (MF) deeply integrates trajectory with text and image within each block of the UNet architecture. Lastly, Adaptive Training (AT) adapts the model from optical flow conditions to user-friendly trajectories. Ultimately, DragNUWA is capable of handling open-domain videos with multiple objects and their complex trajectories*

### 三大核心模块

1. **轨迹采样器 (TS)**：从开放域视频的光流中动态采样稀疏跟踪点。具体而言，在均匀网格（间隔 $\lambda$）上添加随机偏移 $\delta$ 选取锚点，仅保留锚点处的光流值，形成稀疏锚点光流 $f_{0,i,j}^a$：
   $$f_{0,i,j}^a = \begin{cases} 0, & \text{else} \\ f_{0,i,j}, & (i+\delta) \% \lambda = 0 \ \& \ (j+\delta) \% \lambda = 0 \end{cases}$$
   随后对稀疏轨迹施加高斯滤波，增强轨迹图的鲁棒性，使模型能学习开放域中任意对象的复杂运动轨迹。

2. **多尺度融合 (MF)**：将图像条件 $s$ 和轨迹条件 $g$ 下采样到多个尺度，在 UNet 的每个块中与文本条件协同注入。图像和轨迹条件通过零初始化卷积预测缩放参数 $w$ 和平移参数 $b$，以残差方式融入 UNet 隐藏状态 $h$：
   $$h := w_s^{(l)} \cdot h + b_s^{(l)} + h \quad \text{(图像融合)}$$
   $$h := w_g^{(l)} \cdot h + b_g^{(l)} + h \quad \text{(轨迹融合)}$$
   文本条件则通过 Prompt Cross-Attention 注入。这种多尺度深度融合策略使得轨迹控制能在不同粒度上生效，从粗粒度的相机运动到细粒度的物体局部移动。

3. **自适应训练 (AT)**：采用两阶段训练策略。第一阶段以稠密光流 $f$ 为条件训练模型，损失函数为：
   $$\mathcal{L}_{\theta} = \left|\left| \epsilon - \epsilon_{\theta}\left( x_{t}, p, s, f \right) \right|\right|_{2}^{2}$$
   该阶段确保模型学会生成动态一致的视频。第二阶段改用 TS 采样的稀疏轨迹 $g$ 作为条件继续训练：
   $$\mathcal{L}_{\theta} = \left|\left| \epsilon - \epsilon_{\theta}\left( x_{t}, p, s, g \right) \right|\right|_{2}^{2}$$
   这一策略使模型从稠密光流先验平滑迁移到推理时用户提供的稀疏拖拽轨迹，兼顾生成稳定性与控制友好性。

### 数据流与推理

训练时，视频帧经 VQ-GAN 编码为潜在表示 $x_0$，按扩散前向过程加噪得到 $x_t$：
$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{(1 - \bar{\alpha}_t)} \epsilon$$
UNet 以 $x_t$ 和三种控制条件为输入，预测噪声 $\epsilon_{\theta}$。推理时，文本经 CLIP 编码，图像首帧重复 $L$ 次后编码，用户提供的轨迹经高斯滤波和零帧填充后作为条件，从纯噪声迭代去噪生成视频潜在表示，最终由 VQ-GAN 解码器重建为视频帧。

### 控制维度与必要性

消融实验（Figure 6）验证了三种控制的必要性：仅文本到视频（s2v）缺乏空间一致性，仅图像到视频（p2v）无法表达运动，而文本、图像、轨迹三者结合（pgs2v）才能同时实现语义、空间和时间的细粒度控制。这一结果直接支撑了框架设计的核心洞察——三个模态分别对应视频不可分割的三个维度，缺一不可。

## 核心模块与公式推导

DragNUWA 的核心技术贡献在于对**轨迹控制**的全新建模，通过三个紧密协作的模块——轨迹采样器（TS）、多尺度融合（MF）和自适应训练（AT）——首次实现了在开放域视频中对任意轨迹的细粒度控制。这三个模块共同解决了从开放域光流中提取轨迹、将轨迹与文本和图像条件深度融合、以及从稠密光流适应到稀疏用户轨迹的关键瓶颈。

### 1. 轨迹采样器 (Trajectory Sampler, TS)

轨迹采样器是 DragNUWA 实现开放域任意轨迹控制的基础。其核心思想是直接从开放域视频的光流中动态采样稀疏的跟踪点轨迹，而不是依赖特定域的检测器（如人体关键点检测器），从而打破了对简单数据集和特定对象类型的限制。

**采样机制**：TS 首先使用通用光流估计器（Unimatch）计算视频帧间的稠密光流 $f$。随后，在第一帧上均匀分布间隔为 $\lambda$ 的锚点，并添加范围在 $[-\lambda/2, \lambda/2]$ 内的随机偏移 $\delta$，以确保覆盖整个图像区域。仅保留这些锚点处的光流值，形成稀疏的锚点光流 $f^a$：

$$
f_{0,i,j}^a = \begin{cases} 0, & \text{else} \\ f_{0,i,j}, & (i+\delta) \% \lambda = 0 \ \& \ (j+\delta) \% \lambda = 0 \end{cases}
$$

其中，$f_{0,i,j}$ 是第0帧在位置 $(i,j)$ 处的光流向量，$\lambda$ 是锚点间隔，$\delta$ 是随机偏移。通过追踪这些锚点在后续帧中的对应位置，TS 构建出包含 $n$ 个跟踪点的稀疏轨迹集合 $f^s$。

**轨迹增强**：为提升轨迹图的鲁棒性并便于模型学习，TS 对稀疏轨迹 $f^s$ 施加高斯滤波（核大小为99，sigma值为10），得到增强后的轨迹图 $f^g$。这一步骤将离散的跟踪点转化为平滑的轨迹热力图，为后续的多尺度融合提供了更稳定的条件信号。

### 2. 多尺度融合 (Multiscale Fusion, MF)

多尺度融合模块解决了如何将轨迹控制信号与文本、图像控制信号深度整合的问题。与简单的条件串联或单尺度注入不同，MF 在 UNet 架构的每个块中，将轨迹和图像条件下采样到多个尺度，并通过缩放-平移操作融入隐藏状态，实现不同粒度上的轨迹控制。

**条件编码**：文本 $p$ 通过 CLIP 文本编码器编码为嵌入向量，并通过交叉注意力机制注入 UNet。图像 $s$ 由预训练的 VQ-GAN 编码器将第一帧重复 $L$ 次后编码为潜在表示。轨迹 $g$ 则经过高斯滤波和零帧填充后，与图像条件一起被下采样到多个分辨率。

**融合操作**：在每个 UNet 块中，图像条件、掩码条件和轨迹条件分别通过零初始化的卷积层预测缩放参数 $w$ 和平移参数 $b$，然后以残差方式融入隐藏状态 $h$：

图像条件融合：
$$
h := w_s^{(l)} \cdot h + b_s^{(l)} + h
$$

掩码条件融合（指示帧是否为条件帧）：
$$
h := w_m^{(l)} \cdot h + b_m^{(l)} + h
$$

轨迹条件融合：
$$
h := w_g^{(l)} \cdot h + b_g^{(l)} + h
$$

其中，上标 $(l)$ 表示第 $l$ 个 UNet 块的参数。这种多尺度、逐块的深度融合策略使得模型能够在不同抽象层次上感知轨迹信息，从而实现对运动粒度的精细控制。

### 3. 自适应训练 (Adaptive Training, AT)

自适应训练策略是连接模型训练与用户推理的关键桥梁。直接使用稀疏轨迹训练会导致模型难以收敛和生成质量下降，而仅使用稠密光流训练则无法适应用户在推理时提供的稀疏轨迹。

**两阶段训练**：AT 采用先稠密后稀疏的训练范式。

**第一阶段**：以稠密光流 $f$ 为条件训练模型，损失函数为标准扩散模型的均方误差：

$$
\mathcal{L}_{\theta} = \left|\left| \epsilon - \epsilon_{\theta}\left( x_{t}, p, s, f \right) \right|\right|_{2}^{2}
$$

其中，$\epsilon$ 是真实噪声，$\epsilon_{\theta}$ 是模型预测的噪声，$x_t$ 是加噪后的潜在表示，$p$ 是文本条件，$s$ 是图像条件。此阶段确保模型学会生成具有良好动态一致性的视频。

**第二阶段**：使用 TS 从原始光流 $f$ 中采样得到的稀疏轨迹 $g$ 继续训练，损失函数调整为：

$$
\mathcal{L}_{\theta} = \left|\left| \epsilon - \epsilon_{\theta}\left( x_{t}, p, s, g \right) \right|\right|_{2}^{2}
$$

此阶段使模型从依赖稠密光流逐步适应到仅依赖稀疏轨迹，从而在推理时能够泛化到用户提供的任意拖拽轨迹。这种课程式学习策略有效缓解了稀疏控制信号带来的训练困难。

### 4. 扩散过程基础

DragNUWA 的视频生成基于潜在扩散模型框架。前向扩散过程将初始潜在表示 $x_0$ 逐步加噪为 $x_t$：

$$
x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{(1 - \bar{\alpha}_t)} \epsilon
$$

其中，$\bar{\alpha}_t$ 是累积噪声调度参数，$\epsilon \sim \mathcal{N}(0, I)$ 是标准高斯噪声。模型 $\epsilon_{\theta}$ 在文本、图像和轨迹条件的引导下，学习从 $x_t$ 中预测噪声 $\epsilon$，从而在反向去噪过程中生成受控的视频潜在表示。

## 实验与分析

### 实验设置

DragNUWA 的实验在两个分辨率配置下进行：**DragNUWA‑LD** 在 320×192 分辨率上生成 8 帧视频，**DragNUWA‑HD** 在 576×320 分辨率上生成 16 帧视频（Table 1）。训练数据来自 WebVid‑10M 及自收集视频，光流由 Unimatch 估计。轨迹采样器（TS）中最大轨迹数 $N=8$，锚点间隔 $\lambda=16$；高斯滤波核大小为 99，$\sigma=10$。模型使用 Adam 优化器，批大小为 128，学习率 $5\times10^{-6}$。推理时，文本经 CLIP Text Encoder 编码，图像首帧重复 $L$ 次后编码，轨迹经高斯滤波与零帧填充后输入。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_08089/figures/004_Table_1.jpg]]
*Table 1: Implementation details of DragNUWA*

### 相机运动控制

Figure 4 展示了在固定文本和图像条件下，仅改变拖拽轨迹即可实现多种相机运动效果。通过在期望缩放位置绘制方向性轨迹，模型能够生成平滑的 zoom‑in 与 zoom‑out 效果，同时支持水平与垂直平移。这表明 DragNUWA 从开放域光流中隐式学会了相机运动模式，无需显式建模相机参数。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_08089/figures/005_Figure_4.jpg]]
*Figure 4: Various camera movement effects can be achieved by utilizing identical text and images while altering the dragging trajectories. For instance, zoom-in and zoom-out effects can be expressed by drawing the directional trajectories at the desired zoom locations*

### 复杂轨迹与多物体控制

Figure 5 验证了 DragNUWA 对复杂轨迹的控制能力。在相同文本和图像条件下，改变拖拽轨迹可驱动：
- **复杂曲线轨迹**：物体沿弯曲路径运动；
- **可变轨迹长度**：不同物体的运动持续时间可独立控制；
- **多物体并发控制**：同时驱动多个物体沿不同轨迹运动。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_08089/figures/006_Figure_5.jpg]]
*Figure 5: Various complex trajectory effects can be achieved by employing the same text and image while altering the dragging trajectory. DragNUWA supports complex curved trajectories, allows for variable trajectory lengths, and supports concurrent control of trajectories for multiple objects*

这得益于 Trajectory Sampler 从开放域光流中采样多样化的稀疏跟踪点，以及 Multiscale Fusion 在 UNet 各块中深度融入轨迹条件。

### 消融研究：三种控制的必要性

Figure 6 通过比较五种控制组合的生成效果，系统验证了文本、图像、轨迹各自的必要性：

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2308_08089/figures/007_Figure_6.jpg]]
*Figure 6: DragNUWA achieves fine-grained video generation by integrating three essential controls: text, image, and trajectory, corresponding to semantic, spatial, and temporal aspects, respectively*

- **s2v**（仅图像）：能保持空间结构，但无法引入运动；
- **p2v**（仅文本）：可生成语义相关的运动，但空间布局不可控；
- **gs2v**（图像+轨迹）：空间与时间可控，但语义内容受限；
- **ps2v**（文本+图像）：语义与空间可控，但运动模式不可控；
- **pgs2v**（文本+图像+轨迹，即 DragNUWA 完整配置）：**语义、空间、时间三个维度均实现细粒度控制**。

消融结果直接支撑了论文的核心洞见：文本对应语义维度，图像对应空间维度，轨迹对应时间维度，三者缺一不可。

### 实验局限性

本节所呈现的实验结果存在以下局限，需读者注意：

1. **缺乏定量比较**：论文未提供与基线方法（如 MCDiff、Video Composer）在 FVD、FID 或用户偏好等定量指标上的对比，所有控制效果评估均依赖定性观察，结论的统计显著性无法判断。
2. **评估指标缺失**：轨迹控制精度缺乏客观的运动一致性度量（如轨迹跟随误差），仅凭目视判断可能高估模型能力。
3. **数据集偏差风险**：训练数据为 WebVid‑10M 和自收集视频，域覆盖范围未公开，模型在特定领域外的泛化能力未经检验。
4. **失败案例未报告**：未系统展示超长轨迹、极密集多物体场景或高度遮挡条件下的生成失败情况，模型的实际边界尚不明确。

### 关键图表结论

- **Table 1**：提供了两阶段训练、TS/MF/AT 模块的完整超参数配置，是复现工作的核心参考。
- **Figure 4**：证明 DragNUWA 无需显式相机模型即可从开放域轨迹中学习多种相机运动。
- **Figure 5**：证明模型支持曲线轨迹、变长轨迹和多物体并发控制，突破了以往轨迹控制方法的简单场景限制。
- **Figure 6**：通过消融实验直接证实了文本、图像、轨迹三模态互补的必要性，是全文核心主张的关键证据。

## 方法谱系与知识库定位

### 核心瓶颈与突破点

现有视频生成方法在控制粒度上存在明显断层：文本条件（如Stable Diffusion Video系列）仅能提供高层语义引导，无法精确约束物体的空间布局与运动轨迹；图像条件（如Video Composer）固化了首帧外观，却丧失了对时间维度的操控能力；而早期轨迹控制方法（如**MCDiff**, Chen et al., arXiv 2023；**C2M**, Ardino et al., ICCV 2021）虽引入了运动先验，但受限于特定域关键点检测器（如HRNet提取人体17点），仅能在Human3.6M等结构化数据集上工作，无法泛化至开放域图像中的任意物体和复杂曲线轨迹。

DragNUWA的关键突破在于识别出这一瓶颈的本质：**文本、图像、轨迹分别对应视频的语义、空间、时间三个不可分割的维度**，任何单一或双模态控制都会在对应维度上产生失控。因此，其核心创新是将三者同时作为控制条件引入扩散模型，并通过三个专门设计的组件——轨迹采样器（TS）、多尺度融合（MF）和自适应训练（AT）——实现了从开放域视频中学习任意轨迹、并在多粒度上与文本/图像深度协同的能力。

### 与基线方法的关键差异

| 控制维度 | 基线方法 | DragNUWA |
|---------|---------|----------|
| **控制模态** | 单模态或双模态（仅文本、仅图像、或仅轨迹） | 文本 + 图像 + 轨迹 三模态同时控制 |
| **轨迹来源** | 特定域关键点检测器（如HRNet） | 通用光流估计器（Unimatch）+ 均匀锚点采样，支持开放域任意轨迹 |
| **条件融合** | 简单串联或单尺度注入 | 多尺度融合（MF）：轨迹与图像下采样至多个尺度，在UNet各块中与文本交叉注意力同时注入 |
| **训练策略** | 直接使用稀疏轨迹或稠密光流训练 | 两阶段自适应训练（AT）：先学习稠密光流稳定生成，再适应稀疏轨迹以匹配推理时的用户输入 |

具体而言，**MCDiff**仅支持人体动作的轨迹控制，其轨迹来源于人体关键点检测器，无法处理非人体对象或复杂曲线运动。**Video Composer**使用运动向量进行组合式视频合成，但仅支持简单物体运动，缺乏对多物体、曲线轨迹和相机运动的统一建模。**CVG**通过预测光流和扭曲特征实现轨迹控制，但其光流预测依赖于特定域训练，泛化能力有限。DragNUWA通过TS直接从开放域视频光流中采样稀疏跟踪点，突破了这些方法的域限制。

### 适用边界与局限

DragNUWA的适用边界由以下因素决定：

1. **训练数据域偏差**：模型在WebVid-10M和自收集视频上训练，这些数据集的分布特性（如视频长度、场景类型、运动模式）会直接影响模型的泛化能力。对于训练分布外的极端场景（如超长轨迹、极密集多物体交互），模型性能可能下降，但论文未提供系统性的失败案例分析。

2. **轨迹控制精度**：轨迹控制效果目前仅依赖定性观察评估（Figure 4, Figure 5），缺乏客观的运动一致性度量（如轨迹跟随误差、光流一致性指标）。用户提供的轨迹与实际生成运动之间的偏差程度未能量化。

3. **定量比较缺失**：论文未报告与基线方法（MCDiff、Video Composer等）在标准指标（如FVD、IS、用户偏好研究）上的定量比较，这削弱了性能声明的可验证性。当前证据主要来自定性示例，需要后续工作补充定量评估。

4. **推理交互成本**：模型依赖用户提供精确的拖拽轨迹，在实际应用中，用户可能难以对所有期望控制的物体运动进行精确标注，尤其在多物体、复杂场景下。

### 开放问题

1. **超长轨迹扩展性**：DragNUWA在训练时使用8帧（LD）或16帧（HD）的视频片段，对于数百帧的超长轨迹，模型的时间一致性和轨迹跟随能力如何扩展尚不明确。

2. **并发控制的内部机制**：模型如何协调相机运动、多物体运动和复杂曲线轨迹的并发控制？TS、MF和AT三个组件各自的贡献边界和协同机制需要更深入的消融分析。

3. **定量基准建立**：需要建立包含轨迹控制精度的标准化评估基准，包括运动一致性度量、轨迹跟随误差等指标，以客观比较DragNUWA与未来方法。

4. **视频编辑扩展**：DragNUWA目前聚焦于从头生成，其轨迹控制机制能否迁移至视频编辑任务（如局部物体操作、运动重定向、场景理解引导的生成）仍是一个开放问题。

5. **控制精度与内容一致性的权衡**：在开放域中，如何保证轨迹控制的精确性同时维持生成内容的时间一致性和视觉质量，这一权衡机制需要进一步研究。

## 原文 PDF

![[paperPDFs/arxiv_2023/DragNUWA_Fine_grained_Control_in_Video_Generation_by_Integrating_Text_Image_and_Trajectory.pdf]]