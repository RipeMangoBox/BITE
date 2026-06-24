---
title: "AC3D: Analyzing and Improving 3D Camera Control in Video Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.pdf
aliases:
- AA3CC
- AC3D
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过三个关键设计限定相机控制的作用域：① 将相机条件注入限制在反向扩散前40%的时间步（低频生成阶段）；② 仅将相机条件注入前8个DiT块（浅层），避免干扰高层视觉特征；③ 使用20K动态但固定相机的视频补充训练数据，解耦相机运动与场景动态。"
primary_logic: "视频扩散模型在去噪早期即确定相机运动（低频信号），且模型内部隐式编码了相机姿态知识（集中于中间层）。因此只需在早期时间步和浅层注入相机条件即可实现精确可控，同时不影响高频视觉细节，从而突破相机控制与画质/动态性之间的权衡。"
claims:
- "相机运动主要为低频信号，在去噪过程的前10%时间步（t=0.9）即已完全生成，而高频细节直到t=0.5才明确。"
- "将训练与推理的噪声/相机条件限制在 [0.6,1] 区间（前40%去噪步）使视觉保真度指标FID/FVD平均提升14%，MSR‑VTT上相机跟随度提升30%。"
- "线性探测证实VDiT中间层隐式编码了精确的相机姿态（旋转误差0.025，平移误差0.48），信息在#9‑#21层达到峰值。"
- "仅将相机条件注入前8个DiT块使训练参数量减少约4倍，训练/推理加速15%，视觉质量提升10%。"
---

# AC3D: Analyzing and Improving 3D Camera Control in Video Diffusion Transformers

> [!tip] 核心洞察
> 视频扩散模型在去噪早期即确定相机运动（低频信号），且模型内部隐式编码了相机姿态知识（集中于中间层）。因此只需在早期时间步和浅层注入相机条件即可实现精确可控，同时不影响高频视觉细节，从而突破相机控制与画质/动态性之间的权衡。

