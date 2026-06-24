---
title: "Unified 3D Scene Understanding Through Physical World Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unified_3D_Scene_Understanding_Through_Physical_World_Modeling.pdf
openreview_forum_id: NQq9JLMfNN
aliases:
- 33WM
- U3SUTPWM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将光流作为显式中间动作空间，在统一概率图模型中构建不同的条件推理路径（如 RGB→Flow→RGB 用于生成，RGB+Camera→Flow 用于深度估计），从而在不改变模型结构的情况下实现多种三维任务的零样本切换。"
primary_logic: "通过将 RGB、光流与相机姿态等多模态场景元素统一表示为图节点，并采用局部随机访问序列与指针内容编码，可训练一个自回归变压器同时学习所有条件概率，使三维感知与操纵任务自然涌现为图中的不同推理路径，显著提升几何可控性与跨任务泛化能力。"
claims:
- "3WM 在未使用任务特定训练的情况下，在 WildRGB-D 和 DL3DV 数据集上以 PSNR 18.02 和 19.02 显著超越专用新视角合成模型。"
- "在 3DEditBench 上，3WM 的编辑一致性指标 EA 达到 0.797，明显优于扩散和拖拽式基线。"
- "消融实验证实：局部随机访问序列与光流中间表示对性能至关重要，采用光流控制比相机单独控制 PSNR 提升 3.53。"
- "在室内深度估计三大基准上，3WM 的自监督深度估计 AbsRel 分别为 0.078、0.084、0.137，大幅超越现有自监督方法。"
---

# Unified 3D Scene Understanding Through Physical World Modeling

> [!tip] 核心洞察
> 通过将 RGB、光流与相机姿态等多模态场景元素统一表示为图节点，并采用局部随机访问序列与指针内容编码，可训练一个自回归变压器同时学习所有条件概率，使三维感知与操纵任务自然涌现为图中的不同推理路径，显著提升几何可控性与跨任务泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过物理世界建模实现统一三维场景理解 |
| 英文题名 | Unified 3D Scene Understanding Through Physical World Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NQq9JLMfNN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3WM (3D World Model) |
| Dataset | WildRGB-D (NVS), DL3DV (NVS), SEVA RE10K (NVS), 3DEditBench (Object Manip.) |

> [!tip] 效果简介
> - WildRGB-D (NVS) 上，PSNR↑ 为 18.02，对比 16.14 (ZeroNVS)，变化 +1.88。
> - DL3DV (NVS) 上，PSNR↑ 为 19.02，对比 16.59 (ViewCrafter)，变化 +2.43。
> - SEVA RE10K (NVS) 上，PSNR↑ 为 21.54，对比 20.88 (ViewCrafter)，变化 +0.66。

## 概述

当前三维场景理解面临一个根本性瓶颈：深度估计、新视角合成、物体操纵等任务通常由孤立模型分别处理，缺乏统一的表征与跨任务知识迁移能力。现有生成式三维模型在几何一致性、精确可控性方面表现不足，难以灵活组合不同的感知与交互能力。

本文提出 **3WM（3D World Model）**，一个统一的物理世界模型，通过将光流作为显式中间动作空间，在统一概率图模型中构建不同的条件推理路径，从而在不改变模型结构的情况下实现多种三维任务的零样本切换。其核心洞察在于：将 RGB、光流与相机姿态等多模态场景元素统一表示为图节点，并采用局部随机访问序列与指针-内容编码，训练一个自回归变压器同时学习所有条件概率，使得三维感知与操纵任务自然涌现为图中的不同推理路径，显著提升了几何可控性与跨任务泛化能力。

在实验验证方面，3WM 在多个基准上展现出显著优势：
- **新视角合成**：在 WildRGB-D 和 DL3DV 数据集上，PSNR 分别达到 18.02 和 19.02，显著超越 ZeroNVS、ViewCrafter 等专用模型（Table 1）。
- **三维物体操纵**：在 3DEditBench 上，编辑一致性指标 EA 达到 0.797，PSNR 达到 22.73，明显优于 LightningDrag 等扩散和拖拽式基线（Table 2）。
- **自监督深度估计**：在 NYUv2、BONN、TUM 三大室内基准上，AbsRel 分别为 0.078、0.084、0.137，大幅超越 IndoorDepth 等现有自监督方法（Table 3）。

