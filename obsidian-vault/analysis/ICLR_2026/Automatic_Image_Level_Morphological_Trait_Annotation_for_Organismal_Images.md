---
title: "Automatic Image-Level Morphological Trait Annotation for Organismal Images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Automatic_Image_Level_Morphological_Trait_Annotation_for_Organismal_Images.pdf
project_link: https://osu-nlp-group.github.io/sae-trait-annotation/
code_link: null
aliases:
- SGTAPMS
- AILMTAOI
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "该流水线用DINOv2特征上的稀疏自编码器定位形态部位，并由MLLM生成图像级性状描述。"
primary_logic: "SAE筛选物种判别性空间掩码后，将带框图像和多图像上下文交给MLLM生成一致的形态标注。"
claims:
- "SAE潜在单元可在无人工定位标注下对应翅膀、触角等可解释形态区域。"
- "物种对比排序和多图像提示能减少图像特定噪声性状。"
- "生成的BIOSCAN-TRAITS数据提升人类评分和BioCLIP零样本物种分类表现。"
---

# Automatic Image-Level Morphological Trait Annotation for Organismal Images

> [!tip] 核心洞察
> 稀疏自编码器在无监督条件下从基础模型特征中分解出单语义的潜在单元，这些单元的空间激活图能精确定位有意义的形态部位；结合物种对比排序和多图像一致性约束，可自动生成高质量、可解释的性状描述，从而将大规模物种标注的图像库转化为丰富的性状数据集。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 生物图像自动图像级形态性状标注 |
| 英文题名 | Automatic Image-Level Morphological Trait Annotation for Organismal Images |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oFRbiaib5Q) · [Project](https://osu-nlp-group.github.io/sae-trait-annotation/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | SAE-guided trait annotation pipeline (MLLM + SAE) |
| Dataset | BIOSCAN-5M (昆虫图像), 人类评估（5分制）, Insects (Ullah et al., 2022) |

> [!tip] 效果简介
> - BIOSCAN-5M (昆虫图像) 上，标注规模 为 80K条性状描述 / 19K张图像，对比 N/A，变化 N/A。
> - 人类评估（5分制） 上，平均评分 (多图像) 为 3.91 (MLLM+SAE)，对比 3.15 (MLLM-only)，变化 +0.76。
> - 人类评估（5分制） 上，平均评分 (单图像) 为 3.84 (MLLM+SAE)，对比 3.00 (MLLM-only)，变化 +0.84。

## 概要

本文提出了一种自动化的图像级形态性状标注流水线，旨在解决大规模生态学研究中高质量性状数据集极度匮乏的瓶颈问题。该方法利用稀疏自编码器（Sparse Autoencoder, SAE）从预训练基础模型（DINOv2）的特征中分解出单语义、空间可定位的潜在单元，并通过物种对比排序筛选出具有物种判别力的性状相关区域，最终由多模态大语言模型（MLLM）生成可解释的形态性状描述。在BIOSCAN-5M昆虫图像数据集上，该方法使用最佳配置标注了19K张图像，获得80K条形态性状描述（平均每张图像4.2条），构建了BIOSCAN-TRAITS数据集。人类评估表明，SAE引导的MLLM（多图像设置）平均评分为3.91（5分制），显著高于仅使用MLLM的3.15。此外，在BIOSCAN-TRAITS上微调BioCLIP后，在Insects基准上的零样本物种分类准确率从34.8%提升至39.9%。

形态性状（morphological traits）是生态学和进化生物学研究的核心数据，能够预测物种与环境之间的相互作用（Díaz et al., 2016; Kennedy et al., 2020; McGill et al., 2006）。研究表明，形态性状预测生态位的准确率可达85%（Pigot et al., 2020）。然而，传统性状提取依赖领域专家的手工劳动，测量简单特征就需要数分钟/标本（Hardisty et al., 2022），而全球自然历史博物馆收藏的超过30亿标本（Nelson & Ellis, 2019）使得人工标注几乎不可行。此外，人工标注还存在观察者主观性和系统偏差问题（Heberling, 2022）。

现有自动化解方法包括：使用卷积三元组网络学习表型嵌入空间（Hoyal Cuthill et al., 2019）、深度模型分割植物标本相关区域（Ariouat et al., 2025）、以及变分自编码器学习潜在表示（Tsutsumi et al., 2023）。但这些方法要么需要大量人工标注数据，要么缺乏可解释性，难以直接生成可用的性状描述。

本文的核心洞察在于：稀疏自编码器在无监督条件下从基础模型特征中分解出单语义的潜在单元，这些单元的空间激活图能精确定位有意义的形态部位；结合物种对比排序和多图像一致性约束，可自动生成高质量、可解释的性状描述，从而将大规模物种标注的图像库转化为丰富的性状数据集。

## 核心方法与创新机理

本文的核心创新可概括为以下三点：

1. **SAE驱动的性状定位**：利用稀疏自编码器从DINOv2特征中学习单语义、空间可定位的神经元。例如，SAE神经元4852一致激活于昆虫翅膀，神经元13860响应于触角（Figure 5）。与Grad-CAM产生的弥散热图相比，SAE能够精确定位特定解剖结构（Figure 2）。

2. **物种对比排序与多图像一致性**：通过物种对比评分对SAE单元排序，筛选出对目标物种强激活但对近缘物种弱激活的判别性单元。同时，提供同一物种的多张图像（通常3张）鼓励MLLM关注跨图像一致的共享形态特征，抑制图像特定的虚假性状。

3. **端到端自动标注流水线**：该方法仅需图像及其物种标签——这种监督信息在iNaturalist（Horn et al., 2018）、TreeOfLife（Stevens et al., 2024）、Caltech-UCSD Birds-200-2011（Wah et al., 2011）等数据集中广泛可用——即可自动生成大规模、高质量的性状描述数据集。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/001_Figure_1.jpg]]
*Figure 1: Given an input specimen image, we first compute dense visual representations using an off-the-shelf backbone (e.g., DINOv2). These features are passed through a pre-trained sparse autoencoder (SAE), which identifies high-activation latent units corresponding to semantically meaningful regions (Algorithm 1). We extract the spatial masks associated with these activations and overlay them on the original image to localize trait-relevant boxes. Finally, a multimodal language model (MLLM) is prompted with the annotated image to generate fine-grained morphological trait descriptions. This results in a large-scale, automatically labeled image-level trait dataset.*

