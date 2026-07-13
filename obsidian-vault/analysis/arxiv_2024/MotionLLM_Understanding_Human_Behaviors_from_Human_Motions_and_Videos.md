---
title: "MotionLLM: Understanding Human Behaviors from Human Motions and Videos"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MotionLLM_Understanding_Human_Behaviors_from_Human_Motions_and_Videos.pdf
project_link: https://lhchen.top/MotionLLM
code_link: https://github.com/Lightning-AI/lit-gpt
aliases:
- MotionLLM
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过构建大规模配对数据集MoVid并采用分离的视觉-语言转换器处理运动与视频模态，实现联合指令微调，融合互补信息。
primary_logic: 将紧凑的运动数据与内容丰富的视频数据进行联合建模，利用大型语言模型的推理能力，通过分离的模态转换器对齐不同模态，并利用大规模生成式指令数据提升细粒度时空理解和推理能力。
claims:
- 在MoVid-Bench运动理解测试中，MotionLLM相比MotionGPT准确率绝对提升12.64%（49.50 vs 36.86）。
- 在MoVid-Bench视频理解测试中，MotionLLM相比Video-LLaVA准确率绝对提升6.47%（49.00 vs 42.53）。
- 联合训练使视频理解整体准确率提升17%，运动理解提升28.6%。
- MoVid数据集包含272k H3DQA指令QA对、200k Motion-XQA指令QA对和24k重标注视频描述。
---

# MotionLLM: Understanding Human Behaviors from Human Motions and Videos

