---
title: "StreamAvatar: Streaming Diffusion Models for Real-Time Interactive Human Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/StreamAvatar_Streaming_Diffusion_Models_for_Real_Time_Interactive_Human_Avatars.pdf
project_link: "https://streamavatar.github.io"
code_link: null
aliases:
- StreamAvatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 通过将双向 DiT 改造为块因果 DiT 并进行自回归蒸馏，将去噪步数从数十步降至 3 步，从而在保持生成质量的同时实现实时流式生成；同时引入分离的音频注意力和音频掩膜，使模型能够根据说话/聆听状态生成对应的自然行为和过渡。
primary_logic: 高质量但速度较慢的非因果扩散模型可以通过两阶段框架（自回归蒸馏 + 对抗性增强）高效适配为实时流式生成器，其中参考汇 (Reference Sink)、参考锚定位置重新编码 (RAPR) 和一致性感知判别器是解决长视频一致性和身份漂移的关键，而基于音频掩膜的分离式说话/聆听模块则赋予了模型自然的交互对话能力。
claims:
- 两阶段自回归适配框架能够将双向扩散模型转换为实时流式模型。
- 引入的 Reference Sink 和 Reference-Anchored Positional Re-encoding (RAPR) 解决了长视频生成中的身份漂移和 out-of-distribution 问题。
- 消融实验显示，逐步加入各组件后，FID、FVD 及稳定性指标显著改善。
- Short dataset (50 pairs, 5s audio) 上 FID = 74.21
---

# StreamAvatar: Streaming Diffusion Models for Real-Time Interactive Human Avatars

