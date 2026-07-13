---
title: "YoNoSplat: You Only Need One Model for Feedforward 3D Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/YoNoSplat_You_Only_Need_One_Model_for_Feedforward_3D_Gaussian_Splatting.pdf
project_link: https://botaoye.github.io/yonosplat/
code_link: null
openreview_forum_id: ImRhA9xmay
aliases:
- YoNoSplat
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "采用混合强制（mix-forcing）训练策略：从纯教师强制（真值位姿）开始，逐步以线性概率引入模型预测的位姿参与聚合，从而解耦位姿与几何学习；配合最大成对相机距离归一化的场景归一化方案以及内参条件嵌入（ICE）模块，从根本上消除尺度模糊，使模型在无位姿、无内参条件下仍能稳定收敛。"
primary_logic: "通过渐进混合预测位姿与真实位姿，模型既避免了早期位姿误差对高斯学习的破坏性反馈，又通过后续引入预测位姿消除了曝光偏差，从而在单一模型内实现了对任意数量、无先验图像的一致且可扩展的前馈3D高斯重建。"
claims:
- "混合强制训练从纯教师强制开始，逐步线性增加预测位姿的概率，最终混合比 r=0.1，有效平衡了位姿依赖与无位姿两种设置下的性能。"
- "最大成对相机距离归一化在所有场景归一化策略中表现最优，是无深度监督数据集上尺度恢复的关键。"
- "在使用预测内参与内参条件嵌入时，无内参设置的PSNR (24.711)显著优于无任何内参条件的基线(24.481)，证明ICE模块有效缓解了尺度模糊。"
- "在6视图设置下，混合强制在无位姿测试中达到最佳PSNR (25.587)，超越了其他训练策略，且位姿依赖设置仍保持竞争力。"
---

# YoNoSplat: You Only Need One Model for Feedforward 3D Gaussian Splatting

