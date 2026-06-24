---
title: "A Spectral-Grassmann Wasserstein metric for operator representations of dynamical systems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Spectral_Grassmann_Wasserstein_metric_for_operator_representations_of_dynamical_systems.pdf
aliases:
- SGOTS
- SGWMORDS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/physics
core_operator: "将每个动力系统的转移算子表示为其特征值和谱投影子上的联合分布，并利用最优传输和格拉斯曼几何定义Wasserstein距离（SGOT）。"
primary_logic: "通过将非自伴算子的谱分解视为离散分布（每个原子包含特征值和对应的特征子空间），并设计一个结合特征值差和子空间格拉斯曼距离的基代价函数，最优传输自然提供了排列不变性，从而得到一个真正的度量空间。"
claims:
- "SGOT在频率偏移、衰减率偏移、子空间偏移和采样频率变化四种场景下均表现出单调且鲁棒的行为，而其他度量（Hilbert-Schmidt、Operator、SOT、GOT、Martin）存在饱和或振荡问题。"
- "在14个UEA时间序列数据集上，SGOT在使用线性核、RBF核和深度特征核三种算子估计方式下均取得最佳平均排名（线性核1.34±0.79，RBF核1.48±0.70，深度核1.71±0.77）。"
- "SGOT的Fr\\'echet均值能够在线性振荡系统和流体动力学系统之间实现有意义的插值，而Hilbert-Schmidt度量（带谱约束）陷入局部极小值。"
- "SGOT具有有限样本收敛保证，收敛率为n^{-(α-1)/(2(α+β))} ln(Nδ^{-1})。"
---

# A Spectral-Grassmann Wasserstein metric for operator representations of dynamical systems

> [!tip] 核心洞察
> 通过将非自伴算子的谱分解视为离散分布（每个原子包含特征值和对应的特征子空间），并设计一个结合特征值差和子空间格拉斯曼距离的基代价函数，最优传输自然提供了排列不变性，从而得到一个真正的度量空间。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向动力系统算子表示的谱-格拉斯曼Wasserstein度量 |
| 英文题名 | A Spectral-Grassmann Wasserstein metric for operator representations of dynamical systems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=B02EqvyiF3) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/physics |
| Method | Spectral–Grassmann Optimal Transport (SGOT) |
| Dataset | UEA时间序列分类（线性核）, UEA时间序列分类（RBF核）, UEA时间序列分类（深度特征核）, BasicMotions (RBF核) |

> [!tip] 效果简介
> - UEA时间序列分类（线性核） 上，平均排名（越低越好） 为 1.34 ± 0.79，对比 Hilbert-Schmidt: 3.66 ± 1.08, Operator: 4.00 ± 1.13, Martin: 4.34 ± 1.37, SOT: 3.34 ± 1.26, GOT: 4.31 ± 1.28，变化 SGOT排名最低（最佳）。
> - UEA时间序列分类（RBF核） 上，平均排名（越低越好） 为 1.48 ± 0.70，对比 Hilbert-Schmidt: 3.52 ± 1.09, Operator: 4.07 ± 1.07, Martin: 4.48 ± 1.28, SOT: 3.33 ± 1.56, GOT: 4.14 ± 1.27，变化 SGOT排名最低（最佳）。
> - UEA时间序列分类（深度特征核） 上，平均排名（越低越好） 为 1.71 ± 0.77，对比 Hilbert-Schmidt: 3.86 ± 1.35, Operator: 4.14 ± 1.27, Martin: 5.06 ± 1.48, SOT: 3.84 ± 1.34, GOT: 2.94 ± 1.33，变化 SGOT排名最低（最佳）。

## 概述

本文针对动力系统算子表示之间的比较问题，提出了一种名为**谱-格拉斯曼最优传输（Spectral–Grassmann Optimal Transport, SGOT）**的新度量。现有方法（如范数度量、Martin伪度量）在理论完备性、鲁棒性或计算效率上存在缺陷：要么对噪声敏感且缺乏可解释性，要么仅定义伪度量且局限于自伴算子。SGOT的核心创新在于，将每个非亏损转移算子的谱分解视为一个离散分布，其中每个原子包含一个特征值和对应的特征子空间。通过设计一个结合特征值差与子空间格拉斯曼距离的基代价函数，并利用最优传输的排列不变性，SGOT在算子空间上定义了一个真正的度量空间（满足正定性、对称性和三角不等式）。

