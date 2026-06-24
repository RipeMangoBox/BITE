---
title: "VideoAnydoor: High-fidelity Video Object Insertion with Precise Motion Control"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Control.pdf
aliases:
- VideoAnydoor
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "像素变形器（Pixel Warper）利用参考图像上的关键点与对应轨迹图，通过内容/运动编码器与交叉注意力融合，将像素细节显式地变形到目标区域，使外观细节与运动控制联合建模。"
primary_logic: "通过端到端的框架，将ID提取器（DINOv2）的全局身份信息与边界框序列的粗粒度运动控制，以及像素变形器的细粒度外观-运动联合建模相结合，可在零样本条件下实现高保真视频物体插入，并精确跟随用户指定的轨迹。"
claims:
- "定量对比中VideoAnydoor在所有自动指标（CLIP-Score、DINO-Score、PSNR、AJ、δavg、OA）上均显著超越对比方法。"
- "移除像素变形器后，ID保留和运动一致性指标大幅下降（PSNR 59.1→33.8, CLIP-Score 81.4→72.4, AJ 88.3→78.5）。"
- "用户研究中VideoAnydoor在质量、保真度、运动流畅度、多样性上均获得最优评分（Quality 3.75, Fidelity 3.80, Smooth 3.65, Diversity 3.70 out of 4）。"
- "定性消融表明，缺少像素变形器时视频出现运动不一致和不正确的物体姿态。"
---

# VideoAnydoor: High-fidelity Video Object Insertion with Precise Motion Control

