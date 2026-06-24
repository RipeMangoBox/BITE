---
title: "RnG: A Unified Transformer for Complete 3D Modeling from Partial Observations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RnG_A_Unified_Transformer_for_Complete_3D_Modeling_from_Partial_Observations.pdf
project_link: "https://npucvr.github.io/RnG"
code_link: null
aliases:
- RRG
- RnG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 重建引导的因果注意力掩码 M：阻止源视图Query关注目标视图Key，从而在注意力层面解耦重建与生成，使单一Transformer能同时完成两项任务。
primary_logic: 利用因果注意力设计将Transformer的KV-Cache重新解释为隐式完整三维表示：重建阶段缓存源视图特征，生成阶段通过查询缓存高效渲染新视角RGBD，实现从3D重建先验向生成任务的高效迁移。
claims:
- RnG在GSO数据集的新视角合成PSNR达26.276 dB，显著优于无位姿统一模型Matrix3D（18.736 dB），并与需要位姿的LVSM（27.522 dB）接近。
- 通过KV-Cache机制，RnG将单次新视角推理时间从213 ms降至85 ms（A800 GPU），实现实时性能且性能无损。
- 在新视角深度预测上，RnG的深度误差（Rel=0.717）比Matrix3D（Rel=9.964）低一个数量级以上，表明生成的几何高度一致。
- GSO 上 Camera Pose RA@5 (%) = 85.146
---

# RnG: A Unified Transformer for Complete 3D Modeling from Partial Observations

