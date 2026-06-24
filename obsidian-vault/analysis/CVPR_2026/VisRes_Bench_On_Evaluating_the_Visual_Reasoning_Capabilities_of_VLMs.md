---
title: "VisRes Bench: On Evaluating the Visual Reasoning Capabilities of VLMs"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VisRes_Bench_On_Evaluating_the_Visual_Reasoning_Capabilities_of_VLMs.pdf
project_link: "https://visres-bench.github.io"
code_link: null
aliases:
- VB
- VBEVRCV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过移除语言监督并将任务复杂性分解为感知重建、单属性规则抽象和多属性组合推理三个层次，系统性地诊断VLMs的视觉推理能力。
primary_logic: VLMs在文本条件下的表现可能主要源自语言先验，而非真正的视觉理解；视觉推理需要从知觉组织到组合抽象的分层能力，而当前模型在底层视觉抽象（如遮挡补全、方向感知）上存在严重缺陷，导致高层推理失败。
claims:
- Level-1微调实验表明原始Qwen2.5-3B平均准确率仅24.5，远低于人类基线的90.4。
- GPT-5在Level-2的Uniform Color任务上准确率可达96-97%，但在Level-3多属性任务上降至34-56%。
- Frontier模型在单属性方向识别上准确率仅39.8% (GPT-4o) 和49.6% (GPT-5)，远低于颜色和计数。
- 启用思考模式一致提升所有模型在各个Level上的表现，尤其在Level-3上提升显著。
---

# VisRes Bench: On Evaluating the Visual Reasoning Capabilities of VLMs

> [!tip] 核心洞察
> VLMs在文本条件下的表现可能主要源自语言先验，而非真正的视觉理解；视觉推理需要从知觉组织到组合抽象的分层能力，而当前模型在底层视觉抽象（如遮挡补全、方向感知）上存在严重缺陷，导致高层推理失败。

