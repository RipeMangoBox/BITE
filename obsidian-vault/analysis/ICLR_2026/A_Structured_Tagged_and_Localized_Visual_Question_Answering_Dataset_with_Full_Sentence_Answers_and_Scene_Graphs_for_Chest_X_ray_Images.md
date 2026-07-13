---
title: "A Structured, Tagged, and Localized Visual Question Answering Dataset with Full Sentence Answers and Scene Graphs for Chest X-ray Images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Structured_Tagged_and_Localized_Visual_Question_Answering_Dataset_with_Full_Sentence_Answers_and_Scene_Graphs_for_Chest_X_ray_Images.pdf
project_link: null
code_link: https://github.com/philip-mueller/mimic-ext-cxr-qba/
aliases:
- MECQCQ
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/health
core_operator: "提出一个自动化的数据集构建流水线，从放射学报告中利用LLM提取信息构建场景图，再基于模板和场景图生成问答对，并自动评估质量。"
primary_logic: "通过LLM信息提取和语义实体映射构建细粒度场景图（257个区域、221个发现），结合模板和报告原文生成多部分、多粒度的详细答案，并附带边界框和结构化标签，从而创建大规模、高质量的VQA数据集。"
claims:
- "CXR-QBA数据集包含42M问答对，是迄今为止最大的胸部X光VQA数据集，并提供边界框和标签。"
- "场景图在发现标签和边界框评估上优于或持平Chest ImaGenome，尤其在长尾类别上提升20%。"
- "自动质量评估识别出7.5M微调级和31.2M预训练级问答对，LLM评判的过评级率不超过2%。"
- "基于CXR-QBA训练的VLM在逻辑和定位指标上取得高分，PT→FT两阶段训练策略最佳。"
---

# A Structured, Tagged, and Localized Visual Question Answering Dataset with Full Sentence Answers and Scene Graphs for Chest X-ray Images

