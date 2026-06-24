---
title: "CoSMo3D: Open-World Promptable 3D Semantic Segmentation through LLM-Guided Canonical Spatial Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CoSMo3D_Open_World_Promptable_3D_Semantic_Segmentation_through_LLM_Guided_Canonical_Spatial_Modeling.pdf
project_link: null
code_link: "https://github.com/JinLi998/CoSMo3D/tree/main"
aliases:
- CoSMo3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入可学习的潜在规范参考框架，通过LLM引导的跨类别规范数据集和双分支架构中的规范映射锚定损失与规范框校准损失，将不同姿态、对称性和形状变体下的同一功能部件映射到稳定的规范嵌入，从而消除姿态变异，实现空间语义的鲁棒迁移。
primary_logic: 将开放世界3D分割重构为基于规范空间规律的推理，而非在输入姿态空间中进行几何-文本匹配。通过从数据中学习一个跨类别共享的潜在规范参考系，使语义部分在规范空间中的分布一致且姿态无关，从而大幅提升分割的准确性和稳定性。
claims:
- CoSMo3D在多个基准上均取得最优结果，在3DCompat和ShapeNet-Part上的平均mIoU分别比最强基线提高25.55%和29.89%。
- 在消融实验中，完整模型（含规范映射锚定、规范框校准和跨类别规范数据）达到47.51 mIoU，相比基线Find3D提升10.62个点。
- 定性结果显示，CoSMo3D在几何相似但语义不同、跨类别语义和任意姿态等挑战性场景中均能产生更准确且一致的部件分割。
- "3DCompat-Coarse (canonical {Part} of {Obj.}) 上 mIoU = 47.51"
---

# CoSMo3D: Open-World Promptable 3D Semantic Segmentation through LLM-Guided Canonical Spatial Modeling

