---
title: Conditional Mixture Path Guiding for Differentiable Rendering
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Conditional_Mixture_Path_Guiding_for_Differentiable_Rendering.pdf
project_link: null
code_link: "https://github.com/Cchen-77/bounded-gpis"
aliases:
- BRMSBI
- CMPGDR
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入分层伯努利冲激（SBI）及其可预计算的二进制序列界限，设计点级界限以快速排除非交点，并在区域级通过均值和方差界限剔除低概率区域，从而大幅减少全噪声评估次数。
primary_logic: 在射线步进中，一个保守的、可廉价计算的界限足以保证非交点，而无需精确但昂贵的全噪声评估。分层伯努利冲激的二进制分类特性使得界限可预计算并快速查表。
claims:
- 全噪声评估减少高达97.4%
- 渲染时间对比：Dragon场景从31.33s降至2.28s (1 spp)
- 点级界限和区域级界限各自均能显著提速，两者结合效果更佳（尤其在N=30时）
- Dragon 上 Rendering Time (s) per sample = 2.28
---

# Conditional Mixture Path Guiding for Differentiable Rendering

> [!tip] 核心洞察
> 在射线步进中，一个保守的、可廉价计算的界限足以保证非交点，而无需精确但昂贵的全噪声评估。分层伯努利冲激的二进制分类特性使得界限可预计算并快速查表。

| 字段 | 内容 |
|------|------|
| 中文题名 | 用于射线步进高斯过程隐式曲面的分层伯努利冲激界限 |
| 英文题名 | Conditional Mixture Path Guiding for Differentiable Rendering |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://zhiminfan.work/) · [Code](https://github.com/Cchen-77/bounded-gpis) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Bounded Ray Marching with Stratified Bernoulli Impulses |
| Dataset | Dragon, Lion, Cloud |

> [!tip] 效果简介
> - Dragon 上，Rendering Time (s) per sample 2.28 vs 31.33 (Xu et al. 2025) (13.7x speedup)。
> - Lion 上，Rendering Time (s) 4.64 vs 29.73 (Xu et al. 2025) (6.4x speedup)。
> - Cloud 上，Rendering Time (s) 5.68 vs 28.43 (Xu et al. 2025) (5.0x speedup)。

## 概要

在基于高斯过程隐式曲面（GPIS）的渲染中，光线与隐式曲面的交点求解需沿射线进行密集步进，每一步进点均须评估稀疏卷积噪声以判定零交叉。该全噪声评估成本极高，构成渲染效率的核心瓶颈。本文提出**分层伯努利冲激（Stratified Bernoulli Impulses, SBI）**，将冲激权重限定为二值，使每条射线上的噪声实现可依据冲激权重的二进制序列进行分类。基于此，作者推导出**点级下界**：利用二进制序列预计算边界映射表，在步进时以廉价查表快速计算保守下界，仅当下界指示可能存在交点时才触发昂贵的全噪声评估。进一步，利用均值与方差构建**区域级概率界限**，结合均值引导的稀疏体素八叉树（MGSVO）剔除概率空区域，形成两级裁剪机制。

实验表明，该方法在Dragon场景下将全噪声评估减少高达97.4%，渲染时间从Xu et al.（2025）的31.33秒降至2.28秒（1 spp），实现13.7倍加速；等时渲染下视觉质量显著优于函数空间方法（Seyb et al., 2024）及一维稀疏卷积基线。消融实验证实，加速主要源于界限机制而非冲激类型替换，点级与区域级界限各自均能大幅提速，联合使用效果更优。该方法以极小内存开销和可忽略的偏差，为GPIS的高效渲染提供了一条实用路径。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

在基于高斯过程隐式曲面（GPIS）的渲染中，光线与隐式曲面的交点求解是计算瓶颈的核心。传统方法沿射线进行密集步进（ray marching），每个步进点都需要评估完整的稀疏卷积噪声 $\psi(\mathbf{x}) = \sum_i w_i h(\mathbf{x}, \mathbf{q}_i)$，导致大量全噪声评估成为渲染效率的主要障碍。

