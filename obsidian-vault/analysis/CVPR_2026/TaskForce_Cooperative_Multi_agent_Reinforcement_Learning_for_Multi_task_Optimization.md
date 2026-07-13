---
title: "TaskForce: Cooperative Multi-agent Reinforcement Learning for Multi-task Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TaskForce_Cooperative_Multi_agent_Reinforcement_Learning_for_Multi_task_Optimization.pdf
project_link: null
code_link: null
aliases:
- TaskForce
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将多任务优化重构为合作马尔可夫博弈，引入多智能体强化学习，让每个任务的自适应策略智能体学习如何协同聚合梯度。
primary_logic: 通过紧凑的Gram矩阵观测捕获梯度幅值与对齐信息，并设计混合奖励（损失改进对数 + 聚合梯度L2范数最小化），使MARL智能体既解决梯度冲突又维持收敛性，从而突破确定性方法的局部最优困境。
claims:
- TaskForce在三个异构基准（NYU-v2, Cityscapes, QM9）上一致超越现有MTO基线。
- 混合奖励函数使智能体有效解决梯度冲突并避免不良收敛。
- 消融实验证实合作MARL各组件带来一致且显著的性能增益。
- NYU-v2 (3-task) 上 Δm↓ = -6.47%
---

# TaskForce: Cooperative Multi-agent Reinforcement Learning for Multi-task Optimization

> [!tip] 核心洞察
> 通过紧凑的Gram矩阵观测捕获梯度幅值与对齐信息，并设计混合奖励（损失改进对数 + 聚合梯度L2范数最小化），使MARL智能体既解决梯度冲突又维持收敛性，从而突破确定性方法的局部最优困境。

| 字段 | 内容 |
|------|------|
| 中文题名 | TaskForce：面向多任务优化的协作多智能体强化学习 |
| 英文题名 | TaskForce: Cooperative Multi-agent Reinforcement Learning for Multi-task Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Choi_TaskForce_Cooperative_Multi-agent_Reinforcement_Learning_for_Multi-task_Optimization_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | TaskForce |
| Dataset | NYU-v2, Cityscapes |

> [!tip] 效果简介
> - NYU-v2 (3-task) 上，Δm↓ -6.47% vs 单任务基线 (0.0%) (-6.47%)；△t↓ -9.96% vs 单任务基线 (0.0%) (-9.96%)。
> - Cityscapes (3-task) 上，Δm↓ -0.65% vs 单任务基线 (0.0%) (-0.65%)。

## 概要

多任务优化（Multi-Task Optimization, MTO）的核心挑战在于：不同任务的梯度往往存在冲突，导致联合训练时出现负迁移，使整体性能甚至不如单任务独立训练。现有方法主要分为两类——基于损失的重加权策略（如**Uncertainty**（Kendall et al., CVPR 2018）、**DWA**（Liu et al., CVPR 2019））和基于梯度的聚合策略（如**MGDA**（Sener & Koltun, NeurIPS 2018）、**PCGrad**（Yu et al., NeurIPS 2020）、**CAGrad**（Liu et al., NeurIPS 2021））。然而，前者缺乏随机性，容易陷入局部最优；后者虽直接操作梯度，但大多依赖确定性启发式，未能显式建模任务间的动态博弈关系，导致梯度冲突难以根除。

TaskForce 的核心洞察在于：将多任务优化重构为一个**合作马尔可夫博弈**（cooperative Markov game），引入多智能体强化学习（MARL）来学习梯度聚合策略。每个任务对应一个自适应策略智能体，通过观测紧凑的梯度 Gram 矩阵（捕获梯度幅值与对齐信息）和任务损失值，输出连续平衡权重，以凸组合方式聚合任务梯度。混合奖励函数——对数损失改进与聚合梯度 L2 范数最小化的加权组合——引导智能体在解决梯度冲突的同时维持收敛性，从而突破确定性方法的局部最优困境。

实验表明，TaskForce 在三个异构基准（NYU-v2 三任务密集预测、Cityscapes 三任务语义场景理解、QM9 十一任务分子性质预测）上一致超越现有 MTO 基线。消融研究进一步证实，合作 MARL 的各个组件（Gram 观测、多智能体架构、集中式评论家、去中心化执行、共享奖励）均带来显著且一致的性能增益。

