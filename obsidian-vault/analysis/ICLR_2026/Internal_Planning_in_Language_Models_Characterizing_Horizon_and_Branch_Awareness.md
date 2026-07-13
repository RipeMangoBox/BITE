---
title: "Internal Planning in Language Models: Characterizing Horizon and Branch Awareness"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Internal_Planning_in_Language_Models_Characterizing_Horizon_and_Branch_Awareness.pdf
project_link: null
code_link: null
openreview_forum_id: dqGWQdFdTC
aliases:
- VV
- IPLMCHBA
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "采用基于 VQ-VAE 的离散码压缩隐藏状态，并在此基础上计算互信息（MI），从而自动化地、无需监督探针地分析内部计算结构。"
primary_logic: "预输出计算的规划视野高度依赖任务性质：在局部语法任务中表现为短视，而在长程规划任务中保持更远的前瞻依赖；模型隐式保留了未使用的正确延续信息（分支意识），且预测决策最依赖最近的计算块和最后几层，但早期块仍包含可用信息。"
claims:
- "在 CFG 任务上，前缀计算与未来决策状态之间的 nMI 快速衰减（τ=10 时降至约 1/5），表明短视野规划。"
- "在路径查找任务（PF）上，nMI 不衰减甚至增加，表明长视野规划依赖，且 MTP 训练的模型 nMI 更均匀，准确率更高。"
- "前缀计算与备选正确路径的互信息显著高于与无关诱饵路径的互信息（比例 > 1），证实了分支意识。"
- "在自然语言文本上，预测信息集中于最近的块和最后几层，但早期块仍提供额外信息（条件互信息 ≈0.3）。"
---

# Internal Planning in Language Models: Characterizing Horizon and Branch Awareness

> [!tip] 核心洞察
> 预输出计算的规划视野高度依赖任务性质：在局部语法任务中表现为短视，而在长程规划任务中保持更远的前瞻依赖；模型隐式保留了未使用的正确延续信息（分支意识），且预测决策最依赖最近的计算块和最后几层，但早期块仍包含可用信息。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 语言模型的内部规划：表征规划视野与分支意识 |
| 英文题名 | Internal Planning in Language Models: Characterizing Horizon and Branch Awareness |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dqGWQdFdTC) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | 基于 VQ-VAE 压缩与互信息估计的规划分析框架 |
| Dataset | CFG (上下文无关语法), PF-Long (路径查找-长), PF-Long, PF-Short (路径查找-短) |

> [!tip] 效果简介
> - CFG (上下文无关语法) 上，nMI (前缀-决策状态) 衰减 为 M_MTP 衰减略慢，但整体迅速下降，对比 M_NTP 快速衰减，τ=10 降至约 1/5，变化 M_MTP 稍高，但无显著反向。
> - PF-Long (路径查找-长) 上，准确率 为 M_MTP 0.85 ± 0.02，对比 M_NTP 0.60 ± 0.01，变化 +0.25。
> - PF-Long 上，分支意识比率 (T(Z_H;Z_alt) / T(Z_H;Z_decoy)) 为 M_MTP 1.82 ± 0.27，对比 M_NTP 1.45 ± 0.01，变化 +0.37。

## 概要

语言模型（LM）在生成文本时是否进行了“内部规划”——即前缀计算是否前瞻性地编码了未来决策所需的信息——是一个悬而未决的问题。现有分析方法主要依赖线性或非线性探针（probing），但这些探针存在严重混淆：探针本身可能学习到与模型内部计算无关的模式，且其预测性能受目标变量边际复杂度的干扰，无法可靠地揭示模型的前瞻计算和分支意识。因此，**该领域的核心瓶颈在于缺乏一种自动化、无监督且不受探针混淆因素影响的分析框架，来可靠地刻画 LM 内部计算的信息结构。**

本文提出了一种基于向量量化变分自编码器（VQ-VAE）与互信息（MI）估计的规划分析框架，直击上述瓶颈。其核心思路是：先将冻结的 LM 中选定 Transformer 块的隐藏状态通过 VQ-VAE 压缩为离散码（codebook indices），再基于这些离散码的经验共现分布计算 Shannon 互信息及其归一化形式（nMI），从而在无需手工电路挖掘或逐对训练探针的前提下，自动化地度量模型内部不同计算组件之间的信息共享。**该框架的关键洞察在于：预输出计算的规划视野高度依赖任务性质——在局部语法任务中表现为短视，而在长程规划任务中保持更远的前瞻依赖；模型隐式保留了未使用的正确延续信息（分支意识），且预测决策最依赖最近的计算块和最后几层，但早期块仍包含可用信息。**

