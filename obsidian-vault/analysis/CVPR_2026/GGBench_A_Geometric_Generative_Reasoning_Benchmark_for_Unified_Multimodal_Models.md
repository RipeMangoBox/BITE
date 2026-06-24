---
title: "GGBench: A Geometric Generative Reasoning Benchmark for Unified Multimodal Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GGBench_A_Geometric_Generative_Reasoning_Benchmark_for_Unified_Multimodal_Models.pdf
code_link: null
aliases:
- GGBench
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过要求模型生成可执行的GeoGebra代码，将推理过程与几何操作严格对齐，从而强制实现从语言到图形的精确映射，并提供完全可自动化的验证手段。
primary_logic: 几何构造任务天然融合语言理解、多步空间推理和结构化视觉生成；提供文本-代码-图像三重对齐的数据，使得能够全面评估模型的集成生成式推理能力，而不仅仅是孤立的理解或生成能力。
claims:
- 端到端图像生成模型（如Nano Banana）的构造质量（VLM-I=33.82）远低于基于代码生成的模型（如GPT-5，VLM-I=57.08），证明直接生成无法保证几何正确性。
- GGBench为每个构造步骤提供可执行GeoGebra代码，使评估能够自动验证几何正确性和一致性。
- 基于代码的顶尖模型GPT-5在GGBench-Code上达到79.02%的pass@1，并获得最高的VLM-I和人类评分，显示出代码管道在生成式推理上的有效性。
- 自动VLM评分与人类专家评分高度相关（r=0.9295），验证了该基准的评估可靠性。
---

# GGBench: A Geometric Generative Reasoning Benchmark for Unified Multimodal Models

> [!tip] 核心洞察
> 几何构造任务天然融合语言理解、多步空间推理和结构化视觉生成；提供文本-代码-图像三重对齐的数据，使得能够全面评估模型的集成生成式推理能力，而不仅仅是孤立的理解或生成能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | GGBench: 面向统一多模态模型的几何生成式推理基准 |
| 英文题名 | GGBench: A Geometric Generative Reasoning Benchmark for Unified Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.11134) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | GGBench |
| Dataset | GGBench, GGBench-Code |

> [!tip] 效果简介
> - GGBench (Overall VLM-I) 上，VLM-I (综合视觉评分) 57.08 (GPT-5, code-based best) vs 33.82 (Nano Banana, end-to-end UMM best) (+23.26)。
> - GGBench-Code (Execution Accuracy) 上，Pass@1 (代码执行通过率) 79.02 (GPT-5) vs 40.39 (DeepSeek-R1) (+38.63)。
> - GGBench (Human Evaluation) 上，Human Score (人工评分的整体质量) 83.06 (GPT-5) vs 78.44 (DeepSeek-V3.1) (+4.62)。

## 概述

**问题瓶颈**：现有的统一多模态模型（UMMs）在需要根据自然语言描述精确生成几何图形时普遍失败。其根本原因在于，这些模型无法将抽象的几何推理转化为精确、可执行的构造步骤，且缺乏代码级的可验证性，导致生成的图形频繁违反几何约束。

**核心洞察**：几何构造任务天然融合了语言理解、多步空间推理和结构化视觉生成。通过要求模型生成可执行的GeoGebra代码，将推理过程与几何操作严格对齐，可以实现从语言到图形的精确映射，并提供完全可自动化的验证手段。

**GGBench的定位**：GGBench是一个面向统一多模态模型的几何生成式推理基准，其独特之处在于为每个构造步骤提供文本-代码-图像三重对齐的数据（Figure 2），从而能够全面评估模型的集成生成式推理能力，而非孤立地考察理解或生成能力（Figure 1）。

**方法谱系与知识库定位**：现有数学多模态基准（如MathVista、MathVerse等）通常仅覆盖文本和图像两种模态，评估形式多为选择题或开放性文本生成，依赖与参考答案的匹配评分。GGBench的关键改进在于：
- **评估模式转变**：从答案匹配转向端到端的几何构造生成，通过可执行代码和最终图形的几何正确性进行验证。
- **三模态监督**：在文本和图像之外引入可执行GeoGebra代码，每个推理步骤均由代码锚定，实现了100%的文本-代码-图像对齐。
- **过程验证**：包含中间构造步骤的逐步评估，量化步骤准确性和过程一致性，而非仅评估最终答案或单一图像。

