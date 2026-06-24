---
title: "BEVNeXt: Reviving Dense BEV Frameworks for 3D Object Detection"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/BEVNeXt_Reviving_Dense_BEV_Frameworks_for_3D_Object_Detection.pdf
aliases:
- BEVNeXt
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过引入 CRF 调制增强深度一致性、Res2Fusion 扩大时序感受野并跳过自车运动变换，以及两阶段透视精炼补偿特征畸变，系统性地重振密集 BEV 框架性能。"
primary_logic: "密集 BEV 表达天然擅长深度估计与目标定位，结合现代化的 2D 建模增强、多尺度时序融合和实例级特征精炼，可使密集框架在 3D 检测中全面超越稀疏方法，同时保留定位鲁棒性。"
claims:
- "CRF调制在点云稀疏监督下大幅提升深度一致性，带来+1.9% NDS增益。"
- "Res2Fusion以窗口大小3且移除自车运动变换取得最佳融合，NDS提升1.0%并避免动态对象错位。"
- "BEVNeXt在 nuScenes 测试集达到 64.2 NDS，超越先前最佳密集方法 SOLOFusion 2.3%，验证框架整体优势。"
- "引入透视精炼与深度嵌入，定位误差 mATE 在所有方法中最低，表明框架定位鲁棒性。"
---

# BEVNeXt: Reviving Dense BEV Frameworks for 3D Object Detection

