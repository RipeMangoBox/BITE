---
title: "SurgCoT: Advancing Spatiotemporal Reasoning in Surgical Videos through a Chain-of-Thought Benchmark"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SurgCoT_Advancing_Spatiotemporal_Reasoning_in_Surgical_Videos_through_a_Chain_of_Thought_Benchmark.pdf
project_link: null
code_link: "https://github.com/CVI-SZU/SurgCoT"
aliases:
- SurgCoT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: SurgCoT 基准引入的结构化三阶段渐进推理框架和五元组标注协议（知识+线索），通过显式提供临床背景知识和视频时空证据，将隐式推理过程分解为可审核的级联子问题，从而干预并评估模型的推理路径。
primary_logic: 通过将外科视频诊断任务分解为“全局理解-片段定位-帧级精确定位”的层级化子问题，并在每个阶段注入领域知识（Knowledge）和时空线索（Clue），可以引导 MLLMs 执行透明的链式推理，显著提升其时空定位精度；然而，实验表明即使最强的商业模型在帧级细粒度任务上仍存在较大性能差距，凸显了当前 MLLMs 在复杂动态场景理解上的局限性。
claims:
- 在 Full-Context（FC）设置下，GPT-5 在 SurgCoT 主问题上的平均准确率达到 87.58%，较基线（BL）的 76.62% 提升 10.96 个百分点。
- 引入知识增强（KE）后，LLaVA-Med-7B 的主问题准确率从 68.15%（BL）提升至 75.22%，提升幅度达 7.07%。
- 在微过渡定位（MTL）和异常发生追踪（AOT）等细粒度时空推理任务上，从 BL 到 FC 的设置转换使 Claude-Sonnet-4.5 的准确率分别大幅提升 27.71% 和 20.60%。
- SurgCoT 通过三级子问题分解和 Knowledge/Clue 注入，迫使模型执行可追溯的推理链，基本解决了直接回答时常见的语义混淆和时空错位问题。
---

# SurgCoT: Advancing Spatiotemporal Reasoning in Surgical Videos through a Chain-of-Thought Benchmark

> [!tip] 核心洞察
> 通过将外科视频诊断任务分解为“全局理解-片段定位-帧级精确定位”的层级化子问题，并在每个阶段注入领域知识（Knowledge）和时空线索（Clue），可以引导 MLLMs 执行透明的链式推理，显著提升其时空定位精度；然而，实验表明即使最强的商业模型在帧级细粒度任务上仍存在较大性能差距，凸显了当前 MLLMs 在复杂动态场景理解上的局限性。

