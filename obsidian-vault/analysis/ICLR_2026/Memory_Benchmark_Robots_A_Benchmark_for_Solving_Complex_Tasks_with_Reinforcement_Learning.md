---
title: "Memory, Benchmark & Robots: A Benchmark for Solving Complex Tasks with Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Memory_Benchmark_Robots_A_Benchmark_for_Solving_Complex_Tasks_with_Reinforcement_Learning.pdf
openreview_forum_id: 9cLPurIZMj
aliases:
- MMISASA
- MBRBSCTRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入系统化的记忆任务分类（对象、空间、序列、容量），可以精确控制任务的记忆负荷和类型，从而诊断智能体在不同记忆维度上的优势与不足。"
primary_logic: "构建覆盖四类记忆任务的统一基准MIKASA，包括MIKASA-Base通用环境和MIKASA-Robo机器人操作任务，能够系统揭示当前强化学习算法及视觉-语言-动作模型在长时记忆上的严重缺陷，推动记忆增强机制的发展。"
claims:
- "PPO-MLP在状态完整条件下可达100%成功率，但在部分可观测RGB+关节模式下，即使PPO-LSTM也几乎无法解决中等以上复杂度的任务，证明了任务本身对记忆的强依赖。"
- "所有测试的离线RL模型（RATE、DT、BC、CQL、DP）在MIKASA-Robo 32个任务中无法解决绝大多数任务，特别是在记忆容量和序列记忆任务上成功率几乎为零。"
- "在真实世界RememberColor3-v0实验中，经过微调的VLA模型π0.5在完整记忆要求下触碰成功率仅0.10，远低于无记忆要求任务（1.00），直接验证了当前模型缺乏长时记忆能力。"
- "MIKASA-Robo ShellGameTouch-v0 (sparse, RGB) 上 Success Rate = RATE: 0.92±0.01"
---

# Memory, Benchmark & Robots: A Benchmark for Solving Complex Tasks with Reinforcement Learning

