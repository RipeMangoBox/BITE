---
title: "FreeSOLO: Learning to Segment Objects without Annotations"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/FreeSOLO_Learning_to_Segment_Objects_without_Annotations.pdf
project_link: null
code_link: https://github.com/NVlabs/FreeSOLO
aliases:
- FreeSOLO
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "利用自监督稠密特征通过查询-键注意力机制（Free Mask）生成粗糙掩码，并采用弱监督投影损失和自训练策略（Self‑Supervised SOLO）逐步提升掩码质量。"
primary_logic: "SOLO 的“自上而下与自下而上相统一”设计天然地将像素分组、目标定位和特征学习融为一体，使得全流程可在无标注条件下以自监督方式训练。"
claims:
- "FreeSOLO 在无任何标注的情况下，在 COCO 上取得 9.8% AP50 的类别无关实例分割结果，优于需要标注的 MCG 等 proposal 方法。"
- "FreeSOLO 的无监督目标检测性能比现有最好方法提升约 100% 相对 AP。"
- "FreeSOLO 的自监督预训练在 5% COCO 掩码微调时，比 DenseCL 提高了 +9.8% AP。"
- "弱监督设计中的平均投影损失 L_avg-proj 能防止模型坍缩为仅分割轮廓，移除后 AP 从 3.3 降至 2.0。"
---

# FreeSOLO: Learning to Segment Objects without Annotations

