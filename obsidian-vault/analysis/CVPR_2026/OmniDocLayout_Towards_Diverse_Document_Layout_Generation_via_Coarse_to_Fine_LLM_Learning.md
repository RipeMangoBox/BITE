---
title: "OmniDocLayout: Towards Diverse Document Layout Generation via Coarse-to-Fine LLM Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OmniDocLayout_Towards_Diverse_Document_Layout_Generation_via_Coarse_to_Fine_LLM_Learning.pdf
project_link: null
code_link: "https://github.com/rednotehilab/dots.ocr"
aliases:
- OL
- OmniDocLayout
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 两阶段 Coarse-to-Fine 学习范式：先在大规模多样化数据上学习粗粒度通用布局原则（对齐、避免重叠等），再用少量细粒度标注快速适应特定领域。
primary_logic: 不同文档类型虽然布局风格多样，但共享基本美学原则。先在多样化的粗粒度数据上学习这些通用空间组织规则，再向复杂细粒度领域迁移，可以大幅降低学习难度，仅需数百个样本即可有效适应。
claims:
- OmniDocLayout-LLM 在 M6Doc 五类文档（Textbook, Newspaper, Magazine, Exam, Academic）上全面超越现有布局生成专家和通用 LLM，U-Cond 任务 FID 降低至 36.48~41.82，远低于最强基线 LGGPT 的 154.20~197.81。
- 粗到细学习范式至关重要：只做粗粒度预训练即可大幅降低 Overlap，结合细粒度微调后细节更丰富，Full Coarse+Fine 在所有指标上均超越仅粗粒度或仅细粒度的变体。
- 人工评估显示，在 1,200 页上模型生成的边界框与人工标注质量相当（≥92% 的相似感知质量），验证了自动标注流水线的可靠性。
- M6Doc (Textbook, U-Cond) 上 FID = 40.28
---

# OmniDocLayout: Towards Diverse Document Layout Generation via Coarse-to-Fine LLM Learning

