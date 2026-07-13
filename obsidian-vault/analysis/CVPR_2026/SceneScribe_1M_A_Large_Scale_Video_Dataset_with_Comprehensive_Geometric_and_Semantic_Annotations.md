---
title: "SceneScribe-1M: A Large-Scale Video Dataset with Comprehensive Geometric and Semantic Annotations"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SceneScribe_1M_A_Large_Scale_Video_Dataset_with_Comprehensive_Geometric_and_Semantic_Annotations.pdf
project_link: "https://wangyunnan.github.io/SceneScribe-1M"
code_link: "https://github.com/UmiMarch/OpenVideo"
aliases:
- S1
- SceneScribe-1M
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 通过大规模并行部署多个专有模型（Qwen2.5-VL-72B、MegaSaM、TAPIP3D）对海量开放世界视频进行全面的几何与语义联合标注，弥补了单模态数据集的根本缺陷。
primary_logic: 构建一个统一的大规模多模态视频数据集，结合精确的相机参数、连续深度图、一致3D点轨迹和详细结构化文本描述，并设计解耦相机与物体运动的采样策略（SceneScribe-MVS），能够同时推动3D几何感知和可控视频生成的研究。
claims:
- 使用SceneScribe-1M数据训练后，单目深度估计模型MoGe在五个标准基准上的平均相对误差（Average Rel）从4.72降至4.68。
- 在CO3Dv2和ETH3D上的3D重建AUC30指标，使用SceneScribe-1M训练的VGGT从89.5提升至89.9。
- 在Sintel上的4D重建ATE指标，使用SceneScribe-1M训练的MonST3R从0.108降至0.099。
- 在TAP-Vid基准上的2D点跟踪平均AJ指标，使用SceneScribe-1M训练的CoTracker3从76.6提升至77.4。
---

# SceneScribe-1M: A Large-Scale Video Dataset with Comprehensive Geometric and Semantic Annotations

