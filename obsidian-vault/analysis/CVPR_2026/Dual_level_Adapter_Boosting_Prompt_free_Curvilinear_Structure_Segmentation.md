---
title: Dual-level Adapter Boosting Prompt-free Curvilinear Structure Segmentation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Dual_level_Adapter_Boosting_Prompt_free_Curvilinear_Structure_Segmentation.pdf
project_link: null
code_link: "https://github.com/kylechuuuuu/SACM"
aliases:
- SSACM
- DLABPFCSS
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 双级适配器架构（DLAda）：在冻结SAM编码器的每个Transformer块中同时引入块内适配器（Adapter-I）和块间适配器（Adapter-E），前者细化局部细节，后者在块间传播全局结构性线索，并通过适配器融合（Adapter Fusion）注入掩码解码器，实现无提示、少样本的跨域曲线分割。
primary_logic: 将曲线结构的全局拓扑一致性建模为跨层特征融合问题，通过在Transformer块间引入外部适配器显式捕捉长程依赖，与内部适配器协同，从而无需交互式提示即可在仅18张标注图像上实现鲁棒的跨域曲线结构分割。
claims:
- 双级适配器组合在WIRE消融实验中带来协同增益（Dice 54.60），优于仅使用单一适配器或基线SAM。
- Grad-CAM可视化显示Adapter-E捕获全局血管结构，Adapter-I聚焦局部细节，证明互补作用。
- 在12个多样化曲线结构数据集上仅用18张训练图像即取得SOTA性能，验证跨域泛化能力。
- 无提示分割设计通过Adapter Fusion将多层外部适配器特征集成到解码器，替换了需要交互提示的原始SAM。
---

# Dual-level Adapter Boosting Prompt-free Curvilinear Structure Segmentation

> [!tip] 核心洞察
> 将曲线结构的全局拓扑一致性建模为跨层特征融合问题，通过在Transformer块间引入外部适配器显式捕捉长程依赖，与内部适配器协同，从而无需交互式提示即可在仅18张标注图像上实现鲁棒的跨域曲线结构分割。