> [!tip] 核心洞察
> 不同文档类型虽然布局风格多样，但共享基本美学原则。先在多样化的粗粒度数据上学习这些通用空间组织规则，再向复杂细粒度领域迁移，可以大幅降低学习难度，仅需数百个样本即可有效适应。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniDocLayout: 面向多样化文档版面生成的粗到细LLM学习 |
| 英文题名 | OmniDocLayout: Towards Diverse Document Layout Generation via Coarse-to-Fine LLM Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.26213) · [Code](https://github.com/rednotehilab/dots.ocr) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | OmniDocLayout-LLM |
| Dataset | M6Doc |

> [!tip] 效果简介
> - M6Doc (Textbook, U-Cond) 上，FID 40.28 vs 197.81 (LGGPT) (-157.53)。
> - M6Doc (Newspaper, C→S+P) 上，FID 10.71 vs 167.39 (LGGPT) (-156.68)。
> - M6Doc (Magazine, C+S→P) 上，FID 20.74 vs 169.95 (LGGPT) (-149.21)。

## 概述

现有文档布局生成面临双重瓶颈：**数据层面**，主流数据集（如PubLayNet）严重偏向学术论文等简单布局，真实世界中报纸、杂志等复杂文档类型样本稀少；**模型层面**，现有生成方法难以处理每页元素数量多、类别细粒度高的长序列布局，导致生成质量急剧下降。

针对上述挑战，本文提出**OmniDocLayout-LLM**，一个基于0.5B参数大语言模型的统一布局生成框架。其核心创新在于**粗到细（Coarse-to-Fine）两阶段学习范式**：首先在大规模多样化数据上学习粗粒度的通用布局原则（对齐、避免重叠等空间组织规则），再通过标签映射机制用少量细粒度标注快速适应特定领域。这一设计的核心洞察是：不同文档类型虽然布局风格多样，但共享基本的美学原则——先在多样化粗粒度数据上掌握这些通用规则，再向复杂细粒度领域迁移，可大幅降低学习难度。

为支撑上述范式，本文还构建了**OmniDocLayout-1M**数据集，涵盖6种常见文档类型、约100万样本、4800万元素实例，在规模和多样性上远超现有数据集。

在M6Doc基准的五类文档（教科书、报纸、杂志、试卷、学术论文）上，OmniDocLayout-LLM全面超越现有布局生成专家模型和通用大语言模型：在无条件生成（U-Cond）任务上，FID降至36.48~41.82，而最强基线LGGPT为154.20~197.81，降幅超过150点。消融研究证实，完整的粗到细学习策略在所有指标上均大幅优于仅粗粒度预训练或仅细粒度微调的变体，且0.5B轻量模型即可取得有竞争力的结果，无需更大的模型规模。

## 背景与动机

### 问题背景：从简单布局到复杂文档的鸿沟

文档版面生成（Document Layout Generation）旨在自动预测页面内各元素（文本块、表格、图片、标题等）的类别与空间位置，是自动化文档合成、版面设计与智能排版的核心技术。近年来，基于扩散模型（如 **LayoutDM**、**LACE**）和大语言模型（如 **LayoutPrompter**、**LGGPT**）的布局生成方法取得了显著进展，但这些工作几乎完全建立在以学术论文为主的数据集（如 PubLayNet）之上。

然而，真实世界的文档类型远比学术论文复杂。以 M6Doc 基准涵盖的五类文档为例——教科书（Textbook）、报纸（Newspaper）、杂志（Magazine）、试卷（Exam）和学术论文（Academic）——其布局复杂度与 PubLayNet 存在本质差异。如 Figure 6 所示，复杂文档类型每页的最大元素数量和平均元素数量均远高于 PubLayNet，且元素类别粒度更细（例如报纸中需要区分标题、副标题、导语、正文等多种文本子类，而非简单的“text”标签）。这种**长序列、细粒度、多风格**的布局模式对现有方法构成了严峻挑战。

### 现有方法的瓶颈

当前文档版面生成面临两个相互交织的核心瓶颈：

**（1）数据瓶颈：布局多样性严重不足。** 现有布局数据集（如 PubLayNet 仅含 36 万样本且几乎全为学术论文，DocBank 仅含 50 万样本且文档类型陈旧）在文档类型覆盖和元素类别粒度上均存在显著局限。如 Table 1 所示，这些数据集缺乏报纸、杂志、幻灯片等复杂真实文档类型的代表性样本，导致模型难以学习到通用的空间组织原则。

**（2）模型瓶颈：长序列布局建模能力不足。** 复杂文档每页可能包含数十个甚至上百个元素，且需要精细区分多达 25-42 个类别。现有布局生成专家模型（如基于扩散的 LayoutDM、LACE 和基于 LLM 的 LGGPT）在 M6Doc 复杂文档类型上的 FID 指标高达 154-198（见 Table 2），表明其在处理高元素密度和细粒度类别时存在严重的模式坍塌和空间混乱问题。通用大模型（如 GPT-4o、Gemini-2.5-Flash、Claude-3.7-Sonnet）在零样本/少样本设置下同样表现不佳，难以准确理解复杂布局的空间约束。

### 核心洞察与本文动机

尽管不同文档类型的布局风格千差万别，但它们在底层共享一套基本的**美学原则**——元素对齐、避免重叠、合理的空间留白与视觉层次。本文的核心洞察在于：**如果能让模型先在海量多样化数据上学习这些通用的空间组织规则，再以少量细粒度标注快速适应特定复杂领域，就能大幅降低学习难度。**

基于这一洞察，本文提出 **OmniDocLayout-LLM**，一个仅 0.5B 参数的轻量级布局生成模型，配合两阶段 **Coarse-to-Fine（粗到细）学习范式**：
- **第一阶段**：在百万级多领域数据集 OmniDocLayout-1M 上使用粗粒度统一标签集（如 text, table, image 等）进行预训练，使模型掌握跨文档类型的基本布局原则；
- **第二阶段**：通过标签映射函数 $\phi$ 将粗粒度类别展开为领域特定的细粒度子类别（如 text → {paragraph, lead, ordered list}），仅需数百个目标域样本即可完成领域适应。

这一范式的关键优势在于：粗粒度预训练阶段的数据获取成本低（可借助自动标注流水线大规模构建），而细粒度适应阶段仅需极少量人工精标数据，实现了**数据效率与生成质量的最优平衡**。

## 核心创新

OmniDocLayout-LLM 的核心创新在于提出了一种**粗到细（Coarse-to-Fine）的两阶段 LLM 学习范式**，系统性地解决了复杂文档布局生成中数据稀缺与布局复杂度高两大瓶颈。与传统方法直接在有限目标域数据上微调或进行少样本提示不同，该工作通过三个关键 changed slots 实现了突破。

### 1. 训练策略：从单域微调到两阶段 Coarse-to-Fine 学习

现有布局生成方法（如 LayoutDM、LACE、LGGPT）通常直接在目标域的细粒度标注数据上进行训练，但真实世界复杂文档（如报纸、杂志）的高质量标注样本极为稀少，导致模型难以学习到有效的布局规律。

OmniDocLayout-LLM 将学习过程解耦为两个阶段：
- **Stage 1 — 粗粒度预训练**：在百万级多样化数据集 OmniDocLayout-1M 上，使用统一的粗粒度类别标签（如 text、table、image、title 等），让 LLM 学习跨文档类型通用的布局美学原则——对齐、避免重叠、空间组织等基本规则。
- **Stage 2 — 细粒度适应**：利用少量目标域细粒度标注数据（如 M6Doc 的 25-42 类），通过标签映射函数 $\phi: \mathbb{C}_{\mathrm{coar}} \to \mathbb{C}_{\mathrm{fine}}$ 将粗粒度类别展开为领域特定的细粒度子类别，实现快速领域迁移。

这一设计的核心洞察在于：**不同文档类型虽然布局风格迥异，但共享底层空间组织原则**。先在多样化数据上掌握这些通用规则，再向特定领域迁移，可大幅降低学习难度。消融实验（Table 4）强有力地证实了这一点：仅粗粒度预训练即可显著降低 Overlap 指标，而完整的 Coarse + Fine 策略在所有指标上均大幅超越仅粗粒度或仅细粒度的变体。

### 2. 标签粒度：从直接细粒度学习到粗-细粒度解耦

传统方法直接在细粒度类别空间（如 25-42 类）上进行学习，面临类别数量多、样本分布稀疏的挑战。OmniDocLayout-LLM 通过**标签粒度的解耦设计**改变了这一范式：

- 预训练阶段使用统一的粗粒度标签集，使模型专注于学习空间布局的结构性规律，而非特定类别的细节差异。
- 微调阶段通过映射 $\phi$ 将粗粒度类别扩展为细粒度后代类别（例如 text → {paragraph, lead, ordered list}），仅需数百个样本即可有效适应新领域。

这种设计使得模型能够利用大规模粗粒度数据学习可迁移的布局知识，同时保持对细粒度领域的高效适应能力。

### 3. 数据规模与多样性：从单域小样本到百万级多域数据集

现有布局数据集（如 PubLayNet）严重偏向学术论文等简单布局类型，样本量通常不足 10K，难以支撑复杂文档布局生成任务的学习。OmniDocLayout-1M 数据集从根本上改变了这一局面：

- **规模**：约 100 万样本，4800 万元素实例
- **多样性**：覆盖 6 种常见文档类型（教科书、报纸、杂志、试卷、学术论文等），来自 36 个数据源
- **标注质量**：通过自动标注流水线生成，人工评估显示在 1200 页上模型生成的边界框与人工标注质量相当（≥92% 的相似感知质量）

这一大规模、多样化的数据集为粗粒度预训练提供了坚实基础，使得模型能够在接触少量细粒度标注前，已掌握丰富的通用布局知识。

### 创新总结

三项 changed slots 形成了协同效应：大规模多样化数据提供了学习通用布局原则的基础，粗粒度标签集降低了学习难度，两阶段训练策略实现了从通用知识到领域特化的高效迁移。这一组合使得仅 0.5B 参数的轻量模型即可在 M6Doc 五类文档上全面超越现有布局生成专家和通用 LLM，U-Cond 任务的 FID 降至 36.48-41.82（最强基线 LGGPT 为 154.20-197.81）。

## 整体框架

OmniDocLayout-LLM 将复杂文档布局生成建模为统一令牌空间上的条件序列生成任务。其整体框架由三个核心组件串联而成：**Base Prompt 编码器**、**Condition Prompt 构造器**与**Task Prompt 描述符**，三者拼接后送入一个自回归解码器完成布局序列的逐令牌生成（Figure 3）。

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/005_Figure_3.jpg]]
*Figure 3: Overview of our layout generation framework (OmniDocLayout-LLM). Left: The unified layout prompt consists of a Base Prompt (document metadata), a Condition Prompt for U-Cond, C→S+P, C+S→P, Completion, and Refinement, and a Task Prompt defining the layout objective. Right: A Coarse-to-Fine Mapping*

