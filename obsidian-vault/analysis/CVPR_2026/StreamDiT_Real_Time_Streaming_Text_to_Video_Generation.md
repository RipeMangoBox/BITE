---
title: "StreamDiT: Real-Time Streaming Text-to-Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/StreamDiT_Real_Time_Streaming_Text_to_Video_Generation.pdf
project_link: "https://cumulo-autumn.github.io/StreamDiT/"
code_link: null
aliases:
- StreamDiT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过引入带有逐帧不同噪声等级的移动缓冲区（Buffered Flow Matching）和混合分块训练策略，统一了均匀噪声、对角线噪声等多种去噪方案，模型能够泛化到流式推理，在不牺牲一致性的前提下实现逐块输出。
primary_logic: 核心洞察在于：在DiT架构中将时间条件从标量扩展为沿帧维度分离的序列（变时间嵌入），配合窗口注意力降低计算复杂度，并通过混合不同分块方案训练，使模型能够从全注意力标准生成平滑过渡到流式生成；同时，针对分块结构设计的多步蒸馏大幅减少了采样步数，实现实时性能。
claims:
- StreamDiT在VBench的综合质量得分（0.8185）显著高于ReuseDiffuse（0.8019）和FIFO-Diffusion（0.7981），蒸馏后模型（0.8163）仍接近教师模型。
- "混合训练所有分块大小的模型（chunk sizes [1,2,4,8,16]）取得最佳质量得分0.8144，优于固定单一尺寸的训练。"
- 蒸馏后的StreamDiT-4B在单张H100 GPU上达到512p分辨率16 FPS的实时流式生成。
- 人类评估中，我们的模型在总体质量、帧一致性、运动完整性、运动自然度等方面胜率均高于基线方法。
---

# StreamDiT: Real-Time Streaming Text-to-Video Generation

