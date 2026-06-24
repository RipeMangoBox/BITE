---
title: "ToolWeaver: Weaving Collaborative Semantics for Scalable Tool Use in Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ToolWeaver_Weaving_Collaborative_Semantics_for_Scalable_Tool_Use_in_Large_Language_Models.pdf
openreview_forum_id: Ge1DKuzWTO
aliases:
- ToolWeaver
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过协作感知的残差向量量化将每个工具映射为层次化的离散码序列（组合码），以对数方式控制词汇增长，并利用共享码的稠密共现来学习工具间的协同模式。"
primary_logic: "将工具的内在功能语义与外在共现模式联合编码到层次化码本中，使模型能通过共享的父码学习协同性，从而克服单一标记瓶颈。"
claims:
- "在语义初始化基础上引入协同引导后，复杂I3多工具任务的NDCG@1大幅提升。"
- "在最复杂的I3检索场景中，ToolWeaver的NDCG@1达到88.00，显著超过ToolGen的81.00。"
- "平衡内在语义与外在协同模式至关重要，当协同正则化权重λ=1时性能达到峰值。"
- "ToolBench retrieval (I3) 上 NDCG@1 = 88.00"
---

# ToolWeaver: Weaving Collaborative Semantics for Scalable Tool Use in Large Language Models

