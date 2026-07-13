---
title: "Sample More to Think Less: Group Filtered Policy Optimization for Concise Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sample_More_to_Think_Less_Group_Filtered_Policy_Optimization_for_Concise_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: UKOqoULbZS
aliases:
- GFPOG
- SMTLGFPOCR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "GFPO引入“分组过滤”机制：训练时增大采样组量G，根据长度或token效率等指标仅保留top-k响应（控制k/G比值），通过掩码将其余响应的优势设为零，从而直接抑制策略向冗长方向更新。"
primary_logic: "在训练时增加采样数量并进行选择性过滤，可以隐式地传递简洁性偏好，使得模型在推理时学会“少思考”，同时保持甚至提升准确率；保留比例k/G是控制长度降低幅度的核心调节杠杆。"
claims:
- "GFPO将GRPO的长度膨胀降低高达85%，在AIME 24/25、GPQA、Omni-MATH和LiveCodeBench等基准上维持统计无差异的准确率。"
- "降低保留比例k/G（增大G或减小k）即可线性地缩短响应长度，是控制冗长的关键因子。"
- "基于奖励/token效率的Token Efficiency过滤比单纯按长度过滤能更大幅度地削减长度，且仅增加约7%的训练时间。"
- "GFPO在分布外的代码基准LiveCodeBench上同样抑制了GRPO造成的长度膨胀，并有时提升准确率。"
---

# Sample More to Think Less: Group Filtered Policy Optimization for Concise Reasoning

> [!tip] 核心洞察
> 在训练时增加采样数量并进行选择性过滤，可以隐式地传递简洁性偏好，使得模型在推理时学会“少思考”，同时保持甚至提升准确率；保留比例k/G是控制长度降低幅度的核心调节杠杆。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 少思考多采样：用于简洁推理的分组过滤策略优化 |
| 英文题名 | Sample More to Think Less: Group Filtered Policy Optimization for Concise Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UKOqoULbZS) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Group Filtered Policy Optimization (GFPO) |
| Dataset | AIME 25, AIME 24, GPQA, Omni-MATH |

> [!tip] 效果简介
> - AIME 25 上，Pass@1 / Response Length / ELR 为 69.5% / 12k / 70.9%，对比 72.4% / 14.8k / 0%，变化 -2.9% (n.s.) / -2.8k / +70.9%。
> - AIME 24 上，Pass@1 / Response Length / ELR 为 76.4% / 10.6k / 84.6%，对比 77.7% / 13.3k / 0%，变化 -1.3% (n.s.) / -2.7k / +84.6%。
> - GPQA 上，Pass@1 / Response Length / ELR 为 68.5% / 7.5k / 79.7%，对比 67.5% / 10.7k / 0%，变化 +1.0% (n.s.) / -3.2k / +79.7%。

## 概要

基于强化学习的推理训练（RLVR）在提升大型语言模型复杂推理能力方面取得了显著进展，但其主流方法 GRPO（Shao et al., 2024）暴露出一个关键瓶颈：训练过程中模型的响应长度会持续膨胀，产生大量冗余 token，而准确率并未相应提升。这种“长度爆炸”现象不仅增加了推理延迟和计算成本，还使得在监督微调（SFT）阶段形成的逐步推理习惯被进一步放大。

本文提出 **Group Filtered Policy Optimization (GFPO)**，通过一种简单而有效的“分组过滤”机制来解决上述问题。其核心思想是：在训练时**增大每个问题的采样组量 G**，然后根据用户指定的指标（如响应长度或 token 效率）仅保留 top-k 条最优响应参与策略更新，将其余响应的优势直接置零。这一设计隐式地向策略传递了简洁性偏好，使模型在推理时学会“少思考”，同时保持甚至提升准确率。

实验结果表明，GFPO 将 GRPO 造成的长度膨胀降低高达 **85%**，在 AIME 24/25、GPQA、Omni-MATH 和 LiveCodeBench 等基准上维持统计无差异的准确率。其中，基于奖励/token 效率的 Token Efficiency 过滤变体取得了最优的简洁性-准确率权衡，仅增加约 7% 的训练时间，即可减少近 30% 的推理延迟。消融实验进一步揭示，保留比例 **k/G** 是控制长度降低幅度的核心调节杠杆，降低该比例即可线性地缩短响应长度。

GFPO 无需复杂的奖励工程，可灵活适配长度、token 效率等多种过滤指标，并支持根据问题难度自适应调整保留数量。该方法在 DeepSeek-R1 蒸馏模型（Qwen、Llama，7B–14B）上同样有效，展现出良好的模型和任务泛化能力。

### 推理模型中的“长度膨胀”困境

