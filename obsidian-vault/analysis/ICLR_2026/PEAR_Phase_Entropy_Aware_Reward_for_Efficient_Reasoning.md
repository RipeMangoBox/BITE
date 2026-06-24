---
title: "PEAR: Phase Entropy Aware Reward for Efficient Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PEAR_Phase_Entropy_Aware_Reward_for_Efficient_Reasoning.pdf
openreview_forum_id: HLc2igXEA3
aliases:
- PPEAR
- PEAR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "模型在不同推理阶段（思考阶段和最终回答阶段）的令牌级熵（token-level entropy）可作为控制响应长度与准确性的关键调节变量；思考阶段的高熵对应探索性行为，而最终回答阶段的低熵对应确定性表达。"
primary_logic: "在奖励设计中引入阶段性熵感知惩罚，通过降低思考阶段的过度熵来抑制冗余探索，同时保留回答阶段的适度熵以维持灵活性，从而在不牺牲准确性的前提下显著缩短推理轨迹。"
claims:
- "模型熵与响应长度在不同模型和基准上呈一致正相关（图2(a)）。"
- "思考阶段的熵显著高于最终回答阶段（图2(b)）。"
- "熵过滤实验表明，去除高达40%的高熵令牌不会损害准确性，证明冗余集中于思考阶段（图3）。"
- "PEAR在三个模型尺度上实现32.4%-56.6%的响应长度压缩，准确度下降小于1%（表1）。"
---

# PEAR: Phase Entropy Aware Reward for Efficient Reasoning