本文的核心洞察在于：在射线步进中，一个保守的、可廉价计算的界限足以保证非交点，而无需精确但昂贵的全噪声评估。基于这一洞察，作者提出了一套双层界限机制——点级界限（point-level bound）与区域级界限（region-level bound）——来大幅减少全噪声评估次数，从而显著加速渲染。

### 关键创新点一：分层伯努利冲激（Stratified Bernoulli Impulses, SBI）

传统1D稀疏卷积噪声使用高斯冲激（Gaussian impulses），其权重从高斯分布采样，导致每个实现（realization）的冲激权重不可预知，难以构建统一的界限查找表。

本文提出的分层伯努利冲激（SBI）将冲激权重限制为仅两个可能值：$+1/\sqrt{\lambda}$ 或 $-1/\sqrt{\lambda}$，并在每个单元（cell）内以分层方式放置冲激。这一设计的核心优势在于：

1. **二进制分类特性**：每个冲激的权重仅由对应的伯努利随机变量决定，使得整个噪声实现可由一个二进制序列 $\mathbf{s}$ 唯一表征。
2. **可预计算性**：由于权重取值有限，可以针对所有可能的二进制序列预计算界限查找表（bound map），在运行时通过查表快速获得保守的下界估计。
3. **统计性质保持**：尽管SBI的Cramér–von Mises统计量略高于高斯冲激（Figure 5），但在实际渲染中，即使每单元冲激数 $N=10$ 的低密度设置下，SBI与高斯冲激的渲染结果在视觉上不可区分（Figure 6），验证了该近似在渲染任务中的充分性。

### 关键创新点二：点级界限（Point-Level Bound）

点级界限的目标是对每个步进点 $\mathbf{p}$ 快速计算稀疏卷积噪声的下界 $\underline{\psi}(\mathbf{p})$。若下界大于零，则该点不可能位于零水平集上，可直接跳过全噪声评估。

界限构建分为三个层次：

**冲激级下界**：对每个冲激 $i$，利用卷积核 $h$ 随距离单调递减的性质，计算其最小可能贡献：
$$\underline{\psi_i}(\mathbf{p}) = w_i h_{\mathbf{p}}(d_i)$$
其中 $d_i$ 为冲激到步进点的最小可能距离。对于SBI，$d_i$ 可预计算为仅依赖冲激索引 $i$ 与步进点所在子单元索引 $i_p$ 之差的函数：
$$d_i = \begin{cases} \max(0, (|i - i_p| - 1)c), & w_i < 0 \\ (|i - i_p| + 1)c, & w_i \geq 0 \end{cases}$$
这一公式利用了SBI的分层放置特性：冲激被限制在其所属子单元内，因此与步进点的距离存在确定的下界。

**界限映射预计算**：由于SBI权重仅由二进制序列决定，可对所有可能的长度为 $N$ 的二进制序列预计算基础界限映射：
$$B(\mathbf{s}) = \frac{1}{\sqrt{\lambda}} \sum_{j=1}^N \begin{cases} -h((j-1)c), & \mathbf{s}_j=0 \\ h((j+1)c), & \mathbf{s}_j=1 \end{cases}$$

**点级下界评估**：在运行时，将步进点所在子单元内的冲激单独处理，而将其左右两侧的冲激序列分别查表求和：
$$\underline{\psi}(\mathbf{p}) = w_0 h(\|\mathbf{p} - \mathbf{q}_0\|) + B(\mathrm{rev}(\mathbf{s}^\mathrm{L})) + B(\mathbf{s}^\mathrm{R})$$
其中 $\mathbf{s}^\mathrm{L}$ 和 $\mathbf{s}^\mathrm{R}$ 分别为步进点左右两侧冲激的二进制序列。这一设计使得点级界限的计算复杂度从 $O(N)$ 降至 $O(1)$ 查表操作。

