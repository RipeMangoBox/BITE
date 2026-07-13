---
title: "UniSH: Unifying Scene and Human Reconstruction in a Feed-Forward Pass"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniSH_Unifying_Scene_and_Human_Reconstruction_in_a_Feed_Forward_Pass.pdf
project_link: "https://murphylmf.github.io/UniSH/"
code_link: null
aliases:
- UniSH
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过设计三阶段训练策略（表面蒸馏、粗对齐、细对齐），有效利用未标注的真实世界视频，将专家深度模型的几何细节蒸馏到重建分支，并通过直接优化SMPL网格与人体点云的几何对应来桥接域差距。
primary_logic: 将预训练的场景重建模型（π³）和人体姿态估计模型（CameraHMR）的组合先验融合，通过轻量对齐网络和由粗到细的对齐监督，使单次前向传播即可实现高保真、度量尺度的场景和人体联合重建。
claims:
- 在Bonn数据集上，UniSH的Abs Rel达到0.035，比π³的0.049降低28.6%，δ<1.25精度0.980（vs 0.975）。
- 在EMDB-2上，UniSH的WA-MPJPE为118.5 mm，显著优于联合重建前馈基线JOSH3R（220.0 mm）。
- 消融实验表明，仅使用合成数据训练的模型在真实数据上的Abs Rel退化至0.062，而本文的蒸馏策略使其降至0.035，证明利用未标注数据是必要的。
- 图5的定性消融验证了由粗到细对齐策略对实现真实场景下鲁棒人景对齐的关键作用。
---

# UniSH: Unifying Scene and Human Reconstruction in a Feed-Forward Pass

