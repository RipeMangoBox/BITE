---
title: Joint 3D Geometry Reconstruction and Motion Generation for 4D Synthesis from a Single Image
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Joint_3D_Geometry_Reconstruction_and_Motion_Generation_for_4D_Synthesis_from_a_Single_Image.pdf
aliases:
- J3GRMG4SFSI
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过统一的扩散模型（4D-STraG）紧密耦合运动生成与几何重建，直接从单张图像联合预测密集4D点轨迹的相对位移，并配合深度引导的运动归一化和运动感知模块（MPM），确保动态与几何的内在一致性。
primary_logic: 密集点云轨迹可作为统一的4D表示，隐式编码几何和运动信息；深度引导的视角归一化实现运动尺度不变性；利用预训练运动特征（OmniMAE）和MAdaNorm向扩散Transformer注入空间自适应的运动先验，实现几何约束与视觉先验的相互正则化。
claims:
- 在VBench基准上，MoRe4D在动态程度（1.0 vs 0.77）和美学质量（0.56 vs 0.49）上显著超越4Real，在主体一致性（0.82 vs 0.80）和美学质量（0.48 vs 0.41）上超越GenXD，在美学质量（0.48 vs 0.36）和成像质量（0.59 vs 0.36）上超越Free4D。
- 消融实验中，移除运动感知模块（MPM）导致动态得分从0.90降至0.85，移除深度隐变量使一致性从0.87降至0.86，证明各模块对运动幅度和一致性的关键作用。
- 联合生成框架在时空一致性上显著优于“Wan2.1-I2V + DELTA/VGGT”的串行流水线，后者因误差累积出现碎片化。
- 在VLM评估中，MoRe4D的运动-几何耦合得分领先于所有基线（如组III中3.35 vs Free4D 1.17和Gen3C 2.01），几何一致性和纹理稳定性也更高。
---

# Joint 3D Geometry Reconstruction and Motion Generation for 4D Synthesis from a Single Image

