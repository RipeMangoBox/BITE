---
title: "MoRe: Motion-aware Feed-forward 4D Reconstruction Transformer"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/MoRe_Motion_aware_Feed_forward_4D_Reconstruction_Transformer.pdf
project_link: https://hellexf
code_link: null
aliases:
- MoRe
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过训练时注意力强制（attention-forcing）策略，利用运动掩码显式引导相机token关注静态区域，实现运动与场景结构的解耦；配合分组因果注意力，使得模型在保持帧内空间连贯性的同时具备时序因果推理能力，并以类似光束平差（BA）的token聚合机制进行全局优化。
primary_logic: 在训练阶段引入运动掩码作为显式监督，让模型学会在注意力分配中抑制对动态区域的依赖，而不增加推理时的额外计算；同时设计分组因果注意力，在帧内保留全注意力以维持空间一致性，在帧间施加因果约束以支持流式处理，最终通过轻量的全局token聚合补偿因果注意力带来的长程信息损失，从而在实时效率下实现高质量的动态4D重建。
claims:
- 注意力强制策略显著提升相机姿态估计精度。
- 分组因果注意力在深度估计上一致优于标准因果注意力。
- BA-like token 聚合有效降低流式重建的平移与旋转误差。
- 提出的运动门控损失优于KL散度损失，在动静场景下均更稳定。
---

# MoRe: Motion-aware Feed-forward 4D Reconstruction Transformer