> [!tip] 核心洞察
> 将预训练的场景重建模型（π³）和人体姿态估计模型（CameraHMR）的组合先验融合，通过轻量对齐网络和由粗到细的对齐监督，使单次前向传播即可实现高保真、度量尺度的场景和人体联合重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniSH：前馈式统一场景与人体重建 |
| 英文题名 | UniSH: Unifying Scene and Human Reconstruction in a Feed-Forward Pass |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.01222) · [Project](https://murphylmf.github.io/UniSH/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UniSH |
| Dataset | Bonn, EMDB-2 |

> [!tip] 效果简介
> - Bonn 上，Abs Rel ↓ 0.035 vs 0.049 (π³) (-0.014)；δ<1.25 ↑ 0.980 vs 0.975 (π³) (+0.005)。
> - EMDB-2 上，WA-MPJPE ↓ 118.5 vs 220.0 (JOSH3R) (-101.5)。

## 概要

从单目视频中同时恢复三维场景几何、相机参数和人体运动，是视觉理解的核心难题。现有前馈重建方法（如 **π³**、**VGGT**）虽能高效输出场景点云，但缺乏对人体的显式建模；专用人体姿态估计方法（如 **GVHMR**、**WHAM**）则忽略场景上下文，导致人-景关系割裂。联合重建的尝试（如 **JOSH3R**）仍受限于合成数据的域差距，在真实视频上的人体几何细节和对齐精度均不理想。

**UniSH** 提出了一种前馈式统一场景与人体重建框架，首次在单次前向传播中同时输出度量尺度的场景点云、相机位姿、SMPL人体网格及其全局运动。其核心创新在于：

1. **融合预训练先验的轻量对齐**：将场景重建模型（π³）与人体姿态估计模型（CameraHMR）的特征通过两层Transformer解码器（AlignNet）融合，联合预测全局尺度和每帧人体平移，实现度量尺度对齐。
2. **三阶段训练策略桥接域差距**：依次进行表面蒸馏（从MoGe-2专家模型注入高频几何细节）、合成数据粗对齐、未标注真实视频细对齐，有效利用大规模无标注数据克服sim-to-real退化。
3. **几何驱动的自监督对齐**：在细对齐阶段引入单边Chamfer距离与深度排序正则化，直接优化SMPL网格与人体点云的几何对应，无需真实标注即可实现鲁棒的人景对齐。

实验表明，UniSH在Bonn数据集上的人体视频深度估计Abs Rel达到0.035，较π³基线的0.049降低28.6%；在EMDB-2上的全局人体运动估计WA-MPJPE为118.5 mm，显著优于联合重建前馈基线JOSH3R（220.0 mm）。消融研究证实，仅使用合成数据训练会导致深度误差恶化（Abs Rel 0.062），而本文的蒸馏与对齐策略是泛化到真实场景的关键。UniSH是当前唯一同时重建3D场景的前馈方法，其性能可与专用HMR方法竞争，且无需优化迭代。

**局限性**包括：未标注数据以舞蹈视频为主，存在群体偏差；仅支持单人场景，无法处理多人交互；细对齐阶段依赖粗对齐初始化，增加了训练复杂度。



### 问题背景：场景与人体重建的割裂

从单目视频中理解三维世界是计算机视觉的核心目标之一。这一任务包含两个紧密关联的子问题：**三维场景重建**和**三维人体重建**。前者恢复环境的几何结构与相机运动，后者估计人体的姿态、形状与全局运动。在真实应用中——例如增强现实、人机交互、运动分析——场景与人体并非孤立存在：人体在场景中移动、与地面接触、被环境遮挡，二者共享同一度量空间和相机参数。

然而，现有方法几乎将这两个问题完全割裂处理。场景重建方法（如 **π³**、**VGGT**）在前馈式点云和相机估计上取得了显著进展，但它们将人体视为场景中的普通几何点，无法解析人体的语义结构与运动。另一方面，人体重建方法（如 **GVHMR**、**WHAM**、**TRAM**）专注于从视频中恢复精确的SMPL参数和全局运动，但它们**不重建三维场景**，因而无法获得人体与环境的真实空间关系。

### 联合重建的瓶颈：数据稀缺与域差距

将场景与人体统一重建面临一个核心瓶颈：**大规模真实标注数据的极度稀缺**。要训练一个联合模型，需要同时标注场景的度量深度、相机参数，以及人体的SMPL顶点和关节位置。这种全标注数据在实际中几乎不可能大规模获取。现有方法被迫依赖合成数据（如BEDLAM数据集），但这引入了严重的 **sim-to-real域差距**：合成场景的纹理、光照、人体外观与真实世界存在系统性差异，导致模型在真实视频上泛化能力差，表现为人体几何细节丢失、人体与场景的对齐错误。

### 现有联合方法的局限

目前唯一的前馈式联合重建基线是 **JOSH3R**，它尝试在单一网络中同时输出场景点云和人体参数。然而，JOSH3R在真实数据上的表现远不理想——在EMDB-2数据集上，其全局人体运动误差WA-MPJPE高达220.0 mm，远高于专用人体重建方法。这暴露了仅依赖合成数据训练的联合方法在真实场景中的根本缺陷。

### 本文动机：桥接域差距的前馈式统一框架

本文的核心动机在于回答一个关键问题：**能否在不依赖大量全标注真实数据的前提下，实现高保真、度量尺度的场景与人体联合重建？**

我们的核心洞察是：可以利用两个预训练专家模型——场景重建模型（π³）和人体姿态估计模型（CameraHMR）——各自在合成数据上习得的强大先验，然后通过**利用未标注的真实世界视频**来桥接域差距。具体而言，我们设计了三个关键技术：

1. **轻量对齐网络（AlignNet）**：融合场景几何特征与人体特征，联合预测全局尺度和每帧人体平移，将两个分支的输出统一到同一度量空间。
2. **表面细节蒸馏**：从专家单目深度模型（MoGe-2）的伪标签中，将高频人体表面细节蒸馏到多视图重建分支中，解决通用重建模型输出粗糙人体几何的问题。
3. **由粗到细的对齐训练**：先用合成数据学习粗对齐，再利用未标注真实数据通过几何对齐损失（单边Chamfer距离）和深度排序正则化进行细对齐，使SMPL网格与可见人体点云在物理上正确对应。

通过这一设计，UniSH在单次前向传播中即可输出度量尺度的场景点云、相机参数和SMPL人体参数，在Bonn数据集上将深度误差Abs Rel从π³的0.049降至0.035（降低28.6%），在EMDB-2上将人体运动误差从JOSH3R的220.0 mm降至118.5 mm（降低46.1%），同时保持了前馈方法的实时性优势。



## 核心方法与创新机理

UniSH 的核心创新在于将**场景重建**与**人体姿态估计**这两个此前独立发展的前馈式模型，通过一个轻量的**对齐网络（AlignNet）**和一套**三阶段训练策略**融合为单一的前向传播框架，首次实现了度量尺度下场景与人体网格的联合重建。其关键 changed slots 可归纳为以下三个维度。

### 1. 度量尺度的全局对齐：AlignNet

此前的通用场景重建模型（如 **π³** 和 **VGGT**）能够输出高质量的点云和相机位姿，但缺乏全局尺度信息，无法将人体以正确的物理尺寸放置于场景中。UniSH 引入了一个由两层 Transformer 解码器构成的 **AlignNet**，其核心操作可形式化为：

$$( s , \mathcal { T } ) = \mathrm { A l i g n N e t } ( \mathcal { F } _ { \mathrm { g e o } } , [ T _ { s } | \mathcal { F } _ { \mathrm { h m r } } ] )$$

该模块以场景重建分支提取的几何特征 $\mathcal{F}_{\mathrm{geo}}$ 作为键/值对（K/V），将可学习的尺度令牌 $T_s$ 与人体分支输出的 HMR 特征 $\mathcal{F}_{\mathrm{hmr}}$ 拼接后作为查询（Q），联合预测全局场景尺度 $s$ 和每帧 SMPL 模型的平移量 $\mathcal{T} = \{t_i\}$。这一设计使得人体网格能够以度量尺度被“放置”到场景点云中，从根本上解决了前馈式联合重建的尺度缺失问题。

### 2. 人体表面几何的细节蒸馏

通用重建模型（如 π³）虽然多视图一致性良好，但输出的人体点云几何粗糙，缺乏高频表面细节。UniSH 提出了一种**置信度感知的局部深度蒸馏**策略：利用专家单目深度模型（MoGe-2）为未标注的真实视频生成伪深度标签，然后在人体锚点周围的局部图像块内，通过最小二乘求解器对齐预测深度与伪深度，并计算置信度加权的 L1 损失：

$$\mathcal { L } _ { h , i } = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \left( \frac { 1 } { | \mathcal { N } _ { k } | } \sum _ { j = 1 } ^ { | \mathcal { N } _ { k } | } C _ { k } ^ { j } \cdot | ( s _ { k } \cdot \hat { D } _ { k } ^ { j } + t _ { k } ) - D _ { k } ^ { j } | \right)$$

同时辅以对原始点云的正则项 $\Vert P_i - P_i^{\mathrm{orig}} \Vert_1$ 来保持多视图一致性。这一蒸馏机制的关键在于：**仅依赖未标注的真实世界视频即可将专家模型的高保真几何细节迁移到多视图重建框架中**，无需任何真实深度标注。

### 3. 由粗到细的人景对齐监督

直接将合成数据训练的模型应用于真实场景会遭遇严重的 sim-to-real 域差距。UniSH 设计了两阶段对齐策略：

- **粗对齐阶段（Stage 2）**：在合成数据集 BEDLAM 上使用强监督信号（SMPL 顶点、3D/2D 关键点、姿态、形状和尺度对齐的平移量）学习初始的 SMPL 放置能力，损失函数为：

$$\begin{array} { r l } \mathcal { L } _ { \mathrm { s m p l } , i } = & \lambda _ { \mathrm { v } } \| V _ { \mathrm { s m p l } , i } - V _ { \mathrm { s m p l } , i } ^ { \mathrm { g t } } \| _ { 1 } + \lambda _ { \mathrm { j } 3 \mathrm { d } } \| J _ { 3 \mathrm { d } , i } - J _ { 3 \mathrm { d } , i } ^ { \mathrm { g t } } \| _ { 1 } \\ & + \lambda _ { \mathrm { j } 2 \mathrm { d } } \| J _ { 2 \mathrm { d } , i } - J _ { 2 \mathrm { d } , i } ^ { \mathrm { g t } } \| _ { 1 } + \lambda _ { \mathrm { p o s e } } \| \theta _ { i } - \theta _ { i } ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } \\ & + \lambda _ { \mathrm { s h a p e } } \| \beta - \beta ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } + \lambda _ { \mathrm { t r a n s } } \| s _ { \mathrm { o p t } } \cdot t _ { i } - t _ { i } ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } \end{array}$$