### 关键创新点三：区域级界限与MGSVO

区域级界限在空间维度上进行更粗粒度的裁剪。其核心思想是：利用高斯过程的均值和方差信息，识别并剔除概率上不可能包含表面的空间区域。

**三西格玛准则**：对于空间体素 $V$ 内的任意点 $\mathbf{x}$，其实现值 $\psi(\mathbf{x})$ 以近似100%的概率落在区间内：
$$\mu(V) - 3\bar{\sigma}(V) \leq \psi(\mathbf{x}) \leq \bar{\mu}(V) + 3\bar{\sigma}(V)$$
若该区间的下界大于零，则整个体素可被安全剔除。

**均值引导的稀疏体素八叉树（MGSVO）**：为高效管理和遍历保留区域，本文构建了MGSVO空间加速结构。该结构以均值函数为引导，仅在均值接近零的区域进行细分，从而避免在显然不可能包含表面的区域浪费存储和遍历开销。

### 管线模块与因果关系

整体有界射线步进管线（Figure 7）由以下模块串联构成：

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/009_Figure_7.jpg]]
*Figure 7: An overview of bounded ray marching. For clarity, we assume the ray originates outside the surface, where the realization value is positive, and omit the path-wise updating term*

1. **SBI生成**：为每条射线的每个单元生成分层伯努利冲激，确定其二进制序列。
2. **区域级裁剪（MGSVO遍历）**：射线穿越MGSVO，仅在与非空体素相交的区段进行步进，跳过概率空区域。
3. **点级界限评估**：对保留区段内的每个步进点，通过查表快速计算 $\underline{\psi}(\mathbf{p})$。若 $\underline{\psi}(\mathbf{p}) > 0$，跳过全噪声评估；否则执行完整的稀疏卷积噪声计算。
4. **路径条件化**：使用Renewal+记忆模型沿路径进行条件化更新，确保噪声实现的空间一致性。

模块间的因果关系清晰：SBI的二进制分类特性使得界限可预计算并快速查表（因），从而点级界限能以 $O(1)$ 成本排除大部分非交点（果）。区域级界限通过空间加速结构在更粗粒度上剔除低概率区域（因），减少了需要点级界限处理的步进点总数（果）。两层界限协同作用，实现了全噪声评估减少高达97.4%的效果。

### 非稳态核的扩展

对于非稳态协方差核，本文通过核分解策略将界限框架进行扩展：
$$h(\mathbf{x}, \mathbf{y}; \boldsymbol{\theta}(\mathbf{x})) = N(\boldsymbol{\theta}(\mathbf{x})) \hat{h}(\mathbf{x}, \mathbf{y}; \boldsymbol{\theta}(\mathbf{x}))$$
将核分解为标量部分 $N(\boldsymbol{\theta}(\mathbf{x}))$ 和无标度部分 $\hat{h}$，使得界限映射可在参数空间离散化后预计算。这要求非稳态参数 $\boldsymbol{\theta}(\mathbf{x})$ 在空间上具有单调性，以保证界限的保守性。

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/011_Figure_8.jpg]]
*Figure 8: Illustration of the construction of the impulse-level bound. In each subfigure, five subcells are arranged from left to right. The red point indicates the marching points, and*

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/012_Figure_10.jpg]]
*Figure 10: Illustration of the point-level bound. We use a squared-exponential kernel with a length scale of 0.1 and an amplitude of 0.1, along with a normalization factor, resulting in a Gaussian process with a standard deviation of 0.1. We set the impulses-per-cell*

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/014_Figure_13.jpg]]
*Figure 13: 2D illustration of ray marching with MGSVO. For clarity, we omit the hierarchy traversal process and show only the finest level of the MGSVO*

## 实验与关键发现

### 核心性能增益

