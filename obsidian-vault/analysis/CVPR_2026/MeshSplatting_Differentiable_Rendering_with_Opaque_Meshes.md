---
title: "MeshSplatting: Differentiable Rendering with Opaque Meshes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MeshSplatting_Differentiable_Rendering_with_Opaque_Meshes.pdf
project_link: "https://meshsplatting.github.io/"
code_link: null
aliases:
- MeshSplatting
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过两阶段训练（先优化非连通三角片，再利用受限Delaunay三角剖分建立连通性并微调），配合不透明度重参数化和窗口参数线性衰减调度，使三角形逐渐变为不透明且尖锐，同时保证梯度流动。
primary_logic: 在训练早期保持半透明和平滑窗口以允许梯度传播，随着训练进展通过强制连通性和逐步增加不透明度，实现端到端优化的不透明连通网格，且一次性三角剖分避免每步重建的高开销。
claims:
- 在Mip-NeRF360上，PSNR较MiLo提高0.69 dB，同时训练快2倍，内存使用少2倍。
- 最终网格仅由不透明三角形组成，可直接在游戏引擎中渲染，无需自定义着色器。
- 消融实验显示，移除第二阶段连接性优化导致PSNR下降8.56 dB，证明两阶段策略至关重要。
- Mip-NeRF360 上 PSNR / LPIPS / SSIM = 24.78 / 0.310 / 0.728
---

# MeshSplatting: Differentiable Rendering with Opaque Meshes

> [!tip] 核心洞察
> 在训练早期保持半透明和平滑窗口以允许梯度传播，随着训练进展通过强制连通性和逐步增加不透明度，实现端到端优化的不透明连通网格，且一次性三角剖分避免每步重建的高开销。

