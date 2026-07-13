---
title: "CompBench: Benchmarking Complex Instruction-guided Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CompBench_Benchmarking_Complex_Instruction_guided_Image_Editing.pdf
project_link: "https://comp-bench.github.io/"
code_link: "https://huggingface.co/stabilityai/cosxl"
aliases:
- CompBench
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建具有高场景复杂度（平均13.58个对象、98.47%遮挡率）、多任务覆盖（涵盖局部编辑、多编辑、动作编辑、空间编辑和复杂推理）以及高质量数据（高SSIM）的基准CompBench，能够暴露模型在背景保持、目标识别和指令跟随上的根本局限。
primary_logic: 采用MLLM-人类协同框架和指令解耦策略（空间定位、视觉属性、运动状态、对象实体）可以生成高质量、细粒度的复杂编辑数据，从而推动模型从简单编辑向具备真正理解和推理能力的下一代系统演进。
claims:
- InstructPix2pix在CompBench上相比ReasonEdit基准，PSNR下降约2.5，SSIM下降0.02，CLIP-Score下降0.4，证明CompBench显著提高了任务难度。
- 所有模型在多轮编辑的第二轮中，背景一致性指标（PSNR, SSIM, LPIPS）均出现显著下降，暴露了连续编辑中的上下文保持缺陷。
- 集成MLLM的模型（如Bagel、Qwen-Image-Edit）在复杂任务上大幅领先未集成MLLM的模型，说明标准CLIP-文本对齐不足以支撑复杂推理。
- 采用MLLM-人类协同框架和指令解耦策略（空间定位、视觉属性、运动状态、对象实体）可以生成高质量、细粒度的复杂编辑数据，从而推动模型从简单编辑向具备真正理解和推理能力的下一代系统演进。
---

# CompBench: Benchmarking Complex Instruction-guided Image Editing

> [!tip] 核心洞察
> 采用MLLM-人类协同框架和指令解耦策略（空间定位、视觉属性、运动状态、对象实体）可以生成高质量、细粒度的复杂编辑数据，从而推动模型从简单编辑向具备真正理解和推理能力的下一代系统演进。

