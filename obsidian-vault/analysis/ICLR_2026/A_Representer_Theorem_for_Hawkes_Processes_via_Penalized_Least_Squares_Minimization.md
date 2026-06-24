---
title: "A Representer Theorem for Hawkes Processes via Penalized Least Squares Minimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Representer_Theorem_for_Hawkes_Processes_via_Penalized_Least_Squares_Minimization.pdf
aliases:
- RTHPPLSM
- Ours
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/learning_theory
core_operator: "利用线性霍克斯过程的惩罚最小二乘损失函数的二次型结构，通过Mercer展开将无限维优化问题转化为有限维线性系统，且所有对偶系数解析地固定为1，从而避免了对对偶系数的昂贵优化。"
primary_logic: "在线性霍克斯过程的惩罚最小二乘框架下，最优触发核估计量可以表示为数据点处一组等价核（通过Fredholm积分方程组定义）的线性组合，且所有对偶系数均为1，因此无需求解优化问题，仅需一次矩阵求逆即可得到闭式解。"
claims:
- "最优触发核估计量可表示为等价核的线性组合，且对偶系数均为1。"
- "等价核通过一组Fredholm积分方程定义。"
- "所提方法计算复杂度为O(N^2 M^2 U^2 + M^3 U^3)，远低于Bonnet方法的O(N^4 U^2 P)。"
- "在合成数据集上，所提方法在预测精度上与SOTA核方法相当，但计算时间降低数个数量级。"
---

# A Representer Theorem for Hawkes Processes via Penalized Least Squares Minimization

> [!tip] 核心洞察
> 在线性霍克斯过程的惩罚最小二乘框架下，最优触发核估计量可以表示为数据点处一组等价核（通过Fredholm积分方程组定义）的线性组合，且所有对偶系数均为1，因此无需求解优化问题，仅需一次矩阵求逆即可得到闭式解。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于惩罚最小二乘的霍克斯过程表示定理 |
| 英文题名 | A Representer Theorem for Hawkes Processes via Penalized Least Squares Minimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gJjRdLG5MY) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/learning_theory |
| Method | Ours |
| Dataset | Mutually-exciting scenario (T=2000), Mutually-exciting scenario (T=7000) |

> [!tip] 效果简介
> - Mutually-exciting scenario (T=2000) 上，Δ² 为 0.38 (0.15)，对比 0.21 (0.05) (Bonnet)，变化 +0.17。
> - Mutually-exciting scenario (T=2000) 上，cpu (s) 为 5.04 (0.62)，对比 413 (55.5) (Bonnet)，变化 ~82x faster。
> - Mutually-exciting scenario (T=7000) 上，Δ² 为 0.16 (0.04)，对比 0.14 (0.04) (Bonnet)，变化 +0.02。

## 概述

本文针对多元线性霍克斯过程的核方法估计中计算瓶颈问题，提出了一种新的表示定理及相应的闭式求解算法。现有基于核的SOTA方法（Bonnet & Sangnier, 2025）因需求解与数据规模成比例的非线性优化问题，复杂度高达O(N^4 U^2 P)，严重限制了其在大规模事件数据上的应用。核心洞察在于：利用惩罚最小二乘损失函数的二次型结构，可将无限维优化问题转化为有限维线性系统，且所有对偶系数解析地固定为1，从而避免了昂贵的优化过程。具体而言，最优触发核估计量可表示为数据点处一组等价核（通过Fredholm积分方程组定义）的线性组合，且对偶系数均为1。

方法上，通过Mercer展开（具体采用随机傅里叶特征）将核函数近似为退化形式，使得所有积分可解析计算，最终仅需一次矩阵求逆（求解线性系统(1/γ I_MU + Ξ)^{-1}）即可得到触发核与基线强度的闭式解，计算复杂度降至O(N^2 M^2 U^2 + M^3 U^3)（M为特征数，通常远小于N）。实验结果表明，在合成数据集上，所提方法在预测精度上与SOTA核方法相当（如T=7000时，Δ²=0.16 vs 0.14），但计算时间降低数个数量级（13.1秒 vs 2070秒，加速约158倍）；在金融真实数据集上亦取得竞争性表现。该方法为大规模多元霍克斯过程的高效非参数估计提供了一条新路径，但其基于线性模型假设，不保证强度非负性，且计算复杂度随维度U呈立方增长，实际应用中建议处理不超过几百维的数据。

