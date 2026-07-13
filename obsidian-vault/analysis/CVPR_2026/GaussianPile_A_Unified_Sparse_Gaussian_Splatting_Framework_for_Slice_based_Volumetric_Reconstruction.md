---
title: "GaussianPile: A Unified Sparse Gaussian Splatting Framework for Slice-based Volumetric Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GaussianPile_A_Unified_Sparse_Gaussian_Splatting_Framework_for_Slice_based_Volumetric_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- GaussianPile
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将成像系统的聚焦物理（PSF/敏感度图）显式注入高斯的渲染流程：通过轴向重参数化（协方差注入）与不透明度调制（马氏距离衰减），使基元的轴向贡献与聚焦区精确匹配，同时舍弃球谐函数以减少参数冗余。
primary_logic: 物理驱动的聚焦感知管线（轴向重参数化+不透明度调制+加法光栅化）天然保证3D-2D一致性，维护体积结构的同时保留实时渲染效率和紧凑性，一条可微分CUDA管线即可实现高保真重建、快速渲染与高压缩比。
claims:
- 融合物理聚焦模型同时提升2D切片渲染与3D体积重建质量（表1、表3）。
- GaussianPile在所有超声数据集和多数显微数据集上取得最优2D/3D指标，显著优于INR方法和3DGS。
- 消融实验证实设置切片厚度等于真实层间距（σ_z ≈ δ_z）在2D与3D指标上均为最优。
- 方法在平均8分钟内收敛（约比INIF快5倍），同时实现高达19倍的平均压缩比。
---

# GaussianPile: A Unified Sparse Gaussian Splatting Framework for Slice-based Volumetric Reconstruction

> [!tip] 核心洞察
> 物理驱动的聚焦感知管线（轴向重参数化+不透明度调制+加法光栅化）天然保证3D-2D一致性，维护体积结构的同时保留实时渲染效率和紧凑性，一条可微分CUDA管线即可实现高保真重建、快速渲染与高压缩比。

| 字段 | 内容 |
|------|------|
| 中文题名 | GaussianPile：面向切片式体积重建的统一稀疏高斯泼溅框架 |
| 英文题名 | GaussianPile: A Unified Sparse Gaussian Splatting Framework for Slice-based Volumetric Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.20611) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | GaussianPile |
| Dataset | ABUS, rDL-LSM, ISBI12, CREMI |

> [!tip] 效果简介
> - ABUS 上，2D PSNR (dB) 33.07 vs 29.67 (HEVC) (+3.40)；3D PSNR (dB) 33.22 vs 28.49 (3DGS) (+4.73)；压缩比 (CR) 19× vs 15× (INIF) (+4×)。
> - rDL-LSM 上，2D PSNR (dB) 34.57 vs 29.34 (HEVC) (+5.23)；3D PSNR (dB) 34.47 vs 25.39 (3DGS) (+9.08)。
> - ISBI12 上，2D PSNR (dB) / 2D SSIM / 3D PSNR (dB) / 3D SSIM / CR / 时间 28.79 / 0.815 / 28.98 / 0.881 / 8× / 6m vs 25.19 / 0.708 / 24.98 / 0.715 / 3× / 51m (CoordNet) (+3.60 / +0.107 / +4.00 / +0.166 / +5× / 8.5倍加速)。

## 概要

体积成像中切片式采集（如超声、光片显微镜、序列切片电子显微镜）面临一个根本矛盾：**2D渲染看似合理，但3D内部结构严重错乱**。标准3D高斯泼溅（3DGS）的渲染模型基于针孔相机假设，未考虑成像系统真实的有限焦深物理过程，导致基元在轴向任意贡献，产生大量漂浮伪影。现有隐式神经表示（INR）方法虽能建模切片形成，但训练缓慢、压缩率有限。

**GaussianPile** 提出一种统一的稀疏高斯泼溅框架，核心创新在于将成像系统的聚焦物理显式注入渲染管线。通过**轴向重参数化**将有限轴向分辨率编码进高斯协方差，配合**不透明度调制**抑制离焦基元贡献，并采用**加法光栅化**替代传统alpha混合，天然保证3D-2D一致性。该方法同时舍弃球谐函数，在保留实时渲染效率的同时实现高压缩比。

实验表明，GaussianPile在超声（ABUS、rDL-LSM）和显微数据集（ISBI12、CREMI）上全面超越INR方法和切片适配的3DGS。在ABUS上，2D PSNR达33.07 dB（较HEVC提升3.40 dB），3D PSNR达33.22 dB（较3DGS提升4.73 dB）；平均训练时间仅约8分钟（比INIF快约5倍），压缩比高达19倍。消融实验证实，将切片厚度设为真实层间距时2D/3D指标均达最优，验证了物理模型的准确性。

