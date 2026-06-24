---
title: "PixARMesh: Autoregressive Mesh-Native Single-View Scene Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PixARMesh_Autoregressive_Mesh_Native_Single_View_Scene_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- PixARMesh
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将物体位姿估计与网格生成统一为自回归序列预测：通过将位姿编码为包围盒角点并使用网格量化标记，使位姿预测与网格生成共享标记词表，在一个自回归Transformer解码器中完成；同时增强点云编码器，融入像素对齐的图像特征和场景级交叉注意力，以补偿单视图观测的遮挡和缺失几何信息。
primary_logic: 艺术家级网格生成的自回归范式可以扩展到场景级重建，只需将物体位姿作为令牌序列与网格令牌拼接，并由统一的解码器学习布局推理与几何生成的协同关系。像素对齐的图像特征为部分观测的点云提供了外观线索，而场景上下文的交叉注意力使每个实例的潜在编码能感知全局空间关系，从而在无后处理优化的情况下直接生成全局一致的场景网格。
claims:
- PixARMesh在3D-FRONT数据集上取得了场景级重建的最新水平，其EdgeRunner变体的场景Chamfer距离为98.8×10⁻³、F分数为33.55%，均优于SDF类方法（如DepR的153.2和25.00%）。
- 联合位姿-网格建模相比两阶段分离设计显著提升了物体重建质量（CD从4.75降至4.04，F-Score从80.85升至82.27）。
- 移除像素对齐图像特征导致场景级和物体级性能的大幅下降，证明了外观线索对补偿遮挡几何的重要性。
- 使用真值深度可将物体级Chamfer距离从4.13降至3.04，F分数从81.64%提升至86.66%，表明深度精度是性能提升的关键瓶颈。
---

# PixARMesh: Autoregressive Mesh-Native Single-View Scene Reconstruction

> [!tip] 核心洞察
> 艺术家级网格生成的自回归范式可以扩展到场景级重建，只需将物体位姿作为令牌序列与网格令牌拼接，并由统一的解码器学习布局推理与几何生成的协同关系。像素对齐的图像特征为部分观测的点云提供了外观线索，而场景上下文的交叉注意力使每个实例的潜在编码能感知全局空间关系，从而在无后处理优化的情况下直接生成全局一致的场景网格。

| 字段 | 内容 |
|------|------|
| 中文题名 | PixARMesh：自回归网格原生单视图场景重建 |
| 英文题名 | PixARMesh: Autoregressive Mesh-Native Single-View Scene Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05888) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PixARMesh |
| Dataset | 3D-FRONT |

> [!tip] 效果简介
> - 3D-FRONT 上，Scene-level CD (×10⁻³) 98.8 (EdgeRunner) / 98.4 (BPT) vs 153.2 (DepR) (-54.4 / -54.8)；Scene-level F-Score (%) 33.55 (EdgeRunner) / 32.26 (BPT) vs 25.00 (DepR) (+8.55 / +7.26)；Object-level CD (×10⁻³) 4.04 (EdgeRunner) / 4.57 (BPT) vs 2.57 (DepR) (+1.47 / +2.00)。

## 概述

单视图场景重建旨在从单张RGB图像中恢复完整的三维场景结构。现有方法主要依赖隐式符号距离函数（SDF）表示，通过等值面提取获得网格，再结合后处理布局优化完成场景组装。这一范式存在三个根本性瓶颈：（1）生成的网格面数多、几何平滑，缺乏艺术家可直接编辑的拓扑质量；（2）物体重建与布局组装分离进行，难以保证全局空间一致性；（3）SDF提取流程复杂，增加了系统复杂度。

**PixARMesh** 提出了一个网格原生的自回归场景重建框架，核心思想是将物体位姿估计与网格生成统一为单一的自回归序列预测任务。具体而言，系统将物体位姿编码为包围盒角点令牌，与网格量化令牌共享同一词表，由一个自回归Transformer解码器依次预测位姿序列和网格序列。为补偿单视图观测固有的遮挡和几何缺失，该方法增强了点云编码器，融入像素对齐的图像特征和场景级交叉注意力，使每个实例的潜在编码能感知全局空间关系。

在3D-FRONT数据集上，PixARMesh取得了场景级重建的最新水平：其EdgeRunner变体的场景Chamfer距离为98.8×10⁻³、F分数为33.55%，显著优于SDF类方法（如DepR的153.2和25.00%）。消融实验表明，联合位姿-网格建模相比两阶段分离设计将物体Chamfer距离从4.75降至4.04；像素对齐图像特征的移除导致场景和物体级性能大幅下降，验证了外观线索对补偿遮挡几何的关键作用。此外，使用真值深度可将物体级F分数从81.64%提升至86.66%，揭示深度估计精度是当前性能提升的主要瓶颈。