> [!tip] 核心洞察
> 在奖励设计中引入阶段性熵感知惩罚，通过降低思考阶段的过度熵来抑制冗余探索，同时保留回答阶段的适度熵以维持灵活性，从而在不牺牲准确性的前提下显著缩短推理轨迹。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PEAR：基于阶段熵感知奖励的高效推理方法 |
| 英文题名 | PEAR: Phase Entropy Aware Reward for Efficient Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HLc2igXEA3); [GitHub](https://github.com/iNLP-Lab/PEAR) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | PEAR (Phase Entropy Aware Reward) |
| Dataset | Average (6 benchmarks), Average (5 benchmarks) |

> [!tip] 效果简介
> - Average (6 benchmarks) 上，Accuracy / Generated Tokens 为 74.27% / 3221，对比 74.85% / 7428，变化 Acc: -0.58%; Tok: -56.6%。
> - Average (6 benchmarks) 上，Accuracy / Generated Tokens 为 77.56% / 3200，对比 77.48% / 6845，变化 Acc: +0.08%; Tok: -53.3%。
> - Average (5 benchmarks) 上，Accuracy / Generated Tokens 为 81.95% / 3708，对比 81.15% / 5364，变化 Acc: +0.80%; Tok: -30.87%。

## 概述

大型推理模型（LRMs）在生成思维链时倾向于产生冗长的推理轨迹，包含大量冗余步骤，导致推理效率低下且计算成本高昂。PEAR（Phase Entropy Aware Reward）针对这一瓶颈，提出了一种基于阶段熵感知的奖励机制，核心洞察在于：模型在不同推理阶段（思考阶段与最终回答阶段）的令牌级熵可作为控制响应长度的关键调节变量——思考阶段的高熵对应探索性行为，而回答阶段的低熵对应确定性表达。

PEAR 通过惩罚思考阶段的过度熵来抑制冗余探索，同时保留回答阶段的适度熵以维持灵活性，从而在不牺牲准确性的前提下显著缩短推理轨迹。该方法无需依赖精心策划的数据集或显式长度约束，仅通过修改奖励信号即可实现高效推理。

主要实验结果：在 Qwen3-4B 上，PEAR 实现 56.6% 的响应长度压缩，准确率仅下降 0.58%；在 Qwen3-8B 上，长度压缩 53.3% 的同时准确率提升 0.08%；在 Qwen3-14B 上，长度压缩 30.87%，准确率提升 0.80%。熵过滤实验进一步证实，去除高达 40% 的高熵令牌不会损害准确性，证明冗余主要集中在思考阶段。

PEAR 建立在 GRPO（Group Relative Policy Optimization）框架之上，与 Step Entropy、LCPO 等现有方法相比，其独特之处在于将熵分解为思考与回答两个阶段，并据此设计差异化的惩罚策略，而非简单地限制总长度或插入终止标记。

## 背景与动机

大型推理模型（LRMs）通过在输出最终答案前生成显式的思维链（Chain-of-Thought, CoT）推理过程，在数学、编程等复杂推理任务上展现了强大的能力。然而，这一能力伴随着显著的计算开销：模型倾向于产生过长的响应，其中包含大量冗余的推理步骤，这些步骤并未实质性提升答案的准确性，却消耗了可观的推理预算。在追求模型性能的同时，如何提升推理效率、抑制冗余生成，已成为LRMs走向实际部署的核心瓶颈。

现有的效率优化方法主要分为两类。一类是基于长度约束的策略优化，如**LCPO**（Aggarwal & Welleck, 2025），通过在奖励函数中显式加入长度惩罚来联合优化准确性与响应长度。另一类通过特殊令牌或阶段设计来压缩推理过程，如**Step Entropy**（Li et al., 2025）采用两阶段训练，插入[SKIP]令牌来缩短思维链。这些方法虽然有效，但通常依赖于精心设计的长度约束、额外的训练阶段或特定的数据构造，缺乏对模型内部生成行为的自适应调控。

本文从一个新的视角切入：**模型在推理过程中的令牌级熵（token-level entropy）**。熵衡量了模型在每个生成位置上的预测不确定性——高熵意味着模型在多个候选令牌间犹豫，对应探索性行为；低熵则表明模型对当前输出高度确定，对应确定性表达。这一信号天然存在于模型的生成分布中，无需额外的标注或约束即可获取。

初步分析揭示了两个关键观察。首先，**平均熵与响应长度呈一致的正相关关系**（Figure 2(a)）：在不同模型系列和尺度上，熵越高的模型或样本，其生成的推理轨迹越长。其次，**推理过程中的熵分布具有显著的阶段性特征**（Figure 2(b)）：位于`<think>`与`</think>`标签之间的思考阶段，其平均熵远高于最终回答阶段。这表明，思考阶段的冗余探索是导致响应膨胀的主要来源。

进一步的熵过滤实验为这一假设提供了因果证据。通过按令牌级熵从低到高排序，逐步移除高熵令牌后评估模型性能，实验发现：在Qwen3-4B上，保留60%的低熵令牌时，准确率保持稳定甚至略有提升，同时响应长度大幅缩短；只有当过滤比例超过40%（即移除过多低熵令牌）时，准确率才出现骤降（Figure 3）。在Qwen3-8B上的验证实验（Figure 6）也呈现一致趋势。这意味着，**高熵令牌主要承载冗余探索而非核心推理逻辑**，对其进行抑制不会损害答案质量。

基于上述发现，本文的核心动机是：**能否利用推理过程的阶段性熵特征，在强化学习训练中自适应地压缩冗余推理，而无需依赖显式的长度约束或数据构造？** 这一思路将效率优化的控制变量从“响应长度”转移至“生成熵”，使模型学会在思考阶段收敛不确定性、在回答阶段保持适度灵活性，从而在准确性与效率之间取得更优的平衡。

## 核心创新

### 问题洞察：推理效率瓶颈的熵视角

大型推理模型（LRMs）在生成思维链时普遍存在响应过长的问题，其根源在于思考阶段产生了大量冗余的探索性推理步骤。PEAR 从信息论角度重新审视了这一瓶颈：模型在不同推理阶段的令牌级熵（token-level entropy）表现出显著差异——思考阶段的高熵对应探索性行为，而最终回答阶段的低熵对应确定性表达。实验证据表明，平均熵与响应长度在不同模型和基准上呈一致正相关（Figure 2(a)），且思考阶段的熵显著高于最终回答阶段（Figure 2(b)）。进一步的熵过滤实验揭示了一个关键发现：去除高达 40% 的高熵令牌不会损害准确性，证明冗余集中于思考阶段（Figure 3）。

### 核心机制：阶段性熵感知奖励

基于上述洞察，PEAR 的核心创新在于**将阶段性熵惩罚直接嵌入奖励函数**，通过调节思考阶段与回答阶段的熵平衡来实现推理轨迹的自适应压缩。与现有方法相比，PEAR 的关键差异体现在以下 changed slot：

| 组件 | 基线方法（GRPO） | PEAR 改进 |
|------|-----------------|----------|
| **奖励函数** | 规则化二元奖励：正确回答为 1，错误为 0 | 阶段性熵惩罚奖励：正确回答的奖励为 $\min(1, s - \mathcal{P}(y))$，其中 $\mathcal{P}(y) = \max(0, \bar{H}_{\text{think}} - \alpha \bar{H}_{\text{answer}})$，错误回答保持格式奖励 $r_{\text{fmt}}$ |

该设计的因果机制如下：

1. **相位分解**：将响应划分为 `<think>` 至 `</think>` 的思考阶段和其后的最终回答阶段，分别计算平均熵 $\bar{H}_{\text{think}}$ 和 $\bar{H}_{\text{answer}}$（式 6）。

2. **熵差惩罚**：通过惩罚项 $\mathcal{P}(y) = \max(0, \bar{H}_{\text{think}} - \alpha \bar{H}_{\text{answer}})$ 构建奖励信号。当思考阶段熵过高而回答阶段熵相对较低时，惩罚增大，从而抑制冗余探索；参数 $\alpha$ 调节回答阶段熵的贡献权重，$\alpha=1$ 为默认设置。

3. **奖励整合**：正确回答的最终奖励为 $\min(1, s - \mathcal{P}(y))$，其中 $s$ 为正确基准分。该设计确保模型在追求正确答案的同时，主动压缩思考阶段的冗余推理。

### 与现有方法的本质区别

- **对比 Step Entropy**（Li et al., 2025）：Step Entropy 采用两阶段训练并通过插入 `[SKIP]` 令牌缩短推理，依赖显式的长度控制信号。PEAR 则通过奖励塑形在单一训练阶段中隐式引导模型自主学习高效推理，无需特殊令牌或数据集干预。

- **对比 LCPO**（Aggarwal & Welleck, 2025）：LCPO 通过联合优化准确性和显式长度约束来控制响应长度。PEAR 不依赖任何显式长度目标或截断规则，而是利用模型自身的熵信号作为自适应调节器。

- **对比原始 GRPO**：PEAR 仅修改了奖励函数中的标量奖励计算，策略更新保持与 GRPO 相同的裁剪代理目标与 KL 散度正则化（式 2-3），因此可无缝集成到现有 GRPO 训练框架中。

### 效率-准确性权衡的控制机制

超参数 $\alpha$ 是 PEAR 实现效率-准确性权衡的关键控制变量。研究表明（Figure 5）：$\alpha=0$（仅惩罚思考熵）会损害准确率；$\alpha=-1$（同时惩罚两个阶段）进一步恶化性能；适当的 $\alpha$（如 1）在压缩冗余的同时保持性能，而过高的 $\alpha$ 则使惩罚减弱，响应长度回升。这一机制使得 PEAR 能够在不同任务难度和模型规模下灵活调节压缩强度。

## 整体框架

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/002_Figure_1.jpg]]
*Figure 1: PEAR reduces the response length by penalizing excessive entropy during the thinking phase while allowing moderate exploration at the final answer phase*

