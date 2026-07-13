---
title: "CoMPAS3D: A Dataset and Benchmark for Interactive Motion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/CoMPAS3D:_A_Dataset_and_Benchmark_for_Interactive_Motion.pdf"
project_link: null
code_link: null
aliases:
- CoMPAS3D
tags:
- arxiv_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入专家标注的动作类别标签和熟练度层级，构建CoMPAS3D数据集；在此之上微调视觉语言模型（VLM）作为动作分类器和熟练度估计器，将其转化为可量化的客观评估指标——动作可辨识性（move legibility）和熟练度适配性（proficiency appropriateness）。
primary_logic: 将双人舞蹈类比为口语对话：动作分类如同语音转写，熟练度估计如同流利度评估。基于这一类比，利用专家标注语料训练VLM作为“自动裁判”，可检测生成动作是否在salsa动作词汇内可辨识、是否匹配目标熟练度层级——这些语义维度是运动学指标完全无法捕捉的。
claims:
- 生成方法在运动学指标上表现与真实数据可比，但在动作可辨识性和熟练度适配性上远低于真实数据
- 人工评估在全部6个真实竞赛评分维度上确认生成动作与真实动作之间存在显著差距
- 微调VLM可有效替代人工进行动作分类和熟练度评估，dyadic设置下InternVL3动作分类F1=51.09，Qwen2.5-VL熟练度估计F1=84.53
- "CoMPAS3D Move Classification 上 Dyadic Move Accuracy / Macro F1 = InternVL3: 74.24 / 51.09; Qwen2.5-VL: 69.87 / 49.30; LLaVA-..."
---

# CoMPAS3D: A Dataset and Benchmark for Interactive Motion

> [!tip] 核心洞察
> 将双人舞蹈类比为口语对话：动作分类如同语音转写，熟练度估计如同流利度评估。基于这一类比，利用专家标注语料训练VLM作为“自动裁判”，可检测生成动作是否在salsa动作词汇内可辨识、是否匹配目标熟练度层级——这些语义维度是运动学指标完全无法捕捉的。

