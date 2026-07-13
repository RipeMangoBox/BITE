---
title: "Random Policy Valuation is Enough for LLM Reasoning with Verifiable Rewards"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Random_Policy_Valuation_is_Enough_for_LLM_Reasoning_with_Verifiable_Rewards.pdf
project_link: null
code_link: null
openreview_forum_id: ujLgLz6QQa
aliases:
- RPVIELRVR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "用固定均匀随机策略的 Q 值替代迭代策略评估-改进循环，直接从 Q 值中推导最优策略。"
primary_logic: "在确定性树结构 MDP 中，均匀随机策略的 Q 值恰好编码了从当前状态-动作对出发，后续随机行动最终获得正确解的概率；因此，对 Q 值采用贪婪选择即可达到最优，而使用软最大化则能在保持性能的同时实现多样性。"
claims:
- "在确定性树结构 MDP 中，均匀策略的 Q 函数贪婪策略是最优的。"
- "在 tabular MDP 中，ROVER (greedy) 达到最优奖励但模式崩溃，而 ROVER (softmax) 覆盖了所有 4 种最优模式。"
- "ROVER 在 AIME24, AIME25, HMMT25 上 pass@1 提升 +8.2，pass@256 提升 +16.8。"
- "ROVER 在多样性上提升 +20.5%。"
---

# Random Policy Valuation is Enough for LLM Reasoning with Verifiable Rewards

> [!tip] 核心洞察
> 在确定性树结构 MDP 中，均匀随机策略的 Q 值恰好编码了从当前状态-动作对出发，后续随机行动最终获得正确解的概率；因此，对 Q 值采用贪婪选择即可达到最优，而使用软最大化则能在保持性能的同时实现多样性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 随机策略评估足以实现基于可验证奖励的 LLM 推理 |
| 英文题名 | Random Policy Valuation is Enough for LLM Reasoning with Verifiable Rewards |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ujLgLz6QQa) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ROVER |
| Dataset | AIME24, AIME25, HMMT25 (平均), Countdown (TinyZero), MATH500 (Llama3.1-8B-Instruct) |

> [!tip] 效果简介
> - AIME24, AIME25, HMMT25 (平均) 上，Pass@1 为 ROVER (Qwen3-8B)，对比 最佳基线 (GRPO)，变化 +8.2。
> - AIME24, AIME25, HMMT25 (平均) 上，Pass@256 为 ROVER (Qwen3-8B)，对比 最佳基线，变化 +16.8。
> - Countdown (TinyZero) 上，测试成绩 为 ROVER，对比 GRPO (最高基线)，变化 达到最高上限性能，多样性显著优于 GRPO。

## 概要

当前基于可验证奖励的 LLM 推理（RLVR）方法，如 PPO 和 GRPO，普遍沿用经典强化学习中的广义策略迭代（GPI）框架，通过迭代的策略评估与策略改进来优化模型。然而，数学推理任务本质上对应一个**确定性树结构 MDP**，其转移是确定性的，且仅在终止状态获得二元奖励。现有方法忽视了这一简化特性，导致训练不稳定、多样性崩溃，并依赖大量启发式技巧。

本文的核心发现是：在确定性树结构 MDP 中，**均匀随机策略的 Q 值恰好编码了从当前状态-动作对出发、后续随机行动最终获得正确解的概率**。基于这一洞察，作者提出 **ROVER**，完全摒弃迭代 GPI，转而**对固定的均匀随机策略进行单次 Q 值评估，并直接从该 Q 值中推导策略**：贪婪选择即可达到最优，而软最大化采样则能在保持性能的同时实现多样性。ROVER 利用 LLM 自身的对数概率差进行 Q 函数内在参数化，无需额外的价值网络。

实验结果表明，ROVER 在 AIME24、AIME25、HMMT25 上平均 pass@1 提升 **+8.2**，pass@256 提升 **+16.8**，多样性提升 **+20.5%**，且训练过程更轻量、更稳定。



### LLM 推理中的可验证奖励强化学习

基于可验证奖励的强化学习（RLVR）已成为提升大语言模型推理能力的核心范式。其基本流程为：模型针对给定问题生成完整推理链，仅在最终答案处获得二元奖励信号（正确为 1，错误为 0），随后通过强化学习更新模型参数。数学推理任务天然适配这一范式——答案的正确性可被自动验证，无需人工标注。

从 MDP 视角审视，LLM 数学推理的 RLVR 过程可形式化为一个**有限时域马尔可夫决策过程**，其状态为当前已生成的 token 序列，动作为从词汇表中选择下一个 token。该 MDP 具有两个关键的结构特性：**转移是确定性的**——给定当前状态和动作，下一状态唯一确定；**状态空间形成树结构**——每个状态-动作对仅通向一个后继状态，不存在合并路径。此外，奖励信号仅在终止状态给出，且为二元值。

