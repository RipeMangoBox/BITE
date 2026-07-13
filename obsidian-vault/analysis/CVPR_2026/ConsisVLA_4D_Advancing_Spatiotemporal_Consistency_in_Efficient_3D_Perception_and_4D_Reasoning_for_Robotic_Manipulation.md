---
title: "ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ConsisVLA_4D_Advancing_Spatiotemporal_Consistency_in_Efficient_3D_Perception_and_4D_Reasoning_for_Robotic_Manipulation.pdf
project_link: null
code_link: "https://github.com/JiuTian-VL/ConsisVLA-4D"
aliases:
- C4
- ConsisVLA-4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入多视角对象语义对齐（CV-Aligner）与空间几何关系聚合（CO-Fuser），并结合跨场景时空推理（CS-Thinker）来建立从3D感知到4D推理的一致性纽带。
primary_logic: 受人类通过双目视觉和大脑预测维持时空一致性启发，利用指令驱动对象选择和跨视角几何聚合来学习隐式动态与深度知识，从而以极低的视觉冗余实现鲁棒的4D推理。
claims:
- ConsisVLA-4D在LIBERO基准上平均成功率达到98.1%，相较于OpenVLA在性能和推理速度上分别提升21.6%和2.3倍。
- ConsisVLA-4D在LIBERO四个子套件（Spatial, Object, Goal, Long）上均取得领先，其中Object达到99.8%。
- 消融实验确认CV-Aligner和CO-Fuser对时空一致性的关键作用：移除前者使模拟成功率下降7.0%，真实任务下降10.0%；移除后者分别下降8.2%和13.3%。
- LIBERO 上 平均成功率 (%) = 98.1
---

# ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation

> [!tip] 核心洞察
> 受人类通过双目视觉和大脑预测维持时空一致性启发，利用指令驱动对象选择和跨视角几何聚合来学习隐式动态与深度知识，从而以极低的视觉冗余实现鲁棒的4D推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | ConsisVLA-4D：推进高效3D感知与4D推理的时空一致性以实现机器人操作 |
| 英文题名 | ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.05126) · [Code](https://github.com/JiuTian-VL/ConsisVLA-4D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ConsisVLA-4D |
| Dataset | LIBERO, ManiSkill2, Real-World Long-Horizon |

> [!tip] 效果简介
> - LIBERO 上，平均成功率 (%) 98.1 vs 76.5 (OpenVLA) (+21.6%)。
> - ManiSkill2 上，平均成功率 (%) 94.3 vs 88.7 (OpenVLA-OFT) (+5.6%)。
> - Real-World Long-Horizon (Galaxea R1 Lite) 上，平均任务完成率 (%) 70.0 vs 68.3 (OpenVLA-OFT) (+1.7%)。

## 概要

当前视觉-语言-动作（VLA）模型在机器人操作中面临一个核心瓶颈：3D空间理解依赖额外传感器（如点云、深度图）导致计算开销高企，且普遍缺乏与语言指令对齐的时空一致性推理能力，难以应对动态场景中的对象歧义和空间关系模糊。**ConsisVLA-4D** 针对这一问题，提出了一条从高效3D感知到4D推理的统一路径，其核心思路是受人类双目视觉与大脑预测维持时空一致性的启发，利用指令驱动的对象选择和跨视角几何聚合来学习隐式动态与深度知识，从而以极低的视觉冗余实现鲁棒的动作预测。

方法上，ConsisVLA-4D 构建了三个关键模块：**CV-Aligner**（跨视图对齐器）通过显式语义对象选择（ES-Selection）将视觉token压缩至原始的1/8，仅保留与指令相关的对象，并确保同一对象在多视角下的身份一致性；**CO-Fuser**（跨对象融合器）通过分组融合（Group-Fusion）和隐式几何聚合（IG-Aggregation）消除单视图深度歧义，建立跨对象空间几何关系的一致性；**CS-Thinker**（跨场景推理器）在训练中学习未来动态对象和全局深度的隐式知识，推理时通过时空一致性注意力（SC-Attn）并行解码动作chunk，无需显式输出动态或深度信息。

在LIBERO基准上，ConsisVLA-4D取得了**98.1%**的平均成功率，较OpenVLA提升21.6%，推理速度提升2.3倍；在四个子套件（Spatial、Object、Goal、Long）上均取得领先，其中Object套件达到99.8%。消融实验证实，CV-Aligner和CO-Fuser对时空一致性至关重要：移除前者使模拟成功率下降7.0%、真实任务下降10.0%；移除后者分别下降8.2%和13.3%。这些结果表明，通过精简的视觉表征和隐式时空知识学习，ConsisVLA-4D在性能与效率之间取得了显著突破。

### 机器人操作中的视觉-语言-动作模型

视觉-语言-动作（VLA）模型已成为机器人操作领域的核心范式，其目标是将自然语言指令与视觉观察映射为可执行的动作序列。近年来，一系列代表性工作推动了该方向的发展：**Diffusion Policy**（RSS 2023）以扩散模型生成动作轨迹，**Octo**（RSS 2024）构建了通用的机器人策略框架，**OpenVLA**（CoRL 2024）则率先开源了大规模VLA模型，推动了社区的广泛复现与改进。在此基础上，**OpenVLA-OFT**（RSS 2025）和**π0**（RSS 2025）等优化版本进一步提升了策略的适应性与推理效率。

然而，上述方法在空间理解上存在根本性局限：它们通常将2D视觉输入直接映射为动作，缺乏对三维场景结构的显式建模。当任务涉及对象间的空间关系推理（如“将碗放在饼干盒左侧”）或多视角操作时，纯2D方法难以消解对象位置的歧义性，导致动作预测的时空一致性不足。

### 现有3D/4D方法的瓶颈

为弥补2D方法的不足，学术界探索了多种引入三维信息的技术路线（Figure 1）。范式A直接使用显式3D/4D输入（如点云、深度图、历史帧），但依赖额外传感器，计算开销高昂；范式B将2D输入投影至3D空间，但投影过程引入的误差难以消除；范式C从2D观测中预测3D表示，虽降低了对硬件的依赖，却仍面临尺度歧义和跨视角不一致的挑战。

近期，一些VLA工作尝试将时空信息纳入建模。**TraceVLA**（ICLR 2025）引入时序追踪，**CoT-VLA**（CVPR 2025）利用链式思维增强推理，**SpatialVLA**（RSS 2025）和**GeoVLA**（arXiv 2025）分别从空间和3D角度改进感知。然而，这些方法仍存在两个关键缺口：

1. **视觉冗余与计算效率**：多数方法使用全量视觉token（如256个），未根据指令筛选任务相关对象，导致大量无关区域参与计算，拖累推理速度。
2. **时空一致性断裂**：现有方法要么仅关注空间感知，要么仅预测未来帧，缺乏将3D感知与4D推理统一在一致性框架内的机制。这导致模型在动态场景中难以维持跨时刻、跨视角的对象身份一致性。

### 核心瓶颈与本文动机

综合上述分析，当前VLA模型面临的核心瓶颈可概括为：**3D空间理解依赖额外传感器导致高计算开销，且缺乏与指令对齐的时空一致性推理能力，难以应对动态场景中的对象歧义和空间关系模糊**。

受人类视觉系统的启发——人类通过双目视觉建立空间一致性，并利用大脑预测机制维持时间一致性——本文提出**ConsisVLA-4D**框架，旨在以极低的视觉冗余实现从3D感知到4D推理的时空一致性。具体而言，我们引入**跨视图对象语义对齐（CV-Aligner）**与**跨对象空间几何关系聚合（CO-Fuser）**来确保空间域的一致性，并通过**跨场景时空推理（CS-Thinker）**学习隐式动态与深度知识，在时间域上延续这种一致性，从而构建从3D到4D的完整一致性纽带。

## 核心方法与创新机理

ConsisVLA-4D 的核心创新在于首次将 VLA 模型从“3D 感知”推进到“4D 推理”，并在极低的视觉冗余（仅保留约 1/8 的原始视觉 token）下实现了时空一致的鲁棒操作。其关键突破体现在三个紧密耦合的 **changed slots** 上：

### 1. 从全量视觉输入到指令驱动的稀疏对象选择

现有 VLA 模型（如 OpenVLA）通常使用全量视觉 token（256 个），缺乏与语言指令的相关性筛选，导致大量冗余计算和对象歧义。ConsisVLA-4D 通过 **CV-Aligner** 中的 **Explicit Semantic Object Selection（ES-Selection）** 改变了这一范式：先对 SigLIP 视觉 token 施加 FiLM 调制以注入指令信息，再计算调制后 token 与指令嵌入的余弦相似度，最后以 Top‑K 策略保留仅 1/8（32 个）的指令相关对象 token。这一设计使得模型能够精准锁定任务相关物体，从源头消除了无关视觉信息的干扰。

### 2. 从单视图深度歧义到多视图隐式几何关系聚合

传统方法依赖单视图深度估计或额外传感器（点云/深度图）来获取空间信息，前者存在尺度歧义，后者显著增加计算开销。ConsisVLA-4D 的 **CO-Fuser** 模块彻底改变了这一局面：它采用跨三视图的 **Group-Fusion** 策略，以余弦衰减权重逐层聚合 DINOv2 几何特征与 VGGT 3D 特征；随后通过 **IG-Aggregation**（块状因果自注意力）融合跨视图几何 token，生成紧凑的隐式几何表示。这一设计以仅 1/12–1/8 的原始视觉 token 代价，消除了多视角下对象位置的几何歧义。

### 3. 从无时序建模到训练时隐式时空知识学习

现有 VLA 在推理时缺乏与指令对齐的场景动态建模，仅预测未来帧或直接输出动作，难以应对动态场景中的时空一致性挑战。ConsisVLA-4D 的 **CS-Thinker** 引入了一个巧妙的“训练-推理”不对称设计：训练阶段，模型通过 CoTracker 和 Depth-Anything 监督，学习预测动态对象的未来位置（$\mathcal{L}_{\mathrm{dyn-4D}}$）和跨视图全局深度（$\mathcal{L}_{\mathrm{dep-4D}}$），从而内化隐式的局部动态与全局深度知识；推理阶段，**SC-Attn** 仅使用训练中习得的隐式知识，无需显式输出动态/深度预测，即可并行解码动作 chunk。这种“学而不露”的策略使模型在推理时兼具时空一致性与高效性。

### 创新间的因果链路

三个 changed slots 形成了清晰的因果闭环：**CV-Aligner** 提供指令对齐的稀疏对象 token → **CO-Fuser** 在此基础上聚合跨对象空间几何关系 → **CS-Thinker** 利用前两者提供的语义与几何隐式知识进行时空推理。消融实验强有力地验证了这一链路：移除 CV-Aligner 使模拟任务成功率下降 7.0%、真实任务下降 10.0%；移除 CO-Fuser 分别下降 8.2% 和 13.3%；移除 CS-Thinker 中的动态对象和深度预测使模拟下降 2.7%–4.8%、真实下降 5.7%–11.6%。三者协同作用，最终在 LIBERO 基准上实现了 98.1% 的平均成功率，相较 OpenVLA 提升 21.6%，推理速度提升 2.3 倍。

ConsisVLA-4D 提出了一条从 2D 观测到 3D 感知再到 4D 推理的统一流水线，其核心设计逻辑是：**先构建空间一致的 3D 表示，再将其延伸为时空一致的 4D 推理**。整个框架可概括为 `2D → 3D → 4D` 的两阶段递进结构——3D 感知阶段负责从多视角图像中提取指令相关的对象语义和几何关系，4D 推理阶段则在此基础上学习隐式的动态对象与全局深度知识，以支撑动作预测。

### 输入与编码

系统接收三路视觉输入（主视图 M、左视图 L、右视图 R）和一条语言指令。视觉信号通过两条并行的编码通路处理：

- **语义通路**：SigLIP 编码器将三视图分别映射为语义 token 序列 `z^{sem}`，每个 token 携带语言对齐的语义信息。
- **几何通路**：DINOv2 提取几何视觉特征 `z^{geo}`，利用对比学习保证跨视图一致性；VGGT 则从多视图 RGB 中密集预测深度图、点图和特征网格 `(D, P, G)`，提供显式的 3D 空间信息。

### 3D 感知：空间一致性

3D 感知阶段由两个核心模块串联完成：

1. **CV-Aligner（跨视图对齐器）**：首先通过 FiLM 调制将指令嵌入注入 SigLIP 视觉 token，计算与指令的余弦相似度后进行 Top‑K 选择，仅保留 1/8（256→32）的指令相关对象 token。随后，选中的语义 token 与 VGGT 3D 特征通过 Single-Fusion（交叉注意力 + 残差连接）逐帧融合，生成指令相关的对象 3D 表示 `z^{obj-3D}`。这一过程保证了同一对象在不同视图下的身份一致性。

2. **CO-Fuser（跨对象融合器）**：将 DINOv2 几何特征与 VGGT 3D 特征按余弦衰减权重 `α_l` 逐层加权聚合（Group-Fusion），再通过块状因果自注意力（IG-Aggregation）融合跨视图几何信息，生成紧凑的聚合 3D 表示 `z^{agg-3D}`。此模块消除了单视图下的对象空间关系歧义，压缩比达 1/12–1/8。

### 4D 推理：时空一致性

4D 推理阶段的核心是 **CS-Thinker（跨场景思考器）**，它不直接输出显式的动态预测或深度图，而是在训练中学习隐式知识，推理时仅通过 **SC-Attn（时空一致性注意力）** 并行解码动作 chunk。

具体而言，SC-Attn 接收六类输入：
- 三视图的对象 3D token `z^{obj-3D}`
- 聚合几何 token `z^{agg-3D}`
- 指令嵌入 `t`
- 三组可学习的动态 token（初始化为零，训练时由 CoTracker 监督）
- 一组可学习的深度 token（初始化为零，训练时由 Depth-Anything 监督）
- 可学习的动作 token

训练阶段，动态 token 在对应视图的对象表示和指令引导下，预测动作执行后目标视图中的动态对象区域（以 L2 损失 `L_{dyn-4D}` 监督）；深度 token 则预测跨视图的全局深度（以 L2 损失 `L_{dep-4D}` 监督）。推理时，这些预测作为中间视觉推理信号，与动作 token 一起通过 SC-Attn 并行解码出动作序列。总训练目标为动作损失、动态对象损失和深度损失的联合优化：`L_total = L_action + L_{dyn-4D} + L_{dep-4D}`。

### 模块关系与数据流

整体数据流可总结为：**多视图图像 → 语义/几何/3D 编码 → CV-Aligner 语义选择与融合 → CO-Fuser 几何聚合 → CS-Thinker 隐式时空推理 → 动作输出**。CV-Aligner 和 CO-Fuser 分别解决空间域的对象语义一致性和几何关系一致性问题，CS-Thinker 则将这两类一致性延伸至时间域，形成从 3D 感知到 4D 推理的完整闭环。整个框架仅使用约 1/8 的原始视觉 token，在保证时空一致性的同时实现了显著的效率提升。

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/001_Figure_1.jpg]]
*Figure 1: Comparison with Existing Paradigms. Beyond conventional 2D visual inputs, Para. A employs explicit 3D/4D inputs (e.g., point clouds, depth maps, historical frames), Para. B projects 2D inputs into 3D space, and Para. C predicts 3D representations from 2D observations. In contrast, we extend the paradigm from 3D-Perception to 4D-Reasoning within a unified framework (Para. D): 1) CV-Aligner extracts instructionrelated and cross-correlated spatial objects; 2) CO-Fuser aggregates multi-view geometric relation; 3) CS-Thinker infers actions based on implicit knowledge of future dynamic objects and global depth. ConsisVLA-4D achieves spatiotemporal consistency using only about 1/8 of the original...*