PEAR 的整体 pipeline 建立在 GRPO（Group Relative Policy Optimization）的强化学习框架之上，通过仅修改奖励信号实现推理效率的提升，不引入额外的模型组件或数据筛选流程。其核心设计在于将模型生成的完整响应按阶段划分，并利用阶段性熵作为效率调节的“控制旋钮”。

### 模块关系与数据流

PEAR 的训练流程由四个顺序耦合的模块构成，形成“采样—熵计算—奖励重构—策略更新”的闭环：

1. **响应采样与熵计算**  
   对于每个输入提示 $q$，从旧策略 $\pi_{\theta_{\text{old}}}$ 中采样 $G$ 个完整响应。对每个响应中的每个令牌 $t$，计算其在旧策略下的令牌级熵：
   $$H_t = - \sum_{v\in\mathcal{V}} \pi_{\theta_{\text{old}}}(v | y_{<t}) \log \pi_{\theta_{\text{old}}}(v | y_{<t})$$
   随后，根据响应的结构标记（`<think>` 至 `</think>`）将令牌划分为思考阶段和最终回答阶段，分别计算两阶段的平均熵：
   $$\bar{H}_{\text{think}} = \frac{1}{k-1}\sum_{t=1}^{k-1} H_t,\quad \bar{H}_{\text{answer}} = \frac{1}{T-k}\sum_{t=k+1}^{T} H_t$$
   其中 $k$ 为 `</think>` 标记的位置，$T$ 为响应总长度。这一模块是整个 pipeline 的感知层，为后续奖励计算提供阶段粒度的熵信号。

