---
title: "RealUnify: Do Unified Models Truly Benefit from Unification? A Comprehensive Benchmark"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RealUnify_Do_Unified_Models_Truly_Benefit_from_Unification_A_Comprehensive_Benchmark.pdf
project_link: null
code_link: "https://github.com/FrankYang-17/RealUnify"
aliases:
- RealUnify
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 缺乏旨在促进理解与生成双向交互的训练目标与归纳偏置，使得模型无法在端到端场景中协同使用两种能力。
primary_logic: 尽管统一模型在单独的理解或生成任务上可能表现不俗，但在需要两者深度协同的任务上表现大幅下降，表明架构统一不等于能力协同。逐步分解后UEG任务性能提升、GEU任务性能下降的双重模式揭示了模型内部拥有相关知识但无法有效整合。
claims:
- 直接评估下，最佳开源统一模型在UEG上的平均准确率仅为37.5%，GEU任务同样表现不佳。
- 逐步分解UEG任务后，所有模型性能提升，其中BAGEL提升最大（+15%）；但逐步分解GEU任务后，所有模型性能反而下降。
- 组合最好的专用模型（Gemini 2.5 Pro用于理解，GPT-Image-1用于生成）作为“oracle”，在UEG上达到72.7%，远超现有统一模型。
- RealUnify UEG (Overall) 上 Accuracy (%) = UniPic2 (最佳开源统一) 37.5
---

# RealUnify: Do Unified Models Truly Benefit from Unification? A Comprehensive Benchmark

> [!tip] 核心洞察
> 尽管统一模型在单独的理解或生成任务上可能表现不俗，但在需要两者深度协同的任务上表现大幅下降，表明架构统一不等于能力协同。逐步分解后UEG任务性能提升、GEU任务性能下降的双重模式揭示了模型内部拥有相关知识但无法有效整合。

