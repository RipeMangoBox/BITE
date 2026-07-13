---
title: "4DSurf: High-Fidelity Dynamic Scene Surface Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/4DSurf_High_Fidelity_Dynamic_Scene_Surface_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- 4HFDSSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用高斯速度场导出SDF（有向距离函数）流，将其与由深度图估计的SDF流对齐，以此约束高斯运动与表面演化的时间一致性。
primary_logic: 将静态SDF流理论扩展到动态高斯表示：通过高斯速度场预测每个高斯的刚体运动，进而推导出SDF流（即表面随时间的变化率），并与从渲染深度图近似估计的SDF流进行匹配，从而强制整个表面在时间上光滑演化。
claims:
- 提出了高斯变形诱导的SDF流正则化，约束高斯运动与演化表面对齐，实现时间一致性重建。
- 在Hi4D和CMU Panoptic两个数据集上分别以49%和19%的Chamfer距离提升超越现有最优方法。
- 重叠段分割策略有效处理大形变，缓解误差累积，提升可扩展性。
- CMU Panoptic Band1 上 Chamfer Overall (mm) ↓ = 12.7
---

# 4DSurf: High-Fidelity Dynamic Scene Surface Reconstruction

> [!tip] 核心洞察
> 将静态SDF流理论扩展到动态高斯表示：通过高斯速度场预测每个高斯的刚体运动，进而推导出SDF流（即表面随时间的变化率），并与从渲染深度图近似估计的SDF流进行匹配，从而强制整个表面在时间上光滑演化。

| 字段 | 内容 |
|------|------|
| 中文题名 | 4DSurf：高保真动态场景表面重建 |
| 英文题名 | 4DSurf: High-Fidelity Dynamic Scene Surface Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.28064) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 4DSurf |
| Dataset | CMU Panoptic Band1, CMU Panoptic Ian3, Hi4D Cheers37, Hi4D Basketball13 |

> [!tip] 效果简介
> - CMU Panoptic Band1 上，Chamfer Overall (mm) ↓ 12.7 vs 16.0 (Dynamic-2DGS) (-3.3)。
> - CMU Panoptic Ian3 上，Chamfer Overall (mm) ↓ 10.5 vs 12.5 (Dynamic-2DGS) (-2.0)。
> - Hi4D Cheers37 上，Chamfer Overall (cm) ↓ 0.47 vs 1.81 (Sparse2DGS) (-1.34)。

## 概要

动态场景的高保真表面重建是计算机视觉中的一项核心挑战，尤其当输入仅为稀疏多视角视频时，现有方法在处理大形变、多物体交互场景时往往面临表面抖动、时间不一致以及重建质量严重退化的问题。**4DSurf** 针对这一瓶颈，提出了一套端到端的动态表面重建框架，其核心思想是：**将静态场景的SDF流理论扩展到动态高斯表示中，通过约束高斯运动与表面演化的一致性，实现时间上光滑且几何精确的重建。**

### 核心问题与动机

当前基于高斯泼溅（Gaussian Splatting）的动态重建方法，如 **Dynamic-2DGS**（Zhang et al., ACM MM 2025）和 **Space-Time-2DGS**（Wang et al., arXiv 2024），主要面向小形变或单物体场景设计。当场景中发生大幅度非刚体运动时，这些方法的表面重建结果会出现严重的帧间抖动和几何失真，时间一致性难以保证。其根本原因在于：**缺乏一种机制将高斯的运动与底层表面的演化显式地关联起来**，导致变形场的学习缺乏几何层面的约束。

### 方法定位与关键思路

4DSurf 在方法谱系上属于基于2D高斯泼溅的动态表面重建路线，但引入了三个关键创新点，形成了一条从“运动建模—时间正则化—序列处理”的完整技术链路：

1. **高斯速度场**：摒弃了直接预测绝对变形的传统做法，转而预测每个高斯在规范空间中的线性速度、角速度和膨胀速度，以刚体运动参数化描述变形。这一设计不仅更符合物理直觉，也为后续的SDF流推导提供了数学基础。

2. **SDF流正则化**：这是本文最核心的理论贡献。从高斯速度场出发，推导出表面随时间的变化率——即SDF流（有向距离函数流），并将其与从渲染深度图中近似估计的SDF流进行匹配。该正则化损失强制高斯的运动与观察到的几何变化保持一致，从而在训练过程中自然地抑制表面抖动，提升时间稳定性。

3. **重叠段分割与增量运动调整**：为应对长序列中的大形变和误差累积，4DSurf 将视频划分为具有重叠虚拟时间步的多个短段，每段仅处理小形变。段间通过共享的虚拟时间步传递几何信息，同时采用LoRA低秩适配对高斯速度场进行增量微调，在保持重建精度的同时大幅压缩存储开销。

