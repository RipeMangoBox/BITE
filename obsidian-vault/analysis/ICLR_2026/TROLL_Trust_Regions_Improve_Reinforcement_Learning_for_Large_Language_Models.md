---
title: "TROLL: Trust Regions Improve Reinforcement Learning for Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TROLL_Trust_Regions_Improve_Reinforcement_Learning_for_Large_Language_Models.pdf
project_link: https://niklasfreymuth.github.io/troll/
code_link: null
openreview_forum_id: X9D5MVpPJ9
aliases:
- TTROLLM
- TROLL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "用可微的离散信任区域投影（TROLL）替代 PPO 的剪裁目标，对每个 token 施加精确的 KL 散度约束。"
primary_logic: "通过将策略更新限制在信任区域内，能够稳定优化过程；结合可微投影与基于概率质量的稀疏化方案，使得严格的 token‑级 KL 约束能够高效扩展到现代大语言模型的大规模词表。"
claims:
- "在数学推理（DAPO‑Math）和代码生成（Eurus‑Code）任务上，TROLL 始终带来更高的训练效率和最终成功率。"
- "TROLL 使 GSPO 稳定收敛，而 Clip 导致发散（成功率为 0）。"
- "TROLL 在训练中保持更高的 token 熵，同时获得更高的成功率，无明显熵崩溃。"
- "TROLL 对批次大小变化鲁棒，而 Clip 随批大小增加性能下降。"
---

# TROLL: Trust Regions Improve Reinforcement Learning for Large Language Models

