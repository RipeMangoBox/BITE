---
title: "MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured Long Reasoning Chains"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MC_Search_Evaluating_and_Enhancing_Multimodal_Agentic_Search_with_Structured_Long_Reasoning_Chains.pdf
project_link: https://mc-search-project.github.io
code_link: null
openreview_forum_id: JEGDp1E4OH
aliases:
- SA
- MC-Search
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入过程级监督（SEARCH-ALIGN）和高质量逐步推理链（HAVE过滤），通过提供精确的子问题、检索动作和中间证据的监督信号，直接提升模型在规划、多模态检索和推理连贯性上的表现。"
primary_logic: "通过构建包含多样化推理拓扑的高质量逐步标注基准，并设计过程级评估指标及相应的过程级微调框架，不仅可以准确诊断模型在多跳推理中的短板，还能有效训练开源模型，使其达到与闭源模型相当的水平。"
claims:
- "MC-SEARCH 是首个提供长程、逐步标注推理链的多模态代理RAG基准。"
- "HAVE 过滤确保每个推理跳跃的必要性和非冗余性，最终得到3333个高质量样本，平均3.7跳。"
- "SEARCH-ALIGN 过程级微调大幅提升开源模型性能：Qwen2.5-VL-7B 的 F1 平均提升 13.7，HPS 提升 16.0。"
- "并行图文分叉（Parallel Image-Text Fork）是所有模型最难的拓扑，凸显跨模态并行规划的弱点。"
---

# MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured Long Reasoning Chains

