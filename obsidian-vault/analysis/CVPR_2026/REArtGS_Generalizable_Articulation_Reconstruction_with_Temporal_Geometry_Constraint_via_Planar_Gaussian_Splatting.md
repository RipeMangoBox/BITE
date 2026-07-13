---
title: "REArtGS++: Generalizable Articulation Reconstruction with Temporal Geometry Constraint via Planar Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/REArtGS_Generalizable_Articulation_Reconstruction_with_Temporal_Geometry_Constraint_via_Planar_Gaussian_Splatting.pdf
project_link: "https://sites.google.com/view/reartgs2/home"
code_link: null
aliases:
- RGARTGCPGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 解耦的螺旋运动建模（无关节类型先验）与基于泰勒一阶展开的时间连续几何正则化，允许在仅两状态图像监督下联合优化部件分割、关节参数和平面高斯。
primary_logic: 将3D高斯压缩为平面并利用泰勒展开将法向-深度一致性从离散状态推广到整个运动区间，无需深度真值即可为关节运动提供有效的时间几何约束。
claims:
- 解耦螺旋运动无需关节类型先验，通过部件运动混合实现任意关节参数估计。
- 泰勒展开实现时间连续的几何正则化，使未观测状态的动态重建质量显著提升。
- 在PARIS数据集上，CD-w误差相比REArtGS降低27.6%，所有平均指标均达到最佳或次优。
- PARIS Synthetic Objects 上 CD-w (Chamfer Distance weighted) = 1.75
---

# REArtGS++: Generalizable Articulation Reconstruction with Temporal Geometry Constraint via Planar Gaussian Splatting

