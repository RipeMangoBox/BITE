---
title: "RL for Reasoning by Adaptively Revealing Rationales"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RL_for_Reasoning_by_Adaptively_Revealing_Rationales.pdf
openreview_forum_id: wdbgTG5kib
aliases:
- AAB
- RRBARR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "每个训练样本的监督前缀比例 ρ（supervision ratio），它决定了模型在生成时能看到目标答案的多少前缀，并通过奖励阈值动态调节，从而控制任务难度。"
primary_logic: "通过根据模型奖励反馈自适应地揭示目标输出的部分前缀，模型能够逐步学会补全推理链，将原本的长序列稀疏奖励问题分解为一系列较短的子任务，每个子任务具有较高的成功概率，从而实现从监督到无监督的平滑过渡，扩展了可学习任务的范围。"
claims:
- "在合成奇偶校验链任务上，AdaBack成功学习，而SFT、RL及其组合均失败，证明了自适应回溯能够解决SFT和RL无法处理的推理任务。"
- "在DeepScaleR、MATH、GSM8k等数学推理基准上，AdaBack一致超越标准RL和SFT+RL基线，尤其在分布外设置（如Tensor-2 GSM8k）上优势明显。"
- "AdaBack显著提升pass@k指标，表明其扩展了模型的解空间，而非仅仅重新加权已有的答案分布。"
- "DeepScaleR (1B) 上 Test Accuracy = 9.0 (AdaBack)"
---

# RL for Reasoning by Adaptively Revealing Rationales

