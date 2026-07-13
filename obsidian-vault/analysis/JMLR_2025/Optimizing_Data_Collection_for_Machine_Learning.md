---
title: "Optimizing Data Collection for Machine Learning"
type: paper
paper_level: A
venue: JMLR
year: 2025
pdf_ref: paperPDFs/JMLR_2025/Optimizing_Data_Collection_for_Machine_Learning.pdf
project_link: null
code_link: null
aliases:
- LOCL
- ODCML
tags:
- JMLR_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将数据收集形式化为一个随机最优控制问题，其中所需最小数据量被视为随机变量；通过bootstrapping估计该变量的概率分布，并对期望成本进行风险优化，从而引入可调的安全边际。"
primary_logic: "通过优化而非直接估计，结合对数据需求分布的不确定性量化，可以显著降低未能达到性能目标的风险，同时将收集成本控制在接近最优的水平。"
claims:
- "传统标度律外推方法即使在误差较小时也会导致显著的过采与欠采。"
- "LOC在12/18的设置中将失败率降低至10%以下，而回归基线在15/18的设置中失败率超过30%。"
- "LOC通过优化使收集的数据量始终略高于最小需求，从而避免欠采。"
- "单轮情况下LOC等价于收集数据需求分布的(1-ε)分位数。"
---

# Optimizing Data Collection for Machine Learning