| 字段      | 内容                                                                                                                                                                               |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | CoMPAS3D：一个交互式动作数据集与基准评测框架                                                                                                                                                       |
| 英文题名    | CoMPAS3D: A Dataset and Benchmark for Interactive Motion                                                                                                                         |
| 会议/期刊   | arXiv 2025                                                                                                                                                                       |
| Links   | [paper](https://arxiv.org/abs/2507.19684)                                                                                                                                        |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method  | CoMPAS3D（数据集与三层评估框架）                                                                                                                                                             |
| Dataset | CoMPAS3D Move Classification, CoMPAS3D Proficiency Estimation, CoMPAS3D Follower Generation — 运动学指标                                                                              |

> [!tip] 效果简介
> - CoMPAS3D Move Classification 上，Dyadic Move Accuracy / Macro F1 InternVL3: 74.24 / 51.09; Qwen2.5-VL: 69.87 / 49.30; LLaVA-NeXT-Video: 73.36 /... vs Zero-shot最佳: InternVL3 27.95 / 7.74 (Fine-tuned vs Zero-shot: Accuracy +46.29, F1 +43.35 (InternVL3))。
> - CoMPAS3D Proficiency Estimation 上，Dyadic Accuracy / Macro F1 Qwen2.5-VL: 84.63 / 84.53; LLaVA: 83.14 / 82.64; InternVL3: 75.91 / 75.20 vs Zero-shot最佳: Qwen2.5-VL 48.72 / 38.87 (Fine-tuned vs Zero-shot: Accuracy +35.91, F1 +45.66 (Qwen2.5-VL))。
> - CoMPAS3D Follower Generation — 运动学指标 上，FID_k (↓) / Div_k (↑) / BAS (↑) Groundtruth: 0.00 / 8.741 / 0.1552 vs Duolando: 10.47 / 7.964 / 0.2201; InterGen: 23.23 / 8.594 / 0.1970 (Duolando FID_k=10.47 (vs GT 0.00), InterGen FID_k=23.23; 两者运动学指标可比)。

## 概要

现有交互式运动生成研究面临一个关键瓶颈：评估体系严重依赖运动学指标（如 $FID_k$、$BED$、$BAS$ 等），这些指标能够衡量生成动作在运动学特征空间中的分布相似性和节拍对齐程度，却完全无法捕捉动作的**语义可辨识性**（生成的跟舞动作在共享动作词汇内能否被识别为特定舞步）以及**熟练度适配性**（生成动作是否匹配目标舞者的技能水平）。与此同时，已公开的双人舞蹈数据集普遍缺乏细粒度动作标注和熟练度层级划分，使得这类语义层面的评估无从开展。

CoMPAS3D 针对上述缺口提出了系统性的解决方案。其核心思路是将双人即兴舞蹈类比为口语对话——动作分类如同语音转写，熟练度估计如同流利度评估。基于这一类比，该工作构建了首个具备专家动作标注和熟练度层级的即兴双人舞蹈数据集，并在其上微调视觉语言模型（VLM）作为“自动裁判”，将动作可辨识性和熟练度适配性转化为可量化的客观评估指标。

主要发现可概括为三点：

1. **生成方法与真实数据之间存在显著的语义鸿沟**：尽管现有生成基线（Duolando、InterGen）在运动学指标上表现与真实数据可比（Duolando $FID_k=10.47$，InterGen $FID_k=23.23$），但其动作可辨识性（Move F1 分别仅为 6.70 和 7.69）和熟练度适配性远低于真实数据（Groundtruth Move F1=53.55，Proficiency F1=51.64）。人工评估进一步确认，真实动作在全部 6 个真实竞赛评分维度上均显著优于生成动作（$p < 0.001$）。

2. **微调 VLM 可有效替代人工评估**：在真实数据上，微调后的 InternVL3 在双人动作分类任务中达到 F1=51.09，Qwen2.5-VL 在熟练度估计任务中达到 F1=84.53，相比零样本模型提升显著（F1 分别提升 43.35 和 45.66），为生成动作的语义评估提供了可行的自动化工具。

3. **运动学指标与语义指标揭示不同维度的质量**：运动学指标显示生成方法已接近真实数据，但语义指标暴露了其在动作词汇可辨识性和熟练度层级适配上的根本性不足，表明现有评估体系需要多维度的补充。

在方法谱系上，CoMPAS3D 并非提出新的生成模型，而是构建了一个**数据集+评估框架**的基础设施，包含三个基准任务：动作分类（类比转写）、熟练度估计（类比流利度评估）和跟舞生成（类比对话应答）。其评估框架融合了传统运动学指标、基于微调 VLM 的语义客观指标，以及源自真实竞赛评审准则的 6 维主观评估，为交互式运动生成领域提供了更全面的评测基准。



### 问题背景：交互式运动生成的评估盲区

双人舞蹈是一种典型的即兴交互式运动——领舞者通过身体语言发出信号，跟舞者在共享音乐节拍下实时解读并做出动作响应。这一过程与人类口语对话高度相似：动作序列如同语音流，特定舞蹈动作如同词汇，而舞者的熟练度则类似于语言流利度。然而，当前交互式运动生成领域的评估体系却停留在“音质”层面，完全缺失了“语义”维度。

现有运动生成评估指标——包括运动学Fréchet距离（$FID_k$、$FID_g$）、跨距离交互指标（$FID_cd$）、多样性度量（$Div_k$、$Div_g$、$Div_cd$）以及节拍对齐分数（$BED$、$BAS$）——仅能衡量生成动作在运动学特征空间中的分布相似性和节拍同步性。这些指标无法回答两个关键问题：**生成的动作是否属于该舞种的动作词汇（action vocabulary）？生成动作所体现的熟练度水平是否与目标层级匹配？** 换言之，现有的运动学指标完全无法捕捉动作的语义可辨识性（move legibility）和熟练度适配性（proficiency appropriateness）。

### 现有数据集的结构性缺口

评估盲区的根源在于数据集的缺失。现有的公开双人舞蹈数据集存在三个结构性缺陷：

1. **缺乏细粒度动作标注**：现有数据集仅提供原始运动捕捉数据，未对舞蹈动作进行类别标注，使得动作可辨识性评估无从开展。
2. **缺乏熟练度层级差异**：现有数据集多为单人编舞表演，或仅包含单一熟练度水平的舞者，无法支持熟练度适配性评估。
3. **缺乏即兴交互**：多数数据集为编排舞蹈，舞者按预定序列执行动作，缺乏即兴双人交互中领舞-跟舞的动态协商过程。

这些缺口导致了一个恶性循环：没有标注数据就无法构建语义评估指标，没有语义评估指标就无法诊断生成方法的深层缺陷，进而阻碍了交互式运动生成领域的实质性进步。

### 本文动机：从运动学走向语义学

本文的核心动机是打破上述循环。我们提出将双人舞蹈类比为口语对话系统：动作分类对应语音转写（transcription），熟练度估计对应流利度评估（fluency assessment），跟舞生成对应对话响应（dialogue response）。基于这一类比，我们构建了**CoMPAS3D**——首个具备专家细粒度动作标注和熟练度层级的即兴双人舞蹈数据集，并在此基础上训练视觉语言模型（VLM）作为“自动裁判”，将动作可辨识性和熟练度适配性转化为可量化的客观评估指标。

这一框架使得我们首次能够揭示一个关键事实：**现有运动生成方法在运动学指标上表现与真实数据可比，但在语义维度上存在巨大鸿沟**——生成动作的可辨识性远低于真实舞蹈，且无法有效适配目标熟练度层级。这一发现表明，仅依赖运动学指标优化生成模型可能导致“听起来像但不知所云”的运动序列，而CoMPAS3D提供的语义评估维度为生成模型的实质性改进指明了方向。



## 核心方法与创新机理

CoMPAS3D的核心创新在于将双人即兴舞蹈的评估从纯运动学层面提升至语义层面，其关键突破可概括为三个紧密耦合的“changed slots”：**数据集特性**、**客观评估指标**和**主观评估维度**。这三个维度共同解决了一个根本瓶颈——现有评估体系无法衡量生成动作在共享动作词汇内的可辨识性（move legibility）和对搭档熟练度水平的适配性（proficiency appropriateness）。

### 从运动学到语义：评估范式的根本转变

现有交互式运动生成方法（如**Duolando**和**InterGen**）的评估完全依赖运动学指标：$FID_k$、$FID_g$、$FID_cd$ 衡量分布距离，$Div_k$、$Div_g$、$Div_cd$ 衡量多样性，$BED$ 和 $BAS$ 衡量节拍对齐。这些指标能够捕捉动作的物理逼真度和节奏一致性，却完全无法回答两个关键问题：生成的跟舞动作是否在salsa动作词汇内可被辨认？它是否匹配目标熟练度层级应有的动作复杂度与风格？

CoMPAS3D的核心洞察是将双人舞蹈类比为口语对话——动作分类如同语音转写，熟练度估计如同流利度评估。基于这一类比，论文构建了一套全新的评估框架，其运作逻辑分为两个阶段：

1. **验证阶段**：首先在真实数据上微调视觉语言模型（VLM），使其能够准确完成动作分类和熟练度估计（Table 2），从而确立这些模型作为“自动裁判”的有效性。
2. **评估阶段**：将微调后的VLM应用于生成动作，量化其动作可辨识性（Move F1）和熟练度适配性（Proficiency F1），揭示运动学指标无法捕捉的语义差距。

### 数据集特性：从无助标注到专家细粒度标注

现有公开双人舞蹈数据集（如DD100、AIST++、DanceTrack）在三个关键维度上存在空白：缺乏细粒度动作类别标注、无熟练度层级区分、多为单人编舞表演而非即兴双人交互。CoMPAS3D填补了这一空白：

- **规模与即兴性**：包含3小时即兴salsa双人舞，覆盖9对舞者，所有表演均为即兴而非编排，更贴近真实交互场景。
- **三层熟练度**：入门（Beginner）、中级（Intermediate）、专业（Professional）三个层级，每层级包含多对舞者，且测试集采用留出配对策略（每层级留出一对，见Table 5），避免模型记忆特定配对特征。
- **30类动作标注**：由一位15年经验的salsa专家完成2,800+段动作片段标注，涵盖动作类别、执行错误和风格元素（见Table 6），经第二位专家抽样验证（Cohen's Kappa = 0.752）。Figure 2揭示了不同熟练度层级的动作分布差异——入门舞者高度依赖Basic Step，而专业舞者使用更广泛的词汇（如Left Turn、Copa等），且平均每场表演执行54.5次风格化动作（vs. 入门5.1次）。

这一数据集的构建使得“动作可辨识性”和“熟练度适配性”的量化评估首次成为可能——没有专家标注的动作类别和熟练度标签，就无法训练自动分类器，更无法将语义评估转化为客观指标。

### 客观评估指标：从纯运动学到运动学+语义双轨

CoMPAS3D保留了现有运动学指标（$FID_k$、$FID_g$、$FID_cd$、$Div_k$、$Div_g$、$Div_cd$、$BED$、$BAS$），同时引入了两个全新的语义指标：

- **动作可辨识性（Move Legibility）**：通过微调InternVL3（最佳模型）作为动作分类器，在12类salsa动作（含Other）上计算Macro F1。该指标衡量生成跟舞动作在salsa动作词汇内的可辨识程度——F1越高，说明生成的动作越能被识别为特定的salsa动作，而非模糊不清的运动。
- **熟练度适配性（Proficiency Appropriateness）**：通过微调Qwen2.5-VL（最佳模型）作为熟练度估计器，在三个层级上计算F1。该指标衡量生成动作是否匹配目标熟练度水平——例如，当要求生成入门级跟舞时，模型是否确实生成了入门舞者特征的动作（如更多Basic Step、更少复杂旋转）。

Table 2显示，微调VLM在真实数据上取得了可靠的分类性能：InternVL3在双人设置下动作分类F1达51.09，Qwen2.5-VL在熟练度估计上F1达84.53。这为后续评估建立了可信的自动化裁判。Table 4则揭示了关键发现：**生成方法在运动学指标上表现与真实数据可比（Duolando $FID_k$=10.47，InterGen $FID_k$=23.23），但在语义指标上远低于真实数据**——Duolando Move F1仅6.70，InterGen Move F1仅7.69，而Groundtruth Move F1为53.55。这一巨大差距（约7-8倍）是运动学指标完全无法揭示的，直接证明了现有生成方法在动作语义层面的根本性不足。

### 主观评估维度：从3维通用到6维竞赛标准

现有工作通常采用3个通用维度进行人工评估：motion quality、music-motion alignment、partner coordination。CoMPAS3D则直接采用真实salsa竞赛的6个评审维度：timing、musicality、technique、difficulty、partner coordination、originality（见Table 8）。这一选择使得人工评估与真实舞蹈评判标准对齐，大幅提升了评估的生态效度。

Figure 4的人工评估结果显示，Groundtruth在所有6个维度上均显著高于InterGen和Duolando（p < 0.001），而两个生成方法之间无显著差异。值得注意的是，这一结果与运动学指标中两方法可比的表现一致，但语义指标揭示了两者共同的致命短板——它们都无法生成在salsa动作词汇内可辨识的跟舞动作。

### 因果链路总结

CoMPAS3D的创新形成了一个完整的因果链路：**专家标注的数据集** → **可训练的VLM自动裁判** → **语义层面的客观指标** → **揭示运动学指标无法捕捉的生成质量差距**。这一链路的核心价值不在于提出新的生成方法，而在于建立了一套能够诊断生成方法语义缺陷的评估基础设施——正如Table 4所展示的，现有方法在运动学层面“看起来不错”，但在动作可辨识性上几乎完全失败，这一发现如果没有语义评估指标将永远无法被量化。

### 需注意的局限

- 数据集目前仅覆盖salsa单一舞种，VLM分类器和评估框架向其他舞种的迁移性尚未验证。
- 客观语义指标（Move F1、Proficiency F1）与人工判断之间的直接相关性未正式测量，这一局限在当前运动生成评估领域普遍存在，需要后续研究补充。
- 动作标注由单一专家完成（经第二位专家抽样验证），标注者偏差可能存在，尽管Cohen's Kappa=0.752表明一致性良好。



CoMPAS3D 的整体框架围绕一个核心类比构建：**将双人即兴舞蹈视为口语对话**。基于这一类比，论文将动作分类类比为语音转写（transcription），将熟练度估计类比为流利度评估（fluency assessment），将跟舞生成类比为对话响应生成（dialogue response generation）。框架由三个层次构成：**数据集层**、**基准任务层**和**评估层**，三者形成闭环——数据集提供专家标注的“语料”，基准任务定义可操作的预测目标，评估层则将任务输出转化为可量化的语义指标。

### 数据集层：CoMPAS3D

CoMPAS3D 是首个公开的即兴双人舞蹈数据集，包含约3小时的 salsa 舞蹈数据，覆盖 **入门（Beginner）、中级（Intermediate）、专业（Professional）** 三个熟练度层级，共9对舞者。每段舞蹈配有同步音乐，并由一位拥有15年经验的专家进行细粒度标注，经第二位专家抽样验证（Cohen's Kappa=0.752）。标注体系涵盖三类信息：

- **动作类别（Move Types）**：30类 salsa 动作（含 Other），按8拍片段进行标注
- **风格元素（Styling Elements）**：如手臂装饰、身体波浪等
- **执行错误（Execution Errors）**：如节奏错误、引导失误等

该数据集的关键差异化特征在于：相比现有双人舞蹈数据集（如 AIST++、DanceDuet），CoMPAS3D 首次同时提供了**即兴交互**、**熟练度层级**和**细粒度动作标注**三重属性（见 Table 1），使得语义层面的评估成为可能。

### 基准任务层：三项核心任务

框架定义了三个基准任务，形成从感知到生成的递进结构（见 Figure 3）：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/004_Figure_3.jpg]]
*Figure 3: Proposed benchmark tasks for the CoMPAS3D dataset: (1) move classification (dyadic and on solo follower moves), (2) proficiency estimation and (3) follower generation. Objective evaluation of follower dance generation uses (1) and (2)*