> [!tip] 核心洞察
> 通过构建包含多样化推理拓扑的高质量逐步标注基准，并设计过程级评估指标及相应的过程级微调框架，不仅可以准确诊断模型在多跳推理中的短板，还能有效训练开源模型，使其达到与闭源模型相当的水平。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MC-Search：用结构化长推理链评估和增强多模态代理搜索 |
| 英文题名 | MC-Search: Evaluating and Enhancing Multimodal Agentic Search with Structured Long Reasoning Chains |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=JEGDp1E4OH) · [Project](https://mc-search-project.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | SEARCH-ALIGN |
| Dataset | MC-SEARCH (Image-Initiated Chain), MC-SEARCH (Parallel Image-Text Fork) |

> [!tip] 效果简介
> - MC-SEARCH (Image-Initiated Chain) 上，F1 为 45.70 (Qwen2.5-VL-7B + SEARCH-ALIGN)，对比 26.30 (Qwen2.5-VL-7B)，变化 +19.40。
> - MC-SEARCH (Image-Initiated Chain) 上，HPS 为 33.59 (Qwen2.5-VL-7B + SEARCH-ALIGN)，对比 16.51 (Qwen2.5-VL-7B)，变化 +17.08。
> - MC-SEARCH (Parallel Image-Text Fork) 上，F1 为 32.73 (Qwen2.5-VL-7B + SEARCH-ALIGN)，对比 22.94 (Qwen2.5-VL-7B)，变化 +9.79。

## 概要

### 问题背景与瓶颈

多模态检索增强生成（MM-RAG）在开放域问答中展现出巨大潜力，但现有基准普遍存在两个关键局限：**评估粒度粗**——仅以最终答案正确性为评判标准，无法反映模型在逐步规划、多模态检索和过程级推理上的真实能力；**推理链短**——局限于1–2跳的简单检索，难以覆盖需要跨模态、长程依赖的真实场景。这导致我们无法准确诊断多模态大语言模型（MLLM）在代理式搜索中的瓶颈，也无法为模型改进提供有效的过程级监督信号。

### 核心贡献

MC-Search 从基准构建和模型训练两个维度系统性地回应了上述挑战：

1. **首个长程、逐步标注的多模态代理RAG基准**：MC-Search 提供了覆盖五种代表性推理拓扑的3,333个高质量样本，平均推理链长3.7跳，每个样本均配有完整的黄金推理轨迹——包含子问题序列、检索模态、支撑证据和中间答案。通过HAVE（Hop-wise Attribution and Verification of Evidence）过滤机制，确保每一步推理的必要性和非冗余性。

2. **过程级评估体系**：除传统F1外，引入Hit per Step（HPS）和Rollout Deviation（RD）两个过程级指标，分别衡量黄金证据的恢复率和推理步长的偏差，实现对规划能力和检索行为的精细诊断。

3. **SEARCH-ALIGN过程级微调框架**：利用验证后的推理链轨迹，为开源模型提供包含子问题生成、检索动作选择和证据整合的逐步监督信号，使开源模型在代理搜索能力上大幅逼近闭源模型。

### 关键发现

- **并行图文分叉（Parallel Image-Text Fork）是所有模型最困难的推理拓扑**，暴露了跨模态并行规划能力的普遍短板。
- **SEARCH-ALIGN带来显著增益**：以Qwen2.5-VL-7B为例，在Image-Initiated Chain上F1提升19.40、HPS提升17.08；在Parallel Image-Text Fork上F1提升9.79。同时，Rollout Deviation降至约1.0，表明过/欠检索问题得到有效抑制。
- **主要错误类型集中在检索失败（84.7%）、幻觉实体/属性（75.8%）和步骤遗漏（74.3%）**，SEARCH-ALIGN对这些错误均有明显缓解。

### 方法定位

MC-Search 的方法论贡献可归结为“**以过程级标注驱动过程级评估与过程级训练**”。它不改变底层MLLM架构或检索器，而是在统一的代理式MM-RAG管道中，通过引入高质量推理链作为监督信号，实现从最终答案对齐到推理轨迹对齐的范式升级。这一思路为多模态代理搜索领域提供了可复现的评估标准和可迁移的训练策略。



多模态大语言模型（MLLM）在视觉问答、文档理解等任务上取得了显著进展，但其在需要主动搜索、整合外部多模态知识的长程推理场景中仍面临根本性挑战。现实世界中的复杂查询——例如“这张照片中的建筑所在城市，其市花在哪个国家被定为国花？”——要求模型跨越文本与图像模态，执行多跳检索与推理，而非仅依赖参数化知识或单次检索。

现有评估基准的缺口集中体现在三个层面。其一，当前多模态检索增强生成（MM-RAG）基准（如 WebQA、MMCoQA、MultiModalQA）仅评估最终答案的正确性，且局限于 1–2 跳的简单检索链，忽视了长程跨模态推理中逐步规划、检索与过程级推理质量的评估。其二，缺乏对多样化推理拓扑结构的覆盖——真实查询往往涉及图像链、文本链、并行图文分叉等不同模态依赖模式，而现有基准未能系统刻画这些拓扑差异。其三，没有基准提供逐步标注的黄金推理轨迹，导致无法诊断模型在哪个推理环节出错，也无法为过程级监督训练提供信号。

上述缺口使得一个核心问题悬而未决：**MLLM 是否真正具备在多模态知识库中执行长程、结构化搜索推理的能力？** 闭源模型可能通过强大的内部规划能力部分弥补这一短板，但开源模型在此类任务上的表现及其可训练性仍不明确。

针对这些问题，本文提出 **MC-Search**——首个面向多模态代理搜索的基准，提供包含多样化推理拓扑的长程、逐步标注推理链。该基准不仅支持最终答案评估，还引入了过程级指标（命中步数 HPS、展开偏差 RD），使得对模型规划与检索行为的细粒度诊断成为可能。在此基础上，本文进一步提出 **SEARCH-ALIGN** 过程级微调框架，利用验证后的推理轨迹对开源模型进行监督训练，旨在缩小其与闭源模型的差距。



## 核心方法与创新机理

MC-Search 的核心创新在于将多模态代理搜索的评估与训练从**最终答案正确性**推进到**过程级推理质量**，并为此构建了完整的基准-评估-微调闭环。

### 1. 从答案监督到过程监督：SEARCH-ALIGN 框架

现有工作仅以最终答案作为监督信号，模型在长程推理中“如何规划”、“何时检索何种模态”、“如何利用中间证据”等关键行为完全缺乏指导。MC-Search 提出的 **SEARCH-ALIGN** 框架将监督粒度从“答案级”提升到“步骤级”，其 changed slot 如下：

| 监督维度 | 基线方法（仅答案监督） | SEARCH-ALIGN（过程监督） |
|---------|---------------------|----------------------|
| 监督信号 | 最终答案 A | 逐步轨迹 `{(q_t, m_t, r_t, a_t)}` |
| 覆盖内容 | 答案正确性 | 子问题生成、检索动作选择、证据获取、中间答案 |
| 训练数据 | 问答对 | 经 HAVE 过滤的推理链 + Gemini-2.5-Flash 生成的推理思维 |

具体而言，每条训练样本被扩充为完整的推理轨迹，包含：
- **子问题** `q_t`：模型在每一步需要解决的具体子目标
- **检索动作** `m_t`：自适应选择的三种检索动作之一（文本检索、以文搜图、以图搜图）
- **证据** `r_t`：检索器返回的 top-1 证据
- **中间答案** `a_t`：基于当前证据的阶段性推理结果

此外，每条推理链还通过 **Gemini-2.5-Flash** 生成显式的推理思维（reasoning thoughts），解释如何将推理锚定在证据上并连接相邻跳跃。这种过程级监督直接作用于模型的规划、检索和推理连贯性，是性能提升的核心因果杠杆。

### 2. 过程级评估指标：HPS 与 RD

为匹配过程级监督，MC-Search 引入了两个过程级评估指标，突破传统 F1 只能衡量最终答案的局限：

- **Hit per Step (HPS)**：衡量预测推理图中被准确恢复的黄金步骤比例。公式为：
  $$
  \mathrm{HPS}(\hat{\mathcal{G}}, \mathcal{G}) = \frac{1}{|\mathcal{G}|} \big| \{ (t, t') \mid r_t \in \mathcal{G}, \hat{r}_{t'} \in \hat{\mathcal{G}}, \hat{r}_{t'} = r_t \} \big|
  $$
  该指标直接评估模型是否在正确的步骤检索到了正确的证据，而非仅关注最终答案。

- **Rollout Deviation (RD)**：衡量预测推理图与黄金推理图的步骤长度偏差：
  $$
  \mathrm{RD}(\hat{\mathcal{G}}, \mathcal{G}) = \big| |\hat{\mathcal{G}}| - |\mathcal{G}| \big|
  $$
  RD 反映模型的过检索（正向偏差）或欠检索（负向偏差）程度，是诊断规划质量的关键指标。

### 3. 高质量推理链的构建：HAVE 过滤机制

过程级监督的有效性高度依赖训练数据的质量。MC-Search 设计了 **HAVE（Hop-wise Attribution and Verification of Evidence）** 过滤机制，通过两个维度确保每个推理跳跃的必要性和非冗余性：

- **上下文效用（Context Utility）**：测量移除某跳证据后 F1 分数的下降，公式为：
  $$
  \mathrm{Util}(t) = \mathrm{F1}(\mathcal{C}) - \mathrm{F1}(\mathcal{C} \setminus r_t)
  $$
  若移除后性能无显著下降，则该跳为冗余步骤。

- **导航作用（Navigational Role）**：检查中间答案中的实体是否出现在下游子问题中：
  $$
  \mathbf{Nav}(t) = \begin{cases} 1, & \text{if } \mathrm{Ent}(a_t) \cap \mathrm{Ent}(q_{t+1:T}) \neq \emptyset \\ 0, & \text{otherwise} \end{cases}
  $$
  若中间答案实体与后续推理无关，则该跳可能是虚假步骤。

经过 HAVE 过滤，最终数据集包含 **3,333 个高质量样本**，平均 **3.7 跳**，覆盖五种代表性推理拓扑（Image-Initiated Chain、Text-Initiated Chain、Text-Only Chain、Multi-Images Fork、Parallel Image-Text Fork），为过程级监督提供了可靠的数据基础。

### 4. 创新效果：开源模型逼近闭源水平

SEARCH-ALIGN 的过程级监督在开源模型上取得了显著增益：

- **Qwen2.5-VL-7B**：F1 平均提升 **+13.7**，HPS 提升 **+16.0**，RD 降低 **3.1**，在 Image-Initiated Chain 上 F1 从 26.30 跃升至 45.70（接近 Gemini-2.5-Pro 的 47.61）
- **InternVL3.5-8B**：F1 平均提升 **+2.8**，HPS 提升 **+12.0**，RD 降低 **0.6**

值得注意的是，在最具挑战性的 **Parallel Image-Text Fork** 拓扑上，所有模型均达到最低 F1 和 HPS，凸显跨模态并行规划仍是当前多模态代理搜索的核心瓶颈，也是 SEARCH-ALIGN 未来优化的重点方向。



![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/004_Figure_2.jpg]]
*Figure 2: Overview of MC-SEARCH benchmark and evaluation. Left: Benchmark covering five reasoning topologies, filtered via the hop-wise attribution and verification of evidence (HAVE) process. Right: Multimodal agentic RAG pipeline, where an MLLM iteratively generates sub-queries and actions, retrieves multimodal evidence, reasons over the retrieved information, and integrates it to produce the final answer. Our framework further aligns predicted reasoning chains with golden trajectories to assess chain-level retrieval and planning*

MC-Search 的完整框架由两个核心组件构成：一个用于评估和训练的高质量基准 **MC-SEARCH**，以及一个统一的**多模态代理 RAG 管道**。前者提供带逐步标注的长推理链，后者则作为所有模型（包括闭源和开源骨干）的统一推理与评估平台。两者通过过程级监督框架 **SEARCH-ALIGN** 连接，形成“基准构建—管道评估—过程对齐”的闭环。

### 基准构建：从推理拓扑到高质量推理链

MC-SEARCH 基准的核心目标是提供长程、逐步标注的多模态推理链，以弥补现有数据集仅覆盖 1–2 跳简单检索的不足。其构建过程如图 2（左）所示，包含三个关键阶段：

1. **推理拓扑设计**：为刻画多模态知识在长程搜索推理中的交互模式，设计了五种代表性推理拓扑：**Image-Initiated Chain**、**Text-Initiated Chain**、**Text-Only Chain**、**Multi-Images Fork** 和 **Parallel Image-Text Fork**。这些拓扑覆盖了从纯文本到图文并行分叉的多样化信息依赖结构。

2. **逐步推理链生成**：每个样本被形式化为一个推理图 $\mathcal{G}(Q, A) = \{(q_t, m_t, r_t, a_t)\}_{t=1}^T$，其中 $q_t$ 为子问题，$m_t$ 为检索模态，$r_t = \mathcal{R}(q_t, m_t)$ 为检索到的证据，$a_t$ 为中间答案，最终答案 $A$ 由聚合函数 $f$ 产生。这种结构化表示使得每一步的规划、检索和推理都可被独立追踪和评估。

3. **HAVE 过滤机制**：为确保推理链中每一步的必要性和非冗余性，引入 **HAVE（Hop-wise Attribution and Verification of Evidence）** 过滤。该机制通过两个指标对每一步进行验证：
   - **Context Utility**：$\mathrm{Util}(t) = \mathrm{F1}(\mathcal{C}) - \mathrm{F1}(\mathcal{C} \setminus r_t)$，测量移除某跳证据后 F1 分数的下降，评估该步对最终答案的贡献。
   - **Navigational Role**：$\mathbf{Nav}(t) = 1$ 当且仅当中间答案 $a_t$ 中的实体出现在下游子问题 $q_{t+1:T}$ 中，评估该步在推理链中的导航作用。

   只有同时满足上下文效用和导航作用的步骤才会被保留，从而过滤掉幻觉和冗余步骤。经过 HAVE 过滤后，最终得到 **3,333 个高质量样本**，平均链长为 **3.7 跳**，知识库包含 **389,750 张图像**。

### 代理 RAG 管道：迭代规划—检索—推理

统一的代理 MM-RAG 管道（图 2 右）将多模态搜索增强推理建模为一个迭代过程，包含三个核心模块：

1. **Sub-query and Action Generation（子查询与动作生成）**：MLLM 根据当前推理状态生成子目标 $q_t$，并自适应选择三种检索动作之一：文本搜索（以文本查询）、图像搜索（以文本查询）或图像搜索（以输入图像）。这种自适应动作选择使模型能够根据推理需求灵活切换检索模态。

2. **Evidence Acquisition（证据获取）**：执行模态感知检索，对每个子查询保留 top-1 证据（通过查询-答案相似度排序）。管道支持扩展到 top-3 或 top-5 检索，但默认配置为 top-1，以模拟真实代理搜索的效率约束。

3. **Iterative Reasoning and Synthesis（迭代推理与合成）**：子答案 $a_t$ 及其证据被反馈回模型以指导下一步规划，形成“规划—检索—推理”的循环，直至输出最终答案。

该管道作为所有骨干模型的统一推理框架，确保闭源模型（GPT-4o-Mini、Gemini-2.5-Flash/Pro、Claude-3.7-Sonnet）和开源模型（InternVL3.5-8B、Qwen2.5-VL-7B）在完全相同的检索器和提示下进行公平比较。

### 过程级评估与对齐

为诊断模型在推理链层面的表现，框架定义了三个过程级指标：

- **Hit per Step (HPS)**：$\mathrm{HPS}(\hat{\mathcal{G}}, \mathcal{G}) = \frac{1}{|\mathcal{G}|} \big| \{(t, t') \mid r_t \in \mathcal{G}, \hat{r}_{t'} \in \hat{\mathcal{G}}, \hat{r}_{t'} = r_t\} \big|$，衡量黄金步骤中被预测图准确恢复的比例。
- **Rollout Deviation (RD)**：$\mathrm{RD}(\hat{\mathcal{G}}, \mathcal{G}) = \big| |\hat{\mathcal{G}}| - |\mathcal{G}| \big|$，衡量预测与黄金推理图的步骤长度差，反映过检索或欠检索程度。
- **ΔF1**：$\Delta\mathrm{F1} = \mathrm{F1} - \mathrm{F1}_{\mathrm{w/o}\ \mathcal{R}}$，衡量代理 RAG 相对于模型参数知识的性能增益。

**SEARCH-ALIGN** 利用这些逐步标注轨迹提供过程级监督：将每个推理图扩展为由 Gemini-2.5-Flash 生成的显式推理思路（解释如何将推理建立在证据之上并连接相邻跳跃），从而在子问题、检索动作、证据和中间答案四个维度上对齐预测轨迹与黄金轨迹。这种过程级监督与仅使用最终答案的传统监督形成鲜明对比，是开源模型性能大幅提升的关键机制。



### 代理式多模态RAG管道

MC-SEARCH的评估与训练均基于统一的代理式多模态RAG管道，该管道将搜索增强推理建模为三个迭代模块：

1. **子查询与动作生成（Sub-query and Action Generation）**：模型根据当前推理状态生成子目标，并自适应选择检索动作——文本检索（以文本查询）、图像检索（以文本查询）或图像检索（以输入图像查询）。
2. **证据获取（Evidence Acquisition）**：执行模态感知检索，对每个子查询保留查询-答案相似度最高的 top-1 证据。
3. **迭代推理与合成（Iterative Reasoning and Synthesis）**：将子答案及其证据反馈给模型以指导下一步规划，形成“规划—检索—推理”的闭环，直至输出最终答案。

### 推理图的形式化定义

MC-SEARCH将多跳推理过程形式化为推理图 $\mathcal{G}$：

$$\mathcal { G } ( Q , A ) = \{ ( q _ { t } , m _ { t } , r _ { t } , a _ { t } ) \} _ { t = 1 } ^ { T } , \quad r _ { t } = \mathcal { R } ( q _ { t } , m _ { t } ) , \quad A = f ( \{ a _ { t } \} _ { t = 1 } ^ { T } )$$

其中 $q_t$ 为第 $t$ 步的子问题，$m_t$ 为检索模态，$r_t = \mathcal{R}(q_t, m_t)$ 为检索到的证据，$a_t$ 为中间答案，$A$ 由聚合函数 $f$ 从所有中间答案中产生。该定义将多跳推理结构化为可逐步监督的轨迹。

### HAVE过滤机制的关键公式

为保证推理链中每一步的必要性和非冗余性，HAVE（Hop-wise Attribution and Verification of Evidence）引入两个核心度量：

**上下文效用（Context Utility）**：测量移除某跳证据后F1分数的下降幅度，用于判断该跳对最终答案的贡献：

$$\mathrm { U t i l } ( t ) = \mathrm { F } 1 ( \mathcal { C } ) - \mathrm { F } 1 ( \mathcal { C } \setminus r _ { t } )$$

其中 $\mathcal{C}$ 为完整证据上下文集合。效用值过低意味着该步证据对答案生成贡献微弱，可能为冗余步。

**导航作用（Navigational Role）**：检查中间答案的实体是否出现在下游子问题中，判断该步是否承担推理链的衔接功能：

$$\mathbf { N a v } ( t ) = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f } \ \mathrm { E n t } ( a _ { t } ) \cap \mathrm { E n t } ( q _ { t + 1 : T } ) \neq \emptyset , } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right.$$

其中 $\mathrm{Ent}(a_t)$ 为中间答案中的实体集合，$\mathrm{Ent}(q_{t+1:T})$ 为后续子问题中的实体集合。导航作用为0且上下文效用低于阈值的步骤将被过滤，最终得到3333个高质量样本，平均3.7跳。

### 过程级评估指标

为评估模型生成的推理轨迹与黄金轨迹的对齐程度，MC-SEARCH引入两个过程级指标：

**命中步数（Hit per Step, HPS）**：黄金步骤中被预测图成功恢复的比例：

$$\mathrm { H P S } ( \hat { \mathcal { G } } , \mathcal { G } ) = \frac { 1 } { | \mathcal { G } | } \Big | \{ ( t , t ^ { \prime } ) \mid r _ { t } \in \mathcal { G } , \hat { r } _ { t ^ { \prime } } \in \hat { \mathcal { G } } , \hat { r } _ { t ^ { \prime } } = r _ { t } \} \Big |$$

其中 $\mathcal{G}$ 为黄金推理图，$\hat{\mathcal{G}}$ 为预测推理图。HPS直接衡量模型在逐步检索中的证据恢复精度。

**展开偏差（Rollout Deviation, RD）**：预测与黄金推理图的步骤长度差，反映过检索或欠检索程度：

$$\mathrm { R D } ( \hat { \mathcal { G } } , \mathcal { G } ) = | | \hat { \mathcal { G } } | - | \mathcal { G } | |$$

RD越小表示模型生成的推理步数与黄金步数越接近，过大正值表明过检索，负值表明欠检索。SEARCH-ALIGN训练后，Qwen2.5-VL-7B的RD下降3.1，表明过程级监督有效抑制了冗余检索行为。



## 实验与关键发现

### 主要结果

Table 3 展示了各模型在 MC-SEARCH 基准的代理 MM-RAG 管道下的核心结果。闭源模型中，**Gemini-2.5-Pro** 在 Image-Initiated Chain 上取得最高 F1（47.61），而 **Claude-3.7-Sonnet** 在 Text-Only Chain 上表现最优。然而，所有模型在 Parallel Image-Text Fork 拓扑上均达到最低的 F1 和 HPS，揭示出跨模态并行规划是当前 MLLM 的普遍短板。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/006_Table_3.jpg]]
*Table 3: Evaluation of MLLMs on the MC-SEARCH benchmark under the agentic MM-RAG pipeline, reported across five reasoning graphs. Best backbone results are shown in bold, second-best are underlined, and improvements from SEARCH-ALIGN on open-source models are highlighted in bold red*