| 字段 | 内容 |
|------|------|
| 中文题名 | VisRes Bench：评估视觉语言模型视觉推理能力的基准 |
| 英文题名 | VisRes Bench: On Evaluating the Visual Reasoning Capabilities of VLMs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Tortei_VisRes_Bench_On_Evaluating_the_Visual_Reasoning_Capabilities_of_VLMs_CVPR_2026_paper.html) · [Project](https://visres-bench.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VisRes Bench |
| Dataset | VisRes Level-1 subtasks |

> [!tip] 效果简介
> - VisRes Level-1 subtasks 上，Accuracy (average) 43.7% (Finetuned Qwen2.5-3B) vs 24.5% (Original Qwen2.5-3B) (+19.2)；Accuracy (average) 43.7% (Finetuned Qwen2.5-3B) vs 90.4% (Human Baseline) (-46.7)。

## 概述

**VisRes Bench**（CVPR 2026）系统性地诊断了当前视觉语言模型（VLMs）在纯视觉推理上的根本缺陷。其核心发现是：**VLMs 在剥离语言上下文后，视觉推理能力急剧退化**——前沿模型在底层视觉抽象（如遮挡补全、方向感知）上表现糟糕，导致高层组合推理失败；而它们在文本条件下的良好表现，很大程度上源自语言先验，而非真正的视觉理解。

### 问题瓶颈

现有 VLM 评测多依赖于自然语言问答，语言监督为模型提供了捷径，掩盖了其视觉编码器本身的推理局限。VisRes Bench 通过**纯图像四选一格式**最小化语言先验，将任务复杂性分解为三个递进层次：

1. **Level 1 — 感知重建**：要求模型直接补全或匹配被遮挡的自然图像区域，无需显式规则推理。
2. **Level 2 — 单属性规则抽象**：在 Raven 式 3×3 网格中，根据单一视觉属性（颜色、方向、计数）的变化规律推断缺失单元。
3. **Level 3 — 多属性组合推理**：需要同时追踪多个属性的变化模式进行组合推理。

这一分层设计使得研究者能够精确锁定 VLM 视觉推理失败的具体层级和属性维度。

### 方法定位

VisRes Bench 并非提出新模型架构，而是一个**诊断性评测基准**，包含约 19,000 个评估样本。其方法贡献在于：

- **数据构建**：从 Google Street View 和公开网页收集自然图像，经半自动标注管线生成多属性标签，利用随机采样与 DINOv2 相似度采样构造干扰项。
- **评估框架**：支持通用提示和引导提示两种变体，并允许启用思考模式（thinking mode），以测量推理过程对性能的影响。
- **分析维度**：通过微调实验、属性解耦、文本化对照、分辨率消融等手段，多角度揭示模型能力边界。

### 核心结论

- **感知重建严重不足**：微调后的 Qwen2.5-3B 在 Level-1 上平均准确率仅 43.7%，远低于人类基线的 90.4%（Table 2）。MAE 像素重建检索准确率随 tile 尺寸增大从 62.6% 骤降至 39.4%（Table 5），表明模型的底层视觉补全能力有限。
- **方向感知是突出短板**：前沿模型在单属性方向识别上准确率仅 39.8%（GPT-4o）和 49.6%（GPT-5），远低于颜色（84.6%/97.6%）和计数（72.4%/94.2%）（Table 3）。
- **组合推理急剧退化**：GPT-5 在 Level-2 的 Uniform Color 任务上可达 96–97%，但在 Level-3 多属性任务上骤降至 34–56%（Table 1），说明单属性感知是多属性组合推理的必要但非充分条件。
- **思考模式与分辨率带来一致增益**：启用思考模式持续提升所有模型在各 Level 上的表现，开源模型在无思考模式下接近随机水平（Table 6）；将输入分辨率从 512×512 提升至 2048×2048，GPT-5 的 Level-1 准确率从 45.17% 升至 56.51%（Table 7）。

这些结果表明，当前 VLMs 的视觉推理能力存在层级性缺陷——底层知觉组织的不足向上传导，最终导致高层抽象推理的崩溃。

## 背景与动机

视觉推理——从原始像素中抽象出结构、规则和关系的能力——是人类智能的基石，也是构建通用视觉系统的长期目标。当前视觉语言模型（VLMs）在广泛的多模态基准上展现出了令人瞩目的能力，但其成功在多大程度上源自真正的视觉理解，而非对语言先验的依赖，仍是一个悬而未决的问题。现有评估范式通常将视觉输入与自然语言问题配对，这使得模型可以通过文本捷径绕过视觉感知的深层困难，掩盖了其视觉推理能力的真实边界。

VisRes Bench的核心动机正是填补这一评估盲区。该工作观察到，当移除语言上下文并将任务严格限定为纯图像四选一格式时，VLM的视觉推理能力会急剧下降，在感知扰动下甚至接近随机水平。更关键的是，模型在文本条件下表现出的“推理能力”可能主要源于语言先验，而非对视觉世界的真实建模——这一假设构成了整个基准设计的出发点。

为系统性地诊断这一问题，VisRes Bench将视觉推理分解为三个递进层次：**感知重建**（Level-1）、**单属性规则抽象**（Level-2）和**多属性组合推理**（Level-3）。这一分层结构对应了从知觉组织到组合抽象的认知光谱，使得研究者可以精确定位模型的能力边界与失败模式。初步证据表明，当前VLM在底层视觉抽象——如遮挡补全、方向感知——上存在严重缺陷，这些底层瓶颈直接导致了高层组合推理的失败，形成了视觉推理的级联式脆弱性。

## 核心创新

VisRes Bench的核心创新在于**将视觉推理分解为从感知重建到组合抽象的层次化诊断框架**，并通过纯视觉多选格式剥离语言先验，从而暴露VLM在视觉理解上的真实瓶颈。

### 1. 层次化视觉推理诊断框架

现有视觉推理基准通常将感知与推理混杂评估，难以定位模型失败的具体环节。VisRes将任务复杂性显式分解为三个递进层次：

- **Level 1 — 感知重建**：要求模型直接完成图像补全或匹配，不涉及显式规则推理。包括局部补丁补全（Edges、Location、Rotation、Brightness、Blur）和全局遮挡补全（50%、80%遮挡率）。这一层诊断模型的底层视觉抽象能力。
- **Level 2 — 单属性规则抽象**：在Raven式3×3网格中，单一视觉属性（颜色、方向、计数）沿行变化，模型需推断该属性并选择缺失单元格。这一层检验模型能否从视觉模式中抽取出单个抽象规则。
- **Level 3 — 多属性组合推理**：多个属性同时变化，模型必须联合推理不同属性的变化规律才能正确作答。这一层测试组合抽象能力，是视觉推理的核心挑战。

这一分层设计使得研究者能够**逐层定位VLM的失败来源**——究竟是底层感知缺陷导致高层推理崩塌，还是推理能力本身不足。

### 2. 纯视觉多选格式剥离语言先验

VLM在文本条件下的表现可能主要源自语言先验，而非真正的视觉理解。VisRes采用**纯图像四选一格式**，任务呈现为一张主图和四个候选选项（A–D），完全不依赖语言监督。这一设计的关键创新在于：

- **最小化语言捷径**：模型无法通过文本关联或常识猜测答案，必须基于视觉内容进行推理。
- **两种提示变体**：通用提示（Generic）仅给出任务格式说明，引导提示（Guided）指出需关注的视觉属性。两者对比可揭示模型在有无语言引导下的推理差异。

### 3. 干扰项生成策略

Level-1任务的干扰项生成采用两种互补策略：

- **随机采样（Random Sampling, RS）**：从图像中随机选取非目标区域，提供基础难度。
- **DINOv2相似度采样（DINOv2 Similarity, DS）**：在64个均匀采样的候选补丁中，计算DINOv2-large嵌入，选取余弦相似度最高的三个作为干扰项。这一策略生成语义相似但视觉错误的干扰项，显著提升任务难度，更真实地考验模型的细粒度视觉辨别能力。

### 4. 与现有基准的本质差异

不同于依赖文本问答或自然图像分类的现有基准，VisRes的changed slots体现在：

| 维度 | 传统视觉推理基准 | VisRes Bench |
|------|-----------------|-------------|
| 任务格式 | 文本问答为主 | 纯图像四选一 |
| 语言依赖 | 高，存在语言先验 | 极低，剥离语言监督 |
| 能力诊断 | 混合评估 | 分层诊断（感知→单属性→多属性） |
| 干扰项设计 | 随机或简单负样本 | DINOv2相似度采样，难度可控 |
| 可扩展性 | 依赖人工标注 | 半自动标注流水线，19,000样本 |

### 5. 核心洞察

VisRes揭示的关键发现是：**VLM在文本条件下的表现可能严重依赖语言先验，而非真正的视觉理解**。当移除语言上下文后，即使是前沿模型在底层视觉抽象任务（如遮挡补全、方向感知）上也表现糟糕，这直接导致高层组合推理的失败。这一洞察为VLM的视觉能力评估提供了新的方法论范式。

## 整体框架

VisRes Bench 的核心设计目标是通过一个纯视觉的四选一基准，剥离语言先验对视觉推理能力的干扰，从而系统性地诊断当前视觉语言模型（VLMs）在感知重建、单属性抽象和多属性组合推理三个层次上的真实能力。整个基准围绕三个递进的复杂度层级构建，每个层级对应不同的视觉推理瓶颈。

### 任务层级与复杂度递进

VisRes 将视觉推理分解为三个层次，形成从底层感知到高层组合抽象的诊断阶梯：

- **Level 1 — 感知重建与匹配**：任务要求模型在无显式规则推理的情况下，直接完成视觉补全或匹配。具体包含局部补丁补全（如边缘连续性、位置、旋转、亮度、模糊）和全局遮挡补全（遮挡50%和80%的图像）。这些任务考察的是模型对低层纹理、结构和几何连续性的感知能力。
- **Level 2 — 单属性规则抽象**：任务采用 Raven 式 3×3 网格，其中单一视觉属性（颜色、方向或计数）沿行或列按规则变化，模型需推断缺失单元格的正确属性值。这一层级测量模型能否从视觉模式中抽象出单一维度的变化规则。
- **Level 3 — 多属性组合推理**：在 Level 2 的基础上，网格中同时存在多个属性的变化规则（如三种不同颜色、三种不同方向、或颜色-方向-计数的混合组合），要求模型进行联合属性推理。这一层级直接检验模型是否具备真正的组合泛化能力。

图 Figure 1 展示了三个层级的具体任务样例，图 Figure 2 则图解了 Level 2 和 Level 3 中使用的模式规则结构。

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/001_Figure_1.jpg]]
*Figure 1: Real samples from each level. Level 1 (top) involves direct visual completion and matching without explicit rule inference (e.g., patch-C correctly continues the ceiling texture compared to patch-D), while Levels 2 and 3 (bottom) require increasingly complex rule-based reasoning over perceptual attributes. Accurate perception of individual attributes is necessary but not sufficient for solving compositional tasks. Current VLMs show poor performance on these compositional tasks. See Section 4.2*

