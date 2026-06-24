---
title: "ComPose: A Unified Completion-Pose Framework for Robust Category-Level Object Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ComPose_A_Unified_Completion_Pose_Framework_for_Robust_Category_Level_Object_Pose_Estimation.pdf
project_link: null
code_link: null
aliases:
- ComPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过形状补全恢复完整几何形状，为姿态估计提供全面的结构线索。
primary_logic: 将形状补全作为任务驱动的内部组件，紧密集成到统一的姿态估计网络中，而非作为独立的预处理步骤；通过基于关键点的渐进式补全模块获取完整几何表示，并利用几何关系编码和几何关系一致性损失强化全局结构对齐，从而更有效且高效地利用完整几何信息。
claims:
- 将AG-Pose的深度输入替换为地面真实完整点云时，10°2cm准确率从68.5%飙升至91.7%，证明完整几何信息的上界性能增益巨大。
- 简单的两阶段“先补全后姿态”级联流水线仅带来边际性能提升（71.0%），且推理速度从33.5 FPS降至21.5 FPS；而ComPose的统一框架在38.4 FPS下实现更优精度。
- 在REAL275深度模式下，ComPose的10°2cm指标比AG-Pose提高9.1%，证明了紧密集成补全的有效性。
- REAL275 上 10°2cm = 77.6
---

# ComPose: A Unified Completion-Pose Framework for Robust Category-Level Object Pose Estimation

> [!tip] 核心洞察
> 将形状补全作为任务驱动的内部组件，紧密集成到统一的姿态估计网络中，而非作为独立的预处理步骤；通过基于关键点的渐进式补全模块获取完整几何表示，并利用几何关系编码和几何关系一致性损失强化全局结构对齐，从而更有效且高效地利用完整几何信息。

| 字段 | 内容 |
|------|------|
| 中文题名 | ComPose：面向鲁棒类别级物体姿态估计的统一补全-姿态框架 |
| 英文题名 | ComPose: A Unified Completion-Pose Framework for Robust Category-Level Object Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Ren_ComPose_A_Unified_Completion-Pose_Framework_for_Robust_Category-Level_Object_Pose_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ComPose |
| Dataset | REAL275, HouseCat6D |

> [!tip] 效果简介
> - REAL275 上，10°2cm 77.6 vs 68.5 (AG-Pose, depth-only) (+9.1)；5°2cm 55.6 vs 48.8 (AG-Pose, depth-only) (+6.8)；5°2cm 89.2。
> - HouseCat6D 上，IoU_50 (depth-only) 84.2 vs 79.0 (AG-Pose, depth-only) (+5.2)；5°2cm (RGB-D) 85.0 vs 84.0 (GCE-Pose, RGB-D) (+1.0)。

## 概述

类别级物体姿态估计的核心挑战在于：从单视角深度或RGB-D观测中推理6D姿态时，输入点云天然存在几何不完整性，严重制约了网络捕获完整物体形状以进行鲁棒推理的能力。现有方法要么直接从部分点云提取几何特征，要么借助类别级形状先验来弥补信息缺失，但本质上仍在不完整几何上操作，性能提升有限。

ComPose的核心洞察是：**将形状补全作为任务驱动的内部组件，紧密集成到统一的姿态估计网络中**，而非作为独立的预处理步骤。具体而言，ComPose通过基于关键点的渐进式补全模块恢复完整几何表示（稀疏关键点与密集点云），并利用几何关系编码和几何关系一致性损失强化全局结构对齐，从而更有效且高效地利用完整几何信息。

决定性的动机证据来自Oracle实验：当将AG-Pose（Lin et al., CVPR 2024）的深度输入替换为地面真实完整点云时，REAL275上的10°2cm准确率从68.5%飙升至91.7%，揭示了完整几何信息的上界性能增益巨大。然而，简单的两阶段“先补全后姿态”级联流水线仅带来边际提升（71.0%），且推理速度从33.5 FPS降至21.5 FPS，表明分离式设计会引入累积误差与计算冗余。ComPose的统一框架在38.4 FPS下实现了更优精度，在REAL275深度模式下10°2cm指标比AG-Pose提高9.1%。

在方法谱系上，ComPose区别于**GPV-Pose**（Di et al., CVPR 2022）的几何引导投票、**SPD**（Tian et al., ECCV 2020）的形状先验变形、**SecondPose**（Chen et al., CVPR 2024）的DINOv2双流融合以及**GCE-Pose**（Li et al., CVPR 2025）的全局上下文增强——这些方法均未在统一的端到端框架内显式恢复并利用完整几何。ComPose在REAL275和HouseCat6D两个基准上均取得领先结果，同时验证了其在严重遮挡场景下的鲁棒性优势。

