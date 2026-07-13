---
title: "MIRA: Memory-Integrated Reinforcement Learning Agent with Limited LLM Guidance"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MIRA_Memory_Integrated_Reinforcement_Learning_Agent_with_Limited_LLM_Guidance.pdf
project_link: https://narjesno.github.io/MIRA/
code_link: null
openreview_forum_id: oWagByDNPc
aliases:
- MIRA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "从记忆图中派生的效用信号（utility signal）通过加权增强优势估计，补偿早期评论家梯度的不足，从而驱动策略朝着任务目标方向探索。"
primary_logic: "LLM可以为任务提供结构化的先验知识（子目标分解、轨迹片段），通过构建持久化的记忆图将其固定下来，并转化为可衰减的效用塑造信号，从而在不改变长期收敛性质的前提下大幅加速稀疏奖励环境下的早期学习。"
claims:
- "MIRA在所有四个MiniGrid/BabyAI任务上均优于PPO和分层强化学习基线，达到更高的渐进回报和成功率，同时仅需很少的LLM查询（不超过十个离线提示加上少量在线查询）。"
- "MIRA在查询效率上显著高于LLM4Teach和LLM-RS，以更少的LLM查询获得相当的回报。"
- "效用塑造的优势估计在训练早期提供非零梯度，确保在优势函数近乎零时仍能进行有效的策略更新，理论证明在衰减权重下该更新保持PPO的收敛性。"
- "MiniGrid-DOORKEY 上 Mean Return (unseen seeds) = 0.898 ± 0.093"
---

# MIRA: Memory-Integrated Reinforcement Learning Agent with Limited LLM Guidance

