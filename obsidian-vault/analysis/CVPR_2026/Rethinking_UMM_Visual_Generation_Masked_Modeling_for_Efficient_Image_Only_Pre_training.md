---
title: "Rethinking UMM Visual Generation: Masked Modeling for Efficient Image-Only Pre-training"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Rethinking_UMM_Visual_Generation_Masked_Modeling_for_Efficient_Image_Only_Pre_training.pdf
project_link: null
code_link: "https://github.com/LINs-lab/IOMM"
aliases:
- IIOTU
- RUVGMMEIOPT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用纯图像自条件预训练与掩码图像建模，使模型在无配对文本的条件下习得强大的视觉生成先验；第二阶段通过混合纯图像与少量配对数据的微调，以极低的成本恢复并提升指令对齐能力。
primary_logic: 将文本条件替换为“辅助提示 + 图像patch”的自条件信号，并引入掩码图像建模将预训练转化为稀疏到密集的重建任务，从而迫使模型学习场景和物体的组合式视觉表示，彻底摆脱对图文对数据的依赖。
claims:
- IOMM-B (512) 仅使用公开数据集，在 GenEval 上达到 0.89，超越使用额外 30M 专有数据的 BLIP3-o-8B* (0.84) 和 BAGEL-7B (0.88)。
- 图像纯预训练 + 混合数据微调的组合在六种训练配方中获得最高 GenEval 分数 0.89。
- 消融实验证实残差查询适配器、掩码图像建模以及混合微调均能显著提升生成质量。
- 纯图像预训练模型在零样本图像编辑基准 ImgEdit-Bench 上超过图文对预训练模型（整体 2.82 vs. 2.61）。
---

# Rethinking UMM Visual Generation: Masked Modeling for Efficient Image-Only Pre-training

