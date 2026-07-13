---
title: "Flow4DGS-SLAM: Optical Flow-Guided 4D Gaussian Splatting SLAM"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Flow4DGS_SLAM_Optical_Flow_Guided_4D_Gaussian_Splatting_SLAM.pdf
project_link: "https://wangys16.github.io/Flow4DGS-SLAM"
code_link: null
aliases:
- FS
- Flow4DGS-SLAM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 利用光流先验指导动态高斯的位置初始化、传播与自适应插入，并结合相机自运动诱导的运动分解，实现对动态场景的类别无关分割与高效训练。
primary_logic: 1) 通过拟合相机自运动模型并利用光流残差的中位数绝对偏差阈值，可以实现类别无关的动态像素掩码生成，提高动态环境中的跟踪鲁棒性；2) 将动态高斯表示为显式关键帧位置（线性插值）与高斯混合模型（GMM）控制的时变透明度和旋转，在保持训练高效的同时提升对复杂动态的重建能力；3) 利用场景流光流传播和回溯式自适应插入策略，加速动态高斯的在线训练并有效处理新出现的动态对象。
claims:
- 相机诱导运动分解模块在BONN数据集上显著提升跟踪精度和渲染质量。
- 流光传播和自适应插入模块在快速运动场景（如ballon2）中大幅提升重建质量。
- 混合4DGS表示使映射速度相比4DGS-SLAM提升超过17倍（6285 ms vs 110562 ms）。
- 在TUM RGB-D数据集上，本方法在轨迹ATE RMSE和渲染质量（PSNR/SSIM/LPIPS）上均达到最优。
---

# Flow4DGS-SLAM: Optical Flow-Guided 4D Gaussian Splatting SLAM

> [!tip] 核心洞察
> 1) 通过拟合相机自运动模型并利用光流残差的中位数绝对偏差阈值，可以实现类别无关的动态像素掩码生成，提高动态环境中的跟踪鲁棒性；2) 将动态高斯表示为显式关键帧位置（线性插值）与高斯混合模型（GMM）控制的时变透明度和旋转，在保持训练高效的同时提升对复杂动态的重建能力；3) 利用场景流光流传播和回溯式自适应插入策略，加速动态高斯的在线训练并有效处理新出现的动态对象。

