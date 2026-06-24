---
title: SkillMimic Learning Reusable Basketball Skills from Demonstrations
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations.pdf
aliases:
- SLRBSFD
tags:
- CVPR_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 统一的 HOI 模仿奖励设计，特别是乘法组合子奖励和接触图奖励 (Contact Graph Reward)，能够提供细粒度的接触监督和平衡的优化信号，使策略能够精确模仿参考运动的接触状态和整体交互模式。
primary_logic: 通过将交互技能定义为 HOI 状态转移的集合，并使用统一的 HOI 模仿奖励（乘积形式）来最小化仿真与参考之间的状态差异，可以完全替代针对特定技能的手工奖励，从而实现多种篮球技能的统一学习。接触图 (Contact Graph) 提供了一种简单而有效的接触监督方式，是避免运动学局部最优的关键。
claims:
- SkillMimic 使用统一的 HOI 模仿奖励，无需技能特定奖励即可学习多种篮球技能。
- 接触图奖励对于精确接触模仿至关重要，通过消融实验验证。
- 在高层任务中，基于 SkillMimic 技能先验的方法成功率显著高于从零学习 (PPO) 和使用运动先验 (ASE) 的方法。
- BallPlay-M Heading task 上 Success Rate (%) = 93.04
---

# SkillMimic Learning Reusable Basketball Skills from Demonstrations

> [!tip] 核心洞察
> 通过将交互技能定义为 HOI 状态转移的集合，并使用统一的 HOI 模仿奖励（乘积形式）来最小化仿真与参考之间的状态差异，可以完全替代针对特定技能的手工奖励，从而实现多种篮球技能的统一学习。接触图 (Contact Graph) 提供了一种简单而有效的接触监督方式，是避免运动学局部最优的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | SkillMimic：从演示中学习可重用的篮球技能 |
| 英文题名 | SkillMimic Learning Reusable Basketball Skills from Demonstrations |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://ingrid789.github.io/SkillMimic/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SkillMimic |
| Dataset | BallPlay-M Heading task, BallPlay-M Circling task, BallPlay-M Throwing task, BallPlay-M Scoring task |

> [!tip] 效果简介
> - BallPlay-M Heading task 上，Success Rate (%) 93.04 vs PPO: 0.70, ASE: 0.19 (+92.34 to +92.85)。
> - BallPlay-M Circling task 上，Success Rate (%) 79.92 vs PPO: 11.14, ASE: 4.37 (+68.78 to +75.55)。
> - BallPlay-M Throwing task 上，Success Rate (%) 93.40 vs PPO: 0.00, ASE: 0.00 (+93.40)。

## 概述

### 问题与瓶颈

让物理仿真人形智能体学习多样化的篮球交互技能面临两大核心挑战。其一，传统的人-物交互（Human-Object Interaction, HOI）模仿方法依赖为每种技能单独设计奖励函数，无法以统一方式学习运球、投篮、上篮等差异显著的技能。其二，缺乏有效的接触监督导致策略常陷入**运动学局部最优解**——例如，智能体可能用头部而非手部控制篮球，虽然运动学上接近参考运动，但交互语义完全错误。这两个瓶颈共同制约了技能学习的精确性、可扩展性与泛化能力。

### 核心方法

SkillMimic 针对上述瓶颈提出了一个统一的数据驱动框架。其核心洞察是：**将交互技能定义为 HOI 状态转移的集合，并通过乘积形式的统一 HOI 模仿奖励来最小化仿真与参考之间的状态差异，从而完全替代技能特定的手工奖励**。方法的关键创新在于**接触图（Contact Graph）** 与**接触图奖励（Contact Graph Reward, CGR）**——通过显式建模场景中身体部位与物体之间的接触状态，并以指数形式奖励接触误差的最小化，为策略提供了细粒度的接触监督。消融实验表明，移除 CGR 后成功率骤降至 38.6%，且出现头部控球等非期望行为；而采用乘积而非加法组合子奖励，将成功率从 27.0% 提升至 95.4%，验证了乘法形式对平衡多目标优化信号的关键作用。

在架构层面，SkillMimic 训练一个统一的**交互技能（Interaction Skill, IS）策略**，以 HOI 状态和技能标签（one-hot）为输入，输出 PD 控制器的目标关节角度。单一策略通过技能标签区分不同技能，实现了多技能的联合学习与灵活切换。在此基础上，可训练**高层控制器（High-Level Controller, HLC）** 以技能标签为动作空间，驱动预训练的 IS 策略完成长时序复杂任务。

### 主要结果

在 BallPlay-M 基准的四个高层篮球任务上，基于 SkillMimic 技能先验的方法显著优于从零学习的 PPO 和使用运动先验的 ASE（Peng et al., TOG 2022）：

| 任务 | SkillMimic | PPO | ASE |
|------|-----------|-----|-----|
| Heading | **93.04%** | 0.70% | 0.19% |
| Circling | **79.92%** | 11.14% | 4.37% |
| Throwing | **93.40%** | 0.00% | 0.00% |
| Scoring | **80.25%** | 0.00% | 0.00% |