消融实验进一步证实，局部随机访问序列与光流中间表示对性能至关重要：采用光流控制比相机单独控制在新视角合成上 PSNR 提升 3.53，在深度估计上 AbsRel 从 0.173 降至 0.078（Table 4 & Table 5）。这些结果共同表明，3WM 通过统一的概率图建模与光流驱动的推理机制，为三维场景理解提供了一条可扩展的通用路径。

## 背景与动机

三维场景理解是计算机视觉的核心目标之一，涵盖深度估计、新视角合成（NVS）、三维物体操纵等关键任务。这些能力对于增强现实、机器人导航和内容创作等应用至关重要。然而，当前的研究范式存在一个根本性瓶颈：**各项任务通常由孤立模型分别处理，缺乏统一的表征框架与跨任务知识迁移机制**。

具体而言，现有方法面临以下结构性缺口：

**任务碎片化与模型孤立。** 深度估计依赖专门的单目或双目网络，新视角合成则由扩散模型或神经辐射场（NeRF）变体主导，而物体操纵往往需要额外的拖拽式编辑框架或三维感知管线。每个模型针对单一任务设计，无法共享场景几何与外观的底层理解，导致训练冗余且泛化能力受限。

**生成式三维模型的几何可控性不足。** 尽管扩散模型在图像生成上取得了显著进展，但将其应用于三维场景时，几何一致性与精确可控性仍是突出弱点。现有方法通常依赖隐式相机嵌入或粗略的语义控制信号，难以对场景中的物体位移、旋转和遮挡关系进行像素级精确操控。这限制了它们在真实世界交互场景中的实用性。

**统一物理世界建模的需求。** 人类对三维世界的理解是统一且多模态的——我们同时感知外观、运动与空间结构，并能灵活在这些模态间切换推理。构建具有类似能力的计算模型，需要一种能够**联合表示RGB、光流与相机姿态**的框架，并通过统一的推理接口支持多样化的三维任务，而非为每项任务设计专用架构。

本文的动机正是填补上述缺口：通过将三维场景理解重新表述为一个统一物理世界建模问题，使单一模型能够在零样本条件下切换于新视角合成、物体操纵和深度估计之间，同时保持几何精度与外观一致性。这一目标的实现依赖于两个核心设计选择——**将光流作为显式的中间动作空间**，以及**构建支持局部随机访问的图序列建模范式**——从而在不改变模型结构的前提下，让不同任务自然涌现为概率图中的不同推理路径。

## 核心创新

3WM 的核心创新并非单一技术的堆叠，而是**将三维场景理解重构为统一概率图模型中的条件推理问题**，并通过三项关键设计实现跨任务的零样本泛化与精确几何控制。

### 从孤立模型到统一概率图模型

传统方法将新视角合成、深度估计、物体操纵视为独立任务，分别采用扩散模型、控制网络或专用架构。3WM 的根本转变在于：将 RGB 图块、光流图块和相机姿态统一建模为概率图模型中的节点，所有任务共享同一个自回归变压器（Section 3.1, Figure 1）。该图模型定义为：

$$\Psi : ( X , p \not \in \operatorname { d o m } ( X ) ) \mapsto \{ \operatorname* { P r } [ ( p , v ) | X ] : v \in V \}$$

其中 $X$ 为已观测变量集，$p$ 为未观测节点指针，模型输出该节点取各离散值的概率。通过将图模型展开为指针-内容序列：

$$\Psi ( X , p ) \equiv \mathrm { P r } \left[ v _ { k } \ : \middle \vert \ : p _ { 0 } , v _ { 0 } , \ldots , p _ { k - 1 } , v _ { k - 1 } , p _ { k } \right]$$

训练一个 GPT 式因果变压器预测下一内容令牌 $v_k$，条件为历史指针-内容对及当前指针 $p_k$。这一范式转变使不同三维任务自然涌现为图中的不同推理路径，无需任务特定训练。

### 光流作为显式中介动作空间

与基线方法通过相机嵌入或隐式条件控制生成不同，3WM 将**光流作为显式中间控制表面**（Section 3.2, Figure 2）。这一设计是因果调节的关键杠杆：

