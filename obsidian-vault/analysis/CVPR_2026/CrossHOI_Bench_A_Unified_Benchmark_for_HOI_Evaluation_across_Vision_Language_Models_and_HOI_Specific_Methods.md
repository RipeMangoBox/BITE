---
title: "CrossHOI-Bench: A Unified Benchmark for HOI Evaluation across Vision-Language Models and HOI-Specific Methods"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CrossHOI_Bench_A_Unified_Benchmark_for_HOI_Evaluation_across_Vision_Language_Models_and_HOI_Specific_Methods.pdf
project_link: null
code_link: "https://github.com/ChelsieLei/CrossHOI-Bench"
aliases:
- CB
- CrossHOI-Bench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将 HOI 检测重新定义为多答案多项选择题（MCQA），通过自动 VLM 流水线生成候选负例并结合人工精炼，为每道题提供明确的正负例集合，从而消除不完全标注带来的误判，并统一了 VLM 和 HOI 专用模型的评估协议。
primary_logic: MCQA 格式既保留了 VLM 的自由文本生成特性，又通过固定选项提供了可控的评估空间，使得跨范式评估成为可能；同时，通过精心设计的困难负例和多设置评估，能够分离识别、定位和多人物交互能力，揭示 VLM 与 HOI 专用方法的互补优势（VLM 交互推理强但多动作/跨人归因弱，HOI 方法多动作识别好但分布外泛化差）。
claims:
- HICO-DET 的不完全标注导致 VLM 的 mAP 被严重低估至约 15%，而 HOI 方法也仅不足 50%。
- 在 CrossHOI-Bench 中，大模型 VLM（如 Qwen2.5-VL-32B）在零样本设置下 Macro-F1 超越最优 HOI 专用方法（50.71 vs 47.49）。
- 从 Setting 2 到 Setting 1（引入检测），VLM 性能明显下降，说明定位仍是其主要瓶颈。
- VLM 在多人物场景下有约 20-25% 的预测错误源于跨人物交互误分配，而 HOI 方法该比例为 15%。
---

# CrossHOI-Bench: A Unified Benchmark for HOI Evaluation across Vision-Language Models and HOI-Specific Methods

> [!tip] 核心洞察
> MCQA 格式既保留了 VLM 的自由文本生成特性，又通过固定选项提供了可控的评估空间，使得跨范式评估成为可能；同时，通过精心设计的困难负例和多设置评估，能够分离识别、定位和多人物交互能力，揭示 VLM 与 HOI 专用方法的互补优势（VLM 交互推理强但多动作/跨人归因弱，HOI 方法多动作识别好但分布外泛化差）。

