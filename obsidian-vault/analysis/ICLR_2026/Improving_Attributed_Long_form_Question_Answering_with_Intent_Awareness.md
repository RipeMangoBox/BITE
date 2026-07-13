---
title: "Improving Attributed Long-form Question Answering with Intent Awareness"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Improving_Attributed_Long_form_Question_Answering_with_Intent_Awareness.pdf
project_link: null
code_link: https://github.com/colinzhaoust/intent-aware-deep-research
openreview_forum_id: fRCm5c8x0j
aliases:
- IAWF
- IALFQAIA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "在报告的生成过程（推理和训练）中显式引入结构化的段落意图和引文意图，以标签化格式（意图类型+理由）为模型提供写作过程的元认知指导。"
primary_logic: "通过强制模型在生成时考虑每个段落和每条引文的功能目的，可以显著提升科研长报告的整体质量、引用准确性和信息组织，且该能力可通过教师模型蒸馏高效传递给小模型。"
claims:
- "意图感知使大模型在三个基准上的宏平均性能绝对提升 +2.9 点，小模型通过意图感知 SFT 提升 +12.3 点。"
- "意图感知显著改善归因：大模型引文指标平均提升 +3.7 点，小模型平均提升 +18.7 点。"
- "段落意图和引文意图互补：同时使用两者在 SQA-CS-V2 上获得最佳表现（Overall 89.7），优于仅用一种或无意图，且优于 CoT 和 ReAct 推理。"
- "用户研究表明意图标注帮助读者预判段落内容和决定是否深入阅读（Likert 评分从基线 3.84 提升至 4.47）。"
---

# Improving Attributed Long-form Question Answering with Intent Awareness

