---
title: "A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Statistical_Benchmark_for_Diffusion_Posterior_Sampling_Algorithms.pdf
project_link: null
code_link: https://github.com/zacmar/dps-benchmark
aliases:
- SBDPSA
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "使用离散化Lévy过程作为测试信号，其增量分布（高斯、拉普拉斯、Student-t、伯努利-拉普拉斯）具有稀疏或重尾特性，且后验可通过高效的Gibbs方法精确采样，从而提供黄金标准的后验样本用于分布级比较。"
primary_logic: "通过将Lévy过程先验与Gibbs方法结合，可以构建一个统计基准，该基准能够：（1）提供黄金标准的后验样本，用于直接评估DPS算法的分布级性能；（2）利用Gibbs方法采样去噪后验，实现任意精度的蒙特卡洛估计（如MMSE去噪器或其雅可比），从而将算法误差与学习组件的近似误差分离。"
claims:
- "现有评估方法（如SSIM、FID）不适合后验采样算法的统计评估。"
- "高斯混合先验无法再现幂律极端值，可能高估后验质量。"
- "Gibbs方法提供无参数、无偏差且高效的黄金标准后验样本。"
- "任意精度的蒙特卡洛去噪器可以隔离DPS算法中的算法误差。"
---

# A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms

> [!tip] 核心洞察
> 通过将Lévy过程先验与Gibbs方法结合，可以构建一个统计基准，该基准能够：（1）提供黄金标准的后验样本，用于直接评估DPS算法的分布级性能；（2）利用Gibbs方法采样去噪后验，实现任意精度的蒙特卡洛估计（如MMSE去噪器或其雅可比），从而将算法误差与学习组件的近似误差分离。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散后验采样算法的统计基准 |
| 英文题名 | A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zDI2G8t0of) · [GitHub](https://github.com/zacmar/dps-benchmark) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | A Statistical Benchmark for Diffusion-Posterior-Sampling Algorithms |
| Dataset | Denoising, Deconvolution, Imputation, Fourier |

> [!tip] 效果简介
> - Denoising 上，MMSE optimality gap (dB) 为 DiffPIR (best among DPS)，对比 ℓ2 / ℓ1，变化 DiffPIR typically top performer; for BL(0.1,1), DPS (e.g., 0.72) vs ℓ2 (8.61)。
> - Deconvolution 上，MMSE optimality gap (dB) 为 DiffPIR (best among DPS)，对比 ℓ2 / ℓ1，变化 For BL(0.1,1), DPS (e.g., 1.09) vs ℓ2 (6.11)。
> - Imputation 上，MMSE optimality gap (dB) 为 DiffPIR (best among DPS)，对比 ℓ2 / ℓ1，变化 For BL(0.1,1), DPS (e.g., 0.24) vs ℓ2 (1.10)。

## 概要

该工作提出一个用于评估扩散后验采样（DPS）算法的统计基准，核心动机在于现有评估方法存在根本性缺陷：下游应用指标（如SSIM、FID）不适合后验采样算法的统计评估，而常用的高斯混合先验因尾部指数衰减而无法再现真实信号（如金融资产收益、自然图像）中的幂律极端值或稀疏特性，可能导致对后验质量的过高估计。

核心方法创新在于使用离散化Lévy过程作为测试信号，其增量分布涵盖高斯、拉普拉斯、Student-t和伯努利-拉普拉斯分布，能够模拟稀疏与重尾特性。关键洞察是：这些过程的后验可通过高效的Gibbs方法获得无参数、无偏差的黄金标准样本，从而允许在分布级别直接评估DPS算法。此外，通过Gibbs方法还能获得任意精度的蒙特卡洛MMSE去噪器及其雅可比，从而将DPS算法本身的误差与学习组件的近似误差完全分离。

主要结果基于四个线性逆问题（去噪、反卷积、插值、部分傅里叶测量重建）和一维信号（d=64）的系统实验。定量评估采用MMSE最优性差距（以分贝为单位）和后验覆盖检验。结果显示：在稀疏/重尾设定下DPS算法显著优于模型驱动基线（如伯努利-拉普拉斯增量下，DiffPIR的最优性差距为0.24–1.09 dB，而ℓ2基线为1.10–12.22 dB）；但DPS算法获得的后验覆盖值通常远低于目标水平α=0.9，其中C-DPS和DiffPIR的覆盖值几乎总是0，仅对伯努利-拉普拉斯和Student-t增量例外。



扩散后验采样（DPS）算法旨在解决线性逆问题中的贝叶斯后验采样任务，其核心挑战在于如何从高维、非高斯的后验分布中高效生成样本。然而，当前对该类算法的评估存在根本性缺陷。

**现有评估方法的瓶颈。** 主流评估手段依赖下游应用指标（如 SSIM、FID、LPIPS）或过于简化的先验模型。正如 Pierret & Galerne (2025b) 和 Cardoso et al. (2024) 所指出的，这些指标本质上不适合用于后验采样算法的统计评估。更关键的是，现有基准通常采用高斯混合先验，其尾部以最宽分量的指数速率衰减，属于轻尾分布。这种选择无法再现真实世界中普遍存在的重尾或稀疏特性——例如金融资产收益中常见的幂律极端值（Blattberg & Gonedes, 1974; Cont, 2001）以及自然图像的统计特征（Wainwright & Simoncelli, 2000）。使用此类先验评估算法，可能会系统性地高估后验采样质量，因为算法在应对重尾或稀疏结构时的失败模式被完全掩盖。

**因果机制与核心洞察。** 该研究将问题归因于评估框架中两个可调控的“旋钮”：先验分布的选择和黄金标准后验样本的可获得性。其核心洞察在于，通过将离散化 Lévy 过程作为测试信号，可以同时解决这两个问题。Lévy 过程的增量分布可以灵活地设定为高斯、拉普拉斯、Student-t 或伯努利-拉普拉斯分布，从而精确控制信号的稀疏性和尾部行为。更重要的是，对于这类先验，其后验分布可以通过高效的 Gibbs 方法进行无参数、无偏差的采样。这使得研究者能够获得“黄金标准”的后验样本，用于与 DPS 算法进行直接的、分布级别的比较。此外，利用 Gibbs 方法可以构建任意精度的蒙特卡洛 MMSE 去噪器，从而在评估 DPS 算法时，将算法本身的误差与学习组件（如神经网络去噪器）的近似误差分离开来——这是当前评估体系无法做到的。



## 核心方法与创新机理

本文的核心创新在于构建了一个**统计基准**，用于严格评估扩散后验采样（DPS）算法，而非提出新的DPS算法本身。其创新点体现在以下三个关键槽位的改变上：

1.  **先验分布：从轻尾混合到稀疏/重尾的Lévy过程**
    *   **基线问题**：现有工作多使用高斯混合先验。这类先验尾部呈指数衰减（轻尾），无法再现金融资产收益或自然图像中常见的幂律极端值（重尾）或稀疏性，导致对后验采样质量的评估可能高估。
    *   **本文方案**：采用**离散化Lévy过程**作为测试信号。其增量分布可以是高斯、拉普拉斯、Student-t或伯努利-拉普拉斯，这些分布天然具有稀疏或重尾特性。这一改变使得基准能更真实地模拟现实世界信号。

2.  **评估指标：从下游应用指标到分布级指标**
    *   **基线问题**：广泛使用的SSIM、FID等指标是为评估最终重建图像质量而设计的，不适合评估后验采样算法输出的**分布**质量。如原文所述：“these metrics are ill-suited for the statistical evaluation of posterior-sampling algorithms”。
    *   **本文方案**：引入**MMSE最优性差距**（衡量估计器与黄金标准MMSE估计的均方误差比，单位分贝）和**后验覆盖检验**（衡量估计的可信区间是否准确）等分布级指标。这能直接量化算法在分布层面的误差。

3.  **去噪器：从学习型神经网络到任意精度蒙特卡洛去噪器**
    *   **基线问题**：DPS算法依赖学习得到的神经网络去噪器，其近似误差与算法本身的误差纠缠在一起，难以隔离分析。
    *   **本文方案**：利用Lévy过程后验可高效进行Gibbs采样的特性，构建**任意精度的蒙特卡洛MMSE去噪器**。这能“eliminate approximation errors from a learned surrogate and isolate errors in DPS algorithms themselves”，从而将算法误差与学习组件的近似误差分离开来，实现更纯净的算法性能诊断。

**核心洞察**在于，通过将Lévy过程先验与高效的Gibbs采样方法结合，可以同时解决上述三个问题：Lévy过程提供了逼真且可控的先验，Gibbs方法提供了黄金标准的后验样本（用于计算分布级指标和任意精度的去噪器），从而构建了一个能够严格、公平地评估DPS算法统计性能的基准平台。



![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/163_Figure_18.jpg]]
*Figure 18: Qualitative results for reconstruction from partial Fourier measurements using the learned denoiser. Rows: increment distributions. For each increment distribution, the MMSE estimates obtained by the different DPS algorithms and the gold-standard Gibbs methods are shown on top of the corresponding index-wise marginal variances. Columns: Different measurements*

