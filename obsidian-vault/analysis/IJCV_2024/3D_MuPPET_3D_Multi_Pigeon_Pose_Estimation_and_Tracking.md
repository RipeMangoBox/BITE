---
title: "3D-MuPPET: 3D Multi-Pigeon Pose Estimation and Tracking"
type: paper
paper_level: A
venue: IJCV
year: 2024
pdf_ref: paperPDFs/IJCV_2024/3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking.pdf
project_link: null
code_link: https://github.com/
aliases:
- 3M
- 3M3MPPET
tags:
- IJCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过多视图二维关键点三角测量与首帧身份匹配及二维SORT跟踪相结合，无需三维真值训练即可实现交互速度的三维多动物姿态估计与身份跟踪。
primary_logic: 利用二维姿态估计和传统三角测量构建模块化流水线，允许插入任何二维姿态估计器；通过首帧动态匹配实现跨视图身份关联，再以二维跟踪维持身份，大幅降低计算开销，并支持仅使用单只鸽子或室内训练数据推广至多鸽子和户外场景。
claims:
- 3D-ViTPose*与LToHP的中位三维误差仅差1.2 mm（7.0 vs 5.8），PCK10达92.5% vs 94.3%，表明精度可比。
- 二维跟踪MOTA达0.98，HOTA 0.86，实现了高精度的身份保持。
- 在1只鸽子时，2D推理速度可达9.45 fps（内存预载），3D速度可达1.89 fps。
- 仅用室内数据训练的Wild-DLC在Wild-MuPPET数据集上中位误差为15.0 mm，展示了户外泛化能力。
---

# 3D-MuPPET: 3D Multi-Pigeon Pose Estimation and Tracking

