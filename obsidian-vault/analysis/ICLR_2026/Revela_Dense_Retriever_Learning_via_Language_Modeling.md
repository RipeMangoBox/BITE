---
title: "Revela: Dense Retriever Learning via Language Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Revela_Dense_Retriever_Learning_via_Language_Modeling.pdf
openreview_forum_id: e7pAjJZJWb
aliases:
- Revela
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将语言模型的自监督下一个token预测目标与批次内交叉文档注意力相结合，利用检索器计算的相似度作为注意力权重，使得检索器能够通过语言模型的梯度信号进行端到端优化。"
primary_logic: "语言模型中的下一个token预测隐式地捕捉文本内部的依赖关系；通过将其扩展到跨文档的批次内注意力，可以建模文本块之间的宏观相关关系，从而无需显式查询-文档对即可训练检索器。"
claims:
- "在CoIR基准上，自监督的Revela（3B参数）超越了有监督的7B参数模型E5-Mistral-7B-Instruct，平均nDCG@10提升2.8个百分点。"
- "在复杂推理BRIGHT基准上，Revela3B表现优于有监督模型E5-Mistral以及多个专有嵌入API。"
- "在BEIR基准上，Revela3B以约1/1000的训练数据和1/10的算力达到了与弱监督E5-PT相似的性能，展现了极高的数据效率。"
- "在相同LM骨干和训练数据的受控实验中，Revela在BEIR和CoIR上均优于基于对比学习的Contriever，且在域外任务上优势更显著。"
---

# Revela: Dense Retriever Learning via Language Modeling