主要结果包括：（1）在模拟的线性振荡系统四种偏移场景（频率偏移、衰减率偏移、子空间偏移、采样频率变化）下，SGOT展现出单调且鲁棒的行为，而其他度量（Hilbert-Schmidt, Operator, SOT, GOT, Martin）则出现饱和或振荡问题；（2）在14个UEA时间序列分类数据集上，无论使用线性核、RBF核还是深度特征核估计算子，SGOT均取得最佳平均排名（线性核：1.34±0.79，RBF核：1.48±0.70，深度核：1.71±0.77），并在多个数据集上显著提升准确率（如在BasicMotions上提升8个百分点）；（3）SGOT的Fr´echet均值能够在线性振荡系统和流体动力学系统之间实现有意义的插值，而带谱约束的Hilbert-Schmidt度量陷入局部极小值，且SGOT的重心计算快约6倍。此外，SGOT具有有限样本收敛保证，收敛率为 $n^{-(\alpha-1)/(2(\alpha+\beta))} \ln(N\delta^{-1})$。

## 背景与动机

动力系统的比较是时间序列分析、流体动力学和系统识别中的核心问题。一个自然的框架是将每个系统表示为一个转移算子（如Koopman算子），该算子捕捉状态随时间的演化。然而，在此框架下定义一个实用且理论上完备的度量面临着根本性挑战：现有方法要么对噪声高度敏感且缺乏可解释性，要么仅定义伪度量而非真正的度量。

**现有方法的缺口。** 基于算子范数的直接比较（如Hilbert-Schmidt距离和算子范数距离）将算子视为一个整体黑箱，缺乏对系统内在动力模态（特征值和特征子空间）的显式建模，导致对噪声敏感且难以解释。Martin伪度量基于ARMA模型，但对采样频率等变化敏感。更近期的谱最优传输（SOT）和格拉斯曼最优传输（GOT）分别仅考虑特征值或特征子空间，但存在两个关键缺陷：第一，它们仅定义伪度量，不满足三角不等式或不可区分性；第二，它们割裂了特征值和特征子空间之间的耦合关系，而正是这种耦合决定了系统的完整动力学行为。此外，SOT和GOT局限于自伴算子，而许多实际动力系统的转移算子是非自伴的。

**本文的核心动机与因果机制。** 本文的核心洞察在于：将每个动力系统的转移算子表示为其特征值和谱投影子上的联合离散分布，每个“谱原子”包含一个特征值和对应的特征子空间。通过设计一个结合特征值差和子空间格拉斯曼距离的基代价函数 $d_\eta[(\lambda, V), (\lambda', V')] = \eta|\lambda - \lambda'| + (1-\eta)d_{\mathcal{G}}(V, V')$，最优传输自然提供了排列不变性，从而得到一个真正的度量空间。这一机制解决了三个关键问题：第一，联合建模特征值和子空间避免了仅关注单一模态的信息损失；第二，最优传输的排列不变性消除了谱分解的顺序依赖性；第三，基代价的凸组合形式允许在特征值差异和子空间差异之间灵活权衡。

**理论完备性与鲁棒性。** 本文提出的谱-格拉斯曼最优传输（SGOT）度量具有有限样本收敛保证，收敛率为 $n^{-(\alpha-1)/(2(\alpha+\beta))} \ln(N\delta^{-1})$，确保了从有限数据估计的可靠性。在四种典型偏移场景（频率偏移、衰减率偏移、子空间偏移、采样频率变化）中，SGOT表现出单调且鲁棒的行为，而基线度量（Hilbert-Schmidt、Operator、Martin、SOT、GOT）存在饱和或振荡问题。这一对比凸显了SGOT在区分系统差异方面的分辨能力——它能够连续地反映系统参数的微小变化，而不是像其他度量那样过早饱和。

## 核心创新