> [!tip] 核心洞察
> 将3D高斯压缩为平面并利用泰勒展开将法向-深度一致性从离散状态推广到整个运动区间，无需深度真值即可为关节运动提供有效的时间几何约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | REArtGS++：基于平面高斯泼溅和时间几何约束的可泛化关节重建 |
| 英文题名 | REArtGS++: Generalizable Articulation Reconstruction with Temporal Geometry Constraint via Planar Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.17059) · [Project](https://sites.google.com/view/reartgs2/home) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | REArtGS++ |
| Dataset | PARIS Synthetic Objects, ArtGS-Multi + Screw Objects, PARIS Real Objects |

> [!tip] 效果简介
> - PARIS Synthetic Objects 上，CD-w (Chamfer Distance weighted) 1.75 vs 7.67 (REArtGS) (-77.2% (绝对下降5.92，相对误差减少27.6%))。
> - ArtGS-Multi + Screw Objects 上，Axis Ang (Average) 0.55 vs 1.56 (REArtGS, 基于平均估计) (-64.7%)；Part Motion (Average) 0.22 vs ~1.23 (基于表2中其余方法均值估计) (-82.1%)。
> - PARIS Real Objects 上，Axis Ang (Mean) 2.63 vs 44.85 (REArtGS) (-94.1%)。

## 概要

从任意两状态的多视角RGB图像中重建未见关节物体的部件级动态几何并估计关节参数，是视觉理解与机器人操作中的核心挑战。现有方法面临两个关键瓶颈：**关节运动建模依赖类型先验**（仅限旋转或平移），无法处理螺旋关节与多部件物体；**缺乏时间连续的几何约束**，仅依靠离散两状态监督，导致未观测状态的重建质量与关节参数估计精度受限。

REArtGS++ 通过两个核心机制突破上述瓶颈：

1. **解耦螺旋运动建模**：将每个关节的参数解耦为旋转与平移分量，无需关节类型先验，通过部件运动混合（part motion blending）在无监督方式下联合优化部件分割掩码与关节参数，同时支持旋转、平移与螺旋运动。
2. **基于泰勒展开的时间几何约束**：将3D高斯压缩为平面高斯以获得准确法向与无偏深度，利用泰勒一阶展开将法向-深度一致性正则化从离散状态推广到整个运动区间，在无深度真值的条件下为关节运动提供有效的时间连续几何约束。

此外，针对部件边界高斯的分割歧义，引入**局部一致投票机制**（local consistent voting）纠正重叠区域的分割结果。

在PARIS与ArtGS-Multi（含螺旋关节对象）数据集上的实验表明，REArtGS++在所有平均指标上达到最佳或次优：合成物体CD-w误差相比REArtGS降低27.6%，真实物体Axis Ang误差从44.85降至2.63。消融实验证实平面高斯表征、螺旋运动建模与时间几何约束各自对性能提升具有显著贡献。

**方法定位**：REArtGS++属于基于3D高斯泼溅的可泛化关节重建方法，继承自REArtGS（Wu et al., NeurIPS 2025）的几何约束框架，但通过螺旋运动建模与时间连续正则化实现了对任意关节类型与未观测状态的有效泛化，区别于PARIS（Liu et al., ICCV 2023）、DTA（Weng et al., CVPR 2024）等基于神经隐式场的方法，以及ArtGS（Liu et al., ICLR 2025）等依赖关节先验的3DGS方法。



### 问题背景：无先验关节物体的可泛化重建

从多视角RGB图像重建未见过的关节物体（articulated objects）是三维视觉与机器人操作中的核心任务。给定任意两个不同状态下的多视角RGB图像，系统需要同时估计物体的部件分割、关节参数（轴方向、轴位置、运动类型与幅度），并生成任意中间状态的部件级动态表面重建。这一问题的难点在于：关节类型未知（旋转、平移或螺旋）、部件数量与几何结构各异，且训练阶段从未见过该物体实例，要求方法具备强泛化能力。

### 现有方法缺口：关节先验依赖与时间约束缺失

现有方法在关节运动建模上存在两个关键瓶颈。

**瓶颈一：关节类型先验限制。** 基于神经隐式辐射场的方法如 **PARIS**（Liu et al., ICCV 2023）和 **DTA**（Weng et al., CVPR 2024）需要预设关节类型（仅旋转或平移），无法处理螺旋关节（screw joint）等复合运动。基于3D高斯泼溅（3DGS）的方法如 **ArtGS**（Liu et al., ICLR 2025）和 **REArtGS**（Wu et al., NeurIPS 2025）虽然提升了重建效率，但在关节参数估计上仍依赖类型先验，对多部件物体的螺旋运动建模能力不足。这导致在真实场景中面对未知关节类型时，参数估计精度和重建质量显著下降。

**瓶颈二：缺乏时间连续的几何约束。** 现有方法仅利用起始和终止两个离散状态的图像进行监督，缺少对中间未观测状态的有效约束。在仅有两端点监督的条件下，关节参数的优化空间高度欠定，容易收敛到物理上不合理的运动轨迹，导致动态重建在中间状态出现几何畸变。REArtGS引入了法向-深度一致性正则化，但该约束仅在离散状态间成立，未能推广到整个运动时间区间。

### 本文动机：螺旋运动建模与时间几何正则化

针对上述缺口，REArtGS++提出两个核心改进方向：

1. **解耦螺旋运动建模**：将每个关节的运动参数解耦为旋转分量与平移分量，通过部件运动混合（part motion blending）实现无关节类型先验的统一建模，使单一框架同时支持旋转、平移和螺旋关节的参数估计。

2. **时间连续几何正则化**：将3D高斯压缩为平面高斯以获得准确的法向与深度估计，进而利用泰勒一阶展开将法向-深度一致性约束从离散状态推广到整个连续时间区间，为关节运动提供有效的时间几何约束，显著提升未观测状态的动态重建质量。

通过这两个机制，REArtGS++在仅使用两状态多视角RGB图像（无深度监督）的条件下，实现了对未见关节物体的部件级动态重建与精确关节参数估计。



## 核心方法与创新机理

REArtGS++ 针对“仅两状态多视角RGB图像输入下、无关节类型先验的可泛化关节重建”这一瓶颈，提出了三项相互耦合的关键创新，分别从表征、运动建模与时间几何约束三个维度突破现有方法的局限。

### 1. 平面高斯表征：为几何估计提供准确法向与无偏深度

现有基于3D高斯泼溅的关节重建方法（如 **ArtGS**（Liu et al., ICLR 2025）与 **REArtGS**（Wu et al., NeurIPS 2025））使用标准椭球形3D高斯，其法向估计存在系统性偏差，深度图亦非无偏。REArtGS++ 通过尺度损失 $\mathcal{L}_{\mathrm{scale}}$ 强制每个高斯的最小尺度分量趋近于零，将3D高斯压缩为近似平面：

$$\mathcal{L}_{\mathrm{scale}} = \frac{1}{N_{\mathcal{G}}} \sum_i \|\min(s_1, s_2, s_3)\|$$

平面化后的高斯可通过光线-平面交点解析计算无偏深度（Eq. 3），并以高斯平面法向直接作为场景法向估计。这一表征升级是后续时间几何约束得以建立的**必要前提**——只有获得可靠的法向与深度，才能构建有意义的几何正则化信号。消融实验证实，移除平面高斯（回退至标准3DGS）导致所有指标显著恶化（Axis Ang 从 0.41 升至 57.81，Part Motion 从 0.22 升至 35.17），验证了平面表征对几何估计质量的决定性作用。

### 2. 解耦螺旋运动建模：消除关节类型先验依赖

现有方法普遍依赖关节类型先验，仅支持纯旋转（旋转关节）或纯平移（棱柱关节），无法处理现实世界中常见的螺旋关节（如螺丝、瓶盖），也难以泛化至多部件物体。REArtGS++ 将每个关节的运动参数 $\omega$ 解耦为旋转与平移两部分：

$$\omega = \{ \mathbf{q}(\theta, \mathbf{a}), \mathbf{o}, \mathbf{t} \}$$

其中 $\mathbf{q}(\theta, \mathbf{a})$ 为四元数表示的旋转，$\mathbf{o}$ 为旋转轴心，$\mathbf{t}$ 为平移向量。通过以 $t^* = 0.5$ 为正则态进行线性插值：

$$\theta(t) = \frac{(t - t^*)}{t^*} \theta, \quad \mathbf{t}(t) = \frac{(t - t^*)}{t^*} \mathbf{t}$$

该方法无需预先指定关节类型，旋转关节自然对应 $\mathbf{t} \approx 0$，棱柱关节对应 $\theta \approx 0$，螺旋关节则同时具有非零的旋转与平移分量。部件运动通过分割权重混合实现：

$$\mu_i(t) = \sum_{j=1}^{k} m_j \left[ R_j(\mathbf{q}(t)) (\mu_i - \mathbf{o}_j) + \mathbf{o}_j + \mathbf{t}_j(t) \right]$$

这一设计使得关节参数估计与部件分割可在无监督方式下联合优化，从根本上消除了对关节类型先验的依赖。消融实验中，将螺旋运动替换为双四元数（Dual Quaternion）导致 Axis Pos 从 1.18 飙升至 38.17，证实了解耦螺旋模型的必要性。

### 3. 时间几何约束：从离散状态到连续区间的正则化

REArtGS 等先前方法仅依靠两个离散状态的图像监督，缺乏对未观测中间状态的时间连续性约束，导致关节参数估计欠定、动态重建质量受限。REArtGS++ 的核心洞察是：**利用泰勒一阶展开，将法向-深度一致性正则化从离散状态推广到整个运动时间区间**。

具体而言，对于任意时刻 $t$ 的法向图 $\mathbf{N}(\omega, t)$，在正则态 $t_0$ 处进行一阶泰勒近似：

$$\mathbf{N}(\omega, t) \approx \mathbf{N}(\omega, t_0) + \lim_{t \to t_0} \frac{\mathrm{d}N(\omega, t)}{\mathrm{d}t}(t - t_0)$$

其中法向对时间的梯度 $\nabla\mathbf{N}(\omega, t_0)$ 通过有限差分高效近似，避免了对整个时间区间的密集渲染。基于此，构建几何正则化损失 $\mathcal{L}_{\mathrm{geo}}$，强制泰勒近似的法向与深度导出的法向（$\bar{\mathbf{N}}$）在图像梯度加权下保持一致：

$$\mathcal{L}_{\mathrm{geo}} = (1 - \nabla\mathbf{I}(t_0)) \left( \|\bar{\mathbf{N}} - \mathbf{N}\| + \|\nabla\bar{\mathbf{N}} - \nabla\mathbf{N}\| \right)$$

该损失在**无需深度真值**的条件下，为关节运动提供了连续时间区间上的有效几何约束。消融实验表明，移除 $\mathcal{L}_{\mathrm{geo}}$ 后 Axis Ang 从 0.41 升至 4.04，CD-w 从 2.13 升至 5.06；而使用随机时间差（random $\Delta t$）替代基于 $t^*$ 的泰勒近似同样导致性能下降（Axis Ang 升至 5.83），因为早期优化阶段引入额外运动误差。

### 创新耦合关系

上述三项创新并非孤立存在，而是形成因果链条：**平面高斯**提供可靠的法向与深度估计基础，**解耦螺旋运动**定义连续时间上的刚体变换，**泰勒展开几何约束**则将前两者的输出耦合为覆盖整个运动区间的一致性正则化信号。这一“表征-运动-约束”三位一体的设计，使得 REArtGS++ 在仅两状态RGB监督下即可实现高质量部件级动态重建与任意关节类型的参数估计。



REArtGS++ 的整体流程如图 2 所示，其核心目标是：**仅以任意两个状态的 RGB 多视角图像为输入，在不依赖任何外部模型或深度真值的条件下，联合优化部件分割、关节参数与平面高斯表征，最终实现未见关节物体的高质量部件级动态重建与精确关节参数估计**。

### 输入与输出

- **输入**：待重建关节物体在两个不同状态（记为状态 0 与状态 1）下的多视角 RGB 图像，以及对应的相机位姿。
- **输出**：(1) 任意时间状态下的部件级动态表面网格；(2) 各部件的关节参数（旋转轴、旋转角、平移向量与关节中心）；(3) 每个 3D 高斯的部件归属掩码。

### 流水线模块

整个框架由五个关键模块串联构成，各模块之间存在明确的因果依赖关系：

1. **平面高斯初始化与尺度损失**  
   将标准 3D 高斯（椭球体）压缩为近似平面的 2D 高斯。通过最小化高斯尺度矩阵的最小分量（$\mathcal{L}_{\mathrm{scale}}$，Eq. 4），迫使每个高斯退化为平面，从而为后续的法向估计与无偏深度计算提供几何基础。这一步是后续时间几何约束能够成立的前提——只有平面高斯才能通过 Eq. 3 获得准确的法向量与无偏深度图。

2. **部件分割概率估计**  
   对每个高斯 $\mathcal{G}_i$，基于其中心位置与可学习部件中心之间的马氏距离，并辅以 MLP 学习的残差项，计算其属于各部件 $j$ 的软分割掩码 $M_i$。该分割概率直接驱动下游的部件运动混合。

3. **部件运动混合与解耦螺旋运动**  
   这是框架的核心运动建模模块。每个关节的运动参数 $\omega$ 被解耦为旋转与平移两部分（无关节类型先验），并通过分割权重 $m_j$ 对各部件运动进行混合，得到任意时刻 $t$ 的高斯位置（Eq. 5）：
   $$\mu_i(t) = \sum_{j=1}^{k} m_j \left[ R_j(\mathbf{q}(t)) (\mu_i - \mathbf{o}_j) + \mathbf{o}_j + \mathbf{t}_j(t) \right]$$
   其中旋转角度与平移量以 $t^*=0.5$ 为正则态进行线性插值（Eq. 6），避免奇点问题。

4. **时间几何约束（泰勒展开）**  
   利用一阶泰勒展开在 $t_0$ 附近近似任意时刻 $t$ 的法向图（Eq. 8），将法向-深度一致性正则化从离散的两个监督状态推广到整个时间区间 $[0,1]$。几何损失 $\mathcal{L}_{\mathrm{geo}}$（Eq. 10）同时约束法向一致性及其时间梯度，并由图像梯度加权以聚焦于纹理边缘区域。该模块是**将两状态监督信号有效传播至未观测状态的关键机制**。

5. **局部一致投票与网格提取**  
   针对部件边界处高斯分割模糊的问题，通过 k-means 区域聚合与加权概率投票（Eq. 12）修正分割结果。最终根据最大概率将高斯分配到各部件（Eq. 15），并通过 Eq. 5 更新动态高斯位置，提取任意状态的部件级网格。

### 联合优化目标

上述模块通过加权损失函数联合优化（Eq. 14）：
$$\mathcal{L} = \lambda_{\mathrm{render}} \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{scale}} \mathcal{L}_{\mathrm{scale}} + \lambda_{\mathrm{center}} \mathcal{L}_{\mathrm{center}} + \lambda_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} + \lambda_{\mathrm{vote}} \mathcal{L}_{\mathrm{vote}}$$
其中 $\mathcal{L}_{\mathrm{render}}$ 为 RGB 渲染损失（L1 + D-SSIM），$\mathcal{L}_{\mathrm{center}}$ 约束部件中心与高斯分布的一致性，$\mathcal{L}_{\mathrm{geo}}$ 为时间几何正则化，$\mathcal{L}_{\mathrm{vote}}$ 为局部一致投票正则化。所有参数——包括高斯属性、分割掩码与关节参数——在无监督方式下端到端联合优化。

