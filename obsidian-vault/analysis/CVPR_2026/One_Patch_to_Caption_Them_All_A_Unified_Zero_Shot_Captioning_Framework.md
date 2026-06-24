---
title: "One Patch to Caption Them All: A Unified Zero-Shot Captioning Framework"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/One_Patch_to_Caption_Them_All_A_Unified_Zero_Shot_Captioning_Framework.pdf
project_link: "https://paciosoft.com/Patch-ioner/"
code_link: "https://paciosoft.com/Patch-ioner/"
aliases:
- PI
- OPCTAUZSCF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 选择能够产生密集、语义丰富的patch级特征的视觉骨干（如基于DINOv2的Talk2DINO）并结合无参数的patch聚合策略，是实现统一零样本区域描述的关键操纵变量。
primary_logic: 提出从图像中心转向patch中心的范式：将patch作为基本描述单元，利用冻结的视觉-语言骨干提取语言对齐的patch嵌入，通过简单的平均聚合对任意区域（从单个patch到整图）生成描述，无需任何区域-文本对监督，统一了多种粒度的描述任务。
claims:
- 基于DINOv2的视觉骨干（Talk2DINO）在所有区域描述任务上显著优于CLIP，表明密集的patch级语义对区域级描述至关重要。
- Patch-centric框架在细粒度本地任务（Trace/Dense Captioning）上大幅超越全局描述基准和区域监督方法（如AlphaCLIP）。
- 通过简单的无参数patch聚合，模型能够统一处理多种粒度的区域描述，无需任务特定修改，且在区域集描述中表现优于全局和裁剪方法。
- 采用记忆体投影（Memory）缓解模态间隙比噪声注入方法更稳定，在区域级任务上优势明显。
---

# One Patch to Caption Them All: A Unified Zero-Shot Captioning Framework