> [!tip] 核心洞察
> 利用二维姿态估计和传统三角测量构建模块化流水线，允许插入任何二维姿态估计器；通过首帧动态匹配实现跨视图身份关联，再以二维跟踪维持身份，大幅降低计算开销，并支持仅使用单只鸽子或室内训练数据推广至多鸽子和户外场景。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D-MuPPET：多鸽子三维姿态估计与跟踪 |
| 英文题名 | 3D-MuPPET: 3D Multi-Pigeon Pose Estimation and Tracking |
| 会议/期刊 | IJCV 2024 |
| Links | [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3D-MuPPET |
| Dataset | 3D-POP |

> [!tip] 效果简介
> - 3D-POP 上，RMSE (mm) 24.0 (3D-ViTPose*) vs 14.8 (LToHP) (+9.2)；Median Error (mm) 7.0 (3D-ViTPose*) vs 5.8 (LToHP) (+1.2)；PCK10 (%) 92.5 (3D-ViTPose*) vs 94.3 (LToHP) (-1.8)。

## 概要

多动物三维姿态估计与身份跟踪是定量行为分析的核心瓶颈，尤其当群体规模超过4只个体时，实时、在线地维持跨视图身份匹配与三维重建面临巨大挑战。现有方法（如**LToHP**，Iskakov et al., ICCV 2019）依赖三维真值训练，难以灵活扩展至不同物种或野外场景。3D-MuPPET提出了一种模块化的多视图流水线，将二维关键点估计、直接线性三角测量与首帧身份匹配及二维SORT跟踪相结合，无需任何三维真值训练即可实现交互速度的多鸽子三维姿态估计与在线身份跟踪。

其核心洞察在于：将三维重建与身份关联解耦为可插拔的二维模块，通过首帧动态匹配建立跨视图全局身份，后续以轻量二维跟踪维持身份一致性，从而大幅降低计算开销，并赋予框架从单鸽子室内数据向多鸽子户外场景的泛化能力。实验表明，3D-MuPPET在3D-POP基准上与需三维真值训练的LToHP精度可比（中位误差仅差1.2 mm，PCK10达92.5%），同时推理速度提升约2.3倍（1.89 fps vs. 0.83 fps），二维跟踪MOTA达0.98。仅用室内数据训练的模型在户外Wild-MuPPET数据集上中位误差为15.0 mm，初步验证了领域迁移潜力。系统目前限制在最多10只个体，严重遮挡下的二维姿态失败和长时遮挡后的身份丢失仍是主要局限。



理解动物群体的社会行为与集体动力学，离不开对多个体三维姿态的精确、连续测量。在神经科学、行为生态学及生物力学等领域，研究者迫切需要一种能够同步捕获多只动物在三维空间中完整姿态与身份轨迹的工具，以量化个体间的交互模式、社会层级与群体决策机制。然而，这一需求在当前技术条件下仍面临显著瓶颈。

现有动物姿态估计方法大多聚焦于单一个体的二维关键点检测。以DeepLabCut、SLEAP等为代表的工具已在实验室环境中取得了令人瞩目的二维精度，但其设计范式天然缺乏对多视图三维重建与跨个体身份关联的内建支持。当场景中同时存在多只外观相似、频繁交互的动物时，如何将不同相机视图中检测到的关键点正确分配给同一三维个体，并持续追踪其身份，构成了一个尚未被充分解决的挑战。

另一方面，少数能够输出三维姿态的方法则依赖于昂贵的三维真值标注与端到端的可学习三角测量。例如，**LToHP**（Iskakov et al., ICCV 2019）通过代数三角测量与体积可学习三角测量的混合策略，在人体三维姿态估计上取得了领先精度，但其训练过程必须依赖大量三维标注数据。对于动物姿态估计而言，获取高精度的三维真值极为困难——这通常需要复杂的多相机标定、繁重的逐帧手工标注，且难以扩展到户外自然环境。这一数据依赖性使得现有方法在面对新物种或新场景时灵活性不足，无法快速部署。

此外，实时性与身份跟踪的缺失进一步加剧了实用性缺口。许多三维重建方法计算开销巨大，难以在交互速度（≥1 fps）下运行，而行为研究往往要求在线反馈以驱动闭环实验。同时，即使能够重建三维关键点，若无法将跨帧的关键点关联到正确的个体身份，所得数据对行为分析的贡献也将大打折扣。现有跟踪方案多依赖视觉重识别特征，这在动物个体外观高度相似时极易失效，且增加了额外的计算负担。

3D-MuPPET正是在这一背景下被提出，其核心动机是构建一个无需三维真值训练、能够实时运行、且内建身份跟踪能力的多动物三维姿态估计框架。该方法通过将二维姿态估计与经典多视图三角测量相结合，绕过了对三维标注的依赖；同时采用首帧身份匹配与二维SORT跟踪的策略，以极低的计算代价实现了跨视图的身份关联与持续追踪。框架的模块化设计允许灵活插入任意二维姿态估计器，使其既能受益于快速发展的二维姿态估计前沿，又为从室内到野外的领域迁移提供了可行的技术路径。



## 核心方法与创新机理

3D-MuPPET 的核心创新在于**以模块化二维流水线替代需要三维真值训练的端到端方法**，在保持可比精度的同时大幅降低训练成本与计算开销，并首次实现了多动物（>4只）在线身份保持的三维姿态估计与跟踪。

### 关键机制：从“学习三角测量”到“直接三角测量+身份匹配”

与当前最优的三维姿态估计方法 **LToHP**（Iskakov et al., ICCV 2019）相比，3D-MuPPET 在三角测量策略上做出了根本性改变：

- **LToHP**：采用代数三角测量与体积可学习三角测量相结合的方式，需要三维真值标注进行训练，计算成本高且难以泛化到新场景。
- **3D-MuPPET**：直接使用线性三角测量（Direct Linear Triangulation）配合稀疏光束平差（Sparse Bundle Adjustment）与卡尔曼滤波进行平滑，**完全不需要三维真值训练**。这一设计使得框架可以即插即用地接入任意二维姿态估计器（KeypointRCNN、DeepLabCut、ViTPose 等），训练仅需二维标注。

精度对比（3D-POP 数据集，Table 2）验证了这一策略的有效性：3D-ViTPose* 的中位误差仅比 LToHP 高出 1.2 mm（7.0 vs 5.8），PCK10 达到 92.5%（LToHP 为 94.3%），表明直接三角测量在精度损失极小的情况下换来了极大的灵活性和训练效率提升。

### 身份匹配的“首帧匹配+二维跟踪”范式

多动物三维跟踪的核心瓶颈在于跨视图的身份关联。传统方法需要在每一帧对所有视图进行组合匹配，计算复杂度随动物数量和视图数量呈指数增长。3D-MuPPET 的解决方案是：

1. **首帧动态匹配**：仅在视频的第一帧，基于 Huang et al. (2020) 的动态匹配算法，将各视图中检测到的个体关联为全局身份（Global ID）。
2. **二维 SORT 跟踪维持身份**：在后续帧中，每个视图独立运行 SORT 跟踪器（Bewley et al., 2016）维持二维身份，由于首帧已建立跨视图身份映射，二维 ID 可直接对应到全局 ID，无需逐帧进行跨视图匹配。

这一设计将跨视图身份关联的计算量从“每帧全匹配”降低为“仅首帧匹配”，是实现交互速度推理的关键。二维跟踪精度（Table 3）达到 MOTA 0.98、HOTA 0.86，表明身份保持高度可靠。

### 从室内到野外的零样本领域迁移能力

3D-MuPPET 的另一个关键创新在于其**仅需室内单鸽数据即可泛化至户外多鸽场景**。通过以下设计实现：

- **背景移除训练**：使用 SAM 对训练图像进行背景移除，迫使姿态估计器学习与背景无关的特征表示，提升户外泛化能力。
- **单鸽到多鸽的域迁移**：由于 YOLOv8 目标检测器在仅用单鸽训练时无法可靠泛化到多鸽场景，3D-MuPPET 在域迁移实验中改用 KeypointRCNN 作为姿态估计器，直接输出多实例关键点而无需独立的目标检测步骤。

在 Wild-MuPPET 户外数据集上（Table 9），仅用室内数据训练的 Wild-DLC 中位误差为 15.0 mm，验证了框架的户外泛化能力，无需额外户外标注即可获得可用的三维姿态估计结果。

### 推理速度的系统性优势

模块化设计带来了显著的推理速度提升。在完整流水线基准测试中（Table 7），3D-KeypointRCNN 的三维推理速度达到 1.89 fps，是 LToHP（0.83 fps）的 2.3 倍。二维推理在内存预载模式下（Table 6）可达 9.45 fps（单鸽，batch size 1）。这一速度优势源于：三角测量与卡尔曼滤波的计算开销远低于可学习三角测量网络，且首帧匹配策略避免了逐帧的跨视图关联计算。

### 创新边界与局限

需要指出的是，3D-MuPPET 的创新是**架构层面的范式创新**，而非单个模块的算法突破。其核心贡献在于证明：在特定应用场景下，精心设计的传统几何方法配合轻量在线跟踪，可以达到与端到端学习方法可比的精度，同时获得训练效率、推理速度和领域泛化能力的显著优势。然而，这一范式也带来了固有局限：系统依赖已标定的多相机系统，身份匹配假设首帧所有个体可见，且缺乏视觉重识别能力导致长遮挡后可能发生身份丢失。



3D-MuPPET 是一个模块化的多视图三维多动物姿态估计与跟踪框架，其核心设计理念是将二维姿态估计、三角测量与在线身份跟踪解耦为可替换的流水线模块。如图 2 所示，系统以同步多视图图像序列作为输入，输出带有全局身份标签的三维关键点序列。

### 流水线结构

框架由两大核心组件构成：**姿态估计模块**与**跟踪模块**。姿态估计模块负责从每一帧的各个视图中提取二维关键点和边界框；跟踪模块则负责跨视图的身份关联与时间维度的身份维护。

具体而言，流水线按以下步骤运行：

1. **二维姿态估计**：对每个视图独立运行二维姿态估计器，产生关键点坐标与边界框。框架支持插入任意先进的姿态估计器，文中对比了三种实现：KeypointRCNN、结合 YOLOv8 实例检测的改进版 DeepLabCut（DLC*），以及同样结合 YOLOv8 的改进版 ViTPose（ViTPose*）。其中 KeypointRCNN 以端到端方式同时输出关键点和检测框，而 DLC* 和 ViTPose* 采用自上而下范式，先由 YOLOv8 检测个体实例，再对每个实例进行单目标姿态估计。

2. **首帧身份匹配**：仅在第一帧执行跨视图的身份关联。系统基于 Huang et al. (2020) 的动态匹配算法，将各视图中检测到的个体二维身份（由 SORT 跟踪器在单视图内分配的 ID）关联为全局一致的个体身份。这一设计避免了逐帧进行昂贵的跨视图匹配，显著降低了计算开销。

3. **二维跟踪**：在首帧建立跨视图对应关系后，后续帧中每个视图独立运行 SORT 跟踪器（Bewley et al., 2016）来维持个体的二维身份。由于首帧已确定了各视图 SORT ID 与全局 ID 的映射关系，系统只需将二维跟踪结果按此映射转换为全局身份。

4. **三维三角测量**：将各视图中属于同一全局身份的二维关键点通过直接线性三角测量（Direct Linear Triangulation）结合稀疏光束平差（Sparse Bundle Adjustment）重建为三维关键点。该过程不依赖任何三维真值训练，仅需已知的多相机标定参数。

5. **卡尔曼滤波平滑**：对三角测量得到的三维姿态序列施加卡尔曼滤波，以抑制帧间噪声，提升三维轨迹的平滑性。

### 单只到多只的域迁移策略

为验证框架在训练数据受限条件下的泛化能力，3D-MuPPET 设计了单只到多只动物的域迁移实验。在该设定下，二维姿态估计模块使用仅包含单只鸽子的图像训练（从 3D-POP 数据集中筛选出仅含单一个体的帧）。值得注意的是，此时必须使用 KeypointRCNN 作为姿态估计器，因为 DLC* 和 ViTPose* 所依赖的 YOLOv8 目标检测模型——仅在单只鸽子数据上训练——无法可靠地泛化到多鸽子场景。

### 户外泛化扩展（Wild-MuPPET）

为应对从实验室环境到户外场景的域迁移，框架引入了背景移除训练策略。使用 Segment Anything Model（SAM）对训练图像进行背景分割，仅保留前景鸽子区域用于训练二维姿态估计器。由此得到的 Wild-DLC 和 Wild-ViTPose 模型无需任何户外标注即可在 Wild-MuPPET 数据集上运行。若需进一步提升精度，可在少量户外标注样本上进行微调（DLC-Fine-tuned）或从头训练（DLC-Scratch）。

### 输入输出规范

- **输入**：来自多个已标定相机的同步视频帧序列。
- **输出**：每帧中所有个体的三维关键点坐标及其全局身份标签。系统当前支持最多 10 只鸽子同时跟踪，关键点定义包含喙、鼻、左右眼、左右肩、龙骨上端、龙骨下端和尾部共 9 个语义关键点。

### 补充图表

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/002_Figure_2.jpg]]
*Figure 2: 3D-MuPPET. The framework consists of a pose estimation and tracking module, into which we can readily slot any state of the art pose estimator and tracking method. We identify all individuals in all views (blue part) based on Huang et al. (2020) in the first frame only. In the subsequent frames we track the identities (IDs) with SORT (Bewley et al., 2016). 3D-MuPPET predicts 3D poses together with IDs from multi-view image input using triangulation. For details we refer to Sec. 3.2*



