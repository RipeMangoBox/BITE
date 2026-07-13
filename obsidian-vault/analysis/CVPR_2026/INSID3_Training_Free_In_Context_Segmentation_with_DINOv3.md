---
title: "INSID3: Training-Free In-Context Segmentation with DINOv3"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/INSID3_Training_Free_In_Context_Segmentation_with_DINOv3.pdf
project_link: https://visinf.github.io/INSID3
code_link: null
aliases:
- INSID3
tags:
- CVPR_2026
- topic/vision_multimodal_applications/segmentation
- topic/vision_multimodal_applications
core_operator: 使用冻结的DINOv3稠密特征，并通过噪声图像估计位置子空间并投影去除，从而实现无训练的上下文分割，且仅需聚类-选择-聚合三个简单阶段。
primary_logic: DINOv3的纯自监督稠密特征天然具备强空间结构和高粒度的语义对应能力；通过去除位置偏差，该特征可直接用于跨图像匹配与图像内分组，使得任意粒度的分割从单一骨干中涌现，无需任何解码器或外部分割模型。
claims:
- INSID3在one-shot语义、部件和个性化分割的平均mIoU达到55.1%，比先前的训练自由方法平均提升+7.5% mIoU。
- INSID3仅使用304M参数（单骨干DINOv3），而代表性训练自由基线GF-SAM使用945M参数。
- 通过噪声图像估计位置子空间并正交投影，去偏特征在语义对应任务SPair-71k上带来高达+6.6 PCK的增益，并显著抑制虚假的位置相关激活。
- 无聚类和无自相似性聚合的基线在COCO-20i和PASCAL-Part上仅获得44.2%和35.4% mIoU，而完整INSID3达到57.6%和50.5%，验证了聚类与聚合的关键作用。
---

# INSID3: Training-Free In-Context Segmentation with DINOv3