> [!tip] 核心洞察
> 在训练阶段引入运动掩码作为显式监督，让模型学会在注意力分配中抑制对动态区域的依赖，而不增加推理时的额外计算；同时设计分组因果注意力，在帧内保留全注意力以维持空间一致性，在帧间施加因果约束以支持流式处理，最终通过轻量的全局token聚合补偿因果注意力带来的长程信息损失，从而在实时效率下实现高质量的动态4D重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoRe：运动感知的前馈式4D重建Transformer |
| 英文题名 | MoRe: Motion-aware Feed-forward 4D Reconstruction Transformer |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05078) · [Project](https://hellexf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoRe |
| Dataset | Sintel, Bonn, TUM-dynamics, KITTI |

> [!tip] 效果简介
> - Sintel 上，ATE↓ 0.1474 (streaming) / 0.0877 (full attn) vs 0.1715 (VGGT FA) (-0.0838 (FA vs VGGT))；Abs Rel↓ 0.254 (streaming) vs 0.387 (VGGT FA) (-0.133)。
> - Bonn 上，ATE↓ 0.0211 (streaming) / 0.0138 (FA) vs 0.0141 (VGGT FA) (+0.0003 (FA) / +0.0070 (streaming vs VGGT FA))。
> - TUM-dynamics 上，ATE↓ 0.0260 (streaming) / 0.0115 (FA) vs 0.0109 (VGGT FA) (+0.0006 (FA) / +0.0151 (streaming vs VGGT FA))。

## 概要

### 问题与瓶颈

从单目视频中重建动态场景的4D几何（逐帧深度、相机姿态、三维点云）是视觉重建的核心难题。现有方法面临两难：**前馈式方法**（如 VGGT、Spann3R、Stream3R）虽推理高效，但大多在静态数据上训练，面对场景中的运动物体时，相机姿态估计和深度预测精度急剧下降——其根源在于模型难以区分“由相机运动引起的视差”与“物体自身运动产生的位移”，导致相机token的错误注意力分配（Figure 3）；**混合优化方法**虽能通过在线优化缓解运动干扰，但计算代价高昂，难以满足实时流处理需求。因此，**核心瓶颈**在于缺少一个能在流式输入下同时高效、准确地解耦运动与静态结构的统一框架。

### 核心方法与洞察

**MoRe** 是一个运动感知的前馈式4D重建Transformer，其核心创新可归结为三个相互协同的机制：

1. **注意力强制训练**：在训练阶段，利用运动掩码作为显式监督，引导相机token的注意力权重偏向静态区域，从而在推理时无需额外计算即可抑制对动态物体的错误关注。这一策略通过**运动门控损失**（Eq. 8）实现——仅当某个图像token对应的区域具有足够高的“静态先验”时，才鼓励相机token对其分配高于基线C的注意力权重，避免了KL散度损失在大面积静态场景下的归一化问题（Table 7）。

2. **分组因果注意力**：为同时满足流式推理的因果约束和帧内空间一致性，MoRe设计了分组因果注意力（Figure 4）——帧内token之间保持全注意力以维持空间连贯性，帧间则施加因果掩码以支持在线处理。相比标准因果注意力，这一设计在深度估计上带来一致且显著的提升（Sintel Abs Rel: 0.254 vs 0.277, Table 4）。

3. **BA-like全局token聚合**：流式因果注意力天然存在长程信息损失。MoRe在后处理阶段对所有帧的缓存键值对进行全局注意力（Eq. 5），以类似光束平差的方式优化相机token，补偿时序因果推理带来的漂移，有效降低平移与旋转误差（Table 3）。

### 主要结果

在多个动态数据集上，MoRe全面超越了现有流式和全注意力方法：

- **相机姿态估计**（Table 1）：在动态场景Sintel上，MoRe流式模型ATE仅0.1474，优于Stream3R（0.1715）等流式方法；全注意力版本ATE进一步降至0.0877，超越VGGT（0.1715）和π³。
- **视频深度估计**（Table 2）：Sintel上Abs Rel达到0.254，相比VGGT的0.387降低35%；KITTI上Abs Rel为0.072，与VGGT持平。
- **推理效率**（Table 5）：KITTI上FPS达30.09，超过Stream3Rβ的23.48，在实时性与重建质量之间取得最优平衡。
- **静态场景泛化**（Table 6）：在Co3Dv2上，全注意力MoRe的AUC@30达91.42，超越所有对比方法，证明运动感知设计并未损害静态场景性能。

### 方法谱系与知识库定位

MoRe建立在**前馈式多视图重建**的范式之上，直接继承自Dust3R和VGGT的“视觉token+相机token”架构与置信度加权回归损失。其关键改进在于**引入运动感知**，将原本面向静态场景的框架扩展至动态4D重建：

- 相比**VGGT**（全注意力静态重建基础模型），MoRe通过注意力强制训练和分组因果注意力，使模型在动态场景下不再混淆运动与结构。
- 相比**Stream3R / CUT3R / Spann3R**（流式重建方法），MoRe增加了运动掩码监督和BA-like全局聚合，显著提升了姿态精度和时序一致性。
- 相比**MapAnything / Fast3R / FLARE**（全注意力重建方法），MoRe在保持或超越其精度的同时，支持流式推理。
- 相比**π³**（静态场景顶尖方法），MoRe在动态场景下展现出明显优势，且推理速度更快。

### 局限与开放问题

MoRe的性能严重依赖运动掩码标注的质量；当前前馈架构难以捕捉超出训练时间窗口的极长时依赖和复杂动态交互；在极快、非刚性运动或严重运动模糊场景下，注意力对齐可能失效。未来方向包括：减少对高质量运动标注的依赖（如自监督运动解耦）、扩展前馈架构以捕获更长时序依赖、显式建模遮挡与外观剧变以消除重建伪影。

### 动态4D重建：从静态先验到运动感知的范式缺口

从视频序列中同时恢复相机姿态与场景三维几何是计算机视觉的核心问题。近年来，基于Transformer的前馈式重建方法（如 **VGGT**、**DUSt3R**、**Spann3R**、**CUT3R**）在静态场景上取得了令人瞩目的进展——它们无需逐场景优化，仅通过单次前向传播即可从图像中直接回归深度图、点云和相机参数，在ScanNet、Co3Dv2等静态基准上展现出接近甚至超越传统优化方法的精度。然而，这些方法的成功建立在一个隐含假设之上：**场景是静止的**。

现实世界充满运动。当场景中存在移动的行人、行驶的车辆或摆动的物体时，现有前馈方法面临系统性崩溃。核心瓶颈在于：**动态物体严重干扰了相机姿态估计与三维重建的耦合推理**。在全注意力架构中，相机token（用于回归相机参数的专用表示）会不加区分地关注图像中的所有区域——包括正在运动的物体。如 **Figure 3** 所示，VGGT的相机token注意力图在动态场景中明显混淆了运动物体与静态背景，导致模型无法准确区分“由相机运动引起的视差”与“由物体自身运动引起的位移”。这种混淆直接转化为深度估计的畸变和相机轨迹的漂移。

### 现有路线的两难困境

面对动态场景，当前方法大致分为两条路线，但均存在根本性局限：

**路线一：混合优化方法。** 传统SLAM和SfM系统通过鲁棒估计（如RANSAC）和局部BA来剔除动态外点，但计算成本高昂，难以实现实时流处理。基于学习的优化方法（如 **FLARE**、**π³**）虽提升了鲁棒性，仍依赖迭代求解，无法满足前馈式的效率需求。

**路线二：前馈式流式方法。** 为支持在线处理，**Stream3R**、**CUT3R** 等方法采用因果注意力机制，使每帧只能访问历史信息。然而，标准因果注意力在帧内也施加了单向约束，破坏了单帧内部的空间连贯性；更重要的是，这些方法在训练时并未显式建模运动与静态结构的解耦，面对大幅物体运动或快速相机移动时精度急剧下降。

**核心缺口由此显现**：缺少一个能在流式输入下，同时高效、准确地解耦运动与静态结构的统一框架。

### MoRe的切入点：训练时显式引导，推理时零额外代价

本文提出的 **MoRe**（Motion-aware Feed-forward 4D Reconstruction Transformer）直接针对上述缺口。其核心洞察是：**运动解耦的能力可以通过训练时的显式监督来习得，而不需要在推理阶段引入额外计算**。

具体而言，MoRe在训练阶段引入**运动掩码**作为辅助监督信号，通过一种名为“注意力强制”（attention-forcing）的策略，显式引导相机token的注意力分布偏向静态区域。在推理时，模型无需运动掩码作为输入，仅凭训练中习得的注意力偏好即可自然抑制对动态物体的依赖。同时，MoRe设计了**分组因果注意力**（grouped causal attention）——帧内保留全注意力以维持空间一致性，帧间施加因果约束以支持流式处理——并通过轻量的**BA-like全局token聚合**补偿因果注意力带来的长程信息损失。

这一设计使得MoRe在保持实时推理效率（KITTI上30 FPS，**Table 5**）的同时，在多个动态数据集上全面超越现有流式方法：Sintel上ATE降至0.1474（**Table 1**），Abs Rel降至0.254（**Table 2**），并在Co3Dv2静态场景上以91.42 AUC@30验证了其泛化能力（**Table 6**）。

## 核心方法与创新机理

MoRe 的核心创新在于通过**训练时的注意力强制（attention-forcing）策略**，在不增加推理计算的前提下，实现动态场景中运动与静态结构的显式解耦。这一设计直击当前前馈式重建方法的根本瓶颈：现有模型（如 VGGT）的相机 token 在注意力分配中会混淆运动物体与静态背景区域（见 Figure 3），导致动态场景下相机姿态估计和深度重建精度大幅下降。

### 创新一：运动感知的注意力强制训练

MoRe 引入运动掩码作为训练时的辅助监督信号，而非推理时的显式输入。具体而言，模型为每个图像 token $i$ 计算一个静态先验分数 $a_i$：

$$a_{i} = 1 - \frac{1}{s^{2}} \sum_{(u,v) \in m_{i}} m_{i}(u,v)$$

该分数反映该 token 对应图像块中静态像素的比例。在此基础上，提出**运动门控注意力对齐损失**：

$$\mathcal{L}_{\mathrm{attn}} = \frac{1}{M} \sum_{i=1}^{M} \max(0, a_{i} - C) \cdot \alpha_{i}$$

该损失仅在静态先验足够高（$a_i > C$）时才鼓励相机 token 向对应图像 token 分配注意力权重，从而**主动抑制对动态区域的关注**。消融实验证实，该策略将 Sintel 上的 ATE 从 0.163 降至 0.147（Table 3），且注意力可视化（Figure 10）清晰显示训练后的相机 token 注意力图更加干净，不再受运动物体干扰。与之对比，使用 KL 散度损失替代该门控损失时，Sintel ATE 退化至 0.185（Table 7），表明门控设计的必要性。

### 创新二：分组因果注意力机制

为支持流式推理，传统方案采用标准因果注意力，即每个 token 只能关注当前及之前的 token。但这破坏了同一帧内图像 token 之间的空间双向交互，损害空间一致性。MoRe 提出**分组因果注意力**（Grouped Causal Attention, Figure 4）：帧内图像 token 之间保持全注意力（双向），帧间则施加因果约束。这使得模型在保留时序因果推理能力的同时，维持帧内空间连贯性。消融表明，分组因果注意力在深度估计上一致优于标准因果注意力——Sintel Abs Rel 从 0.277 降至 0.254，KITTI Abs Rel 从 0.079 降至 0.072（Table 4）。

### 创新三：类光束平差的全局 token 聚合

因果注意力天然存在长程信息损失。为补偿这一问题，MoRe 在序列处理完毕后，对所有帧的缓存键值对执行一次轻量的全局注意力，优化相机 token：

$$\mathbf{C}_{t}^{\mathrm{opt}} = \mathrm{Attn}( \mathbf{Q}_{t}^{\mathrm{cam}}, [\mathbf{K}_{1:T}], [\mathbf{V}_{1:T}] )$$

该操作类似于光束平差（Bundle Adjustment）的全局优化步骤，仅增加极小的计算开销，却有效改善长期漂移。消融显示，去除该模块后 Sintel RPE_trans 从 0.082 升至 0.085，RPE_rot 从 0.616 升至 0.619（Table 3）。

### 与 baseline 的 changed slots 总结

| 设计维度 | 现有方法（VGGT / 流式方法） | MoRe 方案 | 证据 |
|---------|---------------------------|----------|------|
| 注意力机制 | 标准因果注意力或全局注意力，未区分动静区域 | 分组因果注意力 + 注意力强制训练，使相机 token 偏向静态区域 | Table 3, Table 4, Figure 10 |
| 训练监督 | 仅依赖深度、点云和相机姿态回归损失 | 额外引入运动掩码监督的注意力对齐损失，显式解耦运动与结构 | Table 7, Eq. (8) |
| 全局一致性 | 流式方法无额外全局优化步骤 | BA-like token 聚合，利用全序列缓存特征优化相机姿态 | Table 3, Eq. (5), Figure 5 |

这三项创新协同作用：注意力强制训练赋予模型运动感知能力，分组因果注意力保障流式推理的时空一致性，BA-like 聚合弥补因果注意力的长程信息损失，最终在实时效率下实现高质量的动态 4D 重建。

MoRe 是一个前馈式 4D 重建 Transformer，专为流式（streaming）输入设计，在单目前向推理中联合预测每帧的深度图、相机姿态、动态点云图和运动掩码。其整体 pipeline 围绕三个核心设计展开：**运动感知的注意力强制训练**、**分组因果注意力机制**以及**类光束平差的全局 token 聚合**，在保持实时推理效率的前提下实现了动态场景中运动与静态结构的高效解耦。

### 输入输出流

模型接收单目视频帧序列 $\{I_t\}_{t=1}^T$，以在线方式逐帧处理。在第 $t$ 时刻，模型利用之前累积的缓存信息 $\{C_t\}_{t=1}^{T-1}$ 和上一帧图像 $I_{T-1}$，预测当前帧的深度图 $D_t$、相机参数 $g_t$、动态点云 $P_t$ 以及运动掩码 $M_t$：

$$
\{ D_{t}, g_{t}, P_{t}, M_{t} \}_{t=1}^{T} = f_{\theta}( \{ C_{t} \}_{t=1}^{T-1}, I_{T-1} )
$$

运动掩码仅在训练阶段作为辅助监督信号，不参与推理输入，因此模型在部署时无需显式提供运动标注。

### 核心模块与数据流

如图 2 所示，整体架构由以下模块串联构成：

1. **图像 Token 化与特征提取**：每帧图像经视觉编码器转换为图像 token 序列，同时初始化专用的相机 token（camera token），用于后续相机姿态的全局推理。

2. **分组因果注意力层**：这是 MoRe 的核心时空推理模块。与标准因果注意力不同，分组因果注意力在帧内保留全注意力（双向交互），以维持单帧内的空间一致性；在帧间施加因果约束（仅允许历史帧到当前帧的单向交互），从而支持流式处理。这种设计使模型在具备时序因果推理能力的同时，不会因帧内 token 排序而损失空间连贯性（见 Figure 4）。

3. **相机 Token 分支与注意力强制训练**：在训练阶段，相机 token 对图像 token 的注意力分布受到运动掩码的显式监督。具体而言，每个图像 token 根据其对应图像区域在运动掩码中的平均值计算静态先验分数 $a_i$：
   $$
   a_{i} = 1 - \frac{1}{s^{2}} \sum_{(u,v) \in m_{i}} m_{i}(u,v)
   $$
   运动门控注意力对齐损失 $\mathcal{L}_{\mathrm{attn}}$ 仅在静态先验足够高时，鼓励相机 token 的注意力权重大于基线 $C$，从而抑制对动态区域的关注。这一策略使模型学会在注意力分配中主动偏向静态结构，而不增加推理时的计算开销。

4. **多任务预测头**：经时空注意力处理后的特征分别输入多个预测头，输出深度图、点云图、相机参数和运动掩码。深度和点云图采用置信度加权回归损失 $\mathcal{L}_{\mathrm{conf}}$ 监督，运动掩码通过二值交叉熵损失 $\mathcal{L}_{\mathrm{motion}}$ 监督，相机姿态通过所有帧对之间的相对旋转角度误差与相对平移 L1 距离的平均值 $\mathcal{L}_{\mathrm{cam}}$ 监督。

5. **流式推理与 KV 缓存**：推理时，模型利用分组因果注意力的特性，逐步处理输入帧并复用键值（KV）缓存，大幅降低逐帧计算量，实现约 30 FPS 的实时推理速度（Table 5）。

6. **BA-like 全局 Token 聚合**：因果注意力固有的信息单向流动可能导致长程几何一致性下降。为此，MoRe 在完整序列处理完毕后，对所有帧的缓存键值对执行一次轻量的全局注意力，优化相机 token：
   $$
   \mathbf{C}_{t}^{\mathrm{opt}} = \mathrm{Attn}( \mathbf{Q}_{t}^{\mathrm{cam}}, [\mathbf{K}_{1:T}], [\mathbf{V}_{1:T}] )
   $$
   这一聚合机制在功能上类似于光束平差（BA）的全局优化步骤，以极低的额外计算成本补偿因果注意力的长程信息损失，有效降低平移与旋转漂移（Table 3 消融实验证实，移除该模块后 Sintel RPE_trans 从 0.082 增至 0.085）。

### 训练与推理的解耦设计

值得注意的是，MoRe 的运动解耦能力完全通过训练阶段的注意力强制策略获得——运动掩码仅在训练时作为监督信号引导注意力分布，推理阶段无需任何运动先验。这种“训练时注入先验、推理时零额外成本”的设计，使得模型在保持实时流式处理能力的同时，显著提升了对动态场景的鲁棒性。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. During training, an attention-forcing mechanism aligns the attention weights with ground-truth motion masks, enabling the model to effectively disentangle dynamic motion from static scene structure. For streaming reconstruction task, MoRe is based on a causal transformer where global attention is replaced by aggregated causal attention*

### 3.1 问题形式化：从静态重建到运动感知流式重建

MoRe 将传统前馈三维重建扩展为运动感知的流式 4D 重建。基础流式重建公式为：

$$
\{ D_{t}, g_{t}, P_{t} \}_{t=1}^{T} = f_{\theta}( \{ C_{t} \}_{t=1}^{T-1}, I_{T-1} ) \tag{1}
$$

其中 $D_t$ 为当前帧深度图，$g_t$ 为相机参数，$P_t$ 为动态点云图，$C_t$ 为历史帧的缓存信息，$I_{T-1}$ 为上一帧图像。该公式的核心约束在于：模型仅能访问过去帧的信息，必须在线输出当前帧的全部几何与运动估计。

为引入运动感知能力，MoRe 将输出扩展为包含运动掩码 $M_t$：

$$
\{ D_{t}, g_{t}, P_{t}, M_{t} \}_{t=1}^{T} = f_{\theta}( \{ C_{t} \}_{t=1}^{T-1}, I_{T-1} ) \tag{2}
$$

关键设计在于：运动掩码仅作为训练时的辅助监督信号，推理阶段不依赖运动掩码作为显式输入。这确保了流式推理的效率不受影响，同时通过训练阶段的运动对齐监督，使模型学会隐式解耦动静结构。

### 3.2 注意力强制策略：运动对齐的注意力训练

注意力强制（attention-forcing）是 MoRe 实现运动解耦的核心机制。其动机源于对 VGGT 的观察（Figure 3）：相机 token 在注意力分配中倾向于混淆运动物体与静态背景，导致动态场景下姿态估计精度大幅下降。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/003_Figure_3.jpg]]
*Figure 3: Attention Map Visualization. We visualize the attention map of the camera token within VGGT [39] and observe that the model tends to confuse moving objects with static background regions, which accounts for the degradation in prediction accuracy*

