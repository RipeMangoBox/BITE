---
title: "VideoComposer: Compositional Video Synthesis with Motion Controllability"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/VideoComposer_Compositional_Video_Synthesis_with_Motion_Controllability.pdf
aliases:
- VideoComposer
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入压缩视频中的运动矢量作为显式时间条件，并设计时空条件编码器（STC-encoder）统一聚合多模态条件的时空关系。
primary_logic: 将视频分解为文本、空间和时间条件，通过组合式生成框架实现灵活可控的视频合成，其中运动矢量直接引导像素级运动，STC-encoder增强序列条件的时间连贯性。
claims:
- 使用运动矢量可将运动控制误差（EPE）从仅文本条件的4.03降至2.67，结合STC-encoder进一步降至2.18。
- "STC-encoder在不同时间条件（sketch/depth/motion vectors）下平均提升帧一致性约0.012（例如sketch: 0.923 vs 0.910）。"
- 组合式训练未牺牲文本到视频生成能力，VideoComposer在MSR-VTT上FVD 580优于第一阶段预训练（FVD 803），且CLIPSIM竞争力强（0.2932 vs 0.2876）。
- Custom set (1000 caption-video pairs from WebVid10M) 上 Motion control (EPE) ↓ = 2.18 (VideoComposer with STC-encoder & MV)
---

# VideoComposer: Compositional Video Synthesis with Motion Controllability

> [!tip] 核心洞察
> 将视频分解为文本、空间和时间条件，通过组合式生成框架实现灵活可控的视频合成，其中运动矢量直接引导像素级运动，STC-encoder增强序列条件的时间连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoComposer: 具有运动可控性的组合式视频合成 |
| 英文题名 | VideoComposer: Compositional Video Synthesis with Motion Controllability |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2306.02018) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VideoComposer |
| Dataset | Custom set, MSR-VTT |

> [!tip] 效果简介
> - Custom set (1000 caption-video pairs from WebVid10M) 上，Motion control (EPE) ↓ 2.18 (VideoComposer with STC-encoder & MV) vs 2.67 (w/o STC-encoder, with MV) / 4.03 (w/o STC-encoder, text only) (-0.49 / -1.85)。
> - Custom set (1000 caption-video pairs) 上，Frame consistency (CLIP cosine similarity) ↑ 0.923 (sketch) / 0.928 (depth) / 0.927 (motion vectors) with STC-encoder vs 0.910 / 0.922 / 0.915 without STC-encoder (+0.013 / +0.006 / +0.012)。
> - MSR-VTT 上，FVD ↓ / CLIPSIM ↑ FVD 580 / CLIPSIM 0.2932 vs First-stage pre-training (FVD 803, CLIPSIM 0.2876) (FVD -223 / CLIPSIM +0.0056)。

## 概述

视频生成领域长期面临一个瓶颈：现有方法难以同时精确控制生成视频的**空间布局**与**时间动态**。文本到视频模型（如 **GODIVA**、**CogVideo**、**Make-A-Video** 等）虽然能生成语义相关的视频内容，但缺乏对运动模式的显式建模，导致跨帧一致性和运动可控性不足。VideoComposer 的核心洞察在于，将视频显式分解为**文本条件**、**空间条件**（单帧图像、草图、风格）和**时间条件**（运动矢量、深度序列、掩码序列、草图序列），通过组合式生成框架实现灵活可控的视频合成。

该方法的关键因果调节器有二：其一，引入压缩视频中的**运动矢量**作为显式时间条件，直接引导像素级运动模式；其二，设计统一的**时空条件编码器（STC-encoder）**，通过 2D 卷积与时间 Transformer 聚合多模态条件的时空关系，增强序列条件的时间连贯性。实验证据表明，仅引入运动矢量即可将运动控制误差（EPE）从纯文本条件的 4.03 降至 2.67，叠加 STC-encoder 后进一步降至 2.18；STC-encoder 在不同时间条件设置下平均提升帧一致性约 0.012。在 MSR-VTT 文本到视频基准上，VideoComposer 取得 FVD 580 和 CLIPSIM 0.2932，优于第一阶段预训练（FVD 803），证明组合式训练未牺牲基础文本到视频生成能力。

