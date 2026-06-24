---
title: "FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FSOD_VFM_Few_Shot_Object_Detection_with_Vision_Foundation_Models_and_Graph_Diffusion.pdf
openreview_forum_id: jHlAq2rYUw
aliases:
- FV
- FSOD-VFM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/classification_and_understanding
core_operator: "通过构建基于掩码重叠关系的有向图，并对提议置信度进行扩散传播（带重启），重新分配分数，使得完整物体的提议获得高置信度，碎片化提议被大幅抑制。"
primary_logic: "利用 SAM2 产生的精确物体掩码和 DINOv2 的强表征能力，借助基于掩码空间的图扩散机制实现置信度重加权，无需任何额外训练即可大幅提升小样本目标检测的精度与跨域鲁棒性。"
claims:
- "FSOD-VFM 在 CD-FSOD 跨域基准的 10-shot 设置下达到 31.6 AP，远远超过此前最佳训练免费方法的 21.4 AP。"
- "在 Pascal-5i 三个 novel split 的平均 nAP50 上，FSOD-VFM 达到 77.5，比同样不训练新类的 No-Time-To-Train 高出 6.3 个百分点。"
- "图扩散后处理能将 Pascal-5i 1-shot 性能从无后处理的 7.4 提升至 77.5，远超 NMS、WBF、Soft Merging 等方法。"
- "移除 SAM2 后，特征直接从边界框平均池化得到，Pascal-5i 1-shot 性能从 77.5 骤降至 25.5，证明掩码引导的特征提取至关重要。"
---

# FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion

> [!tip] 核心洞察
> 利用 SAM2 产生的精确物体掩码和 DINOv2 的强表征能力，借助基于掩码空间的图扩散机制实现置信度重加权，无需任何额外训练即可大幅提升小样本目标检测的精度与跨域鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FSOD-VFM：基于视觉基础模型与图扩散的小样本目标检测 |
| 英文题名 | FSOD-VFM: Few-Shot Object Detection with Vision Foundation Models and Graph Diffusion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jHlAq2rYUw); [Project](https://intellindust-ai-lab.github.io/projects/FSOD-VFM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/classification_and_understanding |
| Method | FSOD-VFM |
| Dataset | Pascal-5i (novel splits), COCO-20i, CD-FSOD |

> [!tip] 效果简介
> - Pascal-5i (novel splits) 上，nAP50 (Average over all splits and shots) 为 77.5，对比 71.2 (No-Time-To-Train)，变化 +6.3。
> - COCO-20i 上，nAP (10-shot novel classes) 为 44.0，对比 36.6 (No-Time-To-Train)，变化 +7.4。
> - CD-FSOD 上，nAP (Average over 1/5/10-shot for all 6 domains) 为 31.6 (10-shot)，对比 21.4 (No-Time-To-Train)，变化 +10.2。

## 概述

小样本目标检测（FSOD）的核心挑战在于仅凭极少标注样本（每类 1–10 张）识别全新类别的物体。现有方法大多依赖在新类上进行微调，计算成本高且容易过拟合；而已有的训练免费方法虽然避免了微调，却受限于视觉基础模型（VFM）生成的边界框提议中普遍存在的**过度碎片化问题**——多数提议仅覆盖物体的局部显著区域，导致大量小尺寸假阳性框，难以获得完整的物体检测。

针对上述瓶颈，本文提出 **FSOD-VFM**，一种完全无需在新类别上训练的小样本目标检测框架。其核心思想是：利用 SAM2 产生的精确物体掩码和 DINOv2 的强表征能力，通过一种基于掩码空间有向图的扩散机制进行置信度重加权，从而在无需任何额外训练的前提下，大幅抑制碎片化提议并突出完整物体的检测分数。

具体而言，FSOD-VFM 首先通过通用提议网络（UPN）生成类别无关的粗糙边界框，再由 SAM2 基于这些框生成精确的二值掩码，随后在掩码区域内对 DINOv2 特征进行平均池化以获得物体的语义表征。查询提议通过余弦相似度与各类别支持原型匹配后，进入核心的**图扩散重加权**阶段：基于掩码重叠关系和 UPN 分数构建有向图，利用带重启的 PageRank 式迭代传播重新分配置信度，使完整物体的提议获得高分，碎片化提议被大幅抑制。

实验结果表明，FSOD-VFM 在多个基准上显著超越了此前的训练免费方法。在跨域基准 CD-FSOD 的 10-shot 设置下，FSOD-VFM 达到 **31.6 AP**，远超此前最佳训练免费方法的 **21.4 AP**；在 Pascal-5i 三个 novel split 的平均 nAP50 上达到 **77.5**，比同样不训练新类的 No-Time-To-Train 高出 **6.3 个百分点**；在 COCO-20i 的 10-shot 设置下达到 **44.0 nAP**，领先基线 **7.4 个百分点**。消融实验进一步证实，图扩散后处理将 Pascal-5i 1-shot 性能从无后处理的 7.4 提升至 77.5，远超 NMS、WBF、Soft Merging 等传统方法；移除 SAM2 掩码引导的特征池化后，性能从 77.5 骤降至 25.5，验证了精确掩码对特征聚合的关键作用。

该方法的主要局限在于推理速度（约 2.4 秒/图像，A40 GPU），尚不适合实时应用；此外在部分极端跨域子集上绝对性能仍然较低，SAM2 掩码的失败可能导致严重漏检。

## 背景与动机

小样本目标检测（Few-Shot Object Detection, FSOD）旨在仅利用少量标注样本（通常每类 1–10 张）来检测新类别物体，这对于标注成本高昂或稀有类别频现的实际场景具有重要意义。传统 FSOD 方法通常依赖在大规模基类数据上预训练，再在新类上进行微调。然而，这类方法面临两个核心困境：其一，微调过程容易导致基类灾难性遗忘；其二，当新类与基类的分布差异较大时，跨域泛化能力急剧下降。

近年来，视觉基础模型（Vision Foundation Models, VFMs）的兴起为 FSOD 提供了新的可能性。以 SAM2、DINOv2 为代表的预训练模型具备强大的通用视觉理解能力，使得“训练免费”（training-free）的 FSOD 范式成为现实——即无需在新类上进行任何参数更新，仅通过特征匹配和提议生成即可完成检测。然而，现有训练免费方法面临一个关键瓶颈：**通用提议网络（如 UPN）生成的边界框存在严重的过度碎片化问题**。多数提议仅覆盖物体的局部显著区域（如鸟的头部、车轮的局部），而非完整物体，导致大量小尺寸假阳性提议，难以获得完整的物体检测。

以 No-Time-To-Train 为代表的现有训练免费方法，虽然利用了视觉基础模型进行特征提取和相似度匹配，但其后处理策略（如 Soft Merging）仅对提议分数进行简单的加权合并，缺乏对提议间结构关系的建模，无法有效抑制碎片化提议。这导致在跨域场景下，其性能与训练方法之间存在巨大鸿沟：在 CD-FSOD 跨域基准的 10-shot 设置下，此前最佳训练免费方法仅达到 21.4 AP，远低于训练方法的水平。

本文的核心动机在于：**能否利用 SAM2 产生的精确物体掩码和 DINOv2 的强表征能力，通过一种无需训练的置信度重加权机制，从根本上解决碎片化提议问题？** 直觉上，SAM2 能够为每个 UPN 提议生成高质量的二值掩码，这些掩码之间的重叠关系蕴含了“部分-整体”的结构信息：完整物体的掩码往往被多个碎片化掩码所覆盖，而碎片化掩码则很少能覆盖完整物体。若能利用这一结构信息对提议置信度进行重新分配，使得完整物体的提议获得高置信度、碎片化提议被大幅抑制，则可望在保持训练免费优势的同时，大幅提升检测精度与跨域鲁棒性。

## 核心创新

FSOD-VFM 的核心创新在于通过**图扩散置信度重加权**解决了视觉基础模型在小样本目标检测中的根本性瓶颈，同时以**掩码引导的特征聚合**替代了传统的边界框池化，实现了训练免费框架下的精度跃升。

### 瓶颈：UPN 提议的过度碎片化

直接使用通用提议网络（UPN）生成的边界框存在严重的结构性问题——多数提议仅覆盖物体的局部显著区域，而非完整物体。这导致大量小尺寸假阳性提议，使得基于余弦相似度的类别匹配难以获得可靠的检测结果。在 Pascal-5i 1-shot 设置下，不经任何后处理的原始分数仅能达到 7.4 nAP50（Table 4），充分暴露了这一瓶颈。

### 机制：基于掩码重叠的图扩散重加权

针对碎片化问题，FSOD-VFM 将每个提议建模为有向图中的节点，并利用 SAM2 生成的精确掩码定义边权重：

$$
\mathcal{E}^{i,j} = \begin{cases} 0, & \text{if } s_{\mathrm{upn}}^{i} > s_{\mathrm{upn}}^{j}, \\ \frac{\mathrm{Area}(M^{i} \cap M^{j})}{\mathrm{Area}(M^{i})}, & \text{otherwise}. \end{cases}
$$

该定义确保能量从被覆盖程度高的节点流向覆盖它的节点，使得完整物体的提议获得来自碎片化提议的分数汇聚。扩散过程采用带重启的 PageRank 式迭代：

$$
\boldsymbol{\pi}^{t+1} = \alpha \mathbf{P} \otimes \boldsymbol{\pi}^{t} + (1 - \alpha) \mathbf{w}
$$

最终分数由扩散惩罚项与余弦相似度相乘得到：

$$
\hat{f}^{j} = (1 - \hat{\pi}_{j})^{\lambda} \max_{c} \cos(F_{q}^{j}, \hat{p}_{c})
$$

这一机制的效果在 Figure 1 中有直观展示：扩散 30 步后，高质量框（IoU > 0.75）的分数分布显著右移，低质量框（IoU < 0.1）被大幅抑制。定量上，图扩散将 Pascal-5i 1-shot 性能从 7.4 提升至 77.5 nAP50，远超 NMS（23.4）、Soft NMS（28.3）、WBF（66.0）和 Soft Merging（66.0）等传统后处理方式（Table 4）。

### 关键使能：SAM2 掩码引导的特征聚合

传统方法在 RoI 区域直接进行边界框平均池化，混入大量背景噪声。FSOD-VFM 利用 SAM2 生成的二值掩码 $M_{\mathrm{down}}^{i}$ 对 DINOv2 特征图进行加权池化：

$$
F_{s}^{i} = \frac{1}{N_{\mathrm{mask}}} \sum_{u=y_{1}^{\prime}}^{y_{2}^{\prime}} \sum_{v=x_{1}^{\prime}}^{x_{2}^{\prime}} F_{\mathrm{img}}^{i}[:, u, v] M_{\mathrm{down}}^{i}[u, v]
$$

组件消融实验（Table 11）表明，移除 SAM2 掩码引导后，Pascal-5i 1-shot 性能从 77.5 骤降至 25.5，COCO-20i 10-shot 从 59.4 降至 15.5，证明精确的前景/背景分离是特征聚合质量的决定性因素。

### 与最相关基线的对比

与同样采用视觉基础模型且无需训练的 **No-Time-To-Train**（Espinosa et al., 2025）相比，FSOD-VFM 的核心差异在于后处理机制：No-Time-To-Train 使用 Soft Merging 进行分数合并，而 FSOD-VFM 采用图扩散重加权。这一 changed slot 带来了显著的性能增益——在 Pascal-5i 上平均 nAP50 从 71.2 提升至 77.5（+6.3），在 COCO-20i 10-shot 上 nAP 从 36.6 提升至 44.0（+7.4），在跨域 CD-FSOD 基准上 10-shot nAP 从 21.4 提升至 31.6（+10.2）。

## 整体框架

![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/007_Figure_2.jpg]]
*Figure 2: Overview of FSOD-VFM. Our method integrates UPN, SAM2, and DINOv2 to generate bounding box proposals and perform query matching. We build a graph and perform graph diffusion to mitigate over-fragmentation. The over-fragmented box regions appear more transparent after graph diffusion, indicating that their confidence has decayed*

