---
title: "HAD: Hallucination-Aware Diffusion Priors for 3D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HAD_Hallucination_Aware_Diffusion_Priors_for_3D_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- HADPH
- HAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过预测像素级幻觉分数图对扩散生成的增强视图进行选择性掩码，在3DGS优化中仅使用非幻觉区域计算损失，从而阻止虚假信息进入3D模型；同时利用多采样融合策略结合多个条件视图减少幻觉。
primary_logic: 利用在大规模3D数据上预训练的前馈新视角合成网络（LVSM）的编码器作为多视图理解骨干来检测扩散生成图像中的幻觉内容，并通过从不同输入视图条件化扩散模型生成多个版本并逐像素选择最低幻觉分数的融合策略，有效降低幻觉比例。
claims:
- 在DL3DV数据集上，HAD相比Difix3D将PSNR提高0.78dB（22.134 vs 21.355），同时SSIM和LPIPS也全面提升。
- 在跨域数据集MipNeRF360上，HAD达到18.689 PSNR，比Difix3D提升0.69dB，并优于使用视频扩散先验的GenFusion。
- 幻觉评分网络无需微调即可泛化到视频扩散模型GenFusion，并带来+0.23 PSNR的提升。
- 去除预训练初始化导致PSNR下降0.534（22.134 vs 21.600），证明基于NVS骨干的3D感知能力对幻觉评分至关重要。
---

# HAD: Hallucination-Aware Diffusion Priors for 3D Reconstruction

> [!tip] 核心洞察
> 利用在大规模3D数据上预训练的前馈新视角合成网络（LVSM）的编码器作为多视图理解骨干来检测扩散生成图像中的幻觉内容，并通过从不同输入视图条件化扩散模型生成多个版本并逐像素选择最低幻觉分数的融合策略，有效降低幻觉比例。

| 字段 | 内容 |
|------|------|
| 中文题名 | HAD：面向三维重建的幻觉感知扩散先验 |
| 英文题名 | HAD: Hallucination-Aware Diffusion Priors for 3D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.16873) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Hallucination-Aware Diffusion priors (HAD) |
| Dataset | DL3DV, MipNeRF360 |

> [!tip] 效果简介
> - DL3DV 上，PSNR 22.134 vs 21.355 (Difix3D) (+0.779)；SSIM 0.757 vs 0.734 (Difix3D) (+0.023)；LPIPS 0.190 vs 0.199 (Difix3D) (-0.009)。
> - MipNeRF360 上，PSNR 18.689 vs 18.001 (Difix3D) (+0.688)；SSIM 0.5094 vs 0.475 (Difix3D) (+0.0344)；LPIPS 0.334 vs 0.350 (Difix3D) (-0.016)。

## 概述

在稀疏视角三维重建中，扩散先验已被广泛用于增强新视角的视觉质量，但其引入的“幻觉”问题——即生成与输入视图不一致的虚假纹理与几何——长期被忽视。这些幻觉内容在迭代优化中会逐步累积放大，最终损害重建的保真度与可靠性。本文提出**幻觉感知扩散先验（Hallucination-Aware Diffusion priors, HAD）**，首次系统性地建模并抑制扩散辅助三维重建中的幻觉现象。

HAD的核心思路是：利用预训练前馈新视角合成网络（LVSM）的多视图理解能力，构建一个幻觉评分网络，对扩散生成的增强图像逐像素预测“幻觉分数”；在3DGS优化过程中，仅对非幻觉区域计算损失，从而阻断虚假信息进入三维模型。同时，HAD引入多采样融合策略——从不同输入视图条件化扩散模型生成多个增强版本，逐像素选择最低幻觉分数的像素进行融合——有效降低了幻觉比例。

实验表明，HAD在域内（DL3DV）和跨域（MipNeRF360）数据集上均显著优于现有方法：相比最直接的扩散先验辅助基线**Difix3D**（Wu et al., CVPR 2025），PSNR分别提升0.78 dB和0.69 dB，SSIM与LPIPS也全面改善。幻觉评分网络无需微调即可泛化到视频扩散模型**GenFusion**（Wu et al., CVPR 2025），带来+0.23 dB PSNR的增益。消融研究验证了预训练多视图编码器对幻觉评分的核心作用，以及单阶段训练策略的简洁有效性。

## 背景与动机

三维场景从稀疏视角输入进行重建是计算机视觉中的核心挑战。近年来，3D Gaussian Splatting（3DGS）凭借其高效的显式点基元表示和可微光栅化渲染，成为高质量新视角合成的主流框架。然而，当输入视角极度稀疏（例如仅3–9张图像）时，3DGS的优化过程因观测信息严重不足而难以收敛到真实场景几何与外观，渲染质量急剧下降。

