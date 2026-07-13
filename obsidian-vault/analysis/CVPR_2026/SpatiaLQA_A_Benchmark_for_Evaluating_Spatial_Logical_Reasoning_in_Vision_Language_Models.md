---
title: "SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpatiaLQA_A_Benchmark_for_Evaluating_Spatial_Logical_Reasoning_in_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/xieyc99/SpatiaLQA"
aliases:
- RSGARR
- SpatiaLQA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过递归场景图辅助推理（RSGAR），利用视觉基础模型提供深度和分割先验，并迭代地构建任务相关的空间关系图，为VLM注入结构化的空间信息，从而改善多步推理的准确性。
primary_logic: 将场景分解为以任务对象为中心的递归场景图，能够显式地捕捉对象间的直接接触与空间依赖关系，使VLM从原始图像中抽象出关键空间结构，进而更好地规划具有先后顺序的操作步骤。
claims:
- 即使最先进的VLM在SpatiaLQA上仍表现不佳，前提条件F1显著低于内容F1。
- RSGAR（T=5）在SpatiaLQA上取得最佳F_c=69.8、F_p=28.1，显著优于原始推理（F_c=67.4, F_p=25.1）。
- 递归迭代次数T增加时性能持续提升，且移除深度图或分割图会导致性能下降。
- VLMs倾向于输出较少步骤（平均3.1步 vs 标注4.2步），表明模型在不确定性步骤上选择跳过。
---

# SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models

