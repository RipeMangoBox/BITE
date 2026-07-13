---
title: "VideoNet: A Large-Scale Dataset for Domain-Specific Action Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VideoNet_A_Large_Scale_Dataset_for_Domain_Specific_Action_Recognition.pdf
project_link: null
code_link: null
aliases:
- VideoNet
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 为VLMs提供领域特定、经过自动标注和严格过滤的训练数据（尤其是通过SingleAction策略筛选的高质量视频QA对），并基于此进行微调，能够从根本上提升模型对领域内多样动作的识别能力。该策略使4B模型在多个指标上超越未经微调的8B通用模型。
primary_logic: 领域特定动作识别是一项对感知和组合推理要求极高的任务，现有的通用VLM基准难以充分评估。通过引入“硬负样本”（hard negatives）和创新的非专家标注流水线，可以在控制成本的同时构建高可靠性的评估数据集；而利用视频标题、语音转录等弱信号自动构建训练集的SingleAction过滤策略，证明了在资源有限的情况下，数据质量远比数据规模更能决定下游性能。即“更强的领域内监督”是解锁小模型潜力、补足VLM短板的关键。
claims:
- 开放权重8B模型（如Qwen3-VL-8B）在多项选择题基准上仅取得45.0%的准确率，与闭源模型Gemini 3.1 Pro的69.9%存在显著差距，反映领域特定动作识别的巨大挑战。
- 微调后的4B模型（Molmo2-4B FT）在二分类零样本设置下达到66.6%的准确率，超越所有8B开源模型，证明领域特定训练数据的价值。
- 在3-shot少样本设置下，非专家人类准确率提升13.6个百分点（达82.7%），而VLMs平均仅提升约2.9个百分点（Qwen3-VL提升7.0%，Gemini 3.1 Pro甚至下降4.8%），突显模型缺失人类般的少样本学习能力。
- 专家对620个剪辑的验证显示基准标签正确率达97.6%，证明所提出的非专家标注流水线结合硬负样本生成是收集高质量领域特定数据的可靠方法。
---

# VideoNet: A Large-Scale Dataset for Domain-Specific Action Recognition

> [!tip] 核心洞察
> 领域特定动作识别是一项对感知和组合推理要求极高的任务，现有的通用VLM基准难以充分评估。通过引入“硬负样本”（hard negatives）和创新的非专家标注流水线，可以在控制成本的同时构建高可靠性的评估数据集；而利用视频标题、语音转录等弱信号自动构建训练集的SingleAction过滤策略，证明了在资源有限的情况下，数据质量远比数据规模更能决定下游性能。即“更强的领域内监督”是解锁小模型潜力、补足VLM短板的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoNet：面向领域特定动作识别的大规模数据集 |
| 英文题名 | VideoNet: A Large-Scale Dataset for Domain-Specific Action Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.02834) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoNet (带硬负样本的领域特定动作基准 + 自动训练数据构建及微调方案) |
| Dataset | VideoNet Multiple-Choice, VideoNet Binary 0-shot |

> [!tip] 效果简介
> - VideoNet Multiple-Choice 上，Accuracy (%) 53.5 (Molmo2-4B FT) vs 45.0 (Qwen3-VL-8B, 最佳开源8B) (+8.5)。
> - VideoNet Binary 0-shot 上，Accuracy (%) 66.6 (Molmo2-4B FT) vs 59.3 (Qwen3-VL-8B) (+7.3)；Accuracy (%) 66.6 (Molmo2-4B FT) vs 70.3 (Gemini 3 Flash, 闭源基线) (-3.7)。

## 概要

**VideoNet** 是一个面向领域特定动作识别（domain-specific action recognition）的大规模基准与训练数据集，覆盖 **7大类别、37个领域、1,000种细粒度动作**，并配套提供近50万自动构建的视频问答对用于模型微调。

**核心问题**：当前视觉语言大模型（VLMs）在通用基准上表现强劲，但在需要精细运动理解和组合推理的领域特定动作识别任务上暴露出显著短板。以多项选择题为例，最佳开源8B模型 **Qwen3-VL-8B** 仅取得45.0%的准确率，与闭源模型 **Gemini 3.1 Pro** 的69.9%存在近25个百分点的巨大差距。在更宽松的二元零样本设置下，开源模型同样难以突破60%的瓶颈。这一差距的根源在于：模型缺乏大规模、高质量的领域特定训练数据，难以将已有的文本知识有效映射到视频中的细微运动细节，且其少样本上下文学习能力远弱于人类。