> [!tip] 核心洞察
> 将紧凑的运动数据与内容丰富的视频数据进行联合建模，利用大型语言模型的推理能力，通过分离的模态转换器对齐不同模态，并利用大规模生成式指令数据提升细粒度时空理解和推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionLLM：从人体运动与视频理解人类行为 |
| 英文题名 | MotionLLM: Understanding Human Behaviors from Human Motions and Videos |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2405.20340) · [Project](https://lhchen.top/MotionLLM) · [Code](https://github.com/Lightning-AI/lit-gpt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionLLM |
| Dataset | MoVid-Bench-Motion, MoVid-Bench-Video, MVBench |

> [!tip] 效果简介
> - MoVid-Bench-Motion 上，Accuracy (%) 49.50 vs 36.86 (MotionGPT) (+12.64)。
> - MoVid-Bench-Video 上，Accuracy (%) 49.00 vs 42.53 (Video-LLaVA) (+6.47)。
> - MVBench (human behavior sub-tasks) 上，Avg. Accuracy (%) 31.6 vs 30.0 (VideoChat) (+1.6)。

## 概要

### 问题瓶颈

理解细粒度的人体行为需要同时捕捉运动的时空结构与环境的视觉上下文。然而，现有工作普遍面临一个关键瓶颈：**缺乏高质量的视频-运动-文本配对数据以及对应的指令微调数据**。这导致模型只能在单一模态内运作——运动理解模型（如 **MotionGPT**，Jiang et al., NeurIPS 2023）缺乏视觉场景信息，视频语言模型（如 **Video-LLaVA**，Lin et al., arXiv 2023）又无法获取精确的骨骼运动细节。两个模态长期割裂，限制了联合理解的深度。

### 核心思路

MotionLLM 的核心洞察是：**将紧凑的结构化运动数据与内容丰富的视频数据联合建模，利用大型语言模型的推理能力进行跨模态对齐与融合**。实现这一目标的关键设计是采用**分离的视觉-语言转换器**（分别处理运动和视频模态），而非沿用先前工作中共享转换器的做法。这一设计选择源于运动数据（骨架序列）与视频数据（像素级帧）之间存在较大的模态鸿沟，共享转换器难以有效桥接。

### 方法定位

MotionLLM 属于**多模态大语言模型在人体行为理解领域的延伸**，其架构遵循“视觉编码→模态翻译→大语言模型生成”的范式，但在以下两个关键维度上区别于现有方法：

| 维度 | 基线方法 | MotionLLM |
|------|----------|-----------|
| 视觉-语言转换器 | 共享转换器（如 Video-LLaVA 为图像和视频共用同一投影层） | **分离的运动转换器（线性层）与视频转换器（两层MLP）** |
| 训练数据模态 | 单一模态指令微调（仅运动或仅视频） | **基于 MoVid 数据集的运动-视频联合指令微调** |

在方法谱系中，MotionLLM 可以视为从 **LLaVA**（图像理解）→ **Video-LLaVA**（图像+视频共享转换器）→ **MotionLLM**（运动+视频分离转换器）这一演进路径的最新节点，其本质是将视觉-语言对齐的策略从“缩小模态间隙”推进到“为不同模态定制翻译器”。

### 主要结果

在自建的 **MoVid-Bench** 基准上，MotionLLM 展现出显著的跨模态增益：

- **运动理解**：准确率达 **49.50%**，较 MotionGPT 的 36.86% 绝对提升 **+12.64%**（Table 4）。
- **视频理解**：准确率达 **49.00%**，较 Video-LLaVA 的 42.53% 绝对提升 **+6.47%**（Table 4）。
- **联合训练效益**：引入视频数据使运动理解提升 **28.6%**，引入运动数据使视频理解提升 **17%**（Table 8），验证了双模态互补的有效性。

这些结果表明，通过分离的模态转换器与大规模生成式指令数据，MotionLLM 在细粒度时空理解和推理能力上取得了可观的进步。同时，该工作也揭示了若干局限：视频编码器仅提取 8 帧关键帧，可能遗漏快速动作的时序细节；配对运动-视频数据仅 24k 对且依赖 GPT-4V 标注，存在标注偏差风险；联合训练中的模态知识共享机制尚不明确。这些问题为后续研究指明了方向。

### 问题背景：从人体运动到细粒度行为理解

理解人类行为是计算机视觉与人工智能领域的核心挑战之一。人体运动（human motion）作为行为的直接载体，承载着丰富的时空动态信息；而视频则提供了运动发生的完整环境上下文，包括场景、物体交互和多人关系。然而，现有研究大多将运动与视频视为两条独立的模态轨道：运动理解模型专注于从骨架序列或参数化人体模型中提取动作语义，却忽略了行为发生的物理与社会环境；视频理解模型虽然能够捕捉场景信息，但往往缺乏对细粒度人体姿态、关节运动和时序动态的精确感知能力。

这种模态割裂导致了一个关键瓶颈：**缺乏高质量的视频-运动-文本配对数据以及相应的指令微调数据**，使得现有模型无法同时利用视频和运动模态进行联合理解，从而限制了细粒度人体行为理解的性能上限。以运动理解为例，现有方法如**MotionGPT**（Jiang et al., NeurIPS 2023）仅依赖纯运动数据进行指令微调，在遇到需要环境推理的场景时容易产生幻觉；而在视频理解侧，**Video-LLaVA**（Lin et al., arXiv 2023）等视频大语言模型虽然能够处理视频输入，却无法感知精确的人体姿态变化，导致在方向感知、时序分析等细粒度任务上表现不足。

### 现有方法的缺口

近年来，多模态大语言模型（MLLM）的兴起为视觉理解带来了范式性突破。以LLaVA为代表的工作成功地将图像模态对齐到语言空间，使得大语言模型能够“看懂”图像并进行对话推理。随后，Video-LLaVA、VideoChat（Li et al., arXiv 2023）、VideoChat2（Li et al., CVPR 2024）等工作将这一范式扩展到视频领域，通过共享的视觉-语言（V-L）转换器将视频帧投影到语言空间。

然而，将这些方法直接迁移到人体行为理解场景时，面临两个根本性困难：

1.  **模态鸿沟巨大**：视频与图像之间的模态差距较小，因此Video-LLaVA可以采用统一的V-L转换器同时处理图像和视频。但人体运动数据（通常表示为3D关节序列或离散运动标记）与视频之间存在巨大的模态鸿沟——运动是抽象的时空轨迹，而视频是像素级的视觉信号。共享转换器无法有效弥合这种差异，导致模态对齐质量低下。

2.  **配对指令数据匮乏**：联合理解运动与视频需要成对的运动-视频-文本指令数据，但现有数据集要么仅包含运动-文本对（如HumanML3D、Motion-X），要么仅包含视频-文本对（如Video-ChatGPT指令数据），缺乏将同一行为的运动序列与视频画面关联起来的配对标注。这种数据缺失使得联合训练无从开展。

### 本文动机：联合建模运动与视频

本文的核心洞察在于：**紧凑的运动数据与内容丰富的视频数据具有天然的互补性**。运动数据提供了精确的关节级时空信息，能够准确回答“这个人做了什么动作”、“动作的方向和顺序如何”等问题；视频数据则补充了环境交互信息，能够回答“这个人在什么场景下做动作”、“与周围物体有何关系”等问题。将两者联合建模，有望实现1+1>2的理解能力跃升。

基于这一洞察，本文提出**MotionLLM**——一个能够同时接受人体运动和视频作为输入、利用大语言模型进行细粒度行为理解与推理的统一框架。MotionLLM通过两个关键设计来解决前述缺口：

-   **分离的模态转换器**：针对运动与视频之间的巨大模态鸿沟，MotionLLM采用两个独立的V-L转换器——一个线性层用于运动嵌入投影，一个两层MLP用于视频嵌入投影——分别将不同模态对齐到共享的语言空间，而非强行共享参数。
-   **大规模配对数据集MoVid**：本文构建了包含272k H3DQA指令问答对、200k Motion-XQA指令问答对和24k重标注视频描述的MoVid数据集，首次提供了成对的运动-视频-文本指令数据，使得联合指令微调成为可能。

通过上述设计，MotionLLM旨在实现两大目标：在运动理解上超越纯运动模型（如MotionGPT），在视频理解上超越纯视频模型（如Video-LLaVA），并最终通过联合训练实现跨模态的知识增强。

## 核心方法与创新机理

MotionLLM 的核心创新在于首次将**人体运动（skeleton-based motion）**与**视频（pixel-level video）**两种异构视觉模态联合引入大型语言模型（LLM），并通过**分离的视觉-语言转换器**和**大规模多模态指令微调**实现互补融合，从而显著提升细粒度人体行为理解能力。

### 1. 关键洞察与因果机制

现有视觉-语言大模型（VLLM）通常仅处理图像或视频等像素级视觉输入，而忽略了人体运动这一紧凑、结构化的行为表征。然而，运动数据与视频数据之间存在**巨大的模态鸿沟**——运动是骨架序列的结构化数据，视频是像素级的非结构化数据（见 Figure 3）。共享的视觉-语言转换器（如 **Video-LLaVA**（Lin et al., arXiv 2023））无法有效弥合这一差异。

MotionLLM 的核心洞察在于：**视频提供丰富的环境交互信息，运动提供精确的人体动态信息，两者天然互补**。通过将两种模态分别编码后，经**分离的 V-L 转换器**投影到 LLM 的语言空间，再通过**联合指令微调**让 LLM 学习两种模态的协同推理，模型能够在“发生了什么动作”和“在什么场景下发生”之间建立关联。

这一设计的因果链条为：
1. **分离转换器** → 弥合运动-视频模态鸿沟，避免共享投影层的信息混淆；
2. **联合指令微调** → 强制 LLM 在生成回答时同时关注运动细节与环境上下文；
3. **互补信息融合** → 视频信息补充运动的场景理解，运动信息增强视频的时序精度。

消融实验（Table 8）直接验证了这一因果机制：引入视频数据使运动理解准确率提升 **28.6%**（38.48% → 48.07%）；联合训练使视频理解准确率提升 **17%**（42.53% → 48.94%）。

### 2. 相对基线的关键改动（Changed Slots）

| 设计维度 | 基线方案 | MotionLLM 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| **视觉-语言转换器** | 共享 V-L 转换器（Video-LLaVA 为图像/视频共用同一投影层） | 分离的运动转换器（线性层）与视频转换器（两层 MLP），分别处理骨架运动与像素视频 | Section 3.2, Figure 3 |
| **训练数据模态** | 仅使用单一模态数据（运动或视频）进行指令微调 | 使用配对运动-视频数据（MoVid 数据集）进行联合指令微调 | Section 3.3, Section 4.4 |

#### 2.1 分离的 V-L 转换器设计

MotionLLM 为运动与视频分别设计了独立的 V-L 转换器（Figure 2a, Figure 3c）：
- **运动转换器**：线性层，将 Motion VQ-VAE 编码的离散运动标记投影到语言空间；
- **视频转换器**：两层 MLP，将 Video LanguageBind 编码的视频关键帧嵌入投影到语言空间。

这一设计直接回应了运动数据与视频数据“模态鸿沟较大”的挑战。相比之下，**Video-LLaVA** 采用共享转换器处理图像与视频，其前提是图像-视频模态鸿沟较小——这一假设在引入骨架运动数据时不再成立。

#### 2.2 多模态联合指令微调

MotionLLM 构建了 **MoVid 数据集**（Table 1），包含：
- **272k H3DQA 指令 QA 对**（基于视频-运动-文本三元组）；
- **200k Motion-XQA 指令 QA 对**（基于运动-视频配对数据，由 GPT-4 生成多样化问答）；
- **24k 重标注视频描述**。

在第二阶段（Figure 2b），模型使用上述配对数据同时微调 LLM 和 V-L 转换器，使 LLM 学会在运动与视频信息之间进行跨模态推理。这与 **MotionGPT**（Jiang et al., NeurIPS 2023）仅使用运动-文本数据、**VideoChat**（Li et al., arXiv 2023）/ **VideoChat2**（Li et al., CVPR 2024）仅使用视频-文本数据的做法形成鲜明对比。

### 3. 创新效果验证

联合建模带来的性能增益在 **MoVid-Bench** 上得到充分验证（Table 4）：
- **运动理解**：MotionLLM 达到 **49.50%** 准确率，较 MotionGPT 的 36.86% 绝对提升 **+12.64%**；
- **视频理解**：MotionLLM 达到 **49.00%** 准确率，较 Video-LLaVA 的 42.53% 绝对提升 **+6.47%**。

值得注意的是，这一增益并非简单的多模态堆叠。消融实验（Table 8）表明，当仅使用非配对指令数据（Unpair）时，性能显著下降；而引入配对运动-视频指令数据（Motion-XQA）后，运动理解从 48.07% 进一步提升至 49.50%。这证明**配对数据的跨模态对齐**是性能提升的关键因素。

### 4. 局限与开放问题

尽管分离转换器与联合微调的设计取得了显著效果，但以下问题仍待探索：
- 联合训练中运动与视频模态的知识共享机制尚不明确，模型可能未充分平衡两种模态的信息贡献；
- 视频编码器仅提取 8 帧关键帧，限制了长时序动作的细粒度理解；
- 配对数据规模有限（仅 24k 对），且依赖 GPT-4V 生成标注，可能存在标注偏差；
- 如何将这一多模态架构扩展至运动生成、人机交互等下游任务仍有待研究。

MotionLLM 的整体设计遵循“视觉编码 → 模态翻译 → 语言模型自回归生成”的流水线架构，核心创新在于**分离的视觉-语言（V-L）转换器**与**运动-视频联合指令微调**两阶段训练策略。

### 架构总览

如图2所示，系统接收两类视觉输入：**人体运动序列**或**视频帧**。输入首先经过各自的视觉编码器提取嵌入，再通过独立的V-L转换器投影到大语言模型的语言空间，最终由LLM以自回归方式生成文本回答。整个生成过程可形式化为：

$$\mathbf{z} = F(\mathbf{z}_{l} \mid \mathbf{P}, \mathbf{z}_{<l})$$

其中 $\mathbf{P}$ 为视觉提示（运动或视频嵌入经翻译后的标记），$\mathbf{z}_{<l}$ 为已生成的前缀标记。训练目标为标准的交叉熵损失：

$$\mathcal{L} = -\sum_{\ell=1}^{L} F(\mathbf{z}_{\ell} \mid \mathbf{P}, \mathbf{z}_{<\ell})$$

### 模块组成与数据流

流水线由五个核心模块串联构成：

1. **Motion VQ-VAE Encoder**：将人体运动序列编码为离散标记。该编码器将骨架序列压缩为紧凑的离散表示，保留运动的结构化时空信息。
2. **Video LanguageBind Encoder**：提取视频关键帧的视觉嵌入。实际实现中仅采样8帧关键帧，将其编码为像素级视觉特征。
3. **Motion V-L Translator（线性层）**：将运动嵌入投影到LLM的语言空间。采用简单的线性投影，而非复杂的MLP结构，以适应运动标记与语言标记之间相对直接的映射关系。
4. **Video V-L Translator（两层MLP）**：将视频嵌入投影到LLM的语言空间。使用两层MLP以应对像素级视频特征与语言空间之间更大的语义鸿沟。
5. **LLM（Vicuna-7B）with LoRA**：接收视觉标记与文本指令，自回归生成回答。采用LoRA进行参数高效微调，在保持预训练语言能力的同时适配多模态输入。

### 分离式V-L转换器的设计动机

与LLaVA（仅处理图像）和Video-LLaVA（图像与视频共用统一转换器）不同，MotionLLM采用**分离的运动和视频转换器**。这一设计选择的根本原因在于：运动数据是结构化的骨架序列，而视频数据是像素级的密集信号，两者之间的模态鸿沟远大于图像与视频之间的差异。共享转换器难以同时弥合这两种截然不同的视觉表示到语言空间的映射，因此分离设计是必要的（详见Figure 3的架构对比）。

### 两阶段训练流程

MotionLLM的训练分为两个阶段：

- **第一阶段：模态翻译学习**。冻结视觉编码器和LLM，仅训练V-L转换器。目标是让转换器学会将运动/视频嵌入映射到LLM可理解的语言表示空间，建立初步的模态对齐。
- **第二阶段：运动-视频联合指令微调**。解冻LLM（通过LoRA）和V-L转换器，使用MoVid数据集中的多样化指令QA对进行联合微调。此阶段让模型同时接触运动理解、视频理解以及跨模态推理任务，实现互补信息的融合。

### 输入输出规范

- **输入**：人体运动序列（SMPL-H格式的骨架数据）或视频片段，配以自然语言指令/问题。
- **输出**：关于人体行为的自然语言描述、时空推理答案或分类标签。模型支持开放式生成（如动作描述、行为推理）和闭集分类（如BABEL-QA任务）两种输出模式。

> **注意**：视频编码器仅提取8帧关键帧，这意味着长时序依赖的捕捉能力存在固有限制，后续消融实验也证实了这一点。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/002_Figure_2.jpg]]
*Figure 2: System overview of MotionLLM. (a) MotionLLM takes videos or human motions as visual input V. It first processes the visual input with a vision encoder and translates the vision embeddings into linguistic space via a V-L translator. (b) MotionLLM is trained in two stages. In the first stage, we train the V-L translator to learn the modality translation. In the second stage, we fine-tune the LLM and the V-L translator via instruction tuning data*