- **细对齐阶段（Stage 3）**：在未标注的真实视频上，通过两个无监督几何损失桥接域差距。其一是从可见 SMPL 顶点到带尺度人体点云的**单向 Chamfer 距离**，直接优化几何对应：

$$\mathcal { L } _ { \mathrm { a l i g n } , i } = \sum _ { v _ { \mathrm { s r c } } \in V _ { \mathrm { s r c } , i } } \operatorname* { m i n } _ { v _ { \mathrm { t g t } } \in V _ { \mathrm { t g t } , i } } \| v _ { \mathrm { s r c } } - v _ { \mathrm { t g t } } \| _ { 2 } ^ { 2 }$$

其二是**深度排序正则化**，惩罚人体点云平均深度大于 SMPL 网格深度的情形，确保可见表面不被错误遮挡：

$$\mathcal { L } _ { \mathrm { d r e g } , i } = \mathrm { R e L U } ( \bar { d } _ { \mathrm { t g t } , i } - \bar { d } _ { \mathrm { s r c } , i } )$$

消融实验（Figure 5、Figure 7）证实：移除细对齐阶段会导致真实场景下人景对齐完全失效；去除深度正则化则会使 SMPL 网格浮在点云前方，破坏物理合理性。值得注意的是，若完全跳过粗对齐阶段，训练将无法收敛——这表明合成数据的初始化作用在当前框架中仍是不可或缺的。

### 创新点的因果闭环

上述三个 changed slots 形成了一条清晰的因果链：**AlignNet 提供了尺度与位置的全局骨架**，使度量级联合重建成为可能；**表面蒸馏将单目专家模型的高频细节注入多视图框架**，解决了通用重建模型人体几何粗糙的瓶颈；**由粗到细的对齐监督则有效利用了合成数据的标注优势和真实数据的分布优势**，使模型在真实场景中实现鲁棒的人景对齐。三者共同作用，使得 UniSH 在 Bonn 数据集上将 Abs Rel 从 π³ 的 0.049 降至 0.035（降低 28.6%），在 EMDB-2 上将 WA-MPJPE 从联合重建基线 JOSH3R 的 220.0 mm 降至 118.5 mm。



