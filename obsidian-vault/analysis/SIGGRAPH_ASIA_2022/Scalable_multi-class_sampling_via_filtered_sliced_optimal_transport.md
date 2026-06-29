---
title: Scalable multi-class sampling via filtered sliced optimal transport
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Scalable_multi_class_sampling_via_filtered_sliced_optimal_transport.pdf
project_link: null
code_link: null
aliases:
- FSOTF
- SMCSFSOT
tags:
- SIGGRAPH_ASIA_2022
- topic/other_unclear
core_operator: 将多个优化目标编码为类别函数和过滤操作，构建连续Wasserstein重心，并通过随机子类采样的随机梯度下降进行优化，从而将每步计算与目标总数解耦。
primary_logic: 在扩展空间中用类别函数定义子类，将多目标采样转化为一个连续Wasserstein重心问题；采用切片Wasserstein距离和随机子类抽样，能够高效处理成百上千个并发优化目标，且内存占用几乎不随目标数增长。
claims:
- 提出基于连续Wasserstein重心的多类别优化公式
- 优化方案对目标数量仅弱敏感，可处理大量类别
- 随机梯度下降每迭代仅优化一个子类，内存占用可忽略
- 在3类采样中达到与Qin等人相似质量且速度大幅提升（GPU 38秒 vs CPU 1小时）
---

# Scalable multi-class sampling via filtered sliced optimal transport

