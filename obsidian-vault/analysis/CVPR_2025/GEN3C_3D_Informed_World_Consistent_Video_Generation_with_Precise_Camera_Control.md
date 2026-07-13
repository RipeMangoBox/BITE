---
title: "GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/GEN3C/
code_link: null
aliases:
- GEN3C
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入一个由深度估计和反投影构建的显式三维点云缓存（3D cache），并将其渲染为二维视频作为强条件注入视频扩散模型；这一“3D引导渲染”将视频生成任务转化为在已知几何体上的补全、修复与运动推进任务。"
primary_logic: "将输入视图转化为三维点云缓存，并以该缓存的二维渲染作为模型条件，可以使视频扩散模型专注于生成未观测区域和修正深度投影带来的伪影，从而同时实现精准的相机控制、视角一致性以及长期视频一致性。"
claims:
- "在单视图视频生成任务上，GEN3C 在域内（RE10K）和域外（Tanks-and-Temples）的像素对齐及感知指标均显著优于所有基线（如 CameraCtrl、MotionCtrl、NVS-Solver 等），PSNR 提升约 2–3 dB。"
- "在极端稀疏两视图新视合成中，GEN3C 在外推视角下的表现远优于基于重建的基线（PixelSplat、MVSplat），即使输入视图重叠很小，也能生成平滑、真实的新视角。"
- "在驾驶场景新视合成中，当新轨迹横向偏移达到 4 米时，GEN3C 的 FID 仅为 35.33，远低于重建基线 Nerfacto（112.40）和 3D-GS（81.26），证明生成模型具有很强的缺失区域填补能力。"
- "基于最大池化的多视图融合策略优于显式点云融合（Explicit fusion），在 RE10K 插值/外推任务上取得更高 PSNR/SSIM/LPIPS，同时模型对深度估计噪声具有良好的鲁棒性。"
---

# GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control

