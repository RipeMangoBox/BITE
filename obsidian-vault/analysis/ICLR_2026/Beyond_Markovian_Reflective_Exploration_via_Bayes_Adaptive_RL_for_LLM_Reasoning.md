---
title: "Beyond Markovian: Reflective Exploration via Bayes-Adaptive RL for LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Markovian_Reflective_Exploration_via_Bayes_Adaptive_RL_for_LLM_Reasoning.pdf
openreview_forum_id: vuyk1fSaE4
aliases:
- BBARLR
- BMREBARLR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将反思探索嵌入贝叶斯强化学习框架，优化在后验MDP分布上的期望回报，使策略变得不确定性自适应，从而根据信念更新引导信息收集和策略切换。"
primary_logic: "BARL通过维持MDP假设的后验分布（每个假设关联一个候选答案），利用状态条件下的模型置信度和奖励不一致性惩罚来加权Q值，为策略拼接和切换提供原则性指导，实现高效的探索与利用权衡。"
claims:
- "贝叶斯RL下最优策略可以是严格不确定性自适应的，并且可以比最优马尔可夫策略任意好。"
- "BARL在多个数学推理基准和模型规模上一致优于GRPO和进度奖励基线，同时使用显著更少的令牌。"
- "反思频率与模型性能没有强相关性，BARL的优势源于更有效的探索和利用，体现在更高的贝叶斯状态-动作值上。"
- "在合成的迁移任务中，传统RL记忆训练解但无法泛化，而BARL通过假设消除发现真实MDP。"
---

# Beyond Markovian: Reflective Exploration via Bayes-Adaptive RL for LLM Reasoning

