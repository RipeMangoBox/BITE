---
title: "A Fair Bayesian Inference through Matched Gibbs Posterior"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Fair_Bayesian_Inference_through_Matched_Gibbs_Posterior.pdf
project_link: null
code_link: null
aliases:
- MGP
- FBITMGP
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety
core_operator: "提出一种新的群体公平性度量——匹配偏差（matched deviation），并基于此构建匹配吉布斯后验（matched Gibbs posterior），通过可学习的匹配函数实现高效的MCMC采样，从而在贝叶斯框架下同时实现公平性和不确定性量化。"
primary_logic: "利用匹配函数将不同敏感组的输入空间对齐，使得匹配偏差成为Wasserstein距离的上界，从而将公平性约束转化为易于计算的惩罚项；通过吉布斯后验将惩罚项融入似然函数，使得标准MCMC算法可以直接用于公平后验推断，避免了对抗学习或二次复杂度计算。"
claims:
- "匹配偏差是Wasserstein距离的上界，且当总变差距离有界时存在匹配函数使匹配偏差有界。"
- "匹配吉布斯后验在多个真实数据集（ADULT, DUTCH, CRIME, CELEBA, CIVIL）上，在效用-公平性和不确定性-公平性权衡方面优于所有基线方法。"
- "匹配吉布斯后验的MCMC算法收敛良好，E-BFMI ≈ 1.646 > 0.3，且T的接受率在推荐范围[0.2, 0.5]内。"
- "匹配吉布斯后验在个体公平性指标（Consistency score）上也优于基线方法。"
---

# A Fair Bayesian Inference through Matched Gibbs Posterior

> [!tip] 核心洞察
> 利用匹配函数将不同敏感组的输入空间对齐，使得匹配偏差成为Wasserstein距离的上界，从而将公平性约束转化为易于计算的惩罚项；通过吉布斯后验将惩罚项融入似然函数，使得标准MCMC算法可以直接用于公平后验推断，避免了对抗学习或二次复杂度计算。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于匹配吉布斯后验的公平贝叶斯推断 |
| 英文题名 | A Fair Bayesian Inference through Matched Gibbs Posterior |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=sIjFXzEOOH) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety |
| Method | Matched Gibbs Posterior |
| Dataset | CRIME |

> [!tip] 效果简介
> - CRIME 上，Acc 为 最佳（Pareto前沿最优），对比 gapreg, reduction, adv, mean-field Gaussian VI，变化 显著优于所有基线。
> - CRIME 上，Nll 为 最佳，对比 gapreg, reduction, adv, mean-field Gaussian VI，变化 显著优于所有基线。
> - CRIME 上，brier 为 最佳，对比 gapreg, reduction, adv, mean-field Gaussian VI，变化 显著优于所有基线。

## 概要

本文针对现有公平性方法忽略模型不确定性（model uncertainty）量化的核心瓶颈，提出了一种新的贝叶斯推断框架——匹配吉布斯后验（Matched Gibbs Posterior）。核心思路是引入一种名为匹配偏差（matched deviation）的群体公平性度量，并将其作为惩罚项融入吉布斯后验的似然函数中，从而在无约束参数空间上直接使用标准MCMC算法进行后验采样，同时实现公平性与不确定性量化。

方法的关键洞察在于：匹配偏差通过一个可学习的匹配函数将不同敏感组的输入空间对齐，理论证明（Theorem 4.1和4.2）其是Wasserstein距离的上界，且当总变差距离有界时存在匹配函数使该偏差有界。这使得公平性约束转化为一个计算复杂度仅为O(n)且无需对抗学习的惩罚项，克服了现有变分推断方法（如平均场高斯VI）在处理IPM类公平性度量时面临的二次复杂度或对抗训练难题。

