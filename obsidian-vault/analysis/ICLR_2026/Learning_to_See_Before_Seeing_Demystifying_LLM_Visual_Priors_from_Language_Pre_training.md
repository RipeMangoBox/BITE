---
title: "Learning to See Before Seeing: Demystifying LLM Visual Priors from Language Pre-training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Learning_to_See_Before_Seeing_Demystifying_LLM_Visual_Priors_from_Language_Pre_training.pdf
project_link: https://junlinhan.github.io/projects/lsbs/
code_link: null
openreview_forum_id: pfw176o1YJ
aliases:
- LVAPTDM
- LSBSDLVPFLPT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "语言预训练数据中推理类数据（代码、数学、学术）与视觉描述类数据（视觉概念、属性、关系）的混合比例。"
primary_logic: "视觉先验可分解为可分离的感知先验与推理先验。推理先验主要来自代码、数学等结构化推理语料，随比例增加逐步增强；感知先验从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可饱和。基于此，采用平衡的数据配比（例如mix6：约52%推理/14.8%视觉描述）能在不显著损害语言能力的前提下，显著提升多模态视觉问答性能。"
claims:
- "推理类数据比例从0%增至75%时，视觉推理任务性能持续提升，而视觉描述文本的性能增益快速饱和。"
- "General与OCR（感知类）性能间存在中度正相关(0.37)，Knowledge与Vision-Centric（推理类）间存在中度正相关(0.33)，而两个簇之间相关性弱或为负。"
- "推理先验在三种不同视觉编码器下均表现出通用提升，而感知先验的趋势则不具有一致性。"
- "移除指令微调中的感知数据导致感知类基准大幅下降，移除推理数据对感知任务影响微小，推理任务下降也较温和。"
---

# Learning to See Before Seeing: Demystifying LLM Visual Priors from Language Pre-training