近年来，通过强化学习（RL）训练推理模型已成为提升数学、编程等复杂任务准确率的主流范式。**GRPO**（Shao et al., 2024）作为代表性方法，通过组内归一化优势估计消除了对价值网络的需求，显著推动了开源推理模型的发展。然而，GRPO训练过程中暴露出一个关键问题：**响应长度会不可控地膨胀**。

具体而言，在GRPO训练下，模型的推理链会持续变长，产生大量冗余token，而准确率并未获得相应提升。以**Phi-4-reasoning-plus**（Abdin et al., 2025）为例，该14B模型在GRPO训练后，AIME 25上的平均响应长度从SFT基线的约6k token膨胀至14.8k token，但准确率提升幅度远不匹配这一长度增长。这种冗长不仅增加了推理延迟（在困难问题上可达90秒以上），还使得模型在SFT阶段形成的逐步推理习惯被进一步放大。

### 现有方案的不足

针对长度膨胀问题，已有一些尝试，但效果有限：

- **长度惩罚与token级归一化**：直接在奖励函数中加入长度惩罚项，或调整优势估计中的token级归一化，往往难以精确抑制冗长。这些方法可能意外放大正确但冗长的响应的奖励信号，甚至导致训练不稳定。
- **Dr. GRPO**（Liu et al., 2025）：通过移除token长度归一化来尝试减少冗长，但实验表明其长度缩减幅度有限，且在某些基准上准确率出现下降，训练过程中还存在梯度爆炸和KL散度突增的风险。

上述方法的共同缺陷在于：它们试图通过调整奖励信号或归一化方式来间接约束长度，但未能从根本上阻断策略向冗长方向更新的学习路径。

### 核心动机：从“惩罚”到“过滤”

本文的核心观察是：**GRPO训练中，所有采样响应都参与策略更新，包括那些冗长但恰好获得高奖励的响应。** 这些响应虽然正确，却携带了大量不必要的推理步骤，它们的存在持续向策略传递“长推理是可接受的”信号。

基于此，本文提出**Group Filtered Policy Optimization（GFPO）**，其核心思想是：**在训练时增加采样数量，但仅让满足简洁性偏好的响应参与学习。** 通过将冗长响应的优势直接置零，GFPO从梯度层面切断了冗长行为的强化路径，从而在保持准确率的同时，大幅抑制长度膨胀。

## 核心方法与创新机理

### 问题瓶颈：GRPO 的长度膨胀

基于强化学习的推理训练（如 GRPO，Shao et al., 2024）会系统性地导致响应长度膨胀。在 AIME 2025 上，GRPO 将 SFT 基线的平均响应长度从约 6k tokens 推高至近 15k tokens，而准确率并未获得相应提升——这些额外生成的 token 大部分是冗余推理。现有的长度惩罚和 token 级归一化策略（如 Dr. GRPO，Liu et al., 2025）不足以抑制这种冗长，甚至可能因正确长响应的奖励放大而加剧 SFT 阶段形成的逐步推理习惯。

### 核心机制：分组过滤策略优化（GFPO）

GFPO 的核心创新在于**在训练时通过“采样更多、保留更少”的过滤机制，隐式传递简洁性偏好**，从而在不依赖显式长度惩罚的前提下抑制策略向冗长方向更新。具体而言，GFPO 对 GRPO 做了以下关键改造：

1. **增大采样组量 G**：训练时为每个问题采样 $G \in \{8, 16, 24\}$ 条候选推理链（GRPO 固定 $G=8$），扩大候选池以包含更多具有理想属性的响应。

2. **基于用户定义指标的 Top-k 过滤**：根据选择指标（响应长度或奖励/token 效率）对所有 $G$ 条响应排序，仅保留 top-$k$ 条（$k \leq 8$），通过二进制掩码 $m_i$ 将其余响应的优势直接置零。

3. **屏蔽优势估计**：优势归一化仅在保留子集 $S$ 上计算均值和标准差：
   $$\widehat{A}_{i,t}^{(m)} = \frac{R(q, o_i) - \frac{1}{k} \sum_{j \in S} R(q, o_j)}{\sqrt{ \frac{1}{k} \sum_{j \in S} \bigl( R(q, o_j) - \frac{1}{k} \sum_{p \in S} R(q, o_p) \bigr)^2 }} m_i$$
   未被选中的响应获得零优势，从而直接阻断策略向冗长方向更新。

4. **保留比例 $k/G$ 作为核心控制杠杆**：实验表明，降低 $k/G$ 比例（增大 $G$ 或减小 $k$）即可线性地缩短平均响应长度，这是控制冗长的决定性因素（Figure 6）。