> [!tip] 核心洞察
> 构建覆盖四类记忆任务的统一基准MIKASA，包括MIKASA-Base通用环境和MIKASA-Robo机器人操作任务，能够系统揭示当前强化学习算法及视觉-语言-动作模型在长时记忆上的严重缺陷，推动记忆增强机制的发展。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 内存、基准与机器人：一种用强化学习解决复杂任务的基准测试 |
| 英文题名 | Memory, Benchmark & Robots: A Benchmark for Solving Complex Tasks with Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9cLPurIZMj); [Project](https://tinyurl.com/membenchrobots) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MIKASA (Memory-Intensive Skills Assessment Suite for Agents) |
| Dataset | MIKASA-Robo ShellGameTouch-v0 (sparse, RGB), MIKASA-Robo RememberColor3-v0 (sparse, MIKASA-Robo BunchOfColors7-v0 (sparse, Real-world RememberColor3-v0 (Task 3) |

> [!tip] 效果简介
> - MIKASA-Robo ShellGameTouch-v0 (sparse, RGB) 上，Success Rate 为 RATE: 0.92±0.01，对比 BC: 0.00±0.00，变化 0.92。
> - MIKASA-Robo RememberColor3-v0 (sparse, RGB) 上，Success Rate 为 RATE: 0.65±0.01，对比 BC: 0.00±0.00，变化 0.65。
> - MIKASA-Robo BunchOfColors7-v0 (sparse, RGB) 上，Success Rate 为 RATE: 0.00±0.00，对比 BC: 0.00±0.00，变化 0.00。

## 概述

强化学习（RL）在解决复杂决策任务上取得了显著进展，但现有基准测试普遍忽视了对**记忆能力**的系统评估。尽管部分可观马尔可夫决策过程（POMDP）框架在理论上要求智能体具备记忆，实践中多数研究仍将记忆增强方法（如LSTM、Transformer）在完全可观的MDP环境中测试，导致无法公平比较不同记忆机制的有效性。尤其在机器人操作领域，任务常要求智能体在数秒甚至数十秒的遮挡、干扰后召回关键信息，而现有机器人基准几乎不包含此类记忆依赖场景。

**核心瓶颈**在于：缺乏统一的记忆能力评估基准，使得各类记忆增强方法无法在同一框架下公平比较，且缺少专门针对机器人操作任务中时空记忆需求的测试环境。

针对上述问题，本文提出 **MIKASA**（Memory-Intensive Skills Assessment Suite for Agents），一个面向记忆密集型任务的综合基准。MIKASA包含三项核心贡献：

1. **系统化的记忆任务分类框架**：将记忆需求划分为**对象记忆**、**空间记忆**、**序列记忆**和**记忆容量**四类，为任务设计和结果诊断提供结构化视角（Figure 1）。
2. **MIKASA-Base**：整合现有开源记忆密集型环境，提供统一API和分层评估能力。
3. **MIKASA-Robo**：包含32个精细设计的机器人桌面操作任务，覆盖全部四类记忆类型，支持多种观察模式（状态、RGB、RGB+关节）和奖励函数（稀疏/密集），并配套提供100%成功率的专家演示数据集。

**核心实验结论**（Figure 4–6, Table 8, Table 10）：
- 在状态完全可观模式下，PPO-MLP可达**100%成功率**，证明任务本身可解；但在部分可观测的RGB+关节模式下，即使PPO-LSTM也几乎无法解决中等以上复杂度的任务，确认了任务对记忆的强依赖。
- 所有测试的离线RL模型（RATE、DT、BC、CQL、DP）在MIKASA-Robo的32个任务中无法解决绝大多数任务，尤其在记忆容量和序列记忆任务上成功率趋近于零。
- 真实世界RememberColor3-v0实验中，微调后的视觉-语言-动作模型π0.5在完整记忆要求下触碰成功率仅**0.10**，远低于无记忆要求任务的**1.00**，直接验证了当前模型长时记忆能力的严重缺失。

这些结果表明，MIKASA成功揭示了当前RL算法及VLA模型在记忆维度上的系统性缺陷，为记忆增强机制的研究提供了可量化、可比较的评估平台。

## 背景与动机

### 强化学习中的记忆瓶颈

强化学习（RL）在解决序列决策问题上取得了显著进展，但大多数成功案例仍局限于马尔可夫决策过程（MDP）框架，即智能体在每个时刻都能获取完整的、足以做出最优决策的状态信息。然而，现实世界中的机器人操作任务天然是部分可观测的（POMDP）：关键信息可能在某个时刻被短暂揭示，而智能体必须在数秒甚至数分钟后才能利用该信息做出正确动作。例如，机器人观察到一个目标物体的颜色后，该物体可能被遮挡或移出视野，但机器人仍需记住这一信息以完成后续操作。

本文将这类任务形式化定义为**记忆密集型任务**（memory-intensive task）：存在关联时间步长阈值 $\xi > 1$ 的POMDP，其中 $\xi$ 表示一个对决策至关重要的事件发生时刻与该信息必须被回忆利用的时刻之间的最小时间步数。当 $\xi > 1$ 时，智能体无法仅依赖当前观测做出正确决策，必须通过某种记忆机制来桥接这一时间间隔。

### 现有评估体系的碎片化困境

当前强化学习领域缺乏统一的记忆能力评估基准，导致三个核心问题：

**碎片化的环境设计。** 如表2所示，已有记忆增强方法（如带有LSTM的PPO、Decision Transformer、RATE等）各自在定制的环境中进行评估，这些环境在记忆类型、难度和接口上互不兼容。Atari游戏虽然被广泛使用，但许多研究仅通过帧堆叠（frame stacking）将其转化为MDP进行评估，并未真正测试智能体的记忆能力。这种碎片化使得不同方法之间无法进行公平、系统的比较。

**缺乏系统化的记忆分类。** 现有基准通常仅覆盖1-2种记忆类型（如空间记忆或序列记忆），缺少一个能同时诊断智能体在多种记忆维度上表现的统一框架。研究者无法回答“我的智能体擅长哪种记忆？在哪种记忆上存在短板？”这样的基本问题。

**机器人操作领域的空白。** 如表3所示，主流的机器人操作框架（如ManiSkill、Robosuite等）几乎不包含专门设计的记忆密集型任务。尽管部分框架提供了部分可观测模式，但任务本身并不强制要求记忆能力——智能体可以通过当前观测直接推断出正确动作。这导致在仿真中表现优异的模型部署到真实机器人时，面对需要记忆的任务往往严重失效。

### 本文的动机与目标

为填补上述空白，本文提出**MIKASA**（Memory-Intensive Skills Assessment Suite for Agents）——一个面向强化学习记忆能力的综合基准测试套件。其核心动机在于：

1. **建立统一的记忆任务分类体系**，将记忆需求系统化地划分为对象记忆、空间记忆、序列记忆和容量记忆四类（图1），为任务设计和结果分析提供理论框架。
2. **构建标准化的评估平台**，通过MIKASA-Base整合现有开源记忆环境，通过MIKASA-Robo提供32个专门设计的机器人操作任务，覆盖全部四类记忆，使不同算法能在相同条件下公平比较。
3. **揭示当前方法的真实记忆能力缺陷**，特别是验证视觉-语言-动作（VLA）模型和离线RL模型在长时记忆任务上的严重不足，从而推动记忆增强机制的研究。

图3概括了MIKASA的设计哲学：虽然智能体任务不需要人类记忆的全谱系能力，但也不能被简化为简单的时空依赖关系。MIKASA在两者之间提供了一个平衡的评估框架，旨在系统诊断智能体在不同记忆维度上的优势与不足。

## 核心创新

MIKASA的核心创新并非提出新的记忆增强算法，而是构建了一套系统化的评估基础设施，填补了强化学习领域长期存在的“记忆能力无法统一衡量”的空白。其创新点可归纳为三个紧密耦合的层次。

### 1. 记忆任务分类框架：从模糊需求到可诊断维度

此前，记忆需求在强化学习任务中往往被隐含地处理，缺乏显式的分类学定义。MIKASA提出了一个形式化的分类框架，将记忆密集型任务解构为四个正交维度：

- **对象记忆（Object Memory）**：智能体必须记住之前观察到的特定对象属性（如颜色、形状），并在后续决策中基于该记忆采取行动。
- **空间记忆（Spatial Memory）**：智能体需要追踪物体的空间位置或轨迹，即使该物体不再直接可见。
- **序列记忆（Sequential Memory）**：智能体必须记住一个时间序列中的事件顺序或模式，并据此做出响应。
- **容量记忆（Memory Capacity）**：任务要求同时记住多个独立的信息片段，直接考验智能体记忆存储的上限。

这一分类框架的因果调控作用在于：它允许研究者通过组合或调整这些维度，精确控制任务的记忆负荷与类型，从而诊断智能体在特定记忆维度上的瓶颈。例如，`RememberColor3-v0` 主要考验对象记忆，而 `SeqOfColors` 则同时施加序列记忆和容量记忆压力。该框架是后续基准设计和结果分析的逻辑基石。

### 2. 统一基准的双层架构：MIKASA-Base 与 MIKASA-Robo

MIKASA通过构建双层基准，解决了现有环境碎片化、接口不统一的问题，实现了从诊断性测试到现实任务的全覆盖。

| 层级 | 定位 | 关键改进 | 证据锚点 |
|------|------|----------|----------|
| **MIKASA-Base** | 整合现有开源记忆密集型环境，提供统一 Gymnasium API | 将分散的向量诊断环境（如 `PassiveT-Maze`）和图像复杂任务（如 `Memory Maze`）纳入同一框架，支持分层评估 | Section 5, Table 9 |
| **MIKASA-Robo** | 专为机器人桌面操作设计的32个记忆任务 | 覆盖全部四类记忆，提供状态/RGB+关节两种观察模式、密集/稀疏两种奖励函数，并基于 ManiSkill3 实现 GPU 并行训练 | Section 6, Table 1 |

**MIKASA-Robo 的差异化优势**体现在对现有机器人操作框架的对比中。如 Table 3 所示，主流框架（如 Meta-World、RLBench、CALVIN）几乎不包含显式的记忆密集型任务，而 MIKASA-Robo 是首个在机器人操作领域系统覆盖多类记忆需求的基准。任务设计的关键原则是“隔离性”：每个任务仅需记忆一种特定类型的信息（`Oracle Info`），从而确保性能差异可归因于特定的记忆能力缺陷，而非任务本身的复合难度。

### 3. 标准化工具链与可复现性保障

MIKASA 通过标准化工具链降低了记忆增强研究的进入门槛和实验偏差：

- **统一 API**：采用 Gymnasium 标准接口，支持模块化环境封装，便于与现有算法库集成。
- **专家数据集**：为所有 MIKASA-Robo 任务提供 100% 成功率的专家演示数据（1000 条轨迹），确保离线强化学习基线在相同数据分布下训练，消除了数据质量差异对结论的干扰。
- **可配置难度**：提供可调节的参数（如物体数量、记忆间隔长度、奖励稠密程度），支持课程学习和消融实验。
- **真实世界验证协议**：设计了三阶段递增测试协议（Task 1 验证执行可行性，Task 2 控制动态干扰，Task 3 单独测量记忆需求），有效隔离了感知、控制与记忆能力的混淆因素。

这些工程创新确保了基准结论的可靠性。例如，Figure 4 中 PPO-MLP 在状态完全可观模式下达到 100% 成功率，直接证明了任务本身是可解的，从而将后续在部分可观测模式下的失败归因于记忆需求，而非任务设计缺陷。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/001_Figure_1.jpg]]
*Figure 1: Systematic classification of problems with memory in RL reveals distinct memory utilization patterns and enables objective evaluation of memory mechanisms across different agents*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/002_Table_1.jpg]]
*Table 1: MIKASA-Robo: A benchmark comprising 32 memory-intensive robotic manipulation tasks across 12 categories. Each task varies in difficulty and configuration modes. The table specifies episode timeout (T), the necessary information that the agent must memorize in order to succeed (Oracle Info), and task instructions (Prompt) for each environment. See Appendix K for details*

