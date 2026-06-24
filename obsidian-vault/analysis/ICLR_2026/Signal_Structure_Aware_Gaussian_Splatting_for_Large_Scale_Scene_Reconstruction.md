---
title: Signal Structure-Aware Gaussian Splatting for Large-Scale Scene Reconstruction
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Signal_Structure_Aware_Gaussian_Splatting_for_Large_Scale_Scene_Reconstruction_b8fbdcdc91cf.pdf
project_link: null
code_link: null
aliases:
- SSAGSS
- SSAGSLSSR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过定义3D高斯表示的平均采样频率和场景带宽，在训练中自适应地同步图像分辨率（采样频率）和高斯稠密化过程，使两者随场景频率收敛而逐步提高。
primary_logic: 将场景重建视为信号结构恢复问题，从频域角度推导出3D高斯表示的平均频率，并利用场景频率收敛动态调度图像分辨率和高斯稠密化，实现频率一致的粗到细训练；同时引入球约束高斯和稠密正则化，利用几何先验约束高斯分布。
claims:
- 所定义的场景平均带宽与采样频率（图像分辨率）呈正相关，验证了频率定义的有效性。
- 频率一致的训练策略（SIG）相比直接高分辨率训练和无调度策略，显著减少冗余高斯和浮点，提升渲染质量并加速训练。
- 球约束高斯（SCG）和稠密正则化（DR）有效减少冗余和错误优化，降低高斯数量。
- 本方法在多个基准上实现了质量和速度的显著提升，例如在Mill19 rubble场景上PSNR提升+0.9 dB，训练速度提升1.5倍/块。
---

# Signal Structure-Aware Gaussian Splatting for Large-Scale Scene Reconstruction

> [!tip] 核心洞察
> 将场景重建视为信号结构恢复问题，从频域角度推导出3D高斯表示的平均频率，并利用场景频率收敛动态调度图像分辨率和高斯稠密化，实现频率一致的粗到细训练；同时引入球约束高斯和稠密正则化，利用几何先验约束高斯分布。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大规模场景重建的信号结构感知高斯散点法 |
| 英文题名 | Signal Structure-Aware Gaussian Splatting for Large-Scale Scene Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DavFcTeTbK) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Signal Structure-Aware Gaussian Splatting (SIG) |
| Dataset | Mill-19 rubble |

> [!tip] 效果简介
> - Mill-19 rubble 上，PSNR (dB) 27.35 vs 26.45 (CityGS) (+0.9)；SSIM 0.843 vs 0.809 (CityGS) (+0.034)；LPIPS 0.189 vs 0.232 (CityGS) (-0.043)。

## 概述

**核心问题**：在大规模场景重建中，基于3D高斯散点（3D Gaussian Splatting, 3DGS）的方法面临一个根本性瓶颈——稀疏的初始点云使得高斯表示在训练初期表现为低频信号，而直接使用高频图像进行监督会导致采样频率与目标信号频率之间的严重失配。这种失配引发不受控制的稠密化，产生大量冗余高斯和浮点伪影（floaters），显著降低训练效率和渲染质量（Figure 1）。

**核心洞察**：本文提出**信号结构感知高斯散点法（Signal Structure-Aware Gaussian Splatting, SIG）**，将场景重建重新定义为信号结构恢复问题。核心思路是从频域角度推导3D高斯表示的平均频率，并利用场景频率的收敛动态来同步调度图像分辨率（采样频率）与高斯稠密化过程，实现频率一致的粗到细训练。

**方法定位**：SIG在现有分块重建框架（如**CityGS**, Liu et al., ECCV 2024）的基础上，引入三个关键模块：
- **频率对齐的分辨率调度器（FARS）**：基于场景平均频率的收敛条件自适应提升训练图像分辨率，替代固定分辨率或预定义调度策略（如**DashGS**, Chen et al., CVPR 2025；**TamingGS**, Mallick et al., SIGGRAPH Asia 2024）。
- **球约束高斯（SCG）**：利用初始点云的几何先验，将每个高斯绑定到锚点并限制其最大偏移，防止高斯漂移和浮点生成。
- **稠密正则化（DR）**：通过多视图重投影光度损失约束稠密化过程，增强几何一致性。