| 字段 | 内容 |
|------|------|
| 中文题名 | CompBench：面向复杂指令引导图像编辑的基准测试 |
| 英文题名 | CompBench: Benchmarking Complex Instruction-guided Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.12200) · [Project](https://comp-bench.github.io/) · [HuggingFace](https://huggingface.co/stabilityai/cosxl) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CompBench |
| Dataset | CompBench |
> [!tip] 效果简介
> - InstructPix2pix在CompBench上相比ReasonEdit基准，PSNR下降约2.5，SSIM下降0.02，CLIP-Score下降0.4，证明CompBench显著提高了任务难度。
> - 所有模型在多轮编辑的第二轮中，背景一致性指标（PSNR, SSIM, LPIPS）均出现显著下降，暴露了连续编辑中的上下文保持缺陷。

## 概要

指令引导图像编辑旨在根据自然语言指令对图像进行修改，然而现有基准在场景复杂性和指令全面性上存在严重不足——多数数据集图像仅包含少量物体、遮挡率低，且任务局限于简单的局部编辑，无法有效评估模型在真实复杂环境下的视觉定位、上下文理解和推理能力。CompBench 作为首个面向复杂场景的大规模指令引导图像编辑基准，通过构建高场景复杂度（平均 13.58 个对象/图，98.47% 遮挡率）、覆盖五大类九种任务（局部编辑、多编辑、动作编辑、场景空间编辑、复杂推理）的高质量数据集（高 SSIM），系统性地暴露了当前模型在背景保持、目标识别和指令跟随上的根本局限。

核心方法上，CompBench 提出了 MLLM-人类协同框架与指令解耦策略：多模态大语言模型生成初步编辑指令，人工专家审核迭代以确保指令-图像对齐；同时将编辑意图分解为空间定位、视觉属性、运动状态和对象实体四个维度，提升指令的清晰度和精度。实验表明，集成 MLLM 的模型（如 **Bagel**、**Qwen-Image-Edit**）在复杂推理和空间编辑任务上大幅领先未集成 MLLM 的模型，而标准 CLIP-文本对齐不足以支撑复杂推理；此外，所有模型在多轮编辑的第二轮中背景一致性指标均出现显著下降，揭示了连续编辑中的上下文保持缺陷。这些发现为下一代具备真正理解和推理能力的图像编辑系统指明了方向。

指令引导的图像编辑（Instruction-guided Image Editing）旨在根据自然语言指令对输入图像进行精确修改。近年来，扩散模型驱动的编辑方法在简单场景下取得了显著进展，但当任务复杂度提升至真实世界水平时，现有基准和评估体系暴露出根本性不足。

### 现有基准的三大缺口

**场景复杂度不足。** 主流基准如MagicBrush、HIVE、ReasonEdit等所采用的图像普遍来自相对简单的场景，缺乏真实世界中常见的高密度对象分布和严重遮挡。如Table 1所示，CompBench在平均对象数（13.58）、平均类别数（5.87）、遮挡率（98.47%）和出框对象率（OOF）四个维度上均大幅超越现有基准——平均对象数比第二名GEdit-Bench高出约36.3%。低复杂度场景无法有效检验模型在拥挤、遮挡环境下的视觉定位与目标识别能力。

**指令全面性欠缺。** 现有基准主要覆盖对象增删改等局部编辑任务，对多对象编辑、动作编辑、视角编辑等需要深层语义理解和空间推理的任务几乎空白。如Figure 2第二行所示，典型基准的指令往往过于简单，无法体现真实用户意图的多样性和复杂性。

**编辑质量参差不齐。** 部分数据集（如InstructPix2pix、UltraEdit）的编辑结果存在背景不一致或编辑区域伪影等问题（Figure 2第一行）。CompBench通过MLLM-人类协同验证框架确保所有数据均为成功执行的高保真编辑结果，其SSIM指标显著优于其他数据集（Figure 5），为公平评估提供了可靠的真值基础。

### 核心瓶颈与本文动机

上述缺口指向一个更深层的瓶颈：**现有模型在复杂真实场景下的视觉定位、上下文理解和推理能力存在根本局限**，而缺乏相应难度的基准使得这一局限长期被掩盖。具体表现为：

- **背景保持与目标识别的冲突。** 在遮挡密集的场景中，模型难以在精确编辑前景目标的同时保持背景一致性。所有模型在多轮编辑的第二轮中，背景一致性指标（PSNR、SSIM、LPIPS）均出现显著下降（Table 3），暴露了连续编辑中的上下文保持缺陷。

- **标准CLIP-文本对齐不足以支撑复杂推理。** 集成MLLM的模型（如Bagel、Qwen-Image-Edit）在动作/位置/视角编辑任务上大幅领先未集成MLLM的模型（Table 4），而未集成MLLM的模型频繁忽略指令或编辑错误目标，表明仅依赖CLIP-文本对齐无法满足复杂推理需求。

- **难度验证。** 同一模型InstructPix2pix在CompBench上相比ReasonEdit基准，PSNR下降约2.5，SSIM下降0.02，CLIP-Score下降0.4，定量证明了CompBench显著提高了任务难度。

基于此，本文提出**CompBench**——首个面向复杂场景的大规模指令引导图像编辑基准，通过MLLM-人类协同框架和指令解耦策略，构建覆盖五大类九种任务的高质量编辑数据，旨在暴露模型在背景保持、目标识别和指令跟随上的根本局限，推动从简单编辑向具备真正理解和推理能力的下一代系统演进。

## 核心方法与创新机理

CompBench 的核心创新并非提出新的编辑模型，而是通过**基准测试本身的系统化设计**，暴露并量化当前指令引导图像编辑模型在复杂真实场景下的根本性能力缺陷。其创新点可归结为三个相互耦合的维度：**高复杂度的场景构造**、**MLLM-人类协同的数据生成框架**，以及**指令解耦策略驱动的细粒度评估体系**。

### 1. 从简单场景到复杂真实场景的基准跃迁

现有指令编辑基准（如 MagicBrush、ReasonEdit 等）普遍存在场景简单、指令单一的问题，无法反映模型在真实世界中面临的挑战。CompBench 通过系统化的场景复杂度量化指标实现了关键跃迁：

- **对象密度与类别多样性**：CompBench 平均每张图像包含 **13.58 个对象**，覆盖 **5.87 个类别**，比次优基准 GEdit-Bench 高出约 36.3%（Table 1）。
- **遮挡与出框率**：图像遮挡率（OCC）达 **98.47%**，出框对象率（OOF）同样远高于现有基准，迫使模型在高度遮挡和不完整观测下进行精确的视觉定位与编辑。
- **编辑质量保真**：CompBench 中所有数据均为成功执行的编辑结果，其 SSIM 指标显著优于其他数据集（Figure 5），确保基准本身的高质量参照标准。

这一设计直接导致了模型性能的显著下降——**InstructPix2pix**（Brooks et al., CVPR 2023）在 CompBench 上相比 ReasonEdit 基准，PSNR 下降约 2.5，SSIM 下降 0.02，CLIP-Score 下降 0.4，有力证明了场景复杂度提升对模型能力的有效区分。

### 2. MLLM-人类协同框架与任务专用流水线

为生成高质量、细粒度的复杂编辑数据，CompBench 提出了一套 **MLLM-人类协同框架**（MLLM-Human Collaborative Framework），并针对不同编辑类型设计了四条专用流水线：

- **协同机制**：多模态大语言模型（MLLM）首先分析视觉场景和编辑目标，生成初步编辑指令；随后由人类专家进行审核与迭代修正，确保指令-图像对齐和编辑高保真。这一机制既利用了 MLLM 的语义理解和生成能力，又通过人工把关保证了数据质量。
- **四条任务流水线**：
  1. **局部编辑流水线**：针对对象级操作（添加、删除、替换）
  2. **动作/场景空间编辑流水线**：覆盖动作编辑、位置编辑和视角编辑
  3. **复杂推理流水线**：处理需要上下文理解和隐式推理的编辑任务
  4. **多编辑流水线**：支持多对象编辑和多轮连续编辑

该框架覆盖了五大类共九种编辑任务（Figure 4），包含超过 3000 个图像-指令对，是目前任务覆盖最广的指令编辑基准。

### 3. 指令解耦策略：从模糊意图到结构化描述

CompBench 提出了一种**指令解耦策略**（Instruction Decoupling Strategy），将编辑意图系统化地分解为四个维度：

- **空间定位**（spatial positioning）：明确编辑目标的空间位置
- **视觉属性**（visual attributes）：指定颜色、纹理、形状等外观特征
- **运动状态**（motion states）：描述动态变化或动作
- **对象实体**（object entities）：精确指代被编辑的目标对象

这种结构化分解使得编辑指令从模糊的自然语言描述转变为可验证、可度量的语义单元，既提升了指令的清晰度和精度，也为后续的前景-背景解耦评估（foreground-background decoupling evaluation）奠定了基础——评估时可分别度量编辑准确性（前景）和背景保持能力（背景）。

### 4. 揭示的关键能力鸿沟：MLLM 集成的必要性

CompBench 的实验结果揭示了一个关键洞察：**标准 CLIP-文本对齐不足以支撑复杂推理**。集成 MLLM 的模型（如 **Bagel**、**Qwen-Image-Edit**、**FLUX.1 Kontext**、**Step1X-Edit**）在动作/位置/视角编辑等复杂任务上大幅领先未集成 MLLM 的模型；后者经常忽略指令或编辑错误目标。此外，所有模型在多轮编辑的第二轮中，背景一致性指标（PSNR、SSIM、LPIPS）均出现显著下降（Table 3），暴露了连续编辑中的上下文保持缺陷。这些发现为下一代编辑模型指明了方向：必须从简单的文本-图像对齐向具备真正理解和推理能力的多模态架构演进。

CompBench的构建遵循一个两阶段流水线：**源数据收集与预处理**，以及**任务专用数据生成**。两条主线通过统一的**MLLM-人类协同框架**（MLLM-Human Collaborative Framework）衔接，确保数据质量与指令-图像对齐。

### 第一阶段：源数据收集与预处理

为弥补现有基准在复杂场景上的缺失，CompBench从**MOSE数据集**中提取高质量视频帧作为源数据。预处理流程包含四道关卡：

1. **图像质量过滤**：采用NIQE等自动化指标剔除模糊、噪声或压缩损伤严重的帧，随后由人工进行二次验证。
2. **掩码分解**：将MOSE提供的多对象标注掩码拆分为单对象实例掩码，为后续局部编辑任务提供像素级前景-背景分离依据。
3. **遮挡与连续性评估**：对每帧中的对象遮挡率和跨帧运动连续性进行量化，筛选出高遮挡、高动态的真实复杂场景。
4. **人工终审**：对通过自动筛选的数据进行最终人工核查，排除语义歧义或标注错误的样本。

该阶段产出的核心资产是**高场景复杂度的源图像及对应对象掩码**。定量证据表明，CompBench的场景复杂度显著高于现有基准：平均每张图像包含**13.58个对象**、**5.87个对象类别**，整体遮挡率高达**98.47%**（Table 1），为后续编辑任务提供了极具挑战性的真实世界基底。

### 第二阶段：任务专用数据生成

在预处理数据之上，CompBench部署了**四条专用生成流水线**，分别覆盖五大类共九种编辑任务（Figure 3右侧，Figure 4）：

| 流水线 | 覆盖任务 | 核心生成逻辑 |
|--------|---------|-------------|
| 局部编辑流水线 | 对象添加、删除、替换 | 基于单对象掩码定位目标区域，生成属性/类别变更指令 |
| 动作/场景空间编辑流水线 | 动作编辑、位置编辑、视角编辑 | 描述对象运动状态或空间关系的全局变化 |
| 复杂推理流水线 | 隐式推理 | 构造需要上下文理解与逻辑推断的编辑意图 |
| 多编辑流水线 | 多对象编辑、多轮编辑 | 组合多个编辑操作或连续多步指令 |

四条流水线共享统一的**MLLM-人类协同框架**：多模态大语言模型（MLLM）首先分析视觉场景与编辑目标，生成初始编辑指令；随后由人类专家审核并迭代修正，确保指令-图像语义对齐和编辑结果的高保真度。

### 指令解耦策略

为提升指令的清晰度与可评估性，CompBench引入**指令解耦策略**，将编辑意图系统性地分解为四个维度：

- **空间定位**（spatial positioning）：目标对象在图像中的位置描述
- **视觉属性**（visual attributes）：颜色、纹理、材质等外观特征
- **运动状态**（motion states）：对象的动作或动态变化
- **对象实体**（object entities）：涉及的语义类别与实例身份

这一结构化框架使编辑指令既具备细粒度可操作性，又便于后续的前景-背景解耦评估。

### 数据质量保障

整个流水线的设计目标不仅是覆盖更多任务，更是保证编辑结果的结构一致性。如Figure 5所示，CompBench中编辑后图像的**SSIM**显著高于UltraEdit、InstructPix2pix等数据集，证明其源数据选择和指令生成流程能有效维持背景结构，避免引入伪影。最终，CompBench产出**超过3000组图像-指令对**，为复杂指令引导图像编辑提供了大规模、高质量的评测基准。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/004_Figure_3.jpg]]
*Figure 3: The construction pipeline of CompBench. The pipeline consists of two main stages: (a) Source data collection and preprocessing, wherein high-quality data are identified through image quality filtering, mask decomposition, occlusion and continuity evaluation, followed by thorough human verification. (b) Task-specific data generation using four specialized pipelines within our MLLM-Human Collaborative Framework, where multimodal large language models generate initial editing instructions that are subsequently validated by humans to ensure high-fidelity, semantically aligned instruction-image pairs for complex editing tasks*

