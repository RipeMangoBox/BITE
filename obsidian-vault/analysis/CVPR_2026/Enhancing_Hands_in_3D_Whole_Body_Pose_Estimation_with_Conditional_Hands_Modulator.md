---
title: Enhancing Hands in 3D Whole-Body Pose Estimation with Conditional Hands Modulator
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Enhancing_Hands_in_3D_Whole_Body_Pose_Estimation_with_Conditional_Hands_Modulator.pdf
project_link: "https://mks0601.github.io/Hand4Whole-plus-plus"
code_link: null
aliases:
- EH3WBPECHM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: CHAM模块：通过从冻结的手部姿态估计器提取的手部特征，以空间对齐的方式调节冻结的全身ViT特征流，从而改善手腕方向预测而不影响预训练模型的泛化能力。
primary_logic: 通过冻结的预训练模型，利用轻量级特征调制（CHAM）注入手部特有信息以提升手腕方向的准确性和生理连贯性，同时通过可微刚性对齐直接转移手指关节和手部形状，既保留了手部估计器的精细度又维持了全身结构一致性。
claims:
- 在全身和双手数据集的综合比较中，Hand4Whole++在AGORA、ARCTIC、EHF、IH26M、ReIH、HIC上均取得最低MPVPE/MRRPE（例如AGORA 76.84/49.71），超越了原始SMPLer-X、其微调版本以及手部专用WiLoR。
- 在AGORA上的组合策略消融表明，基于CHAM的特征调制（Ours）在全身MPVPE上达到76.88 mm，手部50.56 mm，明显优于直接分配手腕方向或直接替换手部网格。
- 手指关节和手部形状转移在IH26M、ReIH、HIC上将手部MPVPE分别降低至9.40、7.98、17.72 mm。
- MANO手部模型比SMPL-X手部具有更强的形状表达能力，与3D扫描的点对点误差更低（1.34 mm vs 1.98 mm）。
---

# Enhancing Hands in 3D Whole-Body Pose Estimation with Conditional Hands Modulator