> [!tip] 核心洞察
> 视觉先验可分解为可分离的感知先验与推理先验。推理先验主要来自代码、数学等结构化推理语料，随比例增加逐步增强；感知先验从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可饱和。基于此，采用平衡的数据配比（例如mix6：约52%推理/14.8%视觉描述）能在不显著损害语言能力的前提下，显著提升多模态视觉问答性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 未视先识：揭示语言预训练中LLM的视觉先验 |
| 英文题名 | Learning to See Before Seeing: Demystifying LLM Visual Priors from Language Pre-training |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=pfw176o1YJ) · [Project](https://junlinhan.github.io/projects/lsbs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | 面向视觉感知的LLM预训练数据混合策略 (Vision-Aware Pre-training Data Mixture) |
| Dataset | Multimodal VQA (16 benchmarks averaged), Vision-centric VQA |

> [!tip] 效果简介
> - Multimodal VQA (16 benchmarks averaged) 上，Overall VQA Accuracy 为 38.64，对比 37.32，变化 +1.32。
> - Vision-centric VQA 上，v-acc 为 33.3 (mix6)，对比 32.4 (mix0)，变化 +0.9。

## 概要

### 问题瓶颈

大语言模型（LLM）在纯文本预训练中会自发获得关于视觉世界的隐式知识——视觉先验（visual priors），但这一现象长期缺乏系统性分析。研究者不清楚哪些预训练数据成分驱动了何种视觉能力，导致无法有针对性地优化数据配比以高效提升下游多模态任务性能。

### 核心发现

本文通过超过100组受控实验，揭示了视觉先验由两个可分离的组件构成：**感知先验**（perception prior）与**推理先验**（reasoning prior）。两者的来源与增长模式截然不同：

- **推理先验**主要来自代码、数学、学术等结构化推理语料，随推理数据比例增加而持续提升，直至约75%才趋于饱和（Figure 4）。
- **感知先验**从网络爬取等广泛语料中扩散产生，仅需少量视觉描述文本即可饱和，过量增加并无额外增益。

基于此，采用平衡的数据配比（mix6：约52%推理类数据 / 14.8%视觉描述类数据）能在不显著损害语言能力的前提下，将多模态视觉问答（VQA）总体准确率从37.32提升至38.64（Table 3），视觉中心类VQA准确率从32.4提升至33.3（Table 2）。

### 方法定位

本研究属于**预训练数据工程与多模态能力归因分析**的交叉方向。与直接设计多模态架构或视觉编码器的工作不同，该方法聚焦于纯文本预训练阶段的数据构成对下游视觉能力的影响。其流程为：LLM纯文本预训练 → 视觉对齐（MLP投影器） → 监督微调，参考了Cambrian-1的适配管线（Tong et al., 2024a）。核心调控变量是预训练数据中推理类与视觉描述类内容的混合比例。

### 主要结果

- 在16个多模态VQA基准的平均准确率上，平衡配比模型（mix6）相比语言优先配比模型（mix0）提升+1.32个百分点（Table 3）。
- 推理先验在三种不同视觉编码器下均表现出一致的通用提升趋势，而感知先验的趋势则因编码器而异（Figure 6）。
- 消融实验表明，移除指令微调中的感知数据会导致感知类基准大幅下降，而移除推理数据对感知任务影响微小（Figure 7），进一步验证了两类先验的功能独立性。
- 在MLE-Bench的小物体感知（0-30%像素占比）上，用web-crawl预训练的3B模型持续表现最优，验证感知先验来源于多样化数据（Figure 8）。

### 问题背景：大语言模型的视觉能力之谜

近年多模态大语言模型（MLLM）的快速发展揭示了一个令人困惑的现象：仅经过纯文本预训练的大语言模型（LLM），在接入视觉编码器并进行少量视觉-语言指令微调后，竟能展现出可观的视觉理解能力。这表明LLM在语言预训练阶段已经隐式地获得了关于视觉世界的“先验知识”——即视觉先验（visual priors）。然而，这一现象背后的成因始终缺乏系统性的实证分析。

**核心瓶颈**在于：LLM在纯文本预训练中自发获得的视觉先验缺乏系统性分析，阻碍了研究者有针对性地优化预训练数据以高效提升下游多模态任务性能。具体而言，哪些类型的文本数据催生了视觉先验？视觉先验是否可以分解为若干可分离的子能力？这些子能力各自来源于何种数据？这些问题的悬而未决，使得多模态模型的预训练数据配比长期依赖经验试错，缺乏理论指导。

### 现有方法缺口

当前MLLM的主流构建范式遵循“预训练-对齐-微调”三阶段流程：首先在纯文本上预训练LLM，随后通过MLP投影器将冻结的视觉编码器特征对齐到LLM嵌入空间，最后在视觉-语言指令数据上进行监督微调。在此框架下，研究重心长期集中于视觉编码器架构、对齐策略和指令微调数据的优化，而**LLM预训练阶段的文本数据构成对下游视觉能力的影响**则被严重忽视。

具体而言，存在以下缺口：

1. **缺乏对视觉先验来源的因果归因**：现有工作虽观察到不同预训练语料训练出的MLLM视觉性能存在差异，但未系统区分各类数据（如代码、数学、网络爬取文本、视觉描述文本）对视觉能力的具体贡献。
2. **视觉先验的内部结构未被解构**：视觉能力是单一整体还是由多个可分离的子能力组成？各子能力是否对应不同的数据来源？这些问题尚未得到实证回答。
3. **缺乏面向视觉能力的数据配比指导**：实践中，预训练数据配比通常以语言能力（如困惑度、推理基准）为优化目标，未考虑对下游多模态性能的影响。

### 本文动机与核心思路

针对上述缺口，本文通过超过100组受控实验（消耗约500,000 GPU小时），系统揭示LLM视觉先验的成因与内部结构。核心思路是：

- **将视觉先验分解为感知先验（perception prior）与推理先验（reasoning prior）**，二者来源不同、性质各异。
- **推理先验**主要来自代码、数学、学术等结构化推理语料，随该类数据比例增加而逐步增强。
- **感知先验**从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可使其饱和。
- 基于此发现，提出**面向视觉感知的LLM预训练数据混合策略**，通过调整推理类数据与视觉描述类数据的比例（如将推理数据从33.1%提升至52.0%，视觉描述数据从21.7%降至14.8%），在不显著损害语言能力的前提下，显著提升下游多模态视觉问答性能。

本文的工作为理解LLM中隐式视觉知识的起源提供了实证框架，并为高效训练多模态模型提供了可操作的数据配比指导。

## 核心方法与创新机理

本工作的核心创新在于**揭示并解耦了LLM在纯文本预训练中自发获得的视觉先验**，并据此提出了一种**面向视觉感知的预训练数据混合策略 (Vision-Aware Pre-training Data Mixture)**。其关键洞察是：视觉先验并非单一整体，而是由**感知先验 (perception prior)** 与**推理先验 (reasoning prior)** 两部分构成，二者来源不同、可独立调节。

### 关键变更槽位

相较于注重语言能力的内部基线配比 **mix0**（推理类数据占33.1%，视觉描述类数据占21.7%），所提出的平衡配比 **mix6** 在两个关键数据维度上进行了系统性调整（Table 2）：

| 变更槽位 | 基线值 (mix0) | 提出值 (mix6) | 证据锚点 |
|----------|--------------|--------------|---------|
| 预训练数据中推理类内容占比 | 33.1% | **52.0%** | Table 2 |
| 预训练数据中视觉描述类内容占比 | 21.7% | **14.8%** | Table 2 |

这一调整背后的因果机制是：
- **推理先验**主要来自代码、数学、学术等结构化推理语料，随比例增加而逐步增强（Figure 4：推理数据比例从0%增至75%时，视觉推理任务性能持续提升）。
- **感知先验**从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可使其饱和（Figure 4：视觉描述文本的性能增益快速饱和）。

基于此，mix6 通过**提高推理数据占比、适度降低视觉描述数据占比**，在不显著损害语言能力的前提下（困惑度仅从13.46升至13.52，文本准确率从53.0%微降至52.7%），将视觉中心VQA准确率从32.4%提升至33.3%，获得最高的综合排名（Table 2）。

### 与基线方法的本质差异

mix0 代表传统的“语言友好型”配比，优先保障语言基准性能。而本工作提出的配比策略直接针对**视觉先验的可分解性**这一新发现进行优化：通过网格搜索（Table 1）确定视觉友好配比约为60%推理/15%视觉内容，再通过插值在语言能力与视觉能力之间找到平衡点mix6。这一策略将多模态VQA的16项基准平均准确率从37.32提升至**38.64**（+1.32，Table 3），验证了通过调控纯文本预训练数据即可高效提升下游多模态性能的可行性。

### 方法谱系与知识库定位

本工作属于**LLM预训练数据工程 × 多模态能力涌现**的交叉研究。其核心贡献在于提供了可操作的因果操纵变量（推理/视觉描述数据比例），而非依赖视觉-语言联合预训练或更大的视觉编码器。参考的MLLM适配流程采用**Cambrian-1 adapter pipeline**（Tong et al., 2024a），但本工作的创新点集中在适配之前的纯文本预训练阶段，因此与现有MLLM工作形成互补而非竞争关系。

本工作构建了一条从纯文本预训练到多模态视觉问答的完整实验流水线，用以系统性地剖析语言模型在“未见图像”之前便已内化的视觉先验。整条流水线包含三个严格解耦的阶段，其设计核心在于：**将视觉能力的来源归因于语言预训练数据，而非视觉编码器或指令微调过程**。

### 阶段一：纯文本语言模型预训练

采用 **Llama-3 风格**的纯解码器 Transformer 架构，在完全不接触任何图像或多模态数据的条件下，从 16 类不同来源的文本语料中进行预训练。默认实验配置为 3B 参数模型、30B tokens 训练量，同时覆盖从 340M 到 13B 参数的模型规模以验证可扩展性。这一阶段是本文的核心“因果旋钮”——通过精确控制预训练数据中推理类内容（代码、数学、学术文献）与视觉描述类内容（视觉概念、属性、空间关系描述）的混合比例，来操控 LLM 内部自发形成的视觉先验。

### 阶段二：视觉对齐

在冻结的 LLM 之上，接入一个可训练的 **MLP 投影器**，将预训练好的视觉编码器（默认使用 CLIP 系列）输出的图像特征映射到 LLM 的嵌入空间。此阶段仅训练投影器，LLM 和视觉编码器的参数均保持冻结，确保视觉对齐过程不会向 LLM 注入额外的视觉知识——LLM 在此阶段所能利用的，完全来自阶段一预训练中已编码的文本知识。

### 阶段三：监督微调

使用精心策划的视觉-语言指令数据对完整的多模态大语言模型进行监督微调，激活并适配其下游视觉问答能力。指令微调数据同样被划分为**感知类**与**推理类**两个子集，以便在消融实验中独立考察两类指令数据对最终性能的贡献。此外，研究者还引入了 **盲视觉指令微调** 作为一种探测工具：在微调时仅提供文本问题而不提供对应图像，用以揭示模型在多大程度上依赖纯语言捷径来“破解”视觉任务。

### 评估体系

下游视觉能力通过覆盖四个维度的 16 个 VQA 基准进行综合评估：**General**（通用场景理解）、**OCR**（文字识别与图表阅读）、**Knowledge**（知识密集型问答）和 **Vision-Centric**（视觉中心推理，如空间关系、物体计数、深度判断）。这一多维评估体系使得研究者能够将视觉先验进一步分解为**感知先验**（由 General 和 OCR 性能表征）与**推理先验**（由 Knowledge 和 Vision-Centric 性能表征）两个可分离的组分。

### 输入输出流

- **输入**：纯文本预训练语料（阶段一）→ 图像-文本对（阶段二）→ 视觉-语言指令数据（阶段三）
- **输出**：能够执行多模态视觉问答的 MLLM，其视觉能力可追溯至预训练数据的特定组分

这一框架的关键设计原则在于 **因果隔离**：视觉编码器在阶段三之前保持冻结，指令微调数据被分类控制，从而确保观察到的性能差异可明确归因于语言预训练阶段的数据配比选择。

### 流水线模块

本工作的核心实验管线由三个顺序模块构成，用于将纯文本LLM适配为多模态大语言模型（MLLM）：

- **LLM预训练**：使用Llama-3风格的语言模型（参数量从340M到13B，默认3B参数模型在30B tokens上训练），从16个数据源的纯文本语料中学习语言能力与视觉先验。预训练数据配比是本工作的核心调控变量。
- **视觉对齐**：通过一个MLP投影器将冻结的视觉编码器特征映射到LLM的嵌入空间，实现跨模态表示对齐。
- **监督微调**：在视觉-语言指令数据与纯语言指令数据的混合上进行微调，激活并适配下游视觉能力。

### 关键公式

**视觉-语言核对齐（Vision-Language Kernel Alignment）**

为量化LLM内部表征与视觉表征的跨模态对齐程度，本文引入了核对齐度量：

$$
K_{\mathrm{vision}}(i,j) = \langle f_{\mathrm{vision}}(x_i), f_{\mathrm{vision}}(x_j) \rangle
$$

$$
K_{\mathrm{lang}}(i,j) = \langle f_{\mathrm{lang}}(y_i), f_{\mathrm{lang}}(y_j) \rangle
$$

其中：
- $f_{\mathrm{vision}}(x_i)$ 和 $f_{\mathrm{vision}}(x_j)$ 分别为视觉模型对图像 $x_i$、$x_j$ 的特征表示；
- $f_{\mathrm{lang}}(y_i)$ 和 $f_{\mathrm{lang}}(y_j)$ 分别为语言模型对对应文本 $y_i$、$y_j$ 的特征表示；
- $\langle \cdot, \cdot \rangle$ 表示内积运算，用于计算样本对之间的相似度核矩阵。

该度量用于评估推理类数据比例变化时，语言表征与视觉表征之间对齐程度的变化趋势（见Figure 11）。实验表明，LLM-视觉对齐分数随推理数据比例增加呈总体正向但非单调的趋势。

> **注意**：本文未引入新的模型架构或训练公式，核心贡献在于预训练数据配比的系统性探索。上述核对齐公式为分析工具，而非模型组成部分。其他公式（如困惑度、准确率等标准评估指标）不再赘述。

## 实验与关键发现

### 核心发现：视觉先验的可分解性

通过大规模受控实验，本研究揭示了一个关键洞察：LLM在纯文本预训练中自发获得的视觉先验并非单一整体，而是可分解为**感知先验**与**推理先验**两个可分离的组分。这一分解的证据来自多维度分析：

**相关性证据**（Figure 5）：对16个VQA基准的性能进行相关性分析发现，General与OCR类别之间存在中度正相关（0.37），构成感知能力簇；Knowledge与Vision-Centric类别之间存在中度正相关（0.33），构成推理能力簇。而两个簇之间的相关性弱或为负，表明感知与推理能力在机制上相对独立。

**数据溯源证据**（Figure 4）：推理先验主要来自代码、数学、学术等结构化推理语料。当推理类数据比例从0%逐步增至75%时，视觉推理任务性能几乎单调上升。相反，感知先验从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可使性能饱和——继续增加视觉描述数据带来的增益极为有限。

**跨编码器通用性证据**（Figure 6）：在三种不同视觉编码器（CLIP、SigLIP、DFN）下，推理先验均表现出通用提升趋势：随着LLM预训练中推理数据比例增加，推理密集型VQA任务性能持续改善。而感知先验的趋势则因编码器而异，不具有一致性，进一步印证了感知能力更多依赖于视觉编码器特性及后续的视觉指令微调。

### 主实验结果

基于上述发现，研究从注重语言能力的基线配比（mix0）出发，通过插值搜索得到平衡配比（mix6）。mix0的数据构成为：50%网络爬取、2.5%百科全书、2.5%学术、20%文学、5%数学、20%代码；mix6则调整为约52%推理类内容、14.8%视觉描述类内容（Table 2）。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/009_Table_2.jpg]]
*Table 2: Deriving a data mixture for more vision-aware LLMs. This table details a series of 11 data mixtures, from mix0 (language-favorable blend) to mix10 (approximating the vision-favorable blend), all trained on a 3B-parameter LLM with 50B tokens. The results highlight a trade-off, with mix6 emerging as the most balanced mixture, achieving top-ranked overall performance by improving visual capabilities without a significant drop in language proficiency*

