---
title: "REMem: Reasoning with Episodic Memory in Language Agent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/REMem_Reasoning_with_Episodic_Memory_in_Language_Agent.pdf
project_link: null
code_link: https://github.com/intuit-ai-research/REMem
openreview_forum_id: fugnQxbvMm
aliases:
- REMem
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "构建时间感知的混合记忆图（Gist + Fact）并采用工具驱动的代理推理（agentic inference），以实现结构化情景表示与灵活的迭代检索。"
primary_logic: "通过将情景记忆建模为时间戳明确的简短事件摘要（gists）和结构化事实三元组（facts）的混合图，并利用具有语义/词汇检索、图探索和流控制工具的代理式迭代推理，能够实现对交互经历的高效回忆和跨事件复杂推理。"
claims:
- "REMem在情景回忆和推理任务上分别取得了3.4%和13.4%的绝对提升，显著优于Mem0和HippoRAG 2等最先进系统。"
- "REMem是唯一在Test of Time基准上超过90%精确匹配分数的方法。"
- "移除Gist节点导致LoCoMo上LLM-J分数从76.2骤降至48.9，验证了事件摘要的核心作用。"
- "REMem在拒答行为上获得最高F1分数（63.96%），较Graphiti精度提升+34.4点，实现了更优的精确-召回平衡。"
---

# REMem: Reasoning with Episodic Memory in Language Agent