> [!tip] 核心洞察
> 通过渐进混合预测位姿与真实位姿，模型既避免了早期位姿误差对高斯学习的破坏性反馈，又通过后续引入预测位姿消除了曝光偏差，从而在单一模型内实现了对任意数量、无先验图像的一致且可扩展的前馈3D高斯重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | YoNoSplat：只需一个模型即可实现前馈3D高斯泼溅 |
| 英文题名 | YoNoSplat: You Only Need One Model for Feedforward 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ImRhA9xmay) · [Project](https://botaoye.github.io/yonosplat/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | YoNoSplat |
| Dataset | RealEstate10K (6 views), ScanNet++ (32 views, cross-dataset), RealEstate10K (3 views, sparse), DL3DV (6 views, pose-free) |

> [!tip] 效果简介
> - RealEstate10K (6 views) 上，PSNR (pose-free, no intrinsics) 为 24.571，对比 DepthSplat: 24.156，变化 +0.415。
> - ScanNet++ (32 views, cross-dataset) 上，PSNR (pose-free, no intrinsics) 为 16.886，对比 AnySplat: 14.054，变化 +2.832。
> - RealEstate10K (3 views, sparse) 上，PSNR 为 27.528，对比 NoPoSplat: 26.619，变化 +0.909。

## 概要

从无标定、无位姿的多视图图像中直接重建三维场景，是计算机视觉领域的一项核心挑战。现有前馈方法要么依赖精确的相机位姿（如DepthSplat、MVSplat），要么将场景建模在标准空间中（如NoPoSplat），难以兼顾灵活性与重建质量。其根本瓶颈在于：联合学习相机位姿与三维高斯场时，二者高度纠缠——位姿误差污染几何学习信号，几何误差又反向干扰位姿估计，形成破坏性反馈循环；同时，尺度模糊问题进一步阻碍无先验重建。

YoNoSplat提出了一种全新的前馈3D高斯泼溅范式：**逐视图预测局部高斯，再通过相机位姿聚合到全局坐标系**。这一设计的核心创新在于**混合强制（mix-forcing）训练策略**——训练初期完全使用真值位姿建立稳定的几何基础，随后以线性概率逐步引入模型预测的位姿参与聚合，最终混合比设为 $r=0.1$。该策略有效解耦了位姿学习与高斯学习，既避免了早期位姿误差的破坏性反馈，又消除了纯教师强制带来的曝光偏差。

为从根本上消除尺度模糊，YoNoSplat采用**最大成对相机距离归一化**作为场景归一化方案，并引入**内参条件嵌入（ICE）模块**，将预测的相机内参转换为射线条件，嵌入高斯预测流程。这使得模型在无位姿、无内参的条件下仍能稳定收敛。

在DL3DV、RealEstate10K和ScanNet++三个数据集上的实验表明：YoNoSplat在无位姿、无内参设置下，**一致超越位姿依赖的SOTA方法DepthSplat**（如RealEstate10K上PSNR 24.571 vs 24.156）；跨数据集零样本泛化至ScanNet++时，**大幅领先同期无位姿方法AnySplat**（PSNR 16.886 vs 14.054）；在稀疏3视图设置下，**超越NoPoSplat达0.909 dB**。模型支持任意数量输入视图，100视图重建仅需2.69秒（NVIDIA GH200），且基于不透明度的修剪策略在几乎无损质量的前提下显著降低显存占用。



### 问题背景：无先验多视图3D重建的困境

从多视图图像中恢复三维结构是计算机视觉的核心问题。近年来，基于3D高斯泼溅（3D Gaussian Splatting, 3DGS）的前馈方法（如MVSplat、DepthSplat）在已知相机位姿和内参的条件下取得了显著进展，能够从少数几张图像中快速重建出高质量的三维高斯场。然而，这一范式存在根本性的局限：它要求输入图像同时配备精确的相机位姿（外参）和内参（焦距等），而这些先验信息在真实场景中往往不可得。

当相机位姿未知时，问题变得高度纠缠。模型必须同时从图像中推断三维几何和相机位置，但这两个任务是相互依赖的：位姿估计的误差会直接污染几何学习信号——错误的相机位置导致逐视图预测的局部高斯在聚合到全局坐标系时发生错位，产生模糊或撕裂的重建结果；反过来，不准确的几何预测又会反向干扰位姿估计，形成恶性循环。这种“鸡与蛋”式的耦合使得训练极不稳定，尤其在训练早期，位姿预测尚未收敛，几何学习几乎无法获得有效监督。

### 现有方法的缺口

针对无位姿设定，已有两类尝试。一类方法（如NoPoSplat）将场景建模在一个共享的“标准空间”（canonical space）中，试图绕过显式的位姿预测。然而，标准空间假设所有视图共享统一的坐标系，当视图数量增加或空间覆盖范围扩大时，该假设会引入严重的几何扭曲，限制模型的扩展性。另一类方法（如AnySplat）则采用纯自强制（self-forcing）策略，即始终使用模型自身预测的位姿进行高斯聚合，这虽然避免了训练与测试不一致带来的曝光偏差（exposure bias），但早期位姿误差的破坏性反馈使得训练收敛困难，重建质量受限。

此外，尺度模糊（scale ambiguity）是另一重关键障碍。在缺乏已知内参或真实深度监督的情况下，从单目图像中恢复的几何天然存在尺度歧义——场景可以被放大或缩小任意倍数而仍然满足多视图几何约束。现有方法要么依赖已知内参来消除歧义，要么在无内参条件下性能大幅下降，缺乏在完全无先验条件下稳定工作的能力。

### 本文动机

上述分析揭示了一个核心瓶颈：**联合学习相机位姿与三维高斯场高度纠缠，位姿误差与几何误差相互放大，且尺度模糊进一步阻碍无先验重建。** 本文的动机正是解开这一死结——设计一种训练策略，使模型在早期免受位姿误差的破坏性影响，同时逐步获得在无位姿条件下泛化的能力；并通过显式的尺度归一化与内参条件机制，从根本上消除尺度歧义，使单一模型能够在任意数量、无位姿、无内参的多视图图像上实现一致且可扩展的前馈3D高斯重建。



## 核心方法与创新机理

YoNoSplat 的核心创新在于**解耦位姿估计与三维高斯场学习的纠缠关系**，从而在单一前馈模型中实现对任意数量、未标定、未定位多视图图像的稳定三维重建。其关键设计围绕三个相互关联的 changed slots 展开。

### 1. 逐视图局部高斯预测与全局聚合

与 NoPoSplat 等基于标准空间（canonical space）的无位姿方法不同，YoNoSplat 采用**逐视图局部高斯预测**范式：网络首先为每个输入视图独立预测局部坐标系下的三维高斯参数，同时预测每帧对应的相机位姿，再将局部高斯变换至全局坐标系进行聚合。这一设计使位姿估计与高斯学习在结构上解耦——局部高斯的预测不依赖全局位姿一致性，而聚合步骤则通过位姿完成。

消融实验直接验证了这一选择的有效性：在 6 视图设置下，局部高斯预测的 PSNR 达到 25.587，而标准空间预测仅为 24.104，提升约 1.5 dB（Table 7）。这表明在无位姿先验的条件下，逐视图建模比强制全局一致性更有利于学习稳定的几何表征。

### 2. 混合强制训练策略

位姿与高斯的纠缠在训练中表现为一个恶性循环：若使用模型预测的位姿进行高斯聚合（自强制，self-forcing），早期位姿误差会污染几何学习信号；若始终使用真值位姿（教师强制，teacher-forcing），则模型在推理时面临曝光偏差——训练时从未见过预测位姿引入的聚合误差，导致测试性能骤降。

YoNoSplat 提出的**混合强制（mix-forcing）**策略通过渐进式课程学习打破这一循环：

- 训练初期（$t < t_{\text{start}}$）完全使用真值位姿，建立稳定的几何基础；
- 从 $t_{\text{start}}$ 到 $t_{\text{end}}$，以线性增长的概率 $r$ 使用模型预测的位姿参与聚合；
- 最终混合比固定为 $r = 0.1$，即 10% 的聚合步骤使用预测位姿，90% 使用真值位姿。

这一设计的因果机制清晰：早期教师强制避免了位姿误差对高斯学习的破坏性反馈，后期引入预测位姿则消除了曝光偏差。Table 5 的结果直接支撑这一机制：混合强制在无位姿测试中达到 PSNR 25.587/SSIM 0.854/LPIPS 0.130，显著优于纯教师强制（24.104/0.819/0.172）和纯自强制（22.662/0.757/0.185）；在位姿依赖设置下，混合强制（25.212）与纯教师强制（25.291）几乎持平，表明引入预测位姿并未损害位姿已知时的性能。

超参数分析（Figure 8）进一步确认 $r=0.1$ 是最优折衷：当 $r$ 增大时无位姿性能持续提升，但位姿依赖性能开始下降；$r=0.1$ 恰好处在无位姿性能大幅改善而位姿依赖性能几乎不变的临界点。

### 3. 尺度模糊的联合解决方案

无先验重建面临根本性的尺度模糊问题：相同的多视图外观可以对应任意尺度的场景与相机位移。YoNoSplat 通过两条互补路径消除这一歧义：

**场景归一化**：对预测的相机位姿进行后处理归一化，消除全局尺度的自由度。系统性地评估了多种归一化策略后，**最大成对相机距离归一化**（$\max_{i,j} d_{ij}$）被证明是最优选择，PSNR 达到 25.212，而无归一化时仅为 22.662（Table 6）。这一结果说明，以场景内最远相机距离作为尺度参考，比均值距离或最大平移量更能稳定地锚定场景尺度。

**内参条件嵌入（ICE）**：网络通过一个内参预测头估计焦距等参数，ICE 模块将预测内参转换为相机射线，经线性层编码后作为条件特征注入图像特征。Table 8 显示，使用预测内参与 ICE 时 PSNR 为 24.711，明显优于完全无内参条件的 24.481，证明内参信息通过射线几何为尺度推断提供了有效约束。值得注意的是，即使内参存在噪声扰动，ICE 仍能保持鲁棒性（Table 10），表明模型学会了从内参中提取尺度相关的几何线索，而非机械记忆数值。

### 创新点的协同效应

上述三个 changed slots 并非独立运作，而是形成协同回路：逐视图局部高斯预测降低了位姿误差对几何学习的直接冲击；混合强制确保了位姿估计器在训练中经历自身误差的反馈，从而学会预测与高斯聚合兼容的位姿；场景归一化与 ICE 则为位姿和高斯的联合学习提供了尺度一致的信号空间。三者共同使 YoNoSplat 在无任何先验（无位姿、无内参）的条件下，仍能在 DL3DV 上以 6 视图达到 24.531 PSNR，超越需要真值位姿的 DepthSplat（Table 1），验证了从纠缠到解耦的设计逻辑。



![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/008_Figure_3.jpg]]
*Figure 3: Overview of YoNoSplat. (a) Features are extracted with a DINOv2 encoder, followed by local-global attention across images, and finally used to predict camera poses and local 3D Gaussians. (b) The Intrinsic Condition Embedding (ICE) module predicts intrinsic parameters ( i . e . , focal length), which are then converted into camera rays and re-encoded as conditioning for Gaussian prediction, thereby resolving scale ambiguity*