| 字段 | 内容 |
|------|------|
| 中文题名 | SurgCoT：基于思维链的手术视频时空推理基准 |
| 英文题名 | SurgCoT: Advancing Spatiotemporal Reasoning in Surgical Videos through a Chain-of-Thought Benchmark |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.20319) · [Code](https://github.com/CVI-SZU/SurgCoT) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SurgCoT |
| Dataset | SurgCoT Main Questions |

> [!tip] 效果简介
> - SurgCoT Main Questions (Average) 上，Accuracy (%) 87.58 (FC) vs 76.62 (BL) (+10.96)。
> - SurgCoT Main Questions (LLaVA-Med-7B) 上，Accuracy (%) 75.22 (KE) vs 68.15 (BL) (+7.07)。

## 概述

**核心问题：外科视频理解的时空推理瓶颈**

现有的外科视频问答（VQA）基准，如 **Surgical-VQA**（Seenivasan et al., MICCAI 2022）、**Cholec80-VQA**（Seenivasan et al., MICCAI 2022）和 **SSG-VQA**（Yuan et al., IJCARS 2024），主要局限于帧级或短片段级的单项识别任务（如相位识别、工具识别）。这些基准缺乏对跨时序因果关系和细粒度时空定位的统一评估，无法衡量多模态大语言模型（MLLMs）在外科场景中执行链式思维（Chain-of-Thought, CoT）推理的能力。外科视频理解的根本瓶颈在于：真实临床诊断需要从全局视频理解出发，逐步聚焦到关键片段和精确帧级定位，而现有基准无法为这一层级化推理过程提供结构化的监督信号。

**核心方法：SurgCoT 的三阶段渐进推理与五元组标注**

SurgCoT 基准通过两个关键设计干预模型的推理路径：

1. **三阶段渐进推理框架**：将外科视频诊断任务分解为“全局视频理解（Q1）→ 条件片段分析（Q2）→ 细粒度帧定位（Q3）”的层级化子问题链。每个阶段的答案作为下一阶段的约束条件，形成可追溯的级联推理路径。

2. **五元组标注协议**：在传统“问题-选项-答案”三元组基础上，显式注入**临床背景知识（Knowledge）**和**时空线索（Clue）**。Knowledge 提供手术流程、器械功能等上下文背景，Clue 则提供精确的时间窗口、感兴趣区域（ROI）和空间证据。这种设计将隐式推理过程分解为可审核的级联子问题，迫使模型执行透明的链式推理。

**核心发现：结构化线索显著提升推理精度，但细粒度任务仍存巨大差距**

在 10 个主流 MLLMs 上的系统评估揭示了两个关键结论：

- **结构化知识与时序线索的有效性**：在 Full-Context（FC）设置下，GPT-5 在 SurgCoT 主问题上的平均准确率达到 **87.58%**，较基线（BL）的 76.62% 提升 **10.96 个百分点**。即使对于参数量较小的 LLaVA-Med-7B，仅引入知识增强（KE）即可将主问题准确率从 68.15% 提升至 75.22%（+7.07%）。在微过渡定位（MTL）和异常发生追踪（AOT）等细粒度时空推理任务上，Claude-Sonnet-4.5 从 BL 到 FC 的设置转换分别带来 **27.71%** 和 **20.60%** 的巨大提升，表明结构化线索对复杂时序推理任务尤为关键。

- **MLLMs 的链式推理能力仍存显著差距**：商业模型整体优于开源和医学专用模型，但即使在最强设置下，模型在帧级细粒度定位等子问题上仍存在较大性能缺口。这凸显了当前 MLLMs 在复杂动态场景理解上的根本局限性。

**方法定位**

SurgCoT 区别于现有外科 VQA 基准的核心特征在于：它是首个覆盖 7 个外科专业、支持视频级到帧级多粒度标注、并提供显式时空定位监督的链式推理基准。与仅覆盖单一专业或帧级任务的 **SurgVLM-Bench**（Zeng et al., arXiv 2025）等基准不同，SurgCoT 通过五元组标注和渐进式条件推理链，将外科视频理解从“识别”推向“推理”，为评估 MLLMs 的时空因果推理能力提供了标准化测试平台。

## 背景与动机

### 外科视频理解的范式局限

外科视频理解是迈向智能手术辅助的关键技术环节。近年来，多模态大语言模型（MLLMs）在通用视频理解任务上取得了显著进展，但其在外科场景中的应用仍面临根本性瓶颈。现有的外科视频问答基准，如 **Surgical-VQA**（Seenivasan et al., MICCAI 2022）、**Cholec80-VQA**（Seenivasan et al., MICCAI 2022）、**SSG-VQA**（Yuan et al., IJCARS 2024）和 **SurgVLM-Bench**（Zeng et al., arXiv 2025），普遍将评估局限于帧级或短片段级的单项任务——例如手术阶段识别、器械检测或工具计数。这些基准的标注协议通常采用“问题-选项-答案”三元组形式，缺乏对跨时序因果关系的建模和对细粒度时空推理的统一评估框架。

这一设计缺陷导致了一个深层问题：**现有基准无法衡量 MLLMs 在外科场景中的链式思维能力**。真实的外科诊断并非孤立的帧级判断，而是需要从全局手术流程理解出发，逐步聚焦到关键片段，最终在帧级精确锁定异常位置和时序的层级化推理过程。缺乏对这一推理路径的系统评估，意味着当前基准无法揭示模型在复杂动态场景理解中的真实能力边界。

### 思维链推理的缺失与介入路径

外科视频中的时空推理本质上是一个多级依赖的诊断链：手术建议必须建立在已确认的病变位置之上，而病变位置的确认又依赖于对病理类型和手术阶段的全局把握。然而，现有基准将这一隐式推理过程压缩为单一的端到端问答，既无法追踪模型的推理路径，也无法定位推理失败的具体环节。

SurgCoT 的核心动机正是填补这一空白。该工作引入了一个结构化的三阶段渐进推理框架，将诊断任务分解为“全局视频理解（Q1）→ 条件片段分析（Q2）→ 细粒度帧定位（Q3）”的层级化子问题序列。同时，通过五元组标注协议（问题→选项→知识→线索→答案），在每个推理阶段显式注入临床背景知识（Knowledge）和视频时空证据（Clue），将隐式推理过程转化为可审核、可追溯的级联推理链。这一设计不仅为评估 MLLMs 的链式思维能力提供了基准，也为引导模型执行透明推理提供了结构化干预手段。

## 核心创新

SurgCoT 的核心创新在于将外科视频理解从“单帧/短片段问答”重构为**结构化、可审核的链式时空推理**。与现有基准相比，其关键 changed slots 体现在三个层面。

### 1. 标注协议：从三元组到五元组

传统外科 VQA 基准（如 **Surgical-VQA** (Seenivasan et al., MICCAI 2022)、**Cholec80-VQA** (Seenivasan et al., MICCAI 2022)）采用 Question-Option-Answer 三元组标注，模型直接从问题映射到答案，推理过程不可见且难以纠错。SurgCoT 引入 **五元组标注协议**（Question→Option→Knowledge→Clue→Answer），显式注入两类互补信息：

- **Knowledge**：提供临床背景知识（解剖结构、病理特征、手术规范），用于纠正模型的语义混淆；
- **Clue**：提供从视频内容中直接提取的时空证据（精确时间窗口、ROI 空间定位、动作起始帧），用于消除时空错位。

这一设计将隐式推理过程外化为可追溯的标注序列，使模型的推理路径透明化，便于审核与诊断。

### 2. 推理层级：从单层到三级级联

现有基准通常仅在单一粒度上评估（视频级、片段级或帧级之一），缺乏对跨层级因果推理的考察。SurgCoT 构建了 **Q1→Q2→Q3 三级渐进推理框架**：

$$
\begin{array}{rl}
& \underbrace{(\Omega^{1}, \mathrm{O1}, \mathrm{K1}, \mathrm{C1})}_{\text{Global Video Comprehension}} \Rightarrow \mathbb{A}1 \\
& \underbrace{(\Omega^{2}, \mathrm{O2}, \mathrm{K2}, \mathrm{C2}, \mathbb{A}1)}_{\text{Conditioned Clip Analysis}} \Rightarrow \mathbb{A}2 \\
& \underbrace{(\Omega^{3}, \mathrm{O3}, \mathrm{K3}, \mathrm{C3}, \mathbb{A}2)}_{\text{Fine-grained Frame Localization}} \Rightarrow \mathbb{A}3
\end{array}
$$

该推理链从**全局视频理解**（Q1）出发，确定手术类型与关键阶段；进而**条件化片段分析**（Q2），在缩小的时间窗口内定位异常区域；最终实现**细粒度帧级精确定位**（Q3），给出手术建议或异常判定。每一级子问题的答案作为下一级的约束条件，强制模型执行有依赖的链式推理，而非“跳过中间步骤直接猜测”。

### 3. 时空监督：从无/弱监督到内置证据

此前基准通常不提供时空定位监督，或仅提供粗粒度位置标签。SurgCoT 的 Clue 字段内置了系统化提取的时空证据：空间维度通过 YOLOv10 组织检测与 SAM2 工具分割生成帧级 ROI，时间维度通过 ByteTrack 跨帧追踪与外观变化检测提取动作起始帧。这种**内置时空监督**使模型在推理时可直接引用精确的时空锚点，显著提升细粒度定位能力——实验表明，从 Baseline (BL) 到 Full-Context (FC) 设置，Claude-Sonnet-4.5 在异常发生追踪（AOT）和微过渡定位（AM）任务上准确率分别提升 20.60% 和 27.71%（Table 2）。

综上，SurgCoT 通过**五元组标注 + 三级级联推理 + 内置时空证据**的组合设计，将外科视频理解从“端到端答案映射”升级为“可干预、可审核的链式推理”，为评估和提升 MLLMs 在复杂动态场景中的时空认知能力提供了新的基准范式。

## 整体框架

SurgCoT 基准的构建围绕一个**结构化三阶段渐进推理框架**与配套的**五元组标注协议**展开，其核心目标是将外科视频诊断中隐式的链式思维过程显式化、可审核化。图 2 给出了完整的构建流水线，包含四个关键模块：数据处理、三阶段推理与五元组标注、VQA 生成和质量控制。

### 数据处理模块

该模块负责多源视频的收集、分层分割与自动化证据挖掘。视频来源覆盖 7 个外科专科、35 种术式，经标准化处理后进入分层分割阶段。分割采用**层次化线索融合**策略——同时利用视觉场景变化、器械/组织过渡以及语音识别（ASR）锚点，生成语义连贯的视频片段。在此基础上，系统进行时空证据的自动提取：

- **空间证据**：通过 YOLOv10 进行逐帧组织检测，结合 SAM2 完成器械分割，并利用 ByteTrack 实现跨帧目标追踪，从而获得 ROI 级别的空间定位信息。
- **时间证据**：通过检测外观变化指标来识别动作起始点，以最小视觉线索作为帧级时间锚点。

这些自动提取的时空标注为后续五元组中的 Clue 字段提供了原始素材。

### 三阶段渐进推理与五元组标注

这是 SurgCoT 的方法核心。框架将每个诊断问题分解为三个级联子问题，形成一条从粗到细的推理链：

$$
\begin{array} { r l } & { \underbrace { ( \Omega ^ { 1 } , \ \mathrm { O 1 } , \ \mathrm { K 1 } , \ \mathrm { C 1 } ) } _ { \mathrm { Global \ Video \ Comprehension } } \Rightarrow \mathbb { A } \mathbb { 1 } } \\ & { \qquad \underbrace { ( \Omega ^ { 2 } , \ \mathrm { O 2 } , \ \mathrm { K 2 } , \ \mathrm { C 2 } , \ \mathrm { A1 } ) } _ { \mathrm { Conditioned \ Clip \ Analysis } } \Rightarrow \mathbb { A } \mathcal { 2 } } \\ & { \qquad \underbrace { ( \Omega ^ { 3 } , \ \mathrm { O 3 } , \ \mathrm { K 3 } , \ \mathrm { C 3 } , \ \mathbb { A } 2 ) } _ { \mathrm { Fine-grained \ Frame \ Localization } } \Rightarrow \mathbb { A } \mathcal { 3 } . } \end{array}
$$

- **Q1（全局视频理解）**：模型需从完整视频中把握整体手术上下文。
- **Q2（条件化片段分析）**：以 Q1 的答案 A1 为约束，在相关视频片段内进行更细致的分析。
- **Q3（细粒度帧定位）**：以 Q2 的答案 A2 为约束，在关键帧上完成精确的时空定位与诊断决策。

这种设计强制建立了诊断决策的严格依赖链——例如，手术建议（A3）必须基于已确认的病变位置（A2），而后者又依赖于已建立的病理上下文（A1）。

每个子问题均采用**五元组标注协议**：Question → Option → Knowledge → Clue → Answer。其中，**Knowledge 字段**提供临床背景知识（如解剖结构、病理特征），用于纠正模型的语义理解偏差；**Clue 字段**提供从视频内容中直接提取的时空证据（如时间窗口、ROI 区域），用于引导模型的注意力聚焦。两者协同作用，构成了 SurgCoT 干预模型推理路径的核心机制。

### VQA 生成与质量控制

基于上述框架，系统通过**本体驱动的模板化生成**方式，在五种时空推理任务（详见实验部分）上批量构建带干扰项的 VQA 对，最终生成 19,345 个主问题与 59,177 个子问题。所有标注经过**双轮人机验证**与多标准一致性检查，确保逻辑正确性和时空标注的准确性。

### 补充图表

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/001_Figure_1.jpg]]
*Figure 1: SurgCoT comprises 2,841 surgical videos across 7 specialties and 35 procedures, with 19,345 main questions and 59,177 sub-questions. SurgCoT advances beyond frame-level tasks (e.g., phase/tool recognition) by introducing a three-stage, five-tuple annotation protocol (Question→Option→Knowledge→Clue→Answer) to scaffold chain-of-thought reasoning. The framework’s efficacy stems from its multi-stage reasoning structure and the synergistic interaction between the Knowledge field, which supplies contextual background, and the Clue field, which provides targeted spatiotemporal evidence, jointly enabling hierarchical reasoning*

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/003_Figure_2.jpg]]
*Figure 2: Construction pipeline of SurgCoT benchmark*

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/004_Figure_3.jpg]]
*Figure 3: Statistics of SurgCoT: 2,841 videos, 19,345 questions, and 59,177 sub-questions across 35 procedures and 7 specialties*