> [!tip] 核心洞察
> 密集点云轨迹可作为统一的4D表示，隐式编码几何和运动信息；深度引导的视角归一化实现运动尺度不变性；利用预训练运动特征（OmniMAE）和MAdaNorm向扩散Transformer注入空间自适应的运动先验，实现几何约束与视觉先验的相互正则化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 联合三维几何重建与运动生成的单图像4D合成 |
| 英文题名 | Joint 3D Geometry Reconstruction and Motion Generation for 4D Synthesis from a Single Image |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.05044v1) · [Code](https://github.com/Zhangyr2022/MoRe4D) · [Project](https://ivg-yanranzhang.github.io/MoRe4D/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoRe4D |
| Dataset | VBench |

> [!tip] 效果简介
> - VBench 上，Dynamic Degree 1.0000 vs 0.7708 (4Real) (+0.2292)；Aesthetic Quality 0.5613 vs 0.4938 (4Real) (+0.0675)；Subject Consistency 0.8241 vs 0.8042 (GenXD) (+0.0199)。

## 概述

单张图像到4D动态场景的合成是视觉生成领域的前沿难题。现有方法普遍将几何重建与运动生成解耦为两个独立阶段，形成了两种主流范式，但各自存在根本性瓶颈：**generate-then-reconstruct** 方法先合成多视角视频再重建几何，由于生成的视频缺乏严格的几何一致性，重建阶段容易出现结构崩溃和时空碎片化；**reconstruct-then-generate** 方法则先重建静态三维资产再施加运动，受限于预设的静态几何，难以生成大规模、自主性的动态场景。这一“几何-运动解耦”困境构成了当前4D合成的核心瓶颈。

针对上述问题，本文提出 **MoRe4D**——一个先进的 reconstruct-then-generate 框架，其核心创新在于**将运动生成与几何重建紧密耦合**于统一的扩散模型中。该框架的因果机制体现在三个关键设计上：

1. **统一的4D表示**：采用密集4D点云轨迹 $\mathcal{P} \in \mathbb{R}^{T \times N \times 3}$ 作为场景表示，其中 $N = H \times W$ 个点在 $T$ 帧内的三维坐标隐式编码了几何结构与运动信息，使单一模型能够同时预测两者。

2. **深度引导的运动归一化**：基于初始深度的视锥体尺寸对运动分量进行尺度归一化（$\Delta \tilde{x}_t = \frac{\alpha_x \cdot \Delta x_t}{z}$，$\Delta \tilde{y}_t = \frac{\alpha_y \cdot \Delta y_t}{z}$，$\Delta \tilde{z}_t = \frac{\Delta z_t}{z}$），实现不同深度物体的运动感知一致性，消除了绝对尺度对运动预测的干扰。

3. **运动感知先验注入**：通过预训练的 OmniMAE 提取 patch 级运动特征，经 MAdaNorm 对扩散 Transformer 的中间特征进行逐令牌的空间自适应调制，使几何约束与视觉运动先验相互正则化。

在 VBench 基准上，MoRe4D 展现出显著的性能优势：动态程度达到 1.00，较 **4Real**（Yu et al., NeurIPS 2024）的 0.77 提升 0.23；美学质量达到 0.56，较 4Real 的 0.49 提升 0.07；主体一致性达到 0.82，较 **GenXD**（Zhao et al., ICLR 2025）的 0.80 提升 0.02；成像质量达到 0.59，较 **Free4D**（Liu et al., ICCV 2025）的 0.36 提升 0.24。消融实验进一步验证，移除运动感知模块导致动态得分从 0.90 降至 0.85，移除深度隐变量使一致性从 0.87 降至 0.86，证实了各组件对运动幅度和结构一致性的关键作用。

## 背景与动机

### 4D内容生成的范式困境

从单张静态图像合成动态4D内容（即随时间演化的三维场景）是视觉生成领域的前沿课题。当前主流方法可归为两类范式，各自面临结构性瓶颈：

**generate-then-reconstruct（先生成后重建）**：该范式先利用视频扩散模型合成多视角视频序列，再通过结构运动恢复（SfM）或多视图立体匹配重建动态三维几何。代表工作如**4Real**（Yu et al., NeurIPS 2024）和**Gen3C**（Ren et al., CVPR 2025）。其根本缺陷在于：生成的视频帧之间缺乏严格的几何一致性，导致重建阶段出现结构崩溃和碎片化伪影。如附录Figure A所示，将Wan2.1-I2V的视频输出串联DELTA轨迹追踪或VGGT重建时，误差在管线中逐级累积，最终产生严重的时空不一致。

**vanilla reconstruct-then-generate（先重建后生成）**：该范式先从输入图像重建静态三维资产，再对其施加参数化运动或动画。代表工作如**GenXD**（Zhao et al., ICLR 2025）和**DimensionX**（Sun et al., arXiv 2024）。其根本缺陷在于：运动生成受限于预先确定的静态几何，难以产生大规模的自主动态——例如，一个被重建为刚体的物体无法自然地弯曲或变形。这导致生成结果缺乏动态丰富性，在VBench的动态程度指标上表现孱弱。

### 解耦设计的因果瓶颈

上述两类范式的共同症结在于**几何重建与运动生成的解耦**。当这两个子任务被分配给独立的模型或阶段时，几何约束无法正则化运动预测，运动线索也无法反哺几何估计，形成双向的信息断裂。具体表现为：

1. **误差累积**：串行管线中，前序模块的预测误差（如深度估计偏差、轨迹追踪漂移）会被后续模块放大，缺乏联合优化的纠正机制。
2. **尺度歧义**：单目深度估计固有的尺度不确定性，使得不同深度物体的运动幅度难以归一化，导致运动感知不一致。
3. **先验缺失**：纯几何重建缺乏对“哪些区域可能运动”的语义级先验，而纯运动生成缺乏对三维结构的显式约束。

### 本文动机与核心思路

针对上述瓶颈，本文提出**MoRe4D**，核心动机是**将几何重建与运动生成紧密耦合于统一的扩散框架中**，实现双向互正则化。关键洞察在于：**密集4D点云轨迹**可作为统一的中间表示，隐式编码场景的三维几何（通过初始帧点云）和时序运动（通过帧间位移）。通过直接从单张图像联合预测这一表示，模型能够在去噪过程中同时推理“场景长什么样”和“物体怎么动”，从根本上规避解耦范式的不一致性。

为实现这一目标，MoRe4D引入三项机制：
- **深度引导的运动归一化**：以初始深度为基准缩放运动分量，消除尺度歧义。
- **运动感知模块（MPM）**：利用预训练运动特征向扩散Transformer注入空间自适应的运动先验，引导模型关注可运动区域。
- **4D视图合成模块（4D-ViSM）**：基于修复扩散模型填补新视角投影产生的空洞，将点云轨迹转化为连贯视频。

这种联合生成策略在VBench基准上展现出显著优势：动态程度达到1.0（对比4Real的0.77），美学质量达到0.56（对比4Real的0.49），并在VLM评估的运动-几何耦合得分上以3.35大幅领先Free4D（1.17）和Gen3C（2.01）（Table 1, Table A）。

## 核心创新

MoRe4D的核心突破在于**将几何重建与运动生成从解耦的两阶段范式推进为单一扩散模型内的联合推理**，从根本上解决了现有4D合成方法中时空不一致与泛化能力受限的瓶颈。

### 从解耦到耦合：范式转变

现有4D合成方法普遍遵循两种解耦范式（Figure 1）。**generate-then-reconstruct**方法（如**4Real**，Yu et al., NeurIPS 2024）先合成多视角视频，再从中重建几何结构。该路径的致命缺陷在于：生成的视频缺乏严格的几何一致性，重建阶段面临结构崩溃风险，误差在流水线中累积放大。**reconstruct-then-generate**方法（如**GenXD**，Zhao et al., ICLR 2025）则先重建静态3D资产，再对其施加参数化运动。此范式受限于预设的静态几何，难以生成大规模自主动态，运动自由度被严重约束。

MoRe4D提出的**advanced reconstruct-then-generate**框架（Section 4.1）打破了这一僵局：通过统一的扩散模型**4D-STraG**（4D Scene Trajectory Generator），直接从单张图像联合预测密集4D点轨迹的相对位移，使运动生成与几何重建共享同一个推理过程，实现内在的一致性约束。

### 关键创新点（Changed Slots）

| 设计维度 | 基线方法 | MoRe4D | 证据锚点 |
|---------|---------|--------|---------|
| 运动与几何耦合方式 | 解耦两阶段（先视频后重建 / 先重建后动画） | 单一扩散模型联合去噪，同时预测相对运动位移与几何结构 | Section 4.2 |
| 4D场景表示 | 2D视频序列或静态3D资产+参数化运动 | 密集4D点云轨迹 $\mathcal{P} \in \mathbb{R}^{T \times N \times 3}$，$N=H\times W$，隐式编码几何与运动 | Section 4.1 |
| 运动归一化策略 | min-max归一化或无特定归一化 | **深度引导的视角归一化**：基于初始深度$z$的视锥体尺寸缩放运动分量，实现尺度不变性 | Section 4.2, Eq. (1) |
| 几何先验注入 | 无深度隐变量或简单串联 | 深度图经VAE编码后与图像、噪声隐变量串联作为DiT输入 | Section 4.2, Eq. (2) |
| 运动感知先验 | 无运动先验 | 预训练**OmniMAE**提取运动特征，通过**MAdaNorm**对DiT特征进行逐令牌空间自适应调制 | Section 4.2, Eq. (4)-(6) |

### 深度引导的运动归一化

4D点云轨迹中，不同深度物体的绝对运动量差异巨大——近处物体的像素位移远大于远处物体。若直接预测绝对运动，模型将面临尺度混淆。MoRe4D提出深度引导的运动归一化策略（Eq. 1）：

$$\Delta \tilde{x}_t = \frac{\alpha_x \cdot \Delta x_t}{z}, \quad \Delta \tilde{y}_t = \frac{\alpha_y \cdot \Delta y_t}{z}, \quad \Delta \tilde{z}_t = \frac{\Delta z_t}{z}$$

以初始深度$z$为基准，利用视锥体尺寸将绝对运动量转换为尺度不变的相对量。消融实验证实（Table 2），移除该归一化后，一致性从0.8702降至0.8604，点云运动出现不稳定（Figure 6，Row 1-2），验证了深度引导对运动尺度一致性的关键作用。

### 运动感知模块（MPM）

MPM是MoRe4D实现几何约束与视觉先验相互正则化的核心机制。其工作流程如下：

1. **运动特征提取**：利用预训练的OmniMAE从输入图像中提取patch级运动感知特征$\mathbf{S}$，识别潜在的可运动区域与语义结构。
2. **逐令牌参数生成**：通过线性层从$\mathbf{S}$生成自适应缩放和平移参数（Eq. 4）：
   $$\alpha_1, \alpha_2, \beta_1, \beta_2 = \mathrm{Linear}(\mathbf{S})$$
3. **特征调制**：在DiT的注意力层中，对层归一化后的特征施加逐令牌调制（Eq. 5）：
   $$\mathbf{F}' = \mathrm{Attn}(\gamma_1 \alpha_1 \odot \mathrm{LN}(\mathbf{F}_t^i) + \gamma_1 \beta_1)$$
   其中$\gamma_1$为可学习的全局门控系数，控制调制强度。

消融实验表明（Table 2），移除MPM导致动态得分从0.90降至0.85，生成的运动幅度明显减弱（Figure 6，Row 3-4），证明运动感知先验对激发合理动态幅度至关重要。

### 联合框架的优势验证

MoRe4D的联合生成框架在时空一致性上显著优于串行流水线。附录Figure A对比了MoRe4D与“Wan2.1-I2V视频生成 + DELTA跟踪/VGGT重建”的级联方案：串行方法因视频生成误差与跟踪/重建误差的累积，出现明显的碎片化伪影；MoRe4D的联合推理则保持了连贯的时空结构。这一对比直接证明了耦合设计的必要性——当运动与几何在统一扩散过程中相互约束时，二者能够实现有效的相互正则化，避免了解耦范式中的误差传播。

## 整体框架

MoRe4D 提出了一种**紧耦合的重建-再生成（advanced reconstruct-then-generate）**范式，核心思路是将几何重建与运动生成统一在一个扩散框架内，从根本上避免解耦范式中的时空不一致问题。整个 pipeline 由三个关键模块串联构成，其输入输出流如图3所示。

**输入与4D表示。** 系统仅需一张单目RGB图像作为输入。场景被统一表示为密集4D点云轨迹 $\mathcal{P} \in \mathbb{R}^{T \times N \times 3}$，其中 $N = H \times W$ 对应图像分辨率下的空间点数，$T$ 为时间帧数。这一表示隐式编码了场景的几何结构和运动信息——每个点在 $t$ 时刻的3D坐标直接刻画了该点的运动轨迹，而所有点的集合则构成了动态场景的完整几何。

**4D场景轨迹生成器（4D-STraG）。** 这是框架的核心扩散模型，基于DiT（Diffusion Transformer）架构。它接收三路输入：原始图像隐变量 $z_{\mathrm{image}}$、噪声隐变量 $z_{\mathrm{noise}}$ 和深度图经VAE编码后的隐变量 $z_{\mathrm{depth}}$，三者沿特征维度串联后送入DiT进行联合去噪。模型直接预测相对运动 $\Delta \mathbf{P}_t = \mathbf{P}_t - \mathbf{P}_0$，即每帧相对于首帧的3D位移场，而非绝对坐标。这一设计将几何重建（首帧的静态结构由深度先验约束）与运动生成（后续帧的位移）紧密耦合在同一个去噪过程中。

**运动感知模块（MPM）。** 在4D-STraG内部，MPM负责向DiT注入空间自适应的运动先验。它利用预训练的OmniMAE从输入图像中提取patch级运动特征 $\mathbf{S}$，通过线性层生成逐令牌的缩放参数 $\alpha_1, \alpha_2$ 和平移参数 $\beta_1, \beta_2$，再通过MAdaNorm机制对DiT各层的注意力特征进行调制：
$$\mathbf{F}' = \mathrm{Attn}(\gamma_1 \alpha_1 \odot \mathrm{LN}(\mathbf{F}_t^i) + \gamma_1 \beta_1)$$
其中 $\gamma_1$ 是可学习的全局门控系数，控制运动先验的注入强度。MPM使模型能够感知图像中潜在的可运动区域（如关节、肢体），引导运动生成聚焦于语义合理的部位。

**深度引导的运动归一化。** 为解决不同深度物体的运动尺度不一致问题，4D-STraG在训练和推理中采用基于初始深度 $z$ 的视锥体归一化：
$$\Delta \tilde{x}_t = \frac{\alpha_x \cdot \Delta x_t}{z}, \quad \Delta \tilde{y}_t = \frac{\alpha_y \cdot \Delta y_t}{z}, \quad \Delta \tilde{z}_t = \frac{\Delta z_t}{z}$$
该策略将绝对运动量转换为相对于观察视锥体尺寸的尺度不变量，确保近处和远处物体的运动幅度在模型感知上具有一致性。

**4D视角合成模块（4D-ViSM）。** 4D-STraG输出的密集点云轨迹被投影到新视角下，形成带有空洞的渲染视频。4D-ViSM基于Wan2.1视频修复扩散模型，将带噪隐变量、渲染隐变量和下采样掩码串联后送入修复网络，填补投影空洞，生成时空连贯的新视角视频。用户可通过定义相机轨迹自由控制输出视角。

**数据流总结。** 单张图像 → MPM提取运动特征 + UniDepthv2估计深度 → 4D-STraG联合去噪生成密集4D点云轨迹 → 4D-ViSM新视角渲染与修复 → 多视角动态视频。整个pipeline端到端地实现了从静态图像到可控4D内容的生成，几何与运动的耦合贯穿始终。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of MoRe4D. Top: The 4D Scene Trajectory Generator (Sec. 4.2), a Diffusion Transformer, jointly generates geometry and motion. Bottom-Left: The Motion Perception Module (MPM) identifies potential motion regions and semantic structure from the input image. Bottom-Right: The 4D View Synthesis Module (Sec. 4.3) renders the output into novel-view videos*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/001_Figure_1.jpg]]
*Figure 1: MoRe4D for 4D synthesis from a single image. Most existing paradigms either suffer from geometric inconsistencies (generatethen-reconstruct) or are constrained by animating a pre-determined static geometry (vanilla reconstruct-then-generate). Our MoRe4D advances by tightly coupling geometric modeling and motion generation, effectively achieving consistent 4D motion and geometry*

