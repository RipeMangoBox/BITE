---
title: "UniM: A Unified Any-to-Any Interleaved Multimodal Benchmark"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniM_A_Unified_Any_to_Any_Interleaved_Multimodal_Benchmark.pdf
project_link: "https://any2any-mllm.github.io/unim"
code_link: null
aliases:
- UniM
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 可追溯证据推理模块（Traceable Evidence Reasoning）通过显式的步骤规划、验证和回溯修正，强制模型在生成前构建结构化的逻辑链，从而提升交织输出的结构完整性和语义一致性。
primary_logic: 构建首个支持任意7种模态任意交织的大规模基准UNIM，并设计三维度评估套件；同时提出基于智能体框架的基线模型UNIMA，其核心是可追溯证据推理链，将隐式思维链转化为显式、可验证的推理步骤。
claims:
- UNIM是首个统一任意到任意交织多模态基准，包含31K实例，覆盖30个领域和7种模态。
- 基线模型在UNIM上绝对得分极低（SQCS多低于20%，StS/LeS多低于5%），而UNIMA大幅领先（SQCS约60%，ICS接近70%）。
- 消融实验证实TER模块对结构完整性起决定性作用（去除后StS下降36.3，LeS下降60.8），验证子模块对整体可靠性至关重要。
- UNIM (General Area) 上 SQCS (Semantic Correctness & Generation Quality) = 62.2
---

# UniM: A Unified Any-to-Any Interleaved Multimodal Benchmark