> [!tip] 核心洞察
> 通过根据模型奖励反馈自适应地揭示目标输出的部分前缀，模型能够逐步学会补全推理链，将原本的长序列稀疏奖励问题分解为一系列较短的子任务，每个子任务具有较高的成功概率，从而实现从监督到无监督的平滑过渡，扩展了可学习任务的范围。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于自适应揭示推理链的强化学习推理方法 |
| 英文题名 | RL for Reasoning by Adaptively Revealing Rationales |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=wdbgTG5kib) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AdaBack (Adaptive Backtracking) |
| Dataset | DeepScaleR (1B), Tensor-2 GSM8k (1B), MATH (3B, base model), DeepScaleR (1B |

> [!tip] 效果简介
> - DeepScaleR (1B) 上，Test Accuracy 为 9.0 (AdaBack)，对比 6.8 (Base+RL)，变化 +2.2。
> - Tensor-2 GSM8k (1B) 上，Test Accuracy 为 8.5 (AdaBack)，对比 0.0 (Base+RL)，变化 +8.5。
> - MATH (3B, base model) 上，Test Accuracy 为 19.1 (AdaBack)，对比 15.0 (Base+RL)，变化 +4.1。

## 概述

### 问题瓶颈

在长序列推理任务中，强化学习（RL）面临奖励稀疏的挑战。假设每步推理的正确概率为 $p$，生成完整 $n$ 步正确推理链的概率仅为 $p^n$，随序列长度呈指数衰减。这意味着标准RL在训练初期几乎无法获得任何有效奖励信号，随机探索难以找到正确的解路径，导致模型无法从零开始学会复杂推理。

### 核心方法

**AdaBack（自适应回溯）** 是一种逐样本课程学习算法，通过在RL训练中动态揭示目标答案的部分前缀来解决奖励稀疏问题。其核心机制是：为每个训练样本维护一个监督比例区间 $[\rho_{\min}, \rho_{\max}]$，每轮训练从中均匀采样一个比例 $\rho$，决定揭示目标答案多少比例的前缀作为条件输入。模型只需补全剩余部分，从而将原本的长序列稀疏奖励问题分解为一系列较短的子任务。

区间根据模型在该样本上的平均奖励 $r_t^{(i)}$ 与固定阈值 $\tau$ 的比较进行更新：若奖励低于阈值，则扩大监督比例（降低难度）；若奖励达到阈值，则缩小监督比例（提高难度），并将 $\rho_{\min}$ 重置为0。这一机制使每个样本沿自己的轨迹从完全监督平滑过渡到完全自主生成，实现从监督学习到强化学习的自然衔接。

### 方法定位

在推理任务的训练方法谱系中，AdaBack位于监督微调（SFT，$\rho=1$）与标准强化学习（$\rho=0$）之间，通过自适应调度填补了两者之间的空白。与固定步长切片的课程学习方法 **R3**（Xi et al., 2024）相比，AdaBack的逐样本自适应策略使其在困难任务上效率显著更高——在链式奇偶校验任务上，R3需要超过16000次迭代才达到0.8奖励，而AdaBack仅需不到700次。

### 关键发现

1. **解决SFT和RL均失败的任务**：在合成链式奇偶校验任务（L=16）上，标准RL和SFT+RL均完全失败（奖励停留在约0.1），而AdaBack成功学会该任务（奖励接近1.0），证明了自适应回溯能够突破标准方法的可学习边界。

2. **跨基准一致提升**：在DeepScaleR、MATH、GSM8k等数学推理基准上，AdaBack一致超越标准RL和SFT+RL基线。尤其在分布外设置（如Tensor-2 GSM8k）上优势明显——标准RL准确率为0%，AdaBack达到8.5%。

3. **扩展解空间而非重新加权**：pass@k分析显示，AdaBack在高k值下仍保持对标准RL的显著优势，且在无SFT初始化的基模型上也能提升高k性能，表明其扩展了模型的解分布而非仅仅重新加权已有答案。

4. **高度鲁棒**：奖励阈值 $\tau$ 在0.1至0.9范围内，最终训练奖励和测试准确率趋于一致，表明方法对超参数选择不敏感。

### 适用边界

AdaBack依赖可验证的最终答案奖励信号，适用于数学等可自动判断正确性的领域。对于指令微调模型或在预训练中已大量接触任务分布的模型，训练奖励会迅速饱和，AdaBack无法提供额外帮助。当推理步骤可清晰分割时，随机位置揭示前缀的策略可能不如按步骤切片的课程方法高效。

## 背景与动机

### 长序列推理中的奖励稀疏困境

在大语言模型的强化学习（RL）训练中，模型通过生成完整答案并接收最终奖励信号来优化策略。然而，当推理任务需要多个步骤才能得到正确答案时，这一范式面临根本性困难：生成完整正确推理链的概率随序列长度呈指数衰减。具体而言，若每个推理步骤的正确生成概率为 $p$，则模型一次性生成 $n$ 步完整正确解的概率仅为 $p^n$。这意味着模型在随机探索中获得正向奖励信号的期望迭代次数为 $p^{-n}$，即随序列长度指数增长。

这一奖励稀疏问题构成了当前推理模型训练的核心瓶颈。在标准RL框架下（如 **GRPO**，Shao et al., 2024），模型必须从头生成完整答案，导致在长序列任务中几乎无法获得有效奖励信号，探索效率极低。监督微调（SFT）虽然通过揭示完整目标序列（$\rho=1$）提供了密集的监督信号，但模型仅仅学会了模仿，缺乏自主探索和纠错能力。将SFT与RL结合的常见流程（**SFT+GRPO**）同样面临困境：SFT阶段的完整监督无法为后续RL阶段提供有效的探索引导，模型在RL阶段仍需面对完整的稀疏奖励问题。

### 现有课程学习方法的局限

为缓解上述困难，研究者提出了基于课程学习的方法，如 **R3**（Xi et al., 2024）。R3通过在分隔符位置（如GSM8k中的换行符）将示范答案静态切片为固定步长的片段，并将这些片段混合训练。然而，这种全局固定步长的切片策略存在两个关键缺陷：

1. **缺乏逐样本适应性**：不同问题的难度和推理步骤数量差异显著，全局统一的切片策略无法针对每个样本的特点调整监督程度。
2. **依赖启发式分割**：R3需要预先定义分隔符和切片策略，这不仅引入了额外的超参数，而且在无明确步骤结构的任务上难以有效应用。

### 核心动机：从稀疏奖励到自适应子任务分解

本文的核心洞察是：**通过根据模型当前的奖励反馈，自适应地揭示目标输出的部分前缀，可以将原本的长序列稀疏奖励问题分解为一系列较短的子任务**。每个子任务仅需补全被遮蔽的后缀部分，其成功概率远高于生成完整序列，从而大幅提高探索效率。

具体而言，该方法为每个训练样本维护一个监督比例 $\rho \in [0,1]$，表示模型在生成时能看到目标答案的前缀长度比例。当模型在某个 $\rho$ 值下能够稳定获得高奖励时，系统自动降低 $\rho$（揭示更少前缀），使任务变难；当模型无法获得足够奖励时，系统自动提高 $\rho$（揭示更多前缀），使任务变易。通过这种基于奖励反馈的自适应调节，模型能够在“刚好能学会”的难度区间内持续训练，实现从高监督到零监督的平滑过渡。

这一思路的核心优势在于：它不依赖任何关于任务结构的先验知识，也不需要手工设计课程进度，而是完全由模型自身的奖励信号驱动，自动为每个样本发现合适的学习路径。

## 核心创新

### 问题瓶颈：长序列推理中的奖励稀疏

在长序列推理任务中，标准强化学习（RL）面临根本性困难：模型需要从头生成完整的正确推理链才能获得正向奖励信号。假设推理链包含 $n$ 个步骤，每步独立成功的概率为 $p$，则一次生成获得奖励的概率仅为 $p^n$，而获得首个有效奖励信号的期望迭代次数为 $p^{-n}$。随着序列长度增长，该概率呈指数衰减，导致随机探索几乎无法获得任何学习信号。这一奖励稀疏问题是制约 RL 在复杂推理任务中有效性的核心瓶颈。

### 核心洞察：自适应前缀揭示将长序列问题分解为短子任务

AdaBack 的核心洞察在于：**通过向模型揭示目标输出的部分前缀，将原本需要完整生成的长序列推理任务，分解为一系列仅需补全剩余部分的较短短子任务**。每个子任务的成功概率由 $p^n$ 提升至 $\Theta(p)$，使得 RL 能够在高概率获得奖励信号的区域内进行有效探索。随着模型能力的逐步提升，揭示的前缀长度自适应减少，最终实现从完全监督（$\rho=1$）到完全自主生成（$\rho=0$）的平滑过渡。

### 关键创新：逐样本自适应监督调度

AdaBack 的核心方法创新在于引入**逐样本自适应监督比例调度**机制，与现有方法形成根本性差异：

| 方法 | 监督水平 | 调度策略 |
|------|---------|---------|
| 标准 RL（GRPO） | $\rho=0$，无前缀揭示 | 固定，模型需生成完整答案 |
| SFT | $\rho=1$，揭示完整目标序列 | 固定，进行监督训练 |
| SFT+RL | 先 $\rho=1$ 后 $\rho=0$ | 两阶段切换，无中间过渡 |
| R3（Xi et al., 2024） | 固定步长切片 | 全局统一课程，按固定段数切分示范 |
| **AdaBack** | $\rho \in [0,1]$ 动态采样 | **逐样本根据奖励反馈自适应调整区间** |

具体而言，AdaBack 为每个训练样本维护独立的监督比例区间 $[\rho_{\min}^{(i)}, \rho_{\max}^{(i)}]$，初始化为 $[0,1]$。每轮训练时，从当前区间均匀采样监督比例 $\rho_t^{(i)} \sim U(\rho_{\min}^{(i)}, \rho_{\max}^{(i)})$，揭示目标答案的 $\rho_t^{(i)}$ 比例前缀作为条件输入，模型仅需生成剩余部分。随后利用 GRPO 框架生成多个 rollout 并计算平均奖励 $r_t^{(i)}$，根据以下规则更新区间：

$$\text{If } r_t^{(i)} < \tau: \rho_{\min}^{(i)} \leftarrow \rho_t^{(i)}; \quad \text{If } r_t^{(i)} \geq \tau: \rho_{\max}^{(i)} \leftarrow \rho_t^{(i)}, \rho_{\min}^{(i)} \leftarrow 0.0$$

该更新规则本质上是一种**随机二分搜索**：当模型在当前监督水平下表现不佳时，缩小搜索区间下界以增加监督；当表现达标时，将上界收紧并重置下界为零，允许模型尝试更低监督水平。这一机制使得每个样本按照自身难度和学习进度独立推进，简单样本快速降低监督比例，困难样本则维持在较高监督水平直至能力就绪。

### 相对于 R3 的本质差异

R3（Xi et al., 2024）同样采用分段揭示策略，但其本质是**静态数据增强**：将示范按固定分隔符（如 GSM8k 中的换行符）切分为片段，混合后统一进行 RL 训练。这种全局统一课程缺乏对样本难度的自适应感知。AdaBack 的逐样本自适应机制消除了对分段超参数和启发式全局课程设计的依赖，在合成链式奇偶校验任务上，AdaBack 在不到 700 次迭代内即学会任务，而 R3 需要超过 16,000 次迭代才达到 0.8 奖励，效率差距显著（Figure 2）。

### 辅助机制设计

为增强方法的实用性和鲁棒性，AdaBack 还引入了两项辅助机制：

- **全局移动平均初始化**：对于无历史奖励的新样本，使用全局指数移动平均 $\bar{\rho}_{\min} \leftarrow \alpha \rho_{\min}^{(i)} + (1-\alpha) \cdot \bar{\rho}_{\min}$ 估计合适的初始监督水平，避免从零开始探索。
- **零监督注入**：以 10% 概率直接设置 $\rho=0$，减小训练-测试分布差异并加速向完全自主生成的收敛。

这两项机制在消融实验中被证实对最终性能有积极贡献，但 AdaBack 的核心增益仍来源于逐样本自适应调度本身。

## 整体框架

AdaBack 的核心设计是在标准强化学习训练循环中插入一个**逐样本自适应课程调度器**，通过动态揭示目标答案前缀来调控每个训练样本的难度，从而将长序列稀疏奖励问题分解为一系列可解的子任务。整个 pipeline 由七个模块串联构成，形成“采样-生成-评估-更新”的闭环。

### 输入输出流

训练时，每个样本 $i$ 的输入由两部分拼接而成：原始问题 $X^{(i)}$ 与揭示的部分答案前缀 $Y_{1:k}^{(i)}$，其中 $k = \lfloor \rho_t^{(i)} \cdot |Y^{(i)}| \rfloor$，$\rho_t^{(i)} \in [0,1]$ 为当前轮次的监督比例。模型 $\theta$ 以此拼接序列为条件，生成剩余部分 $\hat{Y}_{k+1:m_i'}^{(i)} \sim P_\theta(\cdot \mid X^{(i)}, Y_{1:k}^{(i)})$。完整输出 $\hat{Y}^{(i)}$ 与目标答案 $Y^{(i)}$ 比较，由可验证奖励函数（如答案正确性判断）给出二值奖励信号。训练目标与 GRPO 一致，通过多次 rollout 估计优势函数并更新策略。

### 模块关系与执行流程

1. **Prompt Prefix Conditioning**：接收问题文本与当前轮次揭示的答案前缀，拼接为生成器的条件输入。这是模型与调度器之间的唯一接口，前缀长度由后续模块动态决定。

2. **Per-Sample Interval Manager**：为每个训练样本 $i$ 维护一个监督比例区间 $[\rho_{\min}^{(i)}, \rho_{\max}^{(i)}]$，初始化为 $[0, 1]$。该区间记录了模型对该样本当前能力的估计：区间下界表示模型已能稳定完成的最低监督水平，上界表示仍需探索的最高监督水平。

3. **Uniform Sampling**：每轮训练从当前区间均匀采样监督比例 $\rho_t^{(i)} \sim U(\rho_{\min}^{(i)}, \rho_{\max}^{(i)})$，决定本次揭示的答案长度比例。均匀采样的随机性保证了探索的多样性，避免模型过拟合到特定的前缀长度。

4. **Reward Evaluation**：使用 GRPO 框架生成多个 rollout（默认 8 次），计算该样本的平均奖励 $r_t^{(i)}$。多次 rollout 的平均值提供了对样本难度的稳定估计，降低了单次采样的噪声影响。

5. **Interval Update Rule**：将平均奖励 $r_t^{(i)}$ 与固定阈值 $\tau$ 比较，执行类似随机二分查找的区间更新：
   - 若 $r_t^{(i)} < \tau$（模型尚未掌握该难度），则将下界提升至当前采样值：$\rho_{\min}^{(i)} \leftarrow \rho_t^{(i)}$，使后续训练提供更多监督；
   - 若 $r_t^{(i)} \geq \tau$（模型已能胜任），则将上界收紧至当前采样值：$\rho_{\max}^{(i)} \leftarrow \rho_t^{(i)}$，同时将下界重置为 $0.0$，允许模型向更低的监督水平探索。

   这一规则使得每个样本沿着自己的难度轨迹从完全监督（$\rho=1$）逐步过渡到完全自主生成（$\rho=0$），形成从 SFT 到 RL 的平滑课程。

6. **Global Moving Average Initialization**：对于新加入训练或历史奖励不足的样本，使用全局指数移动平均 $\bar{\rho}_{\min}$ 初始化其 $\rho_{\min}^{(i)}$，更新公式为 $\bar{\rho}_{\min} \leftarrow \alpha \rho_{\min}^{(i)} + (1-\alpha) \cdot \bar{\rho}_{\min}$。这为冷启动样本提供了合理的初始区间估计，避免从 $[0,1]$ 盲目探索。

7. **Zero Supervision Injection**：以 10% 概率直接设置 $\rho=0$，强制模型在无任何前缀揭示的条件下生成完整答案。这一机制减小了训练（有前缀）与测试（无前缀）之间的分布差异，同时加速了模型向完全自主推理的收敛。

### 与标准 RL 的关键差异

标准 RL（如 GRPO）始终以 $\rho=0$ 训练，模型必须从头生成完整推理链。当推理链长度为 $n$、每步成功概率为 $p$ 时，获得正奖励的概率仅为 $p^n$，随 $n$ 呈指数衰减——这正是稀疏奖励困境的数学根源。AdaBack 通过自适应揭示前缀，将原始的长序列生成任务分解为“补全剩余部分”的短序列子任务，每个子任务的成功概率远高于 $p^n$，从而在训练初期即可获得有效的奖励信号，驱动模型逐步习得完整的推理能力。

## 核心模块与公式推导

### 方法总览

AdaBack 的核心机制是**逐样本自适应监督比例调度**：在 RL 训练过程中，对每个训练样本 $i$，维护一个监督比例区间 $[\rho_{\min}^{(i)}, \rho_{\max}^{(i)}]$，从中均匀采样本次训练揭示的目标答案前缀比例 $\rho_t^{(i)}$，并根据 GRPO 多轮采样的平均奖励 $r_t^{(i)}$ 与固定阈值 $\tau$ 的比较，动态调整区间边界，从而为每个样本构建独立的从全监督到全生成的课程轨迹。

### 关键模块

1. **Prompt Prefix Conditioning**
   - 将输入问题 $X^{(i)}$ 与揭示的部分答案前缀 $Y_{1:k}^{(i)}$ 拼接，作为生成器的条件输入，模型只需补全剩余部分 $\hat{Y}_{k+1:m_i'}^{(i)} \sim P_\theta(\cdot \mid X^{(i)}, Y_{1:k}^{(i)})$。
   - 证据锚点：Section 2.1

2. **Per-Sample Interval Manager**
   - 为每个训练样本 $i$ 维护独立的监督比例区间 $[\rho_{\min}^{(i)}, \rho_{\max}^{(i)}]$，初始化为 $[0, 1]$。
   - 证据锚点：Section 2.1

3. **Uniform Sampling**
   - 每轮训练从当前区间均匀采样监督比例：
     $$\rho_t^{(i)} \sim U(\rho_{\min}^{(i)}, \rho_{\max}^{(i)})$$
   - 证据锚点：Section 2.1, Figure 1

4. **Reward Evaluation**
   - 使用 GRPO 框架（Shao et al., 2024）生成多个 rollout，计算样本 $i$ 的平均奖励 $r_t^{(i)}$，作为任务难度的自然估计。
   - 证据锚点：Section 2.1, Section 3

5. **Interval Update Rule**
   - 根据 $r_t^{(i)}$ 与阈值 $\tau$ 的比较，执行随机二分搜索式更新：
     $$\begin{aligned}
     \text{If } r_t^{(i)} < \tau &: \quad \rho_{\min}^{(i)} \leftarrow \rho_t^{(i)} \\
     \text{If } r_t^{(i)} \geq \tau &: \quad \rho_{\max}^{(i)} \leftarrow \rho_t^{(i)}, \quad \rho_{\min}^{(i)} \leftarrow 0.0
     \end{aligned}$$
   - 当奖励低于阈值时，上移区间下界以增加监督比例（降低难度）；当奖励达到阈值时，下移区间上界并重置下界为零（允许探索更低监督比例）。
   - 证据锚点：Section 2.1, Eq. (1)

6. **Global Moving Average Initialization**
   - 对于无历史奖励的新样本，使用全局指数移动平均估计 $\bar{\rho}_{\min}$ 初始化其监督区间：
     $$\bar{\rho}_{\min} \leftarrow \alpha \rho_{\min}^{(i)} + (1-\alpha) \cdot \bar{\rho}_{\min}$$
   - 证据锚点：Section C

7. **Zero Supervision Injection**
   - 以 10% 概率直接设置 $\rho = 0$，强制模型进行全生成，以减小训练-测试分布差异并加速收敛。
   - 证据锚点：Section C

### 核心公式

**朴素 RL 的成功概率**（用于刻画瓶颈）：
$$P_{\text{success}} = p^n$$
其中 $p$ 为单步推理正确概率，$n$ 为推理步数。成功概率随步数呈指数衰减，导致奖励极度稀疏。AdaBack 通过前缀揭示将长序列分解为多个较短子任务，每个子任务的成功概率提升至 $\Theta(p)$ 量级（Section 1）。

**监督比例采样**：
$$\rho_t^{(i)} \sim U(\rho_{\min}^{(i)}, \rho_{\max}^{(i)})$$
从逐样本区间均匀采样，决定第 $t$ 轮训练揭示的目标前缀长度比例（Section 2.1, Figure 1）。

**区间更新规则**：
$$\begin{aligned}
\text{If } r_t^{(i)} < \tau &: \quad \rho_{\min}^{(i)} \leftarrow \rho_t^{(i)} \\
\text{If } r_t^{(i)} \geq \tau &: \quad \rho_{\max}^{(i)} \leftarrow \rho_t^{(i)}, \quad \rho_{\min}^{(i)} \leftarrow 0.0
\end{aligned}$$
该规则实现随机二分搜索：奖励不足时收缩搜索区间到更高监督比例区域，奖励充足时收缩到更低监督比例区域并允许重新探索零监督（Section 2.1）。

### 设计要点

- **逐样本自适应**：每个样本独立维护区间，确保只在模型对该样本准备充分时才降低监督比例，避免固定全局课程导致的效率损失。
- **随机二分搜索**：通过均匀采样而非确定性选择，在探索与利用之间取得平衡，同时自然实现从全监督到全生成的平滑过渡。
- **与 R3 的本质区别**：R3（Xi et al., 2024）采用固定步长的全局切片策略，将示范按分隔符切分为独立训练样本，缺乏逐样本自适应能力；AdaBack 则通过奖励驱动的区间更新，消除了对分割超参数的依赖（Section 4, Table 2）。

## 实验与分析

### 核心瓶颈与因果机制

在长序列推理任务中，标准强化学习面临**奖励稀疏**的根本困境：生成一条完整且正确的 $n$ 步推理链的概率为 $p^n$（每步独立成功概率 $p$），获得正向奖励信号的期望迭代次数则高达 $p^{-n}$。当 $n$ 较大时，随机探索几乎无法触及有效奖励，模型无法从失败中学习。AdaBack 通过引入**逐样本自适应监督比例 $\rho$** 作为因果调节旋钮，将这一困境转化为可解的子问题：模型每次仅需补全从 $\rho$ 比例处截断的剩余推理链，每个子任务的成功概率提升至 $\Theta(p)$ 量级，从而将指数级困难的探索分解为一系列高成功概率的短序列生成任务。

### 整体实验设置

所有 RL 实验统一使用 **GRPO**（Shao et al., 2024）算法，每组 8 次生成（8 rollouts），学习率 $1\times 10^{-6}$，批量大小 256，无 KL 惩罚或熵正则化。为确保公平，标准 RL 训练至少持续到对应 AdaBack 训练的相同迭代次数；测试准确率取最后 5 个检查点的平均值，若性能下降则取最后 5 个奖励上升的迭代平均值。对于非 SFT 初始化的模型，添加格式奖励 $r_{\text{format}}=0.1$ 以鼓励结构化输出，该设置在所有对比方法中保持一致。

### 主实验结果

**Table 1** 汇总了各方法在不同任务和模型规模下的最终测试准确率，AdaBack 在分布外（OOD）设置上展现出最显著的优势：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/002_Table_1.jpg]]
*Table 1: Final test accuracy for each method across tasks and model sizes*

| 基准测试 | 模型规模 | Base+RL | SFT+RL | AdaBack | SFT+AdaBack |
|---------|---------|---------|--------|---------|-------------|
| DeepScaleR | 1B | 6.8 | — | 9.0 | — |
| Tensor-2 GSM8k | 1B | 0.0 | 6.9 | 8.5 | — |
| MATH | 3B (base) | 15.0 | — | 19.1 | — |

在 **Tensor-2 GSM8k**（将多个 GSM8k 问题拼接为长序列的 OOD 任务）上，Base+RL 完全失败（0.0%），而 AdaBack 达到 8.5%，甚至超越 SFT+RL 的 6.9%。在 **DeepScaleR** 上，AdaBack 较 Base+RL 提升 2.2 个百分点；在 **MATH** 上提升 4.1 个百分点。这些结果表明，当任务难度超出模型预训练分布时，自适应前缀揭示机制是突破奖励稀疏瓶颈的关键。

### 与 R3 的对比

**Table 2** 直接对比了 AdaBack 与固定步长切片课程方法 **R3**（Xi et al., 2024）：

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/005_Table_2.jpg]]
*Table 2: Comparison of R3 and AdaBack on GSM8k, MATH, and DeepScaleR*

