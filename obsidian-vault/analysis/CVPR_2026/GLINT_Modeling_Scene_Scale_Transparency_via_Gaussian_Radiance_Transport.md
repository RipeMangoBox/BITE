---
title: "GLINT: Modeling Scene-Scale Transparency via Gaussian Radiance Transport"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GLINT_Modeling_Scene_Scale_Transparency_via_Gaussian_Radiance_Transport.pdf
project_link: "https://youngju-na.github.io/GLINT"
code_link: null
aliases:
- GLINT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将场景的高斯原语显式分解为接口（interface）、透射（transmission）和反射（reflection）三个功能组，并通过透明度感知的混合渲染（光栅化+光线追踪）分别处理首表面可见性、背景辐射和镜面反射，使各组件独立优化并服从物理一致的辐射传输公式。
primary_logic: 通过显式解耦辐射成分，并利用自举的几何线索（如接口-透射深度差异和扩散反照率）在无分割掩码的情况下定位透明区域，结合视频重光照模型的先验提供几何和材质正则化，解决了透明场景中外观与几何的权衡难题。
claims:
- GLINT在合成数据集3D-FRONT-T上以Normal MAE 7.96、Depth AbsRel 0.04、Mesh CD 0.34全面超越所有基线（包括TSGS、EnvGS、PGSR等），证明分解表示对几何重建的决定性提升。
- 在真实数据集DL3DV-10K和合成数据集上同时取得最高的渲染质量（PSNR 30.21/34.50, SSIM 0.92/0.96），表明分解方案也改善了外观保真度。
- 消融实验中移除透射组件导致PSNR从34.50骤降至32.26，证明显式分离透射路径对透明场景重建至关重要。
- 3D-FRONT-T (synthetic) 上 Normal MAE↓ = 7.96
---

# GLINT: Modeling Scene-Scale Transparency via Gaussian Radiance Transport

> [!tip] 核心洞察
> 通过显式解耦辐射成分，并利用自举的几何线索（如接口-透射深度差异和扩散反照率）在无分割掩码的情况下定位透明区域，结合视频重光照模型的先验提供几何和材质正则化，解决了透明场景中外观与几何的权衡难题。