> [!tip] 核心洞察
> 构建一个统一的大规模多模态视频数据集，结合精确的相机参数、连续深度图、一致3D点轨迹和详细结构化文本描述，并设计解耦相机与物体运动的采样策略（SceneScribe-MVS），能够同时推动3D几何感知和可控视频生成的研究。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneScribe-1M：一个具有全面几何与语义标注的大规模视频数据集 |
| 英文题名 | SceneScribe-1M: A Large-Scale Video Dataset with Comprehensive Geometric and Semantic Annotations |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.07990) · [Project](https://wangyunnan.github.io/SceneScribe-1M) · [Code](https://github.com/UmiMarch/OpenVideo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | SceneScribe-1M 数据构建流水线 |
| Dataset | DIODE / ETH3D / KITTI / NYUv2 / ScanNet / Sintel, CO3Dv2 + ETH3D, Sintel, TAP-Vid-DAVIS / Kinetics / RGB-Stacking |

> [!tip] 效果简介
> - DIODE / ETH3D / KITTI / NYUv2 / ScanNet / Sintel (平均) 上，Average Rel↓ 4.68 vs 4.72 (-0.04)。
> - CO3Dv2 + ETH3D (平均) 上，AUC30↑ 89.9 vs 89.5 (+0.4)。
> - Sintel 上，ATE↓ 0.099 vs 0.108 (-0.009)。

## 概要

当前视频数据集在几何标注的全面性、动态场景覆盖以及数据规模三个维度上存在结构性短板：大多数数据集仅提供单一几何模态（如相机姿态或深度图），且主要面向静态场景，难以同时支撑大规模3D感知与可控视频生成对时空语义及几何信息的联合需求。**SceneScribe-1M** 以超过100万个动态场景、超过4,000小时的视频规模，首次在一个数据集中同时提供**深度图、相机姿态、一致3D点轨迹和结构化语义描述**，填补了这一空白。

其核心构建思路是**大规模并行部署多专有模型**：利用 Qwen2.5-VL-72B 生成结构化场景描述，MegaSaM 估计运动掩码、相机参数和连续深度图，TAPIP3D 结合深度与相机姿态生成一致的3D点轨迹。在此基础上，通过**多视图重投影解耦相机与物体运动**，构建了 SceneScribe-MVS 子集，在保留相机运动多样性的同时有效控制动态物体比例。

在方法谱系与知识库定位上，SceneScribe-1M 并非提出新的感知或生成模型，而是作为一个**统一的多模态视频数据基础设施**，直接服务于单目深度估计（如 **MoGe**）、3D/4D 场景重建（如 **VGGT**、**MonST3R**）、2D/3D 动态点跟踪（如 **CoTracker3**、**SpatialTrackerV2**）以及文本/姿态到视频生成等下游任务。与先前最大规模的类似数据集相比（Sekai 约600小时，SpatialVID 约2,000小时），SceneScribe-1M 在标注时长上提升了一个数量级，且是首个同时提供深度图、相机姿态和3D点轨迹的大规模视频数据集（Table 1）。

实验证据表明，使用 SceneScribe-1M 进行训练后，多个代表性基线模型在标准基准上获得了**一致且小幅但稳健的提升**：单目深度估计模型 MoGe 在五个基准上的平均相对误差（Average Rel）从 4.72 降至 4.68（Table 2）；VGGT 在 CO3Dv2 和 ETH3D 上的 3D 重建 AUC30 从 89.5 提升至 89.9（Table 3a）；MonST3R 在 Sintel 上的 4D 重建 ATE 从 0.108 降至 0.099（Table 3b）；CoTracker3 在 TAP-Vid 基准上的平均 AJ 指标从 76.6 提升至 77.4（Table 4a）。这些提升幅度虽不剧烈，但在多个任务和模型上的一致性验证了数据集作为通用训练资源的有效性。

需要指出的是，该数据集的标注质量受限于所采用现成模型（Qwen2.5-VL-72B、MegaSaM、TAPIP3D）的固有精度，这些模型自身的系统误差可能传播至数据集标注中；整个标注流水线消耗约15万GPU小时，构建成本较高；数据来源主要为公开网络视频，对极端环境或长尾场景的覆盖可能不足，且未进行地理或文化偏见的公平性评估。

### 问题的核心瓶颈

当前视频理解与生成领域面临一个根本性矛盾：**3D感知模型需要精确的几何信息（深度、相机姿态、点轨迹），而视频生成模型需要丰富的语义描述和动态场景覆盖**，但现有的视频数据集无法同时满足这两类需求。

具体而言，现有数据集的缺陷集中在三个维度：

1. **几何标注不完整**：大多数数据集仅提供部分几何标注——有的只有相机姿态，有的只有深度图，几乎没有数据集同时提供深度图、相机姿态和一致的3D点轨迹。这迫使研究者只能在碎片化的几何信息上进行训练，难以学习完整的3D场景表征。

2. **动态场景覆盖不足**：主流数据集（如RealEstate10K、ScanNet）主要聚焦于静态场景，缺乏对动态物体运动的标注。然而，现实世界中的视频大量包含运动物体，这种偏差限制了模型在开放场景下的泛化能力。

3. **规模与多样性的双重不足**：此前最大的类似数据集Sekai约600小时，SpatialVID约2000小时，在覆盖场景多样性方面仍显不足，尤其缺乏对复杂光照、快速运动和长尾场景的覆盖。

### 本文的核心动机

针对上述缺口，本文的动机可以概括为：**通过大规模并行部署多个专有模型，对海量开放世界视频进行全面的几何与语义联合标注，构建一个统一的大规模多模态视频数据集**。

这一思路的关键洞察在于：与其等待人工标注或依赖单一传感器采集，不如利用当前最先进的视觉语言模型（Qwen2.5-VL-72B）、运动结构估计模型（MegaSaM）和3D点跟踪模型（TAPIP3D）进行自动化标注。这种“模型标注”的范式虽然引入了标注偏差的风险，但换来了前所未有的规模（超过4,000小时）和标注全面性。

### 预期的下游推动

SceneScribe-1M的设计目标不仅是填补数据集空白，更是要同时推动3D几何感知和可控视频生成两个方向的研究。其核心假设是：**一个包含精确相机参数、连续深度图、一致3D点轨迹和详细结构化文本描述的统一数据集，能够为多个下游任务提供协同增益**。这种“一数据集多任务”的设计理念，试图打破当前各子领域数据集相互独立的局面。

需要注意的是，该数据集来源于公开网络视频，标注模型本身的系统性偏差可能传播至数据集，且对极端环境和长尾场景的覆盖仍有局限——这些限制需要在后续使用中加以注意和缓解。

## 核心方法与创新机理

SceneScribe-1M 的核心创新并非提出新的模型架构，而是通过**大规模多模型协同标注流水线**，系统性弥补了现有视频数据集在几何与语义标注上的结构性缺陷。其关键突破体现在三个“changed slots”上：

### 1. 几何标注的全面性：从单一模态到联合标注

此前数据集通常仅提供部分几何标注——例如仅包含相机姿态（如 RealEstate10K）或仅包含深度图（如 SpatialVID），缺乏对三维空间结构的完整刻画。SceneScribe-1M 首次在大规模视频数据集上同时提供**深度图、相机姿态和一致的3D点轨迹**（Table 1），三者协同构成了从像素级深度到全局相机运动再到稀疏三维对应点的完整几何金字塔。

这一全面性的实现依赖于流水线中三个专有模型的并行部署（Figure 2）：**MegaSaM** 负责估计运动掩码、相机参数和连续深度图；**TAPIP3D** 利用前一步的深度与相机姿态，将 MegaSaM 输出的2D轨迹提升为一致的3D点轨迹。这种“几何标注链”设计使得各标注之间具有内在一致性，而非独立生成的松散集合。

### 2. 动态场景的覆盖：从静态假设到运动感知

大多数现有3D数据集（如 CO3D、ScanNet）局限于静态场景或可控环境，缺乏对真实世界中动态物体运动的标注。SceneScribe-1M 明确覆盖丰富的动态场景，并通过 MegaSaM 生成的**运动掩码**标记动态区域（Figure 1），使数据集天然支持动态点跟踪、4D重建等需要时序运动理解的下游任务。

### 3. 数据规模的跃升与解耦采样策略

在规模维度，SceneScribe-1M 的标注视频时长达到**4191小时**，远超此前最大的类似数据集（Sekai 约600小时，SpatialVID 约2000小时）。但规模本身并非创新的全部——更具方法学意义的是其提出的 **SceneScribe-MVS 多视图子集采样策略**。

该策略通过多视图重投影解耦相机运动与物体运动：利用2D重投影误差 $e_{2d}$、3D相对深度误差 $e_{3d}$ 和 RGB L2 误差 $e_{rgb}$ 定义运动掩码 $M_{motion}$，过滤动态物体占比较高的片段，同时保留相机运动的多样性（Figure 6, Figure 7）。消融实验表明，SceneScribe-MVS 的相机运动分布（距离、旋转、转向次数）与原始数据集高度相似，而物体运动指标（s1、s2 分数、轨迹可见性比）显著趋于静态。这一设计使得同一数据集既能支撑动态场景理解（原始 SceneScribe-1M），也能服务于静态多视图任务（SceneScribe-MVS），实现了“一集两用”的资源效率。

### 创新本质的再定位

从因果机制看，SceneScribe-1M 的贡献可概括为：**以大规模算力（超过1000块 NVIDIA H20 GPU）为杠杆，撬动多个专有模型的知识蒸馏到统一数据载体中**，从而弥补了单模态数据集的根本缺陷。其真正的“causal knob”不在于模型设计，而在于流水线的并行化部署策略和几何-语义联合标注的组织方式。这一思路为后续构建更大规模、更多模态的世界模型数据集提供了可复用的范式。

SceneScribe-1M 的数据构建流水线遵循“收集—预处理—联合标注—多视图子集采样”四阶段范式，其核心设计目标是在大规模开放世界视频上实现几何与语义信息的全面、一致标注。图2展示了该流水线的整体架构。

**阶段一：视频收集。** 流水线从四个来源汇聚原始视频：三个现有的大规模视频-文本对数据集——HD-VILA-100M、Panda-70M、Koala-36M——以及一个从 Pexels 平台新策划的 Pexels-Video 数据集。收集阶段对视频的基本规格设定了初始门槛：空间分辨率高于1080p、帧率不低于10 fps、时长介于5秒至1分钟之间。

**阶段二：视频预处理与过滤。** 原始视频在进入标注前需经过双重筛选。规格层面，进一步过滤分辨率、帧率和时长不符合要求的视频；内容层面，引入 Qwen2.5-VL-72B 对视频的六维质量指标进行评估，同时利用 TransNetV2 进行镜头过渡检测与分割，确保每个视频片段内部的时间连续性。经过此阶段后，保留的视频在运动多样性和光照条件上均达到可控标准（见图3、图4的统计分布）。

**阶段三：语义与几何联合标注。** 这是流水线的核心模块，通过并行部署三个专有模型实现对每个视频片段的全方位标注：
- **Qwen2.5-VL-72B** 负责生成结构化的场景描述文本，涵盖场景氛围、主体对象和动作等关键语义维度；
- **MegaSaM** 同时估计运动掩码、相机参数（内参和外参）以及连续深度图；
- **TAPIP3D** 利用 MegaSaM 输出的深度图和相机姿态，生成时空一致的3D点轨迹。

三个模型的推理通过批处理和跨多机（超过1,000块 NVIDIA H20 GPU）的并行化策略高效执行，最终产出覆盖4,191小时视频的百万级动态场景标注。

**阶段四：多视图子集采样（SceneScribe-MVS）。** 为支持静态多视图任务，流水线设计了一个基于多视图重投影的解耦采样策略。该策略通过计算2D重投影误差 $e_{2d}$、3D相对深度误差 $e_{3d}$ 和RGB差异 $e_{rgb}$，并联合阈值化生成运动掩码 $M_{motion}$，有效区分相机运动与物体运动。在此基础上构建的 SceneScribe-MVS 子集在显著降低动态物体占比的同时，保留了与原始数据集高度相似的相机运动分布（距离、旋转、转向次数），实现了相机运动多样性与场景静态性的解耦控制。

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/003_Figure_2.jpg]]
*Figure 2: Curation Pipeline for SceneScribe-1M consist of: (a) We begin by collecting large-scale videos from various sources; (b) Raw videos undergo specification and content inspection, with temporal segmentation models employed to ensure continuity; and (c) We integrate Qwen2.5-VL-72B [6], MegaSaM [33], and TAPIP3D [68] to perform comprehensive geometric and semantic annotations*

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/001_Figure_1.jpg]]
*Figure 1: SceneScribe-1M offers more than one million dynamic scenes spanning over 4,000 hours, featuring comprehensive semantic and geometric annotations (i.e., detailed description, motion masks, camera poses, continuous video depths, and dynamic tracks). It supports diverse downstream tasks (i.e., modular depth estimation, scene reconstruction, dynamic point tracking, and pose/text-to-video generation)*