### 与基线方法的架构差异

相比 REArtGS（NeurIPS 2025），REArtGS++ 在三个关键槽位上进行了系统性改进：(1) 关节运动建模从依赖类型先验的旋转/平移扩展为解耦螺旋运动，消除了对关节类型的假设；(2) 高斯表征从标准 3D 椭球压缩为平面高斯，使法向与深度估计从有偏变为准确无偏；(3) 引入基于泰勒展开的时间连续几何约束，填补了 REArtGS 缺乏未观测状态正则化的空白。这三个改进形成因果链：平面高斯提供可靠的几何估计基础 → 解耦螺旋运动提供无先验的运动表达能力 → 时间几何约束将离散监督泛化到连续运动区间。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/002_Figure_2.jpg]]
*Figure 2: Framework of REArtGS++. Our method jointly optimizes part segmentation, joint parameters and planar Gaussians using multi-view RGB images from arbitrary two states, and achieves high-quality part-level mesh reconstruction of any states and accurate joint parameter estimation for an unseen articulated object. “Diff.” denotes the difference approximation*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/001_Figure_1.jpg]]
*Figure 1: Given multi-view RGB images at arbitrary two different states of an unseen articulated objects, our method achieves high-quality part-level dynamic reconstruction and joint parameter estimation, without any external models*