### 问题定义：记忆密集型任务的形式化

MIKASA基准将记忆密集型任务严格定义为一类特殊的**部分可观测马尔可夫决策过程（POMDP）**。一个POMDP由元组 $(\tilde{S}, \tilde{A}, T, R, \bar{\Omega}, \bar{O}, \gamma)$ 定义，其中状态转移函数 $T(s' | s, a) : S \times A \times \hat{S} \to [0,1]$ 和观测函数 $O(o | s, a) : S \times A \times \Omega \to [0,1]$ 刻画了智能体无法直接感知完整环境状态的本质。强化学习的目标是最大化期望折扣累积奖励 $\mathbb{E}_{\pi}\left[\sum_{t=0}^{\infty} \gamma^t R(s_t, a_t)\right]$。

区分记忆密集型任务与非记忆任务的关键在于**关联时间步长（correlation horizon）** $\xi$。当 $\xi > 1$ 时，决策所需的关键事件与信息召回时刻之间存在超过一个时间步的间隔，智能体必须跨越这一间隔维持信息，从而构成对记忆能力的刚性需求。这一形式化定义为基准中所有任务的设计和分类提供了统一的理论锚点。

### 三级模块化架构

MIKASA的整体框架由三个核心模块构成，形成从理论分类到统一评估再到专用测试的完整流水线：

**模块一：记忆任务分类框架。** 该模块将记忆密集型任务系统化地分为四类：
- **对象记忆（Object Memory）**：智能体需记住特定物体的属性（如颜色、形状），并在后续交互中识别该物体。
- **空间记忆（Spatial Memory）**：智能体需追踪物体位置或运动轨迹，即使物体被遮挡或移出视野。
- **序列记忆（Sequential Memory）**：智能体需记住事件或动作的发生顺序，并按序复现或推理。
- **容量记忆（Memory Capacity）**：智能体需同时维持多个独立信息项，测试记忆容量的上限。

这一分类框架（Figure 1）不仅指导了基准任务的设计，也为实验结果的分析提供了维度——不同算法在四类记忆上的表现可被独立诊断。

**模块二：MIKASA-Base。** 这是一个统一的通用记忆基准，整合了现有开源社区中广泛使用的记忆密集型环境（如POPGym、MemoryGym等）。所有环境被封装为标准的Gymnasium API，支持模块化调用和GPU并行训练。任务按难度分为两级：第一级为基于向量的诊断性环境，隔离特定记忆机制；第二级为基于图像的复杂环境，引入真实感知挑战。Table 9展示了MIKASA-Base中24个环境在四类记忆分类下的分布。

**模块三：MIKASA-Robo。** 这是专门为机器人桌面操作场景设计的记忆基准，包含32个精细任务，覆盖全部四类记忆（Table 1）。任务构建于ManiSkill3框架之上，支持多种观察模式（全状态、RGB+关节信息）和奖励函数（密集/稀疏），可通过可配置参数（物体数量、记忆间隔、序列长度）精确调节记忆负荷。该模块还提供100%成功率的专家演示数据集（1000条轨迹），支持离线强化学习研究。

### 输入输出流与评估协议

基准的标准化输入输出流如下：
- **输入**：环境提供部分可观测的传感器数据（RGB图像、机器人关节状态），智能体无法直接访问完整状态。
- **输出**：智能体在每个时间步输出动作，环境返回下一观测、奖励和终止信号。
- **评估协议**：所有任务使用100个随机种子回合评估，报告成功率均值±标准误。在线RL实验采用统一的超参数配置（从ManiSkill3移植），离线RL模型基于相同的专家数据集训练，确保公平可比。

### 关键设计决策

1. **可解性验证**：在状态完全可观的MDP模式下，PPO-MLP在所有任务上达到100%成功率（Figure 4），证明任务本身可解，部分可观测性（而非任务难度）是核心瓶颈。
2. **难度梯度控制**：通过调节任务参数（如RememberColor中颜色数量从3增至9），可系统评估智能体在不同记忆负荷下的性能退化曲线。
3. **真实世界验证通道**：框架包含真实世界实验协议（Figure 26），采用三阶段递增设计（Task 1验证执行可行性，Task 2控制动态干扰，Task 3单独测量记忆需求），隔离混淆因素。

## 核心模块与公式推导

### 问题形式化：POMDP与记忆密集型任务

MIKASA将记忆密集型强化学习问题形式化为部分可观马尔可夫决策过程（POMDP），其标准元组定义为：

$$( \tilde { S } , \tilde { A } , T , R , \bar { \Omega } , \bar { O } , \gamma )$$

其中 $\tilde{S}$ 为状态空间，$\tilde{A}$ 为动作空间，$T ( s ^ { \prime } | s , a ) : S \times A \times \mathbf { \hat { S } } [ 0 , 1 ]$ 为状态转移函数，$R$ 为奖励函数，$\bar{\Omega}$ 为观测空间，$\bar{O}(o|s,a): S \ \bar{\times} \ A \times \Omega [0,1]$ 为观测函数，$\gamma$ 为折扣因子。智能体的目标是最大化期望折扣累积奖励：

$$\mathbb { E } _ { \pi } \left[ \sum _ { t = 0 } ^ { \infty } \dot { \gamma } ^ { t } R ( s _ { t } , a _ { t } ) \right]$$

在此基础上，MIKASA定义了**记忆密集型任务**的判定准则：若存在关联时间步长阈值 $\xi > 1$，即决策所需的关键事件与信息回忆时刻之间的最小时间间隔超过单步，则该POMDP构成记忆密集型任务。这一形式化定义将“是否需要记忆”转化为可量化的时间依赖性度量，为后续任务分类和难度标定提供了统一的理论基础。

### 核心模块一：记忆任务分类框架

MIKASA提出系统化的四类记忆任务分类框架（Figure 1），将记忆需求解耦为相互正交的维度：

1. **对象记忆（Object Memory）**：智能体需记住特定对象的身份或属性（如颜色、形状），并在后续步骤中从干扰项中识别目标对象。典型任务如 `RememberColor3-v0`，要求智能体观察目标颜色后，在物体被遮挡或移除后仍能选择正确颜色的方块。

2. **空间记忆（Spatial Memory）**：智能体需记住对象或目标的空间位置信息，即使该位置不再直接可见。典型任务如 `ShellGameTouch-v0`，智能体需追踪杯子下小球的位置，在杯子被移动后触碰正确的杯子。

3. **序列记忆（Sequential Memory）**：智能体需记住事件或状态出现的先后顺序。典型任务如 `SeqOfColors-v0`，要求智能体按特定顺序触碰多个颜色方块。

4. **容量记忆（Memory Capacity）**：衡量智能体可同时保持的信息量上限。通过增加需记忆的对象数量（如 `RememberColor5-v0` 升级为 `RememberColor9-v0`）或序列长度（如 `SeqOfColors` 从3增至7），可精确控制记忆负荷。

该分类框架的核心设计原则是**正交性与可组合性**：每类记忆可独立调节难度参数，也可组合形成复合记忆需求，从而实现对智能体记忆能力的细粒度诊断。

### 核心模块二：MIKASA-Base统一环境基准

MIKASA-Base整合现有开源记忆密集型环境，采用Gymnasium标准API统一封装，解决先前研究中环境碎片化、接口不一致的问题。其设计包含两个层次：

- **诊断层（Tier 1）**：基于向量的简化环境，隔离特定记忆机制，便于快速原型验证和消融实验。
- **复杂层（Tier 2）**：基于图像的复杂任务，引入真实感知挑战，评估端到端记忆能力。

任务按照上述四类分类框架进行标注（Table 9），使研究者可针对特定记忆维度选择评估环境。

### 核心模块三：MIKASA-Robo机器人记忆任务基准

MIKASA-Robo构建于ManiSkill3框架之上，提供32个机器人桌面操作任务，覆盖全部四类记忆类型（Table 1）。每个任务支持多种观测模式（全状态、RGB+关节角度）和奖励函数（密集奖励、稀疏奖励），并允许通过可配置参数调节记忆负荷：

- **观测模式切换**：全状态模式下任务退化为MDP（无需记忆），可作为可解性验证基线；RGB+关节模式引入部分可观测性，强制记忆需求。
- **难度参数控制**：物体数量（如3/5/7/9个颜色方块）、记忆间隔时长、序列长度等均可调节，支持课程学习和难度消融。
- **奖励函数选择**：密集奖励提供逐步反馈以缓解探索问题，稀疏奖励仅在任务成功时给予信号，更贴近真实场景。

### 核心模块四：专家数据集与工具链

为支持离线强化学习研究，MIKASA-Robo提供100%成功率的专家演示数据集（每条任务1000条轨迹），确保离线RL基线的训练数据分布一致性。同时提供环境定制代码，支持GPU并行训练和模块化封装。

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $( \tilde { S } , \tilde { A } , T , R , \bar { \Omega } , \bar { O } , \gamma )$ | POMDP标准元组 | Section 3.1 |
| $T ( s ^ { \prime } \| s , a ) : S \times A \times \mathbf { \hat { S } } [ 0 , 1 ]$ | 状态转移概率 | Section 3.1 |
| $O ( o \| s , a ) : S \ \bar{\times} \ A \times \Omega [ 0 , 1 ]$ | 观测概率 | Section 3.1 |
| $\mathbb { E } _ { \pi } \left[ \sum _ { t = 0 } ^ { \infty } \dot { \gamma } ^ { t } R ( s _ { t } , a _ { t } ) \right]$ | 期望折扣累积奖励目标 | Section 3.1 |
| $\xi > 1$ | 记忆密集型任务判定阈值 | Section 3.2 |

上述公式均来自论文Section 3的理论定义部分，未进行额外推导或扩展。

## 实验与分析

### 任务可解性验证：MDP模式下的上限

在评估任何记忆增强方法之前，需首先确认任务本身是可解的。在完全可观测的状态模式（MDP）下，PPO-MLP在所有MIKASA-Robo任务上均能达到100%成功率（Figure 4, Figure 10, Figure 11）。这一结果确立了性能上限：任务失败并非源于操作难度或奖励稀疏性，而是源于部分可观测性带来的记忆需求。一旦将观察模式切换为RGB+关节角度的部分可观测设置，PPO-MLP的性能急剧崩溃，即使在密集奖励下也无法解决中等以上复杂度的任务（Figure 5, Figure 12）。这一对比构成基准设计的核心因果证据：**记忆是该基准的核心瓶颈，而非操作技能本身**。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/009_Figure_4.jpg]]
*Figure 4: Performance of PPO-MLP trained in state mode, i.e., in MDP mode without the need for memory. These results suggest that the proposed tasks are inherently solvable with a success rate of 100%. Figure 5: Online RL baselines with MLP and LSTM backbones trained in RGB+joints mode on the RememberColor-v0 environment with dense rewards. Both architectures fail to solve medium and high complexity tasks*

