---
title: "Prosperity before Collapse: How Far Can Off-Policy RL Reach with Stale Data on LLMs?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Prosperity_before_Collapse_How_Far_Can_Off_Policy_RL_Reach_with_Stale_Data_on_LLMs.pdf
openreview_forum_id: IIgl5MWelz
aliases:
- PBC
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "Prosperity before Collapse"
primary_logic: "Prosperity before Collapse"
claims:
- "Prosperity before Collapse"
---

# Prosperity before Collapse: How Far Can Off-Policy RL Reach with Stale Data on LLMs?

> [!tip] 核心洞察
> Prosperity before Collapse

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Prosperity before Collapse: How Far Can Off-Policy RL Reach with Stale Data on LLMs? |
| 英文题名 | Prosperity before Collapse: How Far Can Off-Policy RL Reach with Stale Data on LLMs? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IIgl5MWelz); [GitHub](https://github.com/Infini-AI-Lab/M2PO/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

## 概述

大语言模型（LLM）的强化学习训练（如 GRPO）通常要求使用当前策略模型实时生成的样本（on-policy），这导致训练效率受限于生成速度，形成“生成-训练”瓶颈。直接使用陈旧数据（stale data）进行 off-policy 训练会因策略分布偏移导致性能退化，但移除信任域约束后，陈旧数据训练反而展现出“先繁荣后崩溃”（prosperity-before-collapse）的现象——初期性能甚至超越 on-policy 基线，随后急剧恶化。

本文的核心发现是：**陈旧数据中的极端重要性权重离群值（extreme importance weight outliers）是导致训练不稳定的关键瓶颈，而非整体分布偏移本身。** 基于此，作者提出 **M2PO（Second-Moment Trust Policy Optimization）**，通过约束重要性权重的二阶矩（second moment）来选择性屏蔽极端离群值，同时保留大多数信息丰富的更新。

M2PO 的核心优势在于：
- **自适应信任域**：基于批级二阶矩统计量 $\hat{M}_2$ 动态调整信任域，分布偏移大时自动收紧，偏移小时自动放松，无需手工设定裁剪阈值 $\epsilon$。
- **计算高效**：仅需单样本蒙特卡洛估计，不引入额外前向传播开销，损失计算时间仅占总训练时间的 0.19%。
- **极端稳定性**：在陈旧度高达 256 次模型更新的条件下，M2PO 将被裁剪 token 比例从 1.22% 锐减至 0.06%，性能与 on-policy 基线持平。

在 1.7B 至 32B 参数规模的六组模型和八个数学推理基准上，M2PO 在 off-policy 设置（s=256）下平均准确率最高提升 11.2%，且在五组模型中取得最优平均准确率，验证了其在解耦生成与训练、提升 RL 训练吞吐量方面的实用价值。

## 背景与动机

### 大语言模型推理能力的强化学习训练

近年来，强化学习（RL）已成为提升大语言模型（LLM）推理能力的核心技术路径。通过将推理任务建模为策略优化问题，模型在数学、编程等复杂场景中展现出显著的性能跃升。GRPO（Group Relative Policy Optimization）是这一范式中的代表性算法，其核心机制是在同一提示词的多个采样响应之间进行组内奖励归一化，并利用裁剪后的优势加权概率比进行策略更新：

$$A_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{\mathrm{std}(\{R_i\}_{i=1}^G)}$$

这一设计有效消除了奖励尺度漂移的影响，成为当前主流推理模型训练的基础框架。

### 离线训练中的稳定性困境

然而，GRPO 及其变体在**离线（off-policy）训练**场景下面临严峻挑战。在实际部署中，由于推理引擎与训练引擎分离、异步流水线架构等因素，用于训练的数据往往存在显著**陈旧度（staleness）**——即数据由若干步之前的旧模型生成。实验表明，当陈旧度达到 256 步模型更新时，标准 GRPO 的性能出现明显退化（Figure 1 左），而移除信任区域（trust region）的无裁剪训练则呈现出“**先繁荣后崩溃**”（prosperity-before-collapse）现象：初始阶段性能甚至超越在线基线，随后迅速恶化（Figure 3）。

深入分析揭示，陈旧数据的核心问题在于**重要性权重（importance weight）的极端离群值**。当行为策略与当前策略的分布偏移增大时，重要性比率 $r = \pi_\theta / \pi_{\theta_{\text{old}}}$ 的方差急剧膨胀，导致大量 token 被裁剪。在 Qwen-2.5-32B 模型上，陈旧度为 256 时裁剪率从接近零飙升至约 1.22%（Figure 1 右）。这种大规模裁剪不仅丢弃了宝贵的训练信号，更使得策略更新方向偏离最优轨迹。

### 现有方法的缺口

面对离线训练的稳定性问题，现有方案存在明显局限：

- **固定裁剪阈值**：GRPO 采用固定的裁剪范围 $[1-\epsilon, 1+\epsilon]$，无法感知实际的分布偏移程度。当偏移较小时约束过松，偏移较大时又过度裁剪。
- **截断重要性采样（TIS）**：通过截断极端重要性比率来降低方差，但截断阈值的选取仍是手工设定的，缺乏对批次级分布偏移的自适应能力。
- **非对称裁剪**：对正负优势采用不同裁剪阈值可在一定程度上改善性能，但仍未从根本上解决信任区域的自适应调节问题（Figure 11）。

这些方法的共同缺陷在于：**信任区域的确定与实际的分布偏移程度脱节**。一个理想的信任区域机制应当能够感知每个训练批次的偏移程度，在偏移大时自动收紧约束，偏移小时自动放松约束。

### 本文动机

基于上述分析，本文提出核心问题：**能否设计一种自适应、方差敏感的信任区域机制，既能抑制极端离群值对训练的破坏，又能保留绝大多数信息丰富的更新信号？**

这一动机直接导向 M2PO（Second-Moment Trust Policy Optimization）的设计：利用重要性权重的二阶矩统计量 $M_2$ 作为分布偏移的实时度量，在批次层面动态确定信任区域。$M_2$ 兼具方差敏感性（能捕获高熵 token 引入的不稳定性）和统计稳定性（避免了 KL 散度中正负项抵消的问题），使其成为离线 RL 训练中信任区域自适应的理想指标。

## 核心创新

M2PO 的核心创新在于**用重要性权重的二阶矩（$M_2$）替代传统 KL 散度作为分布偏移的度量**，并据此设计了一种**批量级自适应掩码策略**，在保留绝大多数信息性更新的同时，仅抑制极端离群 token。

### 从 KL 到 $M_2$：度量层面的范式转换

传统 PPO/GRPO 依赖 KL 散度或其近似（如 clipping）来约束策略更新幅度。但论文揭示了一个关键缺陷：**KL 散度作为一阶量，存在正负项相互抵消的问题**，导致其对分布偏移的感知不敏感。具体而言，当行为策略与当前策略的 token 级对数比 $\log r_i$ 同时出现正负值时，批量平均 KL 估计 $\hat{KL} = -\frac{1}{N}\sum \log r_i$ 会因抵消效应而低估真实的分布差距。

M2PO 提出的 $M_2$ 度量定义为：

$$\hat{M}_2 = \frac{1}{N}\sum_{i=1}^{N}(\log r_i)^2$$

该度量具有两个关键性质：
- **方差敏感性**：$M_2$ 始终非负，不会因正负抵消而失真，能有效捕捉高熵 token 引入的不稳定性；
- **统计稳定性**：作为二阶矩，$M_2$ 在批量估计下比 KL 散度更稳定，不易受个别样本扰动。

这一度量转换构成了 M2PO 的理论基石——从“约束平均偏移”转向“约束偏移的离散程度”，使得信任区域能够精准定位真正危险的离群更新。

### 批量级自适应掩码：从“一刀切裁剪”到“选择性抑制”

GRPO 的 clipping 机制对所有超过阈值 $[1-\epsilon, 1+\epsilon]$ 的 token 进行统一截断。在离线策略场景下（staleness $s=256$），由于策略漂移加剧，大量 token 触发裁剪，导致**信息性更新被系统性丢弃**，训练效率急剧下降（裁剪率从 0.07% 飙升至 1.22%）。

M2PO 的掩码策略改变了这一逻辑：

1. **仅在信任区域 token 上施加约束**：M2PO 仅对满足裁剪条件（即 $\pi_\theta / \pi_{\theta_{\text{old}}} \notin [1-\epsilon, 1+\epsilon]$）的 token 应用 $M_2$ 约束，避免对已处于安全区域的 token 进行不必要的干预。

2. **批量级自适应阈值筛选**：在满足条件的 token 集合上，M2PO 计算批量级 $\hat{M}_2$，并按 $|\log r_i|$ 降序逐个排除 token，直到剩余 token 的 $\hat{M}_2$ 降至预设阈值 $\tau_{M_2}$ 以下。被排除的 token 通过掩码 $M_{i,t}=0$ 从损失计算中移除。

3. **保留信息性更新**：由于 $M_2$ 仅抑制极端离群值（$|\log r_i|$ 最大的 token），绝大多数中等偏移的 token 得以保留，这些 token 携带着有效的学习信号。

实验证据直接验证了这一设计的有效性：在 Qwen-2.5-32B 上，M2PO（$s=256$）将平均裁剪率从 GRPO 的 0.66% 降至 **0.02%**，甚至低于 GRPO 在线策略（$s=0$）的 0.07%。同时，训练精度在经历短暂初始平台期后迅速追平在线策略基线（Figure 1）。

### 与 baseline 的 changed slots 对比

| 组件 | GRPO / GSPO | M2PO |
|------|-------------|------|
| 分布偏移度量 | KL 散度近似（clipping 隐式约束） | 二阶矩 $M_2$（显式度量） |
| 约束粒度 | token 级独立裁剪 | 批量级自适应掩码 |
| 约束对象 | 所有超出 $[1-\epsilon, 1+\epsilon]$ 的 token | 仅在信任区域 token 中排除极端离群值 |
| 超参数敏感性 | $\epsilon$ 需谨慎调节 | $\tau_{M_2}$ 不敏感（Figure 7 消融验证） |

这一 changed slot 组合使得 M2PO 在极端离线策略条件下（staleness ≥ 256）仍能保持稳定训练，并在 6 个模型规模（1.7B–32B）上实现与在线策略 GRPO 相当甚至更优的精度（Table 1），其中 Qwen3-Base-1.7B 上 M2PO（$s=256$）以 36.6% 的平均准确率显著超越在线策略 GRPO 的 33.0%。

## 整体框架

M2PO 的整体 pipeline 围绕**批级二阶矩约束下的选择性掩码**展开，在标准 GRPO 的基础上仅改造策略更新的信任域机制，其余数据流保持不变。其核心逻辑可归纳为四个阶段：

### 1. 数据生成与 staleness 控制

在每次训练迭代中，模型使用当前参数 $\theta$ 对一批 prompt 采样生成响应序列 $\{o_i\}_{i=1}^G$。在 off-policy 设定下，这些 rollout 数据并非即时消费，而是被缓存，经过 $k$ 步模型更新后才被用于训练——这 $k$ 即为 staleness 参数。论文主要考察极端情况 $k=256$，即数据滞后 256 次模型更新。

### 2. 逐 token 重要性权重计算

对于每个响应序列中的每个 token，计算重要性权重（importance weight）——即当前策略 $\pi_\theta$ 与行为策略 $\pi_{\theta_{\text{old}}}$ 的概率比值 $r_{i,t} = \frac{\pi_\theta(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid q, o_{i,<t})}$。同时沿用 GRPO 的组内标准化优势函数 $A_{i,t}$，以 prompt 为单位对响应组内奖励进行归一化。

### 3. 批级二阶矩约束与自适应掩码（核心创新）

这是 M2PO 区别于 GRPO 的关键模块。对于所有满足“信任域触发条件”的 token（即那些在标准 PPO 裁剪机制下会被裁剪的 token），计算其对数重要性权重的批级二阶矩：

$$\hat{M}_2 = \frac{1}{N} \sum_{i=1}^{N} (\log r_i)^2$$

若 $\hat{M}_2$ 超过预设阈值 $\tau_{M_2}$（默认 0.04），则按 $|\log r_i|$ 从大到小依次掩码（mask）token，直至剩余 token 的 $\hat{M}_2$ 降至阈值以下。被掩码的 token 不参与本次策略更新。该设计利用 $M_2$ 的方差敏感性来识别极端离群值，同时避免 KL 散度因正负项抵消而掩盖分布偏移的问题。

### 4. 策略更新

最终的目标函数仅对未被掩码的 token 计算：

$$\mathcal{I}_{\text{M2PO}}(\theta) = \frac{1}{\sum_{i=1}^{G} |o_i|} \sum_{i=1}^{G} \sum_{t=1}^{|o_i|} M_{i,t} \cdot \frac{\pi_\theta(o_{i,t})}{\pi_{\theta_{\text{old}}}(o_{i,t})} \cdot A_{i,t}$$

其中 $M_{i,t} \in \{0, 1\}$ 为掩码指示变量。被掩码的 token 梯度贡献为零，其余 token 正常参与优化。

### 模块关系与数据流

```
Prompt → 当前模型采样 → 响应序列缓存（staleness 延迟）
                                    ↓
              行为策略概率 / 当前策略概率 → 重要性权重 r
                                    ↓
              组内奖励归一化 → 优势函数 A
                                    ↓
              信任域触发 token 筛选 → 批级 M₂ 计算
                                    ↓
              M₂ > τ ? → 按 |log r| 降序掩码 token
                                    ↓
              未被掩码 token → 加权策略梯度更新
```

整个 pipeline 仅在“信任域约束”环节替换了 GRPO 的逐 token 裁剪机制，输入（prompt 集、采样响应、奖励信号）和输出（策略梯度更新）的接口与 GRPO 完全兼容。唯一的额外超参数 $\tau_{M_2}$ 经实验验证不敏感（见 Figure 7），使得该方法在实际部署中易于调参。

## 核心模块与公式推导

### M2PO 的核心设计逻辑

M2PO 的核心创新在于用一个**方差敏感的、统计稳定的信任区域度量**替代 GRPO 中基于逐 token 概率比裁剪的硬约束。其设计逻辑分为两步：

1. **度量构造**：用重要性权重的对数比（log-ratio）的二阶矩 $M_2$ 来刻画行为策略与当前策略之间的分布偏移。
2. **掩码约束**：在 batch 层面监控 $\hat{M}_2$，当超过阈值 $\tau_{M_2}$ 时，按 log-ratio 绝对值从大到小逐 token 掩码排除，直到 batch 级 $\hat{M}_2$ 回落到阈值以下。

这一机制的关键性质是：**只压制极端离群 token，保留绝大多数信息性更新**。

### 关键公式

**GRPO 原始目标**（作为背景）：

$$\mathcal{L}_{GRPO}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}(O|q)} \frac{1}{G} \sum_{i=1}^G \left( \min\left(r_i A_i, \text{clip}(r_i, 1-\epsilon, 1+\epsilon) A_i\right) \right)$$