## 背景与动机

类别级物体姿态估计旨在从单张RGB-D或深度图像中预测未知实例在规范空间中的6D姿态（3D旋转与3D平移）。与实例级方法不同，类别级估计必须泛化到训练中未见过的物体实例，因此对模型从有限观测中推断完整物体几何的能力提出了极高要求。

### 部分观测带来的几何不完整性瓶颈

现有方法普遍从部分点云中直接提取几何特征进行姿态推理。然而，由于单视角观测固有的自遮挡和传感器视场限制，输入点云往往只覆盖物体的一小部分表面。这种几何不完整性严重制约了网络捕获完整物体形状的能力，成为限制姿态估计鲁棒性的核心瓶颈。如图1所示，经典方法直接从部分点云编码几何特征，无法获取被遮挡区域的形状信息；基于类别先验的方法虽然引入了形状先验知识来增强特征理解，但本质上仍然在不完整几何上操作，未能从根本上解决信息缺失问题。

### 完整几何信息的上界性能揭示巨大增益空间

一个关键性的证据实验揭示了完整几何信息的潜在价值：当将**AG-Pose**（Lin et al., CVPR 2024）的深度输入替换为地面真实完整点云时，其在REAL275数据集上的10°2cm准确率从68.5%飙升至91.7%（增幅达23.2个百分点，见Figure 2）。这一结果表明，一旦网络能够获取完整的物体几何信息，姿态估计性能存在巨大的提升空间。然而，在实际应用中，完整点云在推理时并不可得，因此如何从部分观测中有效恢复完整几何信息，成为弥合这一性能差距的关键。

### 简单两阶段流水线的局限性

一个直接的思路是将形状补全作为独立的预处理步骤，与姿态估计串联形成两阶段流水线。然而，实验表明这种简单级联策略仅带来边际性能提升——10°2cm准确率仅从68.5%微升至71.0%，同时推理速度从33.5 FPS骤降至21.5 FPS（见Figure 2）。这种效率下降源于两个独立网络带来的计算冗余，而精度提升有限则表明分离式设计容易引入累积误差，且补全过程缺乏面向姿态估计任务的目标导向性。

### 本文动机：统一框架中的任务驱动形状补全

基于上述分析，本文的核心动机是：**将形状补全作为任务驱动的内部组件，紧密集成到统一的姿态估计网络中**，而非将其视为独立的预处理步骤。通过这种方式，补全过程能够直接服务于姿态估计目标，从部分观测中恢复完整几何表示，为后续的姿态推理提供全面的结构线索。同时，统一框架的设计消除了分离式流水线的额外计算开销和累积误差风险，有望在精度和效率之间取得更好的平衡。

## 核心创新

ComPose 的核心创新在于将形状补全从独立的预处理步骤转变为一个**任务驱动的内部组件**，与姿态估计在单一网络中紧密集成。这一设计源于对瓶颈的深刻洞察：部分点云固有的几何不完整性严重制约了网络捕获完整物体形状以进行鲁棒姿态推理的能力。通过恢复完整几何形状，ComPose 为姿态估计提供了全面的结构线索，从而实现了精度与效率的双重提升。

### 关键设计差异：统一集成 vs. 两阶段级联

传统的直观思路是将形状补全作为前置步骤，形成“先补全后姿态”的级联流水线。然而，实验表明（Figure 2），这种简单的两阶段方案仅将 AG-Pose 的 10°2cm 准确率从 68.5% 边际提升至 71.0%，且推理速度从 33.5 FPS 骤降至 21.5 FPS。这一结果揭示了两阶段方案的两大缺陷：**累积误差**（补全误差会直接传播至姿态估计阶段）和**计算冗余**（两个独立网络带来额外开销）。

ComPose 的统一框架从根本上解决了这一问题。它将形状补全和姿态估计融合在单一网络中，消除了阶段间的信息损失和重复计算，在 38.4 FPS 的推理速度下实现了 77.6% 的 10°2cm 准确率，在精度-效率平衡上显著优于两阶段方案。

### 四个核心 Changed Slots

相对于基线方法 AG-Pose，ComPose 在四个关键维度上进行了系统性创新：

**1. 形状表示获取：从部分几何到完整几何**

基线方法直接从部分点云提取几何特征，不进行形状补全。ComPose 引入了**关键点渐进式补全模块**（Keypoint-based Progressive Completion），通过自适应选择候选关键点并利用 Transformer 解码器逐步细化，同时预测稀疏关键点和密集完整点云。这一设计使网络能够获取完整的几何表示，而非仅依赖不完整的观测信息。