在方法谱系中，本文框架相对于现有工作做出了三个关键替换：将原始高维隐藏状态或探针学习的监督表示替换为 VQ-VAE 训练的无监督离散码；将探针预测准确率或 ν-information 等信息度量替换为离散码之间的 Shannon 互信息及其归一化形式，用于相对比较；将需要手工电路挖掘或逐对探针训练的分析流程替换为一次 VQ-VAE 训练即可复用于所有 MI 估计的自动化流水线。基线方法包括标准下一词预测训练（M_NTP）作为训练目标的对比锚点，以及线性/非线性探针和 ν-information 作为信息度量的对比对象。

主要实验结果支撑了核心论断：
- **规划视野的任务依赖性**：在上下文无关语法（CFG）任务上，前缀计算与未来决策状态之间的 nMI 随偏移 τ 快速衰减（τ=10 时降至约 1/5），表明短视野规划（Figure 3a）。而在路径查找（PF）任务上，nMI 不衰减甚至增加，表明长视野规划依赖；多词预测训练（M_MTP）使 nMI 更均匀，且准确率从 0.60 提升至 0.85（Figure 3b, Table 1）。
- **分支意识**：前缀计算与备选正确路径的互信息显著高于与无关诱饵路径的互信息（比率 > 1），证实模型隐式保留了未选择分支的信息（Table 1）。
- **计算历史的贡献分布**：在自然语言文本上，预测信息集中于最近的块和最后几层，但早期块仍提供额外信息（条件互信息约 0.3），表明近期计算并非唯一信息源（Figure 4）。

该框架的局限性在于：依赖离散压缩质量，码书大小有限可能导致信息丢失；MI 估计仅提供平均意义下的洞察，不能解释单个输入；分析限于相对比较，无法给出绝对规划分数；实验限于较小规模模型（GPT-3 Small 及 0.3B 参数）。待解决的问题包括如何将分析扩展到更大规模模型和思维链等提示策略下的规划动态。

语言模型在生成文本时是否进行了“内部规划”——即在输出当前词之前，提前计算未来多步的信息——是理解其推理能力的关键问题。然而，直接回答这一问题面临双重困难：一方面，模型的隐藏状态是高维连续向量，难以直接解读；另一方面，现有的分析方法存在严重的混淆因素。

当前主流的分析范式依赖于**探针（probing）**：在冻结的模型隐藏状态上训练线性或非线性分类器/回归器，以预测某些目标属性（如未来词或句法标签），并将探针的准确率或误差作为信息存在的证据。但这一范式存在根本性缺陷：探针本身具有学习能力，可能从噪声中提取模型并未显式编码的信息，也可能因目标属性的边际分布复杂性不同而产生误导性的得分差异。此外，探针方法需要针对每一对“源状态-目标属性”单独训练，分析成本随变量组合数线性增长，难以自动化地探索模型内部的计算结构。

另一类替代方案是使用 **ν-information** 等信息度量，但其对编码器容量的尺度敏感性使得不同实验设置下的结果难以直接比较，在简单验证实验上已表现出失效。

上述方法学缺口导致了一个核心瓶颈：**我们缺乏一种既能自动化分析、又能避免探针混淆因素的可靠手段，来揭示语言模型内部的前瞻计算和分支意识**。具体而言，三个相互关联的问题悬而未决：

1. **规划视野**：模型的前缀计算究竟覆盖了多远的未来？是仅服务于下一个词的局部决策，还是为长程依赖维持信息？
2. **分支意识**：在存在多个正确延续的任务中，模型是否隐式地保留了未被选择的正确路径的信息？
3. **计算历史组织**：预测决策依赖的计算信息如何在层和位置维度上分布？是集中于最后几层和最近位置，还是分散在更早的计算块中？

本文的动机正是针对这一瓶颈，提出一个基于信息论和离散表示的自动化分析框架，以绕过探针方法的混淆因素，系统性地回答上述三个问题。

## 核心方法与创新机理

本文的核心创新在于提出了一套**基于 VQ-VAE 离散压缩与互信息估计的自动化分析框架**，用以揭示语言模型内部规划的计算结构。相较于现有方法，该框架在两个关键维度上实现了突破。

### 从探针监督到无监督信息度量

传统的内部表征分析方法——无论是线性探针还是非线性探针——存在根本性的混淆因素：探针本身可能学习到与模型内部计算无关的模式，其预测准确率或回归误差受目标变量边际复杂度的严重影响，无法可靠地反映模型内部的信息流动（参见 Appendix D 的探针基线实验）。ν-information 等度量虽然试图改进，但实验表明其在简单验证任务上即已失效（Figure 20），且对尺度高度敏感。

本文的方法通过以下 **changed slots** 绕开了这些陷阱：

