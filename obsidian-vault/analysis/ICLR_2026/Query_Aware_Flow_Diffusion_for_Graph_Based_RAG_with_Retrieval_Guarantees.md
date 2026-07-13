---
title: "Query-Aware Flow Diffusion for Graph-Based RAG with Retrieval Guarantees"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Query_Aware_Flow_Diffusion_for_Graph_Based_RAG_with_Retrieval_Guarantees.pdf
project_link: https://qafd-rag.github.io/
code_link: null
aliases:
- QAFDRQR
- QAFDGBRRG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "动态查询感知边权重：在流扩散过程中，根据查询与边两端节点的语义对齐度在线调整边权重，引导流沿相关路径传播并抑制无关区域。"
primary_logic: "将流扩散重新表述为查询感知的约束优化问题，通过语义相似性动态加权边，使遍历过程既能保证理论收敛与恢复，又能高效在线执行，检索规模与子图大小相关而非全图。"
claims:
- "定理7保证在温和的信噪比条件下，高概率恢复相关子图，且流量泄漏有界。"
- "图1定性地展示了QAFD-RAG抑制无关簇并突出推理路径的能力。"
- "在UltraDomain问答、SQuALITY摘要、多跳问答和Text-to-SQL等任务上，QAFD-RAG一致地超越现有图RAG基线（表1-5）。"
- "UltraDomain (Physics) 上 Comprehensiveness = 89.51"
---

# Query-Aware Flow Diffusion for Graph-Based RAG with Retrieval Guarantees

