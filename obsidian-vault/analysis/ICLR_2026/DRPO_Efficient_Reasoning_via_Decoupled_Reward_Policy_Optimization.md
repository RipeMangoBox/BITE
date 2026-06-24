---
title: "DRPO: Efficient Reasoning via Decoupled Reward Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DRPO_Efficient_Reasoning_via_Decoupled_Reward_Policy_Optimization.pdf
openreview_forum_id: GP5RHZnEsw
aliases:
- DDRPO
- DRPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "解耦正负样本的奖励计算，将长度奖励的归一化仅限制在正样本组内，从而避免负样本的干扰。"
primary_logic: "将长度奖励转化为正样本分布权重，并融入判别式优化目标，推导出闭式解，实现无需额外数据的高效训练。"
claims:
- "GRPO with length penalty pushes correct long answers' advantage below zero, harming learning."
- "DRPO decouples learning signals: positive rewards normalized only within the positive group."
- "DRPO achieves 77% length reduction on GSM8K with only 1.1% performance loss (1.5B model)."
- "Derived closed-form solution enables efficient on-policy computation without extra data."
---

# DRPO: Efficient Reasoning via Decoupled Reward Policy Optimization

> [!tip] 核心洞察
> 将长度奖励转化为正样本分布权重，并融入判别式优化目标，推导出闭式解，实现无需额外数据的高效训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DRPO：基于解耦奖励策略优化的高效推理 |
| 英文题名 | DRPO: Efficient Reasoning via Decoupled Reward Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GP5RHZnEsw); [GitHub](https://github.com/Optimization-AI/DRPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DRPO (Decoupled Reward Policy Optimization) |
| Dataset | GSM8K, AES (1.5B models), AES (7B models), AES (8B models) |

> [!tip] 效果简介
> - GSM8K 上，长度缩减率 为 77%，对比 68% (best baseline)，变化 +9% (同时性能损失 1.1% vs 4.3%)。
> - AES (1.5B models) 上，AES 为 0.178 (DRPO λ=0.1)，对比 -0.129 (RLOO-LP α=0.2)，变化 +0.307。
> - AES (7B models) 上，AES 为 0.249 (DRPO λ=0.1)，对比 -0.033 (RLOO-LP α=0.1)，变化 +0.282。

## 概述

### 问题瓶颈

当前主流的组相对策略优化方法（如 GRPO）在引入长度惩罚以抑制冗长推理时，存在一个关键的优化障碍：**长度惩罚会压低所有正确但冗长的输出的奖励值，使其在组内相对优势计算中变为负数**。具体而言，当正确性奖励为 1 的冗长回答被施加长度惩罚后，其相对于组内均值的优势可能从正值（如 1）跌落至负值（如 -0.17），导致优化器将该有效推理误判为负样本并加以抑制，从而损害模型性能（Figure 1）。这一机制性缺陷使得“缩短推理长度”与“保持推理精度”之间难以有效权衡。

### 核心方法

DRPO（Decoupled Reward Policy Optimization）提出**解耦正负样本的学习信号**：将长度奖励的归一化严格限制在正样本组内，使冗长但正确的回答仅受到适度降权，而不会被错误地推向负样本区域。在此基础上，DRPO 将长度奖励转化为正样本分布权重，并融入一个判别式优化目标（基于 DisCO 框架），推导出**闭式最优正样本分布**，从而仅需在线策略数据即可高效计算梯度，无需额外数据或训练开销。

### 方法定位

DRPO 属于**推理效率优化**方法，通过奖励设计层面的解耦来干预策略优化的学习信号。其直接对比的基线包括：将长度惩罚直接嵌入 RLOO 优势的 **RLOO-LP**、基于通过率自适应调整长度惩罚的 **ALP**、惩罚长于最短正确回答的 **HAPO**，以及长度约束推理模型 **L1-max**、**SB**（Yi et al., 2025）和难度感知动态长度奖励 **LASER-D**（Liu et al., 2025b）。与这些方法将长度惩罚直接作用于奖励或优势计算不同，DRPO 将长度信息以重要性权重的方式注入目标函数，从根本上避免了负样本对正样本长度信号的干扰。

### 主要结果

在数学推理基准上的综合评估显示，DRPO 在多个模型规模下均显著优于各基线方法：

- **GSM8K（1.5B 模型）**：DRPO 实现 77% 的长度缩减，仅伴随 1.1% 的性能损失；而最优基线在牺牲 4.3% 性能的情况下仅达到 68% 的长度缩减。
- **AES 综合分数（Accuracy Efficiency Score）**：在 1.5B、7B 和 8B 模型上，DRPO 分别取得 0.178、0.249 和 0.297 的 AES 分数，均大幅领先于 RLOO-LP、ALP、HAPO 等基线（Table 1）。
- **逻辑推理任务**：DRPO 在保持精度不变的前提下，将生成长度从 2095 降至 1400 tokens（缩减 33.2%）。

案例研究表明，DRPO 在简单提示上仅需 89 tokens 即可给出正确推理，相比 DisCO 的 526 tokens 实现 6 倍压缩；在困难提示上以 455 tokens 完成推理，约为 DisCO（4497 tokens）的十分之一。

## 背景与动机

### 推理效率的困境

大语言模型在数学、逻辑等复杂推理任务上的突破，很大程度上依赖于“思维链”（Chain-of-Thought）式的长文本生成。然而，这种冗长的推理过程带来了显著的推理效率问题：模型倾向于产生大量冗余的反思、重复验证和不必要的中间步骤，导致生成长度远超实际所需。如何在保持推理性能的前提下，有效压缩生成长度，成为当前推理优化领域的核心瓶颈。

### 现有方法的缺陷：长度惩罚为何失效

为解决这一问题，主流方法尝试在强化学习（RL）训练中引入长度惩罚（length penalty），将简洁性偏好直接注入奖励信号。GRPO（Group Relative Policy Optimization）等基于组相对优势（group-relative advantage）的方法被广泛采用，其核心机制是将每个回答的奖励与同组其他回答的均值进行比较，计算相对优势值来决定策略更新的方向。

然而，这种看似直接的方案存在一个关键缺陷。当长度惩罚被施加到正确性奖励上时，一个冗长但完全正确的回答，其奖励值会被显著压低。在 GRPO 的组相对优势计算中，这可能导致该正确回答的优势值跌至零以下，变成负数。**这意味着，模型会被误导，将一个实际上有效的推理过程视为“负面样本”来抑制**。Figure 1 中的示例清晰地展示了这一机制：假设 6 个回答的正确性奖励为 `[1, 1, 1, 0, 0, 0]`，施加长度惩罚后变为 `[0.73, 0.6, 0.2, 0, 0, 0]`。第三个正确但冗长的回答，其 GRPO 优势值从无惩罚时的 1 骤降至 -0.17，被错误地归入了“应被惩罚”的范畴。这种错误信号会抑制有效的推理模式，造成显著的优化障碍，甚至损害模型性能。

### 核心洞见：解耦正负样本的学习信号

上述问题的根源在于，**长度惩罚的效应被负样本（错误回答）所污染**。在组相对优势的计算中，所有回答——无论正确与否——都被放在同一个池子里进行标准化。负样本的存在扭曲了正样本的相对位置，使得冗长但正确的回答在对比中显得“更差”。

本文的核心洞见是：**将正负样本的学习信号彻底解耦**。具体而言，长度奖励的归一化应该仅在正样本组内进行，完全隔绝负样本的干扰。这样，一个正确回答的长度惩罚只会影响它在其他正确回答中的相对权重，而永远不会将其推入“负样本”的领域。基于这一洞见，DRPO（Decoupled Reward Policy Optimization）将长度奖励转化为正样本分布上的重要性权重，并直接融入一个判别式优化目标中，从而从根本上消除了 GRPO 式方法的错误信号问题。

## 核心创新

### 瓶颈发现：GRPO 组相对优势对冗长正确样本的误伤

GRPO 等基于组相对优势的强化学习方法在引入长度惩罚后，会系统性地抑制有效推理。其根本原因在于优势计算机制：GRPO 将同一问题下所有生成回答（无论正确与否）放在同一组内计算均值与标准差，然后以此归一化每个回答的优势值（Eq. 2）。当对正确回答施加长度惩罚后，冗长但正确的回答的奖励值被压低，其组相对优势可能跌至负值。如 Figure 1 所示，假设 6 个回答的正确性奖励为 `[1,1,1,0,0,0]`，施加长度惩罚后变为 `[0.73,0.6,0.2,0,0,0]`，第三个正确回答的优势值从 1 骤降至 -0.17，被错误地标记为负样本。这一机制将“冗长但正确”的回答推入负学习信号区域，与错误回答一同被抑制，形成了显著的优化障碍。

### 核心创新：正负样本学习信号的解耦

DRPO 的核心创新在于**将正负样本的奖励计算彻底解耦**。具体而言，DRPO 将长度奖励的归一化操作严格限制在正样本组内部，完全隔离负样本的干扰。这意味着一个正确回答的长度惩罚仅与其他正确回答比较，而不会因为同一批次中存在错误回答而被错误地压低优势值。这一设计从根源上杜绝了 GRPO 中“冗长正确回答被误判为负样本”的问题：DRPO 会降低冗长正确回答的学习信号强度，但绝不将其推入负值区域（Figure 1）。

### 方法实现：从奖励惩罚到分布加权的范式转换

DRPO 并非简单地在奖励函数中叠加长度惩罚然后计算优势，而是将长度偏好转化为**正样本分布权重**，并融入判别式优化目标。具体路径如下：

1. **基座框架**：DRPO 构建于 DisCO（判别式约束策略优化）之上。DisCO 的目标是直接最大化正样本的生成似然得分、最小化负样本的 log-sum-exp 得分，并在 KL 散度约束下优化策略（Eq. 3）。

2. **长度奖励的分布化**：定义长度奖励函数 $r_l(o) = 1 - |o|/C$（Eq. 4），其中 $C$ 为最大响应长度。DRPO 不直接将此奖励加入优势计算，而是求解一个在 KL 约束下最大化长度奖励的**最优正样本分布**，得到闭式解（Eq. 6）：
   $$P_q^*(o) = \frac{\pi_{\mathrm{old}}^+(o|q) \exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)}$$
   其中 $\lambda$ 控制长度偏好的强度（$\lambda$ 越小，越偏好短回答）。

