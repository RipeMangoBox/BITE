---
title: "Paper2Figure: A Multi-Agent Collaborative System for Figure Generation Towards Academic Research Paper"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Paper2Figure_A_Multi_Agent_Collaborative_System_for_Figure_Generation_Towards_Academic_Research_Paper.pdf
project_link: null
code_link: null
aliases:
- Paper2Figure
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入中间结构化表示语言 FigScript 以及双多智能体协作流水线（生成代理和细化代理），将语义理解、布局规划、视觉细化和迭代修正分离为专门的代理角色，并通过结构化的 FigScript 进行通信和编辑。
primary_logic: 通过分解生成和细化过程，并利用结构化中间语言，可以在不牺牲编辑灵活性的情况下，结合代码生成的精确控制与迭代视觉优化，从而实现学术图表的高保真度和美观性。
claims:
- Paper2Figure 在准确性上提升 12%，美观度提升 13.5%，完整性提升 17.0%，全面超越现有最强基线。
- 完整的 Paper2Figure 系统（包含生成和细化代理）在 Paper2Figure Bench 上取得 79.2% 的整体平均分，比最强基线整体高出 14.1%。
- Paper2Figure 提出的评估指标与人类判断具有最高相关性（Pearson r = 0.7345，Cosine similarity = 0.8652），验证了自动评估的可靠性。
- Paper2Figure Bench 上 Overall Score = 79.2
---

# Paper2Figure: A Multi-Agent Collaborative System for Figure Generation Towards Academic Research Paper

> [!tip] 核心洞察
> 通过分解生成和细化过程，并利用结构化中间语言，可以在不牺牲编辑灵活性的情况下，结合代码生成的精确控制与迭代视觉优化，从而实现学术图表的高保真度和美观性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Paper2Figure：面向学术研究论文的图生成多智能体协作系统 |
| 英文题名 | Paper2Figure: A Multi-Agent Collaborative System for Figure Generation Towards Academic Research Paper |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Han_Paper2Figure_A_Multi-Agent_Collaborative_System_for_Figure_Generation_Towards_Academic_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Paper2Figure |
| Dataset | Paper2Figure Bench, Human correlation |

> [!tip] 效果简介
> - Paper2Figure Bench 上，Overall Score 79.2 vs ~65.1 (strongest baseline) (+14.1%)；Accuracy — vs — (+12%)；Beauty — vs — (+13.5%)。
> - Human correlation (Paper2Figure Bench) 上，Pearson r 0.7345 vs — (—)；Cosine similarity 0.8652 vs — (—)。

## 概要

学术论文中的图表是传递复杂研究思想的核心载体，但高质量图表的制作长期依赖人工绘制，耗时且专业门槛高。现有自动化方法陷入两难困境：基于代码生成的方式（如 SVG、Mermaid）虽能保证结构正确性，但输出布局杂乱、视觉僵硬；直接图像生成模型（如 **GPT-Image-1**，OpenAI 2025）虽视觉丰富，却普遍存在文本渲染错误、逻辑关系混乱且难以编辑的问题。**根本瓶颈在于，现有方法无法同时兼顾语义精度、视觉质量与灵活的结构控制。**

Paper2Figure 针对这一瓶颈，提出**双多智能体协作系统**，核心思路是引入结构化中间表示语言 **FigScript**，将图表生成分解为语义理解、布局规划、视觉细化与迭代修正四个独立阶段，分别由专门的生成代理（Generation Agents）与细化代理（Refinement Agents）承担。生成代理负责从文本描述中抽取实体与逻辑关系，构造 FigScript 视觉模块并优化布局；细化代理则通过“视觉检查—问题定位—修订执行”的闭环迭代，持续提升图表的逻辑清晰度与视觉和谐度。这一设计的关键洞见在于：通过结构化中间语言的桥接，系统得以结合代码生成的精确控制与迭代视觉优化的灵活性，在不牺牲可编辑性的前提下实现学术图表的高保真与美观性。

