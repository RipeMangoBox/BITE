---
title: AiOS All in One Stage Expressive Human Pose and Shape Estimation
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation.pdf
project_link: https://ttxskk.github.io/AiOS/
code_link: null
aliases:
- AAOSEHPSE
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入渐进式检测-解码框架，以人体令牌和关节令牌分别提取全局和局部特征，并利用自注意力和交叉注意力建模人体间与身体部位间关系，从而实现单阶段全帧端到端EHPS。
primary_logic: 将多人物全身网格恢复视为渐进式集合预测问题，基于DETR架构设计人体令牌和关节令牌两级查询，通过变形解码器同步进行人体检测与SMPL-X参数回归，消除了对独立检测器的依赖。
claims:
- AiOS在AGORA SMPL-X测试集上NMVE降低了9%，超越所有使用真值边界框的已有方法。
- AiOS在EHF上PVE降低了30%，在ARCTIC上PVE降低了10%，在EgoBody上PVE降低了3%。
- 在AGORA SMPL测试集上，AiOS的NMVE比最佳一阶段HPS方法BEV降低43%。
- 引入关节令牌和渐进式监督显著提升了全身网格回归精度。
---

# AiOS All in One Stage Expressive Human Pose and Shape Estimation

> [!tip] 核心洞察
> 将多人物全身网格恢复视为渐进式集合预测问题，基于DETR架构设计人体令牌和关节令牌两级查询，通过变形解码器同步进行人体检测与SMPL-X参数回归，消除了对独立检测器的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | AiOS：全合一阶段表现性人体姿态与形状估计 |
| 英文题名 | AiOS All in One Stage Expressive Human Pose and Shape Estimation |
| 会议/期刊 | CVPR 2024 |
| Links | [Project](https://ttxskk.github.io/AiOS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AiOS |
| Dataset | AGORA SMPL-X, EHF, ARCTIC, EgoBody |

> [!tip] 效果简介
> - AGORA SMPL-X 上，NMVE (All) 97.8 mm vs 107.2 mm (SMPLer-X) (-9.4 mm (≈9%))。
> - EHF 上，PVE All 45.4 mm vs OSX 64.3 mm (estimated) (-30%)。
> - ARCTIC 上，PVE All N/A (10% reduction) vs N/A (-10%)。

## 概要

表现性人体姿态与形状估计（EHPS）旨在从单张图像中恢复多人的全身三维网格，包括身体、手部和面部。现有方法普遍采用“检测-裁剪-回归”的多阶段流水线：先用现成的检测器（如Faster R-CNN）定位人体边界框，再对裁剪区域独立回归SMPL-X参数。这种范式存在两个根本性瓶颈：其一，裁剪操作切断了人体间的空间关系和全局场景上下文，导致拥挤场景下的人体间交互信息完全丢失；其二，即使后续工作将回归网络整合为单阶段（如**OSX**, Lin et al., CVPR 2023），仍依赖外部检测器提供的边界框，未能实现真正的端到端全帧推理。另一类基于身体中心热图的单阶段HPS方法（如**ROMP**, Sun et al., ICCV 2021；**BEV**, Sun et al., CVPR 2022）虽然摆脱了裁剪，但仅使用中心点附近的全局特征，缺乏对手部、面部等细粒度局部区域的建模能力，在全身网格精度上与多阶段方法存在显著差距。

针对上述问题，本文提出**AiOS**（All-in-One Stage），首个无需独立人体检测步骤的全合一阶段EHPS框架。其核心洞察在于：将多人全身网格恢复重新定义为**渐进式集合预测问题**，基于DETR的可变形注意力架构，设计人体令牌和关节令牌两级查询机制，在统一的编码器-解码器结构中同步完成人体检测与SMPL-X参数回归。具体而言，AiOS通过人体令牌提取全局位置特征以定位人体，通过关节令牌引导交叉注意力聚焦于身体、手部和面部的细粒度局部区域，并利用解码器中的自注意力机制显式建模人体间与身体部位间的关系。这种设计消除了对独立检测器的依赖，实现了从全帧图像到多人全身网格的直接端到端映射。

实验结果表明，AiOS在多个基准上取得了显著提升。在AGORA SMPL-X测试集上，NMVE降低9%，超越了所有使用真值边界框的已有方法；在EHF上PVE降低30%，在ARCTIC上降低10%，在EgoBody上降低3%。与最佳一阶段HPS方法BEV相比，AiOS在AGORA SMPL测试集上的NMVE从108.3 mm降至61.2 mm，降幅达43%。消融实验证实，关节令牌的引入和渐进式全身监督是性能提升的关键因素，而受限的注意力掩码设计（仅允许同一人体内的关节令牌间注意力）相比全注意力或仅人体间注意力方案取得了最优结果。

### 表现性人体姿态与形状估计的演进

从单张图像中恢复多人的全身三维网格，即表现性人体姿态与形状估计（Expressive Human Pose and Shape Estimation, EHPS），是计算机视觉中的一项核心挑战。该任务要求同时预测人体的姿态、手部动作和面部表情，输出SMPL-X参数模型，其参数空间包含身体、双手和下巴的53个关节旋转 $\theta \in \mathbb{R}^{53 \times 3}$、体型参数 $\bar{\beta} \in \mathbb{R}^{10}$ 以及面部表情参数 $\psi \in \mathbb{R}^{10}$。

现有方法在架构上可大致分为两类。第一类是多阶段的自顶向下方法：首先使用现成的检测器（如Faster R-CNN）定位每个人体边界框，然后裁剪出人体区域，再分别送入不同的网络回归身体、手部和面部参数。这类方法的代表性工作包括 **SMPLer-X** 和 **OSX**（Lin et al., CVPR 2023）。尽管SMPLer-X借助大规模视觉模型和使用真值边界框取得了领先性能，但其多阶段设计存在根本性缺陷：裁剪操作切断了人体与场景的全局上下文，也丢失了多人之间的空间交互信息，在拥挤场景下性能显著退化。

第二类是单阶段HPS方法，如 **ROMP**（Sun et al., ICCV 2021）和 **BEV**（Sun et al., CVPR 2022）。它们在全帧上进行预测，避免了显式的裁剪步骤，但仍依赖于身体中心热图或鸟瞰视图来定位人体。这种方法仅提取了粗粒度的全局特征，缺乏对手部、面部等细粒度局部区域的建模能力，导致全身网格回归精度不足。在AGORA SMPL测试集上，BEV的NMVE高达108.3 mm，远不能满足实际应用需求。

### 核心瓶颈：全局与局部的割裂

上述两类方法的共同瓶颈在于**全局上下文与局部细粒度特征之间的割裂**。多阶段方法虽然通过裁剪获得了局部细节，却牺牲了人体间交互和场景上下文；单阶段方法保留了全局信息，却无法有效获取手部和面部的精细特征。这种割裂使得拥挤场景下的多人全身网格恢复成为一个悬而未决的难题。

### AiOS的动机与核心洞察

AiOS的提出正是为了弥合这一鸿沟。其核心洞察是：**将多人全身网格恢复视为一个渐进式的集合预测问题**。基于DETR架构，AiOS设计了人体令牌和关节令牌两级查询机制——人体令牌负责在全帧中定位人体并提取全局特征，关节令牌则引导交叉注意力聚焦于身体关节、手部和面部的局部区域。通过变形解码器中的自注意力机制，AiOS同时建模了人体间的交互关系和身体部位间的关联，从而在单阶段、全帧、端到端的框架下实现了从粗到细的全身网格回归，彻底消除了对独立人体检测器的依赖。

## 核心方法与创新机理

AiOS 的核心创新在于将多人物全身网格恢复重新定义为**渐进式集合预测问题**，并基于 DETR 架构构建了首个真正意义上的全合一阶段（all-in-one-stage）EHPS 框架。与现有方法相比，其关键变革体现在以下三个维度。

### 1. 内置人体检测：从“先检测后回归”到“检测即回归”

传统多阶段方法（如 OSX, Lin et al., CVPR 2023）依赖现成的检测模型（如 Faster R-CNN）裁剪人体区域，再对每个裁剪区域独立回归 SMPL-X 参数。这一范式存在根本性缺陷：**裁剪操作不可逆地丢失了全局上下文和人体间交互信息**，在拥挤场景下尤为致命。

AiOS 彻底消除了这一依赖。其编码器输出的图像令牌序列通过一个 FFN 分类头直接判断每个令牌是否为“人体令牌”，并保留得分最高的 $M_h = 900$ 个令牌作为候选人体位置。这些人体令牌随后作为对象内容令牌 $\boldsymbol{T} \in \mathbb{R}^{M_h \times D}$ 输入解码器，与可学习的位置查询 $Q \in \mathbb{R}^{M_h \times 4}$ 协同工作，**将人体检测内化为网络推理的自然组成部分**，而非一个独立的前置步骤。

### 2. 双级令牌设计：全局定位与局部细粒度特征的解耦

现有单阶段 HPS 方法（如 ROMP, Sun et al., ICCV 2021；BEV, Sun et al., CVPR 2022）仅使用身体中心热图或鸟瞰视图进行粗粒度定位，缺乏对人体关节级别的细粒度特征提取能力。AiOS 通过**人体令牌与关节令牌的双级查询机制**解决了这一瓶颈：

- **人体位置令牌**（$T_{bl}$）负责定位人体在全局图像中的位置，提取全局上下文特征；
- **关节令牌**（$T_{bj}$、$T_{lhj}$、$T_{rhj}$、$T_{fj}$）通过可学习嵌入扩展，引导交叉注意力聚焦于身体关节、手部关节和面部关节的局部区域，提取细粒度特征。

消融实验证实了这一设计的有效性：添加关节令牌和渐进式全身监督后，AGORA 上的 PA-PVE 从朴素设计的 42.5 mm 降至 39.9 mm（Table 5）。

### 3. 受限注意力机制：显式建模人体间与身体部位间关系

解码器中的自注意力机制同时处理所有人体令牌，天然具备建模人体间交互的能力。但 AiOS 发现**全自由注意力反而损害性能**：Table 5 显示，所有令牌间自由注意力的 PA-PVE 为 42.5 mm，仅人体间注意力为 41.7 mm，而**受限注意力**（关节令牌仅在同一人体内交互，身体位置令牌可跨人体交互）取得了最优的 39.9 mm。

这一反直觉的发现揭示了关键设计原则：**人体间交互建模应聚焦于全局位置层面，而身体部位间的细粒度关系应在单人体内部独立建模**，避免跨人体的关节级特征混淆。

### 4. 渐进式解码：从粗到细的三阶段全身恢复

AiOS 将全身恢复过程拆解为三个递进阶段（Figure 2）：
1. **身体定位阶段**：预测粗粒度人体位置和身体边界框；
2. **身体细化阶段**：扩展身体关节令牌，提取身体局部特征，同时产生手部和面部的粗定位；
3. **全身细化阶段**：扩展手部和面部关节令牌，整合全身局部特征，回归完整 SMPL-X 参数。

消融实验表明，**仅在第 3 阶段施加 SMPL-X 监督优于全阶段监督**（PA-PVE 40.3 mm vs 42.7 mm），但在第 2、3 阶段同时监督取得最佳（39.9 mm），说明渐进式引入监督信号有助于稳定训练过程。

### 方法创新总结

| 创新维度 | 基线方法 | AiOS 方案 | 证据锚点 |
|---------|---------|----------|---------|
| 人体检测方式 | 依赖外部检测器 + 裁剪 | 编码器内置 FFN 分类人体令牌，无需独立检测器 | Section 3.3 |
| 特征提取级别 | 仅全局特征或热图索引特征 | 人体令牌（全局）+ 关节令牌（局部）双级特征 | Section 3.5 |
| 人体间交互建模 | 独立处理，丢失交互信息 | 解码器自注意力 + 受限注意力掩码 | Section 3.4, Table 5 |
| 参数回归策略 | 单步或两阶段回归 | 三阶段渐进式解码，分阶段施加 SMPL-X 监督 | Section 3.5, Table 5 |

AiOS 将多人全身网格恢复建模为**渐进式集合预测问题**，基于 DETR 架构构建了一个全合一阶段（all-in-one-stage）管线，无需独立的人体检测器即可在完整图像上同步完成人体定位与 SMPL-X 参数回归。其核心设计包含三个递进阶段：**身体定位阶段**、**身体细化阶段**和**全身细化阶段**，通过人体令牌（human token）与关节令牌（joint token）两级查询机制，逐步从粗粒度全局定位过渡到细粒度局部特征提取。

### 输入与骨干网络

输入为单张完整图像，首先通过 **ResNet-50** 骨干网络提取多尺度特征图 $F_{img}$，为后续模块提供从细节到整体的层次化视觉特征。这些特征图随后送入标准 Transformer 编码器进行长距离关系编码，得到图像内容令牌 $T_{img}' \in \mathbb{R}^{M \times D}$。编码器输出通过一个前馈网络（FFN）对每个令牌进行二分类，判断其是否属于人体区域，并保留置信度最高的 top-$M_h = 900$ 个令牌作为候选人体定位令牌 $\boldsymbol{T} \in \mathbb{R}^{M_h \times D}$，替代传统方法中依赖外部检测器生成的边界框。

### 阶段一：身体定位

身体定位阶段由前两个解码器层构成，以候选人体令牌 $\boldsymbol{T}$ 和可学习的对象位置查询 $Q \in \mathbb{R}^{M_h \times 4}$（表示边界框 $(x, y, w, h)$）为输入。解码器中的自注意力机制显式建模所有候选令牌之间的交互，捕获人体间关系；交叉注意力则从图像特征中提取全局上下文信息。该阶段输出身体位置令牌 $T_{bl}$，并通过 FFN 回归粗粒度的身体边界框，同时初步预测左手、右手和面部的位置令牌 $T_{lhl}, T_{rhl}, T_{fl}$，形成全身位置令牌的拼接表示 $T_{full} = [T_{bl}, T_{lhl}, T_{rhl}, T_{fl}]$。

### 阶段二：身体细化

身体细化阶段引入**身体关节令牌**以增强局部特征提取能力。利用可学习嵌入 $E_{bj} \in \mathbb{R}^{17 \times D}$ 将每个身体位置令牌 $T_{bl}$ 扩展为 17 个关节令牌 $T_{bj}$，分别对应人体的关键骨骼节点。该阶段的令牌集合为 $T_{bd} = [T_{bl}, T_{bj}, T_{lhl}, T_{rhl}, T_{fl}]$。解码器在此阶段通过注意力掩码约束关节令牌仅关注同一人体实例内的特征，同时保持位置令牌之间的人体间注意力，从而在捕获细粒度身体局部特征的同时不丢失全局交互信息。基于 $T_{bl}$ 和 $T_{bj}$ 回归 SMPL-X 的身体姿态与体型参数，并进一步细化手部和面部的位置定位。

### 阶段三：全身细化

全身细化阶段将手部和面部的位置令牌分别扩展为对应的关节令牌。左手关节令牌 $T_{lhj}$、右手关节令牌 $T_{rhj}$ 和面部关节令牌 $T_{fj}$ 通过各自的可学习嵌入生成，最终形成完整的全身令牌集合 $T_{wd} = [T_{bl}, T_{bj}, T_{lhl}, T_{lhj}, T_{rhl}, T_{rhj}, T_{fl}, T_{fj}]$。该阶段整合了从身体、双手到面部的全部局部特征，通过交叉注意力从图像特征中提取手部和面部的精细纹理与几何线索，最终由 FFN 输出完整的 SMPL-X 参数：姿态参数 $\theta \in \mathbb{R}^{53 \times 3}$（包含身体、双手和下巴共 53 个关节旋转）、体型参数 $\bar{\beta} \in \mathbb{R}^{10}$ 以及面部表情参数 $\psi \in \mathbb{R}^{10}$。

### 渐进式监督策略

训练过程中，模型在三个阶段均施加监督信号，但消融实验表明，仅在第二阶段和第三阶段同时施加 SMPL-X 监督可获得最优性能（PA-PVE 39.9 mm），优于全阶段监督（42.7 mm）或仅在第三阶段监督（40.3 mm）。这种渐进式监督策略使模型在粗定位阶段专注于检测任务，而在后续阶段逐步聚焦于网格回归精度。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline overview. AiOS performs human localization and SMPL-X estimation in a progressive manner. It is composed of (1) the body localization stage that predicts coarse human location; (2) the Body refinement stage that refines body features and produces face and hand locations; (3) the Whole-body Refinement stage that refines whole-body features and regress SMPL-X parameters*

### 3.1 参数化模型：SMPL-X

AiOS 回归的全身网格由 SMPL-X 模型驱动，其核心参数包括：

- **姿态参数** $\theta \in \mathbb{R}^{53 \times 3}$：包含身体、双手、下巴共 53 个关节的旋转参数（Section 3.2）。
- **体型参数** $\bar{\beta} \in \mathbb{R}^{10}$：控制人体的高矮胖瘦（Section 3.2）。
- **表情参数** $\psi \in \mathbb{R}^{10}$：驱动面部表情变化（Section 3.2）。

上述参数共同定义了从模板网格到目标人体网格的形变过程，是后续所有解码器模块回归的最终目标。

### 3.2 通用解码器架构

AiOS 将 DETR 的可变形解码器扩展至三维全身网格恢复任务。其通用解码器接收两类输入（Section 3.3 Generic Decoder）：

- **图像内容令牌** $T_{img}' \in \mathbb{R}^{M \times D}$：经过 Transformer 编码器后的图像特征序列，$M$ 为令牌数量，$D$ 为特征维度。
- **对象内容令牌** $\boldsymbol{T} \in \mathbb{R}^{M_h \times D}$：从编码器输出中经 FFN 分类筛选出的 top-$M_h$（$M_h = 900$）候选人体定位令牌，作为解码器的对象级上下文输入。
- **对象位置查询** $Q \in \mathbb{R}^{M_h \times 4}$：以边界框 $(x, y, w, h)$ 形式表示的可学习位置先验，引导解码器关注候选人体区域。

解码器通过交叉注意力在 $T_{img}'$ 中采样特征，同时通过自注意力建模令牌间关系，逐步将粗糙的位置查询精炼为精确的人体表示。

### 3.3 朴素 AiOS：全身位置解码器

在朴素设计中，AiOS 使用两个身体中心解码器进行人体定位，随后扩展出身体部位的位置令牌（Section 3.4 Whole-body-location Decoder）。全身令牌由各部位的位置令牌拼接而成：

$$T_{full} = [T_{bl}, T_{lhl}, T_{rhl}, T_{fl}]$$

其中 $T_{bl}$ 为身体位置令牌，$T_{lhl}$、$T_{rhl}$ 分别为左右手位置令牌，$T_{fl}$ 为面部位置令牌。该拼接令牌随后用于回归 SMPL-X 参数。朴素设计的核心局限在于：各部位令牌仅编码了位置信息，缺乏对关节细粒度局部特征的显式建模。

### 3.4 AiOS 完整架构：渐进式令牌扩展

为弥补朴素设计的不足，完整 AiOS 引入**关节令牌**机制，通过可学习嵌入将位置令牌扩展为包含细粒度局部特征的令牌组（Section 3.5 AiOS）。

**身体细化阶段**，使用可学习嵌入 $E_{bj} \in \mathbb{R}^{17 \times D}$ 将身体位置令牌 $T_{bl}$ 扩展为 17 个身体关节令牌 $T_{bj} \in \mathbb{R}^{M_b \times 17 \times D}$，形成详细身体令牌集合：

$$T_{bd} = [T_{bl}, T_{bj}, T_{lhl}, T_{rhl}, T_{fl}]$$

该集合同时包含全局位置特征（$T_{bl}$）和局部关节特征（$T_{bj}$），并通过交叉注意力从图像特征中采样对应关节区域的细粒度信息。解码器的自注意力模块显式建模人体间关系与身体部位间关系，同时使用注意力掩码确保关节令牌只关注同一人体的特征，避免跨人体信息污染。

**全身细化阶段**，进一步扩展手部和面部令牌。使用可学习嵌入 $E_{lhj}$、$E_{rhj}$、$E_{fj}$ 分别将左右手位置令牌和面部位置令牌扩展为对应的关节令牌，最终形成完整的人体表示令牌集合：

$$T_{wd} = [T_{bl}, T_{bj}, T_{lhl}, T_{lhj}, T_{rhl}, T_{rhj}, T_{fl}, T_{fj}]$$

该集合整合了身体、双手、面部的全部位置令牌与关节令牌，在全身细化解码器中通过交叉注意力提取多层级特征，最终由 FFN 输出头回归完整的 SMPL-X 姿态、体型和表情参数。

### 3.5 关键设计：注意力机制与渐进式监督

消融实验（Table 5）揭示了两个关键设计决策的因果效应：

- **受限注意力格式**：全注意力（所有令牌间自由交互）导致 PA-PVE 为 42.5 mm；仅人体间注意力为 41.7 mm；而 AiOS 采用的受限注意力（关节令牌仅在人体内交互，位置令牌可跨人体交互）取得最优的 39.9 mm。这表明在保持人体间上下文建模的同时，限制关节令牌的注意力范围可有效抑制噪声。
- **渐进式 SMPL-X 监督**：仅在第 3 阶段施加 SMPL-X 监督（PA-PVE 40.3 mm）优于全阶段监督（42.7 mm），但在第 2、3 阶段同时监督取得最佳 39.9 mm。这说明过早引入全身参数回归会干扰早期阶段的人体定位学习，而适度的渐进式监督能平衡定位精度与网格回归质量。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/009_Figure_5.jpg]]
*Figure 5: Attention Visualization. The green dots represent the location of the reference point, and the red dots are the sampling points*

