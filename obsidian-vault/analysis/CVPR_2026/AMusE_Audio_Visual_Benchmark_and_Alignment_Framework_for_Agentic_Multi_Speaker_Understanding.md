---
title: "AMusE: Audio-Visual Benchmark and Alignment Framework for Agentic Multi-Speaker Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AMusE_Audio_Visual_Benchmark_and_Alignment_Framework_for_Agentic_Multi_Speaker_Understanding.pdf
project_link: null
code_link: null
aliases:
- AMusE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入Reflective Reward Optimization (RRO) 和 Selective Reasoning Adaptation (SRA)，通过自反思奖励和选择性参数更新增强模型的多模态对齐和因果推理。
primary_logic: 将多说话人理解任务建模为计划-行动-反思（Plan-Act-Reflect）的agentic流程，并利用内在感知奖励与选择性适配器实现高效且稳定的多模态对齐。
claims:
- RAFT在AMUSE基准上实现最高39.52%的相对准确率提升。
- 集成RAFT后，平均提升+6.7 BLEU、+1.1 METEOR和+6.8 CIDEr。
- 消融实验表明，移除对齐、时间接地或反思优化均导致性能下降，其中反思项贡献最大。
- SRA在仅用LoRA十分之一参数的情况下达到同等或更高性能。
---

# AMusE: Audio-Visual Benchmark and Alignment Framework for Agentic Multi-Speaker Understanding

> [!tip] 核心洞察
> 将多说话人理解任务建模为计划-行动-反思（Plan-Act-Reflect）的agentic流程，并利用内在感知奖励与选择性适配器实现高效且稳定的多模态对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | AMusE: 面向智能体多说话人理解的视听基准与对齐框架 |
| 英文题名 | AMusE: Audio-Visual Benchmark and Alignment Framework for Agentic Multi-Speaker Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.16250) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RAFT |
| Dataset | AMUSE Audio-Visual Dialogue Summarization, AMUSE Audio-Visual Speaker Association, AMUSE Next Speaker Prediction, AMUSE Speaker Re-identification |

> [!tip] 效果简介
> - AMUSE Audio-Visual Dialogue Summarization (AVDS) 上，BLEU 54.54 (Qwen3-Omni + RAFT Agentic) vs 45.08 (Qwen3-Omni Zero-Shot) (+9.46)。
> - AMUSE Audio-Visual Speaker Association (AVSA) 上，Accuracy (%) 54.22 (Qwen3-Omni + RAFT Agentic) vs 47.74 (Qwen3-Omni Zero-Shot) (+6.48)。
> - AMUSE Next Speaker Prediction (NSP) 上，Accuracy (%) 56.73 (Qwen3-Omni + RAFT Agentic) vs 48.38 (Qwen3-Omni Zero-Shot) (+8.35)。

## 概要

**问题瓶颈**：当前多模态大语言模型（MLLMs）在真实多说话人对话场景中缺乏智能体式（agentic）推理能力——难以持续跟踪说话人身份、维持跨轮次角色连续性，以及在时间维度上精确定位事件。现有基准多聚焦于单模态感知任务，未能系统评估模型在重叠说话、身份关联、时序接地和跨场景叙事等方面的综合推理水平。

**核心洞察**：将多说话人理解建模为“计划—行动—反思”（Plan-Act-Reflect）的智能体流程，利用内在感知一致性奖励替代外部偏好标注，并通过选择性参数更新实现高效且稳定的多模态对齐。

**方法定位**：本文提出 **RAFT**（Reasoning Alignment Framework with Reflective Reward and Temporal Grounding），一个面向智能体式多模态推理的训练框架。RAFT 在标准监督微调之上引入三个关键机制：
- **RRO**（Reflective Reward Optimization）：基于同步性、人脸、语音和说话人分离四个感知代理的内在自评估奖励，通过 softmax 加权回归稳定地强化多模态正确性。
- **Temporal Grounding Regularizer**：强制音频、视觉、文本嵌入在时间步上对齐，提升跨模态同步性。
- **SRA**（Selective Reasoning Adaptation）：仅更新负责跨模态推理的参数子集，以约十分之一 LoRA 参数量实现同等或更高性能。

**主要结果**：在 **AMUSE** 基准的六项任务上，RAFT 使开源模型 Qwen3-Omni 在最具挑战性的 Agentic 评估模式下取得显著提升——对话摘要 BLEU 从 45.08 提升至 54.54（+9.46），跨场景叙事链接准确率从 46.07% 提升至 57.26%（+11.19），相对准确率提升最高达 39.52%。消融实验证实，反思优化、对齐损失和时间正则化三者缺一不可，其中反思项对解决多说话人歧义贡献最大；移除音频或视频模态均导致性能大幅下降，表明多说话人推理高度依赖多模态信息。



### 问题背景：多说话人场景中的视听理解困境