| 字段 | 内容 |
|------|------|
| 中文题名 | Flow4DGS-SLAM: 光流引导的4D高斯溅射SLAM |
| 英文题名 | Flow4DGS-SLAM: Optical Flow-Guided 4D Gaussian Splatting SLAM |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.22339) · [Project](https://wangys16.github.io/Flow4DGS-SLAM) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Flow4DGS-SLAM |
| Dataset | TUM RGB-D, BONN |

> [!tip] 效果简介
> - TUM RGB-D 上，ATE RMSE [cm]↓ Avg. 1.9 vs 2.1 (4DGS-SLAM) (-0.2)；PSNR [dB]↑ Avg. 26.55 vs 22.55 (4DGS-SLAM) (+4.00)；SSIM↑ Avg. 0.831 vs 0.788 (4DGS-SLAM) (+0.043)。
> - BONN 上，ATE RMSE [cm]↓ Avg. 3.5 vs 3.9 (4DGS-SLAM) (-0.4)。

## 概要

**Flow4DGS-SLAM** 针对动态场景下的同时定位与建图（SLAM）提出了一种光流引导的4D高斯溅射方法。当前动态SLAM方法通常将动态对象视为异常值剔除以稳定跟踪，导致只能重建静态背景；而现有的动态3DGS重建方法依赖预计算的多视角位姿和长时间离线训练，无法在SLAM中在线高效地进行动态元素的重建与跟踪。

本方法的核心思路是**利用光流先验指导动态高斯的位置初始化、传播与自适应插入**，并结合相机自运动诱导的运动分解，实现对动态场景的类别无关分割与高效训练。具体而言，Flow4DGS-SLAM 提出三个关键机制：

1. **相机诱导运动分解（Camera-Induced Motion Decomposition）**：通过拟合相机自运动模型并利用光流残差的中位数绝对偏差（MAD）阈值，生成类别无关的动态像素掩码，在提高动态环境中跟踪鲁棒性的同时避免了对特定语义类别的依赖。
2. **混合4D高斯表示（Hybrid 4DGS）**：将动态高斯表示为显式关键帧位置（线性插值）与高斯混合模型（GMM）控制的时变透明度和旋转，在保持训练高效的同时提升对复杂动态的重建能力。
3. **场景流光流传播与自适应插入**：利用场景流光流传播已有高斯中心，并通过回溯式自适应插入策略初始化新出现动态区域的高斯，加速动态高斯的在线训练。

在**TUM RGB-D**数据集上，Flow4DGS-SLAM 在轨迹精度（ATE RMSE 平均 1.9 cm）和渲染质量（PSNR 平均 26.55 dB, SSIM 0.831, LPIPS 0.177）上均达到最优，相比最相关的动态3DGS SLAM基线 **4DGS-SLAM**（Li et al., 2025）分别提升 0.2 cm 和 4.00 dB。在**BONN**动态场景数据集上，相机诱导运动分解模块显著提升了跟踪精度和渲染质量，ATE RMSE 平均达到 3.5 cm。此外，混合4DGS表示使映射速度相比4DGS-SLAM提升超过17倍（6285 ms vs 110562 ms）。

该方法仍存在若干局限：依赖外部光流模型（RAFT）和语义分割模型（YOLOv9），其失效可能影响动态分割与高斯传播精度；主要针对RGB-D输入，深度缺失或噪声大的场景可能影响位姿估计；GMM时变建模假设动态对象的透明度与旋转连续变化，对快速、非连续外观变化的适应能力有限。

### 动态SLAM与3D重建的双重困境

同时定位与地图构建（SLAM）是机器人、增强现实和自动驾驶等领域的核心感知技术。近年来，基于3D高斯溅射（3D Gaussian Splatting, 3DGS）的SLAM方法在静态场景中取得了令人瞩目的进展——**MonoGS**（Matsuki et al., CVPR 2024）和**SplaTAM**（Keetha et al., CVPR 2024）等方法实现了高保真的隐式场景重建与精确的相机跟踪。然而，现实世界充斥着动态元素：行走的行人、移动的车辆、摆动的物体。这些动态对象对SLAM系统构成了根本性挑战。

当前应对这一挑战的主流策略呈现出一种**功能分裂**的态势：

一方面，动态SLAM方法——如**RoDyn-SLAM**（Jiang et al., IEEE RA-L 2024）——通常将动态对象视为需要剔除的“异常值”，通过语义分割或几何残差检测将其从跟踪过程中排除。这种策略虽然稳定了相机位姿估计，却付出了高昂的代价：**只能重建静态背景，动态元素被彻底丢弃**，无法满足对场景完整理解的需求。

另一方面，动态3DGS重建方法——如**SC-GS**（Huang et al., CVPR 2024）——虽然能够同时对静态背景和动态对象进行高质量重建，但它们**依赖预计算的多视角相机位姿和长时间的离线训练**。这些方法假设所有视角的位姿已知且精确，这在SLAM的在线增量式推理场景中是不现实的。

### 4DGS-SLAM的突破与局限

**4DGS-SLAM**（Li et al., 2025）是首个将动态3DGS引入SLAM系统的工作，试图弥合上述分裂。它通过MLP形变场对高斯原语进行时变建模，实现了动态场景下的在线跟踪与重建。然而，其设计存在两个关键瓶颈：

1. **计算效率低下**：MLP形变场需要为每个时间步推理所有动态高斯的变形，映射时间高达110562 ms，难以满足实时性需求。
2. **动态分割依赖类别先验**：基于语义分割的动态检测受限于预定义类别（如“人”），无法处理类别无关的运动物体（如被推动的椅子、滚动的球），泛化能力不足。

### 本文的核心动机

Flow4DGS-SLAM的提出正是为了突破上述瓶颈。其核心动机可以概括为三个递进的目标：

1. **实现类别无关的动态感知**：摆脱对语义类别的依赖，通过分析相机自运动与场景光流之间的物理关系，直接从运动线索中分离动态区域。
2. **提升动态高斯的训练效率**：用显式的、光流引导的位置建模替代隐式MLP形变场，大幅降低计算开销，使在线动态重建成为可能。
3. **保持甚至超越现有方法的精度**：在解决效率和泛化问题的同时，不牺牲跟踪精度与渲染质量。

这三个目标共同指向一个愿景：**让SLAM系统能够在动态世界中，既稳健地定位自身，又完整地重建所见的一切——无论它们是静止的背景，还是运动中的物体。**

## 核心方法与创新机理

Flow4DGS-SLAM 的核心创新在于通过**光流先验**重构了动态 SLAM 中“分割—表示—训练”三个环节的因果链条，实现了从“剔除动态”到“重建动态”的范式转换。与最相关的动态 3DGS SLAM 基线 **4DGS-SLAM**（Li et al., 2025）相比，该方法在以下四个关键维度（changed slots）上做出了实质性改变：

### 1. 类别无关的动态分割：相机诱导运动分解

传统动态 SLAM（如 **RoDyn-SLAM**, Jiang et al., IEEE RA-L 2024）依赖 YOLO 等语义分割器或几何残差来识别动态区域，受限于预定义类别且对未知运动物体泛化能力不足。Flow4DGS-SLAM 提出**相机诱导运动分解模块**（Camera-Induced Motion Decomposition），通过拟合相机自运动模型实现类别无关的运动分割：

- **核心机制**：利用深度图和先验光流，通过加权最小二乘拟合相机 6-DoF 运动 $\hat{\pmb{\xi}}$，预测纯刚体光流场 $\hat{\mathbf{F}}$。观测光流与预测刚体光流的残差 $r(u,v) = \lVert \mathbf{F} - \hat{\mathbf{F}} \rVert_2$ 反映像素的独立运动程度。
- **动态判定**：采用中位数绝对偏差（MAD）阈值策略——$\mathcal{M}_{ca}(u,v) = \mathbb{1}(r(u,v) > \text{median}(r) + k\text{MAD}(r))$——实现对动态像素的鲁棒、非参数化检测。
- **因果作用**：该模块不仅生成动态掩码以稳定跟踪，还提供光流引导的位姿初始化 $\mathbf{T}_{cw}^t = \mathbf{T}_{cw}^{t-1} \exp_{\mathfrak{se}(3)}(\hat{\xi}^*)$，形成从粗到精的跟踪管线。消融实验证实，移除该模块在 BONN 数据集上导致跟踪精度和渲染质量显著下降。

### 2. 混合 4D 高斯表示：显式位置 + GMM 时变属性

现有动态 3DGS 方法（如 **SC-GS**, Huang et al., CVPR 2024）通常采用 MLP 形变场或稀疏控制点变形来建模动态，计算开销大且训练缓慢。Flow4DGS-SLAM 提出**混合 4D 高斯表示**，将动态高斯的空间位置与时变外观属性解耦建模：

- **显式关键帧位置**：动态高斯中心在关键帧处显式存储，任意时刻 $t$ 的位置通过线性插值获得。这避免了形变场 MLP 的逐帧推理开销，是映射速度提升 17 倍以上的关键（6285 ms vs 4DGS-SLAM 的 110562 ms）。
- **GMM 控制的时变属性**：透明度通过 $K=3$ 个高斯成分激活的混合模型 $m_i(t) = 1 - \exp(-A_i \sum_{k=1}^K w_{i,k} \mathcal{N}(\hat{t}; \mu_{i,k}, \tau_{i,k}^2))$ 表示；旋转通过高斯权重平滑混合四元数得到。这种连续表示在保持时域平滑性的同时，参数量远小于逐帧存储方案。

### 3. 光流驱动的在线训练加速

传统动态重建方法依赖离线预计算多视角位姿和长时间优化，无法满足 SLAM 的在线需求。Flow4DGS-SLAM 引入两个光流驱动的模块实现高效在线训练：

- **场景流光流传播**（Scene Flow Gaussian Propagation）：利用前一关键帧的高斯中心与场景流光流，通过反投影估计粗略 3D 形变 $\Delta \mathbf{x}_i^k$，经 KNN 局部刚性平滑后传播到当前关键帧，作为动态高斯的初始位置。这大幅减少了从零优化所需的迭代次数。
- **自适应高斯插入**（Adaptive Gaussian Insertion）：通过光流回溯检测新出现的动态区域（如刚进入视野的物体），在无对应传播高斯的区域初始化新高斯，确保对新增动态对象的快速覆盖。

消融实验表明，移除这两个模块会使快速运动场景（如 ballon2）的重建质量大幅降低。

### 4. 光流引导的位姿初始化

与恒速模型或上一帧位姿的常规初始化不同，Flow4DGS-SLAM 利用相机诱导运动分解估计的 6-DoF 运动进行位姿初始化，形成从粗到精的跟踪管线。这一设计增强了在动态场景中跟踪的收敛鲁棒性，消融实验中移除该初始化（w/o Camera Init.）导致渲染出现明显伪影。

**需要手动验证的点**：GMM 组件数 $K=3$ 的选择依据在现有证据中仅体现为经验设定，缺乏不同 $K$ 值的系统对比实验支撑。此外，光流模型 RAFT 在无纹理区域的失效对动态分割和传播精度的级联影响，在现有消融中未被量化评估。

Flow4DGS-SLAM 的整体 pipeline 以 RGB-D 视频流作为输入，围绕**光流先验**构建了一条从动态分割、位姿初始化到动态高斯映射的闭环系统。如 Figure 2 所示，系统可分解为四个核心阶段：**预处理**、**相机诱导运动分解**、**跟踪**与**动态映射**。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of Flow4DGS-SLAM. Given input RGB-D video, we first extract the prior semantic mask and optical flow, and feed them into a camera-induced motion decomposition module to filter out category-agnostic motion mask and solve an optical-flow guided camera initialization. The static gaussians help refine the camera pose during tracking, and the dynamic Gaussians are represented in a hybrid form, combined with a scene flow Gaussian propagation module and an adaptive gaussian insertion module to accelerate training*

### 输入与预处理

系统接收连续的 RGB-D 帧，并实时调用两个外部模型：**RAFT** 提取稠密光流，**YOLOv9** 生成基于类别的语义先验掩码。光流同时服务于运动分解模块和高斯传播模块，语义掩码则为后续的动态掩码融合提供先验。

### 相机诱导运动分解

该模块是连接感知与状态估计的**核心因果旋钮**。它利用深度图和光流，通过拟合刚体光流方程求解相机自运动：

$$ \mathbf { F } ( u , v ) = \mathbf { J } ( { \pmb x } ) { \pmb \xi } $$

其中 $\mathbf{J}(\pmb{x})$ 为 $2\times 6$ 图像雅可比矩阵，将相机 twist $\pmb{\xi}$ 映射到图像光流。通过 Cauchy 加权的迭代最小二乘估计 $\hat{\pmb{\xi}}$，模块计算出每个像素的光流残差 $r(u,v)$，并以中位数绝对偏差（MAD）阈值生成类别无关的动态掩码：

$$ \mathcal { M } _ { c a } ( u , v ) = \mathbb { 1 } \left( r ( u , v ) > \mathrm { m e d i a n } ( r ) + k \mathrm { M A D } ( r ) \right) $$

该掩码与 YOLOv9 语义掩码融合后形成最终动态掩码 $\mathcal{M}_{dy}$。同时，估计的相机运动 $\hat{\pmb{\xi}}$ 用于光流引导的位姿初始化，形成从粗到精的跟踪管线，提升动态场景下的鲁棒性。

### 跟踪

跟踪阶段仅依赖**静态高斯**渲染的颜色和深度图，通过有效掩码 $\mathcal{M}_v = (\neg \mathcal{M}_{dy}) \cap \mathcal{M}_o$ 排除动态区域和不可见像素，对位姿进行优化：

$$ \mathcal { L } _ { t r a c k } = \frac { 1 } { | \mathcal { V } | } \sum _ { \pmb { u } \in \mathcal { V } } \mathcal { M } _ { v } ( \pmb { u } ) \left( \lambda _ { 1 } L _ { 1 } ( \hat { \mathbf { C } } ( \pmb { u } ) ) + \lambda _ { 2 } L _ { 1 } ( \hat { \mathbf { D } } ( \pmb { u } ) ) \right) $$

### 动态映射

动态映射采用**混合 4DGS 表示**：每个动态高斯的位置由显式关键帧位置经线性插值获得，时变透明度和旋转则由 $K=3$ 的高斯混合模型（GMM）控制。为加速训练，系统引入两个关键模块：

1. **场景流光流传播**：将前一关键帧的动态高斯中心通过场景流光流传播到当前关键帧，作为动态高斯初始化的种子。
2. **自适应高斯插入**：通过光流回溯检测新出现的动态区域，并初始化新高斯以覆盖这些区域。

传播后的 3D 形变通过反投影估计并经 KNN 平滑保持局部刚性。映射总损失联合颜色、深度、光流、掩码和各向同性正则项：

$$ \mathcal { L } _ { m a p } = \lambda _ { 1 } \mathcal { L } _ { c } + \lambda _ { 2 } \mathcal { L } _ { d } + \lambda _ { f } \mathcal { L } _ { f } + \lambda _ { m } \mathcal { L } _ { m } + \lambda _ { i s o } \mathcal { L } _ { i s o } $$

### 模块间数据流

光流作为贯穿全系统的信号载体：在运动分解中驱动动态分割和位姿初始化，在映射中指导高斯传播和自适应插入。这种设计使得各模块共享同一先验，避免了多源信息融合的冲突，同时将动态分割从类别依赖中解耦，实现了对未知动态对象的泛化能力。

### 3.1 相机诱导运动分解模块

该模块是系统实现类别无关动态分割的核心。给定输入 RGB-D 帧，首先利用现成的光流估计器和语义分割模型（YOLOv9）提取先验光流场 $\mathbf{F}$ 和语义掩码。随后，通过拟合相机自运动模型，将观测光流分解为由相机运动诱导的刚体光流和由动态物体引起的残差光流。

**刚体光流方程**：对于三维空间中的静态点 $\mathbf{x} = (X, Y, Z)^\top$，其在微小相机运动下的运动场可表示为：

$$\mathbf{F}(u, v) = \mathbf{J}(\mathbf{x}) \, \boldsymbol{\xi}$$

其中 $\boldsymbol{\xi} \in \mathfrak{se}(3)$ 为相机位姿的 twist 参数，$\mathbf{J}(\mathbf{x})$ 为 $2 \times 6$ 的图像雅可比矩阵：

$$\mathbf{J}(\mathbf{x}) = \begin{bmatrix} -\frac{f_x}{Z} & 0 & \frac{u}{Z} & \frac{uv}{f_y} & -f_x - \frac{u^2}{f_x} & v \\ 0 & -\frac{f_y}{Z} & \frac{v}{Z} & f_y + \frac{v^2}{f_y} & -\frac{uv}{f_x} & -u \end{bmatrix}$$

这里 $f_x, f_y$ 为相机焦距，$(u, v)$ 为像素坐标，$Z$ 为该像素对应的深度值。

**加权最小二乘估计**：为求解相机自运动 $\boldsymbol{\xi}$，在剔除语义先验动态区域后的剩余像素上，使用 Cauchy 加权迭代最小二乘：

$$\hat{\boldsymbol{\xi}} = \arg\min_{\boldsymbol{\xi}} \sum_i w_i \, \| \mathbf{F}_i - \mathbf{J}_i \boldsymbol{\xi} \|^2$$

其中 $w_i$ 为 Cauchy 鲁棒权重，用于抑制残差异常大的像素（即实际动态点）对估计的干扰。

**类别无关动态掩码生成**：求解 $\hat{\boldsymbol{\xi}}$ 后，计算每个像素的光流残差：

$$r(u, v) = \lVert \mathbf{F}(u, v) - \hat{\mathbf{F}}(u, v) \rVert_2$$

其中 $\hat{\mathbf{F}} = \mathbf{J}\hat{\boldsymbol{\xi}}$ 为预测的刚体光流。基于残差的中位数绝对偏差（MAD）阈值，生成类别无关的动态掩码：

$$\mathcal{M}_{ca}(u, v) = \mathbb{1}\big(r(u, v) > \text{median}(r) + k \, \text{MAD}(r)\big)$$

该掩码与 YOLOv9 提供的语义先验掩码取并集，形成最终动态掩码 $\mathcal{M}_{dy}$。同时，估计的运动 $\hat{\boldsymbol{\xi}}$ 用于光流引导的相机位姿初始化：

$$\mathbf{T}_{cw}^t = \mathbf{T}_{cw}^{t-1} \exp_{\mathfrak{se}(3)}(\hat{\boldsymbol{\xi}}^*)$$

形成从粗到精的跟踪管线，提升动态环境下的鲁棒性。

### 3.2 混合4D高斯表示

为高效表示动态场景，本方法将场景显式分解为静态高斯 $\mathcal{G}^s$ 和动态高斯 $\mathcal{G}^d$。静态高斯的渲染沿用标准 3DGS 的 alpha 混合：

$$\hat{\mathbf{C}}^s(\mathbf{u}) = \sum_{i=1}^{|\mathcal{G}^s|} c_i^s \alpha_i^s(\mathbf{u}) \prod_{j<i} (1 - \alpha_j^s(\mathbf{u}))$$

动态高斯则采用混合表示，联合显式关键帧位置与 GMM 控制的时变属性。

**显式关键帧位置**：动态高斯的位置在离散关键帧时刻 $t_k$ 显式存储为 $\mathbf{x}_i^k$。在任意时刻 $t \in [t_{k-1}, t_k]$，其位置通过线性插值获得：

$$\mathbf{x}_i(t) = \frac{t_k - t}{t_k - t_{k-1}} \mathbf{x}_i^{k-1} + \frac{t - t_{k-1}}{t_k - t_{k-1}} \mathbf{x}_i^k$$

这种显式位置建模避免了形变场 MLP 的昂贵推理，是实现快速映射的关键。

**GMM 时变透明度**：透明度系数由 $K$ 个高斯成分的混合模型控制（实验中设 $K=3$）：

$$m_i(t) = 1 - \exp\left(-A_i \sum_{k=1}^{K} w_{i,k} \, \mathcal{N}(\hat{t}; \mu_{i,k}, \tau_{i,k}^2)\right)$$

其中 $\hat{t}$ 为归一化时间，$A_i$ 为基准幅度，$w_{i,k}$、$\mu_{i,k}$、$\tau_{i,k}^2$ 分别为第 $k$ 个成分的权重、均值和方差。该公式使透明度随时间平滑变化，适应动态对象的出现与消失。

**GMM 时变旋转**：旋转四元数同样通过 GMM 权重平滑混合：

$$\mathbf{q}_i(t) = \frac{\sum_{k=1}^{K} w_{i,k} \, \mathcal{N}(\hat{t}; \mu_{i,k}, \tau_{i,k}^2) \, \mathbf{q}_{i,k}}{\left\| \sum_{k=1}^{K} w_{i,k} \, \mathcal{N}(\hat{t}; \mu_{i,k}, \tau_{i,k}^2) \, \mathbf{q}_{i,k} \right\|}$$

这保证了旋转插值的光滑性和单位模长约束。GMM 的混合权重 $w_{i,k}$ 在透明度与旋转之间共享，减少了参数量。

### 3.3 跟踪损失

跟踪阶段仅使用静态高斯渲染颜色和深度图，并在有效掩码区域内优化相机位姿。有效掩码 $\mathcal{M}_v$ 由两部分交集构成：动态掩码的取反 $(\neg \mathcal{M}_{dy})$ 和基于渲染不透明度的掩码 $\mathcal{M}_o$：

$$\mathcal{M}_o(\mathbf{u}) = \mathbb{1}\big(\hat{\mathbf{O}}(\mathbf{u}) \geq \alpha\big)$$

跟踪损失为颜色和深度的 L1 损失：

$$\mathcal{L}_{track} = \frac{1}{|\mathcal{V}|} \sum_{\mathbf{u} \in \mathcal{V}} \mathcal{M}_v(\mathbf{u}) \left( \lambda_1 L_1(\hat{\mathbf{C}}(\mathbf{u})) + \lambda_2 L_1(\hat{\mathbf{D}}(\mathbf{u})) \right)$$

### 3.4 场景流光传播与自适应插入

为加速动态高斯的在线训练，本方法引入两个关键模块。

**场景流光高斯传播**：当新关键帧 $k$ 到来时，利用前一关键帧 $k-1$ 已优化的动态高斯中心 $\mathbf{x}_i^{k-1}$，通过先验光流进行传播。首先将 $\mathbf{x}_i^{k-1}$ 投影到帧 $k-1$ 的图像平面，获取光流向量后得到在帧 $k$ 的投影位置 $\bar{\mathbf{u}}_i^k$，再结合深度 $D_i^k$ 反投影得到粗略的 3D 形变：

$$\Delta \mathbf{x}_i^k = \mathbf{R}_k^\top \left( D_i^k \mathbf{K}^{-1} \bar{\mathbf{u}}_i^k - \mathbf{t}_k \right) - \mathbf{x}_i^{k-1}$$

其中 $\mathbf{R}_k, \mathbf{t}_k$ 为帧 $k$ 的相机位姿，$\mathbf{K}$ 为内参矩阵。为保持局部刚性，对形变进行 KNN 平滑：

$$\Delta \widehat{\mathbf{x}}_i^k = \sum_{j \in \mathcal{N}(i)} w_{ij}^{knn} \, \Delta \mathbf{x}_j^k$$

传播后的高斯中心初始化为 $\mathbf{x}_i^k = \mathbf{x}_i^{k-1} + \Delta \widehat{\mathbf{x}}_i^k$。

**自适应高斯插入**：对于新出现的动态区域（如刚进入视野的物体），光流回溯检测未被现有高斯覆盖的像素，并在对应 3D 位置初始化新的动态高斯，确保快速收敛和完整覆盖。

### 3.5 映射总损失

映射阶段联合优化静态和动态高斯的所有属性，总损失为：

$$\mathcal{L}_{map} = \lambda_1 \mathcal{L}_c + \lambda_2 \mathcal{L}_d + \lambda_f \mathcal{L}_f + \lambda_m \mathcal{L}_m + \lambda_{iso} \mathcal{L}_{iso}$$

其中 $\mathcal{L}_c$、$\mathcal{L}_d$ 为颜色和深度渲染损失，$\mathcal{L}_f$ 为光流一致性损失，$\mathcal{L}_m$ 为动态掩码监督损失，$\mathcal{L}_{iso}$ 为各向同性正则项，用于约束高斯的形状。

## 实验与关键发现

### 主结果

#### TUM RGB-D 数据集

Flow4DGS-SLAM 在 TUM RGB-D 动态序列上同时评估了相机跟踪精度和渲染质量。跟踪方面，本方法取得了平均 ATE RMSE **1.9 cm**，优于最相关的动态基线 **4DGS-SLAM**（Li et al., 2025）的 2.1 cm，也显著超过静态 3DGS SLAM 方法 **MonoGS**（Matsuki et al., CVPR 2024）和 **SplaTAM**（Keetha et al., CVPR 2024），以及动态 RGB-D SLAM **RoDyn-SLAM**（Jiang et al., IEEE RA-L 2024）（见 Table 1）。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/003_Table_1.jpg]]
*Table 1: Trajectory ATE RMSE [cm]↓ on the TUM RGB-D sequences. Best results are shown in bold*