为了弥补这一信息缺口，研究者开始引入扩散先验（diffusion prior）作为额外的监督信号。其基本思路是：利用预训练的图像或视频扩散模型，以当前3DGS渲染的粗糙图像为条件，生成视觉质量更高、细节更丰富的“增强视图”，并将这些增强视图作为伪真值（pseudo ground-truth）加入3DGS的训练损失中。**Difix3D**（Wu et al., CVPR 2025）和**GenFusion**（Wu et al., CVPR 2025）是该方向的代表性工作，分别在图像扩散先验和视频扩散先验的辅助下取得了显著的性能提升。

### 核心瓶颈：扩散先验的幻觉问题

尽管扩散先验能有效提升渲染图像的视觉逼真度，但它引入了一个关键但尚未被充分解决的副作用——**幻觉（hallucination）**。扩散模型在去噪生成过程中，由于缺乏对底层三维场景结构的显式约束，会“凭空编造”出与输入观测不一致的纹理细节和几何结构。这些幻觉内容在视觉上可能高度逼真，但与真实场景存在偏差，表现为虚假纹理、错位边缘、浮动物体（floaters）和几何畸变。

更严重的是，在迭代优化的3DGS管线中，幻觉具有**累积放大效应**。如原文Figure 4所示，即使初始3DGS输出中的微小瑕疵（如轻微浮点或几何扭曲），也会被扩散先验逐步放大，最终演变为清晰可见的幻觉伪影。这一现象在Difix3D和GenFusion中均被观察到，表明幻觉并非孤立引入，而是在迭代精化过程中不断恶化。因此，直接将扩散增强视图作为无差别监督信号，会将这些虚假信息反向传播至3D模型参数，损害重建的**保真度（fidelity）**——即渲染结果与真实场景之间的一致性。

### 现有方法的缺口

现有的扩散辅助三维重建方法存在一个共同的盲区：**它们将扩散生成的增强视图整体视为可靠监督，缺乏对其中幻觉内容的感知与过滤机制**。具体而言：

- **Difix3D**采用两阶段训练策略（先训练初始3DGS，再渐进引入扩散增强视图），试图通过延迟增强视图的参与来缓解幻觉影响，但并未从根本上识别和剔除幻觉像素。
- **GenFusion**利用视频扩散模型的多帧一致性来提升生成质量，但同样缺乏像素级的可靠性评估，幻觉问题依然存在。
- 上述方法均未利用多视图输入中蕴含的三维结构信息来检测生成图像中的不一致区域。

### 本文动机

基于上述分析，本文的核心动机是：**在利用扩散先验增强稀疏视角重建的同时，显式建模并抑制其引入的幻觉内容，从而在保持视觉逼真度的前提下提升重建保真度**。

为实现这一目标，本文提出**Hallucination-Aware Diffusion priors（HAD）**框架，其核心思想是：

1. **幻觉感知**：利用在大规模三维数据上预训练的前馈新视角合成网络（LVSM）的编码器作为多视图理解骨干，构建幻觉评分网络（Hallucination Score Network），对扩散生成的增强视图进行像素级幻觉分数预测。
2. **选择性掩码**：基于幻觉分数图生成二值掩码，在3DGS优化中仅对非幻觉区域计算损失，阻止虚假信息进入三维模型。
3. **多采样融合**：从不同输入视图条件化扩散模型生成多个增强版本，逐像素选择幻觉分数最低的像素进行融合，有效降低幻觉比例。

通过这一“感知–掩码–融合”的闭环机制，HAD首次在扩散辅助三维重建中实现了对幻觉内容的显式建模与主动抑制，为稀疏视角重建的保真度提升开辟了新的技术路径。

## 核心创新

HAD（Hallucination-Aware Diffusion priors）的核心创新在于**首次显式建模并抑制扩散先验在三维重建中引入的幻觉内容**。现有方法（如 **Difix3D**，Wu et al., CVPR 2025）利用扩散模型增强稀疏视角下的新视图，虽能提升视觉逼真度，却不可避免地产生与输入视图不一致的虚假纹理和几何结构——这些“幻觉”在迭代优化中被逐步放大，最终损害重建保真度。HAD 围绕这一瓶颈设计了三个相互协同的创新机制。

### 1. 像素级幻觉评分与选择性掩码

HAD 的核心操控变量是**像素级幻觉分数图**。与 Difix3D 对整幅增强图像计算损失不同，HAD 引入一个幻觉评分网络（Hallucination Score Network），为扩散生成的每个像素预测其“不可靠程度”，并据此生成二元掩码，使 3DGS 优化仅对非幻觉区域计算损失：

$$
\mathcal{L}_{\mathrm{novel}} = \mathcal{L}_1(\neg\mathbf{m}\odot\mathcal{R}_\Phi(\tilde{\mathbf{c}}), \neg\mathbf{m}\odot\tilde{\mathbf{i}}) + \mathcal{L}_{\mathrm{D\text{-}SSIM}}(\neg\mathbf{m}\odot\mathcal{R}_\Phi(\tilde{\mathbf{c}}), \neg\mathbf{m}\odot\tilde{\mathbf{i}})
$$