> [!tip] 核心洞察
> LLM可以为任务提供结构化的先验知识（子目标分解、轨迹片段），通过构建持久化的记忆图将其固定下来，并转化为可衰减的效用塑造信号，从而在不改变长期收敛性质的前提下大幅加速稀疏奖励环境下的早期学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MIRA：结合有限LLM引导的记忆集成强化学习智能体 |
| 英文题名 | MIRA: Memory-Integrated Reinforcement Learning Agent with Limited LLM Guidance |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oWagByDNPc) · [Project](https://narjesno.github.io/MIRA/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MIRA |
| Dataset | MiniGrid-DOORKEY, MiniGrid-LAVACROSSING, MiniGrid-REDBLUEDOOR, MiniGrid-REDBALL |

> [!tip] 效果简介
> - MiniGrid-DOORKEY 上，Mean Return (unseen seeds) 为 0.898 ± 0.093，对比 0.018 ± 0.016 (Baseline RL)，变化 +0.880。
> - MiniGrid-LAVACROSSING 上，Mean Return (unseen seeds) 为 0.855 ± 0.132，对比 0.012 ± 0.027 (Baseline RL)，变化 +0.843。
> - MiniGrid-REDBLUEDOOR 上，Success Rate (unseen seeds) 为 0.944 ± 0.020，对比 0.036 ± 0.043 (Baseline RL)，变化 +0.908。

## 概要

**核心问题**：在稀疏奖励或延迟反馈的强化学习环境中，评论家（critic）早期输出的价值估计近乎均匀，导致优势函数无法提供有意义的更新梯度，使策略探索效率极低、收敛缓慢。

**核心方法**：MIRA（Memory-Integrated Reinforcement Learning Agent）通过构建一个**持久化的演化记忆图**，将大语言模型（LLM）提供的结构化先验知识（子目标分解、轨迹片段）固定下来，并从中派生**效用信号**（utility signal），以加权方式增强优势估计。该效用项在训练早期补偿评论家梯度的不足，驱动策略朝任务目标方向探索，同时其权重随时间衰减至零，确保长期收敛性质与标准PPO一致。

**方法定位**：MIRA属于**LLM引导的强化学习**范式，但与现有工作有本质区别——它不依赖频繁的在线LLM查询来实时生成奖励或策略。相反，MIRA用极少的离线提示（不超过十个）初始化记忆图，仅辅以少量经筛选的在线查询进行补充，将LLM的知识转化为可衰减的塑造信号，而非直接干预奖励函数或策略蒸馏。这一设计使其在查询效率上显著优于**LLM4Teach**（Zhou et al., 2023）和**LLM-RS**（Bhambri et al., 2024）等方法。

**主要结果**：
- 在MiniGrid的四项稀疏奖励任务（DOORKEY、LAVACROSSING、REDBLUEDOOR、REDBALL）上，MIRA在所有指标上均显著优于标准PPO和分层强化学习基线（HRL），在未见种子上达到0.898–0.956的成功率或平均回报，而基线RL在多数任务上几乎无法学习（如DOORKEY回报仅0.018）。
- MIRA以远少于LLM4Teach和LLM-RS的LLM查询次数，取得了相当的渐进回报和成功率，查询效率优势显著。
- 消融实验证实：效用塑造使评论家产生有意义贡献的迭代提前约50轮，回报提升约2.5倍；更多在线查询预算加速收敛；策略成熟后对在线LLM依赖降低，即使切换为不可靠LLM并禁用筛选，性能仍保持稳定。

**局限性**：当前验证限于离散动作空间的小规模网格环境，扩展到连续控制和高维视觉输入仍需探索；记忆图初始化依赖LLM输出质量，误导性先验可能延缓收敛。

**稀疏奖励与延迟反馈：强化学习的核心瓶颈**

强化学习（Reinforcement Learning, RL）在复杂序列决策任务中面临一个根本性困境：当环境仅在任务完成时提供奖励（稀疏奖励），或奖励在时间上严重滞后（延迟反馈），智能体在训练早期几乎无法获得有意义的梯度信号。此时，评论家（critic）输出的价值估计近似均匀，导致优势函数 $A_t$ 趋近于零，策略更新近乎随机游走。这一现象在长时序、部分可观测的导航与操作任务中尤为突出——智能体可能在数百万步的无效探索后才偶然发现目标，收敛效率极低。

**LLM辅助强化学习的现有路径与缺口**

为缓解上述瓶颈，近年研究开始引入大型语言模型（Large Language Models, LLMs）为RL提供先验知识。现有方法大致可分为三类：

- **分层强化学习（HRL）**：利用LLM作为高层策略选择子目标，如Matthews et al. (2022)的工作。尽管提供了结构化引导，但LLM需持续在线决策，查询成本高，且高层策略的错误会逐层累积。
- **势能奖励塑造**：通过实时LLM查询生成势能函数，如**LLM-RS**（Bhambri et al., 2024）。然而，频繁的在线查询不仅引入推理延迟，还使训练过程高度依赖LLM的即时可靠性。
- **知识蒸馏**：以LLM作为教师策略进行监督，如**LLM4Teach**（Zhou et al., 2023）。该方法虽能加速早期学习，但蒸馏过程需要大量教师查询，且教师策略的偏差会固化到学生策略中。

上述方法的共同缺口在于：**LLM的参与方式过于“重”，要么作为持续决策者，要么作为密集监督源，既增加了查询成本，又使系统对LLM质量高度敏感**。更重要的是，它们未能将LLM提供的一次性结构知识（如子目标分解、可行轨迹片段）持久化并转化为可衰减的引导信号——一旦LLM退出，引导也随之消失。

**核心动机：从“LLM主导”到“LLM辅助”的范式转换**

MIRA的设计动机源于一个关键洞察：**LLM的真正价值不在于替代RL的探索过程，而在于为稀疏奖励环境注入结构化的先验锚点**。这些锚点——包括任务分解、典型轨迹模式、子目标间的依赖关系——可以通过持久化的记忆结构固定下来，并在训练早期提供有偏向的探索方向，随后逐步让位于智能体自身积累的经验。

这一范式转换意味着：LLM从“驾驶员”变为“导航员”，其建议被吸收进一个演化的记忆图中，转化为可衰减的效用信号（utility signal）。该信号通过加权增强优势估计，在不改变底层奖励函数的前提下补偿早期评论家梯度的不足，且理论上保证最终收敛到标准策略梯度方法的解。由此，MIRA在保持极低LLM查询预算（不超过十个离线提示加上少量在线查询）的同时，实现了与依赖密集LLM监督方法相当的加速效果。

## 核心方法与创新机理

MIRA 的核心创新在于**将 LLM 的结构化先验知识转化为一种可衰减的效用塑造信号**，通过持久化的记忆图（Memory Graph）补偿稀疏奖励环境下评论家（Critic）早期训练的梯度不足，从而在不改变长期收敛性质的前提下大幅加速早期探索与学习。

### 问题瓶颈：稀疏奖励下的评论家失效

在稀疏奖励或延迟反馈环境中，强化学习的评论家网络在训练早期通常输出近似均匀的价值估计。这使得标准优势函数 $A_t$ 趋近于零，无法为策略更新提供有意义的梯度信号，导致智能体陷入低效的随机探索，收敛极其缓慢。这是 PPO 等标准方法在 MiniGrid-DOORKEY、LAVACROSSING 等任务上几乎无法学习的根本原因——**Baseline RL 在未见种子上平均回报仅为 0.018 和 0.012**（Table 2）。

### 关键机制：效用塑造的优势估计

MIRA 的核心操作在于**替换了标准 PPO 的优势估计**——这是方法谱系中唯一的根本性“changed slot”。具体而言，MIRA 引入了一个塑造后的优势函数：

$$\tilde{A}_t = \eta_t A_t + \xi_t U_t, \quad 0 < \eta_t \le 1, \quad \xi_t \le \delta \eta_t, \quad \delta \in [0, 1), \quad \lim_{t \to \infty} \eta_t = 1, \quad \lim_{t \to \infty} \xi_t = 0$$

其中 $U_t$ 是从记忆图中导出的**效用信号**，$\eta_t$ 和 $\xi_t$ 是随时间衰减的权重。这一设计的精妙之处在于：

- **早期补偿**：当评论家尚未成熟、$A_t$ 近似为零时，$\xi_t U_t$ 项提供了非零的、方向正确的梯度，将策略推向任务目标方向。
- **渐进退化**：随着训练推进，$\xi_t \to 0$ 且 $\eta_t \to 1$，使得 $\tilde{A}_t \to A_t$，最终完全退化为标准 PPO 更新，保证了**长期收敛性质不变**。理论证明表明，在标准随机逼近条件下，评论家误差保持在真实值的 $O(\delta_t)$ 邻域内（Theorem 1）。

消融实验直接验证了这一机制的有效性：在适当的效用塑造权重下，效用项使评论家开始产生有意义贡献的迭代**提前约 50 轮**，回报**提升约 2.5 倍**（Figure 15）。

### 效用信号的来源：LLM 先验与记忆图

效用信号 $U_t$ 并非凭空产生，而是从智能体维护的**演化记忆图**中计算得出：

$$U_t \doteq c_m \cdot \hat{r}_m \cdot \rho(\mathbf{g}_{\mathrm{p}}, \zeta_m) \cdot \textstyle \int \big((o_t, a_t), (o_{t'}, a_{t'})_{\tau_m} \big)$$

该信号综合了四个因素：记忆节点的置信度 $c_m$、估计奖励 $\hat{r}_m$、目标对齐因子 $\rho$，以及当前轨迹与存储轨迹的相似度。记忆图的节点包括轨迹片段、子目标分解等决策相关信息，这些信息**由离线 LLM 输出初始化，并由筛选后的非频繁在线查询持续补充**（Sections 2.1-2.3）。

与 LLM4Teach（Zhou et al., 2023）和 LLM-RS（Bhambri et al., 2024）等需要频繁在线 LLM 查询的方法不同，MIRA 将 LLM 知识**固定为持久化的图结构**，仅在必要时通过筛选单元（Screening Unit）注入高置信度的在线建议。这使得 MIRA 在查询效率上显著优于前述方法——以更少的 LLM 查询获得相当的回报（Figure 6），同时在所有四个 MiniGrid/BabyAI 任务上均优于 PPO 和 HRL 基线（Figure 5）。

### 与基线方法的关键差异

| 方法 | 外部知识集成方式 | 探索引导信号 | 优势估计 |
|------|-----------------|-------------|---------|
| **PPO** (Schulman et al., 2017a) | 无 | 随机探索 | 标准 $A_t$ |
| **HRL** (Matthews et al., 2022) | 预训练 LLM 选项策略 | 分层子目标 | 标准 $A_t$ |
| **LLM-RS** (Bhambri et al., 2024) | 实时 LLM 查询生成势能奖励 | 势能塑造 | 标准 $A_t$（奖励被修改） |
| **LLM4Teach** (Zhou et al., 2023) | LLM 作为策略教师进行知识蒸馏 | 教师引导 | 标准 $A_t$ |
| **MIRA** | 离线 LLM 初始化 + 筛选后的非频繁在线查询 → 演化记忆图 | 记忆图导出的效用信号 $U_t$ | 塑造 $\tilde{A}_t = \eta_t A_t + \xi_t U_t$ |

MIRA 的独特之处在于：**它不修改环境奖励函数**（区别于 LLM-RS 的势能奖励塑造），**不依赖频繁的在线 LLM 监督**（区别于 LLM4Teach 的持续蒸馏），而是通过记忆图将 LLM 先验转化为可衰减的、作用于优势估计层面的软引导信号。这种设计既保留了 PPO 的收敛保证，又在稀疏奖励环境中提供了关键的早期探索梯度。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/001_Figure_1.jpg]]
*Figure 1: Offline priors and online LLM suggestions are filtered by a screening unit before being incorporated into the memory graph as healthy grafts. MIRA agent acts under partial observations, interacting with the environment. A utility module evaluates trajectory rollouts against the evolving memory graph, producing a utility signal that shapes advantage estimation and policy updates*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/002_Figure_2.jpg]]
*Figure 2: MIRA’s evolving memory graph. Trajectory segments $\tau _ { j }$ are grouped under subgoal nodes $\kappa _ { \ell }$ . Subgoals can be shared across multiple final goals, enabling reuse of common behaviors

