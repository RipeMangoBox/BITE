---
title: Training One Model to Master Cross-Level Agentic Actions via Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Training_One_Model_to_Master_Cross_Level_Agentic_Actions_via_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- TOMMCLAARL
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: Training
primary_logic: Training
claims:
- Training
---

# Training One Model to Master Cross-Level Agentic Actions via Reinforcement Learning

> [!tip] 核心洞察
> Training

| 字段 | 内容 |
|------|------|
| 中文题名 | Training One Model to Master Cross-Level Agentic Actions via Reinforcement Learning |
| 英文题名 | Training One Model to Master Cross-Level Agentic Actions via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09706) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method |  |
| Dataset | Minecraft open-world task benchmark, mixed-space SFT dataset, ID/OOD task sets |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

现有具身智能体在 Minecraft 等开放环境中通常被限制在**单一的动作空间**（如原子操作或高层命令）内完成整个任务轨迹，导致执行效率低下且难以泛化。本文提出 **CrossHA**，一个统一的智能体模型，能够在同一轨迹中**自主、动态地选择最合适的异构动作空间**（Motion、Grounding、Raw），无需人工定义的启发式规则。

核心训练管线包含三个阶段：**冷启动监督微调（SFT）→ 单轮强化学习（STRL）→ 多轮强化学习（MTRL）**。其中 STRL 阶段通过 GRPO 让模型学习单一动作空间的正确性，MTRL 阶段则利用 Multi-Turn GRPO 以整条轨迹的成功率为优化信号，驱动模型学会**上下文自适应的动作空间切换**，同时平衡任务成功率与执行效率。

在仅使用 30 个任务训练的情况下，CrossHA 泛化至 Minecraft 中 **超过 800 个任务**，取得 state-of-the-art 性能。该方法在方法谱系上属于**多动作空间统一建模 + 多阶段强化学习**，区别于固定单空间的传统方案（如 VPT、MPGD 等依赖单一动作接口的方法）。

### 问题背景：Minecraft 中的异构动作空间

Minecraft 作为具身智能体的开放世界测试平台，要求智能体在同一个任务轨迹中应对截然不同的交互场景：从第一人称的导航与物体操作，到 GUI 界面的合成与背包管理。这些场景对应着性质迥异的动作空间——**连续运动控制、离散坐标点击、原始键鼠操作**——它们在粒度、抽象层级和控制精度上存在根本差异。

Figure 1 展示了这一核心矛盾：现有方法通常将智能体锁定在单一动作空间内（如纯原子运动指令），迫使模型在需要精细 GUI 操作或快速原始输入时仍使用不匹配的接口，导致执行效率低下和任务失败。

### 现有方法的缺口

当前 Minecraft 智能体研究主要沿两条路线展开：

1. **单一动作空间范式**：无论是基于高层语义指令的规划器，还是直接输出原始键鼠的端到端模型，都假设在整个轨迹中维持统一接口。这种做法忽略了任务阶段对动作粒度的动态需求——例如，长距离导航需要粗粒度的运动指令，而合成台操作则需要精确的 GUI 点击。

2. **人工启发的切换策略**：部分工作尝试组合多个动作空间，但切换逻辑依赖手工设计的规则或启发式函数。这类方法缺乏灵活性和泛化能力，无法根据上下文自主判断最优接口。

从实验证据看，单一空间基线在 Multi-Turn RL 训练中不仅收敛速度更慢，且渐近性能显著低于使用异构空间的方法（Figure 3）。这表明**动作空间的固定约束本身构成了性能瓶颈**。

### 本文动机

本文的核心动机源于一个观察：人类玩家在 Minecraft 中会自然地在不同操作模式间切换——键盘疾跑穿越平原，鼠标精确点击合成界面。这种**上下文自适应的动作空间选择**是高效完成任务的关键。

为此，CrossHA 提出两个根本性转变：

- **统一异构动作空间**：将多个动作子空间形式化为可联合建模的整体 $\mathcal{A} = \bigcup_{x=1}^{N} \mathcal{A}_x$，使单一模型具备跨空间操作的能力。
- **自主动态切换**：智能体在轨迹的每一步自主选择最合适的动作空间，无需人工定义切换规则。这一能力通过包含 Single-Turn RL 和 Multi-Turn RL 的完整强化学习流水线习得，目标函数显式平衡任务奖励与执行成本：$J = \mathbb{E}\left[\sum_t \left(r_t - \lambda_x \cos(a_t)\right)\right]$。