| 字段 | 内容 |
|------|------|
| 中文题名 | GLINT：基于高斯辐射传输建模场景级透明表面 |
| 英文题名 | GLINT: Modeling Scene-Scale Transparency via Gaussian Radiance Transport |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26181) · [Project](https://youngju-na.github.io/GLINT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GLINT |
| Dataset | 3D-FRONT-T, DL3DV-10K |

> [!tip] 效果简介
> - 3D-FRONT-T (synthetic) 上，Normal MAE↓ 7.96 vs 9.89 (TSGS) (-1.93)；Depth AbsRel↓ 0.04 vs 0.08 (TSGS) (-0.04)；Mesh CD↓ 0.34 vs 0.52 (PGSR/TSGS) (-0.18)。
> - DL3DV-10K (real) 上，PSNR↑ 30.21 vs 29.65 (EnvGS) (+0.56)。

## 概述

**GLINT** 提出了一种面向场景级透明表面重建的新框架，其核心目标是解决现有 3D 高斯泼溅方法在处理透明物体时的根本性困境：传统方法采用单体 α 混合，将来自透明界面、背景透射和环境反射的多条辐射路径纠缠为单一合成，导致几何与外观的固有冲突——透明高斯要么被推向零不透明度以呈现背景，要么变为不透明以保留几何完整性，最终造成透明表面几何不准确、伪影或缺失。

为突破这一瓶颈，GLINT 将场景的高斯原语显式分解为**接口（interface）**、**透射（transmission）** 和**反射（reflection）** 三个功能组，并通过透明度感知的混合渲染——光栅化处理首表面可见性，光线追踪查询背景辐射与镜面反射——使各组件独立优化并服从物理一致的辐射传输公式。同时，GLINT 利用自举的几何线索（接口-透射深度差与扩散反照率）在无任何分割掩码的条件下定位透明区域，并引入视频重光照模型 **DiffusionRenderer** 的编码器提供跨视角一致的几何与材质先验，从而在无需外部分割模型的情况下，实现对透明场景几何与外观的协同重建。

实验结果表明，GLINT 在合成数据集 **3D-FRONT-T** 上以 Normal MAE 7.96、Depth AbsRel 0.04、Mesh CD 0.34 全面超越所有基线方法（包括 TSGS、EnvGS、PGSR 等），同时在真实数据集 **DL3DV-10K** 和合成数据集上取得最高的渲染质量（PSNR 30.21/34.50, SSIM 0.92/0.96），验证了分解表示对几何重建和外观保真度的决定性提升。

## 背景与动机

### 透明场景重建的核心困境

在真实世界的三维场景中，透明表面（如玻璃窗、展柜、车窗）无处不在。然而，对这类场景进行高质量的三维重建与新颖视角合成，至今仍是计算机视觉与图形学领域的开放难题。其根本困境在于：**透明表面的出射辐射是多重光路的纠缠结果**——观察者看到的像素颜色，同时包含了透明界面本身的反射光、穿过透明介质透射而来的背景光，以及可能的环境镜面反射。这三条辐射路径在物理上相互独立，但在图像中却被压缩为单一的RGB值。

现有主流方法，尤其是以3D高斯泼溅（3DGS）及其变体为代表的显式辐射场方法，采用**单体α混合**来合成所有颜色信息。这种混合方式将来自透明界面、背景透射和环境反射的多条辐射路径强行纠缠为单一合成，导致几何与外观之间产生固有冲突：优化过程中，透明区域的高斯原语要么被推向零不透明度以呈现背景内容，要么变为不透明以保留几何完整性。最终结果是透明表面重建的几何不准确、伪影频发，甚至完全缺失——玻璃窗被重建为空洞，或窗框的几何结构被错误地延伸到透明区域。

### 现有方法的缺口

针对透明场景重建，学界已有多条探索路径，但各自存在显著局限：

- **基于分割掩码的方法**（如TSGS）：依赖外部分割模型（如Grounded-SAM2）生成玻璃区域掩码，然后对掩码区域施加特殊处理。然而，这类掩码往往稀疏且时空不一致，在复杂场景中容易遗漏或误标透明区域，且无法恢复透射辐射的物理属性。

- **引入环境建模的方法**（如EnvGS）：通过环境高斯和光线追踪来建模反射效应，在镜面反射场景中表现优异。但其设计缺少专门的透射组件，无法解耦背景辐射，面对透明场景时几何和外观质量均受限。

- **纯光栅化方法**（如3DGS、2DGS、PGSR）：完全依赖光栅化渲染，无法有效查询次级光路（透射和反射），在透明区域必然产生几何模糊或外观失真。

- **几何增强方案**（如2DGS）：采用透视正确投影和平面约束改善了表面几何，但未解决辐射成分的纠缠问题，透明表面的外观与几何权衡依然存在。

### 本文动机与核心思路

GLINT的提出正是为了从根本上解决上述困境。其核心洞察是：**只有将纠缠的辐射成分显式解耦，才能同时获得准确的几何和逼真的外观**。

具体而言，GLINT将场景的高斯原语显式划分为三个功能组：
- **接口组件**（G_intr）：捕获首表面可见性，作为几何载体；
- **透射组件**（G_trans）：建模穿过透明表面的背景辐射；
- **反射组件**（G_refl）：建模在非透明和透明界面处的环境反射。

通过**混合渲染策略**——对接口组件使用光栅化生成G-buffer（深度、法线、透明度、镜面度），再基于G-buffer使用光线追踪查询透射和反射组件——各组件可以独立优化，并服从物理一致的辐射传输公式。同时，GLINT利用自举的几何线索（如接口-透射深度差异和扩散反照率）在无分割掩码的情况下定位透明区域，并引入视频重光照模型的编码器提供跨视角一致的几何和材质先验，从而在透明场景中突破外观与几何的权衡瓶颈。

## 核心创新

GLINT 的核心创新在于将 3D 高斯泼溅从“单体混合”范式推进到“分解式辐射传输”范式。传统方法（包括 2DGS、PGSR、EnvGS 等）用单一高斯原语集通过标准 α 混合合成所有颜色，导致透明界面的几何与外观被纠缠在一起：优化时，透明区域的高斯要么被迫趋近零不透明度以展示背景，要么变为不透明以维持几何完整性，最终造成几何不准确、伪影或透明表面完全缺失。GLINT 通过以下五个关键设计突破这一瓶颈。

### 1. 三组件高斯分解表示

GLINT 将场景的高斯原语显式划分为三个功能组：**接口组件**（G_intr）、**透射组件**（G_trans）和**反射组件**（G_refl）。接口组件捕获首表面可见性并作为几何载体；透射组件建模穿过透明表面的背景辐射；反射组件处理非透明和透明界面处的环境反射。这种分解使各组件独立优化，从根本上解耦了几何与多条辐射路径。消融实验证实，移除透射组件导致 PSNR 从 34.50 骤降至 32.26，深度 AbsRel 从 0.035 升至 0.038（Table 3），证明显式分离透射路径对透明场景重建至关重要。

### 2. 混合渲染与透明度感知辐射传输

GLINT 采用**混合渲染策略**：对接口组件使用光栅化生成 G-buffer（深度、法线、透明度 t、镜面度 s），随后基于 G-buffer 使用光线追踪查询透射和反射组件。最终辐射通过物理启发的透明度门控公式合成：

$$L_o = (1 - t) L_{\mathrm{opaque}} + t L_{\mathrm{transparent}}$$

其中不透明分支和透明分支分别用菲涅尔加权镜面度 $k_s$ 混合接口基色与反射/透射颜色（Eq. 5-10）。这与 EnvGS 仅对反射使用光线追踪、且缺少透射分支的设计形成鲜明对比——Figure 13 显示 EnvGS 无法提供透射分量，其对应槽位为空。

### 3. 自举透明度定位

与传统方法依赖外部分割模型（如 Grounded-SAM2）生成玻璃掩码不同，GLINT 通过**自举机制**定位透明区域：利用接口-透射深度差 $\Delta z$ 和扩散反照率 $\hat{a}$ 生成二元透明度掩码 $M_{\mathrm{trans}}$（Eq. 13），并以此监督透明度缓冲 t 的学习（Eq. 14）。这一设计无需任何分割输入，避免了外部分割模型的稀疏性和时空不一致问题。Figure 15 显示 GLINT 的自举掩码比 Grounded-SAM2 更干净、一致，后者常产生噪声、不完整甚至完全缺失的掩码。

### 4. 视频重光照几何先验

GLINT 引入预训练视频重光照模型 **DiffusionRenderer** 的编码器，提供跨视角一致的深度、法线和反照率先验。通过比例-平移不变深度损失（Eq. 15）和阈值化法线损失（Appendix C）对接口 G-buffer 进行正则化，稳定几何收敛。消融实验表明，移除所有几何损失导致 Normal MAE 激增至 24.69，Depth AbsRel 升至 0.126（Table 3），证实几何先验对维持界面结构不可或缺。值得注意的是，Figure 14 显示即使为 EnvGS 添加相同的 DiffusionRenderer 先验，其在透明区域仍产生模糊渲染，说明先验本身不能替代分解表示。

### 5. 从薄透明到场景级透明的泛化

TSGS 等专门针对薄透明表面的方法需要分割掩码且无法恢复透射辐射，而 GLINT 的分解框架将透明度建模为连续缓冲 t，使同一套表示同时处理不透明、透明和反射区域。在合成数据集 3D-FRONT-T 上，GLINT 以 Normal MAE 7.96、Depth AbsRel 0.04、Mesh CD 0.34 全面超越所有基线（Table 1）；在真实数据集 DL3DV-10K 上同时取得最高渲染质量 PSNR 30.21（Table 2），证明分解方案在场景级透明重建中的普适优势。

## 整体框架

GLINT 的整体流水线围绕一个核心思想展开：将场景的高斯原语**显式分解为三个功能组**，并通过**混合渲染**和**物理启发的辐射传输公式**将它们整合为最终的出射辐射。图 2 给出了流水线概览。

### 三组件分解

与 3DGS/2DGS 使用单一高斯集合并以单体 α 混合合成所有颜色不同，GLINT 将场景中的每个高斯原语划分到三个独立的组件中：

- **接口组件** $\mathcal{G}_{\mathrm{intr}}$：负责捕获首表面可见性。该组件通过光栅化渲染，输出 G‑buffer（深度 $z$、法线 $\mathbf{n}$、透明度 $t$、镜面度 $s$），同时作为整个场景的几何载体。
- **透射组件** $\mathcal{G}_{\mathrm{trans}}$：负责建模穿过透明表面的背景辐射。该组件通过光线追踪查询，解耦背景内容与接口几何，避免背景被错误地“粘贴”到透明界面上。
- **反射组件** $\mathcal{G}_{\mathrm{refl}}$：负责建模在非透明和透明界面处的环境反射，同样通过光线追踪查询。

这种分解使每一类辐射成分可以独立优化，从根本上解决了单体 α 混合中“透明高斯要么被推向零不透明度以呈现背景，要么变为不透明以保留几何”的冲突。

### 混合渲染与辐射传输

渲染过程分为两步：

1. **光栅化阶段**：接口组件 $\mathcal{G}_{\mathrm{intr}}$ 采用 2DGS 的透视正确光栅化，生成 G‑buffer（深度、法线、透明度 $t$、镜面度 $s$）。
2. **光线追踪阶段**：基于 G‑buffer 提供的位置和方向信息，对透射组件 $\mathcal{G}_{\mathrm{trans}}$ 和反射组件 $\mathcal{G}_{\mathrm{refl}}$ 执行光线追踪查询，获取透射辐射 $L_{\mathrm{trans}}$ 和反射辐射 $L_{\mathrm{refl}}$。

最终的出射辐射 $L_o$ 由透明度门控的物理启发公式整合：

$$L_o = (1 - t) L_{\mathrm{opaque}} + t L_{\mathrm{transparent}}$$

其中不透明分支 $L_{\mathrm{opaque}}$ 和透明分支 $L_{\mathrm{transparent}}$ 分别用菲涅耳加权镜面度 $k_s$ 混合接口基色与反射/透射颜色：

$$L_{\mathrm{opaque}} = (1 - k_s) L_{\mathrm{intr}} + k_s L_{\mathrm{refl}}$$

$$L_{\mathrm{transparent}} = (1 - k_s) L_{\mathrm{trans}} + k_s L_{\mathrm{refl}}$$

菲涅耳反射率 $F(\omega_o)$ 由 Schlick 近似计算，镜面度 $k_s = s + (1-s)F(\omega_o)$ 用可学习的镜面度参数 $s$ 插值菲涅耳项。当 $t=0$ 时走不透明分支，$t=1$ 时走透明分支，中间值实现平滑过渡。

### 优化目标

训练通过最小化渲染图像与真值之间的光度损失 $\mathcal{L}_{\mathrm{photo}}$（L1 + SSIM + LPIPS 的组合）来驱动。同时，流水线引入两个关键的正则化模块：

- **几何正则化**：利用预训练视频重光照模型（DiffusionRenderer）的编码器，提供跨视角一致的深度先验 $\hat{z}$ 和法线先验 $\hat{\mathbf{n}}$，通过尺度-平移不变深度损失 $\mathcal{L}_{\mathrm{depth}}$ 和掩码法线损失 $\mathcal{L}_{\mathrm{normal}}$ 约束接口 G‑buffer。
- **透明度自举**：基于接口-透射深度差 $\Delta z$ 和扩散反照率 $\hat{a}$ 自动生成二值透明度掩码 $M_{\mathrm{trans}}$，并通过 L1 损失 $\mathcal{L}_{\mathrm{trans}}$ 监督预测的透明度缓冲 $t$，无需任何外部分割模型。

### 输入输出流

- **输入**：多视角 RGB 图像及对应的相机参数。
- **处理**：接口组件光栅化 → G‑buffer 提取 → 透射/反射光线追踪 → 辐射传输合成。
- **输出**：新视角渲染图像、法线图、透明度图、各辐射成分分解图，以及可导出的重建网格（通过 TSDF 融合）。

### 补充图表

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline Overview. The interface component*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/001_Figure_1.jpg]]
*Figure 1: Our framework GLINT performs decomposed Gaussian radiance transport to reconstruct transparent surfaces with physically consistent geometry and appearance. (Left) The first row shows a rendered image, normal map, and transparency map. The second row visualizes the radiance contributions of the interface, transmission, and reflection components. (Right) Reconstructed Mesh*