> [!tip] 核心洞察
> 通过强制模型在生成时考虑每个段落和每条引文的功能目的，可以显著提升科研长报告的整体质量、引用准确性和信息组织，且该能力可通过教师模型蒸馏高效传递给小模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过意图感知改进带归因的长篇问答 |
| 英文题名 | Improving Attributed Long-form Question Answering with Intent Awareness |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fRCm5c8x0j) · [GitHub](https://github.com/colinzhaoust/intent-aware-deep-research) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | Intent-aware Writing Framework |
| Dataset | SQA-CS-V2, DeepScholar Bench |

> [!tip] 效果简介
> - SQA-CS-V2 上，Overall (macro-average) 为 89.7 (gemini-2.5-pro + intent)，对比 88.1 (gemini-2.5-pro)，变化 +1.6。
> - SQA-CS-V2 上，Citation Precision (Citation P) 为 95.7 (gemini-2.5-pro + intent)，对比 93.2 (gemini-2.5-pro)，变化 +2.5。
> - SQA-CS-V2 上，Citation Recall (Citation R) 为 86.1 (gemini-2.5-pro + intent)，对比 82.4 (gemini-2.5-pro)，变化 +3.7。

## 概要

当前长文本问答系统在生成带归因的科学报告时，仅从最终文本中隐式学习写作模式，缺乏对作者在段落组织与引文选择背后的**意图**进行显式建模。这一瓶颈导致生成内容在归因充分性、引用质量与可读性上均存在不足。

本文提出**意图感知写作框架（Intent-aware Writing Framework）**，核心思路是将写作过程的结构化元认知——段落意图（Paragraph Intent）与引文意图（Citation Intent）——以标签化格式显式注入报告的生成过程。具体而言，模型在推理时被要求在每个段落前嵌入 `<bpit>[意图类型]: 理由 <epit>`，在每条引文后嵌入 `<bcit>[意图类型]: 理由 <ecit>`，从而强制模型在生成时考虑每个段落和每条引文的功能目的。

**核心结论**：
- 意图感知使大模型在三个基准上的宏平均性能绝对提升 **+2.9 点**，小模型通过意图感知 SFT 提升 **+12.3 点**。
- 归因指标显著改善：大模型引文指标平均提升 **+3.7 点**，小模型平均提升 **+18.7 点**。
- 段落意图与引文意图互补：同时使用两者在 SQA-CS-V2 上取得最佳 Overall 89.7，优于仅用一种或无意图，且显著优于 CoT 和 ReAct 推理。
- 用户研究表明，意图标注帮助读者预判段落内容并决定是否深入阅读（Likert 评分从基线 3.84 提升至 4.47）。

该方法通过教师模型（gemini-2.5-pro）蒸馏生成带意图标签的合成训练数据，使小模型（如 qwen3-8b）在 SQA-CS-V2 上以 Overall 88.6 超越大模型基线（gemini-2.5-pro 88.1），验证了意图感知能力可高效传递给小模型。



当前长文本问答系统在生成科学深度研究报告时面临一个关键瓶颈：模型仅从最终报告文本中隐式学习写作风格，缺乏对作者在段落组织与引文选择背后**意图**的显式建模。这种“只看结果、不问目的”的学习方式导致生成内容在归因充分性、引用质量与可读性三个维度上均存在显著不足——引用往往缺乏明确的功能目的，段落之间的信息组织缺少清晰的修辞逻辑，读者难以预判内容走向或判断引文的支撑强度。

现有方法主要通过直接生成或基于最终报告文本的监督微调来训练模型，隐含地假设写作意图可以从表面文本中自动习得。然而，写作本质上是一个**目的驱动的认知过程**：作者选择引用某篇文献是为了提供背景、说明方法来源或进行对比；组织一个段落是为了下定义、展开论述或提出问题。当这些结构化意图信息在训练和推理中完全缺失时，模型只能模仿表层语言模式，难以掌握深层的信息组织策略。

本文的核心动机在于：**能否在报告的生成过程中显式引入结构化的段落意图和引文意图，为模型提供写作过程的元认知指导？** 具体而言，我们提出一个意图感知写作框架，在推理和训练两个阶段以标签化格式（意图类型 + 理由）嵌入意图信号，使模型在生成每个段落和每条引文时明确考虑其功能目的。这一设计的直觉在于：通过强制模型“思考”每个写作单元的目的，可以显著提升科研长报告的整体质量、引用准确性和信息组织，且该能力可通过教师模型蒸馏高效传递给小模型。

初步证据表明这一方向具有显著潜力：意图感知使大模型在三个基准上的宏平均性能绝对提升 +2.9 点，小模型通过意图感知 SFT 提升 +12.3 点；在归因维度上，大模型引文指标平均提升 +3.7 点，小模型平均提升 +18.7 点。这些结果提示，**显式意图建模可能是突破当前长文本问答归因瓶颈的关键因果杠杆**。



## 核心方法与创新机理

当前长文本问答系统仅从最终报告中隐式学习写作风格，缺乏对作者在段落组织与引文选择背后**意图**的显式建模，导致生成内容的归因不足、引用质量欠佳。本文的核心创新在于将写作过程的元认知——**段落意图**和**引文意图**——以结构化标签格式显式注入模型的推理与训练流程，从而为语言模型提供“为什么这样写、为什么引用这篇文献”的过程性指导。

具体而言，方法在以下两个关键维度上改变了基线行为：

1. **段落级引导**：从基线中仅从最终文本隐式建模，转变为在每个段落前显式插入 `<bpit>[PIT-type]: rationale <epit>` 标签，强制模型在生成前明确该段的功能目的（如 Exposition、Definition、Compare and Contrast 等话语模式类型）。
2. **引文语境化**：从基线中无显式意图的引用方式，转变为在引用句后附加 `<bcit>[CIT-type]: rationale <ecit>` 标签，要求模型阐明每条引文的具体功能（如 Background、Motivation、Uses 等六类 ACL-ARC 框架）。

这一设计形成了两个可操作的 pipeline 模块：
- **意图感知推理**（Verbalized Intents）：在推理时通过 prompt 引导模型生成内嵌意图标签的报告，可视为 test-time scaling 的一种变体。
- **意图感知 SFT 数据蒸馏**：用大型教师模型（gemini-2.5-pro）在意图感知条件下生成合成训练数据，再通过三种变体（intent-explicit、intent-implicit、intent-multiview）微调小模型，使小模型继承意图感知能力。

**决定性证据**（Table 5）表明，段落意图与引文意图具有互补性：在 SQA-CS-V2-dev 上同时使用两者时 Overall 达到 89.7，优于仅用引文意图（88.6）、仅用段落意图（89.1）和无意图基线（88.1），且显著优于 CoT（81.3）和 ReAct（77.6）。这一差距验证了显式意图建模相对于通用推理策略的独特增益，而非简单增加推理计算量所能替代。



![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/001_Figure_1.jpg]]
*Figure 1: Current long-form question answering systems don’t consider intents when generating responses. The figure above shows how having explicit citation intents and paragraph intents helps reason about the text and generate better responses*

