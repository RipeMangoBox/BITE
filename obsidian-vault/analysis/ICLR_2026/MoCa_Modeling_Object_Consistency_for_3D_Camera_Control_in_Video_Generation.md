---
title: "MoCa: Modeling Object Consistency for 3D Camera Control in Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MoCa_Modeling_Object_Consistency_for_3D_Camera_Control_in_Video_Generation_fe63ef4de104.pdf
project_link: null
code_link: null
aliases:
- MoCa
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式建模对象在视图、外观和运动三个维度上的一致性，以隐式学习相机与场景之间的3D关系，从而桥接2D像素与3D场景的鸿沟。
primary_logic: 3D场景中平滑的相机运动映射到2D视频时自然产生一致的对象视图、外观和运动；通过约束这三种2D投影中的一致性，可以反向注入3D空间感知，绕开显式3D重建的需求。
claims:
- 在RealEstate10K上，MoCa的FID达到207.4，优于AC3D (225.2)，FVD 667.9也显著优于对比方法。
- 在动态场景数据集VidGen上，MoCa的CLIPSIM (0.349) 和对象一致性OC (94.7%) 均超过AC3D (0.345, 93.5%)，且运动平滑度MS (98.3%) 保持稳定。
- 消融实验证实，移除语义引导策略会导致严重对象失真（如海龟几何扭曲），验证了外观一致性建模的有效性。
- 在相机运动与文本指定的对象运动方向冲突的场景中（如鸟从右向左飞而镜头向右平移），MoCa成功解耦两种运动，不扭曲对象运动方向，体现了运动一致性优势。
---

# MoCa: Modeling Object Consistency for 3D Camera Control in Video Generation

> [!tip] 核心洞察
> 3D场景中平滑的相机运动映射到2D视频时自然产生一致的对象视图、外观和运动；通过约束这三种2D投影中的一致性，可以反向注入3D空间感知，绕开显式3D重建的需求。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoCa：面向视频生成中3D相机控制的对象一致性建模 |
| 英文题名 | MoCa: Modeling Object Consistency for 3D Camera Control in Video Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DZcpnudp7f) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MoCa |
| Dataset | RealEstate10K, VidGen |

> [!tip] 效果简介
> - RealEstate10K 上，FID↓ 207.4 vs 225.2 (AC3D) (-17.8)；CLIPSIM↑ 0.312 vs 0.309 (AC3D) (+0.003)；OC↑ 94.9% vs 95.1% (AC3D) (-0.2%)。
> - VidGen 上，FVD↓ 1643.7 vs 1712.0 (AC3D) (-68.3)；CLIPSIM↑ 0.349 vs 0.345 (AC3D) (+0.004)；OC↑ 94.7% vs 93.5% (AC3D) (+1.2%)。

## 概要

**问题瓶颈**：现有相机可控视频生成方法（如 **MotionCtrl** (Wang et al., 2024b)、**CameraCtrl** (He et al., 2024)、**AC3D** (Bahmani et al., 2024a)）主要在2D像素空间直接集成相机条件，缺乏对底层3D场景的隐式理解。这导致生成视频中对象的视图、外观和运动难以保持一致——尤其在复杂动态场景下，纹理崩塌和对象失真问题突出。

**核心思路**：MoCa 通过显式建模对象在**视图一致性**、**外观一致性**和**运动一致性**三个维度上的约束，隐式学习相机与场景之间的3D关系。其关键洞察在于：3D场景中平滑的相机运动投影到2D视频时，天然要求对象在视图、外观和运动上保持一致；反过来，通过约束这三种2D投影中的一致性，可以反向注入3D空间感知，从而绕开显式3D重建的需求。

**方法定位**：MoCa 采用双分支融合框架（ReferenceNet + DenoisingNet），在 **CogVideoX** 基础上引入三个核心模块：(1) 基于 Plücker 嵌入的时空相机编码器（ST-Encoder）维持视图一致性；(2) 语义引导策略利用视觉-语言特征稳定对象外观；(3) 基于2D离散小波变换（2D-DWT）高频分解的对象感知掩码实现相机运动与对象运动的解耦。

**主要结果**：在 RealEstate10K 静态场景数据集上，MoCa 的 FID 达到 **207.4**（AC3D 为 225.2），FVD 为 **667.9**，均优于对比方法。在动态场景数据集 VidGen 上，MoCa 的 CLIPSIM（**0.349**）和对象一致性 OC（**94.7%**）均超过 AC3D（0.345, 93.5%），同时运动平滑度 MS（98.3%）保持稳定。消融实验证实，语义引导策略的移除会导致严重对象失真，高频对象掩码是实现运动解耦的关键组件。