SGOT（谱-格拉斯曼最优传输度量）的核心创新在于将动力系统的比较问题转化为其转移算子谱分解上的最优传输问题，从而在单一框架内同时解决了现有方法的三个根本性瓶颈：对噪声的鲁棒性、对非自伴算子的适用性，以及度量性质的完备性。

**瓶颈与因果机制**：现有基于算子的动力系统比较方法（如Hilbert-Schmidt距离、Martin伪度量、SOT、GOT）要么对噪声敏感且缺乏可解释性，要么局限于自伴算子且仅定义伪度量。SGOT的因果旋钮在于：将每个动力系统的转移算子表示为其特征值和谱投影子上的联合分布，并利用最优传输和格拉斯曼几何定义Wasserstein距离。具体而言，每个算子被表示为离散分布 $\mu(T) \triangleq \sum_{j\in[\ell]} (m_j / m_{\text{tot}}) \delta_{(\lambda_j, V_j)}$，其中每个原子包含一个特征值 $\lambda_j$ 和对应的特征子空间 $V_j$。

**四个关键变化槽位**：
1. **算子表示形式**：从将算子视为整体（Hilbert-Schmidt、Operator norm）或仅考虑特征值（SOT）或仅考虑子空间（GOT），转变为将算子表示为特征值和特征子空间上的联合分布。
2. **基代价函数**：从仅使用特征值差（SOT）或仅使用子空间距离（GOT），转变为 $d_\eta[(\lambda, \mathcal{V}), (\lambda', \mathcal{V}')] = \eta|\lambda - \lambda'| + (1-\eta)d_\mathcal{G}(\mathcal{V}, \mathcal{V}')$，结合特征值差和格拉斯曼距离的凸组合。其中 $d_\mathcal{G}$ 是子空间之间的格拉斯曼距离（通过正交投影器的Hilbert-Schmidt范数定义）。
3. **度量性质**：从SOT和GOT仅定义伪度量（不满足三角不等式或不可区分性），提升为SGOT是真正的度量（满足正定性、对称性和三角不等式），如Theorem 1所述 $(S_r(\mathcal{H}), d_S)$ 是一个度量空间。
4. **采样频率不变性**：从Martin伪度量和范数度量对采样频率敏感，转变为SGOT对采样频率变化具有不变性（在合理范围内），如Figure 1(d)所示。

**决定性证据**：SGOT在四种偏移场景（频率偏移、衰减率偏移、子空间偏移、采样频率变化）下均表现出单调且鲁棒的行为，而其他度量存在饱和或振荡问题（Figure 1）。在14个UEA时间序列数据集上，SGOT在使用线性核（平均排名1.34±0.79）、RBF核（1.48±0.70）和深度特征核（1.71±0.77）三种算子估计方式下均取得最佳平均排名（Table 1）。此外，SGOT的Fr\'echet均值能够在线性振荡系统和流体动力学系统之间实现有意义的插值，而Hilbert-Schmidt度量陷入局部极小值（Figure 4, Figure 15）。理论上，SGOT具有有限样本收敛保证，收敛率为 $n^{-(\alpha-1)/(2(\alpha+\beta))} \ln(N\delta^{-1})$（Theorem 2）。

**证据强度**：上述关键证据的置信度均为1.0，来自论文中的明确数值结果和定理陈述。唯一的例外是有限样本收敛保证的置信度为0.95，因为其依赖于对算子谱性质的假设（A2和A3）。

## 整体框架

SGOT（Spectral–Grassmann Optimal Transport）的完整 pipeline 包含四个核心模块，将原始时间序列数据转化为动力系统算子之间的可度量距离，并支持系统插值。

**模块一：转移算子估计（RRR）**  
输入为多通道时间序列轨迹数据。采用 Reduced Rank Regression (RRR) 估计器，从观测数据中学习每个动力系统的有限秩转移算子 $T$。该模块支持三种核函数形式：线性核（有限维）、RBF 核（无限维，通过 Nyström 近似）以及深度特征核（基于预训练深度网络提取的特征）。这一步骤将每个系统压缩为一个秩至多为 $r$ 的算子。