> [!tip] 核心洞察
> 通过将情景记忆建模为时间戳明确的简短事件摘要（gists）和结构化事实三元组（facts）的混合图，并利用具有语义/词汇检索、图探索和流控制工具的代理式迭代推理，能够实现对交互经历的高效回忆和跨事件复杂推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | REMem：语言代理中的情景记忆推理 |
| 英文题名 | REMem: Reasoning with Episodic Memory in Language Agent |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fugnQxbvMm) · [GitHub](https://github.com/intuit-ai-research/REMem) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | REMem |
| Dataset | LoCoMo, REALTALK, Complex-TR, Test of Time |

> [!tip] 效果简介
> - LoCoMo 上，F1 为 42.4 (REMem-I)，对比 39.0 (HippoRAG 2)，变化 +3.4。
> - REALTALK 上，LLM-J 为 65.3 (REMem-S)，对比 55.8 (HippoRAG 2)，变化 +9.5。
> - Complex-TR 上，LLM-J 为 89.6 (REMem-I)，对比 81.6 (Full-Context)，变化 +8.0。

## 概要

### 问题与瓶颈

语言代理在长时间交互中需要有效回忆和利用过往经历，但现有记忆系统普遍以语义记忆为主，缺乏对具体经历（情景）的**时空上下文建模**和**事件级推理能力**。具体而言，当前方法面临以下瓶颈：

- **扁平化检索**：基于向量相似度的单次检索难以捕捉事件间的时间顺序、因果关系和跨事件关联。
- **事件表征缺失**：缺乏对“何时发生何事”的结构化建模，导致无法有效回答涉及时间定位、事件比较和多跳推理的查询。
- **推理能力薄弱**：单步检索+生成的范式无法支持需要迭代探索和证据链构建的复杂情景推理。

### 核心方法：REMem

REMem 是一个**两阶段框架**，通过构建时间感知的混合记忆图并采用工具驱动的代理推理来解决上述问题：

1. **索引阶段**：将交互经历转化为**混合记忆图**，包含两类核心节点——带有时间戳的简洁事件摘要（**gists**）和附加时间限定符的结构化事实三元组（**facts**）。图结构通过关系边、上下文边和同义词边灵活连接这些节点，形成对情景经历的多粒度表征。

2. **代理推理阶段**：采用 **ReAct 风格代理**，配备三类精心设计的工具——语义/词汇检索工具、图探索工具和流控制工具。代理通过迭代调用这些工具，在记忆图上进行灵活的检索和推理，实现对交互经历的高效回忆和跨事件复杂推理。

### 方法定位

REMem 在记忆增强语言代理的方法谱系中占据独特位置：

- **相对于嵌入检索方法**（如 **NV-Embed-v2** (Lee et al., 2025a)、**Qwen3-Embed-8B** (Zhang et al., 2025)）：REMem 超越了单纯的向量相似度匹配，通过显式的事件摘要和结构化事实图支持时间感知和关系推理。
- **相对于结构化记忆方法**（如 **Mem0** (Chhikara et al., 2025)、**Graphiti** (Rasmussen et al., 2025)、**HippoRAG 2** (Gutierrez et al., 2025)）：REMem 引入了 gist 节点作为事件级记忆单元，并结合代理式迭代推理，而非单次图检索。
- **相对于提示式时间推理**（如 **TISER** (Bazaga et al., 2025)）：REMem 将时间推理能力内化到图结构和工具约束中，可与 TISER 等提示方法正交叠加。

### 主要结果

REMem 在情景记忆的两个递进能力维度上均取得显著提升：

- **情景回忆**：在 LoCoMo 和 REALTALK 基准上，REMem 较最强基线 HippoRAG 2 分别提升 **+3.4** 和 **+9.5** 个绝对百分点（LLM-J 分数）。
- **情景推理**：在 Complex-TR 和 Test of Time 基准上，REMem 较全上下文基线分别提升 **+8.0**（LLM-J）和 **+13.4**（精确匹配），且是唯一在 Test of Time 上超过 **90%** 精确匹配分数的方法。
- **拒答能力**：REMem 在不可回答问题上的精确-召回平衡最优，F1 达 **63.96%**，较 Graphiti 的精度提升 **+34.4** 个百分点。

消融实验进一步验证了设计的有效性：移除 gist 节点导致 LoCoMo 上 LLM-J 分数从 76.2 骤降至 48.9，确认了事件摘要是核心记忆载体；移除事实节点、同义词边或任一检索工具均导致性能退化，表明各组件的互补作用。



语言代理在与环境交互的过程中会积累大量经历，这些经历构成了**情景记忆**——即关于“何时、何地、发生了什么”的具体事件记忆。与存储一般性知识的语义记忆不同，情景记忆要求系统能够回忆特定交互中的时空上下文细节，并在此基础上进行跨事件的时序推理。例如，当用户询问“上周三会议中讨论的那个预算方案后来怎么样了？”，系统需要准确定位到具体会话片段，理解事件发生的先后顺序，并关联后续相关事件。

现有语言代理的记忆系统存在一个根本性瓶颈：**以语义记忆为主，缺乏对具体经历的情景上下文建模和事件级推理能力**。当前主流方案主要分为两类：

**嵌入检索式方法**（如基于 **NV-Embed-v2** (Lee et al., 2025a) 或 **Qwen3-Embed-8B** (Zhang et al., 2025) 的RAG系统）将交互历史编码为向量，通过语义相似度检索相关片段。这类方法虽然高效，但将记忆扁平化为无结构向量，丢失了事件之间的时序关系、因果关联和结构化事实信息，难以支持“先回忆再推理”的复杂查询。

**结构增强式方法**试图引入显式的记忆结构。**Mem0** (Chhikara et al., 2025) 在事实/语句层面存储信息，但缺乏有效的事件抽象和时间建模。**Graphiti** (Rasmussen et al., 2025) 构建时序知识图谱，但图谱粒度过细，难以捕捉事件级语义。**HippoRAG 2** (Gutierrez et al., 2025) 采用图检索增强生成，但其记忆表示仍以概念节点为主，缺少对完整事件片段及其时间上下文的系统建模。这些方法的共同缺陷在于：要么忽略了时间维度，要么仅在提示层面处理时序（如 **TISER** (Bazaga et al., 2025)），未能将时间感知深度嵌入记忆的表示和检索机制中。

上述缺口导致现有系统在两类关键能力上表现不足：一是**情景回忆**——准确提取过去经历中的时间和情境要素；二是**情景推理**——基于回忆结果进行跨时间线的多跳推理（如事件间关系判断、计数查询、序数查询等）。这构成了本文的核心动机：**如何构建一个能够对交互经历进行结构化表示，并支持灵活迭代检索的情景记忆系统？**



## 核心方法与创新机理

REMem 的核心创新在于对情景记忆（episodic memory）的**表示粒度、结构化方式和推理范式**三个维度进行了系统性重构，形成了一条从“语义向量匹配”到“事件级时空推理”的能力跃迁路径。

### 1. 事件表示：从扁平向量到时间感知的结构化摘要

现有记忆系统（如 Mem0、HippoRAG 2）主要依赖语义嵌入进行扁平检索，缺乏对交互经历中**事件边界**和**时间上下文**的显式建模。REMem 将情景记忆形式化为两类互补的表示单元：

- **Gist（事件摘要）**：从对话会话或事件语句中提取的简洁、人类可读的摘要，带有解析后的时间戳。这为每个交互片段提供了时间锚定的“记忆快照”。
- **Fact（结构化事实）**：提取为 `(主语, 谓语, 宾语)` 三元组，并附加上下文时间限定符，使事实与特定时间窗口绑定。

这一表示转换的因果效应在消融实验中得到了直接验证：**移除 Gist 节点导致 LoCoMo 上 LLM-J 分数从 76.2 骤降至 48.9**（Table 5），证明事件摘要是情景记忆的核心载体；移除 Fact 节点则在 Complex-TR 上造成一致但较小的下降（LLM-J 从 89.6 降至 87.2），表明结构化事实对多跳推理起辅助支撑作用。

### 2. 记忆结构：从单层存储到混合时空图

REMem 将上述表示组织为一个**类型多重图**（typed multigraph）$\mathcal{M} = (V, E)$，其结构设计直接服务于情景回忆与推理的差异化需求：

- **节点集分割**：$V = V_{\mathrm{gist}} \cup V_{\mathrm{phrase}}$，Gist 节点承载事件级语义，Phrase 节点承载细粒度实体/概念。
- **边集分割**：$E = E_{\mathrm{rel}} \cup E_{\mathrm{ctx}} \cup E_{\mathrm{syn}}$，分别建模实体间关系（含有效时间区间 $\tau(e)$）、Gist 与 Phrase 的上下文归属、以及同义关系。

这种混合图结构的关键优势在于**同时保留了事件摘要的叙事连贯性和结构化事实的可查询性**。消融实验证实，移除同义词边（$E_{\mathrm{syn}}$）会降低 F1 和 BLEU-1，说明同义关系建模对词汇鲁棒性和召回率有直接贡献。

### 3. 推理范式：从单次检索到工具驱动的代理式迭代推理

REMem 在推理侧的核心转变是将“检索-生成”的单次流水线替换为**ReAct 风格的代理式迭代推理**。代理通过三类精心设计的工具（Table 1）与记忆图交互：

- **检索工具**：语义检索（基于嵌入相似度）和词汇检索（基于关键词匹配），双路互补。
- **图探索工具**：沿关系边、上下文边遍历，实现跨事件关联。
- **流控制工具**：支持时间范围过滤（time-range operators），实现“心理时间旅行”式的时间推理。

这一范式转换的效果在推理任务上尤为显著：REMem-I（迭代模式）在 Complex-TR 上相较 Full-Context 基线提升 **+8.0 LLM-J**，在 Test of Time 上达到 **93.1% 精确匹配**，成为唯一超过 90% EM 分数的方法。消融实验中，移除语义检索或词汇检索工具均导致性能下降，验证了双路检索的互补性。

### 4. 时间推理：从提示工程到结构化时间约束

与仅通过提示进行时间推理的 TISER（Bazaga et al., 2025）不同，REMem 将时间推理**嵌入到图结构和工具签名中**：关系边携带有效时间区间，检索工具接受时间范围参数。这使得代理能够执行精确的时间过滤，而非依赖 LLM 在生成阶段对时间信息的模糊推断。这一设计在 Test of Time 基准上产生了 **+13.4%** 的绝对提升（相较 Full-Context），体现了结构化时间约束对精确时间推理的关键作用。



![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/004_Figure_2.jpg]]
*Figure 2: Overview of REMem. The indexing phase turns utterances into time-aware memory by extracting event gists and time-scoped facts (triples) and organizing them as a hybrid graph. The agentic inference phase invokes carefully curated tools over this graph to surface the most relevant gists and facts for reasoning in an iterative manner*