2. **阶段性熵感知奖励计算**  
   基于两阶段平均熵，构建相位惩罚项：
   $$\mathcal{P}(y) = \max(0, \bar{H}_{\text{think}} - \alpha \bar{H}_{\text{answer}})$$
   该惩罚项的核心机制是：当思考阶段熵显著高于回答阶段熵时，惩罚增大，从而抑制过度探索；超参数 $\alpha$（默认设为 1）调节回答阶段熵对惩罚的抵消程度。最终 PEAR 奖励函数为：
   $$r(y) = \begin{cases} \min(1, s - \mathcal{P}(y)), & \text{if answer correct} \\ r_{\text{fmt}}, & \text{otherwise} \end{cases}$$
   正确回答的奖励由基准分 $s$（通常为 1）减去相位惩罚得到，上限为 1；错误回答仅获得固定的格式奖励 $r_{\text{fmt}}$。这一设计的关键在于：奖励信号同时编码了答案正确性和推理效率，且效率约束仅作用于正确样本，避免对错误样本施加额外惩罚。

3. **组优势归一化**  
   用 PEAR 奖励 $r(y_i)$ 替换 GRPO 原有的规则二元奖励，对同一提示下的 $G$ 个响应进行组内标准化：
   $$A_i = \frac{r(y_i) - \text{mean}(\{r(y_j)\}_{j=1}^G)}{\text{std}(\{r(y_j)\}_{j=1}^G)}$$
   标准化后的优势 $A_i$ 反映了每个响应在组内的相对质量：正确且简洁的响应获得正优势，正确但冗长的响应因相位惩罚获得较低的相对优势，错误响应则获得负优势。

4. **策略优化**  
   策略更新保持与 GRPO 相同的裁剪代理目标与 KL 散度正则化，使用上述优势估计进行梯度更新。PEAR 仅改变了传入优势计算的标量奖励值，未修改损失函数形式或模型架构。

### 输入输出规范

- **输入**：训练提示 $q$（来自 GSM8K 训练集，共 7,473 个样本），每个提示采样 $G$ 个响应。
- **输出**：更新后的策略参数 $\theta$，使模型在推理时生成更简洁的思维链。
- **推理时**：模型直接自回归生成，无需额外的熵计算或惩罚注入——效率提升已内化到策略参数中。

### 与基线方法的本质区别

PEAR 与现有方法的根本差异在于“控制变量的选择”：
- **GRPO**（Shao et al., 2024）仅使用二元正确/错误奖励，对响应长度无任何约束，导致模型倾向于生成冗长的探索性推理。
- **Step Entropy**（Li et al., 2025）通过插入 `[SKIP]` 令牌的两阶段训练来压缩思维链，需要额外的训练阶段和数据工程。
- **LCPO**（Aggarwal & Welleck, 2025）通过显式长度约束联合优化准确性和长度，需要预设目标长度。

PEAR 的核心优势在于：它不依赖人工设定的长度目标、不引入额外的训练阶段或数据筛选，而是通过单一超参数 $\alpha$ 调节阶段熵的惩罚强度，使模型在强化学习过程中自主学会平衡探索与效率。这一设计的理论依据来自初步分析中的两个关键发现：(1) 模型熵与响应长度呈一致正相关（Figure 2(a)）；(2) 思考阶段的熵显著高于最终回答阶段（Figure 2(b)），且去除高达 40% 的高熵令牌不会损害准确性（Figure 3），证明冗余主要集中在思考阶段的高熵探索行为中。

## 核心模块与公式推导

PEAR 的核心设计思想是将模型在推理过程中的令牌级熵（token-level entropy）按阶段分解，并将阶段熵差作为惩罚信号嵌入奖励函数，从而在策略优化中引导模型抑制冗余探索。整个方法由四个紧密衔接的模块构成，其数学基础建立在 GRPO（Group Relative Policy Optimization）框架之上。

### 令牌级熵与阶段熵分解

PEAR 首先对模型在生成每个令牌时的不确定性进行量化。给定旧策略 $\pi_{\theta_{\mathrm{old}}}$，令牌 $t$ 的熵定义为：

$$H_t = - \sum_{v\in\mathcal{V}} \pi_{\theta_{\mathrm{old}}}(v | y_{<t}) \log \pi_{\theta_{\mathrm{old}}}(v | y_{<t})$$

其中 $\mathcal{V}$ 为词表，$y_{<t}$ 表示前 $t-1$ 个已生成令牌。该熵值反映了模型在当前上下文下的预测不确定性：高熵意味着模型在多个候选令牌间犹豫不决，通常对应探索性推理行为；低熵则表明模型对下一步输出高度确定，对应确定性表达。

基于大型推理模型（LRMs）的响应结构特征——生成内容被 `<think>` 和 `</think>` 标签自然划分为思考阶段与最终回答阶段——PEAR 将整条响应的熵分解为两个阶段的平均熵。设响应总长度为 $T$，`<think>` 标签位于位置 $k$，则：