![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/002_Table_1.jpg]]
*Table 1: The types and descriptions for our intent awareness schemes. We adopt the citation intent types from ACL-ARC (Jurgens et al., 2018) and extend the paragraph intent types from the discourse modes studied in (Song et al., 2017)*

本文提出的意图感知写作框架（Intent-aware Writing Framework）旨在解决当前长文本问答系统的一个核心瓶颈：现有方法仅从最终报告中隐式学习写作风格，缺乏对作者在段落组织与引文选择背后意图的显式建模，导致归因不足、引用质量与可读性欠佳。该框架通过在报告生成过程中显式引入结构化的段落意图与引文意图，为模型提供写作过程的元认知指导。

### 框架总览

框架由两个核心层次构成，如 Figure 1 所示：

1. **段落级意图（Paragraph-level Intents）**：在生成每个段落之前，模型需明确该段落的功能目的（如 Exposition、Definition、Compare and Contrast、Problem-solution 等），并以标签化格式嵌入报告中。意图类型体系扩展自 Song et al. (2017) 的话语模式研究（Table 1）。

2. **句子级引文意图（Citation Intents）**：在引用文献的句子之后，模型需标注该引用的功能目的（如 Background、Motivation、Uses 等），采用 ACL-ARC (Jurgens et al., 2018) 的六分类框架（Table 1）。

两种意图均以内联标签加理由（rationale）的格式表示：`<bpit>[意图类型]: 理由<epit>` 用于段落意图，`<bcit>[意图类型]: 理由<ecit>` 用于引文意图。这一表示方式受 STaR 和 ToW 方法启发，使模型在生成文本的同时输出其写作决策的元信息。

### 流水线模块

框架通过两个阶段将意图感知能力注入模型：

**阶段一：意图感知推理（Verbalized Intents）**
在推理时，直接通过提示要求模型在生成报告的过程中嵌入段落意图与引文意图标签。该策略可视为测试时缩放的一种变体，适用于任何具有足够指令遵循能力的大模型（如 gemini-2.5-pro、Claude opus-4、o3）。消融实验（Table 5）表明，同时使用段落意图与引文意图在 SQA-CS-V2-dev 上取得最佳 Overall 89.7，显著优于仅用单一意图类型（citation-only: 88.6, paragraph-only: 89.1）和无意图基线（88.1），且远优于 CoT（81.3）和 ReAct（77.6）等替代推理方法。

**阶段二：意图感知训练与蒸馏**
1. **教师数据生成**：使用大模型（gemini-2.5-pro）在意图感知提示下生成包含意图标签的合成训练报告。训练数据来自 OpenScholar 中随机采样的 1,000 个查询。
2. **多视图 SFT 变体**：对每个数据点生成四个指令-报告对——intent-explicit（同时含两种意图）、paragraph-intent（仅段落意图）、citation-intent（仅引文意图）、no-intent（无意图）。在此基础上训练三个 SFT 变体：
   - **intent-explicit**：仅在 intent-explicit 版本上训练
   - **intent-implicit**：仅在 no-intent 版本上训练，但训练数据本身由意图感知教师模型生成
   - **intent-multiview**：在所有四个版本上训练，使模型见过多种意图组合模式

为公平比较，多视图变体使用 1/4 训练步数以控制总计算量。基础模型采用 qwen3-4B/8B 和 llama3.1-8B。

### 输入输出规范

- **输入**：固定检索结果集（控制检索质量对写作性能的干扰），包含用户查询及相关候选文献信息。
- **输出**：带归因的科学长报告，其中段落以 `<bpit>` 标签开头标注意图，引文句以 `<bcit>` 标签结尾标注引用目的。在用户界面中，这些意图标签可被渲染为可读的提示信息，帮助读者预判段落内容和引用理由（用户研究 Likert 评分从基线 3.84 提升至 4.47）。

### 关键机制与证据强度

框架的核心因果机制在于：通过强制模型在生成时显式考虑每个段落和每条引文的功能目的，将隐式的写作规划过程外化为可监督的元认知步骤。决定性证据包括：
- 大模型在三基准上宏平均性能绝对提升 +2.9 点，小模型通过意图感知 SFT 提升 +12.3 点（Abstract, Section 4.2）
- 归因指标显著改善：大模型引文指标平均提升 +3.7 点，小模型平均提升 +18.7 点（Tables 2, 4）
- 段落意图与引文意图互补：同时使用两者获得最佳表现（Table 5）
- 意图感知训练使小模型对检索候选信息的利用率提升约 0.2→0.4，与大模型的引用重叠度从约 0.6 提升至 0.8（Figure 2），表明检索信息利用更充分



