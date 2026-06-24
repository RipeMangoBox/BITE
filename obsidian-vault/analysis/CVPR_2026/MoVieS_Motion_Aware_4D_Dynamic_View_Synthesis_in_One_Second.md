---
title: "MoVieS: Motion-Aware 4D Dynamic View Synthesis in One Second"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoVieS_Motion_Aware_4D_Dynamic_View_Synthesis_in_One_Second.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Lin_MoVieS_Motion-Aware_4D_Dynamic_View_Synthesis_in_One_Second_CVPR_2026_paper.html
project_link: https://chenguolin.github.io/projects/MoVieS
code_link: null
aliases:
- MoVieS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 对每个像素对齐的高斯原语显式施加时间条件的运动监督（点级误差+内部距离分布保持），并将运动与视图合成、深度估计联合优化，驱动多任务一致性。
primary_logic: 将动态场景解构为静态高斯原语和可学习的变形场，通过共享 Transformer 特征骨干和时间自适应运动头，在单模型内统一了外观重建、几何预测和3D运动跟踪。
claims:
- 在动态视图合成基准 DyCheck 上，MoVieS 仅需 0.93 秒即达到 18.46 mPSNR，速度比此前方法快数个数量级，且不使用动态掩码。
- 消融实验证明，联合训练运动估计与新视图合成（Ours）显著优于单独训练运动或 NVS，在 DyCheck 上 mPSNR 均有大幅提升。
- 运动损失中同时使用点对点 L1 损失和分布损失能最有效地提升 3D 点跟踪精度（Aria 数字孪生 EPE 0.2153，δ0.05 达 52.05%）。
- RealEstate10K (static) 上 PSNR = 27.60
---

# MoVieS: Motion-Aware 4D Dynamic View Synthesis in One Second

