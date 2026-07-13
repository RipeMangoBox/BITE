---
title: "MBA-SLAM: Motion Blur Aware Dense Visual SLAM with Radiance Fields Representation"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/MBA_SLAM_Motion_Blur_Aware_Dense_Visual_SLAM_with_Radiance_Fields_Representation.pdf
project_link: null
code_link: https://github.com/WU-CVGL/MBA-SLAM
aliases:
- MS
- MBA-SLAM
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 在SE(3)空间中对相机曝光期间的运动轨迹进行显式建模，以曝光开始和结束时刻的姿态 T_start 和 T_end 为参数，利用该轨迹将参考关键帧重新模糊以匹配当前模糊观测，从而在跟踪和建图中主动补偿运动模糊。
primary_logic: 将物理运动模糊形成模型集成到直接图像对齐和光度束调整中，把去模糊问题转化为重模糊问题，使得SLAM系统能够在严重运动模糊的视频输入下鲁棒地估计相机轨迹并重建清晰的、高逼真度的3D场景，同时不影响对清晰数据的性能。
claims:
- MBA-SLAM achieves the best tracking performance (ATE RMSE) on the ArchViz synthetic blur datasets for both NeRF and 3DGS variants, outperforming all prior dense visual SLAM method...
- Ablation studies confirm that the proposed fully CUDA-implemented frame-to-frame tracker significantly improves both tracking accuracy and mapping quality over frame-to-map baseli...
- MBA-SLAM surpasses state-of-the-art dense visual SLAM pipelines on standard sharp image datasets (Replica, ScanNet, TUM), demonstrating that the blur-aware formulation does not de...
- MBA-SLAM restores sharp, high-fidelity renderings from severe motion blur sequences, with PSNR significantly higher than competing methods on ArchViz.
---

# MBA-SLAM: Motion Blur Aware Dense Visual SLAM with Radiance Fields Representation

