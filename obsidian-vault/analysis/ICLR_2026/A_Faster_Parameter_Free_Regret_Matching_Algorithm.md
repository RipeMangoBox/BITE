---
title: "A Faster Parameter-Free Regret Matching Algorithm"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Faster_Parameter_Free_Regret_Matching_Algorithm.pdf
aliases:
- MISPRMMS
- FPFRMA
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/game_theory
core_operator: "SPRM+ 中支持 O(1/T) 收敛速度的步长范围依赖于累积遗憾 1-范数的下界 R。通过自适应地调整决策空间来单调递增 R，可以同时实现无参数性质和 O(1/T) 收敛。"
primary_logic: "提出自适应遗憾域（ARD）技术，在每次迭代中动态调整决策空间，确保累积遗憾 1-范数的下界单调递增，从而在无需调参的情况下达到 O(1/T) 的理论收敛速度。"
claims:
- "MI-SPRM+ 保留了无参数性质，同时实现了 O(1/T) 的理论收敛速度。"
- "MI-SPRM+ 采用自适应遗憾域（ARD）技术，通过调整决策空间确保累积遗憾 1-范数的下界单调递增。"
- "SPRM+ 的收敛速度随步长 η 变化显著，在 10^5 次迭代后，SPRM+(η=0.1) 的对偶间隙比 SPRM+(η=0.01) 和 SPRM+(η=1) 分别小 10 倍和 5 倍。"
- "MI-SPRM+ 在所有测试游戏中经验性地达到了 O(1/T) 收敛速度。"
---

# A Faster Parameter-Free Regret Matching Algorithm

> [!tip] 核心洞察
> 提出自适应遗憾域（ARD）技术，在每次迭代中动态调整决策空间，确保累积遗憾 1-范数的下界单调递增，从而在无需调参的情况下达到 O(1/T) 的理论收敛速度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种更快的无参数遗憾匹配算法 |
| 英文题名 | A Faster Parameter-Free Regret Matching Algorithm |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JLllvi7dsg) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/game_theory |
| Method | Monotone Increasing Smooth Predictive Regret Matching+ (MI-SPRM+) |
| Dataset | 3x3 两人零和 NFG（SPRM+ 原始论文所用）, 随机生成两人零和 NFG（高斯分布，均值 0，标准差 100）, 标准 EFG 基准（Kuhn Poker, Leduc Poker, Liar's Dice, Goofspiel）, HUNL Subgames (Subgame3, Subgame4) |

> [!tip] 效果简介
> - 3x3 两人零和 NFG（SPRM+ 原始论文所用） 上，对偶间隙 为 2.6e-5，对比 SPRM+(η=0.01): 3.9e-4; SPRM+(η=0.1): 4.0e-5; SPRM+(η=1): 2.1e-4，变化 相比最佳 SPRM+ 基线降低约 35%。
> - 随机生成两人零和 NFG（高斯分布，均值 0，标准差 100） 上，对偶间隙 为 优于所有基线，对比 SPRM+, OGDA, OMWU, DS-OptMD, RM+, PRM+，变化 MI-SPRM+ 实现 92% 的对偶间隙降低（相对于 SPRM+）。
> - 标准 EFG 基准（Kuhn Poker, Leduc Poker, Liar's Dice, Goofspiel） 上，收敛速度 为 O(1/T) 或更快，对比 SPCFR+, PCFR+, CFR+, DCFR，变化 MI-SPCFR+ 在 8 个测试游戏中的全部游戏中显著优于 SPCFR+。

## 概述

该工作针对博弈论中遗憾最小化算法的核心瓶颈：现有的平滑 RM+ 变体（如 SPRM+）虽然理论上能达到 O(1/T) 的收敛速度，但失去了无参数性质，其性能对步长 η 高度敏感，需要大量调参。SPRM+ 中支持 O(1/T) 收敛的步长范围依赖于累积遗憾 1-范数的下界 R，而该下界在标准算法中为固定常数，导致算法无法自动适应不同游戏环境。

核心洞察在于：通过自适应地调整决策空间来单调递增 R，可以同时实现无参数性质和 O(1/T) 收敛。基于此，论文提出单调递增平滑预测性遗憾匹配+（MI-SPRM+），其核心技术是自适应遗憾域（ARD）——在每次迭代中动态调整决策空间，确保累积遗憾 1-范数的下界单调递增，从而在无需调参的情况下达到 O(1/T) 的理论收敛速度。MI-SPRM+ 保留了 RM+ 和 PRM+ 的无参数性质（算法行为与 η 无关），同时继承了 SPRM+ 的平滑投影和预测性更新机制。

