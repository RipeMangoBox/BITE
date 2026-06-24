---
title: "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Evaluating_Memory_in_LLM_Agents_via_Incremental_Multi_Turn_Interactions.pdf
openreview_forum_id: DT7JyQC3MR
aliases:
- EMLAIMTI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "记忆更新策略（如显式的新旧事实优先级规则）和检索/上下文覆盖范围共同决定了智能体在冲突消解和全局理解上的表现。"
primary_logic: "没有一种单一的智能体架构能在所有记忆能力上领先；长上下文模型擅长全量信息学习与推理，RAG在精确检索上具有优势，而融入迭代推理的智能体记忆方法则需要更强的骨干模型才能释放潜力，未来需要设计混合机制以覆盖全部维度的记忆需求。"
claims:
- "在FactConsolidation-MH任务上，所有方法的准确率最高仅为7%，表明多跳选择性遗忘构成当前记忆智能体的极端挑战。"
- "长上下文模型（如GPT-4.1-mini）在测试时学习（TTL）和长程理解（LRU）任务上显著优于RAG和智能体记忆方法，证实全量上下文对综合推理的优势。"
- "多数RAG代理在准确检索（AR）任务上超过其骨干模型GPT-4o-mini，说明检索增强有助于信息定位。"
- "推理模型在短上下文（6K）的选择性遗忘任务上可达近乎完美的准确率，但在32K上下文下性能断崖式下跌，证明长程冲突消解是核心难点。"
---

# Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions

> [!tip] 核心洞察
> 没有一种单一的智能体架构能在所有记忆能力上领先；长上下文模型擅长全量信息学习与推理，RAG在精确检索上具有优势，而融入迭代推理的智能体记忆方法则需要更强的骨干模型才能释放潜力，未来需要设计混合机制以覆盖全部维度的记忆需求。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过增量多轮交互评估LLM智能体的记忆能力 |
| 英文题名 | Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DT7JyQC3MR); [GitHub](https://github.com/HUST-AI-HYZ/MemoryAgentBench); [Project](https://huggingface.co/datasets/ai-hyz/MemoryAgentBench) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MemoryAgentBench |
| Dataset | SH-Doc QA (Accurate Retrieval), FactConsolidation-MH (Selective Forgetting), TTL Multi-Class Classification (Banking77), FactCon-SH (6K vs 32K, Selective Forgetting) |

> [!tip] 效果简介
> - SH-Doc QA (Accurate Retrieval) 上，Accuracy 为 GPT-4.1-mini (Long-Context Agent)，对比 BM25 (Simple RAG Agent)，变化 +17.0 (83.0 vs 66.0)。
> - FactConsolidation-MH (Selective Forgetting) 上，Accuracy 为 HippoRAG-v2，对比 GPT-4.1-mini (Long-Context Agent)，变化 +2.0 (7.0 vs 5.0)。
> - TTL Multi-Class Classification (Banking77) 上，Accuracy 为 GPT-4o-mini with full history (test-time learning)，对比 Zero-shot (no historical examples)，变化 +45.2 percentage points (48.6 vs 3.4)。

## 概述

### 问题与瓶颈

记忆智能体（Memory Agent）需要同时具备四项互补的核心能力：**准确检索**（Accurate Retrieval, AR）、**测试时学习**（Test-Time Learning, TTL）、**长程理解**（Long-Range Understanding, LRU）和**选择性遗忘**（Selective Forgetting, SF）。然而，现有评估基准和智能体架构均未能全面覆盖这四项能力。当前记忆智能体——包括长上下文模型、RAG代理和智能体记忆架构——面临一个根本性瓶颈：**没有任何单一架构能在所有记忆能力上同时领先**。尤其是选择性遗忘中的多跳冲突消解，所有方法的准确率最高仅为7%（Table 3 FC-MH列），暴露出记忆更新与长程推理协同的严重不足。

### 核心结论

1. **架构各有专长，无全能方案**：长上下文模型（如GPT-4.1-mini）擅长全量信息学习与推理，在TTL和LRU任务上显著优于其他架构；RAG代理在精确检索（AR）任务上表现突出，多数超过其骨干模型GPT-4o-mini；而融入迭代推理的智能体记忆方法（如MIRIX）则需要更强的骨干模型才能释放潜力。
2. **选择性遗忘是极端挑战**：推理模型在短上下文（6K）下可达近乎完美的准确率，但在32K上下文下性能断崖式下跌（如o4-mini从100%降至61%，Table 5），证明长程冲突消解是核心难点，仅靠扩大窗口或提示工程无法解决。
3. **混合机制是未来方向**：需要设计融合长上下文全量推理与结构化检索/更新策略的混合机制，以覆盖全部维度的记忆需求。

### 方法定位

**MemoryAgentBench** 是一个专为记忆智能体设计的评估基准，其核心变革在于**输入范式**：将传统长上下文数据集重构为增量多轮对话格式，将文本划分为多个块（chunks）逐步输入，并附上记忆指令，模拟智能体增量处理信息的真实场景。同时，为选择性遗忘任务引入**显式冲突消解机制**：为事实分配序列号，规定新事实具有更大的序列号，要求优先使用最新事实解决冲突。基准涵盖长上下文代理、简单/嵌入式/结构增强RAG代理及商业智能体记忆代理（如MemGPT、MIRIX）三大类方法。

### 主要结果

- **准确检索**：长上下文模型GPT-4.1-mini在SH-Doc QA上达到83.0%，显著优于简单RAG代理BM25的66.0%（Table 3）。
- **测试时学习**：GPT-4o-mini在全记忆设定下较零样本提升45.2个百分点（Banking77: 48.6% vs 3.4%，Table 16），证实性能增益来自历史交互学习。
- **选择性遗忘**：多跳场景（FactConsolidation-MH）所有方法准确率不超过7%，HippoRAG-v2仅以7.0%略高于GPT-4.1-mini的5.0%（Table 3）。
- **骨干模型影响**：RAG代理升级骨干模型收益微弱，而智能体记忆代理（如MIRIX）从更强骨干中获益显著，展示出更大的潜力空间（Table 4）。

## 背景与动机

大规模语言模型（LLM）正从单轮问答系统演化为需要持续与用户交互的智能体（Agent），而记忆能力是实现这一转变的核心瓶颈。一个合格的记忆智能体不仅需要存储历史信息，更必须在多轮交互中动态更新知识、检索相关片段、整合长程依赖，并在新旧事实冲突时做出正确取舍。然而，现有评估体系存在明显缺口：长上下文基准（如Needle-in-a-Haystack）侧重单次输入的全量检索，无法模拟增量式信息涌入的真实场景；而现有的记忆QA基准又缺乏对“选择性遗忘”等关键维度的覆盖，导致不同记忆架构的优势与短板难以被系统比较。

从方法层面看，当前记忆智能体主要分为三类：长上下文模型（Long-Context Agents）将完整对话历史直接送入上下文窗口，依赖模型自身的注意力机制进行隐式检索与推理；检索增强生成代理（RAG Agents）将历史信息存入外部存储，在回答时按需检索相关内容；智能体记忆架构（Agentic Memory）则引入迭代式的检索-推理循环，通过显式的记忆更新与决策流程管理信息。这三类方法在信息获取方式、更新策略和推理深度上存在本质差异，但缺乏统一的评测框架来揭示它们在真实多轮场景下的能力边界。

本文的核心动机在于填补这一评估空白。作者提出 **MemoryAgentBench**，将现有长上下文数据集重构为增量多轮交互格式，并新增 EventQA 和 FactConsolidation 两个数据集，覆盖四项互补的记忆核心能力：**准确检索（Accurate Retrieval, AR）**、**测试时学习（Test-Time Learning, TTL）**、**长程理解（Long-Range Understanding, LRU）** 和**选择性遗忘（Selective Forgetting, SF）**。这四项能力构成了记忆智能体从信息定位到知识冲突消解的完整能力谱系（见图1），任何单一维度的缺失都会导致实际部署中的严重失效。通过在此基准上对三类记忆方法进行大规模对比，本文旨在回答一个根本性问题：是否存在一种统一的记忆机制，能够同时胜任全部四项核心任务？

## 核心创新

本工作的核心创新并非提出一种新的记忆智能体架构，而是构建了一套**系统性的评估范式**，并通过对现有记忆方法的全面诊断，揭示了当前记忆智能体在四项互补能力上的结构性缺陷。其创新点集中体现在以下三个维度。

### 1. 增量多轮交互的评估范式

传统长上下文评估通常将完整文本一次性输入模型进行提问，这无法模拟记忆智能体在实际部署中逐步接收信息、增量更新记忆的真实工作模式。MemoryAgentBench 的关键改变在于**输入范式的重构**：

- **基线范式**：一次性输入完整长文本进行提问。
- **提出范式**：将文本划分为多个块，以增量多轮对话形式逐步输入，并附上记忆指令。所有数据集被统一组织成标准结构 $c_{1}, c_{2}, \cdots, c_{n}$ (chunks), $q_{1}, q_{2}, \cdots, q_{m}$ (questions), and $a_{1}, a_{2}, \cdots, a_{m}$ (answers)，模拟智能体随时间推移逐步吸收信息的过程。

这一范式转变使得评估能够真实反映记忆智能体在信息碎片化、时间序列化条件下的检索与推理能力，而非仅仅测试长窗口模型的容量极限。

### 2. 选择性遗忘的冲突消解机制

选择性遗忘（Selective Forgetting）是本工作定义的四项核心能力中最具挑战性的一项，要求智能体在信息更新时能够优先采用新事实、抑制旧事实。为此，MemoryAgentBench 设计了明确的**冲突消解规则**：

- **基线做法**：未指定明确规则，依赖模型自身推理。
- **提出机制**：为事实分配序列号，明确规定新事实具有更大的序列号，要求智能体通过寻找最新事实来解决冲突。

这一设计将“选择性遗忘”从模糊的隐式要求转化为可精确评估的显式任务，使得多跳冲突消解（FactConsolidation-MH）成为暴露当前方法极限的试金石——所有方法的准确率最高仅为7%。

### 3. 能力维度的系统化解构

MemoryAgentBench 将记忆智能体的能力需求分解为四个正交维度：**准确检索（Accurate Retrieval）**、**测试时学习（Test-Time Learning）**、**长程理解（Long-Range Understanding）**和**选择性遗忘（Selective Forgetting）**。这种解构本身是一项重要的方法论创新，因为它揭示了不同记忆架构在各维度上的非对称优势：

- 长上下文模型在测试时学习和长程理解上领先，得益于全量上下文的综合推理优势；
- RAG 代理在准确检索上超过其骨干模型，检索增强有助于信息定位；
- 但在选择性遗忘的多跳场景中，所有方法几乎全部失败。

这种分维度的诊断框架直接指向了核心瓶颈：**没有一种单一的智能体架构能在所有记忆能力上领先**，未来需要设计混合机制以覆盖全部维度的记忆需求。这一洞察为后续研究提供了清晰的能力图谱和优化方向。

## 整体框架

MemoryAgentBench 将记忆智能体的评估统一为一个**增量多轮对话管道**。其核心设计理念是：将原本用于长上下文一次性评估的数据集重构为多个对话块，以时间顺序逐步输入智能体，从而模拟记忆系统在持续信息流下的“吸收—检索—推理”完整循环。

### 输入标准化

所有数据集首先被规范化为统一的三元组结构：

$$c_{1}, c_{2}, \cdots, c_{n} \text{ (chunks)}, \quad q_{1}, q_{2}, \cdots, q_{m} \text{ (questions)}, \quad a_{1}, a_{2}, \cdots, a_{m} \text{ (answers)}$$

其中 $n$ 个输入块按时间顺序依次注入智能体，$m$ 个问题在全部或部分块注入后提出。每个输入块被包装在模拟的 User–Assistant 对话中，并附带显式的记忆指令，以触发智能体的记忆机制。

### 管道模块与数据流

整个评估管道由三个核心模块串联构成：

1.  **Memory Ingestion（记忆摄入）**  
    智能体逐块接收输入 $c_1, c_2, \ldots, c_n$，将其吸收进各自的记忆系统。不同类型的智能体在此阶段的行为截然不同：长上下文模型将所有块累积在上下文窗口中（超出窗口时采用 FIFO 驱逐策略）；RAG 代理将块索引并存入外部检索库；Agentic Memory 代理则可能进行摘要、结构化存储或迭代更新。

2.  **Memory Retrieval（记忆检索）**  
    当问题 $q_i$ 提出时，智能体从其记忆系统中获取相关信息。RAG 代理依赖稀疏或稠密检索器从已存储的块中召回 Top-K 相关片段；Agentic Memory 代理通过多轮决策式检索与推理循环动态获取证据；长上下文模型则直接依赖其完整上下文窗口进行隐式检索。

3.  **Answer Generation（答案生成）**  
    智能体利用检索到的信息（或全量上下文）生成最终答案，并与标准答案 $a_i$ 进行比对评估。

### 选择性遗忘的特殊设计

对于选择性遗忘任务，管道引入了**冲突消解机制**：每个事实被分配序列号，新事实具有更大的序列号，智能体被强制要求通过寻找最新事实来解决信息冲突。这一设计将记忆更新策略显式化，使评估能够区分“检索到了正确信息”与“在冲突中选择了正确版本”两个不同层面的能力——而后者正是当前所有方法的集体性失败点（多跳冲突消解准确率最高仅 7%）。

### 评估覆盖维度

该管道并非仅测试单一能力，而是系统性地覆盖了记忆智能体应当具备的四项互补核心能力：**准确检索**、**测试时学习**、**长程理解**和**选择性遗忘**。通过统一管道、标准化提示模板和一致的评估协议，性能差异可归因于记忆机制本身，而非提示工程或评估条件的不一致。

## 核心模块与公式推导

### 数据集标准化格式

MemoryAgentBench 将所有评估数据集统一为增量多轮交互的标准结构。给定一个原始数据集，其被组织为 $n$ 个输入块、$m$ 个查询和 $m$ 个答案的三元组形式：

$$c_{1}, c_{2}, \cdots, c_{n}\ (\text{chunks}),\ q_{1}, q_{2}, \cdots, q_{m}\ (\text{questions}),\ \text{and}\ a_{1}, a_{2}, \cdots, a_{m}\ (\text{answers})$$

其中每个块 $c_i$ 被包裹在一个模拟的 User-Assistant 对话轮次中，并附加显式的记忆指令以触发智能体的记忆机制。该格式是所有智能体类型（长上下文模型、RAG 代理、智能体记忆代理）的统一输入范式，确保性能差异仅来源于记忆架构本身，而非输入结构的不一致。

### 选择性遗忘的冲突消解规则

针对 FactConsolidation 数据集中的选择性遗忘任务，基准引入了一种基于事实序列号的优先规则。每个事实被分配一个序列号，较新的事实具有更大的序列号。智能体被明确要求通过寻找最新事实来解决冲突：

$$\text{newer facts have larger serial numbers} \implies \text{resolve conflicts by finding the newest fact}$$

该规则构成了选择性遗忘评估的因果控制变量：消融实验（Table 19）表明，显式优先新事实的策略（Policy A）仅能略微改善单跳表现，无法推广至多跳推理；保守策略（Policy B）反而导致整体性能下降。这一结果验证了仅靠提示工程无法解决选择性遗忘问题，冲突消解机制需要更深层的架构支持。

### 记忆流水线模块

MemoryAgentBench 覆盖的三类智能体共享一个抽象的记忆流水线，包含三个核心模块：

1. **Memory Ingestion（记忆摄入）**：接收并存储增量输入的块。所有智能体被要求逐个接收块 $c_1, c_2, \ldots, c_n$，将其吸收到记忆中，并增量更新记忆状态。
2. **Memory Retrieval（记忆检索）**：根据查询从记忆系统中获取相关信息。RAG 代理通过存储过去信息并按需检索相关内容实现；长上下文模型则依赖全量上下文窗口进行隐式检索。
3. **Answer Generation（答案生成）**：利用检索到的信息或全量上下文生成最终答案。

这三类智能体的本质差异体现在检索模块的实现上：长上下文模型将全部历史作为上下文传入生成器；RAG 代理采用稀疏检索（BM25）、稠密检索（Contriever、Qwen3-Embedding-4B）或结构增强检索（RAPTOR、GraphRAG、MemoRAG、HippoRAG-v2）；智能体记忆代理（MemGPT、MIRIX）则使用迭代的、决策驱动的检索与推理循环。

### 关键参数与消融发现

基准通过消融实验揭示了两个关键参数对记忆性能的影响机制：

- **块大小（chunk size）**：减小块大小可提高嵌入式 RAG 在准确检索任务上的性能，因为更细粒度的分段增强了检索信息的相关性；但块大小的变化会损害长程理解任务的表现，暗示上下文碎片化与长程注意机制之间存在冲突。
- **检索 Top-K**：增加 RAG 检索的 Top-K 数量通常能提升多数任务的准确率，但过度增大可能引入噪声。

这些参数构成了记忆智能体性能的关键调节旋钮，其在不同能力维度上的权衡效应是未来设计混合记忆机制的重要依据。

## 实验与分析

### 总体性能对比：四种核心能力的权衡

Table 3 汇总了所有代理类型在 MemoryAgentBench 四项核心能力上的表现。最核心的发现是：**没有任何一种单一架构能在全部维度上领先**，不同记忆范式之间存在显著的能力权衡。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/005_Table_3.jpg]]
*Table 3: Overall Performance Comparison. In the absence of a specified model, All RAG agents and commercial memory agents use GPT-4o-mini as the backbone. Thus we highlight the performance of GPT-4o-mini as the reference. FC-SH and FC-MH mean FactConsolidation Single Hop and FactConsolidation Multi Hop, respectively. Best viewed in colors*

