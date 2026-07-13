---
title: "MetaEmbed: Scaling Multimodal Retrieval at Test-Time with Flexible Late Interaction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MetaEmbed_Scaling_Multimodal_Retrieval_at_Test_Time_with_Flexible_Late_Interaction.pdf
project_link: null
code_link: https://github.com/facebookresearch/MetaEmbed
openreview_forum_id: yKDqg9HwZX
aliases:
- MetaEmbed
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "在查询和候选的输入序列中附加少量可学习的 Meta 令牌，并利用其 VLM 最后隐藏状态作为上下文感知的多向量嵌入；通过 Matryoshka 多向量检索训练强制嵌入呈前缀嵌套结构，使用户在测试时可通过选择不同前缀组来调节检索预算。"
primary_logic: "通过固定数量的可学习 Meta 令牌获取紧凑的多向量表示，并并行优化多个嵌套组的前缀表示，使模型第一次在多模态多向量检索中实现测试时“精度-效率”可动态伸缩的能力。"
claims:
- "METAEMBED 引入少量可学习的 Meta 令牌，并将其最后隐藏状态作为紧凑的多向量嵌入。"
- "Matryoshka Multi-Vector Retrieval (MMR) 组织嵌入为嵌套组，实现测试时检索预算的选择。"
- "METAEMBED 在 MMEB 和 ViDoRe v2 上取得了最先进的检索性能，远超相同规模的最强单向量基线。"
- "测试时可伸缩性显著：将检索预算从 (1,1) 增加到 (16,64) 在所有模型尺寸上均提升性能，在 32B 模型上增益最大（+6.6 个百分点）。"
---

# MetaEmbed: Scaling Multimodal Retrieval at Test-Time with Flexible Late Interaction

