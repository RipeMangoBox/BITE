---
title: "GHOST: Getting to the Bottom of Hallucinations with A Multi-round Consistency Benchmark"
type: paper
paper_level: A
venue: WACV
year: 2026
pdf_ref: paperPDFs/WACV_2026/GHOST_Getting_to_the_Bottom_of_Hallucinations_with_A_Multi_round_Consistency_Benchmark.pdf
aliases:
- GHOST
tags:
- WACV_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "提出物体级别的组合三元组与多轮一致性检查框架，通过构建困难负样本并计算GHOST一致性分数（GCS）来惩罚不一致性。"
primary_logic: "多轮一致性检查能够揭露模型在回答多个相关问题时自相矛盾的隐藏幻觉，即使整体准确率较高也可能存在严重不一致；通过精心设计的负样本和一致性度量，可以更精确地评估模型真实的物体级理解能力。"
claims:
- "Figure 2 显示：随着负样本增加，准确率上升但无幻觉样本比例下降，证明准确率可能掩盖幻觉。"
- "GCS公式根据假阳性和假阴性数量的加权几何平均来惩罚幻觉，强调一致性而非单纯正确率。"
- "在Table 4中，跨三元组的GCS(OAR)远低于单独评估，揭示跨组件的累积不一致性。"
- "Table 8显示GPT-4o在POPE上87.0，但在GHOST上GCS仅63.9，证明GHOST能揭示更深层次的幻觉。"
---

# GHOST: Getting to the Bottom of Hallucinations with A Multi-round Consistency Benchmark

