---
title: "Pareto-Conditioned Diffusion Models for Offline Multi-Objective Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pareto_Conditioned_Diffusion_Models_for_Offline_Multi_Objective_Optimization.pdf
openreview_forum_id: S2Q00li155
aliases:
- PPCD
- PCDMOMOO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "直接以期望的目标折衷（target trade-offs）作为条件信号，通过条件扩散模型在单个端到端框架中完成解生成，消除了对代理模型的需求；同时，引入基于支配数的多目标重加权策略，使模型聚焦于高性能区域，并利用参考方向向量构建多样化的条件点，引导生成超出观测数据的新解。"
primary_logic: "将离线多目标优化转化为条件生成问题，利用条件扩散模型直接建模 p(x|y)，从而将解生成与帕累托前沿建模统一；通过重加权数据训练和参考方向驱动的条件点生成，模型可以在无需代理函数近似的情况下，从静态数据中泛化出高质量且多样化的帕累托解集。"
claims:
- "PCD 在五个任务大类的100分位超体积平均排名中取得最佳（4.80），显著优于所有代理模型基线和生成式基线 ParetoFlow。"
- "消融实验证实，所提出的重加权策略在多个代表性任务上一致且显著优于简单的数据修剪策略。"
- "参考方向机制生成的多样化条件点相比简单策略（如直接使用理想点）可带来接近翻倍的超体积提升。"
- "Overall (5 task categories: Synthetic, MORL, RE, Scientific, MONAS) 上 Average Rank (100th percentile HV, ↓) = 4.80 ± 0.30"
---

# Pareto-Conditioned Diffusion Models for Offline Multi-Objective Optimization

