---
title: "FlowAct-R1: Towards Interactive Humanoid Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: "paperPDFs/arxiv_2026/FlowAct-R1:_Towards_Interactive_Humanoid_Video_Generation.pdf"
project_link: "https://grisoon.github.io/FlowAct-R1/"
code_link: null
aliases:
- FR
- FlowAct-R1
tags:
- arxiv_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过引入分块扩散强制（chunkwise diffusion forcing）策略与自强制（self-forcing）变体，在MMDiT骨干上实现流式自回归生成并抑制误差累积；结合结构化记忆库与记忆修复（Memory Refinement），维持长期一致性；并通过多阶段蒸馏将去噪步骤压缩至3个NFE，以及MLLM驱动动作规划，实现低延迟实时推理和生动的行为...
primary_logic: 将全序列扩散Transformer改造为分块流式架构，利用假因果注意力与自强制训练弥合推理差距，同时通过蒸馏和系统优化达到25fps低延迟，再引入多模态大模型规划动作，使生成的人形视频在无限时长流播中保持身份一致性和行为自然性。
claims:
- FlowAct-R1在用户研究中以GSB（good-same-bad）指标显著优于KlingAvatar 2.0、LiveAvatar和Omnihuman-1.5，在运动自然度、唇音同步、帧结构稳定性和运动丰富性上均获得多数偏好。
- 分块扩散强制和自强制变体可以缓解流式生成中的误差累积，结合记忆细化策略实现长期时序一致性。
- 通过多阶段蒸馏（包括CFG消除、朴素步骤蒸馏、DMD）将推理NFE降至3，并结合系统优化实现480p 25fps实时生成，首个帧延迟仅约1.5秒。
- User study (20 participants, full scene comparison) 上 GSB (good-same-bad) preference rate = FlowAct-R1
---

# FlowAct-R1: Towards Interactive Humanoid Video Generation