| 基准 | 规模 | R3 | AdaBack |
|------|------|-----|---------|
| DeepScaleR | 1B | 6.6 | **9.0** |
| DeepScaleR | 3B | 9.6 | **10.6** |
| MATH | 1B | 7.8 | **9.1** |
| MATH | 3B | 19.2 | 19.1 |
| GSM8k | 1B | **41.5** | 39.2 |
| GSM8k | 3B | **74.2** | 73.3 |

AdaBack 在 **DeepScaleR** 上全面领先（1B 提升 2.4，3B 提升 1.0），在 MATH 1B 上也有 1.3 的优势。但在 **GSM8k** 上略低于 R3，论文指出这是因为 GSM8k 的推理步骤可通过换行符清晰分割，R3 的按步骤切片策略恰好匹配该结构；而 AdaBack 采用的随机位置揭示前缀在此类结构化任务上可能不如显式步骤分割高效。这一现象在 **Figure 2** 的合成实验中也有呼应：R3 在链式奇偶校验任务上需要超过 16,000 次迭代才达到 0.8 奖励，而 AdaBack 仅需不到 700 次，说明非自适应策略在缺乏天然步骤边界的任务上效率极低。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/001_Figure_2.jpg]]
*Figure 2: Training Dynamics. Left: Training and test rewards along with supervision ratios throughout training. With AdaBack, Llama 3.2 1B successfully learns the task in under 700 iterations. Right: Training and test rewards for SFT+RL (red) plateau at 0.1, indicating that only the output format—learned during supervised pretraining—has been retained. Test reward for R3 (Xi et al., 2024) is shown in purple; it reaches only 0.8 reward after more than 16,000 iterations. R3 segments training examples at all whitespace positions and applies RL uniformly over these fragments, resulting in inefficiency due to its non-adaptive strategy*