**模块二：谱分解**  
对估计出的算子 $T$ 进行谱分解，提取其特征值 $\lambda_j$ 和对应的特征子空间 $V_j$（即谱投影子的像空间）。对于非亏损算子，该分解将算子表示为离散的谱原子集合 $\{(\lambda_j, V_j)\}$，每个原子对应一个动力学模态。

**模块三：构建谱分布**  
将每个算子的谱原子集合形式化为一个离散概率分布：
$$\mu(T) \triangleq \sum_{j\in[\ell]} \frac{m_j}{m_{\text{tot}}} \delta_{(\lambda_j, V_j)}$$
其中 $m_j$ 是模态 $j$ 的权重（通常由子空间维数或谱测度决定），$\delta$ 为狄拉克测度。至此，每个动力系统被表示为一个支撑在特征值-子空间对上的离散分布。

**模块四：计算 SGOT 距离（核心度量）**  
定义基代价函数 $d_\eta$，它结合了特征值差异和子空间的格拉斯曼距离：
$$d_\eta[(\lambda, V), (\lambda', V')] = \eta|\lambda - \lambda'| + (1-\eta)d_\mathcal{G}(V, V')$$
其中 $d_\mathcal{G}$ 是格拉斯曼流形上的距离（通过正交投影子的 Hilbert-Schmidt 范数计算），$\eta \in [0,1]$ 是平衡两个代价的超参数。然后，两个系统 $T$ 和 $T'$ 之间的 SGOT 距离定义为它们谱分布之间的 $p$-Wasserstein 距离：
$$d_S(T, T') = W_{d_\eta, p}(\mu(T), \mu(T'))$$
该最优传输问题通过求解离散 Monge-Kantorovich 线性规划实现，其排列不变性自然解决了谱原子的对应问题。Theorem 1 证明 $(S_r(\mathcal{H}), d_S)$ 构成一个真正的度量空间（满足正定性、对称性和三角不等式），区别于 SOT 和 GOT 仅定义伪度量。

**可选模块：Fr´echet 均值（系统插值）**  
对于多个系统 $\{T_k\}$ 及其权重 $\{\gamma_k\}$，SGOT 重心定义为加权 Fr´echet 均值：
$$\arg\min_{T \in S_r(\mathcal{H})} \sum_k \gamma_k d_S(T, T_k)^2$$
由于无限维 RKHS 中的直接优化不可行，论文将算子参数化为 $T_\theta$（由特征值 $\lambda_i$、控制点 $\mathbf{x}$ 和系数 $\alpha_i, \beta_i$ 定义），并将问题转化为带约束的优化问题（约束包括 $\alpha^*\mathbf{K}\beta = \mathbf{I}$ 和 $\beta_j^*\mathbf{K}\beta_j = 1$）。该问题通过坐标下降法求解，交替优化传输计划 $\mathbf{P}_i$ 和算子参数 $\theta$，每个梯度步的计算时间约为 2.29ms（比带谱约束的 Hilbert-Schmidt 快约 6 倍）。

**整体数据流**：原始轨迹 → RRR 估计 → 谱分解 → 离散分布 → 最优传输 → 距离矩阵/重心。该 pipeline 的输出可直接用于 K-NN 分类（K=1）、T-SNE 可视化降维，以及通过 Fr´echet 均值实现系统间的有意义的插值。

## 核心模块与公式推导

### 1. 转移算子与谱分解基础

动力系统的演化通过**转移算子**描述。给定可观测量 $f$，转移算子 $A_t$ 定义为条件期望：

$$
[ A _ { t } ( f ) ] ( x ) : = \mathbb { E } [ f ( X _ { t } ) | X _ { 0 } = x ] , x \in \mathcal { X } .
$$

其生成元 $L$ 的谱分解为：

$$
L = \sum _ { j \in \mathbb { N } } \lambda _ { j } g _ { j } \otimes _ { \mathcal { F } } f _ { j } ,
$$

其中 $\lambda_j$ 为特征值，$f_j, g_j$ 分别为左右特征函数。可观测量期望的演化可写为各模态的加权和：