FSOD-VFM 的整体流程围绕一个核心瓶颈展开：**UPN 生成的类别无关边界框提议存在严重的过度碎片化问题**——多数提议仅覆盖物体的局部显著区域（如鸟的喙部、飞机的机头），而非完整物体，导致大量小尺寸假阳性候选。为此，方法构建了一条“粗提议 → 精掩码 → 强特征 → 图扩散重加权”的处理链，在不进行任何新类别训练的前提下，将碎片化提议的置信度重新分配给完整物体的提议。

**Pipeline 模块关系与数据流**（Figure 2 给出了完整概览）：

1. **UPN（Universal Proposal Network）**：以“coarse”为文本提示，生成类别无关的粗糙边界框提议，经置信度过滤（阈值 0.01）后每图保留最多 500 个候选框。这些提议为后续处理提供候选区域，但其本身存在严重的碎片化缺陷。

2. **SAM2**：以 UPN 提议的边界框作为输入提示，为每个提议生成精确的二值物体掩码。该掩码将前景与背景分离，为后续特征池化提供像素级指导。Figure 4 的跨域分割可视化表明，SAM2 在昆虫、卡通、深海等多样化场景下均能输出可靠的掩码。

3. **DINOv2**：对输入图像提取稠密特征图。对于支持图像，在 SAM2 掩码区域内进行掩码引导的 RoI 平均池化，获得物体的语义特征表示，随后对同类样本特征进行均值聚合与 L2 归一化，构建类别级原型 $\hat{p}_c$。对于查询图像，同样使用掩码引导池化提取每个提议的特征 $F_q^j$，通过余弦相似度 $\hat{c}^{j} = \arg \max_{c} \cos(F_{q}^{j}, \hat{p}_{c})$ 完成类别预测。