**主要结果**：在多个大规模场景基准上，SIG实现了显著的质量与效率提升。以Mill-19 rubble场景为例，相比CityGS基线，PSNR提升**+0.9 dB**（27.35 vs 26.45），SSIM提升至0.843，LPIPS降至0.189，同时训练速度提升约**1.4倍**（71 min/block vs 98 min/block）。消融实验（Table 2）验证了频率一致训练策略的核心作用：去除FARS导致PSNR下降约1.17 dB，高斯数量从1.5M激增至2.2M。SCG和DR分别通过空间约束和几何正则化进一步减少冗余高斯并提升渲染质量。

## 背景与动机

### 大规模场景重建的核心挑战

大规模场景的神经渲染与重建在数字孪生、自动驾驶仿真、虚拟现实等领域具有重要应用价值。以3D Gaussian Splatting（3DGS）（Kerbl et al., ACM Trans. Graph. 2023）为代表的高斯散点方法，凭借其显式表示和可微光栅化管线，在渲染质量和速度上取得了突破性进展。然而，当面对城市级或建筑级大规模场景时，现有方法普遍面临一个深层瓶颈：**稀疏初始点云导致高斯表示在训练初期呈现低频特性，而直接使用高频图像进行监督，会引发采样频率与目标信号频率之间的严重失配**。

### 频率失配的因果机制

这一频率失配问题可从信号重建的角度加以理解。在大规模场景中，初始点云通常来自运动恢复结构（SfM），其密度远不足以刻画场景的高频细节。因此，训练初期的3D高斯表示本质上是一个低频信号。若此时直接以全分辨率图像（高频信号）作为监督目标，优化过程会强制低频表示去拟合高频目标，导致以下连锁问题：

1. **不受控制的稠密化**：为弥合频率差距，梯度驱动的稠密化机制会在缺乏足够低频支架的情况下盲目分裂高斯原语，产生大量冗余高斯。
2. **浮点伪影（Floaters）**：冗余高斯在稀疏观测区域尤其严重，它们缺乏多视图几何约束，在优化中漂移至错误位置，形成视觉上的浮点伪影。
3. **训练效率骤降**：冗余高斯不仅降低渲染质量，还显著增加计算开销，拖慢训练收敛速度。

Figure 1 直观展示了这一现象：直接以高频图像监督的方法会产生大量冗余高斯和浮点，且无法有效利用更多原语来捕获高频细节。

### 现有方法的缺口

针对大规模场景重建，近期工作主要沿两条路径展开：

- **分块策略**：如 **CityGS**（Liu et al., ECCV 2024）和 **BlockGS**（Wu et al., arXiv 2025）将大场景划分为多个块分别训练，有效管理了内存和计算资源，但未解决块内训练的频域失配问题。
- **预定义调度**：如 **DashGS**（Chen et al., CVPR 2025）和 **TamingGS**（Mallick et al., SIGGRAPH Asia 2024）采用固定的分辨率提升或稠密化调度，虽引入了粗到细的思想，但调度策略与场景实际频率演化脱节——分辨率提升时机和稠密化轮次均基于预设规则，而非场景信号的收敛状态。

这两类方法的共同缺陷在于：**未能将场景重建显式建模为信号结构的恢复过程**，因此无法从根本上解决频率失配带来的冗余和伪影问题。

### 本文动机与核心思路

本文的核心洞察是：**大规模场景重建本质上是一个信号结构恢复问题**。从频域视角出发，3D高斯表示具有可定义的场景带宽和平均频率，而图像分辨率决定了监督信号的采样频率。当且仅当两者协调一致时，优化过程才能高效且无冗余地进行。

基于这一洞察，本文提出**信号结构感知高斯散点法（Signal Structure-Aware Gaussian Splatting, SIG）**，核心思路包括：

- **频率对齐训练**：通过数学定义3D高斯表示的平均频率，在训练中自适应地同步图像分辨率（采样频率）与高斯稠密化过程，使两者随场景频率收敛而逐步提高，实现频率一致的粗到细训练。
- **几何先验约束**：引入球约束高斯（Sphere-Constrained Gaussians）和稠密正则化（Densification Regularization），利用初始点云的空间先验和多视图几何一致性约束高斯分布，进一步抑制冗余和浮点。

