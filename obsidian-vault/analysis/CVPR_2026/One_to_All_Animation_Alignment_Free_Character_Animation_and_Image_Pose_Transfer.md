---
title: "One-to-All Animation: Alignment-Free Character Animation and Image Pose Transfer"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/One_to_All_Animation_Alignment_Free_Character_Animation_and_Image_Pose_Transfer.pdf
project_link: "https://ssj9596.github.io/one-to-all-animation-project/"
code_link: "https://github.com/ssj9596/One-to-All-Animation"
aliases:
- OAA
- OAAAFCAIPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过自我监督的outpainting训练范式模拟空间错位，并设计身份鲁棒姿态控制来解耦身份特征与驱动骨骼，使模型能够从任意布局的参考图像生成高质量动画。
primary_logic: 将训练重构为统一遮挡输入格式下的outpainting任务，迫使网络学习补全被遮挡区域并保留身份信息，同时结合面部区域增强与参考引导的姿态控制，避免姿态过拟合，实现对齐自由的个性化生成。
claims:
- 在TikTok和Cartoon数据集上，One-to-All-14B的FID-VID（13.93 vs 17.42）和FVD（297.94 vs 358.42）均显著优于UniAnimate-DiT。
- 在DeepFashion图像姿态迁移任务中，本方法在512×352分辨率下FID 6.85和LPIPS 0.249均为最优；高分辨率（944×624）下FID 6.92依然领先。
- 用户研究证实，在非对齐场景下，本方法在未见区域质量（47.6% vs 28.1%）和已见区域保真度（72.4% vs 16.1%）上大幅超越Wan-Animate。
- 身份鲁棒姿态控制消融实验显示，全模型CSIM达0.8172，去除面部增强或参考引导后指标明显下降。
---

# One-to-All Animation: Alignment-Free Character Animation and Image Pose Transfer

