---
title: Towards Real-World Document Parsing via Realistic Scene Synthesis and Document-Aware Training
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Real_World_Document_Parsing_via_Realistic_Scene_Synthesis_and_Document_Aware_Training.pdf
project_link: null
code_link: "https://github.com/datalabto/marker"
aliases:
- RSSDATDM
- TRWDPRSSDAT
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 数据与训练的协同设计框架，即真实场景合成（RSS）生成多样化合成数据，结合文档感知训练策略（渐进式学习PTP与结构标记优化ST），是提升鲁棒性的关键。
primary_logic: 通过合成大规模、包含真实世界变异且结构多样化的页面级数据，并采用先学习孤立元素再过渡到整页理解的渐进式课程，同时强调结构标记的损失加权，可以显著提高端到端模型在真实文档上的鲁棒性、解析精度和抗重复能力。
claims:
- 在 OmniDocBench 上，DocHumming (RSS+ST+PTP) 的 Overall 达到 93.75，超过最强基线 PaddleOCR-VL 的 91.93。
- 在 Wild-OmniDocBench 上，DocHumming 的 Overall 为 87.03，性能退化仅 -6.72，远低于级联方法如 MinerU2.5 的 -19.76。
- 消融实验显示，移除结构标记优化 (ST) 导致 OmniDocBench Overall 下降 5.01，重复率从 2.1 升至 4.6。
- 移除渐进式训练 (PTP) 导致 Overall 下降 2.51，重复率从 2.1 升至 4.2。
---

# Towards Real-World Document Parsing via Realistic Scene Synthesis and Document-Aware Training