REMem 是一个面向语言代理的两阶段情景记忆框架，其核心设计围绕一个关键瓶颈展开：现有记忆系统以语义记忆为主，缺乏对具体交互经历的时空上下文建模与事件级推理能力。为此，REMem 将情景记忆形式化为**时间感知的事件表示**，并通过**索引**与**代理推理**两个阶段实现结构化记忆的构建与灵活检索。

### 两阶段流水线

整个框架的输入为带有时间戳的对话会话或事件语句，输出为对用户查询的自然语言回答。其处理流程如图 2 所示，分为以下两个阶段：

1.  **索引阶段**：将原始交互经历转化为一张**混合记忆图**（hybrid memory graph）。该阶段依次执行三个模块：
    -   **Gist 提取**：从事件语句或对话会话中提取带有时间戳的简洁事件摘要（gists）。
    -   **事实提取**：提取结构化事实三元组（主语、谓语、宾语），并附加上下文时间限定符，形成时间范围约束的事实表示。
    -   **图构建**：将 gist 节点与短语节点（phrase nodes）组织为一张类型多重图，并通过关系边、上下文边和同义词边连接，形成统一的结构化记忆存储。

2.  **代理推理阶段**：采用 ReAct 风格的代理，在混合记忆图上进行迭代式检索与推理。代理配备了三类精心设计的工具：
    -   **检索工具**：包括语义检索与词汇检索，分别从 gist 和事实两个维度召回相关记忆。
    -   **图探索工具**：利用上下文边和关系边在图中导航，从已检索到的节点出发，扩展获取关联的 gist 和事实。
    -   **流控制工具**：负责判断何时终止检索并输出最终答案。

