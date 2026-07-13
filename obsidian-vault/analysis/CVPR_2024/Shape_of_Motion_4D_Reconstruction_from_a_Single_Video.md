---
title: "Shape of Motion: 4D Reconstruction from a Single Video"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Shape_of_Motion_4D_Reconstruction_from_a_Single_Video.pdf
project_link: https://shape-of-motion.github.io/
code_link: null
aliases:
- SM
- SM4RFSV
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "显式建模持久3D点云的运动，并将其表示为少量共享SE(3)运动基的线性组合，从而捕捉运动的低维结构；同时融合单目深度和长距离2D跟踪作为互补噪声信号，通过优化获得全局一致的4D表示。"
primary_logic: "1) 3D场景运动是低维的，可以分解为少量刚体运动基的线性组合，这为运动提供强大先验；2) 现代数据驱动先验（深度估计和点跟踪）尽管有噪声，但可以整合到一个统一的长期4D表示中，相互纠正并产生高保真度的新视角和3D跟踪。"
claims:
- "与直接将2D跟踪提升到3D的方法（TAPIR+DA）相比，我们的方法在3D跟踪EPE上降低了28%（0.114→0.082），验证了运动基融合的有效性。"
- "消融实验表明，2D跟踪监督对3D跟踪性能至关重要；移除该监督会导致性能大幅下降。"
- "使用SE(3)运动基显著优于平移运动基或逐点运动，验证了低维刚体运动表示的重要性。"
- "我们的方法在iPhone数据集上实现了最佳新视角合成质量，同时生成最平滑、最准确的3D轨迹，优于所有动态NeRF和3D-GS基线。"
---

# Shape of Motion: 4D Reconstruction from a Single Video

