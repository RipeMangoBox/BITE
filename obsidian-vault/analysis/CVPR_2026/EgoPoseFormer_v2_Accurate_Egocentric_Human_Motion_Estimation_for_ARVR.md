---
title: "EgoPoseFormer v2: Accurate Egocentric Human Motion Estimation for AR/VR"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/EgoPoseFormer_v2_Accurate_Egocentric_Human_Motion_Estimation_for_AR_VR.pdf
code_link: null
aliases:
- EVE
- EVAEHMEAV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入单一整体查询（single holistic query）并结合投影2D关键点作为条件交叉注意力的空间引导，配合因果时间注意力实现时间一致性；并通过不确定性指导的半监督自动标注系统利用大量无标注数据提升泛化性。
primary_logic: 通过将多视角几何关系编码为可微的双阶段transformer结构，并利用单一查询解耦计算量与姿态表示，EPFv2实现了高效、准确且时间一致的自我中心运动估计；同时半监督学习可扩展利用大量无标注数据。
claims:
- EPFv2在EgoBody3M上实现MPJPE 4.02cm，比EgoBody3M和EgoPoseFormer分别提高22.4%和15.4%
- EPFv2将MPJVE相对于EgoBody3M和EgoPoseFormer分别降低了22.2%和51.7%
- 单一整体查询设计使得计算效率比16查询标准注意力版本降低4倍FLOPs
- 自动标注系统将手腕MPJPE进一步降低13.1%
---

# EgoPoseFormer v2: Accurate Egocentric Human Motion Estimation for AR/VR

> [!tip] 核心洞察
> 通过将多视角几何关系编码为可微的双阶段transformer结构，并利用单一查询解耦计算量与姿态表示，EPFv2实现了高效、准确且时间一致的自我中心运动估计；同时半监督学习可扩展利用大量无标注数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoPoseFormer v2：面向AR/VR的精确自我中心人体运动估计 |
| 英文题名 | EgoPoseFormer v2: Accurate Egocentric Human Motion Estimation for AR/VR |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.04090) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EgoPoseFormer v2 (EPFv2) |
| Dataset | EgoBody3M |

> [!tip] 效果简介
> - EgoBody3M 上，MPJPE (cm) 4.02 vs 5.18 (EgoBody3M) (-1.16 (↓22.4%))；MPJVE 0.42 vs 0.54 (EgoBody3M) (-0.12 (↓22.2%))；Wrist MPJPE (cm) 4.99 vs 6.14 (EgoBody3M) (-1.15 (↓18.7%))。

## 概述

自我中心（egocentric）人体运动估计是增强现实（AR）与虚拟现实（VR）设备实现自然交互的核心技术，典型应用包括 **Apple Vision Pro** 、**Meta Quest 3** 以及 **Momentum** 等平台。该任务要求从头戴式设备的多视角图像流中实时、精确地恢复全身 3D 姿态，但面临三个根本性瓶颈：

1. **时空推理缺失**——现有方法（如 **UnrealEgo**（Tome et al., ECCV 2022）的单帧热图回归、**EgoBody3M**（Zhao et al., ECCV 2024）的 LSTM 融合）缺乏端到端的时空联合建模能力，导致时间一致性差；
2. **计算效率低下**——**EgoPoseFormer**（EPFv1, Yang et al., ECCV 2024）采用逐关节查询令牌，计算量随关键点数量线性增长，难以部署于实时设备；
3. **标注数据稀缺**——高精度 3D 姿态标注成本极高，模型泛化性受限。

针对上述瓶颈，**EgoPoseFormer v2（EPFv2）** 提出三项核心改进：

- **单一整体查询（single holistic query）**：用一个查询令牌表示全身状态，将计算量与关键点数量解耦，相比 16 查询标准注意力方案 FLOPs 降低 4 倍以上（622K vs. 131K）；
- **条件多视角交叉注意力 + 因果时间注意力**：以投影 2D 关键点作为空间引导条件，结合带 KV-cache 的因果自注意力实现时间一致性，形成端到端可微的双阶段 Transformer 结构；
- **不确定性引导的半监督自动标注系统（ALS）**：采用教师-学生框架与不确定性蒸馏，利用大规模无标注数据（EGO-ITW-70M）提升泛化能力。

在 **EgoBody3M** 基准上，EPFv2 实现 **MPJPE 4.02 cm**，较 EgoBody3M 和 EgoPoseFormer 分别降低 22.4% 和 15.4%；**MPJVE 0.42**，分别降低 22.2% 和 51.7%；手腕 MPJPE 4.99 cm，降低 18.7%。自动标注系统进一步将手腕误差降低 13.1%。全模型 GPU 推理延迟仅 0.8 ms，满足实时 VR 设备需求。

方法的局限性在于半监督流程依赖私有无标注数据集，完全可复现性受限；在更多样化设备上的泛化能力尚需进一步验证。

## 背景与动机

### 自我中心人体运动估计的兴起

