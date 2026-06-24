---
title: "PPISP: Physically-Plausible Compensation and Control of Photometric Variations in Radiance Field Reconstruction"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PPISP_Physically_Plausible_Compensation_and_Control_of_Photometric_Variations_in_Radiance_Field_Reconstruction.pdf
aliases:
- PPPICMC
- PPISP
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过物理合理的ISP校正模块（曝光偏移、渐晕、色彩校正、相机响应函数）解耦传感器固有属性和捕获相关设置，并引入一个从渲染辐射预测每帧ISP参数的控制器，实现无需目标图像的新视角评估。
primary_logic: 利用相机图像形成的物理过程对辐射场进行事后校正，不仅增强了可解释性和可控性，还能通过训练控制器直接从辐射场预测参数，逼近真实相机的自动曝光和自动白平衡行为，从而无需访问目标图像即可完成新视角合成评估。
claims:
- PPISP在全标准基准上取得最佳PSNR/SSIM/LPIPS，在多数设置下超越BilaRF（即使后者使用目标图像对齐）
- 移除曝光模块导致Tanks and Temples新视角PSNR从24.62降至23.33，各模块均对整体性能有贡献
- 在HDR-NeRF数据集上，利用元数据可将3DGUT+PPISP PSNR从17.86提升至34.30，证明元数据融合的有效性
- PPISP控制器预测的参数使PSNR接近甚至达到目标图像色彩对齐后的指标（PSNR-CC），表明其泛化能力
---

# PPISP: Physically-Plausible Compensation and Control of Photometric Variations in Radiance Field Reconstruction

> [!tip] 核心洞察
> 利用相机图像形成的物理过程对辐射场进行事后校正，不仅增强了可解释性和可控性，还能通过训练控制器直接从辐射场预测参数，逼近真实相机的自动曝光和自动白平衡行为，从而无需访问目标图像即可完成新视角合成评估。