## 核心模块与公式推导

### 4D场景表示：密集点云轨迹

MoRe4D将4D场景统一表示为密集点云序列 $\mathcal{P} \in \mathbb{R}^{T \times N \times 3}$，其中 $T$ 为帧数，$N = H \times W$ 为空间点数。第 $t$ 帧的点云 $\mathbf{P}_t$ 刻画了该时刻场景的完整三维几何，而跨帧的点对应关系则隐式编码了运动信息。这一表示的核心优势在于：几何结构与运动轨迹被耦合在同一数据结构中，无需额外的运动参数化或显式对应场。

### 4D场景轨迹生成器（4D-STraG）

4D-STraG是一个基于扩散Transformer（DiT）的生成模型，其核心任务是直接从单张输入图像预测相对运动位移 $\Delta \mathbf{P}_t = \mathbf{P}_t - \mathbf{P}_0$，即每个空间点在 $t$ 帧相对于初始帧的三维偏移量 $\{[\Delta x_t, \Delta y_t, \Delta z_t]\}$。该设计将几何重建（初始帧点云 $\mathbf{P}_0$）与运动生成（后续帧位移 $\Delta \mathbf{P}_t$）统一于单一去噪过程，从根源上避免了解耦范式中的误差累积。

#### 深度引导的运动归一化