> [!tip] 核心洞察
> 将场景分解为以任务对象为中心的递归场景图，能够显式地捕捉对象间的直接接触与空间依赖关系，使VLM从原始图像中抽象出关键空间结构，进而更好地规划具有先后顺序的操作步骤。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpatiaLQA：面向视觉语言模型空间逻辑推理能力的基准评测 |
| 英文题名 | SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.20901) · [Code](https://github.com/xieyc99/SpatiaLQA) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Recursive Scene Graph Assisted Reasoning (RSGAR) |
| Dataset | SpatiaLQA |

> [!tip] 效果简介
> - SpatiaLQA 上，F_c (内容F1) 69.8 vs 67.4 (+2.4)；F_p (前提条件F1) 28.1 vs 25.1 (+3.0)。

## 概要

**问题瓶颈**：视觉语言模型（VLM）在整合空间理解与多步逻辑推理方面存在显著不足。与传统的视觉问答（VQA）或抽象符号逻辑推理不同，空间逻辑推理要求模型同时从真实场景中感知物体的空间关系，并据此规划具有先后依赖的多步操作序列。当前最先进的VLM在前提条件（precondition）推理上的能力远低于内容（content）推理，导致在复杂真实场景中难以生成逻辑一致且空间合理的操作步骤。

**核心洞察**：将场景分解为以任务对象为中心的递归场景图，能够显式地捕捉对象间的直接接触与空间依赖关系，使VLM从原始图像中抽象出关键空间结构，进而更好地规划具有先后顺序的操作步骤。

**方法定位**：本文提出**递归场景图辅助推理（Recursive Scene Graph Assisted Reasoning, RSGAR）**，利用视觉基础模型（Depth Anything V2 与 SAM）提取深度和分割先验，并迭代地构建任务相关的空间关系图，为VLM注入结构化的空间信息，从而改善多步推理的准确性。该方法属于“感知增强+结构化中间表示”的技术路线，区别于单纯的思维链（CoT）或端到端推理。

**主要结果**：
- 在 SpatiaLQA 基准上，RSGAR（T=5）取得内容F1 $F_c=69.8$、前提条件F1 $F_p=28.1$，较原始推理（$F_c=67.4$, $F_p=25.1$）有显著提升。
- 即使最先进的VLM（如GPT-4.1）在 SpatiaLQA 上仍表现不佳，前提条件F1（$F_p=38.0$）远低于人类水平（$F_p=92.5$），表明空间逻辑推理仍是开放挑战。
- 消融实验证实：递归迭代次数增加带来持续性能增益，移除深度图或分割图均导致性能下降，验证了结构化空间先验的必要性。

### 视觉语言模型的空间推理困境

视觉语言模型（VLM）在常规视觉问答（VQA）和抽象符号逻辑推理上已取得显著进展，然而当任务要求同时整合**空间理解**与**多步逻辑推理**时，现有模型暴露出系统性不足。如Figure 1所示，常规VQA侧重于识别视觉内容和事实知识，常见逻辑推理聚焦于抽象符号问题求解，而空间逻辑推理则要求模型在真实场景中理解物体间的空间关系，并据此规划具有先后依赖的操作步骤——这正是当前VLM的核心瓶颈。

### 现有基准的缺口

当前评估VLM的基准主要分为两类：一类关注视觉内容识别（如VQA v2），另一类测试抽象逻辑推理（如LogiQA）。然而，这两类基准均未触及空间理解与逻辑推理的交叉地带。Table 1将SpatiaLQA与现有基准进行了系统对比，揭示了关键缺口：现有基准要么缺乏空间理解维度，要么不涉及多步推理，且无一标注步骤间的前提条件（precondition）——即哪些步骤必须先于其他步骤完成。这一缺失使得我们无法有效评估模型在真实场景中“先做什么、后做什么”的空间逻辑规划能力。

### 前提条件推理：被忽视的关键能力

多步操作序列的正确性不仅取决于步骤内容本身，更依赖于步骤间的**前提条件关系**。例如，“将杯子放入橱柜”的前提是“橱柜门已打开”，而“打开橱柜门”又可能依赖于“移开挡在橱柜前的椅子”。这种链式空间依赖要求模型具备递归式的空间推理能力。然而，实验表明（Table 2），即使是最先进的VLM（如GPT-4.1），其内容F1（$F_c$）可达73.5，但前提条件F1（$F_p$）仅为38.0，而人类在$F_p$上可达92.5。这一巨大差距表明，前提条件推理是当前VLM的致命短板，也是空间逻辑推理任务的核心挑战。

### 本文动机与贡献

针对上述缺口，本文提出**SpatiaLQA基准**——首个专门评估VLM空间逻辑推理能力的基准，包含来自241个真实室内场景的9,605个问答对，每个答案由多步操作序列构成，并显式标注了步骤间的前提条件。在此基础上，本文进一步提出**递归场景图辅助推理（RSGAR）**方法，利用视觉基础模型（Depth Anything V2和SAM）提取深度与分割先验，通过迭代构建任务相关的场景图，为VLM注入结构化的空间信息，从而改善多步空间逻辑推理的准确性。

## 核心方法与创新机理

SpatiaLQA 的核心创新并非提出一个新的模型架构，而是**定义了一个被现有 VLM 普遍忽视的能力维度——空间逻辑推理**，并针对该瓶颈设计了一种**结构化先验注入的推理框架 RSGAR**。其创新点可从问题定义、方法机制和评估范式三个层面理解。

### 1. 问题定义的创新：从“看见”到“空间逻辑推理”

现有 VLM 基准（如 VQA、逻辑推理）通常将视觉理解与逻辑推理分离：VQA 关注内容识别，逻辑推理关注抽象符号操作（见 Figure 1）。SpatiaLQA 将二者耦合，要求模型在真实室内场景中完成**多步操作序列的生成**，且每一步必须同时满足**内容正确性**（$F_c$）与**前提条件合理性**（$F_p$）。

这一设定暴露了 VLM 的关键短板：**前提条件推理远弱于内容推理**。以 GPT-4.1 为例，$F_c=73.5$ 但 $F_p=38.0$，而人类 $F_p=92.5$（Table 2）。这种不对称性表明，模型能“知道要做什么”，但难以“判断何时能做”，这正是空间逻辑推理的核心瓶颈。

### 2. 方法机制的创新：递归场景图辅助推理（RSGAR）

RSGAR 的核心思想是**将隐式的空间关系显式化为任务相关的递归场景图**，为 VLM 提供结构化的空间先验。相比直接端到端推理（Vanilla Reasoning），RSGAR 在三个关键环节引入了变化：

| 变更维度 | Baseline（Vanilla Reasoning） | RSGAR | 作用机制 |
|---------|------------------------------|-------|---------|
| **感知输入** | 仅原始 RGB 图像 | RGB + 深度图（Depth Anything V2）+ 分割图（SAM） | 注入几何与语义先验，帮助 VLM 感知物体边界和空间距离 |
| **推理中间表示** | 无结构化中间表示 | 以任务对象为起点的递归场景图（节点=物体，边=空间关系） | 将复杂的场景空间关系压缩为任务相关的图结构，降低推理负担 |
| **推理流程** | 单步端到端推理 | 递归图生成（最多 T 轮）→ 图+提示联合推理 | 将空间理解与逻辑推理解耦，先“理解场景结构”再“规划步骤序列” |

**递归场景图生成**是 RSGAR 最关键的创新机制。它以任务指定的对象为初始源节点，迭代地识别与之直接接触的目标对象及其空间关系，逐步扩展场景图。这一设计模拟了人类解决空间任务时的认知过程：从操作目标出发，逐层追溯依赖关系。消融实验证实，递归次数 $T$ 从 1 增至 7 时，$F_c$ 从 68.5 提升至 70.6，$F_p$ 从 27.3 提升至 28.6（Table 5a），验证了迭代深化的有效性。

### 3. 评估范式的创新：步骤级前提条件匹配

传统 VQA 评估仅关注答案的最终正确性，而 SpatiaLQA 引入了**步骤级的内容与前提条件双重匹配**。评估流程（Figure 5）首先用 GPT-4o 对预测步骤与标注步骤进行语义匹配，再通过匈牙利算法求得最优一对一映射，最终计算 $F_c$ 和 $F_p$。这一设计的独特性在于：

- **细粒度诊断**：$F_c$ 与 $F_p$ 的分离使研究者能定位模型失败的具体环节——是步骤内容错误，还是步骤顺序/前提条件错误。
- **可扩展的自动评估**：GPT-4o 评分与人工评估的 Pearson 相关系数高达 0.99（Table 3），保证了大规模评估的可行性。

### 4. 创新边界与局限

RSGAR 的创新在于**推理范式的改进**而非模型架构的革新。其性能增益依赖于视觉基础模型（Depth Anything V2、SAM）提供的先验质量，以及 VLM 自身的场景图生成能力。递归机制虽然有效，但带来了显著的计算开销（$T=5$ 时单次验证耗时 174.5 小时，Table A1），且 $F_p$ 的绝对水平（28.1）仍远低于人类（92.5），表明前提条件推理仍是开放难题。

SpatiaLQA 工作提出了 **递归场景图辅助推理（Recursive Scene Graph Assisted Reasoning, RSGAR）**，其核心设计动机源于一个关键瓶颈：当前视觉语言模型（VLM）在整合空间理解与多步逻辑推理时存在显著断裂，尤其对操作步骤间的前提条件（precondition）推理能力远弱于内容（content）推理。RSGAR 通过引入结构化的空间中间表示，将复杂的真实场景逐步分解为任务相关的场景图，从而为 VLM 注入显式的几何与语义先验，改善多步推理的准确性与逻辑一致性。

### 整体流程

RSGAR 的整体 pipeline 由三个串行模块构成，形成“视觉先验提取 → 递归场景图生成 → 场景图辅助推理”的级联结构，如 Figure 8 所示。整个流程中，场景图生成与最终问答由**同一个 VLM** 完成，保证了表征空间的一致性。

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/012_Figure_8.jpg]]
*Figure 8: The overview of RSGAR. Scene graph generation and question answering are performed by the same VLM*