| 字段 | 内容 |
|------|------|
| 中文题名 | RealUnify: 统一模型真能从统一中获益吗？一个综合基准测试 |
| 英文题名 | RealUnify: Do Unified Models Truly Benefit from Unification? A Comprehensive Benchmark |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.24897) · [Code](https://github.com/FrankYang-17/RealUnify) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | RealUnify (双评估协议基准) |
| Dataset | RealUnify UEG, RealUnify GEU |

> [!tip] 效果简介
> - RealUnify UEG (Overall) 上，Accuracy (%) UniPic2 (最佳开源统一) 37.5 vs Nano Banana (最佳商用统一) 63.0 (-25.5)。
> - RealUnify UEG (BAGEL 逐步 vs 直接) 上，Accuracy (%) 逐步 47.7 vs 直接 32.7 (+15.0)。
> - RealUnify GEU (Overall) 上，Accuracy (%) BAGEL (最佳统一) 39.3 vs Gemini 2.5 Pro (最佳专用) 54.8 (-15.5)。

## 概要

### 1. 问题：统一模型的能力协同困境

当前多模态统一模型（unified models）旨在将视觉理解与图像生成整合于单一架构，然而，一个根本性问题悬而未决：**理解能力与生成能力之间是否真正实现了相互增强？** RealUnify 基准测试的构建正是为了系统性地回答这一问题。

现有基准大多停留在孤立评估理解或生成能力的阶段（Stage 1），或仅仅将两类任务简单拼接（Stage 1.5），少数工作初步探索了能力间的单向促进（Stage 2）。然而，这些工作均未能全面检验理解与生成之间的**双向协同**——即理解能否提升生成质量（Understanding Enhances Generation, UEG），以及生成能力能否反过来辅助理解任务（Generation Enhances Understanding, GEU）。RealUnify 正是首个针对这一能力协同问题进行系统性诊断的基准。

### 2. 核心结论：架构统一不等于能力协同

RealUnify 的核心发现揭示了一个关键瓶颈：**当前统一模型无法有效融合理解与生成能力，仅靠架构统一无法实现双向协同。** 具体表现为以下三个层次的证据：

- **端到端性能低下**：在直接评估（direct evaluation）下，最佳开源统一模型在 UEG 任务上的平均准确率仅为 37.5%，而最佳商用统一模型也仅达到 63.0%。GEU 任务同样表现不佳，最佳统一模型（BAGEL）的准确率仅为 39.3%，远低于专用模型的 54.8%。
- **分解评估揭示能力割裂**：当将 UEG 任务逐步分解为“先理解、后生成”两个阶段时，所有统一模型性能均获提升（BAGEL 提升最为显著，达 +15%）；然而，当将 GEU 任务分解为“先生成、后理解”时，所有模型性能反而下降。这一“UEG 分解提升、GEU 分解下降”的双重模式表明，模型内部虽然拥有相关知识，但无法在端到端场景中有效整合两种能力。
- **专用模型组合远超统一模型**：将最佳专用理解模型（Gemini 2.5 Pro）与最佳专用生成模型（GPT-Image-1）以逐步方式组合，构成“oracle”模型，其在 UEG 上达到 72.7%，显著优于最佳统一模型（63.0%）。这进一步说明，当前统一模型的瓶颈不在于单个能力的缺失，而在于**缺乏促进双向交互的训练目标与归纳偏置**。

### 3. 方法定位：首个能力协同诊断基准

RealUnify 的方法论贡献在于设计了一套**双评估协议**（dual-evaluation protocol），包含直接评估与逐步分解评估两个互补维度。直接评估测量端到端性能，检验统一是否带来整体增益；逐步分解评估则将任务拆解为理解与生成两个子阶段，精确诊断瓶颈所在——是单一能力不足，还是能力间协同失败。

基准数据集包含 1,000 个人工标注实例，覆盖 10 个类别、32 个子任务，均衡分布于 UEG 与 GEU 两大轨道。为评估生成图像质量，RealUnify 采用**投票式图像评判**机制，以 Gemini 2.5 Pro 作为评判模型，通过验证问题对生成结果进行自动化评估，并与人类专家评价进行了可靠性校验。

### 4. 主要结果概览

| 评估维度 | 最佳统一模型 | 对比基线 | 关键发现 |
|---------|------------|---------|---------|
| UEG 直接评估 | 37.5%（UniPic2，开源） / 63.0%（Nano Banana，商用） | Oracle 72.7% | 统一模型远未达到专用模型组合的上限 |
| UEG 逐步分解 | BAGEL +15%（32.7% → 47.7%） | 所有模型均提升 | 理解能力可辅助生成，但端到端整合失败 |
| GEU 整体 | 39.3%（BAGEL） | Gemini 2.5 Pro 54.8% | 生成能力对理解的辅助极为有限 |
| GEU 逐步分解 | 所有模型性能下降 | — | 分解后生成能力反而干扰理解，揭示协同机制缺失 |

这些结果表明，当前统一模型在需要理解与生成深度交互的复杂任务上存在系统性缺陷，架构统一远未带来能力协同。RealUnify 为未来研究指明了方向：需要设计专门促进双向交互的训练策略与模型归纳偏置，而非仅仅将两种能力堆叠于同一架构中。



### 问题背景：从能力堆叠到能力协同

多模态大模型正经历从“单一能力”到“统一架构”的范式迁移。早期基准仅关注视觉理解或图像生成中的某一维度（Stage 1），随后出现的基准开始在同一模型中同时考察两类能力（Stage 1.5），部分工作甚至初步探索了理解与生成之间的单向增强（Stage 2）。然而，一个根本性问题始终悬而未决：**统一模型是否真正从统一中获益？** 换言之，将理解与生成能力置于同一架构中，是否能够产生超越各自独立运行的协同效应？

Figure 1 清晰地定位了 RealUnify 在这一演进脉络中的位置——它是首个全面评估并充分挖掘理解与生成能力双向协同的基准，标志着从“能力共存”到“能力互促”的评估范式跃迁。

### 现有方法缺口：架构统一 ≠ 能力协同

当前统一模型的设计哲学隐含着一个未经严格检验的假设：只要将视觉理解和图像生成模块集成到同一模型中，两种能力就会自然地相互增强。然而，这一假设面临三重挑战：

1. **评估缺位**：现有基准（如 Table 1 所示）或聚焦于单一能力，或仅将两类任务简单拼接，缺乏专门设计来衡量“理解如何提升生成”以及“生成如何反哺理解”的机制。
2. **诊断盲区**：即使统一模型在孤立的理解或生成任务上表现尚可，我们也无从知晓其内部是否真正实现了跨能力的知识迁移，还是仅仅作为两个独立模块的松散耦合。
3. **协同瓶颈未知**：当任务需要理解与生成深度交互时——例如根据复杂推理生成精确图像，或通过生成图像辅助空间推理——现有模型的能力边界和失败模式缺乏系统性刻画。

### 本文动机：建立能力协同的严格基准

针对上述缺口，RealUnify 提出以下核心动机：

- **定义双向协同轨道**：构建两条核心评估轨道——**理解增强生成（Understanding Enhances Generation, UEG）** 和**生成增强理解（Generation Enhances Understanding, GEU）**——分别考察理解能力对生成精度的提升，以及生成能力对理解任务的辅助作用。
- **引入双评估协议**：设计**直接评估**与**逐步分解评估**相结合的双协议框架。直接评估测量端到端协同表现，逐步分解评估则将任务拆解为理解子任务和生成子任务，精确诊断能力瓶颈所在——是模型缺乏相关知识，还是无法有效整合已有能力？
- **揭示协同真相**：通过严格对照实验回答核心问题：统一模型的能力协同是真实的双向增强，还是仅停留在功能叠加层面？专用模型的组合是否比统一模型更有效？

这一基准的建立，不仅为现有统一模型提供了能力诊断工具，更为未来模型设计指明了关键方向：**如何从架构统一走向真正的能力协同**。



## 核心方法与创新机理

RealUnify的核心创新不在于提出一个新的统一模型，而在于构建了一套系统性的**诊断框架**，用以回答一个根本性问题：统一模型是否真正实现了理解与生成能力的协同，还是仅仅在单一架构内完成了功能的物理堆叠？

### 从“能力共存”到“能力协同”的评估范式转移

现有基准测试（如MMBench、GenEval）大多孤立地评估理解或生成能力，即便少数基准尝试同时覆盖两者，也仅停留在“能力共存”层面，未触及双向交互。RealUnify首次将评估焦点转向**能力协同**，通过两条核心任务轨道实现这一转变：

- **理解增强生成（Understanding Enhances Generation, UEG）**：测试模型是否能够利用知识和推理来提升生成精度。例如，模型需先理解“将红色立方体放在蓝色球体右侧”的空间语义，再生成符合约束的图像。
- **生成增强理解（Generation Enhances Understanding, GEU）**：测试生成能力是否能反过来辅助理解任务。例如，模型需先生成一张辅助图像来追踪心理旋转后的物体状态，再据此回答问题。

这一范式转变的深层动机源于一个关键观察：当前统一模型在单独的理解或生成任务上表现尚可，但在需要两者深度交互的端到端场景中性能骤降。这表明**架构统一不等于能力协同**——模型内部虽拥有相关知识，却无法在推理链中有效整合。

### 双评估协议：诊断而非仅评测

RealUnify的方法论创新集中体现在其**双评估协议**上，这是该基准区别于所有现有工作的核心“changed slot”：

| 评估维度 | 现有基准做法 | RealUnify做法 |
|---------|------------|-------------|
| 评估方式 | 仅直接端到端评估 | 直接评估 + 逐步分解评估 |
| 诊断能力 | 仅输出性能分数 | 揭示能力瓶颈与协同模式 |

**直接评估**测量模型端到端完成协同任务的整体表现，回答“统一是否带来收益”这一问题。**逐步分解评估**则将每个任务拆解为独立的“理解阶段”和“生成阶段”，分别提供中间结果（ground truth）作为输入，观察模型在各阶段的独立能力。两者的对比产生了揭示性发现：

- **UEG任务**：逐步分解后所有模型性能提升，其中BAGEL-7B提升幅度最大（+15个百分点，从32.7%升至47.7%）。这说明模型的理解能力本身是足够的，瓶颈在于端到端场景中无法将理解结果有效转化为生成约束。
- **GEU任务**：逐步分解后所有模型性能反而下降。这揭示了一个更深层的问题：当模型被迫依赖自身的生成输出作为理解输入时，生成质量的缺陷会级联放大，反而损害理解性能。换言之，**“以图助思”的前提是生成足够精确**，而当前统一模型尚未达到这一门槛。

这套双协议设计使得RealUnify不仅是评测工具，更是一个**诊断仪器**——它能够区分“能力缺失”与“整合失败”两种根本不同的失败模式。

### “Oracle”实验：揭示统一模型的性能上限

为量化统一模型与理想协同之间的差距，RealUnify构建了一个“Oracle”基线：将最佳专用理解模型（**Gemini 2.5 Pro**, Gemini Team, 2025）与最佳专用生成模型（**GPT-Image-1**, OpenAI, 2025）以逐步方式组合。该组合在UEG任务上达到72.7%的准确率，远超最佳统一模型Nano Banana的63.0%，差距达9.7个百分点。这一结果表明，**即使使用当前最强的专用模型，通过简单的流水线组合即可显著超越任何统一模型**，进一步印证了“统一架构远未实现能力协同”的核心论断。

### 投票式图像评判：面向协同任务的自动化评估

由于UEG和GEU任务涉及复杂生成图像的准确性判断——如属性绑定、数量控制、空间关系等——传统自动化指标（如FID、CLIPScore）无法有效评估。RealUnify设计了**验证问题驱动的投票式评判方法**：针对每张生成图像，构造一组可自动验证的是非问题（如“图中是否恰好有三个红色立方体？”），并利用**Gemini 2.5 Pro**作为评判模型进行回答。与人类专家评估的一致性验证（Table 4）表明，该方法在保持可扩展性的同时，达到了可接受的可靠性水平，为大规模协同能力评估提供了实用方案。



RealUnify 并非一个模型，而是一个**面向统一模型能力协同的双评估基准**。其整体框架围绕一个核心诊断问题构建：当前统一模型是否真正实现了理解与生成能力的双向增强，还是仅仅在架构层面完成了功能堆叠？为此，RealUnify 设计了三个相互衔接的模块，形成从任务定义到瓶颈诊断的完整评估链路。

### 任务定义层：UEG 与 GEU 双向协同

RealUnify 将评估任务划分为两大类别（**Figure 2**）：

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/003_Figure_2.jpg]]
*Figure 2: Overview of RealUnify. The benchmark includes 2 task categories: Understanding Enhances Generation (UEG) and Generation Enhances Understanding (GEU), encompassing 10 task types. Hints are provided to guide task decomposition in the stepwise evaluation*

