---
title: "Deep SPI: Safe Policy Improvement via World Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Deep_SPI_Safe_Policy_Improvement_via_World_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 24C3bSaH3F
aliases:
- DSSPIWM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过重要性比率（IR）定义的邻域算子约束策略更新幅度，并联合最小化局部奖励与转移预测损失。"
primary_logic: "当新旧策略的重要性比率有界时，局部模型损失可直接控制值函数近似误差，从而使世界模型内的策略改进能以高概率转移到真实环境，同时表征学习能保持值函数的Lipschitz连续性。"
claims:
- "邻域算子能够保证策略单调改进并收敛（Thm.1）。"
- "当SIR<1/γ时，真实环境与世界模型在任意邻域内策略上的回报差可通过局部损失和SIR上界进行控制（Thm.2）。"
- "结合邻域约束和局部损失，DeepSPI提供了安全策略改进的保证：真实改进不低于世界模型内的改进减去由局部损失决定的误差项ζ（Thm.3）。"
- "局部损失的优化使得表征在多数状态下保证值函数几乎Lipschitz，即相似值状态在隐空间中被分开（Thm.4）。"
---

# Deep SPI: Safe Policy Improvement via World Models

> [!tip] 核心洞察
> 当新旧策略的重要性比率有界时，局部模型损失可直接控制值函数近似误差，从而使世界模型内的策略改进能以高概率转移到真实环境，同时表征学习能保持值函数的Lipschitz连续性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DeepSPI: 基于世界模型的安全策略改进 |
| 英文题名 | Deep SPI: Safe Policy Improvement via World Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=24C3bSaH3F) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DeepSPI |
| Dataset | ALE-57 (stochastic), Illustrative Grid World |

> [!tip] 效果简介
> - ALE-57 (stochastic) 上，Human Normalized Score (IQM aggregate) 为 DeepSPI，对比 PPO / DeepMDP (PPO)，变化 显著提升，见图5。
> - Illustrative Grid World 上，Return from initial state 为 ≈8.01 (DeepSPI)，对比 ≈4.8 (PPO)，变化 +3.2。

## 概要

深度强化学习中利用世界模型进行策略优化面临两个核心瓶颈：**分布外（Out-of-Trajectory, OOT）预测错误**和**混淆策略更新（Confounding Policy Update）**。前者指当策略在世界模型中偏离行为策略过远时，模型预测变得不可靠；后者指表征与策略同步更新时，仅依赖行为策略经验可能导致性能退化而非提升。这两个问题共同导致世界模型内的策略改进无法安全地转移到真实环境。

本文提出 **DeepSPI**，通过三个关键机制解决上述问题：

1. **邻域算子约束**：基于重要性比率（Importance Ratio, IR）定义策略邻域 $\mathcal{N}^{C}(\pi)$，将策略更新幅度限制在 $[2-C, C]$ 范围内，从理论上保证策略单调改进并收敛至最优值函数（定理1）。

2. **局部损失驱动的安全改进保证**：通过联合最小化局部奖励损失 $L_R$ 和转移损失 $L_P$，建立了真实环境与世界模型之间回报差的上界——该上界由局部损失和重要性比率上界共同控制（定理2）。在此基础上，DeepSPI 提供了安全策略改进保证：真实改进不低于世界模型内的改进减去一个由局部损失决定的误差项 $\zeta$（定理3）。

3. **表征的 Lipschitz 连续性**：局部损失的优化使得值函数在多数状态下近似于表征距离的 Lipschitz 函数，即相似值状态在隐空间中被有效分离，从而确保表征对策略更新的适应性（定理4）。

在 ALE-57 随机版本基准上，DeepSPI 在人类标准化得分的 IQM 聚合指标上显著优于 **PPO**（Schulman et al., 2017）和 **DeepMDP**（Gelada et al., 2019），同时具有统计显著更低的转移预测损失（均值差 -0.1381，$p=6.6\times10^{-4}$）。在示例迷宫环境中，DeepSPI 的回报（≈8.01）相比 PPO（≈4.8）提升约 67%。

**方法定位**：DeepSPI 属于基于世界模型的策略优化方法，其核心创新在于将策略改进的安全性保证形式化地嵌入到优化过程中——通过重要性比率约束策略更新幅度，并将辅助预测损失直接纳入策略优化目标（效用函数 $U = A - \alpha_R \ell_R - \alpha_P \ell_P$），而非仅作为额外的表征学习目标。这一设计使得世界模型内的策略改进能够以高概率转移到真实环境。

**主要局限**：理论分析依赖回合制设定和重置状态对齐假设；安全改进的紧致性取决于行为策略平稳分布的覆盖性；实验验证主要限于 Atari 离散控制环境，尚未在连续控制或部分可观测环境中检验。



### 世界模型在深度强化学习中的角色与困境

基于模型的深度强化学习（MBRL）通过构建世界模型来模拟环境动态，从而降低与真实环境交互的样本成本。一个典型的世界模型由编码器 $\phi$、转移预测器 $\bar{P}$ 和奖励预测器 $\bar{R}$ 组成，其核心目标是最小化经验回放缓冲区上的预测损失：

