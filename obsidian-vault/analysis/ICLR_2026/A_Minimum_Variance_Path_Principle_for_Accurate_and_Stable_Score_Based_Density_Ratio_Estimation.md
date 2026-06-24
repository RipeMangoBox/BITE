---
title: "A Minimum Variance Path Principle for Accurate and Stable Score-Based Density Ratio Estimation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Minimum_Variance_Path_Principle_for_Accurate_and_Stable_Score_Based_Density_Ratio_Estimation.pdf
openreview_forum_id: vf16PZJWD1
aliases:
- MMVPP
- MVPPASSBDRE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/probabilistic_methods
core_operator: "路径方差——概率路径上时间得分函数的二阶矩。选择具有低路径方差的路径能够直接降低估计误差的上界，从而提升密度比估计的准确性与稳定性。"
primary_logic: "将路径方差显式地识别为理想训练目标与实际目标之间的缺失项，提出最小方差路径（MVP）原则：通过可学习的Kumaraswamy混合模型（KMM）参数化路径，直接利用解析的路径方差表达式进行优化，使路径自适应于数据分布，无需手工选择。"
claims:
- "实际目标与理想目标相差一个路径依赖项，该缺失项正是路径方差。"
- "推导出DI和DDBI插值下路径方差的解析闭式表达式，使优化可行。"
- "KMM参数化路径可直接最小化路径方差，实现数据自适应路径，在各种具有挑战性的基准上取得最优性能。"
- "固定路径在不同数据几何下性能不一致，而MVP自适应路径在所有测试场景中始终表现优越或具有竞争力。"
---

# A Minimum Variance Path Principle for Accurate and Stable Score-Based Density Ratio Estimation

> [!tip] 核心洞察
> 将路径方差显式地识别为理想训练目标与实际目标之间的缺失项，提出最小方差路径（MVP）原则：通过可学习的Kumaraswamy混合模型（KMM）参数化路径，直接利用解析的路径方差表达式进行优化，使路径自适应于数据分布，无需手工选择。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 准确稳定的基于得分密度比估计的最小方差路径原理 |
| 英文题名 | A Minimum Variance Path Principle for Accurate and Stable Score-Based Density Ratio Estimation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vf16PZJWD1) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/probabilistic_methods |
| Method | MVP (Minimum Variance Path Principle) |
| Dataset | 高维互信息估计 (d=160, MI=40), 表格数据密度估计 (BSDS300), Additive Noise 互信息估计 (corr=0.9), Gamma-Exponential 互信息估计 (corr=1.8) |

> [!tip] 效果简介
> - 高维互信息估计 (d=160, MI=40) 上，MSE 为 1.02 (MVP Affine)，对比 72.98 (Föllmer Spherical)，变化 显著降低。
> - 表格数据密度估计 (BSDS300) 上，NLL 为 -143.97 (MVP Spherical)，对比 -143.50 (VP Spherical)，变化 -0.47。
> - Additive Noise 互信息估计 (corr=0.9) 上，MSE 为 0.0009 (MVP Spherical)，对比 0.0044 (Cosine Spherical)，变化 降低约一个数量级。

## 概述

基于得分的密度比估计（Score-based DRE）通过沿概率路径积分时间得分来估计两个分布之间的对数密度比。然而，现有方法普遍采用固定的、手工设计的路径调度，忽略了路径选择对估计性能的关键影响。本文揭示了一个被长期忽视的核心瓶颈：实际训练中可处理的切片时间得分匹配（STSM）损失与理想时间得分匹配（TSM）损失之间存在一个路径依赖的方差项，该缺失项正是**路径方差**——即概率路径上时间得分函数的二阶矩积分。

基于这一发现，本文提出**最小方差路径（Minimum Variance Path, MVP）原理**，将路径方差显式地纳入优化目标。理论上，密度比估计误差的上界受限于STSM损失与路径方差之和（Theorem 4.2），因此最小化路径方差能够直接收紧误差界。方法上，本文推导了DI和DDBI两种插值框架下路径方差的解析闭式表达式（Proposition 4.3），使优化可处理；并采用Kumaraswamy混合模型（KMM）参数化路径调度，通过梯度下降直接最小化路径方差，实现数据自适应的路径学习。

实验结果表明，MVP路径在多个具有挑战性的基准上显著优于所有固定路径基线：在高维互信息估计（d=160, MI=40）中，MVP的MSE为1.02，而最优固定路径基线为72.98（Table 3）；在五个真实表格数据集的密度估计中，MVP一致取得最优负对数似然（Table 4）；在Additive Noise和Gamma-Exponential等病理几何数据集上，MVP的MSE通常比固定路径低一个数量级（Table 2）。完整的五数据集评估进一步验证了MVP在广泛相关性和数据几何下的稳健优势（Table 6）。消融实验确认KMM组件数K=5为最优设置（Table 1），而基于方差的时步采样策略有助于稳定训练。