> [!tip] 核心洞察
> 将训练重构为统一遮挡输入格式下的outpainting任务，迫使网络学习补全被遮挡区域并保留身份信息，同时结合面部区域增强与参考引导的姿态控制，避免姿态过拟合，实现对齐自由的个性化生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一对多动画：无对齐的角色动画与图像姿态迁移 |
| 英文题名 | One-to-All Animation: Alignment-Free Character Animation and Image Pose Transfer |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22940) · [Project](https://ssj9596.github.io/one-to-all-animation-project/) · [Code](https://github.com/ssj9596/One-to-All-Animation) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | One-to-All Animation |
| Dataset | TikTok, Cartoon, DeepFashion, User Study |

> [!tip] 效果简介
> - TikTok 上，FID-VID↓ 13.93 (One-to-All-14B) vs 17.42 (UniAnimate-DiT) (-3.49)；FVD↓ 297.94 (One-to-All-14B) vs 358.42 (UniAnimate-DiT) (-60.48)。
> - Cartoon 上，FVD↓ 403.47 (One-to-All-14B) vs 485.92 (Wan-Animate) (-82.45)。
> - DeepFashion (512×352) 上，LPIPS↓ 0.249 (One-to-All-1.3B) vs 0.275 (MCLD) (-0.026)。

## 概述

**One-to-All Animation** 提出了一种统一的姿态驱动个性化生成框架，旨在解决现有角色动画方法对空间对齐与骨骼匹配的刚性依赖。传统方法（如 **MimicMotion**、**StableAnimator**、**UniAnimate-DiT**、**Wan-Animate**）在参考图像与驱动视频之间出现空间布局错位或面部骨骼不一致时，生成质量急剧下降——身份信息丢失、出现严重伪影或肢体扭曲（Figure 2）。

本工作的核心洞察是：**将训练重构为自监督的 outpainting 任务**。通过在训练阶段对面部区域进行随机遮挡来模拟空间错位，迫使网络学会补全被遮挡区域并保留身份信息；同时设计身份鲁棒姿态控制来解耦身份特征与驱动骨骼，避免姿态过拟合。这一对齐自由的范式使模型能够从任意布局的参考图像生成高质量动画。

在方法定位上，One-to-All Animation 对扩散视频生成骨干进行了四项关键改造：

1. **Outpainting 预处理**：以面部为中心的随机掩码训练 + 推理时的姿态引导平移，统一处理多样的身体比例与空间布局。
2. **参考提取器与混合参考融合注意力（HRFA）**：专用参考网络提取多级外观特征，通过交叉注意力注入去噪骨干，支持变分辨率和动态帧数。
3. **身份鲁棒姿态控制**：面部区域增强有意制造面部骨骼不一致性，配合参考引导姿态控制稳定训练，实现身份与姿态的解耦。
4. **Token Replace 长视频策略**：利用前一片段的上下文令牌替换当前片段的初始潜变量，实现片段间的平滑过渡。

实验表明，在 **TikTok** 和 **Cartoon** 视频动画基准上，14B 规模的模型在 FID-VID（13.93 vs 17.42）和 FVD（297.94 vs 358.42）上均显著优于 UniAnimate-DiT（Table 1）；在 **DeepFashion** 图像姿态迁移任务中，FID 6.85 和 LPIPS 0.249 均达到最优（Table 2）。用户研究进一步证实，在非对齐场景下，本方法在未见区域质量（47.6% vs 28.1%）和已见区域保真度（72.4% vs 16.1%）上大幅超越 Wan-Animate（Figure 7）。

消融实验验证了各组件的必要性：身份鲁棒姿态控制的全模型 CSIM 达 0.8172，去除面部增强或参考引导后指标明显下降（Table 4）；Token Replace 策略使 FVD 从 355.2 降至 297.9（Table 3）；HRFA 中将交叉注意力查询的 RoPE 帧维度设为 0 是避免长视频生成崩溃的关键设计（Figure 13）。

**局限性与开放问题**：14B 模型推理需 65 GB 显存且单次推理超过 7 分钟，限制了消费级部署；图像与视频训练数据的最佳混合比例尚未充分探索；当前仅依赖 2D 姿态序列，无法独立控制摄像机运动。这些方向为后续工作留下了明确的改进空间。

## 背景与动机

### 问题定义与核心瓶颈

角色动画（character animation）的目标是，给定一张参考图像（提供角色身份与外观）和一段驱动视频（提供运动姿态），生成该角色执行驱动视频中动作的连贯视频。这一任务在虚拟数字人、影视制作、社交媒体内容生成等领域有广泛应用。

现有方法普遍依赖一个隐含假设：**参考图像与驱动视频之间保持空间对齐**——即角色在参考图像中的位置、尺度和身体比例与驱动视频第一帧大致匹配。当这一假设成立时，方法如 **MimicMotion**（Zhang et al., arXiv 2024）、**StableAnimator** 和 **Animate-X** 等可以生成高质量结果。然而，**实际应用场景中空间错位（spatial misalignment）是常态而非例外**：参考图像可能是任意构图的人物照片，驱动视频可能来自不同拍摄距离和角度的动作序列。此时，依赖对齐的方法会出现严重的身份失真、肢体断裂和背景伪影（见 Figure 2）。

更深层的瓶颈在于**面部骨骼不一致**问题。当驱动视频中人物的面部骨骼结构（如眼距、下颌形状）与参考角色不同时，现有方法倾向于将驱动姿态的骨骼特征“过拟合”到生成结果中，导致角色身份发生不可控的漂移——这被称为**姿态过拟合（pose overfitting）**。这一问题的本质是，现有方法未能有效解耦身份特征与姿态骨骼结构。

### 现有方法缺口

当前主流角色动画方法可归为以下几类，各有结构性局限：

- **基于对齐的重建范式**：如 MimicMotion、StableAnimator 等，在训练时假设参考帧与驱动帧逐像素对齐，通过自重建（self-reconstruction）学习身份保持。当推理时出现空间错位，模型缺乏处理遮挡区域和布局差异的能力。
- **基于扩散模型的直接生成**：如 **UniAnimate-DiT** 和 **Wan-Animate**，利用大规模预训练视频扩散模型（如 Wan2.1）的生成先验，通过将参考图像特征和姿态条件注入去噪过程来生成动画。这些方法在空间对齐时表现优异，但面对错位输入时生成质量急剧下降——未见区域（occluded regions）出现模糊或伪影，已见区域的身份保真度也受影响。
- **图像姿态迁移方法**：如 **CFLD**（CVPR 2024）和 **MCLD**（CVPR 2025），专注于单帧姿态迁移，缺乏时序建模能力，无法直接用于视频动画。

从方法设计角度，现有工作的三个关键缺口可总结为：
1. **训练范式**：依赖对齐的自重建训练，无法让模型学会处理空间错位和遮挡。
2. **参考特征注入**：多采用 CLIP 编码器或简单地将参考图像首帧复制粘贴到视频骨干中，缺乏对多尺度外观特征的有效提取和融合。
3. **姿态控制机制**：直接将驱动姿态关键点注入去噪网络，未对身份-骨骼耦合进行显式解耦，导致姿态过拟合。

### 本文动机

针对上述瓶颈，本文提出 **One-to-All Animation**，一个统一的对齐自由（alignment-free）角色动画框架。核心动机是：**将训练重构为一项自我监督的 outpainting 任务**，迫使模型在训练阶段就学会从部分遮挡的参考图像中补全未知区域并保持身份一致性，从而在推理时天然具备处理空间错位的能力。

具体而言，本文的方法设计围绕三个关键洞察展开：
- **Outpainting 训练范式**：通过对参考图像面部区域进行随机遮挡，模拟实际场景中的空间错位和部分可见性，将多样化的参考布局统一为“遮挡输入”格式，使模型学会从局部信息重建完整外观。
- **身份鲁棒姿态控制**：通过面部区域增强（有意制造面部骨骼不一致）和参考引导姿态控制（将参考潜变量与驱动姿态联合建模），显式解耦身份特征与驱动骨骼，从根本上避免姿态过拟合。
- **统一的个性化生成框架**：同一模型支持跨尺度视频动画（可使用重定向或原始驱动姿态）、跨尺度图像姿态迁移，以及时序连贯的长视频生成（见 Figure 1），无需针对不同任务设计独立架构。

这一设计使得 One-to-All Animation 在空间错位场景下，相比现有 SOTA 方法展现出显著鲁棒性，为对齐自由的角色动画开辟了新路径。

## 核心创新

One-to-All Animation 的核心创新在于将角色动画问题从根本上重新定义为**无对齐的个性化生成任务**，通过三个紧密耦合的设计突破现有方法对空间对齐和骨骼匹配的刚性依赖。

### 瓶颈洞察：从对齐依赖到布局鲁棒

现有角色动画方法（如 **MimicMotion**（Zhang et al., arXiv 2024）、**StableAnimator**、**UniAnimate-DiT**）普遍采用自重建训练范式，假设参考图像与驱动视频帧之间天然对齐。这一假设在实际场景中频繁失效——当参考角色与驱动角色的空间布局、身体比例或面部骨骼存在差异时，生成质量急剧恶化，表现为身份丢失、纹理模糊或肢体畸变（参见 Figure 2 的对比可视化）。

本方法识别出这一根本瓶颈，并提出了系统性的因果干预方案：**通过自我监督的 outpainting 训练范式模拟空间错位，同时设计身份鲁棒姿态控制来解耦身份特征与驱动骨骼**，使模型能够在任意布局的参考图像下保持高质量生成。

### 关键创新点（Changed Slots）

相较于现有方法，One-to-All Animation 在以下四个维度实现了范式级改进：

**1. 训练范式：从自重建到自我监督 Outpainting**

传统方法将训练视为“同一视频的自重建”，隐含要求参考帧与驱动帧空间对齐。本方法引入 **Outpainting Preprocess**（Sec 3.1），在训练时对参考图像的面部区域施加随机遮挡，将其转化为统一的遮挡输入格式。这一设计迫使网络学习补全被遮挡区域，从而在推理时天然适应空间错位场景。同时，推理阶段通过姿态引导平移将参考图像与驱动视频对齐，无需任何显式配准步骤。

**2. 参考特征提取：从 CLIP 编码到专用参考提取器 + 混合融合注意力**

现有方法通常使用 CLIP 编码器或直接复制粘贴 I2V 骨干的首帧作为参考特征，难以在遮挡条件下保留细粒度身份信息。本方法设计了**专用 Reference Extractor**（Sec 3.2），从遮挡参考图像中提取多层次外观特征，包含多个与去噪骨干平行的 DiT 块（无文本交叉注意力）。进一步地，**混合参考融合注意力（HRFA）** 在 DiT 的自注意力层后添加交叉注意力，将参考特征注入视频潜变量，支持变分辨率和动态帧数。关键设计在于 HRFA 中查询的 RoPE 帧索引设为 $f=0$，避免学习绝对帧位置依赖，从而支持推理时生成任意长度的视频（消融实验证实，保留全 3D RoPE 会导致超出训练帧数后生成崩溃，见 Figure 13）。

**3. 姿态控制：从直接注入到身份鲁棒解耦**

传统方法直接将驱动姿态关键点注入去噪骨干，导致模型过拟合于特定身份-骨骼耦合关系，在面部骨骼不一致时产生身份漂移。本方法提出**身份鲁棒姿态控制**（Sec 3.3），包含两个互补机制：

- **面部区域增强**：训练时仅扰动驱动姿态的面部关键点，生成有意的骨骼不一致性，迫使模型解耦身份与姿态。消融实验显示，单独使用此策略会破坏训练稳定性（SSIM 从 0.773 降至 0.748），但配合下述机制后性能显著提升至 0.795（Table 3）。
- **参考引导姿态控制**：将参考图像潜变量及其未增强的姿态特征与驱动序列沿帧维度拼接（$\tilde{\mathbf{z}}^{1:(n+1)} = [\mathbf{z}^{r}, \mathbf{z}^{1:n}]_{\mathrm{frame}}$），经自注意力建模关系后加法注入。这一设计在稳定训练的同时显著提升身份一致性（全模型 CSIM 达 0.8172，去除后明显下降，见 Table 4）。

**4. 长视频生成：从逐段独立到可训练 Token Replace**

现有方法逐段独立生成长视频，缺乏时序过渡机制，导致片段边界出现跳变或闪烁。本方法提出**可训练的 Token Replace 策略**（Sec 3.4）：在去噪的每个时间步，用前一片段最后五帧编码的上下文令牌替换当前片段的前两个潜变量帧（$\tilde{\mathbf{z}}_{t}^{1:n} = [\mathbf{z}_{\mathrm{ctx}}, \mathbf{z}_{t}^{3:n}]$），以 $t=0$ 的干净信号进行调制。消融实验表明，该策略使 FVD 从 355.2 降至 297.9（Table 3），实现了片段间的无缝平滑过渡（Figure 10）。

### 创新协同效应

上述四个创新点并非孤立设计，而是形成了一条因果链路：**Outpainting 训练创造了对遮挡鲁棒的学习需求 → 专用参考提取器和 HRFA 满足了这一需求 → 身份鲁棒姿态控制防止了模型走“捷径”过拟合骨骼 → Token Replace 将鲁棒性扩展到长视频场景**。分阶段训练策略（先训练参考提取，再联合训练姿态控制，Table 6 证实 Ref → Ref+Pose 策略 SSIM 最优）进一步验证了这一协同设计的必要性。

## 整体框架

One-to-All Animation 将角色动画与图像姿态迁移统一为**对齐自由的个性化视频生成**问题。其核心设计哲学是：将训练重构为自我监督的 outpainting 任务，使模型学会从任意空间布局的参考图像中恢复被遮挡区域并保留身份信息，从而在推理时无需参考-驱动帧之间的空间对齐或骨骼匹配。

### 输入输出规范

框架接收三类输入：
- **参考图像**：任意分辨率、任意空间布局的角色图像，不要求与驱动视频中的人体比例或位置一致；
- **驱动姿态序列**：从驱动视频中提取的 2D 姿态关键点序列，可选择是否进行姿态重定向（retargeting）；
- **文本提示**（可选）：用于辅助生成的文本描述。

输出为一段与驱动姿态序列帧数相同的视频，其中角色的外观来自参考图像，动作来自驱动姿态。

### 核心模块与数据流

整个 pipeline 由五个关键模块串联构成，数据流如图 3 所示：

1. **Outpainting Preprocess（外扩预处理）**  
   训练时，以面部为中心对参考图像施加随机遮挡掩码，模拟实际场景中参考与驱动帧之间的空间错位。被遮挡的参考图像与掩码一同输入后续模块。推理时，通过姿态引导的平移变换将参考图像与驱动视频的关键点对齐，无需重训练。

2. **Reference Extractor（参考特征提取器）**  
   从被遮挡的参考图像中提取多层次外观特征。该模块由 M 个与去噪骨干平行的 DiT 块组成，不含文本交叉注意力，初始化自预训练 I2V 模型权重。输入为参考图像潜变量与掩码潜变量的通道拼接：  
   $$r^{0} = \mathrm{patchify}\left( [z^{r}, z^{m}]_{\mathrm{channel}} \right)$$

3. **Hybrid Reference Fusion Attention（混合参考融合注意力，HRFA）**  
   在去噪骨干的每个 DiT 块中，于自注意力层后插入交叉注意力层，将参考特征注入视频潜变量。关键设计在于：对交叉注意力中的查询和键施加 $f=0$ 的 3D RoPE，避免模型学习绝对帧位置依赖，从而支持变分辨率和动态帧数。融合输出为自注意力与交叉注意力之和。

4. **Identity-Robust Pose Control（身份鲁棒姿态控制）**  
   由两个协同子模块构成：
   - **面部区域增强**：训练时仅扰动驱动姿态的面部关键点，生成有意的面部骨骼不一致性，破坏身份特征与骨骼结构的虚假耦合，迫使网络从参考特征中独立提取身份信息；
   - **参考引导姿态控制**：将参考图像潜变量 $\mathbf{z}^{r}$ 与驱动序列沿帧维度拼接为 $\tilde{\mathbf{z}}^{1:(n+1)} = [\mathbf{z}^{r}, \mathbf{z}^{1:n}]_{\mathrm{frame}}$，经自注意力建模参考-驱动关系后，以加法方式注入去噪骨干，稳定训练并提升身份一致性。

5. **Token Replace（令牌替换）**  
   用于长视频生成。将前一片段的最后五帧编码为上下文令牌 $\mathbf{z}_{\mathrm{ctx}}$，在当前片段的每个去噪时间步 $t$，替换前两个潜变量帧：  
   $$\tilde{\mathbf{z}}_{t}^{1:n} = [\mathbf{z}_{\mathrm{ctx}}, \mathbf{z}_{t}^{3:n}]$$  
   上下文令牌以 $t=0$ 调制为干净信号，实现片段间无缝过渡。

### 训练策略

训练遵循 Rectified Flow 框架，损失函数为预测速度场与真实速度场的均方误差：  
$$\mathcal{L}_{\mathrm{RF}} = \|v_{t} - u_{t}\|^{2}, \quad u_{t} = \varepsilon - \mathbf{x}_{0}$$

采用分阶段训练策略：先训练 Reference Extractor（Ref 阶段），再联合训练姿态控制模块（Ref+Pose 阶段）。消融实验证实，此顺序在 SSIM 指标上（0.773）优于先姿态后参考或联合训练策略（Table 6）。

### 关键设计决策与证据

| 设计选择 | 因果机制 | 证据强度 |
|---------|---------|---------|
| Outpainting 而非 crop-and-resize | 避免裁剪引入的严重伪影（Figure 14），使模型学会真实遮挡补全 | 强（消融对比） |
| HRFA 中 $f=0$ 的 RoPE | 防止交叉注意力学习绝对帧位置，确保变帧数推理不崩溃（Figure 13） | 强（失败案例分析） |
| 面部增强 + 参考引导姿态控制联合使用 | 单独使用面部增强会破坏训练稳定性（SSIM 从 0.773 降至 0.748），两者协同使 SSIM 提升至 0.795（Table 3） | 强（定量消融） |
| Token Replace 而非静态上下文 | 无过渡机制时 FVD 为 355.2，Token Replace 降至 297.9（Table 3） | 强（定量消融） |

### 补充图表

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed framework. We introduce outpainting preprocess to handle diverse body proportions through facecentered random masking during training and pose-guided translation at inference. The driving poses are encoded and refined via referenceguided pose control to preserve facial identity despite skeletal mismatch. Reference features are progressively injected through hybrid reference fusion attention, supporting variable resolutions and dynamic sequence lengths*

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/001_Figure_1.jpg]]
*Figure 1: We introduce One-to-All Animation, a unified framework for pose-driven personalized generation. Unlike prior methods that require both spatially-aligned references and pose retargeting, our framework supports: (1) cross-scale video animation with either retargeted or original driving motion, (2) cross-scale image pose transfer, and (3) temporally coherent long video generation*