MIRA 的整体框架围绕一个核心思想构建：**将大语言模型（LLM）提供的结构化先验知识转化为持久化的记忆图，并从中导出可衰减的效用信号来塑造强化学习的策略更新**。该框架由四个关键模块串联而成，形成一条从外部知识注入到策略优化的完整信息流。

### 框架总览

图 1 展示了 MIRA 的系统架构。整个 pipeline 的信息流向如下：

1. **离线 LLM 先验**与**在线 LLM 建议**分别进入系统。离线先验在训练开始前一次性获取（通常不超过十个提示），提供任务的结构化分解（子目标、轨迹片段）；在线建议则在训练过程中按需触发，频率极低。
2. 所有 LLM 输出首先经过**筛选单元（Screening Unit）**，通过置信度评估过滤不可靠的建议，仅将“健康嫁接”（Healthy Grafts）注入记忆图。
3. **记忆图（Memory Graph）**作为持久化存储，将 LLM 先验与智能体自身的高回报经验共同组织为可演化的图结构。
4. **效用计算器（Utility Computer）**在每个时间步将当前轨迹与记忆图进行匹配，计算出状态-动作对的效用信号 $U_t$。
5. **塑造 PPO 更新器（Shaped PPO Updater）**将效用信号加权注入优势估计，得到塑造后的优势 $\tilde{A}_t$，用于策略和值函数的更新。权重随时间衰减，确保训练末期退化为标准 PPO。

```
离线LLM先验 ──┐
              ├──► 筛选单元 ──► 记忆图 ──► 效用计算器 ──► 塑造PPO更新器 ──► 策略更新
在线LLM建议 ──┘                                      ▲
                                                     │
                                              智能体经验（轨迹回滚）
```

### 模块职责与交互

#### 记忆图（Memory Graph）

