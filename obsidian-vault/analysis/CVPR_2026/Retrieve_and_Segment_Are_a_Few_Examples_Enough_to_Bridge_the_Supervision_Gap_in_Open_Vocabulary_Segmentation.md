---
title: "Retrieve and Segment: Are a Few Examples Enough to Bridge the Supervision Gap in Open-Vocabulary Segmentation?"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Retrieve_and_Segment_Are_a_Few_Examples_Enough_to_Bridge_the_Supervision_Gap_in_Open_Vocabulary_Segmentation.pdf
project_link: null
code_link: null
aliases:
- RSR
- RSAFEEBSGOVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 视觉支持示例（pixel-annotated images）的可用数量与质量，以及多模态特征融合策略（检索机制、混合系数 Λ、类别相关性权重、损失加权）的设计。
primary_logic: 通过检索与测试图像最相关的视觉支持特征，并与文本类别原型进行可学习的融合（使用多个混合系数 λ），训练一个轻量的测试时线性分类器，可在仅少量像素标注示例的情况下大幅提升开放词汇分割性能，并自然处理部分支持缺失场景（缺失视觉或文本），保持开放词汇泛化能力。
claims:
- RNS在仅有每个类别一张支持图像时，相对于零样本基线显著提升：OpenCLIP上+7.3%，DINOv3上+18.4% mIoU。
- 在六个OVS基准上的平均mIoU（DINOv3.txt + SAM），RNS B=20达到61.9，将零样本与全监督之间的差距缩小至11.5，且超过了基于大规模训练的CAT-Seg（47.8）14.1个点。
- 去除类别相关性权重（w_c）导致各支持量级性能一致下降（B=10时-0.48 mIoU），证实其可抑制不相关检索类别的作用。
- 将检索到的视觉支持特征替换为随机子集会导致性能大幅下降，验证了基于相似度检索的关键性。
---

# Retrieve and Segment: Are a Few Examples Enough to Bridge the Supervision Gap in Open-Vocabulary Segmentation?

> [!tip] 核心洞察
> 通过检索与测试图像最相关的视觉支持特征，并与文本类别原型进行可学习的融合（使用多个混合系数 λ），训练一个轻量的测试时线性分类器，可在仅少量像素标注示例的情况下大幅提升开放词汇分割性能，并自然处理部分支持缺失场景（缺失视觉或文本），保持开放词汇泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 检索与分割：少量示例能否弥合开放词汇分割中的监督差距？ |
| 英文题名 | Retrieve and Segment: Are a Few Examples Enough to Bridge the Supervision Gap in Open-Vocabulary Segmentation? |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.23339) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Retrieve and Segment (RNS) |
| Dataset | 6 OVS benchmarks average, 同上（OpenCLIP ViT-B/16 + SAM 2.1）, 同上（DINOv3.txt + SAM）, PASCAL VOC |

> [!tip] 效果简介
> - 6 OVS benchmarks average (VOC, Context, Object, Stuff, City, ADE) 上，mIoU 61.9 (RNS B=20, DINOv3.txt ViT-L/16 + SAM 2.1) vs 27.9 (DINOv3.txt + SAM zero-shot) (+34.0)。
> - 同上（OpenCLIP ViT-B/16 + SAM 2.1） 上，mIoU 51.6 (RNS B=20) vs 31.7 (zero-shot) (+19.9)。
> - 同上（DINOv3.txt + SAM） 上，mIoU 61.9 (RNS B=20) vs 47.8 (CAT-Seg, trained on COCO 118k annotations) (+14.1)。

## 概要

开放词汇分割（Open-Vocabulary Segmentation, OVS）旨在将图像划分为具有任意语义类别的区域，其核心挑战在于视觉-语言模型（VLMs）的图像级粗粒度监督与像素级细粒度预测之间的监督差距。纯文本驱动的零样本方法受限于自然语言类别描述的语义模糊性，难以精确区分外观相似但语义不同的类别（如将树枝误判为鸟，或将沙发与椅子混淆）。

本文提出 **Retrieve and Segment (RNS)**，一种检索增强的测试时适配方法。其核心洞察是：通过检索与测试图像最相关的少量像素标注支持特征，并与文本类别原型进行可学习的多模态融合，训练一个轻量的测试时线性分类器，即可在仅需极少标注示例的情况下大幅弥合监督差距。RNS 天然支持支持集的动态扩展，并能优雅处理部分模态缺失（缺失视觉或文本支持）的场景，保持开放词汇的泛化能力。

在六个主流 OVS 基准上的实验表明，RNS 在每类仅有一张支持图像时，即可相对于零样本基线实现显著提升（OpenCLIP 上 +7.3%，DINOv3 上 +18.4% mIoU）。当每类支持图像增至 20 张时，RNS（DINOv3.txt + SAM）达到 61.9 的平均 mIoU，将零样本与全监督之间的差距缩小至 11.5，并超过基于大规模训练的 CAT-Seg（47.8）达 14.1 个百分点。

### 开放词汇分割的核心瓶颈

开放词汇分割（Open-Vocabulary Segmentation, OVS）要求模型在推理时能够分割任意类别，而不仅限于训练时见过的封闭词汇集。当前主流方案依赖视觉-语言模型（VLMs）的零样本能力，但其性能受制于两重根本性挑战：

**监督粒度不匹配。** VLM的训练使用图像级粗粒度监督（如对比语言-图像预训练），而分割任务需要像素级细粒度预测。这种粒度鸿沟导致VLM的patch特征虽然保留了丰富的语义信息，却缺乏精确的对象边界感知，直接用于分割时产生大量模糊和错误分类。