在自建的 **Paper2Figure Bench**（从约 500 篇 arXiv 论文中筛选 100 张代表性图表并经人工标注）上，完整版 Paper2Figure 取得 **79.2%** 的整体平均分，较最强基线提升 **14.1%**，且在准确性（+12%）、美观度（+13.5%）和完整性（+17.0%）三个维度全面领先。所提出的自动化评估指标与人类判断达到最高相关性（Pearson r = 0.7345，Cosine similarity = 0.8652），验证了评估体系的可靠性。系统还提供交互式 Web 编辑器，支持自然语言指令与直接画布操作，实现自动化生成与人工微调的无缝衔接。

![Figure 1]()

*图 1：Paper2Figure 框架概览，对比传统代码方法与本文双多智能体系统及交互式编辑器*

学术论文中的图表是传达复杂研究思想的核心媒介。高质量的图表能够将抽象的方法流程、模型架构和实验结果转化为直观的视觉表达，直接决定读者对论文的第一印象和理解效率。然而，对于大多数研究者而言，创建专业级图表是一项耗时且依赖设计经验的繁重任务。

近年来，大语言模型（LLM）的快速发展为自动化图表生成带来了新的可能。现有方法大致可归为两条技术路线：**基于代码生成**的方法和**直接图像生成**的方法。基于代码生成的路线利用 LLM 输出 SVG 或 Mermaid 等标记语言来构建图表。SVG 类方法（如 **GPT-5**、**Claude Opus 4**、**Gemini 2.5 Pro**）能够保留详细的文本信息，但普遍存在元素重叠、布局松散等问题；Mermaid 类方法（如 **GPT-5 (Mermaid)**、**Claude 4.5 Sonnet (Mermaid)**）则受限于僵化的模板布局，美学表现力不足。直接图像生成路线（如 **GPT-Image-1**、**Gemini 2.5 Flash Image**）能够产生视觉丰富的光栅图像，但文本渲染错误频繁、逻辑关系错乱，且输出为不可编辑的位图格式。

这两条路线的困境揭示了一个核心瓶颈：**现有方法无法同时保证语义精度、视觉质量和灵活的结构控制**。代码生成方法在结构正确性上有优势，但缺乏对视觉美学的精细把控；图像生成方法在视觉丰富度上领先，却牺牲了语义准确性和可编辑性。二者之间的鸿沟正是学术图表生成面临的根本矛盾——研究者需要的是一种既能精确传达科学内容，又具备出版级视觉质量，同时还能灵活编辑和迭代优化的生成方案。

正是这一矛盾催生了 **Paper2Figure** 的设计动机：通过引入中间结构化表示语言 **FigScript** 以及**双多智能体协作流水线**（生成代理与细化代理），将语义理解、布局规划、视觉细化和迭代修正分离为专门的代理角色。这种分解式架构使得系统能够结合代码生成的精确控制与迭代视觉优化，在不牺牲编辑灵活性的前提下实现学术图表的高保真度和美观性。

## 核心方法与创新机理

Paper2Figure 的核心创新在于**引入结构化中间表示语言 FigScript，并将图表生成分解为“生成—细化”双多智能体协作流水线**，从而在保留代码生成精确控制优势的同时，获得迭代视觉优化能力。这一设计直接回应了现有方法的根本瓶颈：基于代码的方法（SVG/Mermaid）虽能保证结构正确，却产生视觉杂乱或布局僵硬的输出；直接图像生成模型（如 GPT-Image-1）虽视觉丰富，但文本渲染不准确、逻辑关系错误且难以编辑。

### 关键 changed slots

**1. 中间表示语言：从 SVG/Mermaid 到 FigScript**