### 意图感知写作框架

本工作提出 **Intent-aware Writing Framework**，其核心瓶颈在于：当前长文本问答系统仅从最终报告中隐式学习写作风格，缺乏对作者在段落组织与引文选择背后的**功能目的**进行显式建模，导致归因不足、引用质量与可读性欠佳。该框架通过两个关键模块将写作过程的元认知信号显式注入生成流程：

1. **段落级意图 (Paragraph-level Intents)**：在每段正文前，以标签化格式 `<bpit>[意图类型]: 理由 <epit>` 显式声明该段落的修辞功能（如 Exposition、Definition、Compare and Contrast、Problem-Solution 等），引导模型在组织信息时具备结构意识。
2. **引文级意图 (Citation-level Intents)**：在每条引文句后，以 `<bcit>[意图类型]: 理由 <ecit>` 标注该引用的功能目的（采用 ACL-ARC 的六分类体系：Background、Motivation、Uses、Extension、Comparison、FutureWork），强制模型为每次引用提供功能理由。

这两个模块通过**口头化意图 (Verbalized Intents)** 在推理时直接生效：模型被提示在生成报告的过程中同步输出意图标签，形成“意图-内容”交织的生成轨迹。该方法可视为测试时缩放 (test-time scaling) 的一种变体。

### 训练阶段：意图感知监督微调

在训练阶段，框架利用大模型（gemini-2.5-pro）以意图感知方式生成合成数据，并通过三种 SFT 变体将意图信号蒸馏至小模型：

- **Intent-explicit SFT**：训练数据与推理时均保留完整的意图标签，模型学习显式生成意图。
- **Intent-implicit SFT**：训练数据包含意图标签，但推理时不输出标签，仅利用训练中习得的隐式意图规划能力。
- **Intent-multiview SFT**：对同一数据点生成四个指令-报告对（intent-explicit、paragraph-intent-only、citation-intent-only、no-intent），模型在 4 倍数据量上训练，推理时可按需切换模式。

为保证公平比较，multiview 变体使用 1/4 训练步数控制总计算量。

### 公式推导

本文未引入新的数学公式。意图表示采用标签化模式，而非概率图或优化目标形式。其核心机制可概括为以下生成范式转变：

- **基线生成**：$P(\text{report} \mid \text{query}, \text{retrieved\_docs})$
- **意图感知生成**：$P(\text{report}, \text{intents} \mid \text{query}, \text{retrieved\_docs})$

其中 $\text{intents}$ 为段落意图与引文意图的序列。推理时模型联合生成内容与意图，训练时通过教师强制 (teacher forcing) 学习该联合分布。这一范式转变的因果效应已在多基准上得到验证：大模型宏平均性能绝对提升 +2.9 点，引文指标提升 +3.7 点；小模型经意图感知 SFT 后宏平均提升 +12.3 点，引文指标提升 +18.7 点（详见 Table 2、Table 4）。



## 实验与关键发现

### 核心瓶颈与因果机制

当前长文本问答系统仅从最终报告中隐式学习写作风格，缺乏对作者在段落组织和引文选择背后的**意图**进行显式建模。这导致生成内容的归因不足、引用质量欠佳，且可读性受限。本文提出的**意图感知写作框架（Intent-aware Writing Framework）** 通过在生成过程中显式引入结构化的段落意图（Paragraph Intent, PIT）和引文意图（Citation Intent, CIT），以标签化格式（`<bpit>[意图类型]: 理由 <epit>` 和 `<bcit>[意图类型]: 理由 <ecit>`）为模型提供写作过程的元认知指导。这一设计本质上是一个**因果调节旋钮**：强制模型在生成每个段落和每条引文时考虑其功能目的，从而显著提升科研长报告的整体质量、引用准确性和信息组织。

### 主实验结果

#### 大模型意图感知推理

在 SQA-CS-V2 基准上，意图感知推理使三个主流大模型均获得一致的性能提升（Table 2）：
- **gemini-2.5-pro**：Overall 从 88.1 提升至 **89.7**（+1.6），Citation Recall 从 82.4 提升至 **86.1**（+3.7），Citation Precision 从 93.2 提升至 **95.7**（+2.5）。
- **Claude opus-4**：Overall 从 85.4 提升至 **89.0**（+3.6），表现尤为突出。
- **o3**：Overall 从 85.1 提升至 86.0（+0.9），提升幅度相对较小但仍一致。

