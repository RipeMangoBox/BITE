---
title: ": One LLM Token for Explicit Graph Structural Understanding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One_LLM_Token_for_Explicit_Graph_Structural_Understanding.pdf
project_link: null
code_link: https://github.com/Jingyao-Wu/SOG
aliases:
- SSGT
- OLTEGSU
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "引入一个特殊的离散结构标记<SOGk>，通过拓扑感知的标记化器将图拓扑映射为单个离散标记，并与文本标记共享同一嵌入空间。"
primary_logic: "通过自监督拓扑重建将连续图表示离散化为一个高度选择性的结构标记，再通过混合结构QA语料库进行标记对齐，使得单个标记即可准确、简洁地传递完整图拓扑信息，从而消除结构幻觉。"
claims:
- "在五个图级基准数据集上，<SOGk>方法相比基线实现了9.9%–41.4%的性能提升。"
- "结构标记具有高度选择性：只有正确的标记才能忠实传递拓扑信息并带来一致的性能提升。"
- "结构标记嵌入在文本标记的邻域内，有效桥接了图空间和语言空间。"
- "BBBP 上 AUC-ROC = 76.9±3.1 (LLaMA3-3B)"
---

# : One LLM Token for Explicit Graph Structural Understanding

> [!tip] 核心洞察
> 通过自监督拓扑重建将连续图表示离散化为一个高度选择性的结构标记，再通过混合结构QA语料库进行标记对齐，使得单个标记即可准确、简洁地传递完整图拓扑信息，从而消除结构幻觉。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | <SOGk>：一个用于显式图结构理解的LLM标记 |
| 英文题名 | : One LLM Token for Explicit Graph Structural Understanding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eXidGkRUFt) · [GitHub](https://github.com/Jingyao-Wu/SOG) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | <SOGk> (Structure Of Graph token) |
| Dataset | BBBP, Tox21, ClinTox, HIV |

> [!tip] 效果简介
> - BBBP 上，AUC-ROC 为 76.9±3.1 (LLaMA3-3B)，对比 最佳基线 (LLaMA3-3B) 约 67.0 (估计)，变化 +9.9% (相对提升)。
> - Tox21 上，AUC-ROC 为 83.4±3.3 (LLaMA3-3B)，对比 最佳基线 (LLaMA3-3B) 约 73.5 (估计)，变化 +9.9% (相对提升)。
> - ClinTox 上，AUC-ROC 为 94.3±0.1 (LLaMA2-7B)，对比 最佳基线 (LLaMA2-7B) 约 82.9 (估计)，变化 +11.4% (相对提升)。

## 概要

该论文针对大型语言模型（LLM）在图结构理解中的核心瓶颈——现有方法要么将图拓扑展开为冗长的文本序列（Graph-to-Text），导致token消耗过大且注意力分散；要么将图结构压缩为连续嵌入（Graph-to-Embedding），引发严重的模态不对齐问题——提出了一个简洁而有效的解决方案：引入一个特殊的离散结构标记 `<SOGk>`（Structure Of Graph token）。

方法的核心创新在于三个紧密耦合的组件：首先，一个拓扑感知的图结构标记化器（Topology-Aware Graph Structural Tokenizer）通过锚节点层次遍历、虚拟全局节点池化、GNN编码以及自监督向量量化（VQ）离散化，将任意图拓扑映射为单个高度选择性的离散token。其次，构建混合结构问答语料库（Hybrid Structure QA Corpora），通过三类任务（k-NN匹配、相似性判断、描述-标记配对）对结构标记与文本标记进行嵌入空间对齐，仅更新新标记嵌入并使用LoRA微调。最后，在下游任务微调阶段，将 `<SOGk>` 与任务提示、文本属性一同输入LLM进行推理。

主要结果方面，在MoleculeNet的五个图级分类基准（BBBP、Tox21、ClinTox、HIV、BACE）上，该方法相比现有最佳基线实现了9.9%–41.4%的性能提升，且仅需3B或7B参数的LLM即可超越更大规模模型的性能。消融实验验证了结构标记的高度选择性——只有正确的标记才能忠实传递拓扑信息；t-SNE可视化显示结构标记嵌入位于文本标记的邻域内，有效桥接了图空间与语言空间。该方法为LLM显式理解图拓扑提供了一条兼具准确性与简洁性的新路径。



将图结构信息注入大语言模型（LLM）是图机器学习与自然语言处理交叉领域的关键问题。现有方法在处理图拓扑时面临一个根本性的两难困境，这构成了当前工作的核心动机。

**现有方法的两难困境与结构幻觉**：当前主流范式可分为两类。Graph-to-Text方法将图结构（如分子键连关系或社交网络连接）序列化为文本描述（例如Talk Like a Graph、InstructGraph、GraphText等）。这类方法虽然保留了完整的拓扑细节，但会消耗大量token，导致LLM的注意力在冗长的结构描述中分散，从而产生“结构幻觉”——即模型在推理时错误地理解或丢失了图拓扑信息。Graph-to-Embedding方法（如GraphGPT、LLaGA、G-retriever等）则试图通过GNN编码器将图结构压缩为连续向量，再通过MLP投影到LLM的嵌入空间。然而，这种连续表示与LLM原本的离散文本标记空间存在严重的模态不对齐，使得模型难以精确捕捉拓扑语义。简言之，前者“信息过载但注意力稀释”，后者“信息压缩但语义错位”，两者都未能可靠地解决图结构的忠实表达问题。

**核心因果机制**：本文的洞察在于，图拓扑信息可以被高度压缩为一个离散的、具有语义选择性的标记，关键在于设计一个拓扑感知的离散化过程。具体地，作者引入一个特殊的离散结构标记 `<SOG_k>`（Structure Of Graph token），通过一个拓扑感知的标记化器（topology-aware graph structural tokenizer）将完整图拓扑映射为单个离散标记。该标记化器首先基于锚节点（如度中心性最高的节点）对图进行层级结构遍历，为每个节点赋予结构属性；随后引入虚拟全局节点连接所有节点作为池化机制，获得全局表示；最后通过向量量化（VQ）进行自监督离散化，将连续图表示映射到大小为K的码本中，得到唯一的离散索引k作为结构标记。该标记与文本标记共享同一嵌入空间，从而从根本上避免了模态不对齐问题。

**对齐策略与证据强度**：为了弥合结构标记与文本标记之间的语义鸿沟，作者构建了三类混合结构QA语料库（k-NN匹配、相似性判断、描述-标记配对），通过监督微调（仅更新新标记嵌入，使用LoRA）实现对齐。关键证据表明，结构标记具有高度选择性：只有正确的标记才能忠实传递拓扑信息并带来一致的性能提升（消融实验验证了随机或错误标记会导致性能显著下降）。t-SNE可视化进一步显示，结构标记嵌入位于文本标记嵌入的邻域内，有效桥接了图空间和语言空间（Figure 6）。

**性能提升与缺口填补**：在MoleculeNet的五个图级基准数据集（BBBP、Tox21、ClinTox、HIV、BACE）上，`<SOG_k>`方法相比所有基线实现了9.9%–41.4%的性能提升（Table 1），且仅需3B或7B参数的LLM即可超越更大模型（如GPT-4、Deepseek-R1）的基线表现。这一结果验证了单个离散结构标记足以高效且准确地传递完整图拓扑信息，从而填补了现有方法在“信息保真度”与“模态对齐”之间的缺口。



## 核心方法与创新机理

<SOGk> 的核心创新在于将图拓扑信息压缩为一个**离散的、与文本共享嵌入空间的结构标记**，从根本上改变了LLM接收图结构的方式。现有方法面临一个根本性瓶颈：Graph-to-Text 方法将图结构展开为冗长的文本序列（如邻接表），消耗大量token并导致注意力分散；Graph-to-Embedding 方法虽然压缩了信息，但连续嵌入与文本嵌入空间存在严重的模态不对齐。两者都导致LLM产生“结构幻觉”——无法准确理解图拓扑。

### 因果机制：从连续压缩到离散选择

<SOGk> 的设计围绕一个关键洞察：**结构信息不需要完整传递，只需要高度选择性传递**。其因果链如下：

1. **拓扑感知标记化器**将每个图映射为一个离散码本索引。具体流程为：基于度中心性选择锚节点 → 对图进行层次遍历，为每个节点分配结构属性 → 引入虚拟全局节点作为池化机制 → 用两层GCN编码 → 通过向量量化（VQ）将连续图表示离散化为码本中的最近邻条目。码本检索公式为 $k = \arg\min_j \|h_s^i - c_j\|_2$，其中 $c_j \in \mathcal{C} = \{c_1, c_2, \ldots, c_K\}$。训练损失由重建损失、更新损失和承诺损失三部分组成（见公式 $\mathcal{L} = \|A - \hat{A}\|_F^2 + \|\mathbf{sg}[H_s] - \mathbf{z}_e(H_s)\|_2^2 + \beta \|H_s - \mathbf{sg}[\mathbf{z}_e(H_s)]\|_2^2$）。

2. **混合结构QA语料库**将结构标记与文本标记对齐。该语料库包含三种类型：k-NN匹配（结构相似的图应选择相近的标记）、相似性判断（判断两个图是否共享相同骨架）、描述-标记配对（将结构标记与自然语言描述关联）。其中描述-标记配对贡献最大（Figure 3）。

3. **任务特定微调**仅更新新标记嵌入（使用LoRA），LLM的其他参数冻结。推理时输入为 $\{P, T, <SOG_k>\}$，输出为预测标签（公式 $\mathcal{O} = \mathcal{M}(\{P, T, <SOG_k>\} | G; \mathcal{V}', \Theta)$）。

### 关键改变：三个核心槽位的重构

相比基线方法，<SOGk> 在三个关键槽位上做了根本性改变：

| 槽位 | 基线值 | 提出值 | 证据 |
|------|--------|--------|------|
| **图拓扑输入表示** | 文本序列（Graph-to-Text）或连续嵌入（Graph-to-Embedding） | **单个离散结构标记 <SOGk>** | 论文摘要明确说明“incorporate one special token <SOGk> to fully represent the Structure Of Graph within a unified token space” |
| **标记空间对齐方式** | MLP投影（Graph-to-Embedding）或无显式对齐（Graph-to-Text） | **混合结构QA语料库监督微调**，仅更新新标记嵌入 | 论文方法部分明确“construct a set of hybrid structure Question-Answering corpora to align new structural tokens with existing text tokens” |
| **图结构编码方式** | GNN编码后直接投影或文本化 | **拓扑感知标记化器**：层次遍历+虚拟全局节点+GNN编码+自监督离散化（VQ） | 论文方法部分描述“topology-aware graph structural tokenizer, which extracts the graph topology, encodes global information, and further projects into one structural token” |

### 证据强度与验证

核心创新的有效性通过三个层次的证据支撑：

1. **性能提升**：在MoleculeNet五个数据集上，<SOGk> 相比所有基线实现了 **9.9%–41.4%** 的相对性能提升（Table 1）。例如，在BACE数据集上，LLaMA2-7B的AUC-ROC从约57.0提升至98.4（+41.4%）。这一提升在3B和7B两种规模的LLM上均一致出现。

2. **选择性验证**：消融实验（Table 2, Figure 2）证明，只有正确的结构标记才能带来性能提升。使用随机标记或错误标记会导致性能显著下降。论文明确断言“only the correct token generated by our topology-aware graph structural tokenizer is able to faithfully convey the correct topology information”。

3. **空间对齐验证**：t-SNE可视化（Figure 6）显示，结构标记嵌入位于文本标记嵌入的邻域内，而Graph-to-Embedding方法的软提示嵌入则明显偏离。这表明<SOGk>有效桥接了图空间和语言空间。

### 设计选择与失败模式

- **词汇表大小K**：K=256时取得最佳平均性能（Table 4），K过小导致区分度不足，K过大增加学习难度。
- **锚节点选择**：度中心性优于随机选择（Table 5），但当前仅在分子图上验证，在更复杂图结构上的泛化性需手动验证。
- **混合QA语料库**：三种类型均贡献性能，但描述-标记配对贡献最大（Figure 3），暗示显式的语义关联比隐式结构匹配更重要。
- **局限性**：当前方法仅在分子图上评估，在社交网络、知识图谱等更广泛图类型上的泛化能力尚未验证。节点级任务通过2跳ego-graph实现，大规模图可能面临扩展性问题。



![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/001_Figure_1.jpg]]
*Figure 1: The overall architecture for LLM understanding with structural token { \< S O G _ { k } > }*

<SOGk>（Structure Of Graph token）的核心设计将图结构理解问题拆解为两个解耦的阶段：**结构离散化**与**标记对齐**，整体流程如Figure 1所示。

**第一阶段：拓扑感知图结构标记化器（Topology-Aware Graph Structural Tokenizer）**  
该模块负责将任意图拓扑压缩为单个离散标记 `<SOG_k>`。其内部流程为：
1. **层次遍历与属性分配**：基于锚节点（按度中心性选取）对全图进行层次遍历，为每个节点赋予一个结构属性字符串（如 `"anchor-1-layer-2"`）。
2. **初始特征编码**：使用SentenceTransformers（all-MiniLM-L6-v2）将结构属性编码为连续向量，作为GNN的初始节点特征。
3. **全局信息注入**：引入虚拟全局节点连接所有节点，作为池化机制获取图级表示。
4. **向量量化（VQ）离散化**：将GNN编码后的节点特征通过码本检索（公式：$k = \arg\min_j \|h_s^i - c_j\|_2$）映射到大小为K的离散码本空间，最终聚合为单个结构标记。
5. **自监督训练**：通过重建邻接矩阵A与码本更新（总损失函数包含重建损失、更新损失和承诺损失）优化标记化器，无需下游任务标签。

**第二阶段：混合结构QA语料库与标记对齐**  
为弥合结构标记与文本标记的模态鸿沟，论文构建了三类混合结构问答语料：
- **k-NN匹配**：判断两个结构标记是否对应拓扑相似的图；
- **相似性判断**：比较两图的拓扑相似程度；
- **描述-标记配对**：将结构标记与自然语言描述（如“该分子具有苯环骨架”）对齐。

在LLM微调阶段，仅更新新引入的结构标记嵌入，LLM主干参数通过LoRA冻结更新。最终推理公式为：

$$
\mathcal{O} = \mathcal{M}(\{P, T, <SOG_k>\} | G; \mathcal{V}', \Theta)
$$

即LLM根据任务提示P、文本属性T和结构标记`<SOG_k>`生成预测输出O。

**输入输出流**：输入为图G（节点属性+邻接矩阵），输出为结构标记`<SOG_k>`与原始文本标记拼接后的序列。这一设计使得图拓扑信息以单个token的形式直接注入LLM的离散标记空间，避免了Graph-to-Text方法的长序列注意力分散问题，也消除了Graph-to-Embedding方法的模态不对齐瓶颈。

**关键设计约束**：结构标记具有高度选择性——消融实验（Table 2）证实，只有正确的标记才能忠实传递拓扑信息并带来一致的性能提升（9.9%–41.4%），随机或错误的标记会导致性能显著下降。t-SNE可视化（Figure 6）进一步显示，结构标记嵌入落在文本标记的邻域内，有效桥接了图空间与语言空间。



<SOGk>方法的核心在于通过一个离散的结构标记桥接图拓扑与LLM文本空间。其整体推理过程可形式化为：

$$\mathcal{O} = \mathcal{M}(\{P, T, <SOG_k>\} | G; \mathcal{V}', \Theta)$$

其中LLM $\mathcal{M}$ 根据任务提示 $P$、文本属性 $T$ 和结构标记 $<SOG_k>$ 生成输出 $\mathcal{O}$（包含预测标签）。$\mathcal{V}'$ 是扩展后的词汇表（包含新标记），$\Theta$ 为冻结的模型参数。

该方法由三个核心模块组成：

**1. 拓扑感知图结构标记化器**

该模块将图拓扑压缩为单个离散标记。其工作流程包括：

- **层次遍历**：基于锚节点（按度中心性选择）对每个节点 $v^i \in V$ 分配新的结构属性 $t_s^i$，编码节点在拓扑中的相对位置。
- **虚拟全局节点**：引入一个连接所有节点的虚拟节点，作为池化机制获取图的整体表示。
- **GNN编码**：使用两层GCN作为编码器，将节点特征 $h_s^i$ 映射到隐空间。
- **向量量化（VQ）**：通过码本检索将连续表示离散化：

$$k = \arg\min_j \|h_s^i - c_j\|_2, \quad c_j \in \mathcal{C} = \{c_1, c_2, \ldots, c_K\}$$

其中 $\mathcal{C}$ 为大小为 $K=256$ 的结构词汇表，$c_j$ 为可学习的码本向量。

该模块通过自监督拓扑重建训练，总损失函数为：

$$\mathcal{L} = \underbrace{\|A - \hat{A}\|_F^2}_{\mathrm{Reconstruction\ loss}} + \underbrace{\|\mathbf{sg}[H_s] - \mathbf{z}_e(H_s)\|_2^2}_{\mathrm{Update\ loss}} + \beta \underbrace{\|H_s - \mathbf{sg}[\mathbf{z}_e(H_s)]\|_2^2}_{\mathrm{Commitment\ loss}}$$

其中 $A$ 为邻接矩阵，$\hat{A}$ 为重建矩阵，$\mathbf{sg}[\cdot]$ 为停止梯度算子，$\mathbf{z}_e(\cdot)$ 为编码器输出，$\beta$ 为承诺损失权重。重建损失确保拓扑信息被保留，更新损失和承诺损失则稳定VQ训练过程。

**2. 混合结构QA语料库**

为对齐结构标记与文本标记的嵌入空间，构建三类问答数据：
- **k-NN匹配**：判断两个图的结构标记是否在码本空间中邻近。
- **相似性判断**：比较两个图的拓扑相似性。
- **描述-标记配对**：将结构标记与自然语言描述（如“包含苯环的分子”）关联。

其中描述-标记配对贡献最大（Figure 3）。该阶段仅更新新标记的嵌入，使用LoRA保持LLM参数冻结。

**3. 任务特定微调**

将$<SOG_k>$应用于下游分类任务，损失函数为：

$$\mathcal{L} = -\sum_t \log p_\Theta(y_t \mid y_{<t}, P, T, <SOG_k>)$$

即给定提示、属性和结构标记下真实标签序列的负对数似然。该阶段同样使用LoRA微调。

**关键设计选择**：结构词汇表大小 $K=256$ 在平均性能上最优（Table 4）；锚节点按度中心性选择优于随机选择（Table 5）。



## 实验与关键发现

### 主实验结果 (RQ1)

在MoleculeNet的五个图级基准数据集（BBBP、Tox21、ClinTox、HIV、BACE）上，<SOGk>方法在LLaMA2-7B和LLaMA3-3B两个骨干模型上均取得了最佳或次优性能。与所有基线方法（包括Graph-to-Text和Graph-to-Embedding两大类）相比，<SOGk>实现了9.9%–41.4%的相对性能提升（Table 1）。具体而言：

![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/002_Table_1.jpg]]
*Table 1: Performance comparison across five datasets, where bold indicates the best performance and underlined indicates the second-best*

- **BBBP**：LLaMA3-3B下AUC-ROC达76.9±3.1，相对最佳基线提升约9.9%。
- **Tox21**：LLaMA3-3B下AUC-ROC达83.4±3.3，相对提升约9.9%。
- **ClinTox**：LLaMA2-7B下AUC-ROC达94.3±0.1，相对提升约11.4%。
- **HIV**：LLaMA2-7B下AUC-ROC达83.2±1.9，相对提升约9.9%。
- **BACE**：LLaMA2-7B下AUC-ROC达98.4±0.8，相对提升高达41.4%，这是所有数据集中增益最大的，说明在原本基线表现较弱的任务上，结构标记的增益最为显著。

这些结果验证了核心瓶颈：现有方法因大量token导致注意力分散（Graph-to-Text）或模态不对齐（Graph-to-Embedding）而产生结构幻觉，而单个离散结构标记<SOGk>通过共享嵌入空间有效消除了这一幻觉。值得注意的是，<SOGk>仅需一个额外标记即可在3B/7B参数的小模型上超越GPT-4、Deepseek-R1等大模型，说明结构信息的有效传递比模型规模更关键。

### 消融与选择性验证 (RQ2)

**结构标记的选择性**是方法的核心因果机制。Table 2的消融实验表明：

![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/003_Table_2.jpg]]
*Table 2: Ablation of different structural token { \< S O G _ { k } > } on five datasets*

- **随机标记 vs. 正确标记**：使用随机结构标记或错误标记（即来自其他图结构的<SOGk>）会导致性能显著下降，甚至低于无结构标记的基线。这直接证明了结构标记的高度选择性——只有拓扑感知标记化器生成的正确标记才能忠实传递对应图的拓扑信息，并带来一致的性能提升。
- **Figure 2**通过玩具示例展示了不同标记选择导致的性能变化：当选择与图结构不匹配的标记时，AUC-ROC可能下降10–20个百分点，进一步确认了选择性机制。

**混合QA语料库的贡献**（Figure 3）：
- 三种QA类型（k-NN匹配、相似性判断、描述-标记配对）均对最终性能有正面贡献。
- 其中**描述-标记配对**贡献最大，移除该类型后平均性能下降最明显。这符合预期：描述-标记配对直接建立了自然语言描述与离散结构标记之间的映射，是桥接图空间和语言空间的关键对齐机制。

### 词汇表大小与锚节点策略

**结构词汇表大小K**（Table 4）：
- K=256时取得最佳平均性能（AUC-ROC 81.7）。
- K过小（如64）会导致不同图结构被迫映射到相同标记，信息区分度不足；K过大（如512）则可能因标记过于稀疏而难以有效对齐，且增加训练难度。

![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/012_Table_4.jpg]]
*Table 4: Effect of Structural Vocabulary Size K on Model Performance*

