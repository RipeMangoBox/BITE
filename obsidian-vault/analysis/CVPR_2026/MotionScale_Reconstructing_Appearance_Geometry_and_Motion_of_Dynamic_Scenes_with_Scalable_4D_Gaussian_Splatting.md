---
title: "MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionScale_Reconstructing_Appearance_Geometry_and_Motion_of_Dynamic_Scenes_with_Scalable_4D_Gaussian_Splatting.pdf
project_link: "https://hrzhou2.github.io/motion-scale-web/"
code_link: null
aliases:
- MotionScale
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入集群中心的自适应运动场（cluster-centric motion field）以及解耦的背景扩展与前景传播渐进优化策略，从根本上改善了几何约束和时序一致性。
primary_logic: 通过将动态高斯点划分为可自适应分裂的集群，并为每个集群学习全局刚体和局部非刚体基变换的组合运动场，实现了运动表示的可扩展性；同时利用2D先验引导的渐进式优化，确保长序列中的几何与运动一致性。
claims:
- MotionScale在DyCheck和NVIDIA Dynamic Scenes数据集上一致优于所有先前方法，PSNR分别达到17.98和26.75。
- 点追踪指标3D EPE 0.070、2D AJ 37.7、OA 0.87，显著优于Shape of Motion等基线。
- 消融实验表明，集群运动场比全局基方法PSNR提升1.28，自适应控制和三阶段细化对运动精度至关重要。
- DyCheck 上 PSNR↑ = 17.98
---

# MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting

> [!tip] 核心洞察
> 通过将动态高斯点划分为可自适应分裂的集群，并为每个集群学习全局刚体和局部非刚体基变换的组合运动场，实现了运动表示的可扩展性；同时利用2D先验引导的渐进式优化，确保长序列中的几何与运动一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionScale：基于可扩展4D高斯溅射的动态场景外观、几何与运动重建 |
| 英文题名 | MotionScale: Reconstructing Appearance, Geometry, and Motion of Dynamic Scenes with Scalable 4D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29296) · [Project](https://hrzhou2.github.io/motion-scale-web/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionScale |
| Dataset | DyCheck, NVIDIA Dynamic Scenes, DyCheck Point Tracking |

> [!tip] 效果简介
> - DyCheck 上，PSNR↑ 17.98 vs Prior SOTA (see Tab.1) (见Tab.1)；SSIM↑ 0.70 vs Prior SOTA (see Tab.1) (见Tab.1)；LPIPS↓ 0.40 vs Prior SOTA (see Tab.1) (见Tab.1)。
> - NVIDIA Dynamic Scenes 上，PSNR↑ 26.75 vs Prior SOTA (see Tab.1) (见Tab.1)；SSIM↑ 0.78 vs Prior SOTA (see Tab.1) (见Tab.1)；LPIPS↓ 0.07 vs Prior SOTA (see Tab.1) (见Tab.1)。
> - DyCheck Point Tracking 上，3D EPE↓ 0.070 vs Prior SOTA (see Tab.2) (见Tab.2)。

## 概述

**问题背景** 从单目视频中重建动态场景的完整4D表示（外观、几何、运动）是计算机视觉的核心挑战。现有基于4D高斯溅射（4DGS）的方法虽然在新视角合成上取得进展，但普遍面临两个根本瓶颈：**几何欠约束**——缺乏严格的3D结构一致性导致重建几何崩塌；**长时序误差累积**——逐帧或一次性优化策略难以维持长序列中的运动漂移控制。

**核心思想** MotionScale提出了一种**可扩展的4D高斯溅射框架**，通过两个关键创新突破上述瓶颈：

1. **集群中心的自适应运动场**：将动态高斯点划分为可自适应分裂的集群，为每个集群学习由全局刚体变换和局部非刚体基变换组合的层次化运动模型。这种设计使运动表示容量能随场景复杂度自主扩展，从根本上改善了几何约束与运动建模精度。

2. **解耦的渐进式优化策略**：将长序列优化分解为**背景扩展**（填充新观察区域、细化相机位姿、建模瞬态阴影）和**前景传播**（利用2D追踪先验进行三阶段细化：初始对准→短期一致性→长期细化）两个独立阶段，有效抑制了时序误差累积。

**方法定位** MotionScale首次在动态高斯溅射框架中实现了运动表示的可扩展性——不同于SC-GS（Huang et al., CVPR 2024）的全局MLP变形场或SplineGS（Park et al., CVPR 2025）的固定容量样条运动模型，MotionScale的集群基运动场能根据场景运动复杂度自适应增长或剪枝。

**主要结果** 在DyCheck和NVIDIA Dynamic Scenes两个标准基准上，MotionScale一致超越所有先前方法：PSNR分别达到**17.98**和**26.75**（Tab.1）。点追踪指标同样取得最优：3D EPE **0.070**、2D AJ **37.7**、OA **0.87**，显著优于Shape of Motion（Wang et al., ICCV 2025）等基线（Tab.2）。消融实验证实，集群运动场相比全局基方法PSNR提升**1.28**，阴影高斯模块和自适应控制对最终性能均至关重要（Tab.3）。

## 背景与动机

### 动态场景重建的核心挑战

从单目视频中重建动态场景的完整4D表示（外观、几何与运动）是计算机视觉与图形学中的基础性难题。该任务要求同时恢复场景的静态结构、时变外观以及每个表面点的精确3D运动轨迹，其核心困难在于：单目观测提供的约束极为稀疏，而动态场景本身又具有高度的非刚体变形、遮挡和光照变化。

近年来，以3D Gaussian Splatting（3DGS）为代表的显式点云表示方法在静态场景重建中取得了突破性进展。然而，将3DGS扩展到动态场景（即4DGS）时，现有方法普遍面临两个根本性瓶颈：

1. **几何欠约束与运动漂移**：现有4DGS方法通常采用全局MLP或固定容量的变形场来建模运动，缺乏严格的3D结构一致性约束。在长时序优化过程中，这种松散的几何约束导致高斯点的3D位置逐渐偏离真实表面，引发几何崩塌和运动漂移，表现为渲染质量随时间推移而显著下降。

2. **运动表示的可扩展性不足**：真实动态场景包含从全局刚体运动到局部精细非刚体变形的多尺度运动模式。现有方法的运动表示容量固定，无法根据场景复杂度自适应扩展，导致对复杂运动（如人体关节运动、流体变形）的建模能力不足。

### 现有方法的局限

当前主流的动态场景重建方法可大致分为两类。第一类以**Deformable 3DGS**（Yang et al., CVPR 2024）和**4D-GS**（Yang et al., ICLR 2024）为代表，通过全局变形网络将规范空间的高斯点映射到各时刻，但全局参数化难以捕捉局部非刚体运动的多样性。第二类如**SC-GS**（Huang et al., CVPR 2024）和**SplineGS**（Park et al., CVPR 2025）引入了更灵活的运动基表示，但仍然缺乏对运动拓扑变化的显式建模——当场景中出现新的运动模式或物体分离时，这些方法无法自适应地增加表示容量。

在优化策略方面，现有方法通常一次性优化整个序列或逐帧独立优化，忽略了长序列中背景与前景在时序一致性上的本质差异。一次性优化容易导致误差在时间轴上累积，而逐帧优化则破坏了跨帧的运动连续性。

此外，动态场景中常见的瞬时光照变化（如移动阴影）在现有方法中几乎被完全忽略。这些光照效应若不被显式建模，会被错误地吸收到几何或运动表示中，进一步加剧几何退化。

### MotionScale的动机与核心思路

针对上述瓶颈，MotionScale提出了两个核心机制：

- **可扩展的集群中心运动场**：将动态高斯点划分为可自适应分裂与剪枝的集群，每个集群学习一组全局刚体变换与局部非刚体基变换的组合运动模型。这种层次化设计使得运动表示能够根据场景复杂度自主扩展容量，同时通过集群内共享运动基来强化局部几何约束，从根本上抑制运动漂移。

- **解耦的渐进式优化策略**：将优化过程分解为背景扩展与前景传播两个阶段。背景阶段负责填充新引入帧的未观察区域并细化相机位姿与阴影效应；前景阶段则利用2D点追踪先验，通过初始对准、短期一致性和长期细化三个步骤逐步传播运动场。这种解耦设计确保了长序列中全局结构的稳定性和局部运动的精度。

通过上述设计，MotionScale旨在实现动态场景重建中外观质量、几何精度与运动一致性的三重提升，同时保持表示的可扩展性以应对任意长度的视频输入。

## 核心创新

MotionScale 的核心创新在于从根本上重构了动态场景的运动表示与优化范式，以解决现有 4DGS 方法普遍存在的几何欠约束和长时序误差累积问题。其关键创新点可归纳为三个紧密耦合的 changed slots：

### 1. 集群中心的自适应层次运动基（Cluster-centric Hierarchical Motion Bases）

传统 4DGS 方法（如 **Deformable 3DGS** Yang et al., CVPR 2024；**4D-GS** Yang et al., ICLR 2024）通常采用全局 MLP 或固定容量的变形场来建模场景运动，这类表示难以同时捕捉不同物体的独立运动模式，且在复杂非刚体变形场景下容量不足。MotionScale 提出了一种**可扩展的运动场**：将动态高斯点划分为 $K$ 个不相交的集群 $\{\mathcal{C}_k\}_{k=1}^K$，每个集群拥有独立的分层运动模型——

- **全局刚体变换**：一个 SE(3) 变换 $(\mathbf{R}_{k,g}^t, \mathbf{t}_{k,g}^t)$ 建模集群的整体运动；
- **局部非刚体基变换**：$B$ 个可学习的旋转基 $\mathbf{r}_{k,b}^t$ 和平移基 $\mathbf{t}_{k,b}^t$，通过可学习权重 $w_{i,b}$ 混合，为集群内每个高斯点提供精细的局部变形：

$$\mathbf{R}_{i,\ell}^{t} = \mathcal{R}\left( \sum_{b=1}^{B} w_{i,b} \mathbf{r}_{k,b}^{t} \right), \quad \mathbf{t}_{i,\ell}^{t} = \sum_{b=1}^{B} w_{i,b} \mathbf{t}_{k,b}^{t}$$

最终，高斯点在 $t$ 时刻的位置与朝向由全局与局部变换组合得到：

$$\mu_i^t = \mathbf{R}_{k,g}^t ( \mathbf{R}_{i,\ell}^t \pmb{\mu}_i^0 + \mathbf{t}_{i,\ell}^t ) + \mathbf{t}_{k,g}^t, \quad \mathbf{R}_i^t = \mathbf{R}_{k,g}^t \mathbf{R}_{i,\ell}^t \mathbf{R}_i^0$$

这种设计的核心洞察在于：**运动表示的容量不是固定的，而是随场景复杂度自适应增长**。当某个集群内的运动出现不一致时，自适应控制机制（Adaptive Control）通过 HDBSCAN 和 Agglomerative Clustering 将其分裂为多个子集群，从而“隔离”不同的运动模式；反之，贡献过小的集群被剪枝。消融实验证实，将集群运动场替换为全局基础变换（Global Bases）会导致 PSNR 下降 1.28（Tab.3），验证了局部集群基对非刚体变形建模的关键作用。

### 2. 解耦的背景扩展与前景传播渐进优化策略

现有方法多采用一次性优化整个序列或逐帧独立优化的方式，难以在长视频中维持时空一致性。MotionScale 提出**渐进式优化策略**，将优化过程解耦为两个独立阶段：

- **背景扩展（Background Extension）**：当新帧引入时，首先填充新观察到的背景区域，同时细化背景几何与相机位姿。这一步骤为后续前景运动建模提供了稳定的全局几何锚点。
- **前景传播（Foreground Propagation）**：采用三阶段细化流程——① 初始对齐（Initial Alignment）利用 2D 追踪先验快速匹配运动；② 短期一致性（Short-term Consistency）在相邻帧窗口内优化；③ 长期细化（Long-term Refinement）在更大时间窗口内传播运动场，确保长序列中的几何与运动一致性。

该策略的核心优势在于：**将背景几何的稳定性与前景运动的灵活性解耦**，避免了传统联合优化中背景漂移与前景模糊的相互干扰。消融实验表明，三阶段细化对扩展复杂视频至关重要，去除任一步骤均会降低一致性（Sec.4.5）。

### 3. 阴影高斯（Shadow Gaussians）的显式瞬态光照建模

动态场景中普遍存在阴影、光照变化等瞬态效应，但现有 4DGS 方法未对此进行显式建模，导致背景渲染中出现伪影。MotionScale 引入一组专用的**阴影高斯**，专门负责模拟场景中的瞬态阴影和光照变化。消融实验显示，去除阴影高斯模块后，背景渲染 PSNR 从 17.98 骤降至 16.26（Tab.3），验证了其对重建质量的重要贡献。

---

**创新关联性总结**：上述三个创新并非孤立存在，而是形成了因果闭环——集群运动场提供了可扩展的表示容量（创新 1），渐进优化策略确保了该容量在长序列中被有效利用（创新 2），阴影高斯则消除了瞬态效应对背景几何的干扰，为运动建模提供了更干净的信号（创新 3）。三者共同作用，使 MotionScale 在 DyCheck 和 NVIDIA Dynamic Scenes 数据集上一致优于所有先前方法（PSNR 分别达到 17.98 和 26.75，Tab.1）。

## 整体框架

MotionScale 的整体框架围绕一个核心设计展开：**将动态场景表示为规范空间中的一组 3D 高斯点，并由一个可扩展的运动场（scalable motion field）驱动其在时间轴上演化**。该运动场通过集群中心的自适应层次运动基（cluster-centric hierarchical motion bases）来参数化局部区域的动力学，同时引入自适应控制策略自主扩展或剪枝集群，从而实现表示容量的可伸缩性。与之配套的渐进式优化策略解耦为背景扩展与前景传播两个阶段，确保长序列中的时空一致性。图 2 给出了框架总览。

### 输入与输出

- **输入**：单目动态视频序列。
- **输出**：完整的 4D 场景表示，包括逼真的外观、准确的 3D 几何以及多样化的物体运动，支持新视角合成与点追踪。

### 模块组成与数据流

整个 pipeline 由以下核心模块串联构成，数据从原始视频帧逐步转化为可渲染的 4D 高斯场：

1. **3D 高斯溅射基础（3DGS Base）**  
   以规范空间的 3D 高斯点集 $\{g_i\}$ 为静态载体，每个高斯点携带位置 $\pmb{\mu}_i^0$、旋转四元数 $\mathbf{R}_i^0$、颜色 $\mathbf{c}_i$、不透明度 $\alpha_i$ 等属性。渲染时通过 alpha 混合公式：
   $$
   \mathbf{I}(\mathbf{p}) = \sum_{i \in \mathcal{H}(\mathbf{p})} \mathbf{c}_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
   $$
   将视线方向上的高斯点颜色加权累积为像素颜色（Eq. 1）。该模块为整个框架提供可微渲染接口。

2. **可扩展运动场与集群划分（Scalable Motion Field with Cluster Partition）**  
   动态高斯点 $\mathcal{G}_d$ 被划分为 $K$ 个不相交的集群 $\{\mathcal{C}_k\}_{k=1}^K$。每个集群 $\mathcal{C}_k$ 配备一个层次化运动模型：
   - **全局刚体变换**：一个 $\mathrm{SE}(3)$ 变换 $(\mathbf{R}_{k,g}^t, \mathbf{t}_{k,g}^t)$ 捕捉集群的整体运动。
   - **局部非刚体基变换**：$B$ 个旋转基 $\mathbf{r}_{k,b}^t$ 与平移基 $\mathbf{t}_{k,b}^t$，通过可学习权重 $w_{i,b}$ 混合得到每个高斯点的局部变换：
     $$
     \mathbf{R}_{i,\ell}^{t} = \mathcal{R}\left( \sum_{b=1}^{B} w_{i,b} \mathbf{r}_{k,b}^{t} \right), \quad
     \mathbf{t}_{i,\ell}^{t} = \sum_{b=1}^{B} w_{i,b} \mathbf{t}_{k,b}^{t}
     $$
     最终高斯点在时刻 $t$ 的位置与方向由全局与局部变换组合得到：
     $$
     \mu_i^t = \mathbf{R}_{k,g}^t ( \mathbf{R}_{i,\ell}^t \pmb{\mu}_i^0 + \mathbf{t}_{i,\ell}^t ) + \mathbf{t}_{k,g}^t, \quad
     \mathbf{R}_i^t = \mathbf{R}_{k,g}^t \mathbf{R}_{i,\ell}^t \mathbf{R}_i^0
     $$
     （Eq. 2–3）。这种“全局刚体 + 局部基混合”的层次设计，使得运动场既能保持集群整体一致性，又能精细刻画局部非刚体变形。

3. **自适应控制（Adaptive Control）**  
   当集群内高斯点的运动轨迹出现显著不一致时，系统自动触发分裂操作：先通过 HDBSCAN 聚类识别运动模式分歧的子群，再用 Agglomerative Clustering 将其划分为独立集群（Fig. 2a）。分裂后的集群各自学习独立的运动基，从而将原本模糊的动力学解耦为清晰的运动分量。同时，冗余或贡献微弱的集群会被剪枝，控制总体表示复杂度。这一机制是实现运动表示可扩展性的关键——它使运动场能够随场景复杂度自适应增长。

4. **渐进式优化策略（Progressive Optimization）**  
   针对长视频序列，MotionScale 不一次性优化所有帧，而是逐步引入新帧（Fig. 2b），解耦为两个传播阶段：

   - **背景扩展（Background Extension）**  
     新帧引入时，首先通过区域采样填充新可见的背景区域，并细化相机位姿与背景几何。同时引入专用的**阴影高斯（Shadow Gaussians）**显式建模瞬态阴影或光照变化，防止这些外观扰动污染运动场学习。

   - **前景传播（Foreground Propagation）**  
     前景运动场通过三阶段细化逐步传播到长时域窗口：
     1. **初始对齐**：利用 2D 点追踪先验对运动场进行粗对齐。
     2. **短期一致性**：在相邻帧窗口内优化运动基，确保局部时序平滑。
     3. **长期细化**：在扩展的时间窗口上全局微调，消除累积漂移。

     三阶段中均使用 2D 追踪损失与深度一致性损失作为监督信号：
     $$
     L_{\mathrm{track}} = \frac{1}{|I_t|} \sum_{p \in I_t} \| \hat{\mathbf{U}}_{t t'}(\mathbf{p}) - \mathbf{U}_{t t'}(\mathbf{p}) \|, \quad
     L_{\mathrm{depth}} = \frac{1}{|I_t|} \sum_{p \in I_t} \| \hat{\mathbf{D}}_{t t'}(\mathbf{p}) - \mathbf{D}_{t t'}(\mathbf{p}) \|
     $$
     （Eq. 5–6）。3D 轨迹点 $\mathbf{X}_{t t'}(\mathbf{p})$ 则通过 alpha 混合在目标时刻的高斯位置获得（Eq. 4），经投影后与 2D 先验对齐。

### 关键设计逻辑

框架的核心因果链条可概括为：**集群层次运动基 → 自适应分裂/剪枝 → 渐进式解耦优化**。集群运动场提供了比全局 MLP 更强的局部几何约束，避免了传统 4DGS 方法中的几何崩塌；自适应控制使运动表示容量随场景复杂度动态伸缩；背景-前景解耦的渐进优化则从根本上抑制了长序列中的误差累积与运动漂移。阴影高斯的引入进一步隔离了瞬时光照效应，防止其对几何与运动学习的干扰。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionScale. Our method adopts a scalable motion field that progressively captures object motions through an adaptive control mechanism, enabling efficient splitting and refinement of motion components. For optimization, the background is updated through region sampling, camera refinement, and shadow handling, while the foreground propagation employs a three-stage refinement to propagate motion across long temporal windows for consistent 4D reconstruction*

## 核心模块与公式推导

### 3.1 3D高斯溅射基础

MotionScale建立在3D高斯溅射（3DGS）的静态场景表示之上。场景由一组3D高斯点 $\{g_i\}$ 表示，每个高斯点包含中心位置 $\mu_i$、协方差矩阵 $\Sigma_i$（由旋转四元数 $\mathbf{R}_i$ 和缩放 $\mathbf{s}_i$ 参数化）、不透明度 $\alpha_i$ 和颜色 $\mathbf{c}_i$。给定相机位姿，通过可微光栅化将高斯点投影到图像平面。像素 $\mathbf{p}$ 的最终颜色由沿视线排序的高斯点通过alpha混合计算：

$$
\mathbf{I}(\mathbf{p}) = \sum_{i \in \mathcal{H}(\mathbf{p})} \mathbf{c}_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \tag{1}
$$

其中 $\mathcal{H}(\mathbf{p})$ 是与像素 $\mathbf{p}$ 相交的高斯点集合，$\alpha_i$ 是投影高斯权重与不透明度的乘积。这一基础渲染管线为后续动态扩展提供了可微分的优化框架。

### 3.2 可扩展运动场

MotionScale的核心创新在于构建了一个**以集群为中心的可扩展运动场**（cluster-centric scalable motion field），将动态高斯点 $\mathcal{G}_d = \{g_i\}_{i=1}^{N_d}$ 划分为 $K$ 个不相交的集群 $\{\mathcal{C}_k\}_{k=1}^{K}$，每个集群独立建模其运动模式。

#### 3.2.1 层次运动基

对于每个集群 $\mathcal{C}_k$，定义层次运动模型，包含全局刚体变换和局部非刚体细化基：

- **全局变换**：每个集群维护一个 $\mathrm{SE}(3)$ 变换 $(\mathbf{R}_{k,g}^t, \mathbf{t}_{k,g}^t)$，捕获集群整体的刚体运动。
- **局部细化基**：每个集群包含 $B$ 个可学习的局部旋转基 $\mathbf{r}_{k,b}^t$ 和平移基 $\mathbf{t}_{k,b}^t$，用于建模集群内部的非刚体变形。每个高斯点 $g_i$ 通过可学习权重 $w_{i,b}$ 混合这些基，得到其局部变换：

$$
\mathbf{R}_{i,\ell}^{t} = \mathcal{R}\left( \sum_{b=1}^{B} w_{i,b} \mathbf{r}_{k,b}^{t} \right), \quad
\mathbf{t}_{i,\ell}^{t} = \sum_{b=1}^{B} w_{i,b} \mathbf{t}_{k,b}^{t} \tag{2}
$$

其中 $\mathcal{R}(\cdot)$ 是将任意向量映射为旋转矩阵的操作（如通过Rodrigues公式或四元数归一化）。

#### 3.2.2 规范空间到观测空间的变换

将全局刚体变换与局部非刚体变换组合，可得到高斯点 $g_i$ 在时刻 $t$ 的位置和方向。规范空间中的均值 $\mu_i^0$ 首先经过局部变换，再经过全局变换：

$$
\mu_i^t = \mathbf{R}_{k,g}^t ( \mathbf{R}_{i,\ell}^t \mu_i^0 + \mathbf{t}_{i,\ell}^t ) + \mathbf{t}_{k,g}^t \tag{3}
$$

方向变换类似，规范旋转 $\mathbf{R}_i^0$ 依次经过局部和全局旋转变换：

$$
\mathbf{R}_i^t = \mathbf{R}_{k,g}^t \mathbf{R}_{i,\ell}^t \mathbf{R}_i^0
$$

这种层次化设计的关键优势在于：全局变换捕获集群的整体运动趋势，而局部基通过加权混合为每个高斯点提供个性化的非刚体变形能力，从而在保持表示紧凑性的同时具备足够的表达能力。

#### 3.2.3 自适应控制机制

为实现运动场的可扩展性，MotionScale采用自适应控制策略动态调整集群结构。当集群内高斯点的运动轨迹出现显著不一致时，系统通过以下步骤进行分裂：

1. 识别运动不一致的高斯点子集；
2. 使用HDBSCAN聚类将不一致的高斯点分组；
3. 对剩余高斯点应用Agglomerative Clustering进行细化分割。

分裂后的新集群继承父集群的运动参数作为初始化，并独立优化各自的运动基。同时，对贡献过小或退化的集群进行剪枝，控制总集群数量。这一机制使运动场能够随场景复杂度自适应扩展，从简单场景的少数集群逐步演化到复杂动态场景的丰富集群结构。

### 3.3 渐进式优化策略

为处理长视频序列并保持时序一致性，MotionScale采用渐进式优化策略，将优化过程解耦为两个传播阶段：背景扩展和前景传播。

#### 3.3.1 背景扩展

当新帧引入时，背景扩展阶段负责：
- 填充新观察到的背景区域；
- 细化相机位姿估计；
- 引入**阴影高斯**（Shadow Gaussians）显式建模瞬态阴影和光照变化。

阴影高斯是一组专门的高斯点，其颜色和不透明度随光照条件变化而调整，从而在不影响几何结构的前提下处理场景中的光照效应。

#### 3.3.2 前景传播的三阶段细化

前景传播通过三阶段细化过程将运动场传播到长时序窗口：

1. **初始对齐**：利用2D点追踪先验建立新帧与已优化帧之间的初始对应关系，快速初始化运动参数。
2. **短期一致性**：在局部时间窗口内联合优化运动场和渲染质量，确保相邻帧间的运动平滑性。
3. **长期细化**：在全局时间窗口内进行精细调整，消除累积漂移，保证长序列中的几何与运动一致性。

#### 3.3.3 关键损失函数

优化过程中引入2D先验引导的损失函数，将可微渲染与外部先验信号结合。

**3D轨迹渲染**：通过alpha混合计算像素 $\mathbf{p}$ 在目标时刻 $t'$ 的3D位置：

$$
\mathbf{X}_{t t'}(\mathbf{p}) = \sum_{i \in \mathcal{H}(\mathbf{p})} \mu_i^{t'} \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \tag{4}
$$

该3D轨迹点可投影回图像平面获得2D轨迹估计 $\hat{\mathbf{U}}_{t t'}(\mathbf{p})$。

**追踪损失**：将估计的2D轨迹与外部2D点追踪先验 $\mathbf{U}_{t t'}(\mathbf{p})$ 对齐：

$$
L_{\mathrm{track}} = \frac{1}{|I_t|} \sum_{p \in I_t} \| \hat{\mathbf{U}}_{t t'}(\mathbf{p}) - \mathbf{U}_{t t'}(\mathbf{p}) \| \tag{5}
$$

**深度一致性损失**：类似地，利用单目深度先验约束3D几何：

$$
L_{\mathrm{depth}} = \frac{1}{|I_t|} \sum_{p \in I_t} \| \hat{\mathbf{D}}_{t t'}(\mathbf{p}) - \mathbf{D}_{t t'}(\mathbf{p}) \| \tag{6}
$$

其中 $\hat{\mathbf{D}}_{t t'}(\mathbf{p})$ 是通过类似alpha混合机制从高斯点深度值渲染得到的深度估计，$\mathbf{D}_{t t'}(\mathbf{p})$ 为单目深度先验。

这两个损失函数共同作用，将2D先验信息（点追踪和深度估计）注入3D运动场优化，有效缓解了纯光度损失在动态场景中面临的几何欠约束问题。

## 实验与分析

### 实验设置与基准

MotionScale 在两大动态场景重建基准上进行了全面评估：**DyCheck**（包含复杂人体动作的单目视频）和 **NVIDIA Dynamic Scenes**（多视角动态场景）。对比方法覆盖了4D高斯溅射领域的最新工作，包括 **4DGS** (Wu et al., CVPR 2024)、**Deformable 3DGS** (Yang et al., CVPR 2024)、**4D-GS** (Yang et al., ICLR 2024)、**SC-GS** (Huang et al., CVPR 2024)、**SplineGS** (Park et al., CVPR 2025) 等动态重建基线，以及 **Shape of Motion** (Wang et al., ICCV 2025)、**GFlow** (Wang et al., AAAI 2025)、**4D-Fly** (Wu et al., CVPR 2025) 等点追踪与4D重建方法。所有方法使用统一的2D先验（深度图、掩膜、点追踪）和相同的评测协议，以保证公平比较。

### 新视角合成主结果

Table 1 汇总了在 DyCheck 和 NVIDIA Dynamic Scenes 数据集上的新视角合成定量结果。MotionScale 在两个基准上一致优于所有先前方法，在 DyCheck 上达到 **PSNR 17.98**、**SSIM 0.70**、**LPIPS 0.40**，在 NVIDIA 上达到 **PSNR 26.75**、**SSIM 0.78**、**LPIPS 0.07**。这一性能优势源于两个核心机制：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/003_Table_1.jpg]]
*Table 1: Comparison of novel view synthesis results on Dy-Check [10] and NVIDIA [55] datasets*

1. **集群运动场的几何约束能力**：基于集群的分层运动基（全局刚体 + 局部非刚体基变换）有效约束了高斯点的时空轨迹，在保持锐利表面和纹理细节的同时避免了传统全局MLP变形场中的几何崩塌问题。
2. **渐进优化策略的时序稳定性**：解耦的背景扩展与前景传播使运动场始终锚定在已建立的背景几何之上，确保了长序列中全局结构的稳定性和局部运动的细节保真度。

在 DAVIS 数据集上的定性对比（Figure 3）进一步验证了这一优势：面对包含复杂物体运动、遮挡和大尺度外观变化的真实场景，MotionScale 相比 Shape of Motion 和 GFlow 呈现出更清晰的结构完整性和更少的运动模糊伪影。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/004_Figure_3.jpg]]
*Figure 3: Comparison of dynamic scene reconstruction results on challenging real-world videos from DAVIS dataset. We compare MotionScale with Shape of Motion [43] and GFlow [46] on several dynamic scenes containing complex object motions, occlusions, and large appearance variations. For the top rows, we show rendered results under two different viewpoints for each compared method*