> [!tip] 核心洞察
> 构建首个支持任意7种模态任意交织的大规模基准UNIM，并设计三维度评估套件；同时提出基于智能体框架的基线模型UNIMA，其核心是可追溯证据推理链，将隐式思维链转化为显式、可验证的推理步骤。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniM：面向任意到任意交织多模态的统一基准 |
| 英文题名 | UniM: A Unified Any-to-Any Interleaved Multimodal Benchmark |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05075) · [Project](https://any2any-mllm.github.io/unim) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | UNIMA |
| Dataset | UNIM |

> [!tip] 效果简介
> - UNIM (General Area) 上，SQCS (Semantic Correctness & Generation Quality) 62.2 vs 21.2 (MIO), 4.4 (NExT-GPT), 17.9 (AnyGPT) (+41.0 over MIO)。
> - UNIM (Overall) 上，StS (Strict Structure Score) 71.3 (General Area) vs 12.5 (AnyGPT), 2.2 (NExT-GPT), 3.3 (MIO) (+58.8 over AnyGPT)；LeS (Lenient Structure Score) 84.3 (General Area) vs 16.4 (AnyGPT), 2.5 (NExT-GPT), 3.8 (MIO) (+67.9 over AnyGPT)；ICS (Interleaved Coherence Score) 69.8 (General Area) vs 43.6 (AnyGPT), 28.1 (NExT-GPT), 60.0 (MIO) (+9.8 over MIO)。

## 概述

### 问题背景

当前多模态大语言模型（MLLM）的研究正从单一模态理解走向任意到任意（any-to-any）的交织多模态生成。然而，现有交织多模态基准测试存在两个根本性瓶颈：一是仅覆盖文本和图像两种模态，无法评估模型在音频、视频、文档、代码、3D等更广泛模态组合上的表现；二是评估维度单一，仅关注语义正确性，忽略了响应结构完整性和交织连贯性这两个反映真实交织推理复杂性的关键维度。这些不足导致社区缺乏一个统一的标尺来衡量模型在任意模态组合下的综合能力。

### 核心贡献

针对上述问题，本文提出两项核心贡献：

**UNIM基准**：首个统一任意到任意交织多模态基准，包含31K高质量实例，覆盖30个领域和7种代表性模态（文本、图像、音频、视频、文档、代码、3D）。UNIM采用开放式问答格式，输入或输出为任意模态交织的序列，并设计了三维度评估套件——语义正确性与生成质量（SQCS）、响应结构完整性（StS/LeS）和交织连贯性（ICS），结合支持率（τ）实现公平的绝对与相对性能比较。

**UNIMA基线模型**：基于智能体框架的基线模型，其核心创新是可追溯证据推理模块（Traceable Evidence Reasoning, TER）。TER将传统隐式思维链（Chain-of-Thought）转化为显式、可验证的结构化证据推理链（SERC），通过“规划—验证—回溯修正—再生成”循环，强制模型在生成前构建可靠的逻辑链，从而大幅提升交织输出的结构完整性和语义一致性。

### 关键发现

在UNIM基准上的实验揭示了以下核心结论：

1. **现有模型能力严重不足**：**AnyGPT**、**NExT-GPT**、**MIO**等代表性任意到任意MLLM在UNIM上表现极差，语义得分（SQCS）普遍低于20%，结构完整性得分（StS/LeS）多低于5%，表明现有模型几乎无法处理复杂的交织多模态任务。

2. **UNIMA大幅领先**：UNIMA在各项指标上远超基线模型，其中结构完整性得分（StS/LeS）是AnyGPT的2–6倍，是NExT-GPT和MIO的15–40倍；语义得分（SQCS）达到约60%，较最强基线MIO提升约41个百分点；交织连贯性得分（ICS）接近70%。

3. **可追溯推理是性能瓶颈的因果关键**：消融实验证实，TER模块对结构完整性起决定性作用——去除整个SERC推理链后，StS下降36.3个百分点，LeS下降60.8个百分点，呈现结构性崩溃。验证子模块的移除同样导致所有指标显著下降（SQCS -12.2, ICS -8.7, StS -14.4, LeS -15.8），证明“检查—回溯—再生成”设计对可靠交织输出至关重要。

### 方法谱系与知识库定位

UNIMA的方法定位处于“智能体框架下的多模态推理与生成”这一新兴谱系。与传统端到端MLLM（如**NExT-GPT**、**MIO**）依赖隐式思维链和独立模态编码器不同，UNIMA引入了两个关键设计变更：

- **推理机制**：从隐式思维链升级为显式可追溯证据推理链（SERC），包含验证—回溯—再生成循环。
- **模态理解前端**：从独立模态编码器转变为任务条件稠密描述（TCDC），将非文本模态统一为任务相关的文本表征，为后续推理提供语义基础。

这一设计将多模态推理从“黑箱生成”转变为“可验证的规划执行”范式，在交织多模态任务上实现了结构完整性和语义一致性的质变式提升。

## 背景与动机

### 交织多模态：从单模态到任意模态组合的范式跃迁

现实世界的交互天然是多模态交织的。人类在对话中自由切换文字、图像、语音、视频，信息并非孤立模态的简单拼接，而是以交织序列的形式动态组合。然而，当前的多模态大语言模型（MLLMs）大多仍局限于“文本+图像”的双模态范式，即便部分模型宣称支持任意到任意（any-to-any）生成，其评估基准却远远滞后——现有交织多模态基准仅覆盖文本和图像两种模态，缺乏对任意模态组合的统一评估，且评估维度单一，无法反映真实交织推理的复杂性。

Figure 1 展示了任意到任意交织多模态范式的典型应用场景：从多模态内容创作、跨模态信息检索到复杂推理问答，每个实例都需要模型同时具备多模态理解、跨模态对齐、结构化生成和逻辑推理的组合能力。这种“组合能力”正是当前基准和模型的双重盲区。

### 现有基准的结构性缺失

Table 1 将 UNIM 与现有交织多模态基准进行了系统对比。现有基准存在三个结构性缺陷：

1. **模态覆盖狭窄**：主流基准仅支持文本和图像两种模态，无法评估模型对音频、视频、文档、代码、3D 等模态的理解与生成能力。
2. **能力维度单一**：现有评估通常只关注语义正确性或生成质量中的某一维度，忽视了交织输出的结构完整性和模态间连贯性——这两个维度恰恰是任意到任意交织任务的核心挑战。
3. **难度分层缺失**：缺乏对任务难度的系统分类，无法区分模型在不同复杂度场景下的表现差异，也难以定位能力瓶颈。

### 模型能力的现实困境

即便是在有限的“文本+图像”交织场景中，现有任意到任意多模态大语言模型的表现也远未达到可用水平。以 AnyGPT、NExT-GPT 和 MIO 为代表的现有模型，在 UNIM 基准上的绝对得分极低：语义正确性与生成质量耦合得分（SQCS）多低于 20%，严格结构得分（StS）和宽松结构得分（LeS）多低于 5%。这意味着现有模型几乎无法生成符合指定模态类型和数量的交织输出——它们要么“说了正确的话但用错了模态”，要么“模态对了但内容完全偏离”。

这一困境的根源在于：现有模型普遍依赖**隐式思维链（Chain-of-Thought）**进行推理，模型在生成交织输出时缺乏对模态序列的结构化规划，也缺乏对中间推理步骤的可验证性约束。当任务要求“先用文字分析图像，再生成一段对应的音频，最后用代码展示计算结果”时，隐式推理链极易在模态切换处断裂，导致输出结构混乱或语义漂移。

### 本文动机与核心主张

针对上述双重缺口——基准缺失与模型能力不足——本文提出两个核心贡献：

- **UNIM 基准**：首个统一任意到任意交织多模态基准，包含 31K 高质量实例，覆盖 30 个领域和 7 种模态（文本、图像、音频、视频、文档、代码、3D），并设计三维度评估套件（语义正确性与生成质量、响应结构完整性、交织连贯性），系统衡量模型的综合交织能力。
- **UNIMA 基线模型**：基于智能体框架的任意到任意交织多模态基线，其核心创新是**可追溯证据推理模块（Traceable Evidence Reasoning, TER）**——将隐式思维链转化为显式、可验证、可回溯修正的结构化推理链，强制模型在生成前构建可靠的逻辑基础，从而大幅提升交织输出的结构完整性和语义一致性。

## 核心创新

UNIMA 的核心创新在于将隐式思维链重构为**显式、可验证、可回溯的结构化推理链**，并通过**任务条件稠密描述**统一异构模态的语义表征，从而系统性地解决了现有任意到任意多模态模型在交织输出中结构混乱、语义断裂的根本问题。以下从三个关键变更槽位展开分析。

### 推理机制：从隐式思维链到可追溯证据推理链（SERC）

现有基线模型（如 **AnyGPT**、**NExT-GPT**、**MIO**）普遍依赖隐式的 Chain-of-Thought 进行跨模态推理，其推理过程不可验证、不可回溯，一旦中间步骤出错，错误将直接传播至最终输出。UNIMA 提出的 **Traceable Evidence Reasoning (TER)** 模块从根本上改变了这一范式：它建立了一条显式的、以证据为基础的可追溯推理链（Structured Evidence-grounded Reasoning Chain, SERC）。

SERC 包含四个结构化步骤：**步骤规划 → 证据收集 → 推理合成 → 验证与回溯修正**。其中，验证子模块内嵌了一个“检查器-判定器”循环——检查器评估推理步骤与证据的一致性，判定器决定是否接受当前步骤或触发回溯再生成。这一设计将推理过程从“黑箱”转变为“白箱”，使模型在生成最终报告前必须通过自我验证的关卡。

消融实验为这一创新的决定性作用提供了强证据：去除整个 SERC 推理链后，严格结构得分（StS）从 52.7 骤降至 16.4（-36.3），宽松结构得分（LeS）从 82.6 跌至 21.8（-60.8），结构指标近乎崩溃。进一步地，仅禁用验证子模块也导致所有指标显著下降：SQCS -12.2，ICS -8.7，StS -14.4，LeS -15.8。这证实了“检查-回溯-再生成”循环对可靠交织输出至关重要，而非仅仅是推理链存在的边际收益。

### 模态理解前端：从独立编码到任务条件稠密描述（TCDC）

现有基线模型通常使用独立的模态编码器将图像、音频、视频等分别映射到各自的隐空间，再通过连接器桥接到语言模型。这种方式存在两个瓶颈：一是不同模态的隐空间表征难以对齐，二是编码过程与下游任务需求脱节，导致语义信息在跨模态传递中衰减。

UNIMA 的 **Receiving Module** 采用了一种根本不同的策略——**任务条件稠密描述（Task-Conditioned Dense Caption, TCDC）**。它调用专用工具（如 GPT-5 mini 处理图像/文档/代码，Qwen3-Omni Thinker 处理音频/视频）将非文本模态统一转换为任务相关的文本描述，形成一个统一的文本语义空间供后续推理使用。这一设计的核心洞察是：**将异构模态的“理解”问题转化为同构文本空间中的“推理”问题**，从而绕开了跨模态隐空间对齐的固有困难。

消融实验显示，用无条件描述替换 TCDC 后，SQCS 下降 6.7，ICS 下降 5.7，表明任务感知的语义基础对语义正确性和交织连贯性具有实质性影响。值得注意的是，TCDC 对结构指标（StS/LeS）的影响相对较小，这与其主要作用于语义层面而非结构层面的设计预期一致。

### 生成控制：从直接解码到经验证报告驱动的分步生成

基线模型的生成过程通常是端到端的：解码器直接根据隐式推理状态逐 token 生成多模态输出序列。这种方式缺乏对输出结构的全局规划，容易产生模态错位、数量不匹配等结构性问题。

UNIMA 的 **Generating Module** 将生成控制权交给了 TER 模块产出的**经验证的最终报告**。该报告明确规定了每个模态片段的类型、内容和插入位置，生成模块据此按计划调用对应的生成工具，分步产生各模态内容并插入指定占位符。这种“先规划、后执行”的解耦设计，使得结构完整性（StS/LeS）的大幅提升成为可能——UNIMA 在 General Area 上的 StS 达到 71.3，而最强基线 AnyGPT 仅为 12.5，差距高达 58.8 个百分点。

### 创新协同效应

上述三个变更槽位并非孤立创新，而是形成了紧密的因果链条：TCDC 提供任务感知的统一语义基础 → SERC 在此基础上进行可验证的结构化推理并生成最终报告 → 生成模块严格按报告执行输出。这一链条解释了为何 UNIMA 在三个评估维度上均大幅领先基线：语义正确性（SQCS 62.2 vs. 基线最高 21.2）、结构完整性（StS/LeS 领先 2–40 倍）、交织连贯性（ICS 69.8 vs. 基线最高 60.0）同时获得显著提升。

## 整体框架

UNIMA 是一个面向任意到任意交织多模态任务的智能体框架，其核心设计目标是将隐式的多模态推理过程转化为显式、可验证的结构化推理链。整个框架由三个功能模块串联构成，形成“感知—推理—生成”的闭环流水线。

### 流水线总览

如图 4 所示，UNIMA 的输入和输出均为任意模态交织的序列——文本、图像、音频、视频、文档、代码和三维模型等七种模态可以任意组合出现。非文本模态在序列中以占位符标签（如 `<image1>`、`<video2>`）表示。整个处理流程分为三个阶段：

1. **接收模块（Receiving Module）**：将输入中的非文本模态统一转换为任务条件稠密描述（TCDC），形成统一的文本表征空间，供后续推理使用。
2. **可追溯证据推理模块（Traceable Evidence Reasoning, TER）**：在统一的文本空间上执行结构化证据推理链（SERC），通过规划、验证、回溯修正等步骤生成可靠的最终报告。
3. **生成模块（Generating Module）**：以最终报告为驱动，调用对应的模态生成工具，在指定位置插入生成内容，形成完整的交织多模态输出。

### 模块间关系与数据流

三个模块之间的数据流是严格单向且可追溯的。接收模块的输出是任务条件稠密描述，这是 TER 模块的唯一输入；TER 模块输出的最终报告包含了对每个输出片段的生成指令和占位符位置信息；生成模块则完全依据最终报告执行，不再进行额外的推理或决策。这种设计确保了推理过程的可追溯性——最终输出的每一个模态片段都可以回溯到 TER 模块中的具体推理步骤和验证记录。

### 接收模块：任务条件稠密描述（TCDC）

接收模块集成了四个专用工具来处理不同类型的输入模态：GPT-5 mini 负责文本、图像、文档和代码的理解，Qwen3-Omni Thinker 专门处理音频和视频理解。与传统的独立模态编码器不同，TCDC 的关键创新在于其“任务条件”特性——描述内容不是通用的模态转写，而是根据下游任务需求定向提取的语义信息。这一设计使得后续推理模块能够获得与任务高度相关的证据基础，消融实验表明，用无条件描述替换 TCDC 会导致语义正确性（SQCS）下降 6.7、交织连贯性（ICS）下降 5.7，证实了任务感知的语义基础对整体性能的重要影响。

### TER 模块：结构化证据推理链（SERC）

TER 模块是 UNIMA 的核心创新，其内部包含一个四步结构化证据推理链：

1. **步骤规划**：将复杂任务分解为有序的子步骤序列。
2. **证据收集**：针对每个子步骤，从 TCDC 中提取相关证据。
3. **验证与判定**：内嵌的检查器-判定器循环对推理结果进行验证，若发现不一致或证据不足，触发回溯修正。
4. **最终报告生成**：将经过验证的推理结果整合为结构化的最终报告，明确每个输出片段的模态类型、内容和位置。

去除整个 SERC 推理链会导致结构指标崩溃——严格结构得分（StS）从约 52% 降至 16%（-36.3），宽松结构得分（LeS）从约 82% 降至 21%（-60.8），充分说明显式推理链对结构完整性的决定性作用。进一步地，禁用验证子模块也会导致所有指标的显著下降（SQCS -12.2，ICS -8.7，StS -14.4，LeS -15.8），证明检查-回溯-再生成的设计是可靠交织输出的关键保障。

### 生成模块：报告驱动的模态生成

生成模块本身不进行语义决策，而是忠实地执行最终报告中的指令。它根据报告中指定的模态类型调用对应的生成工具（如图像生成模型、音频合成模型等），将生成内容插入到对应的占位符位置，最终拼装成完整的交织多模态输出。这种“推理与生成分离”的设计使得推理链的质量可以独立评估和优化，同时保证了输出格式的精确可控。

### 补充图表

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/006_Figure_4.jpg]]
*Figure 4: Overview of the UNIMA architecture*

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the any-to-any interleaved multimodal paradigm with different real-world application scenarios. Solving any-to-any interleaved multimodal learning requires complex and combined capabilities*

