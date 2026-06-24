---
title: "Geometry Forcing: Marrying Video Diffusion and 3D Representation for Consistent World Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Geometry_Forcing_Marrying_Video_Diffusion_and_3D_Representation_for_Consistent_World_Modeling.pdf
openreview_forum_id: ULXYZCms41
aliases:
- GFG
- GFMVD3RCWM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将视频扩散模型中间特征与预训练三维基础模型（如VGGT）的几何感知特征对齐，迫使模型内部化三维表示。"
primary_logic: "通过解耦的角度对齐（保持方向一致性）和尺度对齐（保持幅度信息）目标，可以从方向与幅度两个维度稳定地引导模型学习几何结构，从而显著提升时空一致性。"
claims:
- "线性探测：预训练视频扩散特征无法重建有意义的深度图，表明纯像素训练忽略了三维结构。"
- "主要结果：GF在RealEstate10K基准上FVD从364降至243，LPIPS、SSIM、PSNR全面提升。"
- "目标表示消融：对齐几何表示（VGGT）FVD-256为243，远优于语义表示（DINOv2）的297；两者结合进一步达到237。"
- "对齐损失消融：角度+尺度组合FVD-256为243，优于仅角度对齐（253）或直接MSE（1648）。"
---

# Geometry Forcing: Marrying Video Diffusion and 3D Representation for Consistent World Modeling

> [!tip] 核心洞察
> 通过解耦的角度对齐（保持方向一致性）和尺度对齐（保持幅度信息）目标，可以从方向与幅度两个维度稳定地引导模型学习几何结构，从而显著提升时空一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 几何强制：融合视频扩散与三维表示以实现一致的世界建模 |
| 英文题名 | Geometry Forcing: Marrying Video Diffusion and 3D Representation for Consistent World Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ULXYZCms41) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Geometry Forcing (GF) |
| Dataset | RealEstate10K (16帧), RealEstate10K (256帧) |

> [!tip] 效果简介
> - RealEstate10K (16帧) 上，FVD↓ 为 193 (Geometry Forcing)，对比 252 (DFoT)，变化 -59。
> - RealEstate10K (256帧) 上，FVD↓ 为 243 (Geometry Forcing)，对比 364 (DFoT)，变化 -121。
> - RealEstate10K (256帧) 上，LPIPS↓ 为 0.51 (Geometry Forcing)，对比 0.55 (DFoT)，变化 -0.04。

## 概述

视频扩散模型在生成逼真视频方面取得了显著进展，但其训练仅依赖于像素级重建目标，导致模型无法捕获底层的三维几何结构。这一根本缺陷使得生成的视频缺乏时空一致性——尤其是在长序列生成和复杂相机运动下，表现为场景漂移、物体形变和视角不一致等问题。线性探测实验证实了这一点：从预训练视频扩散模型中间特征重建的深度图无法形成有意义的几何表示（Figure 1(c)）。

针对上述瓶颈，本文提出**Geometry Forcing (GF)**，一种简洁而有效的训练范式。其核心思路是：在视频扩散模型的训练过程中，将其内部中间特征与预训练三维基础模型（VGGT）的几何感知特征进行对齐，从而迫使模型内部化三维表示，而非依赖外部的显式几何注入。为实现稳定对齐，GF 引入两个互补目标——**角度对齐**（Angular Alignment）保持方向一致性，**尺度对齐**（Scale Alignment）保留幅度信息——从方向与幅度两个维度解耦地引导模型学习几何结构。

在 RealEstate10K 基准上，GF 将 256 帧长视频生成的 FVD 从 364 降至 243，同时 LPIPS、SSIM、PSNR 等像素级指标全面提升。消融实验表明：对齐几何表示（VGGT）显著优于语义表示（DINOv2），且角度+尺度组合优于任一单独目标；内部隐式对齐的效果远超外部显式注入几何信息。用户研究进一步证实，GF 在相机跟随、物体一致性和场景连续性三个维度上均获得显著更高的主观评分。此外，GF 有效缓解了长序列生成中的暴露偏差问题，100 帧后 FVD 累积误差明显低于基线。

