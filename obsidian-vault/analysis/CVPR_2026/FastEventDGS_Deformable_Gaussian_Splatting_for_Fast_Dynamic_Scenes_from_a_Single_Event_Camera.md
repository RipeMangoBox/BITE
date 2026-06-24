---
title: "FastEventDGS: Deformable Gaussian Splatting for Fast Dynamic Scenes from a Single Event Camera"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FastEventDGS_Deformable_Gaussian_Splatting_for_Fast_Dynamic_Scenes_from_a_Single_Event_Camera.pdf
project_link: null
code_link: null
aliases:
- FastEventDGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过引入基于事件边缘的局部块运动损失（L_m）和事件流光损失（L_ef），显式约束高斯运动与事件数据的时空一致性，同时利用VGGT深度估计进行几何校正，有效缓解过拟合并提升结构准确性。
primary_logic: 利用事件数据中隐含的运动信息（如边缘移动）来监督可变形高斯的运动，从而在无RGB帧的条件下实现动态场景的高质量重建。
claims:
- 采用连续相机轨迹参数化（B样条），支持任意时间间隔的事件监督。
- 局部块事件运动损失约束物体运动，减轻过拟合。
- 利用现成的深度模型VGGT进行深度校正，显著提升几何质量。
- 光流分解为相机光流和高斯光流，提供显式运动引导。
---

# FastEventDGS: Deformable Gaussian Splatting for Fast Dynamic Scenes from a Single Event Camera

> [!tip] 核心洞察
> 利用事件数据中隐含的运动信息（如边缘移动）来监督可变形高斯的运动，从而在无RGB帧的条件下实现动态场景的高质量重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | FastEventDGS：基于单事件相机的快速动态场景可变形高斯泼溅 |
| 英文题名 | FastEventDGS: Deformable Gaussian Splatting for Fast Dynamic Scenes from a Single Event Camera |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Dai_FastEventDGS_Deformable_Gaussian_Splatting_for_Fast_Dynamic_Scenes_from_a_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FastEventDGS |
| Dataset | BlenderDynamicEvent |

> [!tip] 效果简介
> - BlenderDynamicEvent (Butterfly) 上，PSNR 24.27 (outperforms all baselines)；SSIM 0.9020 (outperforms all baselines)；LPIPS 0.1195 (outperforms all baselines)。

## 概述

事件相机因其高时间分辨率、高动态范围和低延迟特性，在捕捉高速运动场景方面展现出巨大潜力。然而，事件数据固有的稀疏性、噪声干扰以及缺乏绝对强度信息，使得仅凭单一事件流实现高保真动态重建成为一项极具挑战性的任务。现有方法大多依赖辅助传感器（如RGB相机）提供额外的光度约束，这在一定程度上限制了事件相机独立部署的便捷性。

针对上述瓶颈，**FastEventDGS** 提出了一种基于可变形3D高斯泼溅（Deformable 3D Gaussian Splatting）的单事件相机动态场景重建框架。其核心洞察在于：事件数据中隐含的运动信息（如边缘移动）可以被显式提取并用于监督可变形高斯的运动，从而在无RGB帧的条件下实现高质量的4D重建。

方法层面，FastEventDGS 的关键创新体现在三个维度：
- **连续相机轨迹参数化**：采用三次B样条拟合稀疏位姿，支持任意时间间隔的事件监督，解决了事件异步性与离散位姿之间的失配问题。
- **多层级事件约束**：融合事件单积分（ESI）光度损失与事件流光损失，提供全局与局部的光度-几何联合约束；同时引入基于事件边缘的局部块运动损失（$L_m$），显式约束高斯运动与事件数据的时空一致性，有效缓解过拟合。
- **外部深度校正**：借助现成的深度估计模型VGGT进行几何校正，通过尺度不变对数损失（SiLog）显著提升结构准确性。

实验结果表明，FastEventDGS 在合成数据集 BlenderDynamicEvent 上全面超越 D-NeRF、Deformable 3DGS、4D Gaussian Splatting 等基线方法，在 Butterfly 场景下达到 PSNR 24.27 dB、SSIM 0.9020。消融研究进一步揭示，深度损失对性能提升贡献最大（+3.88 dB），而光流损失与运动损失的贡献相近，正则化项则带来一致但较小的增益。在真实世界 Gen4Dynamic 数据集上，该方法同样展现出对动态区域的优异重建能力，验证了事件相机高时间分辨率特性在实际场景中的优势。

