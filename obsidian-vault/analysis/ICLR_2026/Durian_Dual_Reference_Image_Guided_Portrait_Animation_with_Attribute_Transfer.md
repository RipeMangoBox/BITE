---
title: "Durian: Dual Reference Image-Guided Portrait Animation with Attribute Transfer"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Durian_Dual_Reference_Image_Guided_Portrait_Animation_with_Attribute_Transfer.pdf
openreview_forum_id: tz5GRv9Vzu
aliases:
- Durian
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "自重建训练范式：利用同一视频的两帧作为伪配对，配合互补掩码强制模型分离身份与属性。"
primary_logic: "双参考网络（Dual ReferenceNet）通过分别提取属性与身份特征，并通过空间注意力将其融合去噪，实现无需配对数据的跨身份属性迁移，并天然支持多属性组合与插值。"
claims:
- "自重建训练使用同一视频的两帧分别作为属性参考和身份参考，通过互补掩码强制分离。"
- "双参考网络设计通过独立的ARNet和PRNet提取特征，并由空间注意力融合到去噪U-Net中。"
- "掩码扩展策略与增强方案有效弥合自重建训练与跨身份推理之间的领域鸿沟。"
- "在自属性迁移重建指标上全面超越所有基线（Table 1），且在用户研究中获得 76.50% 的最优偏好（Table 4）。"
---

# Durian: Dual Reference Image-Guided Portrait Animation with Attribute Transfer

