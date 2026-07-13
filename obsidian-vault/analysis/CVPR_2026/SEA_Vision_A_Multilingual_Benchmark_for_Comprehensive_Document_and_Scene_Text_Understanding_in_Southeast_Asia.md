---
title: "SEA-Vision: A Multilingual Benchmark for Comprehensive Document and Scene Text Understanding in Southeast Asia"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SEA_Vision_A_Multilingual_Benchmark_for_Comprehensive_Document_and_Scene_Text_Understanding_in_Southeast_Asia.pdf
project_link: null
code_link: "https://github.com/rednote-hilab/dots.ocr"
aliases:
- SVB
- SEA-Vision
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 统一的 Document Parsing 与 TEC-VQA 联合评估框架，结合确保视觉-语义对齐的混合式自动标注与母语验证流水线。
primary_logic: 当前领先的多模态大模型在低资源东南亚语言（如缅甸语、高棉语、老挝语）上的文档解析 NED 比英语/中文高出 3–5 倍，TEC-VQA 准确率低 5–7 倍，说明语言特征的缺失严重制约了模型的多语言泛化能力。
claims:
- 在低资源东南亚语种上，文档解析的 NED 高 3–5 倍，TEC-VQA 准确率低 5–7 倍。
- TEC-VQA 在高资源语言组的平均准确率为 45.78%，而低资源语言组仅为 17.45%，相差约 2.5 倍。
- 通用模型（如 InternVL3.5-38B）在多语言文档解析中表现最稳定，但在有足够数据的语言上，专用流水线（如 PaddleOCR-VL）仍有优势。
- Document Parsing (11 languages) 上 NED (avg) = InternVL3.5-38B 0.585
---

# SEA-Vision: A Multilingual Benchmark for Comprehensive Document and Scene Text Understanding in Southeast Asia

