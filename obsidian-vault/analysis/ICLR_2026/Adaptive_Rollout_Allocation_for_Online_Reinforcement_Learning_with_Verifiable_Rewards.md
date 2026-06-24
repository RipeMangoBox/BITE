---
title: "Adaptive Rollout Allocation for Online Reinforcement Learning with Verifiable Rewards"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verifiable_Rewards.pdf
aliases:
- VVIPAS
- ARAORLVR
acceptance: accepted
openreview_forum_id: Z5sWYACAop
tags:
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: 基于高斯过程预测每个提示的成功概率，动态计算和最小化梯度方差，从而自适应地分配推广次数，将计算预算集中在具有最大信息增益的提示上。
primary_logic: 通过理论分析揭示梯度方差与提示成功概率 p 的函数关系，利用高斯过程在嵌入空间中对 p 进行在线预测，并将分配问题形式化为一个凸优化问题，可在总预算约束下精确求解并取整，从而显著提升采样效率和最终模型性能。
claims:
- VIP 持续超越基于均匀或启发式分配的所有基线方法，在 AIME24/25 上提升显著（例如 RLOO+VIP 的 Pass@32 从 18.29% 提高到 30.55%）。
- 在 Bamboogle 和 MuSiQue 工具增强推理任务上，Dr. GRPO+VIP 和 RLOO+VIP 均一致提高 EM、F1@5 和 Precision@5。
- 高斯过程预测器的成功概率 MAE 始终低于移动平均和岭回归基线。
- VIP 的额外计算开销极小（1.5B 模型 1.12%，7B 模型 0.83%）。
paradigm: 通过理论分析揭示梯度方差与提示成功概率 p 的函数关系，利用高斯过程在嵌入空间中对 p 进行在线预测，并将分配问题形式化为一个凸优化问题，可在总预算约束下精确求解并取整，从而显著提升采样效率和最终模型性能。
---

# Adaptive Rollout Allocation for Online Reinforcement Learning with Verifiable Rewards

> [!tip] 核心洞察
> 通过理论分析揭示梯度方差与提示成功概率 p 的函数关系，利用高斯过程在嵌入空间中对 p 进行在线预测，并将分配问题形式化为一个凸优化问题，可在总预算约束下精确求解并取整，从而显著提升采样效率和最终模型性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向可验证奖励的在线强化学习的自适应推广分配策略 |
| 英文题名 | Adaptive Rollout Allocation for Online Reinforcement Learning with Verifiable Rewards |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=Z5sWYACAop) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | VIP (Variance-Informed Predictive allocation strategy) |
| Dataset | AIME24, Bamboogle, MuSiQue, Bamboogle |

> [!tip] 效果简介
> - AIME24 上，Pass@32 为 30.55%，对比 18.29%，变化 +12.26%。
> - Bamboogle 上，EM 为 23.2% (Dr. GRPO+VIP)，对比 20.0% (Dr. GRPO)，变化 +3.2%。
> - MuSiQue 上，EM 为 10.5% (Dr. GRPO+VIP)，对比 6.0% (Dr. GRPO)，变化 +4.5%。

## 概述

群体策略优化方法（如 GRPO、RLOO）在在线强化学习中为每个训练提示分配固定数量的推广（rollout），这一均匀分配策略存在根本性的效率瓶颈：大量提示的成功概率接近 0 或 1，其梯度方差极低，却消耗了与高信息量提示相同的计算预算，导致整体梯度方差高、采样效率低下。

本文提出 **VIP（Variance-Informed Predictive allocation strategy）**，核心思路是通过预测每个提示的梯度方差，动态地将推广预算集中分配给那些能最大程度降低梯度方差的提示。具体而言，VIP 包含三个关键模块：① 利用高斯过程在嵌入空间中在线预测每个提示的成功概率 $p$；② 基于理论推导的梯度方差表达式（Dr. GRPO 为 $\mathrm{Var}(\tilde{G}) = \frac{(n-1)}{n^2} 4 \sigma_Z^2 p (1-p)$，RLOO 为 $\mathrm{Var}(\tilde{G}) = \frac{1}{n-1} 4 \sigma_Z^2 p (1-p)$），将分配问题形式化为凸优化问题，并通过 KKT 条件精确求解连续松弛；③ 采用贪心启发式取整得到满足总预算和上下界约束的整数分配。

实验结果表明，VIP 在多个基准上持续超越均匀分配和启发式分配基线。在数学推理任务 AIME24 上，RLOO+VIP 的 Pass@32 从 18.29% 提升至 30.55%（+12.26%）；在工具增强推理任务 Bamboogle 和 MuSiQue 上，Dr. GRPO+VIP 和 RLOO+VIP 均一致提高 EM、F1@5 和 Precision@5。消融实验证实高斯过程预测器和基于方差的分配策略各自对性能提升有贡献，且 VIP 的额外计算开销极小（1.5B 模型仅占 1.12%，7B 模型仅占 0.83%）。高斯过程预测器的成功概率 MAE 始终低于移动平均和岭回归基线，验证了其预测精度。