在单一技能模仿层面，SkillMimic 在投篮、捡球、转身、上篮四项技能上的成功率也全面超越采用 DeepMimic（Peng et al., TOG 2018）和 AMP（Peng et al., TOG 2021）风格奖励的变体方法。此外，捡球技能的泛化性能随训练数据量增加而单调提升：从 1 个片段时的 0.5% 提升至 131 个片段时的 85.6%，表明方法具有良好的数据可扩展性。

### 方法定位

SkillMimic 属于**基于强化学习的物理角色动画**与**人-物交互模仿**的交叉领域。与依赖技能特定奖励的传统方法（如 DeepMimic）不同，SkillMimic 通过统一的乘积奖励设计实现了技能无关（skill-agnostic）的学习。与基于对抗性模仿的 AMP 系列方法相比，SkillMimic 显式引入了接触图监督，有效避免了运动学局部最优问题。在高层任务层面，SkillMimic 提供的交互技能先验相较于 ASE 的运动先验具有更强的任务相关性，使复杂交互任务的策略学习成为可能。

## 背景与动机

### 人-物交互技能学习的核心挑战

让物理仿真环境中的人形代理掌握复杂的物体交互技能，是具身智能领域的长期目标。篮球运动因其高度动态的全身协调、精细的手-球接触以及多样化的技能类型（如运球、投篮、上篮），成为检验交互技能学习能力的理想试验场。然而，传统方法在学习此类技能时面临两个根本性瓶颈。

**瓶颈一：奖励设计的不可扩展性。** 主流的物理角色动画方法，如 **DeepMimic**（Peng et al., TOG 2018）和 **AMP**（Peng et al., TOG 2021），虽然能够通过模仿学习生成高质量的运动，但其奖励机制并非为统一的 HOI 交互而设计。DeepMimic 依赖手工定义的运动学奖励项，AMP 则采用对抗式运动模仿，两者均缺乏对物体接触状态的显式建模。在实际应用中，这意味着研究者需要为每一种技能（运球、投篮、捡球等）单独设计奖励函数，技能之间无法共享优化信号，导致系统难以扩展到多样化的技能集合。

**瓶颈二：接触监督缺失导致的运动学局部最优。** 在缺乏有效接触监督的情况下，强化学习策略往往会收敛到运动学上的“捷径”。例如，代理可能使用头部而非手来控制球，或用手腕而非手掌接触物体——这些行为在运动学误差度量下可能得分不低，但从交互语义上看是完全错误的。这种现象被称为 **运动学局部最优解**（kinematic local-optimal solutions），其根源在于传统的模仿奖励仅关注身体关节的位置和速度，而忽略了“谁接触了谁”这一交互的本质信息。

### 现有方法的缺口

| 方法 | 奖励机制 | 接触建模 | 技能扩展性 |
|------|----------|----------|------------|
| DeepMimic* | 手工运动学奖励（加和组合） | 无显式建模 | 每技能单独设计 |
| AMP* | 对抗式运动模仿 | 无显式建模 | 每技能单独训练 |
| ASE | 运动先验（locomotion prior） | 仅身体运动 | 仅运动技能 |

上述方法的共同缺陷可归结为两点：（1）**缺乏统一的 HOI 模仿奖励**，无法用同一套奖励函数学习多种交互技能；（2）**缺乏细粒度的接触监督**，导致策略无法精确模仿参考运动中的接触模式。这使得现有工作在面对篮球这类需要精细手-物交互的任务时，要么失败，要么需要大量技能特定的工程调优。

### 本文动机与核心思路

SkillMimic 的提出正是为了填补上述缺口。其核心动机是：**如果能够设计一种统一的、数据驱动的 HOI 模仿奖励，使其同时包含身体运动学、物体运动学和接触状态的监督信号，那么就可以用单一策略学习多种交互技能，而无需任何技能特定的奖励设计。**

为实现这一目标，SkillMimic 引入了两个关键机制：

1. **乘法组合的 HOI 模仿奖励**：将身体运动学、物体运动学、相对运动、速度正则化和接触图五类子奖励以乘积形式组合（$r_t = r_t^{b} * r_t^{o} * r_t^{rel} * r_t^{reg} * r_t^{cg}$）。乘积形式迫使策略在所有子奖励上同时表现良好，避免加法组合中“某些项得分高即可掩盖其他项失败”的问题。

2. **接触图（Contact Graph）与接触图奖励（CGR）**：将场景中的接触关系建模为图结构，节点表示身体部位或物体，边表示两者是否接触。通过最小化仿真与参考之间的接触图状态误差（$E_{\mathrm{cg}} = \frac{1}{N} \sum_{t=1}^{N} \mathrm{MSE}(s_t^{cg}, \hat{s}_t^{cg})$），策略获得了明确的接触监督信号，从而有效避免了运动学局部最优解。

通过这两个机制，SkillMimic 首次实现了在统一框架下学习多种篮球交互技能——包括运球、投篮、上篮和捡球——并支持技能间的灵活切换与组合，为后续的高层任务学习提供了可重用的技能先验。

