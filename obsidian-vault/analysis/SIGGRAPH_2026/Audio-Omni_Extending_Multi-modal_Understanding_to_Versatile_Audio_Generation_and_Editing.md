---
title: "Audio-Omni: Extending Multi-modal Understanding to Versatile Audio Generation and Editing"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2026
pdf_ref: paperPDFs/SIGGRAPH_2026/Audio_Omni_Extending_Multi_modal_Understanding_to_Versatile_Audio_Generation_and_Editing.pdf
project_link: "https://zeyuet.github.io/Audio-Omni"
code_link: null
aliases:
- AO
- Audio-Omni
tags:
- SIGGRAPH_2026
- topic/generative_models_diffusion
core_operator: 采用解耦架构，冻结预训练的多模态大语言模型（Qwen2.5-Omni）作为推理核心，仅训练扩散变压器（DiT）进行生成和编辑，并通过设计的混合条件机制将高层语义（MLLM特征和文本嵌入）与低层信号（梅尔谱和视频同步特征）分离注入，同时构建包含超百万样本的AudioEdit数据集以赋予模型编辑能力。
primary_logic: 冻结的MLLM保留了丰富的多模态知识和涌现能力，其倒数第二层隐藏状态作为条件能有效传递世界知识、多语言理解和上下文推理，从而让仅训练英语的生成模块具备零样本跨语言生成、知识增强生成等能力，实现了超越任务单一训练范围的泛化。
claims:
- Audio-Omni在生成和编辑任务上一致且显著优于所有统一基线模型，并在T2M和TTS上超越专有专家模型。
- 混合条件消融实验表明，高层语义作为交叉注意力上下文、低层信号作为噪声拼接的策略显著优于其他注入方式。
- AudioEdit混合管线构建的训练数据相比仅合成或仅真实数据能获得最佳编辑性能，验证了数据混合的必要性。
- 模型在仅用英语训练的情况下，在中文等多语言文本到音频生成上取得了与英语专有模型可比的质量，展现了跨语言零样本能力。
---

# Audio-Omni: Extending Multi-modal Understanding to Versatile Audio Generation and Editing