> [!tip] 核心洞察
> 1) 3D场景运动是低维的，可以分解为少量刚体运动基的线性组合，这为运动提供强大先验；2) 现代数据驱动先验（深度估计和点跟踪）尽管有噪声，但可以整合到一个统一的长期4D表示中，相互纠正并产生高保真度的新视角和3D跟踪。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 运动形状：从单目视频进行4D重建 |
| 英文题名 | Shape of Motion: 4D Reconstruction from a Single Video |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2407.13764) · [Project](https://shape-of-motion.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Shape of Motion |
| Dataset | iPhone dataset, Kubric dataset |

> [!tip] 效果简介
> - iPhone dataset 上，3D EPE↓ 为 0.082，对比 0.114 (TAPIR+DA)，变化 -28%。
> - iPhone dataset 上，2D AJ↑ 为 34.4，对比 27.8 (TAPIR)，变化 +23.7%。
> - iPhone dataset 上，PSNR↑ (NVS) 为 16.72，对比 16.54 (DynMF)，变化 +0.18 dB。

## 概要

从单目视频中重建完整的动态4D场景是一个高度病态的问题：单视角观测天然缺失深度、运动和多视角信息，导致现有方法要么仅能恢复短程场景流，要么无法同时产生高质量的3D运动估计和新视角合成。

**Shape of Motion** 提出了一种新的4D重建范式，其核心思想是显式建模持久3D点云的运动轨迹，并将这些运动表示为少量全局共享的SE(3)刚体运动基的线性组合。这一设计抓住了场景运动的低维结构——复杂动态场景中的运动通常可分解为少数刚体运动分量的叠加。同时，该方法将现代数据驱动先验（单目深度估计和长距离2D点跟踪）作为互补的监督信号，尽管这些信号各自带有噪声，但通过整合到统一的长期4D表示中，它们能够相互纠正，最终产生全局一致的动态场景重建。

方法在三个任务维度上实现了统一：**长程3D点跟踪**、**2D点跟踪**和**新视角合成**。在iPhone数据集上，Shape of Motion的3D跟踪误差（EPE）相比直接将2D跟踪提升到3D的方法（TAPIR+DA）降低了28%（0.114→0.082），同时在新视角合成质量上超越了所有动态NeRF和3D-GS基线。消融实验证实，SE(3)运动基表示和2D跟踪监督是性能的关键支撑——替换为平移运动基后3D EPE从0.082恶化至0.206，移除2D跟踪监督同样导致性能大幅下降。

该方法在方法谱系中处于**动态3D高斯泼溅**与**数据驱动先验融合**的交汇点，其定位区别于仅做新视角合成的动态NeRF/3D-GS方法（如HyperNeRF、Deformable-3D-GS），也区别于仅做2D/3D跟踪的方法（如TAPIR、SpatialTracker），而是首次在统一框架下同时完成这两类任务。

从单目视频重建动态三维场景是计算机视觉中的一个根本性难题。人类仅凭一段手机拍摄的视频，就能毫不费力地理解场景中物体的三维形状和运动轨迹——哪些部分在运动、它们如何移动、彼此之间有何关系。然而，让计算机完成同样的任务仍然极具挑战。

**核心瓶颈：一个高度病态的问题。** 单目视频的动态重建之所以困难，在于它同时缺少三类关键信息：深度（单帧中每个像素到相机的距离）、运动（像素在帧间的对应关系）和多视角信息（从不同角度观察场景的能力）。现有方法往往只能解决其中一部分问题——基于变形场的方法（如 HyperNeRF、Deformable-3D-GS）可以合成新视角，但无法产生世界坐标系下全视频范围的持久三维轨迹；而基于二维跟踪的方法（如 TAPIR、CoTracker）虽然能追踪像素运动，却只能停留在二维平面上，无法提升到三维理解。这种“各管一摊”的局面，使得同时获得高质量的新视角合成和长程三维运动跟踪成为一个尚未被填补的空白。

**因果性调节变量：运动的低维结构。** 尽管场景中可能包含大量移动元素，但其底层运动通常具有低维特性——场景中的绝大多数运动可以分解为少数几个“运动基元”的组合。例如，一个场景中可能有几个刚体物体各自独立运动，而每个物体上的所有点共享相同的刚体变换。这一观察提供了一个强有力的先验：如果我们能显式地建模这种低维运动结构，就能从稀疏、有噪声的观测信号中恢复出全局一致的三维运动。

**本文动机：融合互补信号，构建统一的四维表示。** 近年来，数据驱动的先验模型取得了长足进步——单目深度估计（如 Depth Anything）可以预测每帧的相对深度，二维点跟踪器（如 TAPIR）可以在长视频中追踪任意像素的对应关系。尽管这些预测各自带有噪声和误差，但它们提供了互补的信息：深度估计给出单帧的三维线索，二维跟踪给出跨帧的对应关系。本文的核心动机是：能否将这些互补的噪声信号整合到一个统一的、持久的四维场景表示中，让它们相互纠正、相互增强，从而同时获得高保真的新视角合成和精确的长程三维运动跟踪？

## 核心方法与创新机理

### 1. 问题瓶颈与设计动机

单目视频的动态4D重建面临一个根本性的病态问题：从二维投影中恢复三维几何和运动，同时缺失深度、多视角和运动先验信息。现有方法在此问题上存在明显的功能割裂——动态NeRF或3D-GS方法（如HyperNeRF、Deformable-3D-GS）仅能进行新视角合成，无法输出世界坐标系下的长程3D运动轨迹；而2D/3D跟踪方法（如TAPIR+DA、CoTracker+DA）虽然能跟踪特征点，却无法渲染新视角。Shape of Motion 的核心设计动机正是弥合这一鸿沟：在一个统一的4D表示中同时实现高质量的3D跟踪和新视角合成。

### 2. 关键机制创新：低维运动基表示

本方法的核心创新在于显式建模持久3D点云的运动，并将其表示为少量共享SE(3)运动基的线性组合。这一设计基于一个关键的因果洞察：**自然场景中的3D运动具有低维结构**——场景中不同物体的运动往往可以分解为少数几个刚体运动模式的叠加。

具体而言，方法定义了 $B \ll N$ 个全局共享的可学习基轨迹 $\{\mathbf{T}_{0t}^{(b)}\}_{b=1}^B$（$B=10$），每个3D高斯的运动变换由这些基的加权和给出：

$$\mathbf{T}_{0t} = \sum_{b=0}^B \mathbf{w}^{(b)} \mathbf{T}_{0t}^{(b)}$$

其中 $\mathbf{w}^{(b)}$ 是每个高斯独有的运动系数。这种参数化方式带来了三个关键优势：
- **运动先验的强约束**：低维基表示强制场景运动遵循少数刚体模式，有效抑制了单目重建中的歧义性。
- **遮挡区域的运动推断**：由于运动基是全局共享的，可见区域的运动模式可以自然传播到被遮挡区域。
- **软分解能力**：每个点的运动是多个基的线性组合，允许刚体运动组之间的平滑过渡，而非硬性分割。

消融实验（Table 4）直接验证了这一设计的决定性作用：将SE(3)运动基替换为平移运动基后，3D跟踪的EPE从0.082急剧增加到0.206；而采用逐点独立运动（per-Gaussian motion）同样导致性能大幅下降。

### 3. 监督信号的互补融合

方法的第二个关键创新在于**将现代数据驱动先验整合为互补的监督信号**。传统动态重建方法主要依赖多视角RGB或稀疏深度，而Shape of Motion同时融合了三个信号源：

- **单目深度估计**（Depth Anything）：提供逐帧的几何先验，尽管存在尺度模糊和局部噪声。
- **长距离2D跟踪**（TAPIR）：提供跨帧的对应关系，作为运动监督的核心信号。
- **RGB重建损失**：约束外观一致性。

这些信号各自有噪声且不完整，但通过联合优化可以相互纠正：深度估计约束了3D几何，2D跟踪约束了跨帧运动，而运动基的低维结构则作为正则化器抑制噪声传播。消融实验表明，**完全移除2D跟踪监督会导致3D跟踪性能的显著崩溃**（Table 4），证实了该信号在运动学习中的不可替代性。

### 4. 结构化初始化策略

与通常的随机初始化不同，Shape of Motion 采用了一个精心设计的初始化流程，将噪声观测转化为有效的初始解：

1. **运动基初始化**：对提升到3D的噪声轨迹速度进行k-means聚类，然后通过加权Procrustes对齐求解每个聚类的SE(3)变换，作为运动基的初始值。
2. **动态高斯初始化**：从初始3D轨迹中随机采样 $N$ 个位置作为规范帧下的高斯均值。
3. **静态高斯初始化**：利用对齐后的深度图反投影初始化静态场景部分。

消融实验（Table 4）显示，跳过SE(3)初始化步骤会导致性能明显下降，表明良好的初始化对于后续优化的收敛至关重要。

### 5. 输出能力的范式转变

从功能角度看，Shape of Motion 实现了从“单一任务”到“联合输出”的范式转变。与基线方法的对比清晰展示了这一差异：

| 方法类型 | 新视角合成 | 2D跟踪 | 3D跟踪（世界坐标系） |
|---------|-----------|--------|---------------------|
| 动态NeRF/3D-GS（HyperNeRF, Deformable-3D-GS等） | ✓ | ✗ | ✗ |
| 2D/3D跟踪方法（TAPIR+DA, CoTracker+DA等） | ✗ | ✓ | 部分（仅提升2D结果） |
| **Shape of Motion** | ✓ | ✓ | ✓（全视频长程轨迹） |

这种统一输出能力源于其表示设计的本质差异：动态NeRF使用变形场映射到规范空间，不显式建模世界坐标系下的运动；而Shape of Motion的持久3D高斯直接在SE(3)空间中运动，使得3D轨迹可以通过光栅化自然地生成：

$$^{\mathrm{w}}\hat{\mathbf{X}}_{tt'}(\mathbf{p}) = \sum_{i\in H(\mathbf{p})} T_i \alpha_i \mu_{i,t'}$$

在iPhone数据集上，该方法在3D跟踪EPE上相比TAPIR+DA降低了28%（0.114→0.082），同时在新视角合成PSNR上以16.72超过最佳动态重建基线DynMF（16.54），验证了联合优化的协同效应。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/001_Figure_1.jpg]]
*Figure 1: Shape of Motion. Our method enables joint long-range 3D tracking and novel view synthesis from a monocular video of a complex dynamic scene. We render moving elements at a fixed viewpoint across time and visualize estimated 3D motion as colorful trajectories. These trajectories reveal distinct geometric patterns, which leads to the term “Shape of Motion”*