> [!tip] 核心洞察
> DINOv3的纯自监督稠密特征天然具备强空间结构和高粒度的语义对应能力；通过去除位置偏差，该特征可直接用于跨图像匹配与图像内分组，使得任意粒度的分割从单一骨干中涌现，无需任何解码器或外部分割模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | INSID3: 基于DINOv3的无训练上下文分割 |
| 英文题名 | INSID3: Training-Free In-Context Segmentation with DINOv3 |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.28480) · [Project](https://visinf.github.io/INSID3) |
| Topic | #topic/vision_multimodal_applications/segmentation #topic/vision_multimodal_applications |
| Method | INSID3 |
| Dataset | LVIS-92i, COCO-20i, ISIC, Chest X-Ray |

> [!tip] 效果简介
> - LVIS-92i (语义) 上，mIoU (%) 41.8 vs 35.2 (GF-SAM) (+6.6)。
> - COCO-20i (语义) 上，mIoU (%) 57.6 vs 58.7 (GF-SAM) (-1.1)。
> - ISIC (语义) 上，mIoU (%) 54.4 vs 48.7 (GF-SAM) (+5.7)。

## 概要

上下文分割（In-Context Segmentation, ICS）旨在根据一张带有掩码标注的参考图像，在目标图像中分割出同一语义概念。现有方法主要沿两条路线：一是通过微调解码器（如SegIC、SegGPT等）学习任务特定的映射，二是在冻结的语义对应模型（如DINOv2）上叠加预训练的掩码先验（如SAM），构成多模型组合（如Matcher、GF-SAM）。前者在域内表现良好但泛化能力受限，后者依赖大规模有监督的掩码预训练，参数规模庞大（GF-SAM约945M），且语义对应与掩码生成之间存在解耦的脆弱性。

本工作揭示了DINOv3稠密自监督特征中一个此前未被充分认识的现象：特征中存在系统性的位置偏差（positional bias）——相似空间位置的patch在无关图像间也会产生虚假的高相似度匹配，严重损害跨图像语义对应。在此基础上，本文提出**INSID3**，一种完全无训练、单一骨干的上下文分割方法。其核心洞察在于：DINOv3的纯自监督稠密特征天然具备强空间结构和高粒度的语义对应能力；通过去除位置偏差，该特征可直接用于跨图像匹配与图像内分组，使得任意粒度的分割从单一骨干中涌现，无需任何解码器或外部分割模型。

INSID3仅包含三个简单阶段：**凝聚聚类**将目标图像划分为语义一致的区域簇；**种子簇选择**通过反向最近邻和去偏特征相似度识别与参考区域最匹配的目标簇；**自相似性聚合**结合跨图像语义相似度和目标内结构亲和度，合并相关簇形成最终掩码。整个流程仅使用一个冻结的DINOv3骨干（304M参数），无需任何训练、微调或模型组合。

在涵盖语义、部件和个性化分割的多个基准上，INSID3以平均55.1% mIoU超越先前的训练自由方法+7.5个百分点，同时参数量仅为GF-SAM的三分之一。在医学影像（Chest X-Ray +27.8 mIoU）、遥感（ISIC +5.7 mIoU）等域外数据集上优势尤为显著，验证了其强大的泛化能力。

### 上下文分割：从“看见”到“模仿”

计算机视觉系统长期追求一种类似人类的泛化能力：给定一个带标注的参考图像，模型应能立即理解“分割目标是什么”，并在任意新图像中找出对应区域，无论其语义粒度是完整物体、部件还是个性化概念。这一任务被称为上下文分割（In-Context Segmentation, ICS），其核心挑战在于**仅凭单个示例建立跨图像的语义对应，并将其转化为精确的像素级掩码**。

传统方案通常将ICS拆解为两个子问题——先找到对应关系，再生成掩码——并依赖大规模监督预训练来弥合两者的鸿沟。然而，这种拆解带来了根本性的架构负担：模型要么需要微调解码器来适配特定领域，要么必须组合多个独立模型（如一个用于特征匹配、另一个用于掩码生成），导致参数膨胀和跨域泛化能力受限。

### 现有路线的结构性困境

当前ICS方法大致分为两条技术路线，各自存在系统性缺陷：

**微调路线**（如 **SegIC**、**DiffewS**、**SegGPT**）在特定训练域内表现优异，但泛化能力受限于训练分布。一旦面对域外数据——例如从自然图像切换到医学影像或遥感场景——性能急剧退化。这类方法的本质问题在于：**将分割能力编码进可训练的解码器参数中，使得模型学到的是一种“数据集特定的分割先验”，而非通用的语义对应能力**。

**训练自由路线**（如 **PerSAM**、**Matcher**、**GF-SAM**）通过组合自监督特征提取器（如DINOv2）与预训练分割模型（如SAM）来避免下游微调。SAM提供了强大的掩码先验，但其代价是巨大的参数规模（GF-SAM约945M参数）和两阶段流程的耦合脆弱性：对应模块找到的语义区域与SAM生成的掩码之间缺乏闭环反馈，常常导致过分割或欠分割（见Figure 5）。更根本地，**这些方法并未真正从自监督特征中“涌现”分割能力，而是将分割外包给了外部的监督模型**。

### 被忽视的可能性：单骨干涌现

上述困境指向一个被长期忽视的问题：**能否仅用一个冻结的自监督骨干，在不附加任何解码器、不组合任何外部分割模型的前提下，直接完成上下文分割？**

这一问题的难点在于，自监督特征（如DINOv2）虽然具备强大的图像级语义表达，但其稠密patch特征在跨图像匹配时存在两个关键障碍：
1. **语义对应不够精细**：全局语义相似度高，但局部空间对齐能力弱；
2. **位置偏差**：特征中混杂了与语义无关的绝对位置信息，导致“相同位置”的patch在不同图像间产生虚假匹配。

DINOv3的出现改变了这一局面。其稠密特征展现出更强的空间结构和语义粒度（见Figure 2的聚类效果），使得“从特征中直接读出分割”成为可能。然而，**DINOv3的特征中同时存在比DINOv2更强的系统性位置偏差**（见Figure 4和Figure 8）：相似度图在参考坐标位置产生高激活，无论该位置的实际语义内容如何。这一偏差严重损害跨图像匹配的准确性，成为单骨干方案必须跨越的核心障碍。

### 本文的核心动机

INSID3的出发点正是上述洞察：**DINOv3的稠密自监督特征已经蕴含了足够丰富的语义和结构信息，足以支撑上下文分割——前提是能有效去除位置偏差，并设计一种无需训练的机制来组织这些信息**。

具体而言，本文试图回答以下问题：
- 能否通过一种极轻量的训练自由策略（而非数据增强或微调）来估计并消除DINOv3中的位置偏差？
- 能否仅依赖聚类、跨图像匹配和自相似性聚合这三个简单阶段，从去偏特征中直接生成任意粒度的分割掩码？
- 这种单骨干方案能否在参数规模远小于SAM组合方法的前提下，实现更强的跨域泛化能力？

这些问题的回答指向一个更根本的命题：**鲁棒的分割能力是否可以直接从纯自监督表征中涌现，而无需任何形式的掩码监督——无论是预训练阶段的SAM，还是下游微调阶段的解码器？**

## 核心方法与创新机理

INSID3的核心创新在于**完全摒弃了有监督掩码先验与模型组合，首次证明单个冻结的自监督DINOv3骨干即可涌现出跨粒度、跨领域的上下文分割能力**。这一突破围绕三个紧密耦合的changed slots展开。

### 从多模型组合到单骨干自监督涌现

现有训练自由方法普遍依赖SAM的掩码预训练先验：**Matcher**（Liu et al., ICLR 2024）和**GF-SAM**（Wysoczańska et al., NeurIPS 2024）均采用DINOv2/DINOv3提取语义对应，再交由SAM生成掩码，形成双模型串联架构。微调方法如**SegIC**（Meng et al., ECCV 2024）和**DiffewS**（Chen et al., CVPR 2025）则需在下游数据集上训练专用解码器。这些方案的根本瓶颈在于**语义对应与掩码生成被解耦到不同模型**，导致跨域泛化时两个环节的误差累积，且参数规模庞大（GF-SAM达945M）。

INSID3的changed slot是将整个架构压缩为**单个冻结的DINOv3 ViT-L/14骨干（304M参数）**，无解码器、无微调、无模型组合。其核心洞察是：DINOv3的稠密patch特征天然具备双重能力——跨图像的强语义对应（支撑“找什么”）和图像内的空间结构分组（支撑“在哪切”）。这一发现将分割问题转化为**聚类-选择-聚合**三个纯后处理阶段，使任意粒度的分割直接从自监督表征中涌现。

### 位置偏差的系统性发现与训练自由矫正

DINOv3稠密特征存在一个此前未被充分认识的**系统性位置偏差**：相似度图中会出现与参考坐标对齐的虚假激活，且该模式与语义内容无关（Figure 4）。这种偏差严重损害跨图像匹配的可靠性，是阻碍单骨干分割的关键障碍。

INSID3的changed slot体现在**通过单张噪声图像估计位置子空间并投影去除**，而非依赖数据增强或忽略该问题。具体而言，对随机噪声图像提取的DINOv3特征进行SVD，取前s个右奇异向量构成位置子空间基B，再将参考与目标特征投影到其正交补上：

$$\tilde{\mathbf{F}}^{r} = \mathbf{F}^{r} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top}), \quad \tilde{\mathbf{F}}^{t} = \mathbf{F}^{t} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top})$$

