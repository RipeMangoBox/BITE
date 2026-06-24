---
title: "SMPLest-X: Ultimate Scaling for Expressive Human Pose and Shape Estimation"
type: paper
paper_level: A
venue: TPAMI
year: 2025
pdf_ref: paperPDFs/TPAMI_2025/SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimation.pdf
aliases:
- SX
- SMPLest-X
tags:
- TPAMI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 数据和模型规模的缩放是提升EHPS性能的关键操纵变量；通过大规模多源数据训练与更大容量的视觉Transformer骨干网络，可显著降低跨基准测试的误差。
primary_logic: 通过系统性基准测试发现，不同数据集之间存在显著领域鸿沟，但大量数据集的组合可以互补，从而训练出泛化能力强的通用基础模型；极简架构 SMPLest-X 去除显式的分部件指导模块，使用纯 Transformer 解码器反而显著提升手部估计，说明显式部件引导并非必需。
claims:
- 数据与模型缩放将全身 MPE 从 110 mm 以上降至 60 mm 以下。
- 单数据集训练无法泛化到不同场景（例如，AGORA 训练模型在 AGORA 上排名第1，但在 EHF 上排名第30）。
- SMPLest-X 通过消除组件引导模块并采用 Transformer 解码器，手部 PA-MPE 比 SMPLer-X 低 15%，手部 MPE 低 13%。
- 训练 40 个数据集达到 10M 实例后，模型性能不再随数据量显著提升，出现边际收益递减。
---

# SMPLest-X: Ultimate Scaling for Expressive Human Pose and Shape Estimation

> [!tip] 核心洞察
> 通过系统性基准测试发现，不同数据集之间存在显著领域鸿沟，但大量数据集的组合可以互补，从而训练出泛化能力强的通用基础模型；极简架构 SMPLest-X 去除显式的分部件指导模块，使用纯 Transformer 解码器反而显著提升手部估计，说明显式部件引导并非必需。