YoNoSplat 是一个前馈式 3D 重建模型，其核心映射关系为：

$$f_{\theta} : \{ (\mathbf{I}^v) \}_{v=1}^{V} \mapsto \left\{ \cup \left( \boldsymbol{\mu}_j^v, \alpha_j^v, \mathbf{r}_j^v, \mathbf{s}_j^v, \mathbf{c}_j^v \right), \mathbf{k}^v, \mathbf{p}^v \right\}_{j=1,\dots,H \times W}^{v=1,\dots,V}$$

即从 $V$ 张无位姿、未标定的多视图图像出发，同时预测每视图的局部 3D 高斯参数、相机内参 $\mathbf{k}^v$ 和相机位姿 $\mathbf{p}^v$，最终通过预测（或给定）的位姿将局部高斯聚合到全局坐标系中。

### 模块架构

模型由以下核心模块构成（见图 3）：

1. **DINOv2 ViT 编码器**：采用 DINOv2 Large 模型（24 层注意力层）从输入图像提取特征。同时，在编码器阶段通过级联一个内参 token 与图像 token 来预测相机内参。

2. **交替注意力解码器**：编码后的特征经过 18 层交替注意力块（alternating attention blocks），每块包含逐帧自注意力层和全局拼接自注意力层，实现多视图特征的鲁棒融合。该机制借鉴了 VGGT 的局部-全局注意力设计。

