---
title: "MimicMotion: High-Quality Human Motion Video Generation with Confidence-aware Pose Guidance"
type: paper
paper_level: A
venue: ICML
year: 2025
pdf_ref: paperPDFs/ICML_2025/MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_aware_Pose_Guidance.pdf
aliases:
- MimicMotion
tags:
- ICML_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "利用关键点置信度分数自适应调节姿势引导信号强度，并通过渐进式潜变量融合实现长视频平滑过渡。"
primary_logic: "将姿势估计置信度融入引导过程，使模型减少对错误姿势信号的依赖，平衡帧质量与时间连续性；同时通过位置感知的渐进融合避免简单重叠导致的边界闪烁。"
claims:
- "置信度加权的姿势引导减轻了错误估计的影响，提高了生成鲁棒性。"
- "手部区域损失增强显著减少了手部失真。"
- "渐进式潜变量融合消除了片段边界过渡的不连续性。"
- "TikTok test split 上 FID-VID = 9.3"
---

# MimicMotion: High-Quality Human Motion Video Generation with Confidence-aware Pose Guidance

> [!tip] 核心洞察
> 将姿势估计置信度融入引导过程，使模型减少对错误姿势信号的依赖，平衡帧质量与时间连续性；同时通过位置感知的渐进融合避免简单重叠导致的边界闪烁。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于置信度感知姿态引导的高质量人体运动视频生成 |
| 英文题名 | MimicMotion: High-Quality Human Motion Video Generation with Confidence-aware Pose Guidance |
| 会议/期刊 | ICML 2025 |
| Links | [paper](https://arxiv.org/abs/2406.19680); [Project](https://tencent.github.io/MimicMotion) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | MimicMotion |
| Dataset | TikTok test split |

> [!tip] 效果简介
> - TikTok test split 上，FID-VID 为 9.3，对比 12.4 (Moore)，变化 -3.1。
> - TikTok test split 上，FVD 为 594，对比 728 (Moore)，变化 -134。
> - TikTok test split 上，SSIM 为 0.795，对比 0.776 (MagicPose)，变化 +0.019。

## 概述

基于姿态引导的人体运动视频生成面临两个核心瓶颈：**不准确的姿态估计导致生成图像失真（尤其手部区域）**，以及**长视频生成中片段边界平滑性差**。现有方法（如 MagicAnimate、MagicPose、Moore、MuseV）通常将固定颜色的姿态骨架图作为引导信号，忽略了不同关键点估计置信度的差异，使得错误姿态信号直接污染生成过程。

MimicMotion 的核心洞察在于将**姿态估计置信度**融入引导信号与训练损失，使模型自适应地降低对低置信度姿态信号的依赖。具体而言，该方法通过三个关键设计实现突破：

1. **置信度感知的姿态引导**：将关键点与肢干的颜色亮度乘以其置信度分数，使高置信区域在引导信号中更显著，低置信区域影响被抑制。
2. **手部区域损失增强**：基于置信度阈值识别手部区域，对该区域损失施加 10 倍权重，显著减少手部失真。
3. **渐进式潜变量融合**：在长视频推理中，根据帧在片段中的相对位置分配融合权重（λ_fusion = 1/(C+1)），避免简单平均导致的边界闪烁与突然模糊。

该方法以 Stable Video Diffusion（SVD）为基础模型，通过 PoseNet 提取姿态序列特征并注入时空 U-Net 的第一卷积层，同时利用 CLIP 编码器提取参考图像语义特征进行交叉注意力引导。渐进式潜变量融合为训练无关的推理策略，在去噪过程中平滑过渡重叠视频段的潜变量。

在 TikTok 数据集零样本评估（模型未在该数据集训练）中，MimicMotion 在所有指标上达到最优：FID-VID 为 9.3（Moore 为 12.4），FVD 为 594（Moore 为 728），SSIM 为 0.795，PSNR 为 20.1。消融实验证实，置信度感知姿态引导与手部区域增强在所有指标上带来提升，渐进式潜变量融合显著改善 FVD 分数，表明更好的时间连贯性。用户偏好研究进一步显示，参与者一致偏好 MimicMotion 的生成结果。

## 背景与动机

基于姿态引导的人体运动视频生成旨在从单张参考图像和一段驱动姿态序列出发，合成一段目标人物执行指定动作的视频。该技术在虚拟数字人、影视特效、社交媒体内容创作等领域具有广泛的应用前景。然而，现有方法在生成质量上面临两个核心瓶颈。

**瓶颈一：不准确姿态估计导致的图像失真与时序不稳定。** 现有姿势引导视频生成方法通常依赖第三方姿态估计器（如 OpenPose、DWPose）提取驱动视频的骨架关键点，并将其作为条件输入。然而，这些估计器在复杂场景下（如快速运动、自遮挡、手部细节）输出的关键点位置和置信度存在显著误差。当模型不加区分地将这些带有噪声的姿势信号作为强条件时，错误的关键点会直接误导生成过程，导致帧内图像失真——尤其在手部区域表现为手指粘连、形态异常等问题；同时，帧间姿态估计的不一致性会引入时序噪声，造成视频闪烁和抖动。

**瓶颈二：长视频生成的片段边界不连续性。** 受限于扩散模型的计算资源约束，现有方法通常将长视频分割为固定长度的片段分别生成，再通过片段间的重叠区域进行融合。主流方案（如 MultiDiffusion、Lumiere 等采用的简单平均融合）对所有重叠帧施加均匀权重，导致片段边界处权重突变，产生明显的模糊、闪烁或纹理跳变等伪影，严重损害长视频的观看体验。

针对上述问题，MimicMotion 提出了两个核心动机驱动的设计思路：

1. **将姿态估计置信度纳入引导过程**：既然姿态估计的误差是不可避免的，与其让模型盲目信任所有关键点，不如让模型“知道”哪些关键点是可靠的、哪些是可疑的。通过将关键点置信度分数编码到姿态引导信号中，使模型自适应地降低对低置信度区域的依赖，从而在帧质量与姿态跟随之间取得更优的平衡。

2. **以位置感知的方式平滑片段过渡**：长视频生成不应是独立片段的机械拼接。通过让相邻片段的重叠帧根据其在片段中的相对位置获得渐进变化的融合权重——靠近片段中心的帧保留更多原始信息，边界处则平滑过渡——可以从根本上消除简单平均带来的权重不连续性，实现无缝的长视频合成。

这两个动机共同指向一个目标：在保持高帧质量的前提下，显著提升人体运动视频的时间连贯性，使生成结果在视觉真实感和运动流畅性上同时达到领先水平。

## 核心创新

MimicMotion 的核心创新围绕一个中心洞察展开：**将姿态估计的置信度显式引入生成过程的引导与监督，使模型能够自适应地调节对不可靠姿态信号的依赖**，从而在帧质量与时间连续性之间取得平衡。围绕这一思想，方法在三个关键维度上对现有姿态引导视频生成范式进行了系统性改造。

### 1. 置信度感知的姿态引导表示

传统方法（如 MagicAnimate、MagicPose）使用固定颜色的骨架图作为姿态条件，无法区分关键点估计的可靠程度。当姿态估计器在遮挡或运动模糊下产生错误预测时，这些错误信号会直接污染生成结果，导致手部扭曲和肢体错位。

MimicMotion 将置信度信息编码进姿态表示本身：**关键点与肢干的颜色亮度乘以对应的置信度分数**，使高置信区域（如躯干）在视觉上更显著，而低置信区域（如被遮挡的手部）信号强度减弱。这一设计在训练和推理中均发挥作用——模型天然倾向于依赖可靠的姿态线索，对错误引导信号具有内在鲁棒性。消融实验（Figure 7）直观展示了这一机制：在输入包含明显错误姿态估计（Pose 1&2）时，无置信度感知的变体产生严重失真，而完整模型能够有效抑制错误信号的影响；在自遮挡场景（Pose 3）下，置信度信息为模型提供了处理遮挡的额外提示。

### 2. 手部区域损失增强

手部是人体运动视频生成中最易失真的区域，也是用户感知质量的关键瓶颈。MimicMotion 并未引入额外的手部生成网络，而是通过**训练损失的重新加权**来解决这一问题：基于置信度阈值识别可靠的手部区域，对该区域的逐像素损失赋予 10 倍权重。这种设计将优化压力集中在模型能够从真实信号中学习的手部样本上，避免了对不可靠手部姿态的过度拟合。

消融实验（Table 2）表明，手部区域增强在所有指标（FID-VID、FVD、SSIM、PSNR）上均带来一致提升。定性结果（Figure 8）进一步证实，该策略持续减少手部扭曲，显著改善视觉吸引力。

### 3. 渐进式潜变量融合

长视频生成需要将多个视频片段拼接，现有方法（如 MultiDiffusion、Lumiere 采用的简单平均融合）在片段边界处产生权重突变，导致闪烁和突然模糊。MimicMotion 提出**训练无关的渐进式潜变量融合策略**，在推理阶段的去噪过程中执行。

核心机制如下：将长视频划分为每段 $N$ 帧、相邻段重叠 $C$ 帧的片段（$C \ll N$）。定义融合权重因子 $\lambda_{\text{fusion}} = 1/(C+1)$，对重叠区域的第 $j$ 帧（$j \in [1, C]$），其融合权重为 $j\lambda_{\text{fusion}}$，前一帧段的对应帧权重为 $1 - j\lambda_{\text{fusion}}$。这种位置感知的加权方式使权重从片段边界向中心平滑递增，消除了简单平均带来的时间不连续性。消融实验（Table 2）显示，渐进融合显著降低 FVD 分数（从 623 降至 594），表明时间连贯性的实质改善。Figure 9 通过 Y-T 切片可视化证实，该方法有效消除了边界处的伪影。

### 创新之间的协同关系

三个创新并非孤立设计：置信度感知的姿态引导为手部区域增强提供了可靠的掩码生成基础（只有高置信度的手部才被加权）；手部增强反过来强化了模型对姿态引导中高置信信号的响应；渐进式融合则确保这些帧级质量改进能够平滑地扩展到任意长度的视频。这种协同使得 MimicMotion 在 TikTok 测试集上以零样本方式全面超越现有方法——FID-VID 降至 9.3，FVD 降至 594，SSIM 达到 0.795（Table 1）。

## 整体框架

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our approach for long video generation. The colored boxes represent latent video frames. $\mathbf { A }$ darker color means a higher weight. The dashed boxes represent video frame features involved in latent fusion*

MimicMotion 的整体框架以预训练的图像到视频扩散模型（Stable Video Diffusion, SVD）为骨干，围绕“置信度感知的姿态引导”这一核心思想构建。其设计目标是：给定一张参考人物图像和一段目标姿态序列，生成一段高质量、时序平滑的人体运动视频。

### 架构总览

框架由五个主要模块串联构成，形成从输入到输出的完整推理管线（如 Figure 2 所示）：

1. **VAE Encoder**：将参考图像和视频帧编码至潜空间。该模块直接沿用 SVD 的预训练权重，在训练期间保持冻结。
2. **CLIP Encoder**：提取参考图像的语义特征，通过交叉注意力（cross-attention）注入时空 U-Net 的各个块，为生成过程提供身份和外观一致性约束。
3. **PoseNet**：从输入的姿态序列中提取特征。PoseNet 由多层卷积构成（详见 Table 3），其输出以逐元素相加的方式注入 U-Net 的第一卷积层之后，而非注入每个块。这一设计的原因有二：姿态序列未经时序信息提取，其空间特征更适合在浅层引入；同时，浅层注入能更好地与参考图像特征协同，避免深层干扰。
4. **Spatiotemporal U-Net**：执行扩散去噪的核心模块，同时处理空间与时序维度的特征交互。它接收来自 VAE Encoder 的噪声潜变量、来自 PoseNet 的姿态特征、以及来自 CLIP Encoder 的语义条件，逐步预测并去除噪声。
5. **VAE Decoder（含时序层）**：将去噪后的潜变量解码为视频帧。与标准 VAE Decoder 不同，该模块在空间层之外额外引入了时序层，以增强输出视频的时间平滑性。

### 核心设计：置信度感知的姿态引导

MimicMotion 的关键创新在于将姿态估计的置信度分数显式地融入引导过程，形成两个互补机制：

- **置信度加权的姿态表示**：传统方法使用固定颜色的骨架图作为姿态条件，无法区分关键点估计的可靠性。MimicMotion 将每个关键点和肢干的颜色亮度乘以对应的置信度分数——高置信度区域更亮、更显著，低置信度区域则被抑制。这使得模型在训练和推理时能够自适应地减少对错误姿态信号的依赖。
- **手部区域损失增强**：手部是姿态估计误差的高发区，也是生成失真的重灾区。MimicMotion 基于置信度阈值识别手部区域：仅当手部所有关键点的置信度均超过阈值时，该手部才被视为可靠。对可靠手部区域，训练损失权重被放大至 10 倍，从而将优化重点导向这些高置信区域，显著减少手部失真。

### 长视频生成：渐进式潜变量融合

对于超出单次生成窗口的长视频，MimicMotion 采用训练无关的渐进式潜变量融合策略（如 Figure 3 和 Algorithm 1 所示）：

- 将长姿态序列分割为固定帧数 $N$ 的视频段，相邻段之间重叠 $C$ 帧（$C \ll N$）。
- 在扩散去噪过程中，对重叠区域的潜变量帧进行渐进加权融合。融合权重由帧在段内的相对位置决定：$\lambda_{\text{fusion}} = 1 / (C + 1)$，靠近段中心的帧权重高，边界处逐渐过渡。具体更新规则为：
  $$\mathbf{z}_i^j = j \lambda_{\text{fusion}} \mathbf{z}_i^j + (1 - j \lambda_{\text{fusion}}) \mathbf{z}_{i-1}^{N-C+j}$$
  其中 $\mathbf{z}_i^j$ 表示第 $i$ 段第 $j$ 帧的潜变量，$\mathbf{z}_{i-1}^{N-C+j}$ 为前一段对应重叠帧的潜变量。

该策略避免了简单平均融合导致的权重突变，从而消除了段边界处的模糊和闪烁伪影，确保长视频的时序连贯性。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 关键模块 |
|------|------|------|----------|
| 编码 | 参考图像 + 目标姿态序列 | 噪声潜变量 + 姿态特征 + 语义特征 | VAE Encoder, PoseNet, CLIP Encoder |
| 去噪 | 噪声潜变量 + 条件特征 | 去噪潜变量 | Spatiotemporal U-Net |
| 融合（长视频） | 相邻段的重叠潜变量 | 平滑过渡的潜变量序列 | Progressive Latent Fusion |
| 解码 | 去噪/融合后的潜变量 | 视频帧序列 | VAE Decoder（含时序层） |

## 核心模块与公式推导

MimicMotion 以预训练 Stable Video Diffusion (SVD) 为基座，构建图像到视频的扩散生成管线。其核心架构由五个模块构成，其中推理阶段的渐进式潜变量融合为训练无关策略。

### 扩散基础框架

模型遵循标准潜在扩散范式。前向过程将原始视频帧潜变量 $\mathbf{x}_0$ 逐步加噪至 $\mathbf{x}_t$，其条件分布为：

$$q ( \mathbf { x _ { t } } \mid \mathbf { x } _ { 0 } ) = \mathcal { N } ( \mathbf { x } _ { t } ; \sqrt { \bar { \alpha } _ { t } } \mathbf { x } _ { 0 } , ( 1 - \bar { \alpha } _ { t } ) \mathbf { I } )$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，控制信号衰减程度。训练时采用 EDM 噪声分布 $\log \sigma \sim \mathcal{N}(P_{\mathrm{mean}}, P_{\mathrm{std}}^2)$，参数设为 $P_{\mathrm{mean}}=0.5$、$P_{\mathrm{std}}=1.4$。

去噪网络 $\epsilon_\theta$ 以噪声潜变量 $\mathbf{x}_t$、条件 $\mathbf{c}$ 和时间步 $t$ 为输入，预测所加噪声，训练目标为均方误差最小化：

$$\mathbb { E } _ { \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) , \mathbf { x } _ { t } , \mathbf { c } , t } [ | | \epsilon - \epsilon _ { \theta } ( \mathbf { x } _ { t } ; \mathbf { c } , t ) | | _ { 2 } ^ { 2 } ]$$