> [!tip] 核心洞察
> 核心洞察在于：在DiT架构中将时间条件从标量扩展为沿帧维度分离的序列（变时间嵌入），配合窗口注意力降低计算复杂度，并通过混合不同分块方案训练，使模型能够从全注意力标准生成平滑过渡到流式生成；同时，针对分块结构设计的多步蒸馏大幅减少了采样步数，实现实时性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | StreamDiT：实时流式文本到视频生成 |
| 英文题名 | StreamDiT: Real-Time Streaming Text-to-Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.03745) · [Project](https://cumulo-autumn.github.io/StreamDiT/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | StreamDiT |
| Dataset | VBench, Inference Speed |

> [!tip] 效果简介
> - VBench 上，Quality Score 0.8185 (Teacher) / 0.8163 (Distill) vs 0.8019 (ReuseDiffuse) / 0.7981 (FIFO) (+0.0166 / +0.0204 (Teacher vs baselines))；Subject Consistency 0.9622 vs 0.9501 (ReuseDiffuse) / 0.9412 (FIFO) (+0.0121 / +0.0210)；Dynamic Degree 0.5240 (Teacher) / 0.7040 (Distill) vs 0.2900 (ReuseDiffuse) / 0.3094 (FIFO) (+0.2340 / +0.3946 (Teacher))。
> - Inference Speed 上，FPS 16 vs N/A。

## 概要

现有基于 DiT 的文本到视频（T2V）生成模型面临一个根本性瓶颈：自注意力机制的二次计算复杂度与离线批处理范式，使得在低延迟约束下生成长视频极为困难，难以支撑实时交互应用。同时，自回归生成范式在视频质量上普遍弱于双向全注意力扩散模型。StreamDiT 针对这一矛盾，提出了一套从训练框架到模型架构再到推理加速的完整解决方案。

**核心思路**：在流匹配（Flow Matching）框架中引入**缓冲流匹配（Buffered Flow Matching）**——为移动缓冲区中的不同帧分配逐帧分离的噪声等级，配合**混合分块训练策略**，统一了均匀噪声、对角线噪声等多种去噪方案，使模型能够从标准全注意力生成平滑泛化到流式逐块输出。在模型层面，将时间条件从标量扩展为沿帧维度可分离的**变时间嵌入（Varying Time Embedding）**，并用**窗口注意力**替代全注意力以降低计算复杂度。在推理层面，针对分块结构设计**分段多步蒸馏**，将每个分段的多个微步压缩为单步，最终在单张 H100 GPU 上实现 512p 分辨率 **16 FPS** 的实时流式生成。

**主要结果**：
- 在 VBench 基准上，StreamDiT 教师模型综合质量得分达到 **0.8185**，显著优于 ReuseDiffuse（0.8019）和 FIFO-Diffusion（0.7981）；蒸馏后模型（0.8163）仍接近教师水平（Table 2）。
- 混合训练所有分块大小（[1,2,4,8,16]）取得最佳质量得分 0.8144，验证了统一训练策略的泛化优势（Table 3）。
- 人类评估中，StreamDiT 在总体质量、帧一致性、运动完整性、运动自然度四个维度上胜率均高于基线方法（Figure 5）。

**方法定位**：StreamDiT 处于流式视频生成与 DiT 架构的交汇点，通过“缓冲流匹配 + 变时间嵌入 + 窗口注意力 + 分段蒸馏”四位一体的设计，首次在 DiT 范式下实现了高质量实时流式 T2V 生成，并支持无限时长流式输出与交互式提示词导航。

### 文本到视频生成中的“实时”困境

近年来，基于扩散模型（Diffusion Models）和流匹配（Flow Matching）的文本到视频（T2V）生成取得了显著进展，能够产出高保真、时序连贯的视频内容。然而，这些模型大多采用**离线批处理范式**：用户输入提示词后，需等待完整视频生成完毕才能观看，整个过程通常耗时数十秒甚至数分钟。这种“先完成、后播放”的模式，从根本上阻断了实时交互的可能性——用户无法在生成过程中介入、引导或修改视频走向。

更深层的瓶颈在于模型架构本身。当前主流的 T2V 模型多基于 Diffusion Transformer（DiT）架构，其核心组件**自注意力机制的计算复杂度随序列长度呈二次增长**。对于长视频生成，这意味着推理延迟与显存占用急剧膨胀，使得低延迟流式输出变得极不现实。此外，一些方法尝试用自回归范式逐帧生成视频以模拟流式效果，但自回归生成在视觉质量和时序一致性上显著弱于具备双向注意力的扩散模型，且误差累积问题随视频长度加剧。

### 现有流式方案的尝试与不足

针对上述困境，学术界已开始探索“流式”视频生成方法，试图将去噪过程重新组织为逐步输出的流水线。其中代表性工作包括：

- **ReuseDiffuse**：基于预训练扩散模型，通过迭代去噪策略实现流式输出。但其去噪调度与标准训练范式存在偏差，导致生成质量下降。
- **FIFO-Diffusion**：采用对角线去噪队列，以先入先出的方式管理不同噪声等级的帧。该方法在推理效率上有所改进，但复杂的队列管理策略引入了额外的时序不一致风险。

这些方法虽然在一定程度上实现了“边生成边输出”，但普遍存在一个根本性矛盾：**推理时的流式去噪策略与训练时的标准全注意力去噪策略不一致**。模型在训练中从未见过流式推理所需的“部分去噪、部分噪声”的混合状态，导致推理时出现分布偏移，损害生成质量。此外，这些方法在生成长视频时，内容重复和身份漂移问题依然突出。

### 本文的核心动机

StreamDiT 的提出源于一个关键洞察：**流式生成不应是训练后强行适配的推理技巧，而应当被原生地融入训练框架之中**。具体而言，本文试图回答以下问题：

1. **能否设计一种训练范式，使模型天然具备流式推理能力？** 即训练时就让模型学会处理“同一批次内不同帧处于不同去噪阶段”的混合状态，从而消除训练-推理不一致。
2. **能否在降低自注意力计算复杂度的同时，保持甚至提升生成质量？** 即用高效的局部注意力替代全局注意力，同时不牺牲时序一致性。
3. **能否通过蒸馏等手段，将推理步数压缩到极致，实现真正的实时生成？** 即在单张 GPU 上达到 16 FPS 以上的流式输出速率。

StreamDiT 通过在流匹配框架中引入**移动缓冲区**和**混合分块训练**策略，统一了均匀噪声、对角线噪声等多种去噪方案，使模型能够泛化到流式推理场景。配合**变时间嵌入**和**窗口注意力**的架构改进，以及**分段多步蒸馏**的加速策略，最终在 4B 参数规模下实现了 512p 分辨率、16 FPS 的实时流式文本到视频生成，且质量显著优于现有流式基线方法。

## 核心方法与创新机理

StreamDiT 的核心创新在于将标准流匹配（Flow Matching）从“全量批处理”范式重构为“移动缓冲区渐进去噪”范式，并通过三个关键改造槽位（changed slots）实现这一转变。这些改造并非孤立的技术点，而是围绕一个统一的因果机制：**让模型在训练中学会处理逐帧不同的噪声等级，从而在推理时能够以分块流式的方式逐步生成视频，同时保持与全注意力模型相近的质量**。

### 从标量时间到序列时间：变时间嵌入

标准 DiT 模型以单一的标量 $t$ 作为时间条件，作用于所有帧。StreamDiT 将这一条件扩展为沿帧维度分离的序列 $\tau$（变时间嵌入）。在缓冲流匹配框架下，缓冲区中的每一帧被分配了不同的噪声等级，因此模型必须能够感知并区分这些差异化的时间信号。具体实现上，StreamDiT 修改了 adaLN DiT 的调制机制，将变时间嵌入应用于缩放和平移调制参数（Figure 3），使每一帧的归一化参数由其自身的噪声等级独立决定。这一改造是支撑“同一批次内混合去噪进度”的架构基础，也是缓冲流匹配训练能够生效的前提。

### 从全注意力到窗口注意力：降低流式推理的计算瓶颈

标准 DiT 的自注意力具有二次计算复杂度，直接应用于长序列视频潜变量会导致推理延迟无法满足实时需求。StreamDiT 将全注意力替换为窗口注意力（Window Attention），将 3D 潜变量划分为规则窗口并在窗口内执行局部自注意力，同时通过窗口移位（shifted windows）实现窗口间的信息交互（Figure 4）。这一改造不仅大幅降低了计算复杂度，还与分块流式推理天然兼容：每个分块仅需关注其局部上下文，无需等待全局信息。窗口注意力是 StreamDiT 在单张 H100 GPU 上实现 512p 分辨率 16 FPS 实时生成的关键效率保障。

### 缓冲流匹配 + 混合分块训练：统一多种去噪方案的训练框架

这是 StreamDiT 最核心的方法创新。传统流匹配对整个视频序列施加统一的噪声等级，而 StreamDiT 在训练时构造一个移动缓冲区，为不同帧分配渐进变化的噪声等级（Buffered Flow Matching），使模型学会在同一个前向传播中处理处于不同去噪阶段的帧。在此基础上，StreamDiT 设计了混合分块训练策略（Mixed Partitioning Scheme），将参考帧数 $K$、分块大小 $c$ 和每个分块的微步数 $s$ 进行灵活组合（Table 1），训练时随机混合所有分块配置。这一策略统一了均匀噪声去噪、对角线去噪（FIFO-Diffusion 的方案）和自回归扩散（$c=1$ 的特例）等多种范式。消融实验（Table 3）证实，混合训练所有分块大小（[1,2,4,8,16]）取得最佳 VBench 质量得分 0.8144，优于任一固定分块配置，证明了混合训练带来的泛化优势。

### 分段多步蒸馏：从教学模型到实时模型的效率跃迁

StreamDiT 的蒸馏策略针对分块结构进行了专门设计。教师模型采用 $c=2, s=16, N=8$ 的分块方案进行推理，每个分块需要 16 个微步完成去噪。蒸馏过程将每个分段的多个微步逐步合并为单步（Multistep Distillation per segment），最终将总采样步数从 $16 \times 8 = 128$ 步压缩至 8 步，同时移除分类器自由引导（CFG）以进一步降低计算开销。蒸馏后的模型在 VBench 质量得分上仅从 0.8185 略微下降至 0.8163，保持了接近教师模型的生成质量。

### 创新点之间的因果关联

上述四个改造槽位构成了一个紧密耦合的创新链条：**变时间嵌入**使模型能够处理逐帧差异化的噪声等级，这是**缓冲流匹配**训练的架构前提；**混合分块训练**让模型在多种分块配置下均能泛化，为流式推理提供了灵活性；**窗口注意力**降低了计算复杂度，使流式推理在硬件上可行；**分段多步蒸馏**则将推理步数压缩至极致，最终实现实时性能。四个改造相互依赖，缺一不可——如果仅替换注意力机制而不改变时间条件和训练框架，模型将无法在流式场景下保持一致性；如果仅改变训练框架而不进行蒸馏，推理延迟将无法满足实时要求。

StreamDiT 构建了一条从文本提示到实时视频流的完整生成管线，其核心设计围绕**缓冲流匹配（Buffered Flow Matching）** 训练框架与**变时间嵌入 DiT 骨干网络**展开，并通过多步蒸馏实现推理加速。整个系统由五个关键模块串联而成，形成“文本编码 → 潜变量初始化 → 缓冲区分块去噪 → 潜变量解码 → 流式输出”的处理链路。

### 输入与输出流

系统的输入端接收用户提供的文本提示 $\\mathbf{P}$，该提示经由三条并行的文本编码通路处理：**UL2**、**ByT5** 和 **Meta-CLIP**，将自然语言描述转换为嵌入向量。值得强调的是，文本编码器仅在提示词发生变化时才重新运行（见 Figure 11），这一设计显著降低了交互式场景下的计算开销。

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/015_Figure_11.jpg]]
*Figure 11: Interactive inference pipeline of StreamDiT: To decrease latency, generative models, decoder and text encoder are in separate process*