**2. 关键点特征增强：引入几何上下文编码**

基线方法缺乏专门的几何上下文增强机制。ComPose 设计了**几何关系编码模块**（Geometric Relation Encoding），为每个关键点融合其局部 K 近邻几何关系与全局几何关系嵌入。这一显式的几何上下文编码使关键点特征具备了更强的几何感知能力。

**3. 坐标变换监督：从逐点对应到全局结构对齐**

基线方法仅使用逐点 L2 对应损失进行监督。ComPose 额外引入了**几何关系一致性损失**（Geometric Relation Consistency Loss），通过最小化观测空间与规范 NOCS 空间中成对距离矩阵的均方误差，强制保持全局几何结构的一致性。这一高阶结构对齐监督有效约束了坐标变换的全局一致性。

**4. 流水线集成策略：从分离到统一**

这是 ComPose 最根本的架构创新。基线方法将形状补全和姿态估计视为两个独立阶段，而 ComPose 在单一网络中紧密集成二者，消除了额外开销并实现了端到端的联合优化。这一统一集成策略是实现精度-效率双赢的关键。

### 创新有效性的决定性证据

完整几何信息对姿态估计的巨大增益是 ComPose 设计的根本动机。Oracle 实验（Figure 2）显示，将 AG-Pose 的深度输入替换为地面真实完整点云时，10°2cm 准确率从 68.5% 飙升至 91.7%，揭示了完整几何信息的上界性能增益高达 23.2 个百分点。ComPose 通过任务驱动的内部补全，有效逼近了这一上界，在 REAL275 深度模式下将 10°2cm 指标提升 9.1 个百分点。

消融实验进一步验证了各创新模块的贡献：将完整形状补全替换为仅重建可见区域的策略，5°2cm 指标骤降 6.0 个百分点；移除几何关系编码模块后，5°2cm 下降 6.1 个百分点；移除几何关系一致性损失后，5°2cm 下降 1.8 个百分点。这些结果一致表明，完整几何恢复与显式几何关系建模是性能提升的核心驱动力。

## 整体框架

ComPose 是一个支持 RGB-D 与纯深度两种输入模式的统一框架，其核心设计理念是将形状补全作为任务驱动的内部组件紧密嵌入姿态估计网络，而非作为独立的预处理步骤。如 Figure 3 所示，整个流水线由四个功能模块串联构成：**部分特征提取**、**基于关键点的渐进式补全**、**几何关系编码**以及**基于对应的姿态估计**。

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/003_Figure_3.jpg]]
*Figure 3: (a) Overview of the proposed ComPose framework, which supports both RGB-D and depth-only settings, where the latter omits the RGB images*

### 输入与特征提取

框架接收两类输入：从深度图反投影并下采样得到的部分点云 $\pmb{P}^{\mathrm{part}} \in \mathbb{R}^{\breve{N}^{\mathrm{part}} \times 3}$，以及在 RGB-D 模式下额外提供的裁剪 RGB 图像 $\pmb{I}^{\mathrm{rgb}} \in \mathbb{R}^{H \times W \times 3}$。部分特征提取模块采用 PointNet++ 提取逐点几何特征；在 RGB-D 设定下，进一步借鉴 **SecondPose**（Chen et al., CVPR 2024）的做法，利用 DINOv2 提取姿态一致的语义特征，并通过自注意力层对融合后的初始特征进行全局交互优化，得到精细化的部分表示 $\pmb{F}^{\mathrm{part}}$（Equation 1）。

### 渐进式形状补全

这是框架的核心创新模块。与经典方法直接从部分点云编码几何特征或依赖类别级形状先验不同，ComPose 通过一个 Transformer 解码器结构，以自适应选择的候选关键点作为查询（Equation 3），与部分特征 $\pmb{F}^{\mathrm{part}}$ 进行交叉注意力交互，逐步细化关键点的空间位置与特征表示（Equation 4）。该过程同时输出稀疏的完整关键点 $\pmb{P}^{\mathrm{kpt}}$ 和每个关键点周围的密集局部点集，二者拼接构成恢复的完整点云 $\pmb{P}^{\mathrm{com}}$。这种“稀疏关键点 + 密集局部几何”的双层表示，既捕获了全局拓扑结构，又保留了细粒度表面信息。

### 几何关系编码与姿态求解

补全得到的关键点特征 $\pmb{F}^{\mathrm{kpt}}$ 随后进入几何关系编码模块。该模块显式计算每个关键点的局部 K 近邻几何嵌入与全局几何关系嵌入，并通过交叉注意力与 MLP 融合，生成几何增强的关键点特征 $\pmb{F}^{\mathrm{geo}}$（Equation 14）。最后，姿态估计模块从 $\pmb{F}^{\mathrm{geo}}$ 预测 NOCS 坐标 $\pmb{O}^{\mathrm{kpt}}$，结合深度估计器或直接通过 Umeyama 算法求解最终的 6D 姿态。

