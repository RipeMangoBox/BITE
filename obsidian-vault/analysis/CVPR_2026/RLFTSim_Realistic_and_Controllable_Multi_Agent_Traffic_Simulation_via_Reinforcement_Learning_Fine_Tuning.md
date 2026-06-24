---
title: "RLFTSim: Realistic and Controllable Multi-Agent Traffic Simulation via Reinforcement Learning Fine-Tuning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RLFTSim_Realistic_and_Controllable_Multi_Agent_Traffic_Simulation_via_Reinforcement_Learning_Fine_Tuning.pdf
project_link: "https://ehsan-ami.github.io/rlftsim"
code_link: null
aliases:
- RLFTSim
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过Meta-metric Leave-One-Out（MLOO）将RMM转化为每个回滚（rollout）的相对贡献信号，并利用REINFORCE在线策略梯度与KL正则化进行闭环微调，同时引入事后经验回放（HER）和目标条件，实现可控性蒸馏。
primary_logic: MLOO在保持无偏梯度估计的同时，将奖励方差按1/N²快速下降，使基于RL的细粒度现实性对齐成为可能；结合目标条件与事后经验回放，可在不牺牲真实感的前提下赋予仿真器明确的可控性。
claims:
- MLOO提供无偏策略梯度估计（Proposition 1）
- MLOO的方差随回滚数N呈二次下降（Proposition 3），而RLOO的方差保持不变
- 在奖励函数消融实验中，RMMMLOO显著优于所有其他奖励设计（Table 2、Table S4）
- RLFTSim在WOSAC排行榜上取得SOTA真实感（RMM 0.7867）和最佳交互指标（Interactive 0.8129）
---

# RLFTSim: Realistic and Controllable Multi-Agent Traffic Simulation via Reinforcement Learning Fine-Tuning