VIP 目前主要针对可验证奖励（RLVR）场景设计，奖励为确定且可自动验证的二元变量，直接扩展到带噪声奖励的 RLHF 场景仍需额外设计。

## 背景与动机

### 可验证奖励下的在线强化学习

大型语言模型的对齐训练中，基于可验证奖励的在线强化学习（RLVR）已成为提升模型推理能力的关键范式。与依赖人类偏好或奖励模型的 RLHF 不同，RLVR 使用可自动验证的确定性奖励信号（如数学题答案的正确性、代码执行的通过率），避免了奖励模型训练和推理的额外开销。在此范式下，群体策略优化方法（如 GRPO、Dr. GRPO、RLOO）通过为每个训练提示采样多个推广（rollout），计算组内优势估计来更新策略，展现出显著的性能提升。

### 固定推广分配的核心瓶颈

尽管群体策略优化方法在实践中表现优异，其采样效率存在一个被忽视的结构性问题：**对每个提示分配固定数量的推广**。这一均匀分配策略隐含假设所有提示对梯度更新的贡献相等，但在实际训练中，提示的信息量差异巨大——

- 对于模型已稳定答对（成功概率 $p \approx 1$）或稳定答错（$p \approx 0$）的提示，其梯度方差趋于零，几乎不贡献有效的梯度信号；
- 对于模型处于学习边界（$p \approx 0.5$）的提示，梯度方差最大，信息增益最高。

均匀分配将大量计算预算浪费在低信息量的提示上，导致整体梯度估计方差偏高，收敛缓慢。

### 梯度方差的因果机制

本文从理论上揭示了梯度方差与提示成功概率 $p$ 的函数关系。在二元奖励设定下，Dr. GRPO 和 RLOO 的每提示梯度方差分别为：

$$\mathrm{Var}(\tilde{G})_{\text{Dr. GRPO}} = \frac{(n-1)}{n^2} \cdot 4 \sigma_Z^2 \cdot p(1-p)$$

$$\mathrm{Var}(\tilde{G})_{\text{RLOO}} = \frac{1}{n-1} \cdot 4 \sigma_Z^2 \cdot p(1-p)$$

其中 $\sigma_Z^2$ 为投影梯度的方差。这一形式揭示了两个关键因果杠杆：

1. **$p(1-p)$ 项**：梯度方差随提示难度呈倒 U 型分布，在 $p=0.5$ 时达到峰值，在 $p=0$ 或 $p=1$ 时归零。这意味着模型的学习信号天然集中于难度适中的提示。
2. **推广数 $n$ 的调节作用**：增加推广数可以降低方差，但边际收益递减——Dr. GRPO 中方差以 $O(1/n)$ 速率下降，RLOO 中以 $O(1/(n-1))$ 速率下降。

这一分析表明，**如果能够在线预测每个提示的 $p$ 值，就可以动态地将推广预算从低方差提示重新分配给高方差提示，在不增加总计算量的前提下最小化整体梯度方差**。

### 现有方法的不足与本文动机

现有分配策略均无法有效利用上述因果机制：

- **均匀分配**（Uniform）：完全忽略提示间的信息量差异，效率最低；
- **逆准确率分配**（Inverse-accuracy）：对准确率低的提示分配更多推广，但低准确率（$p \approx 0$）的提示梯度方差同样很低，这种启发式策略与方差最小化的目标不一致；
- **逆方差分配**（Inverse-variance）：基于历史运行方差分配，但历史方差估计噪声大、滞后严重，且无法预测未见提示的方差。

上述方法的核心缺陷在于：**缺乏对提示成功概率的准确在线预测能力，以及缺乏将预测转化为最优分配的数学框架**。本文提出的 VIP（Variance-Informed Predictive allocation strategy）正是针对这两个缺口设计——通过高斯过程在嵌入空间中预测每个提示的 $p$ 值，并将其代入凸优化问题精确求解方差最小化的推广分配方案。

## 核心创新

### 问题瓶颈：固定推广分配导致的采样效率低下

群体策略优化方法（如 GRPO、Dr. GRPO、RLOO）在训练时对每个提示分配固定数量的推广（rollout），这种均匀分配策略存在根本性的效率问题：许多提示的信息量较低（例如过于简单或过于困难），其推广结果无法贡献有效的梯度信号，却消耗了同等的计算预算。这导致两个直接后果——**采样效率低下**和**梯度方差大**，最终限制了模型的收敛速度和最终性能。

### 关键洞察：梯度方差与成功概率的函数关系

