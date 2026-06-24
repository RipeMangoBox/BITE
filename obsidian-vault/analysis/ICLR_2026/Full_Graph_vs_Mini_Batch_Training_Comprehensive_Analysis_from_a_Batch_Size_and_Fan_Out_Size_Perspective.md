---
title: "Full-Graph vs. Mini-Batch Training: Comprehensive Analysis from a Batch Size and Fan-Out Size Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Full_Graph_vs_Mini_Batch_Training_Comprehensive_Analysis_from_a_Batch_Size_and_Fan_Out_Size_Perspective.pdf
aliases:
- SCAF
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability
core_operator: "批次大小 b 与扇出大小 β，它们在全图训练中分别取最大值（n_train 和 d_max），而在迷你批次训练中可自由调节，从而控制训练动态与最终性能。"
primary_logic: "全图训练并非始终优于精心调参的迷你批次训练。批次大小对收敛趋势的影响依赖损失函数（MSE下增大批次需要更多迭代，CE下则相反），而扇出大小对泛化的影响更显著且存在非单调波动。在内存约束下，为加速收敛应优先调节扇出大小，为提升泛化应优先调节批次大小。"
claims:
- "增大扇出大小在 MSE 和 CE 下均一致减少收敛所需迭代数，而增大批次大小在 MSE 下增加迭代数、在 CE 下减少迭代数。"
- "泛化间隙可由 Wasserstein 距离界定，扇出大小通过减少 mini-batch 与 full-graph 的结构差异来提升泛化，且其影响较批次大小更敏感。"
- "在三个数据集上，精心调节的迷你批次训练取得了优于或接近全图训练的测试精度（例如 Reddit 96.32 vs 96.13），验证了全图并非总是最优。"
- "迭代至精度指标在不同硬件环境下变化远小于时间至精度指标（41.28% vs 2787.05%），支持了硬件无关的公平比较。"
---

# Full-Graph vs. Mini-Batch Training: Comprehensive Analysis from a Batch Size and Fan-Out Size Perspective

