---
title: Reasoning Diffusion for Unpaired Test Time Out-of-distribution Text-Image to Video Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reasoning_Diffusion_for_Unpaired_Test_Time_Out_of_distribution_Text_Image_to_Video_Generation.pdf
project_link: null
code_link: null
aliases:
- RDUTTODTIVG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 引入多模态大语言模型（VisionNarrator）将非配对图像和文本推理为时序对齐的逐帧叙事，并通过 AlignFormer 的多阶段时序锚点注意力机制将该推理信息转化为帧级潜变量引导，从而驱动生成过程恢复完整场景。
primary_logic: 将高层多模态推理与低层视频去噪生成解耦，利用 MLLM 推断合理的场景演进序列，再通过专用的跨注意力模块将推理信号注入到扩散模型的潜变量空间，使模型即使在条件图像并非首帧时也能生成视觉与语义均连贯的视频。
claims:
- 在模拟非配对输入的 ActivityNet 数据集上，ReasonDiff 在所有自动指标（除 CLIP Score (Image) 外）均取得最优，其中 CLIP Score (Text) 比最强基线 Wan2.1 提升 16.5%。
- 在用户偏好排序上，ReasonDiff 的 User Rank 达到 1.743（越低越好），显著优于 Wan2.1 的 2.692。
- 消融实验表明，移除 AlignFormer 的增强潜变量会导致视频成像质量大幅下降，禁用多帧叙事会使动态程度显著降低。
- ActivityNet (unpaired) 上 CLIP Score (Text) = 0.571
---

# Reasoning Diffusion for Unpaired Test Time Out-of-distribution Text-Image to Video Generation

> [!tip] 核心洞察
> 将高层多模态推理与低层视频去噪生成解耦，利用 MLLM 推断合理的场景演进序列，再通过专用的跨注意力模块将推理信号注入到扩散模型的潜变量空间，使模型即使在条件图像并非首帧时也能生成视觉与语义均连贯的视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向非配对测试时分布外文本-图像到视频生成的推理扩散模型 |
| 英文题名 | Reasoning Diffusion for Unpaired Test Time Out-of-distribution Text-Image to Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Pan_Reasoning_Diffusion_for_Unpaired_Test_Time_Out-of-distribution_Text-Image_to_Video_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | ReasonDiff |
| Dataset | ActivityNet, MSR-VTT |

> [!tip] 效果简介
> - ActivityNet (unpaired) 上，CLIP Score (Text) 0.571 vs Wan2.1: 0.490 (+16.5%)；User Rank (越低越好) 1.743 vs Wan2.1: 2.692 (-0.949)。
> - MSR-VTT (paired) 上，Imaging Quality 0.571 vs N/A (N/A)。

## 概述

文本-图像到视频（TI2V）生成任务通常假设输入条件高度配对：文本描述与图像在语义上一致，且图像恰好对应视频的首帧。然而，在开放域的真实场景中，用户提供的文本与图像往往是非配对（unpaired）的——图像可能来自视频的任意中间帧，文本描述也可能与图像内容存在偏差。这种**条件分布外（OOD）**的输入对现有模型构成了根本性挑战：它们缺乏推理出文本与图像之间内在时序关联的能力，导致生成视频要么语义一致性崩溃，要么过度偏向单一模态。

**ReasonDiff** 针对这一瓶颈提出了一个解耦式推理-生成框架。其核心洞察是：**将高层多模态推理与低层视频去噪生成解耦**——先利用多模态大语言模型（MLLM）推断出合理的场景演进序列，再通过专用的跨注意力机制将推理信号注入扩散模型的潜变量空间，使模型即使在条件图像并非首帧时也能生成视觉与语义均连贯的视频。

具体而言，ReasonDiff 由两个关键组件构成：(1) **MLLM 驱动的多帧推理器**（含 VisionNarrator 与 AlignFormer），负责从非配对输入中推理出时序对齐的逐帧叙事，并将其转化为帧级潜变量引导；(2) **推理引导的生成模型**（基于 Wan2.1 的流匹配框架），在推理增强的潜变量与叙事条件的共同引导下完成去噪生成。

在模拟非配对输入的 ActivityNet 数据集上，ReasonDiff 在所有自动指标上均优于现有最强基线——CLIP Score (Text) 比 **Wan2.1**（Team Wan et al., 2025）提升 **16.5%**，User Rank 从 2.692 降至 **1.743**（越低越好）。消融实验进一步证实：移除 AlignFormer 的增强潜变量会严重损害成像质量，禁用多帧叙事则导致动态程度显著下降，验证了推理模块对生成质量的关键贡献。