最终目标是构建一个在仅训练 30 个任务的情况下，能泛化至超过 800 个 Minecraft 任务的统一智能体，并在各类任务上达到最优或次优性能（Table 2）。

## 核心方法与创新机理

CrossHA 的核心创新在于将**异质动作空间的选择**本身建模为一个可学习的策略问题，而非依赖人工预设的固定空间或启发式切换规则。具体而言，其关键创新点体现在以下三个层面：

1. **统一异质动作空间与自主切换**：CrossHA 将多个异构的动作子空间（如原子运动、语义定位、原始键鼠操作）联合为一个复合动作空间 $\mathcal{A} = \bigcup_{x=1}^{N} \mathcal{A}_x$，并赋予模型在轨迹的每一步**自主选择最适动作空间**的能力。这与以往方法将智能体全程禁锢于单一固定动作空间（如仅用原子移动）形成根本性差异。

2. **三阶段训练管线**：提出“冷启动监督微调 → 单轮强化学习 → 多轮强化学习”的递进式训练范式。其中，单轮 RL 阶段通过 GRPO 优化单步动作的正确性，多轮 RL 阶段则以**回合成功率**为信号，直接优化动作空间切换策略与任务完成能力。这一管线使得模型仅需在 30 个任务上训练，即可泛化至 800 余个任务。

3. **效率与成功率的联合优化**：在目标函数 $J = \mathbb{E}\left[\sum_t \left(r_t - \lambda_x \cos(a_t)\right)\right]$ 中显式引入执行代价惩罚项，使智能体在追求任务成功的同时，学会选择执行效率更高的动作空间，避免不必要的冗长操作序列。

上述创新共同构成了 CrossHA 相较于固定动作空间基线（如 VPT、ROCKET-1、GroundingHA）的核心差异——**动作空间不再是预设常量，而是策略的一部分**。

CrossHA 的核心设计目标是将**异构动作空间的选择**本身作为一个可学习的策略问题，而非依赖人工定义的启发式规则。为此，论文构建了一个三阶段训练管线，逐步赋予模型在不同动作空间之间自主切换的能力。

### 动作空间定义

系统将完整的动作空间建模为多个子空间的并集：

$$\mathcal{A} = \bigcup_{x=1}^{N} \mathcal{A}_x$$

其中每个 $\mathcal{A}_x$ 代表一种异构的动作接口（如原子移动、方块放置、实体交互等）。与以往将智能体锁定在单一固定动作空间的方法不同，CrossHA 允许模型在轨迹的每一步动态选择最合适的 $\mathcal{A}_x$ 来执行动作。

### 三阶段训练管线

训练管线由三个递进阶段构成，整体流程如 **Figure 2** 所示：

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/002_Figure_2.jpg]]
*Figure 2: | Overview of the CrossHA Training Pipeline. The pipeline comprises three distinct stages: Cold-Start Supervised Fine-Tuning (SFT), Single-Turn Reinforcement Learning (STRL), and Multi-Turn Reinforcement Learning (MTRL). In the first stage, the model learns to decode actions from a heterogeneous action space using a balanced dataset. During STRL, the model is fine-tuned to autonomously select the appropriate action space based on the immediate task context. Finally, in the MTRL stage, the policy is further optimized to balance task success rate with execution efficiency over long horizons. This progressive pipeline ensures CrossHA effectively adapts its action granularity across a wide rang...*

1. **冷启动监督微调（Cold-Start SFT）**：在收集的示范数据上进行初步的监督学习，使模型获得基本的指令遵循和动作生成能力。