长上下文模型 GPT-4.1-mini 以总体得分 71.8 位居所有代理之首，其在测试时学习（TTL）和长程理解（LRU）任务上具有绝对优势——这验证了全量上下文对综合推理的支撑作用。然而，该模型在准确检索（AR）类别中的 SH-Doc QA 任务上仅得 83.0，而基于词法匹配的简单 RAG 代理 BM25 却能达到 66.0，Embedding-based RAG 中表现最好的 Qwen3-Embedding-4B 亦展现出竞争力。这说明**检索增强在信息精确定位上具有不可替代的价值**，即便骨干模型本身已具备长上下文处理能力。

RAG 代理在准确检索类别上普遍优于其骨干模型 GPT-4o-mini（总体得分 42.2），证实了检索机制对信息定位的增益。但在测试时学习和长程理解任务上，RAG 代理的性能显著落后于长上下文模型——这是检索碎片化导致上下文连贯性丧失的直接后果。

### 选择性遗忘：极端挑战与失败模式

选择性遗忘（Selective Forgetting）构成了当前记忆智能体的**最大短板**。在 FactConsolidation-MH（多跳冲突消解）任务上，所有方法的准确率最高仅为 7%（HippoRAG-v2），长上下文模型 GPT-4.1-mini 仅得 5.0。这一近乎全面失败的结果揭示了一个深层瓶颈：**现有记忆架构无法在长程上下文中有效追踪并消解多跳事实冲突**。

