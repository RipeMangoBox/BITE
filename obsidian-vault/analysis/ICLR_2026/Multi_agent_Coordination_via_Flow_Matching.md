---
title: "Multi-agent Coordination via Flow Matching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multi_agent_Coordination_via_Flow_Matching.pdf
project_link: null
code_link: https://github.com/DongsuLeeTech/mac-flow
openreview_forum_id: 2L6MffR0ut
aliases:
- MF
- MACFM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用流匹配（flow matching）对联合行为分布进行建模，并通过两阶段策略蒸馏与IGM原理引导，将表达力强的联合流策略分解为高效的单步采样策略，从而在保持协调能力的同时将推理复杂度降至O(1)。"
primary_logic: "MAC-Flow将表达力学习与价值优化解耦：第一阶段通过流匹配的行为克隆学习丰富的联合分布，第二阶段在IGM约束下同时最大化全局Q值和最小化BC蒸馏损失，并借助Wasserstein距离上界保证性能退化可控，实现了性能与推理速度的帕累托改善。"
claims:
- "MAC-Flow在SMAC基准上实现约14.5倍推理加速，同时保持与扩散方法可比或更优的性能（SMACv1平均回报15.6与DoF持平，SMACv2平均回报14.2超越DoF）。"
- "在连续控制基准MA-MuJoCo和MPE上，MAC-Flow平均回报显著超过扩散基线MADiff（MA-MuJoCo 2749.4 vs 2430.2，MPE 65.8 vs 49.2）。"
- "理论分析表明，蒸馏损失通过2-Wasserstein距离上界联合策略与因子化策略的分布差异，进而由Q函数的Lipschitz性质控制价值函数的性能差距（Proposition 4.2、4.3），且教学实验验证了该界限的紧密性。"
- "SMACv1 & SMACv2 (discrete control) 上 Average Return, Inference Speed = SMACv1 avg 15.6, SMACv2 avg 14.2; inference ~4ms"
---

# Multi-agent Coordination via Flow Matching

