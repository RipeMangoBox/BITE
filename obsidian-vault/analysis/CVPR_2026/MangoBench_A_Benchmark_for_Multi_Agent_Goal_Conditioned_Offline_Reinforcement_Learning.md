---
title: "MangoBench: A Benchmark for Multi-Agent Goal-Conditioned Offline Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MangoBench_A_Benchmark_for_Multi_Agent_Goal_Conditioned_Offline_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- GCOMFGIIHCGG
- MangoBench
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 引入目标重标记（goal relabeling）与目标条件训练框架，通过结构化目标分解实现完全去中心化和CTDE训练，消除对手工奖励的依赖，并提升多目标泛化能力。
primary_logic: 将单智能体离线目标条件强化学习（OGCRL）扩展至多智能体场景，在机器人关节控制和双臂操作等任务中通过局部与全局目标的分解，使智能体在稀疏二值奖励下仍能学习协同策略并泛化到多个目标；多目标评估相比单目标评估能更准确、稳定地衡量算法性能。
claims:
- 多目标评估成功率始终优于单目标评估，例如在lift-barrier任务中，IHIQL多目标成功率达82%，而单目标仅78%；GCMBC从22%提升至47%。
- 在AntMaze-navigate giant (2x4)任务中，IHIQL平均成功率57.3%远高于HIQL-CTDE的1.4%，表明完全去中心化训练在当前层次化设置下优于CTDE。
- GCOMIGA和GCOMAR在几乎所有运动控制任务中失败，证实现有离线MARL方法无法有效处理稀疏奖励。
- 在antmaze-medium-explore 2x4d任务中，仅用单目标评估会导致错误结论：IHIQL在某一特定目标上达到完美成功率1.0，但五目标平均仅49.6。
---

# MangoBench: A Benchmark for Multi-Agent Goal-Conditioned Offline Reinforcement Learning

> [!tip] 核心洞察
> 将单智能体离线目标条件强化学习（OGCRL）扩展至多智能体场景，在机器人关节控制和双臂操作等任务中通过局部与全局目标的分解，使智能体在稀疏二值奖励下仍能学习协同策略并泛化到多个目标；多目标评估相比单目标评估能更准确、稳定地衡量算法性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MangoBench：面向多智能体目标条件的离线强化学习基准 |
| 英文题名 | MangoBench: A Benchmark for Multi-Agent Goal-Conditioned Offline Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_MangoBench_A_Benchmark_for_Multi-Agent_Goal-Conditioned_Offline_Reinforcement_Learning_CVPR_2026_paper.html) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Goal-Conditioned Offline MARL Framework (GCMBC, ICRL, IHIQL, HIQL-CTDE, GCOMIGA, GCOMAR) |
| Dataset | AntMaze-navigate giant, lift-barrier, place-food, antmaze-teleport-explore |

> [!tip] 效果简介
> - AntMaze-navigate giant (2x4) 上，Average Success Rate (%) IHIQL (57.3 ± 2.1) vs HIQL-CTDE (1.4 ± 0.8) (+55.9%)。
> - lift-barrier 上，Success Rate (%) IHIQL (multi-goal) 82% vs GCMBC (multi-goal) 47% (+35%)。
> - place-food 上，Success Rate (%) ICRL (超出 DP 75%) vs Diffusion Policy (DP) (+75%（相对）)。

## 概要

离线多智能体强化学习（Offline MARL）面临一个关键瓶颈：现有方法高度依赖手工设计的稠密任务奖励，难以泛化至新目标，而主流基准缺乏对多目标评估和目标条件训练的系统支持。MangoBench 作为首个面向多智能体目标条件的离线强化学习基准，通过引入**目标重标记（goal relabeling）**与**结构化目标分解**，将单智能体离线目标条件强化学习（OGCRL）扩展至完全去中心化和 CTDE（集中训练分散执行）两种多智能体范式，使算法在稀疏二值奖励下仍能学习协同策略并泛化到多个目标。

核心发现包括：（1）多目标评估相比单目标评估能更准确、稳定地衡量算法性能——在 lift-barrier 任务中，IHIQL 多目标成功率达 82%，而单目标仅 78%；GCMBC 从 22% 提升至 47%（Table 3）。（2）现有离线 MARL 方法 GCOMIGA 和 GCOMAR 在稀疏奖励下几乎完全失败，证实了稀疏奖励是多智能体离线学习的核心挑战（Section 5.1, Figure 2）。（3）在 AntMaze-navigate giant (2x4) 任务中，完全去中心化的 IHIQL 平均成功率达 57.3%，远超其 CTDE 版本 HIQL-CTDE 的 1.4%，表明当前层次化架构下集中训练可能引入显著不稳定（Table 4）。