$$L_R = \mathbb{E}_{\eta \sim B} f_R(\phi, \bar{R}; \eta), \quad L_P = \mathbb{E}_{\eta \sim B} f_P(\phi, \bar{P}; \eta)$$

然而，这种标准范式存在一个根本性瓶颈：**世界模型在分布外（Out-of-Training, OOT）区域的预测错误会通过策略优化环路被放大，导致策略改进不再安全**。具体而言，当策略更新后访问到模型训练时未充分覆盖的状态-动作区域时，模型的转移和奖励预测可能严重偏离真实环境，使得基于模型估计的优势函数误导策略更新方向。

### 两个关键失败模式

DeepSPI 识别并形式化了两种导致世界模型内策略改进失败的核心机制：

**1. 分布外预测错误（OOT Prediction Error）**

如 Figure 1 所示，考虑一个状态空间被划分为四个区域的大规模 MDP。编码器 $\phi$ 将区域 $S_1, S_2, S_4$ 映射到不同的隐状态，但对于 $S_3$ 中的状态，编码器可能将其映射到 $\bar{s}_3$ 或 $\bar{s}_3'$。当世界模型在 $S_1$ 区域训练后，智能体在模型内规划时可能选择一条看似最优的路径，但该路径在实际环境中会经过模型未见过的 $S_3$ 区域，导致预测崩溃。这种 OOT 错误源于世界模型的泛化能力有限，而策略优化天然倾向于探索模型置信度低的区域。

**2. 混淆策略更新（Confounding Policy Update）**

如 Figure 2 和 Figure 3 的迷宫环境所示，当策略和表征同步更新时，表征的漂移会改变隐空间中状态间的距离关系，导致价值函数估计发生非平稳变化。这种耦合效应使得策略改进方向不再可靠：即使世界模型对当前表征是准确的，表征本身的更新也可能“混淆”策略优化过程，使策略收敛到次优解。Figure 4 的实验结果直观展示了这一现象——PPO 在迷宫中仅获得约 4.8 的回报，而 DeepSPI 达到了约 8.01，且 DeepSPI 学到的表征能将不同分支的状态在隐空间中有效分离。

### 现有方法的缺口

当前主流的深度 MBRL 方法存在以下结构性不足：

- **PPO**（Schulman et al., 2017）作为无模型基线，通过裁剪重要性比率来约束策略更新幅度，但完全缺乏对世界模型预测质量的显式考虑，无法利用模型进行安全改进。
- **DeepMDP**（Gelada et al., 2019）引入了辅助的奖励和转移预测损失来训练表征，但其策略优化目标仍使用纯优势函数 $A$，未将模型损失纳入策略改进的决策依据。更重要的是，DeepMDP 缺乏对策略更新幅度的显式约束，无法保证模型内的改进能可靠地迁移到真实环境。

这些方法的共同缺陷在于：**缺乏一个统一的理论框架，能够同时约束策略更新幅度、量化世界模型局部质量，并保证表征学习对策略优化的适应性**。具体而言，缺少以下三个层面的机制：

1. **策略更新约束**：无显式的重要性比率（IR）约束来定义安全的策略邻域。
2. **联合优化目标**：未将局部模型损失纳入策略优化的效用函数。
3. **表征平滑性保证**：未确保值函数在隐空间中近似满足 Lipschitz 连续性。

### 本文的核心动机

DeepSPI 的动机正是填补上述缺口：通过引入基于重要性比率的邻域算子约束策略更新幅度，联合最小化局部奖励与转移预测损失来构造策略优化的效用函数，并利用 Lipschitz 网络保证表征的平滑性，从而在理论上提供**安全策略改进的保证**——即真实环境中的策略改进不低于世界模型内的改进减去一个由局部损失控制的可量化误差项。



## 核心方法与创新机理

DeepSPI 的核心创新在于将**策略改进的安全性保证**从纯理论框架推向了可扩展的深度强化学习实践，其关键抓手是三个相互耦合的“changed slots”：

1. **基于重要性比率的邻域约束替代启发式裁剪**
2. **将世界模型局部损失注入策略优化目标**
3. **通过表征学习强制值函数的近似 Lipschitz 连续性**

这三者并非孤立改进，而是围绕一个中心瓶颈——世界模型的分布外预测错误与表征-策略同步更新引发的混淆——形成了因果闭环。

---

### 1. 策略更新约束：从 PPO 裁剪到 IR 邻域算子

PPO 通过裁剪重要性比率来限制策略更新幅度，但这是一种启发式约束，缺乏对世界模型内策略改进安全性的理论保证。DeepSPI 将其替换为基于重要性比率（IR）严格定义的**邻域算子** $\mathcal{N}^C$：