> [!tip] 核心洞察
> BARL通过维持MDP假设的后验分布（每个假设关联一个候选答案），利用状态条件下的模型置信度和奖励不一致性惩罚来加权Q值，为策略拼接和切换提供原则性指导，实现高效的探索与利用权衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越马尔可夫性：基于贝叶斯自适应强化学习的LLM推理反思探索 |
| 英文题名 | Beyond Markovian: Reflective Exploration via Bayes-Adaptive RL for LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vuyk1fSaE4); [GitHub](https://github.com/shenao-zhang/BARL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | BARL (Bayes-Adaptive RL for LLM Reasoning) |
| Dataset | Average across GSM8K, MATH, CollegeMath, Olympiad, AIME 2024, AMC 2023 (Qwen2.5-Math-1.5B), Average across benchmarks (Qwen2.5-Math-7B), Average across benchmarks (R1-Distill-Llama-8B), Token Efficiency (Qwen2.5-Math-1.5B) |

> [!tip] 效果简介
> - Average across GSM8K, MATH, CollegeMath, Olympiad, AIME 2024, AMC 2023 (Qwen2.5... 上，Accuracy (%) 为 53.3，对比 51.0 (GRPO)，变化 +2.3。
> - Average across benchmarks (Qwen2.5-Math-7B) 上，Accuracy (%) 为 59.4，对比 57.1 (GRPO)，变化 +2.3。
> - Average across benchmarks (R1-Distill-Llama-8B) 上，Accuracy (%) 为 52.7，对比 52.1 (GRPO)，变化 +0.6。

## 概述

当前将强化学习（RL）应用于大语言模型（LLM）推理的主流范式存在一个根本性瓶颈：传统RL训练得到的马尔可夫策略无法产生**反思性探索**（reflective exploration）。这是因为策略仅通过当前状态依赖历史，一旦训练完成便缺乏在相同状态下主动收集额外上下文的动机——探索仅在训练期间以试错方式进行，部署时没有探索激励，因此无法保证反思行为的涌现，也无法从原理上解释其何时有益。

本文的核心洞察是：将反思探索嵌入**贝叶斯强化学习**框架，优化策略在后验MDP分布上的期望回报，从而使策略变得**不确定性自适应**（uncertainty-adaptive）。具体而言，BARL（Bayes-Adaptive RL for LLM Reasoning）通过维持MDP假设的后验分布——每个假设关联一个从当前策略采样得到的候选答案——利用状态条件下的模型置信度和奖励不一致性惩罚来加权Q值，为策略拼接与切换提供原则性指导。当模型的内部信念与累积奖励反馈出现分歧时，BARL通过压低“信念概率高但与观测奖励不一致”的假设权重，自然触发策略切换，实现高效的探索与利用权衡。

理论上，本文证明了传统RL存在不具反思探索能力的最优马尔可夫策略（Theorem 4.1），而贝叶斯RL框架下的最优策略可以是严格不确定性自适应的，并且可以比最优马尔可夫策略任意好（Theorem 4.3）。这为反思行为的必要性提供了形式化保证。

实验上，BARL在多个数学推理基准（GSM8K、MATH、CollegeMath、Olympiad、AIME 2024、AMC 2023）和三种模型规模（Qwen2.5-Math-1.5B/7B、R1-Distill-Llama-8B）上一致优于GRPO和进度奖励基线（Table 1），同时使用显著更少的令牌——平均比GRPO少约2倍，比进度奖励基线少约1.63倍，比基础模型少10倍以上（Figure 5）。消融实验进一步表明，反思频率与模型性能并无强相关性；BARL的优势源于更有效的探索和利用，体现在其思维链具有更高的贝叶斯状态-动作值（Figure 6, Figure 7）。在合成的迁移任务中，传统RL记忆训练解但无法泛化，而BARL通过假设消除成功发现真实MDP（Figure 4），验证了贝叶斯框架的泛化能力。

## 背景与动机

### 马尔可夫策略的反思盲区

大语言模型在数学推理等复杂任务中展现出强大的能力，但当模型在推理中途发现当前路径可能错误时，能否自发地进行反思并切换策略，是决定其最终表现的关键。现有主流方法——基于结果奖励的强化学习训练——通常将推理过程建模为马尔可夫决策过程，优化单一真实MDP下的期望回报。这类训练得到的策略是**马尔可夫策略**：模型在每一步仅依赖当前状态（已生成的推理步骤）做出决策，没有内在动机去收集额外信息或回溯验证。

这导致一个根本性问题：马尔可夫策略无法产生**反思性探索**。在训练阶段，探索仅以试错方式发生；在部署阶段，策略已固化，没有探索激励。因此，传统强化学习训练既不能保证反思行为的涌现，也无法解释反思何时以及为何有益。论文通过一个教学性合成实验揭示了这一缺陷：传统RL（REINFORCE）仅记忆训练解，在分布外任务上泛化失败，而BARL通过假设消除能发现真实MDP并成功泛化（**Figure 4**）。

### 反思探索的关键瓶颈

反思行为的核心在于**不确定性自适应**：当模型对当前推理路径的信念与累积奖励反馈出现偏差时，应触发策略切换。然而，传统RL框架下的策略仅通过当前状态依赖历史，缺乏对MDP本身不确定性的建模——模型不知道“自己不知道什么”。因此，即使面对明显错误的中间步骤，策略也可能继续沿原路径推进，而非停下来反思。

这一瓶颈的因果机制可概括为：**传统RL优化目标仅针对单一真实MDP，策略梯度中的值函数不包含对MDP不确定性的后验信念，导致模型无法区分“需要更多信息”的状态和“已足够确定”的状态。**

### 从贝叶斯RL到反思涌现

本文的核心动机是将反思探索重新置于**贝叶斯强化学习**框架中。贝叶斯RL优化的是在MDP后验分布上的期望回报，而非单一MDP。这一形式化转变使策略变得**不确定性自适应**：通过维持对可能MDP假设的信念分布，策略可以根据信念更新来引导信息收集和策略切换。

BARL的核心洞察在于：当模型内部信念（对候选答案的概率估计）与外部奖励信号（前进奖励的一致性）出现矛盾时，相关MDP假设的权重会被惩罚性降低，从而为策略拼接和切换提供原则性指导。这一机制使反思探索从启发式技巧提升为优化目标的内在属性——反思不是被显式编程的行为，而是贝叶斯最优策略在不确定性下的自然涌现。

### 现有方法的缺口

当前LLM推理的强化学习训练方法存在三个层面的缺口：

1. **目标层面**：GRPO（Guo et al., 2025）和进度奖励基线（Qu et al., 2025）均优化单一MDP下的期望回报，缺乏对认知不确定性的建模。
2. **信号层面**：仅依赖最终结果验证器或简单进度信号，无法向策略传递“当前路径与哪些假设一致或不一致”的结构化信息。
3. **行为层面**：训练得到的策略缺乏部署时的探索激励，反思行为无原则性保障，其频率与性能之间无强相关性（如**Figure 6**所示）。

BARL通过将优化目标替换为贝叶斯期望回报、将值函数替换为后验加权Q值、将奖励信号扩展为进度奖励加结果奖励，系统性地填补了上述缺口。

## 核心创新

### 问题瓶颈：马尔可夫策略为何无法产生反思

传统强化学习（RL）训练LLM推理时，优化目标是在单一真实MDP $\mathcal{M}^*$ 下最大化期望回报 $\mathcal{J}_{\mathcal{M}^*}(\pi)$。这一框架存在一个根本性局限：**存在一个最优马尔可夫策略，该策略仅依赖当前状态 $s_t$ 做决策，无需反思**（Theorem 4.1）。这意味着传统RL没有动机让模型在遇到相同数学状态时停下来重新审视——策略只需记住训练时的成功路径即可。

这导致了两个关键失败模式：
- **训练期间**：探索仅以试错方式发生，策略通过记忆捷径而非真正的信息收集来最大化奖励。
- **部署期间**：没有探索激励，模型无法根据推理过程中的新证据调整策略，泛化能力受限。

教学示例（Figure 4）清晰地展示了这一瓶颈：传统RL（REINFORCE）快速记忆训练解，但在评估任务上完全无法泛化。

### 核心机制：从贝叶斯RL到不确定性自适应策略

BARL将优化目标从单一MDP切换到**后验MDP分布上的贝叶斯期望回报**：

$$\mathcal{I}(\pi) = \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D})} \left[ \mathcal{I}_{\mathcal{M}}(\pi) \right]$$