记忆图是框架的核心数据结构，定义为：

$$\mathcal{G} = \Big\{ \big( (o, a)_{\tau_j}, \zeta_j, \hat{r}_j \big)_{c_j} \Big\}_{j=1}^{N} \cup \big\{ \kappa_\ell \big\}_{\ell=1}^{L} \cup \big\{ g_\mathrm{s} \big\}$$

该图包含三类节点（图 2）：
- **轨迹节点**：存储观察-动作序列片段 $(o, a)_{\tau_j}$，附带目标项 $\zeta_j$、估计奖励 $\hat{r}_j$ 和置信度 $c_j$。
- **子目标节点** $\kappa_\ell$：由 LLM 分解的任务子目标，轨迹节点按层级关系挂载其下。
- **目标节点** $g_\mathrm{s}$：任务的最终目标。

图结构支持子目标跨任务复用——同一子目标节点可被多个最终目标共享，使得通用行为（如“开门”、“导航到物体”）可在不同任务间迁移。

记忆图在训练过程中持续演化：智能体的高回报轨迹片段被嫁接（graft）到图中，而长期未被访问的节点则被剪枝移除。每个节点维护一个访问计数器，当计数器在固定窗口内未变化时，该节点被清除。

#### 筛选单元（Screening Unit）

筛选单元负责评估在线 LLM 输出的可靠性，防止低质量建议污染记忆图。当 token 级别似然可用时，置信度计算为几何平均概率的指数：

$$\exp\left(\frac{1}{L}\sum \log p_i\right)$$

当似然不可用或不完整时，采用多次采样的一致性作为替代置信度估计。只有置信度超过预设阈值的在线建议才会被接受并嫁接进记忆图。消融实验（图 14）表明，阈值选择不影响最终收敛性能，仅调节早期探索广度与中期提升速度的权衡。

#### 效用计算器（Utility Computer）

效用计算器在每个时间步 $t$ 将当前状态-动作对 $(o_t, a_t)$ 与记忆图中的轨迹节点进行匹配，计算效用信号：

$$U_t \doteq c_m \cdot \hat{r}_m \cdot \rho(\mathbf{g}_\mathrm{p}, \zeta_m) \cdot \textstyle \int \big( (o_t, a_t), (o_{t'}, a_{t'})_{\tau_m} \big)$$

效用由四个因子乘积构成：
- **置信度** $c_m$：匹配节点的可靠性权重。
- **估计奖励** $\hat{r}_m$：该轨迹片段的历史回报估计。
- **目标对齐因子** $\rho$：当前策略目标 $\mathbf{g}_\mathrm{p}$ 与节点目标项 $\zeta_m$ 的匹配程度。
- **轨迹相似度** $\int$：当前行为与存储轨迹的相似性度量。

该信号的核心作用是：当评论家（critic）在早期训练中输出近似均匀的价值估计、导致标准优势 $A_t$ 近乎为零时，$U_t$ 提供非零的引导梯度，驱动策略朝着与记忆图中成功轨迹相似的方向探索。

#### 塑造 PPO 更新器（Shaped PPO Updater）

更新器将效用信号以加权方式注入优势估计，定义塑造优势：

$$\tilde{A}_t = \eta_t A_t + \xi_t U_t, \quad 0 < \eta_t \le 1, ~ \xi_t \le \delta \eta_t, ~ \delta \in [0, 1), ~ \lim_{t \to \infty} \eta_t = 1, ~ \lim_{t \to \infty} \xi_t = 0$$

其中 $\eta_t$ 和 $\xi_t$ 是随时间衰减的权重，塑造比率 $\delta_t = \xi_t / \eta_t$ 随训练进行而递减（图 4 右）。策略更新使用塑造后的 PPO 代理目标：

$$\mathcal{L}^\mathrm{shaped}(\pi_\theta) = \mathbb{E}\left[ \min(r_t, 1 \pm \varepsilon_k) \tilde{A}_t \right]$$

该设计的关键性质是：当 $t \to \infty$ 时，$\eta_t \to 1$ 且 $\xi_t \to 0$，塑造优势退化为标准优势，保证 MIRA 最终收敛到与标准 PPO 相同的策略。定理 1 证明，在标准随机近似条件下，该衰减机制使评论家误差保持在真实值的 $O(\delta_t)$ 邻域内。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 触发时机 |
|------|------|------|----------|
| 离线 LLM 查询 | 任务描述提示 | 子目标分解、轨迹片段 | 训练开始前，一次性 |
| 在线 LLM 查询 | 当前观察与历史 | 行动计划或控制信号 | 训练中，按需低频触发 |
| 筛选单元 | LLM 输出 | 健康嫁接节点 | 每次 LLM 查询后 |
| 记忆图更新 | 筛选后的嫁接 + 智能体高回报轨迹 | 演化后的图结构 | 持续进行 |
| 效用计算 | 当前 $(o_t, a_t)$ + 记忆图 | 效用信号 $U_t$ | 每个时间步 |
| 塑造 PPO 更新 | $A_t, U_t$ + 衰减权重 | 策略和价值网络参数更新 | 每个 rollout 批次 |

整个框架的查询效率极高：所有主要实验结果（图 5、表 2-3）仅使用不超过十个离线提示构建记忆图，外加少量在线查询，即实现了对标准 PPO 和分层强化学习基线的显著超越，并达到与需要频繁 LLM 监督的方法（如 LLM4Teach）相当的渐进性能。