**1. 动作分类（Move Classification）**  
给定一段8拍的双人动作序列（或仅跟舞者动作），识别正在执行的 salsa 动作类别。该任务类比语音转写，旨在检测动作是否在共享的动作词汇内可辨识。支持两种输入设置：
- **单人设置（Single-person）**：仅使用跟舞者动作
- **双人设置（Dyadic）**：同时使用领舞和跟舞者动作

**2. 熟练度估计（Proficiency Estimation）**  
给定一段动作序列，判断舞者或舞对所属的熟练度层级（入门/中级/专业）。该任务类比第二语言习得中的流利度评估，旨在捕捉动作执行的质量信号。

**3. 跟舞生成（Follower Generation）**  
给定领舞动作序列、共享音乐和目标熟练度层级，生成跟舞动作序列。该任务类比对话响应生成，是框架中唯一的生成任务，也是评估的最终落脚点——生成动作的质量通过前两个任务的模型来量化。

### 评估层：运动学指标 + 语义指标 + 人工评估

框架的评估体系采用三层结构，逐层递进地衡量生成跟舞动作的质量：

**第一层：运动学指标（Kinematic Metrics）**  
沿用现有运动生成领域的标准指标，包括 $FID_k$（运动学特征空间 Fréchet 距离）、$FID_g$（图形特征空间 Fréchet 距离）、$FID_{cd}$（跨距离交互质量）、$Div_k$ / $Div_g$ / $Div_{cd}$（多样性）、$BED$（领舞-跟舞节拍同步性）和 $BAS$（动作-音乐节拍对齐）。这些指标仅衡量运动分布的统计相似性和节奏一致性，无法捕捉语义层面的质量。

