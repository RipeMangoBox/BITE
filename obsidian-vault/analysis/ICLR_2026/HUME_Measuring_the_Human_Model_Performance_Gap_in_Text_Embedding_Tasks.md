---
title: "HUME: Measuring the Human-Model Performance Gap in Text Embedding Tasks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/HUME_Measuring_the_Human_Model_Performance_Gap_in_Text_Embedding_Tasks.pdf
openreview_forum_id: rcmfu1ydAf
aliases:
- HHEFTE
- HUME
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "在MTEB基础上引入可重复的人类评估框架（HUME），提供人类性能基线以校准模型得分。"
primary_logic: "人类表现并非性能上限而是诊断信号：模型在低共识任务上的‘超人类’表现反映标注伪影拟合而非真正语义理解；高人类共识任务才能提供可靠的评估基准，任务质量对评估可靠性的影响大于模型能力差异。"
claims:
- "人类整体平均性能77.6%，最佳模型80.1%，人类排名第4"
- "14/26个任务中模型得分位于人类95%置信区间之外，且多发生在低标注者共识的任务上"
- "当人类专家在情绪分类任务上仅达52.1%共识（κ=0.39）时，模型却获得87.1%的‘超人类’表现，反映了标注模式复制而非情感理解"
- "Overall (16 tasks) 上 Average score (normalized) = 77.6%"
---

# HUME: Measuring the Human-Model Performance Gap in Text Embedding Tasks