> [!tip] 核心洞察
> 通过合成大规模、包含真实世界变异且结构多样化的页面级数据，并采用先学习孤立元素再过渡到整页理解的渐进式课程，同时强调结构标记的损失加权，可以显著提高端到端模型在真实文档上的鲁棒性、解析精度和抗重复能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向真实世界的文档解析：通过真实场景合成与文档感知训练 |
| 英文题名 | Towards Real-World Document Parsing via Realistic Scene Synthesis and Document-Aware Training |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.23885) · [Code](https://github.com/datalabto/marker) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Realistic Scene Synthesis + Document-Aware Training (DocHumming model) |
| Dataset | OmniDocBench, XFUND, Wild-OmniDocBench |

> [!tip] 效果简介
> - OmniDocBench 上，Overall ↑ 93.75 vs 91.93 (+1.82)；Text Edit ↓ 0.035 vs 0.039 (-0.004)；Formula CDM ↑ 93.27 vs 88.67 (+4.60)。
> - XFUND 上，Per-language scores (de/it/ja/es/pt/fr) 85.15 / 80.06 / 87.99 / 84.39 / 83.67 / 77.48。
> - Wild-OmniDocBench 上，Overall (OmniDocBench / Wild-OmniDocBench) 87.03。

## 概要

**核心瓶颈**：端到端文档解析面临大规模高质量全页数据的稀缺，以及缺乏结构感知训练策略的挑战。现有模型在真实世界场景下容易产生重复输出、幻觉内容和结构不一致的解析结果。

**方法定位**：本文提出数据与训练的协同设计框架——**真实场景合成（Realistic Scene Synthesis, RSS）** 与**文档感知训练（Document-Aware Training）**，集成于 1B 参数的多模态大语言模型 DocHumming 中。RSS 通过组合多样化的布局模板与文档元素，生成大规模、结构多样的全页监督数据；训练侧则采用渐进式学习策略（Progressive Training Paradigm, PTP）与结构标记优化（Structure-Token aware optimization, ST），先学习孤立元素再过渡到整页理解，并对结构标记施加更高损失权重以稳定解码。

**核心结论**：在 OmniDocBench 基准上，DocHumming 以 93.75 的 Overall 分数超越最强基线 **PaddleOCR-VL**（Cui et al., 2025）的 91.93；在真实世界捕获场景的 Wild-OmniDocBench 上，性能退化仅 -6.72，远低于级联方法如 **MinerU2.5**（Niu et al., 2025）的 -19.76。消融实验表明，移除 ST 导致 Overall 下降 5.01 且重复率从 2.1 升至 4.6，移除 PTP 则导致 Overall 下降 2.51 且重复率升至 4.2，验证了训练策略的关键作用。

**方法谱系与知识库定位**：DocHumming 属于端到端文档解析方法，与级联式模块化方法（如 PaddleOCR-VL、MinerU2.5）和通用大模型（如 **Qwen3-VL-235B**, Qwen Team, 2025）形成对比。其核心贡献在于通过合成数据与结构感知训练解决真实场景鲁棒性问题，而非依赖更大规模模型或人工标注数据。

### 文档解析的现实瓶颈

将文档图像转化为结构化、可编辑的机器可读表示，是智能文档处理的核心任务。然而，端到端文档解析系统长期受困于一个根本性矛盾：**大规模高质量全页标注数据的稀缺**与**真实世界场景的复杂性**之间的错配。现有数据要么来自数字-born 的 PDF 转换，缺乏真实捕获中的几何畸变、光照变化和摩尔纹；要么依赖昂贵的人工标注，规模有限且布局多样性不足。这一数据瓶颈直接导致模型在真实场景下产生三类典型失效——**重复生成**、**幻觉内容**和**结构不一致**，严重制约了端到端方法的实际部署。

### 级联与端到端方法的结构性缺陷

当前主流方案分为两条技术路线，各自存在系统性弱点。

**模块化级联流水线**（如 PaddleOCR-VL、MinerU2.5）将解析拆解为版面分析、元素检测、内容识别等多个独立阶段。在干净的扫描/数字文档上，这种分工能取得高精度；但在真实世界捕获场景下，前端版面分析的误差会沿流水线逐级放大，导致元素区域错位或遗漏（见 Figure 2）。从 OmniDocBench 到 Wild-OmniDocBench 的性能退化幅度揭示了这一脆弱性：级联方法 MinerU2.5 的 Overall 下降达 -19.76，而本文提出的端到端方法 DocHumming 仅下降 -6.72（Table 3）。

**通用端到端多模态大语言模型**（如 Qwen3-VL-235B）虽避免了级联误差累积，却面临另一困境：缺乏针对文档结构感知的训练策略。标准自回归微调对所有标记赋予统一权重，模型难以区分内容标记与结构标记（如 `<table>`、`<tr>`）的重要性差异，导致长序列解码时结构边界模糊，表现为重复输出和阅读顺序混乱（Figure 2）。

### 本文动机：数据与训练的协同设计

上述分析揭示了一个关键洞察：**数据质量与训练策略并非独立变量，而是相互制约的耦合瓶颈**。单纯扩充数据规模而不改变训练方式，无法根治结构不一致；仅优化训练策略而缺乏多样化真实场景数据，则难以泛化到野外捕获图像。

基于此，本文提出一种**数据-训练协同设计框架**，核心思路是：

1. **真实场景合成（Realistic Scene Synthesis, RSS）**：通过组合元素库与布局模板，自动生成大规模、结构多样且包含真实世界变异的页面级监督数据，从根本上解决数据稀缺与场景覆盖不足的问题。
2. **文档感知训练策略（Document-Aware Training）**：包含渐进式学习范式（Progressive Training Paradigm, PTP）与结构标记感知优化（Structure-Token Aware Optimization, ST），前者从孤立元素逐步过渡到整页理解以稳定优化过程，后者通过对结构标记施加更高损失权重来强化结构化输出的稳定性。

这一框架集成于 1B 参数的 MLLM（DocHumming），在 OmniDocBench 上取得 93.75 Overall，超过最强基线 PaddleOCR-VL 的 91.93（Table 1），并在真实世界鲁棒性测试中展现出显著优势。

## 核心方法与创新机理

本文的核心贡献并非提出全新的模型架构，而是在**数据构造**与**训练策略**两个维度上进行了协同设计，系统性地解决了端到端文档解析面临的三大瓶颈：大规模高质量全页监督数据稀缺、结构感知训练策略缺失、以及真实世界场景下的鲁棒性不足。

### 创新一：真实场景合成——从元素组合到全页监督

传统文档解析的数据来源主要依赖有限的人工标注或数字-born PDF 转换，难以覆盖真实世界捕获场景中的几何变形、光照变化和相机噪声。本文提出 **Realistic Scene Synthesis (RSS)** 策略，将数据构造抽象为三个层次的可控组合：

1. **元素仓库构建**：整合表格、公式、段落等细粒度文档元素，进行格式规范化与增强，渲染为带标注的图像块。
2. **布局模板库构建**：收集并生成超过 576K 个包含阅读顺序的布局模板，覆盖多样化的页面结构。
3. **数据增强**：在合成过程中模拟几何、光度、相机和环境变化，缩小合成数据与真实捕获图像之间的分布差距。

通过将元素与模板在空间和结构约束下组合，RSS 生成了约 3M 规模的 **DocMix-3M** 数据集，为端到端模型提供了结构多样且包含真实世界变异的页面级监督。消融实验表明，DocMix-3M 合成数据在 OmniDocBench 和 Wild-OmniDocBench 上均优于纯人工标注数据，且将重复率从 5.4 降至 3.8（Table 5），验证了合成数据在覆盖真实场景退化方面的独特价值。

### 创新二：文档感知训练——渐进式课程与结构标记优化

仅有数据不足以解决端到端解析中的重复生成和结构不一致问题。本文提出 **Document-Aware Training Recipe**，包含两个互补的训练策略：

**渐进式训练范式** 将学习过程分为两个阶段：
- **Stage 1（元素级解析）**：使用异构提示训练模型解析单个元素（表格、公式、段落等），并在此阶段扩展布局特定的结构标记（如 `<table>`、`<tr>`），让模型先建立对孤立元素的精确理解。
- **Stage 2（全页解析）**：使用统一提示在 DocMix-3M 和部分真实文档上联合训练整页解析，将元素级能力迁移到页面级上下文理解。

这种“先局部后全局”的课程设计稳定了优化过程，提升了长上下文一致性。消融实验显示，移除 PTP（将两阶段合并为端到端训练）导致 OmniDocBench Overall 下降 2.51，重复率从 2.1 升至 4.2（Table 4）。

**结构标记感知优化** 在损失函数层面强调结构标记的重要性。标准自回归训练对所有标记赋予统一权重，忽略了结构标记（如标签对）对输出格式一致性的关键作用。本文引入加权交叉熵损失：

$$L_{\mathrm{structured}} = - \sum_{t=1}^{T} \alpha_{t} y_{t} \log P(x_{t} | \boldsymbol x_{<t})$$

其中权重 $\alpha_{t}$ 定义为：

$$\alpha_{t} = \begin{cases} \lambda, & \text{if } x_{t} \text{ is a structured token} \\ 1, & \text{otherwise} \end{cases}$$

对结构标记赋予更高权重 $\lambda$，其余标记权重为 1。这一简单而有效的设计显著稳定了解码过程：移除 ST 导致 OmniDocBench Overall 下降 5.01，重复率从 2.1 升至 4.6（Table 4），是消融实验中影响最大的单一组件。

### 创新三：鲁棒性导向的评估基准

为量化真实世界场景下的性能退化，本文构建了 **Wild-OmniDocBench**，通过打印、物理变形、不同光照下拍摄以及屏幕重拍引入摩尔纹和反射等真实退化。该基准揭示了级联方法（如 **MinerU2.5**，Niu et al., 2025）在真实场景中的严重性能衰减（退化达 -19.76），而端到端的 DocHumming 退化仅为 -6.72（Table 3），证明了数据-训练协同设计在鲁棒性上的实质性收益。

### 与 baseline 的关键差异总结

| 维度 | 现有方法 | 本文方法 (DocHumming) |
|------|---------|---------------------|
| 训练数据 | 有限人工标注或数字-born 数据 | 大规模合成 DocMix-3M，包含真实世界变异 |
| 训练策略 | 标准自回归监督微调，统一权重 | 两阶段渐进式训练 + 结构标记感知加权 loss |
| 结构标记 | 无特定结构标记 | 引入布局特定标记（`<table>`, `<tr>` 等） |

这些创新使仅 1B 参数的 DocHumming 在 OmniDocBench 上达到 93.75 Overall，超过最强基线 **PaddleOCR-VL**（Cui et al., 2025）的 91.93，并在公式解析（Formula CDM 93.27 vs 88.67）等细粒度指标上展现出显著优势。

### 核心瓶颈与设计动机

端到端文档解析面临两个根本性挑战：一是大规模、高质量的全页监督数据极度稀缺，现有的数字-born 或人工标注数据无法覆盖真实世界捕获场景中的几何畸变、光照变化和结构多样性；二是缺乏结构感知的训练策略，导致模型在长序列解码中产生重复生成、幻觉内容和结构不一致的输出。针对这两大瓶颈，本文提出了一种数据与训练协同设计的框架，核心思路是：**通过真实场景合成（Realistic Scene Synthesis, RSS）构建大规模、结构多样化的页面级监督数据，并配合文档感知训练策略（渐进式学习与结构标记优化），从数据和优化两个维度共同提升端到端模型的鲁棒性。**

### 整体流水线架构

整个框架由两个协同模块构成：**真实场景合成流水线**负责数据生产，**文档感知训练范式**负责模型优化，二者共同作用于一个 1B 参数的多模态大语言模型（以 InternVL2-1B 为基座），最终得到文档解析模型 DocHumming。

**数据生产端（RSS 流水线）** 包含三个核心组件：

1. **元素仓库构建（Element Repository Construction）**：整合表格、公式、段落等文档原子元素的数据集，进行格式规范化与增强，渲染为带标注的图像元素。该仓库为后续页面合成提供了丰富的细粒度构建块。

2. **布局模板库构建（Layout Library Construction）**：收集并生成超过 576K 个包含阅读顺序标注的布局模板，覆盖多样化的页面结构，确保合成数据在空间组织上的多样性。

3. **数据增强（Data Augmentation）**：在页面合成完成后，施加几何变换、光度变化、相机畸变和环境噪声等真实世界退化模拟，缩小合成图像与真实捕获图像之间的域差距。

合成流程将元素仓库中的原子元素按布局模板进行空间组合，在空间与结构约束下生成完整的页面级标注，再经过增强处理，最终产出 **DocMix-3M 数据集**（约 3M 张合成页面图像），为端到端训练提供大规模、结构多样化的监督信号。

**模型训练端（文档感知训练范式）** 包含两个关键策略：

1. **渐进式训练范式（Progressive Training Paradigm, PTP）**：采用两阶段课程学习。第一阶段在约 9M 个原子元素上训练模型解析单个元素（表格、公式、段落等），使用异构提示扩展结构标记词汇；第二阶段过渡到 DocMix-3M 及部分真实文档上的全页联合训练，使用统一提示。这种“先局部后全局”的课程设计使模型先掌握孤立元素的解析能力，再学习整页级别的结构关系，有效稳定了长序列优化过程。

2. **结构标记感知优化（Structure-Token Aware Optimization, ST）**：在自回归解码的交叉熵损失中，对结构化输出中的结构标记（如 `<table>`、`</table>`、`<tr>` 等）赋予更高的损失权重 $\lambda$，而对普通文本标记保持权重 1。其加权损失函数为：

$$L_{\mathrm{structured}} = - \sum_{t=1}^{T} \alpha_{t} y_{t} \log P(x_{t} | \boldsymbol x_{<t})$$

其中权重 $\alpha_t$ 定义为：

$$\alpha_{t} = \begin{cases} \lambda, & \text{if } x_{t} \text{ is a structured token} \\ 1, & \text{otherwise} \end{cases}$$

这一设计强化了模型对结构边界的感知，显著抑制了解码过程中的重复生成——消融实验表明，移除 ST 会导致 OmniDocBench 上重复率从 2.1 升至 4.6，Overall 下降 5.01。

### 输入输出流

模型的输入为单页文档图像（支持扫描件、数字-born 文档及真实世界拍摄图像），输出为结构化的 Markdown 格式文本，包含完整的阅读顺序、表格结构、公式 LaTeX 表示和段落组织。整个流水线无需级联的布局分析或元素检测模块，实现了从像素到结构化标记序列的端到端映射。

### 补充图表

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Realistic Scene Synthesis. Left: repositories of atomic elements and layout templates with reading order. Right: a synthesis pipeline that composes sampled elements into templates under spatial/structural constraints to produce page-level annotations, followed by capture-aware augmentation to simulate real-world images*

### 3.1 方法总览

DocHumming 的核心架构围绕两个协同设计的模块展开：**真实场景合成（Realistic Scene Synthesis, RSS）** 与 **文档感知训练策略（Document-Aware Training Recipe）**。前者负责构建大规模、结构多样、覆盖真实世界变异的合成数据 DocMix-3M；后者通过渐进式训练范式（Progressive Training Paradigm, PTP）和结构标记感知优化（Structure-Token Aware Optimization, ST）来引导模型从元素级解析逐步过渡到整页理解，并强化结构化输出的解码稳定性。

### 3.2 真实场景合成流水线

RSS 流水线由三个子模块串联构成，其设计目标是从原子元素和布局模板出发，合成具有完整页面级标注和真实世界退化的训练图像。

**元素仓库构建（Element Repository Construction）**。该模块整合表格、公式、段落、标题等细粒度文档元素数据集，进行格式规范化与增强，并将每个元素渲染为带标注的图像。元素仓库为后续合成提供了丰富的原子构建块。

**布局模板库构建（Layout Library Construction）**。该模块收集并生成超过 576K 个包含阅读顺序的布局模板，定义了页面上各区域的空间位置、尺寸和先后关系。布局的多样性直接决定了合成页面在版式上的泛化能力。

**数据增强（Data Augmentation）**。在将元素按布局模板组合成完整页面后，施加几何变换（透视、弯曲）、光度变化（亮度、对比度）、相机模拟（噪声、模糊）和环境效果（阴影、反光），以缩小合成数据与真实拍摄场景之间的域差距。这一增强策略是模型在 Wild-OmniDocBench 上保持鲁棒性的关键——DocHumming 在该基准上的性能退化仅为 −6.72，远低于级联方法 MinerU2.5 的 −19.76（见 Table 3）。

### 3.3 渐进式训练范式

PTP 将训练过程解耦为两个阶段，形成从局部到全局的课程学习路径。

**阶段一：元素级解析训练。** 模型在约 900 万原子元素上训练，使用异构提示（heterogeneous prompts）引导模型解析单个元素（表格、公式、段落等）。此阶段同时扩展模型的词表，引入布局特定的结构标记，如 `<table>`、`<tr>`、`<td>` 等，使模型具备输出结构化标记序列的能力。

**阶段二：整页文档解析训练。** 以 DocMix-3M 为主要语料，辅以部分真实文档数据，使用统一的整页解析提示进行联合训练。此阶段模型学习在完整页面上下文中定位、识别并按阅读顺序输出所有元素的结构化表示。

消融实验（Table 4）表明，移除 PTP（即将两阶段数据合并为一阶段端到端训练）会导致 OmniDocBench Overall 下降 2.51，重复率从 2.1 升至 4.2，验证了渐进式课程对稳定长序列解码和抑制重复生成的作用。

### 3.4 结构标记感知优化

传统自回归训练对所有标记施加均匀的交叉熵损失，但在结构化输出中，结构标记（如 `<table>`、`</table>`、`<tr>` 等）对最终解析结果的格式正确性影响远大于普通文本标记。ST 策略通过加权损失函数显式强调这些关键标记。

结构化损失定义为加权交叉熵：

$$L_{\mathrm{structured}} = - \sum_{t=1}^{T} \alpha_{t} y_{t} \log P(x_{t} | \boldsymbol x_{<t})$$

其中，$T$ 为序列长度，$y_t$ 为真实标记的独热编码，$P(x_t | \boldsymbol x_{<t})$ 为模型在位置 $t$ 的预测概率。权重 $\alpha_t$ 根据当前标记类型动态分配：

$$\alpha_{t} = \begin{cases} \lambda, & \text{if } x_{t} \text{ is a structured token} \\ 1, & \text{otherwise} \end{cases}$$

当 $x_t$ 为结构标记时，其损失权重放大为 $\lambda$（$\lambda > 1$），其余标记保持权重 1。这一机制迫使模型在训练过程中对结构边界的预测投入更多优化资源，从而在推理时更稳定地生成正确的标记对，减少结构错位和重复生成。

消融实验（Table 4）提供了强有力的因果证据：在保持 RSS 和 PTP 不变的前提下，移除 ST 导致 OmniDocBench Overall 骤降 5.01，重复率从 2.1 飙升至 4.6。这表明结构标记的损失加权不仅影响格式正确性，还通过稳定解码路径显著抑制了重复输出这一端到端模型的常见失败模式。

### 3.5 模块间协同效应

Table 4 的完整消融揭示了三个模块的协同关系。仅使用 RSS 而不施加 ST 和 PTP（配置 #1）时，OmniDocBench Overall 为 88.74，重复率为 5.1。逐步加入 ST（配置 #2）和 PTP（配置 #4）后，Overall 分别提升至 91.24 和 93.75，重复率降至 3.2 和 2.1。三者共同作用时达到最佳的精度-稳定性平衡，说明数据合成提供了多样化的训练信号，而 PTP 和 ST 分别从课程难度和损失加权两个维度引导模型有效利用这些信号。

### 补充图表

## 实验与关键发现

### 主结果：OmniDocBench 基准

DocHumming 在 OmniDocBench 基准上取得了 **93.75** 的 Overall 分数，超越了此前最强的专用 MLLM 基线 **PaddleOCR-VL**（Cui et al., 2025）的 91.93（+1.82），如 Table 1 所示。这一优势在多个细粒度指标上均有体现：Text Edit 降至 0.035（PaddleOCR-VL 为 0.039），Formula CDM 达到 93.27（PaddleOCR-VL 为 88.67，提升 +4.60），Table TEDS 为 91.49（PaddleOCR-VL 为 91.01），Reading Order Edit 为 0.041（PaddleOCR-VL 为 0.043）。

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/005_Table_1.jpg]]
*Table 1: Comparison of various OCR and VLM systems on document understanding benchmarks. Higher ↑ indicates better performance, lower ↓ indicates smaller error*