### 数据构建流水线概览

SceneScribe-1M 的数据构建流水线由三个关键步骤组成：**视频收集**、**视频预处理与过滤**、**语义与几何联合标注**（见图2）。流水线的核心设计目标是通过大规模并行部署多个专有模型，对海量开放世界视频进行全面的几何与语义联合标注，从而弥补单模态数据集在深度图、相机姿态和3D点轨迹上无法同时提供的根本缺陷。

### 关键模块详解

#### 模块一：视频收集与预处理

视频来源涵盖四个大规模视频-文本对数据集：HD-VILA-100M、Panda-70M、Koala-36M，以及从 Pexels 平台新收集的 Pexels-Video 数据集。原始视频经过严格的规格过滤：空间分辨率需大于 1080p，帧率不低于 10 fps，时长控制在 5 秒至 1 分钟之间。随后使用 **TransNetV2** 进行镜头过渡检测与分割，确保每个视频片段内的时空连续性。内容质量方面，采用 **Qwen2.5-VL-72B** 从六个维度评估视频内容，进一步筛除低质量样本。

#### 模块二：语义与几何联合标注

这是整个流水线的核心模块，通过集成三个专有模型实现全面的多模态标注：

- **语义标注**：采用 **Qwen2.5-VL-72B** 作为语义标注引擎，为每个视频片段生成结构化的场景描述，涵盖场景上下文、主要物体和动作等关键信息。
- **几何标注**：采用 **MegaSaM** 同时估计运动掩码、相机参数（内参和外参）以及连续深度图；随后 **TAPIP3D** 利用 MegaSaM 输出的深度图和相机姿态，生成时空一致的 3D 点轨迹。
- **并行化部署**：整个标注流水线使用超过 1,000 块 NVIDIA H20 GPU，通过批处理和multithreading对 MegaSaM 和 TAPIP3D 的推理进行并行化加速。