$$\mathcal{N}^{C}(\pi) = \left\{ \pi' \in \Pi \mid 2-C \leq D_{\mathrm{IR}}^{\mathrm{inf}}(\pi, \pi') \leq D_{\mathrm{IR}}^{\mathrm{sup}}(\pi, \pi') \leq C,\ \mathrm{supp}\ \text{equal} \right\}$$

该算子将策略更新限制在一个信任域内，确保新旧策略的重要性比率被严格控制在 $[2-C, C]$ 区间。这一约束是后续所有理论保证的基石：**Thm. 1** 证明，在此邻域内进行策略更新可以保证值函数单调改进并收敛到最优值函数 $V^*$——该证明的关键在于将更新方案归约为 mirror learning 框架（Kuba et al., 2022）的一个实例。

实践中，DeepSPI 将 IR 上界限制为 $1/\gamma - 1$，以满足理论要求的 $C < 1/\gamma$ 条件（见附录 H.2、H.4）。这与 PPO 的裁剪形成鲜明对比：PPO 的裁剪阈值是经验性的超参数，而 DeepSPI 的邻域半径由折扣因子 $\gamma$ 直接决定，具有理论可解释性。

---

### 2. 策略优化目标：从优势函数到效用函数

标准策略优化（包括 PPO）以优势函数 $A^{\pi}$ 为目标。DeepSPI 将其替换为**效用函数** $U^{\pi_n}$：

$$U^{\pi_n}(s, a, s') := A^{\pi_n}(s, a) - \alpha_R \cdot \ell_R(s, a) - \alpha_P \cdot \ell_P(s, a, s')$$

其中 $\ell_R$ 和 $\ell_P$ 分别是转移级别的奖励预测损失和转移预测损失。这一替换的深层动机来自 **Thm. 2** 和 **Thm. 3** 的理论洞察：

- **Thm. 2** 表明，当 SIR $< 1/\gamma$ 时，真实环境与世界模型在邻域内任意策略上的回报差可由局部损失 $L_R^{\xi_{\pi_b}}$、$L_P^{\xi_{\pi_b}}$ 和 SIR 上界联合控制：

$$|\rho(\bar{\pi}\circ\phi, \mathcal{M}) - \rho(\bar{\pi}, \overline{\mathcal{M}})| \leq \mathrm{AEL}(\pi_b) \cdot \frac{L_R^{\xi_{\pi_b}}/\gamma + K_V \cdot L_P^{\xi_{\pi_b}}}{1/D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi}) - \gamma}$$

- **Thm. 3** 进一步给出安全策略改进保证：真实环境中的改进不低于世界模型内的改进减去由局部损失决定的误差项 $\zeta$。

这意味着，**最小化局部损失直接缩小了世界模型与真实环境的回报差距**。将局部损失纳入策略优化目标（即效用函数 $U$），使得策略更新不仅追求高回报，同时主动规避世界模型预测不可靠的区域——这正是“安全”策略改进的核心机制。相比之下，DeepMDP（Gelada et al., 2019）虽然也使用了辅助预测损失，但这些损失仅用于表征学习，并未参与策略优化目标的构造。

---

### 3. 表征训练：联合最小化局部损失以强制 Lipschitz 连续性

DeepSPI 的表征训练同时最小化局部奖励损失 $L_R$ 和转移损失 $L_P$，这与 DeepMDP 的辅助损失表面相似，但目标有本质差异。DeepSPI 的理论分析揭示：联合优化这两个损失可以保证值函数在多数状态下近似于表征距离的 Lipschitz 函数——**Thm. 4**：

$$|V^{\pi}(s_1) - V^{\pi}(s_2)| \leq K_V \cdot \bar{d}(\phi(s_1), \phi(s_2)) + \varepsilon$$

这一性质的意义在于：当策略在邻域内更新时，表征空间中的小幅移动不会导致值函数估计的剧烈跳变，从而避免了“混淆策略更新”问题——即表征与策略同步更新时，值相近的状态在隐空间中被错误合并，导致策略优化方向失真。在玩具迷宫实验中（Figure 4），PPO 的表征将上下分支的 ⋆ 单元坍塌到同一隐表示，仅获得约 4.8 的回报；而 DeepSPI 通过联合损失保持表征分离，回报提升至约 8.0。

此外，DeepSPI 采用 **Lipschitz 网络**（而非梯度惩罚）来显式保证隐空间的平滑性，实验表明这比梯度惩罚更高效（附录 H.4）。这一设计选择直接服务于 Thm. 4 的理论要求。

---

### 创新闭环：三个 changed slots 的耦合关系

上述三个改进并非独立叠加，而是形成了一个理论-算法闭环：

1. **邻域算子**限制了策略更新幅度，使得 SIR 有界，这是 Thm. 2 和 Thm. 3 成立的前提；
2. **效用函数**将局部损失引入优化目标，使得策略更新主动规避模型不可靠区域，从而收紧 Thm. 3 中的误差项 $\zeta$；
3. **联合局部损失优化**强制表征的 Lipschitz 连续性，为 Thm. 2 中的 $K_V$ 提供可控上界，同时防止混淆策略更新破坏邻域约束的有效性。