> [!tip] 核心洞察
> 通过将策略更新限制在信任区域内，能够稳定优化过程；结合可微投影与基于概率质量的稀疏化方案，使得严格的 token‑级 KL 约束能够高效扩展到现代大语言模型的大规模词表。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TROLL：通过信任区域改进大语言模型的强化学习 |
| 英文题名 | TROLL: Trust Regions Improve Reinforcement Learning for Large Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=X9D5MVpPJ9) · [Project](https://niklasfreymuth.github.io/troll/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TROLL (Trust Region Optimization for Large Language models) |
| Dataset | DAPO‑Train (Qwen3‑8B GRPO), DAPO‑Eval (Qwen3‑8B GRPO), MATH‑Eval (Qwen3‑8B GRPO), DAPO‑Train (Qwen2.5‑7B‑Instruct GRPO) |

> [!tip] 效果简介
> - DAPO‑Train (Qwen3‑8B GRPO) 上，Success Rate 为 0.721，对比 0.667，变化 +0.054。
> - DAPO‑Eval (Qwen3‑8B GRPO) 上，Success Rate 为 0.691，对比 0.640，变化 +0.051。
> - MATH‑Eval (Qwen3‑8B GRPO) 上，Success Rate 为 0.551，对比 0.541，变化 +0.010。

## 概要

当前大语言模型（LLM）的强化学习（RL）训练普遍依赖 PPO 式的剪裁目标来近似信任区域约束。然而，这种启发式剪裁缺乏严格的数学基础，对超参数敏感，容易导致训练不稳定、更新偏斜，并在大规模训练中引发熵崩溃——这些因素共同限制了 LLM 强化学习的性能上限。

**TROLL**（Trust Region Optimization for Large Language models）针对这一瓶颈提出了根本性的替代方案：用**可微信任区域投影**取代 PPO 的剪裁目标。其核心思想是对每个 token 施加精确的 KL 散度约束，将策略更新严格限制在信任区域内，从而稳定优化过程。为将这一严格约束高效扩展到现代 LLM 的大规模词表（如 Qwen3 的 151,936 维），TROLL 引入了基于概率质量的稀疏化方案，仅保留高概率 token 进行计算，使额外开销相对于模型训练显存可忽略。

在数学推理（DAPO-Math）和代码生成（Eurus-Code）任务上，TROLL 在多种模型规模（600M–14B）和多种优势估计方法（GRPO、Dr.GRPO、GSPO、REINFORCE++、BAPO、GPG）下均一致优于 PPO 剪裁基线。关键证据包括：
- 在 Qwen3-8B 的 GRPO 训练中，TROLL 将 DAPO 训练成功率从 0.667 提升至 0.721，评估成功率从 0.640 提升至 0.691（Table 1）；
- 在 GSPO 方法上，PPO 剪裁导致训练发散（成功率为 0），而 TROLL 使 GSPO 稳定收敛至 0.736（Table 1）；
- TROLL 在训练过程中保持更高的 token 熵，同时获得更高成功率，有效避免了剪裁方法常见的熵快速坍塌（Figure 5）。

TROLL 作为 PPO 剪裁目标的直接替代，不改变模型推理过程，仅在训练时引入额外投影步骤。其方法定位处于 RL for LLM 中策略优化约束机制的核心位置，为后续在更大规模模型、多模态场景及 RLHF 等任务中的扩展提供了严格且可微的信任区域基础。



### 1. LLM 强化学习的瓶颈：PPO 剪裁的粗糙信任区域

基于人类反馈的强化学习（RLHF）和基于可验证奖励的强化学习（RLVR）已成为大语言模型（LLM）后训练的核心范式。在这些范式中，策略优化算法（如 PPO、GRPO）需要限制新旧策略之间的差异，以防止策略崩溃或训练不稳定。当前的主流做法是采用 **PPO 式剪裁目标**（PPO-clipped surrogate objective，Schulman et al., 2017）：

$$
\mathcal { I } _ { \mathrm { p p o } } ( \theta ) = \mathbb { E } _ { o _ { t } \sim \pi _ { \mathrm { o l d } } ( o | q ) \mathcal { D } ( q ) } \left[ \frac { 1 } { | o | } \sum _ { t = 1 } ^ { | o | } \operatorname* { m i n } \left( r _ { t } A _ { t } ; \operatorname { c l i p } \left( r _ { t } , 1 - \epsilon _ { \mathrm { p p o } } , 1 + \epsilon _ { \mathrm { p p o } } \right) A _ { t } \right) \right]
$$

该目标通过将重要性采样比率 $r_t$ 硬性截断在 $[1-\epsilon, 1+\epsilon]$ 区间内来近似信任区域约束。然而，这种剪裁机制存在本质缺陷：

- **缺乏严格数学约束**：剪裁是对 KL 信任区域的粗糙近似，并不保证更新后的策略真正位于旧策略的 KL 球内。它仅对超出边界的 token 施加零梯度，而非将其拉回可行域。
- **训练不稳定与更新偏斜**：当 $r_t$ 超出剪裁区间时，梯度信号完全消失，导致有效训练样本减少；同时，剪裁无法区分 token 级别的分布偏移程度，对高频和低频 token 施加相同的刚性约束。
- **对超参数敏感**：剪裁边界 $\epsilon_{\text{ppo}}$ 的选择高度影响训练动态——过小则限制探索，过大则失去约束效果。此外，剪裁对批次大小变化敏感，大批次下性能退化明显（Figure 16）。

这些缺陷在序列级优化方法（如 GSPO，Zheng et al., 2025）中尤为突出：**GSPO 搭配 Clip 在训练中直接发散，成功率降至 0**（Table 1），而搭配 TROLL 则稳定收敛且达到 0.736 的成功率。这暴露了剪裁机制在需要更精确信任区域约束的场景下的根本性失效。

### 2. 现有方法的局限与缺口

LLM 强化学习的策略优化方法近年来经历了快速迭代。除 PPO 外，**GRPO**（Shao et al., 2024）通过组内相对优势估计消除了对价值模型的需求；**Dr.GRPO**（Liu et al., 2025）修正了 GRPO 的长度偏置；**REINFORCE++**（Hu et al., 2025）集成了全局优势归一化；**BAPO**（Xi et al., 2025）自适应调节剪裁边界；**GPG**（Chu et al., 2025）则完全放弃了剪裁。然而，这些方法的核心策略更新机制仍依赖于 PPO 的剪裁目标或其变体，**均未从根本上解决信任区域约束的精确性问题**。

在连续动作空间中，信任区域方法（如 TRPO）已证明其有效性，但在 LLM 的离散大词表（如 Qwen3 的 151,936 维）上，直接应用 KL 约束投影面临两大挑战：

- **计算不可行性**：对每个 token 维护稠密分布并在全词表上求解 KL 投影，其存储和计算开销随词表大小线性增长，在现代 LLM 上无法承受。
- **可微性难题**：投影操作本身是一个约束优化问题，如何在保持端到端可微性的同时高效求解，是将其集成到深度学习训练流程中的关键障碍。

### 3. TROLL 的动机与核心思路

TROLL 的出发点是：**用可微的离散信任区域投影替代 PPO 的启发式剪裁，对每个 token 施加精确的 KL 散度约束**。其核心洞察在于：

> 通过将策略更新限制在严格的信任区域内，能够稳定优化过程；结合可微投影与基于概率质量的稀疏化方案，使得 token 级的严格 KL 约束能够高效扩展到现代 LLM 的大规模词表。

具体而言，TROLL 在三个维度上突破了现有瓶颈：

1. **精确约束替代粗糙剪裁**：对每个 token，TROLL 求解一个凸优化问题，将当前策略投影到以旧策略为中心的 KL 信任区域上（Figure 1 Left）。当更新不违反约束时，投影退化为恒等映射；当约束被激活时，投影给出满足 KL 约束且最接近当前策略的分布。这保证了每一次更新都在理论上严格的信任区域内。

2. **可微投影保持梯度流**：通过隐式微分（OptNet 风格），TROLL 使整个投影步骤保持可微性。即使约束被激活，梯度仍能从 RL 目标通过投影操作回传至模型参数（Figure 6），避免了 PPO 剪裁中梯度截断导致的信号丢失。

3. **稀疏化实现高效扩展**：TROLL 利用 KL 投影的几何性质——投影方向仅依赖于高概率 token——设计了一种稀疏化方案：仅保留累积概率质量达到 $1-\delta$ 的 top-K 个 token，其余 token 赋予微小默认质量。理论分析（Theorem A.2）证明，该近似引入的额外 KL 误差上界比信任区域阈值小约两个数量级，在所选超参数下可忽略不计。这使得 TROLL 的存储开销降至 MiB 级别，且投影开销不随模型尺寸增长（Table 5）。

### 4. 预期贡献

基于上述动机，TROLL 旨在实现以下目标：

- 在数学推理（DAPO-Math）和代码生成（Eurus-Code）等 RLVR 任务上，相较于 PPO 剪裁基线，持续提升训练效率和最终成功率（Figure 1 Right, Figure 3）。
- 使不稳定的序列级优化方法（如 GSPO）能够稳定收敛。
- 在训练过程中保持更高的 token 熵，避免剪裁常伴随的熵快速坍塌（Figure 5 Bottom Right）。
- 以可忽略的额外开销（4B 模型上运行时增量不足 10%）实现上述收益，使其成为 PPO 剪裁的实用替代方案。



## 核心方法与创新机理

### 瓶颈：PPO 剪裁的信任区域近似缺陷

当前大语言模型（LLM）强化学习的主流范式依赖 PPO 的剪裁目标（Equation 2）来限制策略更新幅度。然而，这种启发式剪裁本质上是对 KL 信任区域的粗糙近似，存在三个关键缺陷：

1. **缺乏严格数学约束**：剪裁仅在重要性采样比率 $r_t$ 超出 $[1-\epsilon_{\mathrm{ppo}}, 1+\epsilon_{\mathrm{ppo}}]$ 时截断梯度，而非施加明确的分布散度限制，导致信任区域形同虚设。
2. **梯度信号断裂**：当比率被剪裁时，对应 token 的梯度直接归零，造成有效训练信号丢失。
3. **超参数敏感**：剪裁边界 $\epsilon_{\mathrm{ppo}}$ 的选择高度依赖任务和模型规模，且训练稳定性随批次大小增大而退化（Figure 16）。

这些缺陷限制了 LLM 强化学习的性能上限。特别是在 **GSPO**（Zheng et al., 2025）等序列级优化方法中，剪裁直接导致训练发散、成功率为 0（Table 1）。

### 核心机制：可微离散信任区域投影

TROLL 的核心创新是用**可微的离散信任区域投影**替代 PPO 的剪裁目标，对每个 token 施加精确的 KL 散度约束。

#### 投影优化问题

对于每个 token，TROLL 求解如下凸优化问题（Equation 3）：

$$\pi_{\theta}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) = \underset{\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})}{\mathrm{argmin}} \ \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) \| \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})) \ \mathrm{s.t.} \ \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) \| \pi_{\mathrm{old}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})) \leq \epsilon$$