> [!tip] 核心洞察
> 通过冻结的预训练模型，利用轻量级特征调制（CHAM）注入手部特有信息以提升手腕方向的准确性和生理连贯性，同时通过可微刚性对齐直接转移手指关节和手部形状，既保留了手部估计器的精细度又维持了全身结构一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用条件手部调制器增强三维全身姿态估计 |
| 英文题名 | Enhancing Hands in 3D Whole-Body Pose Estimation with Conditional Hands Modulator |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14726) · [Project](https://mks0601.github.io/Hand4Whole-plus-plus) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Hand4Whole++ |
| Dataset | AGORA, ARCTIC, EHF, IH26M |

> [!tip] 效果简介
> - AGORA 上，Full-body MPVPE / Hand MPVPE (mm) 76.84 / 49.71 vs SMPLer-X (see Table 4)。
> - ARCTIC 上，MPVPE / MRRPE (mm) 45.95 / 25.03 vs SMPLer-X (see Table 4)。
> - EHF 上，MPVPE / MRRPE (mm) 61.24 / 33.43 vs SMPLer-X (see Table 4)。

## 概要

### 问题瓶颈

三维全身姿态估计面临一个结构性矛盾：全身估计器（如 **SMPLer-X**, Cai et al., NeurIPS 2023）在全身数据集上训练时，手部姿态多样性极为有限，导致手指细节与手腕方向预测能力不足；而手部专用估计器（如 **WiLoR**, Potamias et al., CVPR 2025）虽能精细恢复手部，却缺乏全身上下文，难以处理双手交互和遮挡场景。更关键的是，直接组合两类模型——例如将手部网格简单拼接到全身网格上——会因手腕方向与上臂运动链不一致而产生解剖学上不合理的姿态配置。

### 核心方法

**Hand4Whole++** 提出了一种模块化框架，通过冻结的预训练模型与轻量级特征调制来化解上述矛盾。其核心组件是 **CHAM（Conditional Hands Modulator，条件手部调制器）**：它从冻结的手部姿态估计器（WiLoR）中提取手部 ViT 特征，以空间对齐的方式注入冻结的全身 ViT 特征流（SMPLer-X），从而在不破坏预训练模型泛化能力的前提下，显著改善手腕方向预测的准确性与生理连贯性。同时，通过可微刚性对齐，将手部估计器预测的手指关节参数 $\theta_{\mathrm{rh}}, \theta_{\mathrm{lh}}$ 与手部形状参数 $\beta_{\mathrm{rh}}, \beta_{\mathrm{lh}}$ 直接转移至全身网格，既保留了手部估计器的精细度，又维持了全身结构一致性。

### 方法谱系与知识库定位

该工作属于**冻结预训练模型的模块化特征调制**范式的典型代表。与此前方法相比：

- 相较于早期直接组合身体与手部网络的方式（如 **FrankMocap**, Rong et al., ICCVW 2021），Hand4Whole++ 不依赖后处理拼接，而是通过特征层面的调制实现深层耦合。
- 相较于在关节级别融合身体与手部特征的 **Hand4Whole**（Moon et al., CVPRW 2022），CHAM 在 ViT 特征流层面进行操作，信息交互更充分。
- 相较于单阶段全身估计方法（如 **OSX**, Lin et al., CVPR 2023；**Multi-HMR**, Baradel et al., ECCV 2024），本方法不重新训练全身模型，保留了预训练能力。
- 相较于利用手部特征但忽略相对手部位置的适配方法（如 **HMR-Adapter**, Shen et al., ACMMM 2024），CHAM 通过空间对齐的 2D 位置编码和交叉注意力显式建模手部在全身体系中的空间关系。

### 主要结果

在全身数据集（AGORA、ARCTIC、EHF）和手部数据集（IH26M、ReIH、HIC）上的综合评估表明，Hand4Whole++ 在全身与手部指标上均取得最优。以 AGORA 为例，全身 MPVPE 降至 76.84 mm，手部 MPVPE 降至 49.71 mm，显著优于 SMPLer-X 及其微调版本，也超越了手部专用 WiLoR。消融实验证实，CHAM 特征调制策略是性能提升的核心——在 AGORA 上全身 MPVPE 达 76.88 mm，手部 50.56 mm，明显优于直接分配手腕方向或替换手部网格的朴素组合策略。手指关节与形状转移进一步将 IH26M、ReIH、HIC 上的手部 MPVPE 分别压缩至 9.40、7.98、17.72 mm。

三维全身姿态与网格恢复旨在从单目图像中重建包含身体、手部和面部的完整三维人体模型。该任务在虚拟现实、人机交互和动作捕捉等领域具有广泛应用。然而，现有方法在实现高精度手部重建方面仍面临根本性挑战。

**核心瓶颈：全身与手部估计器的结构性矛盾。** 全身姿态估计器（如 **SMPLer-X**，Cai et al., NeurIPS 2023）通常在包含有限手部姿态多样性的全身数据集上训练，导致手部细节预测能力不足——手腕方向不准确、手指姿态模糊。另一方面，手部专用估计器（如 **WiLoR**，Potamias et al., CVPR 2025）虽能精细恢复手部姿态和形状，却缺乏全身上下文信息，在双手交互或遮挡场景下容易产生解剖学上不合理的配置。直接组合两类模型（如 **FrankMocap**，Rong et al., ICCVW 2021；**Hand4Whole**，Moon et al., CVPRW 2022）往往导致手部与身体运动链不一致，尤其是在手腕方向预测上出现明显偏差（Figure 1）。

**现有方法的三个缺口。** 第一，早期方法采用简单的后处理拼接策略，将手部网络输出直接嫁接到身体网格上，忽略了手腕作为运动链关键节点的空间连贯性。第二，单阶段方法（如 **OSX**，Lin et al., CVPR 2023；**Multi-HMR**，Baradel et al., ECCV 2024）试图从统一模型中同时预测身体和手部，但受限于训练数据中手部样本的稀疏性，手部精度难以与专用模型匹敌。第三，微调全身模型以适配手部数据虽能部分改善手部预测，却会破坏预训练模型的泛化能力，在未见数据集上产生失真的全身姿态（Figure 5）。

**本文动机。** 针对上述矛盾，本文提出 **Hand4Whole++**，一个模块化框架，旨在在不牺牲预训练模型泛化性的前提下，将手部专用估计器的精细能力注入全身姿态估计流程。核心思想是：通过冻结的预训练模型，利用轻量级特征调制（CHAM）将手部特有信息注入全身特征流，以改善手腕方向预测；同时通过可微刚性对齐直接转移手指关节和手部形状，既保留手部估计器的精细度又维持全身结构一致性。

## 核心方法与创新机理

### 瓶颈定位：全身与手部分裂的困境

三维全身姿态估计长期面临一个结构性矛盾：**全身估计器**（如 **SMPLer-X**，Cai et al., NeurIPS 2023）在包含有限手部姿态多样性的全身数据集上训练，导致手部细节预测能力不足；而**手部专用估计器**（如 **WiLoR**，Potamias et al., CVPR 2025）虽能精细恢复手指关节，却缺乏全身上下文，在双手交互或遮挡场景下表现退化。直接结合两者的朴素策略——例如将手部估计器预测的手腕方向分配给全身模型，或将手部网格直接替换到全身网格上——会导致解剖学上不合理的手部配置，因为手部估计器并不理解上肢运动链的全局约束。

### 核心机制：冻结模型间的条件特征调制

Hand4Whole++ 的核心创新在于**通过冻结的预训练模型实现高效的手部-全身信息融合**，而非端到端重训练。其关键组件是 **CHAM（Conditional Hands Modulator，条件手部调制器）**，一个轻量级特征调制模块，工作在两个冻结的 ViT 骨干网络之间：

1. **空间对齐的特征注入**：CHAM 从冻结的手部姿态估计器（WiLoR）提取手部 ViT 特征，通过 2D 位置编码和空间对齐的变换，以加法调制的方式注入冻结的全身姿态估计器（SMPLer-X）的 24 层 ViT 特征流中。这使得全身模型在预测手腕方向时能够感知手部特有的细粒度信息，同时保持预训练模型的泛化能力不被破坏。

2. **交叉注意力处理双手交互**：当双手均被检测到时，CHAM 引入一个三层交叉注意力 Transformer 编码器，对手部特征进行交互建模，显著改善双手交互场景下的估计精度（在 IH26M 上将手部 MPVPE 从 9.77 降至 9.40 mm，MRRPE 从 35.36 降至 32.30）。

### 手指关节与形状的直接转移

与依赖全身模型统一预测手部姿态和形状的基线方法不同，Hand4Whole++ 将**手指关节和手部形状直接转移**自手部专用估计器。具体而言，从 MANO 参数（手指姿态 $\theta_{\mathrm{rh}}, \theta_{\mathrm{lh}}$ 和形状系数 $\beta_{\mathrm{rh}}, \beta_{\mathrm{lh}}$）生成规范手部网格，通过手腕及四个 MCP 关节（食指、中指、无名指、小指）的可微刚性对齐，将 MANO 手部顶点替换到 SMPL-X 全身网格上。这一设计的理据在于：MANO 手部模型比 SMPL-X 手部具有更强的形状表达能力（与 3D 扫描的点对点误差仅 1.34 mm vs 1.98 mm），且手部专用估计器在手指细节上远优于全身模型。

### 与基线方法的关键差异

| 设计维度 | 基线方法（SMPLer-X / 朴素组合） | Hand4Whole++ |
|---------|-------------------------------|--------------|
| **手腕方向估计** | 由全身模型直接预测，缺乏手部细节且可能与上臂运动链不一致 | CHAM 调制全身特征流，结合手部特征预测，实现准确且解剖学连贯的手腕方向 |
| **手部网格生成** | 使用 SMPL-X 统一参数预测手部姿态和形状，表达力受限 | 从 MANO 参数生成规范手部网格，通过刚性对齐替换 SMPL-X 手部顶点 |
| **训练策略** | 端到端训练或微调全身模型，破坏预训练能力 | 冻结全身和手部姿态估计器，仅训练轻量级 CHAM 模块 |

消融实验验证了这一设计的有效性：在 AGORA 数据集上，CHAM 特征调制策略将全身 MPVPE 降至 76.88 mm、手部 MPVPE 降至 50.56 mm，显著优于直接分配手腕方向或直接替换手部网格等朴素组合策略。更重要的是，与微调全身模型相比，CHAM 保持了预训练模型的泛化能力——在未见的 EHF 数据集上全身姿态保持正确，而微调模型产生明显失真。

### 局限与待解问题

该方法依赖两个预训练模型，导致推理时间增加（约 10 fps），限制了实时应用场景。当手部检测失败时，CHAM 将手部 ViT 特征置零，可能导致手腕预测退化。训练数据仅限于 IH26M、ReIH、ARCTIC 和 AGORA，可能无法覆盖所有手部交互多样性。此外，在仅包含手部标注的数据集上训练时，非手部关节可能因缺乏全身标注而与输入图像对齐不精确。

Hand4Whole++ 是一个模块化框架，旨在将预训练的全身姿态估计器与预训练的手部姿态估计器的优势进行整合，以提升三维全身姿态估计中手部的精度与解剖学合理性。其核心设计理念是：**冻结两个预训练模型，仅训练轻量级的条件手部调制器（CHAM）**，从而在不破坏预训练模型泛化能力的前提下，注入手部特有的精细信息。

### 框架组成与数据流

整体 pipeline 由四个主要模块构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Hand4Whole++, which comprises a pre-trained hand pose estimator, a pre-trained whole-body pose estimator, CHAM, and a finger articulation and shape transfer module. During training, only CHAM is updated, while the pre-trained pose estimators remain frozen*

1. **预训练手部姿态估计器（WiLoR）**：接收输入图像，提取手部视觉特征（ViT 特征），并预测 MANO 参数（手指姿态 $\theta_{\mathrm{rh}}, \theta_{\mathrm{lh}}$ 和手部形状 $\beta_{\mathrm{rh}}, \beta_{\mathrm{lh}}$）。该模块在整个训练过程中保持冻结。
2. **预训练全身姿态估计器（SMPLer-X）**：同样接收输入图像，通过其 ViT 骨干网络提取全身特征流，并预测 SMPL-X 参数。该模块同样保持冻结，但其**手腕方向预测**受 CHAM 调制。
3. **CHAM（条件手部调制器）**：这是框架中唯一可训练的模块。它从手部姿态估计器获取手部 ViT 特征，经过空间对齐的变换后，以加法方式调制全身 ViT 的 24 层特征流，从而将手部特有的空间与姿态信息注入全身特征中，使全身模型能够预测出既准确又与上臂运动链解剖学连贯的手腕方向。
4. **手指关节与形状转移模块**：从 MANO 参数生成规范手部网格，然后利用手腕和四个 MCP 关节（食指、中指、无名指、小指）进行可微刚性对齐，将精细的手指关节和手部形状直接替换到全身 SMPL-X 网格的对应手部顶点上。该模块避免了直接使用手部估计器的手腕方向，从而保证了全身结构的一致性。

此外，框架还包含一个 FaceNet，基于裁剪的面部图像回归下颌姿态和面部表情参数。

### 训练策略

训练时，仅 CHAM 模块的参数被更新，预训练的全身和手部姿态估计器均保持冻结。这种策略确保了：
- 全身模型在未见数据集上的泛化能力不被破坏（与微调全身模型相比，CHAM 在 EHF 等数据集上保持正确的全身姿态，而微调模型则出现失真，见 Figure 5）。
- 手部模型在手指细节和形状表达上的优势得以完整保留（MANO 手部模型比 SMPL-X 手部具有更强的形状表达能力，与 3D 扫描的点对点误差更低：1.34 mm vs 1.98 mm，见 Table S1）。

### 输入输出流总结

- **输入**：单张 RGB 图像。
- **中间特征流**：手部 ViT 特征 → CHAM 空间对齐与交叉注意力处理 → 加法调制全身 ViT 特征流。
- **输出**：融合了精细手部网格的全身 SMPL-X 网格，其中手腕方向由受 CHAM 调制的全身模型预测，手指关节和手部形状由 MANO 模型转移而来。

### 整体架构与设计理念

Hand4Whole++ 是一个模块化框架，其核心设计原则是**冻结所有预训练模型，仅训练轻量级适配模块**，从而在不破坏预训练泛化能力的前提下注入手部特有信息。如图 Figure 2 所示，系统由四个主要组件构成：

1. **预训练手部姿态估计器 (WiLoR)**：提取手部 ViT 特征并预测 MANO 参数（手指姿态与手部形状）。
2. **预训练全身姿态估计器 (SMPLer-X)**：预测 SMPL-X 参数，其中手腕方向由 CHAM 调制。
3. **CHAM（条件手部调制器）**：将手部 ViT 特征注入全身 ViT 特征流，实现手腕方向的精确预测。
4. **手指关节与形状转移模块**：通过可微刚性对齐，将 MANO 手部网格替换到全身网格上。

### CHAM：条件手部调制器

**瓶颈分析**：全身姿态估计器（如 SMPLer-X）训练于手部多样性有限的全身数据集，导致手部细节预测能力不足；而手部专用估计器（如 WiLoR）则缺乏全身上下文，直接组合会导致解剖学不合理的手部配置，尤其在遮挡场景下更为严重。

**核心机制**：CHAM 是一个轻量级特征调制模块，通过从冻结的手部姿态估计器提取的手部特征，以空间对齐的方式调节冻结的全身 ViT 特征流。其架构如 Figure 3 所示，包含以下关键设计：

- **2D 位置编码**：为手部特征添加空间位置信息，使其与全身特征在空间上对齐。
- **交叉注意力 Transformer**：当双手均被检测到时，使用三层交叉注意力 Transformer 编码器处理双手特征的交互关系。消融实验（Table S2）表明，该交叉注意力模块在双手交互数据集上将手部 MPVPE 从 9.77 降至 9.40 mm，MRRPE 从 35.36 降至 32.30。
- **24 层加法调制**：将处理后的手部特征通过加法操作注入全身 ViT 的 24 层特征流中，实现逐层调制。

**关键因果机制**：CHAM 通过调制全身特征流来改善手腕方向预测，而非直接替换手腕参数。这一设计使得手腕方向既受益于手部特征的精细度，又保持与上臂运动链的解剖学连贯性。消融实验（Table 2）验证了该策略的有效性：基于 CHAM 的特征调制（Ours）在 AGORA 数据集上全身 MPVPE 为 76.88 mm、手部 MPVPE 为 50.56 mm，显著优于直接分配手腕方向或直接替换手部网格的原始组合策略。

### 手指关节与形状转移

**设计动机**：MANO 手部模型比 SMPL-X 手部具有更强的形状表达能力。定量比较（Table S1）显示，MANO 与 3D 扫描的点对点误差为 1.34 mm，而 SMPL-X 为 1.98 mm。

**转移流程**（Figure 4）：
1. 从手部姿态估计器获取 MANO 参数：
   - 手指姿态参数：$\theta_{\mathrm{rh}}, \theta_{\mathrm{lh}}$（左右手指关节旋转）
   - 手部形状参数：$\beta_{\mathrm{rh}}, \beta_{\mathrm{lh}}$（左右手形状系数）
2. 使用上述参数生成规范坐标系下的手部网格（忽略 MANO 预测的手腕方向）。
3. 通过**可微刚性对齐**将规范手部网格对齐到全身网格：使用手腕及四个 MCP 关节（食指、中指、无名指、小指）计算刚性变换，替换 SMPL-X 手部顶点。

**关键设计**：该模块仅转移手指关节和手部形状，而手腕方向由 CHAM 调制的全身模型预测。这种分工确保了手指细节的精细度（来自手部专用模型）与手腕-上臂运动链的解剖学连贯性（来自全身模型）兼得。

### 训练策略

整个框架的训练策略极为精简：**冻结全身姿态估计器（SMPLer-X）和手部姿态估计器（WiLoR），仅训练轻量级 CHAM 模块**。这一设计的优势在于：
- 保持预训练模型的泛化能力，避免微调导致在未见数据集上产生失真（Figure 5 验证了这一点：微调全身模型在 EHF 数据集上产生失真，而 CHAM 保持正确姿态）。
- 训练数据需求低，仅需 IH26M、ReIH、ARCTIC、AGORA 等有限数据集即可完成 CHAM 训练。

**局限性**：该策略也带来推理速度的代价——需要运行两个预训练模型，推理速度约 10 fps（Table S3）。此外，当手部检测失败时，CHAM 将手部 ViT 特征置零，可能导致手腕预测退化。

## 实验与关键发现

### 一、主实验结果

Hand4Whole++ 在全身与手部数据集上均取得最低误差，验证了冻结预训练模型 + 轻量级 CHAM 调制的有效性。

**全身数据集表现（Table 4）**：在 AGORA 上，Hand4Whole++ 达到全身 MPVPE 76.84 mm、手部 MPVPE 49.71 mm，优于原始 **SMPLer-X**（Cai et al., NeurIPS 2023）及其微调版本，也优于 **Multi-HMR**（Baradel et al., ECCV 2024）等全身方法。在 ARCTIC 上，MPVPE/MRRPE 为 45.95/25.03 mm；在 EHF 上为 61.24/33.43 mm。值得注意的是，微调 SMPLer-X 在训练数据（AGORA）上表现接近，但在未见过的 EHF 上全身姿态出现失真，而 CHAM 由于冻结了骨干网络，保持了泛化能力（Figure 5）。

**手部数据集表现（Table 5）**：在 IH26M、ReIH、HIC 上，Hand4Whole++ 的手部 MPVPE 分别降至 9.40、7.98、17.72 mm，MRRPE 分别降至 32.30、16.37、29.09 mm，与手部专用 SOTA **WiLoR**（Potamias et al., CVPR 2025）相比具有竞争力甚至更优。这得益于手指关节与形状转移模块直接继承了 WiLoR 的精细手指表达，同时 CHAM 提供了全身上下文以改善手腕方向预测。

**评估协议说明**：手部评估采用基于手腕对齐的 MPVPE 和相对根位置误差 MRRPE，不使用 Procrustes 对齐以避免掩盖手腕方向误差。在全身数据集上训练时，使用真实标注的手部尺度进行协议一致比较（Table 4/5 中以 * 标记）。

### 二、消融研究

#### 2.1 全身与手部模型组合策略（Table 2）

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/007_Table_2.jpg]]
*Table 2: MPVPE comparison on the AGORA dataset using different strategies for combining whole-body and hand-only pose estimators. The last row shows ours*