> [!tip] 核心洞察
> 多轮一致性检查能够揭露模型在回答多个相关问题时自相矛盾的隐藏幻觉，即使整体准确率较高也可能存在严重不一致；通过精心设计的负样本和一致性度量，可以更精确地评估模型真实的物体级理解能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GHOST：通过多轮一致性基准深入揭示幻觉 |
| 英文题名 | GHOST: Getting to the Bottom of Hallucinations with A Multi-round Consistency Benchmark |
| 会议/期刊 | WACV 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/WACV2026/papers/VS_GHOST_Getting_to_the_Bottom_of_Hallucinations_with_A_Multi-round_WACV_2026_paper.pdf); [Project](https://vibashan.github.io/ghost-web/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | GHOST |
| Dataset | GHOST vs. POPE/AMBER (GPT-4o), GHOST (Overall), Consistency Check Rounds |

> [!tip] 效果简介
> - GHOST vs. POPE/AMBER (GPT-4o) 上，Score 为 GHOST GCS 63.9，对比 POPE Acc 87.0, AMBER Score 91.4，变化 lower consistency (-23.1 vs. POPE)。
> - GHOST (Overall) 上，GCS 为 GPT-4o: 69.0，对比 Tiny MLLMs average GCS < 53，变化 large gap (> 16 points)。
> - Consistency Check Rounds 上，Hallucination-free rate 为 Decreases as more checks are added，对比 Accuracy increases with more checks，变化 contradicts accuracy improvement。

## 概述

### 1. 问题背景与核心瓶颈

多模态大语言模型（MLLM）在视觉理解任务中常产生“幻觉”——即生成与图像内容不符的描述。现有幻觉评估基准（如 **POPE**（Li et al., EMNLP 2023）、**AMBER**（Wang et al., 2024）等）主要依赖图像级别的准确率或 F1 分数，存在一个根本性盲区：**准确率等独立指标无法反映模型的自相矛盾**。即使模型整体准确率较高，其在回答关于同一物体的多个相关问题时，可能给出相互冲突的答案，而这种隐藏的不一致性恰恰是幻觉的深层表现。

GHOST 通过图 Figure 2 的证据直接揭示了这一瓶颈：随着负样本数量增加，模型的准确率反而上升，但“无幻觉物体”的比例却持续下降。这意味着，**准确率可能掩盖幻觉**，单纯依靠正确率评估会严重低估模型的真实幻觉程度。

### 2. 核心方法定位

GHOST（**G**etting to the **H**allucination **O**bject **S**core **T**est）提出了一套全新的评估范式，其核心变革体现在三个维度：

- **评估粒度从图像级下沉到物体级**：不再对整个图像做笼统判断，而是针对图像中每个物体构建“组合三元组”——同时考察物体的**类型存在性**、**属性**和**与其他物体的关系**，形成对单个物体的多维度理解画像。

- **度量标准从准确率转向一致性**：提出 **GHOST 一致性分数（GCS）**，利用加权几何平均对假阳性（FP）和假阴性（FN）进行惩罚，权重随幻觉次数呈指数衰减。GCS 的核心思想是：模型只有在面对同一物体的正负样本变体时保持回答一致，才能获得高分。

- **负样本设计从简单随机到条件共现**：通过从多个 VLM 训练数据集中构建条件共现矩阵，生成“看似合理但实际错误”的困难负样本，并辅以人工筛选，大幅提升评估的挑战性。

### 3. 主要结果速览

GHOST 在 760 张图像上构建了 38,076 个问题，覆盖 20 个主流 MLLM（包括 GPT-4o、Gemini-1.5-Pro 等）。关键发现如下：

- **跨基准对比揭示评估鸿沟**：GPT-4o 在 POPE 上准确率达 87.0，在 AMBER 上得分 91.4，但在 GHOST 上的 GCS 仅为 63.9（Table 8）。这一差距（-23.1）表明，GHOST 能够揭露传统基准无法捕捉的深层幻觉。

- **模型规模与架构的影响**：大型模型（如 GPT-4o，整体 GCS 69.0）显著优于微型 MLLM（平均 GCS < 53），且语言模型容量和视觉编码器质量均对一致性有正向影响（Figure 3、Figure 4）。

- **跨三元组一致性远低于单独评估**：当同时考察物体的类型、属性和关系时，跨组件的累积不一致性导致 GCS(OAR) 显著低于各维度独立评估结果（Table 4），说明模型在组合理解上存在系统性缺陷。

### 4. 方法谱系与知识库定位

GHOST 在现有幻觉评估体系中填补了“物体级组合一致性”的空白。Table 1 系统对比了各基准的覆盖维度：

| 基准 | 对象 | 属性 | 关系 | 评估层级 | 一致性检查 | 人工标注 |
|------|------|------|------|----------|------------|----------|
| POPE | ✓ | ✗ | ✗ | 图像级 | ✗ | ✗ |
| AMBER | ✓ | ✓ | ✗ | 图像级 | ✗ | ✗ |
| GAVIE | ✓ | ✓ | ✓ | 图像级 | ✗ | ✗ |
| THRONE | ✓ | ✗ | ✗ | 物体级 | ✗ | ✓ |
| CIEM | ✓ | ✓ | ✓ | 图像级 | ✗ | ✗ |
| **GHOST** | **✓** | **✓** | **✓** | **物体级** | **✓** | **✓** |

GHOST 是首个同时覆盖物体、属性、关系三个维度，并在物体级别引入多轮一致性检查的基准。其核心贡献不在于提出新的模型架构，而在于**重新定义了“幻觉评估”的测量标准**——从“答对多少”转向“有多自洽”。

### 5. 局限与开放问题

GHOST 的当前局限包括：数据集主要源自 Visual Genome / GQA，场景覆盖有限；困难负样本仍需人工筛选，扩展成本高；仅支持判别式 True/False 问题，未涵盖生成式幻觉。未来方向包括：将一致性框架扩展到视频等多模态场景，探索自动化负样本生成方法，以及将一致性度量应用于需要多步推理的复杂问题。

## 背景与动机

### 幻觉评估的瓶颈：从图像级到物体级

多模态大语言模型（MLLM）在视觉-语言任务中展现出强大的能力，但幻觉问题——即模型生成与视觉内容不一致的陈述——仍是制约其可靠性的核心瓶颈。现有的幻觉评估基准，如 **POPE**（Li et al., EMNLP 2023）、**AMBER**（Wang et al., 2024）、**THRONE**（Kaul et al., 2024）和 **CIEM**（Hu et al., NeurIPS 2023 Workshop），大多采用图像级别的评估范式：它们询问关于整张图像的问题，并以准确率或 F1 分数作为主要度量指标。

然而，这种范式存在一个被长期忽视的结构性缺陷：**图像级别的评估无法捕捉模型对单个物体的具体属性、关系的不一致理解**。一个模型可能准确回答了“图中是否有猫”这类整体性问题，却在关于同一只猫的颜色、位置、与其他物体的关系等细节问题上给出相互矛盾的答案。更关键的是，准确率等独立指标将每个问题视为孤立的判断，完全无法反映模型在回答一组相关问题时是否自相矛盾——这种“隐藏的幻觉”恰恰是实际应用中风险最高的失效模式。

### 准确率的欺骗性：一致性缺失的代价

GHOST 通过实验揭示了准确率指标的系统性欺骗效应。如 **Figure 2** 所示，随着评估中加入更多的负样本（negative samples），模型的标准准确率反而上升——这似乎表明模型表现更好。然而，**无幻觉物体的比例却在同步下降**。这一背离现象的根本原因在于：准确率只统计单次回答的正确与否，而忽略了同一物体在多次相关提问中的回答是否一致。模型可以通过“猜测”或表面模式匹配提高单题正确率，但在一致性检查下暴露出的自相矛盾却被准确率完全掩盖。

这种“高准确率、低一致性”的现象意味着，现有基准可能严重高估了 MLLM 的真实理解能力。一个在 POPE 上达到 87.0 准确率的模型，可能在 GHOST 的一致性度量下仅获得 63.9 分（**Table 8**），揭示了被传统指标隐藏的深层幻觉。

### 现有基准的维度缺口

**Table 1** 系统对比了主流幻觉基准的覆盖维度，暴露出三个关键缺口：

1. **评估粒度过粗**：现有基准多为图像级（Image-level）评估，缺乏对单物体（Object-level）的精细考察。THRONE 虽涉及物体级评估，但未系统覆盖属性（Attribute）和关系（Relation）维度。

2. **一致性检查缺失**：无一现有基准引入多轮一致性检查（Consistency Check）机制。这意味着即使模型对同一物体的存在性、属性、关系给出相互矛盾的判断，也不会被惩罚。

3. **负样本设计简单**：多数基准采用随机或简单规则生成负样本，缺乏针对模型弱点的“困难负样本”（hard negatives）设计，导致评估的区分度和挑战性不足。

### GHOST 的动机与核心思路

针对上述缺口，GHOST 提出了一套根本性的评估范式转变：**从“问对了吗”转向“想清楚了吗”**。其核心动机在于：

- **物体级组合三元组**：将评估粒度下沉到每个物体，通过组合三元组（物体类型、属性、关系）全面考察模型对单物体的多维理解。这确保了评估的细粒度和系统性。

- **多轮一致性检查**：对同一物体的正负样本进行多轮提问，检测模型是否在相关问题上保持一致。这一设计直接针对“隐藏幻觉”问题——即使单题正确，自相矛盾的回答也会被捕获。

- **一致性驱动的度量**：提出 GHOST 一致性分数（GCS），利用加权几何平均对假阳性（FP）和假阴性（FN）进行惩罚，权重随幻觉次数指数衰减。GCS 的核心哲学是：**一次不一致比一次错误更严重，多次不一致则呈指数级恶化**。

- **困难负样本构建**：利用多源数据集的共现矩阵生成看似合理但实际错误的负样本，并通过人工筛选确保挑战性。这避免了简单负样本导致的“天花板效应”，使评估更具区分力。

通过这一框架，GHOST 旨在揭示 MLLM 在物体级理解上的真实能力边界，为幻觉研究提供一个更诚实、更严格的评估基准。

## 核心创新

GHOST 的核心创新在于将幻觉评估从**图像级别下沉到物体级别**，并通过**多轮一致性检查**揭露模型的自相矛盾，而非仅依赖传统的独立准确率指标。其关键设计体现在以下四个维度：

### 1. 评估粒度：从图像级到物体级组合三元组

现有基准如 **POPE** (Li et al., EMNLP 2023)、**AMBER** (Wang et al., 2024) 和 **THRONE** (Kaul et al., 2024) 大多在图像层面提问或仅覆盖单一维度（如物体存在性）。GHOST 将评估单元细化到**每个物体的组合三元组**——物体类型、属性、关系——从而捕捉模型对单个物体的具体属性与关系的理解是否一致（Table 1）。例如，一个“球棒”不仅要被识别为存在，还需在“颜色”和“与其他物体的空间关系”上给出前后一致的回答。

### 2. 度量指标：从准确率到 GHOST 一致性分数 (GCS)

传统基准以准确率或 F1 作为核心指标，但 **Figure 2** 的实验证据表明：随着负样本增加，准确率可能上升，而“无幻觉物体”的比例却在下降——准确率掩盖了幻觉。GHOST 提出 **GCS**，利用加权几何平均对假阳性 (FP) 和假阴性 (FN) 进行惩罚，权重随幻觉次数指数衰减：

$$\mathrm { G C S } = 1 - \left( \sum _ { i = 1 } ^ { N _ { \mathrm { h a l l u } } } \frac { 1 } { 2 ^ { i - 1 } } \right) \bigg / \left( \sum _ { i = 1 } ^ { N _ { \mathrm { t o t a l } } } \frac { 1 } { 2 ^ { i - 1 } } \right)$$

其中 $N_{\mathrm{hallu}} = \mathrm{FP} + \mathrm{FN}$，$N_{\mathrm{total}}$ 为该类别总问题数。GCS 的核心洞察是：**频繁的自相矛盾比单次错误更严重**，因此后续幻觉的惩罚权重呈几何级数递减（即对一致性要求更高）。最终，物体、属性、关系三类的 GCS 取平均得到 Overall GCS（Equation 2）。

### 3. 鲁棒性机制：多轮一致性检查

GHOST 引入多轮一致性检查框架：对同一物体，模型需在正样本和多个困难负样本的 True/False 问题中保持回答一致。**Table 4** 显示，跨三元组的 GCS (OAR) 远低于单独评估的 GCS，揭示了跨组件（物体-属性-关系）的累积不一致性。**Table 7** 的消融实验进一步证实，随着一致性检查轮数增加，所有模型的 GCS 系统性下降，暴露出更多隐藏幻觉。

### 4. 负样本设计：基于条件共现的困难负样本

现有基准多采用随机或简单负样本。GHOST 利用多个 MLLM 训练数据集的共现矩阵，生成**看似合理但实际为假的困难负样本**，并经人工筛选确保挑战性。**Table 5** 的消融实验表明，这种条件共现负样本比随机负样本或 LLaMA 生成的负样本更具挑战性，能更有效地限制模型保持一致性。

## 整体框架

GHOST 提出了一套从数据构建到一致性度量再到模型评估的完整流水线，其核心设计目标是将幻觉评估从图像级别下沉至物体级别，并通过多轮一致性检查暴露模型的自相矛盾。

### 流水线总览

整个框架包含五个关键模块，按执行顺序为：

1.  **组合三元组构建**：从 Visual Genome 和 GQA 的场景图标注中提取每个物体的类型（object type）、属性（attribute）和关系（relation），形成以物体为中心的组合三元组。这一步骤将评估粒度从图像级（image-level）转变为物体级（object-level）。
2.  **困难负样本生成**：利用多个 MLLM 训练数据集（Visual Genome、VQA、GQA、TextVQA、OCR-VQA、LLaVA 指令微调数据）构建条件共现矩阵，从中采样在统计上合理但在当前图像上下文中为假的负样本。例如，对于物体 `bat`，可能生成“bat is white”作为属性负样本，或“bat is on the table”作为关系负样本。
3.  **人工筛选**：对生成的负样本进行人工审核，确保每条负样本陈述确实是当前图像上下文中的假命题，同时保持足够的挑战性。
4.  **一致性检查评估**：对每个物体的每个三元组维度（物体存在性、属性、关系），设计多轮 True/False 判别问题——包含 1 个正样本和 3 个负样本，按随机顺序排列。模型需在多个相关问题上做出一致回答。
5.  **GCS 计算**：基于一致性检查结果，按类别（物体、属性、关系）分别计算 GHOST 一致性分数，再取平均得到整体 GCS。

### 输入输出流

-   **输入**：760 张图像，每张图像经场景图解析后提取若干物体，每个物体生成 4 个问题（1 正 3 负），总计 38,076 个 True/False 判别问题。
-   **中间表示**：每个物体的问题组构成一个“一致性检查单元”，模型对该单元内所有问题的回答被记录为正确/错误序列。
-   **输出**：每个模型在每个类别上的 GCS 分数，以及整体 GCS 分数。GCS 越低，表示模型在物体级别的不一致性（即幻觉）越严重。

### 模块间的因果依赖

困难负样本的质量直接决定一致性检查的区分度——Table 5 的消融实验表明，基于共现矩阵的条件负样本相比随机负样本或 LLaMA 生成的负样本，能更有效地暴露模型的不一致性。一致性检查的轮数则是另一个关键控制旋钮：Table 7 显示，随着检查轮数增加，所有模型的 GCS 系统性下降，证明多轮设计是揭露深层幻觉的必要条件。

### 与传统准确率评估的关键区别

Figure 2 揭示了一个反直觉现象：当负样本数量增加时，模型的标准准确率反而上升，但“无幻觉物体”的比例却持续下降。这意味着准确率可能掩盖幻觉——模型只需学会对所有问题回答“否”即可在负样本主导的评估中获得高准确率，而一致性检查通过追踪同一物体上正负样本回答的自洽性，能够穿透这种表面正确性。GCS 公式正是基于这一洞察设计：它使用加权几何平均（权重随幻觉次数指数衰减）来惩罚假阳性（FP）和假阴性（FN），而非简单地计算正确率。

## 核心模块与公式推导

### 关键模块

GHOST 的评估流水线由五个核心模块串联构成，从数据构建到最终评分形成闭环。

**1. 组合三元组构建**
从 Visual Genome 和 GQA 的场景图标注中提取每个物体的类型（object type）、属性（attribute）及其与其他物体的关系（relation），组合成以物体为中心的组合三元组。每个物体均配有一个正样本陈述和三个负样本陈述，覆盖存在性、属性和关系三个维度，确保评估粒度从图像级下沉到物体级（Table 1）。

**2. 困难负样本生成**
利用 Visual Genome、VQA、GQA、TextVQA、OCR-VQA 及 LLaVA 指令微调数据集构建条件共现矩阵，从与正样本物体共现概率高的候选中采样看似合理但实际为假的负样本。这一策略使负样本更具迷惑性，比随机采样或 LLaMA 生成的负样本更能暴露模型的幻觉倾向（Table 5）。

**3. 人工筛选**
对生成的负样本进行人工复核，确保每条负样本陈述确实为假且具有挑战性。该步骤是保证基准质量的关键，但也构成了扩展至更大规模时的成本瓶颈。

**4. 一致性检查评估**
对每个物体的正负样本进行多轮 True/False 判别，检测模型在回答同一物体的多个相关问题时是否自相矛盾。Figure 2 的实证证据表明：随着负样本轮次增加，标准准确率反而上升，但无幻觉物体的比例持续下降——准确率可能掩盖幻觉，一致性检查成为必要手段。

**5. GCS 计算**
基于一致性检查结果，按物体、属性、关系三个类别分别计算 GCS，再取平均得到综合评分。GCS 通过加权几何平均惩罚假阳性（FP）和假阴性（FN），权重随幻觉次数指数衰减。

### 关键公式

**GHOST 一致性分数（GCS）**

$$\mathrm{GCS} = 1 - \frac{\sum_{i=1}^{N_{\mathrm{hallu}}} \frac{1}{2^{i-1}}}{\sum_{i=1}^{N_{\mathrm{total}}} \frac{1}{2^{i-1}}}$$

其中：
- $N_{\mathrm{hallu}} = \mathrm{FP} + \mathrm{FN}$，即该类别中假阳性和假阴性的总次数，直接对应幻觉事件；
- $N_{\mathrm{total}}$ 为该类别的总问题数；
- 分母 $\sum_{i=1}^{N_{\mathrm{total}}} \frac{1}{2^{i-1}}$ 是一个归一化常数，确保 GCS 取值范围在 $[0, 1]$ 之间；
- 分子中的权重 $\frac{1}{2^{i-1}}$ 随幻觉次数 $i$ 指数衰减，意味着首次幻觉受到的惩罚最重，后续幻觉的边际惩罚递减。这种设计强调一致性而非单次正确率：一个偶尔出错的模型比频繁出错的模型获得更高的 GCS。

**综合 GCS**

$$\mathrm{Overall\ GCS} = \frac{1}{3} \left( \mathrm{GCS}_{\mathrm{obj}} + \mathrm{GCS}_{\mathrm{attr}} + \mathrm{GCS}_{\mathrm{rel}} \right)$$

对物体（obj）、属性（attr）、关系（rel）三个维度的 GCS 取算术平均，得到跨维度的综合一致性评价。Table 4 的跨三元组实验表明，综合 GCS 远低于单独评估时的 GCS，揭示了跨组件累积不一致性的严重程度。

## 实验与分析

### 核心发现：准确率掩盖幻觉，一致性检查揭露隐藏矛盾

传统判别式基准（如 **POPE**（Li et al., EMNLP 2023）和 **AMBER**（Wang et al., 2024））以图像级别的准确率或 F1 作为主要指标，无法捕捉模型对单个物体组合属性的自相矛盾。GHOST 通过**多轮一致性检查**揭示了这一隐藏问题：如 Figure 2 所示，随着负样本数量增加，模型的组件级别标准准确率反而上升，但“无幻觉对象比例”持续下降。这意味着模型在回答更多相关问题时暴露出更多不一致——准确率越高，幻觉可能越严重。这一发现构成了 GHOST 评估框架的核心动机。

### 主结果：20 个 MLLM 在 GHOST 上的表现

Table 2 报告了 20 个多模态大模型在 GHOST 基准上的完整结果，包括精确率（P）、召回率（R）、准确率（Acc）和 GHOST 一致性分数（GCS）。主要结论如下：

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/004_Table_2.jpg]]
*Table 2: GHOST evaluation results for 20 MLLMs. P = Precision, R = Recall, Acc = Accuracy, GCS = GHOST Consistency Score*