### 管线模块构成

**VAE Encoder** 将输入视频帧和参考图像编码至潜空间，其权重直接沿用 SVD 预训练参数并保持冻结。对应的 **VAE Decoder** 在空间层之外额外引入时间层，以增强解码视频的时间平滑性。

**Spatiotemporal U-Net** 作为去噪骨干，执行扩散去噪过程中的时空特征交互。该网络接收噪声潜变量，并通过交叉注意力接收来自 CLIP Encoder 的参考图像语义特征。

**PoseNet** 是专门设计的姿态特征提取模块，由多层卷积构成。其输入为姿态序列的骨架图表示，输出特征以逐元素相加的方式注入 U-Net 的第一卷积层输出端。之所以不将姿态特征注入每个 U-Net 块，是因为姿态序列在 PoseNet 中未经时间信息提取，且第一层注入足以提供有效的空间引导信号。

**CLIP Encoder** 负责提取参考图像的语义特征，通过交叉注意力机制注入 U-Net 各块，使生成视频在内容上与参考图像保持一致。

### 置信度感知姿态引导

传统方法使用固定颜色的骨架图作为姿态条件，忽略了姿态估计本身的可靠性差异。MimicMotion 的核心创新在于将关键点置信度分数编码为视觉信号的亮度强度：每个关键点和肢干的颜色乘以对应的置信度分数，使得高置信区域在引导图中更加显著，低置信区域信号减弱。

