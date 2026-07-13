---
title: "ARM-FM: Automated Reward Machines via Foundation Models for Compositional Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ARM_FM_Automated_Reward_Machines_via_Foundation_Models_for_Compositional_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- AFARMFM
- ARM-FM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "用基础模型从自然语言任务自动生成语言对齐奖励机构。"
primary_logic: "ARM-FM先生成LARM结构、标签函数和状态指令，再用状态语言嵌入条件化RL策略并提供稠密奖励。"
claims:
- "LARM为每个奖励机构状态加入自然语言指令和嵌入，使策略能够按当前子目标语义行动。"
- "生成器和评论家基础模型通过自我改进从任务提示和视觉观察生成可执行奖励机构。"
- "在MiniGrid长时域任务中，ARM-FM是唯一能解决全部评估任务并接近完美奖励的方法。"
- "完整的LARM奖励加状态嵌入在多任务XLand-MiniGrid中比单独组件更稳定。"
---

# ARM-FM: Automated Reward Machines via Foundation Models for Compositional Reinforcement Learning

> [!tip] 核心洞察
> 将基础模型的高层推理能力与奖励机构（RM）的形式化结构相结合：FM自动将自然语言任务描述分解为有限状态自动机，每个状态关联一个语言嵌入，使得策略可以基于当前子目标的语义嵌入进行条件化，从而在共享的语义技能空间中实现经验复用和零样本泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ARM-FM：基于基础模型的自动化奖励机构用于组合强化学习 |
| 英文题名 | ARM-FM: Automated Reward Machines via Foundation Models for Compositional Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=OBpQdCWLfd) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ARM-FM (Automated Reward Machines via Foundation Models) |
| Dataset | MiniGrid-DoorKey (固定地图), MiniGrid-DoorKey (程序生成地图), MiniGrid-UnlockToUnlock, MiniGrid-BlockedUnlockPickup |

> [!tip] 效果简介
> - MiniGrid-DoorKey (固定地图) 上，累积奖励 为 持续高于基线，对比 DQN, DQN+ICM, ReAct均显著较低，变化 显著提升。
> - MiniGrid-DoorKey (程序生成地图) 上，累积奖励 为 持续高于基线，对比 DQN, DQN+ICM, ReAct均显著较低，变化 显著提升。
> - MiniGrid-UnlockToUnlock 上，累积奖励 为 近乎完美奖励，对比 DQN, DQN+ICM, ReAct均无学习，变化 从0到近乎完美。

## 概要

本文提出 **ARM-FM (Automated Reward Machines via Foundation Models)**，一个利用基础模型（FM）自动生成**语言对齐奖励机构（Language-Aligned Reward Machines, LARM）** 的框架，用于组合强化学习中的自动化奖励设计。核心思想是将基础模型的高层推理能力与奖励机构（Reward Machine, RM）的形式化结构相结合：FM自动将自然语言任务描述分解为有限状态自动机，每个状态关联一个语言嵌入，使得策略可以基于当前子目标的语义嵌入进行条件化，从而在共享的语义技能空间中实现经验复用和零样本泛化。

ARM-FM在多个基准上取得了显著成果：在MiniGrid的DoorKey任务中持续优于所有基线方法；在UnlockToUnlock、BlockedUnlockPickup和KeyCorridor三个复杂长时域任务中，是唯一能解决所有任务并达到近乎完美奖励的方法；在Craftium的3D钻石采集任务中，PPO+LARM持续完成整个任务序列；在XLand-MiniGrid的多任务设置中，完整方法在同时训练10个任务时仍保持高成功率，并展示了零样本泛化能力。

强化学习中的奖励函数设计高度敏感：稀疏奖励无法提供足够的学习信号，而手工设计的稠密奖励又容易产生奖励破解（reward hacking）问题。将复杂目标转化为结构化的、可操作的奖励信号是核心瓶颈。

奖励机构（Reward Machines, Icarte et al., 2022）提供了一种基于自动机的形式化奖励规范方法，能够将复杂任务分解为子目标序列并结构化地分配奖励。然而，传统RM需要专家手工设计，这限制了其可扩展性。同时，现有方法如使用SAT算法从演示中学习RM（Alsadat et al., 2025）或使用L*算法合成自动机（Vazquez-Chanlatte et al., 2025）仍需要专家演示或大量人工干预。