该基准测试的整体 pipeline 围绕一个核心设计展开：用**离散化 Lévy 过程**替换传统的高斯混合先验，从而使得后验分布能够通过高效的 **Gibbs 方法**获得无参数、无偏差的黄金标准样本。这一设计从根本上解决了现有 DPS 算法评估中依赖下游应用指标（如 SSIM、FID）或轻尾先验所带来的不可靠性问题。

整个框架由四个主要模块构成，其输入输出流如下：

1.  **Lévy 过程信号生成**：生成具有独立平稳增量的测试信号。其密度为各增量分布密度的乘积：$p_{\mathbf{X}}(\mathbf{x}) = \prod_{k=1}^d p_U([\mathbf{D} \mathbf{x}]_k)$。增量分布可选择高斯、拉普拉斯、Student-t 或伯努利-拉普拉斯，以模拟真实信号（如金融资产收益、自然图像）中的重尾或稀疏特性。该模块的输出是一组已知先验分布的测试信号 $\mathbf{x}$。

2.  **线性测量模型**：将生成的信号通过一个前向算子 $\mathbf{A}$ 并添加高斯噪声 $\mathbf{n}$，得到观测数据 $\mathbf{y} = \mathbf{A} \mathbf{x} + \mathbf{n}$。该模块模拟了去噪、反卷积、插值和部分傅里叶测量重建四类逆问题。其输出是观测数据 $\mathbf{y}$，以及已知的算子 $\mathbf{A}$ 和噪声方差 $\sigma_n^2$。

