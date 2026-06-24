---
title: "OmniWorld: A Multi-Domain and Multi-Modal Dataset for 4D World Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/OmniWorld_A_Multi_Domain_and_Multi_Modal_Dataset_for_4D_World_Modeling.pdf
openreview_forum_id: 1y1YFKb9pp
aliases:
- OmniWorld
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建大规模、多领域（模拟器/机器人/人类/互联网）且富含多种精确几何与语义标注的OmniWorld数据集，直接缓解了高质量时空训练数据稀缺的瓶颈。"
primary_logic: "一个覆盖多领域、集成深度、相机姿态、文本描述、光流和前景掩码的大规模数据集，不仅能够通过微调显著增强现有SOTA模型的3D重建与视频生成能力，还能作为更具挑战性的基准，有效暴露当前模型在长序列一致性和复杂动态场景中的根本缺陷。"
claims:
- "OmniWorld-Game在模态多样性和数据规模上大幅超越现有公开合成数据集（超过18M帧，覆盖深度、相机姿态、文本等多种模态）"
- "在OmniWorld上微调的DUSt3R在Sintel单目深度估计中显著优于原始DUSt3R和MonST3R（Abs Rel: 0.370 vs 0.488 vs 0.402）"
- "在OmniWorld上微调的AC3D在OmniWorld-Game基准上的相机控制视频生成TransErr从6.2788降至4.1428，提升34%"
- "OmniWorld-Game基准评估显示，VGGT在视频深度估计中表现最佳（scale&shift Abs Rel 0.194），但仍在高动态场景中出现伪影，没有单一模型能通吃所有任务"
---

# OmniWorld: A Multi-Domain and Multi-Modal Dataset for 4D World Modeling