> [!tip] 核心洞察
> SOLO 的“自上而下与自下而上相统一”设计天然地将像素分组、目标定位和特征学习融为一体，使得全流程可在无标注条件下以自监督方式训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FreeSOLO：无需标注的实例分割学习 |
| 英文题名 | FreeSOLO: Learning to Segment Objects without Annotations |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2202.12181) · [GitHub](https://github.com/NVlabs/FreeSOLO) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | FreeSOLO |
| Dataset | COCO val2017 (类无关实例分割), COCO val2017 (类无关目标检测), PASCAL VOC trainval07 (多目标发现), COCO 5% 掩码微调实例分割 |

> [!tip] 效果简介
> - COCO val2017 (类无关实例分割) 上，AP50 为 9.8，对比 COB 8.8 (最佳需要标注的 baseline)，变化 +1.0 (相对改善约11%)。
> - COCO val2017 (类无关目标检测) 上，AP 为 5.5，对比 DETReg 1.0，变化 +4.5 (+450% 相对改善)。
> - PASCAL VOC trainval07 (多目标发现) 上，AP 为 10.2，对比 LOST* 6.7，变化 +3.5。

## 概要

**问题瓶颈**：现有无监督实例分割方法仍依赖边界框或点标注作为监督信号，完全脱离人工标注的像素级实例分割极具挑战。核心瓶颈在于，如何在不使用任何人工标注的前提下，生成足够质量的伪标签来驱动分割模型的训练。

**核心思路**：FreeSOLO 将 SOLO 架构“自上而下与自下而上相统一”的设计天然地转化为自监督学习范式，提出两大支柱——**Free Mask** 与 **Self‑Supervised SOLO**。Free Mask 利用自监督稠密特征，通过查询‑键注意力机制自动生成粗糙掩码，并以掩码质量评分和非极大抑制进行筛选；Self‑Supervised SOLO 则以这些粗糙掩码为伪标签，采用弱监督投影损失和自训练策略逐步提升掩码质量，同时通过语义嵌入学习增强特征表达。整个流程无需任何人工标注。

**方法定位**：FreeSOLO 在无监督实例分割的方法谱系中处于“完全无标注”的一端。其对比基线包括需要不同程度标注的传统方法 **MCG**（Arbelaez et al., CVPR 2014）和 **COB**（Maninis et al., TPAMI 2018），以及无监督目标检测方法 **DETReg**（Bar et al., arXiv 2021）和多目标发现方法 **LOST***（Simeoni et al., arXiv 2021）。FreeSOLO 的自监督预训练版本亦与稠密自监督方法 **DenseCL** 进行微调对比。

**主要结果**：
- **类别无关实例分割**：在 COCO val2017 上，FreeSOLO 以 9.8% AP50 的结果优于需要标注的最佳基线 COB（8.8% AP50，Table 1）。
- **无监督目标检测**：在 COCO val2017 上取得 5.5% AP，相对 DETReg（1.0% AP）提升约 450%（Table 3）。
- **多目标发现**：在 PASCAL VOC trainval07 上取得 10.2% AP，优于 LOST*（6.7% AP，Table 4）。
- **自监督预训练迁移**：以 5% COCO 掩码微调时，FreeSOLO 预训练模型（29.9% AP）比 DenseCL 预训练模型（20.1% AP）提高 +9.8% AP（Table 6）。

**关键消融发现**：
- 弱监督投影损失中的平均投影损失 $L_{avg-proj}$ 是防止模型坍缩为仅分割轮廓的关键：移除后 AP 从 3.3 降至 2.0，且出现轮廓坍缩现象（Table 7e, Figure 5）。
- 一次自训练即可将 AP 从 3.3 提升至 4.0，但进一步迭代不再增益（Table 7c）。

**局限与开放问题**：FreeSOLO 在目标被截断、高度拥挤或尺寸过小时可能定位失败（Figure 6），且自监督结果与全监督方法（COCO AP 约 4.0 vs 37+）之间仍存在巨大差距。如何进一步缩小这一差距、将方法扩展至无监督全景分割，以及寻找更优的预训练策略以生成更高分辨率的精细掩码，是值得探索的方向。

实例分割是计算机视觉的核心任务之一，要求模型同时完成目标定位与像素级分类。近年来，以 **SOLO** 为代表的全监督方法取得了显著进展，但其成功高度依赖大规模精确的人工标注。在现实场景中，获取像素级掩码标注成本极高，这严重制约了实例分割模型的可扩展性。

现有无监督目标分割方法试图缓解这一困境，但仍存在明显缺口。基于区域提议的传统方法如 **MCG**（Arbelaez et al., CVPR 2014）和 **COB**（Maninis et al., TPAMI 2018），虽然能够生成候选分割区域，却或多或少依赖人工标注进行训练或后处理。近年来涌现的自监督目标发现方法如 **DETReg**（Bar et al., arXiv 2021）和 **LOST***（Simeoni et al., arXiv 2021），仅能输出目标边界框，无法提供像素级实例掩码。**核心瓶颈在于：如何在不使用任何人工标注的条件下，生成足够质量的伪标签来训练像素级实例分割模型。**

FreeSOLO 正是在这一背景下被提出。其核心洞察在于：SOLO 框架“自上而下与自下而上相统一”的设计天然地将像素分组、目标定位和特征学习融为一体，使得整个流程具备了在无标注条件下以自监督方式训练的潜力。具体而言，FreeSOLO 通过两大支柱实现这一目标：**Free Mask** 利用自监督稠密特征的查询-键注意力机制自动生成粗糙掩码，**Self-Supervised SOLO** 则采用弱监督投影损失和自训练策略，将粗糙掩码逐步提升为高质量实例分割结果。这一设计使 FreeSOLO 成为首个完全不依赖任何人工标注、端到端可训练的实例分割框架。

## 核心方法与创新机理

FreeSOLO 的核心创新在于将实例分割框架 SOLO 完全迁移至**零人工标注**的自监督学习范式，其关键突破可归纳为以下三个相互耦合的 changed slots：

### 1. 伪标签来源：从人工标注到自监督特征注意力

传统 SOLO 依赖精确的 ground‑truth 掩码作为监督信号，而 FreeSOLO 通过 **Free Mask** 模块从自监督预训练模型的稠密特征中自动生成粗糙掩码。其机制为查询‑键注意力设计：将骨干网络特征 $I$ 双线性下采样为查询 $\mathbf{Q}$，原始特征作为键 $\mathbf{K}$，通过余弦相似度计算得分图：

$$\mathbf{S}_{i,j,q} = \mathrm{sim}(\mathbf{Q}_q, \mathbf{K}_{i,j})$$

经归一化、掩码质量评分（Maskness）和非极大抑制（NMS）后输出粗糙掩码 $\mathbf{M}$：

$$\mathbf{M} = \mathrm{NMS}(\mathrm{Maskness}(\mathrm{Norm}(\mathbf{Q}' \oplus \mathbf{K}')))$$

这一设计使 FreeSOLO 成为首个**完全不使用任何人工标注**即可生成实例分割伪标签的方法（Section 3.2）。消融实验表明，DenseCL 作为 Free Mask 的预训练方法效果最优（Table 7a），金字塔查询将 AR 从单尺度的 8.7 提升至 11.5（Table 7b）。

### 2. 监督信号类型：从全掩码监督到弱监督投影损失

由于 Free Mask 生成的掩码粗糙且含噪，直接使用 Dice loss 进行全掩码监督会导致模型坍缩。FreeSOLO 的关键应对是将监督信号从精确掩码替换为**弱监督投影损失**组合：

$$\mathcal{L}_{mask} = \alpha \mathcal{L}_{avg-proj} + \mathcal{L}_{max.proj} + \mathcal{L}_{pairwise}$$

其中 $\mathcal{L}_{max.proj}$ 沿 x/y 轴取最大投影计算 Dice 损失，$\mathcal{L}_{avg-proj}$ 沿 x/y 轴取平均投影计算 Dice 损失。**平均投影损失 $\mathcal{L}_{avg-proj}$ 是防止模型坍缩的核心设计**：移除该损失项后，AP 从 3.3 降至 2.0，且模型在训练后期仅分割目标轮廓（Table 7e, Figure 5）。弱监督设计比全掩码监督将 AP 从 1.7 提升至 3.3（Table 7d），验证了“粗糙伪标签 + 弱约束”优于“粗糙伪标签 + 强约束”的反直觉结论。

### 3. 训练策略：从直接标注训练到自训练自循环

FreeSOLO 引入**一次自训练**以进一步提升掩码质量：先用 Free Mask 伪标签训练初始模型，再用该模型重新生成掩码并二次训练。Table 7c 显示自训练将 AP 从 3.3 提升至 4.0，但进一步迭代不再增益——这表明模型在单轮自训练后即饱和，揭示了自监督实例分割中伪标签质量与模型容量之间的瓶颈。此外，语义嵌入学习通过负余弦相似度损失拉近预测嵌入与 Free Mask 提取的语义嵌入，将 10% 掩码微调的 AP 从 24.9 提升至 25.6（Table 7f），为下游任务提供了额外的迁移能力。

### 创新总结

上述三个 changed slots 形成了一条完整的无监督实例分割链路：**自监督特征 → 注意力伪标签 → 弱监督训练 → 自训练精化**。SOLO 框架“自上而下与自下而上相统一”的设计天然地将像素分组、目标定位和特征学习融为一体，使得该链路可在无任何标注的条件下端到端运行。这一创新使 FreeSOLO 在 COCO 上以 9.8% AP50 超越需要标注的 MCG（8.8% AP50），并在无监督目标检测任务上相对 DETReg 提升约 100%（Table 1, Table 3）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/002_Figure_2.jpg]]
*Figure 2: Overview of FreeSOLO. Unlabeled images are first input to Free Mask to generate coarse object masks. The segmentation masks as well as their associated semantic embeddings are used to train a SOLO-based instance segmentation model via weak supervision. We use self-training to improve object mask segmentation*