> [!tip] 核心洞察
> 将物理运动模糊形成模型集成到直接图像对齐和光度束调整中，把去模糊问题转化为重模糊问题，使得SLAM系统能够在严重运动模糊的视频输入下鲁棒地估计相机轨迹并重建清晰的、高逼真度的3D场景，同时不影响对清晰数据的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MBA-SLAM：运动模糊感知的密集视觉SLAM与辐射场表示 |
| 英文题名 | MBA-SLAM: Motion Blur Aware Dense Visual SLAM with Radiance Fields Representation |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2411.08279) · [Code](https://github.com/WU-CVGL/MBA-SLAM) · [paper](https://arxiv.org/abs/2409.06765) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | MBA-SLAM |
| Dataset | ArchViz-1, Replica Room0, Replica |

> [!tip] 效果简介
> - ArchViz-1 (synthetic blur) 上，ATE RMSE [cm] 0.68 (MonoGS-blur-ours f2f) vs 1.06 (MonoGS-blur f2m) (-0.38 cm)。
> - Replica Room0 (sharp) 上，ATE RMSE [cm] 0.31 (MonoGS-ours f2f) vs 0.42 (MonoGS f2m) (-0.11 cm)。
> - Replica (8 scenes, sharp) 上，Average ATE RMSE [cm] Ours-NeRF 0.41, Ours-GS 0.35 vs Best prior SOTA (see Table 4) (outperforms all)。

## 概要

### 问题瓶颈

密集视觉SLAM系统在理想条件下依赖光度一致性假设——即同一3D点在相邻帧中的投影应具有相同的亮度。然而，在手持设备、机器人高速运动或低光照长曝光场景中，相机运动模糊会系统性地破坏这一假设。具体表现为两个相互加剧的退化循环：**跟踪端**，模糊帧使得传统的单姿态估计难以收敛，导致相机轨迹漂移；**建图端**，错误的姿态进一步污染多视图几何一致性，使场景重建质量急剧下降。现有方法（如**CoSLAM**（Wang et al., CVPR 2023）、**ESLAM**（Johari et al., CVPR 2023）、**Point-SLAM**（Sandstrom et al., ICCV 2023）、**SplaTAM**（Keetha et al., CVPR 2024）、**MonoGS**（Matsuki et al., CVPR 2024）等）均假设输入为清晰图像，缺乏对运动模糊的显式建模，因此在模糊数据上性能严重退化甚至完全失效。

### 核心思路

MBA-SLAM的核心洞察在于**将物理运动模糊形成模型集成到SLAM的跟踪与建图两个阶段中**，将传统的“去模糊”问题转化为“重模糊”问题。具体而言：

- **运动轨迹建模**：放弃传统的单帧瞬时姿态假设，转而显式建模相机在曝光时间内的连续运动轨迹。轨迹由曝光起始时刻的姿态 $\mathbf{T}_{\mathrm{start}}$ 和结束时刻的姿态 $\mathbf{T}_{\mathrm{end}}$ 参数化，中间姿态通过SE(3)李代数上的线性插值获得：
  $$\mathbf{T}_t = \mathbf{T}_{\mathrm{start}} \cdot \exp\left( \frac{t}{\tau} \cdot \log( \mathbf{T}_{\mathrm{start}}^{-1} \cdot \mathbf{T}_{\mathrm{end}} ) \right)$$

- **跟踪端重模糊对齐**：跟踪器不再试图从模糊帧中恢复清晰图像，而是从场景表示中渲染参考关键帧的清晰视图，沿估计的轨迹生成 $n$ 个虚拟清晰图像并平均合成重模糊图像，直接与输入的模糊观测进行光度对齐。

- **建图端模糊感知束调整**：建图器同样利用模糊形成模型，在优化场景表示（三平面NeRF或3D高斯）和关键帧轨迹时，将合成模糊图像与真实模糊帧的差异作为光度损失的一部分。

### 方法定位

在方法谱系中，MBA-SLAM处于**密集视觉SLAM**与**运动模糊感知**的交叉点。它继承了基于辐射场表示的SLAM框架（如NeRF-based和3DGS-based SLAM），但通过引入物理模糊形成模型，将适用范围从清晰数据拓展到严重运动模糊场景。其跟踪模块源自**MBA-VO**，建图模块整合了**BAD-NeRF**和**BAD-Gaussians**的模糊感知束调整算法，三者融合构成完整的SLAM流水线。与纯去模糊后处理方案不同，MBA-SLAM在跟踪阶段就主动补偿模糊，避免了“先去模糊再SLAM”的误差累积。

### 主要结果

实验验证了MBA-SLAM的三大核心能力：

1. **模糊数据上的鲁棒跟踪**：在合成模糊数据集ArchViz上，MBA-SLAM的3DGS变体（frame-to-frame跟踪）取得了0.68 cm的ATE RMSE，显著优于MonoGS-blur的frame-to-map基线（1.06 cm），降幅达36%（Table 11）。NeRF变体同样在所有模糊序列上超越先前方法（Table 1, Fig. 4）。

2. **清晰数据上的性能无损**：在标准清晰数据集Replica（8个场景）上，MBA-SLAM的NeRF变体平均ATE RMSE为0.41 cm，3DGS变体为0.35 cm，均优于所有先前SOTA方法（Table 4）。在ScanNet和TUM RGB-D上也保持领先（Table 7），证明模糊感知设计不会损害清晰场景的性能。

3. **高质量去模糊渲染**：从严重运动模糊序列中恢复的清晰渲染图像，PSNR显著高于竞争方法（Table 2, Fig. 5），网格重建质量同样最优（Fig. 6）。

消融实验进一步揭示：全CUDA实现的帧到帧（frame-to-frame）跟踪器是性能提升的关键，在清晰和模糊数据上均显著优于传统的帧到地图（frame-to-map）方案（Table 10, Table 11）；虚拟图像数量 $n$ 增加可提升重建质量，但在 $n \geq 13$ 后趋于饱和（Table 12）；若不启用模糊建模（$n=1$），跟踪精度在模糊数据上大幅退化，验证了模糊形成模型集成的必要性（Table 9）。

### 局限与开放问题

MBA-SLAM当前依赖两姿态线性插值模型，可能难以捕捉长时间曝光下高度不规则的运动轨迹。3DGS版本建图速度仅1.97 FPS，远未达到实时性要求。系统仅支持RGB-D输入，且曝光时间需事先已知。开放问题包括：如何建模超出两姿态近似的复杂运动模糊；帧到帧跟踪器在极低纹理场景中的鲁棒性；以及虚拟图像数量的在线自适应调整策略。

### 运动模糊对视觉SLAM的根本挑战

密集视觉SLAM旨在从视频流中同时恢复相机运动轨迹和重建场景的3D表示。近年来，基于辐射场（NeRF）和3D高斯泼溅（3DGS）的表示方法极大地提升了建图的逼真度和几何精度。然而，这些方法普遍依赖一个隐含假设：输入图像是清晰的，光度一致性在帧间成立。当相机发生快速运动或场景光照不足导致曝光时间延长时，图像中产生严重的运动模糊，这一假设被彻底破坏。

运动模糊带来的核心瓶颈体现在两个层面。在**跟踪**端，模糊图像丢失了精确的像素对应关系，传统基于清晰图像的直接对齐方法难以准确恢复相机姿态，误差累积导致轨迹漂移甚至跟踪丢失。在**建图**端，模糊帧引入的多视图几何不一致性会污染场景表示优化，使重建结果出现重影、细节丢失和几何畸变。这两个问题形成恶性循环：跟踪不准导致建图质量下降，而劣化的地图又进一步恶化跟踪精度。

### 现有方法的缺口

当前主流的密集视觉SLAM方法在设计上并未显式处理运动模糊。基于NeRF的方法（如**CoSLAM**（Wang et al., CVPR 2023）、**ESLAM**（Johari et al., CVPR 2023））和基于3DGS的方法（如**SplaTAM**（Keetha et al., CVPR 2024）、**MonoGS**（Matsuki et al., CVPR 2024）、**Photo-SLAM**（Huang et al., CVPR 2024）、**RTG-SLAM**（Peng et al., SIGGRAPH 2024））均假设每帧对应一个瞬时的相机姿态，并在清晰图像上最小化光度误差。当输入变为模糊序列时，这些方法要么跟踪精度大幅下降，要么完全失效（部分方法在模糊数据集上直接崩溃，见Table 9中的✗标记）。

这一缺口的存在并非偶然。将运动模糊建模集成到SLAM管道中面临两个关键困难：一是需要在跟踪阶段估计曝光期间的连续运动而非单一姿态，二是需要将模糊图像形成模型嵌入到建图的光度束调整中，使优化目标与物理成像过程一致。

### 本文的动机与核心思路

MBA-SLAM的出发点是：**运动模糊不是需要事后去除的噪声，而是蕴含相机运动信息的物理信号**。如果能够显式建模模糊的形成过程，就可以在跟踪和建图中主动补偿模糊的影响，从模糊观测中恢复出清晰的场景表示和精确的运动轨迹。

核心思路是将物理运动模糊形成模型集成到SLAM的两个核心阶段：

1. **运动模糊感知的跟踪器**：不再估计单一的瞬时姿态，而是在SE(3)空间中对曝光期间的相机运动轨迹进行显式建模，以曝光开始和结束时刻的姿态 $T_{\text{start}}$ 和 $T_{\text{end}}$ 为参数。跟踪时，将参考关键帧的清晰渲染结果沿该轨迹重新模糊，与当前模糊观测对齐，从而将去模糊问题转化为重模糊问题。

2. **模糊感知的建图器**：在光度束调整中，沿每条关键帧的运动轨迹采样多个虚拟清晰视图，通过平均合成模糊图像，与真实模糊输入计算损失。场景表示和相机轨迹在统一的模糊形成模型下联合优化。

这一设计使得MBA-SLAM能够在严重运动模糊的视频输入下鲁棒地估计相机轨迹并重建清晰的、高逼真度的3D场景，同时不影响对清晰数据的性能——在标准清晰数据集上，MBA-SLAM同样超越了现有方法。

## 核心方法与创新机理

MBA-SLAM 的核心创新并非提出全新的SLAM架构，而是将**物理运动模糊成像模型**显式地嵌入到密集视觉SLAM的两个核心环节——跟踪与建图——之中，从而将传统SLAM中“去模糊”的隐式需求转化为“重模糊”的显式操作。这一范式转换使得系统能够在严重运动模糊的视频输入下保持鲁棒的位姿估计和高质量的清晰场景重建，同时不影响对清晰数据的处理性能。

### 创新一：将运动模糊从“干扰”转化为“信号”

传统密集视觉SLAM（如 **CoSLAM** (Wang et al., CVPR 2023)、**ESLAM** (Johari et al., CVPR 2023)、**SplaTAM** (Keetha et al., CVPR 2024) 等）基于光度一致性假设，即场景点在相邻帧间的像素强度保持不变。运动模糊破坏这一假设，导致跟踪精度急剧下降甚至完全失效。

MBA-SLAM 的核心洞察在于：**不去从模糊图像中恢复清晰图像（去模糊），而是从清晰参考帧出发，模拟模糊成像过程（重模糊），使其与观测到的模糊帧对齐**。这一“反向”策略将模糊从需要消除的噪声转变为包含相机运动信息的信号，从根本上解决了模糊与光度一致性假设之间的矛盾。

### 创新二：SE(3)空间中的连续运动轨迹建模

传统SLAM为每帧估计一个瞬时相机姿态。MBA-SLAM 将这一假设替换为**曝光时间内的连续运动轨迹**，以曝光开始时刻的姿态 $\mathbf{T}_{\mathrm{start}}$ 和结束时刻的姿态 $\mathbf{T}_{\mathrm{end}}$ 为参数，在SE(3)李代数中进行线性插值：

$$\mathbf{T}_t = \mathbf{T}_{\mathrm{start}} \cdot \exp\left( \frac{t}{\tau} \cdot \log( \mathbf{T}_{\mathrm{start}}^{-1} \cdot \mathbf{T}_{\mathrm{end}} ) \right)$$

这一建模直接对应了运动模糊的物理成因——曝光期间相机的连续运动。相较于单姿态假设，两姿态参数化在仅增加少量自由度的情况下，有效捕捉了曝光期间的相机运动，是后续重模糊操作和联合优化的几何基础。

### 创新三：跟踪中的“重模糊”直接图像对齐

传统跟踪器通过最小化清晰参考帧与当前清晰帧之间的光度误差来估计单个姿态。MBA-SLAM 的跟踪器则直接对齐**清晰参考关键帧的重模糊版本**与**真实模糊当前帧**（Section 3.2.3, Eq. 25）：

$$\hat{\mathbf{B}}_{\mathrm{cur}}(\mathbf{x}) = \frac{1}{n} \sum_{i=0}^{n-1} \mathbf{I}_{\mathrm{ref}}\left(\mathbf{x}_{\frac{i\tau}{n-1}}\right)$$

具体而言，跟踪器沿估计的相机轨迹渲染 $n$ 个虚拟清晰视图并取平均，合成重模糊图像，然后与输入模糊帧进行光度误差最小化。这一设计使得跟踪器能够主动补偿运动模糊，而非被动地受其干扰。

### 创新四：建图中的模糊感知光束法平差

传统建图器的光度损失在清晰渲染图像与清晰真值帧之间计算。MBA-SLAM 的建图器（NeRF或3DGS版本）则将这一损失替换为**合成模糊图像与观测模糊帧之间的光度损失**（Section 3.3.3, Eq. 37），同时保留深度、自由空间、SDF或正则化损失。

合成模糊图像同样通过沿相机轨迹平均虚拟清晰视图生成。建图过程中，场景表示（三平面NeRF或3D高斯）和关键帧轨迹被联合优化，使得场景重建和轨迹估计相互促进——准确的轨迹有助于生成更清晰的场景，而清晰的场景反过来提升轨迹估计精度。

### 创新五：全CUDA帧到帧跟踪器

消融实验（Table 10, Table 11）揭示了另一个关键创新：**全CUDA实现的帧到帧（frame-to-frame）跟踪器**。相较于传统SLAM中常见的帧到地图（frame-to-map）跟踪策略，帧到帧跟踪在清晰和模糊数据上均显著提升了跟踪精度（ATE RMSE）和建图质量（PSNR）。这一改进并非模糊场景的特化优化，而是一个通用的跟踪策略升级，使得MBA-SLAM在标准清晰数据集（Replica、ScanNet、TUM）上同样超越了现有方法（Table 4, Table 7）。

MBA-SLAM 的整体管道由两个核心模块构成：**运动模糊感知的跟踪器（Motion Blur Aware Tracker）** 和**模糊感知的建图器（Blur Aware Mapper）**，两者通过一个物理运动模糊形成模型紧密耦合。该管道以 RGB‑D 视频流为输入，输出相机轨迹与清晰的 3D 场景表示。

### 管道概览

如图 1 所示，系统工作流程如下：

1. **跟踪阶段**：给定一帧新的模糊图像，建图器首先从已构建的 3D 场景中渲染出上一关键帧对应的虚拟清晰图像。运动模糊感知跟踪器随后直接估计相机在曝光期间的运动轨迹，该轨迹由曝光开始时刻的姿态 $\mathbf{T}_{\mathrm{start}}$ 和结束时刻的姿态 $\mathbf{T}_{\mathrm{end}}$ 参数化。中间的相机姿态通过 SE(3) 空间中的线性插值获得。

2. **建图阶段**：建图器沿估计的相机轨迹生成 $n$ 个虚拟清晰视图，按照辐射场或高斯泼溅的标准渲染流程生成。随后，根据运动模糊的物理成像模型，将这些虚拟图像平均合成一张模糊图像。最后，通过最小化合成图像与输入数据之间的损失，联合优化场景表示和相机轨迹。

### 核心设计思路

MBA-SLAM 的核心洞察在于**将去模糊问题转化为重模糊问题**。传统 SLAM 方法假设输入图像是清晰的，当面对运动模糊时，光度一致性假设被破坏，导致跟踪和建图质量急剧下降。MBA-SLAM 反其道而行之：

- **跟踪器**不尝试从模糊帧中恢复清晰图像，而是将清晰的参考关键帧“重新模糊”，使其与当前模糊观测相匹配。这一设计将物理运动模糊形成模型集成到直接图像对齐中。
- **建图器**同样在光度束调整中引入模糊形成模型，通过合成模糊图像与真实模糊帧的对比来优化场景表示和关键帧轨迹。

### 模块关系

跟踪器与建图器之间形成闭环协作：跟踪器为建图器提供初始的相机轨迹估计，建图器在联合优化中进一步精化轨迹和场景表示，精化后的场景又为下一帧的跟踪提供更高质量的参考渲染。这种紧耦合设计使得系统能够在严重运动模糊的视频输入下鲁棒地估计相机轨迹并重建清晰的、高逼真度的 3D 场景。

### 双后端支持

MBA-SLAM 提供了两种可互换的场景表示后端：

- **NeRF 变体（Ours‑NeRF）**：基于三平面（tri‑plane）的神经辐射场，通过 SDF 约束保证几何一致性。
- **3DGS 变体（Ours‑GS）**：基于 3D 高斯泼溅的显式表示，支持全图像渲染，在渲染速度上具有优势。

两种变体共享相同的运动模糊感知跟踪器，仅在建图器的渲染和优化策略上有所差异。实验表明，该模糊感知框架在清晰数据集上不会降低性能，同时能在模糊数据集上显著超越现有方法。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/001_Figure_1.jpg]]
*Figure 1: The pipeline of MBA-SLAM. Our framework consists of blur aware tracking process and bundle adjustment deblurring mapping process. Tracking: Given the current blurry frame, the mapper first renders a virtual sharp image of the lastest blurry keyframe from the 3D scene. Our motion blur-aware tracker directly estimates the camera motion trajectory during the exposure time, represented by the camera positions at the start and end of the exposure*