3D-MuPPET 的核心设计思想是将多视图二维姿态估计、三角测量与轻量级在线身份跟踪解耦为模块化流水线，从而绕过对三维真值训练的依赖。整个框架由以下关键模块串联构成，其结构见 **Figure 2**。

### 二维姿态估计与实例检测

该模块负责从每一视图独立地提取所有个体的二维关键点坐标与边界框。框架设计为即插即用，可接入任意二维姿态估计器。文中对比了三种方案：

- **KeypointRCNN**：端到端的自顶向下检测与姿态估计模型，直接输出多实例的边界框与关键点。
- **DLC\***：将 YOLOv8 实例检测器与单实例 DeepLabCut 姿态估计器组合，先检测后估计。
- **ViTPose\***：将 YOLOv8 实例检测器与单实例 ViTPose 姿态估计器组合，结构与 DLC\* 类似。

对于从单只鸽子到多鸽子的领域迁移实验，由于 YOLOv8 在仅用单只鸽子图像训练时无法可靠泛化到多鸽子场景，框架改用 KeypointRCNN 作为姿态估计器（Sec. 3.3）。

### 三角测量与三维重建

获得各视图的二维关键点后，三维姿态通过直接线性三角测量结合稀疏光束平差计算得到。该步骤不依赖任何三维真值进行训练，与需要三维监督的 **LToHP**（Iskakov et al., ICCV 2019）形成根本性差异。三角测量后，使用卡尔曼滤波器对三维关键点序列进行平滑，以抑制逐帧三角测量引入的高频噪声（Sec. 3.2）。