## 核心创新

### 瓶颈突破：从技能特定奖励到统一 HOI 模仿框架

传统人-物交互（HOI）模仿方法面临一个根本性瓶颈：**每种交互技能都需要单独设计奖励函数**。以篮球技能为例，投篮、运球、上篮等动作的物理约束和接触模式差异巨大，手工为每种技能编写奖励不仅工程量大，更关键的是难以在统一的策略框架下同时优化。此外，现有方法普遍缺乏有效的接触监督——当智能体仅凭运动学相似性进行模仿时，极易陷入**运动学局部最优解**（kinematic local-optima），例如用头部而非手部控制篮球，导致交互行为在视觉上“像”但物理上完全错误。

SkillMimic 的核心突破在于：**将交互技能重新定义为 HOI 状态转移的集合**，并设计了一套**统一的、乘积形式的 HOI 模仿奖励**，完全消除了对技能特定奖励的依赖。这一设计使得单一策略能够从纯数据驱动的角度学习多种篮球交互技能，并在技能间灵活切换。

### 关键控制变量：乘积奖励与接触图监督

SkillMimic 的方法创新可归结为三个关键的 changed slots，每一项都有明确的消融证据支撑：

**1. 乘积组合的模仿奖励（乘法 vs. 加法）**

传统方法将多个模仿子奖励简单相加（additive combination），这会导致优化信号被主导项淹没——例如身体运动学误差远大于物体接触误差时，策略会忽略精细的交互约束。SkillMimic 采用**乘积形式**组合五个子奖励：

$$r_t = r_t^{b} * r_t^{o} * r_t^{rel} * r_t^{reg} * r_t^{cg}$$

其中 $r_t^{b}$（身体运动学）、$r_t^{o}$（物体运动学）、$r_t^{rel}$（相对运动）、$r_t^{reg}$（速度正则化）和 $r_t^{cg}$（接触图）以乘法耦合。这种设计的因果机制在于：**任何一个子奖励的失效都会导致整体奖励归零**，迫使策略在所有维度上同时达到高保真模仿，而非选择性优化。

消融实验（Table 1）给出了决定性证据：在 GRAB 数据集上，乘积奖励的准确率达 95.4%，而改用加法组合（w/o Multiplication）后骤降至 27.0%，接触误差 $E_{cg}$ 从 0.026 飙升至 0.724。这表明乘法机制是平衡多目标优化的关键控制变量。

**2. 接触图奖励（CGR）：避免运动学局部最优的核心监督**

接触图（Contact Graph, Figure 4）将场景中的接触关系建模为图结构：节点存储该部位是否与其他节点接触的二值状态，边存储两个连接节点之间是否存在接触。对于篮球场景，SkillMimic 定义了三个节点——双手（hands）、手部以外的身体（hands-exclusive body）和球（ball），形成简洁而通用的接触表征。

接触图奖励定义为指数形式的加权接触误差：

$$r_t^{cg} = \exp\left( - \sum_{j=1}^{J} \lambda^{cg}[j] \cdot e_t^{cg}[j] \right)$$

其中 $\lambda^{cg}[j]$ 为不同接触元素的敏感度权重，$e_t^{cg}[j]$ 为当前帧的接触图误差。

CGR 的因果作用在消融实验中得到了充分验证（Table 1, Figure 5）：去掉 CGR 后，GRAB 数据集准确率降至 38.6%，接触误差 $E_{cg}$ 增至 0.337。更关键的是，定性结果（Figure 5）揭示了无 CGR 时的典型失败模式——智能体用头部辅助控球、用手腕而非手掌接触物体、无法接住物体、甚至用手支撑桌面保持平衡。CGR 通过提供**帧级别的细粒度接触监督**，直接切断了这些运动学局部最优解的优化路径。

**3. 技能条件化的单一策略架构**

SkillMimic 采用单一交互技能（IS）策略，通过输入技能标签（one-hot encoding）区分不同技能，实现多技能在统一策略下的联合学习。策略以 HOI 状态 $\mathbf{s}_t = \{ \mathbf{o}_t^{prop}, \mathbf{o}_t^{f}, \mathbf{o}_t^{obj} \}$ 和技能标签 $c_j$ 为输入，输出 PD 控制器的目标关节角度。这种设计使得技能间的知识共享成为可能，同时支持高层控制器通过切换技能标签实现复杂任务的技能组合。

### 证据强度总结

| 创新要素 | 核心因果机制 | 关键证据 | 置信度 |
|---------|------------|---------|--------|
| 乘积奖励 | 多目标强制平衡优化，避免信号淹没 | Table 1: 乘积 95.4% vs. 加法 27.0% | 高 |
| 接触图奖励 (CGR) | 帧级接触监督，阻断运动学局部最优 | Table 1 + Figure 5: 去 CGR 降至 38.6%，定性展示失败模式 | 高 |
| 技能条件化策略 | 统一策略下的多技能联合学习与切换 | Table 2: 四项技能成功率 79.6%–99.1%，显著优于 DeepMimic* 和 AMP* | 高 |