GF 的适用范围不限于特定架构或数据域：它可与不同的三维基础模型（如 Pi3）兼容，在 Minecraft 动作条件生成和 Wan2.1 文本条件生成任务上同样带来一致提升。该方法在推理时不引入额外计算开销，仅在训练阶段增加 VGGT 特征提取成本，但换来了更快的收敛和更强的几何一致性。

## 背景与动机

### 视频生成模型的几何盲区

视频扩散模型近年来在生成逼真视频方面取得了显著进展，但其训练范式存在一个根本性缺陷：模型仅从原始像素数据中学习，缺乏对三维几何结构的感知能力。Figure 1(c)的线性探测实验直接揭示了这一问题——从预训练视频扩散模型的中间特征出发，几乎无法重建出有意义的深度图。这意味着，尽管模型能够生成视觉上连贯的帧序列，其内部表征并未编码场景的三维空间关系。

这一缺陷在需要几何一致性的场景中尤为突出。当生成涉及相机运动（尤其是大角度旋转）的长序列视频时，纯像素训练的视频扩散模型会逐渐累积误差，导致物体形变、场景漂移和视角不一致等问题。如Figure 2所示，在完整360°旋转的相机条件下，基线方法**DFoT**（Song et al., 2025）无法保持时间一致性，无法在旋转一周后回到起始视角。这种暴露偏差（exposure bias）会随序列增长而急剧恶化：Figure 4显示，基线模型在100帧后FVD显著上升，而本文方法则有效抑制了这一趋势。

### 现有方法的局限

当前试图为视频生成注入几何信息的方法主要分为两类：

- **显式几何注入**：通过ControlNet等机制将深度图、点云或渲染图像作为额外条件输入模型。然而，Table 4和Table 8的消融实验表明，这类显式注入方法（如渲染图像注入、潜在特征注入）在256帧长序列生成上的FVD分别为280和275，远不及内部对齐方案（243）。显式注入迫使模型学习从几何信号到像素的映射，而非真正内化三维结构。

- **语义特征对齐**：如**REPA**（Yu et al., 2024a）和**VideoREPA**（Zhang et al., 2025c）等方法，通过将扩散特征与DINOv2等语义表示对齐来提升生成质量。Table 2的消融显示，仅对齐语义表示（DINOv2）能将FVD-256从364降至297，但效果远逊于对齐几何表示（VGGT）的243。这说明语义信息无法替代几何结构感知。

### 核心动机

上述分析指向一个清晰的研究动机：**视频扩散模型需要一种机制，使其在训练过程中主动内化三维几何感知能力，而非依赖外部显式注入或仅从像素重建中隐式学习。**

本文的核心洞察在于：预训练的几何基础模型（如VGGT）已经编码了丰富的三维结构信息。如果能在训练过程中，将视频扩散模型的中间特征与这些几何感知特征对齐，就能迫使模型学习到有意义的几何表征。关键在于对齐方式的设计——简单的MSE对齐会导致FVD恶化至1648（Table 3），因为直接匹配特征幅值会破坏扩散模型自身的表征学习。这引出了本文提出的解耦对齐策略：从方向（角度对齐）和幅度（尺度对齐）两个维度分别施加约束，从而稳定地引导模型内化三维结构。

## 核心创新

Geometry Forcing 的核心创新在于识别并解决了一个关键瓶颈：**视频扩散模型仅从原始像素数据训练时，无法自发学习有意义的几何感知结构**。线性探测实验（Figure 1(c)）直接验证了这一缺陷——冻结的预训练视频扩散模型中间特征无法重建出可用的深度图，表明模型尽管能生成看似连贯的像素序列，其内部表示却缺乏对三维世界的理解。

针对这一瓶颈，GF 的因果操作是**将视频扩散模型的中间层特征与预训练三维基础模型（VGGT）的几何感知特征对齐**，迫使模型在训练过程中内部化三维表示。这一设计改变了三个关键训练槽位：