> [!tip] 核心洞察
> 人类表现并非性能上限而是诊断信号：模型在低共识任务上的‘超人类’表现反映标注伪影拟合而非真正语义理解；高人类共识任务才能提供可靠的评估基准，任务质量对评估可靠性的影响大于模型能力差异。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | HUME：测量文本嵌入任务中的人机性能差距 |
| 英文题名 | HUME: Measuring the Human-Model Performance Gap in Text Embedding Tasks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rcmfu1ydAf); [GitHub](https://github.com/embeddings-benchmark/mteb) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | HUME (Human Evaluation Framework for Text Embeddings) |
| Dataset | Overall (16 tasks), Multilingual Sentiment (Arabic), Multilingual Sentiment (Russian), Emotion Classification (English) |

> [!tip] 效果简介
> - Overall (16 tasks) 上，Average score (normalized) 为 77.6%，对比 80.1% (jasper_en_vision_language_v1)，变化 -2.5。
> - Multilingual Sentiment (Arabic) 上，Accuracy 为 95.0%，对比 77.5% (SFR-Embedding-Mistral)，变化 +17.5。
> - Multilingual Sentiment (Russian) 上，Accuracy 为 92.5%，对比 81.2% (multilingual-e5-small)，变化 +11.3。

## 概述

文本嵌入模型在信息检索、语义搜索等任务中应用广泛，但现有基准测试（如MTEB）缺乏可靠的人类性能基线，导致模型得分难以解读：一个模型在某任务上达到85%的准确率，究竟意味着接近人类水平还是仍有巨大差距，此前并无系统答案。HUME正是在此背景下提出的一个面向文本嵌入任务的可重复人类评估框架。

**核心发现**：人类并非性能上限，而是诊断信号。在HUME覆盖的16个任务中，人类整体平均得分为77.6%，在13个嵌入模型中排名第4，落后于最佳模型（jasper_en_vision_language_v1，80.1%）。但这一总体排名掩盖了更深层的模式——在26个任务-语言对中，有14个任务的模型得分落在人类95%置信区间之外，且这些偏离几乎全部发生在标注者间一致性低的任务上。典型案例如情绪分类：人类专家共识仅达κ=0.39（公平一致性），而最佳模型却获得87.1%的“超人类”表现。这说明模型并非真正理解了情感语义，而是拟合了标注数据中的伪影模式。

**方法定位**：HUME在MTEB基础上引入三个关键变化：（1）为相同任务定义建立可重复的人类评估协议，使人类与模型在完全对齐的指标上可比；（2）通过多标注者标注系统性诊断数据集质量，揭示标注歧义和共识水平；（3）评估9个大型语言模型作为标注者的可行性，探索自动化基准构建的边界。

**主要结果**：人类在非英语情感分析（阿拉伯语95.0%、俄语92.5%）和阿拉伯语语义相似度任务上显著超越最佳模型，但在ArXiv学术论文聚类（人类49.2% vs 模型84.6%）和重排序（人类87.2% vs 模型96.4%）等任务上存在巨大差距。LLM作为标注者平均达76.1%，低于人类的81.2%，且在重排序任务上差距尤为明显（78.0% vs 88.3%），表明当前LLM尚不能可靠替代人类判断。

**关键洞察**：任务质量对评估可靠性的影响大于模型能力差异。高人类共识任务（如STS12，ρ=0.77）提供可靠的评估基准，人类与模型表现接近；低共识任务则暴露了基准本身的设计缺陷，而非模型能力的真实边界。

## 背景与动机

文本嵌入模型已成为现代自然语言处理的基础组件，支撑着信息检索、语义相似度计算、文本聚类等广泛应用。MTEB等标准化基准测试通过统一的任务定义和评估指标，为模型能力的横向比较提供了平台。然而，一个关键瓶颈长期被忽视：**这些基准测试缺乏可靠的人类性能基线**。

缺乏人类参照的后果是严重的。当模型在某个任务上取得85%的准确率时，这一数字本身无法回答根本性问题——人类在此任务上能达到多少？模型是真正理解了语义，还是仅仅拟合了标注数据中的统计模式？更隐蔽的是，部分数据集本身存在标注歧义和质量问题，而模型在这些数据集上的“优异”表现可能恰恰反映了对标注伪影的精确复制，而非对语言本质的把握。

HUME框架正是在这一缺口上展开工作。其核心设计思路直接而明确：在MTEB的任务体系之上，引入可重复的人类评估协议，使人类标注者使用与模型完全相同的任务定义和评估指标。这一对齐使得模型得分首次获得了可校准的人类参照点，将评估从“模型间相对排序”升级为“以人类为基准的绝对校准”。

研究揭示的核心洞察具有诊断性价值：**人类表现并非性能上限，而是数据集质量的探针**。当标注者间共识较低时（如情绪分类任务中Fleiss’ κ仅0.39），模型却可能获得87.1%的“超人类”表现——这种背离恰恰暴露了任务设计的根本缺陷，而非模型的语义理解优势。相反，在高共识任务上（如STS12的标注者间Spearman ρ达0.77），人类与最佳模型的表现高度接近（91.2% vs 92.0%），这类任务才构成可靠的评估基准。换言之，任务质量对评估可靠性的影响，可能大于模型能力本身的差异。

这一视角转换意味着：在嵌入模型的评估中，追问“人类能得多少分”比追问“哪个模型得分最高”更能揭示基准测试的真实信息量。

## 核心创新

HUME的核心创新在于为文本嵌入基准测试引入**可重复的人类评估基线**，将人类表现从缺失的参照系转变为诊断基准质量的校准工具。其关键设计变更体现在三个维度。

### 1. 人类基线集成：从无参照到对齐校准

现有MTEB框架完全缺乏人类性能基线，导致模型得分缺乏可解读的参照点。HUME通过建立与模型评估**完全对齐的人类评估协议**填补了这一空白：标注者使用与任务定义完全匹配的指令（如分类使用相同标签集、语义文本相似度使用相同的1-5评分量表），在Argilla平台上通过任务特定界面完成标注。这一设计使人类与模型的得分可直接比较，从而揭示了一个反直觉的发现：人类整体平均表现77.6%，在13个嵌入模型中排名第4，最佳模型为80.1%（Figure 1）。人类并非性能上限，而是竞争性参与者。

### 2. 数据集质量诊断：从无检查到标注共识分析

HUME引入了系统性的数据集质量评估机制。通过计算多标注者间一致性指标（Fleiss' kappa、ARI、Spearman ρ等），框架能够诊断标注歧义和质量问题。关键发现是：**14/26个任务中模型得分落在人类95%置信区间之外，且这些偏离集中发生在低标注者共识的任务上**（Table 8）。例如，情绪分类任务中人类专家仅达成52.1%的共识（κ=0.39），而模型却获得87.1%的“超人类”表现——这并非模型真正理解了情感，而是拟合了标注中的模式伪影。相反，在高质量数据集如STS12（标注者一致性ρ=0.77）上，人类91.2%与最佳模型92.0%的差距仅为0.8个百分点，表明高共识任务提供了可靠的评估基准。

### 3. LLM作为标注者基准：从无评估到可扩展性验证

HUME进一步评估了LLM能否替代人类判断，在相同的19个任务-语言对上使用相同指令测试了9个LLM。结果显示最佳LLM（GPT-4.1-mini）平均准确率76.1%，低于人类的81.2%（Table 2），且人类与LLM的难度模式仅部分共享（ρ=0.52）。尤其在重排序任务上，人类88.3%显著优于最佳LLM的78.0%，表明LLM尚不能完全替代人类判断。

### 核心洞察

这三项创新共同指向一个深层发现：**任务质量对评估可靠性的影响大于模型能力差异**。低共识任务上模型的“超人类”表现反映的是标注伪影拟合而非语义理解；高共识任务才能提供可靠的评估基准。HUME将人类表现重新定位为诊断信号而非性能上限，为基准构建提供了质量过滤的新范式。

## 整体框架

HUME（Human Evaluation Framework for Text Embeddings）是一个在MTEB基础上构建的可重复人类评估框架，其核心目标是为文本嵌入基准测试提供可靠的人类性能基线，从而校准模型得分并诊断数据集质量问题。

### 设计原则

框架遵循三条设计原则：**任务定义对齐**——人类标注指令与模型评估的任务定义完全一致（如分类使用相同标签集、语义文本相似度使用相同的1-5量表）；**指标对齐**——人类表现使用与模型评估相同的度量标准计算；**可重复性**——通过标准化的标注协议和界面设计确保评估可复现。

### Pipeline 模块

HUME的pipeline由五个核心模块组成：

**1. 任务与数据集选择**：从MTEB中选取16个多语言、多类型任务，涵盖分类、聚类、重排序和语义文本相似度（STS）四大类别。为适应人类标注的可行性，对数据集进行重采样（每任务30-50个实例），并使用重排序作为信息检索的人类可评估代理任务。

**2. 标注界面设计**：基于Argilla平台构建与任务定义完全匹配的标注界面。分类任务使用类别标签选择，STS使用0-5量表滑块，聚类使用自由簇ID分配，重排序使用二元相关性判断。

**3. 多标注者数据收集**：招募具有语言背景的NLP从业者独立标注。英文任务由多标注者完成以评估标注者间一致性，非英语任务由单标注者完成。

**4. 一致性与质量分析**：计算Fleiss' kappa、调整兰德指数（ARI）、Spearman相关系数等指标，诊断数据集标注质量和任务定义的清晰度。低一致性任务被标记为潜在存在标注歧义或设计缺陷。

**5. LLM标注实验**：使用相同的指令和评估指标，对9个大型语言模型（LLM）进行标注能力评估，以判断LLM是否能作为人类判断的可靠代理。聚类任务因难以从生成式模型中引出簇分配而被排除。

### 输入输出流

框架的输入为MTEB中的标准数据集和任务定义，输出为三个层次的结果：（1）人类性能基线（含95%置信区间和标注者间一致性指标）；（2）人类与模型性能的逐任务对比；（3）LLM作为标注者的性能评估。这些输出共同支持对基准质量的诊断——高人类共识的任务提供可靠的评估基准，而低共识任务上的"超人类"模型表现则揭示标注伪影拟合问题。

## 核心模块与公式推导

HUME框架的核心设计思路是在MTEB基准上叠加可重复的人类评估层，而非重新定义任务或指标。其关键模块如下：

### 3.1 任务与数据集选择

从MTEB中选取16个多语言、多类型数据集，覆盖分类、聚类、重排序和语义文本相似度（STS）四类任务。选择标准兼顾任务多样性与人类可标注性：重排序被用作信息检索的人类可评估代理任务，因为直接评估大规模检索结果对人类而言不可行——人类仅评估top-k候选文档的相关性，建立与嵌入空间行为概念上等价的基线。

### 3.2 标注界面设计

所有标注通过Argilla平台完成，使用与任务定义严格匹配的界面：
- **分类任务**：提供与模型相同的标签集
- **STS任务**：使用相同的1-5分语义相似度量表
- **聚类任务**：要求标注者自由分配簇ID
- **重排序任务**：二元相关性判断

### 3.3 多标注者数据收集

招募具有语言背景的NLP从业者独立标注。英文任务采用多标注者设计以评估标注者间一致性；非英语任务由单一标注者完成，这一点在后续分析中需注意其局限性。

### 3.4 一致性分析模块

框架内置标注者间一致性分析，计算Fleiss' kappa、调整兰德指数（ARI）、Spearman相关系数等指标，用于诊断数据集质量。这是HUME区别于MTEB的关键模块——它使标注歧义和质量问题可量化检测。

### 3.5 LLM作为标注者评估

将9个大型语言模型（LLM）作为标注者，使用与人类完全相同的指令和指标进行评估。聚类任务因难以从生成式模型中引出簇分配而被排除。该模块检验LLM能否作为人类判断的可扩展代理。

### 公式推导

HUME本身未引入新的数学公式。其核心度量均沿用MTEB和标准评估指标：

**分类任务**使用准确率（Accuracy）和F1分数：

$$ \text{Accuracy} = \frac{\text{正确预测数}}{\text{总样本数}} $$

$$ F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} $$