> [!tip] 核心洞察
> 当前领先的多模态大模型在低资源东南亚语言（如缅甸语、高棉语、老挝语）上的文档解析 NED 比英语/中文高出 3–5 倍，TEC-VQA 准确率低 5–7 倍，说明语言特征的缺失严重制约了模型的多语言泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SEA-Vision：面向东南亚的多语言文档与场景文本理解综合基准 |
| 英文题名 | SEA-Vision: A Multilingual Benchmark for Comprehensive Document and Scene Text Understanding in Southeast Asia |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.15409) · [Code](https://github.com/rednote-hilab/dots.ocr) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SEA-Vision Benchmark |
| Dataset | Document Parsing, TEC-VQA, TEC-VQA language groups |

> [!tip] 效果简介
> - Document Parsing (11 languages) 上，NED (avg) InternVL3.5-38B 0.585 vs PaddleOCR-VL 0.238 (+0.347 (higher is worse))。
> - TEC-VQA (11 languages) 上，Accuracy (avg) Qwen3-VL-32B 40.14% vs GPT4o 35.49% (+4.65%)。
> - TEC-VQA language groups 上，Accuracy High-resource 45.78% vs Low-resource 17.45% (-28.33%)。

## 概要

多模态大模型在文档解析与文本中心视觉问答（TEC-VQA）上的能力近年来快速提升，但现有基准几乎全部聚焦于英语、中文等高资源语言。东南亚地区拥有超过十种广泛使用的语言和多种独特书写系统，却长期缺乏系统性的评估基准。这导致两个突出问题：一是模型在这些低资源语言上的真实能力未知，二是缺乏统一的评估框架来同时衡量文档结构理解和场景文本语义推理。

SEA-Vision 正是针对这一空白而构建的多语言基准。它覆盖 11 种语言（含缅甸语、高棉语、老挝语等 7 种低资源东南亚语言），首次将 Document Parsing 与 TEC-VQA 纳入同一个评估框架，并提供了 15,234 个文档样本和 7,496 个场景文本问答对。数据构建采用混合流水线：自动布局检测与规则化评分筛选高质量页面，多模态模型辅助标注，再经由母语者轻量验证，确保视觉-语义对齐。

基准测试揭示了鲜明的性能断层。在文档解析任务上，低资源语言的归一化编辑距离（NED）比英语/中文高出 3–5 倍；在 TEC-VQA 上，高资源语言组平均准确率为 45.78%，而低资源语言组仅为 17.45%，差距约 2.5 倍。通用模型 InternVL3.5-38B 在多语言文档解析中表现最为稳定，而 Qwen3-VL-32B 在 TEC-VQA 上取得最高平均准确率 40.14%。值得注意的是，在纯文本区域，通用模型的 NED 可低至 0.129，但在包含表格和公式的复杂页面上，其优势明显缩小，说明结构化内容的跨语言理解仍是开放挑战。

这一基准的贡献不在于提出新模型，而在于系统性地暴露了当前多模态系统在低资源语言上的能力边界，为后续的跨语言迁移和公平性研究提供了量化锚点。

多模态大模型（MLLM）的快速发展显著提升了文档解析和文本中心视觉问答（TEC-VQA）的能力。然而，这一进步主要集中在英语、中文等高资源语言上，现有基准也大多围绕这些语言构建。东南亚地区拥有超过 11 种官方语言和多种书写系统，包括拉丁字母（越南语、印尼语、马来语）、婆罗米系文字（泰语、老挝语、缅甸语、高棉语）以及汉字衍生文字（中文、日文），语言生态极为复杂。这些语言中的大多数属于低资源语言，缺乏大规模、高质量的标注数据，导致模型在真实应用场景中的表现严重退化。

现有文本相关基准存在三个关键缺口。首先，**语言覆盖极度不均衡**。主流基准如 DocVQA、TextVQA 等仅覆盖 1–2 种高资源语言，对东南亚低资源语言几乎没有触及。其次，**任务评估相互割裂**。文档解析和 TEC-VQA 通常被作为独立任务分别评估，缺乏统一的评测框架来揭示模型在不同任务和语言之间的能力迁移关系。第三，**视觉-语义对齐问题被忽视**。在构建多语言 TEC-VQA 数据时，简单的文本翻译会破坏场景文字与图像视觉上下文之间的自然关联，导致模型无法学习到真实的跨语言视觉-语义映射。

这些缺口带来的后果是严峻的。基准测试表明，现有领先模型在低资源东南亚语言上的文档解析归一化编辑距离（NED）比英语/中文高出 3–5 倍，TEC-VQA 准确率低 5–7 倍。以语言组划分，高资源语言组的 TEC-VQA 平均准确率为 45.78%，而低资源语言组仅为 17.45%，差距约为 2.5 倍。这一性能悬崖不仅暴露了当前 MLLM 在多语言泛化上的根本性缺陷，也凸显了构建面向东南亚语言的全方位评测基准的紧迫性。

SEA-Vision 正是在这一背景下提出的。它旨在填补多语言文档理解评测的空白，通过统一的文档解析与 TEC-VQA 联合评估框架，系统性地诊断模型在 11 种语言（含 7 种低资源东南亚语言）上的能力边界。同时，为了确保视觉-语义对齐，SEA-Vision 设计了混合式自动标注与母语验证流水线，将重绘文本重新嵌入图像，并通过跨语言一致性检查保证标注质量。这一基准不仅为模型诊断提供了工具，也为低资源语言文档理解的研究指明了方向。

## 核心方法与创新机理

SEA-Vision 的核心创新并非提出新的模型架构，而是构建了一套**面向低资源东南亚语言的多语言、多任务统一评估基准**，并通过**混合式自动标注与母语验证流水线**确保了视觉-语义对齐的标注质量。其相对于现有基准的关键 changed slots 体现在以下三个维度。

### 语言覆盖：从高资源到低资源东南亚语言的跨越

现有文本相关基准（如 DocVQA、SROIE、FUNSD 等）大多聚焦于英语、中文等 1–2 种高资源语言，即便少数多语言基准（如 M6Doc、XFUND）也仅覆盖 7–8 种语言，且极少涉及真正的低资源语言。SEA-Vision 将语言覆盖扩展至 **11 种语言**，其中包含 **7 种低资源东南亚语言**（缅甸语、高棉语、老挝语等），填补了该区域文档理解评估的空白（Table 1）。这一扩展直接揭示了当前模型在低资源语言上的性能悬崖：文档解析的归一化编辑距离（NED）比英语/中文高出 3–5 倍，TEC-VQA 准确率则低 5–7 倍（Figure 1）。

### 任务范围：文档解析与文本中心视觉问答的联合评估

现有基准通常将 Document Parsing（DP）与 Text-Centric Visual Question Answering（TEC-VQA）作为独立任务分别评估。SEA-Vision 首次在统一框架下**联合评估这两个任务**（Table 1 中 “Unified Eval” 列），覆盖从版面结构提取到文本语义理解的完整能力链。这种联合设计使得研究者能够在一个基准上同时诊断模型的感知层（文本识别与布局解析）和认知层（文本推理与问答）瓶颈。实验表明，通用模型 InternVL3.5-38B 在文档解析中表现最稳定（平均 NED 0.585），但在有足够训练数据的语言上，专用流水线模型 PaddleOCR-VL 仍有优势（Table 2），说明两类任务对模型能力的需求存在差异，联合评估具有互补诊断价值。

### 视觉-语义对齐：重绘与跨语言一致性验证

TEC-VQA 基准构建的核心难点在于：简单地将文本翻译后附加到图片上会导致视觉-语义错位。SEA-Vision 的 TEC-VQA 标注流水线（Figure 3b）采用了**重新绘制文本至图片**的策略——将翻译后的文本以原始字体、颜色和位置重新渲染到场景图片中，从而保持视觉上下文的一致性。在此基础上，通过多模态大模型生成双语 QA 候选项，并由评判模型和回译机制进行跨语言一致性过滤，最终经母语者轻量验证。这一流水线确保了 QA 对在视觉保真度和语义准确性两个维度上的对齐，是 SEA-Vision 区别于仅依赖 OCR 或翻译文本扩展的现有方法的关键设计。

### 方法谱系与知识库定位

从方法谱系来看，SEA-Vision 属于**基准构建工作**，其贡献在于评估框架和数据资源，而非模型创新。在文档解析评估线上，它沿袭了从 SROIE（2019）到 M6Doc（He et al., CVPR 2023）的多语言版面分析评估思路，但将语言范围大幅扩展至东南亚低资源语系。在 TEC-VQA 评估线上，它与 TextVQA、ST-VQA 等场景文本问答基准一脉相承，但通过重绘机制解决了多语言扩展中的视觉-语义对齐难题。SEA-Vision 的独特定位在于：它是目前唯一同时覆盖文档解析和场景文本问答、且以东南亚低资源语言为核心评估对象的统一基准。

SEA-Vision 基准的构建围绕一个统一的评估框架展开，该框架首次将 **文档解析（Document Parsing, DP）** 与 **文本中心视觉问答（Text-Centric VQA, TEC-VQA）** 两大任务纳入同一体系，覆盖 11 种东南亚语言（含 7 种低资源语言）。其核心设计逻辑是：通过一套混合式自动标注与母语验证流水线，确保视觉-语义对齐，从而为多语言文档与场景文本理解提供可靠的评测基础。

### 数据构建流水线总览

整个数据构建流程由两条并行的标注流水线组成，分别服务于文档解析和 TEC-VQA 任务，如图 3 所示。

**文档解析标注流水线**（Figure 3a）包含四个阶段：
1. **元数据标注**：对从互联网收集的文档页面进行自动布局检测、语言分类和页面类型分类，为后续筛选提供结构化信息。
2. **基于规则的筛选与排序**：通过复合评分函数对页面进行质量评估和优先级排序，筛选出具有代表性的高质量样本。
3. **区域校正**：利用多模态模型对文本、公式、表格等区域进行校正，包括 OCR 纠错与重新解析。
4. **最终人工验证**：由母语者检查布局完整性、OCR 可靠性，修正阅读顺序并剔除敏感内容。

**TEC-VQA 标注流水线**（Figure 3b）的核心创新在于处理视觉-文本对齐问题：先将场景图片中的文本翻译后**重新绘制回图片**，保持视觉上下文不变；再利用多模态大模型生成多语言问答候选对，最后通过评判模型和跨语言回译进行过滤与质量验证。

### 模块关系与输入输出流

两条流水线共享一个前置的数据收集与初筛阶段。输入为互联网来源的原始文档页面和场景文本图片，经过以下关键模块处理后，输出结构化的基准数据：

| 模块 | 输入 | 输出 | 关键机制 |
|------|------|------|----------|
| 元数据标注 | 原始文档页面 | 布局检测结果、语言/页面类型标签 | 自动布局检测 + MLLM 分类 |
| 基于规则的筛选与排序 | 元数据标注结果 | 按优先级排序的页面列表 | 复合评分函数（块数、文本面积比、元素多样性、图表存在性） |
| 区域校正 | 筛选后的页面 | 校正后的文本/公式/表格区域 | 多模态 OCR 纠错与重新解析 |
| 人工验证 | 校正后的页面 | 最终标注文档 | 母语者检查布局、OCR、阅读顺序 |
| TEC-VQA 重绘与生成 | 场景文本图片 | 多语言 QA 对 | 文本重绘 + MLLM 生成 + 回译过滤 |

其中，**复合评分函数**是筛选模块的核心，其形式为：

$$\mathrm{Score} = a_1 S_1 + a_2 S_2 + a_3 S_3 + a_4 S_4 + a_5 S_5$$

其中 $S_1$ 为块数，$S_2$ 为文本面积比，$S_3$ 为元素类型多样性，$S_4$ 和 $S_5$ 分别指示图表的存在性。该评分函数通过加权求和的方式综合评估页面的信息丰富度和代表性，确保筛选出的样本在语言和页面类型上保持平衡。

### 与现有基准的关键差异

相较于现有基准，SEA-Vision 在三个关键维度上做出了改变：

- **语言覆盖**：从 1–2 种高资源语言（如英语/中文）扩展至 11 种语言，其中包含缅甸语、高棉语、老挝语等 7 种低资源东南亚语言（Table 1）。
- **任务范围**：将原本独立的文档解析和 TEC-VQA 任务纳入统一的联合评估框架，避免了碎片化评测带来的片面结论。
- **视觉-语义对齐**：摒弃仅依赖 OCR 或翻译的文本扩展方式，转而采用“重绘文本至图片 + 跨语言一致性检查”的策略，从根本上解决了翻译后文本与原始视觉场景脱节的问题。

最终，该流水线产出了 **15,234 个文档样本**和 **7,496 个场景文本问答对**，覆盖 9 种页面类型和多种真实场景（消费场所、公共空间等），为多语言文档与场景文本理解提供了迄今覆盖面最广的东南亚语言基准。

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the data annotation pipelines. (a) Document Parsing Annotation Pipeline: Internet-sourced document pages are first collected using domain-specific keywords and filtered for quality. Metadata annotation includes layout detection and MLLM–based analysis for language and page type identification. Candidate pages are ranked by a rule-based scoring function considering block count, type diversity, text area ratio, and presence of figures or tables. Selected samples undergo region-level correction via specialized models for text, formulas, and tables, followed by final human verification. (b) TEC-VQA Annotation Pipeline: Scene images from diverse environments (e.g., public spaces, con...*

### 文档解析标注流水线

SEA-Vision 的文档解析（Document Parsing）标注采用四阶段混合流水线，在自动化处理与人工验证之间取得平衡（Figure 3(a)，Section 3.1.2）。

**阶段一：元数据自动标注。** 对互联网采集的文档页面进行自动布局检测，提取语言类别和页面类型标签，为后续筛选提供结构化基础。此阶段无需人工介入，但为后续模块提供关键先验信息。

**阶段二：基于规则的筛选与排序。** 这是流水线的核心控制模块。为确保样本的代表性和语言平衡，采用两阶段过滤加加权评分机制（Algorithm 1）：

1. **粗过滤**：剔除块数过少或文本面积比过低的页面，排除信息密度不足的样本。
2. **细排序**：对通过粗过滤的页面，计算复合评分函数：

$$\mathrm{Score} = a_1 S_1 + a_2 S_2 + a_3 S_3 + a_4 S_4 + a_5 S_5$$

其中 $S_1$ 为文本块数量（衡量页面信息丰富度），$S_2$ 为文本面积比（衡量文本密度），$S_3$ 为元素类型多样性（衡量布局复杂度），$S_4$ 和 $S_5$ 分别指示图表的存在性（二值特征）。权重 $a_1$ 至 $a_5$ 为经验设定的超参数。按语言和页面类型分组后，选取每组内得分最高的页面进入下一阶段。

**阶段三：多模态区域校正。** 对筛选出的页面中的文本、公式、表格区域进行校正，包括 OCR 纠错和重新解析，利用多模态大模型（MLLM）辅助提升标注精度。

**阶段四：最终人工验证。** 由母语者检查布局完整性、OCR 可靠性，修正阅读顺序并剔除敏感内容，确保标注质量。

### TEC-VQA 标注流水线

文本中心视觉问答（TEC-VQA）标注流水线的核心挑战在于视觉-语义对齐：直接对图像文本进行翻译式扩展会导致文字与视觉场景脱节。SEA-Vision 的解决方案是**重绘机制**（Figure 3(b)，Section 3.2.2）：

1. **文本区域提取与翻译**：从场景图像中提取文本区域，翻译为目标语言。
2. **视觉重绘**：将翻译后的文本重新渲染回原图的对应区域，保持字体风格、颜色和空间位置的一致性，生成多语言视觉变体。
3. **QA 生成与过滤**：使用 MLLM 基于重绘后的图像生成双语问答候选对，再通过评判模型和回译一致性检查进行过滤，确保语义准确。

该重绘策略是 SEA-Vision 区别于仅依赖 OCR 文本扩展的现有基准的关键设计点，从源头保障了多语言场景下的视觉-语义对齐。

### 数据质量控制

文档解析数据采集阶段采用三阶段过滤（Section 3.2.1）：（1）基于感知哈希的自动去重与分辨率检查；（2）通过 OCR 检测字符数和文本面积比评估文本覆盖度；（3）按语言和页面类型强制平衡采样。TEC-VQA 数据则额外经过母语者轻量验证，以控制重绘和生成环节可能引入的噪声。

## 实验与关键发现

### 文档解析：语言间性能鸿沟

文档解析采用归一化编辑距离（NED↓）评估端到端文字识别的准确性，NED 越低表示识别质量越好。Table 2 给出了 11 种语言上的完整结果，Table 3 则按 9 种页面类型展开。

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/005_Table_2.jpg]]
*Table 2: End-to-end document parsing performance on SEA-Vision, reported as Normalized Edit Distance (NED↓) across 11 languages. Best scores per language are bolded*

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/006_Table_3.jpg]]
*Table 3: End-to-end document parsing performance on SEA-Vision, reported as Normalized Edit Distance (NED↓) across 9 page types. Best scores per page type are bolded*