| 字段 | 内容 |
|------|------|
| 中文题名 | CrossHOI-Bench：跨范式人体-物体交互统一评估基准 |
| 英文题名 | CrossHOI-Bench: A Unified Benchmark for HOI Evaluation across Vision-Language Models and HOI-Specific Methods |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.18753) · [Code](https://github.com/ChelsieLei/CrossHOI-Bench) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CrossHOI-Bench |
| Dataset | CrossHOI-Bench Setting 1, CrossHOI-Bench Setting 2, CrossHOI-Bench Setting 3 |

> [!tip] 效果简介
> - CrossHOI-Bench Setting 1 (Full HOI Detection) 上，Macro-F1 Qwen2.5-VL-32B (zero-shot) vs CMD-SE (HOI-specific SOTA) (+3.22%)。
> - CrossHOI-Bench Setting 1 上，Instance-F1 Qwen2.5-VL-32B (zero-shot) vs ADA-CM (HOI-specific SOTA) (+5.18%)。
> - CrossHOI-Bench Setting 2 (Localized Recognition) 上，Macro-F1 Qwen2.5-VL-32B (zero-shot) vs InternVL3-38B (best alternative VLM) (+3.96%)。

## 概要

现有 HOI（人体-物体交互）基准面临一个根本性瓶颈：**不完全标注导致评估失真**。以 HICO-DET 为代表的基准依赖精确匹配评估，但受限于视觉信息模糊（如 mid-motion 动作）和稀疏标注，大量合理交互未被标注为真值。这导致通用视觉语言模型（VLM）的灵活输出被系统性误判为错误——VLM 的 mAP 被压低至约 15%，而 HOI 专用方法也不足 50%（Figure 1c）。此外，现有基准中简单头类场景过多，掩盖了模型在多人、细粒度交互等真实困难场景中的差异。

针对这一问题，**CrossHOI-Bench** 将 HOI 检测重新定义为**多答案多项选择题（MCQA）**，通过自动 VLM 流水线生成候选负例并结合人工精炼，为每道题提供明确的正负例集合，从而消除不完全标注带来的误判，并统一了 VLM 与 HOI 专用方法的评估协议。MCQA 格式既保留了 VLM 的自由文本生成特性，又通过固定选项提供了可控的评估空间，使得跨范式评估成为可能。

核心发现可概括为三点：

1. **VLM 在交互推理上超越 HOI 专用方法**：大模型 VLM（如 Qwen2.5-VL-32B）在零样本设置下，Setting 1 的 Macro-F1 达到 50.71，超越最优 HOI 专用方法 CMD-SE（47.49），Instance-F1 领先 ADA-CM 达 5.18 个百分点（Table 1）。

2. **定位仍是 VLM 的主要瓶颈**：从 Setting 2（给定框的识别）到 Setting 1（完整检测），VLM 性能明显下降，表明其检测能力显著弱于识别能力。

3. **两类方法存在互补弱点**：VLM 在多动作同时发生时倾向于仅预测最显著动作，且在多人场景中约 20-25% 的错误源于跨人物交互误分配；HOI 方法多动作识别较好，但分布外泛化差，在细粒度相似动作上混淆率高达 52%。

CrossHOI-Bench 通过精心设计的困难负例和三种评估设置（完整检测、给定框识别、多人物图像级识别），成功分离了识别、定位和多人物交互能力，为跨范式 HOI 评估提供了统一的公平基准。



### 人体-物体交互理解的评估困境

人体-物体交互（Human-Object Interaction, HOI）检测旨在同时定位图像中的人与物体，并识别两者之间的交互关系。这一任务长期以来由专用检测范式主导，评估体系也围绕精确匹配（exact-match）的 mAP 指标构建，代表性基准如 HICO-DET。然而，随着通用视觉-语言模型（VLM）的快速崛起，这一评估框架暴露出根本性缺陷。

**核心瓶颈在于标注不完整与评估不兼容。** HICO-DET 等现有基准存在两类系统性问题：

**第一，标注稀疏导致误判。** 受限于视觉信息模糊（如 mid-motion 动作的瞬时状态难以标注）和人工标注成本，HICO-DET 中存在大量未标注但视觉上合理的交互。在精确匹配评估下，模型预测这些“未标注但正确”的交互会被一律判为错误。这一问题对 VLM 尤为致命——VLM 凭借开放的视觉推理能力，天然倾向于输出更全面的交互描述，却被严重惩罚至约 15% mAP，而 HOI 专用方法也仅不足 50% mAP（Figure 1(c)）。这意味着现有基准既低估了模型真实能力，也无法公平比较两类范式。

**第二，数据分布掩盖能力差异。** HICO-DET 的训练集与测试集分布高度相似（KL 散度仅 0.088），测试集中充斥大量简单头类场景（单人单物、动作视觉显著），导致模型在真实困难场景（多人物、细粒度交互、歧义动作）中的表现差异被淹没。

### 跨范式评估的统一需求

VLM 的兴起使问题更加紧迫。VLM 以自由文本生成方式回答交互问题，而 HOI 专用方法输出结构化三元组 `<人, 动作, 物体>`，两者输出空间根本不同。现有基准的精确匹配机制无法容纳 VLM 的灵活输出，也无法为两类方法提供统一的比较尺度。

这一困境催生了 **CrossHOI-Bench** 的核心动机：**能否设计一个评估协议，既保留 VLM 的自由生成特性，又提供可控的评估空间，从而公平比较 VLM 与 HOI 专用方法？**

### 本文的解决思路

CrossHOI-Bench 将 HOI 检测重新定义为**多答案多项选择题（MCQA）**。每道题目为一个 `<人, 物体>` 对提供四个候选交互选项，其中明确标注正例集合与精心构建的负例集合。这一格式的关键优势在于：

- **消除不完全标注的误判**：未标注但合理的交互不会被错误惩罚，因为负例经过显式筛选排除了这些模糊情况。
- **统一评估协议**：VLM 和 HOI 专用方法均通过选项选择给出答案，输出空间对齐。
- **保留生成特性**：MCQA 格式天然兼容 VLM 的文本生成能力，无需强制结构化输出。

通过这一设计，CrossHOI-Bench 不仅揭示了 VLM 与 HOI 专用方法的互补优势（VLM 交互推理强但定位弱，HOI 方法多动作识别好但分布外泛化差），更为跨范式 HOI 评估建立了可复用的方法论框架。



## 核心方法与创新机理

CrossHOI-Bench 的核心创新并非提出新的 HOI 检测模型，而是**重新定义了 HOI 评估的任务形式与数据分布**，从而首次实现了视觉语言模型（VLM）与 HOI 专用方法在统一、公平的协议下的可比评估。这一创新通过以下四个相互耦合的 **changed slots** 实现。

### 1. 任务形式：从精确匹配检测到多答案多项选择

传统 HOI 基准（如 HICO-DET）采用精确匹配检测（exact-match detection）：模型输出 `<人, 物体, 动作>` 三元组，与标注完全一致才算正确。这一范式对 VLM 构成双重惩罚——VLM 的开放式文本生成天然难以与固定标签空间精确对齐，而 HICO-DET 的标注不完整性（大量合理交互未被标注）更将 VLM 的灵活输出误判为错误，导致其 mAP 骤降至约 15%（Figure 1c）。

CrossHOI-Bench 将任务重新定义为 **多答案多项选择题（multiple-answer, multiple-choice QA）**：每道题针对一个人-物对提供四个候选交互选项，其中可包含零至多个正确答案。这一格式的关键优势在于：
- **保留 VLM 的自由生成特性**：VLM 无需适配特定分类头，仅需从给定选项中做出选择，与 VLM 的指令跟随范式天然兼容；
- **提供可控评估空间**：固定选项集合明确了评估边界，消除了因标注不完整导致的误判——凡不在选项中的交互均不纳入评估，未标注但合理的交互被纳入负例而非被错误惩罚；
- **统一跨范式评估协议**：HOI 专用方法通过 Top-k 匹配策略（选择其预测分数最高的 k 个输出与选项匹配）即可参与同一评估，无需修改模型架构。

### 2. 评估指标：从单一 mAP 到多维集合匹配指标

传统基准以 mAP（mean Average Precision）为核心指标，该指标依赖精确匹配且对类别频率敏感，在头类主导的 HICO-DET 中容易掩盖模型在长尾类别上的表现差异。

CrossHOI-Bench 采用基于集合匹配的多维指标体系（详见附录 C 公式定义）：

| 指标 | 公式 | 含义 |
|------|------|------|
| **Macro-F1** | $\mathrm{Macro-F1} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \frac{2 \sum_{q} \mathbf{1}[c \in P_q \cap G_q]}{\sum_{q} \mathbf{1}[c \in P_q] + \sum_{q} \mathbf{1}[c \in G_q]}$ | 类平衡 F1，对所有 HOI 类别分别计算 F1 后取平均，消除头类主导偏差 |
| **Instance-F1** | $\mathrm{Instance-F1} = \frac{1}{|Q|} \sum_{q \in Q} \frac{2|P_q \cap G_q|}{|P_q| + |G_q|}$ | 问题级 F1，先计算每道题的 F1 再取平均，反映单样本表现 |
| **Micro-F1** | $\mathrm{Micro-F1} = \frac{2 \sum_{q} |P_q \cap G_q|}{\sum_{q} |P_q| + \sum_{q} |G_q|}$ | 全局 F1，汇总所有预测与真值后计算单一值 |
| **Exact Match (EM)** | $\mathrm{EM} = \frac{1}{|Q|} \sum_{q \in Q} \mathbf{1}[P_q = G_q]$ | 预测集合与真值完全一致的题目比例，最严格的指标 |

其中 Macro-F1 是核心指标，因其对类别不平衡具有鲁棒性，且能公平反映模型在长尾交互类别上的识别能力。

### 3. 数据分布：从头类主导到难度重分配

HICO-DET 测试集与训练集分布高度相似（KL 散度仅 0.088），包含大量简单重复场景（单人单物、动作视觉明显），导致模型间的真实能力差异被掩盖。

CrossHOI-Bench 通过两阶段筛选重塑数据分布：
- **移除简单场景**：剔除单人简单背景下视觉明显的动作、多人执行相同无歧义交互等场景；
- **重分配测试分布**：最终基准与 HICO-DET 训练集的 KL 散度上升至 0.629，显著增加了多人场景、细粒度相似交互、遮挡/模糊动作等困难样本的比例。

这一设计使得基准难度大幅提升——在完整 HICO-DET 测试集上表现相近的模型，在 CrossHOI-Bench 上可呈现显著差异（Figure 6），从而更有效地诊断模型在真实困难场景中的能力边界。

### 4. 负例构建：从隐式缺失到显式精炼

传统基准中，凡未标注的交互均被视为“错误”，但其中大量是视觉信息不足（如 mid-motion 动作）或标注稀疏导致的合理交互。CrossHOI-Bench 首次为每道题构建了**明确的负例集合**，构建流程为：

1. **粗筛选（Coarse Screening）**：利用多阶段 VLM 管线（GPT-4.1 → Qwen2.5-VL-32B + GPT-4o）自动生成候选负例，排除明显不合理选项；
2. **人工精炼（Manual Refinement）**：人工剔除简单场景，校正自动筛选错误，并补充困难正例与负例（如细粒度相似动作、多人场景下的交互歧义）。

这一流程的关键保障在于：粗筛选使用的 VLM 并无偏袒——HOI 专用模型对自动筛选负例的认可度（约 99%）甚至高于 VLM 自身（95–97%），保证了负例的客观性与跨范式公平性（Table 4）。消融实验进一步验证，移除粗筛选中的 Qwen2.5-VL-32B 后基准难度下降约 2% Macro-F1，说明该步骤对生成有效负例具有实质贡献（Table 12）。

### 创新耦合效应

上述四个 changed slots 并非孤立改进，而是形成因果闭环：**MCQA 格式**使跨范式评估成为可能 → **多维指标**揭示不同维度的能力差异 → **难度重分配**放大模型间真实差距 → **显式负例**消除标注不完整带来的评估噪声。这一耦合使得 CrossHOI-Bench 能够首次揭示 VLM 与 HOI 专用方法的互补优势：VLM 在交互推理上超越专门训练的方法（零样本 Macro-F1 50.71 vs. 47.49），但在多动作识别和跨人物归因上存在显著瓶颈；HOI 方法在多动作场景下召回率更高，但在分布外泛化上明显弱于 VLM。



CrossHOI-Bench 的构建与评估围绕一个核心重构展开：**将 HOI 检测重新定义为多答案多项选择题（multiple-answer, multiple-choice QA）**。这一设计并非简单的格式转换，而是对评估协议的根本性修正——它通过为每道题明确提供正例与负例集合，消除了传统精确匹配评估下因标注不完整而产生的大量假阴性惩罚。

整个框架由三个串联的模块组成，形成“数据筛选 → 选项生成 → 多设置评估”的闭环流水线：

### 1. 场景精炼（Scene Refinement）

流水线的第一步是对源数据集（HICO-DET 测试集）进行主动筛选，目标是**移除过于简单的场景，重新平衡数据分布**。具体剔除的场景包括：单人简单背景下执行视觉上显而易见的动作、多人执行相同交互且无歧义的情况等。这一操作使得训练集与重分配后测试集之间的 KL 散度从 0.088 跃升至 0.629，显著拉大了分布差异，迫使模型在面对真实困难场景时展现出能力差异。最终主基准保留 1,274 张图像，覆盖 600 个 HOI 类别。

### 2. 选项生成：粗筛 + 人工精炼

在精炼后的图像上，框架为每个人-物对生成一道四选项选择题，其正例来自原始标注，负例则通过“自动粗筛 → 人工精炼”两阶段构建：

- **Coarse Screening（粗筛）**：采用多阶段 VLM 管线。首先由 GPT-4.1 初步分离候选交互，随后由 Qwen2.5-VL-32B 和 GPT-4o 对每个候选进行联合评估，生成候选负例集合。这一设计利用了不同 VLM 的互补判断能力，减少单一模型的系统性偏差。
- **Manual Refinement（人工精炼）**：人工剔除自动筛选中的错误负例，并补充粗筛遗漏的困难正例与负例。关键原则是：**排除那些视觉上合理但未被标注的交互**，确保负例确实代表“不应发生的交互”而非“标注遗漏”。消融实验表明，移除粗筛中的 Qwen2.5-VL-32B 后基准难度略有下降（Macro-F1 上升约 2%），验证了该步骤对生成有效负例的贡献。

最终生成的每道题包含四个候选选项，选项顺序随机化以避免位置偏差，且允许多个正确答案。整个基准共包含 3,773 道选择题。

### 3. 三级评估设置

框架通过三种递进的评估设置，系统性地分离模型的不同能力维度：

- **Setting 1（完整 HOI 检测）**：模型需自行完成人物检测与交互识别，评估完整的端到端 HOI 检测能力。这是对模型综合能力的最严格测试。
- **Setting 2（给定框的识别）**：提供 ground-truth 人体边界框，仅评估定位后的交互识别能力。通过对比 Setting 1 与 Setting 2 的性能差距，可量化定位误差对整体性能的拖累程度。
- **Setting 3（图像级多人识别）**：不提供任何定位信息，要求模型识别图像中所有人物发生的所有交互。此设置专门考察模型在多人场景下的交互归因与多动作识别能力。

三种设置共享同一套选择题，但输入信息逐级减少，形成从“精确定位+识别”到“纯图像理解”的能力光谱。这种设计使得 VLM 与 HOI 专用方法的互补优势得以显现：VLM 在 Setting 2 和 3 中交互推理能力突出，但从 Setting 2 到 Setting 1 引入检测后性能明显下降，揭示**定位仍是 VLM 的主要瓶颈**；HOI 专用方法在 Setting 1 中定位能力更稳定，但在分布外泛化（Setting 3）上表现逊色。

### 补充图表

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our HOI benchmark construction. Input image undergoes coarse screening and manual refinement to produce a four-choice question, followed by evaluation under three settings*



### 3.1 任务形式化：多答案多项选择题

CrossHOI-Bench 的核心创新在于将 HOI 检测从传统的精确匹配检测任务重新定义为**多答案多项选择题（multiple-answer, multiple-choice QA）**。对于图像中的每个人-物对，构建一道包含四个候选选项的选择题，其中正例为标注的真实交互，负例为精心筛选的困难干扰项。这一形式化消除了不完全标注带来的假阴性误判，同时统一了 VLM 和 HOI 专用模型的评估协议。

### 3.2 基准构建流水线

基准构建分为两个关键模块：

**粗筛选（Coarse Screening）**：采用多阶段 VLM 管线自动生成候选负例。具体流程为：
1. **GPT-4.1** 初步将候选交互分为“可能正确”与“明显错误”两类；
2. 对剩余候选，由 **Qwen2.5-VL-32B** 和 **GPT-4o** 分别进行视觉验证，筛选出视觉上合理但实际未发生的交互作为负例候选。

消融实验（Table 12）表明，移除粗筛选中的 Qwen2.5-VL-32B 后，基准难度略有下降（Macro-F1 上升约 2%），验证了该步骤对生成有效困难负例的关键贡献。

**人工精炼（Manual Refinement）**：人工剔除简单场景（如单人简单背景下执行视觉明显动作），校正自动筛选的错误，并补充粗筛遗漏的困难正例与负例。经此步骤后，测试分布与训练分布的 KL 散度从 HICO-DET 的 0.088 提升至 **0.629**，显著增加了评估难度。

### 3.3 评估设置与指标

为分离不同能力维度，设计了三种评估设置：

- **Setting 1（完整 HOI 检测）**：模型需同时完成人物定位和交互识别，评估完整流水线能力。
- **Setting 2（给定框的识别）**：提供真值人框，仅评估局部化 HOI 识别能力，剥离定位误差。
- **Setting 3（图像级多人物识别）**：无定位信息，评估图像级多人物整体 HOI 识别。

### 3.4 核心评估公式

采用集合匹配指标，直接比较预测选项集合 $P_q$ 与真值选项集合 $G_q$：

**Macro-F1（类平衡 F1）**：对所有 HOI 类别 $\mathcal{C}$ 分别计算 F1 后取平均，避免头类主导：

$$\mathrm{Macro\text{-}F1} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \frac{2 \sum_{q} \mathbf{1}[c \in P_q \cap G_q]}{\sum_{q} \mathbf{1}[c \in P_q] + \sum_{q} \mathbf{1}[c \in G_q]}$$

**Instance-F1（问题级 F1）**：先计算每道题目的 F1，再对所有题目 $Q$ 取平均：

$$\mathrm{Instance\text{-}F1} = \frac{1}{|Q|} \sum_{q \in Q} \frac{2 |P_q \cap G_q|}{|P_q| + |G_q|}$$

**Micro-F1（全局 F1）**：将所有题目的预测和真值汇总后计算单一 F1 值：

$$\mathrm{Micro\text{-}F1} = \frac{2 \sum_{q} |P_q \cap G_q|}{\sum_{q} |P_q| + \sum_{q} |G_q|}$$

**Exact Match Accuracy（精确匹配准确率）**：预测集合与真值集合完全一致的题目比例：

$$\mathrm{EM} = \frac{1}{|Q|} \sum_{q \in Q} \mathbf{1}[P_q = G_q]$$

此外还报告 **Avg. Precision** 和 **Avg. Recall**，分别为测试集上精确率和召回率的均值。

### 3.5 模型适配策略

- **VLM**：直接输入题目文本与格式指令，利用其生成能力输出选项。
- **HOI 专用方法**：采用 **Top-5 匹配策略**——对每个问题取置信度前 5 的预测，检查是否与给定选项匹配。消融实验（Table 10-11）证实 Top-5 在召回率与精确率之间达到最佳平衡，优于置信度阈值过滤或 Top-3/Top-10。

### 补充图表

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/001_Figure_1.jpg]]
*Figure 1: (a) Existing HOI benchmarks (e.g., HICO-DET) rely on exact-match evaluation under incomplete annotations, penalizing valid yet unlabeled interactions (b) Our multi-choice benchmark accepts multiple correct answers and avoids false negatives and enabling unified evaluation of HOI-specific methods and VLMs. (c) Comparison of state-of-the-art (InternVL3 [85], Qwen2.5-VL-32B [3]) and HOI-specific methods (ADA-CM [37], CMMP [40], HOLa [36]). Results are shown using Macro-F1 in our benchmark (Setting 1) versus mean Average Precision (mAP) in HICO-DET*