本文的核心贡献在于：将DRE中路径选择的经验问题转化为一个有理论保证的优化问题，并通过解析方差和可学习参数化提供了完整的解决方案。

## 背景与动机

### 基于得分的密度比估计

密度比估计（Density Ratio Estimation, DRE）是机器学习中的基础问题，在互信息估计、密度估计、生成建模等任务中具有广泛应用。给定两个概率分布 $p_0(\mathbf{x})$ 和 $p_1(\mathbf{x})$，密度比 $r(\mathbf{x}) = p_1(\mathbf{x}) / p_0(\mathbf{x})$ 的对数形式可通过时间得分（time score）沿概率路径的积分表示：

$$\log r(\mathbf{x}) = \int_0^1 \partial_t \log p_t(\mathbf{x}) \mathrm{d}t \triangleq \int_0^1 s^{(t)}(\mathbf{x}, t) \mathrm{d}t$$

其中 $p_t(\mathbf{x})$ 是连接 $p_0$ 和 $p_1$ 的概率路径，通过插值机制定义。两种主流插值框架为：

- **确定性插值（DI）**：$\mathbf{x}_t = \alpha(t) \mathbf{x}_0 + \beta(t) \mathbf{x}_1$，要求 $p_0$ 为标准高斯分布。
- **去量化扩散桥插值（DDBI）**：$\mathbf{x}_t = \alpha(t) \mathbf{x}_0 + \beta(t) \mathbf{x}_1 + \sqrt{t(1-t)\gamma^2 + (\alpha(t)^2 + \beta(t)^2)\varepsilon} \mathbf{z}$，通过引入噪声放宽了对 $p_0$ 的高斯假设。

路径调度 $(\alpha(t), \beta(t))$ 需满足边界条件 $\alpha(0)=\beta(1)=1$、$\alpha(1)=\beta(0)=0$，以及单调性约束。

### 实际训练中的隐藏缺口

为训练时间得分模型 $s_\theta^{(t)}$，现有方法最小化理想的时间得分匹配（TSM）目标。然而该目标不可直接计算，实践中采用其可处理替代——切片时间得分匹配（STSM）损失：

$$\mathcal{L}_{\mathrm{STSM}}(\theta) = 2\mathbb{E}_{p_0(\mathbf{x}_0)p_1(\mathbf{x}_1)}\left[s_\theta^{(t)}(\mathbf{x}_0, 0) - s_\theta^{(t)}(\mathbf{x}_1, 1)\right] + \mathbb{E}_{p(t)p_t(\mathbf{x})}\left[2\partial_t s_\theta^{(t)}(\mathbf{x}, t) + s_\theta^{(t)}(\mathbf{x}, t)^2\right]$$

核心问题在于：**实际优化的 STSM 损失与理想 TSM 损失之间存在一个被忽略的路径依赖项**。两者满足如下恒等式（Eq. 9）：

$$\mathcal{L}_{\mathrm{TSM}}(\theta) = \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathbb{E}_{p_t(\mathbf{x})} \left|\partial_t \log p_t(\mathbf{x})\right|^2 \mathrm{d}t$$

该缺失项正是时间得分函数沿路径的二阶矩——即**路径方差**。在固定路径下，该方差项被视为常数而被忽略，但实际上它随路径选择显著变化，直接导致不同路径的估计性能出现系统性差异。

### 路径依赖现象与动机

初步实验（Figure 1）揭示了路径选择的决定性影响：相同任务在不同路径设置下，密度比估计结果差异显著。Figure 1(b-c) 进一步展示了路径方差大小对概率路径几何形态的影响——大方差路径产生不稳定的概率流，小方差路径则保持平滑过渡。

这一现象的根本原因在于：现有方法依赖手工设计的固定路径调度（如线性 $\alpha(t)=1-t$、VP 调度、余弦调度、Föllmer 桥等），这些路径在特定数据分布下可能表现良好，但缺乏对数据几何结构的适应性。当数据分布具有复杂流形、尖锐不连续性或高度非线性依赖时，固定路径的路径方差可能急剧增大，导致估计误差上界松弛，性能显著退化。

因此，一个自然且关键的问题浮现：**能否通过主动选择路径来最小化路径方差，从而提升密度比估计的准确性与稳定性？** 这正是本文提出最小方差路径（Minimum Variance Path, MVP）原理的核心动机。

## 核心创新

### 1. 识别并量化路径方差：从经验选择到理论驱动