MIRA 的核心架构由四个功能模块构成，它们协同工作，将 LLM 的结构化先验知识转化为可衰减的探索引导信号，最终注入标准 PPO 的优势估计中。下面逐一介绍各模块及其对应的关键公式。

### 记忆图 (Memory Graph)

记忆图是 MIRA 的核心数据结构，用于持久化存储从 LLM 先验和智能体经验中提取的决策相关信息。它是一个动态演化的图结构，其形式化定义为：

$$
\mathcal { G } = \Big \{ \big ( ( o , a ) _ { \tau _ { j } } , \zeta _ { j } , \hat { r } _ { j } \big ) _ { c _ { j } } \Big \} _ { j = 1 } ^ { N } \cup \big \{ \kappa _ { \ell } \big \} _ { \ell = 1 } ^ { L } \cup \big \{ g _ { \mathrm { s } } \big \}
$$

其中各符号的含义如下：
- $(o, a)_{\tau_j}$：轨迹片段 $\tau_j$ 中的观察-动作序列，代表智能体在执行任务时的一段有用行为。
- $\zeta_j$：该轨迹片段对应的目标项，用于与当前任务目标进行对齐匹配。
- $\hat{r}_j$：LLM 为该轨迹片段估计的奖励值，反映其预期效用。
- $c_j$：该轨迹节点的置信度，来自 LLM 输出的概率评估或多次采样一致性检验。
- $\kappa_\ell$：子目标节点，由 LLM 提供的任务分解产生，轨迹节点按层级关系挂载到对应的子目标下。
- $g_\mathrm{s}$：最终目标节点，多个子目标可共享于同一目标，实现通用行为的复用。

记忆图并非静态结构。它通过筛选单元（Screening Unit）持续接收经过置信度过滤的在线 LLM 输出，将可靠的建议作为新节点“嫁接”入图中；同时，长期未被访问的节点会被自动剪枝，以控制图规模并保持信息的新鲜度。

### 效用计算器 (Utility Computer)

效用计算器负责从当前轨迹与记忆图的匹配中，为每个状态-动作对 $(o_t, a_t)$ 计算一个标量效用信号 $U_t$。该信号衡量当前行为与记忆图中存储的有用轨迹片段的相似程度，其计算公式为：

$$
U _ { t } \doteq c _ { m } \cdot \hat { r } _ { m } \cdot \rho ( { \boldsymbol { \mathrm { g } } } _ { \mathrm { p } } , \zeta _ { m } ) \cdot \boldsymbol { \mathrm { \textstyle \int } } \big ( ( o _ { t } , a _ { t } ) , ( o _ { t ^ { \prime } } , a _ { t ^ { \prime } } ) _ { \tau _ { m } } \big )
$$

效用 $U_t$ 是四个因子的乘积：
- **置信度 $c_m$**：记忆节点 $m$ 的可靠性权重，来自 LLM 输出的 token 级概率（几何平均）或多次采样的一致性得分。当 token 概率可用时，置信度定义为 $\exp(\frac{1}{L}\sum \log p_i)$。
- **估计奖励 $\hat{r}_m$**：LLM 为该轨迹片段预估的奖励值。
- **目标对齐因子 $\rho(\mathbf{g}_\mathrm{p}, \zeta_m)$**：衡量当前任务目标 $\mathbf{g}_\mathrm{p}$ 与记忆节点目标项 $\zeta_m$ 的匹配程度，确保效用信号与当前任务相关。
- **轨迹相似度 $\textstyle \int$**：计算当前状态-动作对与记忆节点中存储的轨迹片段之间的相似性，鼓励策略产生与已知有用行为接近的动作。

### 塑造 PPO 更新器 (Shaped PPO Updater)

塑造 PPO 更新器是 MIRA 将效用信号注入强化学习训练的关键环节。它不改变环境奖励函数，而是通过加权组合的方式增强标准 PPO 的优势估计，定义塑造后的优势函数为：

$$
\tilde { A } _ { t } = \eta _ { t } A _ { t } + \xi _ { t } U _ { t }
$$

其中：
- $A_t$：标准 PPO 的优势估计，由评论家（critic）输出。
- $U_t$：从记忆图导出的效用信号。
- $\eta_t$：标准优势的权重，满足 $0 < \eta_t \le 1$，且 $\lim_{t \to \infty} \eta_t = 1$。
- $\xi_t$：效用项的权重，满足 $\xi_t \le \delta \eta_t$，$\delta \in [0, 1)$，且 $\lim_{t \to \infty} \xi_t = 0$。

权重 $\eta_t$ 和 $\xi_t$ 随时间衰减，其比值 $\delta_t = \xi_t / \eta_t$ 在训练过程中单调递减。这一设计确保了：在训练早期，当评论家输出近乎均匀的价值估计、标准优势 $A_t$ 无法提供有意义的更新梯度时，效用项 $U_t$ 主导 $\tilde{A}_t$，为策略提供朝向任务目标的有偏探索梯度；随着训练推进，评论家逐渐准确，效用项的影响被衰减至零，$\tilde{A}_t$ 退化为标准优势 $A_t$，从而保持 PPO 的长期收敛性质。