**STS任务**使用Spearman秩相关系数衡量预测分数与人类标注分数之间的单调关系：

$$ \rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)} $$

其中 $d_i$ 为每对样本的秩差，$n$ 为样本对数。

**聚类任务**使用V-Measure（同质性Homogeneity与完整性Completeness的调和平均）和调整兰德指数ARI：

$$ V_{\beta} = \frac{(1+\beta) \times h \times c}{\beta \times h + c} $$

其中 $h$ 为同质性，$c$ 为完整性，通常 $\beta=1$。

$$ \text{ARI} = \frac{\sum_{ij} \binom{n_{ij}}{2} - \left[\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}\right] / \binom{n}{2}}{\frac{1}{2}\left[\sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2}\right] - \left[\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}\right] / \binom{n}{2}} $$

**重排序任务**使用MAP和nDCG@10等标准信息检索指标。

**标注者间一致性**使用Fleiss' kappa（多标注者分类一致性）：

$$ \kappa = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e} $$

其中 $\bar{P}$ 为观察到的一致性比例，$\bar{P}_e$ 为期望的随机一致性比例。

> **注意**：以上公式均为HUME框架中使用的标准评估指标，非论文原创推导。论文的核心贡献在于将这些指标与人类基线系统性地对齐，而非提出新的数学形式化。