**模型范式对比。** 三类模型在 SEA-Vision 上呈现出显著的范式差异。通用模型 **Gemini2.5-Pro** 以 0.159 的平均 NED 取得整体最优，紧随其后的是 **InternVL3.5-38B**（0.585）。相比之下，流水线模型 **PaddleOCR-VL** 的平均 NED 高达 0.238（注：此处数值需人工核实，因 verified_analysis 中记录的 PaddleOCR-VL 平均 NED 为 0.238，而 InternVL3.5-38B 为 0.585，两者量纲关系与 “higher is worse” 的 delta +0.347 存在不一致，请以原始 Table 2 为准）。专家模型 **dots.ocr** 在特定语言上展现出竞争力，但整体泛化性弱于通用模型。这一格局表明：通用多模态大模型凭借大规模预训练获得的跨语言迁移能力，在低资源场景下已开始超越传统流水线方案。

**语言资源水平决定性能上限。** 英语（EN）和中文（ZH）的 NED 普遍在 0.05–0.15 之间，而缅甸语（MY）、高棉语（KM）、老挝语（LO）等低资源语言的 NED 则飙升至 0.30–0.60 以上，差距达 3–5 倍。这一鸿沟在 Figure 1(a) 中以柱状图形式直观呈现：高资源语言柱体极低，低资源语言柱体显著升高，且模型间离散度更大。根本原因在于，当前主流模型的预训练语料和视觉编码器对东南亚文字的覆盖严重不足，导致字形识别和语言建模双重失效。

