---
title: "Med-CMR: A Fine-Grained Benchmark Integrating Visual Evidence and Clinical Logic for Medical Complex Multimodal Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Med_CMR_A_Fine_Grained_Benchmark_Integrating_Visual_Evidence_and_Clinical_Logic_for_Medical_Complex_Multimodal_Reasoning.pdf
project_link: null
code_link: "https://github.com/LsmnBmnc/Med-CMR"
aliases:
- MC
- Med-CMR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 视觉编码器的多尺度特征提取能力和跨证据一致性是决定模型能否正确提取视觉线索的关键因素；模型规模扩大虽能提升MCQ准确率，但对开放式推理中的视觉基础提升有限。
primary_logic: 将医学多模态推理系统性分解为三个视觉维度（小目标检测、细粒度判别、空间理解）和四个推理维度（时间预测、因果推理、长尾泛化、多源整合），通过多维度评估和双重问答形式（MCQ+开放式）实现了对MLLM临床复杂推理能力的细粒度诊断。
claims:
- 医学推理复杂性可按视觉和推理维度分解为七项任务。
- GPT-5在MCQ上达到57.81%的总体准确率，在开放式问题上获得48.70分，均优于其他模型。
- 长尾泛化是所有模型中最困难的类别，最佳分数仅55.19%。
- 开放式回答中，连贯性和一致性表现良好，但视觉准确性和事实正确性是主要瓶颈。
---

# Med-CMR: A Fine-Grained Benchmark Integrating Visual Evidence and Clinical Logic for Medical Complex Multimodal Reasoning

> [!tip] 核心洞察
> 将医学多模态推理系统性分解为三个视觉维度（小目标检测、细粒度判别、空间理解）和四个推理维度（时间预测、因果推理、长尾泛化、多源整合），通过多维度评估和双重问答形式（MCQ+开放式）实现了对MLLM临床复杂推理能力的细粒度诊断。