| 字段 | 内容 |
|------|------|
| 中文题名 | MeshSplatting：不透明网格的可微渲染 |
| 英文题名 | MeshSplatting: Differentiable Rendering with Opaque Meshes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.06818) · [Project](https://meshsplatting.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MeshSplatting |
| Dataset | Mip-NeRF360, Tanks & Temples, DTU |

> [!tip] 效果简介
> - Mip-NeRF360 上，PSNR / LPIPS / SSIM 24.78 / 0.310 / 0.728 vs MiLo 24.09 / 0.323 / 0.688 (PSNR +0.69 dB; LPIPS -0.013; SSIM +0.040)；训练时间 / 内存 / FPS (HD) 48 min / 100 MB / 220 FPS vs MiLo 106 min / 253 MB / 170 FPS (训练快2倍，内存少2.5倍)。
> - Tanks & Temples 上，PSNR / LPIPS / SSIM 20.52 / 0.287 / 0.745 vs MiLo 21.46 / 0.348 / 0.706 (PSNR -0.94 dB but LPIPS -0.061 and SSIM +0.039 (更少噪声))。
> - DTU (Chamfer Distance) 上，Chamfer Distance Mean 0.79 vs 2DGS 0.80 / GOF 0.74 / MiLo 0.68 (性能相当，与定制网格提取方法同水平)。

## 概述

### 核心问题

基于高斯溅射（如 **3DGS**）或三角基元（如 **Triangle Splatting**）的神经渲染方法，虽然在新视角合成质量上取得突破，但其输出本质上是不连通的“三角形汤”或半透明高斯体，无法直接导入标准游戏引擎、物理模拟或光线追踪管线。现有方法（如 **2DGS**、**GOF**、**RaDe-GS**、**MiLo**）虽然可以通过后处理提取网格，但这一转换过程会损失视觉质量，且最终网格往往需要额外的着色步骤，无法实现端到端的优化。

### 核心方法

**MeshSplatting** 提出了一种基于不透明连通网格的可微渲染方法，核心思路是通过两阶段训练实现从“三角形汤”到连通网格的端到端优化：

1. **第一阶段**：从 SfM 稀疏点云初始化非连通三角形汤，在半透明状态下快速优化场景覆盖和几何结构。
2. **网格构建**：通过受限 Delaunay 三角剖分一次性建立顶点间的连通性，将三角形汤转换为共享顶点的连通网格。
3. **第二阶段**：在连通网格上微调顶点位置和颜色，配合不透明度重参数化和窗口参数 σ 的线性衰减调度，使三角形从半透明平滑过渡到完全不透明且边界尖锐。

这一设计的关键因果机制在于：训练早期保持半透明和平滑窗口以允许梯度传播，随着训练进展通过强制连通性和逐步增加不透明度，实现不透明连通网格的端到端优化，且一次性三角剖分避免了每步重建的高开销。

### 方法谱系与知识库定位

MeshSplatting 处于神经渲染与显式几何表示的交汇点。与 **3DGS** 的体积渲染范式相比，它直接输出可被标准图形管线消费的网格表示；与 **Triangle Splatting** 等三角基元方法相比，它通过共享顶点和连通性约束解决了三角形汤的碎片化问题；与 **MiLo** 等联合网格-高斯优化方法相比，它无需后处理着色步骤，输出即为带颜色的不透明网格，可直接用于游戏引擎、物理模拟和光线追踪。

### 核心结果

在 Mip-NeRF360 数据集上，MeshSplatting 的 PSNR 达到 24.78 dB，较当前最优方法 **MiLo** 提升 0.69 dB，同时训练速度快 2 倍，内存占用减少 2.5 倍。在 Tanks & Temples 数据集上，虽然 PSNR 略低于 MiLo（-0.94 dB），但 LPIPS 显著降低 0.061，SSIM 提升 0.039，表明渲染结果噪声更少、结构更清晰。消融实验表明，移除第二阶段连接性优化会导致 PSNR 骤降 8.56 dB，移除窗口参数 σ 衰减会导致 PSNR 下降 7.96 dB，充分验证了两阶段策略和不透明度/窗口调度机制的关键作用。

## 背景与动机

### 从新视角合成到可部署的3D资产

新视角合成（Novel View Synthesis, NVS）的目标是从一组稀疏的2D图像中重建出可从任意视角渲染的3D场景表示。近年来，以**3D Gaussian Splatting (3DGS)** 为代表的可微渲染方法在该领域取得了突破性进展，实现了实时、高质量的视角合成。然而，3DGS的输出是一组离散的、半透明的3D高斯椭球体，这种表示与标准图形管线存在根本性不兼容：它无法直接导入游戏引擎、不支持物理模拟、不能进行光线追踪，且需要自定义着色器来处理透明度混合。

为解决这一问题，研究者们开始探索将3D高斯转换为网格（mesh）的后处理方案。**2DGS**、**GOF**、**RaDe-GS** 等方法尝试从高斯场中提取网格表面，而**MiLo** 则进一步联合优化网格几何与高斯外观，再通过额外的着色步骤为网格赋予颜色。这些方法虽然在一定程度上弥合了可微渲染与标准图形管线之间的鸿沟，但它们共享一个根本性缺陷：**最终输出的网格并非端到端优化的直接产物，而是需要经过提取、转换、后着色等多阶段后处理**。这不仅增加了流程复杂度，还不可避免地引入视觉质量损失。

### 核心瓶颈：不连通、半透明、无颜色的三角片

从更基础的层面审视，当前基于三角基元的可微渲染方法（如**Triangle Splatting**）面临三个相互纠缠的瓶颈：

1. **非连通性**：三角形以"三角形汤"（triangle soup）的形式存在，每个三角形独立定义其三个顶点，相邻三角形之间不共享顶点。这意味着输出不是一个连通的网格，无法用于物理模拟、碰撞检测等需要拓扑一致性的下游任务。

2. **半透明性**：为保证梯度能够从渲染损失反向传播到几何参数，三角形必须保持一定程度的半透明性，使得光线可以穿过多个三角形进行体积渲染。这使得最终输出无法直接在标准光栅化管线中使用，需要自定义的透明度混合着色器。

3. **颜色缺失或分离**：三角形要么不携带颜色信息（需要后处理着色），要么颜色与几何分离优化，导致几何与外观之间缺乏一致性约束。

这三个瓶颈的根源在于一个深层矛盾：**可微渲染需要半透明性和独立基元来保证梯度流动，而实际应用需要不透明、连通的网格**。现有方法要么牺牲连通性和不透明性以维持可微性，要么在可微优化之后进行破坏性的后处理转换，始终无法在一个统一的端到端框架中同时满足这两个需求。

### MeshSplatting的动机与核心洞察

MeshSplatting 的提出正是为了打破这一僵局。其核心动机是：**能否直接通过可微渲染优化出一个连通、不透明、自带颜色的网格，使其在训练完成后无需任何后处理即可直接部署到标准图形引擎中？**

实现这一目标的核心洞察在于**训练过程的阶段性设计**：

- **早期阶段**，允许三角形保持半透明和较大的平滑窗口参数，确保梯度能够从像素空间顺畅地流向顶点位置和颜色参数。
- **随着训练进展**，通过调度机制逐步将三角形推向不透明、边界锐利的状态，同时引入连通性约束将三角形汤转化为共享顶点的网格。
- **关键突破**在于：连通性建立（受限Delaunay三角剖分）是一次性操作而非每步迭代执行，避免了高昂的计算开销；不透明度和窗口参数的线性衰减调度保证了从半透明到不透明的平滑过渡，使得梯度流在训练全程得以维持。

这一设计使得 MeshSplatting 成为首个在统一端到端框架中直接输出**即用型不透明连通网格**的方法，在 Mip-NeRF360 上以比 MiLo 快2倍的训练速度和少2倍的内存占用，实现了 PSNR +0.69 dB 的质量提升（Table 1），且最终网格可直接在标准游戏引擎中渲染，无需自定义着色器（Figure 1）。

## 核心创新

MeshSplatting 的核心突破在于**首次实现了端到端优化的不透明连通网格**，使输出可直接在标准游戏引擎中渲染，无需任何后处理或自定义着色器。这一能力源于以下关键创新点的协同作用：

### 1. 两阶段优化：从三角形汤到连通网格

现有基于三角基元的方法（如 **Triangle Splatting**）仅产生无连通关系的“三角形汤”（triangle soup），每个三角形独立定义顶点，相邻三角形不共享顶点。MeshSplatting 通过两阶段策略解决了这一结构性缺陷：

- **第一阶段（三角形汤优化）**：从 SfM 稀疏点云初始化等边三角形，大小依据邻居距离自适应缩放。在此阶段，三角形之间无连通约束，以半透明状态自由优化，使场景覆盖和几何快速适应（Figure 3-1b）。
- **受限 Delaunay 三角剖分**：在优化中间阶段，对三角形汤执行一次性受限 Delaunay 三角剖分，创建共享顶点的连通网格（Figure 3-2a）。此步骤保持顶点位置不变，避免了每步重建的高开销。
- **第二阶段（网格微调）**：在连通网格上继续优化，共享顶点的梯度从所有相邻三角形累积，使顶点位置和外观得到精细调整（Figure 3-2b）。

消融实验直接验证了这一策略的关键性：**移除第二阶段连接性优化导致 PSNR 骤降 8.56 dB**（Table 11），证明两阶段设计并非可有可无的工程选择，而是方法有效性的核心支柱。

### 2. 顶点共享的参数化表示

与三角形汤中每个三角形独立存储三个顶点、颜色和不透明度的方式不同，MeshSplatting 采用**共享顶点集**的参数化方案（Figure 2）：

- 每个顶点存储位置 $(x_i, y_i, z_i)$、球谐颜色系数 $\mathbf{c}_i$ 和不透明度 $o_i$。
- 三角形由顶点集中的三个索引定义，相邻三角形自然共享边界顶点。
- 反向传播时，来自所有相邻三角形的梯度在共享顶点处累积，隐式地施加了表面一致性约束。

这一设计使得最终输出是一个**真正的网格**——具有显式拓扑连接关系，而非孤立的三角片集合。

### 3. 不透明度与窗口参数的双重调度

为实现从半透明到不透明的平滑过渡，同时保证训练全程梯度流动，MeshSplatting 引入了两个关键调度机制：

**不透明度重参数化**：
$$o'(o) = O_t + (1 - O_t) \cdot \operatorname{sigm}(o)$$
其中 $O_t$ 在训练中从 0 线性增加到 1。训练早期 $O_t \approx 0$ 时，三角形保持半透明，允许梯度通过重叠区域传播；随着 $O_t \to 1$，三角形逐渐变为不透明。

**窗口参数 $\sigma$ 衰减**：
$$I(\mathbf{p}) = \left( \operatorname{ReLU}\left( \frac{\phi(\mathbf{p})}{\phi(\mathbf{s})} \right) \right)^{\sigma}$$
所有三角形共享 $\sigma$，从 1.0 线性退火至 0.0001（Figure 4）。$\sigma=1.0$ 时窗口函数平滑，三角形边界模糊，梯度可跨边界流动；$\sigma \to 0.0001$ 时窗口趋于尖锐，三角形变为硬边界。

消融实验表明这两个调度缺一不可：**移除 $\sigma$ 衰减导致 PSNR 骤降 7.96 dB，LPIPS 上升 0.27**（Table 11），其影响程度与移除整个第二阶段相当，说明平滑到尖锐的过渡是训练收敛的必要条件。

### 4. 渲染方程的自然简化

训练期间，像素颜色通过体积渲染方程累积深度排序后的重叠三角形贡献：
$$\mathcal{C}(\mathbf{p}) = \sum_{n=1}^{N} \mathbf{c}_{T_n} o_{T_n} I(\mathbf{p}) \left( \prod_{i=1}^{n-1} \left(1 - o_{T_i} I(\mathbf{p}) \right) \right)$$

随着 $O_t \to 1$ 和 $\sigma \to 0.0001$，所有三角形变为不透明且边界尖锐，渲染方程自然简化为单次像素评估：
$$C(\mathbf{p}) = \mathbf{c}_{T_n} I(\mathbf{p})$$
这意味着最终渲染**无需排序、无过度绘制、无需透明度混合**，与标准光栅化管线完全一致。这一特性是 MeshSplatting 输出能够直接导入游戏引擎的根本原因——它不需要任何自定义渲染例程来处理半透明。

### 5. 增密与剪枝策略的适配

为在网格约束下有效控制几何复杂度，MeshSplatting 设计了针对性的增密和剪枝策略：

- **增密**：基于不透明度的伯努利采样选择候选三角形，通过中点细分生成新三角形，确保新增几何集中在视觉重要区域。
- **硬剪枝**：移除不透明度 $o < 0.2$ 的三角形。
- **混合权重剪枝**：当三角形混合权重 $w < O_t$ 时剪枝，确保随着 $O_t$ 增加，仅保留实际参与渲染的不透明三角形。

消融显示，移除硬剪枝导致 PSNR 下降 0.67 dB，移除混合权重剪枝导致下降 0.62 dB（Table 11），表明这些策略对最终网格质量有实质性贡献。

### 创新总结

| 设计要素 | 传统方法（Triangle Splatting） | MeshSplatting | 创新意义 |
|---------|-------------------------------|---------------|---------|
| 顶点表示 | 独立三角形顶点 | 共享顶点网格 | 建立连通性，支持标准网格管线 |
| 不透明度 | 可学习，无调度 | 重参数化 + 线性调度 | 保证梯度流同时实现最终不透明 |
| 窗口参数 σ | 逐三角形独立 | 全局共享 + 线性衰减 | 从平滑到尖锐的稳定过渡 |
| 网格构建 | 无 | 一次性受限 Delaunay 三角剖分 | 避免每步重建开销 |
| 最终渲染 | 需排序和 alpha 混合 | 单次像素评估 | 兼容标准光栅化管线 |

这些创新并非孤立的技术点，而是围绕一个统一目标形成因果链条：**通过调度机制保证训练期间梯度流动，通过两阶段优化建立连通性，最终收敛到可直接使用的不透明连通网格**。

## 整体框架

MeshSplatting 采用**两阶段优化流水线**，将非结构化的半透明三角形汤逐步转化为连通、不透明、带顶点颜色的网格。其核心设计遵循一条清晰的因果链：早期保持几何基元的平滑与半透明以保证梯度流动，中期通过一次性三角剖分建立连通性，后期通过调度机制使三角形硬化并微调外观，最终输出可直接在标准游戏引擎中渲染的网格。

### 流水线总览

1. **三角形汤初始化**：从 SfM 稀疏点云出发，在每个点处初始化一个等边三角形，其大小正比于该点到最近三个邻居的平均距离。此时所有三角形相互独立，无连通约束。

2. **第一阶段优化（三角形汤优化）**：在无连通性、无流形约束的条件下，优化这些半透明三角形的位置、顶点颜色和不透明度。此阶段的目标是让场景覆盖和几何结构快速适应多视图观测，为后续网格化提供良好的顶点分布基础。

3. **受限 Delaunay 三角剖分**：在优化进行到一定阶段后，对三角形汤执行一次性受限 Delaunay 三角剖分，将独立三角形转化为具有共享顶点的连通网格。此步骤保持顶点位置不变，但引入了连通性——同时也带来了几何伪影和视觉质量下降，因为顶点颜色不再精确对齐底层几何。

4. **第二阶段优化（网格微调）**：在连通网格上继续优化，微调顶点位置和外观。由于顶点被相邻三角形共享，反向传播时梯度在共享顶点处累积，促使表面趋于平滑一致。

5. **不透明度与窗口参数调度**：贯穿整个训练过程，不透明度通过重参数化 $o'(o) = O_t + (1 - O_t) \cdot \operatorname{sigm}(o)$ 配合线性调度 $O_t: 0 \to 1$，使三角形从半透明逐渐变为不透明；窗口参数 $\sigma$ 从 $1.0$ 线性退火至 $0.0001$，使三角形从平滑过渡到尖锐。这两项调度确保了训练早期的梯度稳定流动，同时最终输出仅由不透明三角形组成。

6. **增密与剪枝**：基于不透明度的伯努利采样选择候选三角形，通过中点细分生成新三角形；同时通过硬剪枝（不透明度 $o < 0.2$）和混合权重剪枝（$w < O_t$）移除冗余基元。

### 输入输出流

- **输入**：多视图图像及其对应的 SfM 稀疏点云（可选深度图作为正则化信号）。
- **中间表示**：第一阶段输出非连通的半透明三角形汤；三角剖分后得到连通网格（此时视觉质量暂时下降）。
- **最终输出**：仅由不透明三角形组成的连通网格，每个顶点携带位置 $(x_i, y_i, z_i)$、球谐颜色系数 $\mathbf{c}_i$ 和不透明度 $o_i$。训练结束时，渲染方程简化为单次像素评估 $C(\mathbf{p}) = \mathbf{c}_{T_n} I(\mathbf{p})$，无需排序或 alpha 混合。

### 模块关系与因果机制

流水线的关键因果机制在于**“先自由探索，后约束收敛”**。第一阶段放弃连通性约束，使三角形能够自由移动以覆盖场景；若跳过第二阶段直接输出三角形汤，PSNR 会骤降 **8.56 dB**（Table 11），证明连通性微调对视觉质量的决定性作用。同时，窗口参数 $\sigma$ 的衰减调度同样关键——移除该调度导致 PSNR 下降 **7.96 dB**、LPIPS 上升 0.27，说明平滑到尖锐的渐进过渡是维持梯度流和最终渲染精度的必要条件。

损失函数组合了五个项以协调几何与外观的联合优化：

$$\mathcal{L} = \mathcal{L}_{\mathrm{3DGS}} + \beta_o \mathcal{L}_o + \beta_z \mathcal{L}_z + \beta_n \mathcal{L}_n + \beta_d \mathcal{L}_d$$

其中 $\mathcal{L}_{\mathrm{3DGS}}$ 为光度损失（L1 + SSIM），$\mathcal{L}_o$ 鼓励三角形不透明度趋向二值化，$\mathcal{L}_z = \frac{1}{N} \sum_{i=1}^{N} |z_i - z_i^*|$ 使顶点深度与渲染深度图对齐，$\mathcal{L}_n$ 和 $\mathcal{L}_d$ 分别约束法线平滑度和深度一致性。消融实验表明，移除深度对齐或法线正则化虽对 PSNR 影响较小，但会显著降低网格几何质量（Figure 7），说明这些正则化项在“视觉质量-几何质量”权衡中扮演关键角色。

### 补充图表

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/001_Figure_1.jpg]]
*Figure 1: MeshSplatting produces a connected mesh composed only of opaque triangles, achieving high-quality novel view synthesis through end-to-end optimization, with a 2× training speed-up and 2× lower memory usage over current state-of-the-art methods. (a) Our representation is compatible with standard game engines, requiring no a-posteriori conversion and/or custom rendering routines for transparency, and natively supports (b) physical interactions, (c) interactive walkthroughs, and (d) ray tracing. (e) MeshSplatting enables straightforward object extraction, allowing scene elements to be directly exported and imported into game engines*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/003_Figure_3.jpg]]
*Figure 3: From triangle soups to meshes. (1a) We initialize semi-transparent triangles and scale them based on local density. (1b) We optimize a semi-transparent triangle soup without shared vertices, leading to disconnected triangles. (2a) Applying restricted Delaunay triangulation restores global connectivity but introduces geometric artifacts and a loss of visual quality, as vertex colors no longer accurately align with the underlying geometry. (2b) The final fine-tuning stage refines the connected mesh, producing smooth surfaces, accurate geometry, and restoring the visual fidelity lost during triangulation. Using only opaque triangles, our method achieves high visual quality compared to the semi...*