> [!tip] 核心洞察
> 密集 BEV 表达天然擅长深度估计与目标定位，结合现代化的 2D 建模增强、多尺度时序融合和实例级特征精炼，可使密集框架在 3D 检测中全面超越稀疏方法，同时保留定位鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BEVNeXt：复兴密集 BEV 框架用于 3D 目标检测 |
| 英文题名 | BEVNeXt: Reviving Dense BEV Frameworks for 3D Object Detection |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.01696); [GitHub](https://github.com/woxihuanjiangguo/BEVNeXt) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | BEVNeXt |
| Dataset |  |

## 概述

3D 目标检测是自动驾驶感知的核心任务。近年来，基于鸟瞰图（BEV）的检测框架分为两大阵营：密集 BEV 方法和稀疏查询式方法。密集 BEV 方法通过将多视图图像特征显式投影到统一的 BEV 空间进行检测，天然擅长深度估计与目标定位；然而，受限于深度估计精度不足、时序融合感受野受限以及特征投影畸变等问题，密集框架的性能逐渐落后于以 **StreamPETR**（Wang et al., ICCV 2023）和 **SparseBEV**（Liu et al., ICCV 2023）为代表的稀疏查询式方法。

本文提出 **BEVNeXt**，旨在通过系统性改进重振密集 BEV 框架的竞争力。其核心洞察在于：密集 BEV 表达在深度估计和定位鲁棒性上具有先天优势，结合现代化的 2D 建模增强、多尺度时序融合和实例级特征精炼，完全可以全面超越稀疏方法。

BEVNeXt 围绕三个关键瓶颈展开设计：

- **CRF 调制深度估计**：引入条件随机场（CRF）对深度网络输出施加颜色平滑先验，在更大特征图（$F_{1/8}$）上增强对象级深度一致性，缓解点云稀疏监督下的深度退化问题。
- **Res2Fusion 时序融合**：借鉴 Res2Net 的多尺度卷积分组思想，扩大时序 BEV 特征融合的感受野，并因此得以跳过自车运动变换，避免动态对象因运动补偿产生的错位。
- **两阶段透视精炼解码器**：在 CenterPoint 检测头产生粗热图后，利用透视可变形注意力与 CRF 增强的深度嵌入对 ROI 特征进行实例级精炼，补偿 BEV 投影过程中的特征畸变。

实验表明，BEVNeXt 在 nuScenes 测试集上达到 **64.2 NDS**，超越先前最优密集方法 **SOLOFusion**（Park et al., ICLR 2022）**2.3%**，同时在定位误差 mATE 上取得所有方法中的最低值，验证了密集框架在定位鲁棒性上的独特优势。消融研究进一步证实：CRF 调制在稀疏监督下带来 +1.9% NDS 增益，Res2Fusion 以窗口大小 3 且移除自车运动变换时取得最佳融合效果（+1.0% NDS），各组件协同贡献于整体性能提升。

## 背景与动机

3D 目标检测是自动驾驶感知系统的核心任务，其目标是从多视角相机输入中恢复三维空间中的物体位置、尺寸与朝向。近年来，基于鸟瞰图（Bird's-Eye-View, BEV）的检测范式逐渐成为主流，其核心思路是将多视图 2D 特征通过深度估计投影至统一的 BEV 空间，再在 BEV 平面上进行检测。这一范式可大致分为两条技术路线：**密集 BEV 框架**与**稀疏查询式框架**。

密集 BEV 框架（如 **BEVDepth**, Li et al., AAAI 2023；**BEVPoolv2**）直接构建完整的 BEV 特征图，并在其上应用密集检测头（如 CenterPoint）进行预测。该类方法天然擅长深度估计与目标定位，能够充分利用 BEV 空间的几何一致性。然而，近期稀疏查询式方法（如 **StreamPETR**, Wang et al., ICCV 2023；**SparseBEV**, Liu et al., ICCV 2023）凭借基于 Transformer 的稀疏查询机制，在检测精度上迅速超越密集方法，使密集框架一度被视为性能落后的技术路线。

### 密集 BEV 框架的三大瓶颈

BEVNeXt 通过系统性分析，将密集 BEV 检测器性能受限的核心原因归结为以下三个相互关联的瓶颈：

**1. 深度估计精度不足。** 密集 BEV 框架依赖逐像素深度分布将 2D 特征提升至 3D 空间。标准深度网络通常在 1/16 分辨率特征图上训练，缺乏对物体边界深度一致性的显式约束，导致深度估计在物体边缘模糊、前后景混淆，进而引发 BEV 特征投影畸变。当仅依赖稀疏点云监督（如 LiDAR 点云）时，这一问题尤为严重。

**2. 时序融合感受野受限。** 现有密集时序融合方法（如 **SOLOFusion**, Park et al., ICLR 2022）采用并行拼接历史 BEV 特征，并通过自车运动变换对齐不同时刻的 BEV 格。这种方式存在两个缺陷：一是融合感受野局限于相邻帧，难以捕捉长时序依赖；二是自车运动变换假设场景静止，对动态物体（如移动车辆、行人）引入特征错位，反而损害检测精度。

**3. 特征投影畸变与实例级特征粗糙。** 从 2D 图像到 BEV 的投影过程不可避免引入几何畸变，而传统密集检测头（如 CenterPoint）仅在 BEV 平面上进行粗粒度回归，缺乏对目标实例的精细特征补偿。稀疏查询式方法通过可变形注意力在透视特征上精炼查询，有效缓解了这一问题，密集框架却长期缺乏类似的实例级精炼机制。

### 本文动机

上述瓶颈表明，密集 BEV 框架的性能落后并非范式本身的根本缺陷，而是缺乏与稀疏方法相匹配的现代化建模增强。BEVNeXt 的核心动机在于：**通过系统性地补强深度估计、时序融合和实例级特征精炼三个关键环节，重振密集 BEV 框架的竞争力，使其在保留定位鲁棒性优势的同时，全面超越稀疏查询式方法。**

具体而言，BEVNeXt 引入三项针对性设计：**CRF 调制深度估计**利用条件随机场融入颜色平滑先验，增强物体级深度一致性；**Res2Fusion 时序融合**借鉴 Res2Net 的多尺度分组卷积思想扩大时序感受野，并跳过自车运动变换以规避动态物体错位；**两阶段目标解码器**结合透视可变形注意力与 CRF 深度嵌入，对 CenterPoint 产生的粗检测进行实例级精炼。这三项设计协同作用，使密集 BEV 框架在 nuScenes 基准上达到 64.2 NDS 的最新水平，验证了密集范式的复兴潜力。

## 核心创新

BEVNeXt 的核心创新在于系统性地解决了密集 BEV 检测器中三个长期被忽视的结构性缺陷：**深度估计精度不足**、**时序融合感受野受限**以及**特征投影畸变**。通过三个相互协同的模块化改进，该方法在不牺牲密集框架定位鲁棒性的前提下，全面超越稀疏查询式方法。

### 关键改进槽位

#### 1. CRF 调制的深度估计（深度估计模块）

**基线缺陷**：标准深度网络在 $F_{1/16}$ 特征图上训练，缺乏对像素级深度一致性的显式约束，在点云稀疏监督下尤为脆弱。

**改进方案**：将深度网络迁移至分辨率更高的 $F_{1/8}$ 特征图，并引入 CRF 调制，通过颜色平滑先验对深度分布施加对象级一致性约束。CRF 能量函数包含一元势（深度网络输出）和成对势（基于颜色相似度与深度 bin 距离），在不增加额外监督信号的前提下显著提升深度质量。

**证据强度**：消融实验表明，当 LiDAR 点云覆盖稀疏（约 50%）时，CRF 调制带来 **+1.9% NDS** 增益；在密集监督下增益较小（+0.2% NDS），证实其在稀疏监督场景下的关键作用。该优势随输入分辨率提升而进一步放大。

#### 2. Res2Fusion 时序融合（时序融合模块）

**基线缺陷**：并行拼接历史 BEV 特征并辅以自车运动变换（如 SOLOFusion），感受野受限于单帧窗口，且强制对齐操作导致动态对象错位。

**改进方案**：Res2Fusion 借鉴 Res2Net 的多尺度卷积分组思想，将历史 BEV 特征按时间窗口分组，通过层级式 $3\times3$ 卷积逐步扩大感受野。更大的感受野使得跳过自车运动变换成为可能，从根本上规避动态物体错位问题。具体操作流程为：
- 将历史帧按窗口大小 $w$ 分组，经 $1\times1$ 卷积降维；
- 组间通过递进式 $3\times3$ 卷积融合：$B_i'' = K_i^{3\times3}(B_i' + B_{i+1}'')$；
- 最终通过 $1\times1$ 卷积聚合多尺度特征。

**证据强度**：窗口大小 $w=3$ 取得最佳平衡，NDS 提升 **+1.0%**。强制引入自车运动变换反而导致性能下降，验证了跳过该操作的必要性。

#### 3. 两阶段目标解码器（检测头）

**基线缺陷**：仅使用 CenterPoint 检测头从 BEV 特征直接回归目标属性，缺乏对实例级特征的精细化利用。

**改进方案**：设计两阶段目标解码器，第一阶段由 CenterPoint 产生热图与粗预测，第二阶段通过透视可变形注意力对 ROI 特征进行精炼。该过程融合 CRF 调制的深度嵌入，使注意力机制能够感知 2D 空间中的对象级深度一致性，从而更准确地采样判别性特征。与先前方法不同，反向投影仅作用于目标级 BEV 特征而非全局 BEV 表达。

**证据强度**：消融实验中，CRF 深度嵌入为透视精炼带来 **+0.8% NDS** 增益。可视化结果表明，精炼后的检测框与真值框的对齐程度显著优于粗预测，使得 BEVNeXt 在所有方法中取得最低的 mATE 定位误差。

### 模块间协同机制

三个改进并非孤立生效，而是形成递进式增强链路：CRF 调制提供更可靠的深度基础，使 Res2Fusion 在大感受野下仍能保持时序一致性；精确的深度嵌入进一步赋能透视精炼，在实例级别补偿 BEV 投影畸变。这种从深度估计到时序融合再到目标精炼的全链路优化，是 BEVNeXt 以密集框架超越稀疏查询范式的核心原因。

## 整体框架

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/002_Figure_2.jpg]]
*Figure 2: Overall Architecture of BEVNeXt. The backbone first extracts multi-view image features, which are converted into depth distributions with a depth network and CRF modulation. The BEV feature at the current frame is fused with previous ones through a Res2Fusion module. Finally, a CenterPoint detection head, coupled with perspective refinement, generates object heatmaps and attributes*