3. **权重注入判别式目标**：将上述分布作为重要性权重，对 DisCO 目标中的正样本得分项进行加权（Eq. 7）：
   $$\max \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \frac{\exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right]$$

这一公式揭示了 DRPO 的关键性质：正样本的权重由其长度奖励决定，但归一化仅在同问题正样本组内进行；负样本项保持原始 DisCO 的 log-sum-exp 形式，不受长度信号影响。当 $\lambda = +\infty$ 时，权重恒为 1，目标退化为 DisCO。

### 工程优势：闭式解带来的高效训练

DRPO 的闭式解使其具有显著的工程优势：**无需额外数据，仅依赖 on-policy 数据即可完成梯度估计**。训练流程（Algorithm 1）包含六个模块：正负样本划分、长度奖励权重计算（指数形式，组内归一化）、加权正样本得分、负样本 log-sum-exp 惩罚、KL 散度正则化（通过惩罚项 $\beta_0 [D_{KL}(\pi_{\mathrm{old}}||\pi_{\theta}) - \delta]^2_+$ 实现），以及 AdamW 优化器更新。整个过程与 DisCO 的计算开销相当，未引入额外数据需求或复杂采样步骤。

### 与 baseline 的 changed slots 总结

| 维度 | 基线方法（GRPO/RLOO-LP 等） | DRPO |
|------|---------------------------|------|
| 优势计算 | 组相对优势，正负样本混合归一化 | 解耦优势，仅正样本组内归一化 |
| 目标形式 | GRPO/DisCO 目标 + 显式长度惩罚 | 判别式目标 + 长度奖励作为正样本权重 |
| 长度惩罚集成 | 直接修改奖励值，影响优势计算 | 转化为分布权重，不干扰负样本 |

