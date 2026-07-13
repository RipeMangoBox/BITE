---
title: "Task-free Adaptive Meta Black-box Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Task_free_Adaptive_Meta_Black_box_Optimization.pdf
project_link: null
code_link: null
openreview_forum_id: AufVSUgMUo
aliases:
- AAMBBOM
- TFAMBBO
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "ABOM 将离散的元优化框架替换为完全可微的优化器，利用目标任务的在线优化数据（种群与适应度）通过梯度下降自适应更新参数，从而消除了对预定义任务分布 F 的需求。"
primary_logic: "通过将选择、交叉和变异算子参数化为基于注意力机制的可微模块，并结合精英归档的对齐损失进行闭环梯度自适应，ABOM 实现了零样本优化，无需任何预训练任务或启发式规则，同时具备全局收敛的理论保证。"
claims:
- "在 BBOB 和 UAV 路径规划等基准上，ABOM 在无任何手工训练任务的情况下，性能优于或可比肩传统和基于元学习的基线方法。"
- "自适应参数学习损失在所有测试函数上持续下降并收敛，证实了基于精英对齐的自监督调整的有效性。"
- "消融研究表明，移除参数自适应、交叉或变异中任一组件均会导致性能显著恶化，验证了三者均为 ABOM 的关键组成部分。"
- "可视化分析揭示学习到的选择矩阵和变异矩阵呈现出统计显著且可解释的搜索模式，如对高适应度个体的选择偏向和一致的基因交互模式。"
---

# Task-free Adaptive Meta Black-box Optimization

> [!tip] 核心洞察
> 通过将选择、交叉和变异算子参数化为基于注意力机制的可微模块，并结合精英归档的对齐损失进行闭环梯度自适应，ABOM 实现了零样本优化，无需任何预训练任务或启发式规则，同时具备全局收敛的理论保证。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 任务无关的自适应元黑盒优化 |
| 英文题名 | Task-free Adaptive Meta Black-box Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=AufVSUgMUo) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | ABOM (Adaptive meta Black-box Optimization Model) |
| Dataset | BBOB f6 (d=500), BBOB f8 (d=500), UAV 路径规划（28 个地形） |

> [!tip] 效果简介
> - BBOB f6 (d=500) 上，平均目标值 ± 标准差 为 6.201e+3 ± 6.326e+2，对比 CMAES 2.164e+4 ± 6.814e+3（最佳基线），变化 ABOM 显著优于所有基线（Wilcoxon 检验 p<0.05）。
> - BBOB f8 (d=500) 上，平均目标值 ± 标准差 为 8.886e+4 ± 1.267e+5，对比 CMAES 2.827e+5 ± 6.292e+4，变化 ABOM 显著更优。
> - UAV 路径规划（28 个地形） 上，归一化平均成本 为 最低（见图 3），对比 各基线中次优值，变化 ABOM 收敛最快且最终成本最低。

## 概要

黑盒优化（BBO）在超参数调优、神经结构搜索和机器人控制等应用中至关重要，但传统进化算法依赖手工设计的启发式算子，而新兴的元黑盒优化（MetaBBO）方法虽然能从任务分布中学习优化策略，却需要预定义训练任务分布 $\mathcal{F}$。当实际应用中目标任务的分布未知或数据稀缺时，这种依赖严重限制了 MetaBBO 方法的泛化与部署能力。

针对这一瓶颈，本文提出 **ABOM（Adaptive meta Black-box Optimization Model）**，一种任务无关的自适应元黑盒优化框架。其核心思路是将离散的元优化框架替换为**完全可微的优化器**：将选择、交叉和变异算子参数化为基于注意力机制的可微模块，并利用目标任务的在线优化数据——种群与适应度——通过梯度下降自适应更新参数。具体而言，ABOM 通过极小化子代种群与精英归档之间的 L2 距离进行自监督参数学习，从而消除了对预定义任务分布 $\mathcal{F}$ 的需求，实现了零样本优化，同时具备全局收敛的理论保证。

实验结果表明，ABOM 在无需任何手工训练任务的前提下，于 BBOB 合成基准（维度高达 500）和 28 个无人机路径规划实际问题上，取得了优于或可比肩传统自适应方法（如 CMAES）和基于元学习的基线方法（如 GLEET、RLDEAFL）的性能。消融研究进一步证实，参数自适应、交叉和变异三个组件均为 ABOM 的关键组成部分，移除任一部分均会导致性能显著恶化。可视化分析揭示，学习到的选择矩阵和变异矩阵呈现出统计显著且可解释的搜索模式，包括对高适应度个体的选择偏向和一致的基因交互模式。