> [!tip] 核心洞察
> 通过优化而非直接估计，结合对数据需求分布的不确定性量化，可以显著降低未能达到性能目标的风险，同时将收集成本控制在接近最优的水平。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 优化数据收集以用于机器学习 |
| 英文题名 | Optimizing Data Collection for Machine Learning |
| 会议/期刊 | JMLR 2025 |
| Links | [paper](https://www.jmlr.org/papers/v26/23-0292.html) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Learn-Optimize-Collect (LOC) |
| Dataset | 多个数据集（CIFAR-10, CIFAR-100, ImageNet, VOC, BDD100K）, 同上, CIFAR-100 (K=2, 半监督) |

> [!tip] 效果简介
> - 多个数据集（CIFAR-10, CIFAR-100, ImageNet, VOC, BDD100K） 上，平均失败率（Failure Rate） 为 LOC: 12/18设置中<10%，对比 Power Law Regression: 15/18设置中>30%，变化 约2倍降低，许多情况降至0%。
> - 同上 上，平均成本比（Cost Ratio） 为 LOC: 12/18设置中<0.5（额外成本<50%），对比 Power Law Regression: 未明确给出，但LOC保持较低，变化 在保持低失败率的同时，成本比几乎始终低于1。
> - CIFAR-100 (K=2, 半监督) 上，失败率 为 LOC: 显著低于回归，对比 Power Law Regression: 较高，变化 尤其在T=5时差距明显。

## 概要

现代机器学习系统的性能高度依赖于训练数据的规模与质量，但实际数据收集往往面临成本高昂、来源多样且目标性能不确定等挑战。传统做法——收集“尽可能多”的数据——缺乏对成本效益的量化考量，而基于标度律（scaling law）外推的方法虽然试图估算达到目标性能所需的最小数据量，却对估计误差极度敏感：即使很小的曲线拟合偏差，也会在平坦的标度律曲线上被急剧放大，导致严重的数据过采或欠采（Figure 1）。

本文的核心贡献在于将数据收集重新形式化为一个**随机最优控制问题**。作者提出，所需的最小数据量 $D^*$ 不应被视为一个确定性的点估计，而应被建模为一个随机变量——其分布反映了标度律拟合和性能评估中的不确定性。在此基础上，数据收集的目标从“准确估计 $D^*$”转变为“在给定不确定性下优化期望成本”，从而引入可调的安全边际来规避欠采风险。这一思想催生了 **Learn-Optimize-Collect (LOC)** 框架：通过 bootstrapping 估计数据需求分布 $F(q)$，再以投影梯度下降求解一个最小化期望收集成本（含未达目标的惩罚 $P$）的随机优化问题，最终在多轮模型预测控制（MPC）循环中逐步收敛到接近最优的收集量。

在方法论定位上，LOC 区别于三类现有工作：（1）**Power Law Regression**（Rosenfeld et al., ICLR 2020）等直接外推方法，它们仅依赖点估计而忽略不确定性；（2）**Correction-based Power Law Regression**（Mahmood et al., CVPR 2022）等带有校正因子的改进方法，虽试图补偿估计偏差，但仍缺乏对分布尾部风险的显式建模；（3）一般的主动学习或数据选择方法，它们关注“选哪些数据”而非“收集多少数据”。LOC 首次将数据需求的不确定性量化与成本敏感的随机优化统一在一个框架内，并可自然地扩展至多数据源场景（通过加性标度律模型与多变量优化）。

实验覆盖 CIFAR-10、CIFAR-100、ImageNet、VOC 和 BDD100K 等多个数据集与任务，结果表明：在 18 组设置中，LOC 将平均失败率降至 10% 以下的有 12 组，而回归基线在 15 组设置中失败率超过 30%（Table 2）。同时，LOC 在保持极低失败率的前提下，额外收集成本通常不超过最优成本的 50%。这一性能优势在双数据源、不同成本比例、主动学习策略以及新类别添加等扩展场景下均得到验证（Table 3, Table 4）。此外，LOC 对成本参数 $c$ 和惩罚参数 $P$ 在 1 至 3 个数量级范围内的变化表现出良好的鲁棒性（Figure 6）。

值得注意的是，LOC 的理论分析揭示了其决策机制的简洁本质：在单轮场景下，LOC 等价于收集数据需求分布的 $(1-\varepsilon)$ 分位数（Theorem 3），其中 $\varepsilon$ 由成本与惩罚的相对比例决定——这为方法的可解释性提供了坚实的理论基础。

尽管 LOC 在实验中展现出显著优势，该方法仍存在若干边界条件：它假设学习曲线单调非递减（在主动学习或半监督场景下可能不成立）；对于超过两个数据源的高维场景，ground truth 构建的计算成本呈指数增长；惩罚参数 $P$ 的选择仍需领域知识，极端设置下可能产生不切实际的收集建议。这些限制指出了未来工作中纳入隐私与公平约束、处理非平稳数据分布等开放方向。



### 数据收集的现实困境

现代机器学习系统的性能高度依赖数据规模，但数据收集本身并非免费——标注成本、采集难度、隐私约束等因素使得“收集多少数据才够”成为一个具有重大经济意义的决策问题。实践中，从业者通常面临一个两难选择：收集过少，模型无法达到目标性能，导致项目失败；收集过多，则浪费大量资源，压缩后续迭代的预算空间。

这一困境的核心在于 **数据需求量本身是未知的随机变量**——我们无法在收集之前确切知道需要多少数据才能让模型达到指定的性能阈值。因此，数据收集本质上是一个在不确定性下进行序贯决策的优化问题。

### 标度律外推的脆弱性

当前业界的主流做法依赖于**标度律（scaling laws）外推**：在少量初始数据上训练模型，拟合性能随数据量变化的参数曲线，然后外推估计达到目标性能所需的最小数据量。这一范式以 **Power Law Regression**（Rosenfeld et al., ICLR 2020）为代表，在多个数据密集型领域被广泛采用。

然而，这一方法的致命缺陷在于**对外推误差的极端敏感性**。图1（Figure 1）在ImageNet上的实验揭示了问题的严重性：即使标度律曲线在目标数据量附近仅存在≤6%的拟合误差，外推得到的数据需求估计值也可能从58万张（严重欠采）到300万张（严重过采）之间剧烈波动。这种不稳定性源于标度律曲线在高数据量区域趋于平坦——微小的斜率偏差在水平方向上被急剧放大，使得点估计几乎不可靠。

更根本地，标度律外推范式存在两个结构性缺陷：
- **忽略估计不确定性**：仅依赖点估计，无法量化“需要多少数据”这一核心变量的分布特征，因而无法进行风险调控。
- **缺乏多源成本建模**：当存在多种数据源（如有标签/无标签数据、不同采集渠道）且成本各异时，没有统一的框架来权衡来源选择与总量决策。

### 从“估计”到“优化”的范式转换

本文提出一个根本性的视角转换：**不应试图精确估计最小数据需求量，而应直接优化数据收集决策本身**。核心洞察在于：如果我们能够估计数据需求量的概率分布，就可以在期望意义上权衡收集成本与失败风险，从而通过引入可控的安全边际来规避欠采，同时避免过度收集。

这一思想被形式化为一个**随机最优控制问题**：将所需最小数据量 $D^*$ 视为随机变量，目标是最小化期望收集成本与失败惩罚的加权和。通过调节惩罚参数 $P$，决策者可以在“激进收集”（低成本但高失败风险）与“保守收集”（高成本但低失败风险）之间连续调控，实现与业务需求匹配的风险偏好。



## 核心方法与创新机理

### 从“估计-收集”到“学习-优化-收集”

传统数据收集方法遵循一个直观但脆弱的范式：先用当前数据拟合标度律（scaling law），外推出达到目标性能所需的最小数据量 $\mathbf{D}^*$，然后一次性收集该数量的数据。这一范式存在根本性缺陷——**标度律外推对估计误差极度敏感**。如 Figure 1 所示，在 ImageNet 上，即使拟合曲线在目标点 $q=900,000$ 处的误差不超过 6%，外推出的 $\hat{D}$ 也可能从 580,000 剧烈波动到 3,000,000，导致严重欠采（无法达标）或过采（浪费成本）。这一瓶颈的根源在于：标度律曲线在饱和区极度平坦，微小的垂直误差在水平方向上被急剧放大。

LOC（Learn-Optimize-Collect）从根本上改变了这一范式。其核心创新在于**将数据收集形式化为一个随机最优控制问题，并通过优化而非直接估计来决策**。具体而言，LOC 将所需最小数据量 $\mathbf{D}^*$ 视为随机变量，通过 bootstrapping 估计其概率分布 $F(\mathbf{q})$，然后求解一个以期望成本最小化为目标的随机优化问题：

$$\operatorname*{min}_{\mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T} \sum_{t=1}^T \mathbf{c}^{\top}(\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T))$$