> [!tip] 核心洞察
> 提出从图像中心转向patch中心的范式：将patch作为基本描述单元，利用冻结的视觉-语言骨干提取语言对齐的patch嵌入，通过简单的平均聚合对任意区域（从单个patch到整图）生成描述，无需任何区域-文本对监督，统一了多种粒度的描述任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一Patch统摄所有：统一零样本图像描述框架 |
| 英文题名 | One Patch to Caption Them All: A Unified Zero-Shot Captioning Framework |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.02898) · [Code](https://paciosoft.com/Patch-ioner/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Patch-ioner |
| Dataset | Trace Captioning, Dense Captioning, Region-Set Captioning, Image Captioning |

> [!tip] 效果简介
> - Trace Captioning (COCO) 上，CIDEr 27.9 (Talk2DINO + Memory) vs 10.9 (CLIP) (+17.0)。
> - Dense Captioning (VG v1.2) 上，CIDEr 31.9 (Talk2DINO + Memory) vs 10.9 (CLIP) (+21.0)。
> - Region-Set Captioning (COCO Entities) 上，CIDEr 109.1 (Talk2DINO + Memory) vs 41.6 (CLIP) (+67.5)。

## 概述

**问题瓶颈**：现有零样本图像描述方法普遍依赖全局图像表示（如CLS token），无法对任意空间区域生成描述，且缺乏区域级文本监督，难以扩展至细粒度、可交互的描述任务。

**核心洞察**：本文提出从“图像中心”转向“patch中心”的范式——将patch作为基本描述单元，利用冻结的视觉-语言骨干提取语言对齐的patch嵌入，通过简单的无参数平均聚合对任意区域（从单个patch到非连续区域集乃至整图）生成描述，无需任何区域-文本对监督，统一了多种粒度的描述任务。

**方法定位**：所提框架**Patch-ioner**由四个模块构成：①基于DINOv2的**Talk2DINO**视觉编码器提取密集、语义丰富的patch级特征；②无参数**patch平均聚合**将任意区域内的patch嵌入组合为区域表示；③基于文本记忆的**投影模块**将视觉特征映射到文本子空间以缓解模态间隙；④纯文本预训练的**自回归解码器**生成自然语言描述。该方法属于零样本区域描述，无需区域级监督，与全局描述基准（DeCap、CLOSE、ZeroCap、ViECap）和区域监督方法（AlphaCLIP、RegionCLIP）形成对比。

**主要结果**：在Trace Captioning（COCO）上CIDEr达27.9（CLIP基线10.9，+17.0）；Dense Captioning（VG v1.2）上CIDEr达31.9（+21.0）且mAP达21.31（超越AlphaCLIP的14.63）；Region-Set Captioning（COCO Entities）上CIDEr达109.1（+67.5）；Image Captioning上CIDEr达69.2（+27.1）。基于patch的聚合在细粒度本地任务上甚至超越了依赖显式掩码监督的AlphaCLIP，验证了密集patch语义对区域级描述的决定性作用。

## 背景与动机

图像描述（Image Captioning）旨在为视觉内容生成自然语言描述，是连接视觉与语言的核心任务之一。传统方法主要关注整图级别的描述生成，通过在大规模图像-文本对上进行监督训练，学习从全局视觉表示到文本的映射。然而，随着人机交互、视觉问答和内容编辑等应用的发展，用户对视觉内容的理解需求已从整图层面深入到任意空间区域——人们不仅想知道“这张照片里有什么”，更希望针对特定物体、局部区域甚至非连续的多个区域获得精准的语言描述。

现有的零样本图像描述方法（如 **DeCap**、**CLOSE**、**ZeroCap** 等）虽然在无需配对图像-文本数据方面取得了进展，但它们从根本上受限于图像中心化（image-centric）的范式：这些方法依赖全局图像表示（如 CLIP 的 CLS token）来生成描述，无法对任意空间区域进行定位和描述。当用户需要了解图中某个特定物体或区域时，这类方法只能返回整图描述，缺乏空间定位能力。

与此同时，具备区域描述能力的方法（如 **AlphaCLIP**、**RegionCLIP**）又面临另一重困境：它们需要显式的区域-文本对监督信号进行训练。收集大规模、高质量的区域级标注成本极高，且标注质量难以保证，这严重制约了此类方法的扩展性和通用性。

**核心瓶颈**在于：现有视觉-语言模型（如 CLIP）虽然实现了图像与文本的全局对齐，但其 patch 级别的特征缺乏细粒度的语义信息，难以直接用于区域描述。这导致了一个两难局面——要么牺牲空间粒度换取零样本能力，要么牺牲零样本能力换取区域精度。

**Patch-ioner** 的提出正是为了打破这一僵局。其核心动机是：能否将描述的基本单元从“整张图像”下沉到“patch”，从而在保持零样本特性的同时，自然地支持任意粒度的区域描述？这一范式转换的关键在于找到一种能够产生密集、语义丰富的 patch 级特征的视觉骨干，并通过简洁的聚合机制将这些局部特征组织成对任意区域的描述，而无需任何区域级监督。

## 核心创新

Patch-ioner 的核心创新在于将零样本图像描述从传统的“图像中心”范式彻底转向“Patch中心”范式，通过三个关键操纵变量（changed slots）实现统一的区域描述框架。

### 范式转变：从图像到Patch的原子化描述

现有零样本描述方法（如 **DeCap**、**CLOSE**、**ZeroCap**）均依赖全局图像表示（如CLS token），这从根本上限制了它们对任意空间区域生成描述的能力。Patch-ioner 的核心洞察是：**将单个patch视为描述的基本原子单元**，通过聚合任意区域的patch嵌入来生成描述，从而无需任何区域-文本对监督即可统一处理从单个patch到整图的所有描述粒度。这一范式转变的因果机制在于：当描述单元从整图缩小到patch时，模型天然获得了对空间区域的灵活访问能力，而不再受限于全局表示的粗粒度瓶颈。

### 关键操纵变量一：密集语义视觉骨干（Talk2DINO）

视觉骨干的选择是决定区域描述质量的核心操纵变量。传统方法使用的 **CLIP** 骨干虽然具备图像-文本对齐能力，但其patch特征缺乏细粒度语义——CLIP 的训练目标（图像级对比学习）使得patch嵌入主要服务于全局表示，单个patch的语义信息严重不足。

Patch-ioner 转向基于 **DINOv2** 的 **Talk2DINO** 骨干。DINOv2 通过密集局部对比预训练，使每个patch嵌入都包含丰富的语义信息，同时Talk2DINO进一步将这些密集特征与语言空间对齐。这一改变的效果是决定性的：**Table 1** 显示，Talk2DINO在所有区域描述任务上均显著优于CLIP，例如在Trace Captioning上CIDEr从10.9跃升至27.9（+17.0），在Dense Captioning上从10.9升至31.9（+21.0）。这证明密集的patch级语义对区域描述至关重要，而非仅仅依赖全局对齐。

### 关键操纵变量二：无参数Patch聚合

传统方法处理区域描述时，要么使用全局CLS token（丢失空间信息），要么将裁剪区域单独输入模型（计算冗余且无法处理非连续区域）。Patch-ioner 采用极简的无参数聚合策略：对区域内所有patch嵌入进行平均，即：

$$\mathbf{v}_{S} = \sum_{i\in S} w_i \mathbf{v}_i, \quad w_i = 1/|S|$$

这一设计的优势在于：（1）**通用性**——同一聚合机制可处理任意形状区域（边界框、轨迹、非连续区域集）；（2）**零参数**——无需学习聚合权重，避免了对特定粒度任务的过拟合。消融实验（**Table 11**）证实，可学习注意力聚合虽然在训练粒度一致的局部任务上提升显著，但在不同粒度的任务间泛化性较差，而固定平均聚合更为鲁棒。

对于多区域集，表示通过跨区域平均自动实现重叠patch的加权增强：

$$\mathbf{v}_{\mathfrak{B}} = \frac{1}{\sum_{B\in\mathfrak{B}} |S_B|} \sum_{B\in\mathfrak{B}} \sum_{i\in S_B} \mathbf{v}_i$$

### 关键操纵变量三：记忆投影缓解模态间隙

视觉编码器与文本解码器之间的模态间隙是零样本描述的关键瓶颈。Patch-ioner 采用基于文本记忆的投影策略（Memory），将视觉特征映射到文本嵌入空间：

$$\mathbf{v}_{\mathrm{proj}} = M \alpha, \quad \alpha = \operatorname{softmax}\left(\frac{1}{\tau} M^{\top} \mathbf{v}\right)$$

其中 $M$ 是文本记忆矩阵，$\tau=0.01$ 控制投影锐度。与噪声训练方法（Noise）相比，记忆投影在区域级任务上优势更明显（**Table 10**），尤其在密集描述和区域集描述任务上表现更优。这一策略使得视觉特征能够以文本解码器更熟悉的形式呈现，显著提升了区域描述的流畅性和准确性。

### 统一框架的涌现能力

上述三个操纵变量的组合产生了超出单独改进的涌现效果：Patch-ioner 在细粒度本地任务上不仅大幅超越全局描述基准，甚至超过了依赖显式掩码监督的区域方法 **AlphaCLIP**（**Table 2**，Dense Captioning mAP: 21.31 vs. 14.63）。这证明，通过正确的视觉骨干和简单的patch聚合，零样本方法可以匹敌甚至超越需要区域监督的方法——核心在于patch级语义的密度和质量，而非监督信号的多少。

## 整体框架

Patch-ioner 提出了一种从“图像中心”到“patch中心”的范式转换，将单个 patch 视为基本的描述单元，从而统一处理从单个 patch 到非连续区域集再到整图的任意空间粒度的零样本描述任务，全程无需任何区域-文本对监督。

### 核心流水线

整个框架由四个顺序模块构成，输入为图像和用户指定的区域（边界框、轨迹或整图），输出为对应区域的自然语言描述：

1. **视觉编码器**：使用冻结的视觉-语言骨干网络将输入图像编码为密集的、语言对齐的 patch 嵌入。与依赖全局 CLS token 的传统方法不同，Patch-ioner 要求视觉骨干能够在 patch 级别产生语义丰富且与语言空间对齐的特征，这是实现细粒度区域描述的基础。实验表明，基于 DINOv2 的 **Talk2DINO** 在所有区域描述任务上显著优于 CLIP，成为默认视觉骨干（Table 1）。

2. **Patch 聚合**：对用户指定区域内的所有 patch 嵌入进行无参数平均，生成统一的区域表示。对于任意形状的区域 $R$，其表示由区域内 patch 索引集 $S$ 的嵌入加权求和得到：

   $$\mathbf{v}_{S} = \sum_{i\in S} w_i \mathbf{v}_i$$

   默认采用平均聚合（$w_i = 1/|S|$）。该设计的关键优势在于**无参数**和**通用性**：无需针对不同粒度的任务学习不同的聚合策略，且对于重叠区域（如多个边界框的交叠部分），相应的 patch 会被自动加权更多，自然地捕获空间上下文。

3. **模态间隙缓解（记忆投影）**：在送入文本解码器之前，区域表示 $\mathbf{v}$ 被投影到文本嵌入空间，以减轻视觉与语言表示之间的子空间不匹配。具体采用基于文本记忆的投影机制：

   $$\mathbf{v}_{\mathrm{proj}} = M \alpha, \quad \alpha = \operatorname{softmax}\left(\frac{1}{\tau} M^{\top} \mathbf{v}\right)$$

   其中 $M$ 为从文本语料中学习到的记忆矩阵，$\tau=0.01$ 控制 softmax 的锐度。消融实验表明，记忆投影（Memory）在区域集描述和密集描述任务上优于噪声训练（Noise）策略，因此被选为默认配置（Table 10）。

4. **文本解码器**：基于投影后的区域特征，使用自回归语言模型（如 GPT-2 small）生成自然语言描述。解码器仅通过文本数据进行前缀语言建模训练，完全不接触图像-文本对，保证了框架的零样本特性。

### 多粒度区域描述的统一

框架通过简单的 patch 聚合策略自然地支持多种粒度的描述任务，无需任何任务特定的修改：

- **边界框描述**：直接聚合框内所有 patch 嵌入。
- **区域集描述**：对于多个边界框组成的区域集 $\mathfrak{B}$，其表示通过对所有框内 patch 嵌入取平均获得，重叠区域被自动赋予更高权重：

  $$\mathbf{v}_{\mathfrak{B}} = \frac{1}{\sum_{B\in\mathfrak{B}} |S_B|} \sum_{B\in\mathfrak{B}} \sum_{i\in S_B} \mathbf{v}_i$$

- **轨迹描述**：沿鼠标轨迹采样 $L$ 个点，取对应 patch 嵌入的平均：

  $$\mathbf{v}_{T} = \frac{1}{L} \sum_{j=1}^{L} \mathbf{v}_{i_j}$$

- **整图描述**：聚合图像中所有 patch 嵌入，将全局描述任务自然地纳入同一框架。

### 设计决策的因果逻辑

框架有效性的核心因果链路可概括为：**密集的 patch 级语义特征（Talk2DINO）→ 无参数 patch 聚合 → 统一的区域表示 → 记忆投影缓解模态间隙 → 零样本文本解码**。其中，视觉骨干的选择是最关键的操纵变量——Talk2DINO 通过密集局部对比预训练，使得每个 patch 嵌入本身就携带了丰富的语义信息且与语言空间对齐，这是后续简单平均聚合能够工作的前提。相比之下，CLIP 的 patch 特征缺乏细粒度语义，即使采用相同的聚合和投影策略，在区域级任务上的 CIDEr 也大幅落后（如 Trace Captioning 上 10.9 vs. 27.9）。

### 与现有方法的根本差异

传统的零样本描述方法（如 **DeCap**、**CLOSE**、**ZeroCap**）依赖于全局图像表示，无法对任意空间区域生成描述。区域监督方法（如 **AlphaCLIP**、**RegionCLIP**）虽然支持区域输入，但需要显式的区域-文本对训练。Patch-ioner 通过将 patch 作为基本描述单元，首次在完全零样本的条件下实现了对任意区域的描述，且实验表明其 patch 聚合策略甚至超越了依赖显式掩码监督的 AlphaCLIP（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/001_Figure_1.jpg]]
*Figure 1: Patch-centric framework for unified zero-shot captioning. A. Overview of our framework. First, we extract language-aligned dense patch embeddings from the image using a VLM. Given a region, we select the underlying patches and aggregate their features to obtain a region representation. Finally, we obtain the region caption by applying a zero-shot text decoder, that is a) conditioned on the latent region representation, b) trained on text-only data, and c) equipped with a mechanism to handle the modality gap present in vision-language common spaces. This enables regional captioning without requiring region-level supervision. B. By aggregating patch-level features from arbitrary image regions...*

