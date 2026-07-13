---
title: "Optimistic Task Inference for Behavior Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Optimistic_Task_Inference_for_Behavior_Foundation_Models.pdf
project_link: null
code_link: https://github.com/ThomasRupf/opti-bfm
openreview_forum_id: m5byThUSNE
aliases:
- OB
- OTIBFM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过在线构建奖励函数的最小二乘估计及其置信椭球，并利用乐观准则（UCB）主动选择任务嵌入以收集最有信息的状态-奖励对，从而在交互中高效地逼近真实任务嵌入。"
primary_logic: "USF框架下奖励、特征与后继特征之间的线性关系将策略搜索简化为线性置信域上界问题，使得带有理论保障的在线任务推理成为可能。"
claims:
- "OpTI-BFM能够利用USF的线性结构，通过在线回归和乐观探索，显著减少任务识别所需的标注数据量。"
- "在DeepMind Control Suite的零样本基准测试中，OpTI-BFM仅需5个episode（5k环境步）即可恢复Oracle性能，远超离线方法所需的数据量。"
- "OpTI-BFM的乐观收集策略所获得的数据比随机采样的数据信息量更大，在等同交互步数下能更准确地推断任务。"
- "即使在准静止或非静止奖励、后继特征不够精确、奖励存在投影误差或观测噪声等假设违背的情况下，OpTI-BFM依然表现出合理的鲁棒性。"
---

# Optimistic Task Inference for Behavior Foundation Models

