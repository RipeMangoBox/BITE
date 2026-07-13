---
title: "VideoRealBench: A Chain-of-Thought Realism Evaluation Benchmark for Generated Human-Centric Videos"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VideoRealBench_A_Chain_of_Thought_Realism_Evaluation_Benchmark_for_Generated_Human_Centric_Videos.pdf
project_link: null
code_link: "https://github.com/MCG-NJU/VideoRealBench"
aliases:
- VVV
- VideoRealBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入基于人类直观错误描述并严格依据错误空间占比与时间占比的五级客观评分标准，并强制评估器输出三步思维链（问题描述、标准遵循、答案），使评分过程透明且可验证。
primary_logic: 将人类直观的定性错误描述与严格定量的时空错误比例评分相结合，并训练MLLM执行多步CoT推理，是弥合机器评估与人类偏好差距、提升可解释性的关键。
claims:
- VideoRealEval在VideoRealDataset测试集上达到57.07% PLCC和56.78% SROCC，显著优于其他主流评估模型。
- 重新标注后的评分在偏好一致性比率（PCR）上达到0.925，远高于原始VideoPhy-2的0.754，证明新评分标准更贴合人类偏好。
- 消融实验证实CoT推理对评分对齐至关重要，使用完整CoT后PLCC从53.89%提升至57.07%。
- VideoRealDataset (测试集) 上 PLCC / SROCC = 57.07% / 56.78%
---

# VideoRealBench: A Chain-of-Thought Realism Evaluation Benchmark for Generated Human-Centric Videos

