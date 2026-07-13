---
title: "OpenThoughts: Data Recipes for Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OpenThoughts_Data_Recipes_for_Reasoning_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 7xjoTuaNmN
aliases:
- ODP
- OpenThoughts
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "问题来源的选择、数据过滤与去重策略、教师模型选择以及多答案采样比例是影响下游推理性能的关键可控因素。"
primary_logic: "通过系统地探索SFT数据管道的各个步骤（问题收集、混合、过滤、去重、答案过滤、教师选择），可以以小成本构建出超越更大规模模型的开源推理模型。关键发现包括：从少数高质量来源选择问题比追求多样性更有效；使用更弱的教师模型（QwQ-32B）反而能训练出更强的学生模型；不使用答案过滤优于大多数过滤方法；以及采样多个答案（16×）能有效扩大数据规模并提升性能。"
claims:
- "OpenThinker3-7B在AIME 2025、LiveCodeBench和GPQA Diamond上分别达到53.3%、51.7%和53.7%，比DeepSeek-R1-Distill-Qwen-7B提升约18.8、21.0和20.5个百分点（来自表1）。"
- "选择仅两个最佳代码问题源相比混合16个源，在所有基准上平均准确率提升约5%。"
- "QwQ-32B作为教师模型在所有领域均显著优于DeepSeek-R1（例如代码领域平均分44.2 vs 42.3）。"
- "任何答案过滤策略均未超过不过滤的基线，例如数学领域不滤波平均分为41.9，优于GPT验证的38.0。"
---

# OpenThoughts: Data Recipes for Reasoning Models

> [!tip] 核心洞察
> 通过系统地探索SFT数据管道的各个步骤（问题收集、混合、过滤、去重、答案过滤、教师选择），可以以小成本构建出超越更大规模模型的开源推理模型。关键发现包括：从少数高质量来源选择问题比追求多样性更有效；使用更弱的教师模型（QwQ-32B）反而能训练出更强的学生模型；不使用答案过滤优于大多数过滤方法；以及采样多个答案（16×）能有效扩大数据规模并提升性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 开放思维：推理模型的数据配方 |
| 英文题名 | OpenThoughts: Data Recipes for Reasoning Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=7xjoTuaNmN) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | OpenThoughts3 Data Pipeline |
| Dataset | AIME 2025, LiveCodeBench 06/24-01/25, GPQA Diamond, 平均（12个任务） |

> [!tip] 效果简介
> - AIME 2025 上，准确率 为 53.3%，对比 34.5%，变化 +18.8pp。
> - LiveCodeBench 06/24-01/25 上，准确率 为 51.7%，对比 30.7%，变化 +21.0pp。
> - GPQA Diamond 上，准确率 为 53.7%，对比 33.2%，变化 +20.5pp。

## 概要

当前推理模型的训练严重依赖专有数据集，这一瓶颈阻碍了社区对推理模型的研究与复现。**OpenThoughts** 项目旨在构建完全开源的高质量推理数据集，通过系统性地探索 SFT 数据管道的每一步——问题收集、来源混合、问题过滤、去重与多答案采样、答案过滤以及教师模型选择——以可控成本训练出超越更大规模模型的开源推理模型。

该方法的核心洞察可概括为以下几点：

- **少即是多**：从少数（Top 1–2）高质量来源选择问题，比追求来源多样性（混合 8–16 个来源）带来更好的下游性能。
- **弱师强徒**：使用基准表现稍弱但教学效果更好的教师模型（如 QwQ-32B），其蒸馏效果显著优于基准更强的 DeepSeek-R1。
- **不滤胜于滤**：任何答案过滤策略（GPT 验证、多数共识等）均未超过完全不过滤的基线。
- **多采样扩展规模**：每个问题采样 16 个答案并进行精确去重，可在不降低性能的前提下有效扩大数据规模。

基于上述发现构建的 **OpenThinker3-7B** 在 AIME 2025、LiveCodeBench 和 GPQA Diamond 上分别达到 53.3%、51.7% 和 53.7%，相较 DeepSeek-R1-Distill-Qwen-7B 分别提升约 18.8、21.0 和 20.5 个百分点（Table 1），在 12 个任务的综合平均上领先 12.4 个百分点，成为当前同规模开源推理模型中的最优方案。