## 核心模块与公式推导

GLINT 的核心在于将场景的高斯原语显式分解为三个功能组件，并通过透明度感知的混合渲染管线与物理启发的辐射传输公式进行整合。以下按模块逐一阐述其设计与关键公式。

### 基础表示：2D 高斯泼溅

GLINT 构建于 2D Gaussian Splatting (2DGS) 之上，采用定义在局部切平面上的各向异性 2D 高斯作为场景基元。每个基元在切平面局部坐标 $(u, v)$ 上的权重由下式评估：

$$G _ { i } ( { \mathbf { u } } _ { i } ) = \exp \left[ - { \textstyle \frac { 1 } { 2 } } ( u ^ { 2 } + v ^ { 2 } ) \right]$$

基元 $i$ 在像素 $\mathbf{p}$ 处的不透明度贡献为基不透明度 $o_i$ 与高斯权重的乘积：

$$\alpha _ { i } ( \mathbf { p } ) = o _ { i } \cdot G _ { i } ( \mathbf { u } _ { i } ( \mathbf { p } ) )$$

传统 2DGS 通过前端到后端的 alpha 混合合成像素辐射：

$$\mathbf { L } ( \mathbf { o } , \mathbf { d } ) = \sum _ { i \in S ( \mathbf { r } ) } T _ { i } \alpha _ { i } ( \mathbf { p } ) \mathbf { c } _ { i } ( \mathbf { d } )$$