### 3.1 运动模糊图像形成模型

MBA-SLAM 的核心思想是将物理运动模糊的形成过程显式地集成到 SLAM 的跟踪与建图模块中。系统首先对模糊图像的生成过程进行建模。

在相机曝光时间 $\tau$ 内，传感器持续接收光线，最终形成的模糊图像 $\mathbf{B}(\mathbf{x})$ 可以表示为曝光期间所有虚拟清晰图像 $\mathbf{I}_{\mathrm{t}}(\mathbf{x})$ 的积分：

$$\mathbf{B}(\mathbf{x}) = \phi \int_{0}^{\tau} \mathbf{I}_{\mathrm{t}}(\mathbf{x}) \mathrm{dt}$$

其中 $\phi$ 是归一化因子。为便于计算，该连续过程被离散化为 $n$ 个时间戳上的虚拟清晰图像的平均：

$$\mathbf{B}(\mathbf{x}) \approx \frac{1}{n} \sum_{i=0}^{n-1} \mathbf{I}_{\mathrm{i}}(\mathbf{x})$$

这一离散近似的精度取决于虚拟图像数量 $n$。消融实验（Table 12）表明，当 $n \geq 13$ 时，重建质量趋于饱和。该模型是整个系统的理论基石——系统并非试图从模糊图像中“去模糊”，而是主动“重模糊”参考关键帧以匹配当前模糊观测。