### 端到端联合优化

整个框架以端到端方式联合优化，总损失函数由补全损失、关键点得分损失、对应损失和几何关系一致性损失加权求和构成（权重分别为 $\lambda^{\mathrm{com}}=15$、$\lambda^{\mathrm{score}}=1$、$\lambda^{\mathrm{corr}}=2$、$\lambda^{\mathrm{geo}}=1$）。其中几何关系一致性损失（Equation 16）通过约束观测空间与规范 NOCS 空间中的成对距离矩阵保持一致，强制网络学习高阶结构对齐，这是保证坐标变换鲁棒性的关键设计。

## 核心模块与公式推导

ComPose 框架由四个紧密耦合的模块构成：部分特征提取、基于关键点的渐进式补全、几何关系编码，以及基于对应的姿态估计。本节聚焦于前三个核心模块的关键设计与公式。

### 部分特征提取

给定从深度图反投影并下采样得到的部分点云 $\pmb{P}^{\mathrm{part}} \in \mathbb{R}^{\breve{N}^{\mathrm{part}} \times 3}$，首先采用 PointNet++ 提取逐点几何特征。在 RGB-D 模式下，进一步遵循 **SecondPose**（Chen et al., CVPR 2024）的做法，使用 DINOv2 从裁剪后的 RGB 图像 $\pmb{I}^{\mathrm{rgb}} \in \mathbb{R}^{H \times W \times 3}$ 中提取姿态一致的语义特征，并与几何特征拼接得到初始特征 $\pmb{F}^{\mathrm{init}}$。

为增强部分点云内部的全局上下文交互，通过自注意力层对初始特征进行细化：

$$\pmb{F}^{\mathrm{part}} = \mathrm{SA}(\pmb{F}^{\mathrm{init}} + \mathrm{PE}(\pmb{P}^{\mathrm{part}})) \tag{1}$$

其中 $\mathrm{PE}(\cdot)$ 为位置编码，$\mathrm{SA}(\cdot)$ 为标准缩放点积自注意力：

$$\mathrm{SA}({\pmb Q}) = \phi(({\pmb Q}{\pmb W}^{Q})({\pmb Q}{\pmb W}^{K})^{\top} / \sqrt{D})({\pmb Q}{\pmb W}^{V}) \tag{2}$$

$\phi$ 为 softmax 函数，$D$ 为特征维度。经过自注意力后的 $\pmb{F}^{\mathrm{part}}$ 即为包含全局上下文的部分特征表示，将作为后续补全模块的交互基础。

### 基于关键点的渐进式补全

该模块是 ComPose 的核心创新，旨在从部分观测中恢复完整的物体几何形状。其关键设计在于：并非直接回归完整点云，而是通过预测一组稀疏的完整关键点及其周围的密集局部点集，以由粗到精的方式渐进式重建完整形状。

**关键点查询构建。** 首先从部分点云中自适应选择候选关键点 $\pmb{C}^{\mathrm{kpt}}$，包括可见区域和缺失区域的候选点。随后，将全局特征 $\pmb{f}^{\mathrm{global}}$ 复制到每个候选关键点，并加上位置编码，构成关键点查询向量：

$$\pmb{Q}^{\mathrm{kpt}} = \mathrm{Repeat}(\pmb{f}^{\mathrm{global}}) + \mathrm{PE}(\pmb{C}^{\mathrm{kpt}}) \tag{3}$$

**关键点特征细化。** 通过交叉注意力与自注意力层，使关键点查询与部分特征 $\pmb{F}^{\mathrm{part}}$ 进行充分交互，逐步细化关键点特征：

$$\hat{\pmb{F}}^{\mathrm{kpt}} = \mathrm{CA}(\pmb{Q}^{\mathrm{kpt}}, \pmb{F}^{\mathrm{part}}), \quad \pmb{F}^{\mathrm{kpt}} = \mathrm{SA}(\hat{\pmb{F}}^{\mathrm{kpt}}) \tag{4}$$

交叉注意力使每个关键点能够从部分点云中聚合相关信息，自注意力则进一步建模关键点之间的全局依赖关系。经过多层解码器迭代后，得到精炼的关键点特征 $\pmb{F}^{\mathrm{kpt}}$ 和对应的关键点坐标 $\pmb{P}^{\mathrm{kpt}}$。

