---
title: ARC Is a Vision Problem!
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ARC_Is_a_Vision_Problem.pdf
aliases:
- VAV
- AIVP
tags:
  - CVPR_2026
  - topic/vision_multimodal_applications/image_and_video_generation
  - topic/vision_multimodal_applications
core_operator: 视觉先验（包括 2D 位置编码、画布增强、补丁化）的集成程度。该旋钮直接调控模型是否能够从视觉演示中隐式学习空间不变性和组合性规则。
primary_logic: 将 ARC 重构为图像到图像翻译任务，使标准视觉模型（ViT/U-Net）结合测试时训练，能够在无需显式符号推理或大规模语言预训练的情况下，从少量视觉示例中抽象出通用的转换规则。
claims:
- 累积添加视觉先验（2D 位置嵌入、补丁化、平移和缩放增强）使准确率从 26.8% 提升至 54.5%，提升幅度达 27.7 个百分点。
- VARC 在 ARC-1 上以单个 18M 参数的 ViT 达到 54.5% 准确率，大幅超越同样从零训练的循环方法 TRM（44.6%），并接近人类平均水平。
- 缩放增强单独贡献了 6.2 个百分点的提升，表明尺度不变性对于任务泛化至关重要。
- ARC-1 上 pass@2 accuracy (%) = 54.5 (ViT-18M)
---

# ARC Is a Vision Problem!

> [!tip] 核心洞察
> 将 ARC 重构为图像到图像翻译任务，使标准视觉模型（ViT/U-Net）结合测试时训练，能够在无需显式符号推理或大规模语言预训练的情况下，从少量视觉示例中抽象出通用的转换规则。

| 字段 | 内容 |
|------|------|
| 中文题名 | ARC 是一个视觉问题！ |
| 英文题名 | ARC Is a Vision Problem! |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.14761) |
| Topic | #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications |
| Method | Vision ARC (VARC) |
| Dataset | ARC-1, ARC-2 |

> [!tip] 效果简介
> - ARC-1 上，pass@2 accuracy (%) 54.5 (ViT-18M) vs 44.6 (TRM) (+9.9)；pass@2 accuracy (%) 60.4 (ensemble) vs 40.3 (HRM) (+20.1)；pass@2 accuracy (%) 60.4 (ensemble) vs 44.0 (GPT-5) (+16.4)。
> - ARC-2 上，pass@2 accuracy (%) 8.3 (ViT-18M) vs 7.8 (TRM) (+0.5)；pass@2 accuracy (%) 11.1 (ensemble) vs 5.0 (HRM) (+6.1)。

## 概述

**ARC 基准**（Abstraction and Reasoning Corpus）由大量独立的视觉推理任务组成，每个任务仅提供 2–4 对输入-输出演示，要求模型从少量示例中推断隐含的转换规则并应用于新的推理输入。现有方法主要依赖大语言模型（如 GPT-5、o3-mini-high、Claude 3.7）或从零训练的循环推理模型（如 **HRM** (Wang et al., arXiv 2025)、TRM），将 ARC 视为序列生成或符号推理问题。然而，这些方法忽视了 ARC 任务固有的视觉与空间结构——任务背后的核心概念（如“反射”、“对称”、“重力”）与视觉和物理世界紧密相连。

本文提出 **Vision ARC (VARC)** 框架，将 ARC 根本性地重构为**图像到图像翻译**问题，具体化为逐像素分类任务。该框架的核心洞察在于：通过注入基本的视觉先验（2D 位置编码、画布增强、补丁化），标准视觉模型（如 ViT、U-Net）结合测试时训练，能够在无需显式符号推理或大规模语言预训练的情况下，从少量视觉示例中隐式学习空间不变性和组合性规则。

在 ARC-1 基准上，VARC 以仅 18M 参数的 ViT 达到 **54.5%** 的准确率，大幅超越同样从零训练的循环方法 TRM（44.6%），并通过模型集成达到 **60.4%**，与人类平均水平（60.2%）持平。消融实验表明，视觉先验的累积添加贡献了 **27.7 个百分点**的提升，其中画布相关设计（平移和缩放增强）单独贡献 11.5 个百分点，缩放增强贡献 6.2 个百分点。在更具挑战性的 ARC-2 基准上，VARC 集成方法达到 11.1%，较 HRM（5.0%）提升 6.1 个百分点。