渲染质量方面，本方法在三个指标上均达到最优：平均 PSNR **26.55 dB**、SSIM **0.831**、LPIPS **0.177**。相比 4DGS-SLAM（PSNR 22.55 dB / SSIM 0.788 / LPIPS 0.229），PSNR 提升 **+4.00 dB**，LPIPS 降低 **0.052**（见 Table 2）。这表明混合 4DGS 表示与光流引导的传播策略在保持高保真渲染的同时有效处理了动态内容。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on the TUM RGB-D sequences. Best results are highlighted in bold*

#### BONN 数据集

在更具挑战性的 BONN 动态场景数据集上，Flow4DGS-SLAM 同样展现出优势。平均 ATE RMSE 为 **3.5 cm**，优于 4DGS-SLAM 的 3.9 cm（见 Table 3）。在渲染质量上，本方法在多个序列上取得了显著提升，而 4DGS-SLAM 在某些序列（如 *ballon2*）上出现重建失败（Table 4 中以“-”标示），进一步验证了相机诱导运动分解模块在动态场景中的鲁棒性优势。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/005_Table_3.jpg]]
*Table 3: Trajectory ATE RMSE [cm]↓ on the BONN sequences. Best results are highlighted in bold*

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/006_Table_4.jpg]]
*Table 4: Quantitative results on the BONN sequences. Best scores are shown in bold. “-” indicates reconstruction failure*