REArtGS++ 的核心管线由五个紧密耦合的模块构成，围绕“平面高斯→部件分割→解耦螺旋运动→时间几何约束→局部投票”的联合优化环路展开。整体框架如 Figure 2 所示。

### 平面高斯初始化与尺度损失

方法首先将标准 3D 高斯压缩为平面（2D 高斯），这是后续获得准确法向与无偏深度的前提。通过最小化高斯最小尺度分量的损失实现：

$$ \mathcal{L}_{\mathrm{scale}} = \frac{1}{N_{\mathcal{G}}} \sum_i \|\min(s_1, s_2, s_3)\| \quad \text{(Eq. 4)} $$

其中 $s_1, s_2, s_3$ 为高斯协方差矩阵的三个尺度分量。压缩为平面后，光线与平面高斯的交点可给出无偏深度估计：

$$ \mathbf{D}(\rho) = \frac{\mathbf{d}}{\mathbf{N}(\rho) \mathbf{K}^{-1} \widetilde{\rho}} \quad \text{(Eq. 3)} $$

其中 $\mathbf{N}(\rho)$ 为像素 $\rho$ 处的法向，$\mathbf{K}$ 为相机内参，$\widetilde{\rho}$ 为像素齐次坐标，$\mathbf{d}$ 为光线原点到平面的距离。这一形式避免了标准 3D 高斯（椭球）在深度估计中的偏差。