现实世界中的多说话人对话——会议、访谈、社交聚会——天然是多模态的：语音信号承载语义与说话人身份，视觉信号提供面部、唇动与空间线索，而文本转录则记录语言内容。人类在这些场景中能够无缝地整合多模态信息，持续跟踪说话人身份、理解对话流、并在时间维度上定位关键事件。然而，当前的多模态大语言模型（MLLMs）在这些能力上存在根本性缺陷。

AMUSE基准的构建揭示了一个核心瓶颈：**现有MLLMs在多说话人、对话中心场景中缺乏agentic reasoning能力，难以跟踪说话人身份、维持角色连续性以及在时间维度上ground事件**。这种缺陷并非源于感知能力的不足——事实上，专用的感知工具（如Whisper进行语音识别、PyAnnote进行说话人分离、InsightFace进行人脸追踪）已经能够提供高质量的底层信号——而是源于模型无法将这些感知信号与结构化推理进行有效整合。

### 现有方法与基准的缺口

表1系统对比了AMUSE与现有多说话人视听基准的差异。先前的基准数据集普遍存在以下局限：

1. **感知与推理的割裂**：现有基准大多聚焦于纯粹的感知任务（如说话人检测、语音识别），缺乏对时序推理、因果推断和身份关联的评估。
2. **缺乏agentic评估范式**：传统评估仅测试模型在给定明确提示下的表现，未考察模型自主规划、调用工具、反思输出的能力。
3. **说话人重叠场景的缺失**：真实对话中普遍存在说话人重叠现象，但多数基准回避了这一挑战。

AMUSE的独特之处在于：**首次在重叠多说话人场景中整合了时序推理、因果推理和基于身份的推理**，将视听感知与结构化推理对齐，以评估模型对多说话人话语的agentic、类人理解能力。

### 评估范式的递进设计

为系统诊断模型能力的边界，AMUSE设计了三种递进难度的评估协议（Figure 2）：

- **Zero-Shot**：模型直接对原始视听输入进行推理，无任何辅助线索。
- **Guided**：模型接收外部工具预处理的结构化信息（人脸裁剪、语音片段、转录文本、唇音同步信号），但仍需自行整合这些线索。
- **Agentic**：最具挑战性的设定——移除所有关于工具可用性或中间步骤的显式提示，模型必须自主发现并调用外部模块（如Whisper、PyAnnote、InsightFace），在推理过程中动态决策。

这种递进设计揭示了关键发现：**当前MLLMs在非agentic和agentic评估下均表现不佳**，即使是GPT-4o等闭源模型，在Agentic设定下也面临显著挑战。这暴露了现有模型在自主规划、工具调用和跨模态信息整合方面的系统性短板。

### 本文动机与RAFT框架的提出

上述缺口指向一个明确的需求：**需要一种能够将多说话人理解任务建模为agentic流程，并通过内在奖励机制实现高效多模态对齐的训练框架**。

RAFT（Reasoning Alignment Framework for Temporal and Multimodal Coherence）正是为此设计。其核心洞察在于：将多说话人理解任务建模为**计划-行动-反思（Plan-Act-Reflect）**的agentic流程，并利用内在感知奖励与选择性适配器实现高效且稳定的多模态对齐。具体而言，RAFT集成两个关键组件：

- **Reflective Reward Optimization (RRO)**：一种基于感知一致性（同步性、人脸匹配、语音匹配、说话人分离）的内在自评估奖励机制，通过自我反思强化多模态和时序正确性。
- **Selective Reasoning Adaptation (SRA)**：一种参数高效的选择性更新策略，仅更新负责跨模态推理的参数层，在数据效率和参数效率之间取得平衡。

实验表明，RAFT在AMUSE基准上实现最高**39.52%的相对准确率提升**，并在全部六个任务上一致优于PPO、DPO和GRPO等主流优化方法，验证了agentic对齐范式在多说话人理解中的有效性。



## 核心方法与创新机理

AMusE的核心创新在于将多说话人理解任务重新建模为**计划-行动-反思（Plan-Act-Reflect）的agentic流程**，并通过RAFT框架引入三项关键机制来突破现有MLLM在身份追踪、时序接地和因果推理上的瓶颈。

### 从被动感知到主动推理的范式转变

现有MLLM在多说话人场景中本质上是**被动感知器**：它们接收原始视听输入，但缺乏主动调用感知工具、维持角色连续性和在时间维度上精确接地事件的能力。RAFT将这一过程重构为agentic循环——模型自主规划需要调用哪些感知工具（Whisper、PyAnnote、InsightFace、SyncNet），执行工具调用获取多模态线索，最后反思输出与感知信号之间的一致性。这一范式转变的因果机制在于：**当模型被迫显式地推理“谁在何时说了什么”时，它不再依赖模糊的统计关联，而是建立可验证的感知-语义绑定**。

### 三项关键机制设计

**1. 内在感知奖励替代外部偏好信号（changed slot: 奖励机制）**

传统RLHF方法（PPO、DPO）依赖外部奖励模型或人类偏好标注，在多说话人场景中面临标注成本高、奖励信号稀疏的问题。RRO的核心突破在于**利用四个感知代理的内在一致性得分作为自评估奖励**：