VARC 的方法定位具有显著特点：仅使用 ARC 数据和 RE-ARC 扩充进行训练，未利用互联网规模预训练数据；模型参数规模远小于主流 LLM；测试时训练独立于每个测试任务，确保评估的严格性。这一工作表明，ARC 本质上是一个视觉问题，视觉驱动的范式为抽象推理提供了更简洁、更高效的路径。

## 背景与动机

ARC（Abstraction and Reasoning Corpus）是一个用于评估通用人工智能抽象与推理能力的基准。每个 ARC 任务由极少量的输入-输出网格对（通常 2–4 对）作为演示，要求模型从这些示例中推断出隐含的转换规则，并将其应用于新的测试输入。ARC 的核心挑战在于任务的高度多样性：训练集、评估集与测试集之间的任务互不重叠，模型必须在少样本条件下实现跨任务泛化。

现有方法主要沿两条路径展开。一类是**基于语言或循环推理的模型**，例如将网格序列化为离散 token 后送入 Transformer 解码器或循环网络进行自回归生成。代表性工作包括 **HRM**（Hierarchical Reasoning Model, Wang et al., arXiv 2025）和 **TRM**（Transductive Reasoning Model），它们从零开始在 ARC 数据上训练，但精度有限（HRM 在 ARC-1 上 pass@2 仅 40.3%，TRM 为 44.6%）。另一类是**大规模语言模型（LLM）**，如 GPT-5、o3-mini-high、Deepseek R1、Claude 3.7 等，借助互联网规模的预训练知识进行推理，但它们在 ARC-1 上的最优表现（GPT-5 为 44.0%）同样未超越循环模型，且计算成本极高。此外，**ViT-ARC**（Li et al., 2024）曾尝试直接使用视觉模型拟合训练任务，却未能实现泛化。

这些方法的共同瓶颈在于：**未能充分利用 ARC 任务固有的视觉与空间结构**。ARC 的底层概念——如反射、对称、重力、物体计数等——天然与视觉和物理世界紧密相关（Figure 1）。然而，将网格展平为 token 序列会破坏 2D 空间拓扑，使模型丧失对平移、缩放、局部邻域等基本视觉不变性的归纳偏置。语言模型则进一步受限于离散符号推理的路径，缺乏对连续空间变换的隐式建模能力。

本文提出 **Vision ARC (VARC)** 框架，核心洞察是：**将 ARC 重构为图像到图像的翻译问题**，使标准视觉模型能够从少量视觉演示中隐式学习空间不变性和组合性规则，而无需显式符号推理或大规模语言预训练。具体而言，VARC 将 ARC 任务建模为逐像素分类（类似语义分割），采用视觉 Transformer（ViT）或卷积 U-Net 作为骨干网络，结合 2D 位置编码、画布增强与补丁化等视觉先验，并通过两阶段训练（离线训练 + 测试时训练）实现少样本适应。这一范式转换使仅 18M 参数的 ViT 模型在 ARC-1 上达到 54.5% 的 pass@2 准确率，集成后更达到 60.4%，超越所有从零训练的循环模型，并接近人类平均水平（60.2%）。

## 核心创新

VARC 的核心创新在于**将 ARC 从离散符号推理问题重构为图像到图像的翻译问题**，并通过系统性地注入视觉先验，使标准视觉模型能够从少量示例中隐式学习空间变换规则。这一范式转换体现在以下关键维度：

### 任务范式：从符号生成到逐像素分类

现有方法将 ARC 视为语言序列生成（LLM 方法）或递归推理（**HRM** 与 **TRM**），模型需要自回归地输出离散颜色令牌序列。VARC 则将其重新定义为**逐像素语义分割**问题：模型接收输入网格图像，直接输出每个像素的颜色类别分布。这一转变使模型天然保留了二维空间结构，避免了将空间关系序列化造成的信息损失。训练目标为标准逐像素交叉熵损失：

$$\mathcal{L}(\theta) = \mathbb{E}_{T,i} \left[ \mathcal{D}(y_i, f_{\theta}(x_i \mid T)) \right]$$

其中 $f_\theta$ 为神经网络，$T$ 为任务条件标记，$\mathcal{D}$ 为逐像素交叉熵（Equation 1, Section 3.2）。

### 视觉表示：画布增强与空间先验

VARC 引入**基于画布的连续嵌入机制**，取代了将二维网格展平为离散令牌序列的传统做法。具体而言，原始输入经过随机缩放和平移后，被置于固定尺寸（如 64×64）的画布上，画布背景填充额外的背景颜色令牌（Figure 4, Section 3.3）。这一设计带来了两个关键增益：