多任务学习（Multi-Task Learning, MTL）的核心目标是通过跨任务共享表征来提升泛化能力与数据效率。然而，其优化过程本质上是一个多目标优化（Multi-Task Optimization, MTO）问题——需要同时最小化多个可能相互冲突的任务损失函数。这引出了一个根本性的瓶颈：**现有MTO方法要么依赖确定性启发式策略而缺乏随机性探索，易陷入局部最优；要么未显式建模和解决梯度冲突，导致负迁移（negative transfer）难以根除。**

具体而言，现有MTO方法可分为两大范式。**基于梯度的方法**（如**MGDA** (Sener & Koltun, NeurIPS 2018)、**PCGrad** (Yu et al., NeurIPS 2020)、**CAGrad** (Liu et al., NeurIPS 2021)）通过求解一个公共下降方向或对冲突梯度进行投影/修正来聚合任务梯度，但这些操作是确定性的，缺乏对权重空间的有效探索。**基于损失的方法**（如**Uncertainty** (Kendall et al., CVPR 2018)、**DWA** (Liu et al., CVPR 2019)）通过动态重加权任务损失来间接影响梯度，但同样依赖固定启发式规则，无法主动感知和化解梯度冲突。尽管**IGBv2** (Dai et al., UAI 2023) 率先将单智能体强化学习引入MTO，但其奖励信号仅基于损失改进，未能利用梯度层面的冲突信息，且单智能体架构难以捕捉任务间的协同关系。

上述缺口揭示了一个关键因果机制：**梯度冲突的解决需要一种能够感知梯度对齐状态、并在权重空间中执行随机探索的协同决策机制。** 确定性方法之所以受限，是因为它们将梯度聚合视为一个静态优化问题，而实际上MTO是一个动态过程——任务间的梯度关系随训练进程不断演化，单一公共下降方向往往无法兼顾各方利益。TaskForce的动机正是源于这一洞察：将多任务优化重构为一个合作马尔可夫博弈（cooperative Markov game），让每个任务拥有自己的自适应策略智能体，通过多智能体强化学习（MARL）来学习如何在每一步协同选择梯度聚合权重——既保持随机探索以跳出局部最优，又通过梯度层面的显式奖励信号来抑制冲突。

## 核心方法与创新机理

TaskForce 的核心创新在于将多任务优化（MTO）重新构建为一个合作马尔可夫博弈，并引入多智能体强化学习（MARL）来替代传统确定性梯度聚合策略。这一范式转换通过三个紧密耦合的 changed slots 实现，从根本上改变了梯度冲突的解决方式。

### 从确定性聚合到随机性策略探索

现有 MTO 方法的梯度聚合策略本质上都是确定性的：基于损失的方法（如 **Uncertainty**（Kendall et al., CVPR 2018）、**DWA**（Liu et al., CVPR 2019））通过固定规则或启发式权重重分配来聚合梯度；基于梯度的方法（如 **MGDA**（Sener & Koltun, NeurIPS 2018）、**PCGrad**（Yu et al., NeurIPS 2020）、**CAGrad**（Liu et al., NeurIPS 2021））则通过求解凸优化问题寻找单一公共下降方向。这些确定性策略缺乏随机性，容易陷入局部最优，且无法显式建模梯度冲突的动态演变。

TaskForce 将每个任务分配一个独立的策略智能体（演员网络），使其学习如何在连续空间中输出聚合权重。具体而言，每个智能体基于局部观测 $o_t$ 输出连续动作 $a_t = \mu_t(o_t; \phi_t)$，经 softmax 归一化后得到凸组合权重 $w_t$：

$$\mathbf{G} = \sum_{t=1}^{T} w_t g_t, \quad w_t = \frac{\exp(a_t)}{\sum_{k=1}^{T} \exp(a_k)}$$

这种随机性策略使系统能够在训练过程中探索不同的梯度组合方式，突破确定性方法的局部最优困境。同时，合作 MARL 框架通过集中式评论家共享全局信息，使各智能体学会协同决策，而非独立地最大化各自任务的改进。

### 紧凑观测：从完整梯度到 Gram 矩阵

传统基于梯度的方法需要存储和处理完整的任务梯度向量（维度为模型参数量 $|\theta|$），计算和存储开销极大。TaskForce 的关键创新在于设计了紧凑而富有表达力的观测表示：梯度 Gram 矩阵 $\mathbf{g}\mathbf{g}^\top \in \mathbb{R}^{T \times T}$ 拼接任务损失值 $\mathcal{L}(\theta)$。