### 3.1 自回归生成框架

MotionLLM 将人体行为理解建模为条件自回归生成任务。给定视觉输入 $\mathbf{V}$（可以是人体运动序列或视频帧），模型首先通过视觉编码器将其编码为视觉嵌入，再经视觉-语言（V-L）转换器投影到语言空间，形成视觉提示 $\mathbf{P}$。随后，大型语言模型（LLM）在视觉提示 $\mathbf{P}$ 和已生成文本令牌 $\mathbf{z}_{<l}$ 的条件下，自回归地生成回答序列 $\mathbf{z}$：

$$\mathbf{z} = F(\mathbf{z}_{l} \mid \mathbf{P}, \mathbf{z}_{<l})$$

训练目标采用标准的交叉熵损失，对长度为 $L$ 的文本序列进行优化：

$$\mathcal{L} = -\sum_{\ell=1}^{L} F(\mathbf{z}_{\ell} \mid \mathbf{P}, \mathbf{z}_{<\ell})$$

其中 $F(\cdot)$ 表示 LLM 在给定条件下的令牌预测函数，$\mathbf{z}_{\ell}$ 为第 $\ell$ 个位置的真实令牌。该框架统一了运动和视频两种模态的输入，使 LLM 能够在统一的语言空间中理解和推理人体行为。