> [!tip] 核心洞察
> 将全序列扩散Transformer改造为分块流式架构，利用假因果注意力与自强制训练弥合推理差距，同时通过蒸馏和系统优化达到25fps低延迟，再引入多模态大模型规划动作，使生成的人形视频在无限时长流播中保持身份一致性和行为自然性。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlowAct-R1: 面向交互式人形视频生成 |
| 英文题名 | FlowAct-R1: Towards Interactive Humanoid Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10103) · [Project](https://grisoon.github.io/FlowAct-R1/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | FlowAct-R1 |
| Dataset | User study, Real-time performance |

> [!tip] 效果简介
> - User study (20 participants, full scene comparison) 上，GSB (good-same-bad) preference rate FlowAct-R1 vs KlingAvatar 2.0 (FlowAct-R1 receives majority of good votes (see Fig.3, left panel))；GSB (good-same-bad) preference rate FlowAct-R1 vs LiveAvatar (FlowAct-R1 receives majority of good votes (see Fig.3, middle panel))；GSB (good-same-bad) preference rate FlowAct-R1 vs Omnihuman-1.5 (FlowAct-R1 receives majority of good votes (see Fig.3, right panel))。
> - Real-time performance 上，FPS / Time-to-First-Frame (TTFF) 25fps @ 480p / ~1.5s TTFF vs Other methods do not achieve comparable real-time streaming at this resolution (FlowAct-R1 achieves stable real-time streaming; competitors lack such efficienc...)。

## 概要

**FlowAct-R1** 面向交互式人形视频生成的核心瓶颈：现有方法难以在流式生成、低延迟交互与全身行为的高保真生动性之间取得平衡，普遍存在视觉质量与实时响应之间的权衡，且长视频的时序一致性难以维持。

**核心思路**是将全序列扩散Transformer改造为分块流式架构。具体而言，FlowAct-R1 在MMDiT骨干上引入**分块扩散强制（chunkwise diffusion forcing）**策略与**自强制（self-forcing）**变体，实现流式自回归生成并抑制误差累积；配合**结构化记忆库**与**记忆修复（Memory Refinement）**维持长期一致性；通过**多阶段蒸馏**将去噪步骤压缩至3个NFE，并结合系统优化达到480p下25fps的实时生成，首帧延迟仅约1.5秒；同时集成**多模态大语言模型（MLLM）**进行动作规划，使生成的人形视频在无限时长流播中保持身份一致性和行为自然性。

**方法定位**：FlowAct-R1相较于现有SOTA方法（如**KlingAvatar 2.0**、**LiveAvatar**、**Omnihuman-1.5**）的核心差异在于同时具备流式生成、实时推理、全身可控、强泛化性与生动行为过渡的能力（见Table 1）。其技术路线可视为“分块自回归扩散 + 记忆增强 + 蒸馏加速 + MLLM规划”的融合方案。

**主要结果**：
- 用户研究（20名参与者，GSB指标）显示，FlowAct-R1在运动自然度、唇音同步、帧结构稳定性和运动丰富性上均获得多数偏好，显著优于KlingAvatar 2.0、LiveAvatar和Omnihuman-1.5（见Figure 3）。
- 系统性能方面，FlowAct-R1在480p分辨率下实现25fps稳定实时生成，首帧延迟约1.5秒，竞争对手尚无法达到同等实时流式效率。

**证据强度**：核心性能指标（FPS/TTFF）和用户偏好结果均有明确的定量支撑，置信度较高；消融实验（记忆修复、自强制训练、多阶段蒸馏）进一步验证了各组件的有效性，但部分消融的详细量化数据需结合原文确认。



实时交互式人形视频生成旨在根据音频、文本等驱动信号，流式合成具有自然行为的高保真虚拟人物视频，在数字人直播、虚拟助手、在线教育等场景中需求迫切。该任务的核心瓶颈在于：**现有方法难以同时满足流式生成、低延迟交互和全身行为的高保真生动性**，普遍存在视觉质量与实时响应之间的根本性权衡，且长视频的时序一致性难以维持。

早期工作如 **Neural Voice Puppetry**（Thies et al., ECCV 2020）仅聚焦于音频驱动的面部重现，缺乏全身控制能力。**INFP**（Zhu et al., arXiv 2024）虽支持流式交互式头部生成，但同样局限于面部区域。近期涌现的全身人形视频生成方法在质量上取得显著进展，却牺牲了实时性：**Omnihuman-1.5**（Jiang et al., arXiv 2025）仅能生成最长30秒的非流式视频；**KlingAvatar 2.0**（Kling Team et al., arXiv 2025）将时长扩展至5分钟，但仍为离线全序列生成范式；**LiveAvatar**（Huang et al., arXiv 2025）首次尝试实时流式音频驱动人形生成，但在运动自然度、唇音同步精度和帧结构稳定性方面仍有明显不足。

上述方法暴露了三个结构性缺口：

1. **生成范式的局限**：全序列扩散模型一次性生成整个片段，无法支持无限时长的流式输出，且推理成本高昂。
2. **训练-推理不一致**：自回归流式生成中，推理阶段使用模型自身输出作为后续上下文，而训练阶段通常依赖真实潜变量，这种差异导致误差逐块累积，破坏长期一致性。
3. **行为规划缺失**：现有方法缺乏对人物动作的显式高层规划，难以在长时间流播中维持行为的自然过渡和生动性。

本文提出 **FlowAct-R1**，一个面向实时交互式人形视频生成的统一框架。其核心动机在于：通过**分块扩散强制**策略将全序列扩散Transformer改造为流式自回归架构，利用**自强制训练**弥合推理差距，同时引入**多模态大语言模型驱动动作规划**和**多阶段蒸馏**，在480p分辨率下实现25fps稳定实时生成（首帧延迟约1.5秒），并维持无限时长流播中的身份一致性与行为自然性。



## 核心方法与创新机理

FlowAct-R1 的核心创新在于通过**分块扩散强制（chunkwise diffusion forcing）** 策略与配套的**自强制（self-forcing）变体**，将全序列扩散Transformer改造为支持无限时长流式生成的自回归架构，从而突破现有方法在实时交互与视觉质量之间的瓶颈。该创新可分解为以下关键维度：

### 1. 从全序列扩散到分块自回归流式生成

现有全身人形视频生成方法（如 **Omnihuman-1.5** (Jiang et al., arXiv 2025) 和 **KlingAvatar 2.0** (Kling Team et al., arXiv 2025)）均采用全序列扩散范式，需一次性生成完整视频片段，无法支持无限时长的实时流播。FlowAct-R1 在 MMDiT 骨干上引入分块扩散强制策略，将视频生成转化为逐块自回归过程：每个去噪块（chunk）的输出潜变量作为下一块的上下文输入，形成持续的生成流。这一范式转换使得模型天然支持无限长度生成，同时将推理延迟从“等待全片”压缩至块级粒度。

### 2. 自强制训练弥合推理差距

流式自回归生成的核心挑战在于误差累积——训练时模型以真实潜变量（ground truth latents）作为历史记忆，推理时却只能使用自己先前生成的含噪潜变量，这种训练-推理不一致会随时间放大伪影。FlowAct-R1 设计了**Self-Forcing++** 变体：在训练过程中，以一定概率用中间模型自身生成的含噪潜变量替换真实潜变量作为记忆输入，使模型在训练阶段即暴露于推理时的误差分布。这一机制直接对齐了训练与推理的记忆条件，从根源上抑制了流式生成中的累积漂移。

### 3. 结构化记忆库与记忆修复

为维持长期流播中的身份一致性和运动连贯性，FlowAct-R1 构建了三级结构化记忆库：
- **参考帧（Reference Latent）**：提供身份锚定；
- **长期记忆队列（Long-term Memory Queue）**：存储最多3个已去噪块，提供中程时序上下文；
- **短期记忆潜变量（Short-term Memory Latent）**：承载最近帧的细粒度运动状态。

在此基础上，**记忆修复（Memory Refinement）** 策略定期对短期记忆帧执行加噪-去噪修复操作，主动校正流式累积伪影，避免运动质量随时间退化。这一机制是维持无限时长生成中运动流畅性的关键。

### 4. 多阶段蒸馏实现3 NFE实时推理

标准扩散模型需要数十步去噪，无法满足实时交互需求。FlowAct-R1 通过三阶段蒸馏将推理压缩至**3个NFE**（chunk-size=3, 无CFG）：
- **CFG消除**：注入辅助CFG嵌入层，将多尺度引导输出蒸馏至单一模型，消除双次推理开销；
- **朴素步骤蒸馏**：压缩去噪步数；
- **DMD（分布匹配蒸馏）**：进一步对齐少步采样与多步采样的输出分布。

配合FP8量化、算子融合和帧级混合并行等系统优化，最终在480p分辨率下实现**25fps稳定流播**，首帧延迟仅约1.5秒。这是目前唯一同时满足实时性、全身生成和无限时长的方案。

### 5. MLLM驱动的动作规划

现有方法缺乏对行为过渡的显式规划，导致长时间生成中动作可能趋于单调或与音频语境脱节。FlowAct-R1 集成多模态大语言模型（MLLM），根据最新音频片段和参考图像定期预测后续合理动作，引导生成过程中的行为过渡，使流式视频在长时间跨度内保持生动性和语义一致性。

### 创新总结

上述创新共同构成了一条从“离线全序列扩散”到“在线流式自回归扩散”的完整技术路线，其核心洞察在于：**通过分块扩散强制与自强制训练的配合，将扩散模型的生成质量优势与自回归模型的流式能力统一，再通过蒸馏和系统优化将推理成本压缩至实时可用的量级**。这一方案在方法谱系中填补了“实时流式全身人形视频生成”的空白——Table 1 的系统对比显示，FlowAct-R1 是唯一同时具备流式生成、实时推理、全身控制、强泛化性和生动行为过渡能力的框架。



FlowAct-R1 的整体框架围绕“分块自回归扩散 + 结构化记忆 + 多阶段蒸馏”三条主线组织，将原本面向全序列生成的扩散 Transformer 改造为支持无限时长流式推理的实时交互系统。框架分为训练与推理两大阶段（图2），其核心瓶颈在于：**流式生成要求模型在仅看到过去帧的条件下预测未来，而标准扩散模型训练时却依赖完整序列的双向注意力**。FlowAct-R1 通过假因果注意力（pseudo-causal attention）和自强制训练弥合这一差距，同时引入记忆修复机制抑制长时流播中的误差累积。

### 训练阶段

训练阶段包含三个递进环节：

1. **自回归适配（Autoregressive Adaptation）**  
   以预训练的 MMDiT 骨干为基础，将全注意力替换为假因果注意力，使模型只能关注当前及过去的帧。在此约束下，采用**分块扩散强制（chunkwise diffusion forcing）**策略进行训练：将视频序列切分为固定大小的块，每个块的去噪过程以前一块的真实潜变量作为条件。为进一步缩小训练-推理差异，设计了**自强制变体（Self-Forcing++）**——以一定概率选择中间模型自身生成的含噪潜变量替代真实潜变量作为记忆输入，使模型在训练中就暴露于推理时可能出现的记忆误差。

2. **音频-运动联合微调（Joint Audio-Motion Finetuning）**  
   在自回归适配的基础上，引入 Whisper 编码器将 16kHz 音频压缩为与视频帧率对齐的声学令牌，通过 IP-Adapter 风格的交叉注意力注入 MMDiT。此阶段同时优化唇音同步与身体运动，使生成的人形行为与语音节奏协调。

3. **多阶段扩散蒸馏（Multi-Stage Distillation）**  
   为解决扩散模型推理步数过多的问题，采用三级蒸馏流水线：首先通过注入辅助 CFG 嵌入层并蒸馏多尺度引导输出，**消除 CFG 的额外推理开销**；随后进行朴素步骤蒸馏；最后应用分布匹配蒸馏（DMD），将去噪过程压缩至 **3 个 NFE**（chunk-size=3, micro-step=1, 无 CFG），实现约 8 倍加速。

### 推理阶段

推理阶段以流式方式运行，核心组件为**结构化记忆库（Structured Memory Bank）**，包含三类记忆：

- **参考帧潜变量（Reference Latent）**：提供身份锚定，贯穿整个生成过程。
- **长期记忆队列（Long-term Memory Queue）**：保存最近若干个已完成去噪的块，提供跨块时序上下文（最多 3 个块）。
- **短期记忆潜变量（Short-term Memory Latent）**：当前块去噪时直接参与注意力计算的近邻帧。

生成过程以分块自回归方式推进：每轮取短期记忆与长期记忆作为条件，对当前块执行 3 步去噪，输出块的前若干帧追加到长期记忆队列，同时更新短期记忆。为抑制流式生成中不可避免的伪影累积，定期对短期记忆帧执行**记忆修复（Memory Refinement）**——注入噪声后重新去噪，相当于对流式记忆进行“纠偏”。

此外，系统集成了**多模态大语言模型（MLLM）作为动作规划器**：根据最新音频片段和参考图像，定期预测后续合理动作，生成引导文本嵌入，使生成的人形行为过渡更加生动自然。

### 系统优化

在工程层面，FlowAct-R1 结合 FP8 量化、高频算子融合以及帧级混合并行策略，进一步降低延迟与通信开销。最终，系统在 480p 分辨率下达到 **25fps 稳定流式生成，首帧延迟（TTFF）仅约 1.5 秒**，满足实时交互需求。

> **需注意**：关于 MLLM 动作规划的具体实现细节（如预测频率、动作空间定义）以及记忆修复的触发策略，原文未提供充分的定量消融证据，相关性能归因需结合补充材料进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2601_10103/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the FlowAct-R1 framework. It consists of training and inference stages: training integrates converting base full-attention DiT to streaming AR model via autoregressive adaptation, joint audio-motion finetuning for better lip-sync and body motion, multi-stage diffusion distillation; inference adopts a structured memory bank (Reference/Long/Short-term Memory, Denoising Stream) with chunkwise autoregressive generation and memory refinement. Complemented by system-level optimizations, it achieves 25fps real-time 480p video generation (TTFF 1.5s) with vivid behavioral transitions*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2601_10103/figures/001_Figure_1.jpg]]
*Figure 1: We present FlowAct-R1, a novel framework that enables lifelike, responsive, and high-fidelity humanoid video generation for seamless real-time interaction*