该方法谱系将目标条件行为克隆（GCBC）、对比强化学习（CRL）和层次化隐式 Q 学习（HIQL）等单智能体基线扩展至多智能体场景，并与离线 MARL 方法 OMIGA、OMAR 的目标条件变体进行了系统对比。MangoBench 覆盖关节控制运动和多实体操作两大类任务，提供标准化 RL 数据集和多目标评估协议，为离线多智能体目标条件学习建立了首个系统性基准。

### 离线多智能体强化学习的核心瓶颈

离线强化学习（Offline RL）使智能体能够从静态数据集中学习策略而无需与环境交互，在机器人操控、自动驾驶等高风险领域展现出巨大潜力。然而，当场景扩展至多智能体系统时，离线MARL面临两个根本性挑战：**对奖励函数的高度敏感性**和**跨目标的泛化困难**。

现有离线MARL方法（如**OMIGA**（Wang et al., NeurIPS 2023）和**OMAR**（Pan et al., ICML 2022））严重依赖人工设计的稠密任务特定奖励函数。在稀疏二值奖励（达到目标为0，否则为-1）下，这些方法几乎完全失效——MangoBench的实验表明，GCOMIGA和GCOMAR在几乎所有运动控制任务中均无法学习有效策略（Fig.2, Section 5.1）。这一发现揭示了当前离线MARL范式的结构性缺陷：当奖励信号变得稀疏时，现有算法缺乏从有限数据中提取有效学习信号的能力。

### 目标条件范式的缺失

单智能体领域已发展出成熟的目标条件离线强化学习（OGCRL）框架，通过目标重标记（goal relabeling）和目标条件训练，使策略能够在稀疏奖励下学习并泛化至多个目标。代表性方法包括**GCBC**（Ghosh et al., ICLR 2021; Lynch et al., CoRL 2020）、**CRL**（Eysenbach et al., NeurIPS 2022）和**HIQL**（Park et al., NeurIPS 2023）。

然而，多智能体场景中始终缺乏系统性的目标条件离线学习框架。这一缺失导致三个关键问题：

1. **奖励工程负担**：每个新任务都需要手工设计稠密奖励，严重限制了实际部署的可扩展性。
2. **目标泛化受限**：现有基准仅支持单目标评估，无法衡量策略在多目标场景下的真实泛化能力。
3. **评估偏差风险**：单目标评估可能产生误导性结论——在antmaze-medium-explore 2x4d任务中，IHIQL在某一特定目标上达到完美成功率1.0，但五目标平均成功率仅为49.6（Fig.3），说明单一目标的评估无法反映算法的真实性能。

### 多智能体目标条件的独特挑战

将OGCRL从单智能体扩展至多智能体并非简单的维度扩展。核心难题在于**目标表示的结构化分解**：在多智能体系统中，全局目标需要被合理地分解为每个智能体的局部目标。

考虑两类典型任务：
- **联合控制任务**（如AntMaze-navigate）：多个智能体共同控制同一机器人，全局目标为机器人末端位置，每个智能体控制部分关节。此时需要将全局目标映射为各关节的协调运动。
- **多实体操作任务**（如lift-barrier、place-food）：每个智能体控制独立机械臂，需协作完成操作。此时需将全局任务目标分解为每个机械臂的局部目标。

这一分解过程决定了智能体能否在仅依赖局部观测的条件下学习协同策略，是目标条件离线MARL区别于单智能体OGCRL的本质特征。

### 本文动机

综上所述，本文的核心动机可归纳为三个层面：

1. **方法层面**：建立首个系统性的目标条件离线MARL框架，将OGCRL扩展至完全去中心化和CTDE两种范式，通过结构化目标分解消除对手工奖励的依赖，并提升多目标泛化能力。
2. **基准层面**：构建MangoBench——首个纯合作多目标离线MARL基准，覆盖联合控制运动和多实体操作两类任务，提供标准化RL数据集和多目标评估协议。
3. **评估层面**：揭示单目标评估的潜在偏差，建立多目标评估作为衡量目标条件离线MARL算法性能的更准确、更稳定标准。

## 核心方法与创新机理

### 瓶颈与突破：从单智能体目标条件到多智能体离线强化学习