现有基于得分的密度比估计（DRE）方法依赖固定、手工设计的概率路径（如线性、VP、余弦调度），其核心缺陷在于：实际优化的**切片时间得分匹配（STSM）损失**与理想但不可解的**时间得分匹配（TSM）损失**之间存在一个被长期忽略的路径依赖项。本文通过严格的代数分解首次揭示这一缺失项的本质——**路径方差**（path variance），即时间得分函数沿路径的二阶矩积分：

$$\mathcal{L}_{\mathrm{TSM}}(\theta) = \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathbb{E}_{p_t(\mathbf{x})} |\partial_t \log p_t(\mathbf{x})|^2 \mathrm{d}t$$

这一恒等式（Eq. 9）表明：仅最小化STSM损失等价于在忽略路径方差的前提下优化理想目标，而路径方差的大小直接取决于路径调度 $\alpha(t), \beta(t)$ 的选择。不同路径的方差差异解释了固定路径在异质数据几何下性能显著波动的现象（Figure 1），将路径设计从启发式选择提升为可量化优化的理论问题。

进一步，本文建立了**最小方差路径（MVP）原理**（Theorem 4.2）：密度比估计的期望误差上界受限于STSM损失与路径方差之和：

$$\mathbb{E}_{p_1(\mathbf{x})} [\Delta(\mathbf{x})] \le e^L \left[ \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathrm{Var}_{p_t(\mathbf{x})} (\partial_t \log p_t(\mathbf{x})) \mathrm{d}t \right]$$

该上界将模型训练误差与路径结构误差解耦，为联合优化提供了理论基础——最小化路径方差能够直接收紧误差界，而无需依赖更强的模型假设。

### 2. 解析路径方差：使优化可行

直接优化路径方差面临核心挑战：方差表达式依赖数据分布 $p_t$ 的未知得分函数。本文的关键突破在于，针对两种主流插值框架——**确定性插值（DI）**和**去量化扩散桥插值（DDBI）**——推导出路径方差的**解析闭式表达式**（Proposition 4.3）：

- **DI框架**：假设 $p_0$ 为标准高斯，路径方差仅依赖路径系数及其导数：
  $$\mathcal{V}_{DI}[\alpha, \beta] = \int_0^1 \left( \frac{2d \dot{\alpha}(t)^2}{\alpha(t)^2} + \frac{\dot{\beta}(t)^2}{\alpha(t)^2} \mathbb{E}_{p_1(\mathbf{x}_1)} [\| \mathbf{x}_1 \|^2] \right) \mathrm{d}t$$

- **DDBI框架**：引入噪声方差 $\sigma_t^2$ 以放松高斯假设，方差表达式为：
  $$\mathcal{V}_{DDBI}[\alpha, \beta] = \int_0^1 \left( \frac{d}{2} \frac{(\dot{\sigma}_t^2)^2}{(\sigma_t^2)^2} + \frac{\mathbb{E}_{p_0(\mathbf{x}_0) p_1(\mathbf{x}_1)} \| \dot{\alpha}(t) \mathbf{x}_0 + \dot{\beta}(t) \mathbf{x}_1 \|^2}{\sigma_t^2} \right) \mathrm{d}t$$

这些解析式将路径方差转化为仅依赖 $\alpha, \beta$ 及其导数的泛函，使基于梯度的路径优化成为可能。值得注意的是，Table 5 显示所有固定路径在DI下均发散，仅在DDBI下有限，这进一步解释了为何DDBI框架在实践中更稳定。

### 3. KMM参数化与自适应路径学习

为实现数据自适应的路径优化，本文提出用**Kumaraswamy混合模型（KMM）**参数化路径调度。KMM的累积分布函数（CDF）天然满足路径的边界条件（$\alpha(0)=1, \alpha(1)=0$）和单调性约束：

$$F_{\phi}(t) = \sum_{k=1}^K w_k \left[ 1 - (1 - t^{a_k})^{b_k} \right], \quad \alpha_{\phi}(t) = 1 - F_{\phi}(t), \quad \dot{\alpha}_{\phi}(t) = -p_{\phi}(t)$$

该参数化将无穷维的路径函数搜索转化为有限维参数 $\phi = \{w_k, a_k, b_k\}_{k=1}^K$ 的无约束优化（Algorithm 2），通过softmax/softplus重参数化保证参数有效性。将 $\alpha_{\phi}$ 代入解析路径方差 $\mathcal{V}[\alpha_{\phi}, \beta_{\phi}]$，即可利用自动微分直接最小化路径方差，使路径自适应于数据分布。消融实验（Table 1）表明，$K=5$ 在表达能力和优化稳定性之间达到最佳平衡。

### 4. 联合优化策略：稳定训练与方差感知采样