$$\bar{H}_{\mathrm{think}} = \frac{1}{k-1}\sum_{t=1}^{k-1} H_t,\quad \bar{H}_{\mathrm{answer}} = \frac{1}{T-k}\sum_{t=k+1}^{T} H_t$$

这种分解的动机来自初步分析中的关键发现：思考阶段的熵显著高于最终回答阶段（Figure 2(b)），且模型平均熵与响应长度呈正相关（Figure 2(a)）。进一步，熵过滤实验（Figure 3）表明，去除高达 40% 的高熵令牌不会损害准确性，证明冗余主要集中在思考阶段的高熵区域。

### 阶段性熵感知惩罚

基于上述分解，PEAR 构造一个相位惩罚项 $\mathcal{P}(y)$，用于量化思考阶段相对于回答阶段的过度熵：

$$\mathcal{P}(y) = \max(0, \bar{H}_{\mathrm{think}} - \alpha \bar{H}_{\mathrm{answer}})$$

其中 $\alpha$ 是调节回答阶段熵贡献的超参数。该设计的因果逻辑是：当思考阶段熵远高于回答阶段熵时，$\mathcal{P}(y)$ 取正值，表示存在过度探索；当两者接近或思考阶段熵较低时，惩罚归零，不施加额外约束。$\alpha$ 的作用机制在于：降低 $\alpha$ 会放大 $\bar{H}_{\mathrm{think}}$ 的相对权重，增强对思考阶段的压缩力度；提高 $\alpha$ 则通过 $\alpha \bar{H}_{\mathrm{answer}}$ 抵消部分惩罚，保留更多探索空间。

### PEAR 奖励函数

PEAR 将相位惩罚集成到 GRPO 的奖励信号中，替换原有的二元正确/错误奖励。最终奖励函数为：

$$r(y) = \begin{cases} \min(1, s - \mathcal{P}(y)), & \text{if answer correct} \\ r_{\mathrm{fmt}}, & \text{otherwise} \end{cases}$$

- **正确回答**：获得基准分 $s$ 减去相位惩罚 $\mathcal{P}(y)$，并通过 $\min(1, \cdot)$ 截断至上限 1。这意味着即使答案正确，过度冗余的思考过程也会降低奖励，从而驱动策略向更简洁的推理轨迹优化。
- **错误回答**：仅获得固定的格式奖励 $r_{\mathrm{fmt}}$，不施加熵惩罚，避免对错误样本的额外压制。

### 组优势归一化与策略更新

PEAR 仅修改每个样本的标量奖励，策略更新的裁剪代理目标（clipped surrogate objective）与 KL 散度正则化完全沿用 GRPO 框架。具体而言，对于同一提示 $q$ 下采样得到的 $G$ 个响应 $\{y_i\}_{i=1}^G$，PEAR 首先计算每个响应的奖励 $r(y_i)$，然后进行组内标准化得到优势估计：

$$A_i = \frac{r(y_i) - \mathrm{mean}(\{r(y_j)\}_{j=1}^G)}{\mathrm{std}(\{r(y_j)\}_{j=1}^G)}$$

策略参数 $\theta$ 的更新目标为：

$$\mathcal{J}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot|q)} \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \min\left[ r_{i,t}(\theta) A_i, \operatorname{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) A_i \right]$$

其中概率比 $r_{i,t}(\theta) = \frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid q, o_{i,<t})}$，$\epsilon$ 为裁剪阈值。

### 模块间因果链条

四个模块形成闭环的因果调控链路：**响应采样与熵计算**提供阶段熵信号→**相位惩罚计算**将熵差转化为标量惩罚→**PEAR 奖励函数**将惩罚与正确性信号融合→**组优势归一化与策略更新**通过梯度下降将奖励差异反馈至策略参数。这一链条的核心调节变量是思考阶段与回答阶段的熵差 $\bar{H}_{\mathrm{think}} - \alpha \bar{H}_{\mathrm{answer}}$，它直接决定了模型在探索（高熵）与利用（低熵）之间的平衡点。实验验证（Figure 4(a)）表明，PEAR 训练后思考阶段的熵下降幅度最大，证实惩罚机制确实精准作用于目标阶段。

## 实验与分析

### 核心瓶颈的实证锚定

