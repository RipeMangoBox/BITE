---
title: "Benchmarking Stochastic Approximation Algorithms for Fairness-Constrained Training of Deep Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Benchmarking_Stochastic_Approximation_Algorithms_for_Fairness_Constrained_Training_of_Deep_Neural_Networks.pdf
project_link: null
code_link: null
aliases:
- BFFCDT
- BSAAFCTDNN
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety
core_operator: "The benchmark formulates fairness-constrained DNN training as stochastic inequality-constrained optimization and compares recent stochastic approximation algorithms."
primary_logic: "It builds Folktables-based constrained ERM tasks, implements Stochastic Ghost, SSL-ALM, ALM, and Switching Subgradient, then tracks accuracy and fairness metrics over time."
claims:
- "The benchmark stresses nonconvex, nonsmooth, large-scale objectives and constraints that current theory does not fully cover."
- "ALM and SSL-ALM provide the best reported accuracy-fairness tradeoff in the note."
- "Switching Subgradient satisfies constraints strongly but is weaker at minimizing the objective."
---

# Benchmarking Stochastic Approximation Algorithms for Fairness-Constrained Training of Deep Neural Networks

> [!tip] 核心洞察
> 通过构建基于US Census (Folktables) 的真实大规模公平性约束学习基准，首次系统比较了三种近期提出的随机近似算法（Stochastic Ghost, SSL-ALM, Stochastic Switching Subgradient）在优化性能和公平性改善方面的实际表现，并指出目前尚无理论保证的算法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 公平约束深度神经网络训练的随机逼近算法基准评测 |
| 英文题名 | Benchmarking Stochastic Approximation Algorithms for Fairness-Constrained Training of Deep Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=JxmjzC6syB) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety |
| Method | Benchmarking framework for fairness-constrained DNN training |
| Dataset | ACSIncome (Oklahoma, binary protected attribute: race) |

> [!tip] 效果简介
> - ACSIncome (Oklahoma, binary protected attribute: race) 上，Loss (train) 为 0.4448 (SSL-ALM, τ=0.01, η=0.05, μ=0)，对比 0.406 (SGD)，变化 +0.0388。
> - ACSIncome (Oklahoma, binary protected attribute: race) 上，Constraint violation (train) 为 0.0070 (SSL-ALM, τ=0.01, η=0.05, μ=0)，对比 N/A (SGD无约束)，变化 N/A。
> - ACSIncome (Oklahoma, binary protected attribute: race) 上，Independence (Ind, train) 为 0.074±0.005 (SSL-ALM)，对比 0.095±0.003 (SGD)，变化 -0.021。

## 概要

本文提出了首个系统性的基准测试框架，用于评估随机近似算法在公平性约束下的深度神经网络训练中的实际表现。研究聚焦于解决带不等式约束的随机优化问题，其中目标函数和约束函数均为非凸、非光滑且大规模。论文基于US Census数据（通过Folktables包）构建了真实世界的公平性约束学习基准，首次系统比较了三种近期提出的随机近似算法——Stochastic Ghost、SSL-ALM（Stochastic Smoothed and Linearized Augmented Lagrangian Method）和Stochastic Switching Subgradient——在优化性能和公平性改善方面的实际表现。实验结果表明，增广拉格朗日方法（ALM和SSL-ALM）在公平性与准确性之间取得了最佳折中，而Stochastic Switching Subgradient在满足约束方面表现最优但目标函数最小化不足。论文同时指出，目前尚无算法能同时处理非凸、非光滑的目标和约束函数并给出收敛性保证。



深度神经网络在诸多领域取得显著成功，但其训练过程通常仅关注预测准确性，可能学习到训练数据中的偏见，导致对受保护群体的不公平对待。标准的经验风险最小化（ERM）形式为：

$$\operatorname* { m i n } _ { \theta \in \mathbb { R } ^ { n } } \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \ell ( f _ { \theta } ( X _ { i } ) , Y _ { i } ) + \mathcal { R } ( \theta )$$

其中 $f_\theta$ 是由深度神经网络定义的预测函数，其前向传播可递归表示为：

$$a _ { 0 } = X , \qquad a _ { i } = \rho _ { i } ( V _ { i } ( \theta ) a _ { i - 1 } ) , { \mathrm { ~ f o r ~ e v e r y ~ } } i = 1 , \ldots , L , \qquad f _ { \theta } ( X ) = a _ { L }$$

为缓解偏见，研究者提出在训练中引入公平性约束。本文考虑带约束的ERM问题：

$$\operatorname* { m i n } _ { x \in \mathbb { R } ^ { n } } \mathbb { E } [ f ( x , \xi ) ] \quad \mathrm { s . t . } \quad \mathbb { E } [ c ( x , \zeta ) ] \leq 0$$