**第二层：语义客观指标（Semantic Objective Metrics）**  
这是框架的核心创新。通过在 CoMPAS3D 专家标注上微调视觉语言模型（VLM），构建了两个“自动裁判”：

- **动作可辨识性（Move Legibility）**：使用微调后的 InternVL3 作为动作分类器，对生成跟舞动作进行类别预测，计算 Macro F1 分数。该指标衡量生成动作是否在 salsa 动作词汇内可被识别——F1 越高，说明生成的动作越“可读”。
- **熟练度适配性（Proficiency Appropriateness）**：使用微调后的 Qwen2.5-VL 作为熟练度估计器，判断生成动作所属的熟练度层级是否与目标层级一致，计算 F1 分数。该指标衡量生成动作是否匹配指定的熟练度水平。

两个 VLM 评估器先在真实数据上验证有效性（Table 2：InternVL3 双人动作分类 F1=51.09，Qwen2.5-VL 双人熟练度估计 F1=84.53），再应用于生成数据的评估（Table 4）。

**第三层：主观人工评估（Subjective Human Evaluation）**  
采用 salsa 竞赛的真实评审维度（共6个：Timing、Musicality、Technique、Difficulty、Partner Coordination、Originality），由人类评审在5点 Likert 量表上对生成视频片段评分。该层提供与真实竞赛标准对齐的效度锚点。

### 模块间的输入输出流

整体 pipeline 的数据流如下：

1. **数据集构建**：原始舞蹈视频 → SMPL-X 参数提取 → 专家标注（动作类别、风格、错误）→ CoMPAS3D 数据集
2. **评估器训练**：CoMPAS3D 标注数据 → 渲染为视频序列 → 微调 VLM（InternVL3/Qwen2.5-VL/LLaVA-NeXT-Video）→ 动作分类器 + 熟练度估计器
3. **生成评估**：跟舞生成器（Duolando/InterGen）输出 → 渲染为视频 → 运动学特征提取（计算 $FID_k$ 等）→ VLM 评估器推理（计算 Move F1、Proficiency F1）→ 人工评审（计算6维度 Likert 评分）

值得注意的是，框架在评估生成动作时采用**两阶段验证策略**：先在真实数据上确认 VLM 评估器的可靠性（Table 2），再将其应用于生成数据（Table 4），从而确保语义指标的测量效度。Table 4 的核心发现——生成方法在 Move F1 上远低于真实数据（InterGen 7.69 vs GT 53.55），同时运动学指标表现可比（Table 3：Duolando $FID_k$=10.47）——直接验证了框架的核心主张：**运动学指标无法捕捉语义层面的生成质量缺陷**。



### 三层基准任务框架

CoMPAS3D 围绕“双人舞蹈即口语对话”的核心类比，定义了三个递进的基准任务，形成从感知到生成的完整评估链路（图3示意）：

1. **动作分类（Move Classification）**：类比语音转写。给定一段8拍的运动序列视频，识别其中执行的 salsa 动作类别。支持单人（仅跟舞者）和双人（领舞+跟舞）两种输入设置，覆盖30个细粒度动作类别及一个“Other”兜底类。

2. **熟练度估计（Proficiency Estimation）**：类比二语习得中的流利度评估。给定舞者或舞对的运动序列，判断其所属熟练度层级——入门（Beginner）、中级（Intermediate）或专业（Professional）。

3. **跟舞生成（Follower Generation）**：类比对话响应生成。给定领舞动作序列、共享音乐及目标熟练度层级，生成与之协调的跟舞动作序列。该任务的输出随后由任务1和任务2的微调模型进行客观评估。

