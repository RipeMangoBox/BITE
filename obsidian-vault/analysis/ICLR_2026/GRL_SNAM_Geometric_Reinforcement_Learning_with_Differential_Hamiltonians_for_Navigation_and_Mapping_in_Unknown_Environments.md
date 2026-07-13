---
title: "GRL-SNAM: Geometric Reinforcement Learning with Differential Hamiltonians for Navigation and Mapping in Unknown Environments"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GRL_SNAM_Geometric_Reinforcement_Learning_with_Differential_Hamiltonians_for_Navigation_and_Mapping_in_Unknown_Environments.pdf
project_link: null
code_link: null
openreview_forum_id: KcC5mwfGf0
aliases:
- GS
- GRL-SNAM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将导航问题重构为在哈密顿量流形上的能量优化：通过离线学习的哈密顿量提供结构化参考动力学，在线阶段式更新环境驱动的能量权重，从而将感知、规划和变形策略统一于梯度诱导的局部控制。"
primary_logic: "哈密顿量结构作为导航的强归纳偏置：能量守恒稳定长期展开，辛几何自然分离快慢动态，障碍函数直接嵌入势能消除脆弱奖励塑形，使得导航成为在学到的局部能量景观上的梯度流。"
claims:
- "GRL-SNAM使用CBF级路径质量（SPL 0.95）而仅消耗与势场法相近的最小建图预算（10.7%）。"
- "GRL-SNAM在感知到新障碍物时动态修改整个局部能量景观，而不只是调整动作，体现深层哈密顿量适应。"
- "独立得分函数架构通过共享约束集实现并行训练，且独立训练样本复杂度为各策略维度之和的线性界。"
- "在点智能体地下城导航任务中，阶段式哈密顿量监督相比端到端RL（PPO/TRPO/SAC）将成功率从约7%大幅提升至87.5%。"
---

# GRL-SNAM: Geometric Reinforcement Learning with Differential Hamiltonians for Navigation and Mapping in Unknown Environments

> [!tip] 核心洞察
> 哈密顿量结构作为导航的强归纳偏置：能量守恒稳定长期展开，辛几何自然分离快慢动态，障碍函数直接嵌入势能消除脆弱奖励塑形，使得导航成为在学到的局部能量景观上的梯度流。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GRL-SNAM: 基于微分哈密顿量的几何强化学习用于未知环境导航与建图 |
| 英文题名 | GRL-SNAM: Geometric Reinforcement Learning with Differential Hamiltonians for Navigation and Mapping in Unknown Environments |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KcC5mwfGf0) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | GRL-SNAM |
| Dataset | 2D deformable ring navigation (cluttered environments), 2D deformable ring navigation, Point-agent dungeon navigation (short-rollout) |

> [!tip] 效果简介
> - 2D deformable ring navigation (cluttered environments) 上，Success-weighted Path Length (SPL) 为 0.95，对比 0.77 (PF)，变化 +0.18。
> - 2D deformable ring navigation 上，Mapping Ratio (%) 为 10.7，对比 11.2 (CBF)，变化 -0.5。
> - Point-agent dungeon navigation (short-rollout) 上，Success (%) 为 87.5，对比 26.1 (PPO)，变化 +61.4。

## 概要

未知环境中的自主导航与建图（SNAM）要求智能体在缺乏全局地图的条件下，同时完成感知、规划与运动控制。现有强化学习（RL）方法缺乏对导航任务中几何和物理结构的显式编码，导致在未建模动态和分布变化下不稳定、泛化能力差；传统SLAM与规划方法则难以在最小探索预算下实现高质量路径。

GRL-SNAM 将导航问题重构为在**哈密顿量流形上的能量优化**：通过离线学习获得结构化的参考哈密顿量，在线阶段式更新环境驱动的能量权重，从而将感知、规划和变形策略统一于梯度诱导的局部控制。其核心洞察在于，哈密顿量结构为导航提供了强归纳偏置——能量守恒稳定长期展开，辛几何自然分离快慢动态，而障碍函数直接嵌入势能则消除了脆弱的奖励塑形。

方法层面，GRL-SNAM 在三个关键维度上区别于现有范式：

- **学习范式**：通过微分策略优化（DPO）直接学习哈密顿量能量景观，其梯度产生控制动作，无需值函数或显式规划树，从根本上区别于以贝尔曼自助为核心的深度RL方法。
- **安全集成**：将障碍势垒作为可加至哈密顿量势能的天然项，通过自适应对偶权重实现安全与任务目标的统一梯度调节，而非依赖外部CBF滤波器或奖励塑形。
- **多时间尺度协调**：传感器、路径和形状三个策略作为嵌套哈密顿量子系统，运行在不同自然频率上，利用拟静态近似实现无耦合的稳定层级协调。

实验表明，GRL-SNAM 在2D可变形环形机器人导航任务中达到与CBF相近的路径效率（SPL 0.95），而仅消耗与势场法相当的最小建图预算（10.7%）；在点智能体地下城导航任务中，阶段式哈密顿量监督将成功率从端到端RL（PPO/TRPO/SAC）的约7%大幅提升至87.5%。在分布外测试环境下的定性轨迹对比显示，GRL-SNAM 产生的路径平滑、高效且保持安全空隙，而深度RL基线通常停滞、碰撞或偏离目标。