| 字段 | 内容 |
|------|------|
| 中文题名 | SMPLest-X：面向表现力丰富的人体姿态与体型估计的终极缩放方案 |
| 英文题名 | SMPLest-X: Ultimate Scaling for Expressive Human Pose and Shape Estimation |
| 会议/期刊 | TPAMI 2025 |
| Links | [Code](https://github.com/wqyin/SMPLest-X) · [Project](https://sanweiliti.github.io/egobody/egobody.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SMPLest-X |
| Dataset | 五大基准测试（AGORA, UBody, EgoBody, 3DPW, EHF）, SynHand, AGORA test set |

> [!tip] 效果简介
> - 五大基准测试（AGORA, UBody, EgoBody, 3DPW, EHF） 上，平均主误差 MPE (mm) <60 vs >110 (OSX, HybrIK-X) (~50 mm)。
> - SynHand 上，全身 Procrustes-aligned 每顶点误差 (PA-PVE All) (mm) 21.7 (SMPLest-X-H40) vs 38.2 (Multi-HMR) (-16.5 mm (-43%))。
> - AGORA test set 上，归一化平均顶点误差 NMVE All 96.2 (SMPLest-X-H40t) vs （此前最佳未知，但显著优于其他SOTA） (N/A)。

## 概述

SMPLest-X 旨在解决**表现力丰富的人体姿态与体型估计**（EHPS）中长期存在的跨场景泛化瓶颈。现有方法通常依赖单一或少量数据集训练，导致在未见过的场景——尤其是手部姿态估计——上性能显著下降。例如，在 AGORA 数据集上训练的最佳模型，在 EHF 上仅排第 30 名（Table 1），揭示了不同数据集之间存在严重的领域鸿沟。

本文的核心洞见是：**数据和模型规模的缩放**是提升 EHPS 泛化能力的关键操纵变量。通过对 40 个数据集进行系统性的单数据集训练基准测试，作者发现这些数据集在图像外观、全局朝向、身体姿态等属性上的分布高度互补（Fig. 2），组合使用可以有效弥合领域鸿沟。基于此，SMPLest-X 采用极简的一阶段架构——仅包含 ViT 骨干网络、6 层 Transformer 解码器和参数回归头——去除了 SMPLer-X 中显式的分部件引导模块（Fig. 5），反而在手部估计上取得显著提升。

**核心结果**：数据与模型缩放将五大基准测试（AGORA、UBody、EgoBody、3DPW、EHF）上的全身平均主误差（MPE）从 110 mm 以上降至 60 mm 以下，手部主误差从 62 mm 以上降至 31 mm（Fig. 1）。在 SynHand 手部基准上，SMPLest-X-H40 的全身 PA-PVE 达到 21.7 mm，较 Multi-HMR 降低 43%（Table 2）。当训练实例达到 10M 后，性能提升出现边际收益递减。

**方法定位**：SMPLest-X 属于单阶段 EHPS 方法谱系，继承自 OSX（首个基于 ViT 的单阶段框架），与 AiOS、Multi-HMR 等同期方法共享“集成检测与参数回归”的设计理念，但通过极简架构和大规模多源数据训练，实现了从专用模型向通用基础模型的范式转变。

## 背景与动机

表现力丰富的人体姿态与体型估计（Expressive Human Pose and Shape Estimation, EHPS）旨在从单张图像中恢复人体的三维姿态、手部动作、面部表情及体型参数。该任务以参数化人体模型 **SMPL-X** 为基础，需估计姿态参数 $\theta \in \mathbb{R}^{55 \times 3}$（涵盖身体、手部、眼球及下颌共 55 个关节的旋转）、体型参数 $\beta \in \mathbb{R}^{10}$ 以及表情参数 $\psi \in \mathbb{R}^{10}$。通过关节回归器与运动树变换 $R_{\theta}(\mathcal{J}(\beta))$，可从这些参数计算出三维关键点位置。

### 现有方法的瓶颈：跨场景泛化能力不足

尽管 EHPS 领域已涌现出多种方法，但其核心瓶颈在于**跨场景泛化能力严重不足**，尤其是在手部姿态估计方面存在显著性能缺口。这一瓶颈的根源可归结为两个层面：

**数据层面：单一数据集训练的领域锁定效应。** 系统性基准测试（Table 1）揭示了不同数据集之间存在显著的领域鸿沟：在 AGORA 训练集上单独训练的模型，虽然在 AGORA 测试集上排名第 1，但在 EHF 上仅排名第 30，在 3DPW 上排名第 17。类似地，BEDLAM 数据集虽然在所有单数据集训练中取得了最低的平均主误差（MPE 117.1 mm），但其在其他基准上的表现同样参差不齐。这表明，单一数据集的图像外观、全局朝向、人体姿态等属性分布（Fig. 2）与目标测试场景存在系统性偏移，导致模型学到的是数据集特定的偏置而非通用的 EHPS 能力。

**架构层面：显式分部件引导的必要性存疑。** 此前的 SOTA 方法（如 **SMPLer-X**、**OSX**（Lin et al.））普遍采用分阶段或分部件的设计范式：OSX 提出首个基于 ViT 的单阶段框架；SMPLer-X 保留组件引导模块（Component Guiding module），通过中间步骤对手部和面部进行显式定位与裁剪后再分别估计。这种设计直觉上有利于精细部位的建模，但其对泛化性能的实际贡献尚未被严格检验。

### 本文动机：通过缩放突破泛化瓶颈

上述分析指向一个核心操纵变量——**数据与模型规模的缩放**。本文的动机源于一个关键洞察：虽然不同数据集之间存在领域鸿沟，但大量数据集的组合可以互补覆盖多样化的外观、姿态和场景分布，从而训练出泛化能力强的通用基础模型。

为实现这一目标，本文从三个维度展开：
1. **系统性基准测试**：对 40 个 EHPS 数据集进行单数据集训练与跨基准评估，量化各数据集的领域特性与互补性，为数据选择提供依据。
2. **极简架构验证**：提出 **SMPLest-X**，去除显式的分部件引导模块，仅使用 6 层 Transformer 解码器直接回归全部参数，以此检验“显式部件引导是否为必需”这一基础假设。
3. **缩放律探索**：研究数据量（从单数据集到 40 数据集、10M 训练实例）与模型容量（ViT 变体）对全身及手部估计误差的影响规律。

初步实验（Fig. 1）已表明该方向的潜力：通过数据与模型缩放，全身平均主误差（MPE）可从 110 mm 以上降至 60 mm 以下，手部主误差从 62 mm 以上降至 31 mm。然而，当训练实例达到 10M 后，性能提升出现边际收益递减，暗示纯缩放路径存在饱和点，这也构成了本文后续探索的边界条件。

## 核心创新

SMPLest-X 的核心创新在于将“极简架构”与“终极缩放”相结合，以极低的架构复杂度实现了表现力人体姿态与体型估计（EHPS）的性能跃升。其关键创新点可归纳为两个**changed slots**：

### 1. 解码器结构：从显式部件引导到纯 Transformer 解码

**Baseline（SMPLer-X）** 在解码阶段保留了**组件引导模块（Component Guiding module）**，该模块显式地检测并裁剪手部、脸部等局部区域，再分别进行参数回归。这种分部件建模的设计直觉上有利于精细部位（如手部）的估计。

**SMPLest-X** 完全移除了这一显式部件引导模块，代之以一个**6 层 Transformer 解码器**，不包含任何显式的分部件建模。图像特征与任务 Token 拼接后直接送入解码器，由自注意力机制隐式地学习各部位之间的关联（Fig. 5, Section 4.1）。

**关键证据**：这一极简设计带来了反直觉的性能提升。在全身手部姿态估计中，SMPLest-X 的手部 PA-MPE 比 SMPLer-X 低 15%，手部 MPE 低 13%（Table 5, confidence 0.9）。注意力可视化（Fig. 8）进一步表明，扩展的 Token 在没有额外部件引导的情况下，能够自主地关注图像特征中对应的身体部位信息。这揭示了一个重要洞察：**显式的部件引导并非必需，甚至可能限制模型学习更优的全局特征表示**。

### 2. 手部朝向估计：新增手腕姿态一致性约束

**Baseline（SMPLer-X）** 未包含专门的手部朝向估计模块。

**SMPLest-X** 新增了一个**手部朝向估计头**，并构建了**参数一致性损失（wrist pose consistency loss）**（Section 4.2）。该损失约束手腕姿态在身体运动链与手部运动链中的一致性，从而增强手部与身体之间的几何连贯性。

这一设计直接针对 EHPS 中手部估计的瓶颈：手腕是连接身体与手部的关键节点，其姿态一致性对整体精度至关重要。结合 SynHand 数据集提供的多样化手部姿态标注（Fig. 4），该创新显著提升了手部估计的鲁棒性，尤其在遮挡和物体交互场景下表现突出（Fig. 6）。

### 创新本质：缩放律驱动的架构简化

上述两个 changed slots 并非孤立的架构技巧，而是**数据与模型缩放律**驱动下的必然选择。论文通过系统性基准测试（Table 1）发现：
- 单数据集训练无法泛化：AGORA 训练模型在 AGORA 上排名第 1，但在 EHF 上排名第 30。
- 多源大规模数据（40 个数据集、10M 实例）的组合可以互补领域鸿沟。

在这种“数据洪流”下，复杂的部件引导模块反而成为瓶颈——它引入了额外的归纳偏置，限制了模型从海量数据中自主学习跨部位关联的能力。因此，**极简的 Transformer 解码器反而成为最优选择**，使模型能够充分吸收多源数据的互补信息。

> **注意**：训练实例从 7.5M 增至 10M 后，性能提升趋于饱和（Section 5.3, confidence 0.9），表明纯数据缩放的边际收益递减。如何突破这一饱和点，是未来的开放问题。

## 整体框架

SMPLest‑X 的整体流程遵循**单阶段端到端范式**：输入为单张 RGB 图像，输出为 SMPL‑X 参数化人体模型的全部参数（姿态 $\theta \in \mathbb{R}^{55 \times 3}$、形状 $\beta \in \mathbb{R}^{10}$、表情 $\psi \in \mathbb{R}^{10}$），无需独立的检测、裁剪或分部件后处理阶段。这与 **OSX**（首个基于 ViT 的单阶段框架）、**AiOS** 和 **Multi‑HMR** 等近期单阶段方法共享“定位与参数估计一体化”的设计哲学，但其架构被进一步精简至极简形态。

### 流水线模块

整个框架由三个核心模块级联构成（Fig. 5）：

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/007_Figure_5.jpg]]
*Figure 5: Architecture of SMPLest-X. Compared with other frameworks with algorithmic modules in various stages (bottom), SMPLest-X (top) has a minimalistic framework design in all three stages. Noted that SMPLer-X consists B. Component Guiding module in the decoder stage*

