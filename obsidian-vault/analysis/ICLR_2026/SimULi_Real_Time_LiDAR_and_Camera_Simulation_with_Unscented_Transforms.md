---
title: "SimULi: Real-Time LiDAR and Camera Simulation with Unscented Transforms"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SimULi_Real_Time_LiDAR_and_Camera_Simulation_with_Unscented_Transforms.pdf
code_link: null
project_link: https://research.nvidia.com/labs/sil/projects/simuli/
aliases:
- SimULi
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "因子化3D高斯表示将相机与激光雷达信息编码到独立高斯集，通过最近邻锚定损失耦合；基于直方图均衡的自动激光雷达瓦片策略与光线剔除加速渲染。"
primary_logic: "分离传感器表示允许独立优化以适应各模态特性；锚定损失利用激光雷达几何约束提升相机新视角合成；自动瓦片策略无需手工启发即可适应任意旋转激光雷达模型。"
claims:
- "SimULi renders 10-20× faster than ray tracing and 1.5-10× faster than prior rasterization-based work."
- "SimULi reduces mean camera and depth error by up to 40% compared to existing methods."
- "SimULi achieves 30.15 PSNR on Waymo Interp, outperforming SplatAD by 2.33 dB."
- "Automated tiling strategy generalizes to arbitrary spinning LiDAR models without handcrafted heuristics."
---

# SimULi: Real-Time LiDAR and Camera Simulation with Unscented Transforms