黑盒优化（Black-box Optimization, BBO）在科学发现、工程设计、超参数调优等众多领域中扮演着核心角色。其目标是在没有梯度信息、仅能通过查询获取目标函数值的条件下，寻找全局最优解：

$$\operatorname*{min}_{\mathbf{x}\in\mathbb{R}^d} f_T(\mathbf{x})$$

进化算法（Evolutionary Algorithms, EAs）及其自适应变体——如差分进化（**DE**, Storn & Price, 1997）、协方差矩阵自适应进化策略（**CMAES**, Hansen, 2016）——因其无需梯度且具备全局搜索能力，长期以来是解决此类问题的主流方法。然而，这些传统方法的核心瓶颈在于：其搜索策略依赖人工设计的启发式规则和固定的进化算子（选择、交叉、变异），其参数配置高度依赖于专家经验，难以在不同任务间自动迁移和适配。

近年来，元黑盒优化（Meta Black-box Optimization, MetaBBO）试图突破这一限制。其核心思想是从一组训练任务分布 $\mathcal{F}$ 中学习一个可泛化的优化策略 $\pi_{\theta}$，形式化为：

$$J(\pmb\theta) = \operatorname*{max}_{\pmb\theta \in \Theta} \mathbb{E}_{f \sim \mathcal{F}} \left[ \mathcal{R} \big( \mathcal{A}, \pi_{\pmb\theta}, f \big) \right]$$

典型的 MetaBBO 方法包括基于元学习的粒子群优化器（**GLEET**, Ma et al., 2024）、差分进化优化器（**RLDEAFL**, Guo et al., 2025）以及进化策略优化器（**LES**, Lange et al., 2023b）等。尽管这些方法在特定任务分布上取得了显著进展，但它们存在一个根本性的依赖：**必须预先定义训练任务分布 $\mathcal{F}$**。当实际应用中目标任务的分布未知、数据稀缺或与训练分布存在显著差异时，元训练得到的策略往往难以有效泛化，严重限制了 MetaBBO 在真实场景下的部署能力。

这一缺陷揭示了当前 MetaBBO 范式的结构性缺口：**如何在无需任何预定义训练任务的前提下，实现对任意目标黑盒优化任务的零样本自适应？** 这要求优化器能够完全摆脱对 $\mathcal{F}$ 的依赖，转而仅利用目标任务的在线优化数据来动态调整其搜索行为。本文提出的 ABOM（Adaptive meta Black-box Optimization Model）正是针对这一核心问题，通过构建一个端到端可微的进化优化框架，将参数学习与优化过程融为一体，从根本上消除了任务分布依赖。

## 核心方法与创新机理

### 瓶颈突破：从“任务分布依赖”到“任务无关自适应”

现有元黑盒优化（MetaBBO）方法的核心瓶颈在于其对**手工设计的训练任务分布 F** 的刚性依赖。传统范式（如 **GLEET**（Ma et al., 2024）、**RLDEAFL**（Guo et al., 2025）、**LES**（Lange et al., 2023b））遵循“元训练—泛化”的两阶段流程：先在预定义的任务分布上学习元策略，再将其部署到目标任务。然而，当实际应用中目标任务的分布未知或数据稀缺时，这种依赖导致泛化能力急剧退化，严重限制了 MetaBBO 在真实场景下的部署可行性。

ABOM 的突破性创新在于**将这一离散的元优化框架替换为完全可微的优化器**，从根本上消除了对预定义任务分布 F 的需求。其核心机制是利用目标任务的在线优化数据（种群与适应度）通过梯度下降自适应更新参数，实现了**零样本、任务无关的在线自监督学习**。

### 三个关键 changed slots

ABOM 相对于现有 MetaBBO 基线在三个关键维度上实现了范式转换：

**1. 算法搜索空间：从离散设计到连续可微参数空间**

| 维度 | 传统 MetaBBO | ABOM |
|------|-------------|------|
| 搜索空间 | 离散且需人工设计的算法空间 A | 连续可微参数空间 θ，通过梯度学习自动调整 |
| 参数调整 | 依赖元训练或手动调参 | 在线梯度下降自适应更新 |