其物理含义是：寻找一个既尽可能接近当前策略 $\tilde{\pi}_{\theta}$，又与旧策略 $\pi_{\mathrm{old}}$ 的 KL 散度不超过阈值 $\epsilon$ 的分布。该问题的闭式解为两策略对数概率的几何插值（Equation 4）：

$$\pi_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t}) \propto \exp\left( \frac{\eta^{*} \log \pi_{\mathrm{old}}(o_{t} \mid \mathbf{q}, o_{<t}) + \log \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t})}{\eta^{*} + 1} \right)$$

其中最优步长 $\eta^{*}$ 通过求解一维凸对偶问题获得（Algorithm 1 lines 10–15）。

#### 关键设计：KL 回归损失

TROLL 的完整目标函数（Equation 5）在投影分布上计算重要性加权优势，并附加一个从当前策略到投影分布的 KL 回归项：

$$\mathcal{T}_{\mathrm{Troll}}(\theta) = \mathbb{E}_{o_{t} \sim \pi_{\mathrm{old}}(o \mid q) \mathcal{D}(q)} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \left( \frac{\pi_{\theta}(o_{t} \mid q, o_{<t})}{\pi_{\mathrm{old}}(o_{t} \mid q, o_{<t})} A_{t} \right) - \alpha \, \mathrm{KL}\big( \tilde{\pi}_{\theta}(o_{t} \mid q, o_{<t}) \,\|\, \lfloor \pi_{\theta}(o_{t} \mid q, o_{<t}) \rfloor \big) \right]$$

其中 $\lfloor \cdot \rfloor$ 表示 stop-gradient 操作，$\alpha$ 固定为 1。该设计使策略更新始终朝向信任区域内的投影分布，即使约束被激活仍保持有效梯度流。

#### 可微性保证

TROLL 通过 **OptNet** 框架（Amos & Kolter, 2017）对投影步骤的 KKT 条件进行隐式微分，确保整个投影过程可微（Figure 6; Listing 2）。这解决了 PPO 剪裁的梯度断裂问题。

### 工程创新：概率质量驱动的稀疏化

现代 LLM 的词表规模巨大（如 Qwen3 的 151,936 维），在全词表上维护稠密分布并逐 token 求解投影问题将带来不可承受的计算开销。TROLL 的第二个关键创新是**基于概率质量的稀疏化方案**（Section 3.2）：

1. **Top-K 选取**：对每个 token 的 logits 取概率最大的 K 个 token，保留累积质量 $\geq 1-\delta$ 的最小子集，并始终保留实际采样的 token。
2. **默认质量分配**：其余 token 被赋予微小默认质量 $q_{\min}$，重新归一化后形成稀疏分布。

在默认超参数 $K=64, \delta=10^{-5}$ 下，该方案平均仅需 5–10 个 token 即可保留 99.999% 的概率质量。理论分析（Theorem A.2）证明，稀疏化引入的额外 KL 误差上界为：

$$\mathbf{KL}(p \parallel q) \le \gamma^{-1} \mathrm{KL}(p' \parallel q') + \delta \log \frac{\delta}{q_{\min}}$$

该误差比信任区域阈值 $\epsilon$ 小约两个数量级，在工程上可忽略。同时，投影开销不随模型尺寸增长，在 4B 模型上运行时增量不足 10%（Figure 5 Top Right; Table 5）。

### 与 Baseline 的差异总结

| 设计维度 | PPO/GRPO 等基线 | TROLL |
|---------|----------------|-------|
| 信任区域机制 | 启发式比率剪裁（Equation 2） | 可微 KL 投影（Equation 3–4） |
| 梯度信号 | 超出边界时梯度归零 | 隐式微分保持全流程可微 |
| 分布表示 | 稠密全词表分布 | 概率质量驱动的稀疏化（$K=64, \delta=10^{-5}$） |
| 目标函数 | 纯剪裁比率损失 | 投影比率损失 + KL 回归（Equation 5） |