### 关键变体：Token Efficiency 过滤

除按长度过滤外，GFPO 引入**Token Efficiency 过滤**——按奖励/token 效率（$R_i / |o_i|$）排序选择 top-k 响应。该变体带来的长度缩减远超同规模的长度过滤变体（如 Shortest 8/16），甚至比更大组的 Shortest 8/24 更有效，且仅增加约 7% 的训练时间（Table 3）。

### 自适应难度 GFPO

为进一步优化难度-长度权衡，GFPO 引入**自适应难度机制**：通过 streaming t-digest 在线估计问题难度（基于响应平均奖励的分位数），将问题分为四个难度桶，并动态分配保留数量 $k$——极难题保留 $k=8$，中等 $k=6$，简单 $k=4$（$G=16$）。该变体在极端难题上实现了最强的超长响应抑制，同时在多数难度区间保持或超过 GRPO 准确率。

### 与基线方法的本质区别

| 方法 | 核心策略 | 局限性 |
|------|----------|--------|
| **GRPO** (Shao et al., 2024) | 组内全量响应归一化优势 | 无长度控制，响应持续膨胀 |
| **Dr. GRPO** (Liu et al., 2025) | 移除 token 长度归一化 | 训练不稳定，可能出现梯度爆炸或 KL 突增 |
| **GFPO（本方法）** | 采样更多、过滤保留 top-k、屏蔽非保留响应优势 | 训练稳定，长度控制精确，准确率无统计显著下降 |

GFPO 的优势在于其过滤机制与优势归一化正交，可与 Dr. GRPO 等其他 RLVR 改进兼容叠加；同时，它通过拒绝步骤隐式塑造学习信号，避免了显式惩罚项带来的奖励工程复杂性。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/001_Figure_1.jpg]]
*Figure 1: Left: GFPO introduces simple yet powerful modifications to GRPO: sample more responses during training (↑ G), rank them by a target attribute (e.g., length, token efficiency), and learn only from the top-k—setting the advantages of the rest to zero. This selective learning functions as implicit reward shaping, steering the policy toward desired behaviors. Right: When optimizing for length or token efficiency, GFPO curbs GRPO’s length inflation—letting the model think less at inference-time by sampling more at training-time—while maintaining its core reasoning capabilities*

GFPO 的核心管线由五个模块构成，形成一个从采样到策略更新的闭环。其设计思路是：在训练时**增加采样量**，再通过**选择性过滤**隐式传递简洁性偏好，使模型在推理时自动生成更短的推理链。

### 1. Response Sampling（候选响应采样）

对于每个问题 $q$，从当前策略 $\pi_{\theta_{\text{old}}}$ 中采样 $G$ 条候选推理链 $\{o_i\}_{i=1}^G$。与 GRPO（Shao et al., 2024）固定使用 $G=8$ 不同，GFPO 将 $G$ 扩大至 16 或 24，以增加候选池的多样性，为后续过滤提供更丰富的选择空间。

### 2. Metric Scoring（指标评分）

根据用户指定的选择指标对每条响应计算分数。论文实现了两种指标：
- **长度过滤（Shortest）**：直接以响应长度 $|o_i|$ 作为分数，越短分数越高。
- **Token 效率过滤（Token Efficiency）**：以奖励/长度比 $R_i / |o_i|$ 作为分数，同时兼顾正确性与简洁性。

### 3. Top-k Filtering（Top-k 过滤）

按分数排序，保留前 $k$ 条响应（$k \leq 8$），生成二进制掩码 $m_i \in \{0, 1\}$。保留比例 $k/G$ 是控制长度缩减幅度的核心调节杠杆——降低该比例可线性地缩短响应长度（Figure 6）。仅在小采样组内过滤（如 $G=8$ 时取 $k=6$）无法产生有意义的长度缩减，必须同时增大 $G$ 才能获得显著效果。

### 4. Masked Advantage Estimation（掩码优势估计）

在保留集 $S$ 上计算归一化优势，未被选中的响应优势直接置零：

$$\widehat{A}_{i,t}^{(m)} = \frac{R(q, o_i) - \frac{1}{k} \sum_{j \in S} R(q, o_j)}{\sqrt{ \frac{1}{k} \sum_{j \in S} \bigl( R(q, o_j) - \frac{1}{k} \sum_{p \in S} R(q, o_p) \bigr)^2 }} \cdot m_i$$

这一设计使得冗长或低效的响应对策略更新不产生任何贡献，从而抑制策略向冗长方向漂移。

### 5. Policy Update（策略更新）

使用屏蔽后的优势计算 PPO 截断损失，并叠加 KL 散度惩罚和熵奖励，更新策略参数 $\theta$：