> [!tip] 核心洞察
> 将工具的内在功能语义与外在共现模式联合编码到层次化码本中，使模型能通过共享的父码学习协同性，从而克服单一标记瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ToolWeaver：为大规模语言模型中的可扩展工具使用编织协同语义 |
| 英文题名 | ToolWeaver: Weaving Collaborative Semantics for Scalable Tool Use in Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ge1DKuzWTO); [GitHub](https://github.com/Fwibo/ToolWeaver) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | ToolWeaver |
| Dataset | ToolBench retrieval (I3), ToolBench end-to-end (I3), WikiText-2 (language modeling) |

> [!tip] 效果简介
> - ToolBench retrieval (I3) 上，NDCG@1 为 88.00，对比 81.00 (ToolGen)，变化 +7.00。
> - ToolBench end-to-end (I3) 上，SoPR 为 52.19，对比 36.34 (ToolGen)，变化 +15.85。
> - ToolBench end-to-end (I3) 上，SoWR (vs GPT-4o-mini) 为 59.02，对比 49.18 (ToolGen)，变化 +9.84。

## 概述

大规模语言模型（LLM）在工具使用方面面临一个根本性的可扩展瓶颈：主流的“一工具一标记”生成式范式为每个工具分配一个独立的原子标记，导致词汇量随工具数量线性增长，且标记间的语义隔离使模型难以从稀疏的独立工具ID共现中学习协同关系。当工具库规模扩展到数万级别时，这一瓶颈在复杂多工具协同场景中尤为突出。

**ToolWeaver** 提出了一种组合式的工具表示方法，将每个工具映射为由层次化离散码构成的序列，以对数方式控制词汇增长。其核心洞见在于：通过协作感知的残差向量量化（Collaborative-Aware RQ-VAE），将工具的内在功能语义与外在共现模式联合编码到层次化码本中，使模型能通过共享的父码学习工具间的协同性，从而克服单一标记的语义隔离瓶颈。

具体而言，ToolWeaver 的方法包含三个关键环节：（1）**结构化标记化**——利用文本编码器提取工具文档的稠密语义向量，再通过层次化残差量化生成组合式离散码序列，并在最后码本上施加基于Sinkhorn-Knopp算法的均匀映射约束以缓解索引冲突；（2）**协同引导**——基于历史使用轨迹构建工具共现相似度矩阵，通过图拉普拉斯正则化项将协同信号注入量化过程，使频繁共现的工具在码空间中被拉近；（3）**两阶段生成对齐**——先进行工具检索对齐训练，再进行端到端的工具使用轨迹对齐，将结构化码集成到LLM的生成过程中。

在包含近47,000个工具的ToolBench基准上，ToolWeaver在工具检索和端到端工具使用两个层面均显著优于现有方法。在最复杂的I3多工具检索场景中，ToolWeaver的NDCG@1达到88.00，较生成式基线**ToolGen**（Wang et al., 2024b）的81.00提升7个点；端到端任务完成率（SoPR）从36.34提升至52.19，相对提升超过15个百分点。消融实验表明，语义初始化为检索性能带来了超过20个NDCG点的跃升，而协同引导的增益随任务复杂度递增——在简单I1任务上收益温和，在复杂多工具I3任务上最为显著。协同正则化权重λ的最优值为1，验证了内在语义与外在协同模式之间需要精细平衡的核心假设。此外，ToolWeaver在保持通用语言能力方面也显著优于“一工具一标记”范式，其语言建模困惑度仅为25.36，远低于ToolGen的104.54。

在方法谱系上，ToolWeaver处于工具检索与生成式工具使用的交叉地带。与经典的检索式方法（如**BM25**、稠密嵌入相似度**EmbSim**、有监督检索器**ToolRetriever** (Qin et al., 2023)）相比，ToolWeaver将工具选择直接融入LLM的生成过程，避免了独立检索器的级联误差；与生成式基线**ToolGen**相比，它用组合码替代原子标记，从根本上解决了词汇爆炸和语义隔离问题。当前工作的主要局限在于实验仅在ToolBench上进行，跨数据集的泛化性尚待验证；工具协同模式依赖历史轨迹的共现统计，冷启动场景下协同信号可能不足。

## 背景与动机

大规模语言模型（LLM）通过调用外部工具，显著扩展了其在复杂推理与真实世界交互中的能力边界。然而，随着可用工具数量的急剧膨胀——例如 ToolBench 数据集包含近 47,000 个 API——如何高效地将海量工具集成到 LLM 中，已成为制约工具增强型智能体走向实用的核心瓶颈。

### 现有范式的可扩展性困境

当前主流的工具集成方法遵循“一工具一标记”（one-token-per-tool）的生成式范式，即 **ToolGen**（Wang et al., 2024b）为代表的方案：为每个工具分配一个唯一的特殊标记（atomic token），模型通过生成该标记来选择和调用工具。这一范式面临两个根本性缺陷：

**词汇量线性膨胀。** 每新增一个工具就需要在词表中添加一个独立标记。当工具数量达到数万级别时，词表规模随之线性增长。如 Figure 1(a) 所示，这种扁平化的词汇结构导致模型需要维护一个极其庞大的离散输出空间，不仅增加了训练和推理的存储开销，更使得生成过程中的搜索空间急剧扩大。

**语义隔离与协同信号缺失。** 更为关键的是，独立标记之间的语义是完全隔离的。在“一工具一标记”方案下，两个功能相近或经常协同使用的工具——例如“实时天气查询”与“空气质量查询”——被分配了毫无关联的离散 ID。模型只能从稀疏的工具 ID 共现中隐式地学习它们之间的协作关系，而无法利用工具自身的功能语义或历史使用模式中的协同信号。如 Figure 1(b) 所示，当用户提出“今天带孩子去公园合适吗？”这类需要多工具协同的复杂查询时，模型难以在彼此孤立的标记之间建立起有效的推理链路。

### 核心洞察

上述困境的症结在于：**工具表示的形式（原子标记）与其承载的信息（功能语义与协同模式）之间存在结构性的不匹配。** 原子标记将每个工具压缩为词表中的一个孤立点，既无法表达工具内在的功能语义，也无法编码工具之间外在的协作关系。

ToolWeaver 的核心洞察是：**将工具的内在功能语义与外在共现模式联合编码到一个层次化的离散表示空间中。** 具体而言，通过协作感知的残差向量量化（collaborative-aware RVQ），每个工具被映射为由多个码本生成的层次化离散码序列（compositional code sequence）。这种组合式表示从两个维度突破了原子标记的瓶颈：

- **对数级可扩展性：** 使用 $L$ 个大小为 $K$ 的码本，表示容量可达 $K^L$ 个工具，而仅需引入 $L \times K$ 个新标记，将词汇增长从线性压缩为对数级别。
- **协同语义编织：** 层次化码本的结构使得功能相关的工具能够共享父码（parent code），从而在训练过程中形成稠密的共现信号。模型可以通过这些共享的父码学习到工具之间的协同模式，为多工具协作推理提供结构化的先验知识。

### 技术挑战

实现上述构想需要解决三个关键挑战。第一，如何将工具文档的语义信息与历史使用轨迹中的协同信号有机融合到向量量化的码本学习中？第二，如何确保层次化码本的每一层都能得到有效利用，避免码本坍缩（codebook collapse）导致的表示容量浪费？第三，如何将学习到的离散工具表示无缝集成到 LLM 的生成框架中，使模型能够准确地生成有效的工具码序列？ToolWeaver 通过协作感知的码本学习、基于 Sinkhorn-Knopp 的均匀映射约束、以及两阶段生成对齐，系统性地回应了这些挑战。

## 核心创新

ToolWeaver 的核心创新在于**将工具的离散表示从“原子标记”范式重构为“组合式层次化码序列”**，并将工具间的协同模式显式编码到码本学习中，从而系统性地解决了现有生成式工具使用方法的可扩展性瓶颈。

### 1. 从原子标记到组合式层次化码序列

现有方法（如 **ToolGen**，Wang et al., 2024b）遵循“一工具一标记”范式：每个工具被分配一个唯一的特殊标记，导致词汇量随工具数量线性增长，且各工具的标记在语义上完全隔离。ToolWeaver 的核心变革在于采用**残差向量量化（Residual Vector Quantization, RQ-VAE）** 将每个工具表示为一段层次化的离散码序列。

具体而言，ToolWeaver 使用 $L$ 个码本 $\mathcal{C} = \{C_1, \ldots, C_L\}$，每个码本包含 $K$ 个可学习的码向量。每个工具被映射为一个长度为 $L$ 的索引序列 $[\iota_1, \iota_2, \ldots, \iota_L]$，其中第 $l$ 层的索引由当前残差与码本中心点的最近邻匹配决定：

$$\iota_{d,l} = \underset{k \in \{1, \ldots, K\}}{\arg\min} \| r_{d,l} - v_{l,k} \|_2^2$$

残差随后更新为 $r_{d,l+1} = r_{d,l} - v_{l,\iota_{d,l}}$，进入下一层量化。这种组合式结构带来了**对数级别的可扩展性**：仅需 $L \times K$ 个新标记即可表示多达 $K^L$ 个工具，从根本上打破了词汇量线性膨胀的瓶颈。

### 2. 协同感知的码本学习：从语义隔离到协同编码

这是 ToolWeaver 最具区分度的创新。在“一工具一标记”范式下，每个工具的标记是独立的原子符号，模型只能从稀疏的工具 ID 共现中隐式学习工具间关系。ToolWeaver 则通过**协同图拉普拉斯正则化**将工具间的协作模式显式注入码本学习过程。

首先，从工具使用轨迹中构建工具共现矩阵 $C$，并计算工具间的协同相似度：

$$A_{uv} = \frac{C_{uv}}{\sqrt{C_{uu} \cdot C_{vv}}}$$

然后，在 RQ-VAE 的训练目标中加入协同正则化项：

$$\mathcal{L}_{\mathrm{collab}} = \sum_{u,v \in \mathcal{D}} A_{uv} \| \hat{z}_u - \hat{z}_v \|_2^2$$

该损失函数惩罚经常协同使用的工具在量化空间中距离过远，迫使共享的父码（parent code）承载工具间的协同语义。这意味着，当模型学习生成某个工具的层次化码序列时，共享的父码使其能够自然地泛化到同一“协同簇”中的其他工具——这是原子标记范式无法实现的。

### 3. 索引冲突缓解：均匀映射约束

层次化码本的组合式结构带来了新的挑战：当工具数量远小于理论容量 $K^L$ 时，最后一层码本的索引分配可能出现严重不均衡，导致某些码向量未被充分利用。ToolWeaver 在最后码本 $C_L$ 上施加基于 **Sinkhorn-Knopp 算法**的均匀映射约束，将索引分配建模为最优传输问题，确保工具表示尽可能均匀地分布在各中心点上，从而最大化码本利用率并避免表示退化。

### 4. 两阶段生成对齐

与 ToolGen 的单阶段微调不同，ToolWeaver 采用**两阶段生成对齐**策略将结构化码集成到 LLM 中：

- **第一阶段：工具检索对齐**。训练模型根据用户查询 $q$ 生成正确的工具码序列，优化目标为：

$$\mathcal{L}_{\mathrm{retrieval}} = -\mathbb{E}_{(q,d)}[\log P(\iota_d | q)]$$

- **第二阶段：工具使用轨迹对齐**。在检索对齐的基础上，进一步训练模型生成完整的工具调用轨迹，包括参数生成和结果整合。

两阶段设计使得模型先掌握“何时选择哪个工具”，再学习“如何使用工具”，避免了端到端训练中检索信号被复杂的轨迹生成目标所淹没。

### 创新点小结

| 设计维度 | 基线方法（ToolGen） | ToolWeaver 创新 |
|---------|-------------------|----------------|
| 工具表示 | 唯一单一特殊标记 | $L$ 层码本生成的层次化离散码序列 |
| 词汇量增长 | 线性增长 | 对数增长（$K^L$ 容量，$L \times K$ 标记） |
| 工具间关系 | 隐式共现学习 | 协同图拉普拉斯正则化显式编码 |
| 索引冲突 | 无专门机制 | Sinkhorn-Knopp 均匀映射约束 |
| 微调策略 | 单阶段 | 两阶段（检索对齐 + 轨迹对齐） |

消融实验为这些创新提供了强有力的因果证据：语义初始化（即使用 RQ-VAE 编码工具文档语义）使检索 NDCG 提升超过 20 个点，构成工具表示的基础；在此基础上引入协同引导后，性能进一步提升，且提升幅度与任务复杂度正相关——在复杂的多工具 I3 任务上最为显著。协同正则化权重 $\lambda$ 的敏感性分析进一步验证了核心假设：$\lambda=1$ 时性能达到峰值，过小则协同信号不足，过大则压制了工具内在语义，说明**平衡内在语义与外在协同模式**是 ToolWeaver 成功的关键机制。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/001_Figure_1.jpg]]
*Figure 1: An overview of the ToolWeaver framework. (a) We contrast the standard “one-token-pertool” method, which creates a massive flat vocabulary, with our compositional approach that scales logarithmically. (b) Our model leverages collaborative signals between tools (e.g., Realtime Weather and Air Quality) for complex reasoning where “one-token-per-tool” representations fail. (c) The ToolWeaver architecture learns these structured representations through a collaborativeaware vector quantization process, which are then integrated into an LLM*

