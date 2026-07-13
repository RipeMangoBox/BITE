---
title: "WinT3R: Window-Based Streaming Reconstruction with Camera Token Pool"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WinT3R_Window_Based_Streaming_Reconstruction_with_Camera_Token_Pool_5fa1e9c4d8aa.pdf
project_link: null
code_link: "https://github.com/LiZizun/WinT3R"
aliases:
- WinT3R
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 滑动窗口机制使帧内令牌直接交互，以及相机令牌池提供全局历史信息，是提升重建质量和相机位姿准确性的关键可控因素。
primary_logic: 1) 相邻帧具有强相关性，允许窗口内图像令牌直接交互可显著提升几何预测质量；2) 相机令牌可被极度压缩（单帧仅需1536维向量），使得在保持实时性的前提下，通过全局池实现所有历史帧的交互，从而提供可靠的相机位姿估计。
claims:
- WinT3R在多个数据集上取得了在线重建质量的最优性能（见表1、2）。
- 相机令牌池的消融实验表明，去除池后相机位姿估计精度大幅下降（见表6）。
- 滑动窗口去除后（逐帧处理）重建质量明显退化（见表5）。
- 7-Scenes (长序列) 上 Overall↓ (Chamfer) = 0.034
---

# WinT3R: Window-Based Streaming Reconstruction with Camera Token Pool