## 整体框架

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the limitation of GRPO with length penalty and the benefit of our approach. Suppose [1, 1, 1, 0, 0, 0] are the accuracy rewards for 6 responses, and [0.73, 0.6, 0.2, 0, 0, 0] are the rewards after applying the length penalty to correct answers. Using the group-relative advantage calculation of GRPO, the advantages for the third response shift from 1 (without length penalty) to -0.17 (with length penalty added), inadvertently penalizing the third correct response, which may substantially harm performance. In contrast, our proposed DRPO reduces the learning signal for lengthy and correct responses but never pushes them to the negative territory*

DRPO 的整体框架围绕一个核心设计展开：**将长度奖励信号从负样本的干扰中解耦出来，仅用于调节正样本的学习权重**。这一设计直接回应了 GRPO 等组相对优势方法的关键瓶颈——当长度惩罚被引入后，冗长但正确的输出会因组内归一化而获得负的优势值，从而被错误地抑制（见 Figure 1 的示意）。

### 方法动机与因果机制

在 GRPO 中，每个生成回答的优势值由该回答的奖励相对于同组所有回答的均值和标准差决定。当长度惩罚被叠加到正确性奖励上时，一个正确但冗长的回答可能获得低于组均值的奖励，导致其优势值从正值转为负值。这意味着模型会将该回答当作负样本来学习，形成显著的优化障碍。

DRPO 通过**解耦正负样本的奖励计算**来规避这一问题：长度奖励仅在正样本组内进行归一化，完全隔绝负样本的干扰。具体而言，DRPO 将长度奖励转化为正样本的分布权重，并融入判别式优化目标（DisCO 框架）中，推导出闭式解，实现无需额外数据的高效训练。