现有代码生成方法依赖 SVG 或 Mermaid 直接描述图形，这导致两个极端——SVG 的细节控制虽强，但缺乏高层语义抽象，模型难以生成美观布局；Mermaid 的语法虽简洁，却严重约束了视觉表现力。Paper2Figure 设计了 **FigScript**，一种结构化布局语言，同时编码图表的语义元素、样式属性和自动布局约束（Section 2.1）。这一抽象层使生成代理可以专注于“画什么”，而布局引擎负责“怎么摆”，将语义正确性与视觉质量解耦。

**2. 生成架构：从单步生成到双多智能体系统**

现有方法无论是代码生成还是图像合成，本质上都是单步前馈过程，缺乏对输出质量的闭环反馈。Paper2Figure 将流程分解为两个阶段的多智能体协作（Algorithm 1）：

- **生成代理（Generation Agents）**：由 PlanAgent、ModuleAgent 和 LayoutAgent 串联组成，依次完成实体抽取与高层规划、FigScript 视觉模块构造、以及对齐/路由/间距的自动优化。
- **细化代理（Refinement Agents）**：构成一个迭代闭环——CriticAgent 检查渲染图像中的模块错位、文本不对齐、颜色失衡等视觉缺陷；RefineAgent 据此制定结构化修订计划；EditAgent 执行计划并更新 FigScript 规范，触发重新渲染。

这种架构将语义理解、布局规划、视觉诊断和修正分离为专门的代理角色，每个角色只需专注有限子任务，从而显著提升整体生成质量。

**3. 细化机制：从无后处理到迭代视觉闭环**

现有方法普遍缺乏有效的后处理机制，或仅提供有限的手动编辑能力。Paper2Figure 的细化代理实现了**基于视觉分析的自动迭代优化**：系统不依赖启发式规则，而是通过 CriticAgent 直接“看”渲染图像来定位问题，再由 RefineAgent 制定针对性修订方案。消融实验证实，Refinement Agents 在模块组织、文本对齐和色彩平衡上带来显著提升，同时在完整性上也有适度增益（Section 4.2）。完整版 Paper2Figure（含细化代理）在所有子标准上均优于仅生成版本，证明了迭代闭环对视觉质量和逻辑清晰度的关键贡献。

**4. 用户交互：从纯文本提示到交互式 Web 编辑器**

现有工具仅支持文本提示输入，生成结果不可直接操控。Paper2Figure 提供了一个集成对话面板、实时画布和 FigScript 检查器的 **Web 编辑器**（Section 2.3），用户既可以通过自然语言指令驱动代理进行生成和编辑，也可以直接操作画布上的任意视觉元素。这一设计将自动化生成与人工微调无缝衔接，使系统既能全自动产出高质量初稿，又保留了精确编辑的灵活性。

> **注意**：上述关于 FigScript 语言定义、代理间通信协议以及 Web 编辑器交互细节的描述均来自论文方法部分（Section 2.1–2.3）和 Algorithm 1 的伪代码框架。由于分析材料中未提供 FigScript 的具体语法规范和代理提示词设计，这些实现层面的细节需要读者在阅读原文时进一步验证。

Paper2Figure 提出了一种**双多智能体协作系统**，将学术图表生成任务分解为语义理解、布局规划、视觉细化和迭代修正四个阶段，并通过中间结构化表示语言 FigScript 实现代理间的精确通信与可编辑输出。系统整体采用“生成—渲染—批评—修订”闭环流水线，包含六个核心代理和一个交互式 Web 编辑器。

### 核心瓶颈与设计动机

现有学术图表生成方法存在根本性矛盾：基于代码生成的方法（如 SVG/Mermaid）能够保证结构正确性，但输出视觉杂乱、布局僵硬；直接图像生成模型（如 GPT-Image-1）虽能产生视觉丰富的输出，却存在文本渲染不准确、逻辑关系错误且难以编辑等缺陷。Paper2Figure 的核心洞察在于：**将生成与细化过程解耦，并引入结构化中间语言，可以在不牺牲编辑灵活性的前提下，同时获得代码生成的精确控制与迭代视觉优化的高保真度**。