### 核心评估模块

#### 动作分类器（Move Classifier）

该模块将渲染后的8拍运动序列视频作为输入，由微调视觉语言模型（VLM）输出动作类别标签。论文对三种VLM架构进行了微调：**Qwen2.5-VL**、**LLaVA-NeXT-Video** 和 **InternVL3**。微调在 CoMPAS3D 的专家标注语料上进行，输出层适配为30类动作分类头。

关键设计选择：
- **双人（dyadic）vs. 单人（follower-only）**：双人设置始终优于单人设置（Table 2），表明领舞动作携带了额外的动作识别信息，这对分类器设计有直接影响。
- **微调 vs. 零样本**：零样本VLM倾向于过预测单一高频类别（如 Basic Step），导致准确率虚高但宏平均F1极低（InternVL3零样本F1仅7.74，微调后达51.09），验证了专家标注语料微调的必要性。

#### 熟练度估计器（Proficiency Estimator）

该模块与动作分类器共享相同的VLM微调框架，但输出层适配为3类熟练度层级。关键发现：
- 双人熟练度估计准确率可达84.63%（Qwen2.5-VL），远高于单人设置。
- 单人熟练度估计显著困难，提示**交互动态本身携带了关键的熟练度线索**——领舞与跟舞之间的协调模式、响应延迟、力引导的流畅性等信息在单人运动序列中不可见。

#### 跟舞生成器（Follower Generator）

该模块接收领舞动作、音乐特征及目标熟练度层级作为条件输入，生成跟舞动作序列。论文中用于基准测试的两个生成基线为：
- **Duolando**：舞蹈专项跟舞生成模型
- **InterGen**：通用人-人交互生成模型

生成质量通过运动学指标和语义指标双重评估（见实验部分），此处不展开。

### 关键公式与变量含义

以下公式为论文用于运动学评估的标准指标，均用于衡量生成动作与真实动作在特征空间中的分布差异或时间对齐程度。

**Fréchet Inception Distance（运动学特征空间）**

$$FID_k$$

衡量生成动作分布与真实动作分布在运动学特征空间中的 Fréchet 距离。值越低表示分布越接近。特征提取基于预训练的运动编码器，捕捉关节位置、速度等运动学信息。

**Fréchet Inception Distance（图形特征空间）**

$$FID_g$$

与 $FID_k$ 结构相同，但特征提取自渲染后的动作视频帧，捕捉视觉表现层面的分布差异。

**Cross-distance FID**

$$FID_cd$$

专门用于衡量双人交互质量的 Fréchet 距离变体。计算领舞与跟舞之间的跨距离特征分布差异，反映双人协调程度。

**Diversity（运动学/图形/跨距离）**

$$Div_k, \quad Div_g, \quad Div_cd$$

分别对应上述三个特征空间的多样性度量。通过计算特征空间中样本对的平均欧氏距离，衡量生成动作覆盖特征空间的范围。值越高表示多样性越好。

**Beat Echo Degree**

$$BED$$

领舞-跟舞节拍同步性度量。量化跟舞动作对领舞节拍信号的响应一致性，反映双人间的节奏耦合强度。

**Beat Alignment Score**

$$BAS$$

动作-音乐节拍对齐度量。衡量舞者动作的关键帧（如脚步落地）与音乐节拍的时间对齐精度。值越高表示动作与音乐节拍的同步性越好。

### 评估链路闭环

整个框架的评估逻辑形成闭环：首先在真实数据上验证微调VLM的动作分类和熟练度估计能力（Table 2），确认其可作为有意义的客观指标；然后将这些微调模型应用于生成动作的评估，输出 **Move Legibility F1**（动作可辨识性）和 **Proficiency Appropriateness F1**（熟练度适配性）；最后通过人工评估（Figure 4）验证生成动作与真实动作在6个真实竞赛维度上的差距。这一设计使得语义层面的评估不再依赖纯运动学指标。

**需注意的限制**：客观语义指标（Move F1、Proficiency F1）与人工判断之间的直接相关性尚未量化测量，这一缺失在当前运动生成评估领域普遍存在，需后续研究补全。



## 实验与关键发现

### 核心实验设计逻辑

CoMPAS3D的实验体系围绕一个核心论证链条展开：**先验证VLM自动裁判的有效性，再用它揭示现有生成方法的深层缺陷**。具体而言，第一阶段在真实数据上微调并验证动作分类器和熟练度估计器的判别能力（Table 2），确认其可作为有意义的客观语义指标；第二阶段将这些指标应用于生成动作的评估，暴露运动学指标无法捕捉的问题（Table 3–4）；第三阶段通过人工评估（Figure 4）交叉验证，确认语义指标揭示的差距与人类感知一致。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/005_Table_2.jpg]]
*Table 2: Classification results on CoMPAS3D. Move classification (left) reports accuracy (Acc.) and macro-averaged weighted F1 for single-person (follower only) and dyadic (leader + follower) settings. Proficiency estimation (right) identifies skill level from motion*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison on CoMPAS3D. We include ground truth as reference and two generative baselines. We present solo, interactive, and motion–music alignment metrics. Arrows indicate whether higher (↑) or lower (↓) is better. Among generative methods (excluding ground truth), the best value in each column is shown in bold*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/007_Table_4.jpg]]
*Table 4: Objective legibility and proficiency appropriateness evaluations (in bold) on generated follower motions on CoMPAS3D. Ground truth from Table 2 is included as reference*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/008_Figure_4.jpg]]
*Figure 4: Human evaluation study results. Ratings are on a 5-point Likert scale across six salsa competition dimensions [3]. GT = ground truth, IG = InterGen, DU = Duolando. Statistical significance between GT and each generative method is indicated*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/019_Figure_9.jpg]]
*Figure 9: Confusion matrices for move classification using fine-tuned models, reported in Table 2*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/021_Figure_10.jpg]]
*Figure 10: Confusion matrices for move classification using zero-shot models, reported in Table 2*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/023_Figure_11.jpg]]
*Figure 11: Confusion matrices for proficiency classification using fine-tuned models, reported in Table 2*