离线多智能体强化学习（Offline MARL）长期受困于两个根本性瓶颈：**对人工设计稠密奖励的高度敏感**和**跨目标泛化能力的缺失**。现有离线MARL基准（如OMIGA、OMAR）仅支持单目标评估，且依赖任务特定的shaped reward，这导致算法在实际部署中一旦面对稀疏奖励或新目标便迅速失效。MangoBench的核心突破在于将单智能体离线目标条件强化学习（OGCRL）范式系统性地扩展至多智能体场景，通过**目标条件训练**彻底消除对手工奖励的依赖，并借助**多目标评估协议**首次可靠地衡量多智能体策略的泛化能力。

### 关键创新：四个Changed Slots

MangoBench的创新可归纳为四个核心维度的改变，每个维度都直接回应了现有方法的根本缺陷：

**1. 目标表示：从全局目标到结构化分解**

传统多智能体系统仅使用单一全局目标，无法适应智能体间的分工协作。MangoBench引入**结构化目标分解**：对于多实体操作任务（如lift-barrier、place-food），全局目标被分解为每个智能体的局部目标，使各智能体仅依赖局部信息进行决策；对于关节控制运动任务，则通过聚合形成联合目标，支持集中价值学习。这一设计直接支撑了完全去中心化和CTDE两种训练范式（见Equation (5)和(6)）。

**2. 奖励函数：从稠密人工奖励到稀疏二值目标条件奖励**

现有离线MARL方法（如OMIGA、OMAR）在稀疏奖励下几乎完全失效——实验表明OMIGA在稀疏奖励下无法学习，而在shaped奖励下性能大幅提升（见Figure 5）。MangoBench统一采用**稀疏二值目标条件奖励**：智能体达到目标获得0奖励，否则获得-1（见Equation (1)）。这一设计消除了任务特定奖励工程的需求，迫使算法从数据中学习有意义的目标导向行为，而非拟合人工奖励信号。

**3. 训练范式：从单智能体离线RL到多智能体目标条件训练**

MangoBench首次在离线多智能体场景下实现了两种目标条件训练范式：
- **完全去中心化训练**：每个智能体利用局部观测、动作和目标独立更新策略（Equation (5)），无需智能体间通信。
- **CTDE训练**：训练时使用全局信息计算Q值，执行时仅依赖局部观测和目标（Equation (6)），保留协调潜力。

实验揭示了反直觉的发现：在层次化架构下，完全去中心化的**IHIQL**（57.3%成功率）显著优于其CTDE版本**HIQL-CTDE**（仅1.4%），表明集中训练在当前设置下可能引入额外训练不稳定性（见Table 4）。

**4. 评估协议：从单目标到多目标评估**

MangoBench的关键方法论贡献在于揭示了**单目标评估的严重误导性**。在antmaze-medium-explore 2x4d任务中，IHIQL在某一特定目标上达到完美成功率1.0，但五目标平均仅49.6%（见Figure 3）。多目标评估在lift-barrier任务上全面提升了所有基线的表现：**GCMBC**从22%提升至47%，**IHIQL**从78%提升至82%（见Table 3）。这一发现确立了多目标评估作为目标条件离线MARL的必要标准。

### 方法谱系与知识库定位

MangoBench并非提出全新算法，而是通过**目标重标记（goal relabeling）**将现有离线MARL方法改造为目标条件版本，构建了首个系统性的多智能体目标条件离线RL框架：

- **GCMBC**：目标条件行为克隆，代表数据集中行为策略的性能下界（源自**GCBC**，Ghosh et al., ICLR 2021）。
- **ICRL**：目标条件对比强化学习，评估对比学习在稀疏奖励下的效果（源自**CRL**，Eysenbach et al., NeurIPS 2022）。
- **IHIQL**：层次化隐式Q学习，当前最先进的离线目标条件RL方法（源自**HIQL**，Park et al., NeurIPS 2023）。
- **GCOMIGA**和**GCOMAR**：分别源自**OMIGA**（Wang et al., NeurIPS 2023）和**OMAR**（Pan et al., ICML 2022），用于检验现有离线MARL方法在稀疏奖励下的鲁棒性。

实验表明，**GCOMIGA**和**GCOMAR**在几乎所有运动控制任务中失败，证实现有离线MARL方法无法有效处理稀疏奖励；而**IHIQL**凭借其层次化策略缓解稀疏奖励噪声，成为当前多智能体离线目标条件任务的SOTA算法。

### 需要人工验证的要点