### 身份匹配与二维跟踪

多视图间的身份关联是三维多动物跟踪的核心瓶颈。3D-MuPPET 采用“首帧匹配+逐帧跟踪”的策略大幅降低计算开销：

1. **首帧身份匹配**：在第一帧中，基于 Huang et al. (2020) 的动态匹配算法，将各视图内由二维跟踪器分配的局部 ID 关联为跨视图一致的全局 ID。此步骤仅在首帧执行一次。
2. **二维 SORT 跟踪**：在后续帧中，每一视图独立运行 SORT 跟踪器（Bewley et al., 2016）维持个体的局部身份。由于首帧已建立跨视图对应关系，后续帧只需保持各视图内的身份连续性即可实现三维身份跟踪，无需逐帧进行昂贵的跨视图重识别。

### 户外泛化扩展

为支持从室内到野外的领域迁移，框架引入了一个可选的背景移除预处理模块。在训练二维姿态估计器时，使用 SAM 对 3D-POP 室内图像进行背景分割，生成仅保留鸽子前景的掩膜训练数据。由此训练得到的 Wild-DLC 和 Wild-ViTPose 模型可在不依赖野外标注的情况下，直接应用于户外场景的三维姿态估计（Sec. 3.3）。

### 公式说明

本文未提供独立的数学公式推导。三维关键点 $P_{3D} \in \mathbb{R}^3$ 由多视图二维关键点 $\{p_{2D}^{(c)}\}$ 通过直接线性三角测量求解，随后经卡尔曼滤波器进行时序平滑。二维跟踪采用标准 SORT 框架，基于卡尔曼滤波预测边界框位置，并通过匈牙利算法进行逐帧数据关联。具体实现细节可参阅原文 Sec. 3.2 及所引用的原始方法文献。



## 实验与关键发现

### 核心主张与因果支撑