### 输入表示与序列化

给定一页文档，其布局被形式化为一组五元组的集合：

$$\mathcal { L } = \{ e _ { i } = ( c , x , y , w , h ) \mid i = 1 , \ldots , N \}$$

其中 $c$ 为元素类别，$(x, y)$ 为归一化坐标，$w, h$ 为归一化的宽高。每个布局元素 $e_i$ 通过基于字符串的前缀感知编码（String-based Layout Tokenizer）序列化为：

$$<|cat start|>c<|cat end|><|box start|>0x\ 1y\ 2w\ 3h<|box end|>$$

坐标与尺寸被量化到 $[0, 999]$ 的离散区间，与类别标签共享统一的词汇表空间，从而将结构化布局转化为自回归模型可直接处理的离散令牌序列 $T = (t_1, t_2, ..., t_K)$。

### 提示构造与生成流程

页面级的布局生成提示由三部分拼接而成：

1. **Base Prompt**：编码文档元数据，包括文档类型、画布尺寸、当前页应生成的边界框数量以及有效类别集合等全局约束。
2. **Condition Prompt**：根据具体生成任务动态构造。框架统一支持五种任务范式——无条件生成（U-Cond）、类别到尺寸与位置（C→S+P）、类别与尺寸到位置（C+S→P）、布局补全（Completion）和布局精炼（Refinement）。不同任务对应不同的条件信息（如已知类别时仅提供类别序列，已知类别与尺寸时提供二者），由 Condition Prompt Constructor 负责组装。
3. **Task Prompt**：以自然语言指令描述当前布局生成任务的目标，引导模型理解任务语义。