## 核心模块与公式推导

### 三角溅射的投影与窗口函数

MeshSplatting的渲染基元是三维三角形在图像平面的投影。每个三角形投影后，通过其三条边的有符号距离定义像素级覆盖。给定投影三角形的三条边法向量 $\mathbf{n}_i$ 和偏置 $d_i$，像素 $\mathbf{p}$ 到三角形内部的有符号距离场定义为：

$$\phi(\mathbf{p}) = \max_{i\in\{1,2,3\}} L_i(\mathbf{p}), \quad L_i(\mathbf{p}) = \mathbf{n}_i \cdot \mathbf{p} + d_i$$

其中 $L_i(\mathbf{p}) > 0$ 表示像素位于第 $i$ 条边的内侧，三条边约束的交集即为三角形内部区域。该距离场在三角形内心处取最大值 $\phi(\mathbf{s})$，在边界处为0，在外部为负。

为获得平滑可微的覆盖指示，引入窗口函数 $I(\mathbf{p})$：

$$I(\mathbf{p}) = \left( \operatorname{ReLU}\left( \frac{\phi(\mathbf{p})}{\phi(\mathbf{s})} \right) \right)^{\sigma}$$

该函数在三角形内心处取值为1，边界处平滑衰减至0，外部严格为0。窗口参数 $\sigma$ 控制衰减的锐度：$\sigma = 1$ 时覆盖函数呈线性衰减（平滑三角形），$\sigma \to 0$ 时趋近于硬边界（尖锐三角形）。这一设计是梯度传播的核心——训练早期使用平滑窗口保证梯度信号覆盖足够空间范围，训练后期通过收缩窗口使三角形逼近不透明硬边界。