> [!tip] 核心洞察
> 双参考网络（Dual ReferenceNet）通过分别提取属性与身份特征，并通过空间注意力将其融合去噪，实现无需配对数据的跨身份属性迁移，并天然支持多属性组合与插值。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Durian：双参考图像引导的肖像动画与属性迁移 |
| 英文题名 | Durian: Dual Reference Image-Guided Portrait Animation with Attribute Transfer |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tz5GRv9Vzu); [Project](https://hyunsoocha.github.io/durian) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Durian |
| Dataset | Self-Attribute Transfer (Hair) |

> [!tip] 效果简介
> - Self-Attribute Transfer (Hair) 上，L1 ↓ 为 0.0744。
> - Self-Attribute Transfer (Hair) 上，PSNR ↑ 为 18.83。
> - Self-Attribute Transfer (Hair) 上，LPIPS ↓ 为 0.1565。

## 概述

### 问题瓶颈

肖像动画与属性迁移的核心挑战在于：**跨身份属性迁移缺乏成对训练数据**。理想情况下，模型需要同一人物在“有/无某属性”的成对样本才能学习身份与属性的解耦，但这类数据在真实场景中几乎不可获取。直接从单一视频学习时，模型极易将身份与属性信息纠缠在一起，导致跨身份迁移时身份泄露或属性丢失。

### 核心方法

Durian 提出了一套**自重建训练范式**来解决上述瓶颈。其核心思路是：利用同一视频的两帧构造伪配对——一帧作为属性参考，另一帧作为身份参考——并通过**互补掩码**强制模型分离两类信息。具体而言，属性参考图像仅保留目标属性区域（如头发、眼镜），肖像参考图像则将该属性区域移除，使两个参考分支分别专精于属性和身份特征的提取。

在此基础上，Durian 设计了**双参考网络（Dual ReferenceNet）**，包含独立的属性编码器（ARNet）和肖像编码器（PRNet），分别从掩码后的参考图像中提取多尺度空间特征。两组特征通过**空间注意力（Spatial Attention）**注入扩散模型的去噪 U‑Net 中，以空间感知的方式融合身份与属性信息，实现单次前向传播即可完成属性迁移与动画生成。

为弥合自重建训练与跨身份推理之间的领域鸿沟，Durian 引入了**属性感知的掩码扩展策略**与**轻量级参考图像增强**（随机仿射变换、FLUX 出画修复、颜色抖动），并在推理时通过 **Face Aligner** 估计对齐后的属性掩码，缓解姿态和形状不匹配问题。

### 方法定位

在现有方法谱系中，Durian 处于**扩散模型驱动的视频生成**与**属性编辑/迁移**的交叉地带。与分步式方案（如先编辑后动画化的 PbE、TriplaneEdit 结合 LivePortrait）不同，Durian 将属性迁移与动画生成统一在单次前向传播中完成，避免了级联误差。相较于依赖单一 ReferenceNet 或共享编码器的先前工作，双参考网络设计是 Durian 的核心差异化组件，使其能够在无配对数据的条件下实现跨身份属性迁移。

### 主要结果

在自属性迁移（头发类别）的重建指标上，Durian 全面超越所有基线：L1 达到 0.0744，PSNR 18.83，LPIPS 0.1565，FID 38.00（Table 1）。在眼镜类别上，相比 TriplaneEdit + LivePortrait 组合，L1 降低 0.073，FID 降低 30.69（Table 3）。用户研究中，Durian 在跨属性迁移任务上获得 **76.50%** 的最优偏好，远超 PbE + LivePortrait 的 19.04%（Table 4）。

消融实验揭示了几个关键因果机制：
- **掩码扩展策略**的移除会显著降低生成质量，模型无法适应多样化的属性空间范围；
- **参考图像增强**的移除使性能下降，表明空间和光度增强对跨身份泛化至关重要；
- 将双参考网络替换为**单一 ReferenceNet** 会破坏身份与属性的解耦，导致跨身份迁移失败；
- 使用**无掩码的全参考图像输入**虽在自重建指标上表现最优，但在跨身份迁移时完全失效——这说明模型走了“捷径”而非真正解耦；
- 推理时省略 **Face Aligner** 会导致动画中出现间歇性伪影（如头发时隐时现），对齐对稳定性影响显著。

### 局限与开放问题

当前模型在**极端光照不匹配**（如暗蓝光肖像与明亮白日光属性）时，属性外观无法完全适应目标照明；当肖像存在**明显遮挡**（如手部遮挡面部）时，鼻部附近可能出现伪影。评估方面，自属性迁移本质上是重建质量报告，不能完全反映真实跨身份迁移性能。支持的属性类别主要受限于分割掩码可覆盖的区域（头发、胡子、眼镜、帽子），难以直接迁移年龄、疤痕等复杂语义属性。

开放问题包括：框架能否扩展到非面部属性（如服装）并保持零样本泛化？能否端到端地学习更鲁棒的跨身份形状保持？多属性组合质量是否随属性数量增加而显著下降？

## 背景与动机

肖像动画生成旨在根据驱动信号（如面部关键点序列）使静态肖像图像动起来，同时保持人物身份的一致性。近年来，基于扩散模型的方法（如 **LivePortrait** (Guo et al., 2024)、**X-Portrait** (Xie et al., 2024)、**MegActor-Σ** (Yang et al., 2025)）在生成高质量、时间连贯的肖像动画方面取得了显著进展。然而，这些方法通常假设动画前后的属性（如发型、眼镜、胡须）保持不变，缺乏对肖像面部属性进行灵活迁移与编辑的能力。

与此同时，图像属性编辑与迁移领域涌现出多种方法。基于提示的编辑方法（PbE）可生成合成发型等属性，而 **HairFusion** (Chung et al., 2025)、**StableHair** (Zhang et al., 2025) 等专注于发型迁移，**TriplaneEdit** (Bilecen et al., 2024) 则支持眼镜等属性的编辑。但这些方法存在一个共同的瓶颈：它们将属性迁移和动画生成视为两个独立的串行阶段——先编辑属性再驱动动画，这不仅导致流程繁琐，更在两个阶段之间引入了身份不一致和运动失真的累积误差。

更深层的困境在于，跨身份属性迁移本质上缺乏成对的训练数据。我们无法获得“同一个人在不同属性下的同一动作”的真实配对，这使得直接从单一视频中学习身份与属性的解耦变得极为困难。现有方法要么依赖合成数据，要么在推理时进行复杂的优化，难以在保持身份一致性的同时实现高质量的属性迁移。

针对上述问题，本文提出 **Durian**，一种双参考图像引导的肖像动画与属性迁移框架。Durian 的核心动机在于：**将属性迁移与动画生成统一到单个扩散模型的前向过程中，并通过自重建训练范式规避对成对数据的依赖**。具体而言，Durian 利用同一视频的两帧构建伪配对——一帧作为属性参考，另一帧作为身份参考——并配合互补掩码策略，强制模型在去噪过程中分离并重组身份与属性信息。这一设计使得模型能够直接从无标注的野生视频中学习，同时天然支持多属性组合与属性插值，无需额外训练。

## 核心创新

Durian 的核心创新在于通过**双参考网络架构**与**自重建训练范式**，在不依赖任何成对跨身份数据的情况下，实现了单阶段、零样本的肖像动画与属性迁移。其关键设计可归纳为以下五个方面。

### 1. 双参考网络：身份与属性的显式解耦

现有肖像动画方法（如 **LivePortrait** Guo et al., 2024、**X-Portrait** Xie et al., 2024）通常采用单一 ReferenceNet 或共享编码器处理参考图像，无法有效分离身份信息与外观属性。Durian 提出**双参考网络（Dual ReferenceNet）**架构，由两个独立编码器组成：

- **属性参考网络（ARNet）**：接收仅保留属性区域的掩码图像 $\tilde{I}_{\text{attr}}$，提取多尺度属性特征 $\mathcal{F}_{\text{attr}}$；
- **肖像参考网络（PRNet）**：接收去除属性区域后的掩码肖像图像 $\tilde{I}_{\text{port}}$，提取多尺度身份特征 $\mathcal{F}_{\text{port}}$。

两路特征通过**空间注意力（Spatial Attention）**注入去噪 U-Net（DNet）——将目标帧特征、肖像特征与属性特征沿宽度维度拼接后执行缩放点积注意力：

$$\bar{\mathbf{F}}_{t}^{\tau,l} = \text{SA}(\mathbf{F}_{t}^{\tau,l}, \mathbf{F}_{\text{port}}^{l}, \mathbf{F}_{\text{attr}}^{l})$$

消融实验证实，将双参考网络替换为单一 ReferenceNet（通道维拼接双输入）会导致身份与属性特征纠缠，跨身份迁移完全失效（Figure 5）。

### 2. 自重建训练：利用视频内伪配对规避数据瓶颈

跨身份属性迁移的根本瓶颈在于缺乏成对训练数据——无法为同一身份获取具有不同属性（如不同发型）的配对真值。Durian 的解决方案是**自重建（self-reconstruction）策略**：从同一视频中采样两帧分别作为属性参考和身份参考，构成伪配对。

训练时，对两帧施加**互补掩码**——属性参考帧仅保留目标属性区域，肖像参考帧则移除该属性区域。模型被强制从属性参考中提取外观信息、从肖像参考中提取身份信息，并在 DNet 中融合重建原始帧。这一设计使模型学会解耦身份与属性，而无需任何跨身份标注。

### 3. 掩码扩展与增强策略：弥合训练-推理域鸿沟

自重建训练中，属性区域的空间范围相对固定，而跨身份推理时属性区域可能显著不同（如从短发迁移到长发）。为弥合这一域鸿沟，Durian 引入两项关键设计：

- **属性感知的掩码扩展**：训练时对属性掩码进行随机膨胀/腐蚀，模拟多样化的空间覆盖范围；
- **参考图像增强**：对参考图像施加随机仿射变换（平移、缩放、旋转），并使用 **FLUX** 出画修复模型填充新暴露区域，同时辅以颜色抖动。

定量消融（Table 2）表明，去除掩码扩展或参考图像增强均导致 L1、PSNR、LPIPS 等指标显著恶化，且在跨身份迁移中产生明显伪影（Figure 5）。值得注意的是，若直接使用完整参考图像（无掩码）训练，模型虽在自重建指标上达到最优（L1=0.0670, PSNR=19.47），但在跨身份迁移时完全失败——模型学会了利用身份信息作为“捷径”，而非真正解耦。

### 4. 推理时对齐模块：Face Aligner

跨身份迁移中，属性参考与目标肖像的姿态、形状可能严重不匹配。Durian 在推理时引入**Face Aligner**模块，利用轻量级图像到3D化身模型（Chu & Harada, 2024）估计对齐后的属性掩码，而非直接使用原始分割掩码。消融显示（Figure 8），移除 Face Aligner 会导致动画中间歇性伪影（如头发时隐时现），对齐对生成稳定性至关重要。

### 5. 原生多属性组合与插值

双参考网络架构天然支持多属性迁移与属性插值，无需额外训练：

- **多属性组合**：将多个属性特征沿宽度维拼接后输入空间注意力，实现单次前向传播组合多种属性（如发型+眼镜+胡须+帽子）；
- **属性插值**：对两个属性参考的特征进行线性加权混合 $\bar{\mathbf{F}}_t^{\tau,l} = (1-\alpha)\bar{\mathbf{F}}_t^{\tau,l,1} + \alpha\bar{\mathbf{F}}_t^{\tau,l,2}$，实现平滑的属性过渡，甚至适用于眼镜、帽子等刚性物体。

## 整体框架

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Training Pipeline. Given an attribute-masked portrait image $\tilde { \mathbf { I } } _ { \mathrm { p o r t } }$ and an attribute-only image $\tilde { \mathbf { I } } _ { \mathrm { a t t r } }$ , Durian synthesizes a portrait animation with the transferred attribute. These inputs are constructed by randomly sampling two frames from a training video and applying the estimated masks. A sequence of facial keypoints $\{ k _ { \tau } \} _ { \tau = 1 } ^ { F }$ is extracted from the video to guide the motion. During generation, spatial features from PRNet and ARNet are fused via spatial attention into the DNet, ensuring identity preservation and attribute consistency in the synthesized video

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/003_Figure_3.jpg]]
*Figure 3: Aligned Attribute Mask Estimation. To improve attribute-portrait alignment, we estimate an aligned attribute mask via Face Aligner*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/001_Figure_1.jpg]]
*Figure 1: Portrait Animation with Attribute Transfer. Given a portrait image and single or multiple reference images specifying target attributes (e.g., hairstyle, eyeglasses), our method generates a portrait animation with facial attribute transfer conditioned on a keypoint sequence*