- **平移不变性**：完全灵活的平移增强相比“单像素”增强额外贡献 **2.9 个百分点**（Figure 7(e)）。
- **尺度不变性**：缩放增强单独贡献 **6.2 个百分点**（Figure 7(f)），表明尺度泛化是 ARC 任务的核心视觉瓶颈。

消融实验进一步揭示，累积添加视觉先验（2D 位置嵌入、补丁化、平移和缩放增强）使准确率从 26.8% 提升至 54.5%，总提升达 **27.7 个百分点**，其中画布相关设计贡献 **11.5 个百分点**（Figure 7）。

### 骨干网络：视觉 Transformer 替代循环/语言模型

VARC 采用标准 **Vision Transformer (ViT)** 或卷积 **U-Net** 作为骨干网络，替代了循环网络或 Transformer 解码器（Figure 5, Table 1）。ViT 使用 2D RoPE 位置编码处理画布补丁，相比 1D RoPE 提升 **3.5 个百分点**（Figure 7）。在参数规模 6M–18M 范围内，ViT 表现出良好的可扩展性；U-Net 也可达到 48.3% 的准确率，验证了该问题可通过经典视觉主干解决（Table 1）。

### 训练策略：离线训练 + 独立测试时训练

VARC 采用**两阶段训练范式**（Section 3.4）：
1. **离线训练**：在所有训练任务上学习任务条件化映射，使用 RE-ARC 数据扩展可大幅提高准确率（Figure 14）。
2. **测试时训练 (TTT)**：对每个未见任务，利用少量演示对进行独立微调，辅以翻转、旋转、颜色置换的辅助任务增强（Section 3.4, A.2）。

关键发现是，**独立 TTT 比联合所有测试任务训练高出约 10 个百分点**（Figure 9），表明针对每个任务的特化适配优于跨任务共享信息。

### 推理方式：前馈单次推理 + 多视图集成

VARC 摒弃了自回归生成或递归迭代，采用**前馈单次推理**：模型一次前向传播即输出完整预测。为提升鲁棒性，引入**多视图推理与投票**机制：生成多个随机视图的预测，通过多数投票保留 Top-2 最可能的输出用于 pass@2 评估。多视图推理将 pass@1 准确率从 35.9% 提升至 49.8%，并通过 Top-2 选择实现 54.5% 的 pass@2（Table 2, Section 5.2）。

### 与 baseline 的本质差异

| 维度 | 现有方法 | VARC |
|------|---------|------|
| 任务范式 | 语言序列生成 / 递归推理 | 图像到图像翻译（逐像素分类） |
| 视觉表示 | 离散令牌序列 | 画布连续嵌入 + 平移/缩放增强 |
| 骨干网络 | 循环网络 / LLM 解码器 | ViT / U-Net + 2D RoPE |
| 训练策略 | 大规模预训练或从零训练 | 离线训练 + 独立 TTT |
| 推理方式 | 自回归生成 / 递归迭代 | 前馈单次推理 + 多视图集成 |

这些创新使 VARC 以仅 **18M 参数**（远小于数十亿参数的 LLM）在 ARC-1 上达到 **54.5%** 的单模型准确率，超越从零训练的循环方法 TRM（44.6%），集成后达到 **60.4%**，与人类平均水平（60.2%）持平（Table 3）。值得注意的是，VARC 仅使用 ARC 数据和 RE-ARC 扩充进行训练，未利用互联网规模预训练数据，确保了对比的公平性。

## 整体框架

VARC 将 ARC 基准重构为**图像到图像翻译**问题，以逐像素分类的形式进行建模，类似于语义分割任务。整个 pipeline 由离线训练和测试时训练两个阶段构成，核心模块包括输入预处理、视觉主干网络、任务条件化以及多视图推理。

### 输入预处理与画布增强

原始 ARC 网格首先经过**随机缩放和平移变换**，然后被放置在一个固定尺寸的画布上（默认 64×64）。画布额外引入背景颜色和边缘令牌，以保持输出形状信息（Figure 4、Figure 13）。这一设计使得模型能够在统一的连续空间上处理不同尺寸和位置的输入，为后续的尺度不变性和平移不变性学习提供了基础。

### 像素嵌入与位置编码