> [!tip] 核心洞察
> 将人类直观的定性错误描述与严格定量的时空错误比例评分相结合，并训练MLLM执行多步CoT推理，是弥合机器评估与人类偏好差距、提升可解释性的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoRealBench：面向生成人本视频的链式思考真实度评估基准 |
| 英文题名 | VideoRealBench: A Chain-of-Thought Realism Evaluation Benchmark for Generated Human-Centric Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_VideoRealBench_A_Chain-of-Thought_Realism_Evaluation_Benchmark_for_Generated_Human-Centric_Videos_CVPR_2026_paper.html) · [Code](https://github.com/MCG-NJU/VideoRealBench) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoRealBench (包含 VideoRealDataset 与 VideoRealEval) |
| Dataset | VideoRealDataset, Video-Bench |

> [!tip] 效果简介
> - VideoRealDataset (测试集) 上，PLCC / SROCC 57.07% / 56.78% vs 见表4（多数开源和闭源模型低于此值） (优于现有最强模型)。
> - 偏好一致性实验 上，Preference Consistency Ratio (PCR) 0.925 vs 0.754 (VideoPhy-2) (+0.171)。
> - Video-Bench (泛化测试) 上，SROCC (Temporal Consistency) 0.474 vs 0.402 (GPT-4o) (+0.072)。

## 概要

### 问题背景

随着文本到视频生成模型的快速发展，对生成视频真实度的自动评估需求日益迫切。然而，现有基准存在三个核心瓶颈：

1. **标注质量低下**：大量依赖LLM生成的标注，常出现描述错误、不完整或幻觉现象，难以作为可靠的真值参考。
2. **评分标准模糊**：评分多凭直觉或LLM直接生成，缺乏严格定义，导致评分不一致且与人类偏好偏差较大。
3. **缺乏可解释推理**：现有评估器仅输出不透明分数，无法解释评分依据，限制了评估结果的可信度与可验证性。

这些问题使得机器评估与人类对视频真实度的判断之间存在显著鸿沟。

### 核心方法定位

VideoRealBench 从**评分标准重定义**与**推理过程显式化**两个维度切入，构建了面向生成人本视频真实度评估的完整基准。其核心设计包括：

- **VideoRealDataset**：一个高质量人工标注数据集，包含3,297个视频，每个视频配有严格依据时空错误占比定义的1-5分整数评分，以及三步思维链（CoT）推理过程——问题描述、标准遵循、答案。
- **VideoRealEval**：基于Qwen2.5-VL-7B使用LoRA微调的评估模型，具备三步推理能力，使评分过程透明且可验证。

该方法将人类直观的定性错误描述与严格定量的时空错误比例评分相结合，并强制评估器执行多步CoT推理，是弥合机器评估与人类偏好差距、提升可解释性的关键。

### 主要结果

- **评分对齐**：VideoRealEval在VideoRealDataset测试集上达到**57.07% PLCC**和**56.78% SROCC**，显著优于其他主流开源与闭源评估模型。
- **偏好一致性**：重新标注后的评分在偏好一致性比率（PCR）上达到**0.925**，远高于VideoPhy-2的0.754，证明新评分标准更贴合人类偏好。
- **CoT推理的关键作用**：消融实验证实，完整CoT推理使PLCC从53.89%提升至57.07%，是评分对齐提升的核心驱动力。
- **泛化能力**：在Video-Bench和EvalCrafter等外部基准上的零样本测试中，VideoRealEval同样展现出优于GPT-4o等模型的时序一致性评估能力（SROCC: 0.474 vs. 0.402）。

### 方法谱系与知识库定位

VideoRealBench属于**视频质量评估**与**多模态大模型对齐**的交叉方向。与VideoPhy-2、VideoScore、VMBench等先前基准相比，其核心差异在于：

- **评分标准**：从模糊直觉评分转向基于错误时空占比的严格定量评分；
- **推理机制**：从无解释的分数输出转向三步CoT可解释推理；
- **标注质量**：从LLM生成标注转向多人独立标注与审核。

在知识库中，该工作可作为**可解释视频真实性评估**的基准方法，为后续研究提供高质量标注数据和评估模型。

### 问题背景：生成人本视频的真实性评估困境

随着文本到视频（T2V）生成模型的快速发展，生成视频的视觉质量已大幅提升，但**真实性（realism）**——即视频内容是否符合物理规律与人类视觉经验——仍是制约其实际应用的核心瓶颈。人本视频（human-centric videos）因涉及复杂的人体运动、物体交互与物理约束，其真实性缺陷尤为突出，典型错误包括肢体畸变、物体穿模、违背重力等。然而，当前缺乏能够可靠、可解释地评估此类视频真实性的基准与工具，导致模型迭代缺乏有效的反馈信号。

### 现有基准的三大缺口

现有视频真实性评估基准普遍存在三个结构性缺陷，构成当前领域的关键瓶颈：

**1. 标注质量低下，LLM生成描述不可靠。** 为降低标注成本，许多基准（如 **VideoPhy-2**）大量依赖大语言模型（LLM）自动生成错误描述与评分。但如图4所示，LLM生成的描述频繁出现**幻觉**（描述不存在的错误）、**不完整**（遗漏关键错误）或**完全缺失**等问题。这些噪声标注直接污染了评估信号，使得基于此训练的评估器难以学习到真实的真实性判断标准。

**2. 评分标准模糊，与人类偏好不对齐。** 现有基准的评分多依赖标注员的直觉判断或LLM的模糊打分，缺乏可复现的量化依据。以VideoPhy-2为例，其评分与人类真实偏好的一致性比率（PCR）仅为0.754，表明近四分之一的评分排序与人类判断相悖。这种不对齐使得评估分数难以真实反映视频质量，削弱了基准的实用价值。

**3. 缺乏可解释推理，评估过程不透明。** 主流评估模型仅输出一个不透明的分数，用户无法理解分数背后的判断依据。在真实性评估这类需要细粒度归因的任务中，缺乏推理过程不仅降低了评估结果的可信度，也阻碍了对模型失败模式的诊断与改进。

### 本文动机：构建透明、可验证、与人类对齐的评估体系

针对上述缺口，本文提出 **VideoRealBench**，一个面向生成人本视频的链式思考（Chain-of-Thought, CoT）真实度评估基准。其核心动机在于：

- **以人类直观错误描述驱动定量评分**：将人类对视频错误的定性感知（“画面中有多大区域出错？持续了多久？”）转化为严格的1-5分整数评分标准，依据错误内容的空间占比与时间占比进行客观量化，消除评分模糊性。
- **以三步思维链实现可解释评估**：强制评估器输出 `<Problem Description>`（错误描述）→ `<Standard Adherence>`（评分依据）→ `<Answer>`（最终分数）的推理链，使评分过程透明、可验证，便于人工审计与模型诊断。
- **以高质量人工标注弥合人机差距**：通过三位标注员独立标注、多数投票与LLM润色后人工审核的流程，构建高质量的 **VideoRealDataset**，并以此训练 **VideoRealEval** 评估器，显著提升与人类偏好的一致性（PCR从0.754提升至0.925）。

通过将人类直观的定性错误描述与严格定量的时空错误比例评分相结合，并训练多模态大语言模型（MLLM）执行多步CoT推理，VideoRealBench旨在弥合机器评估与人类偏好之间的鸿沟，为生成人本视频的真实性评估提供一个更可靠、更透明的基准平台。

## 核心方法与创新机理

VideoRealBench 的核心创新在于系统性地重构了生成人本视频的真实度评估范式，通过三个紧密耦合的“changed slots”解决了现有基准与人类偏好严重不对齐的根本瓶颈。

### 从模糊直觉到严格量化的评分标准

现有基准（如 **VideoPhy-2**、**VideoScore**）的评分体系存在根本性缺陷：评分依赖 LLM 生成的直觉判断或模糊定义，导致评分不一致且与人类真实感受脱节。VideoRealBench 的核心突破在于将人类对“错误”的直观感知转化为可严格量化的指标——**依据错误内容在画面中的空间占比与持续时间，定义了 1 至 5 分的整数评分标准**（Table 2）。例如，当错误内容占据画面超过 40% 且持续大部分帧时，视频将被评为最低分。这一设计将评分从主观臆断转变为可复现的测量过程，从根本上解决了评分标准模糊的瓶颈。

### 从黑盒分数到可验证的三步思维链推理

现有评估器仅输出不透明的分数，无法解释“为什么这个视频真实度低”。VideoRealBench 强制评估器执行三步思维链（CoT）推理：**`<Problem Description>`（错误描述）→ `<Standard Adherence>`（评分依据）→ `<Answer>`（最终分数）**。这一设计使评分过程完全透明且可验证。消融实验提供了决定性证据：当移除 CoT 推理时，PLCC 从 57.07% 骤降至 53.89%（Table 6），证实推理链是弥合机器评估与人类偏好差距的关键因果杠杆。

### 从 LLM 生成到多人协作的质量控制闭环

现有基准大量依赖 LLM 生成标注，导致描述幻觉、不完整或缺失（Figure 4）。VideoRealBench 构建了严格的多人标注质量控制闭环：**每位视频由三位标注员独立标注，采用多数投票或平均取整确定最终分数**；随后利用 DeepSeek 润色 CoT 推理文本，再经人工审核确保一致性与准确性。这一流程使得重新标注后的评分在偏好一致性比率（PCR）上达到 0.925，远高于 VideoPhy-2 的 0.754（Table 8），直接证明了标注质量对评估有效性的决定性作用。

三个创新点形成因果闭环：严格量化的评分标准为推理提供了客观依据，三步 CoT 使评分过程可解释且可纠错，多人标注质量控制则确保了训练数据的可靠性。三者共同作用，使得基于 Qwen2.5-VL-7B 微调的 VideoRealEval 在 VideoRealDataset 测试集上达到 57.07% PLCC 和 56.78% SROCC，显著优于所有对比模型（Table 4）。

VideoRealBench 的整体框架围绕一个核心目标构建：**弥合机器评估与人类偏好之间的鸿沟**。现有基准（如 **VideoPhy-2**、**VideoScore**、**VMBench**）普遍存在标注质量低下、评分标准模糊、缺乏可解释推理等瓶颈，导致其评分与人类对视频真实性的直觉判断严重不对齐。VideoRealBench 通过重新设计从数据标注到模型推理的完整链路，系统性地解决了这些问题。

框架由两大组件构成，形成“数据驱动模型、模型验证数据”的闭环：

1.  **VideoRealDataset**：一个高质量、细粒度人工标注的数据集，为模型训练提供对齐人类偏好的监督信号。
2.  **VideoRealEval**：一个基于多模态大语言模型（MLLM）微调、具备三步思维链推理能力的评估器，将标注知识内化为可解释的评估行为。

整个 Pipeline 包含四个串行模块（对应 Figure 2），其数据流与模块关系如下：

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of VideoRealBench. We show the whole process, including the data collection and annotation, the training process of VideoRealEval, and the example of the evaluation process*

### 1. 视频收集与筛选
**输入**：现有开源视频生成数据集（如 VideoPhy-2 中由 7 个文本到视频模型生成的视频）。  
**处理**：从中筛选出**人本视频**（human-centric videos），并剔除内容模糊或无意义的低质量样本。  
**输出**：待标注的原始视频池。  
**设计意图**：聚焦“人”这一最敏感的真实性感知对象，提高标注的针对性与一致性。

### 2. 人工标注与评分生成
这是整个框架的**核心瓶颈突破点**，分为三个子步骤：

- **错误描述**：标注员依据预定义的三大错误类别（人状态错误、物状态错误、人机交互错误，见 Table 1）对视频中的真实性缺陷进行定性描述。
- **定量评分**：摒弃以往依赖直觉或 LLM 生成的模糊评分，转而采用**严格量化的 1–5 分整数评分标准**。该标准的核心依据是：错误内容在画面中的**空间占比**以及错误持续的**帧数占比**（见 Table 2）。例如，当错误内容占据画面超过 40% 且持续大部分时间时，会被评为最低分。这种将人类直观判断转化为可计算指标的方式，是评分客观性与可复现性的关键。
- **CoT 推理生成**：为每个视频生成三步思维链（Chain-of-Thought）：
    1.  `<Problem Description>`（问题描述）：具体指出视频中的真实性错误。
    2.  `<Standard Adherence>`（标准遵循）：说明如何根据定量评分标准得出当前分数。
    3.  `<Answer>`（答案）：给出最终的整数评分。

为确保标注质量，每个视频由**三位标注员独立标注**。最终分数采用多数投票决定；若三人评分各不相同，则取平均值四舍五入。生成的 CoT 文本会经过 DeepSeek 等 LLM 润色，并由人工最终审核，以保证一致性与准确性。

### 3. VideoRealEval 训练
**输入**：VideoRealDataset 中的视频及其对应的三步 CoT 标注（共 3,297 个视频，其中 2,309 个用于训练，988 个用于测试）。  
**处理**：基于 **Qwen2.5-VL-7B** 模型，使用 **LoRA** 微调策略进行训练。模型学习从视频输入直接生成包含三步推理的完整评估答案。训练在 4 块 V100 GPU 上进行 10 个 epoch，学习率设为 1e-4，每 GPU 批大小为 1。  
**输出**：具备三步推理能力的评估器 VideoRealEval。  
**关键机制**：通过强制模型学习“描述问题 → 引用标准 → 输出分数”的因果链，使评分过程**透明化、可验证**，而非直接输出不可解释的分数。

### 4. 评估与验证
**输入**：待评估的生成视频。  
**处理**：VideoRealEval 对视频进行推理，输出包含 `<Problem Description>`、`<Standard Adherence>` 和 `<Answer>` 的结构化评估结果。  
**评估指标**：
- **相关性指标**：计算模型评分与人工标注之间的皮尔逊线性相关系数（PLCC）和斯皮尔曼秩相关系数（SROCC），衡量评分准确性。
- **偏好一致性指标**：引入偏好一致性比率（PCR），衡量模型评分排序与人类偏好排序的一致程度。其定义为：
    $$\mathrm{PCR} = \frac{1}{|\mathcal{P}|} \sum_{(i,j) \in \mathcal{P}} \mathbf{1}\left( (S(v_i) > S(v_j)) \iff (v_i \succ v_j) \right)$$
    其中 $\mathcal{P}$ 为所有视频对，$v_i \succ v_j$ 表示人类认为视频 $v_i$ 的真实度高于 $v_j$。

### 框架优势总结
该框架的核心洞察在于：**将人类直观的定性错误描述与严格定量的时空错误比例评分相结合，并训练 MLLM 执行多步 CoT 推理，是弥合机器评估与人类偏好差距、提升可解释性的关键**。消融实验证实，同时进行评分重对齐和推理重对齐（即完整的 CoT）将 PLCC 从 53.89% 提升至 57.07%，而 VideoRealBench 的 PCR 达到 0.925，远高于 VideoPhy-2 的 0.754，直接验证了框架设计的有效性。

VideoRealBench 的核心工作流由三个紧密耦合的模块构成：**视频收集与筛选**、**人工标注与提示生成**、以及 **VideoRealEval 训练**。整个流水线如图 Figure 2 所示，其设计目标是将人类直观的定性错误描述转化为严格定量的时空错误比例评分，并强制评估器输出可验证的三步思维链。

### 视频收集与筛选

该模块负责构建高质量的人本视频数据集。视频源来自现有开源数据集（如 VideoPhy-2），这些视频由 7 个文本到视频模型生成。筛选过程聚焦于人本视频，并剔除内容模糊或无意义的样本，最终形成包含 3,297 个视频的 VideoRealDataset，按 2,309/988 划分为训练集和测试集。

### 人工标注与提示生成

这是整个基准的核心瓶颈突破点。标注过程分为三个子步骤：

**错误分类与问题描述**：标注员依据预定义的三大错误类别（人状态、物状态、人机交互）对视频中的真实性错误进行识别和描述，具体指南见 Table 1。这一步直接针对现有 LLM 生成描述中普遍存在的幻觉、不完整和缺失问题（如 Figure 4 所示）。

**定量评分**：评分标准是 VideoRealBench 的核心创新。与传统依赖直觉或 LLM 模糊打分不同，该方法严格依据**错误内容在画面中的空间占比**和**错误帧的持续时间占比**，定义了 1-5 分的整数评分量表（Table 2）。例如，若错误占据画面 40% 以上区域且持续大部分帧，则对应最低分。这种定量化设计使评分过程客观、可复现。

**CoT 响应生成**：为每段视频生成三步思维链响应：`<Problem Description>`（问题描述）→ `<Standard Adherence>`（标准遵循）→ `<Answer>`（答案）。为确保准确性，每段视频由三位标注员独立标注：若存在多数分数则直接采用；若三个分数各不相同，则取平均值四舍五入作为最终分数。随后利用 DeepSeek 对 CoT 文本进行润色，并经人工审核确认。

### VideoRealEval 训练

评估器基于 **Qwen2.5-VL-7B** 使用 **LoRA** 微调策略进行训练。模型在 4 块 V100 GPU 上训练 10 个 epoch，学习率设为 1e-4，每 GPU 批大小为 1。训练数据即上述人工标注的 CoT 响应，使模型学会执行三步推理评估，而非仅输出一个不透明分数。

### 关键公式

评估标注与人类偏好对齐程度的核心指标是**偏好一致性比率（Preference Consistency Ratio, PCR）**，其定义为：

$$\mathrm{PCR} = \frac{1}{|\mathcal{P}|} \sum_{(i,j) \in \mathcal{P}} \mathbf{1}\left( (S(v_i) > S(v_j)) \iff (v_i \succ v_j) \right)$$

其中，$\mathcal{P}$ 表示所有视频对集合，$S(v)$ 为评分函数，$v_i \succ v_j$ 表示人类标注者认为视频 $v_i$ 的真实度高于 $v_j$。PCR 衡量的是评分排序与人类偏好排序一致的配对比例。实验表明，VideoRealBench 的重新标注评分在 PCR 上达到 **0.925**，远高于 VideoPhy-2 原始评分的 **0.754**（Table 8），验证了定量评分标准与人类偏好的高度一致性。

### 模块间的因果机制

三个模块形成了一条清晰的因果链：**视频筛选**保证了评估对象的针对性（人本视频）；**定量评分标准与多人标注机制**解决了评分模糊和标注噪声问题，这是 PCR 从 0.754 跃升至 0.925 的直接原因；**CoT 推理训练**则赋予了评估器可解释性，消融实验证实完整 CoT 将 PLCC 从 53.89% 提升至 57.07%（Table 6），而同时进行评分重对齐和推理重对齐是达到最优性能的关键（Table 7）。

## 实验与关键发现

### 核心实验设计

为全面评估 **VideoRealEval** 的性能与泛化能力，作者设计了多层次的实验体系。首先，在自建的 **VideoRealDataset** 测试集（988个视频）上，以皮尔逊线性相关系数（PLCC）和斯皮尔曼秩相关系数（SROCC）为核心指标，比较 VideoRealEval 与各类主流开源及闭源视觉语言模型。其次，通过偏好一致性比率（PCR）量化新评分标准与人类偏好的对齐程度。此外，在 **Video-Bench**（Han et al., CVPR 2025）和 **EvalCrafter**（Liu et al., CVPR 2024）两个外部基准上进行零样本泛化测试，以验证模型的跨数据集迁移能力。

### 主实验结果

**VideoRealEval 在自建基准上显著领先。** 如 Table 4 所示，基于 Qwen2.5-VL-7B 微调的 VideoRealEval 在 VideoRealDataset 测试集上取得了 57.07% 的 PLCC 和 56.78% 的 SROCC，在所有参评模型中表现最优。相比之下，闭源模型 GPT-4o 的 PLCC 仅为 51.94%，SROCC 为 50.71%；同为 7B 量级的开源模型 Qwen2.5-VL-7B 未经微调时 PLCC 仅 47.55%。值得注意的是，即使将原始 VideoPhy-2 的自动评估器在 VideoRealDataset 上重新训练（Table 4 中 VideoPhy-2-AutoEval*），其 PLCC（41.05%）也远低于 VideoRealEval，这反向证明了重新设计的评分标准与推理结构是性能提升的核心驱动力，而非仅仅是数据域适配。

**新评分标准与人类偏好高度一致。** 通过偏好一致性比率（PCR）的定量分析，VideoRealBench 的重新标注评分取得了 **0.925** 的 PCR，远超 VideoPhy-2 原始评分的 0.754（Table 8）。PCR 定义为在人类标注者明确偏好的视频对中，评分函数给出相同排序的比例，其公式为：
$$\mathrm{PCR} = \frac{1}{|\mathcal{P}|} \sum_{(i,j) \in \mathcal{P}} \mathbf{1}\left( (S(v_i) > S(v_j)) \iff (v_i \succ v_j) \right)$$
0.925 的 PCR 意味着在 92.5% 的对比中，基于时空占比的严格五级评分与人类直观偏好排序一致，这为 VideoRealEval 学习的目标信号质量提供了有力保障。

**泛化能力初步验证。** 在跨基准泛化测试中，VideoRealEval 在 Video-Bench 的时序一致性维度上取得 0.474 的 SROCC，优于 GPT-4o 的 0.402（Table 10）；在 EvalCrafter 上 SROCC 达到 0.573。虽然绝对数值不高，但在零样本设定下超越通用大模型，表明模型学到了可迁移的“真实性缺陷识别”能力，而非单纯记忆训练集偏差。

### 消融实验

**整数评分优于语言描述。** Table 5 对比了两种评分输出形式：直接预测 1-5 整数评分，或生成语言描述后再映射为分数。整数评分取得 57.07% PLCC，略高于语言描述的 56.89%。作者分析认为，整数评分强制模型做出更明确的判断，减少了语言描述中可能引入的歧义和映射误差。

**思维链推理是性能提升的关键。** Table 6 系统拆解了 CoT 三步骤的贡献。基础模型（无 CoT，仅输出分数）的 PLCC 为 53.89%；仅添加 `<Problem Description>` 后提升至 55.01%；同时包含 `<Problem Description>` 和 `<Standard Adherence>` 时达到最优的 57.07%。这表明，显式地要求模型先描述错误再对照评分标准进行判断，能有效引导其注意力到关键的时空错误特征上，而非依赖黑箱式的整体感知。

**评分重对齐与推理重对齐具有协同效应。** Table 7 的消融显示，若仅使用 VideoRealBench 的重新标注分数但保留 VideoPhy-2 原有的粗糙推理文本进行训练，PLCC 为 55.92%；若同时使用重新标注的分数和重新标注的 CoT 推理（即完整 VideoRealEval 训练方案），PLCC 进一步提升至 57.07%。这证实了高质量推理过程本身对模型学习具有独立贡献，评分信号与推理信号的双重重对齐是必要的。

**模型输出高度稳定。** Table 9 的稳健性测试表明，在三次独立运行中，98.92% 的测试样本获得了完全相同的分数，说明 VideoRealEval 的评分不依赖于随机种子或微小的输入扰动，具备工程部署所需的可靠性。

### 失败模式与局限性分析

尽管 VideoRealEval 在多项指标上表现优异，但其性能上限仍受限于基座模型规模（7B）和训练数据覆盖范围。在涉及极端复杂的人机交互错误（如多物体同时畸变且相互遮挡）时，模型的 `<Problem Description>` 偶尔出现遗漏或描述不够精确的情况，导致后续评分偏差。此外，评分标准中“错误占画面 40% 以上为 1 分”等阈值设定基于经验规则，其在包含大量小目标错误或全景畸变等特殊场景下的适用性尚未经过大规模校准验证。泛化实验中 SROCC 绝对值仍不高，提示模型可能过拟合到了人本视频特有的错误模式，向非人本视频或全新生成模型产出的迁移仍需谨慎。

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/010_Table_6.jpg]]
*Table 6: Ablations for CoT. Rationales are beneficial for evaluator to obtain scores more aligned with human preferences*

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/007_Table_5.jpg]]
*Table 5: Comparison of different score form. Verbal descriptions are slightly lower than integer-based scores*

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/013_Table_7.jpg]]
*Table 7: Ablations for annotation realignment. Realignment of score and rationale enhance the alignment between VideoRealEval with human preferences*

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/012_Table_10.jpg]]
*Table 10: Generalization on other benchmarks. We choose Video-Bench [19] and EvalCrafter [35] because their tasks and evaluation metrics are similar to our task*