> [!tip] 核心洞察
> MAC-Flow将表达力学习与价值优化解耦：第一阶段通过流匹配的行为克隆学习丰富的联合分布，第二阶段在IGM约束下同时最大化全局Q值和最小化BC蒸馏损失，并借助Wasserstein距离上界保证性能退化可控，实现了性能与推理速度的帕累托改善。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于流匹配的多智能体协调 |
| 英文题名 | Multi-agent Coordination via Flow Matching |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2L6MffR0ut) · [GitHub](https://github.com/DongsuLeeTech/mac-flow) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MAC-Flow |
| Dataset | SMACv1 & SMACv2 (discrete control), MA-MuJoCo (continuous control, 4 tasks, 16 datasets), MPE Spread (continuous control) |

> [!tip] 效果简介
> - SMACv1 & SMACv2 (discrete control) 上，Average Return, Inference Speed 为 SMACv1 avg 15.6, SMACv2 avg 14.2; inference ~4ms，对比 DoF: SMACv1 avg 15.6, SMACv2 avg 13.2; inference ~50ms，变化 Comparable performance with ~14.5x inference speedup。
> - MA-MuJoCo (continuous control, 4 tasks, 16 datasets) 上，Average Return 为 2749.4，对比 MADiff: 2430.2，变化 +319.2。
> - MPE Spread (continuous control) 上，Average Normalized Score 为 65.8，对比 MADiff: 49.2，变化 +16.6。

## 概要

离线多智能体强化学习的核心瓶颈在于**联合动作分布的表达力与推理效率之间的根本冲突**：扩散模型能够捕获复杂的多模态协调模式，但每步推理需数十次网络前传；高斯策略推理仅需单步，却无法表达多智能体间的依赖结构。现有方法始终在“表达力”与“实时推理”之间做权衡，缺乏同时兼顾二者的解决方案。

**MAC-Flow** 通过“表达力学习与价值优化解耦”的策略打破这一僵局。其核心思路分两阶段：第一阶段利用流匹配（flow matching）对联合动作分布进行行为克隆，以联合观测为条件训练速度场，捕获丰富的多智能体交互模式；第二阶段在IGM（Individual-Global-Max）原理约束下，将联合流策略蒸馏为每个智能体的单步采样策略，同时最大化全局Q值并最小化BC蒸馏损失。这一设计使推理复杂度从扩散方法的 $O(K)$ 降至 $O(1)$，与高斯策略相当，同时借助Wasserstein距离上界与Q函数的Lipschitz性质，为蒸馏过程的性能退化提供了理论保证。

**主要结果**：在SMAC基准上，MAC-Flow实现了约**14.5倍推理加速**（~4ms vs ~50ms），同时保持与扩散方法可比或更优的性能（SMACv1平均回报15.6，SMACv2平均回报14.2）。在连续控制基准MA-MuJoCo和MPE上，平均回报显著超越扩散基线MADiff（MA-MuJoCo 2749.4 vs 2430.2，MPE 65.8 vs 49.2）。消融实验进一步验证了IGM引导的个体Critic训练、两阶段蒸馏设计以及联合流策略BC的必要性。

**方法定位**：MAC-Flow属于集中训练-分散执行框架下的离线MARL方法，其方法谱系与知识库定位详见后续章节。

### 离线多智能体强化学习的核心挑战

多智能体强化学习（MARL）在现实场景（如机器人编队、交通控制）中面临严峻的样本效率与安全性约束，离线学习范式因此成为关键路径。然而，离线MARL的核心瓶颈并非单纯的数据稀缺，而在于**联合行为分布的表达力与推理效率之间的根本性权衡**：

- **扩散策略（Diffusion Policy）**：通过多步去噪过程建模联合动作分布，能捕获复杂的多模态协调模式，但每步推理需 $O(K)$ 甚至 $O(IK)$ 次网络前传（$K$ 为去噪步数，$I$ 为智能体数量），在实时决策场景中难以部署。
- **高斯策略（Gaussian Policy）**：仅需单次前传（$O(1)$），推理极快，但其单峰假设无法表达离线数据中普遍存在的多模态交互结构，导致协调能力显著退化。
- **现有方法**：要么追求表达力而牺牲速度（如 **DoF**, Zhu et al., 2024；**MADiff**, Li et al., 2025a），要么追求效率而放弃多模态建模（如 **MABCQ**, Yang et al., 2021；**MACQL**, Kumar et al., 2020），缺乏同时兼顾两者的统一方案。

这一权衡的根源在于：**表达力学习与策略优化被耦合在同一阶段**。扩散方法试图直接在价值函数梯度上优化多步采样过程，导致训练不稳定且推理代价高昂；而高斯方法则因参数化限制，从一开始就放弃了复杂分布的建模能力。

### 流匹配的机遇与未解决的问题

流匹配（Flow Matching）作为一类新兴的生成建模范式，通过直接学习速度场将简单先验分布连续变换为目标分布，在单步采样效率与分布表达力之间展现出独特优势。然而，将其应用于离线MARL面临两个未解问题：

1. **如何将流匹配的表达力注入多智能体协调结构？** 独立建模每个智能体的流策略会丧失联合依赖信息，而集中式流策略虽能捕获交互，却无法直接用于分散执行。
2. **如何在不破坏分布表达力的前提下实现策略因子化？** 直接对联合流策略施加价值函数梯度优化会破坏其分布结构，导致模式坍塌或训练崩溃。

### 本文动机：解耦表达力学习与策略优化

针对上述缺口，本文提出 **MAC-Flow**，核心动机是**将表达力学习与价值优化解耦为两个独立阶段**：

- **第一阶段**：通过流匹配的行为克隆（Flow-BC），从离线数据中学习一个表达力强的联合动作分布，完整捕获智能体间的多模态协调模式。
- **第二阶段**：在 IGM（Individual-Global-Max）原理约束下，将联合流策略蒸馏为每智能体的单步采样策略，同时最大化全局 Q 值，实现集中训练与分散执行的统一。

这一解耦设计的关键洞察在于：**蒸馏损失通过 2-Wasserstein 距离上界联合策略与因子化策略的分布差异，进而由 Q 函数的 Lipschitz 性质控制性能退化**（Proposition 4.2、4.3），从而在理论上保证了因子化过程的可控性。最终，MAC-Flow 在保持与扩散方法可比甚至更优性能的同时，将推理复杂度降至 $O(1)$，实现了性能与推理速度的帕累托改善（Figure 1）。

## 核心方法与创新机理

MAC-Flow的核心创新在于**将表达力学习与价值优化解耦**，通过两阶段流程系统性地解决了离线多智能体强化学习中“联合动作分布表达力”与“推理效率”之间的根本性权衡。这一设计在三个关键维度上相对于既有基线实现了结构性改变。

### 联合行为建模与协调机制：从“直接优化”到“先学后分”

现有方法在联合策略建模上呈现两极分化：**高斯策略**（如MABCQ、MACQL）通过独立分布配合IGM值分解实现$O(1)$推理，但无法捕获联合动作空间中的多模态依赖；**扩散策略**（如MADiff、DoF）虽能从离线数据中学习复杂的联合分布，却将表达力学习与价值最大化耦合在同一个迭代去噪过程中，导致优化不稳定且推理需$O(K)$步网络前传。

MAC-Flow将这一耦合拆解为两个独立阶段（Figure 2）：

- **第一阶段**：纯粹通过流匹配行为克隆（Flow-BC）学习联合动作分布，速度场$v_\phi(t, \mathbf{o}, \mathbf{x}^t)$以联合观测为条件，训练目标为
  $$\mathcal{L}_{\mathrm{Flow-BC}}(\phi) = \mathbb{E}_{\mathbf{x}^0 \sim \mathbf{p}_0, (\mathbf{o}, \mathbf{a}) \sim \mathcal{D}, t \sim \mathrm{Unif}([0,1])} \left[ \| v_\phi(t, \mathbf{o}, \mathbf{x}^t) - (\mathbf{a} - \mathbf{x}^0) \|_2^2 \right]$$
  此阶段仅关注分布拟合，不涉及任何价值信号，从而避免了扩散方法中直接对$Q$函数求梯度带来的不稳定性。

- **第二阶段**：在IGM原理指导下，将联合流策略蒸馏为个体单步采样策略$\mu_{w_i}(o_i, z_i)$。蒸馏目标同时最大化全局$Q_{\mathrm{tot}}$并最小化与联合策略的BC蒸馏损失：
  $$\mathcal{L}_\pi(\mathbf{w}) = \mathbb{E}_{\mathbf{o} \sim \mathcal{D}, \mathbf{a} \sim \pi_{\mathbf{w}}, \mathbf{z} \sim \mathbf{p}_0} \left[ -Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a}) + \alpha \sum_{i=1}^{I} \| \mu_{w_i}(o_i, z_i) - [\mu_\phi(\mathbf{o}, \mathbf{z})]_i \|_2^2 \right]$$
  超参数$\alpha$平衡价值最大化与分布保真度。这种“集中训练、分散执行”的范式使得个体策略在推理时仅需单次前传，同时继承了联合流策略捕获的协调模式。

### 推理效率：从$O(K)$到$O(1)$的阶跃改善