| 字段 | 内容 |
|------|------|
| 中文题名 | Med-CMR：集成视觉证据与临床逻辑的医学复杂多模态推理细粒度基准 |
| 英文题名 | Med-CMR: A Fine-Grained Benchmark Integrating Visual Evidence and Clinical Logic for Medical Complex Multimodal Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00818) · [Code](https://github.com/LsmnBmnc/Med-CMR) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Med-CMR |
| Dataset | Med-CMR MCQ, Med-CMR 开放式, Long-Tail Generalization（MCQ） |

> [!tip] 效果简介
> - Med-CMR MCQ 上，准确率 GPT-5: 57.81% vs Gemini-2.5-Pro: 49.87%; Qwen3-VL-235B-A22B: 49.34% (+7.94 (GPT-5 vs Gemini))。
> - Med-CMR 开放式 上，最终得分 (0-100) GPT-5: 48.70 vs Gemini-2.5-Pro: 45.98; Qwen3-VL-235B-A22B: 42.62 (+2.72 (GPT-5 vs Gemini))。
> - Long-Tail Generalization（MCQ） 上，准确率 GPT-5: 55.19% vs 开源最佳: Qwen3-VL-235B-A22B: 45.86% (+9.33)。

## 概要

医学视觉问答（Medical VQA）基准已从早期的基础理解评估逐步向复杂推理演进，但现有基准普遍缺乏对推理复杂性的细粒度分解，难以诊断多模态大语言模型（MLLM）在临床场景中的具体能力短板。针对这一缺口，本文提出 **Med-CMR**——一个将医学多模态推理系统性分解为三个视觉维度（小目标检测、细粒度判别、空间理解）和四个推理维度（时间预测、因果推理、长尾泛化、多源整合）的细粒度基准，并通过多选题（MCQ）与开放式问题的双重问答形式，实现对模型临床复杂推理能力的多维诊断。

核心发现表明，当前 MLLM 的主要瓶颈集中在**视觉证据提取的准确性不足**与**长尾场景的泛化能力薄弱**：在开放式评估中，多数模型在连贯性和一致性维度接近天花板，但在视觉准确性和事实正确性上显著滞后；长尾泛化是所有模型中难度最大的类别，即便最强模型也仅达到 55.19% 的准确率。在 18 个受测模型中，**GPT-5**（Singh et al., 2025）以 57.81% 的 MCQ 总体准确率和 48.70 的开放式得分居首，**Gemini-2.5-Pro**（Comanici et al., 2025）和 **Qwen3-VL-235B-A22B**（Yang et al., 2025）分别以 49.87% 和 49.34% 位列其后，整体性能仍远未饱和，揭示了医学复杂推理领域的显著提升空间。

方法层面，Med-CMR 并非提出新的模型架构，而是构建了一套**维度引导的基准构建与评估框架**：从 JMCR、NEJM 等权威临床期刊收集真实病例图像与标注，通过 GPT-5-mini 辅助生成问题、三个多模态模型协同构建干扰项，并经由模型过滤与持照医师多阶段审核确保质量。该基准覆盖 11 个器官系统和 12 种成像模态，与已有医学多模态基准（如早期的 VQA-RAD、SLAKE，以及初步触及复杂推理的 OmniMedVQA、GMAI-MMBench 等）形成清晰的方法谱系定位——Med-CMR 是首个将视觉与推理复杂性同时细粒度分解的医学推理基准。

多模态大语言模型（MLLM）在通用视觉问答领域已取得显著进展，然而在医学这一高风险领域，其推理能力的评估仍面临根本性挑战。医学复杂推理要求模型同时具备精确的视觉证据提取能力和严谨的临床逻辑推理能力——前者要求从多尺度医学影像中识别微小病灶、辨别细微纹理差异、理解三维空间关系，后者则涉及时间预测、因果推断、长尾病例泛化以及多源信息整合。现有医学多模态基准主要存在两个结构性缺口：一是评估维度粗粒度，难以定位模型的具体能力短板；二是题目设计偏重基础医学知识问答，未能系统性地考察上述复杂推理维度。

从能力瓶颈来看，当前MLLM在医学推理中的核心矛盾并非语言连贯性不足，而是**视觉证据提取的准确性不足**和**长尾场景的泛化能力薄弱**。实验证据表明，多数模型在开放式回答的连贯性和一致性维度上表现接近天花板，但在视觉准确性和事实正确性上得分急剧下降，揭示出“看得见但看不准、说得出但说不对”的深层困境。与此同时，长尾泛化在所有推理类别中难度最高，即便是性能最强的模型，其准确率也仅达到55.19%，凸显了模型对罕见临床表现和非常规影像模式的识别脆弱性。

在方法层面，模型规模扩展虽能持续提升多项选择题（MCQ）的准确率，但对开放式推理中视觉基础的增益十分有限——规模红利更多地流向语言质量而非视觉理解。更值得关注的是，医学微调模型在复杂推理上的表现反而落后于其通用基座模型，提示当前的领域微调策略可能损害了通用的多模态对齐能力，形成了“领域适应”与“推理保持”之间的张力。

为突破上述困境，**Med-CMR**提出了一种细粒度的医学复杂多模态推理基准，将医学推理复杂性系统性地分解为三个视觉维度（小目标检测、细粒度判别、空间理解）和四个推理维度（时间预测、因果推理、长尾泛化、多源整合），并采用双重问答形式（MCQ与开放式）实现对MLLM临床推理能力的多维度诊断。该基准从真实临床案例报告和研究文献中收集数据，经由人机协同的质量控制流程构建，旨在为医学MLLM的推理瓶颈提供可定位、可归因的评估框架。

## 核心方法与创新机理

Med‑CMR 的核心创新并非提出新的模型架构或训练范式，而是构建了一套**细粒度的医学多模态复杂推理诊断框架**，通过将推理复杂性从“单维度准确率”分解为可归因的视觉与推理子维度，首次系统性地暴露了当前 MLLM 在临床复杂推理中的能力边界与瓶颈。

### 1. 推理复杂性的七维分解

与以往医学 VQA 基准仅给出整体准确率不同，Med‑CMR 将医学多模态推理复杂性分解为 **三个视觉维度**（小目标检测、细粒度判别、空间理解）和 **四个推理维度**（时间预测、因果推理、长尾泛化、多源整合），共计七项任务（Figure 1）。这一分解使评估从“模型答对与否”升级为“模型在哪个能力维度上失败”，为后续改进提供了明确的因果抓手。论文明确指出，长尾泛化是所有模型中最困难的类别，即使最强模型 GPT‑5 在该维度也仅取得 55.19% 的准确率（Table 2），揭示了当前 MLLM 在罕见病例推理上的系统性脆弱。

### 2. 双重问答形式与细粒度评分体系

Med‑CMR 对每道题目同时提供 **MCQ 和开放式问题**，并针对开放式回答设计了四维评分框架：一致性（权重 1）、连贯性（权重 1）、视觉准确性（权重 4）、事实正确性（权重 4），最终得分由加权和公式计算：

$$S = \frac{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i s_i}{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i}$$

这一设计的关键创新在于**通过权重倾斜将评估重心压向视觉基础和事实正确性**，从而避免模型凭借语言流畅性“蒙混过关”。实验结果显示，许多模型在连贯性上表现接近天花板，但视觉准确性和事实正确性得分显著偏低（如 Qwen3‑VL‑30b‑A3B 的连贯性达 79.84，而视觉准确性仅 29.73），直接证实了“提取正确的视觉证据并收敛到正确答案”是当前 MLLM 的主要瓶颈。

### 3. 人机协同的数据构建管线

Med‑CMR 的数据构建管线融合了三个关键设计，确保基准的难度与医学可靠性：

- **维度引导的数据收集**：从 JMCR、NEJM 等权威临床案例报告和研究文章中收集符合七种复杂性维度的医学图像及标注，而非从通用图像库中简单爬取。
- **模型辅助的问题生成与干扰项构建**：使用 GPT‑5‑mini 根据人工模板生成 MCQ 和开放式问题，并联合三个多模态模型生成候选干扰项，再由三名医学背景标注者筛选出最终干扰项。
- **多阶段质量过滤**：首先排除三个弱模型（Lingshu‑7B、Qwen2.5‑VL‑7B、Llava‑Med‑v1.5‑Mistral‑7B）均能答对的题目，确保基准难度；随后由执照医师进行全面审核，确认医学准确性。

这一管线在保证题目临床真实性的同时，有效避免了传统人工标注的规模瓶颈和纯模型生成的质量不可控问题。

### 4. 与已有基准的差异化定位

Table 1 将 Med‑CMR 与已有医学多模态基准进行了系统对比。早期基准（如 VQA‑RAD、SLAKE）聚焦于基本理解，近年基准（如 OmniMedVQA、GMAI‑MMBench）开始触及复杂推理，但 Med‑CMR 首次实现了对视觉证据提取和临床逻辑推理的**细粒度、可归因评估**，并同时覆盖 MCQ 和开放式两种问答形式。这一定位使 Med‑CMR 不仅是性能排行榜，更是一个面向 MLLM 临床推理能力的诊断工具。

### 5. 关键发现驱动的创新启示

通过 Med‑CMR 的细粒度评估，论文揭示了两个反直觉的关键发现，这些发现本身构成了对领域的重要创新贡献：

- **模型规模扩展的边际效益递减**：在 MCQ 上规模扩展持续提升准确率，但在开放式推理中，规模优势主要集中在语言质量上，对视觉理解的提升有限（Figure 3）。这表明单纯扩大模型规模无法解决视觉基础的根本问题。
- **医学微调的双刃剑效应**：医学微调模型在 MCQ 上表现落后于其基座模型，仅在部分开放式任务上差距缩小甚至反超（Figure 4b）。这提示当前的医学微调策略可能损害了通用的多模态对齐能力，为未来医学模型训练策略的改进提供了重要警示。

综上，Med‑CMR 的核心创新在于**将医学多模态推理评估从“黑盒打分”转变为“白盒诊断”**，通过七维分解、双重问答形式和加权评分体系，系统性地定位了当前 MLLM 在视觉证据提取和长尾泛化上的能力短板，为后续模型改进和训练策略优化提供了明确的因果指引。

Med-CMR 并非提出一个新的模型架构，而是构建了一个**细粒度诊断基准**，其核心 pipeline 围绕“维度引导的数据构建—双重问答生成—多维度评估”三条主线展开，形成从数据收集到能力诊断的闭环。

### 维度驱动的设计逻辑

整个框架的起点是将医学多模态复杂推理**系统性地分解为七个维度**：三个视觉维度（小目标检测、细粒度判别、空间理解）和四个推理维度（时间预测、因果推理、长尾泛化、多源整合）。这一分解并非随意划分——视觉维度对应模型“看到了什么”，推理维度对应模型“如何基于所见进行临床推断”，二者共同构成对 MLLM 临床复杂推理能力的细粒度诊断基础。每个维度对应一类特定任务，确保评估覆盖从感知到认知的完整链条。

### 数据构建流水线

数据构建遵循“收集—生成—干扰项构建—过滤”的四阶段流程：

1. **维度引导的数据收集**：从 JMCR、NEJM 等权威生物医学期刊的临床案例报告和研究文章中收集符合七种复杂性维度的医学图像及人工标注。这确保了数据来源的真实临床背景，但也引入了潜在的选择偏倚——已发表的案例报告可能无法完全覆盖真实临床场景的多样性。

2. **问题生成**：使用 GPT-5-mini 辅助，根据人工设计的模板为每张图像生成 MCQ 和开放式问题。模型从人工标注的标题中提取正确答案，保证问题与图像证据之间的锚定关系。

3. **干扰项构建**：采用人机协同框架——三个多模态模型（GPT-5-Mini、Qwen3-VL-Plus、Claude-Sonnet-4）生成候选干扰项，再由三名具有医学背景的标注者筛选出四个最终干扰项。这一设计旨在生成具有迷惑性但医学上可区分的错误选项，提升 MCQ 的判别力。

4. **数据过滤与质量保证**：结合模型过滤和多阶段人工审核。先用三个弱模型（Lingshu-7B、Qwen2.5-VL-7B、Llava-Med-v1.5-Mistral-7B）测试每道题目，排除三者均能答对的题目以提升难度；随后所有题目经过持照医师的全面审核，确认医学准确性。

### 双重评估框架

Med-CMR 的评估体系同时覆盖 MCQ 和开放式问题两种形式，避免单一形式带来的评估偏差。MCQ 直接以准确率衡量；开放式问题则采用独立的 LLM（DeepSeek-V3.2-Exp）按四个维度评分：一致性、连贯性、视觉准确性和事实正确性。最终得分通过加权公式计算：

$$S = \frac{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i s_i}{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i}$$

其中视觉准确性和事实正确性的权重（$w_{\mathrm{vis}}=4, w_{\mathrm{gt}}=4$）远高于一致性和连贯性（$w_{\mathrm{cons}}=1, w_{\mathrm{coh}}=1$），反映出框架对**视觉证据提取和事实正确性**的核心关注。这一权重设计直接呼应了核心发现：模型在连贯性方面表现尚可，但视觉准确性和事实正确性才是真正的瓶颈。专家人工评估验证了 LLM 评分与人工判断的高度一致性（Spearman 相关系数 > 0.78），为自动化评估提供了可信度支撑。

### 输入输出流

整个框架的输入是医学图像及其对应的人工标注，经过流水线处理后输出两类评估信号：MCQ 的准确率（按七种推理类型和六种医学智能类别细分）和开放式问题的四维得分。这些输出信号最终汇聚为对模型能力的细粒度诊断——不仅告诉你哪个模型更强，更揭示了强在哪里、弱在何处，从而为后续的模型改进提供明确的因果抓手。

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/004_Figure_1.jpg]]
*Figure 1: Overview of Med-CMR. Med-CMR decomposes medical multimodal reasoning complexity into visual complexity (i.e., smallobject detection, fine-detail discrimination, and spatial understanding) and reasoning complexity (i.e., temporal prediction, causal reasoning, long-tail generalization, and multi-source integration). Each dimension corresponds to a specific task designed to evaluate the model’s capability in that dimension*