**核心方案**：本文提出一套完整的“数据-评估-微调”闭环方案。在评估侧，通过三阶段人工标注流水线结合LLM生成的**硬负样本**（hard negatives），构建了高可靠性基准（专家验证准确率97.6%）；在训练侧，利用自动流水线（Gemini 2.5 Flash视频定位 + WhisperX转录对齐 + **SingleAction** 过滤策略）从网络视频中提取约16.2万高质量视频QA对。基于此对 **Molmo2-4B** 进行指令微调后，该4B模型在多项选择上达到53.5%，超越所有开源8B模型；在二元零样本上达到66.6%，逼近闭源模型 **Gemini 3 Flash**（70.3%），验证了“更强的领域内监督”是补足VLM短板的关键杠杆。

**关键发现**：
- **数据质量压倒规模**：在三种过滤策略中，样本量最小的SingleAction（162K）反而取得最高下游准确率，证明精确标注远比数据体量重要。
- **微调解锁时域建模能力**：从单帧切换到全视频输入，微调模型准确率提升+7.7个百分点，而开源VLM仅提升1~2个百分点，说明领域特定训练使模型真正学会了利用视频时序信息。
- **少样本学习的人机鸿沟**：在3-shot设置下，非专家人类准确率提升13.6个百分点（达82.7%），而VLMs平均仅提升约2.9个百分点，部分模型甚至出现性能倒退，揭示当前架构缺乏人类般的视觉归纳偏差。

**方法定位**：VideoNet在方法谱系上属于**领域特定基准构建 + 自动训练数据生成 + 小模型领域微调**的交叉工作。与通用视频理解基准（如Kinetics、ActivityNet）不同，它强调同一领域内细粒度动作的判别难度；与已有的领域特定基准（如FineDiving、SurgicalActions）相比，它在覆盖领域广度与动作深度上均大幅超越。在数据构建策略上，其“硬负样本生成”与“SingleAction弱信号过滤”为资源受限场景下的高质量数据获取提供了可复用的范式。

### 领域特定动作识别的核心挑战

动作识别是视频理解领域的基石任务之一。近年来，多模态大语言模型（VLMs）在通用视频问答和描述生成上展现出令人瞩目的能力，但当任务聚焦于**领域特定动作**——例如识别一个滑板动作是“Kickflip”还是“Heelflip”、判断一段医疗视频中是否出现了“Romberg征”——时，现有模型的性能急剧下降。这一现象揭示了当前VLM能力边界中的一个关键瓶颈：**模型缺乏对大量细粒度、领域特定动作的先验理解**，且难以将自身丰富的文本知识有效映射到视频中的细微运动线索上。

问题的根源在于数据。通用VLM的预训练语料以大规模互联网图像和视频文本对为主，这些数据对常见物体和粗粒度动作覆盖较好，但几乎不包含专业领域的动作标注。以滑板、医疗检查、乐器演奏等为代表的37个领域中的1000种动作，绝大多数从未在开源训练集中以结构化形式出现。这种**领域特定训练数据的系统性缺失**，使得VLM在面对此类任务时，本质上是在进行“零样本猜测”，而非真正的视觉-运动理解。

### 现有基准的评估盲区

现有的视频理解基准（如Kinetics、Something-Something、ActivityNet）主要面向通用动作或日常活动，其动作类别通常较为宽泛（如“跑步”、“弹吉他”），且负样本往往与正样本在场景、物体层面存在显著差异，模型仅凭单帧中的物体识别即可获得较高分数。这种评估设计无法有效测量模型对**运动细节的感知能力**和**组合推理能力**——而这两者恰恰是领域特定动作识别的核心要求。

例如，区分“French press”与“pour-over”两种咖啡冲泡方式，模型必须理解水流控制、器具操作顺序等时序细节，而非仅仅识别画面中出现了咖啡壶。现有基准中缺乏此类需要精细运动理解的“硬负样本”，导致评估结果高估了模型的真实动作理解水平。

### 少样本学习的巨大鸿沟

另一个关键动机来自人类与VLM在**视频上下文学习能力**上的显著差异。实验表明，当为非专家人类提供3个动作示例视频后，其识别准确率可从69.1%跃升至82.7%（提升13.6个百分点）；而在相同条件下，VLM的平均提升仅为约2.9个百分点。更令人惊讶的是，部分闭源模型（如Gemini 3.1 Pro）在引入少样本示例后准确率反而下降4.8个百分点。这一“人机少样本学习鸿沟”表明，现有VLM的上下文学习机制远未达到人类从少量示例中提取关键运动模式的能力，亟需从数据、模型架构和评估方法三个维度进行系统性改进。

### 本文的核心动机

综上所述，本文的核心动机可归纳为三个层面：

1. **数据层面**：构建首个大规模、高质量的领域特定动作识别基准和训练数据集，填补通用VLM在此类任务上的数据空白。
2. **评估层面**：通过引入“硬负样本”设计和非专家标注流水线，建立一个能够真实反映模型细粒度运动理解能力的评估框架，而非依赖物体识别捷径。
3. **能力层面**：探索领域特定训练数据能否使小模型（4B参数）在领域内任务上超越未经微调的通用大模型（8B参数），并揭示VLM在少样本视频学习中的根本性缺陷。