> [!tip] 核心洞察
> 通过LLM信息提取和语义实体映射构建细粒度场景图（257个区域、221个发现），结合模板和报告原文生成多部分、多粒度的详细答案，并附带边界框和结构化标签，从而创建大规模、高质量的VQA数据集。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向胸部X光图像的具有完整句子答案和场景图的结构化、带标签与定位的视觉问答数据集 |
| 英文题名 | A Structured, Tagged, and Localized Visual Question Answering Dataset with Full Sentence Answers and Scene Graphs for Chest X-ray Images |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LrmyW9JLYq) · [GitHub](https://github.com/philip-mueller/mimic-ext-cxr-qba/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/health |
| Method | MIMIC-Ext-CXR-QBA (CXR-QBA) 数据集构建流水线 |
| Dataset | MIMIC-CXR-JPG Test (CheXpert 13类), CXR-LT 2024 Gold (13 CXP + 12 LT类), MS-CXR (6类), REFLACX (18类) |

> [!tip] 效果简介
> - MIMIC-CXR-JPG Test (CheXpert 13类) 上，MCC (Micro) 为 0.71 [0.69,0.73]，对比 0.67 [0.65,0.68] (Chest ImaGenome)，变化 +0.04。
> - CXR-LT 2024 Gold (13 CXP + 12 LT类) 上，MCC (Micro) 为 0.67 [0.65,0.69]，对比 0.64 [0.62,0.66] (Chest ImaGenome)，变化 +0.03。
> - MS-CXR (6类) 上，IoU@30 (Micro) 为 0.51 [0.47,0.54]，对比 0.45 [0.42,0.49] (Chest ImaGenome)，变化 +0.06。

## 概要

本文针对现有胸部X光（CXR）视觉问答（VQA）数据集规模小、答案简短、缺乏定位信息（边界框）和结构化元数据（如区域、发现标签）的核心瓶颈，提出了一个大规模、高质量的结构化VQA数据集——**MIMIC-Ext-CXR-QBA（简称CXR-QBA）**。

该数据集的核心创新在于设计了一条自动化的构建流水线（pipeline）：首先，利用大语言模型（LLM）从放射学报告中提取信息，结合图像定位模型构建包含257个定位区域和221个发现类别的细粒度场景图，其标签和边界框质量在MIMIC-CXR子集上与专家标注对比，性能优于或持平现有基线Chest ImaGenome，尤其在长尾类别上提升显著（MCC提升0.03-0.04，IoU@30提升0.03-0.06）；然后，基于场景图和模板生成四种类型（指示、研究异常、区域异常、发现）的多部分、多粒度详细答案，每个答案均附带完整句子、边界框和结构化标签；最后，使用Llama 3.1 8B作为评判进行自动质量评估，从蕴含性、相关性、完整性、问题清晰度、答案清晰度五个维度评分，LLM评判的过评级率不超过2%。

主要结果包括：
- **数据集规模**：CXR-QBA包含42.2M问答对，是迄今为止最大的CXR VQA数据集，其中7.5M达到微调（FT）等级，31.2M达到预训练（PT）等级。
- **场景图质量**：在发现标签评估上，MCC微平均达0.71（MIMIC-CXR-JPG测试集），优于Chest ImaGenome的0.67；在边界框评估上，IoP@30在MS-CXR和REFLACX上分别达0.56和0.54，均高于基线。
- **VLM训练效果**：基于CXR-QBA训练的视觉语言模型（VLM）在结构化VQA任务中取得高分，逻辑精确率达0.78，定位精确率达0.89，显著优于MAIRA-2（0.64和0.32）等基线。采用“先预训练后微调”（PT→FT）的两阶段训练策略效果最佳。

该工作定位为通过数据驱动的自动化方法，为CXR VQA领域提供大规模、结构化、可解释的训练资源，并验证了其在训练高性能、可定位的医学VLM中的有效性。



胸部X光（CXR）是临床中最常用的影像学检查之一，其报告解读需要专业放射科医生完成，耗时且存在主观差异。视觉问答（VQA）技术旨在通过自然语言交互辅助影像理解，但现有医学VQA数据集在CXR领域面临三个关键瓶颈：**规模不足**、**答案粒度粗**、**缺乏结构化定位信息**。

**现有数据集的缺口。** 从规模看，此前最大的CXR VQA数据集CheXinstruct仅包含8.5M问答对，且多数数据集（如VQA-RAD、PathVQA）样本量在万级以下。从答案形式看，现有数据集普遍采用简短答案（brief answers），无法提供放射学报告中常见的多句、多粒度描述。更关键的是，**缺乏定位信息**（边界框）和**结构化元数据**（如区域标签、发现类别、确定性标注）——这使得模型难以学习“在何处发现何种异常”的因果关联，也限制了输出的可解释性。例如，Chest ImaGenome虽然提供了场景图，但仅覆盖29个解剖区域和53种发现，对长尾发现的表达能力有限。

**本文的动机与核心思路。** 本文提出一个自动化的数据集构建流水线，旨在同时解决上述三个问题。其因果逻辑是：通过从放射学报告中利用LLM提取结构化信息，构建细粒度的场景图（257个定位区域、221个发现类别），再基于模板和场景图生成问答对，从而在规模化产出的同时保证答案的详细性、定位精度和结构化标签。这一设计的关键在于：**场景图作为中间表示**，将非结构化的报告文本转化为可编程的实体-关系图，使得问答生成可以按需组合不同粒度的信息（如“左肺上叶存在实变” vs “研究层面存在异常”）。此外，流水线内置了LLM自动质量评估（Llama 3.1 8B），从蕴含性、相关性、完整性等五个维度筛选出7.5M微调级和31.2M预训练级问答对，**过评级率不超过2%**（见表5），为下游训练提供了质量保证。

**与现有工作的关键差异。** 相比Chest ImaGenome（29区域/53发现），本文的场景图在区域和发现类别上分别扩大了约9倍和4倍，在长尾类别上MCC提升约20%（见表2a，CXR-LT 2024金标准数据集上微平均MCC：0.67 vs 0.64）。相比MAIRA-2等结构化VQA基线，基于该数据集训练的VLM在逻辑精确率（0.78 vs 0.64）和定位精确率（0.89 vs 0.32）上均有显著提升（见表4）。这些结果验证了：**大规模、细粒度、带定位的结构化数据能够直接转化为模型在逻辑推理和视觉定位上的性能增益**。

**需注意的局限性。** 数据集仅基于MIMIC-CXR单一来源，可能无法代表其他人群或成像设备；自动构建的标签和边界框在极长尾发现上仍可能存在偏差；模板化问题导致问题文本多样性有限（平均重复238次，见表3）。这些因素在后续分析中需保持谨慎。



## 核心方法与创新机理

现有胸部X光VQA数据集普遍面临规模小、答案简短、缺乏定位信息（边界框）和结构化元数据（如区域、发现标签）的瓶颈，这限制了模型的可训练性和可解释性。本工作的核心创新在于提出一个自动化的数据集构建流水线，通过因果链条：**从放射学报告中利用LLM提取信息构建细粒度场景图 → 基于场景图和模板生成多部分、多粒度的问答对 → 自动质量评估**，从而一次性改变多个关键设计槽位（changed slots），创建了迄今为止最大规模的胸部X光VQA数据集。

具体而言，与现有最大基线数据集（CheXinstruct, 8.5M问答对）相比，本工作将**数据集规模**提升至42.2M（微调级7.5M）。更重要的是，**答案格式**从简单的简短答案（brief）转变为包含完整句子、边界框和结构化标签的多部分详细答案。同时，**定位信息**从“无边界框”变为“提供正负答案的边界框”，**结构化标签**从“无标签或仅有简单标签”变为“提供区域、发现、确定性等结构化标签”。在场景图层面，**区域/发现数量**从Chest ImaGenome的29个区域、53个发现，大幅扩展至257个定位区域和221个发现类别。

该流水线由三个核心模块构成：**场景图构建**模块利用LLM从放射学报告中提取信息，结合定位模型构建包含句子节点、观察节点、区域节点和指示节点的场景图；**问答对生成**模块基于场景图和模板，为四种问题类型（指示、研究异常、区域异常、发现）生成多部分答案；**自动质量评估**模块使用Llama 3.1 8B作为评判，从蕴含性、相关性、完整性、问题清晰度、答案清晰度五个维度评分，最终划分出7.5M微调级和31.2M预训练级问答对。LLM评判的过评级率不超过2%（Table 5），且LLM倾向于比人类更严格。

消融实验进一步验证了创新设计的有效性：先预训练后微调（PT→FT）的两阶段训练策略优于仅使用2M预训练样本；去除边界框和标签训练会降低定位和标签相关指标（Table 16）。这些证据共同支撑了该工作在数据集规模、答案丰富度、结构化信息和自动化构建方法上的核心创新。



![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/053_Figure_13.jpg]]
*Figure 13: Scene graph structure overview*