> [!tip] 核心洞察
> 将离线多目标优化转化为条件生成问题，利用条件扩散模型直接建模 p(x|y)，从而将解生成与帕累托前沿建模统一；通过重加权数据训练和参考方向驱动的条件点生成，模型可以在无需代理函数近似的情况下，从静态数据中泛化出高质量且多样化的帕累托解集。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向离线多目标优化的帕累托条件扩散模型 |
| 英文题名 | Pareto-Conditioned Diffusion Models for Offline Multi-Objective Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=S2Q00li155); [Project](https://sites.google.com/view/pcd-iclr26) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | PCD (Pareto-Conditioned Diffusion) |
| Dataset | Overall (5 task categories: Synthetic, MORL, RE, Scientific, MONAS), Real‑World Applications (RE), Synthetic ZDT2 |

> [!tip] 效果简介
> - Overall (5 task categories: Synthetic, MORL, RE, Scientific, MONAS) 上，Average Rank (100th percentile HV, ↓) 为 4.80 ± 0.30，对比 E2E 5.71 ± 0.16 (best baseline avg rank)，变化 −0.91。
> - Real‑World Applications (RE) 上，Average Rank (100th percentile HV, ↓) 为 1.51 ± 0.13，对比 E2E 6.06 ± 0.30，变化 −4.55。
> - Synthetic ZDT2 上，100th percentile Hypervolume (↑) 为 6.25 ± 0.06，对比 ParetoFlow 6.15 ± 0.05，变化 +0.10。

## 概述

离线多目标优化（Offline Multi-Objective Optimization）的核心挑战在于：从静态、分布不均的数据集中，生成超越已观测范围的高质量帕累托解集。传统方法依赖显式代理模型拟合目标函数，再使用多目标搜索算法（如NSGA-II）在代理模型上寻优。然而，代理模型的拟合误差会在搜索过程中被持续放大，导致生成的解不可靠；同时，高维搜索空间与缺乏多目标平衡的可控信号，进一步加剧了泛化困难。

**PCD（Pareto-Conditioned Diffusion）** 将离线多目标优化重新定义为条件生成问题，在单个端到端框架中统一了解生成与帕累托前沿建模。其核心机制包括两个关键创新：

1. **多目标重加权训练**：基于支配数（dominance number）对训练样本进行分箱加权，使条件扩散模型聚焦于帕累托前沿附近的高性能区域，而非均匀拟合整个数据分布。
2. **参考方向驱动的条件点生成**：利用Riesz s-Energy生成方向向量，经非支配排序分配数据点，再沿方向向量外推并注入高斯噪声，产生兼具高质量与多样性的目标条件点，引导采样探索训练数据之外的新区域。

在涵盖合成问题、多目标强化学习（MORL）、现实工程应用、科学设计与多目标神经架构搜索（MONAS）五类任务的基准测试中，PCD取得了最佳综合平均排名（100分位超体积排名 4.80 ± 0.30），显著优于所有代理模型基线及生成式基线ParetoFlow。消融实验证实，重加权策略在多个代表性任务上一致优于简单数据修剪；参考方向机制相比简单条件点选择策略（如直接使用理想点）可带来接近翻倍的超体积提升。

PCD的主要局限在于：高维MORL任务（如MO-Hopper）中所有方法均未能显著超越离线数据集中的已知非支配解；重加权温度τ需针对数据集特性调整；当前框架尚未覆盖离散/组合优化任务。

## 背景与动机

### 离线多目标优化的核心挑战

多目标优化（Multi-Objective Optimization, MOO）广泛存在于工程设计与科学发现中，其目标是同时最小化（或最大化）多个相互冲突的目标函数：

$$\operatorname*{min}_{\mathbf{x}\in\mathcal{X}} \mathbf{f}(\mathbf{x}) = [f_1(\mathbf{x}), \ldots, f_m(\mathbf{x})]$$

由于目标间的冲突，不存在单一最优解，而是需要寻找一组帕累托最优解，构成帕累托前沿。然而，在许多现实场景中，目标函数的在线评估极其昂贵甚至危险——例如药物分子的湿实验验证、航空发动机的物理测试。这催生了**离线多目标优化**范式：仅利用预先收集的静态数据集 $\mathcal{D} = \{(\mathbf{x}_i, \mathbf{f}(\mathbf{x}_i))\}$ 来发现超越数据集中已有解的高质量候选解。

这一范式面临一个根本性瓶颈：**从静态数据中泛化至超出观测的高质量区域极其困难**。具体而言，挑战源于三个层面：

1. **代理模型误差放大**：传统方法依赖显式代理模型（如深度神经网络或高斯过程）拟合各目标函数，再借助多目标进化算法（如 NSGA-II）在代理模型上搜索。但代理模型在数据稀疏区域的预测误差会在搜索过程中被反复放大，导致最终生成的解不可靠。

2. **数据分布不均**：静态数据集的采样往往偏向低性能区域，帕累托前沿附近的高质量样本稀疏，使得模型难以在这些关键区域获得足够的监督信号。

3. **多目标平衡信号缺失**：高维搜索空间中，缺乏有效控制多个目标间折衷关系的机制，使得生成解难以同时兼顾多样性与质量。

### 现有方法的局限性

当前离线多目标优化的主流方法可分为两类：

**代理模型 + 搜索方法**：先训练代理模型近似目标函数，再用进化算法搜索。典型代表包括端到端 DNN 代理模型配合 NSGA-II（E2E），以及多模型分别拟合各目标后结合保守优化策略（如 COMs、ICT、IOM、Tri-Mentoring）。这类方法的根本缺陷在于：代理模型与搜索过程解耦，前者在数据稀疏区域的误差被后者的贪婪搜索放大，导致生成解偏离真实帕累托前沿。

**生成式方法**：ParetoFlow 首次将流匹配引入离线 MOO，通过代理预测器引导生成过程。但其仍然依赖显式的代理模型作为中间引导机制，未能从根本上消除误差放大的风险。

### 本文动机与核心思路

PCD 的出发点是一个关键洞察：**将离线多目标优化重新定义为条件生成问题**，直接建模 $p(\mathbf{x}|\mathbf{y})$，其中条件向量 $\mathbf{y}$ 表示期望的目标折衷。这一视角转换带来了范式层面的突破：

- **消除代理模型依赖**：通过条件扩散模型直接学习从目标条件到解的映射，端到端完成解生成，无需任何中间代理函数近似。
- **统一生成与前沿建模**：条件扩散模型的采样过程天然产生多样化候选解，将解生成与帕累托前沿建模统一在单个框架内。
- **可控的多目标平衡**：以期望的目标折衷作为显式条件信号，通过 Classifier-Free Guidance 引导采样朝向特定偏好区域，实现了对多目标平衡的直接控制。

为实现这一框架，PCD 引入了两项关键技术：（1）基于支配数的多目标重加权策略，使训练聚焦于帕累托前沿附近的高质量区域；（2）参考方向驱动的条件点生成机制，通过外推和噪声注入产生超出观测数据的多样化目标条件，引导模型泛化至新区域。

## 核心创新

PCD 的核心创新在于将离线多目标优化（MOO）重新定义为**条件生成问题**，从而在单一端到端框架中统一了解生成与帕累托前沿建模，彻底消除了对显式代理模型和多目标搜索算法的依赖。这一范式转变通过三个紧密耦合的机制实现，每个机制都针对传统代理模型方法的根本性缺陷。

### 创新一：端到端条件扩散生成范式

传统离线 MOO 方法遵循“先训练代理模型拟合目标函数，再用进化算法（如 NSGA-II）在代理模型上搜索”的两阶段流程。这一流程存在一个关键的误差放大问题：代理模型在远离训练数据的区域预测精度有限，而搜索算法天然倾向于探索这些不确定区域，导致生成解不可靠。PCD 直接建模 $p(\mathbf{x}|\mathbf{y})$——即给定目标折衷条件下解的分布——将优化问题转化为从学习到的条件分布中采样。训练阶段，条件扩散模型学习从噪声中恢复高质量解；推理阶段，只需指定期望的目标条件点 $\hat{\mathbf{y}}$，即可通过 Classifier-Free Guidance 采样直接生成对应解，无需任何中间代理模型或搜索步骤。

这一范式转变的因果逻辑在于：代理模型方法试图逼近整个目标函数景观，但只有帕累托前沿附近的高性能区域对优化真正重要；PCD 通过条件生成直接聚焦于“给定目标值应生成什么解”这一更具针对性的问题，从根本上规避了代理误差在搜索中被放大的风险。

### 创新二：基于支配数的多目标重加权训练

直接从静态数据集中均匀采样训练条件扩散模型存在一个严重问题：数据集中低质量解占多数，均匀训练会使模型分散注意力，降低对帕累托前沿附近关键区域的建模精度。PCD 提出了一种基于**支配数（dominance number）**的多目标重加权策略来解决这一问题。

支配数定义为解被数据集中其他解帕累托支配的次数：

$$o(\mathbf{x}) := \sum_{\mathbf{x}' \in \mathcal{D}} \mathbb{I}[\mathbf{f}(\mathbf{x}) \prec \mathbf{f}(\mathbf{x}'), \mathbf{x} \neq \mathbf{x}']$$

支配数越低，解的质量越高。PCD 将目标空间划分为多个分箱（bin），为每个分箱 $B_i$ 计算权重：

$$w_i = \frac{|B_i|}{|B_i| + K} \exp\Big(\frac{-\frac{1}{|B_i|}\sum_{j=1}^{|B_i|} o(\mathbf{x}_{b_j})}{\tau}\Big)$$

该权重同时考虑了两个因素：分箱内的样本数量（通过 $|B_i|/(|B_i|+K)$ 防止样本过少的分箱被过度加权）和分箱内样本的平均质量（通过支配数的指数衰减）。最终，训练目标被修改为重加权的去噪 L2 损失：

$$\theta = \arg\min_{\theta} \mathbb{E}_{(\mathbf{x},\mathbf{y})\sim p_{\mathrm{data}},\sigma\sim p_{\mathrm{train}},\mathbf{n}\sim\mathcal{N}(0,\sigma^2\mathbb{I})} w(\mathbf{y})\lambda(\sigma)\|D_{\theta}(\mathbf{x}+\mathbf{n}; \mathbf{y}, \sigma) - \mathbf{x}\|_2^2$$

与简单的数据修剪（直接丢弃低质量点）相比，重加权策略保留了所有数据的信息，但通过软权重调整使模型聚焦于高性能区域。消融实验（Table 2）证实，重加权在所有代表性任务上一致且显著优于修剪策略，验证了其在聚焦高质量样本方面的关键作用。

### 创新三：参考方向驱动的多样化条件点生成

推理时，PCD 需要一组条件点 $\Psi$ 来引导生成多样化的帕累托解集。简单的策略（如随机采样或使用理想点）无法有效覆盖帕累托前沿，尤其是在前沿形状复杂或高维目标空间中。PCD 提出了一种**参考方向机制**，通过两阶段过程生成兼具高质量与多样性的条件点：

1. **方向向量生成与点分配**：使用 Riesz s-Energy 方法在目标空间中生成均匀分布的方向向量，类似于 NSGA-III 的生存选择机制。然后通过非支配排序对数据集中的解进行分层，将每个方向向量分配给垂直距离最近的点，确保前沿各个区域都有代表点。

2. **外推与噪声注入**：将分配的点沿其对应的方向向量向外推，以探索超出观测数据的新区域；随后添加零均值高斯噪声，进一步增强条件点的多样性。

这一机制的关键因果效应在于：外推使模型能够生成**超出训练数据覆盖范围**的解，而噪声注入确保了生成解之间的多样性。消融实验（Table 2）表明，该机制相比直接使用理想点策略在 MO-Swimmer 任务上带来了接近翻倍的超体积提升，验证了其在推动泛化至新颖区域方面的核心作用。

### 三个创新的协同关系

上述三个创新并非孤立运作，而是形成了一个因果闭环：重加权训练确保模型在帕累托前沿附近具有高精度的生成能力；参考方向机制生成覆盖前沿且超越观测数据的多样化条件点；Classifier-Free Guidance 采样则将条件信号转化为实际的高质量解。三者共同实现了从静态数据到高质量帕累托解集的端到端映射，无需任何代理函数近似。实验结果表明，这一协同设计使 PCD 在五个任务大类上取得了最佳平均排名（4.80），显著优于所有代理模型基线和生成式基线 ParetoFlow，且这一结果是在使用统一、固定超参数集的情况下取得的，凸显了方法的鲁棒性和泛化能力。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the conditioning points generation procedure: a) The objective space is partitioned via direction vectors, and points are ranked based on non-dominated sorting. b) Each direction vector is paired with the point closest to it in perpendicular distance (black arrow). The rest of the points are paired to the vector with the least amount of assigned points (gray arrow). c) A diverse set of conditioning points is generated by extrapolating the assigned points along the direction vectors and adding Gaussian noise*