> [!tip] 核心洞察
> 将文本条件替换为“辅助提示 + 图像patch”的自条件信号，并引入掩码图像建模将预训练转化为稀疏到密集的重建任务，从而迫使模型学习场景和物体的组合式视觉表示，彻底摆脱对图文对数据的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | 重新思考UMM视觉生成：用于高效纯图像预训练的掩码建模 |
| 英文题名 | Rethinking UMM Visual Generation: Masked Modeling for Efficient Image-Only Pre-training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16139) · [Code](https://github.com/LINs-lab/IOMM) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | IOMM (Image-Only Training for UMMs) |
| Dataset | GenEval, WISE, DPGBench |

> [!tip] 效果简介
> - GenEval 上，Overall (↑) 0.89 vs BAGEL-7B: 0.88; BLIP3-o-8B*: 0.84 (+0.01 / +0.05)。
> - WISE 上，Overall (↑) 0.55 vs MetaQuery-XL: 0.55; BAGEL-7B: 0.52 (持平 / +0.03)。
> - DPGBench 上，Overall (↑) 82.95 vs BLIP3-o-8B*: 81.60; Janus-Pro-7B: 84.19 (+1.35 / -1.24)。

## 概述

当前统一多模态模型（UMM）的视觉生成预训练面临一个根本性瓶颈：严重依赖高质量文本-图像配对数据，而此类数据稀缺且获取成本高昂。同时，现有训练范式效率低下，导致模型在有限数据条件下难以生成与文本指令忠实对齐的图像。

本文提出 **IOMM (Image-Only Training for UMMs)**，一种数据高效的两阶段训练框架。其核心洞察在于：将文本条件替换为由“辅助提示 + 图像patch”构成的自条件信号，并引入掩码图像建模将预训练转化为稀疏到密集的重建任务，从而迫使模型学习场景和物体的组合式视觉表示，彻底摆脱对图文对数据的依赖。具体而言，第一阶段仅利用无标签纯图像数据进行预训练，使模型习得强大的视觉生成先验；第二阶段通过混合纯图像与少量配对数据的微调，以极低的成本恢复并提升指令对齐能力。

在关键性能指标上，**IOMM-B (3.6B)** 仅使用公开数据集，在 GenEval 上达到 **0.89**，超越使用额外 30M 专有数据的 BLIP3-o-8B* (0.84) 和 BAGEL-7B (0.88)；在 WISE 上达到 0.55，与 MetaQuery-XL 持平并优于 BAGEL-7B (0.52)。总训练成本约 1050 H800 GPU 小时，其中 1000 小时用于高效的纯图像预训练，远低于许多大型 UMM。

消融实验进一步证实，残差查询适配器（RQA）、掩码图像建模以及混合数据微调三个关键设计均对生成质量有显著正向贡献。此外，纯图像预训练模型在零样本图像编辑基准 ImgEdit-Bench 上超过图文对预训练模型（整体 2.82 vs. 2.61），展现出更强的视觉先验迁移能力。

## 背景与动机

### 统一多模态视觉生成的瓶颈

统一多模态模型（UMM）旨在以单一架构同时处理理解与生成任务，但在视觉生成方面长期面临一个根本性瓶颈：**高质量文本-图像配对数据的稀缺与高昂获取成本**。当前领先的 UMM 视觉生成方案——无论是原生统一模型（如 **BAGEL-7B**、**BLIP3-o-8B**、**MetaQuery-XL**）还是基于扩散骨干的架构——其预训练阶段均严重依赖大规模图文对数据。例如，BLIP3-o-8B 额外使用了 30M 专有图像-文本对才在 GenEval 上达到 0.84 的综合得分（Table 1）。这类配对数据不仅采集和标注成本极高，且其规模远无法与互联网上近乎无限的纯图像数据相提并论，构成了 UMM 生成能力扩展的核心制约因素。

与此同时，现有训练范式在**数据效率**上表现低下。在图文对数据有限的情况下，模型难以习得足够的视觉组合先验，导致生成图像与文本指令的忠实对齐能力不足——具体表现为物体属性错误、空间关系混乱、多物体组合失败等典型失败模式。这一问题在 GenEval、DPGBench 等细粒度指令遵循基准上尤为突出。

### 核心洞察：以自条件替代文本条件

本文的核心洞察在于一个关键追问：**视觉生成预训练是否必须依赖配对文本？** 答案是否定的。如果将文本条件替换为一种从图像自身派生的“自条件信号”（self-conditioning signal），并设计一种迫使模型学习组合式视觉表示的预训练任务，那么纯图像数据就足以驱动强大的视觉生成先验学习。

具体而言，IOMM 采用**“辅助提示 + 图像 patch 嵌入”**拼接作为条件序列，替代传统图文对中的文本描述，从而构成自条件信号。同时，引入**掩码图像建模（Masked Image Modeling）**将预训练转化为稀疏到密集的重建任务：随机掩码部分图像 patch，迫使扩散模型在仅观测未掩码区域的条件下重建完整图像。这一机制有效地阻止了模型学习恒等映射，转而迫使它理解场景中物体之间的组合关系与空间结构，从而在无任何配对文本的情况下习得结构化的视觉生成先验。

### 两阶段高效训练范式

基于上述洞察，IOMM 提出了一个**数据高效的两阶段训练框架**：

- **第一阶段（纯图像预训练）**：利用冻结的多模态大语言模型（MLLM，如 InternVL3-2B）作为特征提取器，在纯图像数据上训练视觉生成组件（基于 FLUX 的 Multi-Modal DiT 架构）。此阶段完全不需要配对文本，仅依赖海量无标签图像数据，训练成本极低——IOMM-B 的预训练仅需约 1000 H800 GPU 小时。
- **第二阶段（混合数据微调）**：在少量图文对数据与纯图像数据的混合集上进行微调，以极低的成本恢复并提升指令对齐能力。实验表明，这一混合策略在多个开源 UMM（如 OpenUni-L、Qwen-Image）上均能一致提升生成质量（Table 2），验证了其通用性。

这一范式的核心优势在于：**将昂贵的文本监督推迟到微调阶段，使预训练的数据瓶颈被彻底打破**，同时通过掩码建模确保纯图像预训练的质量不降级。后续章节将详细展开各模块的设计与实验验证。

## 核心创新

IOMM 的核心创新在于**彻底解耦视觉生成预训练与文本-图像配对数据的依赖**，通过三条相互咬合的设计线，将统一多模态模型的生成训练从高成本的数据瓶颈中解放出来。

### 1. 自条件信号替代文本条件

传统 UMM 的视觉生成预训练以文本-图像对为输入，文本充当生成条件。IOMM 将这一范式替换为**纯图像自条件（self-conditioning）**：条件序列由固定的辅助提示词嵌入与图像 patch 嵌入拼接而成：

$$c = \mathrm{concat}(c_{\mathrm{aux}}, c_{\mathrm{img}}) \in \mathbb{R}^{(T+P^2) \times D}$$

其中 $c_{\mathrm{aux}}$ 是一组固定的通用辅助提示词嵌入，$c_{\mathrm{img}}$ 是 ViT 编码器从输入图像提取的 patch 嵌入。这一替换的因果效应是直接切断了预训练对配对文本的依赖（changed slot: 预训练数据模态），使模型能够从海量无标签图像数据中学习视觉生成先验。

### 2. 掩码图像建模阻止恒等映射坍塌

纯图像自条件存在一个关键风险：模型可能学会简单的恒等映射（直接将输入图像复制到输出），而非学习有意义的生成能力。IOMM 通过引入**掩码图像建模（Masked Image Modeling）** 解决这一问题（changed slot: 防止恒等映射的机制）。具体而言，对图像 patch 嵌入施加随机掩码：

$$\mathbf{c}_{\mathrm{img}} \gets \mathbf{c}_{\mathrm{img}} \odot \mathbf{M}$$

其中 $\mathbf{M}$ 是二元掩码矩阵，掩码比率 $r \in [0, 1]$。这一操作将训练任务转化为**稀疏到密集的重建**：模型必须从被部分掩码的图像中推断完整场景，从而被迫学习物体组合、场景结构等深层次视觉表示。消融实验证实，掩码比率为 0.45 时获得最佳 GenEval 得分 0.88（Figure 4b）。

### 3. 残差查询适配器精炼条件信号

冻结 MLLM 直接输出的特征用于条件生成时表现次优。IOMM 设计了**残差查询适配器（Residual Query Adapter, RQA）**，一个仅含 29M 参数的轻量模块（changed slot: MLLM 适配方式）。RQA 使用 256 个可学习查询标记，通过交叉注意力对条件序列进行任务特定变换，生成残差查询并附加到原始条件序列：

$$\mathbf{c} \gets \mathrm{concat}(\mathbf{c}, \mathbf{q}_{\theta}(\mathbf{c}))$$

移除 RQA 会显著降低 GenEval 得分（Figure 2b），验证了该模块在桥接冻结 MLLM 语义特征与生成任务需求之间的关键作用。

### 4. 混合数据微调解锁指令对齐

纯图像预训练赋予模型强大的视觉先验，但缺乏文本指令跟随能力。IOMM 在第二阶段采用**混合数据微调**（changed slot: 微调数据组成），将图文对数据与纯图像数据混合训练。这一策略在多个开源 UMM 上验证有效：在 OpenUni-L 上，混合微调使 GenEval 从 0.85 升至 0.88，WISE 从 0.52 升至 0.59（Table 2）；在 Qwen-Image 上同样获得一致提升。其因果机制在于：纯图像数据维持预训练阶段习得的视觉先验，图文对数据以极低成本恢复指令对齐能力。

### 创新协同效应

上述四条设计线形成协同闭环：自条件信号使预训练摆脱配对数据依赖 → 掩码建模迫使模型学习组合式视觉表示 → RQA 高效桥接冻结 MLLM 与生成任务 → 混合微调以最小代价恢复指令对齐。最终，仅使用公开数据集的 IOMM-B (512) 在 GenEval 上达到 0.89，超越使用额外 30M 专有数据的 BLIP3-o-8B\* (0.84) 和 BAGEL-7B (0.88)（Table 1），同时总训练成本仅约 1050 H800 GPU 小时。

## 整体框架

IOMM 提出了一种**数据高效的两阶段训练范式**，旨在解决统一多模态模型（UMM）视觉生成预训练对昂贵图文配对数据的重度依赖。其核心思路是：将文本条件替换为“辅助提示 + 图像 patch”的自条件信号，并引入掩码图像建模，使模型在纯图像数据上即可习得强大的视觉生成先验。

整个 pipeline 由以下关键模块构成，数据流如图 2a 所示。

**第一阶段：纯图像预训练（Image-Only Pre-training）**

输入为无标签的纯图像。图像首先经 ViT Encoder 转换为 patch 嵌入序列 $c_{\text{img}}$，与一组固定的辅助提示词嵌入 $c_{\text{aux}}$ 拼接，形成初始条件序列：

$$c = \mathrm{concat}(c_{\mathrm{aux}}, c_{\mathrm{img}}) \in \mathbb{R}^{(T+P^2) \times D}$$

该条件序列随即进入一个**轻量残差查询适配器（Residual Query Adapter, RQA）**。RQA 仅含 29M 参数，通过交叉注意力机制利用 256 个可学习查询标记对条件信号进行任务特异性精炼，并将生成的残差查询附加回原序列：

$$c \gets \mathrm{concat}(c, q_\theta(c))$$

精炼后的条件序列被送入一个**冻结的多模态大语言模型（Frozen MLLM）**——具体实现为 InternVL3-2B——作为语义特征提取器，输出富含高层语义的条件表示。

为防止自条件学习坍缩为平凡的恒等映射，框架在图像 patch 嵌入上施加**掩码图像建模（Masked Image Modeling）**：以掩码比率 $r$ 随机遮蔽部分图像 patch 标记（$c_{\text{img}} \gets c_{\text{img}} \odot \mathbf{M}$），将训练转化为**稀疏到密集的重建任务**。这一设计迫使扩散骨干网络（基于 FLUX 的 Multi-Modal DiT）在流匹配目标下学习场景和物体的组合式视觉表示：

$$L(\theta) = \mathbb{E}_{x,z,c,t} \left[ \| F_\theta(x_t, t, c) - (z - x) \|_2^2 \right]$$

其中 $x_t = (1 - t) \cdot x + t \cdot z$ 为数据点 $x$ 到噪声 $z$ 的确定性插值路径，推理时通过概率流 ODE $\frac{\mathrm{d} x_t}{\mathrm{d} t} = F_\theta(x_t, t, c)$ 从噪声反向生成样本。

**第二阶段：混合数据微调（Mixed-Data Fine-tuning）**

纯图像预训练完成后，模型在**混合数据**（图文配对数据 + 纯图像数据）上进行微调。此阶段以极低的成本恢复并提升模型的指令对齐能力，同时保留纯图像预训练习得的强视觉先验。消融实验证实，该混合微调策略在多个开源 UMM（如 OpenUni-L、Qwen-Image）上均能一致提升 GenEval 和 WISE 得分。

整体而言，IOMM 通过“纯图像自条件预训练 + 掩码建模 + 混合微调”的组合，彻底摆脱了对大规模图文对数据的依赖，在显著降低数据获取成本的同时，实现了与依赖专有数据的大模型相当甚至更优的文本到图像生成性能。

### 补充图表

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the IOMM framework. (a) The architecture of our proposed framework. (b) Ablation study demonstrating the effectiveness of architectural design choices, confirming that each component contributes positively to the final GenEval score. All variants utilize the same IOMM-XL architecture*

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/001_Figure_1.jpg]]
*Figure 1: An overview and validation of our proposed training paradigm. (a) Visual results of our IOMM-XL, demonstrating high-quality, multi-resolution image synthesis. Corresponding prompts are provided in App. C.7. (b) An illustration of the six training recipes we investigate. (c) Quantitative results of six training recipes on the GenEval benchmark*