使用塑造优势的策略更新采用标准的 PPO 裁剪代理目标：

$$
\mathcal { L } ^ { \mathrm { s h a p e d } } ( \pi _ { \theta } ) = \mathbb { E } \left[ \operatorname* { m i n } ( r _ { t } , 1 \pm \varepsilon _ { k } ) \tilde { A } _ { t } \right]
$$

其中 $r_t$ 为新旧策略的概率比，$\varepsilon_k$ 为裁剪阈值。该目标函数仅将标准优势替换为塑造优势 $\tilde{A}_t$，其余 PPO 机制（裁剪、信任区域）保持不变。

### 筛选单元 (Screening Unit)

筛选单元位于 LLM 输出与记忆图之间，负责过滤不可靠的在线 LLM 建议。当 LLM 提供 token 级概率时，筛选单元计算输出的几何平均概率作为置信度；当概率不可用时，则通过多次采样的一致性（如多数投票）来估计可靠性。只有置信度超过预设阈值的建议才会被“嫁接”为记忆图的新节点。消融实验表明，筛选阈值的选择不影响最终收敛性能，仅调节早期探索广度与中期提升速度之间的权衡（Figure 14）。

## 实验与关键发现

### 核心瓶颈与因果机制

MIRA的设计动机源于稀疏奖励环境下强化学习的一个关键瓶颈：在训练早期，评论家（critic）网络输出近似均匀的价值估计，导致优势函数 $A_t$ 无法提供有意义的更新梯度，策略探索近乎随机，收敛极为缓慢。MIRA的因果调节旋钮是从记忆图中派生的**效用信号** $U_t$，通过加权增强优势估计 $\tilde{A}_t = \eta_t A_t + \xi_t U_t$，在 $A_t \approx 0$ 的早期阶段提供非零的探索引导梯度，从而驱动策略朝任务目标方向前进。随着训练推进，权重 $\eta_t \to 1$、$\xi_t \to 0$，塑造项逐渐退化为标准PPO，确保不改变长期收敛性质。

### 主要结果

MIRA在四个MiniGrid/BabyAI任务上进行了评估，所有方法使用相同的网络架构、PPO超参数和rollout设置以保证公平对比（Section 3.2），实验在多个随机种子下重复进行，结果以均值±标准差报告。

**与RL基线的对比。** 在稀疏奖励任务上，MIRA展现出对标准PPO的压倒性优势。如 Table 2 所示，在DOORKEY环境未见种子上，MIRA的平均回报达到 $0.898 \pm 0.093$，而Baseline RL仅为 $0.018 \pm 0.016$，提升幅度达 $+0.880$；在LAVACROSSING上，MIRA为 $0.855 \pm 0.132$，基线为 $0.012 \pm 0.027$，提升 $+0.843$。成功率方面（Table 3），REDBLUEDOOR上MIRA达到 $0.944 \pm 0.020$，基线仅 $0.036 \pm 0.043$；REDBALL上MIRA为 $0.956 \pm 0.036$，基线为 $0.539 \pm 0.064$。这些结果表明，在标准RL几乎完全失效的稀疏奖励场景中，MIRA的记忆引导机制能可靠地驱动策略学习。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/020_Table_2.jpg]]
*Table 2: Mean return on unseen seeds across MiniGrid environments. MIRA achieves high and stable success, comparable to LLM4Teach, despite requiring substantially fewer LLM queries*

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/021_Table_3.jpg]]
*Table 3: Success rate on unseen seeds across MiniGrid environments. MIRA achieves consistently high success rates, matching LLM4Teach while requiring fewer queries, and outperforming baseline and HRL methods*

**与LLM基线的对比。** 在查询效率上，MIRA显著优于需要频繁在线LLM查询的方法。Figure 6 显示，MIRA以远少于**LLM4Teach**（Zhou et al., 2023）和**LLM-RS**（Bhambri et al., 2024）的LLM查询次数，获得了相当的回报水平。Table 2和Table 3进一步表明，MIRA在未见种子上的平均回报和成功率与LLM4Teach相当（例如REDBLUEDOOR上MIRA成功率 $0.911$ vs LLM4Teach $0.901$），但所需的LLM查询预算极少——不超过十个离线提示加上少量在线查询。Welch's t-test（Table 4）显示MIRA与LLM4Teach在所有任务上的差异均不具统计显著性（$p > 0.05$），证实MIRA以更低的LLM依赖达到了同等性能。

**FrozenLake验证。** 在经典的FrozenLake环境中（Figure 4），MIRA的两个变体均在早期学习中显著优于PPO，而PPO最终达到了相当的渐近回报。右侧子图展示了塑造项 $\eta_t$、$\xi_t$ 及比值 $\delta_t = \xi_t/\eta_t$ 随训练的演化：$\delta_t$ 持续衰减，确保策略更新最终收敛到标准PPO。Figure 15进一步量化了塑造权重对早期学习动态的影响：在适当的 $\xi$ 值下，效用项使评论家产生有意义贡献的迭代提前约50轮，回报提升约2.5倍。

### 消融研究