> [!tip] 核心洞察
> 通过端到端的框架，将ID提取器（DINOv2）的全局身份信息与边界框序列的粗粒度运动控制，以及像素变形器的细粒度外观-运动联合建模相结合，可在零样本条件下实现高保真视频物体插入，并精确跟随用户指定的轨迹。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VideoAnydoor：高保真视频物体插入与精确运动控制 |
| 英文题名 | VideoAnydoor: High-fidelity Video Object Insertion with Precise Motion Control |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2501.01427); [Project](https://videoanydoor.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoAnydoor |
| Dataset | Custom benchmark (200 videos from Pexel), Custom benchmark (200 videos), User study |

> [!tip] 效果简介
> - Custom benchmark (200 videos from Pexel) 上，OA (Overall Alignment) 为 92.5，对比 83.2 (ReVideo)，变化 +9.3。
> - Custom benchmark (200 videos) 上，CLIP-Score (↑) 为 38.0。
> - Custom benchmark (200 videos) 上，DINO-Score (↑) 为 81.4。

## 概述

**问题瓶颈**。现有视频物体插入方法（如 **AnyV2V** (Ku et al., arXiv 2024)、**ReVideo** (Mou et al., arXiv 2024) 等）普遍采用两阶段方案——先修改首帧再将编辑传播至后续帧。这种范式存在两个根本缺陷：首帧插入质量本身欠佳，且后续帧缺乏显式的身份信息注入，导致物体身份一致性差、运动控制不准确，难以在保持高保真外观细节的同时实现精细的运动轨迹对齐。

**核心洞察**。VideoAnydoor 提出端到端的零样本视频物体插入框架，将三个关键能力联合建模：① 使用 **DINOv2** 作为 ID 提取器，从去背景的参考图像中提取紧凑的身份令牌，注入扩散 U-Net 实现全局身份保持；② 通过边界框序列提供粗粒度运动控制；③ 设计**像素变形器（Pixel Warper）**，利用参考图像上的关键点与对应轨迹图，经内容/运动编码器与交叉注意力融合后送入 ControlNet，将像素细节显式地变形到目标区域，实现细粒度外观-运动联合建模。此外，图像-视频混合训练策略与轨迹加权损失进一步增强了细节对齐与运动控制精度。

**主要结果**。在 200 个 Pexel 视频构成的基准测试上，VideoAnydoor 在所有自动指标（CLIP-Score、DINO-Score、PSNR、AJ、δavg、OA）上均显著超越对比方法（Table 2）。用户研究中，VideoAnydoor 在质量、保真度、运动流畅度、多样性四个维度均获得最优评分（Quality 3.75, Fidelity 3.80, Smooth 3.65, Diversity 3.70 / 4.0，Table 3）。消融实验表明，移除像素变形器后 ID 保留和运动一致性指标大幅下降（PSNR 59.1→33.8, CLIP-Score 81.4→72.4, AJ 88.3→78.5），定性结果亦出现运动不一致与错误姿态（Table 4-5, Figure 7），验证了该模块的核心作用。

## 背景与动机

视频物体插入（video object insertion）旨在将给定参考图像中的物体无缝嵌入目标视频，并使其在时间维度上保持身份一致性与运动连续性。该任务在虚拟试穿、视频编辑、数字人驱动等场景中具有广泛的应用前景，但其核心挑战在于：**如何在精确跟随用户指定运动轨迹的同时，完整保留物体的高保真外观细节**。

现有方法大多采用两阶段方案。以 **AnyV2V**（Ku et al., arXiv 2024）和 **ReVideo**（Mou et al., arXiv 2024）为代表的工作，通常先在首帧进行物体插入，再通过视频传播模型将编辑结果扩散至后续帧。这一范式存在两个结构性缺陷：

1. **身份信息注入不足**：首帧插入往往依赖外部图像编辑模型，其输出质量参差不齐；更关键的是，后续帧的生成过程缺乏对参考物体身份特征的显式注入，导致物体外观在时间轴上逐渐漂移或失真。
2. **运动控制与外观细节解耦**：现有方法多通过 ControlNet 等控制模块直接注入轨迹条件，但这种粗粒度的条件信号缺乏与参考图像像素之间的语义对应关系。模型难以在保持外观细节的同时实现精细的运动轨迹对齐——要么运动准确但外观模糊，要么外观清晰但运动不一致。

上述瓶颈的本质在于：**外观身份保持与运动控制被当作两个独立的问题分别处理，缺乏一个联合建模的机制**。视频物体插入需要的不是“先生成再对齐”，而是让物体的像素细节在生成过程中就按照目标轨迹进行变形与融合。

针对这一缺口，本文提出 **VideoAnydoor**，一个端到端的零样本视频物体插入框架。其核心设计思路是将全局身份注入、粗粒度运动控制与细粒度像素变形三者统一于扩散生成过程之中，使模型能够在保持高保真外观的同时精确跟随用户指定的边界框序列或关键点轨迹。

## 核心创新

VideoAnydoor 的核心创新在于将视频物体插入任务中的**外观身份保持**与**精确运动控制**统一到一个端到端框架中，解决了现有两阶段方案（如 AnyV2V、ReVideo）存在的首帧插入质量差、后续帧缺乏身份信息注入的根本瓶颈。

### 1. 像素变形器：外观细节与运动轨迹的联合建模

像素变形器（Pixel Warper）是本方法最关键的技术贡献。其设计动机源于一个因果机制：现有方法仅通过 ControlNet 等控制模块直接注入轨迹条件，缺乏参考图像与目标区域之间的显式语义对应，导致像素级细节无法随运动轨迹准确变形。像素变形器通过以下流程实现细粒度的外观-运动联合建模：

- **轨迹采样**：利用 X-Pose 在首帧初始化关键点，经非极大值抑制（NMS）过滤密集点后，保留运动幅度最大的 $N$ 个点，确保关键点稀疏分布于物体各部位且包含丰富运动信息（Figure 3）。
- **内容/运动双编码**：将标有关键点的参考图像 $c_{ref-key}$ 与对应轨迹图 $c_{mot}$ 分别送入内容编码器 $E_c$ 和运动编码器 $E_m$，提取的特征经两个交叉注意力模块融合。
- **多尺度特征注入**：融合结果作为 ControlNet 的输入，提取多尺度特征 $\mathbf{f}_c$，通过零卷积处理后与扩散 U-Net 原始特征相加：

$$\mathbf{y}_c = \mathcal{F}(\mathbf{z}_t, t, \mathbf{c}_{ref}; \boldsymbol{\Theta}) + \mathcal{Z}(\mathcal{F}(\mathbf{z}_t + \mathcal{Z}(\mathbf{f}_c), t, \mathbf{c}_{ref}; \boldsymbol{\Theta}_c))$$

这一设计使像素细节能够显式地按照用户指定的轨迹变形，同时保持物体身份的一致性。消融实验提供了决定性证据：移除像素变形器后，PSNR 从 59.1 骤降至 33.8，CLIP-Score 从 81.4 降至 72.4，AJ 从 88.3 降至 78.5（Table 4, Table 5），定性结果也显示运动不一致和物体姿态错误（Figure 7）。

### 2. 身份信息注入：DINOv2 全局身份令牌

与基线方法仅使用 CLIP 等全局嵌入或完全缺乏身份注入不同，VideoAnydoor 采用 DINOv2 作为 ID 提取器，从去背景且居中对齐的参考图像中提取紧凑的、具有区分性的身份令牌，并注入扩散 U-Net。消融表明，固定 DINOv2（不进行适应性训练）会导致性能大幅下降，验证了可训练 ID 提取器对身份保持的关键作用。

### 3. 图像-视频混合训练与轨迹加权损失

针对高质量视频训练数据稀缺的问题，VideoAnydoor 设计了两个互补策略：

- **图像-视频混合训练**：通过人工相机操作（等间隔平移、逐步裁剪）将高质量静态图像扩充为伪视频，与真实视频混合训练，并采用自适应时间步采样区分不同模态的贡献。消融显示，仅使用视频训练会导致运动一致性显著退化（AJ 88.3→71.4，Table 5）。
- **轨迹加权损失**：对预测误差进行重新加权，使覆盖较大运动幅度的轨迹区域获得更大权重：

$$\mathcal{L} = \sum_{i=1}^{N} ((\lambda R_i \mathbf{A}_{trj}^i + (1 - \mathbf{A}_{trj}^i) / N) \cdot \|\delta - \delta^*\|_2^2)$$

其中 $R_i$ 为轨迹覆盖面积比率，$\mathbf{A}_{trj}^i$ 为轨迹区域掩码。该损失相比简单边界框损失带来显著性能提升，使模型更聚焦于前景区域的运动控制精度。

### 创新总结

VideoAnydoor 的三项核心创新——像素变形器、DINOv2 身份注入、混合训练与加权损失——形成了完整的因果链条：**像素变形器提供细粒度外观-运动联合建模，ID 提取器保证全局身份一致性，混合训练与加权损失则从数据和优化层面增强了模型对高质量细节和精确运动的拟合能力**。这一组合使 VideoAnydoor 在零样本条件下实现了超越所有对比方法的性能，并在用户研究中获得最优评分（Quality 3.75, Fidelity 3.80, Smooth 3.65, Diversity 3.70 out of 4，Table 3）。

## 整体框架

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline of trajectory generation for training data. We first perform NMS to filter out densely-distributed points and then select points with larger motion. The retained ones can be sparsely distributed in each part of the target and contain more motion information, thus inducing more precise control*

VideoAnydoor 采用端到端的零样本视频物体插入框架，核心设计目标是在保持高保真外观细节的同时，实现精确的运动轨迹控制。整体 pipeline 由三个功能层次构成：**全局身份注入**、**粗粒度运动控制**与**细粒度外观-运动联合建模**。

### 输入与预处理

框架接收三类输入：原始视频 $V \in \mathcal{R}^{N \times 3 \times H \times W}$、物体掩码序列、以及一张参考图像。参考图像首先经过**背景移除与物体居中对齐**预处理，为后续身份提取提供干净输入。原始视频与掩码视频分别经 VAE 编码器投影到潜在空间，再通过 DDIM Inversion 将干净潜在变量逆扩散为噪声潜在变量 $z_T$，作为扩散模型的起点。

### 全局身份注入

经预处理的参考图像送入 **ID 提取器**（基于 DINOv2），提取紧凑且具有判别力的身份令牌。这些令牌被注入到 3D U-Net 中，为整个生成过程提供全局物体身份约束。与现有两阶段方案（如 **AnyV2V**（Ku et al., arXiv 2024）、**ReVideo**（Mou et al., arXiv 2024））仅在首帧进行外观设定、后续帧缺乏身份信息注入不同，VideoAnydoor 的身份令牌贯穿所有帧的去噪过程，从源头抑制了身份漂移。

### 粗粒度运动控制

3D U-Net 接收 9 通道拼接输入（$z_T$、掩码潜在变量、掩码视频潜在变量），同时注入**边界框序列**作为粗粒度运动控制信号。该 U-Net 集成了运动层，确保生成视频的基础时序一致性，并完成背景修复。边界框序列定义了物体在每一帧中的大致位置与尺度，为后续细粒度控制提供空间先验。

### 细粒度外观-运动联合建模：像素变形器

像素变形器（Pixel Warper）是框架的核心创新，负责将参考图像的像素细节按用户指定的轨迹精确变形到目标区域。其工作流程如下：

1. **轨迹采样**：使用 X-Pose 在首帧初始化关键点，经非极大值抑制过滤密集点，保留运动幅度最大的 $N$ 个关键点，生成轨迹图 $\dot{c}_{mot} \in \mathcal{R}^{N \times 3 \times H \times W}$ 和带关键点标注的对应参考图像 $c_{ref-key}$。
2. **双编码器编码**：内容编码器 $E_c$ 处理参考图像，运动编码器 $E_m$ 处理轨迹图，分别提取外观与运动特征。
3. **交叉注意力融合**：两类特征经两个交叉注意力模块进行深度融合，建立像素级语义对应。
4. **ControlNet 注入**：融合结果作为 ControlNet 的输入，提取多尺度特征 $f_c$，经零卷积处理后与原始扩散特征相加，得到更新后的扩散特征：
   $$\mathbf{y}_c = \mathcal{F}(\mathbf{z}_t, t, \mathbf{c}_{ref}; \boldsymbol{\Theta}) + \mathcal{Z}(\mathcal{F}(\mathbf{z}_t + \mathcal{Z}(\mathbf{f}_c), t, \mathbf{c}_{ref}; \boldsymbol{\Theta}_c))$$
   这一设计使外观细节与运动轨迹在扩散去噪过程中被联合优化，而非解耦处理。

### 训练策略与损失加权

针对高质量视频物体插入数据稀缺的问题，VideoAnydoor 采用**图像-视频混合训练**：通过人工相机操作（平移、裁剪）将静态图像扩充为伪视频，并使用自适应时间步采样区分真实视频与模拟视频的贡献。损失函数在标准 MSE 基础上引入**轨迹加权机制**，对覆盖较大运动幅度的轨迹区域赋予更大权重：
$$\mathcal{L} = \sum_{i=1}^{N} ((\lambda R_i \mathbf{A}_{trj}^i + (1 - \mathbf{A}_{trj}^i) / N) \cdot \|\delta - \delta^*\|_2^2)$$
其中 $R_i$ 为轨迹覆盖面积比率，$\mathbf{A}_{trj}^i$ 为轨迹区域掩码，$\lambda$ 为平衡因子。该设计使模型在训练中更关注运动显著区域的对齐精度。

### 模块关系总结

三个层次形成递进式控制链路：DINOv2 身份令牌提供全局“这是哪个物体”的约束，边界框序列提供“物体大致在哪儿”的粗粒度引导，像素变形器则通过轨迹图与参考图像的像素级对应，实现“物体细节如何随运动变化”的精细建模。消融实验表明，移除像素变形器后，ID 保留指标（PSNR 59.1→33.8, CLIP-Score 81.4→72.4）和运动一致性指标（AJ 88.3→78.5）均大幅下降，验证了该模块在联合建模外观与运动中的关键作用。

## 核心模块与公式推导

### 整体框架

VideoAnydoor 的推理管线（Figure 2）由三条并行分支构成：

1. **主视频生成分支**：将原始视频 $V \in \mathbb{R}^{N \times 3 \times H \times W}$、物体掩码序列和掩码视频在潜在空间拼接为 9 通道输入，送入集成运动层的 3D U-Net 进行扩散去噪，同时注入 ID 令牌和边界框序列以控制粗粒度运动与背景修复。
2. **全局身份注入分支**：参考图像经背景移除与物体对齐后，由可训练的 DINOv2 作为 ID 提取器生成紧凑的身份令牌，注入 3D U-Net 以维持跨帧外观一致性。
3. **像素变形器分支**：接收标注关键点的参考图像与对应轨迹图，经内容/运动编码和交叉注意力融合后，通过 ControlNet 将像素级细节按轨迹变形并注入多尺度特征。

### 像素变形器

像素变形器是 VideoAnydoor 实现细粒度外观-运动联合建模的核心组件，由轨迹采样与运动注入两个阶段构成。

**轨迹采样**（Figure 3）：对于训练视频的首帧，使用 X-Pose 初始化关键点，随后执行非极大值抑制过滤密集分布点，最终保留运动幅度最大的 $N$ 个点作为轨迹控制点。该策略确保关键点稀疏分布于物体各部位且携带丰富运动信息，从而诱导更精确的控制。

**运动注入**：将轨迹图 $\dot{c}_{mot} \in \mathbb{R}^{N \times 3 \times H \times W}$ 与对应参考图像 $c_{ref-key} \in \mathbb{R}^{3 \times H \times W}$ 配对输入。内容编码器 $E_c$ 和运动编码器 $E_m$ 分别提取嵌入，经两个交叉注意力模块进行特征融合。融合结果作为 ControlNet 的输入，提取多尺度特征 $\mathbf{f}_c$，随后通过零卷积 $\mathcal{Z}$ 与原始扩散特征相加，得到更新后的扩散特征：

$$\mathbf{y}_c = \mathcal{F}(\mathbf{z}_t, t, \mathbf{c}_{ref}; \boldsymbol{\Theta}) + \mathcal{Z}(\mathcal{F}(\mathbf{z}_t + \mathcal{Z}(\mathbf{f}_c), t, \mathbf{c}_{ref}; \boldsymbol{\Theta}_c))$$

其中 $\mathcal{F}$ 表示原始扩散 U-Net，$\boldsymbol{\Theta}$ 和 $\boldsymbol{\Theta}_c$ 分别为冻结的扩散参数和可训练的 ControlNet 副本参数。该公式实现了 ControlNet 多尺度外观-运动特征与扩散主干的无缝融合。

### 轨迹加权损失

为增强关键点处的运动控制精度，VideoAnydoor 对标准均方误差损失进行区域重加权。损失函数定义为：

$$\mathcal{L} = \sum_{i=1}^{N} \left( \left( \lambda R_i \mathbf{A}_{trj}^i + \frac{1 - \mathbf{A}_{trj}^i}{N} \right) \cdot \|\delta - \delta^*\|_2^2 \right)$$

其中 $\delta$ 和 $\delta^*$ 分别为预测噪声与真实噪声，$\mathbf{A}_{trj}^i$ 为第 $i$ 帧的轨迹覆盖区域掩码，$R_i$ 为该区域的面积比率，$\lambda$ 为平衡因子。该设计使运动幅度较大的轨迹区域获得更大的损失权重，迫使模型聚焦于前景物体的精确运动对齐。

### 训练策略

为缓解高质量视频物体插入数据的稀缺问题，VideoAnydoor 采用图像-视频混合训练策略。具体而言，从同一视频中选取空间距离最大的帧作为参考图像，提取其前景物体并去背景；同时通过人工相机操作（等间隔平移或逐步裁剪）将高质量静态图像扩充为伪视频。训练时引入自适应时间步采样，区分真实视频与图像模拟视频的贡献。

## 实验与分析

### 主结果：定量对比

在包含200个Pexel视频的自定义基准上，VideoAnydoor在所有六项自动指标上均显著超越现有方法（Table 2）。具体而言，其CLIP-Score达到38.0，DINO-Score为81.4，PSNR为59.1，运动一致性指标AJ为88.3，平均轨迹偏差δavg为91.5，综合对齐度OA为92.5。相比之下，两阶段方案的代表**ReVideo**（Mou et al., arXiv 2024）OA仅为83.2，差距达9.3个百分点；**AnyV2V**（Ku et al., arXiv 2024）则在内容保真度和运动一致性上均出现明显退化。这一结果验证了端到端框架在同时保持外观身份与运动精度方面的根本优势。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison between our VideoAnydoor and other related work. Six automatic metrics are employed for the performance evaluation of both content and motion. VideoAnydoor outperforms these methods across all the metrics*

用户研究（Table 3）进一步巩固了上述结论：VideoAnydoor在合成质量（3.75/4）、身份保真度（3.80/4）、运动流畅度（3.65/4）和物体局部多样性（3.70/4）四个维度上均获最优评分，表明其生成结果在人类感知层面同样具有压倒性优势。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/011_Table_3.jpg]]
*Table 3: User study on the comparison between our VideoAnydoor and existing alternatives. “Quality”, “Fidelity”, “Smooth”, and “Diversity” measure synthesis quality, object identity preservation, motion consistency, and object local variation, respectively. Each metric is rated from 1 (worst) to 4 (best)*