- **理解增强生成（Understanding Enhances Generation, UEG）**：考察模型是否能够利用其理解与推理能力来提升图像生成的准确性。任务要求模型首先对提示进行深度解读（如世界知识、常识推理、数学推理、逻辑推理、科学推理、代码转图像），再据此生成符合约束的图像。
- **生成增强理解（Generation Enhances Understanding, GEU）**：考察生成能力是否能反哺理解过程。任务要求模型通过生成图像来辅助认知（如心理重建、心理追踪、注意力聚焦、认知导航），本质上是“以图助思”。

这两类任务的设计意图是捕捉理解与生成之间**双向信息流**的有效性，而非孤立地评测单一能力。

### 评估协议层：直接评估与逐步分解的双重诊断

RealUnify 的核心方法论创新在于其**双评估协议（dual-evaluation protocol）**：

- **直接评估（Direct Evaluation）**：以端到端方式评测统一模型在 UEG 和 GEU 任务上的整体表现，回答“统一模型能否直接解决需要能力协同的复杂任务”。
- **逐步分解评估（Stepwise Evaluation）**：将每个任务显式拆解为理解阶段与生成阶段，分别提供中间提示（hints），引导模型分步执行。这一设计的目的是**诊断性能瓶颈的位置**——如果逐步分解后性能显著提升，说明模型内部具备相关知识但无法在端到端场景中自主整合；如果性能反而下降，则揭示生成能力对理解过程的干扰。

