---
title: "Robust Deep Reinforcement Learning against Adversarial Behavior Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Robust_Deep_Reinforcement_Learning_against_Adversarial_Behavior_Manipulation.pdf
project_link: null
code_link: null
openreview_forum_id: AC6lDj5dzl
aliases:
- BIABTDRTT
- RDRLAABM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "策略对状态变化的敏感性，尤其轨迹早期阶段的敏感性，直接影响攻击者的最大收益；通过减小该敏感性可抑制行为操控效果。"
primary_logic: "行为目标攻击可以转化为模仿学习问题，从而在无白盒访问下利用对抗演示训练对抗策略；基于时间折扣的正则化能够在保持原始任务性能的同时显著提升对行为操控攻击的鲁棒性。"
claims:
- "提出 Behavior Imitation Attack (BIA)，无需白盒访问受害者策略即可利用模仿学习实施攻击。"
- "提出时间折扣正则化（TDRT），在保障鲁棒性的同时维持原始任务性能。"
- "理论证明在任意目标策略下对手收益上界由策略动作对状态变化的敏感度决定，且早期轨迹的敏感度影响更大。"
- "TDRT-PPO 相比无时间折扣的 SA-PPO 平均原始任务性能提升 28.2%，同时保持相当的鲁棒性。"
---

# Robust Deep Reinforcement Learning against Adversarial Behavior Manipulation

> [!tip] 核心洞察
> 行为目标攻击可以转化为模仿学习问题，从而在无白盒访问下利用对抗演示训练对抗策略；基于时间折扣的正则化能够在保持原始任务性能的同时显著提升对行为操控攻击的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向对抗行为操控的鲁棒深度强化学习 |
| 英文题名 | Robust Deep Reinforcement Learning against Adversarial Behavior Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=AC6lDj5dzl) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Behavior Imitation Attack (BIA) 和 Time-Discounted Robust Training (TDRT) |
| Dataset | Meta-World (window-close), Meta-World (全部任务平均), Meta-World (window-close, 攻击者视角) |

> [!tip] 效果简介
> - Meta-World (window-close) 上，Clean Reward (无攻击，↑好) 为 TDRT-PPO 4412±55，对比 SA-PPO 4367±103，变化 +45 (同时鲁棒性相当)。
> - Meta-World (window-close) 上，Best Attack Reward (有攻击，↓好) 为 TDRT-PPO 482±3，对比 SA-PPO 485±61，变化 -3 (鲁棒性持平)。
> - Meta-World (全部任务平均) 上，原始任务性能相较 SA-PPO 提升 为 +28.2%，对比 SA-PPO 作为基准，变化 +28.2%。

## 概要

深度强化学习策略在面对状态观测扰动时存在严重脆弱性：攻击者通过注入精心构造的扰动，可在不改变环境真实状态的前提下操控受害者行为，使其执行攻击者指定的目标策略。这一威胁被称为**行为目标攻击**（behavior-targeted attack）。现有攻击手段普遍依赖白盒访问受害者策略（需获取梯度或参数），在真实部署场景中难以实施；而针对奖励最小化攻击设计的防御方法对行为操控攻击效果有限，导致缺乏独立的防御机制。

本文的核心洞察是：行为目标攻击可转化为模仿学习问题，从而在无白盒访问的条件下利用对抗演示训练对抗策略；同时，策略对状态变化的敏感性——尤其是轨迹早期阶段的敏感性——是决定攻击者收益上界的关键因素，通过时间折扣正则化有针对性地抑制该敏感性，能够在保持原始任务性能的同时显著提升鲁棒性。

具体而言，本文做出以下贡献：

1. **攻击方法**：提出**行为模仿攻击**（Behavior Imitation Attack, BIA），将行为目标攻击形式化为最小化合成策略与目标策略分布距离的问题，并通过理论重构将其转化为标准强化学习问题。BIA 利用 GAIL/GAIfO 等模仿学习框架训练对抗策略，仅需目标策略的演示数据，无需白盒访问受害者策略，在无盒（no-box）条件下亦可实施。

2. **防御方法**：提出**时间折扣鲁棒训练**（Time-Discounted Robust Training, TDRT），基于理论推导得出的对手收益上界——对手收益平方被每步策略 KL 散度的折扣和所控制，早期步因 $ \gamma^t $ 加权而影响更大——在 PPO 训练中引入时间折扣的 KL 正则项 $ \gamma^t D_{\mathrm{KL}}(\pi(\cdot|s) \| \pi \circ \nu(\cdot|s)) $，对轨迹早期阶段的动作敏感性施加更强的抑制。

3. **实验结果**：在 Meta-World、MuJoCo 和 MiniGrid 三类环境上验证，BIA 在黑盒/无盒条件下攻击性能与白盒基线相当；TDRT-PPO 相比无时间折扣的 SA-PPO 在全部任务中平均原始任务性能提升 **28.2%**，同时保持相当的鲁棒性（最佳攻击奖励持平）。

**方法定位**：BIA 属于黑盒对抗攻击方法，通过模仿学习绕过白盒访问限制；TDRT 属于基于正则化的经验防御方法，通过时间折扣机制在性能与鲁棒性之间取得优于均匀策略平滑的权衡。该方法不具备认证鲁棒性保证，在高维图像输入空间中攻击迁移效果受限，超参数 $ \lambda $ 需针对任务人工搜索。



深度强化学习（DRL）在机器人控制、自动驾驶等安全攸关领域的部署日益广泛，然而其对感知扰动的脆弱性已成为制约其可靠性的核心瓶颈。在诸多威胁模型中，**状态观测对抗攻击**（state-adversarial attack）尤为突出：攻击者不直接修改环境状态，而是通过扰动受害者的观测通道，诱导策略产生错误动作。这类攻击的隐蔽性和可实现性使其成为实际部署中的重大隐患。