**训练目标**。基线 DFoT 仅使用流匹配损失 $\mathcal{L}_{\mathrm{FM}}$ 从像素层面优化。GF 额外引入两个解耦的对齐目标：角度对齐损失 $\mathcal{L}_{\mathrm{Angular}}$（最大化扩散特征投影与 VGGT 目标特征的方向一致性，即余弦相似度）和尺度对齐损失 $\mathcal{L}_{\mathrm{Scale}}$（通过归一化扩散特征预测目标特征的幅值，保留尺度信息）。最终训练目标为三者的加权和：
$$\mathcal{L} = \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{Angular}} \cdot \mathcal{L}_{\mathrm{Angular}} + \lambda_{\mathrm{Scale}} \cdot \mathcal{L}_{\mathrm{Scale}}$$
其中 $\lambda_{\mathrm{Angular}}=0.5$，$\lambda_{\mathrm{Scale}}=0.05$。消融实验（Table 3）证明这种解耦设计至关重要：角度+尺度组合将 FVD-256 降至 243，优于仅角度对齐的 253，而直接使用 MSE 同时对齐角度和尺度信息则导致 FVD 飙升至 1648，说明解耦是稳定引导几何学习的必要条件。

**特征空间正则化**。基线模型仅在像素重建损失下学习，其特征空间缺乏结构化约束。GF 通过 Conv3D 投影器 $f_\phi$ 将扩散中间特征映射到与 VGGT 特征兼容的维度，并在该投影空间上施加角度和尺度约束。这一设计使得模型内部特征被正则化为几何可解释的表示，线性探测验证了 GF 训练后的特征可以重建出有意义的深度图。

**几何信息注入方式**。与外部显式注入几何信息（如 ControlNet 注入 VGGT 特征或渲染图像条件）不同，GF 采用内部隐式对齐策略。Table 4 和 Table 8 的对比表明：显式注入 VGGT 特征最高仅将 FVD-256 降至 275，而 GF 的内部对齐达到 243，且在全指标（LPIPS、SSIM、PSNR、RPE、RVE）上均优于显式方法。这说明迫使模型自身学习几何感知表示比直接提供几何信号更有效——模型获得了从像素中推断三维结构的泛化能力，而非简单记忆外部输入。

目标表示的选择同样关键。Table 2 表明对齐几何表示（VGGT）将 FVD-256 降至 243，显著优于对齐语义表示（DINOv2）的 297，两者结合进一步优化至 237。这确认了三维几何信息（而非通用语义）是提升视频生成时空一致性的关键信号源。GF 的方法本身与具体教师模型解耦，Table 7 显示使用 Pi3 作为教师模型同样能将 FVD-256 降至 309，验证了框架的通用性。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/004_Figure_1.jpg]]
*Figure 1: Geometry Forcing equips video diffusion models with 3D awareness. (a) We propose Geometry Forcing (GF), a simple yet effective paradigm to internalize geometric-aware structure into video diffusion models by aligning with features from a geometric foundation model, i.e., VGGT (Wang et al., 2025b). (b) Compared to the baseline method (Song et al., 2025), our method produces more consistent generations both temporally and geometrically. (c) Features learned by the baseline model fail to reconstruct meaningful 3D geometry, whereas our method internalizes 3D representation, enabling accurate 3D reconstruction from the intermediate features*

Geometry Forcing (GF) 的整体框架围绕一个核心操作展开：**在视频扩散模型的训练过程中，将其中间层特征与预训练三维基础模型（VGGT）的几何感知特征进行对齐**。这一对齐并非发生在像素空间或条件输入端，而是直接作用于扩散模型 U-ViT backbone 的隐藏状态，迫使模型内部化三维结构表示。

### Pipeline 模块与数据流

GF 的训练管线由以下模块构成，数据流呈“扩散主干—投影对齐—损失回传”的闭环：

1. **U-ViT Diffusion Backbone**：视频生成的核心网络，采用 7 层下采样-瓶颈-上采样结构。输入为经流匹配（Flow Matching）前向过程加噪的视频帧序列 $\mathbf{x}^{\mathbf{t}}$，输出为预测的速度场 $v_{\theta}(\mathbf{x}^{\mathbf{t}}, \mathbf{t})$。该主干同时产生多层中间隐藏状态 $h$，作为几何对齐的源特征。

2. **VGGT Teacher**：一个冻结的预训练三维基础模型，以视频帧作为输入，从其 Transformer backbone 中提取几何感知的目标特征 $y$。这些特征编码了场景的三维结构信息，作为对齐过程的监督信号。

3. **Conv3D Projector $f_{\phi}$**：一个轻量级的 3D 卷积投影器，将扩散模型某一层的隐藏状态 $h$ 映射到与 VGGT 特征兼容的维度空间，得到投影特征 $f_{\phi}(h)$。