### 顶点共享的参数化方案

与Triangle Splatting中每个三角形独立持有顶点、颜色、不透明度的"三角形汤"参数化不同，MeshSplatting采用共享顶点网格表示。每个顶点 $v_i$ 存储五维参数：

$$v_i = (x_i, y_i, z_i, c_i, o_i)$$

其中 $(x_i, y_i, z_i)$ 为三维位置，$c_i$ 为颜色（使用球谐函数系数编码视角相关外观），$o_i$ 为不透明度。每个三角形由顶点集中的三个索引定义。在反向传播中，来自相邻三角形的梯度在共享顶点处累积，这是第二阶段网格微调能够产生光滑几何的关键机制。窗口参数 $\sigma$ 则全局共享，不随三角形变化。

### 不透明度重参数化与调度

为实现从半透明到不透明的平滑过渡，MeshSplatting对不透明度进行重参数化：

$$o'(o) = O_t + (1 - O_t) \cdot \operatorname{sigm}(o)$$

其中 $O_t$ 是随训练步数 $t$ 线性增长的调度参数，从0递增至1。当 $O_t = 0$ 时，$o' = \operatorname{sigm}(o) \in (0, 1)$，三角形为半透明状态，梯度可自由流通；当 $O_t = 1$ 时，$o' = 1$，三角形变为完全透明（不透明度为1），梯度被阻断。这一设计使得训练早期三角形保持半透明以允许几何调整，训练后期强制不透明以满足游戏引擎兼容性。