> [!tip] 核心洞察
> MLOO在保持无偏梯度估计的同时，将奖励方差按1/N²快速下降，使基于RL的细粒度现实性对齐成为可能；结合目标条件与事后经验回放，可在不牺牲真实感的前提下赋予仿真器明确的可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | RLFTSim：通过强化学习微调实现真实可控的多智能体交通仿真 |
| 英文题名 | RLFTSim: Realistic and Controllable Multi-Agent Traffic Simulation via Reinforcement Learning Fine-Tuning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19033) · [Project](https://ehsan-ami.github.io/rlftsim) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | RLFTSim |
| Dataset | WOSAC private test split, Full WOMD validation set |

> [!tip] 效果简介
> - WOSAC private test split (leaderboard) 上，RMM↑ 0.7867 vs 0.7824 (SMART-tiny †) (+0.0043)。
> - WOSAC private test split 上，Kinematic↑ 0.4927 vs 0.4854 (SMART-tiny †) (+0.0073)；Interactive↑ 0.8129 vs 0.8089 (SMART-tiny †) (+0.0040)。
> - Full WOMD validation set 上，RMM↑ (ablation) 0.7830 (RMMMLOO) vs 0.7804 (SMART-tiny ref.) (+0.0026)。

## 概述

**问题瓶颈**：开环模仿学习（行为克隆）训练的多智能体交通仿真器在闭环部署时，因误差累积导致分布偏移和因果混淆，仿真真实性严重退化。直接优化WOSAC现实性元指标（RMM）作为奖励信号又面临信号稀疏、方差过大的难题，无法用于强化学习（RL）训练。

**核心方法**：RLFTSim提出**Meta-metric Leave-One-Out（MLOO）**，将全局RMM转化为每个回滚（rollout）的相对贡献信号，实现低方差、密集的逐回滚奖励；在此基础上采用REINFORCE在线策略梯度与KL散度正则化进行闭环微调，直接对齐真实数据分布。同时引入**目标条件微调（GCFT）**与事后经验回放（HER），在不牺牲真实感的前提下赋予仿真器明确的可控性。

**关键洞察**：MLOO在保持无偏梯度估计（Proposition 1）的同时，奖励方差随回滚数N按1/N²快速下降（Proposition 3），使基于RL的细粒度现实性对齐成为可能。

**主要结果**：
- 在WOSAC排行榜私有测试集上取得**SOTA真实感**（RMM 0.7867），交互指标最优（Interactive 0.8129）（Table 1）。
- 奖励函数消融实验中，RMMMLOO显著优于minADE、RMMRLOO及所有启发式奖励设计（Table 2、Table S4）。
- 目标条件微调在非真实轨迹的机动控制基准上大幅超越基线（Table S5），验证了可控性蒸馏的有效性。
- 方法具有模型无关性，可提升不同基础模型（如TrafficBots V1.5）的真实感（Table S6）。

## 背景与动机

自动驾驶系统的安全验证高度依赖高保真交通仿真，以生成多样化且真实的交互场景。Waymo Open Sim Agents Challenge（WOSAC）为此提供了标准化评估框架，其核心指标**现实性元指标（RMM）**通过比较仿真轨迹与真实轨迹在多种特征维度上的离散分布来度量仿真真实感：

$$\mathrm{RMM} = \sum_{d=1}^D w_d \left[ \prod_{(a,t) \in V} \hat{P}_{d,a}(k_{d,a,t}^*) \right]^{\frac{1}{|V|}}$$

然而，当前主流的交通仿真模型普遍采用**开环模仿学习（行为克隆）**进行训练。这种范式存在一个根本性瓶颈：模型仅在历史真实轨迹上学习条件分布，从未经历自身决策的闭环反馈。一旦部署到仿真环境中，由误差累积引发的分布偏移和因果混淆会迅速放大，导致生成轨迹偏离真实分布——例如车辆驶出道路、与横向车流发生碰撞等严重失真行为（见 Figure 3 定性对比）。

一个直观的改进思路是直接在闭环环境中优化 RMM。但这一思路面临双重障碍：**RMM 作为奖励信号极为稀疏**（仅在完整回滚结束后才能计算），且**方差极大**——多智能体交互的随机性使得同一场景的不同回滚间 RMM 波动剧烈，直接用于强化学习训练几乎无法收敛。

上述困境揭示了该领域的核心缺口：**如何在闭环训练中获得低方差、密集的奖励信号，使基于强化学习的现实性对齐成为可能？** 更进一步，如何在提升真实感的同时，赋予仿真器明确的**可控性**——使仿真器能够根据外部指定的目标（如特定机动）生成条件化场景——而不牺牲已获得的真实感？

RLFTSim 正是针对这一双重动机而设计：通过引入**元指标留一法（MLOO）**将 RMM 转化为每个回滚的相对贡献信号，并利用闭环在线策略梯度进行微调；同时引入目标条件微调与事后经验回放，在不损害真实感的前提下蒸馏可控行为。

## 核心创新

RLFTSim 的核心创新在于将交通仿真模型的后训练从**开环模仿学习**范式迁移到**闭环在线强化学习微调**范式，并通过三项关键设计解决直接优化真实感指标所面临的信号稀疏与高方差难题，从而在不牺牲真实感的前提下首次赋予仿真器明确的可控性。

### 1. 训练范式转换：从开环模仿到闭环RL微调

传统交通仿真模型（如 SMART-tiny）依赖开环行为克隆进行训练，其根本瓶颈在于无法捕捉闭环部署中由误差累积引起的**分布偏移**和**因果混淆**。RLFTSim 将训练范式切换为闭环在线 RL 微调，使模型在自生成的回滚（rollout）轨迹上进行策略优化，直接最大化真实感元指标（RMM）。这一范式转换是后续所有创新得以生效的前提——只有闭环训练才能让模型“看见”并修正自身错误累积带来的非真实行为。

**Changed Slot：训练范式**  
- Baseline：开环模仿学习（行为克隆）  
- Proposed：闭环在线 RL 微调，直接优化 RMM（通过 MLOO）

### 2. 奖励信号设计：MLOO 低方差稠密奖励

直接使用 RMM 作为 RL 奖励面临两个致命问题：**信号稀疏**（整个场景只有一个标量 RMM）和**方差极大**（不同回滚间的 RMM 波动剧烈）。RLFTSim 提出 **Meta-metric Leave-One-Out（MLOO）**，将 RMM 转化为每个回滚的相对贡献信号：

$$\mathrm{RMM}_i^{\mathrm{MLOO}} = \frac{1}{N} \sum_{j=1}^N \mathrm{RMM}_{-j} - \mathrm{RMM}_{-i}$$

其中 $\mathrm{RMM}_{-i}$ 表示从 $N$ 个回滚中剔除第 $i$ 个后的 RMM 估计。该设计的核心洞察是：**MLOO 在保持无偏梯度估计的同时，使奖励方差按 $1/N^2$ 快速下降**。理论分析（Proposition 1, Proposition 3）证明 MLOO 提供无偏策略梯度估计，且其方差随回滚数 $N$ 呈二次衰减，而传统 RLOO 估计器的方差保持不变。这一性质使基于 RL 的细粒度真实感对齐在样本效率上成为可能。

**Changed Slot：奖励信号**  
- Baseline：无（仅模仿损失）或稀疏的 RMM  
- Proposed：MLOO——低方差、密集的每个回滚奖励

### 3. 可控性蒸馏：目标条件微调 + 事后经验回放

预训练仿真模型是“黑箱”生成器，无法按用户意图控制自车行为。RLFTSim 通过 **目标条件微调（GCFT）** 与 **事后经验回放（HER）** 的组合，在不牺牲真实感的前提下蒸馏出可控性。具体而言：

- **目标表示**：通过位置编码指示（indication）或拼接（concatenation）将目标点注入智能体的观测，使策略学会关注外部目标。
- **混合奖励**：$R_i^{\mathrm{GCFT}} = (1-\lambda) \mathrm{RMM}_i^{\mathrm{MLOO}} + \lambda R_i^{\mathrm{goal}}$，用 $\lambda$ 平衡真实感与目标到达。
- **HER 数据增强**：利用同一场景中最佳回滚的终端状态作为替代目标，扩展训练数据的多样性，使模型学会到达非真实轨迹上的指定目标点。

**Changed Slot：可控性机制**  
- Baseline：无可控性（黑箱生成）  
- Proposed：目标条件微调（GCFT）+ 事后经验回放（HER）

### 4. 优化方法：REINFORCE + KL 正则化

与监督学习的交叉熵损失不同，RLFTSim 采用 **REINFORCE 策略梯度**配合 **KL 散度正则化**进行优化：

$$g = \sum_{i=1}^N \nabla_\theta \log \pi_\theta(\tau_i) \; \mathrm{RMM}_i^{\mathrm{MLOO}}$$

KL 正则化项约束微调策略不偏离预训练模型过远，防止灾难性遗忘和策略崩溃。这一设计使 RLFTSim 能够从任意预训练交通仿真模型出发进行微调，具有**模型无关性**——实验证明该方法同样能提升 TrafficBots V1.5 的真实感（RMM 从 0.7174 提升至 0.7231）。

**Changed Slot：优化方法**  
- Baseline：监督学习（交叉熵）  
- Proposed：REINFORCE + KL 散度正则化

### 创新总结

RLFTSim 的四项 changed slots 构成一个完整的创新链条：**闭环训练范式**提供正确的优化环境，**MLOO 奖励**解决信号质量瓶颈，**GCFT+HER** 赋予可控性，**REINFORCE+KL** 保证稳定微调。这一链条的核心理论贡献在于揭示了 MLOO 的方差衰减性质，使原本不可行的 RMM 直接优化成为现实。

## 整体框架

RLFTSim是一个基于强化学习微调的后训练框架，旨在解决开环模仿学习在闭环部署中因分布偏移和因果混淆导致的仿真真实感不足问题。其核心思路是：将多智能体交通仿真建模为上下文马尔可夫决策过程（Contextual MDP）$(S_t, A_t, S_{t+1}, R_{t+1}, C, G)$，在预训练模型的基础上进行闭环在线RL微调，直接优化Waymo现实性元指标（RMM）。

框架包含两种工作模式，对应不同的仿真需求：

1. **无目标仿真模式（Goal-free simulation）**：纯粹追求真实感对齐，不施加外部控制信号。
2. **目标条件仿真模式（Goal-conditioned simulation）**：在保持真实感的前提下，赋予仿真器可控性，使其能够响应外部指定的目标点。

两种模式共享同一套核心优化机制，其整体pipeline如下：

**输入**：从数据集中采样一个种子场景（seed scenario），包含历史观测轨迹和地图上下文。

**回滚生成**：基于当前策略模型 $\pi_\theta$，在闭环环境中生成 $N$ 条完整的仿真回滚（rollouts），每条回滚包含场景中所有智能体的轨迹。

**奖励计算**：这是框架的关键创新。直接使用RMM作为奖励信号面临稀疏性和高方差问题，无法有效驱动RL训练。RLFTSim引入**元指标留一法（Meta-metric Leave-One-Out, MLOO）**，将全局RMM转化为每个回滚的密集、低方差奖励信号：

$$\mathrm{RMM}_i^{\mathrm{MLOO}} = \frac{1}{N} \sum_{j=1}^N \mathrm{RMM}_{-j} - \mathrm{RMM}_{-i}$$

其中 $\mathrm{RMM}_{-i}$ 表示排除第 $i$ 条回滚后，用剩余 $N-1$ 条回滚计算得到的RMM值。该奖励衡量每条回滚对整体真实感的相对贡献：贡献高于平均水平的回滚获得正奖励，反之获得负奖励。

**策略优化**：使用REINFORCE策略梯度算法，以MLOO奖励作为权重进行参数更新：

$$g = \sum_{i=1}^N \nabla_\theta \log \pi_\theta(\tau_i) \; \mathrm{RMM}_i^{\mathrm{MLOO}}$$

同时引入KL散度正则化，约束微调后的策略不偏离预训练模型过远，防止灾难性遗忘。

**可控性蒸馏**：在目标条件模式下，框架通过**目标条件微调（Goal-Conditioned Fine-Tuning, GCFT）**实现可控性。具体而言：
- 将目标点信息通过**位置编码指示（positional encoding indication）**或**拼接（concatenation）**方式注入智能体的观测表示。
- 采用**事后经验回放（Hindsight Experience Replay, HER）**，将每条回滚中最佳到达目标的终端状态作为替代目标，扩展训练数据。
- 奖励函数结合现实性奖励和目标到达奖励：$R_i^{\mathrm{GCFT}} = (1-\lambda) \mathrm{RMM}_i^{\mathrm{MLOO}} + \lambda R_i^{\mathrm{goal}}$，通过 $\lambda$ 平衡真实感与可控性。

**输出**：微调后的策略模型，能够在给定场景下生成高真实感仿真轨迹，或在指定目标条件下生成符合要求且保持真实感的机动行为。

整个pipeline的闭环在线优化特性使其能够克服开环训练中的分布偏移问题，而MLOO的低方差特性（方差随回滚数 $N$ 呈 $1/N^2$ 下降）则保证了RL训练的样本效率和稳定性。框架具有模型无关性，已在SMART-tiny和TrafficBots V1.5两种不同基础模型上验证有效。

### 补充图表

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/001_Figure_1.jpg]]
*Figure 1: Post-training with RLFTSim. For a seed scenario from the dataset, multiple rollouts are generated. The main reward function is defined based on time-independent distribution matching of the simulated scenarios and the expert demonstration in several feature spaces. This closed-loop on-policy optimization enhances realism beyond what open-loop imitation learning achieves alone*