> [!tip] 核心洞察
> 全图训练并非始终优于精心调参的迷你批次训练。批次大小对收敛趋势的影响依赖损失函数（MSE下增大批次需要更多迭代，CE下则相反），而扇出大小对泛化的影响更显著且存在非单调波动。在内存约束下，为加速收敛应优先调节扇出大小，为提升泛化应优先调节批次大小。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 全图训练与迷你批次训练：基于批次大小和扇出大小的综合分析 |
| 英文题名 | Full-Graph vs. Mini-Batch Training: Comprehensive Analysis from a Batch Size and Fan-Out Size Perspective |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZSfgsh43vT); [GitHub](https://github.com/LIUMENGFAN-gif/GNN_fullgraph_minibatch_training) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability |
| Method | 全图与迷你批次训练系统分析框架 (Systematic Comparative Analysis Framework) |
| Dataset | Reddit, ogbn-arxiv, ogbn-products, ogbn-papers100M |

> [!tip] 效果简介
> - Reddit 上，Test Accuracy (%) 为 96.32，对比 96.13，变化 +0.19。
> - ogbn-arxiv 上，Test Accuracy (%) 为 71.16，对比 70.96，变化 +0.20。
> - ogbn-products 上，Test Accuracy (%) 为 78.80，对比 77.92，变化 +0.88。

## 概述

图神经网络（GNN）的训练通常面临全图训练与迷你批次训练两种范式的选择。全图训练利用完整的图结构和所有训练节点进行梯度下降，而迷你批次训练通过对邻居采样构建子图并使用随机梯度下降，其行为受**批次大小**（$b$）和**扇出大小**（$\beta$）两个关键参数控制。然而，这两个参数如何影响训练动态、泛化能力以及计算效率，一直缺乏系统的理论理解，导致在资源受限的实际场景中难以做出有理论指导的最优决策。

该论文从批次大小与扇出大小的视角，对全图训练和迷你批次训练进行了系统性的理论分析与实验比较。作者首先将两种范式统一在同一分析框架下：全图训练可视为 $b=n_{\mathrm{train}}$（所有训练节点）且 $\beta=d_{\max}$（聚合全部邻居）的极端情形，而迷你批次训练则允许自由调节 $b$ 和 $\beta$，从而可控地改变训练动态与最终性能。

核心洞察是：**全图训练并不总是优于精心调参的迷你批次训练**。批次大小对收敛趋势的影响依赖于损失函数——在均方误差（MSE）损失下增加 $b$ 会导致需要更多的迭代才能收敛，而在交叉熵（CE）损失下增加 $b$ 反而减少迭代次数。相比之下，增大扇出大小在两种损失下均一致地加速收敛，且其对泛化性能的影响更为显著，但可能表现出非单调波动。因此，在内存预算有限时，为加快收敛应优先增大扇出大小，而为提升泛化能力则应优先增大批次大小。

理论上，该工作给出了迷你批次训练在 MSE 与 CE 下的迭代复杂度上界（Theorem 1 和 Theorem 2），并利用 Wasserstein 距离构建了泛化间隙的上界（Theorem 3），从而从优化和泛化两个层面揭示了 $b$ 与 $\beta$ 的作用机理。实验上，作者在 Reddit、ogbn-arxiv、ogbn-products 等大规模图数据集上验证了理论推断，证明精心调节的迷你批次训练能够达到甚至超过全图训练的测试精度（如 Reddit 上 96.32% vs 96.13%），同时采用与硬件无关的“迭代至精度”指标保证公平比较。

整体而言，该论文构建了一个理解 GNN 训练中批次与扇出大小作用的分析框架，为实践中在收敛速度、泛化能力与资源效率之间进行权衡提供了明确的理论指导。其分析主要面向单层 ReLU GNN 和直推式节点分类任务，并指出了向多层模型、其他激活函数及异构图的推广方向，为后续研究留下了开放问题。

## 背景与动机

图神经网络（GNN）的训练范式选择一直存在核心张力：全图训练利用完整图结构与全部训练节点进行优化，理论上可捕获最丰富的结构信息；迷你批次训练则通过子图采样降低内存与计算开销，使大规模图上的训练成为可能。然而，何时应使用全图训练、何时应采用迷你批次训练，以及对两者内在差异的理解，仍主要依赖经验直觉，缺乏系统性的理论指导。这一缺口源于两个关键控制变量——批次大小（batch size, $b$）与扇出大小（fan-out size, $\beta$）——对训练动态、泛化能力和计算效率的影响未被充分认知。在全图训练中，$b$ 取所有训练节点数量，$\beta$ 取节点的最大邻居度；迷你批次训练则允许按需调节这两个参数，从而形成不同的优化与泛化行为。现有研究多孤立地分析全图训练的优势或迷你批次训练的效率，却较少从 $b$ 和 $\beta$ 的共同视角揭示二者在收敛速度、最终性能和资源需求上的本质关系。

本文的动机正是填补这一空白。我们从优化动态与泛化理论出发，系统比较全图训练与迷你批次训练在相同的图学习目标下的行为差异。通过分析，我们发现全图训练并非在所有场景下均优于精心调参的迷你批次训练；相反，$b$ 和 $\beta$ 对收敛趋势的影响因损失函数类型（均方误差或交叉熵）而异，而扇出大小对泛化的作用比批次大小更为敏感且可能出现非单调波动。这些观察促使我们构建一个统一的解释框架，其中批次大小控制着梯度的统计稳定性，扇出大小决定了训练子图与完整图之间的结构差异，二者的交互最终决定了训练的效率与模型效果。本文旨在为该框架提供严格的理论支撑与大规模实验验证，从而为资源受限条件下 GNN 训练范式的选取提供原则性的决策依据。

## 核心创新

全图训练与迷你批次训练二元范式之间的性能优劣长期缺乏一致的理论解释，其根源在于两个关键操作参数——**批次大小 (batch size)** 与 **扇出大小 (fan-out size)**——对优化动态、泛化能力和计算效率的协同影响未被解耦。本文的核心创新在于：将这两种训练范式统一到由 `b` 和 `β` 参数化的同一框架下，首次系统揭示了它们在收敛速度与泛化间隙上的因果机制，并以此为基础推翻了“全图训练始终优于迷你批次训练”的隐含假设。

### 1. 关键控制 Slots 的识别与解耦

在 baseline 全图训练中，`b = n_train`（所有训练节点参与一次梯度下降），`β = d_max`（聚合全部邻居）；迷你批次训练则引入可调 Slots `b ≤ n_train` 与 `β ≤ d_max`（Section 2, Definition 1）。这一参数化使得**子图结构偏差**与**梯度估计噪声**成为可控量，构成全图/迷你批次训练差异的全部来源。

### 2. 收敛性理论：批次大小的损失函数依赖翻转

通过单层 ReLU GNN 的收敛分析（Theorem 1 与 Theorem 2），首次给出 MSE 与交叉熵（CE）下迭代数上界对 `(b, β)` 的定量依赖：

- **MSE 下**增大 `b` 会增加收敛所需迭代数：$T = O\big(n_{\mathrm{train}} h^{2} b^{5/2} \beta^{-1/2} \epsilon^{-1} \log(h^{2}\epsilon^{-1})\big)$；
- **CE 下**增大 `b` 则减少迭代数：$T = O\big(n_{\mathrm{train}}^{2} (\log n_{\mathrm{train}})^{1/2} \alpha^{-2} b^{-1} \beta^{-5/2} (n_{\mathrm{train}}^{2} + \epsilon^{-1})\big)$；
- 无论在哪种损失函数下，增大 `β` 均一致减少收敛所需迭代数，且边际收益递减（Remark 3.1，Remark 3.2）。

这一发现揭示了**损失函数的选择会完全反转批次大小对收敛趋势的影响**，而扇出大小则是加速收敛的通用杠杆。

### 3. 泛化分析：Wasserstein 距离量化结构差异

通过 PAC-Bayesian 框架与最优运输理论，定义训练-测试图结构的 Wasserstein 距离 $\Delta(\beta, b)$（Definition 1），并推导泛化界：

$$L_{\mathrm{test}} - \hat{L}_{\mathrm{train}} = O\Big(\frac{1}{n_{\mathrm{train}}} + \Delta(\beta, b)\Big) \quad (\text{Theorem 3})$$

该界首次将**扇出大小与批次大小的影响同时纳入非 i.i.d. 图数据的泛化控制**：增大 `β` 通过使 mini-batch 子图更接近 full-graph 来减小 $\Delta(\beta, b)$，但会引入非单调波动（Remark 4.1，Figure 6）；增大 `b` 同样降低 $\Delta(\beta, b)$ 但波动更小，因此对泛化提升更稳定——这直接导出“在内存约束下优先调节 `b` 提升泛化、优先调节 `β` 加速收敛”的实用指导。

### 4. 硬件无关评估与实证翻转

为避免硬件差异混淆模型特性与计算效率，本文提出以**迭代至精度**（iteration-to-accuracy）替代时间至精度作为公平比较指标（Section 5.1，Figure 1）。在该指标下，经过网格搜索 `b` 与 `β` 的迷你批次训练在 Reddit、ogbn-arxiv 和 ogbn-products 上分别获得 96.32、71.16、78.80 的测试准确率，均优于全图训练的 96.13、70.96、77.92（Table 1），有力否定了“全图训练始终最优”的先验认知。

综上，本文的理论-实验联合框架将 GNN 训练的设计空间从二选一范式重新定义为一个由 `(b, β)` 参数连续调控的多目标优化问题，为资源受限下的训练策略选择提供了可解释的决策基础。

## 整体框架

本文构建了一个系统比较全图训练（Full-graph Training）与迷你批次训练（Mini-batch Training）的分析框架。该框架将两种范式统一为受**批次大小 $b$​** 与**扇出大小 $\beta$​** 两个关键参数控制的端到端流水线，从而从优化动态、泛化能力与计算效率三个维度进行公平对比。全图训练对应 $b = n_{\mathrm{train}}$、$\beta = d_{\max}$ 的极限情况，而迷你批次训练可在 $b \leq n_{\mathrm{train}}$、$\beta \leq d_{\max}$ 的范围内自由调节。  

框架的理论基础分为两部分：1) 基于单层 GNN 与 ReLU 激活的收敛性分析，给出了 MSE 损失（Theorem 1）与交叉熵损失（Theorem 2）下迷你批次训练的迭代复杂度上界；2) 基于 Wasserstein 距离的泛化性分析（Theorem 3, Definition 1），将训练与测试图的子图结构差异与泛化间隙联系起来。实验部分采用与硬件无关的迭代至精度指标（Section 5.1, Figure 1）来隔离模型优化行为与计算硬件的影响，并通过网格调参在不同数据集上验证理论结论（Table 1, Figure 2–6）。