### 现有方法的瓶颈：GPI 框架下的训练不稳定与多样性崩溃

当前主流的 RLVR 方法——如 **GRPO**（Shao et al., 2024）、**DAPO**（Yu et al., 2025）和 **REINFORCE++**（Hu et al., 2025a）——均建立在广义策略迭代（GPI）框架之上。GPI 交替进行策略评估与策略改进：先估计当前策略的价值函数或优势函数，再据此更新策略以提升期望奖励。

然而，在 LLM 推理场景中，GPI 框架暴露出若干系统性缺陷：

1. **训练不稳定**：策略梯度方法需要估计优势函数，而二元终止奖励导致的高方差使得训练过程高度敏感。为缓解此问题，GRPO 引入了基于组的标准差归一化，DAPO 采用了更高的裁剪上界（$\epsilon_{low}=0.2, \epsilon_{high}=0.28$），但这些启发式技巧增加了方法复杂性和调参负担。

2. **多样性崩溃**：GPI 的迭代改进天然倾向于将概率质量集中到少数高奖励路径上，导致策略的熵快速下降。为对抗这一趋势，现有方法不得不引入 KL 惩罚或重要性采样裁剪，但效果有限——策略仍会过早收敛到单一或极少数推理模式，丧失了探索不同解题策略的能力。

3. **额外模型开销**：部分方法需要额外的价值网络或奖励模型来辅助训练，增加了计算和工程复杂度。

### 核心洞察：确定性树结构 MDP 中的简化机会

本文的关键观察是：现有方法**忽视了 LLM 数学推理 MDP 的特殊结构所带来的简化可能性**。在确定性树结构 MDP 且仅有二元终止奖励的条件下，策略评估与策略改进的交替循环并非必要。具体而言：

- **均匀随机策略的 Q 值具有特殊含义**：在树结构 MDP 中，从状态 $s$ 执行动作 $a$ 后，若后续所有动作均按均匀随机策略选择，则 $Q^{\pi_u}(s, a)$ 恰好等于从 $(s, a)$ 出发最终获得正确解的概率。这一概率天然编码了每个动作的“正确性潜力”。

- **最优策略可直接从均匀 Q 值导出**：由于 Q 值直接反映正确性概率，对 $Q^{\pi_u}$ 采取贪婪选择即可得到最优策略——无需迭代改进，无需优势估计，无需 KL 正则。

- **软最大化天然平衡质量与多样性**：对 $Q^{\pi_u}$ 应用 softmax 算子 $\pi_s(a|s) = \frac{\exp(Q^{\pi_u}(s,a)/\rho)}{\sum_{a'}\exp(Q^{\pi_u}(s,a')/\rho)}$ 进行动作采样，可在保持高正确率的同时覆盖多种最优推理模式，无需额外的熵正则项。

### ROVER 的设计动机

基于上述洞察，本文提出 **ROVER**（**R**andom P**o**licy **V**aluation for LLM R**e**asoning with Verifiable **R**ewards），其核心思想是：**用对固定均匀随机策略的单次 Q 值评估，替代 GPI 的迭代评估-改进循环**。ROVER 的设计遵循三条原则：

1. **极简性**：仅需估计均匀策略的 Q 值，无需策略梯度、无需价值网络、无需 KL 惩罚。
2. **内在参数化**：利用 LLM 自身的对数概率差 $Q(s_t, a_t) = \rho (\log \pi_\theta(a_t|s_t) - \log \pi_{\theta_{old}}(a_t|s_t))$ 来参数化 Q 函数，消除额外模型。
3. **天然多样性**：通过 softmax 采样机制，在不牺牲性能的前提下维持策略的探索能力和推理多样性。

### 问题定位：方法谱系中的空白

在 RLVR 方法谱系中，现有工作可大致分为两类：一类是策略梯度方法（PPO/GRPO 及其变体），依赖优势估计和迭代改进；另一类是偏好优化方法（DPO 等），依赖成对比较数据。ROVER 开辟了第三条路径——**随机策略评估路径**，它既不需要策略梯度的高方差估计，也不需要偏好数据的标注成本，而是直接从 MDP 的结构特性中推导最优行为。这一方法论上的简化，使得 ROVER 在训练效率、稳定性和多样性三个维度上同时获得提升。



## 核心方法与创新机理

ROVER 的核心创新在于**重新审视了 LLM 数学推理中 RLVR 任务的 MDP 结构**，并据此提出了一种比当前主流方法（PPO/GRPO）更简单、更稳定且天然保持多样性的训练范式。

### 1. 从迭代 GPI 到单次均匀策略评估