> [!tip] 核心洞察
> 高质量但速度较慢的非因果扩散模型可以通过两阶段框架（自回归蒸馏 + 对抗性增强）高效适配为实时流式生成器，其中参考汇 (Reference Sink)、参考锚定位置重新编码 (RAPR) 和一致性感知判别器是解决长视频一致性和身份漂移的关键，而基于音频掩膜的分离式说话/聆听模块则赋予了模型自然的交互对话能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | StreamAvatar：面向实时交互式人类化身的流式扩散模型 |
| 英文题名 | StreamAvatar: Streaming Diffusion Models for Real-Time Interactive Human Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22065) · [Project](https://streamavatar.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | StreamAvatar |
| Dataset | Short dataset, Long dataset, Interactive dataset, EMTD |

> [!tip] 效果简介
> - Short dataset (50 pairs, 5s audio) 上，FID 74.21 vs 75.20 (StableAvatar) (0.99 lower (improvement))。
> - Short dataset 上，FVD 707.34 vs 557.46 (HY-Avatar, lowest among baselines) (149.88 higher (worse than best, but competitive overall))。
> - Long dataset (25 pairs, 20s audio) 上，Sync-C 6.64 vs 6.47 (OmniAvatar) (0.17 higher (improvement))。

## 概要

高质量人类化身视频生成在虚拟现实、远程协作、数字人等应用中需求迫切，但现有扩散式方法面临两个核心瓶颈：**实时性不足**与**交互能力缺失**。一方面，主流方案采用非因果的双向注意力机制，且需要数十步迭代去噪，计算开销极大，无法实现流式生成；另一方面，这些方法通常只处理说话状态，忽略聆听行为，导致化身在对话中表现僵硬、缺乏自然过渡。StreamAvatar 正是针对上述瓶颈提出的一套两阶段自回归适配与加速框架。

**核心思路**是将高质量但速度较慢的双向扩散模型改造为块因果架构，并通过自回归蒸馏将去噪步数从 50+ 步压缩至 3 步，从而在保持生成质量的同时达成实时流式输出。在此基础上，引入三项关键技术——Reference Sink、Reference-Anchored Positional Re-encoding (RAPR) 以及 Consistency-Aware Discriminator——分别解决长视频生成中的身份漂移、训练-推理位置编码失配和时序一致性退化问题。同时，通过分离的说话/聆听音频注意力模块和音频掩膜机制，模型首次具备根据对话角色生成自然聆听行为与说话-聆听过渡的能力。

**方法定位**：StreamAvatar 属于基于扩散模型的实时交互式人类化身生成方法，其技术路线融合了自回归蒸馏、对抗性精炼和音频条件注入。相较于 StableAvatar、HY-Avatar、Hallo3 等仅支持说话生成的方法，StreamAvatar 在交互性上形成代差；相较于 MIDAS、X-Streamer 等流式交互方法，StreamAvatar 在视觉质量和行为自然度上具有显著优势。

**主要结果**：在短时说话数据集上，StreamAvatar 的 FID 达到 74.21，优于 StableAvatar 的 75.20；在长视频数据集上，Sync-C 达到 6.64，超过 OmniAvatar 的 6.47。交互式生成方面，聆听行为关键点速度 (LBKV) 和聆听头部关键点速度 (LHKV) 分别达到 15.88 和 16.24，远高于仅支持说话的基线（6.05 和 4.53），表明模型能够生成丰富的聆听动作。消融实验证实，逐步加入 Reference Sink、RAPR 和一致性感知判别器后，FID 从 96.58 持续下降至 74.21，各组件贡献明确。用户偏好研究进一步验证了 StreamAvatar 在同步性、画质、动态多样性、身份一致性和时序连续性上的全面领先。

实时、高保真且具备自然交互能力的人类化身生成，是虚拟会议、数字人助手、游戏和社交应用中的核心需求。理想的化身系统应当能够以流式方式持续生成视频帧，同时根据用户或智能体的语音输入，在“说话”与“聆听”两种状态之间自然切换，产生与之匹配的面部表情和肢体动作。

然而，现有方法在两个关键维度上存在明显缺口。第一，**实时流式生成能力不足**。当前主流的扩散式人类化身生成方法（如 **StableAvatar**、**OmniAvatar**、**HunyuanVideo-Avatar (HY-Avatar)**、**Hallo3**、**EchoMimicV3**）通常基于双向自注意力机制，在生成时需要对整个时间窗口进行非因果建模，且迭代去噪步数往往高达数十步，导致推理延迟远高于实时流式的要求。这使得此类方法难以直接应用于需要即时响应的交互场景。第二，**交互自然性缺失**。现有工作几乎全部聚焦于“说话”状态的生成，忽略了对话中同样重要的“聆听”行为。当用户停止说话时，化身往往陷入不自然的静止状态，无法根据对方语音产生点头、微表情等聆听反馈，严重损害了交互的真实感。

从更根本的层面看，上述瓶颈的实质是：**高质量但计算密集的双向扩散模型与实时流式、交互式生成需求之间的矛盾**。扩散模型通过迭代去噪获得优异的视觉质量，但其推理代价与去噪步数成正比；同时，双向注意力虽然有利于全局一致性，却天然排斥流式推理所必需的因果约束。因此，如何在不牺牲生成质量的前提下，将双向扩散模型改造为支持实时流式推理的自回归生成器，并赋予其说话/聆听双模态的交互能力，构成了本文的核心动机。

针对这一挑战，本文提出 **StreamAvatar**，一个两阶段自回归适配与加速框架。其核心思路是：通过自回归蒸馏将双向扩散教师模型压缩为块因果的学生模型，将去噪步数从数十步降至 3 步；同时引入参考汇 (Reference Sink)、参考锚定位置重新编码 (RAPR) 和一致性感知判别器三项关键技术，解决长视频流式生成中的身份漂移和分布外退化问题。在此基础上，通过分离的说话/聆听音频注意力模块和音频掩膜机制，使模型能够根据对话状态生成对应的自然行为与过渡，从而实现真正意义上的实时交互式人类化身。

## 核心方法与创新机理

StreamAvatar 的核心创新在于将高质量但计算开销极大的双向扩散式人类化身生成模型，改造为**实时、流式、交互式**的生成器。这一改造并非简单的工程加速，而是通过一个**两阶段自回归适配与加速框架**，系统性地解决了非因果扩散模型在流式场景下的三个根本性瓶颈：注意力机制的非因果性、长视频生成中的身份漂移，以及交互对话中聆听行为的缺失。

### 从双向到块因果的注意力重构

现有扩散式化身生成方法（如 StableAvatar、HunyuanVideo-Avatar 等）采用**双向自注意力**，模型在生成时需要访问整个生成窗口内的所有帧，无法实现逐帧流式输出。StreamAvatar 将底层 DiT 的注意力机制从双向自注意力改造为**块因果注意力（block-wise causal attention）**，以 chunk 大小 $C=3$ 进行分块，块内保持双向注意力以保留局部时序一致性，块间则强制因果注意力，使得模型可以基于已生成的帧自回归地预测后续帧。

具体而言，第 $i$ 个 chunk 的起始帧和结束帧索引定义为：
$$s_i = (i-1) \cdot C + 1, \quad e_i = i \cdot C$$

配合**滚动 KV 缓存**，模型在推理时仅需维护有限长度的历史键值对，从而将计算复杂度从 $O(T^2)$ 降至与序列长度解耦的常量级别，为实时流式生成奠定基础。

### 自回归蒸馏：从数十步到三步去噪

双向扩散模型通常需要 50 步以上的迭代去噪，无法满足实时性要求。StreamAvatar 在 Stage 1 中采用 **Score Identity Distillation**，以双向教师模型（基于 Wan2.2-TI2V-5B）为蒸馏源，将去噪步数从数十步压缩至 **$N=3$ 步**。蒸馏后的学生模型同时继承了教师模型的生成质量与块因果架构的流式推理能力，实现了速度与质量的关键平衡。

### 长视频一致性的三重保障

长视频生成面临的核心挑战是**身份漂移**和**注意力衰减**——随着生成帧数增加，模型对参考帧的注意力逐渐减弱，导致人物外观逐渐偏离原始身份。StreamAvatar 引入三个相互协同的组件来解决这一问题：

1. **Reference Sink（参考汇）**：在 KV 缓存中为参考帧 $x_0^0$ 的键值对设置永久保留机制，使其永远不会被逐出缓存。这强制模型在生成每一帧时始终关注参考图像，从根本上抑制身份漂移。

2. **Reference-Anchored Positional Re-encoding (RAPR)**：标准 RoPE 在长序列推理时，位置索引会超出训练分布范围，导致 train-test mismatch 和注意力衰减。RAPR 将位置索引重新锚定到参考帧，并**封顶最大距离 $D=9$**，确保远距离帧仍能有效关注参考帧。消融实验表明，引入 RAPR 后 FID 从 88.75 进一步降至 81.63。

3. **Consistency-Aware Discriminator（一致性感知判别器）**：Stage 2 的对抗精炼阶段引入双分支判别器——**Local Realism Branch** 判别单帧真实感，**Global Consistency Branch** 判别长时序一致性。该判别器从教师模型的主干网络初始化，能够有效捕捉长视频中的不一致伪影。消融实验证实，标准判别器（w/o $D_{CA}$）在时序一致性上明显弱于完整模型。

### 分离式说话/聆听音频注入

现有化身生成方法仅处理说话状态，在聆听阶段通常保持静止，导致交互不自然。StreamAvatar 通过以下设计实现了自然的**听-说转换**：

- **Audio Mask（TalkNet）**：利用联合音视频检测方法自动区分说话帧和聆听帧，生成音频掩膜，无需修改原始波形。
- **分离式音频注意力**：在 DiT 块中扩展两个独立的交叉注意力模块——**Talk Audio Attention** 和 **Listen Audio Attention**，分别注入说话和聆听的音频特征。这使得模型能够根据对话状态生成对应的自然表情和手势，并在说与听之间实现流畅过渡。

消融实验进一步验证了音频掩膜施加位置的重要性：在 Wav2Vec 提取的特征上施加掩膜（Ours），相比在原始音频上施加掩膜（Pre-Mask），LBKV 从 17.74 降至 16.98，LHKV 从 21.44 大幅降至 15.49，表明特征级掩膜能更有效地解耦说话与聆听信息。

### 方法谱系与知识库定位

StreamAvatar 的定位是**实时流式交互式全身体化身生成**。与之相关的工作可分为三类：

- **说话化身生成**：StableAvatar、OmniAvatar、HunyuanVideo-Avatar (HY-Avatar)、Hallo3、EchoMimicV3 等方法仅支持单向说话生成，缺乏聆听行为和流式能力。
- **交互式头部化身生成**：INFP、ARIG 等方法支持听-说交互，但仅限于头部区域，且不具备实时流式能力。
- **流式交互式全身体化身生成**：MIDAS、X-Streamer 等方法是与 StreamAvatar 最直接可比的基线，但在生成质量和自然度上存在差距（定性对比见 Figure 9、Figure 10）。

StreamAvatar 的独特贡献在于：首次将扩散模型的高质量生成能力与实时流式推理、自然交互对话统一在一个框架内，其两阶段蒸馏-精炼范式为其他扩散模型的实时化适配提供了可复用的技术路径。

### 问题定位与设计动机

现有扩散式人类化身生成方法面临两个结构性瓶颈：(1) 模型采用非因果的双向注意力，且迭代去噪过程计算开销极大，无法实现实时流式生成；(2) 这些方法通常只处理说话状态而忽略聆听行为，导致交互不自然。StreamAvatar 的核心思路是将一个高质量但速度较慢的非因果扩散模型，通过两阶段框架高效适配为实时流式生成器。

### 两阶段框架总览

StreamAvatar 的整体 pipeline 由两个阶段组成（见 Figure 2）：

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the two-stage autoregressive adaptation and acceleration framework. The original bidirectional DiT is first transformed into a block-causal DiT with block size C = 3. Then, in stage 1, we apply Score Identity Distillation to distill from the bidirectional teacher into a block-causal student. A Reference Sink and Reference-Anchored Positional Re-encoding is introduced to improve long-term stability and consistency. In stage 2, we apply an adversarial refinement process guided by a Consistency-Aware Discriminator, to further improve generation quality, consistency, and stability*

**第一阶段：自回归蒸馏 (Autoregressive Distillation)**。该阶段完成两项关键改造：
- **架构因果化**：将原始的**双向 DiT (bidirectional DiT)** 改造为**块因果 DiT (block-wise causal DiT)**，其中 chunk 大小 C=3。具体而言，生成窗口被划分为连续的 chunk，第 i 个 chunk 的起始帧和结束帧索引定义为 $s_i = (i-1) \cdot C + 1$ 和 $e_i = i \cdot C$。chunk 之间强制因果注意力，chunk 内部保持双向注意力。
- **少步蒸馏**：利用 Score Identity Distillation 将教师模型数十步的迭代去噪过程蒸馏为仅需 3 步的自回归学生模型。训练目标基于 Flow Matching 框架，带噪潜变量通过线性插值构造 $x^{n} = (1-n)x^{0} + n\epsilon$，模型需要预测的速度场为 $v = \epsilon - x^{0}$。

**第二阶段：对抗性精炼 (Adversarial Refinement)**。在蒸馏后的学生模型基础上，引入一致性感知判别器 (Consistency-Aware Discriminator) 进行对抗训练，进一步提升生成质量和时序一致性。

### 输入输出流

系统的输入包括：一张参考图像 $x_{0}^{0}$、文本提示（实验中固定为 “a person is speaking and listening.”）、以及用户/智能体的音频流。音频流首先经过 TalkNet 生成音频掩膜 (Audio Mask)，用于区分说话帧和聆听帧；随后音频掩膜与 Wav2Vec 提取的音频特征一起送入音频编码器 (Audio Encoder)，产生分离的说话特征和聆听特征。这些特征通过 DiT 块中新增的 Talk Audio Attention 和 Listen Audio Attention 两个交叉注意力模块注入视频潜变量。系统最终输出高分辨率、实时的流式人类视频，呈现自然的说话/聆听表情与手势过渡。

### 长视频一致性的三个关键机制

为解决长视频生成中的身份漂移和 out-of-distribution 问题，框架引入了三个相互配合的组件：

1. **Reference Sink（参考汇）**：在 KV 缓存中永久保留参考帧 $x_{0}^{0}$ 的 KV 对，从不逐出，强制模型在生成全程持续关注参考帧的身份信息。

2. **RAPR (Reference-Anchored Positional Re-encoding，参考锚定位置重新编码)**：改变 KV 缓存中位置索引的管理方式，将最大距离 D 上界限制（实验中 D=9）。这解决了两个问题：训练-推理时的位置编码不匹配 (train-test mismatch)，以及远距离帧的注意力衰减。Figure 3 对比了 Vanilla RoPE 与 RAPR 的机制差异。

3. **一致性感知判别器**：采用双分支设计——局域真实感分支 (Local Realism Branch) 和全局一致性分支 (Global Consistency Branch)，从教师模型的主干网络初始化，在对抗训练中同时约束单帧质量和跨帧时序一致性。

### 交互能力扩展

Figure 4 展示了交互式人类生成模型的完整架构。在基础视频模型之上，系统扩展了音频相关模块，通过音频掩膜机制和分离的说话/聆听音频注意力，使模型能够根据对话状态生成对应的自然行为和平滑过渡。消融实验表明，将音频掩膜应用于 Wav2Vec 提取后的特征（而非原始音频）能获得更好的聆听行为生成效果（Table 3：LBKV 17.74 vs 16.98，LHKV 21.44 vs 15.49）。

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/004_Figure_4.jpg]]
*Figure 4: The architecture of our interactive human generation model. We extend the original video model with audio-related modules to support talking and listening audio conditioning*