## 实验与关键发现

### 主要定量结果

AiOS 在多个基准数据集上取得了领先的性能，尤其是在无需真值边界框的条件下，超越了多数依赖真值框的多阶段方法。

在 **AGORA SMPL‑X 测试集**上，AiOS 的 NMVE（All）达到 **97.8 mm**，相较于此前最优的 **SMPLer‑X**（107.2 mm）降低了约 **9%**（见 Table 1）。该结果在同等设置下（均使用 AiOS 自身检测框）的优势更为显著：当 SMPLer‑X 与 **OSX**（Lin et al., CVPR 2023）等整体式方法采用 AiOS 提供的边界框进行推理时，AiOS 仍以明显差距领先，表明其性能增益并非仅来自检测质量的提升，而是端到端联合优化的结果。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/003_Table_1.jpg]]
*Table 1: AGORA SMPL-X test set. † denotes the methods finetuned on the AGORA training set. ∗ denotes the methods trained on the AGORA training set only. ⋄ denotes the methods that use the AiOS’s bounding box to crop the image. The best results are colored with red, and the second-best results are colored with blue for the upper and lower parts of the table, respectively*

在 **AGORA SMPL 测试集**（仅身体网格）上，AiOS 与单阶段 HPS 方法 **BEV**（Sun et al., CVPR 2022）和 **ROMP**（Sun et al., ICCV 2021）进行了对比。以置信度阈值 0.5 过滤后，AiOS 的 NMVE 为 **61.2 mm**，相较于 BEV 的 108.3 mm 降低了 **43%**，NMJE 亦有约 40% 的改善（见 Table 2）。这一对比直接验证了“全局上下文 + 细粒度局部特征”的设计在拥挤场景下的关键作用——基于鸟瞰图或身体中心热图的单阶段方法因缺乏实例级细粒度特征而误差显著增大。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/004_Table_2.jpg]]
*Table 2: AGORA SMPL test set. † indicates that this method is fine-tuned on the AGORA training set*