### 中间表示语言 FigScript

FigScript 是系统设计的基石。它是一种结构化布局语言，能够编码图表的语义元素、样式属性和自动布局信息。与直接输出 SVG 代码或像素图像不同，所有代理均通过 FigScript 进行通信——生成阶段输出初始 FigScript 规范，细化阶段则通过修改 FigScript 来执行修订操作。这种设计使得系统能够像操作结构化文档一样对图表进行精确编辑，同时保留重新渲染的灵活性。

### 双多智能体流水线

系统工作流分为两大阶段，如 Algorithm 1 所示：

**生成阶段（Generation Agents）** 包含三个代理：
- **PlanAgent**：分析用户输入的文本指令，抽取实体与逻辑关系，生成高层次图表规划 P。
- **ModuleAgent**：根据规划构造 FigScript 视觉模块，包括节点、边、容器和标签等基本元素，生成草稿规范 S_draft。
- **LayoutAgent**：优化对齐、边路由、间距和分组，将草稿规范精炼为初始 FigScript 规范 S_initial，形成紧凑平衡的布局。

**细化阶段（Refinement Agents）** 构成迭代闭环：
- **CriticAgent**：检查当前渲染图像 F_current，识别模块错位、文本不对齐、颜色失衡等视觉问题，输出批评意见 C。
- **RefineAgent**：根据识别的问题制定结构化的修订计划 R。
- **EditAgent**：执行修订计划，更新 FigScript 规范 S_current 并触发重新渲染。

该闭环可多次迭代，直至输出质量满足要求。消融实验表明，完整的细化阶段在模块组织、文本对齐和色彩平衡上带来显著提升，同时在完整性维度上也贡献了适度增益。

### 交互式 Web 编辑器

Paper2Figure 还提供了一个集成式 Web 编辑平台（见 Figure 2），将自动化代理生成与用户驱动控制相连接。编辑器包含三个核心组件：对话面板支持自然语言指令发送给代理进行生成和编辑；实时画布允许用户直接拖拽调整任意视觉元素；FigScript 检查器则展示底层结构化规范，支持高级用户进行精确修改。这种设计使得系统既能全自动运行，也能在需要人工微调时提供直观的操作入口。

### 输入输出流

系统输入为描述图表需求的自然语言文本 I，输出为可直接用于学术出版的高质量图表。整个流程可概括为：文本指令 → 实体抽取与规划 → FigScript 模块构造 → 布局优化 → 渲染 → 视觉批评 → 修订计划 → FigScript 更新 → 重新渲染，循环直至收敛。最终用户可通过 Web 编辑器导出成品图表。

### 补充图表

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Paper2Figure framework, comparing traditional code-based (SVG/Mermaid) and text-to-image methods with our dual multi-agent system and interactive web editor that collaboratively generate, refine, and edit scientific figures*

### 1. 中间表示语言 FigScript

Paper2Figure 的核心创新之一是设计了一种结构化的中间表示语言 **FigScript**，用于编码图形的语义、样式和布局。与直接生成 SVG 或 Mermaid 代码的基线方法不同，FigScript 在语义理解与视觉渲染之间建立了一个可控的抽象层。其关键设计目标包括：

- **语义元素封装**：将节点、边、容器、标签等图形元素抽象为结构化的视觉模块，使生成代理能够以语义级粒度操作图形组件，而非逐像素或逐行代码。
- **样式与布局分离**：通过预定义的布局模板和色彩主题，FigScript 支持自动化的对齐、边路由和间距优化，同时保留对每个模块样式的精细控制。
- **可编辑性**：FigScript 的结构化特性使得细化代理能够精确定位并修改特定模块，而无需重新生成整个图形，这是传统位图图像生成模型无法实现的。