$$
\mathbb { E } [ f ( X _ { t } ) \mid X _ { 0 } = x _ { 0 } ] = [ A _ { t } f ] ( x ) = \sum _ { j \in \mathbb { N } } e ^ { \lambda _ { j } t } \langle f _ { j } , g _ { j } \rangle _ { \mathcal { F } } f _ { j } ( x _ { 0 } ) .
$$

这一谱分解形式表明，动力系统的本质特征完全由其谱模态（特征值和特征子空间）决定。

### 2. 谱-格拉斯曼最优传输度量（SGOT）

SGOT 的核心思想是将每个非亏损算子 $T$ 表示为其谱上的离散分布。设 $T$ 的谱分解为特征值 $\lambda_j$ 和对应的特征子空间 $\mathcal{V}_j$（重数为 $m_j$），则谱分布定义为：

$$
\mu(T) \triangleq \sum_{j\in[\ell]} \frac{m_j}{m_{\text{tot}}} \delta_{(\lambda_j, \mathcal{V}_j)} .
$$

两个算子 $T, T'$ 之间的 SGOT 距离定义为它们谱分布之间的 Wasserstein 距离：

$$
d_S(T, T') = W_{d_\eta, p}(\mu(T), \mu(T')) .
$$

其中基代价函数 $d_\eta$ 同时度量特征值差异和特征子空间的几何差异：

$$
d_\eta[(\lambda, \mathcal{V}), (\lambda', \mathcal{V}')] \triangleq \eta|\lambda - \lambda'| + (1-\eta)d_\mathcal{G}(\mathcal{V}, \mathcal{V}') .
$$

这里 $d_\mathcal{G}$ 是格拉斯曼流形上的距离，定义为正交投影算子的 Hilbert-Schmidt 范数：

$$
d_\mathcal{G}(\mathcal{U}, \mathcal{V}) = \|P_\mathcal{U} - P_\mathcal{V}\|_{\mathcal{HS}} .
$$

参数 $\eta \in [0,1]$ 控制特征值差异与子空间差异的相对重要性。

**离散最优传输问题**：给定谱原子数 $k_S, k_T$，传输成本矩阵 $\mathbf{C} \in \mathbb{R}_+^{k_S \times k_T}$ 的元素为：

$$
C_{i,j} = \eta|\lambda_i - \lambda'_j| + (1-\eta)\big(m_i + m_j - 2\operatorname{Tr}((\beta_i^* \mathbf{M}_y \beta_j)(\pmb\alpha_i^* \mathbf{M}_x \pmb\alpha_j))\big)^{1/2} .
$$

求解 Monge-Kantorovich 问题得到耦合矩阵 $\mathbf{P}$：

$$
\operatorname*{min}_{\mathbf{P} \in \Pi(\mu_S, \mu_T)} \langle \mathbf{C}, \mathbf{P} \rangle_F \quad \mathrm{s.t} \quad \Pi(\mu_S, \mu_T) = \big\{ \mathbf{P} \in \mathbb{R}_+^{k_S \times k_T} \mid \mathbf{P1} = \mathbf{a}, \mathbf{P}^\intercal \mathbf{1} = \mathbf{b} \big\} .
$$

**定理保证**：在可分的复希尔伯特空间 $\mathcal{H}$ 上，秩不超过 $r$ 的非亏损算子集合 $S_r(\mathcal{H})$ 与 SGOT 度量 $d_S$ 构成一个度量空间（满足正定性、对称性和三角不等式）。

### 3. SGOT 重心（Fr\'echet 均值）

对于多个算子 $\{T_i\}_{i=1}^N$ 的加权平均（插值），定义 Fr\'echet 均值问题：

$$
\arg\min_{T \in S_r(\mathcal{H})} \sum_{i \in [N]} \gamma_i d_S(T, T_i)^2 .
$$

当 RKHS 无限维时，该问题不可直接求解。论文引入参数化算子 $T_\theta$：

$$
T_{\pmb\theta}: h \in \mathcal{H} \mapsto \sum_{i \in [r]} \lambda_i \langle \kappa_{\mathbf{x}} \pmb\alpha_i, h \rangle_{\mathcal{H}} \kappa_{\mathbf{x}} \pmb\beta_i \in \mathcal{H} ,
$$