1. **ViT Backbone（图像特征提取器）**  
   输入图像经边界框裁剪后送入预训练的 ViT‑L 骨干网络（来自 HumanBench 或 OSX 的预训练权重），将图像划分为 patch token 并展平为特征向量序列。该模块负责将原始像素转换为高维语义特征，供后续解码器使用。

2. **Transformer Decoder（6 层解码器）**  
   这是 SMPLest‑X 与 SMPLer‑X 的关键分水岭。SMPLer‑X 在此阶段保留了**组件引导模块**（Component Guiding module），通过显式的手部/脸部检测与裁剪来为分部件估计提供局部特征。  
   SMPLest‑X 则完全移除了该模块，代之以一个**纯 6 层 Transformer 解码器**，不包含任何显式的分部件建模。解码器接收拼接后的图像特征与任务 Token，通过交叉注意力机制自主学会关注图像中与身体、手部、脸部等相关的区域（注意力可视化见 Fig. 8），从而产生用于回归的特征表示。

3. **Regression Heads（多任务回归头）**  
   解码器的输出被送入多个并行的回归头，分别预测：  
   - 身体姿态与形状参数（$\theta_{\text{body}}, \beta$）  
   - 左右手姿态参数  
   - 面部表情参数（$\psi$）  
   - 新增的**手部朝向估计头**（wrist pose），并通过参数一致性损失约束手腕姿态与身体运动链的一致性（Section 4.2）