两种协议的结果对比构成了 RealUnify 对“能力协同真实性”的核心判据。

### 评判层：投票式图像评估

对于生成图像的自动化质量评判，RealUnify 采用**投票式评估（polling-based evaluation）**（**Figure 3**）。具体而言，系统针对生成图像设计验证问题（verification questions），并利用 Gemini 2.5 Pro 作为评判模型进行投票判定。实验表明，Gemini 2.5 Pro 与人类专家评价的一致性显著优于 Qwen2.5-VL 等替代评判器（**Table 4**），为自动化评估的可靠性提供了支撑。

### 数据构建与质量保障

RealUnify 包含 **1,000 个人工标注实例**，覆盖 10 个类别、32 个子任务（**Figure 4**），其中 UEG 任务 600 个，GEU 任务 400 个。数据收集自多个来源，经过 10 位人类专家的多轮交叉审核，确保任务设计的合理性与标注质量。

### 模块间的逻辑流

整个框架的评估流程如下：给定一个需要理解与生成协同的复杂任务 → 首先通过直接评估获取端到端性能 → 再通过逐步分解评估将任务解耦为理解子问题和生成子问题 → 对比两种协议下的性能差异 → 结合投票式评判对生成结果进行自动化评分 → 最终输出关于模型“能力协同”状态的诊断结论。这一流程将“统一模型是否真正受益于统一”这一抽象问题，转化为可量化、可归因的实证判断。

