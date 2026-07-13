---
title: "Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: A Comprehensive Evaluation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Benchmarking_Large_Vision_Language_Models_on_Fine_Grained_Image_Tasks_A_Comprehensive_Evaluation.pdf
project_link: null
code_link: https://github.com/SEU-VIPGroup/FG-BMK
aliases:
- FB
- BLVLMFGITCE
- FG-BMK
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "用FG-BMK同时评估LVLM细粒度问答、检索、分类和鲁棒性。"
primary_logic: "FG-BMK构建覆盖12个细粒度数据集的人类导向与机器导向任务，再比较训练范式、对齐粒度和特征扰动影响。"
claims:
- "LVLM在细粒度任务上的主要瓶颈是跨模态对齐过程中视觉判别性的退化。"
- "对比学习视觉特征在细粒度检索和分类上显著优于生成式或重建式范式。"
- "细粒度对齐数据比粗粒度对齐更能保留属性和类别判别能力。"
- "LVLM在CUB、Stanford Dogs和FGVC Aircraft等任务上仍明显落后于专用细粒度模型。"
---

# Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: A Comprehensive Evaluation

> [!tip] 核心洞察
> 对比学习范式（如EVA-CLIP、DINOv2）比生成式或重建式范式更能保持视觉特征的细粒度判别性；视觉-文本对齐若存在粒度不匹配会损害细粒度判别能力；LVLM在细粒度任务上仍落后于专用细粒度模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大规模视觉语言模型在细粒度图像任务上的基准评测：一项全面评估 |
| 英文题名 | Benchmarking Large Vision-Language Models on Fine-Grained Image Tasks: A Comprehensive Evaluation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cVc74MLspe) · [GitHub](https://github.com/SEU-VIPGroup/FG-BMK) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | FG-BMK |
| Dataset | CUB-200-2011, Stanford Dogs, FGVC Aircraft |

> [!tip] 效果简介
> - CUB-200-2011 上，分类准确率（Short-Answer） 为 85.60%，对比 93.10% (FG-Tailored)，变化 -7.50%。
> - Stanford Dogs 上，分类准确率（Short-Answer） 为 86.49%，对比 97.30% (FG-Tailored)，变化 -10.81%。
> - FGVC Aircraft 上，分类准确率（Short-Answer） 为 66.19%，对比 95.40% (FG-Tailored)，变化 -29.21%。

## 概要

本文提出了一个名为 **FG-BMK** 的综合性基准，用于系统评估大规模视觉语言模型（Large Vision-Language Models, LVLMs）在细粒度图像任务上的表现。该基准包含 **101 万个问题** 和 **28 万张图像**，覆盖 12 个成熟的细粒度数据集。FG-BMK 设计了两种互补的评估范式：**人类导向评估**（Human-oriented Evaluation）通过对话式交互（真/假、多选、简答）测试模型对细粒度视觉查询的理解能力；**机器导向评估**（Machine-oriented Evaluation）通过图像检索（mAP）和图像分类（Top-1 准确率）直接评估视觉特征的表示能力。研究评估了 9 个开源 LVLM、2 个闭源模型（GPT-4o-1120, Gemini-2.0-flash）以及纯视觉模型 DINOv2。

现有 LVLM 评估基准（如 LVLM-eHub, MMBench）主要关注通用视觉理解能力，缺乏对细粒度视觉任务（如区分同一属下的不同物种）的系统评估。细粒度视觉任务要求模型具备精细的视觉判别能力，这对 LVLM 的视觉编码器和跨模态对齐模块提出了更高要求。本文的核心动机是揭示 LVLM 在细粒度任务上的真实瓶颈，并探索影响其性能的关键因素。

## 核心方法与创新机理

本文的核心创新在于：

1. **提出 FG-BMK 基准**：首个同时包含人类导向和机器导向评估的细粒度 LVLM 基准，覆盖 12 个数据集、多种任务类型和层次化粒度级别。
2. **揭示关键瓶颈**：通过系统性实验发现，LVLM 在细粒度任务上的主要瓶颈在于**视觉特征在跨模态对齐过程中细粒度判别能力的退化**，以及**训练数据中细粒度知识的分布不均**。
3. **识别因果旋钮**：**对齐阶段的数据粒度一致性**（即图像-文本对中文本描述是否与图像中物体的细粒度类别匹配）是影响 LVLM 细粒度性能的关键可调控因素。
4. **核心洞察**：对比学习范式（如 EVA-CLIP, DINOv2）比生成式或重建式范式更能保持视觉特征的细粒度判别性；视觉-文本对齐若存在粒度不匹配会损害细粒度判别能力；LVLM 在细粒度任务上仍落后于专用细粒度模型。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/001_Figure_1.jpg]]
*Figure 1: Our proposed benchmark: The human-oriented evaluation tests the model’s ability to handle fine-grained visual queries (true/false, multiple-choice, short-answer), while the machine-oriented evaluation directly assesses visual feature representation through image retrieval and classification tasks. =true/false question, =multiple-choice question, =short-answer question*

