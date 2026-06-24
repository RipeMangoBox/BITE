---
title: "Difix3D+: Improving 3D Reconstructions with Single-Step Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Difix3D_Improving_3D_Reconstructions_with_Single_Step_Diffusion_Models.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/difix3d/
aliases:
- DI3RSSDM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过训练一个在特定噪声水平（τ=200）下的单步扩散模型（DIFIX）来增强渲染视图，并利用渐进式3D更新策略将增强视图蒸馏回3D表示，从而在保持多视图一致性的同时消除伪影。"
primary_logic: "单步扩散模型在低噪声水平下能有效去除神经渲染伪影，但直接应用会导致多视图不一致；将增强视图通过渐进式蒸馏注入3D表示，并辅以推理时实时后处理，可以在大幅提升视觉质量的同时维持3D几何一致性。"
claims:
- "噪声水平τ=200在去除伪影和保留上下文之间取得最佳平衡，并在指标上达到最优。"
- "渐进式3D更新对于多视图一致性至关重要，否则LPIPS和FID会显著退化。"
- "DIFIX3D+在Nerfbusters和DL3DV数据集上比基线平均提升PSNR >1dB，FID改善约2倍。"
- "单步扩散模型推理仅需76毫秒（NVIDIA A100），比多步扩散模型快10倍以上。"
---

# Difix3D+: Improving 3D Reconstructions with Single-Step Diffusion Models