## 实验与分析

### 整体人机性能对比

HUME在16个文本嵌入任务上建立了人类性能基线，并与13个最先进的嵌入模型进行系统对比。Figure 1展示了核心发现：人类平均得分为77.6%，在13个模型中排名第4，落后于jasper_en_vision_language_v1（80.1%）、SFR-Embedding-Mistral（78.3%）和e5-mistral-7b-instruct（78.2%）。这一结果表明，当前最佳嵌入模型在整体性能上已略微超越人类水平，但差距有限（-2.5个百分点）。

从任务覆盖范围来看，人类表现呈现出明显的任务依赖性。在26个任务-语言对中，最佳模型得分在14个任务上超出了人类95%置信区间（Table 8），表明模型与人类在大量任务上存在统计显著的差异。然而，这种差异的方向并不一致——人类在5/14的聚合任务-语言对中取得最高性能（Table 1），尤其在非英语情感分析和阿拉伯语语义相似度任务上表现突出。


![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/002_Table_1.jpg]]
*Table 1: Human performance compared to 13 embedding models across task categories and languages. Bold indicates highest performance (human or model), underline indicates best model performance. Humans achieve top performance in 5 of 14 aggregated task-language pairs, particularly excelling in non-English sentiment analysis and Arabic semantic similarity. Overall results are aggregated over the 26 task-language pairs*