其中 $T _ { i } = \prod _ { j < i } ( 1 - \alpha _ { j } ( \mathbf { p } ) )$ 为累积透射率。然而，该单体混合范式将透明界面的多条辐射路径纠缠为单一合成，是透明场景几何与外观冲突的根源。

### 场景表示与辐射分解

GLINT 将高斯原语显式划分为三个功能组：

- **接口组件 $\mathcal{G}_{\text{intr}}$**：捕获首表面可见性，作为几何载体。通过光栅化渲染生成 G-buffer，包含深度 $z$、法线 $\mathbf{n}$、透明度 $t$ 和镜面度 $s$。
- **透射组件 $\mathcal{G}_{\text{trans}}$**：建模穿过透明表面的背景辐射。使用光线追踪查询，解耦背景与接口几何。
- **反射组件 $\mathcal{G}_{\text{refl}}$**：建模在非透明和透明界面处的环境反射。同样使用光线追踪查询。

渲染策略为混合渲染：接口组件使用光栅化以获得高效的首表面可见性；透射和反射组件则基于 G-buffer 信息，通过硬件加速的光线追踪（BVH 遍历）进行查询。

### 透明度感知的辐射传输公式

GLINT 的核心公式是透明度门控的出射辐射合成：

$$L _ { o } = \left( 1 - t \right) L _ { \mathrm { o p a q u e } } + t L _ { \mathrm { t r a n s p a r e n t } }$$