Figure 7 从三个维度对MIRA的关键设计进行了消融分析。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/009_Figure_7.jpg]]
*Figure 7: Ablation Studies. Query frequency (left): Agents share the same offline memory but vary in online budgets. More queries accelerate learning, with high-budget agents achieving optimal returns more quickly. Unreliable LLM (middle): With identical offline memory, screening is disabled and queries are swapped from GPT-o4-mini to Gemini Pro only in the late phase. Performance remains stable in the late phase, indicating reduced dependence on online guidance once policy have matured. LLM models (right): Agents differ only in the LLM used for memory. Performance differences reflect divergent reasoning styles: Gemma3 induces inefficient checking, Claude favors cautious exploration, while Gemini Pro...*

**在线查询频率（Figure 7左）。** 在DOORKEY环境中，所有变体共享相同的离线记忆，仅在线LLM查询预算不同。结果显示，更多的在线查询显著加速收敛并提高最终回报：MIRA (large) 在SR90Return上达到0.851，最终回报0.91，而offline变体收敛较慢且最终回报略低（Table 1）。这验证了在线LLM引导在记忆图演化中的补充价值。

**不可靠LLM的鲁棒性（Figure 7中）。** 在训练后期将在线LLM从GPT-o4-mini切换为不可靠的Gemini Pro并禁用筛选单元后，性能保持稳定。这表明策略成熟后对在线LLM引导的依赖显著降低，记忆图中已积累的高质量经验足以支撑后续学习。

**不同LLM模型的影响（Figure 7右）。** 使用不同LLM（Gemma3、Claude、Gemini Pro、o4-mini）构建的记忆图导致显著不同的学习曲线。Gemini Pro和o4-mini最快达到高回报，Claude表现出谨慎的探索风格导致渐进增长，而Gemma3几乎无学习——其推理痕迹（Figure 11）显示该模型倾向于低效的检查行为。这说明LLM的推理质量直接影响记忆图的效用，进而决定早期探索效率。

**筛选阈值敏感性（Figure 14）。** 不同的筛选阈值不改变最终收敛性能，仅调整早期探索广度与中期提升速度的权衡：宽松阈值（$\tau \ge 2/4$）早期将更多候选节点纳入记忆图，产生更广泛的探索塑造但整体提升速率较慢；严格阈值（$\tau = 1$）延迟图增长，但一旦高置信度节点出现后产生更陡峭的中期增益。所有设置最终收敛到窄性能带。

**提示词鲁棒性（Figure 13）。** 在FrozenLake上使用原始提示与替代提示，MIRA的性能接近，表明方法对任务描述的自然变化具有稳定性。

### 失败模式与局限

尽管MIRA在稀疏奖励任务上表现优异，其有效性高度依赖离线LLM输出的质量。当LLM提供与环境动态不一致的误导性信息时（如Gemma3的案例），记忆图可能引导策略走向低效甚至错误的探索方向，导致收敛变慢或需要更多在线查询来纠正。此外，塑造项的超参数（$\eta_t$、$\xi_t$ 的衰减策略）需要针对具体任务进行调整以保持actor-critic训练的稳定性，这增加了实际部署的工程负担。当前研究仅限于离散动作空间的小规模基准，扩展到连续控制任务或高维视觉输入场景的可行性尚未验证。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_oWagByDNPc/figures/004_Figure_5.jpg]]
*Figure 5: Mean return (top) and success rate (bottom) across four MiniGrid and BabyAI tasks. MIRA consistently outperforms both baselines, achieving faster learning, higher asymptotic return, and greater success rates. These results are obtained with a small LLM budget, using fewer than ten offline prompts to build memory graphs plus infrequent online queries to guide exploration*

## 定位与知识库关联

### 方法定位：稀疏奖励下RL的LLM辅助探索

MIRA 处于**稀疏奖励强化学习**与**大语言模型辅助决策**的交叉地带。其核心设计动机源于一个被广泛观察但未充分解决的瓶颈：在延迟反馈或稀疏奖励环境中，评论家（critic）在训练早期输出近似均匀的价值估计，导致优势函数 $A_t \approx 0$，策略梯度近乎为零，探索陷入随机游走。MIRA 的因果调节旋钮是**从持久化记忆图中派生的效用信号 $U_t$**，通过加权注入优势估计 $\tilde{A}_t = \eta_t A_t + \xi_t U_t$，在 $A_t$ 失效的早期阶段提供有意义的更新方向，同时通过 $\eta_t \to 1, \xi_t \to 0$ 的退火机制保证最终收敛到标准PPO策略。

这一设计在方法谱系中占据了一个独特位置：它**不修改环境奖励函数**（区别于势能奖励塑造），**不依赖频繁在线LLM查询**（区别于LLM-RS和LLM4Teach），**不引入分层策略结构**（区别于HRL），而是通过一个**独立于策略训练的记忆图结构**将LLM的先验知识固化为可衰减的引导信号。

### 与基线方法的关系

**PPO**（Schulman et al., 2017）是MIRA的策略优化骨架。MIRA对PPO的唯一修改在于优势估计环节：将标准优势 $A_t$ 替换为塑造优势 $\tilde{A}_t$，并在代理目标中保持裁剪机制不变。当 $\xi_t \to 0$ 时，MIRA完全退化为标准PPO，因此MIRA可以视为PPO的一个**收敛保持扩展**（convergence-preserving extension），其理论保证由Theorem 1支撑——在标准随机近似条件下，塑造引入的critic误差保持在 $O(\delta_t)$ 邻域内，且 $\delta_t = \xi_t / \eta_t$ 随训练衰减。