### 3.2 分离式视觉-语言转换器设计

MotionLLM 的核心架构创新在于采用**分离的 V-L 转换器**分别处理运动与视频模态。如 Figure 3 所示，现有视觉语言模型（VLLM）通常采用共享的 V-L 转换器处理图像和视频（如 **Video-LLaVA**, Lin et al., arXiv 2023），这依赖于两种模态间较小的语义鸿沟。然而，人体运动数据是结构化的骨架序列数据，与像素级的视频数据存在显著的模态差异。若强行使用共享转换器，会导致模态间信息混淆，损害理解性能。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/003_Figure_3.jpg]]
*Figure 3: Technical comparisons with other VLLMs. (a) LLaVA [38] takes the images as input only. (b) Video-LLaVA [35] shares a unified V-L translator for images and videos due to the small modality gap between the two modalities. (c) To bridge the larger modality gap between motion and videos, we take two separated V-L translators for better modality translations*

因此，MotionLLM 为两种模态分别设计了独立的 V-L 转换器：
- **运动 V-L 转换器**：采用单层线性层，将运动 VQ-VAE 编码器输出的离散运动令牌嵌入直接投影到 LLM 的语言空间。
- **视频 V-L 转换器**：采用两层 MLP，将 Video LanguageBind 编码器提取的视频关键帧嵌入投影到 LLM 的语言空间。

