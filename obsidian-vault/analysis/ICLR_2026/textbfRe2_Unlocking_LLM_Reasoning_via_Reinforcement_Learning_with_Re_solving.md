---
title: "$\\textbf{Re}^{2}$: Unlocking LLM Reasoning via Reinforcement Learning with Re-solving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcement_Learning_with_Re_solving.pdf
project_link: null
code_link: null
aliases:
- RRLRS
- TR2ULRRLRS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "模型是否具备在推理过程中主动放弃低质量推理路径并重新开始（re-solve）的能力。"
primary_logic: "通过纯强化学习训练模型在推理过程中灵活地选择放弃当前路径并重新求解，可以将原本仅0.5%的重新求解行为提升至30%以上，从而显著提升推理准确率。"
claims:
- "当初始推理步骤次优时，LLM即使生成更多token也难以得到正确答案。"
- "Re²将vanilla模型中仅0.5%的重新求解行为提升至30%以上。"
- "Re²在相同训练预算下，在多个推理基准上显著优于标准RLVR方法DAPO。"
- "CoT长度与准确率呈负相关。"
---

# $\textbf{Re}^{2}$: Unlocking LLM Reasoning via Reinforcement Learning with Re-solving

> [!tip] 核心洞察
> 通过纯强化学习训练模型在推理过程中灵活地选择放弃当前路径并重新求解，可以将原本仅0.5%的重新求解行为提升至30%以上，从而显著提升推理准确率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Re²：通过带重求解的强化学习解锁大语言模型推理能力 |
| 英文题名 | $\textbf{Re}^{2}$: Unlocking LLM Reasoning via Reinforcement Learning with Re-solving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HBOLN5m3qg) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Re² (Reinforcement Learning with Re-solving) |
| Dataset | AIME 2024, AIME 2025, AMC 2023, GSM8K |

> [!tip] 效果简介
> - AIME 2024 上，准确率 为 17.1 (Qwen2.5-7B Base)，对比 11.3 (DAPO)，变化 +5.8。
> - AIME 2025 上，准确率 为 19.0 (Qwen2.5-7B Base)，对比 13.5 (DAPO)，变化 +5.5。
> - AMC 2023 上，准确率 为 70.8 (Qwen2.5-7B Base)，对比 65.0 (DAPO)，变化 +5.8。

## 概要

本文针对现有强化学习（RLVR）训练后的大语言模型在推理时的一个关键瓶颈：**当初始推理方向或质量不佳时，模型即使生成更多token也难以恢复正确路径，导致低效的过度思考（overthinking）和答案质量下降**。核心问题在于模型缺乏在推理过程中主动放弃低质量路径并重新开始（re-solve）的能力。

为解决此问题，论文提出 **Re² (Reinforcement Learning with Re-solving)**，一种纯强化学习方法，无需初步监督微调。其核心洞察是：通过训练模型在推理过程中灵活选择放弃当前路径并重新求解，可以将vanilla模型中仅0.5%的重新求解行为提升至30%以上，从而显著提升推理准确率。方法的核心机制包括：(1) **前缀组生成**：为每个问题采样多个完整响应并随机截断为前缀，模拟中间推理状态；(2) **三路奖励策略**：对正确、错误和重新求解三种延续分别赋予奖励，其中重新求解的奖励被设计为从零开始求解的期望准确率；(3) **组内优势计算与策略更新**：在每个前缀组内对奖励归一化得到优势，并使用裁剪的PPO目标更新策略。

主要实验结果（Table 1）显示，在相同训练预算下，Re²在多个推理基准上显著优于标准RLVR方法DAPO。例如，在Qwen2.5-7B-Base模型上，AIME 2024准确率从11.3提升至17.1（+5.8），AIME 2025从13.5提升至19.0（+5.5），AMC 2023从65.0提升至70.8（+5.8）。实验覆盖从3B到14B参数的5种模型，结果具有良好泛化性。此外，分析表明CoT长度与准确率呈负相关（Figure 3），且对于大多数错误回答，仅使用前20%的响应作为前缀时准确率就已显著下降（Figure 4），这进一步验证了早期推理路径质量对最终结果的决定性影响。