其中 $t$ 为 G-buffer 中的透明度缓冲。当 $t=0$ 时走不透明分支，$t=1$ 时走透明分支，中间值实现平滑过渡。

**菲涅尔加权镜面度**：采用 Schlick 近似计算菲涅尔反射率：

$$F ( \omega _ { o } ) = F _ { 0 } + ( 1 - F _ { 0 } ) ( 1 - \operatorname* { m a x } ( 0 , \omega _ { o } \cdot { \bf n } ) ) ^ { 5 }$$

用可学习的镜面度 $s$ 插值菲涅尔反射，得到菲涅尔加权镜面度：

$$k _ { s } = s + ( 1 - s ) F ( \omega _ { o } )$$

**不透明分支**：不透明表面的出射辐射为接口基色与反射色的混合：

$$L _ { \mathrm { o p a q u e } } = \left( 1 - k _ { s } \right) L _ { \mathrm { i n t r } } + k _ { s } L _ { \mathrm { r e f l } }$$

**透明分支**：透明表面的出射辐射为透射背景色与反射色的混合：

$$L _ { \mathrm { t r a n s p a r e n t } } = \left( 1 - k _ { s } \right) L _ { \mathrm { t r a n s } } + k _ { s } L _ { \mathrm { r e f l } }$$

该公式体系使接口几何、背景透射和环境反射各自独立优化，同时服从物理一致的辐射传输约束。

### 优化目标

**光度损失**：结合 L1、SSIM 和 LPIPS 的渲染监督：

$$\mathcal { L } _ { \mathrm { p h o t o } } = \lambda _ { 1 } \mathcal { L } _ { 1 } + \lambda _ { \mathrm { s s i m } } \mathcal { L } _ { \mathrm { S S I M } } + \lambda _ { \mathrm { l p i p s } } \mathcal { L } _ { \mathrm { L P I P S } }$$

**几何正则化损失**：利用视频重光照模型 DiffusionRenderer 的编码器提供跨视角一致的深度 $\hat{z}$ 和法线 $\hat{\mathbf{n}}$ 先验：

$$\mathcal { L } _ { \mathrm { g e o } } = \lambda _ { d } \mathcal { L } _ { \mathrm { d e p t h } } ( z , \hat { z } ) + \lambda _ { n } \mathcal { L } _ { \mathrm { n o r m a l } } ( \mathbf { n } , \hat { \mathbf { n } } )$$

其中深度损失采用比例-平移不变形式：

$$\mathcal { L } _ { \mathrm { d e p t h } } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \left( w z _ { i } + q - \hat { z } _ { i } \right) ^ { 2 }$$

法线损失仅在余弦相似度超过阈值 $\tau_n$ 的像素上计算，以过滤噪声先验：

$$\mathcal { L } _ { \mathrm { n o r m a l } } = \sum _ { u } \mathbf { M } ( u ) \big ( 1 - \langle \mathbf { n } ( u ) , \hat { \mathbf { n } } ( u ) \rangle \big )$$

其中 $\mathbf { M } _ { \mathrm { p r i o r } } ( u ) = \big [ \langle \mathbf { n } ( u ) , \hat { \mathbf { n } } ( u ) \rangle \geq \tau _ { \mathrm { n } } \big ]$。

### 透明度自举模块