与固定路径方法仅优化STSM损失不同，MVP采用**交替优化策略**：在路径参数更新后，刷新基于方差的时步采样分布 $p(t) \propto 1/(\mathrm{Var}(\partial_t \log p_t) + \varepsilon)$，使训练集中于路径方差较大的区域，稳定STSM损失的蒙特卡洛估计。这种联合优化将路径学习与得分模型训练协同，形成完整的自适应DRE框架。

## 整体框架

MVP 的整体 pipeline 由三个核心模块串联构成：**时间得分模型**、**路径优化器**和**密度比估计器**。其输入为来自两个分布的样本对 $(\mathbf{x}_0, \mathbf{x}_1) \sim p_0 \times p_1$，输出为任意点 $\mathbf{x}$ 处的对数密度比估计 $\log \hat{r}(\mathbf{x})$。

**模块关系与数据流**可概括为以下闭环：

1. **时间得分模型**（Time Score Model）接收当前路径调度 $(\alpha_\phi, \beta_\phi)$，通过条件时间得分匹配（CTSM/CJSM）训练时间得分网络 $s_\theta^{(t)}$。该模块的输出是沿路径各时刻的得分预测，其训练损失即为切片时间得分匹配损失 $\mathcal{L}_{\mathrm{STSM}}(\theta)$（Eq. 6）。

2. **路径优化器**（Path Optimizer）利用可学习的 Kumaraswamy 混合模型（KMM）参数化路径调度（Eq. 13–14），并将 Proposition 4.3 给出的解析路径方差 $\mathcal{V}[\alpha_\phi, \beta_\phi]$ 作为优化目标，通过梯度下降直接最小化路径方差。该模块输出最优路径参数 $\phi^*$，并反馈给时间得分模型以更新训练所用的路径。

3. **密度比估计器**（DRE Estimator）在训练完成后，将时间得分模型沿最优路径进行数值积分，得到对数密度比估计（Eq. 5）：
   $$\log \hat{r}(\mathbf{x}) = \int_0^1 s_\theta^{(t)}(\mathbf{x}, t) \, \mathrm{d}t$$

**训练与优化的交替机制**：为避免路径方差估计对时间步采样的敏感性，MVP 采用交替优化策略——每次更新路径参数 $\phi$ 后，刷新基于方差的采样分布 $p(t) \propto 1/(\mathrm{Var}(\partial_t \log p_t) + \varepsilon)$，从而稳定 $\mathcal{L}_{\mathrm{STSM}}$ 的估计。

**关键设计动因**：整个框架的核心驱动力来自 Eq. (9) 揭示的损失分解恒等式：
$$\mathcal{L}_{\mathrm{TSM}}(\theta) = \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathbb{E}_{p_t(\mathbf{x})} |\partial_t \log p_t(\mathbf{x})|^2 \mathrm{d}t$$
该式表明，实际可优化的 STSM 损失与理想的 TSM 损失之间恰好相差一个路径依赖的二阶矩项——即**路径方差**。Theorem 4.2 进一步给出了密度比估计误差的上界：
$$\mathbb{E}_{p_1(\mathbf{x})}[\Delta(\mathbf{x})] \le e^L \left[ \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathrm{Var}_{p_t(\mathbf{x})}(\partial_t \log p_t(\mathbf{x})) \mathrm{d}t \right]$$
这意味着，最小化路径方差能够直接收紧误差上界，从而在理论上保证了联合优化 STSM 损失与路径方差的合理性。MVP 通过 KMM 参数化将原本难以处理的泛函优化转化为有限维参数优化问题，使路径能够自适应于数据分布，无需手工选择。

## 核心模块与公式推导

### 3.1 瓶颈识别：路径方差作为缺失项

基于得分的密度比估计（DRE）将两个分布的对数密度比表示为时间得分沿概率路径的积分：

$$\log r(\pmb{x}) = \int_0^1 s^{(t)}(\pmb{x}, t) \, \mathrm{d}t \tag{Eq. 5}$$

其中 $s^{(t)}(\pmb{x}, t) = \partial_t \log p_t(\pmb{x})$ 为时间得分函数。实际训练中，由于理想的时间得分匹配（TSM）损失不可处理，普遍采用切片时间得分匹配（STSM）损失作为代理目标：

$$\mathcal{L}_{\mathrm{STSM}}(\theta) = 2\mathbb{E}_{p_0(\pmb{x}_0)p_1(\pmb{x}_1)}[s_\theta^{(t)}(\pmb{x}_0,0) - s_\theta^{(t)}(\pmb{x}_1,1)] + \mathbb{E}_{p(t)p_t(\pmb{x})}[2\partial_t s_\theta^{(t)}(\pmb{x},t) + s_\theta^{(t)}(\pmb{x},t)^2] \tag{Eq. 6}$$

本文的核心发现是：理想损失与实际损失之间并非等价，而是相差一个关键的路径依赖项。通过代数恒等式分解：