### 行为目标攻击：从奖励最小化到行为操控

现有状态观测攻击大致可分为两类。第一类以**奖励最小化**为目标，攻击者通过最大化受害者累积奖励的下降幅度来降低任务性能。第二类则更为隐蔽和危险——**行为目标攻击**（behavior-targeted attack），攻击者不仅希望降低原始任务性能，更意图将受害者策略诱导至特定的对抗性行为模式。例如，在自动驾驶场景中，攻击者可能不满足于让车辆减速，而是精确操控车辆转向错误车道。

行为目标攻击的威胁等级更高，但现有研究在两个关键维度上存在明显缺口：

1. **攻击方法的实用性不足**。当前行为目标攻击方法（如 Targeted PGD、SA-RL、PA-AD）普遍依赖对受害者策略的白盒访问——攻击者需要获取策略的梯度信息或参数。在真实部署场景中，受害者策略通常以黑盒或仅通过 API 暴露，白盒假设严重限制了攻击的可行性。

2. **防御机制的独立缺失**。针对奖励最小化攻击的防御方法（如 SA-PPO、ATLA-PPO、WocaR-PPO、RAD-PPO）主要围绕状态扰动下的值函数或策略平滑展开，但这些方法并非为行为操控攻击设计。理论分析和实验均表明，均匀的策略平滑虽能提升对行为目标攻击的鲁棒性，但会以显著牺牲原始任务性能为代价——在无攻击时，防御策略的性能下降可达 28.2% 以上。

### 核心瓶颈与本文动机

上述缺口指向一个更深层的矛盾：**行为目标攻击的防御需要抑制策略对状态变化的敏感性，但过度的全局敏感性抑制会损害策略在原始任务上的表达能力**。这一矛盾在轨迹的不同时间步上并非均匀分布——理论分析表明，攻击者的最大收益受制于策略动作对状态变化的敏感度，且**轨迹早期阶段的敏感性对攻击收益的影响远大于后期阶段**。直观上，早期状态的微小偏移会通过时序累积效应放大为后续轨迹的剧烈偏离，而后期状态的扰动对整体行为的影响则相对有限。

然而，现有防御方法（如 SA-PPO）采用均匀的时间权重进行策略平滑，未能区分不同时间步敏感性的差异化影响，导致防御效率低下：为达到足够的鲁棒性，必须施加高强度的全局正则化，从而过度抑制了策略的正常表达能力。

本文正是针对上述瓶颈展开。核心动机可概括为两个层面：

- **攻击侧**：摆脱白盒依赖，设计一种在有限访问条件下（黑盒甚至无盒）仍能有效实施行为目标攻击的实用方法。关键思路是将行为目标攻击重新表述为模仿学习问题——攻击者无需接触受害者策略内部，仅通过目标行为的演示即可训练对抗策略。

- **防御侧**：在保持原始任务性能的前提下实现针对行为目标攻击的鲁棒性。核心洞察在于引入**时间折扣机制**，对轨迹早期步骤施加更强的敏感性抑制，而对后期步骤逐步放松约束，从而在鲁棒性与任务性能之间取得精细平衡。理论保证来自对手收益上界的推导：对手收益的平方被每步策略 KL 散度的折扣和控制，其中早期步的权重（$\gamma^t$ 项）显著更大，这为时间折扣正则化提供了形式化支撑。



## 核心方法与创新机理

本文的核心创新围绕“对抗行为操控”（Behavior-Targeted Attack）这一威胁模型展开，从攻击与防御两侧分别提出了关键改进，并通过理论分析揭示了策略敏感性与攻击收益之间的因果联系。

### 攻击侧：从白盒依赖到无盒模仿

现有行为目标攻击方法（如 Targeted PGD 和基于奖励最大化的 SA-RL / PA-AD）均需白盒访问受害者策略——要么需要策略梯度，要么需要策略输出的动作分布。这一前提在实际部署中严重限制了攻击的实用性。

本文的核心突破在于**将行为目标攻击重新表述为模仿学习问题**。通过理论推导（Theorem 5.1），作者证明：最小化合成策略 $\pi \circ \nu$ 与目标策略 $\pi_{\mathrm{tgt}}$ 之间的分布散度，等价于在一个精心构造的 MDP $\hat{M}$ 中最大化累积奖励。这一转化直接消除了对受害者策略白盒访问的依赖——攻击者只需收集目标策略的演示数据，即可利用 GAIL 或 GAIfO 等标准模仿学习算法训练对抗策略 $\nu$。

据此提出的 **Behavior Imitation Attack (BIA)** 在访问条件上实现了显著跨越：

- **BIA-ILfD**：仅需目标策略的状态-动作演示，属于黑盒攻击；
- **BIA-ILfO**：仅需状态序列（无需动作标签），属于无盒攻击。

在 Meta-World 的 window-close 任务上，BIA-ILfD 的攻击奖励达到 4505±65（Table 1），与拥有奖励函数白盒访问的 Rew Max (PA-AD) 的 4255±300 相当甚至更优，而单步优化的 Targeted PGD 仅获得 1666±936。这表明**序列决策层面的模仿远比逐步贪心扰动有效**。

### 防御侧：从均匀平滑到时间折扣正则化

防御侧的关键洞察来自 Theorem 6.1：对手收益的平方被每步策略 KL 散度的折扣和所控制：

$$\left( \frac{1}{\sqrt{2} \bar{R}_{\mathrm{tgt}}} \left( \mathbb{E}_{\pi \circ \nu}^{M}[R_{\mathrm{tgt}}] - \mathbb{E}_{\pi}^{M}[R_{\mathrm{tgt}}] \right) \right)^{2} \leq \sum_{t=0}^{\infty} \frac{\gamma^{t}}{1-\gamma} \mathbb{E}_{s \sim d_{\pi}^{t}} [D_{\mathrm{KL}}(\pi(\cdot|s) \| \pi \circ \nu(\cdot|s))]$$