## 背景与动机

文本-图像到视频生成任务旨在从多模态条件输入中合成时序连贯的视频，其核心挑战在于如何准确理解并融合文本语义与视觉内容。近年来，基于扩散模型的方法在该领域取得了显著进展，涌现出如 **CogVideoX**（Yang et al., 2024）、**Dynamicrafter**（Xing et al., ECCV 2024）、**LTX-Video**（HaCohen et al., 2025）以及 **Wan2.1**（Team Wan et al., 2025）等一系列代表性工作。

### 现有方法的潜在假设与缺口

现有视频生成模型普遍建立在一个隐含假设之上：输入的文本描述与条件图像是**完全配对且时序对齐**的。具体而言，这些方法通常将条件图像视为视频的首帧，并将文本视为对该视频的全局语义描述，随后通过自注意力机制学习帧间的时间动态。这一范式在标准测试场景下表现良好，却在实际部署中暴露出明显的脆弱性——当用户提供的文本提示与条件图像在时序上并非严格对应时（即非配对输入），模型往往无法推理出两者之间的内在时序关联，导致生成的视频出现**语义不一致**或**过度偏重某一模态**的问题。

图 1 直观地展示了这一困境：给定文本提示“A cat plays in the room”和一幅“破碎花瓶”的条件图像，现有模型要么生成了与图像无关的猫玩耍场景，要么无法将花瓶的破碎状态合理地融入视频叙事中。这种非配对的文本-图像输入构成了典型的**测试时分布外场景**，而现有方法缺乏对此类场景的有效应对机制。

### 核心瓶颈与解决思路

上述困境的根源在于：现有模型缺乏对非配对多模态输入进行**高层语义推理**的能力。它们能够分别编码文本和图像，却无法推断出两者之间的合理时序关系——例如，条件图像中的场景应出现在视频的哪个时间位置，以及如何围绕该锚点构建前后连贯的视觉叙事。

针对这一瓶颈，ReasonDiff 提出了一条解耦式的解决路径：将**高层多模态推理**与**低层视频去噪生成**分离。具体而言，该方法首先利用多模态大语言模型的推理能力，从非配对的文本-图像输入中推断出合理的场景演进序列（包括条件帧的合理位置和逐帧描述），再通过专用的跨注意力模块将这些推理信号注入到扩散模型的潜变量空间，从而驱动生成过程恢复出视觉与语义均连贯的完整视频。这一设计使得模型即使面对条件图像并非首帧的复杂情况，仍能保持生成质量。

## 核心创新

ReasonDiff 的核心创新在于将**高层多模态推理**与**低层视频扩散生成**解耦，专门应对非配对文本-图像输入的 OOD 场景。现有视频生成模型（如 **Wan2.1**、**CogVideoX**、**Dynamicrafter** 等）均假设输入文本与条件图像在时序上完美对齐——图像被视为视频首帧，文本为全局描述。当这一假设被打破时，模型无法推理出图像在视频中的合理时序位置，导致生成结果或偏重文本语义、或偏重视觉条件，丧失整体的语义与视觉连贯性。

ReasonDiff 通过两个关键模块实现了对上述瓶颈的系统性突破：

### 1. 从“直接条件注入”到“多模态推理叙事”

传统方案直接将条件图像特征注入扩散模型，或将其编码为初始噪声，依赖模型自身的自注意力机制来隐式学习时序动态。ReasonDiff 则引入 **VisionNarrator** 模块，利用冻结的多模态大语言模型（MLLM）对非配对输入进行显式推理。VisionNarrator 首先推断条件图像在最终视频中的最可能帧位置，随后围绕该锚点生成时序对齐的逐帧叙事描述。这一推理过程将原本隐式的、不可靠的时序关联转化为显式的、可解释的帧级语义引导。

### 2. 从“全局自注意力”到“多阶段时序锚点注意力”

在条件注入层面，ReasonDiff 用 **AlignFormer** 模块替代了基线模型中依赖自注意力的全局时序建模。AlignFormer 采用多阶段时序锚点注意力机制（Multi-stage Temporal Anchor Attention, MTAA）：以条件图像特征作为 Query，以 VisionNarrator 生成的逐帧叙事嵌入作为 Key 和 Value，通过缩放点积注意力为每一帧预测出推理增强的潜变量。这一设计将 MLLM 的高层推理信号精确地转化为帧级潜空间引导，使生成过程能够从锚点帧向其他帧传递语义与视觉信息，而非仅依赖噪声空间中的隐式关联。