### 部件分割概率估计

每个高斯 $\mathcal{G}_i$ 的部件归属掩码 $\mathbf{M}_i$ 通过马氏距离与 MLP 残差联合计算。具体地，学习 $k$ 个部件中心 $\mathbf{O} \in \mathbb{R}^{k \times 3}$，计算高斯位置 $\mu_i$ 到各中心的马氏距离，并通过 MLP 学习残差项以捕捉非线性分割边界。最终掩码经 softmax 归一化，用于后续的部件运动混合。

### 部件运动混合与解耦螺旋运动

这是方法的核心创新之一。给定 $k$ 个部件的分割权重 $m_j$，任意时刻 $t \in [0,1]$ 的高斯位置通过部件运动混合得到：

$$ \mu_i(t) = \sum_{j=1}^{k} m_j \left[ R_j(\mathbf{q}(t)) (\mu_i - \mathbf{o}_j) + \mathbf{o}_j + \mathbf{t}_j(t) \right] \quad \text{(Eq. 5)} $$

其中 $\mathbf{o}_j$ 为第 $j$ 个部件的旋转中心，$R_j(\mathbf{q}(t))$ 为旋转矩阵，$\mathbf{t}_j(t)$ 为平移向量。

关键突破在于关节参数的解耦螺旋建模——将每个关节的参数 $\omega$ 解耦为旋转 $\mathbf{q}(\theta, \mathbf{a})$ 和平移 $\mathbf{t}$，**不依赖任何关节类型先验**（无需指定旋转关节或平移关节）。旋转角度与平移量以 $t^*=0.5$ 为正则态进行线性插值：

$$ \theta(t) = \frac{(t - t^*)}{t^*} \theta, \quad \mathbf{t}(t) = \frac{(t - t^*)}{t^*} \mathbf{t} \quad \text{(Eq. 6)} $$

这种参数化避免了两状态端点处的奇异性，同时使螺旋运动（旋转+平移的耦合）自然可表示。

### 时间几何约束（泰勒展开）

这是方法的第二个核心创新。在仅有两状态 RGB 图像监督的条件下，如何约束未观测中间状态的几何一致性？REArtGS++ 利用泰勒一阶展开将法向-深度一致性从离散状态推广到整个运动区间。

首先，任意时刻 $t$ 的法向图 $\mathbf{N}(\omega, t)$ 在 $t_0$ 附近展开：

$$ \mathbf{N}(\omega, t) \approx \mathbf{N}(\omega, t_0) + \lim_{t \to t_0} \frac{\mathrm{d}N(\omega, t)}{\mathrm{d}t}(t - t_0) \quad \text{(Eq. 8)} $$

为降低计算开销，法向对时间的梯度通过有限差分近似：

$$ \nabla\mathbf{N}(\omega, t_0) \approx \frac{N(\omega, t) - N(\omega, t^*)}{t - t^*} \quad \text{(Eq. 9)} $$

基于此，几何正则化损失强制法向一致性及其时间梯度一致性：

$$ \mathcal{L}_{\mathrm{geo}} = (1 - \nabla\mathbf{I}(t_0)) \left( \|\bar{\mathbf{N}}(\omega, t_0) - \mathbf{N}(\omega, t_0)\| + \|\nabla\bar{\mathbf{N}}(\omega, t_0) - \nabla\mathbf{N}(\omega, t_0)\| \right) \quad \text{(Eq. 10)} $$