> [!tip] 核心洞察
> 将动态场景解构为静态高斯原语和可学习的变形场，通过共享 Transformer 特征骨干和时间自适应运动头，在单模型内统一了外观重建、几何预测和3D运动跟踪。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoVieS：运动感知的一秒级4D动态视图合成 |
| 英文题名 | MoVieS: Motion-Aware 4D Dynamic View Synthesis in One Second |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lin_MoVieS_Motion-Aware_4D_Dynamic_View_Synthesis_in_One_Second_CVPR_2026_paper.html) · [Project](https://chenguolin.github.io/projects/MoVieS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoVieS |
| Dataset | RealEstate10K, DyCheck, Aria Digital Twin, Inference Speed |

> [!tip] 效果简介
> - RealEstate10K (static) 上，PSNR 27.60。
> - DyCheck (dynamic) 上，mPSNR 18.46。
> - Aria Digital Twin 上，EPE_3D 0.2153。

## 概述

动态场景的快速、高质量新视图合成是计算机视觉中的核心挑战。现有前馈重建方法局限于静态场景，而动态场景方法依赖昂贵的逐场景优化，难以实现实时4D重建。其根本瓶颈在于：外观、几何和运动被分离式任务建模，缺乏统一的表征与学习框架，导致无法在单次前向推理中同时获得高质量渲染和精确运动跟踪。

MoVieS 针对这一瓶颈提出了**动态 Splatter Pixel 表征**：将动态场景解构为静态像素对齐的高斯原语，并显式学习每个原语的时间相关变形场。通过共享 Transformer 特征骨干和时间自适应运动头，MoVieS 在单一模型内统一了外观重建、几何预测和3D运动跟踪。其核心洞察在于：对每个像素对齐的高斯原语施加时间条件的运动监督——同时约束点级位移误差和内部距离分布保持——并将运动估计与视图合成、深度估计联合优化，从而驱动多任务一致性。

在实验验证中，MoVieS 展现出显著的性能优势：
- **动态视图合成**：在 DyCheck 基准上仅需 **0.93 秒**即达到 **18.46 mPSNR**，速度比此前方法快数个数量级，且不使用任何动态掩码（Table 2）。
- **3D 点跟踪**：在 Aria 数字孪生数据集上，3D 跟踪终点误差降至 **0.2153**，准确率 δ⁰.⁰⁵ 达到 **52.05%**（Table 3）。
- **多任务协同**：消融实验证实，联合训练运动估计与新视图合成显著优于单独训练任一任务，验证了多任务协同的关键作用（Table 6）。

## 背景与动机

### 动态视图合成：从逐场景优化到前馈重建

从稀疏或单目视频中重建可自由导航的 4D 动态场景，是计算机视觉和图形学的核心挑战，直接支撑着增强现实、自动驾驶仿真和沉浸式媒体等应用。传统方法依赖逐场景优化——对每个场景单独运行基于 NeRF 或 3D Gaussian Splatting 的优化管线，虽然能够产生高质量结果，但通常需要数分钟到数小时的训练时间，难以满足实时交互需求。

近年来，前馈重建（feed-forward reconstruction）范式在静态场景上取得了突破。以 **DepthSplat**（Xu et al., CVPR 2025）和 **GS-LRM**（Zhang et al., ECCV 2024）为代表的方法，通过大规模预训练实现了“输入图像、直接输出 3D 表示”的推理流程，将场景重建压缩到秒级甚至亚秒级。然而，这些方法的核心瓶颈在于：**它们仅适用于静态场景，无法建模物体运动、形变和外观随时间的变化**。一旦场景中出现动态内容，前馈方法的输出质量急剧下降，因为它们缺乏对时间维度的任何显式建模。

### 分离式任务建模的困境

在动态场景理解领域，视图合成、深度估计和运动跟踪长期被视为相互独立的任务，各自发展出专门的模型体系：

- **视图合成**：专注于从已知视角生成新视角的逼真图像，典型方法如 **STORM**（Yang et al., ICLR 2025）在户外驾驶场景中实现了多视图时空重建，但其运动建模与外观渲染耦合紧密，难以泛化到通用动态场景。
- **深度估计**：以 **VGGT**（Wang et al., CVPR 2025）为代表的几何基础模型，在静态场景中提供了可靠的 3D 空间定位，但其预训练权重中不包含运动信息，无法直接处理动态内容。
- **运动跟踪**：3D 点跟踪方法通常依赖独立的 2D 光流或轨迹模型，再通过深度估计将 2D 跟踪反投到 3D 空间，这种两阶段流程导致误差累积，且缺乏与外观重建的协同优化。

这种分离式建模带来了两个根本性问题：**第一，不同任务之间缺乏信息共享和相互约束**，例如运动估计的误差无法通过视图合成损失得到纠正；**第二，每个任务都需要独立的训练数据和优化目标，难以在统一框架下实现高效的端到端推理**。已有的一些前馈动态视图合成尝试（如 **BTimer**、**NutWorld**）虽然开始探索时间建模，但要么速度仍然较慢，要么在动态场景的渲染质量和运动精度上存在明显不足。

### MoVieS 的核心动机

本文的核心洞察在于：**动态场景可以被解构为静态高斯原语和可学习的变形场**，通过共享的特征骨干和时间自适应运动头，在单一模型内统一外观重建、几何预测和 3D 运动跟踪。这一设计使得三个任务能够相互增强——运动估计为视图合成提供时序一致性约束，视图合成损失反过来监督运动学习的质量，而深度估计则为两者提供稳定的 3D 空间参考。

在此框架下，MoVieS 旨在回答一个关键问题：**能否在保持前馈推理速度（亚秒级）的前提下，实现动态场景的高质量视图合成和精确的 3D 运动跟踪？** 为此，MoVieS 对每个像素对齐的高斯原语显式施加时间条件的运动监督，并通过联合优化驱动多任务一致性，从而在动态视图合成基准上以 0.93 秒的单场景推理时间达到 18.46 mPSNR，速度比此前方法快数个数量级。

## 核心创新

MoVieS 的核心创新在于将动态场景重建从“逐场景优化”的范式转变为一秒级前馈推理，其关键突破并非单一模块的改进，而是对场景表示、时间建模机制和训练目标的系统性重构。以下从四个 changed slots 展开分析。

### 1. 场景表示：从静态高斯原语到动态 Splatter Pixel

传统前馈视图合成方法（如 **DepthSplat** (Xu et al., CVPR 2025)、**GS-LRM** (Zhang et al., ECCV 2024)）采用静态像素对齐的高斯原语（Splatter Pixel）表示场景，每个像素对应的高斯椭球体在时间上保持不变，因此只能处理静态场景。MoVieS 将其扩展为**动态 Splatter Pixel**：每个原语不仅包含静态的 3D 位置 $\mathbf{x}$ 和外观属性 $\mathbf{a}$，还关联一个时间相关的变形场 $\mathbf{m}(t) := \{\Delta \mathbf{x}(t), \Delta \mathbf{a}(t)\}$，其变形过程为：

$$\mathbf{x} \gets \mathbf{x} + \Delta \mathbf{x}(t), \quad \mathbf{a} \gets \mathbf{a} + \Delta \mathbf{a}(t)$$

这一设计将动态场景解构为“静态基元 + 可学习形变”的组合，使得同一套高斯原语可以在任意查询时刻 $t$ 被驱动到对应状态，从而统一了静态场景和动态场景的表示。在静态输入下，预测的运动量自然收敛至零（小于 $10^{-3}$），保证了表示的向后兼容性。

### 2. 预测头设计：解耦的深度头、Splatter 头与时间条件运动头

基线方法通常使用单一预测头输出所有高斯属性，或将深度估计与外观重建耦合在一起，缺乏对几何、外观和运动的显式分工。MoVieS 引入三个解耦的预测头：

- **深度头（DPT）**：从几何预训练基础模型 **VGGT** (Wang et al., CVPR 2025) 的权重初始化，为每帧预测深度图，提供 3D 空间定位。
- **Splatter 头（DPT + RGB 捷径）**：预测每个像素的高斯外观属性（颜色、不透明度、旋转、尺度等），用于渲染新视图。
- **运动头（DPT + AdaLN）**：通过自适应层归一化（AdaLN）接收正弦编码的查询时间戳 $t_q$，为每个输入像素预测相对于查询时间的 3D 位移 $\Delta \mathbf{x}(t_q)$ 和属性形变 $\Delta \mathbf{a}(t_q)$。

三者共享同一个 Transformer 特征骨干，但在功能上解耦：深度头和 Splatter 头负责静态场景的几何与外观重建，运动头则在此基础上叠加时间条件的变形预测。这种解耦设计使得各任务可以独立优化，同时通过共享骨干实现多任务协同。

### 3. 时间建模机制：AdaLN 注入查询时间的运动回归

此前处理动态场景的方法（如 **STORM** (Yang et al., ICLR 2025)）通常依赖独立的光流或轨迹模型进行运动估计，与视图合成任务分离。MoVieS 的运动头通过 AdaLN 机制将查询时间戳直接注入特征骨干的聚合 token 中，使得运动预测与场景理解深度融合。具体而言，输入帧的时间戳 $t_i \in [0,1]$ 经正弦位置编码后与图像 token、相机 token 拼接，在注意力块中进行跨帧交互；运动头则接收额外的查询时间编码 $t_q$，通过 AdaLN 调节特征分布，直接回归每个像素的 3D 运动向量。

这种设计的关键优势在于：运动预测不再是一个独立的后处理步骤，而是与深度估计、外观重建共享特征表示，使得模型能够学习到运动与场景几何、外观之间的内在关联。

### 4. 训练目标：引入运动损失的多任务联合优化

基线方法通常仅使用深度损失和渲染损失（MSE 或 LPIPS）进行训练。MoVieS 在总损失中显式加入运动损失，形成三任务联合优化：

$$\mathcal{L} := \lambda_{\mathrm{d}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{r}} \mathcal{L}_{\mathrm{rendering}} + \lambda_{\mathrm{m}} \mathcal{L}_{\mathrm{motion}}$$

其中运动损失由两项组成：

$$\mathcal{L}_{\mathrm{motion}} := \lambda_{\mathrm{pt}} \mathcal{L}_{\mathrm{pt}} + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}}$$