其中 $\kappa_{\mathbf{x}} \pmb\alpha_i = \sum_j \kappa_{x_j} \alpha_{ji}$ 为核表示。参数 $\theta = \{\lambda_i, \pmb\alpha_i, \pmb\beta_i, \mathbf{x}\}$ 的优化问题为：

$$
\arg\min_{\theta, \mathbf{P}} \sum_{i \in [N]} \gamma_i \langle \mathbf{C}_i(\theta), \mathbf{P}_i \rangle_F \quad \mathrm{s.t.} \quad \left\{ \begin{array}{ll} \alpha^* \mathbf{K} \beta = \mathbf{I} \\ \beta_j^* \mathbf{K} \beta_j = 1, \forall j \in [r] \\ \mathbf{P}_i \in \Pi(\mu(T_\theta), \mu(T_i)), \forall i \in [N] \end{array} \right. .
$$

约束 $\alpha^* \mathbf{K} \beta = \mathbf{I}$ 保证特征函数的双正交性，$\beta_j^* \mathbf{K} \beta_j = 1$ 保证归一化。该问题通过坐标下降法求解，交替更新传输计划 $\mathbf{P}_i$ 和算子参数 $\theta$。

### 4. 有限样本收敛保证

SGOT 度量具有理论上的有限样本误差界。设 $\widehat{T}_1, \widehat{T}_2$ 为从 $n$ 个样本估计的算子，$T_1, T_2$ 为真实算子，则在概率至少 $1-\delta$ 下：

$$
|d_S(\widehat{T}_1, \widehat{T}_2) - d_S(T_1, T_2)| \lesssim n^{-\frac{\alpha-1}{2(\alpha+\beta)}} \ln(2\delta^{-1}) .
$$

其中 $\alpha > 1$ 和 $\beta \geq 0$ 是反映算子正则性和谱衰减速度的参数。该收敛率表明，当样本量增加时，SGOT 距离的估计误差以多项式速率衰减，为实际应用提供了理论保障。

## 实验与分析

### 核心结果：时间序列分类

SGOT在14个UEA时间序列数据集上的分类任务中，在三种不同的算子估计方式（线性核、RBF核、深度特征核）下均取得了最佳的平均排名。如表1所示，SGOT的平均排名分别为1.34±0.79（线性核）、1.48±0.70（RBF核）和1.71±0.77（深度核），显著优于所有基线度量（Hilbert-Schmidt、Operator norm、Martin、SOT、GOT）。所有基线度量的平均排名均高于3.3，表明SGOT的领先优势具有一致性。


![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/005_Table_1.jpg]]
*Table 1: Classification rank per kernel type. Deep: kernel based on learned deep features. Best and second best performers are highlighted (lower is better). Ranks are denoted: $\langle { \mathrm { m e a n } } \rangle \doteq \langle { \mathrm { s t d } } \rangle$

在具体的准确率指标上（以RBF核为例，见表2），SGOT在BasicMotions、ERing、Epilepsy和NATOPS四个数据集上均取得了最高准确率，分别达到0.95±0.02、0.98±0.02、0.95±0.02和0.80±0.05，相比最佳基线度量（Hilbert-Schmidt或SOT）提升约0.05至0.08。Figure 3的散点图进一步证实了SGOT的优越性：在所有数据点上，SGOT的准确率均位于或高于对角线（即非劣于其他度量）。


![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/006_Table_2.jpg]]
*Table 2: Classification accuracy for operators estimated with RBF kernels. Datasets on rows and similarities on columns. Best and second best performers are highlighted. Accuracy scores are denoted: ⟨mean⟩ ± ⟨std⟩*

### 消融与机制分析

**四种偏移场景下的行为对比（Figure 1）**：这是理解SGOT鲁棒性的关键实验。实验设置了一个线性振荡系统，并分别改变其频率、衰减率、算子秩/子空间以及采样频率。结果显示：
- **频率偏移**和**衰减率偏移**：SGOT的距离值随偏移量近似线性单调增长，而Hilbert-Schmidt、Operator norm和Martin伪度量在偏移较大时出现饱和或振荡。
- **子空间偏移**：SGOT保持单调性，而其他度量（尤其是Martin伪度量）表现出高度非单调的行为。
- **采样频率变化**：SGOT和GOT的距离值保持低且几乎恒定，表现出对采样频率的不变性。相比之下，Hilbert-Schmidt、Operator norm和Martin伪度量的值随采样频率变化剧烈。