其中 $r_i = \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}$ 为概率比，$A_i$ 为组内归一化优势（见下文）。

**组内优势归一化**（GRPO 共用）：

$$A_{i,t} = \frac{r_i - \text{mean}(\{R_i\}_{i=1}^G)}{\text{std}(\{R_i\}_{i=1}^G)}$$

其中 $R_i$ 为第 $i$ 条响应的奖励分数，$G$ 为每组响应数。该归一化使优势值在组内具有零均值、单位标准差。

**Batch 级 KL 散度估计**（作为对比基准）：

$$\hat{KL} = \frac{1}{N} \sum_{i=1}^N \hat{KL}_i = -\frac{1}{N} \sum_{i=1}^N \log r_i = -\frac{1}{N} \sum_{i=1}^N \log \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}$$

该度量存在**正负抵消问题**：当 batch 内部分 token 的概率比偏大、部分偏小时，平均 KL 可能接近零，掩盖真实的分布偏移。

**M2 度量**（M2PO 的核心度量）：

$$\hat{M}_2 = \frac{1}{N} \sum_{i=1}^N \hat{M}_{2,i} = \frac{1}{N} \sum_{i=1}^N (\log r_i)^2 = \frac{1}{N} \sum_{i=1}^N \left( \log \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} \right)^2$$

