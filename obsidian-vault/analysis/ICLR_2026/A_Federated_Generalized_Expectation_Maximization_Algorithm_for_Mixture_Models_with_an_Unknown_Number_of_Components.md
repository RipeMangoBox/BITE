---
title: "A Federated Generalized Expectation-Maximization Algorithm for Mixture Models with an Unknown Number of Components"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Federated_Generalized_Expectation_Maximization_Algorithm_for_Mixture_Models_with_an_Unknown_Number_of_Components.pdf
openreview_forum_id: CELYMnherN
aliases:
- FGEMAMMUNC
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "每个客户端为每个本地分量构造的不确定性集合，服务器通过判定不确定性球体之间的交集来识别跨客户端共享的簇，实现协同训练与最终K推断。"
primary_logic: "通过在M步后求解一个保证完整数据对数似然不下降的最大半径，客户端可以共享稳健的估计（中心点+半径）；服务器利用这些球体的交集进行简单的成对比较，即可检测重叠簇并聚合参数，同时仅分享少量摘要信息，兼顾隐私与准确性。"
claims:
- "客户端在本地执行EM步骤，并围绕每个本地分量的极大值点构造不确定性集合。"
- "中央服务器利用不确定性集合学习客户端之间的潜在簇重叠，并通过闭式计算推断全局簇数。"
- "服务器使用不确定性集合识别客户端之间的簇重叠，将客户端的组件分组为超级簇。"
- "MNIST 上 ARI = 0.452 ±0.049"
---

# A Federated Generalized Expectation-Maximization Algorithm for Mixture Models with an Unknown Number of Components

> [!tip] 核心洞察
> 通过在M步后求解一个保证完整数据对数似然不下降的最大半径，客户端可以共享稳健的估计（中心点+半径）；服务器利用这些球体的交集进行简单的成对比较，即可检测重叠簇并聚合参数，同时仅分享少量摘要信息，兼顾隐私与准确性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种针对分量数未知的混合模型的联邦广义期望最大化算法 |
| 英文题名 | A Federated Generalized Expectation-Maximization Algorithm for Mixture Models with an Unknown Number of Components |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CELYMnherN) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | FedGEM |
| Dataset | MNIST, MNIST (image) |

> [!tip] 效果简介
> - MNIST 上，ARI 为 0.452  ±0.049，对比 0.098  ±0.031 (DP-GMM, 无需已知K的最好对比方法)，变化 +0.354。
> - MNIST 上，Estimated K 为 13.63  ±2.29，对比 18.57  ±2.23 (DP-GMM)，变化 -4.94 (更接近真实K=10)。
> - MNIST (image) 上，Runtime (seconds) 为 552  ±52，对比 2047  ±246 (AFCL)，变化 -1495。

## 概述

联邦聚类面临一个核心瓶颈：各客户端持有的数据分属不同且可能重叠的聚类分量集合，所有参与方均不知道全局聚类总数 $K$，且原始数据不能离开本地。现有联邦聚类方法大多要求预先指定 $K$，而无需已知 $K$ 的集中式方法（如狄利克雷过程混合模型）又难以直接迁移到联邦场景。

FedGEM 针对这一瓶颈提出了一个因果性解决方案：**每个客户端在本地 EM 迭代后，为每个分量的极大值点构造一个不确定性球体**（中心点 + 最大半径），该半径保证球内任意参数均不降低当前完整数据对数似然。**服务器仅通过检测这些球体之间的交集**，即可识别跨客户端的簇重叠，将各客户端的分量归入“超级簇”，从而在无需全局 $K$ 先验的条件下实现协同训练，并在最终聚合阶段通过闭式计算推断出全局簇数。

核心实验结果表明：
- 在 MNIST 上，FedGEM 的 ARI 达到 $0.452 \pm 0.049$，显著优于无需已知 $K$ 的最好对比方法 DP-GMM（$0.098 \pm 0.031$）；
- 估计的簇数 $13.63 \pm 2.29$ 更接近真实值 $K=10$（DP-GMM 为 $18.57 \pm 2.23$）；
- 在图像数据集上，FedGEM 的运行时间（$552 \pm 52$ 秒）远低于 AFCL（$2047 \pm 246$ 秒）。

方法的有效性依赖于最终聚合半径超参数 $v_g$ 的合理设定，在恰当取值下估计 $K$ 可与真实 $K$ 一致；同时对最小簇间距变化表现出良好的鲁棒性。当前局限包括簇权重固定不可学习、模型假设限于等协方差高斯混合、差分隐私仅初步讨论等，这些方向有待后续研究拓展。