BEVNeXt 的整体架构遵循“图像特征提取 → BEV 生成 → BEV 编码 → 检测头”的四阶段流水线，如图 2 所示。其设计目标是通过三个关键模块的协同改进，系统性地解决密集 BEV 检测器在深度估计精度、时序融合感受野和特征投影畸变上的瓶颈。

**图像骨干网络**首先从多视图图像中提取多尺度特征（F₁/₄ 至 F₁/₃₂），为后续深度估计和 BEV 投影提供丰富的语义表示。

**BEV 生成阶段**由深度网络与 CRF 调制深度估计模块构成。深度网络在更大的特征图 F₁/₈ 上运行（而非传统的 F₁/₁₆），并引入条件随机场（CRF）调制，利用颜色平滑先验增强深度估计的对象级一致性。CRF 能量函数由一元项和成对项组成：

$$E(\pmb{d}|\pmb{I}) = \sum_i \psi_u(x_i) + \sum_{i \neq j} \psi_p(x_i, x_j)$$

其中成对势鼓励颜色相似区域具有一致的深度赋值：

$$\psi_p(x_i, x_j) = \sum_w w \exp(-\frac{|\bar{\mathcal{I}}_i - \bar{\mathcal{I}}_j|^2}{2\theta^2}) |x_i - x_j|$$

