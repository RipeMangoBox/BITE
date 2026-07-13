---
title: "PosterIQ: A Design Perspective Benchmark for Poster Understanding and Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PosterIQ_A_Design_Perspective_Benchmark_for_Poster_Understanding_and_Generation.pdf
project_link: null
code_link: "https://github.com/ArtmeScienceLab/PosterIQ-Benchmark"
aliases:
- PB
- PosterIQ
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将海报设计分解为可独立评估的设计维度（OCR、字体、布局、风格、隐喻）并引入细粒度、可复现的指标，能够揭示不同能力短板，从而定向推动模型改进。
primary_logic: 海报设计是一种高度约束的视觉传播任务，不仅依赖于美学，更要求精确的文字识别、层次化布局推理、语义与风格的深度耦合以及创造性隐喻表达；现有模型在这些维度的整合上仍处于初期阶段。
claims:
- 商用模型在高层次推理任务上领先，但在整体评分中与人类判断的相关性极低（最高余弦相似度仅0.465），暴露出其作为自动评分器的敏感性不足。
- 字体生成是所有生成任务中的瓶颈，最高字体风格丰富度仅0.391，远低于构图生成最高0.866的分数，揭示出当前模型在微观排版控制上的严重缺陷。
- GPT-5 在意图理解上得分最高（0.824），Gemini-2.5-Pro 在构图理解上得分最高（0.802），表明不同商用模型已在高层设计语义上展现出专项优势。
- 在合成的简单与困难OCR设置之间，Qwen3-VL-8B 性能下降最小（∆=0.156），显示出更强的抗干扰鲁棒性。
---

# PosterIQ: A Design Perspective Benchmark for Poster Understanding and Generation

> [!tip] 核心洞察
> 海报设计是一种高度约束的视觉传播任务，不仅依赖于美学，更要求精确的文字识别、层次化布局推理、语义与风格的深度耦合以及创造性隐喻表达；现有模型在这些维度的整合上仍处于初期阶段。