这一设计从根源上切断了虚假信息向三维模型的传播路径。幻觉评分网络的关键设计在于：其编码器复用了预训练前馈新视角合成网络 **LVSM** 的特征骨干，通过多视图特征聚合获得三维结构理解能力。消融实验证实，去除预训练初始化会导致 PSNR 下降 0.534 dB（22.134 → 21.600），证明这种三维感知能力对幻觉检测至关重要。

### 2. 单阶段训练策略

Difix3D 采用两阶段训练——先训练初始 3DGS，再渐进引入扩散增强视图——以避免早期训练中幻觉内容的破坏性影响。HAD 凭借幻觉掩码的保护，**将训练简化为单阶段**：从训练起始即可同时使用输入视图和增强视图。这一改变不仅简化了训练流程，更使得 3DGS 在早期就能受益于扩散先验的增强信息，同时不被幻觉污染。

### 3. 多采样融合策略

为降低单次扩散生成的不确定性，HAD 提出多采样融合：从 $K$ 个不同输入视图分别条件化扩散模型，生成 $K$ 个增强版本，再**逐像素选择幻觉分数最低的像素**进行融合：

$$
\tilde{\mathbf{i}}[i] = \tilde{\mathbf{i}}_{\mathcal{G}}^{k^*}[i], \quad k^* = \arg\min_k \mathbf{s}^k[i]
$$

实验表明，ArgMin 策略优于加权平均（PSNR 22.134 vs 21.856），且 $K=4$ 时达到最佳性能，继续增加收益递减。这一模块以约 $K$ 倍推理时间为代价，换取了更可靠的增强视图质量。

### 创新点之间的关系

三个创新形成闭环：幻觉评分网络提供像素级可靠性信号，使单阶段训练成为可能，同时为多采样融合提供逐像素选择依据；多采样融合进一步降低幻觉比例，减轻评分网络的负担。这种协同使得 HAD 在 DL3DV 上相比 Difix3D 提升 0.78 dB PSNR，在跨域 MipNeRF360 上提升 0.69 dB，且幻觉评分网络无需微调即可泛化到视频扩散模型 **GenFusion**（+0.23 dB PSNR），展现出模型无关的通用性。

## 整体框架

HAD 的整体训练流程围绕一个核心矛盾展开：扩散先验在增强稀疏视角三维重建时，会不可避免地引入与输入视图不一致的“幻觉”内容（如虚假纹理和几何），这些内容虽然在视觉上逼真，却严重损害重建的保真度。HAD 通过**幻觉感知的损失掩码机制**，在 3DGS 优化过程中阻止这些不可靠信息进入三维模型。

### 数据流与模块关系

如图 Figure 2 所示，系统包含四个协同工作的核心模块：

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/002_Figure_2.jpg]]
*Figure 2: Overview of framework – We train 3DGS with input images and HAD-augmented novel views. HAD combines a pretrained diffusion prior (which generates images from 3DGS-rendered views conditioned on reference input images) with our hallucination score network (which predicts pixel-wise reliability maps). Our multi-sampling strategy fuses multiple generated versions into refined augmented views. Hallucination scores guide 3DGS optimization by masking off unreliable content, thus improving reconstruction quality*

1. **扩散先验 (Diffusion Prior)**：以 3DGS 当前渲染图像 $\mathcal{R}_\Phi(\tilde{\mathbf{c}})$ 和参考输入视图 $\mathbf{i}_{\mathrm{ref}}$ 为条件，通过去噪生成增强的新视角图像 $\tilde{\mathbf{i}}_{\mathcal{G}}$（Eq. 9）。该模块负责提供视觉质量更高的监督信号，但同时也是幻觉的主要来源。

2. **幻觉评分网络 (Hallucination Score Network)**：接收多视图特征 $\mathbf{F}_{\tilde{\mathbf{c}}}$（由预训练的前馈新视角合成网络 LVSM 的编码器 $\mathcal{V}$ 从输入视图 $\mathbf{P}$ 中提取，Eq. 11）以及扩散生成图像 $\tilde{\mathbf{i}}_{\mathcal{G}}$ 和当前渲染 $\mathcal{R}_\Phi(\tilde{\mathbf{c}})$，输出像素级的幻觉分数图 $\mathbf{s}$（Eq. 10）。该分数图量化了每个像素与多视图几何一致性的偏离程度——分数越高，该像素越可能是幻觉。其架构细节见 Figure 6：由一个冻结的 LVSM 特征骨干和一个三层 U-Net 评分分支组成。