FG-BMK 的整体框架如 **Figure 1** 所示，包含两个主要评估分支：

- **人类导向评估**：通过对话式交互评估 LVLM 对细粒度视觉查询的理解和回答能力，包括：
  - **属性识别**（Attribute Recognition）：识别颜色、图案、形状、长度、大小等属性
  - **知识偏差估计**（Knowledge Bias Estimation）：评估模型在不同细粒度类别上的识别一致性
  - **层次粒度识别**（Hierarchical Granularity Recognition）：在类、属、种等不同粒度级别上进行识别

- **机器导向评估**：通过图像检索和图像分类任务直接评估 LVLM 视觉特征的表示能力，包括：
  - **判别性**（Discriminability）：通过检索和分类评估特征区分能力
  - **鲁棒性**（Robustness）：通过特征扰动分析评估特征稳定性

数据来源为 12 个成熟的细粒度数据集（**Table 6**），涵盖鸟类、狗、汽车、飞机、食物、花卉等多个元类别。

### 5.1 评估模型与训练策略

**Table 1** 列出了开源评估模型的训练策略。模型使用的损失函数包括：
- **对比损失**（Con, Contrastive Loss）：如 EVA-CLIP, InternVL
- **生成损失**（Gen, Generative Loss）：如 Qwen, LLaVA
- **匹配损失**（Mat, Image-Text Matching Loss）：如 BLIP-2, InternVL
- **重建损失**（Rec, Reconstruction Loss）：如 BEiT3
- **蒸馏损失**（Dis, Distillation Loss）：如 DINOv2

### 5.2 人类导向评估任务设计

**知识偏差估计**任务中，正样本将每张图像与其细粒度标签配对，负样本将图像与同一超类别中随机选择的标签配对。对于每个细粒度类别，计算 LVLM 在所有对应真/假问题上的准确率作为该类别的知识理解度量。

**层次粒度识别**任务在 CUB-200-2011 数据集上设计了类（class）、属（genus）、种（species）三个粒度级别的问题。

### 5.3 机器导向评估任务设计

**跨元类别分类**（Cross Meta-class Classification）任务遵循 DINOv2 方法，在合并了不同数据集细粒度类别的统一训练集上训练模型，然后在每个单独数据集上测试。

**特征鲁棒性**评估使用投影梯度下降（Projected Gradient Descent, Madry et al., 2018）对视觉特征引入扰动，分析其对分类准确率的影响。

## 实验与关键发现

### 6.1 人类导向评估结果

**层次粒度识别**：如 **Figure 2** 所示，以 InternVL3 为例，其准确率随粒度变细而下降。在类级别上，InternVL3 在多选题上达到 99.76%，在真/假题上达到 99.77%；在属级别上，多选题准确率降至 90.75%，下降 9.01%；在种级别上，真/假题准确率降至 62.48%，多选题降至 61.18%。**Figure 11** 显示所有模型均呈现相同趋势。