PEAR 的设计动机源自对大型推理模型（LRMs）推理行为中一个可复现现象的观察：**模型熵与响应长度之间存在一致的正相关关系**。如 Figure 2(a) 所示，在多个模型系列（包括 DeepSeek-R1-Distill-Qwen/Llama 的不同规模变体）上，平均熵越高的模型，其生成的响应长度也越长。这一关系并非简单的线性对应——Figure 2(b) 进一步揭示了推理过程内部的**阶段性不对称性**：思考阶段（`<think>` 至 `</think>`）的令牌级熵显著高于最终回答阶段。这意味着模型的“探索性冗余”高度集中于思考阶段，而最终回答阶段则表现为相对确定性的表达。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/004_Figure_2.jpg]]
*Figure 2: (a) Relationship between average entropy and response length across different models. The dot size indicates accuracy. DS(L) represents DeepSeek-R1-Distill-Qwen/Llama. (b) Comparison of average entropy between the thinking phase and the final answer phase*

为量化这种冗余对准确性的实际贡献，作者进行了**熵过滤实验**（Figure 3）：按令牌熵值从低到高排序，逐步滤除高熵令牌，仅保留低熵部分。在 Qwen3-4B 上，当保留 80% 甚至 60% 的低熵令牌时，准确率不仅未下降，反而略有提升，同时响应长度大幅缩减；仅当保留比例降至 40% 以下时，准确率才出现断崖式下跌。这一结果表明，**响应中相当比例的高熵令牌（可达 40%）属于冗余探索，其移除不会损害核心推理质量**，且冗余主要富集于思考阶段。该发现在 Qwen3-8B 上得到验证（Figure 6），增强了结论的跨尺度可靠性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/005_Figure_3.jpg]]
*Figure 3: Accuracy and average response length in the entropy filtering experiments on Qwen3-4B*

### 主要结果：效率-准确性折衷

Table 1 汇总了 PEAR 与基线方法在三个模型尺度、六个基准上的 Acc@1 与生成令牌数对比。PEAR 在所有尺度上实现了**响应长度的最大幅度压缩**，同时将准确性损失控制在极小范围内：

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/006_Table_1.jpg]]
*Table 1: Acc@1 results on mathematical reasoning benchmarks across LRMs. ↓ indicates the relative change with respect to the Original row of each model. PEAR consistently achieves the largest reduction in token usage across model scales, while maintaining comparable accuracy*

| 模型 | 方法 | 平均准确率 | 平均生成令牌数 | 令牌变化 |
|------|------|-----------|---------------|---------|
| Qwen3-4B | Original | 74.85% | 7428 | — |
| | GRPO | 75.12% | 7467 | +0.5% |
| | Step Entropy | 74.65% | 5251 | -29.3% |
| | LCPO | 68.18% | 5753 | -22.5% |
| | **PEAR** | **74.27%** | **3221** | **-56.6%** |
| Qwen3-8B | Original | 77.48% | 6845 | — |
| | **PEAR** | **77.56%** | **3200** | **-53.3%** |
| DeepSeek-R1-Distill-Qwen-1.5B | Original | 56.62% | 4548 | — |
| | **PEAR** | **56.07%** | **3075** | **-32.4%** |

PEAR 的三个关键优势在此表中清晰呈现：

1. **压缩幅度远超同类方法**：在 Qwen3-4B 上，PEAR 的 56.6% 令牌缩减显著优于 Step Entropy（29.3%）和 LCPO（22.5%），且后两者均伴随明显的准确率下降（LCPO 下降逾 6 个百分点）。
2. **准确性几乎无损**：PEAR 在三个尺度上的准确率变化分别为 -0.58%、+0.08% 和 -0.55%，均小于 1%，远优于同等压缩水平下的其他方法。
3. **跨尺度稳健性**：从 1.5B 到 8B，PEAR 始终在保持准确率的同时实现 32.4%–56.6% 的令牌缩减，表明其机制不依赖于特定模型容量。

Table 2 将验证扩展至不同模型系列与更大规模（Qwen3-14B、DeepSeek-R1-Qwen3-8B、DeepSeek-R1-Distill-Llama3.1-8B），PEAR 在五个基准上的平均准确率从 81.15%（Original）提升至 81.95%，同时令牌用量从 5364 降至 3708（-30.87%），进一步验证了该方法在跨架构场景下的有效性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/011_Table_2.jpg]]
*Table 2: Acc@1 results on five benchmarks across three LRMs in different size and model series. ↓ / ↑ indicates the relative change in average token usage with respect to the Original row of each model*

### 机制验证：熵的因果调控