## 核心模块与公式推导

### 流匹配生成框架

IOMM 的生成骨干基于流匹配（Flow Matching）范式。其核心目标是训练网络 $F_\theta$ 学习从数据分布到噪声分布的匀速向量场。给定数据样本 $x$ 和高斯噪声 $z \sim \mathcal{N}(0, I)$，训练时的确定性插值路径定义为：

$$x_t = (1 - t) \cdot x + t \cdot z$$

其中 $t \in [0, 1]$ 为时间步。网络通过最小化以下目标函数来学习该向量场：

$$L(\theta) = \mathbb{E}_{x,z,c,t} \left[ \| F_\theta(x_t, t, c) - (z - x) \|_2^2 \right]$$

这里 $c$ 为条件信号，$F_\theta(x_t, t, c)$ 是网络预测的速度场，监督目标 $(z - x)$ 是数据点到噪声的恒定速度向量。推理时，通过求解概率流 ODE 从噪声反向生成样本：

$$\frac{\mathrm{d} x_t}{\mathrm{d} t} = F_\theta(x_t, t, c)$$

该框架直接继承了 FLUX 的 Multi-Modal Diffusion Transformer (MM-DiT) 架构，独立处理图像与文本模态并在注意力层中融合。

---

### 自条件序列构建

纯图像预训练的核心挑战在于：如何在无配对文本的条件下构建有效的条件信号。IOMM 采用“自条件”（self-conditioning）策略，将条件序列 $c$ 构造为辅助提示嵌入与图像 patch 嵌入的拼接：