### 点追踪性能

Table 2 报告了 DyCheck 数据集上的点追踪定量结果。MotionScale 在全部三个指标上均取得最优：**3D EPE 0.070**（三维端点误差）、**2D AJ 37.7**（二维平均交并比）、**OA 0.87**（遮挡准确率），显著优于 Shape of Motion 等专用追踪基线。这一结果表明，集群运动场不仅有利于渲染质量，其显式的3D轨迹建模（通过 alpha 混合累加目标时刻高斯位置，见 Eq. (4)）与2D追踪先验损失（Eq. (5)）的结合，能够精确恢复像素级的长时序对应关系。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/005_Table_2.jpg]]
*Table 2: Comparison of point-based tracking performance on the DyCheck [10] dataset*

### 消融研究

Table 3 和 Figure 4 展示了在 DyCheck 数据集上的消融实验结果，系统验证了各模块的贡献：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on the DyCheck dataset*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/006_Figure_4.jpg]]
*Figure 4: Visual comparison of ablation results*

- **阴影高斯模块（w/o Shadow）**：移除阴影高斯后 PSNR 从 17.98 降至 **16.26**，降幅达 1.72。这表明显式建模瞬态阴影对于处理真实场景中由光照变化引起的背景外观波动至关重要，尤其是在背景扩展阶段引入新帧时。
- **集群运动场 vs. 全局基（Global Bases）**：将集群运动场替换为全局基础变换使 PSNR 降至 **16.70**，降幅 1.28。这一显著差距证明局部集群基对于建模非刚体变形（如人体关节运动）是不可替代的——全局基无法捕捉不同空间区域运动模式的异质性。
- **自适应控制（w/o Adaptive Control）**：移除集群分裂与剪枝机制导致运动精度下降。自适应控制通过 HDBSCAN 识别运动不一致的高斯点群，并利用层次聚类将其分裂为独立集群，使运动场能够动态扩展表示容量以适配复杂场景演化。
- **三阶段前景传播（Three-stage Refinement）**：初始对齐、短期一致性和长期细化三个阶段缺一不可，移除任一步骤均会降低长时序运动传播的一致性。该结果验证了渐进式优化在扩展长视频时的必要性。