这一去偏策略的关键证据链：在语义对应任务SPair-71k上，去偏使DINOv3-L的PCK@0.10提升5.0个百分点，而DINOv2仅提升0.3个百分点（Table 4），证实DINOv3存在特有的强位置偏差。更关键的是，去偏后的特征经PCA压缩仍优于原始特征的PCA压缩（Figure 9），说明被移除的方向主要编码位置信息，剩余方差集中于语义结构。

### 从相似度阈值到聚类-种子选择-自相似性聚合

传统上下文分割通常直接对相似度图阈值化生成掩码，这会产生碎片化或过度扩散的预测（Figure 4a）。INSID3的changed slot是将分割生成重构为三个阶段：

1. **凝聚聚类**：在目标图像原始特征空间中进行无监督凝聚聚类，将patch划分为语义一致的空间区域簇，无需预定义簇数量（Figure 2）。
2. **反向最近邻种子选择**：通过跨图像去偏特征的反向最近邻匹配，筛选出最近邻落在参考掩码内的目标patch，再选择与之有交集的聚类簇中跨图像相似度最高者作为种子。
3. **自相似性聚合**：将跨图像语义相似度与目标内自相似度相乘，合并与种子高度相关的候选簇，形成连通掩码。

消融实验（Table 3）提供了决定性证据：移除聚类与聚合后，COCO-20i的mIoU从57.6%骤降至44.2%，PASCAL-Part从50.5%降至35.4%，降幅分别达13.4和15.1个百分点。这表明聚类提供的结构化分组与自相似性聚合对分割质量至关重要，远非简单相似度阈值可比。

### 创新协同效应

上述三个changed slots并非孤立改进，而是形成因果闭环：**位置去偏使跨图像语义对应可靠，可靠的对应使种子选择精准，精准的种子结合聚类分组使聚合产生高质量连通掩码**。这一协同效应使INSID3在仅使用304M参数的条件下，在one-shot语义、部件和个性化分割上平均mIoU达55.1%，比先前的训练自由方法平均提升+7.5% mIoU（Table 1），且在医学影像（Chest X-Ray +27.8%）、遥感等域外数据集上优势尤为显著。

INSID3 的核心设计理念是：**单一个冻结的自监督骨干即可涌现上下文分割能力**。整个 pipeline 无需任何解码器、微调或模型组合，仅依赖 DINOv3 的稠密 patch 特征，通过三个概念阶段将示例掩码传递至目标图像。

### 输入输出规范

给定一对图像——包含标注区域的参考图像 $\mathbf{I}^{r}$ 和目标图像 $\mathbf{I}^{t}$，以及参考二值掩码 $\mathbf{M}^{r}$——INSID3 输出目标图像中对应语义区域的二值掩码。系统仅需三个固定超参数（Table 6），在所有数据集和分割粒度上保持一致。

### 三阶段流水线

整个推理流程（Figure 3）可分解为以下串行模块：

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/003_Figure_3.jpg]]
*Figure 3: Overview of INSID3. We leverage the semantic and spatial structure of DINOv3 to perform in-context segmentation without training or model composition. Dense features from the reference and target images are first debiased to suppress positional bias, improving cross-image matching. The target is then decomposed into coherent regions through agglomerative clustering, providing a structured representation. We retain candidate clusters that match the reference through backward correspondence in the debiased space; a reference prototype derived from the annotated region anchors the seed cluster via cross-image similarity. Finally, we combine cross-image similarity, capturing semantic alignment,...*

**阶段一：特征提取与位置去偏（Section 3.1）**
- 使用冻结的 DINOv3 编码器 $\Phi$ 分别提取参考与目标图像的稠密 patch 特征：
  $$\mathbf{F}^{r} = \Phi(\mathbf{I}^{r}), \quad \mathbf{F}^{t} = \Phi(\mathbf{I}^{t})$$