**运动先验分数计算**。对于每个图像 token $i$，利用其对应图像块的运动掩码真值计算静态先验分数：

$$
a_{i} = 1 - \frac{1}{s^{2}} \sum_{(u,v) \in m_{i}} m_{i}(u,v) \tag{3}
$$

其中 $s$ 为 token 对应的图像块边长，$m_i(u,v)$ 为运动掩码在像素 $(u,v)$ 处的二值（1 表示运动，0 表示静态）。$a_i$ 的值域为 $[0,1]$，值越高表示该 token 对应的区域越可能是静态的。

**运动门控注意力对齐损失**。基于静态先验分数，MoRe 设计了运动门控损失来监督相机 token 对图像 token 的注意力分布：

$$
\mathcal{L}_{\mathrm{attn}} = \frac{1}{M} \sum_{i=1}^{M} \max(0, a_{i} - C) \cdot \alpha_{i} \tag{8}
$$

其中 $\alpha_i$ 为相机 token 对图像 token $i$ 的注意力权重，$C$ 为基线阈值。该损失的关键设计在于门控机制：仅当静态先验 $a_i$ 足够高（超过阈值 $C$）时，才鼓励注意力权重 $\alpha_i$ 增大；对于运动区域的 token（$a_i$ 较低），梯度被门控截断，不施加注意力约束。这种非对称设计使模型学会在注意力分配中主动抑制对动态区域的依赖，而不需要显式惩罚运动区域的注意力权重。