## 核心模块与公式推导

### UNIMA 三大核心模块

UNIMA 采用模块化的 Agent 框架，将任意到任意交织多模态任务拆解为三个协同工作的核心模块，如 Figure 4 所示。

**接收模块（Receiving Module）** 负责将非文本输入统一转化为任务感知的文本表征。该模块集成了四个专用工具：GPT-5 mini 处理文本、图像、文档和代码理解，Qwen3-Omni Thinker 专注于音频和视频理解。其核心输出是**任务条件稠密描述（TCDC）**——将图像、音频、视频等非文本模态转换为与当前任务上下文紧密相关的文本描述，而非通用字幕。这一设计使得后续推理模块可以在统一的文本空间中操作，避免了独立模态编码器带来的语义对齐困难。

**可追溯证据推理模块（Traceable Evidence Reasoning, TER）** 是整个架构的核心创新。与传统方法依赖隐式思维链（Chain-of-Thought）不同，TER 构建了一条显式的、可验证的结构化证据推理链（Structured Evidence Reasoning Chain, SERC），包含四个步骤：
1. **规划（Plan）**：根据任务要求制定推理步骤蓝图；
2. **验证（Verify）**：通过内嵌的检查器-判定器循环对中间推理步骤进行验证；
3. **回溯（Backtrack）**：若验证未通过，回溯修正推理路径；
4. **再生成（Regenerate）**：基于修正后的证据链重新生成结论。