开源模型经过 SEARCH-ALIGN 过程级微调后，性能大幅跃升：
- **Qwen2.5-VL-7B**：Image-Initiated Chain 上 F1 从 26.30 提升至 45.70（+19.40），HPS 从 16.51 提升至 33.59（+17.08）；平均 F1 提升 13.7，HPS 提升 16.0，同时 Rollout Deviation 降低 3.1，表明推理链长度偏差显著缩小。
- **InternVL3.5-8B**：Image-Initiated Chain 上 F1 从 39.11 提升至 42.27（+3.16）；平均 F1 提升约 2.8，HPS 提升 12.0，RD 降低 0.6。

即使在最具挑战的 Parallel Image-Text Fork 上，Qwen2.5-VL-7B + SEARCH-ALIGN 也将 F1 从 22.94 提升至 32.73（+9.79），验证了过程级监督对跨模态并行推理的有效性。

### 推理链长度与过/欠检索分析

Figure 3 显示，所有模型的 F1 随推理链长度增加而持续下降，在 4–5 跳时出现急剧退化，说明长程依赖仍是核心瓶颈。Figure 4 进一步揭示了检索步数偏差的影响：适度的过检索（ΔStep = 1–2）往往能提升准确率，但过度过检索（ΔStep ≥ 4）导致 F1 急剧下降。SEARCH-ALIGN 通过将 RD 压缩至约 1.0（Table 14），有效抑制了有害的过度检索行为。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/031_Table_14.jpg]]
*Table 14: Performance of Qwen2.5-VL-7B and +SEARCH-ALIGN under Retrieval@1, @3, and @5. We report F1, ∆F1, Hit per Step (HPS), and Rollout Deviation (RD). Best values per topology and metric are highlighted in bold font*