> [!tip] 核心洞察
> 将流扩散重新表述为查询感知的约束优化问题，通过语义相似性动态加权边，使遍历过程既能保证理论收敛与恢复，又能高效在线执行，检索规模与子图大小相关而非全图。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向图检索增强生成的查询感知流扩散与检索保证 |
| 英文题名 | Query-Aware Flow Diffusion for Graph-Based RAG with Retrieval Guarantees |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=n28wnc2QTc) · [Project](https://qafd-rag.github.io/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | Query-Aware Flow Diffusion RAG (QAFD-RAG) |
| Dataset | UltraDomain (Physics), Spider 2.0 (SQLite), Spider 2.0 (Snowflake) |

> [!tip] 效果简介
> - UltraDomain (Physics) 上，Comprehensiveness 为 89.51，对比 86.33 (GraphRAG)，变化 +3.18。
> - UltraDomain (Physics) 上，Relevance 为 95.61，对比 94.46 (RAPTOR)，变化 +1.15。
> - Spider 2.0 (SQLite) 上，Execution Accuracy 为 26.70%，对比 21.50% (Spider-Agent)，变化 +5.20%。

## 概要

当前基于知识图谱的检索增强生成（Graph-based RAG）方法普遍采用查询无关的静态子图探索策略（如统一社区检测或固定跳数的自我网络），忽略了查询的整体语义，导致检索到的子图混入大量无关信息，且缺乏理论上的恢复保证。针对这一瓶颈，本文提出查询感知流扩散检索增强生成框架 **QAFD-RAG**（Query-Aware Flow Diffusion for Graph-Based RAG with Retrieval Guarantees）。其核心机制是将图遍历重新形式化为查询感知的约束优化问题：根据查询与图中节点的语义对齐度动态调整边权重（式 1），引导流扩散沿相关路径传播并抑制无关区域，从而高效提取与查询紧密关联的精简推理子图。

在方法上，QAFD‑RAG 索引阶段从文档构建知识图谱，查询阶段先抽取关键词并选定种子节点，再通过查询感知边权重与 push–relabel 算法（算法 2）在线完成流扩散，整个过程的计算复杂度仅与检索子图大小成正比，无需全图操作。理论上，本文证明了流扩散的局部性和指数收敛速率（定理 3），并给出在温和信噪比条件下相关子图高概率恢复的保证（定理 7），弥补了现有图 RAG 方法在理论上的缺失。

实验覆盖 UltraDomain 长文档问答、SQuALITY 摘要、HotpotQA/MuSiQue 多跳问答以及 Spider 2.0 Text‑to‑SQL 等多种任务。QAFD‑RAG 在绝大多数数据集和指标上一致超越 GraphRAG、LightRAG、RAPTOR、HippoRAG 等基线：在 UltraDomain 的 Comprehensiveness 上提升 +3.18，在 HotpotQA 的 F1 上提升 +5.51，在 SQL 执行精度上提升约 5–7 个百分点。消融分析表明方法对种子数量、初始质量和边权重变体具有较好鲁棒性，且在不同嵌入模型下保持稳定。定性可视化（图 1）进一步验证了 QAFD‑RAG 能够清晰地抑制无关簇并突出查询相关的推理路径。



基于知识图谱的检索增强生成（Graph-based RAG）在处理多跳推理、长文档问答等复杂任务时展现了超越扁平文本检索的潜力，其核心流程包括将文档转化为实体‑关系图，并在图中检索与查询相关的子图作为生成上下文。现有代表性方法如 GraphRAG（通过 Leiden 社区检测获取整个社区）、LightRAG（仅取 1‑跳自我网络）、HippoRAG（基于个性化 PageRank）等，均采用**查询无关的静态探索策略**，在检索时并不考虑查询的整体语义。这种设计导致检索出的子图不可避免地包含大量语义无关的节点，引入了显著噪声，并降低了生成质量。例如，针对查询 “Introduce Steve Jobs’s products in Apple”，GraphRAG 可能同时提取 “苹果水果” 和 “亚马逊河” 等不相关社区，LightRAG 虽然限制了跳数，却仍会将 “富士” 等结构相近但语义无关的节点纳入子图（图 1）。更严重的是，上述方法均**缺乏对检索子图相关性的理论保证**，无法从原理上确保检索结果对回答查询是必要且充分的。

本文的动机在于填补这一缺口：通过引入查询感知的动态图遍历机制，实现精准的推理子图提取并为之提供理论保障。具体而言，我们提出 **Query-Aware Flow Diffusion RAG (QAFD‑RAG)**，其核心思路是**将流扩散过程重新表述为查询感知的约束优化问题**——在扩散过程中，根据查询与边两端节点的语义对齐度在线调整边权重，从而引导流量优先沿语义相关的路径传播，并主动抑制流向无关区域的扩散。这一设计带来了三个直接优势：

- **动态局部性**：流扩散的复杂性与最终检索到的子图大小成正比，无需全图预处理，可在线高效执行（引理 2、推论 4）。
- **理论保证**：在温和的信噪比条件下，QAFD‑RAG 能够以高概率恢复查询相关子图，且向外部节点泄漏的流量有界（定理 7）。
- **实证有效性**：在 UltraDomain 问答、SQuALITY 长文档摘要、多跳问答和 Text‑to‑SQL 等多个任务上，QAFD‑RAG 一致超越 GraphRAG、LightRAG、RAPTOR 等基线，在涵盖面、相关性等维度上取得显著提升（表 1‑5，详细实验见第 4 节）。

综上，QAFD‑RAG 为图 RAG 提供了一种兼具理论保证与实用效率的查询感知检索范式。本文随后将详细阐述其方法、理论分析和实验验证。



## 核心方法与创新机理

现有图 RAG 方法采用查询无关的静态图探索策略（如统一社区检测、自我网络），忽视了查询的整体语义，导致检索子图混杂大量无关节点，且缺乏理论保障。**QAFD-RAG 的核心创新在于将图检索重新表述为一个查询感知的约束流扩散优化问题**，通过动态边权重和局部 Push–Relabel 算法，使流沿语义相关路径传播并抑制无关区域，首次为图 RAG 的检索过程提供收敛与恢复的理论保证。

### 关键 changed slots 与机制

1. **边权重：静态 → 查询感知动态**  
   基线使用固定的结构权重或无权重图；QAFD-RAG 引入结合节点嵌入与查询相似度的动态边权重（式 1）。该权重可视为“语义筛选器”，在流扩散过程中实时增强与查询相关的连接、弱化无关连接。实验中采用的 Hybrid 变体（式 2c）以 $a=1, b=1/4$ 的设置在多数任务上表现最优且稳定（图 3 右）。

2. **遍历方式：全局/社区 → 约束流扩散 + 局部求解**  
   不同于社区检测或自我网络扩展，QAFD-RAG 将子图检索建模为带权流成本最小化的约束优化（式 3），并通过拉格朗日对偶转化为无约束目标（式 5），由坐标下降式 Push–Relabel 算法（算法 2）在线求解。算法保持严格局部性，仅操作当前探索的节点，复杂度与最终检索子图大小（由源质量 $\alpha$ 控制）成比例，而非全图规模（引理 2，推论 4）。

3. **理论保证：无 → 收敛与恢复保证**  
   所有现有图 RAG 基线均缺乏理论分析。QAFD-RAG 提供了指数收敛速率（定理 3）和高概率恢复保证（定理 7）：在温和的信噪比条件下，算法支持集包含所有相关节点，且流量泄漏受控（式 9），从理论上确保了检索的可靠性与效率。这一保证直接对应图 1 所示的定性结果——流扩散成功抑制了 Amazon River、Amazon.com 等无关簇，并突出了 Apple 产品的推理路径。

4. **计算局部性：全图预处理 → 按需在线计算**  
   通过将流扩散控制在与查询语义高度相关的局部子图中，QAFD-RAG 无需全图预处理或全局操作，真正实现了检索规模与子图大小相关的按需计算（推论 4），同时保持对复杂多跳查询的可扩展性（扩展至多子查询分解，Prompt 5，图 5）。

5. **模块化可插拔设计**  
   作为 training‑free 框架，QAFD‑RAG 可无缝替换现有图 RAG 中的静态检索模块：例如替代 GraphRAG 的 Leiden 社区检测，或为 HippoRAG 的个性化 PageRank 添加查询感知权重。两阶段架构（索引 + 查询阶段）使其在问答、长文档摘要、多跳推理、Text‑to‑SQL 等多种下游任务中开箱即用，且对嵌入模型选择不敏感（不同嵌入下 F1 波动仅 0.78–0.82，表 7、10）。

### 实验证据强度

- **定性对比**：图 1 清晰展示了 QAFD‑RAG 相对 GraphRAG 和 LightRAG 的优势——无关簇被抑制，推理路径被突出。
- **定量提升**：在 UltraDomain 上，QAFD‑RAG 较最佳基线在 Comprehensiveness 上提升 +3.18，Relevance 提升 +1.15（表 1、5）；多跳 QA 中，HotpotQA F1 领先 +5.51，MuSiQue F1 领先 +2.96（表 3）；Text‑to‑SQL 执行精度在 SQLite 和 Snowflake 上分别提升 +5.2% 和 +7.4%（表 4）。
- **理论支撑**：定理 7 保障了相关子图的恢复精度，并定量给出流量泄漏上界，与实验观察一致。

### 局限与未来方向

当前边权重仍为手工设计的函数，对显式逻辑否定的处理能力有限；未来可通过从查询‑答案对中**学习边权重**或引入**对比嵌入**来进一步提升语义区分能力。同时，方法尚未扩展到时序图、多模态知识图谱等更复杂的数据结构。



![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/004_Figure_2.jpg]]
*Figure 2: Two-stage QAFD-RAG framework: the indexing stage builds a KG from documents, and the query stage applies QAFD to extract and prompt subgraphs for response generation*