### 流程模块与输入输出

DRPO 的训练流程由五个核心模块串联构成：

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| **正负样本划分** | 根据正确性奖励将每个问题的生成回答分为正组 $S_q^+$ 和负组 $S_q^-$ | 当前策略 $\pi_{\text{old}}$ 的采样结果 | 正样本集、负样本集 |
| **长度奖励权重计算** | 对正样本使用闭式最优分布计算重要性权重 | 正样本集、长度奖励函数 $r_l(o)$ | 归一化权重 $\omega(o|q)$ |
| **加权得分项** | 计算正样本加权对数似然得分 | 正样本集、权重、当前策略 | 加权期望得分 |
| **负样本惩罚项** | 通过 log-sum-exp 聚合负样本得分，实现判别式下降 | 负样本集、当前策略 | 负样本惩罚值 |
| **KL 散度正则化与模型更新** | 通过惩罚函数约束策略偏离，AdamW 更新模型 | 上述损失项、参考策略 | 更新后的策略 $\pi_\theta$ |

### 核心公式流

整个框架的数学推导从 DisCO 判别式目标出发：

$$
\max_{\theta} \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right], \quad \text{s.t. } \mathbb{D}_{\mathrm{KL}}(\pi_{\mathrm{old}} || \pi_{\theta}) \leq \delta
$$

DRPO 的关键创新在于将长度奖励 $r_l(o) = 1 - \frac{|o|}{C}$ 整合进正样本的分布中，推导出满足 KL 约束的闭式最优正样本分布：

$$
P_q^*(o) = \frac{\pi_{\mathrm{old}}^+(o|q) \exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)}
$$

该分布作为重要性权重直接嵌入 DisCO 目标，得到 DRPO 最终优化目标：

$$
\max \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \frac{\exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right]
$$

其中 $\lambda$ 控制长度惩罚的强度：$\lambda = +\infty$ 时权重退化为 1，目标退化为 DisCO；较小的 $\lambda$ 则赋予短回答更高的权重。KL 约束通过惩罚函数 $\beta_0 [\mathbb{D}_{\mathrm{KL}}(\pi_{\text{old}} || \pi_{\theta}) - \delta]^2_+$ 处理。

### 与基线方法的关键差异

与现有长度惩罚方法相比，DRPO 的核心差异体现在三个维度：

| 维度 | 基线方法（RLOO-LP、ALP、HAPO 等） | DRPO |
|------|------|------|
| **优势计算** | 组相对优势，正负样本混合归一化 | 解耦优势，长度奖励仅在正样本组内归一化 |
| **目标形式** | GRPO/DisCO 目标 + 显式长度惩罚 | 判别式目标 + 长度奖励驱动的正样本权重 |
| **长度惩罚整合** | 直接叠加到奖励值，影响优势计算 | 转化为重要性权重，无负样本干扰 |

这一框架使得 DRPO 在 GSM8K 上以 1.5B 模型实现了 77% 的长度缩减，性能损失仅 1.1%，而最佳基线在牺牲 4.3% 性能的情况下仅实现 68% 的长度缩减。

## 核心模块与公式推导

### 问题根源：GRPO 组相对优势的失效

标准 GRPO 的目标函数为：

$$
\mathcal { I } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } _ { q } \mathbb { E } _ { \{ o _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \mathrm { o l d } } ( \cdot | q ) } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { | \boldsymbol { o } _ { i } | } \sum _ { t = 1 } ^ { | \boldsymbol { o } _ { i } | } \operatorname* { m i n } \left( r _ { i , t } A ( o _ { i } | q ) , \mathrm { c l i p } ( r _ { i , t } , 1 - \epsilon , 1 + \epsilon ) A ( o _ { i } | q ) \right) \right] - \beta \mathbb { D } _ { \mathrm { K L } } ( \pi _ { \theta } | | \pi _ { \mathrm { r e f } } )
$$

其优势函数基于组内所有样本（正负混合）进行标准化：

$$
A ( o _ { i } | q ) = { \frac { r ( o _ { i } | q ) - \operatorname* { m e a n } ( r ( o _ { 1 } | q ) , r ( o _ { 2 } | q ) , \cdots , r ( o _ { G } | q ) ) } { \operatorname* { s t d } ( r ( o _ { 1 } | q ) , r ( o _ { 2 } | q ) , \cdots , r ( o _ { G } | q ) ) } }
$$