- $\hat{M}_2$ 非负，避免了 KL 的抵消缺陷。
- 对 log-ratio 的极端值（即策略偏移剧烈的 token）高度敏感，天然适合检测离群点。
- 统计上比 KL 更稳定，不依赖正负样本的平衡。

**M2PO 掩码目标**：

$$\mathcal{L}_{M2PO}(\theta) = \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} M_{i,t} \cdot \frac{\pi_\theta(o_{i,t}|q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q, o_{i,<t})} A_{i,t}$$

其中 $M_{i,t} \in \{0, 1\}$ 为掩码指示变量。掩码策略为：按 $|\log r_{i,t}|$ 降序排除 token，直至 batch 级 $\hat{M}_2 \leq \tau_{M_2}$。

**重要实现细节**：$M_2$ 约束**仅施加于信任区域 token**——即那些在 PPO 框架下本应被裁剪的 token（概率比超出 $[1-\epsilon, 1+\epsilon]$ 区间且优势方向与概率比偏移方向一致的 token）。这避免了在策略已对齐的区域施加不必要的约束。

### 阈值 $\tau_{M_2}$ 的敏感性

M2PO 仅有一个超参数 $\tau_{M_2}$。实验表明该阈值不敏感（见 Figure 7），默认值 $\tau_{M_2}=0.04$ 在多个模型尺度和任务上均表现稳定，保证了方法的易用性。