GLINT 无需外部分割掩码，而是通过自举机制定位透明区域。利用接口-透射深度差 $\Delta z$ 和扩散反照率 $\hat{a}$ 生成二元透明度掩码：

$$M _ { \mathrm { t r a n s } } = \mathbf { 1 } \big ( ( \Delta z > \tau _ { d } ) \wedge ( \hat { a } < \gamma _ { a } ) \big )$$

然后用 L1 损失监督预测的透明度缓冲 $t$ 与该掩码对齐：

$$\mathcal { L } _ { \mathrm { t r a n s } } = \lambda _ { t } \| M _ { \mathrm { t r a n s } } - t \| _ { 1 }$$

该模块的核心逻辑是：透明区域中接口深度（首表面）与透射深度（背景）存在显著差异，且扩散反照率较低；通过这两个线索即可在无掩码条件下自举定位透明表面。

## 实验与分析

### 核心定量结果

GLINT 在两个基准上同时刷新了几何与外观重建的记录。**Table 1** 报告了合成数据集 3D-FRONT-T 上的几何指标：Normal MAE 降至 **7.96**（此前最佳 TSGS 为 9.89），Depth AbsRel 降至 **0.04**（TSGS 为 0.08），Mesh CD 降至 **0.34**（PGSR/TSGS 为 0.52）。这三项指标的显著领先表明，显式辐射分解使透明表面的几何重建从“勉强可辨认”提升至“接近真值”的水平。

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation of geometry on the synthetic 3D-FRONT-T dataset. We report normal metrics (MAE, and accuracy thresholds of 11.25◦, 22.5◦) and depth metrics (AbsRel, RMSE, δ \< 1.25), along with mesh metrics (CD, F1-score)*

外观质量同样全面占优（**Table 2**）：在真实数据集 DL3DV-10K 上 PSNR 达到 **30.21**（EnvGS 为 29.65），在 3D-FRONT-T 上 PSNR 达到 **34.50**（EnvGS 为 33.71），LPIPS 降至 **0.048**（EnvGS 为 0.07，TSGS 高达 0.14）。值得注意的是，TSGS 虽专为薄透明几何设计，但其 LPIPS 高达 0.14，反映出缺乏透射建模导致的外观严重失真——这正是 GLINT 通过显式透射组件解决的核心矛盾。

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/010_Table_2.jpg]]
*Table 2: Photometric evaluation on real and synthetic datasets. GLINT achieves state-of-the-art rendering quality, quantitatively outperforming all baseline methods on both benchmarks*

定性对比（**Figure 5**、**Figure 7**）进一步验证了数字背后的视觉差异：PGSR 在透明区域产生破碎的深度图，EnvGS 的反射建模尚可但透射区域模糊，TSGS 虽能恢复部分几何却丢失了背景内容；GLINT 则同时保持了清晰的界面几何和完整的背景透射。**Figure 6** 的 TSDF 融合网格可视化显示，GLINT 生成的透明表面网格明显更干净、更完整。

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on synthetic scenes. Each column shows results from GT, PGSR [5], EnvGS [39], TSGS [24], and Ours. For each scene, rows correspond to RGB (top) and depth maps (bottom)*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/007_Figure_6.jpg]]
*Figure 6: Mesh visualization comparison. The meshes are obtained from TSDF fusion following baselines*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison on DL3DV-10K dataset. Each column shows results from GT, PGSR [5], EnvGS [39], TSGS [24], and Ours. For each scene, rows correspond to RGB (top) and normal (bottom) maps*

### 消融实验：各组件的因果贡献

**Table 3** 的消融实验精确量化了每个设计选择的边际贡献，结论与论文的核心因果主张高度一致：

**透射组件（G_trans）是决定性瓶颈。** 移除透射组件后，PSNR 从 34.50 骤降至 **32.26**（降幅 2.24 dB），远超移除反射组件的影响（降至 32.70）。这直接验证了分析中的核心判断——透明场景重建的根本困难在于透射路径与界面几何的纠缠，而非反射建模的不足。深度 AbsRel 也从 0.035 升至 0.038，说明缺少透射分离会导致背景内容错误地附着在接口高斯上，造成几何模糊。**Figure 10** 的定性消融直观展示了这一现象：无透射分支时，玻璃窗后的场景内容消失或扭曲。

**反射组件（G_refl）改善镜面区域的保真度，但对几何影响有限。** 移除反射组件使 PSNR 降至 32.70，主要损失集中在镜面高光区域，而 Normal MAE（7.96→8.12）和 Depth AbsRel（0.035→0.036）基本稳定。这表明反射建模是“锦上添花”的外观增强，而非几何重建的必要条件。