值得注意的是，DocHumming 的模型参数量仅为 **1B**，而部分对比方法规模远超于此——例如 **Qwen3-VL-235B**（Qwen Team, 2025）和 **InternVL3.5-241B**，但 DocHumming 在 Overall 指标上仍显著优于这些通用大模型。这表明数据与训练策略的协同设计可以在极小参数量下实现高精度文档解析，而非单纯依赖模型规模扩展。

在 XFUND 多语言文档解析任务上，DocHumming 展现出跨语言的鲁棒性，各语言得分分别为：德语 85.15、意大利语 80.06、日语 87.99、西班牙语 84.39、葡萄牙语 83.67、法语 77.48（Table 2），验证了合成数据与训练策略对多脚本场景的覆盖能力。

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/006_Table_2.jpg]]
*Table 2: Performance comparison on the XFUND*

### 真实世界鲁棒性：Wild-OmniDocBench

为评估在真实世界捕获场景下的鲁棒性，作者构建了 Wild-OmniDocBench 基准（Figure 4），通过打印、物理变形、不同光照拍摄以及屏幕重拍引入摩尔纹和反射等退化。Table 3 显示，DocHumming 在 Wild-OmniDocBench 上的 Overall 为 **87.03**，性能退化仅为 **−6.72**。相比之下，级联方法 **MinerU2.5**（Niu et al., 2025）的退化高达 **−19.76**，PaddleOCR-VL 同样出现显著下降。

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/007_Table_3.jpg]]
*Table 3: Performance comparison on the Wild-OmniDocBench*

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/004_Figure_4.jpg]]
*Figure 4: Wild-OmniDocBench Construction. We convert scanned pages into real-world–captured images by (i) printing, deforming, and photographing under varied lighting, and (ii) displaying on screens and re-shooting to induce moire and reflections. ´*

