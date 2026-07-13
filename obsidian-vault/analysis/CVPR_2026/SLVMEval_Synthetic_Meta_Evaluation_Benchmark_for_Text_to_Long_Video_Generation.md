---
title: "SLVMEval: Synthetic Meta Evaluation Benchmark for Text-to-Long Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SLVMEval_Synthetic_Meta_Evaluation_Benchmark_for_Text_to_Long_Video_Generation.pdf
project_link: "https://slvmeval.github.io/"
code_link: "https://github.com/danielgatis/rembg"
aliases:
- SBC
- SLVMEval
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 视频时长与评估方面的类型（视频质量 vs 视频-文本一致性）是影响评估准确率的核心杠杆；退化操作的难易程度（人工判定）决定了评估系统的基本能力下限。
primary_logic: 通过合成退化并人工筛选的长视频元评估基准，可以系统地揭示现有评估系统在长视频评估上的根本缺陷；同时，过滤前后的系统排序高度相关，表明可在不依赖昂贵人工过滤的情况下持续扩展基准。
claims:
- 人工评估者在10个方面上的准确率为84.7%-96.8%，而现有自动评估系统在9个方面上均低于人类表现。
- 几乎所有的自动评估系统在视频时长增加时准确率下降，尤其体现在Background Consistency、Color和Temporal Flow等需要长程一致性的方面。
- 在过滤后与未过滤的基准上，各评估系统的准确率具有强相关性（Pearson相关性在多数方面较高），说明人工过滤步骤并非绝对必要。
- 基于文本的评估方式在特定模型（如Qwen3）的部分方面上较基于视频的方式有显著提升（Background Consistency +23.3, Appearance Style +17.1, Object Integrity +12.5）。
---

# SLVMEval: Synthetic Meta Evaluation Benchmark for Text-to-Long Video Generation

> [!tip] 核心洞察
> 通过合成退化并人工筛选的长视频元评估基准，可以系统地揭示现有评估系统在长视频评估上的根本缺陷；同时，过滤前后的系统排序高度相关，表明可在不依赖昂贵人工过滤的情况下持续扩展基准。