推理过程遵循“检索→图探索→流控制”的三阶段协议：代理首先调用检索工具获取初始候选记忆，随后通过图探索工具扩展上下文，最后在流控制工具的协调下决定是否继续迭代或输出答案。代理的最大迭代步数基于小规模验证集从 2 到 5 之间选取。

### 模块间的数据流

索引阶段产出的混合记忆图是代理推理阶段的唯一数据源。推理时，用户查询首先触发检索工具在图节点上进行语义或词汇匹配，返回的 gist 和事实列表作为初始上下文；图探索工具进一步利用边关系扩展这些节点，补充关联信息；最终，流控制工具汇总所有检索到的记忆片段，交由底层 LLM 生成回答。整个过程中，gist 节点承载事件摘要这一核心记忆载体，而事实节点则为多跳推理提供结构化支撑——消融实验表明，移除 gist 节点会导致 LoCoMo 上的 LLM-J 分数从 76.2 骤降至 48.9，验证了其在框架中的核心地位。



### 3.1 索引阶段：混合记忆图构建

REMem 的记忆构建由三个串行模块组成，将对话或事件文本转化为结构化、时间感知的混合记忆图。

**Gist 提取** 是第一个模块，旨在从原始事件语句或对话会话中提取带有时间戳的简洁事件摘要。这些 gist 是人类可读的短句，概括了“谁在何时做了什么”，并附有解析后的时间信息。提取过程依赖 LLM 的提示模板（见 Figure 3），通过指令和示例引导模型输出结构化的事件摘要。