$$r_i = \mathcal{R}(x_i, y_i) = f_{\mathrm{perceptual}}(\mathrm{Sync}, \mathrm{Face}, \mathrm{Speech}, \mathrm{Diarization})$$

这些代理分别评估音视频同步、人脸匹配、语音识别和说话人分离的质量，无需人工标注即可提供稠密的反馈信号。通过softmax加权回归更新策略：

$$\nabla_\theta J_{\mathrm{RRO}} = \sum_{i=1}^{K} w_i \nabla_\theta \log \pi_\theta(y_i | x), \quad w_i = \frac{\exp(\beta(r_i - \bar{r}))}{\sum_j \exp(\beta(r_j - \bar{r}))}$$

这种设计的因果优势在于：当模型错误地将话语归因于错误说话人时，说话人分离代理会给出低分，直接抑制该输出的概率，形成**自纠正闭环**。消融实验证实，移除反思优化导致性能下降最为显著（Figure 6），验证了感知奖励是RAFT中最关键的组件。

**2. 选择性参数更新实现高效对齐（changed slot: 参数更新策略）**

全参数微调或全层LoRA在多模态对齐中存在两个问题：计算开销大，且容易破坏预训练的基础语言能力。SRA的解决方案是**仅更新负责跨模态推理的参数子集**：

$$\tilde{\nabla}_{\theta_i} \mathcal{L} = \begin{cases} \nabla_{\theta_i} \mathcal{L}, & \theta_i \in \theta_{\mathrm{cross}}, \\ 0, & \theta_i \in \theta_{\mathrm{base}}. \end{cases}$$

实验表明，SRA在仅使用LoRA十分之一参数的情况下达到同等或更高性能（Table 15, Figure 10）。这一效率提升的机制在于：多说话人理解的核心困难集中在跨模态绑定（谁的声音对应哪张脸），而非基础的语言生成或视觉识别。冻结基础参数保留了预训练能力，同时集中有限的计算资源攻克真正的瓶颈。

**3. 时间一致性正则化强制跨模态同步（changed slot: 训练损失函数）**

RAFT总损失将结构化对齐、时间一致性和反思奖励统一为单一优化目标：

$$\mathcal{L}_{\mathtt{RAFT}} = \mathcal{L}_{\mathrm{align}} + \alpha \mathcal{L}_{\mathrm{temp}} - \beta J_{\mathtt{RRO}}$$

其中时间一致性损失显式惩罚音频、视觉、文本嵌入在时间维度上的错位：

$$\mathcal{L}_{\mathrm{temp}} = \sum_t \left( \| f_a(t) - f_v(t) \|_2^2 + \gamma \| f_t(t) - f_r(t) \|_2^2 \right)$$

这一设计的必要性在于：多说话人场景中，仅靠内容对齐无法解决“同一时刻多人说话”的歧义。时间正则化强制模型在嵌入空间中将同时发生的视听事件拉近，将时序错位的事件推远，从而在表示层面建立跨模态同步的先验。

### 与现有优化方法的本质差异

与PPO、DPO、GRPO等方法的对比实验（Table 19）表明，RAFT在全部六个AMUSE任务上均取得最优性能。差异根源在于：PPO/DPO依赖外部偏好信号，在多说话人场景中难以定义全局的“好回答”；GRPO虽引入组内相对比较，但仍缺乏对感知一致性的直接约束。RRO通过感知代理提供**可解释、可归因的细粒度反馈**，使模型明确知道错误来源（是认错了人还是搞混了时间），而非仅接收一个整体评分。



RAFT 的整体流程围绕“计划—行动—反思”（Plan–Act–Reflect）的代理式推理循环构建，将多说话人视听理解显式分解为三个顺序阶段，并在训练时引入内在感知奖励与选择性参数适配，形成端到端对齐框架。

### 输入与输出定义

框架的输入为多模态流 $x := \{x^{(a)}, x^{(v)}, x^{(t)}\}$，分别代表音频、视频和文本模态。输出为结构化响应 $y = \{p, a, r\}$，对应 Plan（计划）、Act（行动）、Reflect（反思）三个推理阶段。其中：

- **Plan**：模型根据任务目标和多模态输入，自主决定需要调用哪些感知工具（如 Whisper 进行语音识别、PyAnnote 进行说话人分离、InsightFace 进行人脸跟踪、SyncNet 进行音画同步检测），并制定推理步骤。
- **Act**：执行计划中确定的工具调用，获取结构化感知线索，并将这些线索与原始多模态输入融合，生成中间推理结果。
- **Reflect**：基于感知一致性反馈对 Act 阶段的输出进行自评估和修正，确保说话人身份、时间接地和跨模态同步的正确性。

### 核心模块关系

RAFT 由四个相互协作的模块构成，其关系如图 3 所示：

1. **Structured Reasoning Alignment（结构化推理对齐）**  
   通过负对数似然损失强制模型按照 Plan–Act–Reflect 的顺序生成，维持上下文一致性。该模块是框架的基础对齐机制，其损失函数为：
   $$\mathcal{L}_{\mathrm{align}}(x, y) = -\log \pi_{\theta}(y \mid x)$$
   该损失直接作用于目标响应 $y$ 的条件概率，确保推理阶段的格式和内容均符合预期。