> [!tip] 核心洞察
> 语言模型中的下一个token预测隐式地捕捉文本内部的依赖关系；通过将其扩展到跨文档的批次内注意力，可以建模文本块之间的宏观相关关系，从而无需显式查询-文档对即可训练检索器。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Revela：通过语言建模进行密集检索器学习 |
| 英文题名 | Revela: Dense Retriever Learning via Language Modeling |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=e7pAjJZJWb); [GitHub](https://github.com/TRUMANCFY/Revela); [Project](https://huggingface.co/trumancai/Revela-3b) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Revela |
| Dataset | CoIR, BRIGHT, BEIR |

> [!tip] 效果简介
> - CoIR 上，nDCG@10 为 60.1 (Revela3B)，对比 57.3 (E5-Mistral-7B-Instruct)，变化 +2.8。
> - CoIR 上，nDCG@10 为 56.1 (Revela0.5B)，对比 46.4 (E5-PT 0.3B)，变化 +9.7。
> - BRIGHT 上，nDCG@10 为 20.1 (Revela3B)，对比 13.1 (E5-PT)，变化 +7.0。

## 概述

密集检索器（Dense Retriever）是现代信息检索系统的核心组件，但其训练通常依赖大量人工标注的查询-文档对——这一瓶颈在代码、法律等专业领域以及需要复杂推理的场景中尤为突出，严重限制了检索技术的可扩展性和普及度。

Revela 提出了一种全新的自监督训练范式：**通过语言建模来训练密集检索器**。其核心洞察在于，语言模型中的下一个token预测（Next-Token Prediction, NTP）天然捕捉了文本内部的依赖关系；通过将这种依赖关系扩展到跨文档的批次内注意力，可以建模文本块之间的宏观语义关联，从而完全摆脱对显式查询-文档对的依赖。

具体而言，Revela 在 Transformer 架构中引入**批次内注意力机制（In-Batch Attention）**，允许每个文档在语言建模过程中关注同一批次内的其他文档，并以检索器计算的文档间相似度作为注意力权重。检索器的参数因此通过语言模型的梯度信号进行端到端优化，实现了检索器与语言模型的联合训练。

实验结果表明，Revela 在多个基准上展现出显著的性能优势与极高的数据效率：

- **超越有监督模型**：在代码检索基准 CoIR 上，仅 3B 参数的 Revela 以 60.1% 的 nDCG@10 超越了 7B 参数的有监督模型 E5-Mistral-7B-Instruct（57.3%），提升 2.8 个百分点；在复杂推理基准 BRIGHT 上，Revela3B 同样优于 E5-Mistral 及多个专有嵌入 API。
- **极高的数据效率**：在通用检索基准 BEIR 上，Revela3B 以约 **1/1000 的训练数据量和 1/10 的算力**达到了与弱监督模型 E5-PT 持平的性能（nDCG@10 均为 45.6%）。
- **优于同类自监督方法**：在受控实验中，使用相同骨干网络和训练数据，Revela 在 BEIR 和 CoIR 上均优于基于对比学习的 Contriever，且在域外任务上优势更加显著。
- **良好的可扩展性**：Revela 的性能随模型规模、批次大小和语言模型规模的增加而稳定提升。

在方法谱系上，Revela 位于自监督检索器训练的前沿，与 **REPLUG**（Shi et al., 2024）利用冻结语言模型困惑度进行蒸馏、**Contriever**（Izacard et al., 2022）通过对比学习生成伪查询-文档对等方案形成鲜明对比。Revela 的创新在于将检索器训练与语言建模目标统一，使检索器成为语言模型跨文档推理的有机组成部分，而非独立优化的外部模块。

## 背景与动机

密集检索器在开放域问答、代码搜索、法律信息检索等场景中已成为核心组件。然而，训练高性能密集检索器通常依赖大量人工标注的查询-文档对，这在专业领域（如代码、法律）以及需要复杂推理的场景中成本高昂且难以扩展。现有的自监督方法试图绕过这一瓶颈，但各有局限：**Contriever**（Izacard et al., 2022）通过对比学习利用文档内部结构生成伪查询-文档对，其性能在域外场景下衰减明显；**REPLUG**（Shi et al., 2024）使用冻结语言模型的困惑度作为跨文档相似度监督信号，但检索器不参与语言模型训练，梯度信号间接且稀疏；**E5-PT**（Wang et al., 2022）虽性能强劲，却依赖数百万弱监督文本对和大量计算资源。

上述方法的共同缺陷在于：检索器的优化目标与语言模型的语义理解能力相互割裂。语言模型中的下一个token预测（Next-Token Prediction, NTP）隐式地捕捉文本内部的依赖关系，但这种能力从未被直接用于建模文本块之间的宏观相关关系。

Revela的动机正源于此：**能否将语言模型的自监督NTP目标转化为检索器的训练信号？** 核心洞察是，如果将NTP的上下文从单个序列内部扩展到同一批次中的其他文档，并让检索器计算的相似度来决定跨文档注意力的权重，那么检索器就可以通过语言模型的梯度信号进行端到端优化——无需任何显式查询-文档对。这一思路将检索器训练从“构造伪监督信号”的范式转变为“让检索器参与语言建模”的范式，从根本上解耦了对标注数据的依赖。

## 核心创新

Revela的核心创新在于将密集检索器的训练完全融入语言模型的自监督下一个token预测（Next-Token Prediction, NTP）框架中，从而彻底摆脱了对标注查询-文档对的依赖。其关键改变体现在以下四个维度：

### 训练目标：从对比学习到条件语言建模

传统自监督检索器（如**Contriever** (Izacard et al., 2022)）依赖对比学习损失，通过文档内部的随机裁剪或逆完形填空任务构造伪查询-文档对进行训练；**REPLUG** (Shi et al., 2024)则利用冻结语言模型的困惑度作为跨文档相似度的蒸馏信号。Revela直接采用语言模型的原生NTP目标，但将其条件化范围从单个序列的前缀扩展至批次内的所有其他文档：

$$P _ { R } ( x _ { l } ^ { i } ) = P _ { \Phi , \Theta } ( x _ { l } ^ { i } \mid x _ { < l } ^ { i } , \{ D _ { j } \} _ { j \neq i } )$$

其中 $\Phi$ 为语言模型参数，$\Theta$ 为检索器参数。这一公式化的改变使得检索器能够通过LM损失的梯度直接优化，而非依赖外部构造的监督信号。

### 注意力机制：引入批次内交叉文档注意力

Revela在标准Transformer块中增加了一个批次内注意力（In-Batch Attention）机制，使每个序列不仅能关注自身的因果上下文，还能关注同一批次中的其他文档。具体实现中，该机制将标准自注意力与交叉文档注意力结合——后者利用缓存的自注意力键值对 $K_j^e$ 和 $V_j^e$ 计算跨文档注意力输出 $\mathrm{b}_{ij}^l$，并通过检索器计算的相似度进行加权聚合：

$$\mathrm { b } _ { i } ^ { l } = \sum _ { j = 1 , j \ne i } ^ { B } \mathrm { S i m } ( D _ { i } , D _ { j } ) \mathrm { b } _ { i j } ^ { l }$$

其中 $\mathrm{Sim}(D_i, D_j)$ 由检索器编码的文档向量经余弦相似度和温度缩放softmax得到：

$$\mathrm { S i m } ( D _ { i } , D _ { j } ) = \frac { \exp ( S _ { i j } / \tau ) } { \sum _ { k \ne i } \exp ( S _ { i k } / \tau ) }$$

### 检索器优化：通过LM梯度端到端更新

在Revela中，检索器和语言模型是联合训练的。检索器计算的文档相似度直接调制批次内注意力权重，因此语言模型的NTP损失可以通过交叉文档注意力的计算图反向传播至检索器参数。这与REPLUG中检索器独立训练、LM冻结的范式形成根本区别——Revela的检索器不再是被动接收蒸馏信号，而是主动参与语言建模过程并从中学习文档间的相关性表征。

### 训练数据：仅需原始文本块

Revela的训练数据构建极为简洁：将原始文本按文档切分成块，并将同一文档内的不同块放入同一批次。这一策略的动机源于对比学习中的难负样本思想——同一文档的块具有天然的语义关联性，为批次内注意力提供了有意义的跨文档依赖。整个过程无需构造任何显式的查询-文档对，也无需依赖半结构化文本对（如E5-PT使用的标题-正文对），仅需领域相关的原始语料即可启动训练。

### 因果机制总结

Revela的核心因果链条可概括为：**语言模型的NTP目标隐式捕捉文本内部依赖 → 通过批次内注意力将这种依赖扩展至跨文档的宏观关系 → 检索器计算的相似度作为注意力权重，将文档相关性信息注入语言建模过程 → NTP损失的梯度反向传播至检索器，驱动其学习有效的文档表征**。这一设计使得检索器训练与语言建模形成了闭环，无需任何外部标注信号。

## 整体框架

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/001_Figure_1.jpg]]
*Figure 1: The framework of Revela. The retriever’s in-batch similarity scores are used as in-batch attention weights inside transformer blocks. The retriever is trained by optimizing the language modeling objective, i.e., NTP. The related patterns in red and purple sequences are highlighted in bold and underline. An example of training dynamics is illustrated at App. A*