增强现实（AR）与虚拟现实（VR）设备——如 **Apple Vision Pro** 、**Meta Quest 3** 以及 **Momentum** 等——正在快速普及，驱动了对精确、实时、以自我为中心（egocentric）人体运动估计技术的迫切需求。这类技术旨在仅凭头戴设备（HMD）搭载的多视角相机和惯性测量单元（IMU）信号，实时重建穿戴者的全身3D姿态。其应用场景涵盖虚拟化身驱动、远程临场交互、运动分析以及沉浸式游戏体验。

与传统的“外部观察”（outside-in）动作捕捉不同，自我中心姿态估计面临独特的挑战：相机视角始终随头部运动而变化，且只能观测到身体的部分区域（如下肢常被遮挡）。这要求模型必须融合多视角的局部视觉线索，并利用时序上下文来推断不可见关节的位置。

### 现有方法的缺口

当前自我中心姿态估计方法主要存在三个结构性瓶颈：

**1. 空间建模效率低下，计算量随关节数线性增长。** 早期方法如 **UnrealEgo**（Tome et al., ECCV 2022）采用单帧热图回归，缺乏多视角融合能力。**EgoPoseFormer v1**（Yang et al., ECCV 2024）引入了基于可变形注意力的Transformer架构，为每个关键点分配独立的Joint Query Token（JQT），使得计算量与关键点数量呈线性关系。这种逐关节查询设计不仅增加了计算开销，还引入了较高的开发复杂度（deformable attention的实现和优化难度显著高于标准注意力），不利于在资源受限的移动设备上部署。

**2. 缺乏端到端的时空推理能力。** **EgoBody3M**（Zhao et al., ECCV 2024）采用LSTM融合多视角特征来实现时间一致性，但其时序建模能力有限。EgoPoseFormer v1则完全缺乏时间建模，逐帧独立预测导致输出存在明显的帧间抖动。此外，EgoPoseFormer v1的两阶段架构（Pose Proposal → Pose Refinement）之间没有梯度流动，限制了端到端优化的潜力。

**3. 标注数据稀缺制约泛化性。** 高精度的自我中心3D姿态标注需要昂贵的外部动捕设备，导致有标注数据集规模有限。现有方法仅能利用这些有限的有标注数据进行训练，模型在真实场景中的泛化能力受到严重制约。

### 本文动机

针对上述瓶颈，EgoPoseFormer v2（EPFv2）提出了三个核心设计动机：

- **计算与表示解耦**：用单一整体查询（single holistic query）替代逐关节查询，使注意力计算量与关键点数量解耦，从根本上降低计算复杂度。
- **端到端时空融合**：构建全可微的两阶段Transformer解码器架构，引入因果时间注意力（causal temporal attention）实现帧间一致性，并通过条件多视角交叉注意力（conditioned multi-view cross-attention）高效聚合空间信息。
- **数据效率突破**：设计基于不确定性蒸馏的半监督自动标注系统（Auto-Labeling System），利用大规模无标注数据提升模型泛化能力，突破标注数据的瓶颈。

这些设计使EPFv2在EgoBody3M基准上实现了MPJPE 4.02cm（较EgoBody3M和EgoPoseFormer分别降低22.4%和15.4%），同时将时间一致性指标MPJVE分别降低22.2%和51.7%，且模型推理延迟仅0.8ms，适合实时VR/AR部署。

## 核心创新

EgoPoseFormer v2 (EPFv2) 围绕三个相互关联的设计瓶颈对前代方法进行了系统性重构：**表征解耦、时空融合与数据效率**。其核心创新可归纳为以下五个 changed slots，每个 slot 的改动均直接服务于“高效、准确、时间一致且可扩展”的整体目标。

### 从逐关节查询到单一整体查询

EPFv1 为每个关键点独立维护一个 Joint Query Token (JQT)，计算量随关键点数量线性增长，且各查询之间缺乏显式的全身协调机制。EPFv2 将这一范式彻底替换为**单一整体查询 (single holistic query)**：

$$
\mathbf{q}_t = \mathrm{MLP}_{\mathrm{query}}(\mathbf{H}_t)
$$

该查询从头显 6DoF 姿态等辅助元数据通过 MLP 初始化，作为整个身体状态的统一信息聚合器。所有后续任务预测——3D 关键点、姿态参数、逐关节不确定性——均从这同一个查询令牌计算得出。这一设计使计算量与关键点数量**解耦**：在 16 个关键点的标准设置下，单查询方案的 FLOPs 仅为 16 查询标准注意力方案的约 1/4（131K vs. 622K），且参数量的增长几乎为零（Table 3）。更重要的是，单一查询迫使模型学习全身关节间的隐式协调关系，而非独立处理每个关节。

### 从可变形注意力到条件多视角交叉注意力

EPFv1 的空间融合依赖**可变形立体注意力 (Deformable Stereo Attention)**：每个关节查询以投影 2D 关键点为锚点，通过学习的偏移量在多视图特征图上采样，再将各视图输出串行融合。该模块开发复杂度高，且硬件利用率不理想（Figure 7）。