| 字段      | 内容                                                                                                      |
| ------- | ------------------------------------------------------------------------------------------------------- |
| 中文题名    | AC3D：视频扩散变换器中三维相机控制的分析与改进                                                                               |
| 英文题名    | AC3D: Analyzing and Improving 3D Camera Control in Video Diffusion Transformers                         |
| 会议/期刊   | CVPR 2025                                                                                               |
| Links   | [paper](https://arxiv.org/abs/2411.18673); [Project](https://snap-research.github.io/ac3d)              |
| Topic   | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method  | AC3D (Advanced 3D Camera Control)                                                                       |
| Dataset | RealEstate10K                                                                                           |

> [!tip] 效果简介
> - RealEstate10K 上，TransErr 为 0.358，对比 0.421，变化 -0.063。
> - RealEstate10K 上，RotErr 为 0.035，对比 0.056，变化 -0.021。
> - RealEstate10K 上，FID 为 1.18，对比 1.21，变化 -0.03。

## 概述

视频扩散模型为文本到视频生成带来了革命性进展，但精确控制生成视频中的三维相机运动仍是一个核心挑战。现有相机控制方法普遍面临一个根本性权衡：**提升相机姿态跟随精度会严重损害合成内容的视觉质量与场景动态性**。AC3D通过系统分析这一问题的深层原因，提出了一套简洁而高效的解决方案。

**瓶颈诊断。** 研究发现，上述权衡的根源来自两个层面。其一，相机运动本质上是一种**低频信号**——在扩散去噪过程的前10%时间步（t=0.9附近）即已完全生成，而高频视觉细节直到t=0.5才逐渐明确（Figure 4）。现有方法将相机条件注入全部时间步，导致后期去噪阶段的高频细节生成受到不必要的干扰。其二，主流训练数据（RealEstate10K）几乎全部由**静态场景**构成，模型因此将相机运动条件与场景静止强关联，在遇到动态场景时无法兼顾相机跟随与画面动感。

**核心洞察。** 线性探测实验进一步揭示，冻结的大规模视频扩散Transformer（VDiT）内部隐式编码了精确的相机姿态知识——旋转误差仅0.025，平移误差0.48，且该信息集中于中间层（#9–#21层）达到峰值（Figure 5）。这意味着模型在浅层即可完成相机姿态的解析与传递，深层应专注于视觉渲染。

**方法定位。** 基于上述分析，AC3D通过三个关键设计限定相机控制的作用域，从而突破精度与质量之间的权衡：

1. **时间域截断**：将训练噪声采样和推理时的相机条件注入限制在反向扩散的前40%时间步（[0.6, 1]区间），仅在低频生成阶段施加控制。
2. **空间域截断**：仅将相机条件注入前8个DiT块（浅层），后24个块不受相机条件影响，使深层专注于高频视觉特征合成。
3. **数据去偏**：额外采集20K动态场景但固定相机的视频，解耦相机运动与场景静止的虚假关联。

**主要结果。** 在分布内（RealEstate10K）和分布外（MSR-VTT）基准上，AC3D在相机姿态误差与视觉保真度指标上均显著超越现有方法。具体而言，与强基线VD3D（DiT）相比，MSR-VTT上FID改善22%（6.88→5.34），FVD改善20%（137.62→110.71），同时TransErr降低12%（0.486→0.428）。用户研究进一步表明，AC3D生成的视频在90%的情况下被参与者偏好，在相机对齐、运动质量、文本对齐和视觉质量四个维度上均占优（Table 1）。

**方法谱系与知识库定位。** AC3D建立在冻结的VDiT主干（11.5B参数，32个DiT块）之上，采用ControlNet风格的轻量级相机分支进行条件注入。与现有相机控制方法相比，**MotionCtrl**和**CameraCtrl**基于U‑Net架构，**VD3D**则探索了FIT主干及ControlNet方案；AC3D的独特贡献在于**从信号频谱角度重新审视条件注入的时空范围**，而非设计更复杂的条件编码器或注入机制。该分析框架具有普适性——在CogVideoX上的补充实验验证了相机运动低频偏重的结论跨架构成立（Figure 7, Figure 8）。

## 背景与动机

视频生成模型近年来取得了显著进展，特别是基于扩散Transformer（DiT）的大规模文本到视频模型，已能合成具有丰富视觉细节和复杂场景动态的高质量视频。然而，将这些预训练模型转化为精确可控的创作工具仍面临关键挑战：**如何在引入相机控制的同时，不损害合成内容的视觉质量与场景动态性？**

### 问题现状：相机控制的精度-质量权衡

现有相机控制方法（如基于U-Net的**MotionCtrl**、**CameraCtrl**，以及基于FIT主干和ControlNet的**VD3D**）通常采用标准的ControlNet范式：将相机姿态条件通过额外分支注入预训练视频扩散模型的所有层和全部去噪时间步。这种“全范围注入”策略虽然实现了基本的相机跟随能力，但存在两个严重缺陷：

1. **视觉质量退化**：相机条件的过度注入干扰了模型原有的视觉特征生成过程，导致合成视频出现模糊、伪影和纹理失真。
2. **场景动态性丧失**：模型倾向于将相机运动与场景静止强关联，使得受控生成的视频中物体运动显著减少，场景变得“死寂”。

这种精度-质量权衡构成了当前视频扩散模型相机控制的核心瓶颈。

### 根本原因分析

AC3D通过系统的实证分析，揭示了上述瓶颈的三个深层原因：

**原因一：相机运动是低频信号，在去噪早期即已确定。** 通过对生成视频的运动频谱分析（Figure 3），研究发现相机运动诱导的光流变化主要集中在低频分量，其能量远高于纯场景运动。更重要的是，在反向扩散过程中，相机运动在极早期时间步（$t=0.9$，即前10%的去噪步）就已完全涌现，而高频视觉细节直到$t=0.5$才逐渐明确（Figure 4）。这意味着在去噪后期注入相机条件不仅多余，而且会与正在形成的高频细节产生冲突。

**原因二：视频DiT内部隐式编码了相机姿态知识。** 线性探测实验（Figure 5）表明，冻结的VDiT主干在中间层（#9-#21层）能够以极高精度预测相机姿态（旋转误差0.025，平移误差0.48）。这说明相机信息在模型浅层即被提取，用于指导中深层渲染与视点对齐的视觉特征。因此，将相机条件注入全部32个DiT块是冗余的——深层块需要的是不受干扰的视觉渲染空间。

**原因三：训练数据的静态场景偏置。** 主流的相机控制训练集RealEstate10K包含65K视频，虽然相机轨迹多样，但场景几乎全部为静态（Figure 6上两行）。模型从这种数据中学习到的关联是：“有相机运动 → 场景静止”。当面对分布外的动态场景文本提示时，模型会错误地抑制场景运动以“服从”相机条件，导致动态性丧失。

### 本文动机与核心思路

基于上述分析，AC3D提出了一条突破精度-质量权衡的新路径：**通过精确限定相机控制的作用域，使相机条件仅在必要的时空范围内生效，从而释放模型的视觉生成能力。** 具体而言，三个关键设计构成了方法的核心：

- **时间域限定**：将相机条件注入限制在反向扩散的前40%时间步（$t \in [0.6, 1]$），仅覆盖低频生成阶段。
- **空间域（层）限定**：仅将相机条件注入前8个DiT块，让后24个块专注于不受干扰的视觉特征渲染。
- **数据域解耦**：引入20K动态场景但固定相机的视频作为补充训练数据，显式解耦相机运动与场景动态的虚假关联。

这一框架不仅实现了更精确的相机控制（相机跟随度提升30%），同时显著改善了视觉质量（FID/FVD平均提升14%）和场景动态性（分布外FID改善17%），从根本上解决了现有方法的权衡困境。

## 核心创新

AC3D的核心创新在于**重新定义了相机控制信号在视频扩散模型中的作用域**，而非设计新的条件注入模块。通过对VDiT内部相机知识表征与扩散过程动态的深入分析，该方法揭示了现有相机控制方法性能瓶颈的根本原因，并据此提出了三个精准的“作用域裁剪”策略，在相机跟随精度与视觉质量之间实现了突破性的权衡。

### 瓶颈诊断：相机控制为何损害画质与动态性

现有基于ControlNet的相机控制方法（如**VD3D (DiT)**、**MotionCtrl (VDiT)**、**CameraCtrl (VDiT)**）面临一个根本性矛盾：注入相机条件虽能引导相机运动，却会显著降低生成内容的视觉保真度与场景动态性。AC3D通过两组分析实验定位了该矛盾的深层原因：

1. **信号频率错配**：对VDiT生成视频的运动频谱分析（Figure 3, 4）表明，相机运动本质上是**低频信号**——其频谱能量主要集中在低频分量，且在去噪过程的前10%时间步（t=0.9）即已完全涌现，而高频纹理细节直到t=0.5才逐步清晰。现有方法将相机条件注入整个去噪过程，导致在后期高频生成阶段施加了不必要的低频约束，干扰了视觉细节的合成。

2. **隐式相机知识的层次化分布**：对VDiT各层进行线性探测（Figure 5）发现，模型内部已隐式编码了精确的相机姿态信息——旋转误差低至0.025，平移误差低至0.48，且该信息在中间层（#9–#21）达到峰值。这表明相机信号在浅层即已充分提取，深层主要负责与相机视角对齐的视觉特征渲染。现有方法将相机条件注入所有32个DiT块，过度约束了深层的视觉合成过程。

3. **静态场景偏差**：主流训练数据RealEstate10K（65K视频）几乎全部为静态场景，导致模型将相机运动条件与场景静止强关联。当面对包含动态内容的分布外文本提示时，模型倾向于抑制场景运动以匹配这一虚假相关性。

### 三个关键作用域裁剪

基于上述诊断，AC3D通过三个精准的“changed slots”限定相机控制的作用边界，从根本上解耦相机运动与视觉质量：

**① 时间步截断：仅在前40%去噪步注入相机条件**

将训练噪声分布从标准logit-normal（loc=0, scale=1，覆盖全时间步）改为截断正态分布（loc=0.8, scale=0.075，仅采样[0.6, 1]区间），并在推理时仅在对应时间步注入相机条件。这一设计基于“相机运动在去噪早期即已确定”的发现，避免在后期高频生成阶段施加冗余约束。消融实验（Table 2）证实：不偏置噪声分布（w/o biasing noise）使MSR-VTT上FVD增加16.92；不截断时间步（w/o noise truncation）使FVD增加6.63。

**② 层范围限制：仅注入前8个DiT块**

将相机条件注入从全部32个DiT块缩减至前8个块，后24个块完全不受相机条件影响。这一设计基于线性探测揭示的“相机知识集中于浅中层”的发现，使深层能够专注于与相机视角对齐的视觉特征渲染。该策略带来三重收益：训练参数量减少约4倍，训练/推理速度提升约15%，视觉质量提升10%（Table 2）。

**③ 动态固定相机数据注入：解耦相机运动与场景动态**

在RealEstate10K基础上补充20K动态场景但固定相机的视频，打破“相机运动→场景静止”的虚假相关性。消融实验（Table 2）表明，移除该数据（w/o our dynamic data）使分布外MSR-VTT上FID增加0.89、FVD增加4.40，证实了数据偏差校正对分布外泛化的关键作用。

### 辅助设计：独立CFG与上下文隔离

除三个主要作用域裁剪外，AC3D还引入两项辅助设计以进一步解耦控制信号：

- **独立分类器自由引导**：为文本和相机条件分别设置独立的CFG权重，合成时的最终更新方向为：
  $$\hat{s}(\pmb x | \pmb t, \pmb c) = (1 + w_y + w_c) s_{\theta}(\pmb x | \pmb t, \pmb c) - w_y s_{\theta}(\pmb x | \pmb c) - w_c s_{\theta}(\pmb x | \pmb t)$$
  消融实验表明移除相机CFG（w/o camera CFG）使RE10K上TransErr增加0.014。

- **相机分支上下文隔离**：不将文本嵌入、分辨率条件等上下文信息输入相机处理分支，避免上下文信息干扰相机表示。消融实验（w/o dropping camera context）使MSR-VTT上FVD增加7.41，验证了隔离的必要性。

### 创新本质总结

AC3D的创新不在于提出新的条件注入机制，而在于**通过分析VDiT内部表征与扩散动态，揭示了相机控制的“最小充分作用域”**——仅需在去噪早期的浅层注入相机条件即可实现精确可控。这一“减法式”设计哲学直接回应了相机控制与视觉质量之间的根本性权衡，使AC3D在相机跟随精度（TransErr降低15%）与视觉保真度（FID/FVD平均改善14%）两个维度上同时超越强基线VD3D (DiT)。

## 整体框架

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/001_Figure_1.jpg]]
*Figure 1: Camera-controlled video generation. Our method enables precise camera controllability in pre-trained video diffusion transformers, allowing joint conditioning of text and camera sequences. We synthesize the same scene with two different camera trajectories as input. The inset images visualize the cameras for the videos in the corresponding columns. The left camera sequence consists of a rotation to the right, while the right camera visualizes a zoom-out and up trajectory*