这一设计与论文的“舞蹈即对话”类比紧密对应：动作分类如同语音转写评估词汇可辨识性，熟练度估计如同流利度评估衡量水平适配性——两者共同构成超越传统运动学指标的语义评估层。

### VLM自动裁判的验证：动作分类与熟练度估计

**Table 2** 展示了微调VLM与零样本VLM在动作分类和熟练度估计上的性能对比，这是整个评估框架有效性的前提验证。

**动作分类**：在双人（dyadic）设置下，微调后的InternVL3取得74.24%的Accuracy和51.09的Macro F1，相比零样本InternVL3的27.95% Accuracy和7.74 F1，提升幅度分别为+46.29和+43.35。LLaVA-NeXT-Video微调后达到73.36% Accuracy / 51.24 F1，Qwen2.5-VL微调后达到69.87% Accuracy / 49.30 F1。三个微调模型性能接近，但InternVL3在Accuracy上略优。

零样本模型的低F1（7.74–8.07）暴露了一个关键失败模式：**零样本VLM倾向于过度预测单一高频类别**（如Basic Step），导致准确率因类别不平衡而虚高，但F1极低。这在附录Figure 9–12中得到可视化确认——微调后的模型在所有类别上产生更均衡的预测分布。

**熟练度估计**：微调Qwen2.5-VL在双人设置下达到84.63% Accuracy和84.53 Macro F1，LLaVA-NeXT-Video为83.14% / 82.64，InternVL3为75.91% / 75.20。零样本最佳为Qwen2.5-VL的48.72% Accuracy / 38.87 F1，微调提升+35.91 Accuracy和+45.66 F1。熟练度估计整体优于动作分类，因为三分类任务（入门/中级/专业）远简单于12类动作识别。

**消融发现**：双人设置一致优于单人（follower-only）设置。以InternVL3动作分类为例，双人Accuracy 74.24 vs 单人65.63，F1 51.09 vs 42.34。这表明领舞动作携带了额外的动作识别信息——双人交互动态本身即是判别信号。熟练度估计中这一差距更为显著：单人估计“远难于”双人估计，提示交互动态中包含重要的熟练度线索（如领舞-跟舞的配合流畅度、力度传递等）。

### 生成方法评估：运动学指标的表象与语义指标的真相

**Table 3** 展示了Groundtruth、Duolando和InterGen在运动学指标上的对比。Duolando的$FID_k=10.47$，InterGen的$FID_k=23.23$，两者在$Div_k$、$FID_g$、$Div_g$、$FID_{cd}$、$Div_{cd}$、$BED$和$BAS$等指标上表现可比，且与Groundtruth（$FID_k=0.00$）的差距在运动生成领域的常规范围内。仅看运动学指标，Duolando和InterGen似乎已经取得了可接受的生成质量。

**Table 4** 的语义指标彻底推翻这一表象。在动作可辨识性（Move Legibility F1）上，Groundtruth为53.55，而InterGen仅为7.69，Duolando仅为6.70——**生成动作的可辨识性不到真实动作的15%**。这意味着生成模型虽然能产生运动学上合理的动作序列，但这些动作在salsa动作词汇内几乎无法被识别为有意义的舞蹈动作。在熟练度适配性（Proficiency Appropriateness F1）上，Groundtruth为51.64，InterGen为37.12，Duolando为22.47。InterGen在熟练度适配性上相对优于Duolando，但两者均远低于真实数据。

**关键洞察**：运动学指标与语义指标之间存在严重脱节。Duolando在$FID_k$上优于InterGen（10.47 vs 23.23），但在Move F1上两者几乎持平（6.70 vs 7.69），在Proficiency F1上InterGen反而显著优于Duolando（37.12 vs 22.47）。这表明**运动学质量与语义可辨识性、熟练度适配性之间不存在简单的正相关关系**——一个运动学上“更真实”的生成模型，未必产生语义上更有意义的舞蹈动作。

**零样本VLM的评估陷阱**：附录Section C.3和Figure 13揭示了一个重要的方法论警示。当将零样本InternVL3直接应用于Duolando生成的视频进行动作分类时，模型取得高Accuracy但极低F1——原因是其将绝大多数片段预测为Basic Step。由于Basic Step在数据集中占比最高，这种偏置在类别不平衡下虚高了准确率。这进一步验证了**必须使用微调模型而非零样本模型作为自动裁判**，否则评估结果将被模型自身的预测偏差严重污染。

### 人工评估：六个竞赛维度的交叉验证

**Figure 4** 展示了人工评估在六个真实salsa竞赛维度上的结果。评估者（具有舞蹈经验的参与者）对Groundtruth、InterGen和Duolando生成的视频片段进行5-point Likert评分，维度包括Timing（节奏）、Musicality（音乐性）、Technique（技术）、Difficulty（难度）、Partner Coordination（搭档配合）和Originality（原创性）。

**核心发现**：Groundtruth在所有六个维度上均显著高于InterGen和Duolando（$p < 0.001$），而InterGen和Duolando之间无显著差异。这一结果与Table 3的运动学指标形成对比——运动学指标显示Duolando在多项指标上优于InterGen，但人类评估者无法区分两者的整体质量。这暗示**运动学指标的细微差异可能超出了人类感知的辨别阈值**，而语义指标（Table 4）揭示的差距——两者在动作可辨识性上同样糟糕——更符合人类对“这不是真实舞蹈”的整体判断。

**维度级分析**：从Figure 4的柱状图可见，Groundtruth在Technique和Partner Coordination维度上的优势最为明显，这与熟练度估计器捕捉到的信息一致——真实舞者的技术执行和互动配合是当前生成模型完全无法复现的。在Musicality维度上，尽管生成模型在$BAS$（节拍对齐）指标上表现尚可（Table 3），人类评估仍认为其音乐性远逊于真实舞蹈，说明**音乐性远不止节拍对齐**，还涉及旋律诠释、动态响应等细粒度维度——这是当前运动学指标的盲区，也是论文在开放问题中明确指出的未来方向。