该方法在多个大规模场景基准上实现了显著的质量提升（Mill-19 rubble场景PSNR提升+0.9 dB）和训练加速（每块训练时间减少至1/1.5），验证了频域视角在场景重建中的有效性。

## 核心创新

本工作将大规模场景重建重新定义为**信号结构恢复问题**，从频域视角揭示了现有高斯散点法在大规模场景中的根本瓶颈，并围绕该瓶颈提出了三项关键创新。

### 瓶颈洞察：高频监督与低频表示的频率失配

在大规模场景中，由运动恢复结构（SfM）得到的初始点云极为稀疏，导致初始的3D高斯表示本质上是一个**低频信号**。现有方法（如**3DGS**（Kerbl et al., ACM Trans. Graph. 2023）、**CityGS**（Liu et al., ECCV 2024））在训练全程直接使用高分辨率图像进行监督，这造成了**采样频率与目标信号频率之间的严重失配**。这种频率失配引发了一系列连锁问题：不受控制的稠密化产生大量冗余高斯、浮点伪影（floaters）激增，严重降低了训练效率和渲染质量（如Figure 1所示）。

### 创新一：频率对齐的自适应训练调度（核心机制）

本方法的核心创新在于建立了**场景频率与训练调度之间的因果调控机制**。具体而言：

- **场景频率的数学定义**：将3D高斯表示的不透明度场建模为高斯混合分布 $D(\mathbf{x}) = \sum_{i=1}^{n} o_{i} G_{i}(\mathbf{x})$，通过推导其功率谱，定义了场景的平均频率 $\bar{\omega} = \frac{ \sum_{i}^{n} o_{i}^{2} \operatorname*{det}(\pmb{\Sigma}_{i}) \omega_{3\mathrm{dB}_{i}} }{ \sum_{i}^{n} o_{i}^{2} \operatorname*{det}(\pmb{\Sigma}_{i}) }$，其中 $\omega_{3\mathrm{dB}_{i}}$ 为每个高斯原语的3dB带宽。该定义的有效性得到了实验验证：场景平均带宽与采样频率（图像分辨率）呈明确正相关（Figure 3(a)）。

- **频率对齐的分辨率调度器（FARS）**：不同于基线方法全程使用固定最高分辨率，本方法根据场景频率的收敛条件 $\frac{df}{d\mathfrak{iter}} < k \cdot \mathrm{mean}(\frac{1}{d})$ 自适应地提升训练图像分辨率。当场景频率变化率低于阈值时，表明当前分辨率下的信息已被充分吸收，此时触发分辨率升级。

- **联动稠密化调度器（DS）**：与基线方法按固定迭代间隔稠密化不同，本方法将稠密化与分辨率调度联动——每次分辨率更新后执行 $m$ 轮稠密化，使高斯原语的增加与场景频率的提升同步，逐步恢复高频细节。

这一频率一致的粗到细训练策略构成了方法的核心因果杠杆：通过同步图像采样频率与高斯表示频率，从根本上消除了频率失配导致的冗余和浮点问题。

### 创新二：球约束高斯（SCG）

现有方法中高斯原语可自由移动和缩放，在稀疏观测区域容易漂移产生浮点。本方法引入**球约束高斯**：每个高斯绑定一个来自初始点云的锚点，并限制其最大偏移范围。当高斯超出 $l \times$ 最大偏移时即被修剪。这一设计利用了几何先验约束优化空间，有效抑制了稀疏区域的错误优化。

### 创新三：稠密正则化（DR）

针对稠密化过程中可能破坏多视图一致性的问题，本方法引入基于重投影光度误差的**稠密正则化损失** $\mathcal{L}_{\mathrm{cons}}$：利用渲染深度图在不同视图间进行重投影，计算光度误差，约束稠密化过程保持几何一致性。这弥补了现有方法缺乏显式几何一致性正则化的不足。

### 创新点的协同效应

消融实验（Table 2）量化了各创新的贡献：去除FARS导致PSNR下降约1.17 dB（26.18 vs 27.35）且高斯数量从1.5M增至2.2M；去除DS使PSNR下降0.46 dB；去除SCG和DR分别导致PSNR下降0.3 dB和0.34 dB，同时高斯数量增加。这些结果表明，频率对齐调度是性能提升的主要驱动因素，而SCG和DR作为几何约束进一步巩固了重建质量与效率。