| 字段 | 内容 |
|------|------|
| 中文题名 | SLVMEval：面向文本到长视频生成的合成元评估基准 |
| 英文题名 | SLVMEval: Synthetic Meta Evaluation Benchmark for Text-to-Long Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29186) · [Project](https://slvmeval.github.io/) · [Code](https://github.com/danielgatis/rembg) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | SLVMEval Benchmark Construction |
| Dataset | SLVMEval - Aesthetics, SLVMEval - Technical Quality, SLVMEval - Object Integrity, SLVMEval - Comprehensiveness |

> [!tip] 效果简介
> - SLVMEval - Aesthetics 上，准确率（%） Human 96.5 ± 2.1 vs GPT-5 video 90.1 ± 2.5 (-6.4)。
> - SLVMEval - Technical Quality 上，准确率（%） Human 91.8 ± 4.7 vs GPT-5 video 85.8 ± 4.2 (-6.0)。
> - SLVMEval - Object Integrity 上，准确率（%） Human 86.6 ± 6.7 vs CLIPScore 76.0 ± 8.4 (-10.6)。

## 概要

文本到长视频（T2LV）生成技术正在快速发展，然而，如何可靠地评估生成的长视频质量仍是一个悬而未决的难题。现有的自动评估系统在长视频场景下表现明显劣于人类，尤其是在需要语义对齐和时序一致性的视频-文本一致性方面，且评估准确率随视频时长增加而显著下降。这一瓶颈的根本原因在于，当前缺乏一个能够系统诊断评估系统在长视频上各项能力缺陷的元评估基准。

针对这一空白，本文提出 **SLVMEval**——一个面向文本到长视频生成的合成元评估基准。其核心思路是：基于密集视频标注数据集，通过人工筛选的合成退化操作，构建“高质量-低质量”的受控视频对，覆盖**视频质量**（Aesthetics、Technical Quality、Appearance Style、Background Consistency）和**视频-文本一致性**（Temporal Flow、Comprehensiveness、Object Integrity、Spatial Relationship、Dynamics Degree、Color）两大组共10个评估方面。在此基础上，采用成对比较框架，以准确率衡量各评估系统辨别原始/退化视频的能力。

实验揭示了现有评估系统的根本缺陷：人类评估者在10个方面上的准确率为84.7%–96.8%，而几乎所有自动评估系统在9个方面上均低于人类表现（Table 2）。特别地，在Comprehensiveness和Dynamics Degree等需要深度语义对齐的方面，**GPT-5**（视频模式）的准确率分别仅为51.3%和35.3%，远低于人类的90.2%和95.9%。此外，几乎所有自动评估系统的准确率与视频时长呈负相关，在Background Consistency、Color和Temporal Flow等需要长程一致性的方面尤为显著（Figure 3, Table 7）。

方法层面，SLVMEval的构建流程包含四个关键模块：（1）从Vript密集视频标注数据集中选取长视频作为源视频；（2）对每个视频随机选择5个片段，施加方面特定的合成退化操作；（3）通过众包人工标注对退化成功程度进行三级评价并过滤，确保退化人眼可明确感知；（4）在过滤后的基准上对基于VLM的裁判、CLIPScore和VideoScore等基线系统进行元评估。值得注意的是，过滤前后的系统排序高度相关（Figure 4），表明可在不依赖昂贵人工过滤的情况下持续扩展基准。

在知识库定位上，SLVMEval区别于**VBench-Long**等仅提供自动评估框架的基准，它同时提供了人工标注的元评估真值，且视频时长（平均1141秒）和提示长度（平均57,884字符）远超现有基准（Table 1）。其评估范式借鉴了VBench和UVE的成对比较框架，但在长视频、多维度合成退化控制方面进行了系统性扩展。

主要结果可概括为三点：（1）现有自动评估系统在长视频评估上普遍落后于人类，尤其体现在语义对齐和长程一致性方面；（2）视频时长是影响评估准确率的关键杠杆，时长增加导致系统性能显著下降；（3）基于文本的评估模式在特定模型（如**Qwen3-VL-235B**）的部分方面上较视频模式有显著提升（Background Consistency +23.3, Appearance Style +17.1），但效果依赖于底层模型能力。这些发现为未来T2LV评估系统的改进指明了方向。

### 文本到长视频生成的评估困境

文本到视频（T2V）生成领域正经历从短片段向长视频的范式转变。随着模型能力的提升，生成数分钟甚至更长视频的需求日益迫切，然而与之配套的自动评估体系却严重滞后。现有评估基准主要面向短视频场景设计，在长视频上暴露出系统性缺陷：自动评估系统在需要语义对齐和时序一致性的视频-文本一致性方面表现尤为薄弱，且准确率随视频时长增加而显著下降。这一瓶颈直接制约了文本到长视频（T2LV）生成技术的迭代与可靠比较。

### 现有评估范式的局限性

当前主流的视频生成评估方法可归为三类，但它们在长视频场景下均存在根本性不足：

- **基于视觉-语言模型的裁判系统**（如 GPT-5、Qwen3-VL-235B）直接将视频输入 VLM 进行质量评判。这类方法受限于长视频的上下文窗口和推理成本，难以捕捉跨分钟级别的时序依赖。
- **基于文本-视觉相似度的度量**（如 CLIPScore）通过计算视频帧与文本提示的嵌入相似度来评估对齐质量。然而，长视频的密集标注文本往往远超 CLIP 模型的 token 限制，导致信息截断和评估偏差。
- **基于预训练回归模型的评分系统**（如 VideoScore-v1.1）在特定数据集上微调评分模型，但泛化到长视频和未见退化类型时性能不可靠。

上述方法共享一个核心缺陷：缺乏针对长视频特点设计的、具有可靠人工标注的元评估基准，使得我们无法系统性地诊断各评估系统在长视频上的失效模式。

### 合成元评估基准的设计动机

为解决这一空白，本文提出 SLVMEval——一个面向文本到长视频生成的合成元评估基准。其核心设计理念是：**通过可控的合成退化操作，构建“原始高质量视频 vs. 方面特定退化视频”的配对样本，从而以成对比较的方式精确衡量评估系统在 10 个细粒度方面的辨别能力**。

这一设计基于三个关键洞察：

1. **因果杠杆明确**：视频时长与评估方面类型（视频质量 vs. 视频-文本一致性）是影响评估准确率的核心杠杆。通过系统性地操控退化操作的方面和视频时长，可以精确揭示评估系统的能力边界。
2. **人工验证保障基准有效性**：合成退化并非总能产生人眼可明确感知的质量差异。SLVMEval 引入众包标注与严格过滤机制，仅保留退化效果被人工确认的样本，确保基准的“参考答案”可靠——人工评估者在 10 个方面上达到 84.7%–96.8% 的准确率。
3. **可扩展性设计**：实验表明，过滤前后的评估系统准确率高度相关（Pearson 相关性在多数方面显著），这意味着未来可以在不依赖昂贵人工过滤的情况下持续扩展基准规模。

### 核心贡献与问题定位

本文围绕以下问题展开：**现有自动评估系统在长视频上的表现与人类评估存在多大差距？这些差距在哪些方面和哪些时长条件下最为突出？如何构建一个可扩展的基准来系统性地诊断这些问题？**

通过 SLVMEval 基准，本文首次在长视频场景下对多种评估范式进行了全面的元评估，揭示了现有系统在视频-文本一致性方面的严重不足（如 Comprehensiveness 方面 GPT-5 视频模式仅 51.3%，Dynamics Degree 仅 35.3%，远低于人类 90% 以上的准确率），并验证了合成退化方法在构建可扩展评估基准方面的可行性。

## 核心方法与创新机理

SLVMEval的核心创新在于**通过可控合成退化构建长视频元评估基准**，从而系统性地揭示现有自动评估系统在文本到长视频（T2LV）生成评估上的根本缺陷。其关键设计思路与创新点体现在以下几个方面：

### 1. 合成退化驱动的配对基准构建范式

传统元评估基准依赖人工对真实生成视频进行质量排序或评分，成本高昂且难以覆盖长视频场景。SLVMEval另辟蹊径：**以高质量源视频为“正样本”，通过方面特定的可控退化操作生成“负样本”，构建成对比较测试集**。这一范式的核心优势在于：

- **因果可控性**：退化操作仅改变目标方面的质量（如仅降低背景一致性，保持其他方面不变），使得评估系统的准确率可直接归因于其对该方面的感知能力，排除了多因素混杂的干扰。
- **可扩展性**：退化操作可自动化执行，无需为每个新方面重新进行昂贵的人工标注。实验证明，过滤前后数据集上各评估系统的准确率具有强相关性（Figure 4），表明**即使不依赖人工过滤，也可持续扩展基准**。
- **难度可调节**：退化操作的超参数（如对比度变化幅度、片段选择比例）可系统性地调节，为未来构建多难度等级（简单/中等/困难）的基准提供了技术路径。

### 2. 长视频专用的多维度评估体系

SLVMEval将评估维度组织为**视频质量**与**视频-文本一致性**两大类别，细化为10个具体方面：

| 类别 | 评估方面 | 退化操作核心思路 |
|------|----------|------------------|
| 视频质量 | Aesthetics | 调整亮度、对比度、饱和度 |
| 视频质量 | Technical Quality | 添加高斯噪声与压缩伪影 |
| 视频质量 | Appearance Style | 应用风格迁移改变视觉风格 |
| 视频质量 | Background Consistency | 替换背景使其与前后帧不一致 |
| 视频-文本一致性 | Temporal Flow | 打乱片段顺序破坏时序逻辑 |
| 视频-文本一致性 | Comprehensiveness | 删除部分片段降低信息完整性 |
| 视频-文本一致性 | Object Integrity | 移除或替换提示中描述的对象 |
| 视频-文本一致性 | Spatial Relationship | 改变对象间的空间位置关系 |
| 视频-文本一致性 | Dynamics Degree | 将动态片段替换为静态帧 |
| 视频-文本一致性 | Color | 修改对象颜色使其与提示不符 |

这一分类体系直接对应T2LV评估的两大核心瓶颈：**语义对齐**（视频-文本一致性）与**长程时序一致性**（视频质量中的背景一致性等）。实验结果表明，自动评估系统在Dynamics Degree（GPT-5 video仅35.3%）和Comprehensiveness（GPT-5 video仅51.3%）等视频-文本一致性方面表现尤为糟糕，准确率与人类差距高达60.6和38.9个百分点（Table 2），精确暴露了当前评估系统在语义理解上的严重不足。

### 3. 双模态评估模式的对比框架

SLVMEval系统性地对比了**基于视频的评估**与**基于文本的评估**两种范式，揭示了不同底层模型在模态选择上的显著差异：

- **基于视频的评估**：VLM直接观看视频对并做出判断（Eq. 3）。
- **基于文本的评估**：VLM首先生成视频描述，再由LM比较描述与提示词的对齐度（Eq. 4）。

关键发现是**文本评估模式的效果高度依赖于底层模型能力**：在Qwen3-VL-235B上，文本模式相比视频模式在Background Consistency上提升+23.3个百分点，在Appearance Style上提升+17.1个百分点；但在GPT-5上，文本模式反而导致准确率下降。这表明，**对于能力较弱的VLM，将视频转化为文本描述再评估可能是一种有效的“能力补偿”策略，但该方法并不普适**。

### 4. 视频时长作为核心杠杆变量的发现

SLVMEval通过Spearman秩相关分析（Table 7, Figure 3）揭示了一个此前未被充分量化的现象：**几乎所有自动评估系统的准确率与视频时长呈负相关**（$\rho_S < 0$），且在Background Consistency、Color和Temporal Flow等需要长程一致性的方面尤为显著（p < 0.05, Table 8）。这一发现将“视频时长”确立为影响评估系统性能的核心杠杆变量，为未来长视频评估系统的改进指明了方向——**提升长程时序建模能力是缩小人机差距的关键**。

### 5. 与现有基准的本质差异

相较于现有元评估基准（如VBench-Long仅提供自动评估框架而无人工标注），SLVMEval的差异化创新在于：

- **长视频覆盖**：平均视频时长1141秒，最长10,486秒，远超现有基准（Table 1）。
- **长提示词**：平均提示长度57,884字符，更贴近真实T2LV应用场景。
- **人工验证的ground truth**：通过众包标注与严格过滤（仅保留无C评价且A多于B的样本），确保退化效果人眼可明确感知，为自动评估系统提供了可靠的上界参照。

综上，SLVMEval的核心创新并非提出新的评估指标或模型，而是**构建了一套可扩展、可控制、可诊断的长视频元评估方法论**，通过合成退化与成对比较框架，系统性地暴露了现有评估系统在长视频场景下的能力边界。

SLVMEval 采用成对比较（pairwise comparison）的元评估框架，核心思路是：给定一段长视频及其对应的文本提示，通过受控的合成退化操作生成低质量版本，构建“高质量 vs 低质量”视频对，然后测试自动评估系统能否正确识别出原始高质量视频。该框架不依赖任何特定 T2LV 生成模型的输出，而是从密集视频标注数据集中选取真实长视频作为源素材，从而规避了生成模型质量波动对基准可靠性的干扰。

整个 pipeline 由四个核心模块串联构成：

1. **源视频与标注收集**：以 Vript 密集视频标注数据集作为原始视频来源，按 1 fps 采样并统一尺寸，提取长视频及其对应的密集文本提示。
2. **方面特定的合成退化**：将评估维度组织为视频质量（Aesthetics、Technical Quality、Appearance Style、Background Consistency）和视频-文本一致性（Temporal Flow、Comprehensiveness、Object Integrity、Spatial Relationship、Dynamics Degree、Color）两大组共 10 个方面。对每个源视频，随机选取 5 个片段，分别应用方面特定的退化函数 $\Phi_a^{\mathrm{low}}$ 生成低质量视频 $v_p^-$，最终构建方面特定的配对测试集 $\mathcal{D}_a$（见公式 (2)）。
3. **人工标注与过滤**：众包工人对退化成功程度进行 A/B/C 三级评价，仅保留无 C 评价且 A 多于 B 的样本，确保退化效果在人眼可明确感知的范围内。过滤后数据集的统计信息见 Table 3。
4. **元评估与基线系统评价**：在过滤后的配对数据上，以准确率（公式 (1)）衡量各评估系统辨别原始/退化视频的能力。基线系统涵盖基于 VLM 的视频裁判（GPT-5、GPT-5-mini、Qwen3-VL-235B）、基于文本的裁判（VLM 生成描述后由 LM 比较）、CLIPScore（Jina CLIP v2）以及 VideoScore-v1.1。

整个流程的输入是源长视频及其提示词，输出是各评估系统在 10 个方面上的准确率得分。Figure 1 给出了该 pipeline 的宏观示意：人工验证的原始/退化视频对作为测试素材，自动评估系统在成对比较框架下接受检验，最终以人类表现为上界揭示现有系统的根本缺陷。

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/001_Figure_1.jpg]]
*Figure 1: Overview of proposed SLVMEval benchmark. We construct human-validated pairs of original and aspect (specifically degraded long videos), and we test various automatic evaluation systems. Human evaluators reliably pick the better video; however, all current automatic evaluation systems lag behind human performance from most perspectives, revealing critical weaknesses in T2LV evaluation*

