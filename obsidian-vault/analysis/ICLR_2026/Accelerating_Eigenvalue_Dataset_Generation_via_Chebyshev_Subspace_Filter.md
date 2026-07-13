---
title: "Accelerating Eigenvalue Dataset Generation via Chebyshev Subspace Filter"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerating_Eigenvalue_Dataset_Generation_via_Chebyshev_Subspace_Filter.pdf
project_link: null
code_link: null
aliases:
- SCSFS
- AEDGCSF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/physics
core_operator: "同一分布下算子间的相似性（谱分布与不变子空间的接近程度）被现有方法完全忽略；利用这种相似性，通过重排求解顺序并用已求解问题的特征对加速后续求解，可以大幅减少冗余计算。"
primary_logic: "将独立的特征值问题序列化为一个受排序引导的连续求解过程：先用截断 FFT 排序按低频相似度重排矩阵，再以切比雪夫滤波子空间迭代进行串行求解，并将前一个问题的收敛特征对作为下一个问题的高质量初始子空间，从而把昂贵的迭代收敛转化为廉价的继承与滤波。"
claims:
- "SCSF 相对于最佳对比方法 ChFSI 获得最高 3.5× 加速（Helmholtz 算子，dim=6400，L=200），相对于传统求解器 Eigsh 可达 4.8×。"
- "排序模块使 SCSF 求解时间减少 1.3–2.8×，迭代次数降低 5–50%，总浮点操作减少 7–43%。"
- "截断 FFT 排序中高频成分仅占参数矩阵总能量的 <5%，保证低频相似度能充分近似算子距离。"
- "即使在不连续数据集（混合 Helmholtz 与 Poisson）上，SCSF 仍全面优于基线求解器，证实其鲁棒性。"
---

# Accelerating Eigenvalue Dataset Generation via Chebyshev Subspace Filter

> [!tip] 核心洞察
> 将独立的特征值问题序列化为一个受排序引导的连续求解过程：先用截断 FFT 排序按低频相似度重排矩阵，再以切比雪夫滤波子空间迭代进行串行求解，并将前一个问题的收敛特征对作为下一个问题的高质量初始子空间，从而把昂贵的迭代收敛转化为廉价的继承与滤波。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于切比雪夫子空间滤波的特征值数据集加速生成方法 |
| 英文题名 | Accelerating Eigenvalue Dataset Generation via Chebyshev Subspace Filter |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rrbCQT7JKX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/physics |
| Method | Sorting Chebyshev Subspace Filter (SCSF) |
| Dataset | Helmholtz operator, dim=6400, L=200, tol=1e-8; Generalized Poisson operator, dim=10000, L=400, tol=1e-12; Helmholtz operator (FEM), tol=1e-8 |

> [!tip] 效果简介
> - Helmholtz operator, dim=6400, L=200, tol=1e-8 上，平均计算时间 (秒) 为 31.31，对比 107.1 (ChFSI)，变化 3.4× 加速。
> - Helmholtz operator, dim=6400, L=200, tol=1e-8 上，平均计算时间 (秒) 为 31.31，对比 151.7 (Eigsh)，变化 4.8× 加速。
> - Generalized Poisson operator, dim=10000, L=400, tol=1e-12 上，平均计算时间 (秒) 为 158.49，对比 3162.28 (Eigsh)，变化 20× 加速。

## 概要

特征值数据集是大规模偏微分方程（PDE）算子学习与物理仿真中的重要基础数据。传统生成流程对数据集中每个算子的离散矩阵**独立求解特征值问题**，这一步占总体计算开销的 95% 以上。然而，现有数值求解器（Eigsh、LOBPCG、Krylov‑Schur、Jacobi‑Davidson 等）在面对高维、多特征对、高精度的批量求解时难以承受，构成训练数据驱动模型的关键效率瓶颈。

该瓶颈的根本原因在于**同一参数分布下算子间的谱相似性被完全忽略**。不同参数对应的微分算子往往具有相近的谱分布与不变子空间，但现行方法将它们视为彼此无关的独立问题，导致大量冗余的高成本迭代收敛计算。