## 整体框架

SIG 的整体训练流程建立在分块重建范式之上，其核心创新在于引入了一个**频率对齐的粗到细调度机制**，将场景重建重新表述为信号结构恢复问题。如 Figure 2 所示，框架由五个关键模块串联构成，形成从低频支架到高频细节的渐进式优化管线。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/002_Figure_2.jpg]]
*Figure 2: Overview. We define Gaussian frequency based on the opacity field, represented as a weighted sum of Gaussians. Using a frequency-matching module, we synchronize image supervision with Gaussian frequencies (SIG), and optimize with Sphere-Constrained Gaussians to incorporate geometric priors*

### 1. 粗训练支架

方法沿用 **CityGS**（Liu et al., ECCV 2024）的分块策略：首先在低分辨率下进行全局粗训练，构建场景的基础几何支架。这一阶段产生的初始高斯分布本质上是一个低频表示，为后续的频率感知调度提供了起点。

### 2. 频率对齐的分辨率调度器（FARS）

这是整个框架的**核心调度引擎**。该模块在每个训练迭代中计算场景的平均频率 $\bar{\omega}$（由式 (5) 定义），并监控其变化率。当满足收敛条件
$$\frac{df}{d\mathfrak{iter}} < k \cdot \mathrm{mean}(\frac{1}{d})$$
时，自动触发训练图像分辨率的提升。这一机制确保了**采样频率（图像分辨率）始终与场景表示的当前频率带宽相匹配**，从根本上避免了直接使用高频图像监督导致的频率失配问题。

### 3. 稠密化调度器（DS）

与 FARS 紧密联动，在每次分辨率更新后执行 $m$ 轮高斯稠密化。这种联动设计使得新增的高斯原语仅在场景频率收敛、表示能力达到当前分辨率瓶颈时才被引入，从而逐步恢复高频细节，而非像传统方法那样按固定迭代间隔盲目稠密化。

### 4. 球约束高斯（SCG）

为每个高斯椭球体绑定一个来自初始点云的锚点，并限制其最大偏移范围。当高斯的位置超出 $l \times$ 最大偏移时，该高斯被修剪。这一几何先验有效约束了优化空间，防止高斯漂移和浮点伪影的产生。

### 5. 稠密正则化（DR）

在稠密化过程中引入基于重投影光度误差的一致性损失 $\mathcal{L}_{\mathrm{cons}}$，利用渲染深度图进行帧间重投影，约束多视图几何一致性，进一步抑制错误优化和冗余生成。

### 数据流与模块关系

整个管线的数据流可概括为：**低分辨率图像 → 粗训练支架 → 场景频率监控（FARS）→ 分辨率提升 + 稠密化（DS）→ SCG 约束优化 + DR 正则化 → 高分辨率细训练 → 最终渲染**。FARS 作为调度中枢，同时控制图像分辨率和稠密化节奏；SCG 和 DR 则作为约束层，在优化过程中持续过滤冗余和错误的高斯，确保频率提升带来的额外原语被有效用于高频细节捕获，而非产生浮点。

## 核心模块与公式推导

### 问题形式化：从信号频域视角看高斯散点重建

本方法将大规模场景的3D高斯散点重建重新定义为**信号结构恢复问题**。核心瓶颈在于：稀疏的初始点云（通常来自SfM）使得3D高斯表示在训练初期呈现低频特性，然而现有方法直接使用全分辨率高频图像进行监督。这种**采样频率与目标信号频率之间的失配**导致了不受控制的稠密化、大量冗余高斯原语以及漂浮伪影（floaters），严重降低训练效率和渲染质量（参见Figure 1）。

为解决这一问题，SIG框架建立了3D高斯表示与信号频域之间的桥梁，通过自适应同步图像监督分辨率与高斯表示频率，实现频率一致的粗到细训练。

### 关键模块一：场景频率估计与定义

#### 平均采样频率定义

首先定义场景层面的平均采样频率，用于指导训练图像分辨率的选择。给定场景中 $n$ 个3D高斯原语，对于每个高斯 $i$，其在图像平面上的投影区域内的采样频率取决于相机焦距 $f$ 和该点的深度 $d_i(s)$：

