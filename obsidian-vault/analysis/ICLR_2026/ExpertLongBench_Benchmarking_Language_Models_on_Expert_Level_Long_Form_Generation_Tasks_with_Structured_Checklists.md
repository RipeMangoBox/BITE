---
title: "ExpertLongBench: Benchmarking Language Models on Expert-Level Long-Form Generation Tasks with Structured Checklists"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ExpertLongBench_Benchmarking_Language_Models_on_Expert_Level_Long_Form_Generation_Tasks_with_Structured_Checklists.pdf
openreview_forum_id: nJvgBolRcR
aliases:
- ExpertLongBench
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "向模型提供详细的领域特定评估细则（rubric）作为提示，可显著提升其在专家任务上的表现（如T2LegalSFG上F1从6.2提升至32.5），但仅凭此仍远未达到可接受水平，任务本身对专业知识的要求是核心挑战。"
primary_logic: "将专家设计的领域特定细则转化为结构化检查清单，并基于清单进行逐项参考对比评价，能够实现细粒度、更贴近专家标准的评估，为领域内强任务提供可靠基准。"
claims:
- "最佳模型Gemini-2.5-Pro在ExpertLongBench上仅获得33.4的平均F1，表明现有LLM在专家级任务上仍有巨大的改进空间。"
- "模型虽然能生成覆盖超过67%所需检查项的内容，但实际信息正确性极低，易产生误导。"
- "基于Qwen2.5-72B的清单评分与GPT-4o的评分之间皮尔逊相关系数达0.88，验证了开源模型可用于低成本、可复现的评估。"
- "在T2LegalSFG任务上，将ground-truth评估细则直接嵌入提示后，GPT-4o的F1从6.2跃升至32.5，说明细致引导对模型表现有显著影响。"
---

# ExpertLongBench: Benchmarking Language Models on Expert-Level Long-Form Generation Tasks with Structured Checklists