$$\mathcal{O} = \{ \mathbf{g}\mathbf{g}^\top | \mathcal{L}(\theta) \}$$

Gram 矩阵的对角线元素捕获各任务梯度的幅值信息，非对角线元素编码任务梯度之间的成对对齐关系（余弦相似度）。这一设计将观测维度从 $|\theta|$ 压缩至 $T \times T + T$，在任务数 $T$ 远小于模型参数量时极为高效。同时，该表示保留了梯度冲突与协同的核心信息，使智能体能够基于紧凑的“训练动态摘要”做出决策。

### 混合奖励：兼顾即时改进与长期平衡

现有方法或仅依赖损失改进（如 **IGBv2**（Dai et al., UAI 2023）的单智能体 RL 设计），或仅关注梯度范数最小化（如 MGDA 的凸优化目标），缺乏将两者有机结合的机制。TaskForce 设计了混合奖励函数，同时注入损失反馈和梯度信号：

$$\mathcal{R} = \lambda_{\mathcal{L}} r_{\mathcal{L}} + \lambda_{\mathcal{G}} r_{\mathcal{G}}$$

其中，基于损失的奖励 $r_{\mathcal{L}}$ 衡量对数变换后任务损失的相对改进：

$$r_{\mathcal{L}} = \sum_{t=1}^{T} \log(1 + \mathcal{L}_t^{\mathrm{prev}}(\theta)) - \sum_{t=1}^{T} \log(1 + \mathcal{L}_t(\theta'))$$

基于梯度的奖励 $r_{\mathcal{G}}$ 惩罚聚合梯度的大范数，引导智能体寻找公共下降方向：

$$r_{\mathcal{G}} = -\| \sum_{t=1}^{T} w_t g_t \|_2^2$$

这两项奖励形成互补：$r_{\mathcal{L}}$ 提供即时优化进展的密集反馈，$r_{\mathcal{G}}$ 则从几何角度促进梯度对齐，避免因梯度冲突导致的训练震荡或发散。消融实验（Table 4）证实，混合奖励的各组件均带来一致且显著的性能增益，验证了这一设计的有效性。

### 创新的系统效应

上述三个 changed slots 并非孤立运作，而是形成正向协同：紧凑的 Gram 观测使智能体能够在低维空间中感知梯度冲突模式；随机性策略赋予系统逃离局部最优的能力；混合奖励则同时从损失下降和梯度对齐两个维度引导学习。这一组合突破了现有 MTO 方法“确定性启发式 + 单一信号源”的范式瓶颈，在 NYU-v2、Cityscapes 和 QM9 三个异构基准上均取得了一致且显著的性能提升。

TaskForce 将多任务优化（MTO）重构为一个**合作马尔可夫博弈**，其中多任务骨干网络本身充当交互式、动态演化的环境，每个任务被分配一个独立的策略智能体（演员），各智能体协同学习如何聚合任务梯度，以最有效地降低整体损失。整体 pipeline 如 Figure 1 所示，核心模块与数据流可概括为以下闭环：

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/001_Figure_1.jpg]]
*Figure 1: Overall pipeline of TaskForce. Each agent observes task-specific loss and a compact gradient summary via the Gram matrix, predicts a balancing weight for its task gradient, and is guided by a hybrid reward signal that reflects both gradient alignment and loss reduction. Centralized training, decentralized execution allows to learn coordinated policies while reducing computational efficiency by combining global training signals with local, task-specific decision-making*

1. **观测构建**：在每个优化步，计算各任务梯度 $\mathbf{g}_t$ 并构造紧凑的 **Gram 矩阵** $\mathbf{g}\mathbf{g}^\top \in \mathbb{R}^{T\times T}$，其对角线捕获梯度幅值，非对角线捕获任务间梯度对齐信息；同时收集当前经验损失集合 $\mathcal{L}(\theta)$。拼接后形成联合观测 $\mathcal{O} = \{\mathbf{g}\mathbf{g}^\top \mid \mathcal{L}(\theta)\}$（Eq. 5）。这一设计将高维梯度空间（维度 $|\theta|$）压缩为仅与任务数 $T$ 相关的低维表示，大幅降低智能体输入复杂度。