$$
v = \sum_{i=1}^{n} \int_{s} w_{i}(s) \cdot \frac{f}{d_{i}(s)} ds, \quad \int_{s} w_{i}(s) ds = 1
$$

其中 $w_i(s)$ 为第 $i$ 个高斯在图像坐标 $s$ 处的观测权重，由该高斯的投影覆盖度和不透明度决定。该公式将场景的平均采样频率定义为所有高斯原语在其可见区域内的深度加权平均。

#### 场景不透明度场与频域表示

为从3D高斯表示中提取频率信息，将场景建模为不透明度场 $D(\mathbf{x})$，表示为所有高斯原语的加权和：

$$
D(\mathbf{x}) = \sum_{i=1}^{n} o_{i} G_{i}(\mathbf{x}) = \sum_{i=1}^{n} o_{i} (2\pi)^{3/2} \det(\Sigma)^{1/2} \mathcal{N}(\mathbf{x}; \mu_{i}, \Sigma_{i})
$$

其中 $o_i$ 为第 $i$ 个高斯的不透明度，$\mathcal{N}(\mathbf{x}; \mu_i, \Sigma_i)$ 为均值为 $\mu_i$、协方差矩阵为 $\Sigma_i$ 的3D高斯分布。

#### 场景平均频率估计

通过对不透明度场进行傅里叶变换并近似其功率谱，推导出场景的平均频率估计。将功率谱近似为各高斯原语在其3dB带宽处的离散贡献之和：

$$
|\hat{D}(\omega)|^2 \approx \sum_i o_i^2 \det(\Sigma_i) \delta(\omega - \omega_{3\text{dB}_i})
$$

其中 $\omega_{3\text{dB}_i}$ 为第 $i$ 个高斯的3dB带宽。对于尺度为 $[\sigma_1, \sigma_2, \sigma_3]$ 的高斯原语，其3dB带宽与尺度倒数之和成正比：$\omega_{3\text{dB}_i} \propto \sum_{k=1}^{3} \frac{1}{3\sigma_k}$。

基于此，定义整个场景的平均频率为所有高斯原语3dB带宽的加权平均，权重由 $o_i^2 \det(\Sigma_i)$ 决定：

$$
\bar{\omega} = \frac{ \sum_{i}^{n} o_{i}^{2} \det(\pmb{\Sigma}_{i}) \omega_{3\mathrm{dB}_{i}} }{ \sum_{i}^{n} o_{i}^{2} \det(\pmb{\Sigma}_{i}) }
$$

该定义的有效性得到了实验验证：Figure 3(a) 显示场景平均带宽与采样频率（图像分辨率）呈明显正相关，且随训练迭代稳定增长，表明该频率度量能够准确反映场景表示的信息容量变化。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/003_Figure_3.jpg]]
*Figure 3: Effectiveness Validation: (a) Average Scene Bandwidth during Training under Different Image Resolutions and*

### 关键模块二：频率对齐的分辨率调度器（FARS）

基于上述场景频率定义，FARS模块实现了训练图像分辨率与高斯表示频率的自适应同步。核心思想是：**当场景频率收敛时，提升图像分辨率以引入更高频的监督信号**。

具体地，监控场景平均频率 $\bar{\omega}$ 随训练迭代的变化率。当频率变化率低于预设阈值时，触发分辨率提升：

$$
\frac{df}{d\mathfrak{iter}} < k \cdot \mathrm{mean}\left(\frac{1}{d}\right)
$$

其中 $\frac{df}{d\mathfrak{iter}}$ 为场景频率对迭代次数的导数，$k$ 为收敛阈值系数，$\mathrm{mean}(1/d)$ 为场景平均逆深度。该条件确保只有当当前分辨率下的场景频率已充分收敛时，才引入更高分辨率的监督，避免频率失配导致的冗余稠密化。

### 关键模块三：稠密化调度器（DS）

与FARS联动，稠密化调度器在每次分辨率更新后执行 $m$ 轮高斯稠密化。这一设计的因果逻辑是：分辨率提升后，场景表示需要更多高斯原语来拟合新引入的高频细节，因此在分辨率更新后立即进行稠密化，使高斯数量与场景频率需求保持同步。