输出端则产生连续的 RGB 视频帧。在进入最终解码之前，模型在压缩的潜变量空间中操作：时间自编码器（Temporal Auto-encoder, TAE）对视频执行时间域 4 倍、空间域 8 倍的压缩，将潜变量通道数压缩至 8。推理时，解码器与生成模型分离为独立进程，以流水线方式并行工作，降低端到端延迟。

### 核心模块关系

整个框架的运作逻辑可以按以下流程理解：

1. **文本编码（Text Encoders）**：将提示词 $\\mathbf{P}$ 转化为嵌入，仅在提示词更新时触发。
2. **潜变量初始化**：在 T2V 场景下，StreamDiT 首先执行标准分块生成，准备中间潜变量缓存；当缓存填满后，从中检索适当的分块构建初始流队列（Stream Queue）。
3. **缓冲流匹配训练/推理（Buffered Flow Matching）**：这是框架的核心训练与推理范式。它将视频帧序列组织为一个**移动缓冲区**，缓冲区被划分为 $K$ 个参考帧和 $N$ 个分块（chunk），每个分块包含 $c$ 帧，并经历 $s$ 个微去噪步（micro denoising steps）。缓冲区总帧数 $B$ 与总去噪步数 $T$ 满足约束 $B = K + N \\times c$，$T = s \\times N$（Eq. 7）。训练时，为每个分块的第 $i$ 帧分配不同的噪声等级 $\\tau_i$，从对应的时间区间均匀采样（Eq. 8）；推理时，缓冲区沿预测速度方向逐步更新（Eq. 6），已去噪完成的帧从缓冲区头部移出并输出，同时新的噪声帧从尾部补入，形成流式推进。
4. **混合分块训练（Mixed Partitioning Scheme）**：在训练阶段，分块大小 $c$ 和微步数 $s$ 并非固定，而是在 $[1, 2, 4, 8, 16]$ 等配置中随机混合采样（Table 1）。这种统一的分块策略将均匀噪声去噪、对角线去噪队列（如 FIFO-Diffusion）、自回归扩散（$c=1$）以及标准全批量 T2V（$c=16$）统一到同一框架下，使模型能够泛化到不同的流式推理配置。
5. **变时间嵌入 DiT（Time-varying adaLN DiT）**：骨干网络在标准 adaLN DiT 的基础上，将时间条件从标量 $t$ 扩展为沿帧维度分离的序列 $\\tau$（变时间嵌入），使模型能同时处理缓冲区中处于不同去噪阶段的帧。配合**窗口注意力（Window Attention）** 机制，将 3D 潜变量划分为规则窗口和移位窗口（Figure 4）进行局部自注意，在降低二次计算复杂度的同时，通过窗口移位实现全局信息交互。
6. **多步蒸馏（Multistep Distillation）**：教师模型以 $c=2, s=16, N=8$ 的分块配置进行推理。蒸馏过程将每个分段的 $s$ 个微步压缩为单步，并移除分类器自由引导（CFG），最终将总采样步数降至 8 步，使模型在单张 H100 GPU 上达到 512p 分辨率 16 FPS 的实时流式生成。