![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/003_Figure_1.jpg]]
*Figure 1: Comparison of graph-based RAG methods on Wikipedia pages (Apple fruit, Apple Inc., Amazon River, Amazon.com)1. Query: “Introduce Steve Jobs’s products in Apple.” GraphRAG (Edge et al., 2024b) retrieves entire communities, mixing relevant nodes (e.g., Mac, macOS) with irrelevant ones (e.g., Amazon River, Apple fruit). LightRAG (Guo et al., 2024) focuses on 1-hop neighborhoods, including both relevant nodes (e.g., Steve Jobs, iPhone) and structurally close but irrelevant ones (e.g., Fuji). QAFD-RAG reweights edges by the query’s holistic meaning, suppressing irrelevant one-hop neighborhoods and preventing traversal into the Amazon River, Amazon.com, and Apple fruit clusters. The resulting sub...*

QAFD‑RAG 采用两阶段架构（图 2：索引‑查询分离），将文档集离线转化为知识图谱，再在查询时通过查询感知流扩散在线提取与问题语义相关的推理子图，最终由大语言模型生成答案。

**索引阶段**负责将非结构化文档转化为可供检索的结构化知识：
1. **文档分块**：将原始文档切分为保持上下文的文本块。
2. **实体与关系抽取**：利用LLM从每个文本块中抽取（实体，关系，实体）三元组，构建文档级知识图谱。

**查询阶段**对每条用户查询执行以下流水线：
1. **查询关键词抽取**：从查询中提取高层次与具体关键词（Prompt 2），作为后续种子选择的语义锚点。
2. **种子节点选择（算法 1）**：计算关键词嵌入与图谱节点嵌入的相似度，选取Top‑N个节点作为流扩散的“源”（初始质量注入点）。
3. **查询感知流扩散（算法 2）**：将边权重动态改写为查询与两端节点语义相似度的函数（通用形式见式 (1)），并通过求解一个约束优化问题（式 (3)–(5)）最小化总流成本并满足质量守恒。该问题采用对偶坐标下降（push–relabel 风格）求解，每次更新只涉及局部邻域，复杂度与最终检索出的子图大小成正比（引理 2、推论 4）。
4. **回答生成**：将流扩散得到的节点重要性得分最高的相关子图信息作为上下文片段，提示下游LLM生成回答（Prompt 3）。