**局限性**：MoCa 目前仅支持文本到视频的相机控制，未扩展至图像、视频编辑等多模态输入；此外，方法无法精确控制运动对象在生成帧中的具体位置。

### 视频生成中的相机控制需求

文本到视频生成（Text-to-Video Generation）旨在学习从文本提示 $\mathbf{P}$ 到视频体积 $\mathbf{V}$ 的映射：

$$f ( \mathbf { P } ) \to \mathbf { V } ^ { X \times Y \times T }$$

其中 $X$、$Y$ 为像素坐标，$T$ 为时间维度。然而，这种标准映射缺乏对相机运动的显式控制能力，生成的视频往往只能呈现固定的视角和镜头运动模式。为赋予用户对视频生成过程的精确镜头控制，研究者引入了相机轨迹条件 $\mathbf{\dot{C}}$，将映射扩展为：

$$f ( \mathbf { P } , \mathbf { \dot { C } } ) \to \mathbf { V } ^ { X \times Y \times \dot { Z } \times T }$$

这一扩展映射的输出增加了 $Z$ 维度，表示视频中隐含的 3D 空间关系，使得生成视频能够响应指定的相机运动轨迹（如平移、旋转、缩放等）。

### 现有方法的瓶颈：2D 像素空间与 3D 场景的鸿沟

当前主流的相机可控视频生成方法——如 **MotionCtrl** (Wang et al., 2024b)、**CameraCtrl** (He et al., 2024) 和 **AC3D** (Bahmani et al., 2024a)——普遍采用在 2D 像素空间直接集成相机条件的策略。具体而言，这些方法将相机的外参/内参数值直接编码后，通过逐元素加法等方式融合到去噪网络中。

这种“2D 表面”式处理存在一个根本性瓶颈：**缺乏对底层 3D 场景的隐式理解**。3D 场景中平滑的相机运动，在投影到 2D 视频时，会自然地在像素层面产生三种一致性表现：

- **视图一致性（View Consistency）**：对象在相机运动过程中应保持可见且结构稳定；
- **外观一致性（Appearance Consistency）**：对象的纹理、颜色等外观属性在视角变化下应保持连贯；
- **运动一致性（Motion Consistency）**：对象自身的运动（如鸟飞翔的方向）不应被相机运动所扭曲或覆盖。

现有方法由于未在模型设计中显式建模这三种一致性，导致生成的视频在复杂动态场景下频繁出现**纹理崩塌、对象几何失真、运动方向被相机运动覆盖**等问题。尤其在相机运动与文本指定的对象运动方向发生冲突时（例如文本描述“鸟从右向左飞”而相机镜头向右平移），现有方法往往无法解耦两种运动，导致对象运动方向被相机运动“劫持”。

### MoCa 的核心动机与设计思路

MoCa 的核心动机源自一个关键洞察：**3D 场景中平滑的相机运动映射到 2D 视频时，自然会产生一致的对象视图、外观和运动；反过来，通过约束这三种 2D 投影中的一致性，可以反向向模型注入 3D 空间感知能力，从而绕开显式 3D 重建的复杂需求。**

基于这一洞察，MoCa 提出了一个双分支融合框架，从三个维度显式建模对象一致性：

1. **视图一致性**：通过 Plücker 嵌入和时空相机编码器（ST-Encoder），将相机轨迹编码为具有几何可解释性的像素级表示，对齐相机射线与视觉特征；
2. **外观一致性**：通过语义引导策略（基于 ReferenceNet 的视觉-语言特征注入），稳定对象在强相机运动下的纹理和结构；
3. **运动一致性**：通过基于 2D 离散小波变换（2D-DWT）高频分解的对象感知掩码，将视频运动解耦为相机运动和对象运动两个独立成分。

这种“以 2D 约束反推 3D 感知”的策略，使得 MoCa 无需显式的 3D 重建模块，即可在生成过程中隐式学习相机与场景之间的 3D 关系，从而在保持计算效率的同时显著提升对象一致性表现。

## 核心方法与创新机理

MoCa 的核心创新在于将 3D 相机控制的视频生成问题重新定义为**对象一致性建模问题**，通过显式约束对象在视图、外观和运动三个维度上的一致性，隐式地学习相机与场景之间的 3D 关系，从而桥接 2D 像素空间与 3D 世界的鸿沟。与现有方法在 2D 像素空间直接集成相机条件不同，MoCa 通过以下四个关键设计（changed slots）实现了突破：

### 1. 从数值参数到几何可解释的 Plücker 嵌入