当引入长度惩罚后，冗长但正确的输出其奖励值被压低，导致其在组相对优势计算中可能转为负值。如 Figure 1 所示：正确性奖励为 `[1, 1, 1, 0, 0, 0]` 的 6 个回答，施加长度惩罚后变为 `[0.73, 0.6, 0.2, 0, 0, 0]`，第三个正确回答的优势值从 1 变为 -0.17，被错误地当作负样本抑制。这是 GRPO 系列方法在追求推理效率时的核心瓶颈。

### DRPO 的判别式基座：DisCO

DRPO 构建于 DisCO 框架之上，该框架将策略优化转化为判别式目标——直接最大化正样本得分、最小化负样本得分：

$$
\max_{\theta} \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right], \quad \text{s.t. } \mathbb{D}_{\mathrm{KL}}(\pi_{\mathrm{old}} || \pi_{\theta}) \leq \delta
$$

其中 $s_{\theta}(o,q)$ 为模型对回答 $o$ 的得分，$\tau$ 为温度参数控制负样本聚合的平滑度，KL 散度约束确保策略更新稳定。

### 解耦核心：长度奖励仅作用于正样本组

DRPO 的关键创新在于**解耦正负样本的学习信号**。定义线性长度奖励函数：

$$
r_l(o) = 1 - \frac{|o|}{C}
$$

其中 $C$ 为最大响应长度。DRPO 不将 $r_l(o)$ 直接加入奖励后做组相对优势，而是将其转化为正样本分布权重。在 KL 约束下，最大化长度奖励的最优正样本分布存在闭式解：

$$
P_q^*(o) = \frac{\pi_{\mathrm{old}}^+(o|q) \exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)}
$$

其中 $\lambda$ 为温度超参数，控制长度偏好的强度：$\lambda \to +\infty$ 时权重退化为均匀分布（等价于 DisCO）；$\lambda$ 越小，短回答的权重越大。

### 最终目标与梯度计算

将最优正样本分布代入 DisCO 目标，得到 DRPO 最终优化目标：

$$
\max \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \frac{\exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right], \quad \text{s.t. } \mathbb{D}_{\mathrm{KL}}(\pi_{\mathrm{old}} || \pi_{\theta}) \leq \delta
$$

该目标仅依赖 on-policy 数据，无需额外采样。正样本按长度奖励加权（权重仅在正样本组内归一化），负样本通过 log-sum-exp 聚合惩罚。KL 约束通过惩罚项 $\beta_0 [\mathbb{D}_{\mathrm{KL}}(\pi_{\mathrm{old}}||\pi_{\theta}) - \delta]^2_+$ 实现。

### 算法流程模块

DRPO 的训练流程由以下模块串联：

1. **正负样本划分**：对每个问题 $q$，根据正确性奖励将生成回答分为正组 $S_q^+$ 和负组 $S_q^-$。
2. **长度奖励权重计算**：对正样本使用闭式解 $\exp(r_l(o)/\lambda)$ 计算权重，并在正组内归一化。
3. **加权正样本得分**：计算 $\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+} \omega(o|q) s_{\theta}(o,q)$，短回答获得更高权重。
4. **负样本 log-sum-exp 惩罚**：计算 $\tau \log (\mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-} \exp(s_{\theta}(o',q)/\tau))$，压低所有负样本得分。
5. **KL 散度正则化**：通过惩罚函数约束策略更新幅度。
6. **模型更新**：使用 AdamW 优化器结合梯度估计更新 $\pi_\theta$。

## 实验与分析

### 核心瓶颈验证：GRPO 长度惩罚的误导性信号

现有方法（如 GRPO、RLOO-LP）将长度惩罚直接嵌入奖励函数，然后计算组相对优势（group-relative advantage）。这一设计存在根本性缺陷：当正确但冗长的回答与错误回答处于同一组时，其奖励值被长度惩罚压低后，组内标准化会将其优势值推至零以下（Figure 1）。例如，一个原本优势为 1 的正确回答，加入长度惩罚后优势变为 -0.17，被模型误判为负样本，从而抑制有效推理。Table 3 进一步展示了多种现有奖励设计（RLOO-LP、ALP、HAPO 等）产生负学习信号的案例，说明该问题并非 GRPO 独有，而是组相对优势框架的共性问题。

DRPO 的核心创新在于**解耦正负样本的奖励计算**：正确回答的长度奖励仅在正样本组内归一化，完全隔绝负样本的干扰。这一设计确保了冗长但正确的回答永远不会被推入负值区域，从根本上消除了误导性学习信号。

### 主实验结果

#### 性能-效率权衡全景

Figure 3 展示了 1.5B、7B、8B 三个模型规模下各方法的性能-效率权衡曲线。DRPO（蓝色）在所有模型规模上均呈现出最优的 Pareto 前沿：在相近的 Pass@1 均值下，DRPO 的生成长度显著短于 RLOO-LP、ALP、HAPO 等基线。以 7B 模型为例，DRPO（λ=0.1）将推理长度从基础模型的 4119 降至 1502（51% 缩减），性能仅损失 2.6%；而最优基线 RLOO-LP（α=0.2）在相近长度下性能损失更大。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/005_Figure_3.jpg]]
*Figure 3: Comparison of performance-efficiency trade-off. Left is for fine-tuning 1.5B model, middle is for fine-tuning 7B model and right is for fine-tuning 8B model. Grey lines represent the base model performance before finetuning, with generation length of 4698 for 1.5B model, 4119 for 7B model, and 4325 for 8B model. Squares denote models trained with reference methods without length penalties, i.e., $\lambda { = } + { \infty }$ (corresponding to DisCO) for DRPO, α = 0 for RLOO-LP, β = 0 (corresponding to GRPO) for ALP, w = 0 for HAPO. Triangle, star, and rhombus markers represent models trained by other works