对于需要多跳推理的复杂查询，框架支持 **多子查询分解扩展**（Prompt 5）：将原始查询分解为若干子查询，独立执行种子选择与流扩散，再将各子图合并为最终的检索上下文。

**整体输入输出流**可概括为：
- 输入：文档集 + 用户查询（可选：数据库 schema 用于 Text‑to‑SQL 场景）。
- 输出：以自然语言（或 SQL）给出的答案，附以检索到的知识子图作为可追溯的支持证据。

**关键机制**是 **动态查询感知边权重**（式 (1)，实验中使用 Hybrid 变体式 (2c)），它在保持拓扑连通性的同时，根据节点表示与查询的对齐程度引导流量沿相关路径传播并抑制无关分支，使得检索规模与问题复杂度而非全图大小成正比。该机制同时赋予方法理论上的 **指数收敛保证**（定理 3）和 **高概率子图恢复保证**（定理 7），在温和的信噪比条件下可以严格控制流量泄漏（式 (9)）。

整个框架无需训练，具备即插即用的模块化特性：既可以独立使用，也可以替代现有图 RAG 系统中的静态探索策略（如替换 GraphRAG 中的社区发现或增强 HippoRAG 中的 Personalized PageRank）。



现有图RAG方法普遍采用查询无关的静态遍历策略（如统一社区检测或固定跳数的自我网络扩展），其根本瓶颈在于**忽略查询的整体语义**，导致检索出的子图中掺杂大量无关节点，且整个过程缺乏理论保证。QAFD-RAG通过两个因果性设计打破这一局限：**动态查询感知的边权重**与**基于约束优化的流扩散**。下面依次剖析其核心模块和关键公式，突出它们如何协同实现“检索什么取决于问什么”的机理，并注明证据强度与潜在失效模式。

### 查询感知边权重：语义与结构的动态滤波

**因果机制** 传统的图检索方法以静态结构权重（如共现次数）或无权重方式遍历，无法根据查询需求抑制无关关系。QAFD-RAG在每次扩散时，依据查询与边两端节点文本嵌入的语义对齐度实时调整边权重，相当于在图上施加一个查询特定的 **“滤波器”**，使流优先沿语义相关路径传播，同时压制通往无关区域的边。

**通用公式与变体** 边权重的通用定义（式1）为

$$
\bar{w}(q,u,v) := c \cdot H_{\mathrm{sim}}\bigl(h(u),h(v)\bigr) \;\circ\; \Bigl(a + b \cdot \bigl(H_{\mathrm{sim}}(h(u),h(q)) \;\circ\; H_{\mathrm{sim}}(h(v),h(q))\bigr)\Bigr)
$$

其中 $h(\cdot)$ 为预训练语言模型产生的文本嵌入；$H_{\mathrm{sim}}$ 为相似度函数（例如余弦相似度或RBF核）；$a,b,c$ 为超参数，分别控制基准权重、查询敏感增益和全局缩放；$\circ$ 表示逐元素积或其他用户选定的组合方式。该式清晰表明，若某边的两个端点均与查询高度相似，权重将放大，引导流通过该边；反之则减小权重，阻止流扩散到不相关区域。

实验中实际采用的 **混合变体（Hybrid，式2c）** 将形式简化为

$$
\bar{w}_{\mathrm{Hybrid}}(q,u,v) := H_{\mathrm{sim}}\bigl(h(u),h(v)\bigr) \cdot \Bigl(a + b\,\bigl(H_{\mathrm{sim}}(h(u),h(q)) + H_{\mathrm{sim}}(h(v),h(q))\bigr)\Bigr)
$$

该版本将结构相似度与两端点相对于查询的**平均语义相似度**线性组合，在消融实验中略优于均值变体和乘积变体（Figure 3右）。同时，不同嵌入模型下性能波动较小（F1范围0.78–0.82，Table 7），表明权重机制对嵌入空间的选择具有一定鲁棒性。

**失效模式与局限性** 权重函数完全依赖分布式语义相似度，当查询包含显式逻辑否定、反事实条件或需要严格区分的术语时，这种软性对齐可能仍会赋予错误连接较高权重（论文将此列为显式否定处理不足的局限）。此外，超参数 $a,b,c$ 及组合函数 $\circ$ 的选择目前依赖人工经验，缺乏自动适应不同任务的学习机制。