当前基于强化学习（RLVR）训练的大语言模型在数学推理任务中面临一个关键瓶颈：当模型在推理的初始步骤选择了次优方向时，即使后续生成更多的推理token，也难以自行纠正并抵达正确答案。这种“一步错，步步错”的困境导致模型产生大量低效的“过度思考”（overthinking）行为——CoT链越长，准确率反而越低。论文通过Figure 3和Figure 4的实证分析揭示了这一现象：CoT长度与推理性能呈清晰的负相关，且对于大多数错误回答，仅使用其前20%的响应作为继续推理的前缀时，准确率就已出现显著下降。这表明问题的根源不在于模型缺乏生成更多推理步骤的能力，而在于其缺乏在推理过程中主动识别并放弃低质量路径的机制。

现有RLVR方法（如DAPO、GRPO）的推理路径管理策略存在根本性缺口：它们强制模型沿着单一CoT轨迹持续生成直至给出最终答案，无法在推理中途选择放弃并重新开始。这种设计假设初始推理方向总是足够好，或模型能够通过增加步数来自我修正，但上述实证证据表明这两种假设在复杂推理任务中均不成立。测试时扩展方法（如DLER、DeepConf）虽然试图通过采样多条轨迹来缓解这一问题，但并未在训练层面赋予模型主动放弃路径的能力。

针对这一缺口，本文提出Re²（Reinforcement Learning with Re-solving），其核心动机是：通过纯强化学习训练模型在推理过程中灵活地选择放弃当前路径并重新求解（re-solve），从而将标准RLVR模型中仅约0.5%的罕见重求解行为提升至30%以上。该方法无需任何初步的监督微调，直接通过奖励函数设计来引导模型学习何时应该放弃——对正确/错误/重求解三种延续分别赋予不同奖励，其中重求解的奖励被设计为从零开始重新求解的期望准确率。这一设计的关键洞察在于：让模型意识到在某些情况下，放弃当前路径重新开始比继续在错误方向上投入更多token更有可能获得正确答案。

## 核心方法与创新机理

**瓶颈诊断：从“过度思考”到“路径锁定”**

现有RLVR训练后的LLM在推理时面临一个关键瓶颈：当初始推理方向或质量不佳时，即使生成更多token也难以恢复正确路径（Figure 2(a)）。这导致了一种低效的“过度思考”（overthinking）现象——CoT长度与准确率呈负相关（Figure 3），模型在错误的路径上浪费计算资源。更具体地，对错误回答的分析显示，仅使用前20%的响应作为前缀时，准确率就已出现显著下降（Figure 4），说明错误往往在推理早期就已固化。

**因果旋钮：主动放弃与重求解能力**

核心因果变量是模型是否具备在推理过程中主动识别低质量路径并放弃当前路径、重新开始（re-solve）的能力。在vanilla模型中，这种重求解行为极其罕见（仅约0.5%）。Re²的核心洞察是：通过纯强化学习训练模型灵活地选择放弃当前路径并重新求解，可以将这一行为提升至30%以上，从而打破路径锁定，显著提升推理准确率。

**关键变更点（Changed Slots）**

Re²相对于标准RLVR方法（以DAPO为代表）有三个核心变更：

1.  **推理路径管理策略**：从单一的CoT轨迹生成（无法主动放弃低质量路径）转变为允许模型在推理过程中灵活选择放弃当前路径并重新求解。这一变更直接针对上述瓶颈，使模型具备“试错-重启”能力。