> [!tip] 核心洞察
> USF框架下奖励、特征与后继特征之间的线性关系将策略搜索简化为线性置信域上界问题，使得带有理论保障的在线任务推理成为可能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向行为基础模型的乐观任务推断 |
| 英文题名 | Optimistic Task Inference for Behavior Foundation Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=m5byThUSNE) · [GitHub](https://github.com/ThomasRupf/opti-bfm) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | OpTI-BFM |
| Dataset | ExORL DMC (Walker, Cheetah, Quadruped), ExORL DMC |

> [!tip] 效果简介
> - ExORL DMC (Walker, Cheetah, Quadruped) 上，Episode Return (Relative to Oracle) 为 接近 Oracle 性能（约 5 episodes 内），对比 LoLA 收敛缓慢；Random 约为 0，变化 OpTI-BFM 显著快于 LoLA，5 个 episode 内达到 Oracle 水平。
> - ExORL DMC 上，数据效率：给定 n 个交互步骤后，利用所收集数据推断出的策略性能 为 OpTI-BFM 和其 TS 变体在所有时间和环境中均排名靠前，对比 RND 或 Random 收集的数据训练策略性能较差，变化 OpTI-BFM 收集的数据在任务推断上更高效，同等数据量下策略性能更高。

## 概要

行为基础模型（Behavior Foundation Models, BFMs）通过后继特征（Successor Features, SFs）实现了零样本策略评估：给定一个线性奖励函数 $r(s) = z^\top \phi(s)$，BFM 可以直接输出对应的最优策略，而无需额外的策略优化。然而，这一范式的实际部署面临一个关键瓶颈——**任务推断（task inference）**，即从用户指定的奖励函数中恢复任务嵌入 $z_r$ 的过程，严重依赖预先收集并全部标注的离线数据集。在实际应用中，获取大规模的状态-奖励标签成本高昂且缺乏灵活性，这限制了 BFM 从实验室走向现实场景的步伐。

本文提出 **OpTI-BFM**（Optimistic Task Inference for BFMs），一种面向 BFM 的在线任务推断框架。其核心洞察在于：USF 框架下奖励函数、状态特征与后继特征之间的线性关系，使得策略搜索问题可以被简化为一个线性置信域上界（Linear UCB）问题。OpTI-BFM 通过在线交互主动选择任务嵌入，利用最小二乘估计及其置信椭球对奖励函数的不确定性进行显式建模，并以乐观准则（UCB）指导数据收集，从而在极少的交互步数内高效逼近真实任务嵌入。

在 DeepMind Control Suite 的零样本基准测试中，OpTI-BFM 仅需 **5 个 episode**（约 5k 环境步）即可恢复 Oracle 性能，远超离线方法所需的数据量。其乐观收集策略所获得的数据比随机采样具有显著更高的信息量，在等同交互步数下能更准确地推断任务。即使在 USF 不够精确、奖励存在投影误差、观测噪声或奖励非平稳等假设违背的情况下，OpTI-BFM 依然表现出合理的鲁棒性。

从方法谱系来看，OpTI-BFM 将 BFM 的任务推断从离线最小二乘投影（一次性闭式解）推进到在线自适应估计，建立了与线性 bandit 理论的直接联系，并提供了遗憾界（regret bound）的理论保障。与基于策略搜索的快速适应方法 **LoLA**（Sikchi et al., 2025）、基于随机网络蒸馏的无任务感知探索方法 **RND**（Burda et al., 2018）等基线相比，OpTI-BFM 在数据效率上具有显著优势，同时计算开销仅为 Oracle 推理的 4-5 倍（Nvidia RTX 4090 上 UCB 变体约 280 Hz，Thompson Sampling 变体约 360 Hz），仍在可接受范围内。

### 行为基础模型中的任务推断瓶颈

行为基础模型（Behavior Foundation Models, BFM）通过预训练策略族，使智能体能够零样本泛化到新任务。其核心机制建立在**通用后继特征**（Universal Successor Features, USF）之上：对于特征函数 $\phi(s)$ 和任务嵌入 $z$，若奖励函数满足线性结构 $r(s) = z^{\top}\phi(s)$，则任意策略 $\pi$ 的 Q 函数可分解为任务嵌入与后继特征的线性积：

$$Q_r^{\pi}(s_0, a_0) = z^{\top} \psi^{\pi}(s_0, a_0)$$

其中 $\psi^{\pi}(s_0, a_0) = \sum_{t \ge 0} \gamma^t \mathbb{E}[\phi(s_t) | s_0, a_0, \pi]$ 为策略 $\pi$ 的期望折扣累积特征。这一线性结构使得 BFM 只需推断出任务嵌入 $z_r$，即可通过预训练的策略 $\pi_z$ 直接执行零样本控制，无需重新训练。

然而，现有 BFM 的任务推断流程存在一个关键瓶颈：**严重依赖离线标记数据集**。标准做法是在预先收集的状态-奖励对数据集 $\mathcal{D}$ 上，通过闭式最小二乘投影获得任务嵌入的点估计：

$$z_{r} = \mathrm{Cov}_{\mathcal{D}}(\phi)^{-1} \mathbb{E}_{s \sim \mathcal{D}}[\phi(s) r(s)]$$

在实际部署中，获取如此完整标注的数据集成本高昂且不灵活——用户需要为大量状态标注奖励信号，而这恰恰是 BFM 试图通过零样本泛化避免的负担。这一矛盾限制了 BFM 从实验室走向实用化部署的路径。

### 核心问题与本文动机

本文瞄准的核心问题是：**能否在仅需少量在线交互和奖励标注的条件下，高效地推断出真实任务嵌入，从而恢复接近 Oracle 的策略性能？**

这引出了一个根本性的框架转换：从“在固定数据集上做一次性投影”转向“在交互中主动收集信息并逐步更新信念”。这一转换带来了两个相互交织的挑战：

1. **探索-利用权衡**：智能体必须在收集奖励信息以改进任务估计，与利用当前估计执行高性能策略之间取得平衡。
2. **标注成本控制**：每次请求奖励标注都会产生实际代价，因此数据收集策略需要具备信息效率——用尽可能少的标注获得尽可能准确的任务推断。

本文的动机正是利用 USF 框架下奖励、特征与后继特征之间的线性关系，将上述挑战形式化为一个可处理的在线学习问题，从而设计出兼具理论保障和实用效率的在线任务推断算法。

## 核心方法与创新机理

OpTI-BFM 的核心创新在于将行为基础模型（BFM）的任务推理从**离线一次性投影**转变为**在线交互式推断**，从而从根本上改变了数据来源与标注代价的结构。这一转变由三个紧密耦合的机制驱动：

1.  **在线最小二乘估计与置信椭球维护**：传统离线方法在固定数据集 $\mathcal{D}$ 上通过闭式解 $z_{r} = \mathrm{Cov}_{\mathcal{D}}(\phi)^{-1} \mathbb{E}_{s \sim \mathcal{D}}[\phi(s) r(s)]$ 一次性获取任务嵌入的点估计。OpTI-BFM 则将任务嵌入的推断建模为在线回归问题，每一步利用新观测的状态-奖励对增量更新正则化最小二乘估计 $\hat{z}_t = V_t^{-1} \sum_{i=0}^{t} \phi(s_i) r_i$（其中 $V_t = \lambda I_d + \sum_{i=0}^{t} \phi(s_i) \phi(s_i)^{\top}$），并同步维护一个以 $\hat{z}_{t-1}$ 为中心的马氏距离置信椭球 $\mathcal{C}_t = \{ z \in \mathbb{R}^d : \| z - \hat{z}_{t-1} \|_{V_{t-1}} \le \beta_t \}$。这一机制将点估计升级为**不确定性感知的信念分布**，为后续的主动探索提供了信息量依据。

2.  **乐观任务嵌入选择（UCB 准则）**：基线方法直接使用估计的 $z_r$ 执行对应策略，本质上是利用当前最优猜测。OpTI-BFM 则采用面对不确定性时的乐观原则，在置信椭球内选择使后验乐观回报最大的任务嵌入：
    $$z_t \in \arg\max_{z \in \mathcal{C}_t} \max_{w \in \mathcal{C}_t} w^{\top} \psi(s_t, z)$$
    该双层最大化问题可进一步化简为单变量 UCB 形式：
    $$\arg\max_{z \in \mathcal{C}_t} \psi(s_t, z)^{\top} \hat{z}_{t-1} + \beta_t \|\psi(s_t, z)\|_{V_{t-1}^{-1}}$$
    这一准则的关键因果效应在于：它引导智能体主动选择那些**当前不确定性高且潜在回报大**的任务嵌入，从而在交互中收集到比随机采样信息量更大的状态-奖励对。实验证据直接支持了这一机制——在同等交互步数下，OpTI-BFM 收集的数据所训练出的策略性能显著优于基于 RND 或随机收集数据的策略（Figure 3）。

3.  **策略执行粒度的自适应调整**：离线方法在整个 episode 内固定任务嵌入。OpTI-BFM 将决策准则的更新频率从 episode 级提升到**每步自适应调整**，使算法能够在 episode 内部根据新观测持续修正对任务的信念。消融实验表明，每步更新比仅在 episode 开始更新收敛更快，尽管最终性能相当（Figure 4）。这一设计进一步压缩了任务识别所需的交互预算。

上述三个 changed slots 共同构成了一个完整的因果闭环：USF 框架下奖励、特征与后继特征之间的线性关系（$Q_r^{\pi}(s_0, a_0) = z^{\top} \psi^{\pi}(s_0, a_0)$）将策略搜索简化为线性置信域上界问题，使得在线任务推理不仅可行，而且具备理论 regret 界保障。实验表明，OpTI-BFM 仅需 **5 个 episode（约 5k 环境步）** 即可恢复 Oracle 性能（Figure 2），远超离线方法所需的数据量，验证了在线乐观推断在标注效率上的决定性优势。

OpTI-BFM 将行为基础模型（BFM）的任务推断从离线、依赖大量标注数据的范式，转变为**在线、主动的数据高效推断框架**。其核心思路是：利用 USF 框架下奖励函数与后继特征之间的线性结构，将策略搜索问题转化为线性置信域上界（UCB）优化问题，从而在交互中高效地逼近真实任务嵌入。

### 框架总览

图 1 对比了标准离线任务推断流程与 OpTI-BFM 的在线框架。传统流程需要预先收集完整的状态-奖励标注数据集，通过闭式最小二乘投影一次性获得任务嵌入的点估计。OpTI-BFM 则采用交互式范式：智能体在每步主动选择任务嵌入 $z_t$，执行对应策略 $\pi_{z_t}$ 的动作，并仅对实际访问的状态请求奖励标注。算法在交互过程中逐步构建对任务嵌入的置信分布，而非依赖预先存储的庞大数据集。

### 核心模块与数据流

OpTI-BFM 的在线推断流程由三个紧密耦合的模块构成：

1. **在线最小二乘估计器**：增量计算正则化最小二乘估计 $\hat{z}_t$ 及精度矩阵 $V_t$。给定到时刻 $t$ 为止观测到的状态-奖励对 $\{(s_i, r_i)\}_{i=0}^t$，估计器以闭式更新维护对最优任务嵌入的均值估计：
   $$\hat{z}_t = V_t^{-1} \sum_{i=0}^{t} \phi(s_i) r_i, \quad V_t = \lambda I_d + \sum_{i=0}^{t} \phi(s_i) \phi(s_i)^{\top}$$
   该模块使算法无需存储历史数据即可增量更新信念。

2. **置信椭球构建**：基于 $V_{t-1}$ 的马氏距离，构建以 $\hat{z}_{t-1}$ 为中心的置信椭球 $\mathcal{C}_t$：
   $$\mathcal{C}_t = \{ z \in \mathbb{R}^d : \| z - \hat{z}_{t-1} \|_{V_{t-1}} \leq \beta_t \}$$
   该椭球以高概率包含真实任务嵌入 $z_r$，为后续乐观探索提供不确定性量化。

3. **乐观 UCB 优化器**：在置信椭球内选择使后验乐观回报最大的任务嵌入：
   $$z_t \in \arg\max_{z \in \mathcal{C}_t} \max_{w \in \mathcal{C}_t} w^{\top} \psi(s_t, z)$$
   该双层最大化问题可化简为单变量 UCB 形式：
   $$z_t = \arg\max_{z \in \mathcal{C}_t} \psi(s_t, z)^{\top} \hat{z}_{t-1} + \beta_t \|\psi(s_t, z)\|_{V_{t-1}^{-1}}$$
   通过随机射击或梯度方法求解，实现“探索-利用”的自动平衡。

### 输入输出规范

- **输入**：预训练的 BFM（提供 USF 函数 $\psi(s, z)$ 和策略族 $\{\pi_z\}$），目标任务的奖励函数 $r(s)$（仅在与环境交互时对访问状态进行标注）。
- **输出**：每步选定的任务嵌入 $z_t$ 及对应动作 $a_t \sim \pi_{z_t}(\cdot|s_t)$，最终收敛到接近真实任务嵌入 $z_r$ 的策略。
- **交互粒度**：默认每步更新任务嵌入（实验表明这比仅在 episode 开始时更新收敛更快），也可配置为 episode 级更新以适配理论分析。

### 关键变体

- **Thompson Sampling 变体（OpTI-BFM-TS）**：从贝叶斯后验高斯分布 $\mathcal{N}(\hat{z}_t, V_t^{-1})$ 中采样任务嵌入，无需显式优化 UCB 目标，计算开销更低（约为 Oracle 的 4 倍 vs. 5 倍）。
- **非平稳奖励变体**：引入遗忘因子 $\rho \in (0, 1]$，对历史数据指数加权（时刻 $s$ 的数据在时刻 $t$ 的权重为 $\rho^{t-s}$），使算法能适应奖励函数的漂移。

OpTI-BFM 的核心机制建立在 USF 框架所揭示的线性结构之上：对于特征空间内的奖励函数，其 Q 函数可表示为目标嵌入与后继特征的线性内积。这一性质将原本复杂的策略搜索问题转化为对线性函数的在线优化，从而使得带理论保障的乐观探索成为可能。本节聚焦于构成该算法的三个关键模块及其数学表述。

### 在线最小二乘估计器

在交互的每一步，算法接收状态 $s_t$ 的特征 $\phi(s_t)$ 及该状态对应的奖励标签 $r_t$。为从这些流式数据中推断真实任务嵌入 $z_r$，OpTI-BFM 维护一个正则化最小二乘估计器。其核心更新规则为：

$$\hat{z}_t = V_t^{-1} \sum_{i=0}^{t} \phi(s_i) r_i, \quad V_t = \lambda I_d + \sum_{i=0}^{t} \phi(s_i) \phi(s_i)^{\top}$$

其中 $V_t$ 为精度矩阵（设计矩阵），$\lambda$ 为正则化系数，$I_d$ 为 $d$ 维单位矩阵。该估计器以增量方式运行：每获取一个新的状态-奖励对，仅需更新 $V_t$ 的逆矩阵和累加项，无需存储完整历史数据集。这正是 OpTI-BFM 摆脱离线标注依赖的关键——它将任务推断从“在固定数据集上一次性投影”转变为“在交互中持续精化信念”。

### 置信椭球构建

仅有均值估计 $\hat{z}_t$ 不足以指导探索。OpTI-BFM 进一步围绕该估计构建一个置信区域，以高概率包含真实任务嵌入 $z_r$：

$$\mathcal{C}_t = \{ z \in \mathbb{R}^d : \| z - \hat{z}_{t-1} \|_{V_{t-1}} \le \beta_t \}$$

此处 $\| \cdot \|_{V_{t-1}}$ 表示由精度矩阵 $V_{t-1}$ 诱导的马氏距离，$\beta_t$ 为置信半径，其取值由理论分析确定，确保 $\mathcal{C}_t$ 以高概率覆盖 $z_r$。该椭球的几何形状由 $V_{t-1}$ 的特征结构决定：在数据充分探索的方向上椭球被压缩（不确定性低），在数据稀疏的方向上椭球被拉伸（不确定性高）。这一结构为后续的乐观探索提供了精确的不确定性量化。

### 乐观 UCB 优化器

给定当前状态 $s_t$ 和置信椭球 $\mathcal{C}_t$，OpTI-BFM 通过求解一个双层最大化问题来选择任务嵌入 $z_t$：

$$z_t \in \arg\max_{z \in \mathcal{Z}} \max_{w \in \mathcal{C}_t} w^{\top} \psi(s_t, z)$$

其直观含义是：在置信椭球内寻找一个“乐观”的任务嵌入 $w$，使得在该嵌入下的期望后继特征回报最大化，然后选择能实现该乐观回报的 $z$。通过利用 USF 的线性结构，该双层问题可等价化简为单变量的 UCB 形式：

$$\arg\max_{z \in \mathcal{C}_t} \psi(s_t, z)^{\top} \hat{z}_{t-1} + \beta_t \|\psi(s_t, z)\|_{V_{t-1}^{-1}}$$

其中第一项为利用项（当前均值估计下的预期回报），第二项为探索项（由置信椭球半径加权的探索奖励）。该目标函数将不确定性直接编码为可优化的正则项，使得 OpTI-BFM 能够系统性地平衡利用与探索。

### 实用变体

在实际部署中，OpTI-BFM 提供了两种实用扩展：

- **Thompson Sampling 变体（OpTI-BFM-TS）**：从贝叶斯后验高斯分布 $\mathcal{N}(\hat{z}_t, V_t^{-1})$ 中直接采样任务嵌入，避免了显式求解 UCB 优化问题，计算开销更低（约为 Oracle 的 4 倍，而 UCB 版本约为 5 倍）。
- **非平稳奖励扩展**：引入遗忘因子 $\rho \in (0, 1]$，对历史观测进行指数加权（时间步 $s$ 的数据在 $t$ 时刻的权重为 $\rho^{t-s}$），使算法能够跟踪随时间变化的奖励函数。当 $\rho < 1$ 时，旧观测的影响逐渐衰减，算法获得适应非平稳任务的能力。

## 实验与关键发现

### 核心发现：5个Episode内恢复Oracle性能

OpTI-BFM 在 DeepMind Control Suite（DMC）的零样本基准测试中展现出惊人的数据效率。如图 2 所示，在 Walker、Cheetah 和 Quadruped 三个环境中，OpTI-BFM 仅需约 **5 个 episode（约 5k 环境步）即可恢复 Oracle 性能**，即达到使用完整离线标注数据集进行任务推断的理想上限。相比之下，基于策略搜索的快速适应方法 LoLA（Sikchi et al., 2025）收敛缓慢，而随机选择任务嵌入的 Random 基线性能始终接近零。这一结果表明，利用 USF 的线性结构进行主动探索，能够将任务识别所需的数据量压缩一个数量级以上。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/003_Figure_2.jpg]]
*Figure 2: Mean relative performance over 10 episodes of interaction in DMC. OpTI-BFM recovers Oracle performance in 5 episodes. We report per-task absolute performance in Fig. 14 in Appendix C*