### 种子节点选择与流初始化

为使流从查询相关的区域启动，QAFD-RAG首先用LLM从查询中抽取高层与具体关键词（Prompt 2），再计算每个关键词与图谱节点嵌入的相似度，选择语义最匹配的 **Top‑N** 个节点作为种子（Algorithm 1）。每个种子被赋予初始质量 $\alpha$，构成流扩散的源项 $\Delta$。消融实验表明，种子数量从20开始性能趋于稳定（Figure 3左），说明适度数量的高质量种子已能覆盖查询意图；然而种子质量高度依赖LLM的关键词抽取准确度——若遗漏关键实体或抽取歪曲，后续扩散将因源点失配而难以恢复完整相关子图。

### 查询感知流扩散的约束优化形式

**从启发式到优化** 传统图遍历（如PageRank、社区扩展）依赖于启发式传播规则，缺少显式的查询相关性目标和收敛性保证。QAFD-RAG将子图检索重新表述为**有约束的凸优化问题**，其最优解给出的节点重要性既满足流质量守恒，又最小化总扩散代价，从而从原理上保证了检索的局部化与收敛性。

**原始问题（式3）**

$$
\min_{\mathbf{f}\in\mathbb{R}^{|\mathcal{E}|}} \;\frac12\, \mathbf{f}^{\top} \bar{\mathbf{W}}(q) \mathbf{f} \qquad \mathrm{s.t.} \quad \Delta + \mathbf{B} \bar{\mathbf{W}}(q) \mathbf{f} \leq \mathbf{T}
$$

其中 $\mathbf{f}$ 为各边上的非负流向量，$\bar{\mathbf{W}}(q)$ 为以查询感知权重为对角元的边权重矩阵，$\mathbf{B}$ 为节点‑边关联矩阵。约束保证每个节点的净流出量不超过汇容量 $\mathbf{T}$ （可视为预设的流出上限），源项 $\Delta$ 在种子节点注入质量。目标函数鼓励流尽可能均匀分布（二次代价最小化），同时通过 $\bar{\mathbf{W}}(q)$ 的倒数关系增大无关边的代价，迫使流绕开它们。

**对偶形式与算法实现** 为了使大规模图上可执行，QAFD-RAG通过拉格朗日对偶将问题转化为对节点变量 $\mathbf{x}$ 的无约束优化（式5）：

$$
F(\mathbf{x};q) := \frac12\, \mathbf{x}^{\top} \mathbf{L}(q) \mathbf{x} + \mathbf{x}^{\top} (\mathbf{T} - \Delta), \qquad \mathbf{x} \in \mathbb{R}^{|\mathcal{V}|}_+
$$

其中 $\mathbf{L}(q) = \mathbf{I} - \bar{\mathbf{W}}(q)$ 是**查询感知拉普拉斯矩阵**，$\mathbf{x}$ 的每个分量 $x_u$ 可解释为节点 $u$ 的重要性得分（即对偶变量），非零分量的支持集 $\mathrm{supp}(\mathbf{x})$ 即为检索到的子图。算法2采用 **坐标下降** 直接优化 $F(\mathbf{x};q)$：每一步仅更新当前支持集内的节点，无需操作全图，实现了**按需计算**和**局部图遍历**（Lemma 2），有效避免了对全局预处理或全图扩散的依赖。该局部性质确保计算开销与初始种子总质量 $\lVert\Delta\rVert_1$ 及最终子图大小成正比（推论4），而非全图规模。

**理论收敛与恢复保证** 定理3证明对偶坐标下降以指数速度收敛，迭代次数为 $O(\bar{d}\,\lVert\Delta\rVert_1 \log(1/\epsilon))$，其中 $\bar{d}$ 是平均度，$\epsilon$ 为精度要求。更重要的是，在温和的信噪比条件下（控制嵌入噪声方差与语义类别间的最小间隔），定理7进一步给出了**高概率的恢复保证**：设 $\mathcal{R}_k$ 为第 $k$ 个子查询的真正相关节点集，$\mathbf{x}^{(k)}$ 为优化解，则有

$$
\mathcal{R}_k \subseteq \operatorname{supp}(\mathbf{x}^{(k)}), \quad \text{且} \quad \sum_{u\in\operatorname{supp}(\mathbf{x}^{(k)})\setminus\mathcal{R}_k} T_u \leq \beta \sum_{u\in\mathcal{R}_k} T_u
$$