传统方法在离散的算法搜索空间中通过元学习或手工规则选择进化策略，而 ABOM 将进化算子统一为连续可微的参数空间，使得整个优化流程可通过梯度端到端优化（Section 2）。这一设计使得算法行为能够平滑地适应目标任务的特征，而非在预设的离散选项间切换。

**2. 训练任务分布：从必须预训练到零样本自适应**

| 维度 | 传统 MetaBBO | ABOM |
|------|-------------|------|
| 训练需求 | 必须提供手工设计的训练任务分布 F | 零样本，仅利用目标任务的在线优化数据 |
| 泛化方式 | 从 F 中学习可迁移的元知识 | 实时从目标任务的优化轨迹中自监督学习 |

ABOM 不进行任何任务相关的预训练，所有结果均来自零样本在线自适应。与之对比，MetaBBO 基线（如 RLDEAFL）已在预定义任务分布上进行元训练。这一差异在实验公平性说明中被明确强调：ABOM 在无预训练优势的情况下，仍能在 BBOB 和 UAV 路径规划等基准上达到或超越预训练方法的性能（Table 1, Figure 3）。

**3. 进化算子设计：从固定启发式到可微注意力机制**

| 维度 | 传统进化算子 | ABOM |
|------|-------------|------|
| 选择 | 固定规则（如锦标赛选择、轮盘赌） | 双路径注意力，同时建模解空间关系和适应度值 |
| 交叉 | 固定算子（如均匀交叉、模拟二进制交叉） | 注意力加权重组池 + MLP 生成中间种群 |
| 变异 | 固定扰动（如高斯变异、多项式变异） | 基因维度自注意力建模 + Dropout 探索 + MLP 扰动 |
| 参数更新 | 手动调参或启发式自适应 | AdamW 在线更新所有可学习参数 θ |

具体而言，ABOM 的选择矩阵通过双路径注意力构建（Eq. 5），融合个体空间关系与适应度驱动的选择压力；交叉操作通过注意力重组池与 MLP 实现可微重组（Eq. 6）；变异模块则利用基因维度的自注意力建模与 Dropout 机制在保持探索能力的同时实现梯度驱动的自适应（Section 3.2）。所有可学习参数通过极小化子代与精英归档之间的 L2 距离进行端到端更新（Eq. 10），形成了闭环的自监督学习机制。

### 核心洞察：精英对齐驱动的自监督闭环

ABOM 的核心洞察在于：**通过将选择、交叉和变异算子参数化为基于注意力机制的可微模块，并结合精英归档的对齐损失进行闭环梯度自适应，实现了无需任何预训练任务或启发式规则的零样本优化**。

这一设计的关键在于精英归档 E^(t) 扮演了“自监督信号源”的角色——它保存了优化过程中迄今发现的最优解，为参数更新提供了无需外部标注的监督信号。参数自适应损失 $ \min_{\boldsymbol{\theta}} \mathcal{L}^{(t)} = \| \hat{\mathbf{P}}^{(t)} - \mathbf{E}^{(t)} \|^2 $ 驱动进化算子学习生成更接近精英解的种群，从而实现了搜索行为的持续改进。

消融研究（Table 2）为此提供了决定性证据：移除参数自适应（ABOM w/o adaptation）导致性能显著下降，验证了在线自监督对齐的必要性；单独移除交叉或变异模块同样造成大幅性能损失，证明两种操作符对有效搜索均不可或缺。此外，可视化分析（Figure 4）揭示学习到的选择矩阵和变异矩阵呈现出统计显著且可解释的搜索模式——如对高适应度个体的选择偏向和一致的基因交互模式——进一步证实了可微算子确实学到了有意义的进化行为，而非随机噪声。

### 理论保障：全局收敛性

ABOM 的创新不仅体现在经验性能上，还具备理论层面的保障。在满足搜索空间紧致且全局最优点位于内部等假设条件下，ABOM 几乎必然收敛到全局最优值：$ f_t^* \xrightarrow{a.s.} f^* \quad \text{as} \quad t \to \infty $（Eq. 14）。这一理论结果将可微进化算子的自适应学习与经典进化算法的收敛分析框架桥接起来，为方法的可靠性提供了形式化支撑。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual comparison: (Left) MetaBBO methods learn meta-strategies from task distributions but depend on handcrafted training tasks; (Right) Our framework performs adaptive parameter learning using self-generated optimization data, eliminating task distribution dependency*