> [!tip] 核心洞察
> 冻结的MLLM保留了丰富的多模态知识和涌现能力，其倒数第二层隐藏状态作为条件能有效传递世界知识、多语言理解和上下文推理，从而让仅训练英语的生成模块具备零样本跨语言生成、知识增强生成等能力，实现了超越任务单一训练范围的泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Audio-Omni：将多模态理解扩展到多功能音频生成与编辑 |
| 英文题名 | Audio-Omni: Extending Multi-modal Understanding to Versatile Audio Generation and Editing |
| 会议/期刊 | SIGGRAPH 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10708) · [Project](https://zeyuet.github.io/Audio-Omni) |
| Topic | #topic/generative_models_diffusion |
| Method | Audio-Omni |
| Dataset | MMSU, AudioCaps T2A, Musicaps T2M, VGGSound V2A |

> [!tip] 效果简介
> - MMSU 上，MMSU↑ 56.83 vs Ming-Omni (47.53) (+9.30)。
> - AudioCaps T2A 上，FAD↓ 1.86 vs Unified-IO2 (7.81) (-5.95)。
> - Musicaps T2M 上，FAD↓ 1.94 vs MusicGen (3.94) (-2.00)。

## 概述

### 1. 问题背景与核心瓶颈

音频领域长期面临一个结构性矛盾：理解、生成与编辑三类能力被分散在多个专用模型中，缺乏一个能同时覆盖通用声音、音乐和语音的端到端统一框架。现有统一模型要么受限于特定域（如仅处理语音或音乐），要么依赖工具链编排而无法进行端到端联合优化，且编辑能力严重不足。其根本瓶颈在于：**大规模、高质量、指令引导的音频编辑配对数据极度稀缺**，同时缺乏一种能将多模态理解语义有效注入生成过程的架构设计。

### 2. 核心方法

Audio-Omni 提出了一个解耦架构来解决上述瓶颈。其核心设计包含三个关键决策：

- **解耦架构**：冻结预训练的多模态大语言模型 **Qwen2.5-Omni-3B** 作为推理核心，保留其丰富的多模态知识和涌现能力；仅训练一个基于 **Rectified Flow** 的扩散变压器（DiT）来处理生成与编辑。两者通过特征投影器连接。

- **混合条件机制**：将条件信息分解为两个互补流——**高层语义流**（MLLM倒数第二层隐藏状态 + 文本嵌入）通过交叉注意力注入，提供全局指令和语义引导；**低层信号流**（梅尔谱特征 + 视频同步特征）通过噪声拼接注入，提供精确的时间和音量控制。

- **AudioEdit 数据集**：构建了包含超百万样本的音频编辑数据集，通过混合管线结合真实世界挖掘（约5万高质量配对）与程序化合成（约15万配对用于增删提取，50万配对用于风格迁移），解决了编辑数据匮乏问题。

### 3. 核心洞察

冻结的 MLLM 保留了丰富的多模态知识和涌现能力，其倒数第二层隐藏状态作为条件信号能有效传递世界知识、多语言理解和上下文推理。这使得仅用英语训练的生成模块获得了**零样本跨语言生成**、**知识增强生成**等能力，实现了超越任务单一训练范围的泛化——这是该方法区别于以往工作的关键洞察。

### 4. 主要结果

Audio-Omni 在理解、生成和编辑任务上一致且显著优于所有统一基线模型。在生成任务上，其 **AudioCaps** 文本到音频生成的 FAD 达到 1.86，大幅领先 Unified-IO2 的 7.81；在 **MusicCaps** 文本到音乐生成上 FAD 为 1.94，优于专用模型 MusicGen 的 3.94；在语音合成上 WER 为 1.77，与专用模型 F5-TTS 的 1.83 相当。在编辑任务上，平均 FAD 为 3.27，优于 ZETA（3.81）和 MMEDIT（3.95）。消融实验证实了混合条件策略和混合数据训练的优越性，以及 MLLM 特征相较于单模态编码器的显著优势。

### 5. 方法谱系与知识库定位

Audio-Omni 处于**多模态统一模型**与**音频生成扩散模型**的交叉地带。与 **Ming-Omni**（统一语音理解与生成）、**Unified-IO2**（通用多模态统一）等端到端统一模型相比，其解耦设计允许分别利用冻结 MLLM 的推理能力和 DiT 的生成能力，避免了联合训练中模态间干扰。与 **Tango2**、**Stable-Audio-Open**、**MusicGen** 等专用生成模型相比，其统一框架覆盖了更广泛的任务范围。与 **ZETA**、**MMEDIT** 等音频编辑模型相比，其混合条件机制和 AudioEdit 数据集提供了更强的编辑灵活性和数据支撑。该方法的核心贡献在于：证明了**冻结 MLLM + 可训练 DiT + 混合条件**的架构范式能够将多模态理解能力有效迁移至生成与编辑任务，为构建真正的音频通用模型提供了可行路径。

### 6. 局限与开放问题

模型在复杂音频推理基准（如 MMAU）上仍落后于专用理解模型；零样本跨语言生成质量随语言与英语距离增加而下降；7.9B 参数量和 100 步 ODE 推理带来较大计算开销。开放问题包括：能否通过引入少量多语言数据缩小跨语言性能差距、能否将解耦架构推广至其他模态、如何开发更高效的采样策略、以及如何构建更细粒度的编辑指令数据集。

## 背景与动机

音频作为人类感知世界的核心模态之一，涵盖了通用环境声、音乐和语音三大领域。近年来，多模态大语言模型（MLLM）在文本、图像和视频理解上取得了显著进展，但在音频领域，现有工作仍呈现出明显的碎片化特征：理解、生成与编辑三大能力通常由彼此独立的专有模型分别承担，缺乏一个能同时覆盖全部音频子域的端到端统一框架。

具体而言，当前的统一模型存在以下结构性缺口：

**域覆盖不完整。** 多数统一模型仅局限于某一特定音频子域。例如，**Ming-Omni** 专注于语音理解与生成的统一，**MuMuLLaMA** 面向音乐理解与生成，而 **Unified-IO2** 虽试图构建通用多模态模型，却未纳入音频编辑能力。真正能同时处理通用声音、音乐和语音的理解、生成与编辑的端到端框架仍属空白。

**编辑能力严重缺失。** 音频编辑——包括添加、移除、提取声源以及风格迁移——是实际应用中的高频需求，但现有统一模型几乎不具备此能力。这一缺陷的根源在于大规模高质量指令引导的音频编辑配对数据极度匮乏。现有编辑数据集多为小规模合成混合数据，与真实音频之间存在显著的域差距，且编辑类型单一，难以支撑鲁棒的模型训练。

**架构耦合导致优化困难。** 部分工作试图通过工具编排（tool orchestration）将理解模型与生成模型拼接，但这种松耦合方式无法进行端到端的联合优化，限制了模型在不同任务间的知识共享和协同提升。

在上述背景下，Audio-Omni 的动机可归结为三个核心目标：第一，构建一个真正覆盖通用声、音乐、语音三大域的统一框架，同时具备理解、生成与编辑能力；第二，通过设计大规模混合数据管线解决编辑数据瓶颈；第三，采用解耦架构，使冻结的 MLLM 保留其多模态理解和涌现能力，同时仅训练生成模块以实现高效的多任务学习。这一设计路线旨在回答一个关键问题：能否让一个模型在保持专家级生成质量的同时，继承大语言模型的世界知识和跨语言推理能力，从而超越单一任务训练所能达到的泛化边界？

## 核心创新

Audio-Omni的核心创新在于通过**解耦架构**与**混合条件机制**，首次在单一端到端框架内统一了通用声音、音乐和语音三大域的理解、生成与编辑任务。其关键设计围绕三个维度展开，分别对应方法谱系中的三个核心changed slots。

### 1. 解耦架构：冻结MLLM + 可训练DiT

现有统一模型（如**Ming-Omni**、**Unified-IO2**、**MuMuLLaMA**）或专有模型通常采用单一端到端架构或工具链编排，缺乏跨任务的联合优化能力。Audio-Omni提出**冻结多模态大语言模型（Qwen2.5-Omni-3B）作为推理核心，仅训练扩散变压器（DiT）进行生成与编辑**的解耦设计（Figure 3）。这一架构的核心洞察在于：冻结的MLLM保留了丰富的多模态知识和涌现能力，其倒数第二层隐藏状态作为条件能有效传递世界知识、多语言理解和上下文推理，使得仅用英语训练的生成模块获得了零样本跨语言生成、知识增强生成等泛化能力——这些能力超出了任务单一训练范围，属于从MLLM继承的涌现特性。

### 2. 混合条件机制：语义与信号的双流解耦注入

传统条件生成模型通常采用单一条件流，未显式分离高层语义与低层信号信息。Audio-Omni设计了**两条互补的条件流**，并通过不同的注入策略将其送入DiT主干（Figure 3）：

- **高层语义流（High-Level Semantic Stream）**：由MLLM多模态特征 $\mathbf{F}_{\mathrm{mm}}$ 与转录编码器（ConvNeXtV2）输出的字符级嵌入 $\mathbf{F}_{\mathrm{trans}}$ 拼接而成（公式3），作为交叉注意力的上下文注入DiT，提供全局指令和语义引导。
- **低层信号流（Low-Level Signal Stream）**：由Synchformer提取的视频同步特征 $\mathbf{F}_{\mathrm{sync}}$ 与Mel Encoder计算的梅尔谱特征 $\mathbf{F}_{\mathrm{mel}}$ 拼接而成（公式4），直接与输入噪声和时间嵌入拼接，提供精确的时间和音量控制。

消融实验（Table 6）证实，这一“高层语义作为交叉注意力上下文、低层信号作为噪声拼接”的策略在所有任务上显著优于其他注入方式（如全部使用交叉注意力或全部拼接），验证了语义与信号信息分离注入的必要性。

### 3. AudioEdit数据集：混合管线构建的大规模编辑数据

音频编辑能力的缺失是此前统一模型的关键瓶颈，根源在于缺乏大规模高质量的指令引导编辑配对数据。Audio-Omni提出的**AudioEdit数据集**包含超过100万样本（Table 1），通过混合管线构建以兼顾数据真实性与规模（Figure 2）：

- **真实数据分支**：从VGGSound等真实数据集中挖掘编辑对，使用MLLM（Gemini）进行类别识别，再通过专用分割模型（SAM-Audio）进行声源分离，经CLAP过滤后保留约5万高质量配对。
- **合成数据分支**：利用Scaper工具包程序化生成大量精确标注的编辑场景，包括添加、移除、提取（15万）和风格转换（50万）任务。

消融实验（Table 5）表明，混合真实与合成数据训练获得最佳编辑性能（FAD 2.48, LSD 1.82），仅使用合成数据性能显著下降（FAD 3.80），验证了数据混合策略的必要性。

### 方法谱系与知识库定位

Audio-Omni在方法谱系中处于**统一多模态理解-生成-编辑框架**的交汇点。其理解能力继承自**Qwen2.5-Omni**系列的全能模型路线，生成能力基于**Rectified Flow**（Liu et al., 2022）的扩散框架，编辑能力则通过自建AudioEdit数据集填补了领域空白。相对于**Ming-Omni**（仅覆盖语音理解与生成）、**Unified-IO2**（通用多模态但音频生成受限）、**MuMuLLaMA**（仅音乐域）等统一模型，Audio-Omni首次实现了三域全覆盖；相对于**Tango2**（专有T2A）、**MusicGen**（专有T2M）、**F5-TTS**（专有TTS）等专家模型，Audio-Omni在T2M和TTS上实现了超越，展现了统一框架的竞争力。

## 整体框架

Audio-Omni 采用**解耦架构**，将多模态理解与音频生成/编辑在模型层面分离，却通过精心设计的条件机制实现端到端联合训练。其核心设计哲学是：冻结一个强大的多模态大语言模型（MLLM）作为推理核心，以保留其预训练中积累的丰富世界知识与涌现能力；同时训练一个基于扩散变压器（DiT）的生成模块，专门负责音频的合成与编辑。

### 模块构成与数据流

整个框架由两大功能模块和两组条件流组成：

1.  **理解模块（Frozen MLLM）**
    采用冻结的 **Qwen2.5-Omni-3B** 作为多模态编码与推理核心。该模块接收文本、音频和视频输入，执行理解与推理任务，并提取其**倒数第二层的隐藏状态**作为高层语义特征 $\\mathbf{F}_{\\mathrm{mm}}$。实验表明，倒数第二层特征相比最终层或 CLAP/T5 等单模态编码器，能为下游生成提供更泛化、更丰富的语义表示（Table 7, Table A1）。

2.  **生成模块（Trainable DiT Backbone）**
    一个深度为 36 层、隐藏维度为 2048、拥有 32 个注意力头的 DiT 模型，基于 **Rectified Flow** 框架构建。其任务是预测从噪声 $\\mathbf{x}_1$ 到数据 $\\mathbf{x}_0$ 直线路径上的常速度场 $\\mathbf{v}$：
    $$\\frac{d\\mathbf{x}_t}{dt} = \\mathbf{v}, \\quad \\mathbf{x}_t = (1-t)\\mathbf{x}_0 + t\\mathbf{x}_1$$
    训练损失为均方误差：
    $$\\mathcal{L} = \\mathbb{E}_{t\\sim\\mathcal{U}(0,1), \\mathbf{x}_0, \\mathbf{x}_1, \\mathbf{c}} \\left[||v_{\\theta}(\\mathbf{x}_t, t, \\mathbf{c}) - (\\mathbf{x}_1 - \\mathbf{x}_0)||^2\\right]$$

3.  **混合条件机制（Hybrid Conditioning）**
    这是连接理解与生成模块的关键桥梁，将多源输入解耦为两个互补的条件流，并通过不同策略注入 DiT：
    -   **高层语义流（High-Level Semantic Stream）**：由 MLLM 的多模态特征 $\\mathbf{F}_{\\mathrm{mm}}$ 与可训练的 Transcript Encoder（ConvNeXtV2）提取的字符级嵌入 $\\mathbf{F}_{\\mathrm{trans}}$ 拼接而成：
        $$\\mathbf{c}_{\\mathrm{high}} = \\mathrm{Concat}(\\mathbf{F}_{\\mathrm{mm}}, \\mathbf{F}_{\\mathrm{trans}})$$
        该流作为**交叉注意力（Cross-Attention）的上下文**注入 DiT，提供全局指令、语义内容和世界知识。
    -   **低层信号流（Low-Level Signal Stream）**：由 Synchformer 从视频中提取的同步特征 $\\mathbf{F}_{\\mathrm{sync}}$ 与 Mel Encoder 从参考音频/语音提示中计算的梅尔谱特征 $\\mathbf{F}_{\\mathrm{mel}}$ 拼接而成：
        $$\\mathbf{c}_{\\mathrm{low}} = \\mathrm{Concat}(\\mathbf{F}_{\\mathrm{sync}}, \\mathbf{F}_{\\mathrm{mel}})$$
        该流**与输入噪声和时间嵌入直接拼接（Concatenation）**，提供精确的时间对齐和音量控制信号。

消融实验（Table 6）证实，这种“高层语义作交叉注意力上下文 + 低层信号作噪声拼接”的注入策略在所有任务上均取得最优综合得分，显著优于其他注入方式。

### 端到端训练与推理

整个模型拥有约 79 亿总参数，其中可训练的 DiT 和条件编码器部分约 30.5 亿参数。训练时，理解模块完全冻结，仅生成模块和条件编码器通过 Rectified Flow 目标进行端到端优化。推理时，MLLM 首先处理输入并生成理解响应与条件特征，随后 DiT 以 100 步 ODE 求解器从噪声生成目标音频，并可采用无分类器引导（guidance scale = 6.0）提升条件一致性。

### 关键设计优势

这种解耦设计带来两个核心优势：其一，冻结的 MLLM 保留了多语言理解和上下文推理能力，使得仅用英语训练的生成模块能够展现出零样本跨语言生成、知识增强生成等涌现能力；其二，混合条件机制将“高层语义”与“低层信号”分离注入，使模型既能遵循复杂的语义指令，又能精确控制编辑的时间边界和音色特征，从而在统一框架下同时胜任理解、生成与编辑三大类任务。

### 补充图表

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the Audio-Omni framework and its capabilities. (Top) Our decoupled architecture connects a frozen MLLM for understanding with a trainable DiT for audio synthesis via a feature projector. (Middle) A showcase of the model’s unified capabilities across understanding, generation, and editing. (Bottom) A demonstration of remarkable emergent abilities inherited from the MLLM*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/004_Figure_3.jpg]]
*Figure 3: The Audio-Omni Framework. Our framework utilizes a decoupled design with two distinct conditioning streams to guide a trainable DiT backbone. The High-Level Semantic Features stream provides global, instructional guidance. It is formed by concatenating features from a frozen MLLM (MM Features) with character-level embeddings from a trainable Transcript Encoder. The Low-Level Signal Features stream offers precise, temporal guidance for editing and synchronization. It combines features from Synchformer and Mel Encoder. These two streams are injected into the DiT via different mechanisms: the high-level stream as context for cross-attention, and the low-level stream concatenated with the input...*

