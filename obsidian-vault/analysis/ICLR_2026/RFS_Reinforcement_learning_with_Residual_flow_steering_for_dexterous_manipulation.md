---
title: "RFS: Reinforcement learning with Residual flow steering for dexterous manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RFS_Reinforcement_learning_with_Residual_flow_steering_for_dexterous_manipulation.pdf
openreview_forum_id: Kt9tJeOwjy
aliases:
- RFSR
- RFS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "联合调节预训练流匹配策略的初始潜变量噪声（输入调制，实现全局模式变化）和残差动作（输出调制，实现局部精细校正），同时冻结基础策略参数。"
primary_logic: "将输入调制与输出调制统一起来，使强化学习能够在不更新基础模型参数的前提下，通过潜变量引导全局探索并通过残差动作修正局部执行错误，从而在灵巧操作任务中实现高效策略适应。"
claims:
- "RFS在六个仿真任务上的平均成功率高达0.861，显著超过基础策略(0.250)与最强基线DSRL(0.483)。"
- "RFS通过联合调制基础策略的输入与输出，在保持基础策略性能的同时稳定提升成功率，在所有任务上均取得最高分。"
- "在真实世界已见物体上，RFS的 pick-and-place 成功率达90.0%，抓取成功率达80.0%，均优于零样本迁移(50.0%/43.3%)和联合训练(60.0%/83.3%)。"
- "Simulation (6 tasks average) 上 Success Rate (avg) = 0.861"
---

# RFS: Reinforcement learning with Residual flow steering for dexterous manipulation