与 KL 散度损失相比，运动门控损失的优越性在消融实验中得到验证（Table 7）：Sintel ATE 从 0.185（KL 损失）降至 0.147（运动门控损失），TUM-dynamics ATE 从 0.029 降至 0.026。

### 3.3 分组因果注意力：帧内全注意与帧间因果约束

为使模型支持流式推理，传统做法是采用标准因果注意力，即每个 token 只能关注时间上先于自身的 token。但这种设计破坏了同一帧内图像 token 之间的空间双向交互，导致空间一致性受损。

**分组因果注意力（Grouped Causal Attention, GCA）** 的核心思想是：将注意力掩码按帧分组，帧内允许全注意力（双向），帧间保持因果约束（单向）。公式表示为：

$$
F_{t} = \mathrm{Attn}( \mathbf{Q}_{t}, [\mathbf{K}_{1:t-1}, \mathbf{K}_{t}], [\mathbf{V}_{1:t-1}, \mathbf{V}_{t}] ) \tag{4}
$$

其中 $\mathbf{Q}_t$ 为第 $t$ 帧的查询，$[\mathbf{K}_{1:t-1}, \mathbf{K}_t]$ 和 $[\mathbf{V}_{1:t-1}, \mathbf{V}_t]$ 为累积的历史键值对与当前帧键值对的拼接。分组因果注意力的关键特性在于：当前帧 $t$ 内的所有 token 可以相互关注（帧内全注意），但对历史帧 $1:t-1$ 的访问是因果的。