#### 模块一：视觉先验提取模块

给定输入场景图像与任务描述，首先调用两个视觉基础模型提取几何与语义先验：

- **深度图**：使用 **Depth Anything V2** 生成场景的密集深度估计，提供物体间的相对距离与遮挡线索。
- **分割图**：使用 **SAM** 生成实例级或语义级分割掩码，明确物体边界与类别归属。

这两类先验信息以可视化叠加或文本描述的形式，作为后续场景图生成的辅助输入。消融实验（Table 5b）证实，同时移除深度图和分割图会导致内容 F1 下降 3.3 个百分点，说明几何与语义先验对空间关系推理具有不可替代的作用。

#### 模块二：递归场景图生成模块

这是 RSGAR 的核心创新。该模块以**任务指定的对象**作为初始源节点，执行多轮迭代的场景图构建：

1. **首轮生成**：将初始源对象、深度图、分割图及场景图像输入 VLM，要求 VLM 识别与该源对象**直接接触**的所有目标对象，并描述两者之间的空间关系（如“A 在 B 上方”“C 紧贴 D 左侧”）。
2. **图构建**：将本轮识别出的源对象与目标对象作为节点，空间关系作为有向边，构建当前轮次的局部场景图。
3. **递归扩展**：将本轮新发现的目标对象作为下一轮的源对象，重复上述过程，直至达到预设的最大迭代次数 $T$ 或无新的直接接触对象被发现。