这一“验证-回溯-再生成”循环确保最终报告具有高度的逻辑可靠性和结构完整性。消融实验证实，去除整个 SERC 推理链会导致严格结构得分（StS）从 52.7 骤降至 16.4（−36.3），宽松结构得分（LeS）从 82.6 降至 21.8（−60.8），验证了 TER 对结构遵循性的决定性作用。

**生成模块（Generating Module）** 以 TER 输出的经验证最终报告为驱动，按计划调用对应的模态生成工具，在指定位置插入各模态内容，形成最终的交织多模态输出。

### 关键公式推导

#### 语义-质量耦合得分（SQCS）

UNIM 评估套件的第一维度是语义正确性与生成质量的耦合得分，定义为：

$$\mathrm{SQCS} = \mathrm{SC} \cdot \left( \eta^{\mathrm{SQCS}} + (1 - \eta^{\mathrm{SQCS}}) \cdot \mathbf{GQ} \right)$$

其中：
- $\mathrm{SC}$（Semantic Correctness）：语义正确性得分，由 LLM-as-a-Judge 评估生成内容与参考答案的语义一致性；
- $\mathbf{GQ}$（Generation Quality）：生成质量得分，针对不同模态采用无参考质量评估指标；
- $\eta^{\mathrm{SQCS}}$：权重因子，调节语义正确性与生成质量的相对重要性。