UniSH 是一个前馈式联合重建框架，以单目视频片段为输入，在单次前向传播中同时预测度量尺度的场景几何、相机参数以及人体姿态与形状。如图2所示，框架由三个核心模块构成：**场景重建分支**、**人体重建分支**和**对齐网络（AlignNet）**。

**输入与输出。** 给定 $N$ 帧图像序列 $\mathcal{T} = \{I_i\}_{i=1}^N$，UniSH 在单次前向传播中输出：
- 每帧的度量尺度点云 $P_i$ 及对应的置信度图 $C_i$；
- 每帧的相机外参 $E_i$ 和从点云推导的内参 $K$；
- 全局共享的 SMPL 体型参数 $\beta$ 和每帧姿态参数 $\theta_i$；
- 全局场景尺度 $s$ 和每帧 SMPL 平移向量 $t_i$，用于将人体网格对齐到度量尺度场景中。

**场景重建分支。** 基于 $\pi^3$ 架构，该分支以完整视频帧为输入，通过点图解码器预测每帧的相机外参 $E_i$、置信度图 $C_i$ 和点云 $P_i$，并从中推导相机内参 $K$。该分支同时提取场景几何特征 $\mathcal{F}_{\mathrm{geo}}$，作为 AlignNet 的键/值对输入。

**人体重建分支。** 基于 CameraHMR，该分支处理从视频中裁剪的人体区域，结合焦距信息回归每帧 SMPL 姿态 $\theta_i$ 和共享体型 $\beta$，并提取人体特征令牌 $\mathcal{F}_{\mathrm{hmr}}$。

**对齐网络（AlignNet）。** 一个两层 Transformer 解码器，将场景几何特征 $\mathcal{F}_{\mathrm{geo}}$ 作为键/值对，将可学习的尺度令牌 $T_s$ 与人体特征 $\mathcal{F}_{\mathrm{hmr}}$ 拼接作为查询，联合预测全局尺度 $s$ 和每帧平移集合 $\mathcal{T}$：

$$(s, \mathcal{T}) = \mathrm{AlignNet}(\mathcal{F}_{\mathrm{geo}}, [T_s | \mathcal{F}_{\mathrm{hmr}}])$$

该设计使人体与场景在统一的度量尺度下实现空间对齐，避免了传统方法中场景与人体分别估计导致的尺度不一致问题。

**数据流概要。** 视频帧同时流入场景重建分支和人体重建分支；场景分支输出几何特征与相机参数，人体分支输出 SMPL 参数与人体特征；AlignNet 融合两路特征，预测全局尺度与每帧平移，最终将 SMPL 网格放置到度量尺度场景中，实现端到端的联合重建。

### 补充图表

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/002_Figure_2.jpg]]
*Figure 2: The network architecture of UniSH. UniSH takes a monocular video as input. The video frames are processed by the Reconstruction Branch to predict per-frame camera extrinsics*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/001_Figure_1.jpg]]
*Figure 1: Given a monocular video as input, our UniSH is capable of jointly reconstructing scene and human in a single forward pass, enabling effective estimation of scene geometry, camera parameters and SMPL parameters*



UniSH 的核心架构由三个功能模块构成，分别负责场景几何重建、人体参数回归以及人-景度量尺度对齐。整体数据流如 Figure 2 所示：输入一段 $N$ 帧的单目视频，经双分支处理后由 AlignNet 融合特征，输出全局尺度 $s$ 与每帧 SMPL 平移 $\{t_i\}_{i=1}^N$，最终实现前馈式的联合重建。

### 场景重建分支 (Scene Reconstruction Branch)

该分支基于 **π³** 的前馈重建架构，逐帧处理输入图像 $I_i$，预测相机外参 $E_i$、置信度图 $C_i$ 及点云 $P_i$，并由点云推导出相机内参 $K_i$。分支输出的场景几何特征 $\mathcal{F}_{\mathrm{geo}}$ 将作为 AlignNet 的键/值对输入。

### 人体分支 (Human Body Branch)

该分支以 **CameraHMR** 为基础，接收从原图裁剪的人体区域及焦距信息，回归每帧 SMPL 姿态参数 $\theta_i$ 和共享形状参数 $\beta$，同时提取人体特征令牌 $\mathcal{F}_{\mathrm{hmr}}$ 供 AlignNet 查询使用。

### AlignNet：尺度预测与 SMPL 放置

AlignNet 是一个两层 Transformer 解码器，负责将人体与场景在度量尺度下对齐。其核心公式为：

$$( s , \mathcal { T } ) = \mathrm { A l i g n N e t } ( \mathcal { F } _ { \mathrm { g e o } } , [ T _ { s } | \mathcal { F } _ { \mathrm { h m r } } ] )$$