![[assets/figures/papers/paper_list_l2752_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_VideoRealBench_A/figures/008_Table_3.jpg]]
*Table 3: Comparison between VideoRealBench with prior works. ”Partially” indicates that the dataset only fulfills this feature to some extent*

## 定位与知识库关联

### 1. 与先前基准的关系：填补“可解释真实性评估”的空白

VideoRealBench 并非凭空产生，而是针对现有视频生成评估基准在**真实性维度**上的系统性不足而提出的。理解其定位，需要先厘清先前工作的瓶颈：

- **VideoPhy-2**：作为最直接的前置基准，VideoPhy-2 首次大规模关注生成视频的物理真实性问题。然而，其核心缺陷在于**标注质量与评分标准的模糊性**。该基准大量依赖 LLM 生成错误描述，导致描述幻觉、信息不完整或完全缺失（见 Figure 4）；其评分依赖直觉判断，缺乏可量化的客观依据。实验证据表明，VideoPhy-2 原始评分的偏好一致性比率（PCR）仅为 0.754，远低于 VideoRealBench 重新标注后的 0.925（Table 8），直接证明了其评分与人类偏好的系统性偏差。VideoRealBench 正是在 VideoPhy-2 的视频源基础上，通过**重标注**与**评分标准重定义**实现了质的提升。