VIP 的核心洞察来源于对梯度方差的严格理论分析。在二元可验证奖励的设定下，Dr. GRPO 和 RLOO 的每提示梯度方差可以精确表达为成功概率 $p$ 的函数：

- **Dr. GRPO**：$\mathrm{Var}(\tilde{G}) = \frac{(n-1)}{n^2} \cdot 4 \sigma_Z^2 \cdot p(1-p)$
- **RLOO**：$\mathrm{Var}(\tilde{G}) = \frac{1}{n-1} \cdot 4 \sigma_Z^2 \cdot p(1-p)$

其中 $n$ 为推广次数，$\sigma_Z^2$ 为投影梯度的方差。这一分析揭示了一个关键事实：**梯度方差在 $p \approx 0.5$ 时最大，在 $p$ 接近 0 或 1 时趋近于零**。这意味着，对于模型已经稳定解决（$p \approx 1$）或几乎无法解决（$p \approx 0$）的提示，增加推广次数对降低方差的边际收益极低；真正需要更多推广的是那些处于“学习边界”（$p \approx 0.5$）的提示。

### 方法创新：预测-分配双模块架构

基于上述洞察，VIP 引入了一个**预测-分配双模块架构**，从根本上改变了推广预算的分配方式：

**模块一：高斯过程成功概率预测器**

由于训练过程中每个提示的真实成功概率 $p$ 是未知且动态变化的，VIP 使用一个轻量级的高斯过程（GP）模型在提示的嵌入空间中进行在线预测。具体而言：
- 在隐变量 $g_t(x_q)$ 上放置一个带有 RBF 核 $\boldsymbol{K}(\boldsymbol{x}, \boldsymbol{x}') = \exp(-\|\boldsymbol{x} - \boldsymbol{x}'\|_2^2 / (2h^2))$ 的高斯过程先验
- 通过 sigmoid 链接函数 $p_{q,t} = \mathrm{sigmoid}(g_t(x_q))$ 将隐变量映射为成功概率
- 在每步训练后，利用当前批次的推广结果递归更新后验均值 $m_{t,B_t^c}^\star = m_{t,B_t^c} + \Sigma_{B_t^c B_t} \Sigma_{B_t B_t}^{-1} (\hat{g}_{B_t} - m_{t,B_t})$

这种设计的关键优势在于：GP 不仅能给出点估计，还能利用提示嵌入之间的相似性进行信息共享，使得对未见或少见提示的预测更加准确。实验表明，GP 预测器的 MAE 始终低于移动平均和岭回归基线（Figure 3）。

**模块二：方差最小化推广分配优化器**

在获得每个提示的预测成功概率后，VIP 将推广分配问题形式化为一个**凸优化问题**：在总预算约束 $\sum_q n_q = C$ 和每提示上下界 $L \leq n_q \leq U$ 下，最小化小批量的总梯度方差。对于 Dr. GRPO，其连续松弛形式为：

$$\min\left\{\sum_{q\in\mathcal{B}_t} a_q \frac{n_q-1}{n_q^2} : \sum_{q} n_q = C, L \le n_q \le U \right\}$$

其中 $a_q = 4 \sigma_Z^2 p_q(1-p_q)$。通过 KKT 条件，可得到最优分配 $n_q^\star$ 与对偶变量 $\lambda$ 的解析关系：

$$n_q^\star(\lambda) = \begin{cases} U & \text{if } \lambda \le a_q \frac{U-2}{U^3} \\ \text{unique solution to } \lambda = a_q \frac{n_q-2}{n_q^3} & \text{if } a_q \frac{U-2}{U^3} < \lambda < a_q \frac{L-2}{L^3} \\ L & \text{if } \lambda \ge a_q \frac{L-2}{L^3} \end{cases}$$

该问题可通过二分搜索高效求解，随后使用贪心启发式取整算法（Algorithm 2）将连续解转化为满足整数约束的可行分配。

### 与 baseline 的对比：从固定分配到自适应分配

VIP 与现有方法的本质差异体现在 **changed slot**——推广分配策略上：

| 维度 | Baseline（均匀分配） | VIP（自适应分配） |
|------|---------------------|-------------------|
| 分配依据 | 固定每提示推广数 | GP 预测的成功概率 → 梯度方差 |
| 优化目标 | 无 | 最小化小批量总梯度方差 |
| 计算预算利用 | 均匀消耗 | 集中分配给信息量最大的提示 |
| 对 $p \approx 0.5$ 的提示 | 与其他提示相同 | 分配更多推广 |
| 对 $p \approx 0$ 或 $1$ 的提示 | 与其他提示相同 | 分配较少推广 |