当前方法验证限于二维超弹性环形机器人和点智能体导航，对三维环境、真实传感器噪声及更复杂动力学模型的鲁棒性仍有待评估；多策略、多阶段部署流程的工程复杂度也是实际集成的潜在障碍。



### 导航问题的根本挑战

在未知环境中进行自主导航与建图（SLAM）是机器人学的核心问题。当机器人本体具有可变形结构时，问题难度急剧上升：智能体不仅需要规划无碰撞路径，还必须同时决定何时以及如何改变自身形状以穿越狭窄缝隙。这一过程要求感知、规划和控制三个时间尺度紧密协调——传感器在秒级更新环境信息，路径规划在亚秒级生成航点，而形状变形则需要在毫秒级积分步长内连续调整。

传统方法将这一复合问题拆解为独立的模块：SLAM管线负责建图与定位，全局规划器（如A*）在已知地图上搜索路径，局部反应式控制器（如动态窗口法DWA、势场法PF）处理即时避障，而控制屏障函数（CBF）则作为安全滤波器叠加在控制器之上。这种拆分虽然工程上可行，却带来了根本性的结构缺陷：**各模块的目标函数和优化空间相互独立，缺乏统一的物理基础来协调感知探索、路径效率与形状适应之间的权衡**。

### 强化学习方法的系统性不足

深度强化学习（RL）试图通过端到端学习来绕过模块拆分问题。然而，现有RL方法在导航任务中暴露出三个层面的结构性弱点。

**第一，训练信号脆弱。** PPO（Schulman et al., 2017）、TRPO、SAC（Haarnoja et al., 2018）等方法以值函数的贝尔曼自举为核心，通过最小化时序差分误差来学习策略。这种信号在长周期导航中极易因稀疏奖励和分布漂移而崩溃——实验表明，在点智能体地下城导航任务中，端到端训练的PPO/TRPO/SAC成功率仅约7%（Table 8），即便在短回合设定下也仅达到18%–26%（Table 3）。

**第二，几何与物理结构缺失。** 标准RL策略是黑箱映射，缺乏对导航任务中守恒律、几何约束和快慢动态分离的显式编码。当环境分布发生变化时，策略无法利用物理结构进行泛化，表现为在分布外测试环境中停滞、碰撞或大幅偏离目标（Figure 8）。

**第三，安全集成方式间接。** 现有方法要么通过外部CBF滤波器在动作空间进行事后修正，要么通过奖励塑形将碰撞惩罚作为标量信号加入值函数。这两种方式都无法在策略的深层表征中建立障碍物与安全动作之间的因果联系，导致安全约束容易被其他目标淹没。

### 核心动机：将物理结构注入学习

本工作的核心动机是回答一个根本问题：**能否将导航问题重新表述为在物理意义明确的能量景观上的梯度流，从而让学习算法天然继承哈密顿力学中的结构优势？**

这一思路的出发点是观察到：导航行为本质上可以被描述为多种力场的组合——目标产生吸引力，障碍物产生排斥力，变形需求产生弹性恢复力。如果将这些力统一编码为一个标量能量函数（哈密顿量）的梯度，那么：

- **能量守恒**为长期展开提供稳定性，避免值函数估计的累积误差；
- **辛几何结构**自然分离位置和动量的快慢动态，为多时间尺度协调提供数学基础；
- **障碍物势垒**可以作为势能的天然可加项直接嵌入能量景观，消除脆弱的奖励塑形。

基于这一动机，GRL-SNAM将导航重构为**学习一个结构化的哈密顿能量景观**，其梯度直接产生局部控制动作。离线阶段通过微分策略优化（DPO）从轨迹反馈中学习参考哈密顿量，在线阶段则通过阶段式更新环境驱动的能量权重，将感知、规划和变形策略统一于梯度诱导的局部控制。这一框架不再需要值函数、显式规划树或外部安全滤波器——安全与任务目标在统一的能量景观中通过自适应对偶权重实现协调。



## 核心方法与创新机理

GRL-SNAM 的核心创新在于将导航问题从传统的“值函数优化”或“势场设计”范式，重构为**在哈密顿量流形上的结构化能量优化**。这一转变带来了三个关键的 changed slots，从根本上区别于现有方法。

### 1. 学习范式与训练信号：从贝尔曼自助到微分策略优化

**Baseline 现状**：深度 RL 方法（PPO、TRPO、SAC）以值函数的贝尔曼自助为核心，通过最小化时序差分误差学习策略；经典方法（PF、A\*）则依赖手工设计的势场或代价函数。这些方法均未显式编码导航任务的几何与物理结构，导致在未建模动态和分布变化下不稳定、泛化能力差。

**GRL-SNAM 的变革**：通过**微分策略优化（Differential Policy Optimization, DPO）**直接学习哈密顿量能量景观 $h^{\theta}$，其梯度 $\nabla_q h^{\theta}$ 直接产生控制动作，无需值函数或显式规划树（Section 1.1, 1.4, Theorem 3.2-3.4）。核心公式为：