这种分离设计使得每种模态都能学习到最适合自身特性的投影方式，有效弥合了骨架运动数据与像素视频数据之间较大的模态鸿沟（Section 3.2）。

### 3.3 两阶段训练流程

MotionLLM 的训练分为两个阶段（Figure 2b）：

**第一阶段：模态转换学习。** 在此阶段，仅训练 V-L 转换器（运动转换器和视频转换器），LLM 参数保持冻结。训练目标是让转换器学会将视觉嵌入准确映射到 LLM 可理解的语言空间。此阶段使用基础的视频-文本和运动-文本配对数据进行对齐学习。

**第二阶段：运动-视频联合指令微调。** 在第一阶段的基础上，同时微调 V-L 转换器和 LLM 参数（通过 LoRA 进行高效微调）。此阶段引入大规模指令微调数据，包括 MoVid 数据集中的 H3DQA 指令 QA 对（272k）、Motion-XQA 指令 QA 对（200k）以及重标注的视频描述数据（24k）。通过联合指令微调，模型学会融合运动和视频两种模态的互补信息，实现细粒度的时空理解和推理能力。

### 3.4 关键公式与变量说明

| 公式 | 含义 | 变量说明 |
|------|------|----------|
| $\mathbf{z} = F(\mathbf{z}_{l} \mid \mathbf{P}, \mathbf{z}_{<l})$ | 自回归文本生成 | $\mathbf{z}$：生成的文本序列；$\mathbf{P}$：视觉提示（运动或视频嵌入经 V-L 转换器投影后的令牌序列）；$\mathbf{z}_{<l}$：已生成的前 $l-1$ 个令牌 |
| $\mathcal{L} = -\sum_{\ell=1}^{L} F(\mathbf{z}_{\ell} \mid \mathbf{P}, \mathbf{z}_{<\ell})$ | 交叉熵训练损失 | $L$：目标文本序列长度；$\mathbf{z}_{\ell}$：第 $\ell$ 个位置的真实令牌；$F(\cdot)$：LLM 预测的令牌概率分布 |