扩散基线的推理瓶颈源于迭代去噪：每步需$K$次网络前传（如DoF的$K=5$），若每智能体独立扩散则复杂度升至$O(IK)$。MAC-Flow通过蒸馏将推理压缩为**每智能体单次前传$O(1)$**，总推理时间约4ms，相比扩散基线实现约**14.5倍加速**（Figure 1, Table 3），同时与高斯策略的推理速度相当。这一改善不牺牲性能：在SMACv1上平均回报15.6（与DoF持平），SMACv2上平均回报14.2（超越DoF的13.2）。

### 表达力与优化稳定性：Wasserstein距离保证的可控退化

将联合策略因子化为个体策略必然引入分布差异。MAC-Flow通过理论分析为这一退化提供了上界保证：

- **Proposition 4.2** 证明蒸馏损失的平方根构成2-Wasserstein距离的上界：
  $$W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_\phi(\mathbf{o})) \leq \left( \mathbb{E}_{\mathbf{z} \sim \mathbf{p}_0} \| \mu_{\mathbf{w}}(\mathbf{o}, \mathbf{z}) - \mu_\phi(\mathbf{o}, \mathbf{z}) \|_2^2 \right)^{1/2}$$

- **Proposition 4.3** 进一步将性能差距（期望$Q$值之差）与Wasserstein距离关联：
  $$\left| \mathbb{E}_{\mathbf{a} \sim \pi_{\mathbf{w}}(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] - \mathbb{E}_{\mathbf{a} \sim \pi_\phi(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] \right| \leq L_Q \cdot W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_\phi(\mathbf{o}))$$
  其中$L_Q$为$Q$函数的Lipschitz常数。

教学实验（Figure 3）验证了这一界限的紧密性：所有训练检查点的经验价值差距均位于理论Lipschitz上界之下，且蒸馏损失与价值差距同步下降。这意味着**蒸馏过程中的性能退化是可控且有理论保证的**，而非启发式近似。

### 消融证据支撑

消融实验进一步验证了各创新组件的必要性（Figure 6, Figure 7, Figure 8, Figure 10）：

- **移除蒸馏阶段或RL目标**（仅保留BC或仅最大化$Q$）均导致性能大幅下降。
- **IGM约束的个体Critic**在性能和$Q$估计稳定性上始终优于非IGM变体及集中式Critic。
- **联合流策略**在第一阶段优于独立流策略，且MAC-Flow显著超越其朴素变体MA-FQL（分散流+独立$Q$），验证了联合BC与IGM Critic协同设计的必要性。

综上，MAC-Flow通过“流匹配联合建模→IGM约束蒸馏”的两阶段解耦设计，在保持扩散级表达力的同时实现了高斯级的推理效率，并以Wasserstein距离理论为蒸馏退化提供了可量化的安全边界。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/002_Figure_2.jpg]]
*Figure 2: Overview diagram of proposed solution. Our solution, MAC-Flow, composes of two stages. The first stage models the joint action distribution via flow-matching to capture inter-agent dependencies, thereby facilitating the extraction of coordination behaviors more effectively than treating individual policies. For the next stage, individual critics are trained under the individual-global-max principle, thereby embedding behaviors for multi-agent coordination. At the second stage, practicality is highlighted by deriving individual policies for decentralized execution from a flow-based joint policy via Q maximization and BC distillation*

MAC-Flow 采用**两阶段解耦架构**，将联合行为表达力学习与价值优化分离，从而在保持多智能体协调能力的同时实现高效的单步推理。其核心洞察是：离线多智能体数据中蕴含的复杂联合动作分布可以通过流匹配（flow matching）精确捕获，而无需在推理时承担扩散模型的多步去噪开销；随后通过 IGM 原理引导的策略蒸馏，将这一表达力强的联合流策略分解为可分散执行的个体策略。

### 两阶段流水线

**第一阶段：联合流策略的行为克隆（Flow-BC）**

该阶段以集中式方式训练一个基于流匹配的联合策略 $\mu_{\phi}(\mathbf{o}, \mathbf{z})$，其中 $\mathbf{o}$ 为所有智能体的联合观测，$\mathbf{z} \sim \mathbf{p}_0$ 为从先验分布（如标准高斯）采样的噪声。训练目标为流匹配 BC 损失：

$$\mathcal{L}_{\mathrm{Flow-BC}}(\phi) = \mathbb{E}_{\mathbf{x}^0 \sim \mathbf{p}_0, (\mathbf{o}, \mathbf{a}) \sim \mathcal{D}, t \sim \mathrm{Unif}([0,1])} \left[ \| v_{\phi}(t, \mathbf{o}, \mathbf{x}^t) - (\mathbf{a} - \mathbf{x}^0) \|_2^2 \right]$$

该损失使速度场 $v_{\phi}$ 学习从噪声到目标联合动作的位移方向，从而隐式建模多智能体间的交互依赖与多模态分布。此阶段**仅做行为克隆**，不涉及价值函数优化，避免了直接对扩散策略进行梯度优化时的不稳定性。

**第二阶段：个体策略蒸馏与价值最大化**

在联合流策略冻结后，第二阶段完成两项任务：

1. **IGM 个体 Critic 训练**：基于 IGM 原理训练每智能体的局部 Q 函数 $\{Q_{\theta_i}\}$，保证个体最优动作的集合等价于全局最优动作：
   $$\underset{\mathbf{a}}{\arg\max}\ Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a}) = \left( \underset{a_1}{\arg\max}\ Q_1(o_1, a_1), \dots, \underset{a_I}{\arg\max}\ Q_I(o_I, a_I) \right)$$
   这为后续的因子化策略提供了协调行为嵌入。

