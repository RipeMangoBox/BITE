---
title: "Bayesian Neural Networks for Functional ANOVA Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bayesian_Neural_Networks_for_Functional_ANOVA_Model.pdf
project_link: null
code_link: null
openreview_forum_id: cvZhXILRLI
aliases:
- BT
- BNNFAM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability
core_operator: "将分量索引集$S_k$和分量数$K$视为可学习的架构参数，通过MCMC算法在参数空间中进行随机搜索（包含随机生成和步进式扩展），避免预定义所有分量。"
primary_logic: "利用分层贝叶斯先验（节点稀疏$K$、边稀疏$S_k$）与步进式MCMC搜索（Stepwise move：复制现有节点并增加一条边）在保持模型稳定性的同时有效探测高阶交互，从而在不牺牲精度的前提下获得可解释的组件估计。"
claims:
- "将$S$视为可学习参数并用MCMC搜索架构。"
- "步进式搜索通过复制现有节点并添加边自然生成高阶交互。"
- "证明了对每个分量的后验一致性。"
- "ABALONE（回归） 上 RMSE↓ = 2.053 (0.26)"
---

# Bayesian Neural Networks for Functional ANOVA Model

> [!tip] 核心洞察
> 利用分层贝叶斯先验（节点稀疏$K$、边稀疏$S_k$）与步进式MCMC搜索（Stepwise move：复制现有节点并增加一条边）在保持模型稳定性的同时有效探测高阶交互，从而在不牺牲精度的前提下获得可解释的组件估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向函数型ANOVA模型的贝叶斯神经网络 |
| 英文题名 | Bayesian Neural Networks for Functional ANOVA Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cvZhXILRLI) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/accountability_transparency_and_interpretability |
| Method | Bayesian-TPNN |
| Dataset | ABALONE（回归）, MADELON（分类）, CELEBA-HQ（图像分类CBM）, SERVO（回归） |

> [!tip] 效果简介
> - ABALONE（回归） 上，RMSE↓ 为 2.053 (0.26)，对比 ANOVA-TPNN: 2.051; mBNN: 2.081; BART: 2.197，变化 与最佳基线ANOVA-TPNN相当（差值<0.003）。
> - MADELON（分类） 上，AUROC↑ 为 0.854 (0.007)，对比 XGB: 0.616; BART: 0.595; mBNN: 0.519，变化 显著优于所有黑箱和贝叶斯基线。
> - CELEBA-HQ（图像分类CBM） 上，AUROC↑ 为 0.936 (0.002)，对比 Linear (10 concepts): 0.899，变化 +0.037，且仅使用5个概念即超越10个概念的Linear模型。

## 概要

传统函数型ANOVA模型将回归函数分解为满足和为零条件的分量之和，使每个分量对应特定输入变量的主效应或交互效应。然而，基于神经网络的ANOVA模型（如ANOVA-TPNN）必须预先指定所有可能的分量索引集$S$，导致计算复杂度随输入维度$p$指数增长——高阶交互项（$|S|>2$）因内存和时间限制在实际中几乎无法被纳入。

本文提出Bayesian-TPNN，将分量索引集$S_k$和分量数$K$视为可学习的架构参数，通过分层贝叶斯先验（节点稀疏先验$\pi(K=k)\propto\exp(-C_0 k\log n)$与边稀疏先验）和步进式MCMC算法在参数空间中进行随机搜索。核心机制是：步进式移动（Stepwise move）通过复制现有节点并添加一条边，自然生成比被复制节点高一阶的交互项，从而在不牺牲预测精度的前提下有效探测高阶交互结构。论文同时证明了预测模型及各分量的后验一致性。

实验表明，Bayesian-TPNN在回归和分类任务上的预测精度与最佳基线ANOVA-TPNN相当（ABALONE数据集RMSE：2.053 vs. 2.051），在MADELON分类任务上AUROC达到0.854，显著优于XGB（0.616）和BART（0.595）。在概念瓶颈模型（CBM）的图像分类中，仅使用5个概念即超越10个概念的线性模型（CelebA-HQ AUROC：0.936 vs. 0.899）。消融实验进一步验证了步进式移动和非均匀输入重要性分布$p_{\text{input}}$对性能的关键作用。