## 核心模块与公式推导

Patch-ioner 框架将零样本区域描述解耦为四个核心模块，其完整流程可表述为：

$$t = \phi\big(\text{agg}_R(\psi(I), R)\big)$$

其中 $\psi$ 为视觉编码器，$\text{agg}_R$ 为 Patch 聚合器，$\phi$ 为文本解码器。实际部署时，在聚合器与解码器之间插入模态间隙缓解模块（记忆投影），形成 $\phi(\text{proj}(\text{agg}_R(\psi(I), R)))$。

---

### 模块一：视觉编码器（Vision Encoder）

**角色**：将输入图像 $I$ 编码为密集的、与语言对齐的 patch 级嵌入。

**关键选择**：基于 DINOv2 的 **Talk2DINO** 作为冻结骨干。与 CLIP 的全局图像-文本对齐不同，DINOv2 通过密集局部对比预训练，使每个 patch 嵌入携带丰富的细粒度语义信息，且天然与语言空间对齐。Table 1 的骨干对比实验证实：Talk2DINO 在 Trace Captioning 上 CIDEr 达 27.9，而 CLIP 仅 10.9（+17.0），验证了密集 patch 语义对区域级描述的决定性作用。

---

### 模块二：Patch 聚合（Patch Aggregation）

**角色**：将区域内所有 patch 嵌入无参数地聚合为单一区域表示，支持任意形状区域。