3. **位姿头（Camera Head）**：通过 MLP 层预测 12 维相机向量，包含平移和 9 维旋转表示。

4. **内参头与内参条件嵌入（ICE）**：预测相机内参（焦距等），并将其转换为相机射线，经线性层编码后作为条件嵌入加回原始图像特征，从而显式解决尺度模糊问题。

5. **高斯中心预测头与高斯参数预测头**：采用双头设计，分别逐像素预测高斯中心位置和其余高斯参数（不透明度、旋转、缩放、颜色）。

6. **基于不透明度的修剪**：在聚合后去除不透明度低于阈值的高斯，显著降低显存与计算开销，且重建质量几乎无损（PSNR 下降 < 0.01 dB）。

### 训练策略：混合强制

位姿估计与高斯学习高度纠缠——预测位姿的误差会破坏几何学习信号，而几何误差又反向干扰位姿估计。YoNoSplat 提出**混合强制（mix-forcing）**训练策略来解耦这一依赖：

- 训练初期纯使用真值位姿（教师强制），建立稳定的几何基础；
- 在预设步数 $t_{\text{start}} = 80k$ 后，以线性概率逐渐引入模型预测的位姿参与高斯聚合；
- 至 $t_{\text{end}} = 100k$ 时达到最终混合比 $r = 0.1$。

该策略既避免了早期位姿误差的破坏性反馈，又通过后续引入预测位姿消除了曝光偏差（exposure bias），使模型在无位姿和位姿依赖两种设置下均表现优异。

### 场景归一化

无深度监督条件下，尺度模糊是核心障碍。YoNoSplat 采用**最大成对相机距离归一化**策略——以所有相机中心之间的最大成对距离作为归一化因子。消融实验表明，该策略显著优于平均成对距离归一化、最大平移归一化和无归一化方案（无归一化时 PSNR 从 25.212 骤降至 22.662），是模型成功的关键因素。

### 损失函数

总损失由四项加权求和构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{image}} + \lambda_{\mathrm{intrin}} \mathcal{L}_{\mathrm{intrin}} + \lambda_{\mathrm{pose}} \mathcal{L}_{\mathrm{pose}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}}$$

其中 $\mathcal{L}_{\mathrm{image}}$ 为渲染损失，$\mathcal{L}_{\mathrm{intrin}}$ 为内参预测损失，$\mathcal{L}_{\mathrm{pose}}$ 为成对相对位姿损失（旋转采用测地距离，平移采用 Huber 损失），$\mathcal{L}_{\mathrm{opacity}}$ 为不透明度 L1 正则项以促进稀疏化。训练过程中，若位姿损失超过阈值 1，则跳过该批次以维持训练稳定性。

### 输入输出流总结

1. 输入 $V$ 张任意分辨率、无位姿、无内参的多视图图像；
2. DINOv2 编码器提取特征，同时预测内参并经 ICE 模块嵌入；
3. 交替注意力解码器进行多视图特征融合；
4. 位姿头预测相机外参，高斯头预测逐视图局部高斯；
5. 以混合强制策略（训练时）或纯预测位姿（推理时）将局部高斯聚合到全局坐标系；
6. 基于不透明度的修剪去除冗余高斯，输出全局 3D 高斯场；
7. 可选的后优化步骤进一步优化相机位姿、高斯中心和颜色参数。