ConsisVLA-4D 的核心设计围绕三个递进模块展开：**CV-Aligner**（跨视图对象语义对齐）、**CO-Fuser**（跨对象空间几何聚合）和 **CS-Thinker**（跨场景时空推理）。三者共同构建从 2D 观测到 3D 感知再到 4D 推理的一致性纽带，其信息流可概括为：

$$2D \xrightarrow{\text{construction}} 3D \xrightarrow{\text{prediction}} 4D$$

### 3D 感知基础：VGGT 密集预测

多视角 RGB 图像 $\mathbf{x}_i$（$i=1,\dots,M$，本工作中 $M=3$，分别对应主视图、左视图、右视图）首先通过 VGGT 提取 3D 空间特征：

$$\mathrm{DPT}\left(f_v^{\mathrm{VGGT}}(\mathbf{x}_i)_{i=1}^M\right) = (D_i, P_i, G_i)_{i=1}^M$$

其中 $D_i$ 为深度图，$P_i$ 为点图，$G_i$ 为特征网格。这一密集预测为后续的跨视图几何对齐提供了尺度感知的 3D 基础。

### CV-Aligner：跨视图对象语义一致性

CV-Aligner 的核心机制是 **显式语义对象选择（ES-Selection）** 与逐帧 **单帧融合（Single-Fusion）**。