> [!tip] 核心洞察
> 单步扩散模型在低噪声水平下能有效去除神经渲染伪影，但直接应用会导致多视图不一致；将增强视图通过渐进式蒸馏注入3D表示，并辅以推理时实时后处理，可以在大幅提升视觉质量的同时维持3D几何一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Difix3D+: 通过单步扩散模型改进3D重建 |
| 英文题名 | Difix3D+: Improving 3D Reconstructions with Single-Step Diffusion Models |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.01774); [Project](https://research.nvidia.com/labs/toronto-ai/difix3d); [Project](https://research.nvidia.com/labs/toronto-ai/difix3d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DIFIX3D+ |
| Dataset | Nerfbusters, DL3DV |

> [!tip] 效果简介
> - Nerfbusters 上，PSNR 为 18.32 (Nerfacto) / 18.51 (3DGS)，对比 17.29 (Nerfacto) / 17.66 (3DGS)，变化 +1.03 / +0.85。
> - Nerfbusters 上，LPIPS 为 0.2789 (Nerfacto) / 0.2637 (3DGS)，对比 0.4021 (Nerfacto) / 0.3265 (3DGS)，变化 -0.1232 / -0.0628。
> - Nerfbusters 上，FID 为 49.44 (Nerfacto) / 41.77 (3DGS)，对比 134.65 (Nerfacto) / 113.84 (3DGS)，变化 2.72× lower / 2.73× lower。

## 概述

### 问题瓶颈

基于神经辐射场（NeRF）和3D高斯散点（3DGS）的新视图合成方法，在远离训练视角的欠约束区域会生成严重伪影——包括错误几何、缺失纹理和漂浮物。这些方法缺乏数据驱动的先验来填补缺失的外观信息，导致在极端新视角下的保真度急剧下降。这是当前3D重建方法在稀疏输入或大视角偏移场景下的核心瓶颈。

### 核心思路

DIFIX3D+ 提出将**单步扩散模型的生成先验**注入3D重建流程，以消除神经渲染伪影。其关键洞察是：在特定低噪声水平（τ=200）下，单步扩散模型能够有效去除NeRF/3DGS渲染视图中的伪影，同时保留场景上下文。然而，直接将增强视图用于多视图合成会导致时序不一致（闪烁）。为此，DIFIX3D+ 采用**渐进式3D更新策略**——通过相机姿态扰动生成新视图，经DIFIX增强后逐步蒸馏回3D表示，在维持多视图几何一致性的前提下大幅提升视觉质量。推理阶段，DIFIX还作为实时神经增强器（每帧76毫秒）进一步去除残留伪影。

### 方法定位

DIFIX3D+ 位于**2D生成先验驱动3D重建增强**的方法谱系中。与每场景训练一个GAN的**GANeRF**、利用3D扩散模型去除伪影的**Nerfbusters**（Warburg et al., ICCV 2023）、以及聚合邻近参考视图信息的**NeRFLiX**（Zhou et al., CVPR 2023）不同，DIFIX3D+ 的核心创新在于：1）使用**单步扩散模型**实现比多步扩散模型快10倍以上的推理速度；2）通过**渐进式蒸馏**将增强视图一致性注入3D表示；3）在训练和推理两个阶段协同使用扩散先验。该方法可与Nerfacto（Tancik et al., SIGGRAPH 2023）和3DGS（Kerbl et al., SIGGRAPH 2023）等基础重建方法无缝集成。

### 主要结果

在Nerfbusters和DL3DV数据集上，DIFIX3D+ 相较基线方法平均PSNR提升超过1 dB，FID改善约2倍。具体而言：Nerfbusters上Nerfacto基线的PSNR从17.29提升至18.32，LPIPS从0.4021降至0.2789，FID从134.65降至49.44（2.72倍降低）；3DGS基线的PSNR从17.66提升至18.51，LPIPS从0.3265降至0.2637，FID从113.84降至41.77（2.73倍降低）。在内部自动驾驶数据集RDS上，PSNR从19.95提升至21.75，LPIPS从0.5300降至0.4016。消融实验证实，渐进式更新策略对多视图一致性至关重要——一次性注入所有伪视图会导致LPIPS和FID显著恶化；推理时后处理步骤进一步降低LPIPS并提升PSNR/SSIM，几乎不影响多视图一致性。

## 背景与动机

### 3D重建与新视图合成的核心瓶颈

神经辐射场（NeRF）与3D高斯散点（3DGS）已成为从稀疏多视图图像重建三维场景的主流范式。然而，这些方法在远离训练相机位姿的欠约束区域普遍产生严重伪影——包括错误几何、缺失区域和模糊纹理。这一问题的根源在于：稀疏输入条件下，体渲染或高斯泼溅缺乏足够的观测信号来约束三维表示，而传统重建损失（如MSE）无法提供数据先验来生成合理的外观。因此，在极端新视图上的保真度成为制约3D重建方法走向实际应用的关键瓶颈。

### 现有方法的缺口

围绕这一瓶颈，已有若干改进尝试，但各自存在局限：

- **Nerfacto** (Tancik et al., SIGGRAPH 2023) 和 **3DGS** (Kerbl et al., SIGGRAPH 2023) 作为基础重建方法，在稀疏视图下仅依赖光度损失优化，无法填补观测盲区的内容。
- **Nerfbusters** (Warburg et al., ICCV 2023) 利用3D扩散模型去除NeRF伪影，但操作于3D表示空间，计算代价高且灵活性有限。
- **GANeRF** 为每个场景单独训练一个GAN以增强NeRF的真实性，缺乏跨场景泛化能力，部署成本高。
- **NeRFLiX** (Zhou et al., CVPR 2023) 在推理时聚合邻近参考视图信息来改进新视图合成，但无法从根本上修正三维几何的错误。

这些方法的共同缺口在于：**缺乏一个高效、可泛化的机制，将2D生成模型的强大先验注入到3D重建过程中，同时保持多视图几何一致性**。直接对渲染视图应用现成的2D扩散模型虽然能局部改善视觉质量，但会导致跨视图的闪烁和不一致，破坏三维表示的内在连贯性。

### 核心动机与切入点

本文的核心洞察是：**NeRF和3DGS渲染伪影的分布，与扩散模型训练时使用的低噪声水平图像分布具有相似性**。这意味着，一个经过适配的单步扩散模型可以在特定噪声水平下有效去除神经渲染伪影，而无需多步采样。更关键的是，通过将增强后的视图以渐进方式蒸馏回3D表示，可以在大幅提升视觉质量的同时维持三维几何一致性。

基于这一洞察，DIFIX3D+ 的设计动机围绕三个递进目标展开：

1. **构建专门的伪影去除模型**：训练一个单步图像扩散模型（DIFIX），使其成为从“含伪影渲染视图”到“干净增强视图”的图像翻译器，利用参考视图的交叉注意力机制保持局部一致性。
2. **将增强视图蒸馏回3D表示**：通过渐进式3D更新策略，逐步将DIFIX增强的伪视图注入训练集，扩展3D表示的空间覆盖范围，避免一次性注入导致的多视图不一致退化。
3. **推理时实时后处理**：将DIFIX作为神经增强器在推理阶段实时应用，以76毫秒的单帧延迟进一步去除残余伪影，形成完整的重建与渲染增强闭环。

## 核心创新

DIFIX3D+ 的核心创新在于将**单步扩散模型的2D生成先验**系统性地注入3D重建管线，解决了NeRF和3DGS在欠约束区域产生严重伪影的根本瓶颈。其创新围绕三个紧密耦合的“changed slots”展开，形成了一条从伪影去除到3D一致性保持的闭环管线。

### 1. 单步扩散模型作为伪影去除器（DIFIX）

与传统依赖多步扩散或每场景训练GAN的方法不同，DIFIX3D+提出了**DIFIX**——一个基于预训练单步扩散模型（SD-Turbo）微调的图像到图像翻译模型。其关键设计选择在于：

- **低噪声水平（τ=200）**：研究发现，将NeRF/3DGS渲染伪影视为扩散模型中的特定噪声水平，在τ=200处进行单步“去噪”可以在去除伪影和保留场景上下文之间取得最佳平衡（Figure 4）。更高的噪声水平（如τ=600）会过度修改图像内容，而更低水平（如τ=10）则无法有效去除伪影。
- **参考视图交叉注意力**：DIFIX接收含伪影的渲染视图和一组干净的参考视图作为输入，通过将自注意力层改造为**交叉视图参考混合层**（将视图轴与空间轴合并后执行注意力操作），使模型能够利用多视图信息来保持增强结果与已知视角的一致性。
- **Gram矩阵风格损失**：在标准重建损失和LPIPS损失之外，引入基于VGG-16特征Gram矩阵的风格损失$\mathcal{L}_{\text{Gram}}$，以更好地保留图像的纹理和结构细节。总训练目标为：
  $$\mathcal{L} = \mathcal{L}_{\text{Recon}} + \mathcal{L}_{\text{LPIPS}} + 0.5 \mathcal{L}_{\text{Gram}}$$

消融实验（Table S1/Figure S1）证实，降低噪声水平、引入参考视图条件和Gram损失均对DIFIX性能有正向贡献。

### 2. 渐进式3D更新策略

直接对渲染视图应用DIFIX虽然能改善单帧质量，但会导致严重的多视图不一致（闪烁）。DIFIX3D+的核心机制是将增强视图**蒸馏回3D表示**，并通过**渐进式更新**来维持几何一致性：

- 在3D重建训练过程中，每1.5k次迭代，通过轻微扰动真实相机姿态生成新视图，用DIFIX增强后加入训练集。
- 这种渐进式策略逐步扩展3D表示的空间覆盖范围，确保扩散模型始终有足够强的参考视图条件。
- 消融实验（Table 4）表明，一次性注入所有伪视图会导致LPIPS和FID显著退化，证明了增量更新策略对多视图一致性的关键作用。

### 3. 推理时实时后处理

DIFIX3D+将DIFIX同时用作推理时的**实时神经增强器**，对已蒸馏的3D表示渲染结果进行最终去伪影处理。由于DIFIX是单步模型，在NVIDIA A100 GPU上仅需**76毫秒**额外渲染时间，比标准多步扩散模型快10倍以上。这一后处理步骤能有效去除残留伪影，进一步提升PSNR并降低LPIPS，且几乎不影响多视图一致性（Figure 7）。

### 4. 多策略配对数据构建

为训练DIFIX，论文设计了多策略的配对数据生成管线（Table 1），包括稀疏重建、循环重建、交叉参考和故意欠拟合训练，以模拟典型的新视图合成伪影。这种系统化的数据构建策略为DIFIX提供了强学习信号，使其能够泛化到多样的伪影模式。

### 与基线方法的本质区别

| 创新维度 | 基线方法 | DIFIX3D+ |
|---------|---------|----------|
| 伪影去除机制 | 无（Nerfacto/3DGS直接渲染）或每场景训练GAN（GANeRF） | 通用单步扩散模型，跨场景泛化 |
| 3D一致性保持 | 仅使用原始多视图图像优化 | 渐进式将增强视图蒸馏回3D表示 |
| 推理效率 | 无后处理或多步扩散查询 | 单步76ms实时后处理 |
| 数据先验利用 | 无显式先验 | 系统化构建配对伪影数据，利用2D扩散先验 |

这一创新组合使得DIFIX3D+在Nerfbusters和DL3DV数据集上实现了PSNR平均提升>1dB、FID改善约2倍的显著增益，同时保持了多视图几何一致性。

## 整体框架

DIFIX3D+ 的整体流程围绕一个核心观察展开：神经渲染方法（NeRF 与 3DGS）在远离训练视角的欠约束区域会产生严重的伪影，包括错误的几何结构和缺失的内容。这些伪影源于 3D 表示缺乏足够的数据先验来生成合理的外观。DIFIX3D+ 通过将单步扩散模型的强生成先验蒸馏到 3D 表示中，系统性地解决了这一问题。

### 三阶段流水线

如图 2 所示，DIFIX3D+ 由三个顺序阶段组成，形成一个闭环的增强-蒸馏-后处理框架：

**阶段 1：神经增强（Neural Enhancement）**
给定一个预训练的 3D 表示（可以是 NeRF 或 3DGS），首先通过相机姿态插值生成新视角。具体而言，从已知的参考相机姿态出发，逐步向目标视角方向扰动，渲染出这些中间视角的图像。这些渲染图像通常包含典型的神经渲染伪影。随后，DIFIX 单步扩散模型作为神经增强器，接收含伪影的渲染视图和干净的参考视图作为输入，输出伪影被显著消除的增强视图。

**阶段 2：渐进式 3D 蒸馏（Progressive 3D Distillation）**
增强后的新视角图像并非直接作为最终输出，而是被加入训练集，通过标准的 3D 重建优化过程蒸馏回 3D 表示。这一步骤至关重要：直接对渲染视图应用 DIFIX 虽然能改善单帧质量，但会导致多视图不一致（闪烁伪影）。通过将增强视图蒸馏回统一的 3D 表示，多视图一致性得以保持。该过程以渐进式方式进行：每 1.5k 次迭代，通过姿态扰动生成一批新的伪视图，经 DIFIX 增强后加入训练集，逐步扩展 3D 表示的空间覆盖范围。消融实验证实，这种增量更新策略对于维持 LPIPS 和 FID 指标至关重要，一次性注入所有伪视图会导致这些指标显著退化。

**阶段 3：实时后处理（Real-time Post-Processing）**
在推理时，DIFIX 作为最终的实时神经增强器，对渲染输出进行后处理，进一步去除残余伪影。由于 DIFIX 是单步扩散模型，在 NVIDIA A100 GPU 上的额外渲染时间仅为 76 毫秒，比标准多步扩散模型快 10 倍以上。这一后处理步骤在几乎不影响多视图一致性的前提下，进一步降低了 LPIPS 并提升了 PSNR/SSIM。

### 核心模块关系

三个核心模块的依赖关系如下：

- **DIFIX Neural Enhancer**（图 3）：基于 SD-Turbo 构建的图像到图像翻译模型。其架构包含一个 U-Net，其中标准的自注意力层被改造为交叉视图参考混合层（cross-view reference mixing layer），通过将视图轴与空间轴合并后再进行注意力计算，实现对参考视图信息的有效利用。模型在特定噪声水平 τ=200 下进行单步“去噪”，在去除伪影和保留图像上下文之间达到最优平衡。

- **Progressive 3D Update Layer**：作为连接 2D 增强和 3D 表示的桥梁，负责将 DIFIX 的输出蒸馏回 3D 表示。该模块不改变底层 3D 表示的结构（NeRF 或 3DGS），而是通过扩展训练数据来间接提升重建质量。

- **Data Curation Pipeline**：为训练 DIFIX 提供配对数据。通过稀疏重建、循环重建、交叉参考和欠拟合训练等多种策略，模拟新视角合成中常见的伪影类型，生成含伪影渲染图与干净真值图的配对数据集。

### 输入输出流

整个系统的输入是场景的多视角图像及其对应的相机姿态，输出是经过增强的 3D 表示，以及推理时可选的实时增强渲染结果。数据流呈闭环：3D 表示 → 渲染伪视图 → DIFIX 增强 → 蒸馏回 3D 表示 → 推理时再次经 DIFIX 后处理。这种设计使得 2D 扩散先验能够有效注入 3D 表示，同时避免了直接使用扩散模型带来的多视图不一致问题。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/002_Figure_2.jpg]]
*Figure 2: DIFIX3D+ pipeline. The overall pipeline of the DIFIX3D+ model involves the following stages: Step 1: Given a pretrained 3D representation, we render novel views and feed them to DIFIX which acts as a neural enhancer, removing the artifacts and improving the quality of the noisy rendered views (Sec. 4.1). The camera poses selected to render the novel views are obtained through pose interpolation, gradually approaching the target poses from the reference ones. Step 2: The cleaned novel views are distilled back to the 3D representation to improve its quality (Sec. 4.2). Steps 1 and 2 are applied in several iterations to progressively grow the spatial extent of the reconstruction and hence ensu...*

