---
title: "MultiBanana: A Challenging Benchmark for Multi-Reference Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MultiBanana_A_Challenging_Benchmark_for_Multi_Reference_Text_to_Image_Generation.pdf
project_link: null
code_link: "https://github.com/matsuolab/multibanana"
huggingface_link: "https://huggingface.co/datasets/kohsei/MultiBanana-Benchmark"
aliases:
- MB
- MultiBanana
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 参考图像的数量（从单参考到8参考）和异质性组合（跨域、尺度差异、稀有概念、多语言）是导致性能退化的重要变量，直接引发指令跟随失败和视觉质量下降。
primary_logic: 通过构建 MultiBanana 基准，系统性地揭示了多参考生成中参考保真度与整体图像质量之间的固有矛盾：封闭模型虽能包含所有对象但牺牲构图一致性，开源模型保持视觉干净却遗漏对象。该基准通过引入困难的异质性参考组合，为评估和推进多参考生成能力提供了细粒度的诊断工具。
claims:
- 封闭模型和开源模型在背景替换任务上的表现均显著较差，尤其在参考数量增加时。
- 随着参考数量增多，所有模型的总分均呈下降趋势，但封闭模型在指令对齐和参考一致性上衰减较缓，而开源模型这两个指标本已较低且持续恶化。
- 跨域、不同尺度和视角、稀有概念及多语言等困难参考组合导致所有模型得分降低，验证了这些异质性因素是当前模型的主要挑战。
- 基于 VLM 的自动评估 (GPT-5, Gemini 2.5) 与人类评判高度相关 (Pearson r 0.69/0.57)，验证了评估协议的可靠性。
---

# MultiBanana: A Challenging Benchmark for Multi-Reference Text-to-Image Generation

> [!tip] 核心洞察
> 通过构建 MultiBanana 基准，系统性地揭示了多参考生成中参考保真度与整体图像质量之间的固有矛盾：封闭模型虽能包含所有对象但牺牲构图一致性，开源模型保持视觉干净却遗漏对象。该基准通过引入困难的异质性参考组合，为评估和推进多参考生成能力提供了细粒度的诊断工具。