Table 5 进一步放大了这一问题的严峻性。推理模型 o4-mini 在短上下文（6K）的 FactCon-SH 任务上可达 100.0 的完美准确率，在 FactCon-MH 上亦能达到 80.0；但当上下文扩展至 32K 时，两项任务的准确率分别断崖式下跌至 61.0 和 14.0。GPT-4o 同样呈现类似趋势：FactCon-MH 从 28.0（6K）降至 10.0（32K）。这一现象表明，**长程冲突消解并非单纯由模型推理能力不足所致，而是上下文长度增加后信息定位与冲突识别机制的系统性失效**。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/010_Table_5.jpg]]
*Table 5: Performances of reasoning models on the dataset FactConsolidation*

### 消融实验：关键设计因素的影响

**块大小（Chunk Size）的权衡效应。** Figure 2 展示了 SH-Doc QA 和 ∞-Bench-Sum 任务在不同块大小下的性能变化。减小块大小（更细粒度的分段）可提升嵌入式 RAG 在准确检索任务上的表现——更小的检索单元增强了检索相关性。然而，这一调整会损害长程理解任务的性能：上下文碎片化破坏了模型对文档全局结构的把握。这一发现揭示了记忆代理设计中一个根本性的张力：**检索精度与理解连贯性之间的冲突**。