> [!tip] 核心洞察
> 将开放世界3D分割重构为基于规范空间规律的推理，而非在输入姿态空间中进行几何-文本匹配。通过从数据中学习一个跨类别共享的潜在规范参考系，使语义部分在规范空间中的分布一致且姿态无关，从而大幅提升分割的准确性和稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CoSMo3D：基于大语言模型引导的规范空间建模的开放世界可提示3D语义分割 |
| 英文题名 | CoSMo3D: Open-World Promptable 3D Semantic Segmentation through LLM-Guided Canonical Spatial Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jin_CoSMo3D_Open-World_Promptable_3D_Semantic_Segmentation_through_LLM-Guided_Canonical_Spatial_CVPR_2026_paper.html) · [Code](https://github.com/JinLi998/CoSMo3D/tree/main) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CoSMo3D |
| Dataset | 3DCompat-Coarse, 3DCompat-Fine, ShapeNet-Part, PartNet-E |

> [!tip] 效果简介
> - 3DCompat-Coarse (canonical {Part} of {Obj.}) 上，mIoU 47.51 vs 18.64 (Find3D*) (+28.87)。
> - 3DCompat-Coarse (canonical {Part}) 上，mIoU 54.52 vs 24.35 (Find3D*) (+30.17)。
> - 3DCompat-Fine (canonical {Part} of {Obj.}) 上，mIoU 36.69 vs 13.12 (Find3D*) (+23.57)。

## 概述

开放世界可提示3D语义分割旨在根据任意文本描述，在任意姿态和形状的3D对象中定位语义部件。现有方法（如**Find3D**，Ma et al., ICCV 2025）直接在输入传感器坐标空间中进行几何-文本匹配，缺乏规范空间感知能力，导致在面对姿态变化、形状对称性和跨类别场景时，同一功能部件的分割结果不一致。其根本瓶颈在于：这些方法未能像人类一样，在一个姿态无关的规范参考系中理解部件的功能语义。

本文提出**CoSMo3D**，将开放世界3D分割重构为基于规范空间规律的推理问题。核心思路是：从数据中学习一个跨类别共享的潜在规范参考框架，使语义部件在规范空间中的分布保持稳定且姿态无关，从而消除姿态变异对分割的干扰。为实现这一目标，方法引入双分支架构，在训练时通过规范映射锚定损失和规范框校准损失，将不同姿态、对称性和形状变体下的同一功能部件映射到一致的规范嵌入；同时，利用大语言模型（LLM）指导构建跨类别规范数据集，覆盖200个类别，暴露跨类别的规范空间规律。

实验结果表明，CoSMo3D在多个基准上均取得最优性能：在3DCompat粗粒度数据集上，平均mIoU达到47.51（`canonical {Part} of {Obj.}`设定），较最强基线**Find3D***提升25.55个百分点；在ShapeNet-Part上，mIoU达到36.16，提升29.89个百分点。消融实验证实，规范映射锚定和跨类别规范化是性能提升的关键驱动因素，而规范框校准进一步强化了部件边界的一致性。定性结果显示，CoSMo3D在几何相似但语义不同、跨类别语义和任意姿态等挑战性场景中，均能产生更准确且一致的部件分割。

## 背景与动机

### 问题背景：开放世界可提示3D语义分割

3D语义分割旨在将点云中的每个点赋予语义标签，是三维视觉理解的核心任务。传统全监督方法依赖封闭的类别集合和大量人工标注，难以扩展到现实世界中不断涌现的新物体类别。开放世界可提示3D语义分割（open-world promptable 3D semantic segmentation）通过引入文本提示作为语义桥梁，允许用户以自然语言指定任意部件类别，从而突破封闭类别限制，实现对新概念的无标注识别。

这一范式近年受到广泛关注，代表性工作包括 **PointCLIP V2**（Zhu et al., ICCV 2023）利用CLIP和GPT实现开放世界3D理解，**PartSLIP++**（Zhou et al., arXiv 2023）借助多视图2D基础模型进行低样本3D部件分割，**PartField**（Liu et al., ICCV 2025）通过特征场对比学习实现类别无关的部件分割，以及 **Find3D**（Ma et al., ICCV 2025）直接基于几何-文本对齐进行可提示分割。

### 现有方法的瓶颈：缺乏规范空间感知

尽管上述方法在开放世界分割上取得了进展，但它们共享一个根本性局限：**仅在输入传感器坐标中进行几何-文本匹配，缺乏规范空间感知**。这种“仅几何映射”的策略在以下场景中暴露出严重缺陷：

1. **姿态变化**：同一物体在不同姿态下，其部件的空间坐标发生全局变换，导致几何特征与语义标签的对应关系不稳定。
2. **对称性歧义**：对称物体（如椅子、桌子）存在多个等效姿态，逐点几何标注本身具有歧义，直接监督不可靠。
3. **跨类别泛化**：不同类别的物体即使共享功能部件（如“腿”、“把手”），其几何形态和空间布局差异巨大，缺乏统一的参考系使得语义迁移困难。

从认知角度看，人类在理解物体部件时，天然具备在规范参考系中推理的能力——我们不会因为椅子旋转了45度就认不出它的“椅腿”。这种**规范空间感知**正是现有方法所缺失的。

### 核心动机：将分割重构为规范空间推理

本文的核心洞察是：**开放世界3D分割应被重构为基于规范空间规律的推理，而非在输入姿态空间中进行几何-文本匹配**。具体而言，如果能从数据中学习一个跨类别共享的潜在规范参考框架，使语义部件在该空间中的分布一致且姿态无关，就能从根本上消除姿态变异对分割的干扰，实现空间语义的鲁棒迁移。

这一思路面临两个关键挑战：其一，如何在不依赖人工标注的情况下构建跨类别的规范对齐数据；其二，如何设计网络架构和损失函数，使模型在训练过程中自发地诱导出稳定的规范参考系。

### 本文方案概述

针对上述挑战，本文提出 **CoSMo3D**，一种基于大语言模型引导的规范空间建模方法。其核心设计包括：

- **LLM引导的跨类别规范数据集**：利用大语言模型的常识推理能力，对200个物体类别进行语义聚类和规范对齐，构建统一的规范空间监督信号。
- **双分支架构与规范正则化**：在特征提取分支之外，引入仅训练时使用的规范嵌入分支，通过规范映射锚定损失和规范框校准损失，强制模型学习姿态鲁棒的规范空间表征。

通过这一设计，CoSMo3D在多个基准上均取得最优结果：在3DCompat和ShapeNet-Part上的平均mIoU分别比最强基线提升25.55%和29.89%（Table 1），并在几何相似但语义不同、跨类别语义和任意姿态等挑战性场景中展现出显著更优的分割一致性和准确性（Figure 5）。

## 核心创新

CoSMo3D的核心思想是将开放世界3D语义分割从“输入姿态空间中的几何-文本匹配”重构为“基于规范空间规律的推理”。现有方法（如**Find3D**，Ma et al., ICCV 2025）直接在传感器坐标系下进行点云与文本的对齐，缺乏对物体规范姿态的感知，导致在姿态变化、对称性和跨类别场景下语义分割不一致——无法像人类一样在规范参考系中理解部件的功能含义。CoSMo3D通过从数据中学习一个跨类别共享的潜在规范参考框架，使语义部件在规范空间中的分布一致且姿态无关，从而大幅提升分割的准确性和稳定性。

为实现这一目标，CoSMo3D在基线方法的基础上引入了以下关键创新（changed slots）：

**1. 规范空间推理机制（从“无”到“双分支架构”）**

基线方法仅在输入姿态空间进行几何-文本匹配，缺乏规范空间感知。CoSMo3D引入了一个双分支架构（Figure 2）：特征提取分支负责跨模态部件分割，输出点-文本相似度；训练时专用的规范嵌入分支则通过两个预测头——规范映射预测头（回归连续的规范RGB颜色场）和语义边界框预测头（以文本特征为查询输出每个语义部件的3D规范边界框）——强制模型学习姿态无关的规范空间表示。这一设计使得模型在推理时无需显式进行规范变换，即可隐式地利用规范空间规律进行鲁棒分割。

**2. 训练数据的跨类别规范化（从“类别内规范化”到“LLM引导的跨类别规范对齐”）**

先前工作仅在类别内部进行规范化，忽略了跨类别之间的空间一致性。CoSMo3D利用大语言模型对200个类别进行聚类，并依据关键语义部件和功能一致性对不同类别进行对齐（Figure 3），构建了一个统一的跨类别规范数据集。这一数据层面的创新暴露了跨类别的规范空间规律，为模型学习通用的规范参考框架提供了监督基础。

**3. 困难负样本采样策略（从“均匀点采样”到“边界困难负样本采样”）**

在语义对比对齐损失中，CoSMo3D从部件间边界采样更具判别性的负样本，替代均匀点采样策略，增强了模型对语义模糊和边界噪声的鲁棒性。对应的双向对比损失为：

$$\mathcal { L } _ { h } = \frac { 1 } { 2 M } \sum _ { i = 1 } ^ { M } - \log \frac { f ( \bar { \bf p } _ { i } , { \bf t } _ { i } ) } { \sum _ { k \in \{ { \bf B } _ { i } \} } f \big ( \bar { \bf p } _ { i } , { \bf t } _ { k } \big ) } - \log \frac { f ( { \bf t } _ { i } , \bar { \bf p } _ { i } ) } { \sum _ { n \in \mathcal { P } _ { i } } f \big ( { \bf t } _ { n } , \hat { \bf p } _ { n } \big ) }$$

**4. 规范映射锚定损失（从“无”到“分布级Chamfer距离对齐”）**

针对对称物体存在的逐点规范标签歧义问题（Figure 4），CoSMo3D将每个语义部件视为规范空间中的一个分布，使用双向Chamfer距离对预测规范点集与真值规范点集进行分布级匹配，而非逐点对齐：

$$\mathcal { L } _ { c a } = \frac { 1 } { M } \sum _ { m = 1 } ^ { M } \Big ( \frac { 1 } { | { \mathcal G } _ { m } ^ { p } | } \sum _ { { \bf a } _ { i } \in { \mathcal G } _ { m } ^ { p } } \operatorname* { m i n } _ { { \bf b } _ { j } \in { \mathcal G } _ { m } ^ { t } } \| { \bf a } _ { i } - { \bf b } _ { j } \| _ { p } + \frac { 1 } { | { \mathcal G } _ { m } ^ { t } | } \sum _ { { \bf b } _ { j } \in { \mathcal G } _ { m } ^ { t } } \operatorname* { m i n } _ { { \bf a } _ { i } \in { \mathcal G } _ { m } ^ { p } } \| { \bf b } _ { j } - { \bf a } _ { i } \| _ { p } \Big )$$

这种顺序无关的集合损失自动处理了对称歧义，无需类别特定的对称性标注，具备良好的开放世界可扩展性。

**5. 规范框校准损失（从“无”到“3D边界框L1约束”）**

进一步引入语义部件的3D规范边界框监督，通过L1损失校准部件的空间范围：

$$\mathcal { L } _ { \mathrm { c b } } = \frac { 1 } { M } \sum _ { m = 1 } ^ { M } \frac { 1 } { 6 } \left\| \mathbf { b } _ { m } ^ { \mathrm { p } } - \mathbf { b } _ { m } ^ { \mathrm { t } } \right\| _ { 1 } , \quad \mathbf { b } _ { m } ^ { \mathrm { ( \cdot ) } } \in \mathbb { R } ^ { 6 }$$

总训练目标为上述损失的加权组合：

$${ \mathcal { L } } _ { \mathrm { t o t a l } } = \lambda _ { h } \cdot { \mathcal { L } } _ { h } + \lambda _ { c a } \cdot { \mathcal { L } } _ { c a } + \lambda _ { c b } \cdot { \mathcal { L } } _ { c b }$$

其中权重分别为 $\lambda_h = 1$，$\lambda_{ca} = 10$，$\lambda_{cb} = 3$。

这些创新的因果机制在于：规范映射锚定损失提供了姿态鲁棒的规范空间特征，跨类别规范数据暴露了通用的空间规律，而规范框校准损失进一步强化了部件边界的一致性。消融实验（Table 2）定量验证了这一因果链条：添加规范映射锚定后mIoU从38.12提升至42.23（+4.11），加入跨类别规范数据后提升至43.34（+1.11），最终加入框校准损失后达到完整的47.51（+4.17），相比基线Find3D累计提升10.62个点。

## 整体框架

CoSMo3D 的整体框架围绕一个核心思想展开：**将开放世界3D语义分割重构为基于规范空间规律的推理，而非在输入姿态空间中进行几何-文本匹配**。为此，方法引入一个从数据中直接学习的潜在规范参考框架，使语义部件在规范空间中的分布一致且姿态无关，从而消除姿态变异对分割的干扰。

### 双分支架构

CoSMo3D 采用双分支架构（Figure 2），包含一个始终激活的**特征提取分支**和一个仅在训练时使用的**规范嵌入分支**：

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/002_Figure_2.jpg]]
*Figure 2: We propose a dual-branch framework for open-world promptable 3D semantic segmentation: the feature extraction branch encodes 3D shape features (via Point Transformer) and text semantic features (via SigLIP) to enable cross-modal part segmentation. A training-only canonical embedding branch then enforces consistent canonical space perception via semantic contrastive alignment, canonical map anchoring, and canonical box calibration losses, ensuring robust reasoning across any shape in any pose*