### 2.1 分块扩散强制（Chunkwise Diffusion Forcing）

FlowAct-R1 的核心生成范式是将全序列扩散 Transformer 改造为**分块自回归流式架构**。传统扩散模型一次性生成整个视频片段，难以支持无限时长流播；而朴素的自回归扩展会因误差累积导致时序质量崩溃。

该方法在 MMDiT 骨干上引入**分块扩散强制**策略：将视频潜变量序列按时间切分为固定大小的块（chunk），每一块的去噪过程以前一块的已解码潜变量为条件。具体而言，第 $t$ 个块 $\mathbf{z}_t$ 的生成依赖于前一块 $\mathbf{z}_{t-1}$ 的干净潜变量，形成条件扩散过程：

$$p_\theta(\mathbf{z}_t | \mathbf{z}_{t-1}, \mathbf{c})$$

其中 $\mathbf{c}$ 为多模态条件（文本、音频等）。这种设计将全序列扩散转化为流式自回归生成，使模型能够逐块输出视频帧，理论上支持无限时长。

**训练-推理差距问题**：训练时，条件块 $\mathbf{z}_{t-1}$ 来自真实数据（ground truth），而推理时 $\mathbf{z}_{t-1}$ 来自模型自身的生成结果，其中包含扩散去噪残留的误差。这种分布偏移会在长序列中逐步放大。