**Shape of Motion** 的整体 pipeline 如图 Figure 2 所示，其核心思路是将单目视频的动态场景表示为一组持久存在的 3D 高斯，并通过全局共享的 SE(3) 运动基来建模这些高斯在时间轴上的运动轨迹。整个系统由五个紧密耦合的模块构成，形成从数据预处理到联合优化的完整闭环。

### 输入与数据预处理

系统接收一段单目 RGB 视频序列 $\{ I _ { t } \in \mathbb { R } ^ { H \times W \times 3 } \}$、已知的相机内参 $\mathbf K _ { t } \in \mathbb R ^ { 3 \times 3 }$ 和外参 $\mathbf { E } _ { t } \in \mathbb { S E } ( 3 )$ 作为输入。预处理阶段利用两个现成的数据驱动模型提取互补的噪声监督信号：**Depth Anything** 提供逐帧的单目深度估计，**TAPIR** 提供跨帧的长距离 2D 跟踪轨迹。此外，通过 Track-Anything 获取动态对象的掩码，用于区分场景中的静态与动态区域。

### 运动基初始化

这是连接 2D 观测与 3D 运动表示的关键桥梁。系统首先将 2D 跟踪轨迹通过深度图提升为带噪声的初始 3D 轨迹，然后对这些轨迹的速度向量进行 k-means 聚类，再通过加权 Procrustes 对齐从每个簇中求解出一个 SE(3) 变换，从而初始化 $B$ 个全局共享的运动基 $\{\mathbf{T}_{0t}^{(b)}\}_{b=1}^B$（所有实验中 $B=10$）。这一步为后续优化提供了结构化的运动先验。