复杂数据建模中，理解输入变量之间的交互结构往往是科学发现的核心需求。函数型ANOVA（functional ANOVA）提供了一种将多元回归函数唯一分解为各阶交互分量的理论框架：

$$f(\mathbf{x}) = \sum_{S \subseteq [p]} f_S(\mathbf{x}_S)$$

其中每个分量 $f_S$ 满足和为零条件（sum-to-zero condition），确保分解的唯一性。这一框架天然适合解释“哪些变量组合驱动了预测”，在生物统计、金融风控、图像语义理解等领域具有广泛的应用前景。

### 现有方法的瓶颈

近年来，基于神经网络的ANOVA模型（如ANOVA-TPNN）通过专门设计的TPNN基函数实现了对和为零条件的满足，同时保持了神经网络的表达能力。然而，这类频繁式方法存在一个根本性的瓶颈：**必须预先指定所有可能的分量集合 $S$**。

具体而言，若输入维度为 $p$，要捕捉最高 $d$ 阶交互，需要枚举所有满足 $|S| \le d$ 的子集。当 $d>2$ 时，组合数量随 $p$ 指数增长，导致计算复杂度和内存需求在中等维度上就已不可承受。这意味着，传统方法实际上被限制在一阶（主效应）或二阶交互的估计中，**高阶交互项因计算资源约束而被系统性忽略**——而这些高阶交互在基因调控网络、金融因子联动等场景中恰恰可能是最关键的结构。

### 本文的切入思路

Bayesian-TPNN 的核心洞察在于：**将架构本身视为可学习的参数**。与其预先枚举所有可能的 $S$，不如在贝叶斯推断框架下，通过MCMC算法在参数空间中进行随机搜索，动态决定分量的数量 $K$ 以及每个分量对应的变量索引集 $S_k$。

这一设计的关键机制包括：

- **分层贝叶斯先验**：对节点数 $K$ 施加鼓励稀疏的先验 $\pi(K=k) \propto \exp(-C_0 k \log n)$，对边结构通过变量选择概率 $p_{\text{input}}$ 进行引导，从而在探索高阶交互的同时抑制过参数化。
- **步进式MCMC搜索**：通过“复制现有节点并添加一条边”的步进移动（Stepwise move），新节点自然地比被复制节点多一个变量，从而以增量方式探测高一阶的交互——这避免了从零开始枚举高阶组合的指数代价。
- **后验一致性保证**：论文从理论上证明了预测模型及各分量的后验一致性，为架构搜索的统计可靠性提供了形式化背书。

这一思路将“架构学习”从组合爆炸的困境中解放出来，使得在不牺牲预测精度的前提下获得可解释的高阶交互估计成为可能。



## 核心方法与创新机理

Bayesian-TPNN 的核心创新在于将函数型ANOVA模型的**架构参数化**，并通过**分层贝叶斯推断与步进式MCMC搜索**实现对分量索引集 $S_k$ 和分量数 $K$ 的联合学习，从而突破了传统神经ANOVA模型必须预定义所有可能分量的根本瓶颈。

### 瓶颈突破：从预定义分量到可学习架构

传统神经ANOVA模型（如ANOVA-TPNN）要求预先指定所有可能的分量 $S \subseteq [p]$（通常限制 $|S| \le d$），导致计算复杂度随输入维度 $p$ 指数增长。当 $p$ 较大时，高阶交互项（$|S| > 2$）因内存和时间限制几乎无法被纳入，这构成了该类方法的核心瓶颈。

Bayesian-TPNN 通过一个关键的设计转变解决了这一问题：**将分量索引集 $S$ 和分量数 $K$ 视为可学习的架构参数**，而非固定的预定义列表。具体而言：

> “instead of fixing $S$, we treat $S$ also as learnable parameters ... we adopt a Bayesian approach in which $K$ and $S_k$s are explored via an MCMC algorithm”

这一转变使得模型能够根据数据自适应地探索真正相关的交互结构，而非在所有可能的分量上浪费计算资源。

### Changed Slots：两个关键差异维度

