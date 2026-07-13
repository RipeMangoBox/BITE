---
title: "Stronger-MAS: Multi-Agent Reinforcement Learning for Collaborative LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Stronger_MAS_Multi_Agent_Reinforcement_Learning_for_Collaborative_LLMs.pdf
project_link: null
code_link: https://github.com/pettingllms-ai/PettingLLMs
openreview_forum_id: IdF6JqXWzx
aliases:
- AGATWGRPO
- Stronger-MAS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用“按智能体和轮次分组”（Agent- and Turn-wise Grouping）与“树结构采样”（Tree-structured Sampling），确保每个比较组内的候选动作拥有相同的角色和对话历史，从而恢复GRPO的方差缩减效果。"
primary_logic: "通过将GRPO的组归一化从单智能体扩展到多智能体，并以树型分支采样维持有效的比较组，使MAS各角色通过在线RL习得专业化的协作策略，尤其适用于长程任务，能将准确率从14-47%提升至96-99.5%。"
claims:
- "在Sokoban（Qwen3-8B）上，MAS+AT-GRPO将准确率从单智能体基线9.0%提升至96.0%，相对增益+87%。"
- "移除稠密奖励后，AT-GRPO仅下降4%（Plan-Path），且稀疏奖励下的89.0%仍远超SA（12.0%）和MAS（71.0%）。"
- "交换训练好的角色专用策略导致性能崩溃（从96%降至6%），证实RL强化了角色专属策略。"
- "直接对MAS应用GRPO在CodeContests（8B）上从17.60降至10.30，验证了专用分组（AT-GRPO）的必要性。"
---

# Stronger-MAS: Multi-Agent Reinforcement Learning for Collaborative LLMs