## 核心模块与公式推导

### 解耦架构总览

Audio-Omni 采用解耦设计，将多模态理解与音频生成/编辑分离为两个独立组件，通过混合条件机制桥接：

- **冻结的多模态大语言模型（MLLM）**：采用 Qwen2.5-Omni-3B 作为推理核心，处理文本、音频、视频等多模态输入。其参数完全冻结，保留预训练阶段积累的世界知识、多语言理解和上下文推理能力。模型提取其倒数第二层（penultimate layer）的隐藏状态作为高层语义特征，经验表明该层比最终层提供更泛化、更丰富的语义表示（Table 7）。

- **可训练的扩散变压器（DiT）**：基于 Rectified Flow 框架构建，负责所有音频合成任务。DiT 主干包含 36 个 Transformer 块，隐藏维度 2048，32 个注意力头。整个模型总参数量约 7.9B，其中 DiT 及条件编码器共 3.05B 参数可训练。

### 核心公式：Rectified Flow

生成主干建立在 Rectified Flow 框架之上，其核心思想是将噪声到数据的生成过程建模为一条常速度直线路径。

**常微分方程定义**：

$$\frac{d\mathbf{x}_t}{dt} = \mathbf{v}$$

其中 $\mathbf{x}_t$ 是时刻 $t$ 的样本状态，$\mathbf{v}$ 是常速度向量。该 ODE 定义了从噪声到数据的直线传输轨迹。