即检索到的支持集**完全包含相关节点**，且流泄漏到无关节点上的总量被一个因子 $\beta$ 所控制。这为“查询感知权重引导流精确覆盖相关子图”提供了严格的理论支撑，也是所有现有启发式图RAG方法所缺乏的根本优势。

### 多子查询分解与整合

面对需要多跳推理或涵盖多个方面的复杂查询，QAFD-RAG调用LLM将原始查询分解为若干原子子查询 $q_k$（Prompt 5），对每个子查询独立执行上述“种子选择 → 流扩散”流程，得到各自的重要性向量 $\mathbf{x}^{(k)}$，最后取支持集的并集作为最终检索子图，输入到答案生成模块。由于每个子查询的权重函数与优化问题形式均保持不变，且算法2天然支持按需局部计算，该扩展无需引入全图操作或其他近似，理论保证（如Theorem 7）仍对每个子查询独立成立。该环节的主要失效风险在于LLM的分解质量——错误或遗漏的子查询将直接导致检索覆盖度下降。



## 实验与关键发现

本文在涵盖开放域问答、长文档摘要、多跳推理、Text-to-SQL 的多个标准评测集合上对 QAFD‑RAG 进行验证，并与 GraphRAG、LightRAG、RAPTOR、HippoRAG 等图检索增强生成基线以及 CHASE‑SQL、DIN‑SQL、DAIL‑SQL、CodeS、Spider‑Agent 等 Text‑to‑SQL 基线比较。所有评测均使用 GPT‑4o 在多维度上重复 5 次，报告均值和标准差以降低评判偏差；基线方法使用原论文设置和公开代码复现，仅作必要的最小适配。本节依次给出主结果、消融分析，并在末尾梳理当前方法的失败模式与限制。

### 主结果

**UltraDomain 问答。** 表 1 与表 5 汇总了 QAFD‑RAG 与四种基线在 UltraDomain 五个维度（Comprehensiveness, Diversity, Logicality, Relevance, Coherence）上的对比。QAFD‑RAG 在大多数数据集‑指标组合上取得最优平均分数，且优势在 Comprehensiveness 与 Logicality 维度尤为稳定。以 Physics 子集为例，Comprehensiveness 达 89.51，较 GraphRAG 的 86.33 提高 +3.18；Relevance 为 95.61，较 RAPTOR 的 94.46 提高 +1.15。其他子集（Agriculture, Computer Science, Geography, Music 等）的详细数值见原文附录 A2.1.1。

![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/005_Table_1.jpg]]
*Table 1: Comparison of QAFD-RAG and baselines on UltraDomain across five GPT-4o–scored dimensions (0–100). Rows are grouped by dataset and columns by metric; values are mean (± std) over 5 evaluations. Best per dataset/metric is bolded. Continued in Appendix A2.1.1*

**SQuALITY 长文档摘要。** 表 2 的结果表明 QAFD‑RAG 在参照摘要的自动化指标上整体领先。BLEU‑1 达到 35.44，BLEU‑2 为 18.63，METEOR 为 25.59，ROUGE‑2 F1 为 4.79，多项指标优于包括 GraphRAG 与 HippoRAG 在内的对比方法。该趋势说明查询感知流扩散能够有效抑制长文档知识图谱中的无关社区，从而为生成模型提供更高保真度的上下文。

**多跳问答。** 在 HotpotQA、2WikiMultihopQA、MuSiQue 三个多跳数据集上（表 3），QAFD‑RAG 均表现出强竞争力。HotpotQA 上取得最高 F1 73.42（EM 58.10），较 RAPTOR 的 67.91 F1 提升 +5.51；MuSiQue 上 F1 为 47.99（EM 33.50），较 HippoRAG 的 45.03 F1 提升 +2.96。2WikiMultihopQA 上得分 69.41 F1/59.50 EM，略低于当前最优，但仍处于同一梯队。

![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/007_Table_3.jpg]]
*Table 3: Performance on Multi-Hop QA (F1, EM)*

**Text‑to‑SQL。** 将 QAFD‑RAG 集成到 SQL‑Agent 的检索路径后，在 Spider 2.0 的 SQLite 和 Snowflake 测试集上执行准确率分别达到 26.70% 和 23.70%（表 4），显著超过原版 Spider‑Agent 的 21.50% 和 16.30%，且远高于以固定 schema 链接为主的 DAIL‑SQL 等基线。进一步的 schema 链接分析（表 9）显示 QAFD‑RAG 在 Snowflake 上 F1 达到 0.60（对比 Spider‑Agent 的 0.35），说明查询感知流扩散能够更精准地识别与自然语言问题相关的表和列。