- **点对点 L1 损失** $\mathcal{L}_{\mathrm{pt}}$：对有效跟踪点集合 $\Omega$ 中每个点，计算预测运动向量与真值之间的 L1 误差。
- **内部距离分布保持损失** $\mathcal{L}_{\mathrm{dist}}$：约束预测的运动向量保持与真值一致的内部相对距离结构，对 $\Omega$ 中所有点对计算点积的 L1 差异。

消融实验（Table 5）证明，同时使用两种运动损失在 Aria 数字孪生数据集上将 3D 点跟踪 EPE 降至 0.2153，$\delta_{0.05}$ 提升至 52.05%，优于单独使用任一损失。更关键的是，联合训练运动估计与新视图合成（完整 MoVieS）在 DyCheck 上的 mPSNR 达 18.46，显著优于仅训练 NVS 或仅训练运动的变体（Table 6），验证了多任务协同对两个方向的共同促进作用——这一因果机制是 MoVieS 区别于“先估计运动再合成视图”分离式方案的本质差异。

## 整体框架

MoVieS 提出了一种统一的多任务前馈框架，将动态场景的外观重建、几何预测与 3D 运动跟踪集成在单一模型中。其核心设计思路是：将动态场景解构为**静态像素对齐的高斯原语（splatter pixel）** 和**时间相关的变形场**，通过共享的 Transformer 特征骨干与三个解耦的预测头，在单次前向传播中同时输出深度图、新视图渲染所需的高斯属性，以及任意查询时刻的 3D 运动位移。

**输入与共享编码**

模型接受一段已知相机姿态的单目视频帧序列作为输入。每帧图像首先经过一个共享的图像编码器提取视觉特征；同时，输入帧的时间戳 $t_i \in [0,1]$ 通过正弦位置编码生成时间标记（timestamp token），与图像标记和相机标记（camera token）拼接后送入特征骨干。相机标记贯穿整个骨干网络，与 Plücker 嵌入互补使用，为多帧交互提供相机感知的上下文建模能力。