> [!tip] 核心洞察
> 在扩展空间中用类别函数定义子类，将多目标采样转化为一个连续Wasserstein重心问题；采用切片Wasserstein距离和随机子类抽样，能够高效处理成百上千个并发优化目标，且内存占用几乎不随目标数增长。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于过滤切片最优传输的可扩展多类别采样 |
| 英文题名 | Scalable multi-class sampling via filtered sliced optimal transport |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](http://www.iliyan.com/publications/ScalableMultiClassSampling) |
| Topic | #topic/other_unclear |
| Method | Filtered Sliced Optimal Transport (FSOT) |
| Dataset | 3-class blue-noise sampling, 2D uniform blue-noise sampling, Progressive Monte Carlo integration, Perceptual error distribution |

> [!tip] 效果简介
> - 3-class blue-noise sampling (red, blue, union) 上，视觉质量 / 功率谱径向均值 FSOT (GPU, 38秒) vs Qin et al. 2017 (CPU, ~1小时) (相似质量，速度提升约100倍)。
> - 2D uniform blue-noise sampling (1024 points) 上，各向同性 / 功率谱对齐程度 FSOT with offset correction vs Paulin et al. 2020 (unit square direct) (消除条带对齐，提高各向同性)。
> - Progressive Monte Carlo integration 上，积分误差收敛 FSOT progressive (staircase class, axis-aligned prioritization) vs Paulin et al. 2020 (更低的积分误差，渐进式版本误差行为均匀)。

## 概要

多类别采样需要为同一组采样点中的多个子集分别定义优化目标，现有方法（如基于熵正则化最优传输的 Qin et al. 2017）需逐一指定每个目标，且计算与内存开销随目标数量快速增长，难以扩展到成百上千个并发优化目标。本文提出**过滤切片最优传输（FSOT）**框架，核心思路是将多个优化目标统一编码为扩展维度上的类别函数与过滤操作，将多类别采样转化为一个**连续 Wasserstein 重心问题**，并采用**随机子类抽样的切片 Wasserstein 梯度下降**进行优化，使每一步的计算与内存开销与目标总数解耦。在 3 类蓝噪声采样中，FSOT 在 GPU 上仅需 38 秒即可达到与 Qin et al. 方法（CPU 约 1 小时）相当的质量；在 CMYK 彩色点画、物体放置和感知误差优化等应用中，可同时处理 15 至 4096 个优化目标。该方法将多类别采样从逐目标离散指定的范式转变为连续重心优化的统一范式，其可扩展性瓶颈从目标数量转移到目标分布的可采样性。

## 核心方法与创新机理

### 问题瓶颈与核心思路

多类别采样（multi-class sampling）要求从同一个点集中抽取多个子集，每个子集满足各自的优化目标（如蓝噪声分布、非均匀密度等）。现有方法的根本瓶颈在于：**优化目标必须逐一显式指定，且优化过程的计算与存储开销随目标数量迅速增长**。例如，Qin等人（2017）基于熵正则化Wasserstein重心的方案，在目标类别数较多时，Sinkhorn算法的内存与计算量使其不可行。这一瓶颈限制了多类别采样向数十、数百乃至数千个并发目标的扩展。

本文的核心洞察是：**将多个优化目标统一编码为类别函数（class function）和过滤操作，在扩展空间中构建连续Wasserstein重心（continuous Wasserstein barycenter），并通过随机子类采样的随机梯度下降进行优化**。这一设计使得每步迭代的计算量仅与当前采样的单个子类相关，与目标总数解耦，从而实现了对目标数量的弱敏感性。

### 方法框架总览

整个方法由四个关键模块串联构成，形成从问题定义到高效优化的完整链路：

1. **扩展点集构建**：为每个采样点分配固定的类别坐标，将优化空间从 $\mathcal{X}$ 扩展为 $\mathcal{C} \times \mathcal{X}$。
2. **类别与目标定义**：通过类别函数 $w_t: \mathcal{C} \to [0,1]$ 和目标分布 $\mu_t$ 编码所有优化目标及其相对权重。
3. **连续Wasserstein重心公式**：将多目标采样转化为一个统一的积分形式优化问题，自动涵盖所有子类。
4. **随机梯度下降优化**：每次迭代随机选取一个子类，通过切片Wasserstein距离的一维投影梯度进行更新，实现与目标数解耦的高效优化。

### 关键创新机制

#### 创新点一：类别函数与过滤操作（Changed Slot: 优化目标定义）

传统方法需为每个子集单独指定目标分布，并使用交互矩阵或熵正则化项来协调子集间关系。本文提出用**类别函数** $w$ 统一编码一个类别内的全部优化目标：类别定义为一个对 $(w, \mu)$，其中 $w: \mathcal{C} \to [0,1]$ 是定义在分类维度上的函数，$\mu$ 是目标分布。

具体而言，首先为点集 $\{x_i\}_{i=1}^n$ 的每个点分配一个固定的类别坐标 $c_i \in \mathcal{C}$（通常取归一化索引 $i/n$），形成扩展点 $\bar{x}_i = (c_i, x_i)$。类别函数 $w$ 在 $\mathcal{C}$ 上的取值决定了不同阈值 $z$ 下的子类划分：通过过滤操作 $\bar{X}_{w>z} = \{\bar{x}_i \mid w(c_i) > z\}$ 提取子集。当 $w$ 为阶梯函数时，不同阈值对应不同的子集规模；当 $w$ 为平滑函数时，则产生连续统的子类。

这一设计的因果链路是：**类别函数的形状同时编码了子类的空间结构（哪些点属于哪个子类）和相对重要性（通过阈值 $z$ 的积分权重体现）**。例如，Fig. 2b 中的两个阶梯函数隐式地定义了三类优化问题（红子集、蓝子集、并集），无需显式列出三个优化目标。

#### 创新点二：连续Wasserstein重心公式（Changed Slot: 优化问题形式）

传统多类别方法对每个目标分别最小化Wasserstein距离，或使用离散重心求和。本文将问题重新表述为**连续Wasserstein重心**：对类别函数的所有阈值进行积分，最小化期望Wasserstein距离：

$$\overline{X} := \underset{\overline{X}}{\arg\min} \int_{\mathbb{R}} W_p^p\big(\overline{X}_{w>z}, \mu_{w>z}\big) \, dz$$

当类别函数分段常数时，积分退化为加权和：

$$\overline{X} = \underset{\overline{X}}{\arg\min} \sum_{j=1}^{s} \lambda_j W_p^p\big(\overline{X}_{w>z_j}, \mu_{w>z}\big), \quad \lambda_j = z_j - z_{j-1}$$

扩展到多类别，对类别索引 $t$ 和阈值 $z$ 进行双重积分：

$$\overline{X} = \underset{\overline{X}}{\arg\min} \int_0^1 \int_0^1 W_p^p\big(\overline{X}_{w_t>z}, \mu_{w_t>z}\big) \, dz \, dt$$

这一公式的因果机制是：**积分自动为所有子类分配权重，子类规模越大（对应更低的阈值 $z$），在目标函数中的贡献越大**。这使得优化过程自然地平衡不同规模子类的需求，无需手动设置权重参数。

#### 创新点三：随机子类采样的切片梯度下降（Changed Slots: 优化算法 + 距离度量）

直接优化上述积分在计算上不可行。本文采用三重近似策略，形成高效的随机梯度下降方案：

**（1）切片Wasserstein距离替代**：将高维Wasserstein距离 $W_p$ 替换为切片Wasserstein距离 $SW_p$，通过对随机投影方向 $\theta \in \mathbb{S}^{d-1}$ 的一维Wasserstein距离进行积分来近似：

$$SW_p(\nu, \mu) = \int_{\mathbb{S}^{d-1}} W_p\big(\nu^\theta, \mu^\theta\big) \, d\theta$$

这一替换使得梯度计算仅需在一维投影上进行，复杂度大幅降低。

**（2）随机子类采样**：每次迭代随机选取一个类别 $t$ 和一个阈值 $z$，仅优化对应的单个子类 $\overline{X}_{w_t>z}$。这使得每步迭代的内存占用与目标总数无关——**优化100个类别与优化1000个类别，每次迭代的计算量相同**。

**（3）梯度缩放因子**：在一维投影优化中，直接使用点偏移会导致各向异性对齐伪影。本文引入基于投影目标密度的缩放因子 $\gamma_i^\theta$，更新规则为：

$$x_i^\theta = x_i^\theta - \eta \cdot \gamma_i^\theta \cdot \Delta_i^\theta$$

其中 $\Delta_i^\theta$ 是一维2-Wasserstein距离对点位置的导数：

$$\frac{d}{dx_i} W_2^2(X, \mu) = 2\frac{x_i}{n} - 2\int_{\frac{i-1}{n}}^{\frac{i}{n}} F_\mu^{-1}(x) \, dx$$

缩放因子 $\gamma_i^\theta$ 根据投影目标密度调整梯度幅度，避免点在各向异性方向上的过度对齐。这一机制被证实是消除条带伪影、提高蓝噪声各向同性的关键（Fig. 7 的消融实验验证）。

### 模块间的因果链路

整个方法的因果链路可概括为：

1. **类别函数 $w_t$ 定义子类结构** → 通过过滤操作 $\overline{X}_{w>z}$ 提取子集 → 子集规模由 $z$ 控制。
2. **连续重心公式积分所有 $(t,z)$** → 自动为各子类分配优化权重 → 无需手动调参。
3. **随机采样 $(t,z,\theta)$** → 每步仅优化一个一维投影子问题 → 计算量与目标数解耦。
4. **一维Wasserstein梯度 + 密度缩放** → 更新点位置 $x_i$ → 迭代收敛至多类别重心。

这一链路使得方法能够处理**成百上千个并发优化目标**，且内存占用几乎不随目标数增长。例如，在渐进式蒙特卡洛积分应用中，通过线性斜坡类别函数可产生4096个有效优化目标（子类），而优化过程的内存开销与单类别优化相当。

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/013_Figure_9.jpg]]
*Figure 9: Extending the problem in Fig. 8 to three colors (i.e., 7 classes), using 2049 points (683 points per color). Achieving uniform blue-noise quality across all classes is more difficult in this case due to higher, contention between the objectives*