| 字段 | 内容 |
|------|------|
| 中文题名 | PPISP：辐射场重建中光度变化的物理合理补偿与控制 |
| 英文题名 | PPISP: Physically-Plausible Compensation and Control of Photometric Variations in Radiance Field Reconstruction |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2601.18336) · [Project](https://research.nvidia.com/labs/sil/projects/ppisp/) · [Code](https://github.com/nv-tlabs/ppisp) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | PPISP (Physically-Plausible ISP correction module + controller) |
| Dataset | Tanks and Temples, Mip-NeRF 360, HDR-NeRF, BILARF |

> [!tip] 效果简介
> - Tanks and Temples 上，PSNR 24.62 (PPISP w/ ctrl.) vs 19.78 (BilaRF) (+4.84)。
> - Mip-NeRF 360 上，PSNR 28.15 (3DGUT+PPISP w/ ctrl.) vs 24.97 (3DGUT+BilaRF) (+3.18)。
> - HDR-NeRF (with metadata) 上，PSNR 34.30 (3DGUT+PPISP w/ ctrl. + metadata) vs 17.86 (3DGUT+PPISP w/o metadata) (+16.44)。

## 概述

多视角三维重建高度依赖输入图像的光度一致性，然而真实世界的图像采集过程引入了大量光度变化——这些变化源自相机光学特性、传感器差异以及图像信号处理（ISP）管线的不同。传统应对方案，如每帧隐向量优化（**GLO**）、像素级仿射色彩校正（**BilaRF**）或事后显式处理（**ADOP**），要么缺乏物理基础导致泛化能力不足，要么依赖目标图像进行测试时对齐，掩盖了方法间的真实差异。

本文提出**PPISP**（Physically-Plausible ISP），一个物理合理且可微的图像信号处理校正模块，其核心思想是：**将相机图像形成的物理过程显式建模为辐射场的后处理管线，从而解耦传感器固有属性与捕获相关设置，并引入一个控制器从渲染辐射直接预测每帧ISP参数，实现无需访问目标图像的新视角评估。** 这一设计不仅增强了可解释性和可控性，还使控制器能够模拟真实相机的自动曝光和自动白平衡行为。

PPISP的管道由四个物理接地模块顺序构成：**曝光偏移**（全局基-2指数缩放）、**渐晕校正**（多通道径向多项式衰减）、**色彩校正**（基于色度单应性变换，解耦曝光与白平衡）以及**相机响应函数**（分段幂函数S曲线）。训练分两阶段进行：第一阶段联合优化辐射场表示与ISP模块参数；第二阶段冻结ISP模块，仅训练控制器从渲染辐射预测曝光偏移和色彩校正参数。

实验表明，PPISP在全标准基准上取得最优PSNR/SSIM/LPIPS。在Tanks and Temples数据集上，PPISP（含控制器）新视角PSNR达到**24.62**，较BilaRF的19.78提升**+4.84**；在Mip-NeRF 360上，3DGUT+PPISP较3DGUT+BilaRF提升**+3.18** PSNR。值得注意的是，即使BilaRF在测试时有权访问目标图像进行色彩对齐（PSNR-CC），PPISP在多数数据集上仍能超越或接近其性能。消融实验证实，各物理模块均对整体性能有贡献，其中移除曝光偏移模块导致PSNR下降最大（-1.29）。此外，PPISP可选择性集成相机元数据（如EXIF），在HDR-NeRF数据集上将PSNR从17.86大幅提升至**34.30**。

方法定位上，PPISP属于**物理驱动的事后校正范式**，与基于隐向量的外观建模（GLO）和像素级仿射变换（BilaRF）形成对比。其低维参数化有效限制了模型容量，减少了过拟合——训练视图PSNR低于BilaRF，但新视图PSNR显著更高，验证了泛化优势。

## 背景与动机

### 问题背景：多视角3D重建中的光度不一致性

从多视角图像重建三维场景是计算机视觉与图形学的核心任务。近年来，基于辐射场（radiance field）的方法（如NeRF及其变体）在该领域取得了显著进展。然而，这些方法普遍依赖一个隐含假设：同一场景点在不同视角下具有一致的光度表现。这一假设在真实世界的多视角采集中几乎从不成立。

真实相机在图像采集过程中，会经历一系列图像信号处理（ISP）环节，包括曝光控制、渐晕（vignetting）衰减、白平衡校正以及非线性相机响应函数（CRF）映射。这些环节的参数随相机型号、拍摄设置和场景内容动态变化，导致同一场景在不同图像中呈现显著的光度差异——即使底层辐射度完全一致。这种光度不一致性直接破坏了辐射场重建的核心假设，使得未经校正的重建结果在颜色、亮度和对比度上出现严重偏差。

### 现有方法的局限

当前应对光度变化的方案主要分为三类，均存在根本性缺陷：

**隐式外观编码（GLO/NeRF-W范式）** 为每帧图像学习一个隐式外观向量，将其注入辐射场的生成过程。该方法缺乏物理基础，将相机光学效应与场景几何/材质信息混杂在隐空间中，导致泛化能力差——新视角的外观参数无法从场景内容推断，必须重新优化。

**全局仿射色彩校正（BilaRF范式）** 通过双边网格对渲染结果进行逐像素仿射变换。虽然相比GLO更具结构性，但仿射变换无法解耦曝光、白平衡和CRF等物理上独立的效应，且校正能力过剩，容易过拟合到训练视图的色彩分布，在新视角上产生伪影。

**显式后处理（ADOP范式）** 引入了曝光、白平衡和CRF等显式模块，但模块间缺乏物理约束，导致曝光与色彩校正相互耦合。例如，ADOP中曝光参数的调整会放大辐射场中已“烘焙”的色彩伪影（见Figure 7），说明其解耦不彻底。

此外，现有方法的评估协议存在严重缺陷。常用的PSNR-CC指标在评估前对渲染结果与目标图像进行仿射色彩对齐，这一操作掩盖了方法的真实光度校正能力，且在实际应用中（无目标图像）不可行。这种评估方式使得不同方法的真实差异被系统性低估。

### 核心动机与解决思路

本文的核心动机源于一个关键观察：**相机的图像形成过程遵循明确的物理模型**。曝光偏移是全局的乘法因子，渐晕是径向的衰减函数，白平衡是色度空间中的线性变换，CRF是单调非线性的S曲线。如果将这些物理约束显式地嵌入辐射场重建管道，不仅能实现可解释的光度校正，还能从根本上解耦传感器固有属性与捕获相关设置。

更进一步，真实相机具备自动曝光（AE）和自动白平衡（AWB）机制——它们根据场景内容动态调整成像参数，无需访问“目标图像”。这一机制启示我们：**一个训练好的控制器应当能够从渲染辐射度中直接预测新视角的ISP参数**，从而在测试时完全摆脱对目标图像的依赖。

基于以上动机，PPISP提出了两个核心组件：
1. **物理合理的ISP校正模块**：通过曝光偏移、渐晕、色彩校正和CRF四个顺序模块，将光度变化建模为物理上可解释的变换序列。
2. **ISP参数控制器**：从渲染辐射度预测每帧的曝光和色彩校正参数，模拟真实相机的AE/AWB行为，实现无需目标图像的新视角评估。

## 核心创新

PPISP的核心创新在于将**物理合理的相机图像形成模型**引入辐射场重建的外观校正环节，从而在三个层面实现了对现有方法的突破：校正机制的可解释性、新视角参数的自动预测，以及评估协议的公平性。

### 从隐式外观编码到物理ISP模块

现有外观补偿方法普遍采用隐式或纯数据驱动的校正策略。**GLO**（NeRF-W）为每帧图像优化隐式外观向量，**BilaRF** 使用双边网格进行逐像素仿射色彩校正，**ADOP** 虽然显式建模了曝光、白平衡、CRF和渐晕，但其色彩校正仅采用简单的逐通道增益缩放，且各模块之间缺乏物理约束的耦合。这些方法的一个共同缺陷是：校正参数缺乏明确的物理含义，导致模型容量与泛化能力之间的权衡难以控制——高容量模型容易过拟合训练视图的外观，而低容量模型又无法充分补偿光度变化。

PPISP的关键设计是将校正过程构建为**四个物理基础模块的有序级联**（Figure 2），每个模块对应相机成像管线中的一个真实环节：

1. **曝光偏移模块**（Exposure Offset）：对渲染辐射度施加全局的、基于2的指数的缩放 $$$\mathbf{I}^{\mathrm{exp}} = \mathbf{L} \cdot 2^{\Delta t}$$$ ，模拟相机曝光时间的物理效应。该模块仅引入每帧1个标量参数，是全局光度变化的最主要来源。

2. **渐晕模块**（Vignetting）：通过多项式 $v(r) = \mathrm{clip}_{(0,1)}(1 + \alpha_1 r^2 + \alpha_4 r^4 + \alpha_6 r^6)$ 建模径向强度衰减，并允许优化光学中心位置，捕捉镜头固有的边缘减光效应。

3. **色彩校正模块**（Color Correction）：这是与ADOP等方法的**核心分水岭**。PPISP采用RG色度空间上的3×3单应性变换 $h(\mathbf{x}; \mathbf{H})$，并先进行强度归一化解耦曝光影响，而非简单的逐通道增益。这一设计不仅提供了更丰富的色彩映射能力（可建模白平衡、色彩空间转换等），更关键的是**从结构上解耦了曝光与色彩校正**——曝光模块独立控制全局亮度，色彩模块仅调整色度分布，避免了ADOP中曝光变化导致色彩伪影被放大的问题（Figure 7）。

4. **相机响应函数模块**（CRF）：采用分段幂函数曲线 $f_0(x; \tau, \eta, \xi)$，约束为单调且C1连续，模拟传感器非线性响应。与ADOP的离散节点线性插值相比，该参数化具有更低的自由度和更强的物理合理性。

这种物理模块化设计的直接收益是**有限的模型容量带来的更好的泛化能力**。Table 5显示，PPISP在训练视图上的PSNR低于BilaRF（表明更少的过拟合），但在新视图上的PSNR显著更高（24.62 vs. 19.78），验证了物理约束对泛化的促进作用。

### 从测试时优化到控制器预测

传统方法在处理新视角时面临一个根本困境：要么假设目标图像可访问以重新优化参数（如BilaRF的PSNR-CC评估协议），要么简单地将参数设为零（导致光度不一致）。PPISP通过引入**控制器模块** $$$\mathcal{T}(\mathbf{L})$$$ 彻底改变了这一范式。

控制器从渲染的辐射度 $\mathbf{L}$ 中直接预测曝光偏移 $\Delta t$ 和色彩校正参数 $$\{\Delta \mathbf{c}_k\}$$ ，其设计灵感来源于真实相机的自动曝光（AE）和自动白平衡（AWB）机制。具体实现为：一个粗粒度特征提取器（1×1卷积后池化至5×5网格）接参数回归MLP，在第二阶段独立训练，而其他ISP模块冻结。

Figure 3展示了控制器的动态行为——预测的曝光偏移随场景内容变化而自适应调整，呈现出与真实相机AE相似的响应模式。Table 1表明，控制器预测的参数使新视图PSNR接近甚至达到使用目标图像进行仿射色彩对齐后的指标（PSNR-CC），证明了其在不访问目标图像前提下的泛化能力。这一特性使得PPISP成为首个**真正无需目标图像即可完成新视角合成评估**的外观校正方法。

### 物理约束与元数据的协同

PPISP的物理合理性还体现在其能够**选择性融合相机元数据**以进一步提升性能。Table 3显示，在HDR-NeRF数据集上，利用EXIF元数据可将3DGUT+PPISP的PSNR从17.86提升至34.30（+16.44），展示了物理模型与传感器先验信息的天然兼容性。即使不提供元数据，物理约束本身也足以引导模型学习合理的校正参数。

### 解耦设计的因果验证

Figure 6通过分析曝光偏移与白平衡变量之间的Pearson相关系数，定量验证了PPISP色彩校正模块的解耦效果。在ADOP中，曝光与红/蓝通道缩放强相关（相关系数高），而PPISP中曝光偏移与白点偏移近乎独立（相关系数接近零）。这种解耦是实现Figure 7所示曝光编辑鲁棒性的关键——PPISP的辐射场和输出在曝光变化时保持中性，而ADOP的色彩伪影会随曝光调整而被放大。

综上，PPISP的创新可概括为三个**changed slots**：外观校正从隐式/仿射变换变为物理ISP级联，新视角参数从测试时优化变为控制器预测，色彩校正从逐通道增益变为色度单应性变换。这些设计共同实现了可解释性、可控性和泛化能力的统一提升。

## 整体框架

PPISP 构建了一个**物理合理的可微图像信号处理（ISP）管道**，作为辐射场重建的即插即用外观补偿层。该管道遵循真实相机的图像形成过程，将场景辐射度到最终像素值的转换建模为一系列物理基础模块的级联操作，从而将传感器固有属性与拍摄相关的设置解耦。

### 管道架构与数据流

Figure 2 展示了完整的管道结构。给定辐射场沿相机光线 $\mathbf{r}$ 渲染出的原始辐射度 $\mathbf{L}(\mathbf{r})$（由 Eq. (1) 的体积渲染积分得到），PPISP 依次施加四个物理模块：

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/002_Figure_2.jpg]]
*Figure 2: Our proposed pipeline applies a sequence of physically-grounded modules to the input reconstructed radiance (exposure offset, chromatic vignetting, linear color correction, and non-linear camera response function). Top: all modules except the controller are jointly optimized during the first training phase. Bottom: the controller is then trained to predict per-frame exposure and color correction for novel views while other modules are frozen. The image sequence illustrates the progressive effect of each module*