- **GPT-4o 取得最优整体 GCS 69.0**，但与其在传统基准上的表现形成鲜明对比。如 Table 8 所示，GPT-4o 在 POPE 上准确率达 87.0，在 AMBER 上得分 91.4，但在 GHOST 上的 GCS 仅为 63.9——**一致性分数比 POPE 准确率低 23.1 个百分点**。这有力证明了 GHOST 能够揭露更深层的幻觉问题。
- **微型 MLLM 的平均 GCS 低于 53**，与 GPT-4o 之间存在超过 16 个点的巨大差距，表明小模型在物体级别的组合理解上存在严重缺陷。
- **LLaVA-OneVision 7B 在物体理解维度上表现突出**，GCS 达到 64.4，超越了部分更大规模的模型，提示架构设计和训练策略可能比纯参数规模更重要。
- 所有模型在**属性（Attribute）和关系（Relation）维度上的 GCS 普遍低于物体存在性（Object）维度**，表明当前 MLLM 对物体间关系和属性状态的理解仍是主要瓶颈。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/012_Table_8.jpg]]
*Table 8: Model results across hallucination benchmarks*

### 跨三元组一致性：累积不一致性的暴露

Table 4 对比了“三元组内”（within triplets）和“跨三元组”（across triplets）的准确率与 GCS。结果显示，**跨三元组的 GCS（OAR）远低于单独评估每个维度时的 GCS**。这意味着当同时考察物体类型、属性和关系的组合正确性时，模型的不一致性会累积放大——即使模型在每个单独维度上表现尚可，组合起来仍可能产生严重矛盾。

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/006_Table_4.jpg]]
*Table 4: Accuracy vs GCS within and across triplets*