在3B参数规模、50B token预训练设定下，mix6取得了最高综合排名：视觉VQA准确率（v-acc）达到33.3%，相比mix0的32.4%提升0.9个百分点；文本准确率（t-acc）为52.7%，困惑度（ppl）为13.52，语言能力仅有微弱下降（Table 2）。

在完整的MLLM适配流程（视觉对齐+监督微调）后，平衡模型在16个VQA基准上的平均准确率达到38.64，相比语言偏好模型的37.32提升了1.32个百分点；同时语言困惑度从8.72降至7.49，表明视觉感知导向的预训练数据调整并未损害语言能力（Table 3）。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/013_Table_3.jpg]]
*Table 3: Performance comparisons of the Language-Favorable and Balanced models across both language and vision-language benchmarks. The table summarizes key language metrics (perplexity and accuracy) and provides average scores for a suite of vision tasks*

### 消融实验：感知与推理的指令微调依赖性

Figure 7的指令微调数据消融实验进一步揭示了两种先验在后期适配阶段的不同依赖模式：

- **移除感知指令微调数据**（50%或100%）导致感知类基准（General、OCR）大幅下降，说明感知能力高度依赖视觉指令微调阶段的显式训练。
- **移除推理指令微调数据**对感知任务影响微小，推理任务下降也较温和，表明推理能力在语言预训练阶段已基本建立，指令微调仅起到激活和适配作用。