CXR-QBA 数据集的构建遵循一条三阶段自动化流水线，其核心瓶颈在于如何从非结构化的放射学报告中提取细粒度的结构化信息，并以此生成高质量、可定位的问答对。该流水线依次包含 **场景图构建**、**问答对生成** 和 **自动质量评估** 三个模块，如图 Figure 2 所示。

**场景图构建** 是流水线的基石，其因果机制在于：通过 LLM 从放射学报告的 FINDINGS 和 IMPRESSION 部分提取句子、观察（发现）、区域和指示（indication）等实体，并将其组织为包含四种节点（句子节点、观察节点、区域节点、指示节点）的有向图（Figure 13）。每个观察节点与一个或多个区域节点关联，并携带发现类别、确定性等标签。同时，该模块利用定位模型（如 DETR）为每个区域生成边界框。这一模块的输出是结构化的场景图，它解决了现有数据集缺乏结构化元数据和边界框的根本问题，为后续生成多粒度的、带定位信息的答案提供了结构化基础。

**问答对生成** 模块以场景图和预定义模板为输入，针对四种问题类型（Indication, Study abnormality, Region abnormality, Finding）采用不同的生成策略。其关键设计在于，答案被分解为三个部分：**主答案（main-answer）**、**细节（details）** 和 **相关信息（related-information）**。每个部分都包含一个完整的句子、一组结构化标签（如区域、发现、确定性）和对应的边界框（Figure 3）。这种多部分结构使得答案既能提供简洁的结论（主答案），又能提供详细的证据（细节和相关信息），从而支持不同粒度的推理需求。该模块的输出是原始的问答对，但质量参差不齐。

**自动质量评估** 模块使用 Llama 3.1 8B 作为评判，从五个维度（蕴含性、相关性、完整性、问题清晰度、答案清晰度）对每个问答对进行评分，并据此将问答对划分为 **预训练（PT）** 和 **微调（FT）** 两个等级。该模块的因果机制在于：通过自动化的 LLM 评判，以较低成本识别出高质量样本，从而为下游模型训练提供分级数据。实验表明，LLM 评判的过评级率不超过 2%（Table 5），与人类评判的 Cohen's kappa 在 0.32 到 0.65 之间，证明了该方法的可靠性。