$$\mathcal{J}_{\mathrm{GFPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(O)} \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{\infty} \min\Bigl( r_{i,t}, \mathrm{clip}(r_{i,t}, 1-\varepsilon, 1+\varepsilon) \Bigr) - \beta \mathcal{D}_{KL}(\pi_{\theta} \| \pi_{\theta_{\mathrm{old}}}) + \gamma \operatorname{Entropy}(\pi_{\theta})$$

### 自适应难度扩展

在上述固定 $k$ 方案的基础上，GFPO 进一步引入**自适应难度机制**：根据问题难度动态调整保留数量 $k$。难度由响应平均奖励的 t-digest 分位数在线估计，将问题划分为四个难度桶——极难（0–25%）、困难（25–50%）、中等（50–75%）、简单（75–100%），对应保留 $k \in \{8, 8, 6, 4\}$ 条响应。这一设计使模型在极端难题上获得最强的超长响应抑制效果，同时在多数难度区间保持或超过 GRPO 的准确率。

### 输入输出流

- **输入**：训练问题 $q$ 及其对应的真实答案（用于计算二元准确度奖励）。
- **中间产物**：$G$ 条候选推理链及其奖励值 $R(q, o_i)$，经指标评分和过滤后得到保留子集 $S$ 及掩码 $m$。
- **输出**：更新后的策略参数 $\theta$，该策略在推理时生成比 GRPO 基线更短的推理链，同时保持准确率无统计显著性差异（Wilcoxon 符号秩检验）。

整个管线对 GRPO 的改动集中在采样规模放大和优势计算屏蔽两个环节，与 Dr. GRPO（Liu et al., 2025）等基于归一化修改的方法正交，理论上可与之叠加使用。

### GFPO 的五个核心模块

GFPO 在 GRPO 的训练流程中插入了选择性过滤机制，其完整优化管线由以下五个模块串联构成：

1.  **Response Sampling**：对每个问题 $q$，从当前旧策略 $\pi_{\theta_{\text{old}}}$ 中采样 $G$ 条候选推理链 $\{o_i\}_{i=1}^G$。与 GRPO 固定 $G=8$ 不同，GFPO 将采样组量增大至 $G \in \{8, 16, 24\}$，以扩大候选池中简洁响应的出现概率。
2.  **Metric Scoring**：根据用户指定的选择指标为每条响应计算分数。论文实现了两种指标：**响应长度**（token 数）和 **Token Efficiency**（奖励/长度比 $R_i / |o_i|$）。
3.  **Top-k Filtering**：按分数降序排列，保留前 $k$ 条最优响应（$k \le 8$），构成保留集 $S$，并生成二进制掩码 $m_i$——被选中响应 $m_i = 1$，其余 $m_i = 0$。
4.  **Masked Advantage Estimation**：仅在保留集 $S$ 上计算归一化优势，未被选中的响应优势直接置零。这一步骤是 GFPO 抑制冗长更新的核心机制。
5.  **Policy Update**：使用屏蔽后的优势计算 PPO 截断损失，并施加 KL 散度惩罚与熵奖励，完成策略参数更新。

### 关键公式

**GFPO 屏蔽优势估计**

GFPO 对 GRPO 优势函数的核心修改在于引入二元掩码 $m_i$，并将归一化统计量限定在保留集 $S$ 内计算：

$$\widehat{A}_{i,t}^{(m)} = \frac{R(q, o_i) - \frac{1}{k} \sum_{j \in S} R(q, o_j)}{\sqrt{ \frac{1}{k} \sum_{j \in S} \bigl( R(q, o_j) - \frac{1}{k} \sum_{p \in S} R(q, o_p) \bigr)^2 }} \cdot m_i$$

-   $R(q, o_i)$：第 $i$ 条响应的奖励值。
-   $S$：按选择指标排序后保留的 top-$k$ 响应子集，$|S| = k$。
-   $m_i \in \{0, 1\}$：二元掩码，$m_i = 1$ 当且仅当 $o_i \in S$。
-   **机制**：未保留响应（$m_i = 0$）的优势被强制置零，其对应的策略梯度贡献为零，从而阻止策略向冗长方向更新。保留集内的优势归一化仅使用 $S$ 自身的均值与标准差，避免了长响应拉高整体均值导致的奖励稀释。

**GFPO 总优化目标**

$$\mathcal{J}_{\mathrm{GFPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(O)} \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{\infty} \min\Bigl( r_{i,t}, \mathrm{clip}(r_{i,t}, 1-\varepsilon, 1+\varepsilon) \Bigr) \widehat{A}_{i,t}^{(m)} - \beta \mathcal{D}_{KL}(\pi_{\theta} \| \pi_{\theta_{\mathrm{old}}}) + \gamma \operatorname{Entropy}(\pi_{\theta})$$

-   $r_{i,t} = \frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid q, o_{i,<t})}$：token 级新旧策略概率比。
-   $\widehat{A}_{i,t}^{(m)}$：上述屏蔽优势估计。
-   $\beta$、$\gamma$：KL 惩罚与熵奖励的权重系数。
-   **关键设计**：损失函数在 token 级取平均（除以 $\sum |o_i|$），而非响应级平均，这与 GRPO 的 token-level normalization 保持一致，但通过 $\widehat{A}_{i,t}^{(m)}$ 中的掩码机制实现了对冗余 token 的隐式惩罚。