3.  **黄金标准后验采样器（Gibbs 方法）**：这是框架的核心。对于给定的观测 $\mathbf{y}$，该模块利用 Lévy 过程先验的结构，通过高效的 Gibbs 方法（针对高斯、拉普拉斯、Student-t 增量的 GLM Gibbs 采样器，以及针对伯努利-拉普拉斯增量的专用加速采样器）从后验分布 $p_{\mathbf{X}|\mathbf{Y}=\mathbf{y}}(\mathbf{x}) \propto \exp\left(-\frac{1}{2\sigma_n^2}\|\mathbf{A}\mathbf{x} - \mathbf{y}\|^2\right) \prod_{k=1}^d p_U([\mathbf{D}\mathbf{x}]_k)$ 中采样。其输出是黄金标准的后验样本，用于计算任意精度的蒙特卡洛估计，如 MMSE 去噪器 $\hat{\mathbf{x}}_{\mathrm{MMSE}}^{\mathrm{Gibbs}}(\mathbf{y})$ 及其雅可比矩阵。

4.  **通用 DPS 算法模板**：该模板（Algorithm 2）将 C-DPS、DiffPIR、DPnP 等 DPS 算法统一为一个标准流程。其输入是观测数据 $\mathbf{y}$、前向算子 $\mathbf{A}$ 和噪声方差 $\sigma_n^2$。在每一步反向扩散过程中，算法会调用一个去噪器（可以是学习的神经网络，也可以是来自模块 3 的任意精度蒙特卡洛去噪器）来估计 $\mathbb{E}[\mathbf{X}_0 | \mathbf{X}_t = \mathbf{x}_t]$。模板的核心优势在于，通过替换去噪器，可以隔离 DPS 算法本身的误差与学习组件的近似误差。其输出是 DPS 算法生成的后验样本。

