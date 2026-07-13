---
title: "UniLS: End-to-End Audio-Driven Avatars for Unified Listening and Speaking"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniLS_End_to_End_Audio_Driven_Avatars_for_Unified_Listening_and_Speaking.pdf
project_link: null
code_link: null
aliases:
- UniLS
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 两阶段训练策略：阶段1首先通过无音频的自回归生成器学习内部运动先验（如眨眼、微表情等自发行为）；阶段2再引入双轨音频，以交叉注意力和LoRA微调的方式对先验进行调制，使听者运动既保留自然多样性，又响应对话语境。
primary_logic: 听者行为并非简单的音频到运动映射，而是由内部运动先验和外部音频线索共同塑造。内部先验主导自发行为，外部音频提供对话调制。
claims:
- 直接联合优化导致听者分支坍塌为静态面部先验，产生表达僵硬。
- 音频特征与说话运动高度相关，但与听者运动的对齐明显更弱（t-SNE距离大）。
- 通过两阶段训练，UniLS在听者分布性指标上比先前方法提升了最高44.1%。
- 消融实验表明，移除阶段1（无音频预训练）会导致听者自然性显著下降。
---

# UniLS: End-to-End Audio-Driven Avatars for Unified Listening and Speaking

> [!tip] 核心洞察
> 听者行为并非简单的音频到运动映射，而是由内部运动先验和外部音频线索共同塑造。内部先验主导自发行为，外部音频提供对话调制。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniLS: 端到端音频驱动的统一听说话头化身 |
| 英文题名 | UniLS: End-to-End Audio-Driven Avatars for Unified Listening and Speaking |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09327) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | UniLS |
| Dataset | Seamless Interaction, User Study |

> [!tip] 效果简介
> - Seamless Interaction (speaking) 上，LVE↓ 5.83 vs 6.35 (DualTalk) (↓0.52)；FDD↓ 18.41 vs 27.41 (ARTalk*) (↓9.00)。
> - Seamless Interaction (listening) 上，F-FID↓ 4.304 vs 10.779 (ARTalk*) (↓6.475)。
> - User Study (25 participants) 上，Reaction Naturalness Preference Rate (vs DualTalk) 91.4% vs 50% (random) (+41.4%)。

## 概要

对话式数字人需要同时具备**说话**与**聆听**两种能力。然而，现有方法大多仅处理单向生成——要么只驱动说话表情，要么只生成聆听反应。少数支持听-说双模态的方法（如 **DualTalk**，Peng et al., CVPR 2025）采用非端到端的串行流水线：先生成说话者A的面部序列，再据此生成说话者B的动作，这不仅阻断实时交互，还引入了级联误差。

本文提出 **UniLS**，首个仅以双轨音频为输入的端到端统一听-说表情生成框架。其核心发现是：直接联合优化听-说双分支时，由于聆听者运动与对方音频的相关性显著弱于说话者与其自身音频的相关性（Figure 2 的 t-SNE 分析证实了这一点），模型会坍塌为静态、低方差的“扑克脸”先验，导致聆听表情僵硬不自然。

为解决这一问题，UniLS 采用**两阶段训练策略**：

1. **阶段一（内部运动先验学习）**：在不使用任何音频的条件下，在多样化的多场景视频数据上训练一个自回归生成器，使其学会自发行为（如眨眼、微表情、头部自然摆动）的内部运动先验。
2. **阶段二（双轨音频调制）**：在成对对话数据上微调该生成器，通过双交叉注意力层分别引入说话者A和B的音频特征，并以 LoRA 适配器保护阶段一学到的先验不被遗忘。

实验表明，UniLS 在聆听分布性指标上较先前方法最高提升 **44.1%**，在用户研究中获得了 **91.4%** 的反应自然性偏好率（对比 DualTalk）。消融实验进一步确认：移除阶段一的无音频预训练将导致聆听自然性显著下降，验证了内部运动先验对自然聆听反应的关键作用。



### 问题背景：从单向生成到双向交互

音频驱动的说话头生成（audio-driven talking head）近年来取得了显著进展，但其核心范式长期停留在**单向输出**：给定一段音频，生成对应说话者的面部动画。真实的人类对话场景远非单向独白——参与者交替或同时扮演**说话者（speaker）**与**听者（listener）**，听者的非言语反馈（如点头、微笑、眨眼、注视变化）是对话自然性的关键构成。