4. **Scale Prediction Head $g_{\varphi}$**：一个小型预测网络，以归一化后的投影特征为输入，预测目标特征 $y$ 的尺度（幅值）信息，输出重构的完整特征 $\tilde{y}$。

5. **Angular Alignment Loss $\mathcal{L}_{\text{Angular}}$**：计算投影特征 $f_{\phi}(h)$ 与目标特征 $y$ 之间的余弦相似度，强制两者在方向上的对齐。该损失仅关注特征向量的方向一致性，不约束幅值。

6. **Scale Alignment Loss $\mathcal{L}_{\text{Scale}}$**：计算 Scale Prediction Head 输出的重构特征 $\tilde{y}$ 与目标特征 $y$ 之间的均方误差，保留几何特征的尺度信息，避免仅对齐方向导致的信息丢失。

### 训练目标

整体训练目标为流匹配损失与两个对齐损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\text{FM}} + \lambda_{\text{Angular}} \cdot \mathcal{L}_{\text{Angular}} + \lambda_{\text{Scale}} \cdot \mathcal{L}_{\text{Scale}}$$

其中 $\lambda_{\text{Angular}}=0.5$，$\lambda_{\text{Scale}}=0.05$。流匹配损失 $\mathcal{L}_{\text{FM}}$ 负责像素级视频重建，而角度对齐与尺度对齐损失从方向与幅度两个互补维度引导模型学习几何结构。

### 关键设计决策

**为何选择中间层对齐？** 消融实验（Figure 3）表明，在 U-ViT 的第 3 层（中间层）施加对齐效果最优：FVD-256 降至最低，且不影响 16 帧短序列的生成质量。过早对齐可能干扰低级特征学习，过晚则几何信号难以有效渗透到生成过程。

**为何解耦角度与尺度？** 直接使用 MSE 对齐投影特征与目标特征（即同时约束方向与尺度）会导致 FVD-256 飙升至 1648（Table 3），远差于基线。这说明几何特征的方向与尺度属性具有不同的学习动态，解耦后分别用余弦相似度和尺度预测来引导，才能稳定地将三维结构注入扩散模型。定性结果（Figure 8）进一步显示，加入尺度对齐后，生成的相机跟随行为更加稳定逼真。

**隐式对齐 vs. 显式注入**：GF 在特征空间内部施加对齐，而非像 ControlNet 那样将几何特征作为外部条件显式注入网络。Table 4 和 Table 8 的对比表明，使用相同 VGGT 特征的显式注入方案 FVD-256 最高为 280，而 GF 达到 243，验证了内部隐式对齐在几何信息利用效率上的优势。

### 推理阶段

推理时，GF 不引入任何额外计算开销。模型仅使用训练好的 U-ViT backbone 通过求解概率流 ODE $\mathrm{d}\mathbf{x} = v_{\theta}(\mathbf{x}^{\mathbf{t}}, \mathbf{t}) \cdot \mathrm{d}\mathbf{t}$ 进行自回归采样，VGGT Teacher、Conv3D Projector 和 Scale Prediction Head 均不参与推理。

## 核心模块与公式推导

### 动机：视频扩散模型缺乏几何感知

视频扩散模型直接从原始像素数据学习时，其内部表示无法捕获有意义的三维结构。线性探测实验（Figure 1(c)）证实：冻结预训练视频扩散模型的中间特征，无法重建出有意义的深度图。这表明纯像素级训练目标忽略了场景的三维几何信息，导致生成视频缺乏时空一致性和长期稳定性。

### Geometry Forcing 框架

Geometry Forcing (GF) 通过在训练过程中将视频扩散模型的中间特征与预训练三维基础模型（VGGT）的几何感知特征对齐，迫使模型内部化三维表示。该框架由以下核心模块构成：

- **U-ViT Diffusion Backbone**：视频生成主干网络，采用7层下采样/瓶颈/上采样结构，基于流匹配（Flow Matching）训练。
- **VGGT Teacher**：预训练三维基础模型，提供目标几何特征。其Transformer骨干网络输出的中间特征作为对齐目标，蕴含丰富的三维结构信息。
- **Conv3D Projector**：将扩散模型潜变量映射到与VGGT特征兼容的维度，实现跨模型特征空间的对齐。
- **Scale Prediction Head (g_φ)**：从归一化后的扩散特征预测目标特征的尺度信息，用于保留幅度信息。