### 基准构建流水线

Med-CMR 的构建围绕四个关键模块展开，形成从数据采集到质量保证的完整闭环：

**维度引导的数据收集**：从《Journal of Medical Case Reports》（JMCR）、《New England Journal of Medicine》（NEJM）等权威生物医学期刊的临床案例报告和研究文章中收集医学图像及对应标注，确保每份数据天然对应七种复杂性维度中的至少一种。

**问题生成**：使用 **GPT-5-mini-2025-08-07** 辅助自动生成问题——对每张收集到的图像，模型从人工设计的模板库中选择合适模板，并从人工标注的标题中提取正确答案。每张图像同时生成一道多选题（MCQ）和一道开放式问题，形成双重评估形式。

**干扰项构建**：采用人机协同框架。三个多模态模型（**GPT-5-Mini-2025-08-07**、**Qwen3-VL-Plus-2025-09-23**、**Claude-Sonnet-4-20250514**）各自生成候选干扰项，随后由三名具有医学背景的标注者从中筛选四个最终干扰项，确保干扰项兼具迷惑性和临床合理性。

**数据过滤与质量保证**：通过两阶段过滤确保题目难度和医学准确性。第一阶段为模型过滤：使用三个弱模型（**Lingshu-7B**、**Qwen2.5-VL-7B**、**Llava-Med-v1.5-Mistral-7B**）评估每道题，三个模型均能答对的题目被排除。第二阶段为多轮人工审核，最终由持照医师对所有问题进行医学准确性确认。