> [!tip] 核心洞察
> 将输入调制与输出调制统一起来，使强化学习能够在不更新基础模型参数的前提下，通过潜变量引导全局探索并通过残差动作修正局部执行错误，从而在灵巧操作任务中实现高效策略适应。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RFS：基于残差流引导的强化学习用于灵巧操作 |
| 英文题名 | RFS: Reinforcement learning with Residual flow steering for dexterous manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Kt9tJeOwjy); [Project](https://weirdlabuw.github.io/rfs/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Residual Flow Steering (RFS) |
| Dataset | Simulation (6 tasks average), Stacking (simulation), Real-world Pick-and-Place (seen objects) |

> [!tip] 效果简介
> - Simulation (6 tasks average) 上，Success Rate (avg) 为 0.861，对比 0.488 (IQL, strongest non-modulation baseline)，变化 +0.373。
> - Stacking (simulation) 上，Success Rate 为 0.951，对比 0.135 (DSRL, best modulation baseline)，变化 +0.816。
> - Real-world Pick-and-Place (seen objects) 上，Success Rate 为 90.0%，对比 50.0% (Zero-Shot Transfer)，变化 +40.0%。

## 概述

灵巧操作任务对策略的泛化能力提出了极高要求。尽管基于流匹配（Flow Matching）的模仿学习策略能够从人类遥操作演示中学习协调的行为模式，但这类预训练策略在部署时面临一个核心瓶颈：**演示数据覆盖有限，策略无法泛化到训练分布之外的场景，而现有强化学习（RL）微调方法难以同时实现全局行为适应与局部精细修正**。直接对生成式模型的全量参数进行RL微调不仅不稳定，还容易破坏预训练策略已有的合理行为。

针对上述问题，本文提出**残差流引导（Residual Flow Steering, RFS）**，一种数据高效的强化学习框架。RFS的核心思路是将策略调制统一为对预训练流匹配策略的**输入调制**（调节初始潜变量噪声，实现全局模式变化）与**输出调制**（施加残差动作，实现局部精细校正）的联合优化，同时**冻结基础策略参数**，仅训练轻量的MLP调制网络。这一设计使RL能够在不破坏预训练行为的前提下，通过潜变量引导全局探索并通过残差动作修正局部执行错误。

实验结果表明，RFS在六个仿真灵巧操作任务上的平均成功率达到**0.861**，显著超过基础策略（0.250）与最强基线DSRL（0.483）。在真实世界的已见物体上，RFS的抓取-放置成功率高达**90.0%**，抓取成功率达**80.0%**，均优于零样本迁移和监督微调基线。消融实验进一步验证了联合调制相较于单独使用输入或输出调制的关键优势，以及冻结基础策略参数对训练稳定性的重要贡献。

## 背景与动机

灵巧操作是机器人学中长期存在的挑战，要求策略同时具备全局行为规划与局部精细执行的能力。近年来，基于生成式模型的行为克隆方法——特别是流匹配（Flow Matching, Lipman et al., 2022）——在从人类演示中学习复杂灵巧技能方面展现出显著潜力。这些方法通过学习从简单先验分布到专家动作分布的速度场，能够生成高度协调的操作行为。

然而，预训练的流匹配策略在部署时面临一个核心瓶颈：**泛化能力不足**。由于演示数据覆盖有限，基础策略在面对分布外状态时表现脆弱，典型失败包括抓取时机错误、抓取姿态不稳定、放置位置偏差等。在真实世界中，仿真到现实（Sim-to-Real）的域差距进一步放大了这一问题。

为弥补这一缺口，研究者尝试将强化学习（RL）引入生成式策略的微调。现有方案大致分为三条路径：一是直接对扩散或流模型的全量参数进行RL微调，如**DPPO**（Ren et al., 2024a）和**ReinFlow**（Zhang et al., 2025a），但这类方法训练不稳定且计算代价高昂；二是采用离线到在线RL范式，如**IQL**（Kostrikov et al., 2021）和**AWAC**（Nair et al., 2021），但它们在灵巧操作任务上的提升有限；三是通过调制策略间接影响基础策略，如**DSRL**（Wagenmaker et al., 2025）仅调节生成式模型的初始潜变量以实现全局模式切换，或残差RL方法（如**Policy Decorator**, Yuan et al., 2024）仅在输出端添加修正项。然而，这些方法存在一个共同缺陷：**无法同时实现全局行为适应与局部精细修正**——输入调制缺乏对执行细节的校正能力，输出调制则难以改变策略的全局行为模式。

本文的动机正源于此：能否设计一种统一的调制框架，在不更新基础策略参数的前提下，同时赋予RL对策略全局语义和局部执行的双重控制能力？这一思路的核心洞察是：将输入调制（潜变量引导）与输出调制（残差动作）联合优化，使RL能够通过潜变量探索新的行为模式，同时通过残差项修正执行中的精细错误，从而在保持预训练策略稳定性的同时高效适应新场景。

## 核心创新

RFS 的核心创新在于**将输入调制与输出调制统一为对预训练流匹配策略的联合引导**，从而在灵巧操作任务中实现高效、稳定的策略适应。其关键设计变化体现在以下三个维度。

### 1. 联合调制策略：从单一调制到输入–输出协同

现有工作分别探索了策略调制的两个方向：**DSRL**（Wagenmaker et al., 2025）通过调节扩散/流模型的初始潜变量噪声实现输入调制，改变全局行为模式；**残差RL**（如 Policy Decorator, ResiP）则在策略输出上叠加残差动作，实现局部精细修正。然而，这两类方法各自存在局限——输入调制缺乏对执行细节的精确控制，输出调制则难以引导策略跳出演示数据的分布进行全局探索。

RFS 的核心洞察在于**将二者统一**：调制策略 $\pi_{\mathrm{RFS}}$ 同时输出潜变量噪声 $w_0$（输入调制）和残差动作 $a_r$（输出调制），联合注入冻结的预训练基础策略 $\pi_{\mathrm{FM}}$，最终动作为 $a = a_b + a_r$（Figure 1）。这种设计使策略既能通过潜变量引导全局模式切换（如改变抓取姿态），又能通过残差修正局部执行错误（如调整闭合时机），从而在保持基础策略协调行为的同时，显著扩展其能力边界。

### 2. 参数冻结与稳定微调：从全量更新到调制参数优化

直接对扩散/流模型的全量参数进行强化学习微调（如 **DPPO**（Ren et al., 2024a）、**ReinFlow**（Zhang et al., 2025a））面临严重的训练不稳定问题。实验表明，这些方法在所有仿真任务上的成功率均低于 0.50（Table 1）。

RFS 的关键设计选择是**冻结预训练基础策略的全部参数**，仅优化调制策略的 MLP 参数（潜变量头和残差头）。消融实验证实，将 RL 更新限制在初始噪声和残差项上，比在全量去噪轨迹上应用 RL 在所有任务上的成功率高至少 0.35（Section 5.1.3）。这一设计从根本上规避了生成模型微调的不稳定性，同时保持了基础策略的原有性能。

### 3. 现实世界适应范式：从监督微调到离线强化学习

在真实世界适应方面，现有方法通常采用监督微调（BC Finetuning）或联合训练（Co-Training）在少量人类数据上更新策略。RFS 提出了一种**基于离线强化学习的适应范式**：利用少量人类纠正数据（50 条），通过 TD3+BC 算法在奖励信号下优化调制策略。Critic 以完整动作 $a = a_b + a_r$ 为条件（而非分解的分量），Actor 在最大化 Critic 的同时通过行为克隆正则项约束残差动作（Eq. 10-11）。在已见物体上，RFS 的 pick-and-place 成功率达 90.0%，显著优于零样本迁移（50.0%）和联合训练（60.0%）（Table 2），验证了离线 RL 范式在数据效率上的优势。

**证据强度说明**：联合调制相对于单一调制的优势有充分的消融实验支撑（Table 1 中 RFS vs DSRL vs 仅残差）；参数冻结设计的稳定性优势在 Section 5.1.3 中有明确的对比分析；离线 RL 范式的有效性在 Table 2 中有真机实验验证。所有核心 claims 置信度均在 0.95 以上。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/001_Figure_1.jpg]]
*Figure 1: Residual Flow Steering (RFS). Given a state s , the RFS policy πRFS outputs a latent flow variable w _ { 0 } and a residual action ^ { a _ { r } , } which jointly steer a pretrained base policy πFM to produce the final action a _ { b } + a _ { r } . RFS enables both global mode shifting and fine-grained residual correction, allowing the policy to expand beyond the demonstration data manifold*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the sim-to-real Residual Flow Steering (RFS) pipeline. (1) VR teleoperation is used to collect demonstrations across multiple manipulation tasks to train task-specific flow-matching base policies. (2) In simulation, the RFS policy πRFS is fine-tuned on top of each base policy and distilled into task-specific visuomotor policies to improve sim-to-real transfer. (3) During zero-shot real-world deployment, human corrective actions correct execution failures such as unstable grasps and misplacement. (4) These corrected transitions are used for offline fine-tuning of πRFS on a Franka–Leap Hand system, improving real-world grasping and pick-and-place performance*