在泛化能力评测上，**EHF 数据集**（未参与训练）的 PVE（All）从 OSX 的约 64.3 mm 降至 **45.4 mm**，降幅达 **30%**（见 Table 4）。此外，在 **ARCTIC**（手‑物交互场景）和 **EgoBody**（第一人称视角）上，PVE 分别降低了 **10%** 和 **3%**（见 Abstract），表明 AiOS 对视角变化和交互场景具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/006_Table_4.jpg]]
*Table 4: EHF. As EHF is absent from our training data, it serves as a valuable tool to assess the generalization ability of our models*

在 **UBody 数据集**上，AiOS 在未使用真值框的条件下取得了与使用真值框的 SMPLer‑X 可比甚至更优的结果（PA‑PVE All 32.5 mm vs. 31.9 mm，见 Table 3）。这进一步说明，AiOS 的全帧端到端设计在实际应用场景中具备替代“检测‑裁剪‑回归”范式的潜力。

### 消融实验

消融实验围绕两个核心设计因素展开：注意力格式与 SMPL‑X 监督施加方式（见 Table 5）。

![[assets/figures/papers/paper_list_l12_AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation_motion20v2/figures/010_Table_5.jpg]]
*Table 5: Ablation Studies. The upper part studies the attention format, and the bottom part studies the SMPL-X supervision manners*