**方法定位**：FastEventDGS 属于“基于可变形高斯的单传感器事件相机动态重建”路线，区别于需要RGB-事件融合的 E-4DGS（Feng et al., ACM MM 2025）和 STD-GS（Zhou et al., ICCV 2025），其核心突破在于通过事件内在的运动线索替代外部强度信号，实现了传感器配置的极简化。

**局限与展望**：当前方法依赖已知相机位姿，实际部署需外部位姿估计系统，增加了系统复杂度。未来工作可探索位姿无关的重建技术，进一步提升事件相机在非受控环境中的适用性。

## 背景与动机

事件相机是一种受生物启发的视觉传感器，它异步地检测每个像素的亮度变化，并以微秒级的时间分辨率输出事件流。与传统的基于帧的相机不同，事件相机天然具备高动态范围、低延迟和低带宽的特性，使其在高速运动场景中展现出巨大的潜力。然而，事件数据本身具有稀疏性、噪声大，且仅记录相对亮度变化而缺乏绝对强度信息，这使得从单一事件流中恢复出高保真的动态场景几何与外观成为一个极具挑战性的问题。

近年来，以神经辐射场（NeRF）和3D高斯泼溅（3DGS）为代表的神经渲染技术，在新视角合成和静态场景重建上取得了瞩目的成果。研究者们进一步将此类方法扩展至动态场景，例如**D-NeRF**（Pumarola et al., CVPR 2021）通过引入变形场来建模非刚性运动，**Deformable 3DGS**（Yang et al., CVPR 2024）和**4D Gaussian Splatting**（Wu et al., CVPR 2024）则利用可变形的高斯基元实现了更高效的动态重建。尽管如此，这些方法的成功通常建立在密集、高信噪比的RGB图像输入之上，无法直接适配事件相机稀疏且异步的数据特性。

在事件相机动态重建方向上，已有工作如**E-4DGS**（Feng et al., ACM MM 2025）和**STD-GS**（Zhou et al., ICCV 2025）进行了探索，但它们往往依赖于多传感器融合（如RGB帧与事件流联合）或多视图设置，这在一定程度上削弱了事件相机独立部署的便捷性。核心瓶颈在于：仅凭单一事件流，缺乏绝对强度信息所提供的强约束，模型极易在稀疏信号下产生过拟合，导致动态结构失真或几何坍塌。

针对上述缺口，本文的动机在于：**利用事件数据中隐含的运动信息（如边缘移动），在无RGB帧的条件下，为可变形高斯的运动提供显式、可靠的监督**。通过将事件生成模型与连续相机轨迹参数化相结合，并引入基于事件边缘的局部运动约束和现成的深度估计先验，我们旨在构建一个仅依赖单事件相机的、高保真且快速的动态场景重建框架。

## 核心创新

### 问题瓶颈与创新动机

事件相机以微秒级时间分辨率异步记录亮度变化，天然适合捕捉高速运动。然而，其数据固有的稀疏性、高噪声以及绝对强度信息的缺失，使得仅依赖单一事件流进行高保真动态场景重建极具挑战性。现有方法（如 **E-4DGS**, Feng et al., ACM MM 2025；**STD-GS**, Zhou et al., ICCV 2025）通常需要融合RGB图像或其他辅助传感器来提供光度与几何约束，这严重限制了部署的便捷性。FastEventDGS 的核心创新在于：**首次在仅使用单一事件相机、无任何RGB帧的条件下，实现了高质量的可变形高斯泼溅动态场景重建**。

### 关键创新点（Changed Slots）

相较于基于RGB或多传感器融合的基线方法（如 **D-NeRF**, Pumarola et al., CVPR 2021；**Deformable 3DGS**, Yang et al., CVPR 2024），FastEventDGS 在多个关键维度上进行了根本性重构：

#### 1. 输入数据与表示：从离散帧到异步事件流