**流水线模块与数据流**：一次训练迭代由以下四个模块构成（Section 2, 3.1）：

1. **图数据采样与归一化** – 输入完整图拓扑及全部节点特征，根据当前配置的 $b$ 和 $\beta$ 从训练节点中均匀采样并逐跳选择邻居，构建归一化的子图邻接矩阵 $\tilde{\mathbf{A}}$ 并提取对应节点特征。全图训练时该模块不丢弃任何边或节点，等价于全集构造。  
2. **单层 GNN 前向传播** – 对聚合后的节点表示施加 ReLU 激活，得到隐藏表示 $\mathbf{z}_i = \sigma(\tilde{\mathbf{a}}_i \mathbf{X} \mathbf{W}^\top)$，其中 $\mathbf{W}$ 为可学习权重矩阵。  
3. **损失计算** – 基于 MSE 或交叉熵损失函数，利用当前子图内节点的标签计算经验风险。  
4. **参数更新** – 全图训练使用梯度下降（GD）一次性更新 $\mathbf{W}$；迷你批次训练使用随机梯度下降（SGD），每批返回的梯度仅基于当前采样子图计算。  

整个流水线在前向传播与反向传播之间循环，直到收敛。通过固定所有其他条件而仅调整 $b$ 与 $\beta$，该框架能够解耦出每个参数对收敛速度、泛化表现和计算吞吐量的独立影响，从而为内存受限场景下的参数选择提供理论指导（Remark 3.1, 3.2；Section 4；Section 5.5）。