### 2.2 自强制变体（Self-Forcing++）

为弥合上述训练-推理差距，FlowAct-R1 提出**自强制变体 Self-Forcing++**。其核心思想是：训练时以一定概率将条件块 $\mathbf{z}_{t-1}$ 从真实潜变量替换为**中间模型自身生成的含噪潜变量**，从而模拟推理时的记忆误差分布。

具体操作流程：
1. 在训练的前向传播中，对前一块的潜变量执行部分去噪（使用当前模型参数），得到含噪版本 $\hat{\mathbf{z}}_{t-1}$；
2. 以概率 $p$ 选择 $\hat{\mathbf{z}}_{t-1}$ 作为当前块的条件输入，以概率 $1-p$ 使用真实潜变量；
3. 当前块的去噪损失同时反向传播到当前块和前一条件块的生成路径，使模型学会在含噪条件下仍能稳定去噪。

这种训练策略使模型在推理时面对自身累积误差时具有更强的鲁棒性，有效抑制了流式生成中的误差放大效应。

### 2.3 结构化记忆库与记忆修复

为维持长视频的时序一致性和身份保真度，FlowAct-R1 设计了**结构化记忆库**，包含三个层次：

- **参考帧（Reference Latent）**：存储身份锚定帧的潜变量，提供全局外观约束；
- **长期记忆队列（Long-term Memory Queue）**：保存最近 $K$ 个已解码块的潜变量（$K \leq 3$），为当前块提供中程时序上下文；
- **短期记忆潜变量（Short-term Memory Latent）**：当前块去噪过程中的中间状态，用于帧间平滑过渡。