在ADULT、DUTCH、CRIME、CELEBA、CIVIL五个真实数据集上的实验表明，匹配吉布斯后验在效用-公平性和不确定性-公平性权衡方面均优于确定性基线（gapreg, reduction, adv）和变分贝叶斯基线（mean-field Gaussian VI）。具体地，在CRIME数据集上，该方法在所有四个评估指标（Acc, Nll, brier, Ece）的Pareto前沿上均表现最优；在CELEBA图像分类和CIVIL文本分类任务中，其准确率（Acc）和负对数似然（Nll）也大幅领先于基线方法。此外，该方法在个体公平性指标（Consistency score）上同样优于基线，且MCMC诊断指标（E-BFMI ≈ 1.646 > 0.3）和匹配函数接受率（在[0.2, 0.5]范围内）均表明采样算法收敛良好。



在机器学习公平性领域，现有方法主要聚焦于构建满足群体公平约束（如人口统计平等、等几率等）的单一预测模型。这类确定性方法的核心瓶颈在于：它们完全忽略了模型不确定性（model uncertainty）的量化。然而，对于高风险决策场景（如信贷审批、刑事司法），仅输出一个“公平”的点估计而不提供置信度信息，会严重削弱决策的鲁棒性和可信度。

从技术路径上看，现有公平性方法面临双重困境。首先，常用的公平性度量（如Wasserstein距离、总变差距离、Kolmogorov-Smirnov距离等）在计算上存在根本性障碍：它们要么需要对抗学习（adversarial learning）来逼近度量值，要么需要O(n²)的二次复杂度来计算经验分布距离。这使得将公平性约束融入贝叶斯推断框架变得极为困难——在约束参数空间上进行变分推断时，每个样本都需要重新计算对抗度量，实际不可行。其次，即使采用变分贝叶斯方法（如平均场高斯变分推断），在严格公平性水平下，从优化后的变分分布中采样的样本几乎全部违反公平性约束（例如在δ=0.22时，平均场高斯分布的公平样本比例降至0.000），说明标准变分推断无法有效生成公平的后验分布。

本文的核心动机正是填补这一缺口：在贝叶斯推断框架下同时实现公平性和不确定性量化，且不引入对抗学习或二次复杂度计算。为此，作者提出了一个关键创新——匹配偏差（matched deviation）。匹配偏差的核心思想是引入一个可学习的匹配函数T，将不同敏感组的输入空间对齐。具体而言，对于敏感组S=1的每个样本X₁，T将其映射到敏感组S=0的输入空间中，然后计算两组预测之间的平方差异期望：Δ_M(θ,T) := E_{X₁∼P₁} (‖f_θ(X₁, s=1) - f_θ(T(X₁), s=0)‖²)。

这一设计的因果机制在于：匹配偏差不仅是Wasserstein距离的一个可计算上界（Theorem 4.1：若Δ_M(θ,T) ≤ δ，则Δ_W(θ) ≤ δ），而且当总变差距离有界时，存在匹配函数使匹配偏差保持有界（Theorem 4.2）。这意味着公平性约束可以转化为一个O(n)复杂度的可微惩罚项，无需对抗学习。基于此，作者构建了匹配吉布斯后验（matched Gibbs posterior）：ν_M(f,T|λ) ∝ exp(ℓ(f) - λn Δ_M(f,T)) π(f) π(T)，将公平性惩罚项直接融入似然函数，使得标准MCMC算法可以在无约束参数空间上直接采样。



## 核心方法与创新机理

该工作的核心瓶颈在于现有公平性方法（如 gapreg、reduction、adv）仅输出单一确定性模型，无法量化模型不确定性（model uncertainty），而后者对于高风险决策的鲁棒性和可信度至关重要。变分贝叶斯方法虽能提供不确定性，但将群体公平性约束（如 Wasserstein 距离）直接纳入变分推断时，面临计算不可行的问题：约束项通常需要对抗学习或 $O(n^2)$ 的二次复杂度，且约束后的参数空间高度非凸，使得标准变分族（如平均场高斯）难以有效优化。

针对此瓶颈，论文的关键因果旋钮（causal knob）是提出一种新的群体公平性度量——**匹配偏差（matched deviation）**，并基于此构建**匹配吉布斯后验（matched Gibbs posterior）**。其核心洞察在于：通过引入一个可学习的匹配函数 $T: \mathcal{X}_1 \to \mathcal{X}_0$ 将不同敏感组的输入空间对齐，匹配偏差 $\Delta_M(\theta, T) := \mathbb{E}_{X_1 \sim \mathbb{P}_1} \left( \| f_\theta(X_1, s=1) - f_\theta(T(X_1), s=0) \|^2 \right)$ 成为 Wasserstein 距离 $\Delta_W(\theta)$ 的一个可计算上界（Theorem 4.1）。这使得公平性惩罚项从难以优化的对抗形式转化为简单的 $O(n)$ 复杂度计算。