ABOM 将传统进化算法的种群迭代过程重构为一个端到端可微的元优化器，其整体工作流由五个顺序模块构成闭环（Fig. 2）。核心设计原则在于：将选择、交叉、变异等进化算子统一参数化为基于注意力机制的可微函数，并通过在线自监督信号驱动参数自适应更新，从而完全消除对预定义训练任务分布 $F$ 的依赖。

**初始化**：采用拉丁超立方采样随机生成初始种群 $\mathbf{P}^{(0)} \in \mathbb{R}^{N \times d}$，其中 $N$ 为种群规模，$d$ 为问题维度。该策略确保初始解在搜索空间内均匀覆盖，避免随机聚集带来的探索盲区。

**繁殖（Reproduction）**：ABOM 的可微元策略 $\hat{\mathbf{P}}^{(t)} = \pi_{\theta}(\mathbf{P}^{(t)}, \mathbf{F}^{(t)})$ 通过三个级联的注意力模块实现种群更新：
1. **选择**：构建双路径注意力矩阵 $\mathbf{A}^{(t)}$，同时建模解空间中的个体关系与适应度值驱动的选择压力，生成对高适应度个体的加权关注模式。
2. **交叉**：利用注意力加权重组池 $\mathbf{A}^{(t)}\mathbf{P}^{(t)}$ 经 MLP 变换后与当前种群相加，生成中间种群 $\mathbf{P}^{\prime(t)}$，模拟遗传重组过程。
3. **变异**：通过基因维度的自注意力机制与 MLP 扰动产生子代种群 $\hat{\mathbf{P}}^{(t)}$，引入结构化随机性以维持探索能力。模块内置的 Dropout 机制进一步增强了搜索的随机性。

**评估与精英归档**：对子代种群进行适应度评估后，ABOM 保留历史最优的 $N$ 个个体形成精英归档 $\mathbf{E}^{(t)}$。这一机制确保了优化过程的单调改进，同时为参数自适应提供高质量的对齐目标。

**参数自适应**：ABOM 的核心创新在于在线参数学习。通过最小化子代种群与精英归档之间的 L2 距离 $\mathcal{L}^{(t)} = \|\hat{\mathbf{P}}^{(t)} - \mathbf{E}^{(t)}\|^2$，利用 AdamW 优化器对所有可学习参数 $\theta$ 进行梯度更新。这一自监督信号完全来源于目标任务的在线优化数据 $\mathcal{M}^{(t)}$，使 ABOM 具备零样本、任务无关的自适应能力，无需任何预训练任务或启发式规则。

整个框架的计算复杂度为 $O(N d d_A + N^2 d_A + N d_A d_M + N d_M d + d^2 d_A + d d_A d_M)$，其中 $d_A$ 为注意力维度，$d_M$ 为隐藏维度。在高维场景下，$O(d^3)$ 项可能成为计算瓶颈。理论分析表明，在搜索空间紧致且全局最优点位于内部的假设下，ABOM 几乎必然收敛到全局最优值 $f_t^* \xrightarrow{a.s.} f^*$，其收敛性由精英归档的单调改进与变异模块的非零探索概率共同保证。

ABOM 将传统进化算法的离散算子空间统一为一个端到端可微的连续参数空间 $\pmb{\theta}$，从而消除了对预定义任务分布 $\mathcal{F}$ 的依赖。其核心优化目标直接由目标任务的累积在线数据 $\mathcal{M}^{(t)}$ 驱动：

$$J(\pmb{\theta})=\operatorname*{max}_{\pmb{\theta}\in\Theta}[\mathcal{R}(\pi_{\pmb{\theta}},\mathcal{M}^{(t)})]$$

其中 $\mathcal{R}$ 为期望性能度量，$\pi_{\pmb{\theta}}$ 为可微元策略（Eq. 4）。

### 可微进化算子

ABOM 的元策略 $\hat{\mathbf{P}}^{(t)} = \pi_{\pmb{\theta}}(\mathbf{P}^{(t)}, \mathbf{F}^{(t)})$ 通过三个基于注意力机制的可微模块实现（Fig. 2 Bottom）：

**选择（Selection）** 通过双路径注意力同时建模解空间关系与适应度驱动的选择压力，生成选择矩阵 $\mathbf{A}^{(t)} \in \mathbb{R}^{N \times N}$：