关键定量结果：
- **GSM8K（1.5B）**：DRPO 实现 77% 长度缩减，性能损失仅 1.1%；最强基线以 4.3% 的性能损失仅换取 68% 的长度缩减。
- **AES 综合评分**（Table 1）：DRPO 在所有模型规模上均取得正值，且显著优于基线。1.5B 模型 AES = 0.178（RLOO-LP 最优仅 -0.129）；7B 模型 AES = 0.249（RLOO-LP 最优 -0.033）；8B 模型 AES = 0.297（RLOO-LP 最优 0.251）。AES 正值表示在维持或提升精度的同时有效缩短了输出长度。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/006_Table_1.jpg]]
*Table 1: Accuracy Efficiency Score (AES) Comparison with Baselines. The best AES score for each method is presented*

#### 难度分层分析

Figure 4 按数据集难度递增（GSM8K → MATH500 → OlympiadBench → AIME）展示了各方法的性能-效率权衡。DRPO 在简单问题（GSM8K）上实现了最显著的长度缩减（1.5B 模型 77.2%，7B 模型 73.1%），且性能几乎无损。随着难度增加，DRPO 仍保持优势，但长度缩减幅度收窄——这揭示了 λ 参数与问题难度的内在关联：困难问题需要更大的 λ 以保留推理能力，简单问题可用较小的 λ 大力压缩长度。

值得注意的是，7B 模型在所有数据集上的推理长度均短于 1.5B 模型，表明更大模型天然倾向于更简洁的推理，DRPO 进一步放大了这一优势。

#### 逻辑推理任务泛化

Figure 5 展示了在逻辑谜题推理任务上的结果。DRPO 同样取得了最优的 Pass@1 均值（~0.95-0.98），且输出长度最短（~1400-1800 tokens），而 RLOO-LP 和 ALP 在相近长度下精度明显更低。这验证了 DRPO 的解耦策略在数学之外的推理任务上也具有泛化能力。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/021_Figure_5.jpg]]
*Figure 5: Comparison of performance-efficiency trade-off on logical puzzle reasoning task. Squares denote models trained with reference methods without length penalties, i.e., λ=+∞ (corresponding to DisCO) for DRPO, $\alpha$ = 0 for $\mathtt { R L O O - L P } , \beta$ = 0 (corresponding to GRPO) for $\mathbf { A } \mathbf { L } \mathbf { P }$ , w = 0 for HAPO. Triangles denote the models trained by other works

### 训练动力学

Figure 2 展示了不同 λ 下 DRPO 的训练过程。λ = +∞ 对应 DisCO（无长度奖励），作为参考基线。随着 λ 减小，长度惩罚力度增强，生成长度显著下降。λ = 0.1 在 1.5B 和 7B 模型上均实现了超过 50% 的长度缩减。训练曲线显示，DRPO 的收敛过程平稳，未出现因长度惩罚导致的性能崩塌，这得益于其将长度信号作为正样本权重而非直接修改奖励的优势计算。

### 消融研究：长度奖励函数设计

Figure 6 对比了三种长度奖励函数：
- **线性奖励**：$r_l(o) = 1 - |o|/C$（DRPO 默认）
- **凹奖励**：$r_l(o) = 1 - (|o|/C)^2$
- **余弦奖励**：$r_l(o) = 0.5 + 0.5\cos(\pi|o|/C)$