定性对比（Figure 4）揭示了对比方法的典型失败模式：AnyV2V出现严重的内容扭曲和运动不一致，ReVideo则存在编辑内容丢失和姿态控制不佳的问题。VideoAnydoor在保持细粒度外观细节（如车标、猫尾纹理）的同时实现了平滑且精确的运动跟随（Figure 5, Figure 6）。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/005_Figure_4.jpg]]
*Figure 4: Comparison results between VideoAnydoor and existing state-of-the-art video editing works. Our VideoAnydoor can achieve superior performance on precise control of both motion and content*

### 消融实验：核心组件的因果贡献

消融实验严格保持单一变量，从身份保留（Table 4）和运动一致性（Table 5）两个维度量化各组件的贡献。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/010_Table_5.jpg]]
*Table 5: Quantitative evaluation of core components in VideoAnydoor on motion consistency. † denotes removing the semantic points in the key-point image*

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/012_Table_4.jpg]]
*Table 4: Quantitative evaluation of core components in VideoAnydoor on ID preservation. † denotes removing the semantic points in the key-point image*

**像素变形器（Pixel Warper）是最关键的组件。**移除该模块后，身份保留指标全面崩溃：PSNR从59.1骤降至33.8，CLIP-Score从81.4跌至72.4，DINO-Score从81.4降至48.5；运动一致性同样大幅退化，AJ从88.3降至78.5，δavg从91.5降至81.7，OA从92.5降至83.7。定性结果（Figure 7）显示，缺少像素变形器时视频出现运动不一致和错误的物体姿态，直接印证了该模块在像素级细节变形与运动联合建模中的不可替代性。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative ablation studies on the core components of VideoAnydoor. When removing the pixel warper, it suffers from poor motion consistency due to the undesired posture. And it can be observed that all the components contribute to the best performance*