**模块间的关系**：模块 1 和 2 共同提供了有明确先验和真值的测试问题。模块 3 提供了评估的“黄金标准”。模块 4 是待评估的目标。通过对比模块 4 的输出（如 MMSE 估计 $\hat{\mathbf{x}}^{\mathrm{est}}(\mathbf{y})$）与模块 3 的黄金标准输出，可以计算 **MMSE 最优性差距**（MMSE optimality gap），即 $10 \log_{10}\left( \frac{\|\hat{\mathbf{x}}^{\mathrm{est}}(\mathbf{y}) - \mathbf{x}\|^2}{\|\hat{\mathbf{x}}_{\mathrm{MMSE}}^{\mathrm{Gibbs}}(\mathbf{y}) - \mathbf{x}\|^2} \right)$，从而在分布级别上量化 DPS 算法的性能。此外，还可以利用黄金标准样本进行后验覆盖检验（posterior-coverage tests），评估 DPS 算法生成的不确定性是否校准。



本节梳理该统计基准的核心数学模块与关键公式，聚焦于线性逆问题的概率建模、扩散后验采样（DPS）的通用模板，以及用于评估的最优性差距度量。

### 1. 线性逆问题与贝叶斯后验

基准考虑标准的线性测量模型，测量方程定义为：

$$ \mathbf { y } = \mathbf { A } \mathbf { x } + \mathbf { n } $$

其中 $\mathbf{A} \in \mathbb{R}^{m \times d}$ 为前向算子（如去噪中的单位阵、反卷积中的卷积矩阵、插值中的掩码、部分傅里叶测量中的子采样傅里叶矩阵），$\mathbf{n}$ 为独立同分布的高斯噪声，方差为 $\sigma_n^2$。

给定测量值 $\mathbf{y}$，信号 $\mathbf{x}$ 的后验分布由贝叶斯规则给出：

$$ p _ { \mathbf {X} | \mathbf {Y = y} } ( \mathbf {x} ) \propto p _ { \mathbf {Y} | \mathbf {X = x} } ( \mathbf {y} ) p _ { \mathbf {X} } ( \mathbf {x} ) $$

在高斯噪声假设下，似然函数为：

$$ p _ { \mathbf {Y | X = x} } ( \mathbf {y} ) \propto \exp \bigl ( { - \frac { 1 } { 2 \sigma _ { \mathrm {n} } ^ { 2 } } \bigl \| \mathbf {A x} - \mathbf {y} \bigr \| ^ { 2 } } \bigr ) $$

### 2. 基于Lévy过程增量的先验与后验

基准的核心创新在于使用离散化Lévy过程作为测试信号的先验。信号 $\mathbf{x} \in \mathbb{R}^d$ 的增量由差分矩阵 $\mathbf{D} \in \mathbb{R}^{d \times d}$ 定义，其先验密度为各独立同分布增量密度的乘积：

$$ p _ { \mathbf {X} } ( \mathbf {x} ) = \prod _ { k = 1 } ^ { d } p _ { U } \big ( [ \mathbf {D} \mathbf {x} ] _ { k } \big ) $$