Figure 2 直观展示了不同分配策略的差异：逆准确率分配和逆方差分配等启发式方法无法精确匹配方差最小化的最优分配曲线，而 VIP 通过凸优化精确实现了这一目标。消融实验（Table 3）进一步证实，GP 预测器和方差感知分配策略都对性能提升有独立贡献——仅替换预测器或仅替换分配策略均无法达到完整 VIP 的效果。

### 计算效率：极低的额外开销

尽管引入了 GP 推断和凸优化求解，VIP 的计算开销极小。Table 4 显示，对于 1.5B 参数模型，VIP 的额外开销仅占 RL 训练总时间的 **1.12%**；对于 7B 参数模型，这一比例进一步降至 **0.83%**。这种高效率得益于 GP 仅在小批量嵌入上运行，且优化问题具有解析解形式，无需昂贵的迭代求解。

## 整体框架

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/001_Figure_1.jpg]]
*Figure 1: The process starts with an initial belief over prompt success probabilities. At each step t, a mini-batch B _ { t } is selected, and the belief function m _ { t } ( \cdot ) predicts the success probabilities of the prompts in B _ { t } . \mathrm { A } budget allocation module assigns rollout budgets \{ n _ { q } \} , rollouts are generated, and the resulting data updates the model and beliefs. Repeated for \bar { T } steps, this yields a fine-tuned model \pi _ { \boldsymbol { \theta } _ { T + 1 } } with improved performance and efficient rollout usage*

VIP（Variance-Informed Predictive allocation strategy）是一个围绕**预测-分配-采样-更新**循环构建的轻量级在线分配框架，其核心目标是：在固定的总推广预算约束下，通过最小化小批量的梯度方差来最大化采样效率。

### 框架总览

整个训练流程由四个关键模块串联而成，如 Figure 1 所示：

1. **高斯过程成功概率预测器**：接收当前模型对提示的嵌入表示，利用高斯过程递归更新每个提示成功概率 $p_q$ 的后验信念。
2. **方差最小化推广分配优化器**：将预测的成功概率转化为梯度方差估计，构建凸优化问题，在总预算 $C$ 和每提示上下界 $[L, U]$ 约束下求解最优推广数 $\{n_q\}$。
3. **推广生成与奖励验证**：按分配结果对每个提示采样 $n_q$ 条推理轨迹，通过可验证奖励函数（RLVR）获得二元奖励信号。
4. **模型更新与信念更新**：利用采样数据计算组内优势估计（如 Dr. GRPO 或 RLOO）并更新策略参数；同时将新观测的奖励反馈回高斯过程，更新成功概率的预测。

这一循环在小批量 $B_t$ 上迭代进行，直至训练结束，输出精调后的模型 $\pi_{\theta_{T+1}}$。

### 模块间的数据流与依赖关系

框架的输入包括三个部分：初始信念 $m_1(\cdot)$（零均值高斯过程先验）、小批量调度策略和基础模型 $\pi_{\theta_1}$。在每个训练步 $t$：

- **预测器 → 分配器**：预测器输出小批量 $B_t$ 中每个提示 $q$ 的成功概率 $p_{q,t}$，分配器据此计算方差系数 $a_q = 4\sigma_Z^2 p_q(1-p_q)$。
- **分配器 → 采样器**：分配器求解连续松弛问题（式 6）并通过二分搜索得到精确解 $n_q^\star(\lambda)$（Theorem 5.1），再经贪心取整启发式（Algorithm 2）产出满足整数约束的分配方案 $\{\hat{n}_q\}$。
- **采样器 → 模型更新**：对每个提示采样 $\hat{n}_q$ 条轨迹，计算优势估计和策略梯度，更新模型参数 $\theta_t \to \theta_{t+1}$。
- **采样器 → 预测器**：将轨迹的二元奖励聚合为经验成功概率 $\hat{p}_{q,t}$，通过逆 sigmoid 映射得到隐变量观测 $\hat{g}_{q,t}$，驱动高斯过程后验更新（式 5.1），将信息传播到嵌入空间中邻近的未观测提示。

### 关键设计决策

**方差驱动的分配目标**：不同于启发式的逆准确率或逆方差分配，VIP 的分配优化直接以梯度方差 $\mathrm{Var}(\tilde{G})$ 为最小化目标。理论分析（Proposition 4.2, 4.3）表明，对于 Dr. GRPO 和 RLOO，每提示梯度方差可统一表达为 $p(1-p)$ 乘以与 $n$ 相关的递减函数——这意味着成功概率接近 0.5 的提示（高方差提示）应获得更多推广，而极难或极易的提示应获得较少推广。

**高斯过程预测的平滑性**：使用 RBF 核 $\boldsymbol{K}(\boldsymbol{x}, \boldsymbol{x}') = \exp(-\|\boldsymbol{x} - \boldsymbol{x}'\|_2^2 / (2h^2))$ 建模嵌入空间中提示成功概率的相关性，使得预测器能够利用已观测提示的信息推断未观测提示的难度，而无需对每个提示独立建模。Figure 3 表明，该预测器的 MAE 持续低于移动平均和岭回归基线。