## 核心模块与公式推导

### 3.1 Outpainting 预处理：从空间对齐到统一遮挡输入

现有角色动画方法普遍采用自重建训练范式，假设参考帧与驱动帧在空间上天然对齐。本文的核心改造在于将训练重构为**自我监督的 Outpainting 任务**：训练时对参考图像的面部区域施加随机遮挡，强制网络学习补全被遮挡区域并保留身份信息，从而在推理时天然具备处理空间错位的能力。

具体而言，给定参考图像和对应的掩码，首先通过 VAE 编码器获得潜变量 $\mathbf{z}^r$ 和 $\mathbf{z}^m$，随后沿通道维度拼接并进行 patchify 操作，得到初始参考特征 tokens：

$$r^{0} = \mathrm{patchify}\left( [z^{r}, z^{m}]_{\mathrm{channel}} \right) \tag{1}$$

这一设计的因果机制在于：遮挡迫使网络无法依赖简单的空间复制，而必须从可见区域推断被遮挡部分的身份特征，从而在推理时面对任意空间布局的参考图像时仍能保持鲁棒的身份一致性。推理阶段则通过姿态引导的平移操作将参考图像与驱动视频对齐，无需任何显式的空间配准步骤。

### 3.2 参考提取器与混合参考融合注意力

为从遮挡参考图像中提取多层次外观特征，本文设计了一个专用的 **Reference Extractor**。该提取器由 $M$ 个与去噪骨干平行的 DiT 块组成，移除了文本交叉注意力层，仅保留自注意力机制以专注于身份特征的提取。每个 DiT 块中的自注意力采用 3D 旋转位置编码（3D RoPE）：

