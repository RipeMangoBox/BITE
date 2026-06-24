---
title: "A cross-species neural foundation model for end-to-end speech decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_cross_species_neural_foundation_model_for_end_to_end_speech_decoding.pdf
aliases:
- BBT
- CSNFMEESD
- "BIT (BraIn-to-Text)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "引入跨任务、跨物种的Transformer神经编码器，通过自监督掩码建模在大规模Utah阵列数据（367小时）上预训练，并结合音频大语言模型（audio-LLM）和对比学习实现端到端优化。"
primary_logic: "大规模自监督预训练（结合人类和猴子数据）能够学习稳定的神经表征，这些表征可以跨任务（尝试性言语和想象性言语）迁移，并且通过对比学习对齐神经和文本嵌入空间，使小规模音频LLM在端到端解码中显著优于文本LLM。"
claims:
- "BIT将先前端到端方法的词错误率（WER）从24.69%降低到10.22%。"
- "在级联设置中，预训练编码器在Brain-to-Text '24和'25基准上建立了新的最先进水平（SOTA）。"
- "BIT级联+集成在Brain-to-Text '24保留集上达到5.10% WER，在'25公共排行榜上达到1.76% WER。"
- "BIT端到端+集成在Brain-to-Text '24保留集上达到10.22% WER，在'25公共排行榜上达到7.76% WER。"
---

# A cross-species neural foundation model for end-to-end speech decoding

> [!tip] 核心洞察
> 大规模自监督预训练（结合人类和猴子数据）能够学习稳定的神经表征，这些表征可以跨任务（尝试性言语和想象性言语）迁移，并且通过对比学习对齐神经和文本嵌入空间，使小规模音频LLM在端到端解码中显著优于文本LLM。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 跨物种神经基础模型用于端到端语音解码 |
| 英文题名 | A cross-species neural foundation model for end-to-end speech decoding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Lp1noMpMUG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | BIT (BraIn-to-Text) |
| Dataset | Brain-to-Text '24, Brain-to-Text '25 |

> [!tip] 效果简介
> - Brain-to-Text '24 上，WER 为 5.10% (BIT Cascaded + Ensemble)，对比 6.35% (BIT Cascaded)，变化 -1.25%。
> - Brain-to-Text '24 上，WER 为 10.22% (BIT End-to-End + Ensemble)，对比 24.69% (prior end-to-end method)，变化 -14.47%。
> - Brain-to-Text '25 上，WER 为 1.76% (BIT Cascaded + Ensemble)，对比 —，变化 —。

## 概述

本文提出BIT（BraIn-to-Text），一个用于端到端语音解码的跨物种神经基础模型。其核心瓶颈在于：传统级联框架无法实现端到端联合优化，且RNN编码器在小数据集上表现有限，难以充分利用现代Transformer架构和大规模预训练的优势。BIT的因果机制是引入一个跨任务、跨物种的Transformer神经编码器，通过自监督掩码建模在367小时的Utah阵列数据（包含人类和猴子的言语及手臂运动任务）上预训练，并结合音频大语言模型（audio-LLM）与对比学习实现端到端优化。核心洞见在于：大规模自监督预训练能够学习稳定的、可跨任务迁移的神经表征，且通过对比学习对齐神经和文本嵌入空间，使得小规模音频LLM在端到端解码中显著优于文本LLM。

主要结果方面，BIT将先前端到端方法的词错误率（WER）从24.69%降低至10.22%（Brain-to-Text '24保留集）。在级联设置中，预训练编码器在Brain-to-Text '24和'25基准上均建立了新的最先进水平（SOTA）。BIT级联+集成在'24保留集上达到5.10% WER，在'25公共排行榜上达到1.76% WER；BIT端到端+集成在'24保留集上达到10.22% WER，在'25公共排行榜上达到7.76% WER。在想象性言语解码（50词词汇量）中，BIT-All在级联和端到端设置下均优于所有其他基线。