**Fact 提取** 模块随后从同一源文本中抽取结构化事实三元组（主语、谓语、宾语），并为每个三元组附加上下文时间限定符。这些事实以短语节点形式存储，捕捉事件中的实体关系细节（见 Figure 4 的提示模板）。

**图构建** 模块将上述两类信息组织为类型多重图。记忆图 $\mathcal{M}$ 的形式化定义如下：

$$\mathcal{M} = (V, E)$$

其中节点集 $V$ 被分割为两类互斥子集：

$$V = V_{\mathrm{gist}} \cup V_{\mathrm{phrase}}$$

- $V_{\mathrm{gist}}$：gist 节点，存储事件摘要及其时间戳
- $V_{\mathrm{phrase}}$：phrase 节点，存储从事实三元组中提取的实体和关系短语

边集 $E$ 被分割为三种语义边类型：

$$E = E_{\mathrm{rel}} \cup E_{\mathrm{ctx}} \cup E_{\mathrm{syn}}$$

- **关系边** $E_{\mathrm{rel}}$：连接主体和客体 phrase 节点，形式为 $e = (p_s, r, p_o, \tau(e))$，其中 $p_s$ 和 $p_o$ 分别为主体与客体短语，$r$ 为谓语关系，$\tau(e)$ 为有效时间区间
- **上下文边** $E_{\mathrm{ctx}}$：连接 gist 节点与来自同一源块的 phrase 节点，形式为 $e = (g, p)$，保持事件上下文与实体事实的关联
- **同义词边** $E_{\mathrm{syn}}$：连接语义等价的 phrase 节点，用于提升词汇鲁棒性和召回率

### 3.2 推理阶段：代理式迭代检索

REMem 采用 ReAct 风格的代理推理引擎，通过精心设计的工具集在混合记忆图上进行迭代检索。工具分为三类（见 Table 1）：

1. **检索工具**：包括语义检索（基于嵌入向量相似度）和词汇检索（基于关键词匹配），两者互补输出 gist 列表和 fact 列表
2. **图探索工具**：支持沿关系边、上下文边和同义词边进行图遍历，并支持时间范围过滤操作
3. **流控制工具**：用于判断检索是否充分并输出最终答案

推理遵循三阶段协议：首先通过检索工具获取候选 gist 和 fact，然后利用图探索工具沿边扩展相关上下文，最后通过流控制工具决定是否继续迭代或终止并生成回答。最大迭代步数基于小型验证集从 2 到 5 中选择。

### 3.3 关键设计要点

- **时间感知**：gist 节点携带时间戳，关系边包含有效时间区间 $\tau(e)$，工具参数支持时间范围运算符，实现“心理时间旅行”式的时间过滤
- **双路检索互补**：语义检索和词汇检索分别捕捉深层语义和表层词汇匹配，消融实验表明移除任一工具均导致性能下降
- **混合图结构**：gist 节点提供事件级上下文摘要，phrase 节点提供细粒度事实，二者通过上下文边关联，形成多粒度的记忆表示



## 实验与关键发现

### 评估设置

为系统评估情景记忆能力，REMem在四个基准上进行了测试，覆盖两类渐进式能力：
- **情景回忆（Episodic Recollection）**：在LoCoMo（1,986条查询）和REALTALK（728条查询）上评估，指标为F1、BLEU-1和LLM-as-a-Judge（LLM-J）分数。
- **情景推理（Episodic Reasoning）**：在Complex-TR（1,000条查询）和Test of Time（2,800条查询）上评估，指标为F1、BLEU-1、LLM-J和精确匹配（EM）。