与基线方法ANOVA-TPNN相比，Bayesian-TPNN在两个核心维度上发生了根本性变化：

| 维度 | 基线（ANOVA-TPNN） | 提出方法（Bayesian-TPNN） |
|------|-------------------|--------------------------|
| **分量索引集 $S$** | 预先指定所有 $S \subseteq [p]$，$|S| \le d$，固定列表 | 通过MCMC动态学习每个分量的 $S_k$（随机生成或步进扩展） |
| **训练方式** | 基于梯度的参数优化（如Adam） | 分层贝叶斯推断：MCMC采样架构（$K, S_k$）及连续参数（Metropolis-Hastings + Langevin动力学） |

这两个 changed slots 并非孤立存在，而是通过**分层贝叶斯先验**和**步进式MCMC搜索**形成了一个有机整体。

### 核心机制：步进式搜索与分层先验的协同

Bayesian-TPNN 的架构探索依赖于两个相互配合的机制：

**1. 分层贝叶斯先验（双重稀疏性）**

模型在节点层面和边层面施加了双重稀疏先验：
- **节点稀疏**：分量数 $K$ 的先验为 $\pi(K=k) \propto \exp(-C_0 k \log n)$，其中 $C_0 > 0$ 控制稀疏程度，鼓励模型使用较少的分量。
- **边稀疏**：每个分量的索引集 $S_k$ 通过MCMC随机探索，自然倾向于发现真正有贡献的交互结构。

这种双重稀疏性使得模型在保持表达能力的同时避免过参数化。

**2. 步进式MCMC搜索（Stepwise Move）**

步进式搜索是Bayesian-TPNN区别于简单随机搜索的核心设计。其关键操作是：**复制一个现有节点并为其添加一条新边**。这一设计的精妙之处在于：

> “The stepwise search adds a new node by first copying one of existing nodes and add an edge. By doing so, a newly added node has one more edges than the copied node and thus corresponds to an interaction whose order is larger than the copied one by 1.”

这意味着模型可以在保持已有结构稳定性的前提下，**逐步探测更高阶的交互**——从主效应到二阶交互，再到三阶、四阶交互，每一步只增加一条边。这种“爬坡”式探索策略避免了直接在高维空间中盲目搜索高阶交互的低效性。

消融实验证实了这一设计的决定性作用：移除步进式移动后，MADELON数据集上的AUROC从0.854降至0.820，校准误差ECE从0.076升至0.106（Table 15），表明步进式搜索对发现高阶交互结构至关重要。

### 理论保障：后验一致性

Bayesian-TPNN 不仅在经验上有效，还提供了理论保证。论文证明了**对每个分量的后验一致性**：

$$ \pi_{\xi}\left(f : \|f_{0,S} - f_S\|_{2,n} > \varepsilon \mid \mathbf{X}^{(n)}, Y^{(n)}\right) \to 0 $$

这意味着随着样本量增加，每个函数型ANOVA分量的后验分布会收敛到真实分量，为模型的可解释性提供了严格的统计基础。这一性质是传统基于优化的神经ANOVA方法所缺乏的。

### 创新总结

Bayesian-TPNN 的核心创新可归纳为一条清晰的因果链：**将架构参数化 → 用分层贝叶斯先验施加双重稀疏性 → 通过步进式MCMC实现从低阶到高阶的渐进探索 → 在不牺牲预测精度的前提下获得可解释且理论上一致的分量估计**。这一设计使得模型能够处理传统方法无法触及的高阶交互（如MADELON数据中发现的四阶交互），同时保持了与最佳基线相当甚至更优的预测性能。



![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/001_Figure_1.jpg]]

Bayesian-TPNN 将函数型ANOVA分解与贝叶斯架构搜索统一为一个端到端的可解释回归/分类框架。其核心 pipeline 由四个耦合模块构成，输入为观测数据 $\{(\mathbf{x}_i, y_i)\}_{i=1}^n$，输出为满足和为零条件的可解释分量集合 $\{f_{S_k}(\mathbf{x}_{S_k})\}_{k=1}^K$ 及其后验不确定性。