**核心公式 — 通用 Patch 聚合**：

$$\mathbf{v}_{S} = \sum_{i \in S} w_i \mathbf{v}_i$$

其中 $S$ 为区域内 patch 索引集，$\mathbf{v}_i$ 为第 $i$ 个 patch 的嵌入。默认采用**平均聚合**：$w_i = 1/|S|$，无需任何可学习参数。

**区域集表示**（多个边界框 $\mathfrak{B}$）：

$$\mathbf{v}_{\mathfrak{B}} = \frac{1}{\sum_{B\in\mathfrak{B}} |S_B|} \sum_{B\in\mathfrak{B}} \sum_{i\in S_B} \mathbf{v}_i$$

该公式对重叠区域内的 patch 自动施加更高权重，因其在多个边界框中重复计数。

**轨迹表示**（沿鼠标轨迹 $T$ 采样 $L$ 个点）：

$$\mathbf{v}_{T} = \frac{1}{L} \sum_{j=1}^{L} \mathbf{v}_{i_j}$$

**设计动机**：固定平均聚合在不同粒度的任务间具有强泛化性。消融实验（Table 11）表明，可学习的注意力聚合在训练粒度一致的局部任务上提升显著，但跨粒度泛化能力不足；平均聚合则以鲁棒性见长，支撑了“统一框架”的核心主张。