- **特征提取分支**：负责跨模态部件分割。3D形状特征通过 **Point Transformer (Pt3)** 骨干网络提取，文本语义特征通过 **SigLIP** 文本编码器编码。该分支输出点-文本相似度，实现可提示的语义分割。
- **规范嵌入分支**：在训练阶段强制模型学习一致的规范空间感知。该分支包含两个预测头：
  - **规范映射预测头**：以3D形状特征为输入，回归三个连续标量场（编码为RGB颜色图），锚定每个语义部件在规范空间中的分布。
  - **语义边界框预测头**：以文本特征为查询，输出每个语义部件的3D规范边界框，强化部件空间范围的边界一致性。

### 训练数据构建

为暴露跨类别的规范空间规律，CoSMo3D 构建了一个统一的规范数据集，覆盖200个类别。与先前工作仅进行类别内规范化不同，该方法通过 **LLM引导的跨类别对齐流水线**，利用大语言模型对类别进行聚类，并依据关键语义部件和功能一致性对齐不同类别，从而实现跨类别规范空间的统一（Figure 3）。

### 训练损失与推理流程

训练阶段，总损失由三项加权组成：

$${ \mathcal { L } } _ { \mathrm { t o t a l } } = \lambda _ { h } \cdot { \mathcal { L } } _ { h } + \lambda _ { c a } \cdot { \mathcal { L } } _ { c a } + \lambda _ { c b } \cdot { \mathcal { L } } _ { c b }$$