ToolWeaver 的整体流程围绕一个核心瓶颈展开：传统“一工具一标记”的生成式范式导致词汇量随工具数量线性增长，且独立的原子标记无法捕捉工具间的协同使用模式。ToolWeaver 通过三个紧密耦合的阶段来破解这一瓶颈。

### 1. 结构化标记化

这是框架的核心引擎。给定一个包含近 47,000 个工具的大型工具库，每个工具首先通过文本编码器从其文档中提取稠密语义向量 $e_d$。随后，这些向量进入一个**协作感知的残差向量量化**过程：工具被映射为由 $L$ 层码本生成的层次化离散码序列，每层码本包含 $K$ 个可学习的中心向量。这种组合式表示以对数方式控制词汇增长——仅需 $L \times K$ 个新标记即可表示多达 $K^L$ 个工具，从根本上解决了词汇膨胀问题。

区别于标准 RQ-VAE 的关键在于码本学习目标中引入了**协同图拉普拉斯正则化**。框架从历史使用轨迹中构建工具共现矩阵，并据此计算工具间的余弦相似度 $A_{uv}$。正则化项 $\mathcal{L}_{\mathrm{collab}} = \sum_{u,v} A_{uv} \| \hat{z}_u - \hat{z}_v \|_2^2$ 惩罚协同使用的工具在量化空间中距离过远，使得共享父码的工具天然地学习到协同关系。同时，为解决码本利用不均导致的索引冲突，框架在最后一层码本上施加基于 Sinkhorn-Knopp 算法的均匀映射约束，确保工具在各中心点上均匀分布。