基线方法依赖同步的RGB图像序列作为输入，而 FastEventDGS 直接操作**单一事件相机的异步事件流**。为了支持任意时间戳的事件监督，该方法引入了**连续相机轨迹参数化**：利用三次B样条对稀疏的相机位姿进行插值，从而获得任意时刻的连续位姿，使事件生成模型能够在非均匀时间间隔上进行精确的亮度变化积分。

#### 2. 运动约束：从隐式变形到显式事件边缘监督

传统可变形方法（如 Deformable 3DGS）依赖变形MLP隐式学习物体运动，缺乏显式的运动监督信号，容易在事件稀疏区域产生过拟合。FastEventDGS 提出了**基于事件边缘的局部块运动一致性损失（$\mathcal{L}_m$）**：
$$\mathcal{L}_m = \sum_i \sum_j \| \Delta I_j^{g_i} - \Delta I_{j+1}^{g_i} \|_1$$
该损失约束每个高斯在2D投影平面上，其局部块内的事件积分在短时间间隔内保持稳定。其物理直觉在于：单个高斯的投影不应在短时间内远离邻近的事件边缘（参见Figure 3）。这一设计将事件数据中隐含的运动信息（边缘的移动）显式地转化为对高斯运动的几何约束，有效缓解了过拟合。

#### 3. 损失函数体系：从单一渲染损失到多模态事件约束

基线方法通常仅使用L1+SSIM等标准渲染损失，而FastEventDGS构建了一个多层次的事件驱动损失体系：

- **事件光度损失（$\mathcal{L}_e$）**：结合事件单积分（ESI）损失与D-SSIM损失，提供全局亮度变化监督。
- **事件流光损失（$\mathcal{L}_{ef}$）**：将光流分解为相机光流（$\mathcal{F}^C$）和高斯光流（$\mathcal{F}^G$），通过归一化事件积分与光流预测的亮度变化之间的L1距离，提供显式的运动引导。
- **深度损失（$\mathcal{L}_d$）**：利用现成的深度估计模型 **VGGT** 预测场景深度，通过尺度不变对数（SiLog）损失进行几何校正，显著提升结构准确性。
- **正则化项（$\mathcal{L}_{ne} + \mathcal{L}_{sp}$）**：非事件区域约束惩罚无事件区域的虚假亮度变化；空间梯度正则化抑制渲染图像的噪声伪影。

消融实验（Table 3）表明，深度损失的贡献最为突出（PSNR提升 +3.88 dB），而光流损失与运动损失的贡献相近，正则化项则带来一致但较小的增益。

#### 4. 深度监督：引入外部几何先验

基线方法通常无任何深度约束，导致几何重建质量欠佳。FastEventDGS 创新性地引入 VGGT 作为深度估计器，通过 SiLog 损失将外部几何先验注入训练过程，在不依赖RGB深度传感器的前提下大幅提升了深度重建的准确性（参见Figure 7）。

### 创新总结

FastEventDGS 的核心创新可归纳为：**以事件数据中隐含的运动与边缘信息为核心约束，通过连续轨迹插值、显式运动损失、多模态事件损失体系以及外部深度先验的协同作用，突破了单一事件相机动态重建的瓶颈**。该方法将输入模态从RGB帧彻底转向异步事件流，将运动监督从隐式学习转向显式事件边缘约束，将损失函数从单一渲染损失扩展为多层次事件驱动体系，构成了系统性的方法创新。

## 整体框架

FastEventDGS 的整体流程围绕“可变形3D高斯泼溅 + 连续相机轨迹 + 多层级事件约束”三个核心支柱构建，旨在从单一事件相机的异步事件流中恢复高保真的4D动态场景。图2给出了完整的框架概览。

**输入与轨迹参数化**：系统接收单目事件流和稀疏的相机位姿序列作为输入。为了支持任意时间戳的事件监督，框架首先使用三次B样条将稀疏位姿拟合为一条连续时间轨迹，从而获得任意时刻的相机外参和内参。这一设计使得后续所有损失函数可以在事件发生的精确时间点上进行计算，避免了离散帧采样带来的时间对齐误差。