> [!tip] 核心洞察
> 分离传感器表示允许独立优化以适应各模态特性；锚定损失利用激光雷达几何约束提升相机新视角合成；自动瓦片策略无需手工启发即可适应任意旋转激光雷达模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SimULi：基于无迹变换的实时激光雷达与相机仿真 |
| 英文题名 | SimULi: Real-Time LiDAR and Camera Simulation with Unscented Transforms |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.12901) · [Project](https://research.nvidia.com/labs/sil/projects/simuli) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SimULi |
| Dataset | Waymo Interp, Waymo Dynamic, PandaSet Reconstruction |

> [!tip] 效果简介
> - Waymo Interp 上，PSNR 为 30.15，对比 27.82 (SplatAD)，变化 +2.33。
> - Waymo Dynamic 上，PSNR 为 32.35，对比 30.60 (SplatAD)，变化 +1.75。
> - Waymo Interp 上，MP/s (camera rendering speed) 为 156.90，对比 49.98 (SplatAD)，变化 +106.92。

## 概要

自动驾驶仿真面临一个核心瓶颈：现有方法无法在实时性约束下同时高质量渲染任意相机模型（如鱼眼镜头）与激光雷达数据。由于跨传感器数据存在天然不一致性，将相机和激光雷达信息编码到同一表示中会迫使模型牺牲某一模态的精度——要么相机质量下降，要么激光雷达几何失真。

SimULi 针对这一瓶颈提出了一个因果性解决方案：**因子化3D高斯表示**。其核心洞察是分离传感器表示，将相机与激光雷达信息分别编码到独立的高斯集 $G_c$ 和 $G_l$ 中，并通过最近邻锚定损失耦合两者。这一设计允许各模态独立优化以适应自身特性，同时利用激光雷达的几何约束提升相机新视角合成质量。配合基于直方图均衡的自动激光雷达瓦片策略与光线剔除加速机制，SimULi 实现了实时渲染任意相机模型和旋转激光雷达的能力。

实验表明，SimULi 在 Waymo Interp 上达到 30.15 PSNR，比 **SplatAD**（Hess et al., CVPR 2025）高出 2.33 dB；相机渲染速度达 156.90 MP/s，是 SplatAD 的 3 倍以上。在 PandaSet 重建任务中，SimULi 同样以 29.76 PSNR 优于 SplatAD 的 28.58 PSNR，且渲染速度提升 60%。整体而言，SimULi 比光线追踪方法快 10–20 倍，比先前基于光栅化的工作快 1.5–10 倍，同时将平均相机和深度误差降低最多 40%。

该方法在方法谱系中处于 3D 高斯溅射与多传感器联合仿真的交汇点。与 **SplatAD**（统一高斯表示，仅支持针孔相机）和 **NeuRAD**（Tonderski et al., CVPR 2024，基于 NeRF 的联合表示）不同，SimULi 通过因子化表示解耦传感器特性；与 **3DGUT**（Wu et al., CVPR 2025，支持畸变相机但无激光雷达）相比，SimULi 扩展了激光雷达渲染能力并引入自动瓦片策略。其自动瓦片策略无需手工启发即可适应任意旋转激光雷达模型，这一能力在先前的 SplatAD 中需要针对每种传感器单独设计。

自动驾驶系统的闭环仿真与感知模型训练，高度依赖对多模态传感器数据的高保真重建与实时渲染。激光雷达（LiDAR）与相机是当前自动驾驶感知栈的两大核心传感器，前者提供精确的三维几何信息，后者捕获丰富的视觉外观。然而，现有方法在同时处理这两种模态时，始终面临一个根本性瓶颈：**无法在实时渲染的前提下，同时支持任意相机模型（如鱼眼镜头、卷帘快门）与激光雷达数据的高质量合成**。这一瓶颈迫使现有方案必须在某一模态的精度上做出妥协。

具体而言，当前主流的传感器仿真方法可大致分为两类。第一类是基于神经辐射场（NeRF）的方法，如 **UniSim**（Yang et al., CVPR 2023）和 **NeuRAD**（Tonderski et al., CVPR 2024）。这类方法能够联合建模相机与激光雷达数据，但其体积渲染机制依赖逐射线采样，渲染速度极慢，难以满足实时仿真的需求。第二类是基于3D高斯泼溅（3DGS）的方法，如 **SplatAD**（Hess et al., CVPR 2025），通过光栅化渲染大幅提升了速度。然而，SplatAD 将相机与激光雷达信息编码到同一组高斯粒子中，并仅支持针孔相机模型，无法处理鱼眼镜头和卷帘快门等复杂相机效应。此外，其激光雷达瓦片策略依赖手工启发式规则，无法泛化到不同型号的旋转激光雷达传感器。

更深层的问题在于**跨传感器数据的不一致性**。激光雷达点云在反射表面和薄结构附近常出现“膨胀”伪影，而相机图像在这些区域则保持清晰。当两种模态被强制编码到同一组高斯粒子中时，优化过程会迫使表示在相机质量和激光雷达精度之间做出取舍——要么牺牲激光雷达的几何保真度以换取更好的相机渲染，要么反之。这一“跷跷板”效应是统一表示方法的固有缺陷。

在渲染效率方面，激光雷达的测量模式具有高度不规则性：不同型号的传感器（如Waymo使用的64线激光雷达与PandaSet使用的旋转激光雷达）在仰角分布上差异显著。若采用等距瓦片进行光栅化，大量瓦片将不包含任何有效射线，造成严重的计算浪费。现有方法需要为每种传感器单独设计瓦片划分策略，缺乏通用性。

在上述背景下，**SimULi** 提出了一个统一的实时传感器仿真框架，其核心动机是通过**因子化表示**打破跨传感器不一致性带来的精度瓶颈，并通过**自动化瓦片策略**与**无迹变换相机渲染**实现对任意传感器配置的实时支持。该方法不追求在单一表示中融合两种模态，而是让相机与激光雷达各自拥有独立的高斯粒子集，再通过几何锚定损失进行耦合，从而在保持实时渲染的前提下，同时提升两种模态的合成质量。

## 核心方法与创新机理

SimULi 的核心创新在于通过**因子化表示**与**渲染效率优化**两个维度，系统性地解决了现有联合相机-激光雷达仿真方法中模态精度互斥与实时性不足的双重瓶颈。

### 1. 因子化 3D 高斯表示与锚定损失

现有方法（如 **SplatAD** (Hess et al., CVPR 2025) 和 **NeuRAD** (Tonderski et al., CVPR 2024)）将相机与激光雷达信息编码到**同一组 3D 高斯**中，通过激光雷达监督的深度损失进行约束。然而，跨传感器数据并非完全一致——激光雷达在反射表面和薄结构附近存在“膨胀”伪影（Figure 12），这迫使统一表示在相机质量与激光雷达质量之间做出妥协（Figure 4）。

SimULi 将表示**因子化**为两个独立的高斯集合：
- **相机高斯集 $G_c$**：存储视角相关颜色与体积渲染所需属性
- **激光雷达高斯集 $G_l$**：存储视角相关强度与射线丢失概率，并施加熵损失以鼓励二值化透明度

两个集合通过 **K-近邻锚定损失**（Equation 5）耦合：

$$\mathcal{L}_{anchor} = \frac{1}{n} \sum_{i \in G_c}^{n} \| \mu_i - NN(\mu_i, G_l) \|_2$$

该损失将相机高斯均值拉向最近激光雷达高斯均值，利用激光雷达的几何约束提升相机新视角合成质量，同时允许各模态独立优化以适应其特性。消融实验（Table 5）证实，因子化表示配合锚定损失在相机 PSNR 和激光雷达 Chamfer Distance 上均优于统一表示。

### 2. 任意相机模型支持：无迹变换渲染

传统 3DGS 及其变体仅支持针孔相机模型。SimULi 继承并扩展了 **3DGUT**（Wu et al., CVPR 2025）的渲染管线，通过**无迹变换**（Unscented Transform）实现可微体积渲染，原生支持鱼眼镜头、滚动快门等复杂相机模型（Figure 11）。在 Waymo Dynamic 场景中，SimULi 的滚动快门处理策略能够准确建模快速运动，而 SplatAD 则产生明显伪影（Figure 6, 第三行）。

### 3. 自动激光雷达瓦片策略与光线剔除

激光雷达的测量模式在球面投影下高度不规则（Figure 3, 左）。SplatAD 需要为每种激光雷达传感器手工设计瓦片启发式规则，而 SimULi 提出了基于**直方图均衡**的自动化瓦片生成策略（Procedure 1）：计算仰角标准化 CDF，在 CDF 穿越整数边界处设置瓦片边界，使每瓦片内光束数差异不超过 8 条。该策略可零修改地泛化到任意旋转激光雷达模型（Figure 9）。

在此基础上，SimULi 引入**基于光线剔除**的加速机制：利用积分面积表（summed-area table）进行常数时间的高斯粒子过滤。性能剖析（Table 7）显示，该策略在投影阶段仅引入 2% 开销，但使排序和渲染内核加速 8-9%。

### 4. 关键性能跃迁

上述创新的综合效果体现在定量结果中：
- **渲染速度**：相机渲染达 156.90 MP/s（SplatAD 的 3.1 倍），激光雷达渲染同样领先（Table 1）
- **重建质量**：Waymo Interp 上 PSNR 30.15 dB，超越 SplatAD 2.33 dB（Table 1）；PandaSet 上 PSNR 29.76 dB，超越 SplatAD 1.18 dB（Table 3）
- **参数效率**：SimULi 全局高斯数量上限为 4M，低于 SplatAD 的 5M，却同时实现了更快渲染与更高精度

SimULi 的整体流程围绕一个核心设计展开：**将相机与激光雷达信息编码到两个独立的 3D 高斯粒子集中**，通过最近邻锚定损失进行耦合，从而在统一的动态场景图下实现跨模态的实时渲染与联合优化。

### 场景图分解与双模态表示

SimULi 将场景建模为一个动态场景图，将背景和每个动态参与者分别参数化。每个场景节点维护两组独立的半透明 3D 高斯粒子（Figure 2）：

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. We model the scene as a dynamic graph (Ost et al., 2021) and parameterize the background and each actor with camera and LiDAR 3D Gaussians (left). We render camera views similar to 3DGUT (Wu et al., 2025b) and derive an automated tiling strategy and raybased culling to efficiently render LiDAR (middle). We sample an image and LiDAR scan at each training step to optimize our representation (right). To improve camera novel view synthesis with LiDAR-supervised geometry, we anchor camera Gaussians near surfaces via nearest-neighbor loss*

- **相机高斯集** $G_c$：存储视角相关的颜色（通过球谐函数 $\mathbf{SH}_i^c(\mathbf{d})$ 编码）、不透明度 $\sigma_i$ 和 3D 协方差 $\Sigma_i$，用于相机视图的体积渲染。
- **激光雷达高斯集** $G_l$：存储视角相关的强度与射线丢失概率（通过 $\mathbf{SH}_i^l(\mathbf{d})$ 编码），并施加熵正则化以鼓励二值不透明度，适配激光雷达的稀疏测量特性。

这种因子化表示的设计动机在于：跨传感器数据并非完全一致——激光雷达在反射表面附近存在“膨胀”伪影，而相机则对薄结构更敏感。将两者强行编码到同一表示中会迫使模型在某一模态上妥协（Figure 4）。通过分离表示，SimULi 允许每个模态独立优化其特性，同时通过锚定损失利用激光雷达的几何约束来提升相机新视角合成的质量。

### 渲染管线

SimULi 的渲染分为两条并行路径，在每次训练迭代中同时采样一帧图像和一次激光雷达扫描：

**相机渲染**继承并扩展了 **3DGUT**（Wu et al., CVPR 2025）的框架。对于每条相机射线 $\mathbf{r} = (\mathbf{o}, \mathbf{d})$，在 $G_c$ 中沿射线方向对高斯粒子进行体积渲染，得到前景颜色 $\mathbf{c_f}$ 和累积不透明度 $\omega$：

$$\mathbf { c } _ { \mathbf { f } } ( \mathbf { o } , \mathbf { d } ) = \sum _ { i \in G _ { c } } \mathbf { S } \mathbf { H } _ { i } ^ { \mathbf { c } } ( \mathbf { d } ) \alpha _ { i } T _ { i } , \quad \omega ( \mathbf { o } , \mathbf { d } ) = \sum _ { i \in G _ { c } } \alpha _ { i } T _ { i }$$

其中 $\alpha_i = \sigma_i \rho_i(\mathbf{o} + \tau\mathbf{d})$ 是粒子响应函数与不透明度的乘积，$T_i = \prod_{j=1}^{i-1} 1 - \alpha_j$ 为累积透射率。最终颜色通过可学习的仿射变换 $\mathcal{A}$ 与背景环境贴图 $\mathbf{c_b}$ 进行 alpha 合成：

$$\mathbf { c ( 0 , d ) } = \mathcal { A } ( \omega ( \mathbf { 0 } , \mathbf { d } ) \mathbf { c } _ { \mathrm { f } } ( \mathbf { 0 } , \mathbf { d } ) + ( 1 - \omega ( \mathbf { 0 } , \mathbf { d } ) ) \mathbf { c } _ { \mathrm { b } } ( \mathbf { d } ) )$$

关键创新在于 SimULi 通过**无迹变换（Unscented Transform）**支持任意相机模型，包括鱼眼镜头和卷帘快门。对于卷帘快门，渲染公式将传感器运动纳入投影函数，并使用每条射线的精确时间戳在 3D 中评估粒子响应函数，从而在高粒度上建模时间依赖效应（Figure 11）。这一能力是 **SplatAD**（Hess et al., CVPR 2025）等仅支持针孔相机的方法所不具备的。

**激光雷达渲染**则面临不同的挑战：激光雷达的测量模式在球面坐标上高度不规则，直接使用等间距瓦片渲染效率极低。SimULi 提出了两个关键组件来解决这一问题：

1. **自动瓦片策略**：将 $G_l$ 中的每个高斯粒子通过无迹变换投影为 7 个 sigma 点，转换到传感器坐标系下的球面坐标：

   $$\phi = \arctan 2 ( y , x ) , \quad \omega = \arcsin ( z / r ) , \quad r = \sqrt { x ^ { 2 } + y ^ { 2 } + z ^ { 2 } }$$

   然后计算仰角 $\omega$ 的归一化累积分布函数（CDF），在 CDF 值跨越整数边界处设置仰角瓦片边界，再为每个仰角瓦片计算一个方位角瓦片数，使得每瓦片内的光束数差异不超过 8 个样本（Figure 3）。该策略无需手工启发式规则，可泛化到任意旋转激光雷达模型（Figure 9）。

2. **基于射线的剔除**：利用求和面积表（summed-area table）对投影后的粒子进行常数时间过滤，剔除与当前激光射线无关的高斯粒子，将排序和渲染内核的耗时降低 8–9%，而投影阶段仅增加约 2% 的常数时间开销（Table 7）。

激光雷达特征渲染与相机类似，通过体积渲染输出强度和射线丢失概率：

$$\boldsymbol { \zeta } ( \mathbf { o } , \mathbf { d } ) = \sum _ { i \in G _ { l } } \mathbf { S } \mathbf { H } _ { i } ^ { 1 } ( \mathbf { d } ) \alpha _ { i } T _ { i }$$

此外，SimULi 引入了一个 3D 抗锯齿滤波器来建模激光雷达光束发散效应，但**刻意省略了先前工作中的不透明度补偿**——因为该补偿会导致前景与背景物体的混合，损害深度质量（Figure 10）。

### 优化目标

SimULi 联合优化 $G_c$、$G_l$、双边网格 $\mathcal{A}$ 和环境贴图。总损失函数由三部分组成：

**重建损失** $\mathcal{L}_{recon}$ 分别对两个模态施加监督：

$$\mathcal { L } _ { r e c o n } = \underbrace { \left( \lambda _ { p h o t o } \mathcal { L } _ { p h o t o } + \lambda _ { S S I M } \mathcal { L } _ { S S I M } \right) } _ { \mathrm { c a m e r a l o s s e s } } + \underbrace { \left( \lambda _ { d i s t } \mathcal { L } _ { d i s t } + \lambda _ { i n t } \mathcal { L } _ { i n t } + \lambda _ { r d } \mathcal { L } _ { r d } \right) } _ { \mathrm { L i D A R l o s s e s } }$$

**锚定损失** $\mathcal{L}_{anchor}$ 是连接两个高斯集的关键机制：对 $G_c$ 中的每个高斯粒子，计算其均值 $\mu_i$ 到 $G_l$ 中最近邻均值的 L2 距离（K=50）：

$$\mathcal { L } _ { a n c h o r } = \frac { 1 } { n } \sum _ { i \in G _ { c } } ^ { n } \| \mu _ { i } - N N ( \mu _ { i } , G _ { l } ) \| _ { 2 }$$

该损失以极小的权重（$\lambda_{anchor} = 0.01$）将相机高斯“锚定”到激光雷达约束的场景几何表面附近，在不牺牲激光雷达质量的前提下显著提升相机新视角合成精度。

**正则化损失** $\mathcal{L}_{reg}$ 包含熵损失（鼓励 $G_l$ 的二值不透明度）、总变分损失、身份漂移惩罚，以及尺度和不透明度的 L1 正则项：

$$\mathcal { L } _ { \mathrm { r e g } } : = \mathcal { L } _ { \mathrm { e n t r o p y } } + \mathcal { L } _ { \mathrm { T V } } + \lambda _ { \mathrm { d r i f t } } \mathcal { L } _ { \mathrm { d r i f t } } + \lambda _ { \Sigma } \sum _ { i j } \sqrt { \mathrm { e i g } _ { j } ( \Sigma _ { i } ) } + \lambda _ { \sigma } \sum _ { i } \sigma _ { i }$$

### 模块关系总结

整个框架的模块间关系可概括为：场景图分解为表示提供可控性基础 → 因子化高斯集独立编码各模态信息 → 相机渲染器（基于无迹变换）和激光雷达渲染器（自动瓦片+射线剔除）并行工作 → 锚定损失实现跨模态几何耦合 → 多任务重建损失与正则化项联合驱动优化。这一设计使得 SimULi 在使用比 SplatAD 更少的高斯粒子（4M vs 5M）的条件下，实现了 1.5–20 倍的渲染加速和高达 40% 的误差降低。

### 1. 场景表示：因子化3D高斯

SimULi的核心设计是将相机与激光雷达的信息**解耦到两个独立的3D高斯粒子集**中，而非像以往工作（如**SplatAD**, Hess et al., CVPR 2025）那样使用单一统一的高斯集。

- **相机高斯集 $G_c$**：存储视角相关的颜色（通过球谐函数 $\mathbf{SH}_i^c(\mathbf{d})$ 编码）和体积渲染所需的不透明度 $\alpha_i$。
- **激光雷达高斯集 $G_l$**：存储视角相关的强度（通过球谐函数 $\mathbf{SH}_i^l(\mathbf{d})$ 编码）和射线丢失概率，并施加二值不透明度偏置以适配激光雷达的稀疏特性。

为支持动态场景的操控性，SimULi采用场景图分解策略，将 $G_c$ 和 $G_l$ 中的每个粒子分配给动态目标或静态背景。

### 2. 相机渲染：无迹变换体积渲染

相机渲染基于3DGUT（Wu et al., CVPR 2025）的体积渲染管线，利用无迹变换（Unscented Transform）支持任意相机模型（包括鱼眼镜头和卷帘快门）。

**前景颜色与不透明度渲染**（公式1）：

$$\mathbf{c_f}(\mathbf{o}, \mathbf{d}) = \sum_{i \in G_c} \mathbf{SH}_i^c(\mathbf{d}) \alpha_i T_i, \quad \omega(\mathbf{o}, \mathbf{d}) = \sum_{i \in G_c} \alpha_i T_i$$

其中：
- $\mathbf{o}$ 为射线原点，$\mathbf{d}$ 为射线方向
- $\alpha_i = \sigma_i \rho_i(\mathbf{o} + \tau\mathbf{d})$ 为高斯粒子在采样点处的响应
- $T_i = \prod_{j=1}^{i-1} (1 - \alpha_j)$ 为累积透射率
- $\omega(\mathbf{o}, \mathbf{d})$ 为总不透明度

**最终颜色预测**（公式2）：

$$\mathbf{c}(\mathbf{o}, \mathbf{d}) = \mathcal{A}\big(\omega(\mathbf{o}, \mathbf{d}) \mathbf{c_f}(\mathbf{o}, \mathbf{d}) + (1 - \omega(\mathbf{o}, \mathbf{d})) \mathbf{c_b}(\mathbf{d})\big)$$

其中 $\mathcal{A}$ 为可学习的仿射色彩变换，用于建模光照变化；$\mathbf{c_b}(\mathbf{d})$ 为环境贴图提供的背景颜色。

### 3. 激光雷达渲染：自动瓦片与光线剔除

激光雷达渲染是SimULi的另一核心模块，包含三个关键设计。

**球坐标转换**（公式3）：

$$\phi = \arctan2(y, x), \quad \omega = \arcsin(z / r), \quad r = \sqrt{x^2 + y^2 + z^2}$$

将传感器坐标系下的3D点转换为方位角 $\phi$、仰角 $\omega$ 和距离 $r$。SimULi对每个激光雷达高斯投影其7个Sigma点（通过无迹变换），获得2D方位-仰角网格上的锥形区域用于后续瓦片分配和剔除。

**自动瓦片策略**：传统方法（如SplatAD）需为每种激光雷达传感器手工设计启发式瓦片划分。SimULi提出基于直方图均衡的自动化策略：计算仰角分布的归一化CDF，在CDF跨越整数边界处设置瓦片边界，再根据用户指定的最大点数约束 $M$ 确定方位瓦片数，使得每瓦片光束数差异不超过8。该策略无需手工调整即可适配任意旋转激光雷达模型（见Figure 9）。

**光线剔除**：利用积分面积表（summed-area table）实现常数时间的光线感知粒子过滤，将排序和渲染核函数加速8-9%，而投影开销仅增加约2%（见Table 7）。

**激光雷达特征渲染**：

$$\boldsymbol{\zeta}(\mathbf{o}, \mathbf{d}) = \sum_{i \in G_l} \mathbf{SH}_i^l(\mathbf{d}) \alpha_i T_i$$

输出强度与射线丢失概率。

### 4. 优化目标

**总重建损失**（公式4）：

$$\mathcal{L}_{recon} = \underbrace{(\lambda_{photo}\mathcal{L}_{photo} + \lambda_{SSIM}\mathcal{L}_{SSIM})}_{camera\ losses} + \underbrace{(\lambda_{dist}\mathcal{L}_{dist} + \lambda_{int}\mathcal{L}_{int} + \lambda_{rd}\mathcal{L}_{rd})}_{LiDAR\ losses}$$

其中相机损失包括光度损失和SSIM损失，激光雷达损失包括距离损失、强度损失和射线丢失损失。

**最近邻锚定损失**（公式5）：

$$\mathcal{L}_{anchor} = \frac{1}{n} \sum_{i \in G_c}^{n} \|\mu_i - NN(\mu_i, G_l)\|_2$$

将每个相机高斯的均值 $\mu_i$ 拉向其 $K=50$ 个最近邻激光雷达高斯的均值。该损失利用激光雷达的精确几何约束来改善相机新视角合成质量，是因子化表示的关键耦合机制。

**抗锯齿滤波器**（公式6）：

$$\hat{\rho}_{\perp}(\mathbf{x}) = \sqrt{\frac{|\Sigma_{\perp}|}{|\hat{\Sigma}_{\perp}|}} \exp\left(-\frac{1}{2}(\mathbf{x} - \mu)^{\top} \hat{\Sigma}^{-1} (\mathbf{x} - \mu)\right)$$

用于建模激光雷达光束发散效应的3D平滑滤波器。SimULi**刻意省略了先前工作中的不透明度补偿**，以避免前景-背景混合导致的深度质量退化（见Figure 10）。

**正则化损失**（公式7）：

$$\mathcal{L}_{reg} := \mathcal{L}_{entropy} + \mathcal{L}_{TV} + \lambda_{drift}\mathcal{L}_{drift} + \lambda_{\Sigma} \sum_{ij} \sqrt{\mathrm{eig}_j(\Sigma_i)} + \lambda_{\sigma} \sum_i \sigma_i$$

包含熵正则（鼓励激光雷达高斯的二值不透明度）、总变分正则、身份漂移惩罚、尺度正则和透明度正则。

## 实验与关键发现

### 核心实验设计

SimULi 在三个主流自动驾驶仿真基准上进行了评估：**Waymo Interp**（静态场景插值）、**Waymo Dynamic**（动态场景重建）和 **PandaSet**（重建与新视角合成）。对比基线覆盖了联合相机-激光雷达的光栅化方法 **SplatAD**（Hess et al., CVPR 2025）、基于 NeRF 的联合方法 **NeuRAD**（Tonderski et al., CVPR 2024）与 **UniSim**（Yang et al., CVPR 2023）、纯激光雷达光线追踪方法 **LiDAR-RT**（Zhou et al., CVPR 2025），以及支持畸变相机的纯视觉方法 **3DGUT**（Wu et al., CVPR 2025）。所有速度与质量对比均在相同初始化条件和 A40 GPU 硬件下进行，SimULi 使用全局 4M 高斯上限，低于 SplatAD 的 5M，但渲染速度更快、精度更高。

### 主要定量结果

**Waymo Interp（Table 1）**：SimULi 在相机 PSNR 上达到 30.15 dB，较 SplatAD（27.82 dB）提升 +2.33 dB，且优于所有基线超过 2 dB。相机渲染速度达 156.90 MP/s，是 SplatAD（49.98 MP/s）的 3.1 倍。深度重建质量同样优于纯激光雷达方法 LiDAR-RT。

**Waymo Dynamic（Table 2）**：SimULi 取得 PSNR 32.35 dB、SSIM 0.922、MedL2 0.002、CD 0.148，相机渲染速度 179.45 MP/s，在所有相机和激光雷达指标上均为最优或次优。

**PandaSet 重建（Table 3）**：PSNR 达 29.76 dB，较 SplatAD（28.58 dB）提升 +1.18 dB，相机渲染速度提升 60%。

**PandaSet 新视角合成（Table 4）**：SimULi 在 PSNR 上最优，且在所有激光雷达指标上超越 SplatAD，同时保持最快渲染速度。

### 消融实验

**因子化表示与锚定损失（Table 5）**：将统一的 3D 高斯表示替换为因子化的相机高斯集 $G_c$ 和激光雷达高斯集 $G_l$，并引入最近邻锚定损失，同时提升了相机 PSNR 和激光雷达 Chamfer Distance。这验证了核心洞察：分离表示允许各模态独立优化，而锚定损失利用激光雷达几何约束改善相机新视角合成。

**激光雷达瓦片策略（Table 6）**：在 $M=32$、$N_\phi=16$ 的参数设置下，激光雷达渲染吞吐量达到最高的 15.75 MR/s。自动直方图均衡策略无需手工启发即可适应任意旋转激光雷达模型（Figure 9）。

**光线剔除（Table 7）**：基于射线的高斯过滤通过总和面积表实现常数时间过滤，投影阶段仅增加约 2% 开销，但排序和渲染内核分别加速 8-9%。

**光束发散抗锯齿（Figure 10）**：关键发现是必须省略透明度补偿——先前工作（Steiner et al., 2025; Yu et al., 2024）的补偿机制会导致前景与背景物体混合，破坏深度质量。SimULi 的 3D 平滑滤波器仅作用于协方差，不缩放透明度因子 $\alpha_i$，有效消除“膨胀”伪影。

**激光雷达投影策略（Table 8, Figure 13）**：SimULi 使用无迹变换投影每个高斯的 7 个 sigma 点，而非蒙特卡洛采样的 200 个点，结果近乎一致，但计算成本大幅降低。

### 定性分析

**静态新视角合成（Figure 5）**：将激光雷达投影为稀疏深度图（如 3DGUT 的做法）会导致杆状物等细结构渲染不准确；SimULi 直接渲染激光雷达避免了此问题。双边网格有效抑制了漂浮物。SplatAD 的 CNN 无法正确恢复标志牌字母和车内细节，而 SimULi 的简化管线表现更优。

**动态场景（Figure 6）**：使用 CNN 上采样或视角依赖的方法（UniSim、NeuRAD、SplatAD）普遍存在模糊和文字错误问题。SimULi 的滚动快门策略能处理快速运动场景，而 SplatAD 无法应对。背景细节和反射效果也优于其他方法。

**激光雷达噪声处理（Figure 12）**：激光雷达在反射表面和薄结构附近易产生“膨胀”伪影。因子化表示和锚定损失能准确捕获这些效应，同时不损害相机质量。

### 失败模式与局限性

1. **非刚性物体建模缺失**：SimULi 目前不支持非刚性形变物体（如行人姿态变化），但现有解决方案可直接集成。
2. **大视角偏差下的退化**：当渲染视角远离训练位姿时，新视图合成质量下降；生成先验（如扩散模型）可能缓解此问题。
3. **锚定损失计算开销**：K 最近邻计算增加约 14 分钟训练时间；减小 K 值或定制 CUDA 内核可缓解。
4. **非旋转激光雷达扩展**：自动瓦片策略理论上可推广至方位和仰角两维，但尚未实现。


![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/009_Table_2.jpg]]
*Table 2: Waymo Dynamic. As with static reconstruction (Table 1), we render the fastest and report best or next-best results across every camera and LiDAR metric. we enforce smoothness across our affine color transformations A and background, and regularize Gaussian scale and opacity as in MCMC (Kheradmand et al., 2024). We provide details in Sec. D*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/011_Table_3.jpg]]
*Table 3: PandaSet Reconstruction. We outperform all prior work by a wide margin, improving upon the second-best method (SplatAD) by >1dB PSNR while rendering camera views 60% faster*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/012_Table_4.jpg]]
*Table 4: PandaSet NVS. Similar to Table 3, SimULi renders the fastest, provides the best PSNR, and outperforms next-best method SplatAD across every LiDAR metric*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/013_Table_5.jpg]]
*Table 5: Ablations. NVS metrics averaged across PandaSet*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2510_12901/figures/014_Table_6.jpg]]
*Table 6: LiDAR Tiling (MR/s)*