Durian 的生成目标是在给定属性参考图像、肖像图像及其对应掩码和驱动关键点序列的条件下，直接生成一段具有目标属性的肖像动画视频。其核心函数形式为：

$$\mathbf{V} = \mathrm{Durian}(\mathbf{I}_{\mathrm{attr}}, \mathbf{M}_{\mathrm{attr}}, \mathbf{I}_{\mathrm{port}}, \mathbf{M}_{\mathrm{port}}, \mathbf{K})$$

其中 $\mathbf{I}_{\mathrm{attr}}$ 为属性参考图像，$\mathbf{M}_{\mathrm{attr}}$ 为属性掩码，$\mathbf{I}_{\mathrm{port}}$ 为肖像图像，$\mathbf{M}_{\mathrm{port}}$ 为肖像掩码，$\mathbf{K}$ 为驱动关键点序列，输出 $\mathbf{V}$ 为 $F$ 帧的动画视频。模型在单次前向传播中同时完成属性迁移与动画生成，无需分步处理。

### 训练流程

Durian 采用基于肖像视频的自重建训练策略，避免了对成对跨身份标注数据的依赖。其训练流程（Figure 2）如下：

1. **伪配对构建**：从同一视频中采样两帧，一帧作为属性参考，另一帧作为身份参考。通过分割模型获取属性掩码后，对属性参考图像保留属性区域（$\tilde{\mathbf{I}}_{\mathrm{attr}} = \mathbf{I} \odot \mathbf{M}_{\mathrm{attr}}$），对肖像图像去除属性区域（$\tilde{\mathbf{I}}_{\mathrm{port}} = \mathbf{I} \odot (1 - \mathbf{M}_{\mathrm{port}}^{\mathrm{train}})$），形成互补掩码输入。训练掩码 $\mathbf{M}_{\mathrm{port}}^{\mathrm{train}} = \mathbf{M}_{\mathrm{attr}} \cup \mathbf{M}_{\mathrm{gen}}$ 是原始属性掩码与生成掩码的并集。

2. **掩码扩展与增强**：为弥合自重建训练与跨身份推理之间的领域鸿沟，引入属性感知的掩码扩展策略以模拟多样化的空间覆盖范围，并对参考图像施加随机仿射变换（平移、缩放、旋转）和 FLUX 出画修复，以及颜色抖动等光度增强。

