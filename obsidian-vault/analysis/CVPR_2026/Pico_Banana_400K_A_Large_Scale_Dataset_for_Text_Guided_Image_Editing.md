---
title: "Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Pico_Banana_400K_A_Large_Scale_Dataset_for_Text_Guided_Image_Editing.pdf
project_link: null
code_link: null
aliases:
- PB4
- Pico-Banana-400K
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于先进的 Nano-Banana 图像编辑能力与 Gemini-2.5-Pro 自动质量评判，结合精细的 35 类编辑分类体系。
primary_logic: 利用最先进的 MLLM 进行自动生成和评判，可构建覆盖广泛编辑类型、支持多任务（单轮、多轮、偏好对齐）的高质量编辑数据集。
claims:
- 利用 Nano-Banana 从 OpenImages 真实照片生成多样化编辑对
- 采用精细的图像编辑分类体系确保编辑类型覆盖
- 使用 MLLM 进行质量评分的系统化质量控制
- 包含 72K 多轮编辑示例和 56K 偏好对示例
---

# Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing

> [!tip] 核心洞察
> 利用最先进的 MLLM 进行自动生成和评判，可构建覆盖广泛编辑类型、支持多任务（单轮、多轮、偏好对齐）的高质量编辑数据集。

| 字段 | 内容 |
|------|------|
| 中文题名 | Pico-Banana-400K：用于文本引导图像编辑的大规模数据集 |
| 英文题名 | Pico-Banana-400K: A Large-Scale Dataset for Text-Guided Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qian_Pico-Banana-400K_A_Large-Scale_Dataset_for_Text-Guided_Image_Editing_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Pico-Banana-400K (数据集) |
| Dataset | Pico-Banana-400K, OpenImages |
> [!tip] 效果简介
> - 编辑成功率（全局样式） 上，成功编辑比例 0.9340 (Strong artistic style transfer) vs N/A (N/A)。
> - 编辑成功率（空间编辑） 上，成功编辑比例 0.5923 (Relocate object) vs N/A (N/A)。

## 概要

**核心问题瓶颈**：当前文本引导图像编辑领域长期受限于数据集的规模、质量与可分享性。现有数据集如 **MagicBrush**、**GIER**、**UltraEdit** 等虽基于真实图像，但编辑类型覆盖有限、规模不足，且常因版权或隐私限制无法完全公开。合成数据集如 **HQ-Edit**、**Echo-4o-Image** 虽可大规模生成，但往往在视觉真实性与指令保真度上存在差距。这一瓶颈直接制约了鲁棒编辑模型的训练与评估。

**核心方法与洞察**：本文提出 **Pico-Banana-400K**，一个大规模、高质量、完全可分享的文本引导图像编辑数据集。其核心构建逻辑是：利用最先进的 **Nano-Banana** 图像编辑模型，从 OpenImages 真实照片出发，依据精细定义的 35 类编辑分类体系生成多样化编辑对；再以 **Gemini-2.5-Pro** 多模态大语言模型作为自动质量评判器，从指令合规性、编辑无缝性、内容保留平衡和技术质量四个维度进行系统化质量筛选。数据集不仅包含约 258K 单轮编辑样本，还额外提供 72K 多轮编辑序列和 56K 偏好三元组，支持监督微调、偏好对齐和交互式编辑等多任务研究。

**方法谱系与知识库定位**：该工作属于数据驱动的图像编辑资源构建，位于生成式编辑模型的上游数据层。相较于 **MagicBrush**（真实图像、人工标注）和 **UltraEdit**（真实图像、MLLM 辅助），Pico-Banana-400K 在规模、编辑类型覆盖和可分享性上均有显著扩展；相较于 **GPT-Image-Edit-1.5M**（合成为主），其基于真实照片的源图像选择策略更好地保留了场景自然性。精细的编辑分类体系（8 大类 35 种操作）和双指令格式（详细指令与简洁用户风格指令）为编辑模型提供了更丰富的监督信号。