该方法改变了三个关键设计槽位（changed slots）：

1.  **公平性度量**：从 Wasserstein 距离、总变差距离等需要对抗学习或 $O(n^2)$ 计算的度量，替换为计算复杂度为 $O(n)$ 且无需对抗学习的匹配偏差。理论保证（Theorem 4.2）表明，当总变差距离有界时，存在匹配函数使匹配偏差有界，保证了度量的合理性。

2.  **后验推断方法**：从在约束参数空间上进行变分推断（如平均场高斯 VI），替换为在无约束参数空间上构建吉布斯后验 $\nu_M(f,T|\lambda) \propto \exp\left( \ell(f) - \lambda n \Delta_M(f,T) \right) \pi(f) \pi(T)$。公平性惩罚项被直接融入似然函数，使得标准 MCMC 算法（如 Gibbs 采样器）可以直接用于采样，避免了约束优化和对抗训练的复杂性。实验表明，该 MCMC 算法收敛良好（E-BFMI ≈ 1.646 > 0.3），且匹配函数 $T$ 的接受率在推荐范围 $[0.2, 0.5]$ 内。

3.  **匹配函数 $T$ 的处理**：从基线方法中完全不使用匹配函数，转变为将 $T$ 视为一个可学习的参数，通过部分置换的 Metropolis-Hastings 提议进行 Gibbs 采样。这允许算法在推断模型参数 $\theta$ 的同时，自适应地学习最优的样本级匹配，从而更精确地度量并惩罚群体间的不公平性。

在多个真实数据集（ADULT, DUTCH, CRIME, CELEBA, CIVIL）上的实验表明，匹配吉布斯后验在效用-公平性和不确定性-公平性权衡上均优于所有基线方法（gapreg, reduction, adv, mean-field Gaussian VI），在 CRIME、CELEBA、CIVIL 等数据集上的 Pareto 前沿曲线中占据主导地位。此外，该方法在个体公平性指标（Consistency score）上也优于基线，并能自然扩展至等几率（Equalized Odds）和多值敏感属性场景。



该方法的整体框架由三个核心模块串联而成：**匹配偏差计算模块**、**吉布斯后验构建模块**和**MCMC采样模块**。其核心设计思路是，通过引入一个可学习的匹配函数将群体公平性约束转化为一个易于计算的惩罚项，进而将该惩罚项融入吉布斯后验的似然函数中，使得标准MCMC算法能够在无约束的参数空间上直接进行公平后验推断。

**1. 输入与初始化**

框架的输入包括：训练数据（包含特征 $X$、敏感属性 $S$ 和标签 $Y$）、预测模型 $f_\theta$ 的参数先验 $\pi(f)$，以及匹配函数 $T$ 的先验 $\pi(T)$。匹配函数 $T: X_1 \to X_0$ 旨在将敏感组 $S=1$ 的输入空间映射到 $S=0$ 的输入空间，其初始化通常依赖于最优传输（Optimal Transport）计算。

**2. 匹配偏差计算模块**

该模块的核心是计算**匹配偏差**（matched deviation）$\Delta_M(\theta, T)$，其定义如下（见公式(6)）：

$$
\Delta_M(\theta, T) := \mathbb{E}_{X_1 \sim \mathbb{P}_1} \left( \| f_\theta(X_1, s=1) - f_\theta(T(X_1), s=0) \|^2 \right)
$$

该度量衡量了在匹配函数 $T$ 作用下，不同敏感组的模型预测之间的平方差期望。其关键优势在于：1）计算复杂度仅为 $O(n)$，远低于传统Wasserstein距离的 $O(n^2)$ 或对抗学习；2）理论证明了匹配偏差是Wasserstein距离的一个上界（Theorem 4.1），并且当总变差距离有界时，存在匹配函数使匹配偏差有界（Theorem 4.2）。这使得它成为一个既高效又具有理论保障的公平性惩罚项。