AC3D 的整体 pipeline 围绕一个冻结的大规模文本到视频扩散 Transformer（VDiT Backbone，11.5B 参数，32 个 DiT 块，隐维度 4096）构建，通过轻量级的 ControlNet 风格相机分支实现精确的 3D 相机控制。其核心设计理念源于一个关键发现：相机运动作为低频信号，在去噪过程的前 10% 时间步即已基本生成，且 VDiT 的中间层隐式编码了准确的相机姿态知识。因此，AC3D 将相机条件的作用域严格限定在早期去噪步和浅层网络，从而在实现精确可控的同时避免损害视觉质量与场景动态性。

### 输入输出流

系统的输入包括三部分：
- **文本提示**：描述场景内容的自然语言，经由冻结的 VDiT 文本编码器处理为上下文嵌入。
- **相机轨迹**：一段帧级相机外参/内参序列，首先映射为 Plücker 坐标表示，再通过全卷积编码器投影到与视频 token 相同的维度和分辨率，生成相机 token。
- **初始噪声**：从偏置且截断的正态分布（loc=0.8, scale=0.075，采样区间 [0.6, 1]）中采样的噪声，仅覆盖反向扩散过程的前 40% 时间步。

输出为一段与指定相机轨迹精确对齐的生成视频。

### 模块架构与数据流