![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/003_Table_2.jpg]]
*Table 2: Performance comparison across various models on SQA-CS-V2. Overall denotes the macroaverage of other sub-metics. Bold indicates the best-performing row for overall metrics. +intent denotes the use of our intent-aware-writing framework with both paragraph and citaiton intents*

在 DeepScholar Bench 上（Table 3），意图感知同样有效：
- **Claude opus-4**：Overall 从 58.1 提升至 **59.9**（+1.8）。
- **gemini-2.5-pro**：Overall 从 54.8 提升至 57.8（+3.0）。
- **o3** 在 ResearchQA 的 Rubrics 指标上从 76.3 提升至 **79.3**（+3.0）。

**关键结论**：意图感知对大模型的引文指标提升最为显著（平均 +3.7 点），验证了显式引文意图对归因质量的直接改善作用。

#### 小模型意图感知 SFT

通过教师模型（gemini-2.5-pro）生成带意图标签的合成数据进行 SFT，小模型获得大幅提升（Table 4）：
- **qwen3-8b (intent-multiview SFT)**：Overall 达到 **88.6**，超越教师模型 gemini-2.5-pro 的无意图基线（88.1），Citation Recall 从 66.9（无训练）提升至 85.0（intent-explicit SFT），提升 **+18.1** 点。
- **llama3.1-8B (intent-multiview SFT)**：Overall 从 62.9（无训练）提升至 85.7（+22.8）。
- **qwen3-4b (intent-multiview SFT)**：Overall 从 73.5 提升至 79.6（+6.1）。

![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/005_Table_4.jpg]]
*Table 4: SQA-CS-V2 Performance Across different base models and method variants. For each of the intent-aware method variants, the inference prompt explicitly asks the model to use intents*

**关键结论**：意图感知 SFT 使小模型的引文指标平均提升 **+18.7 点**，验证了意图信号可通过蒸馏高效传递给小模型。多视图训练（intent-multiview）在所有 8B 模型上均取得最优结果，表明同时学习多种意图表示格式有助于模型泛化。

### 消融实验

#### 段落意图与引文意图的互补性

在 SQA-CS-V2-dev 上对 gemini-2.5-pro 进行消融（Table 5）：
- **无意图**：Overall 88.1
- **仅引文意图**：Overall 88.6
- **仅段落意图**：Overall 89.1
- **全部意图**：Overall **89.7**

![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/008_Table_5.jpg]]
*Table 5: SQA-CS-V2-dev Performance results with verbalized intents and gemini-2.5-pro. We bold the best row for the Overall metric*

两者同时使用时达到最佳性能，且均显著优于 Chain-of-Thought（CoT，Overall 81.3）和 ReAct（Overall 77.6）推理方法。这表明意图感知提供的结构化元认知指导比通用推理策略更有效。

#### 意图模式设计消融

比较三种意图模式设计（Table 10）：
- **固定模式（current）**：仅使用预定义类型，Overall 89.7
- **自由模式（free）**：模型完全自定义类型，Overall 89.3
- **混合模式（mix）**：允许在常用类型基础上自定义，Overall **91.6**

![[assets/figures/papers/iclr26_0009_fRCm5c8x0j_Improving_Attributed_Long-form_Question_Answerin/figures/014_Table_10.jpg]]
*Table 10: SQA-CS-V2-dev Performance results with verbalized intents and gemini-2.5-pro. We compare variants of intent schema design. free denotes the use of model improvised types. current denotes the use of our schema. mix denotes the use of most frequent types in our schema and let the model has freedom on adding their own. We bold the best row for the Overall metric*

混合模式取得最佳结果，说明在提供结构化指导的同时保留一定灵活性，能更好地适应具体查询的写作需求。

#### 检索信息利用率分析

Figure 2（左）显示，意图感知训练显著提升小模型对检索候选信息的利用率（从约 0.2 提升至约 0.4 的部分）。Figure 2（右）显示，小模型与大模型（gemini-2.5-pro）的引用重叠度从约 0.6 提升至约 0.8，提示意图感知使模型检索更充分、引用选择更接近高质量参考。

#### 跨任务泛化