### 消融实验：困难负样本与一致性检查轮数

**困难负样本生成策略**（Table 5）：GHOST 采用基于条件共现矩阵的方法生成困难负样本，并与随机负样本和基于 LLaMA 生成的负样本进行对比。结果表明，共现矩阵生成的负样本具有**显著更大的挑战性**，能更有效地暴露模型的不一致性。该方法通过从 Visual Genome、VQA、GQA 等多个 MLLM 训练数据集中提取共现统计，生成“看似合理但实际错误”的负样本，并经人工筛选确保质量。

**一致性检查轮数的影响**（Table 7）：随着一致性检查轮数增加，所有模型的 GCS 系统性下降。这表明更多的相关追问能够持续揭露模型的隐藏矛盾，验证了多轮一致性框架的有效性。同时，Table 7 还对检查顺序进行了排列组合消融，结果显示顺序变化对 GCS 影响较小，说明评估框架对问题顺序具有较好的鲁棒性。

**提示敏感性**（Table 6）：对近期模型而言，不同提示模板对 GCS 的影响较低，表明评估框架本身具有较好的稳定性，不会因提示措辞的微小变化而产生显著偏差。

### 模型规模与视觉编码器的影响

Figure 3 展示了语言模型规模对幻觉的影响：**更大的语言模型在所有维度上均取得更高的 GCS**，尤其在关系任务上提升更为明显，表明复杂视觉-语言理解能力随模型容量增加而持续改善。Figure 4 则揭示了视觉编码器质量的关键作用：采用 **SigLIP 和 MoE Vision 等强视觉编码器的模型在 GCS 上表现一致更优**，凸显了编码器质量对减少幻觉的重要性。