### 高斯初始化

动态高斯：从初始 3D 轨迹的规范帧位置中随机采样 $N$ 个点，作为动态高斯的初始均值 $\mu_0$（实验中约 40k 个）。静态高斯：将对齐后的深度图反投影到 3D 空间，初始化约 100k 个静态高斯。这种分离建模使得动态区域的运动表示更加聚焦。

### 动态与静态高斯联合优化

这是系统的核心优化模块。场景运动被参数化为：每个动态高斯在时间 $t$ 的姿态通过其规范帧姿态经 SE(3) 变换得到：

$$\mu_t = \mathbf{R}_{0t}\mu_0 + \mathbf{t}_{0t}, \quad \mathbf{R}_t = \mathbf{R}_{0t}\mathbf{R}_0$$

而每个点的 SE(3) 变换 $\mathbf{T}_{0t}$ 又表示为 $B$ 个全局运动基的线性组合：

$$\mathbf{T}_{0t} = \sum_{b=0}^B \mathbf{w}^{(b)} \mathbf{T}_{0t}^{(b)}$$

其中 $\mathbf{w}^{(b)}$ 是每个高斯独有的运动系数。优化目标是最小化以下多任务损失：

- **重建损失** $\mathcal{L}_{\mathrm{recon}}$：像素级颜色、深度和掩码的 L1 损失（Eq. 7）
- **2D 跟踪损失** $L_{\mathrm{track-2d}}$：预测 2D 轨迹与观测轨迹的 L1 损失（Eq. 8）
- **跟踪深度损失** $L_{\mathrm{track-depth}}$：渲染深度与观测轨迹处深度的 L1 损失（Eq. 9）
- **刚体损失** $L_{\mathrm{rigidity}}$：保持相邻动态高斯点间距离随时间不变（Eq. 10）

### 可微分渲染

基于 3D Gaussian Splatting 框架，系统将动态高斯投影到图像平面（Eq. 1），通过 alpha 混合光栅化生成 RGB 图像 $\hat{\mathbf{I}}$、深度图 $\hat{\mathbf{D}}$（Eq. 2），以及 2D 轨迹 $\hat{\mathbf{U}}_{tt'}$ 和 3D 轨迹 $^{\mathrm{w}}\hat{\mathbf{X}}_{tt'}(\mathbf{p})$（Eq. 5）。渲染速度约 140 fps，但逐场景优化需约 2 小时（A100 GPU）。

### 输出能力

该框架的独特之处在于同时输出三种互补的 4D 表示：任意像素的长程 3D 运动轨迹、新视角合成图像，以及通过运动系数 PCA 揭示的场景刚体运动分解（Figure 5, 6）。这种统一的显式运动表示使得 Shape of Motion 在 3D 跟踪、2D 跟踪和新视角合成三个任务上均达到 SOTA 水平（Table 1）。

Shape of Motion 的核心是一个可微分的动态场景表示，它将单目视频的4D重建问题分解为三个紧密耦合的模块：**持久3D高斯的参数化**、**低维运动基的建模**、以及**多信号联合优化**。

### 3D高斯投影与渲染

静态3D高斯溅射（3DGS）是本方法的渲染基础。每个3D高斯由均值 $\mu_0 \in \mathbb{R}^3$、协方差 $\Sigma_0 \in \mathbb{R}^{3\times 3}$、颜色 $\mathbf{c}$ 和不透明度 $\alpha$ 定义。给定相机内参 $\mathbf{K}$ 和外参 $\mathbf{E}$，3D高斯通过透视投影和仿射近似的雅可比 $\mathbf{J}$ 投影到2D图像平面：

$$
\mu_0'(\mathbf{K},\mathbf{E}) = \Pi(\mathbf{K}\mathbf{E}\mu_0), \quad \Sigma_0'(\mathbf{K},\mathbf{E}) = \mathbf{J}_{\mathbf{K}\mathbf{E}}\Sigma_0\mathbf{J}_{\mathbf{K}\mathbf{E}}^\top \tag{1}
$$

像素 $\mathbf{p}$ 的RGB颜色和深度通过按深度排序的alpha混合得到：

