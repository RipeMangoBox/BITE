---
title: "Eagle 2: Building Post-Training Data Strategies from Scratch for Frontier Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Eagle_2_Building_Post_Training_Data_Strategies_from_Scratch_for_Frontier_Vision_Language_Models.pdf
aliases:
- E2TM
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过系统化的数据策略（大规模多样性收集、规则化过滤、聚类子集选择、增强与格式化）结合三阶段训练配方，直接操控模型所能学习的视觉-语言知识广度与精确度，从而驱动性能跃升。"
primary_logic: "以“多样性优先，后求精炼”为原则，将数据策略作为后训练的核心杠杆，并利用Stage-1.5与Stage-2的迭代反馈闭环（大轮驱动小轮），可以在有限资源下逼近甚至超越更大规模模型的表现。"
claims:
- "在2阶段训练范式下，逐步扩展数据类别（从基线5.2M到增加各类VQA、OCR、文本数据），平均得分从58.8持续提升至67.0，证明数据多样性的累积效益。"
- "引入Stage-1.5预训练后再进行Stage-2微调，相较先前最佳2阶段模型平均得分提高3.9%，且Stage-1.5自身已具备竞争力。"
- "对训练数据进行格式化与规则过滤后，8项基准提升，OCRBench暴涨45分，证明数据清洗的巨大价值。"
- "将视觉编码器从单一SigLIP升级为Tiled MoVE（SigLIP+ConvNeXt）后，12/14项基准受益，尤其在文档/图表/OCR任务上显著增强。"
---

# Eagle 2: Building Post-Training Data Strategies from Scratch for Frontier Vision-Language Models