针对这一问题，本文提出一种名为 **排序切比雪夫子空间滤波（Sorting Chebyshev Subspace Filter, SCSF）** 的方法。其核心思想是将批量特征值问题从一个**独立求解的集合**转换为一个**由排序引导的连续热启动求解序列**：先用截断快速傅里叶变换（FFT）按其低频参数矩阵的 Frobenius 距离进行贪心排序，使相邻算子的谱分布尽量接近；然后以切比雪夫滤波子空间迭代（ChFSI）依次求解，每个问题都继承前一个问题已收敛的特征对所构成的高质量初始子空间，从而将耗时的迭代收敛转化为廉价的继承与滤波。该方法完全保留数值代数的精度可控性，不改变指定精度下的求解结果。

实验表明，SCSF 在不同类型的 PDE 算子上实现了显著加速。以 Helmholtz 算子为例（矩阵维度 6400，求解 200 个特征对，容差 $10^{-8}$），SCSF 比当前最优的对比方法 ChFSI 快 **3.4 倍**，比广泛使用的传统求解器 Eigsh 快 **4.8 倍**。在广义 Poisson 算子上（维度 10000，求解 400 个特征对），加速比可达 **20 倍**。消融分析揭示了加速的两个来源：排序模块使求解时间减少 1.3–2.8 倍，迭代次数降低 5–50%；切比雪夫子空间滤波的热启动则使 ChFSI 在排序序列上持续受益，且方法在算子分布不连续等挑战场景下仍保持鲁棒性。



数据驱动的特征值求解器（如 NeurKItt）需要大规模、高精度的特征值数据集作为训练样本。这类数据集的生成流程高度依赖数值线性代数求解器：对每个参数化算子进行离散化后，独立求解矩阵的特征值问题。实验中观察到，这一独立求解步骤占整体计算开销的 95% 以上（Table 1、Figure 1）。当矩阵维度达到数千乃至上万，且需求解数百个特征对时，传统 Krylov 子空间方法（如 Eigsh、LOBPCG、Krylov–Schur）或 Jacobi–Davidson 迭代都因反复构建正交子空间而变得极为昂贵，成为数据生成的瓶颈。

现有流程的根本缺口在于，它将同一分布下产生的多个特征值问题视为完全独立的实例。实际上，这些算子共享相似的谱分布与不变子空间结构——参数矩阵之间的 Frobenius 距离可以很好地反映谱相似程度。由于所有方法都采用随机初始子空间并从零开始迭代，这一结构性相似度被完全忽略，导致大量冗余计算。

本文的动机正是将这种相似度转化为计算节约：**将原本孤立的求解过程重新排序为一个连续的串行序列，并让已收敛的特征对服务于后续求解**。具体而言，SCSF 首先通过截断 FFT 排序将参数矩阵重排为谱上更接近的序列（低频成分即占算子距离的绝大部分，高频截断误差小于 5% 总能量，见 Table 20），随后用切比雪夫滤波子空间迭代逐一求解。在每个新问题上，前一问题已收敛的特征对直接作为高精度的初始子空间，切比雪夫多项式则对该区间进行放大滤波，使 Rayleigh–Ritz 过程只需极少的迭代即收敛。这样一来，原本昂贵的"从零冷启动"被替换为廉价的"子空间继承 + 定向滤波"。

关键证据表明这一策略有效且鲁棒：在 Helmholtz 算子（dim=6400, L=200）上，SCSF 相对最好的基线 ChFSI 实现 **3.5×** 加速，相对传统求解器 Eigsh 可达 **4.8×**（Table 1）；排序模块单独带来 1.3–2.8× 求解时间缩减，并降低 5–50% 迭代次数（Table 3）；即使在不连续数据集（混合 Helmholtz 与 Poisson 算子）上，SCSF 仍全面优于所有竞争方法（Table 18），验证了框架对算子相似度变化的鲁棒性。这些结果共同表明，利用算子间相似性来重组求解顺序并复用特征空间，是从数值线性代数角度加速特征值数据集生成的高效路径。



## 核心方法与创新机理

特征值数据集生成的核心瓶颈在于：对每个算子独立求解大规模特征值问题占据了总计算开销的 95% 以上，传统数值求解器在大维度、高精度要求下难以承受。SCSF 的关键创新是将批量独立求解转变为**由排序引导的串行热启动流程**，通过显式利用同一分布下算子在谱分布和不变子空间上的相似性，将昂贵的迭代收敛过程大幅压缩为廉价的继承与滤波。