### 3.2 运动模糊感知的相机轨迹建模

传统 SLAM 假设每帧对应一个瞬时相机姿态，这在运动模糊场景下失效。MBA-SLAM 将每帧的相机运动建模为曝光期间的一条连续轨迹，由曝光开始时刻的姿态 $\mathbf{T}_{\mathrm{start}} \in SE(3)$ 和结束时刻的姿态 $\mathbf{T}_{\mathrm{end}} \in SE(3)$ 参数化。

曝光期间任意时刻 $t \in [0, \tau]$ 的相机姿态 $\mathbf{T}_t$ 通过在 SE(3) 李代数中进行线性插值获得：

$$\mathbf{T}_t = \mathbf{T}_{\mathrm{start}} \cdot \exp\left( \frac{t}{\tau} \cdot \log( \mathbf{T}_{\mathrm{start}}^{-1} \cdot \mathbf{T}_{\mathrm{end}} ) \right)$$

其中 $\exp(\cdot)$ 和 $\log(\cdot)$ 分别为 SE(3) 上的指数映射和对数映射。旋转部分的插值等价于四元数空间中的测地线插值：

$$\bar{\mathbf{q}}_t = \bar{\mathbf{q}}_{\mathrm{start}} \otimes \exp\left( \frac{t}{\tau} \cdot \log( (\bar{\mathbf{q}}_{\mathrm{start}})^{-1} \otimes \bar{\mathbf{q}}_{\mathrm{end}} ) \right)$$