## 背景与动机

多元霍克斯过程是建模事件序列间相互激发现象的标准工具，其条件强度函数定义为 $\lambda_i(t) = \mu_i + \sum_{j \in \mathcal{U}} \int_0^t g_{ij}(t-s) dN_j(s)$。现有基于核方法的估计方法（如 Bonnet & Sangnier, 2025）在理论上具有吸引力，但面临严重的可扩展性瓶颈：其求解过程需要处理一个与数据规模 $N$ 成比例的非线性优化问题，计算复杂度高达 $O(N^4 U^2 P)$（$U$ 为维度，$P$ 为优化迭代次数）。这一复杂度使得现有方法在大规模事件数据上几乎不可行。

本文的核心动机在于揭示线性霍克斯过程在惩罚最小二乘框架下的一个被忽视的结构性质：由于损失函数 $L_{\mathrm{LS}} = \sum_i [\int_0^T \lambda_i(t)^2 dt - 2\sum_n \lambda_i(t_n)]$ 具有二次型形式，其正则化优化问题 $\min_{g,\mu} [L(g,\mu) + \frac{1}{\gamma} \sum_{i,j} ||g_{ij}||^2_{\mathcal{H}_k}]$ 的解存在解析闭式表达。具体而言，最优触发核估计量 $\hat{g}_{ij}(s)$ 可以表示为数据点处一组等价核 $h_j(s, t_n)$ 的线性组合，且所有对偶系数 $\alpha_n^{ij}$ 解析地固定为 1，从而完全避免了对对偶系数的昂贵优化。这等价于将无限维优化问题转化为求解一组 Fredholm 积分方程组 $\frac{1}{\gamma} h_j(s,s') + \sum_l \int_0^T V_{jl}(s,t) h_l(t,s') dt = \sum_n k(s, s'-t_n) \mathbf{1}_{0 < s'-t_n \le A}$，进而通过 Mercer 展开（随机傅里叶特征）得到闭式解。

这一结构洞察带来的计算增益是决定性的：所提方法的复杂度降为 $O(N^2 M^2 U^2 + M^3 U^3)$，其中 $M$ 为随机傅里叶特征数（通常远小于 $N$），而 $M^3 U^3$ 项来自一次性的矩阵求逆。与 Bonnet 方法的 $O(N^4 U^2 P)$ 相比，当数据规模 $N$ 增大时，加速比可达数个数量级。实验验证了这一优势：在互激场景 $T=7000$ 时，所提方法（$\Delta^2=0.16$）与 Bonnet 方法（$\Delta^2=0.14$）的预测精度相当，但计算时间从 2070 秒降至 13.1 秒，加速约 158 倍。

## 核心创新

本文的核心创新在于为线性霍克斯过程的惩罚最小二乘估计建立了一个**解析表示定理**，并由此导出了一个**计算高效的闭式求解算法**。其根本动机是解决现有基于核方法的多元霍克斯过程估计方法（如Bonnet & Sangnier, 2025）在计算上的瓶颈——这些方法需要求解一个与数据规模成比例的非线性优化问题，计算复杂度高达O(N⁴U²P)，严重限制了在大规模事件数据上的可扩展性。

**核心洞察**在于，当采用惩罚最小二乘（而非负对数似然）作为损失函数时，其二次型结构使得无限维优化问题可以转化为一个有限维线性系统。具体而言，该工作证明并利用了以下关键性质：最优触发核估计量可以表示为数据点处一组等价核的线性组合，且所有对偶系数解析地固定为1（即αₙ^{ij}=1），因此无需求解对偶系数的优化问题，仅需一次矩阵求逆即可得到闭式解。