> [!tip] 核心洞察
> 将专家设计的领域特定细则转化为结构化检查清单，并基于清单进行逐项参考对比评价，能够实现细粒度、更贴近专家标准的评估，为领域内强任务提供可靠基准。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ExpertLongBench：以结构化清单基准评测专家级长篇生成任务的语言模型 |
| 英文题名 | ExpertLongBench: Benchmarking Language Models on Expert-Level Long-Form Generation Tasks with Structured Checklists |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nJvgBolRcR); [Project](https://huggingface.co/spaces/launch/ExpertLongBench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | CLEAR |
| Dataset | ExpertLongBench (average over 11 tasks), Expert-level human agreement (T7, T8), Checklist evaluation alternative (all tasks), T2LegalSFG with detailed rubric prompt |

> [!tip] 效果简介
> - ExpertLongBench (average over 11 tasks) 上，F1 score 为 Gemini-2.5-Pro : 33.4，对比 GPT-5 : 31.0 (second best)，变化 +2.4。
> - Expert-level human agreement (T7, T8) 上，Accuracy 为 GPT-4o judge: 91.3% (T8) / 92% (T7)，对比 Domain expert ratings，变化 High agreement。
> - Checklist evaluation alternative (all tasks) 上，Pearson correlation with GPT-4o 为 Qwen2.5-72B judge: 0.88，对比 GPT-4o as reference judge，变化 -。

## 概述

大语言模型（LLM）在通用长文本生成上已展现出显著能力，但在法律、医学、化学等需要严格专业知识的专家级任务中，其表现远未达到可靠水平。**ExpertLongBench** 基准的构建与评估揭示了一个关键瓶颈：模型并非无法触及任务所需的信息维度，而是生成的表面覆盖了检查项，但实际信息准确性极低，存在严重的误导风险。最佳模型 Gemini-2.5-Pro 在全部 11 个任务上的平均 F1 仅为 33.4（Table 2），而模型虽能覆盖超过 67% 的所需检查项，正确性却极差（Figure 2），说明“沾边但不准确”是当前专家级长文生成的核心失效模式。

针对这一瓶颈，本文提出 **CLEAR**（Checklist-based Evaluation with Expert-Designed Rubrics）评估框架。其核心思路是将领域专家设计的细粒度评估细则（rubric）转化为结构化检查清单，从模型输出与人工参考中分别提取对应检查项信息，再通过逐项语义包含比较进行项目级评判。这一方法将评估从模糊的整体印象转变为有据可依的精确对照，使评估粒度从概要级别提升至可检查的原子项级别。框架还采用开源模型 Qwen2.5-72B 作为清单映射器，以降低评估成本并保证可复现性。

主要实验结果如下：
- **整体表现**：15 个被评模型在 ExpertLongBench 上的平均 F1 最高仅 33.4（Gemini-2.5-Pro），GPT-5 以 31.0 位居第二，表明现有 LLM 距专家级可用水平仍有巨大差距（Table 2）。
- **评估可靠性**：GPT-4o 作为评判器与领域专家在 T7、T8 任务上的一致性分别达 92% 和 91.3%，验证了 CLEAR 框架的评估有效性（§4.2）。同时，Qwen2.5-72B 的评分与 GPT-4o 之间的皮尔逊相关系数达 0.88，证明开源模型可作为低成本、高可复现的替代评估方案（Figure 3）。
- **引导效应**：在 T2LegalSFG 任务上，将 ground-truth 评估细则直接嵌入提示后，GPT-4o 的 F1 从 6.2 跃升至 32.5（Table 65），说明细致引导能显著提升模型输出质量，但即便提升后仍远未达到可接受水平，任务本身对专业知识的要求是核心挑战。

## 背景与动机

专家级长篇生成是当前大语言模型（LLM）能力边界中最具挑战性的前沿之一。从法律案件摘要、教育反馈撰写，到化学分子描述、网络安全风险分析，这些任务不仅要求模型产出连贯的长文本，更要求其内容在领域知识的精确性、完整性和可靠性上达到专家水准。然而，现有评测体系在这一方向上存在显著缺口。

通用评测标准（如连贯性、相关性、整体质量）虽然易于使用，但无法捕捉专家任务中细粒度的正确性要求。基于事实分解的评测方法通过将输出拆解为原子事实并进行逐条验证，提升了评测的客观性，但缺乏任务特定的结构化参照，难以区分“表面沾边”与“实质正确”。更关键的是，当前 LLM 在专家级任务中暴露出的核心瓶颈并非无法触及任务所要求的方面——事实上，模型生成的内容能够覆盖超过 67% 的所需检查项——而是这些覆盖的内容信息准确性极低，存在严重的误导风险（见 Figure 2）。这种“高覆盖、低质量”的负相关现象，揭示了一个深层问题：模型学会了生成看似相关但实质上不正确的“幻觉式沾边”内容，而现有评测范式难以有效甄别这一问题。

ExpertLongBench 正是在这一背景下提出。其动机在于构建一个以专家设计的领域特定评估细则（rubric）为锚点的基准，将评测从模糊的整体印象推进到可逐项核验的结构化检查清单（checklist）层面。通过将人工编写的参考输出映射为检查清单，并与模型输出进行逐项双向语义包含比较，CLEAR 框架实现了有据可依、细粒度且贴近专家标准的评估。这一设计不仅为当前 LLM 的专家能力提供了更诚实的衡量，也为未来模型改进指明了方向：仅靠更强的通用生成能力远远不够，专业知识的内化与精确表达才是突破瓶颈的关键。

## 核心创新

CLEAR 框架的核心创新在于将评估标准从通用、主观的整体判断，转向由领域专家设计的任务特定细粒度细则（rubric）驱动的结构化检查清单评估。这一转变体现在四个关键维度上（见 Table 1 的基准统计与 Figure 1 的流程示意）。

**评估标准：从通用准则到专家细则。** 传统 LLM-as-a-judge 方法依赖连贯性、相关性等通用标准进行整体评分，而事实分解类方法虽能进行原子比较，却缺乏任务特定性。CLEAR 直接引入领域专家为每个任务定义的细粒度检查项集合 $\{c_i\}_{i=1}^{n}$，将评估扎根于任务本身的知识要求。这一设计使得评估信号从“模型输出看起来是否合理”转变为“模型输出是否准确覆盖了该领域专家认为必须包含的具体信息点”。

**评估粒度：从整体分数到逐项清单比较。** CLEAR 不输出单一分数，而是通过 Checklist Mapper 从模型输出和人工参考中分别抽取与检查项对应的信息，再由 Checklist Judge 进行双向语义包含比较，判定每个检查项的正确性。这种项目级精确评估使得指标（准确率、精确率、召回率、F1）具有明确的诊断意义——例如，高覆盖率但低 F1 的现象直接揭示了模型“表面沾边但信息不准确”的核心瓶颈（Figure 2）。

**参照依据：从无参照或原文参照到清单映射参考。** CLEAR 为每个样本构建了 checklist-mapped reference——即由 GPT-4o 从人工编写的参考输出中提取与检查项对应的内容。这确保了评估始终有据可依，而非依赖评估模型对“理想答案”的主观想象。在 T7 和 T8 任务上，基于该参照的 GPT-4o 判断与领域专家评估的一致性分别达到 92% 和 91.3%，验证了这一参照机制的有效性。

**清单提取模型：从高成本私有模型到开源可复现方案。** 为降低评估成本并保证可复现性，CLEAR 选用开源模型 Qwen2.5-72B 作为 Checklist Mapper（其在映射任务上 F1 达 90.1，显著优于其他开源模型，见 Table 53），其评分与 GPT-4o 的皮尔逊相关系数达 0.88（Figure 3），为大规模基准评估提供了可行的低成本替代方案。

这些创新共同构成了一个闭环：专家细则定义“应该检查什么”，清单映射从生成内容中“提取出什么”，逐项比较判定“是否正确”，最终聚合为可诊断的细粒度指标。需要指出的是，尽管详细细则提示能显著提升模型表现（如 T2LegalSFG 上 F1 从 6.2 跃升至 32.5，见 Table 65），但最佳模型平均 F1 仅 33.4（Table 2），表明评估框架本身并非解决任务难题的银弹，而是精准暴露了当前 LLM 在专家级长文生成上的真实能力边界。

## 整体框架

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/001_Figure_1.jpg]]
*Figure 1: Pipeline of CLEAR. The example shown is from task T1: multi-document legal case summarization. The checklist mapper takes as input the model output (or human-written reference) and extracts checklist items according to the rubric. Checklists of the model output and the reference are compared at the item level, and the results are subsequently aggregated into the final scores*

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/002_Table_1.jpg]]
*Table 1: Benchmark statistics. ∗: rubric is developed by experts; otherwise, it is created by refining and expanding upon established evaluation protocols; †: task data is held privately. For each task, we report whether the task data is newly created ( $\checkmark$ ) or adapted from previous work; the average number of checklist items in each sample (#Rubric); and the average length of the input (#Input) and human reference (#Reference). Several of these tasks feature significantly longer inputs and references compared to existing domain-specific datasets (see Appendix H)*

ExpertLongBench 的核心贡献是 **CLEAR**（Checklist-based Evaluation for Expert-level Long-form Tasks）框架，其设计目标是将专家级长篇生成任务的评估从主观整体评分转变为可操作的、基于结构化检查清单的细粒度对比。框架的运作逻辑围绕一个关键瓶颈展开：现有模型在专家任务上并非无法触及所需方面（覆盖率超过 67%），而是生成内容的信息正确性极低，表面“沾边”但实质错误，具有高度误导性。

### 管道总览

CLEAR 的评估管道由四个顺序模块构成，形成“细则定义 → 清单提取 → 逐项判定 → 分数聚合”的闭环：

1.  **Expert-Designed Rubric**：由领域专家为每个任务预先定义一组细粒度、可独立检查的评估项目，记为 $`\{c_i\}_{i=1}^{n}`$，其中 $`n`$ 为检查项数量。这些细则直接编码了任务的专业标准，是后续所有评估步骤的唯一依据。
2.  **Checklist Mapper**：分别以模型输出和人工编写的参考输出为输入，根据细则逐项提取对应的信息片段，生成结构化的“检查清单”。这一映射过程将自由文本转化为可比较的原子单元。
3.  **Checklist Judge**：将模型输出的检查清单与参考输出的检查清单进行逐项双向语义包含比较——既检查模型输出是否被参考包含（精确率），也检查参考是否被模型输出包含（召回率），从而判定每个检查项的正确性。
4.  **Metrics Aggregator**：汇总所有检查项的判定结果，计算准确率、精确率、召回率及 F1 分数，最终聚合为任务级性能指标。

Figure 1 以任务 T1（多文档法律案例摘要）为例展示了这一管道的具体运作：检查清单映射器接收模型输出（或人工参考），依据细则提取检查项，随后在项目级别进行比较，结果被聚合为最终评分。

### 关键设计选择与证据

框架中有两个设计选择直接决定了评估的可靠性和可复现性：

**评估标准从通用到领域特定的转变。** 传统 LLM-as-a-judge 方法使用连贯性、相关性等通用标准进行整体评分，无法捕捉专家任务中细微但对错分明的信息点。CLEAR 将评估标准替换为领域专家设计的任务特定细则，使判断依据从主观印象变为可验证的事实检查。这一转变的有效性在 T2LegalSFG 任务上得到直接验证：当将 ground-truth 评估细则嵌入提示后，GPT-4o 的 F1 从 6.2 跃升至 32.5（Table 65），增幅达 26.3 个百分点，说明细致引导对模型表现有显著影响，但同时也表明任务本身的专业难度仍是核心挑战。

**清单提取模型从私有到开源的转变。** 为降低评估成本并确保可复现性，CLEAR 采用开源模型 Qwen2.5-72B 作为检查清单映射器，替代了 GPT-4o 等高成本私有方案。消融实验（Table 53）表明，Qwen2.5-72B 在检查清单映射任务上取得了 90.1 的 F1，与 GPT-4o 性能相当，且显著优于其他开源大模型。更关键的是，Qwen2.5-72B 作为 judge 的评分与 GPT-4o 评分之间的皮尔逊相关系数达 0.88（Figure 3），验证了开源模型可用于低成本、可复现的评估。此外，GPT-4o 基于细则的判断与领域专家评估在 T7 和 T8 上的一致性分别达到 92% 和 91.3%，证实了该评估范式的有效性。

### 基准规模与独特性

ExpertLongBench 基准包含 11 个任务、1,050 个样本，覆盖法律、教育、医疗、化学、生物、金融、网络安全等 9 个专业领域。与现有基准的关键区别在于其超长上下文特性：最大输入长度约 200 万 token，最大输出长度约 15,801 token（Table 62），远超现有领域特定数据集（如最大输入仅 7,525 token 的现有基准），这使得 ExpertLongBench 成为衡量模型在真实专家工作场景下长篇生成能力的独特测试平台。

## 核心模块与公式推导

### 3.1 专家设计的评估细则

ExpertLongBench 为每个任务定义了由领域专家设计的细粒度评估细则，该细则是整个评估框架的基石。每个任务的细则被形式化为一组可检查的评估项目集合：

$$\{c_i\}_{i=1}^{n}$$

其中 $n$ 代表该任务中检查项的总数。这些检查项并非通用的连贯性或相关性标准，而是针对特定领域任务的知识点、逻辑步骤或信息要素。例如，在法律案例摘要任务中，检查项可能包括“是否包含案件编号”、“是否准确陈述判决依据”等具体可验证的条目。

### 3.2 检查清单映射器

检查清单映射器是 CLEAR 框架的第一个核心处理模块。该模块接收模型输出或人工编写的参考答案作为输入，依据任务特定的细则，从中抽取出与每个检查项 $c_i$ 对应的信息片段。映射过程遵循以下逻辑：

- **对于参考答案**：使用 GPT-4o 预先将参考答案中的内容与每个检查项对齐，构建“检查清单映射参考答案”，作为评估的黄金标准。
- **对于模型输出**：采用开源模型 Qwen2.5-72B 作为映射器，以降低评估成本并保证可复现性。该选择基于其在检查项映射任务上达到 90.1 的 F1 分数，显著优于其他开源模型。

### 3.3 检查清单评判器

评判器对映射后的模型输出清单与参考答案清单进行逐项双向语义包含比较，计算三个核心指标：

- **准确率**：模型输出与参考答案在检查项 $c_i$ 上相互语义包含的项数占比。
- **精确率**：模型输出被参考答案语义包含的检查项占比。
- **召回率**：参考答案被模型输出语义包含的检查项占比。

基于上述指标，计算每个样本的 F1 分数，再对所有样本取平均得到任务级性能。GPT-4o 作为评判器，其在任务 T7 和 T8 上与领域专家的人工判断一致性分别达到 92% 和 91.3%，验证了该评估方式的有效性。

### 3.4 指标聚合器

指标聚合器将逐项比较结果汇总为最终评分。具体而言，先计算每个样本的检查项级别准确率、精确率和召回率，再通过调和平均得到样本级 F1 分数，最后对所有样本取算术平均，获得任务级 F1 分数。所有分数均缩放至 0–100 区间以便比较。

## 实验与分析

### 主实验结果：专家级长篇生成仍是系统性瓶颈

我们在ExpertLongBench的11个任务上评估了15个主流大语言模型，以检查项F1分数作为核心指标（Table 2）。最佳模型Gemini-2.5-Pro的平均F1仅为33.4，第二名GPT-5为31.0，第三名o3为29.3。这一结果揭示了当前LLM在专家级长篇生成任务上的系统性瓶颈：即便最强模型，在需要准确、完整地覆盖领域专家所定义的细粒度检查项时，表现仍远未达到可用水平。

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/003_Table_2.jpg]]
*Table 2: Evaluating LLMs on EXPERTLONGBENCH (scaled to 0–100) using F1 scores. Models are sorted by average performance and the best performing model on each task is bolded. Model ranking is indicated by the color of the cell, with green (best) to white (worst)*