这三个层面的工作共同指向一个核心命题：**在资源有限的情况下，更强的领域内监督信号——而非更大的模型规模或更多的测试时计算——才是解锁精细动作识别能力的关键**。

## 核心方法与创新机理

VideoNet的核心创新并非提出一种新的模型架构，而是通过**系统性地改造数据生态**——包括评估基准的设计逻辑和训练数据的构建方式——来诊断并缓解视觉语言模型（VLM）在领域特定动作识别中的根本性短板。其创新点可归纳为两个关键的“changed slots”，分别对应评估与训练两个维度。

### 1. 评估维度：引入“硬负样本”以暴露细粒度感知瓶颈

现有视频理解基准中的负样本通常与正样本差异显著，模型可依赖场景、物体等简易线索“投机取巧”，从而高估其真实动作识别能力。VideoNet改变了这一评估逻辑，将负样本的生成从“随机选取”转变为“对抗性构造”。

具体而言，作者设计了一条**硬负样本生成流水线**（Section 3.4）：首先利用LLM（GPT-4.5-preview）为每个动作生成候选硬负样本，这些负样本在语义上与正样本高度相似，仅在细微的运动线索上存在差异（例如，“反手击球”vs“正手击球”）；随后，使用推理模型（o3）对候选集进行修正与平衡，确保负样本的难度可控且与正样本构成有意义的对比。

这一创新的因果效应在实验中得到了清晰验证（Table 5）：当评估设置从随机负样本切换为硬负样本时，GPT-5.4的3-shot准确率从81.0%骤降至76.3%，非专家人类的准确率也从93.6%下降至82.7%。硬负样本使得基准的难度更真实地反映了细粒度动作识别所需的**精细运动感知与组合推理能力**，而非简单的场景分类。

### 2. 训练维度：以“数据精确度”取代“数据规模”的自动标注策略

领域特定动作识别的一个关键瓶颈在于缺乏大规模、高质量的训练数据。VideoNet的解决方案并非简单地堆砌数据量，而是提出了一种**基于弱信号自动构建训练集、并通过严格过滤策略确保数据精确度**的流水线（Section 4.1）。

该流水线包含三个核心模块：
- **视频定位**：使用Gemini 2.5 Flash从专业教学视频中自动定位包含目标动作的剪辑片段。
- **转录对齐**：利用WhisperX生成语音转录的时间戳，将文本描述与视频片段对齐。
- **多策略过滤**：设计了三种递进的过滤策略——TranscriptLocalized（基于转录定位）、TranscriptLocalizedTitleMatch（额外要求标题匹配）、以及SingleAction（仅保留每个剪辑中单一动作的样本）。

最具创新性的发现来自**SingleAction策略**（Table 6）：尽管该策略产生的训练样本容量最小（约16.2万剪辑），其在多项选择和二分类评估上的准确率却**显著超越**了数据量更大的其他两种策略。具体而言，使用SingleAction数据微调的Molmo2-4B在多项选择上比TranscriptLocalized策略高出约5个百分点。这一结果揭示了一个反直觉的规律：在领域特定动作识别中，**数据质量（单一动作的纯净度）远比数据规模更能决定下游性能**。

### 3. 创新点的协同效应

上述两个创新并非孤立存在，而是形成了闭环验证：硬负样本评估暴露了通用VLM在缺乏领域内监督时的感知脆弱性，而SingleAction训练数据的有效性则证明了“更强的领域内监督”是解锁小模型潜力的关键杠杆。这一协同效应的最佳证据是：仅4B参数的微调模型Molmo2-4B FT在二分类零样本设置下达到66.6%的准确率，超越了所有未经微调的8B开源模型（如Qwen3-VL-8B的59.3%），并逼近闭源模型Gemini 3 Flash的70.3%（Table 4）。这充分说明，VideoNet的创新核心在于**通过数据生态的重新设计，以极低的模型参数量代价换取了领域特定能力的显著跃升**。

VideoNet 的完整技术栈由两条主线构成：**领域特定动作识别基准的构建**与**训练数据的自动生成及模型微调**。二者共享同一套动作分类法（taxonomy），但服务于不同的目的——前者用于严格评估，后者用于提升模型能力。

### 基准构建流水线

基准的构建遵循“自上而下定义动作空间 → 人工采集剪辑 → 硬负样本生成”的三阶段流程。

**阶段一：动作分类法构建。** 研究者采用自上而下（top-down）的方法，首先划定 7 大类别（如 Sports、Medical、Arts 等），再在每类下细分出共 37 个领域，最终为每个领域定义一组领域特定动作，总计 1,000 个动作。动作列表的来源混合了专家编写的社区资料（如滑板博客中的动作名）与 LLM 的扩充生成，确保覆盖面与专业性的平衡。