不同深度物体的相同绝对位移在图像平面上会产生截然不同的感知运动幅度——近处物体的微小移动可能比远处物体的大幅移动更加显著。为解决这一尺度歧义，4D-STraG引入深度引导的运动归一化策略：

$$\Delta \tilde{x}_t = \frac{\alpha_x \cdot \Delta x_t}{z}, \quad \Delta \tilde{y}_t = \frac{\alpha_y \cdot \Delta y_t}{z}, \quad \Delta \tilde{z}_t = \frac{\Delta z_t}{z}$$

其中 $z$ 为初始深度值，$\alpha_x$、$\alpha_y$ 为视锥体尺寸相关的缩放系数。该归一化以每个点的初始深度为基准，将其绝对运动量转换为相对于该深度处视锥体尺寸的尺度不变量。消融实验证实（Table 2），移除该归一化后一致性指标从0.8702降至0.8604，美学质量从0.4820降至0.4672，点云运动出现不稳定（Figure 6）。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/009_Figure_6.jpg]]
*Figure 6: Ablation studies on normalization methods and module components. (Rows 1-2) Depth-guided motion normalization stabilizes 4D point cloud generation. (Rows 3-6) Removing the MPM module reduces motion magnitude while excluding depth guidance breaks structural motion consistency, validating our design choices*