**注意力格式的影响。** 实验对比了三种设置：
1. **全注意力**（所有令牌间自由交互）：PA‑PVE 为 42.5 mm，性能最差。原因是关节令牌与无关人体的特征产生错误关联，引入了跨实例噪声。
2. **仅人体间注意力**（位置令牌可跨人体交互，关节令牌不参与自注意力）：PA‑PVE 降至 41.7 mm，说明建模人体间空间关系有益，但关节令牌缺乏局部交互仍限制了精度。
3. **受限注意力**（AiOS 最终方案：位置令牌人体间交互 + 关节令牌仅与同人体的令牌交互）：PA‑PVE 进一步降至 **39.9 mm**，为最优。这验证了“全局人体间关系 + 局部人体内细粒度特征”的双层注意力设计的必要性。

**SMPL‑X 监督施加阶段的影响。** 实验对比了在不同解码器阶段施加全身网格监督的效果：
- 仅在 **第 3 阶段**（全身细化解码器）施加监督：PA‑PVE 为 40.3 mm。
- 在 **所有三个阶段** 均施加全身监督：PA‑PVE 升至 42.7 mm，性能反而恶化。推测原因是早期阶段（身体定位、身体细化）的特征尚不足以支撑精确的全身参数回归，强行监督会引入噪声梯度。
- 在 **第 2、3 阶段** 同时施加监督：PA‑PVE 达到最优的 **39.9 mm**。这表明身体细化阶段已具备足够的局部特征，此时引入 SMPL‑X 监督可提供有效的中间引导，同时避免早期阶段的噪声干扰。

