---
title: "Conditional Advantage Estimation for Reinforcement Learning in Large Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Conditional_Advantage_Estimation_for_Reinforcement_Learning_in_Large_Reasoning_Models.pdf
openreview_forum_id: CTEXdHB1BB
aliases:
- CCAE
- CAERLLRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "条件重组与组间/组内优势计算的结合。调节μ（组间 vs 组内权重）和α（组间权重）可控制模型对指标趋势的响应，进而影响探索程度与推理效率。"
primary_logic: "按指标值将采样响应等分为两组，跨组比较揭示指标趋势带来的性能差异，组内比较在相同趋势下优选出更好响应，从而在不预设指标方向偏好的前提下，选择性放大特定指标的影响，以指导有利行为的习得。"
claims:
- "在数学推理任务上，基于熵的CANON-Inter相比DR.GRPO平均提升1.9个百分点的准确率，并在AIME24上提升5.0个百分点。"
- "在复杂逻辑推理任务中，基于熵的CANON-Intra相比DR.GRPO提升2.9个百分点准确率，并缩短36.6%的回答长度，在最困难子集上增益高达5.2个百分点。"
- "CANON-Eff（α=0.96）在几乎不损失性能（-0.4分）的情况下，将令牌消耗降低26.3%；α=0.88在低令牌预算场景下性能是DR.GRPO的2.63倍，或在相同性能下减少45.5%的令牌消耗。"
- "定理1证明：当两组大小相等时，组间优势相比DR.GRPO能提供更清晰的信号。"
---

# Conditional Advantage Estimation for Reinforcement Learning in Large Reasoning Models