### 开放式问题评估公式

开放式回答的最终得分采用加权平均方式计算，综合四个评估维度的得分：

$$S = \frac{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i s_i}{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i}$$

其中各变量含义如下：
- $s_{\mathrm{cons}}$：一致性得分（Consistency），衡量回答内部逻辑是否自洽
- $s_{\mathrm{coh}}$：连贯性得分（Coherence），衡量语言表达的流畅度和条理性
- $s_{\mathrm{vis}}$：视觉准确性得分（Visual Accuracy），衡量从图像中提取视觉证据的正确程度
- $s_{\mathrm{gt}}$：事实正确性得分（Ground-truth Correctness），衡量最终结论与标准答案的一致性

权重分配反映了各维度对临床推理的重要性差异：
- 一致性和连贯性权重：$w_{\mathrm{cons}} = 1$，$w_{\mathrm{coh}} = 1$
- 视觉准确性和事实正确性权重：$w_{\mathrm{vis}} = 4$，$w_{\mathrm{gt}} = 4$

这一权重设计体现了基准的核心设计理念：语言质量是必要但不充分的条件，真正决定医学推理能力的是视觉证据提取的准确性和最终临床判断的正确性。该设计也直接呼应了实验中的关键发现——多数模型在连贯性和一致性上表现接近天花板，但在视觉准确性和事实正确性上存在显著瓶颈。