> [!tip] 核心洞察
> 一个覆盖多领域、集成深度、相机姿态、文本描述、光流和前景掩码的大规模数据集，不仅能够通过微调显著增强现有SOTA模型的3D重建与视频生成能力，还能作为更具挑战性的基准，有效暴露当前模型在长序列一致性和复杂动态场景中的根本缺陷。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | OmniWorld：面向4D世界建模的多领域多模态数据集 |
| 英文题名 | OmniWorld: A Multi-Domain and Multi-Modal Dataset for 4D World Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1y1YFKb9pp); [Project](https://yangzhou24.github.io/OmniWorld/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | OmniWorld多领域多模态数据集构建与标注流水线 |
| Dataset | Sintel, OmniWorld-Game (Video Generation) |

> [!tip] 效果简介
> - Sintel 上，Monocular Depth Abs Rel 为 0.370 (DUSt3R fine-tuned on OmniWorld)，对比 0.488 (DUSt3R original)，变化 -0.118 (24.2% 相对降低)。
> - Sintel 上，Video Depth scale&shift Abs Rel 为 0.314 (CUT3R fine-tuned)，对比 0.537 (CUT3R original)，变化 -0.223 (41.5% 相对降低)。
> - OmniWorld-Game (Video Generation) 上，TransErr 为 4.1428 (AC3D fine-tuned)，对比 6.2788 (AC3D original)，变化 -2.1360 (34.0% 相对降低)。

## 概述

4D世界建模旨在从视觉输入中重建动态3D场景的几何、外观与运动，是实现空间智能的关键技术。然而，现有公开数据集普遍存在**动态复杂性不足、领域单一、时空多模态注释匮乏**三大瓶颈，严重制约了通用世界模型的发展。例如，多数合成数据集缺少文本描述、光流或精确相机姿态，而真实场景数据又难以规模化获取高质量标注。

针对这一困境，本文构建了**OmniWorld**——一个大规模、多领域、多模态的4D世界建模数据集。其核心思路是：通过整合模拟器（游戏引擎）、机器人操作、人类活动和互联网视频四大关键领域，并建立一套系统的自动标注流水线，为每条视频序列同步提供**深度图、相机姿态、文本描述、光流和前景掩码**五种精确标注，从数据层面直接缓解高质量时空训练数据稀缺的瓶颈。

**方法定位**：OmniWorld并非提出新的模型架构，而是一个**数据集基础设施与基准**。它通过以下机制产生价值：
- **数据飞轮**：在OmniWorld上微调现有SOTA模型，可显著提升其在真实场景中的深度估计、相机姿态估计和视频生成能力。
- **压力测试**：OmniWorld-Game基准包含高动态场景和长序列，能有效暴露当前模型在时序一致性和复杂运动中的根本缺陷。

**主要结果**：
- 在OmniWorld上微调的DUSt3R，在Sintel单目深度估计中Abs Rel从0.488降至0.370（相对提升24.2%）；CUT3R的视频深度估计scale&shift Abs Rel从0.537降至0.314（相对提升41.5%）。
- 微调后的AC3D在OmniWorld-Game基准上相机控制视频生成的TransErr从6.2788降至4.1428（提升34%）。
- 基准评估揭示：**尚无单一模型能在所有几何预测任务上同时取得最优**，VGGT虽在视频深度估计中表现最佳（scale&shift Abs Rel 0.194），但在高动态场景中仍出现明显伪影。

**局限性**：自动标注流水线在极端遮挡或颜色混淆时可能失效；数据集以游戏渲染为主，存在仿真到真实迁移的潜在差异；基准目前仅覆盖3D几何与视频生成，尚未评估物理推理等更广义的世界建模能力。

## 背景与动机

4D世界建模旨在从多模态输入中重建和生成动态3D场景，其核心瓶颈在于高质量时空训练数据的极度稀缺。现有数据集普遍存在三重缺口：**动态复杂性不足**（缺少长序列、大范围运动与复杂交互）、**领域多样性单一**（局限于自动驾驶、室内或合成游戏等孤立领域）、以及**时空多模态注释缺失**（深度、相机姿态、文本描述、光流、前景掩码等关键模态不完整）。这些缺口直接制约了通用4D世界模型的发展，使得当前SOTA方法在面对复杂动态场景时频繁出现长序列一致性崩溃和几何伪影。

从数据规模看，最大的公开合成数据集仅约4M帧（如SeKai-Game），而OmniWorld-Game单域即提供18.5M帧，整体OmniWorld超过300M帧（Table 1, Table 2）。从模态覆盖看，现有合成数据集普遍缺少文本、深度或光流等关键模态，OmniWorld则全面提供深度、相机姿态、文本描述、光流和前景掩码五种模态（Table 1）。从领域多样性看，多数数据集局限于单一领域，OmniWorld整合了模拟器（Game）、机器人（Robot）、人类（Human）和互联网（Internet）四大关键领域（Table 2, Figure 3a）。

本文的核心洞察在于：一个覆盖多领域、集成多种精确几何与语义标注的大规模数据集，不仅能够通过微调显著增强现有SOTA模型的3D重建与视频生成能力，还能作为更具挑战性的基准，有效暴露当前模型在长序列一致性和复杂动态场景中的根本缺陷。基准评估显示，VGGT在视频深度估计中表现最佳（scale&shift Abs Rel 0.194），但仍在高动态场景中出现伪影，没有单一模型能通吃所有任务（Table 3, Fig. 4）。这一发现进一步印证了构建更具挑战性和多样性的基准数据集的紧迫性。

## 核心创新

OmniWorld 的核心创新并非提出新的模型架构，而是通过构建一个**多领域、多模态、大规模**的数据集，系统性地缓解了当前4D世界建模中高质量时空训练数据稀缺的瓶颈。其创新性集中体现在对现有数据集在三个关键维度上的根本性改进（changed slots），从而解锁了通过数据驱动方式显著增强现有SOTA模型能力的可能性。

### 1. 模态覆盖度：从稀疏标注到全栈时空描述

现有公开合成数据集普遍缺少深度、文本描述或光流等关键模态，导致其无法支撑需要精细几何与语义对齐的通用世界模型训练。OmniWorld的解决方案是为所有数据提供五种核心模态的全面覆盖：**深度图、相机姿态、文本描述、光流和前景掩码**（Table 1, Table 2）。

这一全栈标注体系并非简单堆砌，而是通过一套精心设计的自动化流水线实现（Figure 2）。其中，**相机姿态标注**采用两阶段策略——先用VGGT/DroidCalib进行粗估计，再利用CoTracker3进行稠密追踪与束调整精化，在Sintel上将ATE从0.167降至0.082（Table 11）。**前景掩码生成**则根据领域特性自适应选择RoboEngine+SAM2（机器人数据）或Grounding DINO+SAM（游戏数据）的组合，有效抑制了静态背景的误分割（Figure 13）。这种模态完整性使得OmniWorld不仅能支撑深度估计和相机标定等传统任务，还能直接服务于文本驱动的视频生成与动态场景理解。

### 2. 数据规模：从百万级到千万级的量级跨越

在数据规模上，OmniWorld实现了对现有最大公开合成数据集的量级超越。仅OmniWorld-Game子集即包含**18.5M帧**，而此前最大的同类数据集SeKai-Game仅约4M帧（Table 1）。整体OmniWorld数据集规模超过**300M帧**（Table 2）。

这一规模优势直接转化为下游任务的性能增益。在OmniWorld上微调的**DUSt3R**在Sintel单目深度估计中，Abs Rel从原始模型的0.488降至0.370，相对提升24.2%（Table 5）；微调后的**CUT3R**在Sintel视频深度估计中，scale&shift Abs Rel从0.537降至0.314，相对提升41.5%（Table 6）。在视频生成任务中，微调后的**AC3D**在OmniWorld-Game基准上的TransErr从6.2788降至4.1428，提升34%（Table 7）。这些结果表明，大规模高质量数据能够有效弥补现有模型在动态场景理解与长序列一致性上的不足。

### 3. 领域多样性：从单一域到四域融合

多数现有数据集局限于单一领域（如合成、自动驾驶、室内），导致模型在跨域泛化时性能骤降。OmniWorld首次整合了**模拟器、机器人、人类、互联网**四大关键领域的数据（Table 2），覆盖了从受控渲染到真实世界采集的完整谱系。

这种多域融合的因果机制在于：模拟器数据提供精确的地面真值标注，机器人数据引入操作场景的物理交互，人类数据捕捉自然行为模式，互联网数据则贡献开放世界的视觉多样性。四域协同使得在OmniWorld上微调的模型展现出更强的跨域迁移能力——例如，微调后的DUSt3R不仅在Sintel上优于原始模型，在Bonn、KITTI和NYUv2等真实数据集上同样取得一致提升（Table 5）。同时，OmniWorld-Game基准的评估也暴露了当前模型的根本缺陷：**没有任何单一模型能在所有任务上同时取得最优**，VGGT在视频深度估计中表现最佳（scale&shift Abs Rel 0.194），但在高动态场景中仍出现明显伪影（Table 3, Figure 4），这为下一代通用世界模型的设计提供了明确方向。

> **需手动验证**：论文未提供venue和year信息，若需在正式引用中标注发表来源，请自行查证补充。

## 整体框架

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/004_Figure_2.jpg]]
*Figure 2: OmniWorld acquisition and annotation pipeline. We collect raw data from diverse domains and apply a video slicing filter to obtain high-quality RGB sequences. These sequences are then processed through a suite of specialized pipelines to generate multi-modal annotations, including text captions, depth maps, camera poses, foreground masks, and optical flow*