### 补充图表

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of RealUnify. Unlike benchmarks focused on either understanding or generation (Stage 1), those that merely integrate both capabilities (Stage 1.5), or even those that preliminarily explore the mutual enhancement between understanding and generation (Stage 2), RealUnify stands as the first benchmark to comprehensively evaluate and fully harness the synergy between these capabilities, making it a pioneering effort in assessing ability synergy for unified models*



RealUnify 本身是一个基准测试，不提出新的模型架构或训练公式，其核心贡献在于设计了一套系统性的评估协议与数据集构建流程。以下梳理其关键方法模块。

### 双评估协议

RealUnify 的方法核心是**双评估协议（Dual-Evaluation Protocol）**，包含直接评估与逐步分解评估两种模式，旨在诊断统一模型是否真正实现了理解与生成能力的协同，而非仅仅在功能上并存。

- **直接评估（Direct Evaluation）**：端到端地衡量统一模型在 UEG 和 GEU 任务上的整体表现，考察统一架构是否带来显著的性能增益。
- **逐步分解评估（Stepwise Evaluation）**：将复杂任务拆解为独立的视觉理解子问题和图像生成子问题，分阶段执行。对于 UEG 任务，先由模型输出对提示的理解结果，再基于该理解生成图像；对于 GEU 任务，则先由模型生成辅助图像，再基于该图像进行理解推理。该设计的关键在于：若分解后性能提升，说明模型具备相关知识但无法在端到端场景中有效整合；若分解后性能下降，则说明生成与理解之间存在负向干扰或能力短板。

### 投票式图像评判模块

为客观评估生成图像的质量，RealUnify 设计了**投票式评判机制（Polling-Based Evaluation）**。具体流程为：

1. 针对每个生成任务设计一组验证问题（Verification Questions），用于检测生成图像是否满足提示中的约束条件。
2. 使用 Gemini 2.5 Pro 作为评判模型，对验证问题进行回答。
3. 通过多问题投票聚合的方式判定生成图像的正确性。

该模块本质上是一个基于大模型的自动评估管线，其可靠性通过 Table 4 中与人类专家评判的一致性验证——Gemini 2.5 Pro 与人类专家评价的一致性显著高于 Qwen2.5-VL 等替代评判模型。

### 数据集构建管线

RealUnify 的数据集构建遵循严格的人工标注与审核流程：

- 从多个来源收集原始数据，由 10 位人类专家进行标注。
- 经过多轮交叉审核（cross-check），最终形成 1000 个高质量实例，覆盖 10 个类别、32 个子任务。
- 600 个实例属于 UEG 类别，400 个属于 GEU 类别，每个实例均配有用于逐步分解评估的提示（Hints）。

### 公式推导

RealUnify 作为基准测试，未引入新的数学公式或理论推导。其评估指标为准确率（Accuracy），即模型在验证问题上回答正确的比例，不涉及自定义损失函数或优化目标。论文中所有定量结果均以准确率百分比形式呈现，无独立公式推导部分。

> **注意**：若需了解被评估的统一模型（如 BAGEL、UniPic2 等）的内部公式，需查阅其原始论文，RealUnify 本身不包含此类内容。

### 补充图表

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of polling evaluation. To assess the accuracy of the generated images, we design verification questions and employ Gemini 2.5 Pro as the judge in a polling-based evaluation*



## 实验与关键发现

### 核心发现：统一模型的能力协同瓶颈