> [!tip] 核心洞察
> 通过固定数量的可学习 Meta 令牌获取紧凑的多向量表示，并并行优化多个嵌套组的前缀表示，使模型第一次在多模态多向量检索中实现测试时“精度-效率”可动态伸缩的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MetaEmbed：通过灵活延迟交互实现测试时多模态检索的规模化 |
| 英文题名 | MetaEmbed: Scaling Multimodal Retrieval at Test-Time with Flexible Late Interaction |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=yKDqg9HwZX) · [GitHub](https://github.com/facebookresearch/MetaEmbed) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | METAEMBED |
| Dataset | MMEB, ViDoRe v2 |

> [!tip] 效果简介
> - MMEB 上，Overall Precision@1 为 69.1，对比 67.5，变化 +1.6。
> - MMEB 上，Overall Precision@1 为 76.6，对比 71.5，变化 +5.1。
> - ViDoRe v2 上，Avg. NDCG@5 为 61.3，对比 57.5，变化 +3.8。

## 概要

### 问题瓶颈

多模态检索系统面临一个根本性张力：单向量方法（如 CLIP、VLM2Vec）将查询与候选压缩为单个嵌入向量，计算高效但丢失细粒度语义信息；多向量方法（如 ColPali、ColQwen2）通过延迟交互保留更丰富的表示，却带来高昂的计算与存储开销。更关键的是，现有方案难以同时支持查询端和候选端均包含图像的多模态到多模态检索，且嵌入维度与向量数量在训练后即被固化，无法在测试时根据延迟和存储预算进行动态调整。

### 核心方法

**METAEMBED** 提出了一种可伸缩的延迟交互检索框架，其核心调控机制包含两个协同组件：

1. **Meta 令牌嵌入**：在查询和候选的输入序列后附加少量可学习的 Meta 令牌，利用视觉语言模型（VLM）的最后隐藏状态作为上下文感知的多向量嵌入。这些嵌入紧凑且富有表达力，能通过上下文化捕获细粒度语义。

2. **Matryoshka 多向量检索（MMR）**：受 Matryoshka 表示学习启发，将 Meta 嵌入组织为前缀嵌套结构——前几个向量形成粗粒度摘要，后续向量逐步精细化表示。训练时并行优化多个嵌套组的对比损失，使模型习得从粗到细的多向量嵌入，测试时用户可通过选择不同前缀组来调节检索预算。

这种设计首次在多模态多向量检索中实现了测试时“精度-效率”的可动态伸缩：增大查询与候选端使用的 Meta 嵌入数量可提升检索质量，但会增加索引存储和检索延迟，用户可根据实际约束灵活权衡。

### 主要发现

- **最先进性能**：METAEMBED-7B 在 MMEB 基准上达到 76.6 的整体 Precision@1，超越最强单向量基线 MoCa-7B（71.5）超过 5 个百分点；在 ViDoRe v2 上取得 61.3 的平均 NDCG@5，优于多向量方法 ColQwen2（57.5）。

- **测试时可伸缩性**：将检索预算从 (1,1) 增加到 (16,64) 在所有模型尺寸上一致提升性能，其中 32B 模型增益最大（+6.6 个百分点），且随模型规模扩大收益递减效应较弱。

- **架构鲁棒性**：METAEMBED 可适配不同的 VLM 骨干（Qwen2.5-VL、PaliGemma、Llama-3.2-Vision），表现出跨架构的稳定性。

### 方法定位

METAEMBED 处于单向量检索与多向量检索的交叉地带。与单向量基线（如 VLM2Vec、MM-EMBED、MoCa）相比，它通过多向量延迟交互捕获更细粒度的跨模态对齐；与传统多向量方法（如 ColPali）相比，它通过固定数量的 Meta 令牌获得紧凑表示，并借助 MMR 训练赋予测试时可伸缩性。在方法谱系上，METAEMBED 是首个将 Matryoshka 表示学习引入多向量检索的工作，为多模态检索的效率-精度权衡提供了新的调控维度。

### 局限与开放问题

当前方案依赖预训练 VLM 骨干，基座模型在特定领域（如 VQA）的弱点会传递给 METAEMBED；最大预算下的多向量索引内存和计算开销仍显著高于单向量方法；多语言检索能力依赖基座模型的跨语言泛化，缺乏低资源语言验证。此外，MMEB 基准存在 train-test 类别重叠问题（如 ObjectNet 与 ImageNet 共享 113 个类），可能高估模型泛化能力。开放问题包括：Meta 令牌策略能否脱离预训练 VLM 应用、MMR 分组粒度可否自适应优化、以及该方法能否推广至检索下游的生成任务。

多模态检索的核心任务是在大规模候选库中，根据查询（文本、图像或图文组合）找到最相关的候选项。其关键挑战在于如何构建既能保留细粒度语义信息、又能在计算和存储上保持高效的嵌入表示。

### 现有方法的困境

当前主流方法可归为两类，各有明显短板：

**单向量检索**——将查询和候选各自编码为单个稠密向量，通过点积或余弦相似度计算相关性。代表性工作包括 **CLIP**（Radford et al., 2021）、**MagicLens**（Zhang et al., 2024）、**UniIR**（Wei et al., 2024）、**VLM2Vec**（Jiang et al., 2025）及其后续版本 **VLM2Vec-V2**（Meng et al., 2025）、**MoCa**（Chen et al., 2025a）等。这类方法极度高效，但将整个输入压缩为单一向量不可避免地丧失细粒度信息，在需要精确匹配局部细节的场景（如视觉文档检索、视觉定位）中表现受限。

**多向量检索**——为查询和候选各自生成多个向量，通过延迟交互（Late Interaction）计算相似度，即对每个查询向量在所有候选向量上取最大相似度后求和。典型工作如 **ColPali** 和 **ColQwen2**（Faysse et al., 2025）。多向量表示保留了更丰富的语义粒度，但代价高昂：索引存储需求随向量数线性增长，评分延迟也远超单向量方法。更为关键的是，现有方法难以支持查询端和候选端同时包含图像的多模态到多模态检索场景。

### 核心瓶颈

上述困境的实质是**精度与效率之间缺乏动态调节机制**。单向量方法固定于效率一端，多向量方法固定于精度一端，用户无法根据实际部署条件（延迟预算、存储容量）在测试时灵活取舍。理想的多模态检索系统应当提供一种“可伸缩”的表示：在资源充裕时使用更多向量获得更高精度，在资源受限时使用更少向量保持可用效率，且这一调节无需重新训练或重新索引。

### METAEMBED 的动机

针对上述缺口，METAEMBED 提出了一种全新的多向量嵌入范式。其核心思路是：通过少量可学习的 Meta 令牌获取紧凑的多向量表示，并借助 Matryoshka 多向量检索训练（MMR）强制嵌入呈前缀嵌套结构，从而首次在多模态多向量检索中实现测试时“精度-效率”可动态伸缩的能力。用户只需在检索时选择不同的前缀组，即可在毫秒级延迟和百分点级精度之间连续权衡，无需任何模型修改或索引重建。

## 核心方法与创新机理

METAEMBED 的核心创新在于通过两个相互配合的设计，首次在多模态多向量检索中实现了测试时的“精度‑效率”动态伸缩能力。

### 瓶颈定位：单向量与多向量的两难困境

现有的多模态嵌入方法面临一个根本性权衡。单向量方法（如 CLIP、VLM2Vec、MoCa 等）将查询和候选各自压缩为一个固定维度的向量，索引存储和检索延迟极低，但这一压缩过程不可避免地丢失了细粒度的视觉‑语义对应信息。多向量方法（如 ColPali、ColQwen2）通过保留更多的 token 级表示进行延迟交互，能够捕捉更丰富的跨模态对齐信号，但代价是索引内存和检索计算量随向量数线性增长，且难以支持查询端和候选端同时包含图像的多模态到多模态检索场景。METAEMBED 的设计目标正是打破这一僵局：既保持多向量表示的细粒度表达能力，又赋予系统在测试时按需调节计算预算的灵活性。

### 关键控制变量：可学习的 Meta 令牌与嵌套多向量结构

METAEMBED 引入了两个紧密耦合的机制来实现上述目标。

**Meta 令牌嵌入。** 在查询和候选的输入序列末尾，分别追加少量可学习的 Meta 令牌（查询端 $M_q$ 个，候选端 $M_c$ 个）。这些令牌与原始的视觉和文本 token 一同经过 VLM 的 Transformer 编码，其最后一层的隐藏状态被提取出来，经 L2 归一化后构成查询和候选的多向量表示。与直接使用所有 token 隐藏状态的传统多向量方案不同，Meta 令牌的数量是固定且紧凑的（例如查询端 16 个、候选端 64 个），其表示通过自注意力机制上下文感知地聚合了输入序列中的关键信息，从而在压缩率和表达能力之间取得平衡。

**Matryoshka 多向量检索（MMR）。** MMR 借鉴了 Matryoshka 表示学习的思想，将 Meta 嵌入强制组织为前缀嵌套的分组结构。具体而言，预设 $G$ 个递增的分组大小 $1 \leq r_q^{(1)} < \cdots < r_q^{(G)} = R_q$ 和 $1 \leq r_c^{(1)} < \cdots < r_c^{(G)} = R_c$，使得前 $r_q^{(g)}$ 个查询向量和前 $r_c^{(g)}$ 个候选向量构成第 $g$ 组的粗粒度表示，而更大的组则在前一组的基础上追加更多向量以提供更精细的语义。训练时，对所有嵌套组并行计算延迟交互分数和对比损失：

$$s^{(g)}(\mathbf{q}, \mathbf{c}) = \sum_{i=1}^{r_q^{(g)}} \max_{j \in [1, r_c^{(g)}]} \mathbf{E}_{\mathbf{q}}^{(g,i)} \cdot \mathbf{E}_{\mathbf{c}}^{(g,j)}$$

$$\mathcal{L}_{\text{final}} = \sum_{g=1}^{G} w_g \mathcal{L}_{\text{NCE}}^{(g)}$$

这一设计迫使模型学习从粗到细的多向量嵌入，使得前缀向量天然携带最重要的检索信号。在测试时，用户可根据延迟和存储预算直接选择某一前缀组 $(r_q^{(g)}, r_c^{(g)})$ 进行检索，无需重新训练或重新索引。

### 与基线方法的本质差异

| 设计维度 | 单向量基线 | 传统多向量基线 | METAEMBED |
|---------|-----------|--------------|-----------|
| 嵌入构建 | VLM 末层单向量（last-token 或平均池化） | 所有 token 的隐藏状态 | 少量可学习 Meta 令牌的末层隐藏状态 |
| 检索评分 | 单点积或余弦相似度 | 对所有 token 向量做延迟交互 | 对 Meta 嵌入做延迟交互，且可按前缀组选择预算 |
| 测试时可伸缩性 | 固定维度，不可调节 | 向量数固定，不可调节 | 通过 MMR 嵌套组实现预算可选，从单向量到全多向量无缝切换 |

消融实验直接验证了这一差异的价值。在完全相同的训练设置下，去掉 MMR 的 METAEMBED 在最低预算 $(1,1)$ 时退化为单向量检索，其在 ViDoRe v1 上的 NDCG@5 骤降 9.0 个百分点；而启用 MMR 的完整方案在预算 $(16,64)$ 时，相比最优单向量基线（single-last）在 7B 模型上获得 +5.0 的绝对提升，且 MMR 训练本身不损害最大预算下的性能。这表明 MMR 成功地将多向量的表达能力与单向量在低预算下的效率统一在了同一个模型中。

### 证据强度与局限

上述核心创新有充分的实验支撑：MMEB 和 ViDoRe v2 上的 SOTA 结果、跨模型尺寸（3B/7B/11B/32B）的一致性增益、以及 MMR 消融实验均指向 Meta 令牌与嵌套训练的有效性。但需注意，该方法高度依赖预训练 VLM 骨干的质量——当基座模型在某些子任务（如 VQA）上表现不佳时，其弱点会直接传递给 METAEMBED（例如 Llama-3.2-Vision-11B 导致 VQA 得分骤降）。此外，在最大预算下，多向量索引的存储和计算开销仍显著高于单向量方法，这是多向量检索的固有代价，MMR 提供的仅是预算选择权而非根本性的效率突破。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/001_Figure_1.jpg]]
*Figure 1: Upper Left: Single vector retrieval method computes a score for each pair of query and candidate and uses a contrastive objective to maximize the score for corresponding pairs. Upper Right: Multi-vector retrieval aggregates maximum similarities across vector pairs before training. Lower: METAEMBED structures query and candidate vectors into hierarchical nested groups and trains coarse-to-fine multi-vector embeddings that enable scalable and flexible retrieval*