**特征骨干**

特征骨干基于几何预训练的注意力模块（继承自 **VGGT**，Wang et al., CVPR 2025），在视频帧之间进行跨帧的标记交互。这一设计使得每个像素的共享特征能够融合时序上下文与多视图几何信息，为下游三个预测头提供统一的表示基础。

**三个解耦预测头**

从共享特征出发，MoVieS 分叉出三个功能互补的预测头：

1. **深度头（Depth Head）**：以 VGGT 权重初始化，为每一输入帧预测稠密深度图，提供 3D 空间定位。这是场景几何重建的基础，也为 splatter 像素的 3D 位置初始化提供锚点。

2. **Splatter 头（Splatter Head）**：预测每个像素对应的高斯原语外观属性——颜色、不透明度、旋转四元数、尺度等，同时通过 RGB 捷径（skip connection）保留纹理细节。这些属性与深度头给出的 3D 位置共同构成静态 splatter 像素，用于可微光栅化渲染新视图。

3. **运动头（Motion Head）**：这是 MoVieS 实现动态建模的关键模块。给定 $M$ 个查询时间戳 $t_q$，运动头通过自适应层归一化（AdaLN）将正弦编码的查询时间注入聚合后的标记，为每个输入像素回归相对于查询时刻的 3D 位移 $\Delta\mathbf{x}(t)$ 和高斯属性形变 $\Delta\mathbf{a}(t)$。随后，使用查询时刻对应的相机参数进行光栅化，渲染出 $M$ 个时刻的图像用于监督。

**动态 Splatter Pixel 表示**

在推理时，每个 splatter 像素 $\mathbf{g}$ 关联一个时间相关的变形场 $\mathbf{m}(t) := \{\Delta\mathbf{x}(t), \Delta\mathbf{a}(t)\}$。对于任意查询时刻 $t$，其位置和属性按如下方式更新：

$$\mathbf{x} \gets \mathbf{x} + \Delta \mathbf{x}(t), \quad \mathbf{a} \gets \mathbf{a} + \Delta \mathbf{a}(t)$$

这种设计将静态场景表示与时间演变解耦：静态高斯原语负责场景的“内容”，变形场负责“运动”。对于静态输入，模型预测的运动自然收敛至零（小于 $10^{-3}$），保证了静态场景上的兼容性。

**多任务训练目标**

整个框架通过一个加权多任务损失端到端训练：

$$\mathcal{L} := \lambda_{\mathrm{d}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{r}} \mathcal{L}_{\mathrm{rendering}} + \lambda_{\mathrm{m}} \mathcal{L}_{\mathrm{motion}}$$

其中深度损失 $\mathcal{L}_{\mathrm{depth}}$ 由预测深度与真值的 MSE 及其空间梯度的 L1 损失组成；渲染损失 $\mathcal{L}_{\mathrm{rendering}}$ 包含像素级 MSE 和 LPIPS 感知损失；运动损失 $\mathcal{L}_{\mathrm{motion}}$ 进一步分解为点对点 L1 项和内部距离分布保持项，共同监督 3D 位移的回归质量。消融实验证实，三者联合训练能产生显著的多任务协同增益——在 DyCheck 动态基准上，完整 MoVieS 的 mPSNR 达到 18.46，远优于仅训练静态或仅训练运动的变体。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/001_Figure_1.jpg]]
*Figure 1: Overview. MoVieS consists of a shared image encoder, an attention-based feature backbone (Sec. 3.2.1), and three heads (Sec. 3.2.2) to jointly model appearance, geometry and motion. Motion head is time-conditioned to model dynamic content with respect to several query timestamps. Normalized XYZ values in the 3D space of motion maps are treated as RGB channels for visualization. Time-varying Gaussian attributes are omitted and point clouds with color and identity Gaussian attributes are visualized here for brevity*

## 核心模块与公式推导

### 动态 Splatter Pixel 表示

MoVieS 将动态场景解构为一组**静态高斯原语**（static Gaussian primitives）及其对应的**时间相关变形场**（deformation fields）。每个 splatter pixel $g$ 在基准时刻具有位置 $\mathbf{x}$ 和外观属性 $\mathbf{a}$（包含颜色、不透明度、旋转、尺度等），在任意查询时刻 $t$ 通过运动向量进行变形：

$$
\mathbf{x} \gets \mathbf{x} + \Delta \mathbf{x}(t), \quad \mathbf{a} \gets \mathbf{a} + \Delta \mathbf{a}(t)
$$