其中 $\bar{\mathbf{N}}$ 为由深度图导出的“伪法向”，$\nabla\mathbf{I}(t_0)$ 为图像梯度权重（边缘区域权重低，避免深度不连续处的错误惩罚）。该损失无需深度真值，仅依赖平面高斯的内在几何一致性。

### 局部一致投票

在部件边界区域，高斯的分割概率常出现歧义（多个部件概率相近）。REArtGS++ 提出局部一致投票机制：对每个高斯，在其空间邻域内进行 k-means 区域聚合，以邻域加权概率修正自身的分割结果：

$$ \mathbf{M}_{\mathrm{vote}} = \sum \Phi_{\mathrm{softmax}}(-\delta) \mathbf{M}_i / \sum \mathbf{M}_i \quad \text{(Eq. 12)} $$

其中 $\delta$ 为高斯到聚类中心的距离，$\Phi$ 为 softmax 归一化权重。该机制有效纠正了边界高斯的分割歧义。

### 联合优化总目标

最终训练目标为五项损失的加权组合：

$$ \mathcal{L} = \lambda_{\mathrm{render}} \mathcal{L}_{\mathrm{render}} + \lambda_{\mathrm{scale}} \mathcal{L}_{\mathrm{scale}} + \lambda_{\mathrm{center}} \mathcal{L}_{\mathrm{center}} + \lambda_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} + \lambda_{\mathrm{vote}} \mathcal{L}_{\mathrm{vote}} \quad \text{(Eq. 14)} $$

其中 $\mathcal{L}_{\mathrm{render}}$ 为 L1 + D-SSIM 渲染损失（Eq. 2），$\mathcal{L}_{\mathrm{center}}$ 约束部件中心不远离物体。所有参数——高斯属性、部件分割、关节参数——通过该目标端到端联合优化。优化完成后，动态高斯 $\mathcal{G}^j$ 在任意时刻 $t$ 的位置由 Eq. 5 更新，部件网格通过 $\max(\mathcal{G}_i = m_j)$ 选择提取（Eq. 15）。



## 实验与关键发现

### 核心定量结果

REArtGS++ 在 PARIS 与 ArtGS-Multi 两个基准上均取得最优或次优的关节估计与动态重建结果，且全部实验在无深度监督的公平设置下完成。

**PARIS 数据集（Table 1）**：在合成物体上，REArtGS++ 的加权 Chamfer 距离 CD-w 达到 1.75，相比 REArtGS 的 7.67 绝对下降 5.92，误差降低 27.6%。在真实物体上，轴角度误差 Axis Ang 均值从 REArtGS 的 44.85 降至 2.63，降幅达 94.1%，表明方法对真实世界捕获噪声具有强鲁棒性。其他指标如 CD-s、CD-m 同样在所有物体上达到最优或次优，验证了平面高斯表征与时间几何约束对重建质量的综合增益。

**ArtGS-Multi 与螺旋关节物体（Table 2）**：在多部件物体及两个螺旋关节物体上，REArtGS++ 在所有平均指标上显著领先。轴角度均值 0.55（REArtGS 约 1.56）、轴位置均值 0.50、部件运动误差均值 0.22，均大幅优于 PARIS、DTA、ArtGS 和 REArtGS。这一优势直接源于解耦螺旋运动建模：无需关节类型先验，即可同时处理旋转、平移和螺旋运动，而其他方法对螺旋关节完全失效或误差极大。

### 消融实验

消融实验在 ArtGS-Multi 及两个螺旋关节物体上进行，系统验证了四个关键组件的贡献。

**平面高斯表征（Table 3）**：去除平面高斯（使用标准 3DGS）导致轴角度误差从 0.41 飙升至 57.81，部件运动误差从 0.22 升至 35.17。标准 3DGS 的椭球高斯无法提供准确的法向估计，使得后续的时间几何约束完全失效，充分说明平面压缩是几何正则化的前提。

**解耦螺旋运动（Table 3）**：使用双四元数替代螺旋运动后，轴位置误差从 1.18 升至 38.17。双四元数无法表达螺旋运动的耦合特性，在螺旋关节物体上产生严重的位置漂移，验证了解耦螺旋参数化的必要性。

**时间几何约束（Table 4）**：去除 L_geo 损失后，轴角度误差从 0.41 升至 4.04，CD-w 从 2.13 升至 5.06。这表明仅靠两状态离散监督不足以约束关节参数优化，泰勒一阶展开提供的连续时间法向-深度一致性正则化是关节估计精度的关键保障。

**泰勒近似的 t₀ 选择（Table 4）**：将 t₀ 替换为随机 Δt 后，轴角度误差升至 5.83。随机 Δt 在优化早期引入额外运动误差，破坏法向梯度近似的稳定性，而固定 t₀ = t* 的泰勒展开避免了这一问题。