> [!tip] 核心洞察
> 利用因果注意力设计将Transformer的KV-Cache重新解释为隐式完整三维表示：重建阶段缓存源视图特征，生成阶段通过查询缓存高效渲染新视角RGBD，实现从3D重建先验向生成任务的高效迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | RnG：面向非完整观测的统一三维建模Transformer |
| 英文题名 | RnG: A Unified Transformer for Complete 3D Modeling from Partial Observations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.01194) · [Project](https://npucvr.github.io/RnG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | RnG (Reconstruction and Generation) |
| Dataset | GSO |

> [!tip] 效果简介
> - GSO 上，Camera Pose RA@5 (%) 85.146 vs 43.770 (Matrix3D unposed) (+41.376)；Source View Depth Rel 0.584 vs 5.960 (VGGT) (-5.376)；Novel View Depth Rel 0.717 vs 9.964 (Matrix3D unposed) (-9.247)。

## 概述

从稀疏、无位姿的二维图像观测中恢复完整的三维物体，是计算机视觉长期面临的挑战。现有的前馈三维重建基础模型——如 **VGGT**（Wang et al., CVPR 2025）和 **DUSt3R**（Wang et al., CVPR 2024）——虽然能高效恢复输入视角下可见区域的几何与外观，却无法建模被遮挡或未观测的部分，导致三维表示不完整，难以支撑需要完整物体的下游应用。另一方面，基于扩散模型的方法（如 **Matrix3D**，Lu et al., CVPR 2025）试图统一重建与生成，但推理速度慢、几何一致性弱。

**RnG**（Reconstruction and Generation）以单一前馈Transformer统一了三维重建与新视角生成两项任务。其核心设计是一条**重建引导的因果注意力掩码**：在全局注意力块中，阻止源视图的Query关注目标视图的Key/Value，从而在注意力层面解耦重建与生成。这一设计使Transformer的KV-Cache被重新解释为**隐式完整三维表示**——重建阶段缓存源视图特征，生成阶段通过查询缓存高效渲染新视角的RGBD，实现了从三维重建先验向生成任务的高效迁移。

在GSO数据集上，RnG展现出显著优势：**完整三维Chamfer距离**降至0.0067（VGGT为0.0260），**新视角合成PSNR**达26.276 dB，大幅超越同为无位姿方法的Matrix3D（18.736 dB），且与需要真实位姿的LVSM（27.522 dB）接近。更关键的是，**新视角深度误差**（Rel=0.717）比Matrix3D（Rel=9.964）低一个数量级以上，表明生成的几何高度一致。通过KV-Cache机制，单次新视角推理时间从213 ms降至85 ms（A800 GPU），效率提升约2.5倍且性能无损。RnG在方法谱系中定位为**无位姿、前馈式、统一重建与生成的Transformer模型**，其因果注意力设计填补了现有方法在效率与完整性之间的空白。

## 背景与动机

### 问题背景：从部分观测到完整三维理解

从少量无位姿的二维图像中理解三维世界是计算机视觉的核心目标之一。近年来，以 **VGGT**（Wang et al., CVPR 2025）和 **DUSt3R**（Wang et al., CVPR 2024）为代表的前馈三维重建基础模型取得了显著进展——它们能从稀疏输入视图直接回归相机位姿和逐像素点云，无需任何相机参数。然而，这些方法存在一个根本性瓶颈：**它们仅恢复输入视角下可见区域的几何与外观，对遮挡或不可见部分完全无法建模**。这意味着，即便重建质量再高，输出也只是一个不完整的三维表面片段，无法直接支持需要完整物体表示的下游应用（如虚拟物体交互、三维扫描、机器人抓取等）。

与此同时，新视角合成领域的方法——无论是依赖扩散模型的 **Matrix3D**（Lu et al., CVPR 2025），还是基于3D高斯的 **LGM**（Tang et al., ECCV 2024），抑或需要真实位姿输入的 **LVSM**——虽然能够“想象”出未见视角的内容，但它们通常将重建与生成视为两个解耦甚至独立的过程。这种割裂带来了两个问题：其一，重建和生成无法共享底层三维表示，导致计算冗余和表示不一致；其二，许多生成方法仍依赖已知位姿或迭代采样，难以实现前馈式的实时推理。

### 现有方法的缺口：统一与效率的两难

表1（Table 1）系统对比了代表性方法的能力矩阵，揭示了当前领域的一个清晰空白：

- **重建基础模型**（如VGGT、DUSt3R）具备前馈速度和无位姿重建能力，但缺乏新视角生成和完整三维建模能力。
- **新视角生成模型**（如LVSM）能生成高质量新视角，但需要真实位姿作为输入，且无法输出显式的完整几何。
- **扩散统一模型**（如Matrix3D）尝试同时处理重建与生成，但受限于扩散采样的迭代特性，推理速度慢（RnG比其快超过100倍），且深度预测误差高达一个数量级以上（GSO上新视角深度Rel=9.964 vs RnG的0.717）。

换言之，**尚不存在一种方法能够同时满足“无位姿”、“前馈实时”、“重建与生成统一”、“完整三维建模”这四个需求**。

### 本文动机：一个Transformer，两项任务，一种表示

本文的核心动机在于回答一个根本性问题：**能否用单一的前馈Transformer，从无位姿的部分观测中隐式地学习完整的三维表示，并同时支持可见区域的重建与未见视角的生成？**

这一动机的技术直觉是：如果重建和生成能够在注意力层面被有效解耦，而非在模型架构层面割裂，那么Transformer内部的键值令牌（Key/Value tokens）就可以被重新解释为一种可共享的隐式三维表示——既能服务于源视图的几何恢复，也能被目标视角查询以生成新视角的RGBD输出。这种设计有望实现从“重建先验”到“生成能力”的高效迁移，同时保持前馈推理的实时性。

图1（Figure 1）以Teaser图的形式展示了RnG的核心能力：给定4张无位姿的物体图像，VGGT仅能恢复可见区域的结构，而RnG能在单个A800 GPU上于1秒内估计完整的三维几何，并像“虚拟三维扫描仪”一样将渲染结果累积为完整的物体模型。

## 核心创新

RnG的核心创新在于通过**重建引导的因果注意力**（Reconstruction-guided Causal Attention）将三维重建与新视角生成统一于单个前馈Transformer之中，并由此衍生出两项关键突破：注意力层面的任务解耦，以及KV-Cache作为隐式完整三维表示的推理机制。

### 瓶颈与因果调控变量

现有前馈三维重建基础模型（如**VGGT**（Wang et al., CVPR 2025）、**DUSt3R**（Wang et al., CVPR 2024））仅能恢复输入视角下可见区域的几何与外观，无法建模被遮挡部分，导致三维表示不完整，无法支持需要完整物体的下游应用。扩散模型（如**Matrix3D**（Lu et al., CVPR 2025））虽可生成未见区域，但推理速度慢且几何一致性不足。

RnG的核心因果调控变量是**注意力掩码 $M$**：阻止源视图Query关注目标视图Key/Value，从而在注意力层面解耦重建与生成，使单一Transformer能同时完成两项任务。这一设计直接回应了“如何从部分观测推断完整三维”的根本瓶颈。

### 三个关键Changed Slots

**1. 注意力机制：从双向全局到重建引导因果**

基线方法（VGGT、DUSt3R）采用标准双向全局注意力，源视图与目标视图token相互可见，重建与生成过程耦合。RnG引入二值掩码：

$$M_{i,j} = \begin{cases} 0 & \text{if } i \in \{s\} \text{ and } j \in \{t\} \\ 1 & \text{elsewhere} \end{cases}$$

该掩码应用于全局注意力块中，使得注意力输出计算变为：

$$\mathrm{Out} = \mathrm{softmax}\left( \frac{M \odot QK^{\mathsf{T}}}{\sqrt{d_k}} \right) V$$

源视图token仅能关注自身，而目标视图token可关注所有token。这一非对称设计使重建过程不受生成目标干扰，同时生成过程可充分利用重建得到的几何先验。

**2. 隐式三维表示：从逐视图点云回归到KV-Cache**

基线方法通常为每个视图独立回归点云，或依赖扩散模型的隐变量。RnG将Transformer的KV-Cache重新解释为**可共享的隐式完整三维表示**：

$$K_s' = \mathrm{Cache}(K_s), \quad V_s' = \mathrm{Cache}(V_s)$$

在推理阶段，源视图的Key/Value token被缓存后，新视角生成仅需通过查询缓存完成：

$$\mathrm{Out}_t = \mathrm{softmax}\left( \frac{Q_t \cdot [K_s'; K_t]^\mathsf{T}}{\sqrt{d_k}} \right) [V_s'; V_t]$$

这一设计使三维重建先验高效迁移至生成任务，避免了为每个新视角重新处理源视图的计算开销。

**3. 推理流程：从单次耦合前传到两阶段高效推理**

基线方法重建与生成耦合于单次前向传播。RnG将推理拆分为两阶段：阶段1缓存源视图KV，阶段2查询缓存生成新视角RGBD。这一设计带来显著的效率提升——单次新视角推理时间从213 ms降至85 ms（A800 GPU），效率提升约2.5倍，且性能几乎无损（见Table 4）。

### 决定性证据

- **新视角合成性能**：RnG在GSO数据集上PSNR达26.276 dB，显著优于无位姿统一模型Matrix3D（18.736 dB），并与需要真实位姿的LVSM（27.522 dB）接近。这证明因果注意力设计有效解耦了重建与生成，使无位姿方法接近有位姿方法的性能（Table 2）。
- **几何一致性**：新视角深度预测误差（Rel=0.717）比Matrix3D（Rel=9.964）低一个数量级以上，表明生成的几何高度一致，而非简单的外观幻觉（Table 2）。
- **3D重建先验的迁移效果**：使用VGGT预训练权重（Ours-15K）显著优于从头训练（Ours-15K-scratch），验证了重建先验通过KV-Cache机制向生成任务高效迁移的核心假设（Table 3）。

### 与相关工作的本质差异

与**LGM**（Tang et al., ECCV 2024）等基于3D高斯的多视角生成方法相比，RnG不依赖显式三维表示（如高斯点云），而是通过注意力机制隐式编码完整三维信息，避免了显式表示带来的几何不一致风险。与Matrix3D等扩散模型相比，RnG的前馈特性使其推理速度提升超过100倍，同时保持可比的生成质量。

## 整体框架

RnG是一个统一的前馈Transformer，旨在从少量无位姿的二维图像中同时完成三维重建与新视角生成。其核心设计理念在于：**将Transformer的注意力缓存（KV-Cache）重新解释为一种隐式的完整三维表示**，从而在单一网络中实现从“重建先验”到“生成任务”的高效迁移。

### 输入与输出定义

RnG的输入为 $N$ 张无位姿的源视图图像 $\{I_s\}_{s=1}^{N}$，以及 $M$ 个目标视角的射线参数。输出包含三个层次：

1. **源视图重建**：每张源视图的像素对齐点云地图（point map）及相机位姿；
2. **新视角生成**：每个目标视角的RGB图像与深度图（以点云地图形式输出）；
3. **完整三维表示**：通过KV-Cache隐式编码的全局三维结构，可被反复查询以生成任意新视角。

### 网络架构总览

RnG的整体架构（Figure 2）由以下核心模块串联构成：

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/003_Figure_2.jpg]]
*Figure 2: The Network Architecture of RnG. (a) Source view images are first tokenized using the DINO vision transformer; the Plucker ¨ ray map representing the target view point goes through a linear layer. After adding camera tokens for each view, all tokens will then alternately attend to global- and frame-level attention blocks. Finally, camera tokens from input views are used to estimate camera poses, while a point head and an RGB head process ray tokens from the target view, providing geometry and appearance estimations. (b) In inference, the model can cache K/V token from source views, synthesizing novel view geometry and geometry at a higher speed*

**1. 图像令牌化（DINO ViT Encoder）**
源视图图像首先通过冻结权重的DINO Vision Transformer编码为图像级特征令牌。该编码器提供语义丰富的视觉先验，且不参与训练更新。

**2. 目标射线编码（Plücker Ray Map Projection）**
目标视角的每条射线由其Plücker坐标参数化（包含射线原点和方向），经线性层投影为与图像令牌维度一致的射线令牌。这些令牌作为生成阶段的查询（Query），携带了“从何处观察”的几何信息。

**3. 相机令牌嵌入**
为每个视图（源视图和目标视图）添加可学习的相机令牌，用于后续的位姿估计和跨视图信息聚合。

**4. 交替注意力块（Interleaved Global & Frame Attention Blocks）**
所有令牌（图像令牌、射线令牌、相机令牌）交替通过全局注意力块和帧级注意力块进行处理。全局注意力块负责跨视图的信息交互，帧级注意力块则专注于单视图内部的特征精化。这是重建引导因果注意力机制发挥作用的关键位置。

**5. 输出头（Output Heads）**
- **Camera Head**：从源视图的相机令牌回归相机位姿，其中第一个源视图的位姿被固定为标准位置 $\hat{\mathbf{g}}_{s=1} = \left[ \mathbf{I}_{3\times 3} \mid [0,0,-1]^{\mathsf{T}} \right]$，为重建提供世界坐标系参考。
- **DPT Point Head**：从目标视图的射线令牌解码像素对齐的点云地图，输出几何信息。
- **DPT RGB Head**：从目标视图的射线令牌解码新视角RGB图像，输出外观信息。

### 核心数据流

训练阶段，源视图令牌和目标射线令牌同时输入网络，通过重建引导因果注意力掩码实现重建与生成的解耦（详见下一节）。推理阶段则分为两步：

1. **阶段一：重建与缓存**——仅处理源视图，将各全局注意力块的Key/Value令牌缓存为隐式三维表示 $\mathbf{K}_s' = \text{Cache}(\mathbf{K}_s), \mathbf{V}_s' = \text{Cache}(\mathbf{V}_s)$；
2. **阶段二：生成与查询**——目标射线令牌作为Query，同时关注缓存的源视图KV和自身的Key/Value，高效生成新视角的几何与外观。

这种两阶段设计使得单次新视角推理时间从213 ms降至85 ms（A800 GPU），效率提升约2.5倍且性能无损，为实时应用提供了可能。

### 补充图表

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/001_Figure_1.jpg]]
*Figure 1: What can RnG do? Given a few unposed images of an object, 3D reconstruction foundation models like VGGT can recover the structure of observed regions, but leaves the unseen part un-modeled. RnG can estimate its complete 3D geometry within a second on an A800 GPU, using a single feed-forward transformer. RnG implicitly reconstructs 3D and render onto new viewpoints with appearance and geometry. By accumulating these rendered point maps , RnG can generate a complete 3D object, working like a virtual 3D scanner*