**主要结果**：
- 端到端图像生成模型（如Nano Banana）的构造质量（VLM-I=33.82）远低于基于代码生成的模型（如GPT-5，VLM-I=57.08），差距达+23.26点，直接证明直接生成无法保证几何正确性。
- 基于代码的顶尖模型GPT-5在GGBench-Code上达到79.02%的pass@1，并获得最高的VLM-I和人类评分（Human=83.06），显示出代码管道在生成式推理上的有效性。
- 自动VLM评分与人类专家评分高度相关（Pearson r=0.9295），验证了该基准的评估可靠性。

**当前局限**：GGBench目前仅限于2D几何构造任务，能否推广到3D几何或其他需要生成式推理的领域（如科学图解生成、化学结构图等）仍有待验证。基准构建严重依赖LLM生成训练数据，即使经过多轮人工审核，仍可能引入模型偏好或系统性错误。此外，自动评估VLM虽与人类评分高度相关，但在某些几何细节上仍可能存在打分偏差。

## 背景与动机

### 统一多模态模型的能力瓶颈

近年来，统一多模态模型（Unified Multimodal Models, UMMs）在视觉理解和图像生成两个维度上分别取得了显著进展。现有基准通常将这两类能力割裂评估：理解类基准（如数学推理、图表问答）仅考察模型对视觉输入的语义解析，而生成类基准（如文本到图像的合成）仅衡量视觉输出的感知质量。然而，现实世界中的复杂任务往往要求模型同时具备理解、推理和生成三种能力的有机集成——即“生成式推理”（generative reasoning）。

几何构造任务正是这一集成能力的天然试金石。一个典型的几何构造问题要求模型：首先理解自然语言描述的几何约束，然后规划多步构造序列（推理），最终生成精确满足所有约束的几何图形（生成）。这一过程将语言理解、空间推理和结构化视觉生成紧密耦合，任何一个环节的断裂都会导致最终输出违反几何正确性。

### 现有基准的结构性缺陷

现有面向数学与几何的多模态基准存在三个系统性缺口：

**孤立的能力评估。** 如 Table 3 所示，主流基准要么仅覆盖理解维度，要么仅覆盖生成维度，几乎没有基准同时要求理解和生成。即便少数基准涉及多步推理，其评估方式也停留在选择题答案或开放性文本的匹配评分上，无法验证推理过程是否真正导向了正确的视觉输出。

**缺乏可执行的验证锚点。** 传统基准仅提供文本-图像对作为参考，评估依赖于与参考答案的模糊匹配或人工评判。当模型生成的图形与参考图像在视觉上相似但几何结构错误时，像素级指标（如PSNR、SSIM）往往无法捕获这类缺陷——事实上，GGBench的实验表明，像素质量指标与几何有效性的相关性很弱，高感知相似度可能掩盖严重的结构错误。

**模态监督不完整。** 现有基准的监督信号通常仅限于文本和图像，缺少将推理步骤与可执行操作精确对齐的中间表示。这导致两个后果：一是无法对推理过程进行逐步验证，二是难以区分模型是“真正理解了几何约束”还是“碰巧生成了看似合理的图形”。

### GGBench的动机与设计哲学

GGBench的核心动机正是弥合上述缺口。其设计哲学基于一个关键洞察：**几何构造任务天然融合语言理解、多步空间推理和结构化视觉生成；提供文本-代码-图像三重对齐的数据，使得能够全面评估模型的集成生成式推理能力，而不仅仅是孤立的理解或生成能力。**

具体而言，GGBench通过以下机制实现突破：

- **以可执行代码作为验证锚点**：每个构造步骤均提供对应的GeoGebra代码，使评估能够自动验证几何正确性和一致性（Figure 2）。这从根本上解决了传统基准中“看起来对”但“实际上错”的验证困境。
- **三重模态对齐**：GGBench实现了文本（逐步推理计划）、代码（可执行构造）和图像（渲染图形）之间的100%对齐（Table 3），每个推理步骤均由代码锚定，使得过程性评估成为可能。
- **从孤立评估到集成评估的范式转变**：如 Figure 1 所示，GGBench将评估范式从“理解或生成”的二选一推进到“理解与生成”的集成，要求模型完成从自然语言指令到精确几何图形的完整生成式推理链路。

这一设计使得GGBench不仅是一个新的测试集，更是一种评估方法论——它强制模型将抽象推理转化为可执行的构造步骤，从而暴露当前统一多模态模型在集成生成式推理能力上的真实水平与结构短板。