## 实验与关键发现

### 主实验结果

**3类蓝噪声采样对比。** 在经典的红、蓝、并集三目标优化问题上，FSOT 在 GPU 上仅需 38 秒即可完成 2048 个点的优化，而 **Qin et al. 2017** 的熵正则化 Wasserstein 重心方法在 CPU 上需约 1 小时，速度提升约两个数量级。两者的功率谱径向均值和质量相近（Fig. 8），表明本方法在保持生成质量的同时，大幅降低了计算开销。功率谱中边界附近的各向异性主要源于边界对齐效应，本方法通过偏移校正和环形域优化缓解了此问题。

**单位平方蓝噪声质量。** 在 1024 点的均匀蓝噪声采样任务中，与直接构建的 **Paulin et al. 2020** 方法对比，FSOT 消除了条带对齐伪影，获得了更高质量的各向同性蓝噪声分布（Fig. 7）。Paulin et al. 的单位圆优化再映射方案和直接单位平方优化方案均产生可见的对齐结构，而 FSOT 的偏移校正（offset correction）是消除此类伪影的关键机制。环形域（toroidal domain）优化进一步改善了边界附近的方向性偏差（Fig. 7g）。

**渐进式蒙特卡洛积分。** 在渐进式蒙特卡洛积分任务中，FSOT 采用阶梯类别函数和轴对齐投影优先策略，积分误差收敛优于 Paulin et al. 2020（Fig. 14）。随着阶梯数增多，误差下降点增多但每个下降段变短；完全渐进式点集表现出均匀的误差行为（Fig. 15）。轴对齐投影优先（axis-aligned projection prioritization）比 Paulin et al. 的投影策略更有效，验证了投影方向选择对积分性能的实际影响。