**阶段二：人工三阶段标注流水线。** 给定一个动作名及其文本定义，非专家标注者按以下步骤为每个动作采集 5 个高质量剪辑（参见 Figure 3）：
1. **网络检索**：在公开视频平台中搜索并定位包含该动作的片段；
2. **多数投票验证**：三名标注者对剪辑是否确实包含目标动作进行独立判断，取多数票作为去噪依据；
3. **精细修剪**：对通过验证的剪辑进行起止边界的精确裁剪，去除冗余内容。

该流水线的可靠性得到了专家验证的背书：专家对 620 个剪辑的抽查显示，基准标签正确率达到 **97.6%**（Table 1），证明非专家标注配合多重投票机制是收集高质量领域特定数据的可行方案。

**阶段三：硬负样本生成。** 为提升评估的难度和生态效度，VideoNet 不采用随机负样本，而是引入“硬负样本”（hard negatives）——即与正样本在视觉场景、物体构成上高度相似，仅在细微运动线索上存在差异的负例。生成流程为：先用 LLM（GPT-4.5-preview）为每个正样本生成候选硬负样本，再用推理模型（o3）对候选集进行修正和平衡，确保负样本的难度可控且不引入系统性偏差。

### 训练数据自动生成流水线

训练数据的构建同样依赖自动化流水线，目标是低成本地生成大规模视频问答对：

1. **视频爬取与剪辑定位**：从互联网爬取领域相关的专业视频（如教程、演示），使用 Gemini 2.5 Flash 作为时间定位器，自动提取包含目标动作的视频片段；
2. **转录对齐**：利用 WhisperX 对视频进行语音转录，并获取时间戳信息；
3. **过滤与标注**：基于视频标题和转录文本，采用三种过滤策略生成带标签的 QA 对：
   - **TranscriptLocalized**：仅依赖转录时间戳定位动作；
   - **TranscriptLocalizedTitleMatch**：在前者基础上增加标题匹配约束；
   - **SingleAction**：最严格的过滤策略，确保每个剪辑仅包含单一动作，最终产出约 16.2 万剪辑。

### 模型微调

在构建好的领域特定 VQA 数据集上，对开源模型 **Molmo2-4B** 进行指令微调。微调配置为 4 fps 采样、最大 64 帧输入，并在输入中编码时间戳信息，以增强模型的时域建模能力。

### 输入输出流总览

整个框架的信息流可以概括为：

```
动作分类法（1,000 actions, 37 domains）
        │
        ├──→ 人工标注流水线 ──→ 基准测试集（含硬负样本）
        │                              │
        │                              ↓
        │                    多项选择 / 二元少样本评估
        │
        └──→ 自动训练数据流水线 ──→ 领域特定 VQA 数据集
                                       │
                                       ↓
                                 Molmo2-4B 微调
                                       │
                                       ↓
                                 微调模型评估
```

该设计的一个核心洞察是：**数据质量远比数据规模更能决定下游性能**。在三种过滤策略中，样本容量最小的 SingleAction（162K）反而在多项选择和二分类上均取得最高准确率（Table 6），而产量最大的 TranscriptLocalized 策略表现最差。这表明，在资源有限的情况下，通过严格的过滤机制获得“更强的领域内监督信号”，是解锁小模型潜力、补足 VLM 短板的关键路径。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/005_Figure_3.jpg]]
*Figure 3: | Benchmark data collection pipeline, as described in Section 3.2. Given an action name and definition, humans (1) find clips on the web, (2) remove outliers among these clips, and (3) fix the clip trimmings. This pipeline yields five well-trimmed clips per action*

VideoNet 的核心架构并非提出全新的神经网络模块，而是围绕**数据构建与评估范式**设计了多条创新流水线。其关键模块可归纳为三个层次：基准构建、训练数据自动生成、以及模型微调策略。

### 1. 领域动作分类法构建

论文采用**自上而下（top-down）**的方法构建动作分类体系。首先定义7大类别（如Sports、Medical、Arts等），再细分为37个领域（如Basketball、Diving、Surgery等）。对于每个领域，动作列表的来源有两类：

- **专家书面资料**：例如，滑板动作从权威滑板博客中提取。
- **大语言模型增强**：利用LLM对专家列表进行扩充，并通过交叉验证确保定义的准确性。

最终基准覆盖 **1,000 个独特动作**，每个动作配有文本定义，确保评估的语义清晰度。

### 2. 基准数据三阶段人工标注流水线

如图 Figure 3 所示，该流水线包含三个顺序阶段：

1. **网络检索（Find）**：非专家标注者根据动作名称和定义，在互联网上搜索并下载候选视频片段。
2. **多数投票验证（Verify）**：三个独立标注者对每个片段进行审核，采用多数投票机制剔除离群值，确保片段确实包含目标动作。
3. **精细修剪（Trim）**：对通过验证的片段进行精确的时间边界裁剪，去除冗余帧，最终每个动作保留5个高质量剪辑。