4. **图扩散置信度重加权**：这是方法的核心创新模块。将每个提议作为有向图的节点，基于掩码重叠关系定义边权重——当节点 $i$ 的 UPN 分数高于 $j$ 时边权重为 0，否则权重为 $i$ 的掩码被 $j$ 覆盖的程度（$\frac{\mathrm{Area}(M^{i} \cap M^{j})}{\mathrm{Area}(M^{i})}$）。随后采用 PageRank 式的带重启扩散迭代 $\boldsymbol{\pi}^{t+1} = \alpha \mathbf{P} \otimes \boldsymbol{\pi}^{t} + (1 - \alpha) \mathbf{w}$，将置信度从碎片化提议传播至覆盖它们的完整物体提议。最终分数由扩散收敛后的惩罚项与余弦相似度相乘得到：$\hat{f}^{j} = (1 - \hat{\pi}_{j})^{\lambda} \max_{c} \cos(F_{q}^{j}, \hat{p}_{c})$。

**因果机制**：UPN 的碎片化提议（高 UPN 分数但低 IoU）在图中被赋予低先验权重，其置信度通过扩散流向覆盖它们的完整物体提议（高掩码重叠、高 UPN 分数），从而实现“碎片抑制、完整提升”的效果。Figure 1 的定性对比清晰展示了这一过程：无图扩散时检测框密集覆盖物体局部区域，经过 30 步扩散后仅保留完整物体的高质量框。

**关键证据强度**：组件消融实验（Table 11）表明，移除 SAM2 掩码引导的特征池化后，Pascal-5i 1-shot 性能从 77.5 nAP50 骤降至 25.5，证明精确掩码对特征聚合至关重要；移除 UPN 直接使用 SAM2 生成提议时，性能降至 56.7，说明 UPN 提供的候选集有助于提升检测召回。图扩散后处理将 Pascal-5i 1-shot 性能从无后处理的 7.4 提升至 77.5，远超 NMS（23.4）、Soft NMS（28.3）、WBF（66.0）和 Soft Merging（66.0）等方法（Table 4）。

## 核心模块与公式推导

FSOD-VFM 由四个核心模块串联构成：通用提议网络（UPN）生成类别无关的候选框，SAM2 基于候选框提取精确物体掩码，DINOv2 提供通用视觉特征用于构建支持类原型并与查询提议进行余弦相似度匹配，最后通过图扩散机制对提议置信度进行重加权以抑制碎片化并突出完整物体。

### 掩码引导的 RoI 特征池化

传统 RoI 池化在边界框内均匀聚合特征，容易混入背景噪声。FSOD-VFM 利用 SAM2 生成的二值掩码，仅在物体前景区域内对 DINOv2 特征图进行平均池化。对于支持图像 $i$ 的提议，其掩码引导的 RoI 特征表示为：

$$F_{s}^{i} = \frac{1}{N_{\mathrm{mask}}} \sum_{u=y_{1}^{\prime}}^{y_{2}^{\prime}} \sum_{v=x_{1}^{\prime}}^{x_{2}^{\prime}} F_{\mathrm{img}}^{i}[:, u, v] M_{\mathrm{down}}^{i}[u, v], \quad N_{\mathrm{mask}} = \sum_{u=y_{1}^{\prime}}^{y_{2}^{\prime}} \sum_{v=x_{1}^{\prime}}^{x_{2}^{\prime}} M_{\mathrm{down}}^{i}[u, v]$$