这一范式变化通过三个相互耦合的设计槽位（changed slots）实现：

**1. 排序策略：从无排序/全参贪心到截断 FFT 低频近似**
基线方法或者不做排序，或者直接基于完整参数矩阵的 Frobenius 距离使用贪心排序，计算复杂度高达 $\mathcal{O}(N^2 p^2)$（$N$ 为问题数，$p$ 为参数矩阵边长）。SCSF 改为对参数矩阵先执行截断 FFT，仅保留低频分量（截断频率 $p_0 = 20$），再在低维频域空间执行贪心排序，总体复杂度降至 $\mathcal{O}(N^2 p_0^2 + N p^2 \log p)$。实验表明，高频成分仅占参数矩阵总能量的 5% 以下（Table 20），因此低频相似度能够充分近似算子间的真实谱距离。排序模块单独使 SCSF 的求解时间减少 1.3–2.8×，迭代次数下降 5–50%，总浮点操作减少 7–43%（Table 3），而排序本身的计算开销极低——在 $10^4$ 规模数据集上仅需 0.1658 s，远低于完整贪心排序的 592.7 s（Table 4）。

**2. 初始子空间策略：从随机初始化到继承前一问题的收敛特征对**
传统求解器（Eigsh、LOBPCG、KS、JD）和 ChFSI 均采用随机或默认初始子空间，每次求解都需从零开始迭代。SCSF 在排序后，将前一问题的收敛特征向量直接作为当前问题的初始子空间。这一设计**仅对 Chebyshev 滤波子空间迭代有效**：在 ChFSI 上启用继承后，求解时间从 107.1 s 大幅降至 31.31 s（Table 1）；而同样的修改对 Eigsh、KS 等 Krylov 方法无帮助，甚至使 JD 性能恶化（Table 2）。这揭示出热启动的成功依赖于滤波型方法能够有效利用已收敛的不变子空间，是排序与滤波深度绑定的协同创新。

**3. 求解策略：从独立求解到排序–串行滤波流水线**
基线方法将数据集中的每个特征值问题视为孤立任务。SCSF 则通过"排序–串行求解"流水线将其重构成一个连续过程：首先用截断 FFT 贪心排序得到谱相似度高的矩阵序列；然后依次对每个矩阵执行 Chebyshev 滤波子空间迭代（ChFSI）——在每一次迭代中，以上一问题的收敛特征向量构造初始子空间，利用切比雪夫多项式放大目标谱区间（过滤步占总耗时 70% 以上，Table 11），再通过 Rayleigh‑Ritz 过程精化并锁定收敛特征对。这套"继承–滤波–精化"循环将原先各自独立的迭代收敛转化为廉价的子空间继承与滤波，使 SCSF 在 Helmholtz 算子（dim=6400, L=200）上相对最佳对比方法 ChFSI 获得最高 3.5× 加速，相对 Eigsh 可达 4.8×（Table 1）；在广义 Poisson 算子（dim=10000, L=400）上相对 Eigsh 更是获得 20× 加速（Table 10）。即使在不连续的数据集（混合 Helmholtz 与 Poisson）上，SCSF 仍然全面优于所有基线求解器（Table 18），显示出较强的鲁棒性。

综上，SCSF 的本质贡献并非单一求解器的参数优化，而是通过**排序模块**和**继承式滤波子空间**两处模块化创新，将批量特征值求解的范式从互相独立彻底转变为强相关的谱加速流水线。该加速效果与算子间的相似度直接相关：当数据集内的矩阵完全相同时，求解仅需 2 s（Eigsh 需 151 s）；随着相似度下降，加速比逐渐向 ChFSI 基线靠拢（Table 17），恰恰印证了因果旋钮——**算子的低频谱相似性是加速的根本来源**，而截断 FFT 排序和子空间继承是对这一相似性的高效利用。



![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/003_Figure_2.jpg]]
*Figure 2: Algorithm Flow Diagram: a. Generation of operators to be solved. b. Discretization of operators into matrices. c. Apply SCSF algorithm to sort matrices, obtaining a sequence with strong correlations. d. Other algorithms independently solve eigenvalue problems. d1, d2, d3. SCSF algorithm utilizes Chebyshev subspace iterations to sequentially solve the eigenvalue problems. e. Assembly of eigenvalue pairs into a dataset. f. Amplification of the interval of interest through spectral transformation. g. Replacement of initial subspaces with previously solved invariant subspaces*

