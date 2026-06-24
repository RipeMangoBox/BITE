---
title: "Reducing Belief Deviation in Reinforcement Learning for Active Reasoning of LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reducing_Belief_Deviation_in_Reinforcement_Learning_for_Active_Reasoning_of_LLM_Agents.pdf
openreview_forum_id: r8hzDA3pUY
aliases:
- TTBTT
- RBDRLARLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在检测到轨迹进入BTR时进行早期截断，消除无信息尾部效应，从而保留有效前缀的信用分配，减少梯度偏差。"
primary_logic: "信念陷阱导致信用分配逆转，截断未提供信息的尾部可以显著改善策略优化。"
claims:
- "T3通过截断轨迹抑制无信息尾部效应"
- "T3检测进入BTR并停止轨迹"
- "T3在多个任务上带来最高30点的性能提升"
- "T3减少令牌消耗高达34%"
---

# Reducing Belief Deviation in Reinforcement Learning for Active Reasoning of LLM Agents

> [!tip] 核心洞察
> 信念陷阱导致信用分配逆转，截断未提供信息的尾部可以显著改善策略优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 降低LLM智能体主动推理强化学习中的信念偏差 |
| 英文题名 | Reducing Belief Deviation in Reinforcement Learning for Active Reasoning of LLM Agents |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=r8hzDA3pUY); [GitHub](https://github.com/unimpor/T3) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | T3 (Truncating Belief-Trapped Trajectories) |
| Dataset | CircuitDecoding (CD), SituationPuzzles (SP), GuessNumbers (GN) |

> [!tip] 效果简介
> - CircuitDecoding (CD) 上，EM 为 77.83 (PPO+T3)，对比 61.67 (PPO)，变化 +16.2。
> - SituationPuzzles (SP) 上，F1-word 为 36.85 (PPO+T3)，对比 28.77 (PPO)，变化 +8.1。
> - SituationPuzzles (SP) 上，F1-char 为 81.50 (PPO+T3)，对比 74.56 (PPO)，变化 +6.9。

## 概述

LLM智能体在主动推理任务中需要与环境进行多轮交互，通过提问或查询逐步缩小关于隐藏状态的信念空间。然而，由于LLM的信念更新机制并非完美的贝叶斯推理，智能体在多轮交互后会逐渐进入**信念陷阱区域（Belief-Trap Region, BTR）**——一个信念不再收缩、动作丧失信息增益的认知停滞区。此时，轨迹尾部产生的动作不再提供有效信息，却仍参与强化学习的信用分配，导致优势估计产生系统性负向漂移，策略梯度被污染，优化陷入不稳定。

针对这一瓶颈，本文提出 **T³（Truncating Belief-Trapped Trajectories）**，一种简单而有原则的方法：在训练过程中检测轨迹是否进入BTR，一旦满足截断条件即提前终止轨迹，仅保留信息丰富的前缀用于信用分配。T³的核心洞察在于，**信念陷阱导致信用分配逆转，截断无信息尾部可以显著减少梯度偏差，使学习信号集中于真正有信息量的动作**。

T³作为一个轻量级包装器，可无缝集成到PPO、GRPO、GSPO等主流策略优化算法中。在CircuitDecoding、SituationPuzzles、GuessNumbers、PreferenceEstimation、MovieRecommendation五个主动推理任务上，T³带来最高**41点**的绝对性能提升（GSPO+T³在MovieRecommendation上），同时将令牌消耗降低**高达34%**。方法在分布外场景下仍持续有效，且在不同模型规模（3B/7B/14B）和架构（Qwen/Llama/DeepSeek-distilled）上均表现稳健。

## 背景与动机

### 主动推理中的信念陷阱：核心瓶颈

LLM智能体在主动推理任务中面临一个根本性困境：智能体通过与环境的交互逐步更新对隐藏状态的内部信念，但当信念更新偏离贝叶斯最优时，会逐渐滑入**信念陷阱区域（Belief-Trap Region, BTR）**。在该区域内，智能体的动作不再提供有效信息——例如反复提出已被排除的假设、发出冗余查询或收到“未知”反馈——而错误的累积会导致强化学习的信用分配机制失真，策略优化变得不稳定且探索受限。

具体而言，给定真实隐藏状态 $s^\star$，定义势函数 $\Psi(b) := -\log b(s^\star)$ 衡量信念集中于真实状态的程度。LLM智能体的信念更新相对于贝叶斯更新的期望势函数差异为：

$$c_{\theta}(b_t) := \mathbb{E}_{a_t} \mathbb{E}_{o_t} \Big[ \Psi(B_{\theta}(b_t, a_t, o_t)) - \Psi(B^{\star}(b_t, a_t, o_t)) \Big]$$

当 $c_\theta(b_t) > 0$ 持续累积时，智能体进入BTR——一个吸收集，其中期望任务进展变为非正。一旦进入，后续动作的信用分配被污染，梯度估计产生系统性偏差。

### 信用分配逆转：从理论到实证

论文揭示了信念陷阱对RL信用分配的核心破坏机制。在标准GAE框架下，时刻 $t$ 的优势估计为：

$$\widehat{A}_t = \sum_{j=0}^{T-t-1} (\gamma \lambda)^j \delta_{t+j}$$

其中 $\delta_t = r_t + \gamma V_{t+1} - V_t$ 为TD误差。理论分析表明，当轨迹尾部进入BTR后，期望优势的上界为：

$$\mathbb{E}[\widehat{A}_t] \leq \gamma \left( S_{\mathrm{pre}}(t) - \kappa_V \rho_b S_{\mathrm{tail}}^{\ominus}(t) \right)$$

其中 $S_{\mathrm{tail}}^{\ominus}(t)$ 表示尾部无信息动作带来的负向漂移。这意味着：**前缀中的有效探索动作，其优势会被尾部无信息动作的负向信号所抵消甚至逆转**，导致RL优化方向错误。这一理论预测在实验中得到了验证（Figure 2(c)(d)），实证结果确认了优势漂移的存在。

### 现有RL方法的缺口

当前主流的LLM智能体RL训练方法——包括**PPO**（Schulman et al., 2017）、**GRPO**（Shao et al., 2024）和**GSPO**（Zheng et al., 2025）——均使用完整轨迹进行信用分配，未考虑信念陷阱导致的尾部污染问题。这些方法在主动推理任务中表现受限：直接推理的前沿模型（如o3-mini、Gemini-2.5-Pro）虽然强大，但缺乏任务特定的交互学习能力；而标准RL方法则因信用分配失真而难以稳定提升。

### 核心动机：截断尾部，保留有效前缀

本文的核心洞察是：**如果能在检测到轨迹进入BTR时进行早期截断，消除无信息尾部效应，就可以保留有效前缀的信用分配，显著减少梯度偏差**。形式化地，设 $\widehat{A}_t^{\mathrm{pre}}$ 为截断后的优势估计，理论分析表明：

$$\mathbb{E}[\widehat{A}_t^{\mathrm{pre}}] \geq \mathbb{E}[\widehat{A}_t] + \gamma \kappa_V \rho_b S_{\mathrm{tail}}^{\ominus}(t)$$

即早期截断能够消除尾部负向漂移，使优势估计更准确地反映前缀动作的真实贡献。基于此，论文提出T³方法，通过可观测的代理信号（如假设空间不再收缩、冗余查询等）检测BTR入口并触发截断，从而在不修改底层RL优化器的前提下，为PPO/GRPO/GSPO提供更可靠的信用分配信号。

## 核心创新

### 问题定位：信念陷阱与信用分配逆转

本工作揭示了一个此前未被系统刻画的关键瓶颈：LLM智能体在主动推理（Active Reasoning）中，因内部信念更新不完美，会逐渐滑入**信念陷阱区域（Belief-Trap Region, BTR）**。一旦进入BTR，智能体的后续动作不再提供有效信息——表现为假设空间不再收缩、产生冗余查询、或收到“未知”反馈——但传统的强化学习（RL）训练仍会对这些无信息尾部进行信用分配。

理论分析（Theorem 2）表明，这种无信息尾部会在优势估计中引入**负向漂移**：早期有效动作的优势被尾部噪声稀释甚至逆转，导致梯度估计偏差增大，策略优化不稳定且探索受限。简言之，**信念陷阱导致信用分配逆转**，这是现有RL方法在主动推理任务上表现受限的根本原因。

### 核心方法：T³——截断信念陷阱轨迹

针对上述瓶颈，本工作提出 **T³（Truncating Belief-Trapped Trajectories）**，一个原理简洁、即插即用的轨迹截断策略。其核心创新在于**changed slot**的精准设计：

**轨迹截断策略**：将“无截断，使用完整轨迹进行信用分配”替换为“根据代理信号早期截断轨迹”。具体而言，T³定义了一个截断条件（Definition 2）：当假设空间 $\mathcal{H}_t$ 在长度为 $k$ 的滑动窗口内持续不再收缩时，即

$$d(\mathcal{H}_{\tau}, \mathcal{H}_{\tau+1}) \leq \Delta_{\min} \quad \text{for all } \tau \in [t-k, t)$$

触发早期截断。截断后的轨迹仅保留进入BTR之前的有效前缀，信用分配（如GAE或组优势）仅在该前缀上计算，从而**消除无信息尾部效应**，保留有效前缀的干净学习信号。

### 方法管线

T³作为包装器（wrapper）集成于现有RL优化器之上，其管线由四个模块构成：

1. **信念陷阱检测器**：利用任务特定的可观测代理信号判断轨迹是否进入BTR。例如，在GuessNumbers和CircuitDecoding任务中，以候选集大小的缩减量 $|\mathcal{H}_\tau| - |\mathcal{H}_{\tau+1}|$ 作为细化度量；在SituationPuzzles中，以裁判返回“unknown”作为停滞代理信号；在PreferenceEstimation中，以智能体估计与真实偏好的相似度变化作为截断依据。

2. **早期截断器**：当满足T³条件时终止当前轨迹，丢弃尾部无信息步骤。

3. **信用分配模块**：在截断后的前缀上计算优势（GAE/组优势），避免尾部污染。

4. **策略优化器**：使用截断后的优势进行策略更新，兼容PPO、GRPO、GSPO等主流RL算法。

### 与基线方法的关键差异

相较于标准RL基线（PPO、GRPO、GSPO）使用完整轨迹进行信用分配，T³的**唯一改动**是引入基于信念停滞检测的早期截断。这一改动不修改奖励函数、不调整网络架构、不引入额外模型参数，仅改变训练时轨迹的有效长度。其有效性根植于理论保证（Corollary 1）：截断后的优势估计具有更低的偏差上界，从而提供更准确的梯度信号。

### 证据强度

- **理论支撑**：Assumption 1（更新误差线性增长）和Theorem 2（优势漂移）在Figure 2中得到了实证验证——T³显著衰减了早期token优势的负向漂移。
- **性能验证**：Table 1显示，T³在5个主动推理任务上为PPO带来最高+16.2点、为GRPO带来最高+30.1点、为GSPO带来最高+41.0点的性能提升，同时令牌消耗降低最高34%。
- **消融确认**：Table 3验证了窗口大小 $k$ 的截断策略优于随机截断和基于语义相似性的截断，排除了“截断本身即有益”的替代解释。
- **分布外泛化**：Table 2显示T³在OOD场景下仍持续提升性能，表明方法的鲁棒性。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/001_Figure_1.jpg]]
*Figure 1: Overall framework of $\mathbf { T } ^ { 3 }$ , where $\left( b _ { t } , a _ { t } , o _ { t } \right$) denote the agent’s internal belief, its chosen action, and the resulting feedback at turn t , respectively. By truncating belief-trapped trajectories, we prevent the agent from entering the belief-trap region (BTR) where credit assignment is contaminated in RL training, allowing learning signals to concentrate on genuinely informative actions. As a result, policy optimization becomes more stable and effective under complex active reasoning

