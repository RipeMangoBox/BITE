---
title: "OLATverse: A Large-scale Real-world Object Dataset with Precise Lighting Control"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OLATverse_A_Large_scale_Real_world_Object_Dataset_with_Precise_Lighting_Control.pdf
project_link: "https://vcai.mpi-inf.mpg.de/projects/OLATverse/"
code_link: null
aliases:
- OLATverse
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过光场台（lightstage）一次性采集 765 个真实物体的 35 视角、331 单独可控光源的 OLAT 图像，提供标定参数、掩码、法线、漫反射反照率等辅助数据，构成大规模综合基准，从而推动数据驱动方法向真实世界迁移。
primary_logic: 利用线性光传输的可叠加性，OLAT 图像可以重组成任意新光照下的外观，使得数据集不仅能作为多任务（逆渲染、重光照、新视角合成、法线估计）的评估基准，也能通过重光照合成扩展为大规模生成式先验的训练资源。
claims:
- OLATverse 包含约 9M 张图像，765 个真实物体，覆盖超过 18.5% 的 LVIS 类别，大幅超越现有真实 OLAT 数据集（如 OpenIllumination 仅 64 物体）。
- 每个物体使用 35 台 DSLR 相机和 331 个独立控制光源，提供精确光照条件（包括均匀光、OLAT、环境光、梯度偏振光）和丰富的辅助数据（标定参数、掩码、法线、漫反射反照率）。
- 半自动掩膜管道结合 bgMatting、SAM 和 RMBG-2.0，在所有物体和视角上达到 95% 成功率。
- 相机标定的平均重投影误差为 0.86 像素，确保多视角一致性。
---

# OLATverse: A Large-scale Real-world Object Dataset with Precise Lighting Control

> [!tip] 核心洞察
> 利用线性光传输的可叠加性，OLAT 图像可以重组成任意新光照下的外观，使得数据集不仅能作为多任务（逆渲染、重光照、新视角合成、法线估计）的评估基准，也能通过重光照合成扩展为大规模生成式先验的训练资源。