$$\mathcal{L}_{\mathrm{TSM}}(\theta) = \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathbb{E}_{p_t(\pmb{x})} |\partial_t \log p_t(\pmb{x})|^2 \, \mathrm{d}t \tag{Eq. 9}$$

该缺失项正是**路径方差**——时间得分函数沿概率路径的二阶矩积分。在固定路径方法中，该项被隐含忽略，但其大小直接取决于路径调度 $(\alpha(t), \beta(t))$ 的选择，从而解释了不同路径下估计性能显著差异的现象（Figure 1）。

### 3.2 理论保证：最小方差路径原理

基于Lipschitz连续性假设（$|\partial_\tau \log p_\tau(\pmb{x})| \leq L$），推导出密度比估计误差的上界：

$$\mathbb{E}_{p_1(\pmb{x})}[\Delta(\pmb{x})] \leq e^L \left[ \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathrm{Var}_{p_t(\pmb{x})}(\partial_t \log p_t(\pmb{x})) \, \mathrm{d}t \right] \tag{Theorem 4.2, Eq. 10}$$

其中 $\Delta(\pmb{x}) = |\log r(\pmb{x}) - \log \hat{r}(\pmb{x})|^2$ 为逐点估计误差。该上界由两部分组成：
- **模型损失** $\mathcal{L}_{\mathrm{STSM}}(\theta)$：通过训练时间得分网络可最小化；
- **路径方差** $\mathcal{V} = \int_0^1 \mathrm{Var}_{p_t(\pmb{x})}(\partial_t \log p_t(\pmb{x})) \, \mathrm{d}t$：仅依赖于路径调度，与模型参数无关。

这构成了**最小方差路径（MVP）原理**：选择使路径方差 $\mathcal{V}$ 最小的路径调度，可直接收紧估计误差上界，从而提升密度比估计的准确性与稳定性。

### 3.3 解析路径方差：使优化可行

路径方差 $\mathcal{V}$ 的泛函形式依赖未知的数据分布，无法直接优化。本文的关键技术贡献是：在两种主流插值框架下推导出 $\mathcal{V}$ 的解析闭式表达式，使其仅依赖于路径系数及其导数，消除对数据分布的依赖。

**确定性插值（DI）框架**：概率路径定义为 $\pmb{x}_t = \alpha(t)\pmb{x}_0 + \beta(t)\pmb{x}_1$，假设 $p_0$ 为标准高斯。路径方差的解析式为：

$$\mathcal{V}_{\mathrm{DI}}[\alpha, \beta] = \int_0^1 \left( \frac{2d\dot{\alpha}(t)^2}{\alpha(t)^2} + \frac{\dot{\beta}(t)^2}{\alpha(t)^2} \mathbb{E}_{p_1(\pmb{x}_1)}[\|\pmb{x}_1\|^2] \right) \mathrm{d}t \tag{Proposition 4.3, Eq. 11}$$

其中 $\mathbb{E}_{p_1}[\|\pmb{x}_1\|^2]$ 可从数据中预先估计，$d$ 为数据维度。

**去量化扩散桥插值（DDBI）框架**：引入噪声项构建桥过程 $\pmb{x}_t = \alpha(t)\pmb{x}_0 + \beta(t)\pmb{x}_1 + \sigma_t \pmb{z}$，放松了对 $p_0$ 的高斯假设。路径方差解析式为：

$$\mathcal{V}_{\mathrm{DDBI}}[\alpha, \beta] = \int_0^1 \left( \frac{d}{2} \frac{(\dot{\sigma}_t^2)^2}{(\sigma_t^2)^2} + \frac{\mathbb{E}_{p_0(\pmb{x}_0)p_1(\pmb{x}_1)}\|\dot{\alpha}(t)\pmb{x}_0 + \dot{\beta}(t)\pmb{x}_1\|^2}{\sigma_t^2} \right) \mathrm{d}t \tag{Proposition 4.3, Eq. 12}$$

其中 $\sigma_t^2 = t(1-t)\gamma^2 + (\alpha(t)^2 + \beta(t)^2)\varepsilon$。该表达式通过噪声方差 $\sigma_t^2$ 的引入，使路径方差在端点处保持有限（Table 5 显示所有固定路径在DI下发散，但在DDBI下有限）。

### 3.4 可学习路径参数化：Kumaraswamy混合模型

为将路径方差的泛函优化转化为有限维参数优化，采用**Kumaraswamy混合模型（KMM）**对路径调度进行参数化。

KMM的概率密度函数（PDF）和累积分布函数（CDF）定义为：

$$p_\phi(t) = \sum_{k=1}^K w_k \cdot \mathrm{KS}(t; a_k, b_k), \quad F_\phi(t) = \sum_{k=1}^K w_k [1 - (1 - t^{a_k})^{b_k}] \tag{Eq. 13}$$