上述两个公式构成了 MotionLLM 的训练与推理基础。模型在推理时接收运动序列或视频帧作为视觉输入 $\mathbf{V}$，经编码器和 V-L 转换器形成 $\mathbf{P}$，再由 LLM 自回归生成回答。训练时通过最小化交叉熵损失 $\mathcal{L}$ 来优化 V-L 转换器和 LLM 的参数，使生成的文本序列尽可能接近真实答案。

## 实验与关键发现

### 评估协议与实验设置

MotionLLM采用GPT-3.5-turbo作为自动化评估器，通过比较模型生成答案与参考答案，同时给出二值准确率判定和0-5分的语义质量评分。在BABEL-QA基准上，遵循原始设定使用预测准确率进行评估。所有实验均重复三次取平均值，参考答案经过人工标注和验证以确保评估公正性。

模型训练分为两个阶段：第一阶段训练V-L转换器学习模态翻译，第二阶段通过运动-视频联合指令微调同时更新LLM（Vicuna-7B，配合LoRA）和V-L转换器。视频编码器（Video LanguageBind）提取8帧关键帧，运动编码器（Motion VQ-VAE）将运动序列编码为离散标记。

### 主要结果：MoVid-Bench运动与视频理解

**Table 4**（上表）展示了MoVid-Bench运动理解测试的对比结果。MotionLLM在整体准确率上达到**49.50%**，相比运动理解基线模型**MotionGPT**（Jiang et al., NeurIPS 2023）的36.86%，绝对提升**+12.64个百分点**。在身体部位运动感知（Body.）、顺序分析（Seq.）、方向感知（Dir.）和推理（Reas.）四个子维度上，MotionLLM均取得最优结果，尤其在方向感知维度优势显著。

**Table 4**（下表）展示了MoVid-Bench视频理解测试的对比结果。MotionLLM在整体准确率上达到**49.00%**，相比视频语言基线模型**Video-LLaVA**（Lin et al., arXiv 2023）的42.53%，绝对提升**+6.47个百分点**。与**VideoChat**（Li et al., arXiv 2023）、**VideoChat2**（Li et al., CVPR 2024）、**Video-LLaMA**（Zhang et al., arXiv 2023）等视频语言模型相比，MotionLLM在五个评估维度上全面领先。

### 消融实验：模态互补性的量化验证

**Table 8**的消融实验揭示了运动与视频模态联合训练的核心收益：

- **视频对运动理解的增益**：仅使用运动数据训练时，运动理解准确率为38.48%；引入视频数据后提升至48.07%，相对提升**28.6%**。进一步使用成对运动-视频指令数据（Motion-XQA）后，准确率达到最高的49.50%。
- **运动对视频理解的增益**：仅使用视频数据训练时，视频理解准确率为42.53%；联合训练后提升至48.94%，相对提升**17%**。