| 字段 | 内容 |
|------|------|
| 中文题名 | MultiBanana：面向多参考文本到图像生成的挑战性基准 |
| 英文题名 | MultiBanana: A Challenging Benchmark for Multi-Reference Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.22989) · [Code](https://github.com/matsuolab/multibanana) · [HuggingFace](https://huggingface.co/datasets/kohsei/MultiBanana-Benchmark) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MultiBanana Benchmark |
| Dataset | MultiBanana, LAION-5B |
> [!tip] 效果简介
> - 随着参考数量增多，所有模型的总分均呈下降趋势，但封闭模型在指令对齐和参考一致性上衰减较缓，而开源模型这两个指标本已较低且持续恶化。
> - 跨域、不同尺度和视角、稀有概念及多语言等困难参考组合导致所有模型得分降低，验证了这些异质性因素是当前模型的主要挑战。
> - 基于 VLM 的自动评估 (GPT-5, Gemini 2.5) 与人类评判高度相关 (Pearson r 0.69/0.57)，验证了评估协议的可靠性。

## 概述

**核心问题**：现有的多参考图像生成基准存在两个根本性不足——参考图像数量受限（通常1–4张）且未系统考察参考图像之间的异质性（如跨域、尺度差异、稀有概念、多语言文本等）。这导致无法全面诊断模型在多参考场景下的真实瓶颈：当参考数量增加或参考组合变得困难时，模型要么因过度拟合参考细节而产生构图失真，要么完全忽略部分参考对象，暴露出**参考保真度与整体图像连贯性之间的根本权衡**。

**核心方法**：本文提出 **MultiBanana 基准**，将参考图像数量上限扩展至8张，并系统性地引入跨域、不同尺度与视角、稀有概念及多语言文本等困难参考组合。基准构建采用四阶段流水线（真实与合成图像收集→图像过滤→层次类别分类→任务构建与指令生成），并通过基于 VLM 的五维自动评估协议（指令对齐、参考一致性、图像质量、背景-主体匹配、美学质量）进行细粒度诊断。

**关键发现**：
- **背景替换是共同短板**：无论开源还是封闭模型，在背景替换任务上表现均显著较差，且随参考数量增加进一步恶化（Table 3, Figure 5）。
- **封闭模型 vs. 开源模型的行为分化**：封闭模型倾向于包含所有参考对象但牺牲构图一致性，开源模型则保持视觉干净却遗漏对象——这一分化在困难参考组合下尤为突出（Figure 6, Figure 7）。
- **异质性参考是主要挑战**：跨域、不同尺度/视角、稀有概念及多语言等困难组合导致所有模型得分系统性降低，验证了这些因素是当前模型能力的核心瓶颈（Figure 7, Table 2）。
- **评估协议可靠**：基于 GPT-5 和 Gemini 2.5 的自动评估与人类评判高度相关（Pearson r 分别为 0.69 和 0.57），验证了 VLM 评估的可行性（Table 4）。
- **Agentic 框架的有限收益**：Iterative Prompt Refinement 仅对 GPT 有效，对 Nano Banana 无明显提升甚至导致退化，表明迭代优化策略的泛化性有限（Table 3, Section 4.5）。

**方法谱系与知识库定位**：MultiBanana 继承了 DreamOmni2 等基准的编辑任务设计哲学，但通过大幅扩展参考数量上限和引入异质性参考组合，填补了现有多参考评估体系的空白。与 **ImgEdit-Bench**（Ye et al.）和 **DreamOmni2 Benchmark**（Xia et al.）等主流基准相比，后者在高端模型上已接近天花板（Table 7, Table 8），而 MultiBanana 通过困难参考组合提供了更细粒度的区分能力，为推进多参考生成研究提供了新的诊断工具。

## 背景与动机

文本到图像生成领域近年来取得了显著进展，模型已能根据单张参考图像生成高质量且保持主体一致性的结果。然而，现实应用场景往往要求模型同时处理多张参考图像——例如，用户希望将不同来源的人物、物体和背景融合到一幅连贯的图像中。这一多参考生成（multi-reference generation）场景对模型提出了远超单参考设定的挑战：模型不仅需要准确保持每张参考图像中的视觉属性，还必须协调参考之间的语义与空间关系，同时遵循复杂的文本指令。

当前该领域存在一个关键瓶颈：**现有的多参考图像生成基准在参考图像数量、异质性参考组合及指令跟随评估方面存在严重不足**。具体而言，现有基准（如 DreamOmni2、ImgEdit-Bench 等）通常将参考图像数量限制在 1 至 4 张，且未系统性地考察参考图像之间的差异性对生成质量的影响。当参考图像数量增加，或存在跨域（如照片与插画混用）、尺度差异、稀有概念、多语言文本等异质性参考组合时，模型要么因过度拟合参考细节而产生构图失真，要么完全忽略部分参考对象。这揭示了**参考保真度与整体图像连贯性之间的根本权衡**，而现有基准无法全面诊断这一矛盾。

为填补这一空白，本文提出了 **MultiBanana**——一个面向多参考文本到图像生成的挑战性基准。MultiBanana 将参考图像数量上限扩展至 8 张，并系统性地引入了跨域不匹配、尺度与视角差异、稀有概念以及多语言提示等困难参考组合，旨在显式地揭示多参考生成中的独特挑战。通过构建覆盖 3,769 个高质量编辑任务的基准，并设计基于 VLM 的多维度自动评估协议，MultiBanana 为评估和推进多参考生成能力提供了细粒度的诊断工具。

## 核心创新

MultiBanana 的核心创新并非提出新的生成模型架构，而是**构建了一个系统性揭示多参考图像生成瓶颈的挑战性基准**，其创新点体现在三个层面。

### 1. 突破参考数量的上限与异质性组合设计

现有基于参考的图像生成基准（如 DreamOmni2、ImgEdit-Bench 等）通常将参考图像数量限制在 1–4 张，且未系统考察参考图像之间的差异性与兼容性（Table 1）。MultiBanana 将参考数量上限扩展至 **8 张**，并显式引入了四类困难参考组合：

- **跨域参考（Cross-domain）**：参考图像来自不同视觉域（如照片、绘画、渲染图）；
- **尺度与视角差异（Different scale and view）**：同一类对象以不同尺度或拍摄角度呈现；
- **稀有概念（Rare concepts）**：包含低频或不常见的物体类别；
- **多语言文本（Multilingual text）**：参考图像或指令中包含多语言文字渲染需求。

这些异质性组合直接构成了当前模型的性能瓶颈：Figure 7 显示，在跨域和不同尺度/视角任务上，所有模型的得分均显著低于不含此类条件的任务，验证了这些因素是多参考生成中的关键挑战变量。

### 2. 揭示参考保真度与图像整体质量的根本权衡

MultiBanana 通过细粒度的五维评估体系（Text-Instruction Alignment、Reference Consistency、Background-Subject Match、Physical Realism、Visual Quality），系统性地揭示了一个此前未被充分量化的内在矛盾：

- **封闭模型**（如 Gemini 2.5 Flash Image、GPT-Image-1）能较好地保留所有参考对象，但往往牺牲构图连贯性和视觉质量，产生不自然的拼接感；
- **开源模型**（如 Qwen-Image-Edit、OmniGen2）倾向于保持视觉干净和谐的画面，却容易完全忽略部分参考对象。

这一权衡在背景替换任务中尤为突出：Table 3 显示，无论参考数量多少，所有模型在背景替换任务上的得分均显著低于其他任务类型。进一步的消融实验（Table 15）量化了这一矛盾：在跨域任务中，优先保证参考一致性可获得平均 4.17 分，而优先背景-主体匹配仅得 3.40 分；但后者在背景匹配子指标上反而更高（4.03 vs 3.25），显式证实了参考保真度与场景整体协调性之间的此消彼长。

### 3. 构建可扩展的 VLM 评估协议

MultiBanana 提出了一套基于 VLM（GPT-5、Gemini 2.5）的自动评估协议，从五个维度对生成图像进行 10 分制评分，并按权重 {3, 3, 1, 1, 1} 加权计算总分。该协议的可靠性得到了人类评判的验证：GPT-5 和 Gemini 2.5 与人类评分之间的 Pearson 相关系数分别达到 **0.69** 和 **0.57**（Table 4），表明 VLM 评估可作为人工评判的有效替代，为大规模基准测试提供了可复现的评测手段。

### 4. 数据构建中的分布平衡策略

针对真实数据集中于背景类图像的分布偏差，MultiBanana 在数据收集阶段引入了合成数据补充策略：利用 Nano Banana 和 GPT-Image-1 生成以人物、动物、物体等清晰主体为核心的合成图像，使数据分布更加均衡（Figure 3）。统计分析（Figure 12）表明，合成数据的引入未造成显著偏见，不同数据子集的得分保持在 99% 置信区间内，确保了基准评估的公平性。

**总结**：MultiBanana 的创新不在于提出新模型，而在于通过扩展参考数量、引入异质性组合、量化参考保真度-整体质量权衡、以及建立可复现的 VLM 评估协议，为多参考图像生成领域提供了一个细粒度的诊断工具，系统性地暴露了当前模型的能力边界与根本矛盾。

## 整体框架

MultiBanana 基准的构建与评估遵循一条系统化的流水线，旨在生成高质量、多样化的多参考图像编辑任务，并通过多维度的自动化评分实现对模型能力的细粒度诊断。该框架的核心设计目标是在可控的难度梯度下，暴露模型在参考保真度与整体图像连贯性之间的根本权衡。

### 基准构建流水线

基准的构建过程由四个顺序阶段组成（Figure 2），每个阶段均引入了自动化工具与人工校验相结合的质控机制。

**1. 真实与合成图像收集**  
为缓解真实图像数据在类别分布上的天然偏斜（例如背景类图像占主导，人物与物体类样本稀缺），流水线同时从两个来源收集参考图像：
- **真实图像**：从 LAION-5B 数据集中筛选，要求美学评分（Aesthetic score）高于 6.25 且分辨率大于 512 像素。
- **合成图像**：利用 **Nano Banana** 和 **GPT-Image-1** 在多样化条件下生成，重点补充人物、动物、物体等清晰主体的样本，使类别分布更均衡（Figure 3 左）。

**2. 图像过滤**  
收集到的图像经过多阶段自动过滤，以确保参考质量与语义一致性：
- 使用 **YOLOv12** 进行目标检测，剔除不含明确前景主体的图像。
- 使用 **SAM2** 提取分割掩码，验证主体与背景的可分离性。
- 使用 **CLIP** 计算图像与类别描述的语义相似度，过滤语义不匹配的样本。

**3. 层次化类别分类**  
通过 **Gemini** 对所有通过过滤的图像进行层次化分类，定义六大类及其子类：人物、物体、动物、背景、场景、文本。这一分类体系为后续任务构造中异质性参考组合（如跨域、不同尺度、稀有概念）提供了结构化的采样基础。

**4. 任务构造与指令生成**  
基于分类后的图像池，由 **Gemini** 自动生成编辑指令，并通过人工与自动过滤确保指令的清晰性与可执行性。最终构建的数据集包含 **3,769 个高质量参考图像与指令集**（Table 2），任务类型涵盖单参考、双参考及多参考（最高 8 参考）场景，且各参考数量下的任务分布保持均衡（Figure 4）。

### 评估框架

评估框架采用基于 VLM 的多维度自动评分机制，对生成图像进行细粒度诊断。

**评估维度与加权方案**  
每张生成图像从五个维度进行 10 分制评分，并通过加权求和得到总分：
- **文本-指令对齐**（Text-Instruction Alignment）：权重 3
- **参考一致性**（Reference Consistency）：权重 3
- **背景-主体匹配**（Background-Subject Match）：权重 1
- **物理真实性**（Physical Realism）：权重 1
- **视觉质量**（Visual Quality）：权重 1

权重分配反映了多参考生成的核心挑战：指令跟随与参考保真度被赋予最高优先级，而背景匹配、物理真实性和视觉质量作为辅助诊断指标。

**评估器选择与可靠性验证**  
主评估器采用 **Gemini 2.5** 和 **GPT-5**，两者评分与人类评判的 Pearson 相关系数分别为 0.69 和 0.57（Table 4），验证了 VLM 评估协议的有效性。此外，**Qwen3-VL** 被用作辅助评估器（Table 5、Table 6），以进一步验证评分的可复现性。

### 输入输出流

- **输入**：一组参考图像 $\{R_i\}_{i \in [I]}$（$I \in \{1, 2, \dots, 8\}$）及一条自然语言编辑指令 $P$。
- **处理**：模型需理解指令意图，从多张参考图像中提取相关视觉信息，并生成一张合成图像。
- **输出**：生成图像 $G$，接受五维度评分并汇总为加权总分，用于跨模型、跨任务类型的系统比较。

### 补充图表

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/001_Figure_1.jpg]]
*Figure 1: The overview of MultiBanana. MultiBanana broadly covers problems specific to multi-reference settings, including varying the number of references (top row), domain and scale mismatches among references (two on the left in the middle row), multilingual text rendering (center in the bottom row), and the presence of rare concepts (right in the bottom row)*