> [!tip] 核心洞察
> 以“多样性优先，后求精炼”为原则，将数据策略作为后训练的核心杠杆，并利用Stage-1.5与Stage-2的迭代反馈闭环（大轮驱动小轮），可以在有限资源下逼近甚至超越更大规模模型的表现。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Eagle 2：从零开始构建前沿视觉语言模型的后训练数据策略 |
| 英文题名 | Eagle 2: Building Post-Training Data Strategies from Scratch for Frontier Vision-Language Models |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.14818); [GitHub](https://github.com/NVlabs/EAGLE?tab=readme-ov-file) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Eagle 2 (数据策略+三阶段训练+Tiled MoVE架构) |
| Dataset | 13-benchmark average (from Table 6), 14 diverse benchmarks, ChartQA, OCRBench, MathVista |

> [!tip] 效果简介
> - 13-benchmark average (from Table 6) 上，Average Score 为 73.5 (Eagle2-9B final)，对比 58.8 (Eagle2-Baseline)，变化 +14.7。
> - 14 diverse benchmarks 上，Overall win 为 Eagle2-9B wins all 14 benchmarks，对比 InternVL2-8B，变化 outperforms on 14/14。
> - 14 diverse benchmarks 上，Overall win 为 Eagle2-9B wins 9/14 benchmarks，对比 Qwen2-VL-7B，变化 leads on 9/14 and OpenCompass。

## 概述

当前开源视觉语言模型（VLM）社区在模型权重公开方面取得了显著进展，但一个核心瓶颈始终存在：**关键的后训练数据策略与实现细节仍不透明，且数据多样性与质量不足，导致开源模型性能普遍落后于闭源前沿模型**。Eagle 2 直面这一瓶颈，将数据策略作为后训练的核心杠杆，系统性地构建了一套从零开始的数据收集、精炼与训练流水线。

其核心洞察可概括为 **“多样性优先，后求精炼”**：先通过大规模多源收集获取丰富的视觉-语言知识广度，再通过规则过滤、聚类子集选择、增强与格式化等手段提升数据质量，最终在三阶段训练配方中释放数据潜力。方法上，Eagle 2 引入了一个独特的反馈闭环——Stage-1.5 的大规模预训练为 Stage-2 的高质量指令微调提供加速，而 Stage-2 的性能反馈又反过来指导 Stage-1.5 数据的迭代优化（大轮驱动小轮）。

关键证据链如下：
- **数据多样性的累积效益**：在 2 阶段训练范式下，从基线 5.2M 样本逐步扩展数据类别，平均得分从 58.8 持续提升至 67.0（Table 5）。
- **三阶段训练的增益**：引入 Stage-1.5 预训练后再进行 Stage-2 微调，相较此前最佳 2 阶段模型平均得分再提升 3.9%（Table 6）。
- **数据清洗的巨大价值**：对训练数据进行格式化与规则过滤后，8 项基准受益，OCRBench 更是暴涨 45 分（Table 6）。
- **架构升级的贡献**：将视觉编码器从单一 SigLIP 升级为 Tiled MoVE（SigLIP + ConvNeXt），12/14 项基准获得正向收益，尤其在文档、图表和 OCR 任务上显著增强。
- **最终性能定位**：Eagle2-9B 在 14 项多模态基准上全面超越 InternVL2-8B 和 MiniCPM-v2.6，在 9/14 基准上领先 Qwen2-VL-7B，并在 ChartQA、OCRBench、MathVista 上超越 GPT-4o，在 DocVQA、MMStar、AI2D 等基准上接近 GPT-4o（Table 7）。

这一系列结果证明，通过系统化的数据策略结合三阶段训练配方，可以在有限资源下逼近甚至超越更大规模闭源模型的表现。

## 背景与动机

### 视觉语言模型后训练的透明度困境

近年来，开源视觉语言模型（VLM）在权重公开性上取得了显著进展，使得研究社区能够直接访问和部署这些模型。然而，一个关键的瓶颈逐渐浮现：**后训练数据策略和具体实现细节仍然高度不透明**。许多开源工作虽然发布了模型权重，但其训练数据的构成、收集方法、过滤标准以及各阶段的配方细节往往被模糊处理或完全省略。这种不透明性直接导致开源VLM的性能普遍落后于GPT-4V、GPT-4o等闭源前沿模型——后者的数据策略作为核心商业机密被严密保护。

### 数据多样性与质量的失衡

当前开源VLM面临的第二个核心问题是**数据多样性与质量的不足**。现有方法往往在有限的、同质化的数据池上进行训练，导致模型在特定任务上表现尚可，但在涉及文档理解、图表解析、OCR识别、数学推理等多样化场景时能力严重不足。这种“木桶效应”使得模型的长板无法弥补短板带来的整体性能退化。与此同时，简单地扩大数据规模并不能自动解决问题——低质量数据的引入会引入噪声，甚至损害模型已有的能力。

### 从“权重开源”到“策略开源”的范式转变

针对上述缺口，Eagle 2 提出了一个根本性的思路转变：**将后训练数据策略本身作为核心研究对象，从零开始系统化地构建一套透明、可复现的数据策略与训练配方**。这一动机源于一个核心洞察：在模型架构和基础语言模型能力日趋同质化的当下，数据策略已成为驱动VLM性能跃升的首要杠杆。通过公开完整的数据收集、过滤、选择、增强和训练流程，Eagle 2 旨在弥合开源与闭源模型之间的性能鸿沟，同时为社区提供一个可复现的强基线。

### 核心设计原则：“多样性优先，后求精炼”

Eagle 2 的方法论建立在一个简单而激进的原则之上——**“多样性优先，后求精炼”（Diversity first, then quality）**。这一原则贯穿数据策略的始终：首先通过大规模被动收集与主动搜索，从180余个来源汇聚覆盖10个类别的多样化数据；随后通过规则化过滤、聚类子集选择、数据增强等精炼手段逐步提升数据质量。这种“先广撒网，后精筛选”的策略，使得模型能够在有限的计算资源下，最大化地吸收视觉-语言知识的广度与精确度。

## 核心创新

Eagle 2 的核心创新并非单一算法突破，而是一套以**数据策略为第一性杠杆**的系统化工程方案。其设计哲学围绕“多样性优先，后求精炼”展开，通过三个紧密耦合的维度，将后训练从传统的“模型微调”重新定义为“知识注入与精炼”的闭环过程。

### 1. 数据策略：从被动收集到主动闭环的知识工程

Eagle 2 将数据策略提升至与模型架构同等重要的地位，构建了一套从收集、过滤、选择到增强的完整流水线，直接操控模型所能学习的视觉-语言知识广度与精确度。

*   **大规模多样性收集**：模型最终在 Stage-1.5 使用 **21.6M** 样本，在 Stage-2 使用 **4.6M** 样本，数据来源超过 180 个，覆盖通用 VQA、OCR、图表、科学、数学、文本等 10 个类别。这一规模远超基于 **Cambrian-1 数据子集**（5.2M 样本）的基线。
*   **主动搜索与闭环迭代**：除了被动监控 arXiv 和 HuggingFace 的新数据集，该方法还基于模型错误分析，主动搜索针对模型短板（如特定类型的图表理解）的数据，形成“大轮驱动小轮”的反馈机制。
*   **规则化过滤与格式化**：通过人工审查提取低质数据特征（如问答不匹配、图文无关），制定规则进行清洗。同时遵循“相同任务，相似格式；不同任务，清晰区分”的原则统一数据格式。这一举措在 8 项基准上带来提升，其中 **OCRBench 暴涨 45 分**，证明了数据清洗的巨大价值。
*   **聚类子集选择与增强**：利用无监督 K-means 聚类在 SSCD 图像嵌入上进行均衡采样，并利用第三方 VLM 生成 CoT 解释、基于规则扩充 QA 对，进一步挖掘数据潜力。

### 2. 三阶段训练配方：解耦知识注入与指令对齐

Eagle 2 将传统的两阶段训练（MLP 对齐 + 全模型 SFT）重构为三阶段，解耦了大规模知识注入与高质量指令微调，这是性能跃升的关键因果旋钮。

*   **Stage-1.5 大规模预训练**：在传统的 MLP 对齐（Stage-1）之后、高质量 SFT（Stage-2）之前，插入一个大规模、全参数的预训练阶段。该阶段使用海量多样性数据（21.6M）为模型注入广博的视觉-语言知识。
*   **迭代反馈闭环**：Stage-1.5 为 Stage-2 提供一个强大的基座模型，加速后者的迭代；反过来，Stage-2 的精炼结果会反馈回 Stage-1.5，指导其数据的优化与更新。**Table 6** 的消融实验表明，引入 Stage-1.5 后，再经 Stage-2 微调，模型平均得分相较此前最佳两阶段模型**提高 3.9%**，且 Stage-1.5 的中间检查点自身已具备竞争力。

### 3. Tiled MoVE 视觉架构：以视觉为中心的感知增强

为突破单一视觉编码器的能力瓶颈，Eagle 2 设计了 **Tiled Mixture of Vision Encoders (MoVE)** 架构，将基线中的单一 **SigLIP** 编码器升级为 **SigLIP + ConvNeXt** 的混合编码器。

*   **动态平铺与多编码器融合**：采用动态平铺策略处理任意高分辨率图像，并将两个编码器的特征通过 PixelShuffle 下采样后拼接，送入 LLM。该设计使模型在 **12/14 项基准**上受益，尤其在文档、图表和 OCR 任务上增益显著，成为最终模型平均得分提升至 **73.5** 的关键驱动力。

### 4. 平衡感知数据打包：提升训练效率与稳定性

针对朴素贪心背包算法（如 LLaMa-Factory 所用）导致的长短序列分离、训练不稳定问题，Eagle 2 设计了**平衡感知贪心背包算法**。该算法在打包时优先保证每个包内序列长度分布均匀，在加速训练 2-3 倍的同时，进一步提升了模型性能（如 ChartQA 从 84.7 提升至 **86.4**，OCRBench 从 855 提升至 **868**）。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/011_Figure.jpg]]
*Figure: (a) Knapsacks of naive greedy knapsack method. (b) Knapsacks of balanced knapsack method*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/001_Figure_1.jpg]]
*Figure 1: | Overview of Eagle2-9B’s result across different multimodal benchmarks, in comparison to state-of-the-art open-source and commercial frontier models*