该方法的主要局限在于自回归解码导致推理时间较长（单场景4.5−6.7分钟），且性能受上游感知模型（深度估计、实例分割）误差的显著影响。当前仅重建前景物体，尚未涵盖墙壁、地板等背景结构。

## 背景与动机

单视图场景重建旨在从单一的二维图像中恢复出完整的三维场景几何，这一能力对增强现实、机器人导航和3D内容创作等应用至关重要。近年来，该领域涌现出多种方法，但普遍存在一个核心瓶颈：**现有方法主要依赖隐式符号距离函数（SDF）表示和后处理布局优化**，生成的网格面数多、几何平滑，缺乏可直接编辑的艺术家级网格质量；同时，分离的物体重建与布局组装流程难以保证全局空间一致性，且SDF提取需要复杂的等值面提取（如Marching Cubes），显著增加了流程复杂度。

具体而言，现有工作可大致分为两类路径。一类以 **InstPIFu**（Liu et al., ECCV 2022）和 **Uni-3D**（Zhang et al., ICCV 2023）为代表，采用体素SDF进行整体或组合式场景重建，但其输出为隐式场，需经过等值面提取才能获得显式网格，且网格面数通常远超艺术家级标准（可达数万甚至数十万面）。另一类如 **DepR**（Zhao et al., ICCV 2025）和 **DeepPriorAssembly**（Zhou et al., NeurIPS 2024），虽然引入了扩散模型或先验组装策略来提升重建质量，但本质上仍将物体重建与布局优化视为两个独立阶段——先估计物体位姿，再在规范空间生成几何，最后通过后处理优化将两者拼合。这种分离设计使得全局空间关系难以在生成过程中被充分建模，导致场景级一致性不足。

从3D表示的角度看，**隐式SDF与艺术家级网格之间存在根本性的鸿沟**：SDF天然适合连续表面的优化，但提取出的网格往往缺乏结构化的边和面拓扑，难以直接导入游戏引擎或建模软件进行后续编辑。近期，基于自回归Transformer的网格生成模型（如EdgeRunner、BPT）在物体级网格生成上取得了突破，能够直接输出紧凑、结构良好的艺术家级网格。然而，这些模型仅针对孤立物体设计，缺乏对场景上下文和物体间空间关系的感知能力，无法直接应用于场景级重建任务。

PixARMesh的动机正是弥合这一鸿沟：**将艺术家级网格生成的自回归范式扩展到场景级重建**。其核心洞察在于，物体位姿可以自然地编码为包围盒角点的序列令牌，与网格令牌共享同一词表，从而在一个统一的自回归Transformer解码器中完成位姿推理与几何生成的协同建模。同时，通过增强点云编码器——融入像素对齐的图像特征以补偿单视图观测的遮挡和缺失几何信息，并引入场景级交叉注意力以注入全局空间关系——使得模型能够在无后处理优化的情况下，从单张RGB图像直接生成全局一致的场景网格。

## 核心创新

PixARMesh的核心创新在于将**单视图场景重建从“隐式SDF提取+后优化组装”的分离范式，重构为统一的网格原生自回归序列预测**。其关键设计围绕三个相互关联的changed slots展开，形成一条从表示、感知到生成的因果链路。

### 1. 网格原生自回归表示：从SDF等值面到艺术家级网格令牌

现有方法（如**InstPIFu**，Liu et al., ECCV 2022；**Uni-3D**，Zhang et al., ICCV 2023）普遍采用隐式SDF作为3D表示，需通过Marching Cubes提取等值面，生成的网格面数多、几何平滑，缺乏可直接编辑的艺术家级拓扑。PixARMesh将3D表示从连续隐式场切换为**离散网格量化令牌**，直接复用对象级网格生成模型（EdgeRunner/BPT）的标记化方案，使场景重建的输出天然具备紧凑、可编辑的网格结构，无需后处理表面提取（Table A.1显示面数和顶点数显著低于SDF类方法）。

### 2. 位姿-网格联合令牌序列：从分离布局优化到统一自回归预测