### 模态覆盖偏差

Table 4 的步级检索模态覆盖率分析表明，图像检索覆盖率远弱于文本检索，且高度依赖显式图像输入。以 Gemini-2.5-Pro 为例，有图像输入时图像覆盖率为 87.35%，无图像输入时骤降至 29.50%；InternVL3.5-8B 在无图像输入时图像覆盖率仅为 0.66%。这揭示了模型在主动规划图像检索动作上的严重不足。

### 错误类型分布

Figure 5 的八类错误标注（由 Gemini-2.5-Pro 判断）显示，最频发的错误为：
- **检索失败**（84.7%）：未能检索到正确证据；
- **幻觉实体/属性**（75.8%）：生成不存在于证据中的实体或属性；
- **步骤遗漏**（74.3%）：跳过了必要的推理步骤。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/010_Figure_5.jpg]]
*Figure 5: Eight-way error taxonomy proportions (higher is worse), annotated by Gemini-2.5-Pro*

Figure 7 进一步表明，SEARCH-ALIGN 在四类过程级错误上均实现了比例降低，尤其在检索失败和步骤遗漏方面改善显著，印证了过程级监督直接作用于规划与检索质量的核心机制。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/027_Figure_7.jpg]]
*Figure 7: Error proportions before and after SEARCH-ALIGN across four process-level categories*