> [!tip] 核心洞察
> 将输入视图转化为三维点云缓存，并以该缓存的二维渲染作为模型条件，可以使视频扩散模型专注于生成未观测区域和修正深度投影带来的伪影，从而同时实现精准的相机控制、视角一致性以及长期视频一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GEN3C：具有精确相机控制的3D感知世界一致性视频生成 |
| 英文题名 | GEN3C: 3D-Informed World-Consistent Video Generation with Precise Camera Control |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.03751) · [Project](https://research.nvidia.com/labs/toronto-ai/GEN3C/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GEN3C |
| Dataset | RE10K (域内), Tanks-and-Temples (域外), Two-view NVS (RE10K 插值/外推), Driving NVS (y±4.0m) |

> [!tip] 效果简介
> - RE10K (域内) 上，PSNR↑ / SSIM↑ / LPIPS↓ / TSED↑ 为 19.88 / 0.78 / 0.20 / 0.9143，对比 CameraCtrl 18.40 / 0.72 / 0.25 / 0.8033，变化 PSNR +1.48, SSIM +0.06, LPIPS -0.05, TSED +0.1110。
> - Tanks-and-Temples (域外) 上，PSNR↑ / SSIM↑ / LPIPS↓ 为 18.66 / 0.67 / 0.20，对比 NVS-Solver 16.95 / 0.59 / 0.27，变化 PSNR +1.71, SSIM +0.08, LPIPS -0.07。
> - Two-view NVS (RE10K 插值/外推) 上，PSNR↑ / SSIM↑ / LPIPS↓ 为 22.22 / 0.76 / 0.14 (插值), 20.51 / 0.72 / 0.16 (外推)，对比 MVSplat 20.90 / 0.70 / 0.39 (插值), 16.08 / 0.63 / 0.44 (外推)，变化 插值 PSNR +1.32, SSIM +0.06, LPIPS -0.25; 外推 PSNR +4.43, SSIM +0.09, LPIPS -0.28。

## 概要

### 问题背景

现有视频生成模型在实现精确相机控制和长序列世界一致性方面面临根本性瓶颈：模型缺乏对三维场景结构的显式建模，必须在生成过程中从相机参数隐式推测三维几何，并记忆历史内容以维持时空一致性。这导致两个突出问题——相机运动不精确，以及当相机重新访问同一区域时出现物体“闪现”等严重不一致伪影（Figure 2）。

### 核心思想

GEN3C 提出了一条因果性解决路径：**将视频生成转化为在已知几何体上的补全、修复与运动推进任务**。具体而言，方法维护一个由深度估计和反投影构建的显式三维点云缓存（3D cache），将其按用户指定的相机轨迹渲染为二维条件视频，注入视频扩散模型。这一“3D引导渲染”策略使得扩散模型无需从零推测场景几何，而是专注于生成未观测区域和修正深度投影带来的伪影，从而同时实现精准相机控制、视角一致性及长期视频一致性（Figure 3）。

### 方法定位

GEN3C 位于**生成式新视合成**与**可控视频生成**的交叉点。不同于依赖隐式相机条件注入的基线方法（如 **CameraCtrl** 使用 Plücker 射线嵌入），GEN3C 将相机控制从神经网络内部的黑盒参数化转变为外部的显式三维渲染条件。相比基于重建的稀疏视图方法（如 **PixelSplat**（Charatan et al., CVPR 2024）、**MVSplat**（Chen et al., ECCV 2024）），GEN3C 利用视频扩散模型的生成先验填补缺失区域，而非仅依赖可微渲染，因此在极端视角外推和遮挡区域表现出更强的鲁棒性。

### 主要结果概要

- **单视图视频生成**：在域内数据集 RE10K 上，GEN3C 取得 PSNR 19.88 dB，较 CameraCtrl（18.40 dB）提升约 1.5 dB；在域外数据集 Tanks-and-Temples 上，PSNR 达 18.66 dB，显著优于 NVS-Solver（16.95 dB）（Table 1）。
- **稀疏两视图新视合成**：在外推场景下，GEN3C 的 PSNR 达 20.51 dB，远超 MVSplat（16.08 dB），LPIPS 降低 0.28（Table 2）。
- **驾驶场景新视合成**：当相机横向偏移达 4 米时，GEN3C 的 FID 仅为 35.33，而重建基线 Nerfacto（Tancik et al., SIGGRAPH 2023）和 3D-GS（Kerbl et al., SIGGRAPH 2023）分别为 112.40 和 81.26（Table 3）。
- **方法鲁棒性**：最大池化多视图融合策略在遮挡和光照不一致场景下优于显式点云融合；模型对深度估计噪声具有良好的容忍度（Table 5, Table 6）。

### 适用范围与局限

GEN3C 支持单视图/稀疏视图新视合成、单目动态视频新视合成、驾驶仿真以及电影级特效（如 Dolly Zoom、3D 编辑）等多种应用（Figure 1）。当前方法依赖现成深度估计器，在透明/反射表面可能产生错误深度；推理速度较慢（14帧约30秒，A100），自回归生成可能引入累积误差；动态场景的时序一致性仍有提升空间。

### 视频生成中的三维一致性困境

近年来，基于扩散模型的视频生成取得了显著进展，能够根据文本或图像条件生成逼真的视频序列。然而，当用户需要对生成视频施加精确的相机控制——例如指定一条环绕物体的相机轨迹——时，现有模型普遍暴露出一个根本性问题：**缺乏对三维场景结构的显式建模**。

传统可控视频生成方法（如 **CameraCtrl**、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）通常将相机参数（如 Plücker 射线嵌入）直接注入神经网络，期望模型隐式地从二维训练数据中学会三维几何推理。这种“从相机参数直接推测三维几何”的范式带来了两个核心瓶颈：

1. **相机控制不精确**：由于模型没有显式的几何先验，生成视频中的物体位置、遮挡关系往往无法与指定相机轨迹精确对齐。当相机回到之前经过的区域时，场景内容可能出现严重的时空不一致，表现为物体“闪现”或纹理漂移（见 Figure 2）。
2. **长序列生成中的记忆退化**：模型必须隐式地“记忆”已生成的历史内容，以保持跨帧一致性。随着视频长度增加，这种隐式记忆机制不可避免地导致累积误差和内容遗忘。

### 从“推测几何”到“条件化几何”

本文的核心洞察在于：**将视频生成任务重新表述为在已知三维几何上的补全、修复与运动推进任务**。具体而言，GEN3C 提出了一种范式转变——不再要求扩散模型从零开始推测场景的三维结构，而是：

1. 首先利用现成的深度估计器从输入视图构建一个**显式三维点云缓存**（3D cache）；
2. 将该缓存按照用户指定的相机轨迹**渲染为二维条件视频**；
3. 让视频扩散模型在已知几何的“骨架”上，专注于生成未观测区域的内容和修正深度投影带来的伪影。

这一设计将三维一致性问题从生成模型的黑箱中解耦出来：**几何一致性由显式三维缓存保证，而外观真实感和缺失区域填补由生成模型负责**。如 Figure 2 所示，当相机重复经过同一区域时，GEN3C 能够保持场景内容的一致性，而先前方法则产生严重的伪影。

### 现有方法的缺口

在三维感知视频生成这一交叉领域，现有工作可大致分为三类，但均存在明显局限：

- **基于重建的新视合成方法**（如 **Nerfacto** (Tancik et al., SIGGRAPH 2023)、**3D-GS** (Kerbl et al., SIGGRAPH 2023)、**PixelSplat** (Charatan et al., CVPR 2024)、**MVSplat** (Chen et al., ECCV 2024)）：这些方法通过优化或前馈方式重建场景的三维表示，在新视角渲染时具有天然的几何一致性。然而，它们对输入视图的覆盖范围高度敏感——当新视角偏离输入轨迹较远时，缺失区域会暴露为空洞或模糊伪影，缺乏生成式填补能力。
- **生成式新视合成方法**（如 **NVS-Solver** (You et al., arXiv 2024)、**GenWarp** (Seo et al., NeurIPS 2024)、**GCD** (Van Hoorick et al., ECCV 2024)）：这些方法利用扩散模型的先验知识来生成新视角，具有较强的缺失区域填补能力，但通常缺乏对三维场景结构的显式维护，导致跨视角和长序列中的几何一致性不足。
- **相机可控视频生成方法**（如 **CameraCtrl**、**MotionCtrl**）：这些方法能够根据相机参数生成视频，但如前所述，其相机控制精度和长时一致性受限于隐式几何推理的瓶颈。

GEN3C 的目标正是弥合这一缺口：**同时具备重建方法的几何一致性和生成方法的缺失区域填补能力**，并在此基础上实现精确的相机控制和长序列视频生成。

## 核心方法与创新机理

GEN3C 的核心创新在于将视频生成任务重构为“在已知三维几何体上的补全、修复与运动推进”问题，从而一举解决了现有视频生成模型在相机控制精度与长序列时空一致性上的两个根本性瓶颈。

### 瓶颈与因果调控

现有视频生成模型（如 **CameraCtrl**、**MotionCtrl** (Wang et al., SIGGRAPH 2024)）通常将相机参数（如 Plücker 射线嵌入）直接作为神经网络的条件向量输入。这迫使模型隐式地从相机参数中推测三维几何结构，并完全依赖网络记忆来维持长序列中的历史内容一致性。其直接后果是：当相机轨迹回环或覆盖已观测区域时，模型无法精确复现先前生成的内容，导致物体“闪现”或场景畸变等严重伪影（见 Figure 2）。

GEN3C 的因果调控手段是引入一个**显式的时空三维点云缓存**。该缓存由现成深度估计器（DAV2）预测的逐像素深度经反投影构建，形成一个 $L \times V$ 维的点云数组。模型不再以原始相机参数为条件，而是以该三维缓存在新相机轨迹下的二维渲染视频（RGB 图像与二值遮罩）作为强条件。这一“三维引导渲染”策略将生成模型的职责从“凭空想象几何与外观”转变为“在已知几何体上填补未观测区域并修正深度投影带来的伪影”。

### 关键设计槽位变更

相较于基线方法，GEN3C 在两个关键设计槽位上做出了根本性改变：

| 设计槽位 | 基线方案 | GEN3C 方案 | 证据锚点 |
|----------|----------|------------|----------|
| **相机条件模态** | Plücker 射线嵌入或其他参数化相机向量直接输入神经网络 | 将用户相机轨迹下的三维点云缓存渲染为 RGB 视频和遮罩，作为视频扩散模型的显式条件 | Sec. 4.3, Sec. 5.2（CameraCtrl 使用 Plücker embeddings 替换渲染视频进行对比实验） |
| **长时一致性机制** | 隐式历史（如潜在特征图）或缺乏维护 | 自回归更新显式三维缓存，通过最小化重投影误差将新生成帧的深度与已有点云对齐并合并 | Sec. 4.5, Appendix A.1 |

在相机条件槽位上，GEN3C 将抽象的相机参数替换为具体的三维几何投影。渲染视频中的遮罩通道明确标示了哪些像素区域需要模型生成（即点云未覆盖的缺失区域），哪些区域可以直接依赖缓存内容。这使得模型的任务边界变得清晰，从而在像素对齐指标（PSNR）上相较 CameraCtrl 提升约 1.5–1.7 dB（Table 1），在视角一致性指标（TSED）上提升超过 0.11。

在长时一致性槽位上，GEN3C 的自回归缓存更新机制是其能够生成长达数百帧一致性视频的关键。推理时，长视频被划分为有重叠的块逐段生成；每段生成后，通过最小化重投影误差优化深度估计的尺度 $s$ 和偏移 $t$：

$$s, t = \underset{s,t}{\operatorname{argmin}} \left\| \left( s \cdot \mathbf{d} + t - \mathbf{d}^{\mathrm{tgt}} \right) \cdot M \right\|_2^2$$

对齐后的深度 $\mathbf{d}^{\prime} = s \cdot \mathbf{d} + t$ 被反投影为新的点云并与现有缓存合并，确保后续生成块能够精确引用先前生成的三维结构。这从根本上消除了模型对历史内容的“遗忘”问题。

### 多视图融合策略

当存在多个输入视图时，GEN3C 需要将各视点渲染的潜变量融合为统一的条件信号。基线方法（如显式点云融合或通道拼接）在输入视图存在深度估计不一致或光照差异时容易产生融合伪影。GEN3C 采用“In-Layer + 最大池化”的置换不变融合策略：

$$\mathbf{z}^{v,\prime} = \text{In-Layer}(\text{Concat}(\mathbf{z}^{v} \odot \mathbf{M}^{v,\prime}, \mathbf{z}_{\tau}))$$

$$\mathbf{z}^{\prime} = \mathrm{Max-Pool}\{\mathbf{z}^{1,\prime}, \ldots, \mathbf{z}^{V,\prime}\}$$

各视点的渲染潜变量先与目标噪声潜变量拼接并通过扩散模型的第一层网络处理，随后对所有视点输出进行最大池化聚合。消融实验（Table 6, Figure 10）表明，该策略在遮挡和光照不一致场景中显著优于显式点云融合，在 RE10K 两视图外推任务上 PSNR 达到 20.51（显式融合为 19.85），LPIPS 降至 0.16（显式融合为 0.19）。

### 创新本质总结

GEN3C 的创新不在于提出新的视频扩散架构或深度估计方法，而在于**将三维几何先验以可渲染、可更新的显式缓存形式注入生成流程**。这一设计使得视频生成模型从“黑箱推测几何”转向“白箱利用几何”，从而在相机控制精度（像素对齐）、视角一致性（TSED）和长序列稳定性三个维度上同时取得了显著提升。该范式的另一优势是**基座可扩展性**：使用更强大的基础视频生成模型（如 Cosmos）可进一步提升生成质量并实现极端视角变化（Section 5.7, Figure 11–12），表明三维缓存条件与扩散模型骨干是解耦的。

GEN3C 的核心设计思路是将视频生成任务重新定义为**在已知三维几何体上的补全、修复与运动推进**，而非让模型从相机参数隐式推测场景结构。为此，方法构建了一条从“显式三维缓存构建”到“二维条件渲染”再到“视频扩散生成”的流水线，其整体流程如 Figure 3 所示。

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/003_Figure_3.jpg]]
*Figure 3: Overview of GEN3C. With the user input, which can be a single-view image, multi-view images, or dynamic video(s), we first build a spatiotemporal 3D cache (Sec. 4.1) by predicting the depth for each image and unprojecting it into 3D. With the camera poses from the user, we then render the cache into video(s) (Sec. 4.2), which are fed into the video diffusion model to generate a photorealistic video that aligns with the desired camera poses (Sec. ${ \mathcal { R } } _ { } \in { \mathcal { E } } _ { } \mathrm { ~ { ~ \mathcal ~ { ~ E ~ } ~ } ~ } ^ { }$

### 输入与三维缓存构建

系统接受多种形式的用户输入，包括单张图像、多视图图像或动态视频。无论输入形式如何，第一步都是为每一帧预测逐像素深度，并将其反投影为三维点云，从而构建一个**时空三维缓存**（spatiotemporal 3D cache）。该缓存被组织为一个 $L \times V$ 的点云数组，其中 $L$ 为时间维度长度，$V$ 为视点数量。对于单视图输入，$L=1$ 且 $V=1$；对于多视图或视频输入，则分别沿视点轴或时间轴扩展。

深度估计采用现成的单目深度估计器（DAV2），并通过最小化重投影误差来优化全局尺度 $s$ 和平移 $t$，使深度图与场景尺度对齐：

$$s, t = \underset{s,t}{\operatorname{argmin}} \left\| \left( s \cdot \mathbf{d} + t - \mathbf{d}^{\mathrm{tgt}} \right) \cdot M \right\|_2^2$$

对齐后的深度 $\mathbf{d}^{\prime} = s \cdot \mathbf{d} + t$ 被用于反投影，形成与场景几何一致的初始点云。

### 条件渲染与多视图融合

构建好三维缓存后，系统根据用户指定的相机轨迹，将点云光栅化渲染为二维视频序列。渲染函数定义为：

$$(I^{t,v}, M^{t,v}) := \mathcal{R}(\mathbf{P}^{t,v}, \mathbf{C}^t)$$

其中 $I^{t,v}$ 为渲染得到的 RGB 图像，$M^{t,v}$ 为二值遮罩，标示未被点云覆盖（即需要模型“想象”填充）的像素区域。这一对输出构成了视频扩散模型的**显式条件**。

当存在多个输入视图时，系统为每个视图独立渲染条件视频，然后通过**置换不变的最大池化融合策略**进行聚合。具体而言，每个视点的渲染潜变量 $\mathbf{z}^v$ 与目标噪声潜变量 $\mathbf{z}_\tau$ 拼接后，分别送入扩散模型的第一层（In-Layer）处理：

$$\mathbf{z}^{v,\prime} = \text{In-Layer}(\text{Concat}(\mathbf{z}^{v} \odot \mathbf{M}^{v,\prime}, \mathbf{z}_{\tau}))$$

随后对所有视点的输出进行最大池化：

$$\mathbf{z}^{\prime} = \mathrm{Max-Pool}\{\mathbf{z}^{1,\prime}, \ldots, \mathbf{z}^{V,\prime}\}$$

这种融合方式相较于显式点云融合或通道拼接，在面对视点间深度不一致、光照差异或遮挡时表现出更强的鲁棒性（见 Table 6 和 Figure 10）。

### 视频扩散生成与自回归推理

融合后的特征 $\mathbf{z}^{\prime}$ 被送入视频扩散模型（基于 Stable Video Diffusion 微调）的去噪主干网络。模型以渲染视频和 CLIP 图像特征为条件，在潜空间中进行去噪得分匹配训练，目标函数为：

$$\mathbb{E}_{\mathbf{x}_0 \sim p_{\mathrm{data}}(\mathbf{x}), \tau \sim p_{\tau}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ \lVert \mathbf{f}_{\theta}(\mathbf{x}_{\tau}; \mathbf{c}, \tau) - \mathbf{y} \rVert_2^2 \right]$$

这样，扩散模型只需专注于两项任务：**修复深度投影带来的伪影**（如透明表面、细小结构的深度错误）和**生成被遮罩标记的未观测区域**，而非从零开始推理整个三维场景。

对于长视频生成，GEN3C 采用**自回归推理**策略：将长序列划分为有单帧重叠的块（每块长度 $L$），逐段生成。每段生成后，新帧的深度被估计、对齐并通过最小化重投影误差与已有点云合并，从而增量更新三维缓存，保证跨段的时间一致性。这一机制是 GEN3C 实现“相机多次经过同一区域时仍保持场景一致”（如 Figure 2 所示）的关键。

### 方法定位

从方法谱系看，GEN3C 处于**生成式新视合成**与**可控视频生成**的交叉点。与 CameraCtrl 等依赖 Plücker 射线嵌入的隐式相机控制方法不同，GEN3C 将相机条件显式化为三维缓存的二维渲染，使模型不必同时承担几何推理与图像生成的双重负担。与 PixelSplat（Charatan et al., CVPR 2024）、MVSplat（Chen et al., ECCV 2024）等基于重建的稀疏视图方法相比，GEN3C 利用视频扩散模型的生成先验来填补大范围缺失区域，而非仅依赖可微渲染的插值能力，这在外推场景中优势尤为显著（PSNR 提升约 4.4 dB）。

### 3.1 时空三维缓存构建

GEN3C 的核心创新在于引入一个显式的时空三维点云缓存（3D cache），作为连接二维图像生成与三维场景几何的桥梁。给定输入图像，系统首先利用现成的单目深度估计器（DAV2）预测逐像素深度，随后通过反投影（unprojection）将 RGB-D 数据提升为三维点云。对于单视图输入，缓存为一个 $1 \times 1$ 的点云数组；对于多视图或视频输入，缓存扩展为 $L \times V$ 的时空点云数组，其中 $L$ 为时间帧数，$V$ 为视点数量。这一显式三维表示将视频生成任务重新定义为“在已知几何体上的补全、修复与运动推进”问题，从根本上解决了隐式方法在相机控制精度和长时一致性上的瓶颈。

### 3.2 点云光栅化渲染与遮蔽掩码

为了将三维缓存注入二维视频扩散模型，系统根据用户指定的相机轨迹对点云进行光栅化渲染。渲染函数形式化定义为：

$$(I^{t,v}, M^{t,v}) := \mathcal{R}(\mathbf{P}^{t,v}, \mathbf{C}^t)$$

其中 $\mathbf{P}^{t,v}$ 为时刻 $t$ 视点 $v$ 对应的点云，$\mathbf{C}^t$ 为目标相机参数（包含内外参）。渲染器 $\mathcal{R}$ 输出两个关键组件：RGB 图像 $I^{t,v}$ 提供对已知几何体的视觉参考，二值遮罩 $M^{t,v}$ 则精确标示未被点云覆盖的“缺失区域”。这一遮罩机制至关重要——它明确告知扩散模型哪些区域需要生成新内容（如遮挡解除后的背景），哪些区域可以依赖已有几何信息进行纹理细化。

### 3.3 多视图潜变量融合与注入

当存在多个输入视点时（如稀疏视图新视合成），GEN3C 需要对不同视点的渲染信息进行有效融合。系统采用“逐视图 In-Layer + 最大池化”的置换不变融合策略：

**步骤一：逐视图编码。** 对每个视点 $v$，将渲染潜变量 $\mathbf{z}^{v}$ 与遮罩 $\mathbf{M}^{v,\prime}$ 进行逐元素乘积后，与目标噪声潜变量 $\mathbf{z}_{\tau}$ 拼接，送入扩散模型的第一层网络：

$$\mathbf{z}^{v,\prime} = \text{In-Layer}(\text{Concat}(\mathbf{z}^{v} \odot \mathbf{M}^{v,\prime}, \mathbf{z}_{\tau}))$$

**步骤二：最大池化聚合。** 对所有视点的输出特征图进行逐元素最大池化，实现置换不变的视点信息聚合：

$$\mathbf{z}^{\prime} = \text{Max-Pool}\{\mathbf{z}^{1,\prime}, \ldots, \mathbf{z}^{V,\prime}\}$$

消融实验（Table 6）表明，最大池化策略在 RE10K 插值/外推任务上显著优于显式点云融合（Explicit fusion）和通道拼接（Concat），尤其在输入视图存在深度估计误差或光照不一致时表现出更强的鲁棒性。

### 3.4 训练目标：去噪得分匹配

GEN3C 在潜空间中对预训练 Stable Video Diffusion 进行微调，训练目标为标准去噪得分匹配损失：

$$\mathbb{E}_{\mathbf{x}_0 \sim p_{\mathrm{data}}(\mathbf{x}), \tau \sim p_{\tau}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ \lVert \mathbf{f}_{\theta}(\mathbf{x}_{\tau}; \mathbf{c}, \tau) - \mathbf{y} \rVert_2^2 \right]$$

其中 $\mathbf{x}_0$ 为干净视频潜变量，$\mathbf{x}_{\tau}$ 为加噪版本（噪声水平 $\tau$），$\mathbf{f}_{\theta}$ 为待训练的扩散模型，$\mathbf{c}$ 为条件信号（包含渲染视频和 CLIP 图像特征），$\mathbf{y}$ 为目标预测（噪声 $\epsilon$ 或原始数据 $\mathbf{x}_0$，取决于参数化方式）。通过最小化该损失，模型学习如何从三维缓存渲染中推断缺失区域的真实外观，同时保持与已知几何体的精确对齐。

### 3.5 自回归推理与缓存更新

对于长视频生成，GEN3C 采用分块自回归策略：将目标序列划分为长度为 $L$ 的块，相邻块之间保持一帧重叠。每生成一个块后，系统对新生成帧进行深度估计，并通过最小化重投影误差与已有三维缓存对齐：

$$s, t = \underset{s,t}{\operatorname{argmin}} \left\| \left( s \cdot \mathbf{d} + t - \mathbf{d}^{\mathrm{tgt}} \right) \cdot M \right\|_2^2$$

其中 $\mathbf{d}$ 为新帧预测深度，$\mathbf{d}^{\mathrm{tgt}}$ 为缓存中对应点的深度，$M$ 为有效区域遮罩。优化得到的尺度 $s$ 和偏移 $t$ 用于归一化深度：

$$\mathbf{d}^{\prime} = s \cdot \mathbf{d} + t$$

对齐后的点云被合并入缓存，作为下一块生成的三维条件。这一增量式更新机制确保了跨块的时间一致性，避免了隐式方法中常见的物体“闪现”问题。

## 实验与关键发现

### 核心性能验证

GEN3C 在多个任务维度上展现出显著优势，其性能提升的因果根源在于将视频生成问题转化为“在已知几何体上的补全与运动推进”——模型只需修复深度投影伪影并填补未观测区域，而无须从相机参数中隐式推断三维结构。

**单视图视频生成**（Table 1）：在域内数据集 RE10K 上，GEN3C 的 PSNR 达到 19.88，较 **CameraCtrl** 的 18.40 提升约 1.48 dB；感知一致性指标 TSED 从 0.8033 提升至 0.9143，增幅达 13.8%。在域外数据集 Tanks-and-Temples 上，GEN3C 的 PSNR 为 18.66，较 **NVS-Solver**（You et al., arXiv 2024）的 16.95 提升 1.71 dB，LPIPS 降低 0.07。这一跨域泛化能力表明，显式三维缓存作为条件信号，其几何先验具有任务无关的通用性，而非对特定数据分布的过拟合。

**稀疏两视图新视合成**（Table 2, Figure 6）：在极端外推场景下，GEN3C 的优势尤为突出——PSNR 达 20.51，远超基于 3D 高斯泼溅的 **MVSplat**（Chen et al., ECCV 2024）的 16.08，LPIPS 从 0.44 降至 0.16。即使输入视图重叠极小，GEN3C 仍能生成平滑、真实的过渡视角。这一结果揭示了生成式方法相较于重建式方法的核心优势：当观测信息极度稀疏时，生成先验能够合理“想象”缺失区域，而重建方法只能产生模糊或扭曲的插值。

**驾驶场景新视合成**（Table 3, Figure 7）：当新轨迹横向偏移达 4 米时，GEN3C 的 FID 仅为 35.33，而 **Nerfacto**（Tancik et al., SIGGRAPH 2023）为 112.40，**3D-GS**（Kerbl et al., SIGGRAPH 2023）为 81.26。FID 差距超过 45 点，直观反映了生成模型在填补大面积未观测区域时的能力——重建基线因缺乏对应观测而暴露出空洞和撕裂伪影，GEN3C 则利用扩散先验生成符合场景语义的内容。

**单目动态新视合成**（Table 4, Figure 9）：在 Kubric4D 数据集上，GEN3C 的 FID 为 98.58，较 **GCD**（Van Hoorick et al., ECCV 2024）的 150.64 降低 52.06，LPIPS 从 0.48 降至 0.29。值得注意的是，GEN3C 在保持动态物体细节方面表现更优（Figure 15），这表明三维缓存即使对动态场景也能提供有效的几何约束，模型在此约束下生成的动态内容更不易偏离原始运动模式。

### 消融研究：设计选择的因果效应

**多视图融合策略**（Table 6, Figure 10）：最大池化融合（Ours）在 RE10K 两视图 NVS 任务上显著优于显式点云融合（Explicit fusion）和通道拼接（Concat）。以插值任务为例，最大池化的 PSNR/SSIM/LPIPS 为 22.22/0.76/0.14，而显式融合为 21.50/0.74/0.16。性能差距的根源在于：显式融合要求不同视图的点云在三维空间精确对齐，当输入视图存在光照不一致或深度估计偏差时，融合后的点云会产生重影和错位；最大池化在特征空间进行置换不变聚合，天然容忍视图间的表观差异，使模型能从多个“不完美”的渲染中提取最可靠的信息。Figure 10 的定性对比直观展示了这一机制——当输入视图光照差异明显时，显式融合产生模糊伪影，而最大池化策略生成的视角清晰且真实。

**深度估计鲁棒性**（Table 5）：向深度估计添加 10%–20% 的中等噪声时，GEN3C 在两视图 NVS 上的性能下降很小。这一结果验证了方法的核心设计理念：视频扩散模型并非被动接受深度投影，而是主动修复深度误差。Figure 14 提供了这一机制的直观证据——渲染深度图中的错误投影（如栏杆断裂、光源错位）在模型输出中被自动纠正。这种“生成式纠错”能力使方法对现成深度估计器的精度要求降低，增强了实际部署的可行性。

**基座模型可扩展性**：当将基础视频扩散模型从 Stable Video Diffusion 替换为更强大的 Cosmos 时，生成质量进一步提升，且能处理更极端的视角变化（Figure 11, Figure 12）。这表明 GEN3C 的三维缓存条件框架与扩散模型骨干解耦，可随生成模型技术的进步而持续获益。

### 失败模式与局限性

尽管整体性能优异，GEN3C 在以下场景中存在可辨识的失败模式：

1. **复杂光学表面的深度估计失效**：方法依赖现成深度估计器（DAV2），在面对透明玻璃、镜面反射等表面时，深度预测可能严重偏离真实几何。错误深度直接污染三维缓存，导致渲染视频中的几何结构扭曲，扩散模型虽有纠错能力，但在深度误差过大时仍会产生明显伪影。

2. **高度动态场景的缓存失效**：当前三维缓存基于静态场景假设构建，对于包含大幅非刚性运动（如奔跑的行人、摇曳的树木）的场景，点云缓存无法准确表示动态物体的几何变化。自回归更新虽能部分缓解，但动态物体的缓存本质上仍是过时的，导致生成视频中动态区域的时序一致性下降。

3. **推理延迟与累积误差**：在 A100 GPU 上生成 14 帧视频约需 30 秒，限制了实时应用。此外，自回归分块生成机制中，前序块的误差（如深度对齐偏差）会传播至后续块，在极长序列中可能累积为可察觉的漂移。

4. **多视图输入的同步性假设**：当前多视图融合假设输入视图时间同步且相机位姿精确已知。当视图间存在时间差或位姿估计存在大范围误差时，不同视图的渲染视频将指向不一致的三维区域，最大池化融合可能选择错误的特征来源，导致生成结果中出现内容冲突。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/008_Figure.jpg]]
*Figure: Up 1m Up 2m*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative results on 3D editing for driving scene. We remove and modify the trajectory of cars from the original scene*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/014_Figure_10.jpg]]
*Figure 10: Qualitative results on ablating different fusion strategies. GEN3C can generate a realistic novel view with misaligned depth and different lighting in the input views, while the explicit fusion strategy fails*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/016_Figure_11.jpg]]
*Figure 11: Qualitative comparison on using different base models: Stable Video Diffusion (SVD) [4] v.s. Cosmos [1]. When having a more powerful video generation model, GEN3C is able to generate more realistic output with less artifacts. Note that the slight misalignment between the two results is due to the models using different video resolutions. Figure 12. Example of extreme NVS using Cosmos as the base model: the input view is the middle one, and our model is capable of rotating significantly to the left and right*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/018_Figure_14.jpg]]
*Figure 14: Illustration of rendered depth images and model outputs. Our model can fix the error in the depth projection (such as the orange handrail in the first image and the light in the second one), and generate realistic content in the missing regions (such as the inpainted railway)*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/020_Figure_16.jpg]]
*Figure 16: Comparison of different strategies for incorporating masking information into the model. (Left) the mask channel is concatenated to the latent as an additional channel. (Right) the mask values are applied directly to the latent through element-wise multiplication*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative results on novel view synthesis for driving scene. Our model can fill in the missing regions in the original video even when the deviation is large, while reconstruction-based baselines produce severe artifacts. Table 2. Quantitative results for two-views NVS. The two values in each table cell represent the interpolation and extrapolation results, respectively*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/010_Table_3.jpg]]
*Table 3: Quantitative results of FID [18] for NVS on driving scene. GEN3C significantly outperforms the baselines, especially when generating novel views that are far away from the original trajectory*