FreeSOLO 的整体 pipeline 由两大支柱构成：**Free Mask** 与 **Self‑Supervised SOLO**，二者以串行自训练的方式衔接，形成“伪标签生成 → 弱监督训练 → 自训练精炼”的闭环（Figure 2）。

**输入**：无任何人工标注的原始图像。

**阶段一：Free Mask 生成粗糙掩码**。利用自监督预训练模型（默认 DenseCL，ResNet‑50 骨干）提取的稠密特征图，通过查询‑键注意力机制为每幅图像自动生成一组粗糙的类别无关物体掩码，并附带每个掩码的语义嵌入向量。该阶段完全无需标注，在 V100 GPU 上可达 21 FPS。

**阶段二：Self‑Supervised SOLO 弱监督训练**。将 Free Mask 输出的粗糙掩码作为伪标签，以弱监督投影损失（$\mathcal{L}_{mask} = \alpha \mathcal{L}_{avg‑proj} + \mathcal{L}_{max.proj} + \mathcal{L}_{pairwise}$）替代原始 SOLO 的 Dice loss，同时利用语义嵌入损失（$\mathcal{L}_{sem}$）约束类别分支，训练 SOLO 实例分割模型。投影损失的设计是关键：平均投影损失 $\mathcal{L}_{avg‑proj}$ 能防止模型坍缩为仅分割轮廓（移除后 AP 从 3.3 降至 2.0，见 Table 7e 与 Figure 5）。

**阶段三：自训练（一次迭代）**。用阶段二训练好的模型对训练集重新预测掩码，以这些质量更高的掩码再次训练模型。实验表明，一次自训练即可将 COCO 类无关实例分割 AP 从 3.3 提升至 4.0，但进一步迭代不再增益（Table 7c）。