FigScript 的引入使得生成过程从“直接输出最终图形”转变为“生成结构化规格说明→渲染为图形”，从而在保持代码生成方法的结构精确性的同时，获得了迭代视觉优化的灵活性。

### 2. 双多智能体工作流

Paper2Figure 采用双多智能体架构，将图形生成分解为**生成阶段**和**细化阶段**两个协同过程。算法流程如下：

**Algorithm 1: Dual Multi-Agent Workflow**

1. **PlanAgent**：分析用户输入指令 $I$，抽取实体与逻辑关系，生成高层次图形规划 $P$：
   $$P \leftarrow \text{PlanAgent.run}(I)$$

2. **ModuleAgent**：根据规划 $P$ 构造 FigScript 视觉模块（节点、边、容器、标签），生成草稿规格 $S_{\text{draft}}$：
   $$S_{\text{draft}} \leftarrow \text{ModuleAgent.run}(P)$$

3. **LayoutAgent**：优化对齐、边路由、间距和分组，形成初始 FigScript 规格 $S_{\text{initial}}$：
   $$S_{\text{initial}} \leftarrow \text{LayoutAgent.run}(S_{\text{draft}})$$

4. **CriticAgent**：渲染当前 FigScript 为图像 $F_{\text{current}}$，检查视觉问题（模块错位、文本不对齐、色彩失衡等），生成批评意见 $C$：
   $$C \leftarrow \text{CriticAgent.run}(F_{\text{current}})$$

5. **RefineAgent**：根据批评意见 $C$ 制定结构化修订计划 $R$：
   $$R \leftarrow \text{RefineAgent.run}(C)$$

6. **EditAgent**：执行修订计划 $R$，更新 FigScript 规格并触发重新渲染：
   $$S_{\text{current}} \leftarrow \text{EditAgent.run}(S_{\text{current}}, R)$$

步骤 4-6 构成迭代细化闭环，可重复执行直至图形质量满足要求。这种分解设计的关键优势在于：每个代理专注于特定子任务，通过结构化的 FigScript 进行通信，避免了单步生成中语义理解、布局规划和视觉优化之间的冲突。

### 3. 交互式 Web 编辑器

Paper2Figure 提供了一个集成化的 Web 编辑环境，将自动化代理生成与用户驱动控制相结合。该编辑器包含三个核心组件：

- **对话面板**：支持自然语言指令，用户可直接向生成代理或细化代理发送文本命令。
- **实时画布**：允许用户直接拖拽、调整任何视觉元素，实现对图形的手动微调。
- **FigScript 检查器**：展示当前图形的 FigScript 规格，支持高级用户直接编辑结构化代码。

这种设计使得系统既能够全自动生成高质量图形，又保留了人工干预的灵活性，满足了学术出版对图形精确性的严苛要求。

### 4. 公式变量说明

本文未引入新的数学公式或推导。系统的核心机制通过算法流程定义，变量含义如下：

- $I$：用户输入指令（文本描述或论文段落）
- $P$：高层次图形规划（实体列表、关系图、布局约束）
- $S_{\text{draft}}$：初始 FigScript 规格（包含视觉模块定义）
- $S_{\text{initial}}$：经布局优化的 FigScript 规格
- $S_{\text{current}}$：当前迭代中的 FigScript 规格
- $F_{\text{current}}$：由 $S_{\text{current}}$ 渲染得到的图形图像
- $C$：CriticAgent 识别的视觉问题列表
- $R$：针对问题 $C$ 的结构化修订计划

系统的核心贡献在于架构设计而非公式创新，因此本节未涉及需要推导的数学公式。所有技术细节均通过算法流程和代理角色定义进行描述。

## 实验与关键发现

### 主实验结果

Paper2Figure 在 Paper2Figure Bench 上进行了全面的定量评估，该基准包含 100 个来自 arXiv 论文的精选图表，覆盖 10 个学科领域。评估采用三个维度：准确性（Accuracy）、美观度（Beauty）和完整性（Completeness），三者等权平均得到综合得分（Overall Score）。