---

### 模块三：模态间隙缓解 — 记忆投影（Memory Projection）

**角色**：将视觉空间中的区域表示 $\mathbf{v}$ 投影到文本嵌入子空间，缓解视觉-语言模态间隙。

**核心公式**：

$$\mathbf{v}_{\mathrm{proj}} = M \alpha, \quad \alpha = \operatorname{softmax}\left(\frac{1}{\tau} M^{\top} \mathbf{v}\right)$$

其中 $M \in \mathbb{R}^{d \times K}$ 为可学习的文本记忆矩阵（$K$ 个记忆元素），$\tau = 0.01$ 控制 softmax 锐度。该投影本质上是记忆元素的相似度加权线性组合——视觉特征通过查询记忆矩阵，被“翻译”为文本空间中的表示。

**策略选择依据**：Table 10 对比了记忆投影（Memory）与噪声训练解码器（Noise）两种模态间隙缓解方案。两者整体性能可比，但 Memory 在 Dense Captioning 和 Region-Set Captioning 上优势更大，且训练更稳定，因此被选为默认配置。

---

### 模块四：文本解码器（Text Decoder）

**角色**：基于投影后的区域特征自回归生成自然语言描述。

**训练方式**：采用前缀语言建模（prefix language modeling），仅在文本语料上训练，不接触任何图像-文本对或区域-文本对。解码器以 $\mathbf{v}_{\mathrm{proj}}$ 为条件前缀，逐 token 生成描述 $t = \phi(\mathbf{v}_{\mathrm{proj}})$。

**解码器规模**：Table 4 消融显示，较小的 GPT-2 small（124M）在区域级任务上表现优于更大的语言模型，表明解码器容量并非当前瓶颈，区域表示质量才是性能上限所在。

---

### 可学习聚合的扩展公式（供参考）

论文在附录中探索了可学习聚合方案，将平均池化与注意力池化组合：

$$v_R = v_{\mathrm{mean}} + \alpha \, v_{\mathrm{att}}$$

其中 $\alpha$ 为可学习标量，$v_{\mathrm{att}}$ 为基于 patch 间交互的注意力池化结果。该方案在训练-测试粒度一致时显著优于固定聚合，但因泛化性不足而未作为默认选择。

## 实验与分析

### 核心发现：patch中心化框架的跨粒度优势

Patch-ioner的核心实验结论可归结为一点：**将描述单元从全局图像表示切换为密集的patch级特征，是解锁细粒度零样本区域描述能力的关键因果杠杆**。Table 1 的视觉骨干对比系统性地验证了这一主张。基于CLIP的全局表示在Trace Captioning上仅取得10.9 CIDEr，而基于DINOv2的Talk2DINO达到27.9（+17.0）；在Dense Captioning上差距更为悬殊（10.9 vs. 31.9，+21.0）。这一趋势在Region-Set Captioning上进一步放大（41.6 vs. 109.1，+67.5），表明**密集局部对比预训练产生的patch特征天然携带细粒度语义，而CLIP的patch特征缺乏这种区域级语言对齐**。

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/002_Table_1.jpg]]
*Table 1: Vision-Language Backbones. CIDEr (C) and RefPAC-S (P) across four captioning tasks*

值得注意的是，即使是在传统的整图描述任务上，Talk2DINO + Memory配置也以69.2 CIDEr显著超越CLIP的42.1，同时在CLIP-S上保持优势（72.8 vs. 66.2）。这说明patch中心化范式并未牺牲全局理解能力——通过简单平均聚合所有patch嵌入，模型同样能获得高质量的整图表示。

### 与现有方法的全面对比

Table 2 将Patch-ioner与零样本基线（DeCap、CLOSE、ZeroCap、ViECap）及区域监督方法（AlphaCLIP、RegionCLIP）进行了系统对比。关键观察如下：

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/004_Table_2.jpg]]
*Table 2: Comparison of our Patch-ioner framework, using Talk2DINO (T2D), with ZS methods on trace, dense, region-set, and image captioning tasks. Our approach consistently outperforms whole-image and region-supervised baselines in local, fine-grained captioning tasks, while achieving competitive results on whole-image captioning. The table reports CIDEr (C), RefPAC (P), mean average precision (mAP) for dense captioning, and CLIP-Score (CLIP-S) when applicable; best and second-best results are in bold and underlined, respectively*

**细粒度本地任务上的压倒性优势**。在Trace Captioning和Dense Captioning上，Patch-ioner（Talk2DINO + Memory）大幅领先所有零样本基线。以Dense Captioning的mAP指标为例，Patch-ioner达到21.31，而AlphaCLIP（依赖显式掩码监督的方法）仅为14.63。这意味着**无参数的patch聚合策略在没有区域-文本对训练的情况下，超越了需要区域监督的注意力掩码方法**——这是一个反直觉但证据充分的结果（置信度0.95）。