$$
\hat{\mathbf{I}}(\mathbf{p}) = \sum_{i\in H(\mathbf{p})} T_i \alpha_i \mathbf{c}_i, \quad \hat{\mathbf{D}}(\mathbf{p}) = \sum_{i\in H(\mathbf{p})} T_i \alpha_i \mathbf{d}_i \tag{2}
$$

其中 $T_i = \prod_{j=1}^{i-1}(1-\alpha_j)$ 是累积透射率，$H(\mathbf{p})$ 是投影到该像素的高斯集合，$\mathbf{d}_i$ 是高斯 $i$ 在相机坐标系下的深度。

### 动态场景的运动基表示

这是本方法的核心创新。不同于逐点建模运动或使用变形场，Shape of Motion 将每个动态高斯的运动表示为**全局共享的SE(3)运动基的线性组合**。

对于规范帧 $t_0$ 处的高斯，其在时间 $t$ 的位姿通过刚体变换 $\mathbf{T}_{0t} = [\mathbf{R}_{0t}\; \mathbf{t}_{0t}] \in \text{SE}(3)$ 更新：

$$
\mu_t = \mathbf{R}_{0t}\mu_0 + \mathbf{t}_{0t}, \quad \mathbf{R}_t = \mathbf{R}_{0t}\mathbf{R}_0 \tag{3}
$$

关键假设是场景运动具有低维结构——所有点的运动可由 $B \ll N$ 个全局基轨迹 $\{\mathbf{T}_{0t}^{(b)}\}_{b=1}^B$ 的加权组合描述。每个高斯 $i$ 拥有一组运动系数 $\mathbf{w}_i \in \mathbb{R}^B$（通过softmax归一化），其变换为：

$$
\mathbf{T}_{0t} = \sum_{b=0}^B \mathbf{w}^{(b)} \mathbf{T}_{0t}^{(b)} \tag{4}
$$

这种设计的因果机制在于：运动基充当了强大的归纳偏置，将高维逐点运动压缩到低维流形上，使得被遮挡区域的运动可以从可见区域的共享基中推断出来。

### 3D轨迹的光栅化

为了生成可监督的3D运动轨迹，方法将动态高斯在目标时间 $t'$ 的世界坐标进行光栅化。对于源帧 $t$ 的像素 $\mathbf{p}$，其在目标时间 $t'$ 的3D位置为：

$$
^{\mathrm{w}}\hat{\mathbf{X}}_{tt'}(\mathbf{p}) = \sum_{i\in H(\mathbf{p})} T_i \alpha_i \mu_{i,t'} \tag{5}
$$

其中 $\mu_{i,t'}$ 是高斯 $i$ 在时间 $t'$ 的世界坐标位置。2D轨迹 $\hat{\mathbf{U}}_{tt'}(\mathbf{p})$ 则通过将 $^{\mathrm{w}}\hat{\mathbf{X}}_{tt'}(\mathbf{p})$ 投影到目标帧的图像平面得到。这一光栅化操作使得整个运动表示端到端可微。

### 多信号联合优化

优化目标融合了三个互补的监督信号，形成相互纠正的闭环。

**重建损失** 在每帧施加像素级L1约束，覆盖颜色、深度和动态掩码：

$$
\mathcal{L}_{\mathrm{recon}} = \|\hat{\mathbf{I}}-\mathbf{I}\|_1 + \lambda_{\mathrm{depth}}\|\hat{\mathbf{D}}-\mathbf{D}\|_1 + \lambda_{\mathrm{mask}}\|\hat{\mathbf{M}}-\mathbf{M}\|_1 \tag{7}
$$

**2D跟踪损失** 将渲染的2D轨迹与现成的跟踪器（TAPIR）输出对齐：

$$
L_{\mathrm{track-2d}} = \|\mathbf{U}_{tt'} - \hat{\mathbf{U}}_{tt'}\|_1 \tag{8}
$$

**跟踪深度损失** 在观测到的2D轨迹位置，约束渲染深度与单目深度估计的一致性：

$$
L_{\mathrm{track-depth}} = \|\hat{\mathbf{d}}_{tt'} - \hat{\mathbf{D}}(\mathbf{U}_{tt'})\|_1 \tag{9}
$$

**刚体正则化** 鼓励同一运动基主导的相邻高斯点之间保持距离不变，强化局部刚体假设：

$$
L_{\mathrm{rigidity}} = \big\|\mathrm{dist}(\mathbf{\hat{X}}_t, \mathcal{C}_k(\mathbf{\hat{X}}_t)) - \mathrm{dist}(\mathbf{\hat{X}}_{t'}, \mathcal{C}_k(\mathbf{\hat{X}}_{t'}))\big\|_2^2 \tag{10}
$$