## 核心模块与公式推导

MultiBanana 基准本身不提出新的生成模型，其核心贡献在于构建了一套系统性的评估与诊断框架。该框架的关键模块并非网络结构，而是数据构建管线、任务定义、评估协议以及用于探究模型行为的 Agentic 迭代框架。

### 1. 基准构建管线

基准的构建遵循一个四阶段流水线（Figure 2），旨在生成大规模、多样化的多参考图像编辑任务：

1.  **真实与合成图像收集 (Real and Synthetic Image Collection)**：从 LAION-5B 中筛选美学评分高于 6.25 且分辨率大于 512px 的真实图像。为缓解原始数据中背景类图像过多、人物/物体类样本稀缺的分布偏差，额外使用 **Nano Banana** 和 **GPT-Image-1** 生成以清晰主体（人物、动物、物体）为核心的合成图像，以平衡数据分布。
2.  **图像过滤 (Image Filtering)**：利用 YOLOv12、SAM2 和 CLIP 进行目标检测与语义一致性验证，剔除不适宜或低质量的样本。
3.  **层次化类别分类 (Hierarchical Category Classification)**：使用 Gemini 对图像进行层次分类，定义了人物、物体、背景等六大类及其子类，为后续任务构造提供结构化的参考图像池。
4.  **任务构造与指令生成 (Task Construction and Instruction Generation)**：由 Gemini 生成编辑指令，经人工与自动过滤后，构建包含不同参考图像数量和异质性组合的多参考任务。最终数据集包含 3,769 个高质量的参考图像与指令集。