**凸优化与取整解耦**：将整数规划问题先松弛为连续凸优化，利用 KKT 条件得到 $n_q^\star$ 关于对偶变量 $\lambda$ 的解析表达式，通过二分搜索高效求解；随后采用基于目标函数增益 $f_q(n) = a_q \frac{n-1}{n^2}$（Dr. GRPO）的贪心取整策略，在保证上下界约束的前提下将连续解转化为可行整数解。Table 4 显示，整套 VIP 流程的额外计算开销仅占 RL 训练总时间的 1.12%（1.5B 模型）和 0.83%（7B 模型）。

## 核心模块与公式推导

VIP 方法由三个核心模块串联构成：高斯过程成功概率预测器、方差最小化推广分配优化器，以及贪心启发式整数取整算法。三个模块协同工作，将计算预算动态集中在梯度方差最大的提示上。

### 高斯过程成功概率预测器

对于每个提示 $q$，其成功概率 $p_{q,t}$ 通过 sigmoid 函数映射到一个隐高斯过程：

$$p_{q,t} = \mathrm{sigmoid}(g_t(x_q)) = \frac{1}{1 + \exp(-g_t(x_q))}$$

其中 $g_t \sim \mathcal{GP}(m_t(\cdot), \boldsymbol{K}(\cdot, \cdot))$，核函数为 RBF 核：

$$\boldsymbol{K}(\boldsymbol{x}, \boldsymbol{x}') = \exp\left(-\frac{\|\boldsymbol{x} - \boldsymbol{x}'\|_2^2}{2h^2}\right)$$

在训练步 $t=1$ 时使用零均值先验 $g_1 \sim \mathcal{GP}(0, \boldsymbol{K})$。后续每步，利用当前小批量中已采样的提示及其经验成功概率 $\hat{p}_{q,t} = \mathrm{clip}\left(\frac{\bar{R}_q + 1}{2}, \epsilon, 1-\epsilon\right)$，通过标准高斯过程后验更新公式递归更新隐变量预测：

$$m_{t,B_t^c}^\star = m_{t,B_t^c} + \boldsymbol{\Sigma}_{B_t^c B_t} \boldsymbol{\Sigma}_{B_t B_t}^{-1} (\hat{g}_{B_t} - m_{t,B_t})$$

该预测器是整个分配策略的信息瓶颈——其预测精度直接决定后续优化问题中系数 $a_q$ 的可靠性。实验表明，GP 预测器的成功概率 MAE 始终低于移动平均和岭回归基线（Figure 3），为方差最小化分配提供了可靠的概率估计。

### 梯度方差的理论分析

VIP 的分配策略建立在梯度方差的解析形式上。在二元奖励设定（奖励 $R \in \{-1, 1\}$）下，给定提示 $q$ 的成功概率 $p$，两种主流群体策略优化方法的每提示投影梯度方差分别为：

**Dr. GRPO**（Proposition 4.2）：

$$\mathrm{Var}(\tilde{G}) = \frac{(n-1)}{n^2} \cdot 4 \sigma_Z^2 \cdot p(1-p)$$

**RLOO**（Proposition 4.3）：

$$\mathrm{Var}(\tilde{G}) = \frac{1}{n-1} \cdot 4 \sigma_Z^2 \cdot p(1-p)$$

其中 $\sigma_Z^2$ 为投影梯度的方差，$n$ 为该提示分配的推广次数。两个公式揭示了相同的核心机制：梯度方差与 $p(1-p)$ 成正比，在 $p=0.5$ 时达到最大——这正是模型对提示最不确定、信息量最高的状态。

### 方差最小化推广分配优化器

基于上述方差公式，VIP 将小批量 $\mathcal{B}_t$ 内的推广分配问题形式化为一个受总预算 $C$ 和每提示上下界 $L, U$ 约束的优化问题。以 Dr. GRPO 为例，其连续松弛形式为：

$$\min\left\{\sum_{q\in\mathcal{B}_t} a_q \frac{n_q-1}{n_q^2} : \sum_{q\in\mathcal{B}_t} n_q = C,\ L \le n_q \le U\right\}$$

其中 $a_q = 4\sigma_{Z_q}^2 \cdot p_q(1-p_q)$，由 GP 预测器输出的 $p_q$ 计算得到。该问题是凸的，可通过 KKT 条件求得解析解。最优分配 $n_q^\star$ 与对偶变量 $\lambda$ 的关系为（Theorem 5.1）：