EPFv2 将其替换为基于**标准注意力的条件多视角交叉注意力**（Figure 8）：

$$
\mathbf{q}_t^{\prime} = \mathrm{Linear}\Big(\mathrm{Concat}_{\{v\}}\big(\mathrm{M}\hat{\mathrm{HA}}(\mathbf{q}_{\mathrm{t}} + \sigma_{\mathrm{t}}^{\mathrm{v}}, \mathbf{F}_{\mathrm{t}}^{\mathrm{v}} + \boldsymbol{\Psi}, \mathbf{F}_{\mathrm{t}}^{\mathrm{v}})\big)\Big)
$$

其中条件嵌入 $\sigma_t^v$ 在姿态细化阶段显式编码了姿态提案的投影 2D 关键点位置：

$$
\sigma_t^v = \begin{cases} \xi^v & \text{Pose proposal} \\ \xi^v + \mathrm{MLP}(\mathrm{Concat}_{\{j\}}(\mathbf{o}_{t,j}^v)) & \text{Pose refinement} \end{cases}
$$

这一设计将多视图几何关系**编码为可微的条件信号**注入注意力机制，而非依赖手工设计的采样策略。消融实验证实，移除投影 2D 关键点条件会导致性能大幅下降（Table 2 ③），验证了该空间引导的关键作用。

### 从无时间建模到因果时间注意力

EPFv1 逐帧独立处理，完全缺乏时间建模；EgoBody3M 则采用 LSTM 进行时序融合。EPFv2 引入了**因果时间注意力 (causal temporal attention)**，使当前帧的整体查询能够关注其历史窗口内的查询状态：

$$
\mathbf{q}_t^{\prime} = \mathrm{MHA}\Bigl(\mathrm{RoPE}(\mathbf{q}_t), \mathrm{RoPE}(\{\mathbf{q}_k\}_{k=t-w}^{t}), \{\mathbf{q}_k\}_{k=t-w}^{t-1}\Bigr)
$$

该模块使用**旋转位置编码 (RoPE)** 注入时序位置信息，并配合 **KV-cache** 实现高效推理——在推理时仅需计算当前帧的 query，历史帧的 key-value 对可直接复用。这解释了 EPFv2 在时间一致性指标上的显著优势：MPJVE 相较 EgoBody3M 降低 22.2%，相较 EPFv1 降低 51.7%。

### 从两阶段分离到端到端可微

EPFv1 的姿态提案与姿态细化之间**梯度流被阻断**，两个阶段实质上独立训练。EPFv2 将两个 Transformer 解码器堆叠为**架构相同、梯度全流通**的端到端管道，使得细化阶段的损失可以直接监督提案阶段的学习。这一全微分设计不仅简化了训练流程，还使模型能够以由粗到精的方式协同优化两个阶段，从而提升整体精度。

### 从纯监督到不确定性引导的半监督自动标注

针对自我中心姿态估计标注数据稀缺的根本瓶颈，EPFv2 构建了基于**不确定性蒸馏的教师-学生自动标注系统 (ALS)**。教师模型在有标注数据上预训练后，为大规模无标注数据生成伪标签；学生模型则在有标注与伪标注数据的混合批次上训练，总损失为：

$$
\mathcal{L}_{\mathrm{semi}} = \mathcal{L}_l (x_l, y_l) + \lambda_1 \cdot \mathcal{L}_u (\hat{x}_u, \hat{y}_u) + \lambda_2 \cdot \mathcal{L}_{\mathrm{uncertainty}}
$$

其中不确定性蒸馏损失 $\mathcal{L}_{\mathrm{uncertainty}} = || s_T - s_S ||$ 强制学生模仿教师对每个关节的预测不确定性分布，实现更有效的知识迁移。该系统的关键洞察在于：教师模型不仅提供伪标签，还传递了其对伪标签质量的**置信度估计**，使学生能够自适应地关注可靠样本。在 EGO-ITW-70M 无标注数据集上的实验表明，ALS 将手腕 MPJPE 进一步降低 11.7%，且轻量模型（MobileNetv4-S）从中获益比例更大（Figure 6），验证了该方案对部署友好型模型的适配性。

## 整体框架

EPFv2 构建了一个端到端可微的双阶段 Transformer 解码器架构，用于从多视角自我中心图像序列中估计精确的三维人体姿态。整个 pipeline 围绕一个核心设计理念展开：**用单一整体查询（single holistic query）替代传统的逐关节查询**，从而将计算量与关键点数量解耦，同时保持丰富的姿态表示能力。

### 输入流定义

在时间戳 $t$，系统的同步输入流定义为：

$$\mathcal{T}_t = \{ \{ \mathbf{I}_t^v \}_{v=1}^V, \mathbf{\check{H}}_t \}$$

其中 $\mathbf{I}_t^v$ 表示第 $v$ 个标定相机的图像，$\mathbf{\check{H}}_t$ 为头显的 6DoF 姿态。这一多模态输入同时提供了视觉观测和本体感知信息，为后续的空间-时间推理奠定基础。