**动态场景表示**：核心渲染骨架采用可变形3D高斯泼溅。静态场景由一组带颜色、位置、协方差和不透明度的3D高斯表示；动态性通过一个变形MLP引入，该MLP以高斯中心位置 $\pmb{x}$ 和时间 $t$ 为输入，输出位置偏移 $\Delta\pmb{x}$、旋转偏移 $\Delta r$ 和缩放偏移 $\Delta s$：

$$( \Delta \pmb { x } , \Delta r , \Delta s ) = \mathcal { D } ( \pmb { x } , t )$$

变形后的高斯通过标准可微光栅化管线投影到2D图像平面，经α混合合成像素颜色。这一表示使场景能够以连续时间的方式响应任意时刻的查询，与事件相机的高时间分辨率特性天然匹配。

**多层级事件约束**：框架的核心创新在于从事件数据中提取了三个互补的监督信号，形成从全局到局部的约束层次：

1. **事件光度损失（全局）**：通过事件单次积分将长时间窗口内的事件累积为亮度变化图，与渲染的亮度变化图计算L1和D-SSIM混合损失，提供全局光度约束。
2. **事件流光损失（几何）**：将光流分解为相机光流和高斯光流，利用线性化亮度恒常假设推导出由光流预测的亮度变化，与归一化的事件积分进行对齐，提供显式的几何运动引导。
3. **局部块运动损失（局部）**：在高斯投影的2D中心周围提取局部块，约束相邻时间步内同一高斯的局部事件积分保持时域一致性，确保高斯运动与事件边缘的移动相匹配，有效抑制过拟合。

**深度与正则化辅助**：为弥补事件数据缺乏绝对强度信息的固有缺陷，框架引入VGGT作为外部深度估计器，通过尺度不变对数损失对渲染深度进行校正。在训练后期，加入非事件区域约束和空间梯度正则化，抑制无事件区域的伪影和噪声。

**总损失**：上述各组件通过加权求和构成最终训练目标：

$$\mathcal { L } = \mathcal { L } _ { e } + \lambda _ { e f } \mathcal { L } _ { e f } + \lambda _ { m } \mathcal { L } _ { m } + \lambda _ { d } \mathcal { L } _ { d } + \lambda _ { n e } \mathcal { L } _ { n e } + \lambda _ { s p } \mathcal { L } _ { s p }$$

整个pipeline端到端可微，无需RGB帧或辅助传感器，仅依赖单一事件相机即可完成动态场景的重建与新视角合成。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed FastEventDGS. The framework takes a monocular event stream and its continuous camera pose trajectory (modeled via B-spline) as input. The core pipeline is built around Deformable Gaussian Splatting with a temporal dimension. Explicit motion guidance is derived by calculating the temporal motion loss*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/001_Figure_1.jpg]]
*Figure 1: FastEventDGS is a novel framework built upon a state-of-the-art Deformable 3D Gaussian Splatting representation, achieving high-fidelity 4D dynamic scene reconstruction from a single event camera stream. This strong performance is attributable to the combined effect of the proposed motion constraint, depth constraint, and regularization term*

## 核心模块与公式推导

FastEventDGS 的核心架构围绕可变形 3D 高斯泼溅（Deformable 3DGS）骨架展开，并通过四个关键模块注入事件数据的特有约束：**连续相机轨迹插值**、**事件光度与流光约束**、**局部块运动损失**，以及**深度校正与正则化**。各模块协同作用，使得系统在仅依赖单一事件相机异步流输入的条件下，仍能获得高质量的动态场景重建。

### 3.1 事件相机成像模型

事件相机异步记录每个像素的亮度变化。当一个像素 $i$ 的对数亮度变化超过预设的对比度阈值 $C$ 时，触发一个事件 $e_i = (\mathbf{x}_i, t_i, p_i)$，其中极性 $p_i \in \{-1, +1\}$ 表示亮度增加或减少。其数学描述为：

$$
I(\mathbf{x}_k, t_k) - I(\mathbf{x}_k, t_k - \Delta t_k) = \Delta I(\mathbf{x}_k, t_k) = p_k C
$$