| 字段 | 内容 |
|------|------|
| 中文题名 | PosterIQ：面向海报理解与生成的设计视角基准测试 |
| 英文题名 | PosterIQ: A Design Perspective Benchmark for Poster Understanding and Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.24078) · [Code](https://github.com/ArtmeScienceLab/PosterIQ-Benchmark) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | PosterIQ Benchmark |
| Dataset | Logo OCR, Font Matching, Composition Understanding, Dense Generation |

> [!tip] 效果简介
> - Logo OCR 上，Accuracy GPT-5 (0.952) vs Grok-4-fast (0.440) (+0.512)。
> - Font Matching 上，Normalized Score Claude-Sonnet-4.5 (0.699) vs MiniCPM-V-4.5 (-0.001) (+0.700)。
> - Composition Understanding 上，Points Score Gemini-2.5-Pro (0.802) vs Gemma-3n-c4b-it (0.504) (+0.298)。

## 概要

海报是视觉传播的核心媒介，要求精确的文字识别、层次化的布局推理、语义与风格的深度耦合以及创造性的隐喻表达。然而，当前多模态大模型（MLLM）和文本到图像生成模型在这些设计驱动任务中的能力尚未被系统评估。**PosterIQ** 正是为此提出的一个以设计视角驱动的基准，覆盖海报理解与生成两大模块，包含 7,765 个图像-标注实例和 822 个生成提示，横跨 24 种任务类型。

该基准的核心洞见在于：海报设计是一种高度约束的视觉传播任务，仅靠通用视觉-语言能力远远不够，必须将评估分解为可独立量化的设计维度——OCR、字体感知、布局推理、风格理解与意图沟通——才能揭示不同模型的真实能力短板。实验表明，当前最强商用模型在高层设计语义上已展现出专项优势（如 GPT-5 在意图理解上得分 0.824，Gemini-2.5-Pro 在构图理解上得分 0.802），但整体评分与人类判断的余弦相似度最高仅 0.465，暴露了其作为自动评分器的敏感性严重不足。生成端的瓶颈更为突出：字体风格丰富度最高仅 0.391，远低于构图生成的 0.866，揭示出模型在微观排版控制上的系统性缺陷。这些发现共同指向一个结论——现有模型在海报设计各维度的整合上仍处于初期阶段，设计驱动的严格约束远未被满足。



海报作为一种高度浓缩的视觉传播媒介，承载着信息传递、品牌塑造与审美表达的多重功能。从商业广告到文化活动，海报设计需要同时协调文字内容、排版层级、色彩风格与空间构图，使观众在极短时间内完成“注意—理解—记忆”的认知闭环。然而，这种跨模态、强约束的创作过程对自动化系统提出了严峻挑战：模型不仅需要准确识别图像中的文字，还必须理解字体选择背后的语义暗示、布局中的视觉层次，甚至解读隐喻性视觉修辞的传播意图。

近年来，多模态大模型（MLLM）和文本到图像生成模型在通用视觉理解与生成任务上取得了显著进展，但在设计驱动的场景中仍暴露出系统性不足。现有基准测试大多聚焦于自然场景的OCR或通用图像描述，缺乏对**排版语义、视觉层次、显著性控制与意图沟通**等设计核心要素的细粒度评估。这导致两个关键问题悬而未决：其一，我们不清楚当前模型在设计认知的哪些维度存在短板；其二，缺乏可复现的指标来定量衡量模型的设计能力差距，使得针对性的改进方向难以明确。

PosterIQ的提出正是为了填补这一空白。该基准将海报设计分解为一组可独立评估的设计维度——包括**OCR精度、字体感知、布局推理、风格理解与隐喻意图**——并引入细粒度、标准化的评估指标，旨在系统性地揭示不同MLLM与生成模型在设计驱动任务中的能力图谱。其核心洞察在于：海报设计远不止于美学层面的“好看”，而是一种高度约束的视觉传播任务，要求模型在文字识别、空间推理、语义耦合与创造性表达之间实现深度整合。当前模型在这些维度的整合上仍处于初期阶段，而PosterIQ正是为衡量这一整合水平提供了一把可量化的标尺。



## 核心方法与创新机理

PosterIQ 的核心创新在于将海报理解与生成从通用的视觉问答或图像生成框架中剥离，重新锚定在**设计驱动的多维度评估体系**上。与现有基准仅关注单一美学评分或简单文本识别不同，PosterIQ 将海报的设计质量系统性地分解为五个可独立量化、可定向优化的能力维度：**OCR 精度、字体感知、布局推理、风格理解与隐喻意图**。这一分解构成了基准的“因果旋钮”——通过揭示不同模型在各维度上的具体短板，而非仅给出一个模糊的综合分数，为模型改进提供了可操作的信号。

在方法设计上，PosterIQ 引入了两个关键的 changed slots：**理解模块与生成模块的紧耦合设计**，以及**面向设计约束的细粒度指标族**。理解模块并非简单的 VQA 集合，而是从 Logo OCR 到传统字体效果识别、从文本定位到视觉隐喻理解，构建了一条从低层感知到高层语义的完整认知链。生成模块则对应地覆盖密集内容生成、字体风格生成、风格生成、构图生成和意图生成五个维度，直接检验文本到图像模型在真实设计约束下的合成能力。这种“理解评估→生成诊断”的闭环结构，使得基准不仅是一个静态的排行榜，更成为一个可迭代的诊断工具——例如，实验证实通过 VLM 驱动的迭代式提示优化，可以在不使用人工设计提示的情况下显著提升生成海报的质量，直接验证了理解能力对生成的促进作用。

在评估机制上，PosterIQ 摒弃了单一的全局评分，转而采用任务特定的标准化得分族。例如，针对多项选择题的 K-Option Score 将随机猜测映射为 0，消除了选项数量带来的偏差；针对生成任务，采用 Point Score（关键点覆盖率）和 Richness（风格丰富度）等多维指标，分别捕捉内容的完整性与视觉的多样性。这种细粒度指标设计直接暴露了当前模型的系统性缺陷：商用模型在整体评分中与人类判断的余弦相似度最高仅 0.465，暴露出其作为自动评分器的敏感性严重不足；字体生成的最高风格丰富度仅 0.391，远低于构图生成最高 0.866 的分数，揭示出微观排版控制仍是所有生成任务中的核心瓶颈。



PosterIQ 将海报设计拆解为**理解**与**生成**两大耦合模块，构成一个闭环评估体系。理解模块为生成提供诊断信号，生成模块则反向验证理解能力的实际效用。

**理解模块**从底层感知到高层语义逐级递进：
1. **OCR 层**——包含 Logo OCR、真实海报 OCR、简单/困难 OCR 及多尺寸 OCR 五个子任务（共 3,005 条样本），测试模型在艺术字体、遮挡和尺度变化下的文字识别鲁棒性。
2. **字体感知层**——涵盖字体匹配、字体属性感知、传统字体效果识别和高级字体效果识别四个子任务（共 2,788 条样本），评估对排版语义的细粒度判别。
3. **布局推理层**——通过文本定位、布局生成、留白感知等六个空间推理任务，考察模型对视觉层次和构图结构的理解。
4. **高级设计理解层**——包括风格理解、意图理解、构图理解三项任务，直接测量模型对设计隐喻和传播意图的把握。
5. **整体评分任务**——要求模型给出全局质量评分，以余弦相似度衡量其与人类审美判断的一致性。

**生成模块**覆盖五个设计维度，通过 822 条生成提示评估文本到图像模型的综合设计能力：密集内容生成、字体风格生成、风格生成、构图生成和意图生成。每个维度均采用 Point Score（关键点覆盖率）作为核心指标，辅以丰富度等多维评判。

模块间的因果链路体现在：VLM 驱动的迭代式提示优化可利用理解模块的反馈自动改进生成质量，无需人工设计提示——这一机制直接将理解能力转化为生成增益，证实了基准的闭环设计逻辑。

### 补充图表

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the benchmark, which includes over a dozen tasks*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/011_Figure_5.jpg]]
*Figure 5: Benchmark statistics for understanding tasks (top) and generation tasks (bottom)*