大规模推理模型（如 OpenAI o1、DeepSeek-R1）在数学、编程和科学等复杂推理任务上展现出显著能力，但其训练通常依赖专有数据集和闭源配方。这种封闭性使社区难以复现、改进或理解这些模型的行为，形成了一个核心瓶颈：**缺乏公开、可复现的SFT数据配方阻碍了推理模型的开放研究**。

已有若干开源努力试图填补这一空白。例如，**AM-1.4M** 和 **Nemotron Nano (NemoNano-1M)** 提供了大规模SFT推理数据集，而 **s1.1** 和 **LIMO** 则通过精心筛选的小规模数据集展示了数据质量的重要性。然而，这些工作仍存在明显缺口：它们要么未系统揭示数据管道各环节对下游性能的因果影响，要么在数据规模与质量的权衡上缺乏可控实验支撑。

本文的动机在于：通过系统性地解剖SFT数据管道的每一步——问题收集、来源混合、问题过滤、去重、多答案采样、答案过滤和教师模型选择——以超过1000次受控实验量化每个决策的影响，从而构建一个完全开源、可复现且性能领先的推理模型数据配方。核心假设是：**通过精细的数据工程，可以在远小于闭源方案的计算成本下，训练出超越更大规模蒸馏模型的推理模型**。

## 核心方法与创新机理

OpenThoughts3 的核心贡献在于通过 **1000+ 次受控消融实验**，系统性地解构并优化了推理模型 SFT 数据管道的每一个环节，揭示了一系列反直觉的数据配方选择。这些发现共同构成了一套低成本、高性能的开源推理数据构建方案。

### 关键创新点

**1. 问题来源：少即是多**
传统做法倾向于混合尽可能多的数据源以追求多样性。本研究的关键发现是：**仅选择每个领域排名前 1-2 的最高质量来源，反而显著优于混合 16 个来源**。以代码领域为例，仅使用 Top 2 来源相比 Top 16 来源在所有基准上平均准确率提升约 5%（Table 3, Section 3.3）。这一发现颠覆了“数据多样性优先”的常规认知，表明在推理任务中，来源质量远比数量重要。

**2. 教师模型：弱师出高徒**
直觉上，基准表现更强的模型应作为更好的教师。然而实验表明，**QwQ-32B 作为教师模型在所有领域均显著优于 DeepSeek-R1**（例如代码领域平均分 44.2 vs 38.0，Table 7, Section 3.7），尽管 QwQ-32B 在目标推理基准上的得分更低。这一反直觉结果暗示，教师模型的“教学适配性”（如推理轨迹的清晰度、步骤的可模仿性）可能比其自身的解题能力更为关键。

**3. 答案过滤：无为而治**
在 SFT 数据构建中，通常会对生成的答案进行质量过滤（如 GPT 验证、多数共识）。本研究发现：**任何答案过滤策略均未能超越不过滤的基线**。在数学领域，不过滤策略平均得分 41.9，优于 GPT 验证的 38.0（Table 6, Section 3.6）。这表明，教师模型生成的“次优”答案中可能包含有益的学习信号（如错误探索路径），过滤反而损失了这些信息。

**4. 多答案采样：以量换质**
为扩大数据规模，每个问题采样 16 个答案并进行精确去重（或不去重），可在不降低性能的前提下有效扩展数据集。科学领域精确去重 16× 采样平均分 36.2，接近单次采样 35.5（Table 5, Section 3.5）。这提供了一种低成本的规模化路径：通过重复采样而非寻找更多问题来增加训练数据。

**5. 问题过滤：LLM 优于经典方法**
使用 GPT-4.1-mini 进行响应长度过滤（数学、科学）或难度过滤（代码），显著优于 fastText 等经典方法。数学领域响应长度过滤平均得分 41.9，优于随机过滤基线 39.4（Table 4, Section 3.4）。LLM 对问题质量的语义理解能力是性能提升的关键。

### 方法谱系与知识库定位

与现有工作相比，OpenThoughts3 的差异化定位体现在：