![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/019_Table_8.jpg]]
*Table 8: Human performance with 95% confidence intervals. N = number of samples; K = number of annotators; Tot = total annotations ( $\mathrm { N } \times \mathrm { K }$ ) . CIs computed via Wilson Score Interval (Classification), Fisher’s z-transformation (STS), and Annotator Range (Clustering/Reranking). ∗ indicates model score outside human 95% CI ( p < 0 . 0 5 ) . IAA = Inter-Annotator Agreement

### 按任务类别的性能分解

**分类任务**呈现极端分化。在多语言情感分析中，人类显著优于所有模型：阿拉伯语情感分类人类准确率达95.0%，而最佳模型SFR-Embedding-Mistral仅77.5%（差距+17.5）；俄语情感分类人类92.5%对最佳模型81.2%（差距+11.3）。这一优势揭示了当前嵌入模型在非英语、低资源语言上的文化理解不足。

相反，在英语情绪分类任务上，人类仅达45.8%，而jasper_en_vision_language_v1高达87.1%（差距-41.3）。这一巨大差距并非模型真正"理解"情感的证明——该任务的标注者间一致性仅为κ=0.39（公平水平），表明标注本身存在严重歧义。模型的高分更可能反映对标注模式中表面特征的拟合，而非对复杂情感状态的深层语义理解。

**聚类任务**同样呈现两极分化。WikiCities聚类人类V-Measure达97.6%（ARI=0.91），接近最佳模型stella_en_1.5B_v5的100%。但ArXiv学术论文聚类人类仅49.2%（ARI=-0.001，接近随机水平），而模型达84.6%。ARI接近零意味着人类标注者几乎无法就论文主题类别达成共识，这直接指向数据集标注质量问题——学术论文的跨学科性质使预定义类别边界模糊。

**重排序任务**上，人类平均MAP为87.2%，落后最佳模型e5-mistral-7b-instruct的96.4%（差距-9.2）。模型在信息检索相关度判断上的优势可能源于其对大规模查询-文档对统计模式的学习能力。

**语义文本相似度（STS）**任务上，人机差距最小。STS12数据集人类Spearman ρ达91.2%，最佳模型92.0%（差距仅-0.8）。该数据集标注者一致性高达ρ=0.77，是HUME中质量最高的任务之一，表明在定义清晰、歧义低的语义判断上，模型已接近人类水平。

### 标注者共识与数据集质量诊断

Table 8的核心发现是：**模型得分落在人类95%置信区间之外的14个任务，绝大多数发生在标注者间一致性较低的数据集上**。这一模式构成了HUME最重要的诊断信号——当人类自身对正确答案缺乏共识时，模型的高分不代表语义理解，而更可能反映对标注伪影的过拟合。

典型案例包括：
- 情绪分类（κ=0.39）：人类45.8%对模型87.1%
- ArXiv聚类（ARI=-0.001）：人类49.2%对模型84.6%
- Reddit聚类（ARI=0.34）：人类68.8%对模型100%