**语义模糊性。** 自然语言类别描述具有固有的歧义性。仅凭文本类别名（如“bird”）进行像素级定位时，模型容易将外观相似的物体（如树枝）误判为目标类别，或在不同类别间产生混淆（如“sofa”与“chair”）。Figure 1和Figure 8的定性对比清晰地展示了这一现象：纯文本支持的零样本分割在背景区域产生大量幻觉，而纯视觉支持虽能缓解部分歧义，但面对上下文相似的物体时仍会出错。

### 现有方法的局限

现有的OVS方法在处理上述瓶颈时存在明显不足：

- **零样本方法**完全依赖文本类别原型，无法利用任何像素标注信息，性能受限于VLM的固有偏差。
- **kNN-CLIP**等检索增强方法虽然引入了视觉支持特征，但采用手工设计的固定融合策略（如固定权重组合文本和视觉相似度），无法自适应地平衡两种模态在不同测试场景下的贡献。
- **FREEDA**等方法使用生成或真实支持特征，但依赖固定的融合系数β，缺乏对每个查询进行针对性融合的能力。
- **离线训练方法**（如在全部支持图像上微调视觉编码器和线性分类器）虽然性能较强，但丧失了开放词汇能力——它们只能分割支持集中出现的类别，无法泛化到新类别。

更重要的是，现有方法普遍**未系统处理部分支持缺失场景**：当某些类别缺少视觉支持示例或文本类别名时，kNN-CLIP等方法的性能会急剧下降，甚至低于纯文本零样本基线。这严重限制了OVS方法在真实世界中动态、不完整支持条件下的实用性。

### 本文动机与核心思路

上述分析揭示了一个关键洞察：**少量像素标注示例中蕴含的细粒度视觉信息，如果能够以合理的方式与文本语义融合，就有可能在保留开放词汇泛化能力的同时，大幅弥合零样本与全监督分割之间的性能鸿沟。**

基于此，本文提出**Retrieve and Segment (RNS)**——一种检索增强的测试时适配方法。RNS的核心设计原则是：

1. **检索驱动**：对每张测试图像，从视觉支持集中检索最相关的支持特征，而非使用全量支持集，从而聚焦于与当前场景相关的类别信息。
2. **可学习融合**：使用多个混合系数λ将文本类别原型与检索到的视觉支持特征进行线性融合，生成融合类别特征，并在测试时训练一个轻量线性分类器——不修改VLM编码器，保持开放词汇能力。
3. **统一处理部分支持**：通过伪标签机制补偿缺失视觉支持的类别，通过平均文本特征替代缺失文本支持的类别，使得RNS在完全支持、部分视觉支持、部分文本支持等多种设置下均能有效运作。

RNS的关键优势在于：它并非简单地进行后期融合或离线微调，而是将检索、融合和测试时训练统一为一个整体目标，使得模型能够在仅有**每类别一张支持图像**的条件下，相对于零样本基线实现显著提升（OpenCLIP上+7.3%，DINOv3上+18.4% mIoU），并在B=20时将零样本与全监督之间的差距缩小至11.5 mIoU，超越了基于大规模训练的CAT-Seg（47.8）达14.1个点（Table 2）。

## 核心方法与创新机理

RNS 的核心创新在于将**检索增强的测试时适配**引入开放词汇分割，通过三个相互耦合的机制设计，系统性地弥合了零样本预测与像素级监督之间的鸿沟。

### 1. 检索驱动的支持特征筛选

与以往方法使用全部支持特征或手工设计的固定融合权重不同，RNS 引入了基于内容的检索机制来动态构建测试时支持集。对于每张测试图像的每个 patch 特征 $\mathbf{x}_j^q$，从视觉支持集 $\mathcal{V}$ 中检索 $k$ 个最近邻，构成检索视觉支持集 $\mathcal{V}_r$：

$$\mathcal{V}_r := \bigcup_{j=1}^{n} \mathrm{kNN}(\mathcal{V}, \mathbf{x}_j^q)$$

这一设计的因果逻辑在于：开放词汇场景下类别空间庞大，直接使用所有支持特征会引入大量与当前测试图像无关的类别噪声。通过检索，RNS 将支持集聚焦于与测试图像语义相关的子集，为后续的测试时训练提供了高质量、低噪声的监督信号。消融实验证实了这一设计的关键性：将检索得到的 $\mathcal{V}_r$ 替换为随机子集会导致性能大幅下降，而使用最远邻替代最近邻则表现最差（Figure 5），说明检索相似度与分割质量之间存在直接的因果关联。

### 2. 可学习的多模态融合与测试时训练

RNS 将多模态融合从手工设计的后期组合（如 kNN-CLIP 的固定权重、FREEDA 的固定系数 $\beta$）升级为**可学习的、每查询自适应**的融合策略。具体而言，对每个类别 $c$ 和混合系数 $\lambda \in \Lambda$，生成融合类别特征：

$$\mathbf{f}_{c\lambda} = \lambda \mathbf{t}_c + (1-\lambda) \mathbf{v}_c$$

其中 $\Lambda = \{0.9, 0.8, 0.6, 0.4, 0.2, 0.0\}$ 包含多个混合系数，覆盖从文本主导到视觉主导的全谱融合模式。这些融合特征与检索到的视觉支持特征 $\mathcal{V}_r$ 一起，用于在每张测试图像上训练一个轻量线性分类器 $g_\theta$，通过两个加权交叉熵损失项进行优化：

$$L_v = \sum_{\mathbf{v} \in \mathcal{V}_r} w_{l(\mathbf{v})} \mathrm{CE}(g_\theta(\mathbf{v}), \mathbf{1}_{l(\mathbf{v})})$$