$$\mathrm{Attention}(\mathrm{Q}, \mathrm{K}, \mathrm{V}) = \mathrm{softmax}\left( \frac{\mathrm{Q}(\mathrm{K})^{\top}}{\sqrt{d}} \right) \mathrm{V}, \quad \mathrm{Q} = \mathrm{RoPE}_{3D}(h W_{q}), \quad \mathrm{K} = \mathrm{RoPE}_{3D}(h W_{k}), \quad \mathrm{V} = h W_{v} \tag{2-3}$$

其中 $h$ 为隐藏状态，$d$ 为特征维度，$W_q, W_k, W_v$ 为可学习投影矩阵。3D RoPE 沿帧、高度、宽度三个维度编码时空位置信息，使参考特征能够感知自身的空间结构。

**混合参考融合注意力（HRFA）** 是连接参考特征与视频生成的关键桥梁。在去噪骨干的每个 DiT 块中，自注意力层之后插入一个交叉注意力层，将参考特征注入视频潜变量：

$$\mathrm{Attention}(\mathrm{Q}', \mathrm{K}', \mathrm{V}') = \mathrm{softmax}\left( \frac{\mathrm{Q}'(\mathrm{K}')^{\top}}{\sqrt{d}} \right) \mathrm{V}', \quad \mathrm{Q}' = \mathrm{RoPE}_{3D, f=0}(h W_{q}), \quad \mathrm{K}' = \mathrm{RoPE}_{3D, f=0}(r W_{k}'), \quad \mathrm{V}' = r W_{v}' \tag{4-5}$$

该模块的**关键设计决策**在于将查询 $\mathrm{Q}'$ 的 RoPE 频率参数 $f$ 设为零。消融实验（Figure 13）表明，保留完整 3D RoPE 会导致模型学习到绝对帧位置依赖，当推理帧数超过训练帧数时生成崩溃。$f=0$ 的设计使交叉注意力仅依赖相对空间关系，从而支持变分辨率和动态帧数的推理。

自注意力与交叉注意力的输出通过加法融合：

$$\mathbf{z}_{\mathrm{fusion}}' = \mathrm{Attention}(\mathrm{Q}, \mathrm{K}, \mathrm{V}) + \mathrm{Attention}(\mathrm{Q}', \mathrm{K}', \mathrm{V}') \tag{6}$$

消融实验（Figure 8）证实，Reference Extractor 在遮挡区域重建和身份细节保留上明显优于 IP-Adapter 和直接使用 I2V 骨干作为参考提取器的方案。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative comparison of different reference feature extraction methods in the first training stage*

### 3.3 身份鲁棒姿态控制

角色动画中的核心挑战是**面部姿态过拟合**：当驱动骨骼与参考图像的身份特征耦合时，模型倾向于生成与驱动姿态匹配但与参考身份不一致的面部外观。本文通过两个互补机制解耦身份与骨骼：

**面部区域增强（Face Region Enhancement）**：训练时随机采样一个辅助姿态，将其缩放到与驱动姿态匹配的尺度，然后仅对面部关键点施加两者的骨骼差异，生成有意的不一致性。这一操作迫使网络学习从参考图像中提取身份信息，而非简单复制驱动姿态的面部结构。消融实验（Table 3）显示，仅添加面部增强会破坏训练稳定性（SSIM 从 0.773 降至 0.748），说明单独使用该策略反而引入噪声。

**参考引导姿态控制（Reference-guided Pose Control）**：将参考图像潜变量 $\mathbf{z}^r$ 与视频潜变量沿帧维度拼接：

$$\tilde{\mathbf{z}}^{1:(n+1)} = [\mathbf{z}^{r}, \mathbf{z}^{1:n}]_{\mathrm{frame}} \tag{7}$$

拼接后的序列经过去噪骨干的自注意力层，使参考图像的身份信息与驱动姿态在注意力机制中显式交互。随后将参考引导的姿态特征通过加法注入视频潜变量，稳定训练过程并提升身份一致性。全模型配置下 CSIM 达 0.8172（Table 4），去除面部增强或参考引导后指标明显下降，验证了两者缺一不可。

### 3.4 Token Replace：可训练的长视频过渡

生成长视频时，逐段独立生成会导致片段边界的不连贯。本文提出**可训练的 Token Replace 策略**：将前一片段的最后五帧编码为上下文令牌 $\mathbf{z}_{\mathrm{ctx}}$，在去噪的每个时间步 $t$，用这些上下文令牌替换当前片段的前两个潜变量帧：

$$\tilde{\mathbf{z}}_{t}^{1:n} = [\mathbf{z}_{\mathrm{ctx}}, \mathbf{z}_{t}^{3:n}] \tag{9}$$

上下文令牌在 $t=0$ 时刻被调制为干净信号，确保其作为无噪参考参与去噪过程。消融实验（Table 3）表明，开启 Token Replace 后 FVD 从 355.2 降至 297.9，显著优于无过渡机制或静态上下文替换的变体。

### 3.5 训练目标：Rectified Flow

模型遵循 Rectified Flow 框架进行训练。前向过程定义为干净潜变量 $\mathbf{x}_0$ 与高斯噪声 $\boldsymbol{\varepsilon}$ 的线性插值：

$$\mathbf{x}_t = (1 - t)\mathbf{x}_0 + t\boldsymbol{\varepsilon} \tag{10}$$

训练目标为最小化预测速度场 $v_t$ 与真实速度场 $u_t = \boldsymbol{\varepsilon} - \mathbf{x}_0$ 之间的均方误差：

$$\mathcal{L}_{\mathrm{RF}} = \|v_{t} - u_{t}\|^{2} \tag{11-12}$$

训练采用两阶段策略：第一阶段仅训练参考特征注入（Ref → Ref+Pose），第二阶段加入姿态控制。消融实验（Table 6）证实该分阶段策略（SSIM 0.773）优于先姿态后参考或联合训练方案。

### 补充图表

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/014_Figure_9.jpg]]
*Figure 9: Qualitative ablation of Identity-Robust Pose Control*