### 2. 两阶段生成对齐

结构化码本训练完成后，需要将这些离散码序列集成到 LLM 中。ToolWeaver 采用**两阶段微调**策略：

- **第一阶段：工具检索对齐**。训练模型根据用户查询 $q$ 生成正确的工具码序列 $\iota_d$，损失函数为 $\mathcal{L}_{\mathrm{retrieval}} = -\mathbb{E}_{(q,d)}[\log P(\iota_d | q)]$。这一阶段使模型学会从海量工具库中精准定位所需工具。
- **第二阶段：工具使用轨迹对齐**。在检索能力基础上，进一步训练模型生成完整的工具调用轨迹，包括参数填充、API 调用和结果整合，实现端到端的工具使用能力。

### 3. 受限解码

推理时，为防止模型生成无效的工具码序列，ToolWeaver 利用所有有效工具码构建前缀树，通过受限束搜索约束生成过程，确保输出始终对应一个合法工具。

### 输入输出流

整体来看，框架的输入包括：工具文档语料、历史使用轨迹、以及用户查询。输出为：层次化工具码序列，直接集成在 LLM 的生成文本中，无需额外的检索器模块。图 1 展示了从“一工具一标记”到组合式表示的对比，以及协同信号如何在复杂多工具推理场景中发挥作用。

## 核心模块与公式推导