OmniWorld 的数据构建遵循一条统一的“采集—过滤—标注”流水线，将来自四个异构领域的原始数据转化为富含五种模态的高质量训练与评测资源。其核心设计逻辑是：**先通过视频切片过滤器保障时序质量，再针对不同模态的物理特性，部署差异化的自动标注模块，最终形成多模态对齐的片段数据集**。

### 流水线总览

整个流水线由六个核心模块串联而成，如图 Figure 2 所示：

1. **多领域原始数据采集**
   从模拟器（OmniWorld-Game，通过 ReShade 抓取渲染深度、OBS 同步录制 RGB）、机器人操作平台、人类活动视频和互联网视频四个领域收集原始 RGB 序列。不同来源的数据在帧率、分辨率和场景动态上差异显著，构成了数据多样性的基础。

2. **视频切片过滤器**
   这是保障下游标注质量的第一道关卡。该模块对原始长视频进行帧级质量评估，自动剔除纹理贫乏、严重欠曝、动态遮挡和运动模糊等低质帧（见 Figure 11），并将剩余高质量片段切分为固定长度的视频序列。这一步直接决定了相机姿态标注等模块的输入可靠性。

3. **深度标注模块**
   采用按数据源适配的策略：
   - 对游戏渲染数据，直接从渲染管线抓取真实深度；
   - 对已有公开深度标注的数据集，使用 Depth Anything 进行精化；
   - 对双目或多目数据，使用 FoundationStereo 估计深度。
   这一分层策略在保证标注精度的同时，最大化利用了不同来源的先验信息。