METAEMBED 的核心设计思路是：在查询和候选的输入序列末尾分别追加少量可学习的 **Meta 令牌**，利用视觉语言模型（VLM）的联合编码能力，将这些令牌在最后一层的隐藏状态提取为紧凑的**多向量嵌入**，再通过延迟交互（late interaction）计算相似度。整个框架由五个串联模块构成，形成从输入到检索评分的完整流水线。

**模块一：Meta 令牌追加。** 给定一个查询 $q$ 和一个候选 $c$，METAEMBED 在它们的输入序列后分别附加 $M_q$ 和 $M_c$ 个可学习的 Meta 令牌。这些令牌是随机初始化的嵌入向量，其数量远小于原始输入序列长度，从而将表示压缩为固定大小的多向量集合。

**模块二：VLM 联合编码。** 拼接后的序列 $z^{(0)} = [v; t; M_q; M_c]$ 被送入预训练的视觉语言模型 Transformer。VLM 同时处理视觉和文本模态，通过自注意力机制使 Meta 令牌与原始输入充分交互，获得上下文感知的表示。

**模块三：Meta 嵌入提取。** 从 Transformer 最后一层的隐藏状态中，仅取出 Meta 令牌对应位置的向量，并进行 L2 归一化。这些归一化后的向量即为查询和候选的 **Meta 嵌入**，分别记为 $E_q \in \mathbb{R}^{R_q \times d}$ 和 $E_c \in \mathbb{R}^{R_c \times d}$，其中 $R_q$ 和 $R_c$ 分别为查询端和候选端的 Meta 令牌数量。