**图像-视频混合训练策略**对运动一致性贡献显著。仅使用真实视频训练（无静态图像增强）时，AJ从88.3暴跌至71.4，表明通过人工相机操作（平移、裁剪）将高质量静态图像扩充为伪视频，有效弥补了真实视频中外观-运动对齐数据的稀缺性。

**可训练的DINOv2 ID提取器**远优于固定版本。保持DINOv2权重冻结会导致性能大幅下降（Section 4.4），说明适应性微调对提取具有区分性的身份令牌至关重要。

**轨迹加权损失**优于简单的边界框损失。该设计通过对覆盖较大运动幅度的轨迹区域赋予更大权重，使模型聚焦于前景关键区域，从而提升运动控制精度（Section 4.4）。

**关键点选择策略**的消融（Table 6）表明，筛选运动幅度更大的稀疏关键点进行轨迹控制，相比均匀采样或紧密分布点带来显著的性能增益。这验证了轨迹采样器（X-Pose + NMS + motion filter）设计的有效性：稀疏且高运动信息量的关键点能诱导更精确的控制信号。

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/014_Table_6.jpg]]
*Table 6: Detailed quantitative evaluation of the pixel warper in VideoAnydoor on motion consistency. “Tight box” denotes training with tightly-surrounded boxes*