其中 $F_{\mathrm{img}}^{i}$ 为 DINOv2 提取的密集特征图，$M_{\mathrm{down}}^{i}$ 为下采样至特征图分辨率的二值掩码，$N_{\mathrm{mask}}$ 为掩码区域内有效像素数。该操作将特征聚合严格限定在物体前景，显著提升特征纯度。

所有支持样本的掩码池化特征经 L2 归一化后按类别取均值，得到各类别的归一化原型 $\hat{p}_c$。

### 余弦相似度类别预测

对于查询图像中的每个提议 $j$，同样通过掩码引导池化获得其特征 $F_q^j$，然后计算其与各类别原型的余弦相似度，取最大相似度对应的类别作为预测结果：

$$\hat{c}^{j} = \arg \max_{c} \cos(F_{q}^{j}, \hat{p}_{c})$$

这一分类机制完全基于特征空间的相似性度量，无需在新类别上进行任何训练。

### 图扩散置信度重加权

UPN 生成的提议存在严重的过度碎片化问题——多数边界框仅覆盖物体的局部显著区域，导致大量小尺寸假阳性提议。FSOD-VFM 的核心创新在于将提议建模为有向图的节点，利用 SAM2 掩码间的重叠关系定义边权重，通过扩散传播重新分配置信度。

**有向图构建**：边 $\mathcal{E}^{i,j}$ 表征能量从节点 $i$ 向节点 $j$ 的扩散强度，其权重定义为：

$$\mathcal{E}^{i,j} = \begin{cases} 0, & \text{if } s_{\mathrm{upn}}^{i} > s_{\mathrm{upn}}^{j}, \\ \frac{\mathrm{Area}(M^{i} \cap M^{j})}{\mathrm{Area}(M^{i})}, & \text{otherwise}. \end{cases}$$

该定义蕴含两个关键设计：其一，UPN 分数更高的节点被视为更可靠的提议，不接收来自低分节点的能量（边权重为 0）；其二，边权重等于节点 $i$ 的掩码被节点 $j$ 覆盖的程度，即碎片化提议的置信度将流向覆盖它的更完整提议。

**带重启的扩散迭代**：扩散过程遵循 PageRank 式的更新规则：

$$\boldsymbol{\pi}^{t+1} = \alpha \mathbf{P} \otimes \boldsymbol{\pi}^{t} + (1 - \alpha) \mathbf{w}$$

其中 $\mathbf{P}$ 为归一化转移矩阵，$\boldsymbol{\pi}^{t}$ 为第 $t$ 步的扩散向量，$\mathbf{w}$ 为基于最大出边权重的先验权重（$\mathbf{w}^{i} = \max_{j}(\mathcal{E}^{i,j})$），$\alpha$ 为重启概率。重启机制确保扩散过程不会完全偏离初始先验。

**最终分数计算**：扩散收敛后，节点 $j$ 的惩罚项 $(1 - \hat{\pi}_j)^{\lambda}$ 与其余弦相似度相乘，得到重加权的最终检测分数：

$$\hat{f}^{j} = (1 - \hat{\pi}_{j})^{\lambda} \max_{c} \cos(F_{q}^{j}, \hat{p}_{c})$$

其中 $\lambda$ 控制惩罚强度。扩散后，完整物体提议的 $\hat{\pi}_j$ 较高（接收大量来自碎片提议的能量），惩罚项趋近于 0，分数得以保留；碎片化提议的 $\hat{\pi}_j$ 较低，惩罚项趋近于 1，分数被大幅抑制。

实验表明，扩散步数 $t$ 超过 5 后性能即趋于稳定，超参数 $\lambda=0.5$、$\alpha=0.3$ 时效果最优，且方法对参数变化不敏感，具有良好的鲁棒性。

## 实验与分析

### 核心瓶颈：UPN 提议的过度碎片化