**瓶颈驱动**：传统神经ANOVA模型（如ANOVA-TPNN）必须预先指定所有可能的分量索引集 $S\subseteq[p]$，导致计算复杂度随输入维度 $p$ 指数增长，高阶交互项（$|S|>2$）因内存和时间限制难以被纳入。Bayesian-TPNN 将分量索引集 $S_k$ 和分量数 $K$ 视为可学习的架构参数，通过 MCMC 算法在参数空间中进行随机搜索，从根本上规避了预定义所有分量的组合爆炸问题。

**模块关系与数据流**：

1. **TPNN 基函数层**：对每个分量 $k$，以输入变量子集 $\mathbf{x}_{S_k}$、偏置 $\mathbf{b}_{S_k,k}$ 和尺度 $\Gamma_{S_k,k}$ 为参数，生成满足和为零条件的基函数输出 $\phi(\mathbf{x}|\Theta_k)$。其乘积形式为：

   $$\phi(\mathbf{x}_S|S,\mathfrak{B}_{S,k},\mathfrak{R}_{S,k}) = \prod_{j\in S} \left(1-\sigma(\frac{x_j-b_{S,j,k}}{\gamma_{S,j,k}})+c_j \sigma(\frac{x_j-b_{S,j,k}}{\gamma_{S,j,k}})\right)$$

   其中修正项 $c_j$ 强制满足和为零条件，确保函数方差分解的唯一性。

2. **加权求和层**：将 $K$ 个基函数输出加权求和，得到回归函数 $f(\mathbf{x}) = \sum_{k=1}^{K} \beta_k \phi(\mathbf{x}|\Theta_k)$，并通过指数族似然连接观测 $y$：

   $$q_{f(\mathbf{x}), \eta}(y) = \exp\left(\frac{f(\mathbf{x}) y - A(f(\mathbf{x}))}{\eta} + S(y, \eta)\right)$$

3. **架构采样器**：通过 MCMC 的 Metropolis-Hastings 步骤更新 $K$ 和 $S_k$，包含四种操作——随机生成新节点、步进式扩展（复制现有节点并增加一条边，使交互阶数自然提升 1）、删除节点、更改节点边集。步进式移动是探测高阶交互的关键机制，在保持模型稳定性的同时避免了对所有高阶组合的穷举搜索。

4. **连续参数采样器**：在给定架构下，使用 Langevin 动力学的 MH 算法更新连续参数 $\mathbf{b}, \gamma, \beta$ 及噪声参数 $\eta$，实现架构与参数的联合后验推断。

**先验结构**：框架采用分层贝叶斯先验——节点数 $K$ 服从稀疏先验 $\pi(K=k) \propto \exp(-C_0 k \log n)$，鼓励紧凑的模型结构；边集 $S_k$ 通过预训练的重要性分布 $p_{\mathrm{input}}$（基于 XGB 特征重要性或 DNN 的全局 SHAP 值）引导搜索方向，使高阶交互的探测更具针对性。论文证明了对每个分量的后验一致性，为推断提供了理论保证。



Bayesian-TPNN 的核心架构由三个关键模块构成：满足和为零条件的 TPNN 基函数、加权求和层，以及将分量架构视为可学习参数的 MCMC 采样器。以下逐一展开。

### TPNN 基函数：强制和为零条件

函数型 ANOVA 模型要求每个分量 $f_S(\mathbf{x}_S)$ 满足积分约束：

$$\forall j \in S \; \forall \mathbf{x}_{S\setminus\{j\}}, \int_{\mathcal{X}_j} f_S(\mathbf{x}_S) \mu_j(d x_j) = 0 \quad \text{(Eq. 3)}$$

该条件保证了函数方差分解的唯一性。TPNN 是专门设计以满足此条件的神经网络基函数，其形式为乘积结构：

$$\phi(\mathbf{x}_S|S,\mathfrak{B}_{S,k},\mathfrak{R}_{S,k}) = \prod_{j\in S} \left(1-\sigma\left(\frac{x_j-b_{S,j,k}}{\gamma_{S,j,k}}\right)+c_j \sigma\left(\frac{x_j-b_{S,j,k}}{\gamma_{S,j,k}}\right)\right) \quad \text{(Eq. 5)}$$