> [!tip] 核心洞察
> 1) 相邻帧具有强相关性，允许窗口内图像令牌直接交互可显著提升几何预测质量；2) 相机令牌可被极度压缩（单帧仅需1536维向量），使得在保持实时性的前提下，通过全局池实现所有历史帧的交互，从而提供可靠的相机位姿估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | WinT3R：基于滑动窗口与相机令牌池的流式三维重建 |
| 英文题名 | WinT3R: Window-Based Streaming Reconstruction with Camera Token Pool |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PjviszIZf1) · [Code](https://github.com/LiZizun/WinT3R) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | WinT3R |
| Dataset | 7-Scenes, NRGBD, KITTI |

> [!tip] 效果简介
> - 7-Scenes (长序列) 上，Overall↓ (Chamfer) 0.034 vs 0.062 (CUT3R) (-0.028)。
> - NRGBD (长序列) 上，Overall↓ 0.085 vs 0.142 (CUT3R) (-0.057)。
> - KITTI (深度估计) 上，FPS↑ 17.2 vs best online competitor。

## 概要

在线三维重建面临一个根本性权衡：重建质量与实时性能难以兼得。现有在线方法（如 **CUT3R**（Wang et al., 2025b）和 **Spann3R**（Wang & Agapito, 2024））仅通过状态令牌间接交互图像令牌，缺乏相邻帧之间的直接充分交互，导致几何预测质量欠佳且相机位姿估计不可靠。与此同时，离线方法（如 **Fast3R**（Yang et al., 2025）和 **VGGT**（Wang et al., 2025a））虽能通过全注意力实现高质量重建，却无法满足实时处理需求。

**WinT3R** 针对上述瓶颈，提出两个核心可控因素：

1. **滑动窗口机制**：使窗口内图像令牌直接交互，并借助半重叠（stride=2）的窗口滑动策略实现跨窗口信息传递，显著提升几何预测质量。
2. **相机令牌池**：将单帧相机信息压缩至极紧凑的表示（仅1536维向量），维护一个可扩展的全局池，使当前窗口预测相机位姿时可利用所有历史帧的上下文，从而在保持实时性的前提下大幅提高位姿估计的可靠性。

实验表明，WinT3R 在多个基准上取得了在线重建的最优性能：在 7-Scenes 长序列上，Chamfer 距离（Overall↓）为 0.034，显著优于 CUT3R 的 0.062；在 NRGBD 上为 0.085，优于 CUT3R 的 0.142。同时，模型以超过 17 FPS 的速度实时处理输入图像流，在重建速度与质量之间取得了当前最优平衡。消融实验进一步验证，去除相机令牌池后相机位姿精度大幅下降，去除滑动窗口后重建质量明显退化，证实了两个核心设计的因果作用。

从多视图图像中恢复三维几何与相机位姿是计算机视觉的核心任务，在自动驾驶、机器人导航、增强现实等场景中具有关键应用价值。近年来，基于全注意力机制的离线重建方法（如 **DUSt3R** (Wang et al., 2024b)、**Fast3R** (Yang et al., 2025)、**VGGT** (Wang et al., 2025a)）通过让所有输入帧之间进行充分的令牌交互，在重建质量和相机位姿估计上取得了显著进展。然而，这类方法的计算代价随帧数平方增长，无法满足实时场景对持续流式输入的处理需求。

为应对这一挑战，**在线重建**范式应运而生。现有在线方法（如 **CUT3R** (Wang et al., 2025b)、**Spann3R** (Wang & Agapito, 2024)、**StreamVGGT** (Zhuo et al., 2025)）通过维护一组可学习的**状态令牌**来记忆历史场景信息，新帧仅与状态令牌进行交互，从而将计算复杂度从平方量级降至线性。但这一设计引入了一个关键瓶颈：**图像令牌之间缺乏直接交互**。相邻帧之间仅通过状态令牌间接传递信息，导致几何预测质量欠佳，相机位姿估计不可靠。这构成了在线重建中“质量–实时性”权衡的核心矛盾。

WinT3R 的动机正是打破这一瓶颈。本文提出两个核心洞察：

1. **帧间直接交互的必要性**：相邻帧具有强相关性，允许窗口内图像令牌直接交互可显著提升几何预测质量，而无需引入全注意力的平方复杂度。
2. **相机信息的极致压缩**：相机位姿信息可被极度压缩——单帧仅需 1536 维向量即可有效表征。这使得在保持实时性的前提下，通过维护一个全局相机令牌池实现所有历史帧的交互成为可能，从而为相机位姿估计提供可靠的全局上下文。

基于上述洞察，WinT3R 旨在实现一个既具备帧间充分交互能力、又能维持实时推理速度的在线三维重建系统。

## 核心方法与创新机理

WinT3R 针对在线重建中“帧间交互不足”与“历史信息利用受限”两大瓶颈，提出了两项关键创新。

**瓶颈与因果机制。** 现有在线方法（如 **CUT3R** (Wang et al., 2025b)、**Spann3R** (Wang & Agapito, 2024)）仅通过可学习的状态令牌间接实现跨帧信息传递，相邻帧的图像令牌之间缺乏直接交互，导致几何预测质量欠佳且相机位姿估计不可靠。WinT3R 通过两个可控因素打破这一瓶颈：(1) 滑动窗口机制使窗口内图像令牌直接交互，利用相邻帧的强相关性提升几何预测质量；(2) 相机令牌池以极紧凑的表示（单帧仅1536维向量）存储所有历史相机信息，为位姿估计提供全局上下文，从而在保持实时性（>17 FPS）的前提下同时提升重建精度与位姿准确性。

**Changed Slots：四项关键设计变更。**

| 设计维度 | 基线方案 | WinT3R 方案 | 作用机制 |
|---------|---------|------------|---------|
| **帧间令牌交互方式** | 仅通过状态令牌间接交互 | 滑动窗口内图像令牌直接交互 + 状态令牌，跨窗口半重叠共享 | 窗口内全注意力使相邻帧图像令牌充分通信，显著提升点云预测质量 |
| **历史信息利用** | 仅状态令牌记忆 | 维护可扩展的相机令牌池，预测当前窗口相机位姿时利用所有历史相机令牌 | 全局相机上下文使位姿估计更可靠；消融实验表明去除池后位姿精度大幅下降（Table 6） |
| **点云头部** | DPT头部或线性头部（产生网格伪影） | 轻量卷积头部（ConvHead） | 避免计算昂贵的DPT头部和引入网格伪影的线性头部，兼顾效率与质量 |
| **相机位姿预测头** | 无全局池，仅依赖当前帧 | 具有滑动窗口掩码注意力的Transformer相机头，输入当前窗口+池中历史令牌 | 与解码器架构匹配的掩码注意力机制，有效融合局部窗口与全局历史信息 |

**滑动窗口机制。** 该机制是 WinT3R 的核心架构创新。给定图像流，模型以窗口大小4、步长2的方式滑动处理——相邻窗口重叠一半帧数，确保跨窗口连续性。窗口内所有图像令牌与相机令牌共同送入解码器，与状态令牌进行交替注意力交互（Eq. 2），输出全局增强令牌和局部增强令牌。消融实验证实：去除窗口机制（逐帧处理）后重建质量明显退化（Table 5）；去除窗口重叠后重建精度同样下降（Table 5），验证了半重叠策略对相邻窗口连续性的贡献。

**相机令牌池。** 这是实现“轻量全局记忆”的关键设计。每帧经解码器处理后，其局部和全局相机令牌沿通道维度拼接形成最终相机令牌（Eq. 4），并追加到池中（Eq. 5）。相机头在预测当前窗口位姿时，同时关注当前窗口令牌和池中所有历史令牌（Eq. 6），以滑动窗口掩码注意力控制交互范围。由于相机令牌极度紧凑，池的存储和计算开销极低，使得模型在维持实时性能的同时获得了全局位姿一致性。

WinT3R 的整体流水线以图像流为输入，实时输出每帧的局部点云与相机位姿，其核心架构围绕 **滑动窗口机制** 与 **相机令牌池** 两个关键设计展开（见图2）。

**帧编码阶段**：输入图像流中的每一帧 $I_i$ 首先通过一个逐帧独立的 ViT 编码器，映射为图像令牌 $F_i = \operatorname{Encoder}(I_i)$。随后，可学习的相机令牌 $\mathbf{g}_i$ 被追加到图像令牌之前，形成每帧的完整令牌序列。

**在线窗口解码阶段**：模型以滑动窗口 $\mathcal{W}_t$（窗口大小=4，步长=2）为单位处理帧序列。窗口内所有帧的令牌 $[\mathbf{g}_i, \mathcal{F}_i]_{i \in \mathcal{W}_t}$ 与前一时刻的状态令牌 $\mathcal{S}_{t-1}$ 一同送入解码器。解码器采用双分支结构，通过交替注意力机制实现三类交互：(1) 窗口内图像令牌之间的直接交互；(2) 图像令牌与状态令牌的跨帧信息融合；(3) 状态令牌自身的时序更新。解码器输出三组增强后的令牌——全局图像令牌 $\mathcal{F}_i^g$、局部图像令牌 $\mathcal{F}_i^l$、以及更新后的状态令牌 $\mathcal{S}_t$。相邻窗口之间通过半重叠（stride=2）共享帧，保证跨窗口重建的连续性。

**点云预测阶段**：局部图像令牌 $F_i^l$ 被送入一个轻量卷积头部（ConvHead），直接预测该帧的局部点云 $\hat{P_i}$ 及逐点置信度 $C_i$，避免了 DPT 头部的计算开销和线性头部产生的网格状伪影。

**相机位姿预测与全局记忆**：解码器输出的局部相机令牌 $\mathbf{g}_i^l$ 与全局相机令牌 $\mathbf{g}_i^g$ 沿通道维度拼接为紧凑的最终相机令牌 $\mathbf{g}_i'$（单帧仅1536维）。当前窗口的所有 $\mathbf{g}_i'$ 被追加到全局相机令牌池 $\mathrm{Pool}_{cam}^{t-1}$ 中，形成 $\mathrm{Pool}_{cam}^t$。相机头部基于当前窗口令牌与池中所有历史相机令牌，通过滑动窗口掩码注意力预测每帧的7维相机参数 $[\hat{\mathbf{c}}_i]_{i \in \mathcal{W}_t}$。

**训练目标**：总损失 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{pmap}}$ 由两部分等权重相加构成——相机相对位姿的 $\ell_1$ 损失和置信度加权的点云回归损失，实现端到端训练。