这一发现与Figure 4的趋势一致：推理先验随预训练推理数据比例持续增长，而感知先验在少量视觉描述文本后即饱和，其最终性能更多由视觉编码器和指令微调决定。

### 感知先验的细粒度分析

MLE-Bench（Multi-Level Existence Bench）提供了按目标物体相对像素占比（0-30%、30-60%、60-100%）分层评估感知能力的视角（Figure 8）。结果显示：

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/014_Figure_8.jpg]]
*Figure 8: Performance of MLLMs on the Multi-Level Existence Bench (MLE-Bench). The left plot shows the overall accuracy for models pre-trained on 16 different single-source data types. Other plots detail performance on objects of varying relative sizes, from small (0-30% of image pixels) to medium (30-60%) to large (60-100%). The results demonstrate that pre-training on the broad and diverse web-crawl corpus is most effective in gaining perception prior, with its advantage being particularly pronounced for perceiving smaller objects*

- 使用网络爬取（web-crawl）数据预训练的3B模型在小物体（0-30%像素）感知上持续表现最优，验证了感知先验来源于多样化、广覆盖的语料。
- 单一来源数据预训练的模型在感知细粒度物体时表现明显不足，进一步支持了感知先验的“扩散性”来源假设。

### 失败模式与局限

1. **盲视觉指令微调的幻觉风险**：研究发现，盲视觉指令微调（Blind Visual Instruction Tuning）虽能提高VQA性能，但会诱导模型在缺乏图像输入时生成看似合理的幻觉答案（Table 6）。该方法不应作为标准实践，其性能提升实质上反映了模型利用语言先验“破解”视觉任务的能力。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/021_Table_6.jpg]]
*Table 6: Performance comparisons of the Lang-Favorable and Balanced models across both language and vision-language benchmarks with blind visual instruction tuning trick. The table summarizes key language metrics (perplexity and accuracy) and provides average scores for a suite of vision tasks, categorized as General, Knowledge, OCR & Chart QA, and Vision-Centric. It also shows the impact of applying our blind visual instruction tuning trick (+Blind). The blind tuning method provides an additional performance boost for both models*

