---
title: "MMR-AD: A Large-Scale Multimodal Dataset for Benchmarking General Anomaly Detection with Multimodal Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMR_AD_A_Large_Scale_Multimodal_Dataset_for_Benchmarking_General_Anomaly_Detection_with_Multimodal_Large_Language_Models.pdf
project_link: "https://xcyao00.github.io/MMR-AD"
code_link: "https://github.com/LLaVA-VL/LLaVA-NeXT"
aliases:
- MMR-AD
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过在包含详细推理链（CoT）的MMR-AD数据集上进行后训练，并采用SFT冷启动+GRPO强化学习的训练范式，赋予模型逐步比较分析并精准定位异常的能力。
primary_logic: 构建大规模、高质量的多模态推理异常检测数据集（MMR-AD），并结合基于链式思考（CoT）的监督微调与强化学习（Anomaly-R1），可以大幅提升MLLMs的通用异常检测能力。
claims:
- MMR-AD是当前最大规模的基于推理的工业异常检测多模态数据集，包含127K图像、188个类别、395种异常类型。
- Anomaly-R1通过从CoT数据学习并由强化学习增强，在异常检测和定位上明显优于现有通用MLLMs。
- 移除推理步骤后，模型性能显著下降（MVTecAD检测准确率从88.8降至81.3），验证了推理文本的关键作用。
- 引入正常参考图像能够显著提升模型的通用异常检测能力。
---

# MMR-AD: A Large-Scale Multimodal Dataset for Benchmarking General Anomaly Detection with Multimodal Large Language Models