ARM-FM旨在解决这一瓶颈：利用基础模型自动生成完整的、可执行的奖励机构，包括自动机结构、标签函数和每个子目标的自然语言描述，从而消除对手工设计的依赖。

## 核心方法与创新机理

ARM-FM的核心创新在于将基础模型的高层推理能力与奖励机构的形式化结构相结合，具体体现在：

1. **语言对齐奖励机构（LARM）**：在传统RM基础上，为每个RM状态u配备自然语言指令l_u和嵌入函数φ(·)，将指令映射到嵌入向量z_u = φ(l_u) ∈ R^d。这使得策略可以基于当前子目标的语义嵌入进行条件化。

2. **自动化RM生成**：使用生成器-评论家FM对进行N轮自我改进，直接从自然语言和视觉观察生成完整的LARM，包括自动机结构、可执行的标签函数代码和每个子目标的自然语言描述。人类可选的验证步骤进一步保证了质量。

3. **语义技能空间**：通过语言嵌入构建语义技能空间，使策略能够在相关子目标间共享知识，实现迁移、组合和零样本泛化。策略以环境状态s_t和当前RM状态的语言嵌入z_{u_t}为条件：π(s_t, z_{u_t})。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/001_Figure_1.jpg]]
*Figure 1: An overview of our framework (left) and results in a complex sparse-reward environment (right). Reward Machine Generation (top-left): Given a high-level natural language prompt and a visual observation of the environment, a FM automatically generates the formal specification of the Reward Machine, the executable Python code for the labeling functions, and the natural language descriptions for each RM state. RL training (bottom-left): During the RL training loop, the labeling functions evaluate environment observations to update the Reward Machine’s state, which provides a dense reward signal $R _ { t } ^ { \mathrm { R M } }$ . The RL agent’s policy receives the environment observati...*

ARM-FM的整体框架如Figure 1所示，包含两个主要阶段：

**RM生成阶段（Figure 1左上）**：给定高层自然语言提示和环境视觉观察，FM自动生成奖励机构的形式化规范、可执行的标签函数Python代码以及每个RM状态的自然语言描述。生成过程采用生成器-评论家FM对的自我改进循环（Figure 3），可选人工验证。

**RL训练阶段（Figure 1左下）**：在RL训练循环中，标签函数评估环境观察以更新RM状态，提供稠密奖励信号R_t^{RM}。RL智能体的策略接收环境观察和当前RM状态语言描述的嵌入φ(·)，使其感知当前活跃的子目标。总奖励为R_t^{total} = R_t + R_t^{RM}。

Figure 2展示了ARM-FM如何利用FM自动从MiniGrid的UnlockToUnlock任务描述构建RM。Figure 4展示了生成的三个核心组件：RM规范、标签函数和状态指令与嵌入。

### 5.1 奖励机构（RM）形式化定义