## 核心创新

GGBench 的核心创新并非提出一种新的模型架构或训练算法，而是**重新定义了统一多模态模型（Unified Multimodal Models, UMMs）的评估范式**——从孤立的理解或生成评测，转向对“集成生成式推理”能力的系统性检验。这一范式转移通过三个紧密耦合的 **changed slots** 实现，每一个都直接针对现有基准的根本性缺陷。

### 从答案匹配到可执行构造验证

现有数学与多模态基准（如 MathVista、MathVerse）的评估模式本质上是**答案匹配**：模型输出选择题选项或开放性文本，评分依赖于与参考答案的字符串或语义相似度。这种模式无法捕捉几何构造任务的核心要求——生成的图形必须在欧氏几何约束下严格成立。GGBench 将评估对象切换为**端到端的几何构造生成**，要求模型（或模型管线）产出完整的几何图形，并通过两条互补路径验证其正确性：

1. **代码执行验证**：对于 Track B 的代码驱动模型，GGBench 提供每个构造步骤的可执行 GeoGebra 代码作为真值（Figure 2），评估时直接检验模型生成的代码能否成功执行并产生几何正确的图形。这从根本上消除了语义模糊性——代码要么通过解析器并满足约束，要么失败。
2. **视觉几何评判**：对于 Track A 的端到端图像生成模型（无法产出代码），以及 Track B 模型渲染后的最终图形，GGBench 采用冻结的 VLM 评判器（GPT-4o）从几何一致性、约束满足和视觉质量等维度进行结构化评分（VLM-I、VLM-I-Res 等指标）。

这种双轨验证机制的关键证据来自 Table 4 和 Table 5：端到端模型中的最优者 Nano Banana 仅获得 VLM-I = 33.82，而基于代码生成的 GPT-5 达到 57.08（提升 +23.26 点）。这一巨大差距直接证实了“直接像素生成无法保证几何正确性”的核心论断，也验证了可执行代码作为评估锚点的必要性。

### 文本-代码-图像三重对齐的监督信号

传统多模态基准仅提供文本和图像两种模态的监督，缺乏中间推理过程的结构化锚定。GGBench 引入了**文本-代码-图像三重对齐**的数据结构（Table 3，100% 覆盖），其中每个构造步骤同时具备：

- **文本**：自然语言的逐步推理描述
- **代码**：对应的可执行 GeoGebra 命令序列
- **图像**：执行代码后渲染的几何图形

这一设计的关键价值在于将抽象的几何推理过程**物化为可检验的中间产物**。评估不再仅关注最终图形，而是可以深入到每个中间步骤的准确性和一致性（VLM-I-Mid 指标，Figure 15、Figure 16）。这种细粒度的过程监督使得基准能够区分“碰巧生成正确图形”与“真正理解构造逻辑”的模型行为，为诊断模型的推理缺陷提供了前所未有的分辨率。

### 逐步过程验证与多维度能力剖析

GGBench 的四阶段评估协议（Planning → Middle Process → Final Result → Overall Scores）将生成式推理分解为可独立量化的子能力。Table 4 的结果揭示了不同模型类型的差异化表现模式：

- **端到端 UMMs** 在 Planning 阶段（VLM-T）表现尚可（Nano Banana 58.54，接近 GPT-4o 的 59.73），但在 Middle Process 和 Final Result 阶段急剧恶化，表明其瓶颈在于将文本规划转化为精确几何操作的能力。
- **代码驱动模型**在各阶段表现更均衡，GPT-5 在 GGBench-Code 上达到 79.02% 的 Pass@1，且获得最高的人类评分（83.06），证明代码管道能有效桥接语言理解与几何执行。

此外，按构造类别的细分分析（Figure 5）显示，所有模型在“测量与比例”和“几何定理应用”等需要抽象推理的类别上 VLM-I 分数普遍下降 10–15 点，揭示了当前模型在深层几何理解上的共性短板。这种多维度的能力剖析能力，是仅提供单一总分或答案正确率的传统基准所不具备的。

综上，GGBench 的三个 changed slots 构成了一个逻辑闭环：**可执行验证**提供了客观的评判标准，**三重对齐**锚定了推理过程，**逐步评估**实现了能力的精细解耦。三者共同推动了多模态评估从“结果导向”向“过程导向”的范式升级。