最终，该流水线从 MIMIC-CXR 数据集中生成了包含 **42.2M 问答对** 的 CXR-QBA 数据集，其中 **7.5M 为微调等级**，**31.2M 为预训练等级**（Figure 4a）。整个流水线的输入是原始胸部 X 光图像和对应的放射学报告，输出是带有完整句子答案、边界框和结构化标签的大规模、高质量 VQA 数据集。



### 数据集构建流水线

本工作的核心贡献是提出一个自动化的数据集构建流水线（Figure 2），该流水线由三个串行模块组成：场景图构建、问答对生成和自动质量评估。

#### 1. 场景图构建

**瓶颈与机制**：现有胸部X光VQA数据集缺乏结构化元数据和定位信息，限制了模型的可解释性。本文通过LLM从放射学报告中提取信息，并与图像中定位的区域结合，构建细粒度的场景图。场景图包含四种节点类型：句子节点（直接关联报告原始句子）、观察节点（对应FINDINGS或IMPRESSION部分中每个独立描述的观察）、区域节点（对应每个解剖结构）和指示节点（对应报告的INDICATION部分）。该场景图定义了257个定位区域和221个发现类别，显著多于Chest ImaGenome的29个区域和53个发现。

**证据强度**：场景图在发现标签评估上（Table 2a）在MIMIC-CXR-JPG测试集上达到Micro MCC 0.71 [0.69, 0.73]，优于Chest ImaGenome的0.67 [0.65, 0.68]；在边界框评估上（Table 2b）在MS-CXR上达到Micro IoU@30 0.51 [0.47, 0.54]，优于Chest ImaGenome的0.45 [0.42, 0.49]。这些结果置信度均为1.0，表明自动构建的场景图质量与专家标注相当或更优。

#### 2. 问答对生成

**机制**：基于场景图和模板，为四种问题类型（指示、研究异常、区域异常、发现）生成问答对。答案被组织为多部分结构（Figure 3），包含三种类型：(i) main-answers（主要答案）、(ii) details（细节）和(iii) related-information（相关信息）。每个答案部分都附带完整句子、边界框（正负答案均有）和结构化标签（如区域、发现、确定性等）。这种设计使答案既包含自由文本放射学报告风格的详细描述，又提供机器可解析的结构化信息。

**证据强度**：Table 1显示，本数据集包含42.2M问答对（其中微调级7.5M），是迄今为止最大的胸部X光VQA数据集，且唯一同时提供边界框和结构化标签的数据集。答案文本的平均重复次数仅为5次（Table 3），表明虽然问题基于模板，但答案内容高度多样化。

#### 3. 自动质量评估

**机制**：使用Llama 3.1 8B作为评判，从五个维度评分：蕴含性（entailment，答案是否与原始报告事实一致）、相关性（relevance，答案是否与问题相关）、完整性（completeness，答案是否完整）、问题清晰度（question clarity）和答案清晰度（answer clarity）。评分结果将问答对划分为三个等级：微调级（fine-tuning grade，评级A或更高）、预训练级（pre-training grade，评级B或更高）和排除级。

**证据强度**：Figure 4a显示，18.6%的问答对被评为微调级，58.8%为预训练级，22.6%被排除。Table 5的人机对比研究表明，LLM评判的过评级率（overrated grade）最高不超过2%，Cohen's kappa系数在0.32到0.65之间，表明LLM评判与人类评判具有中等到较高的一致性。需要注意的是，LLM评判可能对某些类型的错误不敏感，但过评级率低这一事实增强了其可靠性。

### 结构化VQA任务与评估指标

**RadStrucVQA指标**：本文定义了一个新的评估指标RadStrucVQA，用于评估模型在结构化VQA任务上的表现。该指标基于蕴含检查，包含逻辑（logical）、定位（grounding）和空间（spatial）三个子指标，遵循与RadFact（Bannur et al., 2024）相同的原则。

**核心公式**：