Figure 4 从熵变化和推理结构两个维度揭示了 PEAR 的作用机理。Figure 4(a) 显示，PEAR 训练后，思考阶段的熵出现显著下降，而最终回答阶段的熵变化相对温和。这与 PEAR 奖励函数的设计预期一致：惩罚项 $\mathcal{P}(y) = \max(0, \bar{H}_{\text{think}} - \alpha \bar{H}_{\text{answer}})$ 主要抑制思考阶段的过度熵，同时通过 $\alpha$ 系数保留回答阶段的适度灵活性。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_HLc2igXEA3/figures/008_Figure_4.jpg]]
*Figure 4: (a) Entropy changes before and after training with PEAR across thinking and final answer phases. (b) Changes in the number of reasoning steps and average tokens per step for Qwen3-4B. PEAR reduces both the number of reasoning steps and the average tokens per step*

Figure 4(b) 进一步表明，PEAR 对推理轨迹的压缩是**双通道的**：既减少了思考阶段的推理步骤数，也降低了每步的平均令牌数。在困难数据集 AIME24 上，思考步骤数减少超过一半，说明 PEAR 并非简单截断推理，而是从根本上抑制了冗余探索行为的生成。

### 超参数 α 的调控效应

Figure 5 展示了超参数 α 对 Qwen3-4B 准确率与响应长度的调控作用，揭示了 PEAR 惩罚机制的精妙平衡：

- **α = 0**（仅惩罚思考阶段熵，忽略回答阶段）：准确率显著受损。这是因为模型在回答阶段失去了必要的表达灵活性，过度压缩导致推理不充分。
- **α = -1**（同时惩罚两个阶段）：性能进一步恶化，说明对回答阶段的负向惩罚直接损害了答案生成的确定性。
- **α 适度增大**（如 α = 1）：在压缩冗余与保持准确性之间取得最优平衡。过高的 α 值会削弱惩罚强度，导致响应长度回升，压缩效果减弱。

这一消融实验表明，**PEAR 的有效性依赖于对两个阶段熵的差异化调控**——思考阶段需要抑制冗余探索，回答阶段需要保留适度熵以维持表达灵活性。α 正是调节这一平衡的关键旋钮。

### 定性分析

Figure 7 的案例研究对比了原始 Qwen3-8B 与 PEAR 微调模型在同一数学问题上的推理轨迹。原始模型产生了大量反思性冗余语句（如反复验证已确定的中间结果），而 PEAR 模型在保持推理正确性的前提下，显著压缩了这些冗余反思，生成更简洁、更直接的推理路径。这一现象与熵过滤实验的结论一致：高熵令牌主要对应冗余探索，而非核心推理逻辑。

### 实验公平性说明

所有实验均在统一框架下进行：训练集为 GSM8K（7473 样本），测试涵盖数学推理（GSM8K、MATH500、AIME24、AMC23）和知识/领域外任务（GPQA Diamond、MMLU）。评估采用 Acc@1 与生成令牌数双维度指标，生成长度上限 16384，温度 0.6，top-p 0.95。PEAR 仅改变奖励信号，未修改模型架构或数据分布，与基线 GRPO 的对比在相同训练配置下公平进行。

## 方法谱系与知识库定位

### 1. 与基线方法的关系

PEAR 的核心贡献在于重新设计了强化学习中的奖励信号，而非引入新的模型架构或训练范式。其直接技术底座是 **GRPO**（Group Relative Policy Optimization, Shao et al., 2024），一种通过组内奖励归一化消除对评论家模型依赖的策略优化方法。PEAR 完整保留了 GRPO 的裁剪代理目标、KL 散度正则化以及组优势归一化框架，唯一的改动是将原始的二元正确/错误规则奖励替换为阶段性熵感知奖励。

与现有推理效率优化方法相比，PEAR 处于一条独特的技术路径上：

- **Step Entropy**（Li et al., 2025）采用两阶段训练策略，通过插入 `[SKIP]` 令牌来缩短思维链，这需要修改训练流程并引入额外的数据标注。PEAR 则无需任何数据层面的干预，仅在奖励函数中引入熵惩罚即可实现端到端的推理压缩。

- **LCPO**（Length-Controlled Policy Optimization, Aggarwal & Welleck, 2025）通过联合优化准确性和显式长度约束来控制响应长度，这要求预设目标长度或长度预算。PEAR 不依赖任何显式长度目标，而是通过相位熵的差值自适应地调节压缩强度——当思考阶段过度探索时自动施加强惩罚，而当回答阶段需要灵活性时保留适度熵。

从方法论角度看，PEAR 的本质是将“推理效率”这一目标从显式约束转化为隐式奖励信号，使模型在最大化奖励的过程中自发学会简洁推理。这种“奖励塑形”思路使得 PEAR 可以与任何基于 GRPO 的推理模型训练流程无缝集成，而无需修改数据、架构或优化器。

### 2. 适用边界与局限