### 关键模块四：球约束高斯（SCG）

为利用初始点云提供的几何先验约束高斯优化，SCG为每个高斯原语分配两个属性：**锚点**（anchor）和**最大偏移量**（max offset）。锚点通常取自初始SfM点云中的最近点，高斯中心被限制在以锚点为球心、最大偏移量为半径的球形区域内。当高斯中心超出 $l \times$ 最大偏移量时，该高斯被修剪。

这一约束有效防止了高斯原语在优化过程中的空间漂移，尤其对稀疏观测区域中的漂浮伪影有显著抑制作用。

### 关键模块五：稠密正则化（DR）

DR通过多视图几何一致性损失约束稠密化过程。利用渲染的深度图进行帧间重投影，计算重投影光度误差：

$$
\mathcal{L}_{\mathrm{cons}} = \sum_{(i,j)} \lVert C_{i}\langle p\rangle - C_{j} \langle \mathcal{F}_{j}(T_{j} T_{i}^{-1} \mathcal{F}^{-1}(z, p)) \rangle \rVert_{2}^{2}
$$

其中 $(i, j)$ 为相邻视图对，$C_i\langle p\rangle$ 为视图 $i$ 中像素 $p$ 的颜色，$z$ 为渲染深度，$T_i$ 和 $T_j$ 为相机位姿，$\mathcal{F}$ 和 $\mathcal{F}^{-1}$ 分别表示投影和反投影操作。该损失函数强制新稠密化的高斯原语在多视图间保持光度一致性，减少错误优化。

### 模块协同与训练流程

SIG的完整训练流程分为两个阶段：

1. **粗训练支架**：采用CityGS的分块策略，使用低分辨率图像构建场景的几何支架，为后续细训练提供稳定的初始表示。
2. **细训练优化**：在每个分块内，FARS和DS协同工作——FARS监控场景频率收敛并自适应提升分辨率，DS在每次分辨率更新后执行稠密化；SCG和DR分别从空间约束和多视图一致性角度约束优化过程，最终完成高频细节的恢复。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/001_Figure_1.jpg]]
*Figure 1: Floaters and redundancy. Prior methods that directly supervise with high-frequency images lead to redundancy and cannot exploit more primitives to capture high-frequency details*

## 实验与分析

### 核心瓶颈验证：频率匹配的因果效应

本工作的核心假设是：稀疏初始点云导致的高斯表示初始为低频信号，若直接使用高频图像监督，会引起采样频率与目标信号频率的不匹配，进而导致不受控制的稠密化、大量冗余高斯和浮点伪影。为验证这一因果链条，作者首先检验了所定义的场景平均带宽的有效性。

**Figure 3(a)** 展示了在不同图像分辨率下，场景平均带宽随训练迭代的变化。结果显示，场景平均带宽与采样频率（图像分辨率）呈明确的正相关关系，且随训练推进稳步增长。这一实证验证了基于3D高斯不透明度场推导的平均频率定义（Equation 5）能够有效刻画场景的频率特性，为后续的频率对齐调度提供了可靠的理论基础。

在此基础上，**Table 2** 的消融实验直接验证了频率一致训练策略的因果效应。去除频率对齐的分辨率调度器（w/o-FARS）后，PSNR从完整方法的27.35 dB骤降至26.18 dB（降幅达1.17 dB），同时高斯数量从1.5M膨胀至2.2M。这表明，缺乏频率同步的训练会引发严重的冗余稠密化，大量高斯原语被错误地用于拟合本应由更高分辨率图像监督的高频细节，而非真正提升重建质量。去除稠密化调度器（w/o-DS）同样导致PSNR下降0.46 dB，说明单纯提升分辨率而不配合相应的稠密化轮次，无法有效利用新增的高频监督信息。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/007_Table_2.jpg]]
*Table 2: Ablation. Frequency-consistent training yields substantial performance gains*

### 主结果分析：质量与效率的双重提升