## 核心模块与公式推导

### DIFIX 神经增强器

DIFIX 是一个以**单步扩散模型 SD-Turbo** 为基础微调的图像到图像翻译模型。其核心设计思路是：将含伪影的神经渲染视图视为扩散过程中某一中间噪声水平的样本，通过单步“去噪”恢复干净图像。模型接收两个输入：

1. **含伪影的渲染视图** $\tilde{I}$（来自 NeRF 或 3DGS 的新视角渲染结果）
2. **一组干净的参考视图** $I_{\text{ref}}$（训练视角下的真实图像）

输出为增强后的新视图 $\hat{I}$。参考视图通过**交叉视图参考混合层**（cross-view reference mixing layer）注入条件信息：该层将自注意力机制中的视图轴与空间轴合并，在合并后的联合空间上执行注意力，随后恢复原始维度结构，从而捕获跨视图依赖关系。

### 噪声水平选择

DIFIX 并非从纯噪声开始采样，而是在特定噪声水平 $\tau$ 下对输入图像进行单步去噪。这一设计基于一个关键假设：**NeRF/3DGS 渲染伪影的分布与扩散模型训练时在 $\tau=200$ 附近的噪声图像分布相似**。实验验证（Figure 4）表明：

- $\tau=600$ 时，模型能有效去除伪影，但会过度改变图像内容（上下文信息丢失）
- $\tau=10$ 时，模型仅做微小调整，大部分伪影残留
- **$\tau=200$ 在去除伪影与保留上下文之间取得最佳平衡，并在各项指标上达到最优**