其中 $I(\mathbf{x}, t)$ 为对数亮度，$\Delta t_k$ 是自上次事件以来的时间间隔。对于短时间间隔 $\Delta \tau$，亮度变化可通过亮度恒常假设线性化：

$$
\Delta I(\mathbf{x}) \approx -\nabla \mathcal{T}(\mathbf{x}) \cdot \mathbf{v}(\mathbf{x}) \Delta \tau
$$

这里 $\mathcal{T}(\mathbf{x})$ 为渲染图像强度，$\mathbf{v}(\mathbf{x})$ 为像素 $\mathbf{x}$ 处的光流。这一关系将事件数据与场景运动显式关联，是后续光流损失与运动损失的理论基础。

### 3.2 可变形 3D 高斯泼溅骨架

动态场景由一组带时间维度的 3D 高斯 $G_i = (\mathbf{x}_i, \mathbf{r}_i, \mathbf{s}_i, \mathbf{c}_i, \alpha_i)$ 表示。每个高斯的几何属性通过一个变形 MLP $\mathcal{D}$ 在时间维度上预测其变化量：

$$
(\Delta \mathbf{x}, \Delta \mathbf{r}, \Delta \mathbf{s}) = \mathcal{D}(\mathbf{x}, t)
$$

变形后的高斯经投影与 $\alpha$-混合生成渲染图像：

$$
C(\mathbf{p}) = \sum_{i}^{N} c_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j)
$$

该骨架提供了可微分的动态场景表示，使得事件信号可通过渲染管线反向传播梯度。

### 3.3 连续相机轨迹与事件积分监督

为支持任意时间戳的事件监督，系统使用三次 B 样条（cubic B-spline）将稀疏的相机位姿拟合为连续时间轨迹。在此基础上，事件积分将离散事件流转化为亮度变化图，作为监督信号：

$$
\Delta I = \int_{t_k - \Delta t_k}^{t_k} C \cdot e(\tau) d\tau
$$

预测的亮度变化 $\Delta \hat{I}$ 由渲染图像在时间维度上的差分得到。事件光度损失 $\mathcal{L}_e$ 由事件单积分（ESI）损失与 D-SSIM 损失加权组合构成：

$$
\mathcal{L}_e = (1 - \lambda_e) \mathcal{L}_{esi}(\Delta I, \Delta \hat{I}) + \lambda_e \mathcal{L}_{D\text{-}SSIM}(\Delta I, \Delta \hat{I})
$$

其中 ESI 损失为：

$$
\mathcal{L}_{esi} = \left\| \Delta I - \Delta \hat{I} \right\|_1 \odot \mathbf{m}
$$

$\mathbf{m}$ 为事件掩码，仅在有事件触发的像素位置施加监督。该损失提供全局光度约束，但缺乏对物体运动的显式引导。

### 3.4 事件流光损失

为引入局部几何约束，系统将光流 $\mathbf{v}(\mathbf{x})$ 分解为相机光流 $\mathbf{F}^C$ 和高斯光流 $\mathbf{F}^G$，并利用线性化亮度恒常假设（式 3）将光流预测的亮度变化与归一化事件积分对齐：

$$
\mathcal{L}_{ef} = \left\| \frac{\Delta I'}{\|\Delta I'\|_2} - \frac{\Delta \hat{I}(\mathbf{x}; \mathcal{F}_{t, t+\Delta \tau}^O)}{\|\Delta \hat{I}(\mathbf{x}; \mathcal{F}_{t, t+\Delta \tau}^O)\|_2} \right\|_1
$$

该损失在归一化空间中比较方向一致性，对亮度尺度不敏感，适合事件相机缺乏绝对强度信息的特性。

### 3.5 局部块运动损失

事件流光损失虽能提供运动引导，但在纹理稀疏区域约束较弱，易导致高斯运动过拟合。为此，系统引入局部块运动损失 $\mathcal{L}_m$，直接约束高斯中心投影 $g^i = \pi(K, T_t, (\mathbf{x} + \Delta \mathbf{x}))$ 附近的事件边缘在短时间内的运动一致性：

$$
\mathcal{L}_m = \sum_i \sum_j \left\| \Delta I_j^{g_i} - \Delta I_{j+1}^{g_i} \right\|_1
$$