### 推理流水线架构

在实际部署中，StreamDiT 采用多线程流水线设计（Figure 11）：生成模型、解码器和文本编码器分别运行在独立进程中。当用户交互式地输入新提示词时，文本编码器异步更新嵌入，生成模型基于更新后的引导继续去噪轨迹。需要注意的是，随着去噪进入后期阶段，改变文本引导对生成结果的影响逐渐减弱（Figure 12），因此交互式控制更适合在去噪早期施加。

> **证据强度说明**：上述框架描述基于论文 Sec. 3.1–3.2 和 Sec. 4.1–4.2 的方法阐述，以及 Figure 2、Figure 3、Figure 11 的架构图示。各模块的消融验证和性能数据详见后续实验分析章节。

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of StreamDiT partitioning. We partition the buffer to K reference frames and N chunks. Each chunk has c frames and s micro denoising steps*

### 3.1 缓冲流匹配（Buffered Flow Matching）

StreamDiT 的训练框架建立在流匹配（Flow Matching, FM）之上。标准 FM 通过线性插值构造训练样本，并预测从噪声指向数据的速度向量：

**训练样本构造**（Eq. 1）：

$$\mathbf{X}_t = t \mathbf{X}_1 + \left( 1 - ( 1 - \sigma_{\min} ) t \right) \mathbf{X}_0$$