离散的颜色索引被映射为可学习的连续嵌入向量。画布上的图像随后被划分为补丁（patch），并注入**2D RoPE 位置编码**，以保留二维空间结构。这与传统方法将 ARC 网格视为一维 token 序列的做法形成根本区别——2D 位置编码是视觉先验的核心组成部分，消融实验中单独贡献了 3.5 个百分点的提升（Figure 7）。

### 视觉主干网络

VARC 采用标准的**视觉 Transformer** 或**卷积 U-Net** 作为骨干网络。ViT 将补丁化后的画布视为自然图像进行处理，通过多层自注意力机制捕获像素间的空间依赖关系。U-Net 同样能够达到可观的准确率（48.3%），验证了该问题本质上可通过经典视觉主干解决（Table 1）。默认配置为 18M 参数的 ViT，在参数规模 6M–18M 范围内表现出良好的可扩展性，但过大模型（66M）会出现过拟合（Figure 8）。

### 任务条件化

每个 ARC 任务被赋予一个可学习的**任务嵌入向量**，作为条件输入调节模型行为。在训练阶段，模型学习将任务嵌入与视觉特征相结合；在推理阶段，未见任务通过测试时训练获得专属的任务嵌入。t-SNE 可视化显示，学到的任务嵌入在语义空间中有意义地聚集，反映出任务间的结构相似性（Figure 12）。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/015_Figure_12.jpg]]
*Figure 12: t-SNE of task embeddings, on the 400 task tokens learned from the ARC-1 training set. Each point represents a single task. To aid the reader, we provide human-written descriptions for the tasks (which are not used in any form by our method)*

### 测试时训练

对于每个未见过的测试任务，VARC 利用少量演示对进行**独立的测试时训练**。训练过程中，通过翻转、旋转（90°、180°、270°）和颜色置换等增强策略，将单个任务扩展为多个辅助任务，以提升泛化能力。消融实验表明，独立测试时训练比联合所有测试任务训练高出约 10 个百分点（Figure 9）。

### 多视图推理与投票

推理阶段生成多个随机视图的预测结果，通过**多数投票**保留前 2 个最可能的输出，用于 pass@2 评估。多视图推理将 pass@1 准确率从 35.9% 提升至 49.8%，最终实现 54.5% 的 pass@2（Table 2）。集成 ViT-18M 和 U-Net-55M 后，pass@2 进一步提升至 60.4%，超越人类平均水平（60.2%）（Table 3）。

### 训练目标

整体训练目标为期望逐像素交叉熵损失：

$$\mathcal{L}(\theta) = \mathbb{E}_{T,i} \left[ \mathcal{D}(y_i, f_{\theta}(x_i \mid T)) \right]$$

其中 $f_{\theta}$ 为以任务 $T$ 为条件的神经网络，$\mathcal{D}$ 为模型输出与真实标签 $y_i$ 之间的逐像素交叉熵损失。该目标在离线训练阶段对所有训练任务进行优化，在测试时训练阶段对单个未见任务进行微调。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/001_Figure_1.jpg]]
*Figure 1: The ARC benchmark (top) consists of a collection of many different tasks, where each task has a few (e.g., 2-4) examples. We propose the Vision ARC (VARC) framework, which addresses the ARC problem as an image-to-image translation problem, from a computer vision perspective (bottom). In this illustration, the underlying concepts of the three tasks can be roughly described by humans as: “reflection” (left), “symmetry” (middle), and “gravity” (right). These concepts are closely related to the visual and physical world*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/005_Figure_5.jpg]]
*Figure 5: The ViT architecture in VARC. The input is randomly placed on a canvas, which is then treated as a natural image and processed by a standard ViT, conditioned on the task token*

## 核心模块与公式推导

VARC 将 ARC 推理任务重构为图像到图像的逐像素分类问题，其核心架构由五个关键模块串联构成，整体遵循“预处理→嵌入→编码→条件调节→分类”的流水线设计。

**输入预处理与画布增强。** 原始输入网格首先经过随机缩放和平移变换，被放置于一个固定尺寸的画布（默认为 64×64）上。画布引入了额外的背景颜色令牌 [BG] 填充空白区域，以及边界令牌 [BD] 指示输出形状。这一设计使模型天然获得平移和尺度不变性的归纳偏置，是后续所有视觉先验的基础。消融实验表明，画布相关的设计（2D 位置编码、灵活平移增强、缩放增强）累计贡献了 11.5 个百分点的准确率提升（Figure 7，c→f），其中缩放增强单独带来 6.2 个点的显著增益（Figure 7f）。