### 训练损失函数

DIFIX 的训练目标由三项损失的加权和构成：

$$\mathcal{L} = \mathcal{L}_{\text{Recon}} + \mathcal{L}_{\text{LPIPS}} + 0.5 \mathcal{L}_{\text{Gram}}$$

其中：

- **$\mathcal{L}_{\text{Recon}}$**：像素级重建损失，基于扩散模型的标准去噪得分匹配目标：

  $$\mathbb{E}_{\mathbf{x} \sim p_{\mathrm{data}}, \tau \sim p_{\tau}, \epsilon \sim \mathcal{N}(\mathbf{0}, I)} \left[ \lVert \mathbf{y} - \mathbf{F}_{\theta}(\mathbf{x}_{\tau}; \mathbf{c}, \tau) \rVert_2^2 \right]$$

  其中 $\mathbf{x}_{\tau}$ 是加噪到水平 $\tau$ 的输入，$\mathbf{c}$ 为参考视图条件，$\mathbf{F}_{\theta}$ 是单步去噪模型，$\mathbf{y}$ 为干净目标图像。

- **$\mathcal{L}_{\text{LPIPS}}$**：感知损失，基于深度特征空间的距离度量。

- **$\mathcal{L}_{\text{Gram}}$**：风格损失，基于 VGG-16 特征自相关的 Gram 矩阵差异：

  $$\mathcal{L}_{\mathrm{Gram}} = \frac{1}{L} \sum_{l=1}^{L} \beta_l \left\| \boldsymbol{G}_l(\hat{I}) - \boldsymbol{G}_l(I) \right\|_2$$

  其中 $\boldsymbol{G}_l(I) = \phi_l(I)^{\top} \phi_l(I)$ 为 VGG-16 第 $l$ 层特征的 Gram 矩阵，$\beta_l$ 为各层权重。该损失强制增强视图与真实图像在纹理风格上保持一致，对于去除 NeRF 渲染中常见的模糊和结构性伪影至关重要。