| 维度 | 基线做法 | 本文做法 | 关键优势 |
|------|----------|----------|----------|
| **内部表示形式** | 原始高维隐藏状态，或探针学习的监督表示 | VQ-VAE 训练的无监督离散码（codebook indices） | 无需标注目标变量，避免探针混淆；离散化使互信息计算可行 |
| **信息度量方式** | 探针预测准确率/MSE，或 ν-information | Shannon 互信息及其归一化形式（nMI），用于相对比较 | 信息论基础严格，nMI 消除绝对尺度影响，支持跨实验比较 |
| **分析自动化程度** | 需手工电路挖掘，或对每对变量单独训练探针 | 对同一类表示训练一次 VQ-VAE，即可复用于所有 MI 估计 | 一次训练，多次分析，大幅降低人工成本 |

核心机制是：对于冻结的预训练 LM，从选定 Transformer block 中提取隐藏状态集合 $G_{\mathcal{S}}$，通过 VQ-VAE 编码器将其映射为离散码书索引 $Z_{\mathcal{S}} \in [K]$。训练目标联合优化重建损失、向量量化损失、码书多样性正则（余弦相似度惩罚）和反崩塌熵正则：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_q \mathcal{L}_{\mathrm{vq}} + \lambda_{\cos} \mathcal{L}_{\cos} + \lambda_{\mathrm{ent}} \mathcal{L}_{\mathrm{ent}}$$

量化过程为最近邻查找 $k^\star = \arg\min_{k \in [K]} \|r_{\mathcal{S}} - e_k\|_2^2$，得到离散码 $Z_{\mathcal{S}} \equiv k^\star$。随后在数据集上统计两组离散码的经验共现分布，计算 Shannon 互信息：

$$I(Z_A; Z_B) = \sum_{z_a \in \mathcal{Z}_A} \sum_{z_b \in \mathcal{Z}_B} p(z_a, z_b) \log \frac{p(z_a, z_b)}{p(z_a) p(z_b)}$$

并归一化为 $\mathrm{nMI}(Z_A; Z_B) = I(Z_A; Z_B) / \mathcal{T}_{\max}$，其中 $\mathcal{T}_{\max}$ 为同组实验中的最大 MI 值。这一归一化使得 nMI 仅用于**相对比较**，而非声称绝对规划分数。

### 从手工电路到自动化结构发现

现有电路发现方法需要大量人工介入和对模型结构的强假设。本文框架将分析流程标准化为三个步骤（Figure 1）：(1) 训练 VQ-VAE 编码器；(2) 应用编码器收集离散码的共现统计；(3) 估计互信息并分析计算结构。这一流程使得研究者可以系统性地探究规划视野、分支意识和计算历史信息分布等维度，而无需针对每个问题重新设计探针或手工追踪信息流。

验证实验（Figure 5-7）表明，随着码书大小从 64 增长到 2048，归一化互信息估计值越来越接近理论参考值，即使在注入噪声和类内变异的困难条件下，估计的排序一致性仍然保持。这为框架的可靠性提供了经验支撑。

### 创新边界与局限

需要明确指出：框架的洞察力受限于 VQ-VAE 压缩质量——码书大小有限，必然导致信息丢失；互信息估计仅提供平均意义下的聚合洞察，无法解释单个输入；分析限于相对比较，不能给出绝对规划分数。此外，当前实验限于 GPT-3 Small 及 0.3B 参数规模，向更大模型的扩展需要额外的数据与计算资源投入。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/001_Figure_1.jpg]]
*Figure 1: The proposed method. Step 1 (training): For a frozen LM M, hidden states from selected transformer blocks $G _ { S }$ are passed through a VQ-VAE encoder, which maps each block to a latent vector and then to a discrete codebook index $Z _ { S }$ ~ $\in$ ~ [ K ] , providing coarse summaries of internal computations. Step 2 (analysis): For two sets of hidden-state blocks, $G _ { S _ { A } }$ and $G _ { S _ { B } }$ , we apply the trained encoder and codebook to the dataset to obtain discrete variables $Z _ { A }$ and $Z _ { B }$ and collect their empirical co-occurrence counts. Step 3: Using these statistics, we estimate joint and marginal distributions p ( $z _ { a } , z _ { b }$ ) , p ( $z _ { a }$ ) , and p...*

本文提出一个基于信息论的分析框架，用于自动化地研究语言模型内部与规划相关的计算组织方式。该框架的核心思想是：将冻结的预训练语言模型的内部隐藏状态压缩为离散摘要码，然后通过计算这些离散码之间的互信息（Mutual Information, MI）来量化模型内部不同计算组件之间的信息共享程度，从而揭示其规划视野（horizon）与分支意识（branch awareness）等特性。