**全面超越现有基线。** 完整版 Paper2Figure（包含生成代理与细化代理）在 Overall Score 上达到 **79.2%**，相比最强基线整体提升 **14.1%**。在三个子维度上，Paper2Figure 分别实现准确性提升 **12%**、美观度提升 **13.5%**、完整性提升 **17.0%**，在所有维度上均显著优于现有方法。

**代码生成类基线的性能分化。** 基于 SVG 代码生成的模型（GPT-5、Claude 4 Opus、Gemini 2.5 Pro 等）表现相对较强，平均准确性约 65.3%、美观度约 66.3%、完整性约 57.0%。这些模型能够保留详细的文本信息，但普遍存在元素重叠和布局松散的问题。基于 Mermaid 图生成的模型（GPT-5 Mermaid、Claude 4.5 Sonnet Mermaid）性能明显更低，准确性约 57.1%、美观度约 55.1%、完整性约 50.0%，其输出结构僵硬、美学质量不足。直接图像生成模型（GPT-Image-1、Nano Banana）则面临文本失真、模块缺失和逻辑流错误等根本性缺陷。

**评估指标的人类一致性验证。** 为确保自动评估的可靠性，论文将所提出的评分方法与人类判断进行了相关性分析。结果显示，Paper2Figure 的评估指标在所有相似度度量上均表现出最强的人类一致性：**Pearson r = 0.7345**，**Cosine similarity = 0.8652**。这一高相关性验证了自动评分体系能够有效替代人工评估，支撑后续实验结论的可信度。

### 消融实验

为验证各系统组件的贡献，论文进行了消融实验，对比仅使用生成代理（w/o Refinement）与完整系统（含细化代理）的性能差异。

**细化代理的关键作用。** 完整版 Paper2Figure 在所有子标准上均优于仅生成版本，Overall Score 达到 79.2%。细化代理在模块组织、文本对齐和色彩平衡方面带来了显著提升，同时在完整性上也产生了适度增益。这表明迭代视觉分析闭环（CriticAgent → RefineAgent → EditAgent）对于将初步生成的 FigScript 草图打磨为高质量学术图表至关重要——它能够系统性地发现并修正布局错位、文本不对齐、颜色失衡等视觉问题，而这些问题是单步生成所无法解决的。

### 定性案例分析

Figure 5 对比了同一输入描述下不同方法的生成效果，揭示了各范式的典型失败模式：

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/007_Figure_5.jpg]]
*Figure 5: Case study of generated figures for the same input description. SVG-based models preserve detailed text but suffer from overlapping elements and loose layouts; Mermaid-based models produce rigid and less aesthetic results; image generation models often contain text distortions, missing modules, and incorrect logical flows. Paper2Figure achieves both structural accuracy and visual clarity, producing publication-quality figures*

- **SVG 代码生成模型**保留了详细的文本信息，但存在严重的元素重叠和布局松散问题，逻辑结构不够清晰。
- **Mermaid 图生成模型**输出结构僵硬，缺乏视觉吸引力，布局受限于模板化的样式。
- **图像生成模型**普遍出现文本渲染错误、模块缺失和逻辑流错误，且输出为不可编辑的位图格式。
- **Paper2Figure** 通过 FigScript 中间表示与双多智能体协作，同时实现了结构准确性和视觉清晰度，生成效果达到出版级质量。

Paper2Figure 内置的布局和色彩模板进一步降低了生成的不确定性——代理使用标准化的视觉组合和预定义的样式关键词来构建图表，这是其视觉质量稳定的重要因素之一。

### 关键图表解读

**Figure 4** 以柱状图形式直观展示了各模型在 Accuracy、Beauty、Completeness 和 Overall 四个维度的得分对比。Paper2Figure（full）在所有维度上均处于最高位置，与代码生成 LLM 和图像生成模型形成明显差距，直观验证了双多智能体架构与 FigScript 中间表示的有效性。