3. **双参考网络特征提取**：掩码后的属性图像和肖像图像分别经过预训练 VAE 编码为潜在表示，并与下采样掩码沿通道维拼接，形成 $(c+1)$ 通道输入：

   $$\tilde{z}_{\mathrm{attr}} = \mathrm{concat_c}(z_{\mathrm{attr}}, m_{\mathrm{attr}}), \quad \tilde{z}_{\mathrm{port}} = \mathrm{concat_c}(z_{\mathrm{port}}, m_{\mathrm{port}})$$

   随后分别送入属性参考网络（ARNet）和肖像参考网络（PRNet），提取多尺度空间特征图 $\mathcal{F}_{\mathrm{attr}}$ 和 $\mathcal{F}_{\mathrm{port}}$。

4. **特征融合与去噪生成**：ARNet 和 PRNet 提取的特征被注入到去噪 U-Net（DNet）中，通过空间注意力（Spatial Attention）机制将目标帧特征、肖像特征和属性特征沿宽向拼接后进行融合：

   $$\mathbf{F}_{\mathrm{ref},t}^{\tau,l} := \mathrm{concat}_{\mathrm{w}}(\{\mathbf{F}_{t}^{\tau,l}, \mathbf{F}_{\mathrm{port}}^{l}, \mathbf{F}_{\mathrm{attr}}^{l}\})$$

   同时利用 CLIP/ArcFace 嵌入通过跨注意力（Cross-Attention）增强身份感知和属性一致性。

5. **两阶段训练**：第一阶段使用单帧去噪扩散损失训练空间模块；第二阶段插入时间自注意力（Temporal Self-Attention）到各 U-Net 块中，仅优化时间注意力参数以保证视频的时间一致性。

### 推理流程

推理时（Figure 3），Durian 引入 Face Aligner 模块以缓解属性参考与目标肖像之间的姿态和形状不匹配问题。该模块利用轻量级图像到 3D 头像模型进行属性-肖像对齐，估计对齐后的属性掩码，从而提高跨身份迁移的稳定性。多属性迁移时，多个属性特征沿宽向拼接后通过空间注意力融合，掩码则通过并集操作组合：

$$\mathbf{M}_{\mathrm{port}}^{\mathrm{infer}} = \mathbf{M}_{\mathrm{port}}^{\mathrm{init}} \cup \bigcup_{k=1}^{N_{\mathrm{attr}}} \mathbf{M}_{\mathrm{attr}}^{\mathrm{align},k}$$

模型天然支持零样本多属性组合与属性插值，无需额外训练。

## 核心模块与公式推导

### 双参考网络架构

Durian 的核心架构由三个主干模块构成：**属性参考网络（ARNet）**、**肖像参考网络（PRNet）** 和 **去噪 U‑Net（DNet）**。ARNet 与 PRNet 共享结构但参数独立，分别接收互补掩码后的输入，从属性区域和身份区域提取多尺度空间特征。

给定属性图像 $\mathbf{I}_{\mathrm{attr}}$ 和肖像图像 $\mathbf{I}_{\mathrm{port}}$，首先通过分割模型获得对应的二值掩码，再经 VAE 编码为潜在表示。掩码经下采样后沿通道维与潜在表示拼接，形成 $(c+1)$ 通道的输入：

$$
\tilde{z}_{\mathrm{attr}} = \mathrm{concat_c}(z_{\mathrm{attr}}, m_{\mathrm{attr}}), \quad
\tilde{z}_{\mathrm{port}} = \mathrm{concat_c}(z_{\mathrm{port}}, m_{\mathrm{port}})
$$

ARNet 和 PRNet 各自从这些掩码潜在表示中提取 $L$ 层多尺度特征图：

$$
\mathcal{F}_{\mathrm{attr}} := \{\mathbf{F}_{\mathrm{attr}}^{l}\}_{l=1}^{L} = \mathcal{E}_{\mathrm{attr}}(\tilde{z}_{\mathrm{attr}}; \boldsymbol{\Theta}_{\mathrm{attr}})
$$
$$
\mathcal{F}_{\mathrm{port}} := \{\mathbf{F}_{\mathrm{port}}^{l}\}_{l=1}^{L} = \mathcal{E}_{\mathrm{port}}(\tilde{z}_{\mathrm{port}}; \boldsymbol{\Theta}_{\mathrm{port}})
$$

### 空间注意力融合

DNet 是扩散模型的主干，负责根据驱动关键点序列生成视频帧。在每个 U‑Net 块的原始自注意力位置，Durian 将其替换为**空间注意力（Spatial Attention, SA）**，通过宽向拼接将目标帧特征、肖像特征和属性特征融合为一个联合特征图，再执行缩放点积注意力：

$$
\mathbf{F}_{\mathrm{ref},t}^{\tau,l} := \mathrm{concat}_{\mathrm{w}}(\{\mathbf{F}_{t}^{\tau,l}, \mathbf{F}_{\mathrm{port}}^{l}, \mathbf{F}_{\mathrm{attr}}^{l}\}) \in \mathbb{R}^{c_l \times h_l \times 3w_l}
$$

$$
\bar{\mathbf{F}}_{t}^{\tau,l} = \mathrm{SA}(\mathbf{F}_{t}^{\tau,l}, \mathbf{F}_{\mathrm{port}}^{l}, \mathbf{F}_{\mathrm{attr}}^{l}) = \mathrm{Attention}(\mathbf{W}_Q \mathbf{F}_{t}^{\tau,l}, \mathbf{W}_K \mathbf{F}_{\mathrm{ref},t}^{\tau,l}, \mathbf{W}_V \mathbf{F}_{\mathrm{ref},t}^{\tau,l})
$$