## 背景与动机

聚类分析是机器学习中的一项核心任务，其目标是将数据点划分为有意义的组别。高斯混合模型（Gaussian Mixture Model, GMM）凭借其坚实的概率基础和对复杂数据分布的灵活建模能力，成为聚类分析的经典工具。期望最大化（Expectation-Maximization, EM）算法是拟合GMM的标准方法，它通过交替执行E步（计算数据点对每个分量的归属概率）和M步（最大化完整数据对数似然以更新分量参数），逐步逼近模型参数的最大似然估计。

然而，在联邦学习场景下应用GMM面临两个根本性挑战。**第一个挑战是数据隔离**：客户端持有各自的本地数据，出于隐私保护、法规限制或通信效率等原因，原始数据不能离开本地，这排除了将所有数据汇集到中央服务器进行集中式EM训练的可能性。**第二个挑战是全局聚类总数未知**：每个客户端只能观察到本地数据的聚类结构，其本地分量集合可能异构且相互重叠——不同客户端可能各自拥有全局某个簇的部分数据，而没有任何客户端知道完整的全局簇数$K$。

现有的联邦聚类方法在这两个挑战面前存在明显缺口。一方面，联邦K均值（FedKmeans）等方法要求预先指定全局聚类数$K$，这在真实联邦场景中往往不可行。另一方面，少数无需已知$K$的方法（如AFCL和基于狄利克雷过程的DP-GMM）虽然放松了这一假设，但其聚类性能与簇数估计精度仍不理想。AFCL作为一种联邦方法，在图像数据集上运行时间长达2047秒，计算开销显著。DP-GMM作为集中式方法，在MNIST上估计的簇数高达$18.57$，远超真实值$K=10$，其调整兰德指数（Adjusted Rand Index, ARI）仅为$0.098$，聚类质量有限。

上述缺口的根源在于一个核心瓶颈：**如何在客户端仅持有局部数据、全局簇数未知、且客户端间分量可能重叠的约束下，实现跨客户端的协同训练与全局簇数推断？** 单纯在客户端本地独立运行EM算法会得到彼此孤立的局部估计，服务器无法判断哪些局部分量对应同一全局簇，也无法聚合出有意义的全局模型。

本文提出的FedGEM算法正是针对这一瓶颈设计。其核心思想是：每个客户端在本地EM迭代后，不仅共享分量的极大值点（中心估计），还额外构造一个**不确定性集合**——一个以该极大值点为中心、以特定半径为边界的球体，保证球内任意点均不降低当前迭代的完整数据对数似然。服务器接收到所有客户端的不确定性球体后，通过简单的成对交集检测即可识别跨客户端的簇重叠，将重叠的分量归入同一“超级簇”，进而聚合参数并推断全局簇数$K$。这一设计使得服务器无需访问原始数据、无需预先知道$K$，仅凭少量摘要信息（中心点+半径）即可完成协同训练与簇数推断，兼顾了隐私保护与聚类精度。

## 核心创新

FedGEM 的核心创新在于将联邦聚类中“未知全局簇数 K”与“客户端分量异构重叠”这两个难题统一为一个**不确定性集合驱动的协同推理框架**。其关键改造体现在以下三个层面。

### 1. 从点估计到球体估计：本地不确定性集合构造

传统联邦聚类方法（如 FedKmeans、FedAvg 变体）在客户端仅共享分量中心点的点估计，服务器无法判断这些点估计的可靠程度，更无法识别跨客户端簇的重叠关系。FedGEM 的**核心因果旋钮**在于：每个客户端在完成本地 EM 步后，不是直接上传极大值点 $\widehat{M}_{k_g}(\theta_g^{(t-1)})$，而是为每个分量求解一个**最大不确定性半径** $\varepsilon_{k_g}$，使得以该极大值点为中心、$\varepsilon_{k_g}$ 为半径的球体内任意参数均不降低当前迭代的完整数据对数似然：