2. **Perceptual Reward（感知奖励）**  
   框架引入四个感知代理——同步（Sync）、人脸（Face）、语音（Speech）、说话人分离（Diarization）——对模型输出进行一致性评分，聚合为内在奖励：
   $$r_i = \mathcal{R}(x_i, y_i) = f_{\mathrm{perceptual}}(\mathrm{Sync}, \mathrm{Face}, \mathrm{Speech}, \mathrm{Diarization})$$
   该奖励无需外部标注或人类偏好，完全基于多模态感知一致性自动计算，是 RRO 的核心驱动力。

3. **Reflective Reward Optimization（RRO，反思奖励优化）**  
   RRO 利用 softmax 加权回归，根据感知奖励调整模型输出分布，强化多模态正确性。其梯度更新形式为：
   $$\nabla_{\theta} J_{\mathrm{RRO}} = \sum_{i=1}^{K} w_i \nabla_{\theta} \log \pi_{\theta}(y_i | x), \quad w_i = \frac{\exp(\beta(r_i - \bar{r}))}{\sum_{j} \exp(\beta(r_j - \bar{r}))}$$
   其中 $\beta$ 为温度参数，控制奖励信号的锐度。该机制使模型在训练过程中逐步偏向高感知一致性的生成，从而在推理阶段隐式内化反思能力。

4. **Temporal Grounding Regularizer（时间接地正则化）**  
   为强制跨模态同步，框架在每个时间步上最小化音频、视觉和文本嵌入的不一致性：
   $$\mathcal{L}_{\mathrm{temp}} = \sum_{t} \left( \| f_a(t) - f_v(t) \|_2^2 + \gamma \| f_t(t) - f_r(t) \|_2^2 \right)$$
   该正则项确保模型对“谁在何时说了什么”的时空绑定保持敏感，是解决多说话人场景中身份混淆的关键约束。

### 训练总目标与参数策略

RAFT 的最终训练目标将上述模块统一为：
$$\mathcal{L}_{\mathrm{RAFT}} = \mathcal{L}_{\mathrm{align}} + \alpha \mathcal{L}_{\mathrm{temp}} - \beta J_{\mathrm{RRO}}$$
其中 $\alpha$ 和 $\beta$ 为平衡系数。训练时，框架采用 **Selective Reasoning Adaptation（SRA）** 策略：仅更新负责跨模态推理的参数 $\theta_{\mathrm{cross}}$，冻结基础模型参数 $\theta_{\mathrm{base}}$。梯度掩码形式为：
$$\tilde{\nabla}_{\theta_i} \mathcal{L} = \begin{cases} \nabla_{\theta_i} \mathcal{L}, & \theta_i \in \theta_{\mathrm{cross}}, \\ 0, & \theta_i \in \theta_{\mathrm{base}}. \end{cases}$$
这一设计使得 SRA 在使用比全层 LoRA 少一个数量级参数的情况下仍能达到同等或更高性能（见 Table 15 / Figure 10），实现了数据和参数双重高效的对齐。

### 推理模式

RAFT 支持三种递进的评估协议（见图 2）：Zero-Shot（仅原始输入）、Guided（提供外部工具输出的结构化线索）和 Agentic（模型自主发现并调用工具）。Agentic 模式是最具挑战性的设置——模型需隐式学习工具选择策略，在无任何显式提示的情况下完成 Plan–Act–Reflect 循环。消融实验表明，工具选择正确率是 Agentic 性能的关键瓶颈（见 Table 17），而 RAFT 的反思机制正是缓解这一瓶颈的核心手段。

### 补充图表

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/005_Figure_3.jpg]]
*Figure 3: RAFT framework for agentic multimodal reasoning. Given a dialogue-rich video, the model uses perception tools to extract multimodal cues. RAFT integrates SRA and RRO within a Reason–Act–Feedback loop, using perceptual consistency to refine temporal and speaker-grounded responses. RAFT ( ) module operates only during training. Dotted arrow shows that RRO passively uses perceptual feedback for reward computation rather than active control of the tools*



RAFT 框架将多说话人理解建模为 **计划-行动-反思（Plan-Act-Reflect）** 的 agentic 流程，并通过四个核心模块实现多模态对齐与因果推理：结构化推理对齐、反思奖励优化、时间接地正则化、选择性推理适配。

### 4.1 问题形式化与优化目标

给定对话视频，输入为多模态流 $x := \{x^{(a)}, x^{(v)}, x^{(t)}\}$，分别表示音频、视频和文本。模型需生成结构化响应 $y = \{p, a, r\}$，对应计划（Plan）、行动（Act）和反思（Reflect）三个阶段。RAFT 的优化目标是在最大化奖励与保持对齐之间寻求平衡：

$$\theta' = \arg\max_{\theta} \mathbb{E}_{(x,y)\sim\mathcal{D}} [\mathcal{R}(x, y) - \lambda \mathcal{L}_{\mathrm{align}}(x, y)] \quad \text{(Eq. 4.1)}$$