Revela 提出了一种自监督的密集检索器训练框架，其核心创新在于将检索器的优化过程与语言模型（LM）的下一个 token 预测（NTP）目标深度耦合，从而完全摆脱对人工标注查询-文档对的依赖。

### 核心思想与因果机制

传统语言模型的 NTP 目标仅建模单个序列内部的 token 依赖关系。Revela 的关键洞察在于：NTP 隐式地捕捉了文本内部的微观依赖，如果将其扩展到跨文档的批次内注意力，就可以建模文本块之间的宏观相关关系。这一扩展使得语言模型自身的梯度信号能够直接用于优化检索器，无需任何显式的相关性标注。

### 整体数据流与模块关系

Revela 的框架由三个核心模块构成，形成闭环训练流程（参见 Figure 1）：

1. **检索器编码器（Retriever Encoder）**：采用 LLaMA 系列模型作为骨干网络，将输入文档编码为向量表示。具体而言，在每个序列末尾添加 `<eos>` token，取其对应的嵌入作为整篇文档的句向量，并通过余弦相似度计算批次内所有文档对之间的相似度矩阵。

2. **批次内交叉注意力机制（In-Batch Cross-Document Attention）**：在 Transformer 的每一层中，Revela 在标准因果自注意力之外增加了一个跨文档注意力模块。该模块允许当前序列关注同一批次中的其他文档，利用缓存的自注意力键值对计算跨文档注意力输出。

3. **语言模型与联合训练**：检索器计算的相似度经过温度缩放 softmax 转换为概率权重，用于对批次内其他文档的交叉注意力输出进行加权聚合。聚合后的跨文档上下文与标准自注意力输出融合，最终影响语言模型的 NTP 预测。检索器的参数通过 LM 损失的梯度进行端到端优化，因为其相似度直接决定了跨文档注意力的权重分布。

### 关键公式

Revela 将传统 NTP 目标从仅依赖序列前缀扩展为同时条件化于批次内所有其他文档：

- **传统 NTP**：$P(x_l^i) = P_{\Phi}(x_l^i \mid x_{<l}^i)$
- **Revela NTP**：$P_R(x_l^i) = P_{\Phi,\Theta}(x_l^i \mid x_{<l}^i, \{D_j\}_{j \neq i})$

其中 $\Phi$ 为语言模型参数，$\Theta$ 为检索器参数，$\{D_j\}_{j \neq i}$ 表示批次中除当前文档外的所有其他文档。