### 消融实验

消融实验（见 Table 6）揭示了各核心模块的贡献：

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2604_22339/figures/010_Table_6.jpg]]
*Table 6: Ablation study*

1. **相机诱导运动分解模块（w/o Motion Decomp.）**：移除该模块后，跟踪精度和渲染质量均显著下降，尤其在 BONN 数据集上退化明显。这验证了类别无关动态掩码对动态环境中位姿估计鲁棒性的关键作用。

2. **光流引导的位姿初始化（w/o Camera Init.）**：取消该初始化后，跟踪精度下降，说明利用估计的相机自运动进行粗到细的位姿初始化有助于提升优化收敛的稳定性。

3. **流光传播与自适应插入模块**：移除这两个模块后，快速运动场景（如 *ballon2*）的重建质量大幅降低。这表明显式关键帧位置建模依赖光流传播来加速动态高斯的在线训练，而自适应插入机制则确保了对新出现动态区域的及时覆盖。

4. **混合 4DGS 表示的效率**：Table 5 显示，本方法的映射时间仅为 **6285 ms**，而 4DGS-SLAM 需要 **110562 ms**，速度提升超过 **17 倍**。该加速主要归因于显式关键帧位置（线性插值）替代了基于 MLP 的形变场，同时 GMM 时变属性（K=3）在保持表达能力的前提下避免了逐帧存储或复杂映射的开销。