PCD 将离线多目标优化（MOO）重新定义为条件生成问题：给定一个静态数据集 $\mathcal{D} = \{(\mathbf{x}_i, \mathbf{y}_i)\}_{i=1}^N$，其中 $\mathbf{x}$ 为候选解，$\mathbf{y} = \mathbf{f}(\mathbf{x})$ 为对应的目标值向量，模型直接学习条件分布 $p(\mathbf{x} \mid \mathbf{y})$，并在推理时以期望的目标折衷（target trade-offs）作为条件信号，通过单次采样生成高质量解集。这一端到端范式彻底消除了传统方法中“先训练代理模型、再用多目标搜索算法优化代理模型”的两阶段依赖，从根本上避免了代理模型误差在搜索中被放大的核心瓶颈。

框架由三个紧密协作的模块构成，形成“数据重加权训练 → 条件点生成 → 引导采样”的完整闭环：

**1. 重加权去噪训练（Reweighted Denoising Training）**
在标准条件扩散模型的去噪训练目标之上，PCD 引入基于支配数（dominance number）的多目标分箱重加权策略。具体而言，对数据集中每个解 $\mathbf{x}$ 计算其被其他解 Pareto 支配的次数 $o(\mathbf{x})$（值越低表示质量越高），随后将目标空间划分为若干分箱 $B_i$，每个分箱的权重 $w_i$ 由箱内样本数量和平均支配数共同决定：
$$w_i = \frac{|B_i|}{|B_i| + K} \exp\Big(\frac{-\frac{1}{|B_i|}\sum_{j=1}^{|B_i|} o(\mathbf{x}_{b_j})}{\tau}\Big)$$
该权重 $w(\mathbf{y})$ 直接作用于去噪 L2 损失，使模型在训练时自动聚焦于 Pareto 前沿附近的高性能区域，而对低质量区域的建模精度要求大幅降低。消融实验证实，这一重加权策略在所有代表性任务上均一致且显著优于简单的数据修剪（pruning）策略（Table 2）。

**2. 条件点生成（Conditioning Point Generation）**
推理时需要一组多样化的目标条件点 $\Psi = \{\hat{\mathbf{y}}_j\}_{j=1}^J$ 来引导采样覆盖 Pareto 前沿的不同区域。PCD 采用类似 NSGA-III 生存选择的两阶段机制（Figure 2）：首先通过 Riesz s-Energy 方法在目标空间生成均匀分布的方向向量，再基于非支配排序将数据集中的优质解分配给各方向向量；随后，每个被分配的点沿其方向向量向外推（extrapolation），并叠加零均值高斯噪声，从而生成既超出观测数据范围、又保持多样性的条件点。这一机制相比简单策略（如直接使用理想点或随机采样）可带来接近翻倍的超体积提升（MO-Swimmer 任务上，Section 5.4）。