跨文档注意力的聚合方式为：

$$\text{Sim}(D_i, D_j) = \frac{\exp(S_{ij} / \tau)}{\sum_{k \ne i} \exp(S_{ik} / \tau)}$$

$$\mathrm{b}_i^l = \sum_{j=1, j \ne i}^{B} \text{Sim}(D_i, D_j) \mathrm{b}_{ij}^l$$

其中 $S_{ij}$ 为检索器计算的文档 $i$ 与 $j$ 的余弦相似度，$\tau$ 为温度参数（训练中设为 $10^{-4}$），$\mathrm{b}_{ij}^l$ 为文档 $i$ 对文档 $j$ 在第 $l$ 层的交叉注意力输出，$B$ 为批次大小。

### 训练数据构建

Revela 仅需原始文本作为训练数据。具体做法是将文档切分成块，并将同一文档内的不同块放入同一个训练批次中。这一策略借鉴了对比学习中困难负样本的思想——同一文档内的不同块通常具有较高的语义相关性，迫使检索器学习更精细的相似度区分能力。训练时文档被截断为 160 个 token，使用 bf16 混合精度在 4 块 A100 80GB GPU 上进行，检索器和语言模型均采用秩为 256 的 LoRA 进行参数高效微调。

### 与基线方法的根本差异

相较于传统方法，Revela 在三个关键维度上实现了范式转变：

- **对比学习基线（Contriever）**：需要构造伪查询-文档对，通过独立的对比损失训练检索器，检索器不参与语言模型训练。Revela 则让检索器直接参与 LM 的 NTP 训练，利用 LM 的梯度信号优化。
- **困惑度蒸馏基线（REPLUG）**：使用冻结语言模型的困惑度作为跨文档相似度的监督信号，检索器训练与 LM 训练分离。Revela 则实现检索器与 LM 的联合更新。
- **有监督/弱监督基线（E5 系列）**：依赖大规模标注查询-文档对或半结构化文本对进行训练。Revela 完全消除了对配对数据的依赖，仅使用原始文本即可达到甚至超越其性能。

## 核心模块与公式推导

### 3.1 训练目标的范式转换

Revela的核心创新在于将密集检索器的训练目标从传统的对比学习或蒸馏范式，彻底转换为语言模型的下一个token预测（Next-Token Prediction, NTP）目标。这一转换的数学基础体现在对条件概率建模范围的扩展上。

传统的语言建模中，序列 $i$ 中位置 $l$ 的token $x_l^i$ 的概率仅依赖于其自身的前缀上下文：

$$P(x_l^i) = P_{\Phi}(x_l^i \mid x_{<l}^i)$$

其中 $\Phi$ 表示语言模型的参数。这一范式将每个文档视为独立的生成单元，文档之间不存在信息交互。

Revela对这一公式进行了根本性的扩展——将NTP的条件概率从单文档前缀扩展为“自身前缀 + 批次内所有其他文档”的联合条件：

$$P_R(x_l^i) = P_{\Phi, \Theta}(x_l^i \mid x_{<l}^i, \{D_j\}_{j \neq i})$$

此处 $\Theta$ 为检索器参数，$\{D_j\}_{j \neq i}$ 表示训练批次中除当前文档 $D_i$ 外的所有其他文档。这一扩展的深层含义在于：**token的生成不仅受其局部上下文约束，还受批次内其他文档的全局语义关联所调制**。检索器 $\Theta$ 的作用正是量化这种跨文档的关联强度，从而将检索信号嵌入到语言建模的梯度流中。

### 3.2 批次内注意力机制

为实现上述扩展的概率建模，Revela在标准Transformer块中引入了一个额外的**批次内注意力（In-Batch Attention）**机制。该机制与原有的因果自注意力并行运作，共同构成每一层的表示更新。

**标准自注意力路径**。对于文档 $D_i$ 在第 $l$ 层的输入表示 $\mathrm{e}_i^{l-1}$，首先通过线性投影获得查询、键、值：

$$Q_i^e = \mathrm{e}_i^{l-1} W^Q, \quad K_i^e = \mathrm{e}_i^{l-1} W^K, \quad V_i^e = \mathrm{e}_i^{l-1} W^V$$

随后执行标准的因果自注意力计算，得到该文档自身的上下文表示 $\mathrm{e}_i^l$：