上述三项创新共同构成了 SkillMimic 的方法论核心：乘积奖励提供全局优化约束，接触图奖励提供局部接触精度，技能条件化实现多技能的规模化学习。三者缺一不可，消融实验已充分证明了每一项的独立贡献。

## 整体框架

SkillMimic 的系统设计遵循**数据驱动、技能无关、可扩展**的核心原则，旨在通过统一的模仿学习框架，使物理仿真人形机器人从 HOI 运动数据中学习多样化的篮球交互技能。整个 pipeline 由三个紧密衔接的模块构成，如图 Figure 3 所示。

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/003_Figure_3.jpg]]
*Figure 3: Our system consists of three parts. (a) First, we capture real-world basketball skills to create a large Human-Object Interaction (HOI) motion dataset. (b) Second, we train an Interaction Skill (IS) policy to learn interaction skills by imitating the corresponding HOI data through reinforcement learning. Specifically, the IS policy takes as input the HOI state*

### 1. HOI 数据收集与预处理

系统首先构建一个技能标注的 HOI 运动数据集。通过从真实世界捕获或估计篮球交互运动数据，将原始运动分割为带有技能标签的 HOI 片段。每个片段对应一种特定技能（如投篮、运球、捡球），其核心定义是：**一种交互技能被视作一组与预期技能语义对齐的 HOI 状态转移集合**（Figure 2）。这一阶段为后续的模仿学习提供了参考运动轨迹和接触状态真值。

### 2. 交互技能 (IS) 策略训练

IS 策略是 SkillMimic 的核心低层控制器，其训练流程如下：

- **输入**：策略在时间步 $t$ 接收 HOI 状态 $\mathbf{s}_t$ 和技能标签 $c_j$（one-hot 编码）。HOI 状态定义为 $\mathbf{s}_t = \{ \mathbf{o}_t^{prop}, \mathbf{o}_t^{f}, \mathbf{o}_t^{obj} \}$，分别包含人形代理的本体感知（关节角度、速度等）、净接触力感知以及物体状态（位置、速度等）。
- **网络结构**：策略输出建模为与机器自由度维度相同的高斯分布（常数方差），其均值由一个三层 MLP [1024, 512, 512] 加 ReLU 激活函数参数化。
- **动作执行**：从策略中采样的动作 $\mathbf{a}_t$ 作为全套 PD 控制器的目标关节角度，驱动仿真人形机器人与物体交互。
- **奖励驱动**：仿真器计算出新的 HOI 状态 $\mathbf{s}_{t+1}$ 后，由**统一 HOI 模仿奖励模块**计算乘积形式的复合奖励 $r_t = r_t^{b} * r_t^{o} * r_t^{rel} * r_t^{reg} * r_t^{cg}$，分别对应身体运动学、物体运动学、相对运动、速度正则化和接触图 (Contact Graph) 五个子奖励。其中，**接触图奖励 (CGR)** 是避免运动学局部最优解（如用头部控制球）的关键设计。
- **学习方式**：SkillMimic 仅使用状态轨迹（state-only trajectories）通过强化学习学习动作，这使其对数据噪声具有更好的容忍度，同时数据效率更高。单一策略通过输入不同的技能标签，即可联合学习多种技能并支持技能间的灵活切换。

### 3. 高层控制器 (HLC)

在 IS 策略完成多种交互技能的学习后，系统训练一个高层控制器（HLC）来实现复杂长程任务的技能组合。HLC 以当前 HOI 状态和任务观测 $\mathbf{h}_t$ 为输入，输出一个离散的技能嵌入，该嵌入作为预训练 IS 策略的输入，驱动低层技能的执行。例如，在“连续得分”任务中，HLC 需要依次调度“捡球”、“运球”、“投篮”等技能。据论文报告，一个可用的 Scoring 任务 HLC 仅需在单张 NVIDIA RTX 4090 GPU 上训练约 3 小时。

### 模块间的信息流

整体信息流可概括为：**真实世界捕获 → HOI 片段数据集 → IS 策略（RL 模仿学习 + 统一乘积奖励 + 接触图监督）→ 多技能策略 → HLC（任务级调度）→ 复杂任务执行**。这一设计使得 SkillMimic 能够完全摒弃针对特定技能的手工奖励函数，在统一配置下以纯数据驱动的方式掌握几乎涵盖所有基础篮球技能的动作库（Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/001_Figure_1.jpg]]
*Figure 1: We propose a novel approach that for the first time enables physically simulated humanoids to learn a variety of basketball interaction skills from Human-Object Interaction (HOI) data, including but not limited to shooting (blue), retrieving (red), and turnaround layup (yellow). Once acquired, these interaction skills can be composed to accomplish complex tasks, such as consecutive scoring (green)*

## 核心模块与公式推导

SkillMimic 的系统框架由三个核心模块构成：HOI 数据收集与预处理、交互技能策略训练、以及高层控制器。其中，交互技能策略训练是整个方法的核心，其关键在于一个统一的 HOI 模仿奖励设计与接触图建模。

### 交互技能策略