## 整体框架

GGBench 的整体构建与评估框架围绕一个核心瓶颈展开：**现有统一多模态模型（UMMs）无法将抽象几何推理转化为精确的可执行构造步骤**，导致直接生成的图形频繁违反几何约束。为解决这一问题，GGBench 建立了一条从数据构建到模型评估的完整流水线，其核心思想是通过要求模型生成可执行的 GeoGebra 代码，将推理过程与几何操作严格对齐，从而实现从语言到图形的精确映射和完全自动化的验证。

### 数据构建流水线

GGBench 的数据构建采用六阶段流水线（Figure 3），每个阶段均由 LLM 辅助完成并辅以人工审核：

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/007_Figure_3.jpg]]
*Figure 3: Overview of the GGBench data construction pipeline*

1. **候选池收集（阶段 a）**：从网络中广泛搜索公开的几何构造问题，构建初始候选池。
2. **LLM 辅助标注与筛选（阶段 b）**：使用 LLM 对候选问题进行“可构造性”判别，通过单 token 决策（true/false）进行高通量自动分流，再由人工检查确认。
3. **提示设计与问题适配（阶段 c–d）**：设计复合提示模板，将原始问题改写为面向几何构造的声明形式，确保文本指令与后续执行步骤对齐。
4. **解答生成（阶段 e）**：由 GPT-5 作为核心生成引擎，同步输出逐步推理文本、可执行 GeoGebra 代码以及渲染的示意图，形成文本-代码-图像三重对齐的样本。
5. **自动审核与专家定稿（阶段 f）**：LLM 自动检查代码的可执行性、逻辑连贯性和图形正确性，输出严格的 0/1 评分，最终由领域专家核准。

经过上述流水线，GGBench 最终保留了 **1,411 个高质量几何构造问题**，包含 7,165 张图像，覆盖 8 个推理类别和 3 个难度级别（Table 1、Table 2）。

### 评估流水线

GGBench 的评估采用**四阶段协议**（Section 4.2），全面衡量模型的生成式推理能力：

1. **规划阶段（Planning）**：评估模型生成的文本推理步骤的逻辑性和几何合理性（VLM-T 指标）。
2. **中间过程（Middle Process）**：评估构造过程中间步骤的准确性和过程一致性（VLM-I-Mid 指标）。
3. **最终结果（Final Result）**：评估最终渲染图形与参考解的几何一致性和约束满足度（VLM-I-Res 指标）。
4. **综合评分（Overall）**：融合上述维度的综合视觉评分（VLM-I）。

所有自动评分均由冻结的 VLM 评判模型（GPT-4o）使用固定提示完成，其评分与人类专家评分高度相关（Pearson r = 0.9295），验证了评估的可靠性。

### 两条评估轨道

为全面对比不同技术路线，GGBench 设置了两条评估轨道：

- **Track A（端到端 UMMs）**：模型直接根据文本描述生成最终图形，评估对象包括 Qwen-Image、Seedream 4.0、Janus、BAGEL、Nano Banana 等。
- **Track B（基于代码的 LLMs/LRMs）**：模型首先生成 GeoGebra 代码，再渲染为图形，评估对象包括 GPT-5、Claude Sonnet 4.5、Gemini-2.5-Pro、DeepSeek-R1 等。

这种双轨设计使得能够直接对比“直接生成”与“代码驱动生成”两种范式在几何构造任务上的根本差异，从而揭示当前 UMMs 在生成式推理上的真实瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/005_Figure_1.jpg]]
*Figure 1: The paradigm shift to generative reasoning. Conventional benchmarks evaluate (a) Understanding or (b) Generation in isolation. GGBench introduces (c) integrated Understanding& Generation evaluation, requiring generative reasoning from Unified Multimodal Models*

## 核心模块与公式推导

GGBench 本身是一个基准而非模型，因此其“核心模块”体现为数据构造流水线与评估协议的设计，而非可训练的神经网络组件。以下按流水线阶段与评估维度分别阐述关键模块。

### 数据构造流水线

GGBench 的数据构造遵循六阶段流水线（Figure 3），每个阶段承担明确的筛选或生成职责：

1. **候选池构建（Data Collection & Candidate Pooling）**  
   从公开网络资源中检索几何问题，形成原始候选池。