其中 $\lambda_h=1$、$\lambda_{ca}=10$、$\lambda_{cb}=3$。三项损失分别为：

1. **语义对比对齐损失** $\mathcal{L}_h$：结合困难负样本采样的双向对比损失，负样本从部件间边界采样，增强对语义模糊和边界噪声的鲁棒性。
2. **规范映射锚定损失** $\mathcal{L}_{ca}$：对每个语义部件，计算预测规范点集与真值规范点集之间的双向Chamfer距离，以分布匹配代替逐点对齐，自动处理对称歧义（Figure 4）。
3. **规范框校准损失** $\mathcal{L}_{cb}$：预测的3D规范边界框与真值之间的L1损失，校准部件空间范围。

推理时，规范嵌入分支被移除，仅使用特征提取分支进行前向传播，在GPU上仅需约0.6–0.9秒即可完成单个形状的分割。

### 补充图表

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/001_Figure_1.jpg]]
*Figure 1: We propose CoSMo3D, an open-world promptable 3D semantic segmentation method. It introduces canonical space perception to break the limitation of any pose and shape, achieves state-of-the-art performance across multiple settings, and significantly outperforms geometry-mapping-only methods*

## 核心模块与公式推导

CoSMo3D 的整体框架（Figure 2）由两条分支构成：**特征提取分支**（推理时使用）和**规范嵌入分支**（仅训练时使用）。特征提取分支以 Point Transformer（Pt3）骨干网络提取 3D 形状特征，以 SigLIP 文本编码器提取文本语义特征，并通过跨模态对齐输出点-文本相似度，实现可提示的部件分割。规范嵌入分支则承担核心的规范空间感知学习任务，包含两个预测头：**规范映射预测头**和**语义边界框预测头**，两者共同将不同姿态、对称性和形状变体下的同一功能部件映射到稳定的潜在规范参考框架。