交互技能策略是一个基于强化学习的低层策略，其目标是通过模仿参考 HOI 运动片段来学习交互技能。策略以当前 HOI 状态和技能标签作为输入，输出人形机器人的目标关节角度，由 PD 控制器执行。

**状态空间** 定义为：

$$\mathbf{s}_t = \{ \mathbf{o}_t^{prop}, \mathbf{o}_t^{f}, \mathbf{o}_t^{obj} \}$$

其中 $\mathbf{o}_t^{prop}$ 为人形代理的本体感知信息，$\mathbf{o}_t^{f}$ 为各身体链节受到的净接触力，$\mathbf{o}_t^{obj}$ 为物体的位置、朝向、线速度与角速度等状态。技能标签 $c_j$ 以 one-hot 向量形式输入，使单一策略能够同时学习多种技能并在推理时灵活切换。

策略输出建模为一个固定方差的高斯分布，其均值由三层 MLP（隐藏层维度 [1024, 512, 512]，ReLU 激活）参数化。从该分布采样得到的动作 $\mathbf{a}_t$ 作为全套 PD 控制器的目标关节旋转角。

### 统一 HOI 模仿奖励

SkillMimic 的核心创新在于使用乘积形式的统一 HOI 模仿奖励，完全替代了传统方法中为每种技能单独设计的手工奖励函数。该奖励定义为：

$$r_t = r_t^{b} \cdot r_t^{o} \cdot r_t^{rel} \cdot r_t^{reg} \cdot r_t^{cg}$$

各子奖励的含义如下：

- **$r_t^{b}$（身体运动学奖励）**：衡量仿真人形与参考运动中身体关节位置、旋转、速度等运动学量的匹配程度。
- **$r_t^{o}$（物体运动学奖励）**：衡量仿真物体与参考物体在位置、朝向、线速度、角速度上的匹配程度。
- **$r_t^{rel}$（相对运动奖励）**：衡量人形末端执行器（如双手）与物体之间相对位置和相对朝向的匹配程度，确保交互的空间关系正确。
- **$r_t^{reg}$（速度正则化奖励）**：惩罚异常大的关节速度，提升运动的自然度和稳定性。
- **$r_t^{cg}$（接触图奖励）**：衡量仿真与参考之间接触状态的匹配程度，是避免运动学局部最优解的关键组件。

**乘积形式的设计动机**：消融实验表明，乘法组合优于加法组合。在 GRAB 数据集上，乘积奖励的准确率达到 95.4%，而加法组合（w/o Multiplication）仅为 27.0%，接触误差 $E_{\mathrm{cg}}$ 从 0.026 急剧增大至 0.724。乘积形式强制所有子奖励同时保持较高水平，避免了某一子奖励极高而其他子奖励极低时策略仍能获得高总奖励的“作弊”行为——这正是加法组合容易陷入局部最优的根本原因。

### 接触图与接触图奖励

接触图是 SkillMimic 中实现精确接触监督的关键结构。它将场景中的接触关系建模为一个图：节点存储一个二值量，表示该节点是否与其他节点接触；边存储一个二值量，表示两个相连节点之间是否存在接触。对于篮球技能，定义了三个节点：双手、双手以外的身体、篮球，构成一个简单的接触图来统一建模多样化的接触模式。

**接触图奖励** 定义为指数形式的加权误差：

$$r_t^{cg} = \exp\left( - \sum_{j=1}^{J} \lambda^{cg}[j] \cdot e_t^{cg}[j] \right)$$

其中 $e_t^{cg}[j]$ 为第 $j$ 个接触元素的误差（仿真与参考接触状态的差异），$\lambda^{cg}[j]$ 为对应的独立权重，用于调节对不同接触元素的敏感度。指数形式将加权误差映射到 (0, 1] 区间，误差越小奖励越接近 1。

**接触图奖励的关键作用**：消融实验表明，去掉接触图奖励后，GRAB 数据集上的准确率从 95.4% 骤降至 38.6%，接触误差 $E_{\mathrm{cg}}$ 从 0.026 增大至 0.337。定性结果显示，无接触图奖励时策略会陷入运动学局部最优解——例如用头部辅助控球、用手腕而非手掌接触球、抓取物体失败、或借助桌面保持平衡。接触图奖励通过提供细粒度的接触监督信号，有效引导策略学习精确的交互行为。

**接触误差评估指标** 定义为参考接触图状态与仿真接触图状态在 $N$ 帧上的均方误差：

$$E_{\mathrm{cg}} = \frac{1}{N} \sum_{t=1}^{N} \mathrm{MSE}(s_t^{cg}, \hat{s}_t^{cg})$$

该指标取值范围为 [0, 1]，用于量化接触模仿的精度。

### 高层控制器

在完成交互技能策略的训练后，SkillMimic 引入一个高层控制器来复用已学技能以完成复杂的长程任务。高层控制器以当前 HOI 状态和任务观测 $\mathbf{h}_t$ 为输入，输出一个离散的技能标签，该标签作为预训练 IS 策略的输入，驱动人形执行相应的交互技能。通过这种方式，复杂的任务被分解为一系列技能的组合与切换，显著降低了高层任务的学习难度。例如，在 Scoring 任务中，仅需约 3 小时的 RTX 4090 GPU 训练即可获得表现良好的高层控制器。