其中 $\mathcal{R}(x, y)$ 为内在感知奖励，$\mathcal{L}_{\mathrm{align}}$ 为结构化对齐损失，$\lambda$ 控制二者的权衡。

### 4.2 结构化推理对齐（Structured Reasoning Alignment）

该模块强制模型按照 Plan→Act→Reflect 的顺序生成，并保持上下文一致性。其损失函数为对目标响应 $y$ 的负对数似然：

$$\mathcal{L}_{\mathrm{align}}(x, y) = -\log \pi_{\theta}(y \mid x) \quad \text{(Eq. 4.2)}$$

通过优化该损失，模型学习在给定多模态输入下生成符合推理阶段结构的响应序列，确保计划、行动和反思三个环节的因果连贯性。

### 4.3 反思奖励优化（Reflective Reward Optimization, RRO）

RRO 是 RAFT 的核心创新。不同于依赖外部奖励模型或人类偏好的传统 RLHF 方法，RRO 引入基于感知一致性的内在自评估奖励。奖励函数聚合四个感知代理的一致性得分：

$$r_i = \mathcal{R}(x_i, y_i) = f_{\mathrm{perceptual}}(\mathrm{Sync}, \mathrm{Face}, \mathrm{Speech}, \mathrm{Diarization}) \quad \text{(Eq. 4.3)}$$

其中四个维度分别衡量：**Sync**（音画同步）、**Face**（人脸匹配）、**Speech**（语音识别正确性）、**Diarization**（说话人分离准确性）。

为稳定策略更新，RRO 采用 softmax 加权回归，根据奖励的相对大小调整各样本的更新权重：

$$\nabla_{\theta} J_{\mathrm{RRO}} = \sum_{i=1}^{K} w_i \nabla_{\theta} \log \pi_{\theta}(y_i | x), \quad w_i = \frac{\exp(\beta(r_i - \bar{r}))}{\sum_j \exp(\beta(r_j - \bar{r}))} \quad \text{(Eq. 4.4)}$$

其中 $\beta$ 为温度系数，控制奖励差异的放大程度；$\bar{r}$ 为批次内平均奖励。该机制使模型更关注感知一致性高的生成结果，从而强化多模态正确性。

### 4.4 时间接地正则化（Temporal Grounding Regularizer）

多说话人场景要求模型在时间维度上精确对齐音频、视觉和文本信息。时间一致性损失通过最小化各模态嵌入在时间步上的差异来实现：

$$\mathcal{L}_{\mathrm{temp}} = \sum_t \left( \|f_a(t) - f_v(t)\|_2^2 + \gamma \|f_t(t) - f_r(t)\|_2^2 \right) \quad \text{(Eq. 4.5)}$$

其中 $f_a(t)$、$f_v(t)$ 分别为音频和视觉特征在时间 $t$ 的嵌入，$f_t(t)$、$f_r(t)$ 为文本和推理特征嵌入，$\gamma$ 平衡两项的贡献。该正则化强制跨模态同步，减少时序错位导致的说话人混淆。

### 4.5 RAFT 总损失与选择性推理适配（SRA）

RAFT 的最终训练目标为上述三个模块的组合：

$$\mathcal{L}_{\mathrm{RAFT}} = \mathcal{L}_{\mathrm{align}} + \alpha \mathcal{L}_{\mathrm{temp}} - \beta J_{\mathrm{RRO}} \quad \text{(Eq. 4.6)}$$

其中 $\alpha$ 和 $\beta$ 分别控制时间正则化和反思奖励的权重。

在参数更新策略上，SRA 仅更新负责跨模态推理的参数子集 $\theta_{\mathrm{cross}}$，而冻结基础模型参数 $\theta_{\mathrm{base}}$：

$$\tilde{\nabla}_{\theta_i} \mathcal{L} = \begin{cases} \nabla_{\theta_i} \mathcal{L}, & \theta_i \in \theta_{\mathrm{cross}}, \\ 0, & \theta_i \in \theta_{\mathrm{base}}. \end{cases}$$

这一选择性梯度掩码机制使 RAFT 在仅使用 LoRA 十分之一参数量的情况下实现同等或更高性能，显著提升了数据和参数效率。

### 关键机制总结

| 模块 | 核心作用 | 关键公式 |
|------|---------|---------|
| 结构化对齐 | 强制 Plan-Act-Reflect 推理顺序 | Eq. 4.2 |
| RRO | 自评估感知奖励驱动稳定策略更新 | Eq. 4.3, 4.4 |
| 时间接地 | 最小化跨模态时序不一致性 | Eq. 4.5 |
| SRA | 选择性参数更新实现高效对齐 | 梯度掩码 |

消融实验（Figure 6）证实，移除任一模块均导致性能下降，其中 RRO 的反思项对解决多说话人歧义贡献最大。与 PPO、DPO、GRPO 等优化方法的对比（Table 19）进一步表明，RAFT 在所有六个 AMUSE 任务上均取得更优性能，验证了内在感知奖励与选择性适配器组合的有效性。