## 核心模块与公式推导

### 3.1 网络架构总览

RnG采用单一前馈Transformer统一处理源视图重建与目标视角生成。其核心数据流如图2所示，由以下关键模块构成：

- **DINO ViT编码器**：以冻结参数提取源视图图像的图像级特征令牌（patch tokens），作为重建阶段的输入。
- **Plücker射线图投影**：将目标视角的射线方向与原点编码为令牌，作为生成阶段的查询信号。
- **交替全局与帧级注意力块**：所有令牌（源视图图像令牌、目标视图射线令牌、相机令牌）交替进行全局注意力和帧内注意力计算，实现跨视图信息交互。
- **相机头**：从源视图对应的相机令牌回归相机位姿。
- **DPT点云头与RGB头**：从目标视图令牌分别解码像素对齐的点云地图和新视角RGB图像。

### 3.2 世界坐标系定义

为建立统一的世界坐标系参考，RnG将第一个源视图的相机位姿固定为标准位置：

$$\hat{\bf g}_{s=1} = \left[ I_{3\times 3} | [0,0,-1]^{\mathsf{T}} \right]$$

其中 $I_{3\times 3}$ 为单位旋转矩阵，$[0,0,-1]^{\mathsf{T}}$ 表示相机沿负Z轴方向，为后续所有视图的位姿估计提供锚点。