**属性识别**：**Table 2** 显示 InternVL3 在 CUB-200-2011 上的属性识别准确率：图案识别平均 50.13%，形状识别仅 30.95%，长度属性 71.03%，大小属性 52.55%。**Table 10-14** 提供了 LLaVA、BLIP2、InternVL、Gemini-2.0-flash、Qwen2.5-VL 的详细属性识别结果。所有模型在形状属性上表现最弱。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/004_Table_2.jpg]]
*Table 2: Attribute recognition accuracy of InternVL3 (Zhu et al., 2025) on the CUB-200-2011 (Wah et al., 2011) dataset (values in parentheses represent the average accuracy for each attribute)*

**知识偏差**：**Figure 3** 显示原始 LLaVA 在不同细粒度鸟类类别上的识别准确率高度不一致（某些类别接近 90%，其他类别仅约 30%）。在类别平衡的数据集上微调后（黄色点），LLaVA 在所有类别上均表现出稳定的识别能力，验证了数据分布偏差是主要原因。**Figure 12-13** 展示了闭源模型和 Qwen2.5-VL 的类似结果。

### 6.2 机器导向评估结果

**检索与分类**：**Figure 4-5** 显示对比训练范式（EVA-CLIP, InternVL, DINOv2）在细粒度检索和分类上显著优于生成式（Qwen）和重建式（BEiT3）范式。**Figure 6-7** 的 Nemenyi 统计检验进一步确认了这一差异的显著性。

**与专用细粒度模型对比**：**Table 3** 显示 LVLM 在细粒度任务上仍落后于专用细粒度模型。例如，在 CUB-200-2011 上，LVLM 简答（SA）准确率为 85.60%，线性分类器（LC）为 91.65%，而专用细粒度模型（FG-Tailored）达到 93.10%；在 Stanford Dogs 上，LVLM SA 为 86.49%，LC 为 90.50%，FG-Tailored 为 97.30%；在 FGVC Aircraft 上，LVLM SA 为 66.19%，LC 为 78.88%，FG-Tailored 为 95.40%。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/010_Table_3.jpg]]

**多元分类**：**Figure 8** 显示 EVA-CLIP 在多元元类别分类中平均准确率仅下降 1.96%，而 Qwen 和 BEiT3 分别下降 4.16% 和 7.41%。

**编码器大小影响**：**Figure 9** 显示 DINOv2-B（较小编码器）在 CUB-200-2011 上比 BEiT3-L（较大编码器）高 8.08%，在 Stanford Dogs 上高 9.49%。增加 DINOv2 编码器大小从 B 到 L 仅提升 0.6%，从 L 到 G 仅提升 0.3%。

**数据规模影响**：**Figure 7** 显示使用 2B 样本训练的 EVA-CLIP 并未优于使用 142M 样本训练的 DINOv2。

### 6.3 对齐粒度一致性分析

**Table 4** 显示 LLaVA 对齐前的原始视觉特征在细粒度分类上平均比对齐后的特征高 3.39%。使用细粒度文本进行对齐（Aligned-FG）比粗粒度对齐（Aligned）在 Stanford Dogs 上提升 2.55%，在 Stanford Cars 上提升 1.73%。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/015_Table_4.jpg]]

**Table 15** 显示重新训练的 LLaVA（使用粒度匹配的对齐数据）在所有细粒度简答任务上一致优于原始 LLaVA：CUB-200-2011 上 86.32% vs 85.60%，Stanford Dogs 上 87.58% vs 86.49%，Stanford Cars 上 91.73% vs 90.55%，Food-101 上 95.74% vs 95.25%。

### 6.4 特征鲁棒性分析