$$\mathrm{e}_i^l = \mathrm{softmax}\left(\frac{Q_i^e K_i^{e\top}}{\sqrt{d_H}}\right) V_i^e$$

**跨文档注意力路径**。批次内注意力的关键在于**跨文档注意力（Cross-Document Attention）**——它使文档 $D_i$ 能够关注批次中其他文档 $D_j$ 的表示。具体而言，利用其他文档在自注意力路径中缓存的键 $K_j^e$ 和值 $V_j^e$，计算文档 $D_i$ 对文档 $D_j$ 的跨文档注意力输出 $\mathrm{b}_{ij}^l$。

**相似度加权聚合**。跨文档注意力输出的聚合并非简单平均，而是由检索器计算的文档间语义相似度作为权重进行加权。对于文档对 $(D_i, D_j)$，检索器首先将其编码为向量并计算余弦相似度，再通过温度参数 $\tau$ 缩放的softmax转换为概率权重：

$$\mathrm{Sim}(D_i, D_j) = \frac{\exp(S_{ij} / \tau)}{\sum_{k \neq i} \exp(S_{ik} / \tau)}$$

其中 $S_{ij}$ 为文档 $D_i$ 与 $D_j$ 嵌入向量之间的余弦相似度。利用该权重对所有其他文档的跨文档注意力输出进行加权求和，得到文档 $D_i$ 的聚合跨文档上下文表示：

$$\mathrm{b}_i^l = \sum_{j=1, j \neq i}^{B} \mathrm{Sim}(D_i, D_j) \, \mathrm{b}_{ij}^l$$

### 3.3 联合优化的梯度传导

Revela框架的关键工程特性在于**检索器与语言模型的端到端联合训练**。检索器参数 $\Theta$ 的梯度并非来自独立的对比损失或蒸馏信号，而是直接源于语言模型的NTP损失。

梯度传导的因果链如下：检索器计算的相似度 $\mathrm{Sim}(D_i, D_j)$ 直接决定了跨文档注意力聚合的权重 $\mathrm{b}_i^l$；该聚合表示随后融入当前层的输出，逐层向上传播直至影响最终的token预测概率 $P_R(x_l^i)$；NTP损失对该预测的梯度沿计算图反向传播，经跨文档注意力路径回传至检索器的编码参数。这一设计使得检索器能够在语言建模的过程中自然地学习到哪些文档之间的语义关联有助于提升token预测的准确性——这本质上等价于学习文档之间的检索相关性。

### 3.4 架构实现要点

在具体实现层面，批次内注意力的计算通过**文档复制与注意力掩码调整**来高效完成。具体而言，将批次内的文档复制一份，其中一份用于标准自注意力的计算（产生 $\mathrm{e}_i^l$），另一份用于跨文档注意力的计算（产生 $\mathrm{b}_i^l$），并通过精心设计的注意力掩码确保：自注意力路径仅关注文档内部的前缀token，跨文档注意力路径仅关注其他文档的全部token，二者互不干扰。这种实现方式使得Revela可以直接复用现有Transformer架构的注意力算子，降低了工程集成的复杂度。

## 实验与分析

### 核心发现

Revela在三个性质迥异的基准上验证了其有效性：领域专用的代码检索基准CoIR、需要复杂推理的BRIGHT基准，以及通用检索基准BEIR。核心发现是：**自监督的Revela在多个场景下超越了规模更大的有监督模型，同时展现出极高的数据效率**。

在CoIR基准上，Revela3B（3B参数）的平均nDCG@10达到60.1%，超越了有监督的7B参数模型**E5-Mistral-7B-Instruct**（57.3%），提升2.8个百分点（Table 1）。值得注意的是，Revela的训练完全不需要查询-文档对，而E5-Mistral依赖大规模指令微调数据。在相似规模下，Revela0.5B（56.1%）比弱监督的**E5-PT**（46.4%）高出9.7个百分点，显示出方法本身的有效性而非单纯依赖模型规模。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/003_Table_1.jpg]]
*Table 1: Performance on CoIR (nDCG@10, %). Gray indicates supervised models. Bold marks the highest score among non-API models in each row. Columns marked † used code-related pairs during pre-training. The results of APIs are collected from Li et al. (2025). Without query-document pairs, Revela3B surpasses larger supervised models and proprietary APIs, averaged across 10 tasks*