![[assets/figures/papers/paper_list_l48_https_arxiv_org_abs_2503_03751/figures/013_Table_6.jpg]]
*Table 6: Ablation of different fusion strategies on RE10K dataset. The two values in each table cell represent the interpolation and extrapolation results, respectively*

## 定位与知识库关联

### 核心方法定位

GEN3C 本质上是一种**以显式三维几何缓存为条件、以视频扩散模型为生成先验的新视合成与视频生成框架**。其核心创新在于将视频生成任务重新表述为“在已知三维几何体上的补全、修复与运动推进”问题，从而将相机控制的精度、视角一致性和长期视频一致性统一在同一个显式三维表示之下。

这一设计将 GEN3C 置于两条研究线的交汇处：

1. **相机可控视频生成**：以 **CameraCtrl** 和 **MotionCtrl**（Wang et al., SIGGRAPH 2024）为代表的工作，通过将相机参数（如 Plücker 射线嵌入）直接注入扩散模型来实现相机控制。GEN3C 的关键突破在于，它用**三维点云缓存的二维渲染视频**替代了抽象的相机参数嵌入。这一“渲染即条件”的策略，将相机控制从需要模型隐式推断三维几何的任务，转变为在已知几何上做纹理补全的任务，从而在 RE10K 上带来 PSNR +1.48 dB、TSED +0.1110 的显著提升（Table 1）。