Eagle 2 的后训练数据策略遵循 **“多样性优先，后求精炼” (Diversity first, then quality)** 的核心原则，并将其推向极致。整个框架围绕一个系统化的数据流水线与三阶段训练配方构建，旨在从零开始为前沿视觉语言模型（VLM）提供透明、可复现且高性能的后训练方案。

### 数据策略流水线

如图 3 所示，数据策略分为上下两个半区：**数据收集** 与 **数据精炼**。

**数据收集层** 包含两条并行的路径：
1.  **被动收集**：持续监控 arXiv 预印本和 HuggingFace Datasets 上的最新相关数据集，确保数据池的时效性与广度。
2.  **主动搜索**：基于模型错误分析识别能力短板（“木桶效应”），针对性地搜索补充弱项数据。新数据集以批次方式加入，需同时满足两个条件——在所有关注的基准上不引起整体准确率退化，且能引入有意义的多样性。

最终模型在 Stage-1.5 使用了来自 180+ 来源的 21.6M 样本，在 Stage-2 使用了 4.6M 样本，覆盖通用 VQA、OCR、图表/表格、科学、数学、文本等 10 个类别。

**数据精炼层** 由四个核心模块串联构成：
1.  **相似度评分与去重**：对同一类别内的新数据源，计算每个样本与现有数据池中样本的最大图文相似度乘积（公式见下），取均值作为该数据源的相关性评分，用于评估数据重叠度并过滤冗余样本。图像嵌入由 SSCD 生成，文本嵌入由 all-mpnet-base-v2 生成。
    
    $$S _ { k } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \operatorname* { m a x } _ { 1 \leq j \leq M _ { k } } \left( \operatorname { S i m } ( I _ { i } , I _ { j } ) \times \operatorname { S i m } ( T _ { i } , T _ { j } ) \right)$$

2.  **规则化数据过滤**：通过人工审查提取低质量样本的典型特征（如问答不匹配、图文无关、重复文本、数值精度错误等），制定规则批量剔除劣质数据。
3.  **子集选择 (K-means 聚类)**：确定各数据源的采样配额后，在 SSCD 图像嵌入上应用无监督 K-means 聚类，从每个簇中均衡采样，确保所选子集在视觉上具有代表性。
4.  **数据增强与格式化**：利用第三方 VLM 生成 CoT 解释和细粒度图像描述，通过规则扩充问答对，并将短答案扩展为详细回应。格式化遵循“同任务、同格式；异任务、格式分明”的原则，去除不必要的格式装饰（如 LaTeX 提取任务中的固定公式环境）。