3. **多采样融合 (Multi-Sampling Fusion)**：从 $K$ 个不同输入视图作为条件，运行扩散先验生成 $K$ 个增强版本，然后逐像素选择幻觉分数最低的版本进行融合（Eq. 12）。这一策略利用了不同条件视图导致不同幻觉模式的现象，通过“取最小值”有效降低了最终增强图像中的幻觉比例。

4. **3DGS 优化 (3DGS Optimization)**：同时使用输入视图和经过幻觉掩码的增强新视角来训练高斯场景表示 $\Phi$。总损失函数为输入视图损失和增强视图损失的加权和（Eq. 6），其中输入视图损失采用标准的 L1 和 D-SSIM 加权组合（Eq. 7），而增强视图损失的关键创新在于：**仅对幻觉掩码 $\neg\mathbf{m}$ 标记的非幻觉区域计算 L1 和 D-SSIM**（Eq. 8），幻觉区域不参与梯度回传。

### 训练策略：从两阶段到单阶段

与最直接的基线方法 **Difix3D**（Wu et al., CVPR 2025）不同，HAD 采用**单阶段训练策略**。Difix3D 需要先训练一个初始 3DGS 模型，再渐进地引入扩散增强视图（两阶段训练），因为直接从头使用扩散增强视图会将幻觉内容固化到模型中。HAD 凭借幻觉评分网络提供的像素级可靠性掩码，能够在训练伊始就直接融合扩散增强视图，而不会让虚假信息污染三维表示。这一简化不仅提升了训练效率，还避免了初始 3DGS 模型中的偏差对后续优化的影响。

### 输入输出流总结

- **输入**：稀疏的多视图图像集 $\mathbf{P}$（如 9 个视角）
- **中间产物**：扩散增强的新视角图像 $\tilde{\mathbf{i}}_{\mathcal{G}}$、幻觉分数图 $\mathbf{s}$、融合后的增强图像 $\tilde{\mathbf{i}}$
- **输出**：优化后的 3DGS 场景表示 $\Phi$，可从任意新视角渲染出高保真且幻觉受控的图像

整体框架的核心洞察在于：利用在大规模 3D 数据上预训练的前馈新视角合成网络（LVSM）的编码器作为多视图理解骨干，来检测扩散生成图像中的幻觉内容——这种 3D-aware 的特征表示是准确识别几何不一致性的关键。

## 核心模块与公式推导

### 3.1 问题建模与训练目标

HAD的核心思想是在3DGS优化过程中引入幻觉感知机制，使扩散先验增强的新视角图像中不可靠区域被选择性掩码，从而阻止虚假内容污染三维模型。整体训练目标为：

$$\underset{\Phi}{\arg\min}\,\lambda_{\mathrm{input}}\mathcal{L}_{\mathrm{input}} + \lambda_{\mathrm{novel}}\mathcal{L}_{\mathrm{novel}} \tag{6}$$

其中 $\Phi$ 为3DGS的场景参数，$\mathcal{L}_{\mathrm{input}}$ 为输入视图的渲染损失，$\mathcal{L}_{\mathrm{novel}}$ 为经幻觉掩码过滤后的增强新视角损失。

输入视图损失采用标准的L1与D-SSIM加权组合：

$$\mathcal{L}_{\mathrm{input}} = 0.8\mathcal{L}_1(\mathcal{R}_\Phi(\mathbf{c}),\mathbf{i}) + 0.2\mathcal{L}_{\mathrm{D-SSIM}}(\mathcal{R}_\Phi(\mathbf{c}),\mathbf{i}) \tag{7}$$

其中 $\mathcal{R}_\Phi(\mathbf{c})$ 表示3DGS在相机位姿 $\mathbf{c}$ 下的渲染图像，$\mathbf{i}$ 为对应的真实输入视图。

增强新视角损失则引入幻觉掩码 $\mathbf{m}$，仅对非幻觉区域计算损失：

$$\mathcal{L}_{\mathrm{novel}} = \mathcal{L}_1(\neg\mathbf{m}\odot\mathcal{R}_\Phi(\tilde{\mathbf{c}}), \neg\mathbf{m}\odot\tilde{\mathbf{i}}) + \mathcal{L}_{\mathrm{D-SSIM}}(\neg\mathbf{m}\odot\mathcal{R}_\Phi(\tilde{\mathbf{c}}), \neg\mathbf{m}\odot\tilde{\mathbf{i}}) \tag{8}$$

其中 $\tilde{\mathbf{c}}$ 为新视角位姿，$\tilde{\mathbf{i}}$ 为经HAD增强后的新视角图像，$\mathbf{m}$ 为二值幻觉掩码（由幻觉分数阈值化得到），$\neg\mathbf{m}$ 表示取反后仅保留非幻觉区域，$\odot$ 为逐元素乘法。