以下断言基于论文提供的证据，但需读者自行核实细节：
- GCMBC在lift-barrier多目标评估中成功率从22%提升至47%的具体数值，需对照Table 3确认。
- ICRL在place-food任务上超出Diffusion Policy 75%的相对提升比例，原文仅给出相对描述，精确数值需对照Figure 2验证。
- HIQL-CTDE性能远逊于IHIQL的结论（Table 4）仅在AntMaze-navigate任务上验证，是否适用于其他任务类型尚需进一步实验。

MangoBench 构建了首个面向多智能体目标条件的离线强化学习（goal-conditioned offline MARL）框架，其核心 pipeline 由四个关键模块串联而成：**目标重标记与数据集转换** → **目标分解** → **去中心化/CTDE 训练** → **多目标评估**。

### 模块关系与数据流

**1. 目标重标记与数据集转换（Goal-Relabeling & Dataset Conversion）**

原始 rollout 数据本身并不天然携带目标条件结构。该模块对每条轨迹进行目标重标记——从轨迹中随机采样状态作为“事后目标”（hindsight goal），并据此重新计算每个时间步的二值奖励：智能体达到目标状态时获得 $0$ 奖励，否则获得 $-1$（见 Equation (1)）。经过重标记的数据被转化为标准 RL 数据集 $\mathcal{D}$，其中每个样本包含局部观测 $o_i^t$、动作 $a_i^t$、下一观测 $o_i^{t+1}$ 以及对应的局部目标 $g_i$。这一转换消除了对手工设计稠密奖励的依赖，使框架天然适配稀疏二值奖励场景（Section 3.1, Figure 1）。

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/001_Figure_1.jpg]]
*Figure 1: Overview of MangoBench. Through goal relabeling and structured robot factorization into local and global goals, we design goal-conditioned offline MARL baselines under both decentralized and CTDE paradigms, and introduce environments supporting jointcontrol locomotion and multi-entity manipulation with goal-related rewards, standardized RL datasets, and multi-goal evaluation*

**2. 目标分解（Goal Factorization）**

MangoBench 覆盖两类多智能体任务结构：**多实体操纵任务**（multi-entity manipulation）和**联合控制运动任务**（joint-control locomotion）。目标分解模块根据任务类型将全局目标 $\mathbf{g}$ 结构化为各智能体的局部目标 $g_i$：
- 对于多实体任务，每个智能体拥有独立的局部目标，奖励由局部观测与局部目标的匹配决定（Equation (1)）；
- 对于联合控制任务，全局目标被聚合为联合目标 $\mathbf{g}$，所有智能体共享同一个全局目标条件奖励（Equation (2)）。

这种结构化分解使得框架能够同时支持完全去中心化训练和 CTDE（集中训练分散执行）两种范式（Section 3.2）。

**3. 去中心化/CTDE 训练**

在完全去中心化设置下，每个智能体 $i$ 独立优化其目标条件策略 $\pi_i(a_i \mid o_i, g_i)$，仅依赖局部信息：

$$
\nabla_{\theta_i} J_i = \mathbb{E}_{(o_i, a_i, g_i) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(o_i, a_i, g_i) \right]
$$

在 CTDE 设置下，训练时使用全局观测 $\mathbf{o}$、全局动作 $\mathbf{a}$ 和全局目标 $\mathbf{g}$ 来学习集中式价值函数 $Q_i(\mathbf{o}, \mathbf{a}, \mathbf{g})$，而执行时策略仍仅依赖局部信息：

$$
\nabla_{\theta_i} J_i = \mathbb{E}_{(\mathbf{o}, \mathbf{a}, \mathbf{g}) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(\mathbf{o}, \mathbf{a}, \mathbf{g}) \right]
$$

两种范式的优化目标均为最大化期望折扣目标条件回报（Equation (4)），但信息利用方式不同，这直接影响了后续实验中两者的性能差异（Section 3.2–3.3）。

**4. 多目标评估（Multi-Goal Evaluation）**

传统离线 MARL 评估通常仅测试单一目标，MangoBench 引入多目标评估协议：在运动控制任务上使用 5 个预定义目标，在操纵任务上使用 5 个序列化多目标（Section 4.1–4.2）。这一模块是框架的关键创新——实验表明，单目标评估可能产生严重误导：在 antmaze-medium-explore 2×4d 任务中，IHIQL 在某一特定目标上成功率达 1.0，但五目标平均仅 49.6（Figure 3）；而在 lift-barrier 任务上，多目标评估使 GCMBC 成功率从 22% 提升至 47%（Table 3）。