### 模块架构与数据流

如 Figure 2 所示，EPFv2 由以下核心模块串联构成：

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/002_Figure_2.jpg]]
*Figure 2: Architecture overview (left). We stack two transformer decoders for coarse-to-fine pose estimation. A single holistic query, initialized from auxiliary metadata, attends to multi-view features and historic information to estimate 3D keypoints, pose parameters, and per-joint uncertainty in an end-to-end differentiable architecture. Illustration of the two core attention modules (right). Causal temporal C Ca Fattention enables each frame to attend to its temporal history. Conditioned multi-view cross attention incorporates both view identity and ndiCr sal ed-optional 2D keypoint projections of pose proposal to guide spatial feature aggregation across views*

**Image Encoder（图像编码器）**：首先使用共享的视觉骨干网络（如 ResNet-18 或 ViT）从 $V$ 个视角的图像中提取多视图特征 $\mathbf{F}_t^v$。这些特征作为后续 Transformer 解码器的空间信息源。

**Holistic Query Initialization（整体查询初始化）**：与 EPFv1 为每个关键点生成独立查询令牌不同，EPFv2 通过一个轻量 MLP 将辅助元数据（头显姿态 $\mathbf{H}_t$）编码为单一整体查询令牌：

$$\mathbf{q}_t = \mathrm{MLP}_{\mathrm{query}}(\mathbf{H}_t)$$

这一设计使得查询的维度与关键点数量无关，从根本上解决了逐关节查询带来的计算量线性增长问题。

**Pose Proposal Decoder（姿态提案解码器）**：第一个 Transformer 解码器接收整体查询 $\mathbf{q}_t$ 和多视图特征，通过条件多视角交叉注意力（Conditioned Multi-View Cross-Attention）从各视角特征中聚合空间信息，生成粗略的三维关键点提案。该阶段的交叉注意力使用视角身份嵌入 $\xi^v$ 作为查询条件：

$$\sigma_t^v = \xi^v \quad \text{(Pose proposal)}$$

**Pose Refinement Decoder（姿态细化解码器）**：第二个解码器在结构上与第一个相同，但引入了额外的空间引导信息——它将提案阶段的粗略 3D 关键点投影到各视角图像平面，将投影 2D 关键点 $\mathbf{o}_{t,j}^v$ 编码后附加到查询条件中：

$$\sigma_t^v = \xi^v + \mathrm{MLP}(\mathrm{Concat}_{\{j\}}(\mathbf{o}_{t,j}^v)) \quad \text{(Pose refinement)}$$

这种投影条件机制使得细化阶段能够精确地对齐多视图几何关系，显著提升关键点定位精度（消融实验表明，移除该条件会导致性能大幅下降）。

**Causal Temporal Attention（因果时间注意力）**：在两个解码器之后，EPFv2 引入因果时间注意力模块，使当前帧的查询令牌能够关注其历史窗口内的查询序列。该模块使用旋转位置编码（RoPE）和 KV-Cache 机制实现高效推理：

$$\mathbf{q}_t^{\prime} = \mathrm{MHA}\Bigl(\mathrm{RoPE}(\mathbf{q}_t), \mathrm{RoPE}(\{\mathbf{q}_k\}_{k=t-w}^{t}), \{\mathbf{q}_k\}_{k=t-w}^{t-1}\Bigr)$$

这一设计保证了时间一致性，使得 EPFv2 在 MPJVE 指标上相比 EgoBody3M 和 EgoPoseFormer 分别降低了 22.2% 和 51.7%。

**Task Heads（任务头）**：每个解码器阶段后，更新后的查询令牌被送入并行的 MLP 头，分别预测 3D 关键点位置（或姿态参数）以及每关节的不确定性（通过 Cholesky 分解的协方差矩阵表示）。细化阶段的输出通过预测相对于提案关键点的偏移量来计算最终的三维姿态。

### 端到端可微性

EPFv2 的关键改进之一是实现了**完整的端到端梯度流动**。与 EPFv1 中提案阶段和细化阶段之间无梯度传递不同，EPFv2 的两个解码器阶段共享相同的架构，允许梯度从细化阶段反向传播至提案阶段。这一设计使得整个模型能够联合优化，显著提升了训练效率和最终精度。

### 半监督扩展：自动标注系统

为充分利用大规模无标注数据，EPFv2 集成了一个基于不确定性蒸馏的自动标注系统（Auto-Labeling System, ALS），如 Figure 4 所示。该系统采用教师-学生框架：首先在有标注数据上预训练一个强教师模型，然后用教师模型为无标注数据生成伪标签，并通过不确定性蒸馏损失将教师的知识传递给学生模型。这一半监督管道使得 EPFv2 能够从私有的 EGO-ITW-70M 数据集中获益，将手腕 MPJPE 进一步降低 13.1%。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the mixture training in auto-labeling system. We adopt a stronger teacher model for pesudo labeling and apply an uncertainty distillation loss to facilitate the knowledge transfer. The teacher model is pre-trained with the labeled dataset*