在 AGORA 上比较了多种组合策略：
- **直接分配手腕方向**：将手部估计器的手腕方向直接赋给全身模型，导致全身 MPVPE 较高，因为手腕方向与上臂运动链不一致。
- **直接替换手部网格**：将手部估计器的手部网格直接替换到全身网格上，同样产生解剖学不合理的结果。
- **CHAM 特征调制（Ours）**：通过 CHAM 以空间对齐的方式调制全身 ViT 特征流，全身 MPVPE 降至 76.88 mm，手部 MPVPE 降至 50.56 mm，显著优于上述简单组合策略。

这一消融表明，瓶颈不在于手部估计器本身的质量，而在于如何将手部特有信息以结构连贯的方式注入全身预测框架。

#### 2.2 手指关节与形状转移（Table 3）

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/006_Table_3.jpg]]
*Table 3: MPVPE comparison with and without the proposed finger articulation and hand shape transfer. The last row shows ours*

在 IH26M、ReIH、HIC 上，加入手指关节和形状转移模块后，手部 MPVPE 分别从无转移时的较高值降至 9.40、7.98、17.72 mm。该模块通过手腕及四个 MCP 关节的可微刚性对齐，将 MANO 生成的规范手部网格替换 SMPL-X 手部顶点，既保留了 WiLoR 的精细手指姿态，又维持了与全身网格的结构一致性。