#### 几何先验注入：深度隐变量串联

为向DiT注入强几何先验，4D-STraG将深度图经VAE编码后与图像隐变量、噪声隐变量沿特征维度串联：

$$z_{\mathrm{combined}} = \mathrm{Concat}(z_{\mathrm{image}}, z_{\mathrm{noise}}, z_{\mathrm{depth}})$$

这一设计使扩散模型在去噪过程中始终感知场景的三维结构，而非仅依赖RGB外观信息。消融实验表明，移除深度隐变量后一致性降至0.8567，动态得分降至0.85，结构一致性显著受损。

#### 流匹配训练目标

4D-STraG采用流匹配（Flow Matching）框架进行训练，通过最小化预测流场与真实流场之间的误差，学习从噪声到数据的确定性流路径：

$$\mathcal{L}_{\mathrm{fm}} = \mathbb{E}_{t, x_0, x_1}\big[ | v_\theta(t, x_t) - (x_1 - x_0) |^2 \big]$$

其中 $x_0$ 为噪声样本，$x_1$ 为目标数据样本，$v_\theta$ 为DiT预测的速度场。

### 运动感知模块（MPM）

MPM的核心功能是向DiT注入空间自适应的运动先验，引导模型关注场景中可能发生运动的区域。其工作流程分为三个阶段：

**运动特征提取**：利用预训练的OmniMAE模型从输入图像中提取patch级运动感知特征 $\mathbf{S}$，该特征编码了场景中物体的可运动性语义信息。

**逐令牌调制参数生成**：通过线性层将运动特征 $\mathbf{S}$ 映射为逐令牌的缩放和平移参数：

$$\alpha_1, \alpha_2, \beta_1, \beta_2 = \mathrm{Linear}(\mathbf{S})$$

**自适应特征调制（MAdaNorm）**：在DiT的注意力块中，对层归一化后的特征施加逐令牌调制：

$$\mathbf{F}' = \mathrm{Attn}(\gamma_1 \alpha_1 \odot \mathrm{LN}(\mathbf{F}_t^i) + \gamma_1 \beta_1)$$

其中 $\gamma_1 \in \mathbb{R}^d$ 为可学习的全局门控系数，初始化为零以保证训练初期的稳定性。$\alpha_1$ 和 $\beta_1$ 分别对归一化特征进行逐令牌缩放和平移，使模型能够根据空间位置自适应地调整运动生成强度。MLP块中采用类似的调制机制（参数 $\alpha_2$、$\beta_2$，门控 $\gamma_2$）。消融实验表明，移除MPM后动态得分从0.90降至0.85，生成的运动幅度明显减弱（Table 2；Figure 6），验证了运动感知先验对动态生成的关键作用。

### 轨迹编解码与运动敏感VAE

为适配扩散模型的隐空间操作，4D-STraG配备了一个运动敏感VAE，将相对运动位移变换为RGB运动图进行编码，以及从生成的RGB运动图恢复点轨迹。该VAE在重建保真度上表现优异（Figure C），确保了隐空间生成结果能够精确解码为三维运动轨迹。

## 实验与分析