这一目标函数的改变是根本性的——它使最优策略变为**不确定性自适应**（uncertainty-adaptive）的：策略可以根据信念更新，在相同状态 $s_t$ 下选择不同的动作分布（Theorem 4.2, Definition 3.2）。Theorem 4.3进一步证明，贝叶斯RL下的最优策略可以比最优马尔可夫策略**任意好**，因为前者能通过信息收集动作主动消除MDP不确定性。

### 关键设计：四个Changed Slots

相比传统RL基线（GRPO, Guo et al., 2025），BARL在四个关键维度上进行了系统性改造：

**1. 优化目标（Slot: 优化目标）**
- **基线**：$\max_\pi \mathcal{J}_{\mathcal{M}^*}(\pi)$，在单一真实MDP上优化。
- **BARL**：$\max_\pi \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D})}[\mathcal{J}_\mathcal{M}(\pi)]$，在后验分布上优化（公式3.1）。
- **效果**：目标本身内化了认知不确定性，驱动策略主动收集信息。

**2. 策略梯度中的值函数（Slot: 值函数）**
- **基线**：使用真实MDP下的 $Q_{\mathcal{M}^*}^{\pi}(h_t, a_t)$。
- **BARL**：使用后验加权Q值 $\mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|h_t)}[Q_{\mathcal{M}}^{\pi_\theta}(h_t, a_t)]$（公式5.1）。
- **效果**：值估计融合了模型对当前假设的信念，为策略切换提供原则性信号。

**3. 奖励信号（Slot: 奖励信号）**
- **基线**：仅使用最终结果验证器奖励。
- **BARL**：进度奖励（基于答案概率变化）+ 结果奖励（公式3.2）。
- **效果**：进度奖励提供逐步骤的密集反馈，使奖励不一致性惩罚成为可能。

**4. Q值估计器（Slot: Q值估计）**
- **基线**：基于单一MDP的期望未来回报。
- **BARL**：通过自归一化重要性采样对候选MDP集合加权（公式5.4）：

$$\mathbb{E}_{\mathcal{M} \sim p(\mathcal{M} \mid h_t)}[Q_{\mathcal{M}}^{\pi_\theta}(h_t, a_t)] = \sum_{i=0}^{|\mathcal{M}|} Q_{\mathcal{M}_i}^{\pi_\theta}(h_t, a_t) \cdot \underbrace{\pi_\theta(y_{s_0}^{\mathcal{M}_i} \mid s_t + </\mathrm{think}>)}_{\text{模型置信度}} \cdot \underbrace{\prod_{t'=0}^{t-1} \exp(-\beta |r_{t'} - r_{\mathcal{M}_i}(s_{t'}, a_{t'})|)}_{\text{奖励一致性惩罚}}$$

- **效果**：两项权重分别捕获状态条件下的答案信念和累积奖励不一致性，当当前策略的奖励预测与实际观察偏离时自动降低该假设的权重，触发策略切换（Remark 5.1）。

### 算法流程

BARL的核心pipeline由三个模块构成：

1. **候选答案采样**：对每个提示从当前策略 $\pi_\theta$ 采样 $|\mathcal{M}|$ 条思维链，提取最终答案形成MDP假设集合（Algorithm 1, Step 3-4）。
2. **后验加权值计算**：在每个时间步 $t$，按公式5.4组合各MDP假设下的Q值、状态条件答案概率和奖励一致性惩罚。
3. **策略梯度更新**：使用后验加权Q值作为回归目标，通过策略梯度（公式5.1）更新LLM参数 $\theta$，使模型内化奖励预测和信念更新。

### 创新本质

BARL的创新不在于引入反思机制本身，而在于**将反思探索嵌入贝叶斯RL框架，为"何时反思"和"如何切换策略"提供了原则性答案**。传统方法通过提示工程或奖励塑形鼓励反思，但缺乏理论保证；BARL通过维持MDP假设的后验分布，使反思行为作为信念更新的自然产物涌现——当累积奖励与当前假设的预测不一致时，奖励一致性惩罚自动降低该假设权重，驱动策略探索替代方案。Figure 7的消融实验证实，BARL模型的思维链具有一致更高的贝叶斯状态-动作值，表明其探索和利用均更有效。