实验结果表明，MI-SPRM+ 在所有测试游戏中经验性地达到了 O(1/T) 收敛速度。在 3×3 两人零和 NFG 中，迭代 10^5 次后 MI-SPRM+ 的对偶间隙（2.6e-5）比最佳 SPRM+ 基线（η=0.1, 4.0e-5）降低约 35%，比 SPRM+(η=0.01) 和 SPRM+(η=1) 分别小 10 倍和 5 倍。在随机生成的高斯分布 NFG（std=100）中，MI-SPRM+ 实现了相对于 SPRM+ 92% 的对偶间隙降低。在标准扩展式博弈（EFG）基准（Kuhn Poker, Leduc Poker, Liar's Dice, Goofspiel）的 8 个测试游戏中，MI-SPCFR+（MI-SPRM+ 的 EFG 版本）在所有游戏中显著优于 SPCFR+。在大型 HUNL 子游戏中，MI-SPCFR+ 的最终可剥削性（Subgame3: 3.10e-4, Subgame4: 2.70e-4）一致优于 CFR+、PCFR+、SPCFR+ 和 PDCFR+ 等所有基线。

## 背景与动机

在在线学习与博弈论的交汇处，遗憾最小化（Regret Minimization）是求解纳什均衡的核心技术。然而，现有算法在**收敛速度**与**无参数性质**之间存在根本性张力。标准 RM+ 及其预测性变体 PRM+ 虽无需调参（parameter-free），但其理论收敛速度仅为 $O(1/\sqrt{T})$。平滑 RM+ 变体 SPRM+ 通过引入平滑投影，将理论收敛速度提升至 $O(1/T)$，但代价是失去了无参数性质——其性能对步长 $\eta$ 高度敏感，需要大量手动调参才能获得良好效果。实验表明，在 $10^5$ 次迭代后，SPRM+($\eta=0.1$) 的对偶间隙比 SPRM+($\eta=0.01$) 和 SPRM+($\eta=1$) 分别小 10 倍和 5 倍，这凸显了步长选择对算法性能的决定性影响。

**核心瓶颈**在于：SPRM+ 实现 $O(1/T)$ 收敛所需的步长范围依赖于累积遗憾 1-范数的下界 $R$（即决策空间的下界）。具体而言，SPRM+ 的收敛条件为 $\eta \leq R \sqrt{1 / [8D(2L^2 + 4DL^2 + 4DP^2)]}$，其中 $L$ 和 $P$ 分别为损失梯度的 Lipschitz 常数和有界范数。这意味着 $R$ 越小，允许的 $\eta$ 上限越紧，算法越容易因步长选择不当而偏离理论收敛率。然而，$R$ 的合理取值依赖于未知的 $L$ 和 $P$，这正是 SPRM+ 无法同时实现无参数与快速收敛的根源。

**因果机制**：SPRM+ 中，$R$ 是固定的常数，导致算法必须依赖调参来确定合适的 $\eta$。若 $R$ 设置过小，收敛条件难以满足；若 $R$ 设置过大，虽可放宽 $\eta$ 范围，但会引入不必要的保守性。本文的核心洞察在于：**通过自适应地调整决策空间，使累积遗憾 1-范数的下界 $R$ 单调递增，可以同时实现无参数性质和 $O(1/T)$ 收敛**。具体地，提出自适应遗憾域（Adaptive Regret Domain, ARD）技术，在每次迭代中动态调整决策空间的下界 $R^t$，确保其单调递增。这使得算法无需预设 $R$ 或调参 $\eta$（固定 $\eta=1$），即可自动满足收敛条件。

**证据强度**：论文声称 MI-SPRM+ 是首个同时实现无参数性质和 $O(1/T)$ 理论收敛的 RM 变体，这基于 ARD 技术的理论推导。然而，该声称的置信度需谨慎评估：论文提供了 SPRM+ 步长敏感性的定量证据（对偶间隙相差 10 倍），以及 MI-SPRM+ 在 3x3 两人零和 NFG 中达到 $2.6\times 10^{-5}$ 对偶间隙的实验结果，这支持了其经验收敛速度。但理论收敛的严格证明依赖于加权社会遗憾界，其推导细节需进一步验证。此外，论文未提供 ARD 技术中 $R^{t+1}$ 更新规则的完整收敛性分析，该规则仅通过检查一个条件来决定是否递增 $R$，其最优性和充分性尚需更严格的理论支撑（此点需手动验证论文附录中的证明）。