这一设计使模型在训练和推理过程中自适应地调节对姿态信号的依赖程度——当姿态估计不可靠时（如手部关键点误检），引导信号自动衰减，减少错误条件对生成的干扰。

### 手部区域损失增强

为针对性缓解手部失真问题，模型在训练损失中引入区域加权策略。具体而言，基于置信度阈值识别手部区域：仅当手部所有关键点的置信度均超过阈值时，该手部被视为可靠，并对该区域施加权重为 10 的损失放大。这一机制确保模型在可靠的手部区域上获得更强的训练信号，从而显著提升手部生成质量。

### 渐进式潜变量融合

长视频生成时，视频被分割为多个片段，每段包含 $N$ 帧，相邻片段间有 $C$ 帧重叠（$C \ll N$）。推理时，渐进式潜变量融合在去噪过程的每一步对重叠区域的潜变量进行加权混合。

融合权重由帧在片段中的相对位置决定，核心参数为：

$$\lambda_{\mathrm{fusion}} = 1 / (C + 1)$$

对于第 $i$ 段视频的第 $j$ 帧潜变量 $\mathbf{z}_i^j$，其与前一视频段末尾对应帧的融合规则为：

$$\mathbf{z}_i^j = j \lambda_{\mathrm{fusion}} \mathbf{z}_i^j + (1 - j \lambda_{\mathrm{fusion}}) \mathbf{z}_{i-1}^{N-C+j}$$