### 3.1 前馈映射范式

YoNoSplat 的核心映射函数为：

$$f_{\theta} : \{ (\mathbf{I}^v) \}_{v=1}^{V} \mapsto \left\{ \cup \left( \boldsymbol{\mu}_j^v, \alpha_j^v, \mathbf{r}_j^v, \mathbf{s}_j^v, \mathbf{c}_j^v \right), \mathbf{k}^v, \mathbf{p}^v \right\}_{j=1,\dots,H \times W}^{v=1,\dots,V}$$

其中 $\mathbf{I}^v$ 为第 $v$ 张输入图像，$V$ 为视图总数。网络同时预测每个视图的局部高斯参数（中心 $\boldsymbol{\mu}_j^v$、不透明度 $\alpha_j^v$、旋转 $\mathbf{r}_j^v$、缩放 $\mathbf{s}_j^v$、颜色 $\mathbf{c}_j^v$）、相机内参 $\mathbf{k}^v$ 和相机位姿 $\mathbf{p}^v$。这些逐视图局部高斯随后通过预测或给定的相机位姿变换到全局坐标系中聚合。

与 NoPoSplat 等基于标准空间（canonical space）预测的方法不同，逐视图局部高斯预测在 6 视图设置下 PSNR 提升约 1.5 dB（25.587 vs 24.104），验证了该设计选择的有效性。

### 3.2 编码器-解码器架构

**编码器**采用 DINOv2 Large 模型（Oquab et al., 2023），包含 24 层注意力层。在编码阶段，模型通过拼接一个内参 token 与输入图像 token 来预测相机内参，该内参 token 随图像 token 一同经编码器网络处理。

**解码器**由 $N$ 个交替注意力块（alternating attention blocks）组成，每个块包含：
- 逐帧自注意力层（per-frame self-attention）：在单视图内部进行特征交互
- 全局拼接自注意力层（global concatenated self-attention）：跨视图进行特征融合

这种局部-全局注意力机制借鉴了 VGGT（Wang et al., 2025a）的设计，使模型能有效处理任意数量的输入视图。具体配置为 18 层交替注意力层。

### 3.3 内参条件嵌入（ICE）模块

尺度模糊是无位姿、无内参前馈重建的核心挑战。ICE 模块通过以下流程解决该问题：

1. **内参预测**：内参头从编码特征中预测相机内参（焦距等）
2. **射线转换**：将预测的内参参数转换为相机射线（camera rays）
3. **条件嵌入**：射线经线性层映射为嵌入特征，与原始图像特征相加

消融实验验证了 ICE 模块的有效性：使用预测内参时 PSNR 为 24.711，显著优于无内参条件的 24.481，证明内参条件嵌入有效缓解了尺度模糊。

### 3.4 场景归一化

为消除不同场景间的尺度歧义，YoNoSplat 采用最大成对相机距离归一化策略。在所有归一化策略的消融中，$\max_{i,j} d_{ij}$（相机中心间的最大成对距离）表现最优，PSNR 达 25.212；而无归一化时 PSNR 骤降至 22.662，验证了该模块的关键性。

### 3.5 混合强制训练策略

混合强制（mix-forcing）是解耦位姿学习与几何学习的核心机制。训练从纯教师强制（teacher-forcing，使用真值位姿）开始，在步数 $t_{\text{start}}$ 后，以线性概率逐步引入模型预测的位姿参与高斯聚合，最终在步数 $t_{\text{end}}$ 达到混合比 $r$。具体超参数设置为 $t_{\text{start}} = 80\text{k}$，$t_{\text{end}} = 100\text{k}$，$r = 0.1$。

混合比 $r=0.1$ 的选择经实验验证：在提升无位姿性能的同时，位姿依赖性能几乎与 $r=0$ 持平，是理想的折中点。

### 3.6 损失函数

总损失由四项加权求和构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{image}} + \lambda_{\mathrm{intrin}} \mathcal{L}_{\mathrm{intrin}} + \lambda_{\mathrm{pose}} \mathcal{L}_{\mathrm{pose}} + \lambda_{\mathrm{opacity}} \mathcal{L}_{\mathrm{opacity}}$$

**成对相对位姿损失**由旋转和平移两部分组成：