### 框架的因果瓶颈与设计动机

整个 pipeline 的设计围绕一个核心瓶颈展开：**离线多智能体强化学习对奖励函数高度敏感且难以泛化至新目标**。现有离线 MARL 方法（如 **OMIGA**（Wang et al., NeurIPS 2023）和 **OMAR**（Pan et al., ICML 2022））依赖手工设计的稠密奖励，在稀疏奖励下几乎完全失效（Figure 5）。MangoBench 通过目标重标记消除对手工奖励的依赖，通过目标分解实现多智能体协同下的目标条件学习，再通过多目标评估揭示算法的真实泛化能力，从而为离线 MARL 提供了一个更严格、更全面的测试平台。

MangoBench框架的核心在于将单智能体离线目标条件强化学习（OGCRL）扩展至多智能体场景，通过**目标重标记**、**目标分解**和**去中心化/CTDE训练**三个关键模块，使智能体在稀疏二值奖励下仍能学习协同策略并泛化至多个目标。

### 3.1 目标条件奖励函数

框架摒弃了传统多智能体强化学习中依赖人工设计的稠密奖励，转而采用稀疏的二值目标条件奖励。根据任务类型，奖励函数分为两类：

**多实体任务（Multi-entity tasks）** 中，每个智能体根据其局部观测 $o_i$ 和局部目标 $g_i$ 计算奖励：

$$r(o_i, g_i) = \begin{cases} r_1, & o_i \in \mathrm{GoalStates}(g_i) \\ r_2, & \text{otherwise} \end{cases}$$

其中 $r_1$ 通常设为 0（到达目标），$r_2$ 设为 -1（未到达目标），$\mathrm{GoalStates}(g_i)$ 表示目标 $g_i$ 对应的状态集合。

**联合控制任务（Joint-control tasks）** 中，奖励基于全局观测 $\mathbf{o}$ 和全局目标 $\mathbf{g}$：

$$r(\mathbf{o}, \mathbf{g}) = \begin{cases} r_1, & \mathbf{o} \in \mathrm{GoalStates}(\mathbf{g}) \\ r_2, & \text{otherwise} \end{cases}$$

这种统一的稀疏奖励设计消除了对手工奖励工程的依赖，使框架能够适配多种任务形态。

### 3.2 目标重标记与数据集转换

目标重标记（Goal Relabeling）是框架的第一个核心模块（Figure 1）。原始rollout数据被转化为标准离线RL数据集：对于数据集中的每条轨迹，从预定义的目标集合中随机采样目标，并根据上述奖励函数重新计算奖励信号。这一过程使离线数据能够支持目标条件训练，是后续所有基线方法的基础。

### 3.3 目标分解

在多智能体场景中，全局目标需要被合理分解为各智能体的局部目标（Figure 1）。对于多实体任务（如双臂操作），每个机械臂拥有独立的局部目标，形成**结构化目标分解**（structured goal factorization）；对于联合控制任务（如多足机器人运动），多个智能体共享全局目标。这一模块决定了后续训练范式中目标表示的形式。

### 3.4 去中心化与CTDE训练范式

框架支持两种训练范式，其核心区别在于价值函数使用的信息范围。

**完全去中心化训练（Fully Decentralized）**：每个智能体 $i$ 仅利用局部观测 $o_i$、动作 $a_i$ 和局部目标 $g_i$ 独立优化策略，目标为最大化期望折扣目标条件回报：

$$\max_{\pi_i} \mathbb{E}_{(o_i^t, a_i^t, o_i^{t+1}, g_i) \sim \mathcal{D}} \left[ \sum_{t=0}^{\infty} \gamma^t r(o_i^t, g_i) \right]$$

对应的策略梯度为：

$$\nabla_{\theta_i} J_i = \mathbb{E}_{(o_i, a_i, g_i) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(o_i, a_i, g_i) \right]$$

其中 $Q_i$ 为局部目标条件价值函数，$\pi_i$ 为智能体 $i$ 的策略。

**集中训练分散执行（CTDE）**：训练时价值函数 $Q_i$ 使用全局信息 $(\mathbf{o}, \mathbf{a}, \mathbf{g})$，但策略在执行时仍仅依赖局部观测和局部目标：

$$\nabla_{\theta_i} J_i = \mathbb{E}_{(\mathbf{o}, \mathbf{a}, \mathbf{g}) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(\mathbf{o}, \mathbf{a}, \mathbf{g}) \right]$$