2. **感知先验的增强瓶颈**：Figure 14的定性分析显示，单纯增加视觉描述文本并不一定培育更深层的感知理解——25%视觉数据配比的模型在颜色恒常性问题上给出了正确答案和合理推理，而更高视觉数据配比的模型反而提供了错误答案和有缺陷的解释。这表明感知先验的增强不能简单通过堆砌描述性文本实现。

3. **研究范围局限**：当前实验仅覆盖静态图像理解，未探索视频、三维场景等动态模态的视觉先验。此外，预训练文本中的社会偏见可能通过视觉先验传递到下游多模态模型，形成有害的视觉刻板印象，这一问题有待系统研究。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/016_Figure_10.jpg]]
*Figure 10: Qualitative impact of reasoning-centric data on visual reasoning tasks. The plot shows how varying the proportion of different reasoning-centric data categories in the pre-training mix impacts metrics of visual reasoning quality. Results indicate that more reasoning data leads to more coherent and detailed visual reasoning*

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_pfw176o1YJ/figures/020_Figure_12.jpg]]
*Figure 12: MLE Benchmark Examples. The figure provides examples from the MLE-Bench, illustrating how the dataset is partitioned based on the ground-truth object size from reference segmentation maps. For instance, in the 0-30 split, the target object (a fireplace) constitutes a small fraction of the image. In contrast, the 60-90 split features a correct object (grass) that covers a substantial portion of the image. Table 5: Model performance on the MLE-Bench. Results are reported in three splits based on object size in percentage (0-30, 30-60, 60-100), along with a weighted overall accuracy, evaluating the ability of different models to identify objects of varying sizes*