FSOD-VFM 的性能增益根源于一个被精确定位的瓶颈：UPN 生成的类别无关边界框提议存在严重的过度碎片化问题。多数提议仅覆盖物体的局部显著区域（如头部、翅膀或纹理边缘），而非完整物体，导致大量小尺寸假阳性提议。这些碎片化提议在余弦相似度匹配阶段可能获得高分，却无法提供准确的物体定位。图 1 的定性对比直观展示了这一问题：无图扩散时，检测结果充满碎片化框；经 30 步扩散后，完整物体的提议被突出，碎片被大幅抑制。

图 1 的第二行从统计角度量化了扩散效果：高质量框（与任意真值 IoU > 0.75）和低质量框（IoU < 0.1）的分数分布在扩散过程中逐渐分离。无扩散时两类框的分数高度重叠（图 1d），1 步扩散后开始分化（图 1e），30 步后高质量框的分数明显右移，低质量框被压制至低分区域（图 1f）。

### 主实验结果

#### Pascal-5i 基准

表 1 报告了 Pascal-5i 三个 novel split 上的 nAP50 结果。FSOD-VFM-DINOv2-L 在 1-shot 设置下平均达到 77.5，比同样不训练新类的 No-Time-To-Train（71.2）高出 6.3 个百分点。FSOD-VFM-RADIOv4 进一步提升至 79.8。在 split 1 的 1-shot 场景中，FSOD-VFM 达到 83.4，远超所有训练免费基线。值得注意的是，FSOD-VFM 在 1-shot 设置下的性能已超过多数需要在新类上微调的方法在 5-shot 甚至 10-shot 下的结果。


![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/008_Table_1.jpg]]
*Table 1: Results for competing methods are taken from Zhang et al. (2023), with the best highlighted in bold. Table 1: Results on Pascal-5i (Everingham et al., 2010). We report nAP50, i.e., the average precision at IoU 0.5 on novel classes*

#### COCO-20i 基准

表 2 展示了 COCO-20i 上 novel 类的 nAP/nAP50/nAP75。FSOD-VFM-DINOv2-L 在 10-shot 设置下达到 44.0 nAP，比 No-Time-To-Train（36.6）高出 7.4 个点；30-shot 下进一步提升至 45.8。在 nAP50 指标上，FSOD-VFM 10-shot 达到 59.4，30-shot 达到 61.4，显著优于所有训练免费方法。RADIOv4 版本在 10-shot 和 30-shot 下分别达到 46.3 和 47.8 nAP，进一步扩大了优势。


![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/010_Table_2.jpg]]
*Table 2: Results on COCO-20i (Kang et al., 2019; Lin et al., 2014). We report nAP (IoU thresholds 0.5–0.95), nAP50 (IoU 0.5), and nAP75 (IoU threshold 0.75) on novel classes. ◦ indicates Distill-CD-FSOD (Xiong, 2023) results, and † denotes CD-ViTO (Fu et al., 2024) results. Best results are in bold. Table 3: Results on the CD-FSOD benchmark (Xiong, 2023). We report nAP (IoU thresholds 0.5–0.95) for all datasets, with each entry showing results for 1-shot, 5-shot, and 10-shot*

#### CD-FSOD 跨域基准

表 3 和表 9 报告了 CD-FSOD 六个跨域子集上的 nAP。FSOD-VFM 在 10-shot 设置下平均达到 31.6 AP，远超此前最佳训练免费方法的 21.4 AP（提升 10.2 个点）。在 ArTaxOr 子集上，FSOD-VFM 仅需 1-shot 即达到 51.4 AP，体现了极强的跨域泛化能力。图 3 的定性结果显示，FSOD-VFM 在昆虫、卡通、深海等多样化场景中均能实现精确检测与分类，每类仅需一个标注样本。


![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/019_Table_9.jpg]]
*Table 9: ◦ indicates Distill-CD-FSOD (Xiong, 2023) results, and † denotes CD-ViTO (Fu et al., 2024) results. Best results are in bold. Table 9: Results on the CD-FSOD benchmark (Xiong, 2023). We report nAP (IoU thresholds 0.5–0.95) for all datasets, with each entry showing results for 1-shot, 5-shot, and 10-shot*

### 图扩散后处理的消融分析