其中 $\Delta I_j^{g_i}$ 表示以高斯投影 $g_i$ 为中心的局部块内的事件积分。该损失强制高斯运动与事件边缘的移动保持一致，是缓解过拟合的关键机制（见 **Figure 3**）。

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/003_Figure_3.jpg]]
*Figure 3: The illustration of our proposed motion loss. It ensures that individual 2D projections of Gaussians do not move far from the neighboring event edges over a short time period*

### 3.6 深度校正与正则化

由于事件数据不提供绝对深度信息，系统利用现成的单目深度估计模型 VGGT 预测场景深度 $\hat{d}$，并通过尺度不变对数（SiLog）损失进行校正：

$$
\mathcal{L}_d = \frac{1}{n} \sum_i \alpha_i^2 - \frac{1}{n^2} \left( \sum_i \alpha_i \right)^2, \quad \alpha_i = \log d_i - \log \hat{d}_i
$$

此外，为抑制无事件区域的伪影和噪声，引入两项正则化：

- **非事件区域约束** $\mathcal{L}_{ne}$：惩罚无事件像素处预测亮度变化超过阈值 $C$：

  $$
  \mathcal{L}_{ne} = \text{ReLU}(|\Delta \hat{I}| - C) \odot \neg \mathbf{m}
  $$

- **空间梯度正则化** $\mathcal{L}_{sp}$：抑制渲染图像中过大的空间梯度以减轻噪声：

  $$
  \mathcal{L}_{sp} = \|\delta_x \mathcal{T}\|_1 + \|\delta_y \mathcal{T}\|_1
  $$

最终训练损失为各分量的加权和：

$$
\mathcal{L} = \mathcal{L}_e + \lambda_{ef} \mathcal{L}_{ef} + \lambda_m \mathcal{L}_m + \lambda_d \mathcal{L}_d + \lambda_{ne} \mathcal{L}_{ne} + \lambda_{sp} \mathcal{L}_{sp}
$$

消融实验（**Table 3**）表明，深度损失 $\mathcal{L}_d$ 对性能提升贡献最大（PSNR 从 18.61 提升至 22.49），光流损失与运动损失贡献相近，正则化项则带来一致但较小的增益。

## 实验与分析

### 核心实验设置

FastEventDGS 在合成数据集 **BlenderDynamicEvent** 和真实世界数据集 **Gen4Dynamic** 上进行评估。对比基线涵盖动态场景神经辐射场 **D-NeRF**（Pumarola et al., CVPR 2021）、可变形高斯泼溅 **Deformable 3DGS**（Yang et al., CVPR 2024）、**4D Gaussian Splatting**（Wu et al., CVPR 2024）、多视图事件相机动态重建方法 **E-4DGS**（Feng et al., ACM MM 2025），以及事件-帧交互重建方法 **STD-GS**（Zhou et al., ICCV 2025）。所有对比方法均在同一数据集上重新训练或按原文设置进行，但真实世界数据集因存在拖尾事件噪声，可能对公平性产生一定影响，此点需读者酌情考量。

### 合成数据集主结果

在 BlenderDynamicEvent 的四个动态场景上，FastEventDGS 在所有指标上均优于所有基线方法。以最具代表性的 Butterfly 场景为例，本方法取得了 **PSNR 24.27**、**SSIM 0.9020**、**LPIPS 0.1195** 的最佳结果（Table 1）。定性结果（Figure 4）进一步表明，本方法在新视角合成中能够更准确地恢复动态区域的精细几何和纹理细节，而基线方法在快速运动区域往往产生模糊或伪影。这一优势源于事件相机的高时间分辨率特性以及所提出的运动约束与深度约束的协同作用。

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of different methods on the synthetic BlenderDynamicEvent dataset*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative evaluation for novel view image synthesis on our synthetic BlenderDynamicEvent dataset. The results show that our method consistently outperforms all baselines*

### 消融实验

消融实验系统评估了各损失组件和运动速度对重建质量的影响。

**损失组件消融**（Table 3）揭示了以下关键发现：