该上界揭示了两个关键性质：① **策略动作对状态变化的敏感度越小，攻击收益越低**；② **折扣因子 $\gamma^t$ 使得早期时间步的敏感度对攻击收益的影响远大于后期**。

现有防御方法 **SA-PPO**（Zhang et al., 2020b）采用均匀的全局策略平滑正则化，未区分时间步的重要性差异。这导致为保证足够鲁棒性，SA-PPO 必须在整个轨迹上施加高强度正则化，从而严重损害原始任务性能——例如在 drawer-close 任务上，SA-PPO 的 clean reward 降至 2156±453，仅为 TDRT-PPO 的约一半（Table 3）。

本文提出的 **Time-Discounted Robust Training (TDRT)** 将正则化项修改为时间折扣形式：

$$J_{\mathrm{def}}(\pi) = -J_{\mathrm{RL}}(\pi) + \lambda \max_{\nu} \sum_{s_t \in B} \gamma^{t} D_{\mathrm{KL}}\big(\pi(\cdot|s_t) \| \pi \circ \nu(\cdot|s_t)\big)$$

这一设计**在轨迹早期施加更强的敏感性抑制，而在后期逐步放松约束**，从而在保障鲁棒性的同时大幅释放原始任务性能。实验表明，TDRT-PPO 在所有 Meta-World 任务上均以更高的 clean reward 获得与 SA-PPO 相当的 best attack reward，平均原始任务性能提升 **28.2%**。

### 攻击-防御协同的理论闭环

两项创新并非孤立存在。Theorem 6.1 的上界恰好将**攻击者的优化目标**（最大化目标奖励增量）与**防御者的可操作变量**（策略 KL 散度）通过时间折扣权重统一在同一框架下。这使得 TDRT 的防御设计直接针对 BIA 类攻击的因果机制——降低早期轨迹的策略敏感性——而非泛泛的鲁棒训练。这种“攻击揭示脆弱性、防御针对脆弱性”的闭环设计，是本文方法论层面的深层贡献。

### 局限性

需要指出，TDRT 的超参数 $\lambda$ 仍需针对每个任务手动搜索（Table 13 显示 $\lambda=0.03$ 时鲁棒性大幅下降，$\lambda=0.1\sim0.3$ 为最佳区间），且缺乏对未见攻击的认证鲁棒性保证。在图像输入等高维状态空间下，BIA 的攻击迁移效果也显著受限（Table 7）。