其中 $\tau$ 为帧索引，$l$ 为层索引，$\mathbf{W}_Q, \mathbf{W}_K, \mathbf{W}_V$ 为可学习的投影矩阵。该设计使模型在空间维度上显式区分身份区域与属性区域，是实现身份‑属性解耦的关键操作。

### 跨注意力语义注入

为进一步增强身份感知和属性一致性，Durian 在 ARNet、PRNet 和 DNet 的特定层后插入跨注意力（Cross‑Attention, CA），以 CLIP 或 ArcFace 嵌入作为条件信号：

$$
\mathrm{CA}(\bar{\mathbf{F}}, \phi) = \mathrm{Attention}(\mathbf{W}_Q' \bar{\mathbf{F}}, \mathbf{W}_K' \phi, \mathbf{W}_V' \phi)
$$

$$
\tilde{\mathbf{F}}_{\{\mathrm{attr},\mathrm{port}\}}^{l} = \mathrm{CA}(\bar{\mathbf{F}}_{\{\mathrm{attr},\mathrm{port}\}}^{l}, \phi_{\{\mathrm{attr},\mathrm{port}\}}), \quad
\tilde{\mathbf{F}}_{t}^{\tau,l} = \mathrm{CA}(\bar{\mathbf{F}}_{t}^{\tau,l}, \phi_{\mathrm{attr}})
$$

### 时间扩展与训练策略

为生成时序连贯的视频，Durian 在每个 U‑Net 块中插入时间自注意力层（Temporal Self‑Attention），沿用 Hu (2024) 和 Zhu et al. (2024) 的方案。训练分两阶段进行：

**第一阶段**（单帧训练）：仅优化空间注意力与跨注意力，损失为标准的去噪扩散损失：

$$
\mathcal{L}_{\mathrm{diff}}^{(1)} = \mathbb{E}_{z_0,\epsilon,t}\left[\left\|\epsilon - \epsilon_\theta(z_t, t, \mathcal{C}, \mathbf{F}_{\mathrm{kpt}})\right\|^2\right]
$$

**第二阶段**（多帧训练）：冻结空间模块，仅优化时间注意力，损失扩展为 $F$ 帧联合去噪：

$$
\mathcal{L}_{\mathrm{diff}}^{(2)} = \mathbb{E}_{\{z_0^{(\tau)}\}_{\tau=1}^F,\epsilon^{1:F},t}\left[\left\|\epsilon^{1:F} - \epsilon_\theta(\{z_t^{(\tau)}\}_{\tau=1}^F, t, \mathcal{C}, \{\mathbf{F}_{\mathrm{kpt}}^{\tau}\}_{\tau=1}^F)\right\|^2\right]
$$

### 多属性组合与插值

Durian 天然支持零样本多属性组合。给定 $N_{\mathrm{attr}}$ 个属性参考，将各属性特征沿宽向拼接后输入空间注意力：

$$
\bar{\mathbf{F}}_t^l = \mathrm{SA}(\mathbf{F}_t^l, \mathbf{F}_{\mathrm{port}}^l, \mathrm{concat_w}(\mathbf{F}_{\mathrm{attr}}^{l,1}, \mathbf{F}_{\mathrm{attr}}^{l,2}, \cdots, \mathbf{F}_{\mathrm{attr}}^{l,N_{\mathrm{attr}}}))
$$

对应的推理掩码为初始肖像掩码与所有对齐属性掩码的并集：

$$
M_{\mathrm{port}}^{\mathrm{infer}} = M_{\mathrm{port}}^{\mathrm{init}} \cup \bigcup_{k=1}^{N_{\mathrm{attr}}} M_{\mathrm{attr}}^{\mathrm{align},k}
$$

对于属性插值，Durian 对两个属性参考的空间注意力输出进行线性加权，实现平滑过渡：

$$
\bar{\mathbf{F}}_t^{\tau,l} = (1-\alpha) \bar{\mathbf{F}}_t^{\tau,l,1} + \alpha \bar{\mathbf{F}}_t^{\tau,l,2}, \quad \alpha \in [0,1]
$$

### 推理时对齐模块

跨身份推理时，属性图像与目标肖像的姿态和形状可能存在显著不匹配。Durian 引入 **Face Aligner** 模块，利用轻量级图像到 3D 化身模型（Chu & Harada, 2024）估计对齐后的属性掩码，替代训练时的原始分割掩码，有效缓解因未对齐导致的生成伪影。该模块仅用于推理，不参与训练。

## 实验与分析

### 实验设置

Durian 的训练分为两个阶段：第一阶段在单帧上训练基础扩散模型（不含时间注意力），第二阶段冻结除时间自注意力外的所有参数，在视频片段上进行微调。训练数据来自大规模肖像视频数据集，通过自重建设置构造伪配对——从同一视频中采样两帧，分别作为属性参考和身份参考，并施加互补掩码。评估涵盖自属性迁移（同身份重建）和跨属性迁移（跨身份泛化）两种设定。自属性迁移使用 L1、PSNR、SSIM、LPIPS、FID 等全参考指标，跨属性迁移因缺乏成对真值，主要依赖用户研究和定性视觉对比。

### 主实验结果

**自属性迁移（头发类别）**。Table 1 显示，Durian 在所有重建指标上全面超越基线组合（发型合成方法 + 动画驱动方法）。具体而言，Durian 取得 L1 0.0744、PSNR 18.83、SSIM 0.6527、LPIPS 0.1565、FID 38.00，在像素精度、感知质量和分布相似性三个维度均达到最优。需要指出，自属性迁移本质上是重建任务——属性参考和身份参考来自同一视频的相邻帧，模型只需还原已知外观，因此这些指标主要反映重建保真度，不能完全代表跨身份迁移的实际能力。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison. We compare our method with recent approaches that (1) synthesize portraits with transferred hairstyles, and (2) animate the synthesized portrait image*

**自属性迁移（眼镜类别）**。Table 3 中，Durian 与 **TriplaneEdit**（Bilecen et al., 2024）结合 **LivePortrait**（Guo et al., 2024）的级联基线进行对比。Durian 在五项指标上全面领先：L1 从 0.151 降至 0.078，FID 从 106.28 降至 75.59，降幅分别达 48.3% 和 28.9%。这表明双参考网络的一体化生成范式在刚性小物体（眼镜）的迁移上也优于“编辑-后驱动”的级联方案。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/028_Table_3.jpg]]
*Table 3: Quantitative Comparison on Eyeglasses Category. Our method outperforms this baseline on every evaluation metric*