> [!tip] 核心洞察
> 构建大规模、高质量的多模态推理异常检测数据集（MMR-AD），并结合基于链式思考（CoT）的监督微调与强化学习（Anomaly-R1），可以大幅提升MLLMs的通用异常检测能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMR-AD: 用于评估多模态大语言模型通用异常检测的大规模多模态数据集 |
| 英文题名 | MMR-AD: A Large-Scale Multimodal Dataset for Benchmarking General Anomaly Detection with Multimodal Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.10971) · [Project](https://xcyao00.github.io/MMR-AD) · [Code](https://github.com/LLaVA-VL/LLaVA-NeXT) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | Anomaly-R1 |
| Dataset | MVTecAD, VisA |

> [!tip] 效果简介
> - MVTecAD 上，异常检测准确率 (Accuracy) 91.0 vs 75.0 (+16.0)；异常定位准确率 (Localization Accuracy) 67.7 vs 8.9 (+58.8)。
> - VisA 上，异常检测准确率 (Accuracy) 79.0 vs 65.9 (+13.1)；异常定位准确率 (Localization Accuracy) 37.9 vs 2.2 (+35.7)。

## 概述

**问题瓶颈**  
当前多模态大语言模型（MLLMs）在工业异常检测中面临一个关键瓶颈：缺乏大规模、推理导向的多模态数据集，导致其在通用异常检测与精准定位方面表现不佳。现有的多模态异常检测数据集规模有限，且大多仅提供简短描述或粗粒度位置信息，无法支撑模型学习逐步比较与推理的能力。

**核心思路**  
本文的核心洞察是：构建大规模、高质量的多模态推理异常检测数据集，并结合基于链式思考（CoT）的监督微调与强化学习，可以大幅提升MLLMs的通用异常检测能力。具体而言，作者构建了**MMR-AD**——当前最大规模的基于推理的工业异常检测多模态数据集，包含127K图像、188个类别、395种异常类型；并在此基础上提出了**Anomaly-R1**模型，通过冷启动SFT与GRPO强化学习的训练范式，赋予模型逐步比较分析并精准定位异常的能力。

**方法定位**  
Anomaly-R1以Qwen2.5-VL为底座模型，在MMR-AD数据集上进行后训练。其方法谱系融合了三个关键设计：(1) 引入正常参考图像与输入图像形成对齐图像对，为模型提供比较基准；(2) 利用强MLLM自动生成包含详细推理步骤的CoT文本作为训练监督信号；(3) 采用SFT冷启动+GRPO强化学习的训练范式，并设计包含定位一致性惩罚的奖励函数来优化模型的推理与定位能力。与AnomalyGPT（Gu et al., AAAI 2024）等先前基于MLLM的异常检测方法不同，Anomaly-R1不仅输出检测结果，还生成可解释的推理过程。

**主要结果**  
在MVTecAD和VisA两个标准工业异常检测基准上，Anomaly-R1展现出显著优势。在MVTecAD上，异常检测准确率达到91.0%（基线75.0%），异常定位准确率达到67.7%（基线8.9%）；在VisA上，检测准确率为79.0%（基线65.9%），定位准确率为37.9%（基线2.2%）。消融实验进一步揭示：移除推理文本后，MVTecAD检测准确率从91.0降至81.3，验证了CoT推理数据的关键作用；移除正常参考图像同样导致显著性能下降，表明比较式输入模式对通用异常检测具有重要价值。

## 背景与动机

### 工业异常检测的现状与范式局限

工业异常检测（Industrial Anomaly Detection, AD）是智能制造与质量控制中的核心环节，其目标是从产品图像中识别并定位偏离正常模式的缺陷区域。当前主流方法以全监督传统视觉模型为主导，这些模型通常依赖大规模标注数据，在单一类别或特定数据集上通过 AUROC 等指标衡量性能。然而，这类方法存在两个结构性瓶颈：

1. **泛化能力受限**：传统 AD 模型（如 Table 4 中列出的 HGAD、MPGD 等全监督方法）通常针对特定产品类别训练，面对新类别或未见过的异常类型时，需要重新收集标注数据并重新训练，难以实现跨类别的通用异常检测。
2. **可解释性缺失**：传统模型输出的是异常分数或热力图，无法像人类质检员一样提供基于比较分析的推理过程，这在工业场景中严重制约了人机协作与决策信任。

### 多模态大语言模型的机遇与挑战

多模态大语言模型（MLLMs）的快速发展为通用异常检测提供了新的可能性。模型如 **Qwen2.5-VL**（Bai et al., arXiv 2025）、**GPT-4o**、**Gemini-2.5-pro** 以及 **InternVL3.5-38B**（Wang et al., arXiv 2025）在通用视觉理解任务上展现了强大的能力，理论上具备通过自然语言推理来识别异常的潜力。然而，实验证据表明，这些通用 MLLMs 在工业 AD 任务上表现严重不足：

- **定位能力极差**：如 Table 4 所示，主流商业和开源 MLLMs 在 MVTecAD 上的异常定位准确率（IoU≥0.1）普遍低于 10%，几乎不具备实用价值。
- **幻觉问题严重**：如 Figure 4 和 Figure 5 所示，Qwen2.5-VL-72B 在推理过程中出现严重幻觉——将正常区域误判为异常，或完全忽略真实存在的严重缺陷（如将铜片凸起缺陷误报为异常，却忽略了明显的切割缺陷）。

造成这一落差的根本原因在于：**当前 MLLMs 缺乏面向工业异常检测的大规模、推理导向的多模态训练数据**。现有的多模态 AD 数据集（如 MMAD、Anomaly-Instruct-125K）在规模、异常类型覆盖以及推理文本质量上均存在明显不足（见 Table 3 对比），无法支撑模型学习“观察-比较-推理-定位”的完整思考链。

### 本文的核心动机与解决思路

针对上述瓶颈，本文的核心动机是：**通过构建大规模、高质量的多模态推理异常检测数据集，并设计配套的后训练范式，赋予 MLLMs 通用异常检测与精准定位的能力**。

具体而言，本文提出两个关键组件：

- **MMR-AD 数据集**：当前最大规模的基于推理的工业异常检测多模态数据集，包含 127K 图像、188 个类别、395 种异常类型，每条数据均配有详细的链式思考（Chain-of-Thought, CoT）推理文本。
- **Anomaly-R1 模型**：基于 Qwen2.5-VL 后训练的推理型异常检测模型，通过冷启动监督微调（SFT）与 GRPO 强化学习的训练范式，使模型学会逐步比较正常参考图像与输入图像，并精准定位异常区域。

这一思路的核心洞察在于：**将异常检测从“分数回归”重新定义为“推理-定位”任务，利用 CoT 数据和强化学习驱动模型在语义空间中学习异常的比较逻辑，而非仅仅拟合类别边界**。

## 核心创新

Anomaly-R1 的核心创新并非提出全新的模型架构，而是通过**训练范式、输入模态与监督信号的三重重构**，将通用多模态大语言模型（MLLM）改造为具备逐步推理能力的工业异常检测器。其关键创新点体现在以下五个维度。

### 1. 推理链驱动的训练文本（从“只给答案”到“教模型如何思考”）

传统 MLLM 在异常检测任务上的微调通常仅提供最终答案，模型缺乏对“为什么异常”以及“异常在何处”的显式学习。Anomaly-R1 利用 MMR-AD 数据集中包含详细推理步骤的链式思考（CoT）文本进行训练，迫使模型在 `<think>` 阶段执行“比较参考图像与输入图像→逐区域分析差异→判断异常类型→输出定位坐标”的完整推理流程。消融实验直接验证了这一创新的关键作用：**移除推理文本后，MVTecAD 检测准确率从 91.0 骤降至 81.3，定位准确率从 67.7 降至 53.5**（Table 5, w/o reasoning text row），揭示了推理过程本身即是性能的核心支柱。

### 2. 双图像对齐输入（从“单张判图”到“对比参照”）

现有 MLLM 异常检测方法通常仅输入单张待测图像，模型缺乏正常基准作为判断依据。Anomaly-R1 将输入重构为 `(正常参考图像, 输入图像)` 对齐图像对，通过空间对齐检索策略为每个测试样本匹配最相似的正常参考，使模型能够执行“对比分析”而非“孤立猜测”。消融实验表明，**移除正常参考图像后，MVTecAD 检测准确率降至 81.7，VisA 降至 62.5**（Table 5, w/o normal reference row），证实了对比参照机制对通用异常检测能力的显著增益。

### 3. 冷启动 SFT + GRPO 强化学习的双层训练范式（从“单纯模仿”到“探索优化”）

传统方法仅依赖监督微调（SFT），模型受限于训练数据的分布，难以在复杂场景中泛化。Anomaly-R1 采用**冷启动 SFT + GRPO 强化学习**的双阶段训练范式：首先在 MMR-AD 上进行 SFT 使模型掌握基本任务格式和推理能力，随后利用 GRPO 算法通过规则奖励进一步探索优化。奖励函数由两部分构成——图像级答案正确性奖励与定位一致性惩罚（基于 IoU 匹配，对漏检的真实边界框施加 −0.2 × N 的惩罚）。消融实验显示，**移除冷启动 SFT 直接进行 RL 会导致 MVTecAD 检测准确率暴跌至 75.1、定位仅 12.3**；而**仅保留 SFT 移除 RL 则使检测降至 84.5、定位降至 55.9**（Table 5），证明两阶段缺一不可。

### 4. 对比采样与领域知识注入（从“盲目推理”到“有据可依”）

在推理阶段，Anomaly-R1 引入两项关键增强：**对比采样**确保每组查询同时包含正负样本响应，迫使模型学习判别性特征；**领域知识注入**在提示词中显式提供类别特定的异常类型列表（如“在 <类别名> 样本中，可能出现以下异常类型：<类别特定异常>”），引导模型聚焦于领域相关的异常模式。消融实验证实，领域知识注入带来了显著的性能提升，揭示**领域知识的缺失是通用 MLLM 在工业异常检测中的主要瓶颈**（Table 5, w/ domain knowledge vs w/o）。

### 5. 规则驱动的强化学习奖励设计（从“模糊对齐”到“精准定位”）

传统 RLHF 依赖人类偏好模型，成本高昂且难以定义工业场景的精确奖励。Anomaly-R1 利用异常检测任务具有明确真值标签的特性，设计了纯规则驱动的奖励函数：`Result Reward` 对图像级分类正确性给予正向激励，`Consistency Penalty` 对定位边界框与真值之间的不匹配施加惩罚。这一设计使模型在 GRPO 优化过程中能够同时追求“判得对”与“定得准”，直接推动了定位能力的大幅跃升——在 MVTecAD 上定位准确率从基线的 8.9 提升至 67.7（Table 4）。

---

**创新总结**：Anomaly-R1 的方法论贡献不在于模型结构的改动，而在于通过 CoT 推理文本、双图像对比输入、冷启动 SFT+GRPO 训练范式、对比采样与领域知识注入这五项相互协同的设计，系统性地解决了通用 MLLM 在工业异常检测中“不会推理、缺乏参照、定位模糊”的三大核心缺陷。

## 整体框架

Anomaly-R1 的整体框架围绕“多模态推理数据集构建 → 冷启动监督微调 → 强化学习精炼”三条主线展开，其核心目标是将通用多模态大语言模型（MLLM）改造为具备逐步比较分析与精准定位能力的工业异常检测模型。

**输入**：系统接收一个对齐图像对——一张正常参考图像和一张待检测的输入图像。正常参考图像通过空间对齐检索策略从测试正常样本中选取，以确保与输入图像在空间结构上高度匹配。同时，模型在推理时被注入类别特定的领域知识提示，明确告知该类别可能出现的异常类型。

**文本生成流水线**：为获得包含详细推理步骤的链式思考（CoT）文本，作者构建了一套自动化标注流水线。该流水线以（参考图像，输入图像）对齐图像对为输入，利用强MLLM **Qwen2.5-VL-72B**（Bai et al., arXiv 2025），配合结构化的指令模板，自动生成基于逐步比较分析的推理文本。生成的文本包含 `<think>` 推理过程和 `<answer>` 最终答案两部分，并通过将预测异常区域与真实标注区域进行一致性比对来验证文本正确性。所有数据均经过人工检查，低质量样本被剔除，异常区域的边界框和文本标签由人工标注。

**训练范式**：Anomaly-R1 以 **Qwen2.5-VL** 为底座模型，采用 LoRA 适配器进行参数高效微调。训练分为两个阶段：
1. **冷启动监督微调（SFT）**：首先在 MMR-AD 数据集上进行监督微调，使模型学习异常检测任务的基本格式和推理能力，为后续强化学习提供稳定的初始化。
2. **GRPO 强化学习**：以 SFT 模型为初始策略，采用 GRPO 作为强化学习优化算法。奖励函数由两部分组成——图像级答案正确性奖励和定位一致性惩罚（基于预测边界框与真实边界框的 IoU 匹配，对漏检的真实框施加 −0.2×N 的惩罚）。同时引入对比采样策略，确保每组查询响应中同时包含正样本和负样本，以增强对比学习信号。

**输出**：模型最终输出包含显式推理过程（`<think>` 部分）和结构化最终答案（`<answer>` 部分），后者给出异常存在性判断以及异常区域的边界框坐标。

### 补充图表

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/001_Figure_1.jpg]]
*Figure 1: (a) Overview of our MMR-AD dataset. (b) Visualization of the anomaly detection (AD) and anomaly localization (AL) accuracy comparison. Through post-training on our MMR-AD dataset, our finetuned Anomaly-R1-7B shows remarkable performance improvement, especially in anomaly localization*