与Difix3D的两阶段训练策略不同，HAD采用**单阶段训练**：由于幻觉掩码能从训练起始即有效过滤不可靠像素，扩散增强视图可直接与输入视图一同参与优化，无需预训练初始3DGS模型。

### 3.2 扩散先验生成模块

扩散先验以3DGS在当前新视角的渲染图像和参考输入视图为条件，通过去噪生成增强的新视角图像：

$$\tilde{\mathbf{i}}_{\mathcal{G}} = \mathcal{G}(\mathcal{R}_\Phi(\tilde{\mathbf{c}}) \vert \mathbf{i}_{\mathrm{ref}}) \tag{9}$$

其中 $\mathcal{G}$ 为预训练的扩散模型，$\mathcal{R}_\Phi(\tilde{\mathbf{c}})$ 为3DGS在目标视角的当前渲染结果，$\mathbf{i}_{\mathrm{ref}}$ 为选定的参考输入视图。扩散模型以前向加噪过程为基础：

$$x_\tau = \alpha_\tau x + \sigma_\tau \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{4}$$

并通过去噪目标训练：

$$\mathbb{E}_{\boldsymbol{x}\sim p_{\mathrm{data}},\tau\sim p_\tau,\epsilon\sim\mathcal{N}(0,I)}\big[\|\epsilon - \epsilon_\theta(x_\tau; c, \tau)\|_2^2\big] \tag{5}$$

扩散先验的增强能力使渲染图像在视觉上更逼真，但同时也引入了与输入视图不一致的幻觉内容——这正是HAD要解决的核心问题。

### 3.3 幻觉评分网络

幻觉评分网络 $S_\theta$ 是HAD的关键创新，其作用是预测扩散生成图像中每个像素的幻觉分数：

$$\mathbf{s} = S_\theta(\tilde{\mathbf{i}}_{\mathcal{G}} | \mathcal{R}_\Phi(\tilde{\mathbf{c}}), \mathbf{F}_{\tilde{\mathbf{c}}}) \tag{10}$$

其中 $\mathbf{s}$ 为像素级幻觉分数图，分数越高表示该像素越可能是幻觉内容。网络接收三个输入：
- $\tilde{\mathbf{i}}_{\mathcal{G}}$：扩散先验生成的增强图像；
- $\mathcal{R}_\Phi(\tilde{\mathbf{c}})$：3DGS在当前视角的渲染图像，提供当前模型已知的几何与纹理信息；
- $\mathbf{F}_{\tilde{\mathbf{c}}}$：多视图聚合特征，编码了输入视图在目标视角的3D一致性信息。

多视图特征通过预训练的前馈新视角合成网络（LVSM）的特征编码器提取：

$$\mathbf{F}_{\tilde{\mathbf{c}}} = \mathcal{V}(\mathbf{P} \mid \tilde{\mathbf{c}}) \tag{11}$$

其中 $\mathbf{P}$ 为所有输入视图的集合，$\mathcal{V}$ 为LVSM的冻结特征骨干网络，在目标视角 $\tilde{\mathbf{c}}$ 处聚合多视图特征。这一设计的核心洞察在于：**在大规模3D数据上预训练的前馈NVS编码器天然具备多视图几何理解能力**，能够有效区分扩散生成图像中与多视图几何一致的像素和偏离3D结构的幻觉像素。

幻觉评分网络的架构由两部分组成：冻结的LVSM特征编码器（提供多视图3D感知能力）和一个轻量的三层U-Net评分分支（将多视图特征与生成图像融合后输出像素级分数）。该网络在精心构造的多视图-幻觉新视角图像对上训练，学习预测与真实图像之间的像素级差异。

### 3.4 多采样融合策略

为进一步降低幻觉比例，HAD引入多采样融合：从 $K$ 个不同输入视图作为参考条件，分别运行扩散先验生成 $K$ 个增强版本，然后逐像素选择幻觉分数最低的像素进行融合：

$$\tilde{\mathbf{i}}[i] = \tilde{\mathbf{i}}_{\mathcal{G}}^{k^*}[i], \quad k^* = \arg\min_k \mathbf{s}^k[i] \tag{12}$$

其中 $\tilde{\mathbf{i}}_{\mathcal{G}}^k$ 为第 $k$ 个参考视图条件下生成的增强图像，$\mathbf{s}^k$ 为其对应的幻觉分数图。ArgMin策略确保每个像素位置都选取最可靠的生成结果，从而获得比单一增强版本更高质量的融合图像。消融实验表明，ArgMin策略优于加权平均（PSNR 22.134 vs 21.856），且采样版本数增至4时达到最优收益递减点。

### 3.5 幻觉掩码生成与梯度阻断

幻觉分数图 $\mathbf{s}$ 通过阈值 $\tau = 0.9$ 二值化为掩码 $\mathbf{m}$：分数高于阈值的像素被标记为幻觉区域并在损失计算中排除。这一硬掩码机制直接阻断了幻觉像素的梯度回传，防止不可靠的监督信号影响3DGS参数更新。

