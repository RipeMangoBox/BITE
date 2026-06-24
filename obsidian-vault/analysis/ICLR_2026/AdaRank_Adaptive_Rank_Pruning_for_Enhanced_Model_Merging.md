---
title: "AdaRank: Adaptive Rank Pruning for Enhanced Model Merging"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging.pdf
openreview_forum_id: fTygcJVOni
aliases:
- AARP
- AARPEMM
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "对每个任务向量的每个奇异成分是否保留进行自适应二值决策（即学习一组二值掩码B）。"
primary_logic: "通过测试时适应（TTA）和熵最小化作为无监督代理目标，学习一组二值掩码，动态选择那些在减少自身任务损失的同时最小化跨任务干扰的奇异成分，从而突破固定前k选择的局限性。"
claims:
- "顶部的奇异成分虽然能大幅降低自身任务损失，但会显著增加其他任务的损失，导致多任务净损失上升。"
- "不同任务和网络层的固有秩（保留95%谱能量所需的成分数）差异巨大，SUN397的秩远高于MNIST，且深层比浅层秩低、变异性大。"
- "AdaRank在多种骨干网络（ViT-B/32, ViT-L/14, RoBERTa, GPT-2）和合并方法（TA, CART, TSV-M）上均能一致提升性能，平均提升最高达18.6%。"
- "8 Vision Tasks (ViT-B/32) 上 平均准确率 = TA+AdaRank: 87.9, TSV-M+AdaRank: 88.9, CART+AdaRank: 89.2"
---

# AdaRank: Adaptive Rank Pruning for Enhanced Model Merging

> [!tip] 核心洞察
> 通过测试时适应（TTA）和熵最小化作为无监督代理目标，学习一组二值掩码，动态选择那些在减少自身任务损失的同时最小化跨任务干扰的奇异成分，从而突破固定前k选择的局限性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AdaRank：面向增强模型合并的自适应秩剪枝 |
| 英文题名 | AdaRank: Adaptive Rank Pruning for Enhanced Model Merging |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fTygcJVOni) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | AdaRank (Adaptive Rank Pruning) |
| Dataset | 8 Vision Tasks (ViT-B/32), 8 Vision Tasks (ViT-L/14), 7 NLP Tasks (RoBERTa) |

> [!tip] 效果简介
> - 8 Vision Tasks (ViT-B/32) 上，平均准确率 为 TA+AdaRank: 87.9, TSV-M+AdaRank: 88.9, CART+AdaRank: 89.2，对比 TA: 69.2, TSV-M: 84.7, CART: 85.9，变化 TA+AdaRank提升18.7%, TSV-M+AdaRank提升4.2%, CART+AdaRank提升3.3%。
> - 8 Vision Tasks (ViT-L/14) 上，平均准确率 为 TA+AdaRank: 93.0, TSV-M+AdaRank: 93.7, CART+AdaRank: 93.5，对比 TA: 84.5, TSV-M: 91.2, CART: 92.5，变化 TA+AdaRank提升8.5%, TSV-M+AdaRank提升2.5%, CART+AdaRank提升~1%。
> - 7 NLP Tasks (RoBERTa) 上，平均性能 为 TA+AdaRank: 0.7032, TSV-M+AdaRank: 0.7309, CART+AdaRank: 0.7547，对比 TA: 0.6718, TSV-M: 0.6693, CART: 0.6997，变化 CART+AdaRank提升5.5%。

## 概述

模型合并旨在将多个针对不同任务微调的模型整合为一个统一的多任务模型，而无需原始训练数据。现有的基于奇异值分解（SVD）的合并方法采用启发式的前k个奇异成分选择策略（top-k），但这一做法存在两个根本性瓶颈：

1. **跨任务干扰**：顶部的奇异成分虽然能显著降低自身任务的损失，却会大幅增加其他任务的损失，导致多任务净损失不降反升（见Figure 1）。
2. **秩需求差异**：不同任务和网络层对秩的需求存在显著差异——例如SUN397的固有秩远高于MNIST，且深层比浅层秩更低、变异性更大（见Figure 2）。固定的top-k截断无法适应这种多样性。