$$
\mathbf{L}(\mathbf{r}) \xrightarrow{\text{曝光偏移}} \mathbf{I}^{\mathrm{exp}} \xrightarrow{\text{渐晕}} \mathbf{I}^{\mathrm{vig}} \xrightarrow{\text{色彩校正}} \mathbf{I}^{\mathrm{cc}} \xrightarrow{\text{CRF}} \mathbf{I}^{\mathrm{out}}
$$

1. **曝光偏移模块（Exposure Offset）**：对辐射度施加全局的、逐帧的缩放，使用以 2 为底的指数参数化 $\Delta t$，即 $\mathbf{I}^{\mathrm{exp}} = \mathbf{L} \cdot 2^{\Delta t}$（Eq. (3)）。该设计模拟了相机的曝光时间或 ISO 调整，使辐射场本身保持光度一致，而亮度变化由该模块独立承担。

2. **渐晕模块（Vignetting）**：建模逐通道的径向强度衰减，使用关于像素到光学中心距离 $r$ 的多项式 $v(r) = \mathrm{clip}_{(0,1)}(1 + \alpha_1 r^2 + \alpha_2 r^4 + \alpha_3 r^6)$（Eq. (5)）。光学中心 $\mu$ 和多项式系数 $\alpha$ 均为可优化参数，属于传感器固有属性，在训练后固定不变。