### 在线强化学习基线：LSTM提供有限增益

PPO-LSTM与PPO-MLP的系统对比揭示了LSTM记忆机制的能力边界：

- **短时记忆有效**：在RememberColor3-v0（密集奖励）中，PPO-LSTM显著优于PPO-MLP，表明LSTM的门控机制能够有效保留近期颜色信息（Figure 5）。
- **容量与长时依赖失效**：当颜色数量增至5或9时，PPO-LSTM同样失败，成功率趋近于零。在稀疏奖励条件下，即使3色任务也无法解决（Figure 13 vs Figure 12）。这表明LSTM的固定维度隐状态无法扩展至更高容量的记忆需求。
- **序列记忆瓶颈**：在SeqOfColors和ChainOfColors任务中，随着序列长度从3增至7，PPO-LSTM的成功率急剧下降，暴露了其在序列化信息保持上的根本缺陷。

奖励稠密化（密集 vs 稀疏）仅部分缓解了探索困难，并未解决记忆容量不足的根本问题（Figure 12 vs Figure 13）。这验证了基准设计的有效性：通过精确控制记忆负荷，可以诊断出算法的具体失效维度。

### 离线强化学习基线：Transformer架构的优势与局限

在32个MIKASA-Robo任务的全面评估中（Figure 6, Table 8），所有离线RL模型均无法解决大多数任务，尤其在记忆容量和序列记忆任务上表现惨淡：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/008_Figure_6.jpg]]

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/075_Table_8.jpg]]
*Table 8: Results for Offline RL baselines. The table shows comparison of transformer-based baselines (RATE, DT), behavior cloning (BC), classic Offline RL baselines (CQL), and Diffusion Policy (DP) on all 32 tasks from the MIKASA-Robo benchmark. Results are presented as mean ± sem across the three runs, where each run is averaged over 100 episodes and sem is the standard error of the mean. Training was performed using only RGB observations (two cameras: top view and gripper view) and using sparse rewards (success once condition). The results show that even models with memory (RATE, DT) are not able to solve most of the benchmark problems, which makes it challenging and promising for further validati...*