针对上述问题，本文提出**AdaRank（Adaptive Rank Pruning）**，一种自适应秩剪枝框架。其核心思想是：为每个任务向量的每个奇异成分学习一个二值掩码，通过测试时适应（TTA）和熵最小化作为无监督代理目标，动态选择那些在减少自身任务损失的同时最小化跨任务干扰的奇异成分，从而突破固定前k选择的局限性。

实验表明，AdaRank在多种骨干网络（ViT-B/32、ViT-L/14、RoBERTa、GPT-2）和合并方法（TA、CART、TSV-M）上均能一致提升性能——在ViT-B/32的8个视觉任务上，TA+AdaRank相较TA提升高达18.7%；在RoBERTa的7个NLP任务上，CART+AdaRank相较CART提升5.5%。同时，AdaRank仅需1%的测试数据即可超越使用全量测试数据的AdaMerging，展现出良好的数据效率。

## 背景与动机

### 模型合并中的秩选择困境

多任务模型合并的核心操作是将多个针对不同下游任务微调的模型融合为一个统一的模型，而无需原始训练数据。以任务算术（Task Arithmetic, TA）为代表的经典方法将合并过程形式化为：

$$\theta_m^l = \theta_0^l + \lambda^l \sum_{i=1}^T \tau_i^l$$

其中 $\theta_0^l$ 为预训练参数，$\tau_i^l$ 为第 $i$ 个任务的任务向量（微调权重与预训练权重之差），$\lambda^l$ 为缩放系数。为进一步减少参数冗余和跨任务干扰，基于奇异值分解（SVD）的方法（如 CART、TSV-M）引入低秩近似，仅保留每个任务向量的前 $k$ 个奇异成分：

$$\theta_m^l = \theta_0^l + \lambda^l \sum_{i=1}^T \mathrm{SVD}_k(\tau_i^l)$$

然而，这种**启发式的前 $k$ 选择策略**（top-$k$）构成了当前方法的核心瓶颈。

### 前 $k$ 选择的双重缺陷

**缺陷一：顶部奇异成分引入严重的跨任务干扰。** 图 1 的可视化分析揭示了这一反直觉现象：当将一个目标任务向量的各奇异成分逐一添加到一个已由其他任务全秩合并的模型中时，顶部的奇异成分（即奇异值最大的成分）虽然能大幅降低该目标任务的损失，但同时也会显著增加其他任务的损失。综合来看，**前 $k$ 个成分带来的单任务收益被跨任务干扰所抵消，导致多任务净损失反而上升**。这一现象在 Task Arithmetic 和 CART 两种合并框架下均被观察到，说明问题根植于 top-$k$ 选择策略本身，而非特定合并方法。

**缺陷二：不同任务和网络层对秩的需求存在显著差异。** 图 2 测量了 ViT-B/32 在不同任务上微调后，任务向量各层达到 95% 谱能量所需的固有秩（intrinsic rank）。结果显示，不同任务之间的秩需求差异巨大——例如 SUN397 的固有秩远高于 MNIST；同时，同一模型的不同层之间也存在明显变异，深层（如最后一个 block）的秩普遍低于浅层（如第一个 block），且变异性更大。固定的 top-$k$ 截断无法适应这种任务间和层间的多样性：对某些任务/层而言，$k$ 可能过大（保留了干扰成分），对另一些则可能过小（丢失了有益成分）。

### 现有自适应方法的局限

AdaMerging 等方法通过测试时适应（Test-Time Adaptation, TTA）以熵最小化为目标来调节合并系数 $\lambda$，在一定程度上缓解了静态合并的不足。然而，这类方法仅调整各任务向量的全局缩放权重，并未触及**奇异成分级别的细粒度选择**——即无法区分同一任务向量内部哪些成分有益、哪些有害。这使得它们在面对前述的“顶部成分干扰”问题时，缺乏足够的干预手段。

### 本文动机

上述分析表明，突破现有方法瓶颈的关键在于：**用自适应的成分级选择取代启发式的前 $k$ 截断**。这一选择需要同时满足两个条件：（1）保留那些在降低自身任务损失的同时不显著损害其他任务的奇异成分；（2）根据不同任务和网络层的特性动态调整保留成分的数量。这构成了 AdaRank 方法的核心动机——通过学习一组二值掩码，对每个任务向量的每个奇异成分做出保留或剪枝的自适应决策。