**η参数的敏感性（Figure 13）**：SGOT的基代价函数d_η包含一个超参数η ∈ [0,1]，用于平衡特征值差异（η）和子空间格拉斯曼距离（1-η）。实验表明，SGOT的分类性能随η平滑变化，最优值通常偏向于强调子空间代价（即较小的η）。论文提出了一个启发式值η̃ = (1 + f_samp/(2√2))^{-1}，该值在大多数数据集上提供了一个合理的初始选择和搜索范围上界（图中以红色虚线标记）。

### 插值（Fr´echet均值）实验

**线性振荡系统插值（Figure 4, Figure 15）**：SGOT的Fr´echet均值能够在线性振荡系统的两个实例之间实现有意义的插值。插值系统的衰减率和频率随插值权重线性变化，完美地过渡了源系统和目标系统的动态特性。相比之下，Hilbert-Schmidt度量（带谱约束）的插值结果陷入局部极小值，无法正确插值频率和衰减率。此外，SGOT的Fr´echet均值算法在计算效率上显著优于带谱约束的Hilbert-Schmidt：每梯度步的平均计算时间为2.29ms，而后者为13.11ms，加速约6倍。

**流体动力学系统插值（Figure 5）**：SGOT成功计算了流经圆柱和三角形障碍物的Koopman算子的重心。该重心的前三阶右本征函数在空间结构上呈现出从圆柱到三角形的平滑过渡，特别是与涡旋脱落现象相关的模态，验证了SGOT在复杂动力系统插值中的有效性。

### 有限样本收敛保证

理论分析（Theorem 2）保证了SGOT度量的有限样本收敛率。对于两个由RRR估计器从n个样本中估计的算子，其SGOT距离与真实算子距离之间的误差以概率至少1-δ被界定为O(n^{-(α-1)/(2(α+β))} ln(Nδ^{-1}))，其中α和β是控制算子谱衰减和采样分布特性的参数。这为SGOT在实际应用中的可靠性提供了理论支撑。

### 失败模式与局限性

1. **谱假设的依赖性**：SGOT的有效性依赖于假设(A2)和(A3)，即算子的主要谱成分位于一个公共的RKHS中。当该假设不成立时，比较会引入偏差。
2. **谱估计的稳定性**：对于高维或高度病态的算子，谱分解（尤其是特征子空间估计）可能不稳定，从而影响SGOT的计算结果。
3. **重心优化缺乏严格保证**：SGOT的Fr´echet均值优化问题目前缺乏存在性和唯一性的严格证明（附录D中提及），虽然实验表现良好，但理论完备性有待加强。
4. **小数据集下的性能下降**：深度特征核实验表明，当数据集较小时，深度特征的学习受限，所有度量的性能均下降，SGOT的领先优势也会相应缩小。

### 补充图表

![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/016_Table_3.jpg]]
*Table 3: Metrics on Grassmann manifold ${ \mathcal { G } }$ ( k , n ) ! angle-based and matrix-based formulations. Here $\mathbf { M } = \mathbf { U } ^ { \top } \mathbf { V } , \mathbf { P } = \mathbf { U } \mathbf { U } ^ { \top } , \mathbf { Q } = \mathbf { V } \mathbf { V } ^ { \top }$ , and S = $\sqrt { \mathbf { M } \mathbf { M } ^ { \top } }$ where U, V are orthonormal bases

![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/018_Table_4.jpg]]
*Table 4: Datasets main characteristics: Size: number of time series, Channels: number of dimensions per time series, Length: time series length, Classes: number of classes*

![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/019_Table_5.jpg]]
*Table 5: Classification accuracy scores. Transfer operators are estimated with the finite dimensional linear kernel. Datasets on rows and similarities on columns. Best and second best performers are highlighted. Accuracy scores are denoted: \< mean > $\pm$ \< std >*