**关节令牌的增益。** 从朴素 AiOS（无关节令牌，仅位置令牌）到完整 AiOS（引入身体、手部、面部关节令牌），PA‑PVE 从 42.5 mm 降至 39.9 mm（见 Table 5 中 Naive AiOS vs. Full AiOS）。关节令牌通过交叉注意力从特征图中提取关节周围的细粒度局部特征，为姿态回归提供了关键的空间线索。

### 定性分析

**Figure 3** 展示了 AiOS 与 SOTA 方法在 AGORA 和 EHF 上的可视化对比。在拥挤、遮挡场景下，多阶段方法（如 OSX、SMPLer‑X）因独立处理每个裁剪区域而容易产生人体间穿透和错误的肢体分配；AiOS 则通过解码器中的自注意力显式建模人体间关系，保持了人体间空间一致性。在 EHF 的复杂姿态下，AiOS 的手部和面部重建也更为准确，这与关节令牌提供的局部特征直接相关。

**Figure 4** 将 AiOS 与单阶段 HPS 方法（ROMP、BEV）在互联网数据上进行了对比。BEV 和 ROMP 在多人密集场景下容易出现漏检或网格漂移，而 AiOS 依赖人体令牌的全局定位能力和关节令牌的局部细化能力，在保持高召回的同时提供了更精确的网格贴合。