## 核心创新

AdaRank 的核心创新在于将现有 SVD 基模型合并方法中**固定的、启发式的前 k 个奇异成分选择（top-k）**，替换为**自适应的、可学习的二值掩码选择机制**。这一转变直接回应了现有方法的两个关键瓶颈：

1. **跨任务干扰问题**：前 k 个奇异成分虽然能大幅降低自身任务损失，但同时会显著增加其他任务的损失，导致多任务净损失上升（Figure 1）。固定 top-k 策略无法区分“对自身有益”与“对他人有害”的成分。

2. **秩需求的异质性**：不同任务和网络层对秩的需求存在显著差异——SUN397 的固有秩远高于 MNIST，且深层比浅层秩更低、变异性更大（Figure 2）。统一的截断比例无法适应这种多样性。

### 核心机制：自适应二值掩码

AdaRank 为每个任务向量 $i$ 的每一层 $l$ 的每个奇异成分引入一个二值掩码 $B_i^l \in \{0,1\}$，直接决定该成分是保留（1）还是剪枝（0）。合并后的模型参数为：

$$\theta^l(B^l) = \theta_0^l + \lambda^l \sum_{i=1}^T U_i^l (\mathrm{diag}(B_i^l) \odot \Sigma_i^l) V_i^{l\top}$$

该掩码通过**测试时适应（TTA）** 在无标签测试数据上优化，优化目标为最小化所有任务输出熵之和：

$$\underset{B}{\operatorname{argmin}} \sum_{i=1}^T \sum_{x_i \in \mathcal{D}_i} H_i(f(\theta(B), x_i))$$

掩码的离散优化使用 Straight-Through Estimator（STE）：前向传播时通过 sigmoid 阈值化得到二值掩码 $b_i^l = \mathbf{1}\{\sigma(\tilde{b}_i^l / T) \geq 0.5\}$，反向传播时保留连续梯度。

### 与 baseline 的关键差异

| 设计维度 | 现有方法（top-k） | AdaRank |
|---------|-----------------|---------|
| 成分选择策略 | 固定比例截断（如前 16%）或全保留 | 每任务每层学习二值掩码，自适应选择 |
| 优化目标 | 无优化（静态合并）或仅调节系数 $\lambda$ | 熵最小化同时优化 $\lambda$ 和 $B$ |
| 干扰感知 | 无，统一截断忽略跨任务影响 | 通过 TTA 隐式感知并减少跨任务干扰 |

消融实验证实了这一设计的有效性：仅学习二值掩码 $B$（不调节 $\lambda$）已能获得与调节系数相当的改善（Table 6），表明**成分选择本身是关键杠杆**。此外，AdaRank 仅需 1% 的测试数据即可超越使用全量测试数据的 AdaMerging（Table 7），展示了良好的数据效率。

## 整体框架

![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/001_Figure_1.jpg]]
*Figure 1: (a), (b) Net change in single-task and multi-task losses for Task Arithmetic (Ilharco et al., 2023) and CART (Choi et al., 2024), respectively, when each singular component of a target task vector is individually added to a model merged with full-rank vectors from other tasks. (c) Loss changes of all tasks when adding singular components from the MNIST task vector, with MNIST shown as a dotted line. For clarity, only the top 10% of singular components are shown*

![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/002_Figure_2.jpg]]
*Figure 2: Intrinsic rank capturing 95% of total spectral energy in the MLP layer of the first and the last block of ViT-B/32 task vectors obtained from 8 different fine-tuned weights*

AdaRank 的核心思路是将基于 SVD 的模型合并中的启发式秩选择，替换为可学习的自适应二值掩码决策。其整体 pipeline 由四个模块串联构成：SVD 分解、二值掩码初始化与参数化、合并模型构造、测试时适应（TTA）。

**SVD 分解。** 给定 $T$ 个任务，每个任务 $i$ 的微调权重与预训练权重之差构成任务向量 $\tau_i$。对每一层的每个任务向量进行奇异值分解，得到 $U_i^l$、$\Sigma_i^l$、$V_i^l$。这一步是静态的预处理，为后续自适应选择提供候选的奇异成分池。

