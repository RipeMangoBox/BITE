---
title: Rethinking Glyph Spatial Information in Font Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_Glyph_Spatial_Information_in_Font_Generation.pdf
project_link: null
code_link: "https://github.com/sp777g/GlyphSpatialNet"
aliases:
- GSS
- RGSIFG
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 显式建模并保留字形空间信息：通过空间保留渲染（SPR）方案消除空间偏差，并设计GlyphSpatialNet解耦形状与位置。
primary_logic: 在像素空间中显式解耦形状与位置，并采用从设计空间到像素空间的精确渲染映射，可以消除空间偏差，实现高保真矢量化，从而在无需组件标签的情况下大幅提升字体生成质量。
claims:
- "SPR方案使扩散模型的性能显著提升：在UFSC 8-shot设置下，N[L1]从0.2922降至0.2349，N[RMSE]从0.7530降至0.6187。"
- GlyphSpatialNet在无组件标签的条件下达到SOTA，4-shot UFSC的RMSE为0.0947，PSNR 25.51，SSIM 0.9093，LPIPS 0.0498。
- "UFSC (SPR scheme comparison) 上 N[L1]↓ (8-shot) = 0.2349"
- UFSC (8-shot) 上 RMSE↓ = 0.0916
---

# Rethinking Glyph Spatial Information in Font Generation