当前 RLVR 方法（如 GRPO、DAPO、REINFORCE++）普遍遵循广义策略迭代（GPI）框架：交替进行策略评估（通常通过优势函数估计）和策略改进（通过梯度更新）。然而，LLM 数学推理任务具有一个被忽视的关键特性：其 MDP 是**确定性的树结构**，且奖励为**二元的终止奖励**（正确/错误）。

ROVER 的理论核心是证明了在此类 MDP 中，**最优策略可以直接从固定的均匀随机策略的 Q 值中推导出来，无需迭代的策略改进循环**。具体而言，均匀随机策略 $\pi_u$ 的 Q 值 $Q^{\pi_u}(s,a)$ 恰好编码了“从当前状态-动作对出发，后续采取随机行动最终获得正确解的概率”。因此，对 $Q^{\pi_u}$ 采用贪婪选择即可达到最优策略（Theorem 1），从而将 RLVR 简化为对均匀策略的**单次策略评估**。

| 策略评估方式 | 基线方法（GRPO/PPO） | ROVER |
|---|---|---|
| 评估对象 | 当前策略（迭代改进） | 固定均匀随机策略（单次评估） |
| 评估算子 | 优势函数（组优势/GAE） | 均值算子（贝尔曼更新） |
| 是否需要迭代 GPI | 是 | 否 |

### 2. 从 KL 惩罚到软最大化天然多样性

传统方法为维持策略多样性，依赖 KL 散度惩罚与重要性采样裁剪，但这些机制在实际训练中常导致**熵崩溃**（entropy collapse），使策略过早收敛到单一解题模式。

ROVER 的多样性机制源于对均匀策略 Q 值的**软最大化采样**：

$$\pi_s(a \vert s) = \frac{\exp(Q^{\pi_u}(s, a) / \rho)}{\sum_{a'} \exp(Q^{\pi_u}(s, a') / \rho)}$$

该策略以温度参数 $\rho$ 控制探索-利用权衡：$\rho \to 0$ 时退化为贪婪策略，$\rho > 0$ 时按 Q 值的相对大小进行概率采样。理论分析表明，软最大化策略的价值下界为：

$$V^{\pi_s}(s_0) \geq R \left( 1 - \sum_{s \in P} Pr^{\pi_s}(s|s_0) \frac{N(s)}{N(s) + \exp(\max_a Q^{\pi_u}(s, a) / \rho)} \right)$$

该下界表明随着 $\rho \to 0$，性能差距消失。在表格化 MDP 实验中（Figure 5），ROVER (softmax) 成功覆盖了全部 4 种最优解题模式，而 Q-learning 和 ROVER (greedy) 均收敛到单一模式。

| 探索与多样性机制 | 基线方法（GRPO/PPO） | ROVER |
|---|---|---|
| 机制 | KL 惩罚 + 重要性采样裁剪 | 软最大化采样（无额外正则项） |
| 熵变化趋势 | 快速下降，易崩溃 | 温和下降，保持较高熵 |
| 多样性表现 | 模式单一（Countdown 仅 3 种解） | 模式丰富（Countdown 17 种解） |

### 3. 从额外价值网络到内在 Q 函数参数化

传统 RL 方法通常需要额外的价值网络或优势估计器来估计状态/动作价值。ROVER 利用 LLM 自身的对数概率差进行**内在参数化**：

$$Q(s_t, a_t) = \rho \big( \log \pi_\theta(a_t|s_t) - \log \pi_{\theta_{old}}(a_t|s_t) \big)$$

该设计以旧策略 $\pi_{\theta_{old}}$ 为基线，天然保持训练稳定性，且无需引入额外网络参数。训练损失为当前 Q 值与目标 Q 值（以均值算子生成）的均方误差：

$$\mathcal{L}_{\text{ROVER}} = \frac{1}{\sum_{i=1}^{n} |y_i|} \sum_{i=1}^{n} \sum_{t=0}^{|y_i|-1} \| Q(a_t|s_t), \mathbf{sg}[\hat{Q}(a_t|s_t)] \|^2$$

### 4. 从标准差归一化到均值中心化

GRPO 使用组内标准差进行优势归一化，而 ROVER 仅采用**均值中心化奖励**：

$$\tilde{r}(x, y_i) = r(x, y_i) - \frac{1}{n} \sum_{i=1}^{n} r(x, y_i)$$

该设计简化了奖励处理流程，避免标准差估计引入的额外方差，并将中心化奖励广播到每个 token 以提升训练效率。

### 创新总结