2.  **奖励函数设计**：从简单的二元奖励（正确=1，错误=0）扩展为三路奖励策略。对于选择重求解（re-solve）的延续，其奖励被设定为从零开始重新求解的期望准确率（Eq. 1）。该期望值使用组外（out-of-group）的CoT完成结果进行估计，并考虑了最多R轮重试。这一设计的关键在于为“放弃”行为提供了有信息量的、非零的奖励信号，使得模型能够学习到何时放弃是有利的。

3.  **训练数据生成方式**：从为每个问题采样完整推理轨迹，转变为先采样完整响应并随机截断为前缀（截断比例均匀采样自[0, 0.8]），再为每个前缀生成多个延续。这种“前缀组生成”策略（Section 4.1）创建了丰富的中间推理状态，使得模型能够在各种推理阶段学习重求解决策，而非仅在最终答案处学习。

**机制与证据强度**

Re²的完整流程（Figure 5）包括：前缀组生成 → 三路奖励分配 → 组内优势计算与策略更新。其中，组内优势归一化（Eq. 2）和裁剪的PPO目标（Eq. 3）是标准的RLVR技术，创新在于将其应用于前缀组这一新结构。

决定性证据表明该机制有效：
- 在Qwen2.5-7B-Base上，Re²在AIME 2024上达到17.1（DAPO为11.3），在AIME 2025上达到19.0（DAPO为13.5），在AMC 2023上达到70.8（DAPO为65.0）（Table 1）。
- 在5种模型（3B-14B参数，含预训练、指令微调和推理模型）上，Re²均一致优于DAPO（p-value < 0.05）。
- 在测试时扩展方面，当样本数超过64时，Re²持续超越性能已饱和的RLVR模型（Figure 6）。
- 按难度分组分析显示，在RLVR偶尔能解决的问题上（Group 4），Re²将准确率从51.2%提升至81.7%（Figure 8(b)）。

**失败模式与开放性**

论文坦诚指出了Re²的局限：缺乏显式机制控制推理过程中重求解动作的调用概率；模型可能需要多轮重求解才能得到正确答案，增加了推理时的token消耗（约11%的rollout时间增加）。此外，Re²在非数学推理任务、视觉/多模态推理任务以及工具使用/搜索密集型任务上的表现尚未探索。这些开放性问题的存在意味着该方法的泛化边界尚需验证。

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/009_Figure_5.jpg]]
*Figure 5: The framework of $\mathrm { R e ^ { 2 } }$ . For each query, $\mathrm { R e ^ { 2 } }$ samples multiple prefixes, then generates multiple continuations for each prefix. The advantage is calculated within each group, while the out-of-group accuracy is used as the reward for the redo action

Re² 的整体框架建立在“前缀组生成 → 三路奖励分配 → 组内优势计算与策略更新”这一核心 pipeline 上，其设计动机源于一个关键瓶颈：标准 RLVR 训练后的 LLM 在推理时，一旦初始推理方向不佳，即使生成更多 token 也难以恢复正确路径，导致低效的过度思考（overthinking）和准确率下降。Figure 2(a) 和 Figure 3 分别展示了这一现象：当初始步骤次优时，模型挣扎于错误路径；且 CoT 长度与准确率呈负相关。核心因果旋钮在于模型是否具备在推理过程中主动放弃低质量路径并重新开始（re-solve）的能力。

**模块关系与输入输出流如下：**

1. **前缀组生成（Prefix Group Generation）**：对于每个查询 $q$，模型 $\pi_{\theta_{\text{old}}}$ 首先生成 $n$ 个完整响应。每个响应被随机截断（截断比例从 [0, 0.8] 均匀采样），产生 $n$ 个多样化的前缀 $\text{Pre}_i$，作为中间推理状态。然后，对于每个前缀，模型生成 $m$ 个 CoT 延续 $\mathcal{O}_{i,j}$。这些延续包含三种可能的输出类型：给出正确最终答案、给出错误最终答案、或选择重求解（re-solve）。该模块的输出是 $n$ 个前缀组，每组包含 $m$ 个延续。此设计的关键在于：Figure 4 显示，对于大多数错误回答，仅使用前 20% 的响应作为前缀时，准确率就已显著下降，因此截断前缀能有效模拟模型在早期就需要放弃的推理状态。