> [!tip] 核心洞察
> 在像素空间中显式解耦形状与位置，并采用从设计空间到像素空间的精确渲染映射，可以消除空间偏差，实现高保真矢量化，从而在无需组件标签的情况下大幅提升字体生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考字体生成中的字形空间信息 |
| 英文题名 | Rethinking Glyph Spatial Information in Font Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Su_Rethinking_Glyph_Spatial_Information_in_Font_Generation_CVPR_2026_paper.html) · [Code](https://github.com/sp777g/GlyphSpatialNet) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GlyphSpatialNet (with SPR scheme) |
| Dataset | UFSC |

> [!tip] 效果简介
> - UFSC (SPR scheme comparison) 上，N[L1]↓ (8-shot) 0.2349 vs 0.2922 (original rendering) (-0.0573)。
> - UFSC (8-shot) 上，RMSE↓ 0.0916 vs 0.0994 (MSD-Font) (-0.0078)。

## 概述

**问题瓶颈**：现有字体生成方法在渲染阶段普遍采用边界框居中与非均匀缩放操作，破坏了字形固有的空间信息（如基线位置、控制点坐标），导致渲染过程引入空间偏差。这种偏差使模型在训练中被迫隐式耦合形状与位置，损害细粒度特征学习和跨字体泛化能力。

**核心洞察**：在像素空间中显式解耦形状与位置，并建立从设计空间到像素空间的精确可逆渲染映射，可以从根源上消除空间偏差，实现高保真矢量化，从而在无需组件标签的条件下大幅提升字体生成质量。

**方法定位**：本文提出 **GlyphSpatialNet**（配合 SPR 渲染方案），属于两阶段像素空间扩散框架。其关键创新在于：将字形空间信息显式建模为可学习的位置偏移量，通过形状-位置解耦架构与梯度广播机制，使扩散模型能够分别处理风格迁移与空间校正。方法谱系上，该方法区别于依赖组件标签的 **LF-Font**（Park et al., AAAI 2021）、**CF-Font**（Wang et al., CVPR 2023）等局部分解方法，也不同于直接在高分辨率或潜在空间生成的 **MSD-Font**（Fu et al., CVPR 2024）、**HFH-Font**（Li and Lian, TOG 2024）等扩散基线。其平均条件机制免除了组件先验依赖，SPR 方案则为所有方法提供了统一的渲染评测基准。

**主要结果**：在 UFSC 数据集 8-shot 设置下，SPR 方案使扩散模型基线性能显著提升（N[L1] 从 0.2922 降至 0.2349）；GlyphSpatialNet 在无组件标签条件下达到 SOTA，4-shot UFSC 的 RMSE 为 0.0947，PSNR 25.51，SSIM 0.9093，LPIPS 0.0498。消融实验表明，风格细节增强模块（SDE）使基础模型性能与 MSD-Font 持平，进一步引入形状-位置解耦（SPD）与梯度广播模块（GBM）后，UFSC 8-shot RMSE 降至 0.0916，UFUC 8-shot RMSE 降至 0.1588，验证了各模块的持续增益。

## 背景与动机

### 字体生成中的空间信息困境

字体自动生成旨在从少量参考字形中学习风格特征，并将其迁移到未见字符上，从而大幅降低字体设计的人工成本。近年来，基于生成对抗网络和扩散模型的方法在图像质量上取得了显著进展，但一个根本性问题长期被忽视：**字形空间信息的丢失**。

在典型的字体生成流程中，字形首先以矢量格式存在于设计空间（通常以 `EM` 单位定义坐标系），然后通过渲染引擎转换为像素图像供模型训练。现有方法普遍采用“边界框居中 + 非均匀缩放”的渲染策略——将字形包围盒对齐到画布中心，并拉伸至固定分辨率。这一操作看似无害，实则**系统性地破坏了字形的绝对空间坐标**：基线位置、字面框偏移、部件间的相对距离等关键空间线索全部被抹除。

由此产生的后果是双重的。第一，**渲染过程引入空间偏差**：不同字形的缩放比例和偏移量各不相同，模型接收到的输入图像在空间上已丧失一致性，相当于在训练数据中注入了与风格无关的空间噪声。第二，**模型训练中形状与位置隐式耦合**：由于空间信息被破坏，模型被迫同时学习“字形长什么样”和“字形应该放在哪里”，这两个目标在像素空间中相互干扰，损害了细粒度风格特征的学习效率和泛化能力。

### 现有方法的隐性瓶颈

当前主流的少样本字体生成方法可大致分为两类：基于风格-内容分离的生成对抗网络方法（如 **EMD**（Zhang et al., CVPR 2018）、**LF-Font**（Park et al., AAAI 2021）、**DG-Font**（Xie et al., CVPR 2021）、**FSFont**（Tang et al., CVPR 2022）、**CF-Font**（Wang et al., CVPR 2023）），以及近年来兴起的扩散模型方法（如 **MSD-Font**（Fu et al., CVPR 2024）、**HFH-Font**（Li and Lian, TOG 2024））。这些方法在架构设计和风格建模上各有创新，但**无一例外地继承了有偏渲染的隐性前提**。

实验证据揭示了这一瓶颈的严重性（Table 2）：在统一使用空间保留渲染（SPR）方案后，基于扩散模型的方法性能大幅跃升——以 8-shot UFSC 设置为例，扩散模型的 N[L1] 从 0.2922 降至 0.2349，N[RMSE] 从 0.7530 降至 0.6187。这表明**原始渲染引入的空间偏差已成为限制模型学习能力的首要矛盾**，其负面影响甚至超过了模型架构本身的差异。

部分方法尝试通过引入组件标签、笔画标注等局部先验来缓解这一问题，但这类策略不仅增加了标注成本，还限制了方法的灵活性和可扩展性。更关键的是，它们并未从根本上解决空间信息的丢失——**形状与位置的耦合依然存在于像素表征中**。

### 本文动机与核心思路

上述分析指向一个清晰的结论：**字体生成的性能瓶颈不在于风格编码的复杂度，而在于空间信息在渲染-学习-生成全链路中的系统性缺失**。要突破这一瓶颈，必须在三个层面进行重新设计：

1. **渲染层面**：建立从设计空间到像素空间的可逆映射，使字形空间信息在渲染过程中得以保留，而非被归一化操作破坏。
2. **建模层面**：在模型架构中显式解耦形状预测与位置校正，避免两者在优化过程中相互干扰。
3. **矢量化层面**：利用保留的空间信息，将模型输出的像素字形精确转换回矢量格式，实现端到端的可用字体生成。

基于这一认识，本文提出**空间保留渲染（Spatial-Preserving Rendering, SPR）方案**和**GlyphSpatialNet**两阶段框架。SPR 方案基于 EM 单位和基线偏移建立可逆的渲染-矢量化映射，从根本上消除空间偏差；GlyphSpatialNet 则通过形状-位置解耦（SPD）架构和梯度广播模块（GBM），在像素空间中显式分离形状学习与空间校正，最终在无需组件标签的条件下达到 SOTA 性能。

## 核心创新

本工作的核心创新在于**显式建模并保留字形空间信息**，从根本上解决现有字体生成方法中形状与位置隐式耦合的问题。具体而言，作者识别出关键瓶颈：传统渲染流程中的边界框居中与非均匀缩放操作破坏了字形的绝对坐标（如基线位置、控制点坐标），导致模型训练时形状学习与空间偏差校正相互干扰，损害细粒度生成能力与泛化性。围绕这一瓶颈，本文提出了一套从数据渲染到模型架构的完整解决方案，包含三个层面的创新。

### 1. 空间保留渲染方案（SPR）

传统的字体渲染流程将字形边界框居中后非均匀缩放至画布，这等价于在像素空间中引入了不可逆的空间扭曲——字形在画布中的位置不再携带任何设计空间信息。SPR方案彻底摒弃了这种扭曲操作，直接基于字形的设计空间参数（EM单位、基线偏移等）定义渲染参数，建立了从设计空间 $\mathcal{G}$ 到像素空间 $\mathcal{R}$ 的可逆映射：

$$
\left[ T _ { x } \right] = \frac { H } { 2 } \cdot \left( \left[ 1 - \mathrm { F _ { s c a l e } } \right] - \left[ 0 \right] \right)
$$

渲染时，字形原点被精确映射到像素坐标 $(T_x, T_y)$；矢量化时，通过逆映射将控制点坐标恢复至原始设计空间：

$$
\left[ x ^ { \prime } \right] = { \frac { E M } { \mathrm { F } _ { \mathrm { s c a l e } } \cdot H } } \cdot \left[ x - T _ { x } \right]
$$

这一可逆性使得模型输出可直接转换为可用的TTF字体文件，同时为模型训练提供了空间无偏的监督信号。**决定性证据**：在UFSC 8-shot设置下，将扩散模型的渲染方式从原始方案切换为SPR后，N[L1]从0.2922降至0.2349，N[RMSE]从0.7530降至0.6187（Table 2），表明消除空间偏差后模型学习效果获得显著提升。

### 2. 形状-位置解耦（SPD）架构

现有方法通常将形状生成与空间定位统一优化，导致两者在训练中隐式耦合。GlyphSpatialNet在第一阶段低分辨率风格迁移中引入SPD架构，将扩散模型的逆向过程显式分解为两条路径：

- **形状路径**：预测初始形状估计 $I _ { G } ^ { l , i n i t } = I _ { \theta } ( I _ { t } , I _ { C } ^ { l } , t , \mathcal { F } _ { S } )$，负责学习字形的笔画结构与风格特征。
- **位置路径**：通过MLP预测二维空间校正偏移 $\varphi _ { \Delta } \in \mathbb { R } ^ { 2 \times 1 }$，负责校正渲染或预测过程中的空间偏差。

这种解耦设计的核心优势在于：形状学习不再被位置误差的梯度所干扰，位置校正也能独立优化。然而，位置路径中使用的双线性采样（warping）存在梯度局部化问题——梯度仅在采样点邻域内传播，导致位置路径难以校正大范围的空间偏移。

### 3. 梯度广播模块（GBM）

为突破双线性采样的梯度局部性限制，GBM通过保留高频分量并利用梯度直通（detach）机制扩大梯度传播范围：

$$
\mathrm { G B M } ( I ) = \mathcal { B } _ { \sigma } ( I ) + \left( I - \mathcal { B } _ { \sigma } ( I ) . \mathrm { d e t a c h } ( ) \right)
$$

其中 $\mathcal{B}_{\sigma}$ 为高斯模糊，$I - \mathcal{B}_{\sigma}(I)$ 提取高频细节，detach操作使这部分分量在反向传播时直接传递梯度，从而让位置路径的校正信号能够影响更大范围的像素。消融实验证实了GBM的关键作用：在SDE基础上引入SPD和GBM后，UFSC 8-shot RMSE从0.0994进一步降至0.0916（Table 5）。

### 4. 免组件标签的平均条件机制

与依赖组件标签或笔画标注的方法（如LF-Font、CF-Font）不同，GlyphSpatialNet通过平均条件机制聚合多个参考图像的风格编码：

$$
\mathcal { F } _ { S } = \frac { 1 } { k } \sum _ { i = 1 } ^ { k } \mathcal { E } _ { s t y l e } ( I _ { S , i } ^ { h } )
$$

这一设计支持动态数量的参考图像，且无需任何局部先验标签，显著提升了方法的易用性与灵活性。在无需组件标签的条件下，GlyphSpatialNet在UFSC 4-shot上达到RMSE 0.0947、PSNR 25.51、SSIM 0.9093、LPIPS 0.0498的SOTA性能（Table 4）。

### 创新点总结

| 创新维度 | 现有方案 | 本文方案 | 关键机制 |
|---------|---------|---------|---------|
| 渲染方案 | 边界框居中+非均匀缩放 | SPR可逆映射 | 保留绝对坐标，消除空间偏差 |
| 形状与位置建模 | 隐式耦合，统一优化 | SPD显式解耦 | 形状路径与位置路径独立优化 |
| 梯度传播 | 双线性采样梯度局部化 | GBM梯度广播 | 高频保留+梯度直通扩大传播范围 |
| 先验依赖 | 需组件/笔画标签 | 平均条件机制 | 仅需参考图平均风格特征 |

**需人工验证**：SPR方案对GAN类方法的性能影响为负（Table 2中GAN方法在SPR下指标普遍上升），这一现象的具体原因在现有证据中未充分解释，建议结合原文Section 4.2的讨论进一步确认。

## 整体框架

GlyphSpatialNet 是一个两阶段像素空间字体生成框架，其核心设计目标是在无需组件标签的条件下，显式解耦字形形状与空间位置，从而实现高保真、可矢量化的少样本字体生成。整个 pipeline 围绕三个关键环节展开：空间保留渲染（SPR）提供无偏训练数据与可逆矢量化通道；第一阶段在低分辨率下完成风格迁移与形状-位置解耦；第二阶段在像素空间恢复高分辨率风格细节。

**数据准备与矢量化闭环**

框架的入口是 SPR 渲染方案（见 Figure 1）。与传统的边界框居中加非均匀缩放不同，SPR 直接基于字体的 EM 单位、基线偏移等字形度量参数定义渲染参数，将设计空间 G 的原点映射到像素空间 R 的坐标 $(T_x, T_y)$：

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our study. (1) We propose SPR scheme, which provides a spatially unbiased rendering process and enables accurate vectorization by preserving spatial information from the font design space to the raster space; (2) We introduce a large-scale vector Chinese font dataset, providing the data foundation for our benchmark. (3) We develop GlyphSpatialNet for explicit spatial modeling. Our model jointly predicts an initial shape estimate and a spatial offset field from the position path, enabling longrange gradient propagation between pixels. Finally, the output is vectorized into ready-to-use TTF font files*

$$\left[ T _ { x } \right] = \frac { H } { 2 } \cdot \left( \left[ 1 - \mathrm { F _ { s c a l e } } \right] - \left[ 0 \right] \right)$$

这一映射保留了字形的绝对空间坐标信息，消除了渲染过程中的空间偏差。模型推理完成后，矢量化过程通过逆映射将像素空间 R 中的控制点坐标恢复至原始设计空间 G：

$$\left[ x ^ { \prime } \right] = { \frac { E M } { \mathrm { F } _ { \mathrm { s c a l e } } \cdot H } } \cdot \left[ x - T _ { x } \right]$$

由此形成从设计空间到像素空间再到设计空间的信息保留闭环，最终输出可直接使用的 TTF 字体文件。

**两阶段生成架构**

GlyphSpatialNet 的整体架构如 Figure 3 所示，分为两个训练阶段：

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/004_Figure_3.jpg]]
*Figure 3: Overview. In training, our model has two stages: Stage I. We train the process of font style transfer to generate low resolution target images for efficiency. (a) An average conditional mechanism is applied in high resolution pixel space for flexible style conditioning. (b) We incorporate our SPD architecture into the reverse process of a diffusion model, which we call the SPD reverse process, to reduce the coupling of shape artifacts and positional bias during training. This step is carried out in low resolution pixel space to lower computational complexity. (c) Our GBM addresses the gradient locality issue in bilinear sampling, allowing the position path to effectively correct large spati...*