结果显示，线性奖励提供了最广的性能-效率权衡谱，允许通过调节 λ 灵活控制长度压缩力度。凹奖励和余弦奖励在相同 λ 下倾向于获得更高精度，但以更长的推理长度为代价。这一现象的原因是：凹函数和余弦函数在中等长度区域的奖励梯度更平缓，对冗长回答的惩罚力度较弱。线性奖励的均匀梯度使其成为默认选择，但凹/余弦设计在精度优先的场景下具有实用价值。

### 公平性说明

所有方法均在相同条件下比较：
- 训练数据统一使用 DeepScaleR-Preview 数据集（40.3k QA 对）
- 基础模型均为 DeepSeek-R1-Distill 系列，训练 1000 步，每 200 步评估
- 生成预算统一为 8k tokens，temperature=0.6，top-p=0.95
- 各基线超参数在原作者推荐范围内调优（RLOO-LP α∈{0.05,0.1,0.2}，ALP β∈{1e-9,1e-8,1e-7} 等）

### 失败模式与局限

1. **固定长度奖励的适应性不足**：当前 $r_l(o) = 1 - |o|/C$ 对所有问题使用相同的 C 和 λ，未考虑问题难度差异。Figure 4 已暗示简单问题可承受更强的长度压缩，困难问题则需要保留更多推理空间。手动调节 λ 可以缓解，但缺乏自动化机制。

2. **任务覆盖有限**：实验仅在数学推理（GSM8K、MATH500、OlympiadBench、AIME）和逻辑谜题上进行，代码生成、科学问答等更广泛推理任务上的表现需要进一步验证。

3. **大模型行为未知**：当前实验上限为 8B 模型，更大规模模型（如 70B+）上的长度惩罚效果和超参数敏感性尚未探索。

4. **与过程奖励的协同未探索**：DRPO 的框架理论上可以整合过程奖励（如步骤正确性），但该方向仍为开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/024_Table_4.jpg]]
*Table 4: Detailed AES performance for 1.5B models*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_GP5RHZnEsw/figures/025_Table_5.jpg]]
*Table 5: Detailed AES performance for 7B models*

## 方法谱系与知识库定位

### 核心瓶颈：GRPO 组相对优势的负向信号陷阱

DRPO 的出发点直指 GRPO（Group Relative Policy Optimization）与长度惩罚结合后的一个隐蔽失败模式。在 GRPO 中，每个回答的优势值通过组内标准化计算：

$$A ( o _ { i } | q ) = { \frac { r ( o _ { i } | q ) - \operatorname* { m e a n } ( r ( o _ { 1 } | q ) , r ( o _ { 2 } | q ) , \cdots , r ( o _ { G } | q ) ) } { \operatorname* { s t d } ( r ( o _ { 1 } | q ) , r ( o _ { 2 } | q ) , \cdots , r ( o _ { G } | q ) ) } }$$

当引入长度惩罚后，冗长但正确的回答的奖励值被压低，其组相对优势可能跌入负值区间。论文给出具体示例：假设 6 个回答的正确性奖励为 `[1, 1, 1, 0, 0, 0]`，施加长度惩罚后变为 `[0.73, 0.6, 0.2, 0, 0, 0]`，第三个正确回答的优势从 +1 骤降至 -0.17（Figure 1）。这意味着 GRPO 被误导，将有效的冗长推理视为负样本进行抑制，形成显著的优化障碍。

这一发现揭示了现有方法的根本缺陷：**正负样本的奖励信号在组内标准化过程中相互污染**。所有基于 GRPO 框架引入长度惩罚的变体——包括 RLOO-LP、ALP、HAPO 等——都受困于同一机制性缺陷（Table 3 给出了各方法产生误导性学习信号的示例）。

### 解耦机制：从奖励修正到分布优化

DRPO 的解决方案并非在奖励函数层面修修补补，而是从优化目标的结构入手，实现**正负样本学习信号的彻底解耦**。其技术路线分为两步：

**第一步：判别式基座的选择。** DRPO 放弃了 GRPO 的策略梯度框架，转而建立在 DisCO（Li et al., 2025a）的判别式约束策略优化之上。DisCO 的目标函数直接最大化正样本得分、最小化负样本的 log-sum-exp 得分：

$$\max_{\theta} \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right], \quad \text{s.t. } \mathbb{D}_{\mathrm{KL}}(\pi_{\mathrm{old}} || \pi_{\theta}) \leq \delta$$

这一框架天然区分正负样本，为解耦提供了结构基础。

**第二步：长度奖励作为正样本分布权重。** DRPO 的核心创新在于，将长度奖励转化为正样本的分布权重，而非直接修改奖励值。给定长度奖励函数 $r_l(o) = 1 - \frac{|o|}{C}$，DRPO 推导出在 KL 约束下最大化长度奖励的最优正样本分布：