其中 $p_U$ 是增量分布，可以是高斯（Gauss）、拉普拉斯（Laplace）、Student-t（St）或伯努利-拉普拉斯（BL）。这种构造使得后验分布具有封闭形式：

$$ p _ { \mathbf {X} | \mathbf {Y} = \mathbf {y} } ( \mathbf {x} ) \propto \exp \bigl ( - \frac { 1 } { 2 \sigma _ { \mathrm {n} } ^ { 2 } } \| \mathbf {A} \mathbf {x} - \mathbf {y} \| ^ { 2 } \bigr ) \prod _ { k = 1 } ^ { d } p _ { U } \bigl ( [ \mathbf {D} \mathbf {x} ] _ { k } \bigr ) $$

该后验的关键特性在于：它可以通过高效的Gibbs方法进行无参数、无偏差的精确采样，从而提供黄金标准的后验样本。对于高斯、拉普拉斯和Student-t增量，使用GLM Gibbs采样器（Algorithm 1）；对于伯努利-拉普拉斯增量，使用专门的潜变量Gibbs采样器（Algorithm 4），该采样器通过分层表示（Dirac-δ与高斯混合）实现高效采样，并获得了74.61倍的累积加速。

### 3. 扩散后验采样（DPS）的通用模板

基准将DPS算法统一为Algorithm 2所示的通用模板。该模板的核心在于利用扩散模型的反向过程从条件分布 $p_{\mathbf{X}_0|\mathbf{Y}=\mathbf{y}}$ 中采样。扩散过程由前向SDE定义：

$$ \mathrm { d } \mathbf { X } _ { t } = \mathbf { f } ( \mathbf { X } _ { t } , t ) \mathrm { d } t + g ( t ) \mathrm { d } \mathbf { W } _ { t } $$

其反向SDE为：

$$ \mathrm { d } \mathbf { X } _ { t } = \left( \mathbf { f } ( \mathbf { X } _ { t } , t ) - g ^ { 2 } ( t ) \nabla \log p \mathbf { x } _ { t } ( \mathbf { X } _ { t } ) \right) \mathrm { d } t + g ( t ) \mathrm { d } \mathbf { W } _ { t } $$

反向过程中，得分函数 $\nabla \log p_{\mathbf{X}_t}$ 通过Tweedie公式与MMSE去噪器关联：

$$ \nabla \log p _ { \mathbf {X} _ { t } } ( \mathbf {x} ) = - \sigma ( t ) ^ { - 2 } \big ( \mathbf {x} - \alpha ( t ) \mathbb { E } [ \mathbf {X} _ { 0 } \mid \mathbf {X} _ { t } = \mathbf {x} ] \big ) $$

DDPM的离散反向步骤可由此推导：

$$ \mathbf {X} _ { t - 1 } = \frac { 1 } { \sqrt { 1 - \beta _ { t } } } \left( \mathbf {X} _ { t } + \beta _ { t } \nabla \log p _ { \mathbf {X} _ { t } } ( \mathbf {X} _ { t } ) \right) + \sqrt { \beta _ { t } } \mathbf {Z} _ { t } $$

对于条件采样，后验得分分解为：

$$ \nabla \log p _ { { \mathbf {X} } _ { t } | { \mathbf {Y} } = { \mathbf {y} } } = \nabla \log p _ { { \mathbf {X} } _ { t } } + \nabla { \big ( } { \mathbf {x} } \mapsto \log p _ { { \mathbf {Y} } | { \mathbf {X} } _ { t } = { \mathbf {x} } } ( { \mathbf {y} } ) { \big ) } $$

基准框架的关键优势在于：可以通过Gibbs方法获得任意精度的蒙特卡洛MMSE去噪器 $\mathbb{E}[\mathbf{X}_0|\mathbf{X}_t=\mathbf{x}_t]$ 及其雅可比矩阵（等于条件协方差矩阵），从而完全消除学习去噪器引入的近似误差，将DPS算法本身的算法误差与学习组件的误差分离开来。