**感知误差分布优化。** 在渲染任务中，FSOT 将感知误差分布建模为多类别问题（4096 个类别），在镜面反射等区域表现出明显优于传统非相关像素采样和现有蓝噪声误差分布方法的误差分布（Fig. 16），验证了该方法在图形学渲染中的实际价值。

### 可扩展性验证

FSOT 的优化时间对类别数增长仅呈弱敏感性。对于 262,144 个点：单类别优化耗时 3840 秒，3 类别耗时 4325 秒，7 类别耗时 4370 秒。从 1 类到 7 类，时间增幅仅约 14%，远低于传统方法中随目标数线性或超线性增长的趋势。这一性质源于随机子类采样策略——每次迭代仅优化一个子类，内存占用与目标总数解耦，使得处理成百上千个并发优化目标成为可能。

### 关键消融分析

**偏移校正（offset correction）。** 消融结果表明，偏移校正是消除对齐伪影、提高蓝噪声质量的决定性因素（Fig. 7）。该机制通过基于投影目标密度的梯度缩放因子 $\gamma_i^\theta$ 实现，避免了点集在投影方向上向目标分布的各向异性对齐。移除偏移校正后，点集出现明显的条带对齐结构。

**环形域优化。** 在单位平方上启用环形域优化可进一步改善边界附近的各向异性（Fig. 7g），但该改进相对偏移校正而言是次要的。环形域对周期性边界条件场景（如平铺纹理）尤为重要。

**随机子类采样。** 每次迭代随机选取一个类别和阈值进行一维切片投影优化，使得内存消耗与优化目标数解耦。这一设计是实现成百上千个类别同时优化的核心使能技术，也是 FSOT 区别于整体批次优化方法（如 Sinkhorn 算法）的关键架构差异。

**投影方向优先选择。** 在蒙特卡洛积分应用中，轴对齐投影优先策略（30% 的优化步选择坐标轴方向）显著提升了积分收敛速度（Fig. 14），表明投影方向分布对特定应用性能有实质影响。

### 适用边界与限制

**目标分布的可采样性要求。** FSOT 要求目标分布可被采样，不适用于仅有解析形式但无法高效采样的分布。这一限制在感知误差优化等应用中可通过点采样目标分布来缓解，但在一般场景下构成方法边界。

**硬件比较的不完全公平性。** 与 Qin et al. 2017 的时间对比中使用了不同硬件（GPU vs CPU），性能差异部分源于硬件而非算法本身。但质量对比（功率谱、视觉质量）仍具有参考价值，且 FSOT 的内存可扩展性优势独立于硬件选择。

**多目标争用下的质量退化。** 当类别数增加至 7 类（三色及其并集）时，由于目标间的争用加剧，在所有类别上同时保持均匀蓝噪声质量变得更加困难（Fig. 9）。这表明 FSOT 的质量并非完全独立于目标数量，在极高争用场景下存在质量退化。