RFS（Residual Flow Steering）的完整管线围绕“预训练生成式策略的强化学习适应”这一核心目标，构建了从仿真训练到真实世界部署的四阶段闭环，如 Figure 2 所示。

**核心架构：联合调制机制**

RFS 的策略架构（Figure 1）将两种调制范式统一在一个轻量级 MLP 策略 π_RFS 中：

1. **输入调制（潜变量引导）**：π_RFS 根据当前状态 s 输出一个潜变量噪声 w₀，替代基础策略原本的随机采样噪声。该噪声作为流匹配生成过程的起点，通过改变初始条件实现**全局行为模式的切换**——例如将抓取姿态从侧抓调整为顶抓。
2. **输出调制（残差校正）**：π_RFS 同时输出一个残差动作 a_r，与基础策略生成的动作 a_b 相加，形成最终执行动作 a = a_b + a_r。该残差项实现**局部精细修正**——例如微调指尖位置以稳定抓取。

基础流匹配策略 π_FM 的参数在此过程中**完全冻结**，RL 仅优化 π_RFS 的 MLP 参数。这一设计的关键因果机制在于：将 RL 更新限制在潜变量与残差项上，避免了直接对扩散/流模型全量参数进行 RL 微调时的不稳定问题（Section 5.1.3 证实，RFS 比 DPPO/ReinFlow 等全量微调方法在所有任务上成功率至少高 0.35）。

**四阶段 Sim-to-Real 管线**

Figure 2 展示了从数据采集到真实世界适应的完整流程：

1. **基础策略预训练**：通过 VR 遥操作采集多任务演示数据，训练任务特定的流匹配策略 π_FM。这些策略提供初步的协调行为，但受限于演示数据的分布。

2. **仿真在线 RL 训练**：在仿真环境中，使用 PPO 在线训练 RFS 调制策略 π_RFS。奖励函数围绕抓取成功与稳定性设计。训练完成后，通过学生-教师蒸馏将 RFS 策略的知识迁移到基于点云的视-动策略中，以提升 Sim-to-Real 迁移能力。