**检索数量（Top-K）的影响。** Figure 3 表明，增加 RAG 检索的 Top-K 数量通常能提升多数任务的准确率，因为更多的候选片段增加了覆盖相关信息的概率。但这一趋势并非单调递增，过度增大 Top-K 可能引入噪声，需要根据具体任务进行权衡。

**骨干模型升级的差异化收益。** Table 4 比较了四种代表性记忆代理在三种不同骨干 LLM 下的表现，揭示了一个关键洞察：**RAG 代理从更强骨干模型中获益微弱，而 Agentic 记忆代理则展现出显著的潜力空间**。当骨干从 GPT-4o-mini 升级至 GPT-4.1-mini 时，RAG 代理的性能提升有限；但 MIRIX 等 Agentic 记忆方法在更强骨干下获得了大幅增益。这表明，融入迭代推理的记忆架构对模型的基础能力更为敏感，未来更强大的模型可能释放这类方法的更大潜力。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/009_Table_4.jpg]]
*Table 4: Performance comparison on three different backbone LLMs and four representative memory agents. We choose one dataset from every competency to evaluate agent performance*

**选择性遗忘策略的消融。** Table 19 验证了不同覆盖策略对选择性遗忘任务的影响。显式优先新事实的策略（Policy A）仅能略微改善单跳表现，无法推广至多跳推理；保守策略（Policy B）反而导致整体性能下降。这一结果证实：**仅靠提示工程无法解决选择性遗忘问题**，需要设计结构化的记忆更新与冲突消解机制。

