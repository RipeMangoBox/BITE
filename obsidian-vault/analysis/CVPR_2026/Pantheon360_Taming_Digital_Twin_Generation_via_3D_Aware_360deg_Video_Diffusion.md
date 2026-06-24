---
title: "Pantheon360: Taming Digital Twin Generation via 3D-Aware 360deg Video Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Pantheon360_Taming_Digital_Twin_Generation_via_3D_Aware_360deg_Video_Diffusion.pdf
project_link: "https://koi953215.github.io/pantheon360_page/"
code_link: null
aliases:
- Pantheon360
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 显式3D Cache（从稀疏360°输入重建的3D点云）作为几何骨架，将复杂3D推理与逼真纹理合成解耦，使扩散模型专注于纹理细化而3D Cache强制全局几何一致性。
primary_logic: 利用3D基础模型从稀疏360°输入重建场景点云，沿用户定义相机轨迹渲染几何视频（V_geo），并将其编码为潜变量，与噪声隐变量拼接后引导扩散模型去噪，从而在保持全景视野的同时实现精确的相机轨迹控制和跨视角形状连贯。
claims:
- 在Web360数据集单视图360°视频生成任务上，Pantheon360在所有指标（FVD、SSIM、PSNR、LPIPS、MET3R）上显著优于ViewCrafter、TrajectoryCrafter、GEN3C等基线。
- 在Habitat数据集稀疏360°视图视频生成任务上，Pantheon360同样取得最优的几何一致性（MET3R）。
- 显式3D Cache框架相比基于动作控制的GenEX，在长时生成中保持稳定的质量与几何精度，不会出现快速退化。
- 双锚点潜变量融合（Dual+Latent Fusion）在插值任务上达到最佳PSNR（28.95）和最小插值误差（7.44 IE），验证了该方法缓解几何不一致的有效性。
---

# Pantheon360: Taming Digital Twin Generation via 3D-Aware 360deg Video Diffusion

> [!tip] 核心洞察
> 利用3D基础模型从稀疏360°输入重建场景点云，沿用户定义相机轨迹渲染几何视频（V_geo），并将其编码为潜变量，与噪声隐变量拼接后引导扩散模型去噪，从而在保持全景视野的同时实现精确的相机轨迹控制和跨视角形状连贯。