**Table 1** 提供了所有模型在每个评估子标准上的详细得分，读者可从中获取更细粒度的性能差异信息。**Table 2** 则对比了不同自动评分方法（如 CLIP Score、GPT-4o 等）与人类判断的一致性，Paper2Figure 的评分方法在两个指标上均取得最优，为基准测试的评估框架提供了可靠性背书。

### 补充图表

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/003_Figure_3.jpg]]
*Figure 3: Evaluation pipeline of our rubric-based framework. GPT-4o scores Accuracy and Beauty directly from the image, and evaluates Completeness by generating and comparing a visually inferred caption with the reference one. The three scores are equally weighted to produce the final result*

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of different models on Paper2Figure benchmark, showing the average scores for Accuracy, Beauty, Completeness, and the overall mean. Paper2Figure(full) clearly outperforms code-generating LLMs and image-generation models across all dimensions*

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/005_Table_1.jpg]]
*Table 1: Detailed quantitative results for all models on each evaluation sub-criterion*

![[assets/figures/papers/paper_list_l2561_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Paper2Figure_A_Mul/figures/006_Table_2.jpg]]
*Table 2: Comparison of different automatic scoring methods in terms of their agreement with human judgments*

## 定位与知识库关联

### 问题域与现有范式

学术论文图表的自动生成长期面临一个核心矛盾：**语义精确性**与**视觉质量**难以兼得。现有方法可大致归入三条技术路线：

1. **基于代码的生成（SVG/Mermaid）**：利用大语言模型直接输出矢量图形代码。代表性基线包括 **GPT-5**（OpenAI, 2025）、**Claude 4.5 Sonnet**（Anthropic, 2025）、**Claude Opus 4**（Anthropic, 2025）、**Gemini 2.5 Pro**（Gemini 2.5, 2025）等 SVG 生成模型，以及 **GPT-5 (Mermaid)** 和 **Claude 4.5 Sonnet (Mermaid)** 等 Mermaid 图表生成模型。这类方法能够保留详细的文本信息，但 SVG 输出常出现元素重叠、布局松散等问题；Mermaid 则受限于僵化的语法约束，产生的图表结构规整但缺乏视觉美感。

2. **直接图像生成（text-to-image）**：以 **GPT-Image-1**（OpenAI, 2025）和 **Nano Banana / Gemini 2.5 Flash Image**（Gemini 2.5, 2025）为代表，将文本描述直接映射为位图。此类模型在视觉丰富度上具有优势，但普遍存在文本渲染不准确、逻辑关系错误、模块缺失等问题，且位图输出难以进行结构化编辑。

3. **单步生成 + 有限后处理**：上述方法本质上均为单步或端到端生成，缺乏系统性的迭代修正机制。即便部分模型支持简单的后处理，也无法在语义理解、布局规划、视觉细化和错误修正之间形成闭环反馈。

### Paper2Figure 的定位与核心贡献

Paper2Figure 并非在上述范式内做增量改进，而是通过**过程分解**和**中间表示**两个设计决策，从根本上改变了问题求解的结构：

- **中间结构化语言 FigScript**：不同于直接输出 SVG 或 Mermaid 代码，Paper2Figure 设计了一种专门的结构化布局语言 FigScript，用于编码图表的语义元素、样式和自动布局信息。这一中间层将“理解要画什么”与“如何精确绘制”解耦，使得后续代理可以独立操作语义结构和视觉呈现。