专家对620个剪辑的验证显示，该流水线的标签正确率达 **97.6%**（Table 1），证明非专家标注结合多重验证的可靠性。

### 3. 硬负样本生成模块

为提升基准的难度和区分度，VideoNet 引入**硬负样本（hard negatives）**生成机制，而非使用随机负样本。其生成流程为：

- **候选生成**：使用 **GPT-4.5-preview** 为每个正样本动作生成高度相似但关键运动线索不同的候选负样本。
- **推理模型精炼**：利用 **o3 推理模型**对候选集进行修正和平衡，确保负样本与正样本在场景、物体、背景上相似，仅在细微动作上存在差异。

硬负样本的引入使基准更真实地反映细粒度动作识别的困难。例如，GPT-5.4 在 3-shot 设置下，从随机负样本的 81.0% 降至硬负样本的 76.3%；人类同样从 93.6% 降至 82.7%（Table 5）。

### 4. 自动训练数据生成流水线

为构建领域特定的微调数据集，论文设计了一条低成本自动流水线，核心步骤为：

1. **视频爬取与定位**：从互联网爬取专业教学/教程视频，使用 **Gemini 2.5 Flash** 作为定位器，提取候选动作片段。
2. **转录对齐**：利用 **WhisperX** 进行语音转录，获取时间戳信息。
3. **过滤与标注**：基于视频标题和转录文本，设计三种过滤策略：
   - **TranscriptLocalized**：仅依赖转录定位。
   - **TranscriptLocalizedTitleMatch**：转录定位 + 标题匹配。
   - **SingleAction**：最严格的策略，仅保留标题中明确提及且转录中唯一出现的单一动作片段。

三种策略产生的数据量递减（SingleAction 仅约 16.2 万剪辑），但下游性能却呈反向关系——SingleAction 在多项选择和二分类上均取得最高准确率（Table 6），证明了**数据精确度远胜于规模**。

### 5. 微调策略

微调基于 **Molmo2-4B** 模型进行指令微调，关键配置为：

- **帧采样**：以 4fps 采样，最大输入 64 帧。
- **时间戳编码**：在输入中编码时间戳信息，增强时域感知。
- **训练数据**：使用 SingleAction 过滤策略生成的领域特定 VQA 对。

微调后的 4B 模型在多项选择上达到 53.5%，超越所有 8B 开源模型（最佳为 Qwen3-VL-8B 的 45.0%）；在二分类零样本下达到 66.6%，仅比闭源 Gemini 3 Flash 低 3.7 个百分点（Table 3, Table 4）。

### 关键公式与变量

本文未提出新的数学公式或损失函数。其方法论贡献集中在数据构建流水线的工程设计和评估范式创新，而非模型架构或优化目标的数学推导。所有实验均基于标准的多项选择交叉熵损失和指令微调框架，未引入自定义公式。

如需了解具体的评估指标计算方式，多项选择准确率定义为：

$$\text{Accuracy}_{\text{MC}} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}[\hat{y}_i = y_i]$$

其中 $N$ 为问题总数，$\hat{y}_i$ 为模型预测的动作选项，$y_i$ 为真实动作标签。二分类准确率同理，正负样本各半，随机基线为 50%。

## 实验与关键发现

### 主要结果：多项选择与二元零样本评估

VideoNet 在多项选择（Multiple-Choice）和二元零样本（Binary 0-shot）两种设定下对现有视觉语言模型（VLM）进行了系统评估。核心发现是：**领域特定动作识别对当前 VLM 构成了远超通用视频理解基准的挑战**，且开源模型与闭源模型之间存在巨大鸿沟。

在多项选择设定中（Table 3），性能最优的开源 8B 模型 **Qwen3-VL-8B** 仅取得 45.0% 的总体准确率，而闭源模型 **Gemini 3.1 Pro** 达到 69.9%，二者差距高达 24.9 个百分点。其他闭源模型（Gemini 3 Flash 68.7%、GPT-5.4 68.0%、GPT-5 67.6%）均聚集在 68–70% 区间，表明闭源模型已接近某种性能平台。值得注意的是，经 **SingleAction 策略** 过滤的领域特定数据微调后的 **Molmo2-4B FT** 达到 53.5%，不仅超越所有开源 8B 模型（+8.5 pp），还缩小了与闭源模型的差距——这一 4B 模型的表现证明，**领域内监督信号的质量远比模型参数量更为关键**。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/008_Table_3.jpg]]
*Table 3: | Multiple-choice evaluation results. Open models hover at 45%, while closed models fall just short of 70%. This sizeable gap suggests that VideoNet is challenging for existing VLMs, with high performance requiring larger models. A category-wise random baseline is the best accuracy attainable by guessing 1 letter for all questions in that category; the overall random baseline is the best accuracy attainable by guessing 1 letter for the entire benchmark. Highest accuracy for each column is in bold; highest accuracy by a non-proprietary model is underlined. Our fine-tuned model is in purple*