### 流匹配基础

视频扩散模型的前向过程对每一帧独立加噪：

$$x_i^{t_i} = (1 - t_i) \cdot x_i^0 + t_i \cdot \epsilon_i, \quad \text{where} \quad \epsilon_i \sim \mathcal{N}(0, I)$$

其中 $x_i^0$ 为干净帧，$\epsilon_i$ 为标准高斯噪声，$t_i$ 为时间步。网络 $v_{\theta}$ 被训练以预测速度场（噪声与干净输入的差）：

$$\mathcal{L}_{\mathrm{FM}} = \left\| v_{\theta}(\mathbf{x}^{\mathbf{t}}, \mathbf{t}) - (\epsilon - \mathbf{x}) \right\|^2$$

推理时，通过欧拉方法求解概率流ODE进行采样：

$$\mathrm{d}\mathbf{x} = v_{\theta}(\mathbf{x}^{\mathbf{t}}, \mathbf{t}) \cdot \mathrm{d}\mathbf{t}$$

### 几何表示对齐

GF的核心在于将扩散模型中间特征与VGGT几何特征对齐。设扩散模型隐藏状态为 $h$，VGGT目标特征为 $y$，对齐通过两个互补的损失函数实现。

#### 角度对齐损失

角度对齐强制扩散特征投影与目标几何特征的方向一致性，使用余弦相似度：

$$\mathcal{L}_{\mathrm{Angular}} = -\frac{1}{LNP} \sum_{\ell=1}^{L} \sum_{n=1}^{N} \sum_{p=1}^{P} \cos\left(y_{\ell,n,p}, f_{\phi}(h_{n,p})\right)$$

其中 $L$ 为VGGT特征层数，$N$ 为帧数，$P$ 为每帧的点数，$f_{\phi}$ 为Conv3D投影器。该损失仅约束方向，不限制幅度。

#### 尺度对齐损失

尺度对齐保留几何特征的幅度信息。首先对投影后的扩散特征进行归一化，再通过尺度预测头 $g_{\phi}$ 预测目标特征的完整值：

$$\mathcal{L}_{\mathrm{Scale}} = \frac{1}{LNP} \sum_{\ell=1}^{L} \sum_{n=1}^{N} \sum_{p=1}^{P} \left\| \tilde{y}_{\ell,n,p} - y_{\ell,n,p} \right\|_2^2$$

其中 $\tilde{y}$ 为预测的目标特征。该损失使模型不仅学习几何方向，还能保留尺度相关的结构信息。

### 整体训练目标

GF的最终训练目标为流匹配损失与两个对齐损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{FM}} + \lambda_{\mathrm{Angular}} \cdot \mathcal{L}_{\mathrm{Angular}} + \lambda_{\mathrm{Scale}} \cdot \mathcal{L}_{\mathrm{Scale}}$$

实验设置中 $\lambda_{\mathrm{Angular}}=0.5$，$\lambda_{\mathrm{Scale}}=0.05$。消融实验（Table 3）证实，角度对齐与尺度对齐的组合（FVD-256=243）显著优于仅角度对齐（FVD-256=253）或直接MSE（FVD-256=1648），验证了从方向与幅度两个维度解耦引导几何学习的必要性。

## 实验与分析

### 核心瓶颈与因果验证

视频扩散模型从原始像素数据训练时，其内部特征无法捕获有意义的三维几何结构。线性探测实验（Figure 1(c)）直接验证了这一瓶颈：冻结预训练视频扩散模型的中间特征，训练一个解码器重建深度图，结果无法产生有意义的几何表示。这表明纯像素级训练目标忽视了场景的三维一致性，导致生成内容在长期序列中出现几何漂移和暴露偏差。

Geometry Forcing (GF) 的核心因果机制在于：通过在训练过程中将扩散模型的中间特征与预训练三维基础模型 VGGT 的几何感知特征对齐，迫使模型内部化三维表示。这一对齐通过解耦的角度对齐（保持方向一致性）和尺度对齐（保留幅度信息）两个互补目标实现，从方向与幅度两个维度稳定地引导模型学习几何结构。