> [!tip] 核心洞察
> 按指标值将采样响应等分为两组，跨组比较揭示指标趋势带来的性能差异，组内比较在相同趋势下优选出更好响应，从而在不预设指标方向偏好的前提下，选择性放大特定指标的影响，以指导有利行为的习得。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大型推理模型中强化学习的条件优势估计 |
| 英文题名 | Conditional Advantage Estimation for Reinforcement Learning in Large Reasoning Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CTEXdHB1BB); [GitHub](https://github.com/biuboomc/CANON) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | CANON (Conditional advANtage estimatiON) |
| Dataset | AIME 24, Math Reasoning (Avg), High Complexity Reasoning (Avg), Math Reasoning (Token Cost) |

> [!tip] 效果简介
> - AIME 24 上，Accuracy 为 32.7，对比 27.7，变化 +5.0。
> - Math Reasoning (Avg) 上，Accuracy 为 57.6，对比 55.7，变化 +1.9。
> - High Complexity Reasoning (Avg) 上，Accuracy 为 29.5，对比 26.2，变化 +3.3。

## 概述

**问题瓶颈**：基于群组的优势估计方法（如 **DR.GRPO**，Liu et al., 2025a）在比较目标上存在模糊性——其优势信号混合了多种因素，无法有效放大特定训练指标（如生成熵、响应长度）对模型行为的积极影响。直接通过奖励塑形引入先验则容易导致过度偏差，需要精心调参。

**核心方法**：本文提出 **CANON（Conditional advANtage estimatiON）**，一种条件优势估计方法。其核心思路是：按目标指标值将采样响应等分为两组，通过**跨组比较**揭示指标趋势带来的性能差异，通过**组内比较**在相同趋势下优选出更好响应，从而在不预设指标方向偏好的前提下，选择性放大特定指标对模型行为的引导。

**方法定位**：CANON 属于群组相对优势估计方法的改进，其统一优势公式为 $\hat{A}^{\mathrm{CANON}} = \mu \hat{A}^{\mathrm{inter}} + (1-\mu) \hat{A}^{\mathrm{intra}}$。当两组大小相等且 $\mu=0.5$ 时，CANON 退化为 DR.GRPO，即 DR.GRPO 是 CANON 的一个特例。通过调节 $\mu$（组间 vs 组内权重）和 $\alpha$（组间权重），可控制模型对指标趋势的响应程度，进而影响探索与推理效率。

**主要结果**：
- **准确率提升**：基于熵的 CANON-Inter 在数学推理任务上相比 DR.GRPO 平均提升 **1.9 个百分点**，在 AIME24 上提升 **5.0 个百分点**；基于长度的 CANON-Intra 在复杂逻辑推理任务上提升 **2.9 个百分点**，同时缩短 **36.6%** 的回答长度。
- **效率增益**：CANON-Eff（$\alpha=0.96$）在几乎不损失性能（-0.4 分）的情况下，将令牌消耗降低 **26.3%**；$\alpha=0.88$ 在低令牌预算场景下性能是 DR.GRPO 的 **2.63 倍**，或在同等性能下减少 **45.5%** 的令牌消耗。
- **动态调度**：采用“先组间后组内”的调度策略，在多个模型和任务上一致优于 DR.GRPO。

> **注意**：本文实验仅基于 Qwen 和 Llama 系列模型，在数学与逻辑推理任务上验证，对其他架构和任务类型的泛化性尚待确认。

## 背景与动机

### 问题背景

大型语言模型（LLM）在数学推理、代码生成等复杂任务上的突破，很大程度上得益于强化学习（RL）的引入。在RL训练中，优势估计（advantage estimation）是策略梯度方法的核心组件，它决定了模型如何评判当前生成响应相对于期望水平的优劣，进而影响策略更新的方向和幅度。早期的优势估计方法，如PPO，需要训练一个与策略模型等大的价值网络，计算开销巨大。为此，研究者提出了多种无需价值网络的方法，例如**GRPO**（Shao et al., 2024）、**RLOO**（Ahmadian et al., 2024）、**ReMax**（Li et al., 2023）和**REINFORCE++**（Hu, 2025），其中GRPO通过在同一问题下采样一组响应，以组内平均奖励作为基线来计算优势，显著降低了计算成本。

**DR.GRPO**（Liu et al., 2025a）进一步简化了GRPO，去除了优势标准化步骤，成为当前主流的高效优势估计方法。然而，DR.GRPO将同一问题下的所有采样响应视为一个整体，其优势计算仅反映了单个响应相对于组内平均水平的相对好坏，并未考虑响应在特定指标（如生成熵、响应长度）上的差异如何影响最终性能。

### 现有方法缺口

当前基于群组的优势估计方法存在一个关键瓶颈：**比较目标的模糊性**。DR.GRPO将高奖励响应和低奖励响应混合在一起计算平均基线，导致优势信号中混杂了多种因素的共同影响。具体而言：

1. **无法选择性放大特定指标的影响**：在推理任务中，生成熵（反映模型探索程度）和响应长度（反映推理深度）与最终性能存在复杂关联。例如，较高的生成熵可能意味着模型正在尝试更多样的推理路径，但也可能引入噪声；较长的响应可能包含更详尽的推理步骤，但也可能是冗余的。DR.GRPO无法针对性地放大或抑制这些指标对模型行为的引导作用。

2. **直接奖励塑形引入过度偏差**：另一种思路是通过修改奖励函数来鼓励或惩罚特定行为（如长度惩罚、熵奖励），例如**Entropy Adv**（Cheng et al., 2025）和**Clip-Cov**（Cui et al., 2025）。然而，这种方法容易引入过度偏差，需要精心调参以平衡任务性能与辅助目标，且往往在域外泛化时表现脆弱。

### 核心动机

本文的核心动机源自一个关键洞察：**通过按特定指标值对采样响应进行条件分组，可以揭示该指标趋势带来的性能差异，从而在不预设指标方向偏好的前提下，选择性放大其影响**。

具体而言，将同一问题下的采样响应按目标指标（如熵、长度）的值等分为两组——高指标组和低指标组——然后进行跨组比较，可以直接量化“指标高低”这一因素对奖励的贡献。同时，在组内进行比较，可以在相同指标趋势下优选出更好的响应。这种“条件重组—分组比较”的范式，使得优势估计能够精确地分离并放大特定指标的影响，而不会干扰其他因素的信号传递。

基于上述动机，本文提出**CANON（Conditional advANtage estimatiON）**，通过条件重组与组间/组内优势计算的结合，为强化学习训练提供了更精细、更可控的优势估计框架。

## 核心创新

CANON 的核心创新在于将**条件重组（Conditional Regrouping）** 引入优势估计，解决了现有基于群组的优势估计方法（如 DR.GRPO）在比较目标上的模糊性问题。

### 1. 从无差别比较到条件化对比

在 DR.GRPO 等基线方法中，优势估计仅基于响应奖励与全组平均奖励的差值（$R_o - \text{mean}(\{R_{o'} | o' \in G_q\})$），无法区分奖励差异究竟源于何种行为特征。CANON 的关键改变在于：

- **条件重组（Changed Slot 1）**：将采样响应按特定指标（如熵、响应长度）的值排序，等分为两组（高指标组 $G_q^+$ 和低指标组 $G_q^-$），使组间比较能够捕捉该指标趋势带来的性能差异。
- **组间优势（Inter-group Advantage）**：响应奖励减去异组平均奖励，公式为：

$$
\hat{A}_{q,o,t}^{\mathrm{inter}} = \begin{cases} R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^- \\ R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^+ \end{cases}
$$

- **组内优势（Intra-group Advantage）**：响应奖励减去本组平均奖励，在相同指标趋势下优选出更好响应：

$$
\hat{A}_{q,o,t}^{\mathrm{intra}} = \begin{cases} R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^+ \\ R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^- \end{cases}
$$

### 2. 统一优势组合框架（Changed Slot 2 & 3）

CANON 通过可调参数 $\mu$ 将组间与组内优势进行加权组合：

$$
\hat{A}_{q,o,t}^{\mathrm{CANON}} = \mu \hat{A}_{q,o,t}^{\mathrm{inter}} + (1 - \mu) \hat{A}_{q,o,t}^{\mathrm{intra}}
$$

这一公式揭示了一个重要事实：**DR.GRPO 是 CANON 在 $\mu=0.5$ 且两组大小相等时的特例**（定理 1，Eq. 7）。CANON 通过调节 $\mu$ 打破了 DR.GRPO 的固定等权混合，使模型能够灵活控制对指标趋势的响应程度：
- $\mu \to 1$（CANON-Inter）：强化组间比较，放大指标趋势的影响；
- $\mu \to 0$（CANON-Intra）：聚焦组内择优，弱化指标趋势的引导。

### 3. 加权组间优势实现高效推理（Changed Slot 4）

为进一步控制推理效率，CANON-Eff 在组间优势中引入权重 $\alpha$，对长响应组施加温和惩罚：

$$
\hat{A}_{q,o,t,\alpha}^{\mathrm{inter}} = \begin{cases} R_o - \alpha * \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^- \\ \alpha * R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^+ \end{cases}
$$

通过调节 $\alpha$，可在几乎不损失性能的前提下大幅降低令牌消耗（$\alpha=0.96$ 时性能仅降 0.4 分，令牌减少 26.3%）。

### 4. 选择性放大机制的理论保证

CANON 的核心洞察在于：**基于某一指标（如熵）进行条件分组后，组间优势仅放大该指标可归因的优势部分，不会放大其他独立因素（如响应长度）的影响**。这避免了直接奖励塑形（如 Numerical Scaling Entropy Adv）引入的过度偏差——后者虽能提升域内数学性能，却严重损害域外逻辑推理能力（18.5 vs 26.2，Table 4）。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/001_Figure_1.jpg]]
*Figure 1: Overview of CANON. CANON regroups all the sampled responses based on the value of a specific metric, and computes the advantages through inter-group and intra-group comparison*