### 主实验结果

MoRe4D在VBench基准上进行了系统的定量对比。由于不同基线方法的能力和实验设置存在差异（如闭源/开源、生成轨迹复杂度不同），作者将对比分为三组进行公平评估（Table 1）：

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on VBench. Higher values are better. The best results in each comparison group are marked in bold*

**Group I：与generate-then-reconstruct范式的对比。** 主要对比对象为**4Real**（Yu et al., NeurIPS 2024），这是当前最强的闭源4D生成方法之一。MoRe4D在动态程度上取得1.0000，远超4Real的0.7708（+0.2292），证明联合框架生成的运动幅度显著更大；在美学质量上达到0.5613，对比4Real的0.4938（+0.0675）；成像质量上为0.6230 vs 0.5095（+0.1135）。这一组结果表明，将运动生成与几何重建解耦的generate-then-reconstruct范式在动态表现力和视觉质量上存在固有瓶颈。

**Group II：与3D重建基线的对比。** 对比对象为**GenXD**（Zhao et al., ICLR 2025），这是从单图进行3D重建的开源方法。MoRe4D在主体一致性上达到0.8241（GenXD为0.8042），背景一致性为0.9044（GenXD为0.8789），美学质量为0.4820（GenXD为0.4077）。值得注意的是，GenXD仅重建静态几何，而MoRe4D同时生成动态内容，却在一致性指标上仍取得领先，说明联合框架中的几何先验和运动感知模块对结构保持起到了关键作用。

**Group III：与4D生成基线的对比。** 对比对象包括**Free4D**（Liu et al., ICCV 2025，免训练方法）和**Gen3C**（Ren et al., CVPR 2025，3D感知视频生成）。MoRe4D在美学质量上以0.4820大幅领先Free4D的0.3607（+0.1213），成像质量上以0.5939领先Free4D的0.3562（+0.2377），背景一致性上以0.9065领先Free4D的0.8883。与Gen3C相比，MoRe4D在主体一致性（0.8241 vs 0.8171）和美学质量（0.4820 vs 0.4102）上均占优。

此外，基于VLM的4D生成一致性评估（Table A）提供了更细粒度的对比。MoRe4D在运动-几何耦合得分上显著领先所有基线：在Group III中，MoRe4D取得3.35，而Free4D仅为1.17，Gen3C为2.01。几何一致性和纹理稳定性指标上同样保持优势，验证了联合框架在时空一致性上的根本性改进。

### 消融实验

为验证各组件的贡献，作者进行了系统的消融实验（Table 2），以完整MoRe4D（一致性0.8702，动态0.9000，美学0.4820）为基准：

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/010_Table_2.jpg]]
*Table 2: Ablation Study. We evaluate the contribution of each component. The best results are marked in bold*

**运动感知模块（MPM）的影响。** 移除MPM后，动态得分从0.9000降至0.8500，降幅达5.6%。定性结果（Figure 6第3-4行）显示，无MPM时生成的运动幅度明显减弱，说明预训练运动特征（OmniMAE）和MAdaNorm调制机制对激发模型的运动生成能力至关重要。进一步的MAdaNorm内部消融（Table C）表明，移除注意力调制或MLP调制均会导致一致性下降。

**深度引导的运动归一化。** 将深度引导归一化替换为min-max归一化后，一致性从0.8702降至0.8604，美学质量从0.4820降至0.4672。Figure 6第1-2行的定性对比显示，min-max归一化导致4D点云运动不稳定，而深度引导归一化通过视锥体尺寸缩放实现了运动尺度不变性，保证了不同深度物体的运动感知一致性。

**深度隐变量的作用。** 移除深度隐变量（即不将深度图经VAE编码后与图像、噪声隐变量串联）导致一致性降至0.8567，动态得分降至0.8500。这表明深度信息作为强几何先验，对DiT在联合去噪过程中维持结构一致性具有不可替代的作用。

**与顺序管线的对比。** 作者将联合框架4D-STraG与“Wan2.1-I2V视频生成 + DELTA跟踪/VGGT重建”的串行流水线进行了定性对比（Figure A）。顺序方法因各阶段误差累积导致明显的碎片化伪影，而联合框架在时空一致性上显著优于串行方案，验证了紧密耦合设计的必要性。

### 失败模式与局限性

尽管MoRe4D在多个指标上取得领先，论文明确指出了以下局限：

1. **计算资源需求高。** 框架依赖大型预训练扩散模型（7B参数的DiT + 14B参数的Wan2.1修复模型），单次生成约需6分钟（NVIDIA A100，Table B），限制了实时应用场景的部署。

2. **深度估计的敏感性。** 4D-STraG依赖UniDepthv2提供初始深度，深度估计错误会导致运动归一化偏差和点云畸变。这在深度不连续区域（如物体边界）尤为突出。