| 字段 | 内容 |
|------|------|
| 中文题名 | 双级适配器增强的无提示曲线结构分割 |
| 英文题名 | Dual-level Adapter Boosting Prompt-free Curvilinear Structure Segmentation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhu_Dual-level_Adapter_Boosting_Prompt-free_Curvilinear_Structure_Segmentation_CVPR_2026_paper.html) · [Code](https://github.com/kylechuuuuu/SACM) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SACM (Segment Anything Curve Model) |
| Dataset | DRIVE, CHASEDB1, DCA1, CORN |

> [!tip] 效果简介
> - DRIVE 上，Dice 78.89。
> - CHASEDB1 上，Dice 79.27。
> - DCA1 上，Dice 75.67。

## 概述

曲线结构（curvilinear structures）——如视网膜血管、遥感道路、线网、轮胎纹理——广泛存在于医学影像、工业检测与遥感等领域。此类结构具有**纤细、拓扑连续且跨域形态差异巨大**的特点，使得通用分割模型难以直接迁移。**Segment Anything Model (SAM)**（Kirillov et al., ICCV 2023）虽具备强大的泛化潜力，但其依赖交互式提示（点、框、掩码），在曲线结构上提示质量高度敏感，分割结果往往局部可信而全局断裂（Figure 4）。现有基于适配器的SAM微调方法（如**SAM-Med2D**, Ma et al., Nature Communications 2024）仅将适配器插入Transformer块内部的MLP路径，仅能进行**局部特征细化**，缺乏跨层的全局上下文建模能力，无法有效捕捉曲线结构所需的长程空间依赖和拓扑连续性，导致跨域泛化性能受限。

本文提出**SACM（Segment Anything Curve Model）**，一个基于冻结SAM编码器的**无提示（prompt-free）**曲线结构分割框架。其核心创新是**双级适配器架构（DLAda）**：在每个Transformer块中同时引入**块内适配器（Adapter-I）**和**块间适配器（Adapter-E）**。Adapter-I嵌入MLP子层，进行逐token的局部细节精化；Adapter-E置于整个Transformer块的残差路径上，在块间传播全局结构性线索，显式建模跨层长程依赖。多层Adapter-E的输出通过**适配器融合模块（Adapter Fusion）**自适应加权聚合为全局结构描述符，注入掩码解码器以替代交互式提示，实现完全无提示分割。解码器进一步采用**双阶段细化**：第一阶段生成粗掩码并对多个输出头排序，第二阶段基于排序结果精细化掩码，兼顾边界精度与拓扑一致性。

在仅使用**18张标注图像**、覆盖6个域的极小训练集下，SACM在**12个多样化曲线结构数据集**上取得SOTA性能，涵盖已见域、未见过域及全新类别。Grad-CAM可视化（Figure 8）证实Adapter-E捕获全局血管结构，Adapter-I聚焦局部细节，两者功能互补。消融实验（Table 5）表明双级适配器组合带来协同增益。该方法将曲线结构的全局拓扑一致性建模为跨层特征融合问题，为少样本、跨域稠密预测提供了新的范式。

## 背景与动机

### 曲线结构分割的跨域挑战

曲线结构（curvilinear structures）广泛存在于医学影像（视网膜血管、角膜神经）、遥感图像（道路网络）、工业检测（轮胎胎面、线缆网络）和植物表型（叶片脉络）等多样化场景中。从图像中精确、完整地提取这些纤细且拓扑连续的结构，对于临床诊断、地理信息系统和工业质量控制等下游任务至关重要。

然而，曲线结构分割面临两个核心困难：**域间外观差异极大**（不同成像模态、分辨率、对比度下同一类别结构呈现迥异的视觉特征）和**拓扑连续性要求高**（局部断裂或缺失会直接破坏结构的语义完整性）。传统分割方法通常针对单一数据集设计专用架构，跨域泛化能力有限。

### 现有方法的缺口

#### 专用分割网络的局限性

以 **U-Net**（Ronneberger et al., MICCAI 2015）为代表的卷积网络及其变体（如 **CS2-Net**, Mou et al., Medical Image Analysis 2021；**BCU-Net**, Zhang et al., Computers in Biology and Medicine 2023）在特定数据集上取得了良好性能，但缺乏大规模预训练知识，面对新域时往往需要重新训练。基于 Transformer 的通用分割模型（如 **nnWNet**, Zhou et al., CVPR 2025；**SegDINO**, Yang et al., arXiv 2025）虽具备更强的特征建模能力，但在极度有限的标注样本（如仅 18 张图像）下仍难以实现鲁棒的跨域迁移。

#### 基于 SAM 的适配器方法的瓶颈

**SAM**（Segment Anything Model, Kirillov et al., ICCV 2023）作为大规模视觉基础模型，展现出强大的泛化潜力。然而，SAM 原生的交互式提示机制（点、框、掩码）在曲线结构分割中效果欠佳——Figure 4 的可视化证据表明，三种提示模态均无法引导 SAM 生成拓扑完整的分割结果。

为适配 SAM 到特定领域，参数高效微调（PEFT）方法被广泛采用。典型工作如 **SAM-Med2D**（Ma et al., Nature Communications 2024）、**CWSAM**（Pu et al., IEEE JSTARS 2025）和 **SAM-OCTA**（Wang et al., ICASSP 2024）在 Transformer 块内部的 MLP 路径中插入适配器模块，仅进行局部特征细化。这种“块内适配器”策略存在根本性局限：

> **核心瓶颈**：现有基于适配器的 SAM 微调方法仅将适配器插入 Transformer 块内部的 MLP 路径，仅能进行局部特征细化，缺乏跨层的全局上下文建模能力，导致无法有效捕捉曲线结构所需的长程空间依赖和拓扑连续性，从而限制跨域泛化性能。

具体而言，块内适配器（Adapter-I）在每个 Transformer 块内独立运作，块与块之间缺乏结构信息的显式传播通道。曲线结构的拓扑一致性本质上是一种**跨尺度、跨位置的全局约束**——例如，一根血管从视盘延伸到黄斑区，其连续性跨越多个感受野尺度，需要编码器不同层级协同建模。仅靠块内局部细化无法满足这一需求。

### 本文动机：从局部适配到全局结构感知

基于上述分析，本文提出一个关键问题：**能否将曲线结构的全局拓扑一致性建模为跨层特征融合问题，通过在 Transformer 块间引入外部适配器显式捕捉长程依赖，与内部适配器协同，从而在极少标注样本下实现鲁棒的跨域分割？**

这一动机驱动了 **SACM（Segment Anything Curve Model）** 的设计。SACM 的核心思路是构建一个**双级适配器架构（Dual-Level Adapter, DLAda）**：在冻结 SAM 编码器的每个 Transformer 块中同时引入块内适配器（Adapter-I）和块间适配器（Adapter-E），前者细化局部细节，后者在块间传播全局结构性线索。通过适配器融合（Adapter Fusion）将多层全局特征注入掩码解码器，SACM 实现了完全无提示（prompt-free）的端到端分割，从根本上规避了 SAM 原始提示机制在曲线结构上的失效问题。

## 核心创新

### 1. 瓶颈洞察：从局部适配到全局拓扑建模

现有基于适配器的SAM微调方法（如 **SAM-Med2D**，Ma et al., Nature Communications 2024；**CWSAM**，Pu et al., IEEE JSTARS 2025）仅将适配器插入Transformer块内部的MLP路径，进行逐token的通道级特征细化。这种设计存在根本性局限：适配器的雅可比矩阵在token维度上呈块对角结构，更新被限制在局部感受野内，缺乏跨层信息交互能力。对于曲线结构分割任务而言，血管、道路、线缆等目标具有固有的长程空间依赖和拓扑连续性，单一的内部适配器无法建模这种全局结构先验，导致跨域泛化性能不足。

SACM的核心洞察在于：**将曲线结构的全局拓扑一致性建模为跨层特征融合问题**。通过在Transformer块间引入外部适配器显式捕捉长程依赖，与内部适配器形成协同，从而在冻结编码器的约束下实现鲁棒的曲线结构表征学习。

### 2. 关键创新：双级适配器架构（DLAda）

SACM提出了双级适配器架构（Dual-Level Adapter, DLAda），在冻结SAM编码器的每个Transformer块中同时引入两类适配器，构成层次化的特征适应机制：

**块内适配器（Adapter-I）**：嵌入MLP子层内部，采用标准瓶颈结构——下投影 $\mathbf{W}_{\downarrow}^{I}$、GELU激活 $\mathcal{G}$、上投影 $\mathbf{W}_{\uparrow}^{I}$，通过残差连接注入MLP输出：

$$\mathbf{H}_{\mathrm{out}}^{I} = \mathrm{MLP}(\mathrm{LN}(\mathbf{Y})) + \mathbf{Y} + \mathrm{Adapter}_{\mathcal{I}}(\mathrm{LN}(\mathbf{Y}))$$

Adapter-I专注于逐token的局部细节细化，保留对纤细曲线边界的敏感性。

**块间适配器（Adapter-E）**：置于整个Transformer块的残差连接外部，形成跨层的直接信息通路：

$$\mathbf{X}^{(l+1)} = F_{l}(\mathbf{X}^{(l)}) + \mathrm{Adapter}.E\big(\mathrm{LN}(F_{l}(\mathbf{X}^{(l)}))\big)$$

Adapter-E同样采用瓶颈形式 $\mathrm{Adapter-}E(\mathbf{Y}) = \mathcal{G}(\mathbf{Y}\mathbf{W}_{\downarrow}^{E})\mathbf{W}_{\uparrow}^{E}$，但其独特之处在于操作于块的输出端，能够将当前层的全局结构线索传播至后续层，实现层次化的上下文聚合。

**协同机制**：Grad-CAM可视化（Figure 8）提供了直接证据——Adapter-E的激活图覆盖了完整的血管树结构，呈现全局性响应；而Adapter-I的激活图则聚焦于血管边缘和分叉等局部细节区域。消融实验（Table 5）进一步量化了这种协同效应：在WIRE数据集上，仅使用Adapter-I的Dice为52.43，仅使用Adapter-E为50.12，而两者联合提升至54.60，验证了局部细化与全局建模的互补增益。

### 3. 机制创新：无提示分割与适配器融合

SAM原版依赖点、框或掩码等交互式提示来引导解码器生成分割结果。然而，Figure 4的定性分析表明，对于曲线结构，三种提示模态均产生次优分割——提示难以精确覆盖细长且拓扑复杂的结构。

SACM通过**适配器融合模块（Adapter Fusion）**实现了完全无提示（Prompt-Free）分割。核心思想是将Adapter-E在多个编码器层输出的全局结构描述符聚合为统一的先验表示，替代人工提示注入解码器。具体流程为：

1. **层描述符池化**：对每层Adapter-E输出 $\mathcal{E}_l$ 进行平均池化，得到层级描述符 $\mathbf{z}_l = \mathcal{A}(\mathcal{E}_l)$。
2. **自适应权重学习**：将所有层的描述符拼接后送入FFN，经Softmax获得各层贡献权重 $\alpha = \mathrm{Softmax}(\mathrm{FFN}(\mathrm{Concat}(\mathbf{z}_1, \dots, \mathbf{z}_L)))$。
3. **加权融合与注入**：对多层特征加权求和后经MLP和上采样，通过残差连接注入解码器：$\mathbf{F}_{\mathrm{decoder}}^{\mathrm{out}} = \mathbf{F}_{\mathrm{decoder}}^{\mathrm{in}} + \mathcal{F}_{\mathrm{fusion}}$。

这一设计将Adapter-E学习到的跨层全局结构先验编码为可学习的“软提示”，使解码器在无人工干预下即可感知目标的拓扑骨架，是实现少样本（仅18张训练图像）跨域泛化的关键。

### 4. 流程创新：双阶段掩码细化

SAM原版解码器采用单次前向生成多个掩码候选，再通过IoU预测选择最优输出。对于曲线结构，单阶段解码常产生局部合理但全局不一致的预测（如血管断裂、拓扑错误）。

SACM引入**双阶段掩码细化（Dual-Stage Refinement）**：

- **Stage-1**：生成粗掩码 $\mathbf{M}^{(1)} = \mathbf{MLP}_1(\mathbf{U})$，并通过最大池化和Softmax对多个预测头进行置信度排序 $\mathbf{w} = \mathrm{Softmax}(\mathcal{M}(\mathbf{M}^{(1)}))$。
- **Stage-2**：基于排序结果重新组织特征描述符 $\mathbf{s}$，生成精细化掩码 $\mathbf{M}^{(2)} = \mathbf{MLP}_2(\mathbf{U}, \mathbf{s})$，平衡边界精度与拓扑一致性。

消融实验（Table 5）证实，双阶段细化在WIRE数据集上将Dice从单阶段的52.43提升至54.60，验证了分离粗定位与精细优化的有效性。

### 5. 创新总结：Changed Slots全景

| 维度 | 基线方法（SAM系列） | SACM创新 | 证据锚点 |
|------|---------------------|----------|----------|
| **适配器位置与层级** | 仅块内MLP适配器 | 双级适配器：块内Adapter-I + 块间Adapter-E | Figure 2, Section 3.1 |
| **提示机制** | 点/框/掩码交互式提示 | 完全无提示，Adapter Fusion替代提示 | Section 3.2.1, Figure 4 |
| **掩码解码器流程** | 单次前向+IoU选择 | 双阶段细化：粗掩码→排序→精细化 | Section 3.2.2, Figure 5 |
| **特征融合** | 仅编码器末层特征 | 多层Adapter-E输出加权FFN融合 | Formula (5)-(8) |

这四项创新共同构成了SACM的核心竞争力：在冻结SAM编码器的前提下，以极少的可训练参数（适配器瓶颈比例r=0.1最优，Figure 9a）实现了对曲线结构分割的跨域泛化，仅需18张标注图像即可在12个多样化数据集上取得SOTA性能。

## 整体框架

SACM 的整体设计遵循“冻结基础模型 + 双级适配器微调 + 无提示掩码解码”的范式，目标是在仅使用极少标注样本（18 张图像）的条件下，实现对多样化曲线结构的跨域鲁棒分割。其核心 pipeline 由四个模块串联构成，如图 Figure 3 所示。

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the SACM framework. SACM leverages the pretrained SAM as the foundation model, enhanced with dual-level adapter fine-tuning. Multi-layer features from external adapters are aggregated and integrated into the mask decoder via a dual-stage refinement mechanism to improve curvilinear structure segmentation*

**冻结 SAM 图像编码器** 作为特征提取的基础，SACM 直接复用预训练的 SAM ViT 编码器，并保持其全部参数冻结。该编码器将输入图像映射为多尺度的中间特征，为后续适配器提供强大的视觉先验，同时避免大规模微调带来的灾难性遗忘与高昂训练开销。

**双级适配器（DLAda）** 是 SACM 的核心创新模块，嵌入在冻结编码器的每一个 Transformer 块中，由两类适配器协同工作：
- **块内适配器（Adapter-I）** 置于每个 Transformer 块的 MLP 子层内部，通过 token-wise 的瓶颈结构对通道维进行局部特征细化，专注于增强细薄曲线结构的细节表达。其数学形式为 $\mathrm{Adapter}_{\mathcal{I}}(\mathbf{X}) = \mathcal{G}(\mathbf{X} \mathbf{W}_{\downarrow}^{I}) \mathbf{W}_{\uparrow}^{I}$，并通过残差连接 $\mathbf{H}_{\mathrm{out}}^{I} = \mathrm{MLP}(\mathrm{LN}(\mathbf{Y})) + \mathbf{Y} + \mathrm{Adapter}_{\mathcal{I}}(\mathrm{LN}(\mathbf{Y}))$ 注入 MLP 输出。
- **块间适配器（Adapter-E）** 位于整个 Transformer 块的残差路径上，即 $\mathbf{X}^{(l+1)} = F_{l}\big(\mathbf{X}^{(l)}\big) + \mathrm{Adapter}.E\Big(\mathrm{LN}\big(F_{l}(\mathbf{X}^{(l)})\big)\Big)$，同样采用瓶颈形式 $\mathrm{Adapter-}E(\mathbf{Y}) = \mathcal{G}\big(\mathbf{Y}\mathbf{W}_{\downarrow}^{E}\big)\mathbf{W}_{\uparrow}^{E}$。它在相邻块之间建立直接的跨层信息通路，显式传播全局结构线索，弥补了仅使用内部适配器时长程依赖建模不足的缺陷。

两类适配器的功能互补性已由 Grad-CAM 可视化（Figure 8）验证：Adapter-E 的激活区域覆盖全局血管网络轮廓，而 Adapter-I 的响应集中于局部细节点，二者协同实现了局部精度与全局拓扑一致性的统一。

**适配器融合模块（Adapter Fusion）** 负责将多层外部适配器的输出聚合并注入掩码解码器，从而彻底消除对交互式提示的依赖。具体流程为：首先对每层外部适配器输出进行平均池化得到层描述符 $\mathbf{z}_{l} = \mathcal{A}(\mathcal{E}_{l})$，随后通过一个 FFN 与 Softmax 学习自适应权重 $\alpha = \mathrm{Softmax}\left(\mathrm{FFN}\left(\mathrm{Concat}({\bf z}_{1}, \dots, {\bf z}_{L})\right)\right)$，再以加权和方式融合多层特征 $\mathcal{F}_{\mathrm{fusion}} = \mathrm{UP}\left(\mathbf{MLP}\left(\sum_{l=1}^{L} \alpha_{l} \cdot \mathbf{\mathcal{E}}_{l}\right)\right)$，最后以残差形式注入解码器 $\mathbf{F}_{\mathrm{decoder}}^{\mathrm{out}} = \mathbf{F}_{\mathrm{decoder}}^{\mathrm{in}} + \mathcal{F}_{\mathrm{fusion}}$。该融合描述符实质上充当了学习得到的全局结构先验，替代了原始 SAM 所需的点、框或掩码提示。

**无提示掩码解码器（PFAF-D）** 采用双阶段细化策略解决单次解码中局部边界与全局拓扑难以兼顾的问题：
- **Stage-1** 生成粗掩码并评估各头部置信度：$\mathbf{M}^{(1)} = \mathbf{MLP}_{1}(\mathbf{U}), \quad \mathbf{w} = \mathrm{Softmax}\left(\mathcal{M}(\mathbf{M}^{(1)})\right)$；
- **Stage-2** 依据置信度排序重新组织头部描述符，再进行精细化掩码预测 $\mathbf{M}^{(2)} = \mathbf{MLP}_{2}(\mathbf{U}, \mathbf{s})$，最终由 MLP IoU 预测头选择最优掩码。

整个框架以加权组合损失 $\mathcal{L}_{SACM} = \mathcal{L}_{BCE} + \lambda \cdot \mathcal{L}_{Dice}$ 进行端到端训练，在边界精度与区域重叠之间取得平衡。

**输入输出流总结**：输入为单张 RGB 或灰度图像，流经冻结的 ViT 编码器与双级适配器增强后，多层外部适配器特征经 Adapter Fusion 聚合成全局结构描述符，注入无提示解码器，经双阶段细化后直接输出二值分割掩码，全程无需任何人工提示。

## 核心模块与公式推导

### 双级适配器（DLAda）

SACM 在冻结的 SAM 图像编码器（ViT）上引入双级适配器架构，由块内适配器（Adapter-ℐ）和块间适配器（Adapter-ℰ）构成，二者协同解决曲线结构分割中的局部细节与全局拓扑连续性问题。

#### 块内适配器（Adapter-ℐ）

Adapter-ℐ 嵌入每个 Transformer 块的 MLP 子层内部，对每个 token 独立进行通道级特征细化。其核心是一个带 GELU 激活的瓶颈模块：

$$
\mathrm{Adapter}_{\mathcal{I}}(\mathbf{X}) = \mathcal{G}(\mathbf{X} \mathbf{W}_{\downarrow}^{I}) \mathbf{W}_{\uparrow}^{I}
$$

其中 $\mathbf{W}_{\downarrow}^{I} \in \mathbb{R}^{D \times rD}$ 为下投影矩阵，$\mathbf{W}_{\uparrow}^{I} \in \mathbb{R}^{rD \times D}$ 为上投影矩阵，$r$ 为瓶颈比例（最优值 $r=0.1$，见 Figure 9(a)），$\mathcal{G}$ 为 GELU 激活函数。该设计使适配器的 Jacobian 矩阵在 token 维度上保持块对角结构，将更新集中于通道维度的局部细化。

Adapter-ℐ 的输出通过残差连接融入 MLP 路径：

$$
\mathbf{H}_{\mathrm{out}}^{I} = \mathrm{MLP}(\mathrm{LN}(\mathbf{Y})) + \mathbf{Y} + \mathrm{Adapter}_{\mathcal{I}}(\mathrm{LN}(\mathbf{Y}))
$$

其中 $\mathbf{Y}$ 为注意力子层输出，$\mathrm{LN}$ 为 Layer Normalization。

#### 块间适配器（Adapter-ℰ）

Adapter-ℰ 位于整个 Transformer 块的残差连接处，在块间建立直接的跨层信息通路，显式捕捉全局结构线索：

$$
\mathbf{X}^{(l+1)} = F_{l}\big(\mathbf{X}^{(l)}\big) + \mathrm{Adapter}.E\Big(\mathrm{LN}\big(F_{l}(\mathbf{X}^{(l)})\big)\Big)
$$

其中 $F_{l}$ 表示第 $l$ 个 Transformer 块的完整前向函数，$\mathbf{X}^{(l)}$ 为该块的输入特征。Adapter-ℰ 同样采用瓶颈结构：

$$
\mathrm{Adapter-}E(\mathbf{Y}) = \mathcal{G}\big(\mathbf{Y}\mathbf{W}_{\downarrow}^{E}\big)\mathbf{W}_{\uparrow}^{E}
$$

Grad-CAM 可视化（Figure 8）提供了两种适配器功能互补的直接证据：Adapter-ℰ 捕捉全局血管网络结构，而 Adapter-ℐ 聚焦于局部细节区域。消融实验（Table 5）进一步证实，同时启用两种适配器在 WIRE 数据集上取得 Dice 54.60 的协同增益，优于任何单一适配器配置。

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/016_Figure_8.jpg]]
*Figure 8: Grad-CAM visualizations of the original SAM, SAM with only Adapter-I, and SAM with only Adapter-E*