特征值数据集生成的核心瓶颈在于：对同一分布下的 $N$ 个算子，现有方法将每个矩阵的特征值问题视为独立任务，用传统数值求解器逐个求解，这部分计算占总体开销的 95% 以上。SCSF 的核心思想是将孤立的求解过程转化为一个受排序引导的串行求解过程，利用已收敛问题的特征对为后续问题提供高质量初始子空间，从而将昂贵的迭代收敛成本转化为廉价的继承与滤波。

整体框架由两个级联模块构成。

**模块一：截断 FFT 排序。** 输入为 $N$ 个待求解矩阵的参数矩阵集合 $\{P^{(i)}\}_{i=1}^N$。对每个 $P^{(i)}$ 执行快速傅里叶变换，截取仅包含低频成分的 $p_0\times p_0$ 子块。基于 Parseval 恒等式，参数矩阵在空间域的 Frobenius 距离等价于其在频域的 Frobenius 距离；而高频成分的能量占比普遍低于 5%，因此截断后的低频 Frobenius 距离能有效逼近算子间的谱相似度。在此基础上执行贪心排序，输出一个重排后的矩阵序列 $\{A^{(i)}\}$，使相邻问题间的谱分布尽可能接近。该模块的复杂度为 $\mathcal{O}(N^2 p_0^2 + N p^2 \log p)$，远低于直接在全参数矩阵上贪心排序的 $\mathcal{O}(N^2 p^2)$。

**模块二：切比雪夫滤波子空间迭代。** 接收排序后的矩阵序列，以串行方式依次求解特征值问题。对第 $i$ 个问题 $A^{(i)}$，将前一个问题已收敛的特征对 $(\Lambda^{(i-1)}, V^{(i-1)})$ 构造为初始子空间，替代传统方法中的随机初始化。随后利用前一问题谱区间 $[\alpha, \beta]$ 计算中心 $c$ 与半宽 $e$，构造切比雪夫多项式滤波器作用于当前矩阵，对目标谱区间进行放大。通过 Rayleigh-Ritz 过程细化特征对，并锁定收敛者。滤波操作占总计算时间超过 70%，是核心计算单元。初始子空间的热启动只对切比雪夫滤波框架有效，对 Eigsh、Krylov-Schur 等传统求解器无加速作用，甚至会使 Jacobi-Davidson 性能恶化。

**端到端数据流：** 参数集合 → 截断 FFT 排序 → 矩阵序列 → 串行 ChFSI（每个问题继承前一问题的特征对作为初始子空间）→ 所有矩阵的特征对集合 → 组装为数据集。该流程不改变指定精度下的求解结果，仅加速达到收敛的过程。

在多种算子上的实测表明，该框架相对最佳对比方法 ChFSI 可获 3.5 倍加速（Helmholtz，dim=6400，L=200），相对传统求解器 Eigsh 可达 4.8 倍加速。排序模块单独贡献 1.3–2.8 倍加速，使迭代次数降低 5–50%。



SCSF 将原本各自独立的特征值求解任务转化为一个顺序相关的加速过程，其核心由两个模块构成：**截断 FFT 排序（Truncated FFT Sorting）** 与**切比雪夫滤波子空间迭代（Chebyshev Filtered Subspace Iteration, ChFSI）**。前者通过频域近似度量算子间的谱相似性并重排求解顺序，后者在排序后的序列上串行求解，利用前一个问题的收敛特征对作为当前问题的高质量初始子空间，再配合切比雪夫滤波放大目标谱区间，从而大幅降低迭代收敛的冗余开销。

### 截断 FFT 排序

给定 $N$ 个算子的参数矩阵 $P^{(i)}\in\mathbb{R}^{p\times p}$，直接基于 Frobenius 范数 $\|P^{(i)}-P^{(j)}\|_F$ 进行贪心排序的复杂度高达 $\mathcal{O}(N^2 p^2)$。SCSF 利用 Parseval 恒等式将距离等价地分解到频率域：

$$
\| P^{(i)} - P^{(j)} \|_F^2 = \| \mathrm{FFT}(P^{(i)}) - \mathrm{FFT}(P^{(j)}) \|_F^2 = \text{SCSF Metric} + \epsilon_{ij},
$$