PosterIQ 基准包含两大核心模块：**理解模块**与**生成模块**，辅以全局质量评分任务，构成对多模态大模型（MLLM）和文本到图像生成模型的系统性设计能力评估。

### 理解模块

理解模块覆盖三个递进层次的设计认知任务：

- **OCR 任务**：包含 Logo OCR、真实海报 OCR、简单 OCR、困难 OCR 和多尺寸 OCR 五个子任务，评估模型在艺术字体、透视变形、遮挡等干扰下的文字识别能力。
- **字体感知任务**：包含字体匹配、字体属性感知、传统字体效果识别和高级字体效果识别四个子任务，考察模型对字体风格、粗细、衬线等微观排版属性的判别能力。
- **布局推理任务**：包含文本定位、布局生成、布局比较和空白空间感知等六个空间推理子任务，评估模型对海报层次结构和视觉流的理解。
- **高级设计理解任务**：涵盖风格理解、构图理解和意图理解三个维度，测试模型对海报整体设计语义和传播意图的把握。

### 生成模块

生成模块覆盖五个维度的设计合成能力：

- **密集内容生成**：要求模型在给定布局约束下生成包含大量文本的海报。
- **字体风格生成**：评估模型对指定字体风格的复现和多样化表达能力。
- **风格生成**：考察模型对特定视觉风格（如极简主义、复古风）的迁移能力。
- **构图生成**：评估模型对指定构图模板的遵循程度。
- **意图生成**：测试模型将抽象传播意图（如“环保呼吁”）转化为视觉表达的能力。

### 全局评分任务

该任务要求模型对海报的整体设计质量进行打分，通过与人类专家评分的余弦相似度衡量模型审美判断与人类的一致性。

### 关键评估公式

PosterIQ 采用细粒度、可复现的指标设计，以下为各任务的核心公式：

**OCR 准确率** 衡量正确识别文本实例的比例，采用去除不可见字符后的精确匹配计算：

$$A C = \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \mathbb { 1 } \left( \hat { T } _ { i } = T _ { i } \right)$$

其中 $N$ 为文本实例总数，$\hat{T}_i$ 为预测文本，$T_i$ 为真值文本。

**词级召回率** 以五字符为单元衡量真值文本在预测中的覆盖比例：

$$W R = \frac { \sum _ { g \in G } \mathbb { 1 } \left( g \subseteq o u t p u t \right) } { | G | }$$

其中 $G$ 为真值文本的五字符单元集合。

**K 选项标准化得分** 将多项选择题的随机猜测映射为 0，完美准确率映射为 1，消除选项数量带来的偏差：

$${ \mathrm { S c o r e } } = \operatorname* { m a x } \left( 0 , { \frac { k \cdot a - 1 } { k - 1 } } \right)$$

其中 $k$ 为选项数量，$a$ 为原始准确率。

**布局 IoU** 衡量前 $n$ 个预测边界框与对应真值框的平均空间重叠度：

$$\mathrm { I o U } = \frac { 1 } { n } \sum _ { j = 1 } ^ { n } \frac { | { B } _ { j } ^ { \mathrm { p r e d } } \cap { B } _ { j } ^ { \mathrm { g t } } | } { | { B } _ { j } ^ { \mathrm { p r e d } } \cup { B } _ { j } ^ { \mathrm { g t } } | }$$