## 实验与分析

### 主实验结果

#### 视频角色动画（TikTok 与 Cartoon）

Table 1 给出了 TikTok 和 Cartoon 两个基准上的定量对比。在 1.3B 参数规模下，**One-to-All-1.3B** 在多数指标上已超越同量级的 **MimicMotion**（Zhang et al., arXiv 2024）、**StableAnimator** 和 **Animate-X** 等方法。当模型规模扩展到 14B 时，**One-to-All-14B** 在两个数据集上均取得最优结果：在 TikTok 上 FID-VID 降至 13.93（对比 **UniAnimate-DiT** 的 17.42），FVD 降至 297.94（对比 358.42）；在 Cartoon 上 FVD 降至 403.47（对比 **Wan-Animate** 的 485.92）。这表明本方法在跨尺度视频动画任务中具有一致的性能优势。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons on TikTok and Cartoon datasets. In the table, a / b denotes results on TikTok / Cartoon*

Figure 6 的定性对比进一步佐证了上述结论：在 TikTok 和 Cartoon 测试样本上，本方法生成的动画在身份一致性和运动保真度方面均优于现有 SOTA 方法。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparisons with state-of-the-art methods*

#### 图像姿态迁移（DeepFashion）

Table 2 报告了 DeepFashion 数据集上的图像姿态迁移结果。在 512×352 分辨率下，**One-to-All-1.3B** 的 FID 为 6.85、LPIPS 为 0.249，均优于 **MCLD**（CVPR 2025）等专门设计的姿态迁移方法。在高分辨率（944×624）场景下，本方法的 FID 为 6.92，同样领先于 **CFLD**（CVPR 2024）的 8.38。这一结果表明，尽管本方法并非专为图像姿态迁移设计，其统一的 outpainting 训练范式仍能有效泛化到该任务。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison on DeepFashion dataset*