## 核心模块与公式推导

### 空间对齐正常参考图像检索

为每个测试样本检索最匹配的正常参考图像，是构建（参考图像，输入图像）对齐图像对的关键前置模块。该模块采用空间对齐检索策略，通过计算输入图像 $I$ 与第 $i$ 张正常图像之间的空间对齐度 $D_{align}^i$ 来度量匹配程度：

$$D_{align}^i \triangleq \frac{1}{S^2 - \tau} \sum_{j=1}^{S^2 - \tau} D_j^i, \quad i = 1,2,\dots,N$$

其中 $S^2$ 为图像分块总数，$\tau$ 为截断阈值，$D_j^i$ 表示排序后的块间 KL 散度。该度量通过平均排序后的块间分布差异，筛选出空间结构最相似的正常样本作为参考图像。消融实验表明，移除正常参考图像后，MVTecAD 检测准确率从 91.0 降至 81.7，定位准确率从 67.7 降至 62.1，验证了该模块的核心价值。

### 基于强 MLLM 的 CoT 文本自动生成

MMR-AD 数据集的核心竞争力在于其包含详细的推理链文本，而非仅提供最终答案。该模块利用 **Qwen2.5-VL-72B**（Bai et al., arXiv 2025）作为文本生成器，以（参考图像，输入图像）对齐图像对和结构化指令模板为输入，自动生成包含 `<think>` 推理过程和 `<answer>` 最终答案的结构化文本。生成文本需通过一致性验证：从 `<answer>` 中提取预测异常区域，与真实标注区域进行比对，仅保留一致的文本数据。这一自动化流水线使 MMR-AD 成为当前最大规模的基于推理的工业异常检测多模态数据集（127K 图像、188 类别、395 异常类型）。