**跨属性迁移的用户研究**。Table 4 报告了用户偏好结果：Durian 获得 76.50% 的参与者偏好，远超 **PbE + LivePortrait**（19.04%）和 **TriplaneEdit + LivePortrait**（4.45%）。这一压倒性优势表明，自重建设训练配合掩码扩展与增强策略，有效弥合了训练-推理的领域鸿沟，在真实跨身份场景中保持了属性迁移的视觉质量和身份一致性。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/029_Table_4.jpg]]
*Table 4: User Study. We conduct a user study on two baseline methods that achieve strong performance in both self-attribute transfer and cross-attribute transfer. Our approach receives the highest preference among participants*

**定性对比**。Figure 4 展示了跨身份迁移的视觉对比：级联基线（X-Portrait + StableHair）在发型迁移时出现明显的身份泄露或纹理模糊，而 Durian 能保持目标肖像的身份特征，同时准确复现参考发型的形状和纹理。Figure 10–12 进一步提供了头发和眼镜类别的自属性与跨属性迁移定性结果。

### 消融实验

Table 2 和 Figure 5 系统消融了 Durian 的关键设计选择：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_tz5GRv9Vzu/figures/008_Table_2.jpg]]
*Table 2: Ablation Study. Bold indicates the best, underline the second*

**掩码扩展策略（w/o mask expansion）**。移除属性感知的掩码扩展后，模型在训练中仅见过原始分割掩码的空间范围，导致推理时对多样化属性区域（如蓬松发型 vs. 紧贴头皮的短发）的泛化能力下降，生成质量出现明显退化。定量上，L1 从 0.0744 升至 0.0811，LPIPS 从 0.1565 升至 0.1692。

**参考图像增强（w/o ref. image aug.）**。禁用随机仿射变换、FLUX 出画修复和颜色抖动后，模型在跨身份迁移中难以应对空间错位和光照差异，性能显著下降（L1 升至 0.0801，LPIPS 升至 0.1716）。这验证了空间和光度增强对弥合域鸿沟的关键作用。

**参考掩码输入（w/o ref. mask input）**。将掩码从参考输入中移除后，模型失去了显式的空间定位信号，身份与属性的融合出现混乱。定量指标全面恶化，表明掩码通道为空间注意力提供了不可或缺的“在哪里迁移”的空间先验。

**双参考网络 vs. 单一 ReferenceNet（single ReferenceNet）**。将 ARNet 和 PRNet 替换为共享编码器（接收沿通道维拼接的肖像和属性图像）后，模型在跨身份迁移中完全失效——身份特征与属性特征在编码阶段即发生纠缠，空间注意力无法有效解耦。Figure 5 的定性结果显示了严重的身份污染和属性模糊。

**全参考图像输入（full ref. image input）**。一个关键的消融变体是使用无掩码的完整参考图像。该变体在 Table 2 的自重建指标上取得最优（L1 0.0670, PSNR 19.47），但在跨身份迁移中彻底失败（Figure 5 及附录 C.2）。原因在于模型学到了“复制粘贴”的快捷方式——直接利用完整参考图像中的像素信息进行重建，而非学习身份与属性的解耦表示。这一结果深刻揭示了自重建训练中互补掩码的必要性：掩码是强制解耦的因果调控旋钮，缺少它，模型将绕过属性迁移的核心挑战。

**Face Aligner 消融**。Figure 8 显示，推理时移除 Face Aligner 会导致动画中出现间歇性伪影，例如头发区域在部分帧中时隐时现。这是因为属性掩码与目标肖像的姿态/形状未对齐时，空间注意力的特征注入位置发生偏移。Face Aligner 通过轻量级图像到 3D 模型估计对齐后的属性掩码，显著提升了时序稳定性。

### 属性掩码敏感度分析

Figure 9 展示了生成质量对属性掩码精度的敏感度。通过对掩码施加不同程度的腐蚀和膨胀，观察到：适度的掩码扩展（模拟推理时的不完美分割）对质量影响有限，但过度腐蚀（掩码过小）导致属性迁移不完整，过度膨胀（掩码过大）则引入背景污染。这表明模型对掩码误差具有一定的鲁棒性，但极端偏差仍会损害输出质量。

### 多属性组合与属性插值

Durian 的空间注意力机制天然支持多属性组合。Figure 6 展示了同时迁移发型、眼镜、胡须和帽子四种属性的结果——模型在单次前向传播中完成组合，无需额外训练。其实现原理是将多个属性特征沿宽向拼接后输入空间注意力（Eq. 12），让去噪 U-Net 在不同空间位置选择性关注不同属性源。