**第一阶段：低分辨率风格迁移与形状-位置解耦。** 该阶段包含三个关键模块：

- **平均条件机制（Average Conditional Mechanism）**：在高分辨率像素空间对 $k$ 张参考图像 $I_{S,i}^h$ 分别提取风格编码，取平均获得全局风格条件 $\mathcal{F}_S$：

$$\mathcal { F } _ { S } = \frac { 1 } { k } \sum _ { i = 1 } ^ { k } \mathcal { E } _ { s t y l e } ( I _ { S , i } ^ { h } )$$

这一设计支持动态数量的参考图像，且无需任何组件标签，仅依赖参考图像的平均风格特征。

- **形状-位置解耦架构（SPD）**：整合在扩散模型的逆向过程中，分为两条并行的路径——形状路径预测初始形状估计 $I_G^{l,init}$，位置路径预测二维空间校正偏移 $\varphi_\Delta \in \mathbb{R}^{2 \times 1}$。两条路径显式分离，避免形状伪影与位置偏差在训练中隐式耦合。

- **梯度广播模块（GBM）**：解决双线性采样导致的梯度局部化问题。通过保留图像高频分量并对其 detach 实现梯度直通，使位置路径的梯度能够传播到更远的空间区域，从而有效校正大范围空间偏移：