相反，高共识任务上人机表现趋同：
- STS12（ρ=0.77）：人类91.2%对模型92.0%
- WikiCities聚类（ARI=0.91）：人类97.6%对模型100%
- Robust04重排序（ρ=0.72）：人类88.5%对模型98.8%

这一发现揭示了评估基准构建中的关键瓶颈：**任务质量（以人类共识度衡量）对评估可靠性的影响，远大于模型能力的差异**。低共识任务不仅无法有效区分模型优劣，还会产生误导性的"超人类"表现结论。

### LLM作为标注者的局限性

Table 2展示了9个LLM作为标注者的性能评估结果（排除聚类任务）。最佳LLM标注者GPT-4.1-mini平均准确率76.1%，低于人类标注者的81.2%，且在所有任务类别上均落后于最佳嵌入模型。

重排序任务是LLM与人类差距最大的类别：人类88.3%对最佳LLM（Mistral-Small）78.0%。这表明LLM在需要精细比较多个候选文档与查询相关性的任务上，仍缺乏人类水平的判断力。

Spearman秩相关性分析显示，人类与LLM在19个任务-语言对上的难度模式仅部分共享（ρ=0.52），说明LLM标注者尚不能可靠替代人类判断来构建基准。这一发现对当前依赖LLM生成训练数据或评估标签的实践提出了警示。

### 消融分析：任务质量的关键作用

移除聚类等低共识任务后，人类与模型的整体表现差距显著缩小。相关性分析进一步证实，人类与LLM在任务难度感知上存在中等程度的一致性（ρ=0.52），但这种一致性在低共识任务上明显减弱。

这些消融结果强化了核心洞察：**当前嵌入基准中观察到的"模型超越人类"现象，很大程度上是数据集设计缺陷的产物，而非模型语义理解能力的真实突破**。高人类共识任务才能提供可靠的评估基准，而低共识任务更适合作为数据集质量诊断工具，而非模型能力评判标准。

### 失败模式与局限性

HUME揭示了当前评估范式的三个系统性失败模式：

1. **标注歧义被误读为模型优势**：情绪分类和ArXiv聚类等任务中，模型"超人类"表现实际反映的是对标注噪声的模式复制，而非语义理解。这些任务应被重新设计或从严肃基准中移除。

2. **多语言评估的标注偏差**：非英语任务仅由单一标注者完成（论文明确指出的局限），阿拉伯语和俄语情感分析中人类的大幅领先可能部分源于标注者特定的语言文化知识，而非普遍的人类优势。这些设置下的结论可靠性受限。

3. **标注者群体单一性**：所有标注者均为20-35岁男性NLP从业者，无法代表更广泛用户群体的判断分布。这可能导致人类基线本身存在系统性偏差，尤其是在涉及文化敏感或主观性强的任务上。

### 图表核心结论

- **Figure 1**：人类排名第4（77.6%），证明当前最佳嵌入模型已整体略超人类，但差距微小。

![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/001_Figure_1.jpg]]
*Figure 1: Human performance versus 13 embedding models across 16 tasks. Humans rank 4th (77.6), showing competitive but not dominant performance. Darker shades indicate larger models*

- **Table 1**：任务类别间人机差距差异巨大（-41.3%至+17.5%），揭示评估基准的任务依赖性远大于模型依赖性。
- **Figure 2**：人类表现通常处于模型表现范围的上半区（61.5%任务超中位数），但极少匹配最佳模型（15.4%任务）。
- **Table 2**：LLM标注者（最佳76.1%）尚不能替代人类（81.2%），尤其在重排序任务上差距显著。

![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/004_Table_2.jpg]]
*Table 2: LLM-as-annotator performance compared to human annotators and best embedding models per task category. Human and LLM performance is computed over 19 task-language pairs (clustering tasks excluded due to difficulty eliciting cluster assignments). Best embedding model per task category shown with abbreviated name: jasper (jasper_en_vision_language_v1), SFR (SFR-Embedding-Mistral), e5 (multilingual-e5-large). Bold indicates best LLM performance (humans and embedding models consistently outperform LLMs and are not bolded)*