![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/008_Table_4.jpg]]
*Table 4: SQL execution accuracy on 135 SQLite and Snowflake test sets*

### 消融与分析

**超参数敏感性。** 图 3（左）考察种子节点数量的影响：当种子数由 5 增至 20 时性能提升明显，继续增加收益趋于饱和，表明 20 个种子已经能够充分覆盖查询相关的语义起点。图 3（中）针对源质量参数 α 的扫描表明，α=10 时各维度得分平衡且稳定，过度增大 α 会引入更多无关子图，导致 Relevance 轻微下降。图 3（右）对比三种边权重变体——Mean、Product 与 Hybrid（式 (2c)）——Hybrid 变体在多数指标上略优于 Mean 和 Product，说明同时通过加法和乘法组合结构相似度与查询‑节点相似度，有利于在语义和拓扑之间取得更稳健的权衡。

![[assets/figures/papers/iclr26_0016_n28wnc2QTc_Query-Aware_Flow_Diffusion_for_Graph-Based_RAG_w/figures/010_Figure_3.jpg]]
*Figure 3: Sensitivity of QAFD-RAG to the number of seed nodes (left), initial mass α (middle), and edge weight choice (right), evaluated across five dimensions on the Mix dataset*

**嵌入模型鲁棒性。** 为验证方法不依赖于特定预训练嵌入，在 Mix 问答集上更换五种不同嵌入模型（包括 text‑embedding‑3‑large、NVIDIA‑nv‑embed‑v2 等）测试 QAFD‑RAG，结果如表 7 所示：不同嵌入下的 Comprehensiveness 均值集中在 86.8–88.1，Coherence 等维度波动亦很小，整体 F1 变化幅度控制约 0.78–0.82。Text‑to‑SQL 局部类别上的对应分析（表 10）呈现类似趋势，F1 跨模型的差异不超过 0.04，进一步支持方法的嵌入无关性与工程实用性。

**效率与局部性。** 综合运行时间统计（表 6）显示，QAFD‑RAG 的总检索时延与子图大小成正比，而非与全图规模成正比，这与引理 2 和推论 4 给出的局部性保证一致——流扩散仅会在与查询语义相关的连通分量内推进。在 Mix 数据集全图上，QAFD‑RAG 的索引后检索耗时与基于 1‑hop 的 LightRAG 相当，但显著低于需要全图社区检测的 GraphRAG，而检索质量则大幅领先。

### 失败模式与限制

尽管 QAFD‑RAG 在多个任务上取得一致优势，分析结果也揭示了若干边界与失败模式：

1. **显式逻辑否定处理困难。** 流扩散依赖连续嵌入相似度加权，难以准确表达“不包含 X”“排除 Y”等严格逻辑条件，可能导致在需要高精度符号区分的法律、医疗等场景中出现检索泄漏。
2. **边权重超参数依赖经验设定。** 当前采用的 Hybrid 变体中，系数 a、b、c 以及函数形式依靠实验调参（a=1，b=1/4），尚不能根据数据或查询自适应学习，在面对极端分布偏移时可能失效。
3. **未覆盖时序与多模态图谱。** 方法当前仅适用于静态同构图，缺少对时间戳、多模态节点属性的原生支持，限制了在事件演变、视觉问答等场景的应用。
4. **子查询分解质量影响最终效果。** 在多子查询扩展中，依赖 LLM 进行查询分解（Prompt 5），若分解不完整或产生冗余/矛盾子查询，会导致合并子图引入噪声或遗漏关键证据。
5. **Text‑to‑SQL 绝对精度仍有限。** 即使在增强 schema 链接后，SQL 执行准确率仅为约 24%，离产业可部署水平尚有差距，且错误主要源于复杂嵌套查询和稀有操作语义的建模不足。

上述限制也指明了未来的改进方向，包括从查询‑答案对中学习边权重、引入对比或符号‑神经混合机制以处理逻辑区分，以及将流扩散框架拓展到时序与多模态知识图谱。

### 关键图表结论