**3. 吉布斯后验构建模块**

该模块将上述惩罚项集成到贝叶斯框架中，构建**匹配吉布斯后验**（matched Gibbs posterior）$\nu_M(f, T | \lambda)$。其形式为（见公式(5)）：

$$
\nu_M(f, T | \lambda) \propto \exp\left( \ell(f) - \lambda n \Delta_M(f, T) \right) \pi(f) \pi(T)
$$

其中，$\ell(f)$ 是模型的对数似然（衡量预测性能），$\lambda$ 是一个超参数，用于控制公平性惩罚的强度。通过这种形式，公平性约束被平滑地融入了后验分布，从而将问题转化为在一个无约束的参数空间上对联合分布 $(f, T)$ 进行采样。

**4. MCMC采样模块（Gibbs采样器）**

为了从匹配吉布斯后验中采样，该框架采用Gibbs采样器，交替更新模型参数 $f$ 和匹配函数 $T$：
- **采样 $f \sim \nu_M(f | T, \lambda)$**：在给定 $T$ 和 $\lambda$ 的条件下，后验分布退化为一个带有二次惩罚项的广义线性模型，可以使用标准的MCMC方法（如HMC）进行高效采样。
- **采样 $T \sim \nu_M(T | f, \lambda)$**：在给定 $f$ 和 $\lambda$ 的条件下，采样匹配函数 $T$。由于 $T$ 是一个离散的匹配映射，论文设计了基于**部分置换的Metropolis-Hastings (MH) 提议**（见Figure 4的示意图），该提议通过随机交换少量匹配对来生成新的 $T'$，从而保证采样的效率和收敛性。实验表明，该MCMC算法收敛良好（E-BFMI ≈ 1.646 > 0.3），且 $T$ 的接受率在推荐范围 [0.2, 0.5] 内。

**5. 输出与超参数选择**

MCMC采样完成后，得到一系列来自后验的样本 $\{ (f^{(t)}, T^{(t)}) \}_{t=1}^N$。这些样本可以直接用于不确定性量化，例如计算预测均值和置信区间。超参数 $\lambda$ 的选择通过网格搜索进行：选择能够最大化ELBO（证据下界），同时使得后验样本的平均人口统计平等差距（DP gap）小于预设阈值 $\delta$ 的 $\lambda$ 值。最终的输出是一个能够同时提供公平预测和不确定性量化的贝叶斯模型。



### 1. 公平性度量：从群体偏差到匹配偏差

现有公平性贝叶斯推断的核心瓶颈在于：将群体公平性约束（如人口统计平等）直接融入后验推断时，需要计算两个敏感组预测分布之间的偏差度量，而大多数常用度量（如Wasserstein距离、IPM）的计算复杂度高（通常为 $O(n^2)$）或需要对抗学习，导致变分推断在约束参数空间上难以高效进行。

为解决此问题，论文提出一种新的群体公平性度量——**匹配偏差（matched deviation）**。其核心思想是：通过学习一个匹配函数 $T: \mathcal{X}_1 \to \mathcal{X}_0$，将敏感组 $S=1$ 的每个样本映射到 $S=0$ 组中的一个样本，然后直接计算映射后的预测差异。

**匹配偏差的定义**（Equation 6）：

$$
\Delta_M(\theta, \mathbf{T}) := \mathbb{E}_{X_1 \sim \mathbb{P}_1} \left( \| f_\theta(X_1, s=1) - f_\theta(\mathbf{T}(X_1), s=0) \|^2 \right)
$$

其中 $f_\theta$ 是参数为 $\theta$ 的预测模型，$\mathbf{T}$ 是一个从 $S=1$ 组样本索引到 $S=0$ 组样本索引的映射函数。该度量的计算复杂度仅为 $O(n)$，无需对抗学习。