**二值掩码初始化与参数化。** 为每个任务 $i$ 的每一层 $l$ 的每个奇异成分引入一个连续参数 $\tilde{b}_{ir}^l$，通过 sigmoid 函数和温度参数 $T$ 映射到 $(0,1)$，再以 0.5 为阈值二值化得到掩码 $b_{ir}^l = \mathbf{1}\{\sigma(\tilde{b}_{ir}^l / T) \geq 0.5\}$。前向传播使用离散的 $\{0,1\}$ 掩码，反向传播通过 Straight-Through Estimator（STE）保持连续梯度流。这些掩码参数是 AdaRank 唯一新增的可学习变量，约占模型总参数量的 0.032%。

**合并模型构造。** 根据当前二值掩码 $B_i^l$，合并后的第 $l$ 层参数为：

$$\theta^l(B^l) = \theta_0^l + \lambda^l \sum_{i=1}^T U_i^l (\text{diag}(B_i^l) \odot \Sigma_i^l) V_i^{l\top}$$

其中 $\lambda^l$ 为层级别的合并系数。当 $B_{ir}^l = 1$ 时，第 $r$ 个奇异成分被保留；$B_{ir}^l = 0$ 时被剪枝。这与传统 top-$k$ 截断的本质区别在于：选择是逐任务、逐层、逐成分自适应决策的，而非全局统一的固定截断。

**测试时适应（TTA）。** 掩码 $B$ 和系数 $\lambda$ 通过无标签测试数据联合优化，目标是最小化所有任务输出熵之和：

$$\underset{B}{\operatorname{argmin}} \sum_{i=1}^T \sum_{x_i \in \mathcal{D}_i} H_i(f(\theta(B), x_i))$$

熵最小化作为无监督代理目标，避免了直接使用交叉熵需要标签的限制。优化完成后，得到最终的二值掩码 $\breve{B}$，代入合并公式生成最终的多任务模型。

整个 pipeline 的输入是预训练权重 $\theta_0$ 和各任务向量 $\tau_i$ 的 SVD 分解结果，输出是经过自适应秩剪枝的合并模型 $\theta(\breve{B})$。关键因果机制在于：TTA 通过熵最小化隐式地识别出那些降低自身任务损失同时不显著增加跨任务干扰的奇异成分，从而突破固定 top-$k$ 选择的瓶颈（该瓶颈的实证证据见 Figure 1 和 Figure 2 的分析）。

## 核心模块与公式推导

### 问题形式化

给定 $T$ 个针对不同下游任务微调的模型，每个任务 $i$ 在第 $l$ 层的任务向量定义为微调权重与预训练权重的差值：$\tau_i^l = \theta_i^l - \theta_0^l$。基于奇异值分解（SVD）的模型合并方法将每个任务向量分解为 $\tau_i^l = U_i^l \Sigma_i^l V_i^{l\top}$，并通过保留前 $k$ 个奇异成分构建低秩近似，合并公式为：

$$\theta_m^l = \theta_0^l + \lambda^l \sum_{i=1}^T \mathrm{SVD}_k(\tau_i^l)$$

其中 $\mathrm{SVD}_k(\cdot)$ 表示仅保留前 $k$ 个奇异值及对应奇异向量的截断操作。这种启发式的固定 top-k 选择存在两个根本缺陷：顶部奇异成分虽有利于自身任务，却会引入严重的跨任务干扰；不同任务和网络层对秩的需求差异显著，固定截断无法适应这种多样性。

### AdaRank 核心机制

AdaRank 将固定的 top-k 截断替换为自适应二值掩码选择。对每一层 $l$ 和每个任务 $i$，引入二值掩码向量 $B_i^l \in \{0,1\}^{1 \times m}$，其中 $m$ 为奇异成分总数。掩码的每个元素决定对应奇异成分是保留（1）还是剪枝（0）。合并后的模型参数表示为：

$$\theta^l(B^l) = \theta_0^l + \lambda^l \sum_{i=1}^T U_i^l \left(\mathrm{diag}(B_i^l) \odot \Sigma_i^l\right) V_i^{l\top}$$