### 3.1 基准构建流程

SLVMEval的构建遵循“源视频收集→方面特定退化→人工验证”三阶段管线，核心模块如下：

**模块一：源视频与标注收集。** 使用Vript密集视频标注数据集作为原始视频来源，按1 fps采样并统一尺寸。Vript提供了覆盖15个内容类别的长视频及其对应的密集文本描述（平均提示长度约57,884字符），为后续退化操作提供了丰富的语义锚点（Section 4.2）。

**模块二：方面特定的合成退化。** 将评估维度组织为两大类共10个方面——视频质量（Aesthetics、Technical Quality、Appearance Style、Background Consistency）和视频-文本一致性（Temporal Flow、Comprehensiveness、Object Integrity、Spatial Relationship、Dynamics Degree、Color）。对每个源视频，随机选择5个片段，通过方面特定的退化函数生成低质量版本，保持其他因素不变（Figure 2, Section 4.3, Algorithm 1）。退化操作的设计原则是“人类可明确感知”：例如，Dynamics Degree退化将片段内所有帧替换为中间帧以消除运动；Color退化通过Qwen-Image-Edit-2509修改片段内物体的颜色。

**模块三：人工标注与过滤。** 众包工人对退化成功程度进行A/B/C三级评价（A=退化明显，B=退化可感知但不明显，C=退化错误或不可见）。仅保留无C评价且A多于B的样本，确保退化人眼可明确感知。过滤后数据集包含3,932个视频，最大时长10,486秒，1,461个唯一提示（Table 1, Table 3, Section 4.4）。