3. **运动类型的分布约束。** 训练数据TrajScene-60K主要包含具有可计数实体和自主动态的场景，模型对无结构运动（如人群流动、水面波纹、烟雾）的泛化能力有限。这是数据集分布带来的固有约束。

4. **新视角渲染伪影。** 4D-ViSM基于视频修复扩散模型，当4D点云在新视角投影产生大范围空洞或极端视角时，修复网络可能产生纹理模糊或结构失真。

5. **评估指标的局限性。** 目前缺乏专门针对生成式4D模型的标准化一致性自动评估指标，现有VBench指标主要面向2D视频质量，对4D时空一致性的刻画不够全面。论文采用的VLM评估（Table A）是初步尝试，但仍需人工验证。

### 关键图表结论

- **Table 1**：MoRe4D在三组对比设置下均取得领先，尤其在动态程度（1.0 vs 0.77）和美学质量（0.56 vs 0.49）上对4Real的优势最为显著。
- **Table 2**：完整MoRe4D在所有指标上达到最优，MPM对动态得分贡献最大（+0.05），深度隐变量对一致性贡献最大（+0.0135）。
- **Figure 6**：定性展示了各模块移除后的退化效果——无MPM运动减弱，无深度归一化点云不稳定，无深度隐变量结构一致性受损。
- **Figure A**：联合框架与顺序管线的定性对比，顺序方法出现碎片化，联合框架保持时空一致性。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison with baseline methods. For each sample, the first row shows the baseline results while the second row presents our MoRe4D results. The first column displays the input image and text prompt*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results of our model. The first row shows the 4D point cloud generated by our 4D-STraG. The second and third rows show the videos rendered by our 4D-ViSM under two distinct, user-defined camera trajectories*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/013_Figure.jpg]]
*Figure: A. Two examples comparing our joint 4D-STraG framework (top row) against sequential pipelines. For each sample, rows 2-4 show results from a cascaded approach: Wan2.1-I2V video generation, followed by DELTA tracking or VGGT reconstruction. Our method yields superior spatio-temporal coherence, while sequential approaches exhibit fragmentation from error accumulation. All samples are consistently rendered from the fixed camera viewpoint for fair comparison*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/011_Table.jpg]]
*Table: A. Quantitative evaluation on 4D Generation Consistency via VLM-based assessment. Higher values are better. The best results in each comparison group are marked in bold*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/015_Table.jpg]]
*Table: C. Ablation study on MAdaNorm. We evaluate the contribution of each component. The best results are marked in bold*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/012_Table.jpg]]
*Table: B. Comparative runtime analysis of 4D generation methods. All timings of open-source methods are measured on single NVIDIA A100 GPU averaged over 100 samples*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2512_05044v1/figures/002_Figure_2.jpg]]
*Figure 2: TrajScene-60K curation pipeline. We curate videos from WebVid-10M, filtered via VLMs for structured motion and countable entities. Dense 4D point tracks are extracted and refined via depth filtering and Gaussian Splatting, producing 60K high-quality 4D scenes*

## 方法谱系与知识库定位

### 1. 问题瓶颈：解耦范式的结构性缺陷

现有单图像4D合成方法可归为两条技术路线，均面临由“解耦”引发的根本性瓶颈：

- **generate-then-reconstruct（先生成后重建）**：先通过视频扩散模型生成多视角视频，再借助3D重建（如DUSt3R、VGGT）恢复几何。该路线的核心缺陷在于生成的2D视频缺乏严格的跨视角几何一致性，导致重建阶段出现结构崩溃和时空碎片化。代表性工作包括**4Real**（Yu et al., NeurIPS 2024）和**DimensionX**（Sun et al., arXiv 2024）。
- **reconstruct-then-generate（先重建后生成）**：先从单图重建静态3D资产，再施加参数化运动或视频先验。该路线受限于预设的静态几何，难以生成大规模自主动态，本质上将运动降级为几何的后处理。代表性工作包括**GenXD**（Zhao et al., ICLR 2025）和**Free4D**（Liu et al., ICCV 2025）。

MoRe4D的核心洞察在于：几何重建与运动生成并非两个独立阶段，而应作为同一推理过程的耦合输出。这一判断由附录Figure A的对比实验直接支撑——将Wan2.1-I2V视频生成与DELTA/VGGT重建串行组合，因误差累积导致输出碎片化，而MoRe4D的联合框架在时空一致性上显著优于该流水线。

### 2. 方法锚点：MoRe4D在谱系中的定位

MoRe4D属于**联合重建-生成范式**，其关键设计选择与现有方法的差异体现在以下维度：