### 困难负样本对比对齐

在特征提取分支中，模型需要对 3D 点特征与文本特征进行对比对齐。直接采用均匀采样的负样本策略在面对语义边界模糊或几何相似的部件时判别力不足。为此，CoSMo3D 引入**困难负样本采样**策略：不再从所有点中均匀采样负样本，而是从部件间边界区域采样更具判别难度的负样本。对应的双向对比损失为：

$$\mathcal{L}_h = \frac{1}{2M} \sum_{i=1}^{M} \left[ -\log \frac{f(\bar{\mathbf{p}}_i, \mathbf{t}_i)}{\sum_{k \in \{\mathbf{B}_i\}} f(\bar{\mathbf{p}}_i, \mathbf{t}_k)} - \log \frac{f(\mathbf{t}_i, \bar{\mathbf{p}}_i)}{\sum_{n \in \mathcal{P}_i} f(\mathbf{t}_n, \hat{\mathbf{p}}_n)} \right]$$

其中 $\bar{\mathbf{p}}_i$ 为第 $i$ 个语义部件的平均池化点特征，$\mathbf{t}_i$ 为对应文本特征，$\{\mathbf{B}_i\}$ 为从部件间边界采样的困难负样本集，$\mathcal{P}_i$ 为点视角下的负样本集，$f(\cdot,\cdot)$ 为余弦相似度函数。该损失通过双向对比增强了模型对语义模糊和边界噪声的鲁棒性。

### 规范映射锚定损失

规范映射预测头以 3D 形状特征为输入，回归三个连续的标量场（编码为 RGB 颜色图），为每个点赋予规范空间坐标。监督这一预测的核心挑战在于：对称物体存在多个有效姿态，导致逐点的规范坐标真值存在歧义（Figure 4a）。CoSMo3D 的关键洞察是**避免建立逐点对应关系**，转而将每个语义部件视为规范空间中的一个分布，通过分布级匹配进行监督。具体而言，对每个语义部件 $m$，计算其预测规范点集 $\mathcal{G}_m^p$ 与真值规范点集 $\mathcal{G}_m^t$ 之间的双向 Chamfer 距离：

$$\mathcal{L}_{ca} = \frac{1}{M} \sum_{m=1}^{M} \left( \frac{1}{|\mathcal{G}_m^p|} \sum_{\mathbf{a}_i \in \mathcal{G}_m^p} \min_{\mathbf{b}_j \in \mathcal{G}_m^t} \|\mathbf{a}_i - \mathbf{b}_j\|_p + \frac{1}{|\mathcal{G}_m^t|} \sum_{\mathbf{b}_j \in \mathcal{G}_m^t} \min_{\mathbf{a}_i \in \mathcal{G}_m^p} \|\mathbf{b}_j - \mathbf{a}_i\|_p \right)$$

该损失以分布匹配代替逐点对齐，自动处理对称歧义：只要预测的规范点集在整体布局上与真值分布一致，即可获得低损失，而无需关心对称变换下的逐点对应（Figure 4c）。这使得方法无需类别特定的对称性标注，天然适应开放世界场景。

### 规范框校准损失

语义边界框预测头以文本特征为查询，输出每个语义部件的 3D 规范边界框 $\mathbf{b}_m^p \in \mathbb{R}^6$（格式为 $[x_{\min}, y_{\min}, z_{\min}, x_{\max}, y_{\max}, z_{\max}]$）。该预测通过 L1 损失与真值边界框 $\mathbf{b}_m^t$ 对齐：