## 实验与分析

### 核心发现：M2PO 在极端陈旧数据下的稳定性与性能

M2PO 的核心实验结论是：在数据陈旧度高达 256 次模型更新的极端离线策略条件下，M2PO 不仅保持了训练稳定性，而且实现了与在线策略 GRPO 相当甚至更优的推理性能。这一结论在多个模型规模和任务类型上得到了一致验证。

**主结果（Table 1）** 覆盖了从 1.7B 到 32B 的六种模型（Llama-3.2-3B、Qwen2.5-Math-7B、Qwen3-Base-1.7B/4B/8B、Qwen2.5-32B）在八个数学推理基准（AIME、AMC、Math500、Gaokao、Minerva、Olympiad 等）上的表现。关键对比数据如下：


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/009_Table_1.jpg]]
*Table 1: Performance (%) comparison across eight math reasoning benchmarks using models from 1.7B to 32B parameters. We report results for GRPO, GSPO, and M2PO under both on-policy (s = 0) and off-policy (s = 256) settings. Underlined numbers denote the best average accuracy, while bold numbers highlight the best average accuracy under stale rollouts (s = 256). M2PO consistently improves stability under staleness and achieves higher average accuracy than GRPO*

- **M2PO (s=256) vs. GRPO (s=0)**：在六个模型组中，M2PO 在陈旧数据上的平均准确率有五个组别达到或超过了在线 GRPO。例如，Qwen3-Base-1.7B 上 M2PO (s=256) 达到 36.6%，而 GRPO (s=0) 仅为 33.0%；Qwen2.5-32B 上 M2PO (s=256) 为 52.6%，GRPO (s=0) 为 51.6%。
- **GRPO 在陈旧数据下的退化**：GRPO (s=256) 相比其在线版本 (s=0) 在所有模型上均出现显著性能下降，降幅从 Llama-3.2-3B 的 2.7 个百分点到 Qwen3-Base-4B 的 10.6 个百分点不等。这确认了标准 GRPO 的信任区域机制无法应对高陈旧度带来的分布偏移。
- **GSPO 同样失效**：GSPO 作为另一个基线方法，在 s=256 下同样出现大幅性能退化，表明仅靠重要性采样重加权不足以解决离线策略训练的稳定性问题。