ToolWeaver 的核心由三个模块构成：**结构化标记化**、**协同图构建**，以及**两阶段生成对齐**。其关键创新在于将工具的内在功能语义与外在共现模式联合编码到层次化码本中，使模型能通过共享的父码学习工具间的协同性。

### 结构化标记化

该模块是 ToolWeaver 的核心，包含语义初始化、协同感知残差量化与冲突缓解三个阶段。

**初始语义编码。** 对每个工具 $d$ 的文档 $\mathrm{Doc}_d$，首先通过文本编码器获得稠密语义向量：

$$e_d = \mathrm{Text-Encoder}(\mathrm{Doc}_d)$$

该向量作为残差量化的输入初始残差 $r_{d,1} = e_d$。

**协同感知残差量化。** 采用 $L$ 个码本 $\{C_1, \dots, C_L\}$，每个码本 $C_l$ 包含 $K$ 个可学习码向量。在第 $l$ 层，为当前残差 $r_{d,l}$ 分配最近的中心点索引：

$$\iota_{d,l} = \arg\min_{k \in \{1, \ldots, K\}} \| r_{d,l} - v_{l,k} \|_2^2$$

随后计算下一层残差：

$$r_{d,l+1} = r_{d,l} - v_{l,\iota_{d,l}}$$

每个工具最终表示为一个长度为 $L$ 的离散码序列 $[\iota_{d,1}, \dots, \iota_{d,L}]$，表征容量可达 $K^L$，而新增词汇量仅为 $L \times K$，实现对工具数量的对数级词汇增长。

**协同引导。** 为让码本学习感知工具间的共现关系，引入基于工具共现相似度矩阵的图拉普拉斯正则化。工具 $u$ 与 $v$ 的共现相似度定义为：

$$A_{uv} = \frac{C_{uv}}{\sqrt{C_{uu} \cdot C_{vv}}}$$

其中 $C_{uv}$ 为两工具在历史使用轨迹中的共现次数。协同正则化损失惩罚经常共现的工具在量化空间中距离过远：

$$\mathcal{L}_{\mathrm{collab}} = \sum_{u,v \in \mathcal{D}} A_{uv} \| \hat{z}_u - \hat{z}_v \|_2^2$$

其中 $\hat{z}_u$ 为工具 $u$ 在所有层级量化后的累积表示。总损失为标准 RQ-VAE 的重建损失、量化损失与该协同正则化项的加权和，权重 $\lambda$ 在实验中证明取 1 时性能最优。

**冲突缓解。** 为防止工具在最终码本 $C_L$ 上集中映射到少数中心点，对最后一层的索引分配施加基于 Sinkhorn-Knopp 算法的均匀映射约束，将分配问题建模为最优传输问题，强制每个中心点承载等量工具，从而最大化码本利用率。

### 协同图构建

协同图基于工具使用轨迹中的共现统计构建。从交互轨迹 $\mathrm{Traj} = [q, (p_1, d_1, \alpha_1, f_1), \dots, (p_t, d_t, \alpha_t, f_t), a]$ 中提取工具共现矩阵 $C$，再通过上述余弦归一化得到相似度矩阵 $A$，作为协同正则化的监督信号。

### 两阶段生成对齐

将结构化码序列集成到 LLM 中分两阶段微调：

**阶段一：工具检索对齐。** 训练模型根据用户查询 $q$ 生成正确的工具码序列 $\iota_d$：

$$\mathcal{L}_{\mathrm{retrieval}} = -\mathbb{E}_{(q,d)}[\log P(\iota_d | q)]$$

**阶段二：工具使用轨迹对齐。** 在检索对齐基础上，进一步微调模型生成完整的工具调用与推理轨迹。

推理时采用受限解码：预计算所有有效工具码序列的前缀树，引导束搜索确保生成的码序列始终对应有效工具。

## 实验与分析

### 主实验设置

实验基于 **ToolBench** 基准进行，该基准包含近 47,000 个真实工具，并依据查询复杂度划分为三个层级：**I1**（单工具）、**I2**（类别内多工具）和 **I3**（跨类别多工具）。对比方法涵盖经典检索基线（**BM25**, Robertson & Zaragoza, 2009）、稠密嵌入相似度（**EmbSim**）、有监督检索式方法（**ToolRetriever**, Qin et al., 2023），以及生成式“一工具一标记”基线（**ToolGen**, Wang et al., 2024b）。所有生成式方法均基于相同的 **Llama-3-8B** 基础模型进行微调，训练配置和超参数按各自论文推荐设置，确保了比较的公平性。

### 工具检索性能（Table 1）