4. **前景遮罩生成模块**
   针对动态场景中的运动主体生成精确的二值遮罩，服务于相机姿态估计的背景提取和动态建模研究：
   - 机器人数据：RoboEngine 生成关键帧初始遮罩，SAM2 进行时序追踪与融合；
   - 游戏数据：Grounding DINO 进行开放词汇检测，SAM 生成精细分割。
   该模块的输出直接作为相机姿态标注流水线中“静态背景区域”的掩码输入。

5. **相机姿态标注模块**
   这是流水线中技术复杂度最高的模块，采用**两阶段粗到精**策略：
   - **粗估计阶段**：利用 VGGT 或 DroidCalib 在前景遮罩提取的静态背景区域上估计初始相机姿态；
   - **精化阶段**：引入 CoTracker3 进行稠密点追踪，结合束调整对粗姿态进行全局优化，显著提升几何一致性。
   表 Table 11 和 Table 12 的消融实验验证了该两阶段设计的关键作用：在 Sintel 基准上，ATE 从 0.167 降至 0.082，重投影误差 <1 像素的对应点比例从 69.85% 提升至 78.36%。

6. **文本描述与光流生成模块**
   - **文本描述**：基于 Qwen2-VL-72B-Instruct 的多视角视觉语言模型，为每个视频片段自动生成场景级文本描述；
   - **光流**：使用 DPFlow 在原始分辨率下生成稠密光流场。
   这两个模块为数据集提供了语义和运动维度的补充标注。

### 模块间的依赖与数据流

流水线中存在明确的依赖关系：**视频切片过滤器**是所有后续模块的前提条件；**前景遮罩**的输出是相机姿态估计中背景区域提取的关键输入；**深度、相机姿态和前景遮罩**三者共享同一 RGB 序列，但在标注过程中相互独立，仅在最终的多模态对齐阶段进行时间戳同步。

这种模块化设计使得 OmniWorld 能够灵活扩展——当引入新的数据领域或新的标注模态时，只需替换或新增相应的模块，而不影响整体流水线的稳定性。

## 核心模块与公式推导

OmniWorld的核心贡献在于其大规模多模态标注流水线，而非提出新的算法模型。该流水线由六个关键模块构成，协同工作以从多领域原始视频中生成高质量的时空标注。

### 视频切片过滤器 (Video Slicing Filter)

此模块是流水线的入口，负责帧级质量评估与视频分段。其核心机制是自动检测并丢弃低质量帧，包括纹理贫乏、严重欠曝、动态遮挡和运动模糊等情况（见 Figure 11）。这一预处理步骤对于保证后续相机姿态标注等模块的输入质量至关重要，因为低质帧会严重干扰几何估计的稳定性。

### 深度标注 (Depth Annotation)

深度标注策略根据数据来源采用差异化方案：
- **游戏数据**：通过 ReShade 等工具在渲染过程中直接抓取深度缓冲，获得像素级精确的真值深度。
- **公有机深度数据**：对已有深度初值的数据，使用 Depth Anything 进行优化精炼。
- **双目/多目数据**：利用 FoundationStereo 进行稠密深度估计。

这种分层策略在保证标注精度的同时，最大化利用了不同来源数据的固有特性。