### 输入输出流

- **输入**：单张 RGB 图像 + 人体边界框（由外部检测器提供或端到端集成）  
- **中间表示**：ViT 输出的 patch‑level 特征序列 → Transformer 解码器输出的任务感知特征向量  
- **输出**：SMPL‑X 参数集 $\{\theta, \beta, \psi\}$，可直接驱动 SMPL‑X 模型生成 3D 网格与 3D 关键点（$R_{\theta}(\mathcal{J}(\beta))$）

### 设计动机与证据

移除组件引导模块的动机源于一个反直觉的发现：**显式分部件引导并非必需，甚至可能损害手部估计**。Table 5 显示，SMPLest‑X 的手部 PA‑MPE 比 SMPLer‑X 低 15%，手部 MPE 低 13%。这表明 Transformer 解码器在足够数据与模型容量的支撑下，能够通过自注意力机制隐式地学会关注手部等局部区域，而无需架构层面的硬性引导。Fig. 8 的注意力图进一步证实了这一机制：扩展的 Token 会自动聚焦于图像中对应的身体部件区域。

## 核心模块与公式推导

### 人体参数化模型

SMPLest-X 采用 **SMPL-X** 作为底层参数化人体模型，统一对人体的身体、手部和面部几何进行建模。模型的核心参数定义如下：

- **姿态参数**：$\theta \in \mathbb{R}^{55 \times 3}$，包含身体、双手、眼球和下颌共 55 个关节的旋转姿态。
- **形状参数**：$\beta \in \mathbb{R}^{10}$，控制身体、手部和面部的联合体型变化。
- **表情参数**：$\psi \in \mathbb{R}^{10}$，编码面部表情的形变。

给定上述参数，3D 关键点通过关节回归器与运动学树变换得到：
$$R_{\theta}(\mathcal{J}(\beta))$$
其中 $\mathcal{J}(\beta)$ 为从形状参数回归的关节位置，$R_{\theta}$ 表示沿运动学树的旋转变换。

### 性别中性适配器

由于部分训练数据使用性别化 SMPL-X 模型（男性/女性），而评估与推理采用中性模型，论文引入了一个适配器损失来桥接这一差异。给定性别化参数 $(\theta, \beta_{f/m})$ 和中性参数 $(\theta, \beta_n)$，适配器通过最小化顶点间 L2 距离来实现形状空间的映射：
$$\mathcal{L} = \| M_{f/m}(\theta, \beta_{f/m}) - M_n(\theta, A(\beta_{f/m})) \|_2$$
其中 $M_{f/m}$ 和 $M_n$ 分别为性别化与中性模型的顶点生成函数，$A(\cdot)$ 为形状参数的适配函数。该损失确保性别化标注数据能够有效贡献于中性模型的训练。

### 架构管线模块

SMPLest-X 的架构由三个核心模块串联构成，形成极简的端到端管线（见 Fig. 5）：

#### 1. ViT Backbone（特征编码器）

输入为经人体检测框裁剪后的图像，采用预训练的 **Vision Transformer (ViT)** 作为骨干网络。ViT 将图像分割为 patch tokens，并输出扁平化的特征向量序列。论文实验中使用了 ViT-H 和 ViT-L 等不同规模变体，以研究模型缩放效应。

#### 2. Transformer Decoder（解码器）

这是 SMPLest-X 与 SMPLer-X 的核心差异所在。SMPLer-X 在解码阶段保留了**组件引导模块（Component Guiding Module）**，通过显式检测手部和面部区域来辅助分部姿态估计。SMPLest-X 则完全移除了这一模块，替换为一个 **6 层标准 Transformer 解码器**，无任何显式的分部件建模。

解码器的输入由两部分拼接而成：
- ViT 输出的图像特征序列
- 一组可学习的任务 Token（task tokens）

解码器通过自注意力与交叉注意力机制，使各任务 Token 自主关注图像特征中的相关区域，无需外部组件引导即可隐式学习身体各部分的对齐关系。注意力可视化（Fig. 8）表明，扩展的任务 Token 能够自发地关注到手部、面部等对应区域。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/023_Figure_8.jpg]]
*Figure 8: Attentions of tokens. The extended tokens in SMPLest-X attends to the respective information in the image feature without additional component guidance*