Figure 1 对比了先前方法与UniLS的范式差异。大多数已有工作仅处理“仅说话”或“仅聆听”的单一模式；少数尝试同时建模两者的方法（如**DualTalk**，Peng et al., CVPR 2025）采用**非端到端**的流水线——先生成说话者A的面部序列，再基于A的输出生成听者B的动作。这种级联架构不仅阻断了实时交互的可能性，还将听者生成退化为对说话者输出的条件映射，忽略了听者行为的自发特性。

### 核心瓶颈：听者分支的“扑克脸”坍塌

端到端联合训练说话与聆听分支看似直接，实则面临一个深层困境。Figure 2 通过t-SNE可视化揭示了问题的本质：**音频特征与说话运动的分布高度聚集，但与听者运动的对齐明显更弱**。这意味着，听者行为并非像说话唇形那样与对方音频存在强相关性——听者的面部表情更多由内部状态（注意力、情绪、社交意图）驱动，而非声学信号的直接映射。

当模型被强制从对方音频中学习听者运动时，由于缺乏足够强的监督信号，优化过程会驱动听者分支坍塌为一个**安全但静态的面部先验**——即所谓“扑克脸”（poker face）。直接联合优化使模型退化为生成僵硬、低方差的听者表情，丧失了对话中应有的丰富非言语反馈。这一坍塌现象的置信度很高（0.95），构成了本文的核心动机。

### 现有方法的缺口

综合来看，已有工作在以下几个维度存在明显缺口：

1. **范式单向性**：大多数方法仅支持说话或聆听的单一模式，无法在统一框架内同时生成两者的面部运动。
2. **非端到端架构**：少数听说话头方法依赖级联生成，先产生说话者输出再驱动听者，阻碍实时应用。
3. **听者先验缺失**：现有方法未显式建模听者的内部运动先验，导致在弱音频-运动相关性的条件下，听者分支容易坍塌为静态表情。
4. **训练策略失配**：端到端联合训练未区分说话与聆听任务在音频依赖性上的本质差异，使模型无法为两者学习到适配的表征。

### 本文动机与核心思路

针对上述瓶颈，UniLS提出一个根本性的视角转换：**听者行为并非简单的音频到运动映射，而是由内部运动先验和外部音频线索共同塑造**。内部先验主导眨眼、微表情等自发行为，外部音频提供对话节奏和社交信号的调制。

基于这一洞察，UniLS设计了两阶段训练策略（Figure 3）：
- **阶段1**：在无音频条件下，于多场景视频数据上训练自回归生成器，迫使模型学习丰富的内部运动先验——即“一个人即使在沉默中也会自然产生的面部动态”。
- **阶段2**：引入双轨音频（说话者A和B的语音），通过交叉注意力机制对预训练先验进行调制，使听者运动既保留自然多样性，又能响应对话语境。

这一设计将听者生成从“从零学习音频-运动映射”重构为“用音频调制已有运动先验”，从根本上规避了坍塌问题。



## 核心方法与创新机理

### 问题瓶颈：听者分支的“扑克脸”坍塌

端到端统一生成说话与聆听面部运动的核心挑战在于**音频-运动相关性的不对称**。如 Figure 2 的 t-SNE 可视化所示，音频特征与说话运动的分布高度重叠，但与聆听运动的对齐明显更弱。当直接进行端到端联合训练时，模型会倾向于学习一个“安全”的静态面部先验——听者分支坍塌为低方差、缺乏表情变化的“扑克脸”，导致聆听反应僵硬不自然。这一现象是 UniLS 方法设计的直接动因。

### 核心洞见：内部运动先验与外部音频调制的解耦

UniLS 的核心洞见在于重新定义了听者行为的生成机制：**听者运动并非简单的音频到运动映射，而是由内部运动先验和外部音频线索共同塑造**。内部先验主导自发行为（如眨眼、微表情、头部微动），外部音频提供对话语境下的调制信号。基于这一认识，UniLS 设计了**两阶段训练策略**（Figure 3），将先验学习与音频调制解耦：

- **阶段1：无音频运动先验预训练**。在未配对的多场景视频数据上训练一个音频自由的自回归生成器 $\mathcal{G}(M_{1:t}, \mathbf{s})$，仅基于过去运动和风格嵌入预测未来运动块。该阶段使模型掌握丰富的内部运动先验，包括自发面部行为和时序多样性。