### 失败模式与局限性

尽管VideoAnydoor在整体性能上表现出色，论文明确指出其在处理复杂标志（如文字、商标）时仍存在困难。这可能源于训练数据中缺乏足够的复杂纹理样本，或当前主干网络对高频细节的建模能力不足。作者建议通过收集相关领域数据或采用更强的主干网络来解决该问题。

### 关键图表结论汇总

- **Table 2**：VideoAnydoor在六项自动指标上全面超越ReVideo、AnyV2V、ConsistI2V等对比方法，OA领先9.3个百分点。
- **Table 3**：用户研究四项评分均最优，身份保真度达3.80/4。
- **Table 4 & Table 5**：移除像素变形器导致身份保留PSNR下降25.3点、运动一致性AJ下降9.8点；纯视频训练使AJ下降16.9点。
- **Figure 7**：定性消融直观展示缺少像素变形器时的运动不一致和姿态错误。
- **Table 6**：大运动关键点选择策略带来显著性能增益。

### 补充图表

![[assets/figures/papers/paper_list_l24_VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Co/figures/004_Table_1.jpg]]
*Table 1: Statistics of datasets used for training our VideoAnydoor. “quality” particularly refers to the image resolution*

## 方法谱系与知识库定位

### 问题定位与现有方案瓶颈