**模块四：MMR 分组构建。** 受 Matryoshka 表示学习的启发，METAEMBED 将 Meta 嵌入按前缀嵌套结构组织为 $G$ 个组。具体而言，固定一组递增的组大小 $1 \le r_q^{(1)} < \cdots < r_q^{(G)} = R_q$（候选端同理），使得前 $g$ 个组的向量恰好是第 $g+1$ 组向量的前缀子集。这种嵌套设计使得嵌入具备“由粗到细”的层次化语义：前几个向量构成粗粒度摘要，后续向量逐步补充细节。

**模块五：延迟交互评分与对比损失优化。** 对每个组 $g$，计算查询与候选在该组内的延迟交互分数：

$$s^{(g)}(q, c) = \sum_{i=1}^{r_q^{(g)}} \max_{j \in [1, r_c^{(g)}]} E_q^{(g,i)} \cdot E_c^{(g,j)}$$

即对查询端的每个向量，在所有候选端向量中取最大点积，再求和。训练时，对所有 $G$ 个组并行施加包含批内负样本和硬负样本的 InfoNCE 损失，最终损失为各组损失的加权和：

$$\mathcal{L}_{\text{final}} = \sum_{g=1}^{G} w_g \mathcal{L}_{\text{NCE}}^{(g)}$$

这种并行优化强制模型在所有嵌套层级上同时学习有区分力的表示，使得前缀组在低预算下仍能保持可用的检索质量。

**测试时可伸缩性。** 上述嵌套分组结构的关键价值在于：用户可以在测试时根据延迟和存储预算自由选择使用的组别 $(r_q^{(g)}, r_c^{(g)})$。当预算紧张时，仅使用最小的前缀组（如 $(1,1)$）进行单向量检索；当预算充裕时，使用完整的 $(R_q, R_c)$ 向量集进行精细的多向量延迟交互。这一机制首次在多模态多向量检索中实现了“精度-效率”的动态权衡，无需重新训练或重新索引。

METAEMBED 的核心设计围绕两个关键模块展开：**Meta 令牌嵌入构建** 与 **Matryoshka 多向量检索（MMR）训练**。前者负责生成紧凑的多向量表示，后者赋予这些表示测试时可伸缩的嵌套结构。

### 3.1 基础定义

多模态检索任务中，给定查询 $q$ 和候选集 $\{c_1, \dots, c_N\}$，top‑1 检索结果定义为相似度最大的候选：

$$
\mathbf{c}^{\star} = \operatorname*{argmax}_{\mathbf{c} \in \{\mathbf{c}_1, \hdots, \mathbf{c}_N\}} s(\mathbf{q}, \mathbf{c}) \tag{1}
$$

标准的多向量延迟交互评分机制为：对每个查询向量，在所有文档向量上取最大相似度，然后求和：

$$
\mathbf{LI}(q, d) = \sum_{i=1}^{N_q} \max_{j \in [1, N_d]} \mathbf{E}_q^{(i)} \cdot \mathbf{E}_d^{(j)} \tag{2}
$$