**像素嵌入。** 画布上的每个像素（离散颜色索引共 C 类，加上背景和边界令牌）被映射为可学习的连续嵌入向量。这一步骤将离散的符号化网格转化为视觉模型可处理的连续表示。

**ViT 编码器（或 U-Net）。** 嵌入后的画布被划分为补丁（patch），送入标准视觉 Transformer 处理。编码器采用 2D 旋转位置编码（2D RoPE）替代传统的 1D 位置编码，以保留网格的空间结构信息。消融实验显示，2D RoPE 相比 1D RoPE 在 ViT-18M 上提升了 3.5 个百分点。除 ViT 外，卷积 U-Net 也可作为视觉骨干，在相似参数量下达到 48.3% 的准确率（Table 1），验证了该问题可通过经典视觉主干解决。

**任务条件标记。** 每个训练任务被分配一个可学习的任务嵌入向量，作为条件信息注入网络。该嵌入在离线训练阶段与模型参数联合学习，使模型能够区分不同任务的转换规则。t-SNE 可视化（Figure 12）显示，学到的任务嵌入在语义上呈现出合理的聚类结构。

**分类头。** 编码器输出的逐像素特征通过分类头映射为 C+2 类（C 种颜色 + 背景 + 边界）的概率分布，完成逐像素预测。

**核心损失函数。** 整体训练目标为逐像素交叉熵损失的期望，形式化定义为：

$$\mathcal{L}(\theta) = \mathbb{E}_{T,i} \left[ \mathcal{D}(y_i, f_{\theta}(x_i \mid T)) \right]$$

其中 $T$ 表示任务，$i$ 表示样本索引，$x_i$ 为输入图像，$y_i$ 为真实标签，$f_{\theta}(x_i \mid T)$ 为以任务 $T$ 为条件的网络输出，$\mathcal{D}$ 为逐像素交叉熵损失。该损失同时应用于离线训练阶段和测试时训练（TTT）阶段。

**测试时训练模块。** 对于未见过的测试任务，VARC 在推理前先用少量演示对进行微调。TTT 阶段通过翻转、旋转（90°、180°、270°）和颜色置换将单个任务扩充为多个辅助任务，同时继续应用平移和缩放增强。实验表明，独立对每个测试任务进行 TTT 比联合所有测试任务训练高出约 10 个百分点（Figure 9），说明任务特异性微调对泛化至关重要。

**多视图推理与投票。** 推理时，模型对同一输入生成多个随机视图的预测，通过多数投票保留前 2 个最可能的输出用于 pass@2 评估。多视图推理将 pass@1 准确率从 35.9% 提升至 49.8%，最终实现 54.5% 的 pass@2 准确率（Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/004_Figure_4.jpg]]
*Figure 4: The raw input undergoes random scale and translation transformations and is placed on the “canvas” (denoted in gray)*

## 实验与分析

### 核心实验结果

VARC 在 ARC-1 基准上取得了与人类平均水平相当的准确率。如 **Table 3** 所示，单个 18M 参数的 ViT 模型在 pass@2 评估下达到 **54.5%** 的准确率（四次运行均值 ± 标准差为 54.5±0.7），显著超越了同样从零训练的循环方法 TRM（44.6%）和 HRM（40.3%）。通过集成一个 18M ViT 和一个 55M U-Net，并对每个模型执行四次测试时训练，VARC 的集成准确率进一步提升至 **60.4%**，不仅大幅领先所有从零训练的基线方法，还超越了 GPT-5（44.0%）等大型语言模型，并略微超过人类平均水平（60.2%）。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/011_Table_3.jpg]]
*Table 3: System-level comparisons on the ARC-1 and ARC-2 benchmarks. LLM-based results are from the ARC-AGI leaderboard [18]. HRM, TRM, and our VARC are trained from scratch only on ARC data. Our single-model result is based on ViT, with mean±std of 54.5±0.7 (ARC-1) and 8.3±0.4 (ARC-2) over four runs. Our ensemble result aggregates an 18M ViT and a 55M U-Net, each with test-time training performed four times*

在更具挑战性的 ARC-2 基准上，VARC 同样展现出优势：单模型达到 8.3%，集成模型达到 11.1%，均优于 TRM（7.8%）和 HRM（5.0%）。这一结果表明，将 ARC 重构为图像到图像翻译问题，使标准视觉模型能够从少量视觉示例中抽象出通用的转换规则，而无需依赖大规模语言预训练或显式符号推理。