这些创新使 TROLL 成为一个可直接替换 PPO 剪裁的即插即用模块（Figure 2），在不改变模型推理过程的前提下，显著提升训练稳定性和最终性能。



![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/003_Figure_1.jpg]]
*Figure 1: Trust Region Optimization for Large Language models (TROLL) overview. (Left) Example of a 3-token distribution (cat, troll, hamster). The old policy favors the troll, while the new policy shifts toward the hamster. The projection ensures that the updated policy stays within the trust region (circle). (Right) TROLL yields clear performance gains over PPO-like clipping (CLIP) on mathematical reasoning and code generation tasks, as shown for Qwen3-14B trained with GRPO*

TROLL 的整体设计遵循一个简洁的“替换即用”理念：将 PPO 中启发式的剪裁目标替换为一个**可微的离散信任区域投影**，在不改变模型推理过程的前提下，为每个 token 施加严格的 KL 散度约束。整个训练 pipeline 由三个核心模块串联而成，数据流依次为稀疏化 → 信任区域投影 → 策略比率损失计算。

### 训练流程概览

Figure 2 给出了 TROLL 训练流程的示意。对于一条从经验回放缓冲区中采样的序列，旧策略 $\pi_{\mathrm{old}}$ 记录了收集该序列时的输出分布，当前策略 $\tilde{\pi}_{\theta}$ 则给出最新的输出分布。TROLL 对序列中的每个 token 执行以下步骤：

1. **稀疏化模块**：从当前策略和旧策略的全词表 logits 中，选取累积概率质量达到 $1-\delta$ 的 top‑K 高概率 token，其余 token 赋予微小默认质量。这一步将 15 万维的词表压缩到平均 5–10 个有效 token，使后续投影的计算和存储开销与词表大小解耦。

2. **信任区域投影（对偶求解器）**：对每个 token，求解一个一维凸对偶问题，得到最优步长 $\eta^*$，然后计算投影分布 $\pi_{\theta}$。该分布是当前策略与旧策略对数概率的几何插值（Equation 4），保证其与旧策略之间的 KL 散度不超过预设阈值 $\epsilon$，同时尽可能靠近当前策略。

3. **策略比率 + KL 回归损失**：使用投影后的分布 $\pi_{\theta}$ 计算重要性加权优势（即 $\frac{\pi_{\theta}}{\pi_{\mathrm{old}}} A_t$），并加入一个从当前策略 $\tilde{\pi}_{\theta}$ 到投影分布 $\pi_{\theta}$ 的 KL 回归项（对 $\pi_{\theta}$ 施加 stop‑gradient），强制当前策略向信任区域内的投影分布靠拢。最终的 TROLL 目标函数如 Equation 5 所示。

### 模块关系与关键设计

三个模块之间的依赖关系清晰：**稀疏化是投影的前置条件**，它将稠密分布压缩为稀疏表示，使投影求解仅需处理少量 token；**投影是损失计算的基础**，它提供了满足 KL 约束的“目标分布”，策略比率项和 KL 回归项都建立在该分布之上。整个流程通过 OptNet 框架的隐式微分保持端到端可微——即使某个 token 的 KL 约束被激活（$\eta^* > 0$），梯度仍能通过 KKT 条件反向传播至策略参数，避免了 PPO 剪裁在约束边界处梯度截断的问题。

Figure 1 (Left) 用一个 3‑token 的简化示例直观展示了投影的几何意义：旧策略偏好 “troll”，新策略向 “hamster” 偏移，投影确保更新后的策略停留在以旧策略为中心的 KL 信任区域（圆）内，从而防止单步更新过大的策略偏移。

### 与 PPO 剪裁的对比

Table 1 的系统性对比揭示了两种信任区域实现方式的本质差异：PPO 的剪裁目标（Equation 2）仅在重要性比率超出 $[1-\epsilon_{\mathrm{ppo}}, 1+\epsilon_{\mathrm{ppo}}]$ 时截断梯度，这是一种**无严格数学约束的启发式近似**；而 TROLL 通过求解凸优化问题（Equation 3）对每个 token 施加**精确的 KL 散度上界**，其投影解具有闭式形式（Equation 4），且整个过程保持可微。这一设计差异直接导致了 GSPO 方法上的关键结果：GSPO (Clip) 在训练中发散（成功率为 0），而 GSPO (TROLL) 稳定收敛至 0.736（Qwen3‑8B），表明严格的 token‑级信任区域约束对于序列级策略优化方法的稳定性至关重要。



### 瓶颈与设计动机

当前主流的 LLM 强化学习微调普遍采用 PPO 的剪裁替代目标（clipped surrogate objective）来近似信任区域约束：

$$
\mathcal{I}_{\mathrm{ppo}}(\theta) = \mathbb{E}_{o_{t} \sim \pi_{\mathrm{old}}(o \mid q) \mathcal{D}(q)} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \min\left( r_{t} A_{t}, \operatorname{clip}\left( r_{t}, 1-\epsilon_{\mathrm{ppo}}, 1+\epsilon_{\mathrm{ppo}} \right) A_{t} \right) \right]
$$