MANO 手部模型的形状表达能力优于 SMPL-X 手部：在 3D 扫描数据上，MANO 优化网格与扫描的点对点平均距离为 1.34 mm，而 SMPL-X 为 1.98 mm（Table S1, Figure S1），这为转移模块提供了更强的几何基础。

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/012_Figure_S.1.jpg]]
*Figure S.1: Comparison of hand shape expressiveness between MANO and SMPL-X. MANO produces hand shapes that more closely match the 3D scans compared to SMPL-X*

#### 2.3 CHAM 中交叉注意力的作用（Table S2）

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/015_Table_S.2.jpg]]
*Table S.2: Comparison of MPVPE/MRRPE with and without cross-attention in CHAM*

CHAM 中的交叉注意力模块对双手交互场景尤为重要。在 IH26M 上，加入交叉注意力后手部 MPVPE 从 9.77 降至 9.40，MRRPE 从 35.36 降至 32.30。该模块仅在双手均被检测到时激活，通过 2D 位置编码和三层的交叉注意力 Transformer 编码器融合双手特征，缓解了交互场景下的手部预测歧义。

#### 2.4 泛化能力验证（Figure 5）

![[assets/figures/papers/paper_list_l1017_https_arxiv_org_abs_2603_14726/figures/008_Figure_5.jpg]]
*Figure 5: Effectiveness of the proposed CHAM*