其中 $\phi = \{w_k, a_k, b_k\}_{k=1}^K$ 为可学习参数（混合权重 $w_k > 0, \sum w_k = 1$；形状参数 $a_k, b_k > 0$），$\mathrm{KS}$ 为Kumaraswamy分布。

路径系数 $\alpha(t)$ 及其导数由KMM的CDF直接构造：

$$\alpha_\phi(t) = 1 - F_\phi(t), \quad \dot{\alpha}_\phi(t) = -p_\phi(t) \tag{Eq. 14}$$

该构造天然满足边界条件（$\alpha(0)=1, \alpha(1)=0$）和单调性约束，无需额外约束处理。在球面约束下，$\beta(t) = \sqrt{1 - \alpha(t)^2}$；在仿射约束下，$\beta(t) = 1 - \alpha(t)$。

将 $\alpha_\phi, \dot{\alpha}_\phi$ 代入Proposition 4.3的解析方差表达式，路径优化退化为对有限维参数 $\phi$ 的无约束优化：

$$\phi^* = \arg\min_\phi \mathcal{V}[\alpha_\phi, \beta_\phi]$$

优化采用标准重参数化技巧：对无约束潜变量 $\hat{\phi} = \{\hat{w}_k, \hat{a}_k, \hat{b}_k\}$ 通过softmax（权重）和softplus（形状参数）映射到合法参数空间，利用自动微分进行梯度下降（Algorithm 2）。

### 3.5 训练与推理流程

**时间得分模型训练**：采用条件时间得分匹配（CTSM/CJSM）训练时间得分网络 $s_\theta^{(t)}$。在DI和DDBI框架下，条件得分具有闭式表达式，可直接作为回归目标。

**交替优化策略**：为稳定训练，采用交替优化方案——每次更新路径参数 $\phi$ 后，刷新基于方差的 $t$ 采样器 $p(t) \propto 1/(\mathrm{Var}(\partial_t \log p_t) + \varepsilon)$，使STSM损失估计对高方差区域更为鲁棒。

**推理**：训练完成后，将时间得分沿优化路径进行数值积分得到对数密度比估计（Algorithm 1），与常规DRE方法一致，无额外推理开销。

**KMM组件数选择**：消融实验（Table 1）表明 $K=5$ 为最优平衡点——$K=1$ 表达能力不足导致性能显著下降，$K=8$ 反而因过参数化降低性能。

## 实验与分析

### 核心实验设计

实验覆盖三类任务：互信息（MI）估计、密度估计（NLL）和表格数据建模，评估指标为均方误差（MSE）和负对数似然（NLL）。基线方法包括五种固定路径调度——Linear、VP、Cosine、Föllmer、Trigonometric——分别在仿射约束（Affine）和球面约束（Spherical）下运行。MVP路径使用KMM参数化（K=5，经消融确定），通过直接最小化Proposition 4.3中的解析路径方差进行优化。时间得分模型统一采用CTSM/CJSM训练。

### 主要结果

**病理几何下的互信息估计。** 表6汇总了五个具有挑战性几何结构的数据集（Edge-Singular Gaussian、Half-Cube Map、Asinh Mapping、Additive Noise、Gamma-Exponential）上的完整MSE结果，覆盖广泛的相关系数范围。MVP在所有数据集上一致取得最优或最具竞争力的性能。以Additive Noise（尖锐不连续性）和Gamma-Exponential（非线性依赖）为例（表2）：在Additive Noise的corr=0.9条件下，MVP Spherical的MSE为0.0009，而最佳固定路径基线Cosine Spherical为0.0044，降低约一个数量级；在Gamma-Exponential的corr=1.8条件下，MVP Spherical的MSE为0.0004，线性仿射路径为0.0026，同样降低一个数量级。

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/003_Table_2.jpg]]
*Table 2: MSE results on the Additive Noise (sharp discontinuities) and Gamma–Exponential (nonlinear dependency) datasets. Across all correlation levels (top row of each sub-table), MVP achieves notably lower MSE than fixed-path baselines. Full results on 5 datasets given in Tab. 6 in appendix*

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/010_Table_6.jpg]]
*Table 6: (a) MSE results for the Edge-Singular Gaussian dataset*