- 发现 DINOv3 特征存在系统性位置偏差——相似空间位置的 patch 在无关图像间也会产生虚假的高相似度匹配（Figure 4a-b）。
- 通过单张随机噪声图像 $\mathbf{I}^{\mathrm{noise}}$ 提取特征 $\mathbf{F}^{\mathrm{noise}}$，对其执行 SVD 并取前 $s$ 个右奇异向量构成位置子空间基 $\mathbf{B}$。
- 将参考与目标特征投影到该子空间的正交补上，得到去偏特征：
  $$\tilde{\mathbf{F}}^{r} = \mathbf{F}^{r} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top}), \quad \tilde{\mathbf{F}}^{t} = \mathbf{F}^{t} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top})$$
  该投影矩阵可离线预计算并存储，推理时仅需单次矩阵乘法，计算开销可忽略（Table 5）。

**阶段二：目标图像凝聚聚类（Section 3.2）**
- 在**原始**特征空间中对目标 patch 执行迭代凝聚聚类，将图像划分为 $K$ 个互不相交的空间区域：
  $$\bigcup_{k=1}^{K} \mathcal{G}_{k} = \Omega, \quad \mathcal{G}_{i} \cap \mathcal{G}_{j} = \emptyset \quad \forall i \neq j$$
- 聚类无需预定义簇数量，自动产生具有语义一致性的空间分组（Figure 2），为后续选择与聚合提供结构化表示。

**阶段三：种子选择与簇聚合（Section 3.3–3.4）**
- **反向最近邻过滤**：在去偏空间中，为每个目标 patch $i$ 找到参考图中最相似的 patch $\mathrm{NN}(i)$，仅保留最近邻落在参考掩码内的目标 patch 作为候选集 $\mathcal{C}_{\mathrm{NN}}$。
- **候选簇筛选**：选择与候选 patch 有交集的聚类簇构成候选簇集 $\mathcal{C}_{\mathrm{cand}}$。
- **种子簇选择**：计算各候选簇的去偏特征原型与参考原型的跨图像余弦相似度 $s_{k}^{\mathrm{cross}}$，选取相似度最高的簇作为种子 $\mathcal{G}^{*}$。
- **簇聚合**：结合跨图像语义相似度 $s_{k}^{\mathrm{cross}}$ 与目标内自相似度 $s_{k}^{\mathrm{intra}}$（候选簇与种子簇在原始特征空间中的相似度），通过乘性得分 $S_{k} = s_{k}^{\mathrm{cross}} \cdot s_{k}^{\mathrm{intra}}$ 合并得分超过阈值 $\alpha$ 的候选簇：
  $$\mathcal{M}_{\mathrm{final}} = \mathcal{G}^{*} \cup \{ \mathcal{G}_{k} \in \mathcal{C}_{\mathrm{cand}} \mid S_{k} \geq \alpha \}$$

**可选后处理**：最终掩码经过全连接条件随机场（CRF）优化边缘，提升空间精度。

### 关键设计决策

| 设计维度 | 选择 | 依据 |
|---------|------|------|
| 特征空间分工 | 去偏空间用于跨图像匹配，原始空间用于图像内分组 | 去偏增强语义对应（Table 2），原始特征保留完整空间结构利于聚类 |
| 聚类时机 | 在目标图像侧执行，参考侧不聚类 | 参考掩码已提供精确区域，仅需目标侧的结构化分解 |
| 种子选择策略 | 反向最近邻 + 跨图像相似度最大化 | 直接相似度阈值易产生广泛激活（Figure 4a），反向匹配引入负证据抑制无关区域 |
| 聚合机制 | 乘性得分结合语义对齐与结构一致性 | 消融实验表明，去除聚类和自相似性聚合后 COCO-20i 从 57.6% 降至 44.2% mIoU（Table 3） |

### 参数规模与扩展性

INSID3 仅使用单个 DINOv3 骨干（304M 参数），而代表性训练自由基线 GF-SAM 需 945M 参数（Table 1）。该框架可自然扩展至多示例上下文（最多 5-shot），无需调整任何超参数，平均 mIoU 从 55.1% 提升至 59.9%（Table 7）。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/001_Figure_1.jpg]]
*Figure 1: Results and overview of INSID3, our training-free in-context segmentation approach. INSID3 performs in-context segmentation directly from DINOv3 [56] features, without any decoder, fine-tuning, or model composition. (left) A single annotated example guides the model to segment any concept, from object parts to medical images and aerial views. (right) Comparing generalization across datasets and segmentation granularities: fine-tuned methods (orange) excel in-domain ( ) but degrade out of distribution, while SAMbased pipelines (blue) generalize better but rely on large, multi-stage architectures. INSID3 (purple) achieves the strongest generalization with a single backbone, revealing that rob...*

INSID3 由三个核心阶段构成：**位置去偏特征提取**、**目标图像凝聚聚类**、**种子选择与簇聚合**。整个流程无需任何训练或模型组合，仅依赖冻结的 DINOv3 编码器。

### 3.1 特征提取与位置去偏

给定参考图像 $\mathbf{I}^{r}$ 和目标图像 $\mathbf{I}^{t}$，使用冻结的 DINOv3 编码器 $\Phi$ 提取稠密 patch 特征：