$$P_q^*(o) = \frac{\pi_{\mathrm{old}}^+(o|q) \exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)}$$

该闭式解是 DRPO 的理论支柱。将其代入 DisCO 目标，得到最终 DRPO 目标：

$$\max \mathbb{E}_q \left[ \mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \frac{\exp(r_l(o)/\lambda)}{\mathbb{E}_{o \sim \pi_{\mathrm{old}}^+(\cdot|q)} \exp(r_l(o)/\lambda)} s_{\theta}(o,q) - \tau \log \left( \mathbb{E}_{o' \sim \pi_{\mathrm{old}}^-(\cdot|q)} \exp \left( \frac{s_{\theta}(o',q)}{\tau} \right) \right) \right]$$

关键性质：**权重归一化仅在正样本组内进行**，负样本完全不参与长度奖励的计算。冗长的正确回答被赋予较小权重（弱化学习信号），但永远不会被推入负向区域。当 $\lambda = +\infty$ 时，DRPO 退化为 DisCO，保证了方法的连续可调性。

### 与基线方法的关系定位

DRPO 与现有高效推理方法的本质差异在于**信号解耦的层级**：

| 方法 | 长度惩罚机制 | 正负信号关系 | 核心局限 |
|------|-------------|-------------|---------|
| **RLOO-LP** | 长度惩罚直接加入奖励，RLOO 优势估计 | 耦合：负样本拉低组均值，影响正样本优势 | 冗长正确回答可能获得负优势 |
| **ALP** | 基于通过率的自适应长度惩罚 | 耦合：同 GRPO 框架 | 仍受组标准化污染 |
| **HAPO** | 惩罚长于最短正确回答的响应 | 耦合：同 GRPO 框架 | 过度惩罚合理冗长推理 |
| **L1-max** | 长度约束推理模型 | 架构级约束 | 灵活性受限 |
| **SB**（Yi et al., 2025）| 匹配最短正确回答长度 | 耦合 | 忽视问题难度差异 |
| **LASER-D**（Liu et al., 2025b）| 难度感知的动态目标长度 | 耦合 | 依赖难度估计准确性 |
| **DRPO** | 长度奖励作为正样本分布权重 | **解耦**：权重仅在正组内归一化 | 长度奖励函数固定，未自适应难度 |

DRPO 的方法贡献可以总结为三个关键槽位的变更：优势计算从“全组相对”变为“正组内归一化”；目标函数从 GRPO 策略梯度变为判别式 DisCO 框架；长度惩罚从“奖励修正”变为“重要性权重”。

### 适用边界与局限

**已验证的适用范围：**
- 模型规模：1.5B、7B、8B 参数量的 DeepSeek-R1-Distill 系列
- 任务领域：数学推理（GSM8K、MATH500、OlympiadBench、AIME）和逻辑推理
- 训练数据：DeepScaleR-Preview-Dataset（40.3k QA 对）
- 生成预算：8k tokens

**明确的局限：**
1. **长度奖励函数固定**：当前使用线性函数 $r_l(o) = 1 - |o|/C$，未根据问题难度自适应。消融实验（Figure 6）表明，线性奖励提供最广的权衡谱，而凹奖励和余弦奖励在牺牲一定长度的情况下获得更高精度，但均未实现难度自适应。
2. **任务泛化未验证**：实验仅在数学和逻辑推理任务上进行，在代码生成、科学问答等推理任务上的有效性需要进一步验证。
3. **超参数敏感性**：$\lambda$ 的绝对值设置可能因模型规模和数据分布而异，论文仅给出了经验性的调节方向（简单问题用较小 $\lambda$，困难问题用较大 $\lambda$）。
4. **与过程奖励的结合未探索**：DRPO 的框架理论上可以扩展至过程奖励或其他偏好奖励（论文在结论中提及），但尚未实现。

### 开放问题

1. **自适应 $\lambda$ 机制**：如何根据问题难度动态调整正则化权重？Figure 4 的结果暗示了难度与最优 $\lambda$ 之间的关联，但缺乏自动化的调节方案。
2. **任务扩展**：DRPO 在代码生成、科学推理等需要更长推理链的任务上是否仍能保持高效权衡？
3. **长度奖励函数设计**：能否设计基于推理步骤正确性的更精细的长度奖励，以进一步提升性能-效率权衡的上界？
4. **更大规模验证**：当前最大实验规模为 8B 参数，DRPO 在更大模型上的行为尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2026/DRPO_Efficient_Reasoning_via_Decoupled_Reward_Policy_Optimization.pdf]]