本文方法在渲染效率上取得了数量级的提升。**Table 3** 报告了在 1 spp 下的渲染时间对比：在 Dragon 场景中，本文方法仅需 **2.28 s**，而 Xu et al. (2025) 的 1D 稀疏卷积方法需 **31.33 s**，加速达 **13.7 倍**；Lion 场景从 29.73 s 降至 4.64 s（**6.4 倍**）；Cloud 场景从 28.43 s 降至 5.68 s（**5.0 倍**）。这一加速的核心机制是全噪声评估次数的大幅削减——文中报告全噪声评估减少**高达 97.4%**（Section 1）。

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/018_Table_3.jpg]]
*Table 3: Rendering statistics. We count the marching points that perform full noise evaluations or are skipped by the point-level bound. We estimate runtime percentages relative to the total overall runtime for (1) ray–surface intersections, which subsume (2) full noise evaluations, (3) point-level (PL) bound evaluations, and (4) mean function evaluations. We also report the memory usage of the bound map and MGSVO. All statistics were collected at 1 spp*

**等时渲染对比**（Fig. 14, 10 分钟）进一步验证了效率优势：在相同时间预算下，本文方法可获得远高于基线方法的 spp，视觉质量（以 MSE 计）显著优于函数空间方法（Seyb et al., 2024）和 1D 稀疏卷积方法（Xu et al., 2025），semblance 提升最高达 **14.8 倍**。

### 界限机制的贡献分解

消融实验揭示了加速效果的真正来源。

**冲激类型替换的边际效应**：Fig. 16 表明，仅将高斯冲激替换为 SBI 而不使用任何界限机制，性能提升微乎其微。这一微弱增益仅源于伯努利变量采样比高斯采样略低的计算成本。加速的核心并非冲激类型本身，而是 SBI 的二进制分类特性所支撑的界限机制。

**点级界限与区域级界限的独立与协同贡献**：Fig. 17 展示了在 Dragon 场景上的消融对比（等时 10 分钟）：
- **仅区域级界限**：单独使用已能实现大幅提速，因为它能在射线步进早期快速剔除概率空区域。
- **仅点级界限**：同样提供显著加速，通过预计算的 bound map 查表快速跳过非交点步进点。
- **两者结合**：在 N=30（每单元 30 个冲激）时提升更为显著，说明高冲激密度下点级界限的查表开销被更精确的非交点判定所抵消，而区域级界限则从粗粒度层面减少了需要点级判定的步进点总数。

**运行时剖析**：Fig. 18 的堆叠柱状图对比了 Dragon 场景在 N=10 和 N=30 下各方法的运行时分解。完整有界射线步进（full bounded ray marching）将大部分时间从全噪声评估转移到了廉价的点级界限评估和均值函数评估上，全噪声评估占射线-曲面求交时间的比例大幅下降（Table 3）。

### 冲激密度的影响

Fig. 15 展示了不同每单元冲激数 N（10, 20, 30, 40）下的等时渲染对比。随着 N 增大：
- 1D 稀疏卷积方法的渲染质量提升，但计算成本线性增长。
- 本文方法在所有 N 设置下均优于基线，且在高 N 下优势更为突出——因为更多的冲激意味着更密集的步进点，界限跳过机制节省的绝对计算量更大。

### 协方差与场景参数的边界条件

**方差增大的退化**：Fig. 20 和 Table 4 揭示了方法的关键边界条件。当场景（协）方差增大时：
- 概率空区域缩小，区域级界限可剔除的体素减少。
- 点级界限的跳过比例也随之下降。
- 整体加速效果减弱。

Table 4 统计了不同协方差场景下步进点的分类：随着方差增大，被区域级界限剔除（RL pruned）和被点级界限跳过（PL skipped）的步进点比例均下降，全噪声评估比例上升，渲染时间相应增加。

**极低方差下的对比**：当协方差极小时，GPIS 表面趋近于确定性隐式曲面。Fig. 20(b) 将本文方法与传统的基于网格的路径追踪进行了对比，表明在该极端情况下本文方法仍具竞争力，但优势缩小。