### 主要结果

在两个公开的动态场景数据集上，4DSurf 以显著优势超越了现有最优方法：
- 在 **Hi4D** 数据集上，Chamfer距离整体指标平均提升 **49%**；
- 在 **CMU Panoptic** 数据集上，Chamfer距离整体指标平均提升 **19%**。

消融研究进一步验证了各模块的贡献：SDF流正则化与高斯速度场的组合使6个Hi4D场景的平均Overall从1.49降至1.02；重叠段分割策略进一步将指标推至0.67；而采用秩64的LoRA增量运动调整（IMT-64）在几乎不损失精度的情况下（Overall 0.70），有效控制了运动场参数的存储增长。在时间稳定性方面，4DSurf 的Overall标准偏差最低仅0.18，远优于 **Sparse2DGS** 的0.68和 **Dynamic-2DGS** 的1.19，充分证明了该方法在抑制表面抖动上的有效性。



### 动态表面重建的挑战

从稀疏多视角视频中重建动态场景的高保真表面，是计算机视觉与图形学中长期存在的核心难题。该任务要求同时估计随时间变化的几何形状与外观，其难度在于：可用视角极其有限（通常仅4–6个摄像头），而场景中的物体可能经历大幅度的非刚性形变（如人体运动、交互动作）。现有方法在应对此类场景时暴露出两个关键瓶颈：

**表面时间一致性差。** 基于高斯泼溅（Gaussian Splatting）的动态重建方法（如 **Dynamic-2DGS** (Zhang et al., ACM MM 2025)、**Space-Time-2DGS** (Wang et al., arXiv 2024)）虽然在渲染质量和效率上表现出色，但其变形建模缺乏对表面随时间演化规律的显式约束。这导致重建表面在连续帧之间出现严重抖动——即使渲染图像看起来平滑，提取出的网格却存在明显的时间不一致性。

**大形变场景可扩展性不足。** 现有方法通常将整个视频序列输入单一变形场，期望网络学习从起始帧到任意目标帧的绝对变形。当场景形变幅度较大时，这种策略会遭遇误差累积：变形场在远离规范帧的时间步上预测精度急剧下降，且训练过程难以收敛。这使得多数工作局限于单物体小形变场景，无法推广到多人物体交互、剧烈运动等通用动态场景。

### 现有方法的缺口

从方法谱系来看，动态表面重建可大致分为两条技术路线：

- **基于NeRF的隐式方法：** 以 **NDR** (Cai et al., NeurIPS 2022) 和 **Neural SDF-Flow** (Mao et al., ICLR 2024) 为代表，通过神经网络隐式建模有向距离函数（SDF）及其时间演化。Neural SDF-Flow 率先将静态SDF流理论引入动态表面重建，利用场景流约束表面变化。然而，这类方法依赖体积渲染，计算开销大，且难以处理稀疏视角下的精细几何细节。

- **基于高斯泼溅的显式方法：** 以 **4DGS** (Wu et al., CVPR 2024)、**SC-GS** (Huang et al., CVPR 2024) 和 **GauSTAR** (Zheng et al., CVPR 2025) 为代表，用显式高斯原语表示场景，通过变形场驱动高斯运动。这类方法渲染速度快，但变形场通常直接预测绝对位移，缺乏对表面几何一致性的约束。**Sparse2DGS** (Wu et al., CVPR 2025) 虽在静态场景中表现优异，但逐帧独立应用时完全忽略了时间关联，无法保证动态表面的连贯性。

关键缺口在于：**尚无方法将SDF流的理论优势与高斯泼溅的表示效率相结合**，从而在保持高渲染质量的同时，强制动态表面在时间上光滑演化。

### 本文动机

4DSurf 的核心动机是填补上述缺口。我们观察到：静态SDF流理论表明，表面随时间的变化率等于负的场景流在表面法向上的投影——这一关系为约束表面时间一致性提供了严格的数学基础。然而，将其直接应用于动态高斯表示面临两个根本性问题：

1. **如何从离散高斯运动推导连续的SDF流？** 高斯泼溅使用离散原语表示场景，其运动由变形场驱动，但SDF流定义在连续表面上。需要建立从高斯速度到表面演化速率的可微映射。

2. **如何处理大形变下的误差累积？** 即使有了时间正则化，单一变形场在长序列大形变场景中仍会失效。需要设计一种机制，将长序列分解为可管理的子问题，同时保持段间几何信息传递。

针对第一个问题，我们提出**高斯速度场**——预测每个高斯的线性速度、角速度和膨胀速度，从而导出其刚体运动。基于此，可解析计算高斯运动诱导的SDF流，并与从渲染深度图近似估计的SDF流进行匹配，形成**SDF流正则化**。针对第二个问题，我们设计**重叠段分割策略**，将视频序列划分为带虚拟时间步的重叠段，每段仅处理小幅度形变，并通过共享时间步增量传递几何信息。配合**增量运动调整（IMT）**，使用LoRA对速度场进行段间低秩适配，有效控制存储开销。