> [!tip] 核心洞察
> 通过将GRPO的组归一化从单智能体扩展到多智能体，并以树型分支采样维持有效的比较组，使MAS各角色通过在线RL习得专业化的协作策略，尤其适用于长程任务，能将准确率从14-47%提升至96-99.5%。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Stronger-MAS：面向协作式大语言模型的多智能体强化学习 |
| 英文题名 | Stronger-MAS: Multi-Agent Reinforcement Learning for Collaborative LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IdF6JqXWzx) · [GitHub](https://github.com/pettingllms-ai/PettingLLMs) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AT-GRPO (Agent- and Turn-wise Grouped Relative Policy Optimization) |
| Dataset | Sudoku (4×4) – Qwen3-1.7B, Sokoban (6×6) – Qwen3-8B, Plan-Path (10×10) – Qwen3-1.7B, LiveCodeBench-v6 – Qwen3-8B |

> [!tip] 效果简介
> - Sudoku (4×4) – Qwen3-1.7B 上，Accuracy (%) 为 99.00，对比 7.00，变化 +92.00。
> - Sokoban (6×6) – Qwen3-8B 上，Accuracy (%) 为 96.00，对比 9.00，变化 +87.00。
> - Plan-Path (10×10) – Qwen3-1.7B 上，Accuracy (%) 为 96.00，对比 5.00，变化 +91.00。

## 概要

多智能体系统（MAS）通过角色分工与协作，有望突破单一大语言模型（LLM）在长程规划、推理等复杂任务中的能力边界。然而，现有方法面临两个关键瓶颈：其一，**单智能体强化学习（RL）缺乏跨角色协同**，在长程规划任务上准确率仅为14–47%；其二，**标准GRPO直接应用于MAS时**，由于各智能体在不同轮次接收的提示不同，无法形成同质比较组，导致优势估计方差大、训练不稳定，甚至出现性能倒退（如CodeContests上从17.6%降至10.3%）。

针对上述问题，本文提出 **Stronger-MAS** 框架及其核心算法 **AT-GRPO**（Agent- and Turn-wise Grouped Relative Policy Optimization）。核心思路是：**通过按智能体和轮次分组**，确保每个比较组内的候选动作共享相同的角色与对话历史，从而恢复GRPO的方差缩减效果；同时采用**树结构采样**，在每个决策点生成多个候选动作并贪心选择最优者执行，维持有效的比较组结构。在此基础上，AT-GRPO支持角色共享与角色专用两种策略优化模式，使各智能体通过在线RL习得专业化的协作策略。

实验结果表明，该方法在长程规划任务上实现了质的飞跃：**Sokoban 准确率从单智能体基线的9.0%提升至96.0%**，Plan-Path从5.0%提升至96.0%，Sudoku从7.0%提升至99.0%。在编码与数学推理任务上同样取得一致增益：LiveCodeBench-v6 Pass@1从22.8%提升至33.1%，AIME24准确率从18.3%提升至57.0%。消融实验进一步揭示：联合MAS环境进行RL训练至关重要（单独训练再组合仅达16%）；训练好的角色专用策略不可互换（交换后准确率从96%骤降至6%）；方法在移除稠密奖励后性能下降极小（≤4%），展现出对稀疏奖励的鲁棒性。



大语言模型（LLM）在推理与规划任务上已展现出显著能力，但单一LLM在面对长程规划、多步推理等复杂任务时仍存在明显瓶颈。近期研究表明，通过引入多智能体系统（MAS），让不同角色的LLM协同工作，可以有效提升任务完成质量。然而，现有MAS方案大多依赖提示工程或监督微调，缺乏在交互环境中通过在线强化学习（RL）持续优化协作策略的能力。

将RL引入MAS面临一个根本性障碍：**标准GRPO算法在MAS中失效**。GRPO（Group Relative Policy Optimization）通过在同一次提示的多条响应之间构建比较组来计算相对优势，从而降低优势估计方差。但在多智能体多轮交互场景中，不同智能体在不同轮次接收的提示各不相同——前置对话历史持续分叉，导致各候选动作的状态条件不再同质。这意味着标准GRPO的“按提示分组”策略在轮次 $t>0$ 时，每个比较组内仅剩单一候选动作（组大小退化为1），优势估计方差急剧放大，训练变得极不稳定。验证实验显示，直接将GRPO应用于MAS，在CodeContests（Qwen3-8B）上准确率反而从17.60%降至10.30%（**Table 2, MAS+GRPO行**）。

与此同时，单智能体RL在长程规划任务上的表现令人堪忧。在Sokoban和Plan-Path等需要多步前瞻与决策的任务上，单智能体GRPO的准确率仅为9.0%和5.0%（**Table 1, Table 2**），远未达到实用水平。这暴露了单一模型的固有限制：缺乏跨角色的校验、反思与规划分工，难以在复杂状态空间中有效探索。

现有面向LLM的多智能体RL框架亦存在覆盖缺口。**MAPORL**（Park et al., 2025）仅支持同质角色的辩论式工作流；**MARFT**（Liao et al., 2025）局限于单轮顺序交互；**CURE**（Wang et al., 2025a）虽引入Coder-Tester协同但强制所有角色共享同一策略。这些方法或缺乏多轮支持，或无法处理角色异质性，或跨域泛化能力有限（**Table 5**），尚未提供一套通用的、支持角色专用策略在线优化的MAS训练方案。

本文的核心动机正是填补这一空白：**设计一种适用于多智能体、多轮交互的GRPO变体，使MAS中的各角色能够通过在线RL习得专业化协作策略，同时构建可扩展的训练系统以支撑异构工作流的高效执行**。



## 核心方法与创新机理

Stronger-MAS 的核心创新在于将标准 GRPO（Group Relative Policy Optimization）从单智能体场景系统性地适配到多智能体协作训练中，解决了原方法在 MAS 环境下因同质性假设被打破而导致优势估计方差大、训练不稳定的根本瓶颈。该创新通过三个紧密耦合的技术组件实现，可统一表述为 **AT-GRPO（Agent- and Turn-wise Grouped Relative Policy Optimization）** 算法。

### 瓶颈定位：GRPO 在 MAS 中的失效机制

标准 GRPO 的核心机制是按提示（prompt）分组：对同一输入采样 $K$ 条响应，在组内计算相对优势以缩减方差。然而在 MAS 中，不同智能体在不同轮次接收的提示（包含角色指令和对话历史）必然不同，导致：

- **平行采样失效**：若沿完整轨迹平行采样，从第二回合起，每个状态仅对应一条采样轨迹，比较组大小退化为 1，优势估计完全失去方差缩减效果。
- **跨角色比较无意义**：不同角色的动作空间和语义完全不同（如 Planner 生成计划 vs. Executor 生成动作），将其放入同一比较组会引入系统性偏差。

直接对 MAS 应用 GRPO 的后果已被实验证实：在 CodeContests（Qwen3-8B）上，MAS+GRPO 的 Pass@1 从 17.60 降至 10.30，甚至低于未经训练的纯提示 MAS 基线（Table 2）。

### 核心创新点：三个 Changed Slots

AT-GRPO 通过以下三个关键设计，将 GRPO 的组相对优化范式完整迁移至 MAS 场景。

#### Changed Slot 1：优势比较分组方式

| 维度 | 基线（GRPO） | AT-GRPO |
|------|-------------|---------|
| 分组键 | 提示文本（同输入的多条响应） | `(环境ID, 智能体ID, 轮次)` 的哈希 |
| 组内条件 | 共享相同输入提示 | 共享相同角色身份和对话历史 |
| 效果 | 在 MAS 中组大小退化为 1 | 始终维持 $K$ 路候选的比较组 |

**因果机制**：通过 Agent- and Turn-wise Grouping，每个比较组内的 $K$ 个候选动作由同一智能体在同一轮次、面对相同历史状态时采样产生，满足 GRPO 组归一化的同质性前提。这直接恢复了优势估计的方差缩减效果，是训练稳定性的根本保障。

#### Changed Slot 2：采样策略

| 维度 | 基线（平行采样） | AT-GRPO（树结构采样） |
|------|-----------------|----------------------|
| 采样方式 | 每回合采样 1 条完整轨迹 | 每智能体每轮次采样 $K$ 个候选动作 |
| 轨迹结构 | 线性，无分支 | 树形，每节点 $K$ 分支 |
| 执行选择 | 直接执行唯一采样结果 | 贪心选择组内最高奖励动作执行 |

**因果机制**：树结构采样（Tree-structured Sampling）是 Agent- and Turn-wise Grouping 的必要前提——只有在每个决策点同时采样 $K$ 个候选，才能构建有效的比较组。贪心选择策略确保实际执行的轨迹始终沿当前最优方向前进，同时保留所有候选的经验用于策略更新。Figure 3 清晰对比了两种方案的差异：平行采样在 $t>0$ 时组大小退化为 1，而树采样始终保持 $K$ 路比较。

#### Changed Slot 3：信用分配

| 维度 | 基线 | AT-GRPO |
|------|------|---------|
| 奖励信号 | 单一团队奖励或简单局部奖励 | $r_{t,i} = \alpha r_{t}^{\mathrm{team}} + r_{t,i}^{\mathrm{loc}}$ |
| 混合权重 | — | $\alpha=1$（默认等权混合） |
| 局部奖励来源 | — | 角色特定的中间启发式信号 |

**因果机制**：Agent-wise Credit Assignment 为每个智能体提供角色专属的局部反馈，缓解了 MAS 中团队奖励稀疏且难以归因的经典问题。消融实验（Table 6）表明，即使完全移除稠密奖励（仅保留结局信号），AT-GRPO 在 Plan-Path 上仅从 96.0% 降至 89.0%，仍远超单智能体基线（12.0%）和未训练 MAS（71.0%），证明该方法对奖励稀疏性具有强鲁棒性。

#### Changed Slot 4：策略优化模式

| 维度 | 基线（角色共享） | AT-GRPO |
|------|-----------------|---------|
| 策略数量 | 所有角色共享 1 个策略 | 支持共享或每角色独立策略 |
| 训练批次 | 单一批次 | 按策略分配关系 $\sigma(i)$ 构建独立批次并行更新 |

**因果机制**：角色专用策略使每个智能体在其专属数据上深度专业化。交换实验（Table 4）提供了决定性证据：将训练好的 Planner 和 Executor 策略互换后，准确率从 96% 骤降至 6%，证实 RL 训练确实习得了不可互换的角色专属能力。但策略共享与专用的最优选择取决于任务特性：编码任务中角色专用平均高 3.05 点，而数学推理中共享策略有时更优。

### 方法谱系与知识库定位

AT-GRPO 在现有 LLM 多智能体训练框架中占据独特位置（Table 5 对比）：

- **vs. MAPORL**（Park et al., 2025）：后者仅支持同质角色辩论，AT-GRPO 支持异构角色协同。
- **vs. MARFT**（Liao et al., 2025）：后者为单轮顺序交互，AT-GRPO 支持多轮迭代。
- **vs. CURE**（Wang et al., 2025a）：后者仅支持共享策略的 Coder-Tester 协同，AT-GRPO 同时支持共享和专用策略。

AT-GRPO 是目前唯一同时满足**策略共享+专用双模式、多轮交互、异构角色、跨域适用**四个维度的框架。



![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/004_Figure_3.jpg]]
*Figure 3: Two sampling schemes. (a) In parallel sampling, trajectories are sampled but incomparable, leading to groups of size 1. (b) In tree sampling, branching at each turn forms a valid comparison group of size K*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/014_Table_5.jpg]]
*Table 5: Comparison of RL-based LLM multi-agent training frameworks*