其中，$T_s$ 为可学习的尺度令牌，$[\cdot|\cdot]$ 表示拼接操作。AlignNet 以场景几何特征 $\mathcal{F}_{\mathrm{geo}}$ 作为键/值对，以尺度令牌与人体特征令牌的拼接作为查询，联合预测全局场景尺度 $s$ 和每帧 SMPL 平移集合 $\mathcal{T} = \{t_i\}_{i=1}^N$。这一设计使人体网格能够被准确放置在度量尺度的场景点云中。

### 人体表面细化损失（阶段一）

为从专家模型 MoGe-2 的伪深度标签中蒸馏高频几何细节，UniSH 在人体锚点周围的局部块内进行置信度加权的深度监督。对于第 $i$ 帧，损失定义如下：

$$\mathcal { L } _ { h , i } = \frac { 1 } { K } \sum _ { k = 1 } ^ { K } \left( \frac { 1 } { | \mathcal { N } _ { k } | } \sum _ { j = 1 } ^ { | \mathcal { N } _ { k } | } C _ { k } ^ { j } \cdot | ( s _ { k } \cdot \hat { D } _ { k } ^ { j } + t _ { k } ) - D _ { k } ^ { j } | \right)$$

其中，$K$ 为锚点数量，$\mathcal{N}_k$ 为第 $k$ 个锚点的局部邻域像素集，$C_k^j$ 为对应像素的置信度权重，$\hat{D}_k^j$ 和 $D_k^j$ 分别为预测深度与伪标签深度。$s_k$ 与 $t_k$ 由局部 RANSAC 优化的刚性变换求解器 (ROE) 估计，用于将预测深度与伪深度在局部块内对齐后再计算 L1 误差。阶段一的总损失结合了该局部人体损失与对原始点云的正则化项：

$$\mathcal { L } _ { \mathrm { s t a g e 1 } } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \left( \lambda _ { h } \mathcal { L } _ { h , i } + \lambda _ { \mathrm { p r e g } } \Vert P _ { i } - P _ { i } ^ { \mathrm { o r i g } } \Vert _ { 1 } \right)$$

正则化项约束细化后的点云 $P_i$ 不过度偏离原始点云 $P_i^{\mathrm{orig}}$，以保持多视图一致性。

### 粗对齐损失（阶段二）

阶段二使用合成数据集 BEDLAM 的真值监督，学习人体在场景中的初始放置。每帧的 SMPL 损失为：

$$\begin{array} { r l } & { \mathcal { L } _ { \mathrm { s m p l } , i } = \lambda _ { \mathrm { v } } \| V _ { \mathrm { s m p l } , i } - V _ { \mathrm { s m p l } , i } ^ { \mathrm { g t } } \| _ { 1 } + \lambda _ { \mathrm { j } 3 \mathrm { d } } \| J _ { 3 \mathrm { d } , i } - J _ { 3 \mathrm { d } , i } ^ { \mathrm { g t } } \| _ { 1 } } \\ & { \phantom { \mathcal { L } } + \lambda _ { \mathrm { j } 2 \mathrm { d } } \| J _ { 2 \mathrm { d } , i } - J _ { 2 \mathrm { d } , i } ^ { \mathrm { g t } } \| _ { 1 } + \lambda _ { \mathrm { p o s e } } \| \theta _ { i } - \theta _ { i } ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } } \\ & { \phantom { \mathcal { L } } + \lambda _ { \mathrm { s h a p e } } \| \beta - \beta ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } + \lambda _ { \mathrm { t r a n s } } \| s _ { \mathrm { o p t } } \cdot t _ { i } - t _ { i } ^ { \mathrm { g t } } \| _ { 2 } ^ { 2 } } \end{array}$$

该损失同时监督顶点 ($V_{\mathrm{smpl}}$)、3D 关键点 ($J_{\mathrm{3d}}$)、2D 投影关键点 ($J_{\mathrm{2d}}$)、姿态 ($\theta$)、形状 ($\beta$) 以及经全局最优尺度 $s_{\mathrm{opt}}$ 对齐后的平移项。阶段二总损失为所有帧的 SMPL 损失与全局尺度监督之和：

$$\mathcal { L } _ { \mathrm { s t a g e 2 } } = \frac { \lambda _ { \mathrm { s m p l } } } { N } \sum _ { i = 1 } ^ { N } \mathcal { L } _ { \mathrm { s m p l } , i } + \lambda _ { \mathrm { s c a l e } } \Vert s - s _ { \mathrm { o p t } } \Vert _ { 1 }$$

### 细对齐损失与深度排序正则化（阶段三）

阶段三利用未标注的真实世界视频，通过无监督几何损失桥接 sim-to-real 域差距。核心是对齐损失——从可见 SMPL 顶点到带尺度的人体点云的单向 Chamfer 距离：