### 失败模式与局限性

尽管 GHOST 在揭露幻觉方面表现出色，但存在以下局限：

1. **属性与关系理解仍是主要短板**：所有模型在属性和关系维度的 GCS 显著低于物体存在性维度，表明当前 MLLM 对“物体是什么颜色/状态”和“物体之间如何交互”的理解远不如“物体是否存在”可靠。
2. **数据集覆盖范围有限**：GHOST 的数据主要来源于 Visual Genome 和 GQA，可能未覆盖更广泛的视觉场景和概念，泛化性需进一步验证。
3. **人工筛选成本高**：困难负样本的生成仍需人工审核以确保质量，扩展到更大规模基准时成本较高。
4. **评估形式受限**：当前仅评估判别式 True/False 问题，未涉及生成式幻觉或开放式回答的评估，无法完全反映模型在实际对话中的幻觉行为。

### 开放问题

- 如何将 GHOST 的对象级一致性框架扩展到视频、音频等其他模态？
- 能否利用对抗生成等自动化方法替代人工筛选，构建更具挑战性的负样本？
- 如何进一步改进属性和关系理解，以缩小与物体识别之间的性能差距？
- 在同等计算预算下，语言模型容量与视觉编码器质量的最优权衡是什么？

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/001_Figure_1.jpg]]
*Figure 1: Top: Illustration of GHOST benchmark’s object-centric evaluation, where each object (e.g., "bat") is assessed using compositional triplets consisting of the object’s type, attributes, and relations. During consistency check rounds, plausible negative variations are introduced to evaluate whether the model truly understands the object or is hallucinating. Bottom: The GHOST Consistency Score (GCS) framework evaluates the model’s consistency across positive and negative statements by penalizing hallucinated responses. Unlike traditional accuracy metrics that treat each question independently, GCS is a function of the consistency checks and accounts for the frequency of hallucinations. By focus...*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/002_Table_1.jpg]]
*Table 1: Hallucination benchmarks contents. O=Object, A=Attribute, R=Relation, IL=Image-level, OL=Object-level, CC=Consistency Check, ML=Manual labeling*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/007_Table_5.jpg]]
*Table 5: Ablation study on hard negatives generation*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/009_Table_3.jpg]]
*Table 3: GHOST Comparison against previous benchmarks*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/010_Table_6.jpg]]
*Table 6: Prompt sensitivity ablation for different models with corresponding response types. Italics represent our GHOST prompt*