通过在 CMU Panoptic 和 Hi4D 两个多人物体大形变数据集上的系统验证，4DSurf 在 Chamfer 距离指标上分别以 **49%** 和 **19%** 的优势超越现有最优方法，同时显著提升了重建表面的时间稳定性。



## 核心方法与创新机理

4DSurf 的核心创新围绕一个因果机制展开：**利用高斯速度场导出 SDF 流，并将其与由渲染深度估计的 SDF 流对齐**，从而在动态高斯泼溅框架中强制表面演化的时间一致性。这一机制直接针对现有方法的瓶颈——大形变下的表面抖动和时间不一致——提供了系统性的解决方案。具体体现在以下三个关键设计变更上：

### 1. 从绝对变形到场驱动运动：高斯速度场

现有动态高斯方法（如 **Dynamic-2DGS** (Zhang et al., ACM MM 2025)、**Space-Time-2DGS** (Wang et al., arXiv 2024)）通常使用变形场直接预测每个高斯在每一时刻的绝对位移。4DSurf 将其替换为**高斯速度场（Gaussian Velocity Field）**，预测三种运动参数：线性速度 $\mathbf{v}$、角速度 $\boldsymbol{\omega}$ 和膨胀速度 $e$。这一变更的深层动机在于：速度场不仅描述了运动本身，更使得**运动与表面几何变化之间建立了可微的解析联系**，为后续的 SDF 流正则化提供了理论桥梁。

### 2. 时间一致性的显式约束：SDF 流正则化

这是 4DSurf 最关键的创新。静态 SDF 流理论指出，表面随时间的变化率等于负的场景流在表面法向上的投影：

$$\frac{\partial s}{\partial t} = -(\boldsymbol{\omega} \times \hat{\mathbf{x}} + \mathbf{v})^\top \mathbf{n}(\hat{\mathbf{x}})$$

4DSurf 将该理论扩展到动态高斯表示：从高斯速度场导出的 SDF 流 $\mathbf{f}$ 描述了高斯运动所隐含的表面演化速率；同时，从渲染深度图近似估计的 SDF 流 $\tilde{\mathbf{f}}$ 反映了实际观察到的几何变化。通过 L1 损失 $\mathcal{L}_{\mathrm{flow}} = \sum_i |\mathbf{f}_i^t - \tilde{\mathbf{f}}_i^t|$ 强制两者一致，该方法**将表面重建从逐帧独立优化提升为时空联合约束**，从根本上解决了大形变下的表面抖动问题。基线方法缺乏此类显式的时间正则化机制。

### 3. 大形变场景的可扩展处理：重叠段分割与增量运动调整

当动态序列包含大幅度运动时，单一变形场难以覆盖整个形变空间，导致误差累积。4DSurf 引入两个协同的设计变更：

- **重叠段分割（Overlapping Segment Partitioning）**：将序列划分为含 $K+1$ 个时间步的重叠段，每段仅需处理小形变。相邻段通过共享一个虚拟时间步传递几何信息，确保段间连续性。这与基线方法在整个序列上训练单一变形场的策略形成对比。

- **增量运动调整（Incremental Motion Tuning, IMT）**：后续段的高斯速度场参数在前一段基础上通过 LoRA 进行低秩更新 $\boldsymbol{\theta}^N = \boldsymbol{\theta}^{N-1} + \mathbf{A}^N \mathbf{B}^N$，而非重新初始化。这在保持重建精度的同时，显著降低了运动场的存储开销。

这三个变更槽位协同作用：速度场提供了运动与几何的解析关联，SDF 流正则化利用该关联约束时间一致性，段分割与 IMT 则确保该框架能扩展到任意长度的复杂动态序列。消融实验证实，仅引入高斯速度场和 SDF 流正则化即可将 6 个 Hi4D 场景的平均 Overall Chamfer 距离从 1.49 降至 1.02，进一步加入段分割策略后降至 0.67，验证了每个创新模块的独立贡献。



4DSurf 的整体训练流程围绕**重叠段分割**展开，将长序列动态场景重建分解为多个可控的局部子问题，并通过**高斯速度场**与**SDF 流正则化**协同约束时间一致性。图 2(a) 给出了完整的 pipeline 示意。

**序列分段与几何传递。** 输入为一组稀疏多视角视频。首先将整个序列划分为 $N$ 个重叠段，每段包含 $K+1$ 个时间步，其中相邻段共享一个虚拟时间步。第一段以前景掩码构建的视觉外壳点云作为高斯初始位置，后续段则从前一段的共享时间步继承几何信息，实现增量式传递。这种设计将每个段内的形变控制在较小范围内，有效缓解大形变场景下的误差累积。