| 字段 | 内容 |
|------|------|
| 中文题名 | Pantheon360: 通过3D感知的360°视频扩散生成数字孪生 |
| 英文题名 | Pantheon360: Taming Digital Twin Generation via 3D-Aware 360deg Video Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Chen_Pantheon360_Taming_Digital_Twin_Generation_via_3D-Aware_360deg_Video_Diffusion_CVPR_2026_paper.html) · [Project](https://koi953215.github.io/pantheon360_page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Pantheon360 |
| Dataset | Web360 |

> [!tip] 效果简介
> - Web360 上，FVD↓ 356.151 vs 380.080 (GEN3C) (23.929)；SSIM↑ 0.746 vs 0.583 (GEN3C) (0.163)；PSNR↑ 22.838 vs 20.730 (GEN3C) (2.108)。

## 概述

**问题瓶颈**：现有透视视频生成模型受限于有限视场，在长轨迹或多视角探索时需重复“臆测”不可见区域，导致跨视角不一致与时序漂移。360°视频虽能提供全场景上下文，却面临等距矩形投影（ERP）畸变与精确几何控制的双重难题——如何让生成模型既享有全景视野，又严格服从用户指定的相机轨迹，是数字孪生与沉浸式内容生成的核心瓶颈。

**核心方法**：Pantheon360 提出**显式3D Cache**作为几何骨架，将复杂的3D推理与逼真纹理合成解耦。其关键思路是：从稀疏360°输入出发，利用3D基础模型（如PI3、VGGT）重建场景点云；沿用户定义的相机轨迹 $C_{\text{target}}$ 将该点云渲染为几何视频 $V_{\text{geo}}$，经VAE编码为潜变量支架 $v_{\text{equi}}$ 后与噪声隐变量拼接，同时以首帧的8个透视裁剪CLIP特征作为语义条件，引导微调的SVD视频扩散模型去噪。这一设计使扩散模型专注于纹理细化，而3D Cache强制全局几何一致性。

**方法定位**：Pantheon360 属于**3D感知的360°视频扩散框架**，区别于透视视频生成方法（如 **ViewCrafter** (Yu et al., arXiv 2024)、**TrajectoryCrafter** (Yu et al., ICCV 2025)、**GEN3C** (Ren et al., CVPR 2025)），也不同于仅支持高层动作控制的360°世界模型 **GenEX** (Lu et al., ICLR 2025)。其核心创新在于将显式3D重建与全景扩散生成深度融合，在保持360°全局视野的同时实现精确的相机轨迹跟随。

**主要结果**：在Web360数据集单视图360°视频生成任务上，Pantheon360在所有指标上显著超越基线——FVD降至356.15（GEN3C为380.08），SSIM提升至0.746（GEN3C为0.583），几何一致性指标MET3R降至0.2840（GEN3C为0.3496）。在Habitat稀疏视图生成任务上同样取得最优几何一致性。双锚点潜变量融合在插值任务上达到PSNR 28.95，有效缓解了3D Cache质量不足导致的几何不一致。与GenEX的对比表明，显式3D Cache框架在长时生成中保持稳定质量与几何精度，不会出现快速退化。

## 背景与动机

数字孪生与沉浸式内容创作对可控、一致的3D场景视频生成提出了迫切需求。现有视频扩散模型在透视视频生成上取得了显著进展，但其视场范围（FoV）存在根本性局限：当相机沿长轨迹移动或进行多视角探索时，模型必须反复“臆测”视野外的不可见区域，导致跨视角几何不一致和时序漂移。如图Figure 2所示，透视锚帧在穿越至房间背面时缺乏完整场景上下文，生成结果出现严重伪影；而360°锚帧天然覆盖全场景信息，能够准确生成被遮挡区域。

360°视频格式为上述困境提供了清晰的解决方案。通过从初始时刻即捕获完整场景上下文，360°表示提供了透视模型所缺乏的整体理解。然而，360°视频生成面临双重挑战：一方面，等距矩形投影（ERP）固有的几何畸变使得直接应用透视视频模型变得困难；另一方面，如何在全景视野下实现精确的相机轨迹控制和跨视角形状连贯性，仍是一个开放问题。

现有方法在解决上述问题时各有不足。基于透视视频的生成方法——如**ViewCrafter**（Yu et al., arXiv 2024）、**TrajectoryCrafter**（Yu et al., ICCV 2025）和**GEN3C**（Ren et al., CVPR 2025）——虽然可通过逐视角拼接模拟360°输出，但跨视角一致性难以保证（Figure 4）。基于3D重建的方法如**PanoSplatt3R**（Ren et al., ICCV 2025）在360°新视角合成中表现出几何伪影和结构畸变（Figure 6）。360°世界模型**GenEX**（Lu et al., ICLR 2025）仅支持高层动作控制，缺乏精确轨迹跟随能力，且生成质量随轨迹延长快速退化（Figure 7）。并发工作**CamPVG**主要在合成数据上验证，对真实场景的泛化能力有限。

本文的核心动机在于：若能构建一个显式的3D几何骨架来强制执行全局一致性，便可将复杂的3D推理与逼真纹理合成解耦——让扩散模型专注于纹理细化，而由3D骨架保证几何正确性。这一思路构成了Pantheon360的设计基础。

## 核心创新

Pantheon360的核心创新在于通过**显式3D Cache**将复杂的3D几何推理与逼真纹理合成解耦，从而在保持360°全景视野的同时实现精确的相机轨迹控制。这一设计直接回应了透视视频生成模型的两个根本瓶颈：有限视场导致的跨视角不一致，以及缺乏几何约束造成的时序漂移。

### 关键变更槽位（Changed Slots）

#### 1. 视场范围：从有限透视到完整360°全景

透视视频生成模型（如**ViewCrafter**（Yu et al., arXiv 2024）、**GEN3C**（Ren et al., CVPR 2025））受限于平面透视视场，当相机穿越到场景背面时，必须“臆测”不可见区域的内容，导致严重的跨视角不一致和遮挡区域伪影（Figure 2左）。Pantheon360将生成空间直接提升至**完整360°等距矩形投影（ERP）全景视场**：从$t=0$时刻起，模型便拥有整个场景的完整上下文，无需在生成过程中逐步推断未观测区域。这一变更从信息源头上消除了跨视角不一致的结构性诱因——同一扇门从不同角度观察时始终保持一致的几何结构，而GEN3C的透视生成则产生几何不一致的结果（Figure 2右）。

#### 2. 几何条件注入：从隐式射线嵌入到显式3D支架

这是Pantheon360最核心的机制创新。透视方法通常依赖Plücker射线嵌入等隐式几何信号，这些信号仅编码相机姿态信息，缺乏对场景几何的显式建模。Pantheon360引入**显式3D Cache**——从稀疏360°输入重建的3D点云——作为几何骨架，并沿用户定义的相机轨迹$C_{\text{target}}$将其渲染为等距矩形投影格式的几何视频$V_{\text{geo}}$。该几何视频经VAE编码器$\mathcal{E}$编码为潜变量支架$v_{\text{equi}} = \mathcal{E}(V_{\text{geo}})$，随后与噪声隐变量在通道维度上拼接，作为扩散U-Net的条件输入。这一设计的因果机制在于：**3D Cache强制场景的全局几何一致性，扩散模型仅需专注于纹理细化**，无需同时推理3D结构。消融证据表明，当3D Cache质量不足时，双锚点潜变量融合可部分缓解几何不一致（Table 3），但整体框架的优越性仍高度依赖几何支架的质量。

#### 3. 语义条件注入：从单张透视CLIP特征到多视角全景特征

基线方法通常从单张透视图像提取CLIP特征作为语义条件。Pantheon360针对360°输入的特殊性，从首张360°帧中**裁剪8张透视视图**（间隔45°偏航），分别提取CLIP特征后拼接为语义条件$c_{\text{img}}$，通过交叉注意力注入去噪U-Net。这一设计确保语义条件覆盖完整的全景内容，避免单视角特征的信息盲区。

#### 4. 训练数据模态：从透视视频到360°真实视频

Pantheon360的训练数据从带已知位姿的透视视频数据集切换至**360°真实视频数据集360-1M**，并配合在线生成的3D Cache与轨迹真值标注。这一变更不仅提供了全景训练信号，还通过自动标注管线（利用ViPE处理完整视频$Y_{\text{GT}}$）实现了可扩展的数据生产，无需人工标注相机轨迹。

### 与最相关工作的本质差异

与同为360°世界模型的**GenEX**（Lu et al., ICLR 2025）相比，Pantheon360的关键差异在于控制粒度：GenEX仅支持高层动作控制（如“前进”“左转”），缺乏精确的轨迹跟随能力，且生成质量随帧数增加快速退化（Figure 7）；Pantheon360通过显式3D Cache实现了对任意用户定义相机轨迹的精确跟随，并在长时生成中保持稳定的质量与几何精度。与并发工作**CamPVG**相比，Pantheon360在真实场景数据上进行了全面验证，而非仅限于合成数据。

## 整体框架

Pantheon360 的整体设计围绕一个核心解耦思路展开：将复杂的 3D 几何推理与逼真的纹理合成分离，使视频扩散模型专注于纹理细化，而由显式 3D Cache 强制全局几何一致性。该框架基于预训练的潜变量视频扩散模型 SVD (Blattmann et al., 2023) 构建，但引入了一套由显式 3D 场景表征引导的鲁棒条件注入机制。

### Pipeline 总览

整个生成流程可分为五个紧密衔接的模块，如 Figure 3 所示：

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/003_Figure_3.jpg]]
*Figure 3: Pantheon360 Pipeline. Given sparse 360° input frames, we first crop them into perspective views and reconstruct a 3D point cloud cache using foundation models*