这一递归机制的关键在于：它模拟了人类在规划多步操作时的“顺藤摸瓜”式空间推理——从一个关键对象出发，逐步追溯其空间依赖链，而非一次性理解全局场景。Table 5a 的消融表明，当 $T$ 从 1 增至 7 时，内容 F1 从 68.5 持续提升至 70.6，前提条件 F1 亦有同步增益，验证了递归深度对推理质量的累积贡献。

#### 模块三：场景图辅助推理模块

将经过 $T$ 轮迭代生成的完整场景图（包含所有已发现的对象节点与空间关系边）与原始任务提示**拼接**，共同输入 VLM，由 VLM 生成最终的多步操作序列答案。此时 VLM 无需从原始像素中隐式推断空间结构，而是可以直接在结构化场景图上进行逻辑规划，从而降低推理难度。

### 输入输出规范

- **输入**：一张真实室内场景的 RGB 图像 + 一条自然语言任务指令（如“请将书架上的书移到书桌上”）。
- **中间产物**：深度图、分割图，以及由 VLM 迭代生成的、以任务对象为根的任务相关场景图。
- **输出**：一个有序的多步操作序列，每个步骤包含**内容**（执行什么动作）与隐式的**前提条件**（该步骤执行前必须完成的先行步骤）。

### 与基线方法的差异

相较于直接使用 VLM 进行端到端推理的 **Vanilla Reasoning**，RSGAR 在三个关键维度上进行了结构性改造：

| 维度 | Vanilla Reasoning | RSGAR |
|------|-------------------|-------|
| 感知输入 | 仅原始 RGB 图像 | RGB + 深度图 + 分割图 |
| 推理中间表示 | 无结构化表示 | 递归生成的任务相关场景图 |
| 推理流程 | 单步端到端 | 多轮递归场景图生成后辅助推理 |

此外，与简单地在输入中拼接深度图或分割图的变体（如 `+ depth`、`+ seg`、`+ depth&seg`）相比，RSGAR 的增益并非仅来自多模态信息的堆叠，而是源于**递归场景图这一结构化中间表示**对空间依赖关系的显式建模。Table 4a 显示，RSGAR（$T=5$）的内容 F1 达到 69.8，前提条件 F1 达到 28.1，均显著优于所有非递归基线。

### 效率与局限

递归机制带来了可观的性能提升，但也引入了显著的计算开销。Table A1 显示，RSGAR 在 $T=5$ 时完成 SpatiaLQA 全量验证需 174.5 小时，远超 Vanilla Reasoning 的推理时间。这一效率瓶颈限制了其在实时场景中的直接部署，如何在保持递归推理优势的同时降低计算成本，是后续研究需要解决的关键问题。

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/005_Figure_4.jpg]]
*Figure 4: The data collection pipeline for SpatiaLQA. Note that although the graph expansion augmentation in the figure is applied only to the data from subgraph extraction augmentation, we actually also applied graph expansion augmentation to the manually annotated data*