| 字段 | 内容 |
|------|------|
| 中文题名 | OLATverse：一个具有精确光照控制的大规模真实世界物体数据集 |
| 英文题名 | OLATverse: A Large-scale Real-world Object Dataset with Precise Lighting Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.02483) · [Project](https://vcai.mpi-inf.mpg.de/projects/OLATverse/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | OLATverse |
| Dataset | OLATverse validation set |

> [!tip] 效果简介
> - OLATverse validation set (inverse rendering) 上，PSNR 38.538 (GS³) vs 27.903 (Mitsuba, Tab.2) (+10.635)；LPIPS 0.0263 (GS³) vs 0.0807 (Mitsuba, Tab.2) (-0.0544)；SSIM 0.982 (GS³) vs 0.934 (Mitsuba, Tab.2) (+0.048)。
> - OLATverse validation set (normal estimation) 上，Mean Angular Error 31.85 (SN) vs 43.27 (DR, Tab.3) (-11.42)；Median Angular Error 30.25 (SN) vs 40.53 (DR, Tab.3) (-10.28)。

## 概述

物体级别的逆渲染与重光照是视觉计算中长期存在的挑战。现有方法严重依赖合成数据训练，而真实世界数据集要么规模过小（如 OpenIllumination 仅 64 个物体），要么缺乏精确可控的多光照条件，导致模型在真实场景中的泛化能力显著受限。根本瓶颈在于缺少一个同时满足大规模、真实物体多样性、高保真外观以及精确多光照标注的数据基准。

针对这一缺口，本文提出 **OLATverse**——首个公开发布的大规模真实世界 OLAT 数据集。OLATverse 包含约 **9M 张图像**，覆盖 **765 个真实物体**，涵盖超过 **18.5% 的 LVIS 类别**，在规模上远超现有同类数据集。每个物体通过 35 台 DSLR 相机和 331 个独立控制光源进行采集，提供均匀光、OLAT、环境光及梯度偏振光等多种精确光照条件，并附带标定相机参数、物体掩码、光测表面法线和漫反射反照率等辅助数据。

其核心洞见在于：利用线性光传输的可叠加性，OLAT 图像可被重组成任意新光照下的物体外观。这使得 OLATverse 不仅能作为多任务评估基准（逆渲染、重光照、新视角合成、法线估计），还可通过重光照合成扩展为大规模生成式先验的训练资源。

在方法谱系上，OLATverse 本身是一个数据集贡献，但其设计直接服务于数据驱动的逆渲染与重光照方法。与依赖合成渲染的 **Mitsuba**（Jakob 等, 2010）或仅提供有限光照的 **OpenIllumination**（Liu 等, 2024）不同，OLATverse 通过真实采集与精确光场控制，为 **GS³**（Gao 等, 2024）、**BiGS**（Cao 等, 2024）、**RNG**（Gao 等, 2024）等新一代逆渲染方法提供了真实世界验证平台。在法线估计任务上，它也为 **StableNormal**（Ye 等, 2024）、**GeoWizard**（Fu 等, 2024）等前沿方法提供了多光照条件下的评估基准。

主要实验结果验证了数据集的有效性：在逆渲染任务上，当前最优方法 GS³ 在 OLATverse 验证集上达到 PSNR 38.538、SSIM 0.982、LPIPS 0.0263，相比传统可微路径追踪器 Mitsuba（PSNR 27.903）提升显著；在法线估计任务上，StableNormal 在四组不同光照输入下取得 31.85° 的平均角度误差，优于 DiffusionRender 的 43.27°。这些结果初步表明，OLATverse 能够有效区分不同方法的真实世界性能差异，为领域发展提供了关键的数据支撑。

需注意，法线真值源自偏振梯度照明估算而非几何扫描，可能引入系统性偏差；数据集规模（765 物体）对长尾类别的覆盖仍有限。这些限制为后续工作留下了明确的改进空间。

## 背景与动机

### 物体中心逆渲染与重光照的现状

从单目或多视角图像中恢复物体的几何、材质与光照属性——即逆渲染——并在此基础上合成任意新光照下的逼真外观——即重光照——是计算机视觉与图形学中长期存在的核心挑战。这一技术栈在增强现实、虚拟试穿、影视特效及具身智能等应用中具有广泛前景。近年来，基于神经辐射场、3D 高斯泼溅及扩散先验的方法在逆渲染与重光照任务上取得了显著进展，但一个根本性瓶颈始终制约着这些方法向真实世界迁移的能力：**缺乏同时满足大规模、真实物体多样性、高保真外观以及精确可控多光照条件的数据集**。

现有物体中心数据集可大致分为三类。第一类为合成数据集，如 ShapeNet、Objaverse 等，虽规模庞大，但渲染外观与真实世界存在难以弥合的域间隔。第二类为混合数据集，如 OmniObject3D，包含约 6000 个真实物体扫描，但缺乏精确的光照控制与逐光源标定。第三类为真实光照控制数据集，最具代表性的是 **OpenIllumination**，但其仅包含 64 个物体，远不足以支撑数据驱动的逆渲染方法训练与泛化评估。更关键的是，这些数据集大多不提供或仅提供有限的辅助真值——如标定相机参数、精确物体掩码、表面法线与漫反射反照率——而这些正是逆渲染方法训练与评估所必需的监督信号。

### 核心瓶颈：规模、真实性与光照控制的三角缺失

上述现状揭示了一个清晰的“不可能三角”：现有数据集难以同时满足**大规模物体覆盖**、**真实世界外观保真**与**精确可控多光照条件**三者。合成数据可无限扩展但缺乏真实感；真实扫描数据虽具真实外观但光照条件不可控或极度稀疏；而小规模光场台数据虽提供精确光照，但物体数量不足以覆盖材质与类别的长尾分布。这一缺口直接导致逆渲染与重光照方法在真实场景中的泛化能力严重受限——在合成数据上训练的方法在真实图像上往往产生明显的材质失真与光照伪影。

### OLAT 范式与线性光传输的优势

一次点亮一个光源（One-Light-at-a-Time，OLAT）的采集范式为突破上述瓶颈提供了理论基础。基于光传输的线性可叠加性，OLAT 图像可以通过加权求和重组成任意新光照下的物体外观：

$$\mathbf{I}_{\mathrm{relit}} = \sum_{i=1}^{N_{\mathrm{olat}}} \left( \mathcal{F}( \mathbf{E} \odot \mathbf{M}_{\mathrm{i}} ) \cdot \mathbf{I}_{\mathrm{i}} \right)$$

其中 $\mathbf{E}$ 为目标环境光照，$\mathbf{M}_i$ 为第 $i$ 个光源的可见性掩码，$\mathbf{I}_i$ 为对应的 OLAT 图像，$\mathcal{F}$ 为下采样函数。这意味着，一个完整采集的 OLAT 数据集不仅是逆渲染与重光照的评估基准，其本身也可通过重光照合成扩展为大规模生成式先验的训练资源——前提是该数据集在物体数量、材质多样性与采集质量上达到足够规模。

### 本文动机与贡献定位

基于上述分析，本文的核心动机是：**填补大规模真实世界 OLAT 数据集的空白，为数据驱动的逆渲染与重光照方法提供一个兼具规模、真实感与精确光照控制的综合基准与训练平台**。具体而言，OLATverse 数据集包含约 900 万张图像，覆盖 765 个真实物体，横跨超过 18.5% 的 LVIS 类别，每个物体在 35 个标定相机视角下采集了 331 个独立控制光源的 OLAT 图像，并配套提供相机参数、物体掩码、光测表面法线与漫反射反照率。这一规模远超现有最大真实 OLAT 数据集 OpenIllumination（64 物体），为逆渲染、重光照、新视角合成与法线估计等任务提供了迄今最全面的真实世界评估基准。

## 核心创新

OLATverse 的核心创新不在于提出新的算法架构，而在于**构建了首个大规模、真实世界、精确光照可控的物体数据集**，从根本上改变了物体中心逆渲染与重光照研究的评估与训练范式。其关键创新可归纳为三个维度的“changed slots”。

### 数据集规模与真实多样性

现有真实 OLAT 数据集规模极为有限。**OpenIllumination**（CVPR 2024）仅包含 64 个物体，而合成数据集 **OmniObject3D**（CVPR 2023）虽有约 6K 物体，却缺乏精确的光照控制。OLATverse 将真实物体数量提升至 **765 个**，覆盖超过 **18.5% 的 LVIS 类别**，包含约 **9M 张图像**，在规模上实现了一个数量级的跨越（对比 OpenIllumination 的 64 物体）。这一规模优势使数据集不仅可作为评估基准，还具备支撑生成式先验训练的潜力。

### 精确可控的多光照条件

现有数据集通常仅提供少数环境光照或无光照控制。OLATverse 为每个物体采集 **331 个独立可控光源的 OLAT 图像**，外加均匀白光、12 组偏振梯度光照和 10 组环境光照。这一设计的因果杠杆在于**线性光传输的可叠加性**：OLAT 图像可以按任意权重重组成新光照下的物体外观（重光照合成公式 $\mathbf{I}_{\mathrm{relit}} = \sum_{i=1}^{N_{\mathrm{olat}}} \left( \mathcal{F}( \mathbf{E} \odot \mathbf{M}_{\mathrm{i}} ) \cdot \mathbf{I}_{\mathrm{i}} \right)$），使得数据集天然支持无限光照条件下的评估与数据增广。

### 多模态辅助真值

多数现有数据集不提供或仅提供有限的辅助标注。OLATverse 为每个物体提供了**标定相机参数**（平均重投影误差 0.86 px）、**精确物体掩码**（半自动管道成功率 95%）、**光测表面法线**和**漫反射反照率**。其中法线和反照率通过偏振梯度照明技术计算（$\mathbf{D} = 0.5 ( \mathbf{I}_{\perp}^{+} + \mathbf{I}_{\perp}^{-} )$；$\mathbf{N}^{*} = \frac{ ( \mathbf{I}^{+} - \mathbf{I}^{-} ) }{ ( \mathbf{I}^{+} + \mathbf{I}^{-} ) }$），使数据集可同时支撑逆渲染、重光照、新视角合成和法线估计等多任务的统一评估。

### 创新边界与待验证假设

需注意以下限制：法线真值来自偏振梯度照明的**估算而非几何扫描真值**，在高光泽或低反照率物体上可能引入系统性偏差；数据集规模（765 物体）仍可能不足以覆盖长尾类别；缺少真实几何/深度真值限制了某些依赖几何重建的逆渲染方法的闭环评估。这些限制是否会在更大规模扩展或联合几何扫描后被突破，仍需后续工作验证。

## 整体框架

OLATverse 的数据生成与评估框架围绕“一次采集、多任务复用”的理念构建，其核心 pipeline 由四个顺序模块组成：**相机与灯光标定** → **半自动掩膜分割** → **法线与漫反射反照率提取** → **重光照合成**。各模块之间的输入输出流如下所述。

**输入与采集阶段**。每个物体被放置在光场台（lightstage）中，由 35 台固定位置的 DSLR 相机和 331 个独立可控 LED 光源进行同步采集。采集过程依次记录均匀白光、12 组偏振梯度照明、10 种预定义环境光照以及 331 组逐一激活的单光源（OLAT）图像，每个物体最终产生约 12K 张原始图像。相机与光源的几何配置通过定期标定维护：每 20–30 次常规采集后，使用纹理丰富的参考物体配合 **Metashape** 进行相机标定，平均重投影误差为 **0.86 像素**（Figure 5 展示了标定后相机、光源与物体网格的空间一致性）。

**掩膜生成模块**。原始图像包含物体、木质支架及背景。框架采用半自动分割管道生成两类掩膜：支架掩膜与物体掩膜。对于低视角相机（视野中包含大量支架），直接使用 **SAM** 分割背景图像获得支架掩膜；对于其他视角，则结合 **bgMatting**、**SAM** 和 **RMBG-2.0** 的级联策略（见公式 `M_stup`）。物体掩膜由前景图像的 SAM 分割结果减去支架掩膜得到（`M_obj* = M_2(I_fg) · (1 - M_stup)`），再经形态学后处理细化。该管道在所有物体和视角上的成功率达到 **95%**（Figure 6 定性对比了各中间步骤的掩膜质量）。

**法线与反照率提取模块**。利用偏振梯度照明下的双向亮度关系计算辅助真值。漫反射反照率 **D** 由正交极化的满亮照明图像均值得到：`D = 0.5 (I_⟂⁺ + I_⟂⁻)`。表面法线 **N** 基于相反梯度方向的照明图像对计算：`N* = (I⁺ - I⁻) / (I⁺ + I⁻)`，再归一化为单位向量 `N = N* / |N*|`。需注意，此法线为光度法估算的伪真值，并非几何扫描真值，在高光泽或低反照率物体上可能引入伪影。

**重光照合成与应用接口**。OLAT 图像的可叠加性使得任意新环境光照下的物体外观可通过加权求和合成：`I_relit = Σᵢ (F(E ⊙ Mᵢ) · Iᵢ)`，其中 E 为目标环境图，Mᵢ 为第 i 个光源的方向掩膜，F 为下采样函数。这一机制将数据集从静态基准扩展为生成式先验的训练资源。框架最终输出多模态数据包：每个物体包含 35 视角 × 331 OLAT 图像、10 种重光照图像、精确掩膜、表面法线及漫反射反照率（Figure 4 展示了单物体的完整数据样本），可直接服务于逆渲染、新视角合成、法线估计等下游任务的训练与评估。

**模块间的依赖关系**。标定模块为所有后续处理提供相机内外参和光源方向；掩膜模块为法线/反照率提取限定有效像素区域，也为重光照合成提供前景遮罩；法线与反照率作为逆渲染任务的辅助监督信号或评估真值。四个模块呈严格串行依赖，前序误差会向后传播——例如标定漂移会影响多视角一致性，掩膜边缘误差会污染法线提取结果。

### 补充图表

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/006_Figure_3.jpg]]
*Figure 3: Illustration of the dataset capture setup and process pipeline. We utilize wooden stands with varying sizes and (a) a lightstage setup to capture raw videos of objects. During the calibration session, we record (b) reference objects to extract accurate camera parameters, which are utilized to extract (c) undistorted OLALs and relit images under varying illuminations from raw videos. Next, we capture (d) background stand image and perform (e) semi-automatic mask segmentation and normal extraction for each object*

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/005_Figure_4.jpg]]
*Figure 4: We visualize one sample of OLATverse, which includes full bright (FB), OLATs, relit images under varying pre-defined environmental illuminations (ENV), object mask, surface normals, and diffuse albedo*