传统组合式重建方法将物体位姿估计与几何生成分离，依赖后处理布局优化（如**Gen3DSR**的inpainting优化；**DeepPriorAssembly**，Zhou et al., NeurIPS 2024的零样本组装），难以保证全局空间一致性。PixARMesh将位姿编码为**包围盒8个角点的令牌序列**，与网格令牌共享同一词表，构建统一的令牌流：`<bos>, [pose_seq], <sep>, [mesh_seq], <eos>`。一个自回归Transformer解码器以联合交叉熵损失（Eq.5）同时学习布局推理与几何生成，使位姿预测和网格生成在序列层面相互约束。消融实验证实，联合建模相比两阶段分离设计将物体CD从4.75降至4.04，F-Score从80.85%提升至82.27%（Table 2）。

### 3. 像素对齐场景感知编码器：从孤立实例生成到全局上下文融合

对象级网格生成模型仅接受完整点云（x,y,z坐标），缺乏对部分观测和场景上下文的理解。PixARMesh对点云编码器进行了两处关键增强：

- **像素对齐图像特征融合**（Eq.2）：将DINOv2提取的图像特征按像素对齐方式拼接到每个点的几何特征上，通过Transformer融合块生成实例潜在编码，为部分观测点云提供外观线索以补偿遮挡几何。
- **场景上下文交叉注意力聚合**（Eq.3）：以实例潜在编码为查询、全局场景点云的潜在编码为键值进行交叉注意力，使每个实例的表示能感知全局空间关系。

消融实验显示，移除像素对齐图像特征导致场景F-Score从46.15%骤降至42.84%，物体F-Score从82.27%降至78.14%，是所有消融中下降最大的（Table 3），证明了外观线索对补偿单视图遮挡几何的关键作用。完整的“图像特征+场景上下文”组合在场景级F-Score上表现最优。

## 整体框架

PixARMesh 的整体设计围绕一个核心思想展开：将场景重建中的物体位姿估计与网格生成统一为单一的自回归序列预测任务。如图2所示，系统以单张RGB图像为输入，通过一组离线感知模型提取场景的几何与外观线索，随后在一个共享的自回归Transformer解码器中逐令牌生成每个实例的位姿和规范空间网格，最终组合为全局一致的场景。

### 管道模块与数据流

**二维感知前端** 负责从输入图像中提取三类信息：实例分割掩码（Grounded-SAM）、单目深度图（Depth Pro）以及像素级图像特征（DINOv2）。深度图经相机内参反投影为场景点云，并根据实例掩码裁剪出各物体的局部点云；图像特征则通过像素对齐的方式与点云几何坐标绑定，为后续编码器提供外观线索。

**像素对齐点云编码器** 是感知信息融合的关键环节。对于每个实例 $i$，编码器 $\mathcal{E}_{\mathrm{pc}}$ 将其局部点云中每个点 $p$ 的几何特征 $\mathbf{f}_p^{\mathrm{pc}}$ 与像素对齐的图像特征 $\mathbf{f}_p^{\mathrm{img}}$ 级联，通过Transformer融合块生成实例潜在编码 $\mathbf{z}_i$：

$$\mathbf{z}_i = \mathcal{E}_{\mathrm{pc}}\left(\mathbf{f}_p^{\mathrm{pc}}, \mathbf{f}_p^{\mathrm{img}}\right) \quad \forall p \in P_i$$

这一设计使模型能够从单视图的稀疏、遮挡观测中补偿缺失的几何信息——消融实验表明，移除像素对齐图像特征会导致场景级F-Score从46.15%骤降至42.84%，物体级F-Score从82.27%降至78.14%，是编码器设计中最关键的组件（Table 3）。

**场景上下文聚合** 将实例级编码提升到场景级感知。系统对全局场景点云进行归一化采样，通过同样的点云编码器获得场景潜在编码 $\mathbf{z}_{\mathrm{scene}}$，随后以实例编码为查询、场景编码为键值执行交叉注意力：

$$\mathbf{z}_i^{\mathrm{agg}} = \mathrm{CrossAttn}(q = \mathbf{z}_i, k = \mathbf{z}_{\mathrm{scene}}, v = \mathbf{z}_{\mathrm{scene}})$$

这一操作使每个实例的潜在表示能够感知全局空间关系——例如相邻物体的相对位置与尺度——从而在没有后处理布局优化的情况下生成空间一致的场景。消融实验证实，完整的“图像特征 + 场景上下文”组合在场景级F-Score上表现最优（Table 3）。