在BRIGHT复杂推理基准上，Revela3B的nDCG@10达到20.1%，显著超过E5-PT的13.1%（+7.0个百分点），并超越了多个专有嵌入API（Figure 3左，Table 8）。这表明语言建模目标隐式捕捉的跨文档依赖关系能够有效迁移到需要深层语义理解的检索任务中。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/004_Figure_3.jpg]]
*Figure 3: Performance on BRIGHT (left) and BEIR (right) (nDCG@10, %). Results for Revela are shown in opaque bars, while all other models are represented by transparent bars. On BRIGHT, Revela3B surpasses E5-Mistral, a supervised retriever with more parameters, and properties APIs. On BEIR, Revela achieves similar performance with E5-PT with much less data and compute. Please refer to Tab. 7 and Tab. 8 in App. B.6 for the per-task results*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/014_Table_8.jpg]]
*Table 8: Performance on BRIGHT (nDCG@10, %). Bold marks the best performance. The results of BM25, E5-Mistral and APIs are taken from BRIGHT (Hongjin et al., 2025)*

在BEIR通用基准上，Revela3B的nDCG@10为45.6%，与E5-PT持平，但**训练数据量减少约1000倍，计算量减少约10倍**（Figure 3右，Table 7）。这一数据效率优势源于Revela无需构造伪查询-文档对，仅利用原始文本的语言建模信号即可学习有效的文档表示。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/013_Table_7.jpg]]
*Table 7: Performance of unsupervised/self-supervised retriever models on BEIR datasets (nDCG@10, %). Bold marks the best score per dataset among unsupervised methods*

### 与Contriever的受控对比

在相同LM骨干（LLaMA-3.2-1B）和相同训练数据的严格受控实验中，Revela在BEIR和CoIR上均优于经典的对比学习自监督方法**Contriever**（Izacard et al., 2022）（Table 2）。具体而言：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/005_Table_2.jpg]]
*Table 2: Revela vs. Contriever Performance*

- 使用Wikipedia数据训练时，Revela-wiki1B在BEIR上达到42.7%（Contriever-wiki1B为42.4%），在CoIR上达到53.2%（Contriever为50.3%）。
- 使用代码语料训练时，差距进一步拉大：Revela-code1B在BEIR上为39.6%，而Contriever-code1B仅为32.3%。

**关键洞察**：在域外数据上的性能差距更为显著，说明Revela的语言建模范式比对比学习的伪查询构造策略具有更强的泛化能力。对比学习依赖文档内部结构生成伪正例，而语言建模通过批次内交叉注意力直接建模文档间的语义关联，这种信号更加丰富和自然。

### 批次大小的影响

批次大小是Revela的关键超参数，直接影响批次内交叉注意力的信息丰富度。实验表明，**Revela的性能随批次大小增加而单调提升**（Figure 4, Table 11, Table 12）：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/006_Figure_4.jpg]]
*Figure 4: Performance comparison on CoIR and BEIR with different batch sizes. For both benchmarks, Revela performance generally scales with batch size*

- 在CoIR上，0.1B模型使用批次大小4时平均nDCG@10为43.2%，批次大小增至16时提升至48.4%（+5.2个百分点）。
- 在BEIR上同样呈现正向趋势，但增益幅度略小。

这一现象与监督对比学习中的批次内负样本效应类似——更大的批次提供了更多样化的跨文档上下文，使检索器能学习到更鲁棒的相似度度量。但Revela的优势在于不需要显式的正负例标注，所有文档对的关系通过语言建模目标自然涌现。

### 语言模型规模的影响

通过固定检索器规模、变化LM规模进行消融实验（Figure 5, Table 13, Table 14），发现**LM规模对领域专用任务的增益显著，对通用任务影响有限**：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/007_Figure_5.jpg]]
*Figure 5: Performance comparison on CoIR and BEIR using various combinations of retrievers and LMs. For code retrieval tasks, larger LMs can yield greater gains in retriever performance*

- 在代码检索CoIR上，更大的LM持续带来检索性能提升，呈现明确的正向趋势。
- 在通用BEIR基准上，增大LM并未提供一致的优势，部分任务甚至出现轻微下降。

这一差异的解释是：代码等专业领域具有独特的语法结构和领域知识，更大的LM能更好地建模这些模式，从而为检索器提供更高质量的训练信号。通用领域的文本模式相对简单，LM规模带来的边际收益递减。这提示在实际部署中应根据目标领域选择适当规模的LM，避免不必要的计算开销。

### 域适应与数据混合