### 三阶段训练策略

为最大化利用上述数据，Eagle 2 采用三阶段训练配方（Table 4）：

- **Stage-1**：仅训练 MLP 连接器，对齐视觉与语言模态。
- **Stage-1.5**：在大规模多样化数据上训练全模型，作为承上启下的预训练阶段。
- **Stage-2**：在高质量、精选的指令数据上进行最终微调。

Stage-1.5 与 Stage-2 之间形成**迭代反馈闭环**（Figure 8）：Stage-1.5 为 Stage-2 提供一个强壮的基座，加速 Stage-2 的数据迭代；Stage-2 的消融发现则反向指导 Stage-1.5 数据的更新与优化，形成“大轮驱动小轮”的高效迭代机制。

### 视觉编码器架构

在视觉端，Eagle 2 采用 **Tiled Mixture of Vision Encoders (Tiled MoVE)** 设计（Figure 11），将动态图像平铺与多编码器融合统一在一个架构中：同时使用 SigLIP 和 ConvNeXt-XXLarge 作为视觉编码器，对高分辨率图像进行动态平铺后分别提取特征，经 PixelShuffle 下采样后拼接，显著增强文档、图表和 OCR 任务的理解能力。

### 数据打包

训练时采用**平衡感知贪心背包算法**，在传统贪心背包中引入长度均匀性约束，确保每个训练包内同时包含长序列和短序列，避免朴素贪心方法导致的包间长度分布不均问题，从而加速训练并提升性能。

## 核心模块与公式推导

### 数据收集与相似度评分

Eagle 2 的数据策略流水线（Figure 3）由收集与精炼两大环节构成。在收集端，团队采用“被动收集 + 主动搜索”的双轨机制：持续监控 arXiv 和 HuggingFace 上的最新数据集，同时基于模型的错误分析定向补充弱项数据。新引入的数据源需通过两道门槛——加入后不导致各基准性能退化，且能引入有意义的多样性。

为量化新数据源与现有数据池的重叠程度，论文定义了**相似度评分**（Similarity Score）。该评分在相同数据类别内计算，以评估新增数据的边际价值：

$$S _ { k } = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \operatorname* { m a x } _ { 1 \leq j \leq M _ { k } } \left( \operatorname { S i m } ( I _ { i } , I _ { j } ) \times \operatorname { S i m } ( T _ { i } , T _ { j } ) \right)$$

其中：
- $S_k$：新数据源 $k$ 与现有数据池的相似度评分，值越高表示重叠越严重；
- $N$：新数据源 $k$ 中与现有池同类的样本数；
- $M_k$：现有数据池中与样本 $i$ 同类的样本数；
- $I_i, T_i$：分别为样本 $i$ 的图像嵌入和文本嵌入；
- $\operatorname{Sim}(\cdot, \cdot)$：余弦相似度函数；
- 图像嵌入由 **SSCD** 模型生成，文本嵌入由 **all-mpnet-base-v2** 模型生成；
- 核心操作：对每个新样本，取其在现有池中图文相似度乘积的最大值，再对所有新样本求平均。

该公式的直觉是：仅当新样本的图像和文本同时与现有样本高度相似时，才被视为冗余。实验表明，该评分能粗略反映新数据集与 Cambrian 数据池的重叠程度（Table K）。

### 子集选择：K-means 聚类

在确定各数据源的采样配额后，Eagle 2 采用无监督 **K-means 聚类**进行平衡子集选择。具体而言，在 **SSCD 图像嵌入**空间上运行 K-means，使具有相似图表类型、视觉布局的样本聚类到同一簇中，然后从每个簇中均匀采样，确保所选子集在视觉特征上具有最大覆盖度。这一方法在图表、OCR 等视觉敏感类别中尤为关键。

### 数据打包：平衡感知贪心背包

标准的数据打包（如 LLaMa-Factory 中的朴素贪心背包）倾向于将长序列与短序列分离，导致不同包的长度分布严重不均，影响训练效率与稳定性。Eagle 2 提出了**平衡感知贪心背包算法**（balanced_greedy_knapsack），其核心约束是：每个包内同时包含长样本和短样本，使包间长度分布更均匀（Figure 9 右图 vs. 左图）。

该算法在保持打包效率（2-3 倍训练加速）的同时，通过长度均衡化避免了极端长包导致的显存峰值和梯度噪声。消融实验证实，平衡打包在 ChartQA（84.7 → 86.4）和 OCRBench（855 → 868）上均优于朴素贪心打包（Table N）。