**关键变更（Changed Slots）**：

1.  **损失函数**：从标准的负对数似然（LL）切换为精确的惩罚最小二乘对比函数（L_LS）。这一选择是表示定理得以解析成立的根本原因。
2.  **对偶系数求解**：从需要求解非线性优化问题（如Bonnet方法）变为**解析地固定为1**，完全消除了对偶优化的计算开销。
3.  **积分方程求解**：从近似Riemann求和（Bonnet方法）变为通过**退化核近似（随机傅里叶特征）** 将Fredholm积分方程转化为线性系统，从而得到闭式解。
4.  **计算复杂度**：从O(N⁴U²P)降低至O(N²M²U² + M³U³)，其中M为随机傅里叶特征数量（通常远小于N）。这意味着计算复杂度从对数据规模的**四次方依赖**降为**二次方依赖**。

**实现机制**：该方法通过三个核心模块实现：首先，利用随机傅里叶特征（Rahimi & Recht, 2007）将平移不变核近似为M个傅里叶特征的线性组合，使所有积分可解析计算；其次，通过求解线性系统 (1/γ I_{MU} + Ξ)^{-1} 得到等价核的闭式表达；最后，利用等价核的闭式解，通过矩阵运算直接得到触发核和基线强度的估计（Equation 17）。

**证据强度**：表示定理（Theorem 1）和对偶系数为1的结论有严格的数学证明（置信度1.0）。计算复杂度的降低有明确的复杂度分析支持（置信度0.95）。在合成数据实验（Table 1）中，该方法在T=7000时预测误差Δ²=0.16（Bonnet为0.14），但计算时间仅13.1秒，比Bonnet的2070秒快约158倍，验证了理论优势。需要注意的是，在小数据场景（T=2000）下，该方法的预测精度（Δ²=0.38）略低于Bonnet（0.21），表明精度-效率权衡在小数据时偏向于基于似然的方法。

## 整体框架

本文提出的方法围绕一个核心洞察构建：在线性Hawkes过程的惩罚最小二乘框架下，最优触发核估计量可以表示为数据点处一组等价核的线性组合，且所有对偶系数解析地固定为1。这一发现将原本需要求解非线性优化问题（如Bonnet & Sangnier, 2025的O(N⁴U²P)复杂度）的核方法估计，转化为一个仅需一次矩阵求逆的闭式解问题。

**Pipeline与模块关系**：整个方法由三个紧密耦合的模块组成，形成从数据到估计量的端到端流程。

1. **随机傅里叶特征近似模块**：作为整个方法的基础层，该模块将平移不变RKHS核近似为M个傅里叶特征的线性组合：$\phi_m(s) = \sqrt{2/M} \cos(\omega_m s + \theta_m)$。这一近似的关键作用在于使后续所有积分运算（包括Fredholm积分方程中的各项）均可解析计算，避免了数值离散化近似。

2. **等价核构造模块**：这是方法的核心计算环节。基于退化核近似，等价核$h_j(s,s')$通过求解一个MU维线性系统得到闭式表达：
   $$h_j(s,s') = \phi(s)^\top \left[ \left( \frac{1}{\gamma} I_{MU} + \Xi \right)^{-1} \tilde{\phi}(s') \right]_{1+(j-1)M:jM}$$
   其中$\Xi$是一个$MU \times MU$矩阵，其元素由傅里叶特征在观测区间上的积分构成。该矩阵求逆是整体计算的主要瓶颈，复杂度为$O(M^3U^3)$。