CANON（Conditional advANtage estimatiON）的核心流程围绕一个关键操作展开：**条件重组（Conditional Regrouping）**，并在此基础上构建两种互补的优势估计信号，最终通过一个可控的混合系数统一起来。其整体 pipeline 由以下模块串联而成：

1. **采样与奖励获取**：对于每个输入问题 $q$，策略模型采样一组 $N$ 条响应 $\{o_1, \dots, o_N\}$，并由奖励函数给出每条响应的标量奖励 $R_o$。
2. **条件重组**：选取一个目标指标（如生成熵、响应长度），将所有 $N$ 条响应按该指标值排序后等分为两组——高指标组 $G_q^+$ 和低指标组 $G_q^-$。
3. **组间优势计算**：跨组比较——每条响应的奖励减去**异组**的平均奖励，用于捕捉指标趋势（高 vs 低）带来的系统性性能差异。
4. **组内优势计算**：组内比较——每条响应的奖励减去**本组**的平均奖励，用于在相同指标趋势下优选出相对更好的响应。
5. **统一优势组合**：通过混合系数 $\mu \in [0,1]$ 将组间优势与组内优势加权求和，形成最终的优势估计 $\hat{A}^{\mathrm{CANON}}$。
6. **策略更新**：将 $\hat{A}^{\mathrm{CANON}}$ 代入标准的 PPO/GRPO 目标函数中进行梯度更新。