- **阶段2：双轨音频交叉注意力微调**。在阶段1预训练权重基础上，引入双交叉注意力层分别融合说话者 A 和 B 的音频特征，生成式变为 $\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{a}_{1:t}^{A}, \mathbf{a}_{1:t}^{B}, \mathbf{s})$。同时采用 **LoRA 适配器**对骨干网络进行高效微调，防止音频条件的引入破坏已学到的内部运动先验。

### 关键架构改进：双交叉注意力与 LoRA 微调

相比先前方法（如 **DualTalk**，Peng et al., CVPR 2025）的级联式或单音频条件化设计，UniLS 在架构层面做了两个关键改进：

1. **双交叉注意力机制**：在每个 Transformer 块中分别添加针对说话者 A 和 B 音频的交叉注意力层，使模型能同时感知自身语音（驱动唇形同步）和对方语音（驱动聆听反应）。消融实验证实，将其替换为单交叉注意力会导致唇形同步指标（LVE、MHD）显著退化。

2. **LoRA 微调策略**：阶段2中骨干网络权重继承自阶段1，仅通过 LoRA 低秩适配器进行参数高效微调。这一设计在引入音频条件的同时保留了预训练先验，避免了直接全参数微调可能导致的先验遗忘。

### 与 baseline 的核心差异

| 维度 | 先前方法 | UniLS |
|------|---------|-------|
| 训练策略 | 端到端联合训练 | 两阶段：先验预训练 + 音频调制微调 |
| 音频条件化 | 单音频输入或未明确区分 | 双交叉注意力（说话者 A + B 音频） |
| 听者先验 | 无显式先验，易坍塌 | 阶段1多场景数据预训练获得内部运动先验 |
| 微调方式 | 全参数微调 | LoRA 低秩适配，防止先验遗忘 |

### 证据支撑

消融实验（Table 3）提供了关键因果证据：**移除阶段1**（仅用阶段2训练）导致听者运动自然性显著下降，FDD 升高、F-FID 变差，直接验证了内部运动先验对自然聆听反应的必要性。此外，使用**多场景数据**训练阶段1能够学习更强的内部运动先验，进而同时提升说话和聆听表现，表明先验的泛化能力是方法有效性的重要基础。



UniLS 提出首个端到端音频驱动的统一听说话头生成框架，仅以双轨音频（说话者 A 和 B 的语音）为输入，同时输出两人的 3D 面部运动序列，涵盖说话和聆听两种行为。与以往单向（仅说话或仅聆听）或非端到端（需先为说话者 A 生成序列再为 B 生成）的方法不同，UniLS 实现了实时、统一的听说话头运动生成（Figure 1）。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between previous methods and our proposed approach. Most previous studies remain one-way, i.e., speak-only or listen-only. The previous speak–listen method [35] requires generating speaker A’s facial sequence before producing speaker B’s motions. The speaker-A generation makes it non-end-to-end and blocks real-time. In contrast, our method provides an end-to-end framework for unified, real-time speak–listen motion generation*

### 核心瓶颈与设计动机

直接端到端联合训练听说话头生成器会遭遇一个关键瓶颈：**听者运动与对方音频的相关性显著弱于说话运动与自身音频的相关性**。t-SNE 可视化分析（Figure 2）清晰表明，音频特征与说话运动高度聚类，但与听者运动的对齐明显更弱。这导致模型在联合优化时倾向于将听者分支坍塌为静态、低方差的“扑克脸”——一种安全的静态面部先验，使聆听表情僵硬不自然。

### 两阶段训练策略

为解决上述瓶颈，UniLS 引入两阶段训练范式（Figure 3），将内部运动先验的学习与音频驱动调制解耦：

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our two-stage training strategy. Stage 1 trains an audio-free generator on unpaired multi-scenario video data without using audio. Given past motions and a style embedding, the model predicts future free motion chunks. Stage 2 finetunes the generator on paired conversational clips by conditioning on speaker-A and speaker-B’s audios through cross-attention, producing audiodriven speak–listen motions*