### 解空间扩展的证据

**Figure 4** 展示了 GSM8k 上 pass@k 指标的对比。AdaBack 在 SFT 初始化模型和基模型上均保持对标准 RL 的显著优势，且在高 $k$ 值（如 $k=256$）下优势进一步扩大。基模型上 AdaBack 的 pass@256 接近 0.9，而标准 RL 仅约 0.5。这表明 AdaBack **扩展了模型的解空间**，而非仅仅重新加权已有的答案分布——这与 Yue et al. (2025) 的观察形成对比。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/004_Figure_4.jpg]]
*Figure 4: Pass@k for Llama3-1B SFT-initialized models (left) and base models (right) on GSM8k. AdaBack keeps a significant gap compared to standard RL and improves performance at higher k even without SFT suggesting it expands the solution distribution rather than reweighting known answers (contra Yue et al. (2025))*

### 合成任务上的决定性证据

**Figure 2** 展示了链式奇偶校验任务（$L=16$）上的训练动态。该任务要求模型计算序列的累积奇偶校验值 $Z_i = Z_{i-1} \oplus Y_i \oplus X_i$（$Z_0=0$），长程依赖使其对标准 RL 极为困难。左图显示 AdaBack 在不到 700 次迭代内训练奖励接近 1.0，同时监督比例 $\rho$ 从约 0.5 逐步下降至接近 0，表明模型从部分监督平滑过渡到完全自主生成。右图则显示 **SFT+RL 的奖励停滞在 0.1**，仅保留了监督预训练中学到的输出格式，未能习得推理能力。这一对照实验构成 AdaBack 有效性的最强证据：当 SFT、RL 及其组合均失败时，自适应回溯是唯一成功的方法。