其中 $f$ 为损失函数，$c$ 为约束函数。在公平性场景中，约束可具体化为子组损失差异约束：

$$\begin{array} { r l } { \underset { \theta \in \mathbb { R } ^ { n } } { \operatorname* { m i n } } } & { \displaystyle \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \ell ( f _ { \theta } ( X _ { i } ) , Y _ { i } ) + \mathcal { R } ( \theta ) } \\ { \mathrm { s . t . } } & { \displaystyle - \delta \leq \ell ^ { s _ { i } } ( \theta ) - \frac { 1 } { m } \sum _ { j = 1 } ^ { m } \ell ^ { s _ { j } } ( \theta ) \leq \delta , \quad i = 1 , \ldots , m . } \end{array}$$

**核心瓶颈**：目前没有一种算法能够同时处理大规模、非凸、非光滑的目标函数和约束函数，并给出收敛性保证。现有算法要么假设目标函数光滑（如 $C^1$），要么只处理等式约束，要么需要大量采样，无法直接应用于公平性约束下的深度神经网络训练。

**因果旋钮**：算法设计中对目标函数和约束函数的可微性、凸性假设，以及采样策略（如是否使用几何分布增大批大小、是否使用平滑项）是决定算法能否实际收敛的关键。



## 核心方法与创新机理

本文的核心创新在于：

1. **首个系统性基准测试**：提供了第一个用于评估优化方法在真实世界公平性约束训练中性能的基准测试框架。
2. **算法实现与比较**：实现了三种近期提出的但尚未被广泛实现的随机近似算法（Stochastic Ghost, SSL-ALM, Stochastic Switching Subgradient），并在统一框架下进行比较。
3. **大规模真实数据集**：利用US Census数据（通过Folktables包）构建基准，支持定义多达57亿个受保护子组。
4. **自动化工具链**：提供自动化方式从PyTorch或TensorFlow定义的计算图构建ERM公式，并发布为Python包（https://github.com/humancompatible/train）。
5. **硬约束优于惩罚项**：遵循Cotter et al. (2019)的论点，采用硬约束（不等式约束）而非加权惩罚项，提供更清晰的模型设计理解。



![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/004_Figure_1.jpg]]
*Figure 1: Train (blue) and test (orange) statistics over time (s) on the ACS Income dataset for each algorithm: SGD (column 1), fairret-regularized SGD (column 2), SSL-ALM (column 3), ALM (column 4) Switching Subgradient (column 5), and Stochastic Ghost (column 6). The plots depict the mean values for loss (first row) and the constraint at each timestamp, rounded to the nearest 0.5 seconds, over 10 runs. The shaded area depicts the region between the first and third quartiles.*

本文提出的基准测试框架包含以下模块：

| 模块名称 | 作用 |
|---------|------|
| 数据加载与预处理 | 使用Folktables加载US Census数据，定义保护属性和子组 |
| 约束定义 | 支持准确性平等、机会平等、均等化几率等公平性约束（Table 1） |
| 优化算法 | 实现Stochastic Ghost, SSL-ALM, ALM, Stochastic Switching Subgradient四种算法 |
| 评估与可视化 | 计算公平性指标（独立性、分离性、充分性）和Wasserstein距离，生成损失和约束随时间变化的曲线 |

**基线方法**：
- SGD：无公平性约束的基线
- fairret-regularized SGD / Regularized SGD：基于惩罚项的公平性方法基线

**改变的槽位**：
- 约束处理方式：从惩罚项（如fairret）改为硬约束（不等式约束）
- 采样策略：从固定小批量大小改为几何分布控制批量大小（Stochastic Ghost）或切换规则（Switching Subgradient）
- 优化器类型：从SGD（无约束）改为增广拉格朗日方法、随机幽灵方法、切换次梯度方法



### 5.1 优化问题形式化

本文考虑的一般优化问题为：

$$\min_{x \in \mathbb{R}^n} F(x) \quad \mathrm{s.t.} \quad C(x) \leq 0$$

其中 $F$ 和 $C$ 定义为期望函数。随机梯度的小批量估计为：

$$\overline{\nabla}^J f(\boldsymbol{x}) = \frac{1}{J} \sum_{j=1}^J \nabla f(\boldsymbol{x}, \boldsymbol{\xi}_j)$$

### 5.2 Stochastic Ghost方法

该方法结合确定性方法和随机采样，使用几何分布控制批量大小。算法核心是计算无偏搜索方向估计：

$$d(x_k) = \frac{d(x_k; X_k^{2^{N+1}}) - \frac{1}{2}(d(x_k; \mathrm{odd}(X_k^{2^{N+1}})) + d(x_k; \mathrm{even}(X_k^{2^{N+1}})))}{(1-p_0)^N p_0} + d(x_k; X_k^1)$$