2. **三路奖励策略（Three-way Reward Strategy）**：对每个延续 $C_{i,j}$ 分配奖励 $r_{i,j}$。正确的延续获得奖励 1，错误的获得 0。对于选择重求解的延续，其奖励被设定为从零开始重新求解的期望准确率，该值通过组外（out-of-group）的 CoT 完成序列估计得到。具体公式为：
   
$$
r_{i,j} = \begin{cases} 
   1, & \text{if } C_{i,j} = \text{correct} \\
   0, & \text{if } C_{i,j} = \text{incorrect} \\
   P_{\neq i}(\text{correct}) \cdot \frac{1 - P_{\neq i}(\text{resolve})^R}{1 - P_{\neq i}(\text{resolve})}, & \text{if } C_{i,j} = \text{resolve}
   \end{cases}
$$

   其中 $R$ 是允许的最大重试轮数。这个奖励设计的核心洞见是：它不将重求解视为“失败”，而是赋予其一个介于 0 和 1 之间的、有意义的期望奖励值，从而在策略梯度中为正的重求解行为提供学习信号。

3. **组内优势计算与策略更新（Group-wise Advantage & Policy Update）**：在每个前缀组 $\{\mathcal{O}_{i,j}\}_{j=1}^m$ 内，对 $m$ 个延续的奖励进行归一化，得到优势 $\hat{A}_{i,j}$：
   
$$
\hat{A}_{i,j} = \frac{r_{i,j} - \text{mean}(\{r_{i,j}\}_{j=1}^m)}{\text{std}(\{r_{i,j}\}_{j=1}^m)}
$$

   然后使用裁剪的 PPO 目标更新策略参数 $\theta$。优化目标 $\mathcal{J}_{\text{Re}^2}(\theta)$ 在公式 (3) 中给出，它整合了所有前缀和延续上的裁剪重要性采样比率与组内优势。该模块的输出是更新后的策略 $\pi_\theta$。

**与基线方法的关键差异**：与标准 RLVR 方法（如 DAPO）相比，Re² 改变了三个核心插槽：(1) **推理路径管理策略**从“生成单一 CoT 轨迹并最终给出答案”变为“模型可以灵活选择放弃当前路径并重新求解”；(2) **奖励函数**从简单的 1/0 二元奖励变为包含第三种选择（重求解）的三路奖励，且重求解的奖励被设计为期望准确率；(3) **训练数据生成方式**从为每个问题采样多个完整轨迹，变为先采样完整响应并随机截断为前缀，再为每个前缀生成多个延续。

**证据强度**：该 pipeline 的每个模块都有明确的证据支持。Figure 5 直观展示了框架的流程。Table 1 的实验结果验证了整体有效性：在 Qwen2.5-7B Base 上，Re² 在 AIME 2024 上达到 17.1（DAPO 为 11.3，+5.8），在 AIME 2025 上达到 19.0（DAPO 为 13.5，+5.5），在 AMC 2023 上达到 70.8（DAPO 为 65.0，+5.8）。更重要的是，Figure 1(a) 显示在相同的训练预算下（每步生成的 token 数相当），Re² 的准确率提升持续优于 DAPO。Figure 1(b) 和 Figure 6 进一步表明，Re² 在测试时扩展方面也优于多数投票和 RLVR 模型，当样本数超过 64 时优势明显。

**需要人工验证的点**：奖励函数中重求解的期望准确率估计依赖于组外 CoT 完成序列，其偏差和方差在 Figure 11 中进行了分析，表明随着 $n$ 或 $m$ 增大，估计器优于 EMA 基线。然而，最优的 $R$ 值（最大重试轮数）如何针对不同问题类型自适应调整，以及前缀截断比例分布对性能的具体影响，论文中未提供系统性的消融实验，这些点的最优设置需要进一步验证。