### 关键变化总结

| 变化维度 | 基线方案 | ReasonDiff 方案 |
|---------|---------|----------------|
| 输入条件语义对齐 | 直接使用配对文本-图像，图像视为首帧 | VisionNarrator 推理图像在视频中的合理位置，生成时序对齐的逐帧叙事 |
| 帧级条件注入方式 | 条件图像特征直接注入或作为初始噪声，依赖自注意力学习全局动态 | AlignFormer 多阶段时序锚点注意力，从锚点图像和叙事预测帧级潜变量，再与去噪过程融合 |

这两个 changed slots 相互协同：VisionNarrator 提供高层推理能力，AlignFormer 将其转化为可操作的潜空间信号，使基座生成模型（基于 Wan2.1 的流匹配框架）能够在条件图像并非首帧的情况下，生成视觉与语义均连贯的视频。

## 整体框架

ReasonDiff 的整体架构由两个核心组件构成：**MLLM 驱动的多帧推理器（MLLM-Driven Multi-frame Reasoner）** 与 **推理引导的生成模型（Reasoning-Guided Generative Model）**，其协作流程如 Figure 2 所示。模型以非配对的文本提示和条件图像作为输入，输出一段视觉与语义均连贯的视频。

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the ReasonDiff model, which consists of two key components: (1) the MLLM-Driven Multi-frame Reasoner, and (2) the Reasoning-Guided Generative Model. The generative model operates under the guidance of the multi-modal reasoning results*

### 输入输出流

给定一个文本提示（如 “A cat plays in the room”）和一张条件图像（如 “a broken vase”），这两者之间不存在天然的时序对齐关系。ReasonDiff 的核心任务是将这对非配对的跨模态输入转化为一段完整的视频，且该视频需要同时忠实于文本语义和图像内容。

### 模块协作关系

1. **VisionNarrator（多模态推理叙事生成器）**  
   该模块利用一个冻结的多模态大语言模型（MLLM）对非配对的文本-图像输入进行高层语义推理。它首先推断条件图像在最终视频中最可能出现的帧位置（即“锚点帧”），然后围绕该锚点帧生成一段时序对齐的逐帧叙事（per-frame narratives）。这些叙事为后续的帧级生成提供了全局场景演进的逻辑骨架。

2. **AlignFormer（时序锚点注意力对齐器）**  
   AlignFormer 接收来自 VisionNarrator 的叙事嵌入以及锚点帧的图像特征，通过其核心机制——**多阶段时序锚点注意力（Multi-stage Temporal Anchor Attention, MTAA）**——逐步合成每一帧的推理增强潜变量（reasoning-enhanced latents）。MTAA 以锚点帧特征作为 Query，以叙事嵌入作为 Key 和 Value，利用交叉注意力将高层推理信息传递到所有帧的潜变量空间中，从而实现对未见帧的表征预测。

3. **推理引导的生成模型（Reasoning-Guided Generative Model）**  
   该组件以 **Wan2.1**（Team Wan et al., 2025）为基座视频生成器，在 AlignFormer 输出的推理增强潜变量和叙事条件的联合引导下，通过流匹配（flow matching）方式从噪声中逐步去噪生成最终视频。生成过程同时受到文本叙事和视觉推理信号的双重约束，确保输出视频在语义连贯性和视觉真实性之间取得平衡。

### 训练策略

为规避直接训练 MLLM 带来的高昂成本，VisionNarrator 在整个训练过程中保持冻结。训练任务被重新形式化为条件视频生成问题，分两阶段进行：第一阶段仅训练基座生成模型的标准流匹配去噪目标；第二阶段引入辅助重构损失，约束 AlignFormer 预测的潜变量与真实潜变量之间的差异（权重 β=0.2），从而强化推理信号对生成过程的引导能力。

## 核心模块与公式推导

ReasonDiff 的整体架构由三个核心模块构成：**VisionNarrator**（多模态推理叙事生成）、**AlignFormer**（时序锚点注意力对齐与潜变量预测）以及基于 **Wan2.1** 的推理引导生成模型。其中，前两者共同组成“MLLM 驱动的多帧推理器”（MLLM-Driven Multi-frame Reasoner），负责将高层多模态推理信号转化为可注入去噪过程的帧级引导信息。

### VisionNarrator：非配对输入的时序推理与叙事生成