**对比：GRPO 原始优势估计**

$$\widehat{A}_{i,t} = \frac{R(q, o_i) - \operatorname{mean}\{R(q, o_1), \dots, R(q, o_G)\}}{\operatorname{std}\{R(q, o_1), \dots, R(q, o_G)\}}$$

-   **差异**：GRPO 使用全部 $G$ 条响应的全局均值与标准差进行归一化，所有响应均参与训练。当 $G=8$ 且存在冗长但正确的响应时，其优势可能被高估，驱动策略向更长方向更新。

### 训练奖励函数

GFPO 沿用了与 GRPO 基线相同的奖励函数，未引入显式的长度惩罚项：

$$R = w_{\mathrm{acc}} \cdot \mathrm{LENGTHSCALE}(R_{\mathrm{acc}}) + w_{\mathrm{rep}} \cdot R_{\mathrm{rep}}, \quad R \in [-1, 1]$$

-   $R_{\mathrm{acc}}$：二元准确度奖励（正确为 1，错误为 -1）。
-   $\mathrm{LENGTHSCALE}(\cdot)$：长度缩放函数，用于缓解奖励稀疏问题。
-   $R_{\mathrm{rep}}$：5-gram 重复惩罚。
-   $w_{\mathrm{acc}}$、$w_{\mathrm{rep}}$：权重系数。

**要点**：GFPO 并未修改奖励函数本身，而是通过**优势屏蔽**在策略梯度层面间接传递简洁性偏好，避免了复杂奖励工程可能引入的偏差。

## 实验与关键发现

### 核心瓶颈与因果机制

GRPO训练存在一个显著但常被忽视的问题：策略优化过程中，模型的响应长度会持续膨胀，产生大量冗余token，而准确率并未获得相应提升。在Phi-4-reasoning-plus（Abdin et al., 2025）这一14B基线模型上，GRPO使AIME 25的响应长度从SFT的9.5k膨胀至14.8k，增幅达55.8%，但Pass@1准确率仅从68.4%提升至72.4%。这一现象在GPQA、Omni-MATH等基准上同样存在——模型学会了“说更多”而非“想更好”。

传统应对手段效果有限：长度惩罚和token级归一化难以有效抑制冗长，甚至可能放大正确长响应的奖励信号，反而强化了SFT阶段形成的逐步推理习惯。Dr. GRPO（Liu et al., 2025）通过移除token长度归一化来尝试解决此问题，但实验显示其训练过程不稳定，且长度缩减幅度远不及GFPO。

GFPO的核心洞察在于：**在训练时增加采样数量并进行选择性过滤，可以隐式地传递简洁性偏好，使模型在推理时学会“少思考”**。具体而言，GFPO将采样组量从GRPO的G=8增大至16或24，然后根据用户指定的指标（响应长度或奖励/长度效率）仅保留top-k条响应（k≤8），通过掩码将未被选中的响应优势设为零。这一机制直接抑制了策略向冗长方向更新，而保留比例k/G成为控制长度降低幅度的核心调节杠杆。

### 主要结果

Table 1展示了GFPO各变体在五个基准上的综合表现。Token Efficiency GFPO（按奖励/token效率排序，G=16，k=8）实现了最显著的长度缩减效果：

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/002_Table_1.jpg]]
*Table 1: Pass@1 Accuracy, Response Lengths, and Length Inflation Reduction. Across all benchmarks, GFPO cuts length inflation while matching GRPO accuracy (no significant difference under Wilcoxon signed-rank test). Sampling more responses is key and lowering k/G effectively controls length. Token Efficiency delivers the largest reduction in length inflation (79.5%) at GRPO-level accuracy, and Adaptive Difficulty outperforms shortest k/G at equal compute. On LiveCodeBench (OOD coding), GRPO lengthens chains without accuracy gains, whereas GFPO shortens them and sometimes improves accuracy (e.g., 8/16, 4/24). GFPO also outperforms Dr. GRPO, with higher accuracy and larger excess-length reductions. Pa...*