## 核心模块与公式推导

### 3.1 整体架构与查询设计

EPFv2 的核心架构由两个结构相同的 Transformer 解码器堆叠而成，形成粗到细（coarse-to-fine）的姿态估计流程。与 EPFv1 为每个关键点分配独立 Joint Query Token (JQT) 的设计不同，EPFv2 采用**单一整体查询**（single holistic query token）作为信息聚合器，所有任务预测均从该查询计算得出。这一设计将计算量与关键点数量解耦，使得标准注意力下的 FLOPs 相比 16 查询版本降低超过 4 倍（131K vs. 622K）。

整体查询从头显姿态等辅助元数据初始化：

$$\mathbf{q}_t = \mathrm{MLP}_{\mathrm{query}}(\mathbf{H}_t)$$

其中 $\mathbf{H}_t$ 为时间戳 $t$ 的头显 6DoF 姿态信息，$\mathbf{q}_t$ 为生成的初始整体查询令牌。

### 3.2 条件多视角交叉注意力

EPFv2 使用标准“查询到图像”交叉注意力替代 EPFv1 的可变形注意力，通过**条件嵌入**（conditional embedding）融合视角身份和可选的投影 2D 关键点信息：

$$\mathbf{q}_t^{\prime} = \mathrm{Linear}\Big(\mathrm{Concat}_{\{v\}}\big(\mathrm{\hat{M}HA}(\mathbf{q}_t + \sigma_t^v, \mathbf{F}_t^v + \mathbf{\Psi}, \mathbf{F}_t^v)\big)\Big)$$

其中 $\mathbf{F}_t^v$ 为视角 $v$ 的图像特征，$\mathbf{\Psi}$ 为视角身份编码，$\sigma_t^v$ 为条件嵌入，其形式根据解码器阶段不同而变化：

$$\sigma_t^v = \begin{cases} \xi^v & \text{Pose proposal} \\ \xi^v + \mathrm{MLP}(\mathrm{Concat}_{\{j\}}(\mathbf{o}_{t,j}^v)) & \text{Pose refinement} \end{cases}$$

在姿态提案阶段，$\sigma_t^v$ 仅包含视角身份嵌入 $\xi^v$；在姿态细化阶段，额外附加投影 2D 关键点 $\mathbf{o}_{t,j}^v$ 的编码作为空间引导条件。

### 3.3 因果时间注意力

为实现时间一致性，EPFv2 引入带旋转位置编码（RoPE）和 KV-cache 的因果时间注意力，使当前帧查询仅关注历史帧：

$$\mathbf{q}_t^{\prime} = \mathrm{MHA}\Bigl(\mathrm{RoPE}(\mathbf{q}_t), \mathrm{RoPE}(\{\mathbf{q}_k\}_{k=t-w}^{t}), \{\mathbf{q}_k\}_{k=t-w}^{t-1}\Bigr)$$

其中 $w$ 为时间窗口长度（默认 16 帧），因果掩码确保 $\mathbf{q}_t$ 仅与 $k \leq t-1$ 的历史查询交互。

### 3.4 任务头与不确定性预测

每个解码器阶段后，查询令牌经并行 MLP 头预测 3D 关键点或姿态参数。EPFv2 支持预测每关键点的不确定性，采用多元 Student-t 分布的负对数似然损失：

$$\mathcal{L}_{\mathrm{tNLL}} = \frac{(\nu + d)}{2} \log(1 + \frac{\mathbf{m}}{\nu}) + \frac{1}{2} \log |\Sigma|$$

其中 $\mathbf{m} = \delta^{\mathrm{T}} \Sigma^{-1} \delta$ 为马氏距离（$\delta_j = \hat{\mathbf{p}}_j - \mathbf{p}_j$），$\Sigma$ 为通过 Cholesky 分解预测的协方差矩阵，$\nu$ 为自由度参数，$d=3$ 为空间维度。

### 3.5 训练目标

总体训练损失结合 MSE、不确定性损失和 Jerk 平滑损失，并通过余弦调度的动态权重 $w_d$ 平衡 MSE 与 tNLL：

$$\mathcal{L} = \lambda_{\mathrm{pos}} w_d \mathcal{L}_{\mathrm{mse}}(\mathbf{P}_r, \hat{\mathbf{P}}) + \lambda_{\mathrm{pos}} (1 - w_d) \mathcal{L}_{\mathrm{tNLL}}(\mathbf{P}_r, \hat{\mathbf{P}}, \mathbf{\Sigma}) + \lambda_{\mathrm{pos}} \mathcal{L}_{\mathrm{mse}}(\mathbf{P}_p, \hat{\mathbf{P}}) + \lambda_{\mathrm{jerk}} \mathcal{L}_{\mathrm{jerk}}(\mathbf{P}_r) + \lambda_{\mathrm{jerk}} \mathcal{L}_{\mathrm{jerk}}(\mathbf{P}_p)$$