## 核心模块与公式推导

GNN训练的两个范式——全图训练与迷你批次训练——可统一由两个可调节的控制变量描述：**批次大小** $b$ 与**扇出大小** $\beta$。全图训练将 $b$ 设为全部训练节点数 $n_{\mathrm{train}}$，$\beta$ 设为最大节点度 $d_{\max}$，相当于在每个梯度步中聚合完整邻域信息；迷你批次训练则允许 $b \le n_{\mathrm{train}}$ 且 $\beta \le d_{\max}$，通过均匀邻居采样构建子图，在计算效率与优化动态之间进行折中。两种范式共享相同的基本模块：基于 $b$ 和 $\beta$ 的**图采样与归一化**、**单层GNN前向传播**（$\mathbf{z}_i = \sigma(\tilde{\mathbf{a}}_i \mathbf{X} \mathbf{W}^{\top})$，采用ReLU激活）、**经验风险计算**（均方误差MSE或交叉熵CE）以及**参数更新**（全图采用梯度下降GD，迷你批次采用随机梯度下降SGD）。以下从收敛与泛化两个角度给出刻画 $b$ 和 $\beta$ 作用的核心公式及其含义。

### 收敛迭代复杂度

**均方误差（MSE）下的迭代上界（Theorem 1）**  
在MSE损失与ReLU激活下，迷你批次训练达到 $\epsilon$ 训练损失所需的迭代次数 $T$ 满足
$$T = O\left( n_{\mathrm{train}} h^{2} b^{\frac{5}{2}} \beta^{-\frac{1}{2}} \epsilon^{-1} \log\left( h^{2} \epsilon^{-1} \right) \right),$$
其中 $n_{\mathrm{train}}$ 为训练节点数，$h$ 为隐藏层维度，$b$ 为批次大小，$\beta$ 为扇出大小，$\epsilon$ 为目标损失。该界限揭示了 **$b$ 增大反而不利于收敛**（指数 $+5/2$），而 **$\beta$ 增大一致减少所需迭代**（指数 $-1/2$）。这一反直觉行为的根源在于：MSE下梯度方差随 $b$ 缩放的方式导致大步长需要更多迭代来稳定。