- **VideoScore** 与 **VMBench**：前者尝试多维评估但定义模糊且缺乏推理过程；后者主要关注运动质量，未对真实性的细粒度错误类型（如人状态、物状态、人机交互）进行系统建模。Table 3 的系统对比显示，这些工作在“人工精细标注”“CoT 推理”“严格评分标准”等维度上均存在缺失或仅部分满足。

- **EvalCrafter** (Liu et al., CVPR 2024) 与 **Video-Bench** (Han et al., CVPR 2025)：作为综合评估基准，它们覆盖了更广泛的评估维度，但在真实性评估的细粒度与可解释性上并未深入。VideoRealEval 在零样本泛化测试中（Table 10）于 Video-Bench 的时序一致性指标上达到 0.474 SROCC，超越 GPT-4o 的 0.402，表明其学到的真实性判别能力具有一定跨基准迁移性，但该泛化性能仍受限于训练数据的分布。

**核心区分点**：VideoRealBench 的本质创新不在于提出全新的评估任务，而在于将**人类直观的定性错误描述**与**严格定量的时空错误比例评分**相耦合，并强制评估器输出可验证的三步思维链。这一设计使真实性评估从“不透明打分”转向“透明推理”，是弥合机器评估与人类偏好差距的关键机制。

### 2. 适用边界与局限