## 实验与关键发现

### 实验设置与评估协议

CrossHOI-Bench 将 HOI 检测重新定义为**多答案多项选择题**（multiple-answer, multiple-choice QA），每道题包含四个候选选项，其中可同时有多个正确选项。评估采用集合匹配指标，直接比较预测标签集与真实标签集：

- **Macro-F1**：类平衡 F1，对所有 HOI 类别分别计算 F1 后取平均，避免头类主导评估。
- **Instance-F1**：问题级 F1，先计算每道题目的 F1 再取平均。
- **Micro-F1**：全局 F1，将所有题目的预测和真值汇总后计算单一 F1 值。
- **Exact Match Accuracy (EM)**：预测集合与真值集合完全一致的题目比例。

对于通用 VLM，论文将每道题以提示形式输入，附带明确的答案格式指令；对于 HOI 专用方法，采用 Top-5 匹配策略——取每道题置信度最高的 5 个预测，检查是否与提供的选项匹配，与标准 Top-5 评估协议一致。

实验分为三种递进式评估设置（见 Figure 3）：
- **Setting 1**：完整 HOI 检测流水线，需要同时定位人-物对并识别交互类别。
- **Setting 2**：提供 ground-truth 人框，仅需局部化 HOI 识别，用于分离定位误差。
- **Setting 3**：图像级多人物 HOI 识别，不提供任何定位信息，评估整体交互理解能力。