![[assets/figures/papers/paper_list_l2_https_openaccess_thecvf_com_content_WACV2026_papers_VS_GHOST_Getting_to/figures/011_Table_7.jpg]]
*Table 7: Ablation study for all order permutation of CC rounds*

## 方法谱系与知识库定位

### 1. 与现有幻觉基准的对比定位

GHOST 在评估粒度、度量指标和鲁棒性设计三个维度上对现有基准形成了系统性改进。Table 1 直接对比了各基准在物体（O）、属性（A）、关系（R）覆盖度、评估层级（图像级 IL vs. 物体级 OL）、一致性检查（CC）和人工标注（ML）方面的差异。现有主流基准的定位如下：

- **POPE**（Li et al., EMNLP 2023）和 **AMBER**（Wang et al., 2024）属于判别式基准，评估粒度停留在图像级别，采用准确率/F1 等独立指标，缺乏对模型自相矛盾的检测能力。
- **GAVIE**（Liu et al., 2024）引入了生成式评估和 LLM 裁判，但仍未进行对象级细粒度的一致性检查。
- **THRONE**（Kaul et al., 2024）虽聚焦于对象级幻觉，但未系统性地覆盖属性与关系维度，也未引入多轮一致性验证。
- **CIEM**（Hu et al., NeurIPS 2023 Workshop）作为判别式基准，同样缺少一致性检查机制。