VisionNarrator 利用一个冻结的多模态大语言模型（MLLM），对非配对的文本-图像输入进行高层语义推理。其核心功能包括两步：

1. **锚点定位**：MLLM 推断条件图像在最终视频中最可能出现的帧位置（即锚点索引），而非默认将其视为首帧。
2. **逐帧叙事生成**：围绕该锚点，MLLM 生成一段时序对齐的逐帧描述（per-frame narrative），为后续的帧级潜变量预测提供语义连贯的文本条件。

这一设计的关键在于将“非配对输入之间的隐含时序关联”显式化为可操作的文本序列，从而弥补传统视频生成模型在 OOD 场景下无法建立跨模态时序对应关系的缺陷。

### AlignFormer：多阶段时序锚点注意力与潜变量预测

AlignFormer 负责将 VisionNarrator 生成的逐帧叙事嵌入与锚点图像特征进行对齐，并预测出每一帧的“推理增强潜变量”（reasoning-enhanced latents）。其核心机制为**多阶段时序锚点注意力**（Multi-stage Temporal Anchor Attention, MTAA）。

**公式推导流程如下：**

首先，为锚点图像特征和叙事嵌入注入时序位置编码，以显式建模帧间时间顺序：

$$
\tilde{c}_i = \phi_{\mathrm{proj}}\left(\mathrm{Flatten}(c_i)\right) + \mathrm{pe}_i^{(\mathrm{time})}, \quad \tilde{h}_j = h_j + \mathrm{pe}_j^{(\mathrm{time})}
$$

其中 $c_i$ 为第 $i$ 帧锚点图像的 VAE 编码特征，经展平与投影后加上时序位置编码 $\mathrm{pe}_i^{(\mathrm{time})}$；$h_j$ 为第 $j$ 帧的叙事文本嵌入，同样加上对应的时序位置编码。

随后，将锚点特征映射为 Query，叙事嵌入映射为 Key 和 Value，构建交叉注意力：

$$
\mathbf{Q}_i = \mathbf{W}_{\mathrm{Q}} \tilde{c}_i, \quad \mathbf{K}_j = \mathbf{W}_{\mathrm{K}} \tilde{h}_j, \quad \mathbf{V}_j = \mathbf{W}_{\mathrm{V}} \tilde{h}_j
$$

通过缩放点积注意力，从锚点帧向其他帧传递信息，生成第 $j$ 帧的推理增强潜变量 $c_j^*$：

$$
c_j^* = \mathrm{Attn}(\mathbf{Q}_i, \mathbf{K}_j, \mathbf{V}_j) = \mathrm{Softmax}\left(\mathbf{Q}_i \mathbf{K}_j^T / \sqrt{d}\right) \mathbf{V}_j
$$

该机制的核心作用是：以锚点帧的视觉特征为“提问”（Query），以各帧的叙事描述为“上下文”（Key/Value），通过注意力权重自适应地聚合文本语义，从而为每一帧生成融合了高层推理信息的潜变量表示。多阶段的设计意味着该过程在多个特征层级上迭代进行，逐步细化帧间对齐。

### 推理引导生成模型的训练损失

基座视频生成器基于 Wan2.1 的流匹配（flow matching）框架。其标准训练目标为最小化预测速度场 $u_\theta$ 与真实速度场 $v(x_t)$ 之间的差异：

$$
\mathcal{L} = \mathbb{E}_{x_1, x_0 \sim \mathcal{N}(0,1), y, t \sim \mathcal{U}(0,1)} \left[ || u_\theta(x_t, y, t) - v(x_t) ||_2^2 \right]
$$

其中 $x_0$ 为标准高斯噪声，$x_1$ 为目标视频潜变量，$x_t = t x_1 + (1-t) x_0$ 为插值样本，条件速度场定义为 $v(x_t) = v(x_t \mid x_1) = x_1 - x_0$。

在 ReasonDiff 的第二阶段训练中，VisionNarrator 被冻结，训练被重构为条件视频生成任务。损失函数在标准去噪损失基础上，增加了 AlignFormer 预测潜变量 $c^*$ 与真实潜变量 $c$ 之间的辅助重构损失：

$$
\mathcal{L} = \mathbb{E}_{x_1, x_0, h, t, c} \left[ || u_\theta(x_t, h, c^*) - v(x_t) ||_2^2 + \beta \cdot || c^* - c ||_2^2 \right]
$$