### 3.2 元评估框架与核心公式

SLVMEval采用成对比较框架进行元评估：给定提示 $p$ 和一对视频 $\{v_p^+, v_p^-\}$（分别为原始高质量视频和退化低质量视频），评估系统 $e$ 需判断哪个视频质量更高。

**准确率定义。** 元评估的核心指标为准确率，定义为评估系统在测试集上正确选择高质量视频的比例：

$$\operatorname{acc}(e, \mathcal{D}) = \frac{1}{|\mathcal{D}|} \sum_{(p, \{v_p^+, v_p^-\}) \in \mathcal{D}} \mathbf{1}\bigl[e(p, \{v_p^+, v_p^-\}) = v_p^+\bigr]$$

其中 $\mathcal{D}$ 为测试集，$\mathbf{1}[\cdot]$ 为指示函数。随机猜测的基线准确率为50%（Section 3.2, Eq.(1)）。

**方面特定数据集构建。** 对每个评估方面 $a$，通过对源视频应用退化函数 $\Phi_a^{\text{low}}$ 生成配对测试集：

$$\mathcal{D}_a = \{(p, \{v_p^+, v_p^-\}) \mid (p, v_p^+) \in \mathcal{D}_{\text{src}}\}, \quad \text{where} \quad v_p^- = \Phi_a^{\text{low}}(p, v_p^+)$$