### 3.1 评估指标公式体系

SpatiaLQA 的核心评估围绕“内容（content）”与“前提条件（precondition）”两个维度展开，分别衡量模型对操作步骤本身及其执行顺序依赖的预测质量。指标体系由以下六个公式构成：

**内容召回率** $R_c$ 衡量预测步骤内容与标注步骤内容匹配的召回率，反映模型对必要操作步骤的覆盖程度。

**内容精确率** $P_c$ 衡量预测步骤内容与标注步骤内容匹配的精确率，反映模型生成步骤的准确性。

**前提条件召回率** $R_p$ 衡量预测的前提条件与标注前提条件匹配的召回率，反映模型对步骤间依赖关系的识别覆盖度。

**前提条件精确率** $P_p$ 衡量预测的前提条件与标注前提条件匹配的精确率，反映模型对依赖关系判断的准确性。

**内容 F1** $F_c$ 综合 $R_c$ 与 $P_c$，是内容维度预测质量的综合指标。

**前提条件 F1** $F_p$ 综合 $R_p$ 与 $P_p$，是前提条件推理质量的综合指标。

上述指标的计算依赖于 GPT-4o 与匈牙利算法的两步匹配流程（见 Figure 5）：首先由 GPT-4o 基于图像对预测步骤与标注步骤进行逐对匹配，生成匹配矩阵；随后通过匈牙利算法滤除冗余匹配，得到最大一对一匹配结果。该评估流程与人工评估的 Pearson 相关系数高达 $\rho = 0.99$（Table 3），验证了其可靠性。

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/007_Figure_5.jpg]]
*Figure 5: The matching process between the predicted and annotated steps. We first use GPT-4o to match the predicted steps and annotated steps in pairs based on the image (allowing one-to-many matches), resulting in a matching matrix. Then, we apply the Hungarian algorithm to filter the matching matrix, removing redundant matches to achieve the maximum one-to-one matches*

### 3.2 RSGAR 方法核心模块

Recursive Scene Graph Assisted Reasoning（RSGAR）通过三个级联模块为 VLM 注入结构化的空间理解，其整体架构见 Figure 8。

**模块一：视觉先验提取模块**

该模块利用两个视觉基础模型为场景提供几何与语义先验：
- **Depth Anything V2** 生成深度图，提供对象间的相对距离与空间层次信息。
- **SAM** 生成分割图，提供对象的边界与语义区域信息。
两种先验以视觉标注的形式叠加到原始 RGB 图像上，共同构成增强后的感知输入。

**模块二：递归场景图生成模块**

这是 RSGAR 的核心创新。该模块以任务指定的对象为初始源节点，迭代执行场景图生成，单轮流程为：
1. 将当前源对象与增强后的场景图像输入 VLM；
2. VLM 识别与源对象直接接触的目标对象，并提取两者间的空间关系（如“A 在 B 上方”“C 紧贴 D 右侧”）；
3. 将识别出的目标对象作为下一轮的源对象，重复上述过程，直至达到预设的最大迭代轮数 $T$。

最终生成的任务相关场景图以对象为节点、空间关系为边，显式编码了场景中与任务相关的接触传递链与空间依赖结构。

**模块三：场景图辅助推理模块**

将递归生成的完整场景图与原始任务提示合并，共同输入 VLM 以产生最终的多步操作序列。场景图作为结构化的中间表示，使 VLM 能够从原始像素中抽象出关键空间约束，从而更好地规划具有先后顺序的操作步骤。

### 3.3 关键消融变量

RSGAR 的性能受两个关键变量调控：

- **递归轮数 $T$**：控制场景图生成的迭代深度。$T$ 越大，场景图覆盖的空间依赖链越长，但计算开销也随之线性增长。消融实验（Table 5a）表明，$T$ 从 1 增至 7 时，$F_c$ 从 68.5 提升至 70.6（+2.1），$F_p$ 同步提升，验证了递归深度对空间逻辑推理的正向作用。
- **深度图与分割图**：移除深度图或分割图均导致性能下降（Table 5b），同时移除两者时 $F_c$ 下降 3.3，表明几何与语义先验对场景图构建质量具有互补且不可替代的贡献。