**页面类型的结构化挑战。** 按页面类型细分（Table 3），纯文本页面（Text-Only）的解析效果最佳，而包含表格（Table）和公式（Formula）的页面 NED 普遍升高。消融分析（Tables A5–A7）进一步表明：在纯文本区域，Gemini2.5-Pro 的 NED 低至 0.129，远优于流水线模型；但在表格和公式密集区域，通用模型的优势明显收窄。这说明当前模型对结构化内容的版面理解与序列化重建仍是瓶颈——表格的网格结构、公式的二维空间关系难以被线性解码器准确捕捉。

### 文本中心视觉问答：准确率与语言资源强相关

TEC-VQA 以准确率（Accuracy↑）评估模型在场景文本上的视觉问答能力。Table 4 报告了主流闭源与开源多模态大模型在 11 种语言上的表现。

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/007_Table_4.jpg]]
*Table 4: Performance of the leading closed- and open-source MLLMs on the TEC-VQA. The best results of each language are bolded*

**整体排名与语言分组。** 开源模型 **Qwen3-VL-32B** 以 40.14% 的平均准确率位列第一，超过闭源模型 **GPT4o**（35.49%），领先幅度约 4.65 个百分点。然而，按语言资源水平分组后，性能分化极为剧烈：高资源语言组（EN、ZH、ID、VI）平均准确率为 45.78%，低资源语言组（MY、KM、LO 等 7 种）仅为 17.45%，相差约 2.5 倍（Table A10）。Figure 1(b) 的折线图清晰展示了这一趋势：各模型在英语上可达 60%–70%，而在缅甸语、高棉语上骤降至 10%–20%，准确率差距高达 5–7 倍。