其中 $j \in [1, C]$ 表示当前段中重叠帧的索引。该规则使靠近片段中心的帧保留较高权重，边界处则逐渐过渡至相邻片段的特征，从而避免简单平均融合造成的权重突变和边界闪烁伪影。此策略完全集成于推理阶段的去噪循环中，无需额外训练。

## 实验与分析

### 定量评估与基准对比

在 TikTok 数据集测试分割上的零样本评估（模型未在该数据集训练）表明，MimicMotion 在所有指标上均优于现有方法。Table 1 报告了与 **MagicAnimate** (Xu et al., CVPR 2024)、**MagicPose** (Chang et al., ICML 2023)、**Moore** 和 **MuseV** (Xia et al., arXiv 2024) 的对比结果。为公平比较，所有生成视频均中心裁剪为正方形区域视图。

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/007_Table_1.jpg]]
*Table 1: MimicMotion: High-Quality Human Motion Video Generation with Confidence-aware Pose Guidance Table 1: Quantitative comparison to state-of-the-art methods: MagicAnymate (Xu et al., 2024), MagicPose (Chang et al., 2023), Moore (moo, 2024), MuseV (Xia et al., 2024). We evaluate on the TikTok dataset test split. MimicMotion is the best in all metrics*

MimicMotion 在 FID-VID 上达到 **9.3**，相比 Moore 的 12.4 降低了 3.1；FVD 为 **594**，较 Moore 的 728 降低了 134，表明时序连贯性显著更优。在结构相似性（SSIM）和峰值信噪比（PSNR）上，MimicMotion 分别达到 **0.795** 和 **20.1**，均优于 MagicPose 的 0.776 和 18.8。这些提升直接源于置信度感知姿态引导和手部区域增强设计——置信度加权减轻了错误姿态估计的干扰，而手部区域损失加权（权重 10）持续减少了手部失真。