与微调全身模型的对比实验显示，CHAM 由于冻结了预训练骨干，在未见数据集（EHF）上保持了正确的全身姿态，而微调 SMPLer-X 产生了明显的姿态失真。这验证了冻结骨干 + 轻量级调制的训练策略在保持泛化能力方面的优势。

### 三、运行效率与局限性

**推理时间**（Table S3）：在 RTX A6000 GPU 上，单张图像处理时间约 100 ms（约 10 fps），主要开销来自两个预训练模型的推理。CHAM 本身为轻量级模块，额外开销较小。

**已知失败模式**：
1. **手部检测失败**：当手部检测失败时，CHAM 将手部 ViT 特征置零，可能导致手腕预测退化至纯全身模型的水平。
2. **非手部关节对齐**：在仅包含手部标注的数据集（如 IH26M、ReIH）上训练时，非手部关节因缺乏全身标注，可能与输入图像对齐不精确。
3. **训练数据覆盖**：CHAM 训练仅使用了 IH26M、ReIH、ARCTIC、AGORA 四个数据集，可能未覆盖所有手部交互多样性，在极端手势或强遮挡场景下性能可能下降。

### 四、关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Table 1 | Hand4Whole++ 在全身和手部数据集上全面超越基线方法 |
| Table 2 | CHAM 特征调制策略显著优于直接分配手腕方向或替换手部网格的简单组合 |
| Table 3 | 手指关节与形状转移模块在三个手部数据集上均带来显著增益 |
| Table 4 | 与全身姿态估计器的全面比较中，Hand4Whole++ 在所有基准上取得最优 |
| Table 5 | 与手部专用估计器比较，Hand4Whole++ 达到竞争性或更优的手部精度 |
| Figure 5 | CHAM 冻结骨干策略保持了泛化能力，微调全身模型在未见数据上产生失真 |
| Table S1/Figure S1 | MANO 手部形状表达力优于 SMPL-X，为转移模块提供了更强的几何基础 |
| Table S2 | 交叉注意力在双手交互场景下有效降低误差 |