$$
\mathbf{F}^{r} = \Phi(\mathbf{I}^{r}), \quad \mathbf{F}^{t} = \Phi(\mathbf{I}^{t}) \tag{1}
$$

其中 $\mathbf{F}^{r}, \mathbf{F}^{t} \in \mathbb{R}^{P \times D}$，$P$ 为 patch 数量，$D$ 为特征维度。

**关键发现**：DINOv3 的稠密特征存在系统性的位置偏差——相似空间位置的 patch 在跨图像匹配时会产生虚假的高相似度激活，与语义内容无关（见 Figure 4）。这一偏差在 DINOv2 中几乎不存在，是 DINOv3 特有的现象。

**去偏策略**：输入一张随机噪声图像 $\mathbf{I}^{\mathrm{noise}}$，提取其特征：

$$
\mathbf{F}^{\mathrm{noise}} = \Phi(\mathbf{I}^{\mathrm{noise}}) \in \mathbb{R}^{P \times D} \tag{3}
$$

对 $\mathbf{F}^{\mathrm{noise}}$ 进行奇异值分解（SVD），选取前 $s$ 个右奇异向量构成位置子空间的基 $\mathbf{B} \in \mathbb{R}^{D \times s}$。然后将参考与目标特征投影到该子空间的正交补上：

$$
\tilde{\mathbf{F}}^{r} = \mathbf{F}^{r} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top}), \quad \tilde{\mathbf{F}}^{t} = \mathbf{F}^{t} (\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top}) \tag{4}
$$

该投影矩阵 $(\mathbf{1}_{D} - \mathbf{B} \mathbf{B}^{\top})$ 可离线预计算并存储，推理时仅需单次矩阵乘法，计算开销可忽略。去偏后，跨图像匹配在语义对应任务 SPair-71k 上带来高达 **+6.6 PCK** 的增益（Table 2），并显著抑制与位置相关的虚假激活。

### 3.2 目标图像凝聚聚类

在原始特征空间中对目标图像的 $P$ 个 patch 进行迭代凝聚聚类，将其划分为 $K$ 个不相交的空间区域：

$$
\bigcup_{k=1}^{K} \mathcal{G}_{k} = \Omega, \quad \mathcal{G}_{i} \cap \mathcal{G}_{j} = \emptyset \quad \forall i \neq j \tag{5}
$$

聚类在 DINOv3 特征上自然产生语义连贯的区域划分（Figure 2），为后续种子选择提供结构化的候选单元。聚类粒度由距离阈值 $\tau = 0.6$ 控制，无需预定义簇数 $K$。

### 3.3 种子簇选择

**参考原型计算**：对参考掩码区域 $\mathcal{R}$ 内的特征取均值，得到去偏参考原型：

$$
\tilde{\mathbf{p}}^{r} = \frac{1}{|\mathcal{R}|} \sum_{j \in \mathcal{R}} \tilde{\mathbf{F}}_{j}^{r} \tag{9}
$$

**反向最近邻过滤**：对每个目标 patch $i$，在去偏空间中寻找参考图中最相似的 patch：

$$
\mathrm{NN}(i) = \arg\max_{j \in \Omega} \langle \tilde{\mathbf{F}}_{i}^{t}, \tilde{\mathbf{F}}_{j}^{r} \rangle \tag{6}
$$

保留最近邻落在参考掩码内的目标 patch 作为候选：

$$
\mathcal{C}_{\mathrm{NN}} = \{ i \mid \mathbf{M}_{\mathrm{NN}(i)}^{r} = 1 \} \tag{7}
$$

将与候选 patch 有交集的聚类簇纳入候选集：

$$
\mathcal{C}_{\mathrm{cand}} = \{ \mathcal{G}_{k} \mid \mathcal{G}_{k} \cap \mathcal{C}_{\mathrm{NN}} \neq \emptyset \} \tag{8}
$$

**种子选择**：计算每个候选簇的去偏原型 $\tilde{\mathbf{p}}_{k}^{t}$，其与参考原型的跨图像余弦相似度为：

$$
s_{k}^{\mathrm{cross}} = \langle \tilde{\mathbf{p}}_{k}^{t}, \tilde{\mathbf{p}}^{r} \rangle \tag{10}
$$

选择相似度最高的簇作为种子：

$$
\mathcal{G}^{*} = \arg\max_{\mathcal{G}_{k} \in \mathcal{C}_{\mathrm{cand}}} s_{k}^{\mathrm{cross}} \tag{11}
$$

### 3.4 簇聚合

种子确定后，需合并与之语义一致的其他候选簇。聚合得分由两项乘性组合：

**跨图像语义相似度** $s_{k}^{\mathrm{cross}}$：衡量候选簇与参考原型的语义对齐程度（式 10）。

**自相似度**：在原始特征空间中计算候选簇原型 $\bar{\mathbf{p}}_{k}^{t}$ 与种子簇原型 $\bar{\mathbf{p}}_{*}^{t}$ 的余弦相似度：