## 背景与动机

脑机接口（BCI）领域的一个核心挑战是将神经活动直接解码为自然语言，即“脑到文本”（Brain-to-Text）翻译。现有方法主要采用级联框架：先通过神经编码器预测音素序列，再借助独立的语言模型（如n-gram模型）将其转换为单词。这种级联设计存在根本性瓶颈——神经编码器与语言模型无法联合优化，导致信息流在中间表示处被截断，丢失了端到端语义一致性。此外，广泛使用的循环神经网络（RNN）编码器在小规模标注数据集上表现有限，无法充分利用现代Transformer架构和大规模预训练带来的表征能力提升。

现有方法的另一个缺口在于对神经表征的跨任务、跨物种泛化能力探索不足。言语BCI通常依赖特定任务（如大声朗读）和特定受试者的标注数据，但临床相关场景（如想象性言语）的标注数据极为稀缺。能否利用大规模无标注数据（包括来自不同物种的数据）学习稳定的神经表征，并迁移到新任务上，是一个尚未解决的关键问题。

本文提出的BIT（BraIn-to-Text）框架，其核心动机正是同时解决上述两个瓶颈。BIT引入了一个基于Transformer的神经编码器，通过自监督掩码建模在367小时的Utah阵列数据（涵盖人类和猴子的言语及手臂运动任务）上进行预训练。这一设计的关键因果机制在于：大规模跨任务、跨物种的预训练能够学习到对传感器变异和任务差异鲁棒的神经表征，从而在标注数据极少的想象性言语任务中实现有效迁移。在解码端，BIT抛弃了级联的n-gram语言模型，转而采用音频大语言模型（audio-LLM）作为端到端解码器，并通过对比学习对齐神经嵌入和文本嵌入空间。这一改变使得小规模音频LLM能够在有限标注数据下显著优于文本LLM，将先前端到端方法的词错误率（WER）从24.69%降低到10.22%。同时，在级联设置下，预训练编码器也在Brain-to-Text '24和'25基准上建立了新的最先进水平（SOTA），BIT级联+集成在'24保留集上达到5.10% WER，在'25公共排行榜上达到1.76% WER。

## 核心创新

BIT (BraIn-to-Text) 的核心创新在于用一套**跨任务、跨物种的自监督预训练 Transformer 编码器**替换了传统级联框架中的 RNN 编码器，并引入**音频大语言模型（audio-LLM）**与**对比学习**实现端到端联合优化。这一因果链直接针对了此前方法的核心瓶颈：级联框架无法端到端联合优化，且 RNN 编码器在小数据集上表现有限，无法充分利用现代 Transformer 架构和大规模预训练的优势。

**关键 changed slots 及其因果机制：**

1. **神经编码器架构**：从 RNN 切换为 Transformer（带 RoPE 和双向注意力掩码）。Transformer 的双向注意力机制允许每个时间 patch 关注所有其他 patch，相比 RNN 的序列依赖，能更有效地捕捉神经活动中的长程时间依赖关系。证据锚点明确声明“We employ a transformer to learn latent representations from neural activity”，置信度 0.95。

2. **预训练策略**：从无预训练或仅监督预训练，转变为跨任务、跨物种的自监督掩码建模。预训练数据规模达到 367 小时 Utah 阵列记录，涵盖人类和猴子的言语及手臂运动任务。这一策略的核心洞察在于：大规模自监督预训练能够学习稳定的神经表征，这些表征可以跨任务（尝试性言语和想象性言语）迁移。证据锚点明确提及“a transformer neural encoder pretrained with self-supervised masked modeling on 367 hours of Utah array recordings from humans and monkeys across speech and arm-related motor tasks”，置信度 0.95。

3. **解码器类型**：从 n-gram 语言模型（级联）或文本 LLM（端到端），切换为音频 LLM（如 Aero1-Audio 1.5B）。实验表明，在模型规模相近时，基于音频的 LLM 在端到端解码中优于基于文本的 LLM（Figure 3C–D，置信度 0.95）。这一结果暗示音频 LLM 的预训练表征空间与神经编码器的输出表征存在更自然的对齐。