任务间难度差异显著。T2LegalSFG（法律结构化事实生成）是所有模型表现最差的任务，全部模型F1均低于11分，表明法律领域对精确事实提取与结构化表达的要求构成了极端挑战。相比之下，T5EduFG（教育领域反馈生成）和T6HealthR（健康推理）等任务上部分模型表现相对较好，但最高F1也仅在50-60区间。

值得注意的是，模型排名在不同指标下保持相对一致。以检查项准确率（Table 45）和精确率（Table 46）、召回率（Table 47）分别评估时，Gemini-2.5-Pro仍保持领先地位，但各指标的绝对数值均偏低，进一步印证了专家级任务对模型能力的全面考验。

### 覆盖率悖论：表面沾边不等于真正正确

Figure 2揭示了本基准发现的核心悖论：模型的检查项覆盖率（即生成内容所触及的检查项比例）与F1分数之间存在明显的负相关关系。多数模型能够覆盖超过67%的所需检查项，部分模型覆盖率甚至超过75%（Table 48），但实际正确性极低。这意味着模型倾向于生成“看起来相关”但信息严重不准确的内容——它们学会了触及话题的各个方面，却未能提供专家级别的精确信息。

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/004_Figure_2.jpg]]
*Figure 2: F1 score vs. coverage of checklist items (i.e., the percentage of checklist items that are covered in the generation regardless their correctness)*