2. **单轮强化学习（Single-Turn RL, STRL）**：此阶段关注单步动作的正确性。目标函数为最大化期望奖励：

   $$J(\theta) = \mathbb{E}_{(x, a^\star) \sim D} \mathbb{E}_{\hat{a} \sim \pi_\theta(\cdot \vert x)} [r(\hat{a}, a^\star)]$$

   其中 $r(\hat{a}, a^\star)$ 衡量模型生成动作 $\hat{a}$ 与参考动作 $a^\star$ 之间的一致性。该阶段采用 **GRPO**（Group Relative Policy Optimization）进行策略优化——GRPO 利用同一查询下多个采样输出的组内统计量来估计优势函数，无需额外的价值函数网络，从而简化了训练架构。GRPO 的优化目标为：

   $$J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{\sigma_i\}_{i=1}^G \sim \pi_{\mathrm{old}}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|\boldsymbol{o}_i|} \sum_{t=1}^{|\boldsymbol{o}_i|} \min\left( \rho_{i,t} \hat{A}_{i,t}, \operatorname{clip}(\rho_{i,t}, 1-\epsilon, 1+\epsilon) \hat{A}_{i,t} \right) - \beta D_{KL}(\pi_\theta \| \pi_{\text{ref}}) \right]$$

   其中概率比 $\rho_{i,t} = \frac{\pi_{\theta}(o_i | q, \boldsymbol{o}_{<t})}{\pi_{\mathrm{old}}(o_i | q, \boldsymbol{o}_{<t})}$。在 STRL 启动前，还通过拒绝采样构建了一个覆盖多动作空间的数据集进行预热微调。

3. **多轮强化学习（Multi-Turn RL, MTRL）**：将优化目标从单步正确性提升到**整个轨迹的任务成功率**。奖励信号简化为轨迹级别的稀疏二元奖励：

   $$r(\tau) = \mathbf{1}\{\text{success}(\tau)\}$$

   同时引入自训练重标记机制：若模型选择的动作空间在语义上等价于参考动作空间，则用模型自身的动作空间标签替换原始标签：

   $$a'(x) = \begin{cases} \hat{a}(x), & \text{if } g(\hat{a}(x)) = g(a^\star(x)), \\ a^\star(x), & \text{otherwise}. \end{cases}$$

   这一机制使模型能够在多轮交互中自主学习何时切换动作空间，以最大化任务成功率与执行效率的平衡。最终优化目标为：

   $$J = \mathbb{E} \left[ \sum_{t} \left( r_t - \lambda_x \cos(a_t) \right) \right]$$

   其中 $\lambda_x \cos(a_t)$ 项对不同动作空间施加差异化的执行成本惩罚，引导模型在高奖励与低开销之间取得平衡。

### 输入输出流

整个管线中，模型接收任务指令 $x$ 作为输入，在每个时间步输出一个动作 $\hat{a}$，该动作来自当前选择的动作空间 $\mathcal{A}_x$。经过 MTRL 阶段训练后的最终模型 $M_{\mathrm{mtrl}}$ 即为完整的 CrossHA 智能体。

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/001_Figure_1.jpg]]
*Figure 1: | The CrossHA Framework. Unlike prior methods that confine the agent to a fixed action space (e.g., atomic movements) throughout a trajectory, CrossHA dynamically switches across different action spaces to adapt to the context*

### 3.1 复合动作空间

CrossHA 的核心设计是将多个异质动作空间统一为一个复合动作空间，使模型能够在轨迹的每一步自主选择最合适的动作接口。形式上，复合动作空间定义为各子空间的并集：

$$\mathcal{A} = \bigcup_{x=1}^{N} \mathcal{A}_x$$

其中 $\mathcal{A}_x$ 表示第 $x$ 个动作子空间（如 Motion、Grounding、Raw），$N$ 为子空间总数。模型在每个时间步不仅需要输出具体动作，还需隐式地选择当前步应使用哪个子空间——这一选择本身作为策略学习的一部分被优化，而非依赖人工预设的启发式规则。

### 3.2 单轮强化学习（STRL）与 GRPO

STRL 阶段的目标是让模型在单步决策中学会生成正确的原始动作。其优化目标为：

$$J(\theta) = \mathbb{E}_{(x, a^\star) \sim D}\; \mathbb{E}_{\hat{a} \sim \pi_\theta(\cdot \vert x)} \left[ r(\hat{a}, a^\star) \right]$$

其中 $x$ 为观测输入，$a^\star$ 为标注的正确动作，$\hat{a}$ 为模型策略 $\pi_\theta$ 采样的候选动作，$r(\cdot)$ 为动作正确性的奖励函数。