用户偏好研究（Figure 6）进一步验证：在与各基线方法的成对比较中，用户一致偏好 MimicMotion 的生成结果。

### 消融实验

Table 2 系统消融了三个核心模块：手部区域增强（hand）、置信度感知姿态引导（conf.）和渐进式潜变量融合（prog.）。

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/006_Table_2.jpg]]
*Table 2: Ablation studies of hand region augmentation (hand), confidence-aware pose guiding (conf.), and progressive latent fusion (prog.)*

**置信度感知姿态引导**：移除该模块后，所有指标均下降。定性消融（Figure 7）揭示了其因果机制——当输入姿态包含错误估计（Pose 1&2）或自遮挡（Pose 3）时，标准固定颜色骨架图会将错误信号等权重注入模型，导致生成帧扭曲；而置信度加权通过降低低置信度关键点的视觉显著性，使模型减少对不可靠引导信号的依赖，从而提升生成鲁棒性。

**手部区域增强**：单独启用手部损失加权（权重 10）即可显著减少手部失真。Figure 8 的定性对比显示，使用相同参考图像和姿态引导时，该模块持续改善手部生成质量和视觉吸引力。其工作机制是：基于置信度阈值识别可靠手部区域并放大其训练损失，迫使模型优先学习高质量手部表征。