### 3.3 重建引导的因果注意力

这是RnG实现重建与生成解耦的核心机制。在全局注意力块中，引入二值掩码 $M$ 控制注意力流向：

$$M_{i,j} = \begin{cases} 0 & \text{if } i \in \{s\} \text{ and } j \in \{t\} \\ 1 & \text{elsewhere} \end{cases}$$

其中 $\{s\}$ 为源视图令牌索引集合，$\{t\}$ 为目标视图令牌索引集合。该掩码阻止源视图的Query关注目标视图的Key/Value，从而在注意力层面将重建与生成解耦。掩码后的注意力输出为：

$$\mathrm{Out} = \mathrm{softmax}\left( \frac{M \odot QK^{\mathsf{T}}}{\sqrt{d_k}} \right) V$$

此设计的因果性体现在：源视图的特征提取仅依赖自身信息（重建），而目标视图的特征生成可同时关注源视图和自身信息（生成），形成单向信息流。

### 3.4 KV-Cache作为隐式三维表示

因果注意力设计使得Transformer的KV-Cache可被重新解释为隐式完整三维表示。推理分为两阶段：

**阶段一：重建与缓存**。对源视图执行前向传播，缓存每个全局注意力块中源视图的Key和Value令牌：

$$K_s' = \mathrm{Cache}(K_s), \quad V_s' = \mathrm{Cache}(V_s)$$