## 核心模块与公式推导

### 三级渐进式推理框架

SurgCoT 的核心创新在于构建了一条从粗粒度到细粒度的结构化推理链，将外科视频诊断任务分解为三个级联子问题：

1. **Q1 — 全局视频理解（Global Video Comprehension）**：模型需从完整手术视频中提取宏观语义，例如识别手术类型、关键解剖结构或整体操作阶段。
2. **Q2 — 条件片段分析（Conditioned Clip Analysis）**：在 Q1 答案的约束下，模型聚焦于特定视频片段，定位关键事件发生的时空窗口。
3. **Q3 — 细粒度帧定位（Fine-grained Frame Localization）**：以 Q2 的定位结果为条件，模型需在帧级别精确识别目标区域、工具交互或异常发生时刻。

该框架的核心机制是**条件化级联依赖**：每一阶段的答案作为下一阶段的输入约束，迫使模型执行可追溯的推理路径，而非直接从视频跳跃到最终答案。这种设计干预了 MLLMs 在外科场景中常见的语义混淆和时空错位问题。

### 五元组标注协议

为支撑三级推理，SurgCoT 引入了五元组标注协议 `(Question, Option, Knowledge, Clue, Answer)`，相较传统 VQA 基准的三元组 `(Question, Option, Answer)` 增加了两个关键字段：