### 计算成本与效率

在计算延迟方面，长上下文模型虽在性能上领先，但其推理延迟随上下文增长而线性增加。RAG 代理在记忆构建阶段需额外时间开销，但查询执行效率较高。Agentic 记忆代理因涉及多轮迭代检索与推理，查询执行延迟最高。这构成了性能、效率与成本之间的三维权衡空间，需要根据实际应用场景进行选择。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/003_Table_1.jpg]]
*Table 1: A comparison between MemoryAgentBench and existing long-term memory QA benchmarks. #Q denote the total number of questions. Context depth is defined as the number of tokens in the history. *Not reported in the paper, based on our approximation. The context depth of StoryBench is not reported in paper. We compare these datasets in terms of their ability to comprehensively and effectively evaluate the each capability dimension that we propose. We also compare prior work in terms of their evaluation coverage of memory agents—specifically, whether they provide comprehensive assessments across different categories of memory methods: Long-Context Agents (LCA), RAG Agents, and Agentic Memory (AM)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/004_Table_2.jpg]]
*Table 2: Overview of evaluation datasets. We select datasets that cover various important long-context capabilities. In the table, we underline the datasets we constructed ourselves. AvgL.: Average Context Length (measured using the GPT-4o-mini model’s tokenizer)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/011_Table_6.jpg]]
*Table 6: Datasets categorized by the specific aspects of evaluation. Here 1K is 1024*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/014_Table_7.jpg]]
*Table 7: Overall performance comparison on the datasets for TTL. All RAG agents and commercial memory agents use GPT-4o-mini as the backbone*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/015_Table_8.jpg]]
*Table 8: Performance comparison on different datasets and chunk sizes. Here we choose chunk sizes from {512, 1024, 2048, 4096} and we use k=10 for RAG-based methods. Table 9: Performance comparison on different retrieve number*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/016_Table_9.jpg]]

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/017_Table_10.jpg]]
*Table 10: Performance comparison on different context length*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/018_Table_11.jpg]]
*Table 11: Computational latency (in seconds) comparison on Long-Context Agents*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_DT7JyQC3MR/figures/019_Table_12.jpg]]
*Table 12: Computational latency (in seconds) comparison on RAG based agents. M.C. means Memory Construction and Q.E. means Query Execution. *Indicates that the time is obtained through estimation*