2. **去中心化执行**：每个任务 $t$ 拥有独立的演员网络 $\mu_t(o_t; \phi_t)$，从联合观测中提取任务特定观测 $o_t$，输出连续动作 $a_t$。所有动作经 **softmax 归一化** 得到凸组合权重 $w_t = \exp(a_t) / \sum_k \exp(a_k)$，确保权重非负且和为 1（Eq. 6）。最终聚合梯度为 $\mathbf{G} = \sum_{t=1}^T w_t \mathbf{g}_t$，用于更新骨干网络参数 $\theta \gets \theta - \eta \mathbf{G}$。

3. **混合奖励信号**：环境更新后，计算混合奖励 $\mathcal{R} = \lambda_{\mathcal{L}} r_{\mathcal{L}} + \lambda_{\mathcal{G}} r_{\mathcal{G}}$（Eq. 10），引导智能体在损失下降与梯度对齐之间取得平衡：
   - **损失奖励** $r_{\mathcal{L}}$（Eq. 7）：所有任务对数损失改进之和，鼓励快速降低任务损失。
   - **梯度奖励** $r_{\mathcal{G}}$（Eq. 9）：负聚合梯度 L2 范数平方 $-\|\mathbf{G}\|_2^2$，惩罚梯度冲突，推动聚合方向趋近 Pareto 最优的公共下降方向（Eq. 8 的凸最小化目标）。

4. **集中式训练**：采用标准 MADDPG 框架。每个任务配备一个集中式评论家 $Q_t^\mu(\mathcal{O}, A; \psi_t)$，利用全局联合观测 $\mathcal{O}$ 与所有智能体的联合动作 $A$ 最小化 TD 误差（Eq. 11）；演员则通过确定性策略梯度更新（Eq. 12）。目标网络通过指数移动平均缓慢更新以稳定训练（Eq. 13）。

该框架的关键因果机制在于：**随机性策略探索**突破了确定性聚合方法（如 MGDA、CAGrad 等）易陷入局部最优的瓶颈；**Gram 矩阵观测**以极低开销为智能体提供梯度冲突的结构化信息；**混合奖励**将短期损失改进与长期梯度对齐统一在同一强化学习目标下，从而系统性地缓解负迁移。

TaskForce将多任务优化建模为合作马尔可夫博弈，核心由七个模块串联构成一个完整的训练循环。以下按执行顺序展开关键模块及其支撑公式。

### 观测构建

每个智能体的观测由两部分拼接而成：任务梯度的Gram矩阵与当前所有任务的经验损失值。Gram矩阵维度仅为 $T \times T$（$T$ 为任务数），对角元编码各任务梯度的幅值，非对角元编码任务梯度间的成对对齐程度。这一紧凑表示避免了直接暴露完整梯度向量（维度 $|\theta|$）带来的维度灾难。

$$\mathcal{O} = \{ \mathbf{g}\mathbf{g}^\top \mid \mathcal{L}(\theta) \}$$

其中 $\mathbf{g} = [g_1, g_2, \ldots, g_T]$ 为各任务梯度，$\mathcal{L}(\theta) = \{\mathcal{L}_1(\theta), \ldots, \mathcal{L}_T(\theta)\}$ 为任务损失集合。各任务的经验损失定义为：

$$\mathcal{L}_t(\boldsymbol{\theta}) := \frac{1}{N} \sum_{i=1}^{N} \bar{\mathcal{L}}_t(\mathcal{F}(\mathbf{x}^i; \boldsymbol{\theta}), \mathbf{y}_t^i)$$

### 任务特定智能体与权重归一化

每个任务分配一个独立的演员网络 $\mu_t(\cdot; \phi_t)$，以局部观测 $o_t$（即Gram矩阵与损失向量的拼接）为输入，输出连续动作 $a_t \in \mathcal{A}$。随后通过softmax将所有智能体的动作归一化为凸组合权重 $w_t$：

$$\mathbf{G} = \sum_{t=1}^{T} w_t g_t, \quad w_t = \frac{\exp(a_t)}{\sum_{k=1}^{T} \exp(a_k)}, \quad a_t = \mu_t(o_t; \phi_t)$$

### 梯度聚合与环境更新

使用上述凸组合权重对任务梯度加权求和，得到聚合梯度 $\mathbf{G}$。随后执行一步标准的梯度下降更新多任务模型参数 $\theta$：

$$\theta \leftarrow \theta - \eta \mathbf{G}$$