- **Knowledge（知识字段）**：提供临床背景知识，如解剖学定义、手术步骤规范或病理特征描述，帮助模型建立正确的语义先验。
- **Clue（线索字段）**：提供从视频内容中直接提取的时空证据，包括精确的时间窗口、感兴趣区域（ROI）坐标和空间关系描述。

Knowledge 与 Clue 的协同作用构成了 SurgCoT 的因果调控旋钮：Knowledge 解决“语义纠偏”问题，Clue 解决“时空锚定”问题，二者共同将隐式推理过程显式化为可审核的级联子问题。

### 证据挖掘模块

线索字段的生成依赖两个自动化证据挖掘子模块：

- **空间证据构建**：通过 YOLOv10 进行帧级组织检测，结合 SAM2 进行工具分割，并利用 ByteTrack 实现跨帧目标跟踪，生成组织-工具的 ROI 空间关系描述。
- **时间证据构建**：通过检测外观变化指标来识别动作起始点（Action onsets），以最小视觉线索作为帧级时间锚点，标记关键事件的时间边界。

### 核心公式：渐进条件化推理链

SurgCoT 的三级推理过程可形式化为如下递推结构：

$$
\begin{array} { r l } 
& \underbrace{ ( \Omega ^ { 1 } , \ \mathrm { O 1 } , \ \mathrm { K 1 } , \ \mathrm { C 1 } ) } _ { \mathrm { Global~Video~Comprehension } } \Rightarrow \mathbb { A } \mathbb { 1 } \\
& \qquad \underbrace{ ( \Omega ^ { 2 } , \ \mathrm { O 2 } , \ \mathrm { K 2 } , \ \mathrm { C 2 } , \ \mathbb { A } \mathbb { 1 } ) } _ { \mathrm { Conditioned~Clip~Analysis } } \Rightarrow \mathbb { A } \mathcal { 2 } \\
& \qquad \underbrace{ ( \Omega ^ { 3 } , \ \mathrm { O 3 } , \ \mathrm { K 3 } , \ \mathrm { C 3 } , \ \mathbb { A } \mathcal { 2 } ) } _ { \mathrm { Fine-grained~Frame~Localization } } \Rightarrow \mathbb { A } \mathcal { 3 } .
\end{array}
$$