其中 $\mathbf{X}_0$ 为噪声，$\mathbf{X}_1$ 为数据，$t \in [0, 1]$ 为时间步。

**目标速度**（Eq. 2）：

$$\mathbf{V}_t = \frac{d \mathbf{X}_t}{dt} = \mathbf{X}_1 - ( 1 - \sigma_{\min} ) \mathbf{X}_0$$

该速度向量与 $t$ 无关，是流匹配的回归目标。

**训练损失**（Eq. 3）：

$$\mathbb{E}_{t, \mathbf{X}_t} \| u( \mathbf{X}_t, \mathbf{P}, t; \Theta ) - \mathbf{V}_t \|^2$$

模型 $u(\cdot)$ 以文本提示 $\mathbf{P}$ 为条件，预测速度并与目标速度求均方误差。

**关键创新**在于将标准 FM 扩展为缓冲流匹配：引入一个沿帧维度具有**不同噪声等级**的移动缓冲区。具体而言，为缓冲区中第 $i$ 帧分配独立的时间 $\tau^i$，构造带噪样本（Eq. 5）：

$$\mathbf{X}_{\tau}^i = \tau \circ \mathbf{\Delta} \mathbf{X}_1^i + ( 1 - ( 1 - \sigma_{\min} ) \tau ) \circ \mathbf{\Delta} \mathbf{X}_0$$

其中 $\circ$ 表示逐元素乘法，$\mathbf{\Delta} \mathbf{X}_1^i$ 为第 $i$ 帧的数据增量。推理时，缓冲区沿预测速度方向更新（Eq. 6）：

$$\mathbf{X}_{\tau + \Delta \tau}^i = \mathbf{X}_{\tau}^i + u( \mathbf{X}_{\tau}^i, \mathbf{P}, \tau; \Theta ) \circ \Delta \tau$$

缓冲区总帧数 $B$ 与总去噪步数 $T$ 满足约束（Eq. 7）：

$$B = K + N \times c, \quad T = s \times N$$

其中 $K$ 为参考帧数，$N$ 为分块数，$c$ 为每块帧数，$s$ 为每块微去噪步数。

### 3.2 混合分块训练（Mixed Partitioning Scheme）

StreamDiT 的核心训练策略是**混合分块训练**，统一了均匀噪声、对角线噪声等多种去噪方案（Table 1）。训练时，为第 $i$ 个分块从对应时间区间均匀采样子时间步（Eq. 8）：

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/003_Table_1.jpg]]
*Table 1: StreamDiT unifies different partitioning schemes*