**自回归Transformer解码器** 将聚合后的潜在向量 $\mathbf{z}_i^{\mathrm{agg}}$ 作为条件，以统一的令牌序列预测物体的位姿与网格。序列结构为 `<bos>, [pose_seq], <sep>, [mesh_seq], <eos>`：位姿部分由包围盒8个角点的量化令牌组成，复用网格顶点标记化方案（BPT或EdgeRunner），使位姿预测与网格生成共享同一词表；网格部分则直接生成规范空间下的艺术家级网格令牌。位姿令牌解码后，通过最小二乘对齐从预测的全局坐标角点 $\mathbf{X}_{\mathrm{global}}$ 与规范空间角点 $\mathbf{X}_{\mathrm{local}}$ 之间恢复重力对齐的仿射变换 $\mathbf{T}^{\star}$：

$$\mathbf{T}^{\star} = \underset{\mathbf{T}}{\arg\min} \big\| \mathbf{X}_{\mathrm{global}} - [\mathbf{X}_{\mathrm{local}} \; \mathbf{1}] \mathbf{T}^{\top} \big\|_2^2$$

该变换将规范空间网格映射到场景坐标系，完成实例的放置。

### 训练目标

整个框架以标准的自回归交叉熵损失端到端训练：

$$\mathcal{L}_{\mathrm{ce}} = -\sum_{t=1}^{T} \log p_{\theta}(s_t \mid s_{<t}, \mathbf{z}_{\mathrm{agg}})$$

模型在给定过去令牌和聚合潜在变量的条件下，逐令牌预测整个位姿-网格序列。联合建模位姿与网格（而非两阶段分离设计）使物体级Chamfer距离从4.75降至4.04，F-Score从80.85%提升至82.27%（Table 2），验证了统一解码器学习布局推理与几何生成协同关系的有效性。

### 关键设计决策与局限

框架的模块化设计使其能够适配不同的网格生成基础模型（BPT或EdgeRunner），但推理速度受自回归解码制约——单场景重建需4.5–6.7分钟（A100 GPU）。此外，性能对上游感知模型的精度高度敏感：使用真值深度可将物体级F-Score从81.64%提升至86.66%（Table 4），而提供真值实例分割对场景级F-Score的提升最大（从33.55%升至46.15%，Table 5），表明深度估计和分割质量是当前系统的两大瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. Given an RGB image, we use pretrained models to extract the depth point cloud and image features for both the target object i and the global scene. These local and global cues are fed into the Pixel-Aligned PC-Encoder to produce the fused latent code, which is then aggregated into a single latent vector via cross-attention. This latent vector conditions the Transformer Decoder, which predicts the object’s pose followed by its mesh token sequence*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of PixARMesh with recent compositional scene reconstruction methods. PixARMesh predicts object poses and reconstructs native meshes in a single autoregressive decoding process, without relying on SDF-based surface extraction or layout optimization, producing compact and artist-ready mesh outputs*

## 核心模块与公式推导

PixARMesh 的核心架构围绕一个统一的**自回归 Transformer 解码器**展开，该解码器以序列化令牌（token）的形式同时预测物体位姿与规范空间网格，从而将场景重建转化为端到端的序列生成任务。整个流程由三个关键模块协同完成：像素对齐点云编码器、场景上下文聚合机制，以及位姿-网格联合序列建模。

### 3.1 联合预测框架

对于场景中的每个实例 `i`，模型 `F_AR` 从单视图观测中联合预测其场景级位姿 `T_i` 和规范空间网格 `O_i`：

$$( T _ { i } , O _ { i } ) = F _ { \mathrm { A R } } ( P _ { i } , M _ { i } , { \mathcal { F } } _ { \mathrm { i m g } } , P _ { \mathrm { s c e n e } } )$$

其中 `P_i` 为实例的深度点云，`M_i` 为实例掩码，`F_img` 为像素对齐的图像特征，`P_scene` 为全局场景点云。这一公式定义了 PixARMesh 的核心目标：**将位姿估计与几何生成统一在同一个自回归前馈架构中**，避免分离式流程中的误差累积。

### 3.2 像素对齐点云编码器

传统物体级网格生成模型仅以完整点云的 `(x, y, z)` 坐标作为输入。PixARMesh 对此进行了两项关键增强：

**（1）像素对齐图像特征融合**

对于实例点云中的每个点 `p`，其几何特征 `f_p^pc` 与对应像素位置的图像特征 `f_p^img`（由 DINOv2 提取）进行级联，并通过 Transformer 融合块得到实例潜在编码：

$$\mathbf { z } _ { i } = { \mathcal { E } } _ { \mathrm { p c } } \left( \mathbf { f } _ { p } ^ { \mathrm { p c } } , \mathbf { f } _ { p } ^ { \mathrm { i m g } } \right) \ \forall p \in P _ { i }$$