### 消融实验与鲁棒性分析

**奖励阈值 $\tau$ 的鲁棒性**：**Figure 5** 展示了 $\tau \in \{0.1, \dots, 0.9\}$ 下的训练奖励和测试准确率。尽管高阈值（0.8、0.9）在训练初期表现略低，但随着训练推进，所有阈值的曲线趋于一致。**Figure 6** 进一步显示，高阈值初始时平均揭示比例更高（约 0.5），但最终所有设置收敛到相似的监督水平。这表明 AdaBack 的课程调度对 $\tau$ 具有高度鲁棒性，无需精细调参。

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/007_Figure_5.jpg]]
*Figure 5: Training reward (left) and test accuracy (right) across different AdaBack reward thresholds. Although there is some difference at the begining of training for high thresholds ( $\tau$ = 0 . 8 and $\tau$ = 0 . 9 ) , the learning curves and performance become indistinguishable as training goes on

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_wdbgTG5kib/figures/008_Figure_6.jpg]]
*Figure 6: Dynamics of the average revealed portion for different reward thresholds. High thresholds such as $\tau$ = 0 . 8 and $\tau$ = 0 . 9 result in a larger average revealed portion in the initial part of training. Nonetheless, as training continues, all thresholds converge to stable supervision levels. Combined with Figure 5, this suggests AdaBack’s curriculum adapts similarly across a wide range of thresholds