该框架的关键设计在于：**CANON 仅放大由分组指标所贡献的优势成分，而不会放大其他无关因素的影响**。定理证明表明，当两组大小相等时，组间优势相比 DR.GRPO 能提供更清晰的信号；且 DR.GRPO 恰是 CANON 在 $\mu=0.5$ 且分组大小相等时的特例。

### 输入输出流

- **输入**：问题 $q$、一组采样响应及其奖励 $\{o, R_o\}$、目标指标值（如熵或长度）。
- **输出**：每条响应的优势估计 $\hat{A}^{\mathrm{CANON}}_{q,o,t}$，直接用于策略梯度更新。

### 两个关键调控旋钮

- **$\mu$（组间 vs 组内权重）**：控制模型对指标趋势的响应强度。$\mu \to 1$ 时强调组间信号，推动模型向指标更优的方向偏移；$\mu \to 0$ 时强调组内信号，在保持指标趋势不变的前提下优化响应质量。
- **$\alpha$（组间权重，用于 CANON-Eff）**：在组间优势中引入不对称权重，温和地偏向短响应，实现在几乎不损失性能的前提下大幅降低令牌消耗。

### 方法定位

与现有基于群组的优势估计方法（如 GRPO、DR.GRPO）相比，CANON 的增量在于**将无差别的群组比较拆解为条件化的跨组与组内比较**，从而能够针对特定指标（熵、长度等）进行选择性行为引导，避免了直接奖励塑形带来的过度偏差和繁琐调参。

## 核心模块与公式推导

### 瓶颈与核心调控机制

现有基于群组的优势估计方法（如DR.GRPO）在比较目标上存在模糊性：它无法有效放大特定训练指标（如熵、响应长度）对模型行为的积极影响。而直接通过奖励塑形引入先验则易导致过度偏差，需精心调参。CANON的核心调控机制在于**条件重组与组间/组内优势计算的结合**：调节混合系数μ（组间 vs 组内权重）和加权系数α（组间权重）可控制模型对指标趋势的响应，进而影响探索程度与推理效率。

### 关键模块：条件重组

CANON将每个查询q的采样响应按目标指标值排序，并等分为两组：
- **高指标组** $G_q^+$：指标值较高的响应
- **低指标组** $G_q^-$：指标值较低的响应

这种分组方式使得跨组比较能够揭示“指标趋势带来的性能差异”，而组内比较则在相同趋势下优选出更好响应。分组指标可以是训练过程中的任何连续度量，如生成熵、响应长度等。

### 核心公式：组间优势与组内优势

**组间优势**（Inter-group Advantage）将响应与其**异组**的平均奖励进行比较：

$$
\hat{A}_{q,o,t}^{\mathrm{inter}} = \begin{cases} R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^- \\ R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^+ \end{cases}
$$

**组内优势**（Intra-group Advantage）将响应与其**同组**的平均奖励进行比较：

$$
\hat{A}_{q,o,t}^{\mathrm{intra}} = \begin{cases} R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^+ \\ R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^- \end{cases}
$$

其中 $R_o$ 为响应o的奖励，$\mathrm{mean}(\cdot)$ 为组内奖励均值。

### 统一优势组合

CANON通过混合系数 $\mu \in [0,1]$ 将两类优势加权组合：

$$
\hat{A}_{q,o,t}^{\mathrm{CANON}} = \mu \hat{A}_{q,o,t}^{\mathrm{inter}} + (1 - \mu) \hat{A}_{q,o,t}^{\mathrm{intra}}
$$

- 当 $\mu=1.0$ 时，仅使用组间优势（CANON-Inter）
- 当 $\mu=0.0$ 时，仅使用组内优势（CANON-Intra）
- 当 $\mu=0.5$ 且两组大小相等时，CANON退化为DR.GRPO

### DR.GRPO的特例关系

DR.GRPO可表示为组间与组内优势的等权组合：

$$
\hat{A}_{q,o,t}^{\mathrm{DR.GRPO}} = R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q\}) = \frac{1}{2} \hat{A}_{q,o,t}^{\mathrm{inter}} + \frac{1}{2} \hat{A}_{q,o,t}^{\mathrm{intra}}
$$