消融实验（Table 4）验证了 GCA 的有效性：将 GCA 替换为标准因果注意力后，Sintel Abs Rel 从 0.254 退化到 0.277，KITTI Abs Rel 从 0.072 退化到 0.079，表明帧内全注意力对维持空间一致性至关重要。

### 3.4 BA-like 全局 Token 聚合：补偿因果注意力的长程信息损失

因果注意力的固有限制在于：当前帧无法关注未来帧，导致全局几何一致性受损。MoRe 通过在序列处理完毕后执行一次轻量的后处理步骤来补偿这一损失，该步骤被类比为光束平差（Bundle Adjustment, BA）。

具体而言，对于每个帧的相机 token，复制一份副本并对所有历史帧的缓存键值对执行全局注意力：

$$
\mathbf{C}_{t}^{\mathrm{opt}} = \mathrm{Attn}( \mathbf{Q}_{t}^{\mathrm{cam}}, [\mathbf{K}_{1:T}], [\mathbf{V}_{1:T}] ) \tag{5}
$$

其中 $\mathbf{Q}_{t}^{\mathrm{cam}}$ 为复制后的相机 token 查询，$[\mathbf{K}_{1:T}]$ 和 $[\mathbf{V}_{1:T}]$ 为全部 $T$ 帧的缓存键值对。该操作使相机 token 能够利用完整的序列上下文进行全局优化，类似于 BA 中联合优化所有相机位姿和三维点的过程。