## 实验与关键发现

### 主要结果：VLM在空间逻辑推理上普遍表现不足

作者在SpatiaLQA上对41个主流VLM进行了全面评估（Table 2），结果显示，即使是最先进的模型在空间逻辑推理任务上仍与人类存在巨大差距。人类评估者在内容F1（$F_c$）上达到97.6，前提条件F1（$F_p$）达到92.5；而表现最好的专有模型GPT-4.1仅取得$F_c=73.5$、$F_p=38.0$。这一对比揭示了核心瓶颈：**前提条件的推理能力远低于内容推理**，即模型能够识别“做什么”，但难以准确判断“在什么条件下做”。

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/006_Table_2.jpg]]
*Table 2: The evaluation results of 41 VLMs. ‘Ins’ indicates that the model is an ‘instruction-tuned’ version. Recall and precision are used as reference metrics and are marked in gray. The best and second-best F1 scores (excluding human results) are marked in red and blue, respectively, and we use a dashed line to separate open-source VLMs (above) and proprietary VLMs (below)*

从模型类别来看，开源VLM与专有VLM之间存在明显的性能鸿沟。专有模型在$F_c$和$F_p$上普遍领先，但即使是GPT-4.1的$F_p$也不及人类的一半。值得注意的是，部分经过指令微调的模型（如Qwen2.5-VL-72B-Instruct）表现优于其基础版本，说明指令微调对空间逻辑推理有一定帮助，但提升幅度有限。

另一个关键发现是，VLM倾向于输出比标注更少的步骤（平均3.1步 vs. 标注4.2步），表明模型在不确定性较高的步骤上选择跳过而非尝试推理，这是一种隐性的失败模式——模型通过降低任务复杂度来规避空间逻辑推理的困难。

**评估可靠性的验证**：作者使用GPT-4o作为评分VLM，并验证了其与人工评估的高度一致性。Table 3显示，GPT-4o在内容F1上的Pearson相关系数达到$\rho_c=0.99$，前提条件F1的相关系数$\rho_p$同样极高，平均绝对误差（MAE）仅约3%。这一结果为后续实验的自动化评估提供了可信基础。

### RSGAR方法的效果与分析

RSGAR（递归场景图辅助推理）在GPT-4o上取得了$F_c=69.8$、$F_p=28.1$的最佳结果（Table 4a），相较于Vanilla Reasoning（$F_c=67.4$, $F_p=25.1$）分别提升了+2.4和+3.0。这一提升虽然绝对值不大，但在该困难任务上具有统计意义。

**按步数分层分析**（Table 4b）揭示了RSGAR的优势场景：在标注步数较多的样本上，RSGAR的提升更为显著。例如，当标注步数为4时，$F_c$提升达+4.5；而当步数为2时，提升仅为+1.2。这表明递归场景图的构建对于需要多步推理的复杂任务尤为有效——场景图显式地捕捉了对象间的空间依赖关系，帮助模型在长程推理中保持逻辑一致性。

与其他方法的对比（Table 4a）显示：
- 直接添加深度图（+ depth）或分割图（+ seg）仅带来微弱提升（$F_c$约+0.5~1.0），说明单纯的视觉先验注入不足以解决空间逻辑推理问题。
- 同时添加深度图和分割图（+ depth&seg）的$F_c=68.5$，接近RSGAR的$F_c=69.8$，但$F_p$仍低于RSGAR（26.8 vs. 28.1），说明结构化的场景图表示对前提条件推理有独特价值。
- PhysAgent和CoT在$F_c$上均低于Vanilla Reasoning，表明通用的物理推理或思维链方法未能有效适配空间逻辑推理任务。

### 消融实验：递归深度与视觉先验的关键作用