Stronger-MAS 的整体框架围绕 **AT-GRPO**（Agent- and Turn-wise Grouped Relative Policy Optimization）算法构建，旨在解决标准 GRPO 直接应用于多智能体系统（MAS）时的根本性瓶颈：由于各智能体在不同轮次面对不同的提示与对话历史，无法形成同质比较组，导致优势估计方差大、训练不稳定。AT-GRPO 通过三个核心设计——**树结构采样**、**按智能体与轮次分组**、以及**智能体级信用分配**——将 GRPO 的组归一化机制从单智能体扩展到多智能体，使各角色通过在线 RL 习得专业化的协作策略。

### Pipeline 模块与数据流

整个训练系统采用**分布式架构**，由以下模块构成（参见 Figure 4）：

1. **RolloutWorker（每模型）**：每个 LLM 绑定一个 GPU 推理服务，负责在每轮为对应智能体生成 $K$ 个候选动作（树结构采样）。生成的动作及其概率比 $r(\theta) = \frac{\pi_{\theta}(o_i | q)}{\pi_{\theta_{old}}(o_i | q)}$ 被记录用于后续策略更新。

2. **CPU EnvWorker Pool**：维护沙盒环境实例池，执行 RolloutWorker 选定的动作并流式返回奖励。每个 EnvWorker 管理一个独立的沙盒实例，确保安全性、可复现性（固定随机种子、墙钟超时、I/O 配额、确定性工具调用）。