**ES-Selection** 首先对 SigLIP 视觉 token $\mathbf{z}_{i,l}^{\mathrm{sem}}$ 施加 FiLM 调制，引入指令嵌入 $\mathbf{t}$：

$$\widetilde{\mathbf{z}}_{i,l}^{\mathrm{sem}} = (\mathbf{1} + \gamma(\mathbf{t})) \odot \mathrm{Self-Attn}(\mathbf{z}_{i,l}^{\mathrm{sem}}) + \beta(\mathbf{t})$$

调制后的 token 与指令嵌入计算余弦相似度，按 Top‑K 策略筛选指令相关对象 token。稀疏化比率 $R=1/8$ 时，视觉 token 从 256 压缩至 32，仅保留约 1/8 的原始视觉输入。

筛选出的语义对象 token 与 VGGT 3D 特征通过 **Single-Fusion** 逐帧融合，生成指令相关的对象 3D 表示：

$$\mathbf{z}_{\{M,L,R\}}^{\mathrm{obj-3D}} = f_{\mathrm{SF}}\left(f_{\mathrm{ES-S}}(\mathbf{z}_{\{M,L,R\}}^{\mathrm{sem}}, \mathbf{t}), \mathbf{z}_{\{M,L,R\}}^{\mathrm{3D}}\right)$$