GHOST 的核心差异化在于三个维度的同步升级：**评估粒度**从图像级下沉到对象级，为每个物体构建组合三元组（类型、属性、关系）；**度量指标**从准确率切换为 GHOST 一致性分数（GCS），通过加权几何平均惩罚假阳性和假阴性；**鲁棒性设计**引入基于条件共现矩阵的困难负样本和多轮一致性检查，使评估能够揭露隐藏的不一致性。

Table 8 的跨基准对比直接验证了这一差异：GPT-4o 在 POPE 上准确率达 87.0，在 AMBER 上得分为 91.4，但在 GHOST 上 GCS 仅为 63.9，差距超过 23 个百分点。这证明传统准确率指标可能严重高估模型的真实理解能力，而 GHOST 通过一致性检查揭露了更深层的幻觉。

### 2. 适用边界

GHOST 的设计决定了其适用范围存在明确的边界条件：

**适用场景**：
- 评估多模态大模型对静态图像中单个物体的细粒度理解，包括物体存在性、属性识别和空间/语义关系判断。
- 检测模型在回答一组相关问题时是否保持内部一致性，适用于需要可靠视觉推理的下游任务筛选。
- 作为模型开发过程中的诊断工具，通过分解物体、属性、关系三个维度的 GCS 分数定位能力短板。