$$\tau_i \sim \mathrm{Uniform}\left( \left[ \frac{T}{N} \cdot (i-1), \frac{T}{N} \cdot i \right] \right)$$

训练过程中随机混合不同的分块大小（如 chunk sizes [1, 2, 4, 8, 16]），使模型能够泛化到流式推理场景。消融实验（Table 3）证实，混合所有分块大小的训练策略取得最佳 VBench 质量得分 0.8144，优于固定单一尺寸（如 chunk size=1 的 0.8129）。

### 3.3 变时间嵌入与窗口注意力

骨干网络在 adaLN DiT 基础上进行两项关键改造：

**变时间嵌入（Varying Time Embedding）**：将原本的标量时间条件 $t$ 扩展为沿帧维度可分离的序列 $\tau$，使模型能够同时处理缓冲区中处于不同去噪阶段的帧。具体实现是将变时间嵌入作用于 adaLN 的 scale 和 shift 调制参数（Figure 3）。

**窗口注意力（Window Attention）**：将 3D latent 划分为规则窗口并执行局部自注意力，通过窗口移位（shifted windows）实现跨窗口的全局信息交互（Figure 4）。这一设计将自注意力的二次计算复杂度降至窗口内线性复杂度，是流式低延迟推理的关键。

### 3.4 多步蒸馏（Multistep Distillation）

为达到实时性能，StreamDiT 采用**分段多步蒸馏**策略。教师模型使用分块方案 $c=2, s=16, N=8$ 进行推理（共 128 微步），蒸馏后将每个分段的 $s$ 个微步压缩为 1 步，并移除分类器自由引导（CFG），最终将总采样步数降至 8 步。蒸馏后模型在单张 H100 GPU 上实现 512p 分辨率 16 FPS 的实时流式生成。

## 实验与关键发现

### 主实验结果

**VBench 自动评估**。Table 2 报告了 StreamDiT 在 VBench 基准上的综合质量得分。教师模型（Teacher）取得 **0.8185** 的总分，显著优于流式生成基线 ReuseDiffuse（0.8019）和 FIFO-Diffusion（0.7981），分别领先 +0.0166 和 +0.0204。蒸馏后的模型（Distill）得分为 **0.8163**，与教师模型极为接近（仅下降 0.0022），表明多步蒸馏策略在大幅压缩采样步数的同时几乎无损地保留了生成质量。

在关键子指标上，StreamDiT 展现出对一致性和动态性的双重优势：

- **主体一致性（Subject Consistency）**：教师模型达到 0.9622，相比 ReuseDiffuse（0.9501）和 FIFO-Diffusion（0.9412）分别提升 +0.0121 和 +0.0210，验证了缓冲流匹配和混合分块训练对长程一致性的增强作用。
- **动态程度（Dynamic Degree）**：教师模型为 0.5240，蒸馏模型进一步跃升至 **0.7040**，远超 ReuseDiffuse（0.2900）和 FIFO-Diffusion（0.3094）。蒸馏模型在动态性上的反超可能源于蒸馏过程中分类器自由引导的移除，释放了更大的运动幅度。

**人类评估**。Figure 5 展示了 50 个提示词下 8 秒 512p 视频的人类偏好评估结果。StreamDiT 在总体质量、帧一致性、运动完整性、运动自然度四个维度上的胜率均高于所有基线方法，与自动指标的趋势一致。

**推理速度**。蒸馏后的 StreamDiT-4B 在单张 H100 GPU 上实现 512p 分辨率下 **16 FPS** 的实时流式生成（Sec. 5.4）。这一性能得益于将每个分段的多个微步蒸馏为单步，总采样步数降至 8 步。

### 消融实验

**混合分块训练的影响**。Table 3 报告了不同分块大小配置下的 VBench 质量得分。关键发现如下：

- 固定分块大小训练时，chunk size = 1（等价于 Progressive AR Diffusion）得分为 0.8129，chunk size = 16（等价于标准 T2V 无流式）得分为 0.8128，两者接近。
- **混合训练所有分块大小（[1, 2, 4, 8, 16]）取得最佳得分 0.8144**，优于任何单一固定尺寸。这证明混合训练策略使模型能够泛化到不同的流式推理配置，在一致性和质量之间取得更优平衡。