**Figure 5** 的可视化揭示了关节令牌的注意力行为：参考点（绿点）定位在人体关键部位附近，采样点（红点）分布在关节周围的局部区域。这直观地解释了关节令牌如何聚焦于细粒度特征，从而提升手部和面部姿态的估计精度。

### 失败模式与局限性

尽管 AiOS 在整体指标上领先，但仍存在以下可辨识的失败模式：

1. **低分辨率下的手部退化。** 当人体在图像中占比较小时，手部关节令牌的交叉注意力感受野不足以捕获足够的纹理信息，导致手指姿态出现明显偏差。这一现象在 EgoBody 等第一人称远距离场景中尤为突出，也是 PVE 仅降低 3% 的主要原因之一。
2. **极端拥挤场景的漏检。** 虽然人体令牌通过 top‑900 筛选机制保持了较高的召回，但在严重遮挡（>70% 可见区域被遮挡）的情况下，编码器产生的图像令牌可能缺乏足够的人体特征，导致分类 FFN 将其误判为背景。此时模型无法恢复该人体的网格。
3. **数据规模瓶颈。** 作者明确指出，模型性能受限于多人物真实数据集的规模。当前训练数据以合成数据（AGORA、BEDLAM）为主，真实多人物样本有限，这可能导致在真实世界复杂光照和服饰条件下的泛化不足。