#### 3. Regression Heads（回归头）

解码器输出的任务 Token 特征被送入多个并行的回归头，分别预测：
- 身体姿态参数
- 手部姿态参数
- 面部姿态与表情参数
- 形状参数
- 相机参数

此外，SMPLest-X 新增了一个**手部朝向估计头**，专门预测手腕的全局朝向，并通过腕部姿态一致性损失（wrist pose consistency loss）约束手部与手臂之间的运动学连贯性。这一设计是 SMPLer-X 所不具备的，对提升手部估计精度起到了关键作用。

### 关键设计决策

| 设计槽位 | SMPLer-X（基线） | SMPLest-X（本文） | 证据锚点 |
|---------|-----------------|------------------|---------|
| 解码器结构 | 组件引导模块（显式手部/脸部检测与裁剪） | 6 层 Transformer 解码器（无显式分部建模） | Section 4.1, Fig. 5 |
| 手部朝向估计 | 未包含 | 额外手部朝向估计头 + 腕部一致性损失 | Section 4.2 |

这一极简设计带来了反直觉的收益：去除显式的部件引导后，手部估计的 PA-MPE 比 SMPLer-X 降低了 15%，手部 MPE 降低了 13%（Table 5），说明在充足数据与模型容量的支撑下，Transformer 解码器的隐式注意力机制足以替代手工设计的部件引导模块。

## 实验与分析

### 6.1 核心发现：数据与模型缩放的缩放律

本研究最核心的发现是，通过系统性缩放训练数据量和模型容量，可以显著降低全身表现力人体姿态与体型估计（EHPS）的误差。Fig. 1 以散点图形式直观展示了这一趋势：在 AGORA、UBody、EgoBody、3DPW 和 EHF 五个关键基准测试上，全身平均主误差（MPE）从超过 110 mm 降至 60 mm 以下，手部主误差从超过 62 mm 降至 31 mm。图中圆面积代表模型规模（以 ViT 变体为参考），清晰地揭示了数据量和模型大小两个维度上的单调改善趋势。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/001_Figure_1.jpg]]
*Figure 1: Scaling up EHPS. a) Whole-body and b) hand-only mean primary error (MPE) indicate both data and model scaling are effective in reducing mean errors on primary metrics across key benchmarks for: AGORA [12], UBody [6], EgoBody [5], 3DPW [13] and EHF [14]. OSX [6] and HybrIK-X [15] are SOTA methods. Area of the circle indicates model size, with ViT variants as the reference (top right in the left figure)*

Table 3 和 Table 4 分别从全身和手部两个维度系统量化了这一缩放律。在全身基准上，当训练实例从约 1.5M 增至 10M 时，MPE 持续下降；模型从 ViT-B 升级至 ViT-H 也带来一致的性能增益。手部基准呈现相同规律，但值得注意的是，手部估计对数据缩放的敏感度更高——这与此前工作中手部标注稀缺、模型难以泛化的瓶颈直接对应。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/009_Table_3.jpg]]
*Table 3: Evaluate foundation models on whole-body benchmarks. We study the scaling law of the amount of data and the model sizes. The metrics are MPJPE for 3DPW, and PVE for other evaluation benchmarks. MPE: mean primary error. The lower, the better for all the metrics. The best values are bolded and the second best are underlined. AGORA uses the validation set, and EgoBody uses the EgoSet. 40+ denotes the model trained with 10 million instances from 40 datasets. Unit: mm*

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/010_Table_4.jpg]]
*Table 4: Evaluate foundation models on hands. We study the scaling law of the amount of data and the model sizes and evaluate the hand pose estimation. The metrics are hand PA-PVE and hand PVE for all evaluation benchmarks. (PA-)MPE: (PA-)mean primary error. Best values are bolded and second best are underlined. AGORA uses the validation set, and EgoBody uses the EgoSet. Unit: mm*

然而，缩放并非无限有效。Section 5.3 明确指出，训练 40 个数据集达到 10M 实例后，模型性能不再随数据量显著提升，出现边际收益递减。同时，训练实例从 7.5M 增至 10M 导致每 epoch 训练时间从 23 小时增至 33 小时（计算成本增加 43%），而性能提升甚微。这表明在当前架构下，数据和模型缩放已接近饱和点。

### 6.2 数据集基准测试：领域鸿沟与互补性