- 子指标sub的样本级精确率（Precision）：
  $$p_{sub}(\hat{y}, y) = s_{sub}(\hat{y}, y)$$
  其中 $\hat{y}$ 是预测答案，$y$ 是真实答案。

- 子指标sub的样本级召回率（Recall）：
  $$r_{sub}(\hat{y}, y) = s_{sub}(y, \hat{y})$$

- 评分函数 $s_{sub}$：
  $$s_{sub}(H, C) = \frac{|\{h \in H \mid \text{entailed}_{sub}(h, C[h]) \land \text{relevant}_{sub}(h)\}|}{|\{h \in H \mid \text{relevant}_{sub}(h)\}|}$$
  其中 $H$ 是假设元素集合，$C$ 是上下文元素集合。该函数计算相关假设元素中被蕴含的比例。

- 证据集 $C[h]$：
  $$C[h] = \{c \in C \mid h \text{ is logically entailed with } C \text{ and } c \text{ provides evidence for } h\}$$
  从上下文 $C$ 中为假设 $h$ 提供证据的元素集合。

- 蕴含检查函数 $\text{entailed}_{sub}(h, C[h]) \in \{\text{true}, \text{false}\}$：子指标特定的蕴含检查函数。

**变量含义**：
- $p_{sub}$：子指标sub的精确率，衡量预测答案中正确部分的比例。
- $r_{sub}$：子指标sub的召回率，衡量真实答案中被正确预测部分的比例。
- $s_{sub}$：评分函数，计算假设集合中被蕴含的相关元素比例。
- $H$：假设元素集合（如预测答案中的句子、标签等）。
- $C$：上下文元素集合（如真实答案中的句子、标签等）。
- $C[h]$：为假设元素 $h$ 提供证据的上下文元素子集。
- $\text{entailed}_{sub}$：子指标特定的蕴含检查，判断假设是否被上下文证据蕴含。
- $\text{relevant}_{sub}$：子指标特定的相关性检查，判断假设元素是否相关。

**实验验证**：Table 4显示，基于CXR-QBA训练的VLM在逻辑精确率（Logical Precision）上达到0.78 [0.77, 0.78]，远超过MAIRA-2的0.64 [0.63, 0.65]；在定位精确率（Grounding Precision）上达到0.89 [0.88, 0.89]，显著优于MAIRA-2的0.32 [0.31, 0.33]。消融实验（Table 16）表明，先预训练后微调（PT→FT）策略优于仅使用2M预训练样本，而去除边界框和标签训练会降低定位和标签相关指标。这些结果置信度为0.95。



## 实验与关键发现

### 主结果：场景图与VQA数据集质量

**场景图评估（Table 2）** 表明自动构建的场景图在发现标签和边界框上均达到或超越现有标准。在MIMIC-CXR-JPG测试集上（CheXpert 13类），本方法发现标签的Micro MCC为0.71 [0.69,0.73]，比Chest ImaGenome的0.67 [0.65,0.68]高出0.04。在CXR-LT 2024金标准（13 CXP + 12长尾类）上，本方法Micro MCC为0.67 [0.65,0.69]，同样优于基线的0.64 [0.62,0.66]，尤其在长尾类别上提升约20%。边界框评估方面，在MS-CXR（6类）上本方法IoU@30为0.51 [0.47,0.54]，高于基线的0.45 [0.42,0.49]；在REFLACX（18类）上为0.45 [0.44,0.47]，高于基线的0.42 [0.4,0.43]。这一提升主要源于更大的区域和发现集合（257个区域、221个发现 vs. 29区域、53发现），使更多细粒度解剖结构和病理能被定位和标注。

![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/008_Table_2.jpg]]
*Table 2: (a) Evaluation of finding tags against 13 CheXpert (CXP) classes from the MIMIC-CXR-JPG test set and 25 classes, 13 CXP and 12 long-tail (LT) classes, from the CXR-LT 2024 gold standard dataset (Sec. C.2). We report the Matthews Correlation Coefficient (MCC) macro-averaged over different finding subsets (CXP-5, CXP-7, CXP-13, LT) and micro-averaged. Compared to Chest ImaGenome, we produce slightly more accurate tags, performing especially well on long-tail classes, highlighting the importance of our fine-grained tags*