#### 模块三：多视图子集采样（SceneScribe-MVS）

为解决动态物体对静态多视图任务的干扰，本文设计了一种基于多视图重投影的解耦采样策略。该策略通过计算重投影误差来区分相机运动与物体运动，从而构建一个紧凑的子集 **SceneScribe-MVS**，在有效控制动态物体包含比例的同时，保留原始数据集的相机运动多样性。

### 关键公式推导

多视图重投影解耦策略的核心在于定义一组误差度量，用于判断像素点是否属于静态区域。给定源视图和参考视图之间的相机位姿变换，首先将源视图的深度图 $D_s$ 和图像 $I_s$ 重投影到参考视图坐标系下，得到重投影深度 $D_{s2r}$ 和重投影图像 $I_{s2r}$，以及重投影像素坐标 $(x_{s2r}, y_{s2r})$。

**2D 重投影误差**衡量重投影像素位置与参考图像素位置之间的几何一致性：

$$e_{2d} = \sqrt{(x_{s2r} - x_r)^2 + (y_{s2r} - y_r)^2}$$

其中 $(x_r, y_r)$ 为参考视图中的对应像素坐标。该误差越小，表明重投影在图像平面上的几何对齐越精确。

**3D 深度误差和 RGB 误差**进一步衡量重投影后的三维和颜色一致性：