窗口参数 $\sigma$ 采用线性退火调度，从1.0线性衰减至0.0001，贯穿整个训练过程。两个调度协同工作：半透明阶段（$O_t$ 低）配合平滑窗口（$\sigma$ 高）最大化梯度传播；不透明阶段（$O_t$ 高）配合尖锐窗口（$\sigma$ 低）精确确定三角形边界。

### 体积渲染方程与简化

渲染时，对每个像素按深度顺序累积所有重叠三角形的颜色贡献：

$$\mathcal{C}(\mathbf{p}) = \sum_{n=1}^{N} \mathbf{c}_{T_n} o_{T_n} I(\mathbf{p}) \left( \prod_{i=1}^{n-1} \left(1 - o_{T_i} I(\mathbf{p}) \right) \right)$$

其中 $T_n$ 为按深度排序的第 $n$ 个三角形，$\mathbf{c}_{T_n}$ 为其颜色，$o_{T_n}$ 为三角形不透明度（取三个顶点不透明度的最小值），$I(\mathbf{p})$ 为窗口函数值。该方程与3DGS的体积渲染公式结构一致，但用三角形窗口函数替代了高斯核。

在训练结束时，由于所有三角形变为不透明（$o_{T_n} = 1$），且窗口函数趋近于硬指示函数，渲染方程退化为单次像素评估：