### 失败模式与局限性

尽管 MotionScale 取得了显著性能提升，分析揭示了若干需要人工验证的潜在失败模式：

1. **2D先验依赖性**：重建质量严重依赖深度估计和点追踪先验的准确性。在动态模糊严重或密集遮挡的场景中，2D先验的退化会直接传导至运动场优化，导致几何失真和追踪漂移。该点需在极端场景下进行人工验证。
2. **阴影高斯的适用范围**：阴影高斯模块仅处理简单瞬态阴影，对镜面反射、强光变化等复杂光照效应的建模能力有限。在包含高光或透明物体的场景中，渲染质量可能出现退化。
3. **计算开销**：渐进优化策略虽然提升了一致性，但三阶段细化和自适应控制引入了显著的计算开销，当前设计不适用于实时应用。
4. **语义盲区**：模型不包含语义理解能力，无法进行分割或结构化编辑。在需要语义感知的场景理解任务中存在天然局限。

### 待解决问题

基于上述分析，以下开放问题值得后续探索：

- 如何将语义先验引入集群运动场，实现场景的语义感知解耦与编辑？
- 能否通过模型压缩或高效推理策略降低计算成本，实现实时或移动端部署？
- 该方法在极端非朗伯体或透明物体场景中的鲁棒性如何？
- 能否利用多摄像头或额外传感器（如深度相机）进一步提升几何精度与运动鲁棒性？

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2603_29296/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of a reconstructed dynamic scene and extracted moving objects. Given a single monocular video as input, MotionScale reconstructs a 4D scene representation that effectively captures photorealistic appearance, accurate 3D geometry, diverse human motion. Refer to the supplementary material for video results and additional examples*