其中 **SCSF Metric** 仅取自前 $p_0\times p_0$ 的低频分量，$\epsilon_{ij}$ 为高频截断误差。实验表明高频成分占参数矩阵总能量的 $<5\%$（Table 20），因此低频近似能充分捕捉算子间的谱相似性。排序时先对所有 $P^{(i)}$ 执行二维 FFT 并截取 $p_0\times p_0$ 低频系数，再按低频 Frobenius 距离进行贪心排列（Algorithm 2）。整体排序复杂度降至

$$
\mathcal{O}\bigl(N^2 p_0^2 + N p^2 \log p\bigr),
$$

相比完全贪心排序在 $p_0\ll p$ 时带来数量级的加速（Table 4），且后续求解性能几乎不受影响（Table 5）。排序后相邻问题的谱分布相近，使热启动更具价值。

### 切比雪夫滤波子空间迭代

对排序后的矩阵序列 $A^{(1)},A^{(2)},\dots,A^{(N)}$，SCSF 串行求解特征值问题（Algorithm 3）。设前一个问题 $A^{(i-1)}$ 已收敛的特征对为 $(\Lambda^{(i-1)},V^{(i-1)})$，则以 $Y_0 = V^{(i-1)}$ 作为当前问题 $A^{(i)}$ 的初始迭代子空间。为使该子空间快速逼近 $A^{(i)}$ 的不变子空间，方法利用 **切比雪夫多项式** 放大感兴趣区间内的谱成分。

首先根据 $A^{(i-1)}$ 的谱分布估计当前问题的目标区间 $[\alpha,\beta]$，其中心与半宽定义为

$$
c = \frac{\alpha + \beta}{2}, \qquad e = \frac{\beta - \alpha}{2}.
$$

将该区间线性映射至 $[-1,1]$ 后，第一类切比雪夫多项式

$$
C_m(t) = \cos\!\bigl(m\cos^{-1}(t)\bigr),\quad |t|\le 1
$$

满足三项递推关系。对标量 $t$ 有

$$
C_{m+1}(t) = 2t\,C_m(t) - C_{m-1}(t),
$$

作用在初始子空间 $Y_0$ 上产生向量形式的递推：

$$
C_{m+1}(Y_0) = 2A\,C_m(Y_0) - C_{m-1}(Y_0),\qquad
C_m(Y_0) \equiv C_m(A)\,Y_0.
$$

$C_m(A)$ 在谱区间内快速增长，区间外保持有界，从而将原问题转化为一个增大目标特征成分、压缩非目标成分的滤波操作。滤波后的子空间经 Rayleigh‑Ritz 过程提取近似特征对，并锁定已收敛的向量，仅对剩余子空间继续迭代，直至满足预设精度（如相对残差 $<10^{-8}$）。

整个过程中，滤波操作占总计算时间的 $70\%$ 以上（Table 11），但对 $m$ 的选取不敏感（合理范围内 $m=12\sim 40$ 性能接近），保证开销受控。排序模块提供的强相关初始子空间使迭代次数减少 $5\%\sim 50\%$，总浮点操作降低 $7\%\sim 43\%$（Table 3），构成了 SCSF 整体加速的因果基础。



## 实验与关键发现

### 总体性能表现

SCSF 在所有测试数据集上均显著超越现有特征值求解器。在 Helmholtz 算子（dim=6400, L=200, tol=1e‑8）上，SCSF 的平均求解时间仅为 31.31 秒，相较最优对比方法 ChFSI（107.1 秒）实现 3.4× 加速，相较传统求解器 Eigsh（151.7 秒）可达 4.8× 加速（Table 1）。在更大规模的广义 Poisson 算子（dim=10000, L=400, tol=1e‑12）上，SCSF 进一步拉大差距：求解时间 158.49 秒，而 Eigsh 需 3162.28 秒（20× 加速），LOBPCG 需 2511.89 秒，KS 需 1995.26 秒，ChFSI 需 590.3 秒（3.7× 加速）（Table 10）。随着矩阵维度升高，SCSF 的优势愈加突出：在 dim ≤ 3600 时与 Eigsh 接近，dim > 5000 后明显优于所有对比算法（Figure 3）。