$$H(\boldsymbol{q}, \boldsymbol{p}; \mathcal{E}) = \frac{1}{2} \boldsymbol{p}^{\top} (\boldsymbol{A}(\boldsymbol{q}) \Phi^{-1} \boldsymbol{A}(\boldsymbol{q})^{\top}) \boldsymbol{p} + \boldsymbol{p}^{\top} \boldsymbol{f}(\boldsymbol{q}) + \mathcal{R}(\boldsymbol{q}; \mathcal{E})$$

其中动能项由控制惩罚的 Legendre-Fenchel 共轭自然导出，势能 $\mathcal{R}(\boldsymbol{q}; \mathcal{E})$ 由环境条件化。这一设计将控制问题转化为能量景观上的梯度流，使得哈密顿量结构本身成为导航的强归纳偏置：能量守恒稳定长期展开，辛几何自然分离快慢动态。

**决定性证据**：在点智能体地下城导航任务中，阶段式哈密顿量监督相比端到端 RL（PPO/TRPO/SAC）将成功率从约 7% 大幅提升至 **87.5%**（Table 3, Table 8），且仅需 500k 梯度步，远低于 RL 基线的 3.2-4.1M 步。

### 2. 安全集成方式：从外部约束到内嵌势能

**Baseline 现状**：现有方法通过外部 CBF 滤波器、奖励塑形或碰撞惩罚等间接方式处理安全约束。这些机制与策略学习解耦，容易产生冲突或脆弱性——奖励塑形需要精细调参，CBF 滤波器可能过度保守。

**GRL-SNAM 的变革**：将障碍势垒作为**可加至哈密顿量势能的天然项**，通过自适应对偶权重实现安全与任务目标的统一梯度调节（Section 3.2 Eq.4, Section 4.1）。总势能分解为：

$$\mathcal{R}(q; \omega, \eta_{\xi}(\mathcal{E})) = E_{\mathrm{sensor}} + \beta(\mathcal{E}) E_{\mathrm{goal}} + \lambda(\mathcal{E}) E_{\mathrm{obj}} + \sum_{i \in \mathcal{C}_t} \alpha_i b(d_i)$$

其中 $\sum_{i \in \mathcal{C}_t} \alpha_i b(d_i)$ 是主动障碍物屏障项，权重 $\alpha_i$、$\beta$、$\gamma$ 由元策略 $g_{\xi}$ 根据环境动态调整。当新障碍物被感知时，GRL-SNAM **修改整个局部能量景观**，而不仅仅是调整动作（Figure 10, Section 4.1）——系数 $(\beta, \gamma, \bar{\alpha})$ 动态演化，重新定义约化哈密顿量本身，而非在策略输出上叠加外部滤波器。

**决定性证据**：GRL-SNAM 在杂乱环境中以最小建图预算（**10.7%**）达到 CBF 级路径质量（SPL **0.95**），且空隙始终高于碰撞阈值（Table 5, Figure 10）。相比之下，深度 RL 基线的 SPL 仅为 0.60-0.77，且绕路比更大、空隙更小（Table 1）。

### 3. 多时间尺度协调：从单一时钟到嵌套哈密顿量子系统

**Baseline 现状**：传统方法采用手动设计的层级或单一时钟控制，难以有效分离感知、规划和控制的不同时间尺度需求。端到端 RL 将所有决策压缩到同一频率，导致样本效率低下和耦合不稳定。

**GRL-SNAM 的变革**：将导航分解为三个**独立的得分函数模块**——传感器策略 $\pi_y$、帧策略 $\pi_f$、形状策略 $\pi_o$——它们分别运行在不同的自然频率上，利用拟静态近似实现无耦合的稳定层级协调（Section 3.4, Figure 2, Definition 3.1）：

- **传感器策略**（低频，每阶段一次）：建立环境约束集 $\mathcal{C}_t$
- **帧策略**（中频，阶段内多次）：计算无碰撞路径点
- **形状策略**（高频，每积分步）：连续适应变形

每个子模块拥有独立的局部哈密顿量：

$$H_k(q_k, p_k; \xi, \mathcal{E}) = \frac{1}{2} p_k^{\top} M_k^{-1} p_k + \mathcal{R}_k(q_k; \mathcal{E})$$

参数集满足互斥性 $\Theta_i \cap \Theta_j = \emptyset$，确保独立训练。**Theorem 3.4** 证明，独立训练的样本复杂度为各策略维度之和的线性界 $N_{\text{total}} = \sum_{k} O(\epsilon_k^{-(2d_k+4)})$，而非联合维度的指数级，这是实现高效训练的理论保障。

**决定性证据**：消融实验（Table 6）表明，摩擦损失（$w_{\text{fric}}$）对稳定性至关重要——移除后导致欠阻尼振荡和障碍物穿透；多起点损失（$w_{\text{multi}}$）防止过度保守。两者组合获得最佳整体性能，验证了层级协调中阻尼与鲁棒性的互补作用。

### 与基线方法的范式级差异