2. **LLM 辅助标注与过滤（LLM-assisted Tagging & Filtering）**  
   使用 LLM 对每个问题进行可构造性判别，输出单 token 的 true/false 决策（Figure 9），再由人工抽检确认，筛除不适合构造为 GeoGebra 任务的问题。

3. **提示设计与问题改写（Prompt Design & Problem Adaptation）**  
   将筛选后的问题通过复合提示（Figure 10）改写为面向构造的声明式描述，明确构造目标与约束，为后续代码生成对齐执行步骤。

4. **解答生成（Solution Generation, LLM-iii）**  
   由 GPT-5 同步生成三类对齐内容：逐步推理文本、可执行 GeoGebra 代码、以及每个步骤对应的渲染示意图（Figure 11）。这是实现文本-代码-图像三重对齐的核心环节。

5. **自动审核（Automated Screening, LLM-iv）**  
   LLM 自动检查代码的可执行性、字段合规性与命令级正确性，输出严格的 0/1 评分（Figure 12）。

6. **专家终审（Expert Finalization）**  
   领域专家对通过自动审核的样本进行最终核准，确保逻辑连贯性与几何正确性。

### 评估协议的四阶段结构

GGBench 采用四阶段评估协议，由冻结的 VLM 评判模型（GPT-4o）以固定提示执行，确保可复现性：

- **阶段一：规划（Planning）** — 评估文本推理步骤的逻辑性、几何合理性与结构完整性，输出 VLM-T 分数（1–5 标量，Figure 13）。
- **阶段二：中间过程（Middle Process）** — 细分为两个子维度：
  - *步骤准确性（Step Accuracy）*：检查视觉步骤与符号指令之间的对齐程度（Figure 15）。
  - *过程一致性（Process Consistency）*：检查连续构造步骤之间的视觉与逻辑连贯性（Figure 16）。
- **阶段三：最终结果（Final Result）** — 将模型生成的最终图形与参考图像比较，依据几何一致性与约束满足程度给出 VLM-I-Res 分数（1–5 标量，Figure 14）。
- **阶段四：综合评分（Overall Scores）** — 聚合前述维度，形成统一的 VLM-I 综合指标。

### 关键公式

本工作未提出新的数学公式或定理。评估中使用的指标均为标准度量，其定义在此列出以明确变量含义。

**像素级相似度指标**（用于对照实验，证明其与几何有效性弱相关）：

- **PSNR（峰值信噪比）**：
  $$ \text{PSNR} = 10 \cdot \log_{10}\left(\frac{\text{MAX}_I^2}{\text{MSE}}\right) $$
  其中 $\text{MAX}_I$ 为图像像素最大值（通常为 255），$\text{MSE}$ 为生成图与参考图之间的均方误差。PSNR 越高表示像素级保真度越高，但高 PSNR 可能掩盖结构错误。

- **SSIM（结构相似性指数）**：
  $$ \text{SSIM}(x, y) = \frac{(2\mu_x\mu_y + C_1)(2\sigma_{xy} + C_2)}{(\mu_x^2 + \mu_y^2 + C_1)(\sigma_x^2 + \sigma_y^2 + C_2)} $$
  其中 $\mu_x, \mu_y$ 为图像 $x, y$ 的局部均值，$\sigma_x^2, \sigma_y^2$ 为方差，$\sigma_{xy}$ 为协方差，$C_1, C_2$ 为稳定常数。SSIM 度量亮度、对比度和结构的综合相似性。

- **LPIPS（学习感知图像块相似度）**：
  $$ \text{LPIPS}(x, y) = \sum_l \frac{1}{H_l W_l} \sum_{h,w} \| w_l \odot (\hat{x}_l^{hw} - \hat{y}_l^{hw}) \|_2^2 $$
  其中 $\hat{x}_l^{hw}, \hat{y}_l^{hw}$ 为预训练深度网络第 $l$ 层在空间位置 $(h,w)$ 的归一化特征，$w_l$ 为可学习的通道权重，$H_l, W_l$ 为特征图尺寸。LPIPS 越低表示感知相似度越高。

**代码执行指标**：

- **Pass@1**：模型在单次生成中产生的 GeoGebra 代码能够成功执行且通过自动审核的比例。这是衡量代码生成可靠性的核心指标，直接反映从语言到可执行几何构造的映射精度。

> **注**：上述像素级指标在 GGBench 中的主要作用是作为对照基线——实验表明它们与几何正确性的相关性较弱，从而论证了必须采用几何感知的 VLM-I 评估体系。