消融实验还表明，取消视频数据训练会导致模型缺乏环境交互理解，产生幻觉（Table 14, Table 15）。这验证了核心洞察：紧凑的运动数据提供精细的人体骨架动态信息，而视频数据补充环境上下文和物体交互信息，两者通过联合指令微调实现互补融合。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/032_Table_14.jpg]]
*Table 14: Comparison on whether using motion data for hallucinations.The blue text specifically details the woman’s bodily movements, whereas the pink text merely describes hallucinations, which significantly differ from the actual content of the video*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/033_Table_15.jpg]]
*Table 15: Comparison on whether using video data. Video data helps to infer the environment content of the “treadmill” due to the large number of video grounds in training*

### BABEL-QA与MVBench泛化能力

在BABEL-QA闭集分类任务上（Table 5），MotionLLM不经微调（开放词汇生成模式）达到0.372的整体准确率；经BABEL-QA微调后（MotionLLM\*）提升至0.436，与闭集回归专家模型（如MLP和RNN变体）达到可比水平。这证明模型具备一定的跨任务泛化能力，但需注意微调后仍与最优专家模型存在差距。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/010_Table_5.jpg]]
*Table 5: Comparison of different methods on BABEL-QA test set. The “*” denotes finally finetuned on BABEL-QA. “Pred. type” denotes the prediction type, including closed set classification (cls.) and open vocabulary generation (gen.). “-M” and “-R” denote MLP and RNN, respectively. MotionLLM shows comparable performance with close-set regression expert models*

在MVBench的人体行为相关子任务上（Table 6），MotionLLM平均准确率为**31.6%**，略优于VideoChat的30.0%。提升幅度有限（+1.6个百分点），可能受限于视频编码器仅提取8帧关键帧，遗漏了长时序依赖信息。

### 失败模式与局限性

1. **时序信息丢失**：视频编码器仅提取8帧关键帧，在长视频或快速动作场景下可能遗漏细粒度的时序信息，限制了时序理解能力（MVBench提升有限即为佐证）。
2. **配对数据规模瓶颈**：MoVid数据集中成对运动-视频数据仅24k对，且依赖GPT-4V生成标注，可能存在标注偏差。消融实验显示，非成对数据训练的性能明显低于成对数据训练。
3. **模态融合机制不透明**：联合训练时不同模态的知识共享机制尚不明确，模型可能未充分利用环境交互信息。Table 14-15的幻觉现象表明，缺乏视频输入时模型对空间关系和物体交互的推理能力显著下降。
4. **闭集任务泛化不足**：BABEL-QA上不经微调的性能（0.372）与微调后（0.436）差距明显，说明模型在特定领域的闭集分类任务上仍需任务特定适配。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2405_20340/figures/015_Table_8.jpg]]
*Table 8: Ablation studies for modeling different datasets and modalities. The top table is for motion and the bottom table is for video. Unpair refers to using unpaired instruction datasets, including H3DQA, BabelQA, Video-ChatGPT instruction datasets, while Pair means using Motion-XQA to do instruction tuning*

## 定位与知识库关联

### 1. 与现有工作的关系

MotionLLM 处于**多模态大语言模型（MLLM）** 与**人体运动理解**的交叉地带，其设计思路直接承袭自视觉-语言大模型（VLLM）的通用范式，但针对运动-视频-语言三模态对齐问题做出了关键性的架构调整。

#### 1.1 与通用 VLLM 的架构分歧

现有的视频语言模型普遍采用**共享的视觉-语言（V-L）转换器**来处理图像和视频模态。例如 **Video-LLaVA**（Lin et al., arXiv 2023）使用统一的投影层将图像和视频特征映射到语言空间，其设计前提是图像与视频之间的模态差距较小。**LLaVA**（Liu et al., NeurIPS 2023）则仅处理图像输入。MotionLLM 指出，**骨架结构化的运动数据与像素级的视频数据之间存在更大的模态鸿沟**（skeleton-based structural data vs. pixel-level video data），共享的 V-L 转换器已不再是最优选择。因此，MotionLLM 采用**两个分离的 V-L 转换器**——运动模态使用线性层，视频模态使用两层 MLP——分别将运动嵌入和视频嵌入投影到 LLM 的语言空间（Figure 3）。这一设计选择是 MotionLLM 与 Video-LLaVA 等工作的核心架构分歧点。

#### 1.2 与运动理解模型的对比

在运动理解领域，**MotionGPT**（Jiang et al., NeurIPS 2023）是将人体运动与语言进行统一建模的代表性工作，但其仅依赖单一的运动模态进行指令微调，缺乏对视频中环境交互信息的利用。MotionLLM 在 MoVid-Bench 运动理解测试中以 **49.50%** 的准确率显著超越 MotionGPT 的 36.86%，绝对提升 **+12.64 个百分点**（Table 4 top），验证了引入视频模态互补信息的有效性。