AC3D 的模块关系与数据流如下：

1. **Plücker 相机编码器**：将输入的相机外参/内参序列转换为 Plücker 坐标，并通过全卷积编码器生成与视频潜在空间分辨率和维度对齐的相机 token。

2. **1D 时序相机编码器**：采用因果 1D 卷积将帧级 Plücker 坐标序列（F×6）转换为匹配潜在空间时间分辨率的表示（F/4×32），确保时序一致性。

3. **Camera DiT-XS 块**：一系列轻量级 Transformer 块（隐维度 128，4 个注意力头），专门处理相机信息。这些块与主 VDiT 的 DiT-XL 块（隐维度 4096）形成鲜明对比，体现了“重主干、轻分支”的设计哲学。

4. **条件注入（求和）**：在每个主 DiT 块前，将相机 token 与视频 token 通过求和操作混合。**关键设计**：相机条件仅注入前 8 个 DiT 块，后 24 个块完全不受相机条件影响。这一设计基于线性探测的发现——VDiT 中间层（#9-#21）隐式编码了最精确的相机姿态（旋转误差 0.025，平移误差 0.48），因此只需在浅层提供相机信号，深层即可自行完成视角对齐的视觉渲染。

5. **交叉注意力反馈**：从视频 token 向相机 token 的交叉注意力连接，形成双向信息流，使相机表示能够感知视频内容的变化。

6. **独立 CFG 模块**：合成阶段采用独立的文本和相机分类器自由引导权重，最终更新方向为：

   $$\hat{s}(\pmb x | \pmb t, \pmb c) = (1 + w_y + w_c) s_{\theta}(\pmb x | \pmb t, \pmb c) - w_y s_{\theta}(\pmb x | \pmb c) - w_c s_{\theta}(\pmb x | \pmb t)$$

   其中 $w_y$ 和 $w_c$ 分别为文本和相机的引导权重，允许独立调节文本对齐与相机跟随的强度。