该公式保证了每个方面仅改变目标维度的质量，其他因素保持不变，从而实现对评估系统在该方面辨别能力的精确测量（Section 4.1, Eq.(2)）。

### 3.3 基线评估系统的决策公式

论文评估了四类自动评估系统，其决策机制如下：

**基于视频的VLM评估。** VLM直接比较两个视频，根据给定方面 $a$ 选择更优者：

$$e_a(p, \{u_p, v_p\}) = \begin{cases} u_p, & \text{if } \text{VLM}(a, p, u_p, v_p) = \text{"first"}, \\ v_p, & \text{if } \text{VLM}(a, p, u_p, v_p) = \text{"second"}. \end{cases}$$

该模式测试了VLM对视频内容直接感知和比较的能力（Section 5.1, Eq.(3)）。

**基于文本的VLM评估。** VLM首先生成对每个视频的方面特定描述，再由语言模型比较描述与提示词的对齐度，间接选择视频：

$$d = \mathbf{LM}(a, p, \mathbf{VLM}_{\text{cap}}(a, u_p), \mathbf{VLM}_{\text{cap}}(a, v_p)),$$
$$e_a(p, \{u_p, v_p\}) = \begin{cases} u_p, & \text{if } d = \text{"first"}, \\ v_p, & \text{otherwise}. \end{cases}$$

该模式将视频评估转化为文本对齐问题，避免了长视频输入的计算开销（Section 5.1, Eq.(4)）。

**CLIPScore评估。** 对每个视频，使用FFmpeg检测场景切换点，计算各片段中心帧与提示词的CLIPScore平均值，选择得分更高的视频：