**密集局部几何重建。** 在每个精炼后的关键点周围，通过折叠式解码恢复细粒度局部几何。具体而言，将关键点特征 $\pmb{F}_n^{\mathrm{kpt}}$ 与其坐标 $\pmb{P}_n^{\mathrm{kpt}}$ 拼接后送入 MLP，输出重塑为局部密集点集 $\pmb{P}_n^{\mathrm{fold}}$。所有关键点的局部点集聚合后构成完整点云 $\pmb{P}^{\mathrm{com}}$。

### 几何关系编码

为充分利用补全得到的完整几何信息来增强姿态推理，ComPose 设计了几何关系编码模块，显式地将局部与全局几何上下文注入关键点特征。

**局部几何嵌入。** 对于每个关键点，在完整点云 $\pmb{P}^{\mathrm{com}}$ 中搜索其 $K$ 近邻，构建局部几何特征 $\pmb{F}_n^{\mathrm{knn}}$，并添加层级嵌入 $\pmb{E}_n^{\mathrm{l}}$ 以区分不同关键点的局部邻域。随后通过交叉注意力更新关键点特征：

$$\hat{\pmb{F}}_n^{\mathrm{kpt}} = \mathrm{CA}(\pmb{F}_n^{\mathrm{kpt}}, \mathrm{MLP}(\pmb{F}_n^{\mathrm{knn}} + \pmb{E}_n^{\mathrm{l}})) \tag{13}$$

**全局几何嵌入。** 计算所有关键点之间的成对距离矩阵 $\pmb{G}^{\mathrm{kpt}}$，并通过 MLP 编码为全局几何关系嵌入 $\pmb{E}_n^{\mathrm{g}}$，捕捉关键点之间的整体结构约束。

**几何增强特征融合。** 将更新后的关键点特征、全局平均池化特征、位置编码以及全局几何嵌入进行融合，得到最终的几何增强关键点特征：

$$\pmb{F}_n^{\mathrm{geo}} = \mathrm{MLP}(\hat{\pmb{F}}_n^{\mathrm{kpt}} + \mathrm{AvgPool}(\hat{\pmb{F}}^{\mathrm{kpt}}) + \mathrm{PE}(\pmb{P}_n^{\mathrm{kpt}}) + \mathrm{AvgPool}(\pmb{E}_n^{\mathrm{g}})) \tag{14}$$

该特征充分编码了局部细粒度几何与全局结构关系，为后续 NOCS 坐标预测提供了丰富的几何线索。

### 几何关系一致性损失

为确保从观测空间到规范 NOCS 空间的坐标变换保持全局几何结构的一致性，引入几何关系一致性损失。该损失通过最小化观测空间中关键点成对距离矩阵 $\pmb{G}^{\mathrm{kpt}}$ 与 NOCS 空间中对应距离矩阵 $\pmb{G}^{\mathrm{nocs}}$ 之间的均方误差来实现：

$$\mathcal{L}^{\mathrm{geo}} = \frac{1}{N^{\mathrm{kpt}} \times N^{\mathrm{kpt}}} \sum_{n,m} (G_{n,m}^{\mathrm{kpt}} - G_{n,m}^{\mathrm{nocs}})^2 \tag{16}$$

这一高阶结构监督信号与逐点对应损失互补，强制网络在预测 NOCS 坐标时保持物体各部分之间的相对几何关系不变，从而提升姿态估计对严重遮挡和几何不完整场景的鲁棒性。消融实验表明，移除该损失后 5°2cm 指标从 55.6 降至 53.8，降幅 1.8 个百分点，验证了其有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of geometric representation strategies in category-level object pose estimation. (a) Classic methods directly encode geometric features from partial point clouds, which limits their ability to capture complete object structures. (b) Prior-based approaches resort to category-level shape priors [31] to enhance feature understanding of full object shapes, yet they still operate on incomplete geometries. (c) Our method explicitly integrates shape completion to recover complete geometries, facilitating more comprehensive and robust pose reasoning*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/009_Figure_4.jpg]]
*Figure 4: Visualization of the keypoint-based progressive completion. Complete object geometries are progressively recovered*

## 实验与分析

### 核心实验设计逻辑

实验围绕一个中心假设展开：**部分点云固有的几何不完整性是制约类别级姿态估计性能的根本瓶颈**。为验证这一假设，作者设计了三个递进的实验层面：首先通过“神谕实验”揭示完整几何信息的上界性能增益；其次在标准基准上对比统一框架与分离式流水线的精度-效率权衡；最后通过消融实验逐模块验证形状补全策略、渐进式补全过程和几何关系建模各自的功能贡献。

### 基准性能对比