在 DeepScholar Bench 上（Table 9），qwen3-8b 的 intent-implicit SFT 以 Overall **60.3** 超越所有大模型基线（如 Claude opus-4 的 59.9），验证了意图感知训练的跨任务泛化能力。

### 意图类型分布分析

Table 6 展示了不同模型生成的引文和段落意图类型分布。与人类参考相比，意图感知模型生成的意图类型分布更接近人类写作的功能目的模式，进一步支持了显式意图建模的有效性。

### 公平性说明

所有实验固定检索结果集，仅度量写作性能差异，排除了检索质量的干扰。训练阶段通过使用 1/4 训练步数来统一计算量（因多视图变体生成 4x 数据点），确保 SFT 变体间的公平比较。

### 失败模式与局限

尽管意图感知在多数指标上表现优异，但 Table 2 显示 o3 模型在 SQA-CS-V2 上的提升幅度（+0.9）明显小于其他模型，提示意图感知的收益可能与模型架构或推理能力有关。此外，当前框架依赖预定义的意图类型体系，在领域迁移时可能需要重新设计意图模式。需要人工验证的是：意图标签的生成质量是否在所有查询类型上保持一致，以及意图感知是否会引入额外的推理延迟。



## 定位与知识库关联

### 1. 与现有方法的继承与断裂

本文提出的意图感知写作框架（Intent-aware Writing Framework）与现有长文本问答系统存在根本性的认知断裂，而非增量改进。当前主流系统（如 STORM、AutoSurvey、OpenScholar 等）的核心瓶颈在于：它们仅从最终报告文本中隐式学习写作风格，缺乏对作者在段落组织和引文选择背后意图的显式建模。本文的框架通过引入结构化的段落意图（Paragraph Intent）和引文意图（Citation Intent）标签，将写作过程从“模仿最终产物”转变为“模拟写作决策过程”，这一断裂体现在两个层面：

**从隐式模仿到显式元认知。** 基线方法（Direct Generation）直接生成报告文本，模型对“为何选择这条引文”、“为何在此处展开对比分析”缺乏可追溯的推理链。本文通过在生成过程中嵌入 `<bpit>[PIT-type]: rationale <epit>` 和 `<bcit>[CIT-type]: rationale <ecit>` 标签（Section 3.2），强制模型在生成每个段落和每条引文时进行功能性自我解释。这种设计借鉴了 STaR 和 ToW 的标签化推理格式，但将其从通用推理任务迁移到了结构化写作的特定场景。

**意图类型体系的选择依据。** 引文意图采用 ACL-ARC 的六分类框架（Background、Motivation、Uses 等），该框架已在科学文献引文功能分析中得到充分验证（Jurgens et al., 2018）。段落意图则从话语模式研究中扩展而来（Smith, 2003; Song et al., 2017），包含 Exposition、Definition、Compare and Contrast、Problem-solution 等功能类别（Table 1）。这一选择的合理性在于：话语模式直接捕捉文本段落的交际目的，与长文本问答中“组织信息、构建论证”的需求高度对齐。

### 2. 推理层面的基线对比

在推理层面，本文的意图感知推理（Verbalized Intents）与两种主流推理增强方法形成直接对比：

**vs. Chain-of-Thought (CoT)。** CoT 通过通用推理链提升模型推理能力，但不针对写作任务的结构化需求进行专门设计。消融实验（Table 5）显示，在 SQA-CS-V2-dev 上，CoT 的 Overall 仅为 81.3，而意图感知推理（all intents）达到 89.7，差距达 8.4 点。这一巨大差距表明，通用推理增强无法替代面向写作结构的专门化引导。

**vs. ReAct。** ReAct 将推理与行动交织，适用于需要与外部环境交互的任务，但在固定检索结果的长文本写作场景中，其交织式推理反而可能引入冗余步骤。实验显示 ReAct 的 Overall 仅为 77.6，显著低于意图感知推理。这验证了在检索结果已固定的条件下，结构化的写作规划比通用的推理-行动循环更有效。

### 3. 训练层面的基线对比与蒸馏路径

在训练层面，本文的意图感知 SFT 变体形成了清晰的蒸馏路径：

**教师模型与数据生成。** 使用 gemini-2.5-pro 作为教师模型，在 1,000 个 OpenScholar 随机采样查询上，通过意图感知提示生成合成训练数据（Section 4.1）。每份数据生成四个变体：intent-explicit（同时含段落和引文意图）、paragraph-intent、citation-intent 和 no-intent，构成多视图训练集。