三者拼接形成统一布局提示后，送入基于 **Qwen2.5-0.5B-Instruct** 的自回归解码器，模型按令牌顺序生成完整布局序列，最终解析为边界框集合。

### 粗到细学习范式

框架的训练策略是其区别于现有方法的核心设计。传统方法直接在有限的目标域细粒度标注数据上训练，而 OmniDocLayout-LLM 采用两阶段 **Coarse-to-Fine** 学习范式：

- **阶段一（粗粒度预训练）**：在百万级多样化数据集 OmniDocLayout-1M 上，使用统一的粗粒度标签集（如 text, table, image, title 等）进行预训练。此阶段的核心目标是让模型习得跨文档类型通用的布局美学原则——元素对齐、避免重叠、合理的空间组织等。
- **阶段二（细粒度适应）**：通过标签映射函数 $\phi : \mathbb { C } _ { \mathrm { c o a r } } \to \mathbb { C } _ { \mathrm { f i n e } }$，将粗粒度类别展开为目标域的细粒度子类别（例如 text → {paragraph, lead, ordered list}），仅需数百个细粒度标注样本即可快速适应特定文档领域。

这种设计的核心洞察在于：不同文档类型的布局风格虽差异显著，但共享底层的空间组织规则。先在多样化数据上学习这些通用原则，再向复杂细粒度领域迁移，可大幅降低学习难度。消融实验证实，仅粗粒度预训练即可显著降低元素重叠（Overlap），而细粒度微调在此基础上进一步丰富类别级细节，完整的 Coarse + Fine 策略在所有指标上均大幅优于任一单独阶段（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/001_Figure_1.jpg]]
*Figure 1: Overview of OmniDocLayout. (Top & Middle) show the curation process and examples of OmniDocLayout-1M. (Bottom) illustrates diverse layouts unconditionally generated by our OmniDocLayout-LLM*

## 核心模块与公式推导

### 布局的数学表示

OmniDocLayout-LLM 将文档布局建模为一组布局元素的集合。每个元素 $e_i$ 包含语义类别和空间位置信息，形式化为五元组：

$$\mathcal{L} = \{ e_i = (c, x, y, w, h) \mid i = 1, \ldots, N \}$$

其中 $c$ 表示元素类别（如 text、table、image），$(x, y)$ 为边界框的左上角或中心点坐标，$w$ 和 $h$ 分别表示宽度和高度。这种统一的数值化表示构成了模型输入输出的基础数据结构（Section 4.1, Equation 1）。

### 粗到细学习范式的数学框架

核心创新在于两阶段 Coarse-to-Fine 学习策略的形式化定义。粗粒度预训练阶段，模型在多样化文档类型集合上学习通用布局原则：

$$\mathbb{D}_{\mathrm{coar}} = \{ D_{\mathrm{coar}}^{(m)} \}_{m=1}^{M}$$