**交叉熵（CE）损失下的迭代上界（Theorem 2）**  
在交叉熵损失与特征分离假设下，收敛迭代次数上界为
$$T = O\left( n_{\mathrm{train}}^{2} \left( \log\left( n_{\mathrm{train}} \right) \right)^{\frac{1}{2}} \alpha^{-2} b^{-1} \beta^{-\frac{5}{2}} \left( n_{\mathrm{train}}^{2} + \epsilon^{-1} \right) \right),$$
其中 $\alpha$ 为反映类别分离程度的常数。与MSE相比，CE损失下 **增大 $b$ 会减少所需迭代数**（指数 $-1$），而 $\beta$ 仍保持正向加速效应（指数 $-5/2$）。这种差异源于交叉熵对梯度归一化的不同响应，使得大批次在分类问题中更高效。

**扇出大小的收敛敏感性（Remark 3.2）**  
在MSE设置下，迭代数对 $\beta$ 的偏导数给出
$$|\partial T / \partial \beta| = O\left( \beta^{-3/2} b^{5/2} \right),$$
表明当批次较大时，调节扇出大小对收敛速度的影响将显著放大，即在内存允许的前提下，优先增大 $\beta$ 比增大 $b$ 能更有效地加速MSE训练的收敛。

### 泛化误差界

为量化迷你批次与全图之间的结构差异，引入**Wasserstein距离**（Definition 1）
$$\Delta(\beta, b) = \inf_{\theta \in \Theta[\rho_{\mathrm{train}},\rho_{\mathrm{test}}]} \sum_{i} \sum_{j} \theta_{i,j} \delta(y_i, y_j, \beta, b),$$
该公式通过最优运输测度训练集与测试集节点表示分布的距离，其中 $\delta$ 封装了全图推断与迷你批次训练下节点表示的结构性差别，并由 $b$ 和 $\beta$ 参数化。

基于PAC‑Bayesian框架，泛化误差可被上界控制（Theorem 3）
$$L_{\mathrm{test}} - \hat{L}_{\mathrm{train}} = O\left( \frac{1}{n_{\mathrm{train}}} + \Delta(\beta, b) \right).$$
该界说明测试损失与训练损失之差由训练集大小与图结构分布差异 $\Delta$ 共同决定。增大 $b$ 和 $\beta$ 通常能够缩小 $\Delta$，从而收窄泛化间隙，但实验观察到 $\beta$ 对泛化的影响可能存在非单调波动，提示在实际调参中 $b$ 对泛化的提升更为稳定。因此，在内存受限场景下，应优先调节扇出大小来换取收敛加速，而若目标为提升泛化能力，则调整批次大小是更可靠的路径。

这些公式共同揭示了 $b$ 和 $\beta$ 作为核心控制变量的作用机制：批次大小主要决定优化路径的收敛趋势（在MSE与CE下方向相反）和泛化稳定性，扇出大小则一致地降低收敛所需迭代数并增强泛化，但其高敏感性可能引入不易预测的波动。

## 实验与分析

我们以与硬件无关的**迭代至精度（iteration-to-accuracy）**为核心指标（Figure 1），系统比较全图训练与迷你批次训练在四个大规模图数据集（Reddit、ogbn-arxiv、ogbn-products、ogbn-papers100M）上的优化动态、泛化能力和计算效率。所有实验基于单层及多层 GraphSAGE，损失函数覆盖 MSE 与交叉熵（CE），并通过网格搜索独立调节批次大小 b 与扇出大小 β，以揭示两者对训练行为的因果作用。


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/006_Figure_1.jpg]]
*Figure 1: Time-to-acc and iteration-to-acc in mini-batch and full-graph training with varying bandwidths (i.e., two inter-GPU bandwidth values: bw1=infinity > bw2=900GB/s) and computational capacities (i.e., GPU with 40GB of memory and CPU with 512GB of host memory )*