这一现象的根本原因在于级联流水线在真实世界捕获场景中会累积布局分析错误并传播至元素解析阶段（如 Figure 2 所示），而 DocHumming 作为端到端模型，通过真实场景合成（RSS）数据训练获得了对光照变化、几何变形等真实世界变异的鲁棒性。

### 消融实验：各组件的因果贡献

Table 4 的消融实验揭示了三个核心组件的独立贡献：

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/008_Table_4.jpg]]
*Table 4: Extended ablation study on Realistic Scene Synthesis. and Document-Aware Training Recipe*

**结构标记优化（ST）** 是最关键的组件。在保持 RSS 和 PTP 不变的情况下移除 ST，OmniDocBench Overall 从 93.75 骤降至 88.74（**−5.01**），Wild-OmniDocBench Overall 从 87.03 降至 84.90（−2.13），且重复率从 2.1 升至 4.6。这证实了结构标记感知的加权损失函数（公式 $L_{\mathrm{structured}} = - \sum_{t=1}^{T} \alpha_{t} y_{t} \log P(x_{t} | \boldsymbol x_{<t})$，其中 $\alpha_{t} = \lambda$ 当 $x_t$ 为结构标记）对稳定解码和抑制重复输出的关键作用。

**渐进式训练范式（PTP）** 同样贡献显著。将两阶段课程合并为单阶段端到端训练（保持 RSS 和 ST 不变），Overall 下降 2.51（OmniDocBench），重复率从 2.1 升至 4.2。这表明先从孤立元素学习再过渡到整页理解的课程设计，有效稳定了长上下文优化并提升了结构一致性。