### 前景掩码生成 (Foreground Mask Generation)

动态前景分割是处理非静态场景的关键。流水线同样采用领域适配策略：
- **机器人数据**：利用 RoboEngine 在关键帧生成初始掩码，随后通过 SAM2 进行时序追踪与融合。
- **游戏数据**：采用 Grounding DINO 进行开放词汇检测，结合 SAM 生成精细分割掩码。

与 SegAnyMo 的定性对比（Figure 13）表明，该流水线能更精确地追踪和分割动态主体，有效抑制了静态背景的误分割。但需注意，在极度拥挤或颜色混淆的场景中，该模块仍可能出现漏检或语义泄露（Figure 14）。

### 相机姿态标注 (Camera Pose Annotation)

这是流水线中技术最复杂的模块，采用两阶段精化策略：

1. **粗估计阶段**：利用前景掩码聚焦于静态背景区域，使用 VGGT 或 DroidCalib 进行初始相机姿态估计。
2. **精化阶段**：通过 CoTracker3 进行稠密点追踪，结合束调整（Bundle Adjustment）对初始姿态进行全局优化。

该流水线的有效性在 Sintel 基准上得到验证：ATE 从 0.167 降至 0.082，RPE 旋转误差从 0.491 降至 0.246，提升超过 50%（Table 11）。在 8,345 对帧上的几何一致性评估显示，平均重投影误差为 1.09 像素（DroidCalib 为 1.30），误差小于 1 像素的对应点比例从 69.85% 提升至 78.36%（Table 12）。

### 文本描述生成 (Text Captioning)

基于 Qwen2-VL-72B-Instruct 视觉语言模型，采用半自动多视角描述生成策略。通过提示工程优化，为视频片段生成场景级文本描述，覆盖环境、物体、动作和相机运动等信息。Figure 3(c) 展示了描述文本的 token 长度分布。

### 光流生成 (Optical Flow Generation)

使用 DPFlow 在原始分辨率下生成稠密光流场，为视频帧间的像素级运动提供精确标注。这一模态对于理解和建模动态场景中的运动模式至关重要。

### 公式与理论基础

本文作为数据集工作，未提出新的数学公式或算法推导。各模块所依赖的底层方法（如束调整、稠密光流估计、视觉语言模型推理等）均基于现有成熟技术，其数学原理可参见相应原始文献。流水线的核心创新在于将这些技术有机整合，形成一套可扩展、高质量的多模态标注体系，而非对单一算法的理论突破。

## 实验与分析

### 基准评估：暴露当前模型的根本缺陷

OmniWorld-Game基准的设计目标不仅是提供测试集，更是作为一面“照妖镜”，暴露当前SOTA模型在长序列一致性和复杂动态场景中的根本缺陷。评估结果印证了这一设计意图：**没有单一模型能在所有任务上同时取得最优**。

**深度估计**方面，Table 3汇总了单目与视频深度估计在OmniWorld-Game上的表现。单目深度估计中，**MoGe-2**取得最佳定量结果（Abs Rel 0.401, δ<1.25 0.589），但视频深度估计的领先者是**VGGT**（scale&shift Abs Rel 0.194），其在精度与推理效率（FPS）上均展现出优势。然而，Figure 4的定性对比揭示了关键问题：VGGT在高动态场景中仍会产生明显的深度伪影，表明现有模型对复杂运动的时空建模能力不足。

**视频生成**方面，Table 4的相机控制视频生成评估显示，以图像为条件的模型中**CamCtrl**表现最佳（TransErr 1.2882, RotErr 0.2022, CamMC 1.3856），而以文本为条件的**AC3D**则几乎无法遵循相机轨迹，定量与定性得分均较差（Figure 5）。这揭示了文本条件在精确相机控制上的天然劣势，以及动态场景下相机-内容解耦的难度。

### 微调验证：OmniWorld作为训练数据的价值

OmniWorld的核心价值在于其作为高质量训练数据的能力。通过在OmniWorld子集上微调多个SOTA基线模型，验证了数据集对下游任务的显著提升效果。