### 数据与标注管线

整个基准包含约 19,000 个评估样本，其构建依赖一条半自动化的数据处理与标注管线：

1. **数据采集与预处理模块**：Level 1 的图像来源于 Google Street View（用于遮挡任务）和公开网页图像（用于局部补全任务），经过过滤和中心裁剪等预处理后形成基础图像池。局部补全任务使用 80×80 像素的掩码补丁，以白色方块加黑色边框的形式呈现，最终组合成 512×512 的复合图像。
2. **半自动标注管线**：对于 Level 2 和 Level 3 所需的颜色、计数、方向标签，管线结合了图像元数据、Molmo 计数模型和 GPT-5 验证，并辅以人工标注进行校正，从而在保证标注质量的同时兼顾可扩展性。需要指出的是，方向属性的标注仍高度依赖人工，这在一定程度上限制了数据规模的上限。
3. **任务生成引擎**：Level 1 的干扰项（错误候选补丁）通过两种策略生成：随机采样（RS）和基于 DINOv2 相似度的采样（DS）。在 DS 策略中，系统均匀采样 64 个不重叠的候选补丁，计算其 DINOv2-large 嵌入，并选取余弦相似度最高的三个作为干扰项。Level 2 和 Level 3 的 Raven 式网格及干扰项则由规则引擎程序化生成。