Re² 的核心创新在于通过强化学习训练 LLM 在推理过程中主动放弃低质量路径并重新求解（re-solve），从而解决标准 RLVR 模型在初始推理方向不佳时难以恢复正确路径的问题。其方法由三个紧密耦合的模块组成：前缀组生成、三路奖励策略和组内优势更新。

### 1. 前缀组生成（Prefix Group Generation）

该模块为每个问题构造多样化的中间推理状态。具体流程为：对每个查询 `q`，首先采样 `n` 个完整响应 `{Response_i}`，每个响应在 `[0, 0.8]` 区间内均匀随机选择一个截断比例进行截断，得到 `n` 个不同的前缀 `{Pre_i}`。随后，对于每个前缀 `Pre_i`，模型生成 `m` 个延续（continuation）`{O_{i,j}}`。每个延续有三种可能的输出：给出正确答案、给出错误答案、或选择重新求解（re-solve）。这一设计的瓶颈在于：截断比例分布的选择直接影响前缀的难度分布，进而影响训练信号的丰富度；论文未深入探讨不同分布对性能的影响，这是一个需要手动验证的开放问题。

### 2. 三路奖励策略（Three-way Reward Strategy）

这是 Re² 的核心因果旋钮。与标准 RLVR 仅对正确/错误答案给予二元奖励不同，Re² 为三种延续分别赋予奖励。对于第 `i` 个前缀的第 `j` 个延续 `C_{i,j}`，奖励函数定义为：

$$r_{i,j} = \begin{cases} 1, & \text{if } C_{i,j} = \text{correct} \\ 0, & \text{if } C_{i,j} = \text{incorrect} \\ P_{\neq i}(\text{correct}) \cdot \frac{1 - P_{\neq i}(\text{resolve})^R}{1 - P_{\neq i}(\text{resolve})}, & \text{if } C_{i,j} = \text{resolve} \end{cases}$$

其中，`P_{\neq i}(correct)` 和 `P_{\neq i}(resolve)` 分别是从零开始求解时正确的概率和选择重新求解的概率，两者均使用**组外**（out-of-group）的 CoT 完成序列进行估计。`R` 是允许的最大重试轮数。重新求解的奖励公式推导自：选择重新求解的期望奖励等于在前 `R` 轮内首次非重试结果为正确的概率。该公式的因果机制在于：它使得模型在评估是否放弃当前路径时，能够理性地比较“继续当前路径”与“重新开始”的期望收益，从而学习到何时应该放弃。奖励估计器的准确性依赖于 `n` 和 `m` 的大小——实验表明（Figure 11），随着 `n` 或 `m` 增大，估计的偏差和方差均低于 EMA 基线，但计算成本也随之线性增加。

### 3. 组内优势计算与策略更新（Group-wise Advantage & Policy Update）

在每个前缀组内部，对 `m` 个延续的奖励进行归一化得到优势：

$$\hat{A}_{i,j} = \frac{r_{i,j} - \text{mean}(\{r_{i,j}\}_{j=1}^m)}{\text{std}(\{r_{i,j}\}_{j=1}^m)}$$

组内归一化的关键作用是消除不同前缀难度差异带来的奖励尺度偏移，使模型专注于学习“在当前前缀下，哪种延续更优”的相对比较。最终，Re² 的优化目标为：

$$\mathcal{J}_{\text{Re}^2}(\theta) = \mathbb{E}_{[q \sim \mathcal{D}, \{\text{Pre}_i\}_{i=1}^n \sim \pi_{\theta_{\text{old}}}(\cdot|q), \{\mathcal{O}_{i,j}\}_{j=1}^m \sim \pi_{\theta_{\text{old}}}(\cdot|q, \text{Pre}_i)]} \left[ \frac{1}{nm} \sum_{i=1}^n \sum_{j=1}^m \frac{1}{|O_{i,j}|} \sum_{t=1}^{|O_{i,j}|} \min\left( \frac{\pi_\theta^{i,j,t}}{\pi_{\theta_{\text{old}}}^{i,j,t}} \hat{A}_{i,j}, \ \text{clip}\left( \frac{\pi_\theta^{i,j,t}}{\pi_{\theta_{\text{old}}}^{i,j,t}}, 1-\varepsilon_{\text{low}}, 1+\varepsilon_{\text{high}} \right) \hat{A}_{i,j} \right) \right]$$

