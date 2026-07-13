---
title: "Bee: A High-Quality Corpus and Full-Stack Suite to Unlock Advanced Fully Open MLLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bee_A_High_Quality_Corpus_and_Full_Stack_Suite_to_Unlock_Advanced_Fully_Open_MLLMs.pdf
project_link: https://open-bee.github.io/Bee
code_link: null
aliases:
- HD
- Bee
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过 HoneyPipe 对多源多模态指令数据进行去噪、短 CoT 增强、长 CoT 增强和验证，并用所得 Honey-Data-15M 训练 Bee-8B。"
primary_logic: |
  Bee 先聚合社区多模态数据并做去重、领域标注、规则过滤和模型过滤，降低图文不匹配与格式噪声。
  然后用短 CoT 与长 CoT 两级增强补充推理路径，并通过 LLM-as-a-Judge 进行保真度验证，形成 Honey-Data-15M。
  最后通过 MLP 预热、视觉-语言对齐、大规模 SFT、高质量子集精炼和 GRPO 强化学习训练 Bee-8B，验证数据质量优先策略。
claims:
- "系统性数据清洗和双层级 CoT 增强能显著缩小全开放 MLLM 与半开放模型之间的性能差距。"
- "HoneyPipe 提供了透明、可复现的数据策展流水线，可替代昂贵人工标注形成高质量 SFT 数据。"
- "Bee-8B 在多个多模态理解和推理基准上达到或超过 InternVL3.5-8B 等半开放 8B 模型。"
---

# Bee: A High-Quality Corpus and Full-Stack Suite to Unlock Advanced Fully Open MLLMs