这等价于CANON在 $\mu=0.5$ 且分组大小相等时的特例（Eq. 7）。

### 加权组间优势（CANON-Eff）

为温和地偏向短响应以实现高效推理，CANON-Eff在组间优势中引入权重 $\alpha$：

$$
\hat{A}_{q,o,t,\alpha}^{\mathrm{inter}} = \begin{cases} R_o - \alpha * \mathrm{mean}(\{R_{o'} | o' \in G_q^+\}), & \text{if } o \in G_q^- \\ \alpha * R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q^-\}), & \text{if } o \in G_q^+ \end{cases}
$$

其中 $\alpha$ 控制对长响应组的惩罚程度。当 $\alpha=1.0$ 时退化为标准组间优势；$\alpha<1.0$ 时对高指标组施加更强的抑制，从而降低令牌消耗。

### 选择性放大原理

CANON的核心洞察在于：基于某一条件（如熵）进行分组时，它仅放大与该条件相关的优势信号，**不会放大其他独立条件的影响**。定理1证明，当两组大小相等时，组间优势相比DR.GRPO能提供更清晰的信号（Theorem 1, Eq. 6）。这意味着CANON可以在不预设指标方向偏好的前提下，选择性放大特定指标的影响，以指导有利行为的习得。

## 实验与分析

### 核心瓶颈与因果机制

现有基于群组的优势估计方法（如DR.GRPO）在比较目标上存在模糊性——它平等地混合组间与组内比较信号，无法有效放大特定训练指标（如熵、响应长度）对模型行为的积极影响。直接通过奖励塑形引入先验则容易导致过度偏差，需要精心调参。

CANON通过**条件重组**这一因果旋钮解决了上述问题：将采样响应按目标指标值等分为两组，跨组比较揭示指标趋势带来的性能差异，组内比较在相同趋势下优选出更好响应。调节混合系数μ（组间vs组内权重）和组间权重α，可精确控制模型对指标趋势的响应，进而影响探索程度与推理效率。

### 主要实验结果

**数学推理任务。** Table 1展示了Qwen2.5-Math-7B上的完整结果。基于熵的CANON-Inter（μ=1.0）在六个数学基准上平均准确率达57.6%，相比DR.GRPO的55.7%提升1.9个百分点，其中AIME 24上提升最为显著（32.7 vs 27.7，+5.0个百分点）。基于长度的CANON-Inter在保持相近准确率的同时，将令牌消耗从1522降至1008（-33.8%）。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/002_Table_1.jpg]]
*Table 1: Overall performance based on Qwen2.5-Math-7B. We compare with the following baselines: (1) Qwen2.5-Math-7B-Instruct (Qwen-Instruct), (2) prior advantage estimation methods. All models are evaluated under a unified setting. Bold and underline indicate the best and second-best results, respectively*

**复杂逻辑推理任务。** 基于熵的CANON-Intra（μ=0.0）相比DR.GRPO提升2.9个百分点准确率（29.5 vs 26.2），同时缩短36.6%的回答长度。在最困难子集（XLarge）上，增益高达5.2个百分点。这表明完全关闭跨组比较、仅保留组内优选，对域外泛化场景更为有利。

**动态调度策略。** Table 2展示了CANON-Dynamic在三个模型上的表现。采用“First-Inter-Later-Intra”调度策略（训练前期μ=1.0，后期切换为μ=0.0），在Qwen2.5-Math-7B上数学推理准确率达57.0%，复杂推理达29.2%，均优于DR.GRPO（55.7和26.2）。该策略在Qwen2.5-Math-1.5B和Llama3.1-8B上也一致优于DR.GRPO，验证了跨模型泛化性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/009_Table_2.jpg]]
*Table 2: Overall performance of CANON-Dynamic across three different models and two tasks. All models are evaluated under a unified setting. Bold and underline indicate the best and second-best results, respectively*