ROVER 的四个 changed slots 共同构成了一个**更轻量、更稳定、多样性更强**的 RLVR 框架：它从 MDP 结构特性出发，用单次均匀策略评估替代迭代 GPI，用软最大化天然保持多样性，用内在参数化消除额外网络，用均值中心化简化奖励处理。在 AIME24/25 和 HMMT25 上，ROVER 以相同的默认超参数（$\rho=1$）实现了 pass@1 提升 +8.2、pass@256 提升 +16.8、多样性提升 +20.5% 的显著增益。



![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/006_Figure_3.jpg]]
*Figure 3: Illustration of ROVER (greedy)*

ROVER 的整体 pipeline 建立在一个核心洞察之上：在 LLM 数学推理所对应的确定性树结构 MDP 中，最优策略可以直接从**固定均匀随机策略的 Q 值**中导出，而无需传统的迭代策略评估-改进循环。基于这一洞察，ROVER 将整个训练流程组织为三个紧密耦合的模块。

### 模块一：采样与奖励中心化

对于每个输入提示 $x$，ROVER 首先从旧策略 $\pi_{\theta_{old}}$ 中采样 $n$ 个完整回答 $\{y_i\}_{i=1}^n$，并获取对应的二元终止奖励 $r(x, y_i)$。随后，对这些奖励进行**均值中心化**处理：

$$\tilde{r}(x, y_i) = r(x, y_i) - \frac{1}{n} \sum_{i=1}^{n} r(x, y_i)$$

该中心化奖励仅减去组内均值，**不使用标准差归一化**，这与 GRPO 的组优势估计形成鲜明对比。中心化后的奖励被广播到对应回答的每一个 token，作为后续 Q 值计算的信号源。

### 模块二：Q 值计算与目标生成

这是 ROVER 区别于所有策略梯度方法的核心模块。ROVER 采用一种**内在参数化**方案，将 Q 函数直接与 LLM 自身的参数 $\theta$ 绑定：

$$Q(s_t, a_t) = \rho \big( \log \pi_\theta(a_t|s_t) - \log \pi_{\theta_{old}}(a_t|s_t) \big)$$

其中 $\rho$ 为温度参数，旧策略 $\pi_{\theta_{old}}$ 作为基线以保持训练稳定性。这种参数化**完全消除了对额外价值网络或优势估计器的需求**。

目标 Q 值 $\hat{Q}$ 的生成遵循均匀随机策略的贝尔曼更新，使用**均值算子**而非最大值算子进行策略评估：