**主要结果速览**：数据集编辑成功率在不同编辑类型间呈现显著分化。全局外观与风格化编辑表现出极高可靠性，如强艺术风格迁移成功率达 0.9340。而需要精细空间控制或符号保真度的编辑则构成瓶颈：对象重新定位成功率仅 0.5923，改变字体/样式低至 0.5759。这一分化揭示了当前编辑模型在空间推理与排版渲染方面的根本性局限。

**局限与开放问题**：数据集质量受限于 Nano-Banana 的编辑能力和 Gemini-2.5-Pro 的评判偏好，可能引入系统性偏差。细粒度空间编辑和排版编辑的成功率低下，表明这些方向仍是开放难题。此外，多轮编辑序列中的错误累积效应尚未被系统分析，数据集的零样本泛化能力也有待下游模型训练验证。



文本引导的图像编辑旨在根据自然语言指令对输入图像进行修改，生成符合语义意图的编辑结果。这一任务在创意设计、内容创作和人机交互等领域具有广泛应用前景。然而，当前该领域面临一个核心瓶颈：**缺乏大规模、高质量且完全可分享的编辑数据集**，这严重制约了鲁棒编辑模型的训练与发展。

现有数据集存在明显的结构性缺陷。真实图像编辑数据集如 **GIER**、**MagicBrush**、**UltraEdit** 和 **OmniEdit** 在规模或编辑类型覆盖上存在局限；合成编辑数据集如 **HQ-Edit** 和 **Echo-4o-Image** 虽然规模较大，但图像真实性不足，难以反映真实场景的编辑需求。**GPT-Image-Edit-1.5M** 试图兼顾规模与多样性，但其质量控制和可分享性仍不理想。总体而言，现有数据集在编辑类型的细粒度覆盖、指令格式的多样性、质量保证机制以及多任务支持（单轮编辑、多轮编辑、偏好对齐）等方面均存在明显缺口。

针对上述问题，本文提出 **Pico-Banana-400K** 数据集，其核心动机在于：利用当前最先进的图像编辑模型 **Nano-Banana** 生成多样化的编辑对，结合多模态大语言模型 **Gemini-2.5-Pro** 进行系统化质量评判，从而构建一个覆盖广泛编辑类型、支持多任务训练范式的高质量编辑数据集。该数据集从 OpenImages 真实照片中采样源图像，采用包含 8 大类别、35 种编辑类型的精细分类体系，并提供长详细指令与简短用户风格指令的双指令格式，最终形成约 258K 单轮监督微调样本、72K 多轮编辑序列以及 56K 偏好三元组的完整数据生态。



## 核心方法与创新机理

Pico-Banana-400K 的核心创新并非提出新的编辑模型架构，而是构建了一个**大规模、高质量、完全可分享的文本引导图像编辑数据集**。与现有数据集相比，其关键差异化要素体现在以下几个维度：

### 1. 利用最先进 MLLM 构建的自动化高质量数据管道

传统图像编辑数据集常受限于人工标注成本高、规模小或质量参差不齐。Pico-Banana-400K 的核心机制创新在于构建了一条**完全自动化的生成-评判闭环管道**：

- **生成端**：利用 **Nano-Banana** 模型（一种先进的图像编辑模型）从 OpenImages 真实照片出发，执行多样化的编辑操作。
- **评判端**：引入 **Gemini-2.5-Pro** 作为自动质量裁判，基于四项加权标准对编辑结果进行系统化评分——指令合规性（40%）、无缝性（25%）、保留平衡（20%）和技术质量（15%）。每个编辑对最多允许三次重试，三次均失败则丢弃，成功前的失败案例则保留为偏好学习数据。

这一设计使得数据集在**无需人工干预**的情况下，同时实现了规模化和质量可控，最终生成了约 258K 成功单轮编辑样本和 56K 偏好对。

### 2. 精细化的 35 类编辑分类体系

与现有数据集通常只覆盖粗粒度编辑类型不同，Pico-Banana-400K 建立了一个覆盖 **8 大类别、35 种具体编辑操作**的精细分类法（Table 1），包括：