4. **训练目标**：从仅交叉熵损失（端到端）或 CTC 损失（级联），变为交叉熵损失 + 对比学习损失（InfoNCE）。对比学习通过对称 InfoNCE 损失对齐神经和文本嵌入空间，使小规模音频 LLM 在端到端解码中显著优于文本 LLM。总损失函数定义为 $\mathcal{L}_{\text{BIT}} = \mathcal{L}_{\text{CE}} + \mathcal{L}_{\text{contrastive}}$，置信度 0.95。

5. **LLM 微调方法**：从全参数微调变为 LoRA（低秩适配），仅更新 LLM 注意力和前馈层中的线性层子集。这一设计在保持模型性能的同时显著降低了计算开销，证据锚点明确提及“We apply low-rank adaptation (LoRA) to a subset of LLM parameters”，置信度 0.95。

**决定性证据强度：**
- BIT 将先前端到端方法的 WER 从 24.69% 降至 10.22%（置信度 0.95）。
- 在级联设置中，预训练编码器在 Brain-to-Text '24 和 '25 基准上建立了新的 SOTA（置信度 0.95）。
- BIT 级联+集成在 Brain-to-Text '24 保留集上达到 5.10% WER，在 '25 公共排行榜上达到 1.76% WER（置信度 1.0）。
- 在想象性言语解码（50词词汇表）中，BIT-All 在级联和端到端设置下均优于所有其他基线（置信度 1.0）。

**消融实验揭示的因果机制：**
- 音频 LLM 优于文本 LLM（置信度 0.95），说明音频预训练表征与神经编码器输出存在更好的模态对齐。
- 对比学习进一步提升性能（置信度 0.9），证实模态对齐是端到端解码的关键瓶颈。
- 小规模 LLM 在有限标注数据下通常比大规模 LLM 取得更低 WER（置信度 0.85），暗示在标注数据稀缺的场景下，模型容量与数据量之间存在权衡。
- 人类数据带来的性能提升大于跨物种（猴子）数据（置信度 0.95），说明任务相关性比数据量更为关键。
- 在控制数据量时，监督预训练与自监督预训练在想象性言语解码上无显著差异（置信度 1.0），提示自监督预训练的核心优势可能主要来自数据量的规模效应，而非预训练范式本身。这一发现需要进一步验证。

**因果链总结：** 跨物种自监督预训练 → 稳定的神经表征 → 跨任务迁移能力 → 对比学习对齐神经-文本嵌入空间 → 小规模音频 LLM 实现高效端到端解码。这一链条的每个环节都通过消融实验得到了验证，且最终 WER 的显著下降（从 24.69% 到 10.22%）提供了强有力的因果证据。

## 整体框架

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/001_Figure_1.jpg]]
*Figure 1: Schematic illustration of BIT. (A) BIT is an end-to-end speech decoding framework that translates neural activity directly into text by combining a cross-task, cross-species pretrained neural encoder with an audio-LLM decoder. The data are separately obtained and preprocessed from each study. (Appendix A). (B) The neural encoder is a transformer that embeds 20 ms bins of thresholded spikes and spike-band power into multi-bin time patches. It is pretrained using SSL with time-patch masking, reconstructing patch tokens via subject-specific linear read-in and read-out layers with an MSE loss. After pretraining, the masking module is removed, and the encoder is fine-tuned for phoneme decoding u...*

BIT（BraIn-to-Text）是一个端到端的语音解码框架，其核心设计理念是将**跨任务、跨物种预训练的Transformer神经编码器**与**音频大语言模型（audio-LLM）解码器**相结合，直接从神经活动解码为文本。其整体pipeline由四个核心模块串联组成，形成两条可选的推理路径。