- **新视角合成与物体操纵**：通过 $\Psi(\text{RGB}_0, \text{F}_{01}) \to \text{RGB}_1$ 路径，以光流 $\text{F}_{01}$ 为条件生成目标视角图像。
- **深度估计**：通过 $\Psi(\text{RGB}_0, \text{C}_{\text{in-plane}}) \to \text{F}_{01}$ 路径，从单张 RGB 和相机运动预测光流，再通过 $D_{\text{depth}} \propto 1/F_{\text{flow}}$ 提取深度。

消融实验证实了这一设计的决定性作用：在 WildRGB-D 新视角合成中，使用光流控制的 3WM 相比仅用相机控制的 3WM$_{\text{rgb}}$ PSNR 提升 3.53（Table 5 左）；在 NYU 深度估计中，直接预测光流的 AbsRel 为 0.078，显著优于从预测图像推导光流的 0.173（Table 5 右）。光流提供了对场景几何的直接操控，避免了相机参数中的尺度模糊性。

### 局部随机访问序列与指针-内容编码

传统自回归模型采用光栅扫描顺序，引入空间偏置且无法灵活查询任意区域。3WM 提出**局部随机访问序列建模**（Section 3.1, Figure 1），包含两个关键组件：

- **层次化局部量化器（HLQ）**：采用感受野严格限制在每个图块内的卷积自编码器，确保编码的局部性，避免 VQGAN 等全局量化器造成的图块间信息泄漏。
- **指针-内容令牌对**：将图节点序列化为（指针，内容）对，指针指明空间位置，内容为其离散代码。训练时随机打乱序列顺序，推理时可任意指定待预测的指针位置。

消融实验（Table 4）表明：在 100M 参数规模下，局部随机访问序列（Local & Random）相比局部光栅序列（Local & Raster）在 WildRGB-D 上 PSNR 提升 2.28；而采用 VQGAN 全局量化器时性能显著下降。这一设计使模型能够条件于、查询和更新任意空间区域，是实现多任务灵活推理的基础架构保障。

**总结**：3WM 的创新本质是以光流为中介动作空间，在统一概率图模型框架内通过局部随机访问序列实现多模态条件推理。三项设计相互依赖——光流提供几何可控性，指针-内容编码提供空间灵活性，统一图模型提供任务泛化性——共同构成了从“多模型分立”到“单模型统一”的范式跃迁。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/002_Figure_2.jpg]]
*Figure 2: Flexible inference pathways across modalities. Our framework allows us to flexibly construct inference pathways for 3D scene understanding. Using optical flow tokens as conditioning, the model performs image editing by generating the next RGB frame. Conversely, when optical flow tokens serve as the prediction target, the model enables depth estimation by predicting the next flow field from a single RGB image and in-plane camera motion input*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/001_Figure_1.jpg]]
*Figure 1: Local random access sequence modeling. Our modeling framework has three key components: (a) a local patch quantizer trained based on a small convolutional autoencoder; (b) a video serialization process based on a ”pointer-content representation”, which allows arbitrary ordering of the patches during training and generation; and (c) an LLM-like autoregressive transformer to predict the contents of the next patch, trained in random sequence order*

3WM 的核心设计理念是将三维场景理解统一到一个概率图模型（PGM）中，并通过自回归序列建模实现跨任务的灵活推理。整个框架由三个关键模块串联而成：层次化局部量化器（HLQ）、指针-内容序列化机制，以及一个 GPT 风格的自回归变压器。

**输入与模态统一。** 模型将 RGB 图像、光流场和相机姿态统一表示为图节点。具体而言，RGB 和光流被分割为局部 patch，每个 patch 作为一个节点；相机姿态则作为额外的条件节点注入图中。这种统一表示使得不同任务（新视角合成、物体操纵、深度估计）共享同一套模型参数，仅通过改变推理路径即可切换任务。

**层次化局部量化器（HLQ）。** 传统 VQGAN 等全局量化器在编码时可能引入跨 patch 的信息泄漏，破坏局部可控性。HLQ 采用一个小型卷积自编码器，其感受野严格限制在每个 patch 内部，确保编码的局部性。每个 RGB 或光流 patch 被量化为离散代码，作为后续自回归建模的词汇表（Figure 1a）。