这一机制保留了细粒度的 token 级对齐信息，但传统做法（如 ColPali）直接使用视觉 token 的所有隐藏状态作为多向量，导致索引存储和检索延迟随 token 数线性增长，难以规模化。

### 3.2 Meta 嵌入构建

METAEMBED 的核心创新在于用少量可学习的 **Meta 令牌** 替代大量视觉 token 作为多向量表示的来源。具体流程为：

1. **Meta Token 追加**：在查询和候选的输入序列末尾分别附加 $R_q$ 和 $R_c$ 个可学习的 Meta 令牌 $M_q$ 和 $M_c$。这些令牌不携带任何语义先验，完全通过训练学习如何从上下文中提取信息。
2. **VLM 联合编码**：将视觉 token $v$、文本 token $t$ 与 Meta 令牌拼接后送入 VLM 的 Transformer 处理。
3. **Meta 嵌入提取**：取 Meta 令牌位置的最后隐藏状态，经 L2 归一化后作为查询和候选的多向量嵌入 $\mathbf{E}_q$ 和 $\mathbf{E}_c$。

利用这些 Meta 嵌入，延迟交互评分定义为：

$$
s(\mathbf{q}, \mathbf{c}) = \sum_{i=1}^{R_q} \max_{j \in [1, R_c]} \mathbf{E}_q^{(i)} \cdot \mathbf{E}_c^{(j)} \tag{3}
$$

由于 $R_q$ 和 $R_c$ 远小于视觉 token 数量（例如 16 和 64 vs. 上千个 patch token），Meta 嵌入在保持上下文感知能力的同时，大幅压缩了索引存储和计算开销。

### 3.3 Matryoshka 多向量检索（MMR）

仅靠固定的 Meta 嵌入数量无法实现测试时的预算灵活调节。METAEMBED 引入 MMR 模块，强制 Meta 嵌入形成 **前缀嵌套结构**：前 $r_q^{(1)}$ 个查询向量构成最粗粒度的表示，逐步增加到 $r_q^{(G)} = R_q$ 个向量构成最细粒度的表示，候选侧同理。共设定 $G$ 个嵌套组，满足 $1 \leq r_q^{(1)} < \cdots < r_q^{(G)} = R_q$。

在第 $g$ 组内，延迟交互分数为：

$$
s^{(g)}(\mathbf{q}, \mathbf{c}) = \sum_{i=1}^{r_q^{(g)}} \max_{j \in [1, r_c^{(g)}]} \mathbf{E}_q^{(g,i)} \cdot \mathbf{E}_c^{(g,j)} \tag{4}
$$

训练时，对每个组并行应用 InfoNCE 对比损失。第 $g$ 组的损失包含批内负样本和一个显式硬负样本：

$$
\mathcal{L}_{\mathrm{NCE}}^{(g)} = -\frac{1}{B} \sum_{u=1}^{B} \log \frac{\exp(\mathbf{S}_{u,u}^{(g)})}{\exp(\mathbf{S}_{u,u}^{(g)}) + \sum_{v \neq u} \exp(\mathbf{S}_{u,v}^{(g)}) + \exp(\frac{1}{\tau} s^{(g)}(\mathbf{q}^{(u)}, \mathbf{c}^{(u,-)}))} \tag{6}
$$

其中 $\mathbf{S}_{u,v}^{(g)}$ 为第 $g$ 组下查询 $u$ 与候选 $v$ 的相似度，$\mathbf{c}^{(u,-)}$ 为查询 $u$ 的硬负样本，$\tau$ 为温度系数。

最终训练损失为所有组损失的加权和：

$$
\mathcal{L}_{\mathrm{final}} = \sum_{g=1}^{G} w_g \mathcal{L}_{\mathrm{NCE}}^{(g)} \tag{7}
$$

通过同时优化粗粒度和细粒度组的对比目标，模型学会将最重要的信息压缩在前缀向量中，使得测试时可根据延迟和存储预算自由选择 $(r_q^{(g)}, r_c^{(g)})$ 进行检索——预算越小，使用的向量越少，精度略降但效率显著提升；预算越大，精度越高。

**因果机制总结**：MMR 的多组并行训练迫使 Meta 嵌入形成“由粗到精”的信息排序，这是测试时可伸缩性的根本来源。消融实验证实，去掉 MMR 后，在最低预算 $(1,1)$ 下 ViDoRe v1 的 NDCG@5 骤降 9.0 个百分点，而保留 MMR 时即使只用 1 个向量也能保持可用的检索质量。

## 实验与关键发现

### 主结果：MMEB 与 ViDoRe v2 上的性能