**神经编码器（Transformer）** 是整个框架的基石。它接收预处理后的神经活动数据——将20ms时间bin内的阈值化尖峰信号（thresholded spikes）和尖峰带功率（SBP）组合，并按 $T_{\text{patch}}$ 个时间bin分组为patch，得到形状 $(T/T_{\text{patch}}, C \times T_{\text{patch}})$ 的输入张量。编码器采用RoPE相对位置编码和双向注意力掩码，使每个时间patch能够关注所有其他patch。该编码器首先通过**自监督掩码建模**（masked autoencoder风格）在367小时的Utah阵列数据（来自人类和猴子的言语及手臂运动任务）上进行大规模预训练，重建被掩码的patch token。预训练后，掩码模块被移除，编码器进入两个不同的微调分支。

**分支一：级联解码路径。** 编码器输出经线性分类器，使用CTC损失微调为音素解码器。推理时，音素序列通过5-gram语言模型进行束搜索，再经OPT句子重打分，生成最终文本。这条路径是计算高效的基线。

**分支二：端到端解码路径。** 这是BIT的主要创新所在。编码器输出通过一个浅层MLP投影器（Linear, ReLU, Linear）映射到audio-LLM的文本嵌入空间。在此基础上，引入**模态对齐器**：通过对比学习（对称InfoNCE损失）将平均池化的神经嵌入和文本嵌入投影到共享潜在空间，进行L2归一化后优化。最终，在神经嵌入token和文本嵌入token之间插入提示词"decode the above neural activity into an English sentence:"，送入audio-LLM解码器生成句子。微调时，更新神经编码器、投影器，并对audio-LLM的注意力和前馈层应用LoRA低秩适配，其余参数冻结。

**关键因果机制**：该框架的瓶颈在于传统级联方法无法端到端联合优化，且RNN编码器在小数据集上表现有限。BIT通过三个核心设计打破这一瓶颈：1）大规模自监督预训练学习稳定的跨任务神经表征；2）对比学习对齐神经和文本嵌入空间，使小规模audio-LLM能够有效利用神经表征；3）LoRA高效微调使有限标注数据足以驱动端到端优化。

**数据流**：原始神经活动 → 20ms bin + z-score跨天归一化 → 组合特征（阈值化尖峰+SBP）→ patch化 → Transformer编码器 → 端到端路径（MLP投影器 → 模态对齐 → audio-LLM解码）或级联路径（CTC分类 → n-gram LM → 句子重打分）→ 最终文本。

## 核心模块与公式推导

### 神经编码器：Transformer架构与掩码预训练

BIT的核心创新在于其神经编码器，一个使用**自监督掩码建模**在大规模数据上预训练的Transformer。该编码器将20 ms时间bin的神经活动（阈值化锋电位和锋电位带功率）分组为时间块（patch）。给定总时间bin数 $T$ 和块大小 $T_{\mathrm{patch}}$，数据被重塑为形状 $( T / T_{\mathrm{patch}}, \mathsf{C} \times T_{\mathrm{patch}} )$，其中 $\mathsf{C}$ 为电极数。编码器使用**旋转位置编码（RoPE）**编码时间信息，并采用**双向注意力掩码**，允许每个时间块关注所有其他块。预训练阶段采用类似掩码自编码器的策略：随机遮蔽一部分时间块，通过受试者特定的线性读入/读出层（使用MSE损失）重建被遮蔽块的神经活动。预训练完成后，移除遮蔽模块，编码器进入下游微调阶段。

### 级联解码：CTC音素解码 + n-gram语言模型

在级联设置中，预训练后的编码器首先使用**连接主义时序分类（CTC）损失**微调为音素解码器。CTC损失 $\mathcal{L}_{\mathrm{CTC}}$ 允许在输入序列长度大于输出序列长度时进行序列对齐，无需强制对齐。解码时，CTC输出的音素序列通过一个5-gram语言模型和束搜索（beam search）解码为单词序列，再使用OPT句子重评分（OPT sentence re-scoring）进行优化。该级联路径是BIT在Brain-to-Text基准上取得SOTA性能的基础。