$$\mathbf{A}^{(t)}=\mathrm{softmax}\left(\frac{(\mathbf{P}^{(t)}\mathbf{W}^{QP})(\mathbf{P}^{(t)}\mathbf{W}^{KP})^{\top}+(\mathbf{F}^{(t)}\mathbf{W}^{QF})(\mathbf{F}^{(t)}\mathbf{W}^{KF})^{\top}}{\sqrt{d_A}}\right)$$

其中 $\mathbf{P}^{(t)}$ 为当前种群，$\mathbf{F}^{(t)}$ 为适应度值，$\mathbf{W}^{QP},\mathbf{W}^{KP},\mathbf{W}^{QF},\mathbf{W}^{KF}$ 为可学习的投影矩阵，$d_A$ 为注意力维度（Eq. 5）。

**交叉（Crossover）** 利用注意力加权重组池与 MLP 生成中间种群：

$$\mathbf{P}^{'(t)}=\mathbf{P}^{(t)}+\mathrm{MLP}_{\theta_c}(\mathbf{A}^{(t)}\mathbf{P}^{(t)})$$

$\mathrm{MLP}_{\theta_c}$ 为以 $\theta_c$ 参数化的多层感知机（Eq. 6）。

**变异（Mutation）** 通过基因维度的自注意力建模与 MLP 扰动产生子代 $\hat{\mathbf{P}}^{(t)}$。整个参数化过程将进化算子转化为随机但可微的函数，内置的 Dropout 机制在保持探索能力的同时不破坏梯度传播。

### 自适应参数学习

ABOM 的优化循环包含初始化、繁殖、评估、精英保留和参数自适应五个步骤。初始化采用拉丁超立方采样生成 $\mathbf{P}^{(0)}$。核心的自适应机制通过极小化子代种群与精英归档 $\mathbf{E}^{(t)}$ 之间的 $L_2$ 距离实现：

$$\operatorname*{min}_{\pmb{\theta}}\mathcal{L}^{(t)}=\|\hat{\mathbf{P}}^{(t)}-\mathbf{E}^{(t)}\|^2$$

精英归档 $\mathbf{E}^{(t)}$ 由历史最优的 $N$ 个个体组成，确保单调改进。该自监督损失通过基于梯度的优化器（如 AdamW）在线更新所有可学习参数 $\pmb{\theta}$，使算法能够根据目标任务的实时反馈持续调整搜索行为（Eq. 10, Algorithm 1）。

### 收敛性保证

在搜索空间紧致且全局最优点位于内部的假设下，ABOM 具备几乎必然收敛到全局最优的理论保证：

$$f_t^*\xrightarrow{a.s.} f^* \quad as \quad t\to\infty$$

该保证源于可微算子中 Dropout 引入的非零探索概率——对任意 $\delta > 0$，有 $\mathbb{P}(\exists i : \|\hat{\mathbf{p}}_i^{(t)} - \mathbf{x}^*\| < \delta \mid \mathcal{F}_t) \geq 1 - (1 - \gamma)^N > 0$，结合精英保留策略确保了全局收敛性（Eq. 14, Section 3.4）。

## 实验与关键发现

### 核心瓶颈的实证验证

本文提出的 ABOM 旨在解决元黑盒优化（MetaBBO）对**手工设计训练任务分布 F 的强依赖**这一瓶颈。实验设计围绕以下因果链条展开：若 ABOM 的完全可微架构与在线自监督对齐机制有效，则其在无任何预训练的条件下，应能在合成基准与现实任务上达到或超越需要 F 进行元训练的基线方法。

**决定性证据**来自三个层次：

1. **零样本性能优势**：在 BBOB 高维测试集（d=500）上，ABOM 在多个函数上显著优于所有基线（Table 1）。例如，在 f6 上 ABOM 达到 $6.201\times10^3 \pm 6.326\times10^2$，而最强基线 CMAES 仅为 $2.164\times10^4 \pm 6.814\times10^3$（Wilcoxon 检验 p<0.05）。这一结果直接证明，**消除对 F 的依赖并未损害优化能力**，反而通过在线自适应获得了更强的任务适配性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/003_Table_1.jpg]]
*Table 1: The comparison results of the baselines on the BBOB suite with d = 500. All results are reported as the mean and standard deviation (mean ± std) over 30 independent runs. Symbols “−”, “≈”, and “+” imply that the corresponding baseline is significantly worse, similar, and better than ABOM on the Wilcoxon rank-sum test with 95% confidence level, respectively. The best results are indicated in bold, and the suboptimal results are underlined*