### GRPO 强化学习优化目标

Anomaly-R1 在冷启动 SFT 之后，采用 GRPO（Group Relative Policy Optimization）进行强化学习训练，以进一步提升模型的推理与定位能力。GRPO 的优化目标函数为：

$$\mathbb{E}_{q \sim \mathcal{D}, \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}(\cdot|q)} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \min \left( w_{i,t}(\theta) \hat{A}_{i,t}, \operatorname{clip}(w_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t} \right) - \beta D_{KL}(\pi_\theta || \pi_{ref}) \right]$$

其中各变量含义如下：

- **$q$**：从数据分布 $\mathcal{D}$ 中采样的查询样本。
- **$G$**：每组采样的响应数量。
- **$o_i$**：策略 $\pi_{\theta_{old}}$ 对查询 $q$ 生成的第 $i$ 个输出序列。
- **$|o_i|$**：输出序列 $o_i$ 的 token 长度。
- **$w_{i,t}(\theta)$**：token 级别的重要性比率，衡量当前策略与旧策略在位置 $t$ 的生成概率比。
- **$\hat{A}_{i,t}$**：组归一化优势估计。
- **$\epsilon$**：裁剪超参数，限制策略更新幅度。
- **$\beta$**：KL 惩罚系数，防止策略偏离参考策略 $\pi_{ref}$ 过远。