2. **单步策略蒸馏**：通过同时最大化全局 Q 值和最小化 BC 蒸馏损失，将联合流策略蒸馏为每智能体的单步采样策略 $\mu_{w_i}$：
   $$\mathcal{L}_{\pi}(\mathbf{w}) = \mathbb{E}_{\mathbf{o} \sim \mathcal{D}, \mathbf{a} \sim \pi_{\mathbf{w}}, \mathbf{z} \sim \mathbf{p}_0} \left[ -Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a}) + \alpha \sum_{i=1}^{I} \| \mu_{w_i}(o_i, z_i) - [\mu_{\phi}(\mathbf{o}, \mathbf{z})]_i \|_2^2 \right]$$
   其中超参数 $\alpha$ 平衡价值最大化与分布对齐。蒸馏损失直接对齐个体策略输出与联合流策略的对应分量，使因子化后的策略尽可能保留原始联合分布的协调模式。

### 模块关系与输入输出流

整体框架（Figure 2）的数据流如下：

- **离线数据集** $\mathcal{D} = \{(\mathbf{o}, \mathbf{a}, \mathbf{o}', \mathbf{r})\}$ 同时供给三个阶段：联合流 BC 训练、个体 Critic 训练、策略蒸馏。
- **联合流策略模块**：以联合观测 $\mathbf{o}$ 和噪声 $\mathbf{z}$ 为输入，经 ODE 求解器（M 步离散化）输出联合动作 $\mathbf{a}$。该模块仅在训练阶段使用，推理时被个体策略替代。
- **个体 Critic 模块**：每智能体拥有独立的 Q 网络，以局部观测 $o_i$ 和动作 $a_i$ 为输入，通过 IGM 约束的 TD 学习训练。
- **个体策略模块**：每智能体的单步策略 $\mu_{w_i}$ 以局部观测 $o_i$ 和独立噪声 $z_i$ 为输入，直接输出动作。推理时每智能体仅需一次前传，时间复杂度为 $O(1)$。

### 理论保证

蒸馏过程的理论基础由两个命题支撑：

- **Proposition 4.2**（Wasserstein 上界）：联合策略 $\pi_{\phi}$ 与因子化策略 $\pi_{\mathbf{w}}$ 之间的 2-Wasserstein 距离被蒸馏损失的平方根所上界：
  $$W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_{\phi}(\mathbf{o})) \leq \left( \mathbb{E}_{\mathbf{z} \sim \mathbf{p}_0} \| \mu_{\mathbf{w}}(\mathbf{o}, \mathbf{z}) - \mu_{\phi}(\mathbf{o}, \mathbf{z}) \|_2^2 \right)^{1/2}$$

- **Proposition 4.3**（性能差距上界）：若 $Q_{\mathrm{tot}}$ 关于动作是 $L_Q$-Lipschitz 连续的，则因子化策略与联合策略的期望 Q 值差距被 Wasserstein 距离控制：
  $$\left| \mathbb{E}_{\mathbf{a} \sim \pi_{\mathbf{w}}(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] - \mathbb{E}_{\mathbf{a} \sim \pi_{\phi}(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] \right| \leq L_Q \cdot W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_{\phi}(\mathbf{o}))$$

教学实验（Figure 3）验证了这些界限的紧密性：蒸馏损失与价值差距同步下降，所有检查点的经验价值差距均低于理论 Lipschitz 上界，表明蒸馏过程的性能退化可控。

### 关键设计选择

消融实验确认了以下设计选择的必要性：

- **联合流策略优于个体流策略**（Figure 9）：第一阶段使用联合流策略能更有效地捕获智能体间的交互依赖，且降低了样本复杂度和内存开销。
- **IGM 个体 Critic 优于集中式 Critic**（Figure 8）：IGM 约束下的个体 Critic 训练带来更高且更稳定的学习曲线。
- **蒸馏阶段与 RL 目标缺一不可**（Figure 6）：移除蒸馏阶段或 Q 最大化目标均导致显著的性能退化。
- **IGM 原理对协调至关重要**（Figure 14）：在纯协同博弈中，无 IGM 约束的因子化策略无法恢复正确的协调模式。

### 局限性

MAC-Flow 的性能保证依赖于两个关键假设：Q 函数的 Lipschitz 连续性与 IGM 可分解性。在强交互、反协同场景（如 XOR 任务，Figure 15）中，IGM 原理失效，导致蒸馏策略退化为近似均匀的乘积分布。此外，超参数 $\alpha$ 对性能敏感，需针对不同任务仔细调节。

### 4.1 两阶段架构概览

MAC-Flow 的核心设计遵循“表达力学习与价值优化解耦”的原则，将多智能体离线强化学习分解为两个阶段（Figure 2）：

- **第一阶段（联合流策略行为克隆）**：以联合观测 $\mathbf{o} = (o_1, \dots, o_I)$ 为条件，通过流匹配学习一个联合动作分布的速度场 $v_\phi(t, \mathbf{o}, \mathbf{x}^t)$，从而捕获离线数据集中智能体间的交互依赖与多模态协调模式。
- **第二阶段（策略蒸馏与因子化）**：在 IGM 原则下训练个体 Critic $\{Q_{\theta_i}\}_{i=1}^I$，随后将联合流策略 $\mu_\phi(\mathbf{o}, \mathbf{z})$ 蒸馏为一组个体单步采样策略 $\{\mu_{w_i}(o_i, z_i)\}_{i=1}^I$，通过同时最大化全局 Q 值与最小化 BC 蒸馏损失实现集中训练、分散执行。

这种解耦使表达力学习（流匹配 BC）与价值最大化（RL 蒸馏）互不干扰，避免了扩散方法中直接对价值函数梯度优化带来的不稳定性。

### 4.2 第一阶段：联合流策略的行为克隆

流匹配的核心思想是训练一个速度场 $v_\phi$，使其能够通过 ODE 将简单先验分布 $\mathbf{p}_0$ 中的样本连续地变换为目标数据分布中的样本。通用流匹配训练目标为：

$$\mathcal{L}(\phi) = \mathbb{E}_{x^0 \sim p_0,\ x^1 \sim p_1,\ t \sim \mathrm{Unif}([0,1])} \left[ \| v_\phi(t, x^t) - (x^1 - x^0) \|_2^2 \right] \tag{4}$$

其中 $x^t = (1-t)x^0 + t x^1$ 为线性插值路径上的中间点，速度场被训练为匹配从噪声到目标样本的位移向量。

将上述框架扩展到多智能体策略学习，MAC-Flow 在第一阶段以联合观测 $\mathbf{o}$ 为条件，定义联合流策略 BC 损失：

$$\mathcal{L}_{\mathrm{Flow-BC}}(\phi) = \mathbb{E}_{\mathbf{x}^0 \sim \mathbf{p}_0,\ (\mathbf{o}, \mathbf{a}) \sim \mathcal{D},\ t \sim \mathrm{Unif}([0,1])} \left[ \| v_\phi(t, \mathbf{o}, \mathbf{x}^t) - (\mathbf{a} - \mathbf{x}^0) \|_2^2 \right] \tag{6}$$

- **变量含义**：$\mathbf{x}^0$ 为从先验 $\mathbf{p}_0$（标准高斯）采样的噪声；$\mathbf{a}$ 为数据集 $\mathcal{D}$ 中的联合动作；$t$ 为均匀采样的时间步；$v_\phi(t, \mathbf{o}, \mathbf{x}^t)$ 为以联合观测为条件的速度场网络。
- **作用**：训练后的速度场通过 ODE 求解器（如 Euler 方法，$M$ 步，步长 $d=1/M$）可将噪声 $\mathbf{z} \sim \mathbf{p}_0$ 变换为联合动作样本，从而获得联合流策略 $\mu_\phi(\mathbf{o}, \mathbf{z})$。

### 4.3 IGM 原理与个体 Critic 训练

为保证个体策略的最优性与全局最优性一致，MAC-Flow 采用 IGM（Individual-Global-Max）原理训练个体 Critic：

$$\underset{\mathbf{a}}{\arg\max}\ Q_{\mathrm{tot}}(\pmb{o}, \mathbf{a}) = \left( \underset{a_1}{\arg\max}\ Q_1(o_1, a_1), \dots, \underset{a_I}{\arg\max}\ Q_I(o_I, a_I) \right) \tag{1}$$

该原理确保全局 Q 函数的 argmax 等于各智能体局部 Q 函数 argmax 的元组。个体 Critic 通过标准 TD-error 损失进行训练，并采用目标网络 $\bar{\theta}_i$ 稳定优化。

### 4.4 第二阶段：策略蒸馏与因子化

第二阶段的核心是将联合流策略 $\mu_\phi(\mathbf{o}, \mathbf{z})$ 分解为个体单步采样策略 $\mu_{w_i}(o_i, z_i)$（每智能体仅需一次网络前传，推理复杂度 $O(1)$）。蒸馏损失定义为：

$$\mathcal{L}_{\mathrm{Distil-Flow}}(\mathbf{w}) = \mathbb{E}_{\mathbf{o} \sim \mathcal{D}, \mathbf{z} \sim \mathbf{p}_0} \Bigg[ \sum_{i=1}^{I} \big\| \mu_{w_i}(o_i, z_i) - [\mu_\phi(\mathbf{o}, \mathbf{z})]_i \big\|_2^2 \Bigg] \tag{7}$$

- **变量含义**：$\mu_{w_i}(o_i, z_i)$ 为第 $i$ 个智能体的个体策略输出；$[\mu_\phi(\mathbf{o}, \mathbf{z})]_i$ 为联合流策略输出的第 $i$ 个分量。
- **作用**：将每个智能体的单步策略输出与联合流策略的对应分量对齐，实现从集中式联合分布到分散式因子化分布的迁移。

因子化个体策略的完整训练目标为：

$$\mathcal{L}_\pi(\mathbf{w}) = \mathbb{E}_{\mathbf{o} \sim \mathcal{D}, \mathbf{a} \sim \pi_{\mathbf{w}}, \mathbf{z} \sim \mathbf{p}_0} \left[ -Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a}) + \alpha \sum_{i=1}^{I} \| \mu_{w_i}(o_i, z_i) - [\mu_\phi(\mathbf{o}, \mathbf{z})]_i \|_2^2 \right] \tag{9}$$