## 核心模块与公式推导

OLATverse 的数据生成流程围绕四个核心模块展开：相机与灯光标定、半自动掩膜分割、法线与漫反射反照率提取，以及重光照合成。以下逐一阐述其关键机制与公式。

### 相机与灯光标定

为确保多视角一致性，系统利用光场台固定相机配置，每 20–30 次常规采集后进行一次标定会话。标定过程使用纹理丰富的参考物体，并借助 **Metashape** 中的特征匹配算法解算相机内外参数，最终平均重投影误差为 **0.86 像素**。灯光位置则通过物理测量确定，与相机参数联合构成精确的光传输先验。

### 半自动掩膜分割

掩膜生成采用分层策略，根据相机视角高度分情况处理。对于较低视角的相机，直接对背景图像 $\mathbf{I}_{\mathrm{bg}}$ 应用 **SAM**（记为 $\mathbf{M}_2$）获得支架掩膜；对于其余视角，则先通过 **bgMatting**（记为 $\mathbf{M}_1$）融合前景 $\mathbf{I}_{\mathrm{fg}}$ 与背景 $\mathbf{I}_{\mathrm{bg}}$ 生成初始支架蒙版，再经 **RMBG-2.0**（记为 $\mathbf{M}_3$）精修，最终与 SAM 结果融合。支架掩膜的计算形式为：