视频物体插入（Video Object Insertion）要求在保持物体外观身份一致性的同时，精确跟随用户指定的运动轨迹。该任务的核心瓶颈在于**外观身份保持**与**运动控制精度**的联合建模。现有方案多采用两阶段范式，代表性工作包括：

- **AnyV2V** (Ku et al., arXiv 2024)：首先利用图像编辑模型修改首帧，再通过视频扩散模型将首帧编辑结果传播至后续帧。该方法在首帧插入时缺乏全局身份信息的显式注入，且后续帧传播过程中不包含参考物体的身份约束，导致物体外观在时序上逐渐退化，运动一致性差。
- **ReVideo** (Mou et al., arXiv 2024)：将内容编辑与运动控制解耦为两个阶段，首帧插入依赖外部图像编辑模型，运动控制模块缺乏语义感知的特征注入机制。这种解耦设计使得外观细节与运动轨迹之间缺少像素级的对应关系，难以实现高保真细节的精确运动对齐。
- **ConsistI2V** (Ren et al., TMLR 2024)：作为基于图像到视频（I2V）的编辑方法，在定量对比中参与评估，但其设计目标并非专门的物体插入任务，在身份保持和运动控制上均存在明显不足。

这些方法的共同缺陷可归纳为：**缺少从参考物体到目标视频帧的显式身份信息注入通路**，以及**运动控制信号与像素级外观细节之间缺乏语义对应**。