1. **3D Cache 重建** — 将稀疏的 360° 输入帧裁剪为多个透视视图，送入 3D 基础模型（如 **PI3** 或 **VGGT**）重建场景的 3D 点云，作为几何骨架。
2. **几何支架渲染** — 沿用户定义的目标相机轨迹 $C_{\text{target}}$，将 3D 点云渲染为等距矩形投影（ERP）格式的几何视频 $V_{\text{geo}}$。
3. **几何潜变量编码** — 将 $V_{\text{geo}}$ 通过 VAE 编码器 $\mathcal{E}$ 编码为潜变量支架 $v_{\text{equi}} = \mathcal{E}(V_{\text{geo}})$，在每一扩散步与噪声隐变量拼接。
4. **语义特征提取** — 从首张 360° 帧 $I_0$ 裁剪 8 张透视视图（偏航角间隔 45°），经 CLIP 提取器 $F$ 编码后拼接为语义条件 $c_{\text{img}}$，通过交叉注意力注入去噪 U-Net。
5. **双条件视频扩散去噪** — 微调后的 SVD U-Net $f_\theta$ 在几何潜变量（拼接）和语义特征（交叉注意力）双条件下迭代去噪，生成时序一致的逼真 360° 视频 $Y_{\text{equi}}$。

### 输入输出流

- **输入**：稀疏或单张 360° 等距矩形投影图像，以及用户定义的相机轨迹 $C_{\text{target}}$。
- **中间表征**：3D 点云 Cache、几何视频 $V_{\text{geo}} \in \mathbb{R}^{T \times 3 \times H' \times W'}$、几何潜变量 $v_{\text{equi}}$、语义特征 $c_{\text{img}}$。
- **输出**：时序一致的 360° 等距矩形视频 $Y_{\text{equi}} \in \mathbb{R}^{T \times 3 \times H' \times W'}$。

### 训练与推理流程

训练时，框架利用 360-1M 数据集进行在线数据标注：通过 ViPE 处理完整视频 $Y_{\text{GT}}$ 自动标注 3D Cache 和真值轨迹。扩散模型以标准去噪损失训练：