**Table 1** 报告了在多个大规模场景基准上的定量对比结果。以Mill-19 rubble场景为例，本方法取得了27.35 dB的PSNR，较CityGS基线（26.45 dB）提升+0.9 dB；SSIM从0.809提升至0.843，LPIPS从0.232降至0.189。这一质量增益在稀疏观测区域尤为显著：**Figure 4** 的定性对比显示，基线方法在稀疏视角区域产生大量浮点伪影和冗余高斯，而本方法通过球约束高斯（SCG）和稠密正则化（DR）有效抑制了这些错误优化，同时保持了完整的高频几何结构。

在训练效率方面，**Table 3** 展示了本方法作为即插即用模块与不同基线集成的效果。以CityGS为支架时，集成后的训练时间从每块98分钟降至71分钟，加速约1.4倍；集成BlockGS时加速达1.5倍。效率提升的核心机制在于：频率对齐调度避免了无效的冗余稠密化，使优化过程更加聚焦于真实的高频细节恢复，而非在低频阶段浪费计算资源。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/008_Table_3.jpg]]
*Table 3: Integration with other baselines. We improve quality and efficiency by augmenting baselines with our method (*). Opt.time: min/block*

### 消融实验：各模块的独立贡献与失效模式

**Table 2** 的系统消融揭示了四个关键模块的独立贡献和失效后果：

- **去除SCG（球约束高斯）**：高斯数量从1.5M增至1.8M，PSNR下降0.30 dB。球约束通过将每个高斯绑定至初始点云锚点并限制最大偏移，防止了高斯在优化中漂移出合理空间区域。去除该约束后，高斯可自由移动和缩放，导致在稀疏观测区域产生大量偏离真实几何的浮点高斯。

- **去除DR（稠密正则化）**：PSNR下降0.34 dB，高斯数量增至1.9M。稠密正则化损失（$\mathcal{L}_{\mathrm{cons}}$）利用渲染深度图进行帧间重投影光度约束，强制多视图几何一致性。缺乏该约束时，稠密化过程缺乏几何引导，容易在遮挡或纹理模糊区域生成错误高斯。

- **降低CityGS稠密化阈值（CityGS-L）**：该变体试图通过更激进的稠密化来拟合高频细节，但PSNR仅为26.55 dB，且高斯数量高达2.3M。**Figure 5** 的定性对比显示，CityGS-L虽然生成了更多高斯，但由于缺乏频率同步机制，大量高斯被浪费在低频区域的冗余表达上，反而引入了更多伪影。这进一步印证了频率匹配而非简单增加原语数量才是关键。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/005_Figure_5.jpg]]
*Figure 5: Ablation. CityGS-L: lower densification threshold of CityGS for higher-frequency fitting*

### 局限性与开放问题

当前方法的一个显著局限是未能充分利用粗到细训练过程自然产生的层次化高斯结构。在频率逐步提升的训练过程中，不同阶段生成的高斯天然具有不同的频率特性（粗高斯对应低频结构，细高斯对应高频细节），但本方法并未将这些高斯组织为内在的细节级别（LOD）层次。在更大规模场景中，这一缺失可能限制渲染效率的进一步提升。如何从频率一致的训练过程中自动构建层次化LOD结构，是值得探索的开放方向。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison of NVS results. The best, the second best, and the third best results are highlighted in red , orange and yellow*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_DavFcTeTbK/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative Results. The top two rows illustrate sparse observations, whereas the bottom two represent regular regions. For regions corresponding to sparse viewpoints, our approach effectively minimizes the generation of redundant and erroneous Gaussian components. For general regions, our method recovers high-frequency details while maintaining intact geometric structures*

## 方法谱系与知识库定位

### 与基线方法的关系

**SIG** 以 **3D Gaussian Splatting (3DGS)**（Kerbl et al., ACM Trans. Graph. 2023）为基础表示框架，但并非简单的工程改进，而是从信号结构恢复的视角重新审视了高斯散点优化的核心矛盾。其关键突破在于识别出：稀疏初始点云导致高斯表示初始为低频信号，直接使用高频图像监督会引起采样频率与目标信号频率的失配，从而导致不受控制的稠密化、大量冗余高斯和浮点伪影。这一瓶颈认知将本方法与现有工作明确区分开来。