在二元零样本设定中（Table 4），任务难度降低（仅需判断视频中是否出现指定动作），但开源模型的困境依旧：Qwen3-VL-8B 仅 59.3%，而微调后的 Molmo2-4B FT 达到 66.6%，超越所有 8B 开源模型，仅落后 Gemini 3 Flash（70.3%）3.7 个百分点。然而，即使最优闭源模型 GPT-5 也仅取得 72.9%，表明**仅靠零样本推理难以突破领域动作识别的性能上限**，这直接引出了少样本学习的必要性。

### 少样本学习：人类与模型的根本差异

二元少样本（Binary Few-shot）实验揭示了 VLM 与人类在**上下文学习能力上的本质鸿沟**（Figure 5）。当提供 3 个上下文示例（3-shot）时，非专家人类在硬负样本设定下的准确率从 0-shot 的 69.1% 跃升至 82.7%（+13.6 pp），而 VLM 的平均提升幅度极为有限：Qwen3-VL 提升 7.0 pp，GPT-5.4 提升 5.7 pp，**Gemini 3.1 Pro 甚至下降 4.8 pp**。这一反常退化表明，某些模型不仅无法从示例中提取有效运动模式，反而被示例中的表面特征所干扰。模型间的少样本学习能力也呈现高度异质性：GPT-5.4 在 3-shot 硬负设定下达到 76.3%，而 Gemini 3.1 Pro 仅 65.1%，差距超过 11 pp。**VLM 缺失人类般的视频归纳学习能力，是当前领域动作识别的核心瓶颈之一。**

### 消融实验：视频输入与时域建模

对视频输入配置的系统消融（Table 11, Figure 4）揭示了几个关键洞察：

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/010_Figure_4.jpg]]
*Figure 4: | Ablations on video input configurations in the binary 0-shot setting. Open models show limited gains from full-video input, indicating difficulty in effectively leveraging video context. (A notable exception is our model, which benefits significantly.) GPT-5.4 shows only a slight improvement at higher fps, suggesting that test-time scaling via denser video sampling is insufficient for solving domain-specific action recognition*

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/025_Table_11.jpg]]
*Table 11: | Zero-shot results while varying video inputs. Performance gain from the previous setup is highlighted in blue and loss in red. Models are sorted by strongest to weakest overall performance in the default “video” input configuration. As expected, none of the models perform better when only given the center frame vs. the default video input. Notably, our fine-tuned model sees the biggest boost in accuracy from center frame input to the default, indicating its ability to leverage video inputs. The proprietary models benefit by less than half a percentage point when the action definition is added, suggesting that their language backbones possess sufficient world knowledge about the domain-spe...*

1. **从单帧到全视频的增益反映时域建模能力**：将输入从中心帧替换为完整视频，微调模型 Molmo2-4B FT 的准确率提升 +7.7 pp，而开源 8B 模型仅提升 +1～2 pp。这表明通用 VLM 难以有效利用视频中的时序信息，而领域微调能显著增强其时域建模能力。

2. **动作文本定义的价值有限**：在视频输入基础上额外提供动作的文本定义，闭源模型的增益不超过 0.5 pp，开源模型不超过 2 pp。这说明 VLM 的语言主干已具备较丰富的领域动作知识，**真正的瓶颈在于将文本知识映射到视频中的细微运动线索**。

3. **提高帧率收效甚微**：将 FPS 从 1 提高到 2 为 GPT-5.4 带来 +1.3 pp 增益，但继续提高到 4 fps 仅增加 +0.7 pp（Table 10）。测试时通过增加视频采样密度来提升性能的边际效益极低，进一步佐证了**领域特定训练数据**而非推理时算力投入，才是解决问题的关键路径。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/024_Table_10.jpg]]
*Table 10: | Impact of higher FPS sampling in 0-shot. Performance gain from the previous setup is highlighted in blue and loss is highlighted in red. The Qwen-3-VL series defaults to 2fps sampling, whereas GPT-5.4 recommends 1fps. While 2fps sampling does provide gains in both models, these gains are limited; in fact, they are smaller in magnitude than the gains yielded by providing an in-context example*

### 硬负样本的挑战性验证