### 渐进式 3D 更新层

直接将 DIFIX 应用于渲染视图可提升单帧质量，但会导致多视图不一致（闪烁效应）。为解决此问题，DIFIX3D+ 引入**渐进式 3D 更新策略**：

1. 每约 1.5k 次迭代，对训练相机姿态施加微小扰动，生成朝向目标视角的中间姿态
2. 从当前 3D 表示渲染这些中间视角，得到含伪影的视图
3. 用 DIFIX 增强这些渲染视图，生成干净的伪视图
4. 将增强后的伪视图加入训练集，继续优化 3D 表示

通过多次迭代，3D 表示的覆盖范围逐步扩展，DIFIX 的增强效果被蒸馏回 3D 几何，从而在提升视觉质量的同时维持多视图一致性。

### 推理时后处理增强器

在推理阶段，DIFIX 作为**实时神经增强器**对渲染输出进行后处理，进一步去除残余伪影。由于 DIFIX 是单步扩散模型，该步骤仅增加 **76 毫秒**的渲染延迟（NVIDIA A100 GPU），比标准多步扩散模型快 10 倍以上。

### 3D 表示基础公式

DIFIX3D+ 可作用于两种主流 3D 表示，其渲染机制分别如下：

**NeRF 体积渲染**（Eq. 1）：沿射线累计辐射度

$$\mathcal{C}(\mathbf{p}) = \sum_{i=1}^{N} \alpha_i \mathbf{c}_i \prod_{j}^{i-1} (1 - \alpha_i)$$

其中 $\mathbf{p}$ 为射线上的采样点，$\alpha_i$ 为不透明度，$\mathbf{c}_i$ 为颜色。

**3DGS 高斯透明度**（Eq. 2）：三维高斯在空间点的透明度贡献

$$\alpha_i = \eta_i \exp\left[-\frac{1}{2}(\mathbf{p} - \pmb{\mu}_i)^{\top} \pmb{\Sigma}_i^{-1} (\mathbf{p} - \pmb{\mu}_i)\right]$$