其中 $h$ 为叙事嵌入，$c^*$ 为 AlignFormer 输出的推理增强潜变量，$\beta = 0.2$ 控制重构损失的权重。这一辅助损失强制 AlignFormer 学习预测与真实视频帧分布一致的潜变量，从而确保推理信号在注入去噪过程时不会引入域外偏差。

### 补充图表

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/003_Figure_3.jpg]]
*Figure 3: Reasoning results generated by the VisionNarrator. The conditions are the same as in Figure 1. We select some key frames and connect them with the related prompts using different colors*

## 实验与分析

### 主实验：非配对 OOD 场景下的定量评估

为验证 ReasonDiff 在非配对文本-图像输入下的视频生成能力，作者在 ActivityNet 数据集上构建了模拟非配对条件的测试基准，并与多个主流视频生成基线进行对比。**Table 1** 汇总了各模型在 ActivityNet（非配对）和 MSR-VTT（配对）上的定量指标。

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison between ReasonDiff and the baselines. The top and second top performances have been bolded or underlined respectively. Complete table with standard errors can be found in the supplementary materials*

在非配对 ActivityNet 场景下，ReasonDiff 在所有自动指标上均取得最优结果，唯一的例外是 CLIP Score (Image)。其中，**CLIP Score (Text)** 达到 0.571，相比最强基线 **Wan2.1**（Team Wan et al., 2025）的 0.490 提升了 16.5%，表明生成视频与输入文本的语义对齐度显著增强。在 **Imaging Quality** 指标上，ReasonDiff 取得 0.528，同样领先于所有对比方法。这一优势直接转化为用户偏好：在 **User Rank**（越低越好）上，ReasonDiff 获得 1.743，远优于 Wan2.1 的 2.692（差值 0.949），说明人类评估者更倾向选择 ReasonDiff 生成的视频。

值得注意的是，ReasonDiff 在 CLIP Score (Image) 上略低于部分基线。这一现象的成因在于：非配对条件下，输入图像并非视频首帧，而 CLIP Score (Image) 衡量的是生成帧与条件图像的整体相似度。当模型正确推理出条件图像在视频中的时序位置并生成合理的场景演进时，中间帧与条件图像的相似度自然下降，因此该指标的降低反而暗示模型进行了有效的时序推理，而非简单复制条件图像。

在配对条件的数据集 MSR-VTT 上，ReasonDiff 同样表现出竞争力，其 Imaging Quality 达到 0.571，甚至超越了其基座模型 Wan2.1。这证明 ReasonDiff 的多模态推理机制不仅适用于非配对场景，在常规配对条件下也不会损害生成质量。

### 消融实验：核心模块的有效性验证

为揭示各组件对性能的贡献，作者设计了四组消融变体，结果以完整模型为基准进行比例化展示（**Figure 5(a)**）。

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/006_Figure_5.jpg]]
*Figure 5: (a) Ablation studies on four variants of ReasonDiff. All metrics are reported as ratios relative to the full model. (b) Comparison between ReasonDiff and Wan2.1, where for Wan2.1 the prompt is rewritten using an MLLM and the condition index is manually selected*

- **移除增强潜变量（Excluding Enhanced Latents）**：直接禁用 AlignFormer 生成的推理增强帧级潜变量，导致 **Imaging Quality 大幅下降**。这表明 AlignFormer 预测的潜变量是维持视频视觉质量的关键信号，单纯的文本叙事不足以在潜空间层面引导高质量生成。

- **禁用多帧叙事提示（Disabling Multi-frame Prompt）**：将 VisionNarrator 生成的逐帧叙事替换为单一全局描述，导致 **Dynamic Degree 急剧下降**。这验证了逐帧时序对齐的叙事对于驱动视频动态演进至关重要，全局描述无法提供足够的帧间变化信息。

- **移除辅助重构损失（Removing Auxiliary Loss）**：去掉训练损失中的 $\beta \cdot ||c^* - c||_2^2$ 项（$\beta=0.2$），导致 **Motion Smooth 等指标明显下降**。该辅助损失强制 AlignFormer 预测的潜变量与真实视频帧的潜变量对齐，缺失时模型难以学习准确的帧级表征，运动连贯性受损。

- **替换为简单提示词重写（Rewrite Prompt）**：用 MLLM 仅重写输入文本而不生成逐帧叙事，同时手动选择条件帧索引。该变体虽能维持较高的 CLIP-Image 分数，但 **CLIP-Text 分数严重下降**。这进一步证实：仅靠文本重写无法恢复非配对输入间的时序关联，VisionNarrator 的逐帧推理是实现文本-视频语义对齐的核心。