$$c = \mathrm{concat}(c_{\mathrm{aux}}, c_{\mathrm{img}}) \in \mathbb{R}^{(T+P^2) \times D}$$

其中：
- $c_{\mathrm{aux}}$ 是固定的通用辅助提示词（如 “Generate a high-quality image”）经过冻结 MLLM 编码后的嵌入，长度为 $T$；
- $c_{\mathrm{img}}$ 是输入图像经 ViT Encoder 提取的 patch 嵌入序列，长度为 $P^2$（$P$ 为 patch 网格尺寸）；
- $D$ 为嵌入维度。

该拼接序列随后被送入冻结的 InternVL3-2B MLLM 进行语义编码，生成富含场景理解的条件表示。这一设计使得模型完全摆脱了对文本-图像配对数据的依赖，仅利用纯图像即可习得视觉生成先验。

---

### 残差查询适配器（RQA）

直接将冻结 MLLM 的输出作为条件信号会导致次优性能（消融实验证实，Fig. 2b）。为此，IOMM 引入残差查询适配器（Residual Query Adapter, RQA），记为 $q_\theta$。RQA 是一个轻量级模块（仅 29M 参数），通过交叉注意力机制，使用 256 个可学习的查询标记对条件序列 $c$ 进行任务特定的精炼。其输出以残差方式拼接到原始条件序列：