2. **生成式新视合成**：以 **NVS-Solver**（You et al., arXiv 2024）和 **GenWarp**（Seo et al., NeurIPS 2024）为代表的零样本扩散新视合成方法，以及以 **PixelSplat**（Charatan et al., CVPR 2024）和 **MVSplat**（Chen et al., ECCV 2024）为代表的稀疏视图 3D 高斯泼溅重建方法。GEN3C 区别于前者的地方在于其显式三维缓存提供了更强的几何约束；区别于后者的地方在于其生成式先验能够填补重建方法无法处理的严重遮挡区域——在两视图外推任务上，GEN3C 的 LPIPS 为 0.16，而 MVSplat 为 0.44（Table 2）。

### 与重建基线的边界

GEN3C 与基于重建的方法（如 **Nerfacto**, Tancik et al., SIGGRAPH 2023；**3D-GS**, Kerbl et al., SIGGRAPH 2023）存在清晰的适用边界：

- **重建方法优势区**：当输入视图覆盖充分、相机轨迹偏离较小时，重建方法能够提供精确的几何重建和像素级对齐。
- **GEN3C 优势区**：当相机轨迹大幅偏离原始路径、需要填补大面积未观测区域时，生成式先验的优势凸显。在驾驶场景中，当横向偏移达到 4 米时，GEN3C 的 FID 为 35.33，而 Nerfacto 为 112.40，3D-GS 为 81.26（Table 3）。这一差距的根本原因在于，重建方法在缺失区域只能产生模糊或空洞，而扩散模型能够从数据先验中合成合理的纹理和结构。