**锚节点选择策略**（Table 5）：
- 基于度中心性的选择优于随机选择，这与图论直觉一致：高度节点通常包含更丰富的拓扑信息，以它为锚点进行层次遍历能更好地捕获全局结构模式。

![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/011_Table_5.jpg]]
*Table 5: Comparison of Anchor Node Selection Strategies*

### 嵌入空间可视化与对齐验证

Figure 6的t-SNE可视化提供了关键证据：
- **结构标记嵌入**位于**文本标记嵌入**的邻域内，而Graph-to-Embedding方法（如GNP）生成的软提示嵌入则远离文本标记空间。
- 这说明<SOGk>成功实现了图空间与语言空间的对齐，而连续嵌入方法存在严重的模态不对齐——这正是其性能瓶颈的根本原因。

Figure 4的相关性热力图显示，前50个结构标记之间具有清晰的分块结构，表明词汇表内部形成了有意义的拓扑模式聚类，而非随机分布。

### 节点级任务扩展

<SOGk>通过构建2跳ego-graph将节点分类转化为图级任务。在Cora数据集上（Table 3），LLaMA3-3B达到91.58%的准确率，超越了所有基线。这表明结构标记方法在节点级任务上同样有效，但需注意：对于大规模图，2跳ego-graph的构建可能面临扩展性问题。