### 评估框架与输入输出流

所有任务均以统一的四选一格式呈现：一张主图像和四个候选选项（A–D），其中仅有一个正确补全，其余三个为程序化生成的干扰项。这种纯图像格式的设计刻意最小化语言先验的介入，确保模型的表现反映的是视觉推理能力而非文本捷径。

评估框架支持两种提示变体：
- **通用提示**：仅提供最简指令，不指明需关注的视觉属性。
- **引导提示**：明确指出当前任务应关注的视觉属性（如“注意方向的变化”）。

评估对象覆盖了当前主流的开源与闭源 VLM，包括 **GPT-4o**、**GPT-5**、**Gemini**、**Qwen2.5-VL**、**InternVL3.5**、**Kimi-VL**、**Mimo-VL** 和 **GLM-4.5V**。此外，框架还支持思考模式（thinking mode）的开启与关闭对比，以及输入图像分辨率的调节，为分析模型行为提供了多维度的控制变量。

### 诊断逻辑与核心因果机制

VisRes 的诊断逻辑建立在一条清晰的因果链上：如果 VLMs 在文本条件下的表现主要源自语言先验而非真正的视觉理解，那么在纯视觉任务中应观察到显著的性能下降。实验设计通过以下机制来验证这一假设：

- **层级隔离**：Level 1 剥离了规则推理需求，直接测量感知重建能力；Level 2 引入单属性规则，测量抽象能力；Level 3 叠加多属性组合，测量组合泛化能力。若模型在低层就已失败，则高层推理的失败可归因于感知瓶颈的传导。
- **文本解耦**：通过将 Level 2 和 Level 3 任务转换为纯文本描述（Table 4），可以对比模型在视觉输入与语言输入下的推理能力差异，从而量化视觉模态本身带来的性能损失。
- **感知探针**：使用 MAE 在像素空间进行重建检索（Table 5），以 L2 距离 $d_{\mathrm{pixel}}({\hat{\mathbf{C}}}, \mathbf{C}_i) = \| {\hat{\mathbf{C}}} - \mathbf{C}_i \|_2$ 作为重建质量的度量，从信号层面评估模型的底层视觉编码能力。

这一框架的系统性在于：它不是简单地报告模型的综合得分，而是通过分层任务设计、模态解耦和感知探针的组合，定位模型在“知觉组织→单属性抽象→组合推理”这一认知链条上的具体断裂点。

## 核心模块与公式推导

### 1. 数据采集与预处理模块