### 补充图表

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/014_Figure_6.jpg]]
*Figure 6: Overview of hallucination scoring network – The network predicts a pixel-wise hallucination score map s for a hallucinated novel view*

## 实验与分析

### 核心定量结果

HAD 在两个公开数据集上均取得了最优性能，显著超越了现有基于扩散先验的稀疏视角重建方法。

**域内评估（DL3DV）**：如 Table 1 所示，HAD 在 9 视图稀疏输入设定下达到 **22.134 PSNR**，相比最直接的基线 Difix3D（Wu et al., CVPR 2025）提升 **0.78 dB**；SSIM 从 0.734 提升至 0.757，LPIPS 从 0.199 降至 0.190。值得注意的是，采用与 Difix3D 相同两阶段训练策略的 Ours* 变体也达到 21.779 PSNR（Table 3），验证了幻觉评分网络本身带来的增益独立于训练策略的简化。

**跨域泛化（MipNeRF360）**：在 Table 2 中，HAD 达到 **18.689 PSNR**，比 Difix3D 高出 **0.69 dB**，并优于使用视频扩散先验的 GenFusion（Wu et al., CVPR 2025）。SSIM 从 0.475 提升至 0.509，LPIPS 从 0.350 降至 0.334，表明幻觉感知机制在分布外场景中同样有效。

**密集视角设置**：即使在 24 个输入视图的密集设定下，HAD 仍比 Difix3D 提高 0.20 dB PSNR（Table 7），说明幻觉问题并非稀疏视角独有，HAD 的掩码机制在信息更丰富的条件下依然能过滤扩散先验引入的虚假细节。

### 消融实验

**组件贡献（Table 3）**：以 Difix3D 为基准（21.355 PSNR），单独加入幻觉评分网络（Difix3D + HAD）即提升至 21.779 PSNR，进一步叠加多采样融合后达到 22.134 PSNR。两个组件各自贡献了可观的性能增益，且相互正交。

**多采样版本数（Table 4）**：采样版本数从 1 增至 4 时，PSNR 从 21.856 单调上升至 22.134；继续增加至 6 时收益递减（22.098），表明 4 个版本在质量与计算开销间取得最优平衡。

**融合策略（Table 5）**：ArgMin（逐像素选取最低幻觉分数的版本）达到 22.134 PSNR，显著优于加权平均（21.856 PSNR）。这一结果表明，幻觉具有局部性——不同扩散生成版本在不同位置产生幻觉，硬选择能更有效地从多个候选版本中拼接出最可靠的像素。

**幻觉评分网络设计**：
- Table 6 以 MAE 评估幻觉分数估计精度：完整模型（预训练多视图编码器 + 三层 U-Net）取得最低 MAE，去除预训练权重或 3DGS 渲染输入均导致精度显著下降。
- Table 10 直接衡量对重建的影响：去除预训练初始化使 PSNR 从 22.134 降至 21.600（下降 **0.534 dB**），证明基于前馈 NVS 骨干（LVSM）的 3D 感知能力对幻觉评分至关重要。

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/017_Table_10.jpg]]
*Table 10: The impact of different design choices in hallucination score network on the 3D reconstruction*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/010_Table_6.jpg]]
*Table 6: Different hallucination score estimators. We use Mean Absolute Error (MAE) of the predicted hallucination score maps as our evaluation metric. We demonstrate that our hallucination score network, with the pretrained multiview encoder, achieves the best performance*

### 幻觉评分网络的泛化性

HAD 的幻觉评分网络展现出令人瞩目的零样本泛化能力：
- **视频扩散模型**（Table 8）：将幻觉评分网络直接应用于 GenFusion 的视频扩散先验，无需任何微调，即带来 **+0.23 PSNR** 的提升。Figure 7 展示的掩码示例表明，网络能准确识别视频扩散生成图像中的幻觉区域。
- **多视图扩散模型**（Figure 9）：同样无需微调即可泛化至多视图扩散 SVC，进一步验证了幻觉评分网络学习到的是跨扩散范式的通用幻觉模式。

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/012_Table_8.jpg]]
*Table 8: Improving GenFusion [43] via HAD. We demonstrate that our hallucination scoring network generalizes to video diffusion models without fine-tuning, effectively masking hallucinated pixels and improving reconstruction quality. We test it on DL3DV [25]*

### 幻觉模式分析