### 补充图表

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/006_Figure_2.jpg]]
*Figure 2: GGBench’s step-by-step evaluation. Beyond traditional text-image pairs, GGBench provides executable code for each construction step, allowing for precise and automated verification*

## 实验与分析

### 主要结果：代码驱动 vs. 端到端生成

GGBench 的核心发现是：**基于代码生成的模型在几何构造任务上系统性碾压端到端统一多模态模型（UMM）**。Table 4 给出了两类模型的完整四阶段评估对比。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/012_Table_4.jpg]]
*Table 4: Main results on GGBench. Higher is better (↑) except for LPIPS (↓)*

在综合视觉评分 VLM-I 上，最佳端到端 UMM **Nano Banana** 仅取得 33.82，而基于代码的 **GPT-5** 达到 57.08，领先幅度高达 **+23.26 点**。这一差距贯穿整个评估管道：从中间过程（VLM-I-Mid）到最终结果（VLM-I-Res），代码驱动模型始终维持 15–25 点的优势。值得注意的是，端到端模型在规划阶段（VLM-T）表现尚可——Nano Banana 的 58.54 与 GPT-4o 的 59.73 几乎持平——说明这些模型**能“说出”正确的构造步骤，却无法将其转化为几何精确的图形**。这正是论文所揭示的核心瓶颈：抽象推理与可执行构造之间存在断层。

Table 5 从代码执行维度进一步印证了这一结论。在 GGBench-Code 上，GPT-5 的 Pass@1 高达 **79.02%**，而 DeepSeek-R1 仅为 40.39%，差距达 38.63 个百分点。人工评估同样支持这一排名：GPT-5 获得 83.06 的人类评分，显著优于其他模型。自动 VLM 评分与人类专家评分的 Pearson 相关系数达到 **r = 0.9295**（Figure 19），验证了自动评估的可靠性。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/013_Table_5.jpg]]
*Table 5: Evaluation results on GGBench-Code across execution, similarity, and structural metrics*

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/023_Figure_19.jpg]]
*Figure 19: Correlation between VLM-I and human evaluation*

### 按构造类别与任务类型的细粒度分析

Figure 5 的热图揭示了不同推理类别上的性能分化。所有模型在“测量与比例”和“几何定理应用”两个类别上 VLM-I 分数普遍下降 10–15 点，表明当前模型在需要抽象数值推理和定理调用的场景中仍然薄弱。相比之下，“基本构造”和“对称与变换”类别的得分普遍更高，反映出模型对操作化、步骤化的几何任务掌握更好。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/014_Figure_5.jpg]]
*Figure 5: VLM-I scores across eight construction categories in GGBench. Each cell reflects the average multimodal reasoning quality for a model-category pair*

Figure 6 按任务类型拆分结果：解析构造（AC）、几何变换构造（GTC）和尺规构造（SCC）。代码驱动模型在三种类型上均显著优于端到端 UMM，其中 SCC 类型的差距最大——这类任务要求严格的逐步作图，端到端模型几乎无法生成符合约束的图形。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/015_Figure_6.jpg]]
*Figure 6: VLM-I scores across geometric task types: Analytic Construction (AC), Geometric Transformation Construction (GTC), and Straightedge-and-Compass Construction (SCC). Higher values indicate better performance*

### 难度敏感性

Figure 7 展示了按难度级别的 VLM-I 性能。所有模型在 Easy 级别表现最好，Hard 级别显著下降。GPT-5 在 Hard 子集上仍保持约 50 的 VLM-I，而端到端 UMM 在 Hard 级别已降至接近随机水平。这表明**几何构造的难度对生成式推理能力构成非线性挑战**——当问题需要多步构造和辅助线推理时，模型性能急剧退化。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/016_Figure_7.jpg]]
*Figure 7: VLM-I performance across difficulty levels on GGBench. Bars represent Easy, Medium, Hard, and overall scores. VLM-I captures both intermediate reasoning quality and final visual correctness*

### 像素指标失效：为什么需要几何感知评估

消融实验中的一个关键发现是：传统像素级质量指标（PSNR、SSIM、LPIPS）与几何有效性**相关性弱**。Table 4 中端到端模型的 LPIPS 分数并不差，但其 VLM-I 和人类评分却很低。高感知相似度可能掩盖结构错误——例如，图形看起来“像”一个三角形，但顶点位置不满足给定的约束条件。这证明了 GGBench 采用几何感知评估（可执行代码验证 + VLM 评判）的必要性：只有通过代码执行或几何约束检查，才能可靠地区分“表面正确”与“真正正确”。