- **Table 8**：14/26任务中模型得分超出人类95%置信区间，且与低标注者共识强相关，证实任务质量是评估可靠性的首要瓶颈。

### 补充图表

![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/024_Figure_13.jpg]]
*Figure 13: Human performance gaps versus best-performing models across 26 task-language pairs. Humans outperform the best models on only 4 tasks (15.4%), with largest advantages in Arabic semantic similarity and sentiment analysis. The analysis reveals systematic model advantages in technical domains (clustering, reranking) versus human advantages in culturally-informed tasks*

![[assets/figures/papers/iclr26_0011_rcmfu1ydAf_HUME_Measuring_the_Human-Model_Performance_Gap_i/figures/023_Figure_12.jpg]]
*Figure 12: Human win rates across task categories and languages. Top left: By task category shows humans perform moderately in classification but struggle in clustering, reranking, and STS against best models. Top right: English-only vs multilingual tasks reveals humans perform better on multilingual tasks (29% vs 0% against best models). Bottom left: Performance varies dramatically by baseline comparison (15% vs best, 62% vs mean models). Bottom right: Language-specific breakdown shows varying performance across different language codes*



## 方法谱系与知识库定位

### 在基准评估谱系中的位置

HUME直接构建于MTEB（Massive Text Embedding Benchmark）之上，其核心创新不在于提出新的任务或指标，而是**引入可重复的人类评估协议作为校准参照系**。在HUME之前，文本嵌入基准测试完全依赖模型间的相对排序，缺乏对人类性能上限的可靠估计，导致对模型得分（如“87.1%的准确率”）的解读缺乏锚点。

HUME的方法论贡献体现在三个层面的改造：

1. **人类基线集成**：在保持MTEB任务定义和评估指标不变的前提下，为16个多语言多类型任务建立了人类标注流程。这一设计使得人类与模型在完全相同的输入和评分标准下进行比较，而非依赖间接的众包估计或历史数据。

2. **数据集质量诊断**：通过计算标注者间一致性指标（Fleiss' κ、ARI、Spearman ρ等），HUME将数据集质量从隐性假设变为可量化的评估维度。这一转变揭示了MTEB中部分数据集存在严重的标注歧义问题。

3. **LLM-as-annotator基准化**：将9个LLM作为标注者纳入同一框架，评估其替代人类判断的可行性。这一设计同时服务于两个目的：检验LLM能否降低基准构建成本，以及揭示LLM与人类在判断模式上的系统性差异。

### 与相关工作的关系

**与MTEB的关系**：HUME是MTEB的补充层而非替代品。MTEB提供了模型评估的基础设施（任务、数据、指标），HUME在此基础上叠加了人类参照系和质量诊断层。论文明确指出“我们的框架构建于MTEB之上，通过建立与模型评估直接对齐的可重复人类评估协议”（Section 3.1）。这种设计使HUME的结论可以直接映射回MTEB的模型排名，无需重新定义评估体系。

**与LLM评估基准的关系**：HUME借鉴了NLP中人类评估的传统方法论（如机器翻译中的BLEU与人类判断的相关性研究），但将其应用于一个此前缺乏人类基线的领域。与聊天/生成任务的偏好评估不同，HUME聚焦于**判别性任务**（分类、聚类、重排序、语义相似度），这些任务的评估更接近传统标注质量研究。

**与数据集质量研究的关系**：HUME的发现与数据中心AI的研究议程高度一致——模型在低共识任务上的“超人类”表现（如情绪分类中模型87.1% vs 人类45.8%）实质上是**标注伪影拟合**的典型案例。这一发现呼应了NLP社区对基准数据集质量日益增长的关注，但HUME通过系统性的多任务人类基线提供了更全面的证据。