**大模型稳定性验证**。在 30B 参数模型上的消融实验（Table 4，附录）表明，不同配置变化对质量得分的影响极小，验证了所提方法在大规模模型上的稳定性和可扩展性。

### 公平性说明

所有对比方法（ReuseDiffuse、FIFO-Diffusion）均基于相同的 4B MovieGen 基座模型重新实现，共享文本编码器（UL2、ByT5、Meta-CLIP）和时间自编码器（TAE），确保比较的公平性。人类评估采用与 VBench 相同的 50 个提示词，生成 8 秒 512p 视频，从四个维度进行系统比较。

### 失败模式与局限性

尽管 StreamDiT 在流式生成质量和速度上取得了显著进展，仍存在以下不足：

1. **视觉伪影**：4B 参数模型容量有限，部分生成视频存在视觉伪影，整体质量不如更大的 30B 版本。
2. **长期一致性退化**：有效上下文长度受限于基座 T2V 模型的短期记忆窗口。超出窗口的内容可能出现身份不一致或背景突变，缺乏长期记忆机制。Figure 16 展示了通过故事化提示词序列缓解内容重复的策略，但本质问题仍未解决。
3. **分块解码接缝**：由于视频潜变量分块解码，块间可能出现轻微接缝或闪烁伪影，需依赖重叠解码策略（Figure 17）缓解，但无法完全消除。
4. **硬件依赖**：16 FPS 实时性能依赖 H100 GPU，在消费级设备上可能无法达到实时。

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/021_Figure_16.jpg]]
*Figure 16: Sequential storytelling prompts can mitigate repetitive content and enable dynamic contents change*

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/022_Figure_17.jpg]]
*Figure 17: Overlap decoding*

### 重要图表结论

- **Table 1**：StreamDiT 将均匀噪声、对角线噪声、分块去噪等不同分块策略统一到同一框架下，通过参考帧数 K、块大小 c、微步数 s 三个参数灵活配置。
- **Table 2**：教师模型和蒸馏模型在 VBench 上均显著优于现有流式生成方法，蒸馏模型在动态程度上反超教师模型。
- **Figure 5**：人类评估确认 StreamDiT 在全部四个主观质量维度上胜率领先。
- **Table 3**：混合分块训练是取得最优质量的关键设计，验证了训练策略的核心作用。
- **Figure 16**：故事化提示词序列可在一定程度上缓解长期生成中的内容重复问题，但长期一致性仍是开放挑战。

![[assets/figures/papers/paper_list_l2225_https_arxiv_org_abs_2507_03745/figures/007_Table_2.jpg]]
*Table 2: VBench quality metrics of our evaluation. Our models outperform others, and our distilled model is close to our teacher model*

## 定位与知识库关联

### 与现有流式生成方法的关系

StreamDiT 并非孤立地提出一种新的生成范式，而是对现有流式文本到视频生成方法的统一与改进。在流式生成的谱系中，存在两条主要技术路线：**自回归扩散**与**对角线去噪**。

**自回归扩散（Progressive AR Diffusion）** 将视频生成视为逐块预测的过程，每一块在上一个已去噪块的条件下进行去噪。这种范式在 StreamDiT 的分块框架中对应于 chunk size = 1 的极端情况（Table 1）。其优势在于天然的流式能力，但缺陷显著：自回归生成缺乏对未来帧的双向注意力，导致帧间一致性和运动质量弱于全注意力扩散模型。Table 3 的消融实验直接验证了这一点——chunk size = 1 的训练配置在 VBench 上的质量得分（0.8129）低于混合分块训练的配置（0.8144）。

**对角线去噪（Diagonal Denoising）** 的代表工作为 **FIFO-Diffusion**，其核心思想是在一个滑动窗口中为不同帧分配沿对角线分布的噪声等级，通过队列管理实现流式输出。StreamDiT 的缓冲流匹配（Buffered Flow Matching）在概念上与此同源，但关键区别在于：StreamDiT 通过**变时间嵌入（Varying Time Embedding）** 将时间条件从标量扩展为沿帧维度分离的序列，使得模型原生支持每帧不同的噪声等级，而非依赖外部队列调度。这一架构改进使得 StreamDiT 能够统一均匀噪声、对角线噪声和分块去噪等多种方案（Table 1），并在 VBench 上以 0.8185 的质量得分显著超越 FIFO-Diffusion 的 0.7981（Table 2）。