#### 用户偏好研究

Figure 7 展示了与当前 SOTA 方法 **Wan-Animate** 的用户偏好对比。在空间错位场景下，本方法在**未见区域质量**上的偏好率为 47.6%（对比 28.1%），在**已见区域保真度**上的偏好率为 72.4%（对比 16.1%）。这直接验证了 outpainting 训练范式在应对空间错位输入时的关键作用。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/009_Figure_7.jpg]]
*Figure 7: Human evaluation with current SOTA*

### 消融实验

#### 参考特征提取器设计

Figure 8 对比了不同参考特征提取方案的定性效果。专用的 **Reference Extractor** 在遮挡区域重建和身份细节保留上明显优于 **IP-Adapter** 和直接使用 I2V Backbone 的方案。Table 3 的定量消融显示，移除 Reference Extractor 后 SSIM 从 0.773 降至 0.748，FVD 从 297.9 升至 355.2，证实了该组件对生成质量的核心贡献。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/011_Table_3.jpg]]
*Table 3: Ablation study on model components. Experiments are conducted on the TikTok benchmark using 14B model*

#### 身份鲁棒姿态控制

Table 4 针对 100 对错位图像-视频对的消融表明，完整的身份鲁棒姿态控制方案（面部区域增强 + 参考引导姿态控制）使 CSIM 达到 0.8172。单独移除面部增强或参考引导后，CSIM 分别降至 0.7934 和 0.8016，APD-body 也出现劣化。Figure 9 的定性对比进一步显示，去除这些组件会导致面部身份信息丢失或姿态跟随不准确。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/012_Table_4.jpg]]
*Table 4: Ablation on identity-robust pose control using 100 misaligned image-video pairs*