Revela展现出良好的域适应能力。在Wikipedia和代码语料的混合数据上训练后（Table 15, Table 16），模型基本保持了各域的原有性能（CoIR均值1B: 56.4%，BEIR均值1B: 43.0%），未出现灾难性遗忘或域间干扰。

更值得注意的是，**使用完全域外数据训练时Revela仍具竞争力**（Table 17, Table 18）：使用Fineweb-edu（通用网页语料）训练的Revela0.5B在CoIR上达到48.6%，仍超过使用代码相关数据训练的E5-PT（46.4%）。这说明语言建模目标捕捉的文本依赖关系具有跨域迁移性，为低资源领域的检索器训练提供了可行路径。

### 语言模型能力保留

联合训练的一个潜在风险是语言模型本身的能力退化。实验表明这一风险几乎不存在（Table 19）：LLaMA-3.2-1B在多个下游基准上的平均准确率为52.5%，经过Revela训练后为52.2%，仅下降0.3个百分点。这说明批次内交叉注意力机制对原始语言建模能力的干扰极小，Revela可以安全地应用于需要同时保留生成和检索能力的场景。

### 计算成本与公平性说明

所有Revela模型在4块A100 80GB GPU上训练，每个域约需44-48小时。与E5-PT使用数百万查询-文档对和更长训练周期相比，Revela的计算成本显著更低。受控实验中，Revela与Contriever使用相同的LM骨干、LoRA秩（256）、学习率（1e-4）和批次构建方式，确保比较的公平性。评估时所有模型统一使用`<eos>` token embedding作为文档表示，并使用相同的查询/文档前缀格式。

### 局限性与失败模式

尽管整体表现优异，Revela存在以下局限：

1. **架构复杂性**：额外的交叉文档注意力模块增加了实现难度，无法直接复用标准Transformer的优化实现。论文通过文档复制和注意力掩码调整的技巧简化实现，但仍需侵入式修改模型结构。

2. **低资源域的数据需求**：虽然不需要标注查询-文档对，但仍需一定量的领域原始文本。对于极端低资源领域，语言建模信号可能不足以学习有效的检索表示。

3. **长文档处理**：训练时文档被截断至160 tokens，对于需要长距离依赖的检索任务可能信息不足。论文未探索更长的上下文窗口或稀疏注意力机制。

4. **模态限制**：当前仅在文本模态上验证，向多模态数据的泛化能力尚未研究。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/009_Table_3.jpg]]
*Table 3: CoIR Benchmark Tasks. The superscripts present the type of the tasks. The abbreviation of the tasks is noted in the parentheses, presented in Table 1*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/010_Table_4.jpg]]
*Table 4: BRIGHT Benchmark Tasks. Abbreviations and descriptions*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/011_Table_5.jpg]]
*Table 5: Baseline retrievers, LMs (Revela’s backbone), CodeRAG-Bench datasets, and evaluation benchmarks with their HuggingFace URLs and licenses*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_e7pAjJZJWb/figures/012_Table_6.jpg]]
*Table 6: Embedding models and their reference URLs*


## 方法谱系与知识库定位

### 1. 与基线方法的关系

Revela 在自监督密集检索器训练范式中引入了一种新的因果机制，其核心区别于现有基线在于**训练信号的来源与检索器参与语言建模的方式**。

**与对比学习基线（Contriever）的比较**

Contriever（Izacard et al., 2022）是经典的自监督检索器，其核心机制是通过文档内部结构（如同文档中不同片段）构造伪查询-文档对，并利用对比学习损失（InfoNCE）训练检索器。该方法将检索器训练与语言模型完全解耦——语言模型不参与检索器的优化过程，仅作为特征提取的骨干网络。

Revela 的因果转折在于：**将检索器嵌入语言模型的下一个token预测循环中**，使检索器计算的跨文档相似度直接调制批次内注意力权重。这意味着检索器的梯度信号来源于语言建模损失，而非独立的对比损失。在受控实验中（相同LLaMA-3.2-1B骨干、相同训练数据、相同LoRA秩和学习率），Revela 在 BEIR 和 CoIR 上均优于 Contriever，且在域外分布上的优势更显著——例如 Flan-code1B 在 BEIR 上达到 39.6 nDCG@10，而 Contriever-code1B 仅为 32.3（Table 2）。这一差距表明，**通过语言建模目标隐式捕捉文档间相关性，比显式构造伪正负样本的对比学习具有更好的泛化能力**。

**与语言模型蒸馏基线（REPLUG）的比较**