**Table 1** 汇总了在 REAL275 数据集上与最先进方法的全面对比。在深度模式下，ComPose 在 10°2cm 指标上达到 77.6%，相比 **AG-Pose** (Lin et al., CVPR 2024) 的 68.5% 提升 9.1 个百分点；在更严格的 5°2cm 指标上，从 48.8% 提升至 55.6%，增幅 6.8 个百分点。在 RGB-D 模式下，ComPose 的 5°2cm 达到 89.2%，15°5cm 达到 62.1%，均处于领先水平。值得注意的是，RGB-D 模式下与 **GCE-Pose** (Li et al., CVPR 2025) 的差距较小，提示语义特征的引入部分稀释了形状补全带来的相对增益。

在 HouseCat6D 数据集上（**Table 2**），深度模式下 IoU_50 从 AG-Pose 的 79.0% 提升至 84.2%（+5.2 个百分点）；RGB-D 模式下 5°2cm 达到 85.0%，比 GCE-Pose 的 84.0% 高出 1.0 个百分点。跨数据集的性能一致性表明，形状补全策略对不同场景分布具有良好的泛化能力。

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/005_Table_2.jpg]]
*Table 2: Performance comparison with state-of-the-art methods on the HouseCat6D dataset. The method marked with ‘*’ is reproduced by us. For each data setting, the best results are shown in bold, and the second best results are underlined*

### 神谕实验与流水线效率

**Figure 2** 展示了深度模式下精度与推理速度的散点分布。当将 AG-Pose 的深度输入替换为地面真实完整点云时，10°2cm 准确率从 68.5% 飙升至 91.7%（增幅 23.2 个百分点），直接证实了完整几何信息的上界性能增益巨大。然而，简单的两阶段“先补全后姿态”级联流水线仅将 10°2cm 提升至 71.0%，且推理速度从 33.5 FPS 降至 21.5 FPS。相比之下，ComPose 的统一框架在 RTX3090Ti 上达到 38.4 FPS，同时实现更高精度，证明了紧密集成策略在消除累积误差和计算冗余方面的双重优势。

### 遮挡鲁棒性分析

**Table 4** 报告了遮挡增强测试下的性能对比。在 REAL275 数据集上施加人工遮挡后，ComPose 在 5°2cm 指标上仍保持 49.2%，而 AG-Pose 降至 40.1%，**SecondPose** (Chen et al., CVPR 2024) 为 42.3%。这一结果表明，通过形状补全恢复的完整几何表示，为网络提供了超越可见区域的全局结构线索，使其在严重遮挡场景下仍能维持可靠的姿态推理。

### 形状补全策略消融

**Table 5** 系统消融了形状补全策略的三个关键维度。将完整形状补全替换为仅重建可见区域的“Partial Instance”策略后，5°2cm 从 55.6 下降至 49.6（降幅 6.0 个百分点），直接验证了恢复完整几何（而非简单重建可见表面）的核心作用。移除密集点云补全分支后，10°5cm 从 85.0 降至 83.3（降幅 1.7 个百分点），表明局部密集几何为关键点提供了细粒度的几何感知增强，但其贡献权重低于稀疏关键点补全。

### 渐进式补全过程消融

**Table 6** 在固定关键点数量为 64 的条件下，消融了渐进式补全的迭代轮次。单轮补全（无渐进细化）导致 5°2cm 从 55.6 降至 52.1（降幅 3.5 个百分点），说明多轮交叉注意力交互对于从部分特征中逐步恢复完整几何至关重要。这一发现与 **Figure 4** 的可视化一致：初始粗关键点仅捕获大致轮廓，经多轮细化后逐步逼近真实完整形状。

### 几何关系建模消融

**Table 7** 揭示了几何关系编码和一致性损失各自的功能贡献。移除几何关系编码模块后，5°2cm 从 55.6 降至 49.5（降幅 6.1 个百分点），是单模块消融中降幅最大的项，表明显式编码局部 K 近邻几何与全局几何关系嵌入对关键点特征的几何感知能力具有决定性影响。移除几何关系一致性损失后，5°2cm 从 55.6 降至 53.8（降幅 1.8 个百分点），验证了在观测空间与规范 NOCS 空间之间强制保持成对距离矩阵一致性，能够提供有效的高阶结构对齐监督。

### 形状重建质量

**Table 3** 以 REAL275 数据集中相机类别为例，比较了不同方法的 Chamfer Distance 重建误差。ComPose 的重建质量显著优于未集成补全的方法，且与专用补全网络相当，表明姿态估计任务驱动的补全模块并未牺牲重建精度，反而通过联合优化实现了两者的协同提升。

### 定性分析