**整体评分余弦相似度** 衡量模型评分向量与人类评分向量在零中心化后的一致性：

$$\mathrm{Overall\ Rating} = \frac{\tilde{\mathbf{h}}^{\top} \tilde{\mathbf{m}}}{\|\tilde{\mathbf{h}}\|_2 \|\tilde{\mathbf{m}}\|_2}$$

其中 $\tilde{\mathbf{h}}$ 和 $\tilde{\mathbf{m}}$ 分别为零中心化后的人类评分向量和模型评分向量。

**点分制评分** 用于高级理解与生成任务，衡量在所有样本中被判定为充分覆盖关键点的样本比例：

$$\mathrm{Point\ Score} = \frac{N_{\mathrm{Yes}}}{N_{\mathrm{Total}}}$$

其中 $N_{\mathrm{Yes}}$ 为满足关键点覆盖要求的样本数，$N_{\mathrm{Total}}$ 为总样本数。



## 实验与关键发现

### 实验设置概览

PosterIQ基准共包含 **7,765个标注实例**用于理解任务和 **822个生成提示**，覆盖24种任务类型。理解部分涵盖5个OCR任务（3,005项：Logo OCR、真实海报OCR、简单OCR、困难OCR、多尺寸OCR）、4个字体感知任务（2,788项：字体匹配、字体属性、传统字体效果识别、高级字体效果识别）、6个空间推理任务、3个高级视觉设计任务以及1个整体评分任务（Section 4）。评估指标采用任务特定的标准化得分，多项选择题使用K-Option Score将随机猜测映射为0以消除选项数量偏差，生成任务结合多个MLLM评判与人工评估以避免单一自动评分器的系统性偏差。

### 理解任务主结果

#### OCR能力：闭源模型占据绝对优势，但鲁棒性分化明显

Table 1呈现了全面的OCR基准结果。在Logo OCR和真实海报OCR任务上，除Grok-4-fast外所有闭源模型准确率均接近0.9。**GPT-5**在Logo OCR上取得最高准确率 **0.952**，**Gemini-2.5-Pro**在真实海报OCR上取得最高准确率 **0.952**，而Grok-4-fast的Logo OCR准确率仅为0.440，差距达+0.512。

鲁棒性分析揭示了更关键的信息：通过对比简单OCR与困难OCR之间的性能差距（∆），**Qwen3-VL-8B**表现出最强的抗干扰鲁棒性，性能下降最小（∆=0.156），而部分模型在引入视觉干扰后性能急剧退化。此外，Claude-Sonnet-4.5和Qwen系列在多尺寸OCR任务中展现出最稳定的字体大小适应能力（Table 1 Std指标）。

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/002_Table_1.jpg]]
*Table 1: Comprehensive OCR benchmark results across multiple visual text recognition tasks. AC denotes the accuracy, and W R denotes the word-level recall rate. ∆ represents the performance gap between the simple and hard OCR settings, reflecting model robustness. Std denotes the standard deviation of W R across different font sizes, indicating stability*

#### 字体感知：高层语义识别远优于细粒度匹配

Table 2的字体任务对比显示，**Claude-Sonnet-4.5**在字体匹配上取得最高归一化得分 **0.699**，而MiniCPM-V-4.5仅为-0.001，差距达+0.700。这一极端分化表明，字体匹配需要模型具备精确的排版特征提取能力，而多数开源模型在此维度上几乎完全失效。相比之下，字体属性感知和字体效果识别任务的整体得分更高，说明模型在高层字体语义理解上远优于细粒度的字体实例匹配。

#### 高级设计理解：不同模型展现专项优势

Table 3的高级视觉设计理解结果显示，商用模型已在高层设计语义上展现出明确的专项优势分化：**GPT-5**在意向理解上得分最高（**0.824**），**Gemini-2.5-Pro**在构图理解上得分最高（**0.802**），GPT-5在风格理解上也取得最高分（**0.851**）。这种分化暗示不同模型架构可能擅长捕捉设计的不同维度——Gemini系列对空间关系更敏感，而GPT系列对语义意图的推理更强。

Table 4的布局推理任务进一步印证了这一趋势：Gemini-2.5-Pro在文本定位Top-1 IoU上取得 **0.491**，在所有闭源模型中领先。

#### 整体评分：自动评分器与人类判断的系统性鸿沟