该剪裁机制存在根本性缺陷：它是一种启发式近似，缺乏严格的数学约束。当策略比率 $r_t$ 超出 $[1-\epsilon, 1+\epsilon]$ 区间时梯度被直接截断为零，导致更新偏斜、训练不稳定，且对超参数（如 $\epsilon_{\mathrm{ppo}}$、批次大小）高度敏感。这限制了 LLM 强化学习的性能上限。

TROLL 的核心洞察是：**用可微的离散信任区域投影替代 PPO 的剪裁目标，对每个 token 施加精确的 KL 散度约束**，从而稳定优化过程。

### 模块一：信任区域投影（Trust Region Projection）

TROLL 将策略更新形式化为一个凸优化问题。对于每个 token，寻找一个分布 $\hat{\pi}_{\boldsymbol{\theta}}$，使其同时满足两个条件：(1) 尽可能接近当前模型输出的分布 $\tilde{\pi}_{\boldsymbol{\theta}}$；(2) 与旧策略 $\pi_{\mathrm{old}}$ 之间的 KL 散度不超过阈值 $\epsilon$：

$$
\pi_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) = \underset{\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})}{\mathrm{argmin}} \; \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) \| \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})) \quad \mathrm{s.t.} \quad \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) \| \pi_{\mathrm{old}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})) \leq \epsilon
$$

该问题的投影方向可解析求解，投影后的分布为当前策略与旧策略对数概率的几何插值：

$$
\pi_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t}) \propto \exp\left( \frac{\eta^{*} \log \pi_{\mathrm{old}}(o_{t} \mid \mathbf{q}, o_{<t}) + \log \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t})}{\eta^{*} + 1} \right)
$$

其中 $\eta^{*}$ 是通过求解一维凸对偶问题得到的最优步长。该对偶问题仅涉及标量求解，计算开销极低。

**关键机制**：当新旧策略间的 KL 散度未超过 $\epsilon$ 时，$\eta^{*}=0$，投影分布退化为当前策略 $\tilde{\pi}_{\boldsymbol{\theta}}$；当 KL 散度超出阈值时，$\eta^{*}>0$，投影分布向旧策略方向收缩，确保更新始终落在信任区域内。整个投影过程通过隐式微分（基于 OptNet 框架，Amos & Kolter, 2017）保持可微性，即使约束被激活仍有梯度信号。

### 模块二：稀疏化表示（Sparsification Module）

现代大语言模型的词表规模巨大（如 Qwen3 为 151,936 维），在全词表上维护稠密分布并进行投影计算代价过高。TROLL 利用投影分布的几何插值特性：**投影后分布的概率质量高度集中在当前策略与旧策略共同赋予高概率的 token 上**。

基于此，TROLL 对每个 token 的 logits 进行 top-K 选取：保留累积概率质量 $\geq 1-\delta$ 的最大概率 token，并额外保留实际被选中的 token；其余 token 被赋予微小默认质量后重新归一化。稀疏化引入的 KL 误差存在理论上界：

$$
\mathbf{KL}(p \parallel q) \le \gamma^{-1} \mathrm{KL}(p' \parallel q') + \delta \log \frac{\delta}{q_{\min}}
$$

在默认超参数 $K=64$、$\delta=10^{-5}$ 下，该误差比信任区域阈值 $\epsilon$ 小约两个数量级，可忽略不计。实际运行时仅需保留 5-10 个 token，存储与计算开销相对于 LLM 训练显存可忽略。

### 模块三：TROLL 完整训练目标

投影分布 $\pi_{\boldsymbol{\theta}}$ 用于计算重要性加权优势，同时引入从当前策略 $\tilde{\pi}_{\boldsymbol{\theta}}$ 到投影分布的 KL 回归项（对投影分布施加 stop-gradient），促使当前策略不偏离信任区域：

$$
\mathcal{T}_{\mathrm{Troll}}(\theta) = \mathbb{E}_{o_{t} \sim \pi_{\mathrm{old}}(o \mid q) \mathcal{D}(q)} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \left( \frac{\pi_{\boldsymbol{\theta}}(o_{t} \mid q, o_{<t})}{\pi_{\mathrm{old}}(o_{t} \mid q, o_{<t})} A_{t} \right) - \alpha \, \mathrm{KL}\big( \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid q, o_{<t}) \,\|\, \lfloor \pi_{\boldsymbol{\theta}}(o_{t} \mid q, o_{<t}) \rfloor \big) \right]
$$

其中 $\alpha$ 固定为 1，$\lfloor \cdot \rfloor$ 表示 stop-gradient 操作。该目标作为 PPO 剪裁目标的直接替代，可无缝集成到 GRPO、Dr.GRPO、GSPO 等现有优势估计框架中，仅更改策略更新部分，不改变模型推理过程。



## 实验与关键发现

### 主实验：数学推理与代码生成

TROLL 在数学推理（DAPO‑Math）与代码生成（Eurus‑Code）两大 RLVR 任务上进行了系统验证，覆盖 Qwen3（600M～14B）、Qwen2.5‑Instruct（500M～7B）及 Llama 等多个模型家族。所有对比方法共享相同的优势估计、学习率与批大小等超参数，仅将策略更新部分的 PPO‑like clipping 替换为 TROLL 的可微信任区域投影，确保公平比较。