**输出**：训练完成后，模型可直接执行类别无关的实例分割与目标检测，其预测掩码在定性上显著优于 Free Mask 的初始粗糙掩码（Figure 2）。此外，语义嵌入学习模块使模型在下游有监督微调时具备更强的迁移能力——仅用 5% COCO 掩码微调即比 DenseCL 预训练高出 +9.8% AP。

**模块间的因果链路**：Free Mask 提供初始定位信号 → 弱监督投影损失在粗糙伪标签上稳定训练 → 自训练利用模型自身能力提升伪标签质量 → 语义嵌入损失保留 Free Mask 提取的语义结构以辅助下游任务。这一设计将 SOLO 的“自上而下与自下而上相统一”的架构天然转化为自监督学习范式，使得全流程在零标注条件下得以运转。

FreeSOLO 的整体框架由两大支柱构成：**Free Mask** 负责从无标注图像中生成粗糙物体掩码，**Self‑Supervised SOLO** 则利用这些粗糙掩码以弱监督方式训练实例分割模型，并通过一次自训练进一步提升掩码质量（Figure 2）。

### 3.1 Free Mask：基于查询‑键注意力的粗糙掩码生成

Free Mask 的核心思想是利用自监督预训练模型产生的稠密特征图，通过查询‑键（query‑key）注意力机制自动发现图像中的物体区域。给定一张无标注图像，首先由自监督预训练的骨干网络提取稠密特征图 $\mathbf{I}$。将 $\mathbf{I}$ 经双线性下采样后构成查询集合 $\mathbf{Q}$，而 $\mathbf{I}$ 本身直接作为键集合 $\mathbf{K}$。

对于 $\mathbf{Q}$ 中的每一个查询向量 $\mathbf{Q}_q$，计算其与 $\mathbf{K}$ 中每个空间位置 $(i,j)$ 处的键向量 $\mathbf{K}_{i,j}$ 的余弦相似度，得到分数图 $\mathbf{S}$：

$$\mathbf{S}_{i,j,q} = \mathrm{sim}(\mathbf{Q}_q, \mathbf{K}_{i,j})$$

该操作等价于将归一化后的查询与键进行卷积：

$$\mathbf{S} = \mathbf{Q}' \circledast \mathbf{K}'$$

随后，每张分数图经过掩码质量评分（Maskness）和**非极大抑制（NMS）** 滤除冗余掩码，最终输出粗糙物体掩码集合 $\mathbf{M}$。整体流水线可表示为：

$$\mathbf{M} = \mathrm{NMS}(\mathrm{Maskness}(\mathrm{Norm}(\mathbf{Q}' \oplus \mathbf{K}')))$$

其中 $\mathrm{Norm}$ 为归一化操作，$\oplus$ 表示查询与键的相似度计算。Free Mask 在 V100 GPU 上以 ResNet‑50 为骨干可达 21 FPS 的掩码生成速度。

### 3.2 Self‑Supervised SOLO：弱监督投影损失与自训练

SOLO 框架的原始掩码生成公式为：

$$\mathbf{S} = \mathbf{G} \circledast \mathbf{F}$$

即通过预测的掩码核 $\mathbf{G}$ 与掩码特征 $\mathbf{F}$ 卷积得到分数图 $\mathbf{S}$。在 FreeSOLO 中，$\mathbf{G}$ 和 $\mathbf{F}$ 的训练不再依赖精确的人工标注，而是以 Free Mask 生成的粗糙掩码 $\mathbf{m}^*$ 作为伪标签，并采用一套**弱监督投影损失**来规避粗糙标签中的噪声。

核心设计在于将二维掩码监督退化为一维投影监督。设预测掩码为 $\mathbf{m}$，粗糙掩码为 $\mathbf{m}^*$，定义以下损失项：

**最大投影损失** $\mathcal{L}_{max.proj}$：沿 $x$ 轴和 $y$ 轴分别取最大值投影，计算投影向量之间的 Dice 损失：

$$\mathcal{L}_{max.proj} = \mathcal{L}(\max_x(\mathbf{m}), \max_x(\mathbf{m}^*)) + \mathcal{L}(\max_y(\mathbf{m}), \max_y(\mathbf{m}^*))$$

**平均投影损失** $\mathcal{L}_{avg-proj}$：沿 $x$ 轴和 $y$ 轴分别取平均值投影，计算 Dice 损失。该损失对离群像素不敏感，能有效保持物体形状并防止模型坍缩：