- **RATE的相对优势**：带有记忆机制的Recurrent Action Transformer（RATE, Ni et al., 2023）在ShellGameTouch-v0（稀疏奖励）上达到0.92±0.01成功率，在RememberColor3-v0上达到0.65±0.01，显著优于BC（0.00）、CQL（0.00）和DP（0.00）。这归因于RATE的Transformer架构能够通过注意力机制直接访问历史token，提供了比LSTM隐状态更灵活的记忆检索。
- **无记忆模型的全面失败**：BC-MLP、CQL-MLP和Diffusion Policy在所有依赖记忆的任务上成功率几乎为零，证实了这些架构缺乏有效的时间信息整合机制。
- **容量与序列任务的零成功率**：在BunchOfColors7-v0、SeqOfColors7-v0、ChainOfColors7-v0等任务上，所有模型（包括RATE）的成功率均为0.00±0.00（Table 8, 任务24-32）。这表明即使是最先进的Transformer记忆架构，在面对高容量或长序列依赖时仍完全失效。

### 视觉-语言-动作模型的记忆缺陷

VLA模型的评估结果（Table 4）进一步揭示了当前大模型在记忆能力上的严重不足：

- **上下文窗口的边际效应**：Octo-small（上下文长度10）在ShellGameTouch（0.46）和InterceptMedium（0.39）上优于随机基线，但在RememberColor5/9上成功率骤降至0.17和0.11。OpenVLA在K=8时RememberColor3可达0.59，但K=4时所有模型表现接近随机。这表明有限的上下文窗口无法有效保留长时记忆信息。
- **架构固有缺陷**：SpatialVLA和π0即使在简单记忆任务上也表现随机，说明当前VLA架构缺乏显式的记忆编码机制，仅依赖前馈处理或短上下文注意力不足以应对记忆密集型场景。