其中 $\Delta \mathbf{x}(t)$ 和 $\Delta \mathbf{a}(t)$ 分别表示位置和属性的 3D 形变。这一表示将静态场景的像素对齐高斯原语（借鉴自 **DepthSplat** (Xu et al., CVPR 2025) 和 **GS-LRM** (Zhang et al., ECCV 2024)）自然推广到动态域，使每个原语具备可追踪的时间演化能力。

### 预测头设计

模型包含三个解耦的预测头，共享来自特征骨干的上下文感知 token：

- **深度头（Depth Head）**：从预训练的 **VGGT** (Wang et al., CVPR 2025) 权重初始化，为每帧输入预测稠密深度图，提供 3D 空间定位。
- **Splatter 头（Splatter Head）**：基于深度头输出，通过 RGB 捷径连接预测每个像素的高斯外观属性，用于可微光栅化渲染。
- **运动头（Motion Head）**：通过自适应层归一化（AdaLN）注入正弦编码的查询时间戳 $t_q$，直接回归每个输入像素在查询时刻的 3D 位移 $\Delta \mathbf{x}(t_q)$ 和属性变化 $\Delta \mathbf{a}(t_q)$。

### 多任务训练目标

总损失由深度、渲染和运动三部分加权组成：

$$
\mathcal{L} := \lambda_{\mathrm{d}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{r}} \mathcal{L}_{\mathrm{rendering}} + \lambda_{\mathrm{m}} \mathcal{L}_{\mathrm{motion}}
$$

**深度损失** 监督几何估计，包含预测深度与真值的 MSE 及其空间梯度的 L1 损失：

$$
\mathcal{L}_{\mathrm{depth}} := \sum_{i=1}^{N} \| D_i - \hat{D}_i \|_2 + \| \nabla D_i - \nabla \hat{D}_i \|_1
$$

**渲染损失** 作用于从 $M$ 个视角渲染的图像与对应时刻的真实视频帧：

$$
\mathcal{L}_{\mathrm{rendering}} := \sum_{v=1}^{M} \| I_v - \hat{I}_v \|_2 + \lambda_{\mathrm{LPIPS}} \cdot \mathrm{LPIPS}(I_v, \hat{I}_v)
$$

包含像素级 MSE 和 LPIPS 感知损失，确保外观重建质量。

**运动损失** 由两项组成，对有效跟踪点集合 $\Omega$ 中的 $P$ 个点进行监督：

$$
\mathcal{L}_{\mathrm{motion}} := \lambda_{\mathrm{pt}} \mathcal{L}_{\mathrm{pt}} + \lambda_{\mathrm{dist}} \mathcal{L}_{\mathrm{dist}}
$$

点对点 L1 损失直接约束每个点的预测运动向量与真值一致：

$$
\mathcal{L}_{\mathrm{pt}} = \frac{1}{P} \sum_{i \in \Omega} \| \Delta \hat{\mathbf{x}}_i - \Delta \mathbf{x}_i \|_1
$$

内部距离分布保持损失约束预测的运动向量维持与真值一致的相对距离结构，对 $\Omega$ 中所有点对计算点积的 L1 差异：

$$
\mathcal{L}_{\mathrm{dist}} = \frac{1}{P^2} \sum_{(i,j) \in \Omega \times \Omega} \| \Delta \hat{\mathbf{x}}_i \cdot \Delta \hat{\mathbf{x}}_j^{\top} - \Delta \mathbf{x}_i \cdot \Delta \mathbf{x}_j^{\top} \|_1
$$

消融实验（Table 5）证实，同时使用点对点 L1 损失和分布损失能最有效地提升 3D 点跟踪精度，在 Aria 数字孪生数据集上 EPE 降至 0.2153，$\delta_{3D}^{0.05}$ 达 52.05%。

### 时间条件注入机制

特征骨干中，输入帧的时间戳 $t_i \in [0,1]$ 通过正弦位置编码生成时间 token，与图像 token 和相机 token 拼接后送入基于 **VGGT** 几何预训练注意力块的 Transformer 骨干进行跨帧交互。运动头则通过 AdaLN 接收查询时间戳 $t_q$ 的正弦编码，使模型能够在任意查询时刻预测运动，而非仅局限于输入帧时刻。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/002_Figure_2.jpg]]
*Figure 2: Motion Head. Given M query timesteps, the proposed motion head is conditioned via adaptive layer normalization (AdaLN) and predicts 3D displacements for each input pixel. After rasterization using the M corresponding query-time cameras, output images in shape*

## 实验与分析

### 4.1 实验设置