![[assets/figures/papers/iclr26_0004_B02EqvyiF3_A_Spectral-Grassmann_Wasserstein_metric_for_oper/figures/020_Table_6.jpg]]
*Table 6: Average computation time per similarity on all validation folds*


## 方法谱系与知识库定位

SGOT（Spectral–Grassmann Optimal Transport）位于动力系统算子表示比较方法谱系中的一个关键空白处：它同时克服了基于范数的度量（Hilbert-Schmidt距离、算子范数距离）对噪声敏感且缺乏可解释性的问题，以及最优传输类方法（SOT、GOT）因仅考虑特征值或子空间而只能定义伪度量的局限。其核心因果机制是将每个非缺陷算子的谱分解编码为特征值与特征子空间上的联合离散分布，并通过一个结合特征值差（$|λ-λ'|$）与格拉斯曼流形距离（$d_G(V,V')$）的基代价函数 $d_η$，利用最优传输的排列不变性自然得到一个真正的度量空间（Theorem 1）。

**与baseline的关系**：实验证据清晰地展示了SGOT的压倒性优势。在四种模拟偏移场景（频率偏移、衰减率偏移、子空间偏移、采样频率变化）中，SGOT表现出单调且鲁棒的行为，而Hilbert-Schmidt、Operator norm、Martin伪度量、SOT和GOT均存在饱和或振荡问题（Figure 1）。在14个UEA时间序列分类基准上，SGOT在三种算子估计方式（线性核、RBF核、深度特征核）下均取得最低的平均排名（线性核1.34±0.79，RBF核1.48±0.70，深度核1.71±0.77），显著优于次优方法（Table 1）。在RBF核下的具体数据集上（如BasicMotions、ERing、Epilepsy、NATOPS），SGOT的准确率提升达5-8个百分点（Table 2）。

**适用边界与关键假设**：SGOT的有效性依赖于两个核心假设：(A2)和(A3)要求算子的主要谱成分位于一个公共的再生核希尔伯特空间（RKHS）中。当此假设不成立时，不同系统间的谱比较会引入不可控的偏差。此外，方法依赖于从轨迹数据中通过降秩回归（RRR）估计转移算子，再进行谱分解。对于高维或高度病态的算子，谱估计本身可能不稳定，这会直接传导至最终的度量计算。

**局限与开放问题**：
1. **重心理论不完整**：SGOT的Fr´echet均值（重心）优化问题目前缺乏存在性和唯一性的严格证明（附录D提及）。虽然实验上（Figure 4, Figure 5）展示了有意义的插值结果，且计算效率比带谱约束的Hilbert-Schmidt快约6倍（每梯度步2.29ms vs 13.11ms），但理论保证仍是开放问题。
2. **参数η的选择**：消融实验（Figure 13）显示性能随η平滑变化，最优值通常偏向强调子空间代价（较小的η）。论文提出的启发式值 $\tilde{η} = (1 + f_{samp}/(2\sqrt{2}))^{-1}$ 提供了一个实用的初始选择，但其理论最优性依据不明。
3. **深度特征核的局限性**：当数据集较小时，深度特征的学习受限，所有度量的性能均下降，SGOT的优势幅度也随之缩小（深度核下平均排名1.71±0.77，方差增大）。
4. **可扩展性**：SGOT的计算需要为每对系统求解最优传输问题，其计算成本随系统数量增长。虽然Table 6报告了平均计算时间，但大规模场景下的可扩展性未充分讨论。

**知识库定位**：SGOT为动力系统比较提供了一个理论完备（真正的度量）、鲁棒（对采样频率变化等不敏感）且可解释（谱分解联合分布）的新工具。它填补了“基于算子的系统比较”与“最优传输几何”之间的交叉空白，但需要手动验证其在非公共RKHS假设下的行为退化程度。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Spectral_Grassmann_Wasserstein_metric_for_operator_representations_of_dynamical_systems.pdf

![[paperPDFs/ICLR_2026/A_Spectral_Grassmann_Wasserstein_metric_for_operator_representations_of_dynamical_systems.pdf]]