$$c \gets \mathrm{concat}(c, q_\theta(c))$$

这一设计的关键机制在于：RQA 不修改原始条件，而是生成补充性的“残差查询”标记，使后续的扩散骨干网络能够同时利用原始语义信息和经过适配器精炼的任务导向特征。消融实验表明，移除 RQA 会显著降低 GenEval 得分，验证了该模块的有效性。

---

### 掩码图像建模（MIM）

纯图像自条件训练面临一个根本性风险：模型可能退化为简单的恒等映射，直接复制输入图像而非学习有意义的生成先验。IOMM 通过引入掩码图像建模（Masked Image Modeling）来解决这一问题。

具体而言，在训练时对图像 patch 嵌入 $c_{\mathrm{img}}$ 施加随机掩码。设掩码比率 $r \in [0, 1]$，通过逐元素乘以二值掩码 $\mathbf{M}$ 实现：

$$c_{\mathrm{img}} \gets c_{\mathrm{img}} \odot \mathbf{M}$$

其中 $\mathbf{M}$ 中比例为 $r$ 的元素为 0，其余为 1。这一操作将训练任务转化为稀疏到密集的重建问题：模型仅能观测到部分 patch 的条件信息，必须推断被掩码区域的视觉内容，从而被迫学习场景中物体和布局的组合式表示。

掩码比率的消融实验（Fig. 4b）显示，$r = 0.45$ 时获得最佳 GenEval 得分 0.88 和 DPGBench 得分 79.79，证实适度的信息稀疏性对学习鲁棒的视觉先验至关重要。

---

### 两阶段训练流程

IOMM 的完整训练分为两个阶段，其核心逻辑由上述模块串联实现：