VideoRealBench 的设计决策同时划定了其适用边界：

- **模态与内容边界**：基准聚焦于**生成式人本视频**（human-centric videos）的真实性评估，错误分类体系（人状态、物状态、人机交互）均围绕人体结构、动作与交互展开。对于纯场景视频、非人主体或抽象生成内容的真实性评估，该框架无法直接复用。

- **评分阈值的经验性**：评分标准中定义的空间占比阈值（如“错误内容超过画面 40% 为 1 分”）和帧数阈值（如“超过 80% 帧包含错误为 2 分”，见 Table 2）基于人类直觉设定，缺乏大规模跨场景验证。这意味着在不同分辨率、不同主体尺度的视频中，同一阈值的感知意义可能不同，其普适性需要进一步检验。

- **模型容量的上限约束**：VideoRealEval 基于 7B 参数的 Qwen2.5-VL 模型微调，在 4 张 V100 GPU 上训练 10 个 epoch。这一规模限制了模型在极端复杂案例（如多重错误叠加、罕见失真类型）上的推理上限。分析指出，当前评估器可能未覆盖未来更先进生成模型可能产生的新型失真。

- **数据分布依赖**：训练数据源自 7 个文本到视频模型在 VideoPhy-2 中的生成结果，其错误分布受限于这些模型的能力边界。若未来生成模型的失真模式发生质变，当前评估器的判别能力可能退化。