其中 $N \sim \text{Geometric}(p_0)$，批量大小 $J = 2^{N+1}$。该方法使用四个特定的小批量计算无偏估计。

### 5.3 SSL-ALM（Stochastic Smoothed and Linearized AL Method）

该方法用于处理随机线性约束，通过松弛变量处理不等式约束，使用小批量大小。其随机梯度更新为：

$$G(x,y,z;\xi,\zeta_1,\zeta_2) = \nabla f(x,\xi) + \nabla c(x,\zeta_1)^\top y + \rho \nabla c(x,\zeta_1)^\top c(x,\zeta_2) + \mu(x-z)$$

迭代更新规则为：

$$y_{k+1} = y_k + \eta c(x,\zeta_1), \quad x_{k+1} = \mathrm{proj}_{\mathcal{X}}(x_k - \tau G(x_k, y_{k+1}, z_k; \xi, \zeta_1, \zeta_2)), \quad z_{k+1} = z_k + \beta(x_k - z_k)$$

其中 $y$ 为对偶变量，$x$ 为原始变量，$z$ 为辅助变量。

### 5.4 Stochastic Switching Subgradient方法

该方法允许弱凸、可能非光滑的目标和约束函数，使用次梯度并依赖预设的不可行容忍度序列 $\epsilon_k$。算法在下降步和约束减少步之间切换，基于小批量约束违反是否低于容忍度 $\epsilon_k$。

### 5.5 公平性约束定义

Table 1列出了用于实施公平性的约束函数 $c$ 的具体形式，包括准确性平等、机会平等（Hardt et al., 2016）和均等化几率。

Table 2定义了三种基本公平性概念：
- **独立性（Independence）**：$P(\hat{Y} = + \mid S = s_i)$ 在所有组中相等
- **分离性（Separation）**：$P(\hat{Y} = + \mid S = s_i, Y = v)$ 在所有组中相等
- **充分性（Sufficiency）**：$P(Y = + \mid \hat{Y} = v, S = s)$ 在所有组中相等

### 5.6 损失函数

所有问题中使用带Logits的二元交叉熵损失：

$$\ell ( f _ { \theta } ( X _ { i } ) , Y _ { i } ) = - Y _ { i } \cdot \log \sigma ( f _ { \theta } ( X _ { i } ) ) - ( 1 - Y _ { i } ) \cdot \log ( 1 - \sigma ( f _ { \theta } ( X _ { i } ) ) )$$

其中 $\sigma$ 是sigmoid函数，$f_\theta$ 是神经网络预测。

### 5.7 多值保护属性的惩罚问题

对于多值保护属性，使用带公平性正则化项的无约束惩罚问题：

$$\operatorname*{min}_{\theta\in\mathbb{R}^n} \frac{1}{N}\sum_{i=1}^N \ell(f_\theta(X_i),Y_i) + \mathcal{R}(\theta) + \lambda \sum_{i=1}^m \left| \ell^{s_i}(\theta) - \frac{1}{m}\sum_{j=1}^m \ell^{s_j}(\theta) \right|$$



## 实验与关键发现

### 6.1 实验设置

所有实验使用ACSIncome数据集，二元分类任务预测收入是否超过$50,000。二元保护属性实验使用种族（RAC1P）二值化为白人/非白人，数据集大小17,917，9个特征，80/10/10划分。多值保护属性实验使用种族原始多类别值。约束界 $\delta$ 在二元属性实验中设为0.05，多值属性实验中设为0.05。

### 6.2 主要结果

**实验1：二元保护属性（种族）**

Table 4报告了各算法的公平性指标。关键结果如下：

![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/005_Table_4.jpg]]
*Table 4: Fairness metrics (independence, separation, sufficiency), inaccuracy, and Wasserstein distances between groups (Wd) for the four constrained estimators and the two baselines.*

| 算法 | Ind (训练) | Sp (训练) | Ina (训练) | Sf (训练) | Wd (训练) |
|------|-----------|-----------|-----------|-----------|-----------|
| SGD | 0.095±0.003 | 0.124±0.006 | 0.186±0.023 | 0.065±0.004 | 0.062±0.012 |
| SSL-ALM | 0.074±0.005 | 0.091±0.010 | 0.208±0.009 | 0.050±0.009 | 0.043±0.006 |
| ALM | 0.083±0.009 | 0.112±0.024 | 0.210±0.010 | 0.057±0.011 | 0.049±0.009 |
| StGh | 0.080±0.010 | 0.108±0.015 | 0.230±0.025 | 0.048±0.022 | 0.046±0.009 |
| SSw | 0.082±0.008 | 0.107±0.012 | 0.222±0.011 | 0.058±0.008 | 0.047±0.007 |