T³（Truncating Belief-Trapped Trajectories）作为一个轻量级包装器，可嵌入到任意基于优势估计的策略优化算法（PPO、GRPO、GSPO）中。其核心流水线由四个模块构成，形成“检测—截断—分配—优化”的闭环。

### 流水线模块与数据流

1. **信念陷阱检测器**
   在每个交互轮次 $t$，智能体基于当前信念 $b_t$ 选择动作 $a_t$ 并接收反馈 $o_t$，随后更新信念至 $b_{t+1}$。检测器利用任务特定的可观测代理信号，判断轨迹是否已进入信念陷阱区域（Belief-Trap Region, BTR）。BTR 的形式化定义为：信念空间中的一个吸收子集，一旦进入，期望任务进展（以势函数 $\Psi(b) = -\log b(s^\star)$ 衡量）将不再改善，即 $\mathbb{E}[\Psi(b_{t+1}) \mid b_t \in \mathcal{R}_\theta] \ge \Psi(b_t)$（Definition 1）。检测的核心依据是 T³ 条件（Definition 2）：当假设空间 $\mathcal{H}_t$ 在长度为 $k$ 的滑动窗口内持续缺乏收缩——即连续 $k$ 步满足 $d(\mathcal{H}_\tau, \mathcal{H}_{\tau+1}) \le \Delta_{\min}$——则判定轨迹已陷入信念陷阱。