### 视觉先验的消融分析

**Figure 7** 系统性地揭示了视觉先验对模型性能的累积贡献。从一个朴素的基线（仅使用 1D 位置嵌入和 1×1 补丁，准确率 26.8%）出发，逐步添加视觉先验带来了总计 **27.7 个百分点**的提升，最终达到 54.5%。具体而言：

- **补丁化与画布引入**（c→d）：将补丁大小从 1×1 扩展到 2×2，并将画布从 32×32 扩展到 64×64，带来了基础性的结构改进。
- **2D RoPE 位置编码**：相比 1D RoPE，2D RoPE 在 ViT-18M 上单独贡献了约 **3.5 个百分点**的提升，验证了二维空间感知对 ARC 任务的重要性。
- **平移增强**（e）：在画布上应用完全灵活的平移增强，相比“单像素”增强额外提升了 **2.9 个百分点**（从 45.4 到 48.3）。
- **缩放增强**（f）：缩放增强单独贡献了 **6.2 个百分点**的提升，是单个先验中增益最大的组件，表明尺度不变性对任务泛化至关重要。

综合来看，基于画布的设计（2D RoPE、平移、缩放）累计贡献了 **11.5 个百分点**的提升（c→f），证明了视觉归纳偏置是 ARC 任务求解的核心瓶颈。

### 视觉主干对比与可扩展性

**Table 1** 对比了 ViT 与 U-Net 两种视觉主干在相似参数量下的表现。ViT 系列一致优于 U-Net，但 U-Net 也能达到 48.3% 的可观准确率，这验证了 ARC 问题确实可以通过经典视觉主干来解决，而非必须依赖循环或语言模型。

**Figure 8** 展示了 ViT 在 6M 至 18M 参数范围内的可扩展性：随着宽度和深度的增加，模型性能持续提升，表现出良好的可扩展性。然而，当模型规模扩大到 66M 时，出现了过拟合现象——训练准确率继续上升，但评估准确率反而下降。这表明当前训练策略在泛化性上存在瓶颈，需要进一步研究正则化或数据增强方法以支持更大模型的有效训练。

### 测试时训练策略分析

**Figure 9** 对比了不同的测试时训练策略。独立测试时训练（每个测试任务单独微调）比联合训练（将所有测试任务合并训练）高出约 **10 个百分点**。这一反直觉的结果表明，ARC 任务之间的差异性极大，联合训练可能导致任务间的负迁移，而独立微调使模型能够针对每个任务的特定规则进行专门化适应。

### 多视图推理的贡献

**Table 2** 量化了多视图推理对性能的贡献。单视图推理的 pass@1 准确率仅为 35.9%，而通过生成多个随机视图（包含不同的画布位置、缩放和增强）并进行多数投票，多视图推理将 pass@1 提升至 **49.8%**（提升 13.9 个百分点）。进一步保留投票中前 2 个最可能的输出用于 pass@2 评估，最终达到 54.5%。这一结果表明，多视图集成是弥补单次前馈推理不确定性的有效手段，但也暴露了模型在单视图上的根本推理能力仍有较大提升空间。

### 数据规模与多样性的影响

**Figure 14** 显示，使用 RE-ARC 数据扩展离线训练可大幅提高准确率，但收益呈递减趋势——随着每个任务的合成样本数量增加，性能增益逐渐饱和。**Figure 15** 则表明，增加训练任务的多样性比单纯增加每个任务的样本数量更为有效，任务多样性的提升带来了显著的泛化能力改善。

### 失败模式与局限性

尽管 VARC 取得了显著进展，但分析揭示了若干关键失败模式：

1. **简单任务的意外失败**：部分对人类极为简单的任务（如基本的对称或填充操作）仍会被模型错误求解，表明模型的视觉推理能力与人类之间仍存在本质差距。

2. **歧义任务的处理困境**：如 **Figure 19** 所示，当任务存在多种合理解释时（例如，蓝色线条“接触”红色矩形是否应将其变为蓝色），模型的多视图投票可能产生不可靠的猜测，而非进行真正的推理。

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/026_Figure_19.jpg]]
*Figure 19: Ambiguous examples. Although most ARC tasks are unambiguous, some may admit multiple plausible explanations or rules. Here, in the given three demonstration examples of a test task (top panel), it is unclear whether a blue line “touching” (but not “going through”) a red rectangle should render that rectangle blue. The inference example (bottom panel) involves this situation (“touching”), and our model attempts to interpret the rule as either “going-through-only” (attempt 1) or “touching” (attempt 2)*