**HRL**（Matthews et al., 2022）使用预训练LLM作为高层选项策略，本质上将LLM的推理能力直接嵌入决策循环。MIRA与之的关键区别在于**解耦了LLM推理和策略执行**：LLM输出仅用于构建和更新记忆图，而非实时控制。这使得MIRA在LLM不可靠或不可用时仍能运行——消融实验（Figure 7 middle）表明，在训练后期将LLM切换为不可靠模型（Gemini Pro）并禁用筛选后，性能保持稳定，验证了策略成熟后对在线LLM依赖的降低。

**LLM-RS**（Bhambri et al., 2024）通过实时LLM查询生成势能奖励塑造函数，每次查询直接修改环境奖励信号。MIRA与之相比有两个优势：（1）查询效率——MIRA仅需少量离线提示构建初始记忆图，加上非频繁的在线查询补充，而LLM-RS需要持续查询以维持塑造函数；（2）收敛安全性——势能塑造在理论上保证策略不变性，但实践中不准确的势能函数可能引入偏差；MIRA通过退火权重显式控制塑造项的影响衰减，最终完全依赖环境奖励。

**LLM4Teach**（Zhou et al., 2023）将LLM作为策略教师，通过知识蒸馏将LLM的决策能力迁移到RL策略中。在MiniGrid基准上，MIRA达到了与LLM4Teach相当的回报和成功率（Table 2, Table 3），Welch's t检验显示两者差异在 $\alpha=0.05$ 水平上不显著（Table 4），但MIRA所需的LLM查询量显著更少（Figure 6 right）。这表明**记忆图机制可以在不牺牲性能的前提下大幅降低LLM依赖成本**。

### 适用边界

MIRA的设计在以下条件下最为有效：

1. **任务具有可分解的结构**：LLM能够提供有意义的子目标分解和轨迹片段建议。当任务结构过于简单（LLM先验无信息增益）或过于复杂（LLM无法提供有效分解）时，记忆图的效用信号可能退化为噪声。消融实验中Gemma3几乎无学习（Figure 7 right）即说明LLM推理质量对初始记忆图构建至关重要。

2. **稀疏奖励或延迟反馈占主导**：MIRA的核心收益来自补偿早期critic的无效梯度。在密集奖励环境中，标准PPO本身即可快速收敛，塑造项的边际收益有限。FrozenLake实验（Figure 4 left）展示了这一模式：MIRA在早期显著加速，但PPO最终达到相当的渐进回报。

3. **离散动作空间**：当前MIRA的实现和验证均限于离散动作空间（MiniGrid, BabyAI, FrozenLake）。扩展到连续控制是一个自然但尚未探索的方向，需要重新设计效用计算中的轨迹相似度度量 $\int$ 以及记忆图中的动作表示。

4. **LLM输出可通过置信度筛选**：筛选单元依赖token概率或多次采样一致性来过滤不可靠输出。当LLM不提供token概率且生成一致性差时，筛选机制的有效性会下降。Figure 14显示筛选阈值影响早期探索广度与中期提升速度的权衡，但不影响最终收敛，表明该机制具有一定的容错性。

### 局限与开放问题

**当前局限**（来自论文明确讨论）：

- **离线LLM依赖**：MIRA依赖离线LLM输出来初始化记忆图。若LLM提供与环境动态不一致的误导性信息，可能导致收敛变慢或需要更多在线查询来纠正。这一风险在自定义环境（如DISTRACTED DOORKEY）中尤为突出，因为LLM对环境的理解完全来自提示词描述。
- **超参数敏感性**：塑造权重 $\eta_t, \xi_t$ 的退火调度需要针对具体任务调整，以保持actor-critic训练的稳定性。Figure 15显示 $\xi$ 值过小时效用项无法有效加速critic贡献，过大时可能引入偏差。
- **规模验证有限**：所有实验均在特定小规模基准（MiniGrid, BabyAI, FrozenLake）上进行，未在大规模高维场景（如Atari、Minecraft）下验证记忆图的可扩展性。

**开放问题**：

1. **连续控制扩展**：MIRA能否扩展到机器人操作等连续动作空间任务？这需要重新设计效用计算中的轨迹匹配机制，可能需要引入基于嵌入空间的相似度度量替代当前的离散匹配。

2. **高维视觉输入适应**：在完全基于像素输入的环境（如Atari游戏）中，记忆图中的观察表示和效用计算的相似度函数需如何调整？当前MiniGrid实验使用了卷积编码器（Figure 18），但观察空间仍相对结构化。

3. **自适应查询触发**：如何自动选择最优的LLM查询触发阈值和记忆图大小，以减少人工设计？当前筛选阈值和查询频率均需手动设定。

4. **多任务记忆复用**：记忆图的子目标共享机制（Figure 2）暗示了跨任务复用的可能性。能否将MIRA应用于多目标或多任务环境，实现通用的记忆图迁移？这需要研究不同任务间子目标表示的泛化能力。

5. **LLM推理质量与训练动态的交互**：消融实验（Figure 7 right）揭示了不同LLM的记忆导致显著不同的学习曲线，但这一现象的深层机制——LLM推理风格如何通过记忆图结构影响探索策略——尚需进一步分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/MIRA_Memory_Integrated_Reinforcement_Learning_Agent_with_Limited_LLM_Guidance.pdf]]