ToolWeaver 在工具检索任务上全面超越所有基线方法。在最复杂的 **I3** 场景中，ToolWeaver 的 **NDCG@1 达到 88.00**，显著高于 ToolGen 的 81.00（+7.00），也远超检索式方法中最好的 ToolRetriever（NDCG@1 为 64.86）。在 I1 和 I2 场景中，ToolWeaver 同样保持领先，NDCG@1 分别达到 91.16 和 89.76。这一结果直接验证了核心假设：层次化组合码比单一原子标记能更有效地捕获工具的语义与协同关系。


![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/002_Table_1.jpg]]
*Table 1: Tool retrieval evaluation performance on ToolBench. Performance is measured by NDCG@k across varying query complexities (I1-I3). ToolWeaver consistently outperforms both retrieval-based (BM25, EmbSim, ToolRetriever) and generative (ToolGen) methods. * represents the results disclosed in Wang et al. (2024b), while the others are the results we re-implemented based on the open-source checkpoints*

值得注意的是，ToolWeaver 的优势随任务复杂度增加而扩大——在简单 I1 任务上相对 ToolGen 的增益为 +2.16，而在需要多工具协同的 I3 任务上增益扩大至 +7.00，表明协同语义编码对复杂推理场景尤为关键。

### 端到端工具使用性能（Table 2）

在端到端评估中，ToolWeaver 同样展现出显著优势。以 **SoPR**（Solvable Pass Rate）衡量任务完成率，在 I3 场景下 ToolWeaver 达到 **52.19**，远超 ToolGen 的 36.34（+15.85）。以 **SoWR**（Solvable Win Rate）衡量相对于 GPT-4o-mini 的胜率，ToolWeaver 在 I3 场景下达到 **59.02**，而 ToolGen 仅为 49.18（+9.84）。在 I1-Tool 和 I1-Cat 等未见工具泛化场景中，ToolWeaver 同样保持领先，SoPR 分别达到 54.08 和 57.50。


![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/003_Table_2.jpg]]
*Table 2: Comparison of end-to-end evaluation performance on ToolBench, measured by Solvable Pass Rate (SoPR) and Solvable Win Rate (SoWR). The SoWR is calculated against the GPT-4omini baseline. GPT-4o-mini and ToolLlama-2 are tested in a challenging Retrieval setting (Re.) that requires selecting tools from the full set. In contrast, ToolGen and ToolWeaver generate tool tokens directly, without the need for a retriever. ToolWeaver outperforms other models in diverse scenarios, highlighting its effectiveness in both tool selection and execution*

### 通用语言能力保持（Table 3）

工具词汇的引入通常会损害基础模型的语言能力。在 WikiText-2 语言建模评估中，ToolGen 的困惑度（PPL）从基础模型的约 6.5 急剧上升至 **104.54**，而 ToolWeaver 仅为 **25.36**，显著减轻了对原有语言能力的损害。在 CNN/DailyMail 摘要任务上，ToolWeaver 的 BERTScore（85.07）几乎与基础模型（85.35）持平，而 ToolGen 则下降至 83.25。这表明 ToolWeaver 的紧凑组合式词汇（仅需 $L \times K$ 个新标记）比 ToolGen 的扁平大词汇（每个工具一个标记）对模型原有能力的干扰更小。

### 消融分析（Figure 3）

消融实验揭示了各组件对性能的贡献层级：


![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/007_Figure_3.jpg]]
*Figure 3: Cumulative ablation analysis of ToolWeaver’s components on tool selection (NDCG@k). Performance is shown for the baseline (w/o Semantic Initialization), after adding semantic initialization (w/o Collaborative Guidance), and for the full model*

1. **语义初始化**是工具表示最关键的基础。在未使用语义初始化的基线（随机初始化码本）上加入语义编码后，检索 NDCG 指标**提升超过 20 个点**，证明将工具文档的语义信息编码到离散码中对检索至关重要。

2. **协同引导**在语义初始化基础上进一步带来显著提升，且增益幅度随任务复杂度增加而扩大。在复杂多工具 I3 任务上，协同引导带来的额外增益最为明显，验证了通过共享父码学习工具共现模式的有效性。

3. 完整的 ToolWeaver（语义初始化 + 协同引导 + 冲突缓解）在所有指标上达到最佳性能。

### 协同正则化权重 λ 敏感性分析（Figure 2）