其中 $P$ 是未达到性能目标的惩罚参数。这一目标函数的关键性质是：它不试图精确估计 $\mathbf{D}^*$，而是基于 $\mathbf{D}^*$ 的完整分布进行风险优化，从而在“收集不足的风险”与“过度收集的成本”之间取得最优权衡。

### 与基线方法的关键差异（Changed Slots）

**1. 数据收集决策方式：从点估计到分布优化**

- **基线（Power Law Regression, Rosenfeld et al., ICLR 2020）**：直接估计 $\mathbf{D}^*$ 的点值并收集该数量。当估计偏低时，模型无法达标；估计偏高时，成本浪费。
- **LOC**：估计 $\mathbf{D}^*$ 的完整分布 $F(\mathbf{q})$，并求解随机优化问题以最小化期望成本。Theorem 3 表明，在单轮情况下，LOC 的最优解等价于收集数据需求分布的 $(1-\varepsilon)$ 分位数，其中 $\varepsilon$ 由成本参数 $c$ 和惩罚参数 $P$ 共同决定。这意味着 LOC 天然地“多收集一点”以对冲不确定性，而非在点估计的刀刃上行走。

**2. 不确定性处理：从忽略到显式建模与风险调节**

- **基线**：忽略估计不确定性，仅依赖单次拟合的点估计。即使使用集成回归（Ensemble Regression）估计均值，也只是将不确定性平均掉，无法主动规避风险。
- **LOC**：通过 bootstrapping 对学习曲线进行重采样，对每次重采样拟合标度律并求解 $\mathbf{D}^*$，得到 $\mathbf{D}^*$ 的经验分布样本；随后使用核密度估计（KDE, $K=1$）或高斯混合模型（GMM, $K=2$）拟合其累积分布函数 $F(\mathbf{q})$。惩罚参数 $P$ 作为可调的安全边际，直接控制风险规避程度：$P$ 越大，LOC 越倾向于收集更多数据以避免失败。

**3. 多数据源处理：从无统一框架到加性标度律 + 多变量随机优化**

- **基线**：缺乏统一的多数据源收集框架，无法系统处理不同数据源的成本差异。
- **LOC**：采用加性标度律模型 $v(\mathbf{q}; \pmb{\theta}) = \theta_0 + \sum_{k=1}^K v_k(q_k; \pmb{\theta}_k)$，将多数据源的性能贡献分解为独立学习曲线之和。在此模型下，$\mathbf{D}^*$ 是一个向量值随机变量，LOC 的多变量随机优化可同时决定各数据源的最优收集量，并在不同相对成本下自动调整数据源间的分配比例（见 Figure 5 和 Table 3）。

### 方法流水线的模块化创新

LOC 的整体框架由四个模块构成，形成闭环的模型预测控制（MPC）循环：

1. **学习曲线统计收集**：通过对当前数据子采样并重新训练模型，获取学习曲线样本点（Algorithm 1, lines 4-7）。
2. **最小数据需求分布估计**：对学习曲线进行 bootstrapping 并拟合标度律，得到 $\mathbf{D}^*$ 的样本；通过 KDE 或 GMM 拟合 CDF（Section 4.2）。
3. **随机优化**：在当前估计的 $F(\mathbf{q})$ 下最小化期望收集成本，使用投影梯度下降求解（Algorithm 2）。
4. **模型预测控制循环**：每轮仅应用最优解的第一步，收集数据后更新统计并重新优化（Algorithm 3）。这种滚动优化的设计使 LOC 能随着数据增加不断修正对 $\mathbf{D}^*$ 的估计，逐步逼近真实需求。

### 理论洞察：单轮问题的解析解

在假设 $\mathbf{D}^*$ 服从正态分布 $\mathcal{N}(\hat{\mu}, \hat{\sigma}^2)$ 的条件下，单轮 LOC 问题存在闭式候选解（Proposition 5; Corollary 6）：

$$d_1^* = \max\{\hat{\mu} + \sqrt{2}\hat{\sigma}\sqrt{\log\frac{P}{c\hat{\sigma}\sqrt{2\pi}}} - q_0, 0\}$$

这一解析形式揭示了 LOC 的核心机制：最优收集量在估计均值 $\hat{\mu}$ 的基础上增加了一个与不确定性 $\hat{\sigma}$ 和惩罚-成本比 $P/c$ 成正比的安全边际项。当 $P$ 足够小（$P < c\hat{\sigma}\sqrt{2\pi}$）时，惩罚不足以抵消收集成本，最优策略是不收集任何数据（$d_1^* = 0$）；当 $P$ 增大时，安全边际随之扩大，体现了风险规避程度的可调性。



LOC（Learn-Optimize-Collect）将数据收集建模为一个多轮序贯决策问题，其核心pipeline由三个交替执行的模块构成：**学习曲线统计收集**、**最小数据需求分布估计**和**随机优化**，并通过模型预测控制（MPC）循环串联（Algorithm 3）。整体输入为用户指定的性能目标 $V^*$、数据源单位成本向量 $\mathbf{c}$、未达标惩罚 $P$、时间轮次 $T$ 以及初始数据量 $\mathbf{q}_0$；输出为每轮应收集的数据量决策 $\mathbf{q}_t^*$。