**3. 无分类器引导采样（Classifier-Free Guided Sampling）**
对每个条件点 $\hat{\mathbf{y}}$，采样过程采用 Classifier-Free Guidance（CFG），通过加权组合条件去噪器预测 $D_\theta(\mathbf{x}; \hat{\mathbf{y}}, \sigma)$ 和无条件去噪器预测 $D_\theta(\mathbf{x}; \sigma)$ 来引导生成方向：
$$\hat{D}_\theta(\mathbf{x}; \hat{\mathbf{y}}, \sigma) = \gamma D_\theta(\mathbf{x}; \hat{\mathbf{y}}, \sigma) + (1 - \gamma) D_\theta(\mathbf{x}; \sigma)$$
引导尺度 $\gamma$ 控制生成解与目标条件的贴合程度。实验表明，$\gamma$ 在 2.5 以内时性能逐步提升，之后趋于饱和甚至略有下降（Figure 3），说明适度引导已足够有效。

**输入输出流总结：**
- **训练阶段**：输入为静态数据集 $\mathcal{D}$ 中的 $(\mathbf{x}, \mathbf{y})$ 对，经支配数计算和分箱重加权后，训练条件扩散去噪器 $D_\theta$。
- **推理阶段**：输入为期望的条件点数量 $J$ 和引导尺度 $\gamma$；先通过参考方向机制生成条件点集 $\Psi$，再对每个 $\hat{\mathbf{y}} \in \Psi$ 运行 CFG 引导的扩散采样，输出候选解集 $\{\mathbf{x}_j\}_{j=1}^J$，最终通过非支配排序提取 Pareto 前沿解集。

整个框架使用统一、固定的超参数集（Table 3），无需针对不同任务类别单独调参，在合成、MORL、现实工程、科学设计和 MONAS 五大类任务上均展现出强鲁棒性。

## 核心模块与公式推导

PCD 将离线多目标优化重新定义为条件生成问题，其核心由三个紧密耦合的模块构成：**重加权去噪训练**、**条件点生成** 和 **无分类器引导采样**。以下逐一剖析其机理与关键公式。

---

### 模块一：重加权去噪训练

**动机**：标准扩散模型对训练样本均匀对待，但离线 MOO 中低质量解的大量存在会稀释模型对 Pareto 前沿附近高性能区域的建模能力。PCD 通过引入基于支配数的多目标重加权策略，使训练聚焦于高质量样本。

**支配数定义**：给定数据集 $\mathcal{D}$，解 $\mathbf{x}$ 的支配数 $o(\mathbf{x})$ 计算其被数据集中其他解 Pareto 支配的次数：

$$o(\mathbf{x}) := \sum_{\mathbf{x}' \in \mathcal{D}} \mathbb{I}[\mathbf{f}(\mathbf{x}) \prec \mathbf{f}(\mathbf{x}'), \mathbf{x} \neq \mathbf{x}']$$