### 数据集特性的实验支撑

**Figure 2** 和数据集分析提供了理解实验结果的重要上下文。动作类别分布显示：入门舞者主要使用Basic Step，中级和专业舞者使用更广泛的30类动作（如Left Turn、Copa等）。专业舞者每场表演平均执行54.5个风格动作（styling moves），而中级为12.9个，入门仅5.1个。这种熟练度层级间的动作词汇差异是熟练度估计器能够达到84%+ F1的数据基础，也解释了为何生成模型在熟练度适配性上表现不佳——它们缺乏对不同熟练度层级动作分布差异的建模能力。

### 局限性与失败模式

1. **动作分割依赖预设边界**：当前所有任务依赖人工预设的8拍分割，自动动作分割仍是开放问题。若分割边界偏移，动作分类和可辨识性评估的准确性将受影响。

2. **客观-主观相关性未量化**：虽然Table 4的语义指标和Figure 4的人工评估在趋势上一致（生成方法远低于真实数据），但Move F1和Proficiency F1与人类Likert评分之间的直接相关性系数未被测量。这是论文明确承认的局限，也是该领域普遍存在的问题。

3. **数据集覆盖范围有限**：CoMPAS3D仅包含salsa单一舞种和9对舞者，Table 5的留出配对策略（每层级留出一对用于测试）虽然避免了模型记忆特定配对特征，但样本量有限意味着结论的统计稳健性需要更大规模验证。

4. **零样本VLM的评估污染风险**：如前述，零样本模型因类别偏置导致准确率虚高，若研究者未加验证地使用零样本VLM作为自动裁判，将得出严重误导性的结论。

### 重要图表索引

- **Table 2**：VLM自动裁判验证核心表——微调vs零样本的动作分类和熟练度估计性能，含单人/双人消融
- **Table 3**：运动学指标对比——Groundtruth、InterGen、Duolando在$FID_k$、$Div_k$、$FID_g$、$FID_{cd}$、$BED$、$BAS$上的表现
- **Table 4**：语义指标对比——Move Legibility F1和Proficiency Appropriateness F1，揭示运动学指标无法捕捉的深层差距
- **Figure 4**：人工评估结果——六个竞赛维度的5-point Likert评分，GT显著优于生成方法（$p < 0.001$）
- **Figure 2**：动作类别分布——入门/中级/专业舞者的30类动作使用频率差异，解释熟练度估计的数据基础
- **Table 5**：配对信息与测试集留出策略
- **Table 6**：完整标注词典——30类动作、风格标注和错误类型的定义
- **Table 8**：人工评估维度定义——来源于salsa竞赛评审准则

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/003_Figure_2.jpg]]
*Figure 2: Distribution over the 30 move classes (sorted by beginner move frequency) in CoMPAS3D for beginner, intermediate and pro pairs. Beginners tend to primarily use the “basic step”, which professionals use less. Instead, pros use a wider variety of moves such as left turns and copa*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/027_Figure_13.jpg]]
*Figure 13: Confusion matrices for legibility using both zero-shot and fine-tuned InternVL3 models, reported in Table 4*

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/028_Figure_14.jpg]]
*Figure 14: Confusion matrices for appropriateness using both zero-shot and fine-tuned Qwen2.5-VL models, reported in Table 4*

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2507_19684/figures/002_Table_1.jpg]]
*Table 1: Comparison of publicly available dance datasets capturing human-human interaction (HHI). T¯/s represents the average duration per sequence in seconds. Pairs/Genre highlights the depth of coverage within a single movement vocabulary: DD100 captures 0.5 pairs per genre across 10 ballroom styles, and InterDance’s pairs per genre is unknown across 15 genres, whereas CoMPAS3D dedicates all 9 pairs to a single genre, similar to a richly annotated dataset in English rather than shallow coverage across multiple languages*



## 定位与知识库关联

### 1. 任务定义与类比框架

CoMPAS3D 将双人即兴舞蹈建模为一种**非语言交互对话**，并据此定义了三项基准任务：

- **动作分类（Move Classification）**：类比语音转写（transcription），识别给定动作序列中正在执行的 salsa 动作类别。
- **熟练度估计（Proficiency Estimation）**：类比第二语言习得中的流利度评估，从动作序列中推断舞者或舞对的技能层级。
- **跟舞生成（Follower Generation）**：类比对话响应生成，给定领舞动作、共享音乐和目标熟练度层级，预测跟舞者的动作序列。

这一类比框架的核心洞察在于：将舞蹈视为一种共享“动作词汇”的交流系统。动作分类检测生成动作是否在该词汇内可辨识（move legibility），熟练度估计检测生成动作是否匹配目标熟练度层级（proficiency appropriateness）——这两个语义维度是传统运动学指标（如 $FID_k$、$BAS$）完全无法捕捉的。

### 2. 与现有数据集的定位关系

Table 1 将 CoMPAS3D 与现有公开双人舞蹈数据集进行了系统对比。关键差异体现在三个维度：

- **即兴性**：AIST++、DanceDB、DD100 等数据集以编舞表演为主，舞者按预设动作序列执行；CoMPAS3D 采集的是即兴 salsa 双人舞，领舞实时决策、跟舞即时响应，更贴近真实交互场景。
- **动作标注粒度**：现有数据集缺乏细粒度动作类别标签。CoMPAS3D 提供了 30 类 salsa 动作的专家标注，覆盖动作类型、风格元素和执行错误三个维度（完整词典见 Table 6）。
- **熟练度层级**：CoMPAS3D 是首个按熟练度（入门/中级/专业）分层标注的双人舞蹈数据集，每层级包含 3 对舞者，总计时长约 3 小时、超过 2800 个标注片段。