- **阶段1：无音频运动先验预训练。** 在不使用任何音频的条件下，在非配对的多场景视频数据上训练一个自回归生成器。给定过去运动块 $M_{1:t}$ 和风格嵌入 $\mathbf{s}$，模型预测未来运动块 $\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{s})$，并通过逐块 L1 重建损失 $\mathcal{L} = \sum_{t=1}^{T} \|\hat{M}_{t:2t} - M_{t:2t}\|$ 进行优化。此阶段使模型学会内部运动先验（如眨眼、微表情等自发行为），为听者运动提供自然的多样性基础。

- **阶段2：双音频交叉注意力微调。** 在阶段1预训练权重基础上，引入双轨音频条件。在每个 Transformer 块中增加两个交叉注意力层，分别融入说话者 A 和 B 的音频特征，使生成器能够根据对话语境调制运动：$\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{a}_{1:t}^{A}, \mathbf{a}_{1:t}^{B}, \mathbf{s})$。为防止音频条件化破坏阶段1学到的运动先验，骨干权重通过 LoRA 进行微调，仅新增的交叉注意力层从头训练。

### Pipeline 模块组成

UniLS 的完整 pipeline 包含以下核心模块：

1. **音频编码器（wav2vec）：** 采用冻结的 wav2vec 编码器将原始双轨音频分别编码为特征序列，作为后续交叉注意力的条件输入。
2. **多尺度 VQ 编解码器：** 学习紧凑的离散运动表示，作为生成器的监督目标。通过逐级量化和残差更新 $\mathbf{c}^{(l+1)} = \mathrm{Interp}(\mathrm{Quant}(\mathbf{f}^{(l)}), k_l)$，$\mathbf{f}^{(l+1)} = \mathbf{f}^{(l)} - \mathbf{c}^{(l+1)}$ 实现多尺度压缩。
3. **自回归生成器（Transformer）：** 基于堆叠的自注意力和前馈块构建，以过去运动、风格嵌入和音频条件预测下一块运动。阶段1仅依赖运动和风格，阶段2增加双交叉注意力模块。
4. **双交叉注意力模块：** 分别融入说话者 A 和 B 的音频特征，驱动对应的说话和听者运动分支。
5. **LoRA 适配器：** 在阶段2微调时保持预训练先验，高效适应音频条件。

### 输入输出流

- **输入：** 双轨音频（说话者 A 和 B 的语音流）、风格嵌入（控制面部运动风格）、初始运动块。
- **输出：** 说话者 A 和 B 的同步 3D 面部运动序列，包含表情参数和头部姿态，同时覆盖说话和聆听行为。
- **推理流程：** 音频编码器实时提取双轨特征 → 自回归生成器基于历史运动、风格嵌入和双交叉注意力条件逐块预测未来运动 → 解码为连续的 3D 面部参数序列。

该框架实现了 560.6 FPS 的推理速度，支持实时应用，同时模型参数量相比基线方法更小（Table 4）。



### 3D面部运动表示

UniLS采用FLAME 3D可变形模型表示面部运动，将连续 $T$ 帧的表情参数 $\psi$ 和姿态参数 $\theta$ 拼接为运动矩阵：

$$M \in \mathbb{R}^{T \times D}$$

其中 $D$ 为每帧的运动参数维度。这一表示同时捕获面部表情和头部姿态的动态变化，为后续的离散化与生成提供统一的运动空间。

### 多尺度VQ编解码器

为获得紧凑且富有表达力的离散运动表示，UniLS采用时序多尺度VQ编解码器。该模块通过逐级量化和残差更新的方式，将连续运动特征压缩为多层离散编码。

核心公式为渐进式量化与残差更新：

$$\mathbf{c}^{(l+1)} = \mathrm{Interp}(\mathrm{Quant}(\mathbf{f}^{(l)}), k_l), \quad \mathbf{f}^{(l+1)} = \mathbf{f}^{(l)} - \mathbf{c}^{(l+1)}$$

其中 $\mathbf{f}^{(l)}$ 为第 $l$ 层的输入特征，$\mathrm{Quant}(\cdot)$ 执行向量量化操作，$\mathrm{Interp}(\cdot, k_l)$ 以因子 $k_l$ 进行上采样以匹配原始时间分辨率，$\mathbf{c}^{(l+1)}$ 为当前尺度量化的运动编码，$\mathbf{f}^{(l+1)}$ 为传入下一层的残差。通过多尺度分解，模型能够在不同时间粒度上捕获从细微表情到宏观姿态的运动模式。

### 阶段一：无音频自回归生成器