## 核心模块与公式推导

RLFTSim 围绕一个核心洞察展开：**开环模仿学习无法应对闭环部署中的分布偏移**，而直接以 Waymo 现实性元指标（RMM）作为强化学习奖励信号又面临信号稀疏、方差过大的问题。为此，RLFTSim 设计了三个关键模块，构成完整的闭环微调管线。

### 4.1 元指标留一法奖励（MLOO）

RMM 是一个在多个特征维度上比较模拟轨迹与真实轨迹离散分布的复合指标，其定义为：

$$\mathrm{RMM} = \sum_{d=1}^D w_d \left[ \prod_{(a,t) \in V} \hat{P}_{d,a}(k_{d,a,t}^*) \right]^{\frac{1}{|V|}}$$

其中 $d$ 为特征维度，$w_d$ 为维度权重，$V$ 为验证集，$\hat{P}_{d,a}$ 为维度 $d$ 上智能体 $a$ 的经验分布。RMM 本质上是一个**场景级聚合指标**，无法直接分解为单个回滚（rollout）的贡献，导致直接用作 RL 奖励时信号极度稀疏。

MLOO 的核心思想是：通过留一法（Leave-One-Out）将 RMM 转化为**每个回滚的相对贡献信号**。对于 $N$ 个回滚 $\{\tau_1, \ldots, \tau_N\}$，定义回滚 $i$ 的 MLOO 奖励为：