### 评估指标的公平性基础

时间至精度在不同硬件配置下可产生高达 **2787.05%** 的波动，而迭代至精度仅变化 **41.28%**（Figure 1）。该巨大差异表明时间指标严重受制于硬件带宽和计算能力，无法公允反映模型自身的收敛行为。因此，后续分析均以迭代次数作为模型性能的度量，杜绝硬件环境对结论的混淆。

### 收敛行为验证

单层 GraphSAGE 在 ogbn-products 上的收敛曲线（Figure 2）直接验证了理论预见的收敛规律（Theorem 1、Theorem 2、Remark 3.1）：


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/011_Figure_2.jpg]]
*Figure 2: Iteration-to-loss of one-layer GraphSAGE under CE and MSE across varying learning rates and batch sizes or fan-out sizes for ogbn-products*

- **批次大小 b 的作用因损失函数而异**——在 MSE 下，增大 b 会导致达到固定训练损失所需迭代数显著增加；而在 CE 下，增大 b 反而减少迭代数。
- **扇出大小 β 在两种损失下均一致地加速收敛**，但边际收益递减：β 从小值增大时收敛改善明显，进一步增大后改进趋于饱和。
- 多层模型的扩展实验（Figure 4）再现了上述规律，表明理论分析即使基于单层设置，其定性洞察仍可外推至更深网络。


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/023_Figure_4.jpg]]
*Figure 4: Iteration-to-loss of GraphSAGE under CE and MSE across varying batch and fan-out sizes. (a) Iter-to-acc, CE*

这些现象的根源在于：MSE 与 CE 下随机梯度的方差–批大小耦合方式截然不同，而扇出大小通过提升邻域聚合精度直接降低每次更新的梯度噪声。

### 泛化性能与精度对比

泛化界（Theorem 3）将训练-测试 Wasserstein 距离 Δ(β, b) 作为结构差异的核心度量，预测增大 b 或 β 能缩小该距离从而抑制泛化间隙。实际测试精度扫描（Figure 3、Figure 6）与这一预测方向一致，但揭示出重要细节：


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/014_Figure_3.jpg]]
*Figure 3: (a) Products, Batch size (b) Products, Fan-out size (c) Reddit, Batch size (d) Reddit, Fan-out size Figure 3: Test accuracy of one-layer GraphSAGE under MSE across varying learning rates and batch sizes or fan-out sizes for ogbn-products and reddit*

- 测试精度随 b 的提升整体平稳，是**稳定提升泛化的更可靠途径**。
- β 对泛化的影响存在**非单调波动**：在部分区间内增大 β 反而造成精度振荡甚至下降（如局部峰值后的退化），与理论上 Δ(β, b) 的单调减小预期不完全吻合。

在多模型最优超参搜索后，迷你批次训练在三个数据集上取得了优于或持平全图训练的结果（Table 1）：Reddit（96.32 vs 96.13）、ogbn-arxiv（71.16 vs 70.96）、ogbn-products（78.80 vs 77.92）。仅在超大规模图 ogbn-papers100M 上稍逊（58.52 vs 59.54）。该结果直接否定了“全图训练始终最优”的普遍假设，并证实精心调参的迷你批次范式具备与全图竞争甚至超越的能力。


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/031_Table_1.jpg]]
*Table 1: Best test accuracies of full-graph and mini-batch training of multi-layer GraphSAGE model without dropout layers after graph-based hyperparameter tuning*

### 消融研究与效率权衡

通过对 b 与 β 的二维消融，联合考察迭代至精度、时间至精度及训练吞吐量（Figure 5、Figure 6），得到以下对实践具有指导意义的结论：