### 端到端解码：音频LLM + 对比学习对齐

BIT的端到端框架将神经编码器与一个**音频大语言模型（audio-LLM）解码器**直接连接。神经编码器的输出通过一个浅层**MLP投影器**（Linear, ReLU, Linear）映射到音频LLM的文本嵌入空间。解码时，在神经嵌入token和文本嵌入token之间插入提示“decode the above neural activity into an English sentence:”。微调过程中，更新神经编码器、投影器，并对音频LLM的注意力层和前馈层应用**低秩适配（LoRA）**，其余参数冻结。

端到端训练目标由两部分组成：

1.  **交叉熵损失**：用于神经到文本的翻译，公式为：
    
$$
\mathcal{L}_{\mathrm{CE}} = -\frac{1}{B}\sum_{i=1}^{B}\sum_{t=1}^{L_i}\log\hat{p}_{i,t}(y_{i,t})
$$

    其中 $B$ 为批次大小，$L_i$ 为第 $i$ 个句子的长度，$y_{i,t}$ 为第 $t$ 个位置的真实token，$\hat{p}_{i,t}$ 为模型预测的概率。

2.  **对比学习损失**：用于对齐神经和文本模态的嵌入。一个**模态对齐器**使用独立的线性层将平均池化的神经嵌入token和文本嵌入token投影到共享潜在空间，然后使用**对称InfoNCE损失**进行优化：
    
$$
\mathcal{L}_{\mathrm{contrastive}} = \frac{1}{2B}\sum_{i=1}^{B}\Big[-\log\frac{\exp(\tilde{\mathbf{z}}_i^s\cdot\tilde{\mathbf{z}}_i^t/\tau)}{\sum_{j=1}^{B}\exp(\tilde{\mathbf{z}}_i^s\cdot\tilde{\mathbf{z}}_j^t/\tau)}-\log\frac{\exp(\tilde{\mathbf{z}}_i^t\cdot\tilde{\mathbf{z}}_i^s/\tau)}{\sum_{j=1}^{B}\exp(\tilde{\mathbf{z}}_i^t\cdot\tilde{\mathbf{z}}_j^s/\tau)}\Big]
$$

    其中 $\tilde{\mathbf{z}}_i^s$ 和 $\tilde{\mathbf{z}}_i^t$ 分别为L2归一化后的神经和文本嵌入，$\tau$ 为可学习的温度参数。该损失将同一句子的神经和文本嵌入在潜在空间中拉近，同时将不同句子的嵌入推开。

BIT的总训练目标为两者之和：

$$
\mathcal{L}_{\mathrm{BIT}} = \mathcal{L}_{\mathrm{CE}} + \mathcal{L}_{\mathrm{contrastive}}
$$

### 投影器变体与模型集成

除MLP投影器外，BIT还探索了**交叉注意力投影器**（CrossAttentionProjector），其输出为 $\mathbf{z}^*, \mathbf{A} = \mathrm{CrossAttentionProjector}(\mathbf{z}^s, \mathbf{z}^t)$，其中神经token作为查询（queries），文本token作为键和值（keys and values），实现token级别的模态交互。实验表明，MLP投影器在想象性言语解码上表现最佳（T12: 16.39% WER, T15: 13.61% WER），而交叉注意力投影器性能略低（T12: 17.33% WER, T15: 17.67% WER）。在最终基准提交中，BIT使用**LLM合并**（LLM merging）进行模型集成，将多个微调后的LLM权重进行平均，进一步降低了词错误率（WER）。

## 实验与分析

### 主结果：BIT在言语解码基准上实现SOTA