**线性插值解**：

$$\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$$

其中 $\mathbf{x}_0$ 是目标数据（干净音频的潜在表示），$\mathbf{x}_1$ 是初始噪声（从标准高斯分布采样）。当 $t$ 从 0 变化到 1 时，$\mathbf{x}_t$ 沿直线从数据点移动到噪声点。

**训练损失**：

$$\mathcal{L} = \mathbb{E}_{t\sim\mathcal{U}(0,1), \mathbf{x}_0, \mathbf{x}_1, \mathbf{c}} \left[||v_{\theta}(\mathbf{x}_t, t, \mathbf{c}) - (\mathbf{x}_1 - \mathbf{x}_0)||^2\right]$$

网络 $v_{\theta}$ 以当前状态 $\mathbf{x}_t$、时间步 $t$ 和条件 $\mathbf{c}$ 为输入，预测真实速度 $(\mathbf{x}_1 - \mathbf{x}_0)$。损失函数为预测速度与真实速度之间的均方误差。时间步 $t$ 从均匀分布 $\mathcal{U}(0,1)$ 采样。

推理时，从随机噪声 $\mathbf{x}_1$ 出发，通过 100 步 ODE 求解器沿学习到的速度场积分至 $\mathbf{x}_0$，再经 VAE 解码器重建为音频波形。生成过程中采用无分类器引导（classifier-free guidance），引导尺度设为 6.0。