这些缓存的令牌编码了从源视图提取的完整三维几何与外观先验。

**阶段二：生成与查询**。对于任意新目标视角，仅需计算目标视图的Query令牌 $Q_t$，并查询缓存的源视图令牌与目标视图自身的Key/Value：

$$\mathrm{Out}_t = \mathrm{softmax}\left( \frac{Q_t \cdot [K_s'; K_t]^{\mathsf{T}}}{\sqrt{d_k}} \right) [V_s'; V_t]$$

该机制使得单次新视角推理无需重新处理源视图，推理时间从213 ms降至85 ms（A800 GPU），效率提升约2.5倍且性能无损（Table 4）。

### 3.5 多任务训练损失

RnG联合优化三个目标：

$$\mathcal{L} = \mathcal{L}_{RGB} + \lambda_{pmap} \mathcal{L}_{pmap} + \lambda_{c} \mathcal{L}_{cam}$$

其中 $\mathcal{L}_{RGB}$ 为新视角RGB重建损失，$\mathcal{L}_{pmap}$ 为点云地图损失（通过DPT点云头从目标视图令牌解码，见公式(6)），$\mathcal{L}_{cam}$ 为相机位姿回归损失。$\lambda_{pmap}$ 和 $\lambda_{c}$ 为平衡权重。该多任务设计使网络同时学习几何一致性（点云地图与位姿）和外观生成能力。

### 补充图表

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/004_Figure_3.jpg]]
*Figure 3: The reconstruction-guided causal attention. (a) During training, we decouple reconstruction and generation at the attention level inside global attention blocks. At inference time, the attention process is split into two steps: (b) source-view key value tokens are cached as an implicit 3D representation; (c) the KVcache is queried by target view poses to generate novel views*

## 实验与分析

### 核心瓶颈与评估逻辑

现有前馈三维重建模型（如 **VGGT** (Wang et al., CVPR 2025)、**DUSt3R** (Wang et al., CVPR 2024)）的核心瓶颈在于：它们仅恢复输入视角下可见区域的几何与外观，无法建模未见部分，导致三维表示不完整。RnG 的设计目标正是突破这一限制——在无位姿输入的条件下，同时完成源视图重建与新视角生成，从而获得完整的三维物体表示。因此，实验评估需要同时覆盖重建质量（相机位姿、源视图深度、完整三维几何）和生成质量（新视角合成、新视角深度一致性）两个维度。