### 2. Agentic 迭代框架中的关键公式

为探究如何缓解多参考生成中的性能退化，论文引入了三种 Agentic 迭代式生成框架。这些框架的核心是生成器 (Gen) 与规划器 (Plan) 的交替迭代，其公式化定义如下：

**迭代式提示精炼 (Iterative Prompt Refinement, IPR)**
$$G^{t+1} = \text{Gen}(P^t, \{R_i\}_{i \in [I]}, \mathcal{D}), \quad P^{t+1} = \text{Plan}(P^t, \{R_i\}_{i \in [I]}, G^{t+1})$$
其中，$G^t$ 为第 $t$ 步生成的图像，$P^t$ 为第 $t$ 步的文本提示，$\{R_i\}_{i \in [I]}$ 为所有参考图像的集合，$\mathcal{D}$ 为任务指令。规划器根据当前步生成的图像 $G^{t+1}$ 来优化下一步的提示 $P^{t+1}$。

**上下文感知反馈生成 (Context-Aware Feedback Generation, CAFG)**
$$G^{t+1} = \text{Gen}(P^t, \{R_i\}_{i \in [I]}, G^t), \quad P^{t+1} = \text{Plan}(P^t, \{R_i\}_{i \in [I]}, G^{t+1})$$
与 IPR 不同的是，生成器在生成 $G^{t+1}$ 时，将上一步生成的图像 $G^t$ 作为额外的上下文条件输入，使模型能基于自身历史进行迭代修正。