阶段一的核心是训练一个不依赖音频的自回归Transformer生成器，学习面部运动的内部先验分布。给定前 $t$ 帧的运动 $M_{1:t}$ 和风格嵌入 $\mathbf{s}$，模型预测下一块运动：

$$\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{s})$$

训练目标为逐块L1重建损失：

$$\mathcal{L} = \sum_{t=1}^{T} \|\hat{M}_{t:2t} - M_{t:2t}\|$$

生成器 $\mathcal{G}$ 由堆叠的自注意力和前馈模块组成。此阶段在无音频条件下，迫使模型从多样化多场景数据中学习眨眼、微表情等自发面部行为的统计规律，形成稳健的内部运动先验。

### 阶段二：双音频条件化微调

阶段二在冻结的音频编码器（wav2vec）基础上，向每个Transformer块引入两个交叉注意力层，分别融入说话者A和说话者B的音频特征：

$$\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{a}_{1:t}^{A}, \mathbf{a}_{1:t}^{B}, \mathbf{s})$$

其中 $\mathbf{a}_{1:t}^{A}$ 和 $\mathbf{a}_{1:t}^{B}$ 分别为双轨音频的特征序列。双交叉注意力设计使得模型能够区分自身语音驱动的说话行为和对方语音驱动的聆听行为——前者与唇形同步高度相关，后者仅提供对话节奏和语调等声学线索。

为防止音频条件化破坏阶段一学到的内部运动先验，阶段二采用LoRA对骨干网络权重进行低秩微调，而交叉注意力层则从头训练。这一设计在引入音频调制能力的同时，保留了聆听表情的自然多样性。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/002_Figure_2.jpg]]
*Figure 2: Correlation between facial expression parameters [17] and corresponding audio features [2]. For speaking, the audio is the speaker’s own speech. For listening, the audio comes from the other speaker’s speech*



## 实验与关键发现

### 5.1 实验设置

UniLS 基于 **Seamless Interaction** 数据集进行训练与评估，该数据集包含丰富的双人对话视频，涵盖说话与聆听两种状态。面部运动采用 **FLAME** 3D 可变形模型表示，提取表情参数 $\psi$ 和头部姿态参数 $\theta$，构成运动矩阵 $M \in \mathbb{R}^{T \times D}$。音频特征通过冻结的 **wav2vec** 编码器提取。

训练分为两个阶段。首先训练一个**多尺度 VQ 编解码器**，使用 AdamW 优化器，学习率 $1 \times 10^{-4}$，批量大小 64，共训练 100,000 次迭代，以获得紧凑的离散运动表示。随后进行两阶段自回归生成器训练：阶段1在无音频条件下以批量大小 128 训练 200,000 次迭代；阶段2引入双轨音频，以 LoRA 方式微调。全部训练在 **4 块 NVIDIA H200 GPU** 上完成，总计约 **40 GPU 小时**（阶段1约10小时，阶段2约30小时）。

### 5.2 主实验结果

#### 定量评估

Table 1 展示了在 Seamless Interaction 测试集上的全面定量对比。UniLS 在说话和聆听两类指标上均取得最优或次优结果。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/004_Table_1.jpg]]
*Table 1: Evaluation of speaking and listening facial motions on the Seamless Interaction [1] test split. We use colors to denote the first and second places, respectively*

**说话性能**方面，UniLS 在唇形同步关键指标上显著领先：
- **LVE**（唇部顶点误差）降至 **5.83**，较 **DualTalk**（Peng et al., CVPR 2025）的 6.35 降低 0.52，较 **ARTalk\*** 的 7.08 降低 1.25。
- **MHD**（嘴部豪斯多夫距离）为 **1.89**，优于 DualTalk 的 2.06 和 ARTalk\* 的 2.23。
- 面部动态距离 **FDD** 为 **18.41**，较 ARTalk\* 的 27.41 大幅降低 9.00，表明整体面部运动更接近真实分布。

**聆听性能**方面，UniLS 的优势更为突出：
- **F-FID**（面部 Fréchet Inception Distance）降至 **4.304**，较 ARTalk\* 的 10.779 降低 **6.475**，相对提升约 60%。
- **P-FID**（姿态 FID）为 **0.038**，远优于 DualTalk 的 0.075 和 ARTalk\* 的 0.055。
- **FDD** 为 **17.12**，较 ARTalk\* 的 21.17 降低 4.05。