**记忆修复（Memory Refinement）** 是维持长期一致性的关键机制。在流式生成过程中，短期记忆帧会逐渐累积微小伪影。记忆修复定期对短期记忆帧执行**加噪-去噪修复操作**：向短期记忆潜变量注入适量噪声，再通过轻量去噪步骤恢复，从而消除累积的失真。这一操作类似于扩散模型中的“回退-重采样”，但仅在记忆层面局部执行，计算开销极小。

### 2.4 多阶段蒸馏

为实现实时推理，FlowAct-R1 采用**三阶段蒸馏流水线**将去噪步数压缩至 3 NFE（chunk-size=3, micro-step=1, 无 CFG），达到约 8 倍加速：

**阶段一：CFG 消除**。标准扩散模型依赖无分类器引导（CFG）提升生成质量，但 CFG 需要双倍推理计算（同时评估条件与无条件分支）。FlowAct-R1 注入一个辅助 CFG 嵌入层，将多种引导尺度下的输出蒸馏到单一统一模型中，消除推理时的双重评估开销。

**阶段二：朴素步骤蒸馏**。以教师模型（全步数）的输出来监督学生模型（少步数），直接减少去噪步数。

**阶段三：分布匹配蒸馏（DMD）**。在步骤蒸馏基础上，进一步通过分布匹配损失使学生模型生成的分布逼近教师模型，弥补少步采样带来的质量损失。DMD 损失定义为：