### 3.1 MLLM-人类协同框架

CompBench 的核心构建机制是一套 **MLLM-人类协同框架（MLLM-Human Collaborative Framework）**。该框架并非单一模型，而是一种数据生成与验证策略，旨在解决复杂编辑场景下高质量指令-图像对难以获取的瓶颈。

框架的工作流程如下：首先由多模态大语言模型（MLLMs）根据输入图像和编辑目标，生成初步的编辑指令；随后由人工专家对指令-图像对齐度及编辑保真度进行审核与迭代修正。这一闭环机制确保了最终基准中每一条指令的语义清晰度和可执行性。

### 3.2 指令解耦策略

为提升指令的精确度，CompBench 提出了一种 **指令解耦策略（Instruction Decoupling Strategy）**，将编辑意图显式分解为四个正交维度：

- **空间定位（Spatial Positioning）**：指定编辑目标在图像中的位置；
- **视觉属性（Visual Attributes）**：描述目标的外观特征，如颜色、纹理、形状；
- **运动状态（Motion States）**：刻画目标的动态变化，如“奔跑”、“旋转”；
- **对象实体（Object Entities）**：明确被编辑的具体对象类别与实例。

这一解耦设计使得复杂指令能够被结构化为可独立验证的子维度，既降低了人工标注的歧义性，也为后续的细粒度评估提供了逻辑基础。