整个分析流程分为三个步骤，如 Figure 1 所示：

**步骤一：VQ-VAE 编码器训练。** 对于一个冻结的语言模型 $M$，从选定的 Transformer 块（block）集合 $G_{\mathcal{S}}$ 中提取隐藏状态。这些隐藏状态被送入一个 VQ-VAE 编码器，编码器将每个块映射到一个潜在向量，再通过最近邻查找量化为离散的码书索引 $Z_{\mathcal{S}} \in [K]$，作为内部计算的粗粒度摘要。训练目标联合了重建损失、向量量化损失、码书多样性正则项和熵正则项，以防止码书坍塌并保证压缩质量：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_q \mathcal{L}_{\mathrm{vq}} + \lambda_{\cos}\mathcal{L}_{\cos} + \lambda_{\mathrm{ent}}\mathcal{L}_{\mathrm{ent}}$$

其中 $\mathcal{L}_{\cos}$ 通过余弦相似度惩罚推动码书嵌入多样化，$\mathcal{L}_{\mathrm{ent}}$ 则抑制码使用分布的过度集中。

**步骤二：经验分布统计。** 对于两组需要分析的隐藏状态块 $G_{\mathcal{S}_A}$ 和 $G_{\mathcal{S}_B}$，分别应用已训练好的编码器和码书，在数据集上获得离散变量 $Z_A$ 和 $Z_B$，并收集它们的共现计数，用于估计联合分布 $p(z_a, z_b)$ 和边缘分布 $p(z_a)$、$p(z_b)$。

**步骤三：互信息估计与分析。** 基于经验分布计算 Shannon 互信息：

$$I(Z_A; Z_B) = \sum_{z_a \in \mathcal{Z}_A} \sum_{z_b \in \mathcal{Z}_B} p(z_a, z_b) \log \frac{p(z_a, z_b)}{p(z_a)p(z_b)}$$

为进一步进行相对比较，定义归一化互信息（Normalized Mutual Information, nMI）：

$$\mathrm{nMI}(Z_A; Z_B) = \frac{I(Z_A; Z_B)}{\mathcal{T}_{\max}}$$

其中 $\mathcal{T}_{\max}$ 为同一实验分析中所有 MI 计算的最大值。这一归一化使得跨实验的 MI 值具有可比性，但框架本身不提供绝对的规划分数，仅支持相对排序分析。此外，框架还支持条件互信息分析，用于评估特定计算块在已知其他块信息后的增量贡献。

该框架的关键优势在于：对同一类表示的 VQ-VAE 只需训练一次，即可复用于所有后续的 MI 估计，避免了传统探针方法（probing）需要针对每对变量单独训练监督探针的繁琐流程，同时也消除了探针学习能力差异带来的混淆因素。

### 方法流水线总览

本方法围绕三个核心步骤构建（Figure 1）：

1. **VQ‑VAE 编码器训练**：对冻结的预训练语言模型，从选定的 Transformer 块中提取隐藏状态，训练一个向量量化变分自编码器（VQ‑VAE），将高维隐藏状态压缩为离散码书索引，作为内部计算的粗粒度摘要。
2. **经验分布统计**：对两组隐藏状态块分别应用已训练的编码器，在数据集上收集离散码的共现计数，得到联合分布与边缘分布的经验估计。
3. **互信息估计**：基于经验分布计算 Shannon 互信息及其归一化形式，用于分析模型计算组件之间的信息共享。

### 关键模块

#### 隐藏状态提取

从冻结的预训练 LM 中提取指定层 $\ell$ 和位置 $t$ 的 Transformer 块输出 $h_t^\ell$。对于前缀计算的整体总结，定义集合：

$$H = \{h_t^\ell \mid t = 1,\ldots,T;\; \ell = 1,\ldots,L-1\} \in \mathbb{R}^{T \times (L-1) \times d}$$

该集合囊括了除最终层外所有前缀位置的隐藏状态，编码了模型在生成决策前的全部计算历史。

#### VQ‑VAE 编码与离散化

编码器将可变长度的隐藏状态块 $G_{\mathcal{S}}$ 映射为紧凑的潜在向量 $r_{\mathcal{S}}$，再通过最近邻查找量化为码书索引：

$$k^\star = \arg\min_{k \in [K]} \|r_{\mathcal{S}} - e_k\|_2^2, \quad Z_{\mathcal{S}} \equiv k^\star$$

其中 $e_k$ 为码书嵌入向量，$K$ 为码书大小。量化后的表示 $\widetilde{r}_{\mathcal{S}} = e_{k^\star}$ 用于解码器重建原始输入。