3. **触发核与基线强度估计模块**：利用已求得的等价核闭式解，触发核和基线强度的估计可直接通过矩阵运算得到：
   $$\hat{g}_{ij}(s) = \phi(s)^\top \left[ \left( \frac{1}{\gamma} I_{MU} + \Xi \right)^{-1} \left( \sum_{n \in \mathcal{N}_i} \tilde{\phi}(t_n) - \hat{\mu}_i \int_0^T \tilde{\phi}(t) dt \right) \right]_{1+(j-1)M:jM}$$
   $$\hat{\mu}_i = \frac{|\mathcal{N}_i| - \left( \int_0^T \tilde{\phi}(t) dt \right)^\top \left( \frac{1}{\gamma} I_{MU} + \Xi \right)^{-1} \left( \sum_{n \in \mathcal{N}_i} \tilde{\phi}(t_n) \right)}{T - \left( \int_0^T \tilde{\phi}(t) dt \right)^\top \left( \frac{1}{\gamma} I_{MU} + \Xi \right)^{-1} \left( \int_0^T \tilde{\phi}(t) dt \right)}$$

**输入输出流**：输入为多元事件序列$\{t_n\}_{n \in \mathcal{N}_i, i \in \mathcal{U}}$（观测区间[0,T]），以及超参数（正则化系数$\gamma$、支持窗口A、傅里叶特征数M）。输出为所有维度对的触发核估计$\hat{g}_{ij}(s)$和基线强度估计$\hat{\mu}_i$。关键中间产物是等价核$h_j(s,s')$，它编码了数据分布和核结构信息。

**计算复杂度与瓶颈**：整体复杂度为$O(N^2 M^2 U^2 + M^3 U^3)$，其中$N$为总事件数，$U$为维度，$M$为傅里叶特征数（通常远小于N）。与Bonnet & Sangnier (2025)的$O(N^4 U^2 P)$相比，该方法在数据规模上的可扩展性显著提升。然而，复杂度随维度U呈立方增长，实际应用中建议处理不超过几百维的数据。小数据场景下，该方法的估计精度（Δ²）低于基于似然的Bonnet方法——例如在T=2000的互激场景中，Ours为0.38(0.15)而Bonnet为0.21(0.05)，表明在数据稀疏时似然方法的统计效率更高。

## 核心模块与公式推导

### 问题形式化与损失函数

论文考虑一个 $U$ 维线性Hawkes过程，其第 $i$ 维的条件强度函数定义为：

$$
\lambda_i(t) = \mu_i + \sum_{j \in \mathcal{U}} \int_0^t g_{ij}(t-s) dN_j(s), \quad t \in \mathbb{R}_+, \quad i \in \mathcal{U} := [1, U]
$$

其中 $\mu_i$ 是基线强度，$g_{ij}$ 是触发核，$\mathcal{N}_i$ 是维度 $i$ 的事件索引集。为了从观测数据 $[0,T]$ 上估计 $\{\mu_i, g_{ij}\}$，标准方法是极小化负对数似然 $L_{LL}$。但该函数非凸，求解困难。本文转而使用**最小二乘对比函数**（least squares contrast）：

$$
L_{\mathrm{LS}} = \sum_{i \in \mathcal{U}} \left[ \int_0^T \lambda_i(t)^2 dt - 2 \sum_{n \in \mathcal{N}_i} \lambda_i(t_n) \right]
$$

该损失函数具有二次型结构，是后续表示定理推导的关键。将触发核限制在RKHS $\mathcal{H}_k$ 中，加入正则项后，优化问题变为：

$$
\hat{g}, \hat{\mu} = \underset{g \in \mathcal{H}_k^U, \mu \in \mathbb{R}^U}{\arg \min} \left[ L(g, \mu) + \frac{1}{\gamma} \sum_{(i,j) \in \mathcal{U}^2} ||g_{ij}||_{\mathcal{H}_k}^2 \right]
$$

### 表示定理（Theorem 1）

这是论文的核心理论贡献。通过分析上述优化问题的变分导数，作者证明最优触发核估计量具有如下形式：

$$
\hat{g}_{ij}(s) = \sum_{n \in N_i} \alpha_n^{ij} h_j(s, t_n) - \hat{\mu}_i \int_0^T h_j(s, t) dt, \quad \alpha_n^{ij} = 1
$$

关键洞察在于：**所有对偶系数 $\alpha_n^{ij}$ 被解析地固定为1**，无需像传统核方法那样通过优化求解。这意味着一旦得到等价核 $h_j$，估计量可直接通过一次求和与积分计算得出。等价核 $h_j$ 由一组联立的**Fredholm积分方程**定义：

$$
\frac{1}{\gamma} h_j(s, s') + \sum_{l \in \mathcal{U}} \int_0^T V_{jl}(s, t) h_l(t, s') dt = \sum_{n \in \mathcal{N}_j} k(s, s' - t_n) \mathbf{1}_{0 < s' - t_n \le A}
$$

其中 $V_{jl}(s, t) = \sum_{n \in \mathcal{N}_j} \sum_{n' \in \mathcal{N}_l} k(s, t - t_{n'}) k(t, t_n - t_{n'})$ 是数据依赖的核函数，$A$ 是触发核的支持窗口。该积分方程的解 $h_j$ 独立于目标维度 $i$，因此所有 $\hat{g}_{ij}$ 共享同一组等价核。

### 退化核近似与闭式解

Fredholm积分方程（6）没有解析解。论文采用**随机傅里叶特征**（Random Fourier Features, Rahimi & Recht, 2007）将平移不变核近似为 $M$ 个特征的线性组合：

$$
\phi_m(s) = \sqrt{\frac{2}{M}} \cos(\omega_m s + \theta_m)
$$

其中 $\omega_m$ 从核的傅里叶变换采样，$\theta_m \sim \text{Uniform}(0, 2\pi)$。在此近似下，核函数成为退化核，积分方程（6）转化为一个 $MU \times MU$ 的线性系统，从而得到等价核的闭式解：

$$
h_j(s, s') = \phi(s)^\top \left[ \left( \frac{1}{\gamma} I_{MU} + \Xi \right)^{-1} \tilde{\phi}(s') \right]_{1+(j-1)M:jM}
$$

其中 $\Xi$ 是一个 $MU \times MU$ 的矩阵，其 $(m, l)$ 块为 $\Xi^{(m,l)} = \sum_{n \in \mathcal{N}_m} \sum_{n' \in \mathcal{N}_l} \int_0^T \phi(t - t_{n'}) \phi(t - t_n)^\top dt$，$\tilde{\phi}(s')$ 是堆叠的特征向量。将闭式解代入表示定理，得到触发核的最终估计：

$$
\hat{g}_{ij}(s) = \phi(s)^\top \bigg[ \Big( \frac{1}{\gamma} I_{MU} + \Xi \Big)^{-1} \Big( \sum_{n \in \mathcal{N}_i} \tilde{\phi}(t_n) - \hat{\mu}_i \int_0^T \tilde{\phi}(t) dt \Big) \bigg]_{1+(j-1)M:jM}
$$

基线强度 $\hat{\mu}_i$ 也有闭式解：

$$
\hat{\mu}_i = \frac{|\mathcal{N}_i| - \big( \int_0^T \tilde{\phi}(t) dt \big)^\top \big( \frac{1}{\gamma} I_{MU} + \Xi \big)^{-1} \big( \sum_{n \in \mathcal{N}_i} \tilde{\phi}(t_n) \big)}{T - \big( \int_0^T \tilde{\phi}(t) dt \big)^\top \big( \frac{1}{\gamma} I_{MU} + \Xi \big)^{-1} \big( \int_0^T \tilde{\phi}(t) dt \big)}
$$

### 计算复杂度

所提方法的核心计算开销在于构造 $\Xi$ 矩阵（$O(N^2 M^2 U^2)$）和求解 $MU \times MU$ 线性系统（$O(M^3 U^3)$）。总复杂度为 $O(N^2 M^2 U^2 + M^3 U^3)$，其中 $M$（特征数）通常远小于数据规模 $N$。相比之下，SOTA核方法（Bonnet & Sangnier, 2025）的复杂度为 $O(N^4 U^2 P)$（$P$ 为优化迭代次数）。当 $N$ 较大时，本文方法可实现数个数量级的加速。**需注意**：复杂度随维度 $U$ 呈立方增长，实际应用建议处理不超过几百维的数据。

## 实验与分析

### 主要结果：预测精度与计算效率的权衡

在互激场景（mutually-exciting scenario）合成数据集上的实验揭示了所提方法（Ours）的核心特性：**以极低的计算成本换取与SOTA核方法（Bonnet & Sangnier, 2025）接近的预测精度**。如表1所示，当数据规模T=7000时，Ours的触发核积分平方误差Δ²为0.16（标准差0.04），而Bonnet为0.14（0.04），两者差距仅为0.02。然而，Ours的平均CPU时间仅为13.1秒，而Bonnet高达2070秒——加速比约158倍。在较小数据规模T=2000时，Ours的Δ²为0.38（0.15），Bonnet为0.21（0.05），差距扩大至0.17；但Ours仅需5.04秒，Bonnet需413秒（约82倍加速）。这一模式在不应期场景（refractory scenario）中复现：T=5000时Ours的Δ²为0.59（0.13），Bonnet为0.42（0.08），CPU时间分别为13.1秒和2070秒。

**关键瓶颈**：Bonnet方法需要求解一个与数据规模N呈四次方关系的非线性优化问题（O(N⁴U²P)），而Ours利用惩罚最小二乘的二次型结构，将问题转化为线性系统求解，复杂度降至O(N²M²U² + M³U³)，其中M为随机傅里叶特征数（通常远小于N）。加速的根本原因在于对偶系数被解析地固定为1，无需迭代优化。

**因果机制**：Ours的精度损失源于两个因素。其一，线性Hawkes过程的假设——强度函数为历史事件的线性叠加，不保证非负性——在互激场景中可能产生负强度值，而Bonnet通过非线性链接函数（如softplus）强制非负。其二，随机傅里叶特征近似引入的核近似误差在小样本下更为显著。证据表明，当数据量增大时（T从2000增至7000），Ours的Δ²从0.38降至0.16，与Bonnet的差距从0.17缩至0.02，说明**数据量是弥补近似误差的关键**。

在金融数据集（Table 4）上，Ours在负对数似然（nll）指标上与参数化方法（Exp、Gau）和Bonnet保持竞争力，同时计算时间显著低于Bonnet。由于该数据集为公开基准，结果可信，但需注意金融数据的真实触发核未知，Δ²无法计算，只能通过预测似然间接评估。


![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/004_Table_4.jpg]]
*Table 4: Results on financial dataset across 1O trials with standard errors in brackets.nll is the negative log-likelihood on test data. N is the data size per trial. cpu is the CPU time in seconds. The other notations follow Table 1*