$$\mathrm { G B M } ( I ) = \mathcal { B } _ { \sigma } ( I ) + \left( I - \mathcal { B } _ { \sigma } ( I ) . \mathrm { d e t a c h } ( ) \right)$$

第一阶段在低分辨率像素空间运行，以降低计算复杂度。

**第二阶段：风格细节增强（SDE）。** 冻结风格编码器，引入参数无关的双线性下采样器 DS 和风格引导的上采样器 US。高分辨率目标图像 $I_G^h$ 经下采样后，由 US 结合风格条件 $\mathcal{F}_S$ 进行上采样重建，训练目标为 L2 损失：

$$\mathcal { L } _ { \mathrm { S t a g e I I } } = \| U S \big( D S ( I _ { G } ^ { h } ) , \mathcal { F } _ { S } \big ) - I _ { G } ^ { h } \| _ { 2 } ^ { 2 }$$

该阶段在像素空间直接恢复和增强高分辨率风格细节，避免潜在空间生成可能导致的模糊或细节损失。

**推理流程**

推理时，将两个阶段的组件组合使用：高分辨率内容图像 $I_C^h$ 经下采样得到低分辨率输入 $I_C^l$，送入第一阶段的 SPD 逆向过程（使用 DDIM 采样器，$\eta=0$ 加速采样），生成低分辨率目标字形；再通过第二阶段的 SDE 模块上采样至目标分辨率，最终经 SPR 矢量化输出 TTF 字体。

**方法谱系与知识库定位**

在字体生成领域，现有方法可大致分为基于 GAN 的风格-内容分离路线（如 **EMD**（Zhang et al., CVPR 2018）、**LF-Font**（Park et al., AAAI 2021）、**DG-Font**（Xie et al., CVPR 2021）、**FSFont**（Tang et al., CVPR 2022）、**CF-Font**（Wang et al., CVPR 2023））和基于扩散模型的生成路线（如 **NTF**（Fu et al., CVPR 2023）、**MSD-Font**（Fu et al., CVPR 2024）、**HFH-Font**（Li and Lian, TOG 2024））。GlyphSpatialNet 在以下维度进行了差异化改造：

1. **渲染方案**：将普遍使用的“边界框居中+非均匀缩放”替换为 SPR，建立可逆映射，消除空间偏差。
2. **形状与位置建模**：从隐式耦合统一优化转变为 SPD 显式解耦架构。
3. **梯度传播**：引入 GBM 解决双线性采样的梯度局部化问题。
4. **高分辨率生成**：采用两阶段像素空间处理（SPD+GBM → SDE），而非直接在高分辨率或潜在空间生成。
5. **先验依赖**：通过平均条件机制仅使用参考图像的平均风格特征，免去组件标签等局部先验。

SPR 方案本身具有通用性——论文在 Table 2 中验证，将其应用于扩散模型可使 UFSC 8-shot 的 N[L1] 从 0.2922 降至 0.2349，N[RMSE] 从 0.7530 降至 0.6187，表明无偏渲染对扩散模型的性能提升显著。但值得注意的是，SPR 对 GAN 类方法反而有负面影响，这暗示空间偏差的消除可能暴露了 GAN 在细粒度空间建模上的固有不足，需要手动验证具体原因。

## 核心模块与公式推导