**关键理论关系**（Theorem 4.1 & 4.2）：
- **$\Delta_M \Rightarrow \Delta_W$**：若匹配偏差 $\Delta_M(\theta, T) \leq \delta$，则Wasserstein距离 $\Delta_W(\theta) \leq \delta$。即匹配偏差是Wasserstein距离的一个上界。
- **$\Delta_{TV} \Rightarrow \Delta_M$**：若总变差距离 $\Delta_{TV}(\theta) \leq \delta$（$\delta \in [0,1]$），则存在一个匹配函数 $T$ 使得 $\Delta_M(\theta, T) \leq 2c\delta$（$c>0$ 为常数）。即当总变差距离有界时，匹配偏差也有界。

这意味着匹配偏差可以替代Wasserstein距离作为公平性约束，且计算上更高效。

### 2. 匹配吉布斯后验：将公平性惩罚融入似然

基于匹配偏差，论文构建了**匹配吉布斯后验（matched Gibbs posterior）**（Equation 5）：

$$
\nu_n(\theta; \lambda) \propto \exp\left( \ell(\theta) - \lambda n \Delta_M(\theta, T) \right) \pi(\theta)
$$

其中 $\ell(\theta)$ 是对数似然（衡量预测性能），$\lambda$ 是控制公平性-效用权衡的超参数，$\pi(\theta)$ 是先验分布。

与传统的变分推断方法不同，匹配吉布斯后验将公平性惩罚项 $\lambda n \Delta_M(\theta, T)$ 直接融入似然函数，从而将问题转化为在**无约束参数空间**上进行后验采样。这使得标准MCMC算法可以直接用于公平后验推断，无需对抗学习或二次复杂度计算。

**完整后验形式**（考虑匹配函数 $T$ 的先验）：

$$
\nu_M(f, T | \lambda) \propto \exp\left( \ell(f) - \lambda n \Delta_M(f, T) \right) \pi(f) \pi(T)
$$

其中匹配函数 $T$ 的先验 $\pi(T)$ 基于输入空间距离定义（Equation 8）：

$$
e(\mathbf{T}; \tau) := \exp\left( -\frac{1}{n_0} \sum_{i=1}^{n_1} d(X_i^{(0)}, \mathbf{T}(X_i^{(1)})) / \tau \right)
$$

该先验鼓励匹配函数将特征相似的样本配对，$\tau$ 是温度参数。

### 3. MCMC采样算法

匹配吉布斯后验的采样采用**Gibbs采样器**，交替进行：
1. **采样 $f \sim \nu_M(f | T, \lambda)$**：给定匹配函数 $T$，后验对 $f$ 是标准的高斯过程回归形式（当使用GP先验时），可通过解析条件后验直接采样。
2. **采样 $T \sim \nu_M(T | f, \lambda)$**：给定模型参数 $f$，匹配函数 $T$ 的后验采样使用**部分置换的Metropolis-Hastings（MH）提议**。具体地，随机选择 $k$ 个 $S=1$ 组的样本，将其对应的匹配目标在 $S=0$ 组中进行置换，生成新的匹配函数 $T'$。这种提议机制保证了MCMC的收敛性。

**MCMC诊断**：实验中使用E-BFMI（Energy Bayesian Fraction of Missing Information）指标评估采样质量：

$$
\widehat{\mathrm{E{-BFMI}}} := \frac{\sum_{n=1}^N (E_n - E_{n-1})^2}{(E_n - \bar{E})^2}
$$

当E-BFMI > 0.3时表明MCMC采样行为良好。在ADULT数据集上，匹配吉布斯后验的E-BFMI ≈ 1.646，且匹配函数 $T$ 的接受率在推荐范围 [0.2, 0.5] 内。

### 4. 超参数 $\lambda$ 的选择

$\lambda$ 控制公平性-效用的权衡，通过以下步骤选择：
1. 对一组候选 $\lambda$ 值运行匹配吉布斯后验的MCMC采样。
2. 计算每个 $\lambda$ 下的经验ELBO（证据下界）和平均人口统计平等差距 $\mathbb{E}_\theta \Delta_W^{1/2}$。
3. 选择满足平均DP < $\delta$（$\delta$ 为目标公平性水平）且最大化ELBO的 $\lambda$ 值。

### 5. 扩展：等几率与多值敏感属性