PEAR 的有效性建立在两个关键假设之上，这些假设同时界定了其适用边界：

**假设一：高熵令牌主要承载冗余探索而非核心推理。** 熵过滤实验（Figure 3, Figure 6）表明，去除高达 40% 的高熵令牌不会损害准确性，这验证了冗余集中于高熵区域的假设。然而，这一假设的普适性存在边界：在需要深度探索的复杂推理任务（如多步数学证明、开放式科学推理）中，部分高熵令牌可能承载着关键的探索性思维，过度惩罚可能导致“欠推理”风险。论文在 AIME24 等困难基准上的实验（思考步骤减少超过一半，Figure 4(b)）虽未观察到显著的准确率下降，但更极端的任务场景仍需验证。

**假设二：思考阶段与回答阶段的熵具有可分离的因果效应。** PEAR 通过超参数 α 调节两个阶段熵的贡献，α=1 时惩罚项为 `max(0, H_think - H_answer)`。这种设计隐含地假设思考阶段的高熵是冗余的，而回答阶段的熵是必要的。超参数研究（Figure 5）证实了这一假设的脆弱性：α=0（仅惩罚思考熵）会损害准确率，α=-1（同时惩罚两个阶段）则进一步恶化性能。这意味着 PEAR 的性能对 α 的选择具有一定敏感性，而当前论文未提供自动选择 α 的机制。

**方法本身的局限还包括：**

- **训练数据依赖性**：所有实验均使用 GSM8K（7,473 样本）进行训练，该数据集以小学数学题为主。在代码生成、多语言推理或领域专业知识问答等分布外任务上，PEAR 的泛化能力尚未被系统评估。
- **模型规模上限**：实验覆盖的最大模型为 Qwen3-14B（Table 2），在 70B+ 规模模型上的效率-准确性折衷趋势尚不明确。更大规模模型可能具有不同的熵分布特征，PEAR 的惩罚强度可能需要重新校准。
- **奖励设计的二元性**：PEAR 对错误回答仅给予固定的格式奖励 `r_fmt`，不施加熵惩罚。这意味着模型在错误轨迹上不会受到压缩压力，可能导致训练效率降低或策略优化方向的偏差。

### 3. 开放问题

基于上述分析，PEAR 开启了以下值得进一步探索的方向：

1. **自适应 α 选择机制**：当前 α 作为全局超参数固定，但不同任务、不同难度的问题可能需要不同的压缩强度。是否可以通过元学习或在线自适应方法，使模型根据问题难度动态调整 α？

2. **与架构级效率方法的协同**：PEAR 在奖励层面压缩推理，而动态早退、跳步令牌、KV 缓存压缩等方法在推理时层面提升效率。两者是否可以叠加，在不牺牲准确性的前提下实现更极致的效率提升？

3. **跨领域泛化与熵下限**：在代码生成、科学问答等需要不同推理模式的领域中，思考阶段的“必要熵”水平可能不同。是否需要针对不同领域设定不同的熵下限，以避免过度压缩导致关键探索被抑制？

4. **欠推理的检测与缓解**：PEAR 的惩罚机制在极端情况下可能导致模型过早终止推理。是否可以设计一种“推理充分性”监测信号，在检测到潜在欠推理时动态降低惩罚强度？

5. **更大规模模型的验证**：在 70B+ 参数规模的模型上，PEAR 的效率-准确性折衷曲线是否会保持线性趋势，还是会出现新的相变行为？这需要更大规模的实验验证。

### 4. 知识库定位

PEAR 处于以下研究脉络的交汇点：

- **推理效率优化**：与 Step Truncation、Early Exit、Token Skipping 等方法并列，属于不修改模型架构的轻量级效率提升方法。
- **强化学习奖励塑形**：继承 GRPO 的无评论家框架，通过奖励函数设计而非策略约束来实现行为引导，与 RLHF 中的 KL 惩罚、长度惩罚等方法共享技术基因。
- **熵正则化与探索控制**：将信息论中的熵概念引入推理过程控制，与最大熵强化学习、熵正则化策略梯度等方法形成概念连接，但 PEAR 首次将熵的相位分解应用于推理效率优化。

PEAR 的核心洞察——思考阶段的高熵对应冗余探索，回答阶段的适度熵对应必要灵活性——为理解大型推理模型的内部行为提供了新的分析维度，也为后续的推理效率研究开辟了“以熵为信号”的技术路线。

## 原文 PDF

![[paperPDFs/ICLR_2026/PEAR_Phase_Entropy_Aware_Reward_for_Efficient_Reasoning.pdf]]