### 主实验结果

**RealEstate10K 基准测试**（Table 1）显示，GF 在短期（16帧）和长期（256帧）视频生成上均显著优于所有基线方法。在 256 帧设定下，GF 将 FVD 从 DFoT 的 364 降至 243（降幅 33.2%）；LPIPS 从 0.55 降至 0.51；几何一致性指标 RPE 从 0.3575 降至 0.3337，RVE 从 297 降至 272。在 16 帧设定下，GF 的 FVD 为 193，同样优于 DFoT 的 252 以及其他对比方法。这些结果涵盖了像素级质量（SSIM、PSNR）和几何一致性（RPE、RVE）的多维度指标，证据强度高（置信度 0.98）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on the RealEstate10K dataset for both short-term (16-Frame) and long-term (256-Frame) video generation. Our method (Geometry Forcing) achieves the best performance across all metrics. bold values denote the best, and Underlined values indicate the second best. * indicates the method is conditioned on the first frame only*

**定性分析**（Figure 2）展示了完整 360° 旋转相机视角下的视频生成对比。DFoT、VideoREPA、REPA 等基线方法在旋转过程中逐渐偏离起始视角，无法维持时序一致性；而 GF 生成的视频能够稳定地回到起始视点，验证了内化几何表示对长期一致性的关键作用。

### 目标表示消融

Table 2 对比了不同目标表示的对齐效果。仅对齐语义表示 DINOv2 将 FVD-256 降至 297，而仅对齐几何表示 VGGT 降至 243，降幅显著更大（相比基线 364）。两者联合使用进一步达到 237 的最佳 FVD。这表明几何表示提供的三维结构信息对视频一致性至关重要，且语义信息可作为有益补充。证据强度高（置信度 0.95）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/007_Table_2.jpg]]
*Table 2: Ablation study on target representation. We compare the effect of aligning the diffusion model with different target representations: DINOv2 (semantic), VGGT (geometric), and their combination. The joint use of both representation achieves the best FVD*

### 对齐损失组分消融

Table 3 验证了角度对齐与尺度对齐的各自贡献。仅使用角度对齐将 FVD-256 降至 253，而角度与尺度组合降至 243。直接使用 MSE 对齐（同时约束方向和幅度）导致 FVD 飙升至 1648，远差于基线（364）。这揭示了关键洞察：解耦对齐（分别处理方向和幅度）比简单联合约束更有效，因为 MSE 可能过度约束特征空间，干扰扩散模型原有的表示学习。尺度对齐的定性效果见 Figure 8：加入尺度对齐后，模型生成的相机跟随行为更稳定、更逼真。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/008_Table_3.jpg]]
*Table 3: Ablation study on alignment loss. Angular and Scale Alignment losses are evaluated for long-term video generation, with MSE as a naive baseline of aligning both angular and scale information. The combination of Angular and Scale Alignment yields the best results*

### 几何信息注入方式对比

Table 4 与 Table 8 系统对比了内部隐式对齐（GF）与外部显式注入的差异。使用相同 VGGT 特征，通过 ControlNet 进行外部潜变量特征注入的 FVD-256 为 275，渲染图像条件注入为 280，均不及 GF 的 243。这表明迫使模型内部学习几何感知表示比外部注入更有效——内部对齐使模型在生成过程中主动利用几何约束，而非被动接受外部信号。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/009_Table_4.jpg]]
*Table 4: Ablation study on explicit and implicit geometry information. We compare explicit geometry condition with internal alignment (ours)*

### 对齐策略消融

**对齐层级深度**（Figure 3）：在 U-ViT 架构中，中间层（第 3 层）对齐在 FVD-256 上表现最佳，且不影响 16 帧性能。对齐最后三层（Table 10）相比仅对齐中间层未带来进一步增益，说明中层特征已包含足够的几何结构信息。

**对齐上下文长度**（Table 9）：使用 16 帧提取 VGGT 特征进行对齐的 FVD-256 为 243，8 帧为 257，4 帧为 261。更长的上下文为几何基础模型提供更多观测视图，产生更准确的三维表示，从而更有效地引导扩散模型学习。

### 暴露偏差缓解