$$
\mathbf{M}_{\mathrm{stup}} = \begin{cases}
\mathbf{M}_2(\mathbf{I}_{\mathrm{bg}}) & \text{低视角相机} \\
\mathbf{M}_2(\mathbf{I}_{\mathrm{bg}}) \left[1 - \mathbf{M}_3\!\left(\mathbf{M}_1(\mathbf{I}_{\mathrm{bg}}, \mathbf{I}_{\mathrm{fg}})\right)\right] & \text{其余视角}
\end{cases}
$$

获得支架掩膜后，从前景图像中减去支架区域得到初始物体掩膜：

$$
\mathbf{M}_{\mathrm{obj}}^{*} = \mathbf{M}_2(\mathbf{I}_{\mathrm{fg}}) \left(1 - \mathbf{M}_{\mathrm{stup}}\right)
$$

随后通过形态学后处理消除孔洞与边缘噪声，形成最终物体掩膜。该管道在所有物体和视角上达到 **95% 成功率**。

### 法线与漫反射反照率提取

本模块基于偏振梯度照明技术，利用正交极化状态下相反梯度方向的照明图像对，恢复表面法线与漫反射反照率。具体地，漫反射反照率 $\mathbf{D}$ 由正交极化的满亮照明图像 $\mathbf{I}_{\perp}^{+}$ 与 $\mathbf{I}_{\perp}^{-}$ 的均值给出：