### 重要性比率与组归一化优势

GRPO 的核心在于 token 级别的重要性比率和基于组内相对比较的优势估计：

$$w_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t} | q, o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t} | q, o_{i,<t})}; \quad \hat{A}_{i,t} = \frac{r_i - \operatorname{mean}(\{r_i\}_{i=1}^G)}{\operatorname{std}(\{r_i\}_{i=1}^G)}$$

- **$w_{i,t}(\theta)$**：当前策略 $\pi_\theta$ 与旧策略 $\pi_{\theta_{old}}$ 在给定前缀 $o_{i,<t}$ 下生成 token $o_{i,t}$ 的概率比值，用于控制策略更新的置信区间。
- **$\hat{A}_{i,t}$**：对第 $i$ 个响应的总奖励 $r_i$ 进行组内标准化（减去均值、除以标准差）得到的优势估计，使奖励信号在不同样本组间可比。

### 奖励函数设计

GRPO 的奖励信号 $r_i$ 由两部分组成：

1. **图像级答案奖励（Result Reward）**：根据模型输出的最终答案（正常/异常判定及异常类型）与真实标签的匹配程度给予正向奖励。
2. **定位一致性惩罚（Consistency Penalty）**：对未检测到的真实边界框施加惩罚，具体为 $-0.2 \times N$，其中 $N$ 为漏检的真实边界框数量。该惩罚通过 IoU 匹配机制实现，鼓励模型输出与真实标注一致的精确边界框坐标。

消融实验表明，移除强化学习阶段（仅保留 SFT）后，MVTecAD 检测准确率从 91.0 降至 84.5，定位准确率从 67.7 降至 55.9，验证了 GRPO 训练范式的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/002_Figure_2.jpg]]
*Figure 2: The illustration of the text generation pipeline. We utilize the (reference, input) image pair and leverage Qwen2.5- VL-72B to automate the generation of reasoning-based texts. We prompt the model to generate the reasoning-based AD thinking process (i.e., based on comparison and analysis of the two images). To ensure that the model can correctly recognize abnormal areas, we plot red bboxes on the image as visual hints and also provide the anomaly types and bbox coordinates of the abnormal areas as text hints to the instruction. In the generated texts, the red parts mark the anomaly-related reasoning words*

## 实验与分析

### 主实验结果

**Anomaly-R1** 在 MVTecAD 和 VisA 两个工业异常检测基准上均显著超越所有通用 MLLM 基线。Table 4 报告了核心指标对比：