该目标使用裁剪的重要性采样比率和组内优势，是标准的 PPO 风格策略梯度。关键变量含义：`π_θ` 和 `π_{θ_old}` 分别为当前和旧策略；`|O_{i,j}|` 为延续的 token 数；`ε_low` 和 `ε_high` 为裁剪边界（论文中设为 0.2 和 0.28）。该公式本身不引入新机制，其瓶颈在于：组内优势计算假设同一前缀下的 `m` 个延续是条件独立的，但实际中模型可能因自回归生成而产生序列依赖，这一假设的违反程度尚待量化。

## 实验与关键发现

### 主要结果：Re² 显著优于标准 RLVR 基线

Re² 的核心实验在五个数学与科学推理基准（AIME 2024、AIME 2025、AMC 2023、GSM8K、GPQA-Diamond）上进行，以标准 RLVR 方法 DAPO 为主要基线。实验覆盖了从 3B 到 14B 参数的 5 种不同模型（包括预训练、指令微调和蒸馏推理模型），以确保结果的泛化性。如 Table 1 所示，在相同训练预算下，Re² 在所有基准和所有模型上均一致地优于 DAPO（p-value < 0.05）。以 Qwen2.5-7B-Base 为例，Re² 在 AIME 2024 上达到 17.1，比 DAPO 的 11.3 高出 5.8 分；在 AIME 2025（一个未被污染的新基准）上达到 19.0，比 DAPO 的 13.5 高出 5.5 分。在较简单的 GSM8K 上，提升幅度较小（+1.8），因为基线性能已接近饱和（91.8%）。这些结果在 Table 2 中通过 95% 置信区间得到了确认，例如 Qwen2.5-7B-Base 在 AIME 2024 上的区间为 17.1 ± 1.4。

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/010_Table_1.jpg]]
*Table 1: Experimental results on five reasoning benchmarks. $\mathrm { R e ^ { 2 } }$ consistently improves the overall reasoning performance of each model over DAPO (p-value \< 0 . 0 5 ) . Red numbers in parentheses indicate performance gains relative to DAPO*

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/021_Table_2.jpg]]
*Table 2: Accuracy with 95% confidence intervals on five reasoning benchmarks, confidence intervals are given in parentheses*

### 核心机制验证：从“过度思考”到“主动重求解”

论文通过一系列分析实验揭示了 Re² 成功的因果机制。

**瓶颈诊断：** Figure 2(a) 和 Figure 3 共同指出了标准 LLM 推理的核心瓶颈。Figure 3 展示了 CoT 长度与准确率之间存在**清晰的负相关**：生成更长推理轨迹的样本，其平均准确率反而更低。这表明模型存在“过度思考”现象——当初始推理方向错误时，生成更多 token 并不能挽救答案，反而浪费了计算资源。Figure 4 进一步量化了这一现象：对于大多数错误回答，当仅使用其前 20% 的响应作为前缀来继续推理时，准确率就已发生显著下降。这意味着错误往往在推理的早期阶段就已注定。