### 常见错误模式

Figure 8 归纳了典型失败案例，可归为以下几类：

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/017_Figure_8.jpg]]
*Figure 8: The common error analysis*

1. **约束违反**：生成的图形缺少关键几何约束（如未保证垂直、等长、共线），在端到端 UMM 中最为普遍。
2. **步骤遗漏**：模型跳过了必要的中间构造步骤，直接生成看似合理但不满足构造逻辑的图形。
3. **辅助线缺失**：在需要辅助线推理的任务中，模型未能添加或正确放置辅助线，导致后续构造无法进行。
4. **代码语法错误**：基于代码的模型偶尔生成无法执行的 GeoGebra 命令（如参数顺序错误、未定义的对象引用），这在低性能 LRM 中更常见。

这些错误模式共同指向一个深层问题：**当前模型缺乏将几何约束精确编码为可执行操作的能力**，而非缺乏几何知识本身。

### 基准统计与可比性

Table 1 汇总了 GGBench 的语料库统计：共保留 1,411 个高质量构造问题，包含 7,165 张图像。Table 2 展示了推理类别分布——每个问题可能涉及多个类别，总计 3,097 个标签。Table 3 将 GGBench 与现有数学多模态基准进行了系统对比：GGBench 是唯一实现文本-代码-图像三模态 100% 覆盖的基准，且 100% 的样本要求多步推理，每个步骤均由可执行代码锚定。这一设计保证了评估的自动化和可复现性。

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/011_Table_3.jpg]]
*Table 3: Comparison with existing multimodal mathematical benchmarks. Percentages under Understanding/Generation/Multi-step indicate the share of samples exercising each capability. Text/Image/Code report modality support (%). GGBench uniquely achieves full tri-modal coverage with executable code*

![[assets/figures/papers/paper_list_l2235_https_arxiv_org_abs_2511_11134/figures/008_Table_1.jpg]]
*Table 1: Corpus-level statistics of GGBench*

### 实验公平性保障

所有模型在温度 0.0 下推理，使用统一的提示模板（Figure 17–18）和评估管道。自动评分采用冻结的 VLM（GPT-4o）和固定提示，并通过双盲人工评审验证（r=0.9295）。评估同时覆盖整体图像质量和逐步推理正确性，避免了单一维度的偏见。

## 方法谱系与知识库定位

### 1. 与现有基准的关系：从孤立评估到集成生成式推理

GGBench 在评估范式上与现有数学与多模态基准存在根本性差异。传统基准将“理解”与“生成”视为彼此独立的能力维度进行评测：理解类基准（如 MathVista、MathVerse）要求模型从给定图形中选择或回答文本答案，生成类基准则仅关注端到端图像生成质量。GGBench 的核心突破在于将二者耦合为统一的**生成式推理**任务——模型必须首先理解几何约束的语言描述，然后通过可执行代码或直接图像生成完成精确的几何构造，最终由冻结的 VLM 评判器对中间步骤和最终图形进行几何一致性验证。

从模态覆盖角度看，Table 3 的系统对比揭示了 GGBench 的独特定位：现有基准（如 GeoQA、UniGeo、Geometry3K）通常仅提供文本和图像两种模态，且缺乏可执行代码作为可验证的真值。GGBench 实现了**文本-代码-图像三重完全对齐**（100% 覆盖率），每个构造步骤均由可执行的 GeoGebra 代码锚定，使得评估从模糊的语义匹配转向确定性的几何正确性验证。这一设计直接回应了当前统一多模态模型（UMMs）的核心瓶颈：模型在抽象推理向精确构造的映射过程中系统性失败，而缺乏代码级可验证性使得此类失败难以被传统指标捕获。

### 2. 与基线方法的方法论对比

GGBench 并非提出新的模型架构，而是构建了一个区分两类技术路线的评估框架：

**Track A：端到端统一多模态模型（直接图像生成）。** 此类模型（包括 **Qwen-Image**、**Seedream 4.0**、**Janus**、**BAGEL**、**Nano Banana**）接收文本指令后直接输出渲染图像，跳过了显式的结构化推理与代码生成环节。实验结果表明，即使表现最好的端到端模型 Nano Banana 在综合视觉评分 VLM-I 上仅达到 33.82，远低于基于代码的模型（GPT-5 为 57.08）。这一差距在需要精确比例控制和几何定理应用的任务类别上尤为突出（Figure 5），表明直接像素生成无法可靠地保证几何约束的满足。