### 4. 评估指标：MMSE最优性差距

基准使用MMSE最优性差距作为核心分布级评估指标，定义为：

$$ 10 \log_{10} \left( \frac{ \| \hat{\mathbf{x}}^{\mathrm{est}}(\mathbf{y}) - \mathbf{x} \|^2 }{ \| \hat{\mathbf{x}}_{\mathrm{MMSE}}^{\mathrm{Gibbs}}(\mathbf{y}) - \mathbf{x} \|^2 } \right) $$

其中 $\hat{\mathbf{x}}^{\mathrm{est}}(\mathbf{y})$ 是待评估方法（如C-DPS、DiffPIR、DPnP）的估计，$\hat{\mathbf{x}}_{\mathrm{MMSE}}^{\mathrm{Gibbs}}(\mathbf{y})$ 是通过Gibbs方法获得的黄金标准MMSE估计。该指标以分贝为单位，0 dB表示完美重建，正值越大表示与最优估计的差距越大。



## 实验与关键发现

### 主要结果：MMSE最优性差距

本文通过MMSE最优性差距（dB，越低越好，0为完美重建）评估了三种DPS算法（C-DPS、DiffPIR、DPnP）与两个模型驱动基线（ℓ2和ℓ1重建）在四种线性逆问题（去噪、反卷积、插值、部分傅里叶重建）上的表现。测试信号维度为d=64，增量分布包括高斯、拉普拉斯、Student-t（St(1)）和伯努利-拉普拉斯（BL(0.1,1)）。

**核心发现：** 在重尾或稀疏信号场景下，DPS算法显著优于模型驱动基线，但所有DPS算法与黄金标准Gibbs后验样本之间仍存在系统性差距。

*   **伯努利-拉普拉斯（稀疏-重尾混合）：** 这是DPS算法优势最明显的场景。例如，在反卷积任务中，对于BL(0.1,1)增量，DiffPIR的最优性差距为1.09 dB，而ℓ2基线高达6.11 dB；在去噪任务中，DiffPIR为0.72 dB，ℓ2为8.61 dB；在傅里叶重建中，差距更为悬殊（0.83 dB vs 12.22 dB）。这表明DPS算法在处理具有尖峰和重尾特性的信号时，能够更好地利用先验信息。
*   **高斯和拉普拉斯增量：** 在这些相对简单的场景下，DPS算法与模型驱动基线的差距缩小，有时甚至不如调优后的ℓ1或ℓ2基线。例如，在高斯增量去噪中，ℓ2基线的最优性差距（约0.01 dB）优于所有DPS算法。这揭示了DPS算法在简单先验下可能引入不必要的复杂性或近似误差。
*   **DPS算法内部比较：** 在大多数实验配置中，DiffPIR是DPS算法中的最佳表现者（表中粗体标注）。DPnP紧随其后，而C-DPS的表现则显著较差，尤其是在傅里叶重建任务中，其最优性差距经常远大于其他两种方法。

### 消融与诊断：去噪器质量与超参数敏感性

**去噪器替换消融：** 通过将DPS算法中使用的学习型神经网络去噪器替换为通过Gibbs方法获得的任意精度蒙特卡洛去噪器，可以隔离算法误差与学习组件的近似误差。实验结果（Table 4）显示，这种替换对DPnP的影响最大。例如，对于St(1)增量的插值任务，使用蒙特卡洛去噪器后，DPnP的最优性差距降低了10.46 dB，几乎消除了所有误差。这表明DPnP的性能瓶颈主要在于其使用的去噪器质量。相比之下，对于C-DPS和DiffPIR，替换去噪器带来的改善较小，甚至在某些情况下（如高斯增量）会导致性能下降，说明它们的核心算法误差或超参数设置是更大的限制因素。