其中 $\sigma(\cdot)$ 为 sigmoid 函数，$b_{S,j,k}$ 为偏置参数，$\gamma_{S,j,k}$ 为尺度参数。修正项 $c_j$ 的定义为：

$$c_j(b,\gamma) := -\frac{1 - \int_{\mathcal{X}_j} \sigma\left(\frac{x_j-b}{\gamma}\right) \mu_{n,j}(dx_j)}{\int_{\mathcal{X}_j} \sigma\left(\frac{x_j-b}{\gamma}\right) \mu_{n,j}(dx_j)}$$

该修正项强制每个因子在边缘分布 $\mu_{n,j}$ 下的积分为零，从而保证整个乘积形式的分量满足和为零条件。这一设计使得每个基函数天然对应一个合法的 ANOVA 分量，无需事后校正。

### 加权求和层与最终模型

给定 $K$ 个基函数，回归函数由加权求和构成：

$$f(\mathbf{x}) = \sum_{k=1}^{K} \beta_k \phi(\mathbf{x}|\Theta_k) \quad \text{(Eq. 8)}$$

其中 $\Theta_k = (S_k, \mathbf{b}_{S_k,k}, \Gamma_{S_k,k})$ 封装了第 $k$ 个分量的索引集和连续参数，$\beta_k$ 为权重系数。该形式与函数型 ANOVA 分解 $f(\mathbf{x}) = \sum_{S \subseteq [p]} f_S(\mathbf{x}_S)$（Eq. 4）一一对应，每个基函数 $\phi(\mathbf{x}|\Theta_k)$ 即对应一个分量 $f_{S_k}(\mathbf{x}_{S_k})$。

### 似然函数：指数族框架

模型假设响应变量 $Y_i$ 在给定输入 $\mathbf{x}_i$ 下服从指数族分布：

$$q_{f(\mathbf{x}), \eta}(y) = \exp\left(\frac{f(\mathbf{x}) y - A(f(\mathbf{x}))}{\eta} + S(y, \eta)\right) \quad \text{(Eq. 2)}$$

其中 $f(\mathbf{x})$ 为回归函数（自然参数），$A(\cdot)$ 为对数配分函数，$\eta$ 为冗余参数（如高斯噪声方差 $\sigma^2$）。论文主要讨论高斯似然（回归）和逻辑回归似然（分类）两种情形。

### 分层贝叶斯先验：稀疏性诱导

Bayesian-TPNN 通过分层先验实现架构的自动稀疏化。节点数 $K$ 的先验鼓励模型使用较少的分量：

$$\pi(K=k) \propto \exp(-C_0 k \log n) \quad \text{(Eq. 9)}$$

其中 $C_0 > 0$ 控制稀疏程度：$C_0$ 越大，后验倾向于更小的 $K$。这一设计与 mBNN 的节点稀疏先验思路一致，但 Bayesian-TPNN 进一步将边稀疏（即每个分量的索引集 $S_k$）也纳入先验——通过 MCMC 动态学习 $S_k$，而非预定义所有可能子集。

连续参数的先验设定为：偏置 $b_{j,k} \sim \text{Uniform}(0,1)$，尺度 $\gamma_{j,k} \sim \text{Gamma}(a_\gamma, b_\gamma)$，噪声方差 $\sigma^2 \sim \text{IG}(v/2, v\lambda/2)$。

### MCMC 架构采样器：核心创新

区别于传统 ANOVA-TPNN 必须预先指定所有分量索引集 $S$，Bayesian-TPNN 将 $K$ 和 $S_k$ 视为可学习参数，通过 MCMC 算法在参数空间中随机搜索。采样策略分为两层：

1. **更新 $K$**：通过 Metropolis-Hastings 步骤随机添加或删除节点。添加新节点时，其索引集 $S_{K+1}$ 从预训练的重要性分布 $p_{\text{input}}$ 中采样生成，其中 $p_{\text{input}}(j) \propto \omega_j$，$\omega_j$ 为输入变量 $j$ 的重要性度量（如 XGB 特征重要性或 DNN 的全局 SHAP 值）。