2. **早期截断器**
   当 T³ 条件触发时，截断器立即终止当前轨迹，保留从起点到截断点 $t_S$ 的前缀。该操作的理论依据来自 Theorem 2 与 Corollary 1：尾部无信息段产生的 TD 误差 $\delta_{t+j}$ 在 GAE 累积中引入负向漂移，导致早期信息性动作的优势估计被系统性低估。截断后的优势估计满足 $\mathbb{E}[\widehat{A}_t^{\text{pre}}] \ge \mathbb{E}[\widehat{A}_t] + \gamma \kappa_V \rho_b S_{\text{tail}}^{\ominus}(t)$，从而恢复对前缀动作的公正信用分配。

3. **信用分配模块**
   在截断后的前缀上计算广义优势估计（GAE）或组优势。GAE 的标准形式为 $\widehat{A}_t = \sum_{j=0}^{T-t-1} (\gamma \lambda)^j \delta_{t+j}$，其中 $\delta_t = r_t + \gamma V_{t+1} - V_t$。截断后，尾部无信息段的 $\delta$ 被排除，避免了信用逆转对前缀梯度的污染。

4. **策略优化器**
   使用截断后的优势信号驱动策略更新。以 PPO 为例，优化目标为 $\mathcal{T}_{\text{PPO}}(\theta) = \mathbb{E}\left[\frac{1}{|y|}\sum_t \min(w_t \widehat{A}_t, \,\text{clip}(w_t, 1-\epsilon, 1+\epsilon) \widehat{A}_t)\right]$，其中 $w_t$ 为新旧策略概率比。T³ 不修改该目标函数，仅改变输入的优势估计 $\widehat{A}_t$ 的计算范围。