![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/004_Table_1.jpg]]
*Table 1: Comparison of average computation times (in seconds) for eigenvalue problems using various algorithms. The first row lists different algorithms, the first column details the datasets, including matrix dimensions and solution precisions (relative residual), and the second column shows the number of eigenvalues L computed for each matrix. The best algorithm is in bold. The symbol '–' denotes the result of a method that fails to converge under the given setting*

![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/014_Table_10.jpg]]
*Table 10: Comparison of different algorithm computation time (in seconds) for varying matrix dimensions using the generalized Poisson operator dataset. Results show average computation times for solving 400 eigenvalues with a precision of 1e-12*

SCSF 的加速效果对求解特征值个数 L 的敏感性较低。在二阶椭圆算子数据集上，当 L 从 200 升至 400 时，SCSF 相对于 KS 的加速比从 2.5× 提升至 5.5×，表明其计算时间随 L 增长温和，而传统方法代价陡增（Table 1 及相关文本）。

### 消融实验

#### 初始子空间的作用

SCSF 的核心加速机制来自将前一问题的收敛特征对作为当前问题的热启动子空间，但这一策略**仅对 Chebyshev 滤波子空间迭代（ChFSI）有效**。Table 2 的实验显示：对 ChFSI 替换初始子空间后，求解时间大幅下降；而对 Eigsh、KS 赋予同样热启动非但不能加速，甚至使 JD 性能恶化。这解释为何 SCSF 必须依赖 Chebyshev 滤波——只有该方法能够有效利用继承的子空间，通过滤波放大目标谱区间，将昂贵的随机初始收敛转化为廉价的子空间继承与滤波。


![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/006_Table_2.jpg]]

#### 排序模块的贡献

排序模块是 SCSF 的另一关键组件。在广义 Poisson 算子（dim=2500, tol=1e‑12）上，启用排序后 SCSF 求解时间减少 1.3–2.8×，迭代次数下降 5–50%，总浮点操作减少 7–43%（Table 3）。排序的作用源于截断 FFT 贪心策略：先将参数矩阵的低频成分（p₀×p₀，经验取 p₀=20）排序，使相邻问题的谱分布高度相关，从而让 ChFSI 的继承子空间成为高质量初值。


![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/007_Table_3.jpg]]
*Table 3: Performance comparison of SCSF with and without sorting. The first column lists the number of eigenvalues L computed, while subsequent columns display average computation times, average iteration counts, total Flop counts, and filter Flop counts. Experiments used the matrix dimension of 2500 and precision 1e-12 on the generalized Poisson operator dataset*

截断 FFT 排序本身的开销极低，且近似质量接近完全贪心排序。在 Helmholtz 数据集（dim=6400, N=10⁴）上，完全贪心排序需 592.7 秒，而截断 FFT 排序仅 151.1 秒（含 FFT 145.7 秒 + 贪心 0.1658 秒），且最终 SCSF 求解时间（400 特征值）仅差 0.6%（Table 4、Table 5）。低开销的根本在于高频分量能量占比极小：Appendix F 及 Table 20 显示，高频成分（频率 > p₀）在各类 PDE 参数矩阵中均不足总能量 5%，故只需低频 Frobenius 距离即可充分近似算子间的真实距离。


![[assets/figures/papers/iclr26_0005_rrbCQT7JKX_Accelerating_Eigenvalue_Dataset_Generation_via_C/figures/008_Table_4.jpg]]
*Table 4: Comparison of average computation times (in seconds) for different sorting algorithms, with the first column indicating dataset size. Experiments used the matrix dimension of 6400 on the Helmholtz dataset*

#### 参数敏感性

SCSF 对关键超参数不敏感。滤波多项式次数 m 在 12–40 范围内变动时，求解时间波动极小（Table 12）；截断阈值 p₀ 从 16 增大至 24 时性能平稳，默认值 20 已在绝大多数情况下达到最优（Table 14）。继承子空间的大小与待求特征值数 L 成比例，适度增加不会引起退化（Table 13）。

### 失败模式与局限性

SCSF 的加速效果与数据集的相似度强相关。当所有问题相同时（0% 扰动），SCSF 仅需 2 秒求解，而 Eigsh 需 151 秒；随着随机扰动增大，相似度下降，SCSF 的求解时间逐渐逼近 ChFSI 的无排序版本（Table 17）。因此，在问题间谱分布差异极大的场景下，SCSF 退化为普通 ChFSI，初始子空间无法提供帮助。