**指针-内容序列化。** 这是实现随机访问和灵活条件推理的核心创新。每个图节点被序列化为一个“指针-内容”令牌对：指针令牌指示当前节点的空间位置和模态类型，内容令牌存储该节点的离散代码。训练时，模型以随机顺序遍历所有节点，学习条件概率 $ \mathrm{Pr}[v_k \mid p_0, v_0, \ldots, p_{k-1}, v_{k-1}, p_k] $。这种设计移除了光栅扫描顺序的偏差，使模型能够在推理时以任意顺序解码任意空间区域（Figure 1b）。

**自回归变压器。** 模型采用因果注意力机制的 GPT 风格变压器，根据历史指针-内容对和当前指针预测下一个内容令牌。训练目标是最小化所有可能序列顺序下的负对数似然，从而隐式学习图中所有条件分布 $ \Psi(X, p) $。推理时，给定已观测节点集 $ X $ 和目标节点指针 $ p $，模型自回归地生成该节点的内容（Figure 1c）。

**光流作为中间动作空间。** 框架的关键洞察在于将光流作为显式的几何控制表面。不同任务通过构建不同的推理路径实现：新视角合成和物体操纵使用 $ \Psi(\text{RGB}_0, F_{01}) \rightarrow \text{RGB}_1 $ 路径，以光流作为条件控制生成；深度估计则使用 $ \Psi(\text{RGB}_0, C_{\text{in-plane}}) \rightarrow F_{01} $ 路径，从相机运动预测光流，再通过 $ D_{\text{depth}} \propto 1/F_{\text{flow}} $ 提取深度（Figure 2）。这种设计使得模型无需任务特定的结构修改，即可在零样本条件下切换于感知与交互任务之间。

## 核心模块与公式推导

### 概率图模型形式化

3WM 将三维场景理解建模为一个统一概率图模型（PGM），其核心函数定义为：

$$\Psi : ( X , p \not \in \operatorname { d o m } ( X ) ) \mapsto \{ \operatorname* { P r } [ ( p , v ) | X ] : v \in V \}$$

其中 $X$ 为已观测变量集（可包含 RGB 图像块、光流块、相机姿态等节点），$p$ 为待查询的未观测节点指针，$V$ 为离散值空间（即量化码本）。该函数输出节点 $p$ 取各离散值 $v$ 的条件概率分布。这一形式化将多模态场景元素统一为图节点，使不同任务自然涌现为图中的不同推理路径（Section 3.1）。

### 自回归序列建模

为实现可扩展训练，该 PGM 被展开为指针-内容序列，由 GPT 式因果自回归变压器学习所有条件分布：

$$\Psi ( X , p ) \equiv \mathrm { P r } \left[ v _ { k } \ : \middle \vert \ : p _ { 0 } , v _ { 0 } , \ldots , p _ { k - 1 } , v _ { k - 1 } , p _ { k } \right]$$

其中 $p_i$ 为指针令牌（标识空间位置与模态类型），$v_i$ 为对应的内容令牌（离散化的 RGB 或光流值）。模型在训练时以随机序列顺序输入历史指针-内容对及当前指针 $p_k$，预测下一内容令牌 $v_k$。指针令牌消除了光栅扫描顺序偏差，支持对任意空间区域的灵活条件化与查询（Section 3.1）。

### 层次化局部量化器（HLQ）

为确保编码过程中每个图像块严格独立，3WM 采用层次化局部量化器（HLQ）替代全局量化器（如 VQGAN）。HLQ 是一个小型卷积自编码器，其感受野被限制在单个 patch 内，从而保证编码的严格局部性。消融实验证实，局部量化器（Local）相比 VQGAN 在 WildRGB-D 新视角合成任务上性能更优，结合随机访问序列策略后达到最佳整体表现（Table 4）。

### 光流作为中间动作空间

光流是 3WM 实现跨任务统一的核心控制信号。模型通过构建不同的条件推理路径实现任务切换：

- **新视角合成与物体操纵**：使用 $\Psi(\text{RGB}_0, F_{01}) \rightarrow \text{RGB}_1$ 路径，以源图像和光流场为条件生成目标图像。光流场通过相机运动或物体三维变换显式构造（Figure 7），提供精确几何操控。
- **自监督深度估计**：使用 $\Psi(\text{RGB}_0, C_{\text{in-plane}}) \rightarrow F_{01}$ 路径，从单张 RGB 图像和平面内相机运动生成光流场，再通过深度-光流关系提取深度图。