$$\mathrm{RMM}_i^{\mathrm{MLOO}} = \frac{1}{N} \sum_{j=1}^N \mathrm{RMM}_{-j} - \mathrm{RMM}_{-i}$$

其中 $\mathrm{RMM}_{-i}$ 表示移除第 $i$ 个回滚后剩余 $N-1$ 个回滚计算的 RMM 值。该公式的直观含义是：**如果移除回滚 $i$ 导致 RMM 下降幅度大于平均移除效应，则回滚 $i$ 对整体真实感有正向贡献，获得正奖励**。

MLOO 具备两个关键理论性质（经命题证明，置信度 0.95）：
- **无偏性**（Proposition 1）：基于 MLOO 奖励的 REINFORCE 策略梯度估计器 $g = \sum_{i=1}^N \nabla_\theta \log \pi_\theta(\tau_i) \, \mathrm{RMM}_i^{\mathrm{MLOO}}$ 是 $\nabla_\theta \mathbb{E}[\mathrm{RMM}(\tau_{1:N-1})]$ 的无偏估计。
- **方差二次衰减**（Proposition 3）：MLOO 的奖励方差随回滚数 $N$ 以 $1/N^2$ 速率下降，而传统 RLOO 估计器的方差基本保持不变。这一性质使 MLOO 在有限采样下提供低方差、密集的奖励信号，是实现样本高效 RL 微调的关键。

### 4.2 闭环策略优化

RLFTSim 采用 **REINFORCE + KL 散度正则化** 的在线策略梯度框架进行微调。优化目标在最大化 MLOO 奖励的同时，通过 KL 散度约束微调策略 $\pi_\theta$ 不偏离预训练参考模型 $\pi_{\text{ref}}$ 过远，以防止灾难性遗忘和训练不稳定。

策略梯度估计器为：

$$g = \sum_{i=1}^N \nabla_\theta \log \pi_\theta(\tau_i) \, \mathrm{RMM}_i^{\mathrm{MLOO}}$$

KL 正则化项的具体控制机制在附录 B 中描述（KL controller），其作用是自适应调节正则化强度，平衡探索与稳定性。

### 4.3 目标条件微调（GCFT）与事后经验回放（HER）

为实现**不牺牲真实感的可控性蒸馏**，RLFTSim 引入目标条件微调（GCFT）。在 GCFT 模式下，策略接收外部目标 $G$（如目标位置点）作为额外输入，奖励函数变为现实性奖励与目标到达奖励的加权组合：

$$R_i^{\mathrm{GCFT}} = (1-\lambda) \, \mathrm{RMM}_i^{\mathrm{MLOO}} + \lambda \, R_i^{\mathrm{goal}}$$

其中 $\lambda$ 平衡真实感与可控性，$R_i^{\mathrm{goal}}$ 为目标到达奖励（支持软/硬两种准则）。

目标表示采用两种方式：
- **拼接（concatenation）**：将连续目标坐标直接拼接到智能体的状态表征中。
- **位置编码指示（positional encoding indication）**：通过位置编码将目标信息注入智能体观测。

为缓解稀疏目标奖励问题，GCFT 借鉴**事后经验回放（HER）**：对于每个场景，将当前回滚组中最佳回滚的终端状态作为替代目标，扩充训练数据，使模型从“未到达目标”的经验中也能学习（Algorithm 1 描述了完整流程）。

### 4.4 管线总览

RLFTSim 的完整管线（Figure 1）包含以下模块：
1. **回滚生成**：从数据集种子场景出发，通过当前策略生成 $N$ 个闭环回滚。
2. **MLOO 奖励计算**：基于留一法 RMM 估计为每个回滚计算低方差贡献信号。
3. **策略梯度更新**：使用 REINFORCE + KL 正则化进行在线策略优化。
4. **可控性蒸馏**（可选）：在 GCFT 模式下，结合目标条件和 HER 赋予仿真器明确的可控性。

### 补充图表

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/005_Figure_2.jpg]]
*Figure 2: Empirical reward variance of MLOO and RLOO on the validation set, computed over rollouts per scenario for varying N . Shaded regions represent ±1 std. in log space*

## 实验与分析

### 核心实验设计

RLFTSim 的实验围绕两个核心目标展开：**真实感对齐**（realism alignment）与**可控性蒸馏**（controllability distillation）。所有实验均基于 Waymo Open Sim Agents Challenge（WOSAC）协议，每场景生成 32 条回滚轨迹，使用 Waymo Open Motion Dataset（WOMD）的私有测试集（排行榜）和全量验证集进行评估。

真实感的核心指标是 **Waymo Realism Meta-Metric（RMM）**，其定义为多维度特征分布匹配的加权几何平均：