Table 5的整体评分比较是本次实验最具揭示性的发现之一。尽管商用模型在各项子任务中表现优异，但当被要求对海报整体质量进行评分时，其与人类判断的余弦相似度最高仅为 **0.465**。这一低相关性暴露出当前MLLM作为自动评分器的根本性局限：模型能够识别孤立的设计元素，但无法像人类设计师那样整合多维度信息形成连贯的审美判断。该发现对依赖MLLM进行自动化设计评估的研究方向提出了严肃警示。

### 生成任务主结果

Table 6呈现了图像生成模型在五项评估任务上的性能。整体而言，生成任务的表现远低于理解任务，且不同维度之间存在显著的能力不均衡。

**Gemini-2.5-Flash-Image**在密集内容生成上取得最高Point Score **0.622**，Qwen-Image为0.464，差距+0.158。然而，字体生成是所有生成任务中的核心瓶颈：即使表现最好的Gemini-2.5-Flash-Image，其字体风格丰富度（Richness）也仅为 **0.391**，远低于构图生成的最高分0.866（Table 6）。这一悬殊差距揭示出当前文本到图像模型在微观排版控制上的严重缺陷——模型能够合理布局视觉元素，但无法精确控制字体风格、字间距、字体效果等排版细节。

风格生成和意图生成任务的中等得分进一步表明，模型在将抽象设计意图转化为具体视觉输出时，仍存在语义与风格耦合不足的问题。

### 理解到生成的迭代优化

Section 4.2报告的消融实验证实了一个重要假设：通过VLM驱动的迭代式提示优化，可以在不使用人工设计提示的情况下显著提升生成海报的质量（Fig. 4）。这一发现建立了理解能力与生成能力之间的因果桥梁——更强的设计理解直接转化为更精准的生成控制，为未来的联合优化框架提供了实证基础。

### 综合能力排名

Table 7汇总了各模型在理解任务上的平均得分（仅聚合与人类判断正相关的指标）。闭源商用模型整体领先，但开源模型在特定子任务上展现出竞争力。值得注意的是，没有任何单一模型在所有维度上全面领先，这与设计任务本身的多维性高度一致——海报设计需要同时满足文字识别、排版、布局、风格和意图等多个正交约束，而当前模型在这些维度的整合上仍处于初期阶段。

### 失败模式与局限

综合实验结果，可识别出以下系统性失败模式：

1. **排版控制的根本性缺陷**：字体生成丰富度最高仅0.391，表明模型无法可靠地生成具有特定风格属性的字体，这是当前生成模型在设计应用中最关键的瓶颈。
2. **审美判断的整合不足**：整体评分与人类判断的最高余弦相似度仅0.465，说明模型缺乏将多维度设计要素整合为连贯审美评价的能力。
3. **抗干扰鲁棒性分化**：OCR任务中不同模型在视觉干扰下的性能退化幅度差异显著，部分模型对复杂背景和艺术化字体极为敏感。
4. **细粒度字体匹配的普遍失效**：开源模型在字体匹配任务上得分接近随机水平，表明精确的排版特征提取能力仍是MLLM的共性短板。

需要指出的是，所测试的模型多为商业闭源系统，无法深入分析其内部推理机制，这限制了从基准结果直接导出可操作的架构改进方案。此外，数据集虽然覆盖了多种海报类型，但仍不能代表所有文化和设计风格，某些特定风格或隐喻类型的样本较少，相关结论的外推需要谨慎。

### 补充图表

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/003_Table_2.jpg]]
*Table 2: Comparison of Font tasks across models*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/004_Table_3.jpg]]
*Table 3: Results of Understanding*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/005_Table_4.jpg]]
*Table 4: Comparison of layout reasoning tasks across models*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/006_Table_5.jpg]]
*Table 5: Comparison of Overall Rating*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/007_Table_6.jpg]]
*Table 6: Performance of image generation models across five evaluation tasks. Point Score(P S), Score(S), Richness(R)*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/009_Figure_3.jpg]]
*Figure 3: Qualitative comparison of four models on five generation tasks*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/010_Table_7.jpg]]
*Table 7: Average scores across understanding tasks. The average is computed by aggregating only these positively correlated scores*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/053_Figure.jpg]]
*Figure: Style Generation Results*

![[assets/figures/papers/paper_list_l772_https_arxiv_org_abs_2603_24078/figures/054_Figure.jpg]]
*Figure: Composition Generation Results*