### 输入输出与整体逻辑

- **输入**：LLM 策略 $\pi_\theta$、任务环境（POMDP）、截断窗口大小 $k$、最小进展阈值 $\Delta_{\min}$。
- **输出**：优化后的策略参数 $\theta$。
- **逻辑闭环**：智能体在环境中执行多轮交互，每轮产生动作-观测对 $(a_t, o_t)$。检测器实时监控假设空间的收缩程度；一旦满足 T³ 条件，轨迹被截断。截断后的前缀进入信用分配模块计算优势，最后交由策略优化器更新参数。随着训练推进，策略逐渐学会在进入 BTR 前终止无信息探索，使学习信号集中于真正推进任务进展的动作上。

Figure 1 直观对比了标准 RL 方法与 T³ 的差异：左侧的标准方法中，智能体在进入 BTR 后继续执行无信息动作（如重复猜测同一思路），导致尾部优势漂移和错误累积；右侧的 T³ 在检测到 $b_{t_S}$ 进入 BTR 时即行截断，赋予截断奖励 $R_{\text{cut}}$，使策略优化保持稳定有效。

## 核心模块与公式推导

### 关键模块

T³ 方法由四个核心模块构成，围绕“检测信念陷阱→早期截断→净化信用分配→策略优化”这一因果链条组织：

**信念陷阱检测器**。该模块利用任务特定的可观测代理信号，判断当前轨迹是否已进入信念陷阱区域（BTR）。其设计原则来自 Definition 2 的 T³ 条件：当假设空间 $\mathcal{H}$ 在长度为 $k$ 的滑动窗口内持续缺乏收缩时，判定已陷入 BTR。不同任务的代理信号实例化如下：
- **GuessNumbers / CircuitDecoding**：直接以候选集大小的缩减量作为精炼度量 $d(\mathcal{H}_\tau, \mathcal{H}_{\tau+1}) := |\mathcal{H}_\tau| - |\mathcal{H}_{\tau+1}|$。
- **SituationPuzzles**：以裁判返回“unknown”作为信息停滞的代理信号。
- **PreferenceEstimation**：以智能体估计向量与真实偏好向量的相似度变化 $\mathrm{Sim}(v_{\tau+1}, v^{\bar{\star}}) - \mathrm{Sim}(v_{\tau}, \bar{v^{\star}})$ 作为精炼信号，连续 $k=2$ 步为负时触发截断。

**早期截断器**。当检测器判定轨迹进入 BTR 时，立即终止当前轨迹，保留有效前缀。截断点 $t_S$ 之后的尾部交互（无信息查询、重复猜测等）被丢弃，从而消除尾部效应对信用分配的污染。

**信用分配模块**。在截断后的前缀上计算优势函数，避免尾部 TD 误差的负向漂移。论文使用广义优势估计（GAE）：

$$
\widehat{A}_t = \sum_{j=0}^{T-t-1} (\gamma \lambda)^j \delta_{t+j}
$$

其中 $\delta_t = r_t + \gamma V_{t+1} - V_t$ 为时序差分误差，$\gamma$ 为折扣因子，$\lambda$ 为 GAE 参数。截断后，优势估计仅累积到 $t_S$ 之前的步数，从而保留信息性动作的真实贡献。

**策略优化器**。T³ 作为包装器（wrapper）可嵌入 PPO、GRPO、GSPO 等标准策略优化算法。以 PPO 为例，其目标函数为：