- **双多智能体协作流水线**：系统将生成过程分解为两个阶段、六个专门化代理。生成阶段由 **PlanAgent**（抽取实体与逻辑关系，制定高层次规划）、**ModuleAgent**（构造 FigScript 视觉模块）和 **LayoutAgent**（优化对齐、边路由和间距）组成；细化阶段由 **CriticAgent**（检查渲染图像中的视觉问题）、**RefineAgent**（制定结构化修订计划）和 **EditAgent**（执行修订并更新 FigScript）构成闭环。这种分解使得语义理解、布局规划和视觉优化可以各自独立优化，同时通过 FigScript 保持信息传递的精确性。

- **人机协同接口**：Paper2Figure 提供交互式 Web 编辑器，支持自然语言指令和直接画布操作，将自动化生成与人工微调集成在同一环境中。这与纯文本提示输入的基线方法形成鲜明对比。

### 与基线方法的关系

从定量结果来看，Paper2Figure 完整版在 Paper2Figure Bench 上取得 **79.2%** 的整体平均分，比最强基线（约 65.1%）高出 **14.1 个百分点**。在子维度上，准确性提升 **12%**，美观度提升 **13.5%**，完整性提升 **17.0%**。这些增益并非来自单一技术的改进，而是源于架构层面的重构——消融实验表明，细化代理（Refinement Agents）的引入显著提升了模块组织、文本对齐和色彩平衡，同时带来完整性的适度增益。

SVG 类基线模型（如 GPT-5、Claude Opus 4、Gemini 2.5 Pro）在准确性上平均约 65.3%，美观度约 66.3%，完整性约 57.0%；Mermaid 类基线的整体表现更低（准确性约 57.1%，美观度约 55.1%，完整性约 50.0%）。Paper2Figure 通过内置的布局和色彩模板，使代理能够以标准化的视觉组合和预定义样式关键词构建图表，这是其超越纯代码生成方法的关键因素之一。

### 适用边界与局限

尽管 Paper2Figure 在基准测试上表现突出，但论文未明确讨论系统的失败模式或边界条件。以下分析基于方法设计推断，需结合原文进一步验证：

- **模板依赖**：系统内置的布局和色彩模板在提升一致性的同时，可能限制图表风格的多样性。对于需要高度定制化视觉风格的场景，模板约束可能成为瓶颈。
- **多智能体通信的稳定性**：双多智能体流水线涉及多个 LLM 代理之间的 FigScript 传递和迭代修正，链式通信中的错误累积或语义漂移是潜在风险，论文未对此进行量化分析。
- **基准覆盖范围**：Paper2Figure Bench 从约 500 篇 arXiv 论文中筛选 100 个代表性图表，其分布可能偏向特定学科或图表类型，泛化到更广泛的学术图表类型（如复杂数学公式图、地理空间图）的能力尚不明确。
- **计算成本**：多轮迭代细化相比单步生成必然带来更高的推理开销，论文未报告生成延迟或计算成本的对比数据。

### 开放问题

1. **FigScript 的表达能力上限**：FigScript 能否覆盖所有类型的学术图表语义？对于超出其语法约束的复杂图表（如混合了照片、手绘和矢量元素的图），系统的降级策略是什么？
2. **跨学科泛化**：Paper2Figure Bench 的 100 个样本是否足以代表计算机科学以外的学科？在化学结构式、生物通路图、物理示意图等领域的表现需要独立验证。
3. **自动化评估的可靠性边界**：论文提出的评估指标与人类判断的相关性（Pearson r = 0.7345，Cosine similarity = 0.8652）虽然是最优的，但约 0.73 的 Pearson 系数仍表明存在不可忽视的偏差——在哪些类型的图表上自动评估可能系统性偏离人类偏好？
4. **细化代理的收敛性**：迭代闭环的终止条件是什么？是否存在 CriticAgent 持续发现新问题导致无限循环的情况，或 RefineAgent 的修订引入新错误的“修复-破坏”循环？

## 原文 PDF

![[paperPDFs/CVPR_2026/Paper2Figure_A_Multi_Agent_Collaborative_System_for_Figure_Generation_Towards_Academic_Research_Paper.pdf]]