### 3.1 空间保留渲染（SPR）方案

SPR方案是整个方法的数据基础，其核心在于**建立设计空间与像素空间之间的可逆映射**，从而消除传统渲染流程中因边界框居中和非均匀缩放引入的空间偏差。

**渲染过程**：将字形从设计空间 $G$ 映射到像素空间 $R$ 时，SPR直接基于字形的空间信息（如基线位置、EM单位）定义渲染参数，而非依赖边界框。渲染原点的偏移量由下式给出：

$$\left[ T _ { x } \right] = \frac { H } { 2 } \cdot \left( \left[ 1 - \mathrm { F _ { s c a l e } } \right] - \left[ 0 \right] \right)$$

其中 $H$ 为渲染分辨率，$\mathrm{F_{scale}}$ 为缩放因子，$(T_x, T_y)$ 将设计空间原点映射到像素空间的对应坐标。该映射保留了字形的绝对空间位置信息。

**矢量化过程**：模型推理结果经矢量化后，需将轮廓控制点从像素空间 $R$ 恢复至原始设计空间 $G$，坐标变换为：

$$\left[ x ^ { \prime } \right] = { \frac { E M } { \mathrm { F } _ { \mathrm { s c a l e } } \cdot H } } \cdot \left[ x - T _ { x } \right]$$

其中 $EM$ 为字体的EM单位，$(x, y)$ 为像素空间中的控制点坐标，$(x', y')$ 为恢复至设计空间的坐标。这一可逆映射确保了生成的字形可直接转换为可用的TTF字体文件。

**笔画归一化度量**：为消除空白区域对评测的影响，提出笔画归一化指标：

$$\mathbf { N } [ d ] ( I , \hat { I } ) = \frac { d ( I , \hat { I } ) } { \mathcal { W } _ { s t r o k e } ( I ) + \delta }$$

其中 $d(\cdot,\cdot)$ 为原始差异度量（如L1或RMSE），$\mathcal{W}_{stroke}(I)$ 为目标图像 $I$ 的笔画权重（笔画区域像素数），$\delta$ 为防止除零的小常数。该归一化将绝对损失转化为笔画内的相对损失密度。

### 3.2 平均条件机制

为支持动态数量的参考图像且无需组件标签，采用平均条件机制聚合风格信息：

$$\mathcal { F } _ { S } = \frac { 1 } { k } \sum _ { i = 1 } ^ { k } \mathcal { E } _ { s t y l e } ( I _ { S , i } ^ { h } )$$

其中 $\mathcal{E}_{style}$ 为风格编码器，$I_{S,i}^h$ 为第 $i$ 张高分辨率参考图像，$k$ 为参考图像数量，$\mathcal{F}_S$ 为聚合后的全局风格条件。该机制在训练和推理中统一使用，避免了组件标签的依赖。

### 3.3 形状-位置解耦（SPD）架构

SPD架构嵌入扩散模型的逆向过程中，显式分离形状预测与位置校正两条路径。

**形状路径**：预测初始形状估计：

$$I _ { G } ^ { l , i n i t } = I _ { \theta } ( I _ { t } , I _ { C } ^ { l } , t , \mathcal { F } _ { S } )$$

其中 $I_t$ 为当前时间步的噪声图像，$I_C^l$ 为低分辨率内容图像，$t$ 为时间步，$\mathcal{F}_S$ 为风格条件，$I_\theta$ 为形状预测网络，输出初始形状估计 $I_G^{l,init}$。

**位置路径**：预测二维空间校正偏移：

$$\varphi _ { \Delta } = \mathrm { M L P } ( \mathbf { F } _ { c a t } ) , \quad \varphi _ { \Delta } \in \mathbb { R } ^ { 2 \times 1 }$$

其中 $\mathbf{F}_{cat}$ 为形状路径与位置路径特征的拼接，MLP输出平移变换参数 $\varphi_\Delta$，用于对初始形状进行空间校正。

### 3.4 梯度广播模块（GBM）

双线性采样导致梯度仅在局部邻域传播，限制了位置路径对大范围空间偏差的校正能力。GBM通过保留高频分量并利用梯度直通机制解决此问题：

$$\mathrm { G B M } ( I ) = \mathcal { B } _ { \sigma } ( I ) + \left( I - \mathcal { B } _ { \sigma } ( I ) . \mathrm { d e t a c h } ( ) \right)$$

其中 $\mathcal{B}_\sigma$ 为高斯模糊操作，$I - \mathcal{B}_\sigma(I)$ 为高频残差。通过 `.detach()` 阻断高频分量的梯度回传，使梯度经低频路径广播至更大空间范围，同时前向传播中高频信息得以完整保留。

### 3.5 风格细节增强（SDE）

第二阶段在像素空间恢复高分辨率风格细节，损失函数为：

$$\mathcal { L } _ { \mathrm { S t a g e I I } } = \| U S \big ( D S ( I _ { G } ^ { h } ) , \mathcal { F } _ { S } \big ) - I _ { G } ^ { h } \| _ { 2 } ^ { 2 }$$

其中 $DS$ 为无参数双线性下采样器，$US$ 为风格引导的上采样器，$I_G^h$ 为高分辨率目标图像。该阶段冻结风格编码器，仅训练上采样器以恢复细节。