这一设计的因果逻辑在于：单视图观测存在严重的遮挡和缺失几何，**像素对齐的图像特征提供了外观线索**，帮助编码器推断被遮挡部分的形状信息。消融实验（Table 3）证实，移除图像特征导致物体级 F-Score 从 82.27% 骤降至 78.14%，是所有消融中下降幅度最大的。

**（2）场景上下文聚合**

实例潜在编码 `z_i` 通过交叉注意力层注入全局场景信息：

$$\mathbf { z } _ { i } ^ { \mathrm { a g g } } = \mathrm { C r o s s A t t n } ( q = \mathbf { z } _ { i } , k = \mathbf { z } _ { \mathrm { s c e n e } } , v = \mathbf { z } _ { \mathrm { s c e n e } } )$$

其中 `z_scene` 为归一化全局场景点云编码得到的场景潜在编码。以实例编码为查询（query）、场景编码为键值（key-value）的交叉注意力，使每个实例能够**感知全局空间关系**——例如邻近物体的相对位置和尺度——从而在无后处理布局优化的情况下直接生成全局一致的场景网格。

### 3.3 位姿-网格联合序列建模

PixARMesh 的核心创新在于将位姿预测与网格生成统一为**单一令牌序列**的自回归预测任务。

**位姿令牌化**：物体位姿被编码为包围盒的 8 个角点坐标，并复用网格顶点量化方案将其映射为令牌。这一设计使得位姿令牌与网格令牌**共享同一词表**，自回归解码器无需额外的模态分支。

**统一序列结构**：解码器按以下顺序生成令牌流：
```
<bos> → [pose_seq] → <sep> → [mesh_seq] → <eos>
```
模型首先自回归预测位姿令牌序列，随后预测网格令牌序列。位姿令牌为后续的网格生成提供了**空间先验**——解码器在生成网格时已“知道”该物体在场景中的位置和尺度。

**位姿恢复**：解码完成后，通过最小二乘法从预测的包围盒角点恢复重力对齐的仿射变换：

$$\mathbf { T } ^ { \star } = \underset { \mathbf { T } } { \arg \operatorname* { m i n } } \big \| \mathbf { X } _ { \mathrm { g l o b a l } } - [ \mathbf { X } _ { \mathrm { l o c a l } } \mathbf { 1 } ] \mathbf { T } ^ { \top } \big \| _ { 2 } ^ { 2 }$$

其中 `X_global` 为解码的全局坐标角点，`X_local` 为规范空间角点。该变换将规范空间网格映射到场景坐标系，完成实例的放置。

### 3.4 训练目标

整个模型以标准的自回归交叉熵损失进行端到端训练：

$$\mathcal { L } _ { \mathrm { c e } } = - \sum _ { t = 1 } ^ { T } \log p _ { \theta } ( s _ { t } \mid s _ { < t } , \mathbf { z } _ { \mathrm { a g g } } )$$

模型在给定过去令牌 `s_<t` 和聚合潜在编码 `z_agg` 的条件下，逐令牌预测整个序列。位姿令牌和网格令牌在训练中**联合优化**，迫使模型学习布局推理与几何生成之间的协同关系。消融实验（Table 2）表明，联合建模相比两阶段分离设计，将物体 Chamfer 距离从 4.75 降至 4.04，F-Score 从 80.85 提升至 82.27，验证了统一序列建模的有效性。

## 实验与分析

### 主实验结果

PixARMesh在3D-FRONT数据集上与多个SOTA方法进行了定量对比（Table 1）。在场景级指标上，PixARMesh-EdgeRunner变体取得了**98.8×10⁻³**的Chamfer距离（CD）和**33.55%**的F-Score，PixARMesh-BPT变体则为98.4×10⁻³和32.26%，均显著优于基于SDF的隐式重建方法DepR（153.2×10⁻³，25.00%）和基于先验组装的DeepPriorAssembly（128.7×10⁻³，25.83%）。这一优势的核心原因在于：自回归网格原生生成避免了SDF提取过程中的几何退化，同时联合位姿-网格建模消除了分离式布局优化的累积误差。

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/003_Table_1.jpg]]
*Table 1: Qualitative comparison with state-of-the-art methods on the 3D-FRONT [14] dataset. Following DepR [49] and DeepPriorAssembly [51], we report object- and scene-level Chamfer Distance (CD; lower is better) and F-Score (higher is better). We additionally include the single-direction Chamfer Distance (CD-S) to account for missing instances*