**递归次数T的影响**（Table 5a）：随着递归迭代次数T从1增加到7，$F_c$从68.5持续提升至70.6（+2.1），$F_p$从26.8提升至28.1（+1.3）。这一单调递增趋势验证了递归场景图生成的核心假设：更多的迭代轮次使模型能够探索更远的空间依赖关系，构建更完整的任务相关场景图。但边际收益在T≥5后递减，T=5到T=7的$F_c$提升仅+0.8，说明5轮迭代已能覆盖大部分任务所需的空间关系。

**视觉先验的作用**（Table 5b）：移除深度图或分割图均导致性能下降。当同时移除深度图和分割图时，$F_c$从69.8降至66.5（-3.3），$F_p$从28.1降至25.1（-3.0），性能回退到接近Vanilla Reasoning的水平。这证实了深度和分割先验对场景图构建质量的关键支撑——深度图帮助模型判断对象间的相对位置和接触关系，分割图提供精确的对象边界，两者共同减少了场景图生成中的空间歧义。

### 效率与局限

RSGAR的计算开销显著：T=5时完整验证SpatiaLQA需174.5小时（Table A1），远超Vanilla Reasoning的推理时间。这一效率瓶颈源于每轮递归都需要VLM进行场景图生成，且随着T增加，生成的场景图规模扩大，后续推理的上下文长度也随之增长。这限制了RSGAR在实际部署中的可行性，需要在推理效率与性能之间进行权衡。

此外，场景图的准确性完全依赖于VLM的生成质量。当VLM错误识别对象或误判空间关系时，这些错误会通过递归传播并放大，最终影响推理结果。这一失败模式在复杂杂乱场景中尤为突出，需要人工验证具体案例。

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/009_Table_3.jpg]]
*Table 3: Comparison between scoring VLM evaluation results and human evaluation results*

![[assets/figures/papers/paper_list_l2216_https_arxiv_org_abs_2602_20901/figures/002_Table_1.jpg]]
*Table 1: Comparison between SpatiaLQA and other benchmarks (VQA, logical reasoning and EQA). ‘SU’ and ‘LR’ denote spatial understanding and long-range reasoning, respectively. ‘I’, ‘P’ and ‘V’ denote image, point cloud and video, respectively. ‘Open’ and ‘MC’ stand for open-vocabulary and multiple-choice respectively. ‘Multi-step’ specifies whether the answers involve multiple steps. ‘Precondition’ indicates whether each step in the answer is annotated with its preconditions (i.e., which steps must be completed beforehand)*

## 定位与知识库关联

### 任务定位：空间逻辑推理的新基准

SpatiaLQA 将任务锚定在**空间逻辑推理**——要求模型同时整合空间理解与多步逻辑推理，以生成在真实场景中可执行的操作序列。这与传统 VQA（识别视觉内容与事实知识）和抽象逻辑推理（符号化问题求解）形成明确区分（Figure 1）。该基准的独特贡献在于：**首次将前提条件推理纳入评测体系**，即每个操作步骤必须明确其前置依赖步骤，从而检验模型对任务因果结构的理解。

### 方法谱系中的位置

**RSGAR** 的核心思路是将视觉先验（深度图、分割图）与递归场景图生成相结合，为 VLM 注入结构化的空间信息。在方法谱系中，该工作位于以下几条研究脉络的交汇点：

1. **视觉基础模型辅助推理**：利用 Depth Anything V2 和 SAM 提取几何与语义先验，这类“视觉前端 + VLM 后端”的范式与 PhysAgent 等物理推理方法共享相似动机，但 RSGAR 的独特之处在于将先验信息组织为**任务相关的递归场景图**，而非直接拼接入提示。

2. **场景图推理**：与传统的单次场景图生成不同，RSGAR 采用**递归扩展**策略——以任务指定对象为初始源节点，迭代识别直接接触的目标对象及其空间关系，逐步构建覆盖完整操作链的场景图。这一设计使场景图的粒度与任务需求对齐，避免了全图生成带来的冗余。