调制后的深度概率与图像特征结合，通过视锥投影生成当前帧的 BEV 特征。

**BEV 编码阶段**采用 Res2Fusion 时序融合模块。与传统的并行拼接或循环融合不同，Res2Fusion 受 Res2Net 架构启发，通过多尺度分组卷积扩大时序感受野。具体而言，历史 BEV 特征按窗口大小 w 分组后进行通道压缩：

$$B_i' = K_i^{1\times1}([B_{t-(i+1)\times w}; ...; B_{t-i\times w}]) \quad (i=0,...,g)$$

随后通过层级式 3×3 卷积逐步聚合多尺度特征：

$$B_i'' = \begin{cases} K_i^{3\times3}(B_i') & \mathrm{if~} i=g; \\ K_i^{3\times3}(B_i' + B_{i+1}') & \mathrm{if~} 0<i<g; \\ B_i' & \mathrm{if~} i=0. \end{cases}$$

最终通过 1×1 卷积融合所有尺度输出：

$$\tilde{B} = K_{final}^{1\times1}([B_g''; ...; B_0''])$$

增大的感受野使得 Res2Fusion 可以跳过自车运动变换，从而避免动态对象的运动错位问题。

**检测头阶段**采用两阶段目标解码器。第一阶段使用 CenterPoint 从 BEV 特征生成热图并提取初始目标查询；第二阶段通过透视可变形注意力，结合 CRF 调制的深度嵌入，对 ROI 特征进行实例级精炼。与以往对整个 BEV 表示进行反向投影的方法不同，BEVNeXt 仅对目标级 BEV 特征进行透视精炼，大幅降低了计算开销，同时利用深度嵌入引导注意力聚焦于判别性 2D 特征。

整个流水线中，三个改进模块形成因果闭环：CRF 调制提供更准确的深度估计，为 Res2Fusion 提供更可靠的 BEV 特征基础；Res2Fusion 通过扩大时序感受野增强特征表达能力；两阶段解码器则利用透视精炼补偿 BEV 投影中的特征畸变，进一步提升定位精度。

## 核心模块与公式推导

BEVNeXt 围绕密集 BEV 框架的三个瓶颈进行系统性重构，核心模块包括：CRF 调制深度估计、Res2Fusion 时序融合，以及两阶段目标解码器。

### CRF 调制深度估计

传统深度网络在稀疏点云监督下难以保持对象级深度一致性。BEVNeXt 引入条件随机场（CRF）调制，将颜色平滑先验融入深度概率分布，在不引入额外监督信号的前提下增强像素级深度一致性。

CRF 能量函数定义为：

$$E(\pmb{d}|\pmb{I}) = \sum_i \psi_u(x_i) + \sum_{i \neq j} \psi_p(x_i, x_j)$$

其中 $\pmb{d}$ 为深度赋值，$\pmb{I}$ 为输入图像。一元势 $\psi_u(x_i)$ 来自深度网络输出的初始深度分布，二元势 $\psi_p(x_i, x_j)$ 则基于颜色相似性约束相邻像素的深度一致性：

$$\psi_p(x_i, x_j) = \sum_w w \exp(-\frac{|\bar{\mathcal{I}}_i - \bar{\mathcal{I}}_j|^2}{2\theta^2}) |x_i - x_j|$$

$\bar{\mathcal{I}}_i$ 表示像素 $i$ 的颜色特征，$|x_i - x_j|$ 为深度 bin 之间的距离。该设计使得颜色相近的像素倾向于具有一致的深度赋值，从而在对象边界处形成更清晰的深度区分。

此外，深度网络被提升到更大的特征图 $F_{1/8}^i$ 上运行（而非通常的 $F_{1/16}^i$），同时将通道数减半。这一设计在更高分辨率下放大了 CRF 调制的效果——如表 4 所示，当输入分辨率提升时 CRF 调制的增益愈发显著。

### Res2Fusion 时序融合

密集 BEV 方法的时序融合通常受限于有限的感受野，且需要自车运动变换来对齐历史帧，这会导致动态对象的错位。Res2Fusion 借鉴 Res2Net 的多尺度分组卷积思想，在时序维度上扩大感受野。

给定 $g$ 组历史 BEV 特征，每组包含窗口大小 $w$ 的连续帧，首先通过 $1\times1$ 卷积降维：

$$B_i' = K_i^{1\times1}([B_{t-(i+1)\times w}; ...; B_{t-i\times w}]) \quad (i=0,...,g)$$

随后进行多尺度层级聚合，每一组在自身卷积后与更高层级的特征相加，逐步扩大感受野：

$$B_i'' = \begin{cases} K_i^{3\times3}(B_i') & \mathrm{if~} i=g; \\ K_i^{3\times3}(B_i' + B_{i+1}') & \mathrm{if~} 0<i<g; \\ B_i' & \mathrm{if~} i=0. \end{cases}$$

最终通过 $1\times1$ 卷积融合所有尺度的输出：

$$\tilde{B} = K_{final}^{1\times1}([B_g''; ...; B_0''])$$

该设计的核心优势在于：扩大的感受野使得模型可以直接跳过自车运动变换，避免强制 warp 历史 BEV 特征带来的动态对象错位。消融实验（Table 6）表明，窗口大小 $w=3$ 在短期局部性与长期感受野之间取得最优平衡，带来 1.0% NDS 提升；而加入自车运动变换反而导致性能下降。

### 两阶段目标解码器

检测头采用两阶段设计：第一阶段由 CenterPoint 头在 BEV 特征上产生热图与粗预测；第二阶段通过透视可变形注意力对 ROI 特征进行精炼。该过程的关键在于将 CRF 调制的深度嵌入引入反向投影，使模型在透视视图中能够利用对象级深度一致性聚焦于判别性特征，从而补偿 BEV 投影过程中的特征畸变。这一设计使 BEVNeXt 在所有对比方法中取得了最低的 mATE 定位误差。

## 实验与分析

### 整体性能对比

BEVNeXt 在 nuScenes 3D 目标检测基准上全面刷新了密集 BEV 框架的性能上限。在验证集上，以 ResNet-50 为骨干、输入分辨率 256×704 的 BEVNeXt 达到 **54.8% NDS** 和 **43.7% mAP**；引入透视预训练的 BEVNeXt* 进一步提升至 **56.0% NDS** 和 **45.6% mAP**，相比先前最优密集方法 SOLOFusion 分别高出 **2.6% NDS** 和 **2.9% mAP**（Table 1）。在测试集上，搭载 V2-99 骨干的 BEVNeXt 取得 **64.2% NDS** 和 **55.7% mAP**，超越 SOLOFusion **2.3% NDS**，并达到与当时最先进稀疏方法 StreamPETR 和 SparseBEV 相当甚至更优的水平（Table 2）。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/005_Table_1.jpg]]
*Table 1: Comparison on the nuScenes val set. ViT-L [10] is pretrained on COCO [33] and Objects365 [52], while ViT-Adapter-L [8] is pretrained on DINOv2 [47]. * The backbone benefits from perspective pretraining [61]*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/006_Table_2.jpg]]
*Table 2: Comparison on the nuScenes test set. ConvNeXt-B [42] is pretrained on ImageNet-22K [9], while V2-99 is initialized from a DD3D [48] backbone. The listed methods do not use future frames during training or testing. Table 3. 3D multi-object tracking on the nuScenes test set. Ours uses V2-99 as the backbone while the others use ConvNeXt-B*