**选择性参考适应 (Selective Reference Adaptation, SRA)**
$$G^{t+1} = \text{Gen}(P^t, \{R_i\}_{i \in U^t}, G^t), \quad P^{t+1}, U^{t+1} = \text{Plan}(P^t, \{R_i\}_{i \in [I]}, G^{t+1})$$
在此框架中，规划器不仅优化提示，还动态选择一个需要改善的参考图像子集 $U^t$。生成器仅使用该子集和上一步图像 $G^t$ 进行生成，实现了对特定参考对象的针对性优化。

### 3. 评估协议

评估是本基准的另一核心模块，采用基于 VLM 的多维度评分机制。所有生成图像均从五个维度进行 10 分制评估：

-   **文本-指令对齐 (Text-Instruction Alignment)**
-   **参考一致性 (Reference Consistency)**
-   **背景-主体匹配 (Background-Subject Match)**
-   **物理真实性 (Physical Realism)**
-   **视觉质量 (Visual Quality)**

最终总分由加权求和得出，权重分配为 `{3, 3, 1, 1, 1}`，分别对应上述五个维度，凸显了指令跟随与参考保真度在多参考生成任务中的核心地位。评估主要由 **Gemini 2.5** 和 **GPT-5** 执行，其与人类评判的高度相关性验证了此自动评估协议的可靠性。

## 实验与分析

### 整体趋势与瓶颈分析

MultiBanana 基准上的实验揭示了多参考图像生成中的一个根本性矛盾：**参考保真度与整体图像质量之间的固有权衡**。随着参考图像数量的增加，所有模型的总分均呈下降趋势（Figure 5），但封闭模型与开源模型的退化模式截然不同。

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/008_Figure_5.jpg]]
*Figure 5: Changes in scores for each evaluation criterion when varying the number of reference images. Both open-source and closedsource models exhibit a general trend of decreasing scores across all metrics as the number of references increases*