RealUnify 通过在 1,000 个人工标注实例上对 7 个统一模型进行双协议评估，揭示了一个关键矛盾：**架构统一并不自动带来理解与生成能力的协同**。在直接评估（端到端）下，表现最佳的开源统一模型 **UniPic2** 在 UEG 任务上的平均准确率仅为 37.5%，而最佳商用统一模型 **Nano Banana**（基于 Gemini 2.5 Flash Image）达到 63.0%（见 Table 2）。在 GEU 任务上，最佳统一模型 **BAGEL** 仅取得 39.3%，远低于专用视觉理解模型 **Gemini 2.5 Pro** 的 54.8%（见 Table 3）。

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/006_Table_2.jpg]]
*Table 2: Evaluation results on RealUnify. WR: World Knowledge; CR: Commonsense Reasoning; MR-I: Mathematical Reasoning; LR: Logical Reasoning; SR: Scientific Reasoning; C2T: Code-to-Image; MR-II: Mental Reconstruction; MT: Mental Tracking; AF: Attentional Focusing; CN: Cognitive Navigation. For each task, we present both direct and stepwise evaluation results, reported in the format direct/step. The best performance on each task is in blue*

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/008_Table_3.jpg]]
*Table 3: Performance comparison of unified models and specialized models. We report results by selecting the top-3 performing unified models based on their overall performance in UEG and GEU and comparing them against specialized models*

这一差距的根源在于：统一模型内部虽然分别具备理解能力和生成能力，但缺乏将两者有效整合的机制。逐步分解评估协议为这一诊断提供了决定性证据。

### 双协议评估揭示的双重模式

RealUnify 的核心方法创新在于其**双评估协议**：直接评估测量端到端能力协同，逐步评估则将任务分解为理解子任务和生成子任务，以诊断瓶颈所在。

**UEG 任务（理解增强生成）**：逐步分解后，所有模型性能均提升。其中 **BAGEL** 提升最为显著，从直接评估的 32.7% 跃升至 47.7%（+15.0 个百分点）。这表明模型具备完成任务所需的理解能力，但在端到端场景中无法有效将理解结果转化为精确的生成指令。

**GEU 任务（生成增强理解）**：情况截然相反。逐步分解后，所有模型性能反而下降。这一反直觉的结果说明，GEU 任务的核心挑战不在于生成图像本身，而在于将生成结果作为推理的中间媒介——模型需要“以图助思”，而当前的统一模型在生成-理解循环中无法维持连贯的推理链。

### 与专用模型的对比：Oracle 实验

为量化统一模型的协同上限，研究者构造了一个 **Oracle 模型**：将最佳专用理解模型 **Gemini 2.5 Pro**（Gemini Team, 2025）与最佳专用生成模型 **GPT-Image-1**（OpenAI, 2025）以逐步方式组合。该 Oracle 在 UEG 任务上达到 72.7%，远超最佳统一模型 Nano Banana 的 63.0%（+9.7 个百分点，见 Table 5）。这一结果表明，即使使用当前最强的专用模型组合，统一模型的能力协同仍有显著提升空间——但关键在于，这种协同需要超越简单的流水线拼接。

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/009_Table_5.jpg]]
*Table 5: Comparisons with Gen-Und SOTA*

### 评估可靠性验证

为验证基于生成图像的评估可靠性，RealUnify 采用**投票式图像评判**方法：设计验证问题，由评判模型判断生成图像是否满足约束。Table 4 显示，**Gemini 2.5 Pro** 作为评判模型与人类专家评价的一致性最高，在 Nano Banana 上分别为 63.0 和 59.3，在 BAGEL 上分别为 32.7/47.7 和 31.5/44.2（直接/逐步）。相比之下，**Qwen2.5-VL** 与人类专家的一致性较弱。这一验证为基准测试结果的可靠性提供了支撑，但需注意单一评判模型可能引入系统性偏差。

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/007_Table_4.jpg]]
*Table 4: Comparisons of different judges. We assess the quality of the models’ generated images with different judges, and the results are reported in the direct/step format*

### 典型失败模式

定性分析（Figure 11、Figure 12）揭示了统一模型在图像生成中的常见失败模式：

- **属性纠缠**：模型无法将多个独立属性正确绑定到同一对象，例如要求“红色圆形和蓝色方形”时生成颜色形状错配的图像。
- **数量控制失败**：在需要精确计数的场景中，模型生成的物体数量与指令不符。
- **空间关系错误**：模型难以维持物体间的相对位置关系，如“A 在 B 的左边”被生成为上下排列。
- **推理链断裂**：在 GEU 任务中，即使逐步分解提供了中间结果，模型仍无法基于生成图像完成后续推理（Figure 6）。

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/011_Figure_6.jpg]]
*Figure 6: Challenging examples of stepwise execution in task solving. Despite using a stepwise approach, the unified model struggles to complete complex tasks, only succeeding with intermediate results based on the given ground truth*