$$\mathrm{RMM} = \sum_{d=1}^D w_d \left[ \prod_{(a,t) \in V} \hat{P}_{d,a}(k_{d,a,t}^*) \right]^{\frac{1}{|V|}}$$

其中 $d$ 为特征维度索引，$(a,t)$ 遍历所有待评估的智能体-时间步对，$\hat{P}_{d,a}$ 为离散化后的经验分布匹配概率。RMM 越高，表示仿真轨迹与真实数据在统计分布上越一致。WOSAC 还提供了 Kinematic、Interactive 和 Map-based 等子指标，用于分解真实感的不同方面。

可控性评估则采用自建的机动控制基准（maneuver controllability benchmark），通过设定目标点（如 U 形转弯、左转等）来衡量模型在保持真实感的同时执行指定机动的能力，主要指标包括 Miss Rate（未到达率，越低越好）和 Arrival Rate（到达率，越高越好）。

预训练参考模型为 **SMART-tiny**（作者重训练版本，记为 SMART-tiny †），在 WOSAC 排行榜上 RMM 达到 0.7824。RLFTSim 在此基础模型上进行闭环 RL 微调，使用 MLOO 奖励信号、REINFORCE 策略梯度和 KL 散度正则化。

---

### 主结果：WOSAC 排行榜 SOTA 真实感

**Table 1** 展示了 WOSAC 私有测试集排行榜上的核心结果。RLFTSim 在所有真实感指标上均超越参考模型 SMART-tiny †：

| 指标 | SMART-tiny † | RLFTSim | 提升 |
|------|-------------|---------|------|
| **RMM↑** | 0.7824 | **0.7867** | +0.0043 |
| **Kinematic↑** | 0.4854 | **0.4927** | +0.0073 |
| **Interactive↑** | 0.8089 | **0.8129** | +0.0040 |
| **Map-based↑** | 0.6991 | **0.7014** | +0.0023 |

RLFTSim 的 RMM（0.7867）在 WOSAC 排行榜上取得 SOTA，Interactive 指标（0.8129）同样为最佳。值得注意的是，Interactive 指标的提升尤为关键——它直接衡量多智能体交互行为的真实度，这正是开环模仿学习最容易产生因果混淆的维度。闭环 RL 微调通过直接优化仿真轨迹的分布匹配，有效纠正了开环训练中累积的交互偏差。

**定性证据（Figure 3a）** 进一步佐证了这一点：在复杂交叉路口场景中，基线模型 SMART-tiny 生成了偏离道路的轨迹（红色轨迹）并与横向车流发生碰撞，而 RLFTSim 则生成了遵守交通规则的合理车道保持行为。这表明 MLOO 驱动的 RL 微调不仅提升了统计指标，更在关键安全行为上产生了质变。

---

### 奖励函数消融：MLOO 的核心作用

**Table 2** 在全量 WOMD 验证集上对奖励函数设计进行了系统性消融。核心发现是：**RMM^MLOO 作为奖励信号在所有变体中取得最高 RMM（0.7830）**，显著优于其他奖励设计。

消融对比的奖励函数包括：
- **minADE**：最小平均位移误差，模仿学习中常用的开环指标
- **RMM^RLOO**：基于单条回滚的留一法 RMM 估计（Reward Leave-One-Out）
- **Heuristic**：手工设计的启发式奖励（如碰撞惩罚、速度偏差等，详见 Table S.3）
- **RMM^MLOO**：本文提出的 Meta-metric Leave-One-Out

| 奖励函数 | RMM↑ | Kinematic↑ | Interactive↑ |
|----------|------|------------|--------------|
| minADE | 0.7786 | 0.4851 | 0.8052 |
| RMM^RLOO | 0.7806 | 0.4868 | 0.8083 |
| Heuristic | 0.7811 | 0.4875 | 0.8086 |
| **RMM^MLOO** | **0.7830** | **0.4891** | **0.8106** |

**Table S4** 的配对 t 检验确认了 RMM^MLOO 相对于其他奖励函数的优势具有统计显著性。minADE 表现最差，直接验证了本文的核心论断：**开环指标无法捕捉闭环部署中的分布偏移**，将其作为 RL 奖励信号会导致优化目标与真实仿真质量之间的错位。

RMM^RLOO 虽然也使用了 RMM 作为基础，但其方差远高于 MLOO。**Figure 2** 的实证方差分析显示：MLOO 的奖励方差随回滚数 $N$ 按 $1/N^2$ 快速下降，而 RLOO 的方差基本保持不变。这与 Proposition 3 的理论分析完全一致——MLOO 通过对称的留一法结构实现了方差的二次缩减，使得基于 RL 的细粒度真实感对齐在样本效率上成为可能。

启发式奖励（Heuristic）虽然取得了次优结果，但其设计依赖于大量领域知识（碰撞惩罚、离路惩罚、速度分布匹配等，见 Table S.3），泛化能力受限。MLOO 的优势在于无需手工设计，直接以 RMM 本身作为优化目标，实现了端到端的真实感对齐。

---

### 可控性蒸馏实验

**Table 3** 分析了目标表示方式和奖励准则对可控性与真实感的影响。实验在全量 WOMD 验证集上进行，评估指标包括 RMM（真实感）和 Miss Rate / Arrival Rate（可控性）。