**高维高差异互信息估计。** 表3展示了MI∈{10,20,30,40} nats、维度d∈{40,80,120,160}条件下的结果。在最具挑战性的d=160、MI=40设置下，MVP Affine取得MSE 1.02，而次优基线Föllmer Spherical为72.98，性能差距显著。这一结果直接验证了最小方差路径原理在“密度鸿沟”问题上的有效性——当两个分布差异极大时，固定路径的路径方差急剧膨胀，而MVP通过自适应调度将其最小化。

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/004_Table_3.jpg]]
*Table 3: Mutual information estimation under high-discrepancy settings ( $\mathbf { M I } \in \{$ 1 0 , 2 0 , 3 0 , 4 0 $\}$ nats). We report the estimated mutual information (mean ± std) and MSE across different path settings and constraint types. Bolded MSE values indicate the best performance for each dimension. Our MVP path demonstrates superior performance in most high-discrepancy settings

**密度估计与表格数据建模。** 图2展示了checkerboard和tree数据集上的密度估计可视化：MVP成功学习到针对每个数据集流形定制的自适应路径，生成的密度估计比固定路径基线更锐利、更准确。在五个真实表格数据集上（表4），MVP在所有基准上一致优于所有固定路径基线，取得新的最优结果：BSDS300上MVP Spherical达到NLL -143.97（VP Spherical为-143.50），POWER上MVP Affine达到NLL -0.81。

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/006_Table_4.jpg]]
*Table 4: Test Negative Log-Likelihood (NLL) on five tabular datasets (lower is better). Our MVP path consistently outperforms all fixed-path baselines, achieving SOTA across the benchmarks*

### 消融实验

**KMM组件数K的影响。** 表1的消融实验在最具挑战性的MI估计（d=160, MI=40）和密度估计（BSDS300）任务上进行。K=1（单Kumaraswamy分布）表达能力受限，MSE为40.60±0.66；K=2有所改善；K=5达到最佳平衡点（MSE 1.02±0.55，NLL -143.97±0.22）；K=8时性能反而下降。这表明过高的K值可能引入优化难度或过拟合，K=5被推荐为默认设置。

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/002_Table_1.jpg]]
*Table 1: Ablation study on the number of KMM components (K) on the most challenging mutual information (MI) estimation ( $\bar { d }$ ~ = ~ 1 6 0 ) and density estimation (BSDS300) tasks. We use mean squared error (MSE) negative log-likelihood (NLL). Lower is better. We recommend K = 5*

**基于方差的t采样策略。** 第4.1节中提出的方差感知时间步采样（$p(t) \propto 1/(\text{Var}(\partial_t \log p_t) + \varepsilon)$）与交替优化策略相结合，有效稳定了STSM损失的估计。这一设计的必要性源于：路径方差在t的某些区域可能极大，均匀采样会导致STSM损失估计的高方差，进而影响路径优化的梯度质量。

### 路径方差分析

表5总结了不同固定路径调度的特性及其在DI和DDBI框架下的方差行为：所有固定路径在DI框架下路径方差发散（因端点奇异性），而在DDBI框架下因噪声正则化而有限。这一分析解释了为何DDBI框架在实践中更稳健，也说明了MVP在两种框架下均能通过优化避免高方差区域。

![[assets/figures/papers/iclr26_0011_vf16PZJWD1_A_Minimum_Variance_Path_Principle_for_Accurate_a/figures/009_Table_5.jpg]]
*Table 5: Summary of path characteristics and associated variance properties*

### 失败模式与局限

尽管MVP在所有测试场景中表现优越，但需注意以下限制：（1）解析路径方差公式依赖特定分布假设——DI要求$p_0$为标准高斯，DDBI依赖条件高斯结构。在完全无参数设定下，这些闭式表达需要新的近似或扩展。（2）路径方差与Lipschitz常数$L$之间的精确理论关系尚未严格建立，当前误差上界（Theorem 4.2）的紧致性有待进一步分析。（3）交替优化策略虽在实践中有效，但缺乏全局收敛性保证。这些局限指向了未来工作的方向。

## 方法谱系与知识库定位

### 与基线方法的关系

MVP 原则在基于得分的密度比估计（DRE）框架内引入了一个新的自由度——概率路径的优化。与现有的固定路径基线相比，MVP 的核心差异在于将路径从手工设计的超参数提升为可学习的对象。

**固定路径基线的共同局限**：Linear、VP、Cosine、Föllmer、Trigonometric 等基线方法均采用预定义的路径调度，其设计遵循特定的几何约束（仿射约束或球面约束），但未考虑数据分布的特性。Table 5 总结了这些路径的特性：所有固定路径在 DI 插值下的路径方差均发散（divergent），仅在 DDBI 插值下保持有限。这意味着在 DI 框架下，这些路径的理论误差上界无法被有效控制，实际性能高度依赖数据与路径的偶然适配。Figure 1 的初步实验直接印证了这一现象：同一估计任务在不同路径设置下，估计值差异显著。

**MVP 的改进机制**：MVP 将路径参数化为 Kumaraswamy 混合模型（KMM），通过直接最小化解析路径方差 $\mathcal{V}[\alpha_\phi, \beta_\phi]$ 来优化路径参数 $\phi$。这一改进的理论依据来自 Eq. (9) 的损失分解恒等式：