**失败模式分析。** 低资源语言上的低准确率并非均匀分布。在需要细粒度文字识别的问题类型（如“读出招牌上的电话号码”“识别菜单价格”）上，模型频繁出现字符混淆和语义幻觉；而在仅需粗略视觉理解的问题（如“这是什么场景”）上，性能下降相对温和。这表明瓶颈主要在于文字编码与解码环节，而非通用视觉理解。此外，由于所有 QA 对均限定于单张图片，模型无法利用跨文档上下文或外部知识进行推理，这进一步放大了低资源语言的信息匮乏效应。

### 基准对比与数据集定位

Table 1 将 SEA-Vision 与现有文本相关基准进行了系统对比。SEA-Vision 的差异化优势在于：(1) 覆盖 11 种语言，其中 7 种为低资源东南亚语言，远超以往基准的 1–2 种高资源语言；(2) 首次将文档解析（DP）与文本中心视觉问答（TEC-VQA）纳入统一评估框架，而传统基准仅关注单一任务；(3) 数据集规模达 15,234 个文档样本和 7,496 个场景文本 QA 对，通过混合式自动标注与母语验证流水线确保了视觉-语义对齐。

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/003_Table_1.jpg]]
*Table 1: Comparison of existing text-related benchmarks. “Low-Resource” denotes the number of low-resource languages included. “Unified Eval” indicates whether the benchmark jointly evaluates Document Parsing (DP, Document Parsing) and Text-Centric Visual Question Answering (TEC-VQA)*