这一设计的关键因果链路在于：滑动窗口使相邻帧的图像令牌得以直接交互，解决了现有在线方法仅通过状态令牌间接交互导致的几何预测退化问题；而极度压缩的相机令牌池则以极低的存储代价提供了全局历史信息，使相机位姿估计能够利用长程上下文，在保持17 FPS实时性能的同时显著提升了位姿预测的可靠性。

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/002_Figure_2.jpg]]
*Figure 2: WinT3R pipeline. We detail the reconstruction process within a single window. All images are first passed through a frame-wise ViT encoder, which outputs image tokens. Camera tokens are then appended to these tokens. Then the tokens within this window are collectively fed into a decoder to interact with state tokens. Finally, the image tokens output by the decoder are sent to a lightweight convolutional head to predict local point maps. Meanwhile, the camera tokens, along with those in the camera token pool, are jointly fed into a camera head to predict camera parameters, while these camera tokens are simultaneously added to the camera token pool*

WinT3R 的在线重建流程围绕两个核心设计展开：**滑动窗口机制**（Online Window Mechanism）与**相机令牌池**（Camera Token Pool），二者分别解决帧间交互不足与历史信息利用不充分的问题。整体管线如 Figure 2 所示，包含以下关键模块。

### 帧编码与令牌准备