## 方法谱系与知识库定位

### 1. 动态场景表示的方法谱系

MotionScale 处于**基于高斯溅射（3DGS）的动态场景重建**这一活跃研究线上。该线路的核心挑战是在保持渲染效率的前提下，为单目视频中的非刚性运动建立可扩展、几何一致的4D表示。现有方法可大致分为两类：

**变形场路线**以 **Deformable 3DGS**（Yang et al., CVPR 2024）和 **4D-GS**（Yang et al., ICLR 2024）为代表，在规范空间维护一组静态高斯点，通过全局MLP预测每帧的位移或变形。这类方法的根本瓶颈在于**几何欠约束**：MLP缺乏对3D结构一致性的显式保证，导致高斯点在长序列中逐渐偏离真实表面，产生几何崩塌与运动漂移。

**稀疏控制点路线**以 **SC-GS**（Huang et al., CVPR 2024）和 **SplineGS**（Park et al., CVPR 2025）为代表，通过稀疏控制点或样条曲线驱动局部区域变形。这类方法在局部运动建模上更高效，但控制点的固定拓扑限制了表示能力的可扩展性——当场景包含多个独立运动对象或复杂非刚体变形时，固定容量的控制结构难以自适应扩展。

**4DGS**（Wu et al., CVPR 2024）直接优化每帧的高斯参数，虽然避免了变形场的欠约束问题，但逐帧独立优化牺牲了时序一致性，且存储开销随帧数线性增长。