BIT在Brain-to-Text '24和'25两个基准上均取得了当时的最佳结果。在Brain-to-Text '24保留集（1200句）上，BIT级联+集成（Cascaded + Ensemble）达到了5.10%的词错误率（WER），显著低于之前的最佳方法。BIT端到端+集成（End-to-End + Ensemble）将先前端到端方法的WER从24.69%降低到10.22%（Table 1）。在Brain-to-Text '25公共排行榜上，BIT级联+集成以1.76% WER领先，端到端+集成达到7.76% WER（Table 2）。这些结果明确验证了BIT的核心假设：跨任务、跨物种的自监督预训练能够学习到稳定的神经表征，并在级联和端到端两种解码框架中均实现性能突破。

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/010_Table_2.jpg]]

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/011_Table_2.jpg]]
*Table 2: We benchmark BIT on the Brain-to-Text ’25 hold-out set (1450 sentences), comparing it to other speech BCIs within the same decoding framework (cascaded or endto-end) for fairness. Background colors indicate comparable methods. See the competition leaderboard for more details*

**尝试性言语与想象性言语解码**：Figure 2A显示，对于尝试性言语（大词汇量），预训练编码器（BIT-Human, BIT-All）在级联和端到端设置下均优于RNN和从头训练的Transformer（BIT-TFS）。对于想象性言语（50词词汇表），BIT-All在所有基线中表现最佳（Figure 2B）。值得注意的是，自监督预训练对想象性言语的提升大于尝试性言语，这直接源于想象性言语的标注数据极少，预训练提供的无监督表征学习优势更为突出。

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/009_Figure_2.jpg]]
*Figure 2: Benchmarking BIT versus baselines in attempted and imagined speech decoding. (A) For attempted speech, the pretrained encoder (BIT-Human, BIT-All) outperforms RNN and BIT-TFS using both cascaded and end-to-end approaches. Bar plots show mean WER across competition holdout sentences. (B) For imagined speech (50-word vocabulary), BIT-All outperforms all other baselines in both cascaded and end-to-end settings. Bar plots show mean WER across partitioned test sentences. SSL pretraining provides greater benefits for imagined speech than for attempted speech, since imagined speech has far fewer labeled examples. (C) Scatterplots compare BIT-All vs. BIT-Cross-Task-Only on imagined speech decoding,...*

### 消融实验：解码器模态、模型大小与对比学习

**音频LLM vs. 文本LLM**：Figure 3C–D的关键消融表明，在模型大小相近时，基于音频的LLM（如Aero1-Audio 1.5B）在端到端解码中一致优于基于文本的LLM。其因果机制在于：音频LLM的预训练表征与神经编码器输出的神经嵌入具有更高的表征相似性（RSA分析支持，Figure 4A），从而降低了模态鸿沟。

**模型大小与数据量**：一个反直觉但重要的发现是，在有限标注数据下，小规模LLM（如1.5B参数）通常比大规模LLM（如7B参数）取得更低的WER（Figure 3C–D）。这揭示了当前端到端方法的瓶颈：标注的神经-文本配对数据量不足以支撑大规模LLM的有效微调，导致过拟合。这也是端到端方法（10.22% WER）与级联方法（5.10% WER）存在差距的根本原因。

**对比学习对齐**：在总损失中加入对比学习（对称InfoNCE损失）进一步提升了端到端解码性能（Figure 3C–D），验证了神经-文本嵌入空间的对齐是提升语义一致性的有效因果杠杆。

### 特征与编码器消融

**神经特征组合**：Table 3的消融表明，结合阈值化尖峰（thresholded spikes）和尖峰带功率（SBP）得到最低的音素错误率（PER 17.26%），单独使用任一特征均导致性能下降。这证实了多模态神经特征融合的必要性。

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/017_Table_3.jpg]]
*Table 3: Ablation of features used for speech decoding. Validation PER is reported*

**编码器预训练策略**：Table 4显示，BIT-All在尝试性言语的音素解码上取得最低PER（T12: 14.39%, T15: 7.12%），优于BIT-Human和BIT-TFS。Figure 8的缩放曲线进一步揭示：增加人类预训练数据带来的性能增益大于增加猴子数据，说明跨物种迁移的有效性受限于任务相关性（人类数据包含言语相关任务，猴子数据主要为手臂运动）。