$$
\mathbf{D} = 0.5 \left( \mathbf{I}_{\perp}^{+} + \mathbf{I}_{\perp}^{-} \right)
$$

表面法线则通过相反梯度方向照明图像对 $\mathbf{I}^{+}$ 与 $\mathbf{I}^{-}$ 的差分与求和之比计算，并经归一化得到单位法向量：

$$
\mathbf{N}^{*} = \frac{ \mathbf{I}^{+} - \mathbf{I}^{-} }{ \mathbf{I}^{+} + \mathbf{I}^{-} }, \quad \mathbf{N} = \frac{ \mathbf{N}^{*} }{ |\mathbf{N}^{*}| }
$$

此处 $\mathbf{I}^{+}$ 与 $\mathbf{I}^{-}$ 分别对应梯度方向相反的两幅照明图像，$\mathbf{N}^{*}$ 为未归一化的法线估计。该方法的物理基础是漫反射表面在相反梯度照明下的亮度差异直接编码表面朝向信息。需注意，法线真值为偏振梯度照明估算的伪真值，对高光泽或低反照率物体可能产生伪影。

### 重光照合成

基于线性光传输的可叠加性，任意新环境光照下的物体外观可通过 OLAT 图像的加权求和合成。给定目标环境光照 $\mathbf{E}$，将其与每个 OLAT 光源的掩膜 $\mathbf{M}_i$ 逐元素相乘后经函数 $\mathcal{F}$ 调制得到权重，再与对应 OLAT 图像 $\mathbf{I}_i$ 加权求和：

$$
\mathbf{I}_{\mathrm{relit}} = \sum_{i=1}^{N_{\mathrm{olat}}} \left( \mathcal{F}( \mathbf{E} \odot \mathbf{M}_i ) \cdot \mathbf{I}_i \right)
$$

其中 $\mathcal{F}$ 将环境光在光源方向上的辐照度映射为标量权重，$\odot$ 表示逐元素乘积。这一模块使 OLATverse 不仅能作为多任务评估基准，还能通过重光照合成扩展为大规模生成式先验的训练资源。

### 补充图表

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of calibrated cameras (marked as red), light sources (marked as green) and object mesh in our capture setup. In the left part of the figure, the reconstructed mesh decently matches the original image, demonstrating the correctness of the calibration process*

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/008_Figure_6.jpg]]
*Figure 6: Semi-automatic mask processing. We show the object masks generated by SAM, bgMatting, RMGB-2.0 as well as our final mask produced by our proposed mask segmentation strategy*