3. **大模型过拟合**：66M 参数的 ViT 出现明显的过拟合，限制了通过扩大模型规模进一步提升性能的路径。

4. **增强策略的局限性**：当前方法依赖手工设计的增强策略（翻转、旋转、颜色置换），可能无法覆盖所有可能的任务变换类型，限制了模型对更复杂变换的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/008_Figure_7.jpg]]
*Figure 7: Effects of visual priors in VARC. Accuracy is reported on the ARC-1 evaluation set. The model used is ViT-18M. Entries (a-c) use a patch size of 1×1 on a 32×32 canvas, whereas entries (d-f) use a patch size of 2×2 on a 64×64 canvas. Each entry modifies the one above it. We start from a na¨ıve baseline with components (b-f) removed. These vision priors cumulatively yield 27.7 improvement (a→f), in which the canvas-based designs (c→f) contribute an 11.5 gain*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/007_Table_1.jpg]]
*Table 1: Vision backbones. We compare variants of ViTs and U-Nets of similar sizes. U-Net settings are in appendix*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/012_Table_2.jpg]]
*Table 2: Single-view vs. multi-view inference*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/009_Figure_8.jpg]]
*Figure 8: Scalability: ViTs with different width (x-axis) and depth. The circle areas denote model sizes*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/010_Figure_9.jpg]]
*Figure 9: TTT strategies: with vs. without offline training, and joint vs. independent for each task*

![[assets/figures/papers/paper_list_l18_https_arxiv_org_abs_2511_14761/figures/024_Figure_17.jpg]]
*Figure 17: Successful and failed examples on ARC-1. (Top): Examples of test tasks successfully solved by VARC. (Bottom): Examples of test tasks unsolved by VARC. (Left): Two demonstration example pairs shown for each task (some have more demonstrations not shown here). (Right): Inference input and the first and second solutions proposed by VARC. The green box indicates the correct output*

## 方法谱系与知识库定位

### 任务范式谱系：从符号推理到视觉翻译

ARC 基准自提出以来，主导方法长期围绕离散符号推理和语言模型展开。早期尝试将 ARC 网格视为 token 序列，利用循环网络或 Transformer 解码器进行自回归生成。**HRM**（Wang et al., arXiv 2025）和 **TRM** 代表了从零训练的循环推理路线，在 ARC-1 上分别达到 40.3% 和 44.6% 的 pass@2 准确率。另一条路线以大规模语言模型为核心，包括 GPT-5、o3-mini-high、Deepseek R1、Claude 3.7、Grok-4 等，这些模型依赖互联网规模预训练注入的通用知识，在 ARC-1 上最高达到 44.0%（GPT-5）。**ViT-ARC**（Li et al., 2024）曾尝试直接使用视觉模型，但仅拟合训练任务而无法泛化，验证了单纯替换骨干而不引入视觉先验的无效性。

VARC 的根本性转变在于将 ARC 从“序列生成问题”重构为“图像到图像翻译问题”——具体化为逐像素分类，与语义分割范式对齐。这一重构使得标准视觉模型（ViT/U-Net）能够直接利用 2D 空间结构，而无需将网格展平为离散 token 序列。核心差异体现在五个关键维度：

| 维度 | 语言/循环路线 | VARC 视觉路线 |
|------|-------------|-------------|
| 任务范式 | 语言序列生成或递归推理 | 图像到图像翻译（逐像素分类） |
| 视觉表示 | 二维网格作为离散 token 序列 | 基于画布的连续嵌入 + 平移/缩放增强 |
| 骨干网络 | 循环网络或 Transformer 解码器（LLM） | 视觉 Transformer（ViT）或卷积 U-Net |
| 训练策略 | 大规模预训练（LLM）或从零训练（循环模型） | 两阶段：离线训练 + 测试时训练（TTT） |
| 推理方式 | 自回归生成或递归迭代 | 前馈单次推理 + 多视图集成 |

### 关键设计决策的因果机制

VARC 的性能优势并非源于模型规模或数据量——其 ViT-18M 仅含 18M 参数，且仅使用 ARC 数据和 RE-ARC 扩充进行训练，未利用任何互联网预训练数据。决定性因素在于**视觉先验的累积注入**：