这一发现对LLM-as-a-judge评估范式具有重要警示意义：仅凭整体印象或表面覆盖度进行评分将严重高估模型的实际能力。CLEAR框架通过逐项比较语义包含关系，有效区分了“提及某方面”与“正确表述某方面”，从而暴露了这一隐蔽但致命的失败模式。

### 评估框架的可靠性验证

为确保CLEAR评估结果的可信度，我们进行了多维度验证。在T7和T8两个任务上，我们将GPT-4o基于细则的判断与领域专家的人工评估进行对齐。结果显示，GPT-4o与专家判断的一致性准确率在T7上达到92%，在T8上达到91.3%（§4.2），证实了基于专家设计细则的LLM评估可以有效逼近领域专家的判断标准。

在跨模型一致性方面，我们进一步考察了不同LLM作为评判者时的一致性。GPT-4o与Gemini-2.0-Flash在T1、T6、T7、T8四个任务上的Cohen's Kappa分别为0.81、0.87、0.89和0.85（§4.2），表明不同强模型在使用相同细则框架时能够达成高度一致的判断。

### 开源模型替代方案：低成本可复现评估

为实现低成本且可复现的评估，我们系统考察了开源模型作为检查项映射器和评判者的可行性。在检查项映射任务上，Qwen2.5-72B取得了90.1的F1分数（Table 53），显著优于其他开源模型，达到与GPT-4o相当的水平。这验证了使用开源模型从模型输出中提取检查项对应信息的可靠性。

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/064_Table_53.jpg]]
*Table 53: The performance of different open-source models in checklist mapping scaled to 0-100. Given that Qwen2.5-72B achieves best performance, we also analyze smaller models from the same family*