- **深度损失 $L_d$ 贡献最大**：在基础事件光度损失 $L_e$ 之上加入深度损失后，PSNR 从 18.61 跃升至 22.49（**+3.88 dB**），验证了 VGGT 深度估计对几何校正的决定性作用。
- **光流损失与运动损失贡献相近**：$L_{ef}$ 和 $L_m$ 各自带来显著且幅度相近的性能提升，表明事件流光约束和基于边缘的局部块运动约束互为补充，共同抑制了变形场的过拟合。
- **正则化项带来一致但较小的提升**：非事件区域约束 $L_{ne}$ 和空间梯度正则化 $L_{sp}$ 在已有较强监督的基础上仍能提供稳定的增益，有效抑制了无事件区域的噪声伪影。

**运动速度消融**（Table 2）显示，随着物体运动速度从 1× 增加到 4×，PSNR 从 22.91 持续下降至 18.31。这一趋势（Figure 6 提供视觉对比）表明，极高速运动下事件数据的稀疏性和模糊性加剧，对变形场的时序建模能力提出了更大挑战，构成了当前方法的一个边界条件。

### 深度重建质量

Figure 7 展示了深度重建的定性对比。引入 VGGT 深度监督后，本方法能够恢复出结构清晰、边界锐利的深度图，而缺少深度约束的变体则出现明显的几何塌缩和边界模糊。这从侧面印证了在缺乏绝对强度信息的事件相机设定下，外部几何先验对于约束三维结构的关键作用。

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/010_Figure_7.jpg]]
*Figure 7: Comparison of depth reconstruction*

### 失败模式与局限性

尽管 FastEventDGS 在合成和真实场景中均表现出色，但仍存在以下局限：

1. **依赖已知相机位姿**：当前方法假设相机轨迹已通过外部系统（如 B 样条拟合的稀疏位姿）预先标定。在实际部署中，这一要求增加了系统复杂度。未来工作需探索位姿无关的重建技术。
2. **极高速运动退化**：如运动速度消融所示，在 4× 速度条件下性能显著下降，事件数据的信噪比降低导致运动约束的有效性减弱。
3. **真实世界噪声敏感性**：真实数据集中的拖尾事件噪声可能引入额外的不确定性，当前的正则化策略虽能部分缓解，但尚未从根本上解决噪声鲁棒性问题。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the object motion speed*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the proposed loss components*

![[assets/figures/papers/paper_list_l22_https_openaccess_thecvf_com_content_CVPR2026_html_Dai_FastEventDGS_Defor/figures/009_Figure_6.jpg]]
*Figure 6: Comparison of different motion speeds*

## 方法谱系与知识库定位

### 1. 与已有工作的关系

**FastEventDGS** 处于动态场景重建、事件相机视觉与3D高斯泼溅三个领域的交叉点。其设计思路可归入“可变形高斯泼溅 + 事件驱动约束”这一技术路线，与以下基线方法形成明确对比：

- **D-NeRF** (Pumarola et al., CVPR 2021)：作为动态场景神经辐射场的代表性工作，D-NeRF 将场景分解为规范空间与变形场，但依赖RGB图像作为监督信号。FastEventDGS 继承了“规范空间 + 变形”的建模范式，但将输入模态替换为事件流，并引入显式运动约束以弥补事件数据缺乏绝对强度信息的缺陷。

- **Deformable 3DGS** (Yang et al., CVPR 2024)：在3DGS基础上引入变形MLP，实现动态场景的高效渲染。FastEventDGS 直接复用其变形骨架 $(\Delta \pmb{x}, \Delta r, \Delta s) = \mathcal{D}(\pmb{x}, t)$，但在损失函数层面进行了根本性改造——将标准渲染损失替换为事件光度损失、事件流光损失、运动损失与深度损失的组合，使框架能够从纯事件流中学习。

- **4D Gaussian Splatting** (Wu et al., CVPR 2024)：将时间维度直接嵌入高斯表示。FastEventDGS 未采用4D高斯参数化，而是选择“3D高斯 + 时变变形”的分离式设计，这使其对快速运动的建模更灵活，但也增加了变形场学习的难度。