$$L = \mathbb{E}_{y_{\text{equi}}, v_{\text{equi}}, c_{\text{img}}, t, \epsilon} [\lambda(t) ||\epsilon - f_\theta(y_{\text{equi},t}, t, v_{\text{equi}}, c_{\text{img}})||_2^2]$$

推理时，对于单视图输入，先通过 PI3 构建 3D Cache，沿目标轨迹渲染几何支架后送入扩散模型生成视频。对于稀疏多视图输入，则对每个视图预测深度后融合为统一 3D Cache，其余流程一致。在插值任务中，框架进一步采用双锚点潜变量融合机制，融合起始与结束锚帧的潜变量以平滑过渡并缓解因 3D Cache 质量不足导致的几何不一致。

### 补充图表

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/001_Figure_1.jpg]]
*Figure 1: Pantheon360: Controllable 360° Video Generation. Given sparse or single 360° input images, Pantheon360 generates temporally consistent 360° videos along user-defined camera trajectories with precise geometric control. Top: From sparse views or a single view, our method synthesizes smooth videos following diverse camera trajectories across varied scenes, demonstrating flexible trajectory control from minimal input. Bottom: Our framework enables practical applications, including video stabilization (left, transforming shaky footage into smooth output) and motion interpolation (right, generating smooth transitions between distant anchor frames marked in red)*

## 核心模块与公式推导

### 问题形式化

给定稀疏360°输入帧，Pantheon360的目标是沿用户定义的相机轨迹 $C_{\text{target}}$ 生成时序一致的360°等距矩形投影（ERP）视频 $Y_{\text{equi}} \in \mathbb{R}^{T \times 3 \times H' \times W'}$。核心瓶颈在于：透视视频生成模型视场受限，长轨迹探索时需重复臆测不可见区域，导致跨视角不一致和时序漂移；而360°视频虽提供全场景上下文，却面临ERP投影畸变与精确几何控制的双重挑战。

Pantheon360的核心洞察是：利用3D基础模型从稀疏360°输入重建场景点云作为显式3D Cache，将复杂的3D推理与逼真纹理合成解耦——3D Cache强制全局几何一致性，扩散模型仅专注于纹理细化。

### 核心模块

**模块一：3D Cache重建**

从稀疏360°输入帧出发，将每帧裁剪为多个透视视图，送入3D重建基础模型（如PI3或VGGT）生成场景的3D点云。该点云作为显式几何骨架，建模场景的球面几何结构，为后续所有相机轨迹提供统一的几何参照。

**模块二：几何支架渲染**

将重建的3D点云沿目标相机轨迹 $C_{\text{target}}$ 渲染为ERP格式的几何视频 $V_{\text{geo}} \in \mathbb{R}^{T \times 3 \times H' \times W'}$。该视频仅包含几何信息，作为强3D一致性支架，为扩散模型提供精确的空间引导。

**模块三：几何潜变量编码**

几何视频 $V_{\text{geo}}$ 经VAE编码器 $\mathcal{E}$ 编码为潜变量支架：

$$v_{\text{equi}} = \mathcal{E}(V_{\text{geo}})$$

该潜变量在每一步扩散去噪中与噪声隐变量沿通道维度拼接，构成几何条件注入的核心通路。

**模块四：语义特征提取**

从首张360°帧 $I_0$ 裁剪8张透视视图（偏航角间隔45°），分别通过CLIP特征提取器 $F$，将所得特征拼接为语义条件 $c_{\text{img}}$，通过交叉注意力注入去噪U-Net，提供场景语义引导。

**模块五：微调视频扩散U-Net**

生成器 $G$ 为基于SVD预训练权重的微调U-Net $f_\theta$，接受双流条件：
- **几何潜变量**（拼接注入）：$v_{\text{equi}}$ 与噪声隐变量拼接，提供显式3D几何约束；
- **语义特征**（交叉注意力注入）：$c_{\text{img}}$ 提供场景外观与语义先验。

**模块六：双锚点潜变量融合**

针对运动插值任务，采用Time Reversal Fusion的潜变量融合技术，在去噪过程中融合起始帧与结束帧的潜变量信息，缓解因3D Cache质量不足导致的几何不一致，确保长距离插值的平滑过渡。

### 关键公式

**扩散训练损失**

模型以标准扩散去噪目标训练，条件为几何潜变量 $v_{\text{equi}}$ 和语义特征 $c_{\text{img}}$：

$$L = \mathbb{E}_{y_{\text{equi}}, v_{\text{equi}}, c_{\text{img}}, t, \epsilon} \left[\lambda(t) \|\epsilon - f_\theta(y_{\text{equi},t}, t, v_{\text{equi}}, c_{\text{img}})\|_2^2\right]$$