![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/001_Table_1.jpg]]
*Table 1: Results of Exp (Bonnet et al., 2023), Gau (Xu et al., 2016), Ber (Lemonnier & Vayatis, 2014),Bonnet (Bonnet & Sangnier,2025),and Our s on mutually-exciting scenario dataset across 10 trials with standard errors in brackets.N is the average data size per trial. cpu is the CPU time in seconds.The performances not significantly ( p $\ge$ 0 . 0 1 ) ）different from the best one under the Mann-Whitney U test (Holm,1979) are shown in bold*

### 消融实验：支持窗口与超参数敏感性

支持窗口A（触发核的有效时间范围）的消融实验（Table 3）表明存在最优值。在T=5000的互激场景中，A=5时Δ²为0.30（0.07），A=10时降至0.16（0.04），A=20时回升至0.20（0.05）。**因果解释**：A过小会截断长程依赖，A过大则引入噪声（因核估计在尾部区域方差增大）。该现象与Hawkes过程的物理直觉一致——触发效应通常随时间衰减。


![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/003_Table_3.jpg]]
*Table 3: Performance of Ours regarding the support window A on mutually-exciting scenario dataset (T= 5OOO) across 1O trials with standard errors in brackets*

超参数网格的细化实验（Section H.3）显示，从3×3网格（γ和核带宽各3个候选值）扩展到10×10网格，Δ²仅从0.59±0.13边际改善至0.58±0.12。这表明**Ours对超参数选择相对鲁棒**，无需精细调参即可获得接近最优的性能。该结论基于10次独立试验的统计，具有可信度。