现有方法（如 **CameraCtrl** (He et al., 2024)、**AC3D** (Bahmani et al., 2024a)）通常将相机外参/内参直接线性投影后融合，缺乏对底层几何结构的显式编码。MoCa 采用 **Plücker 嵌入**（Sitzmann et al., 2021）将相机参数转化为几何可解释的表示：

$$\mathbf{p} = ( \mathbf{o} \times \mathbf{d}^{\prime}, \mathbf{d}^{\prime} )$$

其中 $\mathbf{d} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^{T} + \mathbf{t}$ 为从相机光心到像素的世界坐标射线方向，$\mathbf{o}$ 为相机中心，$\mathbf{d}^{\prime}$ 为归一化射线方向。该嵌入天然编码了每条像素射线在 3D 空间中的位置与方向，使得模型能够建立像素级视觉表示与相机几何之间的精确对齐。消融实验证实，使用 Plücker 嵌入替代数值相机参数后，相机控制误差（TransErr/RotErr）显著降低，对象与背景一致性同步提升（Table 2, W/O PLUCKER EMBEDDING vs Ours Full Attention Fusion）。

### 2. 从加法融合到交叉注意力融合

在相机条件与视频特征的融合方式上，CameraCtrl 和 AC3D 采用逐元素加法融合，信息交互能力有限。MoCa 改用 **DiT 块内的交叉注意力融合**，使得去噪网络能够动态地、有选择地关注相机轨迹中与当前生成帧最相关的时空信息。消融实验表明，交叉注意力融合在相机控制误差和视频质量指标（FID/FVD/CLIPSIM）上全面优于加法融合（Table 2, Addition Fusion vs Attention Fusion）。这一设计配合时空相机编码器（ST-Encoder），构成了完整的 **Camera Condition Module**，负责维持视图一致性。

### 3. 从无引导生成到语义引导的对象外观保持

现有方法缺乏对生成对象外观的显式约束，在强相机运动下容易出现纹理崩塌和对象几何失真。MoCa 引入基于 **ReferenceNet 的语义引导策略**，通过双分支框架（ReferenceNet + DenoisingNet）将视觉-语言特征注入去噪过程，稳定对象的外观表示。消融实验中移除语义引导后，生成视频出现严重对象变形（如海龟几何扭曲，Figure 6），量化指标上对象一致性（OC）和背景一致性（BC）均显著下降（Table 2, W/O SEMANTIC GUIDANCE），验证了该策略对维持外观一致性的关键作用。

### 4. 从运动纠缠到基于高频分解的运动解耦

现有方法将相机运动与对象运动混合处理，导致在相机与对象运动方向冲突时对象运动被相机运动覆盖或扭曲。MoCa 提出**对象感知运动解耦机制**：首先利用多级 2D 离散小波变换（2D-DWT）将视觉-语言特征分解为低频近似和高频细节：

$$\mathrm{DWT}( \mathbf{X} ) \to \{ \mathbf{LL}, \mathbf{LH}, \mathbf{HL}, \mathbf{HH} \}$$

通过丢弃低频分量 $\mathbf{LL}$ 并经由逆小波变换重建高频增强表示 $\mathbf{X}_{\mathrm{high}} = \mathrm{iDWT}( 0, \mathbf{LH}, \mathbf{HL}, \mathbf{HH} )$，得到对象感知掩码，该掩码能够精确捕获前景对象的结构与位置（Figure 7）。随后通过混合条件融合策略，将相机运动信号与对象运动信号解耦注入。在相机运动与文本指定的对象运动方向冲突的场景中（如鸟从右向左飞而镜头向右平移），MoCa 成功解耦两种运动，不扭曲对象运动方向（Figure 5）。消融实验中移除高频建模后，对象一致性和背景一致性均明显下降（Table 2, W/O HIGH-FREQUENCY MODELING），证实该机制是运动一致性的关键使能器。

**因果机制总结**：上述四个 changed slots 并非孤立改进，而是围绕“对象一致性建模”这一核心洞察形成因果链条——Plücker 嵌入和交叉注意力融合提供了精确的几何基础（视图一致性），语义引导策略在此基础上稳定了对象的纹理与结构（外观一致性），而高频运动解耦则确保对象运动不被相机运动污染（运动一致性）。三者协同作用，使得 MoCa 无需显式 3D 重建即可在 2D 生成过程中注入 3D 空间感知。

MoCa 是一个双分支融合框架，核心目标是通过显式建模对象一致性来桥接 2D 像素空间与 3D 场景之间的鸿沟。其设计动机源于一个关键观察：现有相机可控视频生成方法在 2D 像素空间直接集成相机条件，缺乏对底层 3D 场景的隐式理解，导致生成视频中对象的视图、外观和运动出现不一致，尤其在复杂动态场景下表现为纹理崩塌和对象失真。MoCa 的核心洞察在于：3D 场景中平滑的相机运动映射到 2D 视频时，必然产生一致的对象视图、外观和运动；反过来，通过约束这三种 2D 投影中的一致性，可以反向注入 3D 空间感知，从而绕开显式 3D 重建的需求。