### 混合条件机制

条件信号被解耦为两个互补流，分别通过不同机制注入 DiT：

**高层语义流（High-Level Semantic Stream）**：

$$\mathbf{c}_{\mathrm{high}} = \mathrm{Concat}(\mathbf{F}_{\mathrm{mm}}, \mathbf{F}_{\mathrm{trans}})$$

- $\mathbf{F}_{\mathrm{mm}}$：冻结 MLLM 倒数第二层的多模态隐藏状态，携带全局语义、世界知识和指令理解。
- $\mathbf{F}_{\mathrm{trans}}$：可训练的 Transcript Encoder（基于 ConvNeXtV2）输出的字符级嵌入，提供语音相关的文本特征。

该流作为交叉注意力（cross-attention）的上下文注入 DiT 的每一层，提供全局指令和语义引导。

**低层信号流（Low-Level Signal Stream）**：

$$\mathbf{c}_{\mathrm{low}} = \mathrm{Concat}(\mathbf{F}_{\mathrm{sync}}, \mathbf{F}_{\mathrm{mel}})$$

- $\mathbf{F}_{\mathrm{sync}}$：Synchformer 从视频中提取的 25fps 同步特征，提供精确的时间对齐信息。
- $\mathbf{F}_{\mathrm{mel}}$：Mel Encoder 从参考音频或语音提示中计算的 100 维梅尔谱特征，提供音量和音色等声学细节。

该流直接与输入噪声和时间步嵌入拼接（concatenation），为编辑和同步任务提供精确的时间与信号级控制。

消融实验（Table 6）验证了该分离注入策略的优越性：高层语义作为交叉注意力上下文、低层信号作为噪声拼接的组合在所有任务上取得最优综合得分，显著优于其他注入方式（如全部使用交叉注意力或全部拼接）。

### 条件特征源选择

Table 7 和 Table A1 的消融表明，使用 MLLM 倒数第二层特征作为条件源优于以下替代方案：
- MLLM 最终层特征（性能下降，可能因过拟合于文本生成任务）
- 单模态编码器如 CLAP 或 T5（缺乏多模态上下文理解能力）