这一两姿态线性插值模型是系统的核心控制旋钮——它将每帧的待估计参数量从 6 自由度扩展到 12 自由度，从而在曝光期间主动补偿运动模糊。该模型假设曝光期间运动近似匀速，对于高度不规则的运动可能精度下降，属于系统的已知局限性。

### 3.3 运动模糊感知跟踪器

跟踪器的任务是从当前模糊帧中估计相机轨迹参数 $\mathbf{T}_{\mathrm{start}}$ 和 $\mathbf{T}_{\mathrm{end}}$。与传统的直接图像对齐不同，MBA-SLAM 的跟踪器采用“重模糊”策略：将清晰的参考关键帧 $\mathbf{I}_{\mathrm{ref}}$ 沿候选轨迹重新模糊，与真实模糊帧 $\mathbf{B}_{\mathrm{cur}}$ 进行光度对齐。

具体而言，对于参考帧中的像素 $\mathbf{x}$，其在第 $i$ 个虚拟视图中的对应位置 $\mathbf{x}_{\frac{i\tau}{n-1}}$ 通过相机轨迹插值和投影几何计算得出。重模糊像素强度由 $n$ 个虚拟视图的平均值合成：

$$\hat{\mathbf{B}}_{\mathrm{cur}}(\mathbf{x}) = \frac{1}{n} \sum_{i=0}^{n-1} \mathbf{I}_{\mathrm{ref}}\big(\mathbf{x}_{\frac{i\tau}{n-1}}\big)$$

跟踪器通过最小化重模糊图像与真实模糊图像之间的光度误差来优化 $\mathbf{T}_{\mathrm{start}}$ 和 $\mathbf{T}_{\mathrm{end}}$。为简化计算，系统从当前模糊图像中选取局部图像块（而非从参考帧选取），这一策略的几何关系在 Fig. 2 和 Fig. 3 中详细说明。

虚拟相机姿态 $\mathbf{T}_i$ 由轨迹参数显式计算：

$$\mathbf{T}_{i} = \mathbf{T}_{\mathrm{start}} \cdot \exp\left( \frac{i}{n-1} \tau \cdot \log\left( \mathbf{T}_{\mathrm{start}}^{-1} \cdot \mathbf{T}_{\mathrm{end}} \right) \right)$$