该公式采用乘法耦合而非简单加权平均：当语义完全错误时（$\mathrm{SC} \to 0$），整体得分归零，体现“语义正确是生成质量的前提”这一设计理念。

#### 交织连贯性得分（ICS）

第三维度评估模型在多模态整合中维持逻辑连接和表达协调的能力：

$$\mathrm{ICS} = \eta^{\mathrm{ICS}} \cdot \mathrm{HC} + (1 - \eta^{\mathrm{ICS}}) \cdot \mathrm{SH}$$

其中：
- $\mathrm{HC}$（Holistic Coherence）：整体连贯性，衡量跨模态内容之间的逻辑一致性；
- $\mathrm{SH}$（Stylistic Harmony）：风格和谐性，评估不同模态输出在表达风格上的协调程度；
- $\eta^{\mathrm{ICS}}$：权重因子，调节整体连贯性与风格和谐性的贡献比例。

合理性验证实验（Figure 5）显示，ICS 与人工评分的 Pearson 相关系数达 $r = 0.960$，SQCS 与人工评分的相关系数达 $r = 0.974$，证实了这两个指标的有效性。

#### 结构完整性得分（StS 与 LeS）

响应结构完整性维度包含两个互补指标：

**严格结构得分（StS）** 要求模态类型和数量均与参考答案精确匹配：

$$\mathrm{StS} = \frac{1}{|\mathcal{M}'|} \sum_{m \in \mathcal{M}'} F1_m$$

其中 $\mathcal{M}'$ 为所有模态类型的集合，$F1_m$ 为模态 $m$ 的 F1 分数。

**宽松结构得分（LeS）** 仅要求模态类型覆盖，不要求数量一致：

$$\mathrm{LeS} = \frac{|\mathrm{Overlap}|}{|g_t|}$$

其中 $|\mathrm{Overlap}|$ 为预测与参考答案的模态类型交集大小，$|g_t|$ 为参考答案的模态类型总数。受控扰动实验（Figure 6）验证了二者的合理性：增加或删除占位符标签时 StS 下降，而 LeS 仅在模态类型被移除时才下降。

#### 支持率与相对性能

为公平评估不同模型在其实际支持模态子集上的表现，引入支持率 $\tau$ 作为条件修正因子：

$$\mathcal{X}^{rel} = \tau \cdot \mathcal{X}^{abs}$$

其中 $\mathcal{X}^{abs}$ 为绝对性能得分，$\mathcal{X}^{rel}$ 为考虑支持率后的相对性能。这一设计避免了因模型不支持某些模态而导致的评分不公，使得跨模型比较更加客观。

### 补充图表

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the UNIM evaluation suite. ① refers to the calculation process of the StS and LeS (§4.2). ② represents the calculation process of the ICS in Eq. (2). ③ refers to the calculation process of the SQCS; please refer to Eq. (1)*