### 双分支架构与数据流

MoCa 的整体架构由两个并行分支构成：**ReferenceNet** 和 **DenoisingNet**（见 Figure 2）。ReferenceNet 负责提取参考帧的视觉-语言特征，为对象外观保持提供语义锚点；DenoisingNet 则作为主生成分支，在扩散去噪过程中融合相机条件、语义引导和运动解耦信号，逐步生成目标视频帧。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/002_Figure_2.jpg]]
*Figure 2: The overview of MoCa. To maintain view consistency, we utilize the Camera Condition Module with Plucker embedding to align camera rays with pixel-level visual representation. For ¨ appearance consistency, a semantic guidance strategy employs ReferenceNet’s vision-language features to stabilize objects. Motion consistency is achieved by disentangling video motion into camera movement and object motion*

输入到输出的完整数据流如下：

1. **输入**：文本提示 $\mathbf{P}$ 和相机轨迹条件 $\dot{\mathbf{C}}$（包含每帧的内参和外参序列）。
2. **相机条件编码**：相机轨迹首先通过 **Plücker 嵌入** 转换为几何可解释的像素级表示 $\mathbf{p} = (\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，其中 $\mathbf{o}$ 为相机光心，$\mathbf{d}'$ 为归一化射线方向。射线方向由 $\mathbf{d} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^{T} + \mathbf{t}$ 计算，$\mathbf{R}$ 为旋转矩阵，$\mathbf{K}$ 为内参矩阵，$\mathbf{t}$ 为平移向量。随后，**时空相机编码器（ST-Encoder）** 将 Plücker 嵌入序列编码为时空潜变量，并通过 DiT 块内的交叉注意力机制注入 DenoisingNet，取代了 CameraCtrl 和 AC3D 中常用的逐元素加法融合方式。
3. **语义引导**：ReferenceNet 从参考帧提取视觉-语言特征，注入 DenoisingNet 以稳定对象外观，防止强相机运动下的纹理崩塌。
4. **运动解耦**：对视觉-语言特征应用多级二维离散小波变换（2D-DWT），分解为低频近似 $\mathbf{LL}$ 和高频细节 $\{\mathbf{LH}, \mathbf{HL}, \mathbf{HH}\}$。丢弃低频分量后通过逆小波变换重建高频增强表示 $\mathbf{X}_{\mathrm{high}} = \mathrm{iDWT}(0, \mathbf{LH}, \mathbf{HL}, \mathbf{HH})$，生成对象感知掩码。该掩码与相机条件通过混合条件融合策略结合，实现相机运动与对象运动的解耦。
5. **输出**：生成视频 $\mathbf{V}^{X \times Y \times T}$，其中 $X$、$Y$ 为像素坐标，$T$ 为时间维度。

### 三大一致性模块的协同关系

框架中的三个核心模块分别对应对象一致性的三个维度，形成互补的约束体系：

- **相机条件模块（Camera Condition Module）**：通过 Plücker 嵌入和 ST-Encoder 维持**视图一致性**，将相机射线与像素级视觉表示对齐，确保对象在相机运动过程中保持可见且结构稳定。
- **语义引导策略（Semantic Guidance Strategy）**：通过 ReferenceNet 注入视觉-语言特征来保持**外观一致性**，防止对象纹理在强相机运动下发生崩塌或几何扭曲。消融实验证实，移除该策略会导致严重对象失真（如海龟几何扭曲，见 Figure 6）。
- **对象感知运动解耦（Object-aware Motion Disentanglement）**：通过 2D-DWT 高频分解生成对象感知掩码，结合混合条件融合策略，将视频运动分解为相机运动和对象运动，确保**运动一致性**。在相机运动与文本指定的对象运动方向冲突的场景中（如鸟从右向左飞而镜头向右平移），该机制能成功解耦两种运动，不扭曲对象运动方向（见 Figure 5）。

这三个模块并非孤立运作，而是通过双分支架构中的特征融合机制协同作用：相机条件提供空间约束，语义引导提供外观锚定，运动解耦提供时序一致性，共同实现从 2D 像素生成到 3D 空间感知的隐式桥接。

**需要人工验证**：论文未明确披露 ReferenceNet 与 DenoisingNet 之间特征交互的具体层级和维度细节，上述数据流描述基于 Figure 2 的架构概览推断，建议对照原文方法部分确认。

### 补充图表

MoCa 围绕对象一致性建模这一核心洞察，构建了三个关键模块：**相机条件模块**（视图一致性）、**语义引导策略**（外观一致性）和**对象感知运动解耦**（运动一致性）。这三个模块通过一个双分支框架（ReferenceNet + DenoisingNet）协同工作，将 3D 场景中平滑相机运动所隐含的空间关系，通过 2D 投影中的一致性约束反向注入生成过程。

### 3.1 相机条件模块：Plücker 嵌入与时空编码

相机条件模块的目标是维持视图一致性，即确保相机运动过程中前景对象的结构和可见性保持稳定。其核心创新在于采用 **Plücker 嵌入**替代传统的数值相机参数线性投影。

对于每一帧的每个像素 $(u,v)$，首先从相机外参（旋转矩阵 $\mathbf{R}$、平移向量 $\mathbf{t}$）和内参（$\mathbf{K}$）计算世界坐标系下的射线方向：

$$\mathbf{d} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^{T} + \mathbf{t}$$

其中 $\mathbf{R} \mathbf{K}^{-1} [u, v, 1]^{T}$ 将像素坐标反投影到相机坐标系下的方向，加上 $\mathbf{t}$ 后得到世界坐标系下的射线方向。随后，基于相机光心 $\mathbf{o}$ 和归一化射线方向 $\mathbf{d}^{\prime}$ 构造 Plücker 嵌入：

$$\mathbf{p} = ( \mathbf{o} \times \mathbf{d}^{\prime}, \mathbf{d}^{\prime} )$$

该嵌入具有显式的几何可解释性：第一分量编码了射线的空间位置（光心到射线的力矩），第二分量编码了射线方向。与直接使用数值外参/内参相比，Plücker 嵌入在像素级别提供了与视觉特征空间更对齐的几何表示。

Plücker 嵌入随后输入 **时空相机编码器（ST-Encoder）**，生成时序连贯的相机条件特征，并通过 DiT 块内的**交叉注意力融合**机制注入去噪网络。消融实验证实（Table 2），交叉注意力融合在相机控制误差（TransErr/RotErr）和视频质量指标（FID/FVD/CLIPSIM）上全面优于 CameraCtrl 和 AC3D 等基线方法采用的逐元素加法融合。

### 3.2 语义引导策略：外观一致性

外观一致性的瓶颈在于：强相机运动下，生成模型容易丢失对象纹理细节，导致纹理崩塌或几何扭曲。MoCa 通过基于 **ReferenceNet** 的语义引导策略解决这一问题。

ReferenceNet 作为双分支框架中的参考分支，提取视觉-语言特征并注入去噪分支（DenoisingNet），为对象外观提供稳定的语义锚定。这种设计使得即使在剧烈相机运动下，对象也能保持纹理一致性。消融实验的定性结果（Figure 6）直观展示了该模块的关键作用：移除语义引导后，生成视频中的海龟出现显著的几何扭曲；定量结果（Table 2）进一步确认，语义引导策略大幅增强了对象外观一致性指标。

### 3.3 对象感知运动解耦：运动一致性

运动一致性的核心挑战在于：当相机运动与文本指定的对象运动方向冲突时（例如，鸟从右向左飞而镜头向右平移），现有方法往往让相机运动覆盖或扭曲对象运动。MoCa 通过 **2D 离散小波变换（2D-DWT）** 实现对象感知的运动解耦。

首先，对视觉-语言特征 $\mathbf{X}$ 进行多级 2D-DWT 分解：

$$\mathrm{DWT}(\mathbf{X}) \to \{ \mathbf{LL}, \mathbf{LH}, \mathbf{HL}, \mathbf{HH} \}$$

其中 $\mathbf{LL}$ 为低频近似分量，$\mathbf{LH}$、$\mathbf{HL}$、$\mathbf{HH}$ 分别为水平、垂直和对角方向的高频细节分量。由于前景对象的边缘和纹理集中在高频分量中，通过丢弃低频 $\mathbf{LL}$ 并执行逆小波变换，可重建出对象感知的高频掩码：

$$\mathbf{X}_{\mathrm{high}} = \mathrm{iDWT}(0, \mathbf{LH}, \mathbf{HL}, \mathbf{HH})$$

该掩码能够有效捕获前景对象的结构和定位信息，即使在多对象场景中也能准确提取所有对象的轮廓（Figure 7）。基于此掩码，MoCa 采用**混合条件融合**策略，将相机运动条件与对象运动条件在空间上解耦，确保相机运动不会覆盖对象的独立运动。在相机与对象运动方向冲突的场景中（Figure 5），MoCa 成功解耦两种运动，对象运动方向不被扭曲，体现了运动一致性的优势。消融实验（Table 2）表明，移除高频建模后，对象一致性和背景一致性均显著下降。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/009_Figure_7.jpg]]
*Figure 7: This figure presents a visualization of applying high-frequency decomposition to visual features in a latent space. Our strategy yields an object-aware mask that effectively captures the structure and localization of the foreground object. As shown in the right case, our high-frequency decomposition can accurately extract the structure of all objects, even in scenes containing multiple objects of different classes*