## 实验与关键发现

### 整体性能提升

RAFT在AMUSE基准的六个任务上为开源多模态大语言模型带来了显著且一致的性能增益。以**Qwen3-Omni-7B**为例，在Agentic评估模式下集成RAFT后，各任务指标均有大幅跃升：

- **Audio-Visual Dialogue Summarization (AVDS)**：BLEU从Zero-Shot的45.08提升至54.54（+9.46），相对提升约21%（Table 3）。
- **Audio-Visual Speaker Association (AVSA)**：准确率从47.74%提升至54.22%（+6.48）（Table 4）。
- **Next Speaker Prediction (NSP)**：准确率从48.38%提升至56.73%（+8.35）（Table 4）。
- **Speaker Re-identification (SRID)**：准确率从56.98%提升至62.53%（+5.55）（Table 4）。
- **Speaker Temporal Grounding (STG)**：Temporal IoU从48.56提升至54.04（+5.48）（Table 5）。
- **Cross-scene Narrative Linking (CSNL)**：准确率从46.07%提升至57.26%（+11.19），人类评判的连贯性得分从5.82提升至7.11（Table 5）。

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/006_Table_3.jpg]]
*Table 3: Audio-Visual Dialogue Summarization results. While closed-source models such as GPT-4o achieve strong zero-shot and guided performance, open-source MLLMs benefit substantially from RAFT training*

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/007_Table_4.jpg]]
*Table 4: Performance comparison on AV Speaker Association, Next Speaker Prediction, and Speaker Re-identification tasks. Consistent performance gains for Qwen-based models after RAFT fine-tuning. Agt w/R: Agentic evaluation with RAFT finetuning*

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/008_Table_5.jpg]]
*Table 5: Performance on Speaker Temporal Grounding and Cross-scene Narrative Linking tasks. Human-Judged Coherence is scaled between 0-10. RAFT yields substantial gains in temporal precision and narrative coherence, especially for open-source MLLMs such as Qwen3-Omni. Ag w/R: Agentic evaluation with RAFT finetuning*

论文在Introduction中声称的“最高39.52%相对准确率提升”指向的是某些具体模型-任务组合下的相对增益（例如CSNL任务上Qwen3-Omni从46.07%到57.26%，相对提升约24.3%；更小的基线模型可能获得更大的相对提升）。整体而言，RAFT对开源模型的赋能效果尤为突出，使其在多个任务上逼近甚至超越闭源模型**GPT-4o**的Zero-Shot/Guided表现。

### 消融实验：RAFT各组件的贡献

在AVDS任务上对RAFT进行组件消融（Figure 6），揭示了各模块的独立贡献：

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/011_Figure_6.jpg]]
*Figure 6: Ablation analysis of RAFT on AVDS. (a) Removing core objectives degrades performance across models (b) Highlights stage-wise gains*

1. **移除反思优化（RRO）**：性能下降最为显著，表明基于感知一致性的自反思奖励是解决多说话人歧义的核心驱动力。
2. **移除结构化对齐（Alignment）**：模型失去按“计划-行动-反思”阶段生成的能力，输出质量和一致性明显退化。
3. **移除时间接地正则化（Temporal Grounding）**：跨模态时间同步性减弱，影响说话人关联和事件定位精度。

三者联合移除时性能降至接近Zero-Shot基线水平，验证了RAFT总损失函数 $\mathcal{L}_{\mathtt{RAFT}} = \mathcal{L}_{\mathrm{align}} + \alpha \mathcal{L}_{\mathrm{temp}} - \beta J_{\mathtt{RRO}}$ 中各组件不可替代的协同作用。

### 参数效率：SRA vs LoRA

**Selective Reasoning Adaptation (SRA)** 的核心设计是仅更新跨模态推理层的参数，冻结基础骨干网络。实验表明：

- 在Qwen3-Omni上，SRA仅使用LoRA十分之一的可训练参数量，即达到同等或更高的AMUSE平均得分（Table 15 / Figure 10）。
- 参数效率曲线（Figure 10）显示，SRA在极低参数预算下即迅速收敛至高性能区间，而LoRA需要更大的参数规模才能匹配。

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/024_Table_15.jpg]]
*Table 15: Performance vs. trainable parameter budget. SRA matches or exceeds LoRA with an order of magnitude fewer parameters*

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/025_Figure_10.jpg]]
*Figure 10: Average AMUSE score vs. fraction of trainable parameters for LoRA and SRA on Qwen3-Omni. RAFT with SRA achieves higher performance at significantly lower parameter budgets*

这一结果验证了选择性梯度掩码策略 $\tilde{\nabla}_{\theta_i} \mathcal{L}$ 的有效性——多说话人推理能力的提升并不需要对整个模型进行全参数或全层微调，精准更新跨模态交互层即可实现高效对齐。

### 模态消融：多模态依赖的刚性