该跟踪器完全基于 CUDA 实现，支持帧到帧（frame-to-frame）对齐。消融实验（Table 10, Table 11）表明，相比传统的帧到地图（frame-to-map）跟踪，帧到帧跟踪在清晰和模糊数据集上均显著提升了跟踪精度和建图质量。

### 3.4 运动模糊感知建图器

建图器的目标是在给定模糊观测和估计轨迹的条件下，联合优化场景表示与关键帧轨迹。建图损失同样基于运动模糊形成模型构建。

对于 NeRF 变体，总损失函数为：

$$\mathcal{L} = \lambda_c \mathcal{L}_c + \lambda_d \mathcal{L}_d + \lambda_{fs} \mathcal{L}_{fs} + \lambda_{sdf} \mathcal{L}_{sdf}$$

其中 $\mathcal{L}_c$ 为模糊感知的颜色损失——将沿轨迹渲染的虚拟清晰图像平均后与输入模糊帧比较；$\mathcal{L}_d$ 为深度损失；$\mathcal{L}_{fs}$ 为自由空间损失；$\mathcal{L}_{sdf}$ 为 SDF 正则化损失。3DGS 变体采用类似的模糊感知光度损失，配合深度和正则化项。

通过在建图损失中显式建模模糊形成过程，建图器能够在严重运动模糊的输入下恢复清晰的 3D 场景表示。当 $n=1$（即不建模模糊）时，跟踪精度在模糊数据集上显著退化（Table 9），验证了模糊形成模型集成的必要性。

## 实验与关键发现

### 运动模糊数据集上的跟踪与建图性能

MBA-SLAM 的核心优势在于对严重运动模糊的鲁棒处理。在合成模糊数据集 ArchViz 上，该方法在跟踪精度上显著超越所有先前稠密视觉 SLAM 方法。以 3DGS 变体为例，MonoGS-blur-ours (f2f) 在 ArchViz-1 上取得 0.68 cm 的 ATE RMSE，而 MonoGS-blur (f2m) 为 1.06 cm，绝对提升 0.38 cm（Table 11）。NeRF 变体同样表现优异，在 ArchViz 各序列上均取得最佳跟踪结果（Table 1, Fig. 4 轨迹可视化）。Fig. 4 展示了 MBA-SLAM 在极具挑战性的相机运动下估计出的精确轨迹，直观验证了方法的鲁棒性。

在渲染质量方面，MBA-SLAM 能够从严重模糊的输入中恢复出清晰、高保真的视图。在 ArchViz 数据集上，其渲染 PSNR 显著高于竞争方法（Table 2, Fig. 5）。Fig. 5 的定性对比显示，MBA-SLAM 恢复的图像细节清晰、边缘锐利，而其他方法（如 CoSLAM、ESLAM、Point-SLAM、SplaTAM）仍残留明显的模糊伪影。网格重建方面，Fig. 6 表明 MBA-SLAM 的 NeRF 和 3DGS 变体均优于对比方法，且隐式辐射场方法（CoSLAM、ESLAM）在网格质量上优于显式点方法（Point-SLAM、SplaTAM）。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative rendering results of different methods with synthetic ArchViz datasets. It demonstrates that MBA-SLAM can restore and render sharp images from blurry input and outperform other dense visual SLAMs. Best viewed in high resolution*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative mesh visualization of different methods with ArchViz-1 datasets. The result reveals that implicit Radiance Fields (e.g.CoSLAM, ESLAM) deliver better reconstruction mesh performance than explicit point based methods (i.e.Point-SLAM, SplaTAM). MBA-SLAM always achieves best performance, no matter Ours-NeRF or Our-GS. RTG-SLAM fails to reconstruct mesh*

在真实世界数据集上（TUM、ScanNet、自采 Realsense），MBA-SLAM 同样展现出优越的跟踪和渲染性能（Table 3, Fig. 7, Fig. 8）。值得注意的是，Photo-SLAM 在自采数据集的第一列出现了视角错误，归因于跟踪失败（Fig. 8 说明），这从侧面反映了运动模糊对传统 SLAM 方法的严重干扰。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative rendering results of different methods with the real public ScanNet and TUM RGB-D datasets. The experimental results demonstrate that our method achieves superior performance over prior methods on the real public dataset*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/012_Figure_8.jpg]]
*Figure 8: Qualitative rendering results of different methods with our real captured Realsense datasets. The experimental results demonstrate that our method achieves superior performance over prior methods on the real captured dataset as well. Note that the first column shows an incorrect view rendered by Photo-SLAM, attributed to a failure in tracking*

### 清晰数据集上的性能验证

一个关键问题是：模糊感知的建模是否会在清晰数据上引入性能退化？实验结果给出了否定的答案。在标准清晰数据集 Replica（8 个场景）上，MBA-SLAM 的 NeRF 变体平均 ATE RMSE 为 0.41 cm，3DGS 变体为 0.35 cm，均超越所有先前 SOTA 方法（Table 4）。在 Replica Room0 上，MonoGS-ours (f2f) 的 ATE RMSE 为 0.31 cm，而 MonoGS (f2m) 为 0.42 cm（Table 10）。这表明模糊感知框架不仅未损害清晰场景的性能，反而因改进的跟踪器设计而有所提升。