### 主实验结果

#### Setting 1：完整 HOI 检测

Table 1 展示了 Setting 1 下的完整结果。核心发现如下：

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/004_Table_1.jpg]]
*Table 1: Setting 1 experiment results comparison. Results are grouped by VLM and HOI-specific methods. Best performance within each group is highlighted in bold. “Avg. Prec.” and “Avg. Rec.” denote the precision and recall averaged across the test set, respectively*

**大模型 VLM 在零样本条件下超越最优 HOI 专用方法。** Qwen2.5-VL-32B 以 50.71 Macro-F1 领先所有模型，比 HOI 专用方法中最优的 CMD-SE（47.49 Macro-F1）高出 **+3.22 个百分点**。在 Instance-F1 上，Qwen2.5-VL-32B 达到 52.76，比 HOI 专用方法中最优的 ADA-CM（47.58）高出 **+5.18 个百分点**。这表明大规模 VLM 在零样本条件下已经具备超越专门训练 HOI 模型的交互理解能力。

**小型 VLM 在需要检测时性能急剧下降。** 以 InternVL3-8B 为例，其 Macro-F1 仅 28.63，远低于 HOI 专用方法。从 Setting 2（给定框识别）到 Setting 1（需自行检测）的性能落差表明，**定位仍是 VLM 的主要瓶颈**——小型 VLM 的检测能力尤其薄弱，而大型 VLM 虽有所改善，但检测误差依然是其与 HOI 专用方法差距的主要来源。