## 整体框架

BARL 将 LLM 推理的反思探索重构为贝叶斯自适应强化学习问题。其核心 pipeline 由三个模块串联构成，形成一个从候选答案采样到后验加权值估计再到策略梯度更新的闭环。

**候选答案采样模块**：对于每个输入提示 $s_0$，从当前策略 $\pi_\theta$ 采样 $|\mathcal{M}|$ 条思维链（CoT），提取每条链的最终答案，构成 MDP 假设集合 $\{\mathcal{M}_i\}_{i=1}^{|\mathcal{M}|}$。每个假设 $\mathcal{M}_i$ 关联一个候选答案 $y_{s_0}^{\mathcal{M}_i}$，其奖励函数定义为：若最终答案匹配该候选答案则进度奖励和结果奖励均为 1，否则为 0。这一设计将“哪个答案正确”的认知不确定性显式编码为可操作的 MDP 后验分布。

**后验加权值计算模块**：对于推理过程的每个时间步 $t$，BARL 不依赖单一 MDP 下的 Q 值，而是计算所有候选 MDP 假设下的后验加权 Q 值。该加权机制由三项因子乘积构成（公式 5.4）：
1. **MDP 条件 Q 值** $Q_{\mathcal{M}_i}^{\pi_\theta}(h_t, a_t)$：在假设 $\mathcal{M}_i$ 下，从当前历史 $h_t$ 执行动作 $a_t$ 后的期望未来回报；
2. **状态条件答案概率** $\pi_\theta(y_{s_0}^{\mathcal{M}_i} \mid s_t + \langle/\text{think}\rangle)$：LLM 在当前部分推理状态下对候选答案 $\mathcal{M}_i$ 的内在置信度；
3. **奖励一致性惩罚** $\prod_{t'=0}^{t-1} \exp(-\beta |r_{t'} - r_{\mathcal{M}_i}(s_{t'}, a_{t'})|)$：累积已观察奖励与假设 $\mathcal{M}_i$ 预测奖励之间的差异，温度参数 $\beta$ 控制惩罚强度。

当某个假设的预测奖励与实际观察持续不一致时，其累积惩罚项趋近于零，该假设的权重被有效消除。这一机制为策略提供了原则性的切换信号：LLM 应在内在信念与累积奖励反馈出现分歧时进行反思，即降低高置信度但奖励不匹配假设的权重，转向其他候选策略。

**策略梯度更新模块**：使用后验加权 Q 值替代传统 RL 中的单一 MDP Q 值，通过策略梯度更新 LLM 参数 $\theta$：

$$\nabla_{\theta} \mathcal{I} = \mathbb{E}_{s_0, \pi_\theta} \left[ \sum_{t=0}^{T-1} \nabla_{\theta} \log \pi_\theta(a_t \mid h_t) \cdot \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D}, h_t)} \left[ Q_{\mathcal{M}}^{\pi_\theta}(h_t, a_t) \right] \right]$$

这一梯度使策略学会内化奖励预测和信念更新，从而在部署时无需显式贝叶斯推断即可产生不确定性自适应行为。

**输入输出流**：整个流程以提示 $s_0$ 为输入，经过策略自回归生成思维链 $a_0, a_1, \dots, a_{T-1}$，每一步的生成由后验加权值引导。训练时，进度奖励 $r(s_t, a_t)$ 由冻结的奖励模型 $\pi_\phi$ 计算正确答案概率的增量得到（公式 3.2），结果奖励由最终答案验证器提供。输出为经过贝叶斯 RL 微调的 LLM 策略 $\pi_\theta$，其在推理时能根据观察到的中间结果动态调整策略，实现假设消除驱动的反思探索。

## 核心模块与公式推导

### 3.1 贝叶斯自适应RL目标

BARL的核心优化目标是将策略训练从单一真实MDP扩展到MDP后验分布上的期望回报。给定训练数据 $\mathcal{D}$ 诱导的MDP后验分布 $p(\mathcal{M}|\mathcal{D})$，贝叶斯预期回报定义为：

$$\mathcal{I}(\pi) = \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D})} \Big[ \mathcal{I}_{\mathcal{M}}(\pi) \Big], \quad \mathcal{I}_{\mathcal{M}}(\pi) = \mathbb{E}_{s_0,\pi} \left[ \sum_{t=0}^{T-1} r_{\mathcal{M}}(s_t, a_t) \right]$$