结合 RSS、ST 和 PTP 的完整方案（#4）在精度-稳定性权衡上达到最优：OmniDocBench 93.75 / 重复率 2.1，Wild-OmniDocBench 87.03 / 重复率 4.3。

### 数据规模与来源的影响

Table 5 的扩展消融显示，**DocMix-3M 合成数据**在 OmniDocBench 和 Wild-OmniDocBench 上均优于纯人工标注数据：OmniDocBench Overall 89.96 vs. 89.26，重复率 3.8 vs. 5.4；Wild-OmniDocBench Overall 83.21 vs. 80.20，重复率 4.8 vs. 7.8。合成数据在抑制重复输出方面的优势尤为明显。

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/009_Table_5.jpg]]
*Table 5: Extended ablation study on Realistic Scene Synthesis. and Document-Aware Training Recipe*

数据规模方面，从 1M 增至 3M 带来显著收益，但在 3M 后趋于饱和，表明当前合成策略在数据多样性覆盖上已接近边际收益递减点。

### 失败模式与局限

尽管整体表现优异，该方法仍存在以下已知局限：

1. **极端不规则布局**：在布局极不规则、图文交错（如报纸、海报）且阅读顺序模糊的文档上，模型可能难以泛化，结构边界和阅读顺序的一致性无法保证。
2. **超高分辨率处理**：模型仅训练于固定分辨率，对超高分辨率文档直接缩放或分块处理可能引入伪影，细节保持能力受限。
3. **推理延迟**：约 3 秒每页的推理延迟限制了交互式或高吞吐量场景的应用。
4. **重复率指标的鲁棒性**：当前重复率指标在处理部分重复或近重复输出时是否足够鲁棒，仍需进一步验证（需人工核实具体计算方式）。