其中 $f_{\mathrm{SF}}$ 的具体形式为跨注意力与残差连接：

$$\mathbf{z}_{i}^{\mathrm{obj-3D}} = \left( \mathrm{FFN}( \mathrm{Cross-Attn}( \mathbf{z}_{i}^{\mathrm{obj}}, \mathbf{z}_{i}^{\mathrm{3D}} ) ) + \mathrm{Res}( \mathbf{z}_{i}^{\mathrm{obj}} ) \right) \big|_{\mathrm{Layer}=N}$$

这一设计确保同一对象在左、中、右三视图中的语义身份一致，消除跨视图的对象歧义。

### CO-Fuser：跨对象空间几何一致性

CO-Fuser 通过 **Group-Fusion** 和 **IG-Aggregation** 两个子机制聚合多视角几何关系。

**Group-Fusion** 将 DINOv2 几何特征 $\mathbf{z}_l^{\mathrm{geo}}$ 与 VGGT 3D 特征 $\mathbf{z}_l^{\mathrm{3D}}$ 按层加权融合：

$$\mathbf{z}_{l}^{\mathrm{geo-3D}} = (1 - \alpha_{l}) \odot \mathbf{z}_{l}^{\mathrm{geo}} + \alpha_{l} \odot \mathbf{z}_{l}^{\mathrm{3D}}$$

其中 $\alpha_l$ 为可学习权重，按余弦衰减策略逐层变化，使浅层更偏重几何纹理，深层更偏重 3D 结构。

**IG-Aggregation** 采用块状因果自注意力（Block-Wise Causal Self-Attention）融合跨视图几何特征与聚合 token：

$$(\mathbf{z}_{l+1}^{\mathrm{geo-3D}}, \mathbf{z}_{l+1}^{\mathrm{agg-3D}}) = \mathrm{BC-Attn}(\mathbf{z}_{l}^{\mathrm{geo-3D}} \oplus \mathbf{z}_{l}^{\mathrm{agg-3D}})$$

该机制将多视图几何信息压缩至紧凑的隐式表示，压缩比达 1/12–1/8，消除单视图深度估计的尺度歧义，同时避免引入显式点云或深度图带来的计算开销。

### CS-Thinker：跨场景时空一致性推理

CS-Thinker 在训练阶段学习两类隐式知识——**动态对象（Dyn. O.）**和**全局深度（Glob. D.）**，推理时通过 **SC-Attn** 并行解码动作 chunk，不输出显式动态/深度预测。

**SC-Attn** 整合多源信息生成动作输出：

$$\hat{\mathbf{A}} = \mathbf{SC}\mathrm{-}{\mathrm{Attn}}( \mathbf{z}_{\{M,L,R\}}^{\mathrm{obj-3D}}, \mathbf{z}_{\mathcal{L}'}^{\mathrm{agg-3D}}, \mathbf{t}, \mathbf{0}_{\{M,L,R\}}^{\mathrm{dyn-4D}}, \mathbf{0}^{\mathrm{dep-4D}}, \mathbf{0}^{A} )$$

其中 $\mathbf{0}^{\mathrm{dyn-4D}}$ 和 $\mathbf{0}^{\mathrm{dep-4D}}$ 为可学习的隐式查询 token，推理时无需外部动态/深度输入。

**动态对象损失** 监督预测的动态对象与真实动态对象在目标掩码下的 L2 距离：

$$\mathcal{L}_{\mathrm{dyn-4D}} = \big\| (\hat{\mathbf{z}}_{i^*}^{\mathrm{dyn-4D}} \odot \mathbf{m}_{i^*}^{\mathrm{obj-3D}}) - (\mathbf{z}_{i^*}^{\mathrm{dyn-4D}} \odot \mathbf{m}_{i^*}^{\mathrm{obj-3D}}) \big\|_2^2$$

其中 $i^*$ 为固定视角，$\mathbf{m}_{i^*}^{\mathrm{obj-3D}}$ 为对象位置掩码。该损失由 CoTracker 提供监督信号。

**全局深度损失** 监督跨视角预测深度与真实深度的 L2 距离：

$$\mathcal{L}_{\mathrm{dep-4D}} = \sum_{i=1}^{N_i} \big\lVert \hat{\mathbf{z}}_i^{\mathrm{dep-4D}} - \mathbf{z}_i^{\mathrm{dep-4D}} \big\rVert_2^2$$

该损失由 Depth-Anything 提供监督信号。

**总训练目标** 联合优化动作预测与时空一致性：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{action}} + \mathcal{L}_{\mathrm{dyn-4D}} + \mathcal{L}_{\mathrm{dep-4D}}$$

> **关键设计要点**：动态对象和全局深度的预测仅在训练时作为辅助任务提供隐式时空知识，推理时完全移除这些预测头，SC-Attn 仅依赖训练阶段学到的隐式表征进行动作解码。这一设计使得 ConsisVLA-4D 在保持时空一致性的同时，推理效率达到 72.7 Hz（相比 OpenVLA-OFT 的 58.4 Hz 提升 24.5%）。

## 实验与关键发现

### 主结果：LIBERO 基准

ConsisVLA-4D 在 LIBERO 基准的四个子套件上均取得领先，平均成功率达到 **98.1%**，较 OpenVLA（76.5%）提升 **+21.6%**（Table 1）。各子套件细分如下：

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/005_Table_1.jpg]]
*Table 1: Simulation Results on LIBERO. Task success rates across four suites and their overall average*