$$\mathcal{L}_{avg-proj} = \mathcal{L}(\mathrm{avg}_x(\mathbf{m}), \mathrm{avg}_x(\mathbf{m}^*)) + \mathcal{L}(\mathrm{avg}_y(\mathbf{m}), \mathrm{avg}_y(\mathbf{m}^*))$$

**掩码总损失** $\mathcal{L}_{mask}$ 由上述投影损失与成对亲和力损失 $\mathcal{L}_{pairwise}$ 加权组合而成：

$$\mathcal{L}_{mask} = \alpha \mathcal{L}_{avg-proj} + \mathcal{L}_{max.proj} + \mathcal{L}_{pairwise}$$

消融实验（Table 7e, Figure 5）表明，移除 $\mathcal{L}_{avg-proj}$ 会导致模型坍缩为仅分割物体轮廓，AP 从 3.3 降至 2.0，验证了平均投影损失在防止退化中的关键作用。

### 3.3 语义嵌入学习

Free Mask 为每个生成的掩码关联一个查询特征向量，作为该物体的语义嵌入 $\mathbf{q}^*$。在训练 SOLO 时，模型同时预测一个语义嵌入 $\mathbf{q}$，并通过**负余弦相似度损失**拉近预测嵌入与提取嵌入：

$$L_{sem} = 1 - \frac{\mathbf{q}}{\|\mathbf{q}\|_2} \cdot \frac{\mathbf{q}^*}{\|\mathbf{q}^*\|_2}$$

类别分支的总损失为焦点损失与语义损失的加权和：

$$\mathcal{L}_{cate} = \mathcal{L}_{focal} + \beta L_{sem}$$

语义嵌入学习主要提升下游有监督微调的性能：在 10% COCO 掩码微调时，该损失将 AP 从 24.9 提升至 25.6（Table 7f）。

### 3.4 自训练策略

初步训练后的 SOLO 模型能够预测出比 Free Mask 原始粗糙掩码质量更高的掩码。FreeSOLO 采用一次自训练：用当前模型重新生成伪标签，再训练一次模型。Table 7c 显示，一次自训练将 AP 从 3.3 提升至 4.0，但进一步迭代不再带来增益，表明模型在此框架下容易饱和。

## 实验与关键发现

### 核心实验设置

FreeSOLO 在无任何人工标注的条件下，使用 ResNet-50 作为骨干网络，以 DenseCL 自监督预训练权重初始化 Free Mask，在 MS COCO train2017 上完成自监督训练后，在 COCO val2017、UVO val 和 PASCAL VOC 等基准上评估类别无关的实例分割与目标检测能力。Free Mask 在 V100 GPU 上以 21 FPS 生成粗糙掩码，整体推理速度达 16 FPS。

### 类别无关实例分割主结果

Table 1 展示了 COCO val2017 上的类别无关实例分割性能。FreeSOLO 在完全无标注的条件下取得 **9.8% AP50**，优于需要不同程度人工标注的 **MCG**（Arbelaez et al., CVPR 2014）和 **COB**（Maninis et al., TPAMI 2018）等经典 proposal 方法。在更严格的 AP 指标下，FreeSOLO 达到 4.0 AP。这一结果表明，自监督稠密特征结合 SOLO 的“自上而下与自下而上相统一”架构，能够在零标注条件下产生具有竞争力的物体掩码。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/004_Table_1.jpg]]
*Table 1: Class-agnostic instance segmentation on MS COCO val2017. Both MCG and COB require annotations more or less. Table 2. Class-agnostic instance segmentation on UVO val split. Results of Mask R-CNN are from the paper of UVO [59]*

在 UVO val 数据集上（Table 2），FreeSOLO 取得 **4.8 AP**，进一步验证了其在开放世界场景下的泛化能力。

### 无监督目标检测与多目标发现

Table 3 报告了 COCO val2017 上的无监督类别无关目标检测结果。FreeSOLO 取得 **5.5 AP**，相比此前最优的无监督检测方法 **DETReg**（Bar et al., arXiv 2021）的 1.0 AP，实现了约 **450% 的相对提升**。在多目标发现任务上（Table 4），FreeSOLO 在 PASCAL VOC trainval07 上达到 **10.2 AP**，显著优于并发工作 **LOST\***（Simeoni et al., arXiv 2021）的 6.7 AP。这表明 Free Mask 生成的粗糙掩码不仅覆盖了显著目标，还能有效发现图像中的多个物体实例。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/006_Table_3.jpg]]
*Table 3: Unsupervised class-agnostic object detection on MS COCO val2017. Compared results are directly from DETReg*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/007_Table_4.jpg]]
*Table 4: Multi-object discovery on PASCAL VOC trainval07 and MS COCO 20k. LOST* is a concurrent work*