### 补充图表

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/004_Figure_4.jpg]]
*Figure 4: We propose the Contact Graph (CG) to model general contacts within an explicitly defined scene. The node stores a binary value that denotes whether it contacts other nodes. Each edge stores a binary value indicating whether the two connected nodes are in contact. The node definition is unified for a certain scene and shared between diverse interactive skills. For example, we define three nodes: hands, hands-exclusive body, and ball, to form a simple CG to model contacts for diverse basketball skills*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/005_Figure_5.jpg]]
*Figure 5: The HOI imitation falls into kinematic local-optimal solutions without Contact Graph Reward (CGR): (b) use the head to help control the ball; (e) use the wrist to contact the ball; (h) fail to catch the object; (k) support the table to keep balance. In comparison, the guidance of CGR effectively yields precise interactions, as shown in (c, f, i, l)*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/002_Figure_2.jpg]]
*Figure 2: Concept of SkillMimic. We define an interaction skill as a set of Human-Object Interaction (HOI) state transitions that align with the intended skill semantics. These state transitions can be derived from captured HOI motion clips. If a simulated humanoid can manipulate objects such that the resulting HOI state transitions closely match those of the reference, we consider the humanoid to have successfully learned the interaction skill*

## 实验与分析

### 统一 HOI 模仿奖励的消融实验

SkillMimic 的核心贡献之一是提出了乘积形式的统一 HOI 模仿奖励，其设计决策通过严格的消融实验得到验证。实验在 GRAB 和 BallPlay-V 两个数据集上进行，评估指标包括成功率 (Acc.)、身体运动学误差 (E_b-mpjpe)、物体运动学误差 (E_o-mpjpe) 和接触误差 (E_cg)。

**乘法组合 vs. 加法组合。** 乘积奖励是 SkillMimic 取得高精度模仿的关键。当将所有子奖励从乘积改为加和形式（w/o Multiplication）时，GRAB 数据集上的成功率从 95.4% 骤降至 27.0%，接触误差 E_cg 从 0.026 急剧恶化至 0.724（Table 1）。这表明乘法组合通过子奖励间的联合约束，有效避免了优化过程中某一维度奖励被其他维度主导的问题，提供了更平衡的优化信号。

**接触图奖励 (CGR) 的关键作用。** 移除接触图奖励（w/o CGR）后，GRAB 数据集成功率降至 38.6%，接触误差 E_cg 升至 0.337。更关键的是，定性结果（Figure 5）揭示了缺乏 CGR 时策略会陷入运动学局部最优解：仿人代理使用头部辅助控制球、用手腕而非手掌接触球、无法成功接住物体、甚至依靠支撑桌面来维持平衡。加入 CGR 后，这些非期望行为被有效消除，交互变得精确。这验证了接触图作为一种简单而有效的接触监督形式，是避免运动学局部最优的关键机制。

### 篮球技能学习的主结果

SkillMimic 在 BallPlay-M 基准的四种典型篮球技能上与两种变体方法进行了对比：DeepMimic*（使用类似 DeepMimic 的运动学模仿奖励，Peng et al., TOG 2018）和 AMP*（使用类似 AMP 的对抗性模仿奖励，Peng et al., TOG 2021）。所有方法在相同的物理仿真环境（Isaac Gym）和计算资源下评估。

**Table 2** 报告了各技能的成功率：

| 技能 | DeepMimic* | AMP* | SkillMimic (Ours) |
|------|-----------|------|-------------------|
| Pick Up | 0.0% | 0.0% | **86.7%** |
| Dribble Forward | 0.0% | 0.0% | **79.6%** |
| Layup | 0.0% | 0.0% | **99.1%** |
| Shot | 0.0% | 0.0% | **97.9%** |

DeepMimic* 和 AMP* 在所有技能上均完全失败（0.0% 成功率），而 SkillMimic 取得了 79.6%–99.1% 的高成功率。这一巨大差距源于两种基线方法的根本局限：DeepMimic* 的运动学奖励缺乏对物体交互和接触的显式建模，AMP* 的对抗性奖励在 HOI 场景下难以提供足够细粒度的接触监督。SkillMimic 通过统一的乘积奖励和接触图奖励，同时优化身体运动学、物体运动学和接触状态，从而实现了精确的交互技能模仿。

### 技能泛化性分析

**捡球技能的泛化能力。** Figure 7 展示了从 40 个 HOI 运动片段学习的捡球技能的泛化表现：仿人代理不仅能轻松捡起静止球，还能拦截随机速度的来球，甚至在首次接触失败后（蓝色帧）调整姿态并在第二次尝试中成功取回球。Figure 8 定量分析了训练数据规模对泛化性能的影响：仅用 1 个片段时成功率为 0.5%，40 个片段提升至 76.5%，131 个片段达到 85.6%。这表明 SkillMimic 能够通过增加数据规模持续提升技能鲁棒性和泛化能力，但当前泛化仍受限于已有数据的覆盖范围。