2. **自适应机制的有效性**：Figure 6 显示参数自适应损失在所有 BBOB 测试函数（d=500）上持续下降并收敛，证实了基于精英对齐的自监督损失 $\min_{\pmb{\theta}}\mathcal{L}^{(t)}=\|\hat{\mathbf{P}}^{(t)}-\mathbf{E}^{(t)}\|^2$ 能够稳定驱动参数学习，而非随机波动。

3. **组件的因果必要性**：消融实验（Table 2）表明，移除参数自适应（No Parameter Adaptation）、交叉（No Crossover）或变异（No Mutation）中任一组件均导致性能显著恶化，验证了三者在 ABOM 框架中均为不可或缺的关键组成部分。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/007_Table_2.jpg]]
*Table 2: Ablation study of ABOM’s key components on the BBOB suite with d = 30*

---

### 主实验结果

#### BBOB 基准测试（d=500）

Table 1 给出了完整的高维对比结果。ABOM 在 24 个测试函数中的大多数上取得最优或次优，尤其在高维不可分离函数（如 f6、f7、f8）上展现出显著优势。值得注意的是，**所有 MetaBBO 基线（GLEET、RLDEAFL、LES、GLHF）均在与 RLDEAFL 相同的合成问题分布上进行了预训练**，而 ABOM 完全未使用任何预训练任务。这一对比强化了 ABOM 任务无关自适应机制的价值。

#### UAV 路径规划

在 28 个地形问题上，ABOM 展现出**最快的收敛速度和最低的最终归一化成本**（Figure 3）。左侧收敛曲线显示 ABOM 在有限评估预算下迅速下降并稳定在最低水平；右侧运行时对比表明 ABOM 的 GPU 推理效率显著优于多数基线。该结果验证了 ABOM 从合成基准到现实连续优化问题的跨域泛化能力。

---

### 消融研究

Table 2 系统解耦了 ABOM 的三个关键机制：

| 变体 | 性能影响 | 机制解释 |
|------|---------|---------|
| No Parameter Adaptation | 大幅下降 | 移除在线自监督对齐后，进化算子参数无法根据当前任务景观调整，退化为固定随机策略 |
| No Crossover | 显著下降 | 仅依赖变异无法有效重组种群中的优质基因片段，搜索效率降低 |
| No Mutation | 显著下降 | 缺少变异引入的多样性，种群易陷入局部最优，探索能力受限 |

消融结果确认：**选择-交叉-变异的三阶段可微进化管道与在线参数自适应构成了一个不可分割的闭环系统**，任何环节的缺失都会破坏“探索-利用”平衡。

---

### 学习到的搜索模式可视化

Figure 4 揭示了 ABOM 在 BBOB 函数 f4、f11、f24（d=30）上演化过程中学习到的**选择矩阵与变异矩阵**：

- **选择矩阵**：随代数增加，矩阵行向量呈现相似性，表明 ABOM 学习到从少数高适应度个体生成后代的行为模式，这与差分进化（DE）中的差分向量机制类似。该模式在不同函数上一致出现，说明 ABOM 自发发现了“精英引导”的搜索策略。
- **变异矩阵**：从随机初始化逐步演化为有序结构，表明变异操作遵循适应于问题结构的**一致基因交互模式**，而非无方向扰动。

这些可视化提供了 ABOM 可解释性的直接证据：基于注意力的可微算子并非黑盒，而是涌现出与传统进化算法相似的、统计显著且可解释的搜索行为。

---

### 超参数敏感性分析

Figure 5 分析了四个关键超参数在 BBOB（d=30）上的敏感性：

- **种群规模 N**：过小导致多样性不足，过大增加计算开销，存在一个较宽的鲁棒区间。
- **隐藏维度 d_M**：模型容量需与问题维度匹配，过小限制表达能力，过大可能导致过拟合。
- **交叉 Dropout 率 p_C** 与**变异 Dropout 率 p_M**：适中的 Dropout 率对维持探索-利用平衡至关重要。过高导致搜索随机化，过低则削弱探索能力。

总体而言，ABOM 在较宽的超参数范围内保持稳定性能，表明框架具有较好的鲁棒性。

---

### 失败模式与局限性

尽管 ABOM 在多数任务上表现优异，分析揭示了以下**失败模式与局限**：

1. **极端复杂景观上的差距**：在部分 BBOB 函数（如 f10 等）上，ABOM 相对于精细调优的 CMAES 等自适应方法仍有差距，表明在高度多模态或病态条件数景观上，纯在线自适应可能不足以完全捕捉问题结构。