更新后的模型在新参数 $\theta'$ 下重新计算各任务损失与梯度，构成下一时刻的观测 $\mathcal{O}'$。

### 混合奖励计算

奖励信号由基于损失的奖励 $r_{\mathcal{L}}$ 和基于梯度的奖励 $r_{\mathcal{G}}$ 加权组合而成，分别引导智能体关注即时损失下降与长期梯度对齐。

**基于损失的奖励** 衡量对数变换后各任务损失的相对改进：

$$r_{\mathcal{L}} = \sum_{t=1}^{T} \log(1 + \mathcal{L}_t^{\mathrm{prev}}(\theta)) - \sum_{t=1}^{T} \log(1 + \mathcal{L}_t(\theta'))$$

其中 $\mathcal{L}_t^{\mathrm{prev}}$ 为更新前的任务损失，$\mathcal{L}_t(\theta')$ 为更新后的损失。对数变换抑制了损失幅值差异过大的任务对奖励的主导。

**基于梯度的奖励** 惩罚聚合梯度L2范数的平方，鼓励智能体寻找使聚合梯度范数最小的公共下降方向。该设计源于以下凸最小化问题的最优值：

$$\underset{w_1,\cdots,w_T}{\operatorname{minimize}} \left\| \sum_{t=1}^{T} w_t g_t \right\|_2^2, \quad \mathrm{subject\ to} \sum_{t=1}^{T} w_t = 1, w_t \geq 0$$

基于此定义梯度奖励为负的聚合梯度L2范数平方：

$$r_{\mathcal{G}} = - \left\| \sum_{t=1}^{T} w_t g_t \right\|_2^2 = - \|\mathbf{G}\|_2^2$$

**混合奖励** 将两者加权组合：

$$\mathcal{R} = \lambda_{\mathcal{L}} r_{\mathcal{L}} + \lambda_{\mathcal{G}} r_{\mathcal{G}}$$

其中 $\lambda_{\mathcal{L}}$ 和 $\lambda_{\mathcal{G}}$ 为超参数，分别控制损失改进与梯度对齐的相对重要性。

### 集中式评论家训练

采用集中训练、分散执行的MADDPG框架。每个任务 $t$ 的评论家 $Q_t^{\mu}(\mathcal{O}, A; \psi_t)$ 以全局观测 $\mathcal{O}$（所有智能体共享的Gram矩阵与损失）和联合动作 $A = [a_1, \ldots, a_T]$ 为输入，通过最小化时序差分（TD）误差进行训练：

$$\mathcal{L}(\psi_t) = \mathbb{E}_{(\mathcal{O}, A, \mathcal{R}, \mathcal{O}') \sim \mathbf{D}} \big[ \big( Q_t^{\mu}(\mathcal{O}, A; \psi_t) - (\mathcal{R} + \gamma Q_t^{\mu'}(\mathcal{O}', A'; \psi_t')) \big)^2 \big]$$

其中 $\gamma$ 为折扣因子，$\mu'$ 和 $\psi_t'$ 为目标网络。

### 演员策略梯度更新

各演员网络通过确定性策略梯度进行更新，梯度方向由评论家对联合动作的偏导给出：

$$\nabla_{\phi_t} J(\phi_t) = \mathbb{E}_{(\mathcal{O}, A) \sim \mathbf{D}} \left[ \nabla_{\phi_t} \mu_t(o_t; \phi_t) \nabla_{a_t} Q_t^{\mu}(\mathcal{O}, A; \psi_t) \right]$$

该梯度引导演员朝着提升评论家估计的Q值方向更新策略。

### 目标网络软更新

目标网络通过指数移动平均缓慢跟踪在线网络参数，以稳定训练：

$$\phi_t' \leftarrow \tau \phi_t + (1 - \tau) \phi_t', \quad \psi_t' \leftarrow \tau \psi_t + (1 - \tau) \psi_t'$$

其中 $\tau \ll 1$ 为软更新系数。

### 关键设计决策的因果逻辑

上述模块协同解决现有MTO方法的两大瓶颈。**观测构建**用紧凑的Gram矩阵替代完整梯度，使智能体在低维空间中感知梯度冲突模式。**混合奖励**的双信号设计是核心因果旋钮：纯损失奖励（如IGBv2）可能使智能体贪婪追逐短期损失下降而忽视梯度冲突，导致负迁移累积；纯梯度奖励则可能使智能体过度追求梯度对齐而牺牲收敛速度。TaskForce通过 $\lambda_{\mathcal{L}}$ 和 $\lambda_{\mathcal{G}}$ 的平衡，使智能体在解决梯度冲突的同时维持有效的收敛轨迹。**多智能体合作博弈**框架赋予每个任务自适应策略，其随机性探索能力使系统能够跳出确定性启发式方法（如PCGrad、CAGrad求解单一公共下降方向）易陷入的局部最优。

## 实验与关键发现

### 主要结果：跨基准一致优势

TaskForce 在三个结构差异显著的基准上系统性地超越了现有 MTO 方法，验证了合作 MARL 范式对不同任务关系、数据规模与网络架构的泛化能力。

**NYU-v2 三任务场景**（语义分割、深度估计、法线预测，MTAN 骨干）。以单任务基线为参考零点，TaskForce 取得 Δm↓ = -6.47%，△t↓ = -9.96%，在所有比较方法中降幅最大（Table 1）。相比之下，基于梯度的强基线 **CAGrad**（Liu et al., NeurIPS 2021）和 **Aligned-MTL**（Senushkin et al., CVPR 2023）虽同样降低了相对性能损失，但幅度明显小于 TaskForce。这表明引入随机性策略探索与显式梯度冲突消解能有效突破确定性聚合的局部瓶颈。

**Cityscapes 三任务场景**（语义分割、深度估计、实例轮廓，PSPNet 骨干）。TaskForce 取得 Δm↓ = -0.65%，优于 Aligned-MTL 的 -0.02%（Table 2）。Δm 的改进幅度虽小于 NYU-v2，但在 Cityscapes 这类任务间冲突相对缓和的场景中仍体现出稳健的协同聚合能力。

**QM9 十一任务场景**（11 个分子属性回归，MPNN 骨干）。这是任务数量最多的测试场景，对梯度冲突消解和权重动态分配提出更高要求。TaskForce 在 Table 3 中继续保持最优，说明 Gram 矩阵观测的紧凑性在多任务扩展时仍能提供有效的梯度对齐信息，同时多智能体架构在任务数增加时未出现明显的策略退化。

### 消融实验：合作 MARL 各组件的因果贡献

Table 4 通过逐步添加合作 MARL 组件，在 NYU-v2 三任务设置上量化了每个设计选择的增益：

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/007_Table_4.jpg]]
*Table 4: Ablation studies on Cooperative MARL components on the NYU-v2 3-tasks setup. We report the training cost relative to the final configuration of each method on the MTAN [28] network architecture. We set*

- **基础配置**（单智能体 + 纯损失奖励 + 无 Gram 观测）性能最弱，验证了单一策略无法有效协调多任务梯度冲突。
- **引入 Gram 观测**后性能显著提升，证实梯度幅值与对齐信息的紧凑编码对智能体决策具有关键信息价值。
- **从单智能体扩展到多智能体**（每个任务独立策略）带来进一步增益，说明去中心化执行允许各任务自适应地表达不同的聚合偏好。
- **添加集中式评论家**（共享全局观测与动作信息）使智能体间的协同更有效，TD 学习提供的全局价值信号稳定了策略更新。
- **最终配置**（多智能体 + Gram 观测 + 集中评论家 + 混合奖励）取得最优结果，验证了各组件间存在正向交互——混合奖励在损失改进与梯度对齐之间提供平衡，集中评论家则缓解了多智能体训练的非平稳性。

### 效率分析：训练开销可控

Table 5 比较了各方法的每 epoch 训练时间。TaskForce 因额外维护 MARL 模块（演员、评论家、Gram 矩阵计算、回放缓冲区采样）而增加了训练开销，但相对于骨干网络的梯度计算，该开销保持在可接受范围内。Table 6 进一步分解了各组件的时间成本，Gram 矩阵构建与策略网络前向传播是主要额外开销来源，但其维度仅随任务数 T 呈二次方增长（T×T），在常见多任务规模下仍属轻量。

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/006_Table_5.jpg]]
*Table 5: Per-epoch training cost (epoch/sec) comparison between the proposed TaskForce and other baselines*

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/008_Table_6.jpg]]
*Table 6: Computational cost of TaskForce components on the NYUv2 dataset*