$$\hat{Q}^{\pi_u}(s, a) \gets r(s, a) + \frac{1}{|A|} \sum_{a' \in \mathcal{A}} \hat{Q}^{\pi_u}(s', a')$$

在实现中，该更新被具体化为：对于每个 token 位置 $t$，目标 Q 值 $\hat{Q}(a_t|s_t)$ 由该 token 的广播中心化奖励加上其后继 token 的 Q 值均值构成。这一设计的理论保证来自 **Theorem 1**：在确定性树结构 MDP 中，均匀策略 Q 值的贪婪策略 $\pi_{greedy}$ 是最优的。直觉上，$Q^{\pi_u}(s,a)$ 恰好编码了从状态-动作对 $(s,a)$ 出发、后续采取均匀随机行动最终获得正确解的概率。

### 模块三：损失计算与优化

ROVER 的训练损失定义为当前 Q 值与目标 Q 值之间的均方误差，对目标 Q 值施加**停止梯度**（stop-gradient）：

$$\mathcal{L}_{\text{ROVER}} = \frac{1}{\sum_{i=1}^{n} |y_i|} \sum_{i=1}^{n} \sum_{t=0}^{|y_i|-1} \| Q(a_t|s_t), \mathbf{sg}[\hat{Q}(a_t|s_t)] \|^2$$

该损失通过 AdamW 优化器反向传播，仅更新策略参数 $\theta$。值得注意的是，整个 pipeline **不涉及任何 KL 惩罚、重要性采样裁剪或熵正则项**——多样性天然地从均匀策略 Q 值的软最大化采样中涌现。

### 输入输出流与关键设计选择

| 设计槽位 | 基线方法（GRPO/PPO） | ROVER |
|---------|---------------------|-------|
| 策略评估方式 | 迭代 GPI，组优势估计 | 固定均匀策略单次评估，均值算子 |
| 探索与多样性 | KL 惩罚 + 裁剪，易熵崩溃 | 软最大化采样，天然保持多样性 |
| Q 函数参数化 | 额外价值网络或优势估计器 | LLM 内在参数化（对数概率差） |
| 奖励归一化 | 组内标准差归一化 | 仅均值中心化 |

ROVER 在所有基准测试中使用相同的默认超参数（$\rho=1$），无需任务特定的调优。消融实验表明，温度 $\rho$ 控制探索与利用的权衡：$\rho=1$ 在所有任务上提供稳健性能，$\rho$ 过小导致过早利用和多样性降低，$\rho$ 过大则利用不足。系数 $\beta$ 在 0.2 至 1.0 的宽范围内对性能影响不敏感，表现稳定。



### 3.1 均匀策略 Q 值评估

ROVER 的核心操作是**对固定的均匀随机策略进行策略评估**，而非迭代执行策略评估与策略改进的 GPI 循环。在数学推理对应的确定性树结构 MDP 中，定义均匀随机策略为：

$$\pi_u(a|s) = \frac{1}{|\mathcal{A}|}$$

其 Q 值的贝尔曼更新使用**均值算子**替代标准期望算子：

$$\hat{Q}^{\pi_u}(s, a) \gets r(s, a) + \frac{1}{|\mathcal{A}|} \sum_{a' \in \mathcal{A}} \hat{Q}^{\pi_u}(s', a')$$

其中 $r(s,a)$ 为即时奖励，$\mathcal{A}$ 为动作空间，$s'$ 为下一状态。该更新的直觉含义是：**均匀策略的 Q 值编码了从当前状态-动作对出发，后续采取随机行动最终获得正确解的概率**。

基于此，可直接从 $Q^{\pi_u}$ 导出策略，无需迭代改进：

- **贪婪策略**：$\pi_{\text{greedy}}(s) = \arg\max_a Q^{\pi_u}(s, a)$，在确定性树结构 MDP 中被证明是最优的（Theorem 1）。
- **软最大化策略**：通过对 Q 值施加温度参数 $\rho$ 的 softmax 实现随机化：

$$\pi_s(a|s) = \frac{\exp(Q^{\pi_u}(s, a) / \rho)}{\sum_{a'} \exp(Q^{\pi_u}(s, a') / \rho)}$$

该策略的性能下界为：

$$V^{\pi_s}(s_0) \geq R \left( 1 - \sum_{s \in P} Pr^{\pi_s}(s|s_0) \frac{N(s)}{N(s) + \exp(\max_a Q^{\pi_u}(s, a) / \rho)} \right)$$

其中 $R$ 为最大累积奖励，$P$ 为从初始状态到终止状态的路径集合，$N(s)$ 为状态 $s$ 下的非最优动作数量。该下界表明：**当温度 $\rho \to 0$ 时，性能差距消失**，软最大化策略收敛到最优；当 $\rho > 0$ 时，策略在保持性能的同时实现多样性。

### 3.2 实用化 Q 函数参数化

在大语言模型的巨大动作空间中，直接维护 Q 值表不可行。ROVER 利用 LLM 自身的参数 $\theta$ 进行**内在 Q 函数参数化**，无需额外价值网络。核心定义是**相对 Q 函数**：

$$Q(s_t, a_t) = \rho \big( \log \pi_\theta(a_t|s_t) - \log \pi_{\theta_{\text{old}}}(a_t|s_t) \big)$$

其中 $\pi_\theta$ 为当前策略，$\pi_{\theta_{\text{old}}}$ 为采样时的旧策略，$\rho$ 为温度参数。该参数化以旧策略的对数概率作为基线，将 Q 值表达为当前策略与旧策略之间的对数概率差，从而保持训练稳定性。

### 3.3 低方差奖励中心化

为降低训练方差，ROVER 对每个提示的 $n$ 个采样回答进行**均值中心化奖励**处理：

$$\tilde{r}(x, y_i) = r(x, y_i) - \frac{1}{n} \sum_{i=1}^{n} r(x, y_i)$$

其中 $r(x, y_i)$ 为原始二元奖励（正确为 1，错误为 0），$\tilde{r}(x, y_i)$ 为中心化后的奖励。与 GRPO 使用标准差归一化不同，ROVER 仅进行均值中心化，避免了标准差估计引入的不稳定性。该中心化奖励随后被广播至生成序列的每个 token。

### 3.4 目标 Q 值构造与损失函数

ROVER 的训练流程包含三个关键步骤：

1. **采样与奖励中心化**：从旧策略 $\pi_{\theta_{\text{old}}}$ 采样 $n$ 个回答 $\{y_i\}$，计算中心化奖励 $\tilde{r}$。
2. **目标 Q 值构造**：对序列末端 token，目标 Q 值即为中心化奖励；对中间 token，使用均值算子递归构造：

$$\hat{Q}(a_t|s_t) = \tilde{r} + \frac{1}{|V|} \sum_{a_{t+1} \in V} Q(a_{t+1}|s_{t+1})$$

其中 $V$ 为词汇表，$Q(a_{t+1}|s_{t+1})$ 由相对 Q 函数参数化计算。

3. **损失函数**：最小化当前 Q 值与目标 Q 值的均方误差，目标 Q 值使用 stop-gradient 防止梯度流动：

$$\mathcal{L}_{\text{ROVER}} = \frac{1}{\sum_{i=1}^{n} |y_i|} \sum_{i=1}^{n} \sum_{t=0}^{|y_i|-1} \| Q(a_t|s_t), \mathbf{sg}[\hat{Q}(a_t|s_t)] \|^2$$

其中 $|y_i|$ 为第 $i$ 个回答的 token 长度，$\mathbf{sg}[\cdot]$ 表示 stop-gradient 操作。参数通过 AdamW 优化器更新。

### 3.5 关键消融结论

- **温度参数 $\rho$**：控制探索与利用的权衡。$\rho=1$ 在所有任务中无需任务特定调优即可提供稳健性能；$\rho$ 过小导致过早利用和多样性降低，$\rho$ 过大导致利用不足（Figure 8, Figure 21）。
- **系数 $\beta$**：损失函数中对应项的系数在 0.2 至 1.0 之间时，ROVER 性能保持稳定（Figure 13）。
- **与熵正则化的对比**：在 GRPO 中加入熵正则化虽增加熵，但性能下降；ROVER 则同时提升性能和熵（Table 9：ROVER Pass@1 11.10, entropy 0.055 vs GRPO+entropy Pass@1 9.31, entropy 0.020）。



## 实验与关键发现

### 核心性能对比

ROVER 在数学推理基准上展现出显著的质量与多样性双重优势。以 Qwen3-8B-Base 为基础模型，在 AIME24、AIME25、HMMT25 三个竞赛级数学任务上取平均，ROVER 的 Pass@1 达到 30.6，较最佳基线 GRPO 提升 **+8.2**；Pass@256 则达到 46.4，提升 **+16.8**（Table 1、Figure 9）。这一 Pass@k 随 k 增长而持续扩大的剪刀差，直接源于 ROVER 在训练中维持了更高的策略熵，从而保留了更多样化的正确推理路径（Figure 22）。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/019_Table_1.jpg]]
*Table 1: Pass@1 results across different methods on mathematical and O.O.D benchmarks. The highest and the second-best scores are shown in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/022_Figure_9.jpg]]
*Figure 9: pass@k of ROVER and baselines on Qwen3-8B-Base*