MoVieS 在八个异构数据集上进行大规模联合训练（Table 1），覆盖静态场景、动态场景、深度标注和 3D 点跟踪标注。评估围绕两大核心任务展开：**新视图合成（NVS）** 和 **3D 点跟踪**。NVS 在静态基准 RealEstate10K 和动态基准 DyCheck、NVIDIA Dynamic 上进行，指标为 PSNR、SSIM、LPIPS；3D 点跟踪在 TAPVid-3D 基准（含 Aria Digital Twin、DriveTrack、Panoptic Studio）上评估，指标为 3D 端点误差 $\mathrm{EPE}_{3D}$、$\delta_{3D}^{0.05}$ 和 $\delta_{3D}^{0.10}$。所有比较方法均使用相同的相机参数（内参和外参），动态场景评估中不使用任何动态物体掩码，3D 点跟踪比较时为基线方法提供相同的深度估计模型和相机信息以确保公平。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/003_Table_1.jpg]]
*Table 1: Training Datasets. Eight datasets from diverse sources are utilized to train MoVieS at scale*

### 4.2 新视图合成主结果

**Table 2** 展示了新视图合成的主实验结果。在静态场景 RealEstate10K 上，MoVieS 达到 27.60 PSNR，与当前最优的静态专用方法保持竞争力；更重要的是，当处理静态输入时，模型预测的运动自然收敛至零（小于 $10^{-3}$），无需任何静态/动态场景判别机制。在动态场景 DyCheck 上，MoVieS 以 **18.46 mPSNR** 取得最优，且推理速度仅需 **0.93 秒/场景**，比此前需要数分钟至数小时的逐场景优化方法快数个数量级。定性结果（Figure 3）显示，MoVieS 合成的动态新视图在运动边界和纹理细节上均优于对比方法。

值得关注的是，MoVieS 在 DyCheck 上的优势是在不使用任何动态掩码的条件下取得的，而多数对比方法依赖掩码来隔离动态区域。这表明模型通过显式运动监督学到了鲁棒的运动-外观解耦能力。

### 4.3 3D 点跟踪主结果

**Table 3** 报告了 3D 点跟踪结果。在 Aria Digital Twin 上，MoVieS 取得 $\mathrm{EPE}_{3D}=0.2153$ 和 $\delta_{3D}^{0.05}=52.05\%$，显著优于依赖独立深度估计模型（如 Video Depth Anything）的基线方法。在 DriveTrack 和 Panoptic Studio 上同样保持领先。这一优势源于 MoVieS 在统一框架内联合优化几何估计和运动预测：深度头为 3D 反投影提供精确的空间定位，运动头直接回归 3D 位移，避免了分离式流水线中的误差累积。

### 4.4 消融实验

#### 4.4.1 相机条件化方式

**Table 4** 消融了相机条件化策略。单独使用相机 token 或 Plücker 嵌入均不如二者组合：组合方案在 RealEstate10K 上取得最佳 PSNR 27.60。相机 token 通过注意力机制注入特征骨干，提供全局的相机姿态上下文；Plücker 嵌入则编码逐像素的射线几何信息。二者互补，共同增强了模型对相机变化的感知能力。

#### 4.4.2 运动监督信号

**Table 5** 消融了运动损失的设计。单独使用点对点 L1 损失（$\mathcal{L}_{\mathrm{pt}}$）或分布损失（$\mathcal{L}_{\mathrm{dist}}$）均不如二者组合：组合方案在 Aria Digital Twin 上将 EPE 降至 0.2153，$\delta_{0.05}$ 提升至 52.05%。Figure 4 的可视化进一步揭示：仅用 L1 损失时，运动预测在低纹理区域出现漂移；仅用分布损失时，运动方向大致正确但幅度不准确。组合损失同时约束了逐点精度和点间相对结构，实现了更稳定的运动学习。

#### 4.4.3 运动估计与视图合成的协同

**Table 6** 是揭示核心机制的关键消融。对比三个变体：
- **Static w/o Motion**：仅训练深度和渲染损失，无运动头，在 DyCheck 上 mPSNR 大幅下降；
- **Motion Only w/o NVS**：仅训练运动损失，无渲染损失，运动预测质量显著劣化；
- **Ours（完整 MoVieS）**：联合训练所有任务，取得最优 mPSNR 18.46。

这验证了论文的核心洞见：**运动估计和新视图合成之间存在双向协同**——视图合成提供的像素级外观监督帮助运动头学习更精确的对应关系，而运动头学到的形变信息反过来提升动态场景的渲染质量。Figure 4 的定性对比直观展示了这种协同效应：联合训练的运动预测在运动边界处更清晰，在遮挡区域更合理。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/007_Figure_4.jpg]]
*Figure 4: Motion Visualization for Ablation Studies. We investigate key factors affecting motion learning in MoVieS, such as loss design and synergy with view synthesis. XYZ values in motion maps are normalized as RGB for visualization. Red arrows on video frames indicate motion directions*

### 4.5 零样本应用