表 4 对比了多种后处理策略在 Pascal-5i（1-shot）和 COCO-20i（10-shot）上的效果。基线无后处理时，nAP50 仅为 7.4（Pascal-5i）和 9.9（COCO-20i），说明原始余弦相似度分数无法有效区分完整物体与碎片。标准 NMS 和 Soft NMS 仅带来有限提升（23.4–28.3），WBF 和 Soft Merging 改善明显但仍不足（25.5–66.0）。图扩散将 Pascal-5i 性能推至 77.5，COCO-20i 至 59.4，远超所有替代方案。值得注意的是，在图扩散基础上叠加 NMS 不会带来增益（77.2 和 59.1），表明扩散本身已充分处理了冗余框。


![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/013_Table_4.jpg]]
*Table 4: Post-processing comparison of nAP50 on Pascal-5i (1-shot) and COCO-20i (10-shot)*

表 5 分析了图扩散的三个关键超参数。惩罚强度 λ 在 0.3–0.7 范围内性能稳定，λ=0.5 时最优。重启概率 α 在 0.1–0.5 间波动较小，α=0.3 最优。扩散步数 t 超过 5 后性能趋于平稳，t=30 时达到最佳，继续增加至 50 步几乎无变化。图 5 的收敛分析显示，扩散过程在 Pascal-5i split1 的 1-shot 设置下约 70 步停止，但 AP 在 5 步后即稳定，表明方法对迭代次数不敏感，具有良好的鲁棒性。

### 组件消融：SAM2 与 UPN 的关键作用

表 11 的组件消融揭示了各模块的贡献。移除 SAM2 掩码引导的特征池化，改为直接从边界框平均池化 DINOv2 特征，Pascal-5i 1-shot 性能从 77.5 骤降至 25.5，COCO-20i 10-shot 从 59.4 降至 15.5。这一近 3–4 倍的性能衰减证明，SAM2 提供的精确前景/背景分离对特征聚合质量至关重要——边界框池化会混入大量背景噪声，严重污染物体表示。


![[assets/figures/papers/iclr26_0011_jHlAq2rYUw_FSOD-VFM_Few-Shot_Object_Detection_with_Vision_F/figures/021_Table_11.jpg]]
*Table 11: Component ablation studies. We report nAP50 (IoU 0.5) on novel classes*

移除 UPN 直接使用 SAM2 的自动掩码生成提议时，Pascal-5i 降至 56.7，COCO-20i 降至 41.5。UPN 提供的候选集虽存在碎片化问题，但保证了较高的检测召回；SAM2 自动提议可能遗漏部分物体，导致召回不足。

### 骨干网络选择

表 6 对比了不同 DINOv2/v3 变体及 REG 骨干。DINOv2-L 在 COCO-20i 上效果最优（59.4 nAP50），而 DINOv2-B 在 Pascal-5i 上略微更优（81.2 vs 77.5），整体差距不大。带寄存器（register）的变体通常略优于无寄存器版本。RADIOv4 作为更强的特征提取器，在多数子集上进一步带来小幅提升（Pascal-5i 平均 79.8，COCO-20i 10-shot 46.3 nAP），验证了方法对特征提取器选择的兼容性。

### 失败模式与局限性

尽管 FSOD-VFM 在多数场景下表现优异，仍存在明确的失败模式：

1. **SAM2 掩码失败**：在部分极端跨域子集（如 CD-FSOD 的 NEU-DET 钢材缺陷检测）上，绝对性能仍然较低（约 6% AP）。图 4 显示 SAM2 在多数场景下分割可靠，但某些纹理复杂或对比度低的工业场景中可能产生错误掩码，错误的前景分割直接污染特征聚合，导致严重漏检。

2. **多 shot 收益递减**：当支持样本从 5-shot 增加到 10-shot 时，性能增幅明显放缓。这表明简单的原型平均策略未能充分利用更多标注信息，可能需要更精细的支持集聚合机制。

3. **推理效率**：表 10 显示，单张图像推理约需 2.4 秒（A40 GPU），其中 SAM2 占 0.86 秒为主要瓶颈。该方法尚不适合实时应用，但可作为高精度离线检测方案。
## 方法谱系与知识库定位

### 与训练免费基线的对比

FSOD-VFM 属于**完全训练免费**的小样本目标检测方法，即在新类别上不进行任何微调或元学习。与其最直接可比的基线是 **No-Time-To-Train**（Espinosa et al., 2025），两者均利用视觉基础模型（UPN、SAM2、DINOv2）进行提议生成与特征匹配，但核心差异在于**置信度重加权机制**：No-Time-To-Train 采用 Soft Merging 进行分数合并，而 FSOD-VFM 引入基于掩码重叠关系的图扩散（Graph Diffusion）对提议分数进行重分配。