### 真实世界验证：模拟到现实的记忆鸿沟

真实世界RememberColor3-v0实验（Table 10）采用三阶段递增协议隔离混淆因素：
- **Task 1**（完全可观测，无记忆需求）：微调后的π0.5模型触碰正确方块的成功率达1.00，验证了操作执行的可行性。
- **Task 2**（动态干扰控制）：性能略有下降，但仍保持较高水平。
- **Task 3**（完整记忆需求）：触碰成功率骤降至0.10，拾取成功率更低。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_9cLPurIZMj/figures/090_Table_10.jpg]]
*Table 10: Real-world performance of the fine-tuned $\pi _ { 0 . 5 }$ on the three evaluation tasks using 30 episodes per task. For each color and each task, we report the fraction of episodes where the robot touched the correct cube (i$s_$touched) and where it successfully picked it (i$s_$picked)*

这一从1.00到0.10的剧烈衰减，在排除了操作执行和动态干扰因素后，直接归因于记忆需求。它构成了当前VLA模型缺乏长时记忆能力的最直接证据，也验证了MIKASA基准在真实场景中的诊断有效性。

### 失败模式总结

综合以上实验，当前RL和VLA方法在MIKASA基准上呈现三类系统性失败模式：

1. **容量饱和**：LSTM隐状态和Transformer上下文窗口均存在固定容量上限，当记忆项目数（如颜色数）超过阈值时性能崩溃。
2. **序列衰减**：随着需要记忆的事件间隔（ξ）增大，信息保留能力急剧下降，现有架构缺乏有效的长时记忆寻址机制。
3. **检索干扰**：在BunchOfColors等多项目同时记忆任务中，即使单个项目在容量范围内，多项目间的干扰仍导致检索失败，表明缺乏结构化记忆编码。