## 核心创新

本文的核心贡献是提出了**单调递增平滑预测性遗憾匹配+ (MI-SPRM+)**，这是首个同时实现**无参数**性质和 **O(1/T)** 理论收敛速度的遗憾匹配（RM）变体。其关键创新在于解决了现有平滑 RM+ 变体（如 SPRM+）中一个根本性的权衡：SPRM+ 虽然达到了 O(1/T) 的收敛速度，但失去了无参数性质，其性能对步长 η 高度敏感。实验证据表明，在 10^5 次迭代后，SPRM+(η=0.1) 的对偶间隙比 SPRM+(η=0.01) 和 SPRM+(η=1) 分别小 10 倍和 5 倍，凸显了调参的必要性和难度。

**核心洞察与因果机制：** 瓶颈在于 SPRM+ 中支持 O(1/T) 收敛的步长范围依赖于累积遗憾 1-范数的下界 R。具体地，SPRM+ 的收敛条件为 `η ≤ R * sqrt(1/(8D(2L²+4DL²+4DP²)))`，其中 L 和 P 分别是损失梯度的 Lipschitz 常数和 L1 范数上界。这意味着，为了实现理论上的快速收敛，R 必须足够大，且是一个需要提前设定的常数。MI-SPRM+ 通过引入**自适应遗憾域（Adaptive Regret Domain, ARD）**技术，在每次迭代中动态调整决策空间的下界 R^t，确保其单调递增，从而在无需预设 R 值（即无参数）的情况下，自动满足 O(1/T) 收敛的条件。

**改变的关键插槽：**
1.  **决策空间下界 R：** 从 SPRM+ 中的**固定常数**变为 MI-SPRM+ 中通过 ARD 技术**自适应单调递增的 R^t**。这是实现无参数化的核心改变。
2.  **步长 η：** 从 SPRM+ 中**需要手动调参**变为 MI-SPRM+ 中的**无参数**（算法行为与 η 无关，固定为 1）。MI-SPRM+ 继承了 RM+ 和 PRM+ 的无参数性质。

**核心算法模块：** MI-SPRM+ 的流水线由三个关键模块构成：
1.  **自适应遗憾域 (ARD)：** 核心创新模块。通过一个条件判断式 `R^{t+1} = R^t + 1` 当 `||F^t(θ^t) - F^{t-1}(θ^{t-1})||_2^2 - (B_ψ(θ̂^t, θ^{t-1}) + B_ψ(θ̂^t, θ^t))/2 > 0` 时递增 R，否则保持不变。这确保了 R^t 单调递增至一个常数，从而在理论上保证 O(1/T) 收敛。
2.  **预测性更新：** 使用上一轮反馈 `F^{t-1}(θ^{t-1})` 作为当前轮的预测，加速收敛过程。
3.  **平滑投影：** 在非负象限的子集 `R_{≥R^t}^{|A_i|}` 中进行更新，保证了算法更新的稳定性。

**证据强度与实验支撑：** 核心创新点（无参数 + O(1/T) 收敛）的证据强度很高（置信度 0.95）。在 3x3 两人零和正规形式博弈（NFG）中，MI-SPRM+ 在 10^5 次迭代后的对偶间隙为 2.6e-5，优于最佳 SPRM+ 基线（η=0.1, 4.0e-5）约 35%。在随机生成的高斯分布（std=100）NFG 中，MI-SPRM+ 相对于 SPRM+ 实现了 92% 的对偶间隙降低。在标准扩展式博弈（EFG）基准测试（如 Kuhn Poker, Leduc Poker）以及大型 HUNL 子游戏中，其对应的扩展式版本 MI-SPCFR+ 在所有测试游戏中均显著优于 SPCFR+ 等基线。

**失败模式与局限性：** 尽管 MI-SPRM+ 在理论上和经验上均达到了 O(1/T) 收敛，但其运行时约为 SPRM+ 的 1.5 倍（尽管每次迭代的理论复杂度相同，均为 `O(∑|A_i| log|A_i|)`）。此外，在三人一般和 NFG 中，所有算法（包括 MI-SPRM+）均未能成功学习纳什均衡，表明该方法在多人一般和场景下的有效性有待验证。论文也指出，MI-SPRM+ 隐式学习了 Lipschitz 常数 L 和 P，但未显式利用优化领域中的自适应学习未知 Lipschitz 常数技术，这可能是未来的改进方向。