### 触发核估计精度与预测性能的关系

Table 8直接揭示了估计精度（Δ²）与预测性能（测试集负对数似然nll）的正相关关系：当Δ²从0.38降至0.16时，nll从-1.12降至-1.21。这一单调关系验证了**触发核估计的改进直接转化为点过程模型的预测能力提升**，而非通过过拟合等虚假路径。该证据强度高（置信度1.0），因为实验在同一数据集上控制了所有其他变量。

### 可扩展性分析

更大数据规模（Table 5）和更高维度（Table 6, 7）的实验验证了复杂度分析的预测。当数据规模从T=5000增至T=15000时，Ours的CPU时间从13.1秒增至29.5秒，呈近线性增长（O(N²)主导）。维度U从3增至15时，时间从5.04秒增至29.9秒。更系统的维度缩放实验（Table 7）显示，U=10时0.68秒，U=100时26.9秒，U=500时2010秒。**关键发现**：训练时间随U的增长略低于O(U³)的理论上界（Figure 3），因为实际计算中矩阵求逆的常数因子较小，且M通常随U保持固定。然而，当U超过200时，时间开始显著偏离线性，提示**实际应用中建议处理不超过几百维的数据**。


![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/023_Table_5.jpg]]
*Table 5: Average CPU time in seconds across 10 trials. $\tilde { N }$ denotes the average data size per trial*