1. **2D 位置编码（2D RoPE）**：相比 1D RoPE，2D RoPE 单独提升 3.5 个百分点。这直接源于 ARC 任务的空间本质——反射、对称、重力等概念天然存在于 2D 邻域关系中，1D 序列化会破坏这种结构。

2. **画布机制与平移增强**：固定尺寸画布（64×64）配合灵活平移增强，贡献 2.9 个点。画布使得模型能够在统一的坐标空间中处理不同位置的输入，隐式学习平移不变性。

3. **缩放增强**：单独贡献 6.2 个百分点，是所有消融项中收益最大的单因素。这表明尺度不变性对任务泛化至关重要——同一变换规则可能作用于不同大小的对象，模型必须从少量演示中抽象出尺度无关的规律。

4. **补丁化（Patchification）**：将 1×1 像素补丁切换为 2×2 补丁，配合 64×64 画布，进一步贡献显著提升。补丁化降低了计算复杂度，同时引入了局部空间聚合的归纳偏置。

累积效果惊人：从朴素基线（26.8%）到完整模型（54.5%），视觉先验贡献了 27.7 个百分点的提升，其中画布相关设计（2D RoPE、平移、缩放）合计贡献 11.5 个点。

### 测试时训练的策略边界

VARC 采用独立的测试时训练（TTT）策略——每个测试任务单独微调，而非将所有测试任务联合训练。消融实验揭示了一个反直觉的发现：独立 TTT 比联合 TTT 高出约 10 个百分点。这表明 ARC 任务之间的差异性远大于共性，联合训练可能引入任务间的干扰，而独立 TTT 允许模型针对每个任务的特定变换规则进行专门化适应。

TTT 期间的辅助任务增强（翻转、旋转、颜色置换）是关键的泛化机制。这些增强将单个演示任务扩展为多个变体，使模型能够从有限示例中学习变换的不变性。但这也暴露了当前方法的边界：增强策略是手工设计的，可能无法覆盖所有可能的任务变换类型。

### 适用边界与已知局限

**模型规模瓶颈**：ViT 在 6M-18M 参数范围内表现出良好的可扩展性，但 66M 模型出现过拟合，准确率反而下降。这表明当前训练策略在泛化性上存在根本瓶颈——更大的模型倾向于记忆训练任务而非学习可迁移的视觉推理能力。

**单视图推理能力不足**：单视图 pass@1 准确率仅为 35.9%，依赖多视图集成（510 个视图）才提升至 49.8%（pass@1）和 54.5%（pass@2）。这揭示了一个深层问题：模型在单次推理中尚未形成稳定的空间推理能力，多视图投票本质上是对不确定性的一种补偿机制。

**对人类简单任务的失败**：VARC 在部分对人类直观简单的任务上仍会出错。Figure 17 和 Figure 18 展示了成功与失败案例的对比，表明视觉推理能力与人类水平之间仍有质的差距。

**歧义任务的处理缺陷**：当任务存在多种合理解释时（Figure 19 展示的“接触”vs“穿过”歧义），模型的多视图投票可能产生不可靠的猜测，缺乏对歧义进行显式建模和不确定性量化的机制。

### 未探索路径与开放问题

1. **视觉-语言融合**：当前方法完全摒弃语言信息，但 ARC 任务的空间变换规则往往可以用自然语言简洁描述（如“反射”“对称”“重力”）。如何将视觉驱动的模式学习与语言驱动的概念理解结合，是一个根本性的开放问题。

2. **大规模视觉预训练的迁移**：VARC 刻意避开了 ImageNet 等大规模图像预训练，以证明纯 ARC 数据训练的可行性。但自然图像中蕴含的丰富视觉常识（物体恒常性、光照不变性、三维几何等）是否能够迁移到抽象推理任务，尚未被探索。

3. **过拟合的机制性解决**：66M 模型的过拟合问题表明，当前的正则化和训练策略不足以约束大模型。需要研究专门针对少样本跨任务泛化的正则化技术，而非依赖模型规模限制作为隐式正则。

4. **测试时训练的效率**：TTT 对每个测试任务独立微调，计算成本随任务数量线性增长。能否通过元学习或参数高效微调（如 LoRA）降低 TTT 成本，同时保持独立训练的泛化优势？

5. **歧义的显式建模**：对于存在多种合理解释的任务，当前方法缺乏对歧义的显式表征。引入概率推理或生成式建模（如扩散模型）来捕捉输出分布的多模态性，可能是一个有前景的方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/ARC_Is_a_Vision_Problem.pdf]]