其中 $\mathrm{diag}(B_i^l)$ 将二值掩码向量展开为对角矩阵，$\odot$ 表示逐元素乘积。该公式的因果机制是：通过二值掩码对奇异谱进行选择性过滤，保留那些在降低自身任务损失的同时最小化跨任务干扰的奇异成分，从而突破固定 top-k 选择的性能瓶颈。

### 测试时适应优化

掩码 $B$ 的优化采用测试时适应（TTA）框架，以无标签测试数据上的香农熵最小化作为无监督代理目标：

$$\underset{B}{\operatorname{argmin}} \sum_{i=1}^T \sum_{x_i \in \mathcal{D}_i} H_i\left(f(\theta(B), x_i)\right)$$

其中 $\mathcal{D}_i$ 为任务 $i$ 的无标签测试数据，$H_i(\cdot)$ 为模型输出概率分布的香农熵。该目标无需训练标签，通过最小化合并模型在测试数据上的预测不确定性来间接优化跨任务干扰。

### 二值掩码的参数化与梯度估计

由于二值掩码不可微，AdaRank 采用 Straight-Through Estimator（STE）进行优化。每个掩码元素对应一个连续参数 $\tilde{b}$，前向传播时通过 sigmoid 函数和阈值生成二值掩码：

$$b_i^l = \mathbf{1}\{\sigma(\tilde{b}_i^l / T) \geq 0.5\}$$

其中 $T$ 为温度参数，$\sigma$ 为 sigmoid 函数。前向传播使用四舍五入后的二值，反向传播时则绕过取整操作，直接将连续值的梯度传递给 $\tilde{b}$。优化完成后，最终的二值掩码 $\breve{B}_i^l$ 被固化并应用于合并公式。

### 与基线方法的关键差异

| 方法 | 奇异成分选择策略 | 优化目标 |
|------|-----------------|---------|
| Task Arithmetic (TA) | 全部保留（无截断） | 无优化（静态合并） |
| TIES-Merging | 基于幅值的静态剪枝 | 无优化 |
| CART / TSV-M | 固定 top-k 截断 | 无优化 |
| AdaMerging | 全部保留 | TTA + 熵最小化（仅调节 $\lambda$） |
| **AdaRank** | **自适应二值掩码 $B$** | **TTA + 熵最小化（联合优化 $\lambda$ 和 $B$）** |

核心差异在于：AdaRank 将选择权从固定的启发式规则转移到了数据驱动的自适应学习过程，使每个任务、每一层的每个奇异成分都能根据其对多任务损失的净贡献独立决策保留或剪枝。

## 实验与分析

### 核心瓶颈的实证验证

在提出方法之前，作者通过两个关键实验揭示了现有基于SVD的top-k截断策略的根本缺陷。

**顶部奇异成分的干扰效应。** 图1(a)和(b)分别展示了在Task Arithmetic和CART框架下，向已合并其他任务全秩向量的模型中逐个添加目标任务的奇异成分时，单任务损失与多任务损失的变化。结果表明：顶部奇异成分虽然能大幅降低自身任务的损失，但同时会显著增加其他任务的损失，导致多任务净损失上升。图1(c)以MNIST任务向量为例进一步分解了逐任务损失变化——添加MNIST的顶部奇异成分对SVHN有正面影响，却对DTD等不相似任务造成明显干扰。这一发现直接动摇了“保留前k个最大奇异值成分”这一启发式策略的合理性。

**固有秩的跨任务与跨层异质性。** 图2统计了ViT-B/32在8个不同任务上微调后，MLP层中保留95%谱能量所需的最少奇异成分数（即固有秩）。结果显示：SUN397的固有秩远高于MNIST；同一任务内，浅层（首个Transformer Block）的固有秩普遍高于深层（最后一个Block），且深层秩的跨任务变异性更大。这意味着固定的top-k截断无法适配不同任务和网络层对秩的差异化需求。

### 主要实验结果

#### 视觉任务合并

表1汇总了在8、14、20个视觉任务上合并ViT-B/32和ViT-L/14的平均准确率。AdaRank在所有基础合并方法上均带来一致且显著的提升：


![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/003_Table_1.jpg]]
*Table 1: Average accuracy along 8, 14, 20 vision tasks with merged ViT-B/32 and ViT-L/14*