### VideoAnydoor 的核心改进槽位

VideoAnydoor 在以下四个关键槽位上对现有方案进行了系统性改进：

**槽位一：外观身份注入机制。** 基线方法或完全缺乏身份注入，或仅使用 CLIP 等全局嵌入提供粗粒度语义。VideoAnydoor 采用 DINOv2 作为 ID 提取器，从去背景且居中对齐的参考图像中提取紧凑的身份令牌，并注入扩散 U-Net 的交叉注意力层。这种可训练的 ID 提取器相比固定 DINOv2 能显著提升身份保持能力（消融实验中固定版本性能远差于可训练版本，详见 Section 4.4）。

**槽位二：运动控制与细节对齐。** 基线方法仅通过 ControlNet 直接注入轨迹条件，无显式的语义对应关系。VideoAnydoor 设计了像素变形器（Pixel Warper），其核心机制是：以标注任意关键点的参考图像和对应的轨迹图作为输入对，通过内容编码器 $E_c$ 和运动编码器 $E_m$ 分别提取外观和运动特征，经两个交叉注意力模块融合后送入 ControlNet，实现像素级细节按轨迹变形的联合建模。这一设计使外观细节与运动控制从解耦的两阶段关系转变为端到端的联合优化关系。

**槽位三：训练数据与策略。** 基线方法仅使用真实视频训练，缺乏高质量的外观细节对齐样本。VideoAnydoor 采用图像-视频混合训练策略，通过人工相机操作（等间隔平移、渐进式裁剪）将高质量静态图像扩充为伪视频，并使用自适应时间步采样区分不同模态数据的贡献。消融实验表明，仅使用视频训练（无图像混合）会导致运动一致性指标 AJ 从 88.3 骤降至 71.4（Table 5），验证了图像混合训练对保持外观细节的关键作用。