**局部一致投票（Table 3）**：去除 L_vote 后，CD-w 从 2.13 升至 3.07。投票机制有效纠正了部件边界高斯的分割歧义，减少了重叠区域的模糊重建。

### 定性分析

**动态网格重建**：在 ArtGS-Multi 数据集上（Figure 3），REArtGS++ 在起始与结束状态均生成清晰的部件分割和完整的表面网格，关节位置（红色箭头）准确对应运动轴。相比之下，REArtGS 在螺旋关节物体上出现明显的部件错位和网格断裂。PARIS 数据集上的定性结果（Figure 4、Figure 5）进一步展示了方法对旋转与平移关节的精确建模能力。

**消融可视化**（Figure 6）：去除投票与几何正则化后，分割渲染结果在部件边界出现严重混叠，相邻部件的颜色相互渗透，直观验证了 L_vote 和 L_geo 对边界分割的协同作用。

**真实场景泛化**（Figure 7）：在真实世界物体上，REArtGS++ 成功重建出部件级表面网格，分割边界清晰且关节运动合理，验证了方法从合成数据到真实场景的迁移能力。

### 失败模式与局限性

尽管 REArtGS++ 在多数场景下表现出色，仍存在两个主要局限：

1. **透明物体重建困难**：平面高斯假设与透明材质的光学特性不兼容，导致透明表面的法向与深度估计失效。这一问题的根源在于平面高斯无法建模折射与透射效应，需要结合深度估计与透明材质建模来解决。

2. **相机位姿对齐要求**：方法假设两状态间的相机位姿精确对齐，但在真实捕获数据中通常无法直接满足。当前框架未包含相机位姿联合优化，限制了在完全无标定真实数据上的直接应用。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on PARIS dataset. We implement all methods without depth supervision for fair comparison. Axis Pos results are measured by mm. ”-” indicates the object containing only prismatic joints. We highlight best and second best results*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on ArtGS-Multi dataset with additional 2 objects exhibiting screw joints. Due to the large number of parts, we report the average metric for all movable parts. We implement all methods without depth supervision for fair comparison. Part motion error for screw objects is decomposed by translation|rotation. Axis Pos results are measured by mm. ‘-’ indicates the object contains only prismatic joints. We highlight best and second best results*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/011_Table_3.jpg]]
*Table 3: Ablation of key componets. We report the average results on ArtGS-Multi and 2 screw-joint objects. Axis Pos results are measured by mm. “GS” and “dis” denote Gaussians and distance respectively*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/009_Table_4.jpg]]
*Table 4: Ablation of temporal geometry constraints. We report the average results on ArtGS-Multi and 2 screw-joint objects*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/004_Figure_3.jpg]]
*Figure 3: The qualitative results of dynamic surface reconstruction at start state and end state on ArtGS-Multi dataset. We show both part segmentation and surface meshes for best comparison. The red arrows represent joints*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/007_Figure_4.jpg]]
*Figure 4: The qualitative results of dynamic surface reconstruction at start state and end state on PARIS dataset. We show both articulated modeling and surface meshes for best comparison*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/006_Figure_5.jpg]]
*Figure 5: The qualitative results of dynamic surface reconstruction at start state and end state on PARIS dataset. We show both articulated modeling and surface meshes for best comparison*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative results for the ablation of voting and geometric regularization. We use segmentation rendering results for intuitive visualization*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2511_17059/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative results of part-level surface reconstruction at both start and end states on real-world objects*



## 定位与知识库关联

### 1. 问题域定位：可泛化关节重建的瓶颈

REArtGS++ 面向的是**无先验、仅两状态多视角RGB输入的可泛化关节物体重建**。该任务的真实瓶颈在于：现有方法（如表征学习路线和3D高斯泼溅路线）普遍依赖关节类型先验（仅能处理旋转或平移关节），无法建模螺旋关节与多部件物体，且缺乏对未观测中间状态的时间几何约束，导致关节参数估计与动态重建质量受限。

从知识库定位看，本工作处于**3D高斯泼溅（3DGS）× 关节物体重建**的交叉点，其直接前驱包括：

- **PARIS** (Liu et al., ICCV 2023)：基于神经隐式辐射场（NeRF）的关节重建，通过部件运动场实现可泛化重建，但受限于隐式表征的渲染效率与几何精度。
- **DTA** (Weng et al., CVPR 2024)：基于隐式神经表示的关节物体数字孪生，进一步提升了部件级重建的精度，但同样依赖关节类型先验。
- **ArtGS** (Liu et al., ICLR 2025)：首次将3DGS引入关节重建，利用显式高斯表征提升了渲染速度与几何质量，但运动建模仍局限于旋转/平移关节。
- **REArtGS** (Wu et al., NeurIPS 2025)：在ArtGS基础上引入几何与运动约束，增强了重建精度，但仍未突破关节类型先验的限制，且缺乏时间连续的正则化。