## 定位与知识库关联

### 1. 技术脉络与工作定位

SimULi 处于**自动驾驶场景的联合相机-激光雷达实时仿真**这一交叉前沿。其核心贡献——因子化3D高斯表示——直接回应了该领域的一个结构性瓶颈：现有方法将相机与激光雷达信息编码到同一组3D高斯或神经辐射场中，导致跨传感器不一致性迫使模型在某一模态上做出质量牺牲。

从方法谱系看，SimULi 的技术血缘可追溯至三条主线：

**（1）3D高斯溅射（3DGS）及其相机渲染扩展。** SimULi 的相机渲染管线直接继承自 **3DGUT**（Wu et al., CVPR 2025），后者通过无迹变换（Unscented Transform）将3DGS推广至任意相机模型（鱼眼、卷帘快门等）。SimULi 保留了这一能力，并将其作为相机模态的渲染后端。相较于标准3DGS仅支持针孔相机的限制，这一继承使SimULi天然具备对复杂车载相机系统的适应性。

**（2）联合相机-激光雷达的神经渲染。** 在SimULi之前，该方向的代表性工作包括：
- **UniSim**（Yang et al., CVPR 2023）：基于NeRF的联合重建框架，通过CNN上采样提升渲染质量，但在动态场景中易产生模糊，且渲染速度受限于NeRF的体渲染开销。
- **NeuRAD**（Tonderski et al., CVPR 2024）：同样采用NeRF范式，在动态场景建模上有改进，但渲染速度与相机质量仍不及高斯类方法。
- **SplatAD**（Hess et al., CVPR 2025）：将3DGS扩展至联合相机-激光雷达渲染，是SimULi最直接的对比基线。SplatAD使用统一的3D高斯集同时编码两种模态，通过手工启发式策略处理激光雷达瓦片划分，但仅支持针孔相机，且统一表示在跨模态不一致时存在质量权衡。