**段内训练。** 每个段维护独立的规范空间与高斯速度场 $\mathcal{F}_\theta$。对于段内任意时间步，速度场预测每个高斯的线性速度 $\mathbf{v}$、角速度 $\boldsymbol{\omega}$ 和膨胀速度 $e$，进而通过刚体变换将规范空间的高斯变换到当前帧。渲染模块基于 2D Gaussian Splatting 生成 RGB 图像、深度图和法向图，并计算 SDF 近似值。

**SDF 流正则化。** 这是框架的核心约束模块。一方面，从高斯速度场推导出运动诱导的 SDF 流 $\mathbf{f}$——即表面随时间的变化率等于负的场景流在法向上的投影；另一方面，从渲染深度图的时间差分估计几何变化诱导的 SDF 流 $\tilde{\mathbf{f}}$。通过 L1 损失 $\mathcal{L}_{\mathrm{flow}} = \sum_i |\mathbf{f}_i^t - \tilde{\mathbf{f}}_i^t|$ 强制两者一致，从而约束高斯运动与演化表面对齐，实现时间一致的重建。

**增量运动调整。** 为降低多段场景的存储开销，第 $N$ 段的高斯速度场参数在前一段基础上仅学习低秩更新：$\boldsymbol{\theta}^N = \boldsymbol{\theta}^{N-1} + \mathbf{A}^N \mathbf{B}^N$，其中 $\mathbf{A}^N \in \mathbb{R}^{d \times r}$、$\mathbf{B}^N \in \mathbb{R}^{r \times d}$，秩 $r \ll d$。只需存储每段的低秩增量矩阵，即可在几乎不损失重建精度的前提下大幅压缩参数量。

**训练目标与网格提取。** 总损失函数联合光度损失、法向一致性损失、深度畸变损失、SDF 流损失和掩码损失：$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{img}} + \lambda_1 \mathcal{L}_{\mathrm{n}} + \lambda_2 \mathcal{L}_{\mathrm{d}} + \lambda_3 \mathcal{L}_{\mathrm{flow}} + \lambda_4 \mathcal{L}_{\mathrm{m}}$。训练完成后，通过 TSDF 体素融合所有训练视角的 RGB-D 图像，提取最终的动态表面网格。

各模块间的因果链路清晰：段分割将大形变拆解为局部小形变 → 速度场建模刚体运动 → SDF 流正则化保证表面光滑演化 → IMT 压缩多段存储 → TSDF 融合输出网格。这一设计使得 4DSurf 在稀疏视角、多物体大形变场景下仍能产出时间一致的高保真动态表面。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/002_Figure_2.jpg]]
*Figure 2: Overview: (a) Overall Training Pipeline. We first divide the sequence into N segments, each containing K+1 timesteps with one overlapping virtual timestep. For the*



### 高斯速度场与变形建模

4DSurf 摒弃了直接预测绝对变形的传统变形场，转而采用**高斯速度场**（Gaussian Velocity Field）$\mathcal{F}_\theta$ 对每个高斯原语的运动进行建模。对于规范空间中的每个2D高斯，该速度场预测三类运动参数：

- **线速度** $\mathbf{v} \in \mathbb{R}^3$
- **角速度** $\boldsymbol{\omega} \in \mathbb{R}^3$
- **膨胀速度** $e \in \mathbb{R}$（控制高斯在切平面内的缩放）

给定时间步 $t$，高斯的刚体变换通过速度的积分获得：旋转由角速度 $\boldsymbol{\omega}$ 的指数映射 $\mathrm{R}^t$ 给出，平移由线速度 $\mathbf{v}$ 的积分给出。这一设计将变形建模从“逐帧预测绝对位置”转变为“预测运动趋势”，为后续的 SDF 流正则化提供了运动学基础。

### SDF 流理论推导

SDF 流（Signed Distance Function Flow）描述的是表面随时间的变化率。其核心理论源于静态 SDF 流公式，4DSurf 将其推广至动态高斯表示。

**点级 SDF 流**：对于场景中一个局部刚体运动的点 $\hat{\mathbf{x}}$，其 SDF 值 $s$ 随时间的变化率与场景流（scene flow）和表面法向 $\mathbf{n}(\hat{\mathbf{x}})$ 的关系为：

$$
\frac{\partial s}{\partial t} = \operatorname*{lim}_{\Delta t\to 0} \frac{\Delta s}{\Delta t} = -\frac{\partial \hat{\mathbf{x}}}{\partial t}^\top \mathbf{n}(\hat{\mathbf{x}}) = -(\boldsymbol{\omega}\times\hat{\mathbf{x}} + \mathbf{v})^\top \mathbf{n}(\hat{\mathbf{x}})
$$