这些失败模式直接印证了核心瓶颈：统一模型缺乏促进理解与生成双向交互的训练目标与归纳偏置，导致两种能力在端到端场景中无法协同使用。

### 数据集统计与任务分布

RealUnify 数据集包含 600 个 UEG 实例和 400 个 GEU 实例，覆盖 10 个类别、32 个子任务（Figure 4、Table 6）。UEG 类别涵盖世界知识、常识推理、数学推理、逻辑推理、科学推理和代码到图像；GEU 类别包括心理重建、心理追踪、注意力聚焦和认知导航。每个任务均在直接和逐步两种设置下评估，逐步评估进一步将过程分解为视觉理解问题和生成问题。

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/005_Figure_4.jpg]]
*Figure 4: Statistics of RealUnify. The tasks span 10 categories, divided into two groups: UEG and GEU, including 32 subtasks*

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/016_Table_6.jpg]]
*Table 6: Distribution of task instances across different categories in RealUnify. Each task is evaluated under both direct and stepwise settings, where stepwise evaluation further decomposes the process into a visual understanding problem and a generation problem*

### 局限性与开放问题

当前评估存在以下局限：（1）数据集语言限定为英文，可能限制多语言泛化性；（2）部分统一模型不支持图像编辑，导致 GEU 逐步评估结果缺失；（3）任务设计主要针对静态图像，未涵盖视频或交互式场景。核心开放问题在于：如何设计训练策略和模型架构，使统一模型能够在端到端场景中真正整合理解与生成能力，尤其是提升属性绑定、数量控制和空间关系精度，使“以图助思”的 GEU 范式更为有效。

### 补充图表

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/010_Figure_5.jpg]]
*Figure 5: Effective examples of stepwise execution in task solving. Through the unified model’s inherent understanding and generation abilities, the model is able to implement complex tasks*

![[assets/figures/papers/paper_list_l780_https_arxiv_org_abs_2509_24897/figures/002_Table_1.jpg]]
*Table 1: Comparisons on RealUnify and other benchmarks. RealUnify is designed to provide a comprehensive evaluation of unified models across multiple dimensions. It is entirely human-annotated and integrates both direct and stepwise evaluation protocols. RealUnify centers on evaluating whether the synergy between generation and understanding can be effectively harnessed to solve complex tasks*



## 定位与知识库关联

### 1. 统一模型的演进与RealUnify的定位

当前的多模态基准测试可大致分为三个阶段（见 Figure 1）。**第一阶段**的基准仅孤立地评估理解或生成能力，例如传统的VQA、图像描述或图像生成质量评分。**第二阶段**（论文称为“Stage 1.5”）的基准开始将理解与生成任务放在同一框架下，但并未考察两者之间的交互与协同。**第三阶段**的基准初步探索了理解与生成之间的相互增强，但仍停留在浅层关联。

RealUnify将自身定位为**第四阶段的基准**——首次系统性地评估统一模型中理解与生成能力的**深度协同**。其核心问题不是“模型能否同时完成理解和生成任务”，而是“统一架构是否真正实现了两种能力的双向赋能”。这一视角将评估焦点从**能力并存**转向**能力融合**，构成了RealUnify与所有先前基准的根本分界线（Table 1提供了与现有基准的系统对比）。

### 2. 与专用模型的对比：能力协同的“天花板”

RealUnify通过构建“oracle”模型，为统一模型的能力协同设定了参照上限。该oracle由当前最强的专用模型组合而成：**Gemini 2.5 Pro**（Gemini Team, 2025）负责视觉理解，**GPT-Image-1**（OpenAI, 2025）负责图像生成。在UEG任务上，该组合以逐步方式运作，达到72.7%的准确率，显著优于最佳统一模型**Nano Banana**（63.0%）和最佳开源统一模型**UniPic2**（37.5%）（Table 5）。

这一差距揭示了当前统一模型的核心瓶颈：**架构统一不等于能力协同**。专用模型组合之所以更强，并非因为单个模型的能力绝对领先，而是因为逐步分解范式允许理解模型充分提取语义信息后，再交由生成模型精确执行。统一模型虽在单一能力上可能接近专用模型，但在需要两者深度交互的端到端场景中，缺乏有效的内部协调机制。