Level-1 任务的基础数据来源于多源自然图像池：遮挡任务使用 Google Street View 场景，局部补全任务使用公开网页图像。所有图像经过过滤和中心裁剪预处理，为感知重建任务提供标准化的视觉输入。

### 2. 半自动化标注流水线

针对 Level-2 和 Level-3 所需的颜色、计数、方向属性标签，VisRes 构建了一条半自动化标注流水线。该流水线将元数据、Molmo 计数模型和 GPT-5 验证相结合，辅以人工标注，在保证标注质量的同时控制成本。其中方向属性的标注仍高度依赖人工，这构成了数据规模可扩展性的一个瓶颈。

### 3. 任务生成引擎

任务生成引擎是 VisRes 的核心组件，负责为三个层级生成具有不同难度梯度的四选一任务。

**Level-1 干扰项生成**。对于感知补全任务，干扰项（即错误补丁）通过两种策略生成：
- **随机采样**：从图像中随机选取非目标区域。
- **DINOv2 相似度采样**：首先在图像中均匀采样 64 个不重叠的候选补丁，计算每个候选补丁的 DINOv2-large 嵌入向量，然后选取与正确补丁余弦相似度最高的三个作为干扰项。该策略确保干扰项在语义上与正确选项接近，增加任务的感知难度。

**Level-2/3 模式生成**。对于基于规则的推理任务，任务生成引擎构造 3×3 的 Raven 式网格，其中一个单元格缺失。网格的行内属性按照预定义规则变化：
- Level-2：单属性变化（如颜色渐变、方向旋转、数量递增）。
- Level-3：多属性组合变化，要求模型同时追踪多个属性的变化模式。

### 4. 评估框架

所有任务以图像四选一格式呈现，包含一张主图像和四个候选选项（A–D）。评估框架支持两种提示变体：
- **通用提示**：提供最小化指导，测试模型自主识别视觉规律的能力。
- **引导提示**：明确指出需要关注的视觉属性，降低语言理解负担，聚焦于视觉推理本身。

评估框架还支持思考模式的对比测试，以分析推理过程对视觉任务准确率的影响。

### 5. 关键公式

**像素级 L2 距离**。在 Level-1 的感知重建评估中，使用像素级 L2 距离衡量重建补丁与候选裁剪块之间的差异：

$$d_{\mathrm{pixel}}({\hat{\mathbf{C}}}, \mathbf{C}_i) = \| {\hat{\mathbf{C}}} - \mathbf{C}_i \|_2 = \sqrt{ \sum_{h,w,c} ({\hat{\mathbf{C}}}_{hwc} - \mathbf{C}_{i,hwc})^2 }$$

其中：
- ${\hat{\mathbf{C}}}$ 表示模型重建的补丁张量。
- $\mathbf{C}_i$ 表示第 $i$ 个候选裁剪块张量。
- $h, w, c$ 分别遍历高度、宽度和 RGB 通道维度。
- 该距离在 RGB 空间中直接计算，评估像素级重建质量。距离越小，表示重建结果与候选块越接近。

该公式用于 MAE 重建检索实验中，通过计算重建补丁与所有候选块的 L2 距离，选择距离最小的候选块作为预测答案，从而量化模型的底层视觉重建能力。

### 补充图表

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/002_Figure_2.jpg]]
*Figure 2: Illustrative pattern rules used in Levels 2 and 3 tasks. Top: Level-2 tasks where one attribute varies across the row. Bottom: Level-3 tasks where multiple attributes vary. See Section 3.3*

## 实验与分析

VisRes Bench 对 8 款前沿 VLM 进行了系统评估，覆盖三个推理层次、19,000 个评估样本。实验围绕四个核心问题展开：模型在纯视觉条件下的推理能力有多强？底层感知瓶颈如何制约高层推理？微调能否弥补缺陷？思考模式与分辨率等外部因素如何影响性能？

### 4.1 主实验结果：层次化推理能力严重不足

Table 1 报告了在引导提示（guided prompting）与思考模式（thinking mode）启用条件下的各模型准确率。核心发现如下：

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/004_Table_1.jpg]]
*Table 1: Accuracy across VisRes benchmark levels and subtasks under guided prompting with thinking mode enabled (when available)*