### 训练数据构成

AC3D 的训练数据由两部分组成：
- **RealEstate10K**（65K 视频）：提供多样化的相机轨迹，但场景几乎全部为静态，导致基线模型将相机条件与场景静止强关联。
- **自采动态固定相机视频**（20K 视频）：场景动态丰富但相机静止的视频，用于解耦相机运动与场景动态，显著改善分布外泛化能力（MSR-VTT 上 FID 改善 17%，FVD 改善 4%）。

### 与基线方法的架构差异

相较于将 VD3D 或 MotionCtrl/CameraCtrl 移植到 VDiT 主干的基线方法，AC3D 的核心架构差异在于**作用域限定**而非模块替换：
- 基线方法通常向所有 32 个 DiT 块注入相机条件，并在全时间步范围内进行条件控制；
- AC3D 将条件注入限定在前 8 个块和前 40% 去噪步，使训练参数量减少约 4 倍，训练与推理加速约 15%，同时视觉质量提升约 10%。

## 核心模块与公式推导

### 整体架构：VDiT‑CC

AC3D 构建于冻结的大规模视频扩散 Transformer（VDiT，11.5B 参数，32 个 DiT 块，隐维度 4096）之上，采用 ControlNet 风格的轻量级分支注入相机条件。该分支由三个核心模块串联构成：

- **Plücker Camera Encoder**：将帧级相机外参/内参映射为 Plücker 坐标（$F \times 6$），经全卷积编码器投影至与视频 token 相同的维度和分辨率，生成相机 token。
- **Camera DiT‑XS Blocks**：一系列轻量 Transformer 块（隐维度 128，4 个注意力头），专门处理相机信息，与主干的 DiT‑XL 块（隐维度 4096）形成鲜明对比。
- **Condition Injection (Summation)**：在每个受控的 DiT 块前，将相机 token 与视频 token 直接相加混合，实现条件注入。

此外，AC3D 引入了**Cross‑Attention Feedback**：从视频 token 向相机 token 的交叉注意力，形成双向反馈连接，增强相机表示与视频内容的交互。值得注意的是，相机分支**不接收上下文信息**（文本嵌入、分辨率条件等），消融实验表明输入上下文会干扰相机表示，导致 MSR‑VTT 上 FVD 增加 7.41。

### 独立分类器自由引导（Separate CFG）

AC3D 为文本和相机条件分别设置独立的引导权重，合成时的最终更新方向为：

$$\hat{s}(\pmb x | \pmb t, \pmb c) = (1 + w_y + w_c) s_{\theta}(\pmb x | \pmb t, \pmb c) - w_y s_{\theta}(\pmb x | \pmb c) - w_c s_{\theta}(\pmb x | \pmb t)$$

其中 $\pmb x$ 为噪声潜在表示，$\pmb t$ 为文本条件，$\pmb c$ 为相机条件，$w_y$ 和 $w_c$ 分别为文本和相机的引导权重。消融实验证实，移除相机 CFG（$w_c = 0$）会导致 RE10K 上 TransErr 增加 0.014，相机跟随精度下降。

### 度量尺度重标定

RealEstate10K 的 COLMAP 重建与真实度量尺度之间存在不一致，直接使用会影响相机轨迹的绝对精度。AC3D 通过优化缩放因子 $\hat{\lambda}$ 进行重标定：

$$\hat{\lambda} = \arg\min_{\lambda} \mathbb{E}_{f \sim F} | \lambda D_c^{f} - D_m^{f} |$$

其中 $D_c^{f}$ 和 $D_m^{f}$ 分别为帧 $f$ 的 COLMAP 深度和度量深度。消融表明，不进行重标定会使 RE10K 上 FVD 增加 4.65，视觉质量显著下降。

## 实验与分析

### 主实验结果

AC3D在分布内（RealEstate10K）和分布外（MSR-VTT）两个基准上均实现了相机跟随精度与视觉质量的双重提升。Table 2汇总了各方法在相机姿态误差（TransErr/RotErr）和视觉质量指标（FID/FVD/CLIP）上的对比结果。

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation. We evaluate all the models using camera pose and visual quality metrics based on unseen camera trajectories. We compute translation and rotation errors based on the estimated camera poses from generations using ParticleSfM [194]. We evaluate both in-distribution performance with RealEstate10K [201] and out-of-distribtion performance with MSR-VTT [163]*

**RealEstate10K（分布内）**。与复现于VDiT主干的强基线VD3D (DiT)相比，AC3D将平移误差从0.421降至0.358（下降15.0%），旋转误差从0.056降至0.035（下降37.5%），同时FVD从38.57改善至36.55。值得注意的是，AC3D在提升相机控制精度的同时，视觉质量指标也全面优于基线——FID从1.21降至1.18，CLIP得分从28.34提升至28.76。这表明AC3D成功突破了现有方法中相机控制与画质之间的权衡。