| 维度 | 现有方法 | OpenThoughts3 |
|------|----------|---------------|
| 数据来源策略 | 广泛混合多源（如 AM-1.4M） | 精选 Top 1-2 高质量源 |
| 教师选择 | 基准最强模型（如 DeepSeek-R1） | 教学效果更优的 QwQ-32B |
| 答案处理 | GPT 验证/多数共识过滤 | 完全跳过答案过滤 |
| 数据增强 | 单次采样 + 模糊去重 | 16× 采样 + 精确/不去重 |
| 问题过滤 | fastText/嵌入距离 | LLM 难度/响应长度过滤 |

最终，基于这些创新选择构建的 **OpenThinker3-7B** 在 AIME 2025、LiveCodeBench 和 GPQA Diamond 上分别达到 53.3%、51.7% 和 53.7%，比 **DeepSeek-R1-Distill-Qwen-7B**（Guo et al., 2025）提升约 18.8、21.0 和 20.5 个百分点（Table 1），且优于所有同规模开源推理模型。

> **注意**：上述结论均在 **Qwen-2.5-7B-Instruct**（Yang et al., 2024b）基础模型上验证，迁移到其他基础模型或更大规模（如 32B）时结论可能不同（例如验证策略在 7B 有害而在 32B 有益）。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/011_Figure_3.jpg]]
*Figure 3: The OpenThoughts3-1.2M Full Data Pipeline*

OpenThoughts3 的数据配方探索围绕一个六阶段实验管道展开，旨在以可控成本系统性地识别影响推理模型性能的关键数据决策。图 2 给出了管道的完整概览，其核心设计原则是**逐阶段隔离消融**：在每一阶段固定其他步骤不变，仅改变当前步骤的策略，从而独立测量该步骤的因果效应。

### 管道模块与数据流

整个管道按以下顺序执行，每个模块的输出作为下一模块的输入：

1. **问题收集（Question Sourcing）**：从代码、数学、科学三个领域的现有数据集和 LLM 生成的新数据集中获取原始问题。对于需要 LLM 生成的来源，统一使用 GPT-4o-mini 进行问题生成。每个来源独立产出 31,600 个问题（不足时重复采样补齐）。

2. **问题混合（Question Mixing）**：从各领域排名前 N 的来源中各随机采样 31,600/N 个问题，拼接形成固定规模的数据集。实验发现，**仅混合前 1–2 个最佳来源**的效果显著优于追求多样性而混合更多来源（例如代码领域 Top 2 来源相比 Top 16 平均准确率提升约 5%）。

3. **问题过滤（Question Filtering）**：使用基于 LLM 的方法筛选高质量问题。代码领域采用 GPT-4o-mini 的难度评估过滤，保留最难的问题；数学和科学领域采用 GPT-4.1-mini 的响应长度过滤，选择 LLM 直接回答时生成最长响应的问题。这些 LLM 方法在所有领域均优于 fastText 和嵌入距离等经典过滤方法。

4. **问题去重与多答案采样（Deduplication & Multi-Answer Sampling）**：对问题进行去重后，为每个问题从教师模型采样多个答案以扩大数据规模。最终管道对所有领域采用 16× 答案采样，数学和科学使用精确去重，代码不进行去重。实验表明，每个问题采样 16 个答案并进行精确去重，可在不降低性能的前提下有效扩展数据量。

5. **答案过滤（Answer Filtering）**：尝试使用 LLM 验证、多数共识、响应长度选择等方法过滤低质量答案。但消融实验揭示了一个反直觉的结论：**所有答案过滤策略均未超过不过滤的基线**。因此最终管道完全跳过此步骤，直接使用所有生成的答案。

6. **教师模型选择（Teacher Model Selection）**：选择用于生成推理轨迹的教师模型。实验发现 **QwQ-32B 在所有领域均显著优于 DeepSeek-R1**，尽管 QwQ-32B 在基准测试上的表现更弱。这一发现表明教师模型的“教学效果”与其自身基准性能并非正相关。

### 实验控制与公平性

所有消融实验均在 Qwen-2.5-7B-Instruct 上进行微调，每次实验严格控制数据集大小为 31,600 个样本，确保不同策略之间的可比性。评估使用统一的 Evalchemy 工具，并对训练数据进行去污染处理（去污算法真阴性率 99.6%），以防止数据泄露对结论的干扰。

### 最终管道的缩放行为