协同正则化权重 λ 控制内在语义与外在协同模式之间的平衡。实验表明，模型性能随 λ 从 0.01 增加到 1 的过程中持续提升，在 **λ = 1 时达到峰值**。当 λ 进一步增大至 10 时，性能开始下降。这一结果实证验证了核心假设：**最佳性能来自工具内在语义与外在协同模式之间的平衡**，过度强调任何一方都会损害整体表现。


![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/004_Figure_2.jpg]]
*Figure 2: Analysis of the collaborative regularization weight λ. Performance, measured by average NDCG@k across all I1-I3 scenarios, consistently peaks at λ = 1*

### 标记化策略对比（Table 6, Table 7）

与多种标记化策略的对比进一步验证了 ToolWeaver 设计的有效性：


![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Ge1DKuzWTO/figures/011_Table_6.jpg]]
*Table 6: Retrieval performance (NDCG@k) of different tokenization methods. ToolWeaver’s approach of integrating collaborative semantics into a structured representation yields the best performance, especially in complex multi-tool scenarios (I2, I3)*

- **Numerical**（数字 ID）：性能最差，完全缺乏语义信息。
- **Hierarchical**（层次化随机码）：因缺乏语义基础而表现不佳。
- **Semantic**（纯语义量化）：优于随机方法，但缺少协同引导。
- **Atomic**（原子标记，即 ToolGen）：在简单任务上表现尚可，但在多工具场景中因语义隔离而受限。
- **ToolWeaver**（语义 + 协同 + 层次化）：在所有场景中表现最佳，尤其在 I2 和 I3 等多工具场景中优势最为突出。

### 超参数敏感度分析（Figure 5）

**词汇量大小**（Figure 5a）：在固定码长 $L=2$ 的条件下，性能在词汇量为 **2,048 个标记**时达到峰值。词汇量过小（256）表达能力不足，过大（16,384）则导致码空间稀疏，削弱协同学习效果。这证实了紧凑词汇有利于更好的协同学习。

**码长**（Figure 5b）：在固定码本大小 $K=1024$ 的条件下，较深的层次结构（$L=4$）能提升语义分辨率，但过长的码序列（$L=6$）因生成复杂度增加而导致性能下降。

### 推理效率（Table 13）

ToolWeaver 的推理延迟随码本深度 $L$ 线性增长，但绝对开销很小（约 20-75ms）。更重要的是，ToolWeaver 保持了**较低且恒定的内存占用**，而原子标记方法（ToolGen）的词汇嵌入表随工具数量线性增长，在大规模工具库场景下面临内存瓶颈。

### 失败模式分析（Figure 8）

失败类型分布分析显示，随着任务复杂度从 I1 增加到 I3，工具选择错误的占比有所上升，但 ToolWeaver 在各类失败模式上的分布优于基线方法。在工具和类别泛化场景（I1-Tool, I1-Cat, I2-Cat）中，ToolWeaver 的失败率同样低于对比方法，表明层次化组合码在未见工具上具有更好的泛化能力。

### 跨模型尺寸验证（Table 8）

在 Qwen-2.5 系列的不同模型尺寸（1.5B, 3B, 7B, 14B）上，ToolWeaver 在 I2 和 I3 场景中始终优于 ToolGen，且优势随模型尺寸增大而更加明显。这表明协同语义编码的有效性不限于特定模型架构或规模。

### 已知局限

1. 所有实验均在 ToolBench 数据集上进行，未在其他工具使用基准（如 API-Bank）上验证，跨数据集的泛化性未知。
2. 工具协同模式的学习依赖于历史使用轨迹的共现统计，对于新工具或冷启动场景，协同信号可能不足，需要额外机制支持。

## 方法谱系与知识库定位

### 问题根因与核心调控变量

现有工具增强LLM的主流方案可归为两类：检索式方法（如 **ToolRetriever** (Qin et al., 2023)）与生成式方法。生成式方法中的“一工具一标记”范式（以 **ToolGen** (Wang et al., 2024b) 为代表）为每个工具分配一个唯一的原子标记，其根本瓶颈在于：词汇量随工具数量**线性增长**，且各工具标记在语义上相互隔离，模型难以从稀疏的独立ID共现中学习工具间的协同关系。这导致两个后果：（1）大规模工具库下的可扩展性差；（2）需要多工具协作的复杂查询（如“查询天气后判断是否适合带孩子去公园”）中，模型无法利用工具间的功能互补性。