### 3.3 任务专用数据生成流水线

在上述协同框架与解耦策略的基础上，CompBench 设计了四条 **任务专用数据生成流水线（Task-Specific Data Generation Pipelines）**，分别覆盖五类共九种编辑任务：

1. **局部编辑流水线（Local Editing Pipeline）**：处理对象级操作，包括对象添加、删除和替换；
2. **动作/场景空间编辑流水线（Action/Scene Spatial Editing Pipeline）**：生成涉及动作编辑、位置编辑和视角编辑的数据；
3. **复杂推理流水线（Complex Reasoning Pipeline）**：构建需要隐式推理能力的指令，如基于常识或上下文的编辑；
4. **多编辑流水线（Multi-Editing Pipeline）**：覆盖多对象编辑和多轮编辑任务。

每条流水线均遵循“MLLM 生成初始指令 → 人工验证与修正”的统一范式，确保了数据质量的一致性和可复现性。

### 3.4 源数据预处理模块

在进入任务流水线之前，原始数据需经过严格的预处理流程：

- **图像质量过滤**：采用 NIQE 等无参考图像质量评估指标自动筛选高质量帧，辅以人工核验；
- **掩码分解**：将多对象标注掩码拆分为单对象实例掩码，以支持精细化的前景-背景解耦评估；
- **遮挡与连续性评估**：对场景中的对象遮挡率和帧间连续性进行量化，确保所选场景具备足够的视觉复杂性。