**推理流程**：高分辨率内容图像经下采样得到 $I_C^l = DS(I_C^h)$，送入第一阶段SPD逆向过程生成低分辨率字形，再经SDE上采样至目标分辨率，最终通过SPR矢量化转换为TTF字体。推理中采用DDIM采样器（$\eta=0$）加速逆向过程。

### 补充图表

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/003_Figure_2.jpg]]
*Figure 2: Illustration of our SPR scheme. The rendering process provides a spatially unbiased glyph image by preserving spatial information from G to R, and the rendered data is used for model training. The vectorization process performs a transformation from V to G on the control point coordinates of the obtained contour, which is vectorized from the model’s inference results*

## 实验与分析

### 核心瓶颈与实验设计逻辑

现有字体生成方法的根本瓶颈在于渲染过程引入的空间偏差：常规流程将字形边界框居中并进行非均匀缩放，导致基线位置、控制点坐标等关键空间信息丢失，使模型训练中形状与位置隐式耦合。当模型试图学习字形风格时，必须同时隐式补偿这种空间偏移，严重损害细粒度特征学习和跨字体泛化能力。

本文的实验设计围绕两条因果主线展开：
1. **空间保留渲染（SPR）方案的统一性验证**：证明消除渲染端空间偏差本身即可显著提升模型学习效果，且为不同方法提供公平对比基准。
2. **GlyphSpatialNet 的形状-位置解耦能力验证**：证明在 SPR 基础上，显式建模字形空间信息可进一步突破性能上限，且无需组件标签即可达到 SOTA。

为消除空白区域对评测的干扰，实验引入笔画归一化指标 $N[L1]$ 和 $N[RMSE]$，将绝对损失转化为笔画内的相对损失密度：

$$\mathbf { N } [ d ] ( I , \hat { I } ) = \frac { d ( I , \hat { I } ) } { \mathcal { W } _ { s t r o k e } ( I ) + \delta }$$

这使得不同渲染方式下的模型学习效果可直接对比。

---

### SPR 方案有效性验证

Table 2 给出了在统一 SPR 渲染基准下，扩散模型与 GAN 模型在原始渲染与 SPR 渲染下的性能对比。核心发现：

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation of font generation models under original rendering versus our SPR scheme, demonstrating SPR’s capability to enhance model learning and boost generation performance. For each metric pair, the left black number denotes the result under the original rendering, while the right one is produced under the proposed SPR scheme. Red or blue color indicates the metric is increased or decreased, respectively. When spatial noise becomes the principal contradiction, the SPR scheme yields remarkable gains*

- **扩散模型从 SPR 中显著受益**：在 UFSC 8-shot 设置下，本文扩散模型（Ours Diffusion-Based）的 $N[L1]$ 从 0.2922 降至 0.2349，$N[RMSE]$ 从 0.7530 降至 0.6187，降幅分别达 19.6% 和 17.8%。**MSD-Font**（Fu et al., CVPR 2024）同样获得明显提升，$N[L1]$ 从 0.3294 降至 0.2752。
- **GAN 方法在 SPR 下反而退化**：**LF-Font**（Park et al., AAAI 2021）的 $N[L1]$ 从 0.5366 升至 0.6064，$N[RMSE]$ 从 1.0826 升至 1.4243。这表明 GAN 的对抗训练可能已隐式适应了空间偏差，移除偏差后反而破坏了其内部平衡。
- **扩散模型已大幅领先 GAN**：在 SPR 方案下，扩散方法（Ours 0.2349）与 GAN 方法（LF-Font 0.6064）的 $N[L1]$ 差距达 2.6 倍，说明扩散范式天然更适合处理空间信息保留后的字形生成任务。

SPR 方案的另一关键贡献是提供统一渲染基准：此前不同方法各自收集数据、采用不同渲染方式，导致评测结果不可比。Table 2 中所有方法在 SPR 下的结果构成了首个可公平对比的少样本字体生成基准。

---

### 与 SOTA 方法的全面对比

Table 4 给出在 UFSC（未见风格）和 UFUC（未见风格+未见字符）两个子集上，4-shot 和 8-shot 设置下的定量对比。GlyphSpatialNet 在**无需组件标签**的条件下达到 SOTA：

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/007_Table_4.jpg]]
*Table 4: Comparison with SOTA methods. Our model achieves SOTA without requiring component labels, offering better usability and flexibility. The training data is rendered using our SPR scheme on our dataset, establishing a unified benchmark for SOTA methods*

- **UFSC 4-shot**：RMSE 0.0947，PSNR 25.51，SSIM 0.9093，LPIPS 0.0498。相比最强基线 **MSD-Font**（RMSE 0.1068），RMSE 降低 11.3%。
- **UFSC 8-shot**：RMSE 0.0916，PSNR 25.86，SSIM 0.9136，LPIPS 0.0463。
- **UFUC 8-shot**：RMSE 0.1588，PSNR 23.46，SSIM 0.8578，LPIPS 0.0896。UFUC 要求同时泛化到未见风格和未见字符，难度显著高于 UFSC，但 GlyphSpatialNet 在所有指标上仍保持领先。

值得注意的是，**CF-Font**（Wang et al., CVPR 2023）和 **FSFont**（Tang et al., CVPR 2022）等方法依赖组件标签或细粒度局部标注，而 GlyphSpatialNet 仅使用参考图像的平均风格特征 $\mathcal { F } _ { S } = \frac { 1 } { k } \sum _ { i = 1 } ^ { k } \mathcal { E } _ { s t y l e } ( I _ { S , i } ^ { h } )$，在更少先验条件下取得更优性能，实用性更强。