**训练损失** 联合优化重建质量与码书质量：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rec}} + \lambda_q \mathcal{L}_{\mathrm{vq}} + \lambda_{\cos} \mathcal{L}_{\cos} + \lambda_{\mathrm{ent}} \mathcal{L}_{\mathrm{ent}}$$

各分量含义：
- $\mathcal{L}_{\mathrm{rec}}$：重建损失，最小化原始隐藏状态与解码器输出之间的误差。
- $\mathcal{L}_{\mathrm{vq}}$：向量量化损失，约束编码器输出靠近选中的码书嵌入。
- $\mathcal{L}_{\cos}$：码书多样性正则，通过惩罚码书嵌入之间的余弦相似度，推动码向量分散。
- $\mathcal{L}_{\mathrm{ent}}$：熵正则项，防止码书坍缩（即少数码被过度使用），鼓励均匀的码书利用率。

该损失设计是框架自动化的关键——对同一类表示的 VQ‑VAE 仅需训练一次，即可复用于所有后续的互信息估计，避免了传统探针方法需要为每对变量单独训练监督探针的繁琐与混淆因素。

#### 互信息估计

对两组离散随机变量 $Z_A$、$Z_B$，基于经验共现计数估计 Shannon 互信息：

$$I(Z_A; Z_B) = \sum_{z_a \in \mathcal{Z}_A} \sum_{z_b \in \mathcal{Z}_B} p(z_a, z_b) \log \frac{p(z_a, z_b)}{p(z_a) p(z_b)}$$

其中 $p(z_a, z_b)$、$p(z_a)$、$p(z_b)$ 均从数据集的码对计数中获得。互信息衡量了知晓 $Z_A$ 能减少多少关于 $Z_B$ 的不确定性。

#### 归一化互信息 (nMI)

由于互信息的绝对值受码书大小、数据分布等因素影响，跨实验不可直接比较，本文引入归一化互信息用于相对排序：

$$\mathrm{nMI}(Z_A; Z_B) = \frac{I(Z_A; Z_B)}{\mathcal{T}_{\max}}$$

其中 $\mathcal{T}_{\max}$ 为同一实验分析中所有 MI 计算的最大值。nMI 不提供绝对规划分数，仅在同组实验内进行相对比较。

#### 条件互信息分析

为评估特定计算块的增量信息贡献，框架支持条件互信息分解。例如，在分析前缀历史中早期块对决策的贡献时，可计算在已知最后位置状态 $Z_T^\ell$ 的条件下，早期块与决策状态之间的条件互信息，从而剥离由最终位置传递的信息份额。

### 与基线方法的差异

| 设计维度 | 基线方法（探针） | 本文方法 |
|---------|-----------------|---------|
| 内部表示形式 | 原始高维隐藏状态或探针学习的监督表示 | VQ‑VAE 训练的无监督离散码 |
| 信息度量方式 | 探针预测准确率/MSE，或 $\nu$-information | Shannon 互信息及其归一化形式 (nMI) |
| 自动化程度 | 需手工电路挖掘或逐对训练探针 | 同类表示训练一次，复用所有 MI 估计 |

探针方法存在两重混淆：探针自身的学习能力会放大或掩盖真实的信息量，且探针得分受目标变量边际复杂性的影响。$\nu$-information 虽可衡量以某函数族可提取的信息，但对尺度敏感，在简单验证实验中即失效（Figure 20）。本文的离散码 + Shannon MI 方案通过压缩消除表示维度的干扰，并通过归一化实现稳健的相对比较。

## 实验与关键发现

### 核心发现：规划视野由任务性质决定

本研究通过测量前缀计算摘要 $Z_{1:T}^{1:L-1}$ 与未来决策状态 $Z_{T+\tau}^{L}$ 之间的归一化互信息（nMI），量化了语言模型的规划视野。实验揭示了一个关键洞察：**预输出计算的规划视野高度依赖任务性质，在局部语法任务中表现为短视，而在长程规划任务中保持更远的前瞻依赖。**

在上下文无关语法（CFG）任务上，nMI 随未来偏移 $\tau$ 的增加迅速衰减。如 Figure 3a 所示，标准下一词预测模型（$M_{\text{NTP}}$）在 $\tau=10$ 时，前缀计算与决策状态之间的 nMI 降至初始值的约五分之一。多词预测模型（$M_{\text{MTP}}$）的衰减略慢，但整体趋势相似，表明 CFG 任务中的局部语法依赖不需要长程规划。这一结果与 CFG 任务仅依赖最近上文的结构特性一致。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/005_Figure_3.jpg]]
*Figure 3: nMI results between the prefix summary codes and the last hidden state codes of generated tokens for CFG (a) and PF (b) tasks. nMI decays fast in CFG, consistent with short-range dependence, while PF maintains or even increases nMI beyond $\tau$ = 1 , consistent with longer-horizon predictive dependence of prefix computation on later decision states*