3D‑MuPPET 的设计围绕一个核心因果机制展开：**将三维重建与身份跟踪解耦为“首帧跨视图匹配 + 逐帧二维跟踪 + 三角测量”的模块化流水线**，从而在不依赖三维真值训练的前提下，实现多动物（>4 只）的交互速度三维姿态估计与身份保持。这一设计直接回应了领域瓶颈——现有方法（如 **LToHP**，Iskakov et al., ICCV 2019）需要三维真值训练，且难以在实时性与身份匹配上同时满足多动物场景需求。

以下关键证据链支撑了该主张的成立：

1. **精度可比性**：在 3D‑POP 测试集上，3D‑ViTPose\* 的中位三维误差仅比 LToHP 高 1.2 mm（7.0 mm vs 5.8 mm），PCK10 达到 92.5%（LToHP 为 94.3%），表明非学习的三角测量流水线在精细姿态指标上逼近有监督三维方法（Table 2，置信度 0.95）。RMSE 的差距较大（24.0 mm vs 14.8 mm），说明系统对离群误差更敏感，但中位误差和 PCK 的接近程度验证了模块化流水线的有效性。

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/004_Table_2.jpg]]
*Table 2: Quantitative Evaluation of 3D Pigeon Poses. We report the filtered (cf. Sec. 3.2) RMSE and its median (mm), PCK05 (%) and PCK10 (%) for the 3D poses on the 3D-POP test sequences. Comparison between LToHP (Iskakov et al., 2019) and 3D-MuPPET (highlighted in gray). *: We combine YOLOv8 (Jocher et al., 2023) for instance detection with single-object DLC (Mathis et al., 2018) and ViTPose (Xu et al., 2022). We also report the mean 3D inference speed for the complete pipeline in fps. For details on the inference speed we refer to Sec. 4.3. Upwards and downwards arrows represent whether a higher or lower value is better, respectively. Best results per row in bold. See text for a discussion of the...*

2. **身份跟踪的可靠性**：二维跟踪的 MOTA 达 0.98，HOTA 为 0.86（Table 3，置信度 0.98），证明 SORT 跟踪器在首帧身份匹配后能够稳定维持跨视图的身份关联。这是三维身份跟踪的基础——三维 MOTA 等指标在 Table 4 中进一步验证了该链路。

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/007_Table_3.jpg]]
*Table 3: Quantitative Tracking Evaluation in 2D. We test 20 video sequences quantitatively with the metrics specified in Sec. 4.1 and our supplementary materials. Upwards and downwards arrows represent whether a higher or lower value is better, respectively. The threshold for the confidence score of ViTPose* (cf. Sec. 3.2) is set to 0.5*

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/009_Table_4.jpg]]
*Table 4: Quantitative Tracking Evaluation in 3D. We test five sequences quantitatively with the metrics specified in Sec. 4.1. For detailed explanations on abbreviations and metrics, please refer to our supplemental material. Upwards and downwards arrows represent whether a higher or lower value is better, respectively. See text for a discussion of the results*

3. **推理速度优势**：在单只鸽子场景下，完整流水线的二维推理速度可达 9.45 fps（内存预载模式，Table 6），三维推理速度为 1.89 fps（3D‑KeypointRCNN，Table 7），相较于 LToHP 的 0.83 fps 提升约 2.3 倍。该速度优势源于流水线避免了体积式可学习三角测量的计算开销。

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/011_Table_7.jpg]]
*Table 7: 3D Inference Speed. Benchmark for the complete pipelines (including data loading, model loading, inference, data saving). We report the inference speed (fps) for the 3D models. Best results per column in bold, 3D-MuPPET versions highlighted in gray. See text for a discussion of the results*

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/010_Table_6.jpg]]
*Table 6: 2D Inference Speed. Benchmark for our in-memory pipeline using the KeypointRCNN, cf. Sec. 3.2. We benchmark our pipeline with our video sequences preloaded in memory and report values for different batch sizes*

4. **从室内到野外的泛化**：仅用室内 3D‑POP 数据训练的 Wild‑DLC 在 Wild‑MuPPET 户外数据集上中位误差为 15.0 mm（Table 9，置信度 0.95），验证了背景移除（SAM）训练策略对领域迁移的有效性。但需注意，零样本泛化的 RMSE 和 PCK 指标仍明显弱于微调后的模型（DLC‑Fine‑tuned），说明纯零样本性能有限。

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/013_Table_9.jpg]]
*Table 9: Quantitative Evaluation of 3D Pigeon Poses in Our Novel Wild-MuPPET dataset. We report RMSE and its median (mm), PCK05 (%) and PCK10 (%) for the 3D poses of pigeons in the wild, on the 100 test frames in the Wild-MuPPET dataset cf. Sec. 3.1.2. Wild-ViTPose and Wild-DLC are models trained on masked images from 3D-POP using ViTPose (Xu et al., 2022) and DLC (Mathis et al., 2018) respectively, without additional annotations from the wild. DLC-Fine-tuned and DLC-Scratch are trained on sampled images from Wild-MuPPET training set (cf. Sec. 3.1.2), with DLC-Fine-tuned using Wild-DLC as initial weights. See text for a discussion of the results*