![[assets/figures/papers/iclr26_0002_Lp1noMpMUG_A_cross-species_neural_foundation_model_for_end-/figures/018_Table_4.jpg]]
*Table 4: Phoneme decoding benchmark. The metrics shown are the validation PER*

**预训练数据包含/排除微调集**：Table 8的关键消融表明，在预训练中包含或排除微调数据集对尝试性言语解码性能无显著影响。这证明了BIT的泛化能力——预训练学习的表征并非简单地记忆了微调数据，而是学到了可迁移的神经活动模式。

**监督 vs. 自监督预训练**：Table 9在控制数据量相等时发现，监督预训练（BIT-Cross-Task-Only）与自监督预训练（BIT-SameParticipant-SSL）在想象性言语解码上无显著差异。这提出了一个开放问题：大规模自监督预训练的核心优势是否主要来自更大的数据量，而非自监督目标本身？

### 投影器与集成策略

**投影器变体**：Table 6消融了三种投影器：MLP投影器在想象性言语上取得最低WER（T12: 16.39%, T15: 13.61%），优于线性投影器和交叉注意力投影器。这表明对于小词汇量任务，简单的MLP映射足以实现有效的模态对齐。

**模型集成**：通过LLM合并（LLM merging）实现的模型集成进一步降低了WER（Table 1–2），级联和端到端设置下分别获得约1–2%的绝对提升。这是通过组合多个微调后的解码器权重来减少预测方差。

### 失败模式与错误分析

**音素级混淆**：Figure 6的音素错误矩阵揭示了系统性混淆模式：/D/与/T/反转、/B/与/P/替换、/S/与/Z/混淆，以及中央元音/AH/、/IH/、/EH/的误解码。这些模式与语音学上的最小对立体（minimal pairs）高度一致，表明神经编码器在区分声学上相近的音素时存在固有困难。

**词级混淆**：Figure 7的词级混淆矩阵显示，大多数解码错误发生在拼写或语音形式上相似的词之间（如"their" vs. "there", "our" vs. "hour"）。过滤后仅保留出现至少两次错误的高频混淆对（从734个错误事件减少到58个），进一步凸显了语言模型先验与神经信号之间的交互作用。

**端到端推理速度**：端到端方法每句推理需0.95秒，远慢于级联方法的0.24秒，且当前使用双向注意力无法支持流式解码。这是实现实时BCI应用的主要工程障碍。

## 方法谱系与知识库定位

### 与 Baseline/Follow-up 的关系

BIT 的核心突破在于用 **Transformer 神经编码器 + 跨任务/跨物种自监督预训练** 替换了先前言语 BCI 中普遍使用的 **RNN 编码器 + 纯监督训练** 范式。这一变化直接解决了级联框架无法端到端联合优化的根本瓶颈，并使后续的音频大语言模型（audio-LLM）解码成为可能。具体而言：

- **相对于 RNN 基线**：BIT 的 Transformer 编码器（使用 RoPE 和双向注意力掩码）在音素级解码（phoneme error rate, PER）上即显著优于 RNN（Table 4），这为后续句子级解码提供了更高质量的表征基础。RNN 在小数据集上的表征能力有限，无法充分利用现代 Transformer 架构和大规模预训练的优势。
- **相对于级联框架**：BIT 既保留了级联路径（CTC + n-gram LM），也首次在言语 BCI 中实现了端到端路径。在级联设置中，预训练编码器在 Brain-to-Text '24 和 '25 基准上建立了新的 SOTA（级联+集成在 '24 保留集上达到 5.10% WER，在 '25 公共排行榜上达到 1.76% WER）。在端到端设置中，BIT 将先前端到端方法的 WER 从 24.69% 降低到 10.22%（'24 保留集），降幅超过 50%。
- **相对于文本 LLM 基线**：消融实验（Figure 3C–D）明确表明，同等规模的音频 LLM（如 Aero1-Audio 1.5B）在端到端解码中一致优于文本 LLM。这一发现揭示了神经表征与音频表征之间的内在相似性（Figure 4A 的 RSA 分析证实了这一点），是 BIT 方法设计中的关键因果旋钮。