### 适配器融合与无提示解码

#### 多层特征聚合

所有 Transformer 块的外部适配器输出 $\mathcal{E}_l$（$l=1,\ldots,L$）首先通过平均池化压缩为层描述符：

$$
\mathbf{z}_{l} = \mathcal{A}(\mathcal{E}_{l}) \quad (l = 1, \ldots, L)
$$

随后通过 FFN 和 Softmax 学习各层的自适应融合权重：

$$
\alpha = \mathrm{Softmax}\left(\mathrm{FFN}\left(\mathrm{Concat}({\bf z}_{1}, \dots, {\bf z}_{L})\right)\right)
$$

加权融合后的特征经 MLP 和上采样（UP）得到全局结构描述符：

$$
\mathcal{F}_{\mathrm{fusion}} = \mathrm{UP}\left(\mathbf{MLP}\left(\sum_{l=1}^{L} \alpha_{l} \cdot \mathbf{\mathcal{E}}_{l}\right)\right)
$$

该融合特征作为全局结构先验，通过残差连接注入掩码解码器，完全替代原始 SAM 所需的交互式提示（点/框/掩码）：

$$
\mathbf{F}_{\mathrm{decoder}}^{\mathrm{out}} = \mathbf{F}_{\mathrm{decoder}}^{\mathrm{in}} + \mathcal{F}_{\mathrm{fusion}}
$$