### 权重动态可视化：自适应任务平衡

Figure 2 展示了 QM9 十一任务场景下各任务权重随训练进程的动态演化（经窗口大小为 10 的滑动平均平滑）。权重曲线呈现以下特征：

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/005_Figure_2.jpg]]
*Figure 2: Task weight dynamics of 11-tasks QM9 datasets. For improved visualization, we smooth the weight dynamics by using a moving average with a window size of 10*

- **训练初期**权重波动较大，智能体处于探索阶段，尝试不同的聚合策略。
- **训练中后期**权重逐渐收敛至稳定分布，表明合作策略学会了根据任务间梯度对齐关系分配平衡权重。
- **不同任务的权重分化明显**，部分任务获得持续较高的聚合权重，反映出这些任务对整体 Pareto 收敛的贡献更大——这与混合奖励中梯度对齐信号的作用一致：智能体倾向于提升那些与其他任务梯度方向更一致的任务权重，从而降低聚合梯度的 L2 范数。

### 失败模式与局限

尽管 TaskForce 在三个基准上表现优异，但分析揭示了以下局限：

1. **训练开销与扩展性**：当任务数 T 激增时，Gram 矩阵维度（T×T）和智能体数量（T 个演员 + T 个评论家）线性或二次增长，可能导致扩展性瓶颈。Table 6 的成本分解在当前规模下可控，但更大规模场景需进一步优化（如参数共享或稀疏注意力）。
2. **超参数敏感性**：混合奖励的权重 λ_L 和 λ_G、软更新系数 τ 等超参数需针对不同任务集进行调整。当前实验采用固定配置（λ_L=1.0, λ_G=1×10⁻³），其在其他任务关系下的最优性需进一步验证。
3. **收敛速度**：MARL 训练的样本效率低于确定性方法，在训练初期可能需要更多迭代才能达到稳定策略。Figure 2 中的早期波动印证了这一点。
4. **任务关系动态变化**：当前设计假设任务关系在训练过程中相对稳定，未探索持续学习或任务逐步增加等真实世界动态场景的适用性。