## 方法谱系与知识库定位

### 1. 方法谱系：从长上下文到记忆智能体的评估框架

MemoryAgentBench 并非提出一种新的记忆架构，而是构建了一套统一评估框架，将现有三类主流记忆方案——长上下文代理（Long-Context Agent）、检索增强生成代理（RAG Agent）和智能体记忆代理（Agentic Memory Agent）——置于同一增量多轮交互范式下进行系统比较。其核心设计转变在于**输入范式**：将传统的一次性长文本输入重构为 $c_{1}, c_{2}, \cdots, c_{n}$ 个分块，以增量对话形式逐步馈入，并要求代理在每个块上执行记忆吸收与更新。这一转变使得原本面向静态长上下文评估的数据集（如 ∞Bench、LooGLE）得以模拟记忆智能体的动态交互特性。

在基准方法的选取上，论文覆盖了从简单到复杂的完整谱系：

- **长上下文代理**：以 **GPT-4o** 和 **GPT-4.1-mini** 为代表，依赖原生长上下文窗口，采用 FIFO 驱逐策略处理超窗输入。这类方法构成记忆能力的理论上界——它们拥有对全量历史信息的无损访问权。
- **简单 RAG 代理**：**BM25** 作为词法检索基线，代表最轻量级的信息定位方案。
- **嵌入 RAG 代理**：**Contriever** 和 **Qwen3-Embedding-4B** 基于稠密向量检索，构成当前 RAG 系统的主流范式。
- **结构增强 RAG 代理**：包括 **RAPTOR**（树状索引）、**GraphRAG**（图结构检索）、**MemoRAG**（记忆引导检索）和 **HippoRAG-v2**（海马体启发式检索），它们通过构建结构化索引来提升长程信息的组织与访问效率。
- **智能体记忆代理**：**Mem0**、**MemGPT** 和 **MIRIX** 等商业或开源方案，采用迭代式、决策驱动的检索与推理循环，代表了记忆智能体的前沿设计理念。

### 2. 知识库定位：四项核心能力的互补性困境

MemoryAgentBench 的核心洞察在于揭示了**没有单一架构能同时满足全部四项记忆能力**，从而明确了当前记忆智能体研究的真实瓶颈所在。这一发现将不同方法的能力边界清晰地映射到四个维度上：

**准确检索（Accurate Retrieval）维度**：RAG 代理展现出结构性优势。多数 RAG 代理在准确检索任务上的表现超过了其骨干模型 GPT-4o-mini，验证了检索增强机制在信息精确定位上的有效性。然而，这一优势受制于分块粒度的选择——减小块大小（如将 chunk size 降至 512）可提升嵌入 RAG 的检索精度，但会损害长程理解任务的性能（见 Figure 2），揭示出检索粒度与全局理解之间的根本性张力。

**测试时学习（Test-Time Learning）与长程理解（Long-Range Understanding）维度**：长上下文模型占据绝对优势。GPT-4.1-mini 在这两类任务上显著超越所有 RAG 和智能体记忆代理，证实了全量上下文对综合推理的不可替代性。在 Banking77 数据集上，GPT-4o-mini 通过利用完整历史交互示例，将零样本准确率从 3.4% 提升至 48.6%，提升幅度达 45.2 个百分点（Table 16），表明测试时学习能力的核心驱动力在于对历史信息的全面访问而非检索筛选。

**选择性遗忘（Selective Forgetting）维度**：这是所有方法的共同失败区。在 FactConsolidation-MH（多跳冲突消解）任务上，所有方法的准确率最高仅为 7%（HippoRAG-v2），长上下文模型 GPT-4.1-mini 仅获 5%（Table 3）。更令人警醒的是，即使是最先进的推理模型 o4-mini，在短上下文（6K）设定下可达近乎完美的单跳冲突消解准确率（100%），但当上下文扩展至 32K 时性能断崖式下跌至 61%（单跳）和 14%（多跳）（Table 5）。这一现象揭示出**长程冲突消解是当前记忆智能体的核心难点**，且无法通过单纯扩大上下文窗口来解决。