### 失败模式与局限性

尽管 Flow4DGS-SLAM 在多个基准上表现优异，其性能仍受以下因素制约：

- **外部模型依赖**：动态分割依赖 RAFT 光流模型和 YOLOv9 语义分割模型的输出。在无纹理区域（如白墙），RAFT 光流估计可能失效，导致相机诱导运动分解模块生成的动态掩码不准确，进而影响跟踪和高斯传播精度。同样，YOLOv9 的语义先验主要覆盖人形动态对象，对车辆等非人动态物体的泛化性受限。

- **深度输入质量**：方法针对 RGB-D 输入设计，深度图的缺失或噪声会直接影响位姿估计中的反投影精度和动态掩码的几何一致性判断。

- **GMM 时变建模假设**：GMM 假设动态对象的透明度和旋转随时间连续变化，对于快速、非连续的外观突变（如物体瞬间出现或消失）适应能力有限。

## 定位与知识库关联

### 一、与动态SLAM基线的定位关系

Flow4DGS-SLAM 在动态场景SLAM的谱系中处于一个交叉路口：它既不同于传统动态SLAM将动态物体视为“异常值”剔除的策略，也不同于离线动态重建方法对预计算位姿的依赖。具体而言：

**相对于动态RGB-D SLAM基线**（如 **RoDyn-SLAM**，Jiang et al., IEEE RA-L 2024），Flow4DGS-SLAM 的核心分歧在于对动态物体的处理哲学。RoDyn-SLAM 等传统方法的目标是**在动态环境中稳定跟踪相机位姿**，动态区域仅作为需要过滤的噪声源。Flow4DGS-SLAM 则在此基础上向前迈出一步：不仅过滤动态区域以稳定跟踪，还**主动建模和重建动态对象**。这一转变的关键在于相机诱导运动分解模块——它通过拟合相机自运动模型并利用光流残差的中位数绝对偏差（MAD）阈值，生成类别无关的动态掩码（Eq. 5a），从而在不依赖语义先验的情况下识别运动区域。