## 实验与关键发现

### 主结果：跨模型与跨维度的性能诊断

Med-CMR 通过双重问答形式（MCQ 与开放式）对 18 个 MLLM 进行了细粒度评估。**GPT-5**（Singh et al., 2025）在 MCQ 上取得 57.81% 的总体准确率，在开放式任务上获得 48.70 的最终得分，均为所有模型中的最佳表现。商业模型 **Gemini-2.5-Pro**（Comanici et al., 2025）以 49.87%（MCQ）和 45.98（开放式）位居第二。在开源模型中，**Qwen3-VL-235B-A22B**（Yang et al., 2025）表现最优，MCQ 准确率为 49.34%，开放式得分为 42.62。

从七项推理维度审视，**长尾泛化**（Long-Tail Generalization）是所有模型共同面临的最大瓶颈——即使是最强的 GPT-5 也仅达到 55.19%，而开源最佳模型 Qwen3-VL-235B-A22B 在该维度仅为 45.86%，两者差距达 9.33 个百分点。这一结果揭示了当前 MLLM 在罕见病、非典型表现等长尾场景上的系统性脆弱。

在开放式评估中，各模型在**连贯性**（Coherence）和**一致性**（Consistency）维度表现普遍较好，部分模型接近天花板；然而**视觉准确性**（Visual Accuracy）和**事实正确性**（Ground-truth Correctness）得分显著偏低。以 Qwen3-VL-30b-A3B 为例，其连贯性高达 79.84，但视觉准确性和事实正确性分别仅为 29.73 和 25.15。这一反差表明：**提取正确的视觉证据并将其转化为事实正确的答案，是当前 MLLM 医学复杂推理的核心瓶颈**，而非语言生成能力。

### 规模效应与医学微调的悖论

模型规模扩展对性能的影响呈现维度分化（图 3）。在 MCQ 任务上，规模增大持续带来准确率提升，这主要得益于模式识别、多模态整合和临床知识检索能力的增强。但在开放式推理中，规模扩展的收益**高度集中于语言质量维度**（连贯性和一致性），对视觉基础和事实正确性的提升十分有限。这表明单纯扩大模型规模无法从根本上解决视觉证据提取不足的问题。

更值得关注的是医学微调模型的**性能退化现象**（图 4b）。**Medgemma**（Sellergren et al., 2025）和 **Lingshu**（Xu et al., 2025）等医学微调模型在 MCQ 上的表现普遍落后于其对应的基座模型，而在开放式任务上差距有所缩小甚至出现反超。这一悖论暗示：当前的医学微调策略可能在注入领域知识的同时，损害了模型通用的多模态对齐能力，导致其在需要精确视觉证据匹配的 MCQ 任务上反而退步。

### 失败模式：GPT-5 的错误溯源