3. **零样本真实世界部署与数据采集**：蒸馏后的策略直接部署到 Franka-Leap Hand 平台。当出现执行失败（如过早闭合手指、抓取不稳定、放置位置偏差）时，人类操作员通过 SpaceMouse 提供纠正动作，系统记录状态、基础动作、人类动作等完整转换数据。

4. **离线 RL 真实世界微调**：利用收集的人类纠正数据（约 50 条），通过 TD3+BC 离线强化学习对 π_RFS 进行微调。Critic 以完整组合动作 a = a_b + a_r 为条件进行 Q 值估计（消融实验证实该设计优于仅使用 a_r 或拼接 [a_r, a_b]），Actor 在最大化 Q 值的同时通过行为克隆正则项约束残差动作的幅度。

**数据流与模块关系**

整个管线的数据流可概括为：遥操作演示 → 流匹配预训练 → 仿真 PPO 调制训练 → 蒸馏为视-动策略 → 零样本部署 → 人类纠正数据采集 → 离线 RL 适应。各模块职责明确，基础策略负责提供行为先验，RFS 调制策略负责全局与局部适应，蒸馏模块负责跨域迁移，离线 RL 模块负责真实世界微调。

## 核心模块与公式推导

### 3.1 流匹配基础策略

RFS 构建在预训练的流匹配（Flow Matching）策略之上。流匹配由 Lipman et al. (2023) 提出，其核心思想是学习一个时变速度场 $v_\theta(x_t, t)$，将基础分布 $p_0$ 中的样本沿直线路径传输到目标分布 $p_1$。训练目标为回归预测速度与直线路径目标之差：

$$\mathcal{L}(\theta) = \mathbb{E}_{x_0 \sim p_0, x_1 \sim p_1, t \sim \mathcal{U}[0,1]} \| v_\theta(x_t, t) - (x_1 - x_0) \|^2$$

推理时，从 $x^0 \sim p_0$ 出发，通过欧拉积分沿学习到的速度场逐步推进，得到近似目标样本 $x^K \approx x_1$：

$$x^{k+1} = x^k + \Delta t_k \, v_\theta(x^k, t_k)$$

将流匹配用于行为克隆，给定专家数据集 $\mathcal{D}$ 中的状态-动作对 $(s, a)$，以状态 $s$ 为条件学习动作的条件速度场。令 $a_0 \sim p_0$ 为初始噪声，$a_t = (1-t)a_0 + t a$ 为直线插值路径上的中间点，条件流匹配策略的损失函数为：

$$\mathcal{L}(\theta) = \mathbb{E}_{a_0 \sim p_0, (s,a) \sim \mathcal{D}, t \sim \mathcal{U}[0,1]} \| v_\theta(a_t, t, s) - (a - a_0) \|^2$$

该预训练策略 $\pi_{\text{FM}}$ 为后续的强化学习适应提供了具备基本协调能力的初始行为。

### 3.2 RFS 调制策略

RFS 的核心创新在于将**输入调制**与**输出调制**统一到一个调制策略 $\pi_{\text{RFS}}$ 中，同时冻结预训练基础策略 $\pi_{\text{FM}}$ 的全部参数。如 Figure 1 所示，给定状态 $s$，$\pi_{\text{RFS}}$ 输出两个调制信号：

- **潜变量噪声 $w_0$**（输入调制）：替代基础策略原有的随机初始噪声，通过调整流匹配的起始条件实现全局行为模式的切换。这一机制继承了扩散引导 RL（Diffusion Steering RL, DSRL）的思想，使策略能够探索演示数据分布之外的行为模式。
- **残差动作 $a_r$**（输出调制）：作为对基础策略输出 $a_b$ 的仿射修正，实现局部精细调整。这一机制继承了残差强化学习（Residual RL）的思想，用于修正抓取姿态、动作时机等执行层面的错误。

最终执行动作为两者之和：

$$a = a_b + a_r$$

其中 $a_b$ 由基础策略 $\pi_{\text{FM}}$ 以 $w_0$ 为初始噪声、以 $s$ 为条件通过流匹配推理生成。RFS 的强化学习优化目标为标准期望折扣回报最大化：