Table 1 是理解缩放策略有效性的关键实验。研究者对 40 个 EHPS 数据集逐一进行单数据集训练，并在五个主要基准上评估，按 MPE 排序。核心结论是：**单数据集训练无法泛化到不同场景**。例如，在 AGORA 训练集上训练的模型在 AGORA 测试集上排名第 1，但在 EHF 上仅排名第 30；BEDLAM 以 117.1 mm 的 MPE 位列综合排名第 1，但其在 3DPW 上的表现并非最优。这揭示了不同数据集之间存在显著的领域鸿沟（domain gap）。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/002_Table_1.jpg]]
*Table 1: Benchmarking EHPS datasets. For each dataset, we train a model on its training set and evaluate its performance on the testing sets of five major benchmarks: AGORA, UBody, EgoBody (EgoSet), 3DPW, and EHF. Datasets are then ranked by mean primary error (MPE). Top-1 values are bolded, and the rest of Top-5 are underlined. #Inst.: number of instances used in training. ITW: in-the-wild. EFT [16], NeuralAnnot (NeA) [17] and UP3D [18] produce pseudo labels. Unit: mm*

Fig. 2 通过 UMAP 可视化进一步解释了这一鸿沟的成因。从图像特征、全局朝向分布、身体姿态分布三个维度看，各数据集呈现明显的聚类分离。例如，AGORA 和 BEDLAM 等合成数据集在图像特征空间与真实场景数据集（如 3DPW、EHF）距离较远；而不同数据集的全局朝向分布也存在系统性偏差（如某些数据集以站立为主，另一些包含更多俯仰变化）。

Fig. 3 专门分析了手部姿态复杂度。通过计算各数据集手部姿态到“放松手姿”的距离分布，发现 ARCTIC 和 SynHand 等数据集包含大量远离放松姿态的复杂手势，而多数全身数据集（如 AGORA、UBody）的手部姿态集中在低复杂度区域。这解释了为何此前方法的手部估计性能普遍不佳——训练数据缺乏足够多样化的手部姿态样本。

正是基于这一分析，研究者构建了 SynHand 数据集（Fig. 4），专门提供清晰且多样化的手部姿态标注。Table 2 显示，SMPLest-X-H40 在 SynHand 上取得了 21.7 mm 的 PA-PVE（All），相较于 Multi-HMR 的 38.2 mm 降低了 43%，验证了数据质量对特定部位估计的关键作用。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/003_Table_2.jpg]]
*Table 2: Benchmarking EHPS methods on SynHand. Unit: mm. * denotes that the method uses integrated detection results, F1=98.0*

### 6.3 SMPLest-X 的架构消融：极简即高效

SMPLest-X 的核心架构创新在于**消除显式的分部件引导模块**，代之以纯 Transformer 解码器。Table 5 的对比结果具有决定性：在全身 MPE 上，SMPLest-X-L40（59.57 mm）优于 SMPLer-X-L40（60.32 mm）；在手部 PA-MPE 上，SMPLest-X 比 SMPLer-X 低 15%，手部 MPE 低 13%。这表明显式的手部/脸部检测与裁剪并非必需，甚至可能引入信息瓶颈——Transformer 解码器通过自注意力机制能够自主学会关注相关区域。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/012_Table_5.jpg]]
*Table 5: Mean Primary Error (MPE) of whole-body and hand pose estimation. We evaluate EHPS methods on multiple benchmark datasets for whole-body and hand pose estimation. Unit: mm*

Fig. 8 的注意力可视化为此提供了直观证据：SMPLest-X 中的扩展 Token 在没有额外组件引导的情况下，自动聚焦于图像特征中的相应身体部位。这解释了为何“更简单”的架构反而取得了更好的手部估计效果——消除了组件引导模块可能带来的信息损失或错位问题。

### 6.4 数据策略消融

**采样策略鲁棒性**：Table 14 比较了均衡采样、加权采样和拼接采样三种策略，结果显示对 SMPLer-X-H32 的 MPE 影响不显著（均衡 63.08，加权 62.12，拼接 63.32），证实方法对数据采样策略具有鲁棒性。研究最终采用均衡采样以保证每个被选数据集在每轮训练中的样本数一致，避免大规模数据集主导训练。

**数据集选择的重要性**：Table 15 通过对比实验验证了这一点。根据基准排名选择 Top 5/10 数据集训练的模型，其 MPE 显著低于选择 Bottom 5/10 数据集的模型（Top10 89.20 vs Bottom10 115.10）。这验证了基于单数据集基准测试进行数据集筛选的有效性。

**CNN 架构的缩放适用性**：Table 16 表明，在 CNN 主干（Hand4Whole）上应用数据缩放同样有效，将 MPE 从 116.59 降至 96.90。这说明缩放策略并非 ViT 架构的专属特性，具有更广泛的适用性。