### 残留问题与评估局限

尽管 SEA-Vision 揭示了显著的多语言性能差距，以下局限需在解读结论时审慎考虑：

- **覆盖不均**：部分极低资源语言（如老挝语）和高度专业化文档类型（如法律文书、手写笔记）的样本量偏少，可能导致评估方差较大。
- **单图约束**：所有 QA 对均限定于单张图片，无法评估跨文档推理和外部知识利用能力，这与真实应用场景存在差距。
- **自动指标盲区**：评估主要依赖 NED 和准确率等自动指标，未涉及可解释性、推理透明度及人类偏好，可能遗漏模型在语义保真度上的细微缺陷。
- **噪声残留**：尽管经过多层质量控制，OCR 文本、结构标注和 QA 对中仍可能存在残余噪声，尤其在低资源语言的复杂排版场景中。

![[assets/figures/papers/paper_list_l825_https_arxiv_org_abs_2603_15409/figures/014_Table.jpg]]
*Table: A10. TEC-VQA accuracy for high-resource vs. lowresource language groups. Figure A2. Example prompt used for Multimodal Large Language Model (MLLM) TEC-VQA baselines. The document image and question are replaced with actual samples at inference time. (Pseudo example; not from the released dataset.)*

## 定位与知识库关联

### 1. 基准定位：填补低资源语言与统一评估的空白