$$\mathcal{L}_{\text{DMD}} = D_{KL}(q_{\text{student}}(\mathbf{z}) \| p_{\text{teacher}}(\mathbf{z}))$$

其中 $q_{\text{student}}$ 为学生模型生成分布，$p_{\text{teacher}}$ 为教师模型分布。最终模型在 3 NFE 下保持与高步数模型相当的视觉质量。

### 2.5 MLLM 驱动动作规划

为增强生成人形的行为生动性和过渡自然性，FlowAct-R1 集成**多模态大语言模型（MLLM）** 进行动作规划。MLLM 定期（例如每 $N$ 秒）接收最新音频片段和参考图像，预测后续合理动作序列，引导行为过渡。动作规划输出以文本形式注入条件编码器，与音频特征共同约束生成过程，使模型能够根据对话语境产生自然的手势、表情和身体动作变化。

### 2.6 系统优化

在模型层面之外，FlowAct-R1 引入多项系统级优化以实现 480p 25fps 实时流播：

- **FP8 量化**：将模型权重和激活量化为 FP8 精度，降低显存带宽压力；
- **算子融合**：将频繁调用的操作（如注意力计算中的矩阵乘法与缩放）融合为单一 CUDA 内核，减少内核启动开销；
- **帧级混合并行**：在推理时对视频帧维度进行混合并行划分，平衡计算负载并降低跨设备通信开销。

这些优化与蒸馏模型协同，将首个帧延迟（TTFF）压缩至约 1.5 秒，后续帧以 25fps 稳定输出。

> **注意**：本文未提供具体公式的完整 LaTeX 源码，上述公式为基于方法描述的逻辑还原，需以原论文正式版本为准进行验证。



## 实验与关键发现

### 实时性能与系统效率

FlowAct-R1 的核心设计目标之一是低延迟流式推理，而非仅追求离线生成质量。通过多阶段蒸馏，模型将去噪过程压缩至仅 **3 个 NFE**（chunk-size=3, micro-step=1, 无 CFG），实现约 **8 倍加速**。在系统层面，结合 FP8 量化、算子融合以及帧级混合并行策略，最终在 480p 分辨率下达到稳定的 **25 fps** 实时生成，首个帧延迟（TTFF）仅约 **1.5 秒**（见 Abstract 与 Figure 2）。这一延迟指标使得系统能够支持实际的实时交互场景，而非仅生成预录制片段。

### 用户偏好研究

为评估生成质量，作者开展了包含 20 名参与者的用户研究，采用 GSB（good-same-bad）偏好投票，将 FlowAct-R1 与三个代表性基线进行全场景对比：

- **vs. KlingAvatar 2.0**：FlowAct-R1 获得多数 “good” 投票（Figure 3 左）。
- **vs. LiveAvatar**：FlowAct-R1 获得多数 “good” 投票（Figure 3 中）。
- **vs. Omnihuman-1.5**：FlowAct-R1 获得多数 “good” 投票（Figure 3 右）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2601_10103/figures/004_Figure_3.jpg]]
*Figure 3: Comparisons with KlingAvatar 2.0 [31], LiveAvatar [16], and Omnihuman-1.5 [18] via a user study using the GSB (good-same-bad) metric. The orange segments indicate the percentage of user votes favoring FlowAct-R1 over other methods. Video demos are shown in our project page*