#### 双阶段掩码细化（PFAF-D）

解码器采用两阶段设计以分离局部边界精度与全局拓扑一致性。**Stage-1** 生成 $K$ 个粗掩码并通过最大池化 $\mathcal{M}$ 和 Softmax 计算置信度排序：

$$
\mathbf{M}^{(1)} = \mathbf{MLP}_{1}(\mathbf{U}), \quad \mathbf{w} = \mathrm{Softmax}\left(\mathcal{M}(\mathbf{M}^{(1)})\right)
$$

其中 $\mathbf{U}$ 为解码器上采样特征，$\mathbf{w}$ 为各预测头部的置信度权重。**Stage-2** 基于排序后的描述符 $\mathbf{s}$ 生成精细化掩码：

$$
\mathbf{M}^{(2)} = \mathbf{MLP}_{2}(\mathbf{U}, \mathbf{s})
$$

最终通过 MLP IoU 预测选择最优掩码。消融实验（Table 5）表明，双阶段细化对 WIRE 数据集的精度提升至关重要。

### 训练损失

SACM 采用二元交叉熵损失与 Dice 损失的加权组合：

$$
\mathcal{L}_{SACM} = \mathcal{L}_{BCE} + \lambda \cdot \mathcal{L}_{Dice}
$$

其中 $\lambda$ 为平衡权重，最优值 $\lambda=0.4$（见 Figure 9(b)）。该损失同时监督粗掩码和细化掩码，确保两阶段输出的一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/002_Figure_2.jpg]]
*Figure 2: Structure of different SAM-based adapter mechanisms: (a) ViT Block in SAM without adaptation, (b) Medical Image Adapter [4] with internal-only adaptation, and (c) Our dual-level adapter architecture with both block internal and external adapter*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/005_Table_1.jpg]]
*Table 1: Details of the datasets for experiments*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/004_Figure_4.jpg]]
*Figure 4: The orange regions indicate the SAM (ViT-L) output mask, while the green regions represent the input prompts. The visual evidence suggests that the segmentation performance across all three prompt modalities (points, box, and mask) is suboptimal for curvilinear structure segmentation*