**因果旋钮：** Re² 的解决方案是训练模型在推理过程中主动放弃低质量路径并重新开始。Figure 1(a) 展示了训练动态：Re² 的准确率提升曲线在训练早期就显著优于 DAPO，且持续保持优势。更关键的是，Re² 将 vanilla 模型中仅 0.5% 的重新求解行为提升至 30% 以上。Figure 8 按问题难度分组分析了这一行为的影响。当根据基础模型估计的难度对问题进行分组时（Figure 8(a)），Re² 在“困难但可解”的问题组（Group 2）上准确率是 DAPO 的两倍以上。当根据 DAPO 训练后的性能对问题进行分组时（Figure 8(b)），最大的提升出现在“RLVR 偶尔能解决”的问题组（Group 4），准确率从 51.2% 跃升至 81.7%。这直接证明了重求解能力是解锁 RLVR 瓶颈的关键。

### 测试时扩展与效率分析

Figure 1(b) 和 Figure 6 展示了 Re² 在测试时扩展方面的优势。随着推理样本数增加，Re² 的准确率持续提升，而 DAPO 的性能在样本数超过 64 后趋于饱和。Re² 在样本数超过 64 后持续超越所有对比的 RLVR 模型，并继续随测试时计算量增加而改善。与额外的测试时扩展基线（GRPO, DLER, DeepConf）相比，Re² 在 AIME 2025 上同样表现出最优的 token 消耗与准确率权衡（Figure 10）。

在训练效率方面，Re² 每步的 rollout 时间比 DAPO 增加约 11%（431 秒 vs 388 秒），这主要来自前缀生成阶段（89 秒）。但考虑到其显著的性能提升，这一额外开销是合理的。Figure 13 显示，Re² 在训练过程中 CoT 长度趋于稳定，而 DAPO 的 CoT 长度持续增长。这表明 Re² 通过鼓励重求解，有效抑制了无效的“过度思考”行为，使模型学会了更高效地分配推理 token。Figure 14 进一步证明，即使在相同的训练时间下，Re² 的准确率提升也始终优于 DAPO。

### 消融与鲁棒性分析

**奖励估计器：** Re² 的奖励函数依赖于对重求解期望准确率的估计。Figure 11 表明，随着前缀数 n 或每个前缀的延续数 m 的增大，Re² 的估计器偏差和方差均低于简单的 EMA 基线，证明了其估计方法的鲁棒性。

**退化组分析：** Figure 12 展示了训练过程中“退化组”（即所有延续都得到相同奖励的组）的比例。Re² 的退化组比例显著低于 DAPO，说明重求解机制有效增加了训练信号的多样性，避免了策略陷入局部最优。

**跨模型泛化：** 除 Qwen 系列外，Re² 在 Llama3.2-3B-Instruct 和 DeepSeek-R1-Distill-Llama-8B 上也取得了显著提升，例如在 AIME 2024 上分别提升 +2.7 和 +4.4。Table 3 进一步展示了 Re² 在 OpenPangu-Embedded-1B 上的应用，在 AIME 2025 上达到 8.6，显著优于原始模型，验证了该方法对更小、非主流模型的有效性。

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/032_Table_3.jpg]]
*Table 3: The accuracy of OpenPangu-Embedded-1B and $\mathrm { R e ^ { 2 } }$ on four benchmarks*

### 失败模式与局限性

尽管 Re² 效果显著，但分析也揭示了其局限性。
1.  **推理时 token 消耗增加：** 如 Section 5.4 所述，模型可能需要多轮重求解才能得到正确答案，这增加了推理时的 token 消耗。虽然这换来了更高的准确率，但在计算资源严格受限的场景下需权衡。
2.  **缺乏显式控制：** 论文在 Limitations 中明确指出，推理过程中没有显式机制来控制调用重求解动作的概率。模型学习到的重求解策略是隐式的，可能不是最优的。
3.  **任务范围有限：** 实验主要集中在数学推理任务上。Re² 在非数学推理（如常识推理、开放域问答）、视觉或多模态推理，以及工具使用或搜索密集型任务上的表现尚未探索，其泛化能力需要进一步验证。

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/031_Figure_20.jpg]]
*Figure 20: $\mathrm { R e ^ { 2 } }$ Examples 2*