3. **色彩校正模块（Color Correction）**：在色度-强度空间进行线性变换。具体而言，通过 RG 色度坐标上的 3×3 单应性矩阵 $\mathbf{H}$ 实现白平衡和色彩校正（Eq. (8)），并在此过程中进行强度归一化，从而将白平衡与曝光效应解耦。该模块的逐帧参数 $\Delta \mathbf{c}_k$ 控制目标色度点的偏移。

4. **相机响应函数模块（CRF）**：将线性辐照度映射为非线性像素值，采用分段幂函数曲线 $f_0(x; \tau, \eta, \xi)$（Eq. (14)），在分界点 $\xi$ 处保持 $C^1$ 连续性，强制单调且平滑。CRF 属于传感器固有模块，跨帧共享。

### 模块属性分类

PPISP 的关键设计在于区分两类参数：

- **传感器固有参数**（per-sensor）：渐晕系数 $\alpha$ 与光学中心 $\mu$、CRF 曲线参数 $\tau, \eta, \xi$。这些参数在训练阶段联合优化，但在推理时保持固定，反映特定相机的物理特性。
- **捕获相关参数**（per-frame）：曝光偏移 $\Delta t$ 和色彩校正偏移 $\{\Delta \mathbf{c}_k\}$。这些参数随每帧的拍摄条件变化，在训练阶段通过反向传播直接优化，在测试阶段则由控制器预测。

这种解耦使得辐射场重建专注于几何与反射属性，而光度变化完全由 ISP 管道的外部模块解释，避免了将外观变化“烘焙”进辐射场内部表示。

### 控制器与两阶段训练

Figure 2 底部展示了控制器的训练流程。整体训练分为两个阶段：

**第一阶段（联合优化）**：所有模块（除控制器外）与辐射场重建主干网络联合训练。每帧的 $\Delta t$ 和 $\{\Delta \mathbf{c}_k\}$ 作为自由变量直接优化，传感器固有参数跨帧共享。损失函数包括渲染损失与四项正则化项的总和 $\mathcal{L}_{\mathrm{reg}} = \mathcal{L}_b + \mathcal{L}_c + \mathcal{L}_{\mathrm{var}} + \mathcal{L}_{\mathrm{vig}}$（Eq. (22)），分别约束亮度、色度、参数方差和渐晕。

**第二阶段（控制器训练）**：冻结辐射场和所有 ISP 模块，训练一个轻量控制器 $\mathcal{T}$，从渲染辐射度预测逐帧参数：

$$
\left( \Delta t , \{ \Delta \mathbf{c}_k \} \right) = \mathcal{T}(\mathbf{L}) \quad \text{(Eq. (17))}
$$

控制器采用粗粒度特征提取器（1×1 卷积 + 池化至 5×5 网格）后接 MLP 回归头，模拟真实相机的自动曝光（AE）和自动白平衡（AWB）机制。训练目标为第一阶段优化得到的逐帧参数作为伪标签。这使得在测试新视角时，无需访问目标图像即可生成合理的 ISP 参数，实现完全自动化的新视角合成评估。

### 与基线的根本差异

相较于现有方法，PPISP 的框架设计具有本质区别：