$$L_f = \sum_{c \in \mathcal{C}_r} w_c \sum_{\lambda \in \Lambda} \mathrm{CE}(g_\theta(\mathbf{f}_{c\lambda}), \mathbf{1}_c)$$

其中 $w_c$ 为类别相关性权重，通过测试图像全局平均特征与文本类别特征的相似度计算，用于抑制检索到的但不相关的类别。消融实验表明，使用单一融合系数 $\lambda=0.8$ 替代多 $\lambda$ 集合在低资源场景下（$B=1$）导致 5.19 mIoU 的显著下降（Table 1），验证了多融合模式对稀疏支持场景的关键作用。

### 3. 部分支持缺失的优雅退化机制

现实场景中，视觉支持和文本支持往往不完整——某些类别可能缺乏像素标注图像，或缺乏文本类别名称。RNS 针对这两种部分支持缺失场景设计了精巧的补偿机制，使其能够**自然退化而非崩溃**：

- **部分视觉支持缺失**：当某类别 $c$ 缺少视觉支持但被预测为出现在测试图像中时，RNS 利用零样本预测的伪标签 $\tilde{P}_{jc}^q$ 池化测试图像 patch 特征，构造伪视觉原型 $\mathbf{v}_c = \sum_{j=1}^{n} \tilde{P}_{jc}^q \mathbf{x}_j^q$，并通过伪标签 KL 损失 $L_p$ 维持分类器对该类别的判别能力。消融实验证实，去除 $L_p$ 在部分视觉支持设置下导致性能急剧下降（Figure 4 左），验证了该机制对维持未支持类别性能的必要性。

- **部分文本支持缺失**：缺失的文本类别特征用可用类别的平均文本特征替代，提供中性的语义先验；当所有类别均缺失文本支持时，RNS 平滑退化为纯视觉基线（$\Lambda = \{0\}$，$w_c = 1$），避免了性能断崖式下跌。

这种“优雅退化”的设计哲学使 RNS 在从零样本到全监督的整个支持谱系上都能稳定工作，是其区别于以往方法的核心架构优势。

RNS 的整体 pipeline 围绕一个核心思想展开：**将检索增强的测试时适配器引入开放词汇分割**，通过可学习的多模态融合，在少量像素标注支持图像的条件下弥合粗粒度视觉-语言模型（VLM）与细粒度像素预测之间的监督鸿沟。其流程可概括为四个阶段：支持特征提取 → 多模态融合 → 基于相似度的检索 → 测试时线性分类器训练与推理，并可选择性地接入区域提议模块以生成掩膜级分割结果。

### 输入与输出

**输入**包含三个层次的信息：
1. **视觉支持集**：一组像素级标注的支持图像，每张图像提供了某些类别的 patch 级标签。支持集可动态扩展，且允许部分类别缺失视觉示例。
2. **文本支持集**：所有目标类别的文本名称或描述，同样允许部分缺失。
3. **测试图像**：无标注的目标图像，需要为其每个像素（或区域）预测类别标签。

**输出**为测试图像的逐像素/逐区域类别预测，以及可选的类别掩膜。

### 模块关系与数据流

下图（Figure 2）给出了完整文本和视觉支持下的 RNS 流程概览：

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RNS when full textual and visual support is available. Having access to a set of pixel-level annotated images, per-image visual class features*

**Figure 2**：完整文本和视觉支持下的 RNS 概览。利用像素级标注的支持图像，首先提取每图视觉类别特征，与文本类别特征进行多 λ 融合生成融合支持集；对测试图像的每个 patch，从视觉支持集中检索 k 近邻构成相关视觉支持集，并据此确定相关类别集；最后在检索到的视觉特征和融合特征上训练一个轻量线性分类器，完成对测试图像的预测。

各模块的功能与衔接关系如下：

#### 1. 支持特征提取（Support Feature Extraction）

该模块负责将原始支持图像和类别文本转化为结构化的特征表示，是整个 pipeline 的基础。

- **视觉类别特征**：对于每张支持图像 $i$，利用下采样并 L1 归一化的 patch 标签 $P_{jc}^i$ 对 patch 特征 $\mathbf{x}_j^i$ 进行加权平均，得到每图类别视觉原型：
  $$\mathbf{v}_c^i = \sum_{j=1}^{n} P_{jc}^i \mathbf{x}_j^i$$
  所有支持图像的这些特征取并集，构成总视觉支持集 $\mathcal{V}$。对于同一类别出现在多张支持图像中的情况，将其视觉特征累加得到该类的聚合视觉原型 $\mathbf{v}_c$。

- **文本类别特征**：从类名通过 VLM 文本编码器提取文本原型 $\mathbf{t}_c$。

这一模块的输出是结构化的视觉支持集 $\mathcal{V}$ 和文本类别特征，为后续融合与检索提供原材料。支持集设计为动态可扩展，新增标注图像时仅需计算新特征并追加到 $\mathcal{V}$ 中，无需重新训练。

#### 2. 多模态融合（Modality Fusion）

该模块解决的核心问题是：**文本语义先验与视觉像素证据如何有效结合**。RNS 采用可学习的、每个查询进行融合的策略，而非手工设计的固定权重。

具体而言，使用一组混合系数 $\Lambda = \{0.9, 0.8, 0.6, 0.4, 0.2, 0.0\}$，对每个类别 $c$ 和每个 $\lambda \in \Lambda$ 生成融合类别特征：
$$\mathbf{f}_{c\lambda} = \lambda \mathbf{t}_c + (1-\lambda) \mathbf{v}_c$$