- **Spatial**：98.8%
- **Object**：99.8%
- **Goal**：98.0%
- **Long**：95.6%

其中 Object 子套件接近饱和（99.8%），表明 CV-Aligner 的指令驱动对象选择在目标识别类任务中几乎消除了歧义。Long 子套件（长序列任务）相对较低（95.6%），但仍远超 OpenVLA 的 72.3%，说明 CS-Thinker 的隐式动态知识有效缓解了长时域动作预测中的误差累积。

在推理效率维度，ConsisVLA-4D 的吞吐量达到 **72.7 Hz**，较 OpenVLA-OFT（58.4 Hz）提升 **+24.5%**（Table 3），同时训练成本更低——这得益于仅保留 1/8 原始视觉 token 的稀疏化策略。

### 主结果：ManiSkill2 与 RoboTwin 2.0

在 ManiSkill2 基准上，ConsisVLA-4D 取得 **94.3%** 的平均成功率，超过 OpenVLA-OFT（88.7%）**+5.6%**（Table 2）。RoboTwin 2.0 的仿真结果（Figure 5）覆盖多样化场景，每任务 100 次试验，进一步验证了框架的泛化能力。

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/006_Table_2.jpg]]
*Table 2: Simulation Results on ManiSkill2. “†” denotes results reproduced under identical settings as ConsisVLA-4D*

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/008_Figure_5.jpg]]
*Figure 5: Simulation Results on RoboTwin 2.0 Benchmark. The tasks cover diverse scenarios, with each task conducted in 100 trials*

### 真实世界长序列任务

在 Galaxea R1 Lite 平台上执行四项长序列操作任务（Figure 6），ConsisVLA-4D 的平均任务完成率为 **70.0%**，略高于 OpenVLA-OFT（68.3%）**+1.7%**（Table 4）。尽管提升幅度小于仿真环境，但考虑到真实世界中视觉噪声、光照变化和机械臂动力学的不确定性，这一结果仍具竞争力。需要指出的是，真实世界评估仅基于 15 次试验，统计显著性需人工验证。

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/011_Figure_6.jpg]]
*Figure 6: Visualization of ConsisVLA-4D performing four long-horizon real-world manipulation tasks on the Galaxea R1 Lite platform, illustrating key execution-stage observations. Red circles highlight fine-grained gripper operations, including grasping bowl edge, peeling banana, holding drawer handle, and pinching cloth corner*

### 消融实验：CV-Aligner 与 CO-Fuser 的关键作用

Table 5 的系统消融揭示了两个核心模块的因果贡献：