## 定位与知识库关联

PosterIQ 的核心定位并非提出新的模型架构，而是构建一个以**设计视角**为驱动的系统性评估基准，将海报理解与生成任务从通用视觉问答和文本到图像生成的模糊评价中剥离出来。其方法谱系可沿三条轴线展开：**任务定义的学科交叉性**、**评估范式的细粒度转向**，以及**与现有基准的差异边界**。

### 1. 与现有基准的差异边界

现有视觉理解基准（如 TextVQA、DocVQA）聚焦于通用场景或文档的文字识别与问答，而海报生成评估（如 DrawBench、T2I-CompBench）多关注物体属性绑定与空间关系。PosterIQ 的独特贡献在于将**设计传播学**的约束引入评估体系：它同时要求模型处理视觉层次（排版大小、位置、留白）、风格语义（色彩情绪、隐喻传达）与意图沟通（说服力、目标受众匹配）三个设计维度。这种“理解+生成”的双模块耦合设计，使得它能够揭示模型在单一任务中无法暴露的**跨能力整合瓶颈**——例如，一个在 OCR 任务中表现优异的模型，可能在字体风格匹配（Font Matching）上得分近乎随机（MiniCPM-V-4.5 的归一化得分仅 -0.001，见 Table 2），暴露出其视觉编码器对字形美学特征的感知盲区。

### 2. 评估范式的细粒度转向

PosterIQ 的评估方法论代表了从“全局质量评分”到“可归因能力诊断”的范式迁移。传统文本到图像评估常依赖单一审美分数或 CLIP 相似度，而 PosterIQ 将生成质量分解为五个独立维度（密集内容、字体风格、风格、构图、意图），并引入**Point Score**（$N_{\mathrm{Yes}}/N_{\mathrm{Total}}$）衡量关键设计点的覆盖率。这种分解具有可操作的诊断价值：Table 6 显示，所有模型在字体生成丰富度（Richness）上均表现最差（最高仅 0.391），而构图生成得分可达 0.866，这直接指向当前生成模型在**微观排版控制**上的结构性缺陷，而非整体生成能力的不足。此外，K-Option Score 的标准化设计（$\max(0, \frac{k \cdot a - 1}{k - 1})$）将随机猜测映射为 0，消除了选项数量对多项选择题得分的干扰，提升了跨任务可比性。

### 3. 适用边界与局限

PosterIQ 的设计视角既是其优势，也划定了适用边界。其数据集虽覆盖 7,765 个理解实例和 822 个生成提示，但海报类型和文化风格的多样性仍有限，某些特定隐喻或地域性设计语言可能未被充分代表。更关键的局限在于**评估链的依赖**：生成任务的评分严重依赖 MLLM 作为自动评判器。尽管 Table 5 显示商用模型在整体评分中与人类判断的最高余弦相似度仅为 0.465，这一低相关性恰恰暴露了当前自动评分器的敏感性不足——它们能捕捉粗粒度差异，但对高级审美和创造性意图的判断仍与人类专家存在系统偏差。这意味着，PosterIQ 的生成评估结果应被解读为“在现有自动评判器能力范围内的相对排序”，而非对生成质量的绝对裁决。

### 4. 开放问题与方法论启示

从 PosterIQ 暴露的能力断层中，可提炼出三个直接的方法论开放问题：

1. **设计规则的显式编码**：当前模型在字体生成和布局推理上的薄弱表现，提示需要探索能够显式编码网格对齐、视觉流、字体对比等设计规则的生成架构，而非仅依赖端到端的隐式学习。
2. **审美评判器的标定**：Table 5 的低余弦相似度表明，训练与人类设计专家审美判断高度一致的自动评分模型仍是一个开放挑战，这可能需要引入设计专业知识的监督信号或偏好对齐机制。
3. **隐喻传达的量化**：在保持可复现评估的前提下，如何更精确地量化隐喻和视觉修辞的传达效果，是连接计算评估与设计传播学的核心难题。

值得注意的是，PosterIQ 通过 VLM 驱动的迭代式提示优化，初步验证了“理解能力对生成具有直接促进作用”（Section 4.2, Fig. 4），这为未来将理解模块作为生成过程的在线反馈器提供了实证依据，但其泛化到更复杂设计场景的有效性仍需进一步检验。



## 原文 PDF

![[paperPDFs/CVPR_2026/PosterIQ_A_Design_Perspective_Benchmark_for_Poster_Understanding_and_Generation.pdf]]