![[assets/figures/papers/iclr26_0001_eXidGkRUFt_One_LLM_Token_for_Explicit_Graph_Structural_Unde/figures/010_Table_3.jpg]]
*Table 3: Performance comparison on node classification, where bold indicates the best performance and underlined indicates the second-best*

### 失败模式与限制

1. **类别不平衡影响**：多数任务存在严重类别不平衡（Table 6），如HIV训练集中正样本仅占3.8%。虽然采用了1:1或1:5的重采样策略，但极端不平衡任务（如HIV）的性能仍然相对较低（83.2 AUC-ROC），说明结构标记无法完全补偿数据偏差。
2. **词汇表大小敏感性**：K=256在五个数据集上平均最优，但不同数据集的最优K可能不同。当前手动选择K的方式缺乏自适应机制。
3. **泛化范围有限**：实验仅在分子图（MoleculeNet）上进行，在社交网络、知识图谱等更广泛图类型上的泛化能力尚未验证。分子图具有特定的结构规律（如骨架共享模式见Figure 5、10、11），这些规律可能有助于结构标记的聚类，而在其他图类型中未必存在。
4. **组件依赖**：方法依赖于SentenceTransformers和GCN编码器的质量。如果这些预训练组件在特定领域表现不佳，结构标记的质量将受到限制。