$$\mathcal{L}_{cb} = \frac{1}{M} \sum_{m=1}^{M} \frac{1}{6} \left\| \mathbf{b}_m^p - \mathbf{b}_m^t \right\|_1$$

该损失显式约束了每个语义部件在规范空间中的空间范围，强化了部件边界的几何一致性，与规范映射锚定损失形成互补。

### 总训练目标

完整的训练目标为上述三个损失的加权和：

$$\mathcal{L}_{total} = \lambda_h \cdot \mathcal{L}_h + \lambda_{ca} \cdot \mathcal{L}_{ca} + \lambda_{cb} \cdot \mathcal{L}_{cb}$$

其中权重设置为 $\lambda_h = 1$，$\lambda_{ca} = 10$，$\lambda_{cb} = 3$。规范映射锚定损失被赋予最高权重，体现了规范空间感知在整个方法中的核心地位。消融实验（Table 2）验证了这一设计：逐步加入各损失项后，mIoU 从基线的 36.89 持续提升至完整模型的 47.51，其中规范映射锚定损失贡献了最大幅度的性能跃升（+4.11 mIoU）。

### 补充图表

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/003_Figure_3.jpg]]
*Figure 3: (a) Prior works perform category-level canonicalization, aligning intra-category shapes but neglecting cross-category consistency. (b) We cluster categories via LLM and align different categories relying on key semantic parts and functional consistency*

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/004_Figure.jpg]]
*Figure: (c) Ours: Learning the Canonical Map via Semantic Parts Enables Open-World Adaptation,No Category-Specific Design Needed*

## 实验与分析

### 主要定量结果

CoSMo3D 在多个基准上全面超越现有方法，验证了规范空间感知对开放世界可提示3D分割的核心价值。Table 1 汇总了粗粒度、细粒度及跨数据集设置下的 mIoU 对比。

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation for promptable semantic segmentation (with semantic labels as reference and mean IoU reported). Top: coarse-grained dataset and fine-grained dataset; Bottom: ShapeNet-Part dataset and PartNet-E dataset. Find3D∗ denotes retraining using the 3D data we constructed; PartSLIP++∗ denotes fine-tuning on the PartNet-E dataset with canonical views as input*

在 3DCompat-Coarse 基准上，CoSMo3D 在 canonical {Part} of {Obj.} 设定下达到 **47.51 mIoU**，较最强基线 Find3D*（18.64）提升 **+28.87 点**；在 canonical {Part} 设定下达到 **54.52 mIoU**，提升 **+30.17 点**。在更细粒度的 3DCompat-Fine 上，CoSMo3D 取得 **36.69 mIoU**，较 Find3D*（13.12）提升 **+23.57 点**。平均来看，CoSMo3D 在 3DCompat 系列基准上较 Find3D 提升 **25.55%**。

在跨数据集泛化方面，CoSMo3D 同样表现突出：在 ShapeNet-Part 上达到 **36.16 mIoU**，较 Find3D*（6.27）提升 **+29.89 点**；在 PartNet-E 上达到 **34.20 mIoU**，较 PartSLIP++*（29.19）提升 **+5.01 点**。

值得注意的是，纯3D方法（Find3D* 和 CoSMo3D）在 GPU 上仅需 **0.6–0.9 秒/形状**，而基于2D多视图转换的 PartSLIP++ 耗时约 150 秒/形状，表明 CoSMo3D 在精度与效率上均具优势。

### 消融实验

Table 2 系统拆解了各组件对性能的贡献，以 3DCompat-Coarse canonical {Part} of {Obj.} 的 mIoU 为指标，基线为 Find3D 的 36.89 mIoU：

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study. All values are mIoU scores computed over parts from all instances across all categories*

1. **困难负样本采样**：将 mIoU 从 36.89 提升至 **38.12**（+1.23），通过在部件间边界采样更具判别性的负样本，增强了对比对齐对语义模糊和边界噪声的鲁棒性。
2. **规范映射锚定损失**：加入后 mIoU 跃升至 **42.23**（+4.11），这是单组件中增益最大的改动，直接验证了将语义部件建模为规范空间分布并施加分布级对齐的有效性。
3. **跨类别规范化数据**：进一步将 mIoU 推至 **43.34**（+1.11），证明 LLM 引导的跨类别规范对齐（覆盖200个类别）为模型提供了更丰富的空间规律监督信号。
4. **规范框校准损失**：最终完整模型达到 **47.51 mIoU**（+4.17），框约束强化了部件边界一致性，与规范映射锚定形成互补。