**零监督注入**：以 10% 概率直接设置 $\rho=0$ 有利于减小训练-测试分布差异并加速收敛（Section C），该设计确保模型不会过度依赖前缀提示。

**自适应机制的必要性**：移除自适应机制（固定 $\rho=0$ 或固定全局步长）会导致困难任务上训练失败或效率骤降。R3 在链式奇偶校验上需 16,000+ 次迭代的对比已充分说明非自适应策略的局限。

### 失败模式与局限性

1. **预训练饱和效应**：对于指令微调模型或在预训练中已大量接触任务分布的模型，AdaBack 无法提供额外帮助。**Figure 10** 显示 Llama 3.2 3B-Instruct 在 MATH 上训练和测试奖励迅速饱和，几乎所有问题在数百次迭代内即被解决，AdaBack 无探索空间。**Figure 11** 中 Qwen2.5-1.5B 在 GSM8k 上同样出现快速饱和现象。

2. **大规模数据集的逐样本适应衰减**：当数据集非常大时，多数样本被访问次数少，当前实现主要依赖全局指数移动平均 $\bar{\rho}_{\min} \leftarrow \alpha \rho_{\min}^{(i)} + (1-\alpha) \cdot \bar{\rho}_{\min}$ 来初始化监督比例，可能削弱逐样本自适应效果。