### 方法谱系与知识库定位

3D‑MuPPET 在方法谱系上处于**二维姿态估计 + 多视图几何 + 在线跟踪**的交汇点，与以下基线形成明确对比：

- **LToHP**（Iskakov et al., ICCV 2019）：采用代数三角测量与体积式可学习三角测量相结合，需三维真值训练。3D‑MuPPET 将其替换为直接线性三角测量 + 稀疏光束平差 + 卡尔曼滤波，完全免除三维标注需求（Sec. 3.2，置信度 0.9）。这是方法创新槽位的核心差异。
- **I‑MuPPET**（单视图多鸽子姿态估计与跟踪的前置工作）：3D‑MuPPET 通过引入多视图将其扩展至三维域（Sec. 1，置信度 0.9），但身份匹配策略从逐帧跨视图匹配简化为首帧匹配 + 二维跟踪，大幅降低计算开销。
- **YOLOv8 + DLC/ViTPose** 的自上而下范式：文中将其作为可插拔的二维姿态估计模块（DLC\* 和 ViTPose\*），但明确指出 YOLOv8 在仅用单只鸽子训练时无法可靠泛化到多鸽子场景（Sec. 3.3），这是方法选择上的重要经验发现。

在知识库定位上，3D‑MuPPET 不依赖三维标注、不进行端到端学习，属于**几何驱动的模块化框架**。其贡献不在于提出新的网络架构，而在于通过流水线工程将现成组件（KeypointRCNN、ViTPose、DLC、SORT、SAM）组合为可实时运行的多动物三维姿态跟踪系统，并系统验证了从单到多、从室内到野外的迁移边界。

### 关键实验结论与图表解读

#### 二维姿态估计：精度与速度的权衡

Table 1 显示，ViTPose\* 和 DLC\* 在二维 RMSE（中位误差约 2.5 px）和 PCK10（>98%）上显著优于 KeypointRCNN（中位误差约 4.5 px，PCK10 约 93%）。但 KeypointRCNN 的推理速度（7.5 fps，Table 5）远高于 ViTPose\* 和 DLC\* 的自上而下流水线（需先运行 YOLOv8 检测）。这一权衡在三维流水线中同样成立：3D‑KeypointRCNN 速度最快但精度最低，3D‑ViTPose\* 精度最高但速度最慢（Table 2、Table 7）。

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/003_Table_1.jpg]]
*Table 1: Quantitative Evaluation of 2D Pigeon Poses. We report the RMSE and its median (px), PCK05 (%) and PCK10 (%) for estimated 2D poses on the 3D-POP test sequences. Comparison between KeypointRCNN (KP-RCNN, cf. Sec. 3.2), modified DeepLabCut (DLC*) and modified ViTPose (ViTPose*). *: We combine YOLOv8 (Jocher et al., 2023) for instance detection with single-object DLC (Mathis et al., 2018) and ViTPose (Xu et al., 2022). We also report the mean 2D inference speed for the complete pipelines in fps. For details on the inference speed we refer to Sec. 4.3. Upwards and downwards arrows represent whether a higher or lower value is better, respectively. Best results per row in bold*

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/008_Table_5.jpg]]
*Table 5: 2D Inference Speed. Benchmark for the complete pipelines (including data loading, model loading, inference, data saving). We report the inference speed (fps) for the 2D models, cf. Sec. 3.2. Best results per column in bold. See text for a discussion of the results*

#### 三维姿态估计：与 LToHP 的对比

Table 2 是核心对比表。3D‑ViTPose\* 在 PCK10 上仅落后 LToHP 1.8 个百分点（92.5% vs 94.3%），中位误差差 1.2 mm，但 RMSE 差距达 9.2 mm。这表明 3D‑MuPPET 在大多数帧上精度接近 LToHP，但在少数困难帧（如严重遮挡、快速运动）上误差显著放大。卡尔曼滤波（Sec. 3.2）部分缓解了三角测量噪声，但无法完全补偿二维姿态估计失败带来的级联误差。

#### 跟踪性能：二维与三维的联动

Table 3 的二维跟踪指标（MOTA 0.98，HOTA 0.86）表明 SORT 在鸽子场景中极为鲁棒，这得益于鸽子运动相对平滑、遮挡通常短暂。三维跟踪（Table 4）的 MOTA 和 IDS（身份交换次数）指标进一步验证了首帧匹配策略的有效性——只要首帧所有个体可见且被正确关联，后续帧的身份维护高度可靠。但这一假设也是系统的阿喀琉斯之踵（见下文失败模式）。