其中 $\mathbf{f}(\mathbf{x}) \prec \mathbf{f}(\mathbf{x}')$ 表示 $\mathbf{x}$ 在所有目标上不劣于 $\mathbf{x}'$ 且至少在一个目标上严格更优。支配数越低，解的质量越高（非支配解的支配数为 0）。

**分箱重加权**：将目标空间划分为 $B$ 个箱，对第 $i$ 个箱 $B_i$，其权重 $w_i$ 由箱内样本数量和平均支配数共同决定：

$$w_i = \frac{|B_i|}{|B_i| + K} \exp\Big(\frac{-\frac{1}{|B_i|}\sum_{j=1}^{|B_i|} o(\mathbf{x}_{b_j})}{\tau}\Big)$$

- $|B_i|$：箱内样本数，因子 $\frac{|B_i|}{|B_i|+K}$ 防止小箱被过度加权（$K$ 为平滑常数）
- $\frac{1}{|B_i|}\sum o(\mathbf{x}_{b_j})$：箱内平均支配数，反映该区域整体质量
- $\tau$：温度参数，控制质量差异的放大程度。高方差数据集（如 ZDT2）需增大 $\tau$ 以强化对前沿区域的聚焦（Figure 5）

**重加权去噪目标**：将箱权重 $w(\mathbf{y})$ 注入标准去噪训练目标，条件 $\mathbf{y}$ 落入某箱时继承该箱权重：

$$\theta = \arg\min_{\theta} \mathbb{E}_{(\mathbf{x},\mathbf{y})\sim p_{\mathrm{data}},\sigma\sim p_{\mathrm{train}},\mathbf{n}\sim\mathcal{N}(0,\sigma^2\mathbb{I})} w(\mathbf{y})\lambda(\sigma)\|D_{\theta}(\mathbf{x}+\mathbf{n}; \mathbf{y}, \sigma) - \mathbf{x}\|_2^2$$

其中 $D_{\theta}$ 为去噪网络，$\lambda(\sigma)$ 为噪声水平相关的损失权重，$\mathbf{n}$ 为加性高斯噪声。该目标使模型在高权重区域（Pareto 前沿附近）的去噪精度更高。

**关键证据**：消融实验（Table 2）证实，重加权策略在所有代表性任务上一致且显著优于简单数据修剪（仅删除低质量点），验证了基于支配数的软加权对聚焦高质量样本至关重要。

---

### 模块二：条件点生成

**动机**：采样时需要一组多样化的目标条件点 $\Psi = \{\hat{\mathbf{y}}_j\}_{j=1}^J$，既覆盖 Pareto 前沿的已知区域，又外推至可能超越观测数据的新区域。PCD 设计了基于参考方向向量的两阶段生成过程（Figure 2）。

**阶段 1：方向向量生成与点分配**
- 使用 Riesz $s$-Energy 方法在目标空间中生成均匀分布的 $J$ 个方向向量，确保对 Pareto 前沿的全面覆盖
- 对数据集进行非支配排序，提取多层前沿 $F_1, F_2, \dots$
- 将每个方向向量分配给与其垂直距离最近的数据点，优先分配高质量前沿的点；剩余点按负载均衡原则分配

**阶段 2：外推与噪声注入**
- 对每个分配的点，沿其方向向量向外推一定距离，生成超出观测数据的目标候选
- 对外推点添加零均值高斯噪声，引入随机性以增加条件点的多样性

最终条件点集 $\Psi$ 兼具高质量（源于非支配前沿）与多样性（源于方向向量覆盖和外推噪声），引导模型探索 Pareto 前沿的新区域。

**关键证据**：Table 2 显示，参考方向机制相比简单策略（如直接使用理想点 Ideal 或随机采样 Random）带来显著性能提升，在 MO-Swimmer 任务上超体积近乎翻倍。Figure 6 进一步表明，增加噪声尺度和外推距离在一定范围内正向影响性能，但外推距离过大时收益递减。

---

### 模块三：无分类器引导采样

**动机**：条件扩散模型本身已能根据 $\hat{\mathbf{y}}$ 生成对应解，但无分类器引导（Classifier-Free Guidance, CFG）可进一步强化生成解与目标条件的贴合度。

**CFG 更新规则**：在每个去噪步，将条件预测 $D_{\theta}(\mathbf{x}; \hat{\mathbf{y}}, \sigma)$ 与无条件预测 $D_{\theta}(\mathbf{x}; \sigma)$ 线性组合：

$$\hat{D}_{\theta}(\mathbf{x}; \hat{\mathbf{y}}, \sigma) = \gamma D_{\theta}(\mathbf{x}; \hat{\mathbf{y}}, \sigma) + (1 - \gamma) D_{\theta}(\mathbf{x}; \sigma)$$

其中 $\gamma \ge 1$ 为引导尺度。当 $\gamma = 1$ 时退化为纯条件采样；$\gamma > 1$ 时放大条件信号与无条件先验的差异，推动生成解更精准地匹配目标 trade-off。

**关键证据**：Figure 3 的参数分析表明，$\gamma$ 在 0–2.5 范围内增大时性能提升，之后趋于饱和甚至略有下降，说明适度引导已足够，过强引导可能损害生成多样性。

---

### 整体流程

PCD 的完整训练与采样过程可概括为：
1. **训练阶段**：对静态数据集计算支配数并分箱重加权，以重加权 L2 目标训练条件去噪器 $D_{\theta}$
2. **采样阶段**：通过参考方向机制生成 $J$ 个条件点 $\hat{\mathbf{y}}_j$，对每个条件点运行 CFG 引导的扩散采样，产生候选解集 $\{\mathbf{x}_j\}_{j=1}^J$

该端到端框架消除了对显式代理模型和独立优化器的需求，将 Pareto 前沿建模与解生成统一于单一条件扩散模型之中。

## 实验与分析

### 核心实验设置

所有方法在统一的评估协议下比较：对每个任务生成 $Q=256$ 个候选解，计算前 $P \in \{100, 75, 50\}$ 百分位的超体积（Hypervolume, HV），结果基于 5 个随机种子报告均值±标准差。实验覆盖 Offline MOO 基准的五大任务类别：合成问题（Synthetic）、多目标强化学习（MORL）、现实世界应用（RE）、科学设计（Scientific Design）和多目标神经架构搜索（MONAS）。值得强调的是，PCD 在整个实验中使用了**统一、固定的超参数集**（见 Table 3），未针对不同任务类别单独调参，而多数代理模型基线可能受益于任务特定的调参——这使得 PCD 的跨任务鲁棒性结论更具说服力。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/008_Table_3.jpg]]
*Table 3: Default hyperparameters for PCD framework including Residual MLP Denoiser for reweighted training (left) and EDM Sampling (right). If multiple values were used, bolded value indicates default value*

基线方法分为三类：(1) **代理模型+搜索**：包括端到端 DNN 代理配合 NSGA-II（E2E）、结合 PCGrad 梯度冲突缓解（E2E+PC）、结合 GradNorm 动态权重平衡（E2E+GN），以及多模型分别拟合各目标再配合保守优化（MM+COMs）、领域适应（MM+ICT）、模型反转（MM+IOM）、三元指导（MM+TM），还有共享编码器的多头模型（MH）；(2) **贝叶斯优化**：基于高斯过程的多目标贝叶斯优化 qNEHVI（MOBO）；(3) **生成式方法**：基于流匹配的 ParetoFlow，依赖代理预测器引导。此外，离线数据集中已存在的非支配解集合 D(best) 作为性能下界参考。

---

### 主结果：跨任务一致性与性能优势

**Table 1** 汇总了各方法在五类任务中的 100 分位 HV 平均排名（↓）。PCD 以 **4.80 ± 0.30** 的总体平均排名取得最佳，显著优于表现最好的代理模型基线 E2E（5.71 ± 0.16）和生成式基线 ParetoFlow。这一优势在现实世界应用（RE）类别中尤为突出：PCD 的平均排名为 **1.51 ± 0.13**，而 E2E 为 6.06 ± 0.30，差距达 −4.55。即使在 PCD 相对较弱的 MORL 和 MONAS 类别中，其排名仍大幅领先 ParetoFlow。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/003_Table_1.jpg]]
*Table 1: Average rank (↓) of PCD and baseline methods across five task categories. Ranks are calculated based on the 100th percentile HV. Bold and underlined rows indicate the best and runner up methods respectively. PCD achieves the best overall average rank, demonstrating its strong and consistent performance*

**Table 2** 展示了五个代表性任务上的 100 分位 HV 绝对值。PCD 在 MO-Swimmer-v2（3.69±0.11）、RE34（10.17±0.04）和 C10/MOP2（10.59±0.04）上取得最佳，在 ZDT2（6.25±0.06）上为次优。在合成任务 ZDT2 上，PCD 超越 ParetoFlow 约 0.10 的 HV 绝对值，验证了条件扩散框架相对于流匹配方法的优势。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/004_Table_2.jpg]]
*Table 2: Average 100th percentile HV (↑) on 5 representative tasks with different data processing and sampling strategies. Bold and underlined rows indicate the best and runner up methods respectively. The results validate the effectiveness of both our proposed reweighting and referencedirection mechanisms*