OpTI-BFM 的 Thompson Sampling 变体（OpTI-BFM-TS）表现与 UCB 版本相当，验证了乐观探索框架的通用性。所有实验均在 3 个随机种子上完成，误差条为最小-最大区间，结果稳健。

### 数据效率的深层归因：乐观收集的信息增益

为验证性能提升确实源于更高效的数据收集策略，而非仅仅是算法本身的优势，作者设计了一个关键实验（图 3）：在给定不同数量的环境交互步后，利用收集到的数据训练策略，并评估策略性能。结果显示，OpTI-BFM 及其 TS 变体在所有环境和时间步上均位列前茅，显著优于基于随机网络蒸馏的无任务感知探索方法 RND（Burda et al., 2018）和 Random 基线。这直接证明：**OpTI-BFM 的乐观采集策略所获得的状态-奖励对比随机采样具有更高的信息密度**，能更准确地定位真实任务嵌入 $z_r$，从而在同等交互预算下产生更优的策略。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/002_Figure_3.jpg]]
*Figure 3: Relative performance after different # of environment interactions. OpTI-BFM is consistently among the top performers for all environments and time-steps. We show per task performance in Fig. 15 in Appendix C*

### 消融实验：每步更新 vs. 每Episode更新

OpTI-BFM 理论分析部分假设仅在每个 episode 开始时更新决策规则，但实际实现中允许每步自适应调整任务嵌入。消融实验（图 4）对比了两种粒度：**每步更新（默认）的收敛速度显著快于仅在 episode 开始更新的变体（-EP）**，但最终性能趋于一致。这说明在线微调任务嵌入能够更快地利用新观测修正信念，尽管从 regret 角度两者的渐进性能可能相当。注意，当前理论 regret 界仅覆盖 episode 级更新版本，将保证扩展到每步更新仍是一个开放问题。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/005_Figure_4.jpg]]
*Figure 4: Relative performance of our methods, and their variants that keep task embeddings fixed for each episode (-EP). Updating the task embedding during the episode leads to faster convergence. For longer episode evaluations see Fig. 16 in Appendix C*