该预处理模块是保证 CompBench 高场景复杂度（平均 13.58 个对象/图，98.47% 遮挡率）和高编辑质量（SSIM 显著优于现有数据集，见 Figure 5）的基础。

### 3.5 关键公式与评估指标

CompBench 本身不引入新的生成模型或损失函数，其评估体系基于现有指标的组合与解耦应用。核心评估逻辑可形式化为前景-背景解耦框架：

对于局部编辑、多编辑及隐式推理任务，编辑结果 $I_{\text{edit}}$ 与真实图像 $I_{\text{gt}}$ 的比较被分解为前景区域 $F$ 和背景区域 $B$：

**前景编辑一致性**采用局部 CLIP 分数衡量：
- **LC-T（Local CLIP-Text）**：计算编辑后前景区域与局部文本描述之间的 CLIP 相似度；
- **LC-I（Local CLIP-Image）**：计算编辑后前景区域与真实图像前景区域之间的 CLIP 图像相似度。

**背景保持能力**采用传统图像质量指标在背景区域上计算：
- **PSNR**：峰值信噪比，衡量背景像素级保真度；
- **SSIM**：结构相似性指数，衡量背景结构一致性；
- **LPIPS**：学习感知图像块相似度，衡量背景感知差异。

对于动作、位置和视角编辑等难以通过像素对齐评估的任务，引入 **多视角评分机制**，由 GPT-4o、Qwen2.5-VL-72B 和人类标注者在 0-10 分量表上进行独立评分，最终取平均值作为综合性能指标。

> **注意**：以上公式均为评估指标的定义性描述，论文未提供新的推导性公式。若需具体的 PSNR、SSIM、LPIPS 或 CLIP Score 数学表达式，请参考其原始文献。

## 实验与关键发现

### 基准统计与任务难度验证