**MSR-VTT（分布外）**。在更具挑战性的分布外场景下，AC3D的优势更为显著：FID从6.88降至5.34（改善22.4%），FVD从137.62降至110.71（改善19.6%），同时TransErr从0.486降至0.428（下降11.9%）。分布外场景下视觉质量的大幅提升，直接受益于动态固定相机数据集的引入（见消融分析）。

**用户研究**。Table 1显示，在相机对齐（CA）、运动质量（MQ）、文本对齐（TA）、视觉质量（VQ）和整体偏好五个维度上，AC3D均显著优于VD3D (FIT)和VD3D (DiT)。整体偏好方面，AC3D以95.0%的压倒性优势胜出，验证了主观体验与客观指标的一致性。

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/007_Table_1.jpg]]
*Table 1: User study. We compare our approach to the original VD3D (FIT) and reimplemented VD3D (DiT) on top of our base model. We conduct a user study where participants indicate their preference based on camera aligntment (CA), motion quality (MQ), text alignment (TA), visual quality (VQ), and overall preference (Overall)*

### 消融实验

Table 2的消融部分逐项验证了AC3D各设计选择的因果贡献：

**噪声分布偏置与截断**。移除噪声偏置（w/o biasing noise）导致MSR-VTT上FVD增加16.92，相机跟随与视觉质量均显著下降；仅保留偏置但不截断时间步（w/o noise truncation）使FVD增加6.63。这表明将相机条件限制在反向扩散前40%的时间步（[0.6, 1]区间）是实现精确控制与保持画质的关键。

**浅层条件注入**。将相机条件限制在前8个DiT块（而非全部32块）使训练参数量减少约4倍，训练/推理加速约15%，视觉质量提升10%。若将条件注入扩展到所有32个块，视觉质量反而恶化约10%，证实深层注入相机信号会干扰高层视觉特征的生成。

**动态固定相机数据**。移除AC3D自行采集的20K动态固定相机视频（w/o our dynamic data）后，MSR-VTT上FID增加0.89，FVD增加4.40，分布外泛化能力显著退化。该数据集有效解耦了相机运动与场景动态之间的虚假关联，使模型在遇到动态场景文本提示时仍能生成自然的场景运动。

**相机CFG**。移除独立的相机分类器自由引导（w/o camera CFG）使RE10K上TransErr增加0.014，验证了分离式CFG对相机跟随精度的贡献。

**度量尺度重标定**。不进行度量尺度重标定（w/o metric scaled data）使RE10K上FVD增加4.65，说明COLMAP估计深度与真实度量深度之间的尺度一致性对视觉质量有实质影响。

**相机分支上下文隔离**。在相机分支中保留文本嵌入等上下文信息（w/o dropping camera context）使MSR-VTT上FVD增加7.41，证实上下文信息会干扰相机表示的纯度。

**完全移除相机条件**。当完全移除相机条件（w/o camera cond）时，RE10K上TransErr增加0.233、RotErr增加0.153，MSR-VTT上FVD增加53.83，模型完全退化为无控生成，验证了相机条件模块的必要性。

### 关键图表分析

**Figure 5：VDiT隐式相机姿态估计**。线性探测实验揭示了一个重要发现：冻结的VDiT主干在无任何相机条件注入的情况下，其内部已隐式编码了精确的相机姿态信息。旋转误差最低达0.025，平移误差最低达0.48，且该信息在#9–#21层（中间层）达到峰值。这一发现为AC3D仅向前8层注入相机条件提供了理论依据——相机信号在浅层即被提取，供中后层用于视点对齐的视觉特征渲染。

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/005_Figure_5.jpg]]
*Figure 5: Video DiT is secretly a camera pose estimator. We perform linear probing of camera poses in each of VDiT blocks for various noise levels and observe that video DiT performs pose estimation under the hood. Its middle blocks carry the most accurate information about the camera locations and orientations, which indicates that the camera signal emerges in the early layers to help the middle and late blocks render other visual features aligned with the viewpoint*