其中 $\mathbf{P}_p$ 和 $\mathbf{P}_r$ 分别为提案和细化阶段的预测，$\hat{\mathbf{P}}$ 为真值。

### 3.6 自动标注系统（ALS）

半监督管道采用教师-学生框架，教师模型在有标注数据上预训练后生成伪标签。学生训练目标为：

$$\mathcal{L}_{\mathrm{semi}} = \mathcal{L}_l (x_l, y_l) + \lambda_1 \cdot \mathcal{L}_u (\hat{x}_u, \hat{y}_u) + \lambda_2 \cdot \mathcal{L}_{\mathrm{uncertainty}}$$

其中不确定性蒸馏损失为教师与学生预测的不确定性向量之间的 MSE：

$$\mathcal{L}_{\mathrm{uncertainty}} = || s_T - s_S ||$$

该机制使教师模型的知识（包括对预测可靠性的估计）传递给学生模型。

### 补充图表

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/010_Figure_8.jpg]]
*Figure 8: Our simplified multi-view cross-attention module built on standard attention. A single holistic query attends to all view features using conditioned positional encoding in a batch manner, enabling more efficient and scalable spatial fusion. V denotes the number of views. Learnable layers are highlighted in red, with naming aligned to Tab. 3*

## 实验与分析

### 主实验结果

EPFv2 在 EgoBody3M 基准上取得了显著的性能提升。如 Table 1 所示，EPFv2 的 MPJPE 达到 **4.02 cm**，相比 EgoBody3M 基线（5.18 cm）降低 **22.4%**，相比 EgoPoseFormer（4.75 cm）降低 **15.4%**。在时间一致性方面，EPFv2 的 MPJVE 降至 **0.42**，分别比 EgoBody3M（0.54）和 EgoPoseFormer（0.87）降低 **22.2%** 和 **51.7%**。手腕作为对 AR/VR 交互最关键的部位，EPFv2 的手腕 MPJPE 达到 **4.99 cm**，较 EgoBody3M（6.14 cm）降低 **18.7%**。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on Egobody3M benchmark. The percentage in parentheses denotes how much worse each baseline is compared to our method. †: indicates our reproduced results. ‡: presents results reported in the Egobody3M paper with missing metric numbers filled in with −. ALS is short for our Auto-Labeling System*

在 Ego4View-Syn 数据集上，即使移除了时间建模模块，EPFv2 的单帧变体依然在 PA-MPJPE 指标上超越先前方法，在 MPJPE 上保持竞争力（Table 6），验证了其空间推理能力的鲁棒性。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/015_Table_6.jpg]]
*Table 6: Comparison on Ego4View-Syn [7]. We evaluate a single-frame variant of EPFv2 on the Ego4View-Syn dataset. Despite removing temporal modeling, our method achieves strong results, outperforming prior works in PA-MPJPE and remaining competitive in MPJPE*

### 消融实验

Table 2 系统评估了各模块的贡献，揭示了以下关键发现：

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/006_Table_2.jpg]]
*Table 2: Ablation study. We remove or modify each module to assess its contribution. These results demonstrate that each component yields a measurable improvement in accuracy and our autolabeling system further boosts the model performance*

**姿态表示选择**：预测完整身体姿态参数并通过前向运动学（FK）恢复关键点位置，相比直接回归关键点坐标，能显著提升精度。这表明参数化姿态空间提供了更强的几何约束。

**投影条件的关键作用**：移除投影 2D 关键点作为条件嵌入（即去除 refinement decoder 的空间引导）导致性能大幅下降。该条件机制使模型能够将粗略 3D 提案显式投影到各视角图像平面，为交叉注意力提供精确的空间锚点，是两阶段 coarse-to-fine 设计的核心。

**辅助元数据初始化**：去除用于初始化 holistic query 的头显姿态等辅助元数据会降低模型的泛化能力。这表明头显 6DoF 姿态为整体查询提供了关键的先验空间上下文，尤其在遮挡严重时。

**不确定性建模**：加入每关节不确定性头（Student-t NLL 损失）有助于训练鲁棒性。模型能自适应地对高不确定性关节降低损失权重，避免被噪声标注误导。

**自动标注系统（ALS）**：ALS 将手腕 MPJPE 进一步降低 **11.7%**。添加不确定性蒸馏损失（教师与学生模型间的不确定性 MSE）能带来额外的小幅提升，证明教师模型的不确定性知识对学生的指导价值。

### 效率分析

EPFv2 的设计在效率上具有显著优势。Table 3 对比了不同空间注意力模块的计算量：EPFv1 的可变形注意力使用 16 个关节查询和参考点，FLOPs 为 622K；标准注意力的 16 查询基线因密集空间交互导致 FLOPs 高达 622K（4.75×）；而 EPFv2 的**单一整体查询 + 标准注意力**设计将 FLOPs 降至 **131K**，仅为 16 查询基线的约 1/4.75，同时参数量相当。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/011_Table_3.jpg]]
*Table 3: Layer-wise comparison of parameter count and FLOPs for different spatial attention modules. (1) EPFv1 uses deformable attention with 16 joint queries and reference points, introducing moderate compute and high development complexity. (2) A baseline standard attention setup with 16 queries shows 4.75× higher FLOPs due to dense spatial interactions. (3) Our final design adopts a single holistic query and standard attention, achieving the lowest computation (131K FLOPs) while maintaining similar parameter count to other variants*