**Level-1（感知重建）**：即使是最强的闭源模型，在底层视觉补全任务上也表现挣扎。GPT-5 在 Rotation 子任务上仅达 35.42%，Gemini 在 Global occlusion @50% 上为 57.14%。这些任务对人类而言近乎直觉（人类基线约 91%），但模型在需要精细纹理延续和遮挡推理的场景中频繁失败。

**Level-2（单属性规则推理）**：模型在 Uniform Color 任务上表现最强（GPT-5 达 96–97%），Uniform Count 次之，但 Uniform Orientation 成为显著瓶颈——GPT-4o 仅 39.8%，GPT-5 仅 49.6%。这一分化揭示了一个关键因果链：**方向感知是当前 VLM 视觉编码的致命短板，直接限制了后续任何涉及空间关系的推理任务。**

**Level-3（多属性组合推理）**：当任务要求同时追踪颜色、方向、计数中的多个变化维度时，所有模型准确率骤降。GPT-5 在 3-different 类任务上降至 34–56% 区间，表明模型无法可靠地进行属性绑定与组合抽象。从 Level-2 到 Level-3 的性能断崖说明，单属性感知的必要性并不自动转化为组合推理的充分性。

### 4.2 感知瓶颈诊断：方向识别是罪魁祸首

为解耦感知与推理，Table 3 单独测量了前沿模型在单属性识别上的原始能力。颜色识别（GPT-5: 97.6%）和计数（GPT-5: 94.2%）已接近人类水平，但方向识别准确率仅为 49.6%（GPT-5）和 39.8%（GPT-4o）。这一差距远超随机猜测（四选一基线 25%），但远不足以支撑可靠的规则推理。

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/006_Table_3.jpg]]
*Table 3: Frontier-models have high performance on single attributes, but struggle with inferrring orientation*

因果解释链条如下：
1. 视觉编码器对方向特征的表示质量不足；
2. Level-2 的 Uniform Orientation 任务因此失败率高达 50% 以上；
3. Level-3 中任何涉及方向的组合任务（如颜色+方向同时变化）继承并放大了这一误差，导致整体崩溃。

这一发现指向一个根本性问题：**当前 VLM 的视觉主干可能在预训练阶段缺乏足够的方向判别信号，或者其 patch 化编码方式破坏了连续的方向几何结构。**

### 4.3 微调实验：数据驱动方法的上限

Table 2 展示了在 Level-1 任务上对 Qwen2.5-VL-3B 进行监督微调（SFT）的结果。训练集为每个子任务生成 10 万张图像，规模充足。

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/005_Table_2.jpg]]
*Table 2: Finetuning Qwen2.5-3B on Level 1. After finetuning, the model sperformance naturally improves on the Level 1 tasks. However, the performance is well-below human baseline*

- 原始模型平均准确率：24.5%（接近随机水平）
- 微调后平均准确率：43.7%（+19.2 个百分点）
- 人类基线：90.4%

微调带来了显著且一致的提升，但绝对水平仍远低于人类。这表明：**Level-1 所需的视觉补全能力无法通过简单的任务特定微调获得，模型缺乏的可能是底层的像素级重建能力或纹理连续性先验，而非任务格式的适配问题。**

### 4.4 像素重建能力探针：MAE 实验

Table 5 使用 MAE（Masked Autoencoder）作为纯视觉重建能力的探针。将重建补丁与候选裁剪块在 RGB 空间计算 L2 距离进行检索匹配：

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/007_Table_5.jpg]]
*Table 5: MAE Level-1 scores for different tile sizes*

$$d_{\mathrm{pixel}}({\hat{\mathbf{C}}}, \mathbf{C}_i) = \| {\hat{\mathbf{C}}} - \mathbf{C}_i \|_2 = \sqrt{ \sum_{h,w,c} ({\hat{\mathbf{C}}}_{hwc} - \mathbf{C}_{i,hwc})^2 }$$

随着 tile 尺寸从 16×16 增大至 48×48，检索准确率从 62.6% 单调下降至 39.4%。这一退化说明，即使专门训练的像素重建模型，在处理较大缺失区域时也无法可靠恢复纹理细节。VLM 的视觉编码器若缺乏类似的重建能力，在 Level-1 的遮挡补全任务上必然失败——这为微调实验中的性能上限提供了解释。