相反，在路径查找（PF）任务上，nMI 展现出截然不同的模式（Figure 3b）。对于 PF-Long（路径长度 6），$M_{\text{NTP}}$ 的 nMI 在 $\tau$ 增大时保持稳定甚至略有上升，表明前缀计算对远期决策状态保持持续的信息依赖。值得注意的是，$M_{\text{MTP}}$ 的 nMI 曲线比 $M_{\text{NTP}}$ 更均匀，这一特征与其显著更高的准确率（0.85 vs 0.60，Table 1）高度相关，暗示 MTP 训练通过鼓励模型在多个未来步上对齐隐藏状态，促进了更均衡的长程信息编码。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/006_Table_1.jpg]]
*Table 1: Mean ± std for $\mathcal { T } ( Z _ { H } ; Z _ { \mathrm { a l t } } ) \big / \mathcal { T } ( Z _ { H } ; Z _ { \mathrm { d e c o y } }$ ) metric and accuracy values in branches in the plan experiment (§ 3.2). Models encode information about unchosen correct branches more strongly than unrelated decoys, indicating branch awareness in prefix computations

**证据强度**：Figure 3 的结果基于多随机种子的 GPT-3 Small 模型，nMI 趋势在 0.3B 参数模型上也得到复现（Figure 17），增强了结论的可靠性。但需注意，nMI 仅提供相对比较，不能直接解释为绝对规划能力分数。

### 分支意识：模型隐式保留未使用的正确延续

在路径查找任务中，每个前缀存在多条正确路径。通过比较前缀计算与备选正确路径 $Z_{\text{alt}}$ 和无关诱饵路径 $Z_{\text{decoy}}$ 之间的互信息比率，实验揭示了语言模型的**分支意识**——即模型在前缀计算中隐式编码了未选择的正确延续信息。

Table 1 汇总了关键结果：
- **PF-Short**（路径长度 4）：$M_{\text{NTP}}$ 的比率高达 $7.60 \pm 0.78$，$M_{\text{MTP}}$ 为 $6.29 \pm 0.17$，均远大于 1，表明前缀计算与正确备选路径共享的信息显著多于与随机诱饵路径的共享信息。
- **PF-Long**（路径长度 6）：比率降至 $1.45 \pm 0.01$（$M_{\text{NTP}}$）和 $1.82 \pm 0.27$（$M_{\text{MTP}}$），但仍显著大于 1，证实即使在更难的长程任务中，分支意识依然存在。

值得注意的是，在 PF-Long 上，$M_{\text{MTP}}$ 不仅准确率大幅领先（+0.25），其分支意识比率也更高（+0.37），而 PF-Short 上两者准确率相近（0.91 vs 0.89）。这一模式表明，MTP 训练在任务难度增大时对分支意识的增强作用更为明显，可能是其提升长程规划性能的关键机制。

**证据强度**：分支意识比率基于互信息估计，置信度较高（0.95），因为备选路径和诱饵路径的构造明确，且比率 > 1 的结论在两种任务和两种训练目标下均成立。但需注意，该分析仅适用于存在明确分支结构的任务，向自然语言文本的推广需要进一步验证。

### 计算历史中的信息分布：近期块和最后几层主导，早期块仍有贡献

在自然语言文本（OpenWebText）上，实验通过分析不同层和块位置的隐藏状态与生成决策状态之间的 nMI，揭示了预测信息的时空分布规律。Figure 4 的热力图（左和中）显示：
- **块维度**：最近的块（小 $k$）与决策状态的 nMI 最高，随着块距离增大，nMI 单调下降。
- **层维度**：最后几层（高 $\ell$）的 nMI 显著高于低层，表明预测相关信息主要集中在网络的高层。
- **时间衰减**：$\tau=0$（当前生成）的 nMI 整体高于 $\tau=1$（下一生成），符合信息随预测距离衰减的预期。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/008_Figure_4.jpg]]
*Figure 4: nMI across blocks and layers, and conditional nMI. L e f t ${ \mathrm { . } }$ nMI between the hidden state block codes and the token decision state code at $\tau$ = 0 , $\mathrm { n M } ( \mathbf { \bar { B } } _ { k } ^ { \ell } ; Z _ { T } ^ { L }$ ) . Middle: nMI between block codes and the last-layer decision code at $\tau$ = 1 , $\mathrm { n M I } ( \mathbf { B } _ { k } ^ { \ell } ; Z _ { T + 1 } ^ { L }$ ) . In both heatmaps, nMI is higher for recent blocks (small k) and final layers (high ℓ). Right: Conditional nMI for the $1 ^ { \mathrm { s t } }$ block, $\mathrm { n } \mathsf { \breve { M } I } ( Z _ { T - 1 5 : T - 1 } ^ { \ell } ; Z _ { T } ^ { L } \mid Z _ { T } ^ { \ell }$ ) ), showing tha...