三者共同实现了论文的核心承诺：**在世界模型内进行策略改进，其性能提升能以高概率转移到真实环境中**。这一闭环在 ALE-57 基准上得到了实证验证——DeepSPI 在人类标准化得分的 IQM 聚合指标上显著优于 PPO 和 DeepMDP（PPO），同时具有统计显著的更低转移预测损失（均值差 -0.1381，95% CI [-0.2226, -0.05907]，Wilcoxon 检验 $p = 6.6 \times 10^{-4}$，见 Figure 12 及附录 H.3）。



DeepSPI 构建了一个**编码器-世界模型-策略学习**的端到端安全改进管线，核心目标是在世界模型内进行策略优化时，保证优化结果能高概率地迁移回真实环境。该框架由五个关键模块串联而成，其输入输出流与依赖关系如下：

### 管线模块与数据流

1. **Encoder φ**：接收原始高维状态 $s \in \mathcal{S}$，输出隐状态 $\bar{s} = \phi(s)$。该模块是真实环境与世界模型之间的桥梁，其表征质量由后续的局部损失和 Lipschitz 约束共同保证。

2. **World Model $(\bar{P}, \bar{R})$**：在隐空间中预测状态转移和奖励——$\bar{P}(\cdot \mid \bar{s}, a)$ 给出下一隐状态的分布，$\bar{R}(\bar{s}, a)$ 给出即时奖励。世界模型的训练信号来自真实环境交互轨迹，通过最小化局部奖励损失 $L_R$ 和局部转移损失 $L_P$（式 4）实现。

3. **Actor-Critic Networks**：在隐空间 $\bar{\mathcal{S}}$ 中学习策略 $\bar{\pi}$ 和价值函数 $V^{\bar{\pi}}$。Actor 输出动作分布，Critic 估计隐状态的值函数，二者共同为策略改进提供优势估计 $A^{\bar{\pi}}$。

4. **Utility Computation**：将标准优势函数 $A^{\pi_n}(s, a)$ 替换为效用函数 $U^{\pi_n}(s, a, s')$（式 6），显式地将辅助预测损失纳入策略优化目标：
   $$U^{\pi_n}(s, a, s') := A^{\pi_n}(s, a) - \alpha_R \cdot \ell_R(s, a) - \alpha_P \cdot \ell_P(s, a, s')$$
   其中 $\ell_R$ 和 $\ell_P$ 分别为逐样本的奖励预测误差和转移预测误差。这一步是**将世界模型质量反馈与策略改进绑定**的关键机制。

5. **Policy Update with PPO**：在效用 $U$ 下执行 PPO 风格的策略更新，同时通过邻域算子 $\mathcal{N}^C$（式 2）将重要性比率约束在 $[2-C, C]$ 范围内：
   $$\mathcal{N}^{C}(\pi) = \left\{ \pi' \in \Pi \mid 2-C \leq D_{\mathrm{IR}}^{\mathrm{inf}}(\pi, \pi') \leq D_{\mathrm{IR}}^{\mathrm{sup}}(\pi, \pi') \leq C \right\}$$
   这一约束确保策略更新幅度受控，防止策略漂移到世界模型不可靠的分布外区域。

### 模块关系与理论保证

模块间的协同设计由三条理论保证串联：

- **Thm.1**：邻域算子 $\mathcal{N}^C$ 保证策略在真实 MDP 中单调改进并收敛至最优值函数 $V^*$（该结果为 mirror learning 框架的特例）。
- **Thm.2**：当重要性比率上界 $D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi}) < 1/\gamma$ 时，真实环境与世界模型之间的回报差由局部损失 $L_R^{\xi_{\pi_b}}$、$L_P^{\xi_{\pi_b}}$ 和该上界联合控制。这意味着**只要世界模型在行为策略分布上足够准确，邻域内的任意策略在模型中的表现就能可靠地泛化到真实环境**。
- **Thm.4**：通过联合最小化局部损失，表征 $\phi$ 使得值函数 $V^{\bar{\pi}}$ 在多数状态下近似于隐空间距离的 Lipschitz 函数——即相似值状态在隐空间中被适当分离，从而避免因表征坍缩导致的混淆策略更新。

### 实际实现中的关键设计

在 Atari 规模的实践中（Algorithm 1），DeepSPI 采用**同步更新**策略：编码器、世界模型、Actor-Critic 在每轮 rollout 后同时更新。世界模型的转移密度使用 5 个正态分布的混合建模，奖励预测为确定性输出。为满足理论所需的 Lipschitz 连续性，网络使用 **Lipschitz 网络结构**（而非梯度惩罚）来约束隐空间平滑性——实验表明这种方式比梯度惩罚更高效。重要性比率在实际中被限制为 $1/\gamma - 1$，以满足理论要求的 $C < 1/\gamma$ 条件。

整个管线的核心因果机制可概括为：**邻域约束限制策略更新幅度 → 局部损失控制世界模型误差 → 联合优化使表征保持 Lipschitz 连续性 → 模型内的策略改进以可控误差迁移至真实环境**。



DeepSPI 的算法核心由四个关键模块构成，它们协同工作以实现安全策略改进：**策略邻域约束**、**局部模型损失**、**效用函数**以及**Lipschitz表征学习**。以下逐一展开其公式定义与推导逻辑。