### 融合策略的设计选择

GEN3C 在多视图信息融合上的设计选择具有明确的实验支撑。Table 6 和 Figure 10 的消融实验表明，**最大池化融合策略**显著优于显式点云融合（Explicit fusion）和通道拼接（Concat），尤其在输入视图存在深度估计误差或光照不一致时。这是因为最大池化天然具有置换不变性和对异常值的鲁棒性——当某个视点的渲染因深度错误而产生伪影时，其他视点的有效特征可以在池化过程中保留下来。

这一设计的深层含义是：GEN3C 并不要求三维缓存的几何完美精确，而是将扩散模型定位为“几何噪声的校正器”。Figure 14 提供了直观证据——模型能够修正深度投影中的错误（如橙色扶手和灯光的伪影），并在缺失区域生成合理内容。Table 5 进一步证实，对深度估计添加 10%–20% 的中等噪声时，两视图 NVS 的性能下降很小，表明模型对不完美深度具有良好的容忍度。

### 动态场景的延伸与局限

在单目动态新视合成任务上，GEN3C 与 **GCD**（Van Hoorick et al., ECCV 2024）形成直接对比。在 Kubric4D 数据集上，GEN3C 的 FID 为 98.58，显著优于 GCD 的 150.64（Table 4），LPIPS 也从 0.48 降至 0.29。然而，这一优势存在重要限定：当前三维缓存本质上是为静态场景设计的，对于高度动态场景，点云缓存只能捕捉某一时刻的几何快照，动态物体的运动信息并未被显式建模。因此，在动态物体快速移动或形变的场景中，时序一致性仍可能下降。