当 $\lambda=1$ 时，特征退化为纯文本原型；当 $\lambda=0$ 时，退化为纯视觉原型。多 λ 设计的关键优势在于：不同支持图像数量下，文本与视觉信息的最优混合比例不同——在极度稀疏支持时文本先验更为关键，而随着视觉支持增加，视觉证据的权重应逐步提升。通过同时保留多个 λ 并在训练中让分类器自行适应，RNS 避免了手动调参的脆弱性。

#### 3. 检索（Retrieval）

检索模块是 RNS 实现**内容感知适配**的关键机制。其基本逻辑是：并非所有支持特征都与当前测试图像相关，使用不相关的支持特征反而会引入噪声。

对于测试图像的每个 patch 特征 $\mathbf{x}_j^q$，从视觉支持集 $\mathcal{V}$ 中检索 $k$ 个最近邻（默认 $k=4$），取所有 patch 检索结果的并集构成**检索视觉支持集** $\mathcal{V}_r$：
$$\mathcal{V}_r := \bigcup_{j=1}^{n} \mathrm{kNN}(\mathcal{V}, \mathbf{x}_j^q)$$

基于 $\mathcal{V}_r$ 中出现的类别，确定**相关类别集** $\mathcal{C}_r$，后续训练仅针对这些类别进行。同时，通过测试图像全局平均特征与文本类别特征的相似度计算**类别相关性权重** $w_c$，用于在损失函数中抑制不相关检索类别的影响：
$$w_c = s_c\left((\mathbf{x}^q)^\top \mathbf{t}_c\right), \quad \mathbf{x}^q = \frac{1}{n} \sum_{j=1}^{n} \mathbf{x}_j^q$$

检索机制使 RNS 能够为每张测试图像动态选择最相关的支持信息，而非盲目使用全量支持集。

#### 4. 测试时线性分类器训练（Test-Time Linear Classifier Training）

这是 RNS 的核心适配步骤。对于每张测试图像，利用检索到的支持特征训练一个轻量线性分类器 $g_\theta$，训练完成后直接用于该图像的像素/区域预测。训练涉及多个损失项：

- **视觉支持损失** $L_v$：在 $\mathcal{V}_r$ 中的视觉特征上计算加权交叉熵，促使分类器正确识别检索到的支持特征所属类别。
- **融合支持损失** $L_f$：在相关类别的融合特征 $\mathbf{f}_{c\lambda}$（所有 $\lambda$）上计算加权交叉熵，将文本语义信息注入分类器。
- **伪标签损失** $L_p$（可选）：当部分类别缺失视觉支持时，利用测试图像的零样本预测构造伪视觉特征，并通过 KL 散度损失防止分类器遗忘未观察类别。

训练仅更新分类器参数，不修改视觉编码器，因此计算开销可控且保持了 VLM 的开放词汇泛化能力。

#### 5. 区域提议池化（Region-proposal Pooling，可选）

当提供 SAM 等区域提议时，RNS 可将 patch 级特征池化到区域级，以区域为单位训练分类器并生成掩膜：
$$\mathbf{x}_r^q = \sum_{j=1}^{n} \bar{S}_{jr} \mathbf{x}_j^q, \quad r = 1, \ldots, R$$
其中 $\bar{S}_{jr}$ 为下采样并 L1 归一化的区域掩膜。这使得 RNS 既能输出 patch 级预测，也能生成语义连贯的掩膜级分割结果。

### 部分支持缺失的优雅处理

RNS 的一个显著优势是对部分支持缺失场景的自然处理能力，这在真实应用中极为常见：

- **部分视觉支持缺失**：当某些类别缺少视觉示例时，利用零样本预测生成伪标签池化 patch 特征，构造伪视觉原型，并通过伪标签 KL 损失进行补偿。
- **部分文本支持缺失**：用可用类别的平均文本特征替代缺失的文本特征，提供中性语义先验；当所有文本支持均缺失时，设置 $\Lambda = \{0\}$ 且 $w_c = 1$，方法平滑退化为纯视觉基线。

这种设计使 RNS 在支持信息不完整时仍能保持稳健性能，避免了传统方法在类似场景下的灾难性退化。

RNS 的核心工作流由五个模块串联构成：支持特征提取、多模态融合、检索、测试时线性分类器训练，以及可选的区域提议池化。以下按模块逐一展开关键公式与变量含义。

### 支持特征提取

给定一组像素级标注的支持图像，RNS 首先为每张图像提取**每图视觉类别特征**（per-image visual class feature）。对于支持图像 $i$ 中的类别 $c$，其视觉原型通过该图像内所有 patch 特征的加权平均得到：

$$
\mathbf{v}_c^i = \sum_{j=1}^{n} P_{jc}^i \mathbf{x}_j^i \tag{2}
$$

其中 $\mathbf{x}_j^i$ 是 VLM 编码器输出的 patch $j$ 的特征向量，$P_{jc}^i$ 是经下采样并 L1 归一化后的像素级标注在 patch $j$ 上属于类别 $c$ 的权重。所有支持图像的所有类别视觉特征构成**视觉支持集** $\mathcal{V}$：

$$
\mathcal{V} = \bigcup_{i=1}^{M} \{\mathbf{v}_c^i : c \in \mathcal{C}_i\} \tag{3}
$$

该集合是动态可扩展的：新增支持图像时只需追加新的 $\mathbf{v}_c^i$，无需重新处理历史数据。

同时，对于每个类别 $c$，从类名提取**文本类别特征** $\mathbf{t}_c$，构成文本支持集。当某类别在多张支持图像中出现时，其**聚合视觉类别特征**为各图像视觉原型的累加：

$$
\mathbf{v}_c = \sum_{i \in \mathcal{T}_c} \mathbf{v}_c^i \tag{5}
$$