1. **第一阶段（纯图像预训练）**：仅使用无标签图像数据。ViT Encoder 提取 patch 嵌入，与固定辅助提示拼接后经 MIM 随机掩码，通过冻结 MLLM 和 RQA 编码为条件信号，最终由 MM-DiT 骨干网络以流匹配目标进行训练。此阶段迫使模型在无文本监督的条件下习得强大的视觉生成先验。

2. **第二阶段（混合数据微调）**：在纯图像数据中混入少量高质量文本-图像配对数据，以极低成本恢复并提升模型的指令对齐能力。微调时，文本条件替代辅助提示，与图像 patch 共同构成条件序列，其余模块保持不变。

## 实验与分析

### 核心训练配方对比

论文首先通过六种训练配方的系统对比，确立了“纯图像预训练 + 混合数据微调”作为最优范式。如 Table 9 所示，仅使用图文对预训练（Recipe 1）的 GenEval 分数为 0.84；仅使用纯图像预训练而不进行微调（Recipe 2）为 0.82；而将纯图像预训练与混合数据微调结合（Recipe 6）可获得最高分 **0.89**，显著优于其他所有组合。这一结果直接证实了论文的核心因果路径：纯图像预训练提供了强大的视觉生成先验，混合微调则恢复了指令对齐能力，二者缺一不可。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/013_Table_9.jpg]]
*Table 9: Training recipe comparison. The GenEval score of the models pre-trained with different training recipes. Bold denotes the best performance and underline denotes the second best performance*

### 文本到图像生成主结果

IOMM 在多个主流基准上与现有统一多模态模型（UMM）进行了全面对比（Table 1）。在 GenEval 综合指标上，IOMM-B（512px）以 **0.89** 取得最优，超越 **BAGEL-7B**（0.88）和额外使用 30M 专有数据的 **BLIP3-o-8B\***（0.84）。值得注意的是，IOMM-B 仅使用公开数据集，总训练成本约 1050 H800 GPU 小时，其中 1000 小时用于高效的纯图像预训练，远低于许多大型 UMM。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on text-to-image generation benchmarks. The (↑) symbol indicates that higher scores are better. †Results obtained using rewritten prompts from the original GenEval benchmark. ∗Indicates the model was trained on an additional 30M proprietary image-text pairs*

在 WISE 基准上，IOMM-B 达到 0.55，与 **MetaQuery-XL** 持平，优于 BAGEL-7B（0.52）。在 DPGBench 上，IOMM-B 获得 82.95，超过 BLIP3-o-8B\*（81.60），略低于 **Janus-Pro-7B**（84.19）。Table 7 和 Table 8 分别提供了 DPGBench 和 WISE 的细粒度维度评估，展示了 IOMM 在不同子指标上的表现分布。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/011_Table_7.jpg]]
*Table 7: DPGBench evaluation results. Here BLIP3-o-8B* donates the model that is trained with an 30 million proprietary data*

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/012_Table_8.jpg]]
*Table 8: WISE evaluation results. Here BLIP3-o-8B* donates the model that is trained with an 30 million proprietary data*

### 混合微调策略的通用性验证

为验证混合微调策略的普适性，论文将“图文对微调”（Pair）和“混合数据微调”（Mix）应用于两个开源 UMM 基座模型（Table 2）。在 **OpenUni-L** 上，混合微调使 GenEval 从 0.85 提升至 0.88，WISE 从 0.52 提升至 0.59；在 **Qwen-Image** 上，GenEval 从 0.82 提升至 0.84，WISE 从 0.46 提升至 0.50。Figure 6 可视化展示了 OpenUni-L 微调前后的生成结果对比，左侧为原始模型输出，右侧为微调后输出，直观体现了指令遵循能力的提升。这一跨架构验证表明，混合微调并非 IOMM 特有的技巧，而是一种可推广的 UMM 生成能力增强策略。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/004_Table_2.jpg]]
*Table 2: Evaluating different fine-tuning strategies on various open-source UMMs. The notation*

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/017_Figure_6.jpg]]
*Figure 6: Generation results of OpenUni-L before and after finetuning. The left one is the image generated by the original OpenUni-L, while the right one is generated by the OpenUni-L after finetuning*