$$\mathcal { L } _ { \mathrm { a l i g n } , i } = \sum _ { v _ { \mathrm { s r c } } \in V _ { \mathrm { s r c } , i } } \operatorname* { m i n } _ { v _ { \mathrm { t g t } } \in V _ { \mathrm { t g t } , i } } \| v _ { \mathrm { s r c } } - v _ { \mathrm { t g t } } \| _ { 2 } ^ { 2 }$$

其中 $V_{\mathrm{src},i}$ 为第 $i$ 帧的可见 SMPL 顶点集，$V_{\mathrm{tgt},i}$ 为对应的人体点云。为强制物理合理性，引入深度排序正则化：

$$\mathcal { L } _ { \mathrm { d r e g } , i } = \mathrm { R e L U } ( \bar { d } _ { \mathrm { t g t } , i } - \bar { d } _ { \mathrm { s r c } , i } )$$

该正则项惩罚目标点云（人体表面）的平均深度 $\bar{d}_{\mathrm{tgt},i}$ 大于源点云（SMPL 网格）的平均深度 $\bar{d}_{\mathrm{src},i}$，确保人体网格不会浮在可见点云前方。阶段三总损失为：

$${ \mathcal { L } } _ { \mathrm { s t a g e 3 } } = { \frac { 1 } { N } } \sum _ { i = 1 } ^ { N } \left( \lambda _ { \mathrm { a l i g n } } { \mathcal { L } } _ { \mathrm { a l i g n } , i } + \lambda _ { \mathrm { d e p t h } } { \mathcal { L } } _ { \mathrm { d r e g } , i } + \lambda _ { \mathrm { j 2 d } } { \mathcal { L } } _ { \mathrm { j 2 d } , i } \right)$$

消融实验 (Figure 7) 证实：移除对齐损失会导致模型因域差距无法预测正确的场景尺度与 SMPL 放置；移除深度正则化则造成人体网格与可见点云的深度关系错误，破坏物理合理性。此外，细对齐阶段必须依赖粗对齐的初始化，否则训练无法收敛。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/010_Figure_7.jpg]]
*Figure 7: Visual ablation of the Fine-grained Alignment stage. We validate the necessity of our unsupervised geometric losses on inthe-wild data. w/o Align Loss: Without explicit geometric alignment*

### 补充图表

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study of our key design. (a) A variant where the scene branch is directly supervised for metric scale, and the Align Net only predicts SMPL translation. (b) Our model trained with only the coarse (synthetic) alignment stage, omitting the fine-grained alignment. (c) Our full model, which incorporates both coarse (synthetic) and fine-grained (real-world) alignment stages*



## 实验与关键发现

### 1. 核心定量结果

**人体中心视频深度估计**。Table 1 报告了在 Bonn 数据集上的深度估计结果。UniSH 的 **Abs Rel 达到 0.035**，较通用场景重建基线 **π³** 的 0.049 降低了 28.6%；**δ<1.25 精度达到 0.980**（π³ 为 0.975）。同时显著优于另一前馈重建基线 VGGT（Abs Rel 0.057, δ<1.25 0.966）。这一提升的核心驱动力来自人体表面细化策略——通过从专家模型 MoGe-2 的伪深度标签中蒸馏高保真几何细节，使重建分支在保持多视图一致性的同时输出精细的人体点云。

**全局人体运动估计**。Table 2 在 EMDB-2 和 RICH 两个数据集上评估了全局运动估计能力。在 EMDB-2 上，UniSH 的 **WA-MPJPE 为 118.5 mm**，显著优于同为前馈式联合重建的基线 **JOSH3R**（220.0 mm），差距达 101.5 mm。与专用的 HMR 方法（如 GVHMR）相比，UniSH 的全局运动指标略弱，但这一折衷源于方法设计定位的根本差异：UniSH 是唯一同时重建 3D 场景几何的前馈方法，且仅依赖弱监督的未标注真实数据训练，而专用 HMR 方法需要大量高质量标注。Table 2 明确标注了各方法的属性（是否前馈、是否联合重建场景），确保了公平性评估。

### 2. 消融实验

**人体表面细化策略**。Table 3 的消融实验揭示了训练数据源对深度估计精度的决定性影响。仅使用 BEDLAM 合成数据微调导致 Abs Rel 退化至 0.062（甚至差于原始 π³ 的 0.049），直接验证了 sim-to-real 域差距的严重性。而本文提出的蒸馏策略——仅使用未标注真实世界数据配合置信度感知的局部人体损失——将 Abs Rel 降至最优的 0.035。这证明利用未标注真实数据是桥接域差距、实现高保真人体几何的关键。

Figure 6 从定性角度展示了人体表面细化的效果：π³ 基线保持良好跨帧一致性但人体几何粗糙；专家单目模型 MoGe-2 虽细节丰富但缺乏多视图一致性；UniSH 完整方法成功将高频表面细节蒸馏到多视图重建框架中，兼顾了高保真度与跨帧一致性。

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative Impact of Human Surface Refinement. Comparison illustrating the effectiveness of our specialized surface refinement strategy. The*