$$e(p, \{u_p, v_p\}) = \underset{s \in \{u_p, v_p\}}{\arg\max} \frac{1}{N_s'} \sum_{i=1}^{N_s'} \text{CLIPScore}\left(f_{s,i}^{\text{mid}}, p\right)$$

其中 $f_{s,i}^{\text{mid}}$ 为视频 $s$ 第 $i$ 个片段的中间帧。该方法仅依赖静态帧的文本-图像相似度，完全忽略时序信息（Section 5.2, Eq.(5)）。

**VideoScore评估。** 在给定方面 $a$ 下，选择VideoScore得分更高的视频：

$$e_a(p, \{u_p, v_p\}) = \underset{s \in \{u_p, v_p\}}{\arg\max} \text{VideoScore}_a(s, p)$$

VideoScore基于预训练VLM的评分回归，需要将SLVMEval的方面映射到其内置维度（Section 5.3, Eq.(6), Table 10）。

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/019_Table_10.jpg]]
*Table 10: Mapping between our defined aspects and those defined in VideoScore*

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/002_Figure_2.jpg]]
*Figure 2: Viewpoints and aspect-specific degrading operations in the proposed SLVMEval benchmark. We organize the benchmark into two groups, i.e., video quality and video-text consistency, and define 10 aspects. For each aspect, we construct paired videos by applying a controlled synthetic degradation to the original long video while keeping all other factors unchanged. The right panels show example pairs. These controlled pairs enable precise meta-evaluation of whether an automatic evaluation system can reliably identify the high-quality video under each viewpoint. Additional example pairs are provided in the supplementary material*

## 实验与关键发现

### 实验设置

SLVMEval采用成对比较框架进行元评估，核心指标为**准确率（Accuracy）**，定义为评估系统在给定视频对中正确选择原始高质量视频的比例：

$$
\operatorname { a c c } ( e , \mathcal { D } ) = \frac { 1 } { | \mathcal { D } | } \sum _ { ( p , \{ v _ { p } ^ { + } , v _ { p } ^ { - } \} ) \in \mathcal { D } } \mathbf { 1 } \bigl [ e ( p , \{ v _ { p } ^ { + } , v _ { p } ^ { - } \} ) = v _ { p } ^ { + } \bigr ]
$$

评估系统涵盖四类范式：**基于视频的VLM裁判**（GPT-5、GPT-5-mini、Qwen3-VL-235B）、**基于文本的VLM裁判**（先由VLM生成视频描述，再由LM比较描述与提示词的对齐度）、**CLIPScore**（Jina CLIP v2，通过FFmpeg检测片段并计算中心帧与提示词的相似度均值），以及**VideoScore-v1.1**（预训练评分回归模型）。人类基准使用相同界面和准确率计算方式，由众包工人完成。

### 主要结果：自动评估系统全面落后于人类

**Table 2**汇总了各系统在SLVMEval 10个评估方面上的准确率。人类评估者取得84.7%–96.8%的准确率，验证了基准的有效性——退化操作确实产生了人眼可明确感知的质量差异。然而，所有自动评估系统在**9/10个方面上均低于人类表现**，差距从6.3个百分点延伸至43.2个百分点。

具体而言，在**视频质量**维度上，GPT-5（视频模式）表现最强：Aesthetics达到90.1%（人类96.5%，差距−6.4 pp），Technical Quality为85.8%（人类91.8%，差距−6.0 pp）。但在**视频-文本一致性**维度上，各系统暴露出严重短板：

- **Comprehensiveness**（信息全面性）：GPT-5视频模式仅51.3%，远低于人类的90.2%（差距−38.9 pp）。
- **Dynamics Degree**（动态程度）：GPT-5视频模式跌至35.3%，与人类95.9%形成−60.6 pp的巨大鸿沟。
- **Object Integrity**（物体完整性）：最强系统CLIPScore仅76.0%，而人类为86.6%（差距−10.6 pp）。

这些结果表明，现有评估系统在需要深层语义理解和时序一致性判断的方面尤为薄弱，其根本瓶颈不在于感知视频质量，而在于**理解视频内容与文本提示之间的语义对齐关系**。

### 视频时长对评估准确率的系统性影响

**Figure 3**与**Table 7–8**揭示了评估准确率与视频时长之间的显著负相关关系。将数据集按视频时长分为四个桶后，几乎所有自动评估系统的准确率随视频时长增加而单调下降。Spearman相关系数分析表明：