**数学推理（DAPO）**：Table 1 给出 Qwen3‑8B 与 Qwen2.5‑7B‑Instruct 在五种优势估计方法（GRPO、Dr.GRPO、PPO、GSPO、RF++）下的最终成功率。在 Qwen3‑8B 上，TROLL 在 DAPO‑Train 上达到 0.721（Clip 为 0.667，+0.054），在 DAPO‑Eval 上达到 0.691（Clip 为 0.640，+0.051），在 MATH‑Eval 上达到 0.551（Clip 为 0.541，+0.010）。Qwen2.5‑7B‑Instruct 上趋势一致：DAPO‑Train 从 0.443 提升到 0.495（+0.052），DAPO‑Eval 从 0.323 提升到 0.389（+0.066）。Figure 3（上）的训练曲线进一步表明，TROLL 在所有模型规模上均带来更高的样本效率与收敛成功率，且该优势在 DAPO‑Eval 和 MATH‑Eval 上均成立。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/006_Table_1.jpg]]
*Table 1: Final train and evaluation success rates on DAPO for Qwen3-8B and Qwen2.5-7B-Instruct methods for different advantage estimation methods for TROLL and Clip. The better approach is marked in blue. TROLL significantly improves over Clip in most cases, and is able to successfully train GSPO, where Clip causes divergence and little to no success rates on both models*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/017_Figure_7.jpg]]
*Figure 7: Performance of TROLL and the Clip objective across Qwen2.5-Instruct models with 500M to 7B parameters trained with GRPO on DAPO. As in Figure 3, TROLL yields more sample-efficient training and higher rewards at convergence. These improvements extend both to evaluation on indistribution questions and to generalization on out-of-distribution test datasets. Smoothed values are shown in full opacity, with original curves in the background*

**代码生成（Eurus‑Code）**：Figure 3（下）显示 TROLL 在 Qwen3 系列上的提升尤为显著，成功率绝对提升 7～18 个百分点，相对增益达 18%～30%。Figure 1（Right）同样呈现 Qwen3‑14B 上 TROLL 对 Clip 的明显优势。

**跨模型泛化**：Figure 4 汇总了多模型、多数据集上的最终评估与训练曲线。TROLL 在 GSM8K 等数学数据集上普遍优于 Clip，且在 Llama 模型上展现出更快的收敛速度。Figure 7 进一步证实 TROLL 在 Qwen2.5‑Instruct 系列上的一致增益。

**关键失败模式：GSPO 的发散**。Table 1 中 GSPO 的结果构成最有力的对照证据。在 Qwen3‑8B 上，GSPO（Clip）的 DAPO‑Train 成功率为 0.000，即训练完全发散；而 GSPO（TROLL）达到 0.736，与 GRPO、PPO 等方法持平甚至更优。Qwen2.5‑7B‑Instruct 上同样出现 Clip 发散（0.000）而 TROLL 稳定收敛（0.693）的现象。Figure 8 的训练曲线直观展示了 GSPO（Clip）的崩溃过程与 GSPO（TROLL）的稳定优化轨迹。这表明 TROLL 的严格 token 级 KL 约束对于序列级重要性比率方法（GSPO）的稳定训练是必要的，而 PPO 的启发式剪裁无法提供足够的正则化。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/021_Table_4.jpg]]
*Table 4: Success rates for individual MATH test datasets for Qwen2.5-7B-Instruct and Qwen3-8B models trained on DAPO with different advantage estimation methods. TROLL provides consistent benefits across methods and evaluation tasks, showing well-balanced improvements in performance. It also successfully trains GSPO without divergence, wheres Clip eventually causes unstable updates, as shown in Figure 8 and Figure 9*

### 消融实验

**信任区域边界 ε 的影响**（Figure 5 Left）：较小的 KL 边界（ε 较小）会减慢训练速度，但不影响最终收敛性能；过大的 ε 则导致信任区域约束过松，成功率下降。这表明存在一个合理的 ε 区间，在此区间内 TROLL 对边界值不敏感，但超出后性能退化。

**稀疏化 token 数 K 的影响**（Figure 5 Left）：K=16 时保留的 token 过少，更新质量显著下降；K=256 增加了计算开销但未带来性能提升；K=64 在质量与效率之间取得良好平衡。结合默认 δ=10⁻⁵，实际平均仅需 5～10 个 token 即可保留 99.999% 的概率质量。

**熵动态分析**（Figure 5 Bottom Right；Figure 17）：TROLL 在训练过程中保持更高的平均 token 熵，同时获得更高的成功率。相比之下，Clip 常伴随熵的快速坍塌——策略过早地变得确定性，限制了探索与最终性能。这一现象在 Eurus‑Code 训练数据上同样被 Figure 17 证实：TROLL 的熵下降幅度更小，成功率更高。这表明严格的 KL 投影比启发式剪裁更有效地平衡了探索与利用。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/041_Figure_17.jpg]]
*Figure 17: TROLL and Clip entropy (left) and success rate (right) for different Qwen3 models trained with GRPO on the Eurus-Code training data. Smoothed values are shown in full opacity, with original curves in the background. TROLL generally causes less decrease in token entropy while Clip shows a strong negative correlation between success rate and entropy. The quick improvement of Qwen3-8B Clip around step 40 coincides with a rapid drop in entropy. Table 5: Max allocated VRAM and runtime of one iteration. The smallest 0.6B models does not fully saturate the GPU, so the Delta results differ from the larger models. The projection overhead is independent of the model size and already below ten percent...*

**计算与存储开销**（Figure 5 Top Right；Table 5）：TROLL 的稀疏分布存储开销相对于 LLM 训练的总显存可忽略不计。投影步骤的开销不随模型规模增长（仅取决于稀疏化后的 token 数），在 4B 模型上运行时增量不足 10%，且随着模型增大相对成本进一步下降。