$$
\mathcal{T}_{\mathrm{PPO}}(\theta) = \mathbb{E} \left[ \frac{1}{|y|} \sum_t \min \left( w_t \widehat{A}_t, \mathrm{clip}(w_t, 1-\epsilon, 1+\epsilon) \widehat{A}_t \right) \right]
$$

其中 $w_t$ 为新旧策略的概率比，$\epsilon$ 为裁剪阈值。T³ 通过提供净化后的 $\widehat{A}_t$，使策略梯度估计的偏差降低。

### 关键公式与变量含义

**Oracle 贝叶斯信念更新**（式 1）。给定动作 $a_t$ 和观测 $o_t$，按贝叶斯规则更新关于隐藏状态 $s$ 的信念分布：

$$
b_{t+1}^{\star}(s) := B^{\star}(b_t^{\star}, a_t, o_t) = \frac{O(o_t \mid s, a_t) b_t^{\star}(s)}{p_b(o_t \mid a_t)}
$$

其中 $O$ 为观测模型，$p_b$ 为归一化因子。该式定义了理想化的信念更新基准，用于衡量 LLM 智能体信念更新的偏差。

**真实锚定势函数**。衡量信念集中于真实状态 $s^{\star}$ 的程度：

$$
\Psi(b) := -\log b(s^{\star})
$$

$\Psi(b)$ 越小，表示信念越集中于真实状态，即认知进度越大。

**信念更新偏差**（式 2）。LLM 更新规则 $B_\theta$ 相对于贝叶斯更新 $B^{\star}$ 的期望势函数差异：

$$
c_{\theta}(b_t) := \mathbb{E}_{a_t} \mathbb{E}_{o_t} \Big[ \Psi(B_{\theta}(b_t, a_t, o_t)) - \Psi(B^{\star}(b_t, a_t, o_t)) \Big]
$$

$c_\theta(b_t)$ 量化了单步更新后 LLM 信念与最优信念之间的势函数差距，是信念陷阱形成的关键度量。

**T³ 截断条件**（Definition 2）。当假设空间在长度为 $k$ 的窗口内持续无显著收缩时触发截断：

$$
d(\mathcal{H}_{\tau}, \mathcal{H}_{\tau+1}) \leq \Delta_{\min} \quad \text{for all } \tau \in [t-k, t)
$$

其中 $d$ 为精炼度量，$\Delta_{\min} \geq 0$ 为最小进度阈值。该条件将 BTR 的“进度停滞”特征操作化为可检测的截断规则。

**优势漂移的截断修正**（Corollary 1 非正式）。设 $\widehat{A}_t^{\mathrm{pre}}$ 为在 $t_S$ 处截断后的优势估计量，则在 Theorem 2 假设下：

$$
\mathbb{E}[\widehat{A}_t^{\mathrm{pre}}] \geq \mathbb{E}[\widehat{A}_t] + \gamma \kappa_V \rho_b S_{\mathrm{tail}}^{\ominus}(t)
$$

其中 $\kappa_V$ 为值函数 Lipschitz 常数，$\rho_b$ 为 BTR 吸收概率，$S_{\mathrm{tail}}^{\ominus}(t)$ 为尾部负向贡献。该式表明早期截断可降低优势估计的负向偏差，从而改善梯度信号质量。

## 实验与分析

### 核心瓶颈：信念陷阱如何污染信用分配

LLM智能体在主动推理任务中遵循“提问—获取反馈—更新内部信念”的循环。当智能体对隐藏状态的估计偏离真实分布时，其后续动作的信息量递减，最终进入**信念陷阱区域（Belief-Trap Region, BTR）**——一个吸收集，在该区域内每一步的期望任务进展变为非正（Definition 1）。一旦陷入BTR，轨迹尾部产生的低质量动作和零信息反馈会通过GAE等信用分配机制反向传播，导致早期有效动作的优势估计被严重稀释（Theorem 2, Figure 2(c)(d)），策略梯度因此产生系统性偏差，优化停滞。

T³（Truncating Belief-Trapped Trajectories）的核心操作极其简单：**检测到轨迹进入BTR时即行截断，仅保留信息充分的前缀用于信用分配**。这一截断在理论上等价于消除优势估计中的负漂移项，使梯度更集中于真正推动任务进展的动作（Corollary 1）。

### 主实验结果：跨任务、跨RL算法的稳定增益

Table 1汇总了T³在五个主动推理任务上对三种RL基线（PPO、GRPO、GSPO）的性能提升。所有指标均按100分制缩放，↑表示绝对提升点数。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/006_Table_1.jpg]]
*Table 1: Main results across active reasoning tasks (all metrics are scaled by 100). ↑ indicates absolute improvement (in points) over the vanilla RL baseline. We report the average rank across all metrics*