该方法在方法谱系中定位为**基于潜在扩散模型的组合式视频生成框架**，通过条件分解与统一时空编码，将空间控制与时间控制解耦后再融合，实现了从图像到视频生成、视频修复、草图/深度序列到视频、视频到视频转换及运动迁移等多种下游任务的统一支持。

## 背景与动机

视频生成领域近年来取得了显著进展，文本到视频（T2V）模型如 **GODIVA**（Wu et al., arXiv 2021）、**Nuwa**（Wu et al., ECCV 2022）、**CogVideo**（Hong et al., arXiv 2022）、**MagicVideo**（Zhou et al., arXiv 2022）、**Make-A-Video**（Singer et al., arXiv 2022）和 **Video LDM**（Blattmann et al., CVPR 2023）等，已经能够根据文本描述生成具有一定视觉质量的视频。然而，这些方法面临一个核心瓶颈：**难以同时控制视频的空间布局和时间动态**。

具体而言，现有方法存在两个关键缺口：

1. **缺乏对运动模式的显式建模**。大多数方法仅依赖文本条件来隐式地引导视频中的运动，这使得生成视频的运动可控性不足——模型无法精确地按照用户指定的运动轨迹或动态模式来生成内容。跨帧的时间一致性也因此难以保证。

2. **条件编码方式碎片化**。即使部分工作尝试引入额外的空间或时间条件，各条件通常被独立编码后简单级联或加和，缺乏一个统一的机制来聚合序列条件中的时空关系，导致时间连贯性较弱。

针对上述问题，VideoComposer 的动机在于：**将视频分解为文本、空间和时间三类条件，通过组合式生成框架实现灵活可控的视频合成**。其核心思路是引入压缩视频中的运动矢量（motion vectors）作为显式的时间条件，直接引导像素级运动；同时设计一个统一的时空条件编码器（STC-encoder）来聚合多模态条件的时空关系，从而在保持文本到视频生成能力的前提下，显著提升运动可控性和跨帧一致性。

## 核心创新

VideoComposer 的核心创新在于将视频生成问题重新定义为**组合式条件合成**，并围绕“运动可控性”这一瓶颈进行了两项关键设计：**引入运动矢量作为显式时间条件**，以及**设计时空条件编码器（STC-encoder）统一聚合多模态条件的时空关系**。

### 1. 引入运动矢量作为显式时间条件

现有文本到视频生成方法（如 **CogVideo** (Hong et al., arXiv 2022)、**Make-A-Video** (Singer et al., arXiv 2022)）主要依赖文本描述来间接控制视频中的运动，缺乏对像素级运动模式的显式建模，导致生成视频的运动可控性和跨帧一致性不足。VideoComposer 首次将压缩视频中的**运动矢量（motion vectors）** 作为一种独立的时间条件引入扩散生成框架（Section 3.2）。运动矢量直接编码了相邻帧之间的像素位移信息，为模型提供了精确的运动引导信号。

消融实验（Table 1）验证了这一设计的决定性作用：在仅使用文本条件时，运动控制误差（EPE）高达 4.03；引入运动矢量后，误差降至 2.67；进一步结合 STC-encoder，误差降至 2.18。这表明运动矢量是提升运动可控性的核心“因果旋钮”。

### 2. STC-encoder：统一的时空条件聚合接口

在条件编码方式上，VideoComposer 改变了基线方法中各条件独立编码并简单级联/加和的做法（changed slot）。其设计的 **STC-encoder** 是一个统一接口，用于处理各类序列化的时间条件（运动矢量、深度序列、草图序列、掩码序列）。该编码器通过 2D 卷积提取空间特征，再经由时间 Transformer 建模序列帧间的时序依赖关系，从而显式聚合时空信息（Section 3.2, Figure 2）。

STC-encoder 的效果在 Table 2 中得到了系统验证：在三种时间条件设置下（sketch / depth / motion vectors），加入 STC-encoder 后帧一致性（CLIP cosine similarity）分别从 0.910 / 0.922 / 0.915 提升至 0.923 / 0.928 / 0.927，平均提升约 0.012。定性消融（Figure 9）进一步显示，去除 STC-encoder 会导致生成视频中出现明显的时序不一致伪影。