![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SA-MDP*

本文围绕**状态对抗马尔可夫决策过程（SA-MDP）**构建攻防框架。在该框架下，受害者策略 $\pi$ 在每个时间步接收到的不是真实环境状态 $s_t$，而是由对抗策略 $\nu$ 生成的虚假状态 $\hat{s}_t \sim \nu(\cdot|s_t)$，受害者据此选择动作 $a_t \sim \pi(\cdot|\hat{s}_t)$。这一交互机制将受害者的有效行为策略定义为**合成策略**：

$$\pi \circ \nu ( a | s ) \triangleq \sum _ { \hat { s } \in \mathcal{S} } \nu ( \hat { s } | s ) \pi ( a | \hat { s } )$$

攻击者的目标是将合成策略 $\pi \circ \nu$ 拉向一个预定义的**目标策略 $\pi_{\text{tgt}}$**，即最小化两者之间的分布距离 $\mathcal{D}(\pi \circ \nu, \pi_{\text{tgt}})$。

### 攻击端：Behavior Imitation Attack (BIA)

BIA 的核心洞察在于将行为目标攻击重新表述为**模仿学习问题**。通过变分表示理论，分布匹配目标可转化为在构造的 MDP $\hat{M}$ 中最大化累积奖励的标准强化学习问题，从而**无需白盒访问受害者策略**即可训练对抗策略 $\nu$。具体实现分为两条路径：

- **BIA-ILfD（基于演示）**：利用目标策略 $\pi_{\text{tgt}}$ 的轨迹演示，通过 GAIL 框架训练判别器 $D$ 区分合成策略 rollouts 与目标策略演示，为对抗策略提供奖励信号。
- **BIA-ILfO（基于观测）**：仅需状态序列而无需动作标签，适用于**无盒（no-box）**场景，即攻击者完全无法获取受害者策略的任何输出。

训练流程如 Algorithm 1 所示：交替更新判别器（区分合成轨迹与目标演示）和对抗策略（最大化判别器赋予的奖励），最终收敛到能够有效模仿目标行为的 $\nu$。

### 防御端：Time-Discounted Robust Training (TDRT)

防御者的目标是在维持原始任务性能 $J_{\text{RL}}(\pi)$ 的同时，抑制攻击者通过行为操控能获得的最大收益。理论分析（Theorem 6.1）揭示了一个关键因果机制：**对手收益的上界由策略动作对状态变化的 KL 散度的折扣和所控制**，且轨迹早期步骤的敏感度因 $\gamma^t$ 权重而具有更大影响。

基于此，TDRT 在 PPO 训练框架中引入**时间折扣 KL 正则化项**：

$$J_{\text{def}}(\pi) = -J_{\text{RL}}(\pi) + \lambda \max_{\nu} \sum_{s_t \in B} \gamma^t D_{\text{KL}}\big(\pi(\cdot|s_t) \| \pi \circ \nu(\cdot|s_t)\big)$$

其中 $B$ 为 mini-batch，$\gamma^t$ 折扣因子使正则化强度沿时间步递减。与无时间折扣的均匀策略平滑（如 **SA-PPO**，Zhang et al., 2020b）相比，TDRT 在轨迹早期施加更强的敏感性抑制，而在后期逐步放松约束，从而在保障鲁棒性的同时显著减轻对原始任务性能的损害。完整训练流程见 Algorithm 2。

### 模块关系与数据流

整体 pipeline 包含三个核心模块，形成闭环：

1. **对抗策略训练模块（BIA）**：以目标策略演示为输入，通过模仿学习输出对抗策略 $\nu$，用于生成对抗扰动。
2. **时间折扣 KL 正则化模块（TDRT）**：在受害者策略 $\pi$ 的 PPO 更新中，计算当前策略与受扰动策略 $\pi \circ \nu$ 之间的时间折扣 KL 散度，作为鲁棒正则项加入损失函数。
3. **PPO 鲁棒训练框架**：以原始环境交互数据和对抗扰动为输入，输出经过鲁棒训练的受害者策略 $\pi^*$。

输入输出流为：目标演示 → BIA → $\nu$ → 对抗状态 $\hat{s}$ → $\pi$ 产生动作 → 环境反馈 → PPO + TDRT 正则化 → 更新后的 $\pi$。攻防双方交替或独立训练，最终评估时以 $\pi$ 在面对 $\nu$ 攻击时的表现衡量鲁棒性。



### 合成策略与攻击目标

行为操控攻击的核心机制是：攻击者训练一个对抗策略 $\nu(\hat{s}|s)$，在真实状态 $s$ 下生成一个虚假状态 $\hat{s}$ 注入受害者的观测通道。受害者在观测到 $\hat{s}$ 后，依据自身策略 $\pi(a|\hat{s})$ 选择动作。由此，受害者的实际行为由**合成策略**（Composite Policy）描述：

$$\pi \circ \nu ( a | s ) \triangleq \sum _ { \hat { s } \in \mathcal{S} } \nu ( \hat { s } | s ) \pi ( a | \hat { s } )$$

攻击者的目标是使合成策略尽可能接近其期望的**目标策略** $\pi_{\mathrm{tgt}}$，即最小化两者之间的分布距离：

$$\underset { \nu } { \arg \operatorname* { m i n } } \mathcal { D } ( \pi \circ \nu , \pi _ { \mathrm { t g t } } )$$

其中 $\mathcal{D}$ 为 $f$-散度类距离度量。

### 攻击模块：从分布匹配到强化学习

**核心洞察**：上述分布匹配问题可转化为一个标准强化学习问题，从而无需白盒访问受害者策略即可训练对抗策略。这是 Behavior Imitation Attack (BIA) 的理论基础。

**转化机制**：利用 $f$-散度的变分表示，将分布匹配目标重写为在构造的 MDP $\hat{M}$ 中最大化累积奖励的形式。$\hat{M}$ 的状态空间为 $\mathcal{S} \times \mathcal{S}$（真实状态与虚假状态的配对），其虚设奖励函数为：

$$\hat { R } _ { d } ( s , \hat { s } , s ^ { \prime } ) = \left\{ \begin{array} { l l } { - \frac { \sum _ { a \in A } \pi ( a | \hat { s } ) p ( s ^ { \prime } | s , a ) g ( d _ { \star } ( s , a , s ^ { \prime } ) ) } { \sum _ { a \in A } \pi ( a | \hat { s } ) p ( s ^ { \prime } | s , a ) } } & { \text{if } \hat { s } \in \mathcal { B } ( s ) } \\ { C } & { \text{otherwise} } \end{array} \right.$$

其中 $d_{\star}$ 为最优判别器，$g$ 为与 $f$-散度对应的凸函数，$\mathcal{B}(s)$ 为以 $s$ 为中心的 $L_\infty$ 扰动球。该奖励函数仅在虚假状态落在扰动预算内时有效，否则给予常数惩罚 $C$。

**关键优势**：该转化后的 MDP 中，奖励函数 $\hat{R}_d$ 的计算仅依赖受害者策略在虚假状态上的动作分布 $\pi(a|\hat{s})$，而不需要受害者策略的梯度或内部参数。这使得 BIA 可在**黑盒**（有动作标签）甚至**无盒**（仅需状态转移观测）条件下实施。

**实践实现**：BIA 采用生成对抗模仿学习（GAIL）或其仅观测变体（GAIfO）训练对抗策略。GAIL 框架下，判别器 $D$ 区分合成策略的 rollout 与目标策略的演示，对抗策略 $\nu$ 以判别器输出为奖励信号进行强化学习更新。完整流程见 Algorithm 1。

### 防御模块：敏感度上界与时间折扣正则化

**理论瓶颈**：防御者需要抑制攻击者通过状态操控能获得的最大收益。Theorem 6.1 给出了该收益的平方上界：

$$\left( \frac { 1 } { \sqrt { 2 } \bar { R } _ { \mathrm{tgt} } } \left( \mathbb { E } _ { \pi \circ \nu } ^ { M } [ R _ { \mathrm{tgt} } ( s , a ) ] - \mathbb { E } _ { \pi } ^ { M } [ R _ { \mathrm{tgt} } ( s , a ) ] \right) \right) ^ { 2 } \leq \sum _ { t = 0 } ^ { \infty } \frac { \gamma ^ { t } } { 1 - \gamma } \mathbb { E } _ { s \sim d _ { \pi } ^ { t } } [ D _ { K L } ( \pi ( \cdot | s ) \| \pi \circ \nu ( \cdot | s ) ) ]$$

**上界含义**：
- 攻击者收益的平方被每步策略 KL 散度的折扣和所控制。
- 公式右侧的 $\gamma^t$ 因子意味着**轨迹早期步的敏感度对攻击收益的影响被指数级放大**（$t$ 越小，$\gamma^t$ 越大），而后期步的影响被折扣衰减。
- 因此，抑制策略动作对状态变化的敏感性，尤其是轨迹早期的敏感性，是防御行为操控攻击的关键。

**防御目标**：基于上述上界，防御者的优化目标定义为：

$$J _ { \mathrm { d e f } } ( \pi ) = - J _ { \mathrm { R L } } ( \pi ) + \lambda \left( \underset { \nu } { \operatorname* { m a x } } \mathbb { E } _ { \pi \circ \nu } ^ { M } [ R _ { \mathrm { t g t } } ( s , a ) ] - \mathbb { E } _ { \pi } ^ { M } [ R _ { \mathrm { t g t } } ( s , a ) ] \right)$$

防御者最小化原始任务损失 $-J_{\mathrm{RL}}(\pi)$ 的同时，抑制对手通过攻击能获得的最大目标奖励提升。$\lambda$ 控制鲁棒性与任务性能的权衡。

**TDRT 实际训练目标**：将上界中的 KL 散度项直接作为正则化器，并在 mini-batch 上通过凸松弛近似内部最大化，得到 **Time-Discounted Robust Training (TDRT)** 的实际优化目标：

$$J _ { \mathrm { d e f } } ( \pi ) = - J _ { \mathrm { R L } } ( \pi ) + \lambda \operatorname* { m a x } _ { \nu } \sum _ { s _ { t } \in B } \gamma ^ { t } D _ { \mathrm { K L } } \big ( \pi ( \cdot | s _ { t } ) \| \pi \circ \nu ( \cdot | s _ { t } ) \big )$$

**与均匀正则化的本质区别**：无时间折扣的防御方法（如 SA-PPO）对所有时间步施加等权重 KL 正则化。TDRT 通过 $\gamma^t$ 加权，**对轨迹早期步施加更强的正则化**，对后期步逐渐放松约束。这一设计使得策略在保持整体鲁棒性的同时，减少了对后期步的不必要约束，从而显著提升原始任务性能。消融实验证实：TDRT-PPO 相比 SA-PPO 在所有任务中均以更高的 clean reward 获得相似的 best attack reward，平均原始任务性能提升 28.2%。



## 实验与关键发现

### 攻击性能对比

本节首先评估各类攻击方法在 Meta-World 基准上的有效性。表 1 展示了五种对抗任务（window-close、drawer-close、handle-press-side、faucet-close、door-lock）下不同攻击方法的平均 episode 奖励。核心发现如下：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/002_Table_1.jpg]]
*Table 1: Comparison of attack performances. Each value represents the average episode reward ± standard deviation over 50 episodes. Each parenthesis indicates (Access model, Adversary’s knowledge). Under the limited-knowledge setting, BIA’s attack performance is competitive with that of baseline methods that assume greater adversary knowledge*