**区域集描述上的上下文建模能力**。在COCO Entities的Region-Set Captioning上，Patch-ioner的RefPAC-P达到87.5，显著高于CLIP基线的78.8（+8.7）。RefPAC-P衡量的是描述中正确提及指定区域实体的精度，这一指标直接反映了模型对多区域组合语义的把握能力。平均聚合自动赋予重叠patch更高权重（见公式 $\mathbf{v}_{\mathfrak{B}} = \frac{1}{\sum_{B\in\mathfrak{B}} |S_B|} \sum_{B\in\mathfrak{B}} \sum_{i\in S_B} \mathbf{v}_i$），使得模型无需显式建模区域间关系即可产生上下文连贯的描述。

**与大型多模态模型的对比**（Table 3）揭示了当前方法的定位。在整图描述上，LLaVA-1.5等大规模模型凭借海量图文对训练取得更高CIDEr，但Patch-ioner在区域级任务上具有独特优势——LMM通常缺乏对任意空间区域的零样本描述能力。这一对比明确了Patch-ioner的生态位：**不是替代大规模多模态模型，而是在细粒度、可交互的区域描述场景中填补空白**。

### 消融实验：关键设计选择的证据链

**视觉骨干的选择**（Table 1）是最具决定性的消融。DINOv2系列模型（包括DINO.txt和Talk2DINO）在所有区域级任务上一致优于CLIP系列，其中Talk2DINO表现最佳。这验证了核心洞察：**密集局部对比预训练是patch特征获得语言对齐语义的关键机制**。CLIP的全局对比目标使得patch特征缺乏细粒度语义，即使配合相同的聚合和解码策略也无法弥补这一根本差距。

**模态间隙缓解策略**（Table 10）对比了记忆投影（Memory）与噪声训练（Noise）两种方案。两者整体性能可比，但Memory在区域集和密集描述任务上优势更明显。记忆投影通过 $\mathbf{v}_{\mathrm{proj}} = M \alpha$ 将视觉特征映射到文本嵌入空间（其中 $\alpha = \operatorname{softmax}(\frac{1}{\tau} M^{\top} \mathbf{v})$，$\tau=0.01$），有效缓解了视觉与文本表示的子空间不匹配。鉴于区域级任务对语义精度要求更高，Memory被选为默认配置是合理的（置信度0.95）。

**文本解码器容量**（Table 4）的消融结果反直觉：GPT-2 small（124M）在Trace和Region-Set Captioning上的CIDEr优于更大的语言模型。这表明**解码器容量并非当前框架的主要瓶颈**——在视觉表示质量受限的情况下，增大语言模型无法带来增益，甚至可能因过拟合文本先验而损害区域级描述的准确性。

**训练数据规模与多样性**（Table 5）的影响值得关注。在更大的ReLaion数据集（28.3M文本样本）上训练，Region-Set Captioning的CIDEr从109.1提升至113.5，说明**更丰富的文本预训练有助于解码器更好地利用投影后的区域特征**。但增幅有限（+4.4），再次印证视觉表示质量是当前的主要约束。

**固定聚合 vs. 可学习聚合**（Table 11）揭示了统一框架的内在张力。可学习的注意力聚合在训练粒度一致的局部任务（如Trace和Dense）上带来显著提升，但这种增益无法一致地迁移到不同粒度的任务（如Region-Set和Image Captioning）。固定平均聚合虽然在各任务上未必最优，但**提供了跨粒度的鲁棒泛化性**，这正是统一框架的核心需求。

### 失败模式与局限性

尽管Patch-ioner在区域级任务上表现突出，实验中也暴露了若干值得关注的失败模式：

1. **全局描述的上限约束**。在COCO Image Captioning上，Patch-ioner（69.2 CIDEr）与专用的大规模多模态模型（如LLaVA-1.5）存在差距。冻结的视觉骨干无法通过端到端训练进一步对齐区域级语义与文本，这是架构层面的固有限制。

2. **可学习聚合的泛化困境**。Table 11显示，在特定粒度上训练的注意力聚合难以泛化到其他粒度，说明**patch重要性的分布与描述粒度高度相关**，单一的可学习聚合策略无法同时适配从单patch到整图的跨度。

3. **Trace Captioning基准的噪声风险**。该基准依赖LLM自动清洗和重写原始标注，可能引入风格偏差或事实性错误。数据集规模有限（COCO测试集上的Trace样本量未公开具体数字），结论的外推性需谨慎对待。

4. **区域提议的缺失**。当前框架假设区域已给定，无法自主定位值得描述的区域。这限制了其在完全自动化的密集描述场景中的应用。