$$e_{3d} = |D_{s2r} - D_r| / D_r, \quad e_{rgb} = \|I_{s2r} - I_r\|_2$$

其中 $D_r$ 和 $I_r$ 分别为参考视图的深度图和 RGB 图像。$e_{3d}$ 采用相对深度误差，避免绝对深度尺度差异的影响；$e_{rgb}$ 采用 L2 范数衡量颜色差异。

**运动掩码定义**：综合上述三个误差度量，定义二值运动掩码 $M_{motion}$，用于标记静态且标注准确的像素点：

$$M_{motion} = (e_{2d} < \tau_1) \wedge (e_{3d} < \tau_2) \wedge (e_{rgb} < \tau_3)$$

其中 $\tau_1$、$\tau_2$、$\tau_3$ 为预设阈值。满足所有三个条件的像素被标记为静态点，否则被视为动态物体或标注噪声区域。该掩码是 SceneScribe-MVS 采样策略的数学基础：通过筛选运动掩码中静态点占比较高的视频片段，实现对动态物体的有效过滤。

**消融验证**：Figure 6 显示，经过采样策略后，SceneScribe-MVS 的物体运动指标（s1 分数、s2 分数、轨迹可见率）显著趋于静态，证明该公式体系有效控制了动态物体的包含比例。Figure 7 进一步表明，SceneScribe-MVS 的相机运动分布（距离、旋转、转向次数）与原始 SceneScribe-1M 高度相似，验证了运动掩码公式在解耦相机与物体运动方面的有效性。

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/002_Table_1.jpg]]
*Table 1: Comparisons with Previous Works. SceneScribe-1M is a large-scale video dataset with comprehensive geometric and semantic annotations. In the Geometric Annotation column, Depth map, Camera Pose, and 3D Tracks are abbreviated as D., C., and P., respectively*