Figure 7 展示了属性插值能力：通过对两个属性参考的空间注意力特征进行线性加权（Eq. 14），模型可生成平滑的属性过渡动画，即使对于帽子、眼镜等刚性物体也能保持几何一致性。这一零样本能力源于空间注意力特征空间的线性可插值性。

### 失败模式与局限性

尽管 Durian 在多数场景下表现优异，论文明确指出了以下失败模式：

1. **光照不一致**：当属性参考与目标肖像的光照条件极端不匹配时（如暗蓝光下的肖像与明亮日光下的属性），生成结果的属性外观无法完全适应目标照明，出现视觉不协调。
2. **遮挡伪影**：当目标肖像存在明显面部遮挡（如手部遮挡）时，鼻部附近可能出现伪影，尽管整体运动和属性迁移仍保持稳健。
3. **评估局限性**：跨身份迁移缺乏成对真值，定量评估依赖用户研究；自属性迁移指标本质上是重建质量，可能高估模型在真实跨身份场景中的表现。
4. **属性类别受限**：当前支持的属性主要限于分割掩码可覆盖的区域（头发、胡子、眼镜、帽子），难以直接迁移年龄、疤痕等复杂语义属性。

这些失败模式为后续改进提供了明确方向：引入光照归一化或自适应外观融合模块、增强对遮挡的鲁棒性、探索超越分割掩码的属性表示方式。

## 方法谱系与知识库定位

### 任务定位：肖像动画与属性迁移的交叉点

Durian 处于两个任务线的交汇处：**肖像动画生成**与**面部属性编辑/迁移**。传统上，这两类任务由独立的模型串行完成——先通过属性编辑方法修改肖像外观，再将编辑结果送入动画模型生成动态视频。这种流水线式方案存在明显的级联误差：编辑阶段引入的伪影会被动画模型放大，且两阶段之间缺乏联合优化，难以保证时间一致性。

Durian 的核心贡献在于将属性迁移与动画生成统一到**单次前向扩散过程**中。给定属性参考图像、肖像图像、对应的分割掩码以及驱动关键点序列，模型直接输出具有目标属性的动画视频 $\mathbf{V} = \mathrm{Durian}(\mathbf{I}_{\mathrm{attr}}, \mathbf{M}_{\mathrm{attr}}, \mathbf{I}_{\mathrm{port}}, \mathbf{M}_{\mathrm{port}}, \mathbf{K})$。这一范式消除了串行流水线中的信息瓶颈，使属性迁移与运动生成在特征空间中协同优化。

### 与基线方法的关系

#### 肖像动画基线

Durian 的动画能力建立在扩散式肖像动画生成的基础上，与以下方法共享技术基因：

- **LivePortrait**（Guo et al., 2024）和**X-Portrait**（Xie et al., 2024）：这两者代表了基于关键点驱动的扩散肖像动画范式。Durian 继承了其关键点条件注入和时间自注意力机制（"by inserting temporal self-attention into each U-Net block, following Hu (2024); Zhu et al. (2024)"），但将原本用于单一身份重建的 ReferenceNet 扩展为双分支架构。
- **MegActor-Σ**（Yang et al., 2025）：同样面向肖像动画，但未涉及跨身份属性迁移。

这些基线在自属性重建场景下可作为对比对象，但它们**不具备跨身份属性迁移能力**。论文实验中的基线组合（如 X-Portrait + StableHair）本质上是将动画模型与属性编辑模型强行拼接，Durian 的一体化设计正是针对这种拼接方案的改进。

#### 属性编辑/迁移基线

- **StableHair**（Zhang et al., 2025）和**HairFusion**（Chung et al., 2025）：专注发型迁移，但仅生成静态图像，需要额外动画模型才能产生动态结果。
- **PbE (Prompt-based Editing)**：通过文本提示编辑属性，可生成合成发型等，但编辑精度受限于文本描述的粒度，且同样需要后续动画步骤。
- **TriplaneEdit**（Bilecen et al., 2024）：支持眼镜等属性的图像编辑，但仅输出静态帧。

Durian 与这些方法的本质区别在于：**属性迁移发生在扩散去噪的特征空间中，而非像素空间的显式编辑**。通过双参考网络（ARNet + PRNet）分别提取属性与身份的多尺度空间特征，再经空间注意力融合，Durian 隐式地学习了属性与身份的解耦表示，而非依赖显式的编辑操作。

### 核心技术决策的谱系分析

#### 双参考网络 vs 单一 ReferenceNet

在扩散式生成模型中，ReferenceNet 通常作为条件编码器提取参考图像特征并注入去噪 U-Net。Durian 的关键改动是将单一 ReferenceNet 拆分为 **ARNet（属性参考网络）** 和 **PRNet（肖像参考网络）** 两个独立编码器。消融实验（Figure 5, "single ReferenceNet"）表明，将双分支替换为共享编码器并沿通道维拼接输入时，模型"fails to separate the roles of the two references"，跨身份迁移能力显著退化。

这一设计的深层动机在于：**身份保持与属性迁移在特征空间中需要不同的归纳偏置**。PRNet 需要保留面部的结构信息（轮廓、五官位置），而 ARNet 需要捕捉属性的外观细节（发型纹理、眼镜形状）。共享编码器难以同时满足这两种需求，因为身份和属性的特征分布在训练信号中高度纠缠。

#### 自重建训练范式的创新与局限