然而，条件互信息分析（Figure 4 右）揭示了一个重要细节：在给定最后位置 $T$ 的相同层隐藏状态后，早期块（$T-15$ 至 $T-1$）与决策状态之间的条件 nMI 约为 0.3，表明**早期块仍提供不能由最后位置完全传递的额外信息**。这意味着模型并非简单地将所有历史信息压缩到最后位置的表示中，而是保留了分布式的计算依赖。

**证据强度**：该分析基于自然语言数据，结论置信度为 0.85-0.9。条件互信息的结果需要通过消融实验进一步验证其因果性，但当前证据足以支持“信息分布非完全集中”的定性结论。

### 方法验证：VQ-VAE 压缩质量与码书大小的关系

消融实验验证了 VQ-VAE 离散压缩的可靠性。Figure 5 显示，随着码书大小从 64 增至 2048，估计的归一化互信息逐渐逼近理论值，证明了压缩质量的提升。更严格的验证实验（Figure 6 和 Figure 7）表明，即使在前缀相似或完全独立替代的困难条件下，归一化互信息仍能保持与参考互信息一致的排序，且大码书表现更优。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/010_Figure_6.jpg]]
*Figure 6: Harder validation experiment with similar prefixes for each label. Each label maps to 16 surrogates created by one-token edits. Normalized $\bar { \mathcal { T } } \left( Z _ { A } ; Z _ { B } \right$) remains order-consistent with the reference-process MI across K , , despite injected noise and within-class variability

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_dqGWQdFdTC/figures/011_Figure_7.jpg]]
*Figure 7: Hardest validation experiment with fully independent surrogates. Despite the lack of within-class proximity, normalized $\mathcal { T } \left( Z _ { A } ; Z _ { B } \right$) preserves the ordering induced by the referenceprocess MI, and improves as the codebook grows

此外，VQ-VAE 的重建质量随编码器参数量增加而提升（Figure 16，nRMSE 下降），表明充分的编码器容量对有效压缩是必要的。这些结果为基于离散码的互信息估计提供了方法学基础。

### 失败模式与局限

1. **探针方法的混淆问题**：附录 D 中的探针基线实验（Figure 18）显示，探针预测准确率和隐藏状态回归误差随 $\tau$ 的变化趋势受目标边际复杂性的影响，可能产生误导性结论。$\nu$-information（Figure 19、Figure 20）同样存在尺度敏感性问题，在简单验证实验上无法保持排序一致性。这反证了本文提出的无监督离散码方法的必要性。

2. **信息丢失风险**：VQ-VAE 的有限码书大小可能导致信息丢失，尤其在处理高维隐藏状态时。当前实验使用的码书大小（最大 2048）对于复杂任务可能不足，需要进一步探索。

3. **聚合分析的局限**：互信息估计仅在平均意义上提供洞察，不能解释单个输入的规划行为。对于需要实例级解释的应用场景，该方法需要补充其他分析手段。

4. **模型规模限制**：所有实验限于 GPT-3 Small（约 125M 参数）和 0.3B 参数模型，未验证在大规模模型上的适用性。虽然 Figure 17 在 0.3B 模型上复现了 CFG 的 nMI 衰减趋势，但更大模型的规划行为可能有所不同。

## 定位与知识库关联

### 核心瓶颈与设计动机

理解语言模型（LM）在生成过程中的内部规划机制——即模型在输出当前词之前，是否以及如何为未来决策进行前瞻计算——是当前可解释性研究的核心挑战。现有方法主要依赖**线性或非线性探针**（probing），通过训练监督分类器或回归器来解码隐藏状态中的信息。然而，探针方法存在根本性的混淆因素：探针本身的学习能力会引入额外信息提取能力，使得我们无法区分信息究竟是存在于模型表示中，还是由探针“补全”的。此外，探针需要对每一对变量组合单独训练，无法实现自动化分析。

本文提出的框架正是针对这一瓶颈：**采用基于 VQ-VAE 的无监督离散压缩替代探针学习**，将高维隐藏状态映射到离散码书索引，进而在离散空间上计算 Shannon 互信息（MI）及其归一化形式（nMI），从而自动化地、无需监督信号地分析模型内部计算结构。这一设计消除了探针容量带来的混淆，同时通过离散化使得 MI 估计在计算上可行。

### 方法谱系中的位置