### 模块一：学习曲线统计收集

该模块负责获取当前数据量下的模型性能样本，为后续分布估计提供原始信号。具体流程（Algorithm 1, lines 4-7）为：对当前已拥有的数据集进行多次随机子采样，在每个子采样上重新训练模型并评估性能，从而得到一组 $(q, V)$ 观测点。这些点构成了学习曲线的经验样本，是标度律拟合的基础。

### 模块二：最小数据需求分布估计

该模块是LOC区别于传统点估计方法的关键。其输入为模块一产生的学习曲线样本，输出为最小数据需求量 $D^*$ 的概率分布 $F(q) = \Pr\{D^* \le q\}$。具体步骤为：

1. **Bootstrapping重采样**：对学习曲线样本进行bootstrap，生成多组重采样数据。
2. **标度律拟合**：在每组bootstrap样本上拟合标度律函数（如幂律、对数、反正切等，见Table 1），并求解达到目标性能 $V^*$ 所需的最小数据量，得到 $D^*$ 的多个估计值。
3. **分布拟合**：当数据源数量 $K=1$ 时，使用核密度估计（KDE）拟合 $D^*$ 的累积分布函数 $F(q)$；当 $K=2$ 时，使用高斯混合模型（GMM）建模多变量分布（Section 4.2; Appendix B.3）。

这一过程的本质是将点估计的不确定性显式化为一个概率分布——即使标度律拟合存在误差，分布 $F(q)$ 也能刻画“需要多少数据才够”的风险全貌（Figure 9展示了不同 $V^*$ 下 $D^*$ 估计值的直方图及拟合的CDF）。

### 模块三：随机优化

该模块以模块二输出的分布 $F(q)$ 为输入，求解以下期望成本最小化问题：

$$\min_{\mathbf{q}_1 \le \cdots \le \mathbf{q}_T} \sum_{t=1}^T \mathbf{c}^{\top}(\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T))$$

其中 $(1 - F(\mathbf{q}))$ 表示当前数据量 $\mathbf{q}$ 尚未达到 $D^*$（即未达标）的概率。该目标函数将每一轮的收集成本乘以“仍需继续收集”的概率，并在最后一轮加上未达标惩罚的期望值。优化使用投影梯度下降求解（Algorithm 2），约束为数据量单调非递减。

### 模型预测控制循环

上述三个模块在MPC框架下迭代运行（Algorithm 3）：每轮仅执行优化解的第一步（即收集 $\mathbf{q}_1^* - \mathbf{q}_0$ 的数据），实际收集后获得新的模型性能观测，更新学习曲线统计，重新估计 $F(q)$，并基于新的分布重新优化后续轮次的决策。这种“学习-优化-收集”的闭环设计使得LOC能够随着信息增加动态调整策略，避免一次性决策带来的风险。

### 关键假设

LOC的有效性建立在两个核心假设之上：
- **单调性假设**：模型性能随数据量单调非递减，这使得最优数据收集问题简化为公式（3）的形式（Section 3.1）。
- **绝对连续性假设**：$D^*$ 是绝对连续随机变量，具有可微的CDF $F(q)$ 和PDF $f(q)$（Assumption 2），这使得期望成本优化问题有良好的数学性质。

### 与传统方法的本质区别

传统方法（如**Power Law Regression**, Rosenfeld et al., ICLR 2020）直接估计 $D^*$ 的点值并收集该数量，完全忽略了估计不确定性。Figure 1（右）揭示了这种方法的脆弱性：在ImageNet上，标度律仅 $\le 6\%$ 的外推误差就导致估计值从真实的90万张偏离至58万张（欠采）或300万张（过采）。LOC通过将决策从“估计后收集”转变为“优化期望成本”，在分布层面权衡收集不足的风险与过度收集的成本，从根本上解决了这一瓶颈。



### 3.1 最优数据收集问题的形式化

LOC 将数据收集建模为一个随机最优控制问题。其核心在于将“达到目标性能所需的最小数据量”视为一个不可直接观测的**随机变量** $\mathbf{D}^*$，而非一个待估计的固定点值。

**最小数据需求**（Minimum Data Requirement）定义为在给定成本向量 $\mathbf{c}$ 下，达到目标性能 $V^*$ 所需的最小成本数据向量：

$$\mathbf{D}^* := \arg\min_{\mathbf{q}} \{\mathbf{c}^\mathsf{T} \mathbf{q} \mid V_{\mathbf{q}} \geq V^*\}$$

在单调性能假设下，多轮数据收集的优化目标可简化为：

$$\operatorname*{min}_{\mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T} \sum_{t=1}^T \mathbf{c}^\top (\mathbf{q}_t - \mathbf{q}_{t-1}) \mathbb{1}\{V_{\mathbf{q}_{t-1}} < V^*\} + P \mathbb{1}\{V_{\mathbf{q}_T} < V^*\}$$

其中 $\mathbf{q}_t$ 为第 $t$ 轮累计收集的数据量，$\mathbf{c}$ 为各数据源的单位成本，$P$ 为最终未达标时支付的罚金。该目标的核心直觉是：每轮仅在上一轮数据量尚未达标时才产生收集成本，最终若仍未达标则额外支付罚金。