**高效推理。** Table 3和Figure 4展示了CANON-Eff在效率-性能权衡上的优势。当α=0.96时，CANON-Eff在几乎不损失性能（-0.4分）的情况下，将令牌消耗从1115降至822（-26.3%）。在低令牌预算场景下，α=0.88的CANON-Eff性能是DR.GRPO的2.63倍，或在相同性能水平下减少45.5%的令牌消耗。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/011_Table_3.jpg]]
*Table 3: The comparison between different methods towards efficient reasoning. Bold and underline indicate the best and second-best results, respectively. The detailed performance is from the topperforming models for each method, specifically α=0.96 for CANON-Eff. We include CANON-Eff with $\alpha$ = 0 . 8 8 , which has comparable performance with the baseline Length Reward (*)*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/014_Figure_4.jpg]]
*Figure 4: (a) $\mathtt { C A N O N - E f f }$ with $\alpha$ = 0 . 9 6 $\mathrm { c o n - }$ (b) $\mathtt { C A N O N - E f f }$ with $\alpha$ ~ = ~ 0 . 8 8 (c) The Pareto frontier in the tradesistently outperforms baselines meth- achieves significantly better perfor- off between performance and toods. mance at low token budgets. ken efficiency. Figure 4: Budget-Performance and Cost-Performance Curves for Efficient Reasoning. This figure compares the reasoning efficiency of CANON-Eff against baselines under various token budgets

### 消融实验

**μ值的调控效应。** Table 10显示，随着μ从0增至1，域内数学性能逐步提升（54.2→57.9），但域外逻辑性能持续下降（27.1→22.5），熵从2.40急剧降至0.15。这证实μ是控制探索-利用平衡的有效杠杆：高μ放大低熵偏好，有利于域内精度但损害域外泛化。

**α值的平滑调节。** Table 11表明，α从0.96降至0.5时，性能平缓下降（56.2→44.5）但令牌消耗大幅降低（822.4→198.9）。这种平滑性使α成为控制推理效率的精细旋钮，优于离散的长度惩罚机制。

**指标选择的重要性。** Table 12对比了随机重分组、基于长度和基于熵的条件重组。随机重分组无法提升性能或效率，仅与基线持平；基于长度或熵的分组各自带来效率或准确率的明显增益，验证了条件重组的必要性。

**直接缩放优势的失败模式。** Table 4显示，直接数值放大优势（Numerical Scaling Entropy Adv）虽能提升数学性能，但严重损害逻辑推理性能（18.5 vs CANON-Intra的29.1）。这证明了CANON选择性放大机制的关键优势：它仅放大归因于分组指标的信号，不引入对其他因素的偏差。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_CTEXdHB1BB/figures/017_Table_4.jpg]]
*Table 4: The performance comparison between the direct numerical amplification of advantage and CANON*

### 理论支撑

定理1证明，当两组大小相等时，组间优势相比DR.GRPO能提供更清晰的信号。DR.GRPO被证明是CANON在μ=0.5且分组大小相等时的特例（Eq. 7），这为CANON提供了严格的理论基础。

### 实验公平性说明

所有模型在统一设定下评估：温度0.6，最大回答长度、令牌预算等保持一致。CANON与DR.GRPO等基线使用相同的训练数据、rollout设置（每组16条响应）、奖励函数和clip-higher策略，排除了无关因素干扰。

### 局限性与待验证问题

实验仅基于Qwen和Llama系列模型，对其他架构的泛化性未经验证。动态调度策略需要根据模型能力和训练数据集特点进行定制，缺乏统一的自动调度方法。目前仅在数学和逻辑推理任务上评估，在代码、长文本生成等任务上的效果未知。论文主要关注二元指标和连续度量（熵、长度），对多分类或更复杂的奖励信号未作深入探讨。

## 方法谱系与知识库定位

### 与基线方法的关系

CANON 直接建立在群组相对优势估计的框架之上，其最直接的参照系是 **DR.GRPO**（Liu et al., 2025a）和 **GRPO**（Shao et al., 2024）。论文通过理论推导证明，DR.GRPO 是 CANON 在两组大小相等且 μ = 0.5 时的特例：