将各阶段的最优策略依次叠加后，数据集的缩放曲线持续上移（图 5）。最大增益来自问题来源选择和问题过滤阶段，而答案过滤的省略和教师模型的切换进一步巩固了性能优势。最终形成的 OpenThoughts3-1.2M 管道（图 3）以约 22,000 H100 GPU 小时的标注成本，产出了在 7B 规模上超越所有开源同量级推理模型的 SFT 数据集。

**证据强度**：管道各阶段的消融结论均来自 1,000+ 次受控实验，核心发现（如 Top 2 混合优于 Top 16、不过滤答案优于过滤、QwQ-32B 优于 DeepSeek-R1）在 Table 3–Table 7 中有直接数据支撑，置信度普遍在 0.9–0.95。需注意的是，所有结论均基于 Qwen-2.5-7B-Instruct 这一特定基础模型，迁移到其他基础模型或更大规模（如 32B）时，部分结论可能不成立（例如验证策略在 7B 有害而在 32B 有益）。

### 数据管道关键模块

OpenThoughts3 的数据管道由六个顺序模块构成（Figure 2），每个模块均通过严格的控制变量消融实验进行优化：

1. **问题收集（Question Sourcing）**：从代码、数学、科学三个领域的现有数据集和 LLM 生成的数据集中获取问题。对于 LLM 生成的来源，统一使用 GPT-4o-mini 作为生成器。每个来源独立生成 31,600 个问题，不足时重复采样补足。

2. **问题混合（Question Mixing）**：将每个领域排名前 1 或 2 的高质量来源的问题进行混合。混合策略为：选取排名前 N 的数据集，从每个来源随机采样 31,600/N 个问题后拼接。关键发现是选择极少数高质量来源优于追求多样性——代码领域仅使用前 2 个来源相比混合 16 个来源在所有基准上平均准确率提升约 5%（Table 3）。

3. **问题过滤（Question Filtering）**：使用 LLM 进行基于难度或响应长度的过滤。代码问题采用 GPT-4o-mini 评估难度后保留最困难的问题；数学和科学问题则让 LLM 直接回答后选择产生最长响应的题目。LLM 方法显著优于 fastText 和嵌入距离等经典方法（Table 4）。

4. **问题去重与多答案采样（Deduplication & Multi-Answer Sampling）**：对问题进行去重后，每个问题重复采样多个答案以扩展数据规模。最终管道对所有领域采用 16× 采样，数学和科学使用精确去重，代码不进行去重。实验表明，使用更少问题但多次标注的策略与标注更多问题但次数更少的策略性能相当甚至更优（Table 5）。

5. **答案过滤（Answer Filtering，最终未采用）**：尝试了 LLM 验证（GPT 验证）、多数共识、响应长度选择等多种过滤策略，但所有过滤方法均未超过不过滤的基线（Table 6）。因此最终管道跳过此模块，直接使用所有生成的答案。

6. **教师模型选择（Teacher Model Selection）**：在多个候选教师模型中，QwQ-32B 在所有领域均显著优于基准表现更强的 DeepSeek-R1（例如代码领域平均分 44.2 vs 38.0，Table 7），被选为最终教师模型。

### 关键公式

#### 归一化插入-删除相似度

用于问题去重和训练数据去污染的核心相似度度量：

$$\mathrm{indel}_{\mathrm{sim}} = 100 \times \frac{\mathrm{LCS}_{\mathrm{length}}(s_1, s_2)}{\max(|s_1|, |s_2|)}$$

其中：
- $\mathrm{LCS}_{\mathrm{length}}(s_1, s_2)$ 表示字符串 $s_1$ 和 $s_2$ 的最长公共子序列长度；
- $|s_1|$ 和 $|s_2|$ 分别为两个字符串的字符长度；
- 结果归一化到 0–100 区间，用于衡量两个文本的插入-删除相似度。

该公式在去污染流程（附录 C）中用于检测训练集与评估集之间的重叠，算法真阴性率达 99.6%，有效防止数据泄露。

## 实验与关键发现

### 主实验结果