- **ViT-B/32 (8任务)**：TA+AdaRank达到87.9%，相比TA的69.2%提升18.7个百分点；CART+AdaRank达到89.2%，相比CART的85.9%提升3.3个百分点；TSV-M+AdaRank达到88.9%，相比TSV-M的84.7%提升4.2个百分点。
- **ViT-L/14 (8任务)**：TA+AdaRank达到93.0%（+8.5个百分点），TSV-M+AdaRank达到93.7%（+2.5个百分点），CART+AdaRank达到93.5%（+1.0个百分点）。
- 随着任务数量增加至14和20，AdaRank的优势依然保持，且在与基于路由器的合并方法（如Twin-Merging、WEMoE）对比时仍展现出竞争力（表3）。

#### NLP任务合并

表2展示了在7个NLP任务上合并RoBERTa和GPT-2的结果。AdaRank同样表现出跨架构的泛化能力：


![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/004_Table_2.jpg]]
*Table 2: Average performance on 7 NLP tasks with merged RoBERTa and GPT-2*

- **RoBERTa**：CART+AdaRank达到0.7547，相比CART的0.6997提升5.5%；TSV-M+AdaRank达到0.7309，相比TSV-M的0.6693提升6.2个百分点。
- **GPT-2**：TSV-M+AdaRank达到0.6743，CART+AdaRank达到0.6587，均优于各自基础方法及AdaMerging变体。

#### 计算效率分析

表4对比了AdaRank与AdaMerging在ViT-B/32和ViT-L/14上的可学习参数量和TTA耗时。AdaRank引入的可学习参数约29.5万（占模型总参数的约0.032%），TTA时间约10.7分钟，与AdaMerging的10.3分钟基本持平，但性能从80.1%跃升至87.9%。额外的SVD分解仅需执行一次，其时间开销远小于TTA迭代过程。

### 消融实验

**奇异成分选择范围的影响。** 表5的消融表明，仅在top-16%截断范围内应用AdaRank（即对前k个成分做自适应选择，其余强制置零）已带来显著提升（TA: 87.5 vs. 84.7），而全范围应用AdaRank进一步获得增益（87.9）。这说明自适应选择既能优化已被截断保留的成分，也能从被传统方法丢弃的底部成分中挖掘有用信息。

**可学习组件的贡献分解。** 表6分别考察了仅学习系数λ、仅学习二值掩码B、以及联合学习两者的效果。仅学习B时TA达到79.9%，已与仅学习λ的80.1%相当，表明奇异成分的自适应选择本身就是关键驱动因素；联合学习两者达到87.9%，验证了成分选择与系数调节的协同效应。

**测试数据量的鲁棒性。** 表7显示，AdaRank仅使用1%的测试数据即可达到81.2%（TA），超越了使用全量测试数据的AdaMerging（80.1%）。随着数据量增加，性能单调提升，使用全量数据时达到87.9%。这一数据效率优势在NLP任务上同样得到验证（表10）。

### 深入分析

**学习到的秩分布。** 图4(a)统计了AdaRank在8个任务上累积选择的奇异成分索引分布。黑色虚线标记了top-16%的截断边界——大量被选中的成分位于该边界之外，证实了固定top-k截断会丢弃有价值的底部成分。图4(b)将学习到的掩码秩与各层固有秩进行对比，发现AdaRank倾向于在固有秩较高的浅层保留更多成分，在深层则更激进地剪枝，展现出对层间异质性的自适应能力。图4(c)进一步表明，基于固有秩的top-k截断性能不如AdaRank，说明仅凭谱能量保留比例不足以确定最优秩。


![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/010_Figure_4.jpg]]
*Figure 4: (a) Count of singular component indices selected by AdaRank, cumulated along 8 tasks. The black dashed line denotes the top-16% limit. (b) Comparison of ranks obtained from final masks after applying AdaRank, against the intrinsic rank for the MLP layers in the first (left) and last (right) blocks of ViT-B/32. (c) Performance comparison between merged model with top-k truncation based on intrinsic rank and AdaRank (y-axis clipped for better visualization)*