![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/024_Table_6.jpg]]
*Table 6: Average CPU time in seconds across 5 trials*

### 失败模式与局限性

1. **小数据场景精度不足**：在T=2000时，Ours的Δ²（0.38）显著高于Bonnet（0.21）。这是线性模型假设与核近似误差在小样本下的叠加效应。需要手动验证：是否可以通过增加随机傅里叶特征数M来缓解？论文未提供M的消融实验。

2. **负强度问题**：线性Hawkes过程不保证λ_i(t)≥0，在互激场景中可能产生负强度值，而Bonnet通过非线性链接函数避免了该问题。论文未报告负强度的发生频率或对预测的影响程度。

3. **维度立方复杂度**：U=500时需2010秒，对于更高维数据（如U>1000）不可行。论文明确将此列为限制，并指出共轭梯度法因缺乏有效预条件子未能超越Cholesky分解。

4. **缺乏学习理论保证**：论文未提供一致性、收敛速率或泛化界的理论分析，所有结论基于有限实验。该点需手动验证未来研究是否填补了这一空白。

### 图表结论总结

- **Table 1 & 2**：Ours在计算效率上实现2-3个数量级的加速，预测精度在大数据下与SOTA相当，小数据下略有差距。

![[assets/figures/papers/iclr26_0003_gJjRdLG5MY_A_Representer_Theorem_for_Hawkes_Processes_via_P/figures/002_Table_2.jpg]]
*Table 2: Results on refractory scenario dataset across 1O trials. Notations follow Table 1*

- **Table 3**：支持窗口A存在最优值（约10），过大或过小均降低性能。
- **Table 4**：在真实金融数据上，Ours的预测似然与基线竞争，计算时间显著更短。
- **Table 5-7 & Figure 3**：可扩展性验证——数据规模近线性，维度呈亚立方增长，但U>200后时间增长显著。
- **Table 8**：触发核估计精度与预测性能存在单调正相关。
## 方法谱系与知识库定位

### 与基线方法的关系