### 消融实验

Table 14 的检索深度消融显示，SEARCH-ALIGN 在 top-1 检索下已大幅提升性能，在 top-3、top-5 下亦有稳定增益，且 Rollout Deviation 始终维持在 1.0 左右的低位。这表明 SEARCH-ALIGN 带来的推理链对齐改善独立于检索深度，具有较好的鲁棒性。

### 成功与失败案例

Figure 9 展示了成功案例：代理生成的推理链与黄金推理链对齐，最终答案包含所有关键知识实体。Figure 10 展示了典型失败案例：代理成功检索了首尾跳信息，但遗漏了中间第二、三跳的证据，导致最终答案缺失关键实体。这再次印证了多跳推理中中间步骤检索失败的级联效应是主要失败模式。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_JEGDp1E4OH/figures/002_Table_1.jpg]]
*Table 1: Left: Comparison of existing multimodal retrieval-augmented QA datasets. Right: Distribution of the five reasoning topologies in MC-SEARCH, with outer rings illustrating hop diversity (2–5 hops)*



## 定位与知识库关联

### 1. 与现有基准的关系

MC-SEARCH 处于多模态检索增强生成（MM-RAG）基准的演进线上，但其定位与现有工作存在本质差异。如表1（左）所示，此前的多模态 QA 数据集（如 MMQA、WebQA、M3IT 等）普遍存在两个瓶颈：**推理链短**（通常仅1–2跳）且**仅评估最终答案正确性**，无法反映模型在逐步规划、检索和过程级推理中的真实能力。MC-SEARCH 通过引入平均3.7跳的长程推理链和逐步标注的黄金轨迹，首次将评估粒度从答案级下沉到过程级，填补了这一空白。