## 定位与知识库关联

### 1. 方法谱系与基线关系

Hand4Whole++ 处于 **全身三维姿态估计** 与 **手部专用姿态估计** 的交叉地带，其核心设计动机源于对两类方法互补优势的整合：

- **全身姿态估计基线**：以 **SMPLer-X** (Cai et al., NeurIPS 2023) 为代表的全身体态估计器，基于 SMPL-X 参数化模型统一预测身体、手部和面部姿态。其瓶颈在于训练数据（全身数据集）中手部姿态的多样性远低于手部专用数据集，导致手部细节预测能力不足。
- **手部专用姿态估计基线**：以 **WiLoR** (Potamias et al., CVPR 2025) 为代表的手部估计器，在手指关节精度和手部形状表达力上显著优于全身模型，但缺乏全身上下文，无法处理双手交互等需要全局推理的场景。
- **早期融合尝试的不足**：**FrankMocap** (Rong et al., ICCVW 2021) 和 **Hand4Whole** (Moon et al., CVPRW 2022) 尝试在关节级别结合身体和手部网络，但直接组合会导致解剖学不合理的手部配置，尤其在遮挡场景下。**HMR-Adapter** (Shen et al., ACMMM 2024) 虽利用手部特征进行适配，但忽略了手部相对于身体的空间位置关系。