其中 $\eta_i$ 为高斯的不透明度系数，$\pmb{\mu}_i$ 为中心位置，$\pmb{\Sigma}_i$ 为协方差矩阵。

## 实验与分析

### 核心瓶颈与实验动机

NeRF和3DGS在远离训练视角的欠约束区域会产生严重伪影——错误几何、缺失区域和模糊纹理——这些伪影在极端新视图上尤为突出。根本原因在于，这些表示缺乏数据先验来生成合理的外观。DIFIX3D+的实验设计围绕一个核心假设展开：**单步扩散模型在低噪声水平下能够有效去除神经渲染伪影，但直接应用会导致多视图不一致；只有将增强视图通过渐进式蒸馏注入3D表示，才能在大幅提升视觉质量的同时维持几何一致性。**

实验在两个公开基准（Nerfbusters、DL3DV）和一个内部自动驾驶数据集（RDS）上进行，覆盖自然场景和驾驶场景。评估指标包括PSNR、LPIPS、FID，并引入TSED评估多视图一致性。

---

### 主要量化结果

**Table 2** 汇总了在Nerfbusters和DL3DV上的对比结果。DIFIX3D+在两种3D骨干网络（Nerfacto和3DGS）上均取得一致且显著的提升：

| 基准 | 指标 | Nerfacto基线 | DIFIX3D+ (Nerfacto) | 3DGS基线 | DIFIX3D+ (3DGS) |
|------|------|-------------|---------------------|---------|-----------------|
| Nerfbusters | PSNR | 17.29 | **18.32** (+1.03) | 17.66 | **18.51** (+0.85) |
| Nerfbusters | LPIPS | 0.4021 | **0.2789** (-0.1232) | 0.3265 | **0.2637** (-0.0628) |
| Nerfbusters | FID | 134.65 | **49.44** (2.72× lower) | 113.84 | **41.77** (2.73× lower) |
| DL3DV | FID | 112.30 | **41.77** (2.69× lower) | 107.23 | **40.86** (2.62× lower) |

**核心发现**：FID改善约2.7倍，PSNR提升约1dB，LPIPS降低0.06–0.12。FID的大幅改善表明DIFIX3D+显著提升了渲染图像的感知真实感，这与扩散模型先验的注入直接相关。PSNR的温和提升则反映了方法在保持结构保真度方面的保守性——它修复伪影而非重写场景内容。

在内部RDS数据集（**Table 3**）上，DIFIX3D+将Nerfacto的PSNR从19.95提升至21.75（+1.80），LPIPS从0.5300降至0.4016（-0.1284），验证了方法在自动驾驶场景下的泛化能力。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results on the RDS dataset. DIFIX for RDS was trained on 40 scenes and 100,000 paired data samples. Table 3. Comparison of quantitative results on RDS dataset. The best result is highlighted in bold*

---

### 消融实验

**Table 4** 对DIFIX3D+进行了系统的组件消融，逐层揭示每个设计选择的作用：

**(a) 直接DIFIX增强（无3D更新）**：对渲染视图直接应用DIFIX能改善PSNR/LPIPS，但导致严重多视图不一致（闪烁效应）。这验证了核心洞察：2D增强破坏了跨视图的几何一致性。

**(b) 非渐进式蒸馏**：将DIFIX增强的伪视图一次性全部加入训练集。相比(a)，多视图一致性有所改善，但LPIPS和FID显著退化。**这证明渐进式更新策略是关键的**——一次性注入过多增强视图会引入冲突的监督信号，破坏3D表示的收敛。

**(c) DIFIX3D（渐进式蒸馏）**：每1.5k次迭代通过相机姿态扰动生成新视图，用DIFIX增强后逐步加入训练集。该方法在PSNR、LPIPS和FID上均达到最优，且多视图一致性大幅提升。

**(d) DIFIX3D+（渐进式蒸馏 + 推理时后处理）**：在(c)的基础上，推理时使用DIFIX作为实时神经增强器。这进一步降低了LPIPS并提升了PSNR/SSIM，几乎不影响多视图一致性。**Figure 7** 定性展示了后处理步骤对残余伪影的去除效果——特别是细小的漂浮物和纹理模糊区域。

**DIFIX组件消融**（**Table 5** 和 **Figure S1**）进一步验证了三个关键设计：
- **噪声水平τ=200**：在去除伪影和保留上下文之间取得最佳平衡（**Figure 4**）。更高噪声（τ=600）会改变图像内容，更低噪声（τ=10）则几乎不处理伪影。
- **Gram损失**：引入基于VGG-16特征自相关的风格损失，显著改善纹理细节的保真度。
- **参考视图条件**：通过交叉视图参考混合层（**Figure 3**）利用参考视图信息，提升增强结果与场景外观的一致性。