**渐进式粒度的误差行为权衡。** 在渐进式点集优化中，更细的渐进粒度产生更多的误差下降点，但每个下降段更短（Fig. 15）。这一权衡意味着用户需根据具体应用场景选择适当的阶梯数，不存在通用的最优配置。

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/016_Figure_14.jpg]]
*Figure 14: Comparison of the Monte-Carlo variance convergence of our optimized point sets against those of Paulin et al. [2020]. We average variance over 10 realizations of each method and 40 variations of each function. Our axis-aligned projection prioritization is more effective than theirs*

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/010_Figure_7.jpg]]
*Figure 7: Comparison between different variants of our optimization and that of Paulin et al. [2020] which we build upon. All point sets are of size 1024 and the Fourier power spectra are averaged over 10 realizations. For our method we show realizations constructed with and without toroidality. Paulin et al. optimize on the unit circle (a) and then warp the resulting point set to the unit square (b); they also show direct unit-square optimization (c). Both their variants yield alignments that our method avoids (f-h), largely thanks to our offset correction (described in Section 5). One can also prioritize certain projections which can be beneficial for Monte-Carlo integration (see Fig. 14); here we...*

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/012_Figure_8.jpg]]
*Figure 8: 3-class (red, blue, red & blue) optimization of 2048 points (top row), along with the corresponding expected power spectra (middle row) and their radial averages (bottom row). Our optimization (bounded and toroidal) achieves similar quality to that of Qin et al. [2017] (bounded); ours takes 38 sec on GPU and theirs takes about 1 hour on CPU. The spectral anisotropy in the left two results is due to point alignments near the boundaries*

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/015_Figure_11.jpg]]
*Figure 11: A set of 2048 points optimized according to a configuration with two linear-ramp-function classes. At every point index we can split the set into two subsets with good-quality distribution each, for an effective number of 4096 optimization targets (i.e., subclasses). We show six such (color-coded) splits and the 2D Fourier power spectra of the two extracted subsets. The last row shows the radially averaged spectra of the subsets and the entire point set (in green)*

![[assets/figures/papers/paper_list_l86_http_www_iliyan_com_publications_ScalableMultiClassSampling/figures/018_Figure_15.jpg]]
*Figure 15: Progressive point-set optimization using a single, staircase-function class. Increasing the number of steps (with equal lengths in power-of-2 scale) increases the number of prefix subsets to optimize; we show 5 examples. The graphs plot integration-error behavior with increasing number of points taken, up to 16,384, averaged over 30 integrand variations and 20 pointset realisations. We see that finer progressive granularity yields a larger number of error dips, but each is shorter. The fully progressive (pink) point set exhibits uniform error behavior*

## 定位与知识库关联

本文的核心贡献在于改变了多类别采样优化问题的**目标定义与优化算法 slot**，将传统方法中“逐个子集单独指定目标、整体批次优化”的范式，替换为“通过类别函数在扩展维度上统一编码全部目标、以随机子类采样的随机梯度下降进行解耦优化”。这一改变使得优化计算与内存开销几乎与目标总数无关，从而将可处理的目标数量从个位数推高至数百甚至数千个。

### 相对于已有方法的本质差异

**相对于 Qin et al. (2017)**：Qin 等人的方法基于熵正则化 Wasserstein 重心，在 3 类蓝噪声采样中取得了高质量结果，但其优化过程需要同时处理所有目标分布，计算与存储开销随目标数量迅速增长，在目标数多时不可行。本文方法在 3 类场景下达到了与其相似的质量，但优化时间从约 1 小时（CPU）降至 38 秒（GPU），速度提升约 100 倍（Fig. 8）。更关键的是，Qin 等人的框架难以扩展到数十个以上的目标，而本文方法可轻松处理 15 类（CMYK 点画）乃至 4096 个子类（渐进式蒙特卡洛积分）。