Table 4 的范式级对比揭示了 GRL-SNAM 的独特地位：它是唯一在能量守恒、几何结构保持、约束集成、在线适应、多尺度协调等十个维度上均提供全面支持（✓）的框架。深度 RL 方法缺乏几何结构和约束集成，经典规划方法不支持在线适应和多尺度协调，CBF 方法则缺乏学习能力和变形支持。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/001_Figure_1.jpg]]
*Figure 1: Independent score function architecture and query–response interface. The Navigator $g _ { \xi }$ issues queries containing local Hamiltonians $H _ { k }$ , initial states $z _ { k , 0 }$ . , and time horizons $\bar { T } _ { k }$ to each policy $\pi _ { k }$ ( k $\in \{$ y , f , o $\}$ ) . Each policy computes score functions $s _ { k } ^ { \theta _ { k } }$ via energy gradients from learned Hamiltonians $h _ { k } ^ { \theta _ { k } }$ , backed by spatial indices $\scriptstyle { S _ { k } }$ for efficient neighbor queries. Policies return standardized responses $\mathsf { R } _ { k }$ containing state trajectories, score sequences, and QoIs. The Navigator aggregates these to update the surrogate Hamiltonian an...

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/002_Figure_2.jpg]]
*Figure 2: Temporal hierarchy. Sensor policy operates at low frequency (once per stage), establishing environmental constraints $\mathcal { C } _ { t }$ . . Path policy operates at medium frequency within each stage, computing waypoints W. Shape policy operates at high frequency, continuously adapting at each integration step. This creates a natural hierarchy where slow sensor updates provide stable constraints for faster path and shape adaptations*

GRL-SNAM 将未知环境下的导航与建图问题重构为**在哈密顿量流形上的能量优化**。其核心对象是一个定义在相空间上的代理哈密顿量（surrogate Hamiltonian），其梯度直接产生局部控制动作，从而将感知、规划与变形策略统一于梯度诱导的局部控制之中。整个框架由**离线训练**和**在线阶段式适应**两个阶段构成，如图1所示。

### 架构总览

系统由四个核心模块组成，形成清晰的查询-响应接口：

1. **导航器（Navigator）** $g_\xi$：元控制器，负责向三个子策略发出查询，并将响应聚合为环境条件化的能量权重、摩擦系数和端口输入，最终组装代理哈密顿量并执行在线雅可比校正。

2. **传感器策略（Sensor Policy）** $\pi_y$：从局部观测生成障碍物安全场、自由空间场和密度场，建立当前阶段的约束集 $\mathcal{C}_t$。

3. **帧策略（Frame Policy）** $\pi_f$：在约束集内进行无碰撞路径规划，平衡目标吸引力与障碍物排斥力，计算局部路径点。

4. **形状策略（Shape Policy）** $\pi_o$：控制机器人的变形，通过平滑性和拉伸能量约束产生适应缝隙和障碍物的形状变化。

### 独立得分函数架构

三个子策略被定义为**独立的得分函数**（independent score functions），每个得分函数基于学习到的局部哈密顿量的梯度：

$$s_k^{\theta_k}(z_k, \mathcal{E}, t) = S_k^{\theta_k}\bigl(\nabla_{z_k} h_k^{\theta_k}(z_k, \mathcal{E}, t)\bigr)$$

其中 $k \in \{y, f, o\}$ 分别对应传感器、帧和形状策略。各策略的参数集满足**互斥性**（$\Theta_i \cap \Theta_j = \emptyset$），确保独立性并支持并行训练。这一设计使得总样本复杂度为各策略维度之和的线性界，而非联合维度的指数界：

$$N_{total} = \sum_{k \in \{y, f, o\}} O(\epsilon_k^{-(2 d_k + 4)})$$

### 时间层级与嵌套拟静态近似

三个策略运行在不同的自然频率上，形成嵌套的时间层级（Figure 2）：
- **传感器策略**以最低频率运行（每个阶段一次），建立稳定的环境约束；
- **帧策略**以中等频率运行，在阶段内计算路径点；
- **形状策略**以最高频率运行，在每个积分步长内连续适应。

这种时间分离使得**嵌套拟静态近似**成为可能：最快的变形动力学在每个帧更新内达到平衡，中等速度的路径动力学在每个传感器更新内达到平衡，从而在无需显式耦合的情况下实现稳定的层级协调。

### 在线适应机制

在线阶段中，导航器将离线学习到的参考哈密顿量与上下文相关的修正项相加：

$$h^{\mathrm{adapted}} = h^{\mathrm{ref}} + \Delta h^{\mathrm{context}}$$

总势能由四项线性组合而成，权重由元策略根据环境动态调整：

$$\mathcal{R}(q; \omega, \eta_{\xi}(\mathcal{E})) = E_{\mathrm{sensor}} + \beta(\mathcal{E}) E_{\mathrm{goal}} + \lambda(\mathcal{E}) E_{\mathrm{obj}} + \sum_{i \in \mathcal{C}_t} \alpha_i b(d_i)$$

其中 $\beta$ 控制目标吸引力，$\lambda$ 控制变形能量，$\alpha_i$ 控制各障碍物屏障强度。当感知到新障碍物时，GRL-SNAM 不是仅调整动作，而是**动态修改整个局部能量景观**——系数 $(\beta, \gamma, \alpha)$ 的演化实质上重新定义了代理哈密顿量本身（Figure 10），体现了深层哈密顿量适应的核心优势。

### 范式级能力对比