- **变量含义**：$\pi_{\mathbf{w}}$ 为由个体策略乘积构成的因子化联合策略；$Q_{\mathrm{tot}}$ 为通过 IGM 混合网络聚合的全局 Q 值；$\alpha$ 为平衡 RL 目标与蒸馏损失的权衡超参数。
- **作用**：在最大化全局 Q 值的同时，通过 BC 蒸馏损失约束个体策略不偏离原始联合分布，从而在保持协调能力的前提下实现高效分散执行。

### 4.5 蒸馏过程的理论保证

MAC-Flow 通过两个命题为蒸馏过程提供了理论保障。

**命题 4.2（2-Wasserstein 上界）**：因子化策略 $\pi_{\mathbf{w}}(\mathbf{o})$ 与联合流策略 $\pi_\phi(\mathbf{o})$ 之间的 2-Wasserstein 距离被蒸馏损失的平方根所上界：

$$W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_\phi(\mathbf{o})) \leq \Big( \mathbb{E}_{\mathbf{z} \sim \mathbf{p}_0} \| \mu_{\mathbf{w}}(\mathbf{o}, \mathbf{z}) - \mu_\phi(\mathbf{o}, \mathbf{z}) \|_2^2 \Big)^{1/2}$$

- **含义**：蒸馏损失直接量化了因子化策略与原始联合策略之间的分布差异，最小化蒸馏损失即最小化该差异的上界。