### 实验设置与公平性说明

- **硬件与训练配置：** 模型在 16 块 V100 GPU 上训练，总批次大小为 32。训练分两阶段：首先在 AGORA、BEDLAM 和 COCO 上训练 60 个 epoch，随后在所有训练数据集上微调 50 个 epoch。
- **公平性措施：** 由于 AiOS 是首个全合一阶段的 EHPS 方法，缺乏同类单阶段方法进行直接对比。因此，主要对比对象为使用真值框的多阶段方法。为公平起见，AiOS 还提供了自身检测框供多阶段方法使用（见 Table 1 中 ⋄ 标记的结果）。在 AGORA SMPL 测试中，统一使用置信度阈值 0.5 过滤低分检测，以保持与 BEV 等方法的可比性。
- **指标说明：** NMVE（Normalized Mean Vertex Error）和 NMJE（Normalized Mean Joint Error）为逐顶点/关节误差的归一化值；MVE 为平均顶点误差（mm）；PA‑PVE 为 Procrustes 对齐后的顶点误差。

## 定位与知识库关联

### 一、与现有方法的谱系关系

AiOS 的核心定位是**首个全合一阶段（all-in-one-stage）表现性人体姿态与形状估计（EHPS）框架**，其设计直接回应了现有方法在架构范式上的根本性局限。

**（1）对多阶段方法的超越**

传统 EHPS 方法普遍采用自上而下的多阶段流水线：先由独立的人体检测器（如 Faster R-CNN）定位人体边界框，再对裁剪后的单人区域分别回归 SMPL-X 参数。这一范式存在两个结构性缺陷：其一，裁剪操作割裂了全局上下文，导致人体间交互信息完全丢失；其二，检测与回归的级联方式引入了误差累积。代表性工作如 **OSX**（Lin et al., CVPR 2023）虽然将身体、手部、面部回归整合为单一网络，但依然依赖外部检测器提供的边界框裁剪，本质上仍属于多阶段架构。

AiOS 通过将人体检测内化为 DETR 架构中的人体令牌（human token）分类与筛选过程，彻底移除了独立检测器这一外部依赖，实现了从全帧图像到 SMPL-X 参数的端到端单阶段推理。