Hand4Whole++ 的核心贡献在于提出了一种 **非侵入式的特征调制机制**（CHAM），在不破坏预训练模型泛化能力的前提下，将手部专用知识注入全身特征流。相比 **OSX** (Lin et al., CVPR 2023) 的单阶段方法和 **Multi-HMR** (Baradel et al., ECCV 2024) 的多人全身网格恢复，Hand4Whole++ 通过模块化冻结训练策略，保留了各预训练模型的最佳性能。

### 2. 技术谱系中的关键设计选择

| 设计维度 | 全身模型（SMPLer-X） | 手部模型（WiLoR） | Hand4Whole++ |
|---------|---------------------|-------------------|--------------|
| 手腕方向预测 | 由全身 ViT 直接回归 | 独立预测，无身体上下文 | CHAM 调制全身特征后预测 |
| 手部网格生成 | SMPL-X 统一参数 | MANO 参数 | MANO 生成 + 刚性对齐替换 |
| 训练策略 | 端到端 | 端到端 | 冻结双模型，仅训练 CHAM |
| 手部形状表达力 | 较弱（点对面误差 1.98 mm） | 较强（点对面误差 1.34 mm） | 继承 MANO 表达力 |

关键洞察在于：**手指关节和手部形状** 是手部姿态估计器的强项，可直接通过可微刚性对齐转移；而 **手腕方向** 是连接手部与身体运动链的关键，需要全身上下文才能保证解剖学连贯性。CHAM 正是针对后者设计的轻量级调制器。