$$n_q^\star(\lambda) = \begin{cases} U & \text{if } \lambda \le a_q \frac{U-2}{U^3} \\ \text{唯一解 } \lambda = a_q \frac{n_q-2}{n_q^3} & \text{if } a_q \frac{U-2}{U^3} < \lambda < a_q \frac{L-2}{L^3} \\ L & \text{if } \lambda \ge a_q \frac{L-2}{L^3} \end{cases}$$

通过二分搜索确定 $\lambda$ 使得 $\sum_q n_q^\star(\lambda) = C$，即可得到连续最优分配。该优化器的关键设计在于：$a_q$ 越大的提示（即 $p_q$ 越接近 0.5），分配到的推广次数越多，从而将计算预算精准投向梯度信号最强的提示。

### 贪心启发式整数取整

由于实际推广次数必须为整数，VIP 对连续解进行启发式取整：首先将 $n_q^\star$ 向下取整为 $\lfloor n_q^\star \rfloor$，然后按每提示目标函数的边际增益贪心地分配剩余预算。Dr. GRPO 的每提示目标函数为：

$$f_q(n) = a_q \frac{n-1}{n^2}$$

RLOO 的对应形式为 $f_q(n) = a_q \frac{\bar{r}}{n-1}$。取整过程确保满足 $L \le \hat{n}_q \le U$ 的边界约束，直至总预算 $C$ 耗尽。

### 计算开销

三个模块的额外计算开销极小。在单 GPU 上，核矩阵计算、GP 训练/预测和推广分配的总时间仅占整体 RL 训练时间的 1.12%（1.5B 模型）和 0.83%（7B 模型）（Table 4），不会成为训练瓶颈。

## 实验与分析

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/002_Table_1.jpg]]
*Table 1: Percentage results on AIME24 and AIME25. The upper block uses a total rollout budget of C = 8 \times Q , and the lower block uses C = 1 6 \times Q For each pair (Dr. GRPO vs Dr. \mathrm { G R P O _ { + V I P } } and RLOO vs \mathrm { R L O O _ { + V I P } ) } , higher values are highlighted in green*

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/003_Table_2.jpg]]
*Table 2: Performance on Bamboogle and MuSiQue. Green cells indicate improvements of the +VIP variant over its base method*

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/004_Table_3.jpg]]
*Table 3: Ablation study on AIME24 and AIME25. All values are percentages. For each metric, the highest value across methods is highlighted in green*

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/013_Figure_3.jpg]]
*Figure 3: Prediction mean absolute error (MAE) over training steps for two model scales. Our GPR-based predictor achieves consistently lower MAE than moving average and Ridge Regression baselines for both the 1.5B and 7B models*

![[obsidian-vault/assets/figures/papers/paper_list_l7_Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verif/figures/005_Table_4.jpg]]
*Table 4: Wall-clock runtime of core computational components and model-specific operations for Qwen2.5-Math-1.5B and Qwen2.5-Math-7B, measured on a single GPU*

### 核心瓶颈与因果机制

群体策略优化方法（如 GRPO、Dr. GRPO、RLOO）在可验证奖励（RLVR）设定下，对每个训练提示分配固定数量的推广（rollouts）。理论分析揭示，这一均匀分配策略存在根本性的采样效率瓶颈：梯度方差与提示的成功概率 $p$ 呈函数关系 $p(1-p)$，当 $p$ 接近 0.5 时方差最大，而许多提示的 $p$ 远离 0.5，其推广对梯度信号贡献微弱，却消耗了同等的计算预算。

VIP（Variance-Informed Predictive allocation strategy）通过三个模块化组件打破这一瓶颈：
1. **高斯过程成功概率预测器**：在提示嵌入空间上放置 RBF 核 GP 先验，利用 sigmoid 链接函数 $p_{q,t} = \mathrm{sigmoid}(g_t(x_q))$ 在线预测每个提示的成功概率；
2. **方差最小化分配优化器**：基于预测的 $p_q$ 构建凸优化问题，最小化 mini-batch 总梯度方差，通过 KKT 条件导出解析解 $n_q^\star(\lambda)$，并用二分搜索确定对偶变量 $\lambda$；
3. **贪心启发式取整算法**：将连续解向下取整后，按目标函数增益 $f_q(n) = a_q \frac{n-1}{n^2}$（Dr. GRPO）或 $f_q(n) = a_q \frac{1}{n-1}$（RLOO）贪心分配剩余预算，满足上下界约束。

### 主实验结果

**数学推理（AIME24/25）**：Table 1 展示了在总预算 $C = 8 \times Q$ 和 $C = 16 \times Q$ 下的 Pass@32、Mean@32、Maj@32 结果。VIP 在所有模型规模和预算设置下均一致提升性能。以 Qwen2.5-Math-1.5B + RLOO 在 $C = 8 \times Q$ 为例，RLOO+VIP 将 AIME24 的 Pass@32 从 18.29% 提升至 30.55%（+12.26 个百分点），Mean@32 从 6.08% 提升至 9.68%（+3.60 个百分点）。在更高预算 $C = 16 \times Q$ 下，提升幅度依然显著。