Figure 4 展示了长序列生成过程中 FVD 的累积趋势。基线方法在 100 帧后 FVD 急剧上升，暴露偏差严重；GF 在相同帧数后 FVD 显著更低且增长平缓。这直接证明内化的几何表示使模型在自回归生成中更稳定，有效缓解了误差累积。证据强度高（置信度 0.95）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_ULXYZCms41/figures/012_Figure_4.jpg]]
*Figure 4: Exposure bias analysis. This figure shows the trend of FVD scores during long-term video generation. Compared to the baseline, GF results in significantly lower FVD after 100 frames*

### 跨任务与跨模型泛化

**动作条件视频生成**（Table 5）：在 Minecraft 环境中，将 GF 应用于 NFD 模型，16 帧 FVD 从 216 降至 205，验证了 GF 在不同生成范式下的有效性。

**文本条件视频生成**（Table 11）：将 GF 应用于 Wan2.1 1.3B 模型，81 帧 FVD 和美学质量均有改善，表明 GF 可扩展至更大的文本条件视频扩散模型。

**教师模型兼容性**（Table 7）：使用 Pi3 替代 VGGT 作为几何教师，GF 仍将 FVD-256 降至 309（基线 364），证明该方法不依赖特定三维基础模型。

### 用户研究

Table 6 的用户研究（置信度 0.98）从人类感知角度验证了三维一致性。GF 在相机跟随（4.40）、物体一致性（4.44）、场景连续性（4.52）三个维度上均显著优于基线（1-5 分制），与定量指标相互印证。

### 失败模式与局限性

Figure 6 揭示了模型的典型失败案例：包含透明、反射材质（如玻璃桌）的场景中，物体间歇性消失和重现。这表明几何基础模型 VGGT 本身训练于静态场景，对反射/折射等非朗伯表面的几何推理能力有限，GF 继承并放大了这一局限。

训练阶段的计算开销剖析（Table 12）显示，VGGT 编码占训练步骤总时间的 53.4% 和总 FLOPs 的 60.4%。虽然 GF 通过加速收敛部分抵消了这一开销，但在资源受限场景下仍需权衡。此外，当前实验限于中等规模数据集（约 2K 训练视频），向更大规模数据集的扩展能力尚待验证。

## 方法谱系与知识库定位

### 1. 核心问题与因果机制

**真实瓶颈**：视频扩散模型在仅从原始像素数据训练时，无法自发捕获有意义的三维几何结构。线性探测实验（Figure 1(c)）直接证实了这一点——冻结的预训练视频扩散模型中间特征无法重建出有意义的深度图，表明纯流匹配损失驱动下的模型完全忽略了场景的三维底层表示。这导致生成内容在长序列中缺乏几何一致性和时空稳定性，尤其在相机大幅运动时出现漂移和崩坏。

**因果调节变量**：Geometry Forcing 的核心操作是将视频扩散模型中间层的隐藏状态与预训练三维基础模型（VGGT, Wang et al., 2025b）的几何感知特征进行对齐，迫使扩散模型在训练过程中内部化三维表示。这一对齐并非简单的特征蒸馏，而是通过解耦的角度对齐（Angular Alignment）和尺度对齐（Scale Alignment）两个互补目标实现。

**核心洞察**：角度对齐约束方向一致性（最大化余弦相似度），尺度对齐保留幅度信息（通过归一化扩散特征预测目标特征幅值）。两者的组合（FVD-256 = 243）显著优于仅角度对齐（FVD-256 = 253）或直接 MSE（FVD-256 = 1648），说明方向与幅度两个维度的协同约束是稳定引导模型学习几何结构的关键。

### 2. 方法定位与基线关系

Geometry Forcing 位于视频扩散模型与三维感知的交叉地带，其设计思路与以下基线形成明确对比：

**视频扩散基线**：
- **DFoT (Diffusion Forcing Transformer)**（Song et al., 2025）是本文的主要对比基线，采用 U-ViT 架构和流匹配训练范式。GF 直接在其基础上添加几何对齐损失，将 FVD-256 从 364 降至 243（降幅 33.2%），证明了几何感知特征对齐的独立增益。
- **Cosmos**（Agarwal et al., 2025）和 **NFD (Next-Frame Diffusion)**（Cheng et al., 2025）分别代表首帧条件生成和动作条件生成范式。GF 在 RealEstate10K 上全面超越 Cosmos，在 Minecraft 动作条件场景中将 NFD 的 FVD-16 从 216 降至 205（Table 5）。