在视频理解方面，MotionLLM 与 **VideoChat**（Li et al., arXiv 2023）、**VideoChat2**（Li et al., CVPR 2024）、**Video-LLaMA**（Zhang et al., arXiv 2023）等视频语言模型形成对比。在 MoVid-Bench 视频理解测试中，MotionLLM 以 49.00% 的准确率超过最强基线 Video-LLaVA 的 42.53%（+6.47 个百分点），并在 MVBench 的人体行为子任务上以 31.6% 的平均准确率超过 VideoChat 的 30.0%（Table 6）。这些结果表明，细粒度运动信息的注入能够增强视频理解中的时序推理和方向感知能力。

#### 1.3 在知识库中的定位

MotionLLM 的核心贡献在于**首次构建了视频-运动-文本联合指令微调的完整数据与模型管线**。其知识增量体现在两个层面：

- **数据层面**：构建了 MoVid 数据集，包含 272k H3DQA 指令 QA 对、200k Motion-XQA 指令 QA 对，以及 24k 经 GPT-4V 重标注的视频描述（Table 1），填补了高质量配对数据的空白。
- **方法层面**：通过分离的模态转换器和两阶段训练策略（先训练 V-L 转换器学习模态翻译，再联合微调 LLM 和转换器），实现了运动与视频模态的有效融合。

### 2. 适用边界

MotionLLM 的适用场景主要集中在**需要同时理解人体运动细节和环境上下文的细粒度行为分析任务**，包括但不限于：运动描述生成（motion/video captioning）、时空推理（spatial-temporal reasoning）、方向感知（direction awareness）、身体部位运动感知（body-part motion awareness），以及健身教练等交互式应用（Figure 1b）。

然而，其适用边界受以下因素制约：

- **视频编码器仅提取 8 帧关键帧**，限制了模型对长视频或快速动作的时序捕捉能力，在需要精确帧级理解的场景中可能表现不足。
- **配对运动-视频数据规模有限**（仅 24k 对），且依赖 GPT-4V 生成标注，在需要高度专业化领域知识（如医疗康复动作评估）的场景中可能存在标注偏差。
- 在 **BABEL-QA 等闭集分类任务**上，MotionLLM 以生成式开放词汇方式回答时准确率（0.372）仍低于微调后的版本（0.436）和部分专家模型（Table 5），说明其在需要精确类别判定的任务上仍需任务特定微调。

### 3. 局限与开放问题

#### 3.1 已识别的局限

1. **时序建模深度不足**：视频编码器仅采样 8 帧关键帧，可能遗漏细粒度时序信息。消融实验表明，取消视频数据训练会导致模型缺乏环境交互理解并产生幻觉（Table 14, Table 15），但当前帧数限制可能使这种互补信息未能被充分利用。

2. **数据规模与质量瓶颈**：配对运动-视频指令数据仅 24k 对（Motion-XQA），远小于单模态指令数据规模。GPT-4V 生成的标注可能存在系统性偏差，且人工验证成本高昂。

3. **模态融合机制不透明**：联合训练使运动理解提升 28.6%、视频理解提升 17%（Table 8），但消融实验未深入揭示两种模态在 LLM 内部的知识共享与冲突机制。模型可能在某些场景下过度依赖单一模态而产生模态偏置。

4. **泛化能力有限**：在 BABEL-QA 上需微调才能接近专家模型性能，说明模型在分布外任务上的零样本/少样本泛化能力仍有提升空间。

#### 3.2 开放问题

1. **如何扩大高质量配对数据规模？** 当前 MoVid 的配对数据依赖 GPT-4V 标注，未来能否利用合成数据、自监督对齐或弱监督方法减少对昂贵人工标注和闭源 API 的依赖？

2. **如何设计更强的视频编码器？** 将 8 帧扩展到更密集的采样或引入可学习的时序聚合模块（如 temporal transformer），能否在保持计算效率的同时显著提升长时序理解能力？

3. **联合训练中如何更好地平衡多模态信息？** 是否存在最优的模态混合策略（如动态门控、跨模态注意力正则化）以避免模态偏置，并最大化互补信息的利用效率？

4. **如何将 MotionLLM 扩展至更多下游任务？** 当前工作聚焦于行为理解，但运动-视频-语言的联合表征是否可迁移至运动生成（motion generation）、人机交互（HCI）、运动质量评估等任务，仍需进一步探索。

## 原文 PDF

![[paperPDFs/arxiv_2024/MotionLLM_Understanding_Human_Behaviors_from_Human_Motions_and_Videos.pdf]]