**渐进式潜变量融合**：该训练无关的推理策略对 FVD 指标的改善最为显著（从 623 降至 594），表明其有效提升了长视频的时序连贯性。Figure 9 的 Y-T 切片可视化揭示了因果差异：简单平均融合在片段边界产生权重突变，导致突然模糊和闪烁伪影；而渐进融合根据帧在片段中的相对位置分配权重（$\lambda_{\mathrm{fusion}} = 1 / (C + 1)$），靠近片段中心权重高、边界处逐渐过渡，消除了时序不连续性。

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/009_Figure_9.jpg]]
*Figure 9: Progressive latent fusion ensures smooth segment transitions by avoiding temporal discontinuities of weights in simple averaging, which reduces artifacts in Y-T slices*

三者叠加时，模型在所有指标上取得最优结果（FID-VID 9.3, FVD 594, SSIM 0.795, PSNR 20.1），验证了各模块的互补性。

### 定性分析

**帧质量对比**（Figure 4）：与基线方法相比，MimicMotion 在手部生成质量和姿态依从性上均表现更优。MagicAnimate 和 Moore 在手部区域常出现模糊或形态失真，而 MimicMotion 的置信度感知引导有效缓解了这一问题。

**时序平滑性对比**（Figure 5）：通过帧差可视化评估时序稳定性。MagicPose 呈现突变式跳变，Moore 和 MuseV 在纹理和文字区域出现闪烁，而 MimicMotion 维持了稳定的帧差分布。该优势归因于置信度感知姿态引导减轻了不准确姿态输入引入的时序噪声。

**跨域泛化**（Figure 11, Figure 12）：MimicMotion 在卡通角色和动物跳舞视频上展现了零样本泛化能力。尽管外观分布与人类训练数据显著不同，模型仍能保留参考图像的艺术风格或动物形态，同时生成跟随输入姿态的自然运动。该能力缺乏定量指标评估，需进一步验证。

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/016_Figure_12.jpg]]
*Figure 12: Generated animal dancing videos. MimicMotion can generalize to animal dancing zero-shot, producing plausible motions despite the significant appearance differences from humans. Top: reference frame; Left: reference pose guidance; Bottom: generated frames at different timestamps*

### 训练与实现细节

模型在 4,436 段互联网采集的人类跳舞视频上训练（平均时长 20.1 秒），使用 8 块 NVIDIA A100 GPU，训练 20 个 epoch，批量大小 8，每片段 16 帧。PoseNet 的具体架构细节见 Table 3。训练噪声分布遵循 $\log \sigma \sim \mathcal{N}(P_{\mathrm{mean}}, P_{\mathrm{std}}^2)$，其中 $P_{\mathrm{mean}}=0.5$, $P_{\mathrm{std}}=1.4$（Karras et al. 的设置）。

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/012_Table_3.jpg]]
*Table 3: Detailed Architecture of PoseNet*

### 待验证问题与局限

以下问题需人工确认或进一步研究：
- 模型在极端姿态和严重自遮挡下的生成鲁棒性边界尚未量化。
- 渐进融合的超参数 $C$ 和 $N$ 对不同长度视频的自动化选择方案缺失。
- 手部区域增强的置信度阈值敏感性和自适应方案未讨论。
- 跨域生成（卡通/动物）缺乏定量指标系统评估。
- 方法能否扩展至文本、深度等其他条件引导的人类视频生成尚未探索。

### 补充图表

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l7_MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_a/figures/019_Figure.jpg]]

## 方法谱系与知识库定位

**方法定位与基线关系**

MimicMotion 建立在图像到视频扩散模型的范式之上，以预训练 Stable Video Diffusion (SVD) 为生成骨干，将其扩展为姿态引导的人体运动视频生成框架。与现有姿态引导方法相比，其核心差异在于将姿态估计的置信度信息显式引入生成过程，形成闭环的“感知-引导”机制。