### 高层任务中的技能组合

SkillMimic 学习到的交互技能可作为技能先验，供高层控制器 (HLC) 组合使用以完成复杂长程任务。Table 3 对比了三种方法在四个高层篮球任务上的成功率：

| 任务 | PPO (从零学习) | ASE (运动先验) | ASE* (身体+物体运动先验) | SkillMimic (Ours) |
|------|:---:|:---:|:---:|:---:|
| Heading | 0.70% | 0.19% | — | **93.04%** |
| Circling | 11.14% | 4.37% | — | **79.92%** |
| Throwing | 0.00% | 0.00% | 0.00% | **93.40%** |
| Scoring | 0.00% | 0.00% | 0.00% | **80.25%** |

PPO（从零开始训练）和 ASE（使用运动先验，Peng et al., TOG 2022）在所有任务上基本无法收敛。即使扩展 ASE 为 ASE*（同时使用身体和物体运动先验），在 Throwing 和 Scoring 任务上成功率仍为 0.00%。相比之下，基于 SkillMimic 技能先验的方法在所有任务上均取得高成功率（79.92%–93.40%）。这证明统一的 HOI 模仿学习所获得的交互技能先验，其质量远超通用的运动先验，是完成复杂 HOI 任务的关键基础。

### 失败模式与局限性

尽管 SkillMimic 在篮球技能学习上表现优异，仍存在以下局限：

1. **数据依赖性。** 方法依赖大量高质量 HOI 运动数据，需要动作捕捉系统采集，成本较高。当训练数据不足时（如 Figure 8 中 1 个片段仅 0.5% 成功率），技能泛化能力显著受限。
2. **场景限制。** 当前仅支持单人单球的交互场景，无法处理多智能体或多物体交互。
3. **仿真依赖。** 接触图奖励依赖仿真环境中的精确物体状态与接触信息，这些特权信息在真实机器人应用中难以直接获取。
4. **技能覆盖受限。** 技能的泛化能力受限于已有数据的覆盖范围，对未见物体或新技能需要额外数据采集。

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/010_Figure_8.jpg]]
*Figure 8: Pickup generalization performance with different training data scales. First number: clips; second: success rate. In each test, 1000 balls are randomly placed within 1 to 5 meters away from the center. Yellow dots indicate successful pickups and green dots represent failures. See Sec. 4.2 for details*

### 补充图表

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/009_Table_2.jpg]]
*Table 2: Success rates across four typical basketball skills in BallPlay-M. Our method significantly outperforms variant methods that use imitation reward styles of DeepMimic and AMP*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/008_Figure_7.jpg]]
*Figure 7: Demonstration of the pickup skill learned from 40 HOI motion clips. Yellow denotes the initial frame. Left: The humanoid picks up a stationary ball effortlessly. Middle: The humanoid intercepts a ball with random velocity. Right: The humanoid adjusts after missing the ball initially (the frame in blue) and successfully retrieves it on the second attempt, showcasing the potential for learning robust and generalizable skills through extensive data collection*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/012_Figure_9.jpg]]
*Figure 9: Our method supports training a single IS policy under a unified configuration to acquire various interaction skills. These interaction skills can be flexibly switched, as illustrated in (a), where yellow denotes shot, blue denotes pickup, and green denotes turnaround layup. Complex, long-horizon tasks can be easily achieved by training a high-level controller (HLC) to manage switching of the learned interaction skills: (b) scoring from random positions (c) dribbling to target locations, and (d) dribbling along an expanding radius*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/006_Figure_6.jpg]]
*Figure 6: Simulated humanoids exhibit comprehensive basketball skills. SkillMimic can teach humanoids a wide range of basketball skills using the same configuration in a purely data-driven manner, covering almost all fundamental basketball skills. Keyframes are placed in chronological order from left to right*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/011_Figure.jpg]]
*Figure: (a) Manual Control (b) Scoring (c) Heading (d) Circling*