### 图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | Talk2DINO在所有粒度的描述任务上一致最优，密集patch语义是区域级描述的必要条件 |
| Table 2 | Patch-ioner在细粒度任务上超越零样本和区域监督基线，无参数聚合优于显式掩码注意力 |
| Table 3 | 在区域级任务上具有LMM无法替代的优势，整图描述上落后于大规模多模态模型 |
| Table 4 | 解码器容量非瓶颈，GPT-2 small在区域任务上优于更大模型 |
| Table 5 | 更大文本预训练数据带来有限但一致的增益，视觉表示质量是主要约束 |
| Table 10 | 记忆投影在区域级任务上优于噪声训练，被选为默认模态间隙缓解策略 |
| Table 11 | 固定平均聚合跨粒度泛化性最优，可学习聚合仅在训练粒度一致时有效 |

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/005_Table_3.jpg]]
*Table 3: Patch-ioner framework vs. LMMs*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/008_Table_4.jpg]]
*Table 4: Training different decoders. CIDEr (C) and RefPAC-S (P) across four captioning tasks. The model adopted is T2D + Memory (≈ DeCap) trained on COCO train Karpathy split*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/015_Table_10.jpg]]
*Table 10: Mitigation of Modality Gap. Comparison of Memory-based Projection (Memory) vs Noise-trained Decoder*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/010_Table_5.jpg]]
*Table 5: Training on different datasets. CIDEr (C) and RefPAC-S (P) across four captioning tasks. The model adopted is T2D + Memory (≈ DeCap) using the GPT2 textual decoder*

### 补充图表

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/019_Figure_7.jpg]]
*Figure 7: Qualitative results. We report four predictions of our model and compare baselines from the finer (top) to the coarser (bottom) task. For trace captioning examples, the trace time is color-coded from start (red) to end (yellow). DeCap = DeCap applied on the whole image. DeCap (Crop) = DeCap applied on cropped box. ZeroCap = ZeroCap [59] applied to the whole image. CLOSE = CLOSE [18] applied to the whole image. Ours (CLIP + Mem.) = Our patch-based framework using CLIP as backbone and the projection as modality gap mitigation strategy. Ours (Talk2DINO + Mem.) = Our patch-based framework using Talk2DINO as backbone and the projection as modality gap mitigation strategy. GT = ground-truth capti...*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/020_Figure_8.jpg]]
*Figure 8: Qualitative results. We report four predictions of our model and compare baselines from the finer (top) to the coarser (bottom) task. For trace captioning examples, the trace time is color-coded from start (red) to end (yellow). DeCap = DeCap applied on the whole image. DeCap (Crop) = DeCap applied on cropped box. ZeroCap = ZeroCap [59] applied to the whole image. CLOSE = CLOSE [18] applied to the whole image. Ours (CLIP + Mem.) = Our patch-based framework using CLIP as backbone and the projection as modality gap mitigation strategy. Ours (Talk2DINO + Mem.) = Our patch-based framework using Talk2DINO as backbone and the projection as modality gap mitigation strategy. GT = ground-truth capti...*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/011_Table_6.jpg]]
*Table 6: Trace Captioning results on COCO test set*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/012_Table_7.jpg]]
*Table 7: Dense Captioning results on VG v1.2 test set*

![[assets/figures/papers/paper_list_l2332_https_arxiv_org_abs_2510_02898/figures/013_Table_8.jpg]]
*Table 8: Region-Set Captioning results for COCO Entities test set*

## 方法谱系与知识库定位

### 1. 核心范式转换：从图像中心到Patch中心

Patch-ioner的核心贡献在于提出了一种**范式转换**——将图像描述的基本单元从全局图像表示（如CLS token）下移至**单个patch**。这一转换直接回应了现有零样本描述方法的根本瓶颈：依赖全局图像-文本对齐的视觉骨干（如CLIP）无法为任意空间区域生成描述，因为其patch级特征缺乏细粒度的语义信息。通过选择能够产生**密集、语言对齐的patch嵌入**的视觉骨干（基于DINOv2的Talk2DINO），并结合无参数的patch聚合策略，Patch-ioner在不依赖任何区域-文本对监督的条件下，统一了从单patch、任意边界框、非连续区域集到整图的多种描述粒度。

与现有工作的关系可概括为：
- **相对于全局描述基准（DeCap、CLOSE、ZeroCap、ViECap）**：这些方法均以整图CLS token为输入，无法处理区域级描述任务。Patch-ioner通过patch聚合机制，在Trace Captioning上将CIDEr从10.9（CLIP）提升至27.9，在Dense Captioning上从10.9提升至31.9（Table 1），从根本上突破了全局方法的粒度限制。
- **相对于区域监督基准（AlphaCLIP、RegionCLIP）**：这些方法需要区域-文本对进行训练（如AlphaCLIP通过掩码注意力使CLIP聚焦指定区域），而Patch-ioner在**完全零样本**条件下，其patch聚合策略甚至超越了AlphaCLIP（Table 2中Dense Captioning的mAP从14.63提升至21.31），证明了无参数聚合的泛化优势。
- **相对于大语言多模态模型（LLaVA-1.5等）**：在区域级任务上，Patch-ioner展现出竞争力（Table 3），但在整图描述上略弱于专用大规模模型，这反映了patch级语义在全局摘要任务上的固有局限。