CompBench 共包含超过 3k 个图像-指令对，覆盖五大类九种任务（Figure 4）。与现有基准相比，CompBench 的场景复杂度显著更高：平均每张图像包含 13.58 个对象和 5.87 个对象类别，分别比第二高的 GEdit-Bench 高出约 36.3%（Table 1）。此外，CompBench 的图像中遮挡对象比例（OCC）和出框对象比例（OOF）均处于最高水平，使其更接近真实世界的复杂编辑场景。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/002_Table_1.jpg]]
*Table 1: Comparison of existing image-editing datasets and benchmarks. Our benchmark supports seven core editing tasks, including multi-object, action and viewpoint editing, which are absent from most prior benchmarks. Scenario complexity is quantified by four indicators: Avg. Obj. (average number of objects per image), Avg. Cat. (average number of object categories per image), OCC (percentage of images that contain occluded objects), and OOF (percentage of images that contain out-of-frame objects). Across all four metrics, our benchmark exhibits the highest complexity, underscoring its suitability for rigorous evaluation*

为验证基准的任务难度，作者以 **InstructPix2pix**（Brooks et al., CVPR 2023）为探针模型，将其在 CompBench 上的表现与 ReasonEdit 基准进行对比。结果显示，InstructPix2pix 在 CompBench 上的 PSNR 下降约 2.5、SSIM 下降 0.02、CLIP-Score 下降 0.4，表明 CompBench 显著提高了任务难度，能够更有效地暴露模型的编辑能力瓶颈。同时，CompBench 中所有数据的 SSIM 得分显著优于其他数据集（Figure 5），说明基准本身具有较高的编辑质量基准线，避免了低质量 ground truth 对评估的干扰。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/007_Figure_5.jpg]]
*Figure 5: SSIM comparison among different datasets and benchmarks. Note that UltraEdit [48] and InstructPix2pix [3] are datasets, whereas the remaining entries are benchmarks*

### 主实验：五大任务上的模型性能

#### 局部编辑、多对象编辑与隐式推理

Table 2 展示了 15 个模型在局部编辑、多对象编辑和隐式推理任务上的量化结果。评估采用前景-背景解耦策略：前景编辑准确性通过局部 CLIP 分数（LC-T）和前景 CLIP 图像相似度（LC-I）度量，背景保持能力则通过背景区域的 PSNR、SSIM 和 LPIPS 评估。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/005_Table_2.jpg]]
*Table 2: Evaluation results on local editing, multi-object editing and implicit reasoning. LC-T denotes local CLIP scores between the edited foreground and the local description. LC-I refers to the CLIP image similarity between the foreground edited result and ground truth (GT) image. Top-three evaluation results are highlighted in red (1st), blue(2nd), and green (3rd)*

在局部编辑任务上，**Bagel** 取得 LC-T 21.059、LC-I 0.838、PSNR 27.692、SSIM 0.935、LPIPS 0.045 的领先成绩，**FLUX.1 Kontext** 紧随其后（LC-T 21.328、LC-I 0.821、PSNR 25.613、SSIM 0.941、LPIPS 0.050）。Bagel 在 LC-I 指标上持续领先，表明其编辑结果与 ground truth 的前景区域具有最高的语义一致性。

在多对象编辑和隐式推理任务中，集成 MLLM 的模型（Bagel、Qwen-Image-Edit、FLUX.1 Kontext、Step1X-Edit）表现大幅领先于未集成 MLLM 的模型。缺乏 MLLM 集成的模型频繁出现忽略指令或编辑错误目标的问题，说明标准的 CLIP-文本对齐机制不足以支撑复杂场景下的多对象定位和隐式推理需求。

#### 多轮编辑

Table 3 报告了多轮编辑任务的评估结果。一个关键发现是：所有模型在第二轮编辑中，背景一致性指标（PSNR、SSIM、LPIPS）均出现显著下降。这一现象揭示了当前模型在连续编辑任务中的上下文保持缺陷——模型在首轮编辑后难以稳定维持未编辑区域的结构和纹理一致性，第二轮编辑会进一步加剧背景退化。该结果说明，现有模型缺乏有效的历史编辑状态记忆与背景保护机制，多轮编辑场景下的累积误差问题亟待解决。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/008_Table_3.jpg]]
*Table 3: Evaluation results on multi-turn editing*

#### 动作、位置与视角编辑

Table 4 展示了动作编辑、位置编辑和视角编辑任务上的多视角评分结果。评估引入 GPT-4o、Qwen2.5-VL-72B 和人类标注者进行 0-10 分的独立评分，并取平均值作为最终得分。