### 深度-光流关系

从相机运动诱导的光流场中提取深度图的核心关系为：

$$D_{\mathrm{depth}} \propto \frac{1}{F_{\mathrm{flow}}}$$

即深度与预测光流幅度成反比。这一简单关系使得模型无需显式深度监督即可从生成的光流中恢复 2.5D 几何信息（Section 3.3）。消融实验表明，直接预测光流（3WM）在 NYU 深度估计上 AbsRel 为 0.078，显著优于从预测图像间接推导光流的变体（3WM$_{\text{rgb}}$，AbsRel 0.173），验证了光流作为中间几何表示的关键作用（Table 5 右）。

## 实验与分析

### 核心实验设置

3WM 在三个三维理解任务上验证其统一框架的有效性：新视角合成（NVS）、三维物体操纵和自监督单目深度估计。所有任务共享同一预训练自回归变压器，无任何任务特定微调。为公平比较，对基线模型进行场景尺度搜索以对齐相机运动，输入图像统一居中裁剪或调整尺寸，评价指标仅在重叠区域计算；深度估计仅采用全局中值尺度对齐，不使用尺度-位移对齐。

### 新视角合成

3WM 利用 Ψ(RGB₀, F₀₁) → RGB₁ 推理路径，以光流作为显式中间控制信号实现可控新视角生成。在 WildRGB-D 和 DL3DV 评估集上，3WM 以 PSNR 18.02 和 19.02 显著超越所有专用基线（Table 1）：相较 ZeroNVS 提升 +1.88，相较 ViewCrafter 提升 +2.43。在 SEVA 基准的 RE10K 子集上，3WM 同样取得 21.54 PSNR 的最优结果。定性对比（Figure 3）显示，3WM 生成的新视角在物体和场景身份保持方面明显优于 MotionCtrl、ZeroNVS 等基线，未出现突兀的物体形变或场景跳变。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/004_Table_1.jpg]]
*Table 1: Comparison of metrics for novel view synthesis. The left block reports results on WildRGB-D and DL3DV from our evaluation set. The right block presents SEVA benchmark Zhou et al. (2025) performance on the small-viewpoint NVS setting using the Reconfusion split across DTU, LLFF, and RE10K datasets*

### 三维物体操纵

3WM 通过构建与目标三维变换（平移或旋转）对应的光流场，利用同一 Ψ(RGB₀, F₀₁) → RGB₁ 路径实现物体操纵。在作者构建的 3DEditBench（100 对含真实三维变换标注的图像对）上，3WM 在所有指标上均大幅领先（Table 2）：PSNR 达 22.73，较 LightningDrag 提升 +3.21；编辑一致性指标 EA 达 0.797，较最优基线提升 +0.075。Figure 4 的定性结果表明，3WM 在真实图像上能同时保持物体身份并产生逼真的编辑结果，而 DragAnything、DiffusionHandles 等方法在复杂遮挡场景下常出现身份漂移或几何失真。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/005_Table_2.jpg]]
*Table 2: Comparison of metrics for 3D object manipulation*

### 自监督单目深度估计

3WM 通过 Ψ(RGB₀, C_in-plane) → F₀₁ 推理路径预测光流，再利用深度与光流幅度的反比关系 $D_{\mathrm{depth}} \propto 1/F_{\mathrm{flow}}$ 提取深度图。在 NYUv2、BONN、TUM 三大室内基准上，3WM 的 AbsRel 分别为 0.078、0.084、0.137，大幅超越现有自监督方法 IndoorDepth（0.116、0.154、0.205）和 SC-DepthV2（Table 3）。值得注意的是，3WM 在动态场景（如包含行人的 TUM 数据集）上仍保持鲁棒性，而 MotionCtrl、SEVA 等生成式基线在相机运动可控性和几何理解方面明显不足（Figure 5）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/007_Table_3.jpg]]
*Table 3: Comparison of metrics for self-supervised monocular depth estimation on NYUD-v2, BONN, and TUM datasets*

### 涌现的几何推理能力