**精确率与召回率的非对称性。** 所有 VLM 的 Avg. Precision 普遍高于 Avg. Recall，小型 VLM 的召回率低约 30 个百分点。这说明 VLM 倾向于保守预测，在多动作同时发生时仅预测最显著动作，遗漏大量真实交互。

#### Setting 2：局部化识别（分离定位误差）

Table 2 的结果进一步确认了上述诊断。当提供 ground-truth 人框后，VLM 的性能普遍提升：Qwen2.5-VL-32B 的 Macro-F1 达到 55.42，比最优替代 VLM InternVL3-38B（51.46）高出 **+3.96 个百分点**。但即便消除了定位误差，VLM 的召回率依然显著低于精确率，说明**多动作遗漏**是独立于定位的另一核心失败模式。

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/007_Table_2.jpg]]
*Table 2: Setting 2 experiment results comparison. Best performance within each group is highlighted in bold. “Avg. Prec.” and “Avg. Rec.” denote the precision and recall averaged across the test set, respectively*

#### Setting 3：图像级多人物识别

Table 3 展示了最极端的评估条件——不提供任何定位信息，模型需从整张图像中识别所有人物-物体的交互。Qwen2.5-VL-32B 的 Macro-F1 达到 57.59，比 CMD-SE（40.86）高出 **+16.73 个百分点**。这一巨大差距揭示了两类方法的本质差异：VLM 擅长全局场景理解和交互推理，而 HOI 专用方法严重依赖精确的定位先验，在缺乏定位线索时性能崩溃。

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/008_Table_3.jpg]]
*Table 3: Setting 3 experiment results comparison. Results are reported for VLMs and HOI-specific methods. Best performance within each group is highlighted in bold. “Avg. Prec.” and “Avg. Rec.” denote the precision and recall averaged across the test set, respectively*