### 有限标注下的微调性能

FreeSOLO 的自监督预训练在下游有监督微调中展现出显著的迁移价值。Table 5 显示，仅使用 **2% COCO 全标注图像**微调时，FreeSOLO 预训练模型达到 22.0 AP，优于 DenseCL 预训练的 20.0 AP。当仅使用 **5% COCO 掩码标注**（无类别标签）微调时（Table 6），FreeSOLO 取得 **29.9 AP**，相比监督预训练基线的 20.1 AP 提升 **+9.8 AP**，相对改善约 49%。这证明 FreeSOLO 学到的物体定位和分割能力可作为强先验，大幅降低下游任务对标注数据的依赖。

### 消融实验

Table 7 系统性地拆解了 FreeSOLO 各设计组件的贡献，所有实验均使用 ResNet-50 骨干在 COCO val2017 上评估。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/015_Table_7.jpg]]
*Table 7: FreeSOLO ablation experiments. All the experiments are with a ResNet-50 backbone. We report class-agnostic instance segmentation results (a-e) and supervised fine-tuning results (f) on the COCO val2017 split. w/o $\mathcal { L } _ { a v g \_ p r o j }$*

**预训练方法选择（Table 7a）**：对比监督预训练、MoCo v2、InfoMin 和 DenseCL 作为 Free Mask 的初始化，**DenseCL 取得最优的 11.5 AR**。稠密对比学习捕获的局部特征一致性，为查询-键注意力生成物体掩码提供了更高质量的基础表示。

**金字塔查询（Table 7b）**：使用单一尺度查询时 AR 仅为 8.7，引入尺度为 [1.0, 0.5, 0.25] 的金字塔查询后 AR 提升至 **11.5**。多尺度查询使 Free Mask 能够覆盖不同大小的物体，是粗糙掩码召回率提升的关键设计。

**自训练迭代次数（Table 7c）**：以 Free Mask 的粗糙掩码为基线（记为迭代 -1），直接使用粗糙掩码训练 SOLO 的 AP 为 3.3。经过**一次自训练**后，AP 提升至 **4.0**，但进一步迭代不再带来增益。这表明模型在首轮自训练中已充分提炼了粗糙掩码中的有效信息，后续迭代因缺乏新的监督信号而饱和。

**弱监督与全掩码监督对比（Table 7d）**：若直接使用粗糙掩码进行全掩码 Dice loss 监督，AP 仅为 1.7；而采用投影损失等弱监督设计后，AP 提升至 **3.3**。粗糙掩码的边界和形状噪声在全掩码监督下会严重误导模型，弱监督投影损失通过降维操作有效抑制了噪声的影响。

**投影损失项拆解（Table 7e）**：完整的掩码损失 $\mathcal{L}_{mask} = \alpha \mathcal{L}_{avg-proj} + \mathcal{L}_{max.proj} + \mathcal{L}_{pairwise}$ 取得 3.3 AP。移除 $\mathcal{L}_{avg-proj}$ 后 AP 骤降至 **2.0**，且模型出现严重的**轮廓坍缩**现象——如 Figure 5 所示，模型仅分割物体轮廓而非完整区域。平均投影损失 $\mathcal{L}_{avg-proj}$ 通过对空间轴取均值，降低了对粗糙掩码中离群像素的敏感度，是防止坍缩的关键正则项。移除 $\mathcal{L}_{max.proj}$ 或 $\mathcal{L}_{pairwise}$ 同样导致不同程度的性能下降，验证了各损失项的协同作用。

**语义嵌入学习（Table 7f）**：在 10% COCO 掩码微调场景下，加入语义嵌入损失 $\mathcal{L}_{sem}$ 将 AP 从 24.9 提升至 **25.6**。通过负余弦相似度拉近预测嵌入与 Free Mask 提取的语义嵌入，模型在定位物体的同时保留了语义判别能力，这对下游有监督微调尤为有益。

### 失败模式分析

如 Figure 6 所示，FreeSOLO 在以下场景中容易失败：
- **截断目标**：物体被图像边界截断时，Free Mask 的查询-键注意力难以产生完整的响应，导致漏检或掩码不完整。
- **高度拥挤场景**：密集排列的同类物体使得粗糙掩码中的实例边界模糊，NMS 后处理可能错误地合并或删除相邻实例。
- **小目标**：骨干网络下采样后的特征图分辨率有限，小物体在查询-键相似度图中响应微弱，容易被 maskness 评分过滤。