$$J_{k_g}(\pmb{\theta}_g^{(t-1)}) := \underset{\varepsilon_{k_g}}{\operatorname{max}} \varepsilon_{k_g} \; \mathrm{s.t.} \; \sum_{n_g=1}^{N_g} \gamma_{k_g}(\hat{\pmb{x}}_{n_g}, \pmb{\theta}_g^{(t-1)}) \log(\pi_{k_g} p_{k_g}(\hat{\pmb{x}}_{n_g} | \hat{m}_{k_g}(\pmb{\theta}_g^{(t-1)}))) \geqslant \sum_{n_g=1}^{N_g} \gamma_{k_g}(\hat{\pmb{x}}_{n_g}, \pmb{\theta}_g^{(t-1)}) \log(\pi_{k_g} p_{k_g}(\hat{\pmb{x}}_{n_g} | \pmb{\theta}_{k_g}^{(t-1)}))$$

客户端上传的不再是孤立的点，而是**（中心点 + 半径）对**——即一个“可信球体”。这一改造将本地估计的置信度显式编码为几何结构，为服务器端的重叠检测提供了信息基础。

### 2. 服务器聚合方式：基于球体交集的超簇检测与参数更新

服务器聚合方式是 FedGEM 相对 baseline 的**核心 changed slot**。传统联邦聚类服务器通常采用联邦平均或直接参数共享，无法处理客户端分量集合异构且无全局 K 先验知识的场景。FedGEM 的服务器执行两个关键操作：

- **超簇检测**：服务器对所有客户端上传的不确定性球体进行成对比较，**通过判定球体之间的交集来识别跨客户端共享的簇**。存在交集的球体被视为描述同一底层簇，被归入同一个“超簇”（super-cluster）。这一过程无需任何全局 K 的先验，完全由数据驱动的几何关系推断重叠结构。

- **参数更新**：对于每个超簇内的分量，服务器在重叠球体的交集区域内计算凸组合，更新全局参数。更新后的参数向量仍保持在各自的不确定性集合内，保证了更新不会破坏本地对数似然的单调性。

这一机制的本质是将“哪些分量属于同一全局簇”这一离散决策问题，转化为连续几何空间中的交集判定问题，从而实现了**闭式计算**，避免了复杂的匹配或聚类过程。

### 3. 最终聚合与 K 推断：从超簇到全局簇数

在协同训练收敛后，服务器执行单步最终聚合：将属于同一超簇的所有客户端分量估计进行聚合，超簇的数量即为推断的全局簇数 $\hat{K}$。这一设计使得 K 的推断成为算法自然收敛的产物，而非预先指定的超参数。

### 创新总结

| 组件 | Baseline 做法 | FedGEM 做法 | 因果作用 |
|------|-------------|-----------|---------|
| 客户端上传 | 点估计（仅中心点） | 球体估计（中心点 + 不确定性半径） | 编码本地估计置信度 |
| 服务器聚合 | 联邦平均 / 直接参数共享 | 基于球体交集的超簇检测与凸组合更新 | 无需 K 先验，闭式识别重叠 |
| K 推断 | 需预设或启发式估计 | 超簇数量自然收敛为 $\hat{K}$ | K 从数据中自动涌现 |

这一框架的核心洞察在于：**通过 M 步后求解保证对数似然不下降的最大半径，客户端可以共享稳健的球体估计；服务器利用球体交集的简单成对比较，即可检测重叠簇并聚合参数，同时仅分享少量摘要信息，兼顾隐私与准确性**。

## 整体框架

FedGEM 是一种两阶段联邦聚类算法，其核心设计围绕一个关键瓶颈展开：**各客户端持有的聚类分量集合异构且可能重叠，所有客户端均无全局聚类总数 $K$ 的先验知识，且不能共享原始数据**。为突破这一瓶颈，算法引入了一个核心调控机制——每个客户端为本地每个分量构造一个**不确定性集合**（以极大值点为中心、以保证完整数据对数似然不下降的最大半径为半径的球体），服务器通过判定这些球体之间的交集来识别跨客户端共享的簇，从而实现协同训练与最终的 $K$ 推断。

### 两阶段流程

算法由两个阶段构成：**迭代协同训练阶段**与**单步最终聚合阶段**。

**阶段一：迭代协同训练。** 在每一轮全局迭代 $t$ 中，流程如下：

1. **客户端本地更新**：每个客户端 $g$ 接收服务器广播的当前全局参数，在本地数据上执行（可能多步）EM 迭代，得到每个本地分量 $k_g$ 的极大值点 $\widehat{M}_{k_g}(\theta_g^{(t-1)})$。随后，客户端求解一个优化问题，获得每个分量对应的不确定性半径 $\varepsilon_{k_g}$，并将（极大值点，半径）对上传至服务器。