$$\mathcal{L}_{\mathrm{TSM}}(\theta) = \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathbb{E}_{p_t(\mathbf{x})} |\partial_t \log p_t(\mathbf{x})|^2 \mathrm{d}t$$

该式揭示了理想时间得分匹配（TSM）损失与实际可优化的切片时间得分匹配（STSM）损失之间相差一个路径依赖的二阶矩项——即路径方差。固定路径方法仅最小化 $\mathcal{L}_{\mathrm{STSM}}$，而忽略了这一缺失项。MVP 则通过 Theorem 4.2 将误差上界显式表达为 STSM 损失与路径方差之和，从而将路径方差纳入优化目标：

$$\mathbb{E}_{p_1(\mathbf{x})} [\Delta(\mathbf{x})] \le e^L \left[ \mathcal{L}_{\mathrm{STSM}}(\theta) + \int_0^1 \mathrm{Var}_{p_t(\mathbf{x})}(\partial_t \log p_t(\mathbf{x})) \mathrm{d}t \right]$$

**性能差距的量化**：在最具挑战性的高维互信息估计任务（$d=160$, MI=40）中，MVP Affine 的 MSE 为 1.02，而最优固定路径基线 Föllmer Spherical 的 MSE 高达 72.98（Table 3），差距接近两个数量级。在 Additive Noise 和 Gamma-Exponential 数据集的各相关性水平下，MVP 的 MSE 普遍比最优固定路径低约一个数量级（Table 2）。在表格数据密度估计的五个真实数据集上，MVP 在所有基准上一致超越所有固定路径基线（Table 4）。

### 适用边界

**依赖的分布假设**：MVP 的解析路径方差公式依赖特定的插值框架假设。DI 插值的方差公式（Proposition 4.3, Eq. (11)）要求 $p_0$ 为标准高斯分布；DDBI 插值的方差公式（Eq. (12)）依赖条件高斯结构。当数据分布显著偏离这些假设时，解析方差公式的准确性需要额外验证，可能需要新的近似或扩展。

**KMM 参数化的表达能力边界**：KMM 通过有限混合分量（推荐 $K=5$，见 Table 1 消融实验）对路径调度进行参数化。Table 1 显示 $K=1$ 时表达能力不足导致性能显著下降，而 $K=8$ 时性能反而回落，表明过参数化可能引入优化困难。KMM 本质上是对 $[0,1]$ 区间上单调函数的逼近，对于需要极端非单调或高频变化的路径形态，其表达能力存在理论上限。

**路径约束类型的影响**：MVP 在仿射约束（$\alpha(t) + \beta(t) = 1$）和球面约束（$\alpha(t)^2 + \beta(t)^2 = 1$）下均有效，但 Table 3 显示在高维高差异场景下，仿射约束的 MVP 显著优于球面约束。这表明路径约束的选择与数据几何之间存在交互效应，最优约束类型可能依赖于具体任务。

### 局限与开放问题

**理论紧致性不足**：当前误差上界（Theorem 4.2）中的 Lipschitz 常数 $L$ 与路径方差之间的关系尚未严格建立。论文明确指出“路径方差与路径 Lipschitz 常数之间的精确理论关系尚未严格建立，目前的联系主要基于经验启发”。这意味着上界的紧致性有限，理论对实践的指导意义在一定程度上依赖经验验证。

**交替优化的次优性**：MVP 采用交替优化策略——在更新路径参数后刷新基于方差的 $t$ 采样器（$p(t) \propto 1/(\mathrm{Var}(\partial_t \log p_t) + \varepsilon)$），以稳定 STSM 损失的估计。这一策略缺乏全局收敛性保证，能否被统一的双层优化框架取代是一个开放问题。

**路径几何的深层理解缺失**：当前方法仅利用路径方差的一阶信息（二阶矩），路径的更高阶特性（如曲率、导数的高阶矩）与估计误差之间的关系未被探索。论文提出的开放问题“路径几何特性与 Lipschitz 常数 $L$ 之间是否存在可量化的解析关系”直指这一理论空白。

**参数化方法的扩展性**：KMM 参数化在低维路径空间（仅 $\alpha(t), \beta(t)$ 两个函数）中有效，但其能否扩展到更一般的函数族（如神经 ODE 参数化的路径）同时保持可优化性，尚待研究。更丰富的参数化可能带来更强的路径表达能力，但也可能引入优化不稳定或方差估计困难。

## 原文 PDF

![[paperPDFs/ICLR_2026/A_Minimum_Variance_Path_Principle_for_Accurate_and_Stable_Score_Based_Density_Ratio_Estimation.pdf]]