- **MVTecAD 异常检测准确率**：Anomaly-R1 达到 **91.0%**，较最佳开源基线 InternVL3.5-38B 的 75.0% 提升 **+16.0 个百分点**。商业模型 GPT-4o 和 Gemini-2.5-pro 分别仅取得 72.2% 和 77.8%，说明通用 MLLM 在工业场景存在严重能力缺口。
- **MVTecAD 异常定位准确率**：Anomaly-R1 达到 **67.7%**，而所有基线模型的定位准确率均低于 10%（Qwen2.5-VL-72B 仅 8.9%），提升幅度高达 **+58.8 个百分点**。这揭示了通用 MLLM 在精细空间定位上的根本性不足。
- **VisA 数据集**：检测准确率从基线最优的 65.9% 提升至 **79.0%**（+13.1），定位准确率从 2.2% 提升至 **37.9%**（+35.7）。VisA 上定位指标的绝对数值较低，反映该数据集的异常形态更为复杂多样。

值得注意的是，传统全监督 AD 模型（如 HGAD）在 MVTecAD 上可达 96.2% 的检测准确率，但其依赖像素级标注且按 AUROC 评估，与 MLLM 的文本输出评估范式不可直接比较。Anomaly-R1 的核心优势在于**同时具备检测、定位与自然语言推理能力**，这是传统模型无法实现的。

### 消融实验分析

Table 5 的系统消融揭示了各设计组件的因果贡献：

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/007_Table_5.jpg]]
*Table 5: Further analysis experiments. We investigate the impact of Reasoning-based Text, Normal Reference Image, Cold Start Initialization, Contrastive Sampling, and Domain knowledge*

**1. 推理文本的关键作用。** 移除 `<think>` 部分的 CoT 推理文本后，MVTecAD 检测准确率从 91.0% 骤降至 81.3%，定位准确率从 67.7% 降至 53.5%；VisA 上检测从 79.0% 降至 66.1%，定位从 37.9% 降至 18.8%。这表明**逐步比较分析的推理过程**是模型精准判别异常的核心机制，而非简单的答案记忆。

**2. 正常参考图像的必要性。** 移除参考图像后，MVTecAD 检测准确率降至 81.7%，定位降至 62.1%；VisA 检测降至 62.5%，定位降至 24.9%。参考图像提供了“正常基准”，使模型能够通过对比发现细微偏差，在无参考场景下性能退化显著。

**3. 冷启动 SFT 的奠基作用。** 跳过 SFT 直接进行 RL 训练，MVTecAD 检测准确率仅为 75.1%，定位仅 12.3%。这说明 RL 的探索空间过于庞大，缺乏 SFT 提供的合理初始化将导致训练崩溃或收敛到次优解。

**4. 强化学习的增益。** 仅使用 SFT 而不进行 RL，MVTecAD 检测准确率为 84.5%，定位为 55.9%。RL 阶段通过**答案正确性奖励与定位一致性惩罚**的联合优化，进一步提升了约 6.5 个百分点的检测准确率和 11.8 个百分点的定位准确率。

**5. 对比采样与领域知识。** 移除对比采样策略导致性能下降，验证了在 RL 训练中保证每组响应均包含正负样本的重要性。注入类别特定的异常类型知识提示后性能显著提升，揭示**领域知识匮乏是通用 MLLM 在工业 AD 中的主要瓶颈之一**。

### 失败模式与定性分析

Figure 4 和 Figure 5 展示了基线模型 Qwen2.5-VL-72B 的典型幻觉现象：模型在未观察到实际缺陷时虚构异常类型（如将正常样本误判为“铜突缺陷”），或忽略明显的切割缺陷而关注无关区域。Figure 6 显示即使检测正确，定位边界框仍不够精确。Figure 7 和 Figure 8 展示了 Anomaly-R1 的失效案例，主要表现为推理逻辑错误和边界框坐标偏差，说明在复杂异常形态下模型的细粒度空间理解仍有提升空间。

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/009_Figure_4.jpg]]
*Figure 4: Green marks correct reasoning and correct bbox coordinates, red marks wrong reasoning and imprecise bbox coordinates. Qwen2.5-VL-72B shows severe hallucination, thinking that there is an abnormal dark spot, and locating to the white area at the bottom of the image*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/011_Figure_5.jpg]]
*Figure 5: Green marks correct reasoning and correct bbox coordinates, red marks wrong reasoning and imprecise bbox coordinates. Both GPT-4o and Qwen2.5-VL-72B show hallucination, thinking that there is the copper protrusion defect without observing the severe cut defect*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/008_Figure_6.jpg]]
*Figure 6: Green marks correct reasoning and correct bbox coordinates, red marks wrong reasoning and imprecise bbox coordinates. Although both GPT-4o and Qwen2.5-VL-72B generate correct reasoning, the anomaly localization results are still not precise enough*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/010_Figure_7.jpg]]
*Figure 7: Failure case. Red marks wrong reasoning*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/012_Figure_8.jpg]]
*Figure 8: Failure case. Red marks wrong reasoning and incorrect bbox coordinates*