**命题 4.3（Lipschitz 值函数性能差距界）**：假设 $Q_{\mathrm{tot}}$ 关于动作 $\mathbf{a}$ 满足 $L_Q$-Lipschitz 连续，则因子化策略与联合策略的期望 Q 值差距满足：

$$\Big| \mathbb{E}_{\mathbf{a} \sim \pi_{\mathbf{w}}(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] - \mathbb{E}_{\mathbf{a} \sim \pi_\phi(\mathbf{o})} [Q_{\mathrm{tot}}(\mathbf{o}, \mathbf{a})] \Big| \leq L_Q W_2(\pi_{\mathbf{w}}(\mathbf{o}), \pi_\phi(\mathbf{o})) \leq L_Q \sqrt{ \mathbb{E}_{\mathbf{z} \sim \mathbf{p}_0} \| \mu_{\mathbf{w}}(\mathbf{o}, \mathbf{z}) - \mu_\phi(\mathbf{o}, \mathbf{z}) \|_2^2 }$$

- **含义**：性能退化（期望 Q 值之差）由 Lipschitz 常数 $L_Q$ 与 Wasserstein 距离共同控制，而 Wasserstein 距离又被蒸馏损失上界。因此，最小化蒸馏损失可控制性能退化在可接受范围内。Figure 3 的教学实验验证了该界限的紧密性：在所有检查点上，经验值差距均保持在理论 Lipschitz 上界之下。

**关键假设与局限**：上述保证依赖于两个前提——(1) Q 函数的 Lipschitz 连续性；(2) IGM 可分解性假设。在强交互、反协同场景（如 XOR 任务，Figure 15）中，IGM 原理失效，因子化策略会退化为近似均匀的积分布，性能大幅下降。

## 实验与关键发现

### 核心性能与推理速度权衡

MAC-Flow在主流多智能体离线强化学习基准上实现了性能与推理速度的帕累托改善。Figure 1以散点图形式汇总了各算法在SMACv1与SMACv2共18个数据集上的聚合表现：MAC-Flow位于图左上角（推理时间约4ms，平均回报约14.5），在保持与先前最优扩散方法DoF可比性能（SMACv1平均回报15.6持平，SMACv2平均回报14.2超越DoF的13.2）的同时，实现了约14.5倍推理加速（Table 1, Figure 4）。推理时间复杂度分析（Table 3）表明，高斯策略与MAC-Flow的每智能体推理复杂度均为O(1)，而扩散方法需O(K)或O(IK)次网络前传。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/007_Table_1.jpg]]
*Table 1: Performance evaluation for discrete action control. We present a performance comparison across 2 benchmarks, 8 tasks, and 18 datasets. These results are averaged over 6 seeds, and we report the two standard deviations after the ± sign. We highlight the best performance in bold and the second best in underlined*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/001_Figure_1.jpg]]
*Figure 1: TL;DR: MAC-Flow alleviates performance-inference time trade-off, achieving a 14.5x speedup compared to SOTA Performance. vs. Inference time. (Benchmarks: SMACv1 and SMACv2) Figure 1: Summary of results. This summarizes performance vs. inference speed for selected algorithms on widely-used MARL benchmarks, SMACv1 and SMACv2. We plot aggregate mean performance and inference time across 18 datasets for 8 scenarios related to the SMAC maps. More precisely, we measure inference time based on the total computation performed by each algorithm and report it by using milliseconds (ms) unit and log scale, where a higher value indicates greater computational cost. As a result, our proposed solution, M...*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/009_Figure_4.jpg]]
*Figure 4: Inference time. These results are averaged over each benchmark’s scenarios*

在连续控制基准上，MAC-Flow的优势更为显著。Table 2显示，在MA-MuJoCo的4个任务16个数据集上，MAC-Flow平均回报达2749.4，显著超越扩散基线MADiff的2430.2（+319.2）；在MPE Spread任务上，归一化得分65.8对比MADiff的49.2（+16.6）。值得注意的是，MAC-Flow的训练墙钟时间虽比纯高斯策略有所增加，但仍远快于扩散基线（Figure 11）。

### 消融研究的关键发现

消融实验从多个维度验证了MAC-Flow各组件的必要性：

**蒸馏阶段与RL目标的必要性。** Figure 6表明，移除蒸馏阶段（仅保留BC流匹配）或移除Q最大化RL目标（仅做蒸馏）均导致性能大幅退化。这验证了两阶段设计中“表达力学习与价值优化解耦”的核心思想——单独依赖BC无法利用最优行为信息，单独依赖RL目标则可能偏离数据支持分布。

**IGM原理对Critic训练的关键作用。** Figure 7显示，基于IGM原理训练的个体Critic在性能和Q估计稳定性上均优于非IGM变体。Figure 8进一步对比了IGM个体Critic与集中式Critic的差异：IGM个体Critic持续获得更高回报且学习曲线更稳定，这归因于IGM原理保证了个体最优与全局最优的一致性（Equation 1），使因子化策略的优化目标与联合策略保持对齐。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/015_Figure_7.jpg]]
*Figure 7: Ablation study for RQ5. This figure shows the learning curves for performance and Q value. Performance’s y-axes of MA-MuJoCo and MPE are scaled as 1000 and 20 units, respectively*