**由粗到细的对齐策略**。Figure 5 的定性消融直接验证了对齐策略的必要性：(a) 直接监督场景分支预测度量尺度、AlignNet 仅预测平移的变体，在真实场景中人景对齐失败；(b) 仅使用粗对齐阶段（合成数据训练）的模型泛化极差；(c) 完整模型（粗对齐 + 细对齐）实现了正确的人景对齐。Figure 7 进一步消融了细对齐阶段的组件：移除几何对齐损失 $\mathcal{L}_{\mathrm{align}}$ 导致模型无法预测正确的场景尺度和 SMPL 位置；移除深度排序正则化 $\mathcal{L}_{\mathrm{dreg}}$ 则使 SMPL 网格浮在可见人体点云前方，破坏物理合理性。完整细对齐方法实现了准确的全局对齐和正确的深度次序。

### 3. 定性分析

**野外场景的人体点云质量**。Figure 3 在野外视频输入下与强重建基线进行了定性比较。得益于表面细化策略，UniSH 生成的人体点云在表面细节上一致优于 VGGT、CUT3R 等基线方法。

**全局人体运动估计**。Figure 4 在 EMDB-2 上与专用 HMR 方法 WHAM 和 TRAM 进行了定性对比。尽管 UniSH 并非专为全局运动估计设计和优化，其结果仍表现出竞争力，验证了联合重建框架在人体运动估计上的潜力。

**联合场景与人体重建**。Figure 8 展示了在攀岩和城市环境中的定性结果。颜色梯度（浅蓝到深蓝）统一编码了相机轨迹和 SMPL 网格的时间序列。攀岩案例验证了框架对高度关节化姿态的鲁棒性及 SMPL 网格与场景几何的准确对齐；城市环境案例展示了复杂场景下长期人体运动的连贯跟踪，验证了度量稳定性和泛化能力。

### 4. 失败模式与局限性

根据分析，UniSH 存在以下已知局限：

1. **数据偏差与伪标签噪声**：未标注野外数据以舞蹈视频为主，可能存在群体偏差；方法依赖 MoGe-2 的伪深度标签，可能引入噪声并导致人体点云悬浮伪影（floaters）。
2. **单人场景限制**：方法设计仅考虑视频中单人场景，无法处理多人交互或遮挡情况。
3. **训练阶段复杂性**：细对齐阶段需要粗对齐初始化，否则训练不收敛（Figure 7 明确标注了移除粗对齐导致训练发散），增加了训练流程的复杂性。

### 补充图表

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/003_Table_1.jpg]]
*Table 1: Quantitative results of human-centric video depth estimation on the Bonn [30] dataset. Our approach, UniSH, significantly outperforms all prior reconstruction-focused baselines*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/006_Table_2.jpg]]
*Table 2: Evaluation of global human motion estimation on EMDB-2 and RICH datasets. We categorize methods by their properties: Opt. Free(✓) indicates whether the method is feed-forward; Scene(✓) indicates the method jointly reconstructs 3D scene geometry*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/008_Table_3.jpg]]
*Table 3: Ablation study of our human surface refinement on the Bonn [30] dataset. ’BEDLAM’ denotes fine-tuning using only ground-truth (GT) supervision from the synthetic BEDLAM dataset. ’Real’ means using only real-world data and our proposed surface refinement loss*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons of human point cloud. With in-the-wild input, we compare the reconstructed human point cloud with strong reconstruction model baselines. Benefit from our surface refinement strategy, our UniSH generates consistently better human surface point cloud than all baseline methods*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results of global human motion estimation. We compare our method with well known HMR methods WHAM [41] and TRAM [56] on EMDB-2. Our method shows competitive results to these methods that specially designed and optimized for global human motion estimation task*