封闭模型（GPT-Image-1、Nano Banana）在指令对齐和参考一致性上衰减较缓，能够包含所有参考对象，但代价是构图失真和视觉质量下降。开源模型（Qwen-Image-Edit-2509、DreamOmni2、OmniGen2）则保持相对干净的视觉输出，却在多参考场景下频繁遗漏部分参考对象。这一差异在 8 参考任务中尤为显著：开源模型倾向于完全忽略某些参考主体，而封闭模型虽保留所有对象却产生不自然的场景拼接（Figure 6）。

### 各任务类型性能对比

Table 3 给出了不同任务类别下的平均得分。**背景替换任务**是所有模型的共同短板——无论参考数量多少，得分均显著低于其他任务类型。以 GPT-Image-1 为例，其背景任务得分（5.019）远低于全局编辑（6.5+）和局部编辑（6.0+）任务。这一现象在 Qwen-Image-Edit-2509 上更为极端，背景任务得分仅为 2.033，表明当前模型在将前景主体与全新背景进行语义一致且物理合理的融合方面存在严重不足。

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/007_Table_3.jpg]]
*Table 3: Average performance per model across different task categories (10-point scale; the higher the better). The average scores from Gemini 2.5 and GPT-5 are reported. Both open-source and closed-source models exhibit notably lower performance on background replacement tasks, regardless of the number of reference images*

### 异质性参考组合的挑战

MultiBanana 的核心诊断价值在于引入了**困难参考组合**（Table 2）。Figure 7 的结果表明：

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/006_Table_2.jpg]]
*Table 2: Statistics and ratios of difficult reference combinations relative to the total 3,769 tasks. Our benchmark provides sufficient samples for assessing a model’s capacity to interpret relationships among heterogeneous references and integrate them into outputs*

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/010_Figure_7.jpg]]
*Figure 7: Results for difficult reference combinations. For crossdomain and different scale and view tasks, every model shows lower scores than tasks without such conditions*

- **跨域参考**：当参考图像来自不同视觉域（如照片与插画）时，所有模型得分均显著下降。
- **尺度与视角差异**：参考图像间的尺度或视角不一致导致模型难以协调空间关系。
- **稀有概念**：模型对罕见物体或场景的参考保真度明显不足。
- **多语言文本**：多语言文本渲染任务对模型构成额外挑战。

这些异质性因素直接引发了指令跟随失败和视觉质量退化，验证了它们是当前多参考生成模型的主要瓶颈。

### 评估协议的可靠性

基于 VLM 的自动评估与人类评判高度相关。Table 4 显示，GPT-5 与人类评分的 Pearson 相关系数为 0.69，Gemini 2.5 为 0.57，验证了评估协议的可靠性。此外，Qwen3-VL 作为替代评估器的结果（Table 5、Table 6）与主评估器结论一致，进一步支持了评估框架的稳健性。

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/011_Table_4.jpg]]
*Table 4: Correlation between human and VLM judges*

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/012_Table_5.jpg]]
*Table 5: Per-task total scores for each single- and two-reference task, evaluated by Qwen3-VL. “Back.” denotes the Background task. Both open-source and closed-source models exhibit lower performance on background replacement tasks. Note that for Nano Banana and GPT-Image-1, we use the versions available as of January 2026*

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/013_Table_6.jpg]]
*Table 6: Per-task total scores for each multi-reference task, evaluated by Qwen3-VL. The local, global, back, and object columns under X correspond to X–1 Objects + Local, X–1 Objects + Global, X–1 Objects + Background, and X Object, respectively. Both open-source and closed-source models exhibit a general trend of decreasing scores across all tasks as the number of references increases. They also tend to perform worse on background replacement tasks, especially as the number of reference images increases. Note that for Nano Banana and GPT-Image-1, we use the versions available as of January 2026*

### 参考保真度与背景匹配的显式权衡

在跨域任务的子集分析中（Table 15），优先参考一致性可获得平均 4.17 分，优于优先背景-主体匹配（3.40）。然而，后者在背景匹配维度上得分更高（4.03 vs 3.25）。这一结果定量揭示了多参考生成中的显式权衡：**追求参考保真度会牺牲背景融合的自然度，反之亦然**。

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/027_Table_15.jpg]]
*Table 15: Comparison of the mean scores when prioritizing either reference consistency or background–subject match for the subset generated by Nano Banana, latest version as of January 2026*