### 两阶段自回归适配框架

StreamAvatar 的核心是一个两阶段自回归适配与加速框架，其目标是将一个高质量但非因果的双向扩散模型改造为支持实时流式生成的自回归模型。框架的教师模型基于 **Wan2.2-TI2V-5B**，该模型由因果视频 VAE 和双向 DiT 去噪器组成，在 Flow Matching 框架下训练。

#### 阶段一：自回归蒸馏

阶段一承担两个关键任务：将双向 DiT 重新架构为块因果 DiT，并将教师模型的迭代去噪过程蒸馏为少步因果学生模型。

**块因果注意力机制**：原始 DiT 在整个生成窗口内使用双向自注意力。StreamAvatar 将其改造为块因果注意力，以 chunk 大小 $C=3$ 为例，第 $i$ 个 chunk 的起始帧和结束帧索引定义为：

$$s_i = (i-1) \cdot C + 1, \quad e_i = i \cdot C$$

在 chunk 之间强制因果注意力，而在每个 chunk 内部保持双向注意力。推理时，模型通过滚动 KV 缓存实现逐 chunk 的自回归生成，无需重新计算历史帧。

**Score Identity Distillation**：教师模型在 Flow Matching 框架下，通过干净潜变量 $x^0$ 和高斯噪声 $\epsilon$ 的线性插值构造带噪潜变量：