Table 3 还揭示了一个关键交互效应：仅添加面部区域增强会破坏训练稳定性（SSIM 从 0.773 降至 0.748），但配合参考引导姿态控制后性能提升至 0.795。这说明两个组件必须协同工作——面部增强破坏身份-骨骼耦合，参考引导则稳定训练并提供身份锚定。

#### Token Replace 长视频策略

Table 3 中，完整的 Token Replace 策略在 TikTok 上取得 FVD 297.9，显著优于无长视频过渡机制的变体（FVD 355.2）。Figure 10 的定性对比展示了三种策略的差异：无过渡方案产生明显的片段边界跳变，静态上下文方案引入身份漂移，而 Token Replace 实现了平滑的片段间过渡。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/013_Figure_10.jpg]]
*Figure 10: Comparison of long video generation strategies. substantial improvements*

#### 训练阶段设计

Table 6 对比了不同的训练阶段策略。**Ref → Ref+Pose** 的分阶段训练方案（先训练参考特征提取，再加入姿态控制）取得最优 SSIM 0.773，优于先姿态后参考（SSIM 0.748）或联合训练（SSIM 0.758）。这表明渐进式引入训练信号有助于模型稳定收敛。

![[assets/figures/papers/paper_list_l1075_https_arxiv_org_abs_2511_22940/figures/021_Table_6.jpg]]
*Table 6: Ablation on training stage design. All methods evaluated on TikTok benchmark using 14B model*

#### HRFA 中 RoPE 设计

Figure 13 展示了一个关键失败模式：在 HRFA 的交叉注意力中保留全 3D RoPE（即 f≠0）会导致模型学习绝对帧位置依赖，当推理帧数超过训练帧数时生成崩溃。将查询的 RoPE 设为 f=0 是避免该问题的必要条件。

### 失败模式与局限性

1. **Crop-and-Resize 基线引入严重伪影**：Figure 14 显示，若用传统的裁剪-缩放替代 outpainting 预处理，生成结果会出现明显的空间扭曲和伪影，进一步验证了 outpainting 训练范式的必要性。

2. **计算开销极大**：Table 5 显示 14B 模型单次推理需 65 GB 显存且耗时超过 7 分钟，严重限制了其在消费级硬件上的可用性。

3. **数据混合比例未充分探索**：不同任务（视频动画 vs. 图像姿态迁移）需使用不同数据比例训练的 checkpoint，尚未找到统一的泛化最优配比。

4. **摄像机运动控制缺失**：本方法仅依赖 2D 姿态序列作为运动信号，无法独立控制摄像机轨迹，相机运动只能通过角色位置隐式表达。

## 方法谱系与知识库定位

### 问题域与基线方法

角色动画（Character Animation）和图像姿态迁移（Image Pose Transfer）共享一个核心目标：将参考图像中的身份外观迁移到驱动视频或目标姿态上，生成视觉连贯的个性化视频或图像。现有方法可大致分为两类：

**基于对齐的角色动画方法** 假设参考图像与驱动视频帧之间在空间布局和骨骼结构上天然对齐，训练时采用自重建范式（self-reconstruction），即从视频中采样首帧作为参考、其余帧作为驱动目标。代表性工作包括 **MimicMotion**（Zhang et al., arXiv 2024）和 **StableAnimator**。这类方法在实际部署中面临根本性瓶颈：当参考图像与驱动视频存在空间错位（如人物位置偏移、尺度不一致）或面部骨骼不匹配时，生成质量剧烈下降——身份特征丢失、肢体扭曲、出现严重伪影（见 Figure 2）。