3. **Tree Sampling & Grouping Logic**：实现树结构采样和按 `(env, agent, turn)` 的分组逻辑。具体而言，对每个环境 $e$、每个智能体 $i$、每个轮次 $t$，使用轻量哈希函数生成唯一组键 $g$，确保组内 $K$ 个候选动作共享相同的角色身份和对话历史，从而恢复 GRPO 的有效比较组（Alg 1, lines 7-10）。

4. **Credit Assignment Module**：融合团队奖励与局部角色奖励，计算最终标量奖励 $r_{t,i} = \alpha r_{t}^{\mathrm{team}} + r_{t,i}^{\mathrm{loc}}$（$\alpha=1$），为每个智能体提供差异化的学习信号。

5. **Router**：根据策略分配关系 $\sigma(i)$ 将收集到的经验分发至对应模型的 UpdateWorker。若采用角色专用策略，不同角色的经验被路由到各自独立的更新队列；若采用角色共享策略，所有经验汇聚至同一 UpdateWorker。

6. **UpdateWorker（每模型）**：接收路由数据，在迷你批次 $B_m$ 上独立执行 PPO 式参数更新，损失函数为：
   $$\mathcal{L}(\theta^{(m)}) = -\mathbb{E}_{g \in B_{m}} \left[ \frac{1}{K} \sum_{c=1}^{K} \min \left( r_{g}^{(c,m)}(\theta^{(m)}) A_{g}^{(c)}, \mathrm{clip} \left( r_{g}^{(c,m)}(\theta^{(m)}), 1-\varepsilon, 1+\varepsilon \right) A_{g}^{(c)} \right) \right]$$
   其中 $A_{g}^{(c)}$ 为组内相对优势，$r_{g}^{(c,m)}$ 为策略 $m$ 的概率比。

### 输入输出流

- **输入**：环境状态观察 $o_i$ 与对话历史拼接形成的查询 $q$，分发给各角色的 RolloutWorker。
- **采样与执行**：每个智能体每轮采样 $K$ 个候选动作，计算组内优势后贪心选择最高奖励动作执行，环境返回奖励信号。
- **信用分配**：Credit Assignment Module 将团队奖励与角色局部奖励混合，生成每智能体的标量奖励。
- **路由与更新**：Router 按 $\sigma(i)$ 将经验分发至对应 UpdateWorker，各模型独立进行策略更新。
- **输出**：更新后的角色策略参数 $\theta^{(m)}$，支持角色共享（单策略）和角色专用（多策略）两种模式。

### 框架特性对比

Table 5 将 StrongerMAS 与现有基于 RL 的 LLM 多智能体训练框架进行了系统性对比。相较于 **MAPORL**（Park et al., 2025）、**MARFT**（Liao et al., 2025）、**CURE**（Wang et al., 2025a）等方法，StrongerMAS 在以下维度具有全面优势：同时支持策略共享与角色专用模式、支持顺序与并行两种执行模式、原生支持多轮交互与角色异质性、覆盖游戏/规划/编码/数学四个领域、提供通用训练框架。

### 关键设计决策的验证

**树结构采样的必要性**：平行采样完整轨迹会导致 $t>0$ 时比较组大小退化为 1，无法形成有效的相对优势估计。树结构采样通过每轮分支 $K$ 个候选动作，确保每个比较组始终包含 $K$ 个同质候选（Figure 3）。实验证据表明，直接对 MAS 应用标准 GRPO 在 CodeContests（8B）上从 17.60 降至 10.30（Table 2），验证了专用分组机制的必要性。

**联合训练的必要性**：单独训练各智能体再组合仅将准确率从 5% 提升至 16%，而联合训练可达 96%（Table 4），证实了在 MAS 环境中进行联合 RL 训练是不可或缺的。

**角色专用的有效性**：交换训练好的角色专用策略导致性能从 96% 骤降至 6%（Table 4），证实 RL 训练强化了角色的专业化分工，策略不可互换。



### 问题定义与GRPO基础

Stronger-MAS将多智能体协作建模为多轮、多角色的序列决策过程。每个回合$t$中，智能体$i$根据当前环境状态和对话历史生成动作$a_{t,i}$，环境返回团队奖励$r_t^{\mathrm{team}}$和局部角色奖励$r_{t,i}^{\mathrm{loc}}$。标准GRPO（Shao et al., 2024）的核心机制是通过组内相对优势估计来降低方差：