$$x^n = (1-n)x^0 + n\epsilon$$

模型需要预测速度场 $v = \epsilon - x^0$，训练目标为均方误差损失。蒸馏过程中，学生模型被训练为在仅 $N=3$ 步去噪下匹配教师的生成质量。

#### 长视频一致性的三个关键组件

自回归生成面临长视频一致性和身份漂移的核心挑战。StreamAvatar 引入三个组件协同解决：

**Reference Sink（参考汇）**：在 KV 缓存中永久保留参考帧 $x_0^0$ 的 KV 对，永不驱逐。这强制模型在生成所有后续帧时持续关注参考帧，从根本上抑制身份漂移。

**Reference-Anchored Positional Re-encoding (RAPR)**：标准 RoPE 使用全局帧索引，在长序列推理中会出现训练-测试不匹配和注意力衰减问题。RAPR 通过将位置索引重新锚定到参考帧，并将最大距离上限设为 $D=9$，防止远距离帧的注意力衰减，确保模型始终稳定地关注参考帧。

**Consistency-Aware Discriminator（一致性感知判别器）**：阶段二引入对抗性精炼，判别器采用双分支设计——局域真实感分支和全局一致性分支，均从预训练教师模型的主干网络初始化。该判别器引导生成器在保持单帧质量的同时提升时序一致性。