ToolWeaver的因果调控变量是**工具标记的组合化与协同感知**。它通过协作感知的残差向量量化（RQ-VAE）将每个工具映射为一组层次化的离散码序列（组合码），以对数方式控制词汇增长，并利用共享码的稠密共现来学习工具间的协同模式。核心洞见在于：将工具的内在功能语义与外在共现模式联合编码到层次化码本中，使模型能通过共享的父码学习协同性，从而克服单一标记瓶颈。

### 方法沿革与关键改进

ToolWeaver在生成式工具使用范式上对 **ToolGen** (Wang et al., 2024b) 进行了系统性改进，主要体现在四个关键槽位：

| 设计维度 | ToolGen（基线） | ToolWeaver（本文） | 改进机理 |
|---------|---------------|-------------------|---------|
| **工具表示** | 唯一单一特殊标记（原子标记） | 由 $L$ 个大小为 $K$ 的码本生成的层次化离散码序列 | 词汇量从 $\mathcal{O}(N)$ 降至 $\mathcal{O}(L \times K)$，表示容量达 $K^L$ |
| **码本学习目标** | 标准RQ-VAE的重建损失与量化损失 | 标准RQ-VAE损失 + 基于工具共现矩阵的图拉普拉斯正则化项 $\mathcal{L}_{\mathrm{collab}} = \sum_{u,v} A_{uv} \| \hat{z}_u - \hat{z}_v \|_2^2$ | 强制经常共现的工具在量化空间中邻近，使共享父码承载协同语义 |
| **索引冲突处理** | 无专门机制 | 在最后码本上施加基于Sinkhorn-Knopp算法的均匀映射约束 | 避免多个工具映射到相同码序列，保证表示的唯一性 |
| **微调策略** | 单一阶段微调 | 两阶段生成对齐：先进行工具检索对齐（$\mathcal{L}_{\mathrm{retrieval}} = -\mathbb{E}_{(q,d)}[\log P(\iota_d \| q)]$），再进行工具使用轨迹对齐 | 分阶段注入检索能力与执行能力，降低联合优化的难度 |

与检索式基线相比，**BM25** (Robertson & Zaragoza, 2009) 和 **EmbSim** 仅依赖文本相似度，无法捕捉工具间的协同使用模式；**ToolRetriever** (Qin et al., 2023) 虽通过有监督训练学习检索，但仍将工具视为独立实体。ToolWeaver的生成式框架将工具选择与后续使用统一到同一自回归过程中，避免了检索-执行的流水线误差传播。

### 适用边界与局限

**已验证的适用条件**：
- 所有实验均在 **ToolBench** 数据集上进行，涵盖近47,000个工具，验证了大规模工具库下的有效性。
- 在跨模型尺寸的实验中（Qwen-2.5 1.5B至14B），ToolWeaver在复杂任务（I2、I3）上持续优于ToolGen，表明方法对模型容量具有较好的鲁棒性。
- 在域内（In-domain）与多域（Multi-domain）两种设置下均表现出一致的优势。

**已知局限**：
1. **跨数据集的泛化性未验证**：所有实验仅基于ToolBench，未在API-Bank等其他工具使用基准上评估，方法在不同工具库分布下的表现尚不可知。
2. **冷启动问题**：工具协同模式的学习依赖于历史使用轨迹的共现统计。对于新加入的工具或使用频率极低的工具，协同信号可能不足，导致码本分配质量下降。文中未给出增量添加新工具的具体方案。
3. **层次深度与宽度的选择**：消融实验表明，词汇量2,048 tokens、码长 $L=2$ 时性能最优，过深的层次（$L=6$）会因生成序列过长而损害性能。但最优超参数是否可自动确定或跨数据集迁移，仍是开放问题。

### 未解决的问题与未来方向

1. **增量工具学习**：如何在保持已学习协同结构的前提下，高效地为新工具分配码序列而不触发全局重训练，是实际部署中的关键挑战。
2. **协同信号的泛化边界**：协同引导是否有助于模型泛化到未曾同时使用过但功能相关的工具对（例如两个功能相似但来自不同域的API），文中未做专门分析。
3. **码本结构的自适应设计**：层次化码本的最优深度 $L$ 和宽度 $K$ 是否可以根据工具库的统计特性（如工具总数、共现稀疏度）自动确定，而非依赖人工调参。
4. **与其他工具增强范式的融合**：ToolWeaver目前仅与生成式方法对比，其组合码表示是否可以与检索式方法的优势互补（如在检索阶段利用码的层次结构加速候选集筛选），值得探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/ToolWeaver_Weaving_Collaborative_Semantics_for_Scalable_Tool_Use_in_Large_Language_Models.pdf]]