### 基座可扩展性

GEN3C 的方法具有基座模型可扩展性。Section 5.7 和 Figure 11–12 展示了将底层视频扩散模型从 Stable Video Diffusion 替换为更强大的 Cosmos 模型后，生成质量进一步提升，且能处理更极端的视角变化。这表明“三维缓存渲染 + 视频扩散先验”的框架不依赖于特定的生成模型架构，可以随着基础模型的发展而持续受益。

### 主要局限

1. **深度估计依赖**：方法依赖现成的深度估计器（DAV2），在面对透明、反射或高度纹理缺失的表面时，深度估计错误会直接污染三维缓存，进而影响生成质量。虽然模型具有一定容错能力，但严重错误仍会导致几何不一致。

2. **动态场景的几何缓存失效**：当前训练数据以静态场景为主，三维缓存对动态物体的表示能力有限。在动态物体快速移动或发生非刚性形变时，点云缓存无法有效捕捉其时变几何。

3. **推理效率**：14 帧视频在 A100 上约需 30 秒，且自回归生成可能引入累积误差。这限制了实时应用和极长视频的生成。

4. **输入假设**：多视图融合当前假设输入视图时间同步且相机位姿已知，未充分处理不同步或大范围位姿估计误差的情形。

### 开放问题

1. **语义条件注入**：如何将文本提示等语义条件融入三维缓存渲染流程，以控制生成视频中物体的运动与行为？当前方法主要依赖几何条件，缺乏对场景语义的显式控制。

2. **缓存精度提升**：能否利用更精确的深度图（如 LiDAR 融合）或可微渲染来进一步提高缓存精度？这可能在保持生成能力的同时缩小与重建方法在像素对齐指标上的差距。

3. **非刚性场景推广**：如何将方法推广到可变形场景，并维持三维缓存的一致更新？这需要重新设计缓存的表示和更新机制，可能涉及神经变形场或动态高斯表示。

4. **推理加速**：能否通过蒸馏或高效推理策略显著降低生成延迟，迈向实时新视合成？当前 30 秒/14 帧的速度距离实时应用仍有较大差距。

## 原文 PDF

![[paperPDFs/CVPR_2025/GEN3C_3D_Informed_World_Consistent_Video_Generation_with_Precise_Camera_Control.pdf]]