Durian 的训练策略是整个方法的知识论核心。其瓶颈在于：**跨身份属性迁移缺乏成对真值数据**——不存在"同一个人、同一姿态、不同属性"的标注视频对。论文的解决方案是**自重建训练**（self-reconstruction）：从同一视频中采样两帧，一帧作为身份参考（移除属性区域），另一帧作为属性参考（仅保留属性区域），通过互补掩码强制模型从两个不完整输入中重建原始帧。

这一范式的因果逻辑是：
1. 互补掩码切断了模型通过"复制粘贴"完成重建的捷径；
2. 模型必须学习从属性参考中提取外观信息，从身份参考中提取结构信息；
3. 在特征空间中通过空间注意力将两者融合，隐式形成解耦表示。

消融实验提供了有力的因果证据：**全参考图像输入变体**（无掩码）在自重建指标上取得最优（L1 0.0670, PSNR 19.47, Table 2），但在跨身份迁移时完全失效（Figure 5, "full ref. image input"）。这表明无掩码训练让模型学会了依赖"快捷方式"（直接复制参考图像），而非真正的身份-属性解耦。

然而，这一训练范式也带来了**评估偏差**：Table 1 的主定量比较本质上是自重建精度的排名，并不能直接反映跨身份迁移的真实质量。论文对此有清醒认识，因此补充了用户研究（Table 4, 76.50% 偏好率）来弥补成对真值缺失的问题。

#### 领域鸿沟弥合策略

自重建训练与跨身份推理之间存在显著的领域鸿沟（domain gap）：训练时属性参考与身份参考来自同一视频（姿态、光照、背景一致），推理时两者可能来自完全不同的个体和场景。Durian 通过三层策略弥合这一鸿沟：

1. **属性感知的掩码扩展**（mask expansion）：训练时对属性掩码进行随机膨胀/腐蚀，模拟推理时属性空间范围的多样性。消融（Table 2, "w/o mask expansion"）显示去除该策略导致所有指标下降。
2. **参考图像增强**：随机仿射变换（平移、缩放、旋转）+ FLUX 出画修复 + 颜色抖动。这些增强模拟了推理时的空间错位和光照差异。消融（Table 2, "w/o ref. image aug."）证实其必要性。
3. **推理时的 Face Aligner**：利用轻量级图像到3D模型估计属性参考与目标肖像之间的对齐变换，生成更精确的属性掩码。消融（Figure 8）显示省略该模块会导致"间歇性伪影（如头发时隐时现）"。

### 适用边界与局限

#### 已知局限

1. **光照不一致**：当属性参考与目标肖像的光照条件极端不匹配时（如暗蓝光肖像与明亮白日光属性），模型无法完全自适应目标照明，生成结果存在光照断裂。这源于训练数据中缺乏足够的光照多样性——自重建训练天然保证了光照一致性，削弱了模型对光照变化的泛化能力。

2. **遮挡敏感**：当肖像存在明显遮挡（如手部遮挡面部）时，鼻部附近可能出现伪影。尽管整体运动和属性迁移仍保持稳健，但局部区域的生成质量下降。

3. **属性类别受限**：当前支持的属性主要受限于分割掩码可覆盖的区域（头发、胡子、眼镜、帽子等）。对于无法通过语义分割掩码定位的属性（如年龄、疤痕、妆容风格），框架难以直接迁移。这暴露了基于掩码的属性定义方式的根本局限——属性的语义边界并不总是与分割边界重合。

4. **评估生态不完善**：跨身份属性迁移缺乏标准化的成对真值数据集，导致定量评估严重依赖自重建指标和主观用户研究。Table 1 的数值优势可能夸大了模型在实际跨身份场景中的相对性能。

#### 适用场景

- **强适用**：发型、眼镜、帽子、胡子等空间上可分割的属性的跨身份迁移与动画生成；单次前向的多属性组合（Figure 6）；属性间的平滑插值（Figure 7）。
- **谨慎适用**：光照差异较大的跨场景迁移（可能出现不一致）；存在面部遮挡的肖像（可能出现局部伪影）。
- **不适用**：非空间可分割的语义属性（年龄、表情风格等）；需要实时交互的场景（扩散模型推理延迟较高）。

### 开放问题

1. **属性空间的扩展边界**：能否将 Durian 的掩码-双参考范式扩展到非面部属性（如服装、配饰）并保持零样本泛化？这需要解决两个子问题：更复杂的空间形变（服装随身体运动产生非刚性变形）和更稀疏的分割标注。

2. **端到端的形状保持**：当前模型在严重姿态变化的跨身份动画中，面部形状保持仍依赖外部的 Face Aligner 模块。能否将形状对齐内化到扩散过程中，实现端到端的鲁棒跨身份形状保持？这可能需要引入3D可形变模型作为中间表示。

3. **多属性组合的冲突消解**：多属性组合的生成质量是否会随属性数量增加而显著下降？当前的空间注意力通过宽向拼接实现多属性融合，但缺乏显式的优先级或冲突消解机制。当多个属性在空间上重叠或语义上冲突时（如帽子与发型），模型可能产生不一致的结果。

4. **推理效率与交互性**：扩散模型的迭代去噪过程限制了实时交互的可能性。能否通过一致性蒸馏或对抗性加速将 Durian 的推理时间压缩到交互式应用的阈值内？

5. **域外泛化**：模型依赖预训练扩散先验，在极端非真实感风格（如高度抽象卡通）上虽有一定泛化，但仍可能出现结构破坏。如何在不牺牲真实感性能的前提下强化风格泛化能力，是一个开放的设计挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Durian_Dual_Reference_Image_Guided_Portrait_Animation_with_Attribute_Transfer.pdf]]