**工具增强推理（Bamboogle/MuSiQue）**：Table 2 显示，在需要检索和推理的 Bamboogle 和 MuSiQue 数据集上，Dr. GRPO+VIP 和 RLOO+VIP 均一致提高 EM、F1@5 和 Precision@5。例如，Dr. GRPO+VIP 在 Bamboogle 上将 EM 从 20.0% 提升至 23.2%（+3.2 个百分点），同时 F1@5 和 Precision@5 分别提升 0.051 和 0.060。RLOO+VIP 在 Bamboogle 上的 EM 从 10.4% 提升至 17.6%（+7.2 个百分点），提升幅度更为显著。

### 消融分析

Table 3 的消融实验系统解构了 VIP 各组件的贡献。以 RLOO 为基线（AIME24 Pass@32: 18.29%），逐步叠加组件：
- RLOO + GP + Inverse Acc：20.10%
- RLOO + GP + Inverse Var：22.67%
- RLOO + Ridge + Allocation：23.74%
- RLOO + VIP（完整方法）：**30.55%**

关键发现：
1. **GP 预测器优于 Ridge 回归**：GP+Inverse Var（22.67%）显著高于 Ridge+Allocation（23.74% 中包含分配优化，但预测器较弱），说明准确的概率预测是有效分配的前提；
2. **方差最小化分配优于启发式分配**：GP+Inverse Var（22.67%）与完整 VIP（30.55%）的差距（+7.88 个百分点）表明，基于方差最小化的凸优化分配远优于简单的逆方差启发式；
3. **AIME25 上趋势一致**：RLOO+VIP 的 Pass@32 达 26.54%，相较基线 RLOO（17.04%）提升 9.50 个百分点，所有消融变体均低于完整 VIP。

### 预测精度验证

Figure 3 展示了 GP 预测器、移动平均和 Ridge 回归在训练过程中的成功概率预测 MAE。在两个模型规模（1.5B 和 7B）上，GP 预测器的 MAE 持续低于两个基线方法，且随着训练推进，优势保持稳定。这验证了 GP 在嵌入空间中利用核函数捕捉提示间相似性的有效性——相似的提示倾向于具有相似的成功概率，GP 的后验更新机制能够有效利用这一结构信息。

### 计算开销

Table 4 给出了单 GPU 上的墙钟时间分解。VIP 的额外计算组件（核矩阵计算、GP 训练/预测、分配优化）总计约 41.4 秒，而模型相关操作（前向传播、采样等）在 1.5B 模型上约 3695 秒，在 7B 模型上约 4977 秒。VIP 的额外开销仅占整体 RL 训练时间的 **1.12%**（1.5B）和 **0.83%**（7B），几乎可以忽略不计。这一极低开销源于：GP 仅在低维嵌入空间上运行，核矩阵规模受限于 mini-batch 大小；分配优化是凸问题，可高效求解。

### 训练动态

Figure 6 和 Figure 7 展示了训练过程中的平均优势和平均回报曲线，以及 AIME 评估指标随训练步数的变化。GRPO+VIP 的平均优势在训练早期即显著高于 GRPO，且保持稳定增长，表明方差降低使梯度信号更可靠，加速了策略改进。在评估指标上，GRPO+VIP 在 best@32、maj@32 和 mean 准确率上均持续优于 GRPO，且优势随训练步数扩大。

### 失败模式与局限

1. **二元奖励假设**：理论推导和主实验均基于二元奖励 $\{-1, 1\}$，作者在附录中展示了扩展到连续奖励的方法，但该扩展的有效性未在实验中验证；
2. **GP 可扩展性**：当前实验中 mini-batch 规模有限，GP 推断开销极小。若应用于极大提示集（如数十万级别），核矩阵求逆的 $\mathcal{O}(|\mathcal{B}_t|^3)$ 复杂度可能成为瓶颈，需进一步采用稀疏 GP 或诱导点方法；
3. **RLVR 特化**：VIP 依赖奖励的可验证性和确定性，直接扩展到 RLHF 中带噪声的人类偏好奖励模型需要额外设计，例如对奖励噪声建模或调整方差公式；
4. **统计假设验证**：Table 5 和 Table 6 展示了统计独立性检验的全局 p 值（L2 范数），在训练初期 p 值较高（0.73-0.79），训练中期下降至 0.11-0.21，表明独立性假设在训练后期可能部分违反，但作者认为对实际性能影响有限。

### 需要人工验证的要点