值得注意的是，从 Setting 2 到 Setting 3，VLM 的 EM 准确率下降了 5-10 个百分点，主要源于**跨人物交互误分配**——在多人场景中，约 20-25% 的 VLM 预测错误是将周围人的动作错误分配给目标人物（HOI 方法该比例为约 15%）。

### 基准难度验证

Figure 6 对比了 CrossHOI-Bench 与完整 HICO-DET 测试集在 Setting 1 和 2 上的结果。所有模型在 CrossHOI-Bench 上的性能均显著低于在完整 HICO-DET 上的表现，验证了本基准通过移除简单场景、重分配测试分布（KL 散度从 0.088 增至 0.629）和引入困难负例，确实大幅提升了评估难度。这解释了为何 HICO-DET 上 HOI 方法 mAP 不足 50%、VLM 仅约 15%——不完全标注和简单场景主导掩盖了真实能力差距。

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/011_Figure_6.jpg]]
*Figure 6: Experiment result comparison between our CrossHOI-Bench and full HICO-DET based dataset in Setting 1 and 2. “InternVL” refers to InternVL3 and “Qwen” refers to “Qwen2.5-VL”*

### 失败模式分析

Figure 4 展示了 Qwen2.5-VL-32B 在 Setting 1 中的典型失败案例，可归纳为三类核心失败模式：

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/005_Figure_4.jpg]]
*Figure 4: Illustration of VLM (Qwen2.5-VL-32B) failure cases in Setting 1, and red HOI classes refer to missing ground-truth interactions or incorrect predictions*

1. **多动作遗漏**：当同一人-物对同时发生多个交互（如同时“持”和“看”手机），VLM 倾向于仅预测最显著动作，导致召回率低下。这是 VLM 与 HOI 专用方法差距最大的维度——HOI 方法的多动作识别能力明显更优。

2. **跨人物交互误分配**：在多人场景中，VLM 常将周围人的动作错误归因于目标人物。定量分析显示，VLM 约 20-25% 的错误属于此类，而 HOI 方法该比例为 15%。这表明 VLM 缺乏精细的个体级别空间归因机制。

3. **细粒度相似动作混淆**：对于视觉相似的 HOI 类别（如 cut vs. peel），VLM 的混淆率高达 59%，HOI 专用方法也达 52%。两者在此类细粒度区分上均未解决，说明这是当前 HOI 理解的共性瓶颈。

### 消融实验

**Top-K 选择策略。** Table 10 和 Table 11 对比了置信度阈值过滤与 Top-K 预测选择。结果表明，Top-5 选择在召回率与精确率之间实现了最佳平衡——Top-3 召回不足，Top-10 精确率下降明显。