在定量对比中，MimicMotion 在 TikTok 测试集上全面优于同期方法：相比 **MagicAnimate** (Xu et al., CVPR 2024) 和 **MagicPose** (Chang et al., ICML 2023)，MimicMotion 在 FID-VID 上达到 9.3（MagicPose 为 12.4），FVD 降至 594（MagicPose 为 728），SSIM 提升至 0.795（MagicPose 为 0.776），PSNR 达到 20.1（MagicPose 为 18.8）。这些增益源于置信度感知姿态引导对错误姿态信号的抑制，以及手部区域损失增强对关键细节的强化。

具体而言，MimicMotion 在三个关键环节改进了基线设计：

- **姿态引导表示**：基线方法（如 MagicAnimate、MagicPose）使用固定颜色的骨架图作为条件信号，所有关键点与肢干具有相同的视觉显著性。MimicMotion 将关键点和肢干的颜色亮度乘以对应的置信度分数，使高置信区域在引导信号中更突出，低置信区域自动弱化。这一设计使模型在训练和推理中天然具备对错误姿态估计的鲁棒性，尤其在自遮挡场景下（Figure 7）。

- **损失函数设计**：基线方法采用均匀的逐像素损失权重，对手部等易失真区域无特殊处理。MimicMotion 基于置信度阈值识别手部区域，仅当手部所有关键点置信度均超过阈值时才将其视为可靠区域，并对该区域损失施加 10 倍权重。消融实验（Table 2）表明，手部区域增强在所有指标上带来一致提升，显著减少手部失真（Figure 8）。

- **长视频生成策略**：现有长视频生成方法（如 MultiDiffusion 和 Lumiere 的简单平均融合）在视频片段边界处因权重突变导致闪烁和模糊伪影。MimicMotion 提出训练无关的渐进式潜变量融合策略：将长视频划分为每段 N 帧、相邻段重叠 C 帧（C << N）的片段，在去噪过程中根据帧在片段中的相对位置分配融合权重 $\lambda_{\text{fusion}} = 1/(C+1)$，靠近片段中心的帧权重高，边界处渐进过渡。消融实验显示该策略使 FVD 从 623 降至 594，显著改善时间连贯性（Table 2），并消除了 Y-T 切片中的突变伪影（Figure 9）。

**适用边界与泛化能力**

MimicMotion 的训练数据为 4,436 个互联网采集的人体舞蹈视频（平均时长 20.1 秒），模型在该数据分布内的舞蹈动作生成上表现稳定。零样本跨域泛化实验显示，该方法可保持卡通角色的艺术风格并生成自然运动（Figure 11），甚至能泛化至外观差异显著的动物舞蹈生成（Figure 12），表明姿态引导机制具有一定的域外迁移能力。然而，这些跨域结果目前仅有定性展示，缺乏定量指标的系统评估。

**局限与开放问题**

论文未明确列出方法的局限性，但基于实验证据和设计选择，可识别以下开放问题：

1. **极端姿态与严重自遮挡的鲁棒性**：置信度感知机制依赖姿态估计器提供的置信度分数，当姿态估计器本身在极端姿态下系统性失效时，低置信度信号虽被弱化，但模型能否从参考图像中推断出合理的人体结构仍待验证。

2. **融合超参数的自动化**：渐进融合中的片段长度 N 和重叠帧数 C 需手动设定，对不同长度和运动速度的视频，是否存在自适应的参数选择策略是一个开放方向。

3. **手部置信度阈值的敏感性**：手部区域增强依赖固定的置信度阈值来判定可靠性，该阈值的选择是否对不同姿态估计器敏感，以及能否设计自适应阈值方案，值得进一步探索。

4. **跨域生成的定量评估**：卡通和动物舞蹈生成目前仅有定性示例，缺乏如 FID、FVD 等定量指标的系统评估，难以衡量跨域场景下的性能衰减程度。

5. **条件扩展的可能性**：该方法当前仅使用姿态作为运动条件，其置信度感知的引导框架能否推广至其他条件模态（如文本描述、深度图、语义分割）引导的人体视频生成，是一个有潜力的扩展方向。

## 原文 PDF

![[paperPDFs/ICML_2025/MimicMotion_High_Quality_Human_Motion_Video_Generation_with_Confidence_aware_Pose_Guidance.pdf]]