体积成像数据——涵盖超声、光片显微镜、共聚焦显微镜、序列切片电子显微镜（ssEM）等——在现代生物医学研究与临床诊断中无处不在。这类数据以**切片式（slice-based）**方式采集：成像系统沿深度方向逐层扫描，生成一组二维图像栈。与自然图像的“全聚焦”针孔相机模型不同，切片式成像的物理过程受制于**有限焦深**：系统点扩散函数（PSF）在轴向（z方向）具有各向异性响应，仅对焦平面附近区域敏感，离焦信号则迅速衰减。这一物理特性构成了体积重建的核心挑战：**标准3DGS的渲染模型未考虑切片成像的实际物理过程，无法建模有限焦深带来的各向异性轴向响应，导致2D渲染看似合理但3D内部结构严重错乱，产生漂浮伪影**。

现有体积数据压缩与重建方法可归为三类，各有其根本性局限：

- **传统压缩标准（如HEVC）**将体积栈视为视频序列，利用帧间冗余进行编码。其压缩率可观，但解码后的体素网格保真度有限，且无法提供连续的三维表示。
- **隐式神经表示（INR）方法**（如**INIF**、**CoordNet**、**NeurComp**）将体积建模为连续函数，通过坐标网络隐式编码密度场。这类方法在压缩比上表现优异，但训练耗时长达数小时，且渲染需逐点查询网络，难以实现实时交互。
- **3DGS及其切片适配版本**虽具备实时渲染能力，但其渲染模型基于全聚焦针孔相机假设（$\sigma_z \to \infty$），基元无论深度均参与投影。即使引入简单的深度衰减，也无法精确建模有限焦深的物理卷积效应，导致**2D渲染看似合理但3D内部结构严重错乱**——基元可自由漂浮于体积内部而不受轴向约束。

上述缺口揭示了一个根本性矛盾：**INR方法追求高压缩比与连续表示，却牺牲了训练与渲染效率；3DGS追求实时渲染，却因忽视成像物理而丧失体积结构保真度**。是否存在一种统一框架，能同时满足高保真重建、快速训练、实时渲染与高压缩比？

本文的动机正是弥合这一鸿沟。核心洞察在于：**将成像系统的聚焦物理（PSF/敏感度图）显式注入高斯的渲染流程**——通过轴向重参数化与不透明度调制，使基元的轴向贡献与聚焦区精确匹配——可以天然保证3D-2D一致性，维护体积结构的同时保留实时渲染效率和紧凑性。这一思路催生了**GaussianPile**：一个面向切片式体积重建的统一稀疏高斯泼溅框架，以一条可微分CUDA管线实现高保真重建、快速渲染与高压缩比。

## 核心方法与创新机理

GaussianPile 的核心创新在于将切片式成像系统的物理聚焦过程显式注入高斯泼溅的渲染管线，从而在根本上解决标准 3DGS 无法建模有限焦深所导致的 3D-2D 不一致问题。

### 问题瓶颈：3DGS 的物理失配

标准 3DGS 的渲染模型基于针孔相机假设（全聚焦，$\sigma_z \to \infty$），其 alpha 混合与球谐函数着色机制天然适配多视角自然图像，但完全忽略了切片成像的实际物理过程。在超声、光片显微镜等切片式模态中，成像系统具有有限的轴向分辨率 $\sigma_z$，即点扩散函数（PSF）在深度方向呈高斯衰减。当直接使用 3DGS 进行切片式体积重建时，2D 渲染结果看似合理，但 3D 内部结构严重错乱，产生大量漂浮伪影——这是因为基元在轴向的贡献未被物理约束，导致优化过程缺乏 3D 监督信号。

### 因果旋钮：聚焦感知渲染管线

GaussianPile 的核心设计是将成像系统的 PSF 物理模型注入高斯的渲染流程，形成三个关键的 **changed slots**：

**1. 渲染模型：从视角依赖着色到聚焦感知加法光栅化（changed slot）**

标准 3DGS 采用基于视角的 alpha 混合与球谐函数着色。GaussianPile 完全舍弃球谐函数，转而通过协方差驱动的强度表示，将渲染重新定义为聚焦感知的加法累积过程。这一改变的直接收益是每个高斯基元的参数量减少约 40%，同时使渲染强度与成像物理直接对齐。

**2. 切片形成物理建模：轴向重参数化与不透明度调制（changed slot）**

这是方法最关键的创新。GaussianPile 假设成像系统的 PSF 为空间不变的 3D 高斯函数，并定义敏感度图 $h(-z_c) = \exp(-z_c^2 / 2\sigma_z^2)$ 作为系统的轴向反向脉冲响应。在此基础上，两个核心操作被引入：

- **轴向重参数化**：将轴向分辨率项 $\sigma_z^{-2}$ 注入逆协方差矩阵，生成有限厚度的聚焦高斯（Focus Gaussian）：
  $$\pmb{\Sigma}_e^{-1} = \pmb{\Sigma}_c^{-1} + \frac{\mathbf{e}_3 \mathbf{e}_3^{\top}}{\sigma_z^2}, \quad \pmb{\mu}_e = \pmb{\Sigma}_e \pmb{\Sigma}_c^{-1} \pmb{\mu}_c$$
  这使得每个基元在轴向的贡献范围与成像系统的聚焦区精确匹配。