### 非平稳奖励适应：遗忘因子的作用

标准 BFM 假设奖励函数固定，但实际任务可能随时间变化（如追踪变化的目标速度）。OpTI-BFM 通过引入遗忘因子 $\rho$（指数衰减历史观测权重）来处理非平稳奖励。在自定义的 DMC Walker 速度追踪任务中（图 5），当 $\rho = 1$（无遗忘）时，算法无法适应速度目标的变化；**一旦将 $\rho$ 降至 0.99 或 0.95，OpTI-BFM 即可准确追踪目标速度**。过小的 $\rho$ 可能导致不确定性无法充分降低，因此遗忘因子的选择需要在适应速度与估计稳定性之间权衡，目前仍需手动设定。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/006_Figure_5.jpg]]
*Figure 5: Horizontal velocity of OpTI-BFM in our custom velocity tracking tasks in DMC Walker for different decay rates ρ. OpTI-BFM can adapt to non-stationary reward functions when decaying the weight of old observations*

### 预热效应：少量离线标注的加速作用

尽管 OpTI-BFM 的目标是减少标注需求，但在实际部署中可能已存在少量标注数据。实验（图 6）表明，利用 $n$ 个 i.i.d. 离线标注状态-奖励对预热最小二乘估计器，可以快速提升初始性能：**随着 $n$ 从 0 增至 500，初始 episode 的回报迅速上升**。这为半在线场景提供了平滑过渡方案——用极少量离线标注换取冷启动阶段的显著加速。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/007_Figure_6.jpg]]
*Figure 6: Return of OpTI-BFM in DMC Cheetah when warm-starting with n i.i.d. labeled states from the training dataset. Initial performance increases quickly as n grows. We report full results in Fig. 17 in Appendix C*