**基于扩散模型的视频生成方法** 将角色动画视为条件视频生成任务，通过注入姿态信号控制运动。**UniAnimate-DiT** 和 **Wan-Animate**（基于 Wan2.1 骨干）代表了该方向的最新进展，但仍未从根本上解决对齐依赖问题——它们隐含假设参考帧与驱动帧的空间对应关系，在非对齐场景下表现退化。

**图像姿态迁移方法** 专注于单帧到单帧的生成，代表性工作包括 **CFLD**（CVPR 2024）和 **MCLD**（CVPR 2025）。这些方法在固定分辨率下表现优异，但缺乏对视频时序一致性和跨尺度生成的统一支持。

### 本文方法在谱系中的位置

**One-to-All Animation** 在上述谱系中占据一个独特位置：它通过**训练范式的根本性重构**，将角色动画从“对齐依赖”转向“对齐自由”，同时统一了视频动画、图像姿态迁移和长视频生成三项任务。

核心区分点在于三个设计决策：

1. **训练范式从自重建转向自监督 Outpainting**（Sec 3.1）：通过在训练时对面部区域进行随机遮挡（face-centered random masking），迫使网络学习从部分可见的参考图像中补全身份信息。这一设计将多样化的参考布局统一为“遮挡输入”格式，使得模型天然具备处理空间错位的能力。消融实验（Figure 14）表明，若采用传统的 crop-and-resize 基线替代 outpainting，会引入严重伪影。

2. **身份鲁棒姿态控制**（Sec 3.3）：现有方法直接将姿态关键点注入去噪骨干，导致模型在训练中学会将特定身份与特定骨骼结构耦合——即“面部姿态过拟合”。本文通过两个互补机制解耦身份与骨骼：（a）**面部区域增强**：训练时仅扰动驱动姿态的面部关键点，生成有意的骨骼不一致性；（b）**参考引导姿态控制**：将参考图像潜变量及其未增强的姿态特征与驱动序列拼接，经自注意力建模关系后加法注入。消融实验（Table 3-4）证实，单独使用面部增强会破坏训练稳定性（SSIM 从 0.773 降至 0.748），但配合参考引导后 SSIM 提升至 0.795，CSIM 达 0.8172——两者缺一不可。

3. **专用参考提取器与混合融合注意力（HRFA）**（Sec 3.2）：区别于基线方法使用 CLIP 编码器或 I2V 骨干的首帧复制粘贴，本文设计了与去噪骨干平行的多级 DiT 块作为参考提取器，通过 HRFA 中的交叉注意力将多级外观特征注入视频潜变量。关键设计细节是交叉注意力查询的 RoPE 中设置帧维度 $f=0$，避免学习绝对帧位置依赖——若保留全 3D RoPE，在超过训练帧数后生成会崩溃（Figure 13）。

### 适用边界

**已验证的适用场景**：
- 跨尺度视频角色动画（TikTok 和 Cartoon 数据集，1.3B/14B 参数规模）
- 图像姿态迁移（DeepFashion 数据集，512×352 和 944×624 分辨率）
- 长视频生成（通过 Token Replace 策略实现片段间平滑过渡，FVD 从 355.2 降至 297.9）

**已知局限**：
1. **数据混合比例未充分探索**：图像与视频训练数据的最佳混合比例尚不明确，不同任务需使用不同比例的 checkpoint（原文明确提及此限制）。
2. **14B 模型推理成本极高**：生成高分辨率或长视频时需 65 GB 显存，单次推理超过 7 分钟，限制了在消费级 GPU 上的部署可行性。
3. **相机运动控制缺失**：仅依赖 2D 姿态序列作为运动信号，相机运动仅能通过角色位置隐式表示，无法独立控制摄像机轨迹。

### 开放问题

1. **数据配比优化**：如何确定图像和视频数据的最佳训练比例，以在姿态迁移和视频动画之间取得最优泛化？
2. **推理效率提升**：是否可以通过模型量化、蒸馏或高效注意力机制大幅降低 14B 模型的推理成本？
3. **相机运动解耦**：如何引入显式的摄像机参数（如内参/外参）来实现角色运动与摄像机运动的独立控制？
4. **跨域泛化**：在完全未见的角色类型（如非人类角色）或极端遮挡下，本方法的泛化能力如何？这需要额外实验验证。

### 知识库贡献总结

本方法对角色动画领域的核心贡献在于**证明了通过训练范式重构（自监督 outpainting + 身份鲁棒姿态控制）可以消除对齐依赖**，而非仅仅在现有框架上做增量改进。这一洞察具有方法论的迁移价值：对于其他需要从“参考-目标”对中学习外观迁移的任务（如虚拟试衣、面部重演），类似的遮挡预训练和身份-结构解耦策略可能同样有效。

## 原文 PDF

![[paperPDFs/CVPR_2026/One_to_All_Animation_Alignment_Free_Character_Animation_and_Image_Pose_Transfer.pdf]]