### 待验证问题

- 该方法在语言与视觉等大规模异构任务联合训练中的表现与调参稳定性尚需独立验证。
- 引入历史梯度信息（如梯度动量或二阶统计量）作为观测扩展，能否进一步提升智能体的协同决策质量，值得探索。
- 强化学习训练的收敛速度与超参数鲁棒性需更系统的消融与敏感性分析。
- 在动态任务关系（如持续学习、任务增量）场景中的适用性尚未得到实验支持。

![[assets/figures/papers/paper_list_l2727_https_openaccess_thecvf_com_content_CVPR2026_html_Choi_TaskForce_Coopera/figures/002_Table_1.jpg]]
*Table 1: Evaluation results of NYU-v2 3-tasks setup. We report MTAN [28] model performance averaged over 3 random seeds*

## 定位与知识库关联

### 1. 方法定位：从确定性聚合到随机策略协同

TaskForce 的核心贡献在于将多任务优化（MTO）中的梯度聚合问题从**确定性启发式空间**迁移至**合作多智能体强化学习（MARL）空间**。现有 MTO 方法可大致分为两类：

- **基于损失的方法**：通过动态标量化将多任务损失合并为单一标量，典型代表包括 **Uncertainty Weighting**（Kendall et al., CVPR 2018）和 **DWA**（Liu et al., CVPR 2019）。此类方法计算高效，但损失加权与梯度下降方向之间缺乏直接对应，难以显式处理梯度冲突。
- **基于梯度的方法**：直接在梯度空间中操作，寻找公共下降方向或缓解冲突。代表性工作包括 **MGDA**（Sener & Koltun, NeurIPS 2018）通过求解凸优化问题寻找 Pareto 平稳点；**PCGrad**（Yu et al., NeurIPS 2020）将冲突梯度投影至彼此的法平面；**GradDrop**（Chen et al., NeurIPS 2020）基于梯度符号一致性进行选择性丢弃；**CAGrad**（Liu et al., NeurIPS 2021）在收敛性约束下最小化梯度冲突；**IMTL**（Liu et al., ICLR 2021）通过迭代缩放对齐梯度量级；**Aligned-MTL**（Senushkin et al., CVPR 2023）混合损失与梯度信息进行对齐。

上述方法的共同瓶颈在于：**聚合策略均为确定性规则**，缺乏随机探索能力，在高度非凸的损失景观中易陷入局部最优。此外，多数方法未显式建模任务间梯度冲突的时序演化，导致负迁移难以根除。