其中 $y_{\text{equi},t}$ 为时刻 $t$ 的噪声隐变量，$\epsilon$ 为添加的高斯噪声，$\lambda(t)$ 为时间步权重，$f_\theta$ 为去噪U-Net。该损失驱动模型在几何支架和语义特征的双重约束下学习从噪声中恢复逼真360°视频帧。

**视频稳定中的平滑轨迹**

在视频稳定应用中，将原始抖动轨迹处理为平滑轨迹 $C_{\text{smooth}}$，再沿该轨迹渲染几何支架并生成稳定视频。该过程无需额外训练，仅通过改变渲染轨迹即可实现。

### 方法谱系与知识库定位

Pantheon360处于**360°视频生成**与**3D感知视频扩散**的交叉地带。相较于透视视频生成方法（如**ViewCrafter**（Yu et al., arXiv 2024）、**TrajectoryCrafter**（Yu et al., ICCV 2025）、**GEN3C**（Ren et al., CVPR 2025）），其关键区别在于以完整360° ERP视场替代有限透视视场，从根本上消除跨视角臆测需求。相较于360°世界模型**GenEX**（Lu et al., ICLR 2025）的高层动作控制，Pantheon360通过显式3D Cache实现了精确的相机轨迹跟随。与并发工作**CamPVG**相比，Pantheon360在真实场景数据（360-1M）上验证，而非局限于合成数据。与360°重建方法**PanoSplatt3R**（Ren et al., ICCV 2025）相比，Pantheon360以生成式扩散框架实现新视角合成，在几何准确性和结构清洁度上展现优势。

### 已知局限与开放问题

**局限**：
- 生成质量受初始3D Cache重建质量制约；稀疏输入下点云几何可能与目标帧不一致，导致视频跳跃，双锚点融合仅能部分缓解。
- 尚未支持物体级别动态的显式控制。
- 对极端室内、高度动态或域外场景的泛化能力未经充分评估。
- ERP投影固有畸变可能在边缘区域产生伪影。

**开放问题**：
- 如何并入显式运动表征以实现物体级动态控制？
- 更强3D基础模型能否提升极端稀疏输入下3D Cache的鲁棒性？
- 框架能否扩展至多模态条件（文本、语义地图）？
- 快速运动或大幅度视差场景下，当前几何支架是否足以保持所有区域的逼真度？

### 补充图表

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/002_Figure_2.jpg]]
*Figure 2: Motivation for Using 360° Images for Generation. Left: When traversing to the back of the room, 360° anchor frames provide complete scene context, enabling accurate generation of occluded regions. In contrast, perspective anchor frames have a limited field-of-view and must hallucinate unseen areas, leading to significant artifacts. Right: Generating 360° outputs in a single pass ensures global coherence and cross-view consistency. Our method maintains consistent object structures (red boxes highlight the same door/cabinet viewed from different angles), while GEN3C’s perspective-based generation produces geometrically inconsistent results across views*

## 实验与分析

### 核心实验设置

Pantheon360 在两个主流基准上验证了其 360° 视频生成能力：**Web360**（真实场景单视图生成）和 **Habitat**（稀疏多视图生成）。评估指标覆盖视频质量（FVD）、像素保真度（SSIM、PSNR）、感知相似度（LPIPS）以及跨视角几何一致性（MET3R）。基线方法包括三类代表性工作：透视视频生成模型 **ViewCrafter**（Yu et al., arXiv 2024）、**TrajectoryCrafter**（Yu et al., ICCV 2025）和 **GEN3C**（Ren et al., CVPR 2025），均适配为 360° 生成；360° 世界模型 **GenEX**（Lu et al., ICLR 2025）；以及 360° 重建方法 **PanoSplatt3R**（Ren et al., ICCV 2025）。

### 单视图 360° 视频生成（Web360）

Table 1 展示了在 Web360 数据集上单张 360° 视图到视频的生成结果。Pantheon360 在所有指标上均显著优于所有基线方法。与最强基线 GEN3C 相比，FVD 从 380.080 降至 356.151（降低 6.3%），SSIM 从 0.583 提升至 0.746（提升 28.0%），PSNR 从 20.730 提升至 22.838（提升 2.1 dB），LPIPS 从 0.145 降至 0.065（降低 55.2%），MET3R 从 0.3496 降至 0.2840（降低 18.8%）。这些提升的核心驱动力在于显式 3D Cache 提供的几何支架：透视基线在生成过程中需要反复“臆测”视场外的不可见区域，导致跨视角不一致和时序漂移；而 Pantheon360 通过 360° 全景输入和 3D 点云重建，使扩散模型始终拥有完整的场景几何上下文，从而在纹理合成阶段无需承担几何推理负担。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on single 360° view-to-video generation on Web360 dataset. ↓ indicates lower is better, ↑ indicates higher is better*