$$A_{g}(a_{t}^{(c)}) = \frac{R(a_{t}^{(c)}) - \mathrm{mean}(\{R(a_{t}^{(c)})\}_{c=1}^{K})}{F_{\mathrm{norm}}(\{R(a_{t}^{(c)})\}_{c=1}^{K})}$$

其中$R(a_{t}^{(c)})$为候选动作$c$的累积奖励，分母为组内奖励的标准差（或其它归一化因子）。该公式的关键前提是：**比较组内的所有候选动作必须来自相同的状态和提示上下文**，否则组均值作为基线将引入偏差。

### 核心瓶颈：标准GRPO在MAS中的失效

直接将GRPO应用于MAS时，上述前提被系统性地破坏。在平行采样方案中（Figure 3a），各智能体在不同轮次面对不同的对话历史和角色提示，导致：

- **组大小退化为1**：$t>0$时，每条轨迹分叉后的候选动作无法形成有效比较组，优势估计退化为零均值噪声。
- **方差放大**：跨角色、跨轮次的异构提示使得组内奖励分布不再反映同一决策点的相对质量，训练信号混乱。

实验证实了这一点：在CodeContests（8B）上，直接应用MAS+GRPO使Pass@1从17.60%降至10.30%（Table 2），低于未训练的MAS基线。

### AT-GRPO的三大核心模块

AT-GRPO通过三个协同模块恢复GRPO的方差缩减效果，并将其扩展到多智能体场景（Algorithm 1）。

#### 模块一：树结构采样（Tree-structured Sampling）

替代平行采样，在每个智能体的每个轮次进行$K$路分支采样（Figure 3b）：

1. 对智能体$i$在轮次$t$，从当前策略采样$K$个候选动作$\{a_{t,i}^{(c)}\}_{c=1}^{K}$。
2. 环境执行每个候选动作，获得对应奖励$\{R(a_{t,i}^{(c)})\}_{c=1}^{K}$。
3. **贪心选择**奖励最高的候选动作作为实际执行动作，继续展开轨迹。

这一设计确保每个决策点都自然形成大小为$K$的候选组，且组内所有候选共享相同的角色身份和对话前缀。

#### 模块二：按智能体和轮次分组（Agent- and Turn-wise Grouping）

分组逻辑通过哈希键实现：对每个环境$e$、智能体$i$、轮次$t$，生成唯一组标识$g = \mathrm{hash}(e, i, t)$。同一组内的候选动作保证：

- 来自相同的环境实例
- 由相同的智能体角色执行
- 处于相同的交互轮次
- 拥有相同的对话历史前缀

这恢复了GRPO的“同提示比较”前提，使组内优势估计重新有效。

#### 模块三：智能体级信用分配（Agent-wise Credit Assignment）

为每个智能体构造混合奖励信号：

$$r_{t,i} = \alpha r_{t}^{\mathrm{team}} + r_{t,i}^{\mathrm{loc}}$$

其中$\alpha=1$为默认设置，$r_{t}^{\mathrm{team}}$是回合级团队奖励（如任务成功/失败），$r_{t,i}^{\mathrm{loc}}$是智能体$i$的局部角色奖励（如代码编译通过、路径合法性等启发式信号）。该模块解决了MAS中“单一团队奖励导致信用分配模糊”的问题。

### 策略优化损失

AT-GRPO支持两种策略模式：**角色共享**（所有智能体共用单一策略$\theta$）和**角色专用**（每个智能体$i$维护独立策略$\theta^{(m)}$，其中$m=\sigma(i)$为策略分配映射）。优化目标为裁剪PPO损失：

$$\mathcal{L}(\theta^{(m)}) = -\mathbb{E}_{g \in B_{m}} \left[ \frac{1}{K} \sum_{c=1}^{K} \min \left( r_{g}^{(c,m)}(\theta^{(m)}) A_{g}^{(c)}, \mathrm{clip} \left( r_{g}^{(c,m)}(\theta^{(m)}), 1-\varepsilon, 1+\varepsilon \right) A_{g}^{(c)} \right) \right]$$

其中：
- $B_{m}$：分配给策略$m$的所有比较组的迷你批次
- $r_{g}^{(c,m)}(\theta^{(m)}) = \frac{\pi_{\theta^{(m)}}(a_g^{(c)} | q_g)}{\pi_{\theta^{(m)}_{\mathrm{old}}}(a_g^{(c)} | q_g)}$：新旧策略的概率比
- $A_{g}^{(c)}$：组$g$内候选$c$的相对优势（由Eq. 1计算）
- $\varepsilon$：裁剪阈值

角色专用模式下，Router根据$\sigma(i)$将每个智能体产生的经验路由至对应策略的UpdateWorker，各策略独立执行梯度更新。

### 训练系统架构

系统由四类组件构成（Figure 4）：