该公式表明：**表面 SDF 的时间导数等于负的场景流在表面法向上的投影**。

**高斯运动诱导的 SDF 流**：将上述理论应用到高斯表示中，对于规范空间中一点 $\mathbf{x}$，其在时间 $t$ 经高斯速度场变换后的 SDF 流为：

$$
\mathbf{f} = -(\boldsymbol{\omega}\times \mathrm{R}^t \mathbf{x} + \mathbf{v})^\top \mathbf{n}(\mathrm{R}^t \mathbf{x})
$$

其中 $\mathrm{R}^t \mathbf{x}$ 是该点在时刻 $t$ 的位置，$\mathbf{n}(\mathrm{R}^t \mathbf{x})$ 为该点处的表面法向。这个 $\mathbf{f}$ 完全由高斯速度场的参数决定，代表了模型内部“认为”的表面应该如何演化。

### 逐像素 SDF 近似与几何 SDF 流

为获得可监督的 SDF 流信号，4DSurf 从渲染的深度图中近似估计每个高斯中心的 SDF 值。对于相机平面上的像素 $\mathbf{p}^*$（被某高斯覆盖），该高斯中心 $\mu_i^t$ 的近似 SDF 值为：

$$
\widetilde{s}(\mu_i^t, t) = \hat{D}(\mathbf{p}^*, t) - d(\mu_i^t, t)
$$

其中 $\hat{D}(\mathbf{p}^*, t)$ 是像素 $\mathbf{p}^*$ 处的渲染深度，$d(\mu_i^t, t)$ 是高斯中心到相机平面的距离。直观上，若高斯中心位于表面之上，$\widetilde{s} > 0$；若在表面之下，$\widetilde{s} < 0$。

对近似 SDF 求时间导数，得到**由几何观测估计的 SDF 流**：

$$
\widetilde{\mathbf{f}}_i^t = \frac{\partial \widetilde{s}(\pmb{\mu}_i^t, t)}{\partial t} = \frac{\partial \hat{D}(\mathbf{p}^*, t)}{\partial t} - \frac{\partial d(\pmb{\mu}_i^t, t)}{\partial t}
$$

### SDF 流正则化损失

核心正则化项通过 L1 损失强制高斯运动诱导的 SDF 流与几何观测估计的 SDF 流一致：

$$
\mathcal{L}_{\mathrm{flow}} = \sum_i |\mathbf{f}_i^t - \tilde{\mathbf{f}}_i^t|
$$

这一损失直接约束**高斯的运动趋势必须与表面几何的实际演化相匹配**，从而抑制表面抖动，实现时间一致的重建。

### 重叠段分割策略

为处理长序列中的大形变并缓解误差累积，4DSurf 将视频序列划分为 $N$ 个**重叠段**（Overlapping Segment Partitioning）。每段包含 $K+1$ 个时间步（$K=5$），其中最后一个时间步作为**虚拟时间步**与下一段共享。该虚拟时间步传递几何信息：前一段的规范空间高斯和速度场参数被传递至下一段，作为其初始化的基础。

每段维护独立的规范空间和高斯速度场，仅需处理段内的小形变，显著降低了单段优化的难度。

### 增量运动调整 (IMT)

为减少多段带来的存储开销，4DSurf 引入**增量运动调整**（Incremental Motion Tuning, IMT）。对于第 $N$ 段（$N \geq 2$），其高斯速度场参数 $\pmb{\theta}^N$ 在前一段参数 $\pmb{\theta}^{N-1}$ 的基础上进行低秩更新：

$$
\pmb{\theta}^N = \pmb{\theta}^{N-1} + \Delta\pmb{\theta}^N, \quad \Delta\pmb{\theta}^N = \mathbf{A}^N \mathbf{B}^N
$$

其中 $\mathbf{A}^N \in \mathbb{R}^{d \times r}$，$\mathbf{B}^N \in \mathbb{R}^{r \times d}$，秩 $r \ll d$。使用 LoRA 秩 64 时，IMT 在几乎不损失精度的情况下（Overall 0.70 vs 0.67）有效抑制了存储增长（Figure 7 左图）。

### 总损失函数

联合训练目标为各损失的加权和：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{img}} + \lambda_1 \mathcal{L}_{\mathrm{n}} + \lambda_2 \mathcal{L}_{\mathrm{d}} + \lambda_3 \mathcal{L}_{\mathrm{flow}} + \lambda_4 \mathcal{L}_{\mathrm{m}}
$$