除上述标准任务外，3WM 展现出多种涌现的复杂几何推理能力（Figure 6）：(a) 联合物体操纵与新视角合成——模型可移开障碍物以显露自由空间，并模拟穿越新路径的导航；(b) 复杂自中心轨迹导航——模型沿复杂轨迹移动以揭示隐藏区域，并与物体同步运动；(c) 非模态完成——模型逐一移除附着物体以揭示背景几何，在 3DEditBench 被移除物体区域上，深度重建 AbsRel 低至 0.0263（Table 6），优于所有基线；(d) 多模态深度处理——对透明物体等深度歧义场景，模型能生成多个合理的深度输出。

### 消融实验

**局部随机访问序列**（Table 4）：在 100M 参数规模下，局部随机访问序列（Local & Random）相比光栅序列（Local & Raster）在 WildRGB-D 上 PSNR 提升 2.28；采用 VQGAN 全局量化器时，随机访问仍优于光栅顺序，但局部量化器进一步提升了场景可控性，取得最优整体性能。这证实了指针-内容编码与随机访问序列对灵活空间条件建模的关键作用。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_NQq9JLMfNN/figures/011_Table_4.jpg]]
*Table 4: Advantage of local random access sequence modeling. Comparison of 100M models with different tokenizers and sequence strategies shows the benefit of random access. Local tokens further improve controllability of the scene, yielding the best overall performance*

**光流作为控制信号**（Table 5）：在 NVS 任务上，以光流为显式控制信号的 3WM 相比仅用相机控制的变体 3WM_rgb，PSNR 提升 3.53（18.02 vs. 14.49）。在深度估计中，直接预测光流的 3WM 取得 AbsRel 0.078，而 3WM_rgb 从预测图像推导光流的 AbsRel 高达 0.173。这表明光流提供了对场景几何的直接操控，避免了相机控制中的尺度歧义问题。

### 失败模式与局限性

3WM 存在以下主要失败模式（Figure 11）：(a) **运动模糊**——由于训练数据来自真实视频，大位移物体操纵时模型倾向于复现运动引起的模糊，不利于精细操控；(b) **物体残留**——模型偶尔在原位置生成物体的重复副本；(c) **分割敏感性**——刚性物体操纵依赖输入分割质量，错误的分割会导致不可预测的形变结果。此外，模型推理速度尚未达到实时，限制了交互式应用场景。

### 光照与外观理解

Figure 8 展示了 3WM 对光照和外观的涌现理解：物体移动时高光随位置变化而适当调整，投射阴影随物体运动一致位移。尽管部分示例仍存在不完整的高光或阴影行为，但多数结果展现了对阴影和视角依赖外观的正确推理。作者指出，光照保真度主要受模型规模和数据多样性约束，而非方法本身的根本局限。

## 方法谱系与知识库定位

### 1. 与现有工作的关系

3WM 的核心贡献在于将原本孤立的多个三维感知与交互任务统一到一个单一的概率图模型与自回归序列框架中，这与当前“每个任务一个专用模型”的主流范式形成了根本性差异。

**新视角合成（NVS）**领域，现有方法大致分为两类：一类以 **MotionCtrl**、**ZeroNVS**、**ViewCrafter** 为代表，通常依赖扩散模型与显式或隐式的相机条件控制；另一类以 **SEVA** 为代表，探索了生成式模型在深度估计与视角合成间的部分共享。这些方法在各自基准上表现良好，但均针对 NVS 单独设计，无法迁移到物体操纵或深度估计。3WM 在 WildRGB-D 和 DL3DV 上分别以 PSNR 18.02 和 19.02 超越这些专用基线（Table 1），且在 SEVA 基准的 RE10K 子集上也达到 21.54，说明统一模型并未牺牲单任务性能。

**三维物体操纵**方面，**DragAnything**、**DiffusionHandles**、**LightningDrag** 等拖拽式或扩散式方法通过用户交互点或掩码实现编辑，但常面临物体身份保持困难和几何不一致问题。3WM 将物体操纵转化为光流场构建后的条件图像生成——即 Ψ(RGB₀, F₀₁) → RGB₁ 推理路径——从而在 3DEditBench 上取得了 PSNR 22.73 和编辑一致性指标 EA 0.797 的显著优势（Table 2）。这本质上得益于光流作为显式几何控制表面，比隐式条件或拖拽点更精确。