然而在物体级指标上，PixARMesh的表现弱于DepR：EdgeRunner变体的物体CD为**4.04×10⁻³**、F-Score为**82.27%**，而DepR达到2.57×10⁻³和89.66%。这一差距主要源于网格原生生成模型在单物体几何精度上尚不及成熟的SDF解码器，但PixARMesh在场景级一致性上的大幅领先弥补了这一不足——DepR虽然单个物体质量高，但分离式重建与后优化流程导致场景整体布局偏差较大。

定性对比（Figure 3）进一步印证了这一结论。PixARMesh生成的场景网格具有清晰的拓扑结构和可编辑的线框，而SDF类方法如InstPIFu和Uni-3D产生的网格面数多、几何平滑，缺乏艺术家级网格的锐利特征。在真实场景图像（Figure 4，来自Pix3D、Matterport3D、ScanNet）上的定性结果也展示了PixARMesh在域外数据上的泛化潜力，但论文未提供真实场景的定量指标，该结论需要进一步验证。

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparisons on the 3D-FRONT [14] dataset. For PixARMesh, we also show the mesh wireframe to highlight geometric quality*

### 消融实验

**联合位姿-网格建模的有效性**（Table 2）。将PixARMesh的联合自回归预测替换为两阶段设计（先预测布局，再以布局为条件生成网格），物体CD从**4.04升至4.75**，F-Score从**82.27降至80.85**。这表明位姿预测与网格生成之间存在强协同关系：统一的标记序列使解码器能够在生成几何时感知空间位置约束，而分离设计则切断了这一信息流。场景级指标同样下降（CD从98.8升至101.7，F-Score从33.55降至32.44），说明联合建模对全局布局一致性也有贡献。

**点云编码器设计的影响**（Table 3）。移除像素对齐图像特征（Img Feat）导致场景F-Score从**46.15降至42.84**，物体F-Score从**82.27降至78.14**，是所有消融中降幅最大的。这验证了核心设计动机：单视图观测导致的遮挡和缺失几何信息，必须通过像素对齐的外观线索来补偿。单独使用图像特征（无场景上下文聚合）可获得最高的物体级保真度（F-Score 83.38），但场景级F-Score（44.18）低于完整模型，说明场景上下文交叉注意力对全局空间关系建模不可或缺。值得注意的是，仅使用场景上下文聚合（无图像特征）的性能最低（场景F-Score 42.84），表明外观线索是基础，场景上下文是增强。

**深度与布局精度的影响**（Table 4）。使用真值深度替换Depth Pro估计的深度后，物体CD从**4.13降至3.04**，F-Score从**81.64%升至86.66%**；而提供真值布局的提升相对较小（CD降至3.40，F-Score升至83.88%）。这说明深度估计精度是当前性能的关键瓶颈——单目深度估计的误差直接导致输入点云的位置偏差，进而影响几何重建质量。这一发现为后续优化指明了方向：改进深度估计模型或引入多视图深度融合可能带来显著收益。

**上游感知误差的系统性影响**（Table 5）。逐一提供真值输入（深度、实例分割、布局）来隔离上游模型误差的影响。提供真值实例分割将场景F-Score从**33.55大幅提升至46.15**，表明Grounded-SAM的分割遗漏和误检是场景重建完整性的主要制约因素。当所有输入均为真值时，场景F-Score可达**63.91**，揭示了当前性能与理论上限之间的巨大差距——约30个百分点的提升空间来自上游感知模型的改进，而非核心重建算法的不足。

### 效率与网格质量

在推理效率方面（Table A.3），PixARMesh的自回归解码导致单场景重建需**4.5−6.7分钟**（A100 GPU），远慢于前馈方法如InstPIFu（约2秒）和潜在扩散方法如DepR（约30秒）。这是该方法在实际部署中的主要障碍。在网格紧凑性上（Table A.1），PixARMesh生成的面数和顶点数显著低于SDF类方法（通常低一个数量级），验证了艺术家级网格在存储和编辑效率上的优势。布局精度对比（Table A.2）显示PixARMesh的包围盒IoU和中心距离误差均优于分离式方法，进一步支持了联合建模对空间一致性的贡献。

### 失败模式分析

综合消融结果和论文披露的限制，PixARMesh的主要失败模式包括：（1）**遮挡严重或深度估计误差大的区域**，点云输入本身存在几何缺失，即使像素对齐特征也无法完全补偿，导致重建网格出现拓扑错误或缺失部件；（2）**实例分割遗漏**，被遗漏的物体完全不会出现在重建场景中，这是场景级F-Score对分割质量高度敏感的根本原因；（3）**极端拓扑结构**，基础网格生成模型（EdgeRunner/BPT）的固定分辨率量化可能在细长结构或复杂拓扑上产生退化；（4）**背景结构缺失**，PixARMesh仅重建前景物体，忽略墙壁、地板等平面背景，生成的场景在视觉上不完整。