### 局限性与开放问题

当前方法存在四个主要局限：（1）数据集和模型均针对工业场景设计，不适用于医学或视频异常检测；（2）依赖边界框标注，无法输出像素级分割结果；（3）CoT 文本由 Qwen2.5-VL-72B 自动生成，存在偏差和错误风险；（4）性能高度依赖正常参考图像的质量与空间对齐程度。这些局限指向三个开放问题：能否在无参考图像场景下仅依靠领域知识实现可靠检测？如何将定位能力从边界框扩展到像素级分割？CoT 文本的质量验证流程能否完全消除文本-图像不一致的噪声？

### 补充图表

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/003_Table_1.jpg]]
*Table 1: Statistics on the composition of our MMR-AD dataset*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/004_Table_3.jpg]]
*Table 3: Comparison with previous multi-modal AD datasets on different attributes. ✘: no reasoning text. ✔✗: short description text. ✔: detailed reasoning text. “coarse” means anomalous location is described in coarse-grained words, such as “top left”, “bottom right”, etc. “precise” means anomalous location is described in fine-grained coordinates, such as “[xmin, ymin, xmax, ymax]”. In Anomaly-Instruct-125K, there is no defect type label given for each sample, thus the “Defect Types” column is hard to count*

![[assets/figures/papers/paper_list_l2746_https_arxiv_org_abs_2604_10971/figures/006_Table_4.jpg]]
*Table 4: Performance evaluation of anomaly detection and localization for both commercial and open-source MLLMs. All the MLLMbased models (except AnomalyGPT) are based on the (reference, input) image pair as the image input and use the instruction template in Tab.2 for generation. ·/· means anomaly detection/localization metrics, respectively. Anomaly-R1-7B† is a variant in which we add domain knowledge (see Sec.4.1). Bold means the best performance (the full-shot AD models are not included in the comparison)*

## 方法谱系与知识库定位

### 1. 与基线工作的关系

Anomaly-R1 的核心定位是**基于推理链（CoT）与强化学习的通用异常检测 MLLM**。其直接底座模型为 **Qwen2.5-VL-7B** 和 **Qwen2.5-VL-72B**（Bai et al., arXiv 2025），通过 LoRA 适配器进行参数高效微调。与现有工作的关系可从以下几个维度梳理：

**（1）与通用 MLLM 基线的对比。** 论文在统一评估协议下（相同的「参考图像–输入图像」对、相同的指令模板 Tab.2）测试了多个商业与开源 MLLM，包括 **GPT-4o**、**Gemini-2.5-pro**、**InternVL3.5-38B**（Wang et al., arXiv 2025）以及底座模型 Qwen2.5-VL 系列。这些通用 MLLM 在 MVTecAD 上的异常检测准确率最高仅 75.0%，定位准确率仅 8.9%（Table 4），表明**通用视觉语言能力不足以直接迁移到工业异常检测任务**，尤其在需要精确空间定位的场景下表现极弱。Anomaly-R1-7B†（注入领域知识）将检测准确率提升至 85.7%，定位准确率提升至 67.7%，验证了领域后训练的必要性。

**（2）与先前 MLLM-based 异常检测方法的对比。** **AnomalyGPT**（Gu et al., AAAI 2024）是此前基于 MLLM 的异常检测代表工作，但其训练数据缺乏详细推理链，且输入仅为单张图像。Table 4 显示 AnomalyGPT 在 MVTecAD 上的检测准确率为 74.1%，定位准确率为 7.9%，显著低于 Anomaly-R1。这揭示出**推理文本（reasoning text）和正常参考图像**是拉开性能差距的两个关键设计槽位。