Figure 4 的可视化对比进一步印证了这一结论。透视基线（ViewCrafter、TrajectoryCrafter、GEN3C）在从不同视角渲染时出现严重的跨视角不一致，尤其是当初始帧捕捉到近距离几何结构时，有限的视场无法提供足够的空间上下文，导致生成结果在不同视角下结构错位。相比之下，Pantheon360 通过完整的全景覆盖，在所有视角下均保持全局一致的生成质量。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/005_Figure_4.jpg]]
*Figure 4: Visualization Results on the Web360 [61] and Habitat [46] datasets. Our method (Ours) generates temporally consistent videos with coherent cross-view geometry across diverse camera trajectories. In contrast, perspective-based baselines (ViewCrafter [86], TrajectoryCrafter [85], GEN3C [52]) exhibit severe cross-view inconsistencies when rendered from different viewing angles (Left vs. Right), revealing their limited ability to maintain geometric coherence across viewpoints. This inconsistency is particularly pronounced when the initial frame captures geometry at close range, where the limited field-of-view fails to provide sufficient spatial context for consistent generation. Our 360° approa...*

### 稀疏多视图 360° 视频生成（Habitat）

Table 2 展示了在 Habitat 数据集上稀疏 360° 视图到视频的生成结果。Pantheon360 在几何一致性指标 MET3R 上取得最优成绩，验证了 3D Cache 框架在稀疏输入条件下的鲁棒性。值得注意的是，Habitat 场景包含更多结构化室内环境和复杂遮挡关系，稀疏输入进一步加剧了几何推理的难度——此时 3D Cache 从有限视图中重建的点云可能不够完整，但 Pantheon360 仍然在跨视角一致性上优于所有基线，说明几何支架机制即使在点云质量不完美的情况下，仍能提供比纯隐式方法更强的几何约束。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison on sparse 360° views-to-video generation on Habitat [46] dataset. ↓ indicates lower is better, ↑ indicates higher is better*

### 与 360° 世界模型和重建方法的对比

Figure 7 对比了 Pantheon360 与 GenEX 的长时生成质量。GenEX 作为 360° 世界模型，仅支持高层动作控制（如“前进”“左转”），缺乏精确的相机轨迹跟随能力。随着生成帧数增加，GenEX 的质量快速退化，几何不一致性累积；而 Pantheon360 凭借显式 3D Cache 沿精确轨迹渲染几何支架，在整个长序列中保持稳定的质量和几何精度。这一对比直接验证了“显式几何解耦”的核心设计价值。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/007_Figure_7.jpg]]
*Figure 7: Comparison to GenEX [43]. Our method maintains consistent quality throughout the trajectory while GenEX’s quality degrades rapidly with increasing geometric inconsistencies*

Figure 6 和 Figure 8 分别对比了 PanoSplatt3R 和 GEN3C 在新视角合成任务上的表现。PanoSplatt3R 作为专门的 360° 重建方法，在插值结果中出现可见伪影和几何畸变；GEN3C 在 Google Maps Street View 场景中产生鬼影伪影、几何畸变和跨视角不一致。Pantheon360 生成的视角具有清晰的几何结构和准确的空间关系，表明扩散模型的纹理细化能力与 3D Cache 的几何约束形成了有效的互补。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/009_Figure_6.jpg]]
*Figure 6: Comparison to PanoSplatt3R [51]. Our method produces geometrically accurate interpolations with clean structure, while PanoSplatt3R exhibits visible artifacts and geometric distortions*

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/010_Figure_8.jpg]]
*Figure 8: Novel View Synthesis on Google Maps Street View. Our method produces geometrically accurate renderings across different viewing angles with consistent structures. GEN3C [52] suffers from ghosting artifacts, geometric distortions, and inter-view inconsistencies*

Figure 9 从 3D 重建质量角度提供了间接证据：使用 π³ 从生成视频重建 3D 点云时，Pantheon360 生成的点云密集且结构连贯，而 GEN3C 生成的点云稀疏且碎片化。这说明 Pantheon360 生成的视频不仅在视觉上逼真，其底层 3D 结构也更为一致，进一步验证了显式几何支架对生成过程的正向约束作用。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/011_Figure_9.jpg]]
*Figure 9: 3D Point Cloud Reconstruction Quality. We reconstruct 3D point clouds from generated videos using π3 [72]. Our method yields dense, structurally coherent reconstructions (right), while GEN3C [52] produces sparse, fragmented results (left), demonstrating our superior 3D consistency*

### 消融实验：双锚点潜变量融合