## 实验与分析

### 实验设置与评估协议

SACM的训练仅使用**18张标注图像**，覆盖6个不同领域的数据集（DRIVE、CHASEDB1、DCA1、CrackTree、CREMI、CORN），测试集则分为三类：已见域数据集（Base-Seen）、未见过域数据集（Unseen）以及全新类别数据集（Novel Class），全面评估跨域泛化能力。具体数据集划分与统计信息见**Table 1**。

评估指标采用分割任务中标准的**Dice系数、IoU、clDice（中心线Dice）和HD95（Hausdorff距离95分位数）**，所有指标均以固定二值化阈值0.5计算。对比方法分为两组：无预训练方法（U-Net、CS2-Net、BCU-Net等）和有预训练方法（SAM、SAM-Med2D、CWSAM、HQ-SAM、SAM-OCTA、SegDINO、nnWNet等），确保公平性。

### 已见域数据集上的主结果

**Table 2**展示了在4个已见域数据集上的定量对比。SACM在所有数据集上均取得了最优或次优性能：

- 在**DRIVE**视网膜血管数据集上，SACM以Dice 78.89%、IoU 65.24%取得最佳，显著超越基于适配器的SAM-Med2D和CWSAM，验证了双级适配器对医学曲线结构的细粒度捕捉能力。
- 在**CHASEDB1**上，Dice达到79.27%，同样为所有方法中最优。
- 在更具挑战性的**DCA1**和**CORN**数据集上，SACM分别取得Dice 75.67%和55.38%，尤其在CORN（玉米根冠）这种拓扑结构高度复杂的场景中，相比SAM-Med2D等仅使用内部适配器的方法提升明显。