2. **更新 $S_k$ 和连续参数**：对每个现有节点 $k$，通过步进式移动（stepwise move）修改其架构。步进式移动包含三种操作——添加边、删除边、更改边——其核心机制是：**复制一个现有节点并增加一条边**，使得新节点的交互阶数比被复制节点高 1。这自然生成了高阶交互项，避免了预定义所有高阶组合的指数级开销。

接受概率遵循标准 MH 形式：

$$\mathcal{P}_{\text{accept}} = \min\left\{1, \frac{\mathcal{L}(\Theta_k^{\text{new}}, \beta_k, \lambda_k, \eta)}{\mathcal{L}(\Theta_k, \beta_k, \lambda_k, \eta)} \frac{\pi(\Theta_k^{\text{new}})}{\pi(\Theta_k)} \frac{q(\Theta_k|\Theta_k^{\text{new}})}{q(\Theta_k^{\text{new}}|\Theta_k)}\right\}$$

连续参数（$b, \gamma, \beta, \eta$）在给定架构下通过 Langevin 动力学 MH 更新，利用梯度信息加速收敛。

### 理论保证：后验一致性

论文证明了每个分量 $f_S$ 的后验一致性：在适当条件下，当样本量 $n \to \infty$ 时，

$$\pi_{\xi}\left(f : \|f_{0,S} - f_S\|_{2,n} > \varepsilon \mid \mathbf{X}^{(n)}, Y^{(n)}\right) \to 0$$

即估计分量与真实分量 $f_{0,S}$ 的 $L_2$ 距离超过 $\varepsilon$ 的后验概率趋于零。该结果为 MCMC 采样的统计可靠性提供了理论支撑，但需注意其假设基函数满足关于均匀分布的和为零条件。

### 关键瓶颈与因果机制

传统 ANOVA-TPNN 的根本瓶颈在于：必须预定义所有可能的分量索引集 $S \subseteq [p], |S| \le d$，导致计算复杂度随 $p$ 指数增长，高阶交互（$|S| > 2$）因内存和时间限制难以被纳入。Bayesian-TPNN 通过将 $S_k$ 和 $K$ 视为可学习架构参数，利用步进式 MCMC 搜索（复制节点 + 增加边）在保持模型稳定性的同时有效探测高阶交互，从而在不牺牲预测精度的前提下获得可解释的分量估计。



## 实验与关键发现

### 主要预测性能

Bayesian-TPNN在回归与分类任务上均展现出强竞争力。Table 1汇总了各数据集上的预测精度：在ABALONE回归任务上，Bayesian-TPNN的RMSE为2.053 (0.26)，与最佳基线ANOVA-TPNN（2.051）几乎持平，表明架构可学习并未牺牲预测精度。在分类任务上，Bayesian-TPNN优势更为明显——MADELON数据集的AUROC达到0.854 (0.007)，而XGB仅为0.616，BART为0.595，mBNN为0.519，说明模型在高阶交互主导的分类场景中显著优于黑箱树模型和掩码贝叶斯网络。

![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/002_Table_1.jpg]]
*Table 1: The averaged prediction accuracies (the standard errors) on real datasets*

在不确定性量化方面，Table 2比较了贝叶斯模型的CRPS、NLL和ECE。Bayesian-TPNN在ABALONE上的CRPS为1.372、NLL为2.260，均优于mBNN和BART；在FICO数据集上ECE仅为0.036，校准性能突出。这表明分层贝叶斯先验与MCMC架构搜索不仅保持了预测精度，还提供了更可靠的预测分布。

### 分量选择与可解释性

Bayesian-TPNN的核心优势在于自动发现数据中的交互结构。Table 3展示了合成数据集上的分量选择性能：在一阶函数$f^{(1)}$上，Bayesian-TPNN的一阶AUROC达到1.000 (0.000)，完美识别所有主效应；在包含三阶交互的$f^{(3)}$上，三阶AUROC仍保持0.985 (0.010)，而ANOVA-T²PNN和NA²M因预定义分量限制无法有效捕获高阶交互。

![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/004_Table_3.jpg]]
*Table 3: Performance of component selection on synthetic datasets*