在 O.O.D 泛化方面，ROVER 同样表现突出：在 GPQA diamond 上取得 50.2 的 Pass@1，超过所有 RL 基线（Table 1）。在 MATH500 上以 Llama3.1-8B-Instruct 为基座，ROVER 的 avg@5 达到 67.8，相比 GRPO 的 59.0 提升 **+8.8**（Table 10）。

在工具使用场景中，ROVER 在通用 QA 和多跳 QA 上平均准确率达到 0.360，优于 Search-R1-base（GRPO）的 0.342；同时在 Bamboogle 基准上，回答的余弦距离从 0.042 提升至 0.065，表明生成了更多样的检索-推理策略（Table 2、Table 3）。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/027_Table_2.jpg]]
*Table 2: Performance comparison on General QA and Multi-hop QA benchmarks*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/028_Table_3.jpg]]
*Table 3: Diversity comparison evaluated on Bamboogle benchmark using cosine distance between agent responses*

### 多样性的因果机制

ROVER 的多样性增益并非来自显式正则项，而是其核心设计——对均匀随机策略 Q 值进行软最大化采样——的自然产物。Figure 10 的质量-多样性散点图显示，ROVER 在保持高 Pass@1 的同时，发现的独特解题策略数量较 GRPO 多出 **+6.8%**，较全部三个基线均值多出 **+20.5%**。在 Countdown 任务上，这一机制的作用更为直观：ROVER 发现了 17 种不同的正确算式，而 GRPO 仅产出 3 种（Figure 7）。

更重要的是，这种多样性直接转化为下游性能：Maj@k（多数投票）指标上，ROVER 在所有 k 值下均持续优于基线，且随 k 增大优势不衰减（Figure 11）。这表明 ROVER 生成的多样解之间具有互补性，而非低质量的噪声变体。

### 消融实验

**温度参数 ρ 的角色**。ρ 是 ROVER 中唯一控制探索-利用权衡的关键超参数。Figure 8 和 Figure 21 的消融显示：
- ρ=1（默认值）在所有任务上均提供稳健性能，无需任务特定调优；
- ρ 过小（如 0.001）导致过早收敛到单一模式，多样性和 Pass@k 均下降；
- ρ 过大（如 3.0）则利用不足，Pass@1 受损。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/018_Figure_8.jpg]]
*Figure 8: Performance under different ρ*

这一现象与理论分析一致：软最大化策略的性能下界随 ρ→0 趋近最优，但过小的 ρ 会牺牲多样性。