在大规模场景重建这一具体任务上，SIG 直接建立在 **CityGS**（Liu et al., ECCV 2024）的分块策略之上——采用相同的粗训练构建场景支架、再对每个块进行细训练的流程。但 CityGS 在细训练阶段全程使用最高分辨率图像，本质上仍属于“直接高频监督”的范式。SIG 将频率对齐的分辨率调度器（FARS）和联动稠密化调度器（DS）嵌入该流程后，在 Mill-19 rubble 场景上将 PSNR 从 26.45 dB 提升至 27.35 dB（+0.9 dB），同时将每块训练时间从 98 分钟降至 71 分钟（加速约 1.4×）。

与 **BlockGS**（Wu et al., arXiv 2025）集成时，SIG 同样展现出即插即用的兼容性，带来 1.5 倍的训练加速。这验证了频率一致训练策略的通用性——它不依赖于特定的分块方案或初始点云质量。

在调度策略的谱系中，**DashGS**（Chen et al., CVPR 2025）和 **TamingGS**（Mallick et al., SIGGRAPH Asia 2024）均采用预定义的稠密化调度（如每固定迭代间隔执行稠密化），而 SIG 将稠密化调度与分辨率调度联动——在每次分辨率更新后执行 m 轮稠密化，使高斯数量的增长与场景频率的收敛同步。消融实验表明，去除联动调度（w/o-DS）导致 PSNR 下降约 0.46 dB（26.89 vs 27.35），且无法进一步利用高分辨率信息。

### 适用边界

SIG 的有效性依赖于以下前提条件，超出这些边界时性能可能退化：

1. **初始几何先验的可用性**：球约束高斯（SCG）将每个高斯绑定到初始点云的锚点并限制最大偏移，这一机制的有效性取决于初始点云（如 SfM 稀疏重建）的覆盖质量。在极端稀疏观测区域，锚点本身可能不足，虽然论文展示了在这些区域仍能有效抑制冗余高斯生成，但若初始点云存在系统性缺失，约束可能过于严格。

2. **分块策略的依赖**：SIG 沿用 CityGS 的分块策略，这意味着场景需要具有可被合理划分的空间结构。对于高度非结构化或尺度差异极大的场景，分块边界的衔接质量可能需要额外验证。

3. **频率收敛的可检测性**：FARS 的触发条件依赖于场景平均频率的变化率低于阈值（公式 6），这要求训练过程中频率估计本身是稳定的。论文通过 Figure 3(a) 验证了场景带宽随训练迭代稳定增长，但若场景包含大量半透明或镜面反射区域，不透明度场的高斯近似可能偏离实际频率特性。

4. **未利用内在层次化 LOD**：论文明确指出的一个局限是，粗到细训练过程自然产生了粗/细高斯，但 SIG 并未将其组织为层次化的细节级别（LOD）结构。这意味着在更大规模场景中，渲染效率可能受限于线性增长的高斯数量，而非通过 LOD 实现与视距相关的自适应渲染。

### 局限与开放问题

**已识别的局限**：当前方法虽然兼容现有的 LOD 策略，但未能充分利用粗到细训练自然产生的粗/细高斯来构建内在的层次化 LOD 结构。这限制了在更大规模场景中通过视距相关的细节级别切换来进一步优化渲染效率的可能性。

**开放问题**：如何从频率一致的粗到细训练过程中自动生成层次化的 LOD 结构？具体而言，训练过程中不同阶段产生的高斯原语天然具有不同的频率特性（早期粗高斯对应低频结构，后期细高斯对应高频细节），能否设计一种机制，将这些高斯按频率层级组织，并在渲染时根据视距或屏幕空间采样率动态选择合适的层级组合？

**需要人工验证的问题**：论文未提供在非 SfM 初始点云（如 LiDAR 扫描或随机初始化）条件下的消融实验。SCG 对初始点云质量的敏感度边界，以及 FARS 在初始点云极度稀疏时的频率估计稳定性，需要进一步验证。此外，与基于 NeRF 的大规模场景方法（如 Block-NeRF、Mega-NeRF）的直接对比缺失，这限制了在渲染质量-训练效率权衡空间中的完整定位。

## 原文 PDF

![[paperPDFs/ICLR_2026/Signal_Structure_Aware_Gaussian_Splatting_for_Large_Scale_Scene_Reconstruction_b8fbdcdc91cf.pdf]]