**训练动态（Figure 1, Figure 5）** 进一步揭示了 M2PO 的收敛特性。在 Qwen-2.5-32B 上，M2PO (s=256) 在训练初期由于使用基础模型生成的陈旧数据而暂时落后于在线基线，但随后迅速追赶并最终匹配在线策略的性能轨迹。相比之下，GRPO (s=256) 不仅收敛更慢，而且最终准确率明显更低。在训练奖励曲线上，M2PO (s=256) 同样表现出与 s=0 轨迹高度对齐的特性。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/002_Figure_1.jpg]]
*Figure 1: Comparison of on-policy GRPO and off-policy training under a staleness of 256 model updates on Qwen-2.5-32B. Left: Standard GRPO suffers from degradation with stale rollouts, while removing the trust region (GRPO no TR) reveals a clear prosperity-before-collapse phenomenon. In contrast, M2PO achieves stable training and matches on-policy performance even under high staleness. Right: Token clipping ratio comparison shows that M2PO dramatically reduces clipping events compared to GRPO with the same staleness, while avoiding training collapse*

### 裁剪率分析：M2PO 如何维持稳定训练

M2PO 稳定性的直接证据来自对 token 裁剪率的分析。**Figure 6c 和 6d** 给出了关键定量结果：

- 在 Qwen-3-Base-1.7B 上，GRPO (s=256) 的平均裁剪率达到 0.66%，而 GRPO (s=0) 仅为 0.07%，M2PO (s=256) 更是低至 0.02%——比在线 GRPO 还低一个数量级。
- 在 Qwen2.5-32B 上，这一趋势同样成立：M2PO 在极端陈旧条件下维持的裁剪率甚至低于在线策略基线。
- 从训练全程来看（Figure 1 右图），GRPO (s=256) 的裁剪率频繁出现尖峰（最高约 0.02），而 M2PO 的裁剪率始终接近于零，与在线 GRPO 的灰色曲线几乎重合。