- 在**Background Consistency**、**Color**和**Temporal Flow**等需要长程时序一致性的方面，负相关性最为显著（p < 0.05）。
- 视频时长对基于VLM的系统影响尤为突出，因为长视频超出多数模型的上下文窗口，迫使系统依赖稀疏采样或压缩表示，丢失关键时序信息。

这一发现直接印证了本文的核心瓶颈判断：**现有T2LV自动评估系统在长视频场景下性能退化严重，且退化程度与评估方面的类型强相关**。

### 基于文本的评估模式：双刃剑

基于文本的评估策略展现出高度依赖底层模型能力的特性。在Qwen3-VL-235B上，文本模式相比视频模式带来显著提升：Background Consistency +23.3 pp、Appearance Style +17.1 pp、Object Integrity +12.5 pp。然而，在GPT-5上，文本模式反而导致准确率下降。这一不对称现象说明：文本评估模式通过将视频比较转化为文本描述比较，降低了视觉理解负担，但其效果取决于VLM生成描述的准确性和LM比较描述的推理能力。对于视觉能力较强但文本比较逻辑不够精细的模型，该策略可能引入额外误差。

### 人工过滤步骤的必要性分析

SLVMEval的构建流程中包含昂贵的人工过滤步骤（仅保留退化效果明确可感知的样本）。**Figure 4**通过对比过滤前后数据集上各系统准确率的Pearson相关性，检验了这一步骤是否不可或缺。结果显示，在多数评估方面上，过滤前后准确率高度相关（ρ_P较高），表明系统排序在两种条件下基本一致。这一发现具有重要实践意义：**未来可以在不依赖昂贵人工过滤的情况下，通过持续扩展合成退化数据来构建更大规模的基准**，仅需在初始阶段进行小规模人工验证以校准退化操作的超参数。

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/006_Figure_4.jpg]]
*Figure 4: Relationship between accuracy values before and after filtering on the degraded SLVMEval data. For each aspect, we plot the accuracy of each evaluation system before versus after filtering and compute the Pearson correlation coefficient*

### CLIPScore的提示长度处理策略消融

**Table 5**展示了CLIPScore在三种提示处理策略下的准确率对比：DEFAULT（直接截断）、IGNMAX（忽略超长提示）和EACHTRUNC（对每个片段分别截断）。结果显示，三种策略在各方面的准确率变化不大，平均准确率均稳定在约60%–63%区间。这表明CLIPScore对提示长度处理方式不敏感，其性能瓶颈在于视觉-文本对齐模型本身的表征能力，而非提示工程。

### 基准的局限性与开放问题

SLVMEval目前存在三个主要局限：第一，退化操作仅设定为人类易于判断的“简单”难度级别，改变超参数（如对比度变化幅度、片段选择比例）会改变基准挑战性；第二，合成退化数据的分布可能与未来T2LV模型的真实输出存在差异，无法覆盖所有潜在失败模式；第三，当前仅测试评估系统的基本辨别能力，尚未涉及更复杂的真实应用场景。

这些局限指向若干开放问题：如何系统性调节退化超参数以构建多难度层级的扩展基准？在T2LV模型逐渐成熟后，如何设计基于模型真实失败模式的评估基准？以及如何有效融合视频与文本两种评估模态以同时利用其各自优势？

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/003_Table_1.jpg]]
*Table 1: Statistics of existing and proposed benchmarks. VBench-Long [16] only provides a framework for automatic evaluation (it does not include human annotations of video quality). It supplies prompts as inputs to T2V models, assuming generated videos of approximately 1 min [14]*

![[assets/figures/papers/paper_list_l784_https_arxiv_org_abs_2603_29186/figures/004_Table_2.jpg]]
*Table 2: Accuracy (%) of each baseline system on SLVMEval. Numbers are accuracy*

## 定位与知识库关联

### 1. 与现有评估基准的关系

SLVMEval 在视频生成评估领域占据一个独特的位置：它是**首个面向文本到长视频（T2LV）生成的合成元评估基准**。与现有基准相比，其核心区分维度在于视频时长和评估颗粒度。

| 特性 | VBench | VBench-Long | FETV | EvalCrafter | **SLVMEval** |
|------|--------|-------------|------|-------------|-------------|
| 视频时长 | 短（<30s） | ~1分钟 | 短 | 短 | **长（均值1141s，最长10,486s）** |
| 提示长度 | 短 | 短 | 短 | 短 | **长（均值57,884字符）** |
| 评估方面数 | 16 | 16 | — | — | **10（分视频质量/视频-文本一致性两组）** |
| 元评估能力 | ✓ | 仅自动评估框架 | — | — | **✓（成对比较+人工验证）** |
| 退化类型 | — | — | — | — | **方面特定合成退化** |