- **AIME 25**：响应长度从GRPO的14.8k降至12k（↓18.9%），超额长度缩减率（ELR）达70.9%，Pass@1准确率为69.5%，与GRPO的72.4%无统计显著差异（Wilcoxon符号秩检验）。
- **AIME 24**：长度从13.3k降至10.6k（↓20.3%），ELR达84.6%，准确率76.4% vs 77.7%（n.s.）。
- **GPQA**：长度从10.7k降至7.5k（↓29.9%），ELR达79.7%，准确率68.5% vs 67.5%（n.s.）。
- **Omni-MATH**：长度从12.7k降至10.1k（↓20.5%），ELR达82.6%，准确率87.4% vs 86.0%（n.s.）。
- **LiveCodeBench**（分布外代码基准）：长度从13.9k降至11k（↓20.9%），ELR达79.7%，准确率57.0% vs 56.7%（n.s.）。

Figure 2的帕累托前沿图进一步揭示：在除AIME 25外的所有基准上，至少有一种GFPO变体严格支配GRPO——即同时实现更高准确率和更短响应。在AIME 25上，GRPO虽在准确率上略占优势，但GFPO变体以显著更短的长度实现了相近的准确率，整体权衡更优。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/003_Figure_2.jpg]]
*Figure 2: Pareto Trade-off Between Accuracy and Response Length. For all benchmarks except AIME 25, at least one GFPO variant strictly dominates GRPO—achieving both higher accuracy and shorter responses (green region above and to the left of GRPO). For AIME 25, GRPO attains the highest accuracy, but several GFPO variants, while taking non-significant accuracy dips, remain Pareto-optimal because their responses are shorter, and no other method is simultaneously more accurate and more concise. On average, Shortest 4/24, Adaptive Difficulty, and Shortest 8/16 are strictly Pareto-superior to GRPO with Token Efficiency close behind. Dr. GRPO generally falls outside the Pareto frontier–yielding lower accur...*

### 消融实验

**保留比例k/G是核心控制变量**。Figure 6显示，当k/G比例从50%（如Shortest 8/16）降至约17%（如Shortest 4/24）时，平均响应长度几乎线性下降。仅在小采样组内过滤（如Shortest 6/8，k/G=75%）无法产生有意义的长度缩减（ELR仅为1.8%–11.5%），说明**必须同时增大采样组G才能获得显著效果**。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/013_Figure_6.jpg]]
*Figure 6: Average Response Length vs k/G. Reducing k/G, reduces average response length but beyond a point leads to diminishing returns*

**Token Efficiency过滤优于单纯按长度过滤**。在相同k/G比例下，Token Efficiency 8/16带来的长度缩减远超Shortest 8/16（ELR 70.9% vs 26% on AIME 25），甚至比更大采样组的Shortest 8/24（ELR 51%）更有效。其原理在于：奖励/token效率同时惩罚了“长且错”和“长但对”的响应，而仅按长度过滤可能保留正确但冗长的推理链。

**自适应难度GFPO在极端难题上表现突出**。该方法根据问题难度动态调整k值（难题k=8，中等k=6，简单k=4），难度由响应平均奖励的t-digest分位数在线估计。Figure 3显示，自适应难度GFPO在极难（very hard）问题上实现了最强的超长响应抑制（ELR 60%），同时在多数难度区间保持或超过GRPO准确率。但在中等难度（hard）区间，该方法偶尔会过滤掉一些有用的长推理链，导致准确率略低于GRPO。

**与Dr. GRPO的对比**。Table 1和Figure 9显示，Dr. GRPO虽能部分缩短响应长度，但其训练过程存在梯度范数波动和KL散度突增问题。GFPO在所有基准上均提供了更高的准确率和更短的长度，且训练曲线保持稳定。

### 推理段分析与效率权衡

Figure 5将推理过程分解为Solution（核心推理）和Verification（验证）两个阶段。GRPO使Solution阶段从SFT的6.5k膨胀至8.3k tokens，Verification阶段从1.9k膨胀至3.1k。Shortest 8/24 GFPO将Solution阶段缩减至6.6k（消除94.4%的超额长度），Verification阶段缩减至2.3k（消除66.7%的超额长度），表明GFPO主要在抑制核心推理阶段的冗余。

Table 3的效率权衡数据显示：Token Efficiency GFPO的训练步时间仅比GRPO增加约7%（28.5分钟→30.4分钟），但端到端推理延迟从318.5秒降至225.0秒（↓29.4%），在难题上可节省约90秒。这一训练-推理效率的非对称收益，使GFPO在实际部署中具有显著优势。