- **不透明度调制**：利用马氏距离变化计算调制因子，抑制离焦基元的贡献：
  $$\mathrm{opacity}_r = \exp\left(-\frac{1}{2}\left(\pmb{\mu}_c^{\top} \pmb{\Sigma}_c^{-1} \pmb{\mu}_c - \pmb{\mu}_e^{\top} \pmb{\Sigma}_e^{-1} \pmb{\mu}_e\right)\right)$$
  这保证了只有位于聚焦区内的基元对渲染产生显著贡献，天然维护了 3D-2D 一致性。

**3. 压缩策略：莫顿量化与熵编码（changed slot）**

GaussianPile 引入莫顿排序（Z-order）对高斯基元进行空间局部化重排，随后对位置（14 bit）、不透明度（12 bit）、尺度（12 bit）和四元数（12 bit）进行自适应精度量化，最后通过 delta 编码和 LZMA 熵编码实现高压缩比。消融实验表明，该量化方案将平均压缩比从 3.4× 提升至 19×，且不降低重建质量。

### 核心洞察

物理驱动的聚焦感知管线（轴向重参数化 + 不透明度调制 + 加法光栅化）天然保证了 3D-2D 一致性：2D 切片渲染与 3D 体积重建共享同一组高斯基元，优化 2D 损失即可同时约束 3D 结构，无需额外的 3D 监督。这一设计使 GaussianPile 在一条可微分 CUDA 管线中同时实现高保真重建、实时渲染（>100 FPS）与高压缩比（平均 19×）。

### 决定性证据

- **融合物理聚焦模型同时提升 2D 与 3D 质量**：Table 1 和 Table 3 显示，GaussianPile 在所有超声数据集和多数显微数据集上取得最优 2D/3D 指标，在 ABUS 数据集上 3D PSNR 达 33.22 dB（+4.73 dB vs. 3DGS），在 rDL-LSM 数据集上 3D PSNR 达 34.47 dB（+9.08 dB vs. 3DGS）。
- **物理模型准确性验证**：消融实验（Table 4）证实，当切片厚度设为真实层间距 $\sigma_z \approx \delta_z$ 时，2D 与 3D 指标均为最优，验证了聚焦前向模型的物理准确性。
- **漂浮伪影消除**：Figure 5 可视化对比表明，虽然 3DGS 可生成看似合理的 2D 投影，但其重建体积在轴向（z 轴）视角下存在严重伪影，而 GaussianPile 的体积结构清晰完整。
- **效率与压缩比**：方法在平均 8 分钟内收敛（约比 INIF 快 5 倍），同时实现高达 19 倍的平均压缩比（Table 2）。

GaussianPile 的核心设计思路是将切片式成像的物理聚焦模型显式注入 3D 高斯泼溅的渲染管线，从而在保留实时渲染和紧凑表征优势的同时，天然维护 3D 体积结构的一致性。整个框架由三个关键阶段串联而成，形成一条完全可微的 CUDA 管线。

**输入与表征。** 方法将待重建的体积表征为一组各向异性的 3D 高斯基元 $\{(\pmb{\mu}_i, \pmb{\Sigma}_i, \alpha_i)\}$，其中 $\pmb{\mu}_i$ 为空间均值，$\pmb{\Sigma}_i$ 为协方差矩阵，$\alpha_i$ 为基元不透明度。与标准 3DGS 的关键区别在于，GaussianPile 完全舍弃了球谐函数（SH）系数，转而通过协方差驱动的强度表征来编码外观信息，使每个基元的参数量减少约 40%，同时消除了视角依赖着色的冗余。

**阶段一：聚焦感知的轴向重参数化与不透明度调制。** 给定成像系统的点扩散函数（PSF）——假设为空间不变的 3D 高斯函数，其轴向分辨率由 $\sigma_z$ 控制——管线首先将轴向分辨率项注入基元在相机坐标系下的逆协方差矩阵，生成有限厚度的“聚焦高斯”（Focus Gaussian）。这一轴向重参数化操作使基元的轴向贡献范围与成像系统的有限焦深精确匹配。随后，利用轴向注入引起的马氏距离变化计算不透明度调制因子 $\mathrm{opacity}_r$，有效抑制离焦基元对当前切片的贡献，从而消除漂浮伪影并稳定薄切片的重建。

**阶段二：屏幕空间投影。** 聚焦高斯在相机坐标系下的协方差矩阵 $\pmb{\Sigma}_e$ 被投影到成像平面 $(x_c, y_c)$，通过计算其边缘分布获得 2D 投影参数 $(\pmb{\mu}_{2d}, \pmb{\Sigma}_{2d})$。这一步将 3D 聚焦基元转化为可用于光栅化的 2D 高斯足迹。