### 3. 两阶段组合式训练策略

VideoComposer 改变了单阶段端到端训练的方式（changed slot），采用两阶段训练策略（Section 3.3）：第一阶段进行纯文本到视频的预训练，使模型掌握基本的视频生成能力；第二阶段引入多种空间和时间条件进行组合训练。这一设计确保了组合式训练不会牺牲文本到视频的生成质量——在 MSR-VTT 基准上，完整 VideoComposer 的 FVD 为 580，显著优于仅使用第一阶段预训练的 803，同时 CLIPSIM 保持竞争力（0.2932 vs 0.2876）（Table A3）。

### 创新总结

VideoComposer 的创新链条清晰且因果可追溯：**运动矢量**提供了像素级运动引导，解决了“运动不可控”的瓶颈；**STC-encoder** 统一了多模态时空条件的融合方式，解决了“跨帧不一致”的瓶颈；**两阶段训练**则保证了组合式生成能力不损害基础文本到视频质量。三者共同构成了一个灵活的视频合成组合系统，支持文本、空间、时间条件的任意子集组合。

## 整体框架

VideoComposer 提出了一种**组合式视频生成框架**，其核心思想是将视频分解为三类独立条件——文本条件、空间条件和时间条件——然后通过统一的编码与注入机制，在视频潜在扩散模型（VLDMs）的去噪过程中协同引导生成。这一设计使得用户能够灵活地组合或替换条件子集，实现对空间布局、时间动态和语义内容的解耦控制。

### 条件分解与输入流

框架的输入端将目标视频（或生成任务）拆解为三个正交的条件通道：

- **文本条件**：描述视频语义内容的自然语言，由 **OpenCLIP ViT-H/14 文本编码器** 提取为语义嵌入序列。
- **空间条件**：控制单帧空间结构的信号，包括**单帧图像**（用于图像到视频生成）、**单帧草图**（用于草图到视频生成）以及**风格参考图像**（通过 OpenCLIP ViT-H/14 图像编码器提取风格嵌入）。
- **时间条件**：控制跨帧时序动态的信号，包括**运动矢量**（从压缩视频中提取的像素级运动场）、**深度序列**、**掩码序列**和**草图序列**。其中运动矢量是本文引入的关键显式控制信号，直接编码了相邻帧间的像素位移信息。

### 条件编码与融合：STC-encoder

多模态条件在进入去噪网络之前，需要被统一编码为与潜变量兼容的表示。VideoComposer 设计了**时空条件编码器（STC-encoder）** 作为统一接口：

- 对于空间条件（单帧）和时间条件（序列），STC-encoder 首先使用 2D 卷积提取逐帧空间特征，再通过时间 Transformer 聚合序列帧间的时空依赖关系，最终输出与去噪潜变量 $z_t$ 空间形状一致的条件特征序列。
- 所有经 STC-encoder 处理后的条件特征通过**逐元素加法**融合为一个统一的条件张量，然后沿通道维度与 $z_t$ 拼接，送入 3D UNet 进行去噪。
- 文本条件和风格条件（均为嵌入序列形式）则通过**交叉注意力机制**注入到 3D UNet 的各层中，提供语义和风格引导。

### 去噪骨干：3D UNet 与 VLDMs

生成过程基于视频潜在扩散模型（VLDMs），其训练目标为最小化预测噪声与真实噪声的 L2 距离：

$$\mathcal{L}_{VLDM} = \mathbb{E}_{\mathcal{E}(x), \epsilon \in \mathcal{N}(0,1), c, t} \left[ \| \epsilon - \epsilon_{\theta}(z_t, c, t) \|_2^2 \right]$$

其中 $\mathcal{E}(x)$ 将视频编码到潜空间，$z_t$ 为时间步 $t$ 的噪声潜变量，$c$ 为组合条件。去噪网络 $\epsilon_{\theta}$ 采用**3D UNet** 架构——在 2D UNet 基础上引入时间卷积和时间 Transformer 层，以同时建模空间和时间维度上的依赖关系。