与 EgoBody3M 的 LSTM 融合方案相比，EPFv2 在仅比较姿态估计头（假设共享 backbone）的情况下，显著降低了参数量和 FLOPs（Table 4）。端到端推理延迟方面，完整模型在 GPU 上仅需 **0.8 ms**（Table 5），满足实时 VR 设备的部署需求。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/012_Table_4.jpg]]
*Table 4: Efficiency Comparison with EgoBody3M. We compare only the pose estimation heads, assuming a shared backbone. EPFv2 significantly reduces parameter count and FLOPs, demonstrating the efficiency of its streamlined transformer design*

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/013_Table_5.jpg]]
*Table 5: Latency measurement of EPFv2*

### 编码器容量与时间序列长度的影响

Table 8 显示，更强的图像 backbone 能持续提升姿态估计精度。例如，使用 DINOv3-B 替代轻量 backbone 可带来显著增益，表明自我中心视角下强大的视觉特征提取对克服遮挡和自相似外观至关重要。

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/014_Table_8.jpg]]
*Table 8: Comparison across different image backbones. Larger backbones, such as DINOv3-B, significantly improve pose estimation accuracy, demonstrating the benefit of strong visual features in egocentric settings*

Table 7 分析了时间序列长度的影响：仅使用 2 帧会导致性能严重退化，而将窗口扩展至 16 帧能提供稳定且更优的精度。论文默认使用 16 帧以与 EgoBody3M 基线公平对比。

### 失败模式与局限性

尽管 EPFv2 在整体指标上表现优异，其自动标注系统的性能增益依赖于大规模私有无标注数据集 **EGO-ITW-70M**，这在一定程度上限制了社区完全复现半监督流程的能力。此外，模型的鲁棒性主要基于 EgoBody3M 的受控场景验证，在更多样化设备（如不同相机布局的头显）上的泛化表现尚待进一步证明。

### 补充图表

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/008_Figure_6.jpg]]
*Figure 6: ALS effectiveness in in-domain scaling. As more unlabeled data is used, both students achieve improved accuracy. Notably, the MobileNetv4-S-based model benefits more proportionally from ALS despite having lower model capacity, indicating the pipeline’s suitability for lightweight deployment models*

![[assets/figures/papers/paper_list_l1061_https_arxiv_org_abs_2603_04090/figures/009_Figure_7.jpg]]
*Figure 7: Deformable stereo attention module used in EPFv1 [65]. Each joint query independently attends to sampled image features via learned offsets and attention weights. Outputs from different views are sequentially fused using an MLP. This design introduces the specialized component with higher development complexity [64] and suboptimal hardware utilization. B, J, C, numpts, and h denote batch size, number of joints, feature channels, reference points, and attention heads, respectively. Learnable layers are highlighted in red, with layer names matching Tab. 3*

## 方法谱系与知识库定位

### 1. 问题域与技术演化脉络

自我中心（egocentric）人体姿态估计旨在仅从头戴式设备（如Apple Vision Pro[1]、Meta Quest 3[3]）捕获的多视角图像中恢复穿戴者的全身3D运动。与第三人称视角的姿态估计不同，该任务面临自遮挡严重、相机视场受限、缺乏全局场景参照等独特挑战。

早期方法以单帧热图回归为代表。**UnrealEgo**（Tome et al., ECCV 2022）首次系统性地探索了利用多视角RGB图像进行自我中心姿态估计，但其逐帧独立预测的设计忽略了时序信息，导致运动抖动和长时一致性差。

**EgoBody3M**（Zhao et al., ECCV 2024）引入了时序建模，使用LSTM融合多视角特征，并构建了大规模多视角自我中心数据集，显著推动了该领域的发展。然而，其LSTM架构在长程时序建模上存在固有局限，且特征融合方式相对简单，未能充分利用多视角几何约束。

**EgoPoseFormer (EPFv1)**（Yang et al., ECCV 2024）首次将Transformer引入该任务，提出了基于可变形注意力（deformable attention）的立体特征聚合模块，为每个关键点分配独立的查询令牌（Joint Query Tokens, JQTs）。这一设计实现了多视角特征的灵活聚合，但存在两个关键瓶颈：一是计算量随关键点数量线性增长（16个关键点需16个独立查询），二是可变形注意力的实现复杂度高、硬件利用率不理想。此外，EPFv1的姿态提案（proposal）与细化（refinement）两阶段之间缺乏端到端的梯度流动，限制了优化效率。

### 2. EPFv2的核心设计选择与差异化