**不适用或需谨慎推广的场景**：
- 当前仅覆盖判别式 True/False 问题，无法评估生成式幻觉（如模型在开放式描述中凭空捏造物体或关系）。若需评估生成式能力，需与 GAVIE 等生成式基准配合使用。
- 数据集构建依赖 Visual Genome 和 GQA 的场景图标注，主要覆盖自然场景中的常见物体和关系，对专业领域图像（如医学影像、遥感图像）的泛化能力未经验证。
- 一致性检查的轮数固定为三轮，对于需要更长逻辑链或多步推理的复杂矛盾类型，当前框架可能无法充分暴露。

### 3. 已知局限

1. **数据覆盖范围受限**：基准基于 Visual Genome / GQA 构建，场景和概念分布受限于这两个数据集的标注体系，可能无法覆盖长尾物体、抽象概念或文化特定实体。扩展到更广泛的视觉领域需要额外的场景图标注工作。

2. **负样本构建依赖人工**：尽管条件共现矩阵（Table 5）显著提升了负样本的挑战性，但最终仍需人工筛选以确保负样本既“困难”又“确实为假”。当基准规模需要大幅扩展时，人工筛选成为可扩展性的主要瓶颈。

3. **评估范式单一**：当前仅支持判别式 True/False 问题的评估，无法捕捉模型在自由文本生成中的幻觉模式。生成式幻觉（如虚构物体细节、编造关系）需要不同的评估框架。

4. **一致性检查深度有限**：三轮固定检查虽然足以揭露基础的不一致性（Table 7 显示性能随轮数增加而下降），但对于需要多步推理或因果链验证的复杂场景，可能需要更长的检查序列和更复杂的矛盾注入策略。

5. **闭源模型的不透明性**：虽然评估涵盖了 GPT-4o、Gemini-1.5-Pro 等闭源模型，但其具体架构、训练数据和优化策略不可知，限制了对性能差异根因的深入分析。

### 4. 开放问题

1. **跨模态扩展**：GHOST 的对象级一致性框架能否推广到视频、音频等其他模态？视频中的物体跟踪一致性、音频中的声源属性一致性等场景可能受益于类似的多轮检查机制，但需要解决时序对齐和模态特定的负样本生成问题。

2. **自动化负样本生成**：能否利用对抗生成方法或大模型自身来替代人工筛选，自动构建更具挑战性且语义合理的负样本？Table 5 显示 LLaMA 生成的负样本效果不及条件共现矩阵方法，但更先进的生成策略（如基于扩散模型的视觉反事实生成）可能突破这一限制。

3. **属性与关系理解的提升路径**：Table 2 和 Figure 3 一致显示，属性和关系维度的 GCS 显著低于物体识别，且这一差距在不同规模的模型中持续存在。如何针对性地改进属性和关系的视觉-语言对齐，以缩小与物体识别之间的性能鸿沟，是需要进一步研究的关键问题。

4. **一致性度量的深化**：当前的 GCS 公式基于假阳性/假阴性的加权几何平均，惩罚权重按 $1/2^{i-1}$ 指数衰减。这一设计是否适用于需要多步推理或因果一致性检查的问题？是否存在更优的权重衰减策略或更复杂的一致性度量形式？

5. **LLM 容量与视觉编码器的最优权衡**：Figure 3 和 Figure 4 分别展示了语言模型规模和视觉编码器质量对 GCS 的影响。在同等的计算预算下，如何最优地分配 LLM 参数和视觉编码器容量，以达到最佳的幻觉抑制效果？这一权衡关系对实际模型设计具有直接指导意义。

6. **一致性检查的深度与广度权衡**：Table 7 表明增加检查轮数会持续降低 GCS，但边际效应和计算成本的平衡点尚未系统探索。是否存在一个最优的检查深度，能够在评估精度和计算开销之间取得最佳折中？

## 原文 PDF

![[paperPDFs/WACV_2026/GHOST_Getting_to_the_Bottom_of_Hallucinations_with_A_Multi_round_Consistency_Benchmark.pdf]]