SimULi 对SplatAD的突破在于**因子化表示**：将相机高斯集 $G_c$ 与激光雷达高斯集 $G_l$ 分离，各自独立优化以适应各模态特性（如激光雷达需要鼓励二值化透明度的熵损失），同时通过K近邻锚定损失（$K=50$）将相机高斯拉向激光雷达约束的几何表面。这一设计使得激光雷达的几何先验能够提升相机新视角合成质量，而不会因跨模态冲突损害任一传感器的渲染精度。

**（3）激光雷达原生渲染。** 在激光雷达专用渲染方面，**LiDAR-RT**（Zhou et al., CVPR 2025）代表了基于光线追踪的路线，渲染质量高但速度慢。SimULi 在光栅化框架内实现了与之媲美甚至更优的深度重建质量（Table 1中Chamfer Distance更优），同时保持了10-20×的速度优势。

### 2. 核心方法差异与因果机制

下表总结了SimULi与主要基线在关键设计槽位上的差异：

| 设计槽位 | SplatAD | SimULi |
|---------|---------|--------|
| 3D高斯表示 | 统一高斯集，共享参数 | 因子化相机集 $G_c$ 与激光雷达集 $G_l$，通过锚定损失耦合 |
| 激光雷达瓦片策略 | 手工启发式，每个传感器定制 | 基于直方图均衡的自动策略，用户仅需指定最大点数 $M$ |
| 支持的相机模型 | 仅针孔 | 任意相机（鱼眼、卷帘快门），通过无迹变换实现 |
| 激光雷达剔除 | 朴素瓦片渲染 | 基于光线的剔除 + 积分面积表，常数时间过滤 |