| 维度 | 现有方法 | MoRe4D |
|------|---------|--------|
| 运动与几何的耦合方式 | 解耦的两阶段范式 | 单一扩散模型联合去噪，同时预测相对运动位移和几何结构 |
| 4D场景表示 | 2D视频序列或静态3D资产+参数化运动 | 密集4D点云轨迹 $\mathcal{P} \in \mathbb{R}^{T \times N \times 3}$，隐式编码几何和运动 |
| 运动归一化 | min-max归一化或无特定策略 | 深度引导的视角归一化，基于初始深度的视锥体尺寸缩放运动分量 |
| 几何先验注入 | 无深度隐变量或简单串联 | 深度图经VAE编码后与图像、噪声隐变量串联作为DiT输入 |
| 运动感知先验 | 无运动先验 | 预训练OmniMAE提取运动特征，通过MAdaNorm对DiT特征进行逐令牌调制 |

其中，**密集点云轨迹**作为统一4D表示是MoRe4D区别于所有基线的方法学锚点。该表示将 $N=H \times W$ 个点在 $T$ 帧内的3D坐标序列化，使运动（帧间位移）和几何（初始帧结构）编码于同一张量中，从而在扩散模型的去噪过程中实现相互正则化。

### 3. 知识库定位：与相关领域的关系

MoRe4D的知识贡献跨越三个子领域：

- **单目4D重建**：与DUSt3R、VGGT等前馈3D重建方法不同，MoRe4D不依赖多视角输入，而是从单图直接预测带有时序的密集点轨迹。TrajScene-60K数据集（60K高质量4D场景，源自WebVid-10M）在规模上显著超越现有3D场景理解数据集（Table D），为4D生成提供了训练基础。
- **视频扩散模型**：4D-STraG基于DiT架构，采用流匹配训练目标 $\mathcal{L}_{\mathrm{fm}} = \mathbb{E}_{t,x_0,x_1}[|v_\theta(t,x_t) - (x_1 - x_0)|^2]$，与Stable Diffusion 3等图像生成模型共享扩散范式，但将输出空间从RGB像素扩展为4D运动场。
- **运动感知特征学习**：MPM模块利用预训练的OmniMAE提取patch级运动特征，通过MAdaNorm（Motion Adaptive Normalization）生成逐令牌的缩放和平移参数 $\alpha_1, \alpha_2, \beta_1, \beta_2 = \mathrm{Linear}(\mathbf{S})$，对DiT中间特征进行空间自适应调制。这一设计与ControlNet等空间条件注入方法形成互补——ControlNet注入结构条件，MAdaNorm注入运动先验。

### 4. 适用边界与局限

MoRe4D的能力边界受以下因素约束：

**计算资源需求**：方法依赖大型预训练扩散模型（7B参数的DiT + 14B参数的Wan2.1修复模型），单次生成约需6分钟（单张A100 GPU，512×368分辨率，49帧），限制实时和移动端应用。

**深度估计依赖**：4D-STraG依赖UniDepthv2提供初始深度图。深度估计误差会通过运动归一化公式 $\Delta \tilde{x}_t = \frac{\alpha_x \cdot \Delta x_t}{z}$ 传播，导致运动尺度偏差和点云畸变。在深度模糊区域（如透明物体、镜面反射），该问题尤为突出。

**运动类型泛化**：TrajScene-60K数据集经VLM筛选，偏向具有可计数实体和自主动态的场景（如人物、车辆、动物）。对于无结构运动（人群流动、水面波纹、烟雾扩散），模型的泛化能力有限，这是数据分布约束的直接后果。

**新视角渲染伪影**：4D-ViSM基于视频修复扩散模型填补投影空洞。当相机轨迹导致大范围遮挡区域或极端视角时，修复网络可能产生纹理模糊或几何不连贯的伪影。

### 5. 开放问题

MoRe4D揭示的开放问题指向4D生成领域的几个关键方向：

- **统一架构**：当前MoRe4D仍将运动-几何生成（4D-STraG）与外观渲染（4D-ViSM）分离。能否设计单一非自回归模型，将运动、几何和外观生成进一步纠缠，消除阶段间的信息损失？

- **标准化评估**：4D生成领域缺乏公认的自动化一致性度量。现有VBench指标侧重2D视频质量，VLM评估（Table A）虽能捕捉运动-几何耦合，但依赖特定提示词设计且难以标准化。如何定义可微、可优化的4D一致性损失？

- **通用动态先验**：当前运动先验受限于TrajScene-60K的数据分布。能否构建覆盖流体、人群、形变等更广泛运动类型的通用动态先验？物理模拟（如物质点法、刚体动力学）能否作为训练中的归纳偏置引入？

- **轻量级表示**：密集点云轨迹的存储和计算开销随 $T \times N$ 线性增长。稀疏轨迹、高效神经场（如3D Gaussian Splatting的时序扩展）或分层运动表示能否在保证质量的同时降低计算成本？

- **物理合理性**：模型目前从数据中隐式学习运动模式，但缺乏对物理约束（碰撞、遮挡、重力）的显式建模。能否在训练或推理中引入物理模拟器，使生成的4D场景具备物理合理性？

## 原文 PDF

![[paperPDFs/arxiv_2025/Joint_3D_Geometry_Reconstruction_and_Motion_Generation_for_4D_Synthesis_from_a_Single_Image.pdf]]