### 补充图表

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/004_Table_2.jpg]]
*Table 2: Ablation study on joint pose-mesh modeling*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on our point-cloud encoder design. Img Feat, Ctx Agg denote pixel-aligned image features and scene context aggregation, respectively*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/008_Table_4.jpg]]
*Table 4: Effects of depth and layout in object-level metrics*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/006_Table_5.jpg]]
*Table 5: Effects of upstream (depth, segmentation, and layout) errors in scene-level metrics. Note that ground-truth layout implies ground-truth segmentation*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/011_Figure.jpg]]
*Figure: A.1. Additional qualitative results on real images from Pix3D, Matterport3D and ScanNet *

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/010_Table.jpg]]
*Table: A.2. Layout accuracy comparisons*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/012_Table.jpg]]
*Table: A.3. Inference runtime comparisons*

![[assets/figures/papers/paper_list_l2569_https_arxiv_org_abs_2603_05888/figures/009_Table.jpg]]

## 方法谱系与知识库定位

### 单视图场景重建的演化脉络

单视图场景重建（single-view scene reconstruction）的核心挑战在于从一张RGB图像中同时恢复多个物体的几何形状和三维布局。早期工作主要采用**组合式隐式重建**范式：先对每个实例独立重建符号距离函数（SDF），再通过后处理优化进行布局组装。代表性方法包括：

- **InstPIFu**（Liu et al., ECCV 2022）：基于SDF的组合式场景重建，对每个检测到的物体独立预测隐式表面，再通过布局优化组合成场景。
- **Uni-3D**（Zhang et al., ICCV 2023）：整体式场景重建，使用体积SDF一次性预测整个场景的隐式场。
- **Gen3DSR**：结合inpainting和优化的组合式场景重建方法。
- **DeepPriorAssembly**（Zhou et al., NeurIPS 2024）：零样本场景重建，通过先验组装实现无需训练的布局推理。
- **DepR**（Zhao et al., ICCV 2025）：深度引导的扩散模型场景重建，在Table 1中作为SDF类方法的代表，场景Chamfer距离为153.2×10⁻³，F分数为25.00%。

这些方法的共同瓶颈在于：**生成的网格面数多、几何平滑，缺乏可直接编辑的艺术家级网格**；同时，分离的物体重建与布局组装流程难以保证全局空间一致性，且SDF提取需要复杂的等值面提取（Marching Cubes），增加了流程复杂度。

### PixARMesh的方法定位

PixARMesh在方法谱系中占据一个独特位置：**将艺术家级网格生成的自回归范式扩展到场景级重建**。其核心创新在于将物体位姿估计与网格生成统一为自回归序列预测，从而在一个统一的Transformer解码器中完成布局推理与几何生成的协同建模。

具体而言，PixARMesh在以下几个维度上实现了方法跃迁：

1. **表示层面**：从隐式SDF/等值面提取转向**网格原生（mesh-native）自回归生成**。网格被量化为离散令牌序列，可直接解码为紧凑的、艺术家级的三角网格，无需后处理表面提取。

2. **编码器设计**：将传统仅使用完整点云坐标（x,y,z）的编码器，增强为**像素对齐的点云编码器**。该编码器将深度点云的几何特征与DINOv2提取的图像特征进行级联，并通过Transformer融合块生成实例潜在编码。这一设计使模型能从部分观测的点云中补偿遮挡和缺失的几何信息。

3. **场景上下文整合**：引入**跨实例的交叉注意力机制**，以实例潜在编码为查询、全局场景潜在编码为键值，将全局空间关系注入每个实例的特征表示。这使得模型在生成单个物体时能感知其他物体的位置和尺度，从而在无后处理优化的情况下直接生成全局一致的场景网格。

4. **位姿估计范式**：将传统的后处理优化（如点云匹配、布局优化）替换为**自回归包围盒角点预测**。物体位姿被编码为8个包围盒角点的令牌序列，与网格令牌共享同一词表，通过最小二乘法恢复重力对齐的仿射变换。这一设计使位姿预测与网格生成共享学习信号，实现了联合优化。

5. **生成序列结构**：采用统一的令牌流 `<bos>, [pose_seq], <sep>, [mesh_seq], <eos>`，位姿和网格令牌通过下一个令牌预测的交叉熵损失联合训练。

### 与同期工作的关系

PixARMesh与以下工作存在方法层面的关联与区分：