$$
s_{k}^{\mathrm{intra}} = \langle \bar{\mathbf{p}}_{k}^{t}, \bar{\mathbf{p}}_{*}^{t} \rangle \tag{12}
$$

该度量捕捉目标图像内部的结构一致性，抑制外观相似但结构不连贯的虚假匹配。

**合并得分**：

$$
S_{k} = s_{k}^{\mathrm{cross}} \cdot s_{k}^{\mathrm{intra}} \tag{13}
$$

**最终掩码**：合并种子及所有得分超过阈值 $\alpha = 0.2$ 的候选簇：

$$
\mathcal{M}_{\mathrm{final}} = \mathcal{G}^{*} \cup \{ \mathcal{G}_{k} \in \mathcal{C}_{\mathrm{cand}} \mid S_{k} \geq \alpha \} \tag{14}
$$

该乘性得分机制将语义对齐与结构连贯性统一为单一判据，消融实验表明：移除聚类与自相似性聚合后，COCO-20i 的 mIoU 从 57.6% 骤降至 44.2%，PASCAL-Part 从 50.5% 降至 35.4%（Table 3），验证了该设计的核心作用。

## 实验与关键发现

### 核心实验设置

INSID3在三个分割粒度上接受评估：语义分割（LVIS-92i、COCO-20i、ISIC、Chest X-Ray、DRAM）、部件分割（PASCAL-Part、PACO-Part）和个性化分割（PerMIS）。所有实验均采用one-shot上下文设置，即提供一个参考图像及其完整掩码作为提示。方法仅使用三个超参数——聚类粒度τ=0.6、聚合阈值α=0.2、去偏秩s=500——且在所有数据集和任务上保持固定，无需任何逐数据集调参（Table 6）。骨干网络为冻结的DINOv3-L/16，参数量304M。

### 主实验结果

**语义分割。** 在LVIS-92i上，INSID3达到41.8% mIoU，比先前最优训练自由方法GF-SAM（35.2%）高出+6.6个百分点。在跨域医学数据集上优势更加显著：ISIC皮肤镜分割54.4%（+5.7）、Chest X-Ray胸部X光分割78.8%（+27.8）。在COCO-20i上，INSID3取得57.6% mIoU，略低于GF-SAM的58.7%（-1.1），但仍显著超越其他训练自由基线如Matcher（52.9%）。在遥感数据集DRAM上达到47.3%，比GF-SAM的37.8%高出+9.5个百分点。

**部件分割。** 在PASCAL-Part上，INSID3取得50.5% mIoU，超越GF-SAM（44.5%）+6.0个百分点；在PACO-Part上达到32.4%，比GF-SAM（30.0%）高+2.4个百分点。值得注意的是，INSID3在部件粒度上甚至超越了部分微调方法（如SegIC在PASCAL-Part上为48.7%），而后者在训练域内通常占优。

**个性化分割。** 在PerMIS基准上，INSID3达到67.0% mIoU，比GF-SAM（54.1%）大幅提升+12.9个百分点，彰显了自监督特征在开放世界概念上的强泛化能力。

**综合对比。** 三个粒度的平均mIoU为55.1%，比先前训练自由方法平均提升+7.5% mIoU。这一优势在仅使用304M参数的单骨干下取得——GF-SAM需945M参数（DINOv3+SAM组合），参数量约为INSID3的3倍。Table 1汇总了所有主实验结果。

### 位置去偏的因果验证

**语义对应任务。** 在SPair-71k上，DINOv3-L原始特征的PCK@0.10为54.0，去偏后提升至59.0（+5.0个百分点）；DINOv3-B从46.6提升至53.2（+6.6个百分点）。相比之下，DINOv2-L的去偏增益仅+0.3个百分点（Table 4）。这直接证明了DINOv3存在特有的强位置偏差，而去偏投影是解锁其跨图像匹配能力的关键操作。

**定性证据。** Figure 4a-b显示，原始DINOv3特征的相似度图在参考坐标对应位置产生结构性高激活，与语义无关；去偏后这些虚假激活被显著抑制。Figure 4c通过PCA揭示，噪声图像的特征中存在稳定的低维位置子空间，验证了“噪声图像可有效估计位置偏差”这一核心假设。

### 聚类与聚合的消融分析

Table 3系统消融了INSID3的两个核心设计：

- **无聚类基线**（直接使用相似度阈值0.55生成掩码）：COCO-20i仅44.2% mIoU，PASCAL-Part仅35.4%。
- **无自相似性聚合**（仅使用跨图像相似度）：COCO-20i降至52.1%，PASCAL-Part降至45.8%。
- **完整INSID3**：COCO-20i 57.6%，PASCAL-Part 50.5%。

凝聚聚类将目标图像分解为语义一致的区域簇（Figure 2），为后续种子选择和聚合提供了结构化表示。自相似性聚合通过乘性得分$S_k = s_k^{\mathrm{cross}} \cdot s_k^{\mathrm{intra}}$结合语义对齐和结构一致性，有效抑制了仅靠跨图像相似度产生的碎片化误检。两个模块的叠加带来COCO-20i上+13.4、PASCAL-Part上+15.1个百分点的绝对增益。

### 骨干网络与去偏策略