![[assets/figures/papers/iclr26_0014_ZSfgsh43vT_Full-Graph_vs._Mini-Batch_Training_Comprehensive/figures/026_Figure_5.jpg]]
*Figure 5: Iteration-to-accuracy and time-to-accuracy of GraphSAGE under CE and MSE across varying batch sizes and fan-out sizes for reddit*

- **收敛速度与单步开销的权衡**：增大 β 可大幅减少所需迭代数，但每轮计算量亦急剧上升，吞吐量快速下降。实验中，β ≈ 15 时经常达到迭代效率与总训练时间的较优平衡。
- **损失函数对策略选择的影响**：在 MSE 下，增大 b 虽然减缓收敛，但提升吞吐量；在 CE 下，增大 b 同时加速收敛和吞吐量。因此，**优化超参组合时必须结合损失函数特性**。
- **内存约束下的实用优先级**：若目标为加速收敛，应优先调节扇出大小；若目标为提升泛化，应优先调节批次大小，以避免扇出大小引入的精度波动风险。

### 失败模式与开放性局限

实验中观察到以下失效或脆弱现象：

- **扇出大小引发的非单调泛化退化**：在 ogbn-products 等数据集上，β 超出一定阈值后测试精度反而下降（Figure 6），其机理目前仅能从 Wasserstein 距离的局部几何非凸性去推测，缺乏严格刻画。
- **交叉熵损失下泛化分析的缺失**：当前泛化界仅针对 MSE 损失给出（Theorem 3），对 CE 情况尚无理论支撑，导致无法解释图 3 中 CE 精度与 b/β 关系的完整特性。
- **理论与多层模型的鸿沟**：收敛与泛化定理均建立于单层 ReLU-GNN，虽多层实验显示定性一致，但缺少多层严格证明，限制了在深层模型中进行精确预测的置信度。
- 对异构、动态图以及含有历史嵌入的采样方法（如 LADIES、GraphSAINT），本文框架的适用性尚未证实，仍有待扩展。

综上，全图与迷你批次的优劣高度依赖超参选择，且受损失函数与网络深度调制。当前理论已能捕获大部分趋势，但对于扇出诱发的不稳定性和非 MSE 损失的泛化行为，仍需进一步研究。

## 方法谱系与知识库定位

### 1. 基线范式与关键调节旋钮
该工作并非提出一种新的训练算法，而是建立一个 **全图与迷你批次训练的系统比较框架**。两条基线分别为：
- **全图训练 (Full-graph Training)**：在完整邻接矩阵上对所有训练节点进行梯度下降（GD），隐式设定批次大小 $b=n_{\mathrm{train}}$、扇出大小 $\beta=d_{\max}$。
- **迷你批次训练 (Mini-batch Training)**：通过均匀邻居采样构建子图，使用随机梯度下降（SGD）。其行为由两个可以自由调节的 **旋钮** 控制——批次大小 $b$ 和扇出大小 $\beta$。

全图训练可视为迷你批次训练在 $b=n_{\mathrm{train}}$, $\beta=d_{\max}$ 时的特例，但该工作首次揭示了这两个参数如何通过 **优化动态**（收敛所需迭代数）与 **泛化能力**（Wasserstein距离界）从根本上分开影响训练效果与效率（Theorem 1–3）。实验进一步证实：精心调节 $b$ 与 $\beta$ 的迷你批次训练可以取得优于全图训练的测试精度（如 Reddit 上 96.32 vs. 96.13，ogbn-arxiv 上 71.16 vs. 70.96；Table 1），打破了“全图训练始终更优”的常见认知。