其中 $\mathcal{I}_{\mathcal{M}}(\pi)$ 是策略 $\pi$ 在特定MDP $\mathcal{M}$ 下的期望累积奖励。这一目标使得策略必须对MDP的不确定性保持敏感——当后验分布包含多个候选MDP时，最优策略需要主动收集信息以消除歧义，从而自然诱导反思探索行为。

### 3.2 进度奖励设计

为提供逐步反馈信号，BARL采用基于答案概率变化的进度奖励。对于提示 $s_0$ 及其正确答案 $y_{s_0}^*$，在时间步 $t$ 执行动作 $a_t$ 后的奖励为：

$$r(s_t, a_t) = \pi_{\phi}(y_{s_0}^* \mid s_t + a_t + </\mathrm{think}>) - \pi_{\phi}(y_{s_0}^* \mid s_t + </\mathrm{think}>)$$

该奖励度量添加推理步骤 $a_t$ 后，冻结的参考模型 $\pi_{\phi}$ 对正确答案概率的增量。完整的轨迹回报还包括最终的结果验证器奖励 $\mathrm{verifier}(s_0, a_{0:T-1})$，因此MDP $\mathcal{M}$ 下的Q值定义为：

$$Q_{\mathcal{M}}^{\pi}(h_t, a_t) = \mathbb{E}_{\pi} \left[ \sum_{t'=t}^{T-1} r_{\mathcal{M}}(s_{t'}, a_{t'}) + \mathrm{verifier}(s_0, a_{0:T-1}) \right]$$

### 3.3 后验加权策略梯度

直接优化贝叶斯目标 $\mathcal{I}(\pi)$ 的策略梯度为：

$$\nabla_{\theta} \mathcal{I} = \mathbb{E}_{s_0, \pi_{\theta}} \left[ \sum_{t=0}^{T-1} \nabla_{\theta} \log \pi_{\theta}(a_t \mid h_t) \cdot \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D}, h_t)} \left[ Q_{\mathcal{M}}^{\pi_{\theta}}(h_t, a_t) \right] \right]$$

与传统RL的关键区别在于：值函数项被替换为**后验加权Q值** $\mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D}, h_t)}[Q_{\mathcal{M}}^{\pi_{\theta}}(h_t, a_t)]$，而非单一真实MDP下的Q值。这个后验加权项编码了模型对当前轨迹历史 $h_t$ 下各MDP假设的信念，从而为策略提供何时切换推理路径的原则性信号。

### 3.4 后验加权值的可操作估计

上述后验加权Q值的计算需要近似。BARL将MDP后验分解为两项的乘积：

$$p(\mathcal{M} \mid \mathcal{D}, h_t) \propto p(\mathcal{M} \mid \mathcal{D}, s_{0:t}) \cdot p(r_{0:t-1} \mid s_{0:t}, a_{0:t-1}, \mathcal{M})$$

- **第一项** $p(\mathcal{M} \mid \mathcal{D}, s_{0:t})$：给定观测状态序列后MDP假设的先验信念。BARL用策略 $\pi_{\theta}$ 在当前状态 $s_t$ 下输出候选答案 $y_{s_0}^{\mathcal{M}_i}$ 的概率 $\pi_{\theta}(y_{s_0}^{\mathcal{M}_i} \mid s_t + </\mathrm{think}>)$ 来近似，反映模型对该假设的置信度。
- **第二项** $p(r_{0:t-1} \mid s_{0:t}, a_{0:t-1}, \mathcal{M})$：观测奖励序列的似然。BARL建模为：

$$p(r_{0:t-1} \mid s_{0:t}, a_{0:t-1}, \mathcal{M}) \propto \prod_{t'=0}^{t-1} \exp(-\beta |r_{t'} - r_{\mathcal{M}}(s_{t'}, a_{t'})|)$$

其中 $\beta$ 为温度参数（实验中设为1），$r_{\mathcal{M}}(s_{t'}, a_{t'})$ 为假设MDP $\mathcal{M}$ 在状态-动作对上的期望进度奖励。该惩罚项累积预测奖励与观测奖励的绝对偏差：当当前推理路径的奖励反馈与某假设MDP的预期严重不一致时，该项指数衰减，从而**降低该假设的权重**。

综合以上，后验加权Q值的可操作估计为（证据锚点：公式5.4）：

$$\mathbb{E}_{\mathcal{M} \sim p(\mathcal{M} \mid h_t)} \left[ Q_{\mathcal{M}}^{\pi_{\theta}}(h_t, a_t) \right] = \sum_{i=0}^{|\mathcal{M}|} Q_{\mathcal{M}_i}^{\pi_{\theta}}(h_t, a_t) \cdot \pi_{\theta}(y_{s_0}^{\mathcal{M}_i} \mid s_t + </\mathrm{think}>) \cdot \prod_{t'=0}^{t-1} \exp(-\beta |r_{t'} - r_{\mathcal{M}_i}(s_{t'}, a_{t'})|)$$