**批大小鲁棒性**（Figure 16）：当训练批大小从 256 增加到 2048 时，TROLL 的性能保持稳定，而 Clip 的性能随批大小增大逐渐退化。这进一步说明 TROLL 的严格约束提供了更可靠的优化信号，降低了对批次统计量的敏感度。

### 实验局限性与待验证点

1. **任务范围**：所有实验集中在数学推理与代码生成的 RLVR 设定，尚未在 RLHF（人类偏好对齐）等更广泛的 LLM 后训练场景中验证。
2. **模型规模上限**：最大实验模型为 14B，尚未在数十亿至数百亿参数模型及混合专家（MoE）架构上验证可扩展性。
3. **生成长度**：所有实验基于短响应（最大 256 tokens），对于长文本生成任务的行为尚不明确。
4. **稀疏化近似误差**：在极低概率 token 上引入的微小近似误差（理论上界由 Theorem A.2 保证，比信任区域阈值小约两个数量级）在极严格信任区域下的影响需进一步验证。
5. **自适应 ε 机制**：当前 ε 为固定超参数，探索自适应调节信任区域边界的机制可进一步降低调参成本。

### 补充图表

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/007_Table_2.jpg]]

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/013_Table_2.jpg]]
*Table 2: Model checkpoints used as starting points for finetuning throughout this work*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_X9D5MVpPJ9/figures/014_Table_3.jpg]]
*Table 3: Hyperparameters. We use these parameters for all experiments unless mentioned otherwise*



## 定位与知识库关联

### 1. 核心瓶颈与设计动机

当前大语言模型（LLM）的强化学习（RL）后训练普遍采用 PPO 及其变体，其信任区域约束通过重要性采样比率的启发式剪裁实现：

$$ \mathcal { I } _ { \mathrm { ppo } } ( \theta ) = \mathbb { E } _ { o _ { t } \sim \pi _ { \mathrm { old } } ( o | q ) \mathcal { D } ( q ) } \left[ \frac { 1 } { | o | } \sum _ { t = 1 } ^ { | o | } \operatorname* { m i n } \left( r _ { t } A _ { t } ; \operatorname { c l i p } \left( r _ { t } , 1 - \epsilon _ { \mathrm { ppo } } , 1 + \epsilon _ { \mathrm { ppo } } \right) A _ { t } \right) \right] $$

这种剪裁机制存在三个根本性缺陷：**（1）缺乏严格的数学约束**——剪裁仅在比率超出 $[1-\epsilon, 1+\epsilon]$ 时截断梯度，而非对策略分布施加精确的 KL 散度限制；**（2）更新偏斜**——当优势估计不准或分布偏移较大时，剪裁无法有效防止策略崩溃；**（3）超参数敏感**——$\epsilon_{\text{ppo}}$ 的选择直接影响训练稳定性与最终性能，且对不同任务需独立调参。

TROLL 的因果杠杆在于：**用可微的离散信任区域投影替代 PPO 的剪裁目标，对每个 token 施加精确的 KL 散度约束**。其核心洞察是：通过将策略更新限制在信任区域内，能够稳定优化过程；结合可微投影与基于概率质量的稀疏化方案，使得严格的 token 级 KL 约束能够高效扩展到现代大语言模型的大规模词表（如 Qwen3 的 151,936 维）。

### 2. 方法谱系定位

#### 2.1 与 PPO 系方法的继承与超越

TROLL 直接替代的是 **PPO**（Schulman et al., 2017）的剪裁目标，但其信任区域约束的数学基础可追溯至 TRPO（Schulman et al., 2015）的 KL 散度约束思想。与 PPO 的启发式剪裁不同，TROLL 通过求解凸优化问题实现精确的 token 级 KL 约束：

$$ \pi_{\theta}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t}) = \underset{\hat{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, \boldsymbol{o}_{<t})}{\mathrm{argmin}} \ \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}} \| \tilde{\pi}_{\boldsymbol{\theta}}) \quad \mathrm{s.t.} \ \mathrm{KL}(\hat{\pi}_{\boldsymbol{\theta}} \| \pi_{\mathrm{old}}) \leq \epsilon $$

投影解为当前策略与旧策略对数概率的几何插值：

$$ \pi_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t}) \propto \exp\left( \frac{\eta^{*} \log \pi_{\mathrm{old}}(o_{t} \mid \mathbf{q}, o_{<t}) + \log \tilde{\pi}_{\boldsymbol{\theta}}(o_{t} \mid \mathbf{q}, o_{<t})}{\eta^{*} + 1} \right) $$

其中 $\eta^{*}$ 通过求解一维凸对偶问题得到。TROLL 的完整目标函数为：

$$ \mathcal{T}_{\mathrm{Troll}}(\theta) = \mathbb{E}_{o_{t} \sim \pi_{\mathrm{old}}(o \mid q) \mathcal{D}(q)} \left[ \frac{1}{|o|} \sum_{t=1}^{|o|} \left( \frac{\pi_{\theta}(o_{t} \mid q, o_{<t})}{\pi_{\mathrm{old}}(o_{t} \mid q, o_{<t})} A_{t} \right) - \alpha \, \mathrm{KL}\big( \tilde{\pi}_{\theta}(o_{t} \mid q, o_{<t}) \,\|\, \lfloor \pi_{\theta}(o_{t} \mid q, o_{<t}) \rfloor \big) \right] $$