- **图 1** 定性展示了 QAFD‑RAG 通过查询感知边权重抑制“Amazon River”“Apple fruit”等无关簇，同时高亮“Mac”“macOS”“iPhone”等推理路径的能力，直观解释了性能增益的来源。
- **表 1–表 5** 构成主结果矩阵，覆盖问答、摘要、多跳推理、Text‑to‑SQL 四类任务，QAFD‑RAG 在大多数指标上取得最优或次优，且在需要语义‑结构联合检索的场景中优势明显。
- **图 3** 与 **表 7/表 10** 验证了方法的超参数鲁棒性和嵌入模型非敏感性，表明技术方案在工程部署层面具备良好的稳定性。

以上实验分析共同表明，查询感知流扩散以动态边权重在线重路由流，既能从理论上收敛至相关子图（定理 7），又在实践中显著减轻了无关社区泄漏，为图式检索增强生成提供了高效、可扩展且具备保障的新范式。



## 定位与知识库关联

QAFD-RAG 在图 RAG 谱系中引入了一种**查询感知的流扩散范式**，区别于此前静态图探索方法：GraphRAG 依赖查询无关的 Leiden 社区检测，LightRAG 使用固定 1 跳自我网络，RAPTOR 构建树状层次结构，HippoRAG 采用个性化 PageRank。这些基线均采用**静态边权重**和**预先确定的遍历策略**，检索不依赖查询的全局语义，导致无关节点随子图一同被取回。QAFD-RAG 通过四个关键机制的改变解决了这一瓶颈：

1. **边权重动态化**：从无权或结构权重替换为查询感知的混合权重（式 1/2c），使边传导强度由节点嵌入与查询的相似度在线决定，从而抑制语义漂移的簇。
2. **遍历方法转向约束流扩散**：替代社区检测和自我网络，算法 2 在查询感知加权图上求解约束优化问题（式 3），将遍历表述为质量守恒下的最小流成本，实现局部、按需的图扩展。
3. **理论保证的引入**：基线方法缺乏形式保证，而 QAFD-RAG 提供双收敛保证——对流扩散的对偶坐标下降具有指数收敛（定理 3），在温和信噪比条件下高概率恢复相关子图且流量泄漏有界（定理 7）。
4. **计算开销与子图大小成比例**：Lemma 2 和 Corollary 4 证明算法仅访问子图支撑集内的节点和边，复杂度与检索子图规模（由种子质量 Δ 控制）成正比，而非全图规模。

该框架的性质使其能够作为**即插即用的检索模块**嵌入下游系统。在 UltraDomain 问答、SQuALITY 长文档摘要、多跳问答和 Text‑to‑SQL（Spider 2.0）任务中，QAFD-RAG 一致超越上述图 RAG 基线（表 1‑5），例如 HotpotQA F1 达 73.42（+5.51 vs. RAPTOR），SQL 执行准确率在 Snowflake 上达 23.70%（+7.40 vs. Spider‑Agent）。

**适用边界**：QAFD-RAG 面向关系丰富的文本知识图谱场景，尤其擅长需要多跳推理或复杂模式链接的任务（如 Text‑to‑SQL 的跨表关系）。其检索是训练无关的，仅依赖预训练嵌入和轻量 LLM 调用（关键词提取、子查询分解）。当查询可被分解为语义明确的子查询时（Prompt 5），框架表现稳健；种子节点数量（约 20）和超参数 α（默认 10）在敏感度实验中表现平稳（Figure 3）。但该方法本质上是**连续嵌入驱动的扩散**，因此难以处理对显式逻辑否定或严格集合操作的推理；它尚未扩展到时序、多模态或异构知识图谱。

**局限**：① 基于嵌入的边权重无法建模显式逻辑否定，可能影响需要严格区分的问答；② 边权重的超参数 (a, b, c) 和变体仍需手工选定，缺乏从数据中自适应学习的机制；③ 当前实现未覆盖时序图或多模态图谱；④ 查询分解质量依赖 LLM，错误的分解会损害最终检索结果；⑤ 在 Text‑to‑SQL 上的绝对准确率（~24%）仍低，离产业落地有一定距离。

**开放问题**：能否从查询‑答案对中端到端学习边权重，替代手工设计的加权函数？如何将流扩散扩展到含有时间戳、多模态信息或异构类型的知识图谱？引入对比嵌入或符号‑神经混合机制，能否提升对逻辑否定的处理能力？能否在更复杂的多跳场景下给出更紧的恢复保证并进一步降低在线复杂度？流扩散中的种子选择策略能否与图学习或预训练语言模型更紧密耦合？这些问题指向了查询感知图检索未来研究的若干方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/Query_Aware_Flow_Diffusion_for_Graph_Based_RAG_with_Retrieval_Guarantees.pdf]]