这些失败模式为未来记忆增强机制的设计提供了明确方向：需要超越固定容量隐状态和有限上下文窗口的架构，引入外部记忆模块、可微分记忆寻址或层次化记忆压缩等机制。

## 方法谱系与知识库定位

### 1. 问题定位：记忆评估的碎片化与缺失

强化学习社区长期缺乏统一的记忆能力评估基准。现有研究在评估记忆增强型智能体时，通常各自开发定制化的环境，导致方法之间无法在同一框架下公平比较。**Table 2** 清晰揭示了这一碎片化格局：25个记忆密集型环境与17个智能体/基准模型之间仅形成稀疏的评估矩阵，多数智能体仅在其原生环境中被验证。更严重的是，大量记忆增强方法（如使用Transformer、外部存储模块的架构）仍被置于Atari等本质上可转化为MDP的任务中测试——通过帧堆叠即可消除部分可观测性，这使得对记忆机制的诊断变得不可靠。

在机器人操作领域，这一空白更为突出。**Table 3** 对主流机器人框架的分析表明，ManipulaTHOR、CALVIN、RLBench等广泛使用的基准几乎不包含需要记忆的任务；即便是近期出现的并发工作，也仅覆盖单一记忆类型。这直接导致了一个关键瓶颈：**我们无法系统回答“当前RL智能体在何种记忆维度上存在缺陷，以及不同记忆增强机制究竟带来了何种增益”**。

### 2. MIKASA的解决方案：分类框架与统一基准

MIKASA的核心贡献在于提供了一个**系统化的记忆任务分类法**和**两个互补的基准**，从而将碎片化的评估统一到可比较的框架下。

**记忆任务分类框架**（Section 4.2）定义了四类记忆需求：

| 记忆类型 | 核心要求 | MIKASA-Robo中的代表性任务 |
|---------|---------|------------------------|
| **对象记忆** (Object Memory) | 记住特定物体的身份或属性 | RememberObject, RememberColor |
| **空间记忆** (Spatial Memory) | 记住物体在遮挡或移动后的位置 | ShellGameTouch, Intercept |
| **序列记忆** (Sequential Memory) | 记住事件发生的顺序 | SeqOfColors, ChainOfColors |
| **容量记忆** (Memory Capacity) | 同时记住多个信息项 | BunchOfColors, RememberColor9 |

这一分类框架的因果杠杆在于：**通过精确控制任务的记忆负荷和类型，可以诊断智能体在不同记忆维度上的优势与不足**。例如，RememberColor3-v0仅要求记住3个颜色-位置关联，属于低容量对象记忆；而BunchOfColors7-v0要求同时维护7个颜色关联，直接测试记忆容量的上限。

**MIKASA-Base**（Section 5）整合了现有开源记忆密集型环境，按诊断性向量环境和复杂图像环境两个层级组织，统一采用Gymnasium标准API。这解决了“各研究使用自定义环境、无法横向比较”的工程瓶颈。

**MIKASA-Robo**（Section 6）则专门针对机器人桌面操作场景，构建了覆盖全部四类记忆的32个任务。其关键设计选择包括：
- **可解性验证**：在状态完全可观（MDP模式）下，PPO-MLP可达100%成功率（Figure 4），证明任务本身可解，记忆需求是唯一瓶颈。
- **多观察模式**：支持state、RGB+joints、RGB-only等模式，允许隔离视觉感知与记忆的交互影响。
- **双奖励函数**：提供密集奖励和稀疏奖励，用于区分探索困难与记忆不足。
- **标准化专家数据集**：提供1000条100%成功率的轨迹，确保离线RL实验的数据分布一致性。

### 3. 与现有方法的谱系关系

**在线RL基线**方面，MIKASA采用PPO-MLP（Schulman et al., 2017）作为无记忆基线，PPO-LSTM（Hochreiter & Schmidhuber, 1997）作为带循环记忆的基线。实验表明，LSTM在短时记忆任务（如RememberColor3）上显著优于MLP，但在长时依赖和高容量任务上同样失败（Figure 12-13），这揭示了**循环架构的记忆容量上限**。