**相对于静态3DGS SLAM基线**（如 **MonoGS**，Matsuki et al., CVPR 2024；**SplaTAM**，Keetha et al., CVPR 2024），Flow4DGS-SLAM 的增量在于将场景表示从静态3D高斯扩展到4D时空域。MonoGS 和 SplaTAM 在动态场景中会因动态物体的渲染误差而损害跟踪精度和重建质量。Flow4DGS-SLAM 通过引入动态高斯分支，将静态背景与动态前景解耦建模，使两者互不干扰。

**相对于最相关的动态3DGS SLAM基线 4DGS-SLAM**（Li et al., 2025），Flow4DGS-SLAM 在三个关键维度上实现了改进：

1. **动态分割方式**：4DGS-SLAM 依赖语义分割或几何残差识别动态区域，而 Flow4DGS-SLAM 的相机诱导运动分解实现了类别无关的运动分割，理论上可泛化至任意运动物体（包括非语义对象如滚动的球、移动的椅子等）。

2. **动态高斯表示**：4DGS-SLAM 使用基于MLP的形变场或稀疏控制点来建模动态，训练计算量大。Flow4DGS-SLAM 采用混合4D高斯表示——显式关键帧位置（线性插值）+ GMM控制的时变透明度和旋转（Eq. 9, Eq. 10），在保持表达能力的同时大幅降低计算开销。实验表明，映射速度从 4DGS-SLAM 的 110,562 ms 降至 6,285 ms，**加速超过17倍**（Table 5）。