其中 $\mathcal{C}_k(\mathbf{\hat{X}}_t)$ 表示点 $\mathbf{\hat{X}}_t$ 的 $k$ 近邻。

### 初始化策略

优化的成功高度依赖合理的初始化。预处理阶段利用Depth Anything获取单目深度，TAPIR获取2D跟踪，通过深度提升得到含噪的初始3D轨迹。动态高斯的规范帧位置从这些初始3D轨迹中随机采样。运动基的初始化则通过对3D轨迹速度向量进行k-means聚类，并对每个簇求解加权Procrustes对齐问题，得到 $B$ 个初始SE(3)基（所有实验中 $B=10$）。静态场景部分通过反投影对齐后的深度图初始化约100k个静态高斯。消融实验证实，跳过SE(3)拟合初始化步骤会导致性能显著下降（Table 4）。

## 实验与关键发现

### 实验设置

方法在三个数据集上进行评估：**iPhone dataset**（14个真实场景，包含多物体刚体/近刚体运动）、**Kubric dataset**（合成数据，提供真值3D轨迹）和 **NVIDIA dataset**（多视角动态场景）。所有实验统一使用 **TAPIR** 进行2D跟踪估计、**Depth Anything** 进行单目深度估计，相机位姿通过 COLMAP 或数据集提供并对齐到度量尺度。运动基数量 $B=10$，动态高斯点40k，静态高斯点100k，优化器为 Adam，在单张 A100 GPU 上约需2小时，渲染速度约140 fps。

### 主实验结果

**iPhone dataset 综合性能**（Table 1）。Shape of Motion 在三个任务上均达到最优：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/005_Table_1.jpg]]
*Table 1: Evaluation on iPhone dataset. Our method achieves SOTA performance all tasks of 3D point tracking, 2D point tracking, and novel view synthesis. The baselines that perform best on 2D and 3D tracking (TAPIR [16]+DA [121], CoTracker [45]+DA [121], DELTA [74], SpatialTracker [113]) are unable to synthesize novel views of the scene, while the methods that perform best in novel view synthesis struggle with or fail to produce 2D and 3D tracks. Our method achieves a significant boost in all three tasks above baselines. We include training details about “Ours + 2DGS [34]” in the supplement. Figure 4. Qualitative comparison of novel view synthesis on iPhone dataset. The leftmost image in each row sho...*

- **3D跟踪**：3D EPE 为 **0.082**，相比最强基线 TAPIR+DA（0.114）降低 **28%**；$\delta_{\text{3D}}^{0.05}$（5cm阈值内）达到43.0，$\delta_{\text{3D}}^{0.10}$（10cm阈值内）达到73.3。
- **2D跟踪**：AJ 为 **34.4**，相比 TAPIR（27.8）提升 **23.7%**；OA 达到86.6。
- **新视角合成**：PSNR 为 **16.72**，略优于 DynMF（16.54）；LPIPS 为 0.560，与 Deformable-3D-GS（0.553）相当。

值得注意的是，2D/3D跟踪最强基线（TAPIR+DA、CoTracker+DA、DELTA、SpatialTracker）**无法进行新视角合成**，而新视角合成最强基线（DynMF、Deformable-3D-GS）**无法产生有意义的3D轨迹**。Shape of Motion 是唯一同时在这三个任务上达到领先水平的方法。Figure 3 的定性对比显示，基线方法在物体边界处轨迹发散或错误附着到背景，而本文方法产生平滑、准确的3D轨迹。

**Kubric dataset 3D跟踪**（Table 2）。3D EPE 为 **0.16**，相比 TAPIR+DA（0.22）降低 **27%**，验证了方法在合成场景上的泛化能力。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/007_Table_2.jpg]]
*Table 2: 3D Tracking evaluation on Kubric dataset*

**NVIDIA dataset 新视角合成**（Table 3）。PSNR 均值 **23.37**，与 **Dynamic Gaussian Marbles (DGM)**（23.30）相当，说明方法在标准多视角动态场景上不牺牲新视角合成质量。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/009_Table_3.jpg]]
*Table 3: Evaluation on NVIDIA dataset. Our method is comparable with Dynamic Gaussian Marbles (DGM) [94]*

### 消融实验

Table 4 报告了 iPhone 数据集上的消融结果，揭示了三个关键设计的作用：

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/008_Table_4.jpg]]
*Table 4: Ablation Studies on iPhone dataset*

1. **运动基表示**：将 SE(3) 运动基替换为平移运动基（“Transl. Bases”），3D EPE 从 0.082 退化到 **0.206**；替换为逐点平移运动（“Per-Gaussian Transl.”），性能进一步恶化。这表明**低维刚体运动先验**对约束病态问题至关重要。