**离线RL基线**方面，MIKASA评估了五类代表性方法：
- **RATE**（Ni et al., 2023）：带记忆的Recurrent Action Transformer，在ShellGameTouch-v0上达0.92成功率，RememberColor3-v0上达0.65，是表现最好的离线模型。
- **DT**（Decision Transformer, Chen et al., 2021）：基于Transformer的序列建模方法，性能显著弱于RATE。
- **BC**（行为克隆）、**CQL**（Kumar et al., 2020）、**DP**（Diffusion Policy）：无显式记忆机制的方法，在绝大多数记忆任务上成功率接近零。

值得注意的是，即便是表现最好的RATE，在BunchOfColors7-v0等容量记忆任务上也完全失败（成功率0.00），而所有模型在序列记忆任务（SeqOfColors, ChainOfColors）上随序列长度增加均急剧退化至零（Table 8）。这指向一个深层缺陷：**当前基于Transformer的序列模型虽然理论上具有长程建模能力，但在实际RL训练中仍无法有效利用长上下文进行记忆检索**。

**视觉-语言-动作（VLA）模型**方面，MIKASA评估了Octo（Team, 2024）、OpenVLA、SpatialVLA、π0.5等前沿模型。Table 4的结果揭示了一个令人警醒的发现：即使在ShellGameTouch和RememberColor3等相对简单的任务上，多数VLA模型的成功率也仅略高于随机策略；在RememberColor9上，所有模型的表现均接近随机水平。真实世界实验（Table 10）进一步验证了这一缺陷：经过微调的π0.5在完整记忆要求的RememberColor3任务上触碰成功率仅0.10，而无记忆要求的控制任务达1.00。

### 4. 适用边界与局限

MIKASA的适用边界需要明确认知：

**已覆盖的范围**：
- 原子性记忆操作任务（单次记忆-召回循环）
- 桌面操作场景（基于ManiSkill3框架）
- 四类记忆需求的独立评估
- 模拟环境中的标准化评估

**明确的局限**（论文已承认）：
1. **任务粒度**：当前任务为原子性操作，尚未涵盖由多个记忆依赖子任务组合而成的长效复合任务。例如，现实中的“记住配方→依次取料→按序加工”需要多种记忆类型的协同，MIKASA尚未覆盖此类场景。
2. **场景普适性**：仅在桌面操作场景中验证，未扩展到移动操作或导航领域。空间记忆在导航中的表现形式（如记住路径拓扑）与桌面操作（如记住遮挡物体位置）可能存在本质差异。
3. **Sim-to-Real差距**：尽管进行了真实世界验证，但任务数量和多样性有限（仅3个RememberColor变体），且真实实验采用三阶段递增协议（Task 1验证执行可行性，Task 2控制动态干扰，Task 3隔离记忆需求），虽能有效隔离混淆因素，但场景丰富度远不及模拟环境。
4. **记忆长度极限**：未评估在极端记忆长度（如数小时跨度）下智能体的表现。当前任务的episode timeout在100-500步之间，远未触及真实应用中的长时记忆需求。
5. **数据分布偏差**：离线数据集仅包含专家级示范，未包含次优或失败轨迹。这可能导致模型在分布外状态下的记忆检索能力被高估——真实场景中智能体往往需要从不完美的历史中提取关键信息。

### 5. 开放问题

基于MIKASA揭示的当前方法缺陷，以下开放问题值得后续研究关注：

**基准扩展方向**：
- 如何将MIKASA扩展到包含自然语言指令的长程任务和移动操作场景？这需要重新定义记忆类型在复合任务中的交互模式。
- 如何设计更细粒度的记忆度量指标？当前仅依赖成功率，无法区分“记住了但执行失败”与“根本没记住”两种失败模式。信息保留时间、记忆干扰度等指标可能提供更丰富的诊断信息。

**算法改进方向**：
- 当前VLA模型在记忆能力上的不足是架构固有缺陷还是训练数据规模不足？Table 4中Octo（上下文长度10）优于OpenVLA（K=4）的趋势暗示上下文窗口大小可能是关键瓶颈，但RATE在长序列任务上同样失败又表明单纯增大窗口并非充分解。
- 如何在有限上下文长度下实现有效的记忆覆盖与选择性遗忘？这涉及记忆管理策略，而非仅仅是记忆容量问题。
- 如何利用MIKASA进行元强化学习研究，评估智能体在不同记忆模式间的快速适应能力？当前基准的任务多样性为此类研究提供了基础。

**部署验证方向**：
- 如何在真实世界环境中部署和评估更大规模的真实机器人记忆任务？Table 10的初步结果已显示sim-to-real差距显著，需要更系统的真实世界验证协议。

## 原文 PDF

![[paperPDFs/ICLR_2026/Memory_Benchmark_Robots_A_Benchmark_for_Solving_Complex_Tasks_with_Reinforcement_Learning.pdf]]