## 实验与关键发现

### 评估设计

为验证 SceneScribe-1M 的实用价值，作者选取了三类代表性的下游任务进行微调实验：**单目深度估计**（MoGe）、**场景重建**（VGGT 用于 3D 重建，MonST3R 用于 4D 重建）、以及**动态点跟踪**（CoTracker3 用于 2D 跟踪，SpatialTrackerV2 用于 3D 跟踪）。此外，还在 RealEstate10K 上评估了文本/姿态到视频生成任务。所有实验均采用“在 SceneScribe-1M 上微调后评估”的范式，对比基线为各模型在原始预训练权重下的表现。

### 主要结果

#### 单目深度估计

在 DIODE、ETH3D、KITTI、NYUv2、ScanNet 和 Sintel 六个基准上，使用 SceneScribe-1M 微调后的 MoGe 模型在仿射不变深度图的平均相对误差（Average Rel）上从 4.72 降至 **4.68**（Table 2）。这一改善虽然幅度有限（-0.04），但在多个不同场景的基准上一致出现，表明数据集中连续深度图标注对单目深度估计具有正向迁移作用。

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/014_Table_2.jpg]]
*Table 2: Evaluation of Monocular Depth Estimation on Representative Benchmarks*

#### 场景重建

3D 重建方面，在 CO3Dv2 和 ETH3D 上，使用 SceneScribe-1M 训练的 VGGT 将 AUC30 指标从 89.5 提升至 **89.9**（Table 3(a)）。4D 重建方面，在 Sintel 上 MonST3R 的 ATE 从 0.108 降至 **0.099**（Table 3(b)）。两项任务均获得一致增益，验证了相机姿态与深度图联合标注对几何重建任务的价值。

#### 动态点跟踪

在 TAP-Vid-DAVIS、Kinetics 和 RGB-Stacking 三个基准上，CoTracker3 的平均 AJ 指标从 76.6 提升至 **77.4**（Table 4(a)）。这一提升得益于数据集中 3D 点轨迹标注为模型提供了更丰富的运动监督信号。

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/015_Table_4.jpg]]
*Table 4: Evaluation of Dynamic Point Tracking on Representative Benchmarks*

#### 视频生成

在 RealEstate10K 上的文本/姿态到视频生成评估中（Table 5），使用 SceneScribe-1M 训练的 A3CD 模型同样展现出性能提升，具体数值需查阅原表确认。

![[assets/figures/papers/paper_list_l824_https_arxiv_org_abs_2604_07990/figures/016_Table_5.jpg]]
*Table 5: Text/Pose-to-Video Evaluation on RealEstate10K [73]*

### 消融分析：SceneScribe-MVS 采样策略

SceneScribe-MVS 子集的核心设计目标是在过滤动态物体的同时保留相机运动多样性。消融实验从物体运动度和相机运动度两个维度验证了该策略的有效性。

**物体运动度控制**（Figure 6）：采用三个指标衡量物体运动程度——s1 分数、s2 分数和轨迹可见率。结果表明，经过 SceneScribe-MVS 采样策略后，三个指标均显著趋向静态区域，且低于预设阈值。这说明该策略有效控制了动态物体的包含比例，为静态多视图任务（如 3D 重建）提供了更干净的数据。

**相机运动多样性保持**（Figure 7）：通过距离、旋转量和转向次数三个相机运动指标，比较 SceneScribe-1M 原始数据集与 SceneScribe-MVS 子集的分布。两者分布高度相似，证明解耦采样策略在过滤动态物体的同时，成功保留了原始数据中丰富的相机运动模式。

### 失败模式与局限性

1. **标注噪声传播**：所有几何与语义标注均依赖现成模型（MegaSaM、TAPIP3D、Qwen2.5-VL-72B），这些模型在复杂场景（如遮挡、透明物体、快速运动）下的错误会直接传播至数据集。当前缺乏对标注精度的系统性人工校验。