值得注意的是，SACM作为无提示（prompt-free）方法，无需任何用户交互即可直接输出分割掩码，而原始SAM依赖点/框/掩码提示，且在曲线结构上表现欠佳（见**Figure 4**中SAM三种提示模式均产生次优分割的定性证据）。

### 跨域泛化：未见过域与全新类别

**Table 3**和**Table 4**分别展示了在未见过域数据集和全新类别数据集上的跨域泛化性能。SACM在仅用18张多域图像训练的前提下，在12个多样化数据集上展现出鲁棒的泛化能力：

- 在**FIVES、DSCA、XCAD、CRACK**等未见过域数据集上，SACM持续领先，证明双级适配器学习到的全局结构先验可有效迁移至新域。
- 在全新类别数据集（**ROAD、LEAF、TYRE、WIRE**）上，SACM同样表现优异，尤其在WIRE（线网）数据集上取得Dice 54.60%，在ROAD（遥感道路）上取得40.43%，表明模型对未见过的曲线结构类别也具有较强的适应能力。

### 消融实验：组件贡献分析

**Table 5**在WIRE数据集上系统消融了SACM各核心组件的贡献：

- **双级适配器的协同增益**：仅使用Adapter-I（内部适配器）或仅使用Adapter-E（外部适配器）时，性能均低于完整模型。两者组合后Dice达到54.60%，验证了块内局部细化与块间全局上下文建模的互补性。这一结论与**Figure 8**的Grad-CAM可视化一致——Adapter-E捕获全局血管结构，Adapter-I聚焦局部细节。
- **双阶段细化（Dual-Stage Refinement）**：移除双阶段细化后性能显著下降，证明Stage-1的粗掩码头排序与Stage-2的精细化对平衡边界精度和拓扑一致性至关重要。
- **Adapter Fusion模块**：去除多层外部适配器特征的加权融合后，性能同样下降，说明将跨层全局线索注入解码器以替代提示的有效性。