两种范式的对比实验（Table 4）揭示了一个重要发现：在当前层次化架构下，完全去中心化的 IHIQL 在 AntMaze-navigate giant (2x4) 任务上平均成功率达 57.3%，而对应的 CTDE 版本 HIQL-CTDE 仅为 1.4%，表明集中训练可能引入额外的训练不稳定性。

### 3.5 基线方法构建

基于上述模块，框架构建了六种目标条件离线MARL基线：
- **GCMBC**：目标条件行为克隆，代表数据集中行为策略的性能下界
- **ICRL**：基于对比学习的离线RL方法
- **IHIQL**：层次化隐式Q学习，当前最先进的离线目标条件RL方法
- **HIQL-CTDE**：IHIQL的CTDE变体
- **GCOMIGA / GCOMAR**：分别由 OMIGA（Wang et al., NeurIPS 2023）和 OMAR（Pan et al., ICML 2022）通过目标重标记改造而来的目标条件版本

实验表明，GCOMIGA 和 GCOMAR 在几乎所有运动控制任务中完全失败（Figure 2），证实现有离线MARL方法无法有效处理稀疏奖励，这一发现构成了后续研究的重要出发点。

## 实验与关键发现

### 核心瓶颈：稀疏奖励与离线学习的根本冲突

MangoBench 揭示的首要瓶颈是：现有离线多智能体强化学习（MARL）方法在稀疏二值奖励下几乎完全失效。GCOMIGA 和 GCOMAR 作为 OMIGA 和 OMAR 的目标条件变体，在几乎所有运动控制任务中均无法学习有效策略，因而被排除在更具挑战性的操作任务评估之外（Figure 2）。这一失败并非偶然——如 Figure 5 所示，OMIGA 在稀疏奖励下几乎无法学习，而引入 shaped 奖励后性能大幅提升，直接证明了现有离线 MARL 对稠密手工奖励的深度依赖。MangoBench 通过统一采用“达到目标为 0，否则为 -1”的稀疏二值奖励，将这一结构性缺陷暴露为可量化的瓶颈。

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/005_Figure_2.jpg]]
*Figure 2: Benchmark Results. For locomotion tasks, we report each method’s average success rate (%) across five test-time goals, averaged over 5 seeds with standard deviations shown as error bars. Due to the poor performance of GCOMIGA and GCOMAR, they are excluded from more challenging manipulation tasks. For manipulation tasks, we report the average success rate (%) over 100 seeds for three top-performing baselines and the imitation learning method DP [4], along with training time*

### 主结果：谁在稀疏奖励下有效？

在运动控制任务的基准测试中（Figure 2），IHIQL 作为层次化隐式 Q 学习的多智能体扩展，展现出最强的稀疏奖励鲁棒性。在所有 teleport 类迷宫任务中，多智能体 IHIQL 始终优于单智能体 HIQL，且在 antmaze-teleport-explore 和 antmaze-large-stitch 等任务上优势显著。相比之下，ICRL（对比强化学习）在较大迷宫中暴露出泛化与长时程推理的不足，尤其在 antmaze-large-stitch 上表现不佳。

在操作任务层面，IHIQL 在 lift-barrier 上取得最高成功率，超出模仿学习基线 Diffusion Policy（DP）41.4%，且训练时间仅为 DP 的 5%。ICRL 则在 place-food 任务上表现最佳，成功率达 DP 的 175%，训练速度提升 93%（Figure 2）。这一结果说明，目标条件离线 RL 在稀疏奖励下的操作任务中，不仅在成功率上超越行为克隆与扩散策略，在样本效率上也具有显著优势。

### 关键消融：去中心化 vs. CTDE 的意外反转

Table 4 报告了 AntMaze-navigate 任务上去中心化与 CTDE 架构的直接对比。完全去中心化的 IHIQL 在 giant (2x4) 任务上平均成功率达到 57.3%，而对应的 CTDE 版本 HIQL-CTDE 仅为 1.4%——差距高达 55.9 个百分点。这一反转表明，在当前层次化架构下，CTDE 的集中训练可能引入额外的不稳定性，反而损害策略学习。该发现对 CTDE 范式在目标条件离线 MARL 中的适用性提出了重要质疑。

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/006_Table_4.jpg]]
*Table 4: Fully decentralized v.s. centralized training decentralized execution. Results on AntMaze-navigate. We report each method’s average success rate (%) across the five test-time goals on each task. The results are averaged over 4 seeds, and we report standard deviations after ± sign*

### 多目标评估：单目标指标的欺骗性