其中 $\mathcal{T}_c$ 为包含类别 $c$ 的所有支持图像索引集合。

### 多模态融合

RNS 的核心创新之一是对文本原型与视觉原型进行**可学习的、每个查询自适应的融合**。对于类别 $c$，使用混合系数 $\lambda \in \Lambda$ 将文本特征 $\mathbf{t}_c$ 与聚合视觉特征 $\mathbf{v}_c$ 线性组合，生成**融合类别特征**：

$$
\mathbf{f}_{c\lambda} = \lambda \mathbf{t}_c + (1-\lambda) \mathbf{v}_c \tag{4}
$$

其中 $\Lambda$ 是一组预设的混合系数（论文固定为 $\Lambda = \{0.9, 0.8, 0.6, 0.4, 0.2, 0.0\}$）。当 $\lambda=1$ 时 $\mathbf{f}_{c\lambda}$ 退化为纯文本特征，$\lambda=0$ 时退化为纯视觉特征，中间值实现两种模态的连续插值。多 $\lambda$ 集合使分类器在训练时同时接触到不同模态配比的类别原型，消融实验证实单一 $\lambda=0.8$ 在低资源下会导致严重性能退化（B=1 时 -5.19 mIoU，Table 1）。

### 检索

对于每张测试图像，RNS 并不使用全部视觉支持特征，而是基于内容相似度进行**选择性检索**。具体地，对测试图像的每个 patch 特征 $\mathbf{x}_j^q$，从视觉支持集 $\mathcal{V}$ 中检索 $k$ 个最近邻（余弦相似度），取所有 patch 检索结果的并集构成**检索视觉支持集**：

$$
\mathcal{V}_r := \bigcup_{j=1}^{n} \mathrm{kNN}(\mathcal{V}, \mathbf{x}_j^q) \tag{6}
$$

$\mathcal{V}_r$ 中出现的所有类别构成**相关类别集** $\mathcal{C}_r$，后续训练仅在这些类别上进行，大幅降低了计算开销并抑制不相关类别的干扰。

检索的关键性由消融实验强力支撑：将 $\mathcal{V}_r$ 替换为随机子集会导致性能大幅下降（Figure 5），而使用最远邻则表现最差，证实了基于相似度检索的必要性。此外，$k$ 的取值在 $K=4$ 至 $K=16$ 范围内性能相近（Table 5），方法对 $K>1$ 的精确取值不敏感。

### 测试时线性分类器训练

这是 RNS 的核心计算环节。对于每张测试图像，利用检索到的支持特征训练一个轻量线性分类器 $g_\theta$（单层线性映射，输出维度为 $|\mathcal{C}_r|$），训练完成后直接预测该图像的 patch 或区域类别。训练由两个主要损失项驱动。

**视觉支持损失** $L_v$ 在检索到的视觉支持特征上计算加权交叉熵：

$$
L_v = \sum_{\mathbf{v} \in \mathcal{V}_r} w_{l(\mathbf{v})} \mathrm{CE}(g_\theta(\mathbf{v}), \mathbf{1}_{l(\mathbf{v})}) \tag{7}
$$

其中 $l(\mathbf{v})$ 是视觉特征 $\mathbf{v}$ 对应的类别标签，$w_c$ 是**类别相关性权重**，定义为测试图像全局平均特征与文本类别特征的 softmax 相似度：

$$
w_c = s_c\left((\mathbf{x}^q)^\top \mathbf{t}_c\right), \quad \mathbf{x}^q = \frac{1}{n} \sum_{j=1}^{n} \mathbf{x}_j^q \tag{8,9}
$$

$w_c$ 的作用是抑制检索到但与测试图像内容不相关的类别（例如检索到 “car” 的特征但测试图像中并无车辆）。消融实验证实移除 $w_c$ 导致 B=10 时 -0.48 mIoU 的一致性能下降（Table 1）。

**融合支持损失** $L_f$ 在相关类别的融合特征上计算加权交叉熵，将文本信息注入分类器：

$$
L_f = \sum_{c \in \mathcal{C}_r} w_c \sum_{\lambda \in \Lambda} \mathrm{CE}(g_\theta(\mathbf{f}_{c\lambda}), \mathbf{1}_c) \tag{10}
$$

总损失为 $L_v + L_f$ 的加权组合。训练仅涉及 $g_\theta$ 的参数，视觉编码器和文本编码器保持冻结，确保了开放词汇泛化能力不被破坏。

### 部分支持处理

**部分视觉支持缺失**时，对于缺少视觉原型的类别 $c \in \mathcal{C}_d \cap \mathcal{C}_q$（$\mathcal{C}_d$ 为缺失视觉支持的类别集，$\mathcal{C}_q$ 为测试图像中预测出现的类别集），利用零样本预测的伪标签构造**伪视觉特征**：

$$
\mathbf{v}_c = \sum_{j=1}^{n} \tilde{P}_{jc}^q \mathbf{x}_j^q \tag{11}
$$

并引入**伪标签损失** $L_p$ 防止分类器遗忘这些类别：

$$
L_p = \sum_{c \in \mathcal{C}_d \cap \mathcal{C}_q} w_c \sum_{\lambda \in \Lambda} \mathrm{KL}(\hat{\mathbf{p}}_{c\lambda} \| g_\theta(\mathbf{f}_{c\lambda})) \tag{12}
$$

其中 $\hat{\mathbf{p}}_{c\lambda}$ 是融合特征 $\mathbf{f}_{c\lambda}$ 在零样本文本分类器下的预测分布，KL 散度迫使 $g_\theta$ 的输出与之保持一致。消融实验表明移除 $L_p$ 在部分视觉支持设置下导致性能急剧下降（Figure 4 左）。