| 组件 | 职责 |
|------|------|
| **RolloutWorker**（每模型） | GPU推理服务，执行$K$路树结构采样，生成候选动作 |
| **CPU EnvWorker Pool** | 维护沙盒环境实例，执行动作并流式返回奖励 |
| **Router** | 按$\sigma(i)$将经验分发至对应模型的UpdateWorker |
| **UpdateWorker**（每模型） | 接收路由数据，独立执行PPO参数更新 |

该设计支持角色共享和角色专用两种模式的统一训练，且通过GPU资源池与CPU环境池的解耦实现分布式扩展。



## 实验与关键发现

### 核心结果

Stronger-MAS 在游戏、规划、编码和数学四大领域上进行了系统评估，使用 Qwen3-1.7B 和 Qwen3-8B 作为基座模型。表1和表2汇总了主要结果。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/006_Table_1.jpg]]
*Table 1: Qwen3 1.7B results on game, planning, coding, and math*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/007_Table_2.jpg]]
*Table 2: Qwen3 8B results on game, planning, coding, and math*

**长程规划任务上的突破性增益。** 在单智能体 RL 基线几乎无法求解的任务上，MAS+AT-GRPO 实现了从失败到近乎完美求解的跨越。具体而言：
- **Sokoban（6×6）**：Qwen3-8B 上从单智能体 GRPO 的 9.0% 提升至 **96.0%**（+87 个百分点）。
- **Plan-Path（10×10）**：Qwen3-1.7B 上从 5.0% 提升至 **96.0%**（+91 个百分点）。
- **Sudoku（4×4）**：Qwen3-1.7B 上从 7.0% 提升至 **99.0%**（+92 个百分点）。

这些任务的核心瓶颈在于需要多步前瞻规划与状态回溯，单智能体 GRPO 在此类长程依赖中完全失效，而 MAS 的多角色协同（如 Planner-Executor 或 Coder-Tester 循环）从根本上解决了这一问题。

**推理任务上的稳健提升。** 在编码和数学推理任务上，MAS+AT-GRPO 同样带来了显著增益：
- **编码**：LiveCodeBench-v6 上 Qwen3-8B 达到 33.10%（+10.30），APPS 上 Qwen3-1.7B 达到 28.30%（+16.30）。
- **数学**：AIME24 上 Qwen3-8B 达到 57.00%（+38.70），OlympiadBench 上 Qwen3-1.7B 达到 39.60%（+17.40）。

值得注意的是，这些增益并非来自更强的基座模型——所有对比实验使用完全相同的环境观察和奖励信号，唯一变量是是否引入多智能体交互。在已大量预训练的领域，增益相对温和（如 CodeContests 上仅 +2.35），提示性能可能趋于饱和。

**直接应用 GRPO 于 MAS 导致性能退化。** 一个关键的对照实验是 MAS+GRPO（无专用分组）。在 CodeContests（8B）上，该配置从 17.60 降至 **10.30**，甚至低于未训练的 MAS。这直接验证了核心瓶颈：标准 GRPO 的组归一化依赖于同质比较组，而 MAS 中各智能体/轮次的提示不同，导致优势估计方差大且训练不稳定。AT-GRPO 的按智能体和轮次分组机制正是为解决此问题而设计。

### 消融实验

**角色专用策略的必要性。** 表4在 Plan-Path 任务上进行了系统的消融实验：
- 单独训练各智能体再组合仅从 5.0% 提升至 16.0%，而**联合训练**可达 96.0%。这表明智能体间的协同策略必须在交互环境中共同演化，离线独立训练无法习得有效的协作行为。
- **交换训练好的角色专用策略**（Swapped Policies）导致准确率从 96.0% 骤降至 6.0%，证实 RL 确实强化了不可互换的角色专属策略——Planner 和 Executor 的策略已深度专业化，角色互换等同于随机执行。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/011_Table_4.jpg]]
*Table 4: Plan-Path (Qwen3-1.7B) ablation. Performance gain ∆ over the single agent baseline*

**策略共享 vs 角色专用的任务依赖性。** 对比表1和表2中 MAS+AT-GRPO（Shared）与 MAS+AT-GRPO（Per-Role）两行：
- 编码任务中角色专用平均高 **3.05 个百分点**（Qwen3-1.7B），Coder-Tester 的明确分工使得专用策略更有优势。
- 数学推理上共享策略有时更优（如 AIME24 上 1.7B 模型 Shared 为 43.50 vs Per-Role 为 42.00），因为 Reasoner-Verifier 角色的数据分布高度重叠，专用策略反而导致训练数据不足。
- 这一发现揭示了当前方法的一个局限：选择共享还是专用策略目前依赖任务特性的人工判断，缺乏自动化准则。