$$\max_{\pi_{\mathrm{RFS}}} \mathbb{E}_{s_0 \sim p_0(s), s' \sim p(s'|s,a)} \left[ \sum_{t=0}^{\infty} \gamma^t r(s_t, a_t) \right]$$

### 3.3 离线强化学习微调

在真实世界部署阶段，RFS 采用离线强化学习对调制策略进行进一步适应。具体流程为：首先零样本部署仿真训练的策略，收集人类通过 SpaceMouse 提供的纠正动作 $a_{\text{human}}$，定义残差标签为 $a_r = a_{\text{human}} - a_b$，构建离线数据集 $\mathcal{D}_{\text{RFS}}$。随后使用 TD3+BC 算法进行离线微调。

**Critic 更新**：Critic 网络以完整组合动作 $a = a_b + a_r$ 为条件（而非分解后的分量），标准 TD 误差最小化：

$$\min_\phi \mathbb{E}_{((o,s),(a_0,a_r),(o',s'),r)\sim\mathcal{D}_{\mathrm{RFS}}} \| Q_\phi(o,s,a) - r - \gamma Q_{\bar{\phi}}(o',s',a') \|^2$$

消融实验表明（Section 5.2.1），以组合动作 $a_b + a_r$ 为条件的 critic 设计在稳定性和性能上优于仅以 $a_r$ 为条件或以 $[a_r, a_b]$ 拼接为条件的方案。

**Actor 更新**：Actor 最大化 critic 评价值，同时通过行为克隆正则项约束残差动作不偏离人类纠正数据过远：

$$\arg\max_{\pi_{\mathrm{RFS}}} \mathbb{E}_{\mathcal{D}_{\mathrm{RFS}}} [ Q(o,s,\hat{a}) - \lambda_{\mathrm{BC}} \| \hat{a}_r - a_r \|^2 ], \quad \hat{a} = \hat{a}_b + \hat{a}_r$$

其中 $\lambda_{\mathrm{BC}}$ 为行为克隆正则化系数，$\hat{a}_b$ 由基础策略以 $\pi_{\text{RFS}}$ 输出的潜变量 $\hat{a}_0$ 为条件生成，$\hat{a}_r$ 为 $\pi_{\text{RFS}}$ 输出的残差预测。

### 3.4 关键设计选择

RFS 方法链中两个关键设计选择直接决定了其有效性：

1. **参数冻结策略**：基础策略 $\pi_{\text{FM}}$ 的所有参数在 RL 训练期间完全冻结，仅优化调制策略 $\pi_{\text{RFS}}$ 的 MLP 参数。Section 5.1.3 证实，将 RL 更新限制在初始噪声和残差项上比全量微调扩散/流模型（如 DPPO、ReinFlow）在所有任务上成功率至少高出 0.35，学习过程更加稳定。

2. **联合调制优于单一调制**：Table 1 的消融对比表明，同时使用潜变量调制与残差动作的 RFS 在所有六个仿真任务上均优于仅使用单一调制机制的 DSRL（仅输入调制）或残差 RL（仅输出调制）。例如在推至抓取任务上，RFS 成功率为 0.721，而 DSRL 仅为 0.430，Policy Decorator 仅为 0.176。

## 实验与分析

### 仿真主实验：RFS 在所有任务上显著领先

Table 1 汇总了 RFS 与 11 个基线方法在 6 个灵巧操作仿真任务上的成功率。RFS 在所有单个任务上均取得最高成功率，平均成功率高达 **0.861**，远超基础流匹配策略的 0.250 和最强非调制基线 IQL 的 0.488，提升幅度达 **+0.373**。在高精度 Stacking 任务上，RFS 达到 0.951，而最强输入调制基线 DSRL 仅为 0.135，差距高达 **+0.816**；在 Pouring 任务上，RFS 为 0.873，DSRL 为 0.268，差距同样显著。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/006_Table_1.jpg]]
*Table 1: Overall By jointly modulating the input and output of the base policy, RFS preserves base-policy performance while consistently improving upon it, achieving the highest success rates across all tasks: 0.89 (Grasping), 0.94 (Pick & Place), 0.78 (Packing), 0.72 (Push-to-Grasp), 0.95 (Stacking), and 0.87 (Pouring), with an average success rate of 0.87. Table 1: Success rates across tasks and RL methods*