这些结果表明，两阶段训练策略有效解决了聆听分支坍塌问题，使听者运动保持了自然的多样性与表现力。

#### 用户研究

Table 2 报告了 25 名参与者的用户研究结果。用户对 UniLS 与各基线方法生成的视频进行盲评，从唇形同步（Sync）、表情自然度（Exp）、反应自然度（React）和头部姿态自然度（Pose）四个维度进行偏好选择。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/007_Table_2.jpg]]
*Table 2: User study results with 25 participants. Numbers (%) indicate the proportion of users who prefer our method over each baseline. “Sync” measures lip synchronization, while “Exp”, “React”, and “Pose” assess the naturalness of facial expressions, listening reactions, and head pose, respectively*

与 **DualTalk** 的对比中，UniLS 在**反应自然度**上获得了 **91.4%** 的偏好率，远超随机水平（50%），表明用户对 UniLS 生成的聆听反应高度认可。在唇形同步和表情自然度上也分别获得 73.9% 和 78.3% 的偏好率。与 **ARTalk** 和 **DiffPoseTalk**（Sun et al., TOG 2024）的对比同样呈现一致优势。

#### 定性分析

Figure 4 展示了聆听运动的定性对比。基线方法（如 ARTalk\*）生成的听者面部在时间维度上表现出明显的**运动僵硬**（红色矩形标注区域），表情变化幅度极小，呈现“扑克脸”效应。相比之下，UniLS 生成的听者运动展现出丰富的微表情变化和自然的时序多样性，验证了内部运动先验对聆听行为建模的关键作用。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on listening motions. Red rectangles highlight motion stiffness over time. Additional qualitative evaluation results are available in the supplementary materials*

Figure 5 展示了说话运动的定性对比。UniLS 在唇形同步精度和表情风格上与真实值（Ground Truth）高度一致，能够准确捕捉不同音素的发音特征。

### 5.3 消融实验

Table 3 系统消融了 UniLS 各核心组件的贡献。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/008_Table_3.jpg]]
*Table 3: Ablation study on different components in our framework*

**阶段1（无音频预训练）的关键性**：移除阶段1，仅使用阶段2的音频条件训练，导致聆听性能显著退化——FDD 升高、FID 变差。这直接证实了核心洞察：**内部运动先验是自然聆听反应的基础**，直接从音频学习听者运动会导致模型坍塌为静态先验。

**双交叉注意力的必要性**：将双交叉注意力替换为单交叉注意力层后，说话性能出现明显退化，尤其是唇形同步指标 LVE 和 MHD 显著升高。这表明**分别建模说话者A和B的音频对各自运动的驱动关系**是必要的，单一注意力无法有效解耦两种不同的音频-运动映射。

**多场景数据的贡献**：使用多场景数据训练阶段1能够学习更强的内部运动先验，进而同时提升说话和聆听表现。这验证了多样化无配对数据对于构建鲁棒运动先验的价值。

**LoRA 微调的作用**：Table 3 还验证了 LoRA 适配器在阶段2微调中的有效性——它在引入音频条件的同时，有效防止了预训练先验的灾难性遗忘。

### 5.4 实时性能与计算开销

Table 4 对比了各方法的推理速度与模型规模。UniLS 以 **560.6 FPS** 的推理速度远超实时需求，显著优于 ARTalk 和 DualTalk。同时，UniLS 在模型参数量上也更具优势，在实时性、吞吐量和模型大小之间取得了最佳平衡。这一优势源于自回归生成器的轻量化设计以及离散运动表示的高效性——模型仅需预测紧凑的离散编码，而非连续的高维运动参数。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/009_Table_4.jpg]]
*Table 4: Comparison of real-time performance and computational costs. “RT” indicates whether real-time use is supported*

### 5.5 阶段1生成器的独立评估

Table 5 对阶段1训练的无音频生成器进行了独立定量评估。该生成器在无任何音频输入的条件下，仅基于过去运动和风格嵌入预测未来运动。评估结果表明，阶段1生成器能够产生具有合理多样性和时序连贯性的自由面部运动，为阶段2的音频调制提供了有效的初始化先验。

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/010_Table_5.jpg]]
*Table 5: Quantitative evaluation of the audio-free generator trained in stage 1*

### 5.6 失败模式与局限性

尽管 UniLS 在整体性能上表现优异，仍存在以下局限：