### 交互式人类生成架构

为实现自然的听-说交互，StreamAvatar 在视频模型中扩展了音频相关模块。

**音频掩膜与特征提取**：通过 **TalkNet**（联合音视频检测方法）获取音频掩膜，区分说话帧和聆听帧。音频掩膜应用于 Wav2Vec 特征提取之后，而非原始音频之上。消融实验（Table 3）证实，在特征层面施加掩膜优于在原始音频层面施加掩膜（Pre-Mask 变体）。

**分离式音频注意力**：音频编码器接收原始音频片段和音频掩膜，输出分离的说话特征和聆听特征。DiT 块中扩展了两个音频注意力模块——Talk Audio Attention 和 Listen Audio Attention——通过逐帧交叉注意力将说话和聆听线索分别注入视频潜变量。

对于未压缩视频帧 $t=0$，其音频特征由前后数个 Wav2Vec 特征拼接而成：

$$f'_t = \{\mathrm{concat}(\{f_i\}_{i=t-2}^{t+2})\}, \quad t=0$$

这一设计使模型能够根据对话状态动态切换行为：说话时生成生动的口型和手势，聆听时呈现自然的微表情和姿态变化，并在两种状态之间实现平滑过渡。

## 实验与关键发现

### 核心瓶颈与模型改造的因果验证

StreamAvatar 的实验设计围绕一个中心假设展开：高质量但速度缓慢的非因果扩散模型，可以通过两阶段框架（自回归蒸馏 + 对抗性增强）高效适配为实时流式生成器。为验证这一假设，作者从三个维度进行了消融：**长视频一致性**（Reference Sink、RAPR）、**生成质量**（对抗性精炼与一致性感知判别器）和**交互能力**（音频掩膜策略）。