本文所提方法（Ours）直接继承并改进了Bonnet & Sangnier (2025)的核方法框架，但通过关键的设计变更实现了质的飞跃。Bonnet方法处理的是带有非线性链接函数的多元Hawkes过程，其条件强度形式为 $\lambda_i(t) = \varphi(\mu_i + \sum_j \int_0^t g_{ij}(t-s) dN_j(s))$，需要求解一个与数据规模成比例的非线性优化问题，计算复杂度高达 $O(N^4 U^2 P)$。本文的核心洞察在于：当限制为线性Hawkes过程（即 $\varphi$ 为恒等映射）并采用惩罚最小二乘对比函数 $L_{LS}$ 替代负对数似然 $L_{LL}$ 时，损失函数呈现二次型结构。这一结构使得无限维优化问题可以通过Mercer展开转化为有限维线性系统，且所有对偶系数解析地固定为1（Theorem 1），从而完全避免了对对偶系数的昂贵优化。

与参数化方法（Exp、Gau、Ber）相比，本文方法保持了核方法的非参数灵活性——Exp仅在真实核为指数形式时表现良好（Table 1中Δ²=0.28），而本文方法在多种核形状下均能自适应。与同样基于核的Gau方法相比，本文在预测精度上相当（T=7000时Ours Δ²=0.16 vs Gau Δ²=0.18），但在计算时间上更具优势（13.1s vs 17.3s）。

### 适用边界与计算特征

本文方法的核心瓶颈在于计算复杂度 $O(N^2 M^2 U^2 + M^3 U^3)$，其中 $M$ 为随机傅里叶特征数，$U$ 为维度。这一复杂度在三个维度上呈现不同的缩放特性：

1. **数据规模 $N$**：复杂度呈 $O(N^2)$ 增长，远优于Bonnet方法的 $O(N^4)$。Table 5显示，当 $N$ 从约2000增长到15000时，CPU时间从5.04s增加到29.5s，验证了二次缩放的实际可行性。

2. **维度 $U$**：复杂度呈 $O(U^3)$ 增长，这是最严格的限制。Table 7显示，当 $U=100$ 时CPU时间为26.9s，$U=200$ 时为160s，$U=500$ 时达到2010s。论文明确指出该方法实际适用于不超过几百维的数据。

3. **特征数 $M$**：复杂度呈 $O(M^3 U^3)$ 增长，但 $M$ 通常远小于 $N$，且可通过随机傅里叶特征近似控制。

### 局限与失败模式

1. **非负性缺失**：基于线性Hawkes过程的方法不保证强度函数的非负性，可能导致负强度值，这在物理上是不合理的。这是所有线性Hawkes过程方法的固有问题。

2. **小数据性能退化**：在数据量较小时（T=2000），本文方法的估计精度（Δ²=0.38）显著低于Bonnet方法（Δ²=0.21）。这是因为Bonnet方法通过非线性链接函数和似然优化在小样本下更有效地利用信息，而本文的闭式解依赖于大样本下二次损失函数的良好性质。

3. **支持窗口敏感性**：Table 3显示支持窗口 $A$ 存在最优值，过大或过小都会降低性能。这要求用户对触发核的时间尺度有先验知识。

4. **共轭梯度法失效**：论文尝试使用共轭梯度法替代Cholesky分解来求解线性系统，但因缺乏合适的预条件子而未能超越Cholesky的性能。

### 开放问题

1. **学习理论分析**：论文缺乏严格的一致性、收敛速率和泛化界分析，这是核方法理论框架中重要的缺失环节。

2. **预条件子设计**：如何设计有效的预条件子以利用共轭梯度法加速大规模线性系统求解，是提升方法可扩展性的关键。

3. **非线性推广**：能否将表示定理推广到非线性链接函数或带有协变量的Hawkes过程，以在保持计算优势的同时提升模型容量？

4. **深度核学习结合**：能否将所提方法与深度核学习（deep kernel learning）结合，以同时利用核方法的理论优势和深度网络的表示能力？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Representer_Theorem_for_Hawkes_Processes_via_Penalized_Least_Squares_Minimization.pdf

![[paperPDFs/ICLR_2026/A_Representer_Theorem_for_Hawkes_Processes_via_Penalized_Least_Squares_Minimization.pdf]]