这一结果表明，M2PO 通过第二矩约束有效识别并屏蔽了极端离群 token，而非像 GRPO 那样对所有超出固定裁剪区间的 token 进行无差别裁剪。由于被裁剪的 token 往往携带重要的学习信号，GRPO 在陈旧数据下的大规模裁剪直接导致了性能退化。

### 消融与机制验证

**信任区域移除实验（Figure 3）** 揭示了"繁荣-崩溃"现象，这是理解 M2PO 设计动机的关键。在 Llama-3.2-Instruct-3B 上，当完全移除信任区域（ε=∞）并使用陈旧数据 (s=256) 训练时，模型初期表现出比带裁剪训练更高的准确率，有时甚至匹配在线策略基线。然而，训练随后发生灾难性崩溃，性能急剧下降。这一现象说明：


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/005_Figure_3.jpg]]
*Figure 3: Prosperity before Collapse. Training without a trust region (TR) ( $\epsilon$ ~ = ~ $\infty$ ) under stale data (s = 256) initially achieves higher performance than clipped training, sometimes even matching the onpolicy baseline (s = 0). However, it eventually collapses due to uncontrolled variance

1. 陈旧数据中确实包含有价值的、可驱动性能提升的更新信号。
2. 无约束地利用这些信号会导致训练崩溃，因此需要一个"精准"的约束机制——既能保留有益更新，又能过滤破坏性的极端离群值。
3. GRPO 的固定裁剪区间过于粗糙：它在陈旧度升高时过度裁剪，丢弃了太多有用信息。

**超参数敏感性（Figure 7）** 表明 M2PO 的唯一阈值超参数 τ_M₂ 不敏感，这降低了实际使用中的调参负担。

**与 TIS 的兼容性（Figure 10）** 显示，将 M2PO 与 TIS（一种缓解 FSDP 与 VLLM 之间分布差距的技术）结合使用时，性能有轻微提升。但 TIS 单独无法解决陈旧数据导致的离线策略问题，这确认了分布偏移的核心来源是策略陈旧而非推理框架差异。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/018_Figure_10.jpg]]
*Figure 10: Combining TIS with GRPO and M2PO on Qwen2.5-Math-7B with s = 256. Combined with TIS, M2PO shows a slight performance improvement, as TIS better mitigates the distribution gap between FSDP and VLLM. However, TIS alone cannot address the off-policy caused by staleness*

### 泛化性与计算开销

**跨任务泛化（Figure 6b）**：M2PO 在编程任务上同样有效。在 s=256 下，M2PO 显著优于同陈旧度下的 GRPO，且性能与在线 GRPO (s=0) 相当。

**不同陈旧度下的鲁棒性（Figure 13）**：在 Qwen2.5-Math-7B 上，M2PO 在多个陈旧度水平（s=0, 64, 128, 256）下均保持相对稳定的性能，而 GRPO 的性能随陈旧度增加呈明显单调下降趋势。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/023_Figure_13.jpg]]
*Figure 13: The performance of M2PO and GRPO under different staleness on Qwen2.5-Math-7B*