### 数据增强与格式化

数据增强模块（Figure 7）包含三类操作：
1. **CoT 增强**：利用第三方 VLM 为现有 QA 数据生成逐步推理的思维链解释，使模型学会显式推理过程；
2. **规则化 QA 生成**：基于预定义模板和图像元数据自动扩充问答对；
3. **短答案扩展**：将简短答案改写为详细描述，提升模型生成丰富回应的能力。

数据格式化遵循一条基本原则：“相同任务，相似格式；不同任务，清晰区分格式”。例如，从图像中提取 LaTeX 公式的任务，去除不必要的固定方程环境后，OCRBench 得分显著提升（Table 3）。

### Tiled Mixture of Vision Encoders (MoVE)

视觉编码器架构（Figure 11）由两个并行编码器组成：
- **SigLIP**：处理 448×448 分辨率的图像块；
- **ConvNeXt-XXLarge**：处理 512×512 分辨率的图像块。

对于高分辨率输入，图像首先被动态平铺为多个子块（遵循 InternVL-1.5 的平铺策略），每个子块分别经过两个编码器提取特征。ConvNeXt 的输出通过 **PixelShuffle** 操作进行空间到通道的重排以实现下采样，随后与 SigLIP 特征沿序列维度拼接，送入 MLP 投影层与 LLM 对齐。

该设计在 12/14 项基准上带来正向收益，尤其在文档理解（DocVQA）、图表问答（ChartQA）和 OCR 任务上提升显著（Table 6）。

## 实验与分析

### 核心实验设计

Eagle 2 的实验验证围绕一个核心因果命题展开：**系统化的后训练数据策略能否在有限模型规模下，驱动视觉语言模型（VLM）的性能实现跃升？** 为回答这一问题，作者设计了一套递进式的消融验证框架，从基线模型出发，逐步叠加数据多样性扩展、训练阶段改造、数据精炼与架构升级等干预变量，追踪其在 13 至 14 项多模态基准上的平均得分变化（Figure 2 呈现了该消融路径的直观柱状图，详细数值则分列于 Table 5 与 Table 6）。

实验的起点是一个采用经典 LLaVA 两阶段训练配方的基线模型（Table 1），其 Stage-2 数据仅使用 **Cambrian-1** 数据子集（约 5.2M 样本），在 13 项基准上的平均得分为 **58.8**。这一基线代表了当前开源社区“有代码、无数据策略”的典型水平——模型权重公开，但后训练数据配方不透明，性能显著落后于闭源前沿模型。所有后续实验均在此基础上进行受控变量叠加，以确保观测到的性能增益可归因于特定的数据或架构改进。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/003_Table_1.jpg]]
*Table 1: | Baseline Settings*

### 数据多样性的累积效益：2 阶段训练下的消融

Table 5 展示了在保持两阶段训练范式不变的前提下，逐步扩展 Stage-2 微调数据类别所带来的累积效益。实验遵循“每次仅增加一个特定类别数据”的原则，以隔离各类数据对模型能力的贡献：

1. **基线 (Cambrian-1 子集)**：平均得分 58.8。
2. **+ 朴素 OCR 数据**：引入基础 OCR 识别数据后，模型在 OCRBench 等任务上初步获益，平均得分开始上升。
3. **+ 图表、表格与 OCR QA 数据**：这是增益最为显著的一步。加入 ChartQA、TableQA 及 OCR 问答类数据后，平均得分跃升至 **65.0**。这表明结构化视觉推理（读图、读表、读文字并回答）是基线模型的主要能力短板，而针对性数据的引入直接填补了这一缺口。
4. **+ 科学与数学数据**：进一步将平均得分推高至 **66.0**，说明逻辑推理与专业知识理解能力可通过领域数据注入获得增强。
5. **+ Caption、Grounding 与计数数据**：补充视觉定位与描述类数据后，平均得分达到 **66.5**。
6. **+ 纯文本数据**：即使对于多模态模型，高质量纯文本 SFT 数据仍带来正向增益，使平均得分升至 **67.0**。这一发现验证了论文的观点：语言能力的稳固是视觉-语言协同推理的基础，纯文本数据的质量不容忽视。

**关键结论**：在 2 阶段训练设定下，仅通过扩展数据多样性，模型平均得分便从 58.8 持续提升至 67.0（+8.2 分），且每一步增益均为正向，未出现性能倒退。这强有力地证明了 **“多样性优先”原则的有效性**——数据类别的广度直接转化为模型能力的广度。

### 三阶段训练范式的突破：Stage-1.5 的杠杆效应

Table 6 记录了从最佳 2 阶段模型向三阶段训练范式过渡的完整消融路径，这是 Eagle 2 方法体系中最具创新性的实验环节。