### 补充图表

![[assets/figures/papers/paper_list_l2611_https_arxiv_org_abs_2603_23885/figures/001_Figure_1.jpg]]
*Figure 1: Overall Performance and Degradation from OmniDocBench to Wild-OmniDocBench. Underlined method names correspond to modular cascaded pipelines*

## 定位与知识库关联

### 核心瓶颈与设计哲学

端到端文档解析面临的核心瓶颈是**大规模高质量全页数据的稀缺**与**缺乏结构感知训练策略**。现有方法大致分为两类：模块化级联流水线（如 PaddleOCR-VL、MinerU2.5）在干净扫描文档上表现强劲，但在真实世界捕获场景（光照变化、透视畸变、摩尔纹等）下因布局分析误差累积而导致性能急剧退化（Figure 2）；通用大语言多模态模型（如 Qwen3-VL-235B）虽然具备端到端能力，却容易产生重复输出和结构幻觉。DocHumming 通过**数据与训练的协同设计**——真实场景合成（RSS）与文档感知训练（文档感知训练策略，包含渐进式学习 PTP 与结构标记优化 ST）——同时解决了数据稀缺和训练策略缺失两个问题，在 1B 参数规模下实现了超越更大模型的鲁棒性。

### 与基线工作的关系

DocHumming 在 OmniDocBench 上以 Overall 93.75 超过最强基线 **PaddleOCR-VL**（Cui et al., 2025）的 91.91（Table 1），且在公式解析（Formula CDM 93.27 vs. 88.67）和表格解析（Table TEDS 91.49 vs. 91.01）等元素级指标上均占优。在 Wild-OmniDocBench 的真实世界退化场景中，DocHumming 的 Overall 为 87.03，性能退化仅 −6.72，远低于级联方法 **MinerU2.5**（Niu et al., 2025）的 −19.76（Table 3），验证了端到端架构在鲁棒性上的根本优势。与 **MonkeyOCR-pro-3B**（Li et al., 2025）等专用 MLLM 相比，DocHumming 在更小模型规模下实现了更优或可比性能，凸显了合成数据与训练策略的增效作用。