**粗筛选管线消融。** Table 12 显示，在基准构建的粗筛选阶段移除 Qwen2.5-VL-32B 后，基准难度略有下降（Macro-F1 上升约 2%），验证了该步骤对生成有效困难负例的关键贡献。

### 公平性保障

论文通过多项设计确保评估公平性：
- **选项顺序随机化**：每道题的选项顺序随机排列，且真实答案位置分布近似均匀，模型预测分布与之一致（Table 6），排除了 LLM 的位置偏差。
- **负例客观性验证**：粗筛选使用的 VLM 并无偏袒——HOI 专用模型对自动筛选负例的认可度（约 99%）甚至高于 VLM（95-97%），保证了负例质量对不同范式的模型同样公平（Table 4）。
- **统计显著性**：Table 7 报告了基于 1000 次问题级 Bootstrap 重采样的 95% 置信区间，主要结论均具有统计显著性。

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/023_Table_7.jpg]]
*Table 7: Statistical significance analysis. We report 95% bootstrap confidence intervals computed using 1,000 question-level resampling iterations in Setting 1*

### 补充图表

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/009_Figure_5.jpg]]
*Figure 5: Evaluation on our HICO-DET-based, V-COCO-based and SWiG-HOI-based sub-benchmarks in Setting 1 and 2. “InternVL” refers to InternVL3 and “Qwen” refers to “Qwen2.5-VL”*

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/026_Table_10.jpg]]
*Table 10: Comparison between Top-K selection and confidencethreshold filtering for HOI-specific models under Setting 1 (Instance-F1)*

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/027_Table_11.jpg]]
*Table 11: Effect of different Top-K values for HOI prediction selection under Setting 1*

![[assets/figures/papers/paper_list_l2206_https_arxiv_org_abs_2508_18753/figures/028_Table_12.jpg]]
*Table 12: Ablation study on the effect of using Qwen2.5-VL-32B in the coarse screening during dataset construction. The experiment is conducted in a 12% random subset. “w/o Qwen2.5-VL-32B” means that Qwen is not used for screening; “w/ Qwen2.5- VL-32B’ means that Qwen is used for screening*



## 定位与知识库关联

### 1. 任务重定义：从精确匹配检测到多答案选择题

CrossHOI-Bench 的核心贡献不在于提出新的 HOI 检测模型，而在于对评估协议的根本性重构。传统 HOI 基准（以 HICO-DET 为代表）将任务定义为**精确匹配检测**：模型需输出 `<human, object, interaction>` 三元组，且仅当预测与标注完全一致时才算正确。这一范式存在两个结构性缺陷：

- **不完全标注问题**：受限于视觉信息模糊（如 mid-motion 动作）和稀疏标注，大量客观上合理的交互未被标注。在此框架下，VLM 的灵活输出（如生成 "holding" 而标注仅有 "inspect"）被错误惩罚为假阳性，导致其 mAP 骤降至约 15%，而 HOI 专用方法也不足 50%（Figure 1(c)）。
- **跨范式不可比**：VLM 本质上是生成式模型，其输出空间是开放的自然语言；HOI 专用方法则输出固定类别的概率分布。精确匹配评估无法在同一尺度下公平比较二者。

CrossHOI-Bench 将 HOI 检测**重定义为多答案多项选择题（MCQA）**：每道题目针对一个人-物对，提供四个候选交互选项，其中可包含多个正确答案。这一设计的关键洞察在于：**MCQA 格式既保留了 VLM 的自由文本生成特性（通过指令跟随输出选项），又通过固定选项提供了可控的评估空间**，使得跨范式评估成为可能。同时，每道题目的正负例集合是显式定义的——正例来自人工标注，负例通过 VLM 粗筛 + 人工精炼生成——从而从根本上消除了不完全标注带来的误判。

### 2. 与现有基准的关系与差异

CrossHOI-Bench 并非完全从零构建，而是对 HICO-DET 测试集的**选择性重构与难度重分布**。其与现有基准的关键差异体现在：

| 维度 | HICO-DET / V-COCO | CrossHOI-Bench |
|------|-------------------|----------------|
| 任务形式 | 精确匹配检测 | 多答案多项选择 QA |
| 负例定义 | 无明确负例（未标注即错误） | 显式负例集合（VLM 粗筛 + 人工精炼） |
| 评估指标 | mAP | Macro-F1, Instance-F1, Micro-F1, EM |
| 数据分布 | 训练/测试分布高度相似（KL=0.088），头类主导 | 移除简单场景，重分配分布（KL=0.629） |
| 跨范式评估 | 不支持 | 统一 VLM 与 HOI 专用方法 |

具体而言，基准构建流程（Figure 3）包含两个关键阶段：

1. **粗筛选（Coarse Screening）**：利用多阶段 VLM 管线（GPT-4.1 → Qwen2.5-VL-32B + GPT-4o）自动生成候选负例。消融实验表明，移除 Qwen2.5-VL-32B 后基准难度略有下降（Macro-F1 上升约 2%），验证了该步骤对生成有效负例的贡献（Table 12）。
2. **人工精炼（Manual Refinement）**：剔除过于简单的场景（如单人-简单背景下视觉明显的动作），校正自动筛选错误，并补充困难正例与负例。