**变量含义**：
- $\Omega^i$：第 $i$ 阶段的视觉输入（完整视频 / 片段 / 帧序列）
- $\mathrm{O}i$：第 $i$ 阶段的选项集合
- $\mathrm{K}i$：第 $i$ 阶段注入的临床知识
- $\mathrm{C}i$：第 $i$ 阶段提供的时空线索
- $\mathbb{A}i$：第 $i$ 阶段输出的答案，其中 $\mathbb{A}1$ 和 $\mathbb{A}2$ 分别作为下一阶段的条件约束

该公式揭示了 SurgCoT 的核心机制：推理链的每一步不仅依赖视觉输入和选项，还通过显式注入 Knowledge 和 Clue 来引导模型注意力，同时利用前序答案 $\mathbb{A}i$ 实现跨阶段的因果约束——这从根本上区别于传统 VQA 中“单步映射”的推理模式。

## 实验与分析

### 基准评估协议设计

为系统验证 SurgCoT 框架对多模态大语言模型（MLLMs）时空推理能力的干预效果，研究设计了三级渐进式评估协议：

1. **Baseline (BL)**：仅向模型提供手术视频与主问题，模拟直接回答场景，反映模型在无辅助信息下的原始推理能力。
2. **Knowledge-Enhanced (KE)**：在 BL 基础上注入五元组中的临床背景知识（Knowledge），考察领域知识对推理的独立贡献。
3. **Full-Context (FC)**：提供完整五元组支持（视频 + Knowledge + Clue），评估知识与时空间线索协同作用下的链式推理上限。