### 方法谱系定位

DocHumming 处于**端到端文档解析**与**合成数据驱动训练**的交叉点。其数据合成流水线（RSS）将元素库（表格、公式、段落等）与超过 576K 个布局模板组合，并通过几何、光度、相机和环境增强模拟真实世界变异，生成 DocMix-3M 数据集（约 3M 图像）。训练策略上，两阶段渐进式课程（PTP）先让模型学习孤立元素解析并扩展结构标记（`<table>`、`<tr>` 等），再过渡到整页理解，配合对结构标记施加加权损失（ST，权重 λ）以稳定解码。这一框架在方法论上区别于纯数据驱动或纯训练策略驱动的路线，强调两者协同。

### 适用边界与局限

1. **布局泛化边界**：当前方法在布局极不规则、图文交错（如报纸、海报）且阅读顺序模糊的文档上可能难以泛化，合成数据的布局模板库可能未充分覆盖此类极端情况。
2. **分辨率限制**：模型仅训练于固定分辨率，对超高分辨率文档的直接缩放或分块处理可能引入伪影，影响细粒度元素（如小字体、密集表格）的解析精度。
3. **推理延迟**：每页约 3 秒的推理延迟限制了交互式或高吞吐量场景的应用，需要进一步优化。
4. **重复率指标的鲁棒性**：消融实验显示移除 ST 后重复率从 2.1 升至 4.6（Table 4），但该指标在处理部分重复或近重复输出时的判别力尚需验证。

### 开放问题

- 如何处理极端不规则布局并确保结构边界和阅读顺序的一致性？
- 如何在不依赖分块或下采样的前提下处理超高分辨率图像以保持细节？
- 如何进一步降低推理延迟，使模型更适合实时交互使用？
- 所提出的数据合成方法在多语言、多脚本场景下的覆盖度和质量如何进一步提升？
- 重复率指标在处理部分重复或近重复输出时是否足够鲁棒？

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Real_World_Document_Parsing_via_Realistic_Scene_Synthesis_and_Document_Aware_Training.pdf]]