$$\mathcal{L}_{\mathsf{R}}(i,j) = \operatorname{arccos}((\operatorname{tr}((\mathbf{R}_{ij})^{\top} \hat{\mathbf{R}}_{ij}) - 1) / 2)$$

$$\mathcal{L}_{\mathsf{t}}(i,j) = \mathcal{H}_{\delta}(\hat{\mathbf{t}}_{ij} - \mathbf{t}_{ij})$$

其中 $\mathcal{L}_{\mathsf{R}}$ 以测地距离度量预测相对旋转 $\hat{\mathbf{R}}_{ij}$ 与真值 $\mathbf{R}_{ij}$ 的差异，$\mathcal{L}_{\mathsf{t}}$ 使用 Huber 损失 $\mathcal{H}_{\delta}$ 计算相对平移误差。训练中跳过位姿损失大于 1 的批次以维持训练稳定性。

**不透明度正则项**促使高斯稀疏化：

$$\mathcal{L}_{\mathrm{opacity}} = \frac{1}{M} \sum_{i=1}^{M} \left| o_i \right|$$

该 L1 正则配合基于不透明度的修剪策略，在几乎不损失重建质量（PSNR 下降 < 0.01 dB）的前提下显著减少高斯数量与显存占用。



## 实验与关键发现

### 核心实验设置

YoNoSplat 在 DL3DV、RealEstate10K 和 ScanNet++ 三个数据集上进行评估。编码器采用 DINOv2 Large 模型，包含 24 层注意力；解码器由 18 个交替注意力层组成。主干网络、高斯中心预测头和相机位姿头的参数从 π³ 初始化。训练时，上下文视图通过基于相机中心的 Farthest Point Sampling 采样以保证空间覆盖，目标视图从视频片段中随机选取。混合强制训练的超参数设定为 $t_{\text{start}} = 80\text{k}$、$t_{\text{end}} = 100\text{k}$，混合比 $r = 0.1$。为维持训练稳定性，当位姿损失大于 1 时跳过该批次。

### 主要定量结果

**DL3DV 数据集**（表 1）：在 6 视图、无位姿且无内参的设置下，YoNoSplat 的 PSNR 达到 24.531，显著优于需要位姿和内参的 DepthSplat。当提供地面真值内参时，PSNR 进一步提升至 24.887；同时提供位姿和内参时达到 24.717。在 12 视图和 24 视图设置下，性能随视图数增加而持续提升，且始终优于所有对比方法。可选的快速后优化（仅优化位姿、高斯中心和颜色）能进一步将 6 视图 PSNR 推至 25.587。

![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/010_Table_1.jpg]]
*Table 1: Novel view synthesis comparison under various input settings. We report results on DL3DV (Ling et al., 2024) with 6, 12, and 24 input views, where p, k, and Opt denote using groundtruth poses, intrinsics, and post-optimization. Our method consistently outperforms previous SOTA approaches, including the pose-dependent DepthSplat, even without prior information*

**RealEstate10K 数据集**（表 2）：6 视图、无位姿无内参设置下，PSNR 为 24.571，超过 DepthSplat 的 24.156。在 3 视图稀疏设置下（表 9），PSNR 达到 27.528，较 NoPoSplat 的 26.619 提升约 0.9 dB，展现了在极稀疏输入下的优越性。

**跨数据集泛化至 ScanNet++**（表 3）：模型仅在 DL3DV 上训练，零样本测试于 ScanNet++。在 32 视图、无地面真值内参设置下，PSNR 达到 16.886，大幅超越在该数据集上训练的 AnySplat（14.054）。随着输入视图从 32 增至 128，性能持续改善，表明模型具备良好的跨域泛化能力和多视图扩展性。

**位姿估计精度**（表 4）：在 224×224 输入分辨率下，YoNoSplat 的位姿估计 AUC 指标已优于对比方法；当分辨率提升至 518×280 时，精度进一步提高。在 DL3DV 上训练、RealEstate10K 上零样本测试的设置下，仍优于所有对比方法。

### 消融实验

**混合强制训练策略**（表 5）：混合强制在无位姿设置下取得 PSNR 25.587 / SSIM 0.854 / LPIPS 0.130，显著优于自强制（23.436 / 0.788 / 0.180）和教师强制（22.662 / 0.757 / 0.185）；在位姿依赖设置下，PSNR 为 25.212，与教师强制（25.212）持平，仅略低于自强制（25.587）。这表明混合强制有效平衡了位姿依赖与无位姿两种场景的性能。