### 策略邻域算子

DeepSPI 通过基于重要性比率（Importance Ratio, IR）的邻域算子来约束策略更新幅度。对于任意策略 $\pi$，其邻域定义为：

$$
\mathcal{N}^{C}(\pi) = \left\{ \pi' \in \Pi \mid 2-C \leq D_{\mathrm{IR}}^{\mathrm{inf}}(\pi, \pi') \leq D_{\mathrm{IR}}^{\mathrm{sup}}(\pi, \pi') \leq C,\ \mathrm{supp}\ \text{equal} \right\}
$$

其中 $D_{\mathrm{IR}}^{\mathrm{inf}}$ 和 $D_{\mathrm{IR}}^{\mathrm{sup}}$ 分别表示重要性比率的下确界和上确界，常数 $C \in (1, 2)$ 控制邻域半径。该约束确保新旧策略在各状态上的概率比值被限制在 $[2-C, C]$ 范围内，同时保持支撑集一致。

**理论保证**：在此邻域内执行贪心策略改进——即 $\pi_{n+1} := \operatorname*{argsup}_{\pi' \in \mathcal{N}^{C}(\pi_n)} \mathbb{E}_{a \sim \mu_{\pi_n}} \mathbb{E}_{a \sim \pi'(\cdot|s)} A^{\pi_n}(s, a)$——可证明值函数 $V^{\pi_n}$ 单调改进并收敛至最优值函数 $V^*$（Thm. 1）。该证明的核心在于将此更新方案归约为镜面学习（mirror learning, Kuba et al., 2022）的一个实例。

### 局部模型损失

世界模型的质量通过两个局部损失函数度量，均在行为策略 $\pi_b$ 的状态-动作分布 $\xi_{\pi_b}$ 下定义：

**局部奖励损失** $L_R^B$ 和**局部转移损失** $L_P^B$：

$$
L_R^B := \mathbb{E}_{s,a \sim B} \left| R(s,a) - \bar{R}(\bar{s},a) \right|, \quad L_P^B := \mathbb{E}_{s,a \sim B} \mathcal{W}\left(\phi_\sharp P(\cdot|s,a), \bar{P}(\cdot|\phi(s),a)\right)
$$

其中 $\bar{s} = \phi(s)$ 为编码器 $\phi$ 将原始状态映射到的隐状态，$\mathcal{W}$ 为 Wasserstein 距离，$\phi_\sharp P$ 表示真实转移分布经 $\phi$ 推送至隐空间的分布。

**关键假设**：世界模型的隐奖励函数 $\bar{R}$ 和隐转移函数 $\bar{P}$ 在策略 $\bar{\pi}$ 下满足 Lipschitz 连续性，即存在常数 $K_{\bar{R}}^{\bar{\pi}}$ 和 $K_{\bar{P}}^{\bar{\pi}}$ 使得隐空间中相近状态对应的奖励期望和转移分布差异有界。这一假设是后续理论分析的基础。

### 效用函数

为将局部损失纳入策略优化目标，DeepSPI 将传统的优势函数 $A^{\pi_n}$ 替换为**效用函数** $U^{\pi_n}$：

$$
U^{\pi_n}(s,a,s') := A^{\pi_n}(s,a) - \alpha_R \cdot \ell_R(s,a) - \alpha_P \cdot \ell_P(s,a,s')
$$

其中 $\ell_R(s,a) := |R(s,a) - \bar{R}(\phi(s),a)|$ 为逐样本奖励损失，$\ell_P(s,a,s')$ 为对应的逐样本转移损失项。超参数 $\alpha_R, \alpha_P > 0$ 控制辅助损失与优势函数的相对权重。

**设计逻辑**：在 PPO 更新框架中，所有出现 $A^{\pi_n}$ 的位置均替换为 $U^{\pi_n}$。这使得策略在追求高回报的同时，倾向于选择世界模型预测准确的区域，从而避免分布外（OOT）预测错误导致的策略退化。

### 安全改进与表征学习保证

上述模块的组合产生了三个核心理论结果：

**回报差上界（Thm. 2）**：当重要性比率上界 $D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi}) < 1/\gamma$ 时，真实环境与世界模型在隐策略 $\bar{\pi}$ 下的回报差可被局部损失和 SIR 联合控制：

$$
|\rho(\bar{\pi}\circ\phi, \mathcal{M}) - \rho(\bar{\pi}, \overline{\mathcal{M}})| \leq \mathrm{AEL}(\pi_b) \cdot \frac{L_R^{\xi_{\pi_b}}/\gamma + K_V \cdot L_P^{\xi_{\pi_b}}}{1/D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b,\bar{\pi}) - \gamma}
$$

其中 $K_V$ 为值函数的 Lipschitz 常数，$\mathrm{AEL}(\pi_b)$ 为行为策略的平均事件长度。

**安全策略改进（Thm. 3）**：在邻域约束下，真实环境中的改进不低于世界模型内的改进减去误差项 $\zeta$：