## 定位与知识库关联

### 与基线方法的关系：从“文本化”与“投影”到“离散结构标记”

<SOGk>方法的核心贡献在于重新定义了图拓扑信息进入LLM的接口。现有方法可归为两类，各自存在根本性瓶颈：

1. **Graph-to-Text方法**（如Talk Like a Graph, InstructGraph, GraphText, LangTopo, Dr.E）将图结构展开为自然语言描述。其代价是token消耗量巨大，且线性文本序列难以忠实保留图的非欧拓扑结构，导致LLM产生“结构幻觉”——即模型在文本描述中丢失或扭曲了图的结构信息。

2. **Graph-to-Embedding方法**（如GraphGPT, LLaGA, G-retriever, TEA-GLM, GraphLLM, GraphAdapter, GNP）将图编码为连续向量，再通过MLP投影到LLM的嵌入空间。这类方法面临严重的**模态不对齐**问题：连续嵌入在几何空间中的分布与离散文本标记的语义空间存在结构性差异，导致LLM无法有效利用这些嵌入中的拓扑信息。

<SOGk>的因果机制在于引入一个离散的结构标记 `<SOGk>`，通过拓扑感知标记化器将图拓扑映射为单个离散标记，并与文本标记共享同一嵌入空间。这一设计同时解决了上述两类方法的缺陷：单个标记的token开销极小，且离散标记天然与文本标记的嵌入空间对齐，消除了模态不对齐问题。实验证据表明，在五个分子图级基准数据集上，<SOGk>相比基线实现了9.9%–41.4%的性能提升（Table 1），其中在BACE数据集上LLaMA2-7B达到了98.4 AUC-ROC，而最佳基线仅约57.0。