3. **训练加速机制**：场景流光流传播模块和自适应高斯插入模块利用光流先验进行高斯中心传播和新出现区域的回溯式初始化，加速了动态高斯的在线训练收敛。

### 二、与离线动态重建方法的边界

Flow4DGS-SLAM 与离线动态3DGS重建方法（如 **SC-GS**，Huang et al., CVPR 2024）的根本区别在于**在线性**。SC-GS 等方法假设多视角位姿已通过SfM预先计算，可在离线条件下进行长时间优化。Flow4DGS-SLAM 则必须在SLAM的在线约束下工作——位姿估计与场景建图交替进行，计算预算严格受限。这一边界决定了 Flow4DGS-SLAM 的设计取舍：牺牲部分重建精度以换取实时性，同时通过光流引导的初始化策略弥补在线训练的收敛劣势。

### 三、适用边界与局限

基于已验证的分析，Flow4DGS-SLAM 的适用边界受以下因素制约：

**1. 对外部模型的依赖**：方法依赖 RAFT 光流模型和 YOLOv9 语义分割模型作为前置模块。在无纹理区域（如白墙、均匀地面），RAFT 光流可能失效，导致：(a) 相机诱导运动分解的动态掩码精度下降；(b) 场景流光流传播模块无法正确传播高斯中心。同样，YOLOv9 的语义先验主要针对行人等常见动态类别，对非人动态物体（如车辆、动物）的泛化性受限。