对 GPT-5 的人工错误标注分析（图 4a）揭示了三个主导性失败来源：
1. **图像识别错误**：模型未能准确定位或识别图像中的关键视觉特征，尤其在小目标检测和细粒度判别任务中突出；
2. **推理偏差**：即使视觉证据提取正确，模型在因果推理和多源信息整合时仍会出现逻辑断裂；
3. **医学知识不足**：面对长尾病例或罕见表现时，模型缺乏足够的领域知识支撑正确判断。

这些失败模式与前述瓶颈高度吻合，进一步确认了视觉编码器的多尺度特征提取能力和跨证据一致性是决定模型表现的关键因果变量。

### 评估可靠性与数据安全

开放式评估采用独立 LLM **DeepSeek-V3.2-Exp** 按四个维度分别评分，最终得分通过加权公式计算：

$$S = \frac{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i s_i}{\sum_{i \in \{\mathrm{cons, coh, vis, gt}\}} w_i}$$

其中一致性（$w_{\mathrm{cons}}=1$）和连贯性（$w_{\mathrm{coh}}=1$）权重较低，视觉准确性（$w_{\mathrm{vis}}=4$）和事实正确性（$w_{\mathrm{gt}}=4$）权重较高，以突出视觉基础能力的重要性。专家人工评估验证显示，LLM 评分与人类判断的 Spearman 相关系数超过 0.78，表明自动评估具有高度一致性。

数据泄漏分析（表 4、表 5）表明，GPT-5 等模型在 MCQ 转换和开放式子集上的 ROUGE-L 和编辑距离相似度均远低于污染阈值，排除了模型预先接触测试内容的可能性。

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/006_Table_1.jpg]]
*Table 1: Comparison of Med-CMR with prior multimodal medical benchmarks. The background colors denote benchmark categories: purple for early Medical VQA datasets focusing on basic understanding, orange for benchmarks that start to touch complex reasoning, and light yellow for our Med-CMR with fine-grained complex medical reasoning evaluation*

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/007_Figure_2.jpg]]
*Figure 2: Benchmark statistics. The left panel displays the inference types across seven questions in the benchmark and their corresponding quantitative relationships with medical ability. The right side shows the modalities of the benchmark images and the body systems involved*

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/008_Table_2.jpg]]
*Table 2: Scores of MLLMs on the benchmark. Seven inference types are Small-Object Detection (SOD), Fine-Detail Discrimination (FDD), Spatial Understanding (SU), Temporal Prediction (TP), Causal Reasoning (CR), Long-Tail Generalization (LTG), and Multi-Source Integration (MSI). Four metrics for open-ended questions are Consistency (Con), Coherence (Coh), Visual accuracy (VA), and Groundtruth correctness (GT). Bold indicates the best. underline indicates the second place. Closed-source models and open-source models of different sizes are ranked separately*

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/009_Table_3.jpg]]
*Table 3: Scores of MLLMs on the benchmark by medical intelligence in Figure 2. Medical intelligence includes clinical decision support (CDS), diagnosis (DX), psychophysiologic analysis (PA), procedural risk assessment (PRA), staging and extent evaluation (SEE), and treatment response evaluation (TRE)*

![[assets/figures/papers/paper_list_l2744_https_arxiv_org_abs_2512_00818/figures/011_Figure_4.jpg]]
*Figure 4: (a) Human-labeled GPT-5 error distribution across question dimensions. (b) Comparison of base models and corresponding medical models on the Med-CMR metrics. (c) MCQ and open-ended results from 500 reformulated MCQs for comparing base models and corresponding medical models. (d) Comparison of win ratios under human and LLM (DeepSeek-V3.2-Exp) evaluation across four dimensions*

## 定位与知识库关联

### 1. 与已有基准的关系：从基础理解到细粒度复杂推理

Med-CMR 在医学多模态基准的演进脉络中占据“细粒度复杂推理评估”这一缺口。如 Table 1 所示，早期医学 VQA 数据集（如 VQA-RAD、SLAKE、PathVQA）聚焦于基础视觉理解与简单问答；后续基准（如 OmniMedVQA、GMAI-MMBench）开始触及复杂推理，但未对推理困难的来源进行系统分解。Med-CMR 的核心区分点在于将医学复杂性从视觉和推理两个维度解耦为七项可独立评估的任务，从而实现对模型能力的细粒度诊断。