### 超参数敏感性

**Figure 9**展示了两个关键超参数的敏感性分析：

- **适配器瓶颈比例 r**：验证分数在r=0.1时达到峰值，表明适度的瓶颈压缩（降至原维度的10%）在参数效率与表示能力之间取得最优平衡。
- **损失权重 λ**（Dice损失权重）：最优值约为λ=0.4，说明BCE损失主导但辅以适量Dice损失可提升区域一致性。

### 少样本学习能力

**Figure 7**展示了SACM在WIRE数据集上随训练样本数（shots）变化的Dice曲线。随着训练样本增加，性能持续提升，但在极低样本量下（如1-shot）仍能保持一定分割能力，体现了预训练SAM基础模型与参数高效适配器结合的优势。

### 失败模式与局限性

尽管SACM在多数场景下表现优异，分析仍揭示了以下局限：

1. **严重域偏移场景**：当测试域与训练域在成像模态或结构形态上差异极大时，性能仍有下降空间，论文结论部分亦将此列为未来工作方向。
2. **参数效率**：模型依赖冻结的大型SAM编码器（ViT），整体参数量较大，可能不适合边缘设备部署。未来可探索更高效的适配器设计或知识蒸馏方法。
3. **持续学习**：当前方法未探索在线适应新域而不遗忘旧知识的能力，限制了其在动态场景中的应用。
4. **任务扩展性**：无提示设计在其他稠密预测任务（如边缘检测、道路提取）中的有效性尚待验证。

### 关键图表结论总结

| 图表 | 核心结论 |
|------|---------|
| **Table 2** | SACM在4个已见域数据集上取得最优Dice/IoU，验证双级适配器对曲线结构的细粒度分割能力 |
| **Table 3 & Table 4** | 在未见过域和全新类别共8个数据集上持续领先，证明强跨域泛化能力 |
| **Table 5** | Adapter-I与Adapter-E组合产生协同增益，双阶段细化和Adapter Fusion均为关键组件 |
| **Figure 7** | 少样本场景下性能随样本数增长，验证参数高效微调的有效性 |
| **Figure 8** | Grad-CAM可视化证明Adapter-E捕获全局结构、Adapter-I聚焦局部细节的功能互补性 |
| **Figure 9** | 最优超参数r=0.1、λ=0.4，为实际部署提供参考 |

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/007_Table_2.jpg]]
*Table 2: Comparison of Dice(%), IoU(%), clDice(%) and HD95 (px) on 4 base datasets. Best results are in bold, second best are underlined. The upper part of the table represents models without pre-trained weights, while the lower part represents models with pre-trained weights*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/012_Table_5.jpg]]
*Table 5: Ablation study of different components on WIRE dataset. ✓ indicates the component is enabled*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/008_Table_3.jpg]]
*Table 3: Cross-dataset Performance on Four Unseen Datasets*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/009_Table_4.jpg]]
*Table 4: Cross-dataset Performance on Four Unseen Datasets with Novel Classes*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/015_Figure_9.jpg]]
*Figure 9: Validation score with different bottleneck ratio r and loss weight λ*

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/014_Figure_7.jpg]]
*Figure 7: Dice of SACM versus the number of training shots per dataset on the WIRE dataset*

### 补充图表

![[assets/figures/papers/paper_list_l2061_https_openaccess_thecvf_com_content_CVPR2026_html_Zhu_Dual_level_Adapter/figures/006_Figure_5.jpg]]
*Figure 5: Dual-stage mask refinement: Stage-1 generates coarse descriptors and ranks heads by confidence scores; Stage-2 refines masks with reordered descriptors, balancing boundary precision and topological consistency*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

SACM 的核心定位是**面向曲线结构分割的 SAM 参数高效微调框架**，其方法谱系可从三个维度进行定位。

**相对于 SAM 原版 (Kirillov et al., ICCV 2023) 的改进。** SAM 作为通用分割基础模型，依赖点/框/掩码等交互式提示，且其 ViT 编码器为通用视觉任务预训练，缺乏对曲线结构拓扑连续性的感知能力。Figure 4 的可视化证据表明，SAM 在三种提示模态下对曲线结构的分割均不理想。SACM 通过两项关键改造突破了这一局限：(1) **完全无提示设计**——以 Adapter Fusion 模块聚合多层外部适配器输出作为全局结构先验，替代交互式提示；(2) **双级适配器微调**——在冻结编码器内部注入领域特定的结构感知能力。