Table 3 的定性对比进一步验证：在 UFUC 的极端泛化场景下，GlyphSpatialNet 生成的字符在笔画粗细一致性、结构完整性和风格保真度上均优于基线方法。基线方法在未见字符上常出现笔画断裂或位置偏移，而 SPD 架构的显式空间校正有效缓解了这一问题。

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/006_Table_3.jpg]]
*Table 3: Qualitative comparison with SOTA methods on the UFUC dataset. Zoom-in for better inspection*

---

### 消融实验：模块贡献的逐步验证

Table 5 通过逐步叠加模块的方式，在 UFSC 和 UFUC 上量化各组件的贡献：

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/009_Table_5.jpg]]
*Table 5: Ablation study of our proposed module, evaluated on the UFSC and UFUC datasets*

- **Base（仅扩散模型 + SPR）**：UFSC 8-shot RMSE 0.1140，UFUC 8-shot RMSE 0.1839。该基线已使用 SPR 渲染，消除了数据端空间偏差。
- **+ SDE（风格细节增强）**：UFSC 8-shot RMSE 降至 0.0994，UFUC 降至 0.1754。SDE 通过下采样与风格引导上采样在像素空间恢复高分辨率细节，使 RMSE 降低 12.8%（UFSC），验证了第二阶段高分辨率增强的必要性。此配置下性能已与 SOTA 方法 MSD-Font 持平。
- **+ SPD w/ GBM（形状-位置解耦 + 梯度广播）**：UFSC 8-shot RMSE 进一步降至 0.0916，UFUC 降至 0.1588。SPD 架构将形状预测与空间变换显式分离，GBM 通过 $\mathrm { G B M } ( I ) = \mathcal { B } _ { \sigma } ( I ) + \left( I - \mathcal { B } _ { \sigma } ( I ) . \mathrm { d e t a c h } ( ) \right)$ 解决双线性采样的梯度局部化问题，使位置路径能有效校正大范围空间偏移。两个模块联合带来额外 7.9%（UFSC）和 9.5%（UFUC）的 RMSE 降低。

消融实验的因果链条清晰：SPR 消除数据端偏差 → SDE 恢复高分辨率细节 → SPD+GBM 在模型内部显式解耦形状与位置，每步均有可量化的性能增益。

---

### 分辨率选择的精度-效率权衡

Figure 4 给出 SPR 方案在不同渲染分辨率下的误差曲线。当分辨率达到 128² 时，SPR 引入的量化误差已低于生成模型对未见字符的固有预测误差（参考 Table 4 中 UFUC 的 RMSE 水平），继续提高分辨率带来的精度收益边际递减。因此本文选择 128² 作为第一阶段低分辨率风格迁移的工作分辨率，在精度与计算效率间取得平衡。

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/008_Figure_4.jpg]]
*Figure 4: The SPR scheme error curve as a function of resolution. When the resolution is*

---

### 失败模式与局限性

尽管 GlyphSpatialNet 在标准基准上表现优异，分析其失败模式可发现以下局限：

1. **极端风格泛化不足**：中文字体制作成本高，书法和极端风格（如瘦金体、草书）字体数量有限。在训练集中仅 200 种字体的条件下，模型对笔画高度连笔、结构高度变形的稀有风格生成质量下降，可能出现笔画粘连或风格特征丢失。该问题根源在于数据端而非方法端，需要更大规模的多样化字体采集。

2. **跨文字系统迁移未验证**：SPD 架构的设计依赖于中文字符的方块结构和基线对齐特性，对于拉丁文（可变宽度、多基线）或日文（混合文字）等不同文字系统的适用性尚未验证，这是方法泛化性的开放问题。

3. **GAN 方法的 SPR 兼容性**：Table 2 显示 GAN 在 SPR 下性能退化，说明 SPR 方案目前主要惠及扩散模型。如何设计适用于 GAN 的空间信息保留策略仍需探索。

### 补充图表

![[assets/figures/papers/paper_list_l2582_https_openaccess_thecvf_com_content_CVPR2026_html_Su_Rethinking_Glyph_Sp/figures/002_Table_1.jpg]]
*Table 1: Comparison of existing Chinese font datasets in FFG with ours. The quantity and quality of existing datasets are compromised due to spatial distortion during rendering and copyright restrictions, and as a result, different methods typically collect their own datasets. Our dataset provides vector source files, along with our SPR scheme, enabling flexible resolution and spatially unbiased glyph images, or for use in vector-driven methods and future exploration*

## 方法谱系与知识库定位

### 与现有工作的关系

**1. 渲染方案的根本性变革**

传统字体生成方法（包括 LF-Font、DG-Font、CF-Font 等）普遍采用“边界框居中 + 非均匀缩放”的渲染流程，这一操作破坏了字形原始的空间坐标信息，导致渲染后的图像存在空间偏差。GlyphSpatialNet 提出的空间保留渲染（SPR）方案放弃了上述扭曲操作，直接基于字体的 EM 单位和基线偏移定义渲染参数，建立了从设计空间到像素空间的可逆映射（Eq. 1-2），使渲染后的字形图像完整保留了原始空间信息。这一改变并非简单的预处理优化，而是从数据源头消除了空间偏差这一瓶颈——实验表明，仅将 SPR 方案应用于现有扩散模型，UFSC 8-shot 的 N[L1] 即可从 0.2922 降至 0.2349（Table 2），验证了该瓶颈的因果性。