- 光度调整（如改变整体色调、调整曝光/对比度）
- 对象级操作（如添加/移除/替换对象、重新定位对象）
- 风格化变换（如强艺术风格迁移、电影颗粒/复古效果）
- 场景与光照修改（如改变背景、外扩绘制）
- 排版编辑（如改变字体/样式、添加/替换文本）

这种细粒度覆盖确保了数据集的编辑类型多样性远超 **MagicBrush**、**GIER**、**UltraEdit** 等现有真实图像编辑数据集，为训练鲁棒的编辑模型提供了更全面的监督信号。

### 3. 双指令格式设计

Pico-Banana-400K 为每个编辑对提供了**两种互补的指令格式**（Table 2）：

- **Type I**：由 Gemini-2.5-Flash 生成的长篇详细指令，提供丰富的编辑描述和监督信号。
- **Type II**：由 Qwen2.5-7B-Instruct 基于人工示例总结的简洁用户风格指令，模拟真实用户的简短查询。

这种双指令设计使得同一数据集可同时服务于**详细监督训练**和**用户友好型推理**两种场景，是现有数据集中少见的创新。

### 4. 多任务子集构建：单轮、多轮与偏好对齐

Pico-Banana-400K 不仅是一个单轮编辑数据集，还系统性地构建了：

- **72K 多轮编辑序列**：模拟真实对话式编辑场景，保持话语连贯性和引用解析。
- **56K 偏好三元组**：每个三元组包含原图、指令、成功编辑和失败编辑，直接支持偏好对齐训练（如 DPO）。

这种**多任务数据组织**使得 Pico-Banana-400K 可同时用于监督微调、多轮对话训练和人类偏好对齐，而 **HQ-Edit**、**Echo-4o-Image** 等合成数据集通常只聚焦于单轮编辑质量。

### 5. 与现有数据集的定位差异

如 Table 3 所示，Pico-Banana-400K 的定位并非追求最大规模（如 **GPT-Image-Edit-1.5M**），而是强调**质量可控、指令忠实和细粒度类型覆盖**。它从最先进的 Nano-Banana 模型蒸馏而来，结合 MLLM 评判的质量保证机制，在数据质量和编辑类型丰富度上形成了差异化优势。

---

**需要人工验证的点**：由于论文未提供在 Pico-Banana-400K 上训练模型的对比实验，上述创新点主要基于数据集构建方法论的分析。数据集对下游编辑模型性能的实际提升效果，仍需后续基准测试和模型训练研究来验证。



Pico-Banana-400K 的构建遵循一条系统化的流水线，旨在同时保证数据规模与质量。流水线以 OpenImages 真实照片为起点，经过源图像筛选、编辑指令生成、图像编辑执行、自动质量评判与子集构建五个核心模块，最终产出包含单轮编辑对、多轮编辑序列和偏好三元组的复合数据集。

**源图像选择模块**从 OpenImages 中采样图像，确保覆盖人类、物体和文本场景三类视觉内容，为后续多样化编辑提供丰富的原始素材。

**编辑指令生成模块**是该流水线的关键创新之一。它基于一套包含 8 大类别、35 种编辑操作的精细分类体系（Table 1），为每张源图像生成两种互补格式的编辑指令：Type I 是由 Gemini-2.5-Flash 编写的长详细指令，提供充分的编辑监督信号；Type II 是由 Qwen2.5-7B-Instruct 参照人工示例总结的简短用户风格指令，模拟真实用户的简洁表达。双指令格式使数据集同时适用于监督微调和用户交互场景。

**图像编辑执行模块**将每条编辑指令送入 Nano-Banana 模型执行编辑。每对（图像，指令）最多允许三次重试：若某次尝试通过质量评判，则对应的成功编辑被保留；若全部三次尝试均失败，该样本被丢弃；若前两次失败而第三次成功，则失败的中间结果也被保存，用于构建偏好数据。