### 训练策略与推理引导

训练采用**两阶段策略**以保证组合式训练的稳定性：

1. **第一阶段**：仅使用文本条件进行文本到视频预训练，使模型获得基本的视频生成能力。
2. **第二阶段**：引入空间和时间条件进行组合训练，使模型学会响应多模态条件的联合引导。

推理时，VideoComposer 使用 **classifier-free guidance** 机制来调节生成结果对特定条件的遵循程度：

$$\hat{\epsilon}_{\theta}(z_t, c, t) = \epsilon_{\theta}(z_t, c_1, t) + \omega (\epsilon_{\theta}(z_t, c_2, t) - \epsilon_{\theta}(z_t, c_1, t))$$

其中 $c_1$ 和 $c_2$ 为两组不同的条件组合（例如 $c_1$ 仅含文本，$c_2$ 含文本和运动矢量），$\omega$ 为引导尺度。通过外推两组条件的预测噪声，用户可以在文本语义遵循度和时间条件控制精度之间进行权衡。

### 整体数据流

综合来看，VideoComposer 的 pipeline 遵循以下流程：

1. **条件提取**：从输入视频或用户指定中提取文本、空间和时间条件。
2. **条件编码**：STC-encoder 统一编码空间和时间条件，CLIP 编码器提取文本和风格嵌入。
3. **潜变量初始化**：随机噪声 $z_T$ 作为生成起点。
4. **迭代去噪**：在每个去噪步，将融合后的条件与 $z_t$ 拼接，文本/风格嵌入通过交叉注意力注入 3D UNet，预测噪声并更新 $z_{t-1}$。
5. **解码输出**：最终去噪后的潜变量通过 VAE 解码器恢复为视频帧序列。

该框架的模块化设计使得 VideoComposer 能够支持多种下游任务——包括组合式图像到视频生成、视频修复、草图/深度序列到视频生成、视频到视频转换以及运动迁移——而无需针对每个任务重新训练。

### 补充图表

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/002_Figure_2.jpg]]
*Figure 2: Overall architecture of VideoComposer. First, a video is decomposed into three types of conditions, including textual condition, spatial conditions and temporal conditions. Then, we feed these conditions into the unified STC-encoder or the CLIP model to embed control signals. Finally, the resulting conditions are leveraged to jointly guide VLDMs for denoising*

## 核心模块与公式推导

### 3.1 视频潜在扩散模型基础

VideoComposer 的生成主干基于视频潜在扩散模型（Video Latent Diffusion Models, VLDMs）。其核心训练目标为最小化预测噪声与真实噪声之间的 L2 距离：

$$
\mathcal { L } _ { V L D M } = \mathbb { E } _ { \mathcal { E } ( x ) , \epsilon \in \mathcal { N } ( 0 , 1 ) , c , t } \left[ \| \epsilon - \epsilon _ { \theta } ( z _ { t } , c , t ) \| _ { 2 } ^ { 2 } \right]
$$

其中，$x$ 为输入视频，$\mathcal{E}$ 为编码器将视频压缩至潜空间得到 $z_0$，$z_t$ 为加噪后的潜变量，$\epsilon$ 为真实噪声，$\epsilon_\theta$ 为去噪网络预测的噪声，$c$ 为条件信号，$t$ 为时间步。该公式继承自潜在扩散模型框架，但扩展到视频潜空间，为后续多条件注入提供统一的去噪基础。

### 3.2 条件分解与编码模块

VideoComposer 将视频显式分解为三类条件：

- **文本条件**：通过 OpenCLIP ViT-H/14 提取语义嵌入，作为全局语义引导。
- **空间条件**：包括单帧图像、单张草图、风格图像，提供内容或风格约束。
- **时间条件**：包括运动矢量序列、深度图序列、掩码序列、草图序列，提供帧间动态变化的显式控制信号。

其中，**运动矢量**是从压缩视频中提取的像素级运动信息，直接编码相邻帧之间的位移场，作为时间动态的核心控制信号。这是 VideoComposer 区别于仅依赖文本或单帧条件的方法的关键设计。

### 3.3 时空条件编码器