**联合流策略的必要性。** Figure 9表明，第一阶段使用联合流策略（而非个体流策略）能带来性能增益，尤其在需要强协调的场景中。Figure 10将MAC-Flow与MA-FQL（去中心化流策略+独立Q学习）对比，MAC-Flow在所有基准上显著领先，验证了联合BC捕获智能体间依赖与IGM引导因子化的协同必要性。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_2L6MffR0ut/figures/023_Figure_10.jpg]]
*Figure 10: Performance comparison with MA-FQL. We compare our solution and the naive extension of the FQL across four benchmarks. The reported point and shaded area represent the average and tolerance interval from 6 random seeds*

### 理论验证的教学实验

Figure 3通过一个教学示例验证了理论分析的核心命题。Figure 3(a)显示蒸馏损失与价值差距（联合策略与因子化策略的期望Q值之差）在训练过程中同步下降，表明蒸馏确实在缩小分布差异的同时改善了策略质量。Figure 3(b)揭示了一个关键动态：联合策略的智能体间互信息在训练初期较高（捕获了强协调依赖），随后逐渐降低；而因子化策略的互信息始终维持在接近零的水平，反映了其独立采样的结构约束。Figure 3(c)证实了Proposition 4.3的紧密性——经验价值差距始终位于Lipschitz理论上界之下，所有检查点的散点图（Figure 3(d)）均未突破理论界限。这为蒸馏过程的性能退化提供了可控性保证。

### 失败模式与局限性

尽管MAC-Flow在多数基准上表现优异，分析揭示了其根本性局限：

**IGM可分解性假设的失效。** 在XOR压力测试（Figure 15）中，数据集包含两个反协同模式（(0,1)和(1,0)），联合流策略成功恢复了这一不可因子化的结构，但因子化策略退化为近似均匀的乘积分布。这是因为IGM原理要求全局最优动作可分解为个体最优动作的元组，而XOR场景的协调结构违背了这一前提。Figure 16的收益博弈实验进一步量化了交互强度对蒸馏的影响：随着智能体间交互强度增加，联合策略与因子化策略的Wasserstein距离增大，性能差距也随之扩大。

**超参数敏感性。** 蒸馏损失权重α需要在不同任务间仔细调节，对最终性能影响敏感。这一观察在Figure 6的消融中有所体现——α平衡了Q最大化与BC蒸馏两个目标，过大或过小均会导致性能下降。

**离线到在线微调的表现。** Figure 5显示MAC-Flow在离线到在线微调中能够持续提升性能，表明其策略表示具有良好的迁移基础。但在强交互场景下，因子化策略的结构性偏差可能在在线阶段难以完全弥补。

## 定位与知识库关联

### 1. 核心瓶颈与因果机制

离线多智能体强化学习（Offline MARL）面临一个根本性权衡：表达力与推理效率之间的矛盾。扩散模型（如 **DoF** (Zhu et al., 2024) 和 **MADiff** (Li et al., 2025a)）能够捕获联合动作分布的多模态性与复杂的智能体间协调模式，但推理过程需要多步去噪（每步复杂度 $O(K)$ 或 $O(IK)$），导致部署延迟居高不下。高斯策略（如 **MATD3+BC** (Fujimoto & Gu, 2021)、**MACQL** (Kumar et al., 2020)）推理仅需单次前传（$O(1)$），但受限于单模假设，无法表达离线数据中混合行为策略产生的多峰分布。现有方法在表达力与实时性之间始终无法兼得。

MAC-Flow 的因果调控旋钮是**将表达力学习与价值优化解耦**。第一阶段通过流匹配（flow matching）的行为克隆（BC）纯粹学习联合动作分布，不涉及价值函数梯度；第二阶段在 IGM（Individual-Global-Max）约束下，同时最大化全局 Q 值和最小化 BC 蒸馏损失，将联合流策略分解为每个智能体的单步采样策略。这一解耦设计使推理复杂度降至 $O(1)$，同时借助 Wasserstein 距离上界与 Q 函数的 Lipschitz 性质，为蒸馏过程的性能退化提供了理论保证。

### 2. 方法谱系定位

#### 2.1 与扩散策略方法的对比

扩散策略是 MAC-Flow 最直接的对标基线。**Diffusion BC** (Chi et al., 2023) 将扩散模型引入单智能体行为克隆，但在多智能体场景中未考虑联合建模。**DoF** (Zhu et al., 2024) 和 **MADiff** (Li et al., 2025a) 将扩散策略扩展到多智能体离线 RL，通过集中式扩散直接建模联合动作分布。然而，两者在推理时均需多步去噪：DoF 的推理复杂度为 $O(K)$（$K$ 为去噪步数），MADiff 若对每智能体独立扩散则升至 $O(IK)$。MAC-Flow 的核心改进在于：用流匹配替代扩散过程作为表达力载体，并通过蒸馏将多步采样压缩为单步，实现约 14.5 倍的推理加速（Figure 1），同时保持可比或更优的性能（SMACv1 平均回报 15.6 与 DoF 持平，SMACv2 平均回报 14.2 超越 DoF 的 13.2）。

#### 2.2 与高斯策略方法的对比