这验证了冻结 MLLM 中间表示能有效传递跨模态知识，使仅用英语训练的生成模块具备零样本跨语言生成等涌现能力。

### 补充图表

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/009_Figure_4.jpg]]
*Figure 4: 5.3.3 Inherited Abilities and Zero-Shot Capabilities. We further highlight several representative capabilities of Audio-Omni. The first two are emergent abilities inherited from the frozen MLLM’s world knowledge and in-context reasoning, while the latter two are enabled by our masking-based training strategy. We qualitatively showcase these in Figure 4*

## 实验与分析

### 1. 实验设置

Audio-Omni采用解耦架构，冻结的MLLM为**Qwen2.5-Omni-3B**，可训练的DiT骨干含36个Transformer块、隐藏维度2048、32个注意力头。模型总参数量约7.9B，其中可训练的DiT和条件编码器约3.05B。所有任务统一使用Rectified Flow目标（Equation 5）端到端训练，推理时采用100步ODE求解，并配合引导尺度为6.0的分类器无关引导。训练数据覆盖文本到音频、视频到音频、文本到语音、音频编辑等多类任务（详见Table A4）。评估指标包括FAD（Fréchet Audio Distance）、LSD（Log-Spectral Distance）、CLAP分数、WER（词错误率）以及理解任务的MMSU和MMAU准确率。

### 2. 理解能力评估

Table 2展示了多模态理解基准的结果。Audio-Omni在MMSU上取得**56.83**，显著超越此前最好的统一模型**Ming-Omni**（47.53），提升+9.30；在MMAU上取得63.30，与专有理解模型**Audio Flamingo3**（66.40）和**Qwen2-Audio-Instruct**（66.68）的差距已大幅缩小。这表明冻结MLLM的策略有效保留了预训练阶段的多模态理解能力，解耦架构并未损害推理核心的理解性能。

### 3. 生成能力评估

Table 3报告了多模态生成基准的定量结果。核心发现如下：

- **统一模型中的统治性优势**：Audio-Omni在所有生成任务上一致且显著超越所有统一基线模型。以AudioCaps文本到音频（T2A）为例，FAD仅**1.86**，而**Unified-IO2**为7.81，降幅达5.95；在MusicCaps文本到音乐（T2M）上FAD为**1.94**，远优于**MuMuLLaMA**的6.64。
- **超越专有专家模型**：更值得注意的是，Audio-Omni在T2M上超越了专有模型**MusicGen**（FAD 3.94），在文本到语音（TTS）任务上WER仅**1.77**，略优于**F5-TTS**（1.83）。在视频到音频（V2A）上FAD为**1.71**，优于**VATT**（2.55）。
- **跨语言零样本泛化**：Table A2显示，模型仅使用英语训练数据，但在中文文本到音频生成上FAD为**2.47**，与英语场景（1.86）可比，验证了冻结MLLM赋予的跨语言零样本能力。然而，随着语言与英语距离增加，性能有所下降（法语FAD 4.21），提示多语言训练可能进一步缩小差距。

### 4. 编辑能力评估

Table 4展示了音频编辑基准的结果。Audio-Omni在平均FAD上取得**3.27**，优于**ZETA**（3.81）和**MMEDIT**（3.95）；LSD为**2.27**，同样领先。Table A3的详细任务分解显示，模型在添加、移除、提取和风格迁移四类编辑任务上均保持稳定性能。这一优势源于AudioEdit数据集的规模与质量——混合真实世界挖掘（约50K高质量配对）和程序化合成（约150K配对）的策略，为编辑能力提供了关键数据支撑。

### 5. 消融实验

**数据组合消融**（Table 5）：仅使用合成数据训练时，编辑FAD升至3.80，LSD升至2.41；仅使用真实数据时FAD为3.02；混合两者则达到最优FAD **2.48**和LSD **1.82**。这验证了混合管线在兼顾声学真实性与规模多样性方面的必要性。

**条件注入策略消融**（Table 6）：对比了四种注入方式——高层语义经交叉注意力/低层信号经拼接（本文方案）、两者均经交叉注意力、两者均经拼接、两者经加法融合。本文方案在所有任务上取得最优综合得分，证明语义信息与信号信息需要不同的注入路径：全局指令适合交叉注意力，时序精确控制适合拼接。

**条件特征源消融**（Table 7）：使用MLLM倒数第二层隐藏状态优于最终层输出，也优于CLAP或T5等单模态编码器（Table A1）。倒数第二层保留了更丰富的语义表示，尚未被下一token预测目标过度压缩，因而对生成任务的泛化更有利。

**语音提示掩蔽策略**：训练中对梅尔谱提示随机掩蔽20-75%，使模型获得了零样本语音转换和语音编辑能力（Section 5.3.3），这一涌现行为在Figure 4(c)(d)中得到了定性展示。

### 6. 人类评估