标准MDP定义为 ⟨S, A, R, P⟩。奖励机构（RM）定义为元组 ⟨U, u_I, Σ, δ, R, F, L⟩，其中：
- U：有限RM状态集
- u_I：初始状态
- Σ：事件符号集
- δ: U × Σ → U：确定性转移函数
- R: U × S × A × S → R：基于当前RM状态u和MDP转移(s, a, s')分配奖励的函数
- F：终止状态集
- L: S × A → Σ：将MDP状态和动作连接到RM事件符号的标签函数

### 5.2 LARM嵌入

LARM在传统RM基础上增加：
- 每个RM状态u的自然语言指令l_u
- 嵌入函数φ(·)：将语言指令映射到嵌入向量z_u = φ(l_u) ∈ R^d

### 5.3 策略条件化

策略在给定环境状态s_t和当前RM状态u_t的语言嵌入z_{u_t}时选择动作a_t：
π(a_t | s_t, z_{u_t})

### 5.4 DQN训练目标（带LARM）

DQN训练的目标值使用总奖励和目标Q网络，输入为环境状态和LARM状态嵌入：
y_j = 
\begin{cases} 
R_j^{total} & \text{if episode terminates at step } j+1 \\
R_j^{total} + \gamma \max_{a'} \hat{Q}(s_{j+1}, \phi(u_{j+1}), a'; \theta^-) & \text{otherwise}
\end{cases}

梯度下降损失为：
(y_j - Q(s_j, \phi(u_j), a_j; \theta))^2

### 5.5 最优性保持条件

在LARM无正奖励循环且最终奖励严格大于任何非终止轨迹累积奖励的假设下，对LARM增强MDP最优的策略也对原始稀疏MDP最优：
π^* optimal for M_LARM ⟹ π^* optimal for M

## 实验与关键发现

### 6.1 主要实验结果

| 基准 | 指标 | ARM-FM | 基线 | 置信度 |
|------|------|--------|------|--------|
| MiniGrid-DoorKey (固定地图) | 累积奖励 | 持续高于基线 | DQN, DQN+ICM, ReAct均显著较低 | 0.95 |
| MiniGrid-DoorKey (程序生成地图) | 累积奖励 | 持续高于基线 | DQN, DQN+ICM, ReAct均显著较低 | 0.95 |
| MiniGrid-UnlockToUnlock | 累积奖励 | 近乎完美奖励 | DQN, DQN+ICM, ReAct均无学习 | 0.95 |
| MiniGrid-BlockedUnlockPickup | 累积奖励 | 近乎完美奖励 | DQN, DQN+ICM, ReAct均无学习 | 0.95 |
| MiniGrid-KeyCorridor | 累积奖励 | 近乎完美奖励 | DQN, DQN+ICM, ReAct均无学习 | 0.95 |
| Craftium (钻石采集) | 任务完成度 | 持续完成整个任务序列 | PPO基线几乎无进展 | 0.95 |
| Meta-World (多个操作任务) | 成功率 | 在大多数任务中达到高成功率 | 稀疏奖励SAC成功率较低 | 0.95 |
| XLand-MiniGrid (多任务，最多10个) | 平均成功率 | 在10个任务上保持高成功率 | 仅奖励或仅嵌入的基线在任务数增加时失败 | 0.95 |
| XLand-MiniGrid (零样本泛化) | 零样本成功率 | 成功解决未见过的组合任务C | 无基线（零样本设置） | 0.95 |

**Figure 6**展示了ARM-FM在MiniGrid-DoorKey任务中不同网格尺寸下的性能，在固定地图和程序生成地图上均持续优于所有基线。

**Figure 7**展示了在三个复杂长时域MiniGrid任务中，ARM-FM是唯一能解决所有任务并达到近乎完美奖励的方法，而所有基线方法均未取得任何进展。

**Figure 1 (右)**展示了在Craftium的3D钻石采集任务中，PPO+LARM持续完成整个任务序列，而基线PPO几乎无进展。

**Figure 8**展示了在Meta-World操作任务中，ARM-FM在大多数任务中达到高成功率。

### 6.2 消融研究

**Figure 9**展示了ARM-FM组件的消融研究：在XLand-MiniGrid上训练Rainbow智能体处理递增数量的任务。只有完整方法（LARM奖励+状态嵌入）在任务数增加时保持高成功率，而仅使用奖励或仅使用嵌入的基线均失败。这表明LARM奖励和状态嵌入对于学习鲁棒的多任务策略都是必不可少的。

**Figure 19**展示了在UnlockToUnlock任务中，智能体首先学习最大化LARM提供的结构化子目标奖励（蓝色曲线），一旦子目标序列被掌握（虚线），最终目标的成功率急剧上升（橙色曲线）。

**Figure 18**比较了探索基线（ICM, RND, Disagreement）在MiniGrid DoorKey任务上的表现，ICM表现最强且最一致，因此被选为主要比较基线。

**Figure 21**展示了CLIP-based VLM-as-reward-model基线在所有评估的MiniGrid任务上均未取得任何进展。

**Figure 15**展示了在Meta-World上，将奖励机器与RND探索项结合可以获得更好的整体性能。

### 6.3 零样本泛化

**Figure 10**展示了零样本泛化：训练于任务A和B的策略能够零样本泛化到由熟悉子目标组成的新任务C。因为C中的子目标（如"Pick up a blue key"）在训练中语义熟悉，智能体可以复用已学技能解决新任务而无需微调。

### 6.4 FM生成分析

**Figure 11a**展示了在1000个XLand-MiniGrid任务上的LLM-as-judge评估，揭示了强烈的规模缩放趋势：更大的基础模型更可靠地生成正确的RM结构和验证代码。

**Figure 11b**展示了FM生成的状态指令嵌入的PCA可视化，呈现清晰的语义结构：起始、中间和结束状态形成不同的簇，不同任务的相似指令聚类在一起。

### 6.5 公平性说明

- 所有实验均使用3个独立随机种子运行，结果报告平均值和±1标准差。
- 超参数在基线和ARM-FM方法之间保持一致（详见附录A.11）。
- 人类干预需求因环境而异：DoorKey、BlockedUnlockPickup、Craftium和XLand-MiniGrid无需干预；UnlockPickup、KeyCorridor和MetaWorld需要不同程度的人类反馈（见表3）。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/027_Table_3.jpg]]
*Table 3: Summary of Human-in-the-Loop Effort for LARM Generation.*