**阶段三：加法式光栅化。** 与标准 3DGS 基于 alpha 混合（含遮挡关系）的渲染不同，GaussianPile 采用加法积累策略：在同一像素位置，所有重叠基元的高斯足迹无遮挡地线性叠加，形成最终的切片强度图像。这一设计直接对应切片成像的物理过程——像素强度来源于沿投影线的积分贡献，不存在相互遮挡。

**训练与优化。** 每次迭代随机选取一个虚拟切片（即一个 $z$ 平面）进行渲染，确保覆盖整个体积栈。损失函数采用 L1 损失与 D-SSIM 损失的加权组合 $\mathcal{L} = \mathcal{L}_1 + 0.2 \mathcal{L}_{ssim}$。训练过程中，基于分块聚焦半径和高斯不透明度得分执行自适应稠密化与剪枝策略，动态优化高斯点云的分布。完整的梯度流通过 CUDA 实现从像素损失反向传播至世界坐标系下的高斯参数 $(\pmb{\mu}, \mathbf{s}, \mathbf{q}, \alpha)$。

**压缩与体素化。** 训练完成后，所有高斯基元按莫顿序（Z-order）排序，对位置、不透明度、尺度和四元数分别进行自适应精度量化（位置 14 bit、不透明度 12 bit、尺度 12 bit、四元数 12 bit），再经 delta 编码和 LZMA 熵编码实现高压缩比存储。同时，管线集成可微体素化模块，从世界空间高斯基元聚合构建强度体素，用于 3D 质量评估与可视化。

**输入输出流总结。** 输入为切片式体积图像栈和已知的轴向层间距 $\delta_z$（用于设置 $\sigma_z$）；输出包括任意切片的实时渲染图像、压缩存储的高斯表征，以及可微体素化生成的完整 3D 体积。整个管线在平均约 8 分钟内收敛至高质量结果，渲染帧率超过 100 FPS，同时实现平均 19 倍的压缩比。

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/002_Figure_2.jpg]]
*Figure 2: Focus-aware rendering pipeline of GaussianPile. Given 3D Gaussians and a sensitivity map defining the focal zone, the rendering process consists of three stages: (1) Scan: project Gaussians onto slices at different depths; (2) Axial reparameterization and Opacity modulation: apply axial weighting to attenuate off-focal contributions, yielding Focus Gaussians, while modulating opacity based on distance from the focal plane; (3) Screen-space projection and Additive rasterization: compute 2D marginal distributions and additively accumulate weighted Gaussian footprints to form final rendered images*

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/001_Figure_1.jpg]]
*Figure 1: Panel (a) is the average PSNR-fps-minute comparison (circle radius encodes minutes of training). Our method achieves the highest accuracy at far lower compute cost than prior work. Panels (b–d) are the comparisons of Gaussian rendering models under different imaging physics. (b) All-in-focus (σz → ∞): no axial falloff; primitives contribute regardless of its depth, appropriate for all-in-focus pinhole rendering (e.g., original 3DGS [14]) or line-integral modalities (e.g., X-ray [4]). (c) Zero-thickness (σz → 0): delta-like axial response; primitives contribute only at the exact plane, suitable for dense slicing (e.g., MRI [20]). (d) Finite-thickness Focus Gaussian (ours): finite axial sensi...*

GaussianPile 的核心创新在于将切片成像的物理聚焦模型显式注入高斯泼溅的渲染管线。整体流程（图2）包含三个关键阶段：**聚焦感知 PSF 建模**、**轴向重参数化与不透明度调制**、**屏幕空间投影与加法光栅化**。以下逐一展开关键模块及其数学表述。

### 3D 高斯基元表示

GaussianPile 采用各向异性 3D 高斯函数作为基本表示单元，每个基元在空间中的连续密度分布定义为：

$$p(\mathbf{x}) = \exp\left(-\frac{1}{2}(\mathbf{x} - \pmb{\mu})^{\top} \pmb{\Sigma}^{-1} (\mathbf{x} - \pmb{\mu})\right)$$

其中 $\pmb{\mu} \in \mathbb{R}^3$ 为基元中心位置，$\pmb{\Sigma} = RSS^T R^T$ 为 3D 协方差矩阵，由旋转矩阵 $R$（四元数参数化）和各向异性尺度 $S$ 构成。与标准 3DGS 的关键区别在于：**GaussianPile 完全舍弃球谐函数（SH）系数**，转而通过协方差驱动的强度表示实现自然压缩——每个基元的参数量减少约 40%。

### 聚焦感知 PSF 建模

成像系统的物理聚焦特性是 GaussianPile 区别于标准 3DGS 的根本所在。方法假设成像系统的点扩散函数（PSF）为空间不变 3D 高斯函数：