METAEMBED 在两个主流多模态检索基准上全面超越同规模最强基线。在 MMEB 的 36 个任务上，METAEMBED-3B 取得 69.1 的 Overall Precision@1，超过 **MoCa-3B**（Chen et al., 2025a）的 67.5（+1.6 个百分点）；METAEMBED-7B 达到 76.6，显著优于 **MoCa-7B** 的 71.5（+5.1 个百分点）和 **mmE5**（Chen et al., 2025b）的 69.8；METAEMBED-32B 进一步推至 78.7。在 IND 子集上，7B 模型取得 81.8，表明在训练分布内任务上优势更为突出。

在视觉文档检索基准 ViDoRe v2 上，METAEMBED-7B 以 61.3 的平均 NDCG@5 超过多向量基线 **ColQwen2**（Faysse et al., 2025）的 57.5（+3.8 个百分点），且在合成数据、多语言和生物医学子领域均表现强劲。值得注意的是，METAEMBED 未使用多语言数据训练，其跨语言能力完全继承自基座 VLM 的泛化能力，低资源语言上的鲁棒性仍需独立验证。

### 测试时可伸缩性消融

METAEMBED 的核心机制——通过选择不同前缀组实现测试时检索预算的动态调节——在所有模型尺寸上均表现出一致的正向伸缩性（Figure 3）。将检索预算从 (1,1) 增至 (16,64) 时：3B 模型相对单向量方法获得 +3.3 个百分点的增益，7B 模型获得 +5.0 个百分点，而 32B 模型增益最大，达 +6.6 个百分点。这表明更大容量的 VLM 骨干能更充分地利用多向量表示中的细粒度信息。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/005_Figure_3.jpg]]
*Figure 3: Impact of retrieval budget on MMEB across METAEMBED of varying model sizes. Retrieval budget is denoted as ( r _ { q } , r _ { c } ) , i.e. a tuple of the number of Meta Embeddings used on query and candidate side. Increasing the retrieval budget from (1,1) to (16,64) consistently improves performance for all model sizes, with larger gains observed in higher-capacity models. The dashed green lines indicate the best single-vector retrieval performance and red arrows indicate the absolute gain (in percentage points) between METAEMBED and single-vector retrieval*

Figure 4(a) 进一步揭示了模型扩展中的收益递减特征：METAEMBED 在 (16,64) 预算下从 3B 到 7B 的增益为 +7.5，从 7B 到 32B 的增益收窄至 +2.1，但仍未出现饱和迹象。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/007_Figure_4.jpg]]
*Figure 4: (b) Average NDCG@5 (%) on Vi-DoRe v1 benchmark with varying retrieval budgets on METAEMBED-3B with and without MMR design. Figure 4: Ablation studies*

### MMR 设计的决定性作用

消融实验直接验证了 Matryoshka 多向量检索训练的必要性（Figure 4b）。在 ViDoRe v1 上，当禁用 MMR 训练（即 NoMMR）并将预算设为 (1,1) 时，METAEMBED-3B 的 NDCG@5 骤降 9.0 个百分点——此时模型退化为单向量检索，丧失了多向量表示的全部优势。而在高预算 (16,64) 下，MMR 训练仍保持微小但一致的优势，说明嵌套组训练不仅不损害最大预算下的性能，反而通过粗到细的表示学习提供了额外的正则化收益。

Table 5 的对照实验进一步确认：在完全相同训练设置下，METAEMBED (16,64) 相较最优单向量基线 single-last 在 7B 上获得 +5.0 的绝对提升，且该优势在 3B 和 11B 上均可复现。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/010_Table_5.jpg]]
*Table 5: Comparison between METAEMBED and single-vector & multi-vector retrieval models trained with identical settings. NoMMR indicates Matryoshka Multi-Vector Retrieval (MMR) is disabled. ∆ denotes the difference to the best single-vector retrieval method, i.e. single-last*

### 效率分析：延迟与存储的权衡

Table 3 报告了 METAEMBED-7B 在 A100 GPU 上处理 10 万候选时的效率剖面。评分延迟在中等预算范围内几乎持平：(1,1) 为 1.67 ms，(8,16) 仅增至 1.92 ms，这得益于延迟交互的并行化特性。真正的瓶颈在于查询编码——处理 1024 个 token 的图像查询需要 42.72 TFLOPS 和 788 ms，该开销与检索预算无关。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/008_Table_3.jpg]]
*Table 3: Efficiency analysis of METAEMBED-7B with different retrieval budgets on an A100 GPU with 100,000 candidates per query with scoring batch size of 1,000. Query encoding and index generation latency are omitted because they remain the same for all variants. Latency refers specifically to scoring latency and mean and standard deviation of latency are reported with 10 runs. Index is stored and compared with bfloat16 precision (Wang & Kanwar, 2019)*