**解耦 vs. 耦合的区域级界限**：文中还分析了非稳态核下区域级界限的解耦策略（disentangled）相比耦合策略（entangled）进一步提升了性能（Section “Impact of covariance”），因为解耦后均值和方差的界限更紧凑，可剔除更多空区域。

### 偏差与正确性验证

**高采样数下的偏差检验**：Fig. 21 在 2048 spp 下对比了完整方法与其去除区域级界限的变体，两者渲染结果视觉上不可区分，差异图的 L2 范数极小。这表明区域级界限基于三西格玛概率准则（Eq. 17）引入的潜在偏差在实际渲染中可忽略不计。

**SBI 的正态性收敛**：Fig. 4 和 Fig. 5 验证了 SBI 的 1D 稀疏卷积噪声随 N 增大快速收敛于目标高斯分布。尽管在低冲激密度下 SBI 的 Cramér–von Mises 统计量高于高斯冲激，但 Fig. 6 的渲染对比表明，即使 N=10 时，SBI 与高斯冲激的渲染结果在视觉上仍不可区分（差异图 L2 范数极小）。这为 SBI 替代高斯冲激提供了实证支撑。

### 内存与预计算开销

Table 3 报告了 bound map 和 MGSVO 的内存占用。Bound map 的大小取决于二进制序列长度 N，而 MGSVO 的内存则与场景的空间范围和体素分辨率相关。Table 4 补充了不同协方差场景下 MGSVO 的内存变化。这些开销在文中有完整统计，不会隐藏于加速比之后。

### 多对象重叠场景

Fig. 19 展示了两个重叠 GPIS 场景的等时渲染对比，表明本文方法在复合场景中同样有效。但文中也指出（limitations），当大量对象重叠时，各对象独立界定的低概率空区域可能累积出不可忽略的总体占用概率，当前逐对象独立界定策略可能遗漏此类区域，这是方法的已知边界。

![[assets/figures/papers/paper_list_l44_https_zhiminfan_work/figures/006_Figure_4.jpg]]
*Figure 4: Evaluating the Gaussianity of a 1D sparse convolution noise with SBIs. We employ a stationary squared-exponential kernel with a length scale of 0.1. We visualize the normalized 1-point distribution (top row) and the 2-point joint distribution (bottom row). As the number of impulses-per-cell ?? increases, it rapidly converges toward a Gaussian shape*

## 定位与知识库关联

本文的核心贡献在于**渲染管线中“噪声评估”这一slot的彻底重构**：在基于高斯过程隐式曲面（GPIS）的射线步进渲染中，将昂贵的高维高斯采样或全噪声评估替换为“廉价界限预检 + 按需全评估”的复合机制。这一改变不触及GPIS的数学定义、协方差函数形式或光线传输框架本身，而是针对**射线–曲面求交的运行时效率瓶颈**进行外科手术式优化。

### 相对于已有方法的本质差异

与两个直接基线方法相比，本文改变的slot明确且可分离：

- **相对于函数空间射线步进**（Seyb et al., ACM Trans. Graph. 2024）：该基线在每次射线步进迭代中通过多元高斯采样获得沿射线的实现值，计算复杂度为 $O(n^3)$。本文继承了一维稀疏卷积噪声的加速思路，但进一步将噪声评估从“每次步进必做”变为“先查界限表，仅当界限提示可能存在交点时才做全评估”。这是**评估策略**层面的改变，而非噪声模型的替代。

- **相对于一维稀疏卷积方法**（Xu et al., ACM Trans. Graph. 2025）：该基线已使用一维稀疏卷积噪声替代多元高斯采样，大幅降低了单次评估成本，但**仍对每个步进点执行全噪声评估**。本文在该基线之上插入两个层次的界限机制：**点级界限**利用本文提出的分层伯努利冲激（SBI）的二进制权重特性，通过预计算的界限映射表实现 $O(1)$ 查表判定；**区域级界限**通过均值引导的稀疏体素八叉树（MGSVO）在空间上剔除概率空区域。消融实验（Figure 17）明确表明：仅将高斯冲激替换为SBI而不使用界限，加速效果微乎其微；真正的性能增益来自界限机制本身。