橙色段表示用户偏好 FlowAct-R1 的比例。论文指出，FlowAct-R1 在运动自然度、唇音同步、帧结构稳定性和运动丰富性等维度上均表现出优势（见 Figure 3 及其说明）。需注意，为保证公平性，各基线按其最大支持时长运行：Omnihuman-1.5 限制为 30 秒，KlingAvatar 2.0 限制为 5 分钟，LiveAvatar 和 FlowAct-R1 使用完整音频。

### 消融实验

论文报告了三项关键消融，但原文未提供量化数值，仅给出定性结论，建议读者在审阅时注意验证具体数据。

**记忆修复（Memory Refinement）**。消融表明，移除记忆修复策略后，长期流式生成中短期记忆帧会累积可见伪影，导致运动流畅性下降。记忆修复通过定期对短期记忆执行加噪-去噪修复操作，有效校正了流式累积的失真（置信度 0.85）。

**自强制训练（Self-Forcing++）**。标准训练使用真实潜变量作为记忆输入，而推理时只能使用模型自身生成的含噪潜变量，这种训练-推理差距是流式自回归生成中误差累积的主要来源。Self-Forcing++ 在训练中以概率方式选择中间模型生成的含噪潜变量替代真实潜变量，模拟推理时的记忆误差，从而弥合了这一差距，减少了长序列中的累积漂移（置信度 0.85）。

**多阶段蒸馏**。蒸馏管线包含三步：CFG 消除（注入辅助 CFG 嵌入层，将多尺度引导输出蒸馏至单一模型）、朴素步骤蒸馏、以及 DMD 蒸馏。消融显示，该管线在将推理 NFE 压缩至 3 的同时，保持了合成质量，实现了约 8 倍加速（置信度 0.9）。

### 整体能力对比

Table 1 给出了与现有 SOTA 人形视频生成方法的整体能力对比。FlowAct-R1 是唯一同时满足以下所有维度的方法：流式生成、实时推理、全身可控、强泛化性、以及生动行为表现。其他方法在至少一个维度上存在明显短板——例如 LiveAvatar 支持实时流式但行为生动性受限，Omnihuman-1.5 和 KlingAvatar 2.0 生成质量较高但不支持流式实时推理。Table 1 的具体行项数据需参阅原文。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2601_10103/figures/002_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art humanoid video generation methods. FlowAct-R1 simultaneously achieves streaming, real-time generation with fully controllable, generalization, and lifelike video generation capacity*

### 局限与风险

论文明确指出的主要局限并非技术瓶颈，而是伦理风险：该技术可能被滥用以制造欺骗性或有害内容。作者声明将通过访问控制和负责任部署来缓解这一风险。技术层面的失败模式（如极端姿态下的身份漂移、复杂音频场景下的唇音失配等）在已有材料中未展开讨论，需要手动验证。



## 定位与知识库关联

FlowAct-R1 处于人形视频生成从“离线全序列合成”向“实时流式交互”跃迁的关键节点。其核心贡献并非单一模块的创新，而是通过**分块扩散强制（chunkwise diffusion forcing）** 将扩散Transformer改造为流式自回归架构，同时以多阶段蒸馏和系统优化将推理成本压缩至可实时运行的量级，从而在**流式、实时、全身控制、泛化性与生动性**五个维度上首次实现全面覆盖（见 Table 1）。

### 与基线方法的关系与适用边界

**面部/头部流式方法**：早期工作如 **Neural Voice Puppetry**（Thies et al., ECCV 2020）和 **INFP**（Zhu et al., arXiv 2024）已实现音频驱动的流式面部或头部生成，但其控制范围局限于面部区域，无法生成全身动作。FlowAct-R1 将流式能力扩展至全身人形，并引入 MLLM 驱动的动作规划，使行为过渡具有上下文相关性，而非仅依赖音频信号。