**Table 5** 显示对 EVA-CLIP 特征进行扰动后，在细粒度数据集 CUB-200-2011 上准确率从 88.95% 降至 24.94%，而在通用数据集 CIFAR-100 上仅从 93.05% 降至 50.76%，表明 LVLM 特征在细粒度任务上对扰动更敏感。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/016_Table_5.jpg]]
*Table 5: Classification results of LVLMs’ original and perturbed visual features on the fine-grained dataset CUB-200-2011 and the generic dataset CIFAR-100. “Origin” refers to results with original features, while “Perturbed” indicates results with perturbed features*

### 6.5 消融实验总结

| 实验 | 关键发现 | 证据 |
|------|----------|------|
| 对齐前后对比 | 原始视觉特征比对齐后特征平均高 3.39% | Table 4 |
| 对齐粒度一致性 | 细粒度对齐比粗粒度对齐在 Stanford Dogs 提升 2.55%，Stanford Cars 提升 1.73% | Table 4 |
| 特征扰动 | 细粒度任务上扰动导致准确率从 88.95% 降至 24.94%，通用任务仅从 93.05% 降至 50.76% | Table 5 |
| 训练范式 | 对比范式显著优于生成式和重建式 | Figure 4-7 |
| 编码器大小 | 从 B 到 L 仅提升 0.6%，从 L 到 G 仅提升 0.3% | Figure 9 |
| 数据规模 | 2B 样本训练的 EVA-CLIP 未优于 142M 样本训练的 DINOv2 | Figure 7 |

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_cVc74MLspe_Benchmarking_La/figures/002_Table_1.jpg]]
*Table 1: Training strategies of the open-source evaluated models. “DINOv2” is a purely visual model. “Con” denotes contrastive loss, “Gen” generative loss, “Mat” image-text matching loss, “Rec” reconstruction loss used in BEiT3, and “Dis” distillation loss used in DINOv2*

## 定位与知识库关联

### 7.1 与现有基准的关系

FG-BMK 填补了现有 LVLM 评估基准（如 LVLM-eHub, MMBench）在细粒度视觉任务上的空白。与这些通用基准不同，FG-BMK 专门设计了层次化粒度评估、属性识别和知识偏差分析，能够更深入地诊断 LVLM 在细粒度任务上的能力边界。

### 7.2 与专用细粒度模型的关系

实验表明，LVLM 在细粒度任务上仍落后于专用细粒度模型（如 CAP, Diao et al., 2022; Bera et al., 2022）。差距在需要精细视觉属性推理的任务上尤为显著（如 FGVC Aircraft 上差距达 29.21%）。这提示将细粒度专用模型的优势融入 LVLM 框架是一个重要的未来方向。

### 7.3 关键发现与开放问题

**关键发现**：
1. LVLM 在细粒度任务上的主要瓶颈是视觉特征在跨模态对齐过程中细粒度判别能力的退化
2. 对比学习范式比生成式或重建式范式更能保持视觉特征的细粒度判别性
3. 对齐数据中的粒度不匹配会显著损害细粒度性能
4. 训练数据中细粒度知识分布不均是导致模型识别能力不一致的主要原因
5. LVLM 在细粒度任务上对特征扰动更敏感，鲁棒性不足

**开放问题**：
1. 如何设计更有效的对齐策略，在保持视觉特征细粒度判别能力的同时实现良好的跨模态对齐？
2. 是否可以在对齐阶段引入对比学习目标（如 patch 级或区域级对比损失）来进一步保留判别性视觉信息？
3. 如何构建大规模、粒度一致的图像-文本训练数据以提升 LVLM 的细粒度性能？
4. LVLM 在细粒度属性识别（尤其是形状）上的根本限制是什么？是否可以通过专门的训练数据或模型架构改进来克服？
5. 如何将细粒度专用模型（如 CAP）的优势融入 LVLM 框架中？
6. LVLM 在细粒度任务上的鲁棒性不足是否可以通过对抗训练或其他正则化方法缓解？

## 原文 PDF

![[paperPDFs/ICLR_2026/Benchmarking_Large_Vision_Language_Models_on_Fine_Grained_Image_Tasks_A_Comprehensive_Evaluation.pdf]]