### 主实验：GSO 数据集定量对比

表 2 报告了在 GSO 数据集（1030 个物体）上的全面对比。RnG 在几乎全部指标上显著优于同类无位姿方法，并与需要真实位姿的强基线接近。

**相机位姿估计。** RnG 的位姿召回率 RA@5 达 85.146%，而扩散模型 **Matrix3D**（Lu et al., CVPR 2025）仅 43.770%，提升超过 41 个百分点（+41.376）。这表明重建引导的因果注意力设计有效保留了源视图间的几何一致性，无需显式位姿监督即可实现高精度位姿回归。

**源视图深度重建。** RnG 的深度相对误差（Rel=0.584）比 VGGT（Rel=5.960）低一个数量级（−5.376），且优于 Matrix3D（Rel=2.065）。这说明 RnG 在可见区域的重建精度上同样达到了领先水平。

**新视角深度一致性。** 这是检验生成几何质量的关键指标。RnG 的深度误差（Rel=0.717）比 Matrix3D（Rel=9.964）低 9.247，优势超过一个数量级。这一结果直接验证了核心设计——KV-Cache 作为隐式完整三维表示，能为新视角查询提供高度一致的几何信息，而非简单的纹理拼贴。

**新视角合成质量。** RnG 的 PSNR 达 26.276 dB，显著超过 Matrix3D（18.736 dB，+7.540），并与需要真实位姿的 **LVSM**（27.522 dB）仅差约 1.2 dB。考虑到 RnG 完全不依赖位姿输入，这一差距是可接受的，且视觉质量已接近有姿态方法（见图 4）。

**完整三维几何。** 通过累积多视角渲染的点云，RnG 的 Chamfer Distance 仅 0.0067，远低于 VGGT（0.0260，−0.0193），验证了其从部分观测推断完整物体形状的能力。

### 消融实验：设计选择的有效性

表 3 系统消融了训练策略、预训练权重和注意力设计的影响。

**3D 重建先验的关键作用。** 使用 VGGT 预训练权重初始化的 RnG（Ours-15K）在仅训练 15K 步后，新视角合成 PSNR 即达到 24.619，显著优于从头训练版本（Ours-15K-scratch）。这证明从大规模 3D 重建任务中习得的几何先验，可通过 KV-Cache 机制高效迁移至生成任务，是 RnG 数据效率的关键来源。

**训练效率优势。** 在同等 40K 迭代下，RnG 的 PSNR（26.276）超过 LVSM（24.619）。更值得注意的是，RnG 仅使用 LVIS 子集训练 15K 步（Ours-15K）即已超过 LVSM 训练 40K 步的性能。这表明前馈 Transformer 架构相比需要多步采样的扩散模型（如 Matrix3D），在收敛速度和最终性能上均具优势。

**位姿监督的冗余性。** 移除相机位姿监督（w/o cam）后，新视角合成性能几乎不变（PSNR 仅降 0.09 dB），验证了重建引导的因果注意力已能隐式利用几何信息，无需额外的显式位姿损失来驱动生成质量。

### KV-Cache 推理效率

表 4 量化了 KV-Cache 机制的实际收益。在 A800 GPU 上，无缓存时单次新视角推理需 213 ms，启用缓存后降至 85 ms，效率提升约 2.5 倍，且性能几乎无损。这一结果使得 RnG 能够实现实时级的新视角渲染，为其在交互式应用中的部署提供了可行性。

### 泛化能力

RnG 虽仅在 4 视图输入下训练，但在 2 至 8 视图的测试中均展现强泛化能力（表 5）。在真实场景 CO3D 数据集的零样本实验中，RnG 优于 LVSM，与在 CO3D 上训练的 Matrix3D 可比。但需注意，世界原点模糊问题可能影响定量评估的准确性，该点需要手动验证。

### 失败模式与局限

1. **复杂纹理保真度不足**：在精细纹理区域，RnG 的渲染结果可能缺乏锐利细节，这源于 DINO ViT 编码器的特征粒度限制和 MSE 损失的平滑效应。
2. **世界原点歧义**：物体重建时世界坐标系原点定义存在固有歧义，可能导致位姿估计偏差，尤其在对称物体上更为明显。
3. **多视角累积噪声**：从多视角累积完整三维模型时，各视角的局部误差可能累积并产生融合冲突，影响最终几何质量。
4. **动态场景未验证**：当前训练数据均为静态刚性物体，对非刚性或动态内容的支持尚未探索。