2. **服务器聚合**：服务器收集所有客户端上传的不确定性集合，通过成对比较球体之间的交集来检测跨客户端簇重叠，将各客户端的分量分组为“超级簇”。对于存在重叠的分量，服务器在不确定性集合的交集内计算凸组合以更新全局参数，确保更新后的参数仍落在各自的不确定性球体内。更新后的参数被广播回客户端，进入下一轮迭代。

**阶段二：单步最终聚合。** 协同训练收敛后，服务器将所有属于同一超级簇的分量估计进行最终聚合，推断出全局唯一的簇数 $K$，并输出各簇的最终参数。

### 模块关系与数据流

下图概括了 FedGEM 的核心模块及其输入输出关系：

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| Local EM Steps | 客户端在本地数据上执行 E 步与 M 步，更新分量参数 | 当前全局参数 $\theta_g^{(t-1)}$，本地数据 | 各分量的极大值点 $\widehat{M}_{k_g}$ |
| Local Radius Optimization | 求解每个分量对应的最大不确定性半径 | 当前参数、极大值点、本地数据 | 半径 $\varepsilon_{k_g}$ |
| Server Super-cluster Detection | 通过成对比较不确定性球体交集检测跨客户端重叠簇 | 所有客户端的 $(\widehat{M}_{k_g}, \varepsilon_{k_g})$ | 超级簇分组 |
| Server Parameter Update | 对重叠簇内的中心点进行凸组合更新全局参数 | 超级簇分组、各分量估计 | 更新后的全局参数 |
| Final Aggregation and K Inference | 聚合同一超级簇内的所有估计，推断全局 $K$ | 收敛后的超级簇分组及各分量估计 | 最终簇参数及 $K$ |

### 关键设计要点

- **隐私保护**：客户端仅共享每个分量的中心点估计和半径两个标量/向量，不暴露原始数据或完整的模型参数。
- **无需先验 $K$**：服务器通过不确定性集合的交集自动发现共享簇结构，无需任何客户端知晓全局簇数。
- **收敛保证**：理论分析依赖于完整数据对数似然函数的一阶稳定性条件，证明了有限样本 EM 迭代在真实参数邻域内的收缩性质，以及 GEM 迭代的收敛界。

> **注意**：上述流程的理论收敛保证建立在强凹性、一阶稳定性、数据有界等假设之上。实验表明，在实际数据违反这些假设时，算法仍表现良好，但理论保障有待加强。

## 核心模块与公式推导

FedGEM 的核心机制围绕“不确定性集合”展开，其设计逻辑为：每个客户端在本地 EM 迭代后，为每个分量构造一个以极大值点为中心、以最大允许半径 $\varepsilon_{k_g}$ 为边界的球体，使得球内任意参数点均不降低当前迭代的完整数据对数似然。服务器通过检测这些球体之间的交集来识别跨客户端的重叠簇，进而实现参数聚合与全局簇数 $K$ 的推断。

### 客户端：本地 EM 与半径优化

每个客户端 $g$ 在每轮迭代中执行两个关键任务：本地 EM 步骤和不确定性半径求解。

**E 步**：计算数据点 $\widehat{\mathbf{x}}_{n_g}$ 归属于第 $k_g$ 个分量的后验概率（责任值）：

$$\gamma_{k_g}(\widehat{\mathbf{x}}_{n_g}, \theta_g^{(t-1)}) \gets \frac{\pi_{k_g} p_{k_g}(\widehat{\mathbf{x}}_{n_g} | \theta_{k_g}^{(t-1)})}{\sum_{j_g=1}^{K_g} \pi_{j_g} p_{k_g}(\widehat{\mathbf{x}}_{n_g} | \theta_{j_g}^{(t-1)})}$$

其中 $\pi_{k_g}$ 为混合权重，$p_{k_g}(\cdot|\theta_{k_g})$ 为分量密度。

**M 步**：在有限样本下，求取使加权完整数据对数似然最大化的参数点：

$$\widehat{M}_{k_g}(\theta_g^{(t-1)}) \gets \underset{\theta_{k_g} \in \mathbb{R}^d}{\operatorname{argmax}} \sum_{n_g=1}^{N_g} \gamma_{k_g}(\widehat{x}_{n_g}, \theta_g^{(t-1)}) \log(\pi_{k_g} p_{k_g}(\widehat{x}_{n_g} | \theta_{k_g}))$$

**半径优化问题**：在 M 步获得极大值点 $\widehat{M}_{k_g}$ 后，客户端求解以下约束优化问题，以最大化不确定性半径 $\varepsilon_{k_g}$：