其中每个子集 $D_{\mathrm{coar}}^{(m)}$ 对应一种文档类型（如教科书、报纸、杂志），使用统一的粗粒度标签集 $\mathbb{C}_{\mathrm{coar}}$（Section 4.1, Equation 2）。这一阶段的训练目标是让 LLM 掌握对齐、避免重叠等跨域共享的空间组织规则。

细粒度适应阶段引入标签映射函数 $\phi$，将粗粒度类别展开为领域特定的细粒度类别：

$$\phi : \mathbb{C}_{\mathrm{coar}} \to \mathbb{C}_{\mathrm{fine}}$$

例如，粗粒度类别 `text` 通过 $\phi$ 映射为 `{paragraph, lead, ordered list}` 等细粒度子类。这一映射机制使得模型仅需数百个细粒度标注样本即可快速适应目标领域，大幅降低了学习难度（Section 4.3）。

### 基于字符串的布局序列化

模型将布局元素序列化为统一令牌空间中的离散序列。每个元素 $e_i = (c, x, y, w, h)$ 被编码为前缀感知的字符串格式：

```
<|cat start|>c<|cat end|><|box start|>0x 1y 2w 3h<|box end|>
```

其中类别 $c$ 由特殊标记 `<|cat start|>` 和 `<|cat end|>` 包裹，坐标和尺寸 $(x, y, w, h)$ 被归一化到 $[0, 999]$ 区间后由 `<|box start|>` 和 `<|box end|>` 包裹，数字前缀 `0`、`1`、`2`、`3` 分别指示坐标维度（Section 4.2）。完整的页面布局 $\mathcal{L}$ 被序列化为令牌序列 $T = (t_1, t_2, \ldots, t_K)$，其中 $K$ 为序列长度。

### 统一布局提示构建

页面级布局生成提示由三个组件拼接而成（Figure 3, Section 4.2）：

1. **Base Prompt Encoder**：编码文档元数据，包括文档类型、画布尺寸、边界框数量、有效类别集等全局信息。
2. **Condition Prompt Constructor**：根据不同生成任务构造对应的条件序列。框架支持五种任务模式——无条件生成（U-Cond）、类别到尺寸+位置（C→S+P）、类别+尺寸到位置（C+S→P）、布局补全（Completion）和布局精炼（Refinement）。
3. **Task Prompt**：以自然语言指令描述当前布局生成任务的具体目标。

三者拼接后送入基于 Qwen2.5-0.5B-Instruct 的自回归解码器，在统一令牌空间中以自回归方式逐令牌生成完整布局序列（Section 5.1）。

## 实验与分析

### 核心瓶颈与评估框架

现有文档布局生成面临双重挑战：**数据侧**，主流数据集（如 PubLayNet）严重偏向学术论文等简单布局，真实世界中报纸、杂志等复杂文档类型样本稀少；**模型侧**，当每页元素数量多、类别细粒度高时，现有生成模型难以处理长序列布局。为系统评估，作者在 **M6Doc** 基准上覆盖五类文档（Textbook, Newspaper, Magazine, Exam, Academic），并设计五种生成任务：无条件生成（U-Cond）、类别→尺寸+位置（C→S+P）、类别+尺寸→位置（C+S→P）、布局补全（Completion）和布局优化（Refinement）。评估指标包括 FID（越低越好）、mIoU、Alignment 和 Overlap。

### 主实验结果

**与领域专家模型对比（Table 2）**：OmniDocLayout-LLM 在所有五类文档、所有任务上全面超越现有布局生成专家模型，且优势幅度巨大。以 U-Cond 任务为例，模型 FID 降至 36.48~41.82，而最强基线 **LGGPT**（LLM-based, string-based modeling）的 FID 高达 154.20~197.81，降幅超过 150 点。在 C→S+P 任务上，Newspaper 类型 FID 仅 10.71（LGGPT 为 167.39）；在 Refinement 任务上，Exam 类型 FID 仅 6.66（LGGPT 为 153.79）。基于扩散的专家模型（**LayoutDM**、**LACE**）同样被大幅超越，说明 LLM-based 序列建模结合粗到细学习范式的有效性远超传统生成范式。