**稀疏奖励鲁棒性。** 表6评估了移除所有中间启发式奖励后 AT-GRPO 的表现。仅使用结局奖励时：
- Sokoban 从 96.0% 降至 93.0%（仅降 3 个百分点），Sudoku 从 99.5% 降至 99.5%（无下降），Plan-Path 从 96.0% 降至 89.0%（降 7 个百分点，但仍远超 SA 的 12.0% 和 MAS 的 71.0%）。
- 这证明 AT-GRPO 的性能增益并非来自精心设计的稠密奖励，而是源于多智能体协同本身的结构性优势。稠密奖励主要起到加速训练的作用。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IdF6JqXWzx/figures/016_Table_6.jpg]]
*Table 6: Performance Comparison with Sparse Outcome-Only Rewards. To address concerns regarding reward engineering, we evaluate AT-GRPO using only sparse outcome signals (Outcomeonly), removing all intermediate heuristics. Even without dense guidance, our method maintains high performance and significantly outperforms the baselines*

**多轮单智能体无益。** 表7和表8对比了单智能体在单轮和多轮设置下的表现。引入多轮自我修订非但未提升，反而损害性能——例如 LiveCodeBench（1.7B）上单轮 RL 达到 18.80，而多轮 RL 降至 10.40。这进一步支持了核心论点：性能增益来源于**多角色协同**而非简单的多轮交互。

### 与现有 MARL 框架的对比

表3将 StrongerMAS 与 MAPORL（Park et al., 2025）、MARFT（Liao et al., 2025）和 CURE（Wang et al., 2025a）进行了横向对比。在数学任务上，未训练的 MAS（84.4%）已超过经过 RL 训练的 MAPORL（81.0%）和 MARFT（78.7%），而 MAS+AT-GRPO 进一步达到 88.7%。这验证了异构角色工作流（Reasoner + Tool-User）相比同质辩论（MAPORL）和单轮顺序交互（MARFT）的固有优势。

表5从框架特性维度进行了全面对比，StrongerMAS 是唯一同时支持策略共享与专用、顺序与并行执行、多轮交互、角色异构和跨领域（≥2 领域）的方法。

### 训练动态

Figure 6 展示了角色专用策略训练过程中的两个关键趋势：
- **奖励对齐**（Figure 6a）：Tool Agent 和 Plan Agent 的标准化奖励在训练过程中逐步收敛，表明两个角色学会了对齐彼此的期望，形成稳定的协作模式。
- **求解效率提升**（Figure 6b）：平均求解回合数随训练持续下降，说明智能体不仅学会了正确求解，还学会了更高效的协作——减少不必要的交互轮次。

### 失败模式与局限

1. **编码/数学领域的增益饱和**：在 CodeContests 等已大量预训练的基准上，增益仅为 +2.35 个百分点，提示 AT-GRPO 的边际收益在强基线上递减。
2. **策略共享模式的选择依赖人工判断**：目前缺乏可量化的任务特征来自动决定最优策略分配模式。
3. **推理延迟线性增长**：顺序执行的 MAS 中，Wall-clock 推理延迟随智能体数量线性增加（N 倍），在延迟敏感场景下可能不适用。
4. **贪心树搜索可能限制探索**：树结构采样中的贪心选择策略（每步选择最高奖励候选）可能导致探索不足，尤其在奖励信号稀疏的早期训练阶段。



## 定位与知识库关联

### 1. 方法在现有谱系中的位置

AT-GRPO 处于**多智能体强化学习（MARL）与大语言模型（LLM）微调**的交叉地带，其核心贡献在于将单智能体的群体相对策略优化（GRPO）范式系统性地适配到多角色、多轮交互场景。在现有谱系中，该方法填补了以下关键空白：

**与单智能体RL基线的关系。** 标准GRPO（Shao et al., 2024）依赖“同提示多响应”形成比较组以计算相对优势，这一假设在多智能体场景下因各角色提示和对话历史不同而系统性失效。AT-GRPO通过**按智能体和轮次分组**（Agent- and Turn-wise Grouping）与**树结构采样**（Tree-structured Sampling）恢复了GRPO的方差缩减效果，使得MAS环境中的在线RL训练成为可能。直接对MAS应用GRPO的实验证据支撑了这一论断：在CodeContests（8B）上，MAS+GRPO从17.60降至10.30，性能不升反降（Table 2）。

**与现有MARL框架的对比。** 论文将AT-GRPO与三个代表性MARL框架进行了横向比较（Table 3、Table 5）：

- **MAPORL**（Park et al., 2025）：采用同质角色的辩论工作流进行RL训练，缺乏角色异构性和多轮迭代交互。在gsm8k上，StrongerMAS未经训练的MAS（84.4%）即已超越经过训练的MAPORL（81.0%），表明角色化协同本身已具备强基线能力。
- **MARFT**（Liao et al., 2025）：支持单轮顺序交互的MAS微调，但缺乏多轮迭代能力。在math任务上，未经训练的MAS（84.4%）同样优于MARFT（78.7%）。
- **CURE**（Wang et al., 2025a）：采用共享策略的Coder-Tester协同RL，支持多轮交互但与AT-GRPO的角色专用模式相比，在编码任务上平均低3.05个百分点（Table 1）。