### Agentic 框架的消融分析

在 agentic 框架的消融实验中（Section 4.5, Table 3, Appendix F.7）：

- **Iterative Prompt Refinement (IPR)** 能够提升 GPT 的性能，但对 Nano Banana 无明显提升，甚至导致部分指标退化。这表明 IPR 的有效性与基础模型的指令跟随能力高度耦合。
- 不同 agentic 策略（IPR、CAFG、SRA）的效果差异提示，多参考生成的优化路径需要针对模型特性进行定制。

### 合成数据偏见的控制

为缓解真实数据分布偏差而引入的合成数据，经统计分析确认未引入显著偏见。Figure 12 显示，不同数据子集的得分保持在 99% 置信区间内，支持了基准构建策略的合理性。

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/026_Figure_12.jpg]]
*Figure 12: Analysis of potential in-distribution bias. Error bars indicate the 99% confidence intervals. For image generation models, we use the versions available as of January 2026*

### 现有基准的饱和现象

值得注意的是，在 ImgEdit-Bench（Table 7）和 DreamOmni2 Benchmark（Table 8）上，最新的封闭模型已取得接近饱和的高分，表明这些基准在区分高端模型方面的能力正在逼近天花板。MultiBanana 通过引入多参考和异质性组合，有效弥补了这一评估缺口。

### 补充图表

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/002_Table_1.jpg]]
*Table 1: Comparison among major benchmarks for reference-based image generation. Existing benchmarks do not provide systematic evaluation across diverse multi-reference conditions, support only a limited number of references, and fail to adequately account for important factors such as differences and compatibility among reference images. Our benchmark expands the upper limit on the number of references and introduces difficult reference combinations, including domain mismatches, scale mismatches, rare concepts, and multilingual prompts, thereby explicitly addressing challenges unique to multi-reference image generation*

![[assets/figures/papers/paper_list_l2209_https_arxiv_org_abs_2511_22989/figures/004_Figure_3.jpg]]
*Figure 3: (Left) Comparison between the statistics of real data only and those after adding synthetic data. The original dataset was biased toward background images, with few person- and object-related samples. To correct this imbalance, we generated additional synthetic images using Nano Banana and GPT-Image-1, focusing on clear subjects such as people, animals, and objects. This results in a more balanced and comprehensive distribution of data. (Right) Examples of synthesized images in each category*

## 方法谱系与知识库定位

### 基准设计的谱系定位

MultiBanana 在任务定义上继承了 **DreamOmni2** (Xia et al., 2025) 的整体设计哲学，但在参考图像数量上进行了根本性扩展——将上限从典型的 1–4 张提升至 8 张。这一扩展并非简单的规模放大：当参考数量超过 4 时，模型需要在组合空间中同时维持多个对象的身份保真度、空间关系与场景连贯性，这暴露了现有方法在注意力分配和信息压缩上的根本瓶颈。

从基准对比的角度（Table 1），MultiBanana 填补了现有评测体系的两个关键空白：
1. **参考数量维度缺失**：先前基准如 **DreamOmni2**、**ImgEdit-Bench** (Ye et al., 2025)、**AnyDoor** (Chen et al., 2024) 等均将参考数量限制在 1–4 的窄范围内，无法诊断模型在参考数量扩展时的性能退化模式。
2. **异质性参考组合未被系统考察**：跨域参考（照片/绘画/渲染）、尺度与视角差异、稀有概念、多语言文本等困难组合在现有基准中几乎未被覆盖，而这些恰是真实应用中的常见场景。

### 与现有基准的差异化定位

MultiBanana 与主流参考图像生成基准的关系可概括为互补而非替代：

- **相对于 DreamOmni2**：MultiBanana 继承了其任务类型设计框架，但将参考数量从 ≤4 扩展至 8，并引入了困难参考组合的显式标注。Table 7–8 显示，当前最先进的封闭模型在 DreamOmni2 和 ImgEdit-Bench 上已接近性能天花板，而 MultiBanana 仍能有效区分模型能力——这表明 MultiBanana 提供了更高难度的诊断信号。
- **相对于 ImgEdit-Bench**：ImgEdit-Bench 侧重于单参考编辑指令的多样性，而 MultiBanana 聚焦于多参考场景下的组合挑战，两者在评测目标上正交。
- **相对于 AnyDoor 系列**：AnyDoor 等方法以单参考对象插入为核心，MultiBanana 则要求模型同时处理多个参考对象与背景的协调融合，对全局构图能力提出了更高要求。