- **MIDI**（Huang et al., CVPR 2025）：多实例扩散模型用于场景生成。两者都处理多物体场景，但MIDI使用扩散范式，PixARMesh使用自回归范式；MIDI面向生成，PixARMesh面向重建。
- **EdgeRunner-FT**：微调的EdgeRunner配合后处理布局优化。这实际上是PixARMesh的两阶段分离基线（Table 2中的Two-stage），其物体CD为4.75，F-Score为80.85%，而PixARMesh的联合建模将CD降至4.04，F-Score提升至82.27%，验证了统一建模的增益。
- **DepR**：深度引导的扩散场景重建。在Table 1中，DepR在物体级指标上表现更好（CD 2.57, F-Score 89.66%），但场景级指标显著落后于PixARMesh（CD 153.2 vs 98.8, F-Score 25.00% vs 33.55%），说明SDF类方法在全局布局一致性上存在固有劣势。

### 适用边界与约束条件

PixARMesh的适用边界受以下因素制约：

1. **输入模态依赖**：方法假设输入为单张RGB图像，并依赖离线感知模型（Grounded-SAM用于实例分割、Depth Pro用于单目深度估计、DINOv2用于图像特征提取）。这些上游模型的误差会级联影响最终重建质量。Table 5的消融实验表明，提供真值实例分割可使场景F-Score从33.55%提升至46.15%，而所有输入均为真值时场景F-Score可达63.91%，揭示了上游误差的显著影响。

2. **场景范围限制**：PixARMesh仅重建前景物体，忽略墙壁、地板等平面背景结构，生成的场景不完整。这是当前设计的明确边界。

3. **训练数据分布**：模型在合成数据集3D-FRONT上训练，对真实场景的泛化能力有待进一步验证。Figure 4展示了在Pix3D、Matterport3D和ScanNet等真实数据集上的定性结果，但缺乏大规模定量评估。

4. **网格质量上限**：生成网格的质量受限于基础模型（EdgeRunner/BPT）的压缩率与细节保真度权衡。Table A.1的面数和顶点数对比显示，PixARMesh生成的网格比SDF方法更紧凑，但在极端拓扑结构上可能产生退化。

5. **推理速度**：自回归解码导致单场景重建需4.5−6.7分钟（A100 GPU），远慢于前馈和潜在扩散方法（Table A.3），限制了实时或交互式应用场景。

### 局限与开放问题

**已识别的局限**：

- **推理效率瓶颈**：自回归逐令牌解码的固有延迟是当前方法的最大实用障碍。可能的缓解方向包括投机解码（speculative decoding）或非自回归生成。
- **上游感知耦合**：深度估计和实例分割的精度对最终重建质量影响显著（Table 4中真值深度可将物体F-Score从81.64%提升至86.66%）。如何使重建模型对上游误差更具鲁棒性，或设计端到端的联合优化，是重要的改进方向。
- **场景完整性不足**：缺乏对背景结构（墙壁、地板）的建模能力，限制了在室内场景理解、导航规划等下游任务中的应用。
- **网格分辨率固定**：使用固定的网格量化分辨率，可能不适合需要多尺度输出的应用场景。

**开放问题**：

1. 如何将PixARMesh扩展到包含墙壁、地板等背景结构的完整场景重建？这可能需要引入平面基元或房间布局先验。
2. 自回归解码的推理速度如何进一步优化？投机解码、KV缓存、或与非自回归生成的混合策略值得探索。
3. 在动态场景或多视图融合场景中，如何利用时序或视角信息提升重建一致性？像素对齐特征和场景上下文机制可能自然扩展到多视图输入。
4. 能否将像素对齐特征和场景上下文机制推广到其他类别的物体生成模型（如基于扩散的模型）？这可能是提升扩散模型场景一致性的有效途径。
5. 在更大规模、更多样化的真实数据集上训练能否进一步提升泛化能力？目前缺乏类似3D-FRONT规模的真实场景网格数据集。
6. 如何评估和提升生成网格的语义合理性及可编辑性，以满足下游应用（如AR/VR、机器人仿真）需求？这需要超越Chamfer距离和F分数的评价体系。
7. 基础网格生成模型的进步（如更高压缩率或更精细的表示）如何直接惠及PixARMesh？PixARMesh的模块化设计使其可以相对容易地替换底层网格生成器，但不同标记化策略对场景级一致性的影响尚不明确。

## 原文 PDF

![[paperPDFs/CVPR_2026/PixARMesh_Autoregressive_Mesh_Native_Single_View_Scene_Reconstruction.pdf]]