![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/025_Table_5.jpg]]
*Table 5: Mix-forcing achieves the best balance of pose-free and pose-dependent performance*

**混合比 $r$ 的敏感性**（图 8）：当 $r = 0.1$ 时，无位姿性能显著提升，而位姿依赖性能几乎不变。增大 $r$ 会进一步改善无位姿性能，但开始损害位姿依赖性能，因此 $r = 0.1$ 是最优折中。

![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/032_Figure_8.jpg]]
*Figure 8: Effect of the mixing ratio r. PSNR on the RealEstate10K dataset with 6 input views under pose-free and pose-dependent settings as a function of the training hyperparameter r. We choose r = 0 . 1 as it provides a good trade-off, improving pose-free performance while keeping pose-dependent performance nearly unchanged*

**场景归一化策略**（表 6）：最大成对相机距离归一化（$\max_{i,j} d_{ij}$）取得 PSNR 25.212，优于均值成对距离归一化（24.104）和最大平移归一化（24.571）。无归一化时性能大幅下降至 22.662，证实了尺度归一化在无深度监督数据集上的关键作用。

![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/026_Table_6.jpg]]
*Table 6: Pose normalization. Max pairwise distance normalization leads to best performance*

**局部高斯 vs 标准空间高斯**（表 7）：逐视图局部高斯预测的 PSNR 为 25.587，较标准空间高斯（24.104）提升约 1.5 dB，验证了局部预测再聚合策略的有效性。

**内参条件嵌入模块**（表 8）：使用预测内参的 PSNR 为 24.711，显著优于无内参条件的 24.481，但低于使用地面真值内参的 25.587。这证明 ICE 模块能有效缓解尺度模糊，且内参预测质量仍有提升空间。

![[assets/figures/papers/iclr26_0009_ImRhA9xmay_YoNoSplat_You_Only_Need_One_Model_for_Feedforwar/figures/030_Table_8.jpg]]
*Table 8: Effect of ICE Module. Using the intrinsics predicted by our model leads to better performance compared to training without intrinsic conditioning*

**高斯修剪的有效性**（图 7、图 9）：基于不透明度的修剪大幅减少了高斯数量和显存占用，且在整个评估集上平均 PSNR 下降小于 0.01 dB。即使在薄结构、反射/透明表面和宽基线等困难条件下，修剪也未引入可见退化（图 9），重建结果与真值保持视觉一致。

**内参噪声鲁棒性**（表 10）：当内参被不同水平的相对噪声扰动时，带内参条件的模型在所有噪声水平下均优于无条件模型，表明 ICE 模块对不精确内参具有一定鲁棒性。

### 失败模式与局限性

1. **GPU 显存限制**：最大输入视图数受显存约束，当前无法处理超大规模场景，需探索增量式重建策略。
2. **后优化仍有显著增益**：前馈预测结果经后优化可大幅提升（表 1），说明模型预测的位姿和高斯参数仍有较大精化空间。
3. **光照剧烈变化**：视角间存在日夜切换等极端光照变化时，光度一致性假设被破坏，会导致几何误差和漂浮伪影。



## 定位与知识库关联

### 与前馈3D高斯泼溅方法的关系

YoNoSplat 继承了前馈3D高斯泼溅（feedforward 3DGS）的基本范式——从多视图图像直接回归高斯参数，但对其核心假设做出了根本性修正。位姿依赖方法（DepthSplat、MVSplat、pixelSplat）要求提供精确的相机外参作为输入，这在实际应用中构成严重瓶颈。无位姿方法（NoPoSplat、AnySplat）虽移除了这一约束，却引入了新的代价：NoPoSplat 将高斯定义在标准空间（canonical space）中，牺牲了局部几何精度；AnySplat 则需在目标数据集上训练，限制了零样本泛化能力。

YoNoSplat 的关键创新在于**将位姿预测与高斯学习解耦**，而非回避位姿问题。其逐视图局部高斯预测 + 位姿聚合的架构，使模型在无位姿条件下仍能维持与位姿依赖方法相当的几何精度——6视图无位姿设置下 PSNR 达 25.587，显著优于标准空间方案（24.104）[Table 7]。这一设计同时保留了位姿信息的可选择性：当真实位姿可用时，模型可直接利用，无需重新训练。

### 训练策略的谱系定位