$$\mathrm{psf}(\mathbf{x}_c) \propto \exp\left(-\frac{1}{2}\left(\frac{x_c^2}{\sigma_x^2} + \frac{y_c^2}{\sigma_y^2} + \frac{z_c^2}{\sigma_z^2}\right)\right)$$

其中 $\mathbf{x}_c = (x_c, y_c, z_c)$ 为相机坐标系下的空间坐标，$\sigma_x$、$\sigma_y$ 为横向分辨率参数，**$\sigma_z$ 为轴向分辨率参数**——这是整个框架的核心控制旋钮，直接表征成像系统的有限焦深（有限切片厚度）。基于此，定义系统的**轴向反向敏感度图**（sensitivity map）为：

$$h(-z_c) = \exp\left(-\frac{z_c^2}{2\sigma_z^2}\right)$$

该敏感度图描述了系统沿高程方向（$z$ 轴）对信号贡献的加权衰减，是后续轴向重参数化和不透明度调制的物理基础。

### 轴向重参数化：生成聚焦高斯

有限切片厚度通过将轴向分辨率项注入逆协方差矩阵来编码。对于相机坐标系下的原始高斯基元 $(\pmb{\mu}_c, \pmb{\Sigma}_c)$，**聚焦高斯（Focus Gaussian）** $(\pmb{\mu}_e, \pmb{\Sigma}_e)$ 由以下轴向重参数化公式给出：

$$\pmb{\Sigma}_e^{-1} = \pmb{\Sigma}_c^{-1} + \frac{\mathbf{e}_3 \mathbf{e}_3^{\top}}{\sigma_z^2}, \quad \pmb{\mu}_e = \pmb{\Sigma}_e \pmb{\Sigma}_c^{-1} \pmb{\mu}_c$$

其中 $\mathbf{e}_3 = (0, 0, 1)^\top$ 为 $z$ 轴单位向量。这一操作的物理含义是：**沿轴向对原始高斯分布施加额外的精度（逆方差）约束**，使得基元的轴向贡献被压缩到以焦平面为中心、宽度由 $\sigma_z$ 决定的有限区域内。当 $\sigma_z \to \infty$ 时退化为全聚焦渲染（对应标准 3DGS 的针孔模型）；当 $\sigma_z \to 0$ 时退化为零厚度切片（对应 MRI 等密集切片模态）。

### 不透明度调制：抑制离焦贡献

为抑制离焦基元对渲染的伪贡献并稳定薄切片的重建，GaussianPile 利用轴向注入引起的**马氏距离变化**来调制不透明度：

$$\mathrm{opacity}_r = \exp\left(-\frac{1}{2}\left(\pmb{\mu}_c^{\top} \pmb{\Sigma}_c^{-1} \pmb{\mu}_c - \pmb{\mu}_e^{\top} \pmb{\Sigma}_e^{-1} \pmb{\mu}_e\right)\right)$$

调制因子 $\mathrm{opacity}_r \in (0, 1]$ 量化了基元中心相对于焦平面的离焦程度：基元越远离焦平面，马氏距离变化越大，调制因子越小，其对渲染的贡献被指数级衰减。这一机制是消除标准 3DGS 中“漂浮伪影”（floating artifacts）的关键——3DGS 的 2D 投影看似合理，但其 3D 体积内部结构严重错乱（图5），正是因为缺少这种物理驱动的离焦抑制。

### 屏幕空间投影

聚焦高斯生成后，需要投影到成像平面 $(x_c, y_c)$ 以进行 2D 渲染。这通过计算聚焦高斯协方差矩阵 $\pmb{\Sigma}_e$ 关于 $(x_c, y_c)$ 平面的**边缘分布**实现：

$$\Sigma_{2d} = \begin{bmatrix} \Sigma_e[0,0] & \Sigma_e[0,1] \\ \Sigma_e[1,0] & \Sigma_e[1,1] \end{bmatrix}, \quad \mu_{2d} = [\pmb{\mu}_e[0], \pmb{\mu}_e[1]]^{\top}$$

其中 $\Sigma_{2d} \in \mathbb{R}^{2\times2}$ 为 2D 投影协方差，$\mu_{2d} \in \mathbb{R}^2$ 为投影中心。渲染时，基元亮度需根据 2D 协方差的行列式进行归一化以保证能量守恒：

$$\tilde{\alpha} = \alpha \cdot \mathrm{opacity}_r / \sqrt{\det(\Sigma_{2d})}$$

### 加法式光栅化

切片成像中，像素强度来源于沿投影线上所有基元贡献的**无遮挡线性叠加**——这与自然场景渲染中的 alpha 混合（沿视线方向的前后遮挡）有本质区别。因此 GaussianPile 采用**加法累积**（additive accumulation）光栅化：

$$I(p) = \sum_{i \in \mathcal{N}(p)} \tilde{\alpha}_i \exp\left(-\frac{1}{2} \mathbf{d}_i^{\top} \pmb{\Sigma}_{2d,i}^{-1} \mathbf{d}_i\right)$$