REArtGS++ 的核心推进在于**解耦螺旋运动建模**与**时间连续几何正则化**，将上述路线的能力边界从“已知关节类型”拓展至“无先验任意关节”，同时将几何约束从离散两状态推广至整个运动区间。

### 2. 技术路线对比：关键设计槽位的改变

REArtGS++ 相对于基线方法在四个关键设计槽位上做出了实质性改变：

| 设计槽位 | 基线方法 | REArtGS++ | 因果作用 |
|----------|----------|-----------|----------|
| **关节运动建模** | 依赖关节类型先验，仅支持旋转或平移（PARIS/DTA/ArtGS/REArtGS） | 解耦的螺旋运动建模，无关节类型先验，同时支持旋转、平移与螺旋运动 | 消除类型先验依赖，使方法可泛化至任意关节类型 |
| **高斯表征** | 标准3D高斯（椭球），法向与深度估计有偏（ArtGS/REArtGS） | 压缩为平面的2D高斯，获得准确法向与无偏深度 | 为时间几何约束提供可靠的几何基元 |
| **时间几何约束** | 无时间连续正则化，仅依靠离散两状态监督（所有基线） | 基于泰勒一阶展开的法向-深度一致性正则化，覆盖连续时间区间 | 为未观测状态的动态重建提供有效几何监督 |
| **部件分割后处理** | 直接使用分割概率，重叠区域模糊（REArtGS） | 局部一致投票机制，纠正边界高斯的分割歧义 | 提升部件边界的分割精度与网格提取质量 |

这些改变的因果链条是：**平面高斯 → 准确法向与无偏深度 → 泰勒展开下的时间连续几何正则化 → 无先验螺旋运动参数的有效优化**。消融实验（Table 3）验证了这一链条的每个环节：去除平面GS（使用标准3DGS）导致 Axis Ang 从 0.41 恶化至 57.81，Part Motion 从 0.22 恶化至 35.17；去除时间几何约束（L_geo）导致 Axis Ang 升至 4.04，CD-w 升至 5.06。

### 3. 方法适用边界与局限

**适用边界**：
- 输入要求：同一物体在任意两个不同状态下的多视角RGB图像，且两状态间的相机位姿需精确对齐。
- 关节类型：无先验限制，可处理旋转、平移及螺旋关节。
- 物体复杂度：已验证可处理多部件物体（ArtGS-Multi数据集）及螺旋关节物体。

**已知局限**（论文明确指出的失效模式）：
1. **透明物体重建困难**：平面高斯假设与透明/半透明材质的光学特性不兼容，导致透明表面的重建质量下降。这是3DGS类方法的共性局限，但平面高斯进一步加剧了该问题（因为透明表面无法提供可靠的法向估计）。
2. **相机位姿对齐依赖**：方法假设两状态间的相机位姿已精确对齐，但在真实世界捕获数据中，这一条件通常无法直接满足，需要外部标定或额外的位姿优化模块。

**弱证据提示**（需人工验证）：
- 论文未明确讨论方法对**非刚性部件变形**（如柔性连接）的泛化能力，螺旋运动模型假设部件为刚体运动。
- 对于**链式或图结构关节系统**（如机器人操作臂），论文仅在开放问题中提及扩展可能性，未提供实验验证。

### 4. 开放问题与后续方向

论文明确提出的开放问题包括：
1. **透明材质建模**：如何结合深度估计与透明材质建模来处理透明表面的感知与重建？
2. **相机位姿联合优化**：如何在真实世界数据中联合优化两状态的相机位姿而不依赖外部标定？
3. **复杂关节拓扑扩展**：能否扩展至更复杂的链式或图结构关节系统，以适应机器人操作中的通用对象？

从知识库演进角度看，REArtGS++ 为后续工作留下了以下可推进方向：
- **与基础模型结合**：当前方法从零开始优化，未来可探索利用预训练的分割或深度估计模型提供初始化或弱监督。
- **单目/稀疏视角扩展**：当前依赖多视角输入，向单目或稀疏视角的泛化是实用化的关键瓶颈。
- **动态场景扩展**：方法假设静态背景与独立运动的关节物体，向多物体交互场景的扩展需要引入物体间遮挡与碰撞建模。



## 原文 PDF

![[paperPDFs/CVPR_2026/REArtGS_Generalizable_Articulation_Reconstruction_with_Temporal_Geometry_Constraint_via_Planar_Gaussian_Splatting.pdf]]