消融趋势清晰表明：**规范空间感知（锚定+框校准）是性能提升的主驱动力**，跨类别数据与困难负采样则在此基础上提供增量增益。

### 定性分析

Figure 5 展示了 CoSMo3D 在四类挑战性场景下的分割效果：

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of promptable 3D part segmentation. Across challenging cases (similar geometry with different semantics, noise-prone objects, cross-category semantics, and arbitrary poses), our method produces more accurate and consistent part localizations than existing baselines*

- **几何相似但语义不同**：如桌腿与椅腿，CoSMo3D 能准确区分，而几何-文本匹配方法（Find3D）容易混淆。
- **噪声敏感物体**：在点云质量较差时，CoSMo3D 的部件定位仍保持稳定。
- **跨类别语义**：同一功能部件（如“把手”）在不同类别物体上被一致地分割出来。
- **任意姿态**：无论物体处于何种旋转或姿态，CoSMo3D 的分割结果保持一致。

Figure 6 从特征层面揭示了性能差异的根源：PartField 虽能产生清晰的部件分区，但跨形状和跨姿态一致性差；Find3D 改善了一致性，但部件边界模糊；**CoSMo3D 同时实现了清晰的部件分离和跨形状/姿态的稳定特征表达**，这正是规范空间感知带来的核心优势。

![[assets/figures/papers/paper_list_l2032_https_openaccess_thecvf_com_content_CVPR2026_html_Jin_CoSMo3D_Open_World/figures/008_Figure_6.jpg]]
*Figure 6: Shape feature analysis. (a) PartField [11] yields clear part partitions but lacks cross-shape and cross-pose consistency. (b) Find3D [13] improves consistency but produces blurry part boundaries. (c) Our method achieves both clear part separation and consistent features across shapes and poses*

### 失败模式与局限性

论文未系统报告失败案例，但根据方法设计可推断以下潜在风险：

1. **极端非刚性变形**：规范参考框架通过学习刚性姿态变换的规律来稳定语义空间，对于可变形物体（如软体动物、折叠家具）的大幅非刚性变化，当前框架可能失效——这一点需要手动验证。
2. **未见类别的泛化边界**：虽然跨类别规范数据集覆盖了200个类别，但对于与训练类别空间结构差异极大的全新类别（如工具类 vs. 家具类），规范空间规律能否迁移仍存疑。
3. **LLM 聚类质量依赖**：跨类别规范对齐依赖 LLM 对类别功能相似性的判断。若 LLM 聚类不合理（如将功能无关类别归入同一规范组），可能导致规范空间混乱而非对齐——论文未对此进行消融分析。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | CoSMo3D 在全部基准上显著超越基线，平均提升 25–30 mIoU 点 |
| Table 2 | 规范映射锚定和框校准是性能提升的主因，合计贡献超 8 个 mIoU 点 |
| Figure 5 | 在几何混淆、噪声、跨类别和任意姿态场景下，分割更准确且一致 |
| Figure 6 | 规范空间感知使点特征同时具备部件分离度和跨实例一致性 |

## 方法谱系与知识库定位

### 1. 方法定位与核心区分

CoSMo3D 将开放世界可提示 3D 语义分割重构为**基于规范空间规律的推理**，而非在输入姿态空间中进行几何-文本匹配。这一视角转变使其与现有基线方法形成了根本性差异：

- **Find3D**（Ma et al., ICCV 2025）：作为直接对比的开放世界可提示 3D 分割基线，Find3D 仅在输入传感器坐标中进行跨模态对齐，缺乏规范空间感知能力。当物体处于任意姿态或存在对称性时，其几何-文本匹配容易产生语义混淆。CoSMo3D 通过在训练时引入可学习的潜在规范参考框架，将语义部件映射到姿态无关的稳定嵌入空间，从根本上解耦了姿态变异与语义理解。

- **PartSLIP++**（Zhou et al., arXiv 2023）：低样本 3D 部件分割方法，依赖多视图 2D 视觉-语言模型（如 CLIP）进行 3D 语义迁移。其推理时间约 150 秒/形状，远高于纯 3D 方法的 0.6–0.9 秒。更重要的是，PartSLIP++ 缺乏显式的规范空间建模，跨姿态一致性依赖视图覆盖度而非结构化空间推理。