2. **场景覆盖偏差**：数据来源以公开网络视频为主，对极端环境（如恶劣天气、水下场景）、长尾专业场景（如医疗内窥镜）的覆盖不足，可能导致下游模型在这些场景中的泛化能力受限。

3. **构建成本制约扩展性**：整个标注流水线消耗约 15 万 GPU 小时（超过 1000 块 NVIDIA H20 GPU），高昂的计算成本可能限制数据集的进一步规模扩展和更新迭代。

## 定位与知识库关联

### 1. 数据构建范式定位

SceneScribe-1M 属于**大规模自动化标注数据集**路线，其核心范式是通过并行部署多个现成专有模型，对开放世界视频进行“几何+语义”联合标注。这一路线区别于两类传统工作：

- **人工标注或半自动标注数据集**（如 CO3D、RealEstate10K）：标注精度高，但规模受限，且通常只覆盖单一几何模态（如仅相机姿态或仅稀疏点云）。
- **单模态自动标注数据集**（如 SpatialVID、Sekai）：规模较大，但几何标注不全面——SpatialVID 约 2000 小时，Sekai 约 600 小时，且缺乏深度图、相机姿态与 3D 点轨迹的联合覆盖（见 Table 1）。

SceneScribe-1M 的差异化在于**同时提供连续深度图、相机姿态和一致的 3D 点轨迹**，并将标注规模推至 4191 小时（约 100 万动态场景），在规模与标注全面性两个维度上构建了新的 Pareto 前沿。

### 2. 标注模型谱系与依赖关系

数据集的标注质量直接受限于所采用的三个核心模型，理解这些模型的来源与能力边界是评估数据集适用性的前提：

- **Qwen2.5-VL-72B**：负责语义标注（结构化场景描述）。该模型属于大规模视觉-语言模型家族，其描述覆盖场景氛围、主体对象和动作（见 Figure 5），但 VLM 在细粒度空间关系、物体计数和罕见实体识别上的幻觉问题可能传播至标注。
- **MegaSaM**：负责运动掩码、相机参数和连续深度图估计。该模型是单目 SLAM 与深度估计的结合体，在动态场景下可能出现深度边缘模糊和运动边界不准确的问题。
- **TAPIP3D**：利用 MegaSaM 输出的深度和相机姿态，通过多视图重投影生成一致的 3D 点轨迹。其对 MegaSaM 的输出有强依赖，误差会级联放大。

三个模型构成串联依赖链：MegaSaM 的输出是 TAPIP3D 的输入，Qwen2.5-VL-72B 的语义标注与几何标注在逻辑上独立但在下游任务中联合使用。这一架构的优势是模块化、可替换（未来可升级任一模型），劣势是缺乏跨模态的一致性校验机制。

### 3. 解耦采样的方法论贡献

SceneScribe-MVS 子集的构建引入了一个具有方法论价值的操作——**通过多视图重投影误差解耦相机运动与物体运动**。具体而言：

1. 利用 MegaSaM 估计的深度和相机姿态，将源帧像素重投影到参考帧。
2. 计算三个误差指标：2D 重投影误差 $e_{2d}$、相对深度误差 $e_{3d}$ 和 RGB 差异 $e_{rgb}$。
3. 通过联合阈值定义运动掩码 $M_{motion} = (e_{2d} < \tau_1) \wedge (e_{3d} < \tau_2) \wedge (e_{rgb} < \tau_3)$，标记静态且标注准确的区域。

这一解耦策略的有效性由 Figure 6 和 Figure 7 的消融统计验证：SceneScribe-MVS 的物体运动指标（s1、s2、轨迹可见性比）显著趋于静态，而相机运动分布（距离、旋转、转向次数）与原始数据集高度相似。这证明该方法在**过滤动态物体的同时保留了相机运动多样性**，为需要静态场景假设的多视图任务（如 3D 重建）提供了高质量子集。