### 鲁棒性分析：假设违背下的表现

OpTI-BFM 的理论保障依赖于 USF 完美且奖励严格线性的假设。附录中的敏感性分析系统考察了这些假设被违背时的性能退化：

- **USF 偏差**（图 11）：引入与任务嵌入 $z$ 相关的系统性偏置 $\psi'(s_t, z) = \psi(s_t, z) + \alpha \cdot \text{MLP}(z; \theta)$ 后，性能随偏差幅度 $\alpha$ 增大而恶化，但需要非常大的偏差才会退化为随机基线，表明算法对 USF 质量具有合理容忍度。
- **奖励非线性**（图 12）：奖励函数的投影误差在合理范围内对 OpTI-BFM 的影响有限，其性能劣化程度与 Oracle 类似，说明瓶颈主要在于 BFM 本身的表示能力而非在线推理机制。
- **观测噪声**（图 13）：添加高斯观测噪声会按预期减慢收敛速度，但算法仍可正常工作，未出现崩溃性失效。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_m5byThUSNE/figures/014_Figure_11.jpg]]
*Figure 11: Performance of OpTI-BFM over 10 episodes in the Cheetah environment with a mismatch between ψ and ϕ (see Eq. (125)) of magnitude α. Performance deteriorates as α increases*

### 计算开销与实用性