**单目深度估计**（Table 5）：在Sintel基准上，经OmniWorld微调的**DUSt3R**的Abs Rel从原始模型的0.488降至0.370（相对降低24.2%），且显著优于专门针对动态场景设计的**MonST3R**（Abs Rel 0.402）。在Bonn、KITTI、NYUv2等真实场景数据集上，微调模型同样保持一致的提升趋势，表明OmniWorld的多领域数据具有良好的泛化能力。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/012_Table_5.jpg]]
*Table 5: Comparison of original and fine-tuned models for monocular depth estimation on Sintel (Butler et al., 2012), Bonn (Palazzolo et al., 2019), KITTI (Geiger et al., 2013) and NYUv2 (Silberman et al., 2012). * denotes models that have been fine-tuned on OmniWorld*

**视频深度估计**（Table 6）：提升更为显著。经微调的**CUT3R**在Sintel上的scale&shift Abs Rel从0.537降至0.314（相对降低41.5%），δ<1.25从0.270提升至0.565。Figure 9的定性结果显示，微调后模型能恢复更精细的几何细节，生成更准确的深度图。

**相机控制视频生成**（Table 7）：经OmniWorld微调的**AC3D**在OmniWorld-Game基准上的TransErr从6.2788降至4.1428（提升34%），在RealEstate10K上也从3.4847降至2.8648。Figure 10的可视化证实，微调显著增强了模型遵循相机轨迹的能力，并提升了运动物体的时序一致性。这一结果与**He et al., 2025a**的发现一致，即动态数据对改善相机控制至关重要。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/014_Table_7.jpg]]
*Table 7: Comparison of original and fine-tuned models for camera-controlled video generation evaluation on RealEstate10K (Zhou et al., 2018) and OmniWorld-Game benchmark. * denotes models that have been fine-tuned on OmniWorld*

### 标注流水线的消融验证

OmniWorld的标注质量通过多项消融实验得到验证：

**深度标注的下游验证**（Table 10）：使用OmniWorld精化深度标注预训练的**FP3**策略，在四项真实世界机器人操作任务中的成功率显著高于使用原始DROID深度的模型。例如，Stack Cups任务的成功率从10%提升至35%，直接证明了精化深度标注对具身智能任务的实用价值。

**相机姿态标注的精度验证**：Table 11显示，提出的两阶段流水线在Sintel基准上将ATE从VGGT基线的0.167降至0.082，RPE旋转从0.491降至0.246，提升超过50%。Table 12进一步在8,345对帧上进行几何一致性评估：平均重投影误差从DroidCalib的1.30像素降至1.09像素，误差小于1像素的对应点比例从69.85%提升至78.36%。Figure 12的定性对比直观展示了累积点云的一致性改善——DroidCalib在静态结构上出现明显的重影与错位，而提出流水线的重建结果更为清晰。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/029_Table_11.jpg]]
*Table 11: Pose estimation performance on the Sintel benchmark. Comparison between the baseline VGGT and our full annotation pipeline*

**前景遮罩的质量对比**（Figure 13）：与**SegAnyMo**相比，OmniWorld的前景遮罩流水线能更精确地分割运动主体，有效抑制静态背景的误分割。这对后续的相机姿态估计至关重要，因为姿态优化依赖静态背景区域。

**视频切片过滤的有效性**（Figure 11）：多阶段过滤管道能可靠地剔除纹理缺失、严重欠曝、动态遮挡和运动模糊等低质量帧。这些帧若不被过滤，将直接导致相机姿态标注失败或精度下降。

### 失败模式与局限性

尽管OmniWorld在多数场景下表现优异，但分析揭示了若干需要关注的失败模式：

1. **前景遮罩的边界情况**（Figure 14）：在极度拥挤场景或前景与背景颜色高度混淆时，自动分割流水线可能出现漏检或语义泄露。这会间接影响依赖静态背景假设的相机姿态估计精度。

2. **相机姿态的极端动态失效**：标注流水线假设场景中存在足够的静态背景区域。当背景被大面积遮挡或场景整体处于极端动态中时，该假设被打破，可能引入不可忽视的姿态误差。