| 目标表示 | 奖励准则 | RMM↑ | Miss Rate↓ | Arrival Rate↑ |
|----------|---------|------|-----------|---------------|
| Concatenation (cat) | Soft | 0.7820 | 9.180% | 0.383 |
| Concatenation (cat) | Hard | 0.7818 | 12.500% | **0.422** |
| Indication (ind) | Soft | **0.7823** | 9.180% | 0.380 |
| Indication (ind) | Hard | 0.7819 | 12.800% | 0.420 |

**目标表示**：位置编码指示（indication）比直接拼接（concatenation）保持了略高的真实感（RMM 0.7823 vs. 0.7820），说明将目标信息作为独立的指示信号注入，比直接拼接到智能体状态中对原始行为分布的扰动更小。

**奖励准则**：软目标奖励（soft，基于到目标点距离的连续奖励）给出最佳通过率（Miss Rate 9.180%），而硬目标奖励（hard，到达目标点才给正奖励）给出最佳到达率（Arrival Rate 0.422）。这反映了真实感与可控性之间的内在权衡：软奖励允许模型在保持自然行为的前提下接近目标，适合需要高通过率的场景；硬奖励则强制模型必须到达目标，适合对到达精度要求更高的应用。

**Table S5** 和 **Figure S.1** 进一步验证了目标条件微调（GCFT）结合事后经验回放（HER）在非真实轨迹的机动控制上大幅优于基线。在目标全部设为替代机动（alternative maneuvers，即与真实轨迹不同的机动）的严苛条件下，GCFT 模型仍能保持较高的到达率和较低的错误率，证明了可控性蒸馏的有效性。

---

### 模型无关性与扩展性

**Table S6** 的模型无关性消融实验表明，RLFTSim 的方法不依赖于特定的基础模型架构。将 RLFTSim 应用于 **TrafficBots V1.5**（一种不同的仿真架构）后，RMM 从 0.7174 提升至 0.7231（+0.0057），验证了 MLOO 驱动的闭环 RL 微调框架的通用性。

**Table S2** 的扩展基准测试进一步展示了 RLFTSim 的现实性增强能力。从较弱的预训练起点（仅 1 epoch 预训练，RMM 0.7507）开始微调，RLFTSim 将 RMM 提升至 0.7642（+1.8%），增幅远超 CAT-K 等基于启发式搜索的闭环微调基线。这表明 RLFTSim 对于预训练质量较低的模型具有更强的补偿能力。

---

### 失败模式与局限性

尽管 RLFTSim 取得了显著的性能提升，实验中也暴露出几个值得关注的局限性：

1. **RMM 指标的饱和效应**：当前最优 RMM（0.7867）已接近 WOSAC 的 oracle 上限（约 0.79），进一步改进的空间被压缩。RMM 作为分布匹配指标，可能无法捕捉细粒度的安全约束或长尾交互模式。需要更精细的现实性评估指标来区分高质量仿真之间的细微差异。

2. **绝对到达率仍有提升空间**：目标条件微调虽然显著降低了 Miss Rate，但 Arrival Rate 的绝对值（最高 0.422）仍不完美。在硬目标奖励设置下，仍有约 58% 的回滚未能精确到达目标点，说明当前的目标条件机制在复杂场景下的引导能力有限。

3. **高动态场景的响应能力**：基于离散令牌的表示（discrete token-based representation）在高动态场景下可能降低模型的响应能力。当场景中智能体数量多、交互频繁时，离散化的动作空间可能无法捕捉连续、精细的避让行为。

4. **MLOO 的计算开销**：MLOO 需要为每个场景生成 $N$ 条回滚并计算 $N$ 次留一法 RMM，计算开销高于简单的启发式奖励。虽然 $N$ 通常取 32（与 WOSAC 协议一致），但在更大规模部署或实时应用中可能成为瓶颈。

---

### 关键图表结论总结

- **Table 1**：RLFTSim 在 WOSAC 排行榜上取得 RMM 0.7867 的 SOTA 真实感，Interactive 指标 0.8129 为最佳，证明闭环 RL 微调有效纠正了开环模仿学习的交互偏差。
- **Table 2 + Figure 2**：MLOO 奖励在所有消融中取得最高 RMM，其方差按 $1/N^2$ 下降（vs. RLOO 方差不变），是 RL 微调成功的关键使能技术。
- **Table 3**：位置编码指示 + 软目标奖励在保持真实感的同时实现最佳通过率（Miss Rate 9.180%），硬目标奖励则给出最佳到达率，揭示真实感与可控性的权衡。
- **Figure 3**：定性对比显示 RLFTSim 在复杂交叉路口场景中消除了基线模型的不合理离路和碰撞行为，生成符合交通规则的合理轨迹。
- **Table S6**：RLFTSim 可提升不同基础模型（TrafficBots V1.5）的真实感，证明方法具有模型无关性。

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/002_Table_1.jpg]]
*Table 1: Traffic simulation benchmarking results. Results are based on WOSAC leaderboard1 evaluation on the private test split. We also present the results for our reference model (SMART). (↑) indicates that larger values are better. Bold and underline indicate the best and second best values, respectively2. † indicates our retrained version of the reference model*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/003_Table_2.jpg]]
*Table 2: Ablation study on the reward function on the full validation set. Standard errors are shown in parentheses*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/004_Table_3.jpg]]
*Table 3: Effect of goal representation and reward criterion on controllability and realism, evaluated on the full WOMD validation split. Bold and underline indicate the best and second best values, respectively. Standard errors are shown in parentheses*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative Evidence of RLFTSim Effectiveness. (a) Realism Enhancement: Comparison of baseline SMART-tiny (a-2) vs. RLFTSim (a-3) on a challenging intersection scenario. The baseline model generates unrealistic off-road behavior (red trajectory) and a collision with cross-traffic, while RLFTSim produces realistic lane-following behavior that respects traffic rules. (b) Controllability Distillation: Two sets of realistic simulation rollouts of the fine-tuned model are shown for a fixed seed scenario, conditioned on different goal points (magenta points): a U-turn goal (top row) and a left-turn goal (bottom row). In GCFT rollouts, the ego vehicle, depicted with an orange border, achieves the...*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/014_Table_S.6.jpg]]
*Table S.6: Model agnosticism ablation study. Experiments are done using 20% of the WOMD validation split*