## 整体框架

MI-SPRM+（Monotone Increasing Smooth Predictive Regret Matching+）的整体 pipeline 围绕一个核心因果机制构建：现有平滑 RM+ 变体（如 SPRM+）虽然理论上能达到 O(1/T) 收敛速度，但其步长 η 的有效范围依赖于累积遗憾 1-范数的下界 R——这是一个需要手动调参的未知量，使得算法失去了无参数性质。MI-SPRM+ 通过引入自适应遗憾域（Adaptive Regret Domain, ARD）技术，在每次迭代中动态调整决策空间的下界 R，使其单调递增并最终收敛到一个常数，从而在无需调参（η 固定为 1）的情况下同时实现无参数性质和 O(1/T) 的理论收敛速度。

**模块关系与输入输出流**：

1. **预测性更新模块**：在迭代 t，使用上一轮（t-1）的反馈作为当前轮的预测。具体地，PRM+ 风格利用 `F_i^{t-1}(θ^{t-1})` 作为预测梯度，输入到 Bregman 散度正则化的优化问题中。

2. **平滑投影模块**：与 SPRM+ 在非负象限的子集 `R_{≥R}^{|A_i|}` 中更新不同，MI-SPRM+ 的投影空间边界 R 是动态变化的。在迭代 t，算法在 `R_{≥R^t}^{|A_i|}` 中求解以下优化问题（η=1）：
   ```
   θ_i^t ∈ argmin_{θ_i ∈ R_{≥R^t}^{|A_i|}} { ⟨ -F_i^{t-1}(θ^{t-1}), θ_i ⟩ + B_ψ(θ_i, θ̂_i^t) }
   ```
   其中 `B_ψ` 是欧几里得 Bregman 散度，`θ̂_i^t` 是预测点。解得的 `θ_i^t` 通过归一化 `x_i^t = θ_i^t / ‖θ_i^t‖_1` 输出为策略。

3. **ARD 自适应模块**：在迭代 t 结束后，根据以下规则更新 R：
   ```
   R^{t+1} = R^t + 1  if  ‖F^t(θ^t) - F^{t-1}(θ^{t-1})‖₂² - (B_ψ(θ̂^t, θ^{t-1}) + B_ψ(θ̂^t, θ^t))/2 > 0
   R^{t+1} = R^t       else
   ```
   该条件检测当前 R 是否足以抑制梯度变化：若梯度变化超过 Bregman 散度均值，则增大 R 以收紧投影空间。理论证明（Lemma A.1 及后续引理）表明，R^t 单调递增并在有限步内收敛到常数（当 `R^{t-1} ≥ 2√C_2` 时停止增长），从而保证加权平均策略 `x̂^T = (∑ R^t x^t) / (∑ R^t)` 以 O(1/T) 速率收敛到近似纳什均衡。

**关键差异**：与 SPRM+ 的固定决策空间相比，MI-SPRM+ 的 ARD 模块隐式学习了 Lipschitz 常数 L 和梯度范数上界 P（通过 R^t 的终值随游戏维度 D 和 payoff 标准差增加而增加体现），而 SPRM+ 需要用户手动设定 η 来适配这些未知量。实验证据显示，SPRM+ 的收敛速度对 η 高度敏感：在 10^5 次迭代后，SPRM+(η=0.1) 的对偶间隙比 SPRM+(η=0.01) 和 SPRM+(η=1) 分别小 10 倍和 5 倍，而 MI-SPRM+ 在所有测试游戏中经验性地达到了 O(1/T) 收敛，无需任何调参。

**运行时代价**：尽管理论每次迭代复杂度相同（O(∑|A_i| log|A_i|)），MI-SPRM+ 的实际运行时约为 SPRM+ 的 1.5 倍（例如在 dim=100 的 NFG 中，MI-SPRM+ 0.2398 分钟 vs SPRM+ 0.1562 分钟），这主要来自 ARD 条件判断中额外的范数计算和 Bregman 散度评估。

## 核心模块与公式推导

### 算法背景与瓶颈