**几何先验对维持界面结构至关重要。** 去掉所有几何损失（L_geo）后，Normal MAE 从 7.96 激增至 **24.69**，Depth AbsRel 从 0.035 升至 **0.126**——几何完全崩溃。单独移除法线损失使 Normal MAE 升至 12.21，移除深度损失使 Depth AbsRel 升至 0.061，证实了两者的互补作用。**Figure 11** 的定性消融显示，缺少深度监督时接口深度变得不准确，缺少法线监督时表面朝向不稳定，而全部移除则导致深度和法线同时严重失真。这验证了视频重光照模型提供的跨视角一致先验对稳定几何收敛的关键作用。

**透明度自举损失（L_trans）确保透明度图的空间一致性。** 移除 L_trans 后 PSNR 降至 33.57，**Figure 12** 显示透明度图噪声显著增大、空间一致性变差。这说明仅靠辐射传输公式的隐式优化不足以可靠定位透明区域，显式的自举掩码监督是必要的引导信号。

### 效率与能力的权衡

**Table 4** 报告了计算成本对比：GLINT 的渲染速度为 **51 FPS**，慢于 TSGS（159 FPS）但显著快于离线渲染。训练时间约 2.5 小时（单张 RTX 4090）。这一速度差距源于混合渲染管线中光线追踪的额外开销，但考虑到 GLINT 同时重建了几何、透射和反射三种辐射成分，51 FPS 的实时交互帧率已具备实用价值。对于极低延迟应用，这是当前方法的一个已知局限。

### 失败模式与边界条件

尽管整体表现优异，GLINT 在以下场景中存在系统性局限：

1. **嵌套透明结构**：当前辐射传输公式仅建模一阶透射和反射，无法处理光线穿过多层透明表面（如玻璃柜中的玻璃花瓶）的多次弹射。这在消融实验中未被直接测试，但论文将其列为已知局限。

2. **稀疏视角下的分解欠定性**：当输入视角较少或视差有限时，反射和透射成分的分解可能变得欠定，优化可能错误分配辐射。这是物理上固有的歧义，需要更强的先验或语义约束来解决。

3. **对视频先验的依赖**：几何正则化依赖视频重光照模型的编码器提供跨视角一致的深度和法线。在只有静态图像集（无多帧时序信息）的场景中，该先验的可用性和质量可能下降。**Figure 14** 的对照实验显示，即使给 EnvGS 加上同样的 DiffusionRenderer 先验，其透明区域仍无法产生一致的深度和法线，证明先验本身不是充分条件——分解表示才是关键。

4. **初始几何质量对自举透明度的影响**：透明度自举掩码依赖接口-透射深度差（Δz > τ_d），如果训练初期接口几何较差，深度差可能不可靠，导致透明度定位失败。论文未报告该场景下的鲁棒性测试，需要手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/011_Table_3.jpg]]
*Table 3: Ablation studies on our method. We report PSNR, SSIM, LPIPS, Normal MAE, and Depth AbsRel*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/013_Figure_10.jpg]]
*Figure 10: Qualitative ablation study on representation components. Visual comparison between the full model and ablated variants*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/014_Figure_11.jpg]]
*Figure 11: Effect of geometric losses. Ablating geometric supervision leads to degraded geometry reconstruction. Removing Ldepth produces inaccurate interface depth, removing*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/015_Figure_12.jpg]]
*Figure 12: Effect of the transparency loss*

![[assets/figures/papers/paper_list_l2083_https_arxiv_org_abs_2603_26181/figures/016_Table_4.jpg]]
*Table 4: Comparison of computational costs and reconstruction quality on the 3D-FRONT-T dataset*

## 方法谱系与知识库定位

### 1. 核心瓶颈与解决路径

GLINT 的根本动机源于 3D 高斯泼溅（3DGS）家族在处理**场景级透明表面**时的一个结构性缺陷：单体 α 混合（monolithic alpha blending）将来自透明界面、背景透射和环境反射的多条辐射路径纠缠为单一合成，导致几何与外观的固有冲突。优化时，透明高斯要么被推向零不透明度以呈现背景，要么变为不透明以保留几何完整性，最终造成透明表面重建的几何不准确、伪影或缺失。

GLINT 的因果调节旋钮（causal knob）是将场景的高斯原语**显式分解**为接口（G_intr）、透射（G_trans）和反射（G_refl）三个功能组，并通过**透明度感知的混合渲染**（光栅化 + 光线追踪）分别处理首表面可见性、背景辐射和镜面反射，使各组件独立优化并服从物理一致的辐射传输公式。核心洞察在于：通过显式解耦辐射成分，并利用自举的几何线索（如接口-透射深度差和扩散反照率）在无分割掩码的情况下定位透明区域，结合视频重光照模型的先验提供几何和材质正则化，解决了透明场景中外观与几何的权衡难题。