**关键发现**：
- ALM和SSL-ALM在公平性和准确性之间取得了最佳折中：改善独立性、分离性、充分性，同时适度降低准确性
- Stochastic Ghost在充分性（Sf）上表现最好，但准确性下降最多
- Stochastic Switching Subgradient满足约束最好，但目标函数最小化不足

**超参数调优结果**（Table 6）：SSL-ALM在 $\tau=0.01, \eta=0.05, \mu=0$ 时取得最佳性能，损失均值0.4448，约束违反均值0.0070。

**实验2：多值保护属性（种族）**

| 算法 | 损失（验证） | 约束违反（验证） |
|------|------------|----------------|
| SGD | 0.432 | 0.075 |
| SSL-ALM ($\tau=0.05, \eta=0.01$) | 0.530 | 0.000 |
| Switching Subgradient | 0.519 | 0.001 |
| Stochastic Ghost | 0.5442 | 0.0180 |
| Regularized SGD ($\lambda=0.4$) | 0.512 | 0.001 |

### 6.3 消融实验

- **平滑项的影响**：移除平滑项（$\mu=0$）的ALM与SSL-ALM性能相似，表明平滑项对最终结果影响不大
- **批量大小控制**：Stochastic Ghost的批量大小由几何分布控制，较大的批量有助于降低方差但增加计算成本
- **约束容忍度序列**：Stochastic Switching Subgradient的约束容忍度序列 $\epsilon_k$ 对算法行为有显著影响

### 6.4 可视化分析

Figure 1展示了各算法在ACSIncome数据集上损失和约束随时间变化的训练和测试统计量。Figure 3展示了各算法预测值的分布，比较白人和非白人群体。Figure 4以雷达图形式展示平均公平性指标和不准确性。

### 6.5 局限性

- 目前没有算法能同时处理非凸、非光滑的目标和约束函数并给出收敛性保证
- 公平性约束学习只是更广泛的公平性AI流程中的一个环节，不能替代跨学科的整体解决方案
- 实验仅基于US Census (ACSIncome) 数据集，可能无法推广到其他领域
- 超参数调优依赖于验证集，不同数据集可能需要不同的调优策略
- 约束方法虽然提供了更清晰的模型设计理解，但可能比惩罚方法更难调优

### 补充图表

![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/001_Table_1.jpg]]
*Table 1: Particular formulations of the constraint function c to enforce fairness.*

![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/002_Table_2.jpg]]
*Table 2: Three elementary notions of fairness*

![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/003_Table_3.jpg]]
*Table 3: Assumptions on objective and constraint functions, F and C , which allow for theoretical convergence proofs.*

![[assets/figures/papers/iclr26_0002_JxmjzC6syB_Benchmarking_Stochastic_Approximation_Algorithms/figures/015_Table_5.jpg]]
*Table 5: Loss and constraint violation on the validation set after 5 30-second runs of the Stochastic Switching Subgradient in the setup of Exp. 1, rounded to 3 digits.*



## 定位与知识库关联

本文的方法谱系可定位如下：

**优化方法谱系**：
- 确定性约束优化 → 随机约束优化
- 光滑目标/约束 → 非光滑目标/约束
- 等式约束 → 不等式约束
- 惩罚方法 → 硬约束方法

**与现有工具的关系**：
- 与AIF360（Bellamy et al., 2018）和FairLearn（Bird et al., 2020）等公平性评估工具箱互补，本文专注于优化算法层面的实现和比较
- 与fairret（Buyl et al., 2024）等惩罚方法相比，本文采用硬约束方法，提供更清晰的模型设计理解
- 基于Folktables（Ding et al., 2021）数据集，支持大规模真实世界公平性基准

**开放问题**：
- 是否存在一种算法能够同时处理非凸、非光滑的目标和约束函数，并提供理论收敛性保证？
- 如何自动选择约束界 $\delta$？不同的 $\delta$ 值对公平性-准确性权衡有何影响？
- 本基准测试中的算法在其他公平性数据集（如COMPAS, German Credit）上的表现如何？
- 如何将本基准测试扩展到更复杂的公平性定义（如交叉性公平性）？
- Stochastic Ghost方法中几何分布参数 $p_0$ 的最优选择是什么？
- SSL-ALM中的平滑项 $\mu$ 是否真的必要？在哪些情况下它比ALM更有优势？



## 原文 PDF

![[paperPDFs/ICLR_2026/Benchmarking_Stochastic_Approximation_Algorithms_for_Fairness_Constrained_Training_of_Deep_Neural_Networks.pdf]]