在真实数据集上，模型同样展现了发现有意义交互的能力。Table 4显示，MADELON数据集中最重要的分量是一个四阶交互(49, 242, 319, 339)，其归一化重要性分数为1.000。Figure 2进一步可视化了BOSTON数据集上主效应的函数曲线及95%可信区间，为每个输入变量的非线性效应提供了直观解释。

### 概念瓶颈模型应用

Table 5展示了Bayesian-TPNN在概念瓶颈模型（CBM）中的应用。在CELEBA-HQ图像分类任务上，Bayesian-TPNN作为最终分类器达到AUROC 0.936 (0.002)，显著优于Linear模型的0.899。值得注意的是，Bayesian-TPNN仅使用5个概念即超越了使用10个概念的Linear模型，说明其自动发现的交互结构能更高效地利用概念信息。

![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/010_Table_5.jpg]]
*Table 5: Prediction performance with CBM on image datasets. Table 5 presents the averages and standard errors of AUROCs when Bayesian-TPNN, ANOVA-T2PNN, NA2M, and Linear model are used in the final classifier. Among them, Bayesian-TPNN*

### 消融实验

**先验稀疏性控制。** 参数$C_0$控制节点数$K$的稀疏程度（Figure 3）：增大$C_0$使$K$减小，模型更简洁但RMSE上升；减小$C_0$允许更多分量，预测性能改善但可解释性下降。这为精度-可解释性权衡提供了连续调节机制。

**输入变量先验$p_{\mathrm{input}}$的影响。** Table 12对比了均匀分布（UBayesian-TPNN）与基于预训练XGB重要性的非均匀分布：MADELON数据集上AUROC从0.739 (0.002)跃升至0.854 (0.007)，提升超过0.1。这说明当真实交互涉及特定变量时，引导搜索方向至关重要；反之，若重要性分布不准确，性能会显著退化，这是方法的一个关键依赖。

![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/019_Table_12.jpg]]
*Table 12: Prediction performance on MADELON dataset*

**步进式移动的贡献。** Table 15消融了Stepwise move：移除该操作后，AUROC从0.854降至0.820，ECE从0.076升至0.106，NLL从0.479升至0.650。步进式移动通过复制现有节点并添加一条边，自然生成比原节点高一阶的交互，是探测高阶交互的核心机制。

![[assets/figures/papers/iclr26_0009_cvZhXILRLI_Bayesian_Neural_Networks_for_Functional_ANOVA_Mo/figures/022_Table_15.jpg]]
*Table 15: Results of performance with and without Stepwise move*

**Langevin步长敏感性。** Table 11显示步长选择对RMSE影响显著：最优步长0.001时RMSE为2.053，步长增至0.5时RMSE飙升至4.578。这表明连续参数采样对提议分布尺度敏感，需要仔细调节。

**超参数$a_\gamma$和$b_\gamma$。** Table 10展示了Gamma先验参数对预测性能的影响：在$a_\gamma=1$、$b_\gamma=0.01$时取得最优值3.182，偏离该组合时性能下降，但整体波动可控。

### 失败模式与局限

1. **对$p_{\mathrm{input}}$的依赖。** 当预训练重要性分布不准确时（如使用均匀分布），高阶交互的搜索效率大幅下降，MADELON上AUROC损失超过0.1。目前$p_{\mathrm{input}}$在MCMC过程中固定不变，无法自适应更新。

2. **超参数敏感性。** 步进移动概率$q_{add}$、Langevin步长等超参数目前需手动调节，缺少自动化选择策略。步长过大直接导致采样发散。

3. **计算开销。** 虽然避免了预定义所有分量的指数级复杂度，但在高维场景（如500维基因表达数据）上MCMC采样仍需秒到分钟级时间，未与深度集成方法全面对比。

4. **似然假设限制。** 当前仅验证了高斯和逻辑回归似然，复松回归等扩展的普适性尚未完全验证。

### 收敛性

Figure 6展示了MCMC迭代过程中RMSE的收敛轨迹。Bayesian-TPNN的RMSE随迭代快速下降并趋于稳定，收敛速度与mBNN相当，表明架构空间中的随机搜索在实际运行中是可行的。



## 定位与知识库关联

### 与基线方法的关系