**与通用大模型零样本对比（Table 3）**：将 OmniDocLayout-LLM 与 **GPT-4o**、**Gemini-2.5-Flash**、**Claude-3.7-Sonnet** 等通用 LLM 在零样本设定下对比，专用模型在所有文档类型和指标上均显著领先。通用 LLM 即便拥有强大的通用推理能力，在缺乏专门布局训练时仍难以生成符合美学原则的复杂文档布局。

### 消融研究

**粗到细学习范式的关键作用（Table 4）**：消融实验对比了三种训练策略——仅粗粒度预训练（C）、仅细粒度微调（F）、完整两阶段 Coarse + Fine。结果表明：
- **仅粗粒度预训练**已能强烈改善全局布局组织，Overlap 指标显著下降，证明多样化粗粒度数据上学习的通用空间组织原则（对齐、避免重叠等）具有强迁移性；
- **仅细粒度微调**缺乏粗粒度基础，性能明显不足；
- **完整两阶段（Coarse + Fine）**在所有指标上均超越单一阶段变体，粗粒度阶段提供全局结构基础，细粒度阶段补充领域特定的元素级细节。

**模型规模的影响（Table 4）**：将骨干 LLM 从 Qwen2.5-0.5B 扩展到 3B 参数，性能提升有限。0.5B 轻量模型即可取得有竞争力的结果，表明粗到细学习范式的有效性不依赖于大规模参数，具有良好的部署友好性。

### 人工评估验证

为验证自动标注流水线的可靠性，作者在 1,200 页文档上进行盲测人工评估（Figure 7），对比模型生成的边界框与人工标注的感知质量。结果显示 ≥92% 的样本上模型标注与人工标注具有相似的感知质量，支撑了 OmniDocLayout-1M 数据集的质量可信度。

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/012_Figure_7.jpg]]
*Figure 7: Human evaluation of 1,200 pages comparing model-generated and human-annotated layouts. “Pred” refer to the bounding box predicted by MinerU [37]*

### 失败模式与局限

当前自动评估指标（如 FID、mIoU）在评估复杂布局且样本有限的情况下可能不够准确，无法完全反映生成布局的感知质量。此外，尽管模型在 M6Doc 五类文档上表现优异，但在更极端的长尾文档类型或具有特殊排版规则的领域（如古籍、乐谱）上的泛化能力仍需进一步验证。

### 开放问题

1. 如何在复杂文档布局生成任务中设计更可靠、更贴近人类感知的评估指标？
2. 随着通用大模型空间推理能力不断增强，少样本布局生成能否在不经过专门训练的情况下达到实用水平？

### 补充图表

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/006_Table_2.jpg]]
*Table 2: Comparison with Layout Generation Experts across Five Document Types in*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/007_Table_3.jpg]]
*Table 3: Comparison with Powerful General-purpose LLMs in 0-shot Setting across Five Document Types in M6Doc. For models, Gemini-2.5* and Claude-3.7* denote Gemini-2.5-Flash and Claude-3.7-Sonnet*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/009_Table_4.jpg]]
*Table 4: Ablation on Model Sizes and Learning Stages. F. and C. denote Fine-grained Adaptation and Coarse-grained Learning only, respectively*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/008_Figure_4.jpg]]
*Figure 4: Visualization Examples of Various Methods with U-Cond Task. For general-purpose LLMs, we adopt the strongest 5-shot setting*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/010_Figure_6.jpg]]
*Figure 6: Layout Complexity Comparison Between Five Complex Types in M6Doc and Widely-used PubLayNet. (Top) compares the maximum and average number of elements per page. (Bottom) compares the granularity of element categorization. The red dashed line indicates the default maximum number of elements (25) allowed in prior methods*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/002_Table_1.jpg]]
*Table 1: Comparison with Existing Layout Datasets. * indicates that most of the document types are outdated*

![[assets/figures/papers/paper_list_l2330_https_arxiv_org_abs_2510_26213/figures/003_Figure_2.jpg]]
*Figure 2: Statistical Analysis of OmniDocLayout-1M. (a) & (b) show the multi-dimensional diversity, (c) proves its consistency with prior knowledge*

## 方法谱系与知识库定位

### 任务定位与基线谱系

文档布局生成任务旨在自动预测页面中各类元素（文本、标题、表格、图像等）的类别与空间位置。现有方法可大致划分为两条技术路线：

**扩散模型专家**：以 **LayoutDM** 和 **LACE** 为代表的扩散式布局生成方法，将布局建模为连续空间中的去噪过程。这类方法在学术论文等简单布局上表现良好，但受限于训练数据的领域单一性，难以泛化到报纸、杂志等元素密集、类别细粒度高的复杂文档。