3. **微调的局部不稳定性**（Table 8）：经OmniWorld微调的CUT3R在相机姿态估计中，ATE和RPE trans指标一致改善，但RPE rot在部分基准上出现退化（如ScanNet上从0.288升至0.324）。这可能源于预训练数据与OmniWorld细调数据之间的分布差异，需进一步研究优化策略。

4. **仿真到真实的迁移差距**：OmniWorld-Game主要源自游戏渲染数据，尽管微调后在真实场景基准上展现出良好的泛化能力，但某些真实世界的物理特性（如复杂光照、非刚性形变）仍可能构成挑战。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 3 | VGGT在视频深度估计中综合最优（scale&shift Abs Rel 0.194），但无单一模型通吃所有任务 |
| Table 4 | CamCtrl在相机控制视频生成中表现最佳（TransErr 1.2882），AC3D文本条件几乎无法控制相机 |
| Table 5 | OmniWorld微调DUSt3R在Sintel单目深度上超越原始模型24.2%，超越MonST3R |
| Table 7 | OmniWorld微调AC3D的TransErr降低34%，动态数据对相机控制至关重要 |
| Table 10 | 精化深度标注使机器人操作成功率大幅提升（Stack Cups: 10%→35%） |
| Table 11 | 相机姿态流水线将ATE从0.167降至0.082，RPE旋转降低约50% |
| Figure 4 | VGGT在高动态场景中出现深度伪影，长序列一致性仍是瓶颈 |
| Figure 13 | 提出前景遮罩流水线优于SegAnyMo，有效抑制静态背景误分割 |

### 补充图表

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/002_Table_1.jpg]]
*Table 1: Comparisons between OmniWorld-Game and existing synthetic datasets. OmniWorld-Game surpasses existing public synthetic datasets in modal diversity and data scale*

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_1y1YFKb9pp/figures/003_Table_2.jpg]]
*Table 2: OmniWorld structure. A smiling face ( ) indicates the modality is newly (re-)annotated by us, a green check (✔) denotes ground-truth data that already exists in the original dataset, and a red cross (✗) marks missing modalities*

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有4D世界模型的发展受制于一个根本性瓶颈：**高质量时空训练数据的稀缺**。具体而言，当前公开数据集普遍缺乏动态复杂性、多领域多样性以及精细的时空多模态注释（深度、相机姿态、文本描述、光流等）。例如，最大的公开合成数据集仅约4M帧（如SeKai-Game），且模态覆盖不完整。OmniWorld通过构建一个覆盖模拟器、机器人、人类活动、互联网视频四大领域、总量超300M帧的大规模数据集，直接缓解了这一数据瓶颈。

### 与现有数据集的差异定位

OmniWorld相较于现有数据集，在三个关键维度上实现了系统性改进：

**模态覆盖度。** 现有合成数据集普遍缺少文本、深度或光流等关键模态。OmniWorld全面提供深度、相机姿态、文本描述、光流和前景掩码五种模态（Table 1, Table 2）。

**数据规模。** OmniWorld-Game子集即含18.5M帧，整体OmniWorld超300M帧，远超现有最大公开合成数据集的约4M帧规模（Table 1, Table 2）。

**领域多样性。** 多数数据集局限于单一领域（如合成渲染、自动驾驶、室内扫描），OmniWorld首次将模拟器、机器人、人类、互联网四大关键领域的数据整合到统一框架下（Table 2）。

### 与基线方法的关系

OmniWorld作为数据集工作，其核心价值体现在对现有SOTA模型的**增强能力**和**暴露缺陷**两个层面。

#### 3D几何预测基线的增强

在单目深度估计任务上，OmniWorld微调的**DUSt3R**（Wang et al., 2024c）在Sintel基准上达到Abs Rel 0.370，显著优于原始DUSt3R的0.488和**MonST3R**（Zhang et al., 2024）的0.402（Table 5）。在视频深度估计中，微调后的**CUT3R**（Wang et al., 2025b）在Sintel上的scale&shift Abs Rel从0.537降至0.314，相对提升41.5%（Table 6）。这些结果表明，OmniWorld提供的多样化时空标注能够有效弥补现有模型在动态场景理解上的不足。