硬负样本（Hard Negatives）是 VideoNet 区别于通用基准的核心设计。与随机负样本相比，硬负样本使 GPT-5.4 在 3-shot 下的准确率从 81.0% 降至 76.3%，人类从 93.6% 降至 82.7%（Table 5）。**硬负样本更真实地反映了细粒度动作识别的困难**：它们与正样本仅在细微运动线索上存在差异（例如“反手击球”与“正手击球”），迫使模型进行精细的时空推理，而非依赖物体识别或场景上下文等捷径。这一设计有效暴露了当前 VLM 在感知细微运动差异方面的不足。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2605_02834/figures/012_Table_5.jpg]]
*Table 5: | Accuracy with hard vs. random negatives. As intended, our selection of hard negatives makes the benchmark more difficult, especially for humans*

### 训练数据过滤策略：质量压倒规模

三种自动训练数据过滤策略的对比（Table 6）是本文最具启示性的消融发现：

- **TranscriptLocalized**（基于转录时间戳定位，约 500K 样本）
- **TranscriptLocalizedTitleMatch**（额外要求标题匹配，约 300K 样本）
- **SingleAction**（仅保留每个视频中单一动作的剪辑，约 162K 样本）

结果出人意料：**样本量最小的 SingleAction 策略在多项选择和二元零样本上均取得最高准确率**，在多项选择上比次优策略高出约 5 个百分点。其二元零样本准确率（66.6%）甚至超过了 Qwen3-VL-8B 的二元 3-shot 准确率（66.2%）。这一反直觉结果深刻说明：在资源有限的情况下，**数据精确度远胜于数据规模**——SingleAction 通过确保每个训练剪辑仅包含一个明确动作，避免了多动作剪辑带来的标签噪声，从而提供了更纯净的监督信号。

### 失败模式与局限性

尽管微调带来了显著提升，但分析也揭示了若干系统性失败模式：

1. **领域不均衡**：SingleAction 微调模型在 Beauty 和 Food 类别上表现持续较弱（Table 19）。Food 类别的动作常与特定物体或场景高度绑定（如“切洋葱”可通过砧板和洋葱识别，无需理解“切”的动作），可能高估模型能力；Beauty 类别则可能因训练数据质量不足导致微调后性能反而退化。

2. **部分领域微调倒退**：在 Coffee、Cooking、Gardening 等领域，基础模型的表现甚至优于微调模型（Table 21），暗示这些领域的自动标注训练数据存在标签噪声，未能提供有效的监督信号。

3. **CLIP 和 CNN 模型的严重不足**：作为对照，CLIP 模型在 VideoNet 上的零样本二元准确率最高仅 54.7%（Table 13），远弱于最差的 VLM；CNN 模型（以 kNN 评估）的表现虽与 Kinetics 准确率呈正相关，但整体水平同样远低于 VLM（Table 15）。这表明**领域特定动作识别需要超越静态视觉特征匹配的深层时序推理能力**。

4. **提示敏感性**：GPT-4o 和 GPT-4.1 在不同提示风格下总体准确率保持稳定，但正例和负例的准确率发生剧烈变化（Table 16），反映出模型存在严重的“是/否”回答偏差，而非真正的动作理解。

### 关键图表结论摘要

- **Table 3**：开源 8B 模型在多项选择上仅 45%，闭源模型约 70%，微调 4B 模型达 53.5%，证明领域特定训练数据的价值。
- **Table 4**：二元零样本下微调模型（66.6%）超越所有 8B 开源模型，逼近闭源模型水平。
- **Figure 5**：人类从少样本中获益 13.6 pp，VLM 平均仅 2.9 pp，Gemini 3.1 Pro 甚至负增长，暴露模型上下文学习能力的根本缺陷。
- **Table 6**：最小的 SingleAction 数据集（162K）带来最高性能提升，数据质量压倒规模。
- **Table 5**：硬负样本使模型和人类准确率均显著下降，更真实地反映细粒度动作识别的难度。
- **Table 11 / Figure 4**：微调模型从视频输入中获益最大（+7.7 pp），通用 VLM 的时域建模能力严重不足。

## 定位与知识库关联

### 与通用VLM基准的定位关系

VideoNet的提出并非要替代现有的通用视频理解基准（如ActivityNet、Kinetics），而是填补一个关键空白：**领域特定（domain-specific）动作的细粒度识别**。现有基准大多聚焦于日常通用动作（如“跑步”“喝水”），而VideoNet覆盖了7大类37个领域共1,000种动作——从咖啡拉花、神经科检查到木工榫接，其动作类别深度远超同类领域特定基准（Table 7）。这一定位使VideoNet成为评估VLM在专业垂直场景下感知与组合推理能力的“压力测试集”。

### 与基线模型的方法论关系

论文将现有VLM分为两个阵营进行对比：**开源8B量级模型**（Qwen3-VL-8B-Instruct、InternVL3.5-8B、Molmo2-8B）和**闭源大模型**（Gemini 3.1 Pro、Gemini 3 Flash、GPT-5.4、GPT-5）。核心发现是：