其中 $\mathcal{L}_{\mathrm{img}}$ 为光度损失，$\mathcal{L}_{\mathrm{n}}$ 为法向一致性损失，$\mathcal{L}_{\mathrm{d}}$ 为深度畸变损失，$\mathcal{L}_{\mathrm{flow}}$ 为 SDF 流正则化损失，$\mathcal{L}_{\mathrm{m}}$ 为掩码损失。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/003_Figure_3.jpg]]
*Figure 3: Incremental Motion Tuning (IMT). After training the Gaussian Velocity Field of the*



## 实验与关键发现

### 主实验结果

4DSurf 在两个公开动态场景数据集——**CMU Panoptic**（4个场景）和 **Hi4D**（6个场景）——上进行了系统评估，采用 Chamfer Distance（Accuracy ↓、Completeness ↓、Overall ↓）作为核心指标，并与多种动态/静态表面重建及新视角合成方法对比。

**CMU Panoptic 数据集**（Table 1）：4DSurf 在所有场景的 Overall 指标上均取得最优。以 Band1 场景为例，4DSurf 的 Overall 为 12.7 mm，相比最强基线 **Dynamic-2DGS**（Zhang et al., ACM MM 2025）的 16.0 mm 降低 20.6%；在 Ian3 场景上，4DSurf 达到 10.5 mm，较 Dynamic-2DGS 的 12.5 mm 降低 16.0%。值得注意的是，逐帧应用静态方法 **Sparse2DGS**（Wu et al., CVPR 2025）在 Band1 上的 Overall 高达 22.5 mm，表明其缺乏时间约束导致表面抖动严重。

**Hi4D 数据集**（Table 2）：该数据集包含大形变多人体交互场景，挑战性更大。4DSurf 在 Cheers37 场景上 Overall 仅 0.47 cm，相比 Sparse2DGS 的 1.81 cm 提升 74%（原文宣称 49% 为六场景平均提升）；在 Basketball13 场景上 Overall 为 0.70 cm，较 Dynamic-2DGS 的 2.27 cm 提升 69%。基于 NeRF 的 **Neural SDF-Flow**（Mao et al., ICLR 2024）在 Hi4D 上表现不佳（Cheers37 Overall 3.33 cm），说明其隐式表示难以应对稀疏视角下的大形变表面追踪。

### 消融研究

Table 3 在 Hi4D 六场景上系统拆解了各组件的贡献（取 Acc、Comp、Overall 三指标均值）：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/009_Table_3.jpg]]
*Table 3: Ablation Studies on the Hi4D dataset [54]. We calculate the average of the three metrics (Acc, Comp, and Overall) for the six scenes. GVF: Gaussian Velocity Field. SF-Reg: SDF-Flow Regularization. I-Segment: Independent Segment Partitioning. O-Segment: Overlapping Segment Partitioning. IMT-64: Incremental Motion Tuning with LoRA rank 64*

- **基线（a）**：采用变形场直接预测绝对变形的标准流水线，六场景平均 Overall 为 1.49 cm。
- **+ 高斯速度场 + SDF流正则化（b）**：将变形场替换为高斯速度场并引入 SDF 流正则化后，平均 Overall 降至 1.02 cm，降幅达 31.5%，验证了速度场建模与流一致性约束对时间稳定性的关键作用。
- **+ 独立段分割（c）**：引入分段训练策略后，平均 Overall 进一步降至 0.68 cm，表明将长序列分解为小形变段可有效缓解误差累积。
- **+ 重叠段分割（d）**：在段间增加虚拟重叠时间步传递几何信息，平均 Overall 稳定在 0.67 cm，虽数值提升有限，但该设计保证了段间几何连续性，避免独立段间的不一致跳变。
- **+ 增量运动调整 IMT-64（e）**：采用 LoRA 秩 64 的增量微调，平均 Overall 为 0.70 cm，几乎无损于完整训练（d），同时显著降低了存储开销。

Figure 6 展示了 Cheers37 场景上各消融配置的定性对比：基线（a）表面存在明显孔洞和抖动；加入 SDF 流正则化（b）后表面完整性大幅改善；重叠段分割（d）进一步消除了段边界处的不连续伪影。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative comparison of each ablation study on scene Cheers37. Subscripts correspond to rows in Tab. 3. (a): Gaussian Velocity Field with normal & depth regularization from [9], photorealistic and mask losses. (b): Add SDF Flow Regularization based on (a). (c): Training (b) with Independent Segment Partitioning. (d): Training (b) with Overlapping Segment Partitioning. (e): Adopting Incremental Motion Tuning (LoRA rank 64) on (d)*

### 时间稳定性分析