基线方法包括：强嵌入模型（**NV-Embed-v2**，Lee et al., 2025a；**Qwen3-Embed-8B**，Zhang et al., 2025）、结构增强记忆方法（**Mem0**，Chhikara et al., 2025；**Graphiti**，Rasmussen et al., 2025；**HippoRAG 2**，Gutierrez et al., 2025）、基于提示的时间推理方法**TISER**（Bazaga et al., 2025），以及Full-Context和Oracle Message两个参考基线。所有实验统一使用GPT-4.1-mini作为默认LLM，nvidia/NV-Embed-v2作为嵌入模型。REMem提供两种推理模式：**REMem-S（单步）**仅执行一次语义检索后生成，**REMem-I（迭代）**自主选择工具进行多步推理，最大步数根据小型验证集在2到5之间选择。

---

### 主实验结果

**情景回忆任务**（Table 3）：REMem-S在REALTALK上取得最高F1（26.2）、BLEU-1（19.2）和LLM-J（65.3），较HippoRAG 2的LLM-J提升+9.5个点。在LoCoMo上，REMem-I以F1 42.4领先HippoRAG 2（39.0），绝对提升+3.4个点。值得注意的是，REMem-I在LoCoMo上的LLM-J达到76.2，显著高于所有结构增强记忆方法。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/007_Table_3.jpg]]
*Table 3: Performance (%) on episodic recollection task. The highest value and second-highest value in each column are bold and underlined, respectively. Numbers are means with 95% bootstrap confidence intervals as subscripts and superscripts. The same applies to the tables below*

**情景推理任务**（Table 4）：REMem-I配合TISER提示在Complex-TR上取得最优成绩（F1 90.6，BLEU-1 86.0，LLM-J 92.0），较Full-Context的LLM-J提升+8.0个点。在Test of Time上，REMem-I以93.1的EM分数成为**唯一超过90%的方法**，较Full-Context（79.7）提升+13.4个点，较NV-Embed-v2（60.0）提升+33.1个点。REMem-I相比REMem-S在推理任务上展现出显著优势（Complex-TR LLM-J +7.0），验证了代理式迭代检索对多步推理的关键作用。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/008_Table_4.jpg]]
*Table 4: Performance (%) on episodic reasoning tasks*

---

### 消融实验

Table 5展示了图结构和检索工具的消融结果，揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/009_Table_5.jpg]]
*Table 5: Ablation study on LoCoMo and Complex-TR, regarding the graph structure and the usage of retrieval tools*

**Gist节点是核心记忆载体**：移除Gist节点导致LoCoMo上LLM-J从76.2骤降至48.9（-27.3点），Complex-TR上从89.6降至81.5（-8.1点）。这表明事件摘要承载了情景记忆的主要信息密度，结构化事实无法单独弥补其缺失。

**Fact节点辅助多跳推理**：移除Fact节点在Complex-TR上造成LLM-J从89.6降至87.2（-2.4点），影响虽小于Gist但具有一致性。在需要跨事件关联的推理场景中，结构化三元组提供了精确的关系锚点。

**同义词边增强词汇鲁棒性**：移除同义词边降低了两个数据集上的F1和BLEU-1，说明建模同义关系有助于弥合查询与记忆之间的词汇差异，提升召回率。

**双路检索互补**：分别移除语义检索工具或词汇检索工具均导致性能下降，验证了两者在覆盖语义相似性和精确词汇匹配上的互补性。语义检索擅长捕捉释义变体，词汇检索则精确定位特定实体和短语。

---

### 拒答行为分析

LoCoMo数据集中有446条不可回答的对抗性查询（Table 6）。REMem在拒答行为上取得最高F1分数（63.96%），精度达到73.3%，较Graphiti的38.9%提升**+34.4个点**，召回率为56.7%。相比之下，Graphiti虽召回率最高（83.6%），但精度极低（38.9%），存在严重过度拒答问题；Mem0则几乎不拒答（精度100%但召回率仅0.7%）。REMem在精确-召回平衡上显著优于两者，表明其时间感知的记忆结构能更准确地判断信息是否存在于交互历史中。

---

### 人类评估验证