2. **SE(3) 初始化**：省略基于 k-means 和 Procrustes 的初始 SE(3) 拟合步骤（“No SE(3) Init.”），3D EPE 显著增加，验证了结构化初始化的必要性。

3. **2D跟踪监督**：完全移除2D跟踪损失（“No 2D Tracks”），3D EPE 大幅上升，性能显著下降。这表明长距离2D跟踪信号是融合深度和运动信息、纠正单目深度误差的关键约束。

4. **2DGS 变体**：将 3DGS 替换为 2DGS（“Ours+2DGS”），在2D跟踪和 NVS 上进一步提升（Table 1），说明更精确的几何表示有助于改善渲染和跟踪质量。

### 失败模式与局限性

- **外部依赖的噪声传播**：深度估计和2D跟踪的预测噪声会直接影响重建质量。在纹理稀少、重复纹理或运动幅度极大的场景中，TAPIR 跟踪和 Depth Anything 深度可能失效，导致重建退化。
- **非刚体变形**：方法假设场景运动近似刚体，对复杂非刚体变形（如衣服褶皱、流体）的泛化有限。
- **手动交互**：动态对象掩码需要手动通过 Track-Anything 指定，尚未实现全自动分割。
- **计算开销**：测试时优化约需2小时（A100 GPU），不适合实时或流式应用。

### 关键图表结论

- **Figure 3**：定性展示3D轨迹对比，本文方法在物体边界处保持轨迹一致性，而基线方法出现漂移和错误附着。
- **Figure 5**：运动系数 PCA 可视化显示，系数在刚体运动区域呈现恒定颜色，验证了运动基成功捕捉场景的刚体运动分组。
- **Figure 6**：优化后运动系数的前三个 PCA 分量进一步展示了场景运动的低维结构。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2407_13764/figures/010_Figure_6.jpg]]
*Figure 6: First three PCA components of the optimized motion coefficients*

- **Table 1**：综合定量结果，Shape of Motion 在3D跟踪、2D跟踪和新视角合成上均达到最优或接近最优。
- **Table 4**：消融实验确认 SE(3) 运动基、初始化和2D跟踪监督均为关键设计。

## 定位与知识库关联

### 1. 核心瓶颈与设计动机

单目视频的4D重建面临一个根本性的病态问题：从单一视角的2D像素观测中恢复全场景的3D几何和运动，缺少深度、多视角和运动信息的直接约束。现有方法在此问题上存在明显的功能割裂——动态新视角合成方法（如HyperNeRF、DynIBaR、Deformable-3D-GS）能够产生高质量的渲染结果，但无法提供显式的长程3D运动轨迹；而2D/3D跟踪方法（如TAPIR、CoTracker、SpatialTracker）虽然能追踪像素运动，却不具备新视角合成能力，且将2D跟踪直接提升到3D（TAPIR+DA）的方式缺乏全局一致性约束，导致3D轨迹噪声较大。

Shape of Motion的设计动机正是弥合这一鸿沟：通过构建一个统一的4D场景表示，同时支持高保真新视角合成和全视频长程3D跟踪。其核心假设是——真实场景中的运动具有低维结构，可以被分解为少量刚体运动基的线性组合。

### 2. 关键设计决策与因果机制

该方法在三个层面做出了区别于现有工作的关键选择：

**运动表示：从变形场到显式SE(3)基。** 主流动态NeRF和动态3D-GS方法通常采用基于变形场的规范空间映射（如HyperNeRF的切片面潜在编码、Deformable-3D-GS的逐帧偏移预测），这类表示隐式且缺乏对运动结构的显式约束。Shape of Motion转而将每个3D高斯的运动显式建模为$B$个全局共享SE(3)运动基的线性组合：

$$\mathbf{T}_{0t} = \sum_{b=0}^B \mathbf{w}^{(b)} \mathbf{T}_{0t}^{(b)}$$

其中$B \ll N$（实际设置$B=10$）。这种低维分解带来了两个因果效应：第一，运动基的全局共享使得可见区域的运动信息可以传播到被遮挡区域，解决了遮挡下的运动推理问题；第二，每个高斯的运动系数$\mathbf{w}$隐式编码了其所属的刚性运动分组，PCA可视化显示这些系数自然地按运动部件聚类（Figure 5, Figure 6），无需显式的语义分割。