### 3.2 标度律估计与不确定性量化

LOC 的“学习”模块通过标度律函数外推性能曲线。对于多数据源场景，采用**加性标度律模型**：

$$v(\mathbf{q}; \pmb{\theta}) := \theta_0 + \sum_{k=1}^K v_k(q_k; \pmb{\theta}_k)$$

该模型假设不同数据源对性能的贡献是可加的，$\theta_0$ 为基线性能，$v_k$ 为第 $k$ 个数据源的单变量标度律函数（可从 Table 1 中的幂律、对数、反正切等形式中选择）。

为量化估计的不确定性，LOC 对学习曲线进行 **bootstrapping**：对已有数据点进行重采样，拟合多条标度律曲线，每条曲线外推得到 $\mathbf{D}^*$ 的一个样本。随后通过核密度估计（KDE，$K=1$）或高斯混合模型（GMM，$K=2$）拟合 $\mathbf{D}^*$ 的累积分布函数 $F(\mathbf{q}) = \Pr\{\mathbf{D}^* \leq \mathbf{q}\}$。

### 3.3 随机优化与模型预测控制

将 $\mathbf{D}^*$ 视为随机变量后，原问题转化为**期望成本最小化**：

$$\operatorname*{min}_{\mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T} \sum_{t=1}^T \mathbf{c}^\top (\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T))$$

其中 $(1 - F(\mathbf{q}_{t-1}))$ 为第 $t-1$ 轮数据量仍不足以达标的概率。该目标通过投影梯度下降求解（Algorithm 2），在每轮仅执行最优解的第一步（即模型预测控制，MPC），收集数据后更新统计量并重新优化（Algorithm 3）。

### 3.4 单轮问题的解析解

在单轮（$T=1$）且假设 $\mathbf{D}^*$ 服从正态分布 $\mathcal{N}(\hat{\mu}, \hat{\sigma}^2)$ 的条件下，最优收集量具有解析形式：

$$d_1^* = \max\{\hat{\mu} + \sqrt{2}\hat{\sigma}\sqrt{\log\frac{P}{c\hat{\sigma}\sqrt{2\pi}}} - q_0, 0\}$$

该公式揭示了 LOC 的核心机制：最优收集量等于估计均值 $\hat{\mu}$ 加上一个与罚金 $P$、成本 $c$ 和估计不确定性 $\hat{\sigma}$ 相关的**安全边际**。当 $P$ 增大或 $\hat{\sigma}$ 增大时，安全边际增加，收集量趋于保守；当 $P$ 足够小时，最优策略可能是不收集任何数据（$d_1^* = 0$）。更一般地，Theorem 3 证明单轮 LOC 等价于收集数据需求分布的 $(1-\varepsilon)$ 分位数，其中 $\varepsilon$ 由成本与罚金的比值决定。



## 实验与关键发现

### 核心瓶颈与实验动机

基于标度律外推的传统数据收集方法存在一个根本性脆弱点：即使很小的曲线拟合误差，也会在平坦的标度律曲线上被急剧放大，导致严重的数据采多或采少。Figure 1在ImageNet上直观展示了这一现象——当从10%数据量（125,000张）初始化时，四种常用标度律函数（Table 1所列）均无法准确外推未来性能；当目标精度仅为67%时，真实需求为900,000张图像，而仅6%的估计误差就导致预测值在580,000到3,000,000之间剧烈波动。这一瓶颈构成了LOC方法设计的直接动机：**将数据收集从“估计后执行”转变为“优化中纳入不确定性”**。

### 主实验结果

**单数据源场景。** Table 2汇总了LOC与Power Law Regression基线在CIFAR-10、CIFAR-100、ImageNet、VOC、BDD100K五个数据集上的聚合对比。核心指标为失败率（Failure Rate）和成本比（Cost Ratio），其中成本比定义为实际收集成本与事后最优成本之比。结果表明：

- **失败率大幅降低**：在18个实验设置（3个时间轮次 × 6个数据集/任务组合）中，LOC在12个设置中将失败率降至10%以下，而Power Law Regression基线在15个设置中失败率超过30%。许多情况下LOC将失败率直接降至0%。
- **成本保持可控**：LOC在12个设置中成本比低于0.5，意味着额外支出不超过最优成本的50%，同时成本比几乎始终低于1（即最多花费2倍最优量）。

Figure 4以数据收集量与最小需求比值（$q_T^*/D^*$）的形式展示了LOC的行为模式：LOC几乎始终略高于黑线（$q_T^*/D^*=1$），意味着极少出现欠采失败，同时不过度过采。这一模式在$T=1,3,5$各轮次下均保持一致。

**多数据源场景。** Table 3和Figure 5展示了$K=2$数据源（CIFAR-100和BDD100K）下的结果。当两个数据源成本不均等时（$c_1/c_2$从2变化到20），LOC相比回归基线展现出更强的鲁棒性：失败率显著降低，且对于$T>1$的设置能保持较低的成本比。回归基线在成本不均等时表现尤为脆弱，而LOC通过多变量随机优化有效分配了不同成本数据源的收集量。

### 消融实验