在100条LoCoMo样本上，LLM-J与人类评估的一致性达到93%（Table 7），验证了LLM-as-a-Judge作为自动评估指标的可靠性。这一高一致性为前述基于LLM-J的实验结论提供了可信度支撑。

---

### 错误模式分析

对REMem在LoCoMo上的错误进行归类（Section 6.5），主要失败模式包括：
- **多实体列表不完整或不一致**（约21%）：当查询涉及多个实体时，代理检索可能遗漏部分实体或产生不一致的聚合结果。
- **时间偏移方向错误**（约18%）：在处理`before`/`after`等模糊时间术语时，工具调用的时间范围约束可能出现方向性偏差，导致错误的包含或排除。
- 其余错误分布在事实提取不完整、同义词匹配失败等类别中。

与NV-Embed-v2的对比案例（Table 8）进一步揭示了REMem的优势与局限：REMem在需要消歧和时间协调的问题上表现更优，而NV-Embed-v2在直接的时间区间计算问题上更准确，说明混合图结构在处理复杂语义关联时具有优势，但简单的数值时间推理仍有改进空间。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/005_Table_1.jpg]]
*Table 1: Curated tools and their signature. Both the retrieval and graph exploration tools output two sets of results: a list of gists and a list of facts. See Appendix D for prompts and demonstrations*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_fugnQxbvMm/figures/006_Table_2.jpg]]
*Table 2: The statistics of sampled datasets*



## 定位与知识库关联

### 1. 与现有基线的关系

REMem 的提出针对的是现有语言代理记忆系统的一个结构性缺口：**语义记忆丰富而情景记忆贫瘠**。主流的记忆增强方法可大致分为三类，REMem 在每一类的基础上做出了明确的改进或补充。

**大型嵌入模型与朴素 RAG。** 以 **NV-Embed-v2**（Lee et al., 2025a）和 **Qwen3-Embed-8B**（Zhang et al., 2025）为代表的强嵌入模型构成了检索增强生成（RAG）的骨干。这类方法将历史交互编码为向量，通过语义相似度检索相关片段。其核心局限在于：向量检索是扁平的，缺乏对事件边界、时间顺序和结构化关系的显式建模。REMem 保留了语义检索作为其代理推理工具箱中的一个基础工具，但将其嵌入到一个更丰富的图结构中，从而弥补了纯向量检索在时间定位和多跳关联上的不足。

**结构增强的记忆方法。** 这是与 REMem 最直接相关的基线族。

- **Mem0**（Chhikara et al., 2025）引入了结构化记忆，但主要关注用户偏好和事实的持久存储，缺乏对事件级时间上下文的精细建模。
- **Graphiti**（Rasmussen et al., 2025）构建了时间感知的知识图谱，以三元组形式存储事实并支持时间约束检索。REMem 在事实三元组的表示上与之有相似之处，但关键区别在于：Graphiti 缺乏对事件摘要（gist）的显式建模，而消融实验表明，移除 gist 节点会导致 LoCoMo 上 LLM-J 分数从 76.2 骤降至 48.9（Table 5），证明事件级摘要承载了不可替代的情景信息。此外，在拒答行为上，REMem 的 F1 分数（63.96%）较 Graphiti 的精度提升 +34.4 点（Table 6），表明混合图结构带来了更优的精确-召回平衡。
- **HippoRAG 2**（Gutierrez et al., 2025）采用图检索增强生成，但其图结构以概念节点为主，未将事件摘要作为一等公民建模。在情景回忆任务上，REMem 较 HippoRAG 2 取得了 3.4% 的 F1 绝对提升（LoCoMo），在 REALTALK 上 LLM-J 领先 9.5 点（Table 3）。

**基于提示的时间推理方法。** **TISER**（Bazaga et al., 2025）通过提示工程增强 LLM 的时间推理能力，与 REMem 的方法正交。REMem 在推理阶段可选地集成 TISER 提示，在 Complex-TR 上获得了额外的性能增益（LLM-J 从 89.6 提升至 92.0，Table 4），表明结构化记忆与提示增强可以互补。