### 方法适用边界

MultiBanana 作为评测基准，其适用边界由以下设计选择决定：

1. **静态图像生成限定**：基准仅针对静态图像生成任务，未覆盖视频生成或时序编辑中的时间一致性挑战。对于需要跨帧保持参考一致性的视频模型，本基准无法提供直接诊断。
2. **文本指令的空间歧义**：任务指令中的物体位置描述（如“左边”、“前景”）存在固有歧义。不同模型对空间指令的解释偏差可能被误判为指令跟随失败，这需要在评估中结合人工校验。
3. **无结构化布局输入**：基准未提供结构化布局（如 bounding box、分割掩码）作为输入条件，因此无法评估模型在精确空间控制下的多参考组合能力。对于依赖布局输入的生成框架（如 ControlNet 系列），本基准仅能反映其纯文本引导下的表现。
4. **合成数据的分布影响**：为平衡数据分布而引入的合成数据（Figure 3）虽经统计验证未引入显著偏见（Figure 12, 99% 置信区间），但在极端域外场景下仍可能存在轻微的分布偏移，需在结论推广时予以注意。

### 核心局限

1. **参考数量的上界未探明**：基准将参考数量上限定为 8，但模型性能已呈现持续下降趋势（Figure 5）。当参考数量进一步增加时，性能下界如何、是否存在“相变”点，仍是开放问题。
2. **评估代理的相关性边界**：VLM 评估（GPT-5、Gemini 2.5）与人类评判的 Pearson 相关系数分别为 0.69 和 0.57（Table 4），虽达到可用水平，但在细粒度属性（如物理真实性）上的判断仍可能与人类专家存在系统性偏差。Qwen3-VL 的验证（Table 5–6）提供了额外的可靠性支撑，但多评估器之间的分歧模式尚未被充分分析。
3. **失败模式的归因粒度**：基准能够揭示“封闭模型牺牲构图保对象，开源模型保持构图丢对象”的宏观权衡（Figure 6），但无法直接归因到模型架构的具体组件（如注意力机制、特征注入方式）。这限制了基准对模型改进的直接指导价值。

### 开放问题

1. **参考保真度与构图完整性的根本权衡**：Table 15 的消融实验揭示了显式的权衡——优先参考一致性时总分 4.17，优先背景-主体匹配时总分 3.40，但后者在背景匹配维度上更高（4.03 vs 3.25）。如何在不牺牲一方的前提下提升另一方，是当前多参考生成的核心挑战。

2. **异质性参考的鲁棒融合**：跨域和尺度差异任务（Figure 7）导致所有模型得分显著下降。这表明现有模型在将异质参考映射到共享表征空间时存在系统性困难。是否需要专门的域对齐模块，或通过训练策略增强跨域泛化，尚待探索。

3. **多语言文本渲染的可靠性**：多语言文本作为参考条件时，模型表现不稳定。这与文本渲染在生成模型中普遍薄弱的现状一致，但在多参考场景下，文本渲染失败会进一步破坏参考一致性，形成复合错误。

4. **Agentic 框架的有效性边界**：Iterative Prompt Refinement (IPR) 对 GPT 有效但对 Nano Banana 无显著提升甚至退化（Section 4.5），表明 agentic 策略的效果高度依赖基座模型的指令跟随和自省能力。何种模型特性是 agentic 框架生效的前提，值得系统研究。

5. **超越 8 参考的扩展性**：当参考数量继续增加时，模型是否会从“部分遗漏”退化为“完全崩溃”？是否存在有效的参考选择或压缩策略，使模型在大量参考下仍能维持可接受的性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/MultiBanana_A_Challenging_Benchmark_for_Multi_Reference_Text_to_Image_Generation.pdf]]