现有的平滑 RM+ 变体（如 SPRM+）虽然理论上达到了 O(1/T) 的收敛速度，但失去了无参数性质。其性能对步长 η 高度敏感——在 3×3 两人零和 NFG 中，经过 10^5 次迭代后，SPRM+(η=0.1) 的对偶间隙比 SPRM+(η=0.01) 和 SPRM+(η=1) 分别小 10 倍和 5 倍。SPRM+ 实现 O(1/T) 收敛的步长范围依赖于累积遗憾 1-范数的下界 R，具体条件为：

$$\eta \frac { D ( 2 L ^ { 2 } + 4 D L ^ { 2 } + 4 D P ^ { 2 } ) } { R ^ { 2 } } \leq \frac { 1 } { 8 \eta } \Rightarrow \eta \leq R \sqrt { \frac { 1 } { 8 D ( 2 L ^ { 2 } + 4 D L ^ { 2 } + 4 D P ^ { 2 } ) } }$$

其中 L 是损失梯度的 Lipschitz 常数，P 是损失梯度 L1 范数的上界，D 是动作空间维度。这个条件意味着 η 必须足够小，且与 R 成正比——但 R 是固定常数，导致算法无法适应不同游戏实例。

### MI-SPRM+ 核心机制：自适应遗憾域 (ARD)

MI-SPRM+ 的核心创新是自适应遗憾域（Adaptive Regret Domain, ARD）技术。其关键洞察是：通过动态调整决策空间，使累积遗憾 1-范数的下界 R^t 单调递增，从而同时实现无参数性质和 O(1/T) 收敛。

**MI-SPRM+ 更新规则**（η 固定为 1）：

$$\pmb{\theta}_i^t \in \underset{\pmb{\theta}_i \in \mathbb{R}_{\geq R^t}^{|\mathcal{A}_i|}}{\mathrm{argmin}} \left\{ \langle -\pmb{F}_i^{t-1}(\pmb{\theta}^{t-1}), \pmb{\theta}_i \rangle + \mathcal{B}_\psi(\pmb{\theta}_i, \pmb{\hat{\theta}}_i^t) \right\}, \quad \pmb{x}_i^t = \frac{\pmb{\theta}_i^t}{\lVert \pmb{\theta}_i^t \rVert_1}$$

其中 $\mathcal{B}_\psi$ 是 Bregman 散度（使用欧几里得范数平方的一半），$\pmb{F}_i^{t-1}$ 是累积遗憾向量，$\pmb{\hat{\theta}}_i^t$ 是预测项（使用上一轮反馈 $\pmb{F}_i^{t-1}(\pmb{\theta}^{t-1})$）。与 SPRM+ 的固定 R 不同，MI-SPRM+ 使用随时间变化的 R^t。

**自适应 R 更新规则**：