$$C(\mathbf{p}) = \mathbf{c}_{T_n} I(\mathbf{p})$$

其中 $T_n$ 是覆盖该像素的最前景三角形。这等价于标准光栅化管线，无需透明度混合或自定义着色器，是最终网格可直接在游戏引擎中渲染的理论基础。

### 损失函数组合

总训练损失由五项组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{3DGS}} + \beta_o \mathcal{L}_o + \beta_z \mathcal{L}_z + \beta_n \mathcal{L}_n + \beta_d \mathcal{L}_d$$

- $\mathcal{L}_{\mathrm{3DGS}}$：光度损失，采用3DGS中的L1损失与SSIM损失的加权组合。
- $\mathcal{L}_o$：不透明度损失，形式为二值交叉熵，鼓励三角形不透明度趋近于0或1，避免半透明残留。
- $\mathcal{L}_z$：深度对齐损失，L1范数形式 $\mathcal{L}_z = \frac{1}{N} \sum_{i=1}^{N} |z_i - z_i^*|$，使每个顶点的渲染深度 $z_i$ 与从深度图采样的目标深度 $z_i^*$ 对齐，将顶点拉向真实表面。
- $\mathcal{L}_n$：法线损失，鼓励相邻三角形法向量一致，促进表面平滑。
- $\mathcal{L}_d$：深度正则化损失，约束顶点深度与渲染深度图的一致性，防止几何漂移。

各正则化项的权重 $\beta_o, \beta_z, \beta_n, \beta_d$ 在训练过程中保持固定。消融实验表明，法线损失和深度正则化的组合对获得几何准确的网格至关重要（Figure 7），但过强的正则化会损害视觉质量，因为球谐函数难以在过度平滑的表面上编码精细外观细节。

### 补充图表

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/002_Figure_2.jpg]]
*Figure 2: Mesh parametrization. (left) In a triangle soup, each triangle*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/004_Figure_4.jpg]]
*Figure 4: Window parameter scheduling. To ensure stable gradient flow during training, we begin with smooth triangles (σ=1.0, left) and linearly decrease σ throughout training, resulting in sharper triangles by the end. We visualize σ for a prototypical triangle at the beginning and end of each optimization stage*

## 实验与分析

### 主要结果与效率对比

MeshSplatting在Mip-NeRF360和Tanks & Temples两个标准基准上进行了定量评估。Table 1汇总了与当前最佳网格化方法（MiLo）及Triangle Splatting、2DGS、GOF、RaDe-GS等代表性工作的对比结果。

在Mip-NeRF360上，MeshSplatting以3M顶点达到**24.78 PSNR / 0.310 LPIPS / 0.728 SSIM**，较MiLo（24.09 PSNR / 0.323 LPIPS / 0.688 SSIM）PSNR提升**+0.69 dB**，LPIPS降低0.013，SSIM提升0.040。值得注意的是，这一质量优势是在顶点数仅为MiLo的约1/3（3M vs 约10M）的条件下实现的，表明共享顶点网格参数化在紧凑性上的显著收益。

在Tanks & Temples上，MeshSplatting以2M顶点达到**20.52 PSNR / 0.287 LPIPS / 0.745 SSIM**。尽管PSNR较MiLo（21.46）低0.94 dB，但LPIPS大幅降低0.061、SSIM提升0.039，说明MeshSplatting产生的渲染噪声更少、视觉质量更接近真值。Figure 5的定性对比（Bicycle场景辐条细节和Truck场景桌面区域）印证了这一趋势——MeshSplatting重建的细粒度结构更锐利，伪影更少。

效率方面（Table 2），在NVIDIA A100 40GB上，MeshSplatting的Mip-NeRF360训练仅需**48分钟**、内存占用**100 MB**，而MiLo需106分钟、253 MB，训练速度提升约2倍，内存节省约2.5倍。推理端，在消费级MacBook M4上MeshSplatting达到**220 FPS**（HD分辨率），高于MiLo的170 FPS，且最终渲染简化为单次像素评估（$C(\mathbf{p}) = \mathbf{c}_{T_n} I(\mathbf{p})$），无需体积排序或alpha混合。

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/007_Table_2.jpg]]
*Table 2: Speed & memory on MipNeRF-360. MeshSplatting achieves faster training and lower memory usage than concurrent methods. FPS were measured on a costumer MacBook M4*

### 网格连通性与几何质量

Table 3展示了Garden场景的三角形连通性分布：最终网格中绝大多数三角形与三个或更多相邻三角形相连，验证了受限Delaunay三角剖分有效建立了全局连通性。Figure 8（补充材料）进一步可视化了从三角形汤到连通网格的几何改进——第二阶段微调后，表面平滑度和几何一致性显著提升。

在DTU数据集上的Chamfer距离评估（Table 10）显示，MeshSplatting的均值Chamfer距离为**0.79**，与2DGS（0.80）、GOF（0.74）、MiLo（0.68）处于同一水平，证明该方法在几何精度上与专门设计的网格提取方法相当，同时无需后处理步骤。

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/019_Table_10.jpg]]
*Table 10: Chamfer distance on the DTU dataset [23]. MeshSplatting achieves performance comparable to concurrent methods*

### 消融实验

Table 11给出了系统性的消融结果，揭示了各设计选择对性能的因果贡献：