MotionScale 在上述谱系中开辟了第三条路径：**集群中心的自适应层次运动基**。其核心差异在于：

| 维度 | 变形场路线 | 稀疏控制点路线 | MotionScale |
|------|-----------|---------------|-------------|
| 运动表示 | 全局MLP | 固定拓扑控制点 | 可分裂集群 + 层次运动基 |
| 几何约束 | 隐式，易漂移 | 局部显式 | 集群内显式 + 跨集群传播 |
| 容量扩展 | 固定 | 固定 | 自适应分裂/剪枝 |
| 长序列策略 | 一次性优化 | 一次性优化 | 渐进式背景-前景解耦 |

### 2. 关键设计选择与基线差异

**集群运动基 vs. 全局基**。消融实验（Table 3）表明，将集群层次运动场替换为全局基础变换（Global Bases）导致 PSNR 下降 1.28（17.98 → 16.70）。这一差距揭示了核心因果机制：全局基假设所有高斯点共享同一组变形模式，无法捕捉不同对象（如人体不同肢体）的独立运动。集群划分将运动场分解为局部刚体（全局 SE(3)）与局部非刚体基（B 个可学习旋转/平移基）的组合，使每个集群可以学习专属的运动子空间。

**自适应控制 vs. 固定拓扑**。与 SC-GS 的固定控制点不同，MotionScale 的自适应控制机制通过 HDBSCAN 检测运动不一致的高斯点，并利用 Agglomerative Clustering 将其分裂为独立集群。这一设计使运动场的容量随场景复杂度动态增长，而非预先分配。消融表明移除自适应控制导致运动精度显著下降（Sec. 4.5）。