- 所有LARM组件均使用GPT-4o生成，但XLand-MiniGrid的1000个LARM使用了不同规模的开源FM进行消融研究。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/024_Table_1.jpg]]
*Table 1: Supported goals in the XLand-MiniGrid formal language.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/025_Table_2.jpg]]
*Table 2: Supported rules in the XLand-MiniGrid formal language.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/028_Table_4.jpg]]
*Table 4: Comparison of ARM-FM with FM-driven automata and FM-guided RL frameworks. Our method’s advantages are highlighted in bold.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_OBpQdCWLfd_ARM-FM_Automated_Reward_/figures/035_Table_5.jpg]]
*Table 5: DQN hyperparameters used for all MiniGrid and BabyAI experiments.*

## 定位与知识库关联

ARM-FM在方法谱系中占据独特位置，如**Table 4**所示：

**与FM驱动自动机框架的比较**：
- L*LM (Vazquez-Chanlatte et al., 2025)：使用FM回答L*算法的成员查询来合成自动机，需要专家演示。
- RAD (Yalcinkaya et al., 2024)：使用FM生成文本作为SAT算法的反馈来学习RM，需要给定RM。
- Alsadat et al. (2025)：使用FM进行SAT-based RM学习，无需演示但需要手工设计。
- **ARM-FM**：直接生成完整的、语义化的自动机，无需专家演示，且提供语言嵌入实现泛化。

**与FM引导RL框架的比较**：
- ReAct (Yao et al., 2023)：生成文本推理轨迹和动作，不生成RM。
- SayCan (Ahn et al., 2022)：为预定义技能评分可行性，需要预定义技能。
- Voyager (Wang et al., 2023)：生成Python代码用于Minecraft探索，不生成RM。
- Eureka (Ma et al., 2023)：演化程序化奖励函数的代码库，不生成RM。
- **ARM-FM**：生成完整的RM，提供结构化奖励和语言嵌入，实现组合和泛化。

ARM-FM的核心优势在于：直接生成完整的、语义化的自动机，无需专家演示；提供语言嵌入实现跨任务泛化；通过生成器-评论家自我改进循环和可选人工验证保证质量；支持零样本泛化到由熟悉子目标组成的新任务。

**局限性**：
- 人类验证步骤是当前方法的一个权衡：一方面可以作为质量保证的特征，另一方面假设了人类验证者的可用性。
- 对于某些环境（如MetaWorld），初始奖励值可能导致局部最优，需要人类干预来调整奖励值。
- 方法依赖于基础模型的知识和推理能力；对于基础模型不熟悉的领域，生成质量可能下降。
- 零样本泛化仅在子目标语义上熟悉的情况下有效；对于包含全新子目标的任务，泛化可能失败。

**开放问题**：
- 如何进一步减少或消除对人类验证的依赖？论文提到可以利用RM的自动机结构进行形式化验证实现自动自我修正。
- ARM-FM在更复杂、更开放的环境（如完整的Minecraft或真实机器人）中的表现如何？
- 对于基础模型不熟悉的领域，如何保证生成RM的质量？是否需要领域特定的微调或提示工程？

## 原文 PDF

![[paperPDFs/ICLR_2026/ARM_FM_Automated_Reward_Machines_via_Foundation_Models_for_Compositional_Reinforcement_Learning.pdf]]