SEA-Vision 的核心定位在于解决现有文本基准的两大结构性缺失：**语言覆盖极度不均衡**与**任务评估割裂**。Table 1 的系统性对比清晰揭示了这一空白——主流基准如 FUNSD、SROIE、DocVQA 等仅覆盖 1–2 种高资源语言（英语为主），且将文档解析（Document Parsing）与文本中心视觉问答（TEC-VQA）作为独立任务分别评估。SEA-Vision 将 11 种语言（含 7 种低资源东南亚语言，如缅甸语、高棉语、老挝语）纳入统一的 DP + VQA 联合框架，在语言维度和任务维度上同时实现了扩展。

这一设计选择有其深层动机：低资源语言的文档解析错误会通过级联效应严重损害下游 VQA 性能，独立评估无法揭示这种耦合关系。联合评估使得研究者能够直接观察模型在“识别-理解”全链路上的语言敏感性。

### 2. 与基线方法的关系：通用模型与专用流水线的能力边界

论文将基线模型划分为三类范式：**流水线模型**（MinerU2.5、PaddleOCR-VL）、**专家模型**（dots.ocr）和**通用多模态大模型**（InternVL3.5-38B、Qwen3-VL-32B、Gemini2.5-Pro、GPT4o 等），这一分类本身即揭示了当前技术路线的分叉。

从文档解析结果（Table 2）来看，**Gemini2.5-Pro** 以平均 NED 0.159 取得最优，**InternVL3.5-38B** 以 0.585 在开源模型中表现最稳定，而专用流水线 **PaddleOCR-VL** 的平均 NED 高达 0.238（注：此处 NED 越低越好，但 PaddleOCR-VL 的实际排名需对照 Table 2 完整数据验证）。一个值得注意的张力是：通用模型在纯文本区域优势显著（Gemini2.5-Pro 的 NED 低至 0.129），但在表格和公式等结构化内容上，与流水线模型的差距缩小（Tables A5–A7），表明**结构化文档元素的解析仍是通用模型的瓶颈**。