> [!tip] 核心洞察
> 通过构建一个透明、可复现的模型驱动数据流水线（HoneyPipe），对大规模原始数据进行去噪和双层级CoT增强，能够使全开放8B模型（Bee-8B）达到与半开放模型（如InternVL3.5-8B）竞争的性能，证明了数据质量优先策略是缩小全开放与半开放模型差距的关键路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Bee：高质量语料库与全栈套件，解锁先进的全开放多模态大语言模型 |
| 英文题名 | Bee: A High-Quality Corpus and Full-Stack Suite to Unlock Advanced Fully Open MLLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IVluwK8q9q) · [Project](https://open-bee.github.io/Bee) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | HoneyPipe (数据流水线) 和 DataStudio (数据策展框架) |
| Dataset | MMMU, MMStar, MMMU-Pro, CountBench |

> [!tip] 效果简介
> - MMMU 上，Score 为 66.8，对比 InternVL3.5-8B: 65.5，变化 +1.3。
> - MMStar 上，Score 为 71.4，对比 InternVL3.5-8B: 67.7，变化 +3.7。
> - MMMU-Pro 上，Score 为 50.7，对比 InternVL3.5-8B: 49.5，变化 +1.2。

## 概要

本文提出了一套全栈开放多模态大语言模型（MLLM）解决方案，包括高质量监督微调（SFT）数据集 **Honey-Data-15M**、数据策展流水线 **HoneyPipe** 及其底层框架 **DataStudio**，以及基于此训练的8B参数模型 **Bee-8B**。核心贡献在于通过系统性的数据清洗和双层级思维链（CoT）增强策略，构建了一个约1500万问答对的高质量SFT数据集，使全开放模型Bee-8B在多个基准上达到与半开放模型（如InternVL3.5-8B）竞争甚至超越的性能，建立了全开放MLLM的新最优水平（SOTA）。

现有开源SFT数据集普遍存在两大根本性质量问题：一是广泛的数据噪声，包括事实错误、图文不匹配和格式缺陷；二是复杂推理数据的严重不足，特别是缺乏链式思维（Chain-of-Thought, CoT）数据。这些问题导致全开放MLLM与半开放或闭源模型之间存在显著的性能差距。论文指出，数据质量是核心可调节变量，通过系统性的数据清洗和双层级CoT增强，可以显著提升模型性能。

## 核心方法与创新机理

1. **Honey-Data-15M数据集**：约1500万问答对的高质量SFT数据集，通过系统清洗和双层级CoT增强构建。
2. **HoneyPipe数据策展流水线**：开源、模型驱动的自动化数据策展流程，从清洗到增强完全自动化，作为昂贵人工标注的可扩展且经济的替代方案。
3. **双层级CoT增强策略**：短CoT（约1210万对，用于中等推理）和长CoT（约290万对，用于复杂指令），通过保真度验证确保事实一致性。
4. **五阶段训练策略**：MLP预热、视觉-语言对齐、大规模SFT（15M）、高效精炼SFT（1M）、GRPO强化学习（50K）。
5. **Bee-8B模型**：基于Qwen3-8B和SigLIP2视觉编码器，在Honey-Data-15M上训练，建立全开放MLLM新SOTA。

整体框架由数据策展流水线（HoneyPipe）和模型训练流水线两部分组成。

**HoneyPipe流水线**（Figure 1）包含四个阶段：
- **Stage 1: 数据聚合与准备**：从多个社区数据集（如LLaVA-OneVision、PixMo、MAmmoth-VL等）聚合约2400万图文对，进行对级去重（感知哈希+simhash）和源级领域标注。
- **Stage 2: 噪声与无关性过滤**：集成规则过滤（小图像、极端宽高比、重复文本）和模型过滤（Qwen2.5-VL-72B评估图文一致性）。
- **Stage 3: 短CoT增强与验证**：对需要中等推理的指令，使用Qwen2.5-VL-72B/32B生成逐步推理路径，并通过LLM-as-a-Judge进行保真度验证。
- **Stage 4: 长CoT增强循环**：对未通过验证或来自复杂来源的指令，使用顶级专有MLLM生成详细长CoT，再次进行保真度验证。

**模型训练流水线**（Table 1）包含五个阶段：
- **Stage 1: MLP预热**：仅训练MLP投影器，约100万图文对。
- **Stage 2: 视觉-语言对齐**：解冻所有组件，约1260万视觉-语言对+143万纯文本样本。
- **Stage 3: 多模态SFT**：在完整Honey-Data-15M（1500万项）上训练一个epoch。
- **Stage 4: 高效精炼SFT**：在Honey-Data-1M（100万高质量子集）上精炼。
- **Stage 5: GRPO强化学习**：在50K项上使用GRPO算法优化。

### 1 数据清洗模块

规则过滤包括：移除小图像、极端宽高比样本、指令中重复文本等格式问题。模型过滤使用Qwen2.5-VL-72B评估图像-指令一致性，确保图文相关。

### 2 双层级CoT增强模块

**短CoT增强**：对需要中等推理的指令，使用Qwen2.5-VL-72B/32B生成逐步推理路径，通过LLM-as-a-Judge进行保真度验证。验证提示要求评判者仅比较最终答案，忽略推理过程中的潜在错误。

**长CoT增强**：对未通过验证或来自复杂来源（如VisualWebInstruct、Vision-R1）的指令，使用顶级专有MLLM生成详细长CoT，结构化标签为`<think></think>`，再次进行保真度验证。

### 3 GRPO强化学习模块

使用Group Relative Policy Optimization (GRPO)算法，基于规则奖励函数：
- 格式奖励（权重0.2）：强制输出中包含`\boxed{}`
- 准确率奖励（权重0.8）：评估`\boxed{}`内内容与标准答案的匹配

### 4 关键公式

在STEM推理案例中，模型使用了以下几何定理：

**中位线性质**：
$$CE = \frac{1}{2} AB$$
在直角三角形中，斜边上的中线等于斜边的一半。

**勾股定理**：
$$CD^2 + DE^2 = CE^2$$
在直角三角形CDE中，直角边平方和等于斜边平方。

**垂直平分线定理**：
$$MA = MB, NA = NC$$
垂直平分线上的点到线段两端点的距离相等。

**弧长公式**：
$$s = \frac{\theta}{360^\circ} \times 2\pi r$$
给定圆心角（度）和半径的弧长。

## 实验与关键发现

### 1 主要结果

Table 2展示了Bee-8B与其他MLLM的全面基准对比。Bee-8B在多个基准上取得全开放模型最佳成绩：

| 基准 | Bee-8B | 最佳半开放模型 | 差值 |
|------|--------|----------------|------|
| MMMU | **66.8** | InternVL3.5-8B: 65.5 | +1.3 |
| MMStar | **71.4** | InternVL3.5-8B: 67.7 | +3.7 |
| MMMU-Pro | **50.7** | InternVL3.5-8B: 49.5 | +1.2 |
| CountBench | **93.0** | InternVL3.5-8B: 90.5 | +2.5 |
| MMVet | **83.9** | InternVL3.5-8B: 82.3 | +1.6 |
| RealWorldQA | **73.1** | InternVL3.5-8B: 71.6 | +1.5 |
| CharXiv DQ | **84.8** | InternVL3.5-8B: 82.5 | +2.3 |
| CharXiv RQ | **57.3** | Keye-VL-8B: 45.4 | +11.9 |
| MathVerse | **67.0** | InternVL3.5-8B: 61.5 | +5.5 |
| LogicVista | **61.3** | InternVL3.5-8B: 57.3 | +4.0 |
| DynaMath worst | **41.3** | InternVL3.5-8B: 38.5 | +2.8 |
| ChartQA test | **86.7** | InternVL3.5-8B: 85.2 | +1.5 |

### 2 消融研究

**Figure 4**的雷达图展示了数据策展流水线的逐步影响：
- 性能层次为 D_curated > D_no-CoT > D_raw
- 从D_raw到D_no-CoT的提升证明了噪声过滤的益处
- 从D_no-CoT到D_curated的跃升证明了CoT增强的直接贡献，尤其在推理密集型领域

**Figure 5**展示了不同1M数据子集微调模型的性能对比：
- 在Honey-Data-1M上微调的模型优于在Random-1M上微调的模型
- 在近一半基准上超越了原始Qwen2.5-VL-7B

### 3 训练阶段分析

Tables 3-6展示了Stage 3、4、5在通用VQA、表格/图表/文档理解、数学/逻辑推理基准上的性能对比：
- Stage 4精炼SFT带来可察觉的性能提升，归因于策展的1M子集的高质量
- Stage 5 GRPO强化学习进一步显著提升性能，主要通过缓解文本重复等生成问题来增强模型可靠性

### 4 评估稳健性

- **跨模型评估一致性**（Table 7）：使用Qwen3-32B和GLM-4.5-FP8作为评判者时，Bee-8B-RL的全局平均分仅相差0.3分（70.2 vs 69.9），表明评估结果稳健。
- **5次独立运行**（Table 8）：标准差极低，证实了模型性能的高度一致性和可复现性。
- **数据去污分析**（Table 10）：在66,682个评估样本中，仅发现29个潜在重叠样本（0.043%），其中2个为精确匹配（0.003%），表明数据污染极低。
- **盲人评估**（Table 9）：532对比较中，准确率维度83.65%持平，推理维度72.74%偏好增强数据，表达风格维度69.92%偏好增强数据。

### 5 公平性说明

- 数据去污分析显示极低的数据污染率。
- 跨模型评估一致性分析显示评估结果稳健。
- 5次独立推理运行的评估结果标准差极低。
- 论文详细列出了所有使用数据集的许可条款（附录G），部分数据集许可信息缺失。

## 定位与知识库关联

### 1 方法谱系

本工作属于数据驱动的MLLM优化范式，与以下工作形成谱系：

- **数据来源**：继承自LLaVA-OneVision (Li et al., 2025a)、PixMo (Deitke et al., 2025)、MAmmoth-VL (Guo et al., 2025c)等社区数据集。
- **数据策展方法论**：区别于仅发布静态数据集的方法，本工作发布完整的可复现数据流水线HoneyPipe和框架DataStudio，提供透明且可适应的方法。
- **推理增强**：双层级CoT增强策略区别于缺乏或仅有简单回答的现有数据集，填补了复杂推理数据的空白。
- **训练策略**：五阶段训练策略（MLP预热→视觉-语言对齐→大规模SFT→精炼SFT→GRPO）区别于通常的单阶段或两阶段SFT。

### 2 知识库定位

本工作在全开放MLLM领域建立了新的性能标杆，证明了数据质量优先策略是缩小全开放与半开放模型差距的关键路径。Bee-8B在多个基准上超越或接近InternVL3.5-8B等半开放模型，为开源社区提供了可复现的高质量数据策展方法论。

### 3 局限性

- 论文未提供Bee-8B在特定任务（如视频理解、多图像推理）上的性能评估。
- 长CoT生成依赖顶级专有MLLM，可能引入这些模型的偏见或错误，且成本较高。
- 数据策展流程中的模型过滤和增强步骤依赖于特定模型（如Qwen2.5-VL-72B），其性能可能影响最终数据质量。
- 部分数据集的许可信息缺失（如UniChart、UReader KG、SimChart9K等），可能影响数据集的合规使用。
- 论文未详细讨论模型在公平性、偏见或安全性方面的表现。
- Bee-8B的参数量为8B，与更大规模模型（如70B+）的性能差距未探讨。

### 4 开放问题

- HoneyPipe流水线中的规则过滤阈值（如最小图像尺寸、宽高比限制）具体是多少？
- 用于长CoT生成的“顶级专有MLLM”具体是哪些模型？
- Stage 4中使用的Honey-Data-1M子集的具体主题比例构成是什么？
- GRPO阶段的具体奖励函数设计细节（如格式奖励和准确率奖励的权重分配）是否还有优化空间？
- Bee-8B在更多样化的任务（如视频理解、多轮对话、具身推理）上的表现如何？
- Honey-Data-15M数据集是否会导致模型在特定领域（如STEM）过拟合，而牺牲通用能力？
- 数据策展流程中使用的模型（如Qwen2.5-VL-72B）本身是否引入了数据偏差，如何量化？

### 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/001_Figure_1.jpg]]

### 实验与分析

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/004_Figure_3.jpg]]
*Figure 3: Data collection of Honey-Data-15M. A detailed breakdown of our dataset’s composition across seven major categories. The number of samples (in thousands) is listed for each source. The * denotes that the data contains the long CoT response*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/005_Table_1.jpg]]
*Table 1: Detailed configuration for each training stage of Bee-8B*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/006_Table_2.jpg]]
*Table 2: Evaluation of Bee-8B against other MLLMs. We distinguish between fully open (*) and semi-open (†) models. The top and second-best scores for each benchmark are highlighted*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/009_Table_3.jpg]]
*Table 3: Performance comparison of our model after Stage 3, Stage 4, and Stage 5 on general VQA benchmarks (Part 1). The top and second-best scores for each benchmark are highlighted*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_IVluwK8q9q_Bee_A_High-Qual/figures/010_Table_4.jpg]]
*Table 4: Performance comparison of our model after Stage 3, Stage 4, and Stage 5 on general VQA benchmarks (Part 2). The top and second-best scores for each benchmark are highlighted*

## 原文 PDF

![[paperPDFs/ICLR_2026/Bee_A_High_Quality_Corpus_and_Full_Stack_Suite_to_Unlock_Advanced_Fully_Open_MLLMs.pdf]]