### 2. 在 3DGS 方法谱系中的定位

GLINT 建立在 **2DGS**（Huang et al., 2024）的几何表示之上，继承了其各向异性 2D 高斯和透视正确投影的特性，但将单一原语集扩展为功能分解的三组件架构。在渲染策略上，GLINT 融合了光栅化与光线追踪两条技术路线：

- **纯光栅化路线**：3DGS、2DGS 以及 **PGSR**（平面约束高斯泼溅）均采用 α 混合进行前向渲染。它们缺乏对透射和反射的显式建模，在透明场景中几何重建质量受限。GLINT 在合成数据集 3D-FRONT-T 上以 Normal MAE 7.96 和 Depth AbsRel 0.04 大幅超越 PGSR（Table 1），证实分解表示对几何重建的决定性提升。

- **光线追踪路线**：**EnvGS** 引入环境高斯和光线追踪来建模反射，是 GLINT 在反射组件设计上的直接参照。但 EnvGS 缺少透射组件，导致透明区域的深度和法线仍然不一致，渲染模糊（Figure 14）。GLINT 的透射组件填补了这一空白——消融实验中移除透射组件导致 PSNR 从 34.50 骤降至 32.26（Table 3），证明显式分离透射路径对透明场景重建至关重要。

- **薄透明专用方法**：**TSGS** 专门针对薄透明表面几何重建，但需要外部分割掩码（如 Grounded-SAM2）且无法恢复透射辐射。GLINT 通过自举透明度定位（Eq. 13-14）摆脱了对分割模型的依赖，同时完整建模了透射和反射，在 Mesh CD 指标上以 0.34 对比 TSGS 的 0.52（Table 1），且透明度掩码比 Grounded-SAM2 更干净、一致（Figure 15）。

- **强镜面反射方法**：**Ref-GS** 面向强镜面反射场景，GLINT 的反射组件与之形成互补——通过菲涅耳加权镜面度 k_s（Eq. 7）统一处理非透明与透明界面的反射，在真实数据集 DL3DV-10K 上以 PSNR 30.21 超越所有基线（Table 2）。

### 3. 知识库贡献与适用边界

GLINT 的核心知识贡献包括：

1. **辐射分解表示**：将高斯原语按功能划分为接口、透射、反射三组，为透明场景重建提供了可泛化的表示框架。
2. **混合渲染管线**：光栅化处理首表面可见性并生成 G-buffer，光线追踪查询二次效应，实现了效率与物理一致性的平衡（51 FPS，Table 4）。
3. **自举透明度定位**：利用接口-透射深度差 Δz 和扩散反照率 â 生成二元透明度掩码，无需任何分割输入。
4. **视频重光照先验正则化**：引入 DiffusionRenderer 编码器提供跨视角一致的几何和材质先验，通过比例-平移不变深度损失（Eq. 15）和阈值化法线损失（Appendix C）稳定优化。

**适用边界与局限**：

- 当前的辐射传输公式集中于**一次反射和一次透射**（一阶相互作用），无法处理嵌套透明结构（如玻璃柜中的玻璃花瓶）或多次反弹现象。
- 在稀疏视角或视差有限的场景中，反射和透射成分的分解可能变得**欠定**，优化可能错误分配辐射。
- 虽然 FPS 可达 51，但仍低于纯光栅化方法（如 TSGS 的 159 FPS），难以满足极低延迟应用。
- 对**视频重光照模型先验**的依赖可能限制其在没有多帧输入的静止图像集上的应用。训练时间约 2.5 小时，内存消耗较高，需在更广泛设备上优化。

### 4. 开放问题

1. **高阶光传输**：如何扩展混合渲染管线以支持递归光线追踪或多次弹射，从而模拟嵌套透明和多次反射/透射？
2. **语义约束**：能否结合视觉-语言模型（VLMs）引入语义约束，在稀疏观测下帮助区分反射与透射成分？
3. **鲁棒性增强**：自举透明度定位在训练初期依赖深度差，如果初始几何较差，该方法是否会失效？如何增强其鲁棒性？
4. **推广到折射与半透明**：提出的分解框架能否推广到折射透明（如水晶球）或半透明介质？
5. **效率优化**：如何降低训练时间和内存消耗，使得该方法可以在消费级设备上运行？

## 原文 PDF

![[paperPDFs/CVPR_2026/GLINT_Modeling_Scene_Scale_Transparency_via_Gaussian_Radiance_Transport.pdf]]