**自监督深度估计**领域，**SC-DepthV2** 和 **IndoorDepth** 等方法依赖光度一致性损失和专门设计的网络架构。3WM 则通过 Ψ(RGB₀, C_in-plane) → F₀₁ 路径直接预测光流，再利用关系 $D_{\mathrm{depth}} \propto \frac{1}{F_{\mathrm{flow}}}$ 提取深度，在 NYUv2、BONN、TUM 三大室内基准上分别达到 AbsRel 0.078、0.084、0.137，大幅超越现有自监督方法（Table 3）。值得注意的是，3WM 在此任务上未使用任何任务特定的训练或损失函数，深度估计能力完全作为物理世界建模的涌现属性出现。

### 2. 方法适用边界

3WM 的设计使其在以下场景中具有优势：
- **需要跨任务知识迁移的统一场景理解**：同一模型无需微调即可在 NVS、物体操纵、深度估计间零样本切换。
- **需要精确几何可控性的生成任务**：光流作为中间动作空间提供了比相机嵌入或隐式条件更直接的几何操控。
- **训练数据为真实视频序列**：模型从视频中学习物理世界的运动与外观规律，因此对真实场景的泛化能力较强。

然而，以下边界需要特别注意：
- **大位移运动模糊**：由于训练数据来自真实视频，模型在遇到大位移时会复现运动模糊伪影（Figure 11a），这在需要精细操控的场景中可能不可接受。
- **物体副本残留**：模型偶尔会在原始位置生成物体的副本（Figure 11b），表明对“物体已移动”这一物理约束的建模尚不完美。
- **分割质量敏感**：刚性物体操纵依赖输入分割来定义零光流区域，分割错误会导致不可预测的变形（Figure 11c）。
- **推理速度**：当前模型尚未达到实时，限制了交互式应用场景。

### 3. 局限性与开放问题

**已确认的局限性**（均有实验证据支撑）：
1. 运动模糊与物体副本问题已在 Figure 11 中记录，属于模型训练分布与理想编辑需求之间的系统性差距。
2. 光照真实感方面，Figure 8 显示模型在镜面高光和投影阴影上已有初步推理能力，但部分案例仍不完整，论文明确指出这主要受模型规模与数据多样性约束，而非方法本身的限制。

**值得关注的开放问题**：
1. **模型规模与光照真实感的 scaling law**：论文暗示增大模型与增加光照多样性数据可提升光照推理质量，但未给出定量 scaling 实验。这是一个可验证的后续方向。
2. **实时推理的工程化路径**：论文提到可通过 KV 缓存等标准优化加速，但未给出具体延迟数据或优化方案。对于交互式物理世界建模应用，这是关键瓶颈。
3. **导航与规划能力的评估**：Figure 6 展示了移动障碍物后导航、自我中心轨迹探索等涌现行为，但缺乏系统性的导航/规划基准评估。如何量化这些能力是一个值得探索的新方向。
4. **多物体组合操纵的泛化性**：Figure 9b 展示了通过分割掩码实现的选择性操纵，但未在定量实验中评估多物体场景下的编辑一致性。这一能力在实际应用中至关重要。

### 4. 知识库定位

3WM 在方法谱系中占据“统一物理世界模型”这一新兴节点。与传统的任务专用模型（如 NVS 的 ZeroNVS、深度估计的 IndoorDepth）相比，它提供了跨任务的统一表征；与现有的多任务生成模型（如 SEVA）相比，它通过光流中间表示实现了更强的几何可控性；与拖拽式编辑方法（如 DragAnything）相比，它将编辑操作纳入严格的物理运动建模框架。

该方法的核心技术支柱——层次化局部量化器（HLQ）、指针-内容序列化、局部随机访问序列——构成了一个可扩展的框架，允许未来通过增加新的节点类型（如语义标签、材质属性）来扩展建模能力。这一框架对后续研究者的启示在于：物理世界建模的突破口可能不在于设计更复杂的任务专用架构，而在于找到合适的中间表示（此处为光流）和灵活的序列建模策略，使多种物理推理能力自然涌现。

## 原文 PDF

![[paperPDFs/ICLR_2026/Unified_3D_Scene_Understanding_Through_Physical_World_Modeling.pdf]]