这些失败模式揭示了当前自监督实例分割的关键瓶颈：粗糙掩码的质量上限受限于自监督预训练特征的分辨率和判别力，而弱监督训练策略虽能抑制噪声，却无法凭空恢复 Free Mask 完全遗漏的物体。

### 局限性总结

1. 自监督与全监督方法之间仍存在巨大差距（COCO AP 4.0 vs. 37+），实例分割的无监督学习远未解决。
2. 自训练超过一次不再提升，模型在现有框架下容易饱和，缺乏持续自我改进的机制。
3. Free Mask 对预训练方法敏感，其性能上限受限于当前稠密自监督学习的技术水平。
4. 截断、拥挤和小目标场景下的定位失败表明，单一尺度的查询-键注意力机制尚不足以处理复杂场景中的全部实例。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2202_12181/figures/018_Figure.jpg]]
*Figure: S1. More qualitative results of FreeSOLO for the task of class-agnostic instance segmentation. The model is trained without any kind of manual annotations and can infer at 16 FPS on a V100 GPU. Best viewed on screen. w/o ℒ????????????_???????????????? w/ ℒ????????????_????????????????*

## 定位与知识库关联

### 与基线方法的关系

FreeSOLO 建立在 **SOLO** 实例分割框架之上，将其从全监督范式改造为完全不依赖人工标注的自监督训练流程。SOLO 原始设计中“自上而下的目标定位与自下而上的像素分组相统一”的特性，天然地将像素分组、目标定位和特征学习融为一体，使得整个流程可以在无标注条件下运作。FreeSOLO 的核心改造体现在三个关键插槽：

- **监督信号类型**：SOLO 原始使用精确的 ground‑truth 掩码计算 Dice loss；FreeSOLO 将其替换为粗糙掩码配合弱监督投影损失 $\mathcal{L}_{mask} = \alpha \mathcal{L}_{avg-proj} + \mathcal{L}_{max.proj} + \mathcal{L}_{pairwise}$，其中 $\mathcal{L}_{avg-proj}$ 和 $\mathcal{L}_{max.proj}$ 分别沿 x/y 轴对预测掩码和伪标签掩码进行平均投影和最大投影后计算 Dice 损失，$\mathcal{L}_{pairwise}$ 为成对亲和力损失。
- **伪标签来源**：SOLO 依赖人工标注；FreeSOLO 通过 Free Mask 模块利用自监督稠密特征自动生成粗糙掩码。Free Mask 的核心机制是查询-键注意力：将自监督特征图下采样得到查询 $\mathbf{Q}$，原始特征图作为键 $\mathbf{K}$，通过余弦相似度 $\mathbf{S}_{i,j,q} = \mathrm{sim}(\mathbf{Q}_q, \mathbf{K}_{i,j})$ 生成分数图，再经掩码质量评分（Maskness）和非极大抑制（NMS）输出粗糙掩码 $\mathbf{M} = \mathrm{NMS}(\mathrm{Maskness}(\mathrm{Norm}(\mathbf{Q}' \oplus \mathbf{K}')))$。
- **训练策略**：SOLO 直接使用标注训练；FreeSOLO 先通过 Free Mask 生成伪标签进行弱监督预训练，再进行一次自训练（self‑training）以提升掩码质量。

在无监督实例分割的对比中，FreeSOLO 与需要不同程度人工标注的经典方法形成鲜明对照：**MCG**（Arbeláez et al., CVPR 2014）基于区域提议，**COB**（Maninis et al., TPAMI 2018）基于轮廓分割，二者均依赖标注信息。FreeSOLO 在完全不使用任何标注的情况下，在 COCO val2017 上取得 9.8% AP50 的类别无关实例分割结果，超越了需要标注的最佳 baseline COB（8.8% AP50）。

在无监督目标检测任务中，FreeSOLO 与 **DETReg**（Bar et al., arXiv 2021）对比，在 COCO val2017 上取得 5.5 AP，相对 DETReg 的 1.0 AP 提升约 450%。在多目标发现任务中，FreeSOLO 在 PASCAL VOC trainval07 上取得 10.2 AP，显著优于并发工作 **LOST\***（Simeoni et al., arXiv 2021）的 6.7 AP。