**损失系数 β 的鲁棒性**。Figure 13 表明，ROVER 的性能在 β 从 0.2 到 1.0 的宽范围内保持稳定，Pass@1 和 Pass@64 均无显著波动。这说明方法对超参数不敏感，易于复现。

**与熵正则化方法的对比**。Table 9 的关键对比揭示了 ROVER 的独特优势：在 GRPO 上显式添加熵正则化虽能提升熵（从 0.013 到 0.020），但 Pass@1 反而从 10.44 降至 9.31；而 ROVER 在熵达到 0.055 的同时，Pass@1 达到 11.10。这表明 ROVER 的熵增长是结构性的——它鼓励的是通往正确解的多条路径，而非无差别的随机探索。

### 训练效率与公平性

ROVER 在计算开销上具有显著优势。相较于 ProRLv2 使用 136k 训练数据和 16k GPU 小时，ROVER 仅需 40k 数据和 960 GPU 小时，却在性能上与之相当或更优。方法本身无需额外价值网络或奖励模型，所有实验使用统一的默认超参数（如 ρ=1），未进行任务特定的调优，保证了对比的公平性。

### 局限与适用边界

ROVER 的理论保证建立在**确定性树结构 MDP** 和**二元终止奖励**两个假设之上。当前实验验证集中在数学推理和工具使用等符合该假设的任务；对于存在随机状态转移或稠密、连续奖励的场景，均匀策略 Q 值的近似质量及其导出的策略最优性需要进一步验证。此外，实验主要在 3B-8B 参数规模上进行，训练步数相对有限（300-500 步），更大模型和更长训练周期下的行为仍有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/012_Figure_5.jpg]]
*Figure 5: (a) Illustration of the tabular MDP. (b)-(d) Comparison of learned Q-value maps. According to the Q-values, standard Q-learning with ϵ-greedy exploration converges to the mode ACD. ROVER (greedy) assigns the highest Q-values to optimal actions, but still converges to a single mode BDC due to its greedy behavior. ROVER is able to assign equally high Q-values to all optimal actions. (e) Q-learning and ROVER (greedy) converge to a single mode despite both being optimal, whereas ROVER successfully covers all 4 optimal modes*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/016_Figure_6.jpg]]
*Figure 6: Performance of our method and baselines over training on countdown tasks. The y-axis of (c) denotes the number of found distinct correct solution equations, averaged over 1024 questions. Figure 7: ROVER successfully finds 17 diverse solution equations, while only 3 different equations are given by GRPO*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/040_Table_4.jpg]]
*Table 4: Summarization of MDP structures between different tasks, considering the discrete Atari task from traditional RL and the countdown task from RLVR. While traditional RL tasks have smaller spaces and shorter horizons, the underlying MDP structure can be much more complex than LLM RLVR tasks that feature deterministic, episodic, tree-structured MDPs (which have larger spaces and longer horizons and leverage a powerful pre-trained model that can navigate in the large space)*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/041_Table_5.jpg]]
*Table 5: Results of DeepSeek-R1-Distill-Qwen-1.5B on typical math competition tasks. The high and the second-best scores are shown in bold and underlined, respectively*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/042_Table_6.jpg]]
*Table 6: Default hyperparameters for RL training*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_ujLgLz6QQa/figures/043_Table_7.jpg]]
*Table 7: Default hyperparameters for evaluation*



## 定位与知识库关联

### 1. 对 RLVR 范式的结构性简化

当前主流的 LLM 推理强化学习（RLVR）方法——包括 PPO、**GRPO**（Shao et al., 2024）、**DAPO**（Yu et al., 2025）和 **REINFORCE++**（Hu et al., 2025a）——均建立在广义策略迭代（GPI）框架之上，即交替进行策略评估与策略改进。这些方法在数学推理任务中面临共同瓶颈：训练不稳定、策略熵崩溃导致多样性丧失，以及为维持训练而引入的大量启发式技巧（如 KL 惩罚、重要性采样裁剪、组优势归一化等）。

ROVER 的核心突破在于识别出数学推理 RLVR 所对应的 MDP 具有两个关键简化特性：
- **确定性树结构转移**：从提示到回答的生成过程构成一棵确定性的轨迹树；
- **二元终止奖励**：最终答案要么正确（1），要么错误（0）。

基于这两个特性，论文证明了一个反直觉的结论：**最优策略可以直接从固定的均匀随机策略的 Q 函数中恢复，无需迭代的 GPI 循环**（Theorem 1）。这意味着 ROVER 将 RLVR 从一个策略迭代问题降维为单次策略评估问题。

### 2. 与具体基线方法的关键差异