**SFT 变体的设计逻辑。** 三个 SFT 变体对应不同的意图信号保留程度：
- **intent-explicit**：训练和推理均保留完整意图标签，直接学习意图引导的写作模式。
- **intent-implicit**：训练时使用含意图的数据，但推理时不要求输出意图标签，测试隐式知识传递效果。
- **intent-multiview**：在四倍数据量上训练（控制训练步数为 1/4 以保证计算量公平），使模型接触同一内容在不同意图组合下的表达方式。

**性能对比的启示。** 在 SQA-CS-V2 上（Table 4），qwen3-8b 的 intent-multiview SFT 以 Overall 88.6 超越教师模型 gemini-2.5-pro 的无意图版本（88.1），验证了意图感知蒸馏的有效性。更重要的是，intent-implicit SFT 在 DeepScholar Bench 上以 Overall 60.3 超越所有大模型基线（Table 9），表明意图感知训练获得的写作能力具有跨任务泛化性，且不依赖推理时的显式意图标签。

### 4. 适用边界与约束条件

**检索质量的前提假设。** 所有实验均固定检索结果集（Section 4.1），仅度量写作性能差异。这意味着框架的有效性建立在检索质量已达到一定水平的前提下——如果检索结果本身缺乏关键信息，意图引导也无法弥补信息缺失。Figure 2 左图显示，意图感知训练将小模型对检索候选信息的利用率从约 0.2 提升至约 0.4，说明框架能帮助模型更充分地利用已有信息，但不能创造信息。

**意图类型体系的领域依赖性。** 当前引文意图体系源自计算语言学领域（ACL-ARC），段落意图体系源自通用话语模式研究。Table 6 的意图分布统计显示，不同模型生成的意图类型分布存在差异，且与人类参考分布不完全一致。这暗示在科学领域以外的场景（如政策分析、法律文书、人文论述），现有意图类型体系可能需要领域自适应调整。

**模型规模的适用性。** 实验覆盖了从 4B 到大规模闭源模型的多个层级（qwen3-4B/8B、llama3.1-8B、gemini-2.5-pro、Claude opus-4、o3），结果显示意图感知在所有规模上均带来增益，但增益幅度与模型基础能力相关——小模型通过 SFT 获得的相对提升（+12.3 点）远大于大模型通过推理获得的提升（+2.9 点），说明意图感知训练对能力较弱的基础模型具有更强的边际效应。

### 5. 局限与开放问题

**结构表示的表达力上限。** 当前意图表示采用扁平化的标签-理由对，无法捕捉段落间的层级关系或叙事弧线。开放问题指向：能否使用层次化或图结构化的意图表示，使模型在生成时不仅考虑当前段落的局部意图，还能维护全局的叙事连贯性？Table 10 的意图模式消融显示，混合模式（mix）优于纯类型模式（current）和完全自由模式（free），暗示适度的结构化约束优于严格限制或完全放任，但最优的结构化程度仍是一个开放问题。

**意图来源的真实性鸿沟。** 当前意图类型体系基于研究者的人工定义，而非对真实作者写作行为的观测。一个关键的开放问题是：能否基于人类标注或写作行为数据（如键盘记录、修订历史）更精确地建模真实写作意图？这将使意图框架从“规范性指导”转向“描述性建模”，可能进一步提升生成文本的自然度和说服力。

**自我批判与迭代修正的缺失。** 当前框架在生成时一次性输出意图和文本，缺乏对已生成内容的自我评估和修正机制。一个自然的扩展方向是：将意图框架发展为自我批判的脚手架，使模型在生成过程中实时评估自身的结构选择（“当前段落的 Exposition 是否充分铺垫了后续的 Compare and Contrast？”）和引用理由（“这条引文是否真正支持了 Uses 意图，还是仅表面相关？”），并据此进行迭代修正。

**意图类型的自动发现。** 当前意图类型依赖人工预定义，限制了框架在新领域的快速部署。能否从特定领域语料库中自动发现和归纳新的意图类别，减少对预定义模式的人工依赖，是提升框架可扩展性的关键问题。这需要结合无监督聚类、弱监督学习和领域专家验证的混合方法。



## 原文 PDF

![[paperPDFs/ICLR_2026/Improving_Attributed_Long_form_Question_Answering_with_Intent_Awareness.pdf]]