## 实验与分析

### 1. 基准数据集概览

UNIM 是首个面向任意到任意交织多模态的统一基准，其规模与多样性远超现有数据集。如 Table 1 所示，UNIM 包含 31K 高质量实例，覆盖 30 个领域和 7 种模态（文本、图像、音频、视频、文档、代码、3D），而此前基准仅支持文本-图像两种模态的简单组合。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/002_Table_1.jpg]]
*Table 1: Comparison with existing interleaved multimodal benchmarks. Inter. Comb.: Interleaved combinations of modalities. Cap. per Instance: Capability per instance. Difficulty Tax.: Difficulty taxonomy*

Table 2 给出了数据集的详细统计分布。模态层面，图像（22,936，73.9%）和音频（24,963，80.5%）占比最高，视频（2,336，7.5%）、文档（3,858，12.4%）、代码（807，2.6%）和 3D（420，1.4%）形成长尾分布。领域层面，自然科学（NS）占 34.2%，社会科学（SS）占 37.3%，通用领域（GA）占 28.5%。难度分布上，简单实例占 34.4%，中等占 45.4%，困难占 20.2%，呈现合理的梯度结构。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/004_Table_2.jpg]]
*Table 2: General statistics of UNIM dataset*

### 2. 主要结果

#### 2.1 响应结构完整性

Table 3 报告了响应结构完整性维度的评估结果。基线模型在严格结构得分（StS）和宽松结构得分（LeS）上表现极差：**NExT-GPT** 和 **MIO** 的 StS/LeS 大多低于 5%，**AnyGPT** 也仅分别达到 12.5% 和 16.4%。这表明现有任意到任意多模态大语言模型几乎无法遵循交织输出的模态结构要求。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/009_Table_3.jpg]]
*Table 3: Assessment results on Response Structure Integrity*

相比之下，UNIMA 在通用领域的 StS 达到 71.3%，LeS 达到 84.3%，分别超出 AnyGPT 58.8 和 67.9 个百分点。这一巨大差距的核心驱动力在于可追溯证据推理（TER）模块：消融实验证实，去除整个推理链后 StS 从约 52% 骤降至 16%（-36.3），LeS 从约 82% 降至 21%（-60.8），确认 TER 是结构遵循和指令执行的中枢组件。

#### 2.2 语义正确性与生成质量

Table 4 展示了语义正确性与生成质量（SQCS）及支持率（τ）的结果。基线模型的 SQCS 绝对值大多低于 20%：MIO 为 21.2，AnyGPT 为 17.9，NExT-GPT 仅为 4.4。UNIMA 在通用领域达到 62.2，相较 MIO 提升 41.0 个百分点。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/011_Table_4.jpg]]
*Table 4: Performance on Semantic Correctness & Generation Quality and Supporting Rate (τ )*

值得注意的是，支持率 τ 揭示了模态覆盖能力的差异。UNIMA 的 τ 显著高于基线模型，说明其能够处理更广泛的模态组合。通过公式 $\mathcal{X}^{rel} = \tau \cdot \mathcal{X}^{abs}$ 计算的相对性能进一步放大了这一优势，确保公平比较的同时暴露了基线模型在模态支持上的根本性缺陷。

#### 2.3 交织连贯性

Table 5 报告了交织连贯性（ICS）的评估结果。ICS 由整体连贯性（HC）和风格和谐性（SH）加权组合：$\mathrm{ICS} = \eta^{\mathrm{ICS}} \cdot \mathrm{HC} + (1 - \eta^{\mathrm{ICS}}) \cdot \mathrm{SH}$。UNIMA 在通用领域达到 69.8，领先 MIO 的 60.0（+9.8）和 AnyGPT 的 43.6（+26.2）。NExT-GPT 仅得 28.1，表明其在跨模态逻辑衔接和表达协调方面存在严重不足。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/012_Table_5.jpg]]
*Table 5: Evaluation results on Interleaved Coherence*

消融实验进一步揭示，用无条件描述替换任务条件稠密描述（TCDC）后，SQCS 下降 6.7，ICS 下降 5.7，说明任务感知的语义基础对语义准确性和跨模态连贯性具有重要影响。

### 3. 消融实验

Table 6 系统性拆解了 UNIMA 各组件的贡献，结论如下：

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/013_Table_6.jpg]]
*Table 6: Ablation results on UNIMA*

- **TER 模块是结构完整性的决定性因素**：去除整个 SERC 推理链导致 StS 和 LeS 崩盘式下降，确认其在结构遵循中的核心地位。
- **验证子模块对全局可靠性至关重要**：禁用验证子模块后，所有指标均显著下降（SQCS -12.2，ICS -8.7，StS -14.4，LeS -15.8），证明检查-回溯-再生成的设计是可靠交织输出的必要条件。
- **TCDC 主要增强语义基础**：替换为普通描述后，SQCS 和 ICS 出现中等程度下降，表明任务条件的稠密描述主要服务于语义接地和跨模态连贯性，对结构指标影响相对较小。