## 实验与关键发现

### 1. 实验设置

MoCa 在两个具有代表性的数据集上进行评估：**RealEstate10K**（静态场景，以相机运动为主）和 **VidGen**（动态场景，包含丰富的对象运动）。对比基线包括三类主流的相机可控视频生成方法：**MotionCtrl** (Wang et al., 2024b)、**CameraCtrl** (He et al., 2024) 和 **AC3D** (Bahmani et al., 2024a)。为保证公平比较，所有生成视频统一降采样至 16 帧并裁剪为相同尺寸。

评价指标覆盖三个维度：**视频质量**（FID↓、FVD↓、CLIPSIM↑）、**相机控制精度**（TransErr↓、RotErr↓）和**对象/背景一致性**（OC↑、BC↑、MS↑）。其中，对象一致性（OC）和背景一致性（BC）分别衡量前景对象和背景区域在相机运动过程中的结构保持能力，运动平滑度（MS）评估整体运动轨迹的自然程度。

### 2. 主实验结果

Table 1 展示了 MoCa 与各基线方法在 RealEstate10K 和 VidGen 上的量化对比。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on RealEstate10K and VidGen datasets. Lower is better (↓), higher is better (↑). Bold indicates top-1 performance*

**静态场景（RealEstate10K）**：MoCa 在视频质量指标上取得全面领先。FID 达到 **207.4**，相比最强的基线 AC3D（225.2）降低了 **17.8**；FVD 为 **667.9**，显著优于其他方法。这表明 MoCa 生成的视频在像素级分布和时序连贯性上均更接近真实数据。在 CLIPSIM（0.312 vs. 0.309）和对象一致性 OC（94.9% vs. 95.1%）上，MoCa 与 AC3D 基本持平，说明在静态场景中两者均能较好地保持对象结构。