- **GLO**（NeRF-W）使用逐帧隐向量直接补偿外观，缺乏物理可解释性，且无法泛化至新视角。
- **BilaRF** 采用逐像素仿射色彩变换，虽有一定灵活性，但参数化缺乏物理约束，且需要目标图像进行测试时对齐（PSNR-CC 协议）。
- **ADOP** 虽也包含曝光、白平衡、CRF 等模块，但其色彩校正采用简单的逐通道增益（Figure 6 左），与曝光耦合，导致在曝光控制时色彩伪影加剧（Figure 7）。PPISP 的色度单应性变换则实现了曝光与白平衡的有效解耦（Pearson 相关系数显著更低，Figure 6 右）。

PPISP 的物理合理参数化不仅增强了可解释性，还通过有限的模型容量有效抑制了过拟合——Table 5 显示，PPISP 在训练视图上的 PSNR 低于 BilaRF，但在新视图上显著更高，验证了其泛化优势。

### 补充图表

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a differentiable image processing pipeline applied to radiance field reconstruction. By modeling the behavior of conventional cameras, our approach disentangles image formation effects from the rest of the pipeline. Our physically-plausible model admits a controller module that predicts exposure and color changes for novel views*

## 核心模块与公式推导

PPISP的核心设计思想是将相机图像形成过程建模为一系列物理合理、可微分的后处理模块，作用于辐射场渲染的原始线性辐射度 $\mathbf{L}(\mathbf{r})$。整个管道由四个顺序级联的模块构成：曝光偏移、渐晕校正、色彩校正和相机响应函数（CRF），最后通过一个控制器预测每帧参数以实现新视角的自动适配。

### 4.1 曝光偏移模块

曝光是影响图像亮度的最显著因素。PPISP将曝光建模为对辐射度的一个全局、逐帧缩放：

$$ \mathbf{I}^{\exp} = \mathcal{E}(\mathbf{L}; \Delta t) = \mathbf{L} \cdot 2^{\Delta t} \tag{3} $$

其中 $\Delta t$ 是一个逐帧可学习的标量参数，以2为底的指数形式模拟相机的曝光值（EV）偏移。这一设计直接对应真实相机中曝光时间或ISO感光度的对数线性关系，使得参数具有明确的物理含义。在训练阶段，$\Delta t$ 与其他模块参数联合优化；在新视角合成时，控制器从渲染辐射度预测 $\Delta t$。

### 4.2 渐晕模块

渐晕是镜头边缘光衰减现象，表现为图像四角变暗。PPISP采用多项式径向衰减模型：

$$ v(r) = \text{clip}_{(0,1)}(1 + \alpha_1 r^2 + \alpha_2 r^4 + \alpha_3 r^6) \tag{5} $$

其中 $r$ 是像素到可优化光学中心 $\boldsymbol{\mu}$ 的归一化径向距离，$\alpha_1, \alpha_2, \alpha_3$ 是逐通道的衰减系数。该多项式被裁剪到 $[0,1]$ 区间以保证物理合理性。渐晕校正为逐传感器参数，在所有帧间共享：

$$ \mathbf{I}^{\text{vig}} = \mathcal{V}(\mathbf{I}^{\exp}; \boldsymbol{\mu}, \boldsymbol{\alpha}) = \mathbf{I}^{\exp} \cdot \mathbf{v}(r; \boldsymbol{\alpha}) \tag{4} $$

### 4.3 色彩校正模块

色彩校正的目标是补偿光源色温和传感器光谱响应的变化。PPISP采用基于色度坐标的单应性变换，并显式解耦强度与色度，避免白平衡调整与曝光偏移相互干扰。

首先将RGB值转换到色度-强度空间：

$$ \mathbf{C}(\mathbf{x}) = \left( \frac{R}{R+G+B}, \frac{G}{R+G+B} \right), \quad n(\mathbf{x}) = R+G+B \tag{6} $$

然后对色度坐标应用 $3 \times 3$ 单应性矩阵 $\mathbf{H}$，再恢复RGB：

$$ h(\mathbf{x}; \mathbf{H}) \doteq \mathbf{C}^{-1}\left( n(\mathbf{x}; \mathbf{H}) \cdot \left( \mathbf{H} \cdot \mathbf{C}(\mathbf{x}) \right) \right) \tag{8} $$

其中 $\mathbf{C}^{-1}$ 将色度-强度映射回RGB。该单应性由四个控制点（R、G、B、W）的偏移量参数化，保证变换的平滑性和可解释性。色彩校正参数为逐帧变量，反映不同拍摄条件下的白平衡变化。

### 4.4 相机响应函数模块

CRF描述传感器接收的辐照度到输出像素值的非线性映射。PPISP采用分段幂函数曲线，保证单调性和 $C^1$ 连续性：

$$ f_0(x; \tau, \eta, \xi) = \begin{cases} a \left( \frac{x}{\xi} \right)^{\tau}, & 0 \leq x \leq \xi \\ 1 - b \left( \frac{1 - x}{1 - \xi} \right)^{\eta}, & \xi < x \leq 1 \end{cases} \tag{14} $$