**PPO + T³：**
- **CircuitDecoding (CD)**：EM从61.67提升至77.83，**+16.2点**。
- **SituationPuzzles (SP)**：F1-word从28.77提升至36.85（+8.1），F1-char从74.56提升至81.50（+6.9）。
- **GuessNumbers (GN)**：EM从91.62提升至93.98（+2.4）。
- **PreferenceEstimation (PE)**：Binary Sim从42.00提升至49.00（+7.0）。
- **MovieRecommendation (MR)**：EM从24.33提升至38.00（**+13.6**）。

**GRPO + T³：**
- **GN**：EM从61.26飙升至91.36，**+30.1点**，是单任务最大提升。
- **MR**：EM从12.00升至32.67（+20.7）。

**GSPO + T³：**
- **MR**：EM从14.67升至55.67，**+41.0点**，为全表最高绝对提升。
- **GN**：EM从96.04升至99.74（+3.7），逼近满分。

三个关键观察：
1. **T³作为外挂包装器**，对PPO/GRPO/GSPO均有效，说明其解决的问题（信念陷阱导致的信用分配失真）是RL训练中的共性故障，而非特定算法的缺陷。
2. **在基线表现越差的任务上，T³的提升越显著**。例如GRPO在GN上仅61.26，T³带来30.1点的飞跃；GSPO在MR上仅14.67，T³带来41.0点的质变。这符合理论预期：基线差意味着智能体更频繁地陷入BTR，截断的边际收益更大。
3. **训练动态**（Figure 3, Figure 4）显示，T³不仅提升最终奖励，还持续推动奖励曲线上升，而vanilla方法常在中后期停滞。同时，T³有效抑制了响应长度的无意义膨胀，令牌消耗降低最高达34%。

### 分布外泛化：T³的增益不限于训练分布

Table 2展示了OOD场景下的评估结果：
- **PE任务**：当参考集大小S从训练时的5扩大到10、15、20时，PPO+T³的Binary Sim始终优于vanilla PPO，且增益随S增大而扩大（S=20时领先12.7点）。
- **CD任务**：当候选电路数从5增至25时，PPO+T³的EM领先10.8点；当电路数量从2增至3时，领先15.0点。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/015_Table_2.jpg]]
*Table 2: Evaluations of $\mathbf { T } ^ { 3 }$ on out-of-distribution (OOD) scenarios of PE (Qwen-2.5-7B-Inst.) and CD (Qwen-2.5-14B-Inst.) tasks under the PPO algorithm*

这表明T³截断的并非特定任务模式，而是**通用的认知停滞信号**。在OOD场景中，智能体面临更复杂的假设空间，更容易陷入无效探索，T³的早期截断机制因此更加关键。

### 截断条件消融：窗口大小k的优越性

Table 3对比了三种截断策略在SP、CD、PE任务上的表现：
- **窗口大小k（T³默认）**：连续k步假设空间无收缩时截断。SP上k=5最优（F1-word 39.45），CD上k=4最优（EM 79.33），PE上k=2最优（Binary Sim 49.00）。所有k配置均优于不截断的vanilla基线。
- **语义相似度截断（Sim-α）**：当当前查询与历史查询的余弦相似度超过阈值α时截断。在SP和CD上表现弱于k策略，在PE上略优于k=2（Binary Sim 50.00 vs. 49.00），但整体不稳定。
- **随机截断（Rand-β）**：以概率β独立截断每一步。在所有任务上均显著弱于k策略，甚至在某些配置下低于vanilla基线，说明**盲目截断会破坏有效前缀的信用分配**。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/016_Table_3.jpg]]
*Table 3: Ablation Study of Truncation Conditions on the SP, CD, and PE tasks. Beyond the window size k as seen in Def. 2, we consider alternative truncation methods, described in α and β*

Figure 5进一步揭示了训练过程中截断比例的变化：k策略的截断率随训练逐步下降，表明策略确实学会了更高效的信息获取；而Sim-α的截断率波动较大，Rand-β保持恒定，均无法自适应地聚焦于真正的信念陷阱。

### 模型规模与架构的鲁棒性

Figure 6展示T³在3B/7B/14B三种规模及Qwen/Llama/DeepSeek-distilled三种架构上的性能增益。在所有配置下，PPO+T³的EM均高于vanilla PPO，且增益幅度在不同规模和架构间保持稳定（约5-15点），无明显的规模依赖或架构偏好。这印证了T³的原理性：信念陷阱是POMDP框架下的结构性故障，与模型容量或架构细节弱相关。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/022_Figure_6.jpg]]
*Figure 6: Effectiveness of $\mathbf { T } ^ { 3 }$ on different sizes (a, b) and types (c) of LLM architectures. The “Performance Gain” denotes the improvement of $\mathbf { T } ^ { 3 }$ compared to the vanilla RL method