**优化过程的动态分析。** 图5以交叉熵损失为纵坐标，展示了从top-16%截断初始化出发，AdaRank（基于熵最小化）与oracle（基于真实标签的交叉熵）以及固定top-k基线在优化过程中的损失变化。AdaRank的损失下降轨迹与oracle高度一致，验证了熵最小化作为无监督代理目标的有效性；而固定top-k基线的损失始终高于两者，无法通过TTA迭代改善。


![[assets/figures/papers/paper_list_l4_AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging/figures/011_Figure_5.jpg]]
*Figure 5: Cross-entropy loss during the optimization of B initialized from top-16% truncation (black line). We compare optimizing AdaRank with cross-entropy loss to directly minimize the multi-task loss (blue curve) and entropy as surrogate loss (orange curve)*

### 失败模式与局限性

尽管AdaRank在多个基准上表现优异，仍需注意以下局限：

1. **对SVD分解的依赖**：方法要求对每个任务向量进行完整的SVD分解。对于参数规模极大的模型，SVD本身的计算和存储开销可能成为瓶颈，尽管实验表明该开销远小于TTA迭代。
2. **测试数据的必要性**：TTA范式需要无标签测试数据。在完全缺乏测试数据的零样本场景下，AdaRank无法直接应用；但实验已证明仅需极少测试数据（1%）即可取得有竞争力的结果。
3. **任务类型覆盖有限**：当前验证集中在图像分类和文本分类任务上，尚未在生成式任务、目标检测等更多样化的场景中进行评估。
## 方法谱系与知识库定位

### 在模型合并方法谱系中的位置

AdaRank 处于基于奇异值分解（SVD）的模型合并方法与测试时适应（TTA）方法的交叉点。模型合并的核心目标是将多个针对不同任务微调的模型整合为单一模型，无需访问原始训练数据。现有方法可按合并策略分为以下几类：

**静态合并方法**构成了该领域的基础。Task Arithmetic（TA）直接将缩放后的任务向量相加：$\theta_m^l = \theta_0^l + \lambda^l \sum_{i=1}^T \tau_i^l$。TIES-Merging 在此基础上引入基于幅值的静态剪枝，通过元素级掩码 $M_i \odot \tau_i$ 截断低幅值参数。CART 和 TSV-M 则进一步利用 SVD 的低秩结构，将合并公式改写为 $\theta_m^l = \theta_0^l + \lambda^l \sum_{i=1}^T \mathrm{SVD}_k(\tau_i^l)$，即仅保留每个任务向量的前 $k$ 个奇异成分。这些方法的共同瓶颈在于采用固定的启发式选择策略——要么全部保留，要么按固定比例（如 top-16%）截断，无法适应不同任务和网络层对秩的差异化需求（Figure 2 显示 SUN397 的固有秩远高于 MNIST，且深层比浅层秩低、变异性大）。

**自适应合并方法**试图通过引入可学习参数来突破静态限制。AdaMerging 是这一方向的代表性工作，它通过 TTA 和熵最小化学习任务级或层级缩放系数 $\lambda$，但不涉及对任务向量内部结构的自适应选择。Consensus Merging 和 Twin-Merging 则分别采用基于一致性的掩码和基于路由器的低秩合并策略。AdaRank 的直接前身是 AdaMerging，但二者存在本质差异：AdaMerging 仅调节任务向量的整体缩放系数，而 AdaRank 深入到每个任务向量的奇异成分层面，为每个成分学习一个二值掩码 $B_i^l$，通过 $\theta^l(B^l) = \theta_0^l + \lambda^l \sum_{i=1}^T U_i^l (\mathrm{diag}(B_i^l) \odot \Sigma_i^l) V_i^{l\top}$ 实现成分级的选择性保留或剪枝。这一差异的因果效应在 Table 1 中得到了清晰验证：TA+AdaRank 在 ViT-B/32 8 任务上达到 87.9%，而 TA+AdaMerging 仅为 80.1%，差距达 7.8 个百分点。

**基于专家混合（MoE）的方法**如 WEMoE，通过引入路由器动态组合不同任务的参数，通常需要额外的模型结构和显著更多的参数。与之相比，AdaRank 不改变合并模型的结构，仅引入约 0.032% 的可学习参数（Table 4），在保持参数效率的同时获得了竞争力的性能。

### 适用边界与前提条件

AdaRank 的有效运行依赖于以下前提条件：