Table 4 报告了 Hi4D 六场景上各方法在 Acc、Comp、Overall 三个指标上的平均标准偏差（STD），用以衡量重建表面的时间稳定性。4DSurf 的 Overall STD 仅为 0.18，显著优于 **Sparse2DGS** 的 0.68 和 **Dynamic-2DGS** 的 1.19，甚至优于同为分段策略的 **GauSTAR**（Zheng et al., CVPR 2025）的 0.46。这一结果表明，SDF 流正则化通过强制高斯运动与表面演化对齐，有效抑制了逐帧独立重建中常见的高频抖动。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/011_Table_4.jpg]]
*Table 4: Temporal stability comparison on the Hi4D dataset [54]. STD: standard deviation. It shows the average STD of the three metrics (Acc, Comp, and Overall) across six scenes. The best and the second-best are highlighted in bold and underlined*

### 增量运动调整的存储-精度权衡

Table 5 和 Figure 7 分析了不同 LoRA 秩对重建精度和存储开销的影响。在 Backhug02 场景上：
- 完整存储所有段的速度场参数（wo IMT）需约 45 MB，且随段数线性增长。
- IMT-64 将单段存储压缩至约 12 MB，Overall 仅从 0.84 cm 轻微升至 0.87 cm。
- 进一步降低秩至 IMT-16，存储仅 9.4 MB，Overall 仍保持 0.92 cm，展现出良好的压缩-精度帕累托前沿。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/012_Table_5.jpg]]
*Table 5: Different LoRA ranks comparison on Hi4D dataset [54]. It shows the average of the three metrics (Acc, Comp, and Overall) in six scenes under different LoRA ranks*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/008_Figure_7.jpg]]
*Figure 7: LoRA rank and storage analysis on scene Backhug02. Left: As the number of segments increases, Ours wo IMT exhibits growing storage of Gaussian velocity fields, while Ours w IMT-{LoRA-rank} effectively curb the storage growth. Right: For different LoRA ranks, Ours w IMT maintains strong performance (even at rank 16), achieving competitive results to Ours wo IMT*

### 实验设置公平性说明

所有实验均在 NVIDIA RTX 3090Ti 上完成，每段训练 30K 迭代（约 30 分钟）。基线方法使用作者公布的实现及推荐超参数。CMU Panoptic 使用 31 个训练视角，Hi4D 使用 8 个稀疏视角，评估时均采用标准 Chamfer Distance 计算流程，确保对比公平性。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/004_Table_1.jpg]]
*Table 1: CMU Panoptic [13] comparisons. We evaluate performance with Chamfer Distance (unit: mm). The top three results for each metric are highlighted with , and , respectively. Ours consistently achieves the best performance on the Overall metric*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/005_Table_2.jpg]]
*Table 2: Hi4D [54] comparisons. We evaluate performance using Chamfer Distance (unit: cm). The top three results for each metric are highlighted in , and , respectively. Ours significantly outperforms all baselines on the Overall metric*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on CMU Panoptic [13]. We compare our methods with three baselines (Dynamic-2DGS [55], Sparse2DGS [46], FreeTimeGS [43]) at two timesteps of the Band1 and Ian3 scene. Bounding boxes highlight major differences*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_28064/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on Hi4D [54]. We compare our methods with three baselines (Dynamic-2DGS [55], Sparse2DGS [46], FreeTimeGS [43]) at two timesteps of the Basketball13 and Fight17 scene. Bounding boxes highlight major differences*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

4DSurf 瞄准的是**稀疏视角下多物体大形变动态场景的表面重建**。现有基于高斯泼溅（Gaussian Splatting）的动态表面重建方法面临一个关键瓶颈：在处理大形变时，表面抖动严重、时间一致性差，且通常局限于单个物体或小形变场景。这一瓶颈的根源在于现有方法缺乏显式的机制来约束高斯运动与表面演化之间的时间一致性。

### 2. 与基线方法的差异分析

4DSurf 在三个关键维度上区别于现有工作：

**变形建模范式**：现有动态高斯方法（如 **Dynamic-2DGS**（Zhang et al., ACM MM 2025）、**Space-Time-2DGS**（Wang et al., arXiv 2024）、**4DGS**（Wu et al., CVPR 2024））通常使用变形场直接预测高斯的绝对位移。4DSurf 转而采用**高斯速度场**（Gaussian Velocity Field），预测每个高斯的线性速度 $\mathbf{v}$、角速度 $\boldsymbol{\omega}$ 和膨胀速度 $e$，从而将变形建模为刚体运动参数的函数。这一设计使得运动表示与物理规律更一致，也为后续的 SDF 流推导提供了数学基础。

**时间正则化机制**：现有方法缺乏显式的表面演化约束。4DSurf 的核心创新在于**SDF 流正则化**——从高斯速度场导出的 SDF 流 $\mathbf{f} = -(\boldsymbol{\omega}\times\mathrm{R}^t\mathbf{x} + \mathbf{v})^\top\mathbf{n}(\mathrm{R}^t\mathbf{x})$ 与从渲染深度图近似估计的 SDF 流 $\tilde{\mathbf{f}}$ 进行 L1 匹配。这一机制将静态 SDF 流理论（如 **Neural SDF-Flow**（Mao et al., ICLR 2024）在 NeRF 框架下的工作）扩展到动态高斯表示，强制表面在时间上光滑演化。消融实验表明，仅此一项就将 6 个 Hi4D 场景的平均 Overall Chamfer 距离从 1.49 降至 1.02（Table 3, rows a vs b）。