值得注意的是，BEVNeXt 的定位误差 **mATE 在所有对比方法中最低**（Figure 1），验证了密集 BEV 表达在目标定位上的天然优势。此外，在 3D 多目标跟踪任务上，BEVNeXt 同样展现出强竞争力（Table 3），表明其检测特征对时序关联任务具有良好的泛化性。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/001_Figure_1.jpg]]
*Figure 1: Previous SOTAs vs. BEVNeXt on the nuScenes 3D Object Detection Benchmark. On the nuScenes val split and test split, we compare BEVNeXt with previous SOTAs using (ResNet-50, bottom in the left panel), (ResNet-101, top in the left panel), and (VoVNet-99, right panel) as the backbone. BEVNeXt outperforms all previous sparse query-based ones in terms of comprehensive performance, meanwhile generating much fewer localization errors. The diameter of each bubble represents the mean Average Translation Error (mATE) each model produces. Higher and smaller bubbles are better. Best viewed in color*

### 消融实验与因果分析

#### 各组件贡献

以 BEVPoolv2 为基线（输入 256×704，ResNet-50，8 帧历史），逐步叠加 BEVNeXt 三大组件（Table 5）：


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/009_Table_5.jpg]]
*Table 5: Ablation of BEVNeXt Components. The baseline is BEVPoolv2 with an input resolution of 2 5 6 $\times$ 7 0 4 , ResNet50 as the backbone, and a long-term history of 8 frames*