Table 4 从十个维度对比了 GRL-SNAM 与其他学习框架的能力覆盖。GRL-SNAM 是唯一在所有维度上获得全面支持（✓）的框架，涵盖能量守恒、几何结构保持、约束集成、在线适应、多尺度协调等关键能力。相比之下，标准深度 RL 方法（PPO/TRPO/SAC）在能量守恒和几何结构方面完全缺失支持，传统规划方法（A*）则缺乏在线适应和多尺度协调能力。



GRL-SNAM 的核心架构由三个独立得分函数模块和一个元控制器（Navigator）构成，其数学基础是将导航问题嵌入到哈密顿量流形上的能量优化。

### 导航的哈密顿量形式化

导航被重构为学习一个结构化的哈密顿量能量景观，其梯度直接产生局部控制动作。系统总能量定义为动能与势能之和：

$$\mathcal{H}(q, p) = K(p) + P(q)$$

其中 $K(p)$ 为动能项，$P(q)$ 为势能项，二者共同编码控制目标、约束和适应策略（Section 1.2 Eq.1）。

通过 Legendre-Fenchel 共轭消除显式控制变量后，系统内禀运动律由以下控制哈密顿量描述（Section 3.2）：

$$H(\boldsymbol{q}, \boldsymbol{p}; \mathcal{E}) = \varphi^*(\boldsymbol{A}(\boldsymbol{q})^{\top} \boldsymbol{p}) + \boldsymbol{p}^{\top} \boldsymbol{f}(\boldsymbol{q}) + \mathcal{R}(\boldsymbol{q}; \mathcal{E})$$

其中 $\varphi^*$ 为控制惩罚的共轭函数，$\boldsymbol{f}(\boldsymbol{q})$ 为漂移项，$\mathcal{R}(\boldsymbol{q}; \mathcal{E})$ 为环境条件化的势能。在常见的二次控制惩罚情形下，该哈密顿量退化为：

$$H(\boldsymbol{q}, \boldsymbol{p}; \mathcal{E}) = \frac{1}{2} \boldsymbol{p}^{\top} (\boldsymbol{A}(\boldsymbol{q}) \Phi^{-1} \boldsymbol{A}(\boldsymbol{q})^{\top}) \boldsymbol{p} + \boldsymbol{p}^{\top} \boldsymbol{f}(\boldsymbol{q}) + \mathcal{R}(\boldsymbol{q}; \mathcal{E})$$

### 势能的模块化分解

总势能 $\mathcal{R}$ 由元策略 $g_{\xi}$ 根据环境 $\mathcal{E}$ 动态加权的四项组成（Section 3.2 Eq.4）：

$$\mathcal{R}(q; \omega, \eta_{\xi}(\mathcal{E})) = E_{\mathrm{sensor}} + \beta(\mathcal{E}) E_{\mathrm{goal}} + \lambda(\mathcal{E}) E_{\mathrm{obj}} + \sum_{i \in \mathcal{C}_t} \alpha_i b(d_i)$$

各分量含义如下：
- **$E_{\mathrm{sensor}}$**：传感器代价，驱动感知行为的信息采集质量；
- **$E_{\mathrm{goal}}$**：目标吸引势，引导机器人趋向目标位置，权重 $\beta(\mathcal{E})$ 由环境上下文调节；
- **$E_{\mathrm{obj}}$**：变形能量，约束机器人形状变化的平滑性与拉伸代价，权重 $\lambda(\mathcal{E})$ 控制变形激进程度；
- **$\sum \alpha_i b(d_i)$**：主动障碍物屏障项，将障碍物边界直接嵌入势能，$\mathcal{C}_t$ 为当前帧内活跃约束集，$\alpha_i$ 为自适应对偶权重。

这种分解使得安全约束不再依赖脆弱的奖励塑形或外部滤波器，而是作为哈密顿量势能的天然组成部分，通过统一梯度调节实现安全与任务目标的协调。

### 三策略独立得分函数架构

Navigator 将导航问题分解为三个独立得分函数模块，分别对应感知、规划和变形（Section 3.3）：

| 策略模块 | 角色 | 状态空间 | 核心势能项 |
|---------|------|---------|-----------|
| Sensor Policy $\pi_y$ | 感知适应与信息采集 | 传感器位姿 $q_y$ | $E_{\mathrm{sensor}} + \sum \alpha_i b(d_i)$ |
| Frame Policy $\pi_f$ | 无碰撞路径规划 | 帧位姿 $q_f$ | $\beta E_{\mathrm{goal}} + \sum \alpha_i b(d_i)$ |
| Shape Policy $\pi_o$ | 机器人变形控制 | 形状参数 $q_o$ | $\lambda E_{\mathrm{obj}} + \sum \alpha_i b(d_i)$ |

每个策略 $\pi_k$ 定义为基于学习到的能量泛函梯度的独立得分函数：

$$s_k^{\theta_k}(z_k, \mathcal{E}, t) = S_k^{\theta_k}\bigl(\nabla_{z_k} h_k^{\theta_k}(z_k, \mathcal{E}, t)\bigr)$$

各模块的局部哈密顿量具有统一结构（Section 3.3）：