![[assets/figures/papers/paper_list_l2277_https_arxiv_org_abs_2605_05126/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on CV-Aligner and CO-Fuser. Ablation components include ES-Selection, Single-Fusion from CV-Aligner, and Group-Fusion, IG-Aggregation from CO-Fuser*

- **移除 CV-Aligner**（包括 ES-Selection 和 Single-Fusion）：仿真成功率下降 **7.0%**，真实任务下降 **10.0%**。这表明指令驱动的对象语义选择与跨视角身份对齐对时空一致性至关重要。
- **移除 CO-Fuser**（包括 Group-Fusion 和 IG-Aggregation）：仿真成功率下降 **8.2%**，真实任务下降 **13.3%**。CO-Fuser 的损失在真实环境中尤为显著，说明多视角几何关系聚合是消除空间歧义的关键瓶颈——单视图深度估计的尺度歧义在真实场景中被放大。

### 消融实验：CS-Thinker 的隐式知识

Table 6 显示，移除 CS-Thinker 中的动态对象预测（Dyn. O.）使仿真成功率下降 **2.7%**，真实任务下降 **5.7%**；移除全局深度预测（Glob. D.）分别下降 **4.8%** 和 **11.6%**。全局深度知识的贡献大于动态对象知识，这与 CO-Fuser 消融结果一致——深度信息的缺失对空间推理的破坏比对象动态建模更严重。

### 稀疏化比率与衰减策略

Table 7 的稀疏化比率消融表明，**R=1/8**（256→32 token）在 LIBERO（98.1%）和真实世界（78.3%）上取得最佳性能-效率平衡。更激进的稀疏化（R=1/16）导致性能显著下降，尤其在真实场景中；更保守的策略（R=1/4）则带来边际性能提升但推理效率降低。

Table 8 对比了 Group-Fusion 中 $\alpha_l$ 的余弦衰减与线性衰减策略，余弦衰减在多数指标上表现更优，验证了深层网络中对几何特征与 3D 特征进行非线性加权融合的合理性。

### 失败模式与局限性

论文未提供系统的失败案例分析，但可从消融结果推断主要失效模式：

1. **单视图歧义**：移除 CO-Fuser 时真实任务成功率骤降 13.3%，说明当多视角几何聚合失效时，模型无法区分外观相似但空间关系不同的对象（如“碗在饼干盒上”vs“碗在饼干盒旁”）。
2. **长时域漂移**：Long 子套件 95.6% 的成功率虽为最高，但仍是四个子套件中最低的，表明 CS-Thinker 的隐式动态预测在超长序列中仍存在累积误差。
3. **分布外泛化**：模型在单视角或单臂场景下的有效性未经验证，隐式动态与深度知识的跨场景迁移能力尚不明确。在完全非结构化的家庭杂乱场景中的鲁棒性需进一步评估。

## 定位与知识库关联

### 1. 与基线工作的关系

ConsisVLA-4D 的提出建立在 VLA（Vision-Language-Action）模型从 2D 感知向 3D/4D 推理演进的谱系中。现有范式可大致分为四类（见 Figure 1）：

- **范式 A（显式 3D/4D 输入）**：直接使用点云、深度图、历史帧等显式 3D/4D 信号。此类方法依赖额外传感器，计算开销高，代表性工作如 **GeoVLA**（arXiv'25）等 3D VLA 模型。
- **范式 B（2D 投影到 3D）**：将 2D 观测投影到 3D 空间进行推理，如 **SpatialVLA**（RSS'25）等空间 VLA。
- **范式 C（从 2D 预测 3D）**：从 2D 观测预测 3D 表示，如 **TraceVLA**（ICLR'25）等引入时空建模的 VLA。
- **范式 D（ConsisVLA-4D）**：从 3D 感知推进到 4D 推理，在统一框架内实现时空一致性，仅使用约 1/8 的原始视觉输入。

在具体基线对比上，ConsisVLA-4D 与以下代表性方法形成直接竞争：

| 基线方法 | 会议/年份 | 方法角色 | 核心差异 |
|---------|----------|---------|---------|
| **Diffusion Policy** | RSS'23 | 经典基线 | 基于扩散的动作生成，缺乏语言指令对齐和显式 3D 理解 |
| **Octo** | RSS'24 | 通用机器人策略 | 大规模预训练 Transformer，但无专门的空间几何建模 |
| **OpenVLA** | CoRL'24 | 开源 VLA | 直接使用全量 256 个视觉 token，无指令相关筛选和时空一致性机制 |
| **OpenVLA-OFT** | RSS'25 | 优化版 VLA | OpenVLA 的微调版本，仍缺乏显式 3D 感知和 4D 推理 |
| **π0** | RSS'25 | 双系统 VLA | 结合快慢双系统，但未引入跨视图对象对齐和隐式时空知识学习 |
| **TraceVLA** | ICLR'25 | 时空 VLA | 引入时序建模，但依赖额外传感器且缺乏指令对齐的跨视图一致性 |
| **CoT-VLA** | CVPR'25 | 链式思维 VLA | 通过思维链增强推理，但未解决 3D 空间歧义问题 |
| **SpatialVLA** | RSS'25 | 空间 VLA | 将 2D 投影到 3D 空间，但单视图深度估计存在尺度歧义 |
| **GeoVLA** | arXiv'25 | 3D VLA | 显式 3D 建模，但依赖点云/深度图等额外传感器，计算开销大 |
| **CogACT** | arXiv'24 | 认知-动作联合 VLA | 联合认知与动作，但缺乏跨场景时空一致性 |
| **Dita** | ICCV'25 | 基础 VLA | 基础架构，未专门优化 3D/4D 推理 |

### 2. 关键改进槽位

ConsisVLA-4D 在三个关键槽位上相对于基线实现了结构性改进：

**槽位 1：视觉特征提取与选择**

- **基线做法**：使用全量视觉 token（如 OpenVLA 的 256 个），无指令相关筛选，导致大量冗余计算和对象歧义。
- **ConsisVLA-4D 做法**：通过 CV-Aligner 中的 FiLM 调制计算视觉 token 与指令的余弦相似度，以 Top-K 选择保留 1/8（32 个）的指令相关对象 token（ES-Selection）。这直接解决了“哪些视觉信息与当前任务相关”的核心问题。

**槽位 2：空间几何关系建模**

- **基线做法**：单视图深度估计存在尺度歧义（如 SpatialVLA），或依赖额外传感器（点云/深度图）增加计算开销（如 GeoVLA）。
- **ConsisVLA-4D 做法**：CO-Fuser 通过跨三视图的 Group-Fusion（余弦衰减权重聚合 VGGT 3D 特征与 DINOv2 几何特征）和 IG-Aggregation（块状因果自注意力）消除多视角对象位置歧义。这在不增加传感器负担的前提下实现了跨对象空间几何一致性。

**槽位 3：时序推理与动作预测**

- **基线做法**：仅预测未来帧（如 TraceVLA），缺乏与指令对齐的场景动态建模；推理时无显式时空知识。
- **ConsisVLA-4D 做法**：CS-Thinker 在训练中学习隐式动态对象（CoTracker 监督）和全局深度知识（Depth-Anything 监督），推理时通过 SC-Attn 并行解码动作 chunk，不使用显式动态/深度输出。这实现了“训练时学习时空知识，推理时高效利用”的范式。

### 3. 适用边界与局限

**已验证的适用场景**：

- 多视角（主视图 + 左/右腕视图）双臂操作任务
- LIBERO 基准的四个子套件（Spatial, Object, Goal, Long）
- ManiSkill2 仿真任务
- 真实世界长时域操作（Galaxea R1 Lite 和 AgileX Cobot Magic 平台）
- 推理效率敏感场景（72.7 Hz 吞吐量，2.3× 速度提升）

**明确局限**：

1. **单视角/单臂场景未验证**：论文主要在多视角双臂任务上评估，单视角或单臂场景下的有效性需要进一步验证。CV-Aligner 的跨视图对齐机制在单视图输入下可能退化为普通的指令条件选择。
2. **跨场景迁移能力不明确**：CS-Thinker 学习到的隐式动态与深度知识局限于训练分布。在训练分布外的新场景（如全新的物体类别、不同的光照条件、不同的机器人平台）中的泛化能力尚不明确。
3. **依赖外部监督信号**：训练阶段需要 CoTracker（点跟踪）和 Depth-Anything（深度估计）提供监督信号，这些预训练模型本身可能引入偏差或误差。
4. **稀疏化比率的固定性**：Top-K 选择策略使用固定比率 R=1/8（消融实验确认该值为最优平衡点），但能否根据任务复杂度自适应调整 K 值尚未探索。

### 4. 开放问题

1. **自适应稀疏化**：CV-Aligner 的 Top-K 选择策略能否根据任务复杂度（如物体数量、场景杂乱度）动态调整 K 值，而非使用固定比率？
2. **非结构化环境鲁棒性**：模型在完全非结构化的动态环境（如家庭杂乱场景、多人协作场景）中的鲁棒性如何？当前评估主要基于结构化实验台场景。
3. **隐式知识的可迁移性**：CS-Thinker 学习到的隐式时空知识（动态对象和全局深度）是否可迁移到其他 VLA 架构或任务（如导航、抓取检测）？
4. **单视角可行性**：能否将多视角输入缩减为仅单视角，同时通过更强的先验知识保持时空一致性？这将大幅降低硬件需求。
5. **自监督替代方案**：训练阶段所需的 CoTracker 和 Depth-Anything 监督是否可被自我监督信号（如多视角一致性损失、时序预测损失）替代，从而减少对外部预训练模型的依赖？
6. **实时闭环控制**：当前推理效率（72.7 Hz）已满足大多数操作任务，但在需要更高频率（>100 Hz）的精细操作任务中是否仍能保持性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/ConsisVLA_4D_Advancing_Spatiotemporal_Consistency_in_Efficient_3D_Perception_and_4D_Reasoning_for_Robotic_Manipulation.pdf]]