其中 $\xi$ 是分段点，$\tau$ 和 $\eta$ 分别控制暗部和亮部的曲线形状，$a$ 和 $b$ 由连续性条件确定。该参数化能够表达从线性到S形曲线的多种真实CRF形态。CRF为逐传感器参数，在所有帧间共享。

### 4.5 每帧ISP参数控制器

为实现无需目标图像的新视角评估，PPISP引入一个轻量级控制器 $\mathcal{T}$，从渲染辐射度 $\mathbf{L}$ 直接预测逐帧参数：

$$ \left( \Delta t, \{ \Delta \mathbf{c}_k \} \right) = \mathcal{T}(\mathbf{L}) \tag{17} $$

其中 $\Delta t$ 为曝光偏移，$\{ \Delta \mathbf{c}_k \}$ 为色彩校正控制点的偏移量。控制器采用粗粒度特征提取器（$1 \times 1$ 卷积池化至 $5 \times 5$ 网格）后接MLP回归头。训练分为两阶段：第一阶段联合优化辐射场和所有ISP模块参数（不含控制器）；第二阶段冻结其他模块，仅训练控制器，使其学习从场景辐射度到曝光和色彩参数的映射。这一设计模拟了真实相机的自动曝光和自动白平衡行为。

### 4.6 正则化约束

为保证优化的稳定性和物理合理性，PPISP施加四项正则化损失：

$$ \mathcal{L}_{\text{reg}} = \mathcal{L}_b + \mathcal{L}_c + \mathcal{L}_{\text{var}} + \mathcal{L}_{\text{vig}} \tag{22} $$

- **亮度正则化** $\mathcal{L}_b$：约束所有帧的平均曝光偏移接近零，防止辐射度场整体偏暗或偏亮。
- **色度正则化** $\mathcal{L}_c$：约束色彩校正矩阵接近单位变换，使辐射度场保持中性色彩。
- **方差正则化** $\mathcal{L}_{\text{var}}$：约束逐帧参数的方差，防止过拟合到个别帧的特殊光照。
- **渐晕正则化** $\mathcal{L}_{\text{vig}}$：约束渐晕系数接近零，优先假设均匀光照。

这些正则化项共同确保辐射度场学习到场景的真实物理属性，而非将光度变化“烘焙”进几何和材质表示中。

### 补充图表

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/003_Figure_3.jpg]]
*Figure 3: Dynamics of the controller module. The predicted exposure offset (inset) depends on the image content of the rendered radiance. Right side: Plot of exposure offsets as predicted for each frame of the caterpillar sequence, with the three displayed frames highlighted*

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/011_Figure_6.jpg]]
*Figure 6: Correlation between optimized exposure offset and white balancing variables in SMERF’s [8] alameda sequence. Left: ADOP’s [26] red and blue channel scaling. Right: The offsets of the white point of our homography-based correction. The Pearson correlation coefficient for each component is inset*

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/013_Figure_7.jpg]]
*Figure 7: Comparison of ADOP [26]-style post-processing including exposure control against our method. Row labels indicate the post-processing method and the sequence name (in italics). The CRF for ADOP’s formulation compensates for the color artifacts baked into the radiance field only at a specific exposure value. But when controlling exposure for novel views, color artifacts are exacerbated. In contrast, both our method’s radiance field and output remain neutral since all corrections are decoupled*

## 实验与分析

### 主结果：PPISP 在标准基准上的新视角合成性能

Table 1 汇总了 PPISP 在不同重建主干（3DGUT、GSplat、Zip-NeRF）和多个数据集上的表现。PPISP 配合控制器（w/ ctrl.）在绝大多数设置下取得最佳 PSNR、SSIM 和 LPIPS，且即使 BilaRF 享有目标图像色彩对齐的“特权”（PSNR-CC），PPISP 仍在多数数据集上超越该基线。例如，在 Mip-NeRF 360 上，3DGUT+PPISP（w/ ctrl.）达到 28.15 PSNR，相比 3DGUT+BilaRF 的 24.97 提升 3.18 dB；在 BILARF 数据集上，3DGS+PPISP（w/ ctrl.）以 25.39 PSNR 领先 3DGS+BilaRF 的 23.06。在 Tanks and Temples 上，PPISP（w/ ctrl.）取得 24.62 PSNR，远超 BilaRF 的 19.78（+4.84 dB）。

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/006_Table_1.jpg]]
*Table 1: Novel view synthesis results across methods and datasets. We compare appearance compensation methods applied on radiance field reconstruction methods. When the PPISP controller is omitted (w/o ctrl.), novel views use zero per-frame corrections. PSNR-CC factors out global exposure and color differences*

控制器预测的参数使 PSNR 接近甚至达到目标图像色彩对齐后的指标（PSNR-CC），表明其无需访问目标图像即可逼近传统相机的自动曝光与自动白平衡行为。当移除控制器（w/o ctrl.）时，新视角使用零校正，性能大幅下降，这验证了控制器在泛化到新视角时的核心作用。

### 消融实验：各物理模块的贡献