$$J_{k_g}(\pmb{\theta}_g^{(t-1)}) := \underset{\varepsilon_{k_g}}{\operatorname{max}} \varepsilon_{k_g} \; \mathrm{s.t.} \; \sum_{n_g=1}^{N_g} \gamma_{k_g}(\hat{\pmb{x}}_{n_g}, \pmb{\theta}_g^{(t-1)}) \log(\pi_{k_g} p_{k_g}(\hat{\pmb{x}}_{n_g} | \hat{m}_{k_g}(\pmb{\theta}_g^{(t-1)}))) \geqslant \sum_{n_g=1}^{N_g} \gamma_{k_g}(\hat{\pmb{x}}_{n_g}, \pmb{\theta}_g^{(t-1)}) \log(\pi_{k_g} p_{k_g}(\hat{\pmb{x}}_{n_g} | \pmb{\theta}_{k_g}^{(t-1)}))$$

该约束保证：以 $\widehat{M}_{k_g}$ 为中心、$\varepsilon_{k_g}$ 为半径的球体内任意点，其完整数据对数似然不低于当前参数 $\theta_{k_g}^{(t-1)}$ 处的值。客户端将 $(\widehat{M}_{k_g}, \varepsilon_{k_g})$ 对广播至服务器。

### 等协方差高斯混合模型下的可计算重构

针对等协方差高斯混合模型（isotropic GMM），上述半径问题可重构为二维双凸优化问题，从而高效求解。令 $\alpha_{k_g}$ 为辅助变量，重构形式为：

$$\begin{array}{rl} \mathcal{J}_{k_g}(\theta_g') = & \max_{\varepsilon\in\mathcal{R}_0} \varepsilon_{k_g} \\ & \text{s.t. } \varepsilon_{k_g}\alpha_{k_g}^2 + [\sum_{n_g=1}^{N_g}\gamma_{k_g}(\widehat{x}_{n_g},\theta_g')(\|\widehat{x}_{n_g}-\widehat{M}_{k_g}(\theta_g')\|_2^2 - \|\widehat{x}_{n_g}-\theta_{k_g}'\|_2^2 - \varepsilon_{k_g})]\alpha_{k_g} + \\ & (\sum_{n_g=1}^{N_g}\gamma_{k_g}(\widehat{x}_{n_g},\theta_g'))\sum_{n_g=1}^{N_g}\gamma_{k_g}(\widehat{x}_{n_g},\theta_g')\|\widehat{x}_{n_g}-\theta_{k_g}'\|_2^2 \leqslant 0 \\ & \alpha_{k_g} \lesssim \sum_{n_g=1}^{N_g}\gamma_{k_g}(\widehat{x}_{n_g},\theta_g'). \end{array}$$

该重构是 FedGEM 在等协方差 GMM 上实际部署的核心计算模块。

### 服务器：超簇检测与参数聚合

服务器接收所有客户端上传的 $(\widehat{M}_{k_g}, \varepsilon_{k_g})$ 对，通过成对比较不确定性球体的交集来检测跨客户端簇重叠。若两个球体相交，则对应分量被视为属于同一“超簇”（super-cluster）。服务器在重叠球体内计算凸组合以更新全局参数，更新后的参数仍保持在各自的不确定性集合内。最终聚合阶段，服务器将同一超簇内所有分量的估计进行融合，并据此推断全局簇数 $K$。

### 理论收敛的关键条件

收敛分析依赖于完整数据对数似然函数 $Q$ 的一阶稳定性（First-Order Stability, FOS）条件：

$$\lvert | \nabla Q ( M ( \pmb \theta ) | \pmb \theta ) - \nabla Q ( M ( \pmb \theta ) | \pmb \theta ^ { * } ) \rvert | _ { 2 } \leqslant \beta \lvert | \pmb \theta - \pmb \theta ^ { * } \rvert | _ { 2 }$$

该条件与强凹性假设共同保证了有限样本下 M 步迭代到真实参数的收缩界：

$$\| \widehat { M } _ { k _ { g } } ( \theta _ { g } ^ { ( t - 1 ) } ) - \theta _ { k _ { g } } ^ { * } \| _ { 2 } \leqslant \frac { \beta _ { g } } { \lambda _ { g } } \vert \theta _ { k _ { g } } ^ { ( t - 1 ) } - \theta _ { k _ { g } } ^ { * } \vert \vert _ { 2 } + \frac { 1 } { 1 - \frac { \beta _ { g } } { \lambda _ { g } } } \epsilon _ { g } ^ { \mathrm { { u n i f } } } ( N _ { g } , \delta _ { g } )$$