移除音频或视频模态会导致AMUSE性能大幅下降（Table 18 / Figure 13），证实多说话人推理对多模态信息存在刚性依赖。具体而言：

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/030_Table_18.jpg]]
*Table 18: Cue ablation on AMUSE (average score across tasks)*

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/031_Figure_13.jpg]]
*Figure 13: Effect of removing modalities and cues on average AMUSE performance. Multi-speaker reasoning is strongly multimodal*

- 仅使用音频或仅使用视频时，说话人关联、重识别和时间接地任务均严重退化。
- 在Agentic模式下，模型需要自主调用Whisper、PyAnnote、InsightFace、SyncNet等感知工具（Table 17），工具选择正确率直接影响最终性能。RAFT训练后模型在工具选择和感知线索整合上表现出更强的自主性。

### 说话人重叠的挑战

AMUSE数据集包含显著的说话人重叠比例（Figure 8左图），这构成了对RAFT训练后模型的主要挑战。随着重叠比例增加，模型性能持续下降（Figure 11），表明即使在RAFT对齐后，处理多人同时发言的场景仍是瓶颈。可见说话人数量增加同样导致AVSA和NSP准确率下降（Figure 12），场景越拥挤，身份跟踪和下一说话人预测越困难。

### 与主流优化方法的对比

RAFT在全部六个AMUSE任务上均优于**PPO**（Schulman et al., 2017）、**DPO**（Rafailov et al., 2023）和**GRPO**（Shao et al., 2024）等主流对齐优化方法（Table 19）。在STG任务上的Agentic性能对比（Figure 5）进一步显示，RAFT的感知奖励机制和选择性参数更新策略在多模态、多说话人场景下比通用RLHF方法更具优势。

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/032_Table_19.jpg]]
*Table 19: Comparison of RAFT with PPO, DPO, and GRPO across AMUSE tasks on Qwen3-Omni. We report task-specific metrics. B@4: BLEU score*

### 补充图表

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/004_Figure_2.jpg]]
*Figure 2: Evaluation Protocols. Zero-Shot, Guided, and Agentic where MLLMs reason over raw input, use auxiliary cues (e.g., faces, transcripts), or invoke external tools (e.g., Whisper, Pyannote, InsightFace)*

![[assets/figures/papers/paper_list_l813_https_arxiv_org_abs_2512_16250/figures/002_Table_1.jpg]]
*Table 1: Comparison of multi-speaker audio-visual benchmarks. AMUSE uniquely integrates temporal, causal, and identitybased reasoning within overlapping multi-speaker settings. Unlike prior datasets focused on perception-only tasks, AMUSE aligns audio-visual perception with structured reasoning to benchmark agentic, human-like understanding of multi-party discourse*



## 定位与知识库关联

### 1. 问题定位：从多模态感知到Agentic多说话人推理

AMUSE与RAFT的核心瓶颈在于：当前多模态大语言模型（MLLM）在多说话人、对话中心场景中缺乏**agentic reasoning能力**——难以稳定跟踪说话人身份、维持角色在时间维度上的连续性，以及在跨场景叙事中进行因果关联。这一瓶颈的根源并非感知能力的不足，而是现有模型缺乏将多模态感知信号与结构化推理过程对齐的机制。

与现有基准的差异体现在Table 1：此前的主流多说话人视听数据集集中于感知层面任务（如说话人检测、语音分离），而AMUSE首次将**时间推理、因果推理和身份推理**统一纳入重叠多说话人场景的评估框架。这一设计使得AMUSE不仅衡量模型“听到什么”，更衡量模型“理解谁在何时对谁说了什么、以及为什么”。

### 2. 方法谱系：RAFT在优化方法空间中的位置

RAFT的核心技术贡献在于提出了一种**内在奖励驱动、选择性参数更新**的多模态对齐框架。为理解其方法学定位，需从三个关键设计维度展开：

#### 2.1 奖励机制：从外部偏好到内在感知一致性

传统RLHF方法（如**PPO**（Schulman et al., 2017）、**DPO**（Rafailov et al., 2023））依赖外部奖励模型或人类偏好标注来引导策略优化。**GRPO**（Shao et al., 2024）进一步引入了组相对策略优化。然而，在多说话人场景中，人类偏好难以精细刻画跨模态同步性、人脸-语音匹配度、说话人分离质量等感知维度的正确性。

RAFT的**Reflective Reward Optimization（RRO）**改变了这一范式：奖励信号由四个感知代理（同步检测、人脸识别、语音匹配、说话人分离）的内在一致性得分聚合而成（Eq. 4.3）。这一设计使奖励函数直接扎根于多模态信号的物理一致性，而非外部标注者的主观判断。消融实验（Figure 6）表明，移除反思优化项导致性能下降最为显著，验证了内在感知奖励在多说话人歧义消解中的关键作用。

#### 2.2 参数更新策略：从全量微调到选择性跨模态适配

主流参数高效微调方法（如全层LoRA）通常对所有层施加低秩适配。RAFT的**Selective Reasoning Adaptation（SRA）**采取了更激进的策略：仅更新负责跨模态推理的参数子集$\theta_{\mathrm{cross}}$，保持基础编码器参数$\theta_{\mathrm{base}}$完全冻结（Appendix C.2选择性梯度掩码）。