#### 视频生成基线的增强

在相机控制视频生成任务上，OmniWorld微调的**AC3D**（Bahmani et al., 2024）在OmniWorld-Game基准上的TransErr从6.2788降至4.1428，提升34%（Table 7）。这一改善验证了He et al.（2025a）关于动态数据对相机控制至关重要的发现。相比之下，**CamCtrl**（He et al., 2024）作为图像到视频生成基线，在OmniWorld-Game基准上展现出更好的定量性能（TransErr 1.2882, RotErr 0.2022, CamMC 1.3856, Table 4），但AC3D经过OmniWorld微调后差距显著缩小。

#### 暴露模型根本缺陷

OmniWorld-Game基准评估揭示了当前SOTA模型的关键弱点：**VGGT**在视频深度估计中表现最佳（scale&shift Abs Rel 0.194），但仍在高动态场景中出现伪影；没有任何单一3D几何基础模型能在所有任务上同时取得最优（Table 3, Figure 4）。这暴露了当前模型在长序列一致性和复杂动态场景理解上的根本性不足。

### 标注流水线的技术贡献

OmniWorld的标注流水线本身构成独立的技术贡献：

**相机姿态标注流水线**采用两阶段策略（VGGT/DroidCalib粗估 + CoTracker3稠密追踪与束调整精化），在Sintel上将ATE从0.167降至0.082，RPE旋转从0.491降至0.246，提升超过50%（Table 11）。在8,345对帧上的几何一致性评估显示，平均重投影误差为1.09像素（DroidCalib为1.30），<1像素的对应点比例从69.85%提升至78.36%（Table 12）。

**深度标注精化**在下游机器人操作任务中得到验证：使用OmniWorld精化深度标注预训练的FP3，在四项真实世界操作任务中的成功率显著高于使用原始DROID深度的模型（如Stack Cups任务35% vs 10%，Table 10）。

**前景遮罩流水线**结合RoboEngine+SAM2（机器人数据）或Grounding DINO+SAM（游戏数据），在动态场景中产生比SegAnyMo更精确的主体分割，有效抑制了静态背景的误分割（Figure 13）。

### 适用边界与已知局限

**仿真到真实差异。** 数据集主要源自游戏渲染和部分真实场景，尽管覆盖了多领域，仍存在sim-to-real gap的风险，可能限制某些真实世界应用的直接迁移。

**动态场景标注鲁棒性。** 自动前景掩码流水线在极度拥挤或颜色混淆时可能失败（漏检或语义泄露），可能影响少数场景的相机姿态精度（Figure 14）。相机姿态标注依赖静态背景假设，在背景大面积被遮挡或极端动态下可能引入误差。

**基准覆盖范围。** 基准测试目前仅覆盖3D几何预测与相机控制视频生成，尚未评估如物理推理、因果理解等更广义的世界建模能力。

**文本标注质量。** 文本描述由视觉语言模型（Qwen2-VL-72B-Instruct）自动生成，虽经提示优化，仍可能存在不准确或幻觉内容。

### 开放问题

1. **长序列一致性与复杂动态建模。** 当前无单一3D几何基础模型能在OmniWorld-Game的所有任务上同时取得最优，如何设计模型以更好地应对长序列一致性和复杂动态仍待解决。

2. **极端场景标注鲁棒性。** 对于极端遮挡和稠密人群等场景，如何进一步提升自动标注的鲁棒性？

3. **向通用世界模型演进。** 如何利用OmniWorld的丰富标注推动更通用的世界模型发展（例如结合物理模拟与因果推理）？

4. **微调稳定性。** 微调后部分指标（如相机姿态RPE rot）改善不稳定，是否因预训练与细调数据分布差异导致，如何进一步优化？

## 原文 PDF

![[paperPDFs/ICLR_2026/OmniWorld_A_Multi_Domain_and_Multi_Modal_Dataset_for_4D_World_Modeling.pdf]]