在 Nvidia RTX 4090 GPU 上，OpTI-BFM 的推理频率约为 280 Hz（UCB 版本）和 360 Hz（TS 版本），分别是纯策略执行（Oracle）的约 5 倍和 4 倍（表 1）。UCB 优化依赖随机射击，梯度变体（OpTI-BFM +grad）性能相当但计算成本更高（图 8、图 9），因此随机射击在效率与效果之间取得了良好平衡。对于大多数机器人控制场景，280 Hz 的决策频率已足够实时部署，但对延迟极度敏感的应用可能仍需权衡。

### 实验公平性说明

- 所有实验在 3 个不同训练种子上完成，误差条/阴影区域为最小-最大区间。
- OpTI-BFM 的超参数非常鲁棒，仅通过 3 个值的网格搜索即选定固定的 $\beta$ 或 $\sigma$。
- LoLA 基线在与其原始论文相同的条件下（随机初始化任务嵌入）也表现出较慢的改进，与本文结果一致，排除了不公平实现的可能性。

## 定位与知识库关联

### 1. 核心定位：从离线投影到在线线性置信域推断

OpTI-BFM 将行为基础模型（BFM）的任务推理问题从**离线固定数据集上的闭式投影**重新定义为**在线线性置信域优化**问题。其核心洞见在于：当奖励函数可表示为特征 $φ(s)$ 的线性组合 $r(s)=z^\top φ(s)$ 时，后继特征（Successor Features, SFs）框架下的 Q 函数满足 $Q_r^\pi(s,a)=z^\top ψ^\pi(s,a)$。这一线性结构使策略搜索退化为一个线性函数在线优化问题，从而可以直接嫁接线性 bandit 文献中的 UCB 机制。