**大形变处理策略**：现有方法对整个序列训练单一变形场，在大形变场景下误差累积严重。4DSurf 提出**重叠段分割**（Overlapping Segment Partitioning）策略，将序列划分为包含虚拟重叠时间步的短段，每段仅需处理小幅形变，并通过共享时间步增量传递几何信息。这一设计直接缓解了误差累积问题，使平均 Overall 进一步降至 0.67（Table 3, row d）。与之配套的**增量运动调整**（Incremental Motion Tuning, IMT）使用 LoRA 对后续段的速度场进行低秩适配 $\boldsymbol{\theta}^N = \boldsymbol{\theta}^{N-1} + \mathbf{A}^N\mathbf{B}^N$，在几乎不损失精度的情况下有效控制存储增长。

### 3. 在知识库中的定位

4DSurf 处于**动态表面重建**与**3D 高斯泼溅**的交叉地带，其知识贡献可沿以下脉络定位：

- **上游继承**：继承了 2D Gaussian Splatting 的表面表示能力（每个高斯定义在局部切平面上），以及 Neural SDF-Flow 中 SDF 流与场景流关联的理论框架。与 **GauSTAR**（Zheng et al., CVPR 2025）等使用光流先验的方法不同，4DSurf 的 SDF 流正则化直接从高斯运动参数推导，无需外部光流估计。

- **横向对比**：相较于 **Sparse2DGS**（Wu et al., CVPR 2025）等静态方法逐帧独立重建，4DSurf 通过段分割和 SDF 流正则化实现了跨帧一致性，在时间稳定性上显著优于逐帧方法（Overall 标准偏差最低仅 0.18，而 Sparse2DGS 为 0.68，Dynamic-2DGS 为 1.19，见 Table 4）。

- **下游影响**：4DSurf 的段分割 + LoRA 增量微调策略为长序列动态重建提供了一种可扩展的范式，其高斯速度场设计也为后续研究将物理约束（如刚体运动学）引入高斯表示提供了参考。

### 4. 适用边界与局限

基于论文中报告的结果和设计选择，4DSurf 的适用边界可从以下角度理解：

**已验证的适用场景**：多视角（稀疏视角设置）、多物体、大形变的动态场景表面重建，在 CMU Panoptic 和 Hi4D 两个公开数据集上验证有效。Chamfer 距离指标分别在两个数据集上以 49% 和 19% 的优势超越现有最优方法。

**需注意的设计约束**：
- 方法依赖前景掩码进行视觉外壳初始化和掩码损失计算，对分割质量有一定要求。
- 段分割策略中的段长度（默认 5 个时间步）和重叠设计是经验性选择，在不同帧率或运动速度的场景下可能需要调整。
- 论文未明确讨论对拓扑变化（如物体分裂、合并）的处理能力，这可能是 SDF 流框架的内在局限。

**存储与效率权衡**：IMT 通过 LoRA 低秩适配在精度与存储间取得平衡。LoRA 秩 64 时 Overall 为 0.70，秩 16 时存储仅 9.4 MB 但仍保持有竞争力的质量（Table 5, Figure 7）。这是实际部署时的重要可调参数。

### 5. 开放问题与待验证方向

论文未明确讨论以下问题，需要后续工作或手动验证：

1. **极稀疏视角下的鲁棒性**：当前实验基于 CMU Panoptic 和 Hi4D 的多视角设置，在更极端的稀疏视角（如 2-3 个视角）下 SDF 流近似的可靠性需要进一步验证。

2. **非刚体形变的边界**：高斯速度场假设局部刚体运动，对于高度非刚体的形变（如布料褶皱、流体）的适用性尚不明确。

3. **实时性潜力**：当前每段训练约 30 分钟（NVIDIA RTX 3090Ti），远未达到实时。段分割策略天然支持并行训练，但论文未探索这一方向。

4. **与基于 NeRF 的方法的全面对比**：虽然包含了 Neural SDF-Flow 作为基线，但与 **NDR**（Cai et al., NeurIPS 2022）等 NeRF 动态重建方法的直接定量对比有限，仅在 CMU Panoptic 上与 Neural SDF-Flow 进行了比较。



## 原文 PDF

![[paperPDFs/CVPR_2026/4DSurf_High_Fidelity_Dynamic_Scene_Surface_Reconstruction.pdf]]