### 失败模式与需人工验证的边界

1. **过度截断的风险**：Figure 9（附录）显示，当截断条件过于激进（假阳性率高）时，早期探索性动作的优势被削弱，性能反而下降。T³需要在保守性和有效性之间通过k和Δ_min进行权衡，当前最佳k值依赖任务级调参。

2. **代理信号的可获取性**：T³的截断条件依赖任务特定的可观测代理信号（如候选集大小缩减、法官反馈“unknown”）。在PE任务中，若无法获取真实偏好向量v*，基于自适应阈值的T³仍可超越oracle T³（Table 7, Binary Sim 50.67 vs. 49.00），但这一结论来自单一任务的特定设计，**其跨任务通用性需进一步验证**。

3. **理论假设的拟合偏差**：Assumption 1（更新误差下界线性增长）虽经Figure 2(a)(b)实证拟合，但其正斜率在不同任务上的显著性存在差异。若实际LLM行为偏离该假设，Theorem 2的漂移上界可能不再紧致，截断的理论保证弱化。**该点需结合附录C的完整拟合结果进行人工核实**。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_r8hzDA3pUY/figures/030_Figure_8.jpg]]
*Figure 8: Empirical verification of Theorem 2 and Corollary 1. (a-b) Without truncation, early-token advantages exhibit a clear negative drift, while $\mathbf { T } ^ { 3 }$ consistently elevates them across PE and CD tasks. (c) Longer uninformative tails (higher maximum interaction turns, from 6 to 15) cause stronger suppression of early advantages. (d) Stronger $\mathbf { T } ^ { 3 }$ truncation (smaller k) yields cleaner, less-biased early advantages

## 方法谱系与知识库定位

### 1. 问题定位：LLM智能体的信念陷阱与信用分配失效

T³（Truncating Belief-Trapped Trajectories）解决的核心瓶颈是：LLM智能体在主动推理（active reasoning）中，由于不完美的信念更新机制，会逐渐滑入**信念陷阱区域（Belief-Trap Region, BTR）**。一旦进入BTR，后续动作失去信息量，产生无信息尾部效应（uninformative tail effects），导致：

- **信用分配逆转**：强化学习的优势估计（advantage estimation）被尾部无信息动作污染，早期有信息动作的优势被系统性低估（即优势漂移，advantage drift）；
- **策略优化失稳**：梯度估计偏差增大，策略无法有效区分有信息与无信息动作；
- **探索受限**：模型陷入重复无效查询的循环，训练停滞。

该问题在POMDP框架下被形式化：LLM的信念更新算子 $B_\theta$ 与Oracle贝叶斯更新 $B^\star$ 之间存在期望势函数差异 $c_\theta(b_t)$，且该差异在高不确定性区域呈至少线性增长（Assumption 1），最终导致信念被吸收进BTR（Definition 1）。

### 2. 与基线方法的关系

T³并非一种独立的RL算法，而是作为**包装器（wrapper）**嵌入现有策略优化方法，通过轨迹截断修正信用分配偏差。

#### 2.1 策略优化基线的直接扩展

T³集成了三类主流策略优化方法：

- **PPO**（Schulman et al., 2017）：标准近端策略优化，使用GAE进行优势估计。T³在PPO的完整轨迹上检测BTR入口并截断，使GAE仅在截断后的前缀上计算，消除尾部污染。
- **GRPO**（Shao et al., 2024）：组相对策略优化，通过组内相对比较进行信用分配。T³截断后，组优势（group advantage）仅基于有信息前缀计算，避免组内尾部噪声的相互干扰。
- **GSPO**（Zheng et al., 2025）：组序列策略优化，进一步考虑序列结构。T³的截断保留了序列前缀的完整结构信息，同时消除尾部退化段。

T³对这三种方法的提升幅度差异显著：在GuessNumbers任务上，GRPO+T³提升30.1点（从61.26到91.36）；在MovieRecommendation上，GSPO+T³提升41.0点（从14.67到55.67）。这表明**基线方法的信用分配越依赖完整轨迹（如GSPO的序列建模），尾部污染的危害越大，T³的修正效果越显著**。

#### 2.2 与直接推理基线的对比

论文将T³增强的RL方法与前沿LLM的直接推理（direct inference）对比，包括**o3-mini**、**Gemini-2.5-Pro**和**Qwen-2.5-7B-Inst.**。在CircuitDecoding任务上，PPO+T³（77.83 EM）超越所有直接推理基线；在SituationPuzzles上，GRPO+T³（36.85 F1-word）同样优于直接推理。这验证了**RL训练配合信念陷阱截断可以超越单次推理的能力上限**。