该阶段采用 **GRPO（Group Relative Policy Optimization）** 进行策略优化。与 PPO 依赖独立的价值函数网络进行优势估计不同，GRPO 利用同一提示下多组采样输出的组内统计量来估计基线，从而简化训练架构。其核心目标函数为：

$$J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{\sigma_i\}_{i=1}^G \sim \pi_{\mathrm{old}}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|\boldsymbol{o}_i|} \sum_{t=1}^{|\boldsymbol{o}_i|} \min\left( \rho_{i,t} \hat{A}_{i,t},\; \operatorname{clip}(\rho_{i,t}, 1-\epsilon, 1+\epsilon) \hat{A}_{i,t} \right) - \beta \, D_{\mathrm{KL}}(\pi_\theta \Vert \pi_{\mathrm{ref}}) \right]$$

其中概率比率 $\rho_{i,t}$ 定义为：

$$\rho_{i,t} = \frac{\pi_{\theta}(o_i \vert q, \boldsymbol{o}_{<t})}{\pi_{\mathrm{old}}(o_i \vert q, \boldsymbol{o}_{<t})}$$

变量含义：$G$ 为每组采样数，$\boldsymbol{o}_i$ 为第 $i$ 个输出序列，$\hat{A}_{i,t}$ 为基于组内统计的优势估计，$\epsilon$ 为裁剪阈值，$\beta$ 控制 KL 散度惩罚项强度，$\pi_{\mathrm{ref}}$ 为参考策略。

### 3.3 多轮强化学习（MTRL）与目标函数

MTRL 阶段将优化信号从单步动作正确性扩展为整个轨迹的任务成功率。奖励函数简化为二值指示：

$$r(\tau) = \mathbf{1}\{\operatorname{success}(\tau)\}$$

即轨迹 $\tau$ 成功完成任务时奖励为 1，否则为 0。完整的优化目标在奖励基础上引入执行效率惩罚项：

$$J = \mathbb{E} \left[ \sum_{t} \left( r_t - \lambda_x \cos(a_t) \right) \right]$$

其中 $\lambda_x$ 为子空间 $x$ 对应的代价系数，$\cos(a_t)$ 衡量动作 $a_t$ 的执行代价。该目标鼓励模型在保证任务成功的前提下，选择执行效率更高的动作空间。

为支持动作空间的自适应选择，MTRL 阶段引入自训练重标注机制。对于语义正确但动作空间与标注不同的模型输出，将其重标注为有效样本：

$$a'(x) = \begin{cases} \hat{a}(x), & \text{if } g(\hat{a}(x)) = g(a^\star(x)), \\ a^\star(x), & \text{otherwise}. \end{cases}$$

其中 $g(\cdot)$ 为语义等价性判断函数。这一机制使模型在强化学习过程中能够逐步学习到“何时切换至何动作空间”的最优策略，而无需人工指定切换规则。

## 实验与关键发现

### 主结果：跨任务类别的综合性能

CrossHA 在 Minecraft 环境中超过 800 个任务上进行了评估，涵盖 **Mine Blocks**、**Craft Items** 和 **Kill Entity** 三大任务类别。Table 1 报告了各方法在每个类别上的代表性任务成功率、类别内全部任务的完成率（FT, Full-Task completion rate）以及平均成功率（ASR, Average Success Rate）。

CrossHA 在所有三大类别上均取得了最优性能：在 Mine Blocks 类别上达到 **94.7%** 的 ASR，在 Craft Items 类别上达到 **83.3%** 的 ASR。相比之下，采用固定动作空间的基线方法表现出明显的类别偏好——**GroundingHA** 在 Kill Entity 任务上表现突出（FT: 90.1%），但在其他类别上性能受限；**VPT** 在 Mine Blocks 上仅取得 20.0 FT 和 30.7 ASR，**ROCKET-1** 分别为 60.0 FT 和 57.5 ASR。这一结果表明，动态动作空间选择是跨异构任务泛化的关键机制，单一动作空间无法在所有任务类别上同时达到最优。

### 动作空间敏感性分析

Figure 3 展示了 CrossHA 与单一动作空间基线在 Multi-Turn RL 阶段的学习曲线对比。CrossHA 的异构动作空间设计带来了两个显著优势：

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/004_Figure_3.jpg]]
*Figure 3: | Performance Comparison Across Action Spaces. The heterogeneous action space of CrossHA enables superior data efficiency and higher asymptotic performance during multi-turn reinforcement learning, compared to single-space baselines*