输入图像流中的每一帧 $I_i$ 首先经过一个逐帧独立工作的 ViT 编码器，生成图像令牌：

$$F_i = \operatorname{Encoder}(I_i) \tag{1}$$

随后，可学习的相机令牌 $\mathbf{g}_i$ 被追加到图像令牌之前，形成每帧的完整令牌序列 $[\mathbf{g}_i, \mathcal{F}_i]$。这一设计使得相机信息与图像特征在后续解码器中能够联合交互。

### 在线窗口解码器

窗口解码器是 WinT3R 的核心计算模块。给定窗口大小 $|\mathcal{W}_t| = 4$、步长 $2$（相邻窗口半重叠），解码器同时接收当前窗口内所有帧的令牌以及上一时刻的状态令牌 $\mathcal{S}_{t-1}$，输出全局增强令牌、局部增强令牌和更新后的状态令牌：

$$[\mathbf{g}_i^g, \mathcal{F}_i^g]_{i \in \mathcal{W}_t},\; [\mathbf{g}_i^l, \mathcal{F}_i^l]_{i \in \mathcal{W}_t},\; \mathcal{S}_t = \mathrm{Decoders}\big([\mathbf{g}_i, \mathcal{F}_i]_{i \in \mathcal{W}_t},\; \mathcal{S}_{t-1}\big) \tag{2}$$

解码器采用双分支结构并相互连接：一个分支处理图像令牌与相机令牌，执行交替注意力（cross-attention）以产生全局和局部令牌；另一个分支负责更新状态令牌 $\mathcal{S}_t$。状态令牌作为可学习的场景上下文记忆，在窗口间持续传递，确保跨窗口的时序一致性。

注意力掩码的设计（Figure 3）是窗口机制的关键：窗口内所有令牌相互可见（类比全注意力），但跨窗口的交互仅通过状态令牌和相机令牌池间接实现，避免了全序列注意力的二次复杂度。

### 轻量卷积头部与点云预测

为兼顾效率与质量，WinT3R 摒弃了计算昂贵的 DPT 头部和易产生网格伪影的线性头部，采用轻量卷积头部（ConvHead）从局部图像令牌 $\mathcal{F}_i^l$ 直接预测局部点云 $\hat{P}_i$ 及逐点置信度 $C_i$：

$$\hat{P}_i,\; C_i = \mathrm{ConvHead}(\mathcal{F}_i^l) \tag{3}$$

### 相机令牌融合与相机令牌池

解码器输出的全局相机令牌 $\mathbf{g}_i^g$ 和局部相机令牌 $\mathbf{g}_i^l$ 沿通道维度拼接，形成每帧的最终相机令牌：

$$\mathbf{g}_i' = \mathrm{ChannelCat}(\mathbf{g}_i^l,\; \mathbf{g}_i^g) \tag{4}$$

这些相机令牌极为紧凑——单帧仅需 1536 维向量——使得维护一个全局相机令牌池成为可能。每处理完一个窗口，新产生的相机令牌被追加到池中：