Table 2 在 Tanks and Temples 上对各 ISP 模块进行了消融。移除曝光偏移模块导致新视角 PSNR 从 24.62 降至 23.33（-1.29 dB），是影响最大的单一组件，凸显了全局曝光校正对重建一致性的关键作用。移除渐晕、色彩校正和 CRF 模块分别带来 0.54、0.35 和 0.26 dB 的 PSNR 下降，表明每个物理模块均对光度校正有独立贡献，且模块间的解耦设计是有效的。

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/005_Table_2.jpg]]
*Table 2: Component ablation of PPISP on the Tanks and Temples dataset for novel views (NV). Each row shows performance when removing the specified component*

### 元数据融合的增效

Table 3 展示了在 HDR-NeRF 数据集上利用相机元数据（如 EXIF）的效果。不提供元数据时，3DGUT+PPISP 的 PSNR 仅为 17.86；引入元数据后，PSNR 跃升至 34.30（+16.44 dB）。该结果表明 PPISP 的物理参数化可以无缝融合传感器侧信息，大幅提升在极端光度变化场景下的重建质量。

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/007_Table_3.jpg]]
*Table 3: Novel View PSNR across datasets with metadata. Our pipeline is able to leverage metadata (e.g. EXIF) from the sensor as a side data provided to the controller regressor*

### 容量与过拟合分析

Table 5 对比了不同 ISP 模块容量下训练视图（TV）与新视图（NV）的 PSNR。PPISP 有限的模型容量有效抑制了过拟合：训练视图 PSNR 低于 BilaRF，但新视图 PSNR 显著更高。这验证了物理合理约束的归纳偏置——通过限制校正模块的自由度，模型被迫学习更本质的辐射场表示，而非记忆训练视角的外观伪影。

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/009_Table_5.jpg]]
*Table 5: Average PSNR on the Tanks and Temples dataset comparing training views (TV) and novel views (NV) for ISP modules with varying capacity. The limited capacity of our proposed pipeline reduces overfitting and leads to better generalization*

### 渲染效率

Table 4 报告了在 Mip-NeRF 360 上的渲染开销。PPISP（w/ ctrl.）的额外开销为 0.84 ms（26%），低于 BilaRF 的 1.10 ms（36%），表明物理模块的轻量设计在计算效率上同样具有竞争力。

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/008_Table_4.jpg]]
*Table 4: Rendering times (ms) on NVIDIA RTX 5090 for the MipNeRF 360 [2] dataset*

### 与 ADOP 的解耦对比

Figure 7 揭示了曝光与色彩校正解耦的重要性。ADOP 风格的曝光控制将色彩伪影“烘焙”进辐射场，当在新视角调整曝光时，颜色失真被放大。相比之下，PPISP 的色度单应性变换将白平衡与曝光强度归一化解耦（Figure 6 中曝光偏移与白点偏移的 Pearson 相关系数显著低于 ADOP 的通道缩放），使得辐射场本身保持中性，曝光调整不会引入额外色偏。

### 失败模式与局限性

在 BilaRF 数据集上，PPISP 控制器的性能有所下降。该数据集包含大量手动设置覆盖的场景，控制器无法捕捉非自动的相机设置，导致预测参数与真实 ISP 行为失配。此外，当前校正模块均为全局或低维操作（曝光、渐晕、色彩单应性、CRF），无法建模空间变化的局部色调映射或高光压缩等复杂效果。在相机模型间迁移时，传感器特有参数（如渐晕多项式、CRF 曲线）可能需要重新校准。

### 补充图表

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/012_Table_6.jpg]]
*Table 6: Per-scene novel view PSNR comparison. We compare post-processing methods applied on top of 3DGUT reconstruction across all sequences. Higher is better (↑)*

![[assets/figures/papers/paper_list_l71_https_arxiv_org_abs_2601_18336/figures/017_Figure_10.jpg]]
*Figure 10: Our low-parametric formulation of the different image processing steps enables manual editing. Top left shows the input image. Other images have details overlaid, such as the primary effect being applied and an abstract visualization. In the color correction examples, the white dots correspond to the four target chromaticities*

## 方法谱系与知识库定位

### 辐射场外观建模的演进脉络

多视角3D重建中的光度不一致性问题长期困扰着神经辐射场（NeRF）类方法。早期的NeRF变体假设场景具有朗伯特反射特性且光照恒定，当输入图像来自不同相机或拍摄条件时，重建质量显著下降。**NeRF-W** (Martin-Brualla et al.) 率先引入逐帧隐式外观编码（GLO），通过学习与视角和位置无关的潜在向量来补偿外观变化。这一思路虽有效，但潜在空间缺乏物理可解释性，难以推广到训练分布外的新视角。

**BilaRF** (Mildenhall et al.) 进一步引入基于双边网格的逐像素仿射色彩校正，通过3D引导的局部变换实现了更精细的外观对齐。然而，仿射变换缺乏对相机成像物理过程的建模，其参数空间与真实的传感器行为脱节。**ADOP** (Rückert et al.) 则走向显式建模方向，将曝光、白平衡、相机响应函数（CRF）和渐晕作为后处理模块，但其CRF建模采用离散节点线性插值，且曝光与色彩校正的解耦不够充分——当在新视角下控制曝光时，已“烘焙”进辐射场的色彩伪影会被放大（见Figure 7）。