**Figure 4：去噪过程中相机运动的涌现时机**。运动频谱分析表明，相机运动作为低频信号，在去噪早期（t=0.9，即前10%时间步）即已完全生成，而高频细节直到t=0.5才逐渐明确。这一时序特征直接支撑了AC3D仅在前40%时间步注入相机条件的设计决策——后期注入不仅冗余，还会损害场景动态性和视觉质量。

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/004_Figure_4.jpg]]
*Figure 4: (b) Motion spectral volumes of VDiT’s generated videos for different diffusion timesteps (left) and their ratio w.r.t. the motion spectral volume at t = 0 (i.e., a fully denoised video). Figure 4. How camera motion is modeled by diffusion? As visualized in Figure 4a and Figure 3, the motion induced by camera transitions is a low-frequency type of motion. We observe that a video DiT creates low-frequency motion very early in the denoising trajectory: Figure 4b (left) shows that even at t=0.96 (first ≈4% of the steps), the low-frequency motion components have already been created, while high frequency ones do not fully unveil even till t=0.5. We found that controlling the camera pose later in...*

**Figure 3：相机运动与场景运动的频谱差异**。对比相机运动视频（紫色）和场景运动视频（橙色）的运动频谱体积，相机运动在低频分量上能量显著更强。这一频谱偏置是AC3D将相机控制聚焦于低频生成阶段的理论基础，该结论在CogVideoX上的补充分析（Figure 7–8）中也得到了跨架构验证。

### 失败模式与局限

尽管AC3D在整体指标上表现优异，仍需注意以下边界情况：

1. **极端分布外轨迹**：模型对与RealEstate10K训练分布差异过大的相机轨迹（如极端俯仰角或高速旋转）的泛化能力有限，控制精度可能下降。
2. **运动频谱分析的间接性**：运动频谱分析依赖光流估计，且在CogVideoX自编码器潜在空间中进行计算，其结论不完全等价于像素空间的运动行为。
3. **线性探测的领域局限性**：相机知识在中间层集中的结论仅基于RealEstate10K数据验证，在其他领域视频中的层间分布模式尚待确认。
4. **动态数据的标注依赖**：当前动态固定相机视频数据集依赖人工筛选，大规模自动化构建方法仍有待探索。
5. **深度估计误差传递**：度量尺度重标定虽然缓解了COLMAP深度与真实尺度的不一致，但深度估计本身的误差仍可能影响绝对相机轨迹的精确性。

### 补充图表

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/010_Figure_8.jpg]]
*Figure 8: (b) Motion spectral volumes of VDiT’s generated videos for different diffusion timesteps (left) and their ratio w.r.t. the motion spectral volume at t = 0 (i.e., a fully denoised video). Figure 8. How camera motion is modeled by diffusion (CogVideoX)? As visualized in Figure 4a and Figure 3, the motion induced by camera transitions is a low-frequency type of motion. We observe that a video DiT creates low-frequency motion very early in the denoising trajectory: Figure 4b (left) shows that even at t=0.96 (first ≈4% of the steps), the low-frequency motion components have already been created, while high frequency ones do not fully unveil even till t=0.5. We found that controlling the camera p...*

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/012_Figure_9.jpg]]
*Figure 9: Comparing rectified flow noise schedules: (orange) vanilla standard logit-normal noise schedule proposed by [30] and used for baseline experiments; (purple) biased but non-truncated noise schedule; (pink) biased and truncated noise schedule*

![[assets/figures/papers/paper_list_l18_AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transf/figures/013_Figure_10.jpg]]
*Figure 10: Our annotations collected for 200 randomly generated videos from VDiT and used in our camera motion analysis in Section 3.3*

## 方法谱系与知识库定位

### 基线方法谱系

AC3D 建立在冻结的大规模视频扩散Transformer（VDiT，11.5B参数，32个DiT块）之上，其方法定位需从相机控制技术的演进脉络来理解。

**基于U-Net的相机控制方法**构成了早期的技术路线。**MotionCtrl** 和 **CameraCtrl** 均采用U-Net作为去噪主干，通过注入相机姿态条件来控制生成视频的视点运动。这些方法验证了相机条件注入的可行性，但受限于U-Net架构的表达能力，在视觉质量与相机跟随精度之间存在明显权衡。

**基于FIT的VD3D** 将相机控制引入到更先进的FIT（Flow Image Transformer）主干中，并采用ControlNet风格的轻量级条件分支设计。AC3D的架构设计（VDiT‑CC）直接继承了这一ControlNet范式：冻结主去噪网络，通过额外的轻量级Transformer块处理并注入相机信息。

**基于DiT的VD3D复现**是本文构建的强基线——将VD3D的ControlNet方案完整移植到VDiT主干上，使用标准logit‑normal噪声分布、全32块条件注入、仅RealEstate10K训练数据。AC3D正是在此基线上通过三个关键槽位的变化实现突破：截断偏置的噪声时间步分布、仅前8块的条件注入、以及动态固定相机数据的引入。