| 设计维度 | GRPO / DAPO / REINFORCE++ | ROVER |
|---------|--------------------------|-------|
| 策略评估方式 | 迭代 GPI，使用组优势函数估计 | 对固定均匀随机策略进行单次评估，使用均值算子计算 Q 值 |
| 探索与多样性机制 | KL 惩罚 + 重要性采样裁剪，易导致熵崩溃 | 对均匀策略 Q 值进行软最大化采样，天然保持多样性，无需额外正则项 |
| Q 函数参数化 | 额外价值网络或优势估计器 | 利用 LLM 自身的对数概率差进行内在参数化：$Q(s_t, a_t) = \rho (\log \pi_\theta - \log \pi_{\theta_{\text{old}}})$ |
| 奖励归一化 | 基于组的标准差优势归一化（GRPO） | 仅进行均值中心化，不使用标准差归一化 |

**与 GRPO 的本质区别**：GRPO 通过组内相对比较来估计优势函数 $A_t = \frac{r_i - \text{mean}(r)}{\text{std}(r)}$，这本质上是在进行策略改进。ROVER 则完全放弃了优势估计和策略改进步骤，转而直接估计均匀策略的 Q 值，然后通过贪婪或软最大化从中推导策略。这种简化消除了 GRPO 中标准差归一化带来的训练不稳定性和熵崩溃问题。

**与 DAPO 的对比**：DAPO 通过提高裁剪上界来缓解 PPO 的保守性，试图保持更多探索，但这是一种间接的修补。ROVER 从第一性原理出发，通过软最大化采样直接控制探索-利用权衡，无需裁剪机制。

**与 REINFORCE++ 的对比**：REINFORCE++ 是 REINFORCE 的改进版，仍属于策略梯度方法，依赖采样回报进行策略更新。ROVER 则完全避开了策略梯度的高方差问题，采用基于 Q 值回归的确定性更新。

### 3. 理论适用边界

ROVER 的理论保证建立在以下假设之上：

1. **确定性树结构 MDP**：状态转移是确定性的，且轨迹形成树结构（无环、无共享子节点）。这适用于数学推理中从提示到答案的逐步生成过程，但不适用于存在随机环境交互或轨迹合并的场景。

2. **二元终止奖励**：奖励仅在轨迹终止时给出，且只有 0/1 两种取值。这适用于答案可验证的数学问题，但不适用于部分正确奖励或过程奖励的场景。

3. **均匀策略 Q 值的无偏估计**：在实际实现中，由于 LLM 词汇表巨大，无法对每个 token 进行穷举估值。ROVER 通过采样近似和内在参数化来规避此问题，但近似误差在大词汇表和超长推理链下的累积效应尚不明确。

### 4. 已知局限

- **MDP 假设的泛化性**：在奖励更复杂（如连续奖励、过程奖励）或存在随机转移的任务中，Theorem 1 的结论不再成立。论文在 Figure 16 中初步验证了 ROVER 在图结构 MDP 上仍能学到最优策略，但这超出了理论保证的范围，需要进一步分析。

- **模型规模与训练长度**：当前实验主要在 3B 至 8B 参数量的模型上进行，训练步数相对有限（如 Countdown 任务上 400 步即收敛）。ROVER 在更大规模模型（如 70B+）和更长期训练中的表现仍有待验证。

- **与 ProRLv2 的效率对比**：虽然 ROVER 在训练数据量（40k vs 136k）和 GPU 小时（960 vs 16k）上大幅优于 ProRLv2，但这一对比并非严格对照实验，受基础模型、提示集等混杂因素影响。

### 5. 开放问题

1. **非树结构 MDP 的推广**：ROVER 能否推广到更一般的 MDP（如随机转移、图结构、连续动作空间）？需要做哪些理论或算法层面的修改？

2. **大规模词汇表下的估值精度**：在大规模词汇表和超长推理链下，均匀策略 Q 值的采样近似是否仍能保持无偏和稳定？是否存在系统性偏差？

3. **多样性增益的下游转化**：ROVER 的多样性增益（+20.5%）能否可靠地转化为下游工具使用、代码生成等任务的性能提升？论文在工具使用 QA 上仅观察到 +1.8% 的准确率提升，多样性向性能的转化效率仍需深入理解。

4. **与离线 RL 和偏好优化的结合**：能否将均匀策略估值的思想与现有的离线 RL 或直接偏好优化（DPO）方法相结合，以处理无明确二元奖励的场景？

5. **温度参数 ρ 的理论最优性**：论文通过实验表明 ρ=1 在多个任务上提供稳健性能，但缺乏对 ρ 最优值的理论刻画。软最大化策略的性能下界（Theorem 2）表明当 ρ→0 时性能差距消失，但实际中 ρ 过小会导致多样性崩溃，这一矛盾需要更精细的理论分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/Random_Policy_Valuation_is_Enough_for_LLM_Reasoning_with_Verifiable_Rewards.pdf]]