**关键因果机制**：PCD 的一致性优势源于其端到端条件生成范式——直接建模 $p(\mathbf{x}|\mathbf{y})$ 消除了代理模型误差在搜索中被放大的风险。传统方法中，代理模型对目标函数的近似误差会经 NSGA-II 等搜索算法迭代累积，导致生成的解不可靠；PCD 通过条件扩散模型一步到位地生成与目标折衷匹配的解，切断了这一误差传播链。

---

### 消融分析：重加权与参考方向机制的必要性

**Table 2** 的系统消融揭示了两个核心设计的独立贡献：

**多目标重加权 vs. 数据修剪**：相比于仅使用数据修剪（pruned，即简单丢弃低质量样本），加入基于支配数的分箱重加权在所有五个代表性任务上均获得更高 HV。重加权策略通过式 (6) 的权重方案：

$$w_i = \frac{|B_i|}{|B_i| + K} \exp\Big(\frac{-\frac{1}{|B_i|}\sum_{j=1}^{|B_i|} o(\mathbf{x}_{b_j})}{\tau}\Big)$$

同时考虑箱内样本数量与平均支配数，使模型聚焦于 Pareto 前沿附近的高质量区域，而非均匀对待所有数据。

**参考方向机制 vs. 简单条件点策略**：将条件点生成策略从参考方向机制替换为随机采样（Random）或理想点（Ideal），性能大幅下降。在 MO-Swimmer 任务上，参考方向机制相比 Ideal 策略带来了**接近翻倍的 HV 提升**。该机制（Figure 2）通过三个子步骤实现：(a) 用 Riesz s-Energy 生成方向向量并基于非支配排序分配点；(b) 将每个方向向量与其垂直距离最近的点配对；(c) 沿方向向量外推并加高斯噪声，产生兼具高质量与多样性的条件点 $\Psi$。外推步骤使条件点超越训练数据中已观测的目标值范围，是生成新 Pareto 解的关键。

---

### 参数敏感性分析

**引导尺度 $\gamma$（Figure 3）**：Classifier-Free Guidance 的引导强度仅在 $\gamma < 2.5$ 时带来性能提升，之后饱和甚至略有下降。这表明适度引导已足以使采样朝向目标折衷区域，过强的条件信号反而可能限制生成多样性。

**重加权温度 $\tau$（Figure 5）**：在高方差数据集（如 ZDT2，其支配数分布呈长尾，见 Figure 4）上，增大 $\tau$ 显著提升性能，因为更强的温度使重加权更激进地聚焦于少数高质量样本；而在低方差数据集（如 C10/MOP2、MO-Hopper，支配数分布集中）上，$\tau$ 的影响极小。这解释了重加权在不同数据集上效果差异的根源：**数据集质量方差越大，重加权的收益越显著**。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/006_Figure_4.jpg]]
*Figure 4: Normalized dominance number distributions reveal dataset quality differences. The narrow distributions of C10/MOP2 and MO-Hopper indicate consistently high-quality datasets, whereas the long-tailed distribution of ZDT2 signals high variance in sample quality*

**条件点数量 $J$（Table 6）**：增加 $J$ 总体上提升性能，$J=32$ 在多数任务中取得最佳结果，表明丰富的条件点能更好地覆盖 Pareto 前沿。但收益在 $J>32$ 后趋于饱和。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/011_Table_6.jpg]]
*Table 6: Average 100th percentile Hypervolume (↑) on 5 different tasks using varying numbers of conditioning points J. Bold and underlined rows indicate the best and runner up methods respectively. Increasing the number of selected points generally yields higher performance, with J = 3 2 achieving the best results on the majority of tasks*

**采样器选择（Table 5）**：默认的随机 EDM 采样器在大多数任务上优于确定性 ODE 采样器，验证了随机性在探索解空间中的价值。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/010_Table_5.jpg]]
*Table 5: Average 100th percentile HV (↑) on 5 different tasks comparing EDM with stochastic and deterministic samplers. Bold and underlined rows indicate the best and runner up methods respectively. The default stochastic sampler shows superior performance on most tasks*

**去噪步数（Figure 7）**：PCD 对去噪步数选择稳健，即使在较少步数下也能生成高质量解，说明模型学习到了有效的去噪轨迹。

---

### 失败模式与局限性

**高维搜索空间的泛化瓶颈**：在 MORL 任务（如 MO-Hopper）中，所有方法均未能产生显著优于离线数据集中已知非支配解的新解。Figure 8（左）显示，在高维 MO-Hopper 任务上，模型难以在第一个目标上取得改进；Figure 9（左）进一步揭示，模型甚至无法重建其训练所用的数据分布。这表明条件扩散模型在高维搜索空间中面临严重的数据分布拟合困难，条件信号的有效性随搜索空间维度增加而衰减。相比之下，在低维 RE21 任务上（Figure 8 右、Figure 9 右），条件作用高度有效：生成点 $\mathbf{y}_{\text{out}}$ 与条件目标 $\hat{\mathbf{y}}$ 紧密对齐，甚至超越后者。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/015_Figure_8.jpg]]
*Figure 8: Qualitative analysis of Pareto-conditioning effectiveness. Left (MO-Hopper): On this high-dimensional task, the model struggles to generate solutions that improve upon the first objective. Right (RE21): On this lower-dimensional task, the conditioning is highly effective: the generated points ( $\boldsymbol { y } _ { \mathrm { o u t } }$ ) closely align with and even outperform their conditioning targets (yˆ)

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/016_Figure_9.jpg]]
*Figure 9: Analysis of the model’s ability to reconstruct the original data distribution. Colors represent distinct non-dominated fronts ( $F _ { i }$ ) extracted from the training set. The model is conditioned on the objective vectors of the original data (circles, yˆ); successful reconstruction is achieved if the generated solutions (crosses, $y _ { \mathrm { o u t } }$ ) overlap with these circles. Left (MO-Hopper): In this high-dimensional task, the model is unable to capture the original data distribution it was trained on. Right (RE21): In this simpler task, the model faithfully reconstructs the original conditioning points*