Table 3 报告了插值任务上的消融实验，验证了双锚点潜变量融合（Dual+Latent Fusion）的有效性。实验对比了四种变体：

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/012_Table_3.jpg]]
*Table 3: Ablation study on latent fusion for interpolation. STWE refers to Short-Term Warping Error, and IE refers to Interpolation Error. ↓ indicates lower is better, ↑ indicates higher is better*

- **Single**：仅以起始帧为条件，无融合
- **Single+Latent Fusion**：起始帧条件 + 潜变量融合
- **Dual**：以起始帧和结束帧为条件，无融合
- **Dual+Latent Fusion**（完整方法）：双锚帧条件 + 潜变量融合

完整方法在 PSNR 上达到 28.948，插值误差（IE）降至 7.437，显著优于所有消融变体。这一结果揭示了两个关键发现：

1. **双锚点条件的必要性**：仅使用起始帧（Single 变体）在长距离插值时缺乏对目标帧的约束，导致生成结果偏离目标。加入结束帧条件（Dual 变体）提供了目标信息，但仍无法平滑过渡。
2. **潜变量融合的平滑作用**：在双锚点基础上引入潜变量融合（Dual+Latent Fusion），通过混合起始帧和结束帧的潜变量表示，有效缓解了因 3D Cache 质量不足导致的几何不一致，确保长时间插值的平滑过渡。这在实际应用中尤为重要——当输入视图稀疏时，3D Cache 的重建质量可能不足以精确匹配所有中间帧的几何结构，潜变量融合在此充当了“软约束”的角色，在几何支架和语义条件之间取得平衡。

### 应用验证

Figure 5 展示了在 Google Street View 上的视频合成应用。Pantheon360 从稀疏的街景图像生成长距离的连贯 360° 导航视频，验证了方法在真实世界大规模场景中的实用性。视频稳定应用（Figure 1 底部左侧）进一步展示了框架对任意相机轨迹的精确控制能力：通过将抖动轨迹处理为平滑轨迹 $C_{\text{smooth}}$，Pantheon360 能够重新渲染出稳定的 360° 视频。

![[assets/figures/papers/paper_list_l2560_https_openaccess_thecvf_com_content_CVPR2026_html_Chen_Pantheon360_Tamin/figures/006_Figure_5.jpg]]
*Figure 5: Application. Video Synthesis from Google Street View. Our method generates consistent 360° videos from sparse Google Street View imagery, enabling smooth navigation across extended trajectories*

### 失败模式与局限性

尽管 Pantheon360 在整体性能上表现优异，但分析揭示了以下失败模式：

1. **3D Cache 质量依赖**：生成质量的上限受初始 3D Cache 重建质量制约。当输入视图极度稀疏或场景包含细薄结构时，点云几何可能与目标帧的真实几何存在偏差，导致视频出现跳跃或不连续。双锚点潜变量融合仅能部分缓解此问题，无法完全消除底层几何错误。
2. **边缘区域畸变**：360° 等距矩形投影（ERP）固有的畸变在图像边缘区域（对应球面极点附近）仍可能产生伪影，尤其是在快速旋转轨迹下。
3. **动态场景局限**：当前框架专注于全局场景一致性与相机轨迹控制，尚未支持对场景中物体级别动态的显式控制。对于包含移动物体的场景，生成结果可能无法准确反映物体运动。
4. **域外泛化未经充分验证**：训练数据依赖 360‑1M 数据集，对极端室内环境、高度动态场景或域外场景的泛化能力需要进一步评估。

这些失败模式直接指向了方法的核心权衡：显式 3D Cache 提供了强大的几何约束，但其质量瓶颈也成为了系统性能的上限。未来的改进方向包括结合更强的 3D 基础模型以提升稀疏输入下的重建鲁棒性，以及引入显式运动表征以实现物体级别的动态控制。

## 方法谱系与知识库定位

### 1. 问题定位：从透视生成到全景生成的范式迁移

当前主流的视频生成模型——包括 **SVD** (Blattmann et al., 2023)、**ViewCrafter** (Yu et al., arXiv 2024)、**TrajectoryCrafter** (Yu et al., ICCV 2025) 及 **GEN3C** (Ren et al., CVPR 2025)——均构建于透视投影之上。这类模型的核心瓶颈在于视场受限：当相机执行长轨迹或多视角探索时，模型需反复“臆测”不可见区域，导致跨视角不一致与累积性时序漂移。Figure 2 的动机实验清晰地揭示了这一现象：使用透视锚帧生成房间背面时，模型因缺乏全局上下文而产生严重伪影；而360°锚帧凭借完整的全景覆盖，能够准确生成遮挡区域。

Pantheon360 的范式迁移在于将生成空间从有限透视视场扩展至完整的360°等距矩形投影（ERP）全景视场。这一选择并非简单的分辨率缩放，而是从根本上改变了条件信号的语义密度——从局部窗口的猜测变为全局上下文的推断。然而，360°格式引入的新挑战是 ERP 投影固有的几何畸变与精确轨迹控制的困难。