1. **更高的数据效率**：在训练早期，CrossHA 的成功率上升速度明显快于任一单一空间基线，表明模型能够利用多空间探索加速策略学习。
2. **更高的渐近性能**：训练收敛后，CrossHA 的最终成功率显著超越所有单一空间配置，验证了动作空间选择本身作为一个可学习策略组件的价值。

这一结果直接回应了核心研究问题：最优动作空间确实因任务而异，且通过 RL 学习动态切换策略优于任何静态空间选择。

### 分布外泛化能力

Table 2 报告了 RL 训练后的智能体在分布内（ID）和分布外（OOD）任务上的成功率。CrossHA 在 OOD 任务上保持了较强的泛化能力，成功率显著优于单一空间基线。值得注意的是，CrossHA 仅在 **30 个训练任务**（每个主要类别选取 10 个）上进行 MTRL 阶段训练，却能泛化至超过 800 个任务，这表明学习到的动作空间切换策略具有良好的任务结构迁移性，而非对训练任务的简单记忆。

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/006_Table_2.jpg]]
*Table 2: | Evaluation results of RL agents on In-Distribution (ID) and Out-of-Distribution (OOD) tasks. We report the success rate and standard deviation. Red indicates the best performance, and Blue indicates the second best*

### 失败模式分析

尽管 CrossHA 在整体性能上达到最优，但从类别细分结果中可以识别出以下边界情况：

- **Kill Entity 类别**：GroundingHA 在该类别上仍保持竞争力（FT: 90.1%），说明对于需要精确空间定位和交互的战斗类任务，单一的高精度动作空间可能具有天然优势。CrossHA 的动态切换在此类任务中可能引入额外的决策开销。
- **Craft Items 类别**：所有方法的绝对成功率均低于 Mine Blocks 类别，反映了合成类任务固有的长时序依赖和复杂前置条件带来的挑战。CrossHA 虽在该类别上领先，但 83.3% 的 ASR 表明复杂合成任务仍是当前方法的瓶颈。

### 关键图表结论

- **Table 1**：CrossHA 在三大任务类别上全面超越固定动作空间基线，验证了异构动作空间与动态选择机制的有效性。
- **Figure 3**：异构动作空间在 Multi-Turn RL 中带来数据效率与渐近性能的双重增益，单一空间配置无法匹配。
- **Table 2**：CrossHA 在仅使用 30 个训练任务的条件下，展现出对 800+ 任务的强泛化能力，OOD 性能显著优于基线。
- **Table 3**：CrossHA 采用与人类玩家完全对齐的原始键鼠动作空间，保证了交互接口的通用性和可复现性。
- **Table 4**：各训练阶段的超参数配置为后续复现提供了完整参考。

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/010_Table_4.jpg]]
*Table 4: | Hyperparameter settings across different training stages*

![[assets/figures/papers/paper_list_l2728_https_arxiv_org_abs_2512_09706/figures/009_Figure_6.jpg]]
*Figure 6: | Case Study: Action distribution during the Kill Sheep, Chop Tree and Craft Enchanting task. The density curves of each tasks, aggregated over 20 episodes, of different action spaces (Motion, Grounding, Raw) across different task phases. The dynamic shifts in distribution demonstrate the model’s in-context adaptive strategy*

## 定位与知识库关联

### 1. 与基线工作的关系

CrossHA 的核心贡献在于将**异构动作空间的自适应选择**形式化为策略学习问题，而非依赖人工启发式规则。这一设计直接回应了现有 Minecraft 智能体的一个结构性瓶颈：固定动作空间在任务不同阶段效率差异巨大。

- **VPT**（OpenAI, 2022）与 **ROCKET-1**（Cai et al., 2024）均采用单一动作空间贯穿整个轨迹。Table 1 显示，VPT 在 Mine Blocks 任务上仅取得 20.0 FT / 30.7 ASR，ROCKET-1 为 60.0 FT / 57.5 ASR，而 CrossHA 达到 94.7% ASR。性能差距的因果机制在于：固定动作空间迫使模型在需要精细操作时使用粗粒度动作，或在需要快速导航时使用低效的原子动作。
- **GroundingHA** 在 Kill Entity 任务上表现突出（FT: 90.1%），说明特定动作空间在特定任务类别中存在天然优势。CrossHA 不否认这一点，而是通过动态切换机制，在不同任务阶段调用最合适的动作空间，从而在全部三个主任务类别上取得 SOTA。