$$\mathrm{Pool}_{cam}^t = \mathrm{Pool}_{cam}^{t-1} \sqcup [\mathbf{g}_i']_{i \in \mathcal{W}_t} \tag{5}$$

### 相机头部与位姿预测

相机头部采用与解码器架构一致的滑动窗口掩码注意力 Transformer，其输入包含当前窗口的相机令牌 $[\mathbf{g}_i']_{i \in \mathcal{W}_t}$ 以及池中所有历史相机令牌 $\mathrm{Pool}_{cam}^{t-1}$，输出每帧的 7 维相机参数 $\hat{\mathbf{c}}_i$（含四元数旋转与平移向量）：

$$[\hat{\mathbf{c}}_i]_{i \in \mathcal{W}_t} = \mathrm{CameraHead}\big([\mathbf{g}_i']_{i \in \mathcal{W}_t},\; \mathrm{Pool}_{cam}^{t-1}\big) \tag{6}$$

这一设计使得相机位姿估计能够利用所有历史帧的全局信息，消融实验（Table 6）证实去除相机令牌池后位姿精度大幅下降。

### 训练损失

总损失由相机位姿损失与点云回归损失直接相加构成，二者被证明同等关键：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{camera}} + \mathcal{L}_{\mathrm{pmap}} \tag{7}$$

**点云损失**采用置信度加权的 $\ell_2$ 回归损失，并包含置信度正则项以防止置信度退化：

$$\mathcal{L}_{\mathrm{pmap}} = \sum_{i=1}^{T} \sum_{j \in M_i} C_{i,j}\; \ell_{\mathrm{regr}}^{\mathrm{pmap}}(j,i) - \alpha \log C_{i,j} \tag{9}$$

其中 $M_i$ 为第 $i$ 帧的有效像素掩码，$C_{i,j}$ 为逐像素置信度，$\alpha$ 为正则化系数。

**相机位姿损失**在成对相对位姿上计算 $\ell_1$ 损失，避免定义全局坐标系带来的歧义性：

$$\mathcal{L}_{\mathrm{camera}} = \frac{1}{N(N-1)} \sum_{i \neq j} \ell_1(\hat{\mathbf{c}}_{ij},\; \mathbf{c}_{ij}) \tag{12}$$

其中 $\hat{\mathbf{c}}_{ij}$ 和 $\mathbf{c}_{ij}$ 分别为预测和真值的相对相机参数。

## 实验与关键发现

### 核心性能：三维重建质量

WinT3R在多个标准数据集上以在线模式取得了最优的三维重建质量，并在部分指标上超越离线全注意力方法。Table 1和Table 2汇总了DTU、ETH3D、7-Scenes和NRGBD四个基准上的Chamfer距离（Overall↓）对比：

- **DTU**：在线方法中，WinT3R的Overall为2.738，显著优于在线基线**CUT3R**（Wang et al., 2025b）的3.319和**Spann3R**（Wang & Agapito, 2024）的3.072，且逼近离线方法**Fast3R**（Yang et al., 2025）的2.728。
- **ETH3D**：WinT3R的Overall为0.341，同样领先所有在线方法（CUT3R为0.441），并接近离线全注意力方法**VGGT**（Wang et al., 2025a）的0.328。
- **7-Scenes**：Overall降至0.034，相比CUT3R的0.062降低了45%（-0.028），说明滑动窗口机制在长序列室内场景中的几何预测优势尤为突出。
- **NRGBD**：Overall为0.085，相比CUT3R的0.142降低了40%（-0.057），进一步验证了窗口内直接令牌交互对重建精度的关键作用。

定性对比（Figure 4、Figure 5）显示，WinT3R在室内、室外及物体级野外场景中均能生成更逼真、几何更完整的重建结果，且重建速度显著快于其他在线方法。

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of 3D reconstruction. Compared with other online methods, WinT3R achieves higher reconstruction accuracy while also enabling faster reconstruction speed*

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparison of in-the-wild multi-view 3D reconstruction. We demonstrate reconstruction results on in-the-wild sequences across indoor, outdoor, and object-level scenes. Our method consistently achieves the most photorealistic reconstruction results*

### 相机位姿估计

Table 3报告了Tanks and Temples、CO3Dv2和7-Scenes上的相机位姿估计结果。WinT3R在在线方法中取得了最优的RRA@30、RTA@30和AUC@30指标，验证了相机令牌池提供的全局历史信息对位姿预测的可靠性提升。值得注意的是，WinT3R的位姿精度甚至超过部分离线方法，表明紧凑的相机令牌池（单帧仅1536维向量）在保持实时性的同时，能够有效替代全注意力的全局上下文。

### 视频深度估计与实时性

Table 4展示了Sintel、BONN和KITTI数据集上的视频深度估计结果。WinT3R在保持最高推理速度（KITTI上17.2 FPS）的同时，深度估计精度在所有在线方法中排名第一。这一结果直接回应了在线重建的核心瓶颈——WinT3R在重建质量与实时性能之间取得了当前最优的权衡。

### 消融实验：滑动窗口与相机令牌池

Table 5和Table 6分别从重建质量和相机位姿两个维度验证了核心设计的必要性：

- **滑动窗口机制**：去除窗口后（“w/o window”，即逐帧处理），7-Scenes和NRGBD上的Overall指标显著劣化。窗口重叠策略（stride=2）同样关键——去除重叠（“w/o overlap”）后重建精度下降，说明半重叠设计有效保持了相邻窗口的几何连续性。
- **相机令牌池**：去除池后，Tanks and Temples、CO3Dv2和7-Scenes上的相机位姿估计指标全面大幅下降，直接证实了全局历史令牌对位姿预测的决定性作用。这一结论与论文核心洞察一致：相机令牌可被极度压缩，使得全局交互在实时约束下成为可能。

### 长序列鲁棒性

Table 7专门评估了200帧长序列下的重建性能。WinT3R在7-Scenes（Overall 0.034 vs CUT3R 0.062）和NRGBD（0.085 vs 0.142）上均保持显著优势，表明滑动窗口与相机令牌池的组合设计有效缓解了长序列中的误差累积问题。Figure 7的可视化结果进一步佐证了长序列重建的几何一致性。

### 推理效率

Figure 6对比了不同帧数下的推理效率。WinT3R在GPU显存占用和推理速度两个维度均接近最优水平，且随帧数增长的优势愈发明显。这归因于滑动窗口将计算复杂度约束在常数窗口大小内，而相机令牌池仅需维护极低维度的历史信息。

### 失败模式与局限性

尽管WinT3R在多数场景中表现优异，论文明确指出以下局限：

1. **长序列累积误差**：处理极长视频或海量图像时，尽管相机令牌池提供了全局上下文，几何重建仍存在累积漂移问题。这属于流式重建的固有问题，当前设计未能完全消除。
2. **训练效率**：流式模型需顺序传递时序数据，训练时间显著长于离线模型。如何设计节省训练资源的流式训练方案仍是一个开放问题。

上述两点均需在后续研究中进一步探索，当前实验结果无法提供解决方案。

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on 7-Scenes and NRGBD datasets*

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/011_Table_6.jpg]]
*Table 6: Camera Pose Ablation on Tanks and Temples, CO3Dv2 and 7-Scenes datasets*

![[assets/figures/papers/paper_list_l65_https_openreview_net_forum_id_PjviszIZf1/figures/012_Table_7.jpg]]
*Table 7: Long Sequence Comparison on 7-Scenes and NRGBD datasets*

## 定位与知识库关联

### 1. 方法谱系：从离线到在线，从间接交互到直接交互

WinT3R 处于**流式多视图三维重建**这一快速发展的研究线上，其直接前驱是 **CUT3R**（Wang et al., 2025b）和 **Spann3R**（Wang & Agapito, 2024），这两者均基于 **DUSt3R**（Wang et al., 2024b）的双视图重建范式，通过状态令牌（state tokens）实现跨帧信息传递，从而将离线重建扩展为在线流式处理。然而，这一代方法的共同瓶颈在于：**图像令牌之间仅通过状态令牌间接交互，缺乏相邻帧之间的直接充分交互**，导致几何预测质量欠佳且相机位姿估计不可靠。

WinT3R 对此瓶颈的回应是**将“滑动窗口”机制引入在线重建**——在窗口内，所有图像令牌直接参与交叉注意力，同时与状态令牌交互。这一设计使得 WinT3R 在交互模式上向离线全注意力方法（如 **Fast3R**, Yang et al., 2025；**VGGT**, Wang et al., 2025a）靠近，但通过限制窗口大小保持了在线推理的可行性。窗口之间以半重叠（stride=2）滑动，兼顾了相邻窗口的连续性和计算效率。

另一条并行线是 **StreamVGGT**（Zhuo et al., 2025），它将 VGGT 改造为流式版本，同样面临在线-离线性能差距的问题。WinT3R 与这些工作的核心区别可归纳为两个“变化槽”：

| 变化槽 | 基线方法（CUT3R/Spann3R） | WinT3R |
|--------|--------------------------|--------|
| 帧间令牌交互方式 | 仅通过状态令牌间接交互 | 滑动窗口内图像令牌直接交互 + 状态令牌，跨窗口半重叠共享 |
| 历史信息利用 | 仅状态令牌记忆 | 维护可扩展的相机令牌池，预测当前窗口相机位姿时利用所有历史相机令牌 |

### 2. 相机令牌池：全局记忆的轻量化实现

相机令牌池是 WinT3R 的另一关键创新，其核心洞察在于：**相机位姿信息可以被极度压缩**——单帧仅需 1536 维向量即可有效表征。这使得维护一个包含所有历史帧的全局令牌池成为可能，而不会显著增加计算或存储开销。

在具体实现上，解码器输出的局部和全局相机令牌沿通道维度拼接形成最终相机令牌 $\mathbf{g}_i'$，随后追加到池中（Eq. 5）。相机头在预测当前窗口的位姿时，同时关注当前窗口令牌和池中所有历史令牌（Eq. 6），从而获得全局视角。消融实验（Table 6）表明，去除相机令牌池后，相机位姿估计精度大幅下降，证实了这一设计的决定性作用。

### 3. 适用边界与局限

**适用场景**：WinT3R 在室内（7-Scenes、NRGBD）、室外（KITTI）及物体级（DTU、ETH3D）场景中均展现了最优的在线重建性能，且在野外场景（in-the-wild）中保持了照片级真实感的渲染质量（Figure 5）。其实时性（>17 FPS）使其适用于需要即时反馈的应用，如 AR/VR 和机器人导航。

**已知局限**：

1. **长序列累积误差**：尽管相机令牌池提供了全局上下文，但模型在处理非常长的视频或大量图像时仍存在累积误差问题。这是流式方法的共性挑战——缺乏离线方法那样的全局优化（如全局 BA）来纠正漂移。

2. **训练效率**：流式模型的训练需要顺序传递时序数据，比离线模型需要更长的训练时间。论文明确指出，“设计一种节省训练资源的流式模型仍待解决”。

3. **窗口大小的固有限制**：滑动窗口机制虽然提升了帧间交互质量，但窗口大小（默认 4）限制了单次交互的帧数范围。对于需要长程几何一致性的场景（如大范围场景重建），这一限制可能成为瓶颈。

### 4. 开放问题

从 WinT3R 的设计边界出发，以下问题值得进一步探索：

- **如何避免长序列累积误差？** 可能的路径包括：引入轻量级的在线闭环检测与校正模块，或在相机令牌池中设计遗忘/压缩机制以优先保留关键帧信息。
- **如何设计节省计算资源的流式训练方案？** 这涉及训练范式的根本性改进，例如利用课程学习（curriculum learning）逐步增加序列长度，或设计可并行的窗口级训练策略以减少时序依赖。
- **窗口大小是否可以自适应？** 当前固定窗口大小（4）在简单场景中可能冗余，在复杂场景中可能不足。自适应窗口机制（基于运动速度或场景复杂度动态调整）是一个自然延伸方向。
- **相机令牌池的压缩极限在哪里？** 1536 维是否已达到信息论下界？更激进的压缩（如量化或哈希）是否能进一步降低存储开销，使超长序列（数千帧）的实时处理成为可能？

### 5. 知识库定位

WinT3R 在流式三维重建知识库中的定位可以概括为：**首次证明了“窗口内直接交互 + 全局轻量记忆”的架构可以在保持实时性的前提下，显著缩小在线方法与离线方法之间的性能差距**。其滑动窗口机制和相机令牌池设计为后续工作提供了两个可直接复用的模块，而点云头部的轻量化改造（从 DPT 头部替换为 ConvHead）则为工程部署提供了实用参考。

## 原文 PDF

![[paperPDFs/ICLR_2026/WinT3R_Window_Based_Streaming_Reconstruction_with_Camera_Token_Pool_5fa1e9c4d8aa.pdf]]