### 2. 与相关方法的定位与关系
该分析框架处于 **GNN 训练理论** 与 **采样训练实践** 的交汇点。
- **相对于纯理论工作**：以往的收敛性分析多针对全图 GD，本文首次对 SGD 迷你批次下的 GNN 给出依赖 $b$ 与 $\beta$ 的迭代复杂度上界（MSE 下 $T = O(n_{\mathrm{train}} h^{2} b^{5/2} \beta^{-1/2} \epsilon^{-1} \log (h^{2} \epsilon^{-1}))$，CE 下另有界；Theorem 1–2）。泛化分析则引入最优运输视角的 Wasserstein 距离来刻画 mini-batch 与 full-graph 的结构差异（Definition 1, Theorem 3），为后续在非 i.i.d. 图数据上的泛化研究提供了新工具。
- **相对于工程采样器（如 LADIES、GraphSAINT）**：本文有意将分析建立在最基本的均匀邻居采样之上，以隔离 $b$ 和 $\beta$ 的因果效应。因此，该框架可视为 **理解更复杂采样策略的理论锚点**——开放问题中明确指出需要将分析推广到包含历史嵌入或基于重要性的采样方法（See open_questions），说明当前工作奠定了可扩展的理论基础，但尚未覆盖这些 follow-up。
- **相对于硬件驱动优化**：通过引入 **与硬件无关的迭代至精度指标**（iteration-to-accuracy，Figure 1），将模型性能提升与计算吞吐量解耦，为跨环境的公平比较提供了方法论贡献，这在过往研究中常被忽略。

### 3. 适用边界与经验限制
该框架的结论在以下边界内成立，超出这些条件需谨慎推广：
- **模型假设**：理论分析严格依赖 **单层** GNN 和 **ReLU** 激活（Section 3.1）。多层扩展虽在附录中讨论，但严格证明尚未给出。
- **损失函数**：收敛定理覆盖 MSE 与交叉熵，但泛化界仅对 MSE 损失导出（Theorem 3），交叉熵下的泛化理论存在空白。
- **任务与数据**：实验集中于 **transductive 节点分类**，数据集为 Reddit、ogbn-arxiv/products/papers100M。归纳设置与链接预测仅在附录 P 中讨论，未经验证（See limitations）。
- **异构图与激活函数**：框架默认同构图与 ReLU 非线性。对于 Tanh 等其他激活函数、或包含多种边/节点类型的异构图，收敛界与泛化界可能发生本质变化，需要额外研究（See open_questions）。
- **超参数敏感区**：实证给出实用指导——在平均度小于 50 的数据集上，批次大小宜保持在训练节点数的一半以下，扇出大小不超过 15（Section 5.5）。但在更大或更密的图上，以及对于极端参数（如超大批次或超大扇出），泛化性能可能出现非单调波动甚至退化（Observed non-monotonic fluctuations in Figure 3,6），相关机制尚待澄清。

### 4. 局限与开放问题
综合理论与实验，以下核心问题仍然开放，构成未来工作的重要方向：
1. **极端参数下的泛化退化**：在 DNN 中观察到的“大批次泛化降级”现象是否会在 GNN 的巨量 $b$ 或 $\beta$ 下重现？当前实验已观察到扇出大小导致的非单调泛化波动，但原因尚未被理论捕捉。
2. **理论扩展**：将收敛界与泛化界推广到 **多层 GNN**、**交叉熵损失的泛化分析**、以及 **Tanh 等激活函数**，以覆盖更实际的模型配置。
3. **与高级采样方法的统一**：如何将本文的分析框架应用于 **LADIES、GraphSAINT 等采样器**？特别是历史嵌入的引入是否会改变 $b$ 与 $\beta$ 的收敛/泛化权衡？
4. **异构图场景**：对于包含多种关系与节点类型的图，不同类型边的扇出策略与聚合权重将如何与本文的核心结论交互，需要从头构建新的理论与实验体系。
5. **任务泛化**：在归纳学习中，训练/测试图结构差异更大，Wasserstein 距离界是否仍能有效预测泛化？链接预测任务中的梯度动态与节点分类存在根本不同，现有结论能否直接迁移？

上述问题中的部分（如 2、3）在原文附录或开放问题部分已被明确指出，但尚未提供解决方案；其他（如 1、4）则基于观察到的现象或空白推论，需要设计新的实验与理论来验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Full_Graph_vs_Mini_Batch_Training_Comprehensive_Analysis_from_a_Batch_Size_and_Fan_Out_Size_Perspective.pdf]]