### 4.5 思考模式与分辨率的影响

**思考模式（Table 6）**：启用思考模式对所有模型在所有 Level 上均带来一致提升。开源模型（Mimo-VL、Qwen）在无思考模式下接近随机水平，启用后显著改善。Level-3 的提升幅度最大，表明多属性组合推理尤其依赖显式的逐步推理过程，而非前馈式模式匹配。

**图像分辨率（Table 7）**：将 GPT-5 的输入分辨率从 512×512 提升至 2048×2048，Level-1 准确率从 45.17 升至 56.51，所有 Level 均有改善。这证实了视觉 token 的信息密度是瓶颈之一——更高分辨率保留了更多纹理和几何细节，直接惠及感知重建任务，并通过改善底层感知间接提升高层推理。

### 4.6 文本化实验：解耦视觉与推理

Table 4 将 Level-2 和 Level-3 任务转换为纯文本描述后评估。当视觉感知负担被移除，模型仅需基于属性描述进行规则推理时，性能大幅提升。这一对比直接证明了：**VLM 在 VisRes 上的失败主要源于视觉感知阶段，而非规则推理能力不足。** 语言先验在文本条件下可被有效利用，但在纯视觉条件下无法补偿感知缺陷。

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/008_Table_4.jpg]]
*Table 4: Text-verbalized results for Level-2 and Level-3*

### 4.7 失败模式总结

综合所有实验，VLM 在 VisRes 上的失败可归纳为三个层次：

| 层次 | 失败模式 | 证据 |
|------|----------|------|
| 感知层 | 方向识别准确率不足 50%，纹理补全能力弱 | Table 3, Table 5 |
| 绑定层 | 多属性同时变化时无法正确绑定属性到对象 | Level-3 准确率断崖式下降 |
| 推理层 | 无思考模式下开源模型接近随机，但文本化后恢复 | Table 6, Table 4 |

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/010_Table_6.jpg]]
*Table 6: Impact of thinking mode on visual reasoning accuracy. Open-source models (Mimo-VL, Qwen) perform near random without thinking but improve when enabled. ✓ indicates thinking mode enabled, ✗ indicates disabled*

这些失败并非孤立存在，而是形成因果链：感知缺陷 → 属性绑定错误 → 组合推理崩溃。当前 VLM 的视觉推理能力高度依赖语言先验的补偿，在纯视觉条件下暴露出从知觉组织到组合抽象的系统性不足。

### 补充图表

![[assets/figures/papers/paper_list_l2753_https_openaccess_thecvf_com_content_CVPR2026_html_Tortei_VisRes_Bench_On/figures/009_Table_7.jpg]]
*Table 7: Studying the impact of image resolution on GPT-5. All levels improve with higher number of image tokens*

## 方法谱系与知识库定位

### 1. 评估范式定位：从语言先验到纯视觉推理

VisRes Bench 的核心设计动机源于对现有VLM基准的批判性审视：多数主流基准（如MMBench、MME、MMMU）允许模型利用文本选项中的语言先验进行“捷径推理”，导致性能指标无法忠实地反映视觉理解能力。VisRes通过**纯图像四选一格式**彻底移除了语言监督信号，迫使模型仅依赖视觉输入完成任务——这一设计选择将其与依赖文本-图像对齐的基准（如Winoground、VALSE）划清了界限。

在任务谱系上，VisRes继承了Raven渐进矩阵（Raven's Progressive Matrices）的规则推理范式，但将其从合成图形域迁移至自然图像域，构建了从感知重建（Level-1）到单属性抽象（Level-2）再到多属性组合（Level-3）的三层复杂度阶梯。这种分层诊断框架与CV-Bench（Tong et al., CVPR 2025）的二维空间推理和BLINK（Fu et al., 2024）的多项选择视觉感知评估形成互补，但VisRes的独特贡献在于**系统性地解耦了感知、单属性规则和多属性组合三个层次**，使得研究者可以精确定位模型的失效层级。

### 2. 与现有基准的关系：互补与空白填补