整体流水线如Figure 1所示，包含三个主要步骤：

**步骤一：特征提取与SAE编码**。输入标本图像首先通过预训练基础模型（DINOv2-base, ViT-B/14）提取密集视觉表示。这些特征随后输入预训练的稀疏自编码器，识别出高激活的潜在单元，这些单元对应语义上有意义的区域。

**步骤二：空间掩码提取与性状定位**。提取与高激活单元关联的空间掩码，将其叠加到原始图像上，定位性状相关的边界框。通过物种对比排序和频率阈值筛选，保留在物种内一致表达且具有物种判别力的性状区域。

**步骤三：MLLM性状描述生成**。将定位后的图像区域输入多模态大语言模型（Qwen2.5-VL-72B），使用轻量级提示模板生成细粒度的形态性状描述。通过提供同一物种的多张图像，鼓励模型关注跨图像一致的共享形态特征。

### 5.1 稀疏自编码器（SAE）

SAE将密集表示转换为稀疏编码，其中每个单元理想情况下对应一个可解释的潜在因子。本文使用ReLU自编码器（Bricken et al., 2023; Templeton et al., 2024），其编码器、激活函数和解码器定义如下：

**编码器**：将密集骨干表示z映射到预激活潜在向量u：
$$\pmb{u} = \pmb{W_e}(z - \pmb{b_d}) + \pmb{b_e}$$

**激活函数**：应用ReLU获得稀疏潜在表示：
$$g(z) = \mathrm{ReLU}(\mathbf{u})$$

**解码器**：从稀疏编码重建密集表示：
$$\tilde{z} = W_d g(z) + b_d$$

**训练目标**：最小化重建误差并加入稀疏正则化：
$$\mathcal{T}(\phi) = \|z - \tilde{z}\|_2^2 + \alpha \mathcal{R}(g(z))$$

其中α控制稀疏度与重建质量的权衡。较低的α值（如2e-4）导致较低的MSE和更好的重建，但L0较大（1081.1）；较高的α值（如8e-4）导致较高的MSE但L0较小（242.2）。