#### 2.3 截断策略的消融对比

T³的截断条件（Definition 2）基于假设空间在窗口 $k$ 内的收缩停滞 $d(\mathcal{H}_{\tau}, \mathcal{H}_{\tau+1}) \leq \Delta_{\min}$。消融实验（Table 3）对比了三种替代方案：

- **随机截断（Rand-β）**：以概率 $\beta$ 独立截断每一步，缺乏对信息停滞的结构性检测，性能显著低于T³；
- **语义相似度截断（Sim-α）**：当当前查询与历史查询的余弦相似度超过阈值 $\alpha$ 时截断，虽能检测冗余提问，但无法感知假设空间的精细化程度，在CircuitDecoding上表现弱于T³（$k=4$）；
- **窗口大小 $k$ 的T³**：$k$ 过小导致假阳性截断（过早截断有信息的探索），$k$ 过大则延迟截断，最优 $k$ 因任务而异（SP: $k=5$，CD: $k=4$，PE: $k=2$）。

### 3. 适用边界

#### 3.1 任务结构依赖性

T³的截断检测器依赖于任务特定的代理信号（proxy signals）：

- **GuessNumbers / CircuitDecoding**：假设空间为候选集，精细化度量 $d$ 定义为候选集大小的缩减；
- **SituationPuzzles**：代理信号为裁判反馈中的"unknown"响应；
- **PreferenceEstimation**：代理信号为智能体估计与真实偏好的相似度变化；
- **MovieRecommendation**：类似地依赖推荐精度的变化。

这种任务特定实例化限制了T³的**即插即用通用性**。在不具备明确假设空间或可观测精细化信号的任务上（如开放式对话），T³需要额外的代理信号设计。

#### 3.2 截断的保守性-有效性权衡

过度截断（假阳性）会削弱早期探索性动作的优势（Figure 9），因为这些动作可能暂时未带来假设空间收缩，但对长期探索至关重要。T³通过窗口机制 $k$ 和最小进度阈值 $\Delta_{\min}$ 控制假阳性率，但最优参数需要任务级调优。

#### 3.3 理论假设的实践偏离

理论分析基于POMDP框架和信念更新误差的线性下界假设（Assumption 1）。虽然Figure 2(a)(b)在Qwen-2.5-7B和Qwen-2.5-32B上验证了该假设的经验拟合，但实际LLM的信念更新可能呈现更复杂的非线性模式，在极端分布偏移下该假设可能失效。

### 4. 局限性

1. **精确信念状态不可观测**：T³依赖代理信号而非真实信念状态，代理信号的噪声可能导致截断决策偏差。论文在PreferenceEstimation上验证了不依赖真实偏好的自适应阈值仍有效（附录D.3），但该结论的跨任务泛化性待验证。

2. **任务通用性受限**：当前截断检测器需针对每个任务单独设计代理信号，缺乏统一的跨任务检测机制。

3. **假阳性截断风险**：窗口大小 $k$ 和阈值 $\Delta_{\min}$ 的选择在保守性（保留探索）与有效性（消除尾部）之间存在张力，且最优参数可能随训练进程漂移。

4. **理论框架的简化**：POMDP建模假设动作-观测空间的离散性和信念更新的马尔可夫性，实际LLM推理中的长程依赖和语义漂移可能超出该框架的刻画能力。

### 5. 开放问题

1. **通用截断检测器设计**：如何构建不依赖任务特定结构的通用BTR检测器？可能的路径包括：利用LLM内部表征的不确定性度量（如熵、方差）、注意力模式的停滞检测、或基于学习的状态分类器。

2. **认知停滞的特征签名**：如何在隐藏状态空间中刻画"认知停滞"的通用特征签名，以支持跨任务的内部状态信号？这需要建立LLM推理停滞与POMDP信念陷阱之间的更精确映射。

3. **极端分布偏移下的表现**：T³在OOD场景（Table 2）中持续提升性能（PE: +12.7点，CD: +15.0点），但在更极端的分布偏移（如全新任务域、对抗性环境）下的鲁棒性尚未验证。

4. **截断策略的自适应优化**：能否将截断决策本身纳入元学习或在线自适应框架，使窗口大小 $k$ 和阈值 $\Delta_{\min}$ 随训练进程和任务特性自动调整？

5. **与推理时方法的协同**：T³关注训练阶段的信用分配修正，如何与推理时的搜索策略（如树搜索、自我验证）协同，形成"训练截断+推理扩展"的互补机制？

## 原文 PDF

![[paperPDFs/ICLR_2026/Reducing_Belief_Deviation_in_Reinforcement_Learning_for_Active_Reasoning_of_LLM_Agents.pdf]]