### 方法适用边界与关键设计约束

<SOGk>的适用边界由以下设计选择定义：

- **图类型**：当前方法仅在分子图（MoleculeNet）上验证，涵盖毒理学、临床研究和药物化学领域的17个子任务。在社交网络、知识图谱等其他图类型上的泛化能力尚未验证。
- **任务类型**：主要针对图级分类任务，节点级任务通过构建2跳ego-graph实现，对于更大规模的图可能面临扩展性问题。
- **模型规模**：实验基于LLaMA2-7B和LLaMA3-3B，在更大规模LLM（如70B参数）上的表现未知。
- **词汇表大小**：结构词汇表大小K需要手动选择，实验表明K=256时取得最佳平均性能（Table 4），但最优值可能因数据集而异。
- **依赖组件**：方法依赖于预训练的文本编码器（SentenceTransformers all-MiniLM-L6-v2）和GNN编码器（两层GCN），其性能受限于这些组件的质量。

### 核心局限与开放问题

**已知局限**：

1. **泛化边界模糊**：仅在分子图上验证，方法对动态图、异构图等更广泛图类型的适用性未知。
2. **词汇表选择依赖人工**：K值的最优选择缺乏自动化机制，且不同数据集的最优K值可能不同。
3. **组件级联误差**：结构标记化器的质量依赖于文本编码器和GNN编码器的预训练质量，错误会沿管道传播。
4. **扩展性约束**：节点级任务依赖ego-graph构建，在大规模图上计算成本可能过高。

**开放问题**：

1. **动态图与异构图扩展**：如何将<SOGk>的离散结构标记机制扩展到随时间演化的动态图或包含多种节点/边类型的异构图？
2. **锚节点选择策略的泛化**：当前使用度中心性选择锚节点，在非分子图（如社交网络中的影响力传播图）中是否仍为最优策略？
3. **结构标记的可解释性量化**：虽然t-SNE可视化（Figure 6）显示结构标记嵌入在文本标记的邻域内，且Figure 4的相关性热力图表明前50个结构标记具有可区分的模式，但如何通过注意力权重分析等更严格的方式量化每个结构标记所编码的具体拓扑模式？
4. **规模效应**：在70B参数级LLM上，单个结构标记是否仍能有效传递拓扑信息，还是需要增加标记数量？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/One_LLM_Token_for_Explicit_Graph_Structural_Understanding.pdf

![[paperPDFs/ICLR_2026/One_LLM_Token_for_Explicit_Graph_Structural_Understanding.pdf]]