这些差异使得 CoMPAS3D 填补了一个关键空白：现有评估体系仅依赖运动学指标，而 CoMPAS3D 的标注结构使得语义层面的可辨识性和适配性评估成为可能。

### 3. 评估体系的方法谱系

CoMPAS3D 的评估框架包含三个层级，逐层从运动学表层深入到语义深层：

**层级一：运动学指标（继承自现有范式）**
沿用交互运动生成领域的标准指标：$FID_k$（运动学特征 Fréchet 距离）、$FID_g$（图形特征 Fréchet 距离）、$FID_{cd}$（跨距离交互质量）、$Div_k$/$Div_g$/$Div_{cd}$（多样性）、$BED$（领舞-跟舞节拍同步性）、$BAS$（动作-音乐节拍对齐）。这些指标衡量动作的物理真实性和节拍一致性，但无法评估语义层面的可辨识性和适配性。

**层级二：客观语义指标（本文核心贡献）**
利用专家标注语料微调 VLM 作为“自动裁判”，将语义评估转化为可量化的客观指标：
- **动作可辨识性（Move Legibility）**：通过微调 InternVL3 作为动作分类器，计算生成跟舞动作的 Move F1 分数。该分类器在真实数据上 dyadic F1 达 51.09（Table 2），验证了其作为评估工具的可靠性。
- **熟练度适配性（Proficiency Appropriateness）**：通过微调 Qwen2.5-VL 作为熟练度估计器，计算生成动作与目标熟练度层级的匹配 F1。该估计器在真实数据上 dyadic F1 达 84.53（Table 2）。

**层级三：主观评估（对齐真实竞赛标准）**
采用 salsa 竞赛的 6 个评审维度（timing、musicality、technique、difficulty、partner coordination、originality）进行 5-point Likert 人工评分，替代现有工作中常用的 3 维度评估（motion quality、music-motion alignment、partner coordination）。

### 4. 基线方法及其在评估框架中的表现

论文选取两个代表性基线进行跟舞生成评测：

- **Duolando**：舞蹈专项跟舞生成模型，针对 salsa 等双人舞场景设计。
- **InterGen**：通用人-人交互生成模型，覆盖更广泛的交互类型。

在运动学指标层面（Table 3），两者表现可比：Duolando $FID_k=10.47$，InterGen $FID_k=23.23$，均与 Groundtruth（$FID_k=0.00$）存在差距但处于同一数量级。然而，在客观语义指标层面（Table 4），两者均暴露出严重的语义缺陷：

- **动作可辨识性**：InterGen Move F1=7.69，Duolando Move F1=6.70，远低于 Groundtruth 的 53.55。这意味着生成动作在 salsa 动作词汇内几乎不可辨识——模型生成的“舞蹈”在语义层面不是有效的 salsa 动作。
- **熟练度适配性**：Duolando Proficiency F1=22.47，InterGen Proficiency F1=37.12，均低于 Groundtruth 的 51.64。

人工评估（Figure 4）进一步确认了这一差距：Groundtruth 在所有 6 个竞赛维度上均显著高于两个生成方法（$p < 0.001$），而 InterGen 与 Duolando 之间无显著差异。这揭示了当前运动生成评估的关键盲区：运动学指标接近真实数据，但语义层面远未达标。

### 5. 消融洞察与适用边界

**VLM 微调的必要性**：零样本 VLM 在动作分类和熟练度估计上 F1 极低（InternVL3 零样本 Move F1=7.74，Qwen2.5-VL 零样本 Proficiency F1=38.87），且存在严重的类别偏置——倾向于将所有片段预测为高频类别（如 Basic Step 或 Beginner），导致准确率虚高但 F1 极低。微调后模型在所有类别上产生更均衡的预测（Figure 9–12），F1 提升超过 43 个百分点。

**双人信息的增益**：dyadic 设置在动作分类和熟练度估计上一致优于单人（follower-only）设置（Table 2），表明领舞动作携带了额外的动作识别信息。特别地，单人熟练度估计远难于双人估计，提示交互动态中包含重要的熟练度线索。

**数据集边界**：当前数据集仅覆盖 salsa 单一舞种和 9 对舞者（Table 5），熟练度估计测试集采用留出配对策略以避免模型记忆特定配对特征，但样本量有限。泛化至其他舞种或文化背景需独立验证。此外，动作标注由一位 15 年经验专家完成并经第二位专家抽样验证（Cohen's Kappa=0.752），但标注者偏差可能存在。

### 6. 开放问题与后续方向

1. **自动动作分割**：当前任务依赖人工预设的 8 拍分割边界，连续即兴舞蹈的自动动作边界检测仍是开放问题，是实现端到端转写的关键瓶颈。
2. **客观-主观相关性验证**：语义客观指标（Move F1、Proficiency F1）与人工判断之间的直接相关性尚未测量，这一局限在当前运动生成评估领域普遍存在，需要正式量化研究。
3. **语言学指标的迁移**：能否借鉴 BLEU 等 NLP 指标来量化生成动作序列的语义保真度，将舞蹈评估进一步形式化？
4. **接触与触觉信号**：salsa 双人舞中的手部接触力/触觉信号尚未纳入标注和评估体系，这对评估交互质量至关重要。
5. **音乐性细粒度评估**：当前 $BAS$ 仅衡量节拍对齐，如何评估生成动作对旋律、乐器、情绪等音乐维度的响应？
6. **跨舞种泛化**：该评估框架能否迁移至 salsa 以外的舞种或其他即兴双人互动领域（如武术对练、手语对话）？
7. **安全风险**：若数据集被用于开发与真人共舞的机器人，需通过虚拟/增强现实或物理仿真器进行接触事故规避测试。



## 原文 PDF

![[paperPDFs/arxiv_2025/CoMPAS3D:_A_Dataset_and_Benchmark_for_Interactive_Motion.pdf]]