**因子化表示**是SimULi最关键的因果旋钮。消融实验（Table 5）表明，相较于统一表示，因子化设计同时提升了相机PSNR和激光雷达Chamfer Distance。锚定损失的作用机制在于：激光雷达高斯集 $G_l$ 在距离损失 $\mathcal{L}_{dist}$ 的监督下，其均值 $\mu$ 被约束到真实几何表面附近；锚定损失 $\mathcal{L}_{anchor} = \frac{1}{n}\sum_{i \in G_c} \|\mu_i - NN(\mu_i, G_l)\|_2$ 则将相机高斯拉向这些几何可靠的表面位置，从而在不依赖稀疏深度投影的情况下改善相机新视角合成的几何一致性。

**自动瓦片策略**解决了激光雷达渲染中的负载均衡问题。传统等间距瓦片划分在激光雷达不规则扫描模式下效率极低——部分瓦片包含大量光束，部分几乎为空。SimULi通过计算仰角累积分布函数（CDF），在CDF等分点处设置瓦片边界，确保每瓦片的光束数近似相等。这一策略无需手工启发，可泛化至任意旋转式激光雷达（Figure 9），且对非旋转式激光雷达也具备扩展潜力（沿方位和仰角两维同时应用）。

### 3. 适用边界与局限

**（1）非刚性物体建模。** SimULi 当前不支持非刚性物体（如行人）的变形建模。论文明确指出，现有非刚性建模方案可直接集成，但这一扩展尚未实现。在动态场景中，行人等非刚性目标会被视为刚性物体处理，可能导致渲染质量下降。