**2. 深度传感器依赖**：当前方法针对 RGB-D 输入设计，深度图的质量直接影响：(a) 刚体光流方程中图像雅可比矩阵的计算精度（Eq. 2）；(b) 3D形变估计中反投影的准确性（Section 3.4）。在深度缺失或噪声大的场景（如远距离、镜面反射表面），位姿估计和动态掩码生成均可能退化。

**3. GMM时变建模的假设**：GMM控制的时变透明度和旋转假设动态对象的外观变化是**连续且平滑的**。对于快速、非连续的外观变化（如物体突然出现/消失、剧烈形变），K=3的高斯混合模型可能无法充分捕捉。这一假设的有效性边界尚需在更极端的动态场景中验证。

**4. 快速运动场景的鲁棒性**：虽然场景流光流传播和自适应插入模块在 ballon2 等快速运动场景中表现出色（消融实验证实），但当运动速度超过光流模型的有效范围时，传播和插入策略的精度将下降。论文未给出该方法能处理的最大运动速度的定量边界。

### 四、开放问题

1. **单目/立体扩展**：该方法能否扩展到无深度信息的单目或立体设置？这将涉及深度估计与动态分割的联合优化，可能需要在相机诱导运动分解模块中引入深度不确定性建模。

2. **表示迁移性**：光流引导的显式传播策略能否与其他3D表示（如NeRF、三平面）结合？该策略的核心是“利用运动先验加速动态表示训练”，这一思想可能具有跨表示的通用性。

3. **GMM组件数自适应**：当前K=3是固定设置（实验验证为最佳平衡）。能否根据场景动态复杂度自适应选择K？例如，在动态简单的场景使用较小的K以节省计算，在动态复杂的场景使用较大的K以提升表达能力。

4. **长期运行的累积误差**：SLAM系统在长期运行中面临累积漂移问题。Flow4DGS-SLAM 的动态高斯表示是否会在长时间序列中出现形变累积？是否需要引入全局优化或回环检测机制？

5. **多动态对象交互**：当前方法将动态区域作为一个整体处理。当场景中存在多个相互遮挡、交互的动态对象时，GMM时变建模和光流传播策略是否需要扩展为多实例感知的形式？

## 原文 PDF

![[paperPDFs/CVPR_2026/Flow4DGS_SLAM_Optical_Flow_Guided_4D_Gaussian_Splatting_SLAM.pdf]]