![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/018_Table_4.jpg]]
*Table 4: Change in MMSE optimality gap (mean ± standard deviation) after substituting the learned denoiser with the arbitrary-precision denoiser. An asterisk indicates a significant changes according to a Wilcoxon signed-rank test ( p = 0 . 0 5 ) . Negative number with asterisk: MMSE estimates obtained with the arbitrary-precision denoiser are significantly better. Positive number with asterisk: MMSE estimates obtained with the learned denoiser are significantly better*

**超参数敏感性：** 实验中，所有DPS算法的超参数均针对学习型去噪器通过网格搜索调优。当去噪器更换为蒙特卡洛版本后，若直接重用这些超参数，性能会显著恶化。例如，对于St(1)增量的插值任务，DiffPIR的最优性差距恶化了13.56 dB。这揭示了DPS算法对超参数的高度敏感性，以及其性能与去噪器质量之间的复杂耦合关系。一个针对低质量去噪器调优的超参数，在高质量去噪器上可能完全不适用。

### 后验覆盖检验

后验覆盖检验（α=0.9）评估了DPS算法生成样本的不确定性量化是否准确。一个理想的后验采样器应使得真实信号落入其90%最高后验密度区域的概率接近0.9。

**关键发现：** 所有DPS算法的后验覆盖值都普遍远小于0.9，表明它们严重低估了后验不确定性。
*   **C-DPS和DiffPIR：** 在大多数情况下，它们的覆盖值几乎为0，仅在BL(0.1,1)和St(1)增量下略高于0。这强烈表明这两种算法产生的样本分布与真实后验分布存在本质上的不匹配，其样本方差不能可靠地反映估计的不确定性。
*   **DPnP：** 在所有实验配置中，DPnP报告的覆盖值最接近0.9，但通常仍小于0.9。这表明DPnP在不确定性量化方面优于其他DPS算法，但其校准仍然是不足的。

### 失败模式与局限性

1.  **一维信号的局限：** 当前基准仅适用于一维信号（d=64）。扩展到二维图像会面临Gibbs方法计算和内存的挑战（例如，Cholesky分解在d=8096时内存耗尽）。
2.  **模型假设的局限：** Gibbs方法仅适用于线性逆问题和高斯噪声。对于非线性测量模型或非高斯噪声，需要开发新的方法。
3.  **伯努利-拉普拉斯采样器效率：** 尽管实现了74.61倍的累积加速，伯努利-拉普拉斯增量分布的Gibbs采样器运行时仍显著长于其他分布。
4.  **超参数脆弱性：** DPS算法的性能高度依赖于针对特定去噪器调优的超参数，缺乏鲁棒性。

### 补充图表

![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/008_Table_1.jpg]]
*Table 1: MMSE optimality gap in decibel (mean ± standard deviation; lower is better; 0 is a perfect reconstruction) of various estimation methods over the test set. Bold: best among DPS algorithms*

![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/011_Table_2.jpg]]
*Table 2: Univariate distributions used throughout this work. Parameters appear in the order they are specified in this table, e.g. Gauss ( $\mu , \sigma ^ { 2 }$ )

![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/012_Table_3.jpg]]
*Table 3: Latent variable representations and conditional distributions for common distributions*

![[assets/figures/papers/iclr26_0004_zDI2G8t0of_A_Statistical_Benchmark_for_Diffusion-Posterior-/figures/019_Table_5.jpg]]
*Table 5: Runtime of the benchmark with learned objects*



## 定位与知识库关联

### 与基线方法的关系

本文的核心贡献在于构建了一个用于评估扩散后验采样（DPS）算法的统计基准，而非提出新的DPS算法。其方法谱系中的基线可分为两类：**模型驱动基线**与**DPS算法基线**。

**模型驱动基线**包括 $\ell_2$ 重建和 $\ell_1$ 重建，分别对应高斯增量分布和拉普拉斯增量分布下的最大后验（MAP）估计。这些方法直接优化显式正则化目标，不涉及扩散模型。它们的角色是提供传统方法在测试信号上的性能下限，用于对比DPS算法的相对优势。