### 5.2 性状提取算法

性状提取遵循Algorithm 1的流程：
1. **稀疏激活计算**：对每张图像计算SAE潜在表示。
2. **激活阈值化**：应用激活阈值t_activation筛选高激活单元。
3. **分类学性状聚合**：在物种和属级别聚合激活频率。
4. **频率阈值筛选**：应用归一化频率阈值t_freq，仅保留在物种内一致表达的性状。
5. **显著性状识别**：通过物种对比评分识别具有物种判别力的性状。

### 5.3 物种对比排序

对SAE单元按物种对比分数排序，该分数优先考虑对目标物种强激活但对近缘物种弱激活的单元。高分的掩码被裁剪为紧凑的边界框，然后输入MLLM生成性状描述。

## 实验与关键发现

### 6.1 数据集与实验设置

- **BIOSCAN-5M**：大规模昆虫图像多模态数据集（Gharaee et al., 2024），其中9.2%的样本具有物种级标注。
- **BIOSCAN-TRAITS**：本文构建的数据集，包含19K张图像、80K条性状描述（平均每张图像4.2条），覆盖736个物种、417个属。
- **特征提取器**：DINOv2-base（ViT-B/14），从ViT的倒数第二层提取特征用于SAE训练。
- **MLLM**：主要使用Qwen2.5-VL-72B（Wang et al., 2024），消融实验中也比较了Qwen2.5-VL-7B和GPT-5 mini。

### 6.2 主要结果

**Table 1**展示了SAE定位对性状描述质量的显著提升：

| 设置 | 图像数量 | 平均评分 | 均值归一化评分 | Token数/查询 |
|------|---------|---------|--------------|-------------|
| MLLM-only | 1 | 3.00 | 0.97 | 1,072 |
| MLLM+SAE | 1 | 3.84 | 1.24 | 1,072 |
| MLLM-only | 3 | 3.15 | 1.02 | 3,216 |
| MLLM+SAE | 3 | **3.91** | **1.26** | 3,216 |

SAE+多图像MLLM的平均人类评分为3.91，显著高于仅用MLLM的3.15（+0.76）。

**Table 5**展示了性状级监督对零样本物种分类的提升：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/024_Table_5.jpg]]
*Table 5: Zero-shot species classification accuracy (%) on the Insects (Ullah et al., 2022) benchmark. Incorporating trait-level supervision yields clear gains over the baseline pretrained model. BioCLIP 2 is pretrained on BIOSCAN-5M; therefore, we evaluate it directly under trait-level supervision.*

| 模型 | 准确率 (%) |
|------|-----------|
| BioCLIP 基线 | 34.8 |
| BioCLIP + 物种级微调 | 39.6 |
| BioCLIP + 性状级微调 | **39.9** |
| BioCLIP 2 基线 | 55.3 |
| BioCLIP 2 + 性状级微调 | **56.23** |

在BIOSCAN-TRAITS上微调BioCLIP后，零样本物种分类准确率从34.8%提升至39.9%（+5.1%）。

### 6.3 消融实验

**SAE稀疏度的影响（Table 2）**：较低稀疏度（α=2e-4, L0=1081.1）比较稀疏度（α=8e-4, L0=242.2）获得更高评分。较低的α值导致更低的MSE和更好的重建，提高了潜在单元的覆盖率，从而改善召回率。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/020_Table_2.jpg]]
*Table 2: SAEs often trade off between reconstruction error (MSE) and sparsity ( $L _ { 0 }$ ) . We investigate the effect of choosing between different balances of these errors. We find that lower sparsity performs better for both values of frequency threshold $\begin{array} { r } { ( t _ { \mathrm { f r e q } } ) . } \end{array}$ . A lower value of the sparsity coefficient (α) leads to lower MSE and thus better reconstruction. It improves the coverage of latents, leading to better recall. The experimental setup uses an input dataset of 1,000 images.

**频率阈值的影响（Table 3）**：提高t_freq可提升精度但减少提取的性状数量。t_freq=3e-3时提取7,897个性状，t_freq=6e-3时785个，t_freq=1e-2时仅20个，反映了覆盖度与特异性之间的权衡。