### 4. 能力维度与难度分析

Figure 7 展示了 10 项能力维度上的表现对比。UNIMA 在所有维度上均取得最高且最均衡的性能，而基线模型在不同能力间表现出剧烈波动，缺乏稳定的跨能力泛化能力。Figure 9 进一步揭示了难度梯度下的性能变化趋势：仅有 UNIMA 呈现出与难度递增相匹配的清晰性能梯度，基线模型在不同难度级别上的表现几乎无差异，说明其缺乏应对复杂交织任务的基本推理能力。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/010_Figure_7.jpg]]
*Figure 7: Results across 10 capabilities on UNIM. C1: Perceptual Understanding, C2: Spatial Understanding, C3: Temporal Understanding, C4: Semantic Generation, C5: Content Editing, C6: Creative Expression, C7: Reasoning Capability, C8: Emotional Analysis, C9: Structural Analysis, and C10: Planning Capability. Refer to Appendix §C.4 for details*

### 5. 评估指标合理性验证

Figure 5 验证了 SQCS 和 ICS 与人工评分的相关性：SQCS 的 Pearson 相关系数达到 r = 0.974，ICS 达到 r = 0.960，表明两项指标与人类判断高度一致。Figure 6 通过受控扰动实验验证了 StS 和 LeS 的合理性：当增加或移除模态类型和占位符标签时，StS 均会下降；而 LeS 仅在模态类型被移除时下降，符合其宽松匹配的设计预期。

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/007_Figure_5.jpg]]
*Figure 5: Results for rationality verification of SQCS and ICS*

![[assets/figures/papers/paper_list_l800_https_arxiv_org_abs_2603_05075/figures/008_Figure_6.jpg]]
*Figure 6: Results for rationality verification of StS and LeS*

### 6. 失败模式与局限性

尽管 UNIMA 在所有维度上大幅领先，但在极端复杂任务中仍存在退化现象。结构指标（StS/LeS）在高阶模态交织场景下会出现下降，表明当前方法对复杂交织结构的建模能力仍有提升空间。此外，评估套件依赖外部描述工具和 LLM-as-a-Judge，可能引入一定偏差，且对高度开放式生成任务的评估敏感性有待进一步验证。UNIM 当前仅覆盖 7 种模态，未来扩展至更多模态将有助于更全面地模拟真实世界交互。

## 方法谱系与知识库定位

### 任务定位与基准空白

UNIM 填补了任意到任意（any-to-any）交织多模态评估的体系性空白。此前的主流交织多模态基准——如 MM-Interleaved、MMDU、DEMON、OmniBench 等——仅覆盖文本和图像两种模态的交织组合，评估维度通常局限于单一语义正确性或生成质量。UNIM 首次将模态空间扩展至 **7 种模态**（文本、图像、音频、视频、文档、代码、3D），并以 **开放式 QA 格式** 构建了 31K 高质量实例，覆盖 30 个领域和 10 项能力维度。这一设计使得 UNIM 成为目前唯一能系统评估模型在“任意模态组合输入 → 任意模态组合输出”范式下综合能力的基准（Table 1 对比了与现有基准的模态覆盖、交织组合数、每实例能力数及难度分类）。

### 与现有任意到任意模型的基线关系

论文将 UNIMA 与三类代表性任意到任意多模态大语言模型进行了直接对比：

- **AnyGPT**：采用离散序列建模的统一多模态生成框架，支持文本、图像、音频、音乐的任意到任意生成。在 UNIM 上，其结构完整性得分（StS/LeS）约为 12.5/16.4，语义-质量耦合得分（SQCS）约 17.9，交织连贯性得分（ICS）约 43.6。其瓶颈在于缺乏显式的结构规划和跨模态推理机制，导致在要求精确模态序列输出的任务上表现薄弱。
- **NExT-GPT**：基于模态对齐编码器-解码器架构的任意到任意模型，支持文本、图像、视频、音频。在 UNIM 上表现最弱：StS/LeS 仅约 2.2/2.5，SQCS 约 4.4，ICS 约 28.1。其核心缺陷在于模态编码与生成之间的推理链路缺失，无法有效理解交织输入的结构约束。
- **MIO**：支持文本、图像、音频、视频的双向多模态交互模型。其 ICS（约 60.0）在基线中最优，反映出较好的跨模态连贯性，但 SQCS（约 21.2）和 StS/LeS（约 3.3/3.8）仍然极低，说明其语义理解和结构遵循能力与 UNIMA 存在数量级差距。