**基于CogVideoX的VD3D**进一步验证了该方法在不同DiT架构上的可迁移性，但同样面临相机控制与场景动态性之间的根本矛盾。

此外，**MotionCtrl (VDiT)** 和 **CameraCtrl (VDiT)** 是将早期U-Net方法的核心思想移植到VDiT主干的对照基线，用于验证架构升级本身并不能解决相机控制的质量退化问题。

### 核心贡献的因果机制

AC3D的改进并非简单的工程优化，而是源于对视频扩散模型中相机运动建模机制的深入分析，形成了清晰的因果链条：

**瓶颈诊断**：现有方法将相机条件作为通用控制信号注入所有去噪时间步和所有网络层，但相机运动本质上是低频信号——运动频谱分析（Figure 3）表明，相机运动能量集中于低频分量；去噪时序分析（Figure 4）进一步揭示，相机运动在去噪过程的前10%时间步（t=0.9）即已完全生成，而高频视觉细节直到t=0.5才明确。因此，在后期时间步和深层网络中注入相机条件不仅冗余，而且会干扰高频视觉特征的生成，导致画质下降和场景动态性丧失。同时，训练数据几乎全部由静态场景视频（RealEstate10K）构成，使模型将相机条件与场景静止强关联——当面对动态场景时，相机控制指令会抑制场景运动。

**因果调控**：基于上述诊断，AC3D通过三个精准的“作用域限定”来解耦相机控制与视觉质量：
1. **时间步截断**：将训练噪声和推理时的相机条件注入限制在[0.6, 1]区间（前40%去噪步），仅在低频生成阶段施加控制。
2. **浅层注入**：仅在前8个DiT块注入相机条件，后24个块自由生成视觉细节。线性探测实验（Figure 5）证实VDiT中间层（#9–#21）已隐式编码了精确的相机姿态（旋转误差0.025，平移误差0.48），浅层注入足以建立视点约束，深层无需重复接收相机信号。
3. **数据去偏**：引入20K动态场景但固定相机的视频，打破“相机运动↔场景静止”的虚假关联，使模型学会在相机运动的同时保留场景动态。

### 适用边界与局限

尽管AC3D在分布内（RealEstate10K）和分布外（MSR‑VTT）场景下均取得了显著提升，其适用边界仍存在明确约束：

**相机轨迹泛化**：模型对与训练集差异较大的极端相机轨迹（如大幅俯仰、急转、非常规速度变化）的泛化能力有限，控制精度可能下降。RealEstate10K的轨迹分布以室内外漫游为主，缺乏动作场景、航拍等领域的轨迹多样性。

**运动分析的方法学局限**：运动频谱分析依赖于光流估计的准确性，且在CogVideoX自编码器的潜在空间中进行计算，不一定完全等价于像素空间的运动行为。线性探测结果仅基于RealEstate10K测试数据，相机知识在其他领域视频中的层次化程度尚待验证。

**数据构建成本**：动态固定相机视频数据集目前依赖人工标注筛选，大规模自动构建此类数据的方法仍有待探索，限制了该方法向更多领域扩展的效率。

**深度估计误差**：尽管引入了度量尺度重标定（见公式 $\hat{\lambda} = \arg\min_{\lambda} \mathbb{E}_{f \sim F} | \lambda D_c^{f} - D_m^{f} |$），COLMAP深度估计本身的误差仍可能影响绝对相机轨迹的精确性，尤其在纹理稀疏或重复纹理场景中。

### 开放问题

1. **极端分布外控制**：如何保证相机条件控制对与训练分布差异极大的轨迹（如第一人称快速旋转、无人机自由飞行）仍保持良好的跟随性与视觉质量？

2. **自动化数据筛选**：能否设计无需人工标注的方法，自动从海量视频中筛选“无相机运动、有场景动态”的片段，以持续扩展训练数据的多样性和规模？

3. **相机知识的架构普适性**：线性探测揭示的相机姿态信息集中于中间层的现象，是否普遍存在于其他架构（如U-Net、不同规模的DiT）或不同预训练目标的视频扩散模型中？

4. **低频建模的进一步优化**：如果进一步提高去噪早期低频信号的建模精度（例如通过专门的损失函数或更精细的时间步调度），是否会带来相机控制效果与动态场景质量的二次提升？

5. **分析框架的推广**：AC3D的分析框架——通过运动频谱分解识别信号频段，再据此限定条件注入的作用域——能否推广到其他运动控制任务（如物体轨迹控制、人体动作控制），在保持合成质量的同时实现精确可控？

## 原文 PDF

![[paperPDFs/CVPR_2025/AC3D_Analyzing_and_Improving_3D_Camera_Control_in_Video_Diffusion_Transformers.pdf]]