**DPS算法基线**包括 C-DPS、DiffPIR 和 DPnP 三种代表性方法。它们共享一个通用模板（Algorithm 2）：从扩散模型的反向过程中采样，并通过某种机制（如协方差调整、近端优化或去噪器近端映射）将测量信息注入采样轨迹。本文的基准不改变这些算法的内部机制，而是通过替换其关键组件（先验分布、评估指标、去噪器）来暴露它们的性能瓶颈。

### 关键差异：从“下游指标”到“分布级评估”

现有DPS研究的评估方法存在一个根本性瓶颈：依赖SSIM、FID等下游应用指标，或使用过于简化的高斯混合先验。这些指标不适合后验采样算法的统计评估（Pierret & Galerne, 2025b; Cardoso et al., 2024），且高斯混合先验无法再现幂律极端值（常见于资产收益和自然图像），可能高估后验质量。

本文通过三个关键变更解决了这一瓶颈：

1. **先验分布**：从轻尾的高斯混合先验改为离散化Lévy过程先验，其增量分布包括高斯、拉普拉斯、Student-t和伯努利-拉普拉斯，具有稀疏或重尾特性。这使得测试信号更接近真实世界信号（如金融资产收益）的统计特性。
2. **评估指标**：从下游指标改为分布级指标——MMSE最优性差距和后验覆盖检验。MMSE最优性差距直接衡量估计器与黄金标准MMSE估计之间的差距（单位dB），后验覆盖检验则评估算法生成样本的校准程度。
3. **去噪器**：从学习得到的神经网络去噪器改为通过Gibbs方法获得的任意精度蒙特卡洛去噪器。这一变更的因果机制在于：通过消除学习组件的近似误差，可以将DPS算法本身的误差与去噪器误差分离，从而精确定位算法缺陷。

### 适用边界与局限

本文基准的适用边界由以下因素定义：

- **信号维度**：当前仅适用于一维信号（d=64）。扩展到更高维信号（如图像）面临计算和内存挑战——Cholesky分解在d=8096时已耗尽内存（Figure 6）。
- **问题类型**：仅适用于线性逆问题和高斯噪声假设。非线性测量模型或非高斯噪声需要新的方法。
- **先验族**：仅适用于Lévy过程先验。虽然这覆盖了重尾和稀疏分布，但并非所有真实信号都符合这一假设。

实验中的局限性还包括：
- 伯努利-拉普拉斯增量分布的Gibbs采样器虽然经过加速（实现74.61倍累积加速），但运行时仍显著长于其他分布。
- DPS算法的超参数对去噪器质量敏感。当去噪器改变时（如从学习去噪器替换为蒙特卡洛去噪器），C-DPS和DiffPIR的性能可能恶化而不重新调优。实验表明，对于St(1)增量的插值任务，DiffPIR在重用超参数时最优性差距恶化了13.56 dB。

### 开放问题

1. **后验校准**：DPS算法获得的后验覆盖值通常远小于目标水平α=0.9（C-DPS和DiffPIR几乎总是0），如何校准这些算法以实现接近α的覆盖？
2. **超参数鲁棒性**：当去噪器质量改变时，C-DPS和DiffPIR能否在不重新调优的情况下改善性能？当前证据表明不能，但这是否是算法固有缺陷尚待验证。
3. **可扩展性**：Gibbs方法在更大维度（如d=8096）下的可扩展性如何？Perturb-and-MAP方法虽然表现出次线性运行时，但Cholesky方法的内存瓶颈需要解决。
4. **泛化性**：该基准能否扩展到非线性测量模型和非高斯噪声？这需要新的Gibbs方法或替代的黄金标准采样策略。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Statistical_Benchmark_for_Diffusion_Posterior_Sampling_Algorithms.pdf

![[paperPDFs/ICLR_2026/A_Statistical_Benchmark_for_Diffusion_Posterior_Sampling_Algorithms.pdf]]