### 3. 关键基线模型及其在基准中的表现

RealUnify评估了多类统一模型，包括开源和商用系统：

- **BAGEL-7B**：开源统一模型，在直接评估中UEG准确率仅32.7%，但逐步分解后提升至47.7%（+15.0个百分点），是所有模型中提升幅度最大的。这表明BAGEL内部拥有相关知识，但无法在端到端场景中有效调用。
- **Nano Banana（Gemini 2.5 Flash Image）**：商用统一模型，在UEG上达到63.0%的总体准确率，是所有统一模型中表现最好的。但在GEU任务上，其表现仍不及专用模型**Gemini 2.5 Pro**（54.8% vs. 统一模型最佳39.3%，见Table 3）。
- **UniPic2**：最佳开源统一模型，UEG直接评估准确率37.5%。
- **OneCAT** 和 **OmniGen2**：其他开源统一模型，整体表现更为有限。

### 4. 适用边界与评估协议的局限

RealUnify的双评估协议（直接评估 + 逐步分解评估）是其方法论的核心创新，但也界定了其适用边界：

1. **逐步分解范式的假设**：逐步评估通过将UEG/GEU任务显式分解为理解和生成两个阶段来诊断瓶颈。这一设计隐含假设了任务可被清晰分解，但对于某些高度耦合的协同任务，强制分解可能改变任务本质，导致评估结果无法完全反映端到端协同的真实潜力。

2. **评判模型的系统性偏差**：RealUnify使用**Gemini 2.5 Pro**作为图像质量的投票式评判器。尽管Table 4显示其与人类专家评估的一致性高于**Qwen2.5-VL**，但任何自动评判都可能引入系统性偏差，尤其是在评估主观性或创造性较强的生成结果时。

3. **数据集的语言与模态限定**：数据集语言限定为英文，任务设计针对静态图像，未涵盖视频、交互式场景或多语言情境。这限制了结论向更广泛真实场景的泛化。

4. **GEU评估的模型覆盖缺口**：部分统一模型不支持图像编辑功能，导致GEU逐步评估结果缺失（Table 2中部分条目为“-”），可能影响GEU相关结论的普遍性。

### 5. 核心发现的双重模式及其启示

RealUnify揭示了理解与生成协同的**非对称性**：

- **UEG方向**：逐步分解后所有模型性能提升，说明统一模型具备理解能力，但无法在生成过程中有效利用。瓶颈在于**能力整合**，而非能力缺失。
- **GEU方向**：逐步分解后所有模型性能反而下降。这表明在“以图助思”的场景中，生成能力的引入反而干扰了理解过程，统一模型缺乏有效的**生成-理解反馈回路**。

这一双重模式构成了RealUnify最核心的洞察：**统一模型拥有相关知识，但缺乏将知识转化为协同行为的机制**。这为未来的训练策略和架构设计指明了方向——需要设计明确的训练目标来促进理解与生成之间的双向信息流动。

### 6. 开放问题

1. **训练策略设计**：如何设计训练目标（如跨模态对比损失、循环一致性约束）和归纳偏置，使统一模型在端到端场景中真正实现理解与生成的协同，而非仅靠逐步分解“绕过”整合瓶颈？

2. **GEU的架构支持**：如何提升生成能力以服务于理解任务？当前GEU逐步分解后性能下降的现象暗示，生成模块的输出可能引入了噪声或干扰，需要新的架构机制使生成结果成为理解的“支架”而非“障碍”。

3. **复杂推理与生成精度的联合提升**：统一模型在属性绑定、数量控制、空间关系等生成精度问题上仍然存在典型缺陷（见Figure 11、Figure 12），这些问题在需要深度推理的UEG任务中被进一步放大。如何在保持统一架构的同时提升这些基础生成能力？

4. **更优的协同评估协议**：逐步分解范式虽能诊断瓶颈，但其人工设计的分解路径可能不是模型内部最优的协同方式。是否存在更自然的评估协议，能够在不强制分解的情况下度量能力协同的深度？



## 原文 PDF

![[paperPDFs/CVPR_2026/RealUnify_Do_Unified_Models_Truly_Benefit_from_Unification_A_Comprehensive_Benchmark.pdf]]