$$
\rho(\bar{\pi}\circ\phi, \mathcal{M}) - \rho(\pi_b, \mathcal{M}) \geq \rho(\bar{\pi}, \overline{\mathcal{M}}) - \rho(\bar{\pi}_b, \overline{\mathcal{M}}) - \zeta
$$

其中 $\zeta := \mathrm{AEL}(\pi_b) \cdot (L_R^{\xi_{\pi_b}}/\gamma + K_V L_P^{\xi_{\pi_b}}) \left(\frac{1}{1/D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi}) - \gamma} + \frac{1}{1-\gamma}\right)$。

**表征 Lipschitz 连续性（Thm. 4）**：通过联合最小化局部损失，编码器 $\phi$ 学得的表征使得值函数在多数状态下近似 Lipschitz：

$$
|V^{\bar{\pi}}(s_1) - V^{\bar{\pi}}(s_2)| \leq K_V \cdot \bar{d}(\phi(s_1), \phi(s_2)) + \varepsilon
$$

这意味着具有相似值的状态在隐空间中被保持接近，从而确保表征对策略更新的适应性，缓解混淆策略更新问题。

### 模块协同机制

在实际实现中（Algorithm 1），DeepSPI 同时更新编码器 $\phi$、世界模型 $(\bar{P}, \bar{R})$ 和 Actor-Critic 网络。策略更新使用 PPO 框架，但以效用 $U^{\pi_n}$ 替代优势函数，并通过限制重要性比率在 $[2-C, C]$ 内隐式施加邻域约束。世界模型和编码器则通过最小化局部损失 $L_R$ 和 $L_P$ 进行训练，同时使用 Lipschitz 网络结构（而非梯度惩罚）来高效保证隐空间的平滑性。



## 实验与关键发现

### 主实验：ALE-57 基准

DeepSPI 在 Atari-57 的随机版本上进行了全面评估，与 **PPO**（Schulman et al., 2017）和 **DeepMDP (PPO)**（Gelada et al., 2019）两个基线进行对比。图 5 展示了人类标准化得分（Human Normalized Score）的聚合结果，采用 IQM（四分位均值）、中位数、均值和最优性差距四个指标，并附有 95% 置信区间。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_24C3bSaH3F/figures/004_Figure_5.jpg]]
*Figure 5: Aggregate results on stochastic versions of the standard 57 environments from ALE, with 95% confidence intervals (CIs). Higher values for the mean, median, and interquartile mean (IQM) indicate better performance, while a lower optimality gap is preferable (cf. Agarwal et al. 2021b). CIs are obtained through percentile bootstrapping with stratified resampling. Plots per environment available in Appendix H.3*

核心发现是 DeepSPI 在所有聚合指标上均优于两个基线。具体而言，DeepSPI 的 IQM 约为 0.66，而 PPO 和 DeepMDP 约为 0.61；最优性差距方面，DeepSPI 约为 0.47，低于基线的约 0.51。这表明将邻域约束和局部损失纳入策略优化目标后，不仅未损害性能，反而带来了整体提升。论文摘要明确指出“DeepSPI matches or exceeds strong baselines, including PPO and DeepMDPs”，该结论在聚合统计中得到验证。

图 6 进一步展示了样本效率曲线。在 IQM 归一化得分随环境步数变化的趋势中，DeepSPI 始终位于基线上方，且置信区间不重叠，表明其在有限交互预算下具有更优的样本效率。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_24C3bSaH3F/figures/007_Figure_6.jpg]]
*Figure 6: Sample efficiency w.r.t. IQM normalized scores on the stochastic ALE-57. Shaded regions give pointwise 95% CIs obtained via percentile stratified bootstrap*

### 消融实验：转移预测损失

DeepSPI 的核心主张之一是通过联合优化局部损失来提升世界模型质量，从而支撑安全策略改进。这一主张在转移预测损失 $L_P$ 的对比中得到了强力验证。

图 7 展示了训练过程中所有 Atari 游戏的中位转移损失和奖励损失。DeepSPI 的转移损失始终低于 DeepMDP，且差距随训练进程持续扩大。统计检验（附录 H.3）给出了精确的量化证据：DeepSPI 的转移损失均值比 DeepMDP 低 -0.1381，95% 置信区间为 [-0.2226, -0.05907]，Wilcoxon 检验的 p 值为 $6.6 \times 10^{-4}$。这一高度显著的差异证实，邻域约束与效用函数 $U^{\pi_n}$ 的联合设计能够有效降低世界模型的预测误差，而非仅仅将辅助损失作为正则化项附加在标准目标上。

### 表征质量：Lipschitz 连续性的实现

定理 4 要求表征 $\phi$ 使得值函数在隐空间中近似 Lipschitz 连续，即 $|V^{\pi}(s_1) - V^{\pi}(s_2)| \leq K_V \cdot \bar{d}(\phi(s_1), \phi(s_2)) + \varepsilon$。实验表明，使用专门的 Lipschitz 网络来保证这一性质比梯度惩罚更为高效（附录 H.4）。这一设计选择直接关系到理论保证的兑现——若表征不满足平滑性，定理 2 中通过 $K_V \cdot L_P^{\xi_{\pi_b}}$ 项控制回报差上界的机制将失效。