### 零样本图像编辑能力

Table 3 展示了 ImgEdit-Bench 上的图像编辑结果。IOMM 在**零样本**设置下（未使用任何编辑训练数据）整体得分 **2.82**，显著优于使用图文对预训练的对比模型（2.61）。Figure 5 进一步对比了两种预训练方式在编辑任务上的视觉差异。这一结果揭示了纯图像预训练的一个关键优势：模型在无文本条件下学习到的视觉先验，使其对图像内容的理解和操控能力更强，进而在编辑任务中表现出更好的零样本泛化。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/005_Table_3.jpg]]
*Table 3: Image editing benchmark results. Methods highlighted in red are trained on specific editing datasets. Our IOMM, highlighted in blue , is evaluated in a training-free setting without any training on editing data*

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/015_Figure_5.jpg]]
*Figure 5: Image editing ability with different pre-training method*

### 关键组件消融

**残差查询适配器（RQA）**：Figure 2b 的消融显示，移除 RQA 会明显降低 GenEval 分数。直接使用冻结 MLLM 的原始输出（标记为“Raw”）性能次优，而引入仅 29M 参数的 RQA 模块通过交叉注意力生成残差查询标记，有效精炼了条件信号。

**掩码比率**：Figure 4b 展示了掩码比率对性能的影响。当掩码比率设为 **0.45** 时，模型在 GenEval 上达到 0.88，在 DPGBench 上达到 79.79，均为最优。过高或过低的掩码比率均导致性能下降，表明适度的稀疏性对防止恒等映射坍塌和促进组合式表示学习至关重要。

**微调数据混合比率**：Figure 4c 分析了微调阶段纯图像与图文对数据的混合比例。结果表明，适当的混合比率能够平衡视觉质量与指令对齐，但论文未给出单一最优值，暗示该比率可能需要根据具体下游任务进行调整。

### 模型规模效应

在控制训练 epoch 的条件下，IOMM-L 表现优于 IOMM-B（GenEval 0.87 vs. 0.86），证实模型规模可带来正向增益。然而，论文指出 IOMM-L 因训练资源有限未能充分收敛，其潜力尚未完全体现，这构成了一项明确的实验局限。

### 训练配置概要

Table 4 和 Table 5 分别列出了预训练和微调阶段的超参数设置。IOMM-B 和 IOMM-L 使用 AdamW 优化器，IOMM-XL 使用 Muon 优化器。Table 6 提供了 UMM 微调实验（OpenUni-L、Qwen-Image）的超参数配置。

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/008_Table_4.jpg]]
*Table 4: Pre-training settings*

![[assets/figures/papers/paper_list_l924_https_arxiv_org_abs_2603_16139/figures/009_Table_5.jpg]]
*Table 5: Finetuning settings*

## 方法谱系与知识库定位

### 1. 训练范式：从图文对依赖到纯图像自条件

当前统一多模态模型（UMM）的视觉生成预训练普遍遵循“图文对监督”范式——模型通过文本-图像配对数据学习文本条件到图像的映射。这一范式的根本瓶颈在于**高质量图文对数据的稀缺性与高昂获取成本**，同时现有训练范式高度低效，导致模型在有限数据下难以生成与文本指令忠实对齐的图像。

IOMM 将这一范式彻底翻转：**第一阶段采用纯图像自条件预训练**，使模型在无配对文本的条件下习得强大的视觉生成先验；**第二阶段通过混合纯图像与少量配对数据的微调**，以极低的成本恢复并提升指令对齐能力。这一两阶段框架在 GenEval 上的六种训练配方对比（Table 9）中取得最高分 0.89，验证了其相对于纯图文对训练、纯图像训练等替代方案的决定性优势。

### 2. 关键技术组件与基线对比

**残差查询适配器（RQA）**：传统 UMM 直接使用冻结 MLLM 的输出作为条件信号，但 Fig. 2b 的消融实验表明这种“原始”方案性能次优。RQA 通过交叉注意力引入 256 个可学习查询标记，生成残差查询并附加到条件序列（`c ← concat(c, q_θ(c))`），仅增加 29M 参数便显著提升生成质量。该设计可视为对“冻结大模型 + 轻量适配”路线的延续，但区别于 LoRA 等参数高效微调方案，RQA 直接作用于条件序列而非模型权重。