具体而言，OpTI-BFM 维护两个核心组件：
- **增量正则化最小二乘估计器**：在线更新精度矩阵 $V_t$ 和任务嵌入均值估计 $\hat{z}_t$（Eq. 7-8），实现对真实 $z_r$ 的渐进逼近。
- **置信椭球** $\mathcal{C}_t = \{ z : \|z - \hat{z}_{t-1}\|_{V_{t-1}} \leq \beta_t \}$（Eq. 9）：以高概率包含真实任务嵌入，为乐观探索提供不确定性量化。

决策时，算法在置信椭球内选择使后验乐观回报最大的任务嵌入（Eq. 10），等价于求解 UCB 形式的目标函数（Eq. 12），从而在探索与利用之间取得理论上有保障的平衡。

### 2. 与相关工作的关系

#### 2.1 行为基础模型与后继特征

OpTI-BFM 直接构建在 BFM 的零样本策略评估能力之上。BFM 预训练一系列参数化策略 $\{π_z\}$，使每个策略对形如 $z^\top φ(s)$ 的奖励函数最优。OpTI-BFM 不修改 BFM 的预训练过程，而是替换其**任务推理阶段**：将需要大量标注的离线投影替换为少量在线交互中的主动推断。这意味着 OpTI-BFM 的性能上限受限于底层 BFM 的质量——若 USF 与真实后继特征存在系统性偏差，算法性能会随偏差幅度 $α$ 增大而退化（附录 B.5，Figure 11）。

#### 2.2 与在线适应方法的对比