---

### 关键定性结果

**Figure 5** 展示了在DL3DV和Nerfbusters场景上的伪影去除对比。DIFIX3D+纠正了其他方法无法处理的严重伪影——包括错误的几何结构、缺失的物体区域和模糊纹理。与Nerfbusters（使用3D扩散模型去除伪影）和GANeRF（每场景训练GAN）相比，DIFIX3D+在保持场景语义完整性的同时实现了更彻底的伪影消除。

**Figure 6** 展示了RDS自动驾驶场景的定性结果。DIFIX3D+有效修复了远距离物体（如远处车辆和交通标志）的模糊和变形，同时保持了道路标线和建筑结构的一致性。

---

### 多视图一致性评估

**Table S1** 使用TSED指标评估多视图一致性。DIFIX3D（无后处理）在一致性上显著优于直接DIFIX增强，接近基线水平。DIFIX3D+添加后处理步骤后，TSED略有下降但仍保持较高水平，验证了渐进式蒸馏对维持几何一致性的关键作用。

---

### 推理效率

DIFIX作为单步扩散模型，在NVIDIA A100上推理仅需**76毫秒**，比标准多步扩散模型快10倍以上。这使DIFIX3D+的推理时后处理步骤可以实时运行，不影响交互式应用。

---

### 失败模式与局限

1. **初始重建依赖性**：DIFIX3D+的性能受限于初始3D重建质量。对于重建完全失败的视角（如大面积缺失区域），DIFIX的增强能力有限——扩散模型可以修补小范围伪影，但无法凭空生成合理的几何结构。

2. **长程一致性**：DIFIX基于单步图像扩散模型，虽然渐进式蒸馏缓解了多视图不一致问题，但在极端视角变化下仍可能出现轻微的外观漂移。这提示未来工作可探索视频扩散模型以增强长上下文3D一致性。

3. **数据构建成本**：DIFIX的训练需要为每个场景域构建配对数据集（**Table 1**），涉及稀疏重建、循环重建、交叉参考和欠拟合训练等多种策略。虽然这些策略是自动化的，但数据构建过程增加了方法部署的工程复杂度。

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/004_Table_1.jpg]]
*Table 1: Data curation. We curate a paired dataset featuring common artifacts in novel-view synthesis. For DL3DV scenes [23], we employ sparse reconstruction and model underfitting, while for internal real driving scene (RDS) data, we utilize cycle reconstruction, cross reference, and model underfitting techniques*

### 补充图表

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison on Nerfbusters and DL3DV datasets. The best result is highlighted in bold, and the second-best is underlined*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/010_Table_5.jpg]]
*Table 5: Ablation study of DIFIX components on Nerfbusters dataset. Reducing the noise level, conditioning on reference views, and incorporating Gram loss improve our model*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/013_Figure_8.jpg]]
*Figure 8: Qualitative ablation results of DIFIX3D+: The columns, labeled by method name, correspond to the rows in Tab. 4. Table 4. Ablation study of DIFIX3D+ on Nerfbusters dataset. We compare a Nerfacto baseline to: (a) directly running DIFIX on rendered views without 3D updates, (b) distilling DIFIX outputs via 3D updates in a non-incremental manner, (c) applying the 3D updates incrementally, and (d) add DIFIX as a post-rendering step*

![[assets/figures/papers/paper_list_l50_https_arxiv_org_abs_2503_01774/figures/015_Table.jpg]]
*Table: S1. Multi-view consistency evaluation on the DL3DV dataset. A higher TSED score indicates better multi-view consistency*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

当前基于NeRF和3DGS的新视图合成方法在远离训练视角的欠约束区域会产生严重伪影，表现为错误几何、缺失纹理和漂浮物。这些伪影的根源在于：稀疏输入条件下，3D表示缺乏足够的数据先验来推断合理的外观。**DIFIX3D+** 的核心设计动机正是利用2D扩散模型的强生成先验来补偿3D重建中的信息缺失，同时避免破坏多视图几何一致性。

### 方法在谱系中的位置

DIFIX3D+ 处于**2D先验增强3D重建**的方法谱系中，但其设计路径与现有工作存在本质差异：

**与基于扩散模型的方法对比：**
- **Nerfbusters** (Warburg et al., ICCV 2023) 利用3D扩散模型去除NeRF伪影，但3D扩散模型训练成本高、推理慢，且难以泛化到不同场景类型。DIFIX3D+ 采用单步2D扩散模型，推理仅需76毫秒（NVIDIA A100），速度提升超过10倍，且同一模型可同时处理NeRF和3DGS的伪影。
- 同期方法在训练时每步查询扩散模型（如SDS-based方法），DIFIX3D+ 仅在关键迭代节点进行增强和蒸馏，训练效率显著更高。