消融的起点是仅使用 Self-Forcing 的基线模型。该基线在长视频生成时出现严重的身份漂移，FID 高达 96.58。逐步加入各组件后，性能持续改善：

- **+Reference Sink**：将参考帧的 KV 对永久保留在缓存中，强制模型持续关注参考身份，FID 降至 88.75。
- **+RAPR**：通过锚定参考帧的位置编码并限制最大距离 D=9，解决了训练-推理不一致和远距离注意力衰减问题，FID 进一步降至 81.63，长视频上的时间一致性也显著提升。
- **+GAN w/o D_CA**（标准判别器的对抗精炼）：虽进一步改善视觉质量，但一致性指标不及完整模型。
- **完整模型（+Consistency-Aware Discriminator）**：采用双分支判别器（局部真实性分支 + 全局一致性分支），FID 达到最优的 74.21，同时 IQA 等感知质量指标也表现最佳。

这一递进式消融（Table 1）清晰地表明：**Reference Sink 和 RAPR 是解决长视频身份漂移的关键机制，而一致性感知判别器则是平衡局部质量与全局一致性的核心组件**。

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison with SoTA talking avatar video generation methods. Metrics are reported on both short and long datasets, separated by*

### 主实验结果

#### 说话化身生成（Talking Avatar）

在短数据集（50 对，5s 音频）和长数据集（25 对，20s 音频）上，StreamAvatar 与 **StableAvatar**、**OmniAvatar**、**HunyuanVideo-Avatar (HY-Avatar)**、**Hallo3**、**EchoMimicV3** 等基线进行了全面对比（Table 1）。

- **FID**：StreamAvatar 取得 74.21，优于 StableAvatar 的 75.20，相比基线最优的 HY-Avatar（未直接报告 FID 值，但 StreamAvatar 在 EMTD 上以 61.84 优于 HY-Avatar 的 63.09）具有竞争力。
- **FVD**：StreamAvatar 的 707.34 高于 HY-Avatar 的 557.46，说明在视频级动态一致性上仍有提升空间，但仍处于竞争区间。
- **Sync-C（长数据集）**：StreamAvatar 取得 6.64，略优于 OmniAvatar 的 6.47，表明唇音同步精度在长时间生成中保持稳定。
- **EMTD 数据集**（110 个半身演讲视频，Table 4）：StreamAvatar 的 FID 为 61.84，优于所有基线，其中 HY-Avatar 以 63.09 位居第二。

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/010_Table_4.jpg]]
*Table 4: Quantitative comparison with SoTA talking avatar video generation methods on the EMTD dataset. Best in bold and second best underlined*

定性对比（Figure 5）进一步显示，StreamAvatar 生成的说话视频在身份保持和表情自然度上优于现有方法。

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison with SoTA talking avatar video generation methods. Please zoom in for details*

#### 交互式化身生成（Interactive Avatar）

在交互式数据集（50 个来自 SpeakerVid-5M 的视频）上，StreamAvatar 与仅支持说话的基线进行了对比（Table 2）。基线在聆听阶段保持几乎静止，而 StreamAvatar 能生成自然的聆听行为。

- **LBKV（聆听行为关键点方差）**：StreamAvatar 15.88 vs 基线 6.05（+9.83），表明生成的聆听动作丰富度显著提升。
- **LHKV（聆听头部关键点方差）**：StreamAvatar 16.24 vs 基线 4.53（+11.71），进一步验证头部运动在聆听阶段的自然性。
- **LFKV（聆听面部关键点方差）**：StreamAvatar 7.11 vs 基线 2.39，面部微表情在聆听时也更为生动。

定性对比（Figure 6）直观展示了这一差异：基线在聆听阶段近乎静止，而 StreamAvatar 的化身能对聆听音频做出自然反应，在说话与聆听之间流畅过渡。

#### 用户偏好研究

用户研究（Table 5）从多个维度进行了成对偏好投票。StreamAvatar 在视觉质量、唇音同步、动作自然度和整体偏好上均显著优于基线，具体偏好率需要查看原文表格（此处证据锚定于 Table 5，但具体数值需从原文获取）。

### 关键设计选择的消融

#### 音频掩膜位置

音频掩膜（Audio Mask）用于区分说话帧和聆听帧，而不修改波形本身。Table 3 的消融对比了两种策略：