在自监督预训练方面，FreeSOLO 使用 **DenseCL** 作为 Free Mask 的预训练初始化。消融实验（Table 7a）表明，DenseCL 在多种自监督预训练方法中表现最佳。当以 5% COCO 掩码标注进行微调时，FreeSOLO 预训练达到 29.9 AP，比 DenseCL 预训练高出 +9.8 AP，验证了 FreeSOLO 自监督预训练在下游任务中的迁移价值。

### 适用边界与局限

FreeSOLO 的有效性依赖于以下前提条件：

1. **自监督预训练质量**：Free Mask 的粗糙掩码质量直接取决于自监督预训练模型的特征表达能力。消融实验证实 DenseCL 优于其他预训练方法，表明该模块对预训练方法的选择敏感。若预训练特征缺乏足够的物体感知能力，Free Mask 生成的伪标签质量将下降，进而影响整个流程。

2. **目标完整性与尺度**：论文明确指出的失败场景（Figure 6）包括目标被截断、高度拥挤或尺寸过小的情况，此时 FreeSOLO 可能定位失败。这表明 Free Mask 的查询-键注意力机制在处理不完整或严重遮挡的目标时存在局限性。

3. **自训练饱和**：消融实验（Table 7c）显示，一次自训练将 AP 从 3.3 提升至 4.0，但进一步迭代不再带来增益。模型在单轮自训练后迅速饱和，说明当前的自训练策略无法持续提升掩码质量。

4. **与全监督方法的差距**：尽管 FreeSOLO 在无监督设置下取得了显著进展，但其 COCO 实例分割 AP（4.0）与全监督 SOLO 方法（37+ AP）之间仍存在巨大差距。这一差距反映了当前自监督实例分割技术的整体水平限制。

5. **弱监督投影损失的关键作用**：消融实验（Table 7e, Figure 5）表明，移除平均投影损失 $\mathcal{L}_{avg-proj}$ 会导致 AP 从 3.3 降至 2.0，且模型会坍缩为仅分割目标轮廓。这说明弱监督设计中的平均投影操作对于防止模型学习到退化解至关重要——它通过对离群像素的去敏感化，迫使模型关注目标的整体形状而非边缘。

### 开放问题

1. **如何进一步缩小自监督与全监督实例分割之间的巨大差距？** 当前 FreeSOLO 的 COCO AP（4.0）与全监督方法（37+）之间的鸿沟表明，仅靠现有自监督预训练和弱监督训练策略远不足以弥合这一差距。是否需要全新的自监督学习范式，或者引入额外的弱先验（如运动线索、深度信息）？

2. **自监督分割模型能否超越使用人工标注训练的模型？** 论文在 Figure S3 中展示了 FreeSOLO 在某些目标边界处能产生比人工标注更精确的分割，这暗示自监督方法可能在某些维度上具有独特优势。但整体性能的超越仍是一个开放挑战。

3. **如何将 FreeSOLO 扩展到无监督全景分割？** 当前 FreeSOLO 仅处理类别无关的实例分割，尚未涉及语义类别预测和背景区域（stuff）的分割。将 FreeSOLO 的“自上而下与自下而上相统一”的设计理念扩展到全景分割，需要同时解决无监督语义发现和 stuff 区域分割的难题。

4. **是否存在更好的预训练方法，使 Free Mask 能生成更高分辨率的精细掩码？** Free Mask 目前使用 DenseCL 预训练特征，其掩码质量受限于预训练方法的分辨率和细粒度表征能力。探索能够学习高分辨率精细表征的自监督预训练方法，可能直接提升 Free Mask 输出的伪标签质量。

5. **为何自训练超过一次不再提升，是否存在更好的自训练策略？** 当前自训练在单轮后即饱和，这一现象的原因尚不明确。可能的原因包括：模型在粗糙伪标签上训练后已经收敛到局部最优；第二轮自训练使用的伪标签与第一轮高度相似，未能引入新的信息。探索噪声鲁棒的自训练策略、渐进式伪标签精炼或多轮协同训练可能是突破方向。

6. **FreeSOLO 的物体发现机制是否具有类别偏向？** Free Mask 的查询-键注意力机制倾向于发现“常见物体”，但论文未系统分析其对不同类别、尺度、外观变化的目标的发现偏差。理解这一偏向对于评估方法的公平性和泛化性至关重要。

## 原文 PDF

![[paperPDFs/CVPR_2022/FreeSOLO_Learning_to_Segment_Objects_without_Annotations.pdf]]