在评判环节，我们将Qwen2.5-72B作为评判者与GPT-4o的评分进行相关性分析。在所有任务上，Qwen2.5-72B与GPT-4o评分的皮尔逊相关系数达到0.88（Figure 3, §6），表明开源模型组合可以作为GPT-4o的高质量替代方案，大幅降低大规模评估的成本门槛。

![[assets/figures/papers/iclr26_0009_nJvgBolRcR_ExpertLongBench_Benchmarking_Language_Models_on/figures/005_Figure_3.jpg]]
*Figure 3: Correlation of different model combinations with GPT-4o judgments averaged over all the tasks*

Figure 4的回归分析进一步显示，任务平均表现与各模型判断与GPT-4o对齐程度之间存在显著正相关。这意味着在模型表现较差（即任务更难）的任务上，不同评判者之间的分歧趋于增大，提示在极端困难的专家任务上，评估本身也需要更加审慎。

### 消融分析：提示策略与检索增强的效果

我们通过消融实验考察了两种可能提升模型表现的策略。

**详细细则提示的影响**：在T2LegalSFG任务上，我们将完整的ground-truth评估细则直接嵌入提示中，观察其对GPT-4o输出的影响。结果显示，GPT-4o的F1从通用提示下的6.2跃升至32.5（Table 65），提升幅度达26.3分。这一结果表明，向模型提供详细的领域特定评估标准可以显著改善其输出质量——模型在明确知道“什么是正确答案的构成要素”时，能够更好地组织其生成内容。然而，即便在提供完整细则的情况下，32.5的F1仍远未达到可接受水平，说明任务本身的专业知识要求仍是核心挑战，仅靠提示工程无法弥补根本性的能力缺口。