所有模型采用统一零样本提示模板与固定解码参数（temperature=0.0, top_p=1.0），禁用采样重试，并在相同硬件上运行，确保比较公平性。评价指标以准确率（Accuracy）为主。

### 主实验结果

Table 2 展示了 10 个 MLLMs 在五种临床推理任务上跨越 BL→KE→FC 三级设置的性能表现。核心发现如下：

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/005_Table_2.jpg]]
*Table 2: Evaluation of 10 MLLMs across five clinical reasoning tasks under progressive settings (BL→KE→FC) shows: 1) commercial models outperform open-source and medical-specialized counterparts, and 2) the five-tuple annotation protocol improves reasoning accuracy under both (KE) and (FC) settings. Best results in bold, second-best underlined*

**商业模型显著领先开源与医学专用模型。** 在 FC 设置下，**GPT-5** 以 87.58% 的平均准确率位居榜首，**Claude-Sonnet-4.5** 紧随其后。相比之下，医学专用模型 **LLaVA-Med-7B** 在 BL 设置下仅达 68.15%，开源通用模型 **LLaVA-OneVision-7B** 为 69.52%，与商业模型存在显著差距。这一结果表明，当前医学专用 MLLMs 在外科视频时空推理上的泛化能力仍远逊于通用商业模型。

**五元组标注协议持续提升推理准确率。** 从 BL 到 FC 的完整信息注入使 GPT-5 的平均准确率从 76.62% 提升至 87.58%，绝对增益达 **+10.96 个百分点**。仅引入知识增强（KE）即可使 LLaVA-Med-7B 从 68.15% 提升至 75.22%（**+7.07 个百分点**），验证了临床背景知识对推理的独立正向作用。

**细粒度时空推理任务受益最为显著。** 在微过渡定位（MTL）和异常发生追踪（AOT）等需要精确定位时空边界的任务上，Claude-Sonnet-4.5 从 BL 到 FC 的准确率分别提升 **+27.71%** 和 **+20.60%**，表明结构化时空线索对复杂时序推理任务尤为关键。

### 子问题推理链消融分析

Table 3 通过分解三级子问题（Q1→Q2→Q3）的准确率，揭示了 MLLMs 在链式推理过程中的性能瓶颈：

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/007_Table_3.jpg]]
*Table 3: Sub-question accuracy under progressive reasoning settings (BL→KE→FC). Evaluation reveals: 1) MLLMs show chain-of-thought reasoning gaps, with performance dropping at intermediate steps; 2) SurgCoT’s structured framework supports progressive reasoning, yielding gains under KE/FC settings. Best results in bold, second-best underlined*

1. **中间步骤推理断裂**：多数模型在 Q2（条件片段分析）阶段出现准确率骤降，表明从全局理解到局部定位的推理过渡是当前 MLLMs 的主要薄弱环节。即使最终主问题正确，中间子问题的错误率仍较高，说明模型存在“猜对答案但推理路径错误”的现象。

2. **知识与时空间线索的协同增益**：从 BL 到 KE 再到 FC，各子问题准确率呈阶梯式上升。LLaVA-Med-7B 在五个推理维度上的平均准确率从 BL 到 KE 提升近 7%，进一步引入 Clue 后持续增长，证实了 Knowledge 提供语义约束、Clue 提供时空锚点的互补机制。

3. **帧级定位仍是最大挑战**：Q3（细粒度帧定位）在各设置下的准确率普遍低于 Q1 和 Q2，即使最强模型 GPT-5 在 FC 设置下也未能完全解决帧级精确定位问题，凸显了当前 MLLMs 在动态场景细粒度理解上的根本性局限。