**计算开销（Table 2）**：M2PO 的损失计算时间约为 0.065 秒，占总训练时间（约 34-35 秒）的不到 0.2%。虽然略高于 GRPO 的 0.038 秒，但这一差异在实际训练中可忽略不计。


![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/021_Table_2.jpg]]
*Table 2: Comparison of computation time between GRPO and M2PO. Loss computation contributes a negligible portion of the total training time*

### 实验设置说明

所有实验采用数学推理和编程任务作为测试场景。陈旧数据通过 Stale-k 训练协议生成：每次训练迭代使用 k 次模型更新前生成的 rollout 数据。主要对比基线包括 GRPO 和 GSPO，均在在线策略 (s=0) 和离线策略 (s=256) 两种设置下评估。评估指标为各基准上的准确率，最终报告八个数学基准的平均准确率。

**需注意的实验局限**：当前实验的陈旧度上限为 256 次更新，更大陈旧度下的行为尚待验证。此外，τ_M₂=0.04 的通用性在不同模型规模和任务类型上虽有 Figure 7 的敏感性分析支持，但论文未提供跨所有模型配置的系统性阈值扫描结果。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_IIgl5MWelz/figures/013_Figure_6.jpg]]
*Figure 6: (a) Methods comparison under staleness ( s = 2 5 6 ) on Llama3.2-Instruct-3B. (b) Performance comparison between M2PO and GRPO on coding tasks. (c) Clipping ratio dynamics during RL on the Qwen-3-Base-1.7B model. (d) Comparison of the average clipping ratio across models and methods*


## 方法谱系与知识库定位

### 与现有方法的谱系关系

M2PO 的方法根基是 **GRPO**（Group Relative Policy Optimization），后者通过组内奖励归一化和 PPO 风格的 clipped surrogate objective 来约束策略更新幅度。GRPO 的信任区域机制依赖于重要性采样比率的逐 token 裁剪（clipping ratio $r_i$ 被限制在 $[1-\epsilon, 1+\epsilon]$ 内），这在在线策略场景下运行良好，但在离线策略条件下暴露出结构性缺陷。

**GSPO** 是 GRPO 的一个直接变体，同样依赖重要性权重裁剪作为信任区域机制。论文将 GSPO 作为与 GRPO 并列的基线方法进行对比。在表 1 的主实验中，GRPO 和 GSPO 在 $s=256$ 的离线策略条件下均出现显著的性能退化（例如 Qwen3-Base-4B 上 GRPO 从 50.7% 降至 40.1%），表明基于裁剪的信任区域策略对策略分布偏移高度敏感。

M2PO 的谱系突破在于：它不再依赖逐 token 的比率裁剪，而是转向**批量级别的二阶矩约束**。这一设计选择直接回应了 GRPO/GSPO 在离线策略场景下的核心失效模式——裁剪比率在高陈旧度下急剧上升（图 4a），导致大量 token 被裁剪，信息更新被系统性丢弃。M2PO 通过 $M_2$ 指标（$\hat{M}_2 = \frac{1}{N}\sum_{i=1}^N (\log r_i)^2$）测量策略分布偏移的方差，并仅在批量 $M_2$ 超过阈值 $\tau_{M_2}$ 时选择性掩蔽极端离群 token，从而在保留绝大多数信息性更新的同时抑制训练不稳定。

从更广泛的方法谱系来看，M2PO 处于**离线策略信任区域方法**的交叉地带。它借鉴了 PPO/GRPO 的信任区域思想，但用二阶矩约束替代了一阶裁剪；它与 KL 散度约束方法共享"测量分布偏移"的动机，但避免了 KL 散度在批量聚合时的正负抵消效应（$\hat{KL} = -\frac{1}{N}\sum \log r_i$ 在正负比率混合时可能严重低估真实偏移）。论文明确论证了 $M_2$ 相对于 KL 散度的两个优势：(1) **方差敏感性**——$M_2$ 对离群 token 高度敏感，能捕获高熵 token 引入的不稳定性；(2) **统计稳定性**——$M_2$ 非负且无抵消效应，能更忠实地反映批量级别的分布偏移程度。

### 适用边界与前提条件

M2PO 的有效性建立在以下前提之上：