Table A6报告了人类评估结果。在生成任务上，Audio-Omni的总体质量评分（MOS）和相关性评分均优于统一基线，并在T2M和TTS上与专有模型持平或略优。在编辑任务上，人类评估者对Audio-Omni编辑结果的偏好显著高于ZETA和MMEDIT。

### 7. 局限性与失败模式

尽管整体表现优异，Audio-Omni仍存在以下局限：

- **复杂推理不足**：在MMAU推理基准上落后于专有理解模型（如Audio Flamingo3的66.40 vs 63.30），说明冻结MLLM虽保留了基础理解能力，但在需要深层推理的任务上仍有差距。
- **远语言性能衰减**：跨语言零样本生成中，法语FAD（4.21）显著高于英语（1.86），模型对与训练语言距离较远的语言泛化能力受限。
- **推理效率瓶颈**：7.9B参数量配合100步ODE推理，对实时应用和边缘部署构成显著计算开销，需要更高效的采样策略（如蒸馏或减少步数）。
- **编辑粒度限制**：当前编辑依赖参考音频的梅尔谱提示，尚不支持纯文本参数化的细粒度编辑指令（如“将背景音量降低3dB”），这限制了编辑的灵活性和精度。

### 补充图表

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/006_Table_3.jpg]]
*Table 3: Quantitative results on multimodal generation benchmarks*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/010_Table_6.jpg]]
*Table 6: Ablation study on conditioning injection strategies*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/008_Table_5.jpg]]
*Table 5: Ablation study on dataset composition for audio editing training*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/011_Table_7.jpg]]
*Table 7: Ablation study on the source of conditional features from the MLLM*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/013_Table.jpg]]
*Table: A2. Zero-shot cross-lingual text-to-audio generation results*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/012_Table.jpg]]
*Table: A1. Ablation study on different encoders. We evaluate the impact of different encoders for text-to-audio (T2A) and video-to-audio (V2A) tasks*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/002_Table_1.jpg]]
*Table 1: Statistics of our proposed audio editing dataset AudioEdit*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the hybrid pipeline for constructing our AudioEdit dataset. The pipeline consists of two parallel branches to ensure both data authenticity and scale. The Real Data Branch (left) mines editing pairs from real-world datasets (e.g., VGGSound) by first using an MLLM (Gemini) for category identification, followed by a dedicated segmentation model (SAM-Audio) for source separation. Concurrently, the Synthesis Data Branch (right) leverages the Scaper toolkit to programmatically generate a large volume of precisely annotated editing scenarios. This hybrid strategy yields a dataset that combines the acoustic fidelity of natural audio with the large-scale diversity needed for robust mode...*

![[assets/figures/papers/audio_omni_siggraph2026_20260622/figures/014_Table.jpg]]
*Table: A3. Detailed results on audio editing tasks. We report FAD/LSD for each task and their average. Table A4. Training data summary across tasks. Table A5. Detailed quantitative results on multimodal generation benchmarks with multiple metrics*

## 方法谱系与知识库定位

### 1. 与前序工作的关系：从工具集成到端到端解耦

Audio-Omni 在音频统一模型谱系中的核心贡献在于**首次将理解、生成与编辑三大能力整合进单一端到端框架**，同时覆盖通用声音、音乐和语音三个域。此前的工作分别走向了三条不同的技术路线：

**统一理解-生成模型**：Ming-Omni 在语音域实现了理解与生成的联合，但其生成能力受限于语音域，且编辑能力缺失。Unified-IO2 和 MuMuLLaMA 尝试跨模态统一，但前者依赖自回归 token 生成，在音频质量上远不及扩散模型（AudioCaps T2A 的 FAD 为 7.81，Audio-Omni 为 1.86）；后者局限于音乐域。这些模型共同面临的问题是：**将生成任务强行塞入自回归语言模型框架，导致音频质量与建模灵活性之间的根本性张力**。

**专有专家模型**：Tango2（文本到音频）、MMAudio（视频到音频）、MusicGen（文本到音乐）、F5-TTS 和 CosyVoice3（语音合成）等在各自领域取得了领先性能，但彼此孤立，无法共享知识或进行跨任务迁移。Audio-Omni 在 T2M 和 TTS 上超越了这些专家模型（MusicGen FAD 3.94 vs Audio-Omni 1.94；F5-TTS WER 1.83 vs Audio-Omni 1.77），表明**统一框架并不必然以牺牲单任务性能为代价**。

**音频编辑模型**：ZETA 和 MMEDIT 代表了基于扩散的编辑方法，但它们的训练数据规模有限且类型单一。Audio-Omni 的 AudioEdit 数据集（超百万样本，覆盖添加、移除、提取和风格迁移四类操作）在规模与多样性上形成了代际差异，直接转化为性能优势（编辑平均 FAD 3.27 vs ZETA 3.81）。

### 2. 核心设计决策的谱系定位

Audio-Omni 的方法论创新可归结为三个相互耦合的设计决策，每个决策都有明确的谱系参照：