这一差异在性能上体现为显著且一致的提升：
- Pascal-5i 三个 novel split 平均 nAP50 从 71.2 提升至 77.5（+6.3 个百分点）；
- COCO-20i 10-shot nAP 从 36.6 提升至 44.0（+7.4 个百分点）；
- CD-FSOD 跨域基准 10-shot 从 21.4 AP 提升至 31.6 AP（+10.2 个百分点）。

另一训练免费基线 **DE-ViT**（Zhang et al., 2023）使用原型相似度进行分类，但缺乏精细的掩码引导特征聚合与图扩散后处理，在 Pascal-5i 上平均 nAP50 仅约 18.8，远低于 FSOD-VFM。

### 与训练依赖方法的定位

尽管 FSOD-VFM 完全无需在新类上训练，其在 Pascal-5i 和 COCO-20i 上的性能已**超越多数需要微调的方法**。例如，在 COCO-20i 10-shot 设置下，FSOD-VFM 的 44.0 nAP 超过了包括 Meta R-CNN、TFA、FSCE 等经典微调方法。这一现象表明，当基础模型的表征能力足够强时，**精心设计的训练免费推理管线可以替代甚至超越传统的小样本微调范式**，尤其在标注极度稀缺（1-shot、5-shot）的场景下优势更为突出。

### 适用边界与失效模式

**适用场景：**
- 标注极度稀缺（每类 1-10 张）的检测任务；
- 跨域泛化需求强烈的场景（如从自然图像迁移到医学、遥感、水下等领域）；
- 无法承担新类训练成本的资源受限环境。

**已知失效模式：**

1. **SAM2 掩码失败导致性能骤降。** 移除 SAM2 掩码引导的 RoI 池化后，Pascal-5i 1-shot 性能从 77.5 骤降至 25.5，COCO-20i 10-shot 从 59.4 降至 15.5。在 SAM2 无法产生可靠掩码的场景（如极端遮挡、极小目标、域外纹理），特征聚合质量将严重退化。

2. **极端跨域子集性能仍然较低。** 在 CD-FSOD 的 NEU-DET（钢材表面缺陷）子集上，10-shot nAP 仅约 6%，表明当目标域与基础模型预训练数据分布差异过大时，SAM2 和 DINOv2 的零样本能力仍存在瓶颈。

3. **Shot 数增加的边际收益递减。** 从 5-shot 到 10-shot 的性能增幅明显放缓，说明当前方法未能充分利用更多标注样本——原型构造采用简单平均池化，缺乏对支持样本质量的加权或筛选机制。

4. **推理效率不满足实时需求。** 单张图像推理时间约 2.4 秒（A40 GPU），瓶颈主要来自 UPN 提议生成、SAM2 掩码预测和图扩散迭代。该方法更适合离线高精度检测场景，而非实时应用。

### 局限与开放问题

**已确认局限：**
- 图扩散虽在 5 步内即趋于稳定，但整体管线仍涉及三个大型基础模型的串行调用，计算开销较高（Table 10）；
- 当 UPN 生成的候选提议本身遗漏目标时，后续 SAM2 和 DINOv2 无法补救——去除 UPN 直接使用 SAM2 生成提议时，Pascal-5i 性能降至 56.7；
- 边权重定义仅依赖掩码空间重叠，未利用语义特征相似度，可能在语义相关但空间不重叠的提议间错失信息传播机会。

**值得探索的开放方向：**
- 能否通过模型蒸馏或轻量化图扩散策略将推理时间压缩至实时可用水平？
- 引入大语言模型（LLM）提供的类别先验知识（如部件-整体关系、典型外观描述）是否能进一步增强跨域泛化？
- 图扩散的边权重定义是否可以融合语义相似度（如 DINOv2 特征的余弦距离），以替代纯掩码重叠的硬性约束？
- 该训练免费框架能否扩展到视频小样本目标检测，利用时序一致性进一步提升精度并抑制单帧误检？

## 原文 PDF

![[paperPDFs/ICLR_2026/FSOD_VFM_Few_Shot_Object_Detection_with_Vision_Foundation_Models_and_Graph_Diffusion.pdf]]