### 2. 技术谱系定位

Patch-ioner的技术架构可定位于以下三条技术线的交汇点：

**（1）密集视觉-语言预训练线。** 框架的关键操纵变量是视觉骨干的选择。实验系统性地对比了CLIP、DINOv2、DINO.txt和Talk2DINO（Table 1），揭示了一个因果机制：**密集局部对比预训练目标**（如DINO系列的patch级自监督）是产生语义丰富patch特征的必要条件，而CLIP的全局对比目标导致patch特征缺乏细粒度语义。Talk2DINO作为最优骨干，通过额外的语言对齐训练进一步弥合了patch特征与文本空间的距离，使区域级描述质量显著提升。

**（2）零样本文本解码线。** Patch-ioner继承了DeCap的文本解码器训练范式——在纯文本语料上使用前缀语言建模训练解码器，使其能够以视觉特征为前缀自回归生成描述。但Patch-ioner将DeCap的全局CLS条件扩展为区域级patch聚合条件，并通过**记忆投影机制**（Memory-based latent projection）缓解视觉特征与文本嵌入空间的模态间隙。消融实验（Table 10）表明，记忆投影在区域集和密集描述任务上优于噪声训练方法，其核心在于通过文本记忆矩阵 $M$ 将视觉特征 $v$ 投影为相似度加权的文本嵌入组合 $v_{\text{proj}} = M \alpha$，其中 $\alpha = \operatorname{softmax}(\frac{1}{\tau} M^{\top} v)$，$\tau=0.01$ 控制投影锐度。

**（3）区域表示聚合线。** 与需要学习区域提议网络（如RegionCLIP）或掩码注意力（如AlphaCLIP）的方法不同，Patch-ioner采用**无参数平均聚合** $v_S = \sum_{i\in S} w_i v_i$（$w_i = 1/|S|$）作为默认策略。这一设计的优势在于跨粒度的鲁棒泛化：可学习注意力聚合虽然在训练粒度一致的局部任务上提升显著，但泛化至不同粒度的任务时性能下降（Table 11），而固定平均聚合在多种任务间保持稳定表现。

### 3. 适用边界与局限

Patch-ioner的能力边界受以下因素制约：

- **全局描述的性能上限。** 在COCO Image Captioning上，Patch-ioner（CIDEr 69.2）仍低于专用大规模多模态模型（如LLaVA-1.5），表明patch级语义聚合在需要高层语义摘要的全局任务上存在信息瓶颈。这是架构设计的固有取舍——以统一的patch中心范式换取细粒度能力，代价是全局抽象能力的部分损失。
- **视觉骨干的冻结限制。** 框架依赖固定的冻结视觉骨干，无法通过端到端训练进一步对齐区域级语义与文本。这意味着patch特征的质量完全取决于预训练阶段，无法针对特定描述任务进行优化。
- **Trace Captioning的数据偏差。** Trace Captioning基准构建依赖LLM自动清洗和重写，可能引入噪声或风格偏差，且数据集规模有限，影响该任务上性能评估的可靠性。
- **聚合策略的粒度敏感性。** 固定平均聚合虽然通用，但在不同粒度的任务上并非最优。可学习聚合在训练粒度一致时提升显著，但跨粒度泛化不足，揭示了统一框架内部存在粒度-性能的权衡。

### 4. 开放问题

Patch-ioner开启的方向引出以下待探索问题：

1. **弱监督下的patch语义增强。** 当前框架仅利用图像级描述损失进行解码器训练，视觉骨干完全冻结。能否设计弱监督机制（如对比学习或自蒸馏），仅利用图像级描述信号反向提升patch的语义表示质量？

2. **更优的模态间隙缓解。** 记忆投影虽优于噪声训练，但仍依赖文本记忆矩阵的规模和质量。在完全零样本（无任何区域-文本对）条件下，是否存在更有效的投影策略（如非线性映射或对抗训练）进一步减小视觉与文本子空间的不匹配？

3. **联合定位与描述的端到端扩展。** 当前框架假设区域已给定（边界框、轨迹或patch集），能否扩展至包含区域提议模块的联合模型，实现完整的端到端密集描述（同时定位和描述区域）？这需要解决区域提议与描述质量之间的联合优化问题。

4. **跨数据集的文本解码器泛化。** 在更大、更多样的文本数据集（如ReLaion 28.3M）上训练可提升区域集描述的CIDEr至113.5（Table 5），但不同文本域对描述风格和内容准确性的影响尚需系统研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/One_Patch_to_Caption_Them_All_A_Unified_Zero_Shot_Captioning_Framework.pdf]]