**（3）与传统全监督 AD 模型的对比。** 论文在 Table 4 中列出了 **HGAD**、**RD++**、**DeSTSeg** 等全监督异常检测模型作为参照，其中 HGAD 在 MVTecAD 上达到 96.2% 的检测准确率。但需注意：传统 AD 模型使用 AUROC 指标，而 MLLM 类模型直接输出文本答案，采用准确率/召回率/精确率评估，**两类方法的数值不可直接比较**。这一差异源于评估范式的根本不同——传统模型输出连续异常分数，MLLM 输出离散的语义判断。

### 2. 适用边界

**（1）领域边界。** MMR-AD 数据集覆盖 188 个类别、395 种异常类型，但全部来自工业场景（MVTecAD、VisA、WFDD、CSDD 等工业异常检测基准）。论文明确指出该方法**不适用于医学异常检测或视频异常检测**领域。在跨领域泛化方面，目前缺乏实验证据，需手动验证。

**（2）输入依赖边界。** 方法的核心前提是**存在可获取的正常参考图像**。消融实验（Table 5）表明：移除正常参考图像后，MVTecAD 检测准确率从 91.0% 降至 81.7%，VisA 从 79.0% 降至 62.5%。这意味着在无参考图像的单样本检测场景下，性能退化严重。此外，参考图像的质量和空间对齐程度直接影响检测效果——论文采用基于 KL 散度的空间对齐检索策略来匹配最优参考图像，但该策略本身存在对齐误差风险。

**（3）输出粒度边界。** 当前方法依赖边界框（bbox）标注进行训练和监督，**无法直接输出像素级分割结果**。在 Table 4 中，即使是表现最好的 Anomaly-R1-7B†，MVTecAD 定位准确率也仅 67.7%，VisA 仅 37.9%，说明精细空间定位仍是瓶颈。Figure 6 的定性案例也显示，即使推理正确，bbox 坐标仍不够精确。

**（4）训练数据依赖边界。** CoT 文本的生成依赖强 MLLM（Qwen2.5-VL-72B）和人工标注的 bbox 提示信息。文本质量验证流程通过比较 `<answer>` 中预测异常区域与真实异常区域的一致性进行过滤，但**无法完全保证 CoT 推理步骤的语义正确性**——可能存在文本与图像不一致的潜在噪声，影响模型训练的稳定性。

### 3. 局限与开放问题

**已知局限：**

- **参考图像依赖**：在无正常参考图像的场景下性能显著下降，限制了其在完全无监督或单样本场景中的应用。
- **输出粒度受限**：仅支持 bbox 级定位，无法满足需要像素级分割的精细工业检测需求。
- **CoT 数据质量风险**：推理文本由强 MLLM 自动生成，尽管经过一致性验证，仍存在偏差和错误传播的风险。
- **领域泛化未验证**：训练和评估均限于工业场景，在医学、遥感、视频等异常检测领域的适用性未知。

**开放问题：**

1. **无参考图像的可靠检测**：该方法是否能在完全无正常参考图像的情况下，仅依靠领域知识提示实现可靠的异常检测？当前消融实验显示移除参考图像后性能大幅下降，但未探索仅凭领域知识补偿的可能性。

2. **从 bbox 到 pixel-level 的扩展**：如何将现有的 bbox 级定位扩展到像素级分割输出？这需要改变奖励函数设计（从 IoU 匹配转向 mask 匹配）和输出格式定义，是方法层面的重要扩展方向。

3. **CoT 文本质量的严格保证**：MMR-AD 数据集中 CoT 文本的质量验证流程能否完全保证无错误？是否存在文本描述与图像内容不一致的潜在噪声影响模型训练？论文未对此进行系统的噪声鲁棒性分析。

4. **跨领域迁移机制**：工业异常检测中学习的“正常–异常”比较推理模式是否可迁移到医学或视频领域？这需要新的基准数据集和迁移实验来验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/MMR_AD_A_Large_Scale_Multimodal_Dataset_for_Benchmarking_General_Anomaly_Detection_with_Multimodal_Large_Language_Models.pdf]]