**解耦架构（Frozen MLLM + Trainable DiT）**：这一设计直接回应了统一模型中的“生成-理解张力”。冻结的 MLLM（Qwen2.5-Omni-3B）保留了预训练中习得的多模态知识和涌现能力，而 DiT 专注于高质量音频合成。这与工具集成路线（如将多个专家模型通过 API 编排）有本质区别：解耦但端到端训练，使得高层语义信号可以反向传播优化条件表示，而工具集成则完全阻断了这种信号流。

**混合条件机制**：将条件信号分解为高层语义流（MLLM 特征 + 转录文本嵌入，通过交叉注意力注入）和低层信号流（Synchformer 视频同步特征 + 梅尔谱特征，通过噪声拼接注入），这一设计在条件注入策略的谱系中占据独特位置。消融实验（Table 6）表明，这种“语义交叉注意力 + 信号拼接”的组合在所有任务上显著优于其他注入方式（如全部交叉注意力或全部拼接），验证了**不同粒度的条件信息需要不同的注入路径**这一假设。

**MLLM 倒数第二层特征作为条件**：Table 7 的消融表明，使用 MLLM 倒数第二层隐藏状态优于最终层，也优于 CLAP 或 T5 等单模态编码器。这一定位与“中间表示更具泛化性”的表征学习理论一致——最终层可能过度适应预训练任务（如 token 预测），而倒数第二层保留了更丰富的语义结构，为跨任务迁移提供了更好的基础。

### 3. 知识库贡献：AudioEdit 数据集

AudioEdit 数据集的构建管线（Figure 2）代表了音频编辑数据获取方法的重要进展。其混合策略——真实数据分支（从 VGGSound 等数据集中挖掘编辑对，经 Gemini 类别识别和 SAM-Audio 源分离后，CLAP 过滤保留约 50K 高质量对）与合成数据分支（使用 Scaper 程序化生成 150K 添加/移除/提取样本和 500K 风格迁移样本）——解决了此前编辑数据集的两难困境：真实数据保真度高但规模受限，合成数据规模大但存在域差距。

Table 5 的消融实验直接验证了这一策略的必要性：仅使用合成数据训练的编辑 FAD 为 3.80，仅使用真实数据为 2.94，而混合训练降至 2.48。这一定量证据确立了**数据混合作为音频编辑训练的基础性原则**。

### 4. 适用边界与失效模式

Audio-Omni 的能力边界在实验中有明确暴露：

**复杂音频推理的局限**：在 MMAU 推理基准上，Audio-Omni 落后于专有理解模型 Audio Flamingo3 和 Qwen2-Audio-Instruct，甚至落后于统一模型 Ming-Omni。这表明冻结 MLLM 虽然保留了知识，但其推理能力受限于基座模型本身的容量（Qwen2.5-Omni-3B），且生成模块的训练可能并未增强推理能力。

**跨语言性能衰减**：Table A2 揭示了零样本跨语言生成的梯度式退化——英语 FAD 1.86，中文 2.68，法语 4.21。性能与语言距离呈正相关，说明 MLLM 的多语言理解能力虽然存在，但仅用英语训练的生成模块在将非英语语义转化为高质量音频时存在瓶颈。

**计算开销与实时性**：7.9B 总参数量（3.05B 可训练）和 100 步 ODE 推理使得模型难以部署到边缘设备或实时场景。这是 Rectified Flow 类方法的固有局限，与蒸馏或更少步数采样策略的研究方向直接相关。

**编辑粒度的上限**：当前编辑指令以任务类型（添加、移除等）和文本描述为主，缺乏对编辑参数（如时间边界、强度、音色修改量）的细粒度控制。这与基于文本的编辑范式本身的信息带宽限制有关。

### 5. 开放问题与后续工作方向

Audio-Omni 打开的若干问题值得后续工作关注：

1. **解耦架构的跨模态推广**：这种“冻结理解核心 + 可训练生成模块”的设计能否迁移至图像/视频域？关键挑战在于不同模态的生成模块（如视频 DiT）与 MLLM 特征的对齐难度可能存在数量级差异。

2. **多语言生成的帕累托改进**：能否在不损害零样本能力的前提下，通过少量多语言数据微调来压缩跨语言性能差距？这涉及灾难性遗忘与正向迁移之间的权衡。

3. **推理效率的系统性优化**：除蒸馏和减少采样步数外，能否利用 Rectified Flow 的直线路径特性设计更高效的数值求解器？

4. **编辑可控性的维度扩展**：引入空间-时间掩码、强度滑块或参考音频嵌入作为额外的低层信号流，可能在不破坏统一框架的前提下提升编辑精度。

5. **深度伪造风险的结构性缓解**：作者已识别语音转换和编辑技术的滥用风险，并要求用户接受责任条款。但技术层面的水印嵌入和检测方法仍需与生成模型协同设计，而非事后补救。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2026/Audio_Omni_Extending_Multi_modal_Understanding_to_Versatile_Audio_Generation_and_Editing.pdf]]