**与基于GAN的方法对比：**
- **GANeRF** 为每个场景单独训练一个GAN来增强真实性，计算开销大且缺乏跨场景泛化能力。DIFIX3D+ 通过预训练的单步扩散模型实现零样本泛化，无需场景级微调。

**与基于参考视图聚合的方法对比：**
- **NeRFLiX** (Zhou et al., CVPR 2023) 在推理时聚合邻近参考视图信息来改进新视图合成，但本质上仍依赖已有视图的像素级融合，对极端视角的泛化能力有限。DIFIX3D+ 通过扩散先验生成合理内容，而非简单插值。

**与基础重建方法的对比：**
- **Nerfacto** (Tancik et al., SIGGRAPH 2023) 和 **3DGS** (Kerbl et al., SIGGRAPH 2023) 是DIFIX3D+ 的直接增强对象。实验表明，在Nerfbusters数据集上，DIFIX3D+ 将Nerfacto的PSNR从17.29提升至18.32（+1.03 dB），FID从134.65降至49.44（约2.72倍改善）；将3DGS的PSNR从17.66提升至18.51（+0.85 dB），FID从113.84降至41.77（约2.73倍改善）。

### 关键技术决策的因果机制

1. **单步扩散与噪声水平τ=200的选择**：传统多步扩散模型（如Stable Diffusion）的推理速度无法满足实时需求。DIFIX3D+ 基于SD-Turbo构建单步模型，并通过实验确定τ=200为最佳噪声水平——高于此值会过度修改图像内容（改变场景语义），低于此值则伪影去除不充分。这一选择基于一个关键假设：NeRF/3DGS渲染图像的伪影分布与扩散模型训练时τ=200的噪声分布相似。

2. **渐进式3D更新的必要性**：消融实验（Table 4）表明，直接将DIFIX增强视图一次性注入训练集会显著恶化LPIPS和FID，因为扩散模型在不同视角可能产生不一致的增强结果。渐进式更新策略（每1.5k次迭代通过相机姿态扰动生成新视图并蒸馏）确保了3D表示在多视图约束下逐步扩展，维持几何一致性。

3. **推理时后处理的双重作用**：DIFIX在推理时作为实时神经增强器，可进一步去除渐进蒸馏后残留的微小伪影。这一步骤几乎不影响多视图一致性（Table S1的TSED指标验证），同时提升PSNR和SSIM。

### 适用边界与局限

**当前方法的适用边界：**
- 适用于稀疏输入场景和远离训练视角的新视图合成，在自然场景（DL3DV）和自动驾驶场景（RDS）上均验证有效。
- 需要预训练的3D表示作为起点（Nerfacto或3DGS），无法从零开始重建。
- 同一DIFIX模型可跨场景泛化，但训练数据需覆盖目标域（如自动驾驶场景需单独训练RDS版本的DIFIX）。

**已知局限：**
- **严重重建失败区域无效**：当初始3D重建在目标视角完全失败（如大面积空洞或完全错误的几何）时，DIFIX无法有效增强，因为扩散模型缺乏足够的上下文信息。
- **长程多视图一致性仍有提升空间**：尽管渐进式蒸馏显著改善了单帧直接增强的不一致性，但基于单步图像扩散模型的方法在长序列渲染中仍可能出现轻微的闪烁，这是2D先验注入3D表示的固有挑战。
- **未探索视频扩散模型**：当前方法仅使用图像扩散模型，若能扩展为单步视频扩散模型，有望进一步提升时间一致性和长上下文3D一致性。

### 开放问题

1. **如何处理3D重建完全失败的区域？** 当初始3D表示在目标视角存在大面积缺失时，当前的图像级增强无法填补这些区域。一个可能的方向是结合现代扩散模型的inpainting能力或3D-aware生成先验。

2. **能否将DIFIX扩展为单步视频扩散模型？** 视频扩散模型可以提供更强的时序一致性约束，若能实现单步推理，将有望从根本上解决长序列渲染中的多视图一致性问题。

3. **如何降低对初始3D重建质量的依赖？** 当前方法的性能上限受限于基础重建方法（Nerfacto/3DGS）的质量。探索扩散先验与3D重建的更深层次融合（如在3D表示优化过程中直接引入扩散引导）可能是一个有价值的方向。

## 原文 PDF

![[paperPDFs/CVPR_2025/Difix3D_Improving_3D_Reconstructions_with_Single_Step_Diffusion_Models.pdf]]