- **E-4DGS** (Feng et al., ACM MM 2025) 与 **STD-GS** (Zhou et al., ICCV 2025)：这两项工作均涉及事件相机与动态重建，但存在关键差异。E-4DGS 面向多视图事件相机设置，依赖多视角几何约束；STD-GS 则采用事件-帧交互模式，仍需RGB帧提供绝对亮度参考。FastEventDGS 的独特之处在于仅使用**单一事件相机**，完全摆脱对RGB帧的依赖，这在部署便捷性上具有显著优势。

### 2. 核心技术贡献的定位

FastEventDGS 的方法论贡献可凝练为三个因果调节变量，它们共同解决了“单一事件流约束不足”这一瓶颈：

1. **事件边缘驱动的局部块运动损失（$L_m$）**：这是论文最具原创性的设计。传统可变形高斯方法依赖变形MLP隐式学习运动，在缺乏密集光度监督时极易过拟合到噪声事件。$L_m$ 通过约束高斯投影中心邻域内事件积分的时域一致性（Eq. 15），显式地将高斯运动与事件边缘绑定，相当于为变形场提供了稀疏但高精度的运动锚点。这一设计将事件相机“高时间分辨率”的物理优势转化为可优化的几何约束。

2. **VGGT深度校正**：利用现成深度估计模型进行几何正则化并非全新思路，但在事件相机动态重建场景中，其作用被显著放大。消融实验表明，仅添加深度损失即可使PSNR从18.61提升至22.49（+3.88 dB），这揭示了一个深层事实：事件数据对纹理边缘敏感，但对均匀区域的深度歧义几乎无法提供有效信号，外部几何先验恰好填补了这一空白。

3. **光流分解与事件流光损失（$L_{ef}$）**：将光流 $\mathbf{v}(\mathbf{x})$ 分解为相机光流 $\mathcal{F}^C$ 和高斯光流 $\mathcal{F}^G$，并利用归一化事件积分与光流预测的亮度变化进行对齐（Eq. 13）。这一设计的巧妙之处在于，它绕过了事件数据无法直接提供光流真值的问题，转而利用亮度恒常假设的线性化形式建立间接监督。

### 3. 适用边界与局限

**已知位姿依赖**是当前框架最根本的适用限制。FastEventDGS 要求输入连续的相机轨迹（通过B样条插值稀疏位姿获得），这意味着实际部署中必须配备外部位姿估计系统（如外部运动捕捉或SLAM模块）。论文明确将“发展位姿无关的重建技术”列为未来工作方向。

**运动速度的敏感性**构成另一个实用边界。消融实验显示，当物体运动速度从1x提升至4x时，PSNR从22.91降至18.31（Table 2）。这表明在极快速运动下，事件积分的线性化假设（Eq. 3）可能失效，变形MLP的时序建模能力也面临挑战。

**真实世界噪声的鲁棒性**尚未得到充分验证。论文在真实世界Gen4Dynamic数据集上展示了定性结果，但承认存在拖尾事件噪声，这可能影响定量比较的公平性。非事件区域约束（$L_{ne}$）和空间正则化（$L_{sp}$）虽被设计用于抑制噪声，但其在更复杂噪声条件下的有效性仍需进一步检验。

### 4. 开放问题

- **位姿-重建联合优化**：是否可以设计一种完全不依赖预先标定位姿的事件相机动态场景重建方法？这需要将相机位姿也纳入可优化变量，但事件数据的稀疏性可能使联合优化面临严重的尺度模糊问题。

- **多事件相机扩展**：当前方法仅支持单目设置。若扩展至多事件相机，如何融合不同视角的事件流并保持时间一致性，是一个值得探索的方向。

- **与神经辐射场的深度融合**：FastEventDGS 选择了高斯泼溅作为底层表示，主要出于渲染效率的考量。但事件数据天然适合与基于物理的成像模型结合，未来工作可探索将事件生成模型更紧密地嵌入神经辐射场的优化过程中。

## 原文 PDF

![[paperPDFs/CVPR_2026/FastEventDGS_Deformable_Gaussian_Splatting_for_Fast_Dynamic_Scenes_from_a_Single_Event_Camera.pdf]]