### 定性分析：推理路径的可追溯修正

Figure 4 通过典型案例展示了 SurgCoT 框架如何将错误推理逐步修正为正确诊断链：

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/006_Figure_4.jpg]]
*Figure 4: SurgCoT constructs a diagnostic chain-of-thought by progressively decomposing a flawed baseline (BL) into clinical subquestions, correcting semantics with knowledge (KE), and refining evidence with spatiotemporal clues (FC)*

- **BL 阶段**：模型直接回答时出现语义混淆（如将“电凝止血”误判为“机械压迫”）和时空错位（定位到错误手术阶段）。
- **KE 阶段**：注入临床知识后，模型修正了语义理解偏差，但时空定位仍不精确。
- **FC 阶段**：结合时空线索后，模型成功锁定正确的手术片段和帧级关键区域，推理路径变得透明且可审核。

这一级联修正过程验证了 SurgCoT 的核心设计理念：通过将隐式推理分解为可审核的子问题链，并注入领域知识与时空间证据，可以迫使模型执行可追溯的链式推理，基本解决直接回答时常见的语义混淆和时空错位问题。

### 失败模式与局限性

尽管 FC 设置大幅提升了模型表现，实验仍暴露了若干系统性失败模式：

- **细粒度帧级定位能力不足**：Q3 子问题的准确率在所有模型中均显著低于 Q1/Q2，表明当前 MLLMs 在帧级空间关系理解上存在根本性瓶颈。即使提供了精确的时空线索，模型仍难以准确关联视觉证据与语义判断。
- **中间推理步骤的脆弱性**：Q2 阶段的准确率骤降现象暗示，当前 MLLMs 的链式推理能力并非真正意义上的因果推理，而更多依赖表层模式匹配。一旦中间步骤出错，后续推理极易发生级联崩溃。
- **跨专业的泛化差异**：不同外科专业间的性能波动较大，部分罕见手术类型上的准确率显著低于常见手术，说明模型的领域知识覆盖仍不均衡。具体跨专业性能数据需查阅原文详细表格进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2749_https_arxiv_org_abs_2604_20319/figures/002_Table_1.jpg]]
*Table 1: Comparison of surgical benchmarks. Our SurgCoT uniquely spans 7 surgical specialties with multi-level annotations (video/- clip/frame), supporting hierarchical spatiotemporal reasoning with localization supervision and clinician-derived reference standards*

## 方法谱系与知识库定位

### 任务谱系：从帧级识别到链式时空推理

SurgCoT 所处的领域是外科视频理解基准，其演进脉络可归纳为三个阶段：

1. **帧级单任务基准**：早期工作如 **Surgical-VQA**（Seenivasan et al., MICCAI 2022）和 **Cholec80-VQA**（Seenivasan et al., MICCAI 2022）将外科视频问答限定在腹腔镜手术的单帧或短片段层面，任务类型以相位识别、工具识别等分类问题为主，标注协议为传统的“问题-选项-答案”三元组。这类基准的核心局限在于：无法捕捉跨时序的因果依赖关系，也无法评估模型对“何时、何处、发生什么”的联合推理能力。

2. **知识增强型基准**：**SSG-VQA**（Yuan et al., IJCARS 2024）引入场景图作为结构化知识源，将问答与手术场景的语义关系关联起来；**SurgVLM-Bench**（Zeng et al., arXiv 2025）则扩展到多专业覆盖，构建了层次化知识体系。这些工作突破了纯视觉问答的范式，但仍停留在单帧或单片段推理层面，缺乏对视频级时空定位的显式监督。

3. **链式时空推理基准**：SurgCoT 的核心突破在于将任务从“直接回答”重构为“渐进推理”——通过 Q1（视频级全局理解）→ Q2（片段级条件分析）→ Q3（帧级精确定位）的三级级联框架，迫使模型执行可追溯的诊断思维链。这一设计直接回应了现有基准的根本瓶颈：缺乏对跨时序因果关系和细粒度时空推理的统一评估手段。

### 标注协议的范式跃迁

SurgCoT 的方法学贡献集中体现在标注协议的三个关键槽位变更上：