### 3. 适用边界与局限

**适用场景**：
- 需要同时输出高质量全身姿态和精细手部姿态的应用（如虚拟现实、动作捕捉）
- 双手交互场景，其中全身上下文对手部推理至关重要
- 可接受约 10 fps 推理速度的离线或准实时场景

**已知局限**：
1. **推理效率**：依赖两个预训练模型（手部 + 全身），推理时间增加，在 RTX A6000 上约 10 fps（Table S3），不适用于严格实时应用。
2. **手部检测依赖性**：当手部检测失败时，CHAM 将手部 ViT 特征置零，可能导致手腕预测退化至全身模型基线水平。
3. **训练数据覆盖**：CHAM 仅在 IH26M、ReIH、ARCTIC、AGORA 四个数据集上训练，可能未覆盖所有手部交互多样性。
4. **非手部关节对齐**：在仅包含手部标注的数据集上训练时，非手部关节可能因缺乏全身标注而与输入图像对齐不精确。
5. **多人扩展性**：当前设计针对单人场景，如何扩展到多人场景中不同个体的手部交互仍需探索。

### 4. 开放问题

1. **轻量化与实时化**：能否通过知识蒸馏或模型剪枝进一步轻量化 CHAM，使整体框架适应实时应用需求？
2. **无配对数据训练**：能否利用无配对的手部与全身数据，以自监督或弱监督方式训练 CHAM，从而扩展训练数据规模？
3. **多人交互扩展**：如何将方法扩展到多人场景，处理不同个体之间的手部-身体、手部-手部交互？
4. **跨模型泛化**：CHAM 当前与特定预训练模型（SMPLer-X + WiLoR）绑定，能否设计模型无关的特征调制机制，支持任意全身/手部估计器的即插即用组合？
5. **手部检测鲁棒性**：当手部检测失败或置信度较低时，能否设计渐进式特征融合策略，而非直接将手部特征置零？

## 原文 PDF

![[paperPDFs/CVPR_2026/Enhancing_Hands_in_3D_Whole_Body_Pose_Estimation_with_Conditional_Hands_Modulator.pdf]]