STC-encoder 是统一处理序列化时空条件的核心模块。其设计目标是将不同模态的时间条件（运动矢量、深度序列等）聚合为与潜变量 $z_t$ 空间形状一致的统一表示，以增强跨帧的时间连贯性。

STC-encoder 的内部结构采用 **2D 卷积** 提取单帧空间特征，再通过 **时间 Transformer** 建模帧间时序依赖关系。处理后的条件序列通过逐元素相加融合，随后沿通道维度与 $z_t$ 拼接，送入 3D UNet 进行去噪。

对于文本和风格条件，VideoComposer 采用**交叉注意力机制**注入引导信号，而非直接拼接，以保持语义信息与时空条件的解耦。

### 3.4 无分类器引导

在推理阶段，VideoComposer 使用无分类器引导来控制生成结果对特定条件的遵循程度：

$$
\hat { \epsilon } _ { \theta } ( z _ { t } , c , t ) = \epsilon _ { \theta } ( z _ { t } , c _ { 1 } , t ) + \omega ( \epsilon _ { \theta } ( z _ { t } , c _ { 2 } , t ) - \epsilon _ { \theta } ( z _ { t } , c _ { 1 } , t ) )
$$

其中 $c_1$ 和 $c_2$ 为两组条件（例如 $c_1$ 仅包含文本，$c_2$ 包含文本与时间条件），$\omega$ 为引导尺度。该公式通过在两组条件的预测噪声之间进行外推，实现对生成视频在语义遵循与运动可控性之间的灵活权衡。

### 补充图表

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/003_Figure_3.jpg]]
*Figure 3: Examples of motion vectors*

## 实验与分析

VideoComposer 的核心实验围绕三个轴展开：运动可控性的定量验证、时空条件编码器（STC-encoder）对帧一致性的消融分析，以及组合式训练对文本到视频生成能力的保持性检验。所有实验均基于 WebVid10M 数据集的自定义测试集（1000 条视频-文本对）和 MSR-VTT 基准。

### 运动可控性：运动矢量的决定性作用

Table 1 报告了运动控制误差（Motion Control Error，以 EPE 衡量）的对比结果。仅使用文本条件（Text-only）时，模型缺乏显式的运动引导，EPE 高达 4.03。引入运动矢量（MV）作为时间条件后，即使不配备 STC-encoder，EPE 也大幅降至 2.67。当同时启用 STC-encoder 和运动矢量时，VideoComposer 将 EPE 进一步压缩至 2.18，相比纯文本条件降低了 1.85 的绝对误差。这一阶梯式改善揭示了两个关键机制：运动矢量提供了像素级的运动先验，而 STC-encoder 通过聚合序列条件的时空依赖关系，增强了该先验在去噪过程中的时间连贯性。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/006_Table_1.jpg]]
*Table 1: Evaluating the motion controllability. “Text" and “MV" represent the utilization of text and motion vectors as conditions for generation*

### STC-encoder 的消融：帧一致性的系统性提升

Table 2 针对三种时间条件（sketch 序列、depth 序列、motion vectors）分别评估了 STC-encoder 对帧一致性的贡献。指标为相邻帧的 CLIP 余弦相似度。在 sketch 条件下，加入 STC-encoder 使一致性从 0.910 提升至 0.923（+0.013）；depth 条件下从 0.922 升至 0.928（+0.006）；motion vectors 条件下从 0.915 升至 0.927（+0.012）。平均提升约 0.010，表明 STC-encoder 作为一个统一接口，能够有效建模序列输入的空间与时间依赖，而非简单地将各条件独立编码后级联。Figure 9 的定性消融进一步佐证了这一点：去除 STC-encoder 后，生成视频在红框标注区域出现明显的结构抖动和细节丢失，尤其在运动边界处表现更为突出。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/011_Table_2.jpg]]
*Table 2: Quantitative ablation study of STC-encoder. “Conditions" denotes the conditions utilized for generation*

### 组合式训练不损害文本到视频生成质量