上述基线在 UNIM 上的绝对得分普遍偏低（SQCS 多低于 20%，StS/LeS 多低于 5%），且在不同难度级别上表现无显著梯度差异（Figure 9），表明现有任意到任意模型在复杂交织任务上存在系统性能力不足。

### UNIMA 的方法谱系定位

UNIMA 的核心方法论贡献在于将 **智能体式推理框架** 引入任意到任意交织多模态生成。其架构可定位于以下三条方法脉络的交汇点：

1. **工具增强的多模态智能体**：UNIMA 的接收模块（Receiving Module）集成了 GPT-5 mini、Qwen3-Omni Thinker 等专业工具，将非文本模态统一转换为任务条件稠密描述（TCDC）。这与 ToolFormer、HuggingGPT 等工具调用范式一脉相承，但 UNIMA 的创新在于将工具输出直接作为下游推理链的**可验证证据基础**，而非简单的模态翻译。

2. **显式推理链与自我验证**：可追溯证据推理模块（TER）是 UNIMA 的方法核心。与依赖隐式思维链的基线模型不同，TER 构建了四步结构化证据推理链（SERC），并内嵌**检查器-判定器验证循环**——在生成最终报告前对中间推理步骤进行验证、回溯和修正。这一设计在方法谱系上可追溯至 ReAct、Self-Refine 等推理-行动循环范式，但 UNIMA 将其首次系统应用于交织多模态输出的结构控制。消融实验提供了强因果证据：去除整个 SERC 推理链导致 StS 从 52.7 骤降至 16.4（−36.3），LeS 从 82.6 降至 21.8（−60.8）；禁用验证子模块则使所有指标显著下降（SQCS −12.2，ICS −8.7，StS −14.4，LeS −15.8）。

3. **计划驱动的多模态生成**：生成模块（Generating Module）由经验证的最终报告驱动，按计划工具集分步生成各模态内容并插入指定占位符。这与规划-执行（plan-and-execute）式生成框架共享设计哲学，但 UNIMA 将规划粒度细化到模态级别的位置控制，从而实现了基线模型无法达到的结构完整性。

### 适用边界与局限

尽管 UNIMA 在 UNIM 上大幅领先基线（SQCS 约 62.2，StS 约 71.3，LeS 约 84.3，ICS 约 69.8），其适用边界仍受以下因素制约：

- **模态覆盖的有限性**：UNIM 当前仅覆盖 7 种模态，UNIMA 的工具链也仅针对这些模态优化。扩展到触觉、嗅觉、雷达点云等更多模态时，TCDC 的描述质量和工具可用性需重新验证。
- **极端复杂交织场景的退化**：在涉及高阶模态交织的困难实例中，UNIMA 的结构指标（StS/LeS）仍会下降，说明当前推理链的长度和验证粒度可能不足以应对极端复杂的模态序列约束。
- **评估套件的外部依赖偏差**：三维度评估依赖外部描述工具和 LLM-as-a-Judge，可能引入系统性偏差。尽管 SQCS 和 ICS 与人工评分的 Pearson 相关系数分别达到 0.974 和 0.960（Figure 5），但对高度开放生成任务的评估敏感性仍需进一步验证。
- **非端到端架构的效率代价**：UNIMA 的模块化智能体设计在多步推理和验证循环中引入了额外的推理延迟，与端到端统一模型相比存在效率劣势。

### 开放问题

论文在结论中明确提出了若干待解决的研究问题，这些问题构成了该方向的后续工作空间：

1. **统一编码器-解码器架构**：如何设计单一模型以端到端方式支持任意七种模态的组合理解与生成，而非依赖外部工具链？
2. **多能力协同机制**：如何在任意到任意多模态大模型中实现感知、推理、生成等多项能力的协同，以处理复杂的交织任务？
3. **模态间动态交互建模**：如何建模交织场景下模态间的协同与互补关系，并实现根据任务上下文动态调整各模态影响力的推理机制？
4. **交织感知的奖励设计**：如何设计融合语义准确性与交织结构约束的奖励机制，用于模型的对齐训练（如 RLHF）？
5. **深层自我验证嵌入**：如何将 TER 中的检查-回溯-再生成循环更深入地嵌入模型内部推理过程，而非作为外部模块？
6. **认知式交织建模**：如何构建模拟人类多模态推理策略（如选择性注意、跨模态联想、层级化规划）的认知式方法？

这些问题共同指向一个核心挑战：**从“工具拼接式”的任意到任意生成迈向“原生统一”的任意到任意理解与生成**。UNIM 和 UNIMA 为这一方向提供了首个系统性的评估基准和方法论基线，但其方法本质上是智能体框架对现有专用模型的编排，距离真正的统一多模态大模型仍有显著差距。

## 原文 PDF

![[paperPDFs/CVPR_2026/UniM_A_Unified_Any_to_Any_Interleaved_Multimodal_Benchmark.pdf]]