AT-GRPO在框架完备性上具有显著优势（Table 5）：同时支持策略共享与角色专用、并行与顺序执行、多轮交互、角色异构性，且是唯一覆盖四个以上领域的框架。

### 2. 适用边界与条件

**强适用场景。** AT-GRPO在以下条件下表现出决定性增益：

1. **长程规划任务**：在Sokoban（6×6）和Plan-Path（10×10）等需要多步推理和空间规划的任务上，单智能体基线准确率仅9-14%，AT-GRPO将其提升至96%以上（Table 1、Table 2）。这类任务的核心瓶颈在于单智能体缺乏跨角色的验证与纠错机制，而MAS通过角色分工（如Planner-Tool User）实现了有效协同。
2. **需要角色专业化的任务**：消融实验（Table 4）表明，交换训练好的角色专用策略导致准确率从96%骤降至6%，证实RL强化了不可互换的角色专属策略。联合训练（96%）远优于独立训练后组合（16%），说明角色间的在线交互是策略专业化的必要条件。
3. **稀疏奖励环境**：AT-GRPO在仅使用结局奖励（移除所有中间启发式信息）时，性能下降极小（Plan-Path仅从93%降至89%，Table 6），且仍大幅领先单智能体基线（12%）和未训练MAS（71%），表明方法不依赖稠密奖励工程。

**弱适用或需谨慎的场景。**

1. **已大量预训练的领域**：在编码和数学推理任务上，性能增益相对有限（编码平均+3.87-7.62%，数学平均+9.0-17.93%）。论文指出这可能是因为这些领域的预训练数据已使模型具备较强单智能体能力，MAS的边际收益趋于饱和。
2. **策略共享vs专用的选择**：目前依赖任务特性的人工判断——编码任务中角色专用平均高3.05点，但数学推理上共享策略有时更优（Table 1、Table 2）。缺乏自动化的选择准则。
3. **多轮单智能体场景**：消融实验（Table 7、Table 8）显示，引入多轮单智能体自我修订非但未提升性能，反而可能造成损害（如LiveCodeBench从11.6降至10.4），说明多轮交互的收益来源于角色异构性而非简单的迭代次数增加。

### 3. 局限与开放问题

**已确认的局限。**

1. **推理延迟线性增长**：在顺序执行的MAS中，wall-clock推理延迟随智能体数量线性增加（N倍），这在实时性要求高的场景中可能成为瓶颈。
2. **奖励函数依赖领域知识**：尽管稀疏奖励可行，稠密奖励（如中间步骤的正确性判断）仍能加速训练。奖励设计仍需领域特定的启发式信息。
3. **贪心采样的探索局限**：树结构采样采用贪心选择最高奖励动作执行下一步，可能导致探索不足。论文未对此进行系统性分析。
4. **系统复杂度**：当智能体数量大幅增加时，Router的通信调度和EnvWorker池的管理复杂度可能成为扩展瓶颈。

**开放问题。**

1. **跨角色信用分配的一般化**：当前信用分配采用团队奖励与局部奖励的简单混合（$\alpha=1$），当团队奖励稀疏且延迟时，如何更精确地将全局信号归因到各角色各轮次的动作仍是一个开放问题。
2. **策略共享模式的自动决策**：哪些可量化的任务特征（如角色间的动作空间重叠度、信息不对称程度）能够自动决定最优策略共享模式，目前缺乏理论指导。
3. **开放文本任务的扩展**：当前实验集中于具有可验证奖励的符号化任务（游戏、规划、代码执行、数学答案判定）。该方法能否有效扩展到依赖LLM判断的开放文本任务（如辩论、写作协作），需要进一步验证。
4. **探索机制的改进**：树结构采样中的贪心选择策略是否会导致探索不足？能否设计更高效的探索机制（如基于不确定性的分支选择）以进一步提升样本效率？

### 4. 知识库定位

AT-GRPO在知识库中的定位可概括为：**首个将GRPO的组归一化优势估计系统性地适配到多角色、多轮MAS场景的在线RL算法框架**。其核心知识贡献包括：

- **方法论层面**：提出了“按智能体和轮次分组”的原则，解决了MAS中优势估计方差大的瓶颈问题；配合树结构采样，在保持有效比较组的同时支持多轮交互的信用分配。
- **系统设计层面**：构建了支持多策略并行训练和角色专用更新的分布式训练系统，为后续MAS-RL研究提供了可复用的基础设施。
- **实证发现层面**：揭示了角色专用策略的不可互换性、联合训练的必要性、以及多轮单智能体交互的无效性，为MAS设计提供了重要的经验准则。



## 原文 PDF

![[paperPDFs/ICLR_2026/Stronger_MAS_Multi_Agent_Reinforcement_Learning_for_Collaborative_LLMs.pdf]]