TaskForce 通过三个关键设计突破此瓶颈：

| 设计维度 | 基线方法特征 | TaskForce 创新 |
|---------|-------------|---------------|
| **策略类型** | 确定性启发式（固定规则或凸优化单步解） | 随机性策略探索（MARL 智能体输出连续动作） |
| **观测表示** | 完整梯度向量（维度 \|θ\|，计算与存储代价高） | 紧凑 Gram 矩阵（T×T 维度，捕获幅值与对齐信息） |
| **奖励信号** | 纯损失改进（如 IGBv2）或纯梯度量 | 混合奖励：对数损失改进 + 负聚合梯度 L2 范数 |

其中，**IGBv2**（Dai et al., UAI 2023）是唯一引入单智能体 RL 进行损失重加权的基线，但其观测仅为任务损失值，缺乏梯度层面信息，且使用单一智能体而非多智能体协同，本质上仍是基于损失的方法。TaskForce 将 MARL 引入梯度聚合层面，是方法论上的根本差异。

### 2. 与相关领域的交叉定位

TaskForce 处于**多任务优化**、**多智能体强化学习**与**梯度冲突消解**三者的交汇点：

- **MTO 侧**：继承 MGDA 的 Pareto 最优思想（通过梯度奖励鼓励寻找公共下降方向），但将单步优化求解替换为学习型策略，获得跨步决策能力。
- **MARL 侧**：采用 MADDPG（Lowe et al., NeurIPS 2017）的集中式训练-去中心化执行框架，但环境并非传统多智能体博弈场景，而是以 MTL 模型参数更新作为动态环境，任务特定智能体共享全局奖励。
- **梯度冲突侧**：Gram 矩阵观测 $gg^\top$ 显式编码梯度幅值（对角线）与成对对齐（非对角线），为智能体提供冲突感知信号，这与 PCGrad 的余弦相似度判断形成互补——前者用于决策输入，后者用于操作修正。

### 3. 适用边界与局限

**适用场景**：
- 任务数 T 适中的异构多任务学习（论文验证了 T=3 和 T=11 的设置）
- 共享骨干网络的多任务架构（如 MTAN、PSPNet、MPNN）
- 需要同时优化多个可能冲突目标的场景

**已知局限**（论文明确指出的部分）：
1. **训练开销**：需额外维护演员-评论家网络，虽相对骨干网络梯度计算开销较小，但仍增加训练负担。Table 6 的消融显示 MARL 组件引入约 15-20% 的额外计算成本。
2. **可扩展性挑战**：任务数 T 增加时，Gram 矩阵维度以 $O(T^2)$ 增长，智能体数量线性增加，在 T ≫ 100 的大规模场景下可能面临计算瓶颈。

**需要手动验证的边界**：
- 论文未提供 T=2 或 T>20 的实验结果，极端任务数下的行为未知
- 所有实验均使用固定超参数（$\lambda_{\mathcal{L}}=1.0$，$\lambda_{\mathcal{G}}=10^{-3}$），不同任务集上的超参数敏感性缺乏系统研究
- 未涉及异构架构（如视觉+语言任务共享部分参数）的场景

### 4. 开放问题

1. **大规模扩展**：当任务数激增至百级别时，Gram 矩阵的秩结构与稀疏化策略是否可维持观测有效性？能否设计低秩近似或注意力机制降低复杂度？
2. **观测增强**：当前观测仅包含当前步的 Gram 矩阵与损失值，引入历史梯度信息（如梯度动量、二阶统计量）是否能进一步提升智能体的冲突预测能力？
3. **收敛性理论**：MARL 策略的引入使收敛性分析复杂化，混合奖励下的 Pareto 收敛保证尚未建立形式化证明。
4. **动态任务关系**：在持续学习或任务关系动态变化（如课程学习）的场景中，TaskForce 的适应能力与灾难性遗忘问题尚未探索。
5. **超参数鲁棒性**：$\lambda_{\mathcal{L}}$ 与 $\lambda_{\mathcal{G}}$ 的相对权重、软更新系数 $\tau$、演员学习率等对最终性能的敏感性需更系统的消融研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/TaskForce_Cooperative_Multi_agent_Reinforcement_Learning_for_Multi_task_Optimization.pdf]]