一个自然的担忧是：引入多种空间和时间条件进行组合训练，是否会削弱模型的基础文本到视频生成能力？Table A3 在 MSR-VTT 基准上给出了否定答案。VideoComposer 的组合训练阶段（第二阶段）取得了 FVD 580、CLIPSIM 0.2932 的成绩，显著优于仅做文本到视频预训练的第一阶段（FVD 803，CLIPSIM 0.2876）。FVD 降低了 223 点，CLIPSIM 提升了 0.0056，说明组合条件训练不仅没有造成灾难性遗忘，反而通过多任务学习增强了视频生成的语义对齐和时序质量。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/015_Table.jpg]]
*Table A3: Text-to-video generation performance on MSR-VTT. In Fig. A11, we illustrate this capability. Videos generated with VideoComposer faithfully adhere to the given conditions, including text prompts, depth maps, and style*

### 定性结果：组合式生成范式的灵活性

定性示例覆盖了多种组合场景，验证了框架的灵活可控性。Figure 4 展示了组合式图像到视频生成：给定单帧空间条件和文本描述，模型可生成合理视频；进一步加入时间条件（如深度序列）后，能够精细控制视频中物体的时变结构。Figure 5 的组合式视频修复表明，通过手动添加掩码并结合文本指令，VideoComposer 可以修复被遮挡区域，而引入时间条件则可指定修复区域的结构演化。Figure 6 和 Figure 7 分别展示了 sketch-to-video 和 video-to-video translation 的能力，其中运动矢量被用于去除静态背景（Figure 7），手绘运动轨迹则实现了细粒度的运动控制（Figure 8），相比 CogVideo 的有限运动控制展现出显著优势。

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/010_Figure_8.jpg]]
*Figure 8: Versatile motion control using hand-crafted motions. (a) Limited motion control using CogVideo [24]. (b) Fine-grained and flexible motion control, empowered by VideoComposer*

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/004_Figure_4.jpg]]
*Figure 4: Compositional image-to-video generation. We showcase six examples, each displaying two generated videos. The upper video is generated using a given single frame as the spatial condition and a textual condition describing the scene. The lower video is generated by incorporating an additional sequence of temporal conditions to facilitate finer control over the temporally evolving structure*

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/005_Figure_5.jpg]]
*Figure 5: Compositional video inpainting. By manually adding masks to videos, VideoComposer can perform video inpainting, facilitating the restoration of the corrupted parts according to textual instructions. Furthermore, by incorporating temporal conditions specifying the visual structure, VideoComposer can perform customized inpainting that conforms to the prescribed structure*

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/007_Figure_6.jpg]]
*Figure 6: Compositional sketch-to-video generation. In the first example, the upper video is generated using text and a single sketch as the conditions, while the lower is generated by using an additional mask sequence for finer control over the temporal patterns. For the last two examples, the upper video is generated using a single sketch and a textual condition, while the lower is generated with an additional style from a specified image*

### 失败模式与局限性

尽管 VideoComposer 在可控性上取得了突破，但存在三个明确的局限性。第一，训练数据 WebVid10M 含有大量水印，导致生成视频中继承了水印伪影，影响视觉质量。第二，受限于训练成本，当前视频分辨率仅为 256×256，细节清晰度不足。第三，当组合条件的数量增加时，模型如何处理条件间的语义冲突尚未被充分探讨——例如，当文本描述与运动矢量指向不同的运动方向时，模型的行为缺乏系统分析。这些局限性指向了未来的改进方向：使用高质量无标签数据、引入超分辨率级联、以及设计条件冲突的自适应平衡机制。

### 补充图表

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/008_Figure.jpg]]
*Figure A9: (a) Source video (b) Depth-guided generation*

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/012_Figure.jpg]]
*Figure A10: Compositional sketch sequence-to-video generation. We showcase five examples, each displaying a video generated from a sequence of sketches and a textual description. The final example additionally incorporates a style condition*

![[assets/figures/papers/paper_list_l1060_https_arxiv_org_abs_2306_02018/figures/014_Figure.jpg]]
*Figure A12: Motion transfer. We showcase four examples, each displaying a video generated from a single image and motions. In the first three examples, we transfer the motion patterns in a source video to the generated video by extracting and utilizing motion vectors. The final example incorporates hand-crafted motions instead*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