**骨干替换。** 将DINOv3替换为DINOv2、Franca等自监督特征后，COCO-20i mIoU从57.6%骤降至45.1%（DINOv2）和更低水平（Table 8），证明DINOv3的稠密表征对上下文分割至关重要——其更强的空间结构和语义粒度是方法有效性的前提。

**去偏策略对比。** Table 5比较了三种训练自由去偏策略：SVD去偏（57.6%）、数据增强去偏（56.5%，需多次前向传播）、无去偏（52.1%）。SVD去偏不仅性能最优，且计算开销可忽略——投影矩阵离线预计算并存储，推理时仅需单次矩阵乘法。

### 多示例扩展与鲁棒性

INSID3可自然扩展到多示例上下文，无需任何超参数调整。在5-shot设置下（Table 7），平均mIoU从55.1%提升至59.9%，比GF-SAM的5-shot结果高+6.1个百分点。这表明聚类-选择-聚合框架能有效融合多个参考示例的信息。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/016_Table_7.jpg]]
*Table 7: Comparison of INSID3 (mIoU in %, ↑) on 5-shot semantic and part segmentation. Models are provided with 5 contextual examples and tasked with segmenting the annotated concept in the target image. INSID3 scales effectively to multiple references, achieving robust performance across domains. All hyperparameters are reused from the 1-shot setting without any tuning, highlighting the versatility of our approach. Gray indicates the model was trained on the corresponding train split of the dataset; best results bold*

**目标不存在时的行为。** Table 10显示，当目标图像不含参考概念时，INSID3能在78.5%的情况下正确输出空掩码，而GF-SAM等依赖SAM的方法总是返回非空掩码（0%正确率）。这一能力源于反向最近邻机制——当目标图像中没有patch与参考区域匹配时，候选集为空，自然产生空输出。

### 推理效率

Table 11-13报告了推理时间分析。INSID3单次上下文推理总耗时约180ms（RTX 4090），其中特征提取占主导（DINOv3前向约120ms），聚类、种子选择和聚合合计约60ms。相比GF-SAM（需DINOv3+SAM双模型前向），INSID3在推理速度和参数效率上均具优势。

### 定性分析

Figure 5展示了INSID3与GF-SAM、SegIC的定性对比。SegIC在训练域内表现良好，但在跨域和部件粒度上泛化能力有限；GF-SAM依赖SAM的强掩码先验，掩码质量高，但其“对应-分割”解耦机制常导致过分割或欠分割。INSID3仅凭自监督特征即实现了精确定位和竞争性的掩码质量，在医学、遥感、海洋等域外场景上优势尤为突出。

### 失败模式与局限性

尽管整体性能优异，INSID3存在以下已知局限：

1. **单概念限制**：当前设计一次只能处理一个目标概念，无法在单次推理中同时分割多个类别。
2. **提示形式受限**：仅支持完整掩码作为参考提示，不支持点、框等更轻量的交互模式。
3. **缺乏实例级推理**：输出为语义掩码，不区分同一类别的不同实例，多个同类物体会被合并为单一区域。
4. **位置信息的双重性**：去偏虽抑制了有害的位置偏差，但绝对的定位信息在某些任务中可能有益，该权衡尚未深入探索。

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/005_Table_1.jpg]]
*Table 1: Comparison of INSID3 (mIoU in %, ↑) on one-shot semantic, part, and personalized segmentation. State-of-the-art methods are grouped into task-specific fine-tuning and training-free approaches. Previous training-free methods rely on SAM, pre-trained with mask-level supervision, whereas INSID3 uses only frozen self-supervised DINOv3 features. Gray indicates the model was trained on the corresponding train split of the dataset; best results bold, 2nd best underlined. † denotes a GF-SAM variant using DINOv3 features*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/007_Table_2.jpg]]
*Table 2: Semantic correspondence on SPair-71k (PCK@T in %, ↑). Comparison across DINOv3 backbones, w/ and w/o debiasing*

![[assets/figures/papers/paper_list_l28_https_arxiv_org_abs_2603_28480/figures/006_Figure_5.jpg]]
*Figure 5: Comparison of INSID3 with GF-SAM [69] and SegIC [41] on one-shot semantic (left), part (top right), and personalized (bottom right) segmentation. SegIC performs well in-domain but struggles to generalize across domains and part granularity, reflecting its limited flexibility beyond the training distribution. GF-SAM, relying on the strong segmentation priors of SAM [33], produces highquality masks; however, the decoupled mechanism between correspondence and segmentation often leads to over- or under-segmentation. INSID3, despite relying solely on self-supervised features, achieves precise localization and competitive mask quality*

## 定位与知识库关联

### 1. 与基线方法的对比关系

INSID3 在上下文分割（In-Context Segmentation, ICS）领域占据一个独特位置：它是目前唯一完全无监督、无训练、且仅依赖单一自监督骨干的方法。与之形成对比的基线可分为两类：