**BIA 在受限访问条件下达到与白盒攻击相当的强度。** BIA-ILfD（基于演示的模仿学习）仅需 20 条目标策略演示，不访问受害者策略参数，在 window-close 任务上达到 4505±65 的攻击奖励，与拥有奖励函数访问权限的 Target Reward Maximization（SA-RL，白盒）的 4344±416 处于同一水平。在 drawer-close 任务上，BIA-ILfD 的 4760±640 甚至超过了基于奖励的攻击方法 PA-AD（3768±1733）。这表明**将行为目标攻击转化为模仿学习问题**的策略绕过了对受害者梯度信息的依赖，实现了攻击能力的有效迁移。

**单步攻击的局限性被暴露。** Targeted PGD 攻击在每个时间步独立优化对抗扰动，不考虑未来决策的累积效应。在 window-close 任务上，Targeted PGD 仅获得 1666±936 的攻击奖励，远低于 BIA-ILfD 的 4505±65（差距约 2839）。这一差距在所有任务中一致出现，验证了**行为操控需要跨时间步的策略级优化，而非逐步贪心扰动**。

**BIA-ILfO 在无动作信息下仍保持攻击力。** 当仅提供状态观测（ILfO 模式）时，BIA 在 window-close 上达到 3962±666，与 BIA-ILfD 的 4505±65 相比下降有限，且方差增大。这说明 BIA 在 no-box 设定下仍具威胁，但状态-动作联合信息对稳定性有贡献。

### 防御性能对比

表 2 和表 3 对比了六种防御方法在 Meta-World 任务上的鲁棒性与原始任务性能。核心结论：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/003_Table_2.jpg]]
*Table 2: Comparison of robustness. Each value represents the average episode reward ± standard deviation over 50 episodes. Policy smoothing is very effective against behavior-targeted attacks*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/004_Table_3.jpg]]

**策略平滑是抵御行为目标攻击的有效手段。** TDRT-PPO 和 SA-PPO 在所有任务中均将最佳攻击奖励压制到极低水平。以 window-close 为例，无防御的 Vanilla PPO 在攻击下获得 4505±65 的奖励，而 TDRT-PPO 将其降至 482±3，SA-PPO 降至 485±61。相比之下，对抗训练方法 ATLA-PPO 和 PA-ATLA-PPO 在多数任务上仍被攻破（如 window-close 下 ATLA-PPO 的攻击奖励为 4008±198，接近无防御水平），说明**针对观测扰动的对抗训练无法泛化到行为目标攻击**。