$$H_k(q_k, p_k; \xi, \mathcal{E}) = \frac{1}{2} p_k^{\top} M_k(q_k)^{-1} p_k + \mathcal{R}_k(q_k; \mathcal{E})$$

其中 $M_k(q_k)^{-1}$ 为反质量矩阵，$\mathcal{R}_k$ 为模块专属势能。参数集满足互斥性 $\Theta_i \cap \Theta_j = \emptyset$（$i \neq j$），确保独立并行训练，且总样本复杂度为各策略维度之和的线性界（Theorem 3.4）。

### 端口哈密顿量动力学与耗散

每个子模块的动量更新遵循端口哈密顿量动力学（Section 3.3 Eq.9）：

$$\dot{p}_k = -\nabla_{q_k} h_k^{\theta_k} - \Gamma_k^{\xi} \nabla_{p_k} h_k^{\theta_k} + G_k^{\xi} u_k^{\xi}$$

三项分别对应：保守哈密顿力（$-\nabla_{q_k} h_k^{\theta_k}$）、瑞利阻尼（$-\Gamma_k^{\xi} \nabla_{p_k} h_k^{\theta_k}$）和外部端口输入（$G_k^{\xi} u_k^{\xi}$）。摩擦项 $\Gamma_k^{\xi}$ 由元策略在线调节，消融实验证实其缺失会导致欠阻尼振荡和障碍物穿透（Table 6）。

得分函数记录了完整的确定性漂移（Section 3.3）：

$$s_k(z_k, t) := \begin{bmatrix} \nabla_{p_k} h_k^{\theta_k} \\ -\nabla_{q_k} h_k^{\theta_k} \end{bmatrix} + \begin{bmatrix} 0 \\ -\Gamma_k^{\xi} \nabla_{p_k} h_k^{\theta_k} + G_k^{\xi} u_k^{\xi} \end{bmatrix}$$

### 时间层级与在线适应

三个策略运行在不同自然频率上，形成嵌套拟静态近似（Section 3.4, Figure 2）：传感器策略以最低频率（每阶段一次）建立环境约束集 $\mathcal{C}_t$；路径策略以中等频率计算航点；形状策略以最高频率在每个积分步持续适应。慢速传感器更新为更快的路径和形状适应提供稳定约束，实现无耦合的层级协调。

在线阶段，Navigator 将离线学习到的参考哈密顿量与环境驱动的修正项结合：

$$h^{\mathrm{adapted}} = h^{\mathrm{ref}} + \Delta h^{\mathrm{context}}$$

系数 $(\beta, \gamma, \bar{\alpha})$ 由元策略根据感知到的障碍物配置和目标上下文动态演化，本质上是重新定义约化哈密顿量本身，而非仅调整动作输出（Figure 10）。这种深层适应使得系统在感知到新障碍物时能够修改整个局部能量景观，而非仅做局部反应。



## 实验与关键发现

### 核心导航性能对比

GRL-SNAM在2D可变形环形机器人导航任务上实现了路径质量与建图预算的最优平衡。在仅成功轨迹的分析中（Table 5），GRL-SNAM取得**SPL 0.95**，接近基于模型的安全滤波方法CBF（0.96），同时仅消耗**10.7%的建图预算**，与纯反应式势场法PF（10.7%）持平。相比之下，在相同短回合分布和局部观测条件下训练的深度RL基线表现显著逊色：PPO仅达SPL 0.77，且绕路比（Detour Ratio）高达1.34，表明其路径效率与安全性均不足。这一结果的核心机制在于：GRL-SNAM通过哈密顿量能量景观的梯度直接产生控制动作，无需值函数近似或显式规划树，从而在局部感知条件下实现了接近全局规划质量的路径。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/012_Table_5.jpg]]
*Table 5: Comparison of navigation quality across methods (success-only runs). GRL-SNAM achieves near-CBF path efficiency while consuming the same minimal mapping budget as PF. SPL = Success weighted by Path Length; Detour = executed path length / shortest path length*

在点智能体地下城导航任务中（Table 3），GRL-SNAM的优势更为突出：在相同感知、架构和短回合训练分布下，GRL-SNAM成功率达到**87.5%**，而PPO仅为26.1%，TRPO为21.7%，SAC为18.4%。同时，GRL-SNAM的平均状态误差（0.3 m）和目标距离（0.1 m）远低于深度RL基线（1.8–2.4 m和1.2–1.9 m）。值得注意的是，全回合端到端训练的RL基线（Table 8）在该任务上几乎完全失败——PPO成功率仅7.2%，TRPO和SAC分别为5.8%和4.1%，这进一步验证了阶段式哈密顿量监督相较于端到端RL的样本效率和泛化优势。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/007_Table_3.jpg]]
*Table 3: Short-rollout baselines vs. GRL-SNAM on the point-agent navigation task*

### 哈密顿量适应与能量景观动态

GRL-SNAM的核心能力不仅体现在最终指标上，更体现在其对环境变化的深层结构适应。Figure 10的定量验证揭示了三个关键动态：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/015_Figure_10.jpg]]
*Figure 10: Quantitative validation of GRL-SNAM. Top: clearance stays above collision threshold, ensuring safety. Middle: force magnitudes adapt to environment complexity. Bottom: coefficients ( $\beta , \gamma , \bar { \alpha }$ ) evolve dynamically, confirming online adaptation and stagewise refinement of the Hamiltonian