### 3.5 算法流程

BARL的训练循环（Algorithm 1）包含三个核心模块：

1. **候选答案采样**：对每个提示 $s_0$，从当前策略 $\pi_{\theta}$ 采样 $|\mathcal{M}|$ 条思维链（CoT），提取各自的最终答案，形成MDP假设集合 $\{\mathcal{M}_i\}_{i=1}^{|\mathcal{M}|}$。实验中 $|\mathcal{M}|=5$。

2. **后验加权值计算**：对于轨迹的每个时间步 $t$，按公式(5.4)计算后验加权Q值。该值综合了三个信号：每个MDP假设下的未来期望回报 $Q_{\mathcal{M}_i}^{\pi_{\theta}}$、模型对该假设答案的当前置信度、以及历史奖励一致性惩罚。

3. **策略梯度更新**：以后验加权Q值为回归目标，通过策略梯度公式(5.1)更新LLM参数 $\theta$。这一更新机制使模型内化奖励预测和信念更新，从而在推理时自主进行策略拼接与切换。

## 实验与分析

### 主要结果

BARL在多个数学推理基准和模型规模上一致优于GRPO和进度奖励基线。Table 1汇总了三个独立训练运行的平均准确率和标准误差。在Qwen2.5-Math-1.5B上，BARL的平均准确率达到53.3%，比GRPO（51.0%）和进度奖励基线（51.4%）分别高出2.3和1.9个百分点。在Qwen2.5-Math-7B上，BARL以59.4%的平均准确率领先GRPO（57.1%）和进度基线（57.9%）。在R1-Distill-Llama-8B上，BARL同样取得最高平均准确率52.7%，优于GRPO的52.1%和进度基线的51.0%。这些结果表明，BARL的优势在不同模型规模上具有一致性。

值得注意的是，BARL在取得更高准确率的同时使用了显著更少的令牌。Figure 5展示了pass@k准确率与总令牌消耗的关系：BARL以更少的总令牌数实现了更高的pass@k准确率。具体而言，BARL的平均令牌消耗比进度基线少约1.63倍，比GRPO少约2倍，比基础模型少超过10倍。这种令牌效率优势源于BARL的贝叶斯自适应策略能够更有效地分配思考令牌，而非简单地增加推理长度。

### 消融实验

**贝叶斯状态-动作值分析。** Figure 7展示了不同模型产生的CoT在所有时间步上的平均贝叶斯状态-动作值。BARL模型展现出持续更高的贝叶斯值，这表明其CoT在探索和利用两方面都更为有效。贝叶斯值天然地同时捕捉了探索维度（策略是否有效地收集信息以区分假设）和利用维度（策略是否在正确假设下高效推进），因此更高的贝叶斯值直接印证了BARL机制的有效性。

**反思频率与性能的关系。** Figure 6分析了GSM8K和MATH问题上模型的反思频率。结果显示，反思频率与模型性能之间并无强相关性。这一发现具有重要启示：BARL的优势并非简单地源于"更多反思"，而是源于更有效的探索和利用——即模型在正确的时机进行反思，而非在所有情况下频繁反思。这验证了贝叶斯框架提供的原则性策略切换信号的价值。

**长度控制消融。** Figure 8显示，即使对GRPO施加长度惩罚以控制响应长度，其性能仍然不如BARL。这说明BARL的令牌效率优势并非来自简单的长度约束，而是来自其内在的探索-利用权衡机制。

**合成任务泛化能力。** Figure 4展示了教学示例中传统RL与BARL的泛化对比。传统RL（REINFORCE）快速记忆训练解但在评估任务上泛化失败，而BARL在部署到评估任务时表现良好。更重要的是，BARL的性能随着候选集提供更多先验知识而提高——当候选集告知模型"奖励三元组是重复模式"时，BARL的准确率和收敛速度均显著提升。这验证了贝叶斯框架中先验知识对假设消除效率的促进作用。


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/006_Figure_4.jpg]]
*Figure 4: Conventional RL (REINFORCE) memories training solutions and poorly generalizes beyond the training prompts. BARL performs well when deployed to the evaluation tasks, and improves with more informative candidate sets*

**采样温度鲁棒性。** 附录B.3（Figure 16）显示，在采样温度=1时，GRPO和基础模型对温度变化更为敏感，而BARL表现出更好的鲁棒性。这一特性与BARL的不确定性自适应本质一致：当采样噪声增大时，贝叶斯后验更新机制能够更好地维持策略的稳定性。


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/038_Figure_16.jpg]]
*Figure 16: Ablation on token efficiency and pass@k accuracies with sampling temperature= 1. GRPO and the base models are less robust to temperatures*