索引内存随预算线性增长：从 (1,1) 的 0.68 GiB 到 (16,64) 的 42.72 GiB。这构成了测试时可伸缩性的核心权衡：用户可根据存储约束选择候选侧向量数，在精度与内存之间灵活折中。需注意，文中延迟数据基于未优化的 PyTorch 实现，若采用 FAISS 或 WARP 等专用检索加速库，实际延迟可进一步降低，当前数据应视为保守上界。

### 架构鲁棒性与失败模式

METAEMBED 在 Qwen2.5-VL、PaliGemma 和 Llama-3.2-Vision 三种不同 VLM 骨干上均展现出有效性，表明 Meta Token 策略具有架构无关的通用性。但该方法对基座模型存在强依赖：当使用 Llama-3.2-Vision-11B 时，METAEMBED-11B 在 VQA 子任务上得分骤降，原因是该基座模型本身在视觉问答能力上较弱，其缺陷直接传递至下游检索任务。

此外，MMEB 基准的 IND/OOD 划分存在已知缺陷——ObjectNet 与 ImageNet 共享 113 个类别，导致 train-test 类别重叠，可能高估模型的泛化能力。因此，METAEMBED 报告的 OOD 指标应谨慎解读，更严格的跨域评估仍有待开展。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_yKDqg9HwZX/figures/004_Table_2.jpg]]
*Table 2: NDCG@5 (%) results on the ViDoRe v2 benchmark, which covers 7 tasks on visual document retrieval. “Syn” denotes synthetic data, “Mul” indicates multilingual tasks, and “Bio” refers to biomedical domains*

## 定位与知识库关联

### 1. 问题定位：多模态检索的效率-精度困境

METAEMBED 切入的瓶颈是现有多模态嵌入方法在**表示紧凑性**与**细粒度语义保持**之间的根本冲突。单向量检索方法（如 CLIP、VLM2Vec、mmE5 等）将查询和候选压缩为单个向量，通过点积或余弦相似度快速匹配，但这一压缩过程不可避免地丢失了局部语义信息。多向量检索方法（如 ColPali、ColQwen2）保留更多的 token 级表示，通过延迟交互（late interaction）在评分阶段恢复细粒度对齐，但其代价是候选索引的存储和检索延迟随向量数线性增长。更关键的是，现有方法均无法在测试时动态调节这一权衡：一旦模型训练完成，嵌入维度和向量数就固定下来，用户无法根据实际延迟或存储预算调整检索粒度。

METAEMBED 的核心因果调节旋钮是：**在输入序列中附加少量可学习的 Meta 令牌，并强制其最后隐藏状态形成前缀嵌套的多向量表示**。这一设计使得模型第一次在多模态多向量检索中实现了测试时的“精度-效率”可伸缩能力。

### 2. 与单向量检索基线的关系

METAEMBED 在嵌入构建方式上与单向量检索方法形成根本差异。传统方法从 VLM 最后一层隐藏状态中提取单个向量——或取最后一个 token 的表示（如 VLM2Vec, Jiang et al., 2025），或对所有 token 做平均池化——然后直接用于点积评分。METAEMBED 则引入 $M_q$ 个查询端 Meta 令牌和 $M_c$ 个候选端 Meta 令牌，将其最后隐藏状态作为一组上下文感知的多向量嵌入。这一改动本质上是将“压缩”操作从训练后的池化步骤转移到了 VLM 内部的注意力机制中：Meta 令牌通过交叉注意力从视觉和文本 token 中自适应地聚合信息，形成一组紧凑但表达力更强的表示。

在检索评分机制上，METAEMBED 用多向量延迟交互替代了单点积：

$$s(\mathbf{q}, \mathbf{c}) = \sum_{i=1}^{R_q} \max_{j \in [1, R_c]} \mathbf{E}_{\mathbf{q}}^{(i)} \cdot \mathbf{E}_{\mathbf{c}}^{(j)}$$

这一评分函数允许查询的每个向量独立地在候选的所有向量中寻找最佳匹配，从而捕获单向量方法无法建模的局部对应关系。

在 MMEB 基准上，METAEMBED-7B 以 76.6 的 Overall Precision@1 显著超越同期最强单向量基线 MoCa-7B（71.5, Chen et al., 2025a）和 mmE5（69.8, Chen et al., 2025b），提升幅度达 5-7 个百分点。即便在 3B 规模下，METAEMBED-3B（69.1）也超越了 MoCa-3B（67.5）。

### 3. 与多向量检索基线的关系

与 ColPali 和 ColQwen2（Faysse et al., 2025）等现有多向量检索方法相比，METAEMBED 的关键差异在于**向量的来源和结构化方式**。ColPali 系列直接使用 VLM 输出的视觉 token 嵌入作为多向量表示，向量数与输入图像 patch 数成正比（通常数百个），导致候选索引的存储开销极大。METAEMBED 则通过固定数量的可学习 Meta 令牌将表示压缩为少量向量（如候选端 64 个），在保持延迟交互优势的同时大幅降低索引成本。