**等几率（Equalized Odds）扩展**（Section E.1）：使用两个匹配函数 $T_0: \mathcal{X}_{0,1} \to \mathcal{X}_{0,0}$ 和 $T_1: \mathcal{X}_{1,1} \to \mathcal{X}_{1,0}$，分别对应真实标签 $Y=0$ 和 $Y=1$ 的子集。匹配偏差定义为：

$$
\Delta_M(\theta, T_0, T_1) := p_{0|1} \mathbb{E}_{X_1 \sim P_{(0,1)}} \| f_\theta(X_1, 1) - f_\theta(T_0(X_1), 0) \|^2 + p_{1|1} \mathbb{E}_{X_1 \sim P_{(1,1)}} \| f_\theta(X_1, 1) - f_\theta(T_1(X_1), 0) \|^2
$$

**多值敏感属性扩展**（Section E.2）：选择一个锚定组（如 $S=0$），为每个其他组 $S=i$ 定义一个匹配函数 $T_i: \mathcal{X}_i \to \mathcal{X}_0$，然后对所有组的匹配偏差求和。

### 6. 与变分推断的对比

论文还探讨了**公平变分推断**（Fair Variational Inference）方法（Section 3.3），其目标是在约束下最大化ELBO：

$$
\mathrm{ELBO}(\gamma) := \mathbb{E}_{\theta \sim \nu(\cdot|\gamma)} [\ell(\theta)] - D_{\mathrm{KL}}(\nu(\cdot) \| \pi(\cdot))
$$

约束条件为 $\mathbb{E}_{\theta \sim \nu(\cdot|\gamma)} \Delta_\psi(f_\theta) \leq \delta$。然而，实验表明（Table 5），当使用平均场高斯变分分布时，在严格公平性水平（$\delta$ 较小）下，满足约束的样本比例几乎为零（如 $\delta=0.22$ 时比例为0.000），说明标准变分推断难以有效处理公平性约束。



## 实验与关键发现

### 主结果：公平性-性能权衡

匹配吉布斯后验的核心优势在于其能够在群体公平性与预测性能之间实现更优的权衡。实验在五个真实世界数据集（ADULT, DUTCH, CRIME, CELEBA, CIVIL）上展开，覆盖表格、图像和文本分类任务。所有基线方法包括三类确定性公平性方法（gapreg, reduction, adv）以及一个变分贝叶斯基线（mean-field Gaussian VI）。群体公平性使用Wasserstein距离的平方根 $\Delta_w^{1/2}$ 度量，性能指标包括准确率（Acc）、负对数似然（Nll）、布里尔分数（brier）和期望校准误差（Ece）。

**关键发现**：在CRIME数据集上（Figure 1），匹配吉布斯后验的Pareto前沿线在所有四个性能指标上均显著优于所有基线方法，即在任意给定的 $\Delta_w^{1/2}$ 水平下，该方法都能获得更高的Acc、更低的Nll、更低的brier和更低的Ece。这一优势在CELEBA图像分类任务（Figure 2）和CIVIL文本分类任务（Figure 3）中同样成立，且在CELEBA上的Acc提升幅度尤为显著（“with large margins”）。在ADULT和DUTCH数据集（Figure 6, Figure 7）上，匹配吉布斯后验也展现出一致的优越性。

**机制分析**：优越性的根源在于匹配偏差的计算效率与吉布斯后验的灵活采样。确定性基线方法（gapreg, reduction, adv）只能输出点估计，无法量化模型不确定性；而平均场高斯VI在严格的公平性约束下，从后验中采样到的公平样本比例急剧下降（Table 5: δ=0.27时比例0.014，δ=0.22时降至0.000），导致变分推断失效。匹配吉布斯后验通过将公平性惩罚项融入似然函数，在无约束参数空间上使用标准MCMC采样，避免了对抗学习或二次复杂度计算，从而在保持后验多样性的同时有效控制了公平性。

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/027_Table_5.jpg]]
*Table 5: Proportion of samples from mean-field Gaussian distribution optimized with standard ELBO, under varying level of δ*

### 消融研究与鲁棒性分析