**RAG Agent的效果**：我们测试了检索增强生成（RAG）agent在超长上下文任务T1和T2上的表现。结果显示，RAG agent在两项任务上的F1均低于直接使用全上下文的设置（Table 49）。这一反直觉的发现表明，在需要全局信息整合的专家级任务中，分段检索反而可能破坏模型对上下文的整体理解，导致信息遗漏或错误拼接。

### 推理复杂度与知识深度的挑战

Figure 5展示了模型在不同推理复杂度水平上的性能变化趋势。随着推理复杂度的提升，所有模型的F1分数均呈现下降趋势，但下降幅度因模型而异。值得注意的是，专门针对推理优化的模型（如o3）并未在领域特定推理上展现出显著优势，提示当前的推理增强技术可能更适用于通用推理任务，而非需要深厚领域知识的专家级推理。

在知识深度维度上，模型在需要研究生级别知识的任务上表现明显下滑，进一步印证了专家级任务对深层领域理解的要求远超当前模型的知识边界。

## 方法谱系与知识库定位

### 与现有评估范式的继承与分化

CLEAR 框架立足于两条现有评估路线的交汇点上：**基于事实分解的评估**与**基于清单的评估**。论文明确指出其“在这些方向上扩展了事实分解和基于清单的评估”（§2 RELATED WORK），但关键的差异化改造在于评估标准的来源——CLEAR 的检查清单并非从通用维度推导而来，而是**从领域专家设计的任务特定细则（rubric）中派生**，从而将清单式方法适配到专家级任务场景。