其中 $\mathcal{N}(p)$ 为投影覆盖像素 $p$ 的所有基元集合，$\mathbf{d}_i = p - \mu_{2d,i}$ 为像素到投影中心的偏移向量。这一加法式光栅化天然匹配切片成像的物理过程（如超声、光片显微），同时避免了遮挡排序的计算开销。

### 可微体素化与损失函数

为评估 3D 体积重建质量，GaussianPile 集成了**可微体素化模块**，从世界空间高斯基元聚合构建强度体素：

$$\sigma(\mathbf{x}) = \sum_{i=1}^{M} g_i^3(\mathbf{x}; \pmb{\mu}_i, \pmb{\Sigma}_i)$$

其中 $g_i^3$ 为原始（未重参数化）的 3D 高斯基元。训练采用 L1 损失与 D-SSIM 损失的加权组合：

$$\mathcal{L} = \mathcal{L}_1 + \lambda \mathcal{L}_{ssim}$$

其中 $\lambda = 0.2$。整个前向与后向传播均通过 CUDA 加速实现，支持从像素梯度到世界坐标系高斯参数（$\pmb{\mu}, \mathbf{s}, \mathbf{q}, \alpha$）的完整可微梯度流。

## 实验与关键发现

### 核心瓶颈与设计动机

标准3DGS的渲染模型将切片成像视为全聚焦针孔投影，未考虑实际成像系统的有限焦深物理。这导致其2D渲染看似合理，但3D体积内部结构严重错乱，产生大量“漂浮伪影”（floating artifacts）。GaussianPile的核心设计动机正是将成像系统的点扩散函数（PSF）显式注入高斯渲染管线，通过轴向重参数化与不透明度调制，使每个高斯基元的轴向贡献与聚焦区精确匹配，从根本上消除2D-3D不一致性。

### 实验设置

**数据集**：实验覆盖五类切片式体积数据——超声（TDSC-ABUS、rDL-LSM）、共聚焦显微（Tribolium胚胎）、光片显微（ISBI12、CREMI）、工业MIR-OCT（CeraMIRScan）以及大规模EM（EPFL CA1）。其中ISBI12和CREMI具有高度各向异性（轴向欠采样达10×/12.5×），用于测试极端条件下的泛化能力。

**基线方法**：对比分为三组——传统压缩标准**HEVC**（CRF=16，侧重极限压缩率）；隐式神经表示方法**INIF**、**CoordNet**、**NeurComp**；以及切片适配的**3DGS**（内部初始化+有限厚度渲染）。所有方法均在NVIDIA A800 GPU上运行，使用官方代码或已发布参数，并按各自论文最佳实践调优。INR方法均训练至收敛，时间报告包含完整训练过程。

**评估指标**：2D切片保真度（PSNR、SSIM）、3D体积保真度（PSNR、SSIM）、内存占用（MB）、压缩比（CR）以及训练时间（分钟）。

### 2D切片重建与压缩性能

Table 1汇总了五个数据集的2D定量对比。GaussianPile在所有超声数据集和多数显微数据集上取得最优2D指标，显著优于INR方法和切片适配3DGS。具体而言：

- **ABUS数据集**：PSNR 33.07 dB，SSIM 0.825，较HEVC（29.67 dB）提升+3.40 dB；训练仅需13分钟，约为INIF（1h24m）的6.5倍加速。
- **rDL-LSM数据集**：PSNR 34.57 dB，SSIM 0.791，较HEVC（29.34 dB）提升+5.23 dB。

Figure 4的定性对比进一步显示，GaussianPile在乳腺纤维腺体组织和肿瘤区域的细节保留上明显优于现有方法，切片重建更清晰、伪影更少。

Table 2报告了压缩性能。GaussianPile在ABUS数据集上实现19×平均压缩比，显著高于INIF（15×）和CoordNet（3×），同时内存占用仅为原始体积的约1/19。这一高压缩比得益于莫顿排序+自适应精度量化（位置14bit、不透明度12bit、尺度12bit、四元数12bit）+LZMA熵编码的联合压缩管线，且消融实验证实量化操作不降低重建质量。

### 3D体积重建质量

Table 3报告了3D体积重建的定量结果。GaussianPile在所有数据集上大幅领先：

- **ABUS**：3D PSNR 33.22 dB，较3DGS（28.49 dB）提升+4.73 dB。
- **rDL-LSM**：3D PSNR 34.47 dB，较3DGS（25.39 dB）提升+9.08 dB，差距尤为显著。

Figure 5直观展示了3DGS与GaussianPile的体积重建差异。从轴向（z轴）视角观察，3DGS重建的体积存在大量漂浮伪影，内部结构严重错乱；而GaussianPile通过聚焦感知渲染管线，有效消除了离焦基元的错误贡献，体积结构清晰且与2D切片保持严格一致。Figure 3展示了优化过程中的体积演化——即使在早期迭代，GaussianPile已能恢复出高保真的3D结构。