### 关键图表索引

- **Table 2**：GSO 数据集主实验定量对比，涵盖重建与生成的全部指标。
- **Table 3**：消融实验，揭示预训练权重、训练效率和注意力设计的影响。
- **Table 4**：KV-Cache 对推理效率的消融，展示 2.5 倍加速。
- **Figure 4**：新视角合成视觉对比，RnG 无位姿条件下与有姿态方法 LVSM 的视觉质量可比。
- **Figure 5**：相机位姿与点云可视化，验证位姿估计精度和几何一致性。
- **Figure 6**：从 4 视图累加的完整 3D 结构，与 VGGT 仅重建可见区域形成对比。

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison. We evaluate the reconstruction and generation ability of all models on the GSO dataset. ‘—’ means that the model is not capable of delivering that result*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/010_Table_3.jpg]]
*Table 3: Ablation studies. We studies the training efficiency of RnG by comparing with LVSM and effectiveness of the model architecture*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/011_Table_4.jpg]]
*Table 4: Efficiency comparison of models with and without KV-Cache for inferring a single novel-view appearance and geometry*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/006_Figure_4.jpg]]
*Figure 4: Visual comparison of novel view synthesis. Though RnG does not require accurate pose as input, it provides comparable visual quality with state-of-the-art pose-dependent methods like LVSM. Our model can hallucinate unseen regions with high 3D consistency*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/007_Figure_5.jpg]]
*Figure 5: Camera pose and point cloud visualization. Reconstructions are normalized to match GT’s scale and are aligned to first frame’s position (dark blue). The estimated camera pose from RnG highly aligns with the ground truth. Our back-projected point cloud from source views does not suffer from layering artifacts, presenting accurate object structures*

### 补充图表

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/002_Table_1.jpg]]
*Table 1: Comparison between representative 3D reconstruction and novel view synthesis methods*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/014_Table_5.jpg]]
*Table 5: Generalize to other number of input views. Although our model is not trained to handle other number of input views, it still shows strong generalization ability to other number of source images*

![[assets/figures/papers/paper_list_l2585_https_arxiv_org_abs_2603_01194/figures/016_Figure_10.jpg]]
*Figure 10: Qualitative results on CO3D*

## 方法谱系与知识库定位

### 1. 任务定位：无位姿统一重建与生成

RnG试图填补三维视觉中一个关键的能力断层：**从无位姿的稀疏观测直接推断完整三维结构并渲染新视角**。现有方法在此问题上呈现明显的功能割裂：

- **纯重建模型**（如 **VGGT** (Wang et al., CVPR 2025)、**DUSt3R** (Wang et al., CVPR 2024)）可从无位姿图像恢复可见区域的几何与相机位姿，但无法建模被遮挡或不可见部分，输出的三维表示天然不完整。
- **新视角生成模型**（如 **LVSM**）能合成高质量新视角，但依赖真实相机位姿作为输入，且不显式输出完整三维几何。
- **扩散模型统一方法**（如 **Matrix3D** (Lu et al., CVPR 2025)）尝试在无位姿条件下同时完成重建与生成，但依赖迭代去噪过程，推理速度慢，且生成质量与几何一致性有限。

RnG的核心定位在于：**以单一前馈Transformer统一这两项任务，无需真实位姿，输出隐式完整三维表示，并支持实时新视角渲染**。Table 1（见原文）系统对比了代表性方法在“无位姿输入”“完整三维重建”“新视角合成”“前馈推理”四个维度上的能力，RnG是唯一在所有维度上同时具备能力的方法。

### 2. 核心技术分水岭：重建引导的因果注意力

RnG与上述方法最本质的架构差异在于**注意力机制的设计**。这一差异直接塑造了模型的能力边界：

- **VGGT/DUSt3R** 等重建模型使用标准的双向全局注意力，所有token相互可见。这天然将模型限制于“所见即所得”的重建范式——源视图token只能编码已观测到的信息，无法为未见区域生成几何与外观。
- **Matrix3D** 等扩散方法将重建与生成统一在隐空间扩散过程中，但两者在去噪步骤中耦合，缺乏显式的解耦机制。
- **RnG** 引入**重建引导的因果注意力掩码 $M$**（式2）：源视图Query被禁止关注目标视图Key，而目标视图Query可关注所有token。这一设计在注意力层面将“重建”（从源视图提取几何先验）与“生成”（基于先验推断新视角）解耦，使单一网络能同时完成两项任务而不相互干扰。