$$R^{t+1} = \left\{ \begin{array}{ll} R^t + 1 & \mathrm{if~} \|F^t(\theta^t) - F^{t-1}(\theta^{t-1})\|_2^2 - \frac{\mathcal{B}_\psi(\hat{\theta}^t, \theta^{t-1}) + \mathcal{B}_\psi(\hat{\theta}^t, \theta^t)}{2} > 0, \\ R^t & \mathrm{else} \end{array} \right.$$

这个更新规则的核心逻辑是：当相邻两步的累积遗憾变化量（由 $\|F^t(\theta^t) - F^{t-1}(\theta^{t-1})\|_2^2$ 衡量）超过 Bregman 散度的平均值时，说明当前下界 R^t 不足以约束算法行为，需要增加 1。理论分析证明，R^t 会单调递增到一个常数（当 $R^{t-1} \geq 2\sqrt{C_2}$ 时停止增长），其中 $C_2$ 是依赖于 L、P、D 的常数。

### 收敛速度与复杂度

MI-SPRM+ 的理论收敛速度为 O(1/T)，与 SPRM+ 相同，但无需调参。加权平均策略定义为：

$$\hat { \mathbf { x } } ^ { T } = \left( \sum _ { t = 1 } ^ { T } R^t \mathbf { x } ^ { t } \right) / \left( \sum _ { t = 1 } ^ { T } R ^ { t } \right)$$

在多人一般和 NFG 中，当所有玩家使用 MI-SPRM+ 时，加权社会遗憾界为：

$$\frac { \sum _ { t = 1 } ^ { T } R ^ { t } \langle \ell ^ { t } , \mathbf { x } ^ { t } - \mathbf { x } \rangle } { \sum _ { t = 1 } ^ { T } R ^ { t } } \leq O(1)$$

每次迭代的理论复杂度为 $O\left( \sum_{i \in \mathcal{N}} |\mathcal{A}_i| \log |\mathcal{A}_i| \right)$，与 SPRM+ 和 DS-OptMD 相同。然而，实际运行时 MI-SPRM+ 约为 SPRM+ 的 1.5 倍（例如在维度 100 时，MI-SPRM+ 为 0.2398 分钟，SPRM+ 为 0.1562 分钟），这主要是由于自适应 R 更新带来的额外计算开销。

### 关键公式变量含义

| 符号 | 含义 |
|------|------|
| $\pmb{\theta}_i^t$ | 玩家 i 在迭代 t 的累积遗憾向量 |
| $\pmb{x}_i^t$ | 玩家 i 在迭代 t 的策略（$\pmb{\theta}_i^t$ 的 L1 归一化） |
| $\pmb{F}_i^t(\pmb{\theta}^t)$ | 迭代 t 的累积遗憾（负梯度之和） |
| $\mathcal{B}_\psi(\cdot, \cdot)$ | 欧几里得 Bregman 散度（$\|\cdot - \cdot\|_2^2 / 2$） |
| $R^t$ | 迭代 t 的决策空间下界（累积遗憾 1-范数的最小值） |
| $\eta$ | 步长（MI-SPRM+ 中固定为 1） |
| $L$ | 损失梯度的 Lipschitz 常数 |
| $P$ | 损失梯度 L1 范数的上界 |
| $D$ | 动作空间维度（$|\mathcal{A}_i|$） |

## 实验与分析

### 主要收敛结果

MI-SPRM+ 的核心实验验证了其作为首个无参数 RM 变体实现 O(1/T) 理论收敛速度的宣称。实验覆盖了从简单规范式博弈到大规模扩展式博弈的多个基准。

在 SPRM+ 原始论文所用的 3×3 两人零和 NFG 中（Figure 1），MI-SPRM+ 在 10^5 次迭代后的对偶间隙为 2.6e-5，显著优于 SPRM+ 在不同步长下的表现（η=0.01: 3.9e-4; η=0.1: 4.0e-5; η=1: 2.1e-4）。这一结果有两个关键含义：首先，SPRM+ 的收敛速度对步长 η 高度敏感——最佳步长 (η=0.1) 与次优步长 (η=0.01) 之间的对偶间隙差距达 10 倍，这直接验证了该方法的瓶颈在于参数敏感性；其次，MI-SPRM+ 无需调参就超越了所有调参后的 SPRM+ 实例，证实了自适应遗憾域（ARD）技术确实消除了对步长 η 的依赖。

在更广泛的随机生成两人零和 NFG 中（Figure 2，高斯分布标准差 100），MI-SPRM+ 实现了相对于 SPRM+ 的 92% 对偶间隙降低。该实验还包含了 OGDA、OMWU、DS-OptMD 等基线。值得注意的是，DS-OptMD 作为另一种无参数 O(1/T) 算法，其经验收敛速度慢于 MI-SPRM+，这验证了分析中指出的“DS-OptMD 理论上 O(1/T) 但经验收敛慢”的失败模式。MI-SPRM+ 在标准差为 10 和 1 的 NFG 中（Figure 4, 5）也一致优于所有基线，表明其对 payoff 矩阵的尺度具有鲁棒性。

![[assets/figures/papers/iclr26_0002_JLllvi7dsg_A_Faster_Parameter-Free_Regret_Matching_Algorith/figures/002_Figure_2.jpg]]
*Figure 2: Convergence rates of different algorithms in randomly generated two-player zero-sum NFGs, where payoff matrices are sampled from a Gaussian distribution with mean 0 and standard deviation 100. Note that the value of η only involves the performance of $\mathrm { S P R M ^ { + } }$ and OGDA as other algorithms are parameter-free algorithms*

在扩展式博弈（EFG）基准中（Figure 3），MI-SPCFR+（MI-SPRM+ 的 CFR 扩展）在全部 8 个标准测试游戏（Kuhn Poker, Leduc Poker, Liar's Dice, Goofspiel）中显著优于 SPCFR+。在 HUNL 子游戏基准中（Table 2），MI-SPCFR+ 的最终可剥削性（Subgame3: 3.10e-4, Subgame4: 2.70e-4）一致低于所有基线（CFR+, PCFR+, SPCFR+, PDCFR+），最低值在 3.63e-4 到 5.14e-4 之间。这一结果的关键在于，HUNL 子游戏是实际扑克 AI 部署中的典型场景，MI-SPRM+ 的改进在此具有实际应用价值。

![[assets/figures/papers/iclr26_0002_JLllvi7dsg_A_Faster_Parameter-Free_Regret_Matching_Algorith/figures/022_Table_2.jpg]]
*Table 2: Final exploitability for the tested algorithms in HUNL Subgames. The lowest exploitability is highlighted in red*

### 消融与运行时分析

运行时分析（Table 1）揭示了 MI-SPRM+ 的主要代价：尽管理论每次迭代复杂度相同（O(∑|A_i| log|A_i|)），MI-SPRM+ 的运行时约为 SPRM+ 的 1.5 倍（例如，维度 100 时 0.2398 分钟 vs 0.1562 分钟）。这一开销源于 ARD 技术中 R^t 的自适应调整计算。DS-OptMD 的运行时介于两者之间（维度 100 时 0.1901 分钟）。这种运行时增加是 ARD 机制的可接受代价——它在每次迭代中需要计算 F^t(θ^t) 与 F^{t-1}(θ^{t-1}) 的 L2 距离以及两个 Bregman 散度，以决定是否递增 R^t。

![[assets/figures/papers/iclr26_0002_JLllvi7dsg_A_Faster_Parameter-Free_Regret_Matching_Algorith/figures/004_Table_1.jpg]]
*Table 1: Comparison of the runtime (in minutes) between $\mathbf { M I - S P R M ^ { + } } \mathrm { S P R M ^ { + } }$ , and DS-OptMD for randomly generated two-player zero-sum NFGs. It is important to highlight that theoretical periteration complexity for MI-SPRM+, SPRM+, and DS-OptMD remains $\begin{array} { r } { \breve { O } \left( \breve { \sum } _ { i \in \mathcal { N } } | \mathcal { A } _ { i } | \log | \mathcal { A } _ { i } | \right) } \end{array}$

Figure 7 展示了 R^t 的动态变化：在不同标准差的高斯 NFG 中，R^t 均单调递增至某个常数后收敛。这一行为直接验证了 ARD 的核心机制——确保累积遗憾 1-范数的下界单调递增。R^t 的最终值随游戏维度 D 和 payoff 矩阵标准差增加而增加（例如，标准差 100 的 NFG 中 R^t 最终值高于标准差 1 的 NFG），表明 MI-SPRM+ 隐式学习了 Lipschitz 常数 L 和梯度范数上界 P，这正是其实现无参数性质的因果机制。

### 失败模式与边界条件

在三人一般和 NFG 中（Figure 6），所有算法（包括 MI-SPRM+）均未能成功学习纳什均衡。这是一个重要的边界条件：MI-SPRM+ 的 O(1/T) 收敛保证仅适用于两人零和博弈，在多人一般和场景中，加权社会遗憾界虽为 O(1)，但这并不意味着策略收敛到 NE。该实验揭示了 RM 类算法在多人一般和博弈中的固有局限。

另一个值得注意的失败模式出现在多人 EFG 中：当使用二次平均和交替更新时（Figure 9），所有算法的性能可能显著下降。例如，在 3 人和 4 人 Kuhn Poker 中，下降幅度超过 1000 倍。这表明 MI-SPRM+ 的收敛保证可能对更新顺序和策略平均方式敏感，需要进一步的理论分析来理解这一现象。

### 证据强度评估

主要结果的证据强度较高（置信度 0.85-1.0），因为实验覆盖了多种博弈类型、多个随机种子，且与多个基线进行了公平比较。运行时分析的数据来自 10 次独立运行（Table 1 中标注了标准差），统计上可靠。但需注意，EFG 实验（Figure 3, 9）的具体数值在提供的分析中未完全给出，仅以“显著优于”描述，这需要手动验证原始论文中的具体数值。多人一般和 NFG 的失败模式证据充分（置信度 1.0），但“所有算法均未能成功学习 NE”这一结论的严格性依赖于 NE 的近似精度阈值，原文未明确给出该阈值。

## 方法谱系与知识库定位

MI-SPRM+ 填补了遗憾匹配（RM）算法族中长期存在的一个空白：在无参数（parameter-free）与快速收敛（O(1/T)）之间取得统一。其核心贡献——自适应遗憾域（ARD）——直接解决了平滑 RM+ 变体（SPRM+）的瓶颈：SPRM+ 虽然理论上达到了 O(1/T) 收敛，但其步长 η 的选择范围依赖于累积遗憾 1-范数的下界 R，而 R 是未知的。这导致 SPRM+ 的性能对 η 高度敏感——在 3×3 两人零和 NFG 中，经过 10⁵ 次迭代后，SPRM+(η=0.1) 的对偶间隙分别比 SPRM+(η=0.01) 和 SPRM+(η=1) 小 10 倍和 5 倍（Figure 1）。MI-SPRM+ 通过 ARD 在每次迭代中动态调整决策空间，使 R 单调递增至一个常数，从而在 η=1 固定（即无参数）时仍能保证 O(1/T) 的理论收敛。

**与基线的谱系关系**：MI-SPRM+ 位于 RM+ → PRM+ → SPRM+ 的发展线上。RM+ 和 PRM+ 是无参数的但仅达到 O(1/√T) 收敛；SPRM+ 通过将更新限制在非负象限的子集 ℝ_{≥R}^{|A_i|} 中实现了 O(1/T)，但失去了无参数性质。MI-SPRM+ 将 SPRM+ 的固定 R 替换为自适应单调递增的 R^t，本质上是将 SPRM+ 中需要手动选择的超参数 η 与 R 之间的耦合关系解耦，转而由算法自动学习。与另一条无参数 O(1/T) 路线 DS-OptMD 相比，MI-SPRM+ 的经验收敛速度更快（在随机生成 NFG 中相对 SPRM+ 实现 92% 的对偶间隙降低），且理论每次迭代复杂度相同（O(∑|A_i| log|A_i|)），但实际运行时约为 SPRM+ 的 1.5 倍（Table 1），这是 ARD 自适应调整带来的计算开销。

**适用边界**：MI-SPRM+ 及其扩展式博弈版本 MI-SPCFR+ 在两人零和场景中表现优异——在 3×3 NFG 中，MI-SPRM+ 的对偶间隙（2.6e-5）低于所有调参后的 SPRM+ 变体；在 HUNL 子游戏中，MI-SPCFR+ 的最终可剥削性（Subgame3: 3.10e-4, Subgame4: 2.70e-4）一致优于 CFR+、PCFR+、SPCFR+ 和 PDCFR+（Table 2）。然而，在多人一般和 NFG 中，所有算法（包括 MI-SPRM+）均未能成功学习纳什均衡（Figure 6），这表明 ARD 机制本身无法解决多人非零和博弈中策略收敛的根本困难。此外，在多人 EFG 中使用二次平均和交替更新时，所有算法的性能可能下降超过 1000 倍（如 3 人和 4 人 Kuhn Poker），说明 MI-SPRM+ 的收敛保证依赖于特定的平均和更新调度。

**局限与开放问题**：
1. **参数学习的时间成本**：MI-SPRM+ 隐式学习 Lipschitz 常数 L 和 P（通过 R^t 的最终值随游戏维度 D 和 payoff 矩阵标准差增加而增加体现），但未显式利用优化领域中自适应学习未知 Lipschitz 常数的技术。如何在保持无参数性质的同时加速参数学习是一个开放问题。
2. **多人博弈的理论缺口**：MI-SPRM+ 在多人 EFG 中经验性地达到了 O(1/T) 或更快的收敛，但在多人 NFG 中却失败。这一矛盾源于扩展式博弈的特殊结构（如信息集、序列形式）还是实验设置差异？需要进一步的理论分析。
3. **扩展式博弈的理论保证**：虽然 MI-SPCFR+ 在经验上显著优于 SPCFR+，但论文未提供其 O(1/T) 收敛速度在扩展式博弈中的理论证明。这需要将 ARD 与 CFR 框架的收敛分析结合。
4. **运行时开销**：MI-SPRM+ 的 1.5 倍运行时开销在大型博弈中可能成为瓶颈。理论上每次迭代复杂度相同，但 ARD 的 R^t 更新条件计算（涉及 ‖F^t(θ^t) - F^{t-1}(θ^{t-1})‖₂² 与 Bregman 散度的比较）引入了额外的 O(d) 操作。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Faster_Parameter_Free_Regret_Matching_Algorithm.pdf

![[paperPDFs/ICLR_2026/A_Faster_Parameter_Free_Regret_Matching_Algorithm.pdf]]