**监督信号：多源噪声信号的互补融合。** 不同于仅依赖RGB重建损失的方法，Shape of Motion同时吸收三种互补的监督信号：单目深度估计（Depth Anything）提供几何先验，长距离2D跟踪（TAPIR）提供跨帧对应关系，RGB提供光度约束。这三种信号各自有噪声，但在统一的4D优化框架中相互纠正——深度约束规范了3D位置，2D跟踪约束规范了运动轨迹，RGB约束提供了精细的外观拟合。消融实验证实，移除2D跟踪监督会导致3D跟踪性能大幅下降（Table 4），验证了跨帧对应关系对运动学习的关键作用。

**初始化策略：从噪声观测到结构化先验。** 该方法并非随机初始化运动基，而是通过k-means聚类初始3D轨迹的速度向量，再对每个聚类求解加权Procrustes对齐问题来初始化SE(3)基。这一结构化初始化将优化引导至合理的局部极小值附近，跳过该步骤会明显损害性能（Table 4）。

### 3. 与基线方法的关系定位

**动态新视角合成基线。** 在iPhone数据集上，Shape of Motion以PSNR 16.72 dB优于DynMF（16.54 dB）、HyperNeRF（15.97 dB）、DynIBaR（15.56 dB）和Deformable-3D-GS（15.83 dB），验证了显式运动建模对渲染质量的增益（Table 1）。在NVIDIA数据集上，该方法与Dynamic Gaussian Marbles（DGM）性能相当（PSNR 23.37 vs. 23.30，Table 3），表明其在多视角准静态场景上也具有竞争力。但需注意，这些基线方法无法输出3D运动轨迹，因此功能覆盖范围存在本质差异。

**2D/3D跟踪基线。** 与直接将2D跟踪提升到3D的方法相比，Shape of Motion的3D EPE在iPhone数据集上比TAPIR+DA降低28%（0.082 vs. 0.114），比CoTracker+DA降低幅度更大（Table 1）。这一提升源于SE(3)运动基提供的全局运动一致性约束——单纯的深度提升缺乏对运动结构的建模，容易在遮挡边界和深度噪声区域产生不连贯的3D轨迹。在Kubric合成数据集上，该方法同样以3D EPE 0.16优于TAPIR+DA的0.22（Table 2），验证了运动基表示在不同场景类型下的泛化性。

**2DGS变体。** 将3D高斯替换为2D高斯（Ours+2DGS）在2D跟踪和NVS指标上进一步提升（Table 1），表明更精确的表面建模有利于跟踪精度，但3D跟踪性能略有下降，提示需要在表面紧致性和3D运动表达之间权衡。

### 4. 适用边界与失效模式

该方法存在以下明确的适用边界：

- **运动类型假设**：运动基的SE(3)线性组合本质上假设场景运动可分解为刚体或近似刚体运动。对于显著的非刚体变形（如衣服褶皱、流体运动、面部表情），该表示的表达能力有限。论文未在非刚体主导的场景上进行系统评估。
- **纹理依赖**：方法依赖TAPIR的2D跟踪和Depth Anything的深度估计，在纹理稀少、重复纹理或运动幅度极大的场景中，这些预训练模型的预测质量可能严重退化，误差会传播至最终重建。
- **手动交互**：动态对象的初始化需要手动指定掩码（通过Track-Anything），尚未实现端到端的自动分割。这限制了在大规模视频数据上的应用。
- **计算开销**：测试时优化约需2小时（A100 GPU），不适合实时或流式处理场景。渲染速度约140 fps，表明推理阶段效率较高，但优化阶段是主要瓶颈。

### 5. 开放问题

1. **全自动分割**：能否将移动对象分割步骤完全自动化，消除对人工交互的依赖？可能的路径包括将运动分割与运动基学习联合优化，或利用视频分割基础模型。
2. **优化加速**：如何将逐场景优化时间从小时级压缩到分钟级，使其适用于流媒体或交互式应用？可能的思路包括引入前馈运动基预测网络、多分辨率优化策略或更高效的初始化方法。
3. **非刚体扩展**：如何处理包含显著非刚体变形的动态场景？可能需要在SE(3)基的基础上引入局部变形场或混合表示。
4. **先验内化**：能否减少对离线预训练模型的依赖，将这些几何和运动先验内化到一个统一的、可端到端训练的学习框架中？
5. **长视频扩展**：当前实验主要在300帧左右的视频上进行，如何扩展到更长序列并保持计算效率？运动基数量的自适应调整和分层运动表示可能是可行方向。
6. **多模态融合**：能否利用音频、文本等多模态信息辅助运动分解和场景理解，提升在语义复杂场景中的鲁棒性？

## 原文 PDF

![[paperPDFs/CVPR_2024/Shape_of_Motion_4D_Reconstruction_from_a_Single_Video.pdf]]