**相对于 Paulin et al. (2020)**：Paulin 等人提出了基于切片 Wasserstein 距离的单类别点集优化方法，是本文的技术基础之一。本文在其基础上改变了两个关键 slot：（1）**优化目标定义**从单类别扩展为多类别连续重心，通过类别函数和过滤操作统一编码所有子类；（2）**梯度缩放**引入基于投影目标密度的缩放因子 γ（Eq. 16），消除了 Paulin 方法在单位正方形上产生的条带对齐伪影（Fig. 7）。消融实验表明，偏移校正（offset correction）是提高蓝噪声质量的关键因素，而环形域优化进一步改善了边界各向异性。

**相对于 Wei (2010) 与 Jiang et al. (2015)**：这些方法分别基于飞镖投掷和 SPH 进行多类别采样，本质上是对每个子集独立操作或通过交互矩阵协调。它们缺乏一个统一的优化目标来平衡所有子类之间的争用，难以保证全局最优性。本文的连续 Wasserstein 重心公式提供了一个全局一致的优化框架，所有子类通过共享的点集位置相互制约，自动达成平衡。

**相对于 Chen et al. (2013)**：Chen 等人提出了基于核优化的连续多类别采样，但该方法同样需要整体优化，可扩展性受限。本文的随机子类采样策略将每次迭代的计算量限制在单个子类上，内存占用几乎可忽略不计，从根本上解决了可扩展性问题。

### 知识库挂载点

本文在以下知识节点上提供了可挂载的增量贡献：

1. **Wasserstein 重心理论**：将离散 Wasserstein 重心扩展为连续形式（Eq. 4–6），通过类别函数在扩展维度 C 上定义子类的连续统，为多目标分布优化提供了统一的变分框架。该公式可挂载到最优传输理论中“重心”概念的推广分支。

2. **切片最优传输**：将切片 Wasserstein 距离（Eq. 2）与随机子类采样结合，形成可处理大量并发目标的随机优化方案（Eq. 8）。这一组合为切片最优传输在采样领域的应用提供了新的范式。

3. **蓝噪声采样**：在蓝噪声采样知识库中，本文提供了多类别扩展的通用方案，并揭示了偏移校正和环形域优化对消除各向异性伪影的作用机制。

4. **蒙特卡洛积分**：通过类别函数定义渐进式点集分割（Fig. 11, 15），将蓝噪声采样与渐进式蒙特卡洛积分桥接，为积分误差界（Eq. 10–11）提供了可优化的上界。

### 适用边界

- **目标分布需可采样**：本方法要求目标分布 μ_t 可以被采样，以便在每次迭代中生成投影所需的点集。对于仅有密度函数而无解析采样方法的分布，需要额外的采样技术配合。
- **类别函数需预先定义**：类别函数 w_t 的形状直接决定了子类的划分和权重，需要用户根据应用场景手工设计（如阶梯函数、线性斜坡函数等）。方法的自动化程度受限于类别函数的设计空间。
- **优化质量与迭代次数相关**：随机子类采样虽然降低了单步开销，但需要更多迭代来覆盖所有子类。对于极高精度的需求，优化时间可能显著增加。
- **硬件对比的不完全公平性**：文中与 Qin et al. 的时间对比使用了不同硬件（GPU vs CPU），质量对比仍具参考性，但速度提升的精确倍数需谨慎解读。

### 后续启发

1. **类别函数的自动学习**：当前类别函数由用户手工定义，未来可探索从数据或任务中自动学习最优的类别函数形状，进一步提升方法的自动化程度和优化质量。

2. **与其他最优传输变体的结合**：本文使用切片 Wasserstein 距离作为计算高效的近似，后续可探索与熵正则化 Wasserstein、小批量 Wasserstein 等变体的结合，在效率与精度之间寻找新的平衡点。

3. **动态目标分布**：当前框架假设目标分布在优化过程中固定不变，扩展到动态变化的目标分布（如时变密度函数）将是一个有价值的方向。

4. **高维采样空间**：本文主要展示了 2D 空间域的采样结果，框架本身对维度无本质限制，但在高维空间中的切片投影效率和采样质量仍需进一步验证。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Scalable_multi_class_sampling_via_filtered_sliced_optimal_transport.pdf]]