在 ViDoRe v2 视觉文档检索基准上，METAEMBED-7B 以 61.3 的平均 NDCG@5 超越 ColQwen2（57.5），提升 3.8 个百分点。值得注意的是，METAEMBED 在多语言和生物医学子任务上表现尤为突出，尽管其训练数据中未包含多语言样本——这一跨语言能力源于基座 VLM（Qwen2.5-VL）的预训练泛化能力，而非方法本身的显式设计。

### 4. 方法谱系中的独特贡献：测试时可伸缩性

METAEMBED 最独特的贡献在于引入了 **Matryoshka 多向量检索（MMR）** 训练范式。受 Matryoshka 表示学习（Kusupati et al., 2022）启发，MMR 将 Meta 嵌入组织为前缀嵌套的 $G$ 个组，固定组大小使得 $1 \leq r_q^{(1)} < \cdots < r_q^{(G)} = R_q$，并对所有组并行应用对比损失：

$$\mathcal{L}_{\text{final}} = \sum_{g=1}^{G} w_g \mathcal{L}_{\text{NCE}}^{(g)}$$

这一设计强制模型学习“从粗到细”的表示层次：前几个向量构成粗粒度摘要，后续向量逐步补充细节。在测试时，用户可根据延迟约束选择不同的前缀组 $(r_q^{(g)}, r_c^{(g)})$ 进行检索，无需重新训练或重新索引。

消融实验证实了这一设计的因果效应：去掉 MMR 训练后，在最低预算 (1,1) 下（即退化为单向量检索），ViDoRe v1 的 NDCG@5 急剧下降 9.0 个百分点；而在最大预算 (16,64) 下，MMR 仍保持微小优势，表明嵌套训练不仅没有损害高预算下的性能，反而带来了正向正则化效果。

### 5. 适用边界与局限

**依赖预训练 VLM 骨干。** METAEMBED 的性能上限受基座 VLM 能力的强约束。例如，Llama-3.2-Vision-11B 在视觉问答（VQA）任务上的固有弱点会直接传递给 METAEMBED-11B，导致其 VQA 子指标骤降。这意味着方法本身无法弥补基座模型在特定领域的缺陷。

**多向量索引的存储开销。** 尽管 MMR 提供了灵活的存储-精度权衡，但在最大预算 (16,64) 下，7B 模型的候选索引内存达到 42.72 GiB（100,000 候选，bfloat16 精度），仍显著高于单向量方法的 0.68 GiB。对于大规模生产系统，这一开销可能成为部署瓶颈。

**多语言能力的非显式性。** METAEMBED 的多语言检索性能依赖于基座 VLM 的跨语言泛化能力，而非显式的多语言训练数据。在低资源语言上的鲁棒性缺乏系统验证，这在实际多语言场景中构成风险。

**基准评估的潜在高估。** MMEB 基准的 IND/OOD 划分存在 train-test 类别重叠问题（如 ObjectNet 与 ImageNet 共享 113 个类），可能高估模型的泛化能力。这一局限性在原始基准设计中已存在，影响所有在该基准上评估的方法。

**效率分析的保守性。** 文中报告的检索延迟基于未优化的 PyTorch 实现，未使用专用检索加速库（如 FAISS、WARP）。实际部署中，经过专用库优化后的延迟可能显著低于报告值，因此当前数据应视为保守上界。

### 6. 开放问题

1. **Meta 令牌策略能否脱离预训练 VLM？** 当前设计强依赖 VLM 的联合编码能力。若将其应用于纯文本或单模态检索场景，或使用未预训练的 Transformer 骨干，Meta 令牌是否仍能学习有效的上下文聚合，尚待验证。

2. **MMR 分组粒度可否自适应？** 当前分组大小是预先固定的超参数。是否可以根据任务域或数据特性自适应地优化分组粒度，从而在给定总预算下最大化检索效率？

3. **在更大规模模型上的扩展极限。** 实验显示从 3B 到 32B，METAEMBED 的收益递减现象弱于单向量方法，但 32B 以上的扩展行为（如 70B+ 规模）仍是未知的。

4. **检索下游任务的泛化。** METAEMBED 目前专注于检索排序任务。其多向量表示能否推广至多模态问答、生成等检索增强的下游任务，而不仅仅是作为检索器使用？

5. **训练数据覆盖的公平性。** 方法在多语言、多领域场景中的优势部分源于基座模型的预训练数据。若基座模型在特定语言或领域上的预训练覆盖不足，METAEMBED 可能放大而非缓解这些偏差。

## 原文 PDF

![[paperPDFs/ICLR_2026/MetaEmbed_Scaling_Multimodal_Retrieval_at_Test_Time_with_Flexible_Late_Interaction.pdf]]