### 补充图表

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/007_Table_S.1.jpg]]
*Table S.1: Hyperparameter sweep ranges explored for RLFTSim. Final values are highlighted in bold*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/008_Table_S.2.jpg]]
*Table S.2: Extended Benchmarking. Top: Performance scaling comparison of our RLFTSim vs. CAT-K with the number of fine-tuning epochs. † indicates a weaker reference model with only 1 epoch of pre-training. Middle: Stronger realism enhancement with a weaker reference model. Bottom: Max realism metametric for the ground truth trajectories*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/009_Table_S.4.jpg]]
*Table S.4: Paired t-test on per-scenario RMM scores from the full validation set (Tab. 2) at significance threshold*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/010_Table_S.3.jpg]]
*Table S.3: Heuristic rewards for the realism meta-metric. All metrics are evaluated on the ego vehicle and agents tagged as tracks to predict (up to 9 agents). (↑) indicates that larger values are better, and (↓) indicates smaller values are better. Miss rate is computed with the passing goal criterion. Bold and underline indicate the best and second best values, respectively*

![[assets/figures/papers/paper_list_l2720_https_arxiv_org_abs_2605_19033/figures/011_Figure_S.1.jpg]]
*Figure S.1: Controllability benchmark performance across various experimental conditions: (a) all goals are set to ground-truth maneuvers, (b) goals are randomly sampled from all maneuvers, (c) goals are exclusively sampled from alternative maneuvers, and (d) simulation controllability with kinematic perturbations. GCFT models consistently outperform the baseline across all conditions, demonstrating effective controllability distillation*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

RLFTSim 的核心贡献在于将多智能体交通仿真从**开环模仿学习**范式推进到**闭环在线强化学习微调**范式，其方法定位可通过与以下基线的对比来理解。

**与预训练基础模型的关系。** RLFTSim 并非从头训练一个仿真器，而是对一个已通过行为克隆（behavioral cloning）预训练的模型进行后训练（post-training）。论文使用 **SMART-tiny** 作为主要参考模型，并在模型无关性消融中验证了 **TrafficBots V1.5** 也可作为替代基础模型（Table S6：RMM 从 0.7174 提升至 0.7231）。这意味着 RLFTSim 的方法贡献独立于特定的骨干架构，其核心价值在于**训练范式**和**奖励设计**的改进。

**与开环模仿学习的本质差异。** 开环模仿学习（行为克隆）在训练时使用真实历史轨迹作为输入，但在闭环部署时，模型自身的预测误差会逐步累积，导致输入分布偏离训练分布（分布偏移，distribution shift），进而引发因果混淆和仿真失真。RLFTSim 通过在线策略梯度（REINFORCE）在闭环环境中直接优化真实感元指标 RMM，使模型学会在自身误差存在的情况下仍能生成真实轨迹。这一转变解决了开环范式无法触及的**误差累积-分布偏移**恶性循环。

**与启发式闭环微调基线 CAT-K 的对比。** **CAT-K** 是一种基于启发式搜索的闭环微调方法。Extended Benchmarking（Table S2）显示，RLFTSim 在微调 epoch 数增加时表现出更强的性能缩放能力：从较弱预训练起点（1 epoch，RMM 0.7507）出发，RLFTSim 将 RMM 提升至 0.7642（+1.8%），而 CAT-K 在相同条件下的增益幅度较小。这表明基于 RL 的端到端优化比启发式搜索能更有效地利用闭环反馈信号。

**与直接使用 RMM 作为 RL 奖励的对比。** 直接将 RMM 作为 RL 奖励面临两个根本障碍：信号稀疏（一个场景仅有一个标量 RMM）和方差过大（不同回滚间的 RMM 波动掩盖了单个回滚的贡献）。RLFTSim 的核心洞察在于通过 **Meta-metric Leave-One-Out（MLOO）** 将 RMM 转化为每个回滚（rollout）的相对贡献信号，实现了**无偏梯度估计**（Proposition 1）和**方差按 1/N² 快速下降**（Proposition 3，Figure 2 实证验证）。消融实验（Table 2）证实，RMM_MLOO 奖励在所有变体中取得最高 RMM（0.7830），显著优于 minADE、RMM_RLOO 和各类启发式奖励（paired t-test 显著性验证见 Table S4）。

### 2. 方法谱系中的位置

RLFTSim 在交通仿真研究谱系中占据了一个独特位置，其方法组件可追溯至多个研究脉络：