3. **结构化步骤场景的相对劣势**：当推理步骤可通过明确分隔符（如 GSM8k 中的换行）清晰分割时，AdaBack 的随机位置揭示策略不如 R3 的按步骤切片高效。

4. **对可验证奖励的依赖**：AdaBack 依赖可自动判断正确性的最终答案奖励信号，适用于数学等领域；对于奖励难以定义或极其稀疏的任务，方法可能失效。

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

长序列推理任务中，标准强化学习面临一个根本性困难：**奖励稀疏**。若推理链由 $n$ 步组成、每步成功概率为 $p$，则获得正奖励的概率仅为 $p^n$，期望迭代次数为 $p^{-n}$，随序列长度呈指数衰减。这意味着模型在随机探索阶段几乎无法获得任何有效奖励信号，训练无法启动。监督微调（SFT）揭示完整目标序列（$\rho=1$），虽能提供密集信号，但模型仅学会模仿而非探索，在分布外任务上泛化能力有限。SFT+RL 的组合亦无法解决此问题——一旦 RL 阶段要求模型从零生成完整答案，奖励稀疏的困境依然存在。

AdaBack 的核心洞察在于：**通过自适应揭示目标输出的部分前缀，将原本的长序列稀疏奖励问题分解为一系列较短的子任务**。每个子任务只需补全剩余部分，成功概率大幅提升，从而在训练初期就能获得有效奖励。随着模型能力增长，揭示比例 $\rho$ 逐步降低，实现从监督到无监督的平滑过渡。

### 与基线方法的关系

**标准 RL（GRPO）**（Shao et al., 2024）要求模型从头生成完整答案（$\rho=0$），在困难任务上因奖励稀疏而无法学习。AdaBack 通过引入可变前缀揭示，在训练初期提供“脚手架”，使模型能够逐步积累能力。在合成链式奇偶校验任务上，标准 RL 的训练奖励始终停滞在 0.1 附近（仅保留格式奖励），而 AdaBack 在不到 700 次迭代内即达到接近完美的奖励（Figure 2）。