**感知层基准（Level-1）**：VisRes的局部补丁补全和全局遮挡任务与传统的图像修复（inpainting）评估形成对照，但其四选一格式将重建问题转化为判别任务，降低了评估噪声。与PUG（Bordes et al., 2024）的合成扰动不同，VisRes使用自然图像和基于DINOv2相似度的干扰项生成策略，使得感知难度的生态效度更高。

**推理层基准（Level-2/3）**：在规则推理维度上，VisRes与RAVEN（Zhang et al., 2019）和G-set（Mondal et al., 2024）共享Raven式网格结构，但关键区别在于VisRes使用**自然图像属性**（颜色、方向、计数）而非合成几何形状，且要求模型从像素中直接推断属性值——这暴露了当前VLM在底层视觉抽象（尤其是方向感知）上的系统性缺陷。相比之下，Bongard-OpenWorld（Jiang et al., 2024）评估的是开放世界中的少样本概念学习，而VisRes聚焦于封闭规则空间内的组合推理。

**文本条件化对比**：VisRes通过将Level-2/3任务转化为文本描述（Table 4）进行对照实验，直接量化了视觉-语言能力的差距。这一实验设计与VQAv2的“盲测”（blind test）思路一脉相承，但VisRes将其推广至结构化推理任务，揭示了**文本条件下的高性能可能主要源自语言先验而非真正的视觉理解**。

### 3. 方法适用边界

VisRes的设计选择同时定义了其适用边界：

- **静态图像限制**：基准仅覆盖静态自然图像，未涉及视频时序推理、交互式场景或多模态动态理解。对于评估具身智能或视频理解模型中的视觉推理能力，VisRes无法提供直接证据。
- **封闭格式的局限**：四选一格式虽然降低了评估噪声，但也可能高估或低估真实推理能力——模型可能通过排除法而非正向推理得出正确答案，而开放生成场景中的推理失败无法被捕获。
- **属性空间的覆盖范围**：当前Level-2/3仅覆盖颜色、方向和计数三种属性，尚未扩展到纹理、形状、空间关系等更丰富的视觉概念维度。
- **语言与文化的单一性**：评估仅使用英语提示，且自然图像主要源自Google Street View和公开网页（以西方场景为主），跨语言和跨文化泛化性未经验证。

### 4. 局限与开放问题

**已确认的局限**（来自论文声明）：

1. **方向标注瓶颈**：方向属性的标注仍高度依赖人工，限制了数据规模的可扩展性和标注一致性。这直接影响了Level-2/3中方向相关任务的样本多样性和难度校准。
2. **静态评估范式**：基准无法评估模型在动态场景、交互式推理或持续学习场景下的能力演化。
3. **格式约束**：四选一格式和固定答案集可能无法充分反映开放环境中的推理灵活性。

**开放问题**（需进一步研究验证）：

1. **方向感知失败的根源**：前沿模型在单属性方向识别上的准确率仅39.8%（GPT-4o）和49.6%（GPT-5），远低于颜色（84.6%/97.6%）和计数（72.4%/94.2%）。这一瓶颈的根源尚未明确——是视觉编码器本身的旋转等变性不足，还是预训练数据中缺乏足够的方向判别信号？Table 7显示提高分辨率可带来一致增益，但分辨率提升无法根本解决方向感知的结构性缺陷。

2. **视觉-语言解耦的机制**：Table 4的文本化实验表明，当任务转化为纯文本推理时模型表现大幅提升，但这一现象背后的机制——是视觉编码器丢失了关键属性信息，还是推理模块无法有效利用视觉特征——仍需通过中间表征分析进一步厘清。

3. **架构层面的补救路径**：能否通过设计专用的知觉前端模块（如显式编码方向、对称性等几何属性的模块）来弥补当前VLM在底层视觉抽象上的不足？MAE实验（Table 5）表明像素级重建能力随tile尺寸增大而急剧退化（从16×16的62.6%降至48×48的39.4%），提示当前视觉编码器的底层表征可能不足以支撑精细的视觉推理。

4. **思考模式的作用机制**：Table 6显示启用思考模式一致提升所有模型的表现，尤其在Level-3上提升显著，但思考过程究竟是增强了视觉特征的再提取，还是主要提供了推理步骤的结构化引导，目前缺乏细粒度的消融分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/VisRes_Bench_On_Evaluating_the_Visual_Reasoning_Capabilities_of_VLMs.pdf]]