这一设计的因果逻辑在于：多说话人推理的瓶颈并非视觉或语音特征的提取质量，而是跨模态信息的融合与推理过程。Table 15和Figure 10的实验证据直接支持这一假设——SRA在使用LoRA十分之一参数量的情况下，实现了同等或更高的AMUSE平均得分。这意味着**参数效率的提升源于对问题结构的准确建模**，而非简单的低秩近似技巧。

#### 2.3 训练目标：结构化对齐与时间一致性正则

RAFT的总损失函数（Eq. 4.6）由三项构成：
- **结构化对齐损失**$\mathcal{L}_{\mathrm{align}}$（Eq. 4.2）：强制模型按“计划-行动-反思”的agentic阶段生成响应，确保推理过程的可追溯性；
- **时间一致性正则项**$\mathcal{L}_{\mathrm{temp}}$（Eq. 4.5）：在音频、视觉、文本嵌入的每个时间步上施加L2对齐约束，抑制跨模态漂移；
- **RRO奖励项**$J_{\mathrm{RRO}}$（Eq. 4.4）：通过softmax加权回归，根据感知奖励的高低调整生成策略的更新幅度，使高奖励响应获得更大梯度权重。

三项之间存在明确的因果分工：结构化对齐保证推理格式正确，时间正则保证跨模态同步，RRO保证内容质量。消融实验（Figure 6a）显示，移除任一项均导致性能下降，验证了三者的互补性。

### 3. 与基线方法的关系与适用边界

#### 3.1 对比基线体系

AMUSE的评估覆盖了三类基线：
- **闭源MLLM**：GPT-4o、GPT-4o Mini、REKA——代表当前性能上限；
- **开源MLLM**：Unified-IO2-5B、CREMA、Video-SALMONN、VITA-8B、Qwen2.5-Omni-7B、Qwen3-Omni-7B——代表可复现的基线水平；
- **优化方法**：PPO、DPO、GRPO——代表RAFT的替代训练方案。

实验结果表明（Table 19），RAFT在全部六个AMUSE任务上均优于PPO、DPO和GRPO。这一优势的根源在于：通用RLHF方法优化的是“人类偏好”这一抽象目标，而RAFT优化的是“多模态感知一致性”这一可分解、可自评估的具体目标。在多说话人场景中，后者与任务成功率的因果关系更为直接。

#### 3.2 适用边界与局限

RAFT的性能边界受以下因素制约：

**说话人重叠比例**。Figure 11显示，随着重叠比例增加，即使RAFT训练后的模型性能也显著下降。这表明当前框架在处理高度重叠语音（如三人以上同时发言）时仍存在根本性困难，可能需要更强的语音分离前端或更精细的时间注意力机制。

**可见说话人数量**。Figure 12表明，当场景中可见说话人增多时，AVSA和NSP任务的准确率下降。这一趋势反映了视觉拥挤对身份跟踪的干扰——SRA虽然高效，但可能未充分建模多人场景下的视觉注意力分配。

**模态依赖性**。Table 18和Figure 13的模态消融实验揭示了多说话人推理的强多模态特性：移除音频或视频模态均导致性能大幅下降。这意味着RAFT框架难以在单一模态缺失的场景中保持鲁棒性，限制了其在纯音频会议或纯视频监控等场景中的直接应用。

**工具选择正确率**。Table 17显示，在Agentic模式下，模型的工具选择正确率并非100%。这表明“何时调用何种感知工具”的元决策能力仍有提升空间，当前的Plan-Act-Reflect流程可能在复杂场景中产生级联错误。

### 4. 开放问题

基于以上分析，存在以下值得进一步探索的方向：

1. **内在奖励的可扩展性**：当前RRO的感知代理（同步、人脸、语音、说话人分离）覆盖了视听一致性的主要维度，但未包含语义一致性、情感一致性等更高层次的评估。如何在不引入外部标注的前提下扩展内在奖励的维度，是一个开放问题。

2. **SRA的跨架构泛化**：SRA在Qwen系列模型上验证了参数效率优势，但其对跨模态参数子集的识别依赖于特定的架构设计。在更异构的多模态架构（如非Transformer融合层）中，如何自动识别应更新的参数子集，需要进一步研究。

3. **重叠语音的根本性处理**：当前框架将重叠语音的挑战留给感知工具和模型推理共同承担，但Figure 11表明这一策略存在上限。是否需要将语音分离作为可微分模块嵌入训练流程，而非作为黑盒工具调用，是一个架构层面的开放选择。

4. **长程跨场景叙事**：CSNL任务涉及跨视频片段的叙事链接，当前RAFT主要依赖单片段内的时序建模。对于需要跨多个对话场景进行人物关系推理的复杂叙事，是否需要引入外部记忆机制或图结构推理，值得探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/AMusE_Audio_Visual_Benchmark_and_Alignment_Framework_for_Agentic_Multi_Speaker_Understanding.pdf]]