**数据集规模与特性（Table 1）**：CXR-QBA包含42.2M问答对，是迄今为止最大的胸部X光VQA数据集。自动质量评估（Figure 4）识别出7.5M微调级（FT grade）和31.2M预训练级（PT grade）问答对。LLM评判（Llama 3.1 8B）与人类评判的对比（Table 5）显示，过评级率不超过2%（各维度为0%-2%），Cohen's kappa在0.32到0.65之间，表明LLM评判可靠且倾向于比人类更严格。答案多样性（Table 3）方面，尽管问题文本因模板化存在高重复（平均238次重复），但答案文本高度多样（平均5次重复），且发现和区域标签集合展现了丰富的医学变异性。答案长度分布（Figure 6）显示阳性发现答案平均18词，阴性约10词，体现了报告级别的细节程度。

![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/005_Table_1.jpg]]
*Table 1: Medical VQA dataset comparison. Our dataset is the largest to date and provides localized and tagged answers*

![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/009_Table_3.jpg]]
*Table 3: (b) Evaluation of finding bounding boxes against 6 finding classes from MS-CXR and 18 classes from REFLACX (Sec. C.3). We report the pixel-level Intersection-over-Union (IoU), Intersection-over-Prediction (IoP), and Intersection-over-Target (IoT), each thresholded at 30%, and micro-averaged. Compared to Chest ImaGenome, our bounding boxes are better matching the hand-labeled boxes, especially leading to smaller and more precise boxes (larger IoP), which we assume is due to our more fine-grained region annotations*

**结构化VQA任务（Table 4）**：基于CXR-QBA训练的多模态模型在逻辑和定位指标上均取得高分。最佳策略是先在1M预训练级样本上训练，再在1M微调级样本上微调（PT→FT），逻辑精确率达到0.78 [0.77,0.78]，定位精确率达到0.89 [0.88,0.89]。相比之下，基线模型MAIRA-2的逻辑精确率仅0.64 [0.63,0.65]，定位精确率仅0.32 [0.31,0.33]。Qwen3-VL和LLaVA-Med v1.5的表现更差，表明本数据集能有效训练模型生成正确、视觉定位且带标签的答案。

![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/016_Table_4.jpg]]

![[assets/figures/papers/iclr26_0004_LrmyW9JLYq_A_Structured_Tagged_and_Localized_Visual_Questio/figures/018_Table_4.jpg]]
*Table 4: Results on our structured VQA task, evaluated on our fine-tuning grade test set (95% confidence intervals). Our model was trained on 1M or 2M pre-training (PT) grade samples, on 1M fine-tuning (FT) grade samples, or on 1M pre-training (PT) followed by 1M fine-tuning (FT) samples from our dataset. We compare it with MAIRA-2, Qwen3-VL (4b, Instruct), and LLaVA-Med v1.5. Our dataset enables training VLMs to predict correct, visually grounded, and tagged answers*

### 消融实验

**训练策略消融（Table 4）**：PT→FT两阶段训练策略优于仅使用2M预训练样本（不进行微调）的设置，后者在逻辑精确率上低约0.04，定位精确率低约0.02。仅使用1M微调样本训练的效果也弱于两阶段策略，表明预训练阶段提供的广泛知识对微调阶段有正向迁移作用。

**结构化信息消融（Table 16）**：去除边界框和标签训练会显著降低定位和标签相关指标。例如，不训练边界框时定位精确率下降约0.15，不训练标签时标签精确率下降约0.10。这表明结构化标签和定位信息不仅是数据集的输出特性，也是训练过程中的有效监督信号。

**LLM评判一致性（Table 5, Figure 12）**：Llama 3.1 8B与70B作为评判的评级混淆矩阵显示，低质量样本几乎从未被8B误评为微调级，表明8B在关键决策边界上可靠。不同维度中，相关性（Relevance）的Cohen's kappa最高（0.65），而问题清晰度和答案清晰度最低（0.32），提示LLM在主观性更强的维度上与人类一致性较弱。

### 失败模式与局限性

1. **阳性发现预测不足（finding-pos）**：Table 4的详细子指标（Table 16）显示，模型在阳性发现上的召回率低于阴性发现，表明存在预测偏斜。这可能是由于数据集中阳性样本比例较低（Figure 5），需要通过数据过滤或重采样来解决。

2. **长尾发现性能瓶颈**：尽管在长尾类别上有20%提升（Table 2a），但绝对性能仍较低（如CXR-LT上某些长尾类的F1低于0.5），说明自动构建的标签在罕见发现上可能不完整或有噪声。