值得强调的是，MC-SEARCH 并非对现有数据集的简单扩展，而是通过设计五种代表性推理拓扑（Image-Initiated Chain、Text-Initiated Chain、Text-Only Chain、Multi-Images Fork、Parallel Image-Text Fork）系统刻画了多模态知识交互的多样性。其中，**Parallel Image-Text Fork** 被实验证实为所有模型的最难拓扑——所有骨干模型在该拓扑上的 F1 和 HPS 均降至最低值，揭示了跨模态并行规划这一普遍短板。

### 2. 与基线模型的关系

论文在统一的代理 MM-RAG 管道下评估了闭源与开源两类骨干模型，确保了公平比较：

- **闭源基线**：**GPT-4o-Mini**（Achiam et al., 2023）、**Gemini-2.5-Flash** 和 **Gemini-2.5-Pro**（Team et al., 2023）、**Claude-3.7-Sonnet**（Anthropic, 2024）。其中 Gemini-2.5-Pro 在 Image-Initiated Chain 上取得最高 F1（47.61），代表了当前闭源模型的上限。
- **开源基线**：**InternVL3.5-8B**（Wang et al., 2025b）和 **Qwen2.5-VL-7B**（Bai et al., 2025）。两个开源模型在原始状态下与闭源模型存在显著差距，尤其是在过程级指标 HPS 和 RD 上表现薄弱。