#### 推理速度：内存预载的潜力

Table 6 揭示了关键工程洞察：当视频序列预载入内存时，KeypointRCNN 的二维推理速度可从 7.5 fps（Table 5，含数据加载）提升至 9.45 fps（batch size 1），且批处理可进一步加速。这表明 I/O 是完整流水线的主要瓶颈之一，为实际部署提供了优化方向。

#### 领域迁移：单到多、室内到野外

Table 8 量化了从单只鸽子训练到多鸽子测试的领域偏移：KeypointRCNN 的二维 RMSE 中位误差从约 4.5 px 升至约 6.2 px，三维中位误差相应增加。这解释了为何 YOLOv8 检测器在此场景失效——检测模型的泛化失败比姿态估计器本身更严重。Table 9 的野外实验进一步表明，SAM 背景移除训练（Wild‑DLC）可将中位误差控制在 15.0 mm，但微调（DLC‑Fine‑tuned）可将其降至 10.5 mm，说明背景增强是有效的零样本策略，但不能替代目标域标注。

### 失败模式与局限性分析

文中通过 Figure 6 和 Sec. 4 的讨论系统暴露了以下失败模式：

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/015_Figure_6.jpg]]
*Figure 6: Limitations. Cropped frames of failure cases from 3D-POP (Naik et al., 2023) data for 2D pose estimation using the KeypointRCNN (cf. Sec. 3.2), due to occlusions. Blue denotes the ground truth, red denotes the prediction*

1. **遮挡导致的二维姿态估计崩溃**：Figure 6 展示了 KeypointRCNN 在鸽子身体被部分遮挡时完全丢失关键点的案例。由于三维三角测量直接依赖二维关键点，二维失败会不可逆地破坏三维重建。这是系统最致命的单点故障。

2. **首帧匹配假设的脆弱性**：身份匹配算法（Huang et al., 2020）要求第一帧所有个体在所有视图中均可见。若有个体在首帧被遮挡或未进入画面，其身份将无法建立，导致后续跟踪中该个体永久丢失或与已有 ID 混淆。文中未量化该失败率，但将其列为明确局限。

3. **SORT 的无重识别限制**：SORT 仅依赖运动模型（卡尔曼滤波预测 + IoU 匹配），不具备视觉重识别能力。在较长遮挡（如鸽子相互交错）后，身份可能发生交换（IDS，Table 4 中有量化但此处未提供具体数值）。这是三维跟踪中身份漂移的主要来源。

4. **群体规模上限**：系统目前限制最多处理 10 只鸽子，无法扩展至更大群体。该限制可能来自首帧匹配算法的计算复杂度或 SORT 在多目标密集交互下的性能退化，但文中未给出消融分析。

5. **户外零样本泛化的精度边界**：Wild‑DLC 的 RMSE（约 30 mm）显著高于室内场景，且 PCK05 仅约 50%（Table 9），表明在无目标域标注时，系统仅能捕获粗略姿态，精细行为分析仍需要微调。

### 待验证与开放问题

以下结论需读者结合具体应用场景进行验证：

- 文中未提供三维跟踪的 IDS 和 Frag 具体数值（Table 4 提及但未在可用片段中展示），需查阅原文补充材料以评估身份交换的严重程度。
- 首帧匹配失败的概率未量化，实际部署中需评估该假设在目标场景下的成立概率。
- YOLOv8 在多鸽子场景的泛化失败是经验观察，未提供定量消融（如不同训练数据组合下的检测 mAP），其根本原因（类别混淆 vs 尺度变化 vs 密集遮挡）需进一步实验确认。
- 跨物种泛化能力（如从鸽子到其他鸟类或啮齿类）未在本文中验证，属于明确开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/001_Figure_1.jpg]]
*Figure 1: 3D Multi-Pigeon Pose Estimation and Tracking (3D-MuPPET) is a framework for multi-animal pose estimation and tracking for lab (left) and outdoor data (right). Left: Estimated complex pose (beak, nose, left and right eye, left and right shoulder, top and bottom keel and tail) of pigeons recorded in a captive environment. Right: The image shows an example with three pigeons recorded outdoors with estimated 3D keypoints reprojected to camera view (colored dots)*