### 失败模式与局限性

尽管BARL在数学推理任务上表现优异，但其有效性依赖于几个关键前提。首先，候选答案集合的质量和数量直接影响贝叶斯更新的效果——如果采样的候选答案不能覆盖真实答案或合理的错误方向，后验分布将无法有效引导策略切换。其次，BARL的进度奖励依赖于一个冻结的奖励模型$\pi_\phi$来计算答案概率变化；当该模型的校准度不足时，奖励信号可能引入噪声。此外，当前实现需要为每个时间步计算候选答案概率，虽然开销可控，但在超大模型或超长序列场景下可能成为计算瓶颈。论文还指出，尝试使用价值集成方法（如独立线性头或Bayesian LoRA）来估计后验加权值未能有效捕捉认知不确定性，因此当前方法依赖显式的候选答案采样和奖励匹配。

### 关键图表结论

- **Table 1**：BARL在三个模型规模和六个数学基准上均取得最高平均准确率，优势在1.5B和7B模型上尤为显著（+2.3个百分点）。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/007_Table_1.jpg]]
*Table 1: Mean and standard error of the accuracies over three independent training runs*

- **Figure 5**：BARL以更少的总令牌数实现更高的pass@k准确率，令牌效率优势随k增大而更加明显。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/011_Figure_5.jpg]]
*Figure 5: BARL achieves higher pass@k accuracies with fewer total numbers of tokens*

- **Figure 7**：BARL模型的CoT具有持续更高的贝叶斯状态-动作值，直接证明了更有效的探索和利用。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/016_Figure_7.jpg]]
*Figure 7: Ablation on how effective the CoTs explore and exploit, measured by the Bayesian values*

- **Figure 6**：反思频率与性能无强相关，BARL的优势来自在正确时机进行有效反思，而非简单增加反思次数。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/012_Figure_6.jpg]]
*Figure 6: Reflection freq. on GSM8K (dashed) and MATH (solid) problems*

- **Figure 4**：传统RL泛化失败，BARL通过假设消除发现真实MDP，且候选集提供更多先验知识时性能进一步提升。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_vuyk1fSaE4/figures/034_Figure_15.jpg]]
*Figure 15: Results of BARL fine-tuned on Llama-3.2-3B-Instruct. (Left) Training accuracy and (Middle) response length. (Right) Evaluation results*



## 方法谱系与知识库定位

### 问题根源：马尔可夫策略的反思盲区

传统强化学习（RL）在LLM推理训练中的核心瓶颈在于其优化目标天然排斥反思行为。给定单一真实MDP $M^*$，标准RL最大化 $\mathcal{J}_{M^*}(\pi)$，而该目标存在一个马尔可夫最优策略（**Theorem 4.1**）——该策略仅依赖当前状态 $s_t$ 做决策，对相同状态始终输出相同的动作分布。这意味着即使模型在推理中途发现矛盾，它也没有动机“回头”重新审视之前的步骤，因为策略定义本身就禁止了这种状态依赖历史的行为。

BARL将这一洞察形式化为**反思探索**的严格定义（**Definition 3.2**）：当策略在相同潜在状态下输出不同的动作分布时，才构成反思行为。传统RL训练得到的策略不满足此条件，因此反思不会涌现；即便在训练中通过试错偶然出现，部署时也缺乏持续激励。

### 从单点优化到分布鲁棒：贝叶斯RL的范式转换

BARL的核心改动是将优化目标从单一MDP的期望回报替换为后验MDP分布上的贝叶斯期望回报：

$$\mathcal{I}(\pi) = \mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|\mathcal{D})} \left[ \mathcal{I}_{\mathcal{M}}(\pi) \right]$$

这一转换的因果效应体现在三个层面：

1. **策略梯度中的值函数替换**：传统策略梯度使用 $Q_{M^*}^{\pi}$，而BARL使用后验加权值 $\mathbb{E}_{\mathcal{M} \sim p(\mathcal{M}|h_t)}[Q_{\mathcal{M}}^{\pi}(h_t, a_t)]$（**公式5.1**）。这使梯度信号同时编码了“当前轨迹在哪些MDP假设下是合理的”这一信念信息。

2. **奖励信号的密度化**：传统RL仅依赖最终结果验证器奖励，BARL引入进度奖励（**公式3.2**）——每个推理步骤的奖励等于添加该步骤后模型对正确答案概率的增量。这为中间步骤提供了即时反馈，使贝叶斯更新有足够的信息量。