SEARCH-ALIGN 的核心贡献在于证明：**通过过程级监督，开源模型可以大幅缩小与闭源模型的差距**。具体而言，Qwen2.5-VL-7B 经 SEARCH-ALIGN 微调后，F1 平均提升13.7，HPS 提升16.0，RD 降低3.1；InternVL3.5-8B 亦获得约+2.8 F1 和+12.0 HPS 的增益。这表明，高质量的逐步推理链监督信号是提升代理搜索能力的关键因果杠杆，而非单纯依赖模型规模。

### 3. 方法适用边界

SEARCH-ALIGN 的有效性建立在以下前提之上：

1. **高质量逐步标注的可用性**：框架依赖 HAVE 过滤机制确保每条推理链中每跳的必要性和非冗余性。若标注质量下降（例如存在虚假跳跃或冗余步骤），过程级监督的收益将衰减。
2. **检索器能力下限**：在 top-1 检索设置下 SEARCH-ALIGN 已展现显著增益，且在 top-3、top-5 下保持稳定提升，但若底层多模态检索器完全失效，过程级对齐将失去证据基础。
3. **领域泛化未验证**：当前基准数据主要源于维基百科常识，尚未覆盖科学、数学等专业领域。在这些领域中，推理拓扑可能更为复杂，且知识库结构迥异，方法的迁移效果需要进一步验证。