### 2. 与360°世界模型的关系：GenEX 与 CamPVG

在360°视频生成这一细分方向上，最具直接可比性的工作是 **GenEX** (Lu et al., ICLR 2025) 和 **CamPVG**（并发工作）。

**GenEX** 作为一个360°世界模型，仅支持高层动作控制（如“向前走”），缺乏对精确相机轨迹的跟随能力。Figure 7 的对比显示，GenEX 在长时生成中质量快速退化，几何不一致性随帧数增加而累积。Pantheon360 通过显式3D Cache 框架从根本上规避了这一问题：3D Cache 作为几何骨架强制全局一致性，扩散模型仅负责纹理细化，从而在长轨迹上保持稳定的生成质量。

**CamPVG** 是并发提出的360°视频生成方法，但其验证主要集中在合成数据上，未充分处理真实场景的复杂几何与纹理分布。Pantheon360 在 Web360 和 Habitat 两个真实/仿真数据集上均进行了系统验证，且支持稀疏输入（单视图或多视图）的灵活配置。

### 3. 与3D重建/新视角合成方法的关系：PanoSplatt3R

**PanoSplatt3R** (Ren et al., ICCV 2025) 代表了基于重建的360°新视角合成路线。Figure 6 的对比表明，PanoSplatt3R 在插值任务中会产生可见伪影和几何畸变，而 Pantheon360 生成的插值结果具有更清晰的结构。这一差异的深层原因在于：重建方法依赖显式的几何优化（如高斯泼溅），在稀疏输入或大基线场景下易陷入局部最优；而扩散模型通过大规模数据先验隐式地补全了几何不确定性区域的合理纹理。

### 4. 方法架构的谱系定位

从架构演进的角度，Pantheon360 可置于以下知识谱系中：

- **基座模型层**：基于预训练的潜视频扩散模型 **SVD** (Blattmann et al., 2023) 进行微调，继承了其在时序建模和纹理生成上的能力。
- **几何条件注入层**：区别于透视视频模型中常用的 Plücker 射线嵌入（如 ViewCrafter、TrajectoryCrafter），Pantheon360 创新性地引入显式3D Cache 渲染的全景几何视频 $V_{\text{geo}}$，经 VAE 编码为潜变量支架 $v_{\text{equi}} = \mathcal{E}(V_{\text{geo}})$ 后与噪声隐变量拼接。这一设计将复杂的3D推理与逼真纹理合成解耦，是方法的核心因果杠杆。
- **语义条件注入层**：从首张360°帧的8个透视裁剪（间隔45°偏航）提取并拼接 CLIP 特征，相比单张透视图像的 CLIP 条件，提供了更丰富的全景语义上下文。
- **训练数据层**：基于 **360-1M** 数据集，配合在线生成的3D Cache 与轨迹真值标注（通过 ViPE 自动标注），构建了大规模全景视频训练管线。

### 5. 适用边界与局限

Pantheon360 的生成质量存在一个根本性的上游依赖：初始3D Cache 的重建质量。当输入视图极度稀疏时，3D基础模型（PI3/VGGT）重建的点云几何可能与目标帧不一致，导致视频出现跳跃或不连续。双锚点潜变量融合（受 Time Reversal Fusion 启发）在插值任务中部分缓解了这一问题（Table 3 显示 PSNR 达 28.95，插值误差 IE 为 7.44），但无法从根本上解决几何支架本身的质量缺陷。

其他已知局限包括：
- 尚未支持对场景中物体级别动态的显式控制——当前框架侧重于全局场景一致性与相机轨迹控制。
- 训练数据依赖 360-1M 数据集，对极端室内、高度动态或域外场景的泛化能力未经充分评估。
- 360° ERP 投影固有的畸变仍可能在边缘区域产生伪影。

### 6. 开放问题

1. **物体级动态控制**：能否并入显式运动表征（如场景流、物体轨迹）以实现对独立物体的精细化运动控制？
2. **3D Cache 鲁棒性**：结合更强的3D基础模型（如更大规模的 DUSt3R 变体或多视图立体匹配），能否提升极端稀疏输入下的几何支架质量？
3. **多模态条件扩展**：该框架能否扩展到文本描述、语义地图等多模态条件，实现更丰富的可控生成？
4. **大视差场景保真度**：对于快速运动或大幅度视差场景，当前的几何支架是否足以保持所有区域（尤其是 ERP 投影边缘）的逼真度？是否需要自适应分辨率或局部细化机制？

## 原文 PDF

![[paperPDFs/CVPR_2026/Pantheon360_Taming_Digital_Twin_Generation_via_3D_Aware_360deg_Video_Diffusion.pdf]]