EPFv2在继承EPFv1两阶段粗到细架构的基础上，进行了四项关键的结构性改进，形成了一条从“逐关节独立查询”到“整体条件化查询”的范式转变：

| 设计维度 | EPFv1 / EgoBody3M | EPFv2 | 改进动机 |
|---------|-------------------|-------|---------|
| 查询表示 | 每关键点独立JQT（计算量∝关键点数） | 单一整体查询（single holistic query） | 解耦计算量与姿态表示维度 |
| 空间注意力 | 可变形立体注意力（deformable stereo attention） | 条件化多视角标准交叉注意力 | 降低实现复杂度，提升硬件效率 |
| 时序建模 | 无（EPFv1）/ LSTM（EgoBody3M） | 因果时间注意力 + KV-cache | 实现流式推理与长程时序一致性 |
| 端到端训练 | 无梯度从Refinement流向Proposal | 完全可微，全梯度流动 | 提升优化效率与精度 |

**单一整体查询**是EPFv2最根本的设计创新。该查询从头显姿态等辅助元数据通过MLP初始化（Eq. 6），作为整个身体状态的紧凑信息聚合器。这一设计使得空间交叉注意力的计算量与关键点数量解耦——无论预测多少个关键点，仅需维护一个查询令牌。定量证据表明：相比使用16个查询的标准注意力基线，单查询方案将FLOPs降低了超过4倍（622K vs. 131K，Table 3）。

**条件化多视角交叉注意力**替代了EPFv1的可变形注意力。其核心思想是通过条件嵌入（conditional embedding）将视图身份和可选的投影2D关键点编码注入查询和图像特征中（Eq. 7-8）。在姿态提案阶段，条件嵌入仅包含视图身份；在姿态细化阶段，则额外附加来自粗略提案的投影2D关键点编码，为空间特征聚合提供明确的几何引导。这一设计使用标准注意力算子，避免了可变形注意力的自定义实现，显著降低了开发复杂度并提升了硬件利用率。

**因果时间注意力**引入RoPE（旋转位置编码）和KV-cache机制（Eq. 9），使模型能够以流式方式处理时序输入——每一帧仅需关注其历史窗口内的帧，无需重新计算整个序列。这为实时AR/VR部署提供了关键的推理效率保障。

### 3. 知识库定位：半监督学习与不确定性建模

EPFv2的自动标注系统（Auto-Labeling System, ALS）遵循半监督学习范式，采用教师-学生框架。教师模型在有标注数据上预训练后，为无标注数据生成伪标签；学生模型在混合批次（有标注+伪标注）上训练，并通过**不确定性蒸馏损失**（Eq. 13）对齐教师与学生预测的每关键点不确定性。

这一设计与通用半监督学习中的不确定性感知蒸馏方法（如FixMatch的置信度阈值、不确定性引导的自训练）一脉相承，但针对3D人体姿态估计进行了定制：不确定性以Cholesky分解的协方差矩阵形式建模（Eq. 11），采用多元Student-t分布的负对数似然作为损失函数，相比高斯分布对离群值更鲁棒。

### 4. 适用边界与局限

**数据依赖性**：ALS依赖于大规模私有无标注数据集EGO-ITW-70M（约7000万帧），这限制了社区完全复现半监督流程的能力。消融实验显示，ALS将手腕MPJPE进一步降低11.7%（Table 2），但这一增益的泛化性——在非Apple设备或不同相机配置下——尚需验证。

**设备与场景泛化**：主要定量结果在EgoBody3M基准上取得（MPJPE 4.02cm, MPJVE 0.42），该数据集使用Meta Quest头显的特定相机配置。尽管Figure 1展示了in-the-wild序列的定性结果，但模型在更多样化设备（如不同相机数量、基线距离、视场角）上的鲁棒性缺乏系统性评估。

**全身扩展性**：当前方法聚焦于身体关键点（body keypoints）估计，未涉及手指等精细部位。单一整体查询对同时预测身体、手部、面部等多异构任务的扩展性是一个开放问题。

### 5. 开放问题

1. **超大规模数据扩展**：ALS在7000万帧规模下展示了增益，但在更大数据量（如10亿帧级别）下是否仍能保持线性改善，或是否存在性能饱和点？
2. **多任务统一查询**：单一整体查询能否同时支撑姿态估计、动作识别、场景理解等异构任务，还是需要引入任务特定的查询解耦机制？
3. **跨设备零样本迁移**：模型在不同头显设备（如Quest 3 vs. Vision Pro）之间的零样本迁移能力如何？是否需要设备特定的微调或域适应策略？
4. **实时部署的全栈优化**：尽管推理延迟已低至0.8ms（GPU），但在移动端NPU上的量化部署、与SLAM/渲染管线的协同优化等工程问题仍是落地的关键瓶颈。

## 原文 PDF

![[paperPDFs/CVPR_2026/EgoPoseFormer_v2_Accurate_Egocentric_Human_Motion_Estimation_for_AR_VR.pdf]]