**2. 形状-位置耦合问题的显式解耦**

现有方法在模型训练中隐式耦合了字形形状与位置的学习，统一优化目标导致两者相互干扰。GlyphSpatialNet 通过形状-位置解耦（SPD）架构，在扩散模型的逆向过程中分离出形状路径（预测初始形状和噪声）与位置路径（预测空间校正偏移），实现了显式建模。与之配套的梯度广播模块（GBM）解决了双线性采样带来的梯度局部化问题——通过保留高频分量并利用 detach 实现梯度直通，使位置路径能够有效处理大范围的空间偏移。这一设计使得模型在无需组件标签的条件下即可达到 SOTA 性能（Table 4），而此前的方法如 LF-Font（Park et al., AAAI 2021）依赖局部风格分解，CF-Font（Wang et al., CVPR 2023）需要内容融合机制，FSFont（Tang et al., CVPR 2022）则依赖细粒度局部风格标签。

**3. 与扩散模型基线的对比**

在扩散模型方法中，MSD-Font（Fu et al., CVPR 2024）采用多阶段生成策略，HFH-Font（Li and Lian, TOG 2024）聚焦高分辨率扩散。GlyphSpatialNet 与这些工作的关键区别在于：它将两阶段设计定位于“低分辨率风格迁移 + 高分辨率细节增强”，而非简单的多阶段级联。第一阶段在低分辨率像素空间完成形状-位置解耦（SPD + GBM），降低计算复杂度；第二阶段通过风格细节增强（SDE）模块在像素空间恢复高分辨率风格细节。消融实验（Table 5）表明，Base + SDE 即可使 UFSC 8-shot RMSE 降至 0.0994（与 MSD-Font 持平），进一步加入 SPD 和 GBM 后降至 0.0916，验证了每个模块的独立贡献。

**4. 与向量驱动方法的潜在联系**

NTF（Fu et al., CVPR 2023）基于神经变换场，代表了向量驱动方法的探索方向。GlyphSpatialNet 虽然工作在像素空间，但其 SPR 方案提供了精确的矢量化能力——通过 Eq. (2) 将像素空间的控制点坐标恢复至原始设计空间，可直接生成可用的 TTF 字体文件。这一设计为像素空间方法与向量驱动方法的结合提供了桥梁，但目前尚未在实验中直接对比 NTF 等向量方法。

### 适用边界

**有效范围：**
- 中文字体生成任务，在少样本设置（4-shot / 8-shot）下表现出色，覆盖 UFSC（未见风格未见字）和 UFUC（未见风格未见字）两种泛化场景。
- 对常规印刷字体（如宋体、黑体等）的生成质量较高，模型在 200 种训练字体上学习到的风格表征具有较好的泛化能力。
- SPR 方案在 128² 分辨率下已实现精度与效率的平衡——Figure 4 显示该分辨率下的渲染误差已低于生成模型对未见字的固有损失。

**失效或弱化场景：**
- 论文明确指出，中文字体制作成本高，限制了书法和极端风格（如瘦金体、草书）等类型字体的可用性，影响模型在稀有风格上的训练效果。
- Table 2 显示，SPR 方案对 GAN 类方法（如 LF-Font）不仅未能提升，反而造成性能下降（N[L1] 从 0.6064 升至 0.6716），说明 SPR 方案与 GAN 架构存在兼容性问题。论文将此归因于 GAN 的训练不稳定性和对空间噪声的敏感度不同，但具体机制尚待进一步分析。
- 模型训练依赖于 SPR 渲染数据，若应用于未经 SPR 处理的第三方数据集，性能可能下降。

### 局限与开放问题

**已确认的局限：**
1. 稀有风格覆盖不足：受限于字体制作成本，训练集中书法和极端风格字体数量有限，模型在这些风格上的生成质量缺乏充分验证。
2. GAN 架构兼容性差：SPR 方案对扩散模型提升显著，但对 GAN 类方法反而有害，限制了该方案在非扩散架构上的推广。

**待验证的开放问题：**
1. 跨文字系统推广：形状-位置解耦方法是否可有效推广至拉丁文、日文等其他文字系统？不同文字的空间结构差异（如基线系统、连字规则）可能要求重新设计空间建模策略。
2. 极端风格下的空间建模有效性：在瘦金体、草书等笔画高度变形、空间结构非规范的字体上，显式空间建模是否能保持高质量生成？这需要在更大规模的风格多样性数据集上进行验证。
3. 与向量驱动方法的深度融合：SPR 方案已具备精确矢量化的能力，但尚未与向量驱动方法（如 NTF）进行系统性结合。将像素空间的形状-位置解耦与向量空间的轮廓优化相结合，可能是进一步提升轮廓控制精度的方向。
4. 更大空间偏差的校正能力：GBM 模块通过梯度广播扩大了位置路径的校正范围，但其对极端空间偏移（如某些装饰性字体的巨大基线偏移）的校正上限尚未量化评估。

## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_Glyph_Spatial_Information_in_Font_Generation.pdf]]