VideoComposer 处于文本到视频生成（Text-to-Video, T2V）向可控视频生成演进的关键节点。其直接对标的基线包括：

- **纯文本驱动方法**：**GODIVA** (Wu et al., arXiv 2021)、**Nuwa** (Wu et al., ECCV 2022)、**CogVideo** (Hong et al., arXiv 2022)、**MagicVideo** (Zhou et al., arXiv 2022)、**Make-A-Video** (Singer et al., arXiv 2022) 及 **Video LDM** (Blattmann et al., CVPR 2023)。这些方法的核心瓶颈在于仅依赖文本条件，无法对生成视频的空间布局和时间动态进行显式控制。VideoComposer 的突破在于将视频显式分解为文本、空间和时间三类条件，使控制信号从单一的语义描述扩展为多模态组合。

- **运动可控性对比**：Figure 8 直接展示了 VideoComposer 与 **CogVideo** 在手绘运动控制上的差异——CogVideo 仅能提供有限的运动引导，而 VideoComposer 实现了细粒度的灵活运动控制。定量上，Table 1 显示仅使用文本条件时运动控制误差（EPE）高达 4.03，而引入运动矢量后降至 2.67，结合 STC-encoder 进一步降至 2.18。

### 2. 核心方法差异

VideoComposer 相对于上述基线的方法论差异体现在三个关键维度：

**条件类型扩展**：基线方法仅依赖文本条件，VideoComposer 引入了多种时间条件（运动矢量、深度序列、掩码序列、草图序列），其中运动矢量直接编码像素级运动信息，这是区别于所有基线方法的独特设计。

**条件编码方式**：基线方法通常对各条件独立编码后简单级联或加和。VideoComposer 设计了统一的时空条件编码器（STC-encoder），通过 2D 卷积捕获空间特征，再经时间 Transformer 聚合序列条件的时空依赖关系。Table 2 的消融实验证实，STC-encoder 在草图（0.923 vs 0.910）、深度（0.928 vs 0.922）和运动矢量（0.927 vs 0.915）三种时间条件下均显著提升了帧一致性。

**训练策略**：基线方法多采用单阶段端到端训练。VideoComposer 采用两阶段训练——先进行文本到视频预训练，再进行组合条件训练。Table A3 表明，仅使用第一阶段预训练时 FVD 为 803，而组合训练后降至 580，同时 CLIPSIM 从 0.2876 提升至 0.2932，证明组合训练未牺牲文本到视频的基础生成能力。

### 3. 适用边界与局限

VideoComposer 的适用边界受以下因素制约：

- **数据质量约束**：训练依赖 WebVid10M 数据集，该数据集包含大量水印，导致生成的视频存在水印伪影，影响视觉质量。这是当前方法在实用化部署中的显著障碍。

- **分辨率限制**：为控制训练成本，当前生成分辨率限制在 256×256，细节清晰度不足。如何高效扩展至 512 以上分辨率同时保持时空一致性，是工程上的重要挑战。

- **条件冲突处理**：当多种组合条件存在语义冲突时（如文本描述与运动矢量指示的方向不一致），模型如何自适应平衡各条件的贡献，论文未进行充分探讨。

- **时长扩展**：当前方法适用于短视频生成，向数分钟级长视频扩展时，运动连续性和内容一致性的维持机制有待研究。

### 4. 开放问题

基于上述局限，VideoComposer 框架的后续演进方向包括：

1. **基础模型升级**：如何利用更大规模的文本到视频预训练模型进一步提升组合式合成的灵活性和质量？
2. **数据质量优化**：如何有效去除 WebVid10M 的水印，或从高质量无标签数据集中学习，以消除生成视频中的水印伪影？
3. **分辨率扩展**：如何通过超分辨率模型高效提升分辨率，同时保持时空一致性？
4. **条件冲突自适应**：当多条件存在语义冲突时，如何设计自适应机制以平衡各条件的贡献权重？
5. **长视频生成**：如何扩展框架以支持更长时长的视频生成，同时维持运动连续性和内容一致性？

## 原文 PDF

![[paperPDFs/arxiv_2023/VideoComposer_Compositional_Video_Synthesis_with_Motion_Controllability.pdf]]