该目标包含两项：基于投影分布的重要性加权优势项，以及强制当前策略向投影分布靠拢的 KL 回归项（$\alpha$ 固定为 1，通过 stop-gradient 防止梯度回流至投影分布）。

#### 2.2 与其他 RL for LLM 方法的关系

TROLL 作为策略更新机制的替代品，可与多种优势估计方法组合使用。论文验证了其与以下方法的兼容性：

- **GRPO**（Shao et al., 2024）：组相对策略优化，使用样本群组估计优势。TROLL + GRPO 在 Qwen3-8B 上 DAPO-Train 成功率达 0.721（Clip 为 0.667）。
- **Dr.GRPO**（Liu et al., 2025）：修正 GRPO 长度偏置的变体。TROLL 同样带来一致提升。
- **GSPO**（Zheng et al., 2025）：序列级别策略优化，将重要性比率扩展到整个序列。**关键证据**：GSPO + Clip 在训练中发散（成功率为 0.000），而 GSPO + TROLL 稳定收敛至 0.736（Table 1, Qwen3-8B），证明 TROLL 的信任区域约束对于序列级方法至关重要。
- **REINFORCE++**（Hu et al., 2025）：集成全局优势归一化的 REINFORCE 变体。
- **BAPO**（Xi et al., 2025）：自适应调节 PPO 剪裁边界的变体。TROLL 与之正交——BAPO 调节剪裁边界，TROLL 则完全替换剪裁机制。
- **GPG**（Chu et al., 2025）：无剪裁的策略梯度基线（组策略梯度）。

TROLL 相对于这些方法的独特贡献在于：**提供了一种与优势估计方法解耦的、数学严格的可微信任区域投影机制**，可作为任意策略梯度方法的 drop-in 替换。

### 3. 关键技术创新与实现

#### 3.1 可微信任区域投影

TROLL 采用 OptNet 框架（Amos & Kolter, 2017）通过隐式微分保持整个投影步骤的可微性。即使 KL 约束被激活（$\eta^{*} > 0$），梯度仍能通过 KKT 条件反向传播，避免了 PPO 剪裁导致的梯度截断问题（Figure 6 展示了从 LLM 输出到 RL 目标的完整计算图）。

#### 3.2 稀疏化方案

为将投影扩展到现代 LLM 的大规模词表，TROLL 引入基于概率质量的稀疏化：对每个 token 的 logits 进行 top-K 选取，保留累积质量 $\geq 1-\delta$ 的最大概率 token，其余赋予微小默认质量。理论分析（Theorem A.2）给出稀疏化引入的额外 KL 误差上界：

$$ \mathbf{KL}(p \parallel q) \le \gamma^{-1} \mathrm{KL}(p' \parallel q') + \delta \log \frac{\delta}{q_{\min}} $$

在默认超参数（$K=64, \delta=10^{-5}$）下，该误差比信任区域阈值小约两个数量级，实际仅需 5-10 个 token 即可保留 99.999% 的概率质量。

#### 3.3 计算效率

投影开销不随模型尺寸增长，在 4B 模型上运行时增量不足 10%（Figure 5 Top Right, Table 5）。稀疏分布的存储开销相对于 LLM 训练显存可忽略。

### 4. 适用边界与局限

#### 4.1 已验证的适用场景

- **数学推理**：在 DAPO-Math、MATH-Eval、GSM8K 等基准上，TROLL 较 Clip 提升 3-10 个百分点（Figure 3, Table 1）。
- **代码生成**：在 Eurus-Code 上提升 7-18 个百分点，相对增益 18-30%（Figure 1 Right, Figure 3 Bottom）。
- **模型规模**：在 Qwen3 系列（600M 至 14B）和 Qwen2.5-7B-Instruct 上验证有效。
- **短响应生成**：所有实验基于最大 256 tokens 的响应。

#### 4.2 已知局限

1. **任务范围受限**：实验聚焦于 RLVR（可验证奖励的强化学习）场景下的数学推理和代码生成，未验证在 RLHF（人类偏好对齐）等更广泛 LLM 后训练场景中的表现。
2. **模型规模未充分验证**：最大实验模型为 14B，尚未在数十亿至数百亿参数的模型及混合专家（MoE）架构上验证可扩展性。
3. **稀疏化近似风险**：在极低概率 token 上引入的微小近似误差可能在极严格信任区域（$\epsilon$ 极小）下产生未知影响。
4. **长文本生成未知**：对于长文本生成任务（>256 tokens）的行为尚不明确。

### 5. 开放问题

1. **大规模扩展**：将 TROLL 扩展到更大规模模型（>100B）和混合专家（MoE）架构时的投影效率与效果。
2. **多模态适用性**：TROLL 在视觉-语言模型等多模态 LLM 后训练中的适用性。
3. **RLHF 整合**：在 RLHF 等需要与参考策略保持接近的场景中，如何整合 TROLL 的信任区域（当前 TROLL 仅约束与旧策略的 KL 散度）。
4. **自适应信任区域**：探索自适应调节信任区域边界 $\epsilon$ 的机制，以避免手动调参。消融实验（Figure 5 Left）表明较小的 $\epsilon$ 减慢训练但不影响收敛，过大的 $\epsilon$ 导致性能下降，暗示存在最优边界且可能与训练阶段相关。
5. **理论分析深化**：TROLL 的收敛性保证、与自然策略梯度（NPG）的理论联系等尚未充分探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/TROLL_Trust_Regions_Improve_Reinforcement_Learning_for_Large_Language_Models.pdf]]