消融实验（Table 3）表明，去除 BA-like 聚合后，Sintel RPE_trans 从 0.082 增加到 0.085，RPE_rot 从 0.616 增加到 0.619，证实了该模块对降低流式重建漂移的贡献。

### 3.5 多任务训练目标

MoRe 的训练目标由四个损失函数组成：

**置信度加权回归损失**，用于深度图和点云图的监督：

$$
\mathcal{L}_{\mathrm{conf}} = \sum_{i=1}^{N} \Big( \hat{c}_{i} \| \hat{y}_{i} - y_{i} \|_{2}^{2} - \lambda \log(\hat{c}_{i}) \Big) \tag{6}
$$

其中 $\hat{y}_i$ 为预测值，$y_i$ 为真值，$\hat{c}_i$ 为预测置信度，第二项防止置信度退化到零。

**运动掩码二值交叉熵损失**：

$$
\mathcal{L}_{\mathrm{motion}} = -\frac{1}{N} \sum_{i=1}^{N} \left[ M_{i} \log(\hat{M}_{i}) + (1-M_{i}) \log(1-\hat{M}_{i}) \right] \tag{7}
$$

监督每个像素是否属于动态区域。

**注意力对齐损失** $\mathcal{L}_{\mathrm{attn}}$（公式 8，见 3.2 节），实现运动门控的注意力强制训练。

**相机相对姿态损失**：

$$
\mathcal{L}_{\mathrm{cam}} = \frac{1}{T(T-1)} \sum_{i \neq j} ( \theta_{\hat{R}_{ij}, R_{ij}} + \Vert \hat{t}_{ij} - t_{ij} \Vert ) \tag{9}
$$

其中 $\theta_{\hat{R}_{ij}, R_{ij}}$ 为预测相对旋转与真值之间的角度误差，$\Vert \hat{t}_{ij} - t_{ij} \Vert$ 为相对平移的 L1 距离。该损失对所有帧对求平均，强制全局姿态一致性。

训练时，对于原始相机 token，计算从早期帧到后期帧的相对变换损失时，早期帧 token 的梯度被截断；对于 BA-like 聚合中复制的相机 token，则保留完整梯度流，以稳定训练过程。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/005_Figure_5.jpg]]
*Figure 5: Streaming Inference pipeline. Leveraging causal attention, our model can efficiently process streaming input in an online manner. To enhance camera pose accuracy, we apply a bundleadjustment-like post-processing step after the entire sequence has been processed. Specifically, for each frame, we duplicate the camera token and perform inference again using the previously cached key-value pairs*

## 实验与关键发现

### 核心实验结果

MoRe 在多个动态场景基准上进行了零样本评估，涵盖相机姿态估计、视频深度估计和推理效率。Table 1 和 Table 2 汇总了主要结果。

**相机姿态估计**：在动态数据集 Sintel 上，MoRe 流式模型（streaming）取得 ATE 0.1474，显著优于其他流式方法（Stream3R 0.2135，CUT3R 0.2630），并超越了全注意力静态基线 VGGT（0.1715）。当使用全注意力（FA）变体时，ATE 进一步降至 0.0877，为所有对比方法中的最优结果。在 Bonn 和 TUM-dynamics 数据集上，MoRe FA 的 ATE（0.0138 / 0.0115）与顶尖全注意力方法 π³ 基本持平，而流式版本（0.0211 / 0.0260）虽略有退化，仍保持竞争力。在静态数据集 Co3Dv2 上，MoRe FA 的 AUC@30 达到 91.42，超过 VGGT 的 88.59（Table 6），表明运动感知设计并未损害静态场景下的泛化能力。