### 泛化性验证

Table 2展示了GFPO在DeepSeek-R1蒸馏模型上的跨架构泛化能力。在DeepSeek-R1-Distill-Qwen-7B上，GFPO（8/16）将AIME 25的长度膨胀降低63%，AIME 24降低39.6%，GPQA降低48.9%，同时准确率与GRPO持平。在Llama-8B和Qwen-14B上同样观察到一致的长度缩减效果，验证了该方法的模型规模和架构无关性。

### 失败模式与局限

尽管GFPO在整体准确率上未出现统计显著下降，但存在以下边界情况：

1. **极难题上的正确长响应损失**：Token Efficiency变体在部分极困难问题上可能过滤掉少量正确但冗长的推理链，导致这些特定问题的准确率略低于GRPO（见Table 5–6的长度分箱分析）。
2. **中等难度的过度过滤**：自适应难度GFPO在中等难度区间偶尔会因k值设置偏低而损失有用推理链，准确率略低于GRPO基线。
3. **训练计算开销**：增大采样组G需更多训练计算。虽然14B模型上仅增加7%时间，但对于更大规模模型或更高吞吐场景，这一开销可能被放大。
4. **任务范围受限**：当前实验集中于数学和编程等可验证奖励的任务，GFPO在开放式文本生成或主观评估任务上的表现尚未验证。

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/009_Figure_4.jpg]]
*Figure 4: Accuracy Across Response Lengths for AIME 25. (a) GFPO cuts long-tail verbosity (32% to 22% outputs ≥ 20k tokens) and solves hard problems with shorter responses (∼9x harder prompts solved with ≤ 5k tokens). (b) Accuracy declines with increasing response length even at fixed difficulty. On hard problems, most models peak at 12k-16k tokens, while GFPO variants outperform GRPO in the longest bin by producing shorter, more accurate long responses. Table 3: Train–Test Trade-off. Training step time vs. end-to-end latency for GRPO and GFPO variants. Token Efficiency GFPO reduces latency by ∼29% with only a 7% increase in training time, eliminating three-quarters of the latency overhead introduced...*

![[assets/figures/papers/paper_list_l40_https_openreview_net_forum_id_UKOqoULbZS/figures/012_Table_4.jpg]]
*Table 4: Pass@1 Accuracy and Average Response Lengths on AIME 25, AIME 24, GPQA, Omni-MATH, and LiveCodeBench. GFPO variants substantially reduce response lengths while matching GRPO accuracy. We find no statistically significant differences in GFPO’s accuracy under the Wilcoxon signed-rank test for any dataset. Dr. GRPO yields lower accuracy (66.6% vs 69.5% on AIME 25, 74.4% vs 76.4% on AIME 24, 66.7% vs 68.5% on GPQA) and substantially longer responses than GFPO (43.6% vs 70.9% len reduction on AIME 25, 48.5% vs 84.6% on AIME 24, 65.1% vs 79.7% on GPQA, and 7.2% vs 79.7% on LiveCodeBench)*

## 定位与知识库关联

### 与基础RLVR方法的关系

GFPO直接建立在GRPO（Shao et al., 2024）的强化学习框架之上，其核心创新在于对优势估计环节的改造。GRPO通过组内均值-标准差归一化计算每个响应的优势，所有G条响应均参与策略更新。GFPO保留了GRPO的截断代理损失、KL散度惩罚和熵奖励等基础组件，但引入了一个决定性的“分组过滤”步骤：在训练时增大采样组量G（从8增至16或24），然后根据用户指定的指标仅保留top-k条响应，将其余响应的优势掩码设为零。这一修改在数学上体现为将优势估计的归一化范围从全组收缩到保留子集S，并通过二元掩码m截断未选中响应的梯度流。

与Dr. GRPO（Liu et al., 2025）相比，GFPO采取了正交的干预路径。Dr. GRPO试图通过移除token长度归一化来抑制冗长，而GFPO通过选择性过滤直接控制哪些推理链参与学习。实验证据表明，GFPO在所有基准上均提供了更高的准确率和更短的响应长度，且训练过程中未出现梯度爆炸或KL散度突增等不稳定现象（Figure 9）。这意味着仅靠调整归一化策略不足以有效抑制GRPO的长度膨胀，而过滤机制从梯度源头切断了冗长响应的强化信号。

### 与SFT基线的衔接