- **PointCLIP V2**（Zhu et al., ICCV 2023）：基于 CLIP 和 GPT 的开放世界 3D 理解方法，侧重全局形状-文本对齐，未针对细粒度部件分割设计专门的规范空间约束。

- **PartField**（Liu et al., ICCV 2025）：类别无关的 3D 部件分割方法，通过特征场对比学习实现部件划分。CoSMo3D 的特征可视化分析（Figure 6）显示，PartField 虽能产生清晰的部件分界，但缺乏跨形状和跨姿态的特征一致性；Find3D 改善了一致性但部件边界模糊；CoSMo3D 则同时实现了清晰的部件分离和跨实例的稳定特征表达。

### 2. 关键技术谱系

CoSMo3D 的方法设计可定位于以下技术谱系的交汇点：

| 技术维度 | 基线/前序工作 | CoSMo3D 的推进 |
|---------|-------------|---------------|
| **规范空间建模** | 仅类别内规范化（category-level canonicalization） | LLM 引导的跨类别规范化，覆盖 200 类别，实现功能语义驱动的跨类别对齐 |
| **对比采样策略** | 均匀点采样（Find3D 等） | 从部件间边界采样的困难负样本策略，增强语义边界鲁棒性 |
| **规范监督信号** | 无显式规范约束 | 双头规范嵌入分支：规范映射锚定损失（分布级 Chamfer 距离）+ 规范框校准损失（L1 边界框约束） |
| **对称性处理** | 类别特定对称标注（前序工作） | 顺序无关的集合损失，自动处理对称歧义，无需人工标注 |
| **训练数据构建** | 类别内规范化数据集 | LLM 指导的跨类别统一规范数据集，暴露跨类别空间规律 |

### 3. 适用边界与局限

基于论文提供的实验证据和分析，CoSMo3D 的适用边界可从以下维度界定：

**已验证的有效范围：**
- 人造物体部件分割（3DCompat、ShapeNet-Part、PartNet-E 等基准），涵盖粗粒度和细粒度语义部件
- 任意姿态下的语义一致性分割（定性结果 Figure 5 展示了跨姿态稳定性）
- 几何相似但语义不同的挑战性场景（如不同功能部件具有相似几何形态）
- 跨类别语义迁移（如“把手”在不同物体类别中的一致定位）

**潜在局限（论文未明确讨论，需进一步验证）：**
- 极端非刚性变形物体的泛化能力：当前实验主要覆盖刚性和关节式人造物体，对可变形物体（如服装、软体动物）的规范空间定义可能面临挑战
- 未见类别的大规模泛化：跨类别规范对齐依赖 LLM 对类别功能语义的先验知识，当遇到 LLM 训练数据中覆盖不足的罕见类别时，规范空间的质量可能下降
- 真实扫描数据的鲁棒性：实验主要在合成或规范化数据上进行，含噪声、缺失区域的真实扫描点云上的表现仍有待验证

### 4. 开放问题

1. **LLM 引导策略的可扩展性**：跨类别规范空间对齐依赖 LLM 产生的类别聚类质量。当类别数进一步扩大（如 >1000 类）时，聚类合理性如何保证？不合理的聚类是否会导致规范空间混乱？计算成本是否可控？

2. **规范参考框架的可迁移性**：学习到的潜在规范参考框架能否迁移到其他 3D 任务（如部件组合、3D 问答、机器人操作）并保持鲁棒性？规范嵌入是否包含可解释的几何-功能对应关系？

3. **对称性处理的边界**：顺序无关的集合损失在实验中有效处理了旋转对称等常见情况，但对于更复杂的对称模式（如分形对称、非等距对称）是否仍能保持鲁棒性？

4. **与 2D 基础模型的深度整合**：当前方法使用 SigLIP 文本编码器进行文本特征提取，未来是否可进一步利用 2D 视觉基础模型的多模态对齐能力，增强开放世界语义理解的范围和精度？

5. **实时应用场景**：尽管推理时间（0.6–0.9 秒/形状）已显著优于 2D 转换方法，但在需要毫秒级响应的实时机器人交互场景中，是否可通过模型轻量化或知识蒸馏进一步压缩？

## 原文 PDF

![[paperPDFs/CVPR_2026/CoSMo3D_Open_World_Promptable_3D_Semantic_Segmentation_through_LLM_Guided_Canonical_Spatial_Modeling.pdf]]