#### 相对于探针方法（probing）

传统的探针方法（如线性探针、MLP 探针）通过监督学习评估隐藏状态中是否编码了特定属性。本文在 Appendix D 中直接对比了探针基线：在 CFG 任务上，探针的 token 准确率和隐藏状态回归误差随未来偏移 τ 的变化趋势与本文的 nMI 衰减趋势定性一致，但探针得分受目标边际复杂性的影响，无法提供纯粹的“表示中已有信息量”的度量。本文的 nMI 度量则直接基于表示本身的离散码分布，不引入额外学习容量。

#### 相对于 ν-information

Xu et al. 提出的 ν-information 是另一种信息度量，旨在衡量给定函数族下可提取的信息量。本文在 Appendix D 中对比了 ν-information：在简单验证实验上，ν-information 无法保持 MI 的顺序一致性（Figure 20），而本文的归一化互信息估计在码书足够大时能可靠地恢复理论 MI 的排序（Figure 5-7）。ν-information 的尺度敏感性使其不适合本文所需的相对比较场景。

#### 相对于电路发现（circuit discovery）

电路发现方法（如 activation patching、path patching）通过干预实验定位关键子网络，需要手工设计干预模式和假设。本文的方法**不进行任何模型干预**，仅通过观察冻结模型在数据集上的离散码共现统计来推断信息流动，避免了手工工程和强假设，代价是只能提供聚合层面的洞察，无法解释单一样本。

#### 相对于多词预测训练（MTP）

本文对比了两种训练目标：标准下一词预测（**M_NTP**）和多词预测（**M_MTP**）。MTP 并非本文提出，而是作为分析对象：通过对比 M_NTP 和 M_MTP 在规划视野和分支意识上的差异，揭示训练目标如何塑造内部规划能力。实验表明，M_MTP 在长程路径查找任务（PF-Long）上准确率显著更高（0.85 vs 0.60），且其 nMI 分布更均匀、分支意识比率更高，说明 MTP 训练确实促进了更长视野的前瞻计算。

### 适用边界与局限

1. **离散压缩质量依赖**：框架的有效性取决于 VQ-VAE 压缩的质量。码书大小有限（实验中最大 2048），必然导致信息丢失。Figure 5-7 的验证实验表明，随码书增大，nMI 估计更接近理论值，但始终存在偏差。对于需要精细区分的信息，离散化可能掩盖关键差异。

2. **聚合分析而非单样本解释**：MI 估计基于整个数据集的共现统计，提供的是平均意义上的洞察。无法解释特定输入下模型的规划行为，也不适用于需要实例级归因的场景。

3. **仅支持相对比较**：nMI 通过除以同组实验中的最大值进行归一化，因此只能用于同一分析内的相对排序，不能跨实验给出绝对规划分数。

4. **模型规模限制**：实验限于 GPT-3 Small 规模（约 125M 参数）和 0.3B 参数的模型。Figure 17 在 0.3B 模型上复制了 CFG 的 nMI 衰减趋势，表明小模型的发现可能具有可扩展性，但尚未在大模型（如 7B+）上验证。大模型的隐藏状态维度更高、信息更分散，VQ-VAE 压缩的难度和信息丢失可能更严重。

5. **计算开销**：VQ-VAE 训练需要额外的数据和计算资源。对于每个需要分析的状态集合（如全部前缀计算 H、单个 block 等），需要单独训练一个 VQ-VAE 编码器，这在大规模模型或多样任务上可能成为瓶颈。

### 开放问题

1. **规模扩展**：如何将分析扩展到更大规模模型（如 7B、70B 参数）和更复杂的推理任务（如数学推理、代码生成）？大模型的隐藏状态可能包含更丰富的规划信号，但也对压缩质量提出更高要求。

2. **MTP 训练的最优配置**：MTP 训练在多大程度上能促进长期规划？其最优超参数（如预测视野 Γ）如何随任务性质变化？本文仅在固定 Γ 下进行了初步探索。

3. **架构改进**：能否通过修改架构（如引入显式记忆模块、循环连接）来增强模型的规划能力？本文的分析框架可以作为评估此类改进的诊断工具。

4. **思维链下的规划动态**：在 Chain-of-Thought 等逐步推理策略下，内部规划视野和分支意识如何动态变化？模型是否在生成中间步骤时重新规划？

5. **从诊断到改进**：如何将发现的内部表征特征（如分支意识、规划视野）用于改进模型训练或解释性？例如，能否通过正则化鼓励更长的规划视野？

## 原文 PDF

![[paperPDFs/ICLR_2026/Internal_Planning_in_Language_Models_Characterizing_Horizon_and_Branch_Awareness.pdf]]