### 3. 开放问题

从方法谱系的角度，VideoRealBench 留下以下待解问题：

1. **评分标准的跨文化普适性**：五级评分标准基于特定标注群体的直觉判断，不同文化背景对“真实”的容忍阈值可能存在差异。如何验证并校准这一标准的跨文化一致性，是基准走向广泛采用的前提。

2. **CoT 推理范式的可泛化性**：三步推理链（问题描述 → 标准遵循 → 答案）在真实性评估中有效，但这一结构化推理模式能否迁移到更开放的评估任务（如美学质量、创意性）或非人本视频领域，尚待验证。

3. **利用强 MLLM 进行数据增强的可行性**：当前标注完全依赖人工，成本高昂。能否利用 GPT-4o 等更强模型生成候选 CoT 标注，再由人工审核修正，从而在控制成本的同时扩展数据规模与错误覆盖类型，是提升评估器上限的潜在路径。

4. **从“评分对齐”到“排序对齐”的深化**：PCR 指标已证明 VideoRealBench 评分在成对偏好上高度一致（0.925），但如何将这种对齐从二元偏好扩展到更细粒度的全局排序一致性，仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/VideoRealBench_A_Chain_of_Thought_Realism_Evaluation_Benchmark_for_Generated_Human_Centric_Videos.pdf]]