![[assets/figures/papers/paper_list_l2298_https_arxiv_org_abs_2505_12200/figures/009_Table_4.jpg]]
*Table 4: Comparison on Action, Location, and Viewpoint Editing. Results for GPT-4o, Qwen-72B, Human Evaluation, and Average scores (top-3 per column highlighted in red, blue, green)*

**Qwen-Image-Edit** 和 **Bagel** 在这三类任务上表现相当，且显著优于大多数其他模型。这一优势归因于二者均集成了多模态大语言模型，具备更强的空间推理和语义理解能力。相比之下，未集成 MLLM 的模型在需要精确空间定位（位置编辑）和理解动态变化（动作编辑）的任务中表现明显不足，进一步印证了复杂推理任务对高级语义理解能力的依赖。

#### 整体性能概览

Figure 6(a) 展示了五大任务上的 Top-5 模型性能分布，Figure 6(b) 给出了所有模型在全任务上的综合表现对比。综合 Tables 2-4 的结果，Bagel 在 9 个任务的 37 项指标中取得了 18 项 Top-1，成为综合表现最优的模型。总体而言，集成 MLLM 的模型在复杂任务上建立了显著优势，而传统基于扩散模型的编辑方法在场景复杂度高、指令涉及推理或空间关系时暴露出明显的定位不准、背景破坏和指令跟随失败等问题。

### 失败模式分析

基于实验结果和定性观察，当前模型在 CompBench 上主要表现出以下失败模式：

1. **背景保持失败**：多数模型在编辑目标区域时难以完全保持背景不变，尤其在多轮编辑中问题加剧。背景区域的 PSNR 和 SSIM 在第二轮编辑中普遍下降，表明模型缺乏对未编辑区域的显式保护机制。

2. **目标识别与定位错误**：在场景中包含多个相似对象或存在严重遮挡时，未集成 MLLM 的模型频繁出现编辑错误目标的情况。这暴露了 CLIP-文本对齐在细粒度视觉定位上的局限性。

3. **指令跟随偏差**：对于涉及隐式推理或复杂空间关系的指令，部分模型要么忽略关键约束，要么产生与指令语义不一致的编辑结果。这表明模型对组合性指令的理解能力仍有较大提升空间。

4. **物理一致性与几何失真**：在动作编辑和视角编辑任务中，模型生成的编辑结果有时违背物理常识（如物体悬浮、比例失调），说明 2D 编辑模型缺乏对三维结构和物理约束的建模能力。

## 定位与知识库关联

### 1. 基准构建范式的演进定位

CompBench 的构建方法在指令引导图像编辑基准演进中占据了一个承上启下的位置。早期基准如 **InstructPix2pix**（Brooks et al., CVPR 2023）和 **MagicBrush**（Zhang et al., NeurIPS 2023）主要依赖简单场景和单一编辑指令，其数据生成流程缺乏对场景复杂度和指令精确性的系统性控制。CompBench 通过引入 **MLLM-人类协同框架** 和 **指令解耦策略**，将基准构建从“数据收集”范式提升为“系统化任务设计”范式——它不再被动地聚合现有编辑结果，而是主动地根据场景语义生成高质量、细粒度的编辑指令-图像对。

这一构建范式的核心创新在于两条并行路径的交汇：
- **自顶向下的任务分类**：将编辑任务划分为局部编辑、多编辑、动作编辑、场景空间编辑和复杂推理五大类，覆盖九种具体任务（Figure 4），这种分类体系本身就构成了对“指令引导编辑能力”的分解定义。
- **自底向上的数据质量控制**：从 MOSE 数据集中筛选高复杂度帧（平均每图 13.58 个对象，98.47% 遮挡率），通过 NIQE 质量过滤、掩码分解和人工验证确保源数据质量，再经由四条任务专用流水线生成编辑数据（Figure 3）。

与 **ReasonEdit** 等近期基准相比，CompBench 的构建方法在三个维度上实现了系统性提升：场景复杂度（对象数量比次优基准 GEdit-Bench 高出约 36.3%）、任务覆盖面（首次包含多对象编辑、动作编辑和视角编辑）以及数据质量（编辑后图像的 SSIM 显著高于其他数据集，见 Figure 5）。这些提升直接转化为评估难度的增加——InstructPix2pix 在 CompBench 上相比 ReasonEdit，PSNR 下降约 2.5，SSIM 下降 0.02，CLIP-Score 下降 0.4，验证了基准设计的有效性。