**Track B：基于代码生成的 LLMs/LRMs。** 此类模型（包括 **GPT-5**、**Claude Sonnet 4.5**、**Gemini-2.5-Pro**、**DeepSeek-R1**、**DeepSeek-V3.1** 等）首先生成可执行的 GeoGebra 代码，再通过渲染引擎生成最终图形。代码管道将几何推理与视觉输出解耦，使得推理过程可被逐步验证。GPT-5 在 GGBench-Code 上达到 79.02% 的 pass@1，并获得最高的人类评分（83.06），证明了代码中介在生成式推理中的有效性。

**关键机制差异：** 端到端模型将几何约束隐式编码在模型参数中，缺乏显式的约束求解机制；基于代码的模型则通过结构化语言（GeoGebra）将约束显式化，使推理过程可审计、可纠错。这一差异在中间步骤评估（VLM-I-Mid）中尤为明显——代码模型能够保持步骤间的逻辑连贯性，而端到端模型常在多步构造中出现累积误差。

### 3. 适用边界

GGBench 的评估框架目前具有以下明确边界：

- **领域边界：** 仅覆盖 2D 欧氏几何构造任务，包括解析构造、几何变换构造和尺规构造三种类型。能否推广到 3D 几何、工程制图、科学图解生成等需要生成式推理的领域仍有待验证。
- **模型能力边界：** 基准主要评估模型的集成推理与生成能力，而非孤立的识别或理解能力。对于仅具备文本理解能力的纯语言模型，GGBench 无法直接适用。
- **评估边界：** 自动评估依赖冻结的 VLM 评判器（GPT-4o），虽与人类评分高度相关（Pearson r=0.9295），但在拓扑错误、缺失辅助线等几何特异缺陷的检测上可能存在盲区。

### 4. 局限与开放问题

**数据构建的潜在偏差。** GGBench 的构建流水线严重依赖 GPT-5 进行问题筛选、改写和解答生成。尽管经过多轮 LLM 自动审核和领域专家核准，仍可能引入模型偏好或系统性错误。例如，某些构造策略可能因符合 GPT-5 的生成习惯而被过度代表，而其他有效的构造路径被忽略。

**评估维度的覆盖缺口。** 当前 VLM 评判器主要关注几何约束的满足程度和视觉一致性，但对构造过程的“优雅性”或“效率性”缺乏评估。一个冗长但正确的构造方案可能与简洁方案获得相近的评分。此外，像素级质量指标（PSNR、SSIM、LPIPS）被证实与几何有效性相关性弱——高感知相似度可能掩盖结构错误（Section 4.3），这进一步强调了几何感知评估的必要性，但也暴露了当前评估维度尚不完整的现实。

**类别分布的不均衡性。** 基准中某些高级推理类别（如复杂几何变换、多步定理应用）的样本量相对较少，可能影响细粒度能力评估的统计置信度。在“测量与比例”和“几何定理应用”等类别上，所有模型的 VLM-I 分数普遍下降 10–15 点，表明当前模型在这些抽象推理维度上仍存在显著薄弱环节。

**开放研究问题：**

1. **跨领域泛化：** 如何将该集成评估框架扩展到更多 STEM 领域（如物理示意图生成、化学结构图、算法流程图），同时保持代码可执行验证和模态对齐的核心优势？
2. **深度理解的判别：** 在模型不完全理解几何约束的情况下，如何区分“表面正确”（通过模式匹配生成的巧合正确）与“真正理解”？是否需要引入对抗性测试或更深层的违规检测机制？
3. **端到端模型的闭合回路训练：** 能否通过强化学习或训练过程中直接注入代码执行反馈，使端到端 UMMs 获得与代码驱动模型相当的构造精度，同时保留端到端生成的灵活性？
4. **评判模型的进化：** 现有的视觉语言评判模型能否被改进或专门微调，以更精准地捕获拓扑错误、缺失辅助线、比例失调等几何特异缺陷，进一步提升自动评估的可靠性？

## 原文 PDF

![[paperPDFs/CVPR_2026/GGBench_A_Geometric_Generative_Reasoning_Benchmark_for_Unified_Multimodal_Models.pdf]]