Figure 5 展示了 MoVieS 预测的运动图在未经过任何任务特定微调的情况下，可直接应用于**场景流估计**和**运动物体分割**两个下游任务。这得益于运动头输出的逐像素 3D 位移图天然编码了场景的运动信息——位移的幅值对应场景流强度，位移的聚类模式自然分离出运动物体与静态背景。这一零样本迁移能力表明 MoVieS 学到的运动表征具有良好的通用性。

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/011_Figure_5.jpg]]
*Figure 5: Zero-shot Applications. Predicted motion maps from our model can be directly applied to downstream tasks, such as (a) scene flow estimation and (b) moving object segmentation, in a zero-shot manner, without any task-specific fine-tuning or supervision*

### 4.6 局限性与失效模式

尽管 MoVieS 在多个基准上表现出色，以下局限性值得关注：

1. **已知相机姿态依赖**：当前框架假设输入视频的相机姿态已知，未处理无姿态视频的重建场景。实际应用中，相机姿态获取本身是一个非平凡问题。
2. **训练数据异构性**：八个训练数据集在标注类型（深度、跟踪点、动态性）上存在差异，缺乏统一的同步多视图、密集深度和点跟踪标注。这可能影响模型在特定场景组合下的泛化能力，尤其当测试场景的运动模式与训练分布偏差较大时。
3. **尺度归一化损失**：模型通过平均距离进行 3D 场景尺度归一化，虽然简化了训练，但可能损失绝对度量精度，在需要精确尺度信息的应用（如机器人导航）中可能不足。
4. **挑战性材质与遮挡**：论文未专门验证模型在透明、反射或严重遮挡区域的运动建模能力。这些区域的视觉特征模糊或缺失，可能导致运动预测失败——这一点需要在实际部署中手动验证。
5. **长序列与拓扑变化**：当前实验集中在短时视频片段，模型对于更长序列的在线点跟踪能力、以及面对拓扑断裂或碎片化等复杂形变的泛化表现，仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/005_Table_2.jpg]]
*Table 2: Evaluation on Novel View Synthesis. The best , second best and third best results are highlighted for clarity. † indicates our reimplemented version of GS-LRM [91]. “Ours (static)” refers to our method pretrained solely on static datasets without the motion head. The same camera parameters are provided for all methods for fair comparison*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/006_Table_3.jpg]]
*Table 3: Evaluation on 3D Point Tracking. The best , second best and third best results are highlighted for clarity. † denotes combining a depth estimation model [6]. All methods are given the same camera information for unprojecting 3D tracked points*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/010_Table_6.jpg]]
*Table 6: Ablation Study on the synergy of motion estimation and novel view synthesis (NVS)*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/009_Table_5.jpg]]
*Table 5: Ablation study on motion supervision*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/008_Table_4.jpg]]
*Table 4: Ablation study on camera conditioning*

![[assets/figures/papers/paper_list_l16_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_MoVieS_Motion_Awar/figures/004_Figure_3.jpg]]
*Figure 3: Novel View Synthesis for Dynamic Scenes. Given a monocular video, we compare synthesized novel views of different methods. Invisible regions are rendered as black or white, depending on the implementation. More results are in the supplementary material*

## 方法谱系与知识库定位

### 与前馈视图合成方法的继承与突破

MoVieS 的方法论根脉深植于近年快速发展的前馈式新视图合成（feed-forward NVS）路线。这类方法的核心范式是：给定稀疏输入视图，通过单次前向传播直接预测场景的显式表示（如 3D 高斯原语），从而彻底绕开传统逐场景优化的耗时瓶颈。**DepthSplat**（Xu et al., CVPR 2025）和 **GS-LRM**（Zhang et al., ECCV 2024）是这一路线的代表性工作，它们分别探索了基于深度引导的 splatting 和大规模 Transformer 重建模型，但均局限于静态场景。**STORM**（Yang et al., ICLR 2025）将前馈重建拓展到户外驾驶场景的多视图时空建模，初步触及了动态场景，但其设计高度依赖驾驶场景的结构化先验，缺乏对通用动态内容的运动感知能力。

MoVieS 直接继承了 DepthSplat 的“像素对齐高斯原语”（splatter pixel）表示，并将其作为静态基底。在此基础上，MoVieS 引入了一个关键的表示创新——**动态 splatter 像素**：每个静态高斯原语 $g$ 被关联一个时间相关的变形场 $m(t) := \{\Delta\mathbf{x}(t), \Delta\mathbf{a}(t)\}$，使得场景在任意查询时刻 $t$ 的位置和外观可由下式获得：

$$\mathbf{x} \gets \mathbf{x} + \Delta \mathbf{x}(t), \quad \mathbf{a} \gets \mathbf{a} + \Delta \mathbf{a}(t)$$