**参考上界。** Full-Context（全上下文窗口生成）和 Oracle Message（给定真实相关片段后生成）作为参考基线，不构成记忆方法。REMem-I 在情景推理任务上以 8.0 点的 LLM-J 优势超越 Full-Context（Complex-TR），并在 Test of Time 上以 93.1% 的精确匹配分数成为唯一超过 90% 的方法（Table 4），证明精心设计的记忆检索可以优于简单地将所有上下文塞入窗口。

### 2. 适用边界

REMem 的设计假设决定了其有效的作用范围：

- **适用场景：** 需要跨越多个交互会话进行事件回忆和推理的长期对话代理，如个人助手、客户服务历史分析、叙事理解等。其时间感知的混合图结构特别适合回答“某时某地发生了什么”“事件 A 和事件 B 之间隔了多久”等情景性问题。
- **数据形态：** 输入为带有时间戳的对话语句或事件描述流。当前实现假设批量索引，即所有历史数据在推理前已完成图构建。
- **推理模式：** 代理迭代推理（REMem-I）在需要多步检索和跨事件关联的复杂问题上显著优于单步检索（REMem-S），但在简单的事实查找上，单步模式可能已足够且更高效。

### 3. 局限与已知失效模式

基于论文报告的消融实验、错误分析和设计选择，可识别以下局限：

**时间推理的精度边界。** 尽管 REMem 在 Test of Time 上取得了 93.1% 的 EM 分数，但错误分析揭示约 18% 的错误源于时间偏移方向判断失误（Section 6.5）。模糊时间术语（如“before”“after”）在转化为工具调用中的时间范围参数时，可能产生不精确的包含或排除，导致遗漏相关事件或引入无关事件。

**多实体列表的不完整性。** 约 21% 的错误归因于多实体列表的生成不完整或不一致（Section 6.5）。当问题要求枚举满足某条件的所有实体时，迭代检索可能过早终止或遗漏部分实体。

**构建阶段的依赖与开销。** 记忆图的构建依赖 LLM 进行 gist 提取和 fact 提取，提取质量直接影响下游推理。LLM 的幻觉或不一致可能污染图结构。此外，代理推理的迭代过程引入了额外的计算开销：REMem-I 的令牌消耗随步数线性增长（Table 20），不适用于极低延迟的实时应用。

**缺乏流式评估。** 当前所有实验基于预构造的标准基准（LoCoMo、REALTALK、Complex-TR、Test of Time），缺乏对持续流式更新的真实对话场景的评估。在对话进行中增量构建和更新记忆图的鲁棒性尚未验证。

### 4. 开放问题

论文明确指出了若干未来方向，结合方法设计可进一步延伸：

- **流式记忆构建。** 如何将 REMem 从批量索引扩展为流式系统，以持续处理增量到来的对话和事件，是实际部署的关键挑战。这涉及增量图更新、过时信息的淘汰策略以及索引与推理的并发调度。
- **时间比较的精确对齐。** 将“before”“after”等模糊时间关系与工具的时间范围约束精确对齐，可能需要更精细的时间逻辑表示或约束求解机制。
- **多模态扩展。** 当前记忆表示限于文本事件。能否将 gist 和 fact 的提取机制扩展到多模态经历（图像、音频）是值得探索的方向。
- **复杂环境中的长期记忆。** 在多代理协作、游戏等更复杂的交互环境中，混合图结构是否仍能有效支撑长期情景记忆，以及记忆的遗忘与巩固策略如何设计，仍是开放问题。
- **效率优化。** 如何通过缓存、检索剪枝或更轻量的代理策略降低迭代推理的令牌消耗，是走向实用的必经之路。



## 原文 PDF

![[paperPDFs/ICLR_2026/REMem_Reasoning_with_Episodic_Memory_in_Language_Agent.pdf]]