渲染和网格重建方面，MBA-SLAM 在 Replica 上同样表现最佳（Table 5, Table 6, Fig. 9）。Fig. 9 的网格可视化显示，RTG-SLAM 因渲染深度图存在大量空洞而产生不完整网格，而 MBA-SLAM 重建的网格完整且细节丰富。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2411_08279/figures/013_Figure_9.jpg]]
*Figure 9: Qualitative mesh visualization results of different methods with Replica datasets. It demonstrates MBA-SLAM surpasses other stateof-the-art dense visual SLAMs even on standard sharp datasets. Note that RTG-SLAM produces incomplete meshes due to the presence of numerous holes in the rendered depth maps*

### 消融实验与关键设计验证

**帧到帧 (f2f) vs. 帧到地图 (f2m) 跟踪器**：Table 10 和 Table 11 分别展示了在清晰和模糊数据集上的对比。全 CUDA 实现的 f2f 跟踪器在两类数据上均显著优于标准 f2m 跟踪器：在清晰数据上提升跟踪精度和建图质量，在模糊数据上优势更为突出。这验证了 f2f 设计对整体性能的关键贡献。

**模糊建模的必要性**：Table 9 对比了不使用模糊建模（n=1 虚拟图像）与完整方法。在 ArchViz-1 上，无模糊建模时跟踪精度大幅下降（Ours-NeRF* 和 Ours-GS*），部分基线方法（SplaTAM、RTG-SLAM）甚至完全无法运行（标记为 ✗）。这直接证明了将物理模糊形成模型集成到 SLAM 管道中的必要性。

**虚拟图像数量的影响**：Table 12 展示了虚拟图像数量 n 对 ArchViz-1 重建质量的影响。随着 n 增加，性能逐步提升，但在 n ≥ 13 时趋于饱和。论文选用 n=7（NeRF）和 n=13（3DGS）以平衡质量与速度。

### 效率与失败模式

**运行时效率**：Table 8 报告了 Replica Room0 上的运行时间和内存占用。Ours-NeRF 达到 22.57 FPS，具备实时性；Ours-GS 速度慢于 GS-SLAM 但快于 SplaTAM，建图速度为 1.97 FPS，仍远低于实时要求。NeRF 方法在跟踪和建图中仅采样部分像素，而 3DGS 方法使用全图渲染，导致不同的速度-质量权衡。

**已知局限**：(1) 两姿态线性插值模型可能难以捕捉长时间曝光下高度不规则的运动轨迹，高非线性运动时精度可能下降；(2) 3DGS 版本的建图速度远低于实时，限制了在线机器人应用；(3) 仅支持 RGB-D 输入，尚未扩展到单目或立体设置；(4) 曝光时间需事先已知或通过传感器获取，实际应用中可能无法准确获得。

## 定位与知识库关联

### 1. 核心继承与组件来源

MBA-SLAM 并非从零构建，而是将两个既有模块——运动模糊感知的视觉里程计前端与运动模糊感知的光束法平差后端——整合为完整的 SLAM 管线。具体而言，其跟踪器继承自 **MBA-VO**，建图器则分别基于 **BAD-NeRF** 和 **BAD-Gaussians** 的光束法平差去模糊算法。论文明确声明：“we integrate them into a comprehensive SLAM pipeline, by exploiting the motion blur aware tracker from MBA-VO and the motion blur aware bundle adjustment algorithm from either BAD-NeRF or BAD-Gaussians ”。这一集成策略使得系统既能利用 VO 前端的高效帧间对齐，又能借助后端 BA 的全局一致性优化，形成闭环。

### 2. 与现有密集视觉 SLAM 的关系

MBA-SLAM 的直接对比对象覆盖了当前密集视觉 SLAM 的两大主流技术路线：基于 NeRF 的方法和基于 3DGS 的方法。

**NeRF-based 基线：**
- **CoSLAM** (Wang et al., CVPR 2023)：联合坐标与稀疏体素网格的 NeRF SLAM。
- **ESLAM** (Johari et al., CVPR 2023)：基于三平面特征的高效 NeRF SLAM。
- **Point-SLAM** (Sandstrom et al., ICCV 2023)：神经点云表示，渲染质量高但建图优化极慢（超过 CoSLAM 和 ESLAM 的 30 倍）。

**3DGS-based 基线：**
- **SplaTAM** (Keetha et al., CVPR 2024)：首个基于 3D Gaussian Splatting 的密集 SLAM。
- **MonoGS** (Matsuki et al., CVPR 2024)：单目 3DGS SLAM，本文将其扩展为 RGB-D 版本作为基线。
- **Photo-SLAM** (Huang et al., CVPR 2024)：融合光度信息的 3DGS SLAM。
- **RTG-SLAM** (Peng et al., SIGGRAPH 2024)：实时 Gaussian SLAM。