**Figure 5** 展示了 ComPose 与 AG-Pose 在严重遮挡和几何不完整场景下的定性对比。在部分点云仅保留物体单侧表面的极端情况下，AG-Pose 的预测姿态出现明显偏转，而 ComPose 通过恢复完整几何结构，成功维持了准确的 6D 姿态估计。这进一步佐证了完整几何信息对于鲁棒姿态推理的不可替代性。

### 关键结论与边界

综合实验结果表明，ComPose 通过将形状补全紧密集成到姿态估计网络中，有效突破了部分点云几何不完整性的瓶颈。其性能增益主要来源于三个机制：完整几何恢复提供了全局结构约束，几何关系编码增强了关键点的局部-全局上下文感知，几何一致性损失强化了跨空间的结构对齐。然而，在 RGB-D 模式下与纯语义增强方法的差距缩小，提示多模态融合策略仍有优化空间。此外，当前框架依赖关键点数量作为超参数，如何在减少关键点依赖的同时保持精度与效率，仍是待探索的开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/004_Table_1.jpg]]
*Table 1: Performance comparison with state-of-the-art methods on the REAL275 dataset. The method marked with ‘*’ is reproduced by us. “Prior” refers to shape priors [31]. For each data setting, the best results are in bold, and the second best results are underlined*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/002_Figure_2.jpg]]
*Figure 2: Accuracy and inference speed comparison for the depthonly versions of different methods. The dashed circle indicates the performance upper bound achieved using ground-truth complete point clouds as input. Our ComPose achieves the best balance between accuracy and efficiency with 38.4 FPS on an RTX3090Ti GPU. More implementation details are provided in Section 4.3*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/008_Table_5.jpg]]
*Table 5: Ablation studies on the shape completion strategy. “Partial Instance” indicates reconstructing only visible object regions*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/011_Table_7.jpg]]
*Table 7: Ablation studies on the geometric relation modeling*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/007_Table_4.jpg]]
*Table 4: Performance comparison of different depth-only methods under occlusion-augmented testing on the REAL275 dataset*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative comparison between our ComPose and AG-Pose [15]. Red/Green indicates the predicted/GT results*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/010_Table_6.jpg]]
*Table 6: Ablation studies on the progressive completion process, where*

![[assets/figures/papers/paper_list_l2027_https_openaccess_thecvf_com_content_CVPR2026_html_Ren_ComPose_A_Unified/figures/006_Table_3.jpg]]
*Table 3: Reconstruction performance comparisons for the camera category on the REAL275 dataset, measured using Chamfer Distance*

## 方法谱系与知识库定位

### 1. 核心问题定位：部分观测与完整几何的鸿沟

类别级物体姿态估计的核心瓶颈在于，真实场景中传感器只能捕获物体的部分点云，而部分几何信息的缺失严重制约了网络对完整物体形状的理解，进而影响姿态推理的鲁棒性。ComPose 通过一个决定性的 oracle 实验量化了这一鸿沟：当将 **AG-Pose** (Lin et al., CVPR 2024) 的深度输入替换为地面真实完整点云时，REAL275 数据集上的 10°2cm 准确率从 68.5% 飙升至 91.7%（Figure 2），揭示了完整几何信息的上界性能增益高达 23.2 个百分点。这一发现直接定义了 ComPose 的核心因果调节变量——通过形状补全恢复完整几何形状，为姿态估计提供全面的结构线索。

### 2. 方法谱系定位：从独立先验到任务驱动补全

现有类别级姿态估计方法在处理几何不完整性时，可归纳为三条技术路线，ComPose 在其中开辟了新的范式：

- **经典直接编码方法**：**GPV-Pose** (Di et al., CVPR 2022) 等方法直接从部分点云中提取几何特征，依赖几何引导的逐点投票进行姿态推断。这类方法受限于输入的不完整性，无法捕获被遮挡区域的结构信息，在严重遮挡场景下性能退化显著。

- **基于形状先验的方法**：**SPD** (Tian et al., ECCV 2020) 和 **AG-Pose** (Lin et al., CVPR 2024) 等方法引入类别级形状先验，通过变形或对齐预定义的形状模板来增强对完整物体形状的理解。然而，这些方法本质上仍在不完整几何上操作，先验信息仅作为辅助线索，无法真正恢复缺失的几何结构。

- **两阶段补全-姿态流水线**：一种直观的改进思路是将形状补全作为独立预处理步骤，与姿态估计级联。但 ComPose 的实验表明，这种简单的“先补全后姿态”策略仅带来边际性能提升（10°2cm 准确率从 68.5% 提升至 71.0%），且推理速度从 33.5 FPS 降至 21.5 FPS（Figure 2）。其失效原因在于：独立补全模块缺乏姿态任务的引导，可能产生几何上合理但对姿态估计无益的补全结果；同时，两阶段分离引入累积误差和计算冗余。