- 基线 NDS 为 46.9%。引入 **CRF 调制深度估计**后，NDS 提升至 50.8%（+3.9%），证明深度一致性的改善是性能跃升的首要驱动力。
- 进一步加入 **Res2Fusion 时序融合**，NDS 达到 53.9%（+3.1%），表明扩大的时序感受野有效增强了运动场景下的特征聚合。
- 最后叠加 **两阶段目标解码器**（含透视精炼与 CRF 深度嵌入），NDS 达到最终 54.8%（+0.9%），在实例级别补偿了特征投影畸变。

#### CRF 调制的关键机制

CRF 调制的核心价值在于**稀疏监督条件下的深度一致性增强**（Table 4）。当 LiDAR 点云覆盖密集时，CRF 调制仅带来 +0.2% NDS 的边际增益；但当点云覆盖率降至约 50% 的稀疏监督场景时，增益急剧扩大至 **+1.9% NDS**。这揭示了一个因果链条：CRF 的颜色平滑先验在深度标签稀疏区域充当了有效的正则化器，约束相邻像素的深度分配趋于一致，从而产生对象级的连续深度估计（Figure 4 可视化了这一效果）。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/013_Figure_4.jpg]]
*Figure 4: Comparison of Depth Estimation with and without CRF modulation on the nuScenes val split. We visualize depth ranges using an argmax operation on various depth bins. The CRFmodulated depth probabilities can distinguish objects from the background better*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/007_Table_4.jpg]]
*Table 4: Ablation of CRF modulation with different backbones and input resolutions. All depth networks operate on F _ { 1 / 1 6 } . Only 1 history frame is used. The effect of CRF modulation is minor given dense point clouds supervision*

此外，CRF 调制的优势随输入分辨率增大而愈发显著（Table 4），说明高分辨率下更精细的颜色信息能更好地引导深度概率的优化。

#### Res2Fusion 的设计权衡

Res2Fusion 的核心设计选择体现在窗口大小与自车运动变换两个维度（Table 6）：


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/008_Table_6.jpg]]
*Table 6: Ablation of Res2Fusion. We compare different window sizes w and the effect of ego-motion transformation over 8 historical frames (9 frames in total). Zero padding is used if the number of frames cannot be divided evenly by w*