1. **安全空隙保持**：在整个导航过程中，最小空隙始终保持在碰撞阈值之上，验证了障碍物势垒作为哈密顿量势能天然项的有效性。
2. **力幅值自适应**：力幅值随环境复杂度动态变化，在通过狭窄缝隙时显著增强，在开阔区域减弱，体现了元策略对环境条件的精细响应。
3. **系数在线演化**：目标吸引系数$\beta$、障碍物排斥系数$\gamma$和平均屏障权重$\bar{\alpha}$随时间动态调整，本质上是在重新定义约化哈密顿量本身，而非仅仅调动作。这验证了方法的核心主张——GRL-SNAM在新障碍物被感知时修改的是整个局部能量景观（Figure 4, Section 4.1）。

Figure 4进一步展示了哈密顿力场的组合性质：目标力$F_g$与障碍物力$F_{bs}$通过自适应系数合成为统一的导航场，确保轨迹既目标导向又安全避碰。这种统一协调是传统势场法或独立安全滤波器难以实现的。

### 消融实验：摩擦与多起点损失的关键作用

Table 6的损失项消融揭示了两个关键组件的互补机制：

- **移除摩擦损失（w_fric=0）**：导致欠阻尼振荡，智能体频繁穿透障碍物。摩擦项的作用是提供瑞利阻尼，确保哈密顿量流在能量耗散下稳定收敛，而非持续振荡。
- **仅保留多起点损失（w_fric=0, w_multi=0.5）**：智能体避免碰撞但运动过于保守，进展缓慢。多起点损失强制策略在多个初始条件下均能成功，但缺乏摩擦时无法产生平滑轨迹。
- **摩擦+多起点组合（w_fric=0.1, w_multi=0）**：获得最佳整体性能——低碰撞、高空隙、高SPL和高平滑度。然而，若多起点权重过高会略微降低最小空隙，提示两项损失之间存在权衡。

这一消融验证了端口哈密顿量动力学中耗散项（$\Gamma_k^{\xi}$）对稳定性的不可或缺性，以及多起点训练对避免过度保守策略的必要性。

### 鲁棒性与分布外泛化

Table 7的鲁棒性测试表明，GRL-SNAM在感知噪声和动力学扰动下呈现渐进退化而非灾难性失效：从标称条件（噪声水平0.0, 动力学因子1.0）到严重噪声（0.10, 0.7），成功率从98.7%降至87.1%，SPL从0.82降至0.72，最小空隙从0.45 m降至0.28 m。这种渐进退化而非断崖式下跌，归因于哈密顿量结构提供的能量守恒约束——即使感知存在偏差，底层辛几何仍保持长期展开的稳定性。

在分布外（Test-OOD）环境中的定性对比（Figure 8）进一步证实了泛化优势：GRL-SNAM产生平滑、短且保持空隙的轨迹，成功穿越狭窄通道；而运动学和动力学RL策略（PPO/TRPO/SAC-Kin/Dyn）通常停滞、碰撞或远离目标；全局规划器（Rigid A*、Deformable A*）虽能成功但路径锯齿状或过度保守；反应式基线（PF、CBF、DWA）则振荡、擦碰障碍物或路径更长。Figure 9的主实验对比汇总确认了GRL-SNAM在成功率、SPL、平滑度和空隙四个维度上的全面占优，并在帕累托前沿上唯一实现高效率与高安全性的统一。

### 范式级能力对比

Table 4的扩展范式对比从十个维度评估了八种学习框架。GRL-SNAM是唯一在所有维度上获得“全面支持（✓）”的方法，包括能量守恒、几何结构保持、约束集成、在线适应、多尺度协调和物理可解释性等。相比之下，标准RL（PPO/SAC）在能量守恒、几何结构和约束集成方面均为“不支持（×）”，基于模型的方法（CBF/MPC）在在线学习和多尺度协调方面存在局限。这一对比从方法论层面解释了GRL-SNAM在实验中的系统性优势。

### 失败模式与局限

尽管整体性能优异，GRL-SNAM仍存在以下已知局限：

1. **场景维度限制**：当前验证限于二维超弹性环形机器人和点智能体导航，未涉及三维环境或更复杂的动力学模型。
2. **感知假设**：框架依赖精确的局部传感和相对简单的障碍物基元（圆近似）。Table 7虽展示了噪声鲁棒性，但对真实传感器噪声和不规则几何的全面评估仍有待进行。
3. **部署复杂度**：离线训练和在线适应所需的多策略、多阶段部署流程较为复杂，增加了实际集成的工程难度。
4. **在线雅可比更新假设**：元策略权重和端口输入的在线雅可比更新依赖可观测量的局部线性近似，在极度非线性或快速变化场景下可能失效——这需要进一步的手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KcC5mwfGf0/figures/004_Table_1.jpg]]
*Table 1: Navigation quality comparison (success-only runs). GRL-SNAM achieves near-CBF efficiency with minimal mapping budget, while deep RL baselines trained on the same short-rollout distribution and local observations yield lower SPL, larger detours, and smaller clearances*



## 定位与知识库关联

### 与经典规划与反应式方法的对比