### 示例环境验证：迷宫中的混淆策略更新

图 3 所示的玩具迷宫环境用于直观验证 DeepSPI 是否解决了混淆策略更新问题。在该迷宫中，PPO 的编码器将来自不同分支但视觉相似的“⋆”状态映射到隐空间的相近位置，导致策略无法区分高回报路径与低回报路径，最终从起始格 I 获得的回报仅为约 4.8。相比之下，DeepSPI 的表征成功将上下分支的“⋆”状态在隐空间中分离开来，使得策略能够可靠地选择高回报路径，回报达到约 8.01（图 4）。这一差距（+3.2）直接体现了联合优化局部损失对表征学习的改善效果。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_24C3bSaH3F/figures/006_Figure_4.jpg]]
*Figure 4: Value from cell I in the maze (left) and distance between the representation of the ⋆ cell from the top and bottom branches (right)*

### 超参数配置

DeepSPI 的关键超参数如表 1 所示。学习率为 $2.5 \times 10^{-4}$，使用 128 个并行环境，每次 rollout 8 步，GAE 参数 $\lambda = 0.95$，PPO 裁剪参数 $\epsilon = 0.1$。辅助损失的系数设置为：转移损失系数 $5 \times 10^{-4}$，奖励损失系数 0.01。转移密度模型采用 5 个正态分布的混合。重要性比率约束方面，根据理论要求 $C < 1/\gamma$，实际实现中将比率限制为 $1/\gamma - 1$（附录 H.2 和 H.4），确保邻域算子 $\mathcal{N}^C$ 的约束满足定理 2 和定理 3 的前提条件。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_24C3bSaH3F/figures/014_Table_1.jpg]]
*Table 1: Summary of DeepSPI hyperparameters*

### 失败模式与局限

尽管理论和实验均支持 DeepSPI 的有效性，但以下局限性需要在应用时注意：

1. **分布漂移的紧致性衰减**：定理 3 的安全改进下界依赖于行为策略平稳分布对邻域的覆盖。当实际训练中分布漂移较大时，误差项 $\zeta$ 可能膨胀，导致理论保证在实际中变弱。这在 Atari 的部分环境中可能表现为性能波动。

2. **Lipschitz 假设的实践近似**：定理 2 和定理 4 均假设世界模型满足 Lipschitz 连续性。虽然通过 Lipschitz 网络结构可以近似保证，但在高维像素输入下，该假设仍可能被违反，此时回报差上界可能低估真实误差。

3. **环境泛化未验证**：实验仅覆盖 Atari-57 的随机版本，尚未在连续控制或部分可观测环境中测试。扩展到这些领域时，转移模型的 Wasserstein 距离计算和重要性比率的估计都可能面临新的挑战。

4. **重要性比率上界的估计**：定理 2 的回报差上界依赖于 $D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi})$，即行为策略与目标策略之间重要性比率的上确界。在实际中，这一量只能通过有限样本估计，估计误差可能影响约束的紧致性。论文将此列为开放问题之一，目前尚未提供实用的估计方案。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_24C3bSaH3F/figures/016_Figure_12.jpg]]
*Figure 12: Aggregate median, IQR, Mean, and optimality gap for the reported transition and reward losses over all the Atari environments considered in our experiments, with 95% confidence intervals. The confidence intervals are obtained via percentile bootstrapping with stratified resampling. For more information, refer to Agarwal et al., 2021b*



## 定位与知识库关联

### 1. 与基线方法的关系

DeepSPI 并非凭空设计，而是在策略优化与基于模型的强化学习两条主线的交汇处，针对现有方法在安全性与表征质量上的不足进行了系统性修补。

**相对于 PPO（Schulman et al., 2017）**：PPO 通过裁剪目标函数约束策略更新幅度，但这一约束是启发式的，既无法保证单调改进，也无法防止世界模型内的分布外（OOT）预测错误。DeepSPI 将 PPO 的策略更新框架保留为底层优化器，但做了两个关键替换：（1）用基于重要性比率（IR）的邻域算子 $\mathcal{N}^C$ 替代 PPO 的裁剪机制，使策略更新严格限制在 IR 上下界 $[2-C, C]$ 内，从而获得单调改进与收敛的理论保证（Thm.1）；（2）将优化目标从纯优势函数 $A^{\pi_n}$ 替换为效用函数 $U^{\pi_n} = A^{\pi_n} - \alpha_R \ell_R - \alpha_P \ell_P$，将局部奖励损失和转移损失直接纳入策略梯度信号。在玩具迷宫实验中，PPO 仅获得约 4.8 的回报，而 DeepSPI 达到约 8.01，差距源于 PPO 的表征将具有不同值的关键状态映射到隐空间中的相近位置（Figure 4 右图）。