**离线全身方法**：**Omnihuman-1.5**（Jiang et al., arXiv 2025）和 **KlingAvatar 2.0**（Kling Team et al., arXiv 2025）在全身人形生成质量上表现突出，但均采用全序列扩散范式，需要一次性生成整个视频片段（最长分别为30秒和5分钟），无法支持无限时长流播。FlowAct-R1 通过分块自回归生成突破了这一时长限制，同时利用结构化记忆库（参考帧、长期记忆队列、短期记忆潜变量）和记忆修复策略维持长期时序一致性。用户研究（Figure 3）显示，FlowAct-R1 在运动自然度、唇音同步和帧结构稳定性上均获得显著偏好。

**实时流式全身方法**：**LiveAvatar**（Huang et al., arXiv 2025）是当前最接近的竞品，同样支持实时音频驱动的全身生成。但 FlowAct-R1 在用户研究的 GSB 指标上仍获得多数偏好（Figure 3 中面板），其优势可能源于自强制训练弥合的训练-推理差距，以及 MLLM 动作规划带来的更丰富的行为表现。

### 技术瓶颈与因果机制

FlowAct-R1 解决的核心瓶颈是**流式扩散生成中的误差累积**。在全序列扩散中，模型可以访问完整上下文；而在分块自回归推理中，每个块的生成依赖于前序块的潜变量，训练时使用的真实潜变量（ground truth latents）与推理时模型自身生成的含噪潜变量之间存在分布偏移。FlowAct-R1 的**自强制变体（Self-Forcing++）** 通过在训练中概率性地用中间模型生成的含噪潜变量替换真实潜变量，模拟推理时的记忆误差，从而弥合这一差距。消融实验表明该策略有效减少了累积误差。

另一个关键机制是**记忆修复（Memory Refinement）**：在长期流式生成中，短期记忆潜变量会逐渐累积伪影。FlowAct-R1 定期对短期记忆帧执行加噪-去噪修复操作，校正累积的失真，维持运动流畅性。消融实验证实该策略对长期生成质量至关重要。

### 推理效率的实现路径

FlowAct-R1 将去噪步骤压缩至 **3 NFE**（chunk-size=3, micro-step=1, 无 CFG），实现约 **8倍加速**。这一效率来自多阶段蒸馏管线：
1. **CFG 消除**：注入辅助 CFG 嵌入层，将不同引导尺度的输出蒸馏至单一模型，消除推理时的双倍计算开销；
2. **朴素步骤蒸馏**：减少去噪步数；
3. **DMD（分布匹配蒸馏）**：进一步压缩步数并保持生成质量。

结合 FP8 量化、算子融合和帧级混合并行等系统优化，最终在 480p 分辨率下实现稳定的 **25fps** 实时生成，首帧延迟仅约 **1.5秒**。

### 局限与开放问题

论文明确指出的局限主要是**滥用风险**：高保真实时人形生成可能被用于制造欺骗性或有害内容。作者承诺通过访问控制和负责任部署来缓解，但未提供具体技术方案（如不可见水印或检测机制），这一点需要在实际部署中手动验证。

从技术角度看，以下开放问题值得关注：
- **极端长时一致性**：虽然记忆修复策略缓解了累积伪影，但在数小时级别的连续流播中，身份漂移和运动模式退化是否可控尚无定量评估。
- **多模态动作规划的鲁棒性**：MLLM 动作规划依赖音频和参考图像推断后续行为，在音频歧义或场景突变时的鲁棒性未经验证。
- **更高分辨率的实时性**：当前 480p 25fps 的指标能否线性扩展至 720p 或 1080p 尚不明确，系统优化的瓶颈分析缺失。



## 原文 PDF

![[paperPDFs/arxiv_2026/FlowAct-R1:_Towards_Interactive_Humanoid_Video_Generation.pdf]]