**（2）大视角偏差下的新视图合成。** 当渲染视角远离训练轨迹时，SimULi 的合成质量会退化。这是3DGS类方法的共性局限——高斯粒子的分布密度依赖于训练视角覆盖。论文建议引入生成先验（如扩散模型）来缓解此问题，但尚未实施。

**（3）锚定损失的计算开销。** K近邻搜索（$K=50$）在训练中额外增加约14分钟的时间开销。论文指出可通过减小K值或编写定制CUDA核函数来优化，但当前版本未做此类加速。

**（4）激光雷达传感器类型的泛化。** 自动瓦片策略在旋转式激光雷达上已验证有效，但对固态/非旋转激光雷达的适配尚未实现。论文认为将自动瓦片沿方位和仰角两维同时应用是可行的扩展路径。

### 4. 开放问题与未来方向

基于论文的讨论与实验分析，以下开放问题值得关注：

1. **多传感器扩展。** 因子化表示的核心思想——为不同传感器模态维护独立高斯集并通过几何约束耦合——是否可推广至其他传感器（如毫米波雷达、热成像相机）？这需要验证不同传感器之间的几何一致性是否足够支撑锚定损失的有效性。

2. **训练效率优化。** 锚定损失的K近邻计算是当前训练管线的主要瓶颈。如何在不损害几何对齐质量的前提下降低计算开销，是实现更高效训练的关键工程问题。

3. **生成先验的融合。** 大视角偏差下的新视图合成质量退化是3DGS类方法的通病。将扩散模型等生成先验与因子化表示结合，有望在保持实时渲染的同时扩展有效视角范围。

4. **非刚性动态建模。** 将现有的非刚性物体建模方案（如可变形高斯）集成到因子化框架中，需要处理相机高斯与激光雷达高斯的独立变形以及锚定关系的动态维护，这涉及表示层面的非平凡设计。

5. **自动瓦片策略的进一步泛化。** 将基于CDF的自动瓦片从旋转激光雷达推广到任意扫描模式的传感器，需要在方位-仰角二维空间上设计高效的瓦片划分算法，并验证其在不同传感器上的负载均衡效果。

## 原文 PDF

![[paperPDFs/ICLR_2026/SimULi_Real_Time_LiDAR_and_Camera_Simulation_with_Unscented_Transforms.pdf]]