**动态场景（VidGen）**：MoCa 的优势更为突出。FVD 达到 **1643.7**，较 AC3D（1712.0）降低 **68.3**；CLIPSIM 提升至 **0.349**（AC3D 为 0.345）；对象一致性 OC 从 93.5% 提升至 **94.7%**（+1.2%）。值得注意的是，在引入复杂对象运动后，MoCa 的运动平滑度 MS 仍保持 **98.3%**，与静态场景下的 98.5% 几乎无衰减。这一结果直接验证了运动解耦模块的有效性——MoCa 成功将相机运动与对象运动分离，避免了两种运动信号的相互干扰。

**关键洞察**：从 RealEstate10K 到 VidGen，场景动态性增加，AC3D 的 OC 从 95.1% 降至 93.5%（-1.6%），而 MoCa 仅从 94.9% 降至 94.7%（-0.2%）。这一对比揭示了一个深层机制：MoCa 通过显式建模对象一致性，在动态场景下具备更强的鲁棒性，而直接在 2D 像素空间融合相机条件的方法（如 AC3D）在面对对象运动时容易出现一致性退化。

### 3. 消融实验

Table 2 系统拆解了 MoCa 各核心组件的贡献，Figure 6 提供了定性佐证。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/008_Table_2.jpg]]
*Table 2: Ablation studies on RealEstate10K and VidGen datasets. Lower is better (↓), higher is better (↑). Bold indicates top-1 performance*