OpenThinker3-7B 在数学、代码和科学三个领域的 12 个基准上全面超越了所有同参数规模的开源推理模型（Table 1）。在 AIME 2025 上达到 53.3%，LiveCodeBench 06/24-01/25 上达到 51.7%，GPQA Diamond 上达到 53.7%，相比 DeepSeek-R1-Distill-Qwen-7B 分别提升了约 18.8、21.0 和 20.5 个百分点。在 12 个任务的平均准确率上，OpenThinker3-7B 达到 55.3%，比 DeepSeek-R1-Distill-Qwen-7B（42.9%）高出 12.4 个百分点，比次优的开源数据模型 Nemotron-Nano-8B 高出 2.1 个百分点。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/003_Table_1.jpg]]
*Table 1: OpenThinker3-7B outperforms all open-data 7B and 8B reasoning models across domains. Our model also performs well on held out benchmarks which are not measured during our main experimentation, such as HMMT and AIME25. In our table, denotes a model trained from Qwen-2.5-7B-Instruct, M for Qwen-2.5-Math-Base, for Llama-3.1-8B-Instruct, and for DeepSeek-R1-Distill-Qwen-7B. “Base Model” denotes the starting checkpoint of the training strategy. “Method” denotes the model’s optimization algorithm. In each row, we bold values within two standard errors of the highest-scoring model*

缩放曲线（Figure 1）表明，OpenThoughts3 在不同数据规模下均优于现有的 SFT 推理数据集（AM-1.4M、Nemotron Nano），且性能随数据量增加持续提升。这一趋势在数学（AIME 2025）、代码（LiveCodeBench）和科学（GPQA Diamond）三个领域均成立。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/002_Figure_1.jpg]]
*Figure 1: OpenThoughts3 outperforms existing SFT reasoning datasets across data scales. All models are finetuned from Qwen-2.5-7B-Instruct. We compare to large SFT datasets (AM, Nemotron Nano) and small curated datasets (s1.1, LIMO) on AIME 2025 (left), LiveCodeBench 06/24-01/25 (middle), and GPQA Diamond (right). Scaling curves for all evaluation benchmarks are in Figure 6*

### 管道消融实验

所有消融实验均在 Qwen-2.5-7B-Instruct 上微调，每次控制数据集大小为 31,600 个样本，确保比较的公平性。评估使用统一的 Evalchemy 工具，并对训练数据进行去污染处理（去污算法真阴性率 99.6%）。

#### 问题来源选择

Table 2 展示了各领域排名前三的问题来源。代码领域，OpenCodeReasoning 平均得分 27.5，CodeGolf（StackExchange）得分 25.3；数学领域，OpenMath-2-Math 达到 58.8。关键发现是：选择仅两个最佳代码问题源相比混合 16 个源，在所有基准上平均准确率提升约 5%（Table 3）。这一“少即是多”的现象在数学和科学领域同样成立——混合至多两个来源优于追求多样性。

#### 问题过滤

Table 4 比较了不同过滤策略。LLM 基方法显著优于经典方法：在数学领域，GPT-4.1-mini 的响应长度过滤平均得分 41.9，优于随机过滤基线 39.4，且明显优于 fastText；代码领域，GPT-4o-mini 的难度过滤平均得分 43.0。最终管道采用：代码使用难度过滤，数学和科学使用响应长度过滤。

#### 去重与多答案采样

Table 5 表明，每个问题采样 16 个答案并进行精确去重（或不去重）可在不降低性能的前提下有效扩大数据规模。例如科学领域精确去重 16× 采样平均分 36.2，接近单次采样 35.5。数学领域精确去重配合 4× 采样表现最佳，但 16× 采样作为次优方案被选用以兼顾可扩展性。最终管道对所有领域采用 16× 答案采样，数学和科学使用精确去重，代码不进行去重。

#### 答案过滤

Table 6 的结果出人意料：任何答案过滤策略均未超过不过滤的基线。在数学领域，不过滤策略平均得分 41.9，与随机过滤 41.6 相当，优于 GPT 验证的 40.0 和多数共识的 38.0。因此最终管道完全跳过答案过滤步骤。

#### 教师模型选择

Table 7 揭示了反直觉的发现：基准表现更弱的 QwQ-32B 作为教师模型在所有领域均显著优于更强的 DeepSeek-R1。代码领域 QwQ-32B 平均分 44.2 vs DeepSeek-R1 的 38.0（提升 1.9 个百分点），数学领域提升 2.6 个百分点，科学领域同样领先。Phi-4-reasoning-plus 表现最差（29.0）。这表明教师模型的“教学适配性”比其自身的基准性能更重要。