**时间折扣正则化在鲁棒性与任务性能之间取得更优权衡。** 表 3 显示，TDRT-PPO 在所有 10 个 Meta-World 任务上的 clean reward 均高于 SA-PPO。平均而言，TDRT-PPO 相较 SA-PPO 的原始任务性能提升 **28.2%**，同时保持相当的鲁棒性（表 2 中最佳攻击奖励差异不显著）。以 drawer-close 任务为例：SA-PPO 为达到极低攻击奖励（4±2）付出了 clean reward 从约 4800 降至 2156±453 的代价；TDRT-PPO 在攻击奖励 4860±4 的情况下保持了 4237±93 的 clean reward。这验证了 Theorem 6.1 的推论：**对轨迹早期阶段施加更强的敏感性抑制，对后期阶段放松约束，可在不牺牲整体任务性能的前提下有效限制攻击者的最大收益**。

### 消融实验

**正则化系数 λ 的影响。** 表 13 在 window-close 和 window-open 任务上系统扫描了 λ ∈ {0.03, 0.1, 0.3, 0.5}。当 λ=0.03 时，TDRT-PPO 的鲁棒性大幅下降（window-close 最佳攻击奖励升至 1879±580），表明正则化强度不足。λ 增大至 0.1~0.3 区间时，clean reward 与最佳攻击奖励达到最优平衡；进一步增大至 0.5 时鲁棒性不再提升，且 clean reward 出现轻微下降。SA-PPO 在无时间折扣下，为获得可比的鲁棒性需要更高的 λ，导致更严重的性能退化。这一消融直接证实了**时间折扣机制而非单纯的正则化强度**是性能保持的关键。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/025_Table_13.jpg]]
*Table 13: Comparison between TDRT-PPO and SA-PPO with different λ values. Each value is the average episode rewards ± standard deviation over 50 episodes. Clean Rewards are the rewards for the victim’s tasks (no attack). Best attack rewards represent the highest attack reward among the five types of adversarial attacks. The attack budget is set to $\epsilon$ = 0 . 3 . In SA-PPO, which does not apply time discounting, ensuring sufficient robustness leads to a significant drop in performance on the original task. In contrast, TDRT-PPO, which applies time discounting, achieves high robustness while preserving the original-task performance*

**演示数量的稳健性。** 图 3 展示了 BIA 攻击性能随演示集大小的变化。在 window-close 任务上，演示数量从 20 集降至 4 集时，攻击奖励无明显下降，说明 BIA 对演示数据量的需求较低，降低了攻击门槛。

**攻击预算的影响。** 图 4 显示，随攻击预算 ε 从 0.05 增大至 0.5，BIA-ILfD 和 BIA-ILfO 的攻击奖励单调上升并逐渐逼近目标策略的奖励上界。在 ε=0.3 附近攻击效果趋于饱和，表明适中的扰动预算已足以实现有效的行为操控。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_AC6lDj5dzl/figures/020_Figure_4.jpg]]
*Figure 4: Attack performance of BIA-ILfD/ILfO with varying attack budget ϵ. The x-axis shows the value of the attack budget, and the y-axis represents the attack reward. The target reward represents the cumulative reward obtained by the target policy and serves as the upper bound for the attack rewards of BIA-ILfD/ILfO. Each environment name represents an adversarial task. The solid line and shaded area denote the mean and the standard deviation / 2 over 50 episodes*

### 跨环境泛化

**MuJoCo 连续控制。** 表 4 和表 5 在 Ant、HalfCheetah、Hopper 三个 MuJoCo 任务上验证了方法的泛化性。BIA-ILfD 在 Ant 任务上达到 5657±172 的攻击奖励，超过基于奖励的 SA-RL（5073±154）。TDRT-PPO 在所有三个任务上均以最高 clean reward 实现最低或接近最低的最佳攻击奖励（表 5），证实时间折扣正则化在连续高维动作空间中同样有效。

**MiniGrid 离散动作空间。** 表 6 和表 8 在坐标状态表示的 MiniGrid 8×8 和 16×16 任务上验证了方法对离散动作空间的适用性。TDRT-PPO 在保持高 clean reward（~0.92-0.93）的同时将攻击奖励压制到接近零的水平。

**图像输入的限制。** 表 7 和表 9 展示了图像状态空间下的结果。TDRT-PPO 的防御仍然有效，但 BIA-ILfD 的攻击效果显著下降——在 window-close 任务上仅达到 1386±896 的攻击奖励，远低于目标奖励 4617。这表明**基于演示的模仿攻击在高维感知输入下存在迁移瓶颈**，是该方法的已知失败模式。

### 计算成本

表 14 对比了各方法的训练时间。在 window-close 任务上，TDRT-PPO 的训练时间为 7.2 小时，SA-PPO 为 6.8 小时，额外的时间折扣计算带来的开销可忽略。BIA 的攻击策略训练时间约为 2-3 小时，与攻击预算 ε 的大小相关。所有实验均在 Nvidia H100 GPU 上以 300 万步的相同训练预算完成，确保了对比的公平性。



## 定位与知识库关联

### 核心瓶颈与突破路径

本文针对深度强化学习中一个此前缺乏有效攻击手段和独立防御机制的安全缺口：**行为目标攻击**（behavior-targeted attack）。此类攻击的目标不是简单降低受害者累积奖励，而是将受害者策略诱导至攻击者指定的任意目标行为。现有攻击方法存在两个关键瓶颈：(1) 基于奖励最大化的攻击（如 Target Reward Maximization）需要白盒访问受害者策略或攻击者奖励函数，实用性受限；(2) 基于逐步优化的攻击（如 Targeted PGD）将扰动优化视为单步决策问题，忽略轨迹的时序依赖性，导致攻击效果远低于理论上限。在防御侧，针对奖励最小化攻击设计的对抗训练方法（如 ATLA-PPO、PA-ATLA-PPO）在面对行为操控攻击时几乎无效，而策略平滑方法（如 SA-PPO）虽能提供鲁棒性，却以牺牲原始任务性能为代价。