3. **Q值估计的信念加权机制**：BARL通过自归一化重要性采样对候选MDP集合进行加权（**公式5.4**），权重由两项乘积构成：状态条件下的答案概率 $\pi_\theta(y_{s_0}^{\mathcal{M}_i} \mid s_t + </\mathrm{think}>)$（模型置信度）和奖励一致性惩罚 $\prod_{t'} \exp(-\beta |r_{t'} - r_{\mathcal{M}_i}(s_{t'}, a_{t'})|)$。当某假设MDP预测的奖励与观察到的奖励持续不一致时，其权重被指数级压低，策略自然切换至其他假设——这为“何时反思”提供了原则性信号。

### 与基线方法的结构性差异

| 方法 | 优化目标 | 值函数 | 奖励信号 | 反思机制 |
|------|----------|--------|----------|----------|
| **GRPO** (Guo et al., 2025) | 单一MDP下分组相对策略优化 | $Q_{M^*}^{\pi}$ | 仅结果验证器 | 无，策略为马尔可夫 |
| **Progress** (Qu et al., 2025) | 单一MDP + 前进奖励 | $Q_{M^*}^{\pi}$ | 答案概率变化 + 结果奖励 | 奖励密度提升但无信念更新 |
| **BARL** | 后验MDP分布上的贝叶斯期望回报 | $\mathbb{E}_{p(\mathcal{M}|h_t)}[Q_{\mathcal{M}}^{\pi}]$ | 进度奖励 + 结果奖励 + 奖励一致性惩罚 | 通过假设消除驱动策略切换 |

**GRPO**和**Progress**都在单一MDP框架内运作，其策略梯度不携带MDP不确定性信息。Progress虽然通过前进奖励提供了更密集的反馈，但它仍然优化一个固定的奖励函数，不随信念更新而变化。BARL的关键区别在于：后验加权Q值随轨迹展开动态变化，当某个候选答案的预测奖励与实际观察产生累积偏差时，该假设的贡献被自动压低，策略被引导至其他候选方向——这是一种内化的、原则性的探索-利用权衡。

### 适用边界与局限

**已验证的适用场景**：
- 数学推理任务（GSM8K, MATH, CollegeMath, Olympiad, AIME 2024, AMC 2023），在Qwen2.5-Math（1.5B/7B）和R1-Distill-Llama-8B上均一致优于基线
- 合成迁移任务中，当候选集提供更多先验知识时，BARL的泛化能力随之提升（**Figure 4**）

**已知局限**：
1. **计算开销**：虽然BARL声称开销较小，但仍需为每个时间步计算候选答案概率，对于超大模型（100B+）可能显著。论文未提供在70B以上模型的计算开销数据。
2. **后验近似方法受限**：论文尝试了价值集成方法（独立线性头、Bayesian LoRA）来估计后验加权值，但这些方法未能有效捕捉认知不确定性，因此当前实现必须依赖候选答案采样和奖励匹配——这限制了方法的可扩展性。
3. **候选集质量依赖**：贝叶斯更新的有效性取决于候选答案集合的质量和数量（$|\mathcal{M}|=5$），对于特定任务可能需要精心设计的先验。论文未系统研究候选集大小对性能的敏感性。
4. **任务范围狭窄**：当前评估仅限于数学推理。在更一般的LLM推理任务（如常识推理、多跳问答、代码生成）中的有效性尚未验证。

### 开放问题

1. **反思涌现的充分条件**：贝叶斯RL目标是否总能确保反思行为的涌现，还是依赖特定的奖励设计（如进度奖励）和先验分布？**Theorem 4.2**仅证明了存在不确定性自适应最优策略，但未保证梯度优化能收敛到该策略。

2. **奖励函数依赖性**：当前方法强依赖前进奖励函数 $\pi_\phi$ 提供中间反馈。如何在不依赖前进奖励函数的情况下实现类似的探索-利用权衡？这关系到方法能否推广到无可靠中间验证器的任务。

3. **跨模态与开放生成**：BARL的核心机制——维持MDP假设后验并通过奖励一致性进行假设消除——是否适用于多模态推理或开放式文本生成？这些场景中“正确答案”的定义可能模糊，候选答案的采样和评估需要重新设计。

4. **规模化挑战**：在更大规模的模型和数据集上，使用有限候选集（$|\mathcal{M}|=5$）近似贝叶斯后验是否仍然高效？后验坍塌或候选集代表性不足的风险如何量化？

5. **与搜索方法的融合**：BARL通过信念更新实现策略切换，本质上是一种内化的搜索机制。它与显式搜索方法（如树搜索、束搜索）之间是否存在互补性或替代关系？论文未对此进行讨论。

## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Markovian_Reflective_Exploration_via_Bayes_Adaptive_RL_for_LLM_Reasoning.pdf]]