**训练自由方法（依赖SAM掩码先验）**：**PerSAM**、**Matcher**（DINOv2 + SAM）、**GF-SAM**（DINOv2/DINOv3 + SAM）均采用多模型组合策略，将语义对应与掩码生成解耦——通常用DINO系列特征建立跨图像对应，再借助SAM的预训练掩码解码器生成分割结果。这一范式的核心缺陷在于：(1) 参数规模庞大（GF-SAM约945M，而INSID3仅304M）；(2) 对应与分割之间的信息瓶颈导致过分割或欠分割（见Figure 5定性对比）；(3) SAM的掩码先验在医学影像、遥感等域外数据上泛化能力有限。INSID3通过证明“分割可直接从自监督稠密特征中涌现”，从根本上消除了对SAM的依赖。

**微调方法（依赖任务特定训练）**：**SegIC**（基于DINOv2 + 训练解码器）、**DiffewS**（基于Stable Diffusion）、**SegGPT**（通用视觉任务微调）在域内表现强劲，但泛化能力受限于训练分布。Figure 1的泛化对比清晰展示了这一现象：微调方法在训练域内表现优异，但在跨域、跨粒度场景下性能急剧下降。INSID3以无训练的姿态在多数基准上超越这些方法，尤其在域外数据集（Chest X-Ray上领先GF-SAM +27.8 mIoU）上优势显著。

**与SAM3的对比**（Table 9）：即便是最新的SAM3，在视频式掩码传播或图像拼接提示两种适配方式下，其COCO-20i上的mIoU仍不及INSID3，进一步验证了“纯自监督特征+无训练推理”这一技术路线的竞争力。

### 2. 关键技术谱系

INSID3的方法设计可追溯至三条技术脉络的交汇：

- **自监督稠密表征**：DINOv3是该工作的核心使能技术。消融实验（Table 8）表明，将骨干替换为DINOv2或Franca等自监督特征后，COCO-20i mIoU从57.6%骤降至45.1%，证明DINOv3的稠密特征具备独特的空间结构与语义粒度，是ICS任务的关键瓶颈突破点。

- **位置偏差的发现与去偏**：DINO系列特征中的位置偏差并非新现象，但INSID3首次系统揭示了DINOv3中存在比DINOv2强得多的位置偏差（Table 4：去偏在DINOv3-L上带来+5.0 PCK增益，而DINOv2仅+0.3），并提出了一种极简的去偏策略——通过单张噪声图像的SVD估计位置子空间并投影去除。该方法计算开销可忽略（仅需一次矩阵乘法），且优于需要多次前向的数据增强去偏策略（Table 5：57.6% vs 56.5%）。

- **无训练分割机制**：INSID3的聚类-种子选择-聚合三阶段流程（Figure 3）借鉴了经典的无监督分割思想，但创新性地将其构建在去偏后的跨图像语义对应之上。消融实验（Table 3）表明，移除凝聚聚类和自相似性聚合后，COCO-20i mIoU从57.6%降至44.2%，PASCAL-Part从50.5%降至35.4%，验证了这两个模块的关键作用。

### 3. 适用边界

INSID3的优势场景与局限同样明确：

**优势场景**：
- 跨域泛化：医学影像（Chest X-Ray 78.8%）、遥感（ISIC 54.4%）、细粒度部件（PASCAL-Part 50.5%）等域外数据上表现突出
- 多粒度分割：从完整物体到部件级、个性化概念，无需调整任何超参数（Table 6：仅3个固定超参数）
- 多示例扩展：自然支持最多5-shot上下文，平均mIoU提升至59.9%（Table 7），无需额外设计

**已知局限**：
- 单概念限制：一次推理仅能处理一个目标概念，无法同时区分和分割多个类别
- 提示形式受限：需要完整的目标掩码作为参考，暂不支持点、框等轻量交互
- 无实例级推理：同一语义类别的不同实例会被合并为单一区域
- 表征能力上限：分割质量受限于DINOv3的固有表征能力；位置偏差的绝对去除可能对某些需要空间定位的任务产生负面影响，该权衡尚未被深入探索

### 4. 开放问题与后续方向

INSID3开辟了若干值得深入的方向：

1. **多概念并行分割**：当前流程需对每个概念重复完整推理，能否通过共享聚类结果、并行种子选择实现多概念单次推理？

2. **轻量提示嵌入**：如何将点、框等提示形式融入无训练框架，同时保留“仅需自监督特征”的核心优势？

3. **实例级扩展**：能否利用簇间亲和性进行迭代播种与膨胀，在训练自由前提下实现实例分割？

4. **位置偏差的跨任务影响**：DINOv3中的位置偏差是否同样影响目标检测、深度估计等任务？所提出的SVD去偏方法能否作为通用模块提升这些任务的性能？

5. **自适应去偏秩**：去偏投影的秩 $s$ 目前固定为500，是否存在基于图像内容自适应调整的策略，以优化语义对应与空间定位的平衡？

**注意**：本文引用的基线方法（PerSAM、Matcher、GF-SAM、SegIC、DiffewS、SegGPT）的具体作者、会议和年份信息在提供的分析材料中未完整给出，建议读者根据论文原文的参考文献列表进行核实。

## 原文 PDF

![[paperPDFs/CVPR_2026/INSID3_Training_Free_In_Context_Segmentation_with_DINOv3.pdf]]