**Plücker 嵌入 vs. 数值相机参数**：将 Plücker 嵌入替换为数值外参/内参的直接线性投影后，相机控制误差显著上升（TransErr 和 RotErr 均恶化），同时对象一致性和背景一致性下降。这证实了几何可解释的射线表示对于建立像素级 2D 特征与 3D 相机运动之间的精确对应至关重要。Plücker 嵌入将相机位姿编码为射线原点与方向的叉积形式 $\mathbf{p} = (\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，使模型能够隐式学习场景深度结构，而非仅拟合数值映射。

**语义引导策略**：移除基于 ReferenceNet 的语义引导后，生成视频出现严重的对象失真。如 Figure 6 所示，海龟在强相机运动下发生显著的几何扭曲。量化指标上，对象一致性 OC 和 CLIPSIM 均明显下降。这一消融揭示了外观一致性建模的核心作用：视觉-语言特征的注入为去噪过程提供了稳定的语义锚点，防止纹理在相机视角变化时发生崩塌。

**高频对象掩码**：去掉基于 2D-DWT 的高频分解后，对象一致性和背景一致性同步下降。这验证了高频分量对于定位对象边界和结构的有效性。如 Figure 7 所示，通过丢弃低频近似分量 LL 并重建高频细节 $\mathbf{X}_{\mathrm{high}} = \mathrm{iDWT}(0, \mathbf{LH}, \mathbf{HL}, \mathbf{HH})$，模型能够生成精确的对象感知掩码，即使在多对象场景中也能准确提取每个对象的结构。

**交叉注意力融合 vs. 逐元素加法**：在相机条件注入方式上，交叉注意力融合在相机控制误差（TransErr/RotErr）和视频质量指标（FID/FVD/CLIPSIM）上全面优于 CameraCtrl 和 AC3D 采用的逐元素加法融合。这表明交叉注意力机制能更灵活地对齐相机射线特征与视觉 token，而非简单地将相机信息均匀叠加到所有空间位置。

### 4. 运动解耦的定性验证

Figure 5 展示了相机运动与文本指定的对象运动方向发生冲突时的生成结果。例如，当文本描述“鸟从右向左飞”而相机轨迹向右平移时，基线方法往往导致对象运动方向被相机运动覆盖或扭曲，而 MoCa 成功保持鸟向左飞的独立运动轨迹。这直接受益于运动解耦模块的设计：通过 2D-DWT 提取的高频对象掩码将视频运动分解为相机运动和对象运动两个分量，并在混合条件融合阶段分别注入相应的控制信号，从而避免信号纠缠。

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results of our method under the conflicting motion. It shows that our motion disentanglement strategy decouples object motion from camera movements effectively. The foreground object motion is not overridden or distorted by the camera input*

### 5. 局限性与失效模式

尽管 MoCa 在相机控制精度和对象一致性上取得显著提升，仍存在以下局限：

- **应用范围受限**：当前框架仅支持文本到视频的相机控制，未扩展至图像到视频、视频风格迁移等多模态输入场景。
- **对象位置不可控**：MoCa 无法精确约束移动对象在生成帧中的具体位置。在某些情况下，对象可能意外出现在画面边缘，影响构图质量。这一问题的根源在于对象运动解耦仅分离了运动模式，而未引入显式的位置约束信号。

### 6. 总结

MoCa 通过 Plücker 嵌入建立几何可解释的相机-像素对应，通过语义引导策略稳定对象外观，通过高频分解实现相机与对象运动的解耦，在静态和动态场景下均取得了领先的视频质量和对象一致性。消融实验证实，三个组件缺一不可，且交叉注意力融合是连接相机条件与视觉特征的最优方式。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_DZcpnudp7f/figures/012_Figure_10.jpg]]
*Figure 10: More qualitative comparison between our method and existing approaches*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

在视频生成领域，赋予用户对相机运动的精确控制能力是提升内容创作自由度的关键需求。现有方法通常将相机条件（如内外参矩阵）直接注入到2D像素空间的扩散模型中，但这一范式存在一个根本性瓶颈：**缺乏对底层3D场景的隐式理解**。当相机发生大幅平移、旋转或缩放时，2D像素空间中的对象必须经历符合3D几何规律的视图变换、外观保持和运动协调。直接进行2D条件映射的方法难以捕捉这种深层几何约束，导致生成视频中出现三类典型失效：

- **视图不一致**：对象在相机运动过程中发生非自然形变或结构崩塌；
- **外观不一致**：对象纹理在帧间漂移，尤其在强相机运动下出现纹理崩塌；
- **运动不一致**：相机运动与对象自身运动发生纠缠，相机轨迹覆盖或扭曲对象的独立运动方向。

这三类问题在动态场景中尤为突出，构成了相机可控视频生成领域的核心挑战。

### 2. 与现有工作的关系定位

MoCa 的方法设计建立在对三类现有工作的批判性继承之上：

**（1）相机可控视频生成基线**

当前主流方法包括 **MotionCtrl** (Wang et al., 2024b)、**CameraCtrl** (He et al., 2024) 和 **AC3D** (Bahmani et al., 2024a)。这些方法的共同范式是：将相机参数通过线性投影或轻量编码后，以逐元素加法（element-wise addition）的方式融合到扩散模型的去噪网络中。MoCa 在三个关键维度上对这一范式进行了系统性改造：