**相对于 DeepMDP（Gelada et al., 2019）**：DeepMDP 同样在策略优化中引入辅助预测损失，但其损失定义在行为策略分布上，且缺乏对策略更新幅度的显式约束。DeepSPI 的关键改进在于将辅助损失与邻域约束联合使用：Thm.2 和 Thm.3 共同表明，仅当新旧策略的重要性比率有界（$D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b, \bar{\pi}) < 1/\gamma$）时，局部损失才能有效控制真实环境与世界模型之间的回报差。这解释了为何 DeepMDP 的辅助损失无法提供安全改进保证——它缺少将损失与策略更新幅度耦合的理论机制。实验上，DeepSPI 的转移损失 $L_P$ 显著低于 DeepMDP（均值差 $-0.1381$，$p = 6.6 \times 10^{-4}$，Wilcoxon 检验），表明邻域约束确实迫使世界模型在策略实际访问的区域保持更高的预测精度。

### 2. 理论根基与知识贡献

DeepSPI 的理论框架建立在三个相互支撑的支柱上：

- **邻域算子与镜像学习**：策略更新被证明是镜像学习（Kuba et al., 2022）的一个实例，从而继承了单调改进与收敛到最优值函数 $V^*$ 的保证。邻域算子的核心约束 $C < 1/\gamma$ 直接来源于 Thm.2 的分母条件，实践中取 $C = 1/\gamma - 1$。

- **局部损失与回报差上界**：Thm.2 给出的回报差上界
  $$|\rho(\bar{\pi}\circ\phi, \mathcal{M}) - \rho(\bar{\pi}, \overline{\mathcal{M}})| \leq \mathrm{AEL}(\pi_b) \cdot \frac{L_R^{\xi_{\pi_b}}/\gamma + K_V \cdot L_P^{\xi_{\pi_b}}}{1/D_{\mathrm{IR}}^{\mathrm{sup}}(\pi_b,\bar{\pi}) - \gamma}$$
  将世界模型质量（$L_R$、$L_P$）与策略偏移程度（$D_{\mathrm{IR}}^{\mathrm{sup}}$）统一在一个可优化的上界中。这是 DeepSPI 区别于以往基于模型方法的核心洞察：世界模型的局部精度而非全局精度决定了策略改进的安全性。

- **表征的近似 Lipschitz 连续性**：Thm.4 证明，最小化局部损失可确保值函数在多数状态下相对于表征距离近似 Lipschitz：
  $$|V^{\bar{\pi}}(s_1) - V^{\bar{\pi}}(s_2)| \leq K_V \cdot \bar{d}(\phi(s_1), \phi(s_2)) + \varepsilon$$
  这意味着相似值状态在隐空间中被有效分离，从而防止表征更新引发的混淆策略更新问题。实践中通过 Lipschitz 网络结构（而非梯度惩罚）实现这一性质，实验表明前者训练效率更高。

### 3. 适用边界

DeepSPI 的安全改进保证依赖于若干前提条件，这些条件划定了其适用边界：

- **回合制设定与重置状态对齐**：理论分析假设环境具有明确的回合终止条件，且世界模型与真实环境的初始状态分布通过编码器对齐。非回合制或无限视界环境需要额外扩展。
- **行为策略分布的充分覆盖**：安全改进的紧致性取决于 $\mathrm{AEL}(\pi_b)$ 和 $L_R^{\xi_{\pi_b}}$、$L_P^{\xi_{\pi_b}}$ 在行为策略平稳分布下的估计质量。若行为策略的探索不充分导致分布漂移，上界可能变得松弛。
- **世界模型的 Lipschitz 连续性假设**：Thm.2–4 均假设世界模型的奖励和转移函数满足 Lipschitz 条件。实践中虽可通过网络结构近似保证，但在高维观测或剧烈非平滑动态下可能被违反。
- **实验验证范围**：当前实验主要在 Atari ALE-57 的随机版本上进行，尚未在连续控制（如 MuJoCo）、部分可观测环境或真实机器人任务中验证。

### 4. 局限与开放问题

**已知局限**：
- 重要性比率上界 $D_{\mathrm{IR}}^{\mathrm{sup}}$ 在实践中难以精确估计，当前通过限制 IR 比为 $1/\gamma - 1$ 作为启发式替代，可能过于保守或不足。
- 效用函数中的系数 $\alpha_R$、$\alpha_P$ 需手动调节，缺乏自适应机制。
- DreamSPI（基于世界模型的规划扩展）虽能学习有意义行为（Figure 8），但其与 DeepSPI 理论保证的衔接尚未形式化。

**开放问题**：
- 如何将基于模型的规划步骤（如 DreamSPI 的想象 rollout）与 DeepSPI 的安全改进原则统一，以同时提升样本效率与安全性？
- 能否利用有理论保证的世界模型进行形式化安全验证或动作屏蔽，从而在部署前排除高风险动作？
- 如何在实际中高效估计和约束重要性比率上界，使理论保证在在线学习场景中可操作？
- 扩展到非回合制、一般平稳分布环境的理论保证需要哪些额外假设？
- 在连续控制或真实机器人任务中，Lipschitz 网络约束是否仍然足够，还是需要更精细的局部平滑性保证？



## 原文 PDF

![[paperPDFs/ICLR_2026/Deep_SPI_Safe_Policy_Improvement_via_World_Models.pdf]]