高斯策略族包括 **BC**（纯行为克隆）、**MABCQ** (Yang et al., 2021)、**MACQL** (Kumar et al., 2020)、**MATD3+BC** (Fujimoto & Gu, 2021) 和 **ICQ** (Wang et al., 2023)。这些方法推理速度极快（$O(1)$），但在多模态联合分布面前表现力不足——它们只能学习单峰高斯分布，无法捕获离线数据中多个行为策略混合产生的复杂协调模式。MAC-Flow 的蒸馏策略在推理复杂度上与高斯策略相当（$O(1)$），但通过第一阶段流匹配 BC 保留了联合分布的多模态表达能力，从而在性能上显著超越高斯基线。

#### 2.3 与值分解方法的对比

**OMAR** (Barde et al., 2024) 和 **OMIGA** (Liu et al., 2025) 是近期结合值分解与生成建模的代表性工作。OMAR 利用自编码器学习动作表示，OMIGA 则引入互信息正则化。MAC-Flow 与这些方法共享 IGM 原理作为集中训练分散执行的理论基础，但关键差异在于：MAC-Flow 将 IGM 应用于 Critic 训练，而非直接约束策略表达。策略的表达力由流匹配 BC 独立保证，IGM 仅在价值优化阶段确保个体最优与全局最优的一致性。消融实验（Figure 8）证实，IGM-based 个体 Critic 始终优于集中式 Critic，验证了这一设计选择的有效性。

#### 2.4 与流匹配方法的对比

MAC-Flow 并非简单地将流匹配引入多智能体 RL。一个朴素的扩展方案是 **MA-FQL**——将单智能体 Flow Q-Learning 直接分散化，每智能体独立训练流策略和独立 Q 函数。Figure 10 的对比实验表明，MAC-Flow 显著优于 MA-FQL，验证了联合 BC 和 IGM-based Critic 的必要性：仅靠分散化流策略无法有效捕获智能体间的协调依赖。

### 3. 适用边界与局限

#### 3.1 理论假设的边界

MAC-Flow 的性能保证建立在两个核心假设之上：

1. **IGM 可分解性**：全局 Q 函数的 argmax 必须等于个体 Q 函数 argmax 的元组。在强交互、反协同场景（如 XOR 任务，Figure 15）中，联合最优动作无法分解为独立个体动作的笛卡尔积，IGM 原理失效，导致蒸馏策略退化为近似均匀的乘积分布。
2. **Q 函数的 Lipschitz 连续性**：Proposition 4.3 将策略蒸馏的性能差距上界为 $L_Q \cdot W_2(\pi_{\mathbf{w}}, \pi_{\phi})$。若 Q 函数在联合动作空间中剧烈震荡（Lipschitz 常数 $L_Q$ 过大），即使 Wasserstein 距离很小，性能退化仍可能显著。教学实验（Figure 3(c)）验证了该界限的紧密性，但在高维复杂任务中 Lipschitz 常数的实际量级仍需谨慎评估。

#### 3.2 交互强度与因子化质量

Figure 16 的收益博弈实验揭示了交互强度对蒸馏效果的影响：当智能体间交互依赖较弱时，因子化策略能较好地逼近联合策略；随着交互强度增加，Wasserstein 距离上升，性能差距扩大。这表明 MAC-Flow 在松耦合协调任务中更为可靠，而在紧耦合场景下需要额外的协调机制补偿。

#### 3.3 规模与异构性限制

实验验证主要集中于中等规模智能体（SMAC 最多 8 个智能体，MA-MuJoCo 最多 4 个智能体，MPE 最多 3 个智能体）。联合流模型的输入维度随智能体数量线性增长，在大规模系统（如 40+ 智能体）中可能面临维度灾难。此外，所有智能体共享同构的动作空间和策略架构，对异构智能体场景的泛化能力未经检验。

#### 3.4 训练开销与超参数敏感性

虽然推理速度大幅提升，但第一阶段的流匹配 BC 训练仍比纯高斯策略增加了计算开销（Figure 11）。蒸馏损失权重 $\alpha$ 需要在不同任务上仔细调节，对最终性能影响敏感——$\alpha$ 过小导致 BC 约束松弛、策略偏离联合分布；$\alpha$ 过大则抑制价值优化、退化为纯行为克隆。

### 4. 开放问题

1. **超越 IGM 的因子化机制**：能否引入通信通道或更高阶的联合建模（如条件流匹配），在不破坏分散执行的前提下处理不可分解的协调结构？XOR 任务（Figure 15）的失败案例表明，当前框架在反协同模式面前存在根本性局限。

2. **部分可观测与通信受限场景**：MAC-Flow 假设全局观测可用于训练，但执行时仅依赖局部观测。在严格的部分可观测 Dec-POMDP 环境中，联合流模型的训练条件本身就不完整，蒸馏质量可能进一步恶化。

3. **持续学习与迁移**：Figure 5 展示了离线到在线微调的有效性，但 MAC-Flow 在任务分布漂移、持续学习或跨场景迁移中的表现尚待探索。流匹配 BC 提供的联合分布先验能否加速新任务的适应？

4. **生成模型的选择空间**：本文采用流匹配的最简单变体（条件速度场匹配位移向量），未探索更先进的生成建模技术（如扩散模型与流匹配的混合、基于分数的生成模型）能否在表达力上带来进一步提升，同时保持蒸馏的可行性。

5. **大规模系统的维度灾难**：联合流模型的输入维度为 $I \cdot d_a$（$I$ 为智能体数，$d_a$ 为动作维度）。在大规模系统中，能否通过图神经网络、注意力机制或分层建模来缓解维度爆炸，同时保持联合分布的建模精度？

## 原文 PDF

![[paperPDFs/ICLR_2026/Multi_agent_Coordination_via_Flow_Matching.pdf]]