**质量评估模块**使用 Gemini-2.5-Pro 作为自动评判器，基于四项标准对编辑结果打分：指令合规性（权重 40%）、无缝性（25%）、保留平衡（20%）和技术质量（15%）。只有通过评判的编辑对才进入最终发布的单轮子集，总计约 258K 成功样本，同时约 56K 失败案例被保留为偏好三元组（Figure 4）。

**子集构建模块**在此基础上进一步生成多轮编辑序列和偏好数据。多轮编辑遵循与单轮相同的执行与评估流程，每轮指令作用于当前工作图像以产生下一张图像，模型被鼓励使用指代性语言（如“the image”、“the previous edit”）来维持话语连贯性，最终形成 72K 多轮编辑序列（Figure 5）。偏好三元组则由原始图像、编辑指令、一次成功编辑和一次失败编辑组成，用于对齐研究。

整个流水线的输入是 OpenImages 真实照片，输出是一个包含 258K 单轮编辑对、72K 多轮序列和 56K 偏好三元组的大规模数据集，覆盖从全局风格迁移到细粒度空间编辑的广泛编辑类型。

### 补充图表

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/001_Figure_1.jpg]]
*Figure 1: Construction pipeline and dataset composition of Pico-Banana-400k*



Pico-Banana-400K 是一个数据集工作，其核心在于构建管线而非可微模型，因此本节聚焦于数据生成与质量控制的五个关键模块及其运作机制，不涉及模型训练公式。

**1. 源图像选择模块**

从 OpenImages 中采样真实照片，确保覆盖人类、物体和文本场景三类内容。这一筛选策略为后续编辑指令的多样性提供了视觉基础，避免数据集偏向单一场景类型。

**2. 编辑分类体系模块**

定义了 8 大类 35 种编辑类型的精细分类法（Table 1），涵盖光度调整、对象级操作、风格化变换、场景与光照修改等。该分类体系是数据集覆盖度的制度性保证——每种编辑类型均需生成足量通过质量评判的样本，若某（图像，指令）对三次尝试均失败则丢弃，成功样本的中间失败结果则保留为偏好数据。

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/003_Table_1.jpg]]
*Table 1: Image editing taxonomy. Each operation is grouped under its category. Count denotes the number of successful samples in the single-turn subset that passed the Gemini-2.5-Pro judge (instruction compliance and visual quality) within at most three retries. If all three attempts fail for an (image, instruction) pair, the case is deemed a failure and discarded from the released set. If one or two attempts before arriving at a successful edit, then the negative edits are also saved to form the preference data*

**3. 双指令生成模块**

为每个编辑操作生成两种互补的指令格式：
- **Type I（长详细指令）**：由 Gemini-2.5-Flash 生成，包含编辑目标、约束条件和细节描述，为模型训练提供密集监督信号。
- **Type II（短用户风格指令）**：由 Qwen2.5-7B-Instruct 基于人工示例总结生成，模拟真实用户简洁交互风格。

两种指令指向同一编辑目标，形成“详细监督—简洁推理”的双视图训练对。

**4. 图像编辑执行与质量评估模块**

这是管线的核心闭环：
- **执行**：由 Nano-Banana 模型根据指令对源图像进行编辑，最多重试三次。
- **评估**：由 Gemini-2.5-Pro 作为自动评判器，按四项加权标准打分：
  - 指令合规性（Instruction Compliance）：权重 40%
  - 无缝性（Seamlessness）：权重 25%
  - 保留平衡（Preservation Balance）：权重 20%
  - 技术质量（Technical Quality）：权重 15%

通过评判的编辑对进入单轮监督微调子集（约 258K），失败案例（约 56K）保留为偏好三元组（源图、成功编辑、失败编辑）用于偏好对齐研究。

**5. 多轮编辑序列构建模块**

以单轮编辑的最终图像作为下一轮的输入，逐轮应用新指令，形成连贯的编辑序列（约 72K 示例）。执行与评估流程与单轮设置完全一致。序列构建中鼓励模型使用指代语言（referential language），以保持话语连贯性和引用解析能力。