**LLM 基生成方法**：**LayoutPrompter** 采用上下文学习方式，通过少样本示例引导通用 LLM 生成布局；**LGGPT** 则首次将布局序列化为字符串格式进行自回归建模。这些方法初步验证了 LLM 在布局生成中的潜力，但在 M6Doc 基准上 FID 仍高达 154~197（Table 2），暴露出对复杂长序列布局建模能力的不足。

通用大模型方面，**GPT-4o**、**Gemini-2.5-Flash** 和 **Claude-3.7-Sonnet** 在零样本/少样本设置下同样表现不佳，其空间推理能力尚不足以直接处理高密度、多类别的精细布局生成任务（Table 3）。

OmniDocLayout-LLM 在方法谱系中的独特定位在于：**不依赖扩散过程的迭代去噪，也不依赖通用 LLM 的隐式空间推理能力，而是通过大规模多样化数据的粗粒度预训练，让轻量级 LLM 显式学习通用空间组织规则，再以标签映射实现细粒度领域适应。**

### 适用边界与关键前提

该方法在以下条件下表现出显著优势：

1. **目标域数据稀缺但存在粗粒度标注的大规模多样化数据**：OmniDocLayout-1M 提供了百万级、六种文档类型、36 个来源的粗粒度布局数据（Table 1），这是 Coarse-to-Fine 范式的前提。
2. **目标域与预训练域共享基本美学原则**：不同文档类型虽风格迥异，但均遵循对齐、避免重叠、信息密度合理等通用空间组织规则。Figure 6 展示了 M6Doc 五类复杂文档与 PubLayNet 在元素数量和类别粒度上的显著差异，但 Coarse 阶段学到的通用原则仍能有效迁移。
3. **轻量模型即可胜任**：消融实验表明，从 0.5B 扩展到 3B 参数带来的性能提升有限（Table 4），说明核心增益来自学习范式而非模型规模，这降低了部署门槛。

适用边界则体现在：当目标域文档的布局逻辑与预训练域存在根本性冲突（例如完全非结构化或艺术化排版）时，粗粒度预训练学到的通用原则可能无法有效迁移。此外，自动评估指标（FID、mIoU）在样本有限时可能无法准确反映感知质量，这一局限性在论文中已被明确指出。

### 局限与开放问题

**已确认的局限**：
- 当前自动评估指标（FID、mIoU）在复杂布局且样本有限的情况下可能不够准确，无法完全反映生成布局的感知质量。尽管人工评估在 1,200 页上验证了 ≥92% 的相似感知质量（Figure 7），但大规模自动评估的可靠性仍有待提升。

**开放问题**：
1. **感知对齐的评估指标设计**：如何在复杂文档布局生成任务中设计更可靠、更贴近人类感知的自动评估指标？这是该领域从实验走向实用的关键瓶颈。
2. **通用 LLM 空间推理能力的演进**：随着 GPT-4o、Gemini 等通用大模型空间推理能力的不断增强，少样本布局生成能否在不经过专门训练的情况下达到实用水平？这将决定专用布局生成模型在未来生态中的定位。
3. **Coarse-to-Fine 范式的泛化边界**：该范式假设所有文档类型共享通用空间组织原则，但这一假设在极端异质领域（如手写笔记、信息图表）是否仍然成立，需要进一步验证。

### 知识库贡献

OmniDocLayout 的核心知识贡献在于：
- **OmniDocLayout-1M 数据集**：百万级、六域、36 源的多样化文档布局数据，填补了现有数据集严重偏向学术论文的空白（Table 1）。
- **Coarse-to-Fine 学习范式**：验证了“先学通用原则，再适应特定领域”的有效性，仅需数百个细粒度样本即可实现领域迁移，为数据稀缺场景下的布局生成提供了可复用的方法论。
- **统一序列建模框架**：将布局生成统一为条件序列生成任务，支持无条件生成（U-Cond）、类别到位置（C→S+P）、类别+尺寸到位置（C+S→P）、补全（Completion）和精炼（Refinement）五种任务模式（Figure 3），为后续研究提供了灵活的实验基座。

## 原文 PDF

![[paperPDFs/CVPR_2026/OmniDocLayout_Towards_Diverse_Document_Layout_Generation_via_Coarse_to_Fine_LLM_Learning.pdf]]