- **LoLA**（Sikchi et al., 2025）：作为基于策略搜索的快速适应方法，LoLA 忽略 BFM 的线性结构，直接从交互中优化策略参数。在相同实验设置下，LoLA 的收敛速度显著慢于 OpTI-BFM，验证了显式利用线性结构进行任务推断的效率优势。值得注意的是，LoLA 在其原始论文中同样表现出较慢的改进速度，与本文观察一致。
- **RND**（Burda et al., 2018）：基于随机网络蒸馏的无任务感知探索方法。在数据效率对比中（Figure 3），RND 收集的数据用于任务推断时性能明显低于 OpTI-BFM，说明任务感知的乐观探索比通用探索策略更适合 BFM 的任务识别场景。

#### 2.3 与线性 Bandit 理论的关系

OpTI-BFM 的理论 regret 界（附录 A）直接建立在线性 bandit 的 UCB 分析框架之上。关键差异在于：标准线性 bandit 中臂的特征向量是固定的，而 OpTI-BFM 中后继特征 $ψ(s_t, z)$ 依赖于当前选择的 $z$，引入了策略与特征之间的耦合。理论分析仅针对每 episode 更新一次任务嵌入的简化版本，且假设 USF 完美、奖励严格线性。当这些假设被违反时，regret 可能不再具有次线性保证（附录 A.5 分析了有界偏差情况）。

### 3. 适用边界与局限

**理论假设的脆弱性**：
- 理论 regret 界要求 USF 完美且奖励严格位于特征张成的线性空间内。实际中，奖励函数的投影误差会导致性能劣化，尽管实验表明在合理误差范围内 OpTI-BFM 的退化程度与 Oracle 类似（附录 B.6，Figure 12）。
- USF 与真实后继特征的系统性偏差 $α$ 会导致性能下降，但实验显示需要非常大的偏差才会退化为随机基线（附录 B.5，Figure 11）。

**对预训练 BFM 的完全依赖**：
- OpTI-BFM 无法在零样本场景下从无到有学习任务嵌入，其任务推断能力完全受限于预训练 BFM 的覆盖范围和质量。若目标任务的奖励函数无法在特征空间中良好表示，算法将无法有效工作。

**优化方法的局限性**：
- UCB 目标的优化依赖随机射击（random shooting），无法保证找到全局最优的 $z_t$。梯度方法（OpTI-BFM +grad）计算量更大但未带来显著性能提升（Figure 8-9），说明在当前问题规模下随机射击已足够有效。
- 这一局限可能在特征空间维度更高或几何结构更复杂时变得显著。

**计算开销**：
- 相比仅执行策略的 Oracle 推理，OpTI-BFM 约慢 5 倍（UCB 变体，280 Hz），OpTI-BFM-TS 约慢 4 倍（360 Hz），在 Nvidia RTX 4090 上测试（Table 1）。对于实时性要求极高的应用，这一额外开销可能构成限制。

**非平稳奖励的局限**：
- 非平稳变体需要手动选定遗忘因子 $ρ$。过小的 $ρ$ 会导致历史数据权重过低，不确定性无法充分降低；过大的 $ρ$ 则无法有效跟踪奖励变化。目前缺乏自动调整 $ρ$ 的机制。

### 4. 开放问题

1. **理论扩展**：当前 regret 分析仅覆盖每 episode 更新一次任务嵌入的版本，而实验表明每步更新可显著加速收敛（Figure 4）。将理论保证扩展到每步更新版本是一个重要的理论缺口。

2. **特征空间的几何与统计性质**：特征空间 $\mathcal{Z}$ 中元素的属性在理论和实践上均未充分理解。理解这些性质对于提升任务推理精度和跨任务泛化能力至关重要。

3. **大规模场景的可扩展性**：当前实验在状态特征维度较低（DeepMind Control Suite）的场景下进行。在更大规模、更复杂的预训练数据集（如像素输入）上，OpTI-BFM 的计算效率和标注效率是否仍能保持，尚待验证。

4. **主动标注预算分配**：如何结合信息阈值 $κ$ 更智能地决定何时请求奖励标签（Figure 7），以在交互成本与标注成本之间取得更优权衡，是一个有实践价值的方向。

5. **USF 质量的自适应感知**：当前算法对 USF 偏差的敏感度依赖实验评估，缺乏在线检测和自适应纠正 USF 误差的机制。

## 原文 PDF

![[paperPDFs/ICLR_2026/Optimistic_Task_Inference_for_Behavior_Foundation_Models.pdf]]