该设计的深层意义在于：它将Transformer的KV-Cache重新解释为**可共享的隐式完整三维表示**。重建阶段缓存的源视图Key/Value token（式4）编码了场景的几何与外观先验，生成阶段通过查询缓存高效渲染新视角（式5），实现了从3D重建先验向生成任务的高效迁移。

### 3. 与代表性方法的定量关系

在GSO数据集上的主实验（Table 2）清晰刻画了RnG的能力边界：

**新视角合成**：RnG作为无位姿方法，PSNR达26.276 dB，显著优于同为无位姿的Matrix3D（18.736 dB，差距+7.540 dB），且与需要真实位姿的LVSM（27.522 dB）接近。在新视角深度预测上，RnG的深度相对误差（Rel=0.717）比Matrix3D（Rel=9.964）低一个数量级以上，表明生成的几何高度一致，而非仅视觉上合理。

**相机位姿估计**：RnG的位姿召回率RA@5达85.146%，远超Matrix3D的43.770%，验证了重建引导设计有效利用了隐式几何信息。消融实验（Table 3）进一步表明，移除相机位姿监督（w/o cam）并未损害新视角合成性能，说明位姿估计与生成任务可在统一框架内协同。

**完整三维几何**：RnG的Chamfer Distance（0.0067）显著优于VGGT（0.0260），验证了其“虚拟三维扫描仪”能力——通过从多视角累积渲染的点云地图，可重建完整物体几何。

### 4. 适用边界与局限

尽管RnG在统一重建与生成上取得了突破性进展，其当前设计存在明确的适用边界：

**纹理保真度**：在复杂纹理区域，RnG的重建保真度有限，细节可能不够锐利。这与模型依赖DINO ViT的冻结特征提取有关——DINO特征虽富含语义信息，但高频纹理细节可能丢失。

**世界原点歧义**：RnG将第一个源视图的相机位姿固定为标准位置（式1），为重建提供世界坐标系参考。但这一设计在物体重建时可能引入世界原点定义的歧义，导致位姿估计偏差，尤其在物体对称性或旋转歧义场景下。

**多视角融合噪声**：从多视角累积完整三维模型时，不同视角的点云预测可能存在局部不一致，引入噪声和融合冲突。论文未详细讨论融合策略及其对最终几何质量的影响。

**动态与非刚性内容**：当前训练数据（Objaverse子集，约113.5K静态刚性物体）决定了RnG的适用范围限于静态刚性物体，对动态或可变形内容的支持尚未验证。

**极稀疏输入**：RnG在训练时使用固定数量的输入视图（4张），虽展示了对不同数量输入视图的泛化能力（Table 5），但当输入视图极少（如仅1张）时，推断被遮挡区域的几何与外观的可靠性仍需进一步验证。

### 5. 开放问题与后续方向

RnG的架构设计打开了若干值得探索的方向：

1. **动态场景扩展**：如何将重建引导的因果注意力机制扩展到动态或可变形场景？这可能需要引入时序建模或形变场预测模块。

2. **纹理质量提升**：是否可通过结合生成式图像的预训练先验（如扩散模型）来进一步提升纹理合成质量？这需要在保持几何一致性的前提下引入更强的外观先验。

3. **鲁棒的世界原点确定**：在真实世界应用中，如何自动且鲁棒地确定重建物体的上方向和世界原点？这是从物体级重建走向场景级理解的关键一步。

4. **极稀疏输入的可靠推断**：当输入视图极少（如仅1张）时，如何更可靠地推断被遮挡区域的几何与外观？这可能需要更强的语义先验或类别级形状先验。

5. **多模态扩展**：RnG的隐式三维表示（KV-Cache）是否能作为多模态下游任务（如机器人抓取、场景编辑）的通用接口？这需要验证该表示的可迁移性和可解释性。

## 原文 PDF

![[paperPDFs/CVPR_2026/RnG_A_Unified_Transformer_for_Complete_3D_Modeling_from_Partial_Observations.pdf]]