**ReuseDiffuse** 则采用基于预训练扩散模型的迭代去噪策略，在流式生成中复用先前帧的去噪结果。StreamDiT 以相同的基座模型（4B MovieGen）重新实现该方法进行公平对比，在主体一致性（0.9622 vs 0.9501）和动态程度（0.5240 vs 0.2900）上均取得显著提升（Table 2），表明缓冲流匹配框架在保持内容一致性方面具有结构优势。

### 在 DiT 架构谱系中的定位

StreamDiT 的骨干网络继承自 **adaLN DiT**（Peebles & Xie, ICCV 2023），但在两个关键维度上进行了针对性改造：

1. **时间条件的序列化**：标准 DiT 将时间步 $t$ 作为标量条件注入 adaLN 的 scale/shift 调制。StreamDiT 将其替换为沿帧维度可分离的序列 $\tau$，使得同一批次内的不同帧可以接收不同的时间嵌入（Figure 3）。这一改动是缓冲流匹配得以实现的核心——没有变时间嵌入，模型无法同时处理处于不同去噪阶段的帧。

2. **注意力机制的窗口化**：标准 DiT 的全注意力在视频潜变量上的计算复杂度为 $O(N^2)$，其中 $N$ 为帧数乘以空间 token 数。StreamDiT 引入**窗口注意力（Window Attention）**，将 3D latent 划分为规则窗口并在窗口内执行局部自注意，通过窗口移位实现跨窗口信息交互（Figure 4）。这一设计将计算复杂度降至线性，是实时推理（16 FPS）的关键使能技术。

在视频压缩方面，StreamDiT 采用**时间自编码器（TAE）** 进行时间域 4 倍、空间域 8 倍的压缩，潜变量通道数为 8。这与 MovieGen 等主流视频生成模型的压缩策略一致，确保了与现有基座模型的兼容性。

### 适用边界与局限

StreamDiT 的适用边界由其设计选择直接决定：

**模型容量约束**：当前 StreamDiT-4B 的生成质量受限于 4B 的参数规模。部分生成视频存在视觉伪影，整体质量不如更大的 30B 版本。这意味着在追求极致视觉质量的场景下，模型容量仍是瓶颈。

**上下文长度限制**：有效上下文长度受限于基座 T2V 模型的短期记忆窗口。超出该窗口的内容可能出现身份漂移或背景突变，缺乏长期记忆机制。Figure 16 中通过故事化提示词序列部分缓解了内容重复问题，但这属于提示工程层面的补偿，而非模型能力的根本提升。

**分块解码伪影**：由于视频潜变量分块解码，解码后块之间可能出现轻微接缝或闪烁。论文提出了重叠解码策略（Figure 17）作为缓解手段，但未能完全消除该问题。

**硬件依赖**：蒸馏模型的实时性能（16 FPS @ 512p）依赖于 H100 GPU。在消费级 GPU 上可能无法达到实时，限制了方法的普及性。

### 开放问题

1. **长期记忆机制**：如何将状态空间模型（如 Mamba）或外部记忆模块与 StreamDiT 的缓冲流匹配框架结合，以解决身份漂移和长期一致性问题？这需要在不破坏流式推理效率的前提下引入跨块记忆。

2. **接缝消除**：重叠解码之外的更有效方法（如跨块注意力融合、隐空间一致性约束）能否完全消除分块解码带来的接缝/闪烁伪影？

3. **推理加速**：如何进一步降低蒸馏模型的推理延迟，使其在消费级 GPU 上也能实时运行？这可能涉及更激进的蒸馏策略、量化或专用推理算子。

4. **动态分块策略**：混合分块训练中的分块方案是否需要根据视频内容动态调整？例如，高运动场景可能需要更小的 chunk size 以保证运动质量，而静态场景可以使用更大的 chunk size 以提升效率。

5. **高帧率扩展**：该方法能否扩展到高分辨率、高帧率（如 60 FPS）的实时生成？这需要在窗口注意力和缓冲流匹配框架中重新平衡计算复杂度与生成质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/StreamDiT_Real_Time_Streaming_Text_to_Video_Generation.pdf]]