## 定位与知识库关联

### 1. 核心方法定位

本工作提出的**面向视觉感知的LLM预训练数据混合策略**，本质上是一种**数据为中心的视觉先验诱导方法**。其核心操作变量并非模型架构或训练算法，而是纯文本预训练阶段的数据配比——具体而言，是推理类数据（代码、数学、学术）与视觉描述类数据（视觉概念、属性、关系）的混合比例。这一策略通过调整预训练数据的组成，在不修改LLM架构的前提下，改变模型在纯文本训练中自发获得的隐式视觉先验的构成，从而间接提升下游多模态任务的性能。

该方法在MLLM构建流程中占据的位置是**预训练阶段的数据工程**，位于视觉对齐和指令微调之前。整个pipeline包含三个串行模块：① LLM预训练（Llama-3-style，从纯文本数据中学习语言与视觉先验）；② 视觉对齐（MLP投影器，将冻结的视觉编码器特征对齐到LLM嵌入空间）；③ 监督微调（视觉-语言指令数据，激活并适配视觉能力）。本工作的贡献集中在第一个模块——通过数据配比调控LLM预训练阶段所获得的视觉先验质量。

### 2. 与基线方法的关系

#### 2.1 内部基线：Language-favorable mixture (mix0)

mix0是本文设定的内部基线，代表注重语言能力的预训练配比，其组成为50%网络爬取、2.5%百科全书、2.5%学术、20%文学、5%数学、20%代码。该配比下，推理类内容占比33.1%，视觉描述类内容占比21.7%。mix0在纯语言任务上表现最优（文本准确率53.0%，困惑度13.46），但在视觉任务上并非最佳。

本文提出的平衡配比mix6通过从mix0向视觉友好配比（mix9/mix10）插值得到，将推理类占比提升至52.0%，视觉描述类降至14.8%。这一调整带来视觉推理性能的显著提升（Vision-centric VQA从32.4提升至33.3），同时语言能力仅有微弱下降（文本准确率从53.0%降至52.7%，困惑度从13.46升至13.52），实现了语言与视觉能力的平衡。

#### 2.2 参考的MLLM适配流程：Cambrian-1

本文采用的两阶段适配流程（视觉对齐+监督微调）参考了**Cambrian-1**（Tong et al., 2024a）的adapter pipeline。Cambrian-1提供了将预训练LLM转化为MLLM的标准框架，本文在此基础上进行实验，但核心创新在于对LLM预训练阶段数据配比的系统性研究，而非对适配流程本身的改进。

### 3. 知识贡献与谱系定位