![[assets/figures/papers/paper_list_l937_https_arxiv_org_abs_2512_22065/figures/008_Table_3.jpg]]
*Table 3: Ablation on the audio mask position*

- **Pre-Mask**：在原始音频输入 Wav2Vec 之前施加掩膜。
- **Ours（Post-Mask）**：在 Wav2Vec 提取特征之后施加掩膜。

结果显示，Post-Mask 策略在 LBKV（17.74 vs 16.98）和 LHKV（21.44 vs 15.49）上均优于 Pre-Mask，说明在特征空间施加掩膜能更有效地分离说话与聆听的音频表征，从而生成更自然的交互行为。

#### Chunk 大小与 KV 缓存长度

Figure 12 展示了 chunk 大小 C 和 KV 缓存总长度 L 对实时性能的影响。首帧延迟（FFD）和实时因子（RTF）随 C 和 L 的增加而上升。论文最终采用 C=3、N=3（去噪步数）的配置，在生成质量和推理速度之间取得平衡。

### 实时性能

Table 6 报告了 StreamAvatar 的实时性能评估。在消费级 GPU 上，模型能够以流式方式生成高分辨率视频，满足实时交互需求。具体的延迟和吞吐量数值需参考原文表格。

### 失败模式与局限性

尽管 StreamAvatar 在说话与聆听生成上表现出色，但论文指出了一些未解决的问题：

- **遮挡区域处理**：当参考图像中存在遮挡（如手部遮挡面部）时，模型缺乏长期记忆机制来合理补全被遮挡区域。
- **动作多样性**：当前模型的动作生成主要依赖音频驱动，缺乏高层语义规划，可能限制动作的丰富度。
- **VAE 解码延迟**：流式推理中，VAE 解码仍是延迟瓶颈之一，更高效的解码策略有待探索。

这些问题在现有实验中尚未以定量形式呈现为“失败案例”，但作者将其列为开放问题，提示在实际部署中可能需要额外处理。

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

StreamAvatar 瞄准的是**实时、流式、交互式人类化身视频生成**这一复合任务。该任务的传统解法存在两个关键瓶颈：

1.  **速度瓶颈**：现有高质量扩散式化身生成方法（如 StableAvatar、Hallo3、EchoMimicV3）依赖双向自注意力机制，且需要数十步迭代去噪，无法实现实时流式推理。
2.  **交互缺失**：几乎所有现有方法仅支持“说话”状态生成，在用户聆听时化身趋于静止或产生不自然行为，无法支撑自然的对话交互。

StreamAvatar 的因果调控旋钮是将双向 DiT 改造为**块因果 DiT**，并通过自回归蒸馏将去噪步数从 50+ 步压缩至 3 步，在保持生成质量的同时达成实时性；同时引入分离的**说话/聆听音频注意力**和**音频掩膜**，使模型能根据对话状态生成对应的自然行为与过渡。

### 2. 与基线方法的关系

#### 2.1 说话化身基线

StreamAvatar 与以下纯说话化身方法进行了定量对比：

-   **StableAvatar**：说话化身基线，在短数据集上 FID 为 75.20，StreamAvatar 以 74.21 略微领先。
-   **HY-Avatar (HunyuanVideo-Avatar)**：在短数据集上 FVD 最低（557.46），StreamAvatar 的 FVD（707.34）略逊于 HY-Avatar，但在 FID 和多个同步指标上表现更优或持平。
-   **Hallo3**、**EchoMimicV3**：同为说话化身方法，StreamAvatar 在视觉质量和唇音同步上整体达到领先或高度竞争水平（见 Table 1）。

在 EMTD 数据集（110 个半身说话视频）上，StreamAvatar 的 FID 为 61.84，优于最佳基线 HY-Avatar 的 63.09（Table 4）。

#### 2.2 交互化身基线

交互式化身生成是 StreamAvatar 的核心差异化能力。对比对象包括：

-   **OmniAvatar**：被改造为交互基线，即在聆听阶段喂入静音音频。StreamAvatar 在长数据集上的 Sync-C（6.64）略优于 OmniAvatar（6.47），且在交互数据集上的 LBKV/LHKV 指标大幅领先（15.88 vs 6.05, 16.24 vs 4.53，Table 2），表明其聆听行为生成能力远超简单静音方案。
-   **INFP**、**ARIG**：交互式头部化身方法，仅做定性对比（Figure 8）。
-   **MIDAS**、**X-Streamer**：流式交互全身化身方法，仅做定性对比（Figure 9、Figure 10）。