**Stage-1.5 的引入**：在 Stage-2 微调之前插入一个大规模、多样化的全模型预训练阶段（Stage-1.5），使用 21.6M 样本进行训练。令人注目的是，**仅完成 Stage-1.5 的检查点本身已具备竞争力**——其平均得分显著超越了先前经过精心调优的 2 阶段最佳模型。在此基础上再进行 Stage-2 高质量指令微调，平均得分在先前最佳模型基础上**进一步提升了 3.9%**。这一结果揭示了 Stage-1.5 的核心价值：它并非简单的“更多训练”，而是为模型提供了一个在广泛视觉-语言知识上充分预热的阶段，使得后续的指令微调能在一个更高的起点上进行，从而释放出更大的性能潜力。

**数据精炼的增益**：在三阶段框架下，应用第 2.2 节所述的全面数据选择策略（相似度评分去重、K-means 聚类子集选择），将 Stage-2 数据量精简至 **4.6M 样本**，同时实现了平均得分的提升。这证明“先求多样，后求精炼”的策略是高效的——大规模数据用于奠定能力基础，而精炼后的高质量数据用于精准拔高。

**数据格式化与过滤的巨大价值**：对训练数据进行格式化统一和规则化过滤后，**14 项基准中的 8 项获得提升**，其中最引人注目的是 **OCRBench 暴涨 45 分**。这一消融结果直接锚定了论文的核心主张：数据质量（而非仅仅是数量或多样性）是后训练中的关键因果杠杆。低质量数据（如格式不一致、问答错配、图文无关）不仅无益，反而会严重损害模型在特定任务上的表现。手工审查驱动的规则化过滤虽然自动化程度有限，但其效果在实验中得到了量化验证。

**数据增强的贡献**：引入 CoT（思维链）数据增强和规则化图表数据增强后，平均得分从 71.8 提升至 72.1。其中，CoT 增强配合逐步推理提示，使 MathVista-Mini 得分从 61.0 提升至 63.5（Table M）；规则化图表增强则为 ChartQA 带来 1 个点的直接增益。这些看似微小的提升，在模型性能接近前沿水平时，往往是决定性的边际改进。

**Tiled MoVE 架构升级**：将视觉编码器从单一 SigLIP 升级为 **Tiled Mixture of Vision Encoders（SigLIP + ConvNeXt-XXLarge，动态平铺，PixelShuffle 融合）**后，**14 项基准中的 12 项受益**，平均得分达到最终的 **73.5**。增益尤其集中在文档理解、图表解析和 OCR 相关任务上，这与 MoVE 设计的目标高度一致——多分辨率平铺和多编码器融合直接增强了对高分辨率、细粒度视觉信息的捕捉能力。

### 与前沿模型的全面对比

Table 7 展示了 Eagle2-9B 在 14 项多模态基准上与当前主流开源及闭源模型的全面对比，这是验证方法体系最终效能的决定性证据。

**全面超越同级开源模型**：Eagle2-9B **在所有 14 项基准上均超越 InternVL2-8B 和 MiniCPM-v2.6**，并在 **14 项基准中的 9 项上领先 Qwen2-VL-7B**，同时在 OpenCompass 综合评测中胜出。考虑到 Eagle2-9B 与这些模型在参数规模上处于同一量级（8B-9B），这一全面领先充分证明了其数据策略与训练配方的优越性——在同等模型容量下，更优的数据策略可以释放出显著更高的性能。

**逼近甚至超越商业闭源模型**：与 GPT-4V 的对比中，Eagle2-9B **除 MMVet 和 MMMU 外全面超越**。更令人瞩目的是，在与 GPT-4o 的对比中，Eagle2-9B **在 ChartQA、OCRBench 和 MathVista 三项基准上实现了超越**，并在 DocVQA、MMStar、AI2D 和 OpenCompass 上取得了非常接近的性能。这一结果直接回应了论文的核心动机——通过系统化的数据策略，开源模型有能力在多个关键能力维度上挑战甚至击败闭源前沿模型。

**定性能力展示**：论文通过 Figure 12 至 Figure 18 展示了一系列定性示例，涵盖了 OCR 识别（Figure 12）、多语言 OCR（Figure 13）、链式推理（Figure 14）、简单算法题求解（Figure 15）、图像异常分析（Figure 16）、镜子中物体区分（Figure 17）以及手写体识别（Figure 18）等能力。这些示例并非孤立的 cherry-picking，而是与定量基准得分相互印证，共同描绘了 Eagle2-9B 作为一款能力均衡且在某些维度（如 OCR、图表理解）上表现突出的 VLM 的全貌。

### 消融实验中的关键洞察

综合上述实验，可以提炼出以下经过量化验证的核心洞察：