### 高度各向异性数据的泛化

Table 5报告了在ISBI12和CREMI两个高度各向异性ssEM数据集上的结果。GaussianPile展现出强鲁棒性：

- **ISBI12**（10×各向异性）：2D PSNR 28.79 dB / SSIM 0.815，3D PSNR 28.98 dB / SSIM 0.881，压缩比8×，训练仅6分钟。较CoordNet在2D PSNR上提升+3.60 dB，3D PSNR提升+4.00 dB，训练加速8.5倍。
- **CREMI**（12.5×各向异性）：2D PSNR 29.50 dB / SSIM 0.831，3D PSNR 28.27 dB / SSIM 0.752，压缩比10×，训练25分钟。较CoordNet在2D PSNR上提升+6.84 dB，3D PSNR提升+7.47 dB，训练加速6.2倍。

Figure 6和Figure 7分别展示了切片级和深度编码体积级的定性对比，GaussianPile在细胞结构边界和纹理细节上均优于基线方法。Figure 10进一步可视化了连续切片的连贯性，验证了方法在极端轴向欠采样下仍能保持结构完整性。

### 消融实验

Table 4汇总了关键消融发现：

**切片厚度（σ_z）**：将切片厚度设为真实层间距（σ_z ≈ δ_z）时，2D和3D指标均达到最优。增大或减小σ_z均导致性能下降，验证了物理聚焦模型的准确性——系统PSF的轴向分辨率与扫描间距匹配是重建质量的关键。

**初始化策略**：随机初始化（随机空间扰动+不透明度扰动）优于结构化网格初始化。前者生成更少的高斯基元、收敛更快、精度更高，因为随机初始化自然引导稠密化过程聚焦于信息丰富的区域，而非均匀覆盖整个体积。

**聚焦前向模型**：对比切片适配的原始3DGS，GaussianPile的聚焦感知管线在3D体积质量上取得质的飞跃（Figure 5）。这证实了物理驱动的轴向重参数化和不透明度调制是消除漂浮伪影、维护3D结构一致性的决定性因素。

**压缩管线**：莫顿量化+熵编码将平均压缩比从3.4×（无量化）提升至19×，且不降低重建质量，验证了高斯参数在Z序排列下的强空间相干性。

### 收敛与效率分析

Figure 8对比了INIF、3DGS和GaussianPile的收敛曲线。GaussianPile展现出更快且更优的收敛特性：在早期迭代即逼近高质量解，最终精度远超INR基线。平均训练时间约8分钟，约为INIF的5倍加速。渲染端，CUDA加速的前向/后向传播实现>100 FPS的实时查询性能。Figure 11在大规模EPFL CA1 EM数据集上验证了方法的可扩展性。

### 失败模式与局限性

尽管GaussianPile在多个数据集上表现优异，其当前设计存在以下局限：

1. **PSF空间不变假设**：模型假设成像系统PSF为空间不变的3D高斯函数，而真实系统常存在随空间变化的像差（如边缘场曲、非均匀照明）。这在高精度光学系统中可能限制重建质量，尤其是在视场边缘区域。

2. **单体积显式优化**：方法针对每个体积独立优化高斯基元，尚未从大规模体积数据中学习通用先验。这无法实现“一次前馈、即时重建”的推理模式，对需要快速处理大量体积的应用场景不够友好。

3. **4D时空数据未验证**：当前工作仅处理静态3D体积，尚未在活细胞时序成像等4D时空数据上验证有效性。动态场景中的时间一致性约束和运动补偿是未探索的方向。

4. **极低信噪比场景**：方法未集成语义分割或物理先验（如细胞形态约束），在严重欠采样或噪声数据中的重建鲁棒性有待验证。

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/005_Table_1.jpg]]
*Table 1: 2D quantitative comparison of GaussianPile and other methods*

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/007_Table_3.jpg]]
*Table 3: 3D quantitative results of baselines and our method*

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/006_Table_2.jpg]]
*Table 2: Compression comparison of GaussianPile and other methods. Memory size is reported in megabytes (MB)*

![[assets/figures/papers/paper_list_l2496_https_arxiv_org_abs_2603_20611/figures/009_Table_4.jpg]]
*Table 4: Ablation results with our choices in bold*

## 定位与知识库关联

### 1. 与基线方法的谱系关系

GaussianPile 处于**切片式体积重建**与**可微渲染压缩**的交汇点，其直接比较对象覆盖三类代表性基线：

**传统压缩标准**
- **HEVC**（CRF=16）作为视频编码压缩的参考，在极限压缩率下 2D 保真度损失显著（例如 ABUS 上仅 29.67 dB PSNR），且无法直接输出 3D 体积，仅作为存储效率的参照点。