另外，初始子空间继承对非 Chebyshev 滤波类方法（Eigsh、KS、JD）无效甚至有害（Table 2），表明 SCSF 的加速能力**严格绑定于 Chebyshev 滤波框架**，无法直接迁移至其他求解器。

尽管存在上述边界，SCSF 仍表现出强鲁棒性。在混合算子数据集（同时包含 Helmholtz 和 Poisson 问题）上，即使算子类型不连续，SCSF 仍全面优于所有基线求解器（Table 18），未出现崩溃。但该点需人工验证：Table 18 的结果说明低频排序仍能捕捉到一部分跨类型的谱相似性，但若参数-算子映射完全间断，排序可能失效，该情形在未来工作中需进一步探索。

### 关键图表结论

- **Table 1**：主性能表，SCSF 在 4 类算子上全面领先，最佳情况下相较传统求解器加速 20× 以上，相较最强基线 ChFSI 加速 3.5×。该表确认了 SCSF 作为通用加速框架的有效性。
- **Table 2**：揭示了初始子空间修改与算法类型的强耦合：仅 ChFSI 受益，解释了 SCSF 为何必须选用 Chebyshev 滤波迭代。
- **Table 3**：量化排序模块收益，排除排序后性能大幅下降，证实排序是 SCSF 不可或缺的组件。
- **Table 4/5**：截断 FFT 排序以微小精度代价将排序开销降低两个数量级以上，使 SCSF 能处理大规模数据集。
- **Table 10 与 Figure 3**：表明 SCSF 在大维度、多特征值场景下优势不断扩大，具有良性的计算复杂度增长特性。
- **Table 11**：SCSF 各阶段耗时分解证实滤波操作占总时间 70% 以上，与理论分析一致，为未来优化指明方向（如并行化滤波）。
- **Table 17**：SCSF 加速与相似度的单调关系，为实际应用中的数据集构建策略提供参考——应尽可能通过排序增强相邻问题谱相关性。

综上，实验系统的消融与对比证实 SCSF 的加速源于排序与 Chebyshev 滤波的协同：排序创造相似序列，滤波利用继承子空间放大目标谱区间，将大量独立求解开销转化为一次性继承与廉价滤波。该方法在所有测试条件下均保持数值精度不变（Table 15），是一种安全、高效的特征值数据生成加速方案。



## 定位与知识库关联

SCSF 直接承接并改造了批量特征值问题中两类本无关联的工作范式——传统独立求解策略与同分布算子间隐含的低频相似性。传统求解器（Eigsh、LOBPCG、Krylov‑Schur、Jacobi‑Davidson）以及切比雪夫滤波子空间迭代 ChFSI 均将每个特征值问题视为完全独立的计算任务：Eigsh 依赖 ARPACK 的 shift‑invert 模式，LOBPCG 利用块预条件共轭梯度，KS 和 JD 分别以谱变换 Krylov 和校正方程构建子空间，而 ChFSI 虽实现了高效的切比雪夫滤波，却仍采用随机初始子空间独立求解。这些方法完全忽略了同一分布下算子谱分布与不变子空间的接近性，致使每次求解都从零开始迭代，成为数据集生成中占比超过 95% 的瓶颈。

SCSF 通过引入两个相互咬合的模块从根本上改变了求解序列：**截断 FFT 贪心排序**和**携带热启动的 Chebyshev 滤波子空间迭代**。排序模块将一批 N 个特征值问题重新组织成谱相似性最大化的序列，使得相邻问题之间的特征对具有强继承价值；随后的串行求解器不再使用随机初始子空间，而是将前一问题已收敛的特征向量作为当前问题的高质量初始子空间，再经由 Chebyshev 滤波放大目标谱区、Rayleigh‑Ritz 过程细化并锁定收敛对。这种"继承‑滤波"机制将昂贵的迭代收敛转化为廉价的子空间移植与滤波操作，证实了排序与热启动对 ChFSI 类型求解器的唯一适配性（表 2：将前一问题特征对作为初始子空间仅对 ChFSI 有效，对 Eigsh/KS 无效，甚至使 JD 恶化）。