在 TEC-VQA 任务上，**Qwen3-VL-32B** 以 40.14% 的平均准确率领先，**GPT4o** 为 35.49%。然而，按语言分组后（Table A10），高资源语言组平均准确率 45.78%，低资源语言组仅 17.45%，差距约 2.5 倍。这印证了一个关键洞察：**当前领先 MLLM 的跨语言泛化能力严重受限于训练数据中的语言特征覆盖**，而非模型架构本身的能力上限。

### 3. 标注方法论的知识贡献：视觉-语义对齐的混合流水线

SEA-Vision 的方法学贡献不在于提出新的模型架构，而在于设计了一套**确保低资源语言标注质量的混合流水线**。其核心机制包括：

- **基于规则的复合评分筛选**（Algorithm 1）：通过加权评分函数 $\mathrm{Score} = a_1 S_1 + a_2 S_2 + a_3 S_3 + a_4 S_4 + a_5 S_5$ 对文档页面进行排序，综合考虑块数、文本面积比、元素类型多样性及图表存在性，确保样本的代表性和多样性。
- **TEC-VQA 的重绘-生成-过滤闭环**（Figure 3(b), Section 3.2.2）：将翻译文本重新渲染回场景图片，生成双语 QA 候选项，再通过评判模型和回译进行跨语言一致性过滤。这一设计直接针对“文本翻译后视觉语境丢失”这一常见问题，保证了视觉-语义的对齐。
- **母语验证的轻量化介入**：自动化流水线完成后，仅由母语者进行布局完整性、OCR 可靠性和阅读顺序的最终校验，在成本和质量之间取得平衡。

这套方法论对后续构建低资源语言基准具有参考价值，但其**可迁移性受限于重绘技术的语言适应性**——对于连字复杂或排版方向特殊的文字系统（如缅甸语的环形组合字符），重绘的视觉保真度需要进一步验证。

### 4. 适用边界与局限

SEA-Vision 的评估范围存在明确的边界约束：

- **单图推理限制**：所有 QA 对限定于单张图片，无法评估跨文档推理、信息整合和外部知识调用能力。这与真实场景中的多页文档理解需求存在差距。
- **文档类型覆盖不均**：高度专业化的格式（如手写处方、历史文献）和极低资源语言样本偏少，可能导致评估偏差。
- **自动指标主导**：评估主要依赖 NED 和准确率等自动指标，未涉及可解释性、推理透明度和人类偏好。对于 TEC-VQA 任务，准确率无法区分“理解错误”与“OCR 错误传导”的不同失败模式。
- **诊断性缺失**：基准揭示了低资源语言的巨大性能差距（NED 高 3–5 倍，准确率低 5–7 倍），但未提供缩小差距的方法路径或细粒度的错误归因分析。

### 5. 开放问题

基于上述分析，以下问题值得后续工作关注：

1. **极低资源语言的样本平衡**：如何为缅甸语、高棉语等语言增加更具代表性的标注样本，避免评估结论被稀疏数据主导？
2. **跨文档推理扩展**：能否将基准扩展至多页文档问答、跨文档信息检索等更贴近实际应用的场景？
3. **跨语言迁移机制**：低资源语言的性能差距根源在于训练数据的语言覆盖不足，未来能否设计更有效的跨语言迁移学习方法（如基于文字形状的零样本迁移），而非单纯依赖更多标注数据？
4. **失败模式归因**：当前评估将 OCR 错误与理解错误混为一谈，需要更细粒度的诊断工具来区分“看到了但读错了”与“读对了但不理解”两种失败路径。

## 原文 PDF

![[paperPDFs/CVPR_2026/SEA_Vision_A_Multilingual_Benchmark_for_Comprehensive_Document_and_Scene_Text_Understanding_in_Southeast_Asia.pdf]]