3. **模板化问题多样性有限**：问题文本的高重复率（238次）可能限制模型对多样化问题表述的泛化能力，尽管答案多样性弥补了部分不足。

4. **非正面图像排除**：因定位模型限制，仅使用正面（PA/AP）X光图像，排除了侧位和其他视图，减少了数据覆盖范围。

5. **LLM评判的潜在盲区**：尽管过评级率低，LLM评判可能对某些类型的错误（如细微的解剖定位错误）不敏感，这需要人工抽查来验证。

### 开放问题

- 如何通过数据过滤或类别平衡策略解决阳性发现预测不足的问题？
- 数据集构建框架能否迁移到其他影像模态（如CT、MRI）？
- RadStrucVQA指标与其他胸部X光VQA指标（如RadFact）的相关性如何？
- 使用不同LLM（如GPT-4、Claude）进行蕴含预测对最终指标分数的影响是什么？



## 定位与知识库关联

CXR-QBA 数据集及其构建流水线直接回应了现有胸部X光VQA数据集的两大瓶颈：**规模小且答案简短**，以及**缺乏结构化定位信息**。现有最大数据集 CheXinstruct 仅包含 8.5M 问答对，且答案多为简短标签；而 CXR-QBA 将规模提升至 42.2M（微调级 7.5M），并通过场景图驱动的流水线为每个答案附带多部分详细句子、边界框和结构化标签（区域、发现、确定性等）。这一设计将 VQA 从简单的标签预测任务推向具备可解释性的结构化视觉推理任务。

**与基线方法的关系**：场景图构建的核心基线是 Chest ImaGenome，后者定义了 29 个区域和 53 个发现类别。CXR-QBA 将其扩展至 257 个定位区域和 221 个发现类别，并在 MIMIC-CXR-JPG 测试集上以 MCC 0.71 [0.69,0.73] 超过 Chest ImaGenome 的 0.67 [0.65,0.68]（Table 2a）。在长尾类别（CXR-LT 2024）上提升更为显著（MCC 0.67 vs 0.64），边界框 IoU@30 在 MS-CXR 上提升 6 个百分点（0.51 vs 0.45）。结构化 VQA 任务中，基于 CXR-QBA 微调的模型在逻辑精确率（0.78）和定位精确率（0.89）上远超 MAIRA-2（0.64, 0.32）和 LLaVA-Med v1.5，证实了结构化标签和定位信息对可解释性提升的因果作用。

**适用边界**：该流水线的核心假设是输入报告具有规范的 FINDINGS/IMPRESSION 结构，且图像可通过定位模型提取区域边界框。因此其直接适用域为 MIMIC-CXR 风格的胸部X光报告。自动构建的标签和边界框虽经质量评估，但在长尾发现上仍存在偏差；LLM 评判（Llama 3.1 8B）的过评级率不超过 2%，但 Cohen's kappa 在部分维度仅 0.32-0.41，提示对清晰度等主观维度的评判需人工复核。模板化生成导致问题文本重复度高（平均 238 次重复），但答案文本多样性良好（平均 5 次重复）。

**局限与开放问题**：数据集仅基于单一机构（MIMIC-CXR），泛化性未验证。非正面图像因定位模型限制被排除，减少了数据量。实验揭示了一个关键失败模式：模型在 finding-pos（阳性发现预测）子指标上表现不足，提示数据中存在阳性/阴性样本不平衡问题，需要通过数据过滤或重采样解决。消融实验（Table 16）表明去除边界框和标签训练会降低定位相关指标，但具体影响幅度需进一步量化。此外，RadStrucVQA 指标依赖 LLM 进行蕴含预测，不同 LLM 的选择对最终分数的影响尚未系统研究。该框架能否迁移至其他影像模态（如 CT、MRI）是重要的开放问题。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Structured_Tagged_and_Localized_Visual_Question_Answering_Dataset_with_Full_Sentence_Answers_and_Scene_Graphs_for_Chest_X_ray_Images.pdf

![[paperPDFs/ICLR_2026/A_Structured_Tagged_and_Localized_Visual_Question_Answering_Dataset_with_Full_Sentence_Answers_and_Scene_Graphs_for_Chest_X_ray_Images.pdf]]