**部分文本支持缺失**时，缺失的文本类别特征用可用类别的平均文本特征替代，提供中性语义先验；若所有类别均无文本支持，则设 $\Lambda = \{0\}$、$w_c = 1$，方法平滑退化为纯视觉基线（Section 3.5）。

### 区域提议池化（可选）

当提供 SAM 等区域提议时，RNS 将 patch 级特征池化到区域级，以区域为单位训练分类器并生成掩膜。对于区域 $r$，其特征为：

$$
\mathbf{x}_r^q = \sum_{j=1}^{n} \bar{S}_{jr} \mathbf{x}_j^q, \quad r = 1, \ldots, R \tag{13}
$$

其中 $\bar{S}_{jr}$ 是经下采样并 L1 归一化的区域掩膜在 patch $j$ 上的权重。后续的训练和预测过程与 patch 级完全一致，仅将操作对象从 patch 特征替换为区域特征。

## 实验与关键发现

### 核心实验设置

RNS在六个开放词汇分割（OVS）基准上系统验证：PASCAL VOC、PASCAL Context、COCO Object、COCO Stuff、Cityscapes和ADE20K。支持集采样遵循数据集真实类别分布的长尾特性。所有方法统一采用SAM 2.1生成区域提议，并固定超参数（k=4, τ=0.1, βf=1.5, βp=0.2, Λ={0.9,0.8,0.6,0.4,0.2,0.0}），未针对单个基准调整。离线基线则通过训练-验证分割仔细调参，以提供强力参考。

### 全文本与视觉支持下的主要结果

在全文本与视觉支持设置下，RNS在所有支持图像数量（B）上一致超越所有竞争者。Figure 3展示了核心性能曲线：仅需每类**一张**支持图像（B=1），RNS相对于零样本基线在OpenCLIP（ViT-B/16）上提升**+7.3%** mIoU，在DINOv3.txt（ViT-L/16）上提升**+18.4%** mIoU。随着支持图像增加，性能持续增长并逐渐饱和——这是典型的少量示例学习行为。

Table 2汇总了六个基准的平均性能。在DINOv3.txt + SAM配置下，RNS（B=20）达到**61.9** mIoU，将零样本（27.9）与全监督之间的差距从34.0缩小至仅**11.5**个点。更值得注意的是，RNS仅使用每类20张像素标注图像，即超越了基于COCO 118k标注大规模训练的**CAT-Seg**（47.8 mIoU）**14.1**个点。在OpenCLIP + SAM配置下，RNS（B=20）达到51.6 mIoU，较零样本（31.7）提升+19.9。

在单个数据集上，以PASCAL VOC为例，RNS（B=20, DINOv3.txt + SAM）达到**82.1** mIoU，较零样本（31.3）提升高达**+50.8**个点（Table 4）。这一结果逼近全监督方法（Mask2Former约86.4），而后者使用了VOC训练集的全部1464张像素标注图像。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/016_Table_4.jpg]]
*Table 4: OVS vs. fully supervised segmentation. Fully Supervised: best method picked per dataset. ∗: self-evaluated, †: from CAT-Seg. Mask2Former numbers from DINOv3 [65] paper. Domain: using annotations from each training set. Annot: the number of pixel-level annotated images that each method uses. For Domain we report the ADE annotations*

### 消融研究：关键组件的因果作用

Table 1的系统消融揭示了RNS各组件的因果贡献：

**类别相关性权重（w_c）**：移除w_c导致所有支持量级下性能一致下降——B=1时-0.39，B=5时-0.44，B=10时-0.48 mIoU。这证实w_c有效抑制了检索过程中不相关类别的干扰，且该效应随支持集增大而增强——因为更多支持图像意味着更多不相关类别被检索到。

**多λ融合策略**：将多λ集合Λ替换为单一λ=0.8在低资源场景下造成严重损害——B=1时**-5.19** mIoU。原因在于：当视觉支持极度稀疏时，不同类别对文本先验和视觉证据的依赖程度差异巨大，单一融合系数无法适应这种异质性。高资源下多λ仍略有优势，说明可学习融合机制的鲁棒性。

**文本支持的作用**：完全移除文本支持（w/o text）在B=1时导致**-7.48** mIoU的急剧下降，但随着支持图像增加差距缩小。这表明文本先验对稀疏视觉支持尤为关键——当视觉证据不足时，语言语义提供了不可或缺的类别区分能力。

**检索机制**：Figure 5展示了检索对性能的决定性影响。将检索到的视觉支持特征$\mathcal{V}_r$替换为随机子集导致性能大幅下降；使用全量类别特征（未检索）也略差；而选择最远邻则表现最差。这验证了基于相似度的检索是选择信息性支持特征的核心机制。

**kNN检索超参数K**：Table 5显示，K=1显著差于K≥4，而K=4–16性能相近。这表明聚合多个近邻有益，但方法对K>1的精确值不敏感，具有良好的超参数鲁棒性。

### 部分支持场景下的鲁棒性

Figure 4展示了RNS在两类部分支持场景下的表现：

**部分视觉支持（左）**：当部分类别缺少视觉示例时，去除伪标签损失$L_p$（式12）导致性能急剧下降。伪标签机制通过零样本预测为缺失视觉支持的类别构造伪视觉特征，并施加KL散度损失，避免了分类器对这些未观察类别的遗忘。Table 3进一步分解了可见/不可见类别的性能：RNS在保持可见类别大幅提升的同时，通过伪标签机制使不可见类别性能不低于零样本基线，实现了“不伤害”原则。