### 4. 适用边界

**适合的下游任务**（已有验证）：
- 单目深度估计（MoGe 在五个基准上 Average Rel 从 4.72 降至 4.68，Table 2）
- 3D 重建（VGGT 在 CO3Dv2+ETH3D 上 AUC30 从 89.5 升至 89.9，Table 3a）
- 4D 重建（MonST3R 在 Sintel 上 ATE 从 0.108 降至 0.099，Table 3b）
- 2D/3D 点跟踪（CoTracker3 在 TAP-Vid 上 Average AJ 从 76.6 升至 77.4，Table 4a）

**效果增益幅度较小**：上述提升均在 1% 以内或小数点后第二位，表明 SceneScribe-1M 作为辅助训练数据能提供微弱但一致的增益，而非颠覆性改进。这可能源于：（1）标注噪声部分抵消了数据规模的收益；（2）现有模型架构对大规模几何标注的利用效率有限。

**不适合的场景**：
- 极端动态视频（快速运动物体可能突破解耦采样的误差阈值，导致运动掩码失效）
- 需要像素级几何精度的任务（标注模型自身的系统误差无法通过规模消除）
- 长尾场景或极端环境（数据来源限于公开网络视频，覆盖偏差不可避免）

### 5. 局限与开放问题

**已知局限**（论文承认）：
1. **标注质量天花板**：受限于 MegaSaM、TAPIP3D 和 Qwen2.5-VL-72B 的模型能力，标注噪声和系统性偏差会传播至数据集。目前缺乏人工验证的标注精度报告。
2. **构建成本高**：整个流水线消耗约 15 万 GPU 小时（超过 1000 块 NVIDIA H20），限制了社区复现和进一步扩展。
3. **覆盖偏差**：数据来源（HD-VILA-100M、Panda-70M、Koala-36M、Pexels）以网络公开视频为主，对专业领域（医疗、工业检测）、极端天气、低光照等场景覆盖不足。

**开放问题**：
1. **多模态扩展**：当前标注限于视觉几何与语义，能否扩展至音频、热红外、激光雷达等模态，构建更全面的世界模型？
2. **标注偏差缓解**：如何通过多模型集成、一致性校验或人工抽查来降低标注模型的系统性偏差？例如，MegaSaM 在无纹理区域的深度估计错误是否会系统性地影响 3D 点轨迹的质量？
3. **解耦采样的鲁棒性**：SceneScribe-MVS 的重投影误差阈值策略在极端动态视频（如体育赛事、快速移动的车辆）中是否仍然有效？阈值的选择是否具有场景依赖性？
4. **规模收益的边际效应**：当前实验显示从 0 到 4191 小时的增益较小，进一步扩大规模是否仍能带来持续提升，还是标注噪声会形成瓶颈？

### 6. 与相关数据集的定位关系

| 数据集 | 规模（小时） | 深度图 | 相机姿态 | 3D 点轨迹 | 动态场景 | 语义描述 |
|--------|------------|--------|---------|----------|---------|---------|
| RealEstate10K | ~100 | ✗ | ✓ | ✗ | ✗ | ✗ |
| CO3D | ~50 | ✗ | ✓ | ✗ | ✗ | ✗ |
| SpatialVID | ~2000 | ✓ | ✗ | ✗ | 部分 | ✓ |
| Sekai | ~600 | ✓ | ✓ | ✗ | 部分 | ✓ |
| **SceneScribe-1M** | **4191** | **✓** | **✓** | **✓** | **✓** | **✓** |

SceneScribe-1M 在几何标注的全面性（同时覆盖深度、姿态、轨迹）和规模上均处于领先位置，但其标注精度未经人工验证，在这一维度上弱于人工标注数据集。实际使用中，建议将其作为预训练或辅助训练数据，而非精调的唯一监督来源。

## 原文 PDF

![[paperPDFs/CVPR_2026/SceneScribe_1M_A_Large_Scale_Video_Dataset_with_Comprehensive_Geometric_and_Semantic_Annotations.pdf]]