### 失败模式与局限

**答案过滤的失效**：所有验证策略（GPT 验证、多数共识、响应长度过滤）在 7B 模型上均未带来增益，甚至有害。论文推测这可能与 7B 模型的容量限制有关——验证策略可能在 32B 模型上有益，但在 7B 上会丢弃有用的训练信号。

**自反思组件的关键性**：移除自反思（self-reflection）组件导致推理轨迹平均长度降至 328 tokens，平均性能相对下降 49.1%（Table 21，Appendix E.3），说明长链推理中的自我修正机制对性能至关重要。

**泛化不稳定性**：蒸馏推理模型在简单问题上的表现存在强烈波动，缺乏封闭模型那样的稳定性。论文明确指出模型安全性较差，推理数据集训练后有害性显著上升，需要额外的安全数据集微调。

**计算成本**：标注 1.2M 数据约需 22,000 H100 GPU 小时，对部分研究者构成复现障碍。此外，所有管道设计选择均在 Qwen-2.5-7B-Instruct 上优化，迁移到其他基础模型的效果可能不一致。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/023_Table_15.jpg]]
*Table 15: Comparison of OpenThoughts with and without proof-based questions. Throwing out proof-based questions harms performance overall by 5.6 points on average*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/025_Figure_8.jpg]]
*Figure 8: Claude 3.7 accuracy improves consistently with larger thinking-token budgets across three benchmarks. Each panel plots mean accuracy (markers) and ±1 standard error (error bars) over multiple independent runs (5 for AIME 24, 3 for LCB and GPQA Diamond). The horizontal axes are logarithmic in the number of thinking tokens; the answer budget is 1 024 tokens for AIME 24 and 4 096 tokens for LCB and GPQA Diamond and is not counted in the thinking tokens budget. AIME 24: accuracy rises from a no-thinking baseline of 18.0% (red diamond) to 51.3% when the model is allowed 62 976 thinking tokens. LCB: performance climbs steadily from 60.5% to 70.4% at 28 672 thinking tokens. GPQA Diamond: accuracy...*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_7xjoTuaNmN/figures/052_Table_34.jpg]]
*Table 34: Full Ablation for Code Question Source Mixing*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

当前推理模型的训练严重依赖专有数据集，缺乏公开的监督微调（SFT）数据配方，这一瓶颈阻碍了社区对推理模型的研究和复现。OpenThoughts 项目通过系统性地探索 SFT 数据管道的各个步骤，以可控成本构建出超越更大规模模型的开源推理模型，填补了这一空白。

本工作的核心因果旋钮包括：问题来源的选择、数据过滤与去重策略、教师模型选择以及多答案采样比例。这些因素被证明是影响下游推理性能的关键可控变量。

### 2. 与现有工作的关系

#### 2.1 基线模型与数据集

本工作直接对标以下基线：

- **DeepSeek-R1-Distill-Qwen-7B**（Guo et al., 2025）：通过教师模型蒸馏得到的推理模型，是 OpenThinker3-7B 的主要性能对比对象。在 12 个任务的平均准确率上，OpenThinker3-7B 以 55.3% 对 42.9% 领先 12.4 个百分点（Table 1）。
- **Qwen-2.5-7B-Instruct**（Yang et al., 2024b）：所有消融实验统一使用的基础语言模型，确保了对比的公平性。
- **Nemotron Nano（NemoNano-1M）**：开源推理模型/数据集，用于数据规模的缩放对比（Figure 1）。
- **AM-1.4M**：大规模 SFT 推理数据集，同样用于缩放曲线对比。

#### 2.2 关键设计选择与背离

OpenThoughts3 数据管道在多个维度上背离了常规做法：