本文的核心突破在于两条因果路径的打通：**攻击侧**，通过将行为目标攻击重新形式化为分布匹配问题，并利用 f-散度的变分表示将其转化为标准 MDP 中的累积奖励最大化问题（Theorem 5.1），从而将攻击问题桥接到模仿学习领域，使得在无白盒访问甚至无动作观测的极端条件下也能训练有效的对抗策略；**防御侧**，通过理论推导出对手收益的上界由策略动作对状态变化的 KL 散度沿轨迹的时间折扣和所控制（Theorem 6.1），揭示了轨迹早期阶段的策略敏感性对攻击效果具有不成比例的影响，进而设计出时间折扣正则化机制，在抑制敏感性的同时保留后期策略灵活性，实现鲁棒性与任务性能的帕累托改进。

### 攻击方法谱系定位

行为目标攻击的形式化可追溯至 SA-MDP 框架，该框架将对手建模为在受害者观测通道中注入状态扰动的对抗策略 $\nu$，使受害者实际执行的行为策略变为合成策略 $\pi \circ \nu$。在此框架下，本文的 BIA 方法在攻击假设和实现路径上与现有工作形成如下谱系关系：

| 攻击方法 | 所需访问权限 | 核心机制 | 行为操控能力 |
|----------|-------------|---------|-------------|
| Random Attack | 无盒（no-box） | 随机采样对抗状态 | 极弱 |
| Targeted PGD | 白盒（梯度访问） | 逐步最小化 $\pi(\cdot\mid\hat{s})$ 与 $\pi_{\text{tgt}}(\cdot\mid s)$ 的距离 | 弱（忽略时序） |
| Target Reward Maximization (SA-RL) | 黑盒（需攻击者奖励函数 $R_{\text{adv}}$） | 在原始 MDP 中最大化 $R_{\text{adv}}$ 下的累积奖励 | 中 |
| Target Reward Maximization (PA-AD)（Sun et al., 2022） | 白盒（需受害者策略参数） | 在 SA-MDP 中最大化 $R_{\text{adv}}$ | 中 |
| **BIA-ILfD（本文）** | 黑盒（仅需目标策略演示） | GAIL 框架下训练对抗策略，判别器区分合成 rollouts 与目标演示 | 强 |
| **BIA-ILfO（本文）** | 无盒（仅需状态序列观测） | GAIfO 框架，判别器仅使用状态转移对 | 强（与 ILfD 几乎持平） |

BIA 的核心创新在于**将攻击从奖励工程中解放出来**。传统攻击方法需要攻击者显式定义奖励函数 $R_{\text{adv}}$ 来刻画目标行为，这在行为目标攻击场景中往往不可行——攻击者可能只有目标行为的演示，而无法为其设计稠密奖励。BIA 通过 Theorem 5.1 的等价变换，将分布匹配目标 $\min_\nu \mathcal{D}(\pi \circ \nu, \pi_{\text{tgt}})$ 转化为 MDP $\hat{M}$ 中的标准 RL 问题，其中虚设奖励函数 $\hat{R}_D$ 由判别器 $D$ 隐式定义。这使得攻击者只需收集目标策略的演示轨迹即可发动攻击，显著降低了攻击门槛。

实验证据表明（Table 1），BIA-ILfD 在 window-close 任务上达到 4505±65 的攻击奖励，与需要白盒访问的 PA-AD（4255±300）相当甚至略优，而 Targeted PGD 仅能达到 1666±936。这一差距源于 Targeted PGD 的逐步贪婪优化无法协调跨时间步的扰动选择，导致轨迹后期的扰动空间被前期短视决策所耗尽。

### 防御方法谱系定位

在防御侧，现有方法可分为三个流派：

**对抗训练流派**：以 ATLA-PPO（Zhang et al., 2021）和 PA-ATLA-PPO（Sun et al., 2022）为代表，通过在训练过程中注入对抗扰动并优化最坏情况性能来提升鲁棒性。这类方法针对奖励最小化攻击设计，其对抗扰动方向由价值函数或策略输出的最坏情况下降方向决定。然而，行为目标攻击的扰动方向由目标策略决定，与受害者自身的奖励结构无关，导致对抗训练学到的鲁棒性无法泛化到行为操控场景。Table 2 显示，ATLA-PPO 在 window-close 任务上的最佳攻击奖励高达 4065±142，接近无防御 PPO 的 4577±102，几乎未提供任何防护。

**策略平滑流派**：以 SA-PPO（Zhang et al., 2020b）为代表，通过在策略输出上施加局部 Lipschitz 约束（如最小化 $\pi(\cdot\mid s)$ 与 $\pi(\cdot\mid \hat{s})$ 之间的 KL 散度）来抑制对抗扰动的影响。这一流派直接针对行为操控攻击的机理——减小策略对状态变化的敏感性——因此展现出显著优于对抗训练的鲁棒性。然而，SA-PPO 对轨迹所有时间步施加均匀的正则化强度，导致策略在需要精确控制的后期阶段也被过度平滑，原始任务性能严重退化。Table 3 显示，SA-PPO 在 drawer-close 任务上的 clean reward 仅为 2156±453，而 TDRT-PPO 可达 4237±93。

**认证防御流派**：以 WocaR-PPO（Liang et al., 2022）和 RAD-PPO（Belaire et al., 2024）为代表，通过区间传播或 Lipschitz 常数估计提供形式化的鲁棒性下界。这类方法在奖励最小化攻击下具有理论保证，但其认证边界通常针对最坏情况奖励下降设计，无法直接迁移到行为目标攻击场景——行为操控攻击的危害不在于奖励下降，而在于行为偏离，两者的度量空间不同。本文的 TDRT 属于经验防御方法，缺乏认证保证，这是其相对于认证防御流派的主要不足。