**相对于现有适配器方法的改进。** 现有基于适配器的 SAM 微调方法，如 **SAM-Med2D** (Ma et al., Nature Communications 2024) 和 **CWSAM** (Pu et al., IEEE JSTARS 2025)，仅在 Transformer 块内部的 MLP 路径中插入适配器（即块内适配器）。这种设计仅能进行逐 token 的通道级局部特征细化，缺乏跨层的全局上下文建模能力。SACM 的关键创新在于引入**块间适配器 (Adapter-E)**，在 Transformer 块的残差连接处建立跨层信息通路，显式捕捉长程空间依赖。Figure 8 的 Grad-CAM 可视化证实了两种适配器的功能互补：Adapter-E 捕获全局血管结构，Adapter-I 聚焦局部细节。

**相对于其他 SAM 变体的改进。** **HQ-SAM** (Ke et al., NeurIPS 2023) 通过提示和输出细化提升分割质量，但仍需交互式提示；**SAM-OCTA** (Wang et al., ICASSP 2024) 针对 OCTA 血管分割微调 SAM，但依赖结构感知提示工程。SACM 的无提示设计使其在部署效率和跨域泛化方面具有本质优势。

**相对于专用分割网络的改进。** 与 **CS2-Net** (Mou et al., Medical Image Analysis 2021)、**BCU-Net** (Zhang et al., Computers in Biology and Medicine 2023) 等专用曲线结构分割网络相比，SACM 的核心优势在于利用 SAM 的大规模预训练知识，仅需 18 张标注图像即可实现跨域泛化，而专用网络通常需要大规模域内标注数据。

**相对于其他基础模型方法的改进。** **SegDINO** (Yang et al., arXiv 2025) 基于 DINOv3，**nnWNet** (Zhou et al., CVPR 2025) 基于 Transformer，两者均为通用分割模型。SACM 的差异化优势在于其双级适配器架构专门针对曲线结构的拓扑连续性需求设计，在 12 个多样化数据集上展现了更强的跨域泛化能力。

### 2. 适用边界

**适用场景。** SACM 适用于需要提取细长、连续、具有拓扑约束的曲线结构的任务，包括但不限于：医学图像中的血管和神经纤维分割、遥感图像中的道路和河流提取、工业检测中的裂纹和线缆识别、植物学中的叶脉和根系分析。实验覆盖了视网膜血管 (DRIVE, CHASEDB1)、冠状动脉 (DCA1)、裂缝 (CrackTree, CRACK)、线缆 (WIRE)、道路 (ROAD)、轮胎纹理 (TYRE) 等 12 个数据集，验证了跨域的广泛适用性。

**训练数据需求。** SACM 的少样本特性使其在标注数据稀缺的场景中具有显著优势。Figure 7 的少样本性能曲线表明，在 WIRE 数据集上仅需少量训练样本即可达到较高性能，这得益于冻结 SAM 编码器保留的通用视觉知识。

**部署约束。** SACM 依赖冻结的大型 ViT 编码器（SAM 的 ViT-L 变体），参数量较大，可能不适合边缘设备或实时性要求极高的场景。这是参数高效微调方法的共性约束——虽然可训练参数大幅减少，但推理时仍需完整的前向传播。

### 3. 局限与开放问题

**域偏移鲁棒性。** 论文明确指出现有方法在严重域偏移场景下的鲁棒性仍有待提升。当目标域与源域在成像模态、分辨率或结构形态上差异过大时，冻结编码器的通用特征可能不足以支撑精确分割。Table 4 中 ROAD 数据集上的 Dice 仅 40.43，远低于其他数据集，印证了这一局限。

**参数效率的进一步提升空间。** 尽管双级适配器显著减少了可训练参数，但论文指出未来可探索更高效的适配器设计或知识蒸馏方法，以进一步降低微调开销。

**持续学习能力缺失。** 当前 SACM 采用一次性微调范式，无法在线适应新域而不遗忘旧知识。在需要持续扩展适用域的实际部署场景中，这一局限尤为突出。

**架构依赖性。** Adapter-E 的跨层信息传播机制专为 ViT 架构设计，其能否直接迁移至 Swin Transformer 等其他基础模型架构尚待验证。

**无提示设计的泛化性。** 无提示设计在曲线结构分割中取得成功，但其在其他稠密预测任务（如边缘检测、显著性检测）中的有效性仍需进一步探索。

**三维和时序扩展。** 当前 SACM 仅处理二维静态图像，能否扩展到视频流中的曲线结构追踪或 3D 体积数据（如 CT 血管造影）的分割，是重要的开放问题。

**评估指标的完备性。** 当前评估以 Dice、IoU、clDice 和 HD95 为主，但对于曲线结构分割，拓扑一致性（如连通分量数、分支点准确性）的评估可能同样重要，未来工作可引入更全面的拓扑评估指标。

## 原文 PDF

![[paperPDFs/CVPR_2026/Dual_level_Adapter_Boosting_Prompt_free_Curvilinear_Structure_Segmentation.pdf]]