**视频深度估计**：在 Sintel 上，MoRe 流式模型的 Abs Rel 为 0.254，大幅领先 VGGT（0.387）和 Stream3R（0.329）。在 KITTI 上，MoRe 的 Abs Rel 为 0.072，与 VGGT（0.073）持平。在 Bonn 和 TUM-dynamics 上，MoRe 同样展现出稳定的深度估计能力。

**推理效率**：在 KITTI 数据集上测试，MoRe 流式模型达到 30.09 FPS，快于 Stream3Rβ（23.48 FPS）和 CUT3R（17.71 FPS），验证了分组因果注意力设计在实时流处理中的效率优势（Table 5）。

### 消融实验分析

消融实验系统验证了 MoRe 各核心组件的贡献。

**注意力强制策略**：Table 3 显示，移除注意力强制后，Sintel ATE 从 0.147 退化至 0.163，TUM-dynamics ATE 从 0.026 退化至 0.028。这证实了在训练时利用运动掩码引导相机 token 关注静态区域，是提升动态场景下姿态估计精度的关键机制。

**BA-like 全局 token 聚合**：去除该后处理步骤后，Sintel 上的 RPE_trans 从 0.082 增至 0.085，RPE_rot 从 0.616 增至 0.619（Table 3）。这一轻量全局优化有效补偿了因果注意力带来的长程信息损失，改善了平移与旋转的一致性。

**分组因果注意力**：Table 4 的深度估计消融表明，将分组因果注意力替换为标准因果注意力后，Sintel Abs Rel 从 0.254 增至 0.277，KITTI Abs Rel 从 0.072 增至 0.079。帧内全注意力对维持空间连贯性至关重要，而单纯帧间因果约束会导致深度质量下降。

**运动对齐损失函数**：Table 7 对比了提出的运动门控损失与 KL 散度损失。使用 KL 散度时，Sintel ATE 从 0.147 退化至 0.185，TUM-dynamics ATE 从 0.026 退化至 0.029。运动门控损失通过仅在静态先验足够高时鼓励注意力权重，避免了对动态区域的错误压制，在动静场景下均更稳定。

### 定性分析与注意力可视化

Figure 6 展示了全注意力模型的定性重建结果。MoRe 在真实动态场景中估计的几何结构更为精确和鲁棒，对运动物体的深度边缘保持清晰，而对比方法常出现模糊或畸变。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/006_Figure_6.jpg]]
*Figure 6: Qualititive Comparison of Our Full Attention Model with Other Methods. MoRe delivers outstanding performance in realworld scenes, outperforming other methods through its precise and robust geometry estimation*

Figure 10 的注意力图可视化直接揭示了注意力强制策略的效果。在 Dynamic Replica 和 DAVIS 数据集上，经过运动对齐训练的 MoRe 相机 token 的注意力分布明显抑制了对动态物体的关注，呈现出更干净、结构化的静态区域聚焦模式。相比之下，未使用该策略的 VGGT 模型在动态场景中常将注意力分散至运动物体，导致姿态估计精度下降（Figure 3）。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/015_Figure_10.jpg]]
*Figure 10: Attention Map Comparison. We visualize the attention map on Dynamic Replica [34] and DAVIS [28] dataset. Our motion-aligned training suppresses undesired attention from camera tokens to dynamic objects, yielding cleaner and more structured attention patterns*

### 失败模式与局限性

尽管 MoRe 在多数场景下表现优异，但分析揭示了若干固有局限：

1. **运动掩码质量依赖**：注意力强制策略严重依赖训练时运动掩码标注的准确性。噪声较大或边界不精确的掩码会误导注意力对齐，降低姿态和深度估计的可靠性。当前方法未提供对标注噪声的鲁棒性机制。

2. **极快运动与运动模糊**：在物体运动极快或存在严重运动模糊的场景中，运动掩码的提取（基于光流差异）可能失效，导致注意力对齐错误，进而引起深度不准和姿态抖动。

3. **长时依赖与复杂交互**：前馈架构受限于训练时间窗口，难以捕获超出窗口的极长时依赖。对于多物体复杂交互或非刚性变形，模型可能出现几何畸变或时序不一致。

4. **遮挡与外观剧变**：当前框架未显式建模遮挡关系和大幅外观变化，可能导致 4D 重建中出现伪影或结构断裂。

### 公平性说明

所有对比实验在相同数据集和评估协议下进行，流式方法统一采用因果注意力推理，全注意力方法使用完整序列上下文，计算资源均为 NVIDIA A800。训练数据涵盖大规模多样静态与动态场景，未见过的动态数据集用于零样本评估，保证了泛化能力的公平比较。

![[assets/figures/papers/paper_list_l57_https_arxiv_org_abs_2603_05078/figures/010_Table_4.jpg]]
*Table 4: Ablation on Video Depth Estimation*

## 定位与知识库关联

### 与基线方法的谱系关系