上述所有方法均假设输入为清晰图像，在运动模糊场景下其光度一致性假设被破坏，导致跟踪失败或精度严重退化。MBA-SLAM 的核心区分点在于：**将物理运动模糊形成模型显式集成到直接图像对齐和光度束调整中**，从而在模糊输入下仍能保持鲁棒性。

### 3. 关键设计差异：三个改变的方法槽位

MBA-SLAM 相对于上述基线，在三个关键方法槽位上做出了根本性改变：

**槽位一：跟踪器光度对齐目标**
- **基线做法**：估计单一瞬时姿态，通过最小化清晰参考帧与当前帧之间的光度误差来优化（标准直接法，如 Eq. 3）。
- **MBA-SLAM 做法**：将清晰参考帧与自身经重模糊后的版本对齐，以匹配真实模糊帧，优化目标变为曝光起始姿态 $T_{\text{start}}$ 和结束姿态 $T_{\text{end}}$（Eq. 25）。这一“去模糊→重模糊”的策略转换是系统在模糊输入下鲁棒跟踪的根本保障。

**槽位二：相机运动模型**
- **基线做法**：每帧仅估计一个瞬时姿态。
- **MBA-SLAM 做法**：采用 SE(3) 空间中的连续轨迹模型，以 $T_{\text{start}}$ 和 $T_{\text{end}}$ 参数化曝光期间的相机运动，并通过李代数线性插值生成中间姿态（Eq. 5）：
  $$\mathbf{T}_t = \mathbf{T}_{\mathrm{start}} \cdot \exp\left( \frac{t}{\tau} \cdot \log( \mathbf{T}_{\mathrm{start}}^{-1} \cdot \mathbf{T}_{\mathrm{end}} ) \right)$$

**槽位三：建图光度损失**
- **基线做法**：在清晰渲染图像与清晰真值帧之间计算颜色损失。
- **MBA-SLAM 做法**：沿相机轨迹生成 $n$ 个虚拟清晰视图，平均后合成模糊图像，再与真实模糊帧计算颜色损失（Eq. 37），同时结合深度、自由空间和 SDF（或 3DGS 的深度/正则化）损失进行联合优化。

### 4. 适用边界与局限

**输入模态限制**：当前仅支持 RGB-D 输入，尚未扩展到单目或立体设置。深度信息在重模糊像素合成和建图损失中起关键作用，缺乏深度将显著增加模糊下的歧义性。

**运动模型假设**：两姿态线性插值模型假设曝光期间相机运动是平滑且近似线性的。对于长时间曝光或高度不规则的运动轨迹（如剧烈抖动、急转弯），该近似可能不足以捕捉真实运动，导致精度下降。论文未提供针对非线性运动的定量分析。

**实时性差距**：尽管 NeRF 版本达到 22.57 FPS 的跟踪速度，3DGS 版本的建图速度仅为 1.97 FPS，远低于实时要求。这限制了其在在线机器人应用中的部署，尤其是在需要即时地图更新的场景中。

**曝光时间先验**：模糊形成模型需要已知曝光时间 $\tau$。论文假设该参数可通过传感器获取或事先标定，但在实际应用中（如卷帘快门相机、自动曝光场景），准确获取曝光时间可能困难。

**极端低纹理场景**：帧到帧跟踪器依赖局部图像块的光度信息。在纹理极少的场景（如空白墙壁），光度梯度消失可能导致跟踪退化，但论文未对此进行专项消融。

### 5. 开放问题

1. **连续运动模型的扩展能力**：当前两姿态线性插值模型能否通过引入更高阶的 B-spline 或连续时间轨迹表示来处理大幅或非均匀运动模糊？这需要重新推导 Jacobians 并评估计算开销。

2. **Photo-SLAM 跟踪失败的根因**：在 Fig. 8 第一列中，Photo-SLAM 渲染了错误视角，论文归因于跟踪失败。但具体是初始化问题、对模糊的过度敏感，还是其光度模型在模糊下的固有缺陷，仍需深入分析。

3. **虚拟图像数量的自适应机制**：消融实验表明 $n \geq 13$ 后性能饱和（Table 12），但固定 $n$ 在轻度模糊时造成冗余计算，在重度模糊时可能不足。能否根据运动幅度或图像模糊程度在线自适应调整 $n$，以动态平衡质量与速度？

4. **与事件相机的互补性**：事件相机天然对运动模糊鲁棒，MBA-SLAM 的模糊感知框架能否与事件数据融合，在极端运动场景下进一步提升鲁棒性？这是一个有前景但尚未探索的方向。

5. **大场景的扩展性**：当前实验主要在房间级场景（Replica、ScanNet）上进行。在更大尺度场景中，SE(3) 插值的累积误差和 3DGS 的内存增长是否会成为瓶颈，仍需验证。

## 原文 PDF

![[paperPDFs/arxiv_2024/MBA_SLAM_Motion_Blur_Aware_Dense_Visual_SLAM_with_Radiance_Fields_Representation.pdf]]