**部分文本支持（右）**：当部分类别缺少文本名称时，RNS用可用类别的平均文本特征替代缺失特征，提供中性语义先验。当完全无文本支持时，RNS平滑退化为纯视觉基线（Λ={0}, w_c=1），性能仍优于零样本。相比之下，kNN-CLIP在缺失文本支持时性能低于零样本，暴露了其脆弱的模态依赖。

### 跨骨干网络与跨域泛化

Figure 10对比了三种视觉-语言骨干（OpenCLIP ViT-B/16、DINOv3.txt ViT-L/16、SigLIP2 ViT-L/16）下的RNS性能。RNS在所有骨干上一致提升，且DINOv3.txt的增益最为显著——这得益于其更强的视觉特征表示能力，使检索到的视觉支持更具判别性。

Figure 9分析了域外/域内视觉支持的跨域泛化。在Cityscapes↔ACDC的跨域实验中，域内支持（如Cityscapes→Cityscapes）表现最佳；域外支持（如Cityscapes→ACDC）仍有改进效果，但幅度下降。这揭示了当前方法的泛化边界：视觉支持特征的有效性受支持域与测试域分布差异的限制。

### 推理效率

Figure 13展示了精度-推理时间的权衡（DINOv3.txt, patch-level, B=5, 单张A100 GPU）。RNS通过减少测试时训练的迭代次数可大幅降低推理开销，但在极低推理时间下性能会下降。这反映了测试时适配方法的固有特性：额外的优化步骤换来性能提升，但实时性不如纯前馈方法。

### 失败模式与局限性

综合实验分析，RNS的主要失败模式包括：

1. **零视觉支持退化**：完全没有视觉支持时，RNS只能退化为零样本性能，无法主动提升。这是检索增强方法的根本限制。
2. **区域提议依赖**：性能受SAM等区域提议模型质量影响，SAM可能产生过分割或欠分割，不总是符合语义粒度。
3. **域偏移敏感**：视觉支持来自测试域内时表现最佳，域外支持改进幅度下降，泛化性受分布差异限制。
4. **测试时训练开销**：每张图像需进行轻量训练，虽然可通过减少迭代次数大幅降低，但实时性仍不如纯前馈方法。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/007_Table_1.jpg]]
*Table 1: Ablations of RNS. We report average mIoU across the considered datasets for three different numbers of available support images per class (B = 1, B = 5, B = 10). Blue numbers denote difference to the number in the same column but first row*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/005_Figure_6.jpg]]
*Figure 6: Comparison in a closed vocabulary setting. We compare RNS to the offline baseline competitors. To ensure a fair comparison we tune the learning rate, batch size, and number of iterations using a train-validation split from the available support images. No mask proposals are used. We report average performance on VOC, ADE, and Stuff*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/017_Table_5.jpg]]
*Table 5: Ablations of the k-NN retrieval hyperparameter K in RNS. We report average mIoU across the considered datasets for three different numbers of available support images per class (B = 1, B = 5, B = 10). The row with K = 4 (highlighted) corresponds to the configuration used in RNS, and blue numbers denote the difference to this row in the same column*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2602_23339/figures/013_Figure_12.jpg]]
*Figure 12: Comparison to offline baseline with and w/o hyperparameter tuning. We compare RNS against the offline linear classifier trained on per image visual class features on VOC. We include the curves presented in Figure 6 that use hyperparameter tuning per B and support seed (noted as “optimal”). We report the performance of both methods on two hyperparameter configurations: hyperparameter set 1 which corresponds to an optimal set of hyperparameters of the linear classifier for B = 1, and hyperparameter set 2 which corresponds to an optimal set of hyperparameters of the linear classifier for B = 20*

## 定位与知识库关联

### 核心洞见与因果瓶颈

开放词汇分割（OVS）的核心矛盾在于：视觉-语言模型（VLM）在图像级粗粒度监督下训练，却需要输出像素级细粒度预测。这一监督粒度不匹配（supervision granularity gap）导致两个连锁瓶颈：其一，图像级对齐无法提供精确的空间定位信号；其二，自然语言类别描述具有语义模糊性——例如“bird”可能被错误定位到树枝上，而“sofa”与“chair”在外观相似时难以仅靠文本区分（Figure 8 定性证实）。

RNS的因果旋钮在于**视觉支持示例的可用数量与质量**，以及**多模态特征融合策略的设计**。其核心洞见是：通过检索与测试图像最相关的视觉支持特征，并与文本类别原型进行可学习的、每个查询的融合（使用多个混合系数 $\lambda$），训练一个轻量的测试时线性分类器，可在仅少量像素标注示例的情况下大幅提升分割性能，并自然处理部分支持缺失场景（缺失视觉或文本），保持开放词汇泛化能力。

### 方法谱系定位

RNS位于**测试时适配（test-time adaptation）** 与**检索增强生成（retrieval-augmented generation）** 的交叉地带，其设计选择与以下基线形成清晰对比：

| 方法 | 训练范式 | 支持集利用 | 多模态融合 | 部分支持处理 |
|------|----------|------------|------------|--------------|
| **零样本OVS**（纯文本） | 无训练，仅前馈相似度 | 不使用视觉支持 | 纯文本 | 不适用 |
| **kNN-CLIP** | 无训练，kNN检索+固定融合 | 使用全部支持特征 | 手工设计固定权重 | 视觉缺失时性能低于零样本 |
| **FREEDA** | 无训练，生成或真实支持特征 | 全量生成特征 | 固定 $\beta$ 系数 | 未明确处理 |
| **离线线性分类器** | 离线训练于全部支持集 | 每图类别特征 | 无融合 | 封闭集，无开放词汇能力 |
| **离线微调**（视觉编码器+分类器） | 全量支持集上微调 | 全部像素标注 | 隐式 | 封闭集参考基线 |
| **RNS**（本文） | 每张测试图像训练轻量分类器 | 基于内容的kNN检索 | 可学习、每个查询、多 $\lambda$ 融合 | 伪标签KL损失+平均文本替代 |