**关键机制总结**

整个管线的因果杠杆在于：用最先进的 MLLM（Nano-Banana 执行编辑，Gemini-2.5-Pro 自动评判）构建闭环生成—评估系统，配合精细分类体系，实现了覆盖广泛编辑类型、支持单轮/多轮/偏好对齐三种任务的高质量数据集。该管线不涉及可学习的数学公式，所有质量信号均来自 MLLM 的评判输出。

### 补充图表

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/004_Table_2.jpg]]
*Table 2: Examples of Gemini written vs. Qwen summarized editing instructions*



## 实验与关键发现

### 数据集统计与质量分析

Pico-Banana-400K 最终包含约 **258K 单轮编辑监督微调样本**、**56K 偏好三元组**（成功-失败编辑对）以及 **72K 多轮编辑序列**。单轮编辑对的质量通过 Gemini-2.5-Pro 自动评判系统进行严格筛选：每个 (图像, 指令) 对最多允许三次尝试，若三次均未通过评判（指令合规性与视觉质量），则该样本被丢弃；若前两次失败而第三次成功，则失败尝试被保留为偏好数据中的负样本。

Table 1 给出了完整的 35 类编辑分类体系及各类别通过质量筛选的成功样本数量。8 大类别包括：全局外观编辑、风格化编辑、对象级编辑、人物编辑、文本/排版编辑、空间/布局编辑、场景/光照编辑以及视角/构图编辑。

### 编辑成功率分析

Figure 6 展示了各编辑类型的成功率分布，呈现出明显的“易-难”梯度：

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/011_Figure_6.jpg]]
*Figure 6: Per–edit type success rates*

**高成功率编辑（全局与风格化）**：
- 强艺术风格迁移成功率达 **0.9340**
- 胶片颗粒/复古效果达 **0.9068**
- 现代↔历史风格重塑达 **0.8875**
- 改变整体色调达 **0.8793**

这些编辑类型涉及全局外观变换，对精确空间控制要求低，Nano-Banana 模型表现出高度可靠性。

**低成功率编辑（空间与排版）**：
- 重新定位对象成功率仅 **0.5923**，为所有编辑类型中最低
- 改变字体/样式仅 **0.5759**
- 改变大小/形状/方向为 **0.6627**
- 外扩绘制（outpainting）为 **0.6634**

失败模式主要表现为透视不一致、结构断裂以及排版编辑中的字体完整性丧失。这些结果表明，**需要精细空间控制或符号保真度的编辑仍是当前图像编辑模型的核心瓶颈**。

### 偏好数据与多轮编辑

Figure 4 展示了典型的偏好三元组结构：同一原始图像和编辑指令下，成功编辑满足指令要求并保持场景上下文，而失败编辑则违反指令（如错误的物体放置/几何关系）。这 56K 偏好对为后续的对齐研究（如 DPO 或 RLHF）提供了直接训练信号。

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/007_Figure_4.jpg]]
*Figure 4: Preference triplet example. From left to right: the original image, the natural-language instruction (center panel) requesting relocation of the pink–white straws into the leftmost glasses, and two model outputs: a successful edit that satisfies the instruction and preserves scene context, and a failed edit that violates the instruction (incorrect placement/geometry). Such (success, failure) pairs are retained as preference data for alignment studies*

多轮编辑序列（Figure 5）展示了模型在连续编辑中的表现：从原始南瓜图像开始，依次应用复古胶片效果、替换背景为鬼屋场景、转换为雪景、调整全局光照为暖金色调。论文指出模型在多轮对话中保持了话语连贯性和引用解析能力，但未对多轮编辑中的错误累积效应进行定量敏感性分析，这一点需要读者注意。

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/009_Figure_5.jpg]]
*Figure 5: Multi-turn image editing example. Starting from the original pumpkin image, the model first applies a vintage film grain effect, replaces the dark background with a haunted house scene, transforms the entire setting into a snowy winter landscape, and finally adjusts the global lighting to a warm, golden-hour glow, producing the final image on the right*