1. **SVD 可分解性**：方法要求对每个任务向量进行完整的 SVD 分解。对于参数量极大的模型（如数百亿参数的 LLM），这一步骤的计算和存储开销可能成为瓶颈。虽然论文指出 SVD 时间相对 TTA 较短，但该结论仅在 ViT-B/32 和 ViT-L/14 规模上得到验证。

2. **无标签测试数据的可用性**：TTA 阶段需要无标签测试数据来最小化熵目标 $\underset{B}{\operatorname{argmin}} \sum_{i=1}^T \sum_{x_i \in \mathcal{D}_i} H_i(f(\theta(B), x_i))$。在完全缺乏测试数据的零样本场景下，该方法无法直接应用。不过 Table 7 显示，仅使用 1% 的测试数据，AdaRank 已能超越使用全量测试数据的 AdaMerging，表明数据需求可大幅降低。

3. **任务向量的低秩假设**：方法的核心动机建立在任务向量具有低秩结构的前提上（Figure 2 的谱能量分析）。对于秩极高的任务向量，自适应选择的收益可能有限，因为大部分成分都需要保留。

4. **任务间存在干扰**：AdaRank 的收益来源于对跨任务干扰的缓解。如果任务之间高度兼容（即添加任何成分都不会增加其他任务的损失），自适应选择退化为全保留，此时 AdaRank 与无截断的 TA 等价，不带来额外收益。

### 已识别的局限性

1. **计算开销与可扩展性**：尽管 Table 4 显示 AdaRank 的 TTA 时间（约 10.7 分钟）与 AdaMerging（约 10.3 分钟）相当，但额外的 SVD 步骤和更多的可学习参数（294,912 vs 2,440）在更大规模模型上可能成为瓶颈。论文未在超过 ViT-L/14 规模的模型上进行验证。

2. **任务类型覆盖有限**：当前实验仅限于图像分类（8/14/20 视觉任务）和文本分类（7 个 NLP 任务）。尚未在生成任务、目标检测、语义分割等更多样化的任务类型上进行验证。Figure 6 虽然展示了 RoBERTa 和 GPT-2 上的损失变化模式，但并未系统评估 AdaRank 在生成质量指标上的表现。

3. **熵最小化作为代理目标的保真度**：Figure 5 显示，以熵最小化为目标的 AdaRank（橙色曲线）在优化过程中能有效降低多任务交叉熵损失，但其下降曲线与直接最小化交叉熵的 Oracle（蓝色曲线）之间仍存在差距。这表明熵最小化并非完美的代理目标，在某些分布偏移较大的场景下可能导致次优选择。

4. **二值掩码的离散优化**：使用 Straight-Through Estimator（STE）处理二值掩码的离散性是一种近似方法，理论上存在梯度偏差。论文未讨论 STE 的近似误差对最终掩码质量的影响。

### 开放问题与未来方向

1. **零样本自适应秩选择**：如何在完全无测试数据的场景下进行自适应的秩选择？可能的路径包括利用预训练模型的内部表征或任务向量本身的结构信息来预测有益成分，而不依赖外部数据。

2. **跨参数高效微调方法的扩展**：自适应秩选择的思想是否能扩展到 LoRA 等低秩适配器方法中？LoRA 本身已经具有低秩结构，但不同 LoRA 模块之间的合并同样面临类似的任务干扰问题，自适应选择哪些秩成分参与合并可能是一个自然延伸。

3. **干扰上界的理论分析**：能否通过理论分析量化自适应选择带来的跨任务干扰降低？当前论文主要依赖经验证据（Figure 1 的损失变化曲线），缺乏对干扰上界的严格数学刻画。

4. **与动态路由方法的深度融合**：AdaRank 当前与基于路由器的合并方法（如 Twin-Merging）是独立比较的（Table 3）。将成分级自适应选择与任务级动态路由相结合，可能进一步突破性能上限。

5. **大规模模型上的验证**：在数十亿参数级别的模型上验证 AdaRank 的可扩展性，并探索更高效的 SVD 近似方法（如随机化 SVD）以降低计算开销。

## 原文 PDF

![[paperPDFs/ICLR_2026/AdaRank_Adaptive_Rank_Pruning_for_Enhanced_Model_Merging.pdf]]