### 定性分析与失败模式

**Figure 4** 展示了 ReasonDiff 与基线方法在多个非配对输入下的定性对比。以“文本提示为 *A cat plays in the room*，条件图像为 *一个破碎的花瓶*”为例，**CogVideoX**（Yang et al., 2024）和 **Dynamicrafter**（Xing et al., ECCV 2024）生成的视频要么忽略了文本中的猫，要么未能体现花瓶破碎的场景演进。**LTX-Video**（HaCohen et al., 2025）和 Wan2.1 虽能生成部分相关元素，但时序连贯性不足。相比之下，ReasonDiff 成功生成了“猫在房间玩耍导致花瓶破碎”的完整叙事线，视觉与语义均保持连贯。

**Figure 5(b)** 进一步对比了 ReasonDiff 与 Wan2.1 在 MLLM 重写提示下的表现。即使为 Wan2.1 提供相同的 MLLM 重写提示并手动指定条件帧索引，其生成质量仍显著低于 ReasonDiff。这证明 ReasonDiff 的优势并非仅来自 MLLM 的文本推理能力，更关键的是 AlignFormer 将推理信号转化为帧级潜变量引导的机制。

### 证据强度总结

| 核心主张 | 证据来源 | 置信度 |
|---------|---------|--------|
| 非配对场景下文本-视频语义对齐显著提升 | CLIP Score (Text) 较 Wan2.1 提升 16.5% | 高（定量指标+用户评估） |
| 用户偏好显著优于最强基线 | User Rank 1.743 vs 2.692 | 高（人类评估） |
| AlignFormer 增强潜变量对成像质量至关重要 | 移除后 Imaging Quality 大幅下降 | 高（消融实验） |
| 多帧叙事对动态程度至关重要 | 禁用后 Dynamic Degree 急剧下降 | 高（消融实验） |
| 辅助重构损失对运动平滑性至关重要 | 移除后 Motion Smooth 明显下降 | 中高（消融实验） |

### 需人工验证的要点

- 论文未提供 ActivityNet 非配对条件的具体构造方式（如条件帧索引的分布、文本-图像不匹配程度的控制），该基准的生态效度需结合补充材料判断。
- 消融实验中各项指标的具体数值未在正文给出，仅以比例图展示，精确效应量需查阅补充材料中的完整表格。
- 模型在真实世界非配对输入（如用户随意上传的图像与文本）上的泛化表现尚未验证，当前结论限于人工构造的测试条件。

### 补充图表

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of generated results from different models under OOD scenario with unpaired text-image inputs: i) the textual prompt A cat plays in the room and ii) the visual condition image a broken vase in Figure 1(a). Intermediate frames are selected for the convenience of presentation. Our proposed ReasonDiff has the best result with a visually and semantically coherent video*