| 消融条件 | PSNR变化 | LPIPS变化 | 关键结论 |
|----------|----------|-----------|----------|
| w/o stage 2（移除第二阶段连通优化） | **-8.56 dB** | — | 两阶段策略是方法的核心支柱，直接使用三角形汤无法获得可用网格 |
| w/o sigma decay（移除σ衰减调度） | **-7.96 dB** | +0.27 | σ从1.0线性退火至0.0001对训练稳定性和最终质量至关重要 |
| w/o SH（用RGB替代球谐函数） | -2.07 dB | +0.06 | 球谐函数对捕捉视角相关外观变化有显著贡献 |
| w/o supersampling（移除超采样） | -0.80 dB | — | 超采样在抗锯齿和梯度质量上起重要作用 |
| w/o hard pruning（移除硬剪枝） | -0.67 dB | +0.02 | 基于不透明度的硬剪枝（o<0.2）有效剔除冗余三角形 |
| w/o w pruning（仅用不透明度剪枝） | -0.62 dB | — | 基于混合权重的额外剪枝（w < O_t）提供了增量收益 |

**关键因果链路**：消融结果清晰地揭示了MeshSplatting的性能瓶颈分布。σ衰减和不透明度调度（通过重参数化$o'(o) = O_t + (1-O_t) \cdot \operatorname{sigm}(o)$和线性调度$O_t: 0 \to 1$）共同构成了从半透明平滑三角形向不透明尖锐三角形转变的梯度桥梁——移除任一项均导致PSNR骤降约8 dB，说明训练早期的梯度流对最终收敛至关重要。第二阶段连通性优化的8.56 dB损失则表明，共享顶点网格带来的梯度累积效应（相邻三角形梯度在共享顶点处汇聚）对几何和外观的协同优化不可或缺。

Figure 7进一步消融了正则化项对网格质量的影响：(a) 无任何正则化时，渲染视图质量高但底层几何不准确；(b) 法线损失$\mathcal{L}_n$鼓励平滑表面，但无深度正则化$\mathcal{L}_d$时局部区域仍有几何误差；(c) 基线模型（含全部正则化）实现平滑且几何一致的表面；(d) 过度增强正则化强度虽产生更平滑几何，但球谐函数无法捕捉精细外观细节，视觉保真度下降。这表明正则化强度需在几何质量与视觉保真度之间取得平衡。

### 可扩展性与超参数

Table 9展示了顶点数对视觉质量的影响：MeshSplatting随顶点数增加呈现一致的性能提升趋势，表明方法具有良好的可扩展性。Table 5列出了关键超参数，包括学习率、损失权重$\beta_o, \beta_z, \beta_n, \beta_d$、增密间隔、剪枝阈值等，为复现提供了完整配置参考。

### 失败模式与局限性

尽管MeshSplatting在主要指标上表现优异，论文明确指出了以下局限性（Figure 13）：

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/024_Figure_13.jpg]]
*Figure 13: Limitations. Accurately recovering backgrounds (left), particularly under limited viewpoints, and handling transparent objects (right) remain challenging*

1. **背景恢复不足**：由于SfM初始点云在背景区域稀疏，背景几何不完整且保真度较低，尤其在有限视点条件下更为明显。
2. **训练视点外泛化差**：在训练视点范围以外渲染时，视觉质量显著下降，这是基于优化的重建方法的共性挑战。
3. **透明物体处理困难**：玻璃、瓶子等透明物体难以仅用不透明三角形表示，因为方法的核心设计目标即为全不透明网格。
4. **非显式水密性**：最终网格并非显式防水密性保证，尽管在许多下游应用中已可直接使用。

这些失败模式揭示了当前方法在稀疏观测区域和材质多样性场景下的根本瓶颈，也为后续研究指明了方向。

### 补充图表

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/005_Table_1.jpg]]
*Table 1: Mesh-based novel view synthesis on the Mip-NeRF360 dataset. MeshSplatting significantly outperforms all concurrent methods both in visual quality and in compactness, requiring far fewer vertices to achieve superior results. Mesh indicates whether a method directly produces a mesh (vs. requiring post-processing). Color denotes whether the mesh is already colored or requires some form of post-processing (e.g., coloring by fine-tuning). Connect specifies whether the final mesh consists of a connected component. Ready means the output is directly usable in standard game engines without custom rendering shaders. † with only opaque triangles*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/021_Table_11.jpg]]
*Table 11: Detailed ablations (Mip-NeRF360). We isolate the impact of each design choice by removing them individually*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/011_Figure_7.jpg]]
*Figure 7: Regularization vs. mesh quality. (a) Without any regularization, the rendered views have high visual quality, but the underlying geometry is inaccurate. (b) The normal loss*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/009_Table_3.jpg]]
*Table 3: Connectivity. Distribution of triangle connectivity on the Garden scene. The final mesh mostly consists of triangles connected to three or more neighboring triangles, indicating a wellconnected mesh*

![[assets/figures/papers/paper_list_l2132_https_arxiv_org_abs_2512_06818/figures/018_Table_9.jpg]]
*Table 9: Number of vertices vs visual quality. MeshSplatting scales effectively with the number of vertices, showing consistent improvements in visual quality as the vertex count increases. All improvements are shown relative to 2M*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