| 设计维度 | 常规做法 | OpenThoughts3 做法 | 证据锚点 | 置信度 |
|---------|---------|-------------------|---------|--------|
| 问题来源选择 | 广泛混合多个来源（如前16个） | 仅使用每个领域排名前1-2的最高质量来源 | Table 3, Section 3.3 | 0.95 |
| 问题过滤方法 | 使用 fastText 或嵌入距离等经典方法 | LLM 基于难度（代码）或响应长度（数学、科学）的高效过滤 | Table 4, Section 3.4 | 0.95 |
| 答案过滤策略 | 采用 GPT 验证、多数共识等后处理过滤 | **完全跳过答案过滤**，使用所有生成的答案 | Table 6, Section 3.6 | 0.95 |
| 教师模型选择 | 使用基准表现最强的模型（如 DeepSeek-R1） | 使用**教学效果更好但基准稍弱**的模型（QwQ-32B） | Table 7, Section 3.7 | 0.95 |
| 数据增强与去重 | 每个问题仅采样一次答案，采用模糊去重 | 每个问题重复采样 16 次答案，数学和科学采用精确去重，代码不进行去重 | Table 5, Section 3.5 | 0.95 |

#### 2.3 管道模块与功能定位

OpenThoughts3 的完整数据管道（Figure 2, Figure 3）包含以下模块：

1. **问题收集**：从代码、数学、科学领域的现有和新生成的数据集中获取问题（Section 3.2）。
2. **问题混合**：将每个领域顶尖来源的问题进行混合（Section 3.3）。
3. **问题过滤**：使用 LLM 或快速文本分类器过滤高质量问题（Section 3.4）。
4. **问题去重与多答案采样**：对问题进行去重，并为每个问题生成多个答案（Section 3.5）。
5. **答案过滤（最终未采用）**：使用 LLM 验证或多数共识过滤低质量答案，但实验表明不进行过滤更好（Section 3.6）。
6. **教师模型选择**：选择最佳的教师模型来生成推理轨迹（Section 3.7）。

### 3. 适用边界与局限

#### 3.1 已验证的适用条件

- **模型规模**：完整的管道实验仅在 7B 参数规模的模型上进行（Qwen-2.5-7B-Instruct）。更大模型（如 32B）的结论可能不同——例如，验证策略在 7B 模型上有害，但在 32B 模型上可能有益。
- **领域范围**：研究限于数学、代码和科学三个领域。其他领域（如法律、医学）的适用性未经验证。
- **基础模型依赖**：数据配方的设计选择是在特定基础模型（Qwen-2.5-7B-Instruct）上优化的，迁移到其他基础模型的效果可能不一致。

#### 3.2 已知局限

1. **计算成本**：SFT 推理数据管道的计算成本依然可观。标注 1.2M 数据约需 22,000 H100 GPU 小时，限制了一些研究者的复现能力。
2. **安全性问题**：模型的安全性较差，推理数据集训练后有害性显著上升，需要额外的安全数据集微调来缓解。
3. **泛化稳定性**：蒸馏推理模型在简单问题的泛化上仍存在强烈的性能波动，缺乏封闭模型那样的稳定性。
4. **验证策略的规模敏感性**：答案验证策略对 7B 模型有害但对 32B 模型有益的根本原因尚不明确，这限制了该方法在不同规模模型上的统一应用。

### 4. 开放问题

1. **数据源选择机制**：为什么选择数量极少（Top 1-2）的高质量数据源比混合更多来源效果更好？是否存在可理论化的选择准则？
2. **缩放上限**：进一步扩大数据规模（超过 1.2M 样本）是否会持续带来性能提升？缩放曲线是否会出现饱和？
3. **响应长度偏好**：为什么最短响应策略在推理任务中往往优于最长响应策略？这与推理链质量和简洁性之间的关系是什么？
4. **验证策略的规模效应**：验证策略对 7B 模型有害但对 32B 模型有益的根本原因是什么？是否与模型容量和自纠错能力有关？
5. **安全性与推理能力的权衡**：如何在不损害推理能力的前提下融入安全性数据集以降低有害性？
6. **泛化机理**：蒸馏推理模型泛化能力欠缺的深层机理是什么？是否需要更接近 RL 阶段的训练方法来弥补？
7. **证明类问题的验证**：是否可以设计更有效的验证方法来处理证明类问题（当前验证方法对此类问题效果较差）？
8. **训练范式的迁移性**：推理数据配方的结论在连续预训练或强化学习设置下是否仍然成立？

## 原文 PDF

![[paperPDFs/ICLR_2026/OpenThoughts_Data_Recipes_for_Reasoning_Models.pdf]]