### 4. 局限与开放问题

论文明确指出的局限包括：
- **领域覆盖有限**：基准局限于常识知识，未涉及专业领域。
- **模型评估范围有限**：仅在有限的开源和闭源模型上进行实验，未评估更大规模的推理模型。

由此衍生的开放问题包括：
- 如何将基准扩展至科学、数学等领域，并评估更强的推理模型？
- 如何在保持检索效率的同时，减少过检索（ΔStep ≥ 4 时性能急剧下降）和欠检索？
- 如何增强模型的跨模态并行规划能力，以攻克 Parallel Image-Text Fork 这一瓶颈拓扑？

### 5. 错误模式与改进方向

错误分析（Figure 5）揭示了三个最主要的失败模式：**检索失败**（84.7%）、**幻觉实体/属性**（75.8%）和**步骤遗漏**（74.3%）。SEARCH-ALIGN 通过过程级监督有效降低了这些错误的比例（Figure 7），但检索失败的高发生率暗示，单纯优化规划能力而不改进检索器本身，可能触及性能上限。此外，模态覆盖分析（Table 4）表明，图像检索覆盖率远弱于文本，且高度依赖显式图像输入——即使最强的 Gemini-2.5-Pro，在无图像输入时图像覆盖率仅29.50%，这指向多模态检索器能力的结构性短板。



## 原文 PDF

![[paperPDFs/ICLR_2026/MC_Search_Evaluating_and_Enhancing_Multimodal_Agentic_Search_with_Structured_Long_Reasoning_Chains.pdf]]