**匹配函数先验温度 $\tau$**：Figure 9 显示，在ADULT数据集上改变 $\tau$ 值（0.5, 1.0, 2.0）对匹配吉布斯后验的Pareto前沿线影响不大，表明该方法对 $\tau$ 的选择不敏感。Table 8 进一步量化了在 $\Delta_w \approx 0.09$ 时不同 $\tau$ 下的具体性能值，差异在可接受范围内。

**预训练轮数**：Figure 10 表明，不同的预训练轮数不会改变匹配吉布斯后验的优越权衡性能，但预训练不足可能影响MCMC的收敛效率。

**敏感属性翻转**：Figure 11 中，翻转敏感属性（橙色线）未导致性能显著变化，说明方法对敏感属性的编码方式具有鲁棒性。

**不同先验分布**：Figure 12 在CRIME数据集上比较了高斯、柯西和学生t先验，结果显示性能没有显著变化，表明方法对先验选择不敏感。

**其他公平性度量**：Figure 13 和 Figure 14 分别验证了在等几率（Equalized Odds, $\Delta_{EO}$）和强人口统计平等（Strong Demographic Parity, $\Delta_{SDP}$）度量下，匹配吉布斯后验依然优于基线方法，证明了框架的泛化能力。

### 个体公平性

Table 6 和 Table 7 展示了在固定 $\Delta_w^{1/2}$ 水平下，匹配吉布斯后验在个体公平性指标（Consistency score, Con）上优于所有基线方法。例如，在CRIME数据集上 $\Delta_w^{1/2} \approx 0.09$ 时，匹配吉布斯后验的Con为0.837（Acc 0.736），而最佳基线（gapreg）的Con仅为0.805（Acc 0.732）。这表明匹配函数不仅对齐了群体分布，还隐式地促进了输入空间中的个体级公平性。

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/028_Table_6.jpg]]
*Table 6: CRIME. With a fixed level of $\Delta _ { \mathrm { w } } ^ { 1 / 2 } \approx$ 0 . 0 9 , the level of Con and corresponding Acc are reported. The bold faced values implies the best values

### MCMC收敛诊断

Figure 8 展示了ADULT数据集上MCMC采样的能量相关图。计算得到的E-BFMI ≈ 1.646 > 0.3，表明MCMC链的行为良好，没有出现能量缺失信息问题。此外，匹配函数T的接受率在所有 $\lambda$ 值下均处于推荐范围 [0.2, 0.5] 内，证实了部分置换MH提议的有效性。

### 失败模式与局限性

尽管匹配吉布斯后验在大多数场景下表现优异，实验揭示了以下失败模式：
1. **严格公平性下的校准退化**：在非常严格的 $\Delta_w^{1/2}$ 水平下，Ece（期望校准误差）可能增加。这表明过度惩罚公平性可能会损害概率预测的校准质量，可能需要额外的后处理校准技术（如温度缩放）来缓解。
2. **变分推断的失效**：Table 5 明确展示了平均场高斯VI在公平约束下的失败——采样到的公平样本比例随约束收紧而急剧下降至零。这验证了论文的理论动机，即简单的变分族无法同时捕捉后验的不确定性和满足公平性约束。
3. **计算瓶颈**：匹配函数T的初始化依赖于最优传输（OT）计算。对于高维或复杂数据（如高分辨率图像），OT计算可能成为瓶颈。论文未提供关于OT初始化时间的具体消融数据，这是一个需要手动验证的潜在弱点。

### 补充图表

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/013_Table_1.jpg]]
*Table 1: Summary statistics for each dataset*

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/014_Table_2.jpg]]
*Table 2: λ values that are used in the main experiments*

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/016_Table_3.jpg]]
*Table 3: $\pi ( \{ \theta : \Delta _ { \mathrm { D P } } ( \theta ) \leq \eta \} | \mathcal { D } _ { n }$ ) values for varying η

![[assets/figures/papers/iclr26_0002_sIjFXzEOOH_A_Fair_Bayesian_Inference_through_Matched_Gibbs/figures/017_Table_4.jpg]]
*Table 4: Acceptance ratio of random-walk Metropolis-Hastings, only accepting samples that satisfies given constraint threshold*



## 定位与知识库关联

### 与基线方法的关系