**（2）对一阶段 HPS 方法的推进**

在 AiOS 之前，**ROMP**（Sun et al., ICCV 2021）和 **BEV**（Sun et al., CVPR 2022）是代表性的单阶段多人 HPS 方法。ROMP 使用身体中心热图（body-center heatmap）进行多人网格回归，BEV 则引入鸟瞰视图（bird's-eye-view）辅助 3D 定位。然而，这两类方法均存在共同的瓶颈：它们仅从身体中心位置提取单一特征向量，缺乏对细粒度局部特征（如手部关节、面部关键点）的显式建模，导致在拥挤场景和精细部位估计上性能受限。

AiOS 通过引入**关节令牌（joint-related token）** 机制——包括身体关节令牌（$T_{bj}$）、手部关节令牌（$T_{lhj}, T_{rhj}$）和面部关节令牌（$T_{fj}$）——构建了多层级特征表达。身体位置令牌负责全局上下文，关节令牌则通过交叉注意力聚焦于局部细粒度区域，从而在单阶段框架内实现了多尺度特征融合。在 AGORA SMPL 测试集上，AiOS 的 NMVE 为 61.2 mm，相较于 BEV 的 108.3 mm 降低了 43%，验证了这一设计对一阶段 HPS 方法的显著推进。

**（3）与大规模视觉模型方法的关系**

**SMPLer-X** 是当前 EHPS 领域使用真值边界框取得 SOTA 性能的方法，其优势部分源于大规模视觉基础模型的强大表征能力。AiOS 在 AGORA SMPL-X 测试集上取得了 NMVE 97.8 mm 的结果，超越了包括 SMPLer-X（107.2 mm）在内的所有使用真值框的方法。值得注意的是，AiOS 并未依赖外部大规模预训练模型，而是完全基于 ResNet-50 骨干网络和 DETR 架构训练，这表明渐进式令牌设计和注意力机制本身即具备强大的表征学习能力。

### 二、适用边界与局限

**（1）数据规模依赖**

AiOS 的性能受限于多人物真实数据集的规模。当前训练数据主要包含 AGORA、BEDLAM 和 COCO，作者明确指出增加此类数据有望进一步提升性能。这意味着在数据稀缺的特定领域（如特殊视角、极端遮挡场景），模型的泛化能力可能受限。

**（2）手部估计的分辨率瓶颈**

尽管关节令牌机制显著提升了局部特征提取能力，但在低分辨率场景下，手部姿态估计仍有提升空间。这一局限源于全帧输入中手部区域所占像素极少，即使有专门的关节令牌引导注意力，可提取的有效信息仍然有限。

**（3）任务范围限定**

当前 AiOS 仅关注单帧 EHPS，尚未扩展到人体跟踪（tracking）和单目 3D 定位（monocular 3D localization）任务。这意味着在视频时序建模和绝对深度估计方面，该框架尚未提供解决方案。

**（4）注意力机制的设计约束**

消融实验（Table 5）揭示了注意力设计的敏感性：全注意力设置（所有令牌间自由交互）反而导致性能最差（PA-PVE 42.5 mm），而 AiOS 采用的受限注意力——仅允许同一人体内的关节令牌间注意力，同时保留身体部分位置令牌的人体间注意力——取得了最优结果（PA-PVE 39.9 mm）。这表明，不加约束的令牌交互会引入跨人体的噪声干扰，框架的有效性依赖于对人体结构先验的精心编码。

### 三、开放问题

1.  **时序扩展**：如何将 AiOS 的渐进式令牌框架扩展到视频领域，实现多人物全身网格的时序一致性跟踪？这需要解决跨帧令牌匹配和运动建模问题。
2.  **手部估计增强**：在有限分辨率约束下，能否通过超分辨率辅助模块或专用的手部注意力分支进一步改善手部姿态估计精度？
3.  **数据扩展的边际收益**：引入更多多人物真实数据集后，AiOS 的性能增益曲线如何？是否存在数据多样性的饱和点？
4.  **3D 定位能力**：当前 AiOS 依赖 SMPL-X 的弱透视投影假设，如何将其升级为具备度量级深度估计能力的单目 3D 定位框架？
5.  **计算效率优化**：AiOS 使用 16 块 V100 GPU 训练，解码器包含多个阶段的令牌扩展和交叉注意力操作。在实际部署中，如何在不显著损失精度的前提下压缩令牌数量和注意力层数？

## 原文 PDF

![[paperPDFs/CVPR_2024/AiOS_All_in_One_Stage_Expressive_Human_Pose_and_Shape_Estimation.pdf]]