1. **语义理解缺失**：模型仅依赖声学线索驱动听者行为，缺乏对对话语义的理解。当对方音频的声学特征与语义内容不一致时（如平静语调表达重要信息），听者反应可能不够贴切。
2. **块级生成的不连续性**：基于块的生成方式在块边界处偶有轻微不连续，限制了完全平滑的运动过渡。
3. **场景扩展受限**：当前框架仅支持双人对话，尚未扩展到多方交互场景。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_arxiv_org_abs_2512_09327/figures/011_Figure_6.jpg]]
*Figure 6: The interface of our user study. Users evaluate each video based on four perspectives: lip synchronization, expression naturalness, reaction naturalness, and head pose naturalness. All these four perspectives are judged by comparing methods A and B. One of the videos (A or B) is generated by our method, and the other by a baseline method, with their order randomized*



## 定位与知识库关联

### 统一听说话头生成的任务定位

UniLS 将自身定位为**首个端到端音频驱动的统一听说话头生成框架**，其核心区分点在于同时生成对话双方的说话与聆听面部运动，且仅以双轨音频为输入。此前的工作在任务覆盖和架构设计上存在明确的代际差异：

- **单向生成（仅说话或仅聆听）**：大多数先前研究仅处理单一角色——要么生成说话者的面部运动（如 **DiffPoseTalk** (Sun et al., TOG 2024) 基于扩散模型；**ARTalk** 基于自回归模型），要么生成听者的反应运动。这类方法无法处理对话场景中角色身份的动态切换。
- **非端到端的听说话头生成**：**DualTalk** (Peng et al., CVPR 2025) 是此前唯一同时处理听说话头的工作，但其架构要求先生成说话者A的面部序列，再基于A的输出生成听者B的运动。这种级联设计存在两个根本性限制：(1) 非端到端，阻碍实时应用；(2) 听者生成的误差会沿流水线累积。
- **UniLS的架构突破**：通过双交叉注意力机制同时融入说话者A和B的音频特征，UniLS实现了真正的并行端到端生成，无需中间步骤。如 Table 4 所示，UniLS 以 560.6 FPS 的推理速度远超 ARTalk 和 DualTalk，且模型参数量更小，提供了最佳的实时性-质量权衡。

### 核心瓶颈与因果机制

UniLS 的方法设计源于对听者行为生成中一个关键瓶颈的洞察：**端到端联合训练时，听者分支容易坍塌为静态、低方差的“扑克脸”**。这一现象的因果链条如下：

1. **音频-运动相关性不对称**：如 Figure 2 的 t-SNE 可视化所示，音频特征与说话运动的聚类高度紧密，但与听者运动的对齐明显更弱。这意味着听者运动与对方音频之间的映射关系本质上比说话运动弱得多。
2. **模型的安全坍塌策略**：当直接进行联合优化时，模型为最小化整体损失，会驱动听者分支退化为一个“安全”的静态面部先验——生成几乎不变化的聆听表情。这导致表达僵硬，缺乏自然对话中应有的微表情和自发行为（如眨眼、轻微的头部运动）。
3. **内部运动先验的缺失**：听者行为并非简单的音频到运动映射，而是由**内部运动先验**（自发行为，如眨眼、微表情、头部姿态的自然波动）和**外部音频线索**（对话语境提供的调制信号）共同塑造。直接联合训练无法解耦这两个因素，导致内部先验被音频信号的弱相关性所淹没。

### 方法创新与知识贡献

UniLS 通过**两阶段训练策略**解耦了内部运动先验的学习与音频驱动的调制，这一设计构成了方法的核心知识贡献：

**阶段1：无音频运动先验预训练**
- 在**无音频条件**下训练自回归生成器 $\mathcal{G}(M_{1:t}, \mathbf{s})$，仅基于过去运动和风格嵌入预测未来运动块。
- 训练数据采用**未配对的多场景视频数据**（即不要求对话配对），使模型接触更丰富的面部运动多样性。
- 这一阶段的目标是让模型学习**内部运动先验**——即“一个自然的人在没有外部刺激时会如何运动”，包括眨眼频率、微表情变化、头部姿态的自然漂移等自发行为。