- **窗口大小**：窗口大小 3 取得最优 NDS（53.9%），相比窗口大小 1（等效于并行融合）提升 **+1.0% NDS**。窗口过小则感受野受限，无法充分捕获长时序依赖；窗口过大则组内帧数过多，短时局部细节被稀释。
- **自车运动变换**：在 Res2Fusion 中跳过自车运动变换反而带来性能提升，而强制执行变换会导致 NDS 下降。原因是强制 warp 历史 BEV 特征到当前坐标系时，动态物体（如行驶中的车辆）会产生位置错位——静态背景被正确对齐，但运动目标被错误地“拖拽”到错误位置，破坏了特征一致性。

#### 透视精炼中深度嵌入的作用

在目标解码器的透视精炼阶段，CRF 调制深度嵌入贡献了 **+0.8% NDS**（Table 7）。其机制在于：深度嵌入为可变形注意力提供了对象级的 2D 空间一致性先验，使采样点更准确地落在目标表面而非背景区域，从而提升了 ROI 特征的判别力。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/010_Table_7.jpg]]
*Table 7: Ablation of Depth Embedding in Perspective Refinement. All depth networks operate on $F _ { 1 / 8 }$ . , as the input resolution is 2 5 6 $\times$ 7 0 4 . . Only 1 history frame is used*

### 推理效率

以 ResNet-101 为骨干的 BEVNeXt 达到 **4.4 FPS**，虽慢于 StreamPETR（6.4 FPS），但显著快于同为密集框架的 SOLOFusion（1.5 FPS）（Table 8）。Res2Fusion 模块仅需 6.9M 参数和 31.4 GFLOPs，在效率与性能间取得了良好平衡。


![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/011_Table_8.jpg]]
*Table 8: Analysis of Runtime Efficiency. The listed methods use ResNet101 as the image backbone. Both SOLOFusion-R101 and BEVNeXt-R101 utilize a BEV resolution of 256 × 256*

### 失败模式与局限

论文未系统报告失败案例，但从方法机理可推演以下潜在脆弱点：
- **极端稀疏场景**：CRF 调制依赖颜色平滑先验，在低纹理或均匀颜色区域（如白墙、黑夜）可能失效，深度估计退化为纯网络预测。
- **高速动态物体**：Res2Fusion 跳过自车运动变换虽避免了 warp 错位，但完全依赖网络隐式学习运动补偿，对高速运动物体的跨帧关联能力缺乏显式保证。
- **长距离检测**：BEV 特征的分辨率固定，远距离目标在 BEV 网格中仅占极少像素，可能成为定位精度的瓶颈，论文在结论中也提及长距离场景是未来挑战之一。

> **注意**：上述失败模式为基于方法机理的推演，论文未提供对应的定量失败分析，需结合自身实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2312_01696/figures/004_Table.jpg]]


## 方法谱系与知识库定位

### 1. 方法谱系与继承关系

BEVNeXt 立足于**密集 BEV 范式**的复兴，其直接技术基底是 **BEVPoolv2**（作为基准密集 BEV 检测器），并在三个关键维度上对密集框架进行了系统性增强。在方法谱系上，BEVNeXt 可被视为密集 BEV 路线在稀疏查询式方法冲击下的一次全面反击。

**与密集 BEV 前驱的关系：**
- **BEVDepth**（Li et al., AAAI 2023）开创了显式深度监督的先河，BEVNeXt 继承了这一思路，但将深度估计从 1/16 特征图提升至 1/8 特征图，并引入 CRF 调制以补偿稀疏监督下的深度一致性不足。
- **SOLOFusion**（Park et al., ICLR 2022）代表了先前最优的密集时序 BEV 检测器，其采用并行拼接历史 BEV 特征并辅以自车运动变换。BEVNeXt 在时序融合上直接对标 SOLOFusion，但以 Res2Fusion 替代了其并行融合机制，核心差异在于跳过自车运动变换以规避动态物体错位。