MoRe 的架构直接继承自以 **VGGT** 为代表的全注意力前馈重建范式，但在注意力机制、训练监督信号和全局一致性优化三个关键维度上进行了结构性改造，使其从“静态场景专用”迁移到“动态场景可流式处理”的新能力空间。

**与全注意力静态重建方法（VGGT、π³、Fast3R、FLARE、MapAnything）的关系。** 这些方法均依赖全局双向注意力在完整序列上联合推理相机姿态与场景几何，在静态场景（如 ScanNet、Co3Dv2）中精度极高，但面对动态物体时相机 token 的注意力分布会混入运动前景，导致姿态估计显著退化。MoRe 的全注意力变体（FA）在保持全局注意力架构的前提下，通过训练阶段的注意力强制策略（attention-forcing）显式引导相机 token 关注静态区域，从而在 Sintel 上 ATE 从 VGGT 的 0.1715 降至 0.0877（Table 1），在 Co3Dv2 上 AUC@30 从 88.59 提升至 91.42（Table 6），本质上是在不改变推理时计算图的前提下，通过训练信号的重新设计解决了全注意力模型对动态场景的脆弱性。

**与流式重建方法（Stream3R、CUT3R、Spann3R）的关系。** 这些方法采用标准因果注意力以支持逐帧在线处理，但帧内的单向注意力破坏了空间一致性，且缺乏对运动区域的显式建模。MoRe 的分组因果注意力（GCA）在帧内保留全注意力、帧间施加因果约束，同时配合运动掩码辅助输出和 BA-like 全局 token 聚合，在 Sintel 上 ATE 达 0.1474，Abs Rel 达 0.254，全面超越 Stream3R 等流式方法（Table 1 & Table 2），并在 KITTI 上以 30.09 FPS 的推理速度优于 Stream3Rβ 的 23.48 FPS（Table 5）。这表明 MoRe 在流式框架内实现了此前仅全注意力方法才能达到的精度水平。

### 适用边界与能力定位

**核心能力边界。** MoRe 的能力建立在三个相互耦合的机制之上：(1) 注意力强制训练利用运动掩码监督使相机 token 学会抑制对动态区域的关注；(2) 分组因果注意力在保持帧内空间连贯性的同时支持时序因果推理；(3) BA-like token 聚合以轻量后处理补偿因果注意力带来的长程信息损失。这三者的协同使得 MoRe 在动态场景的流式 4D 重建任务上形成了当前最优的精度-效率平衡点。

**适用场景。** 该方法在以下条件下表现最优：运动物体与静态背景有较清晰的语义边界；相机运动幅度适中且帧间重叠充分；运动掩码标注质量较高。在 Sintel、Bonn、TUM-dynamics 等包含明确动态物体的数据集上，MoRe 的流式变体均显著优于同类方法。

**退化条件与已知局限。** 验证分析中明确指出的退化边界包括：
- 运动掩码标注质量敏感：不准确或噪声较大的掩码会直接损害注意力对齐训练的效果，进而降低重建质量和运动推理可靠性。
- 长时依赖有限：前馈结构难以捕捉超出训练时间窗口的极长时依赖和复杂动态交互。
- 极端运动鲁棒性不足：在极快、非刚性运动或严重运动模糊的场景中，注意力对齐可能失效，导致深度不准、姿态不稳定或几何畸变。
- 遮挡与外观变化未显式建模：当前框架未处理遮挡和大幅外观变化，可能导致 4D 场景出现伪影或不一致。

### 开放问题与未来方向

基于上述局限，分析中识别的开放问题指向以下研究方向：

1. **弱监督/自监督运动解耦。** 当前方法严重依赖高质量运动掩码标注，如何通过自监督或弱监督方式学习运动与静态结构的解耦，是降低标注成本、提升实用性的关键。
2. **长时时序依赖的扩展。** 能否在前馈架构中引入更有效的长程记忆机制（如记忆增强模块或层次化时序聚合），在保持实时推理效率的前提下捕获更长时依赖？
3. **极端运动与模糊的鲁棒性。** 如何提升模型在极快运动、非刚性变形和严重运动模糊下的鲁棒性，可能需要改进注意力对齐损失的设计或引入运动先验。
4. **遮挡与外观变化的显式建模。** 显式处理遮挡和剧烈外观变化以消除重建伪影，是提升 4D 重建完整性的重要方向。
5. **部分运动场景的注意力强制稳定性。** 当仅有部分场景区域运动或存在多个运动物体时，注意力强制策略的表现是否仍然稳定，以及如何进一步优化损失设计以适应更复杂的运动模式，仍需系统验证。

> **注意：** 上述基线方法的具体作者、会议和年份信息在当前分析中未提供完整元数据，建议手动补充以增强知识库定位的准确性。例如，Stream3R、CUT3R、Spann3R 等方法的出版信息需从原始论文中核实。

## 原文 PDF

![[paperPDFs/arxiv_2026/MoRe_Motion_aware_Feed_forward_4D_Reconstruction_Transformer.pdf]]