**关键区分**：VBench-Long 虽然面向长视频，但仅提供自动评估框架，不含人工标注的视频质量真值；SLVMEval 通过合成退化构造了人工验证的高/低质量视频对，从而能精确量化评估系统在长视频场景下的可靠性。

**与 FETV 的退化策略验证**：SLVMEval 在 FETV 数据集上验证了其退化策略的排序一致性（Figure 7），表明合成退化方法在跨数据集场景下具有泛化性。

### 2. 与基线评估系统的关系

SLVMEval 评估了三大类自动评估系统，代表了当前视频质量评估的主流技术路线：

**（1）基于 VLM 的裁判系统（VLM-as-a-Judge）**
- **GPT-5 / GPT-5-mini**（视频模式）：直接输入两个视频进行比较
- **GPT-5 / GPT-5-mini**（文本模式）：先由 VLM 生成视频描述，再由 LM 比较描述与提示的对齐度
- **Qwen3-VL-235B**（视频模式 / 文本模式）：同上两种模式

**（2）基于文本-视觉相似度的评估系统**
- **CLIPScore**（基于 Jina CLIP v2）：计算视频片段中心帧与提示词的 CLIPScore 均值，选择得分更高者

**（3）基于预训练评分回归的评估系统**
- **VideoScore-v1.1**：在给定方面下直接输出质量分数，选择得分更高者

SLVMEval 的成对比较框架将所有这些系统统一到同一准确率度量下，使得跨系统、跨方面的公平比较成为可能。

### 3. 适用边界与核心局限

**（1）合成退化的分布偏差**
基准基于人工设计的合成退化构造测试对，其数据分布与未来 T2LV 模型的实际输出可能存在系统性差异。这意味着：
- 当前基准主要测试评估系统对**已知退化类型**的识别能力
- 无法覆盖真实 T2LV 模型中可能出现的**未知失败模式**（如复杂物理不一致、细粒度语义错误）

**（2）退化难度的单一性**
退化操作的超参数（如对比度变化幅度、片段选择数量）目前仅设定为**人类易于察觉的单一难度级别**。这决定了 SLVMEval 当前测度的是评估系统的**基本能力下限**，而非其在更复杂场景下的表现上限。调整这些超参数会直接改变基准的挑战性。

**（3）地域性偏差**
人工评估使用日语界面和日本众包平台，可能引入地域性或语言特定的审美偏好偏差。

**（4）方面覆盖的有限性**
当前 10 个方面虽覆盖了视频质量和视频-文本一致性的主要维度，但未能穷尽所有潜在评估维度（如情感表达、叙事连贯性、文化适配性等）。

### 4. 开放问题

**（1）多难度等级的基准扩展**
如何系统性地调节退化操作超参数，构建**简单/中等/困难**不同难度等级的扩展基准？这将使 SLVMEval 从“基本能力测试”升级为“能力分层诊断”工具。

**（2）真实模型失败模式的对齐**
在真实 T2LV 模型逐渐成熟后，如何基于模型的**实际失败模式**设计更复杂、更贴近应用场景的评估基准？这需要建立合成退化与真实退化之间的映射关系。

**（3）长程时序一致性的评估瓶颈**
实验明确揭示：几乎所有自动评估系统的准确率与视频时长呈负相关（Spearman $\rho_S < 0$），在 Background Consistency、Color 和 Temporal Flow 等需要长程一致性的方面尤为显著。如何提升评估系统对**长程时序依赖**的建模能力，是核心挑战。

**（4）多模态评估模式的融合**
基于文本的评估模式在 Qwen3 上相比视频模式有显著提升（Background Consistency +23.3），但在 GPT-5 上反而下降，说明文本评估的效果依赖于底层模型能力。能否设计一种**自适应融合策略**，根据方面特性和模型能力动态选择或组合视频/文本两种模态？

**（5）无需人工过滤的基准扩展**
过滤前后数据集上评估系统准确率的高度相关性（Figure 4）表明人工过滤步骤并非绝对必要。这是否意味着可以设计**自动化的退化质量验证机制**，从而在不依赖昂贵人工标注的情况下持续扩展基准规模？

## 原文 PDF

![[paperPDFs/CVPR_2026/SLVMEval_Synthetic_Meta_Evaluation_Benchmark_for_Text_to_Long_Video_Generation.pdf]]