### 适用边界

HUME的适用性受以下因素制约：

**任务类型覆盖**：当前框架覆盖了分类、聚类、重排序和语义文本相似度四类任务，但排除了信息检索（以重排序作为代理）、摘要评估等需要开放式生成的任务。对于需要主观判断的复杂任务（如论证质量评估），当前的任务定义和指标可能不足以捕捉人类判断的丰富性。

**语言覆盖**：虽然HUME包含了阿拉伯语、俄语、挪威语、丹麦语等多语言任务，但非英语任务的标注仅由单一标注者完成（见论文局限性部分）。这意味着非英语任务的人类表现估计存在偏差风险，无法评估跨标注者一致性。

**标注者群体**：所有标注者均为20-35岁男性NLP从业者。这一群体的判断可能无法代表更广泛用户群体的语义直觉，特别是对于情感分析、社交媒体文本等涉及文化和个人经验的任务。

**样本规模**：每个任务仅标注30-50个实例，虽然足以检测较大的人机差距，但可能不足以检测细微差异或进行语言/任务维度的细粒度分析。

### 核心局限

1. **诊断而非修复**：HUME能够识别低质量数据集（如ArXiv聚类ARI=-0.001），但未提供改进数据集设计的具体方法论。论文仅停留在“揭示问题”层面，未探索如何重新设计标注指南或任务定义以提升质量。

2. **人类基线的可靠性假设**：框架隐含假设人类标注者的一致性是“金标准”，但论文自身的发现挑战了这一假设——当情绪分类的标注者一致性仅为κ=0.39时，人类表现（45.8%）本身的可信度也值得质疑。这引发了一个递归问题：当人类都难以达成共识时，什么才是“正确”的评估基准？

3. **LLM标注者的排除限制**：聚类任务因“难以从生成式模型中引出聚类分配”而被排除在LLM-as-annotator评估之外。这一排除限制了结论的推广性，因为聚类恰恰是模型表现远超人类（如ArXiv聚类84.6% vs 49.2%）且数据集质量问题最突出的任务类别。

4. **缺乏纵向维度**：HUME是一次性的人类评估快照，未追踪人类表现随时间的稳定性或学习效应。标注者是否会在重复标注中提高一致性？模型更新后的人机差距如何演变？这些问题未被探索。

### 开放问题

**基准设计方法论**：如何设计标注指南以在“减少内在模糊性”和“保留有意义的语义挑战”之间取得平衡？HUME的发现表明，高共识任务（如STS12，ρ=0.77）能提供更可靠的评估，但过度追求共识可能导致任务过于简单，失去对模型能力的区分力。

**文化理解的系统性差距**：模型在多语言、低资源环境中表现显著落后于人类（如阿拉伯语情感分析差距17.5个百分点），其根源是训练数据覆盖不足、文化语境建模缺失，还是多语言表示学习的根本性局限？HUME提供了现象层面的证据，但未深入分析机制。

**LLM标注者的改进空间**：LLM在重排序任务上显著落后于人类（78.0% vs 88.3%），但这一差距是否可通过微调、few-shot提示或思维链推理来缩小？当前评估仅使用零样本设置，未探索LLM标注能力的上限。

**自动化质量预测**：能否开发自动化指标来预测数据集的人类共识水平？如果可以在基准构建早期识别低共识任务（如通过标注者模拟或文本特征分析），就能在资源投入前过滤或重新设计问题。这一能力的建立将显著降低大规模基准构建的成本。

**人类分歧的信息价值**：当前框架将标注者分歧视为“噪声”，但人类分歧本身可能包含有价值的语义信息（如情绪分类中的混合情绪、论文聚类中的跨学科性）。如何设计评估框架以**利用而非消除**人类判断的多样性，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/HUME_Measuring_the_Human_Model_Performance_Gap_in_Text_Embedding_Tasks.pdf]]