**关键差异**：上述交互方法多聚焦头部区域或特定场景，StreamAvatar 是首个在**全身、高分辨率、实时流式**设定下同时支持说话与聆听行为生成的扩散式方法。

### 3. 技术谱系：从双向扩散到流式自回归

StreamAvatar 的方法谱系可概括为“**高质量双向扩散教师 → 块因果自回归学生 → 对抗性精炼**”的两阶段适配框架：

| 阶段 | 核心操作 | 继承自 | 创新点 |
|------|----------|--------|--------|
| 教师模型 | 双向 DiT 去噪（Wan2.2-TI2V-5B） | Rectified Flow 框架 | — |
| 架构改造 | 双向注意力 → 块因果注意力（chunk size C=3） | 自回归生成范式 | 块内双向、块间因果的混合注意力 |
| Stage 1：自回归蒸馏 | Score Identity Distillation 将 50+ 步双向去噪蒸馏为 3 步因果学生 | Self-Forcing 等蒸馏方法 | Reference Sink + RAPR 解决长视频一致性问题 |
| Stage 2：对抗性精炼 | 一致性感知判别器提升视觉质量和时序一致性 | GAN 精炼范式 | 双分支判别器（局部真实感 + 全局一致性） |
| 交互扩展 | 音频掩膜 + 分离的 Talk/Listen Audio Attention | 音频驱动化身生成 | 首次将说话/聆听状态解耦注入 DiT |

**Reference Sink** 和 **Reference-Anchored Positional Re-encoding (RAPR)** 是该框架的两项关键原创设计。Reference Sink 将参考帧的 KV 对永久保留在缓存中，强制模型持续关注参考身份；RAPR 通过截断最大位置距离（D=9）并重新锚定缓存中的位置索引，解决了长序列推理中的训练-测试不匹配和注意力衰减问题（Figure 3）。消融实验证实，逐步加入 Reference Sink 和 RAPR 后，FID 从 96.58 降至 88.75 再到 81.63（Table 1），身份漂移得到显著抑制。

### 4. 适用边界与局限

#### 4.1 适用边界

-   **输入条件**：单张参考图像 + 用户/智能体音频流 + 固定文本提示（“a person is speaking and listening.”）。
-   **生成范围**：全身人类化身视频，支持说话与聆听状态的实时流式生成。
-   **实时性能**：在 chunk size C=3、KV 缓存总长度 L 受限的设定下，可实现实时因子（RTF）满足流式要求（Figure 12、Table 6）。

#### 4.2 已知局限与开放问题

论文明确指出的局限和未来方向包括：

1.  **遮挡区域处理**：当前模型缺乏长时记忆机制，无法有效处理被遮挡的身体部位。未来可引入长时记忆模块来追踪遮挡区域的状态。
2.  **动作多样性**：当前生成的动作多样性受限于训练数据分布。利用多模态大语言模型进行语义规划，有望丰富化身的行为表现。
3.  **解码延迟**：VAE 解码仍是流式延迟的瓶颈之一，探索更高效的 VAE 解码方案可进一步降低端到端延迟。

### 5. 知识库定位

StreamAvatar 处于**扩散模型加速**、**自回归视频生成**和**音频驱动化身**三个领域的交叉点：

-   **扩散模型加速**：继承 Rectified Flow 和 Score Identity Distillation 的少步生成路线，但将其首次应用于块因果自回归视频生成场景。
-   **自回归视频生成**：借鉴自回归 Transformer 的 KV 缓存机制，但创新性地引入 Reference Sink 和 RAPR 来解决身份一致性问题，这对长视频流式生成具有通用参考价值。
-   **音频驱动化身**：在传统音频到视频映射的基础上，首次将说话/聆听状态解耦为独立的注意力分支，为交互式化身生成建立了新的技术范式。

**证据强度评估**：核心主张（两阶段框架有效性、Reference Sink/RAPR 的消融增益、交互能力的定量提升）均有 Table 1-4 和 Figure 5-7 的充分实验支撑，置信度较高。与 MIDAS、X-Streamer 等流式方法的对比目前仅停留在定性层面，定量对比的缺失使得在该子方向上的相对优势需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/StreamAvatar_Streaming_Diffusion_Models_for_Real_Time_Interactive_Human_Avatars.pdf]]