2. **高维可扩展性瓶颈**：计算复杂度中的 $O(d^3)$ 项（来自基因维度自注意力）在高维场景（如 d>1000）下可能成为限制因素，需通过稀疏或低秩注意力机制缓解。

3. **边界最优点的理论假设**：全局收敛证明假设搜索空间紧致且最优点位于内部，当最优点位于边界或存在约束时，理论保证不直接成立。

4. **固定种群与模型容量**：当前框架在整个优化过程中保持种群规模和模型容量固定，动态调整这些超参数或可进一步提升性能与效率。

5. **GPU 依赖性**：框架依赖 GPU 加速以获得可接受的迭代效率，尚未针对纯 CPU 环境进行专门优化。

---

### 关键图表索引

- **Table 1**：BBOB d=500 主结果对比，ABOM 在多数函数上显著优于所有基线（Wilcoxon 检验，95% 置信水平）。
- **Figure 3**：UAV 路径规划收敛曲线与运行时对比，ABOM 收敛最快且最终成本最低。
- **Table 2**：消融实验，验证参数自适应、交叉、变异均为关键组件。
- **Figure 4**：学习到的选择与变异矩阵可视化，揭示统计显著的可解释搜索模式。
- **Figure 5**：超参数敏感性分析，显示框架在较宽范围内鲁棒。
- **Figure 6**：参数自适应损失收敛曲线，证实自监督对齐的有效性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/014_Table_3.jpg]]
*Table 3: Overview of the BBOB suites*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/020_Table_6.jpg]]
*Table 6: Performance comparison of ABOM vs. ABOM-PT on the STOP suite over 30 independent runs, reported as the mean and standard deviation of objective values (lower is better)*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_AufVSUgMUo/figures/021_Table_7.jpg]]
*Table 7: The comparison results of the baselines on the BBOB suite with d = 30. All results are reported as the mean and standard deviation (mean ± std) over 30 independent runs. Symbols “−”, “≈”, and “+” imply that the corresponding baseline is significantly worse, similar, and better than ABOM on the Wilcoxon rank-sum test with 95% confidence level, respectively. The best results are indicated in bold, and the suboptimal results are underlined*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

传统黑盒优化（BBO）方法，包括进化算法（Evolutionary Algorithms, EAs）和群智能算法，依赖手工设计的进化算子（选择、交叉、变异）及其超参数配置。这些设计严重依赖领域专家的先验知识，且在面对不同特性的目标函数时泛化能力有限。

元黑盒优化（MetaBBO）通过引入“学习优化器”的思想，试图从任务分布中自动发现有效的优化策略。然而，现有 MetaBBO 方法存在一个根本性瓶颈：**它们依赖手工设计的训练任务分布 F**。这一依赖导致两个关键问题：

1. **任务分布未知时的失效**：在真实应用场景中，目标任务的分布往往是未知的或难以建模的，无法预先构建合适的 F。
2. **数据稀缺时的泛化困难**：当目标任务仅有少量优化预算时，基于预训练的元策略难以有效迁移。

ABOM 的核心突破在于**彻底消除了对预定义任务分布 F 的需求**。它将离散的元优化框架替换为完全可微的优化器，利用目标任务的在线优化数据（种群与适应度）通过梯度下降自适应更新参数，实现了真正的零样本、任务无关优化。

### 2. 方法谱系：从传统 BBO 到 ABOM

#### 2.1 传统黑盒优化基线

ABOM 对比了多类传统 BBO 方法，代表了该领域的主要技术路线：

- **随机搜索基线**：**Random Search (RS)** (Bergstra & Bengio, 2012)，作为最基本的性能下界。
- **群智能方法**：**Particle Swarm Optimization (PSO)** (Kennedy & Eberhart, 1995) 及其自适应变体 **SAHLPSO** (Tao et al., 2021)。
- **进化算法**：**Differential Evolution (DE)** (Storn & Price, 1997) 及其自适应变体 **JDE21** (Brest et al., 2021)。
- **先进自适应策略**：**CMAES** (Hansen, 2016; Ollivier et al., 2017)，作为自适应进化策略的代表，在多个基准上长期占据领先地位。

这些方法的核心特征是**固定算子与手工调参**，其性能上限受限于人类专家的设计能力。

#### 2.2 元黑盒优化基线