**域内训练的泛化影响**：Table 13 探讨了一个关键问题——在训练中包含评估数据集的部分训练数据（域内训练）是否损害泛化能力。结果显示，域内训练确实能显著提升该数据集上的性能，但对未见过数据集（如 EHF）的泛化性能也有帮助（PVE 错误降低 20.2 mm）。这表明多源数据联合训练能够产生正向的迁移效应，而非简单的过拟合。

### 6.5 主要基准测试结果

**AGORA 测试集**（Table 6）：SMPLest-X-H40t（微调版本）取得了 96.2 mm 的 NMVE All，显著优于其他方法。值得注意的是，仅使用 AGORA 训练集的方法（标记 ∗）在 AGORA 上表现尚可，但在其他基准上泛化能力有限，再次印证了多源数据训练的必要性。

**EHF**（Table 8）：由于 EHF 没有训练集，该基准专门用于验证基础模型的迁移能力。SMPLest-X 在零样本设定下即取得领先性能，微调后进一步提升。

**UBody**（Table 9）和 **EgoBody-EgoSet**（Table 10）：SMPLest-X 在这两个具有挑战性的场景数据集上同样取得最优结果，验证了模型在遮挡、交互等复杂场景下的鲁棒性。

### 6.6 定性分析

Fig. 6 展示了 SMPLest-X 在遮挡（上排）、物体交互（中排）和挑战性手部姿态（下排）三种场景下的手部估计可视化，体现了模型的鲁棒性。Fig. 7 将 SMPLest-X-L40 和 SMPLer-X-L40 与 OSX、Hand4Whole 进行定性对比，在多种场景下 SMPLest-X 的全身估计结果更为准确，尤其是手部姿态的还原度明显优于基线方法。

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/008_Figure_6.jpg]]
*Figure 6: Visualization of hands by SMPLest-X. SMPLest-X demonstrates robust hand pose estimation in whole-body pose and shape estimation tasks across various scenarios, including occlusion (top), object interaction (middle), and challenging hand poses (bottom)*

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/011_Figure_7.jpg]]
*Figure 7: Visualization. We compare SMPLest-X-L40 and SMPLer-X-L40 with OSX [6] and Hand4Whole (H4W) [51] (trained with the MSCOCO, MPII, and Human3.6M) in various scenarios*

### 6.7 失败模式与局限性

尽管取得了显著进展，SMPLest-X 仍存在以下已知失败模式：

1. **极低分辨率或严重遮挡**：基础模型在极端条件下仍可能出现姿态估计错误。
2. **精细交互场景**：极简架构缺乏对局部区域的显式关注机制，可能在某些手部与物体精细交互的场景下不如专为部件设计的算法。
3. **伪标签噪声**：训练数据中来自 InstaVariety、UBody 等的伪 3D 标注包含不准确信息，可能影响模型精度。
4. **资源需求**：大规模训练需要 16 块 V100 GPU，对资源受限的研究者不友好。
5. **性能饱和**：在 10M 实例后性能趋于饱和，单纯增加数据量已无法带来显著收益，需要算法层面的创新突破。

### 补充图表

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/013_Table_6.jpg]]
*Table 6: AGORA test set. † denotes the methods that are finetuned on the AGORA training set. ∗denotes the methods that are trained on AGORA training set only*

![[assets/figures/papers/paper_list_l1650_SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimatio/figures/020_Table_13.jpg]]
*Table 13: Impact of in-domain training. We investigate the impact of seeing the train split of a benchmark dataset during training and how this may affect the generalizability of a model. The highlighted yellow shaded numbers denote that the corresponding train split is used in training. Except for 3DPW using MPJPE as the metric, other datasets are evaluated via PVE. The lower the better for all the metrics. Top-1 values are bolded, and the second best values are underlined. EgoBody: EgoBody-EgoSet. AGORA: AGORA-Val. #Row: Row number. #Data.: number of datasets. #Seen: number of evaluation benchmarks’ train splits used in the training. #Inst.: number of training instances. Unit: mm*

## 方法谱系与知识库定位

### 方法谱系：从多阶段到单阶段极简架构

SMPLest-X 的演进脉络可追溯到 EHPS 领域从多阶段流水线向单阶段框架的范式转移。早期方法 **PyMAF-X** 采用多阶段回归策略，将人体检测、姿态估计和参数回归解耦为独立模块。此后，**OSX** 首次提出基于 ViT 骨干的一阶段框架，将定位与参数估计整合为单一过程，成为该方向的重要转折点。随后出现的 **AiOS** 和 **Multi-HMR** 延续了这一思路，进一步验证了单阶段范式的有效性。