其中 $\lambda_g$ 为强凹性参数，$\epsilon_g^{\mathrm{unif}}$ 为与样本量 $N_g$ 相关的统计误差项。该界表明，当 $\beta_g / \lambda_g < 1$ 时，EM 迭代线性收缩至真实参数邻域，为不确定性半径的有效性提供了理论支撑。

## 实验与分析

### 主结果：聚类质量与簇数推断

FedGEM 在 9 个异构数据集上与 7 种基线方法进行了全面比较，基线分为两类：需已知真实簇数 $K$ 的方法（Centralized EM、k-FED、FFCM-avg1/2、FedKmeans）和无需已知 $K$ 的方法（DP-GMM、AFCL）。表 1 报告了所有方法的调整兰德指数（ARI）。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/001_Table_1.jpg]]
*Table 1: ARI attained by all methods on tested datasets. (Bold = best, underline = second best.)*

**核心发现：** FedGEM 在所有无需已知 $K$ 的方法中取得压倒性优势。以 MNIST 为例，FedGEM 的 ARI 达到 **0.452 ± 0.049**，而此前最好的无需已知 $K$ 的方法 DP-GMM 仅为 0.098 ± 0.031，提升幅度高达 +0.354。在 Fashion MNIST、Extended MNIST、CIFAR-10 等图像数据集上，FedGEM 同样显著优于 AFCL 和 DP-GMM。值得注意的是，FedGEM 的 ARI 在多个数据集上接近甚至匹敌需已知 $K$ 的集中式 EM 算法——例如在 Waveform 数据集上，FedGEM 的 ARI（0.348 ± 0.008）与集中式 EM（0.356 ± 0.001）差距极小，表明基于不确定性集合的联邦协同训练机制有效弥补了数据隔离带来的信息损失。

表 2 进一步揭示了 FedGEM 在簇数推断上的准确性。在真实 $K=10$ 的 MNIST 上，FedGEM 估计的簇数为 **13.63 ± 2.29**，相比 DP-GMM 的 18.57 ± 2.23 和 AFCL 的严重高估，更接近真实值。在 Waveform（真实 $K=3$）上，FedGEM 估计为 3.00 ± 0.20，几乎完美命中。这一能力源于服务器通过不确定性球体交集进行超簇检测的机制——重叠的球体被归入同一超簇，最终超簇的数量即为推断的全局 $K$。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/002_Table_2.jpg]]
*Table 2: Estimated number of clusters for algorithms with unknown K*

**性能瓶颈识别：** 在 CIFAR-10（真实 $K=10$）上，FedGEM 估计的簇数为 22.00 ± 3.74，存在明显高估。这与 CIFAR-10 的类内方差大、类间边界模糊的特性有关——等协方差高斯假设难以捕获复杂的类条件分布，导致本地分量过度分裂。类似的高估也出现在 Frog A 和 Frog B 数据集上，提示当前模型假设的局限性。

### 消融与敏感性分析

**最终聚合半径超参数 $v_g$ 的敏感性。** 图 4 展示了聚类 ARI 和估计簇数对最终聚合半径超参数 $v_g$ 的依赖关系。实验揭示了一个清晰的因果机制：$v_g$ 控制着最终聚合阶段不确定性球体的大小，进而决定哪些分量估计被合并入同一超簇。当 $v_g$ 过小时，球体无法覆盖来自不同客户端的同一真实簇的估计，导致 $K$ 被高估、ARI 下降；当 $v_g$ 过大时，不同真实簇的估计被错误合并，$K$ 被低估，ARI 同样受损。在恰当的 $v_g$ 取值下，估计 $K$ 可与真实 $K$ 精确一致。这一结果验证了算法对 $v_g$ 的敏感性，也说明当前基于交叉验证的调参策略是必要的——尽管这会引入额外的计算和隐私代价。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/025_Figure_4.jpg]]
*Figure 4: (b) Sensitivity of our algorithm’s number of clusters estimation to the hyperparameter value. Figure 4: Results on the sensitivity of our algorithm to its hyperparameter*