![[assets/figures/papers/paper_list_l1646_3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Results. Example frames from 3D-POP (Naik et al., 2023) for multi-pigeon pose estimation and tracking in 3D, reprojected to 2D view. Green lines connect the body, red lines the head keypoints. Some frames are cropped for a better view*



## 定位与知识库关联

### 1. 方法谱系：从二维到三维的模块化延伸

3D-MuPPET 并非从零构建的三维姿态估计器，而是对现有二维多动物姿态估计框架 I-MuPPET 的多视图扩展。其核心设计哲学是**构建模块化流水线**：将二维姿态估计、三角测量、身份跟踪解耦为可替换的独立模块，从而允许插入任意先进的二维姿态估计器（如 KeypointRCNN、DeepLabCut、ViTPose）和跟踪器（SORT）。

这一设计使其与需要三维真值训练的端到端方法形成鲜明对比。以 **Learnable Triangulation of Human Pose（LToHP）**（Iskakov et al., ICCV 2019）为代表的方法，通过代数三角测量与可体积学习三角测量的结合，在三维真值监督下进行训练，虽然精度较高，但训练成本和对三维标注的依赖构成了实际应用的瓶颈。3D-MuPPET 则通过**直接线性三角测量 + 稀疏光束平差 + 卡尔曼滤波**的组合，完全绕过了三维真值训练的需求（changed slot: triangulation strategy, anchor: Sec. 3.2）。

### 2. 知识库定位：填补多动物三维跟踪的空白

在动物姿态估计领域，现有工作主要集中在单一个体的二维或三维姿态估计，或少量个体的二维跟踪。3D-MuPPET 的独特贡献在于：

1. **多动物三维身份跟踪**：首次实现了无需三维标注即可对多个个体（最多10只鸽子）同时进行三维姿态估计和在线身份跟踪。其身份匹配策略——仅在首帧进行跨视图动态匹配（基于 Huang et al., 2020），随后通过各视图独立的 SORT 跟踪器（Bewley et al., 2016）维持身份——大幅降低了计算开销，使交互速度成为可能。

2. **单只到多只的领域迁移能力**：3D-MuPPET 展示了仅用单只鸽子数据训练的姿态估计器（KeypointRCNN）可直接应用于多鸽子场景，无需额外多动物标注。这一能力的边界在于：基于 YOLOv8 的自顶向下方法（DLC\*、ViTPose\*）在此迁移中失效，因为 YOLOv8 的目标检测模块无法可靠泛化到多鸽子场景（Sec. 3.3）。

3. **室内到户外的泛化潜力**：通过引入 SAM 背景移除训练策略（Wild variant），仅用室内数据训练的 Wild-DLC 在户外 Wild-MuPPET 数据集上达到了 15.0 mm 的中位误差（Table 9），展示了初步的领域泛化能力，但纯零样本性能仍然有限，需额外微调才能达到较高精度。

### 3. 适用边界与关键局限

3D-MuPPET 的适用性受以下边界约束：

- **多相机依赖**：系统严重依赖已标定的多相机系统，无法在单目或未标定设置下工作。
- **群体规模上限**：当前最多支持 10 只个体，无法扩展至更大群体。
- **首帧完整性假设**：身份匹配假设第一帧所有个体均可见；若有个体缺失或离开画面，匹配将失败，后续跟踪无法恢复其身份。
- **遮挡脆弱性**：严重的遮挡会导致二维姿态估计完全失败（Figure 6），进而破坏三维重建。SORT 跟踪器缺乏视觉重识别能力，在较长遮挡后可能发生身份丢失或交换。
- **户外精度差距**：虽然背景移除策略提供了泛化路径，但户外场景仍需额外标注微调才能缩小与室内精度的差距。

### 4. 开放问题

1. **密集遮挡下的可靠性**：当多个个体发生持续、复杂的相互遮挡时，3D-MuPPET 的二维-三维级联架构能否通过多视图冗余部分恢复？还是需要引入时序先验或生成式补全？

2. **跨物种泛化**：框架的模块化设计理论上支持替换为其他物种的二维姿态估计器，但在没有额外标注的情况下，跨物种的形态差异（关键点定义、体型比例）是否会导致三角测量和卡尔曼滤波的假设失效？

3. **YOLOv8 的泛化失效机理**：为何仅在单只鸽子图像上训练的 YOLOv8 检测器无法可靠检测多鸽子场景中的个体？这是类别无关的候选框生成问题，还是非极大值抑制策略在多实例密集分布下的固有缺陷？

4. **身份维护的增强路径**：引入视觉重识别特征（如外观嵌入）能否在保持轻量级架构的前提下，显著提升长期遮挡后的身份维护能力？计算开销与精度提升的权衡如何？

5. **轻量化与精度的折衷**：将流水线中的 KeypointRCNN 或 ViTPose 替换为更轻量的姿态估计器（如 MobileNet 系列骨干），在保持可接受精度的前提下，能否将三维推理速度推至实时（>30 fps）？



## 原文 PDF

![[paperPDFs/IJCV_2024/3D_MuPPET_3D_Multi_Pigeon_Pose_Estimation_and_Tracking.pdf]]