#### 关键差异化设计

1. **测试时训练 vs. 无训练/离线训练**：kNN-CLIP和FREEDA均依赖手工设计的融合规则，无需测试时优化。RNS引入每图训练一个线性分类器 $g_\theta$ 的范式，使模型能根据当前测试图像的检索支持特征自适应调整——这本质上是一种**实例级元学习**，而非全局参数更新。离线线性分类器和离线微调虽然也进行训练，但面向整个支持集，丧失了开放词汇泛化能力（Figure 6 证实离线方法在封闭集设置下与RNS可比，但无法处理新类别）。

2. **基于内容的检索 vs. 全量支持集**：kNN-CLIP使用所有支持特征，FREEDA使用全量生成特征。RNS通过测试图像patch特征从视觉支持集 $\mathcal{V}$ 中检索k近邻（Eq.6），构成检索视觉支持集 $\mathcal{V}_r$。消融实验（Figure 5）证实：将 $\mathcal{V}_r$ 替换为随机子集会导致性能大幅下降；使用全量类别特征（未检索）也略差；选择最远邻则表现最差。这验证了**基于相似度的检索是性能关键**。

3. **可学习多模态融合 vs. 固定融合**：kNN-CLIP使用固定权重组合文本和视觉相似度，FREEDA使用固定 $\beta$ 系数。RNS使用多个混合系数 $\lambda \in \Lambda$ 生成融合类别特征 $\mathbf{f}_{c\lambda} = \lambda \mathbf{t}_c + (1-\lambda) \mathbf{v}_c$（Eq.4），并同时在视觉支持损失 $L_v$ 和融合支持损失 $L_f$ 下训练分类器。消融（Table 1）表明：用单一 $\lambda=0.8$ 替代多 $\lambda$ 集合 $\Lambda$ 严重损害低资源性能（B=1时-5.19 mIoU），而多 $\lambda$ 在高资源下也略有优势——这说明**多粒度融合对稀疏支持尤为关键**。

4. **部分支持缺失的显式处理**：这是RNS区别于所有基线的最显著特征。当某些类别缺少视觉支持时，RNS利用零样本预测生成伪标签，池化patch特征构造伪视觉原型 $\mathbf{v}_c$（Eq.11），并引入伪标签KL损失 $L_p$（Eq.12）避免分类器遗忘未观察类别。Figure 4（左）证实：去除 $L_p$ 在部分视觉支持缺失设置下导致性能急剧下降。当文本支持缺失时，RNS用可用类别的平均文本特征替代，提供中性语义先验；完全无文本时平滑退化为纯视觉基线（$\Lambda=\{0\}, w_c=1$）。这种**优雅的退化机制**使RNS在任意模态组合下均能工作。

### 适用边界与局限

1. **视觉支持依赖**：RNS依赖预构建的视觉支持特征集 $\mathcal{V}$，在完全没有视觉支持时只能退化为零样本性能，无法主动提升。这是方法的内在边界——其增益完全来自视觉示例提供的空间定位信号。

2. **域迁移敏感**：视觉支持集来自测试域内时表现最佳；域外支持仍有效果但改进幅度下降（Figure 9 证实Cityscapes与ACDC之间的跨域泛化存在性能衰减）。这限制了RNS在支持域与测试域分布差异较大场景下的适用性。

3. **推理时间开销**：测试时训练为每张图像带来额外推理时间。Figure 13 展示了精度与推理时间的权衡——虽然可以通过减少迭代次数大幅降低开销，但实时性仍不如纯前馈方法（如kNN-CLIP、FREEDA）。

4. **区域提议依赖**：当使用SAM等区域提议时，分割质量受提议质量直接影响。SAM可能产生过分割或欠分割，不总是符合语义粒度（Figure 14 对比了patch级与mask级分割的差异）。

5. **支持集构建假设**：当前支持集采样遵循数据集真实类别分布的长尾，但未考虑主动选择最有信息样例的策略。在极度稀疏支持情况下，随机采样可能无法最大化信息增益。

### 开放问题与未来方向

1. **主动支持选择**：能否结合主动学习或人在回路，在极度稀疏支持情况下选择最有信息的样例来提升性能？当前RNS被动接受给定的支持集，未利用测试图像分布进行支持优化。

2. **纯视觉开放词汇**：在完全缺失文本支持且视觉支持有限时，如何构建合理的类别语义空间以维持开放词汇能力？当前的平均文本替代策略提供的是中性先验，而非真正的语义理解。

3. **终身学习扩展**：RNS的动态扩展能力（支持集 $\mathcal{V}$ 可随时添加新类别特征）是否可以进一步发展成终身学习系统，在不遗忘已学类别的前提下持续集成新类别？这需要解决灾难性遗忘问题。

4. **任务泛化**：该方法能否扩展到全景分割、视频目标分割等更复杂的像素级任务？当前验证限于静态图像的语义分割，时序一致性和实例区分能力尚未探索。

5. **与大规模训练方法的融合**：Table 2 显示RNS（B=20）在六个OVS基准上平均mIoU达61.9，超过基于大规模训练的CAT-Seg（47.8）14.1个点。这提示**少量高质量支持示例可能比大规模弱标注更有效**——如何将RNS的检索-适配范式与大规模预训练结合，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Retrieve_and_Segment_Are_a_Few_Examples_Enough_to_Bridge_the_Supervision_Gap_in_Open_Vocabulary_Segmentation.pdf]]