![[assets/figures/papers/paper_list_l1038_https_arxiv_org_abs_2601_01222/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative Visualization of Joint Scene and Human Reconstruction. The examples demonstrate the robustness and metric consistency of our framework. The color gradient (light blue to dark blue) consistently encodes the temporal sequence across both the reconstructed camera poses and the SMPL meshes. The upper example illustrates robustness in reconstructing highly articulated poses (rock climbing) and accurately aligning the SMPL mesh with the scene geometry. The lower example demonstrates coherent, long-term tracking of human motion in a complex urban environment, verifying the metric stability and generalization of our joint reconstruction framework*



## 定位与知识库关联

### 与前馈式场景/人体重建基线的关系

UniSH 处于前馈式联合重建的交汇点，同时处理场景几何、相机参数和人体网格的端到端推断。其核心架构建立在两个预训练分支的融合之上：

- **场景重建分支**基于 **π³** 的架构，该基线在通用场景重建中已展现出强前馈能力。UniSH 保留了 π³ 从图像序列预测每帧外参、置信度图和点云的核心流程，但 π³ 本身缺乏度量尺度感知和人体建模能力。在 Bonn 数据集上，π³ 的深度估计 Abs Rel 为 0.049，UniSH 通过引入尺度预测和对齐网络将这一指标降至 0.035（Table 1）。

- **人体分支**采用 **CameraHMR** 的回归框架，从人体裁剪框和焦距输入中估计 SMPL 姿态和形状参数。与专用的 HMR 前馈方法（如 **GVHMR**）不同，UniSH 的人体分支并非独立优化全局运动，而是将人体特征令牌作为对齐网络的查询输入，实现场景约束下的人体定位。

- 在联合重建的前馈基线中，**JOSH3R** 是唯一同时输出场景和人体网格的方法。然而，JOSH3R 在真实视频上的全局人体运动估计表现显著弱于 UniSH——在 EMDB-2 上 WA-MPJPE 为 220.0 mm，而 UniSH 达到 118.5 mm（Table 2）。这一差距源于 JOSH3R 缺乏针对真实域差距的对齐策略。

- 与通用场景重建基线 **VGGT** 相比，UniSH 的人体表面细节明显更优。Figure 3 的定性比较显示，VGGT 重建的人体点云粗糙且缺乏身体形状一致性，而 UniSH 通过表面蒸馏策略保留了高频几何细节。

### 与专用人体运动估计方法的关系

UniSH 与专用的全局人体运动估计方法（如 **WHAM** 和 **TRAM**）存在本质差异。这些方法专门为人体运动捕捉设计和优化，通常依赖强监督信号（如高质量的运动捕捉标注）。UniSH 则是一个联合重建框架，主要依赖未标注野外数据的弱监督。这种设计权衡在 Table 2 中明确体现：UniSH 在全局运动指标上略逊于专用方法，但它是唯一同时重建完整 3D 场景的前馈方法。公平性评估中，论文明确标注了各方法的属性（是否前馈、是否联合重建场景），避免不公平比较。

### 适用边界与局限

1. **单人场景约束**：UniSH 的设计假设视频中仅存在单个人体实例。AlignNet 的尺度和平移预测、细对齐阶段的单边 Chamfer 损失均基于单人 SMPL 网格与对应人体点云的几何对应。该方法无法处理多人交互或遮挡场景，扩展到多人需要重新设计对齐机制和损失函数。

2. **数据依赖与域差距的残余影响**：尽管三阶段训练策略有效桥接了 sim-to-real 域差距，但方法仍依赖合成数据 **BEDLAM** 进行粗对齐初始化。消融实验表明，完全移除合成数据会导致训练不收敛（Figure 7 说明）。细对齐阶段使用的未标注野外数据以舞蹈视频为主，可能存在群体偏差，影响在非舞蹈场景（如运动、日常活动）上的泛化。

3. **伪深度标签引入的噪声**：人体表面细化依赖 **MoGe-2** 专家模型生成的伪深度标签。蒸馏过程虽然通过置信度加权和局部块对齐缓解了噪声影响，但伪标签的误差仍可能导致人体点云出现悬浮伪影（floaters）。Figure 6 中，专家模型本身缺乏多视图一致性，蒸馏后的 UniSH 虽有所改善，但论文承认悬浮问题尚未完全解决。

4. **训练流程的复杂性**：三阶段训练（表面蒸馏 → 粗对齐 → 细对齐）增加了训练调度的复杂性。细对齐阶段必须依赖粗对齐的初始化，否则训练发散。这种阶段依赖性限制了端到端联合优化的可能性。

### 开放问题与后续方向

1. **利用对齐 SMPL 网格作为几何先验**：当前方法中，SMPL 网格仅用于对齐监督，未被用于细化人体表面。一个自然的延伸是将已对齐的 SMPL 网格作为几何先验，正则化人体点云的表面重建，以去除悬浮伪影并增强形状一致性。

2. **多人场景扩展**：将 UniSH 扩展到多人场景需要解决个体间的空间关系建模。可能的路径包括引入实例级对齐网络、设计多人互不穿透的约束损失，以及处理遮挡情况下的人体推理。

3. **完全自监督的尺度学习**：当前粗对齐阶段依赖合成数据的度量尺度监督。探索完全从未标注真实数据中自监督学习全局尺度的方案（例如通过场景中的已知尺寸物体或运动线索），可以进一步降低对合成数据的依赖，提升方法的通用性。

4. **跨域泛化的鲁棒性验证**：论文主要在 Bonn、EMDB-2 和 RICH 数据集上评估，这些数据集以人体为中心。在更广泛的场景类型（如无人体存在的纯场景视频、极端光照条件）上的泛化能力尚待验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/UniSH_Unifying_Scene_and_Human_Reconstruction_in_a_Feed_Forward_Pass.pdf]]