## 实验与分析

### 逆渲染评估

为验证 OLATverse 作为真实世界逆渲染基准的有效性，作者在验证集上评估了四种代表性方法：基于可微路径追踪的 **Mitsuba** 、基于 3D Gaussian Splatting 的 **GS³** 、双向高斯原语方法 **BiGS**，以及可重光照神经高斯 **RNG**。评估指标包括 PSNR、SSIM 和 LPIPS，结果汇总于 Table 2。

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/011_Table_2.jpg]]
*Table 2: Numerical comparison of inverse rendering baselines on our validation dataset using PSNR, LPIPS, and SSIM metrics*

GS³ 在所有指标上均显著领先，PSNR 达 38.538，LPIPS 低至 0.0263，SSIM 为 0.982。相比之下，Mitsuba 的 PSNR 仅为 27.903，LPIPS 为 0.0807，SSIM 为 0.934。GS³ 相对于 Mitsuba 的 PSNR 提升超过 10.6 dB，LPIPS 降低约 67%，表明基于高斯泼溅的显式表示在真实世界多光照条件下的逆渲染任务中具有明显优势。

定性结果（Figure 7）进一步揭示了各方法的失败模式：Mitsuba 在光泽表面（如金属兔、塑料路障）上难以重建精确的高光反射，渲染结果模糊；BiGS 和 RNG 虽能部分恢复高光，但在新视角下出现几何伪影和纹理失真。GS³ 则准确捕捉了西瓜表面的镜面反射细节和金属兔的复杂光照交互，验证了其作为当前最佳逆渲染方法在此基准上的代表性地位。

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/009_Figure_7.jpg]]
*Figure 7: We visualize the inverse rendering and novel view synthesis results of several baseline methods (Mitsuba [39]*

### 法线估计评估

表面法线估计是 OLATverse 提供的另一核心辅助任务。验证集上的法线真值通过偏振梯度照明估算获得（非几何扫描真值，需注意此系统性偏差）。作者评估了四种法线估计方法：**DiffusionRender (DR)** 、**RGB↔X (RGBX)** 、**StableNormal (SN)** 和 **GeoWizard (GW)**，采用平均角度误差和角度误差中位数作为指标（Table 3）。

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/012_Table_3.jpg]]
*Table 3: Numerical comparison of normal estimation methods on our validation dataset using normal angular metrics*

StableNormal 表现最优，平均角度误差为 31.85°，中位数误差为 30.25°。DiffusionRender 最差，平均误差达 43.27°，中位数误差 40.53°。StableNormal 相对于 DiffusionRender 的平均误差降低约 11.4°，降幅约 26%。GeoWizard 与 StableNormal 性能接近，两者作为专为法线估计设计的方法，显著优于通用图像到 3D 转换的 RGBX 和 DiffusionRender。

定性对比（Figure 8）显示，DiffusionRender 和 RGBX 在物体边缘和复杂几何区域产生明显噪声，而 StableNormal 和 GeoWizard 恢复的法线方向更平滑、与伪真值更一致。然而，所有方法在低反射率或高光泽区域（如黑色塑料、金属表面）均出现不同程度的偏差，这与此类区域偏振法线提取本身存在伪影有关。

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/010_Figure_8.jpg]]
*Figure 8: Visual comparison of pseudo ground truth normals with normals estimated by DR [30], RGBX [62], SN [59] and GW [15]. To ensure a robust and generalized comparison, we provide input images of each validation object under four different illuminations*

### 数据集规模效应的间接证据