1.  **数据多样性的边际收益递减但持续为正**：在 2 阶段训练中，从 5.2M 到逐步增加各类数据，每一步都带来正向增益，未观察到因数据冲突导致的性能倒退。这说明在当前的 VLM 后训练阶段，数据多样性的天花板尚未触及。

2.  **Stage-1.5 是“大轮驱动小轮”的加速器**：Figure 8 描绘了 Stage-1.5 与 Stage-2 之间的反馈闭环——Stage-1.5 为 Stage-2 提供一个强大的初始化，加速其迭代；而 Stage-2 的实验反馈又可反过来指导 Stage-1.5 数据的优化。实验数据证明，这一闭环设计在有限资源下有效逼近了更大规模模型的性能。

3.  **数据质量是隐藏的性能杀手**：OCRBench 上 45 分的暴涨是整篇论文中最具说服力的单一证据点。它表明，低质量数据对特定能力的损害可能远超直觉预期，而系统化的数据清洗（格式化统一、规则过滤）可以释放被压制的模型潜能。

4.  **视觉编码器架构是文档/图表任务的瓶颈**：Tiled MoVE 在 12/14 基准上的正向收益，尤其是在文档、图表、OCR 任务上的显著增强，说明单一编码器架构已成为高分辨率视觉理解的瓶颈，而多编码器混合与动态平铺是当前有效的突破方向。

### 失败模式与局限性

尽管实验结果整体强劲，论文中仍透露出若干值得关注的局限与潜在失败模式：

- **MMVet 与 MMMU 上的相对短板**：在与 GPT-4V 的对比中，Eagle2-9B 在这两项基准上未能超越。MMVet 侧重细粒度视觉理解与推理，MMMU 涵盖多学科专业知识，这可能暗示当前数据策略在复杂多模态推理和深度专业知识覆盖上仍有提升空间。

- **数据过滤依赖人工审查**：45 分的 OCRBench 增益虽然令人印象深刻，但其背后的规则化过滤高度依赖手工制定的规则（Figure 5 展示了典型低质样本类型）。面对新类型的低质数据，这种手工方法可能遗漏，自动化程度有待提高。

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/007_Figure_5.jpg]]
*Figure 5: | Typical low-quality samples. Figure 6 | Public datasets [60, 58] often do not rigorously handle numerical precision, resulting in high decimal precision impossible to directly extract from the image*

- **计算成本高昂**：Table A 披露了训练资源详情——Eagle2-9B 的 Stage-1.5 需使用 **256 个 H100 GPU 训练 28 小时**。这一计算门槛限制了资源有限的研究团队对完整三阶段流程进行复现或改进。

- **评估覆盖范围有限**：评估主要基于公开的英文多模态基准，对于多语言环境（尽管 Figure 13 展示了多语言 OCR 能力）、安全性、偏见以及长程对话等真实世界应用维度的泛化能力，尚未进行充分验证。

- **数据增强引入噪声风险**：CoT 增强和答案扩展依赖第三方 VLM 生成伪标注。尽管设有自动过滤机制，仍可能引入噪声和错误知识，在特定场景下影响模型可靠性。论文对此风险有所认知，但未提供量化评估。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/024_Table.jpg]]
*Table: B | General VQA Data. Table C | Naive OCR Data. Table D | Counting & Grounding Data*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/025_Table.jpg]]
*Table: H | Chart & Table Data. We heavily use some lowquality data such as MMC-Inst, PlotQA in Stage-1.5. But in our final stage, we just sample a very small part from these sources*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/026_Table.jpg]]
*Table: E | Science Data. ×?? notes repeat the data by ?? times. Table F | Math Data. Table G | Caption & Knowledge Data. Table I | OCR QA Data. “×4" means we repeat every sample 4 times*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/027_Table.jpg]]
*Table: J | Text-only Data. The quality of text-only data still matters for multi-modal LLMs. We collect a diverse collection of open-source text-only datasets. We also convert some preference datasets into SFT format. Table L | Dataset for CoT data augmentation. Table M | With CoT training data, adding "Solve this problem step-by-step" prompt can help to improve the performance*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/008_Figure_7.jpg]]
*Figure 7: | Our three most commonly used data augmentation methods.These methods rely on rule-based approaches or utilize VLM models for automatic labeling. Table 3 | Two samples with same "Extract LATEX from image" task but with different format*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/005_Table_2.jpg]]
*Table 2: Eagle 2: Building Post-Training Data Strategies from Scratch for Frontier Vision-Language Models (b) Summary of the additional Stage 1.5 datasets Table 2 | Dataset used in Eagle 2. Dataset in Magenta is internal data*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/009_Table_4.jpg]]
*Table 4: | We present our three-stage training settings, where Eagle2-9B/2B/1B builds upon Qwen2.5- 32B/7B/1.5B/0.5B [27], respectively. *: For small scale model with 0.5/1.5B LLM, we only use SigLIP as visual encoder and learning rate of 4 $\times$ 1 $0 ^ { - 5 }$ in Stage-1.5 & 2*