这一设计将动态场景解构为“静态几何基元 + 可学习运动场”，在保持前馈推理效率的同时，首次将显式的 3D 运动建模内嵌到视图合成框架中。与 **BTimer** 和 **NutWorld** 等前馈动态合成方法相比，MoVieS 不依赖外部的光流或轨迹预测模块，而是通过共享特征骨干和联合训练目标，在单一模型内统一了外观重建、几何预测和运动跟踪三大任务。

### 与几何基础模型的架构关联

MoVieS 的特征骨干直接复用了 **VGGT**（Wang et al., CVPR 2025）的预训练注意力块。VGGT 是一个面向静态场景的几何重建基础模型，其注意力层已经蕴含了丰富的多视图几何匹配能力。MoVieS 的策略是“几何预训练 + 运动微调”：冻结或部分继承 VGGT 的权重作为特征交互的基础，然后通过时间戳标记（sinusoidal positional encoding 编码的 $t_i \in [0,1]$）的注入和多任务训练目标，使原本仅处理空间对应关系的注意力机制获得跨帧时间推理的能力。这种“借用几何先验、注入时间感知”的路线，使得 MoVieS 在训练数据覆盖不足的动态场景上仍能保持合理的几何稳定性。

### 适用边界与能力定位

**已知相机姿态的单目视频是 MoVieS 的刚性前置条件。** 模型假设输入视频的相机内外参完全已知，且场景尺度通过平均距离进行归一化。这一假设使其无法直接处理无姿态视频或未知尺度的重建任务。在场景类型上，MoVieS 的训练数据覆盖了八个异构数据集（Table 1），包括室内外静态场景、人体运动、一般物体交互等，因此对常见动态场景具有较好的泛化性。但对于以下边界情况，方法存在已知或可预见的局限：

1. **透明、反射和严重遮挡区域**：高斯原语表示本身对非朗伯表面和复杂遮挡的建模能力有限，运动头在这些区域的监督信号也往往稀疏或不可靠。文中未提供针对此类场景的专门验证，实际表现需要谨慎评估。

2. **拓扑变化与碎片化运动**：动态 splatter 像素的运动建模基于连续变形假设（每个原语的位置和属性随时间连续变化）。对于物体断裂、拓扑分离或新原语涌现等离散事件，当前的变形场框架缺乏自然的处理机制。

3. **绝对尺度精度**：3D 场景尺度归一化虽然保证了训练的数值稳定性，但牺牲了绝对度量精度。在需要精确物理尺寸的下游任务（如机器人抓取、建筑测量）中，这一简化可能引入不可忽略的误差。

4. **长序列与在线场景**：MoVieS 设计为离线批处理模式，一次处理固定长度的视频片段。对于需要持续跟踪的长视频流或在线应用，模型缺乏记忆机制和流式处理能力。

### 开放问题与未来方向

MoVieS 的提出打开了一个新的研究空间，但同时也留下了若干亟待解决的关键问题：

- **无姿态视频的 4D 重建**：当前框架对相机姿态的依赖是其走向“通用 4D 重建”的最大障碍。是否可以将姿态估计与运动建模联合优化，或通过自监督信号从视频中同时恢复几何、运动和相机轨迹，是下一步的重要方向。

- **长时序点跟踪与记忆机制**：3D 点跟踪在短片段上表现优异，但面对分钟级或更长的视频，累积误差和遮挡恢复问题将变得突出。引入可学习的记忆模块或滑动窗口状态传递机制，可能是提升长期跟踪鲁棒性的关键。

- **更丰富的运动表示**：当前的变形场假设每个原语独立运动，缺乏对物体级运动一致性的显式建模。引入物体实例分割或运动分组先验，可能进一步提升运动预测的结构化程度和下游任务（如运动物体分割，Figure 5）的精度。

- **跨域泛化能力**：训练数据虽覆盖多个领域，但极端运动（如高速旋转、剧烈变形）和罕见动态场景（如流体、烟雾）的泛化表现尚未得到系统验证。扩大数据规模和多样性，或引入物理先验约束，是提升鲁棒性的潜在路径。

**总体定位**：MoVieS 在前馈视图合成与动态场景建模的交叉点上，通过“静态基元 + 时间条件变形场”的统一表示和“外观-几何-运动”联合训练范式，首次实现了亚秒级的 4D 动态视图合成与 3D 点跟踪。它在方法谱系中处于静态前馈重建模型（DepthSplat, GS-LRM）向通用 4D 场景理解模型演进的关键节点，其解耦的预测头设计和多任务协同训练策略为后续工作提供了可复用的架构模板。

## 原文 PDF

![[paperPDFs/CVPR_2026/MoVieS_Motion_Aware_4D_Dynamic_View_Synthesis_in_One_Second.pdf]]