GRL-SNAM 在导航质量上达到了与 **CBF**（控制屏障函数）相近的路径效率（SPL 0.95 vs. 0.96，绕路比 1.09 vs. 1.04），但仅消耗与 **PF**（势场法）相当的最小建图预算（10.7%）。这一结果揭示了该方法的核心优势：哈密顿量结构将障碍屏障直接嵌入势能项，消除了传统势场法中目标吸引与障碍排斥之间的脆弱平衡问题。相比之下，**DWA**（动态窗口法）和 **Rigid A*** 等全局规划器虽然能成功到达目标，但路径呈现锯齿状或过度保守（Figure 8），且无法处理可变形体的形状适应。**Deformable A*** 虽然考虑了变形惩罚，但其刚性搜索范式无法像 GRL-SNAM 那样在感知到新障碍物时动态修改整个局部能量景观（Figure 10）。

### 与深度强化学习基线的根本差异

GRL-SNAM 与 **PPO**（Schulman et al., 2017）、**TRPO** 和 **SAC**（Haarnoja et al., 2018）等深度 RL 方法的差异是范式级的。在点智能体地下城导航任务中，端到端 RL 的全回合成功率极低（约7%，Table 8），而 GRL-SNAM 在相同的局部观测空间、动作空间和短回合分布下达到 87.5%（Table 3）。这一鸿沟源于学习信号的本质差异：RL 基线依赖值函数的贝尔曼自助，而 GRL-SNAM 通过微分策略优化（DPO）直接学习哈密顿量能量景观，其梯度即产生控制动作，无需值函数或显式规划树。Table 4 的范式级对比进一步表明，GRL-SNAM 是唯一在能量守恒、几何结构保持、约束集成、在线适应和多尺度协调等十个维度上均获得全面支持（✓）的框架。

### 安全集成范式的跃迁

传统方法通过外部 CBF 滤波器、奖励塑形或碰撞惩罚间接处理安全约束。GRL-SNAM 将障碍势垒作为可加至哈密顿量势能的天然项，通过自适应对偶权重实现安全与任务目标的统一梯度调节。这一设计的因果机制在于：当新障碍物被感知时，元策略动态调整系数 $(\beta, \gamma, \bar{\alpha})$，重新定义整个约化哈密顿量本身，而非仅在动作层面施加修正（Figure 10）。这解释了为何 GRL-SNAM 能在维持最小空隙的同时，产生比 CBF 滤波方法更平滑、更结构化的轨迹。

### 多时间尺度协调的独特优势

GRL-SNAM 的嵌套哈密顿量子系统（传感器/帧/变形策略）运行在不同自然频率上，利用拟静态近似实现无耦合的稳定层级协调（Figure 2）。传感器策略以低频（每阶段一次）建立环境约束集，帧策略以中频计算路径点，形状策略以高频在每个积分步连续适应。这种设计避免了手动层级设计的脆弱性，同时通过独立得分函数架构（Definition 3.1）实现了并行训练，其样本复杂度为各策略维度之和的线性界（Theorem 3.4），而非联合维度的指数级增长。

### 适用边界与局限

当前验证存在明确的边界限制：

1. **环境维度与动力学复杂度**：所有实验限于二维超弹性环形机器人和点智能体导航，未涉及三维环境或更复杂的动力学模型（如多体系统、接触摩擦）。
2. **感知假设**：框架依赖精确的局部传感和相对简单的障碍物基元（圆近似）。Table 7 的鲁棒性测试显示，在感知噪声和动力学扰动下性能出现渐进退化，但对真实传感器噪声（如深度图像缺失、语义分割错误）和不规则几何的鲁棒性仍有待全面评估。
3. **部署复杂度**：离线训练和在线适应所需的多策略、多阶段部署流程较为复杂，元策略权重和端口输入的在线雅可比更新依赖于可观测量的局部线性近似，在极度非线性或快速变化场景下可能失效。
4. **消融揭示的敏感依赖**：摩擦损失项对稳定性至关重要——移除摩擦（$w_{\text{fric}}=0$）导致欠阻尼振荡和障碍物穿透（Table 6）；仅保留多起点损失则导致过度保守、进展缓慢。这表明损失项权重的调优对最终行为有显著影响。

### 开放问题

1. **感知模态扩展**：如何将 GRL-SNAM 扩展到更丰富的感知模态（如深度图像、语义分割）和三维可变形体，同时保持哈密顿量结构的归纳偏置？
2. **真实平台验证**：能否在真实的柔软机器人平台上验证该方法，并应对真实物理交互（如非弹性碰撞、摩擦接触）与通信延迟？
3. **与基于模型方法的融合**：哈密顿量结构与模型预测控制（MPC）能否结合，利用 MPC 的长期约束满足能力弥补在线雅可比更新的短视性？
4. **降低交互成本的训练范式**：在稀疏奖励或仅提供演示的设定下，哈密顿量参考能否通过模仿学习或离线 RL 获得，从而降低在线交互成本？



## 原文 PDF

![[paperPDFs/ICLR_2026/GRL_SNAM_Geometric_Reinforcement_Learning_with_Differential_Hamiltonians_for_Navigation_and_Mapping_in_Unknown_Environments.pdf]]