Table 3 在 lift-barrier 任务上系统对比了单目标与多目标评估。多目标评估下，所有方法均获得一致提升：IHIQL 从 78% 升至 82%，GCMBC 从 22% 大幅跃升至 47%。更关键的是，Figure 3 揭示了单目标评估可能导致根本性误判：在 antmaze-medium-explore 2x4d 任务中，IHIQL 在某一特定目标上达到完美成功率 1.0，但五目标平均仅为 49.6。若仅依赖单目标评估，研究者可能错误地认为该算法已解决该任务，而忽略了其在其他目标上的严重退化。这一发现确立了多目标评估作为目标条件离线 MARL 的必要评估协议。

### 失败模式与方法局限

GCOMIGA 和 GCOMAR 的全面失败构成了 MangoBench 中最明确的失败信号。这两种方法在运动控制任务上的成功率几乎为零（Figure 2），表明简单地将现有离线 MARL 算法通过目标重标记转化为目标条件变体，并不足以应对稀疏奖励的挑战。更深层的原因在于，这些方法缺乏处理稀疏反馈信号的机制——当奖励仅在目标达成时才从 -1 变为 0 时，价值函数的学习信号极度稀疏，导致策略无法从离线数据中提取有效信息。

此外，HIQL-CTDE 在层次化设置下的显著退化（Table 4）提示了另一个结构性失败模式：集中价值函数在目标条件多智能体场景中可能面临联合目标空间的高维度和非平稳性，使得 Q 值估计的不确定性被放大，最终导致策略崩溃。

### 环境与奖励设计的基准贡献

Table 1 和 Table 2 从环境与奖励两个维度定位了 MangoBench 的独特贡献。相比现有 MARL 基准，MangoBench 首次在联合控制运动任务和多实体操作任务中引入目标相关奖励、标准化 RL 数据集和多目标评估协议。Table 2 特别强调了奖励函数的稀疏性——这是现有基准普遍缺失的关键属性，也是迫使算法摆脱手工奖励依赖的核心设计选择。

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/002_Table_1.jpg]]
*Table 1: Comparison of Multi-Agent Environments*

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/003_Table_2.jpg]]
*Table 2: Properties of Reward Function in Multi-Agent Environments*

![[assets/figures/papers/paper_list_l2286_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_MangoBench_A_Benc/figures/009_Figure_4.jpg]]
*Figure 4: Visualization of different reward settings. (a) Sparse reward R, (b) shaped reward*

## 定位与知识库关联

### 1. 从单智能体目标条件RL到多智能体扩展

MangoBench的核心贡献在于将单智能体离线目标条件强化学习（OGCRL）系统性地迁移至多智能体场景。这一迁移并非简单的环境替换，而是涉及**目标表示、奖励函数、训练范式和评估协议**四个关键槽位的重新设计。

在单智能体OGCRL中，策略以全局目标为条件进行学习，奖励通常为稀疏二值信号（达到目标为0，否则为-1）。MangoBench将这一范式扩展为两种多智能体训练模式：

- **完全去中心化训练**：将全局目标结构化分解为每个智能体的局部目标，每个智能体仅基于局部观测、动作和局部目标独立学习策略，策略梯度形式为：

$$\nabla_{\theta_i} J_i = \mathbb{E}_{(o_i, a_i, g_i) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(o_i, a_i, g_i) \right]$$

- **CTDE训练**：训练时使用全局观测、联合动作和全局目标，执行时仅依赖局部信息，策略梯度为：

$$\nabla_{\theta_i} J_i = \mathbb{E}_{(\mathbf{o}, \mathbf{a}, \mathbf{g}) \sim \mathcal{D}} \left[ \nabla_{\theta_i} \log \pi_i(a_i \mid o_i, g_i) Q_i(\mathbf{o}, \mathbf{a}, \mathbf{g}) \right]$$

这一扩展直接回应了现有离线MARL方法（如**OMIGA** (Wang et al., NeurIPS 2023) 和 **OMAR** (Pan et al., ICML 2022)）对奖励函数高度敏感的瓶颈——实验表明，OMIGA在稀疏奖励下几乎无法学习，而在shaped奖励下性能大幅提升（Figure 5），证实了手工稠密奖励的脆弱性。

### 2. 与现有基线的谱系关系

MangoBench构建了六类目标条件基线，形成了从简单到复杂的清晰谱系：