**TDRT 的关键创新**在于从 Theorem 6.1 的理论洞察出发，识别出**轨迹早期阶段的策略敏感性对攻击收益具有更大的乘数效应**（由 $\gamma^t / (1-\gamma)$ 因子控制），因此在正则化中引入时间折扣权重 $\gamma^t$，对早期步骤施加更强的平滑约束，对后期步骤逐渐放松。这一设计使得 TDRT-PPO 在所有 Meta-World 任务上以更高的 clean reward 获得与 SA-PPO 相当的最佳攻击奖励（Table 3 vs Table 2），平均原始任务性能提升 28.2%。

### 适用边界与局限

**攻击方法的适用边界**：

1. **目标策略质量依赖**：BIA 的攻击奖励上界由目标策略 $\pi_{\text{tgt}}$ 的累积奖励决定。若目标策略本身性能低下，攻击奖励也相应受限。这一性质源于模仿学习的保真度上限——对抗策略只能逼近目标策略的行为分布，无法超越。

2. **高维感知输入的退化**：在 MiniGrid 图像状态空间中（Table 7），BIA-ILfD 的攻击奖励显著下降（8×8 任务中仅 0.12±0.05，而白盒 PA-AD 可达 0.62±0.13）。这是因为从高维像素输入中学习状态扰动策略需要大量样本，而模仿学习框架下的判别器信号在高维空间中稀疏且噪声大，导致对抗策略训练困难。这一局限在真实机器人视觉场景中将更加突出。

3. **扰动类型限制**：所有实验均基于 $L_\infty$ 范数约束的扰动模型。对于 $L_2$、$L_1$ 或其他语义扰动类型，Theorem 5.1 的 MDP 重构是否仍然成立需要重新验证——虚设奖励函数 $\hat{R}_D$ 的形式依赖于扰动约束集 $\mathcal{B}(s)$ 的结构。

4. **演示数量稳健但非零样本**：BIA 在演示数量从 20 集降至 4 集时攻击奖励无明显下降（Figure 3），表现出良好的样本效率。但该方法仍需要至少少量目标策略演示，无法在完全无目标行为信息的零样本条件下运作。

**防御方法的适用边界**：

1. **缺乏认证保证**：TDRT 是一种经验防御方法，其鲁棒性通过实验评估而非形式化下界保证。在面对自适应攻击（如针对 TDRT 正则化项设计的对抗策略）时，其有效性未经检验。这与 WocaR-PPO 等认证防御方法形成对比，后者可提供独立于攻击方法的鲁棒性证书。

2. **超参数敏感性**：TDRT 的正则化强度 $\lambda$ 需要在每个任务上单独搜索。Table 13 显示，$\lambda=0.03$ 时鲁棒性大幅下降（window-close 最佳攻击奖励升至 4252±195），$\lambda=0.1\sim0.3$ 时达到最佳权衡，$\lambda=0.5$ 时鲁棒性不再提升且 clean reward 有所下降。这一单调但非线性的关系意味着 $\lambda$ 的选择存在任务相关的临界区间，目前缺乏自适应调节机制。

3. **扰动模型的耦合性**：TDRT 的正则化项 $\max_\nu \sum \gamma^t D_{\text{KL}}(\pi(\cdot\mid s_t) \mid\mid \pi\circ\nu(\cdot\mid s_t))$ 中的最大化操作依赖于对抗状态集 $\mathcal{B}(s)$ 的定义。当前实现基于 $L_\infty$ 约束的凸松弛近似，若扰动模型变更（如语义扰动或自然分布偏移），正则化项的计算方式和理论保证均需重新推导。

4. **与对抗训练的互补性未探索**：TDRT 和对抗训练分别从策略平滑和鲁棒优化的角度提升鲁棒性，两者在机理上可能互补。本文未探索将 TDRT 的时间折扣正则化与 ATLA 的对抗训练框架结合的混合防御方案。

### 开放问题

基于上述局限，以下开放问题值得后续工作关注：

1. **认证防御的扩展**：能否将基于区间传播或随机平滑的认证防御框架扩展到行为目标攻击场景，为 TDRT 类方法提供形式化的行为偏离上界？这需要定义行为偏离的度量空间（如策略输出的 Wasserstein 距离），并推导该度量在状态扰动下的传播规律。

2. **高维感知输入的鲁棒攻击**：在图像等原始感知输入下，如何设计不依赖白盒访问的有效行为模仿攻击？可能的路径包括：(a) 利用表示学习将高维输入映射到低维隐空间，在隐空间中训练对抗策略；(b) 采用基于模型的模仿学习，通过学习环境动态模型来增强判别器信号的密度。

3. **自适应正则化调度**：能否通过元学习或贝叶斯优化自动为每个任务确定最优的 $\lambda$ 和时间折扣衰减策略？考虑到 $\lambda$ 的最优值与任务动力学复杂度、目标策略与原始策略的差异度等因素相关，一个可能的方案是训练一个超网络根据任务嵌入预测 $\lambda$。

4. **初始状态分布的影响**：Theorem 6.1 中的上界涉及初始状态分布 $d_\pi^t$，这意味着攻击成功率的方差可能部分源于初始状态的随机性。如何定量刻画初始状态分布对攻击收益方差的影响，并将其用于自适应攻击预算分配或防御优先级排序？

5. **多模态扰动的泛化**：时间折扣正则化在非 $L_\infty$ 扰动（如 $L_2$ 约束、自然分布偏移、语义扰动）下是否仍保持理论优势？Theorem 6.1 的推导依赖于 KL 散度的局部展开，其精度在扰动类型变更时可能退化，需要针对不同扰动模型重新推导敏感性上界。



## 原文 PDF

![[paperPDFs/ICLR_2026/Robust_Deep_Reinforcement_Learning_against_Adversarial_Behavior_Manipulation.pdf]]