**与稀疏查询式方法的对话：**
- **StreamPETR**（Wang et al., ICCV 2023）和 **SparseBEV**（Liu et al., ICCV 2023）代表了稀疏查询范式的先进水平。BEVNeXt 在检测头设计中明确借鉴了稀疏查询式方法的“透视精炼”思想——通过两阶段目标解码器，先由 CenterPoint 产生热图，再通过透视可变形注意力对 ROI 特征进行精炼。但 BEVNeXt 的独特之处在于，其反向投影仅用于精炼目标级 BEV 特征，而非整个 BEV 表示，且该过程由 CRF 调制的深度嵌入增强。

### 2. 方法适用边界与前提假设

BEVNeXt 的设计建立在以下关键前提之上，这些前提也构成了其适用边界：

1. **密集深度估计天然优势假设**：该方法的核心立论是密集 BEV 表达天然擅长深度估计与目标定位。当深度监督极度稀疏（如 LiDAR 覆盖率约 50%）时，CRF 调制的增益尤为显著（+1.9% NDS）；但在密集点云监督下，CRF 调制增益有限（+0.2% NDS），表明该模块的价值与监督密度强相关。

2. **时序融合窗口的尺度敏感性**：Res2Fusion 的性能高度依赖窗口大小的选择。实验表明窗口大小 3 能在短期局部性与长期感受野之间取得最佳平衡，窗口过大或过小均会导致性能下降。此参数需针对具体场景调优，不具备跨设置的普适性。

3. **动态场景下的运动假设**：跳过自车运动变换的前提是 Res2Fusion 的扩大感受野足以隐式处理运动对齐。但这一假设在高度动态场景下的鲁棒性尚未被充分验证，论文仅指出强制 warp 会导致动态物体错位，但未量化不同运动速度下的性能退化程度。

4. **计算效率的折衷**：BEVNeXt 以 ResNet101 为骨干时达到 4.4 FPS，优于 SOLOFusion（1.5 FPS）但慢于 StreamPETR（6.4 FPS），表明密集框架在效率上仍与稀疏范式存在差距，在实时性要求极高的场景中可能受限。

### 3. 已知局限与开放问题

**论文明确指出的局限：**
- 密集 BEV 框架在效率上仍落后于稀疏查询式范式，如何在保持定位鲁棒性的同时提升推理速度是待解难题。
- 将 BEV 框架集成到长距离感知场景中存在挑战，当前方法在远距离深度估计和计算开销方面均未给出解决方案。

**需要人工验证或进一步探索的问题：**
- CRF 调制在极端天气或光照条件下的深度一致性表现缺乏实验支撑，论文仅在标准 nuScenes 条件下验证。
- Res2Fusion 在更长时序跨度（如超过 8 帧历史）下的性能饱和点未被探索，其可扩展性存疑。
- 两阶段目标解码器中的透视可变形注意力与 CRF 深度嵌入的交互机制未被充分消解——Table 7 显示深度嵌入单独带来 0.8% NDS 增益，但其与注意力机制的耦合效应缺乏独立分析。
- 论文未在 Waymo Open Dataset 等更大规模或不同传感器配置的数据集上验证，方法的跨数据集泛化能力尚需外部验证。

### 4. 在知识库中的定位

BEVNeXt 在 3D 目标检测知识库中占据**密集 BEV 范式复兴者**的位置。在 2023 年前后稀疏查询式方法（如 DETR3D、PETR 系列、SparseBEV）迅速崛起的背景下，BEVNeXt 证明了密集框架通过现代化的 2D 建模增强、多尺度时序融合和实例级特征精炼，仍能在检测精度和定位鲁棒性上全面超越稀疏方法。其 64.2 NDS 的 nuScenes 测试集成绩和最低的 mATE 定位误差，为密集 BEV 路线提供了强有力的实证支撑，同时也揭示了效率瓶颈这一密集范式尚未克服的根本性挑战。

## 原文 PDF

![[paperPDFs/CVPR_2024/BEVNeXt_Reviving_Dense_BEV_Frameworks_for_3D_Object_Detection.pdf]]