![[assets/figures/papers/paper_list_l919_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Reasoning_Diffusio/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison between ReasonDiff and the baselines. We select several intermediate frames for the convenience of presentation. For ease of illustration, we provide more generated results and the video samples in the supplement*

## 方法谱系与知识库定位

### 1. 与基座模型的关系：从 Wan2.1 到推理引导的范式跃迁

ReasonDiff 并非从零构建的视频生成模型，而是以 **Wan2.1**（Team Wan et al., 2025, arXiv）作为推理引导生成模型的基座。Wan2.1 本身是一个基于流匹配（flow matching）的 SOTA 视频生成器，其核心训练目标为：

$$ \mathcal { L } = \mathbb { E } _ { x _ { 1 } , x _ { 0 } \sim \mathcal { N } ( 0 , 1 ) , y , t \sim \mathcal { U } ( 0 , 1 ) } \left[ | | u _ { \theta } ( x _ { t } , y , t ) - v ( x _ { t } ) | | _ { 2 } ^ { 2 } \right] $$

其中条件速度场定义为 $v ( x _ { t } ) = v ( x _ { t } \mid x _ { 1 } ) = x _ { 1 } - x _ { 0 }$。Wan2.1 在配对输入场景下已表现出色，但其设计假设输入条件（文本和图像）天然对齐——图像被视为视频首帧，文本为全局描述。当面对非配对 OOD 输入时，这一假设崩塌：模型无法推理条件图像在视频时间线中的合理位置，导致生成结果偏向某一模态或丧失时序连贯性。

ReasonDiff 的关键跃迁在于**不修改 Wan2.1 的去噪骨干**，而是在其上游插入一个多模态推理层（VisionNarrator + AlignFormer），将非配对条件转化为时序对齐的帧级潜变量引导。第二阶段训练损失明确体现了这一设计哲学：

$$ \mathcal L = \mathbb { E } _ { x _ { 1 } , x _ { 0 } , h , t , c } \left[ | | u _ { \theta } ( x _ { t } , h , c ^ { * } ) - v ( x _ { t } ) | | _ { 2 } ^ { 2 } + \beta \cdot | | c ^ { * } - c | | _ { 2 } ^ { 2 } \right] $$

其中 $c^*$ 为 AlignFormer 预测的推理增强潜变量，$c$ 为真实潜变量，$\beta = 0.2$。辅助重构损失迫使 AlignFormer 学习从锚点图像和叙事中恢复完整帧序列，而标准去噪损失则确保生成质量。这种“冻结基座 + 轻量适配”的策略使 ReasonDiff 在保持 Wan2.1 生成能力的同时，获得了对非配对输入的鲁棒性。

### 2. 与同类基线的方法论对比

当前文本-图像到视频生成领域的主流方法可归为三类，ReasonDiff 与它们在输入假设和条件注入方式上存在根本差异：

**（1）配对条件生成模型：Wan2.1、CogVideoX、LTX-Video**

- **Wan2.1**（Team Wan et al., 2025, arXiv）：基于流匹配，将条件图像直接作为初始帧注入潜空间，依赖自注意力学习全局时序动态。在非配对场景下，图像可能对应视频中任意帧，该假设失效。
- **CogVideoX**（Yang et al., 2024, arXiv）：采用级联扩散架构，同样假设图像为首帧，文本为全局语义约束。缺乏对条件帧位置的推理能力。
- **LTX-Video**（HaCohen et al., 2025, arXiv）：基于 Transformer 的视频生成器，条件注入方式与 Wan2.1 类似，未针对非配对输入设计专门的对齐机制。

这三类方法的共同瓶颈在于**条件语义对齐槽位**：它们将输入条件视为“给定事实”而非“待推理线索”。ReasonDiff 通过 VisionNarrator 将该槽位从“直接使用配对条件”改为“推理条件图像在视频中的合理位置并生成时序对齐的逐帧叙事”，从根本上改变了条件信息的利用方式。

**（2）图像动画化模型：Dynamicrafter**

- **Dynamicrafter**（Xing et al., ECCV 2024）：将静态图像作为唯一视觉条件，通过文本描述驱动运动生成。其本质是图像到视频的动画化，而非真正的多模态条件融合。当文本与图像语义不匹配时，Dynamicrafter 倾向于保留图像内容而忽略文本引导，导致语义偏离。

ReasonDiff 与之相比，在**帧级条件注入方式**上存在本质差异：Dynamicrafter 将条件图像特征直接注入去噪过程，而 ReasonDiff 利用 AlignFormer 的多阶段时序锚点注意力（Multi-stage Temporal Anchor Attention, MTAA）机制，从锚点图像和叙事嵌入中预测出推理增强的帧级潜变量。具体而言，MTAA 通过以下步骤实现跨模态对齐：

$$ \tilde { c } _ { i } = \phi _ { \mathrm { p r o j } } \left( \mathrm { F l a t t e n } ( c _ { i } ) \right) + \mathrm { p e } _ { i } ^ { ( \mathrm { t i m e } ) } , \quad \tilde { h } _ { j } = h _ { j } + \mathrm { p e } _ { j } ^ { ( \mathrm { t i m e } ) } $$

$$ \mathbf { Q } _ { i } = \mathbf { W } _ { \mathrm { Q } } \tilde { c } _ { i } , \quad \mathbf { K } _ { j } = \mathbf { W } _ { \mathrm { K } } \tilde { h } _ { j } , \quad \mathbf { V } _ { j } = \mathbf { W } _ { \mathrm { V } } \tilde { h } _ { j } $$

$$ c _ { j } ^ { * } = \mathrm { A t t n } ( \mathrm { Q } _ { i } , \mathrm { K } _ { j } , \mathrm { V } _ { j } ) = \mathrm { S o f t m a x } \left( \mathrm { Q } _ { i } \mathrm { K } _ { j } ^ { T } / \sqrt { d } \right) \mathrm { V } _ { j } $$

这一机制的核心在于：锚点图像特征作为 Query，逐帧叙事嵌入作为 Key 和 Value，通过交叉注意力将高层推理信号转化为帧级潜变量。时序位置编码的引入确保了帧间顺序的显式建模，使模型即使条件图像并非首帧也能生成时序连贯的视频。

### 3. 核心洞察与适用边界

ReasonDiff 的核心洞察可概括为：**将高层多模态推理与低层视频去噪生成解耦**。利用 MLLM 推断合理的场景演进序列，再通过专用的跨注意力模块将推理信号注入扩散模型的潜变量空间。这一设计使模型获得了对非配对输入的鲁棒性，但也划定了其适用边界：

**适用场景**：
- 输入文本和图像存在可推理的语义关联（即使表面不匹配），例如“猫在房间里玩耍”与“破碎的花瓶”图像——VisionNarrator 可推断出猫打碎花瓶的叙事链条。
- 条件图像对应视频中某一帧（不一定是首帧），需要模型自主推理其时序位置。
- 需要生成视觉与语义均连贯的视频，而非仅偏重某一模态。

**不适用场景**：
- 输入图像与文本在语义上完全无法建立合理关联时，VisionNarrator 可能生成不符合真实世界逻辑的叙事。这一边界情况在论文中未被充分探索，属于开放问题。
- 对推理延迟敏感的应用：VisionNarrator 依赖冻结的 MLLM 进行逐帧推理，虽然不参与梯度更新，但推理阶段的前向传播仍引入额外计算开销。论文未报告具体的推理时间对比，该点需要手动验证。

### 4. 消融实验揭示的因果机制

消融实验（Figure 5a）为理解各模块的因果贡献提供了关键证据：

- **移除增强潜变量（Excluding Enhanced Latents）**：直接导致 Imaging Quality 大幅下降。这表明 AlignFormer 预测的帧级潜变量不仅是“锦上添花”的辅助信号，而是维持视频成像质量的关键条件——没有它，基座模型退化为缺乏帧间引导的盲目生成。
- **禁用多帧叙事提示（Disabling Multi-frame Prompt）**：导致 Dynamic Degree 显著下降。这说明逐帧叙事并非冗余信息，而是驱动视频动态性的核心因素。单帧全局描述无法提供足够的时序变化信息。
- **去除辅助重构损失（Removing Auxiliary Loss）**：使 Motion Smooth 等指标明显下降。辅助损失 $\beta \cdot | | c ^ { * } - c | | _ { 2 } ^ { 2 }$ 在训练阶段强制 AlignFormer 学习从锚点恢复完整帧序列的能力，去除后模型失去了这一约束，导致运动平滑性受损。
- **将 VisionNarrator 替换为简单提示重写（Rewrite Prompt）**：虽然能维持较高的 CLIP-Image 分数，但 CLIP-Text 分数严重下降。这揭示了 MLLM 推理的不可替代性——简单的文本重写无法建立图像与文本之间的深层时序关联，模型退化为偏向视觉条件的生成。

### 5. 开放问题与未验证声明

论文在以下方面留下了开放空间，需后续工作验证：

1. **VisionNarrator 的鲁棒性边界**：当输入图像与文本在语义上完全无法建立合理关联时（例如“宇航员在月球漫步”与“海底珊瑚礁”图像），VisionNarrator 能否始终生成连贯且符合真实世界逻辑的叙事？论文未对此极端情况进行测试。

2. **叙事质量的可量化评估**：如何定量评估 VisionNarrator 生成的每帧描述与最终视频的一致性？论文依赖下游视频质量指标间接反映叙事质量，缺乏对叙事模块本身的直接评估。此外，该模块在不同 MLLM（如 GPT-4V、Gemini Pro Vision）上的迁移性如何，论文未涉及。

3. **非配对数据的泛化能力**：训练集中的人工构造的非配对条件（从 ActivityNet 视频中随机抽取非首帧作为条件图像）是否能覆盖真实场景的分布？真实 OOD 输入可能包含更复杂的语义错位模式，模型在大规模、多样化非配对数据上的泛化能力尚待验证。

4. **计算开销的透明化**：论文未报告 VisionNarrator 推理阶段的延迟和显存占用。考虑到 MLLM 的前向传播成本，这一信息对实际部署至关重要，需要手动验证或等待作者开源代码后补充。

## 原文 PDF

![[paperPDFs/CVPR_2026/Reasoning_Diffusion_for_Unpaired_Test_Time_Out_of_distribution_Text_Image_to_Video_Generation.pdf]]