![[assets/figures/papers/paper_list_l20_https_arxiv_org_abs_2501_14818/figures/013_Table.jpg]]

## 方法谱系与知识库定位

### 1. 与现有训练范式的继承与突破

Eagle 2 的方法论根植于视觉语言模型（VLM）的经典两阶段训练范式，但通过引入关键架构与数据策略变革，显著拓展了其性能边界。

*   **训练配方基线**：Eagle 2 以 **LLaVA** 的两阶段训练配方为起点（MLP对齐 + 全模型SFT），但将其扩展为**三阶段训练策略**，即在传统的MLP对齐（Stage-1）与高质量指令微调（Stage-2）之间，插入了一个大规模、多样化的全模型预训练阶段（Stage-1.5）。这一设计并非简单的阶段堆叠，而是构建了一个**迭代反馈闭环**：Stage-1.5 为 Stage-2 提供一个强大的初始化，加速其数据迭代；而 Stage-2 的错误分析又能反向指导 Stage-1.5 的数据补充，形成“大轮驱动小轮”的效率飞轮。
*   **数据基线**：在数据层面，Eagle 2 的 Stage-2 基线直接建立在 **Cambrian-1** 的一个数据子集（5.2M样本）之上。然而，Cambrian-1 的数据策略细节并不完全透明，且数据多样性有限。Eagle 2 的工作核心正是将“数据策略”本身作为可系统化研究、可公开复现的杠杆，从零开始构建了一套完整的后训练数据工程流水线。
*   **架构演进**：在视觉编码器上，Eagle 2 超越了单一 **SigLIP** 编码器的常规设计，提出了 **Tiled Mixture of Vision Encoders (Tiled MoVE)** 架构。该架构融合了 SigLIP 和 ConvNeXt-XXLarge 两个视觉编码器，并结合动态图像平铺与 PixelShuffle 特征融合技术。这一设计直接回应了 VLM 在高分辨率文档、图表和 OCR 任务上的性能瓶颈。

### 2. 适用边界与局限性

尽管 Eagle 2 取得了显著性能，其方法存在明确的适用边界与限制：

*   **数据过滤的自动化瓶颈**：数据过滤与格式化策略高度依赖**人工审查**和手工制定的规则（例如，剔除问答不匹配、图文无关、重复文本等低质模式）。当面对前所未见的、新型的低质量数据模式时，这种基于规则的过滤系统可能会遗漏，泛化能力受限。如何自动化地量化数据价值并取代人工审查，仍是一个开放问题。
*   **高昂的计算资源门槛**：三阶段训练策略伴随着巨大的计算开销。以 Eagle2-9B 为例，其 Stage-1.5 阶段在 256 个 H100 GPU 上训练了 28 小时。如此高的算力需求，极大地限制了资源有限的小型研究团队对该流程进行复现、验证或改进，这在一定程度上削弱了其“开源”的普惠性。
*   **评估的局限性**：模型的评估主要基于一系列公开的**英文多模态基准**（如 Table 7 所列的 14 项测试）。对于多语言环境、真实世界开放域应用中的安全性、偏见、鲁棒性等关键维度，其泛化能力尚未得到充分验证。
*   **数据增强的噪声风险**：数据增强策略（如 CoT 生成、答案扩展）依赖第三方 VLM 生成伪标注。尽管存在自动过滤机制，但此过程仍可能引入噪声和错误知识，尤其是在推理密集型任务中，错误的思维链可能反而损害模型的可靠性。

### 3. 开放问题与未来方向

Eagle 2 的工作揭示了 VLM 后训练领域的几个关键开放问题：

*   **数据策略的自动化闭环**：如何更有效地利用相似度评分（Similarity Score）等指标，并结合模型反馈，实现从“数据发现→价值评估→过滤/选择→训练→错误分析→主动搜索”的完全自动化数据迭代闭环，是提升研发效率的关键。
*   **最优数据配比的探索**：Stage-1.5 和 Stage-2 之间的数据量、数据类别配比、采样策略以及类别平衡是否存在理论或经验上的最优解？当前“多样性优先”的策略在数据规模进一步扩大（例如超过10M）时，其性能增益是否会饱和，以及如何突破，仍有待探索。
*   **能力边界的拓展**：当前的数据策略和评估主要围绕图文问答展开。模型在长程多轮对话、复杂多步推理、安全性对齐、具身智能等更广泛、更贴近真实世界应用场景的能力上，其提升空间和方法论尚不明确。

## 原文 PDF

![[paperPDFs/ICLR_2025/Eagle_2_Building_Post_Training_Data_Strategies_from_Scratch_for_Frontier_Vision_Language_Models.pdf]]