**标度律函数形式的鲁棒性。** LOC不依赖于特定的标度律参数化形式。Table 7（附录C.2）表明，当替换为对数、反正切等其他标度律函数时，LOC仍能实现低失败率和可控成本，验证了优化框架本身而非特定估计器是性能提升的关键。

**与校正因子回归的对比。** Table 8将LOC与Mahmood et al.（CVPR 2022）提出的带校正因子的Power Law Regression进行对比。该基线虽然也能实现较低失败率，但LOC在保持竞争性失败率的同时，将成本比降低了一个数量级。这揭示了单纯“估计得更准”与“优化得更聪明”之间的本质差异。

**主动学习策略下的表现。** Table 9展示了在不同主动学习策略（随机采样、熵采样、置信度采样等）下，LOC在CIFAR-100上仍优于仅估计的基线。这表明LOC的优化框架与数据采样策略是正交的，可叠加使用。

**参数敏感性。** Figure 6（及附录Figure 12、13）系统扫描了成本参数$c$（0.001到1，跨越3个数量级）和惩罚参数$P$（$10^6$到$10^9$，跨越3个数量级）。结果显示LOC的收集行为对参数变化具有鲁棒性：$q_T^*/D^*$比值在广泛参数范围内保持稳定且略高于1。这一鲁棒性源于优化目标中$F(q)$的平滑性——参数变化主要影响安全边际的大小，而非决策的定性模式。

### 案例研究

**新类别添加。** Table 4展示了CIFAR-100上为“beaver”新类别添加数据的场景。模型初始仅在99个类别上训练，新类别零样本。LOC在$T \geq 3$时不仅将失败率控制在10%以下，且成本比甚至低于估计基线——优化框架在高度不确定的场景中优势更为明显。

**有源数据标记与主动学习的权衡。** Figure 7在BDD100K上比较了自动标记（autolabeling，利用未标记数据）与主动学习（人工标记）的总收集成本。由于未标记数据的标度律在性能较高时趋于饱和，自动标记在目标mIoU低于70时更具成本效益，而超过该阈值后主动学习更为有效。LOC框架通过加性标度律模型（Equation 5）和多变量优化自然地处理了这种成本-性能权衡。

### 失败模式与局限性

尽管LOC在绝大多数设置中表现优异，仍需注意以下边界情况：

1. **极端惩罚参数**：当$P$设置过高时（如VOC数据集上$P=10^7$），LOC可能收集高达10,000倍最小需求的数据量。这是因为优化器为规避极小概率的失败而过度保守。实际部署中需根据领域知识合理设置$P$。

2. **非单调学习曲线**：LOC假设学习曲线单调非递减，但在主动学习或半监督场景中（标签/未标记数据混合），性能可能随数据量增加而波动。此时$F(q)$的估计可能失准。

3. **高维数据源扩展**：对于$K>2$的数据源，构建ground truth的计算成本随数据源数量指数增长，使大规模验证不可行。当前实验仅验证到$K=2$。