PPISP的核心定位是填补物理合理性与端到端可学习性之间的鸿沟。与GLO的隐式编码不同，PPISP的每个模块直接对应相机图像信号处理链中的可识别环节；与BilaRF的通用仿射变换不同，PPISP的色彩校正基于色度单应性变换，天然解耦了亮度与白平衡；与ADOP的离散CRF不同，PPISP采用分段幂函数曲线，在保证单调性和C1连续性的同时减少了参数冗余。

### 关键设计决策的因果机制

PPISP的效能根植于三个相互关联的设计选择：

1. **物理约束的容量控制**。PPISP将光度校正分解为曝光偏移（1个标量）、渐晕（每通道3个多项式系数）、色彩校正（4个色度偏移量）和CRF（4个形状参数）等低维模块。这种有限的模型容量并非缺陷，而是防止过拟合的关键机制——Table 5显示，PPISP在训练视图上的PSNR低于BilaRF，但在新视角上的PSNR显著更高（Tanks and Temples: 24.62 vs 19.78），说明物理约束有效抑制了对训练视图光度噪声的“记忆”。

2. **曝光与色彩的显式解耦**。色彩校正模块通过在RG色度空间施加单应性变换，并在变换前后进行亮度归一化和还原（Eq. 8），确保白平衡调整不会干扰曝光控制。Figure 6的Pearson相关系数分析证实了这一解耦效果：PPISP的白点偏移与曝光偏移的相关性（R通道0.06，B通道0.07）远低于ADOP的通道缩放系数（R通道0.42，B通道0.79）。

3. **控制器作为新视角泛化的桥梁**。PPISP控制器从渲染辐射图预测逐帧的曝光和色彩校正参数（Eq. 17），模拟真实相机的自动曝光和自动白平衡行为。Table 1显示，在多数数据集上，控制器预测的参数使PSNR接近甚至达到使用目标图像进行仿射色彩对齐后的指标（PSNR-CC），证明了其泛化能力。Figure 3进一步展示了控制器预测的曝光偏移随图像内容动态变化的定性行为。

### 适用边界与局限性

PPISP的物理合理性既是其优势来源，也划定了其适用边界：

- **手动设置覆盖的场景**。控制器假设相机参数遵循自动曝光/自动白平衡的统计规律。在BilaRF数据集上，PPISP的性能低于仿射色彩对齐（Table 1），因为该数据集包含手动曝光设置覆盖的场景，控制器无法捕捉这些非自动的相机行为。这是方法的内在局限，而非训练不足。

- **全局校正的粒度限制**。当前所有校正模块均为全局或低维空间操作（如渐晕的径向多项式）。对于空间变化的局部效应——如高光压缩、局部色调映射、传感器坏点校正——PPISP无法建模。这些效果需要更高维或空间自适应的校正机制。

- **传感器特定参数的迁移成本**。渐晕和CRF模块包含传感器固有属性参数（如光学中心、响应曲线形状）。当在不同相机模型间迁移时，这些参数可能需要重新校准。虽然PPISP支持从EXIF元数据中获取部分参数（Table 3显示元数据可将HDR-NeRF数据集上的PSNR从17.86提升至34.30），但在元数据不可用时，完全依赖优化的参数可能无法精确复现特定传感器的特性。

- **动态场景与复杂反射的鲁棒性未验证**。现有实验集中于静态场景，对于动态光照、移动物体或非朗伯特表面（如镜面反射）下的光度变化，PPISP的物理模型是否仍然充分尚未得到验证。

### 开放问题与未来方向

1. **空间变化校正的扩展**。如何在不牺牲物理可解释性的前提下，将PPISP扩展到局部色调映射、高光压缩等空间变化效应？可能的路径包括引入引导滤波器或轻量级空间自适应模块，但需谨慎控制容量以防止过拟合。

2. **极端新视角的控制器泛化**。当前控制器在训练视角附近表现良好，但在大幅旋转或场景区域不可见时，其预测的可靠性如何？可能需要引入不确定性估计或基于场景几何的控制器先验。

3. **无元数据的性能提升**。Table 3显示元数据带来显著增益，但在元数据不可用时（如用户上传的互联网图片），能否通过自监督学习或跨数据集先验来弥补？这涉及学习传感器行为的通用先验。

4. **与更高级表示的原生集成**。PPISP作为后处理模块与3DGUT、3DGS、Zip-NeRF等重建方法解耦，但这种松耦合可能限制端到端优化的潜力。能否将ISP校正嵌入到辐射场的隐式表示中，使渲染本身就对光度变化具有不变性？

5. **动态场景与视频重建**。将PPISP扩展到动态场景需要处理时变光照和运动模糊，这要求控制器能够区分场景内容的真实变化和相机参数的变化——一个具有挑战性的因果推断问题。

## 原文 PDF

![[paperPDFs/arxiv_2026/PPISP_Physically_Plausible_Compensation_and_Control_of_Photometric_Variations_in_Radiance_Field_Reconstruction.pdf]]