因此，本文在知识库中的定位是：**在“GPIS渲染的噪声评估”这一slot上，将“全评估”范式改为“界限预检–按需评估”范式**，且这一改变依赖于将冲激类型从高斯冲激改为分层伯努利冲激（SBI）这一使能技术。

### 知识库挂载点与后续启发

**挂载点1：隐式曲面渲染的加速结构**
本文的区域级界限（MGSVO）与经典隐式曲面渲染中的空间加速结构（如球体追踪中的距离场下界）在思路上同源，但针对的是**随机隐式曲面**这一特殊场景。MGSVO基于均值和方差的三西格玛准则判定体素是否“概率空”，这与Seyb et al. (2024) 中基于概率下界的空区域剔除一脉相承，但本文通过解耦均值和方差贡献（disentangled bound）进一步提升了剔除效率。这一设计可启发其他需要处理随机几何的渲染任务（如神经辐射场的几何不确定性量化）。

**挂载点2：二进制序列驱动的预计算界限**
点级界限的核心洞察是：SBI的权重仅有 $+1/\sqrt{\lambda}$ 和 $-1/\sqrt{\lambda}$ 两种取值，因此每个射线单元的冲激配置可由一个长度为 $N$ 的二进制序列完全描述。这允许将下界预计算为 $2^N$ 大小的查找表，在运行时仅需根据当前步进点所处的子单元位置索引查表。这种“用离散化换取预计算”的策略与计算机图形学中基于量化的加速技术（如预计算辐射传输中的球谐系数表）属于同一方法论家族，可迁移至其他具有离散状态空间的随机过程渲染问题。

**挂载点3：非稳态协方差的处理**
本文将界限推导扩展至非稳态协方差核（Section 6.3），通过将核分解为标量部分和无标度部分，使得界限映射可在参数空间离散化后预计算。这为处理空间变化的材质或几何不确定性提供了模板，但代价是增加了查找表的维度和内存占用（Table 3, Table 4）。这一扩展路径可启发后续工作探索更灵活的核分解策略或自适应离散化方案。

### 适用边界与限制

本文方法的适用边界由以下硬约束界定：

1. **核函数限制**：点级界限的推导依赖卷积核的对称性和随距离单调递减性质，非稳态核还需参数单调性（Section 6.3）。这排除了不满足这些条件的通用核函数。一维稀疏卷积噪声本身要求协方差函数具有解析的卷积核，进一步缩小了适用范围。

2. **方差敏感性**：当场景协方差较大或均值函数接近零时，概率空区域缩小，区域级界限的剔除比例下降，加速效果减弱（Figure 20, Table 4）。在极限情况下（极低方差），方法退化为接近传统网格路径追踪的性能。

3. **多对象重叠**：当前逐对象独立构建MGSVO的策略，在面对大量对象重叠时，各对象低概率空区域的累积效应可能导致不可忽略的总体占用概率，区域级界限可能遗漏本应保留的区域。这是一个未被实验覆盖的理论风险点，需在实际应用中谨慎验证。

4. **概率性而非确定性**：区域级界限基于三西格玛概率准则，并非确定性保证。尽管高采样数下的偏差分析（Figure 21, 2048 spp）未显示可见偏差，但在极端参数配置下理论上可能遗漏交点。

### 后续研究价值

本文开创的“界限预检–按需评估”范式为随机几何渲染的效率优化提供了可复用的方法论框架。三个直接可跟进的方向包括：放宽核函数假设以扩展适用范围；利用SBI权重预计算Lipschitz界限以实现自适应步长；以及处理多对象重叠场景下的联合概率空区域判定。此外，SBI作为一种新型冲激类型，其在其他需要稀疏卷积噪声近似高斯过程的场景（如物理仿真中的随机场采样）中的适用性也值得探索。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Conditional_Mixture_Path_Guiding_for_Differentiable_Rendering.pdf]]