全量微调扩散/流模型的 RL 方法（DPPO、ReinFlow）在所有任务上成功率均低于 0.50，表明直接对生成式策略的全量参数进行强化学习微调极不稳定。相比之下，RFS 将 RL 更新限制在初始噪声和残差项上，学习更稳定，在所有任务上成功率至少高出 0.35。

### 消融实验：联合调制的关键作用

Table 1 同时揭示了联合调制相对于单一调制的决定性优势。仅使用潜变量调制的 DSRL 和仅使用残差动作的 Policy Decorator / ResiP 在复杂任务上表现明显不足。以 Push-to-Grasp 为例，RFS 成功率为 0.721，DSRL 仅为 0.430，Policy Decorator 仅为 0.176。这一对比验证了核心设计原则：**输入调制实现全局行为模式切换，输出调制实现局部精细校正，二者缺一不可**。

在离线 RL 的 critic 设计消融中（Section 5.2.1），以完整组合动作 $a_b + a_r$ 作为 critic 输入优于仅使用 $a_r$ 或将 $[a_r, a_b]$ 拼接的替代方案，在稳定性和最终性能上均表现更好。

### 真机实验：已见与未见物体

Table 2 展示了在真实世界已见物体上的表现。RFS 的 pick-and-place 成功率达到 **90.0%**，抓取成功率达到 **80.0%**，均显著优于零样本迁移（50.0% / 43.3%）和监督微调（BC Finetuning, 70.0% / 70.0%）。值得注意的是，联合训练（Co-Training）在抓取任务上达到 83.3%，接近 RFS，但在 pick-and-place 上仅为 60.0%，远低于 RFS，说明联合训练难以同时兼顾两类任务，而 RFS 的调制策略具有更好的任务适应性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/007_Table_2.jpg]]
*Table 2: Performance on seen objects. Values report mean success rate with 95% confidence interval across trials*

在未见物体上（Figure 5），RFS 同样保持领先，pick-and-place 和抓取成功率均优于所有对比方法。这验证了 RFS 在有限人类纠正数据（50 条）下的泛化能力。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/008_Figure_5.jpg]]
*Figure 5: Real-world evaluation results on unseen objects. Bars show mean success rates for Pick-and-Place (left) and Grasping (right), with horizontal error bars denoting the 95% confidence interval. Numeric annotations report the mean success rate (±95% CI)*

### 失败模式与 RFS 修正效果

Figure 6 展示了零样本 sim-to-real 迁移中五种典型失败模式，包括：灵巧手过早闭合、抓取姿态松散或不稳定、pick-and-place 中动作时机错误或放置位置偏移。RFS 通过联合校正动作时序、抓取姿态和目标位置，有效修复了这些失败。例如，在抓取场景中，基础策略因手部闭合时机过早导致物体滑落，RFS 通过学习调整潜变量噪声延迟闭合动作，同时通过残差动作微调手指姿态，实现稳定抓取。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_Kt9tJeOwjy/figures/009_Figure_6.jpg]]
*Figure 6: Common failure modes in real-world manipulation and RFS corrections. We illustrate five representative failure cases of zero-shot sim-to-real transfer, including early hand closure, loose or unstable grasp poses, and mistimed or misplaced actions during pick-and-place. The top row shows failures produced by the zero-shot policy, while the bottom row shows the corrected outcomes after applying Residual Flow Steering (RFS). By jointly correcting action timing, grasp pose, and target location, RFS enables more stable and successful task execution*

## 方法谱系与知识库定位

### 1. 预训练生成式策略的RL微调谱系

RFS处于**预训练流匹配策略的强化学习微调**这一研究脉络中。该脉络的核心瓶颈在于：预训练的模仿学习策略在部署时缺乏泛化能力，而直接对生成式模型的全量参数进行RL微调不稳定。现有方法可沿两条轴分类：

**全量微调方法**直接更新扩散或流模型的全部参数：
- **DPPO**（Ren et al., 2024a）将扩散模型策略与PPO结合，对完整去噪轨迹进行RL更新。
- **ReinFlow**（Zhang et al., 2025a）针对流匹配策略进行全量RL微调。

RFS的实验表明（Section 5.1.3），将RL更新限制在初始噪声和残差项上，比全量微调在所有任务上的成功率高至少0.35，验证了参数冻结策略的稳定性优势。