论文使用的SFT基线为Phi-4-reasoning（Abdin et al., 2025），即未经RL训练的监督微调模型。GRPO在SFT基础上进行RL训练后，响应长度显著膨胀——例如在AIME 25上从约7k tokens增至14.8k tokens，但准确率提升有限。GFPO的定位是在GRPO的RL训练框架内抑制这种超额长度膨胀，其效果通过“超额长度降低比例”（ELR）量化：ELR衡量GFPO相对于GRPO所额外消除的超额长度占GRPO超额长度的比例。Token Efficiency变体在多个基准上实现了70%–85%的ELR，意味着大部分GRPO引入的冗长被消除，响应长度回落至接近SFT水平，同时准确率维持在与GRPO统计无差异的水平。

### 方法适用边界

**任务域边界**：当前验证集中于数学推理（AIME 24/25、Omni-MATH）和编程（LiveCodeBench）等可验证奖励的任务。这些任务的特点是存在明确的正确性判断（答案匹配或测试用例通过），使得基于奖励的过滤指标（长度、奖励/token效率）具有可靠的基础。GFPO在开放式文本生成、主观评价或需要多维度质量权衡（如事实一致性、无害性、创造性）的任务上的表现尚未被评估。

**模型规模边界**：实验覆盖7B至14B参数规模的模型（Phi-4-reasoning-plus、DeepSeek-R1-Distill-Qwen-7B/14B、DeepSeek-R1-Distill-Llama-8B），在更大规模模型（如70B及以上）或更复杂的交互式推理场景中，GFPO的简洁性-准确率权衡是否仍然成立尚需验证。

**训练预算边界**：GFPO通过增大G引入额外训练计算开销。Token Efficiency变体将训练时间增加约7%，换取了约29%的推理延迟下降（Table 3）。这一权衡在当前实验设置下是有利的，但对于更高吞吐的推理训练场景或超大模型，额外采样成本可能成为限制因素。

### 已知局限

1. **极困难问题上的正确长响应损失**：Token Efficiency变体在部分极困难问题上可能过滤掉少量正确但较长的推理链。Figure 4b显示，在非常困难的问题上，Token Efficiency和Shortest 8/24在较长响应区间的准确率有所下降，表明激进过滤可能牺牲了某些需要深度推理的正确解。

2. **中等难度区间的过滤误差**：自适应难度GFPO在中等难度（hard）区间偶尔会过滤掉一些有用的长推理链，导致准确率略低于GRPO（Figure 3b）。这说明基于平均奖励的难度估计和固定的k值分配策略仍有优化空间。

3. **质量维度的单一性**：当前GFPO主要针对推理链的长度进行优化，尚未系统评估其是否会影响生成内容的真实性或多样性等其他重要属性。过滤机制隐式传递了简洁性偏好，但这种偏好是否会在多轮对话或需要详细解释的场景中产生负面影响尚不明确。

4. **保留比例k/G的经验性**：k/G比值是控制长度降低幅度的核心杠杆（Figure 6），但其最佳值目前通过实验确定，缺乏理论指导。随着模型大小、训练数据分布或任务类型的变化，最优k/G可能不同，尚无自动调节该比例的方法。

### 开放问题

1. **多维度过滤的扩展性**：GFPO的过滤思想能否扩展至正确性之外的质量维度？例如，是否可以根据事实一致性、无害性或多样性奖励进行过滤，从而同时优化多个期望属性？这需要设计更复杂的过滤指标和可能的帕累托优化策略。

2. **与RLVR改进的兼容性**：GFPO修改的是优势估计环节，与DAPO（Abdin et al., 2025）等修改损失函数的方法在理论上正交。两者能否无缝结合产生叠加增益？初步证据显示GFPO与Dr. GRPO相比已展现出优势，但与其他RLVR改进的组合效果尚待探索。

3. **最优G/k组合的理论分析**：当G进一步增大时，优势估计的方差会如何变化？是否存在一个理论上的最优G/k组合，在给定训练预算下最大化简洁性-准确率权衡？当前实验仅探索了G∈{8,16,24}和k≤8的配置空间。

4. **跨任务泛化机制**：GFPO在分布外的代码基准LiveCodeBench上同样抑制了长度膨胀，表明过滤机制学习到的简洁性偏好具有一定的任务泛化能力。这种泛化的深层原因——是简洁推理本身具有跨域共性，还是过滤机制隐式地正则化了策略——值得进一步研究。

5. **大规模部署的可行性**：在更大规模模型或更复杂的推理任务中，GFPO的额外采样开销和过滤策略是否仍能维持当前的效率优势？特别是当单次推理成本已经很高时，增大G的边际收益可能递减。

## 原文 PDF

![[paperPDFs/ICLR_2026/Sample_More_to_Think_Less_Group_Filtered_Policy_Optimization_for_Concise_Reasoning.pdf]]