SMPLer-X 在单阶段框架中保留了**组件引导模块**（Component Guiding module），通过显式的手部和面部定位中间步骤来辅助分部估计，这一设计直观地符合“分而治之”的思路。SMPLest-X 的关键突破在于**彻底移除该模块**，代之以纯 6 层 Transformer 解码器，不包含任何显式的分部建模。这一极简设计的动机源于一个反直觉的发现：显式部件引导并非必需，反而可能限制模型学习全局上下文中的手部表征能力。实验表明，SMPLest-X 的手部 PA-MPE 比 SMPLer-X 低 15%，手部 MPE 低 13%（Table 5），验证了“少即是多”的架构哲学。

### 与基线方法的关系定位

在 EHPS 方法谱系中，SMPLest-X 占据“通用基础模型 + 极简架构”的独特位置：

- **相较于 OSX / AiOS / Multi-HMR**：这些方法虽然也采用单阶段范式，但训练数据规模有限（通常为单数据集或少量数据集组合），跨场景泛化能力受限于领域鸿沟。SMPLest-X 通过 40 个数据集、10M 实例的大规模训练，将全身 MPE 从 110 mm 以上降至 60 mm 以下（Fig. 1），实现了数量级的性能跨越。

- **相较于 SMPLer-X**：两者共享相同的 ViT 骨干和数据缩放策略，但 SMPLest-X 通过架构简化实现了手部估计的显著提升。这一差异揭示了缩放策略与架构设计之间的交互效应：在数据充足时，Transformer 解码器的自注意力机制能自主学习分部关注，无需显式引导。

- **相较于 Hand4Whole**：作为基于 CNN 的手部估计方法，Hand4Whole 在数据缩放实验中同样受益（MPE 从 116.59 降至 96.90，Table 16），表明缩放策略具有架构通用性，但 CNN 骨架的收益上限低于 ViT。

- **相较于 HybrIK-X**：多阶段方法的代表，在单数据集训练场景下可能具有领域内优势，但跨基准泛化能力显著弱于大规模训练的基础模型。

### 适用边界与关键局限

**数据缩放边际收益递减**：训练实例从 7.5M 增至 10M 时，每 epoch 训练时间从 23 小时增至 33 小时（计算成本增加 43%），但性能提升甚微（Section 5.3）。这表明在现有架构下，数据缩放已接近饱和点，单纯增加数据量不再具有成本效益。

**伪标签噪声风险**：训练数据中包含 InstaVariety、UBody 等伪标签数据集，其 3D 标注由自动方法生成，可能引入系统性噪声。虽然大规模训练对标注噪声具有一定鲁棒性，但在精细交互场景下，噪声标注可能限制模型精度上限。

**极端场景鲁棒性不足**：极简架构缺乏对局部区域（手、脸）的显式关注机制，在极低分辨率或严重遮挡的图像中仍可能出现姿态估计错误。在需要精细手-物交互理解的场景（如 ARCTIC 基准）中，专为部件设计的算法可能仍具优势。

**资源门槛高**：大规模训练需要 16 块 V100 GPU，对资源受限的研究者不友好，限制了方法的可复现性和社区推广。

### 开放问题

1. **突破缩放饱和点**：如何通过算法创新（如更高效的注意力机制、结构化稀疏训练）突破数据缩放带来的性能饱和点，而非单纯依赖更大规模的数据和模型？

2. **精细交互场景的架构补充**：在保持极简架构的前提下，是否可以通过轻量级的注意力引导或条件化模块，进一步提高手部与物体交互场景的估计精度，同时不牺牲整体简洁性？

3. **高效数据筛选策略**：当前采用均衡采样策略（Table 14 表明采样策略对性能影响不显著），但 Top 5/10 数据集训练的模型 MPE 显著低于 Bottom 5/10（Table 15）。是否可以使用主动学习或基于难度的数据筛选策略，以更少的高价值数据达到同等或更好的性能？

4. **泛化极限探索**：所训练的通用基础模型在未见过的自然环境（极端光照、非常规视角、非人类运动模式）下的泛化极限如何？当前 EHF 的域外测试（Table 8）提供了初步证据，但更系统的分布外泛化评估仍有待开展。

5. **下游任务迁移**：该基础模型学习到的全身表征能否无缝迁移到其他人体相关下游任务（如动作识别、手势生成、人-物交互检测）？这一方向尚未在本文中探索。

## 原文 PDF

![[paperPDFs/TPAMI_2025/SMPLest_X_Ultimate_Scaling_for_Expressive_Human_Pose_and_Shape_Estimation.pdf]]