### 2. 与现有模型的能力边界关系

CompBench 的实验结果揭示了当前指令引导图像编辑模型的两条能力分界线：

**第一分界线：MLLM 集成与否**。在动作编辑、位置编辑和视角编辑等需要复杂语义理解和空间推理的任务上，集成 MLLM 的模型（**Bagel**、**Qwen-Image-Edit**、**FLUX.1 Kontext**、**Step1X-Edit**）显著领先于未集成 MLLM 的模型（如 **InstructPix2pix**、**MagicBrush**、**HIVE**（Zhang et al., CVPR 2024）、**SmartEdit**（Huang et al., CVPR 2024））。未集成 MLLM 的模型频繁出现忽略指令或编辑错误目标的问题，表明标准的 CLIP-文本对齐机制不足以支撑复杂推理任务中的视觉定位和意图理解。

**第二分界线：多轮编辑中的上下文保持**。所有模型在多轮编辑的第二轮中，背景一致性指标（PSNR、SSIM、LPIPS）均出现显著下降（Table 3），暴露了当前模型在连续编辑场景下缺乏对历史编辑状态的稳定记忆和上下文推理能力。这一发现将“多轮编辑一致性”确立为该领域的一个关键开放问题。

Bagel 在局部编辑任务上取得了最佳综合表现（LC-T 21.059，LC-I 0.838，PSNR 27.692，SSIM 0.935，LPIPS 0.045，Table 2），并在 9 个任务的 37 项指标中取得了 18 项第一。FLUX.1 Kontext 在局部编辑的 LC-T 指标上略优（21.328），但在 LC-I 和 PSNR 上落后于 Bagel，表明两者在编辑准确性和图像保真度之间存在不同的权衡策略。

### 3. 适用边界与方法局限

CompBench 作为评估工具，其适用边界由以下设计选择决定：

- **场景来源的偏置**：源数据全部来自 MOSE 视频数据集，虽然保证了高复杂度和真实感，但场景类型可能偏向监控或街景视角，对室内精细场景、艺术风格图像或抽象构图的覆盖不足。
- **编辑类型的覆盖缺口**：当前九种任务未包含风格迁移、全局光照变换、文本渲染等编辑类型，这些任务在 AIGC 应用场景中同样重要。
- **评估指标的代理性局限**：虽然引入了 GPT-4o、Qwen2.5-VL-72B 和人类评估的多视角评分体系，但 VLM 评分与人类偏好之间的一致性程度尚未被量化校准。对于动作编辑等动态概念，静态图像评估本身存在固有的信息损失。
- **MLLM 协同框架的扩展成本**：MLLM-人类协同框架依赖人工专家对 MLLM 生成的指令进行审核和迭代修正，这限制了基准规模的快速扩展。

### 4. 开放问题与未来方向

CompBench 的实验发现直接指向以下开放问题：

1. **像素级定位稳定性**：在杂乱场景中，即使集成 MLLM 的模型也经常出现编辑区域偏移或边界伪影。如何提升模型在密集遮挡条件下的像素级定位精度，是该领域的一个基础性挑战。

2. **3D 结构先验的引入**：当前所有模型均在 2D 空间上训练，缺乏对场景几何结构的显式建模。引入 3D 结构先验或几何引导机制，以维持编辑过程中的物理一致性（如透视关系、遮挡顺序），是推动模型从“像素编辑”走向“场景编辑”的关键路径。

3. **多轮编辑的上下文记忆**：多轮编辑中背景一致性的系统性退化表明，现有模型缺乏有效的编辑状态追踪机制。设计具备编辑历史感知能力的架构（如记忆增强模块或状态编码器），是解决这一问题的潜在方向。

4. **评估体系的可扩展性**：随着编辑任务复杂度的持续增长，基于 VLM 的自动评分需要更精细的校准和更透明的失效模式分析，以确保评估结果与人类判断保持可靠的一致性。

## 原文 PDF

![[paperPDFs/CVPR_2026/CompBench_Benchmarking_Complex_Instruction_guided_Image_Editing.pdf]]