**隐式神经表示（INR）方法**
- **INIF**、**CoordNet**、**NeurComp** 等 INR 方法通过神经网络隐式编码体积场，在压缩比上具备竞争力（INIF 可达 15×），但存在训练慢（ABUS 上 INIF 需 1h24m）、渲染需逐点查询导致低帧率的本质瓶颈。GaussianPile 以显式基元替代隐式场，将训练加速约 5–11 倍（平均 8 分钟收敛），同时实现 19× 的平均压缩比，在 2D/3D 指标上全面超越 INR 基线（见表 1、表 3、表 5）。

**3DGS 切片适配版本**
- 原始 **3DGS**（Kerbl et al., SIGGRAPH 2023）设计用于多视角自然图像合成，其渲染模型假设全聚焦针孔相机（$\sigma_z \to \infty$），未建模切片成像的有限焦深物理。文中构建的 **slice-adapted 3DGS** 通过内部初始化与有限厚度渲染进行适配，但 2D 渲染虽看似合理，3D 体积重建却严重劣化——在 rDL-LSM 上 3D PSNR 仅 25.39 dB，而 GaussianPile 达 34.47 dB（+9.08 dB），漂浮伪影被显著消除（图 5）。这揭示了**物理建模注入渲染管线**的关键性：仅靠数据驱动适配无法弥补成像物理的缺失。

### 2. 核心创新在知识库中的定位

GaussianPile 的方法论贡献可定位于以下知识谱系：

| 维度 | 上游基础 | GaussianPile 的增量 |
|------|----------|---------------------|
| **基元表示** | 3DGS 的各向异性高斯基元 | 舍弃球谐函数（约 40% 参数缩减），以协方差驱动强度表示，适配切片成像的加法光栅化 |
| **渲染物理** | 计算机视觉中的薄透镜模型 | 将成像系统 PSF 显式建模为空间不变 3D 高斯，通过轴向重参数化（协方差注入 $\sigma_z^{-2}$）与不透明度调制（马氏距离衰减）编码有限焦深 |
| **光栅化策略** | 3DGS 的 alpha 混合（含遮挡排序） | 切换为加法式光栅化，符合切片成像中无遮挡叠加的物理过程 |
| **压缩范式** | 神经压缩的量化+熵编码 | 莫顿排序 + 自适应精度量化（位置 14bit / 不透明度 12bit / 尺度 12bit / 四元数 12bit）+ LZMA 熵编码，将压缩比从基础 3.4× 提升至 19× |
| **可微体积化** | NeRF 的体渲染密度聚合 | 从世界空间高斯基元直接构建可微体素，实现 3D 评估与可视化的一体化 |

### 3. 适用边界与局限

**已验证的适用域**
- 医学超声体积（TDSC-ABUS）
- 光片显微数据（rDL-LSM）
- 共聚焦显微数据（Tribolium 胚胎）
- 高度各向异性 ssEM 数据（ISBI12、CREMI，各向异性比 10–12.5×）
- 工业 MIR-OCT 数据（CeraMIRScan）
- 大规模 EM 数据（EPFL CA1）

**方法学局限**
1. **PSF 空间不变假设**：当前模型假设成像系统 PSF 为空间不变的 3D 高斯函数，而真实光学系统常存在随视场变化的像差（如边缘散焦、非对称畸变），这可能限制高精度光学系统中的重建质量。
2. **逐体积显式优化范式**：方法针对每个体积独立优化高斯基元，尚未从大规模体积数据中学习通用先验，无法实现“一次前馈、即时重建”的推理模式，限制了在高吞吐量场景中的部署效率。
3. **未探索的模态与场景**：尚未在 4D 时空数据（如活细胞时序成像）上验证有效性，也未集成语义分割或物理先验（如细胞形态约束）以应对极低信噪比场景。

### 4. 开放问题与未来方向

1. **可学习的空间变化 PSF**：能否引入参数化的空间变化 PSF 模型（例如以位置编码为条件的 $\sigma_z(\mathbf{x})$），以适应复杂光学系统的非均匀聚焦特性？
2. **语义与物理先验的融合**：能否融入语义分割或物理先验（如细胞膜连续性约束）来提升严重欠采样或噪声数据的重建鲁棒性？
3. **通用高斯先验学习**：能否从大规模切片式体积数据中学习通用高斯先验（类似 3D 基础模型），实现单步前馈重建与压缩？
4. **4D 时空扩展**：该方法如何扩展到 4D 时空数据（例如活细胞连续成像），以同时实现压缩与动态可视化？这需要处理时间维度的基元运动建模与跨帧一致性约束。
5. **与神经场方法的深度融合**：GaussianPile 的显式基元与 INR 的隐式连续性各具优势，是否存在混合表示（例如以高斯基元编码低频结构、以小型 MLP 编码高频细节）的 Pareto 最优方案？

## 原文 PDF

![[paperPDFs/CVPR_2026/GaussianPile_A_Unified_Sparse_Gaussian_Splatting_Framework_for_Slice_based_Volumetric_Reconstruction.pdf]]