Bayesian-TPNN 直接解决 ANOVA-TPNN 的核心瓶颈：后者必须预先指定所有可能的分量 $S\subseteq[p], |S|\le d$，导致计算复杂度随输入维度 $p$ 指数增长，高阶交互项（$|S|>2$）因内存和时间限制难以被纳入。Bayesian-TPNN 将分量索引集 $S_k$ 和分量数 $K$ 视为可学习的架构参数，通过 MCMC 算法在参数空间中进行随机搜索，避免预定义所有分量。这一设计使得模型可以从数据中自适应地发现哪些交互项是必要的，而非依赖人工预设。

与 NAM（神经加性模型）相比，Bayesian-TPNN 不仅能够估计主效应和二阶交互，还可以通过步进式 MCMC 移动自然生成高阶交互：步进搜索通过复制现有节点并添加一条边来创建新节点，使得新节点的交互阶数比被复制节点高 1。这在高阶交互主导的数据集（如 MADELON 中识别出 4 阶交互）上具有显著优势。

与 mBNN（掩码贝叶斯神经网络）相比，两者均采用贝叶斯框架并支持节点稀疏性学习，但 Bayesian-TPNN 额外引入了边稀疏性（即学习每个分量的 $S_k$），从而直接产生可解释的 ANOVA 分量估计，而 mBNN 仅提供节点级稀疏性，缺乏分量级别的结构化解释能力。此外，Bayesian-TPNN 证明了每个分量的后验一致性，为分量估计提供了理论保证。

与 BART 和 XGB 等黑箱树模型相比，Bayesian-TPNN 在保持竞争性预测性能的同时，提供了函数型 ANOVA 分解的结构化可解释性，能够直接输出各分量的函数曲线及 95% 可信区间。

### 适用边界

**适用场景**：
- 需要同时获得预测性能和结构化可解释性的回归/分类任务
- 数据中存在未知的高阶交互效应
- 需要不确定性量化（分量级和预测级）
- 中小规模表格数据（论文验证的数据集维度从 4 到 500 维）

**不适用或需谨慎的场景**：
- 极高维稀疏数据：MCMC 采样在 500 维基因表达数据上仍需秒到分钟级采样，未与深度集成方法全面对比
- 对 $p_{\mathrm{input}}$ 分布高度敏感：当该预训练重要性分布不准确时（如使用均匀分布），MADELON 数据集上 AUROC 从 0.854 降至 0.739
- 当前仅验证了高斯似然（回归）和逻辑回归似然（分类），复松回归等扩展的普适性未完全验证

### 局限与开放问题

**已知局限**：
1. **对 $p_{\mathrm{input}}$ 的依赖**：搜索高阶交互依赖预训练的重要性分布（如 XGB 特征重要性或 DNN 的 SHAP 值），当该分布质量差时性能显著下降。目前缺乏在 MCMC 过程中自适应更新 $p_{\mathrm{input}}$ 的机制。
2. **超参数敏感性**：步进移动的超参数 $M$、$q_{add}$、$q_{delete}$、$q_{change}$ 需要人工调节，Langevin 步长选择对 RMSE 敏感（过大步长 0.5 导致 RMSE 升至 4.578），目前未给出自动化选择策略。
3. **计算开销**：虽低于 ANOVA-T²PNN，但在高维大数据上仍有一定开销，未与轻量级集成方法全面对比。
4. **似然族限制**：当前仅讨论高斯和逻辑回归似然，理论分析尚未扩展到非指数族似然（如重尾噪声）。

**开放问题**：
- 能否在 MCMC 过程中自适应更新 $p_{\mathrm{input}}$（如基于当前采样的边使用频率）？
- 如何选择最优的步进选择概率 $M$、添加/删除/更改概率 $q_{add}$ 等超参数？是否存在数据驱动的自适应策略？
- Bayesian-TPNN 与深度神经网络集成的组合是否能在保持可解释性的同时进一步提高预测性能？
- 理论分析是否可以扩展到非指数族似然（如重尾噪声）？后验一致性证明是否仍然成立？



## 原文 PDF

![[paperPDFs/ICLR_2026/Bayesian_Neural_Networks_for_Functional_ANOVA_Model.pdf]]