### 数据集横向对比

Table 3 将 Pico-Banana-400K 与代表性图像编辑数据集进行了横向对比。相较于 GIER、MagicBrush、UltraEdit、OmniEdit 等现有真实图像编辑数据集，以及 HQ-Edit、Echo-4o-Image、GPT-Image-Edit-1.5M 等合成/混合数据集，Pico-Banana-400K 的核心区分点在于：
1. **精细分类覆盖**：35 类编辑类型体系，远超多数现有数据集的粗粒度分类
2. **双指令格式**：同时提供详细监督指令和简洁用户风格指令
3. **内置偏好数据**：直接提供成功-失败编辑对用于对齐训练
4. **多轮编辑支持**：72K 多轮序列覆盖连续编辑场景

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/012_Table_3.jpg]]
*Table 3: Side-by-side comparison of representative image editing datasets*

### 局限与开放问题

基于数据集分析，论文明确指出的开放问题包括：
- 细粒度空间编辑、布局外推和排版编辑仍是未解决的难题
- 有前景的方向包括更强的空间条件化、几何感知训练目标、显式文本渲染监督以及面向人物的身份保持约束

需要注意的是，本数据集的质量评估完全依赖于 Nano-Banana 的编辑能力和 Gemini-2.5-Pro 的评判能力，可能存在模型偏好引入的系统性偏差。此外，论文未提供在该数据集上训练模型的基准测试结果，数据集的实际训练效用有待后续工作验证。

### 补充图表

![[assets/figures/papers/paper_list_l771_https_openaccess_thecvf_com_content_CVPR2026_html_Qian_Pico_Banana_400K/figures/005_Figure_3.jpg]]
*Figure 3: Distribution of image editing instruction content*



## 定位与知识库关联

### 1. 与现有数据集的横向对比

Pico-Banana-400K 的定位需要在文本引导图像编辑数据集的发展脉络中审视。当前该领域的数据集可大致分为真实图像编辑数据集和合成编辑数据集两类。

**真实图像编辑数据集**方面，早期的 **GIER** 和 **MagicBrush** 提供了基于真实照片的人工标注编辑对，但规模有限，编辑类型覆盖较窄。**UltraEdit** 和 **OmniEdit** 在此基础上扩展了规模和编辑多样性，但仍受限于人工标注的成本和质量控制瓶颈。**合成编辑数据集**方面，**HQ-Edit** 和 **Echo-4o-Image** 利用生成模型自动构建编辑对，实现了大规模扩展，但面临着编辑质量不稳定、指令保真度不足的问题。**GPT-Image-Edit-1.5M** 试图融合真实与合成数据，但论文明确指出其更强调规模而非精细的质量控制。

Pico-Banana-400K 的方法论创新在于**将最先进的 MLLM 同时用于编辑执行和质量评判**，形成了闭环的质量保证机制。其核心差异化体现在三个维度：

1. **精细分类体系驱动**：定义了覆盖 8 大类别、35 种编辑操作的分类法（Table 1），从全局外观调整到细粒度空间操作均有系统覆盖，而非依赖随机的指令生成。
2. **双指令格式**：同时提供 Gemini-2.5-Flash 生成的长详细指令和 Qwen2.5-7B-Instruct 总结的简短用户风格指令（Table 2），为模型训练提供多层次的监督信号。
3. **多任务子集构建**：除 258K 单轮监督微调样本外，还包含 72K 多轮编辑序列和 56K 偏好三元组，支持单轮编辑、多轮对话编辑和偏好对齐三类任务的统一训练。

论文在 Table 3 中提供了与代表性数据集的并排对比，明确展示了 Pico-Banana-400K 在编辑类型覆盖度、质量控制和多任务支持方面的优势。但需注意，该数据集本质上是 **Nano-Banana 模型的蒸馏产物**（Section 4），其质量上限受限于该生成模型的能力边界。