**掩码图像建模（MIM）**：将文本条件替换为“辅助提示 + 图像 patch”的自条件信号后，若不施加约束，模型将退化为恒等映射。IOMM 引入随机掩码图像 patch（掩码比率 `r ∈ [0,1]`），将训练转化为稀疏到密集的重建任务，迫使模型学习场景和物体的组合式视觉表示。Fig. 4b 显示掩码比率 0.45 时获得最佳 GenEval 0.88 和 DPGBench 79.79，证实 MIM 是防止自条件塌缩的关键机制。

**与 SoTA UMM 的定量对比**：Table 1 显示，IOMM-B (512) 仅使用公开数据集（Megalith-10M、text-to-image-2M 等），在 GenEval 上达到 0.89，超越使用额外 30M 专有数据的 **BLIP3-o-8B\*** (0.84) 和 **BAGEL-7B** (0.88)。在 WISE 上与 **MetaQuery-XL** 持平 (0.55)，在 DPGBench 上 (82.95) 介于 BLIP3-o-8B\* (81.60) 和 **Janus-Pro-7B** (84.19) 之间。总训练成本约 1050 H800 GPU 小时，其中 1000 小时用于高效的纯图像预训练，远低于许多大型 UMM。

### 3. 混合微调的通用性验证

混合数据微调（图文对 + 纯图像）并非 IOMM 专属，而是可迁移的通用策略。Table 2 显示，在 **OpenUni-L** 上应用该策略使 GenEval 由 0.85 升至 0.88，WISE 由 0.52 升至 0.59；在 **Qwen-Image** 上亦获得一致的指令跟随保真度和图像生成质量提升。这表明混合微调可作为一种即插即用的增强手段，适用于多种 UMM 架构。

### 4. 零样本泛化能力

纯图像预训练学到的视觉先验展现出意外的零样本迁移能力。Table 3 显示，IOMM 在未使用任何编辑数据训练的情况下，于 ImgEdit-Bench 上取得整体 2.82 分，超过图文对预训练模型的 2.61 分。Fig. 5 进一步对比了两种预训练方式的图像编辑质量，证实自条件预训练习得的组合式视觉表示对下游编辑任务具有更强的泛化性。

### 5. 适用边界与局限

**模型规模扩展受限**：IOMM-L 在控制训练 epoch 条件下表现优于 IOMM-B（GenEval 0.87 vs. 0.86），证实规模可带来正向增益。但较大模型因训练资源有限未充分收敛，其潜力未能完全体现——这需要进一步增加训练时长来验证。

**冻结 MLLM 的固有限制**：框架依赖冻结的 InternVL3-2B 作为特征提取器，难以针对生成任务进行端到端联合优化，可能限制深度跨模态理解的进一步提升。RQA 虽然缓解了这一问题，但本质上仍是对冻结输出的后处理。

**自条件信号的单调性**：纯图像预训练阶段使用的辅助提示是固定的通用文本，自适应提示生成或更复杂的自条件策略可能进一步改善性能。

### 6. 开放问题

1. **缩放律探索**：IOMM-L 在进一步增加训练时长后性能如何扩展？是否存在更优的模型缩放策略，使得更大模型能在给定计算预算下获得更高收益？
2. **混合比例最优化**：混合微调阶段最优的图像与文本配对数据比例是什么？不同下游任务（生成、编辑、多模态理解）是否需要不同的混合策略？
3. **跨模态迁移**：纯图像预训练学到的视觉先验能否迁移到其他生成任务（如视频生成、3D 合成）？自条件范式在这些模态中是否同样有效？
4. **适配器技术对比**：RQA 与其他参数高效微调技术（如 LoRA、Adapter、Prefix Tuning）在 UMM 生成场景下的系统对比尚未进行，各自的适用边界有待厘清。

## 原文 PDF

![[paperPDFs/CVPR_2026/Rethinking_UMM_Visual_Generation_Masked_Modeling_for_Efficient_Image_Only_Pre_training.pdf]]