3. **思维链推理的增强**：相较于标准 CoT 仅依赖文本推理链，RSGAR 通过显式的图结构中间表示，将空间依赖关系从隐式的语言描述中解耦出来，使推理过程更具可解释性和结构化。

### 与基线方法的关系

实验对比了以下基线方法，均以 GPT-4o 为基础 VLM：

- **Vanilla Reasoning**：直接输入图像和任务提示，无额外视觉先验或结构化中间表示（$F_c=67.4$, $F_p=25.1$）。
- **+ depth / + seg / + seg&depth**：在输入中分别或同时加入深度图和分割图，但未构建场景图。这些方法验证了视觉先验的独立贡献。
- **CoT**：标准思维链推理，未利用空间结构化信息。
- **PhysAgent**：基于物理代理的推理方法，代表了另一类物理推理范式。

RSGAR（T=5）在所有方法中取得最佳结果（$F_c=69.8$, $F_p=28.1$），相较于 Vanilla Reasoning 分别提升 +2.4 和 +3.0 个百分点。值得注意的是，前提条件 F1 的提升幅度（+3.0）大于内容 F1（+2.4），表明**递归场景图对因果依赖关系的建模尤为有效**。

### 适用边界与局限

1. **场景域限制**：SpatiaLQA 目前仅覆盖 13 类室内场景（如厨房、卧室、客厅等），未涉及室外或动态环境。RSGAR 依赖的深度和分割模型在室外场景中的泛化能力尚未验证。

2. **推理效率瓶颈**：递归场景图生成显著增加了推理时间。T=5 时单次验证耗时 174.5 小时，远高于 Vanilla Reasoning 和其他高效方法。这一计算开销使其难以直接部署于实时应用场景。

3. **场景图质量依赖**：场景图的准确性完全依赖于 VLM 的生成质量。若 VLM 错误识别对象或空间关系，这些错误会通过递归过程传播并放大，最终损害推理结果。消融实验显示，移除深度图或分割图会导致 $F_c$ 下降 3.3 个百分点，说明视觉先验对场景图质量至关重要。

4. **前提条件推理的固有困难**：即使 RSGAR 显著改善了前提条件 F1，其绝对值（$F_p=28.1$）仍远低于人类水平（$F_p=92.5$）。这表明当前方法对“哪一步必须先完成”这类因果判断的理解仍然薄弱，是空间逻辑推理的核心瓶颈。

5. **评估偏差**：评估过程依赖 GPT-4o 进行步骤匹配，尽管与人工评估的 Pearson 相关系数高达 0.99，但平均绝对误差约为 3%，在精细比较时需谨慎对待。

### 开放问题

1. **效率优化**：如何降低递归场景图生成的计算开销？可能的路径包括缓存复用、早期终止策略，或使用轻量级图生成模型替代 VLM 进行场景图构建。

2. **跨域泛化**：RSGAR 框架能否推广至具身任务（如机器人导航、物体操作）或视频/3D 点云数据中的动态空间逻辑推理？这需要验证视觉先验模块和场景图生成策略在更复杂环境中的鲁棒性。

3. **前提条件推理的突破**：当前 $F_p$ 远低于 $F_c$，说明“做什么”和“何时做”之间存在能力鸿沟。是否需要专门的训练策略（如对比学习、图神经网络监督）或模型架构改进（如显式建模时序依赖）来大幅提升前提条件推理？

4. **开放词汇场景的鲁棒性**：在包含未见过的物体类别或复杂空间布局的场景中，如何保证场景图构建的准确性和完整性？这可能需要在视觉基础模型中引入更强的开放词汇能力。

5. **基准扩展**：SpatiaLQA 目前为静态图像基准，未来能否扩展到视频或交互式环境，以评估模型在动态变化场景中的空间逻辑推理能力？

## 原文 PDF

![[paperPDFs/CVPR_2026/SpatiaLQA_A_Benchmark_for_Evaluating_Spatial_Logical_Reasoning_in_Vision_Language_Models.pdf]]