$$\hat{A}_{q,o,t}^{\mathrm{DR.GRPO}} = R_o - \mathrm{mean}(\{R_{o'} | o' \in G_q\}) = \frac{1}{2} \hat{A}_{q,o,t}^{\mathrm{inter}} + \frac{1}{2} \hat{A}_{q,o,t}^{\mathrm{intra}}$$

这一等价关系揭示了 DR.GRPO 在比较目标上的模糊性——它等权重地混合了跨组和组内信号，无法针对性地放大特定训练指标（如熵、响应长度）对模型行为的积极影响。CANON 通过引入条件重组与可调节的 μ 系数，将这种隐式混合显式化、可控化，从而解决了 DR.GRPO 的核心瓶颈。

在更广泛的优势估计谱系中，CANON 与 **RLOO**（Ahmadian et al., 2024）、**ReMax**（Li et al., 2023）、**REINFORCE++**（Hu, 2025）等方法处于同一问题域，但 CANON 的独特贡献在于将指标条件引入优势计算，而非仅依赖奖励信号的统计特性。与直接通过奖励塑形引入先验的方法（如 **Entropy Adv**（Cheng et al., 2025）和 **Clip-Cov**（Cui et al., 2025））相比，CANON 避免了过度偏差和精心调参的需求——消融实验（Table 4）表明，直接数值缩放优势值（Numerical Scaling Entropy Adv）虽能提升数学性能，但会严重损害域外逻辑推理性能（18.5 vs 26.2），而 CANON-Intra 在逻辑推理上表现最佳（29.1）。

### 核心机制的因果可解释性

CANON 的因果调控能力体现在两个可调节的“旋钮”上：

- **μ（组间 vs 组内权重）**：控制模型对指标趋势的响应强度。当 μ 增大，组间优势主导，模型被推向更极端的指标方向（如更低的熵、更短的响应）；当 μ 减小，组内优势主导，模型在相同指标趋势内优选更好响应。消融实验（Table 10）显示，μ 从 0 增至 1 时，域内数学性能逐步提升（54.2 → 57.9），但域外逻辑性能下降（27.1 → 22.5），熵持续降低（2.40 → 0.15），验证了 μ 对探索-利用权衡的调控作用。

- **α（组间权重）**：在 CANON-Eff 中引入，用于温和地偏向短响应。α 从 0.96 降至 0.5 时，性能平缓下降（56.2 → 44.5），但令牌消耗大幅降低（822.4 → 198.9），表明 α 提供了平滑的效率-性能权衡曲线，优于硬性长度截断。

定理 1 进一步从理论上证明：当两组大小相等时，组间优势相比 DR.GRPO 能提供更清晰的信号，因为它将指标差异导致的性能差异从组内噪声中分离出来。随机重分组的消融实验（Table 12）也证实，仅条件重组本身不足以带来增益——基于长度或熵的分组各自带来效率或准确率的明显增益，而随机分组仅与基线持平。

### 适用边界与局限

1. **模型架构泛化性未验证**：实验仅基于 Qwen2.5-Math（7B/1.5B）和 Llama3.1-8B 系列模型，对其他架构（如 Gemma、DeepSeek 等）的泛化性缺乏证据，需手动验证。

2. **任务范围受限**：目前仅在数学推理（AIME、MATH-500 等）和复杂逻辑推理任务上评估，在代码生成、长文本生成等任务上的效果未知。

3. **动态调度依赖人工设计**：CANON-Dynamic 的“First-Inter-Later-Intra”调度策略虽在三个模型和两类任务上一致优于 DR.GRPO（Table 2），但调度函数需根据模型能力和训练数据集特点定制，缺乏统一的自动调度方法。

4. **奖励信号假设简单**：论文主要关注二元指标（如二元奖励）和连续度量（熵、长度），对多分类奖励或更复杂的奖励结构未作深入探讨。

5. **分组策略的敏感性**：CANON 假设两组大小相等，当采样响应数量较少或指标分布极度偏斜时，分组效果可能退化，但论文未对此进行消融。

### 开放问题

- CANON 的条件分组思想能否扩展到其他指标（如生成多样性、多步推理步骤数、自我修正频率）？
- 能否设计自适应机制，根据训练动态自动调整 μ，而无需人工设定调度函数？
- CANON-Eff 的 α 调节与基线长度惩罚方法（如重复惩罚、长度归一化奖励）是否存在互补优势？
- 条件分组框架能否集成到其他优势估计方法（如 RLOO、ReMax）中，形成更通用的条件优势估计范式？
- 在更大规模模型（如 70B+）和更复杂任务（如多轮对话、工具调用）上的效果如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Conditional_Advantage_Estimation_for_Reinforcement_Learning_in_Large_Reasoning_Models.pdf]]