MeshSplatting 处于**可微渲染与显式网格重建**的交叉地带，其核心定位是填补“高质量新视角合成”与“游戏引擎直接可用性”之间的鸿沟。以下分析其在方法谱系中的相对位置。

**（1）相对于 3DGS 及其衍生方法**

原始 **3DGS** 通过大量半透明高斯椭球体实现了高质量体积渲染，但输出无法直接导入标准图形管线，需要后处理转换。MeshSplatting 在渲染质量上以 3DGS 作为体积渲染的上限参考，但目标不同：它直接输出不透明连通网格，省去了后处理步骤。

**2DGS**、**GOF**、**RaDe-GS** 等方法从高斯表示中提取网格，但存在两个共同瓶颈：① 需要额外的后处理步骤（如泊松重建或 TSDF 融合）才能获得网格；② 网格通常不带颜色，需要额外训练着色。MeshSplatting 通过端到端优化直接输出带颜色的不透明网格，消除了这两步依赖。

**MiLo** 是当前联合网格-高斯优化的最佳方法，但仍需后处理着色。MeshSplatting 在 Mip-NeRF360 上以 PSNR +0.69 dB 超越 MiLo，同时训练快 2 倍、内存少 2.5 倍（Table 2）。关键在于 MiLo 保留了半透明高斯基元用于颜色建模，而 MeshSplatting 通过不透明度重参数化和窗口参数调度，使三角形在训练结束时完全变为不透明，无需额外着色步骤。

**（2）相对于 Triangle Splatting**

Triangle Splatting 是最接近的三角基元方法，但其输出是**非连通三角形汤**，且三角形保持半透明。MeshSplatting 在此基础上做了三个关键改变：
- **连通性**：通过受限 Delaunay 三角剖分建立共享顶点网格（Section 3.3），消融实验显示移除该阶段导致 PSNR 下降 8.56 dB（Table 11）。
- **不透明度控制**：引入顶点级不透明度参数化和线性调度，使三角形从半透明逐渐变为不透明（Section 3.4）。
- **窗口参数共享**：所有三角形共享 σ 参数并线性退火，而非独立优化，这保证了全局一致的锐度过渡。

**（3）方法谱系定位总结**

| 维度 | 3DGS 系（体积） | Triangle Splatting | MiLo（混合） | MeshSplatting |
|------|----------------|-------------------|-------------|---------------|
| 基元类型 | 3D 高斯 | 非连通三角片 | 网格 + 高斯 | 连通不透明网格 |
| 是否需要后处理 | 是 | 是（非连通） | 是（着色） | 否 |
| 引擎直接可用 | 否 | 否 | 否 | 是 |
| 连通性 | 无 | 无 | 有 | 有 |

### 2. 适用边界与局限

**（1）背景区域重建**

由于从 SfM 稀疏点云初始化，背景区域点密度低，导致几何不完整且保真度较低（Figure 13 左）。这是所有基于 SfM 初始化方法的共同瓶颈，但 MeshSplatting 的不透明表示使该问题更加突出——半透明基元可以通过低不透明度“模糊”掩盖几何不足，而不透明三角形则直接暴露缺失区域。

**（2）视点外渲染**

在训练视点范围以外渲染时，视觉质量下降。这与 3DGS 面临相同挑战，但 MeshSplatting 的网格表示使得几何外推更加困难——网格的显式表面缺乏体积表示的“软边界”来平滑过渡到未观测区域。

**（3）透明物体**

透明物体（如玻璃、瓶子）难以仅用不透明三角形表示（Figure 13 右）。这是方法设计的固有局限：不透明三角形无法建模折射和透射效果。可能的扩展方向包括引入辅助透明基元或混合表示。

**（4）水密性**

网格并非显式防水密性。尽管受限 Delaunay 三角剖分建立了连通性，但未强制流形约束或防止自相交。Table 3 显示最终网格中大部分三角形连接 3 个以上邻居，表明连通性良好，但未提供水密性保证。对于需要严格水密性的物理模拟场景，可能需要额外后处理。

### 3. 开放问题

基于上述分析，以下问题值得进一步探索：

1. **视觉质量差距**：与 3DGS 的 PSNR 上限相比，不透明网格表示仍有差距。能否通过引入逐三角形纹理学习（类似神经纹理）进一步缩小差距？

2. **透明物体处理**：是否可以通过引入辅助透明基元（如少量高斯或透明三角片）来建模玻璃等材质，同时保持主体网格的不透明性？

3. **水密性增强**：是否可以增加额外正则化项（如自相交惩罚、流形约束）以强制水密性，使输出直接适用于更严格的物理模拟？

4. **初始化改进**：更丰富的初始点云（例如来自深度传感器或多视图立体）能否改善背景重建质量？

5. **场景扩展**：如何将方法扩展到无界场景（当前依赖背景球或天空盒）或动态场景？网格的显式拓扑可能使动态变形更可控，但也带来了拓扑变化处理的挑战。

6. **顶点数-质量权衡**：Table 9 显示视觉质量随顶点数增加而持续改善，但未探索上限。是否存在收益递减点？能否通过自适应顶点密度分配进一步优化？

## 原文 PDF

![[paperPDFs/CVPR_2026/MeshSplatting_Differentiable_Rendering_with_Opaque_Meshes.pdf]]