**语义对齐基线**：
- **REPA**（Yu et al., 2024a）和 **VideoREPA**（Zhang et al., 2025c）通过在扩散训练中对齐语义表示（DINOv2 特征）提升生成质量。Table 2 的消融直接对比了语义对齐与几何对齐：VGGT 几何对齐将 FVD-256 降至 243，而 DINOv2 语义对齐仅降至 297，两者结合达到最优的 237。这明确表明，对于三维一致性任务，几何感知表示比语义表示更具信息量。

**教师模型兼容性**：
- GF 可与不同三维基础模型兼容。Table 7 显示，使用 **Pi3**（Wang et al., 2025）作为教师模型时，FVD-256 降至 309，虽不及 VGGT 的 243，但相比基线 DFoT 的 364 仍有显著提升，验证了方法的通用性。

### 3. 关键设计选择与消融证据

**内部隐式对齐 vs. 外部显式注入**：Table 4 和 Table 8 对比了三种几何信息注入方式：(1) 渲染图像条件注入（FVD-256 = 280）；(2) VGGT 潜特征显式注入（FVD-256 = 275）；(3) GF 内部隐式对齐（FVD-256 = 243）。内部对齐在所有指标上均优于显式注入，表明迫使模型学习几何感知表示比直接提供几何特征更有效。

**对齐层级深度**：Figure 3 的消融表明，U-ViT 的中间层（第 3 层）对齐最为有效——该层 FVD-256 最低且不影响 16 帧短序列性能。这与中间层通常编码结构性信息的认知一致。

**对齐上下文长度**：Table 9 显示，16 帧对齐（FVD-256 = 243）优于 8 帧（257）和 4 帧（261），说明更长的几何上下文有助于模型学习更稳健的三维表示。

### 4. 适用边界与局限

**已知局限**：
1. **反射/透明材质处理不稳定**：Figure 6 的失败案例显示，透明玻璃桌在生成帧中间歇性消失和重现，表明模型对非朗伯表面的几何理解仍有缺陷。
2. **训练计算开销**：Table 12 的剖析显示，VGGT 教师编码占训练步 53.4% 的时间和 60.4% 的 FLOPs。虽然 GF 加速收敛，但训练阶段的额外开销不可忽视。
3. **静态场景偏差**：VGGT 本身训练于静态场景数据，其几何表示可能限制 GF 在高度动态场景（如剧烈非刚性变形、多物体交互）中的泛化能力。
4. **规模验证不足**：当前实验主要基于 2K 训练视频的中等规模设置，扩展到更大规模数据集（如百万级视频）和更大模型（如数十亿参数）时的有效性有待验证。

**推理效率公平性**：GF 在推理时不引入额外计算开销——对齐损失仅在训练时使用，推理流程与标准扩散模型完全相同。

### 5. 开放问题

1. **规模化扩展**：几何强制能否在数十亿参数规模的视频扩散模型上保持有效性？更大模型是否本身就具备更强的几何学习能力，从而降低对外部几何对齐的依赖？

2. **结构化记忆机制**：内化的三维表示能否作为结构化记忆，支持超长视频的自回归生成？论文将“基于几何的记忆机制用于长期世界建模”列为未来工作方向。

3. **动态场景泛化**：在处理非刚性变形、快速运动模糊和复杂多物体交互时，当前基于静态场景训练的几何对齐策略是否仍然有效？可能需要动态场景下的三维基础模型作为教师。

4. **多属性三维对齐**：除深度/点云外，能否结合表面法向、语义布局、材质属性等其他三维属性来进一步增强一致性？Table 2 中 VGGT+DINOv2 组合的增益（FVD-256 = 237）暗示了多表示融合的潜力。

5. **文本条件视频生成的几何一致性**：Table 11 显示 GF 在 Wan2.1 1.3B 文本条件生成上仅带来边际美学质量提升（0.58 → 0.59），FVD 改善有限。如何将几何强制有效适配到无显式相机条件的开放式文本生成场景，仍是一个开放挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Geometry_Forcing_Marrying_Video_Diffusion_and_3D_Representation_for_Consistent_World_Modeling.pdf]]