![[assets/figures/papers/iclr26_0001_HBOLN5m3qg_textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcem/figures/033_Figure_22.jpg]]
*Figure 22: $\mathrm { R e ^ { 2 } }$ Examples 4*

## 定位与知识库关联

Re² 的核心贡献在于将 **推理路径的主动放弃与重启** 引入到纯强化学习（RL）训练框架中，从而解决了现有 RLVR（Reinforcement Learning with Verifiable Rewards）方法的一个根本性瓶颈：当模型初始推理方向错误时，即使生成更多 token 也无法恢复正确路径，反而导致低效的过度思考（overthinking）。该问题在 Figure 2(a) 和 Figure 3 中得到明确验证——CoT 长度与准确率呈负相关，且从错误响应的前 20% 前缀继续推理时准确率已显著下降（Figure 4）。

**与基线的谱系关系：** Re² 直接继承并改进了标准 RLVR 基线 DAPO 和 GRPO。与这些基线相比，Re² 改变了三个关键设计槽位：
1. **推理路径管理策略**：基线强制模型生成单一 CoT 轨迹并最终给出答案，无法主动放弃低质量路径；Re² 允许模型在推理过程中灵活选择重新求解（re-solve）。
2. **奖励函数设计**：基线仅对正确/错误最终答案给予二元奖励（1/0）；Re² 引入第三种选择（resolve），其奖励为从零开始重新求解的期望准确率，通过组外（out-of-group）CoT 完成来估计（Eq. 1）。
3. **训练数据生成方式**：基线为每个问题采样多个完整推理轨迹；Re² 先采样完整响应并随机截断为前缀（截断比例均匀取自 [0, 0.8]），再为每个前缀生成多个延续，形成前缀组（Prefix Group Generation）。

**适用边界：** Re² 在数学推理基准（AIME 2024/2025、AMC 2023、GSM8K、GPQA-Diamond）上，对 3B 到 14B 参数的 5 种模型（包括预训练、指令微调和推理模型）均一致优于 DAPO（p-value < 0.05）。在测试时扩展（test-time scaling）方面，当样本数超过 64 时，Re² 持续超越 RLVR 模型（其性能已饱和）和多数投票（majority voting）基线（Figure 6）。按问题难度分组分析显示，Re² 在“困难但可解”的问题上准确率是 DAPO 的两倍以上（Figure 8(a)），在“RLVR 偶尔能解决”的问题上准确率从 51.2% 提升至 81.7%（Figure 8(b)）。

**局限与开放问题：**
1. **控制机制缺失**：推理过程中没有显式机制来控制调用重求解动作的概率，模型可能仍需要多轮重求解才能得到正确答案，增加了推理时的 token 消耗（Re² 每步 rollout 时间比 DAPO 增加约 11%）。
2. **任务泛化性未验证**：Re² 在非数学推理任务（如常识推理、开放域问答）、视觉或多模态推理任务、以及工具使用或搜索密集型任务上的表现尚未探索。
3. **超参数敏感性**：最优的重求解轮数 R 如何针对不同问题类型进行自适应调整？前缀截断比例分布对性能有何影响？这些问题均未在论文中系统探讨。
4. **训练效率**：论文未报告计算资源消耗的详细对比（如 GPU 小时数），仅报告了每步 rollout 时间，因此 Re² 在总训练成本上的竞争力需要进一步验证。

总体而言，Re² 在 RLVR 方法谱系中开辟了一条“允许推理路径主动放弃与重启”的新分支，其核心洞察——将重求解行为从基线模型的 0.5% 提升至 30% 以上——展示了 RL 框架在塑造模型推理策略方面的巨大潜力。然而，该方法目前仍局限于数学推理领域，且缺乏对重求解行为的精细控制，这构成了其向更广泛推理任务迁移的主要障碍。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcement_Learning_with_Re_solving.pdf

![[paperPDFs/ICLR_2026/textbfRe2_Unlocking_LLM_Reasoning_via_Reinforcement_Learning_with_Re_solving.pdf]]