**MLLM模型规模的影响（Table B.3）**：Qwen2.5-VL-72B（平均评分3.58）显著优于Qwen2.5-VL-7B（2.90），且能避免幻觉。GPT-5 mini获得最高平均评分（4.04），但为闭源模型。

**特征提取器的影响（Table E.6）**：DINOv2-base在1000物种分类基准上显著优于CLIP ViT-B/16（41.28% vs 24.57%）。

### 6.4 定性分析

**Figure 2**展示了BIOSCAN-TRAITS与Grad-CAM在Thymoites guanicae上的性状定位对比。BIOSCAN-TRAITS生成与清晰、特定解剖结构关联的可解释性状描述，而Grad-CAM产生弥散热图，突出显示广泛的体区，缺乏物种级解耦。

**Figure J.11**展示了SAE神经元的空间定位：神经元4040激活于胸部，16584响应于腿-体连接处，13433响应于眼睛，14153响应于腹部。

### 6.5 公平性与局限性

- 所有性状描述评分均由本文作者完成，可能存在主观偏差。评分采用每位评分者均值归一化，以缓解个体评分尺度差异。
- BIOSCAN-5M数据集采用Creative Commons Attribution 3.0 Unported许可，允许学术研究使用。
- GPT-5 mini等闭源模型在较低API成本下表现更强，但存在数据治理约束；开源模型Qwen2.5-VL-72B可内部部署，适合有数据合规要求的场景。
- SAE发现的潜在因子可能对应多个共现性状（如“细长+薄”），而非完全单语义。
- 当前流水线仅依赖图像和物种标签，未利用DNA条形码、地理信息等多模态数据。
- 下游评估仅在一个基准（Insects）上进行，泛化性有待进一步验证。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of salient morphological trait description generation using a just MLLM vs. $\mathbf { M L L M } + \mathbf { S A E } \left( t _ { \mathrm { f r e q } }$ = 1 e - 2 $\right$) for Agyneta straminicola. Each red box highlights a region selected by SAE neurons with high activation, indicating regions used for prompting the MLLM + SAE. The use of SAE helps MLLMs focus on salient morphological traits rather than general descriptions of all body parts. Table 1: Incorporating latent-specific patches significantly improves the quality of trait descriptions. Including multiple images in the prompt encourages MLLMs to focus on the traits common across all images, at the cost of more to...

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/022_Figure_6.jpg]]
*Figure 6: Variation of rating with different levels of SAE sparsity. A lower level of sparsity performs better for both values of frequency threshold $t _ { \mathrm { f r e q } }$*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_oFRbiaib5Q_Automatic_Image/figures/023_Table_4.jpg]]
*Table 4: Runtime and throughput of the proposed pipeline, measured on two NVIDIA H100 80GB GPUs. Times are averaged over the BIOSCAN-TRAITS workload.*

## 定位与知识库关联

本文方法位于以下研究交叉点：

**稀疏自编码器（SAE）**：SAE最初在语言模型领域被提出用于实现单语义性（Bricken et al., 2023; Templeton et al., 2024），随后被扩展到视觉模型（Stevens et al., 2025; Pach et al., 2025）。本文首次将SAE应用于生物形态性状的自动标注，验证了其在细粒度视觉理解任务中的有效性。

**基础模型与生物多样性**：DINOv2（Oquab et al., 2024）作为自监督视觉基础模型，在物种分类任务上显著优于CLIP。BioCLIP（Stevens et al., 2024; Gu et al., 2025）是面向生物多样性的视觉-语言基础模型。本文通过性状级微调进一步提升了BioCLIP的零样本分类能力。

**自动性状提取**：传统方法依赖手工特征或深度学习分割（Hoyal Cuthill et al., 2019; Ariouat et al., 2025），但缺乏可解释性和可扩展性。本文提出的SAE+MLLM流水线实现了从“黑箱特征”到“可解释性状描述”的端到端自动转换。

**知识库定位**：BIOSCAN-TRAITS数据集填补了大规模、高质量、带性状标注的生物图像数据集的空白。该数据集可直接用于生态学中的功能性状分析、物种分类模型训练、以及生物多样性监测等下游任务。

## 原文 PDF

![[paperPDFs/ICLR_2026/Automatic_Image_Level_Morphological_Trait_Annotation_for_Organismal_Images.pdf]]