### 适用边界

BIT 的适用性受以下条件约束：

- **数据要求**：预训练阶段需要大规模（367 小时）的 Utah 阵列颅内记录，且需覆盖多个任务（言语、手部运动）和多个物种（人类、猴子）。这一数据门槛目前仅少数实验室能够满足。消融实验（Figure 8）表明，人类数据的贡献远大于跨物种（猴子）数据，因此获取更多人类数据是提升性能的最直接路径。
- **任务类型**：BIT 在尝试性言语（大词汇量）和想象性言语（50 词小词汇量）上均有效，但提升幅度不同。自监督预训练在想象性言语上带来的增益更大（Figure 2B），因为想象性言语的标注数据极少，预训练提供的通用神经表征弥补了这一不足。这一现象暗示 BIT 在标注稀缺场景下具有更大优势。
- **解码速度**：端到端方法推理速度慢于级联方法（每句 0.95 秒 vs 0.24 秒），尚不满足实时 BCI 应用的需求。这一瓶颈主要来自 LLM 解码器的自回归生成过程。
- **模型规模**：消融实验（Figure 3C–D）发现，在有限标注数据下，小规模 LLM（如 1.5B 参数）反而比大规模 LLM（如 7B 参数）取得更低的 WER。这意味着 BIT 的端到端路径目前无法从更大的语言模型中获益，这限制了其上限。

### 局限与开放问题

1. **端到端 vs 级联的差距**：端到端方法的 WER（10.22%）仍显著高于级联方法（5.10%），差距约 5 个百分点。这一差距的根源在于 LLM 解码器需要从有限的神经标注数据中学习语言模型，而级联方法可以独立使用大规模文本语料训练的 n-gram LM。如何通过更好的模态对齐、提示设计或数据增强来缩小这一差距，是核心开放问题。

2. **流式解码不可用**：当前模型使用双向注意力掩码，无法支持流式解码。引入因果注意力会破坏全局上下文建模，可能导致解码精度下降。如何在保持精度的情况下实现因果化，是走向实际 BCI 应用的必经之路。

3. **大规模 LLM 的失效**：在有限标注数据下，大规模 LLM 反而表现更差。这提示 BIT 的训练范式需要调整——或许需要通过更有效的微调策略（如更好的 LoRA 配置）或获取更多标注数据来解锁大规模 LLM 的潜力。

4. **预训练数据依赖**：BIT 依赖大量私有人类数据，数据获取和隐私问题限制了方法的广泛采用。跨物种迁移（猴子数据）带来的增益有限，不能作为人类数据的替代品。如何通过更复杂的建模策略（如跨受试者功能变异性建模）实现有效的监督跨受试者预训练，是一个值得探索的方向。

5. **长期使用问题未解决**：模型未充分处理非平稳性、神经可塑性和用户-界面协同适应等长期 BCI 使用中的关键挑战。这些因素在实际部署中可能导致性能随时间退化。

6. **自监督预训练的本质优势**：在控制数据量时，监督预训练与自监督预训练在想象性言语解码上性能相当（Table 9）。这引发了一个根本性问题：大规模自监督预训练的核心优势是否仅仅来自数据量的增加，而非自监督目标本身？如果是，那么获取更多标注数据可能比设计更复杂的自监督目标更为有效。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_cross_species_neural_foundation_model_for_end_to_end_speech_decoding.pdf

![[paperPDFs/ICLR_2026/A_cross_species_neural_foundation_model_for_end_to_end_speech_decoding.pdf]]