| 基线方法 | 谱系定位 | 核心机制 | 关键参考 |
|---------|---------|---------|---------|
| **GCBC** (Goal-Conditioned Behavior Cloning) | 行为克隆下界 | 直接模仿数据集中目标条件行为 | Ghosh et al., ICLR 2021; Lynch et al., CoRL 2020 |
| **CRL** (Contrastive RL) | 对比学习探索 | 通过对比表示学习处理稀疏奖励 | Eysenbach et al., NeurIPS 2022 |
| **HIQL** (Hierarchical Implicit Q-Learning) | 单智能体SOTA | 层次化隐式Q学习，缓解稀疏奖励噪声 | Park et al., NeurIPS 2023 |
| **GCOMIGA / GCOMAR** | 现有离线MARL的目标条件变体 | 对OMIGA/OMAR进行目标重标记和随机目标采样 | 基于OMIGA (Wang et al., NeurIPS 2023) 和OMAR (Pan et al., ICML 2022) |
| **Diffusion Policy (DP)** | 模仿学习基线 | 扩散模型策略，用于操作任务对比 | Chi et al., 2025 |

实验揭示了一个关键的谱系断裂：**GCOMIGA和GCOMAR在几乎所有运动控制任务中失败**（Figure 2），表明直接将现有离线MARL方法改造为目标条件版本无法有效应对稀疏奖励。这一发现将离线MARL领域的瓶颈从“如何利用离线数据”推进到“如何在稀疏奖励下实现多目标泛化”。

### 3. 知识库中的定位与边界

MangoBench在以下维度上填补了知识空白：

**填补的空白**：
- 首个面向多智能体的目标条件离线RL基准，此前不存在支持多目标评估的离线MARL环境（Table 1对比了现有环境的目标条件支持情况）
- 首次系统对比完全去中心化与CTDE在目标条件离线MARL中的效果

**适用边界**：
- **任务类型**：仅覆盖纯合作任务，未涉及竞争或混合动机场景
- **目标空间**：评估局限于预定义目标集（运动控制5个目标，操作任务5个序列目标），未测试开放世界目标生成的泛化能力
- **奖励类型**：仅使用稀疏二值目标条件奖励，未探索其他稀疏奖励形式（如基于距离的稀疏奖励）
- **算法范围**：基线方法均为对现有单智能体方法的扩展，未设计专门针对多智能体稀疏奖励问题的新算法

### 4. 局限与开放问题

**已证实的局限**：

1. **CTDE的不稳定性**：在AntMaze-navigate任务上，完全去中心化的IHIQL平均成功率57.3%，而对应的CTDE版本HIQL-CTDE仅1.4%（Table 4）。这表明在当前层次化架构下，集中训练引入的额外信息并未带来协调优势，反而导致训练不稳定。

2. **现有离线MARL方法的稀疏奖励失败**：OMIGA在稀疏奖励下几乎无法学习，GCOMIGA和GCOMAR同样表现极差，说明离线MARL领域缺乏专门针对稀疏奖励的设计。

3. **方法无绝对主导**：如论文所述，“no method dominates all tasks”——IHIQL在lift-barrier上最优，ICRL在place-food上最优，GCMBC在某些简单任务上可接受，表明不同任务特性需要不同的算法设计。

**开放问题**：

- **高效CTDE架构设计**：如何设计更稳定的HIQL-CTDE架构，使其既能利用全局信息进行协调，又避免当前架构中的训练不稳定性？这可能需要重新思考层次化结构中的信息共享机制。

- **稀疏奖励专用算法**：当前所有基线均是对单智能体方法的直接扩展，缺乏专门针对多智能体稀疏奖励问题的算法创新。例如，是否可以利用智能体间的目标依赖关系设计更有效的探索或信用分配机制？

- **竞争/混合场景扩展**：目标条件范式天然适用于合作任务（目标可分解），但在竞争场景中，智能体的目标可能相互冲突。如何定义和分解竞争性目标条件是一个未探索的方向。

- **开放世界目标泛化**：当前评估仅使用预定义目标，实际应用中可能需要泛化到训练时未见过的目标组合。这要求方法具备目标空间的组合泛化能力，而非简单的插值泛化。

**需手动验证的点**：论文未提供HIQL-CTDE性能崩溃的深层原因分析（如梯度冲突、价值函数估计偏差等），建议读者结合Table 4的具体数值和训练曲线进一步判断CTDE失败的根本机制。

## 原文 PDF

![[paperPDFs/CVPR_2026/MangoBench_A_Benchmark_for_Multi_Agent_Goal_Conditioned_Offline_Reinforcement_Learning.pdf]]