最终主基准包含 1,274 张图像，覆盖 600 个 HOI 类别，总计 3,773 道选择题。此外，论文还构建了基于 V-COCO 和 SWiG-HOI 的子基准，以验证评估框架的泛化性（Figure 5）。

### 3. 与 HOI 专用方法的定位关系

CrossHOI-Bench 评估了多种代表性 HOI 专用方法，包括两阶段方法 **ADA-CM**、**LAIN**、**HOLa** 和单阶段方法 **CMMP**、**CMD-SE**。这些方法在 HICO-DET 上已接近性能饱和，但 CrossHOI-Bench 揭示了其隐藏的短板：

- **分布外泛化能力弱**：在 Setting 3（图像级多人物识别）中，最优 HOI 方法 CMD-SE 的 Macro-F1 仅为 33.78，而零样本 VLM Qwen2.5-VL-32B 达到 50.51（差距 +16.73%，Table 3）。这表明 HOI 专用方法高度依赖 HICO-DET 的训练分布，面对重分布的困难场景时泛化能力显著不足。
- **细粒度相似动作混淆**：在相似动作对（如 cut vs. peel）上，HOI 方法的混淆率仍高达 52%，VLM 为 59%，两者均未解决这一难题。
- **多动作识别相对优势**：HOI 方法在多动作同时发生的场景下召回率优于小型 VLM，说明其结构化的多标签输出设计仍有价值。

### 4. 与通用 VLM 的定位关系

论文评估了多款主流 VLM 的零样本表现，包括 **Qwen2-VL / Qwen2.5-VL / Qwen3-VL** 系列、**InternVL2.5 / InternVL3** 系列和 **LLaVA-OV**。关键发现是：

- **大模型 VLM 在交互理解上超越 HOI 专用方法**：Qwen2.5-VL-32B 在 Setting 1 的 Macro-F1 达到 50.71，超越最优 HOI 方法 CMD-SE（47.49），Instance-F1 优势更达 +5.18%（Table 1）。这暗示大规模预训练赋予了 VLM 更强的视觉语义理解和跨模态推理能力。
- **定位仍是 VLM 的主要瓶颈**：从 Setting 2（提供 ground-truth 人框）到 Setting 1（需自行检测），VLM 性能明显下降，说明其目标检测能力远弱于专用检测器。
- **多人物场景下的交互误分配严重**：约 20-25% 的 VLM 预测错误源于将周围人的动作错误分配给目标人物，而 HOI 方法该比例为 15%。这反映了 VLM 缺乏显式的个体级别空间注意力机制。

### 5. 适用边界与局限

尽管 CrossHOI-Bench 在评估公平性和难度设计上取得了重要进展，其适用边界和局限同样明确：

- **规模限制**：主基准仅 1,274 张图像，虽覆盖 600 个类别，但每类样本量有限，可能无法充分代表长尾类别和行为。
- **提示敏感性未充分消融**：VLM 的零样本结果高度依赖指令跟随格式和提示设计，论文未彻底消融提示工程的影响，不同提示策略可能导致结论波动。
- **静态图像局限**：基准聚焦于单帧静态图像，无法评估模型对交互随时间演化的理解能力。在长视频 HOI 理解场景中，MCQA 格式是否仍然适用尚待验证。
- **负例质量的 VLM 依赖性**：粗筛选管线本身依赖 VLM，尽管公平性验证表明 HOI 方法对自动筛选负例的认可度（~99%）甚至高于 VLM（95-97%，Table 4），但负例空间仍受限于筛选模型的认知边界。

### 6. 开放问题与后续方向

基于上述分析，以下几个方向值得后续工作关注：

1. **VLM 交互理解优势的归因**：VLM 在交互推理上超越专门训练的 HOI 方法，究竟得益于更广泛的预训练数据分布、更大的模型容量，还是其生成式特性带来的灵活语义组合能力？这需要控制变量的对比实验来分离各因素贡献。

2. **多人物交互误分配的缓解**：能否为 VLM 引入显式的空间注意力机制或个体级别表示，以降低跨人物交互误分配率？将 HOI 方法的结构先验（如空间拓扑保留、图神经网络建模）与 VLM 的语义理解能力结合，可能是一个有前景的方向。

3. **MCQA 格式的时空扩展**：在视频 HOI 理解中，交互的定义涉及时间维度的起止边界和动作演化。如何将多答案选择题格式扩展到时间维度，同时保持评估的可控性和公平性，是一个非平凡的设计挑战。

4. **更大规模、更细粒度的基准构建**：当前基准的规模和类别覆盖仍有扩展空间。结合自动标注管线与人工验证，构建覆盖更多长尾交互类型、更细粒度动作区分的大规模 MCQA 基准，将有助于推动领域进一步发展。



## 原文 PDF

![[paperPDFs/CVPR_2026/CrossHOI_Bench_A_Unified_Benchmark_for_HOI_Evaluation_across_Vision_Language_Models_and_HOI_Specific_Methods.pdf]]