- **标注字段**：从传统的“Question-Option-Answer”三元组扩展为“Question-Option-Knowledge-Clue-Answer”五元组。其中 Knowledge 字段注入临床背景知识（如解剖结构、病理特征），Clue 字段提供从视频内容中直接提取的时空证据（精确时间窗口、ROI 区域、空间线索）。这一设计将隐式推理过程显式化为可审核的级联子问题。

- **推理层级**：从单帧/短片段的扁平化推理升级为“视频级→片段级→帧级”的三级级联。每级子问题的答案作为下一级推理的约束条件，形成严格的依赖链——例如，手术建议（A3）必须建立在已确认的病灶位置（A2）之上，而后者又依赖于已建立的病理背景（A1）。

- **时空监督**：从通常缺乏或仅有粗粒度位置监督，升级为内置时空线索（Clue）提供精确的时间窗口、ROI 和空间证据。空间证据通过 YOLOv10 帧级组织检测和 SAM2 工具分割构建，配合 ByteTrack 跨帧追踪；时间证据则通过检测动作起始的外观变化指标提取。

### 推理链的形式化

SurgCoT 的渐进条件推理链可形式化为：

$$
\begin{array} { r l } & { \underbrace { ( \Omega ^ { 1 } , \ \mathrm { O 1 } , \ \mathrm { K 1 } , \ \mathrm { C 1 } ) } _ { \mathrm { G i o b a l ~ V i d e o ~ C o m p r e h e n s i o n } } \Rightarrow \mathbb { A } \mathbb { 1 } } \\ & { \qquad \underbrace { ( \Omega ^ { 2 } , \ \mathrm { O 2 } , \ \mathrm { K 2 } , \ \mathrm { C 2 } , \ \mathrm { \mathbb{A}1 } ) } _ { \mathrm { C o n d i t i o n e d ~ C l i p ~ A n a l y s i s } } \Rightarrow \mathbb { A } \mathcal { 2 } } \\ & { \qquad \underbrace { ( \Omega ^ { 3 } , \ \mathrm { O 3 } , \ \mathrm { K 3 } , \ \mathrm { C 3 } , \ \mathbb { A } 2 ) } _ { \mathrm { F i n e - g r a i n e d ~ F r a m e ~ L o c a l i z a t i o n } } \Rightarrow \mathbb { A } \mathcal { 3 } . } \end{array}
$$

其中 $\Omega^i$ 为第 $i$ 级问题，$\mathrm{K}^i$ 和 $\mathrm{C}^i$ 分别为对应的知识和线索，$\mathbb{A}^{i-1}$ 作为下一级的条件约束。这一设计确保了诊断决策的可追溯性。

### 适用边界与局限

SurgCoT 的五元组标注协议和三级推理框架在以下条件下最为有效：
- 任务涉及跨时序因果推理（如异常发生追踪 AOT、微过渡定位 MTL），而非单纯的静态识别；
- 视频内容具有明确的手术阶段结构和可标注的时空证据；
- 评估目标是衡量 MLLMs 的链式思维能力，而非单一任务的绝对性能。

当前工作的主要局限在于：
- 实验证据表明，即使在 Full-Context（FC）设置下，最强商业模型在帧级细粒度任务上仍存在显著性能差距，凸显了当前 MLLMs 在复杂动态场景理解上的根本性局限；
- 基准构建依赖自动化证据挖掘（YOLOv10 + SAM2 + ByteTrack），其标注质量受上游检测模型精度影响，尽管经过双轮人机验证，但在边缘案例上可能存在噪声；
- 五元组标注成本显著高于传统三元组，限制了基准的快速扩展能力。

### 开放问题

SurgCoT 揭示的核心开放问题是：当前 MLLMs 在具备完整知识和时空线索的条件下，仍无法可靠地完成帧级精确定位任务。这指向两个深层研究方向：
1. **视频推理架构**：现有 MLLMs 的视频编码器是否真正捕获了细粒度时序动态，还是仅依赖空间特征的粗糙聚合？
2. **链式推理的可靠性**：即使模型在子问题上表现提升，中间步骤的性能下降（Table 3）表明推理链存在断裂风险——如何保证长程依赖的稳定性？

这些问题超出了基准本身的范围，需要模型架构层面的创新来回应。

## 原文 PDF

![[paperPDFs/CVPR_2026/SurgCoT_Advancing_Spatiotemporal_Reasoning_in_Surgical_Videos_through_a_Chain_of_Thought_Benchmark.pdf]]