**Table 1**（见实验与分析部分）通过颜色标注清晰呈现了这一演进：紫色区为基础理解基准，橙色区为初步触及复杂推理的基准，浅黄色区为 Med-CMR 所代表的细粒度复杂推理评估。Med-CMR 在问题形式（MCQ + 开放式双重问答）、视觉证据提供、长尾泛化专项评估等方面均填补了已有基准的空白。

### 2. 与基线模型的关系

论文评估了 18 个多模态大模型，覆盖闭源商业模型、开源通用模型和医学微调模型三个梯队：

- **最强闭源模型**：**GPT-5**（Singh et al., 2025）在 MCQ 上取得 57.81% 总体准确率，在开放式任务上获得 48.70 分，均显著领先于第二名 **Gemini-2.5-Pro**（Comanici et al., 2025）的 49.87% 和 45.98 分。但需注意，即使是 GPT-5，在最具挑战性的长尾泛化类别上也仅达到 55.19%，表明当前最强模型仍远未解决医学复杂推理问题。

- **开源模型最佳**：**Qwen3-VL-235B-A22B**（Yang et al., 2025）以 49.34% 的 MCQ 准确率位居开源第一，但其在长尾泛化上仅 45.86%，与 GPT-5 差距达 9.33 个百分点，提示开源模型在罕见病例推理上的能力缺口更为显著。

- **医学微调模型**：**Medgemma-4B/27B**（Sellergren et al., 2025）和 **Lingshu-7B/32B**（Xu et al., 2025）等医学微调模型在 MCQ 上表现普遍落后于其基座模型，但在某些开放式任务上差距缩小甚至反超。这一反直觉现象暗示当前的医学微调策略可能损害了通用的多模态对齐能力，而非简单注入领域知识即可提升复杂推理。

### 3. 适用边界

Med-CMR 的适用边界由以下设计选择决定：

- **静态单图像推理**：基准仅考察基于单张静态医学图像的单轮推理，不涉及多轮对话、交互式诊断流程或纵向图像序列分析。对于需要结合患者病史动态调整诊断假设的临床场景，Med-CMR 无法提供评估。

- **已发表案例报告来源**：数据主要来源于 JMCR、NEJM 等期刊的案例报告和研究文章，这些已发表案例可能存在选择偏倚——倾向于教学价值高或罕见但已确诊的病例，不完全代表真实临床环境中遇到的病例分布。

- **双问题形式**：每道题同时提供 MCQ 和开放式问题，这一设计有利于对比封闭式与开放式推理能力，但也意味着模型在开放式回答中可能受益于 MCQ 选项的隐式提示（尽管论文通过问题重述实验检验了这一影响）。

### 4. 局限性与开放问题

**已明确的局限性**：

1. **评估偏差**：尽管开放式评分采用独立 LLM（DeepSeek-V3.2-Exp）按四维度评分，并通过专家人工评估验证了高度一致性（Spearman 相关系数 > 0.78），但外部 LLM 的评估偏差并未完全消除。视觉准确性和事实正确性这两个高权重维度的评分可靠性尤为关键。

2. **覆盖范围**：基准未涉及多轮对话和交互式诊断，且数据来源的选择偏倚可能影响对真实临床场景泛化能力的评估。

3. **医学微调策略反思**：实验结果揭示的医学微调模型性能倒退现象，提示当前医学微调方法可能需要根本性的重新设计，而非简单的领域数据继续训练。

**开放问题**：

1. **视觉编码器瓶颈**：GPT-5 的错误分析（Figure 4a）显示图像识别错误是最主要的失败来源。如何提升视觉编码器对多尺度特征和跨帧一致性的处理能力，是突破当前性能上限的关键工程问题。

2. **长尾泛化**：长尾泛化是所有模型中最困难的类别（最佳仅 55.19%）。是否需要针对性的训练策略（如罕见病例增强、检索增强生成）或外部知识库支持来提升这一能力，仍待探索。

3. **推理架构创新**：将图式推理（graph-of-thought）与多模态证据整合是否能进一步提高临床推理的准确性，是一个值得探索的方向——当前模型在多源整合维度上的表现也远未饱和。

4. **医学微调与通用能力的平衡**：如何在注入领域知识的同时保持通用多模态对齐能力，是医学 MLLM 训练策略设计的核心矛盾。

## 原文 PDF

![[paperPDFs/CVPR_2026/Med_CMR_A_Fine_Grained_Benchmark_Integrating_Visual_Evidence_and_Clinical_Logic_for_Medical_Complex_Multimodal_Reasoning.pdf]]