**渐进式优化 vs. 一次性优化**。现有方法通常一次性优化整个序列，在长视频中面临误差累积。MotionScale 将优化解耦为背景扩展与前景传播两个阶段：背景阶段填充新帧的未观察区域并细化相机位姿，前景阶段通过三阶段细化（初始对齐 → 短期一致性 → 长期细化）将运动场逐步传播到新帧。这一策略使运动场始终锚定在已建立的背景几何上，抑制了长序列中的漂移。

**阴影高斯 vs. 无显式光照建模**。现有动态 3DGS 方法普遍忽略瞬时光照变化。MotionScale 引入专用的阴影高斯（Shadow Gaussians）显式建模场景中的瞬态阴影。消融显示移除该模块使 PSNR 从 17.98 降至 16.26（Table 3），表明光照变化是动态场景重建中不可忽视的误差源。

### 3. 与同期工作的关系

在点追踪能力上，MotionScale 与 **Shape of Motion**（Wang et al., ICCV 2025）和 **GFlow**（Wang et al., AAAI 2025）形成直接对比。Shape of Motion 通过隐式神经场学习运动先验，GFlow 利用光流引导变形。MotionScale 在 DyCheck 点追踪基准上达到 3D EPE 0.070、2D AJ 37.7、OA 0.87（Table 2），显著优于这些基线。其优势源于集群运动场提供的显式几何约束：每个高斯点的 3D 轨迹通过 alpha 混合直接计算（Eq. 4），并由 2D 追踪先验监督（Eq. 5），避免了隐式场中轨迹推断的不确定性。