**SFT+GRPO** 先进行完整监督微调再进行 RL，虽在标准 GSM8k 上表现尚可，但在分布外设置（如 Tensor-2 GSM8k）上显著劣于 AdaBack。Table 1 显示，1B 模型在 Tensor-2 GSM8k 上，SFT+RL 仅达 6.9，而 AdaBack 达 8.5；Base+RL 则为 0.0，完全失败。这表明 SFT 提供的初始能力不足以应对严重的分布偏移，而 AdaBack 的渐进式课程学习能够有效扩展可学习任务的范围。

**R3**（Xi et al., 2024）采用固定步长的切片课程学习：将示范文本按分隔符（如换行）切分为片段，混合训练。R3 本质上是静态数据增强，缺乏逐样本自适应能力。AdaBack 与 R3 的关键区别在于：
- **粒度**：R3 依赖预定义的步骤边界（如 GSM8k 中的换行），AdaBack 可在任意位置揭示前缀，无需任何分割超参数。
- **自适应性**：R3 对所有样本使用统一的全局课程，而 AdaBack 为每个样本维护独立的监督比例区间 $[\rho_{\min}^{(i)}, \rho_{\max}^{(i)}]$，根据该样本的奖励反馈动态调整。

在合成链式奇偶校验任务上，R3 需要超过 16000 次迭代才达到 0.8 奖励，而 AdaBack 仅需不到 700 次（Figure 2）。在数学推理基准上，AdaBack 在 DeepScaleR 上显著优于 R3（1B: 9.0 vs 6.6; 3B: 10.6 vs 9.6），在 MATH 1B 上亦有优势（9.1 vs 7.8），但在 GSM8k 上略低于 R3（Table 2）。GSM8k 上的劣势可能与 R3 利用换行符进行精确步骤切分有关——当推理步骤可被清晰分割时，按步骤切片的课程方法可能比随机位置揭示前缀更高效。

**Base+RL** 从预训练基模型直接进行 RL，不经 SFT。AdaBack 在此设置下表现尤为突出：在 3B 基模型上，MATH 准确率从 Base+RL 的 15.0 提升至 19.1（Table 1）。更重要的是，Figure 4 显示 AdaBack 在基模型上显著提升了 pass@k，表明其扩展了模型的解空间，而非仅仅重新加权已有的答案分布。

### 适用边界与局限

1. **预训练饱和效应**：对于指令微调模型或在预训练中已大量接触任务分布的模型，训练奖励会迅速饱和，AdaBack 无法提供额外帮助。Figure 10 显示 Llama 3.2 3B-Instruct 在 MATH 上几乎无学习动态，Figure 11 显示 Qwen2.5-1.5B 在 GSM8k 上同样快速饱和。在这些场景下，模型已基本“解决”了任务，缺乏探索空间。

2. **大规模数据集的逐样本适应退化**：当数据集非常大时，多数样本被访问次数少，当前实现主要依赖全局指数移动平均 $\bar{\rho}_{\min} \leftarrow \alpha \rho_{\min}^{(i)} + (1-\alpha) \cdot \bar{\rho}_{\min}$ 来初始化新样本的监督比例，可能削弱逐样本自适应效果。

3. **奖励信号依赖**：AdaBack 依赖可验证的最终答案奖励信号，适用于数学等可自动判断正确性的领域。对于奖励难以定义或极其稀疏的任务，方法可能失效。

4. **步骤结构敏感性**：当推理步骤可被清晰分割时（如 GSM8k 中的换行），AdaBack 采用的随机位置揭示前缀可能不如按步骤切片的课程方法（如 R3）高效。

### 开放问题

1. **更长推理链的扩展性**：在数学奥林匹克等更长推理链任务上，AdaBack 是否能更显著地优于现有方法？如何获取足够的高质量数据？

2. **嵌入空间中的区域调度**：是否可以将监督调度从逐样本扩展到嵌入空间中的区域，例如基于 $k$ 近邻的平均监督水平，以更好地适应大规模数据集？

3. **与过程级反馈的结合**：如何将 AdaBack 与过程级奖励（process-based reward）结合，在保持探索效率的同时提升中间推理步骤的质量？

4. **理论收敛保证**：AdaBack 使用的随机二分搜索策略是否有理论收敛保证？如何根据任务特性最优地设定初始 $\rho$ 区间和阈值 $\tau$？实验表明 $\tau \in [0.1, 0.9]$ 范围内最终性能趋于一致（Figure 5），但训练初期的动态存在差异（Figure 6），高阈值导致初期揭示比例更大。

5. **无明确步骤结构任务的适应**：对于无明确步骤结构或需要多跳推理的任务，自适应揭示策略能否自动发现有效的子任务分解？

## 原文 PDF

![[paperPDFs/ICLR_2026/RL_for_Reasoning_by_Adaptively_Revealing_Rationales.pdf]]