#### 3.1 核心发现的知识增量

本工作在以下方面提供了此前未被系统分析的知识：

- **视觉先验的可分解性**：首次系统论证了LLM在纯文本预训练中获得的视觉先验可分解为感知先验与推理先验两个可分离的组分。这一发现通过VQA性能的相关性矩阵得到验证——General与OCR（感知类）间存在中度正相关（0.37），Knowledge与Vision-Centric（推理类）间存在中度正相关（0.33），而两个簇之间相关性弱或为负（Figure 5）。

- **推理先验的数据来源与缩放规律**：揭示了推理先验主要来自代码、数学等结构化推理语料，且随推理数据比例增加而逐步增强（0%→75%时视觉推理性能几乎单调上升）。这一规律在三种不同视觉编码器下均得到验证（Figure 6），表明推理先验具有跨视觉编码器的通用性。

- **感知先验的扩散性与饱和性**：发现感知先验从网络爬取等广泛语料中扩散产生，少量视觉描述文本即可使其饱和。使用web-crawl预训练的模型在MLE-Bench的小物体感知上持续表现最优（Figure 8），验证了感知先验来源于多样化数据而非专门的视觉描述文本。

#### 3.2 在MLLM研究谱系中的位置

本工作处于**LLM预训练数据工程**与**多模态能力涌现机制**的交叉地带。与关注视觉编码器设计、对齐策略或指令微调数据配比的现有工作不同，本文向上游追溯至LLM的纯文本预训练阶段，揭示了文本数据的构成如何通过隐式视觉先验影响下游多模态性能。这一视角补充了现有MLLM研究中“从视觉适配阶段开始优化”的主流范式，将优化窗口前移至LLM预训练阶段。

### 4. 适用边界

本方法的适用性受以下边界约束：

1. **模态边界**：研究仅局限于静态图像理解，未探索视频、三维场景等动态模态的视觉先验。视频理解所需的时序推理能力可能来自故事、文学等不同类型的文本数据，但本文未进行验证。

2. **模型规模边界**：主要实验基于3B参数的LLM（部分实验扩展至340M–13B），更大规模模型（如70B+）上视觉先验的分解规律和数据配比的最优解是否一致，尚需进一步验证。

3. **数据规模边界**：预训练token量设定为30B–50B，远小于当前主流LLM的万亿token级别。在大规模预训练场景下，视觉先验的饱和点和数据配比的最优值可能发生变化。

4. **语言边界**：实验基于英文语料，跨语言的视觉先验迁移特性未经验证。

### 5. 局限性与开放问题

#### 5.1 已识别的局限

- **盲视觉指令微调的风险**：本文引入的Blind Visual Instruction Tuning虽能提升性能，但会诱导模型在缺乏图像的情况下生成幻觉，不应作为标准实践。这一局限性在文中被明确标注。

- **社会偏见的潜在传递**：预训练文本数据中的社会偏见可能通过语言先验被下游多模态模型继承，形成有害的视觉刻板印象。本文未对此进行系统评估或提出缓解方案。

- **感知先验的增强瓶颈**：研究指出感知先验在少量视觉描述文本后即饱和，但未提出有效的独立增强方案。目前仅能通过维持多样化的网络爬取数据来保证感知先验的基本水平。

#### 5.2 开放问题

1. **表征层面的解耦机制**：推理先验与感知先验在模型内部表征层面如何精确解耦？是存在于不同的注意力头、不同的层，还是以更复杂的方式交织？这一问题对于设计更精细的数据策略至关重要。

2. **感知先验的独立增强**：能否通过更精细的数据配比（如特定类型的视觉描述文本、空间关系语料等）独立增强感知先验，而不仅仅依赖网络爬取数据的多样性？

3. **时序推理的文本来源**：视频理解所需的时序推理能力能从何种文本数据（如故事、文学、对话）中习得？这关系到本方法的模态扩展可行性。

4. **幻觉问题的根治**：盲视觉问答中的幻觉问题如何从根本上解决？是否需要在预训练阶段就引入某种形式的视觉-文本对齐约束？

5. **偏见的量化与缓解**：视觉先验是否会导致偏见加剧？如何量化这一效应，并在数据配比阶段进行主动缓解？

## 原文 PDF

![[paperPDFs/ICLR_2026/Learning_to_See_Before_Seeing_Demystifying_LLM_Visual_Priors_from_Language_Pre_training.pdf]]