1. **离线策略训练场景**：M2PO 的核心优势在陈旧数据条件下（$s \ge 256$ 模型更新）才充分显现。在在线策略场景（$s=0$）下，GRPO 本身的裁剪机制已足够有效，M2PO 的额外约束未必带来显著增益（表 1 中 M2PO $s=0$ 与 GRPO $s=0$ 的性能差异在多数模型上不显著）。

2. **批量级别的统计稳定性**：M2PO 的掩蔽策略依赖批量 $M_2$ 估计的可靠性。当批量规模过小或数据分布极度偏斜时，$\hat{M}_2$ 的估计方差可能增大，影响阈值判断的准确性。论文未系统探讨极小批量场景下的行为。

3. **阈值 $\tau_{M_2}$ 的合理设定**：论文使用固定阈值 $\tau_{M_2} = 0.04$，并通过消融实验（图 7）论证该超参数不敏感。但该结论仅在 Llama-3.2-3B-Instruct 和 Qwen2.5-Math-7B 两个模型上验证，跨模型尺度和任务类型的普适性需要进一步确认。

4. **信任区域 token 的识别**：M2PO 仅对"本应被裁剪"的 token 施加 $M_2$ 约束（即满足 PPO 裁剪条件的 token）。这一设计假设裁剪条件本身是识别潜在不稳定 token 的有效信号。如果策略偏移的模式发生变化（例如分布偏移主要来自未被裁剪条件捕获的 token），M2PO 的保护可能不完整。

### 已知局限

1. **陈旧度上限未充分探索**：论文仅在 $s=256$ 的陈旧度下系统验证 M2PO。在更大陈旧度（如 $s=512$ 或 $s=1024$）下的行为未知。图 2 的趋势表明更高陈旧度会导致更严重的性能退化，M2PO 能否持续有效需要验证。

2. **阈值 $\tau_{M_2}$ 的跨任务泛化**：虽然图 7 显示 $\tau_{M_2}$ 在数学推理任务上不敏感，但论文未在编码任务（图 6b）或其他领域验证阈值的鲁棒性。不同任务的数据分布和策略偏移模式可能要求不同的阈值。

3. **计算开销**：M2PO 的掩蔽算法（Algorithm 1）需要计算批量 $M_2$ 并对 token 进行排序和选择性排除，这引入了额外的计算步骤。论文未报告 M2PO 相对于 GRPO 的 wall-clock 时间开销。

4. **"繁荣-崩溃"现象的深层机制**：论文通过图 3 揭示了无信任区域训练在陈旧数据下的"先繁荣后崩溃"现象，但未深入分析崩溃发生的精确条件（例如 $M_2$ 的临界值、模型参数的发散模式）。M2PO 通过 $M_2$ 约束有效阻止了崩溃，但崩溃的早期预警信号和预防机制仍需进一步研究。

### 开放问题

1. **M2PO 能否支持完全异步的离线策略训练？** 当前实验设定中陈旧数据仍来自同一训练轨迹的早期检查点。在完全异步场景下（数据来自不同初始化或不同超参数的训练过程），行为策略与当前策略的分布偏移可能呈现不同模式，M2PO 的二阶矩约束是否仍然充分？

2. **$M_2$ 指标能否推广到其他信任区域方法？** $M_2$ 作为分布偏移的方差敏感度量，其设计原理独立于 GRPO 的组内归一化机制。理论上 $M_2$ 可以嵌入 PPO、TRPO 等其他信任区域框架。这种跨方法迁移的可行性和收益值得探索。

3. **自适应阈值机制**：当前 $\tau_{M_2}$ 为固定值。根据训练阶段的动态特征（如 $M_2$ 的历史分布、奖励信号的稳定性）自适应调整阈值，可能进一步提升 M2PO 在不同训练阶段的效率——在稳定阶段放松约束以加速学习，在波动阶段收紧约束以保证安全。

4. **$M_2$ 约束与奖励塑形的交互**：GRPO 的组内归一化本身是一种隐式的奖励塑形。$M_2$ 约束改变了有效更新 token 的分布，这可能间接影响组内优势估计的统计性质。这种交互效应是否会影响模型探索-利用平衡，需要更系统的分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/Prosperity_before_Collapse_How_Far_Can_Off_Policy_RL_Reach_with_Stale_Data_on_LLMs.pdf]]