REPLUG（Shi et al., 2024）同样探索了利用语言模型信号训练检索器的路径，但其机制本质上是**知识蒸馏**：使用冻结语言模型的困惑度（perplexity）作为跨文档相似度的监督信号，检索器通过拟合该信号进行独立训练。这种方案存在两个瓶颈：（1）语言模型作为固定的"教师"，无法从检索器反馈中受益；（2）困惑度是一个粗粒度的标量信号，无法传递文档内部 token 级别的细粒度相关性信息。

Revela 的突破在于**将单向蒸馏转化为双向联合优化**：检索器和语言模型同步更新，检索器通过批次内注意力机制直接影响语言模型对下一个 token 的预测分布，而语言模型的 NTP 损失梯度则反向传播至检索器参数。在相同冻结 LM（LLaMA-3.2-1B）和相同批次构建方式的设置下，Revela 的性能显著优于 REPLUG 范式。

**与有监督/弱监督基线的比较**

Revela 展现出令人瞩目的**数据效率优势**。在 CoIR 基准上，Revela3B（60.1 nDCG@10）超越了有监督的 7B 参数模型 E5-Mistral-7B-Instruct（57.3），提升 2.8 个百分点（Table 1）。在 BEIR 上，Revela3B 以约 1/1000 的训练数据和 1/10 的计算量达到了与弱监督 E5-PT（Wang et al., 2022）相同的 45.6 nDCG@10（Table 7）。E5-PT 依赖数百万半结构化文本对进行预训练，而 Revela 仅使用原始文本块——这一对比揭示了**语言建模目标中蕴含的丰富语义结构足以替代显式标注数据**。

### 2. 适用边界与领域特异性

Revela 的性能优势在不同领域呈现**非均匀分布**：

- **专业领域（代码检索 CoIR）**：Revela 的优势最为显著。在相同规模下，Revela0.5B（56.1）超越弱监督 E5-PT 0.3B（46.4）达 9.7 个百分点。更大的语言模型对代码检索的提升尤为明显（Figure 5），说明 LM 中蕴含的代码语义知识通过联合训练有效迁移至检索器。

- **复杂推理（BRIGHT）**：Revela3B（20.1）大幅超越 E5-PT（13.1），提升 7.0 个百分点（Table 8），并超越多个专有嵌入 API。这表明**跨文档注意力机制能捕捉推理所需的深层语义关联**，而非仅依赖表面词汇匹配。

- **通用领域（BEIR）**：性能提升相对温和，Revela3B 与 E5-PT 持平。更大的语言模型对通用领域检索的提升不显著（Figure 5），说明当任务主要依赖浅层语义匹配时，联合语言建模的增益有限。

在域外数据场景中，使用 Fineweb-edu 训练的 Revela0.5B 在 CoIR 上仍达到 48.6%，超过域内训练的 E5-PT（46.4%）（Table 17），展现出良好的**跨域迁移能力**。混合域训练（Wikipedia + 代码语料）的实验表明，Revela 能够基本保持各域原有性能（Table 15, 16），未出现灾难性遗忘。

### 3. 局限性与开放问题

**架构复杂性**：Revela 需要额外的交叉文档注意力模块，这增加了模型复杂性，使其直接集成到现有标准 Transformer 实现（如 HuggingFace 等框架）中存在工程挑战。批次内注意力的实现依赖文档复制和注意力掩码调整，对推理部署的友好性有待验证。

**数据依赖性**：尽管无需标注查询-文档对，Revela 仍需要一定量的领域相关原始文本进行训练。对于极端低资源的领域，文本量不足可能限制检索器对领域语义的捕捉。

**索引更新成本**：当前框架中，检索器更新后需要对整个语料库重新计算嵌入，这是一个尚未解决的实际部署瓶颈。如何设计增量索引或高效重编码机制，是推动 Revela 走向实际应用的关键问题。

**多模态泛化**：现有验证仅限于文本模态。将"通过语言建模训练检索器"的范式扩展到图像、音频等多模态数据，需要重新设计跨模态的批次内注意力机制和相似度计算方式，目前尚无明确路径。

**规模扩展的边界**：虽然实验显示性能随批次大小和模型规模提升（Figure 4），但更大规模（如 7B+ 参数）下的收益递减规律、联合训练中 LM 能力保留的上限、以及注意力机制的稀疏化需求，仍是开放的研究方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Revela_Dense_Retriever_Learning_via_Language_Modeling.pdf]]