**4D-Fly**（Wu et al., CVPR 2025）同样探索了动态场景的 4D 表示，但侧重于飞行视角合成。MotionScale 与 4D-Fly 在运动表示上存在互补性：前者强调可扩展的集群分解，后者关注视角泛化。

### 4. 适用边界与局限

**2D 先验依赖链**。MotionScale 的重建质量严重依赖深度估计和点追踪先验的准确性。在动态模糊严重或长时遮挡场景中，2D 先验失效会通过损失函数（Eq. 5、Eq. 6）反向传播至运动场，导致几何退化。这是一个结构性的脆弱点，而非实现细节问题。

**计算开销与实时性**。渐进式优化策略虽然提升一致性，但三阶段细化需要维护跨时间窗口的传播状态，计算开销显著高于一次性优化方法。当前设计不适用于实时或移动端部署。

**光照建模的局限性**。阴影高斯模块仅处理简单的瞬态阴影，对于镜面反射、次表面散射等复杂光照效应缺乏建模能力。在包含反射表面或极端光照变化的场景中，渲染质量可能显著下降。

**语义盲区**。当前运动场仅基于几何和运动一致性划分集群，未融入语义先验。这意味着同一对象的不同部件可能被分配到不同集群，而不同对象的相似运动可能被合并，限制了场景的语义感知编辑能力。

### 5. 开放问题

1. **语义感知的运动分解**：能否将语义分割或人体姿态先验引入集群划分，使运动场天然支持对象级编辑与重定向？
2. **计算效率的阶梯式优化**：是否可以通过粗粒度运动先验（如光流）引导集群初始化，减少自适应控制的迭代次数，从而降低渐进式优化的计算成本？
3. **极端材质的鲁棒性**：该方法在透明物体、非朗伯体表面或强镜面反射场景中的几何与运动恢复能力尚未验证，需要针对性评估。
4. **多传感器融合**：引入深度传感器或惯性测量单元能否为运动场提供更强的几何约束，降低对单目深度先验的依赖？
5. **4D 生成与编辑**：MotionScale 重建的 4D 表示能否作为生成模型的训练数据源，或支持运动迁移、场景插值等下游任务？

## 原文 PDF

![[paperPDFs/CVPR_2026/MotionScale_Reconstructing_Appearance_Geometry_and_Motion_of_Dynamic_Scenes_with_Scalable_4D_Gaussian_Splatting.pdf]]