与 LLM-as-a-judge 的通用标准范式（如连贯性、相关性等整体评分）相比，CLEAR 将评估粒度从概要级别下沉到**逐项清单提取与比较**的项目级精确评估。与纯粹的事实分解方法相比，CLEAR 不依赖通用 NLI 引擎进行原子事实比较，而是通过**双向语义包含判断**来判定每个检查项的正确性——检查项精确率定义为模型输出中被参考输出语义包含的项比例，召回率反之，准确率则为双向相互包含的项比例（§4.1）。

### 适用边界与已知约束

**语言与领域覆盖。** 当前基准仅支持英语任务，尚未扩展到多语言专家应用场景。尽管涵盖法律、教育、健康、化学、生物学、医学、金融、网络安全等 9 个领域的 11 个任务，论文坦承这“仅反映了现实世界中专家应用的一小部分”（limitations）。

**模型评估策略的局限。** 论文仅关注模型的**开箱即用性能**，未探索复杂提示策略、工具使用或代理工作流程。这意味着 CLEAR 测度的基准分数反映的是裸模型能力，而非经过精心编排的系统级表现。

**评估器本身的可靠性边界。** LLM 评估方法仍可能在复杂或模糊案例中产生错误或不一致的判断。尽管 GPT-4o 在 T7 和 T8 上与领域专家的一致性分别达 92% 和 91.3%（§4.2），且 Gemini-2.0-Flash 与 GPT-4o 的 Cohen's Kappa 在 T1、T6、T7、T8 上分别为 0.81、0.87、0.89、0.85，但这些数字也意味着在约 8-19% 的案例中仍存在分歧，尤其在更具挑战性的任务上评估可靠性可能进一步下降。

**未提供改进路径。** 论文虽提供了细粒度评估标准，但并未提出具体的模型改进策略——CLEAR 是一个诊断工具而非治疗方案。

### 关键开放问题

**推理模型为何失效？** 一个引人注目的反直觉发现是，测试时扩展（reasoning models）未能显著提升领域特定推理表现，特别是对于有明确专业标准的任务。这一现象的原因尚不明确，可能指向当前推理扩展策略与结构化专家知识之间的根本性张力。

**覆盖率与质量的负相关根源。** 模型能生成覆盖超过 67% 所需检查项的内容，但实际信息正确性极低（Figure 2 展示了 F1 分数与检查项覆盖率之间的总体负相关关系）。这种“表面沾边”式的幻觉生成机制亟待深入理解——模型似乎学会了“提及”正确方面而非“准确表达”它们，这可能是 RLHF 训练中对表面格式奖励的意外后果。

**评估可靠性的进一步提升。** 尽管 Qwen2.5-72B 与 GPT-4o 的评分相关性达 0.88，为低成本可复现评估提供了可行路径，但在复杂专家场景下如何使 LLM 评估与人类专家判断更加一致仍是开放挑战。Figure 4 的回归分析表明，任务越困难，模型判断与 GPT-4o 的对齐程度越低，暗示评估器本身的能力也受任务复杂度约束。

**Agentic 工作流的潜力未探。** RAG agent 在超长上下文任务 T1 和 T2 上表现不及直接全上下文设置（§5, Table 49），说明简单的检索集成反而可能损害任务表现。但更复杂的 agentic 编排或高级检索增强策略是否能大幅缩小差距，仍有待验证。

**从诊断到改进的桥梁。** 基于细粒度检查表评估揭示的模型弱点——特别是在需要精确专家知识的项目上的系统性失败——可以设计哪些针对性的训练或微调策略？这一问题将决定 CLEAR 作为基准的长期影响力：它能否从“揭示问题”走向“驱动进步”。

## 原文 PDF

![[paperPDFs/ICLR_2026/ExpertLongBench_Benchmarking_Language_Models_on_Expert_Level_Long_Form_Generation_Tasks_with_Structured_Checklists.pdf]]