匹配吉布斯后验（Matched Gibbs Posterior）的核心突破在于将公平性约束引入贝叶斯推断框架，从而同时实现群体公平和模型不确定性的量化。这与现有确定性公平性方法（gapreg, reduction, adv）形成根本性对比——后者仅输出单一预测模型，无法提供预测的不确定性估计。具体而言，方法在三个关键槽位上实现了变革：

1. **公平性度量**：基线普遍使用Wasserstein距离、总变差距离或Kolmogorov-Smirnov距离等IPM度量，这些度量在变分推断中要么需要对抗学习（如adv方法），要么需要O(n²)计算。匹配偏差（matched deviation）将复杂度降至O(n)，且无需对抗训练，这是其计算效率优势的根本来源。

2. **后验推断方法**：基线中的贝叶斯方法（mean-field Gaussian VI）在约束参数空间上优化ELBO，但如消融研究所示（Table 5），在严格公平水平（δ=0.22）下，来自平均场高斯的公平样本比例降至0.000——这意味着约束变分推断在实践中失效。匹配吉布斯后验通过将公平性惩罚项融入似然函数，在无约束参数空间上使用标准MCMC采样，绕过了这一瓶颈。

3. **匹配函数T的处理**：这是方法独有的创新点。T被视为可学习参数，通过部分置换的MH提议进行Gibbs采样（Figure 4可视化其构造过程）。这种设计使得匹配偏差可以随模型参数共同优化，而非固定不变。

### 适用边界与实验证据强度

方法在三个维度上展示了优越的Pareto前沿权衡：
- **表格数据**（CRIME, ADULT, DUTCH）：在所有四个指标（Acc, Nll, brier, Ece）上，匹配吉布斯后验的Pareto前沿线均位于基线之上（Figure 1, 6, 7）。证据强度高（置信度0.95），在CRIME数据集上尤为显著。
- **图像分类**（CELEBA）：Acc提升幅度最大（“with large margins”，Figure 2），Nll和brier也优于所有确定性基线。证据强度较高（0.95），但需注意Nll和brier的置信度略低（0.9）。
- **文本分类**（CIVIL）：类似地，在所有指标上优于基线（Figure 3），但置信度略低（0.9），可能因实验设置或样本量差异。

个体公平性方面，在CRIME、ADULT、DUTCH数据集上固定Δ_w^{1/2}水平时，匹配吉布斯后验的Consistency score均优于基线（Table 6, 7），表明方法在群体公平和个体公平之间不存在根本性冲突。

### 局限与开放问题

**已知局限**：
1. 在严格公平水平下，Ece（期望校准误差）可能增加，可能需要温度缩放等校准技术缓解。这是方法在当前形式下的固有弱点。
2. 匹配函数T的初始化依赖最优传输（OT），对于高维或复杂数据（如深度Transformer），OT计算可能成为瓶颈。当前实验仅在CELEBA（图像）和CIVIL（文本）上验证，但未报告OT计算开销的详细分析。
3. 方法对预训练模型质量有一定依赖——消融研究（Figure 10）显示不同预训练轮数影响性能，但机制尚未明确。

**开放问题**：
1. **理论性质**：匹配吉布斯后验的后验一致性（posterior consistency）缺乏严格证明。虽然Theorem 4.1和4.2建立了匹配偏差与Wasserstein距离、总变差距离之间的理论关系，但后验本身的渐近性质仍是空白。
2. **超参数选择**：匹配函数先验的温度参数τ目前通过网格搜索选择（Figure 9显示τ=1.0不显著影响结果），但缺乏自动选择机制。λ的选择同样依赖网格搜索（Table 2）。
3. **扩展性**：方法已扩展至等几率（Equalized Odds，使用两个匹配函数T_0和T_1，Figure 13）和多值敏感属性（使用锚定组和多个T_i，Section E.2），但扩展到多分类任务和更复杂模型（如Transformer）的MCMC采样效率尚未验证。
4. **其他公平性任务**：如表示学习（representation learning）中的公平性感知，是作者指出的未来方向。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Fair_Bayesian_Inference_through_Matched_Gibbs_Posterior.pdf

![[paperPDFs/ICLR_2026/A_Fair_Bayesian_Inference_through_Matched_Gibbs_Posterior.pdf]]