混合强制（mix-forcing）训练策略处于教师强制（teacher-forcing）与自强制（self-forcing）之间的帕累托前沿。教师强制用真值位姿聚合高斯，训练稳定但产生曝光偏差——测试时使用预测位姿会导致局部高斯跨视图错位。自强制全程使用预测位姿，消除了曝光偏差，但早期位姿误差会破坏高斯学习，形成双向纠缠的恶性循环。

混合强制通过**时间解耦**解决了这一困境：前 80k 步纯教师强制建立稳定几何基础，随后线性引入预测位姿（混合比 r=0.1），最终在 100k 步达到稳态[Appendix A]。这一调度使模型在无位姿和位姿依赖两种设置下均保持竞争力——无位姿 PSNR 25.587，位姿依赖 PSNR 25.212，差距仅 0.375 dB[Table 5]。从方法论角度看，混合强制可视为一种**课程学习**：先让模型在完美信息下学会高斯预测，再逐步引入位姿不确定性，迫使模型适应现实中的不完美输入。

### 尺度模糊解决方案的定位

尺度模糊是单目/无标定重建的根本性问题。YoNoSplat 采用双管齐下的策略：场景归一化消除全局尺度歧义，内参条件嵌入（ICE）提供逐像素的尺度线索。

在场景归一化层面，最大成对相机距离归一化（max pairwise distance）在所有方案中表现最优（PSNR 25.212），显著优于无归一化（22.662）[Table 6]。这与直觉一致：最大成对距离直接约束了场景的空间范围，为网络提供了最强的尺度先验。

ICE 模块则填补了内参缺失时的信息缺口。它将预测的焦距转换为相机射线嵌入，与图像特征相加，使高斯预测头能感知像素级的深度-尺度关系。使用预测内参时 PSNR 达 24.711，明显优于无内参条件（24.481）[Table 8]。值得注意的是，即使内参存在噪声，条件嵌入仍能提供正向收益[Table 10]，表明模型学到的是内参的结构性信息而非精确数值。

### 适用边界与能力范围

**适用场景：**
- 多视图图像具有足够空间覆盖（通过最远点采样保证），视图数量可从 2 到 100+ 线性扩展
- 场景内光照相对一致——剧烈光照变化（如日夜切换）会破坏光度一致性假设
- 前馈推理速度要求高：100 视图重建仅需 2.69 秒（NVIDIA GH200）

**不适用或需谨慎的场景：**
- 弱纹理或重复纹理区域：位姿预测依赖特征匹配，此类区域可能导致位姿估计漂移
- 极端宽基线且视图稀疏（2 视图）：模型虽在 3 视图下显著优于 NoPoSplat（27.528 vs 26.619）[Table 9]，但 2 视图设置下优势缩小，说明最少视图数存在下限
- 需要极高精度的计量级重建：前馈预测结果可通过后优化大幅提升（Table 1 中 Opt 列），表明模型输出是高质量初始化而非最终结果

### 局限性与开放问题

**已识别的局限：**

1. **显存墙**：最大输入视图数受 GPU 显存限制。尽管基于不透明度的修剪大幅减少了高斯数量（PSNR 下降 <0.01 dB）[Figure 7]，注意力机制的计算复杂度仍随视图数二次增长。增量式重建策略是可能的出路，但如何保证全局一致性仍需探索。

2. **光照鲁棒性**：模型假设光度一致性，视角间剧烈光照变化会导致几何误差和漂浮伪影。在多样化光照数据集上显式训练可能是解决方案，但当前数据覆盖不足。

3. **后优化依赖**：前馈输出虽已具备竞争力，但后优化仍能带来显著提升，表明网络预测的位姿和高斯参数尚未达到局部最优。这暗示当前架构在端到端精度上仍有提升空间。

**开放问题：**

- 如何在保持前馈速度优势的同时，实现真正意义上的增量式重建？这需要设计能融合新旧观测而不破坏已有几何的聚合机制。
- 模型的泛化边界在哪里？在 ScanNet++ 上的零样本结果虽大幅领先 AnySplat（32 视图 PSNR 16.886 vs 14.054）[Table 3]，但室外大范围场景、动态场景、非朗伯表面的表现仍需系统评估。
- 混合强制的调度参数（r=0.1, t_start=80k, t_end=100k）是否对不同数据集普适？当前仅在 RealEstate10K 上进行了敏感性分析[Figure 8]，更广泛的验证有待完成。



## 原文 PDF

![[paperPDFs/ICLR_2026/YoNoSplat_You_Only_Need_One_Model_for_Feedforward_3D_Gaussian_Splatting.pdf]]