**离线到在线RL方法**从离线数据预训练后在线微调：
- **IQL**（Kostrikov et al., 2021）和**AWAC**（Nair et al., 2021）是通用离线到在线RL算法。
- **Flow Q-Learning**（Park et al., 2025）将离线RL扩展到流模型策略。
- **RLPD**（Ball et al., 2023）和**IBRL**（Hu et al., 2024）利用演示数据辅助在线RL。

在仿真六任务平均成功率上，这些方法中表现最强的IQL仅达到0.488，远低于RFS的0.861（Table 1），表明通用RL方法难以有效利用预训练生成式策略的结构化先验。

### 2. 策略调制方法的统一视角

RFS的核心创新在于将**输入调制**与**输出调制**统一为联合优化框架（Section 4.1.1）。

**输入调制（潜变量控制）**：
- **DSRL**（Wagenmaker et al., 2025）仅学习初始潜变量噪声的分布，通过改变扩散/流模型的输入实现全局行为模式切换。DSRL在堆叠任务上仅达0.135，而RFS达0.951（Table 1），说明纯输入调制难以应对需要局部精细修正的高精度任务。

**输出调制（残差动作）**：
- **Policy Decorator**（Yuan et al., 2024）和**ResiP**（Ankile et al., 2024a）在基础策略输出上叠加学习的残差动作。Policy Decorator在推至抓取任务上仅达0.176，远低于RFS的0.721（Table 1），表明纯输出调制缺乏全局探索能力。

RFS通过联合优化潜变量噪声（输入调制）和残差动作（输出调制），使RL能够在不更新基础模型参数的前提下同时实现全局行为适应与局部精细校正。这一设计直接回应了单一调制策略的互补性缺陷：输入调制擅长模式切换但缺乏精度，输出调制擅长局部修正但探索能力受限。

### 3. 真实世界适应方法的对比

在Sim-to-Real迁移阶段，RFS采用**基于人类纠正数据的离线RL微调**（TD3+BC），与以下基线形成对比（Table 2）：

- **零样本迁移（Zero-Shot Transfer）**：直接部署仿真训练策略，已见物体上抓取成功率仅43.3%，pick-and-place仅50.0%。
- **监督微调（BC Finetuning）**：在少量人类数据上进行行为克隆，但缺乏奖励信号的引导。
- **联合训练（Co-Training）**：在人类数据上联合训练，抓取成功率达83.3%，但pick-and-place仅60.0%。

RFS的离线RL微调在已见物体上达到90.0% pick-and-place和80.0%抓取成功率（Table 2），其优势在于：利用奖励信号（通过SAM2分割和质心跟踪自动计算）而非仅模仿人类动作，同时通过TD3+BC的行为克隆正则项约束残差动作不会偏离基础策略过远（Eq. 11）。所有比较方法使用相同数量的50条人类纠正数据，确保公平性。

### 4. 适用边界与局限

**已知适用条件**：
- 基础策略需为预训练的流匹配或扩散模型策略，提供初步协调行为。
- 任务需可定义明确的奖励函数（仿真中为抓取成功与稳定性，真实世界通过SAM2自动计算）。
- 真实世界适应目前仅支持离线微调，需要收集人类纠正数据。

**已识别的局限**（Section 6）：
1. **感知能力受限**：当前方法仅依赖点云观测，在杂乱或需要语义理解的场景中性能未知。
2. **离线适应限制**：真实世界微调为离线阶段，缺乏在线学习能力，无法在部署过程中动态响应环境变化。
3. **平台与任务范围有限**：仅在单一Franka-Leap Hand平台和六类操作任务上验证，尚未扩展到移动操作或双手操作场景。

### 5. 开放问题

1. **语义信息融合**：如何将语言指令或语义理解融入RFS框架，以应对更复杂的操作场景？
2. **安全在线微调**：能否设计安全的在线微调机制，使策略在真实世界部署过程中持续改进？
3. **多任务与少样本扩展**：RFS的联合调制机制能否推广到多任务或少样本学习场景？

> **注意**：关于RFS与其他调制方法在理论上的统一性分析（如是否可纳入更广义的策略蒸馏框架），以及该方法在更大规模任务集上的泛化性能，论文未提供直接证据，需进一步研究验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/RFS_Reinforcement_learning_with_Residual_flow_steering_for_dexterous_manipulation.pdf]]