**闭环强化学习用于序列生成。** RLFTSim 将多智能体轨迹生成建模为上下文马尔可夫决策过程（Contextual MDP），使用 REINFORCE 策略梯度与 KL 散度正则化进行优化。这一框架与 RLHF（Reinforcement Learning from Human Feedback）中使用的 PPO 微调在精神上相似，但 RLFTSim 的奖励信号来自分布匹配指标而非人类偏好标注，且使用了更轻量的 REINFORCE 而非需要价值函数的 Actor-Critic 方法。KL 正则化（Appendix B）的作用是防止微调策略偏离预训练模型过远，这与 RLHF 中的 KL 惩罚具有相同的动机。

**分布匹配作为奖励信号。** RMM 本质上是一种基于离散特征空间的分布匹配指标——它比较仿真轨迹与真实轨迹在运动学、交互、地图合规等多个特征维度上的离散分布相似度。这种将分布差异作为优化目标的做法与生成对抗网络（GAN）中的判别器损失和扩散模型中的得分匹配有概念上的联系，但 RLFTSim 使用的是固定的、不可微的元指标而非可学习的判别器。MLOO 的创新在于将这种“场景级”分布匹配指标分解为“回滚级”贡献信号，使得策略梯度优化成为可能。

**目标条件策略与事后经验回放。** 可控性蒸馏部分直接借鉴了 **Hindsight Experience Replay（HER）**（Andrychowicz et al., NeurIPS 2017）的思想：利用最佳回滚的终端状态作为替代目标，将“失败”的尝试转化为“成功”的训练样本。RLFTSim 将 HER 应用于交通仿真的目标条件微调（GCFT），通过目标表示（位置编码指示 vs. 拼接）和软/硬目标奖励的设计（Table 3），在保持真实感的前提下赋予仿真器明确的机动控制能力。

### 3. 适用边界与局限

RLFTSim 的方法边界和局限性在论文中有明确讨论或可从实验设计中推断：

**RMM 指标的饱和效应。** 当前 RMM 指标已接近 oracle 上限（Table 1 中 RLFTSim 的 RMM 为 0.7867，与理论最优的差距在缩小），这可能掩盖真实仿真质量的进一步改进。论文明确指出“需要更精细的现实性评估指标”。这意味着 RLFTSim 的优化目标本身可能成为性能提升的瓶颈——当 RMM 饱和时，即使仿真质量有实际改进，也无法通过该指标反映。

**离散令牌表示的响应能力局限。** 论文承认“基于离散令牌的表示在高动态场景下可能降低响应能力”。这是因为 RLFTSim 的基础模型（如 SMART-tiny）使用离散运动令牌来表示智能体行为，在高交互密度或快速变化的场景中，离散化的粒度可能不足以捕捉精细的连续运动变化。

**目标条件微调的到达率瓶颈。** 尽管 GCFT 显著提升了目标通过率（Table S5：软目标奖励给出 9.180% Miss Rate），但绝对到达率仍不完美。论文指出“需要更强的目标条件机制”，暗示当前的目标表示和奖励设计在精确控制方面仍有提升空间。

**计算开销与规模限制。** MLOO 依赖生成多个回滚（论文中 N=32）来计算每个回滚的奖励，这比简单的启发式奖励（如 minADE）计算开销更高。论文将此列为局限性之一，指出“可能限制更大规模的应用”。

**场景覆盖的潜在盲区。** 论文未明确讨论 RLFTSim 在长尾场景（如罕见交互模式、极端天气条件）上的表现。当前对真实感的优化主要基于 WOMD 数据集的分布匹配，是否遗漏了重要的长尾行为或交互模式是一个开放问题。

### 4. 开放问题与后续方向

从论文的讨论和方法边界出发，可以识别以下开放问题：

**更全面的仿真对齐目标。** 如何将 RMM 或类似的分布匹配指标与更细粒度的安全/合规约束（如碰撞率、交通规则遵守率）结合，实现更全面的仿真对齐？当前 RLFTSim 仅优化 RMM，而 RMM 是多个子指标的加权组合，未来可能需要显式的多目标优化或约束满足框架。

**更灵活的可控性接口。** 当前的目标条件微调使用坐标点作为目标表示。能否设计更灵活的目标表示形式（如自然语言指令、参考轨迹草图、行为语义标签），以进一步提升可控性的多样性和易用性？这将使仿真器从“点到点”控制扩展到“语义级”控制。

**更高效的在线奖励估计。** 在算力受限的情况下，是否存在比 MLOO 更高效的在线奖励估计方法？MLOO 的方差优势依赖于回滚数量 N，但计算成本与 N 线性增长。可能的改进方向包括：使用控制变量（control variates）进一步降方差、设计自适应回滚数量策略、或利用值函数近似来减少对大量回滚的依赖。

**闭环微调的理论理解。** 论文通过实验证明了闭环 RL 微调优于开环模仿学习，但对“为什么闭环微调能克服分布偏移”缺乏更深入的理论分析。未来工作可以探索闭环微调的收敛性质、微调对模型泛化能力的影响，以及微调过程中灾难性遗忘的机制与缓解策略。

**跨仿真器的迁移能力。** RLFTSim 在 SMART-tiny 和 TrafficBots V1.5 上验证了模型无关性，但其是否适用于其他类型的仿真器（如基于物理的仿真器、不同传感器配置的仿真器）仍是一个开放问题。特别是当基础模型使用连续动作空间而非离散令牌时，MLOO 和 GCFT 的适用性需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/RLFTSim_Realistic_and_Controllable_Multi_Agent_Traffic_Simulation_via_Reinforcement_Learning_Fine_Tuning.pdf]]