- **开源模型在多项选择基准上仅约45%准确率**，与闭源最强模型Gemini 3.1 Pro的69.9%存在约25个百分点的巨大鸿沟（Table 3）。这表明通用预训练数据中缺乏足够的领域特定动作知识，单纯扩大模型规模（从8B到闭源大模型）是当前缩小差距的主要路径，但代价高昂。
- **微调后的4B模型（Molmo2-4B FT）在二分类零样本设置下达到66.6%，超越所有开源8B模型**（Table 4），证明“更强的领域内监督”是比“更大的通用模型”更高效的路径。这一定位与**MPGD**（He et al., CVPR 2023）等参数高效微调工作的核心理念一致：针对特定任务的数据质量远比模型参数量更具杠杆效应。

### 核心方法论创新：数据质量驱动的范式

VideoNet的方法论贡献不在于提出新的模型架构或训练算法，而在于构建了一套**低成本、高可靠性的领域特定数据获取与评估体系**：

1. **硬负样本生成机制**：不同于传统基准中随机选取负样本，VideoNet使用GPT-4.5-preview生成候选硬负样本，再由o3推理模型进行修正和平衡（Section 3.4）。这些硬负样本与正样本仅在细微运动线索上存在差异，迫使模型进行真正的运动理解而非依赖场景或物体捷径。实验表明，硬负样本使GPT-5.4在3-shot下的准确率从81.0%（随机负）降至76.3%，人类也从93.6%降至82.7%（Table 5），更真实地反映了细粒度动作识别的困难本质。

2. **SingleAction数据过滤策略**：在自动训练数据构建中，论文对比了三种过滤策略——TranscriptLocalized（基于语音转录定位）、TranscriptLocalizedTitleMatch（转录+标题双重匹配）和SingleAction（仅保留标题中明确包含单一动作的视频）。结果显示，**样本量最小的SingleAction策略（约16.2万剪辑）在多项选择和二分类上均取得最高准确率**，相比次优策略提升约5个百分点（Table 6）。这一反直觉的发现确立了“数据精确度远胜于规模”的原则，与当前“大数据驱动”的主流范式形成鲜明对照。

### 适用边界与已知局限

VideoNet的方法论和数据集存在以下明确边界：

- **数据来源偏差**：训练数据主要来自教学/教程类视频（如YouTube的“How-to”内容），依赖视频标题和语音转录作为弱监督信号。这使得某些领域（如Coffee、Cooking）的标签噪声较高，微调模型在这些领域的表现甚至不如基础模型（Table 21），说明自动标注流水线在面对动作与场景强绑定的领域时存在系统性弱点。
- **评估格式的简化**：目前仅支持多项选择和二分类两种封闭式评估，虽能有效测量模型的辨别能力，但无法评估开放式动作描述或细粒度动作定位等更贴近实际应用场景的能力。
- **视频时长截断**：基准剪辑长度限制为5分钟（Table 8），可能丢弃某些长时程动作（如医疗缝合）的完整上下文，影响对模型时序理解能力的全面评估。
- **微调验证的单一性**：目前仅在Molmo2-4B单一架构上验证了训练数据的有效性，尚未探索其他模型家族（如Qwen系列、InternVL系列）或更大规模训练的迁移效果。

### 关键开放问题

1. **少样本学习的人机鸿沟**：在3-shot设置下，非专家人类准确率提升13.6个百分点（达82.7%），而VLMs平均仅提升约2.9个百分点（Figure 5）。Qwen3-VL提升7.0%已是最好表现，Gemini 3.1 Pro甚至下降4.8%。这一现象指向一个深层问题：当前VLM的视频上下文学习机制与人类的视觉归纳偏差存在根本差异，如何设计更有效的视频少样本提示策略（例如融合帧间差异、运动光流等显式运动表征）是亟待探索的方向。

2. **数据质量与规模的权衡边界**：SingleAction策略的成功证明“少而精”优于“多而杂”，但这一原则是否在所有领域都成立？是否存在某些“困难领域”（如需要极高时序精度的运动技巧），其性能突破需要更高的标注密度而非更严格的过滤？Table 21中基础模型在coffee、cooking等领域反而优于微调模型的现象，暗示当前过滤策略可能过度剔除了有用样本。

3. **从辨别到生成的评测升级**：多项选择/二分类的封闭式评估虽然可靠，但可能高估模型的真实理解能力——尤其是在Food等可通过物体检测捷径解决的类别上。引入开放式动作描述、时序定位等多模态评测方式，是推动领域特定动作理解研究深化的必要步骤。

4. **自动标注流水线的泛化性**：当前流水线严重依赖教学视频的结构化特征（标题明确、语音与视觉对齐），能否推广到监控视频、体育赛事、工业操作等缺乏显式文本锚点的场景，仍有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/VideoNet_A_Large_Scale_Dataset_for_Domain_Specific_Action_Recognition.pdf]]