4. **标度律估计质量依赖**：LOC的性能最终受限于bootstrapping所得$F(q)$的质量。当初始数据量极少时（Figure 1左图所示），标度律拟合本身可能严重偏离，导致$F(q)$的支撑集与真实$D^*$相距甚远。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/002_Figure_1.jpg]]
*Figure 1: Extrapolating scaling laws to estimate $D ^ { * }$ on ImageNet (Deng et al., 2009). The solid blue line is the ground truth test accuracy as a function of data set size. L e f t . : Fitting four different scaling law functions from Table 1 when initializing with 10% ( $q _ { 0 }$ = 1 2 5 , 0 0 0 dotted) and 50% ( $q _ { 0 }$ = 6 0 0 , 0 0 0 , dashed) of the data set. All functions struggle to accurately extrapolate accuracy when $q _ { 0 }$ is small, but are accurate when $q _ { 0 }$ is large. Right: To hit a target $V ^ { * }$ = 6 7 \% accuracy, we need 900, 000 images. If the scaling laws over- or underestimate by only a small amount ( $\leq$ 6 \% error at q = 9 0 0 , 0 0 0 ) , they massively under- (...*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/004_Figure_3.jpg]]
*Figure 3: Evaluating problem (16). L e f t . : We set c = 1 , $q _ { 0 }$ = 1 $0 ^ { 4 }$ and sweep different values for P . If P is sufficiently small ( $\mathrm { i . e . , }$ P < c $\hat { \sigma } \sqrt { 2 \pi }$ ) , then the total expected cost is minimized by setting $d _ { 1 }$ = 0 (i.e., orange, blue curves). Right: We set c = 1 , P = 1 $0 ^ { 5 }$ and sweep√ different values for $q _ { 0 }$ . The dashed lines point to the local maxima and minima at $\hat { \mu } \pm \sqrt { 2 } \hat { \sigma } \zeta$ When $q _ { 0 } \geq \hat { \mu } + \sqrt { 2 } \hat { \sigma } \zeta$ , the optimal $d _ { 1 } ^ { * }$ = 0 \ ( $\mathrm { i . e . }$ , red, purple). When $q _ { 0 } \in [ \hat { \mu } \pm \sqrt { 2 } \hat { \sigma...$

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/014_Figure_8.jpg]]
*Figure 8: For a fixed seed, ground truth learning curves (black) and the estimated power law learning curves (blue) obtained via bootstrapping and ensembling. The shaded region represents the 95 percentile of the ensemble and the dashed blue line represents the mean of the regression functions. The mean is consistently higher than the unknown ground truth, whereas the shaded region can at times cover it*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/015_Figure_9.jpg]]
*Figure 9: For a fixed seed, the histogram of estimates of D ^ { * } from different bootstrapped models (blue bars), the estimated F ( q ) (orange curve), and the ground truth D ^ { * } (black dashed line). Each plot corresponds to a different V ^ { * } for CIFAR-100 (see Figure 8 for the learning curve). With higher targets, regression (i.e., collecting the mean of the distribution) will lead to larger under-estimations*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/001_Table_1.jpg]]
*Table 1: Four common scaling law functions with learnable parameters $\pmb { \theta } = \{ \theta _ { 1 } , \theta _ { 2 } , \theta _ { 3 } \}$ when K = 1 . See Viering and Loog (2022) for an extensive list. For K > 1 , we can add the scaling law for each data source according to (5)

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/006_Table_2.jpg]]
*Table 2: Average cost ratio ± standard error and failure rate measured over a range of V ^ { * } for each T and data set. We fix c = 1 and P = 1 0 ^ { 7 } ( P = 1 0 ^ { 6 } for VOC and P = 1 0 ^ { 8 } for ImageNet). The best performing failure rate for each setting is bolded. LOC consistently reduces the average failure rate, often down to 0%, while keeping the average cost ratio almost always below 1 (i.e., spending at most 2× the optimal amount)*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/008_Table_3.jpg]]
*Table 3: Average cost ratio ± standard error and failure rate over different V ^ { * } for each T and c, after removing 99-th percentile outliers. We fix P = 1 0 ^ { 1 3 } for CIFAR-100 and P = 1 0 ^ { 8 } for BDD100K. The best performing failure rate for each setting is bolded. LOC reduces the average failure rate, is more robust to uneven costs than regression, and for T > 1 , preserves the cost ratio*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/011_Table_4.jpg]]
*Table 4: On CIFAR-100, average cost ratio and failure rate for ‘beaver’ (new class) measured over a range of $V ^ { * }$ for each T , when the model is initialized with only 99 classes and zero training examples for the new class. We fix c = 1 and P = 1 $0 ^ { 5 }$ . The best performing failure rate for each setting is bolded. LOC consistently achieves less than 10% failure rate, while keeping the average cost ratio even lower than the estimation baseline when T $\geq$ 3*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/012_Table_5.jpg]]
*Table 5: Data sets, tasks, and score functions considered*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/013_Table_6.jpg]]
*Table 6: Summary of hyperparameters used in our experiments*

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/017_Table.jpg]]

![[assets/figures/papers/paper_list_l7_https_www_jmlr_org_papers_v26_23_0292_html/figures/018_Table_8.jpg]]
*Table 8: Comparing against the correction factor-based Power Law Regression of Mahmood et al. (2022b) with the same setup as in Table 2. The best performing cost ratio is underlined and the best performing failure rate for each setting is bolded. Although the baseline achieves low failure rates, LOC often can achieve competitive failure rates while reducing the cost ratios by an order of magnitude*



## 定位与知识库关联

### 问题定位：从标度律估计到数据收集优化

LOC 的核心贡献在于将“需要多少数据”这一问题从**估计问题**重新定义为**优化问题**。传统的数据需求预测方法（以 **Power Law Regression** 为代表，Rosenfeld et al., ICLR 2020）遵循“拟合标度律→外推至目标性能→收集该数量”的流水线。这一范式存在根本性缺陷：标度律在平坦区域的外推对拟合误差极度敏感，即使微小的曲线偏差也会被放大为巨大的数据量误判（Figure 1 显示，仅 6% 的精度误差即可导致估计量从 58 万张到 300 万张的跨度，而真实需求为 90 万张）。LOC 通过将最小数据需求量 $\mathbf{D}^*$ 视为随机变量，显式建模其分布 $F(\mathbf{q})$，从而将决策从“点估计后收集”转变为“基于分布的期望成本最小化”。

### 与标度律估计方法的谱系关系

**直接估计基线（Power Law Regression）**：该基线直接拟合参数化标度律函数（如幂律 $v(q) = \theta_1 q^{\theta_2} + \theta_3$），求解 $\hat{\mathbf{D}}^* = \arg\min_{\mathbf{q}} \{ \mathbf{c}^\top \mathbf{q} \mid v(\mathbf{q}; \pmb{\theta}^*) \geq V^* \}$，然后收集 $\hat{\mathbf{D}}^*$。其失败根源在于忽略了估计不确定性——当目标 $V^*$ 位于学习曲线平坦区时，$\hat{\mathbf{D}}^*$ 的方差极大，导致频繁的欠采（failure）或过采（浪费）。