![[assets/figures/papers/paper_list_l1749_SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations/figures/007_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

SkillMimic 针对的是物理仿真人形智能体学习人-物交互（HOI）技能时的两个相互纠缠的根本困难：

**瓶颈一：技能特定奖励的不可扩展性。** 传统 HOI 模仿方法（如 **DeepMimic** (Peng et al., TOG 2018) 和 **AMP** (Peng et al., TOG 2021) 的 HOI 扩展版本）需要为每种交互技能单独设计奖励函数。当技能种类增加时，手工设计奖励的工作量急剧膨胀，且不同技能奖励之间的优化目标可能相互冲突，导致无法用一个统一策略学习多样化技能。

**瓶颈二：缺乏有效接触监督导致的运动学局部最优。** 在仅依赖运动学误差（如关节角度、末端执行器位置）的模仿学习中，策略容易收敛到“视觉上相似但物理上错误”的解。典型失败模式包括：用头部辅助控制球、用手腕而非手掌触球、抓取失败后无法恢复。这些局部最优解在运动学指标上可能表现尚可，但完全丧失了交互的物理正确性。

**因果机制：** SkillMimic 通过两个关键设计切断了上述因果链：
1. **乘法组合奖励**将身体运动学、物体运动学、相对运动、速度正则化和接触图五个子奖励以乘积形式组合（$r_t = r_t^{b} * r_t^{o} * r_t^{rel} * r_t^{reg} * r_t^{cg}$）。乘法形式迫使策略在所有子奖励维度上同时表现良好——任何一个维度失效都会导致整体奖励趋零，从而避免了加法组合中“部分维度高分补偿其他维度低分”的优化漏洞。
2. **接触图奖励（CGR）** 通过显式建模场景中关键节点（如手、手以外的身体、球）之间的二元接触状态，提供细粒度的接触监督信号。CGR 直接惩罚“用错误身体部位接触物体”的行为，从根本上阻断了运动学局部最优的产生路径。

### 2. 与基线方法的关系定位

SkillMimic 在 HOI 模仿学习的方法谱系中占据“统一数据驱动 HOI 技能学习”的位置，与以下基线形成清晰对比：

| 方法 | 奖励设计 | 接触建模 | 技能泛化 | 核心局限 |
|------|---------|---------|---------|---------|
| **DeepMimic\*** (Peng et al., TOG 2018) | 技能特定手工奖励 | 无显式接触奖励 | 单技能策略 | 不可扩展至多技能 |
| **AMP\*** (Peng et al., TOG 2021) | 对抗性运动模仿奖励 | 无显式接触奖励 | 单技能策略 | 接触精度无保证 |
| **ASE** (Peng et al., TOG 2022) | 运动先验引导的任务奖励 | 无接触建模 | 仅运动先验，无物体交互 | 无法处理 HOI 任务 |
| **SkillMimic** | 统一乘积形式 HOI 模仿奖励 | 接触图 + CGR | 单一策略多技能 + 技能切换 | 依赖高质量 HOI 数据 |

**关键区分点：**
- 与 DeepMimic\* 和 AMP\* 相比，SkillMimic 用统一的乘积奖励替代了技能特定奖励，使得单一策略可以同时掌握多种技能（如 Pick Up、Dribble Forward、Layup、Shot），并在技能之间灵活切换。
- 与 ASE 相比，SkillMimic 的技能先验同时包含身体运动和物体交互信息，而 ASE 仅提供运动先验。在高层任务（如 Scoring、Throwing）中，ASE 的成功率为 0%，而 SkillMimic 达到 80%–93%，证明了交互技能先验对于复杂 HOI 任务的必要性。

### 3. 方法适用边界

**适用场景：**
- 单人-单物交互场景，且交互物体的几何和物理属性在训练数据覆盖范围内。
- 可通过动作捕捉或状态估计获取高质量 HOI 状态序列的任务。
- 仿真环境中可获取精确物体状态和接触力信息的场景（利用特权信息训练）。

**不适用或需谨慎的场景：**
- **多智能体/多物体交互：** 当前框架仅支持单人与单球的交互，无法处理传球配合或多个物体同时操作的场景。
- **未知物体几何：** 技能的泛化能力受限于训练数据的物体覆盖范围，对全新形状或物理属性的物体需要额外数据。
- **真实机器人直接部署：** 方法依赖仿真环境中的精确物体状态和接触力信息作为策略输入，这些“特权信息”在真实机器人上难以直接获取，需要额外的感知模块或 sim-to-real 迁移技术。

### 4. 局限与开放问题

**已知局限：**
1. **数据依赖性强：** 方法需要大量高质量 HOI 运动数据，数据采集依赖动作捕捉系统，成本高且覆盖场景有限。消融实验显示 Pickup 技能在仅 1 个训练片段时成功率仅 0.5%，需要 40+ 片段才能达到实用水平（76.5%）。
2. **仿真-现实差距：** 运动重定向、接触动力学建模误差、状态估计噪声等问题使得从仿真到真实人形机器人的迁移仍是一个开放挑战。
3. **接触图定义需人工设计：** 接触图的节点和边需要针对特定场景手动定义（如篮球场景定义手、手以外身体、球三个节点），对于更复杂的多物体场景，图结构设计本身可能变得复杂。

**开放问题：**
1. **去特权化感知：** 如何在不依赖仿真特权信息（精确物体位姿、接触力）的情况下，仅通过视觉或触觉传感器实现同等的接触模仿精度？
2. **跨物体泛化：** 如何学习与不同几何形状、物理属性物体交互的通用技能，使策略在遇到新物体时无需重新训练？
3. **数据效率提升：** 在有限 HOI 数据下如何提升技能鲁棒性？数据增强、运动生成模型或 few-shot 适应是否可行？
4. **语言/语义条件控制：** 如何融合更细粒度的控制条件（如自然语言指令“用左手运球绕过障碍物”），实现更灵活的人机交互控制？
5. **多智能体扩展：** 如何将框架扩展至多人协作/对抗场景（如传球、防守），同时保持接触监督的有效性？

## 原文 PDF

![[paperPDFs/CVPR_2025/SkillMimic_Learning_Reusable_Basketball_Skills_from_Demonstrations.pdf]]