**最小簇间距 $R_{\min}$ 的鲁棒性。** 图 1 的敏感性研究表明，FedGEM 的 ARI 和估计 $K$ 在较宽的 $R_{\min}$ 范围内保持稳定，且性能曲线与集中式 EM 高度接近。这意味着只要数据中的真实簇具有一定程度的分离度，FedGEM 就能有效运作。当 $R_{\min}$ 极小时（簇高度重叠），所有方法的性能均下降，但 FedGEM 的退化程度与集中式 EM 相当，未出现联邦场景特有的崩溃。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/008_Figure_1.jpg]]
*Figure 1: (b) Number of clusters estimated by our proposed FedGEM vs. the true number of clusters. Figure 1: Results of the sensitivity study*

### 计算效率

表 7 报告了图像数据集上联邦算法的运行时间。FedGEM 在 MNIST 上平均耗时 **552 ± 52 秒**，而 AFCL 高达 2047 ± 246 秒，加速约 3.7 倍。这一优势源于 FedGEM 的通信模式：客户端仅上传每个分量的中心点-半径对（$O(K_g \cdot d)$ 的通信量），服务器通过简单的成对球体交集判定进行聚合，避免了 AFCL 中复杂的全局推断步骤。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/026_Table_7.jpg]]
*Table 7: Runtime in seconds of selected federated algorithms on the image datasets evaluated*

图 5 的可扩展性实验进一步表明，FedGEM 的运行时间随客户端数量 $G$ 从 5 增长到 65 时基本保持稳定，未出现超线性增长。但需要注意的是，服务器端的成对比较复杂度为 $O((\sum_g K_g)^2)$，在客户端数量或本地分量数极大的场景下可能成为瓶颈——这是当前设计中一个已知的效率局限。

![[assets/figures/papers/iclr26_0012_CELYMnherN_A_Federated_Generalized_Expectation-Maximization/figures/030_Figure_5.jpg]]
*Figure 5: Results of the scalability experiment for all experimental settings and benchmark models*

### 失败模式与局限的实验证据

1. **簇数高估问题：** 在 CIFAR-10、Frog A、Frog B 等复杂图像/音频数据集上，FedGEM 估计的 $K$ 显著高于真实值。这与等协方差高斯混合模型的假设直接相关——当真实数据分布偏离各向同性高斯时，本地 EM 倾向于用多个分量拟合单个复杂簇，服务器无法仅通过中心点-半径信息纠正这种过度分裂。

2. **簇权重未学习：** 实验设置中客户端簇权重 $\pi_{k_g}$ 在训练期间保持不变，这限制了模型对样本不均衡场景的适应能力。在部分数据集中，这可能导致小簇被大簇"吸收"或忽略。

3. **差分隐私的初步性：** 论文仅对共享的中心点添加高斯噪声进行了初步讨论，未在实验中系统评估隐私预算-效用权衡。不确定性半径本身的隐私含义（半径大小可能泄露本地数据密度信息）尚未被充分考虑。

### 图表结论要点

- **表 1（ARI 主结果）：** FedGEM 在所有无需已知 $K$ 的方法中排名第一，在多个数据集上接近集中式 EM 的性能上界。
- **表 2（估计 $K$）：** FedGEM 的簇数估计最接近真实值，DP-GMM 和 AFCL 普遍严重高估。
- **图 1（$R_{\min}$ 敏感性）：** FedGEM 对簇分离度具有良好鲁棒性，性能退化模式与集中式 EM 一致。
- **图 4（$v_g$ 敏感性）：** 聚类质量对最终聚合半径存在单峰依赖，存在最优 $v_g$ 使估计 $K$ 等于真实 $K$。
- **表 7（运行时间）：** FedGEM 比 AFCL 快约 3.7 倍，通信效率优势明显。
- **图 5（可扩展性）：** 运行时间随客户端数量增长保持稳定，但成对比较的二次复杂度在极端场景下值得关注。

## 方法谱系与知识库定位

### 与基线方法的关系

FedGEM 在联邦聚类方法谱系中占据一个独特位置：它同时解决了**无需预设全局簇数 K**和**跨客户端异构分量对齐**两个瓶颈，而现有方法通常只能处理其中之一。

**与需已知 K 的方法对比。** 集中式 GMM（Centralized EM）和联邦 K 均值（FedKmeans）均要求所有客户端事先知晓真实簇数 K，且假设客户端间的分量一一对应。FedGEM 通过不确定性集合的交集检测，在服务器端自动推断 K，解除了这一先验知识依赖。实验表明，在 MNIST 上 FedGEM 估计的 K 为 $13.63 \pm 2.29$，显著优于同样无需 K 的 DP-GMM（$18.57 \pm 2.23$），更接近真实 K=10（Table 2）。