**重加权对超参数的依赖性**：在高方差数据集上，若温度 $\tau$ 设置不当，重加权可能损害性能。Figure 5 显示 ZDT2 对 $\tau$ 高度敏感，而低方差数据集几乎不受影响——这要求针对数据集特性调整 $\tau$，增加了离线调参的难度。

**范畴限制**：论文明确排除了纯离散/组合优化任务，因为扩散模型直接应用于此类领域需要结构化的去噪与解码方案，当前 PCD 框架无法直接覆盖。MONAS 任务中 PCD 的表现相对较弱，可能部分源于此范畴差异。

**方向向量生成方法的轻微影响**：Table 7 显示，简单的 Das-Dennis 方法在部分任务上略优于默认的 Riesz s-Energy，但差异极小，表明 PCD 对方向向量生成方式整体稳健。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/013_Table_7.jpg]]
*Table 7: Average 100th percentile HV (↑) comparing Riesz s-Energy (default) and Das-Dennis methods for generating direction vectors. Bold rows indicate the best method. The simpler Das-Dennis method yields slightly better results, though the difference is minimal, indicating robustness*

---

### 计算效率与可扩展性

**Table 4** 的计算开销对比显示，PCD 的采样速度在四个代表性任务上均快于生成式基线 ParetoFlow，而一次性数据重加权仅增加可忽略的时间开销（秒级）。**Table 8** 的多目标可扩展性实验表明，在 DTLZ 任务的 3~6 个目标场景下，PCD 相对 D(best) 的超体积提升保持一致，未随目标数增加而衰减，验证了框架对多目标场景的扩展能力。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/009_Table_4.jpg]]
*Table 4: Computational cost comparison. We report the one-time dataset reweighting cost (seconds) and sampling times (seconds) averaged over 3 runs. PCD demonstrates faster sampling speeds compared to the generative baseline ParetoFlow across four representative tasks, while reweighting adds negligible overhead*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_S2Q00li155/figures/017_Table_8.jpg]]
*Table 8: Scalability analysis on many-objective DTLZ tasks. We report the relative Hypervolume improvement (↑) of PCD over the best offline dataset solutions (D(best)). PCD achieves consistent performance improvements regardless of the number of objectives (m)*

## 方法谱系与知识库定位

### 问题定位与核心瓶颈

离线多目标优化（Offline MOO）的核心挑战在于：从固定的静态数据集中，不仅要复现已知的帕累托前沿，更要**泛化至超出观测的高质量区域**。传统方法的主流范式是“代理模型 + 多目标搜索”：先训练显式代理模型（如深度神经网络或高斯过程）拟合各个目标函数，再使用多目标进化算法（如 NSGA-II）或梯度优化方法在代理模型上搜索。这一范式的根本瓶颈在于**代理误差的级联放大**——代理模型对目标函数的近似误差在搜索过程中被反复利用和累积，导致最终生成的候选解在真实目标函数下不可靠，尤其在数据稀疏的高性能区域，代理模型的不确定性最高，却恰恰是搜索最关注的区域。

此外，静态数据集的分布不均、高维搜索空间的稀疏性，以及缺乏平衡多个目标的直接可控信号，进一步加剧了离线多目标优化的难度。现有的梯度平衡方法（如 PCGrad、GradNorm）试图在优化过程中动态调整各目标的权重，但仍依赖代理模型的梯度信号，无法从根本上规避代理误差问题。

### PCD 的方法学定位

PCD（Pareto-Conditioned Diffusion）代表了一种**范式迁移**：将离线多目标优化从“代理建模 + 搜索”的两阶段框架，转化为**端到端的条件生成问题**。其核心思想是直接建模 $p(\mathbf{x}|\mathbf{y})$——即以期望的目标折衷向量 $\mathbf{y}$ 为条件，通过条件扩散模型直接生成对应的候选解 $\mathbf{x}$。这一转化消除了对显式代理模型的需求，将解生成与帕累托前沿建模统一在单个生成式框架中。

从方法谱系上看，PCD 位于**生成式离线优化**与**多目标优化**的交汇点。与代理模型基线（E2E、E2E+PC、E2E+GN、MH、MM+COMs、MM+ICT、MM+IOM、MM+TM、MOBO）相比，PCD 跳过了“先拟合目标函数再搜索”的中间环节。与同属生成式范式的 **ParetoFlow**（Yuan et al., 2025）相比，PCD 的关键差异在于：ParetoFlow 基于流匹配（Flow Matching），且仍依赖代理预测器进行引导；PCD 则通过条件扩散模型直接以目标折衷为条件信号，配合基于支配数的重加权训练和参考方向驱动的条件点生成，实现了对代理引导的完全解耦。

### 关键技术贡献与因果机制

PCD 的性能优势源自三个相互协同的技术组件，每个组件都针对离线多目标优化的特定瓶颈：

**1. 基于支配数的多目标重加权训练**

传统方法对训练数据采用均匀采样或简单的性能裁剪（如丢弃低质量点）。PCD 引入了基于支配数（dominance number）的分箱重加权策略：首先定义解 $\mathbf{x}$ 的支配数 $o(\mathbf{x})$ 为数据集中支配该解的样本数，然后按目标空间分箱，对每个箱 $B_i$ 赋予权重
$$w_i = \frac{|B_i|}{|B_i| + K} \exp\Big(\frac{-\frac{1}{|B_i|}\sum_{j=1}^{|B_i|} o(\mathbf{x}_{b_j})}{\tau}\Big)$$
该权重同时考虑箱内样本数量（防止稀疏箱被过度强调）和平均质量（支配数越低表示越接近帕累托前沿）。重加权后的去噪训练目标为
$$\theta = \arg\min_{\theta} \mathbb{E}_{(\mathbf{x},\mathbf{y})\sim p_{\mathrm{data}},\sigma\sim p_{\mathrm{train}},\mathbf{n}\sim\mathcal{N}(0,\sigma^2\mathbb{I})} w(\mathbf{y})\lambda(\sigma)\|D_{\theta}(\mathbf{x}+\mathbf{n}; \mathbf{y}, \sigma) - \mathbf{x}\|_2^2$$
这使得模型在训练时将容量聚焦于帕累托前沿附近的高质量区域，而对低性能区域的建模精度要求降低。