- **相机表示层面**：从数值外参/内参的直接编码升级为 **Plücker 嵌入**，将相机射线几何显式编码为可解释的六维向量 $\mathbf{p} = (\mathbf{o} \times \mathbf{d}', \mathbf{d}')$，其中 $\mathbf{o}$ 为相机光心，$\mathbf{d}'$ 为归一化射线方向。这一表示天然携带3D几何信息，为视图一致性提供了更强的归纳偏置。
- **条件融合层面**：从逐元素加法融合切换为 **交叉注意力融合**（cross-attention fusion），使相机条件能够以更灵活的方式与视觉特征交互，而非简单的逐通道偏移。
- **对象建模层面**：引入 **语义引导策略** 和 **运动解耦机制**，将对象一致性显式纳入优化目标，这是前述基线方法均未涉及的维度。

**（2）3D感知的视频生成**

MoCa 与显式3D重建方法（如 NeRF-based 或 3DGS-based 方法）形成了互补关系。后者通过显式建模场景的3D几何来保证多视图一致性，但计算开销大且泛化受限。MoCa 采取了一条不同的路径：**通过约束2D投影中的对象一致性来反向注入3D空间感知**。其核心洞察在于：3D场景中平滑的相机运动映射到2D视频时，自然产生一致的对象视图、外观和运动；反过来，强制这三种2D投影的一致性，等价于隐式地学习了相机与场景之间的3D关系，从而绕开了显式3D重建的需求。

**（3）运动解耦相关工作**

在运动解耦方面，MoCa 的 **2D-DWT 高频分解**策略具有独特定位。传统方法通常依赖光流估计或显式运动分割来实现相机与对象运动的分离，但这些方法在生成式框架中难以端到端训练。MoCa 利用小波变换将视觉-语言特征分解为低频近似 $\mathbf{LL}$ 和高频细节 $\{\mathbf{LH}, \mathbf{HL}, \mathbf{HH}\}$，通过丢弃低频分量后经逆变换得到高频增强表示 $\mathbf{X}_{\text{high}} = \text{iDWT}(0, \mathbf{LH}, \mathbf{HL}, \mathbf{HH})$，作为对象感知掩码。这一无参、可微的操作天然适合嵌入扩散模型的去噪流程。

### 3. 方法适用边界

MoCa 的设计决定了其适用边界：

- **输入模态边界**：当前框架仅支持文本到视频（T2V）的相机控制，未扩展至图像到视频（I2V）、视频编辑或多模态条件输入。这是架构层面的限制——语义引导策略依赖文本提示提供的视觉-语言特征，直接迁移到其他模态需要重新设计条件注入机制。
- **对象定位精度边界**：MoCa 能够保证对象在相机运动过程中的视图、外观和运动一致性，但**无法精确控制移动对象在生成帧中的具体位置**。在某些生成结果中，对象可能意外出现在画面边缘，影响构图质量。这一限制源于方法的隐式3D建模特性——它学习的是相机与场景的相对关系，而非对象的绝对空间坐标。
- **相机运动幅度边界**：消融实验显示，在强相机运动下（如大幅旋转和快速平移），语义引导策略对防止对象失真至关重要；但极端运动（如360°环绕）下的鲁棒性未在现有实验中充分验证，需要进一步评估。

### 4. 局限与开放问题

**已知局限：**

1. **模态单一性**：当前仅支持文本到视频的相机控制，应用范围受限。扩展到图像条件、视频编辑等多模态输入需要重新设计条件融合和语义引导机制。
2. **对象定位不可控**：无法精确约束运动对象在帧中的空间位置，有时导致构图不佳。
3. **计算开销**：双分支框架（ReferenceNet + DenoisingNet）和2D-DWT分解增加了推理成本，虽然在精度上带来了显著收益，但在资源受限场景下的部署可行性需要进一步优化。

**开放问题：**

1. **多模态扩展**：如何将相机控制能力从文本到视频推广到图像到视频、视频风格迁移等多模态任务？这需要设计通用的条件表示框架，使相机几何信息能够与不同模态的语义条件协同工作。
2. **精确位置控制**：如何在保持隐式3D感知优势的同时，引入对运动对象位置的精确约束？可能的路径包括结合稀疏关键点标注或引入可微渲染损失。
3. **长时序一致性**：当前实验集中在16帧的生成设置上，更长时间跨度的相机运动（如分钟级视频）下的对象一致性保持能力尚待探索，这可能涉及对长程时序依赖建模的架构改进。
4. **多对象场景泛化**：虽然高频分解在包含多个不同类别对象的场景中能够有效提取结构（如 Figure 7 所示），但在对象密集、相互遮挡的复杂场景下的鲁棒性需要更系统的评估。

## 原文 PDF

![[paperPDFs/ICLR_2026/MoCa_Modeling_Object_Consistency_for_3D_Camera_Control_in_Video_Generation_fe63ef4de104.pdf]]