CrossHA 与上述工作的关系是**包容性超越**：它不排斥任何单一动作空间，而是将多种空间统一到同一策略框架下，让 RL 自动学习切换时机。

### 2. 训练范式的谱系定位

CrossHA 的三阶段训练管线（Cold-Start SFT → Single-Turn RL → Multi-Turn RL）在 LLM 智能体训练范式中有明确谱系位置：

- **SFT 冷启动**：继承自行为克隆范式，但 CrossHA 的创新在于通过拒绝采样（rejection sampling）构造覆盖多动作空间的数据集，使模型在 SFT 阶段即获得跨空间生成能力。
- **Single-Turn RL（STRL）**：采用 **GRPO**（Group Relative Policy Optimization）进行单步动作正确性优化。GRPO 的核心优势在于利用组内统计量进行优势估计，无需独立的价值函数网络，降低了训练复杂度。这一定位使 CrossHA 区别于依赖 PPO 的基线（如需要额外价值网络的方案）。
- **Multi-Turn RL（MTRL）**：以回合成功率 $r(\tau) = \mathbf{1}\{\text{success}(\tau)\}$ 为优化信号，使模型在完整轨迹层面学习动作空间切换策略。这一设计与单步奖励优化形成互补——STRL 保证单动作质量，MTRL 优化全局决策序列。

### 3. 适用边界与约束条件

基于论文提供的证据，CrossHA 的适用边界可归纳如下：

**有效范围**：
- 任务环境需存在多个语义明确、功能互补的动作空间。论文在 Minecraft 中验证了 Motion、Grounding、Raw 三种空间的有效性，但该方法对动作空间数量的上限未做消融。
- 训练任务仅 30 个（每类别 10 个），但泛化至 800+ 任务。这表明方法在**任务分布内插**（ID）和适度外推（OOD）上有效，但极端 OOD 场景的泛化边界未充分测试。

**约束条件**：
- MTRL 阶段的奖励信号依赖环境提供的成功判定，对于缺乏明确成功信号的长程开放任务，奖励设计将成为瓶颈。
- 训练成本方面，STRL 阶段被描述为“低计算开销”，但 Figure 4 仅展示了有无 STRL 的收敛速度对比，未提供绝对计算量对比。具体资源消耗需参考 Table 4 的超参设置并结合实际硬件环境估算。
- 动作空间的定义和实现需人工预先设计，CrossHA 本身不解决动作空间的自动发现或构造问题。

### 4. 局限与开放问题

论文识别的局限及分析中浮现的开放问题包括：

1. **动作空间数量的可扩展性**：当前仅验证了三种动作空间。当空间数量增长到数十个时，GRPO 的组内统计估计是否仍稳定，以及策略学习是否会因动作空间间的干扰而退化，尚不明确。

2. **最优动作空间的任务依赖性**：Open Questions 中明确提出了“固定动作空间的选择如何影响性能，最优空间是否因任务类别而异”。Figure 6 的案例研究展示了不同任务阶段动作分布的变化，但未系统回答是否存在可预测的空间选择模式，以及能否将这种模式迁移到全新任务。

3. **MTRL 训练任务的代表性**：30 个训练任务从三个类别等量选取。若训练任务分布与目标任务分布存在系统性偏差，MTRL 学到的切换策略可能不最优。论文未对训练任务选择策略做消融。

4. **与基础模型能力的耦合**：CrossHA 基于特定 VLM 骨干。动作空间切换能力的上限是否受限于视觉理解和推理能力，以及更换更强/更弱骨干后方法是否仍有效，未做验证。

5. **奖励稀疏性**：MTRL 仅使用回合级成功信号。对于需要数百步才能完成的超长程任务，稀疏奖励可能导致信用分配困难。论文未讨论在此类场景下的扩展方案（如中间奖励 shaping）。

## 原文 PDF

![[paperPDFs/CVPR_2026/Training_One_Model_to_Master_Cross_Level_Agentic_Actions_via_Reinforcement_Learning.pdf]]