**集成回归（Ensemble Regression）**：该方法通过对学习曲线样本进行 bootstrapping 并集成多个标度律拟合，以估计 $\mathbf{D}^*$ 的均值。这相当于仅利用了分布的一阶矩信息，缺乏对尾部风险的控制。LOC 在单轮情形下的理论分析（Theorem 3）表明，最优解等价于收集分布的 $(1-\varepsilon)$ 分位数，而非均值——这正是集成回归无法保证低失败率的本质原因。

**校正因子回归（Correction-based Power Law Regression, Mahmood et al., CVPR 2022）**：该方法对标度律估计施加校正因子以降低欠采风险。Table 8 的对比显示，该基线确实能实现较低的失败率，但代价是成本比（cost ratio）比 LOC 高出一个数量级。LOC 通过优化框架自动平衡成本与风险，无需手动设计校正因子。

### 方法谱系中的结构性创新

LOC 引入了三个在现有数据收集方法中缺失的结构性组件：

1. **分布估计模块**：通过 bootstrapping 重采样学习曲线并拟合标度律，获得 $\mathbf{D}^*$ 的样本集；再使用核密度估计（KDE，$K=1$ 时）或高斯混合模型（GMM，$K=2$ 时）拟合其累积分布函数 $F(\mathbf{q})$。这是将估计不确定性转化为可优化信号的关键。

2. **随机优化目标**：将原始确定性问题转化为期望成本最小化：
   $$\min_{\mathbf{q}_1 \leq \cdots \leq \mathbf{q}_T} \sum_{t=1}^T \mathbf{c}^\top (\mathbf{q}_t - \mathbf{q}_{t-1}) (1 - F(\mathbf{q}_{t-1})) + P (1 - F(\mathbf{q}_T))$$
   其中 $P$ 为未达目标的惩罚参数，$\mathbf{c}$ 为各数据源的单位成本。这一形式将风险规避程度显式参数化。

3. **模型预测控制（MPC）循环**：每轮仅执行优化解的第一步，收集数据后更新模型、重新估计分布并再次优化。这种滚动优化策略使 LOC 能够根据新信息动态调整，避免一次性决策的不可逆风险。

### 适用边界与假设约束

LOC 的适用性受以下假设限制：

- **单调性假设**：方法假设学习曲线单调非递减（$V_{\mathbf{q}}$ 随数据量增加而提升）。在实际中，主动学习或半监督场景下标签/未标签数据的混合可能导致非单调行为，此时 LOC 的优化目标可能偏离真实最优。
- **加性标度律**：多数据源场景（$K>1$）下采用加性模型 $v(\mathbf{q}; \pmb{\theta}) = \theta_0 + \sum_{k=1}^K v_k(q_k; \pmb{\theta}_k)$，这假设各数据源对性能的贡献独立可加。当数据源间存在交互效应时，该假设可能不成立。
- **静态数据源**：当前框架假设数据源在收集轮次之间保持不变，不适用于引入新类别或发生域转移的场景（尽管 Table 4 展示了为新类别添加数据的案例研究，但这仍是在固定数据源设定下）。
- **$K \leq 2$ 的可计算性**：对于 $K>2$ 的数据源，构建 ground truth 的计算成本随数据源数量指数增长，使大规模实验验证不可行。

### 参数敏感性与鲁棒性

LOC 涉及两个关键超参数：单位成本 $\mathbf{c}$ 和惩罚 $P$。消融实验（Figure 6, 12, 13）表明，LOC 对这两个参数在 1 到 3 个数量级范围内的变化具有鲁棒性，收集量始终保持在略高于最小需求的水平。然而，在极端设置下（如 VOC 数据集上 $P$ 设置过高时），LOC 可能产生不切实际的大量收集（可达最小需求的 10000 倍），表明参数选择仍需领域知识。

单轮情形下的理论分析（Proposition 5, Corollary 6）揭示了 $P$ 的作用机制：当 $P$ 低于阈值 $c\hat{\sigma}\sqrt{2\pi}$ 时，最优策略是不收集任何数据（$d_1^* = 0$），因为惩罚不足以抵消收集成本；当 $P$ 足够大时，最优收集量近似于分布的高分位数。这一分析为参数选择提供了理论指导。

### 开放问题与未来方向

1. **隐私与公平性约束**：当前框架未考虑数据收集的隐私成本或对特定保护群体的过采样/欠采样问题。如何将差分隐私预算或人口统计均等约束纳入优化目标，是实际部署中的关键挑战。

2. **非平稳数据源**：当模型能力或数据源特性在收集轮次之间发生变化时（如引入新类别、域转移），当前基于静态标度律的分布估计将失效。这需要在线更新的标度律模型或元学习方法。

3. **高维数据源扩展**：将 LOC 扩展到 $K>2$ 的高维数据收集场景，同时保持分布估计和随机优化的可计算性，需要更高效的采样或变分推断方法。

4. **标度律估计器的改进**：LOC 的性能上限受限于 $F(\mathbf{q})$ 的估计质量。是否存在更准确的标度律估计器（如基于贝叶斯神经过程的方法），可以进一步提升 LOC 的性能而不显著增加计算开销，是一个开放问题。



## 原文 PDF

![[paperPDFs/JMLR_2025/Optimizing_Data_Collection_for_Machine_Learning.pdf]]