**与无需已知 K 的方法对比。** AFCL 是此前唯一无需已知 K 的联邦聚类方法，但其基于层次聚类的设计导致计算开销高昂：在 MNIST 图像数据上运行时间为 $2047 \pm 246$ 秒，而 FedGEM 仅需 $552 \pm 52$ 秒（Table 7）。DP-GMM 作为集中式狄利克雷过程高斯混合模型，虽无需 K，但无法利用联邦场景下的多客户端协同信息，在 MNIST 上的 ARI 仅为 $0.098 \pm 0.031$，远低于 FedGEM 的 $0.452 \pm 0.049$（Table 1）。

**方法定位的本质差异。** FedGEM 的核心创新在于将“客户端分量对齐”和“全局 K 推断”统一为**不确定性球体交集判定**这一单一机制：服务器通过成对比较球体是否相交来识别跨客户端共享的簇，既避免了联邦平均对分量对齐的强假设，也绕过了 DP-GMM 等非参数方法对全局数据集中访问的依赖。

### 适用边界与建模假设

FedGEM 的适用性受限于以下建模假设，违反这些假设时性能可能退化：

1. **等协方差高斯混合模型。** 当前理论推导和可计算半径公式（Theorem 4 中的双凸重构）均针对 isotropic GMM。扩展到各向异性 GMM 需要重新推导半径问题的可计算形式，这是论文明确指出的开放问题。

2. **强凹性与一阶稳定性。** 收敛分析依赖完整数据对数似然函数的 $\lambda_g$-强凹性和 $\beta_g$-一阶稳定性条件（FOS condition，公式 (4)），以及数据有界假设。论文承认这些假设在实践中可能不成立，但实验表明即使违反假设，FedGEM 的实际性能仍然良好——理论保障的泛化是需要进一步研究的方向。

3. **全客户端参与。** 理论证明未考虑部分客户端掉队或退出的场景。在联邦学习常见的异构参与模式下，参数估计的一致性和 K 推断的可靠性尚未得到理论保证。

4. **簇权重固定。** 算法允许客户端设置本地个性化权重 $\pi_{k_g}$，但这些权重在训练过程中保持不变，未被纳入学习过程，限制了模型对数据分布变化的适应能力。

### 局限性与开放问题

**计算效率瓶颈。** 服务器端通过所有客户端分量间的成对比较来检测重叠簇。虽然可扩展性实验（Figure 5）表明在当前规模下性能尚可，但当客户端数量或本地分量数大幅增长时，$O((\sum_g K_g)^2)$ 的成对比较开销将成为瓶颈。论文提出基于 KD 树的近似搜索作为潜在解决方案，但尚未实现。

**最终聚合半径的调参困境。** 最终聚合阶段使用的半径启发式 $\varepsilon_{k_g}^{\text{final}} = \frac{v_g \hat{R}_{\min_g}}{\pi_g \sqrt{N_g}}$ 依赖超参数 $v_g$ 的交叉验证调优。敏感性分析（Figure 4）显示，ARI 和估计 K 对 $v_g$ 的取值敏感，不当选择会导致 K 的显著高估或低估。交叉验证在联邦场景下带来额外的计算和隐私代价，开发更鲁棒、数据驱动的半径设定方法是重要的开放问题。

**差分隐私的浅层处理。** 论文仅对客户端共享的簇中心点添加高斯噪声进行了初步讨论，未深入分析不确定性半径本身的隐私泄露风险及其对收敛的影响。如何为半径信息设计差分隐私保护方案，并量化隐私预算与聚类精度之间的权衡，是联邦聚类实用化必须解决的问题。

**模型复杂度的扩展路径。** 将 FedGEM 从 isotropic GMM 扩展到更丰富的混合模型（各向异性 GMM、非高斯分量、可学习权重）需要解决两个核心挑战：一是推导相应模型下半径问题的可计算形式，二是保证扩展后不确定性集合的几何性质仍支持高效的成对交集判定。

**部分参与与掉队客户端的鲁棒性。** 在实际联邦部署中，客户端可能随时加入或退出。当前 FedGEM 假设每轮所有客户端参与，掉队客户端可能导致服务器端超簇检测的不完整，进而影响 K 推断的准确性。如何设计容错机制，使算法在部分参与下仍能收敛到一致的参数估计和 K 推断，是需要理论突破的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/A_Federated_Generalized_Expectation_Maximization_Algorithm_for_Mixture_Models_with_an_Unknown_Number_of_Components.pdf]]