**槽位四：损失函数设计。** 基线方法使用标准均方误差损失，对所有区域等权处理。VideoAnydoor 设计了轨迹加权损失：

$$\mathcal{L} = \sum_{i=1}^{N} ((\lambda R_i \mathbf{A}_{trj}^i + (1 - \mathbf{A}_{trj}^i) / N) \cdot \|\delta - \delta^*\|_2^2)$$

该损失根据轨迹覆盖面积比率 $R_i$ 和轨迹掩码 $\mathbf{A}_{trj}^i$ 对预测误差进行重新加权，使覆盖较大运动幅度的轨迹区域获得更大的损失权重，从而增强关键点处的运动控制精度。消融实验证实加权损失优于简单的边界框损失。

### 知识库定位与适用边界

**方法谱系位置：** VideoAnydoor 属于**零样本视频物体插入**方法，位于视频编辑（Video Editing）与身份保持生成（Identity-Preserving Generation）的交叉领域。其技术路线融合了扩散模型修复（Inpainting）、身份注入（ID Injection）、以及基于关键点的运动控制（Keypoint-based Motion Control）三条技术线。

**适用边界：**

- **强项场景：** 零样本条件下对任意物体的高保真插入，支持边界框序列的粗粒度运动控制和关键点轨迹的细粒度运动控制。可扩展至视频虚拟试穿、说话头生成、多区域编辑等应用（Figure 8）。
- **已知局限：** 方法在处理复杂标志（如文字、商标）时仍有困难。论文明确指出这可能需要收集相关数据或采用更强的主干网络来解决（Section 5）。
- **待验证边界：** 论文未提供在极端运动幅度、严重遮挡、或大幅光照变化条件下的系统性评估，这些场景下的鲁棒性需进一步验证。此外，方法的零样本泛化能力仅在 Pexel 视频基准上进行了评估，在更广泛的域外分布（如低分辨率视频、艺术风格视频）上的表现尚不明确。

### 证据强度评估

VideoAnydoor 的核心主张获得了多层证据支持：

- **强证据：** 定量对比（Table 2）显示 VideoAnydoor 在所有六项自动指标（CLIP-Score、DINO-Score、PSNR、AJ、$\delta_{avg}$、OA）上均显著超越对比方法；用户研究（Table 3）在质量、保真度、运动流畅度、多样性四个维度上均获得最优评分。
- **因果证据：** 消融实验（Table 4, Table 5）证实移除像素变形器后，身份保持和运动一致性指标大幅下降（PSNR 59.1→33.8，CLIP-Score 81.4→72.4，AJ 88.3→78.5），定性结果（Figure 7）显示缺少像素变形器时视频出现运动不一致和不正确的物体姿态。
- **需注意：** 论文未报告对比方法的训练数据规模和计算资源是否与 VideoAnydoor 对等，公平性比较的严格程度需要读者自行判断。此外，自定义基准（200 个 Pexel 视频）的代表性和多样性未经过标准化验证。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/VideoAnydoor_High_fidelity_Video_Object_Insertion_with_Precise_Motion_Control.pdf]]