Figure 4 揭示了扩散辅助 3DGS 管线中幻觉的累积放大机制：Difix3D（图像扩散）和 GenFusion（视频扩散）在迭代增强 3DGS 渲染的过程中，初始 3DGS 输出中的轻微瑕疵（如小型漂浮物或几何畸变）会被扩散先验逐步放大，最终演化为肉眼可见的幻觉。这表明幻觉并非一次性引入，而是在迭代优化中持续累积——这正是 HAD 从训练起始即使用幻觉掩码的关键动机。

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/011_Figure_4.jpg]]
*Figure 4: Qualitative demonstration of hallucination pattens in diffusion-assisted 3DGS pipelines. Both Difix3D (image diffusion) and GenFusion (video diffusion) iteratively enhance the 3DGS rendering. As a result, even mild artifacts in the initial 3DGS output, such as small floaters or subtle geometric distortions, can be progressively amplified by diffusion priors and eventually evolve into clearly visible hallucinations. This demonstrates that hallucination is not introduced abruptly, but can accumulate and become more pronounced during iterative refinement. Note: method-3DGS denotes direct rendering from 3DGS, while method-diffusion denotes diffusion-enhanced results*

### 局限性

1. **计算开销**：多采样策略每次融合需运行 K 次扩散去噪（默认 K=4），推理时间约为单次生成的 K 倍，限制了实时应用场景。
2. **固定阈值**：二元掩码阈值被经验性地设为 0.9，缺乏对场景内容和幻觉置信度的自适应调整，可能在边缘情况导致过掩码或欠掩码。
3. **数据分布依赖**：幻觉评分网络在 DL3DV 上训练，虽展现出强泛化性，但在显著不同的数据分布下评分精度可能下降。
4. **表示扩展性**：当前仅验证了 3DGS 表示，在 NeRF 等其他 3D 表示上的有效性尚未测试。

### 补充图表

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of different methods on DL3DV [25]. Best, second, and third results are highlighted in 1st , 2nd , and 3rd , respectively. (↑: higher is better, ↓: lower is better). Note that ours* denotes a variant following the twophase 3DGS optimization strategy of Difix3D, enabling a fair comparison between diffusion priors with and without hallucination awareness. We denote*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison of different methods on Mip-Nerf360 [3]. Note the results of Genfusion and FSGS are from Genfusion [43]*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/006_Table_3.jpg]]
*Table 3: Impact of different components*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/008_Table_4.jpg]]
*Table 4: Number of versions in multi-sampling strategy*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/009_Table_5.jpg]]
*Table 5: Fusion methods in multi-sampling strategy. We compare two approaches: (1) ArgMin: selecting pixels with the lowest hallucination score; (2) Weighted Average: computing the weighted mean*

![[assets/figures/papers/paper_list_l2258_https_arxiv_org_abs_2605_16873/figures/007_Table_7.jpg]]
*Table 7: The performance of our method in dense view setting (24 views)*

## 方法谱系与知识库定位

### 问题定位：扩散先验的“幻觉”困境

在稀疏视角三维重建中，扩散先验（Diffusion Prior）已成为增强新视角合成质量的核心手段。然而，现有方法面临一个根本性瓶颈：**扩散模型在增强视图时不可避免地引入与输入观测不一致的“幻觉”内容**（如虚假纹理、错位几何），导致渲染图像虽视觉逼真但保真度受损。这一问题在迭代优化的3DGS管线中尤为严重——如Figure 4所示，初始3DGS输出的轻微漂浮物或几何畸变会被扩散先验逐步放大，最终演化为清晰可见的伪影。这一瓶颈直接限制了扩散辅助重建的可靠性，构成了本文的核心动机。

### 方法谱系：从两阶段掩码到单阶段幻觉感知

**HAD**（Hallucination-Aware Diffusion priors）在方法谱系中的定位可从以下维度理解：

**与最直接基线Difix3D的关系。** **Difix3D**（Wu et al., CVPR 2025）是当前扩散先验辅助3DGS的代表方法，其核心策略是两阶段训练：先仅用输入视图训练初始3DGS，再渐进引入扩散增强视图。这一设计本质上是对幻觉问题的隐式规避——通过延后增强视图的介入时机来减少伪影影响。HAD对此进行了根本性重构，体现在三个关键槽位：

1. **训练阶段**：从两阶段简化为单阶段。HAD的幻觉掩码机制使得增强视图可从训练起始即安全引入（Eq. 6-8），无需等待初始3DGS收敛。这一简化不仅是工程上的便利，更意味着方法不再依赖“先获得可靠初始模型”这一前提假设。

2. **损失函数设计**：Difix3D对整幅增强图像计算L1和D-SSIM损失；HAD则通过幻觉评分图$\mathbf{s}$生成二元掩码$\mathbf{m}$，仅对非幻觉区域计算损失（Eq. 8）。这一差异是因果调节的关键——切断了幻觉像素到3D模型参数的梯度传播路径。

3. **增强策略**：Difix3D仅使用最近邻参考视图进行单次扩散增强；HAD引入多采样融合（Eq. 12），从K个不同输入视图条件化扩散模型，逐像素选择最低幻觉分数的版本。这利用了“不同条件视图诱导的幻觉模式不相关”这一特性来降低整体幻觉比例。