**阶段2：双音频交叉注意力微调**
- 引入双轨音频，通过在每个 Transformer 块中添加两个交叉注意力层，分别融入说话者A和B的音频特征：$\hat{M}_{t:2t} = \mathcal{G}(M_{1:t}, \mathbf{a}_{1:t}^{A}, \mathbf{a}_{1:t}^{B}, \mathbf{s})$。
- 关键设计：阶段1的骨干权重通过 **LoRA 适配器**进行微调，而非从头训练。这确保了模型在适应音频条件时不会“遗忘”已学到的内部运动先验，从而保持聆听表情的自然多样性。
- 消融实验证实了这一设计的必要性：**移除阶段1**（仅用阶段2训练）会导致听者运动自然性显著下降（FDD 升高，FID 变差）；**用单交叉注意力替换双交叉注意力**则会导致说话唇形同步指标（LVE, MHD）明显退化。

这一两阶段范式将听者行为生成重新框定为“先验学习 + 条件调制”问题，而非直接的音频到运动回归，为后续工作提供了可复用的方法论框架。

### 适用边界与局限性

尽管 UniLS 在定量和定性评估上均取得显著提升，其设计存在明确的适用边界：

1. **缺乏语义理解能力**：模型仅依赖声学线索（如韵律、能量、停顿）驱动听者行为，而不理解对话的语义内容。这意味着听者反应可能缺乏语义一致性——例如，对笑话和严肃陈述的聆听表情可能难以区分。这是当前框架的根本性限制，而非训练数据或架构的不足。

2. **基于块的生成方式**：模型采用逐块自回归生成策略，虽然保证了实时性，但块边界处偶有轻微不连续。这限制了生成运动的完全连续性，在高帧率渲染场景下可能被察觉。

3. **仅支持双人对话**：当前框架假设对话参与者恰好为两人（A和B），尚未扩展到多方交互场景。在多人对话中，听者需要同时处理多个说话者的音频流，且注意力分配机制更为复杂。

4. **数据依赖与泛化性**：阶段1的多场景数据多样性直接影响内部运动先验的质量。消融实验表明，使用多场景数据训练能学习更强的先验，但论文未系统评估不同数据组合对跨文化、跨语言场景的泛化能力。

### 开放问题与后续方向

基于上述局限性，以下几个方向值得后续工作探索：

- **语义特征的融合**：引入语言或语义特征（如文本转录、情感标签、对话意图）作为额外条件，使听者反应不仅响应声学线索，还能与对话内容保持一致。这可能需要多模态编码器或大语言模型的介入。
- **多人对话扩展**：将双交叉注意力机制泛化为多头注意力或多流注意力，使框架能够处理三人及以上的对话场景。核心挑战在于如何建模听者对不同说话者的注意力分配。
- **情感与意图感知**：结合情感识别或意图预测模块，生成更丰富的非言语行为（如点头、皱眉、微笑），使听者化身的表现力更接近真实人际交互。
- **文化规范的建模**：不同文化背景下，听者行为的规范存在差异（如眼神接触的频率、点头的时机）。如何在训练数据中编码文化先验，或通过可控生成实现文化适应，是一个兼具技术和社会意义的问题。
- **连续性与长程一致性**：探索超越块级自回归的生成范式（如扩散模型、流匹配），以消除块边界的不连续性，同时保持实时推理能力。

### 知识库定位总结

UniLS 在听说话头生成领域建立了以下可被后续工作引用的知识锚点：

| 知识类型 | 具体内容 | 证据强度 |
|---------|---------|---------|
| **瓶颈发现** | 直接联合训练导致听者分支坍塌为静态先验 | 强（t-SNE分析 + 消融实验） |
| **解耦策略** | 两阶段训练：先学习内部运动先验，再通过交叉注意力 + LoRA 进行音频调制 | 强（消融实验证实阶段1和双交叉注意力的必要性） |
| **性能基准** | 在 Seamless Interaction 测试集上，听者分布性指标（F-FID）较先前方法提升最高 44.1%；用户研究中听者反应自然性偏好率达 91.4% | 强（Table 1, Table 2） |
| **适用边界** | 缺乏语义理解；仅支持双人对话；块生成偶有不连续 | 论文明确声明 |
| **开放方向** | 语义融合、多人扩展、情感感知、文化适应 | 论文讨论部分提出 |



## 原文 PDF

![[paperPDFs/CVPR_2026/UniLS_End_to_End_Audio_Driven_Avatars_for_Unified_Listening_and_Speaking.pdf]]