### 2. 适用边界与能力瓶颈

Pico-Banana-400K 的适用边界由其构建管线的能力分布直接决定。Figure 6 揭示了一个清晰的**难度分层结构**：

**高可靠性区域**（成功率 > 0.85）：全局外观编辑和风格化转换表现最为稳定。强艺术风格迁移成功率达 0.9340，电影颗粒/复古效果为 0.9068，现代-历史风格转换约 0.8875。这些编辑类型主要涉及全局纹理和色彩分布的调整，对空间精确性要求较低。

**中等可靠性区域**（成功率 0.70–0.85）：对象替换、背景替换、光照调整等需要局部语义理解的编辑处于此区间。这些任务要求模型正确识别编辑区域并保持与周围场景的一致性。

**低可靠性区域**（成功率 < 0.70）：需要精细空间控制或符号保真度的编辑类型构成当前瓶颈。具体表现为：
- **空间操作**：对象重新定位成功率仅 0.5923，改变尺寸/形状/方向为 0.6627，外扩绘制为 0.6634。
- **排版编辑**：改变字体/样式成功率低至 0.5759，添加/替换文本同样不稳定，难以在真实场景中保持字体完整性和透视一致性。

这种分层结构揭示了当前 MLLM 驱动的编辑管线在**几何推理**和**符号渲染**两个维度上的根本性局限。数据集虽然通过 Gemini-2.5-Pro 的质量评判过滤了完全失败的案例，但低成功率区域的样本质量仍可能存在较大的方差。

### 3. 局限性与开放问题

**已确认的局限性**：

1. **生成模型偏差**：数据集质量完全依赖于 Nano-Banana 的编辑能力和 Gemini-2.5-Pro 的评判标准，可能系统性继承这些模型的偏好和盲区。例如，评判标准中“指令合规性”占 40% 权重，可能导致对视觉质量相对宽松的样本仍被保留。
2. **细粒度空间编辑质量不足**：如前述，空间操作和排版编辑的成功率显著偏低，失败案例常出现透视不一致、结构断裂或字体变形等问题。
3. **多轮编辑的误差累积**：论文未对多轮编辑序列进行敏感性分析，无法评估随着编辑轮次增加，误差累积对最终图像质量的影响程度。
4. **数据集规模的非均匀分布**：Table 1 显示不同编辑类型的样本数量差异较大（如“改变整体色调”有 14745 个样本，而某些细粒度操作可能仅有数百个），可能导致训练模型在某些编辑类型上的能力不均衡。

**开放问题**：

1. **空间编辑能力的提升路径**：如何在数据集构建层面改善细粒度空间编辑的质量？可能的方案包括引入更强的空间条件控制（如布局图、关键点）、设计几何感知的训练目标，或在评判标准中增加空间一致性的权重。
2. **排版编辑的专门化处理**：文本渲染在自然图像编辑中具有独特挑战，是否需要引入显式的文本渲染监督信号或专门的文本感知评判模块？
3. **数据集的下游训练效果**：论文仅提供了数据集本身的统计分析，尚未报告使用该数据集训练模型后的性能表现。该数据集对模型可控性和视觉保真度的实际影响仍需通过训练实验验证。
4. **泛化到新编辑类型的能力**：35 类编辑分类体系虽然精细，但仍为封闭集合。模型在零样本或少样本场景下泛化到未见编辑类型的能力尚未被探索。
5. **多轮编辑的长期规划**：多轮编辑序列涉及对话状态跟踪和渐进式修改的推理能力，是否可以通过强化学习或过程监督进一步优化，是一个值得探索的方向。
6. **人工评估的缺失**：当前质量评判完全依赖 Gemini-2.5-Pro 的自动评分，缺乏人工评估作为基准参照，自动评判的可靠性边界尚不明确。



## 原文 PDF

![[paperPDFs/CVPR_2026/Pico_Banana_400K_A_Large_Scale_Dataset_for_Text_Guided_Image_Editing.pdf]]