虽然论文未进行严格的消融实验，但 Table 1 的对比数据提供了规模效应的间接证据：OLATverse 覆盖超过 18.5% 的 LVIS 类别（765 个物体），而同期最大的真实 OLAT 数据集 OpenIllumination 仅含 64 个物体，类别覆盖率约 4–5%。GS³ 在 OLATverse 上的优异表现暗示，更大规模、更多样的真实光照数据有助于数据驱动方法学习更鲁棒的外观表示。但这一推论需手动验证——论文未直接对比不同训练数据规模下的性能变化。

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/002_Table_1.jpg]]
*Table 1: Comparison of object-centric datasets targeting inverse rendering and relighting tasks. We list a detailed comparison of OLATverse with existing datasets across several key attributes. The compared aspects include number of object (# Objs), whether data source is real (Real), lighting conditions (IllumCond), number of illuminations (# Illum), number of views (# Views), and capture device (Device). In the column of IllumCond, ENV denotes environment illumination, PAT represents pattern illumination. Unspec. indicates that the corresponding information is not specified in the dataset. () indicates that only a small portion of the dataset satisfies the criterion*

### 失败模式与局限性

实验揭示的失败模式集中在三个层面：
1. **逆渲染方法**：Mitsuba 等基于物理的方法在光泽材质上重建不足；高斯类方法虽整体更优，但在极端新视角下仍可能出现几何坍塌。
2. **法线估计**：所有方法在低反照率或高光泽表面误差增大，这与法线真值本身的提取伪影形成复合误差源。
3. **基准本身**：法线真值来自偏振估算而非几何扫描，可能系统性地低估或扭曲某些材质类别的误差。

### 关键图表结论

- **Table 1**：OLATverse 在物体数量、光照条件丰富度和辅助数据完整性上全面超越现有物体中心数据集。
- **Table 2**：GS³ 以 PSNR 38.538 / LPIPS 0.0263 / SSIM 0.982 显著领先，确立为当前真实世界逆渲染的强基线。
- **Table 3**：StableNormal 以平均角度误差 31.85° 居首，但所有方法在挑战性材质上仍有较大提升空间。
- **Figure 7**：GS³ 在光泽和复杂几何物体上展现最佳视觉质量，Mitsuba 高光重建不足。
- **Figure 8**：法线估计的定性失败集中在物体边缘和高光区域，与数值结果一致。

### 补充图表

![[assets/figures/papers/paper_list_l2099_https_arxiv_org_abs_2511_02483/figures/003_Figure_2.jpg]]
*Figure 2: (a) We visualize the statistics of OLATverse, including the material distribution and high-level object category distribution. (b) We also show comparison against OpenIllumination [33] for the six largest material and object categories in terms of object count*

## 方法谱系与知识库定位

### 1. 任务定位与核心瓶颈

OLATverse 定位为**物体中心逆渲染与重光照**任务的基准数据集与训练资源。该领域长期受困于一个根本性瓶颈：现有方法严重依赖合成数据训练（如 Blender、Mitsuba 渲染的合成物体），而在小规模真实数据基准上评估时，真实感与泛化能力显著不足。造成这一鸿沟的关键在于，此前缺乏一个同时满足以下三个条件的数据集：

1. **大规模**：覆盖足够多的真实物体，支撑数据驱动方法的训练与统计显著性评估。
2. **真实物体多样性**：涵盖丰富的材质、几何形状与语义类别，避免合成数据的域偏差。
3. **精确可控的多光照条件**：提供逐光源独立控制的 OLAT（One-Light-at-a-Time）图像，使得光照可自由重组，而非仅提供少数固定环境光。

OLATverse 通过一次性采集 765 个真实物体的 35 视角、331 个单独可控光源的 OLAT 图像，直接回应了这一瓶颈。其核心因果机制在于：利用线性光传输的可叠加性，OLAT 图像可以被重组成任意新光照下的外观，这使得数据集不仅能作为多任务评估基准，还能通过重光照合成扩展为大规模生成式先验的训练资源。

### 2. 与现有数据集的关系

表 1 给出了物体中心数据集的系统对比。OLATverse 在真实数据规模、光照控制精度和辅助数据完备性三个维度上，与现有数据集形成了清晰的差异化定位。

**相对于真实 OLAT 数据集**：此前最大的真实 OLAT 数据集 **OpenIllumination**（2024）仅包含 64 个物体，OLATverse 以 765 个物体实现了一个数量级的超越。在 LVIS 类别覆盖率上，OLATverse 超过 18.5%，而 OpenIllumination 仅覆盖约 4–5%，**OmniObject3D**（2023）尽管拥有约 6K 物体，但缺乏精确光照控制。

**相对于合成/混合数据集**：**Objaverse**（2023）、**ABO**（2021）等大规模合成数据集虽在数量上占优，但其材质与光照的物理真实感存疑，导致在此类数据上训练的方法向真实场景迁移时性能退化明显。OLATverse 的真实数据属性使其成为验证合成数据训练方法泛化能力的理想试金石。

**辅助数据的差异**：多数现有数据集不提供或仅提供有限的辅助标注。OLATverse 提供标定相机参数（平均重投影误差 0.86 px）、精确物体掩膜（半自动管道 95% 成功率）、基于偏振梯度照明的光测表面法线与漫反射反照率，这些辅助数据使 OLATverse 能支撑逆渲染、法线估计、新视角合成等多任务的统一评估。

### 3. 与逆渲染/重光照方法的关系

OLATverse 本身不提出新的逆渲染或重光照算法，而是作为**评估平台与训练资源**嵌入现有方法谱系。论文在验证集上评测了四类代表性逆渲染方法：

- **Mitsuba**（Jakob et al., 2022）：基于可微路径追踪的物理逆渲染方法，作为传统优化范式的代表。
- **GS³**（Gao et al., 2024）：基于 3D Gaussian Splatting 的逆渲染方法。
- **BiGS**（2024）：采用双向高斯原语的逆渲染方法。
- **RNG**（Gao et al., 2024）：可重光照神经高斯方法。

评测结果显示，GS³ 在 PSNR（38.538）、LPIPS（0.0263）和 SSIM（0.982）上均显著优于其他方法（如 Mitsuba 的 PSNR 为 27.903，LPIPS 为 0.0807），且在光泽表面（西瓜、金属兔、塑料路障）上能准确捕捉镜面反射。这一结果并非对 GS³ 的背书，而是揭示了当前逆渲染方法在真实数据上的性能排序与相对差距，为后续方法改进提供了量化参照。

### 4. 与法线估计方法的关系

OLATverse 提供的法线图基于偏振梯度照明估算（遵循 Ma et al. 的技术路线），属于**光测伪真值**而非几何扫描真值。论文评测了四种法线估计方法：

- **DiffusionRender (DR)**（2023）
- **RGB↔X (RGBX)**（2023）
- **StableNormal (SN)**（2024）
- **GeoWizard (GW)**（2024）

结果显示，专为法线估计设计的 SN 和 GW 显著优于通用图像翻译方法 DR 和 RGBX，其中 SN 取得最低的平均角度误差（31.85°）和中值角度误差（30.25°）。这一定量对比揭示了当前法线估计方法在真实物体上的绝对性能水平（角度误差仍在 30° 以上），表明该任务仍有显著提升空间。

### 5. 适用边界与局限

OLATverse 的适用边界受以下因素制约：

1. **法线真值的系统性偏差**：法线提取对高光泽或低反照率物体可能产生伪影，且其真值来自偏振梯度照明估算，而非几何扫描。这限制了依赖精确几何真值的逆渲染方法的闭环评估可靠性。
2. **标定漂移**：相机标定精度虽高（0.86 px），但随时间可能漂移，需每 20–30 次采集会话重新标定。对于需要极高几何一致性的任务，这一漂移可能引入误差。
3. **规模仍有限**：765 个物体虽远超现有真实数据集，但相对于合成数据集（如 Objaverse 的百万级）仍显不足，可能限制生成式预训练的充分性，尤其对长尾类别。
4. **缺少几何/深度真值**：数据集不提供真实的几何模型或深度图，限制了某些依赖精确几何重建的逆渲染方法（如可微渲染中的网格优化）的端到端评估。
5. **采集设备的可复现性**：数据采集依赖特定的光场台硬件（35 台 DSLR + 331 光源），其他研究团队难以完全复现相同的采集条件来扩展数据集。

### 6. 开放问题

OLATverse 的发布为以下研究问题提供了实证基础：

1. **法线提取鲁棒性**：如何减少在光泽或低反射物体上的法线提取伪影？是否可能结合深度学习先验改进偏振梯度照明的法线估算？
2. **联合几何-外观真值**：能否将先进 3D 扫描（如结构光或激光扫描）集成到采集流程中，以获取与外观数据配准的几何真值，从而支持更全面的逆渲染评估？
3. **生成式先验训练**：OLATverse 的重光照合成能力能否激发结合真实多光照数据的生成式先验训练（如扩散模型或神经辐射场的预训练），并进一步提升逆渲染和重光照在未知物体上的泛化能力？
4. **任务边界拓展**：该数据集是否适用于更复杂的下游任务，如物体材质编辑、多物体组合重光照、或作为真实世界光照估计的校准基准？
5. **规模扩展策略**：如何在保持光照控制精度的前提下，以更低成本扩展数据集规模？半自动化采集管道或合成-真实混合增强是否可行？

## 原文 PDF

![[paperPDFs/CVPR_2026/OLATverse_A_Large_scale_Real_world_Object_Dataset_with_Precise_Lighting_Control.pdf]]