- 连续奖励扩展的实验验证：文中提及但未提供实验结果，若需引用该扩展的有效性，需查阅附录并自行判断理论推导的完备性；
- 更大规模提示集上的可扩展性：当前实验的 mini-batch 规模未公开具体数值，若需评估 GP 在大规模场景下的瓶颈，需根据实际 batch size 估算核矩阵规模。

## 方法谱系与知识库定位

### 核心瓶颈与贡献定位

现有群体策略优化方法（如 GRPO、Dr. GRPO、RLOO）在可验证奖励（RLVR）设定下，对每个训练提示分配**固定数量的推广（rollouts）**。这种均匀分配策略导致采样效率低下和梯度方差大，因为许多提示信息量低（成功概率接近 0 或 1），无法贡献有效梯度信号。VIP 的核心创新在于**将计算预算从“均匀分配”转向“方差感知分配”**：利用高斯过程在线预测每个提示的成功概率，通过理论分析揭示梯度方差与成功概率 $p$ 的函数关系，并将分配问题形式化为一个可在总预算约束下精确求解的凸优化问题。

### 与基线方法的本质差异

- **GRPO / Dr. GRPO / RLOO（均匀固定推广）**：标准组内优势估计方法，使用固定的每提示推广数，不区分提示的信息量差异。其梯度方差由 Proposition 4.2 和 4.3 给出，分别为 $\mathrm{Var}(\tilde{G}) = \frac{(n-1)}{n^2} 4 \sigma_Z^2 p (1-p)$（Dr. GRPO）和 $\mathrm{Var}(\tilde{G}) = \frac{1}{n-1} 4 \sigma_Z^2 p (1-p)$（RLOO）。当 $p$ 接近 0 或 1 时，方差趋近于零，此时分配更多推广的边际收益极低。

- **逆准确率分配（Inverse-accuracy allocation）**：基于运行准确率反比分配推广，是一种启发式策略，缺乏理论保证。Figure 2 显示其分配曲线与 VIP 的方差最小化分配存在显著偏差，尤其在中等难度提示上分配不足。

- **逆方差分配（Inverse-variance allocation）**：基于运行方差反比分配推广，虽与方差相关，但未考虑推广数 $n$ 对梯度方差的非线性影响（Dr. GRPO 中方差随 $n$ 以 $\frac{n-1}{n^2}$ 衰减），因此无法达到理论最优。

### 适用边界与假设约束

VIP 的设计和理论分析基于以下关键假设，超出这些边界时需谨慎：

1. **可验证奖励设定**：奖励是确定且可自动验证的二元变量（$\{-1, 1\}$）。作者虽在附录中展示了扩展到连续奖励的方法，但主实验和理论均围绕二元奖励展开。直接扩展到带噪声的奖励模型（如 RLHF 中的人类偏好奖励）仍需额外设计。

2. **KL 正则化项设为零**（Assumption 3.1）：在 RLVR 设定下，奖励信号足够强，无需 KL 约束来防止策略偏离。若需引入 KL 正则化，梯度方差的推导需要重新进行。

3. **统计独立性假设**：Proposition 4.2 和 4.3 的方差推导假设不同推广间的梯度估计统计独立。作者通过统计检验验证了该假设在实验中近似成立（Table 5、Table 6 中的全局 p 值随训练进行而下降但未完全拒绝）。

4. **嵌入空间平滑性**：高斯过程预测器依赖 RBF 核在嵌入空间中捕捉提示间的相似性。若提示嵌入无法有效反映难度相似性，预测精度将下降。

### 已知局限与开放问题

**计算可扩展性**：高斯过程推断需要计算核矩阵及其逆，对于极大提示集（如数十万级别）可能存在可扩展性瓶颈。当前实验中，VIP 的额外计算开销极小（1.5B 模型仅占 1.12%，7B 模型仅占 0.83%，见 Table 4），但在更大规模场景下需验证。

**奖励分布扩展**：能否在更一般的奖励分布（例如多项分布或连续评分）下，不依赖于 GP 扩展而保持分配效率？当前框架的方差分析依赖二元奖励的简洁形式，扩展到一般分布可能需要不同的方差建模方式。

**与解码策略的协同**：能否将 VIP 的预测-分配框架与自回归解码策略（如多数投票、best-of-N）或提示难度选择相结合，实现更高效的训练？当前框架仅在给定 mini-batch 内分配推广，未涉及提示的选择策略。

**RLHF 场景迁移**：如何将 VIP 扩展到非可验证的、人类偏好奖励的 RLHF 场景？这需要解决奖励噪声建模和预测器设计两个核心挑战。

## 原文 PDF

![[obsidian-vault/paperPDFs/ICLR_2026/Adaptive_Rollout_Allocation_for_Online_Reinforcement_Learning_with_Verifiable_Rewards.pdf]]