**2. 参考方向驱动的条件点生成**

采样时需要一组条件点 $\Psi$ 来引导生成。PCD 采用类似 NSGA-III 生存选择的两阶段过程：首先通过 Riesz s-Energy 生成均匀分布的方向向量，经非支配排序将训练数据中的点分配给各方向向量；然后沿方向向量外推所分配的点，并添加零均值高斯噪声，产生兼具高质量与多样性的条件点。这一机制的关键在于**外推**——条件点可以超出训练数据的观测范围，从而引导模型生成真正新颖的解，而非仅仅复现训练分布。

**3. Classifier-Free Guidance 采样**

对每个条件点 $\hat{\mathbf{y}}$，采样过程使用 Classifier-Free Guidance（CFG）：
$$\mathrm{d}\mathbf{x} / \mathrm{d}\sigma = -(\gamma D_{\theta}(\mathbf{x}; \hat{\mathbf{y}}, \sigma) + (1-\gamma) D_{\theta}(\mathbf{x}; \sigma) - \mathbf{x}) / \sigma$$
通过混合条件与无条件去噪器预测（引导尺度 $\gamma$），CFG 使生成解更贴合目标折衷区域，同时保持生成多样性。

### 实验证据强度

PCD 的核心实验结论具有较高的证据强度：

- **综合排名优势**（Table 1）：PCD 在五个任务大类（合成、MORL、RE、科学设计、MONAS）的 100 分位超体积平均排名中取得最佳（4.80 ± 0.30），显著优于最佳代理模型基线 E2E（5.71 ± 0.16）和生成式基线 ParetoFlow。值得注意的是，PCD 在所有任务中使用统一、固定的超参数集，而其他方法可能有针对任务的调参，这使得 PCD 的跨任务鲁棒性更具说服力。

- **消融实验验证**（Table 2）：重加权策略在所有代表性任务上一致且显著优于简单的数据修剪策略，证实了基于支配数的重加权对聚焦高质量样本至关重要。参考方向机制相比简单策略（如直接使用理想点）可带来接近翻倍的超体积提升（MO-Swimmer 任务上）。

- **CFG 引导尺度分析**（Figure 3）：增大引导尺度 $\gamma$ 仅在 $\gamma < 2.5$ 时带来性能提升，之后饱和甚至略有下降，表明适度引导已足够，过度引导可能损害多样性。

### 适用边界与局限

**1. 高维搜索空间的泛化瓶颈**

在 MORL 任务（如 MO-Hopper）中，PCD 与所有其他方法均未能产生显著优于离线数据集中已知非支配解的新解。定性分析（Figure 8、Figure 9）显示，在高维任务上模型甚至难以重建训练数据的原始分布，条件信号的有效性大幅下降。这表明条件扩散模型在高维搜索空间中的数据分布拟合能力存在根本性限制，需要进一步的结构化改进。

**2. 数据质量敏感性**

PCD 的重加权策略在个别高方差数据集（如 ZDT2）上若温度 $\tau$ 设置不当可能会损害性能（Figure 5）。ZDT2 的支配数分布呈长尾形态，样本质量差异大，需要较大的 $\tau$ 值来充分强调高质量区域；而在低方差数据集（如 C10/MOP2、MO-Hopper）上，$\tau$ 的影响微乎其微。这增加了离线调参的难度，缺乏自适应的 $\tau$ 选择机制。

**3. 离散/组合优化任务的范畴限制**

论文明确排除了纯离散或组合优化任务。扩散模型直接应用于此类领域需要结构化的去噪与解码方案（如图结构、序列生成），当前 PCD 框架无法直接覆盖。这是方法适用范畴的重要边界。

**4. 数据规模依赖**

条件扩散模型训练仍需要大量静态数据（如合成任务使用 60,000 样本）。在极低数据场景下的表现尚未探索，而实际工程优化问题往往面临数据稀缺的约束。

**5. 计算开销与采样效率**

虽然 PCD 的采样速度优于 ParetoFlow（Table 4），但重加权步骤需要额外的一次性计算开销。在需要频繁更新数据集的场景中，这一开销可能成为瓶颈。

### 开放问题与未来方向

1. **离散/组合优化的扩展**：如何将条件扩散框架扩展到需要处理离散变量或序列结构的组合优化任务中（如 MONAS 中的网络架构搜索），同时保持生成质量？可能需要引入专用的图神经网络去噪器或自回归解码方案。

2. **高维空间的生成能力增强**：在高维搜索空间中，如何进一步增强条件扩散模型的数据分布拟合能力，以产生超越离线数据集的真正创新型解？可能的路径包括引入潜在空间扩散、层次化条件机制或混合专家模型。

3. **数据效率与主动学习**：能否结合主动学习或离线到在线的微移策略，在仅有极少量允许查询目标函数的情况下进一步提升帕累托前沿的质量？PCD 的条件生成能力天然适合作为主动学习中的候选解生成器。

4. **自适应重加权**：重加权方案中超参数（$\tau$、$K$）的自适应选择策略可以如何设计，以在不同任务上自动取得最优权衡？基于支配数分布特征的启发式规则可能是一个起点。

5. **超多目标场景的可扩展性**：条件扩散模型在更多目标（$m > 6$）的超多目标场景下的可扩展性及计算效率如何？初步实验（Table 8）显示 PCD 在 3-6 个目标上保持一致的性能提升，但更极端的目标数量可能对条件空间的维度和方向向量的覆盖均匀性提出新挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Pareto_Conditioned_Diffusion_Models_for_Offline_Multi_Objective_Optimization.pdf]]