**与前馈新视角合成方法的关系。** HAD的方法论创新高度依赖前馈NVS网络的预训练能力。具体而言，幻觉评分网络的多视图编码器$\mathcal{V}$（Eq. 11）直接复用了**LVSM**（Large View Synthesis Model）的冻结特征骨干。LVSM本身属于前馈新视角合成方法，与**DepthSplat**（Xu et al., CVPR 2025）等方法共享“从稀疏输入视图直接回归目标视角图像”的范式（Eq. 3）。HAD的独特之处在于：它并未直接使用LVSM的渲染输出，而是将其多视图理解能力迁移到“判断另一生成模型输出是否与多视图几何一致”这一元任务上。这一设计选择的关键证据来自Table 10：去除预训练初始化导致重建PSNR下降0.534（22.134→21.600），证明基于大规模3D数据预训练获得的3D感知能力对幻觉评分至关重要。

**与视频扩散先验方法的关系。** **GenFusion**（Wu et al., CVPR 2025）使用视频扩散模型替代图像扩散模型来生成时序一致的多视角增强。HAD展示了对这一范式的直接泛化能力：在Table 8中，将HAD的幻觉评分网络（未在视频扩散数据上微调）集成到GenFusion中，带来+0.23 PSNR的提升。这一结果揭示了幻觉评分网络的“模型无关”特性——它学习的是“生成内容与多视图几何的一致性”这一通用判据，而非特定扩散模型的伪影模式。Figure 7和Figure 8进一步展示了跨扩散范式的掩码效果。

**与其他稀疏视角方法的对比定位。** 在稀疏视角重建的更大谱系中，**FSGS**（Zhu et al., ECCV 2024）代表无需扩散先验的高斯泼溅稀疏重建方法，而**Gsplat-mcmc**代表改进的3DGS优化策略。Table 1和Table 2的系统比较表明，扩散先验方法（Difix3D、HAD）在视觉质量上显著优于纯几何优化方法，但HAD是首个在享受扩散增强收益的同时显式控制幻觉风险的方法。

### 适用边界与局限

HAD的有效性已在以下条件下得到验证，但其适用边界同样明确：

**已验证的适用范围：**
- **3D表示**：仅验证于3DGS（Gsplat实现），扩展到NeRF或其他表示的有效性尚未测试。
- **输入设置**：稀疏视角（9视图）和密集视角（24视图）均有效，Table 7显示密集设置下仍有+0.20 dB PSNR提升。
- **数据集分布**：域内（DL3DV）和跨域（MipNeRF360）均表现一致，Table 1和Table 2分别验证。
- **扩散模型类型**：图像扩散（Difix3D所用）和视频扩散（GenFusion所用）均可受益。

**已知局限：**
1. **训练数据依赖性**：幻觉评分网络在DL3DV上训练，虽泛化能力强，但在显著不同的数据分布下评分精度可能下降。这一局限需要人工验证具体目标域的表现。
2. **计算开销**：多采样策略每次融合需运行K次扩散去噪，推理时间约为单次增强的K倍。Table 4显示K=4时收益饱和，但未讨论延迟的具体数值。
3. **阈值固定性**：二元掩码阈值被经验性设为0.9，缺乏对场景内容和幻觉置信度的自适应调整机制。这可能导致在幻觉模糊区域出现过度掩码或漏检。
4. **未见区域的主动生成**：当前方法仅防御性地掩码幻觉，未尝试利用幻觉评分来主动引导不可见区域的内容生成。

### 开放问题

从当前方法出发，存在若干值得探索的方向：

1. **从防御到引导**：幻觉评分网络能否反向用于指导扩散模型的采样过程？即，在去噪过程中注入“与多视图几何一致”的约束，从源头抑制幻觉产生，而非事后检测。

2. **自适应阈值机制**：能否设计基于场景内容和幻觉置信度的动态阈值策略，替代固定的0.9？例如，利用幻觉分数图的不确定性估计来自动调节掩码的严格程度。

3. **表示泛化**：HAD的幻觉感知机制是否适用于基于NeRF或基于网格的重建管线？核心挑战在于不同表示对“局部伪影”的敏感度和传播方式不同。

4. **幻觉评分的自监督学习**：当前幻觉评分网络需要配对的真值图像进行监督训练。能否利用多视图一致性约束（如不同增强版本间的差异）进行自监督或弱监督训练，降低对标注数据的依赖？

5. **计算效率优化**：多采样策略的K次推理开销能否通过共享去噪步骤或渐进式融合来降低？这直接关系到方法的实际部署可行性。

## 原文 PDF

![[paperPDFs/CVPR_2026/HAD_Hallucination_Aware_Diffusion_Priors_for_3D_Reconstruction.pdf]]