MetaBBO 代表了从“手工设计”到“学习设计”的范式转变。ABOM 对比了以下代表性方法：

- **基于元学习的 PSO 优化器**：**GLEET** (Ma et al., 2024)，通过元学习自动调整 PSO 的超参数。
- **基于元学习的 DE 优化器**：**RLDEAFL** (Guo et al., 2025)，利用强化学习在任务分布上训练 DE 的策略。
- **基于元学习的 ES 优化器**：**LES** (Lange et al., 2023b)，学习进化策略的元参数。
- **基于元学习的解操控方法**：**GLHF** (Li et al., 2024)，通过元学习直接操控解的生成过程。

这些方法的共同局限在于：**元训练阶段依赖预定义的任务分布 F**。当目标任务的特性偏离训练分布时，元策略的性能会显著退化。ABOM 与这些方法的本质区别在于**算法搜索空间**和**训练范式**两个维度的根本性改变：

| 维度 | MetaBBO 基线 | ABOM |
|------|-------------|------|
| 算法搜索空间 | 离散且需要人工设计的算法搜索空间 A | 连续可微参数空间 θ，通过梯度学习自动调整 |
| 训练任务分布 | 必须提供手工设计的训练任务分布 F | 零样本、任务无关，仅利用目标任务的在线优化数据 |
| 进化算子 | 固定的启发式算子及其手动调参 | 基于注意力的可微算子，内置 Dropout 探索，由 AdamW 在线更新 |

### 3. 适用边界与性能特征

#### 3.1 已验证的优势场景

- **高维连续优化**：在 BBOB 测试套件（d=500）上，ABOM 在多个函数上显著优于所有基线，包括长期占据领先地位的 CMAES。例如在 f6 上，ABOM 达到 6.201e+3 ± 6.326e+2，而 CMAES 为 2.164e+4 ± 6.814e+3（Wilcoxon 检验 p<0.05）。
- **零样本泛化**：在 UAV 路径规划的 28 个地形上，ABOM 无需任何预训练即可实现最快收敛和最低最终成本，而所有 MetaBBO 基线均已在合成问题分布上进行了预训练。
- **可解释的搜索模式**：可视化分析揭示，ABOM 学习到的选择矩阵呈现出对高适应度个体的选择偏向，变异矩阵从随机初始化演化为有序结构，表明其自发涌现了类似自然选择和基因重组的统计显著搜索模式。

#### 3.2 已知局限与失效模式

1. **高维计算瓶颈**：ABOM 的计算复杂度包含 O(d³) 项，主要源于变异模块中的基因维度自注意力机制。当问题维度 d 极大时，计算开销可能限制其可扩展性。

2. **边界与约束问题**：收敛理论假设搜索空间紧致且全局最优点位于内部。当最优点在边界或存在显式约束时，理论保证不直接成立。

3. **极端复杂景观的挑战**：在部分 BBOB 函数（如 f10）上，ABOM 相对于精细调优的 CMAES 等自适应方法仍有差距，表明在极端复杂景观上仍存在改进空间。

4. **硬件依赖**：框架依赖 GPU 加速以获得可接受的迭代效率，尚未针对纯 CPU 环境进行专门优化。

5. **固定架构限制**：当前种群规模与模型容量在整个优化过程中保持固定，缺乏动态调整机制。

### 4. 开放问题与未来方向

1. **计算效率优化**：能否通过稀疏或低秩注意力机制将 O(d³) 的计算瓶颈降至更低？这是 ABOM 走向大规模应用的关键。

2. **动态架构自适应**：如何实现种群大小和模型容量在优化过程中的动态自适应，以在不同阶段分配合理的计算资源？

3. **收敛速率分析**：ABOM 在不同问题结构下的收敛速率（期望到达时间）尚未得到理论刻画，这是理解其效率边界的重要问题。

4. **混合训练范式**：结合预训练与在线微调的混合范式（如 ABOM-PT）能否进一步改善零样本泛化？初步实验表明，即使低相似度任务的预训练也能传递部分可迁移的优化知识，但这一现象的机制尚不明确。

5. **问题类型扩展**：ABOM 在约束优化、离散优化或多目标优化问题上的表现如何？当前框架主要针对无约束连续优化设计。

6. **知识迁移机制**：在 ABOM-PT 中，低相似度任务究竟传递了何种可迁移的优化知识？如何更有效地利用这些知识是一个值得深入探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Task_free_Adaptive_Meta_Black_box_Optimization.pdf]]