- **ComPose 的统一集成范式**：ComPose 的核心洞察在于将形状补全作为**任务驱动的内部组件**紧密集成到姿态估计网络中，而非作为独立的预处理步骤。这种设计使得补全过程能够直接服务于姿态估计目标，消除额外计算开销，并在统一框架内实现端到端联合优化。在 REAL275 深度模式下，ComPose 以 38.4 FPS 的推理速度实现 77.6% 的 10°2cm 准确率，相比 AG-Pose 的 68.5% 提升 9.1 个百分点，同时速度更快。

### 3. 关键技术差异：四个维度的设计创新

ComPose 与基线方法 **AG-Pose** 在四个关键设计维度上存在本质差异：

| 设计维度 | AG-Pose (基线) | ComPose (本文) |
|---------|---------------|---------------|
| 形状表示获取 | 直接从部分点云提取几何特征，无形状补全 | 关键点渐进式补全模块恢复完整几何（稀疏关键点+密集点云） |
| 关键点特征增强 | 无专门的几何上下文增强机制 | 几何关系编码模块融合局部 KNN 几何与全局几何关系嵌入 |
| 坐标变换监督 | 仅使用逐点 L2 对应损失 | 额外添加几何关系一致性损失，强制保持观测空间与规范 NOCS 空间的成对距离矩阵一致性 |
| 流水线集成策略 | 无补全组件 | 单一网络中紧密集成补全与姿态估计，消除额外开销并共同优化 |

**关键点渐进式补全**是 ComPose 的核心技术贡献。该模块自适应选择候选关键点（包括可见和缺失区域），通过 Transformer 解码器逐步细化，预测稀疏关键点和周围密集点云。与仅重建可见区域的“Partial Instance”策略相比，完整形状补全使 5°2cm 指标从 49.6 提升至 55.6（提升 6.0 个百分点，Table 5），验证了恢复完整几何的关键作用。密集点云补全分支的消融进一步表明，局部密集几何增强了关键点的细粒度几何感知（10°5cm 从 83.3 降至 85.0，降幅 1.7 个百分点，Table 5）。

**几何关系编码**模块通过显式编码局部和全局几何上下文，显著增强了关键点特征的几何感知能力。消融实验显示，移除该模块后 5°2cm 从 55.6 降至 49.5（降幅 6.1 个百分点，Table 7），表明几何上下文建模对性能影响显著。**几何关系一致性损失**通过最小化观测空间与规范空间中成对距离矩阵的均方误差，强制保持全局结构对齐，移除后 5°2cm 下降 1.8 个百分点（Table 7）。

### 4. 性能边界与跨数据集泛化

在 REAL275 数据集上，ComPose 在深度模式下的 10°2cm 准确率达 77.6%，显著优于 **AG-Pose** (68.5%) 和 **SecondPose** (Chen et al., CVPR 2024) 等基线；RGB-D 模式下 5°2cm 达 89.2%，与最新方法 **GCE-Pose** (Li et al., CVPR 2025) 可比。

在 HouseCat6D 数据集上，ComPose 同样展现出良好的泛化能力：深度模式下 IoU_50 达 84.2（vs AG-Pose 79.0，提升 5.2 个百分点），RGB-D 模式下 5°2cm 达 85.0（vs GCE-Pose 84.0，提升 1.0 个百分点，Table 2）。遮挡鲁棒性实验（Table 4）进一步表明，ComPose 在严重遮挡场景下相比基线方法具有更稳定的性能表现。

### 5. 适用边界与开放问题

尽管 ComPose 在统一补全-姿态框架上取得了显著进展，其设计仍存在若干适用边界和待探索方向：

- **关键点数量依赖**：渐进补全过程依赖预设的关键点数量（实验中固定为 64），如何进一步减少对关键点数量的依赖，同时保持高精度与效率，是模型轻量化的重要方向。

- **跨任务泛化能力**：所提出的统一补全-姿态框架的核心思想——将任务驱动的几何补全集成到下游任务中——能否推广至其他 3D 视觉任务（如机器人抓取、场景补全），仍需进一步验证。

- **弱监督/自监督训练**：当前方法依赖完整的 CAD 模型和强监督信号进行形状补全训练。在没有 CAD 模型或强监督的情况下，如何实现类别级形状补全与姿态估计的弱监督或自监督训练，是推动该方法走向真实开放场景的关键挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/ComPose_A_Unified_Completion_Pose_Framework_for_Robust_Category_Level_Object_Pose_Estimation.pdf]]