### 3. 因果机制：记忆更新策略与检索覆盖的协同作用

影响智能体记忆表现的核心因果旋钮在于**记忆更新策略**与**检索/上下文覆盖范围**的协同作用。在选择性遗忘任务中，论文通过显式的新旧事实序列号规则（Policy A：优先使用最新事实）尝试引导冲突消解，但消融实验（Table 19）表明这一策略仅能略微改善单跳表现，无法推广至多跳推理；而保守策略（Policy B）反而导致整体性能下降。这验证了**仅靠提示工程无法解决选择性遗忘问题**，真正的瓶颈在于记忆更新与长程推理的深层耦合机制。

在骨干模型能力的影响上，消融实验（Table 4）揭示了架构依赖性的显著差异：RAG 代理从升级到更强骨干模型（如 GPT-4.1-mini）中仅获得微弱提升，表明其性能主要受限于检索机制本身；而智能体记忆代理（如 MIRIX）则从更强骨干中获益显著，展示出更大的潜力空间——更强的推理能力可以更有效地利用其迭代检索与反思循环。这一发现暗示，**智能体记忆方法的性能天花板尚未触及**，未来随着骨干模型能力的提升，这类方法可能释放出更大的潜力。

### 4. 适用边界与局限

MemoryAgentBench 的评估框架和结论存在以下明确的适用边界：

- **模态限制**：基准主要关注基于文本的增量交互，未涵盖多模态、持续实时流式输入等更复杂的记忆场景。四项核心能力（AR、TTL、LRU、SF）的定义和评价标准在多模态场景下的扩展仍是一个开放问题。
- **配置偏差**：商业记忆代理（Mem0、Cognee、Zep、MIRIX）在评估中统一使用块大小 4096，可能与它们各自的最佳配置存在偏差，这意味着对这些代理的评估结果可能低估了其真实潜力。
- **评估协议的阶段性**：测试时学习任务目前采用先吸收所有示例再统一评估的两段式协议，尚未完全模拟实时的在线学习与反馈循环，这限制了其对持续学习场景的代表性。
- **评价可靠性**：部分长文档任务（如 Summarization）依赖 LLM-as-a-judge 进行评价，尽管已与人类评价对齐，但在极端情况下仍可能存在偏差。

### 5. 开放问题与未来方向

基于上述分析，MemoryAgentBench 揭示了若干关键开放问题：

1. **统一记忆机制的架构设计**：如何在不牺牲单跳检索效率的前提下，同时实现可靠的长程多跳冲突消解？当前证据表明，长上下文模型的全量访问与 RAG 的精确检索之间存在互补性，未来的突破可能依赖于混合机制——例如在 RAG 中融入迭代推理，或在长上下文模型中引入结构化记忆更新策略。

2. **上下文碎片化的内部机制**：当块大小变化时，长程理解性能为何受到明显损害？其内部注意机制与上下文碎片化之间如何相互作用？这一问题的解答可能为设计更优的分块策略或记忆压缩方法提供理论指导。

3. **选择性遗忘的根本解决方案**：未来更强大的骨干模型是否能够通过单纯扩大窗口来解决选择性遗忘，还是必须依赖结构化的记忆更新策略？o4-mini 从 6K 到 32K 的性能崩溃表明，窗口扩大本身并非解药，记忆更新与推理的协同机制才是关键突破口。

4. **在线评估范式的建立**：能否在完全在线的交互式场景中评估测试时学习能力，而不仅限于分阶段离线评估？这将更真实地反映记忆智能体在持续部署环境中的表现。

5. **多模态记忆能力的定义与评估**：针对多模态输入的记忆智能体，四项核心能力的定义和评价标准应如何扩展？这需要构建新的数据集和评估协议。

## 原文 PDF

![[paperPDFs/ICLR_2026/Evaluating_Memory_in_LLM_Agents_via_Incremental_Multi_Turn_Interactions.pdf]]