在性能谱系中，SCSF 相对于最强的纯数值基线 ChFSI 在典型 PDE 数据集上获得 **1.3× 到 3.5×** 的求解时间加速（Helmholtz 算子 dim=6400，L=200），相比 Eigsh 加速达 **4.8×**；在大尺度问题（广义 Poisson 算子 dim=10000，L=400）上提升至 **20×** 量级。消融实验将加速归因于排序与热启动的协同：仅排序就能减少 1.3–2.8× 求解时间，迭代次数降低 5–50%，浮点操作减少 7–43%（表 3）；热启动的效果高度依赖于排序带来的子空间相似度，随数据集不一致性增加，SCSF 的加速逐步收敛到 ChFSI 的基线（表 17）。

截断 FFT 排序本身在计算复杂度上显著优于直接 Frobenius 范数贪心排序（N=10⁴ 时排序开销从 592.7 s 降至 0.1658 s），且最终求解性能几乎无损，其理论基础来源于 Parseval 恒等式的频域分解：算子 Frobenius 距离可严格表示为 SCSF 的低频度规与高频截断误差之和，而所有测试的 PDE 族中高频分量能量占比均小于 5%，保证了低频近似可以充分捕获算子差异（表 20）。即使在不连续的混合数据集（Helmholtz + Poisson）上，SCSF 仍优于所有传统求解器，表现出对参数‑算子映射断层的鲁棒性（表 18）。

### 适用边界

SCSF 当前建立在以下前提之上，直接决定了其适用范围：
- **算子类型**：仅针对自伴（Hermitian）线性算子进行了验证，未能覆盖非 Hermitian 及非线性特征值问题。
- **相似性传递机制**：加速依赖于参数矩阵的低频特征能有效代理算子间的谱距离。当算子参数化出现剧烈非平滑映射（例如参数矩阵中存在本质不连续的高频结构）时，截断 FFT 排序引入的近似误差可能破坏相邻问题间的不变子空间继承关系，导致加速退化至无序 ChFSI 水平。
- **求解器耦合**：热启动仅对 Chebyshev 滤波子空间迭代有效，因此 SCSF 的加速无法直接移植到其他迭代框架（如 Eigsh 或 JD），其设计深度绑定于多项式滤波对初始子空间的敏感性和放大机制。
- **精度与硬件**：SCSF 本身不改变指定精度下的特征对结果，可视为纯加速层，与并行计算架构正交互补。

### 局限与开放问题

SCSF 的工作揭示了算子相似性驱动加速的可行路径，但也暴露出若干结构性局限，成为未来研究的自然入口：

1. **算子类型的拓展**  
   当前框架依赖自伴性以确保切比雪夫滤波器的实区间放大性质，对非 Hermitian 算子需要构建复平面谱变换和对应的滤波策略。更广泛的非线性特征值问题（如多项式或延迟特征值问题）如何处理相似性传递仍属空白。

2. **相似性度量与排序策略**  
   截断 FFT 排序以参数矩阵低频 Frobenius 距离作为唯一度规，本质上是一种与算子空间无关的代理度量。当参数矩阵与算子谱分布之间的映射高度非光滑时，低频成分可能无法可靠反映谱相似性。**需要探索直接基于算子离散矩阵的低秩结构、Krylov 子空间轮廓或特征值统计量的问题相关度量**，以支撑更鲁棒的排序。

3. **不连续数据集的处理**  
   实验显示 SCSF 在混合算子类型上仍具优势，但速度增益部分依赖于排序能否将同类算子聚集。对于缺乏任何平滑结构的混杂参数集合，现有排序方法退化为随机顺序，使得加速完全来自热启动。**如何在这种极端情况下自动识别并构建可继承的子序列（例如聚类引导的分段求解）**是一个开放问题。

4. **理论基础的精化**  
   虽然频域截断提供了误差的渐近衰减界，但对于排序和热启动的联合收敛性的定量分析，尤其是排序扰动如何通过初始子空间传播并影响滤波迭代收敛速率，尚缺乏严格理论支持。

上述方向不仅指向 SCSF 自身的深化，也为"利用算子结构加速科学计算数据生成"这类更一般的问题提供了研究线索。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerating_Eigenvalue_Dataset_Generation_via_Chebyshev_Subspace_Filter.pdf

![[paperPDFs/ICLR_2026/Accelerating_Eigenvalue_Dataset_Generation_via_Chebyshev_Subspace_Filter.pdf]]
