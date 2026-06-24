---
title: Instruction-Guided Lesion Segmentation for Chest X-rays with Automatically Generated Large-Scale Dataset
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Instruction_Guided_Lesion_Segmentation_for_Chest_X_rays_with_Automatically_Generated_Large_Scale_Dataset.pdf
project_link: null
code_link: "https://github.com/checkoneee/ROSALIA"
aliases:
- RRSATLGIAD
- IGLSCXRAGLSD
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过全自动管线利用影像-报告对生成大规模指令-掩码对数据集（MIMIC-ILS），使得视觉语言模型能够理解自然语言指令并执行精确的病变分割。
primary_logic: 放射学报告蕴含丰富的病变语义和位置信息；结合预训练视觉模型和大型语言模型，可以在无人工标注条件下，跨模态对齐并生成高置信度的病变掩码与对应的多样化文本指令，从而训练出能够根据用户指令进行灵活病变分割的视觉语言模型。
claims:
- MIMIC-ILS数据集包含1.1M指令-回答对，覆盖7种主要病变，源自192K张影像。
- 四名放射肿瘤科专家评估数据接受率高达96.4%。
- ROSALIA在指令引导分割任务上大幅领先基线，gIoU 71.2%，cIoU 75.6%，空目标准确率91.8%。
- MIMIC-ILS test set 上 gIoU (%) = 71.2
---

# Instruction-Guided Lesion Segmentation for Chest X-rays with Automatically Generated Large-Scale Dataset

> [!tip] 核心洞察
> 放射学报告蕴含丰富的病变语义和位置信息；结合预训练视觉模型和大型语言模型，可以在无人工标注条件下，跨模态对齐并生成高置信度的病变掩码与对应的多样化文本指令，从而训练出能够根据用户指令进行灵活病变分割的视觉语言模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于指令引导的胸部X光病变分割与自动生成大规模数据集 |
| 英文题名 | Instruction-Guided Lesion Segmentation for Chest X-rays with Automatically Generated Large-Scale Dataset |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.15186) · [Code](https://github.com/checkoneee/ROSALIA) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | ROSALIA (RadiOlogy Segmentation Assistant trained on Lesion-grounded Instruction-Answer dataset) |
| Dataset | MIMIC-ILS test set |

> [!tip] 效果简介
> - MIMIC-ILS test set 上，gIoU (%) 71.2 vs 23.8 (+47.4)；cIoU (%) 75.6 vs 18.5 (+57.1)；N-Acc. (%) 91.8 vs 0.6 (+91.2)。

## 概述

### 问题背景

胸部X光（CXR）是临床最常用的影像检查之一，病变分割对辅助诊断至关重要。然而，现有CXR病变分割模型存在两个关键瓶颈：**只能处理极少数病变类型**，且**依赖复杂、冗长的专家级医学描述作为输入**。用户必须事先解读影像、撰写精确的长句描述（如“双肺感染，右上肺和左上肺两处感染区域”），模型才能执行分割——这在实际临床场景中既不友好也不高效。此外，现有模型无法处理“病变缺失”的确认需求，即当用户询问某部位是否存在病变时，模型缺乏显式的否定回答能力。

### 核心思路

本文的核心洞察是：**放射学报告天然蕴含丰富的病变语义和空间位置信息**——报告中的每一句异常描述都隐含了病变类型、存在性、确定性和解剖位置。若能将这些文本信息与预训练视觉模型提取的空间线索跨模态对齐，就有可能在**无需任何人工标注**的条件下，自动生成高质量的病变掩码与对应的多样化文本指令。

基于此，作者提出了**ROSALIA**（**R**adi**O**logy **S**egmentation **A**ssistant trained on **L**esion-grounded **I**nstruction-**A**nswer dataset），并配套构建了首个全自动指令引导分割数据集**MIMIC-ILS**。整套方案仅利用影像-报告对，通过两阶段管线——先自动生成掩码，再合成指令-回答对——训练视觉语言模型（VLM），使其能够根据简洁的自然语言指令灵活执行病变分割。

### 方法定位

从方法谱系来看，ROSALIA处于**视觉语言模型（VLM）+ 医学影像分割**的交叉地带。现有通用领域模型如**LISA**、**PixelLM**虽支持文本引导分割，但缺乏医学领域知识，无法理解“cardiomegaly”“opacity”等专业术语与对应影像特征的关系。医学领域模型如**BiomedParse**、**RecLMIS**虽针对医学影像设计，但要么仅支持单一类别标签而非自然语言指令，要么仍依赖专家级长句描述。ROSALIA通过MIMIC-ILS数据集将两类方法的优势桥接：让VLM在医学影像上学会理解多样化指令并输出精确掩码，同时具备文本解释能力。

### 主要结果

MIMIC-ILS数据集包含**110万条指令-回答对**，源自**19.2万张CXR影像**和**9.1万个独立分割掩码**，覆盖7种主要病变类型。经四位放射肿瘤科专家独立评估，**数据接受率高达96.4%**，验证了自动生成掩码的可靠性。

在分割性能上，ROSALIA大幅领先所有基线模型：**全局IoU（gIoU）71.2%**（最佳基线23.8%，提升+47.4个百分点），**累积IoU（cIoU）75.6%**（最佳基线18.5%，提升+57.1个百分点），**空目标准确率91.8%**（最佳基线仅0.6%）。空目标准确率的巨大差距表明，ROSALIA是首个能可靠识别“病变不存在”场景的模型，这是现有方法完全缺失的能力。

值得注意的是，模型在局灶性病变（如cardiomegaly，gIoU 0.87）上表现优异，而在弥漫性、边界模糊的病变（如opacity，gIoU约0.55-0.60）上精度有限，这反映了X光成像的固有局限性。此外，病变推理类指令（如根据阴影推断具体病变类型）的准确率受限（pneumonia仅36.7%），但这符合CXR无法提供确定性诊断的临床现实。

### 知识库定位

ROSALIA在知识库中填补了“**指令引导的CXR多病变分割**”这一空白。与依赖人工标注的小规模数据集（如SIIM-ACR仅含气胸单一类别、VinDr-CXR仅提供边界框）不同，MIMIC-ILS首次实现了大规模、多病变、掩码级别且无需人工标注的数据构建。其全自动管线为后续研究提供了可复用的范式：仅需影像-报告对即可为任意医学影像模态生成指令-掩码数据，具有向CT、MRI等三维模态扩展的潜力。

## 背景与动机

胸部X光（CXR）是全球最常用的医学影像检查手段之一，其上的病变分割对于辅助诊断、量化病灶范围和跟踪病情演变至关重要。然而，现有CXR病变分割方法面临两个根本性瓶颈：**病变类型的单一性**和**输入指令的复杂性**。

一方面，传统分割模型通常仅针对单一或少数几类病变进行训练（如肺结节、气胸），无法满足临床中多病变并存的真实场景需求。另一方面，少数具备文本引导能力的分割模型（如**BiomedParse**、**RecLMIS**）虽然支持自然语言输入，但要求用户提供冗长、详细的专家级医学描述（例如“双肺感染，右上肺和左上肺两处感染区域”），这大大提高了使用门槛——用户必须先解读CXR影像才能撰写有效指令，形成“先诊断、后分割”的悖论。

更深层的问题在于**数据匮乏**。指令引导的病变分割（Instruction-guided Lesion Segmentation, ILS）需要大规模的“指令-掩码”配对数据，而现有CXR空间标注数据集（如VinDr-CXR、SIIM-ACR）要么仅覆盖单一病变，要么标注规模有限，且均依赖昂贵的人工标注流程，难以支撑多样化指令的分割训练。

上述缺口催生了本文的核心动机：**能否在零人工标注的条件下，自动构建一个大规模、多病变、支持自然语言指令的CXR分割数据集，并训练出能够理解简洁用户指令、灵活执行特异性分割、全局分割和缺失确认的视觉语言模型？** 这一动机直接指向了放射学报告中蕴含的丰富语义信息——报告不仅描述了病变类型和位置，还隐含了病变的空间范围，若能将其与影像视觉线索跨模态对齐，便有望打通从“影像-报告对”到“指令-掩码对”的全自动构建路径。

## 核心创新

### 瓶颈突破：从专家级描述到自然语言指令

现有胸部X光（CXR）病变分割模型面临两个根本性限制：一是仅能处理单一或极少数病变类型，二是依赖冗长、复杂的专家级医学描述作为输入。例如，用户需要写出“双肺感染，右上肺和左上肺两处感染区域”这样的长句才能触发分割，这严重限制了临床实用性和用户友好度。**ROSALIA** 打破了这一瓶颈：用户只需输入简洁的自然语言指令（如“Segment the pneumonia in the right lung.”），模型即可同时输出分割掩码和文本解释，并支持**特异性分割**、**全局分割**和**缺失确认**三类任务。这一能力跃迁的因果机制在于训练数据的范式变革——从依赖专家手工标注的小规模数据集，转向全自动管线生成的大规模指令-掩码对数据集。

### 核心因果机制：全自动指令-掩码对生成管线

ROSALIA 的核心创新并非模型架构本身，而是其**训练数据的构建方式**。该工作首次提出了一套全自动管线，仅利用影像-报告对，无需任何人工干预，即可生成大规模指令引导分割（ILS）数据集 **MIMIC-ILS**。管线通过四个关键环节实现跨模态对齐与掩码生成：

1. **报告结构化与位置映射**：利用LLM将放射学报告中的异常描述句子转换为六元组（实体、句索引、存在性、确定性、报告位置、疑似病变类型），并将文本位置映射为解剖标签（如“right lung”），为后续视觉定位提供语义锚点。
2. **空间信息提取**：联合三个预训练视觉模型——RadEdit（生成异常图）、CXAS（生成解剖掩码）和预训练YOLO（检测病变框）——从图像端提取多层次的视觉线索。
3. **病变掩码生成与验证**：通过四个条件（解剖重合度、置信度、异常信号强度、框尺寸）过滤YOLO候选框，与异常图求交并后处理生成最终掩码，再经位置验证确认掩码与报告描述的一致性。
4. **指令-回答对自动生成**：根据验证结果，按模板自动生成Basic、Global、Lesion Inference三类指令及对应正负样本回答，覆盖七种主要病变类型（cardiomegaly、pneumonia、atelectasis、opacity、consolidation、edema、effusion）。

这一管线的核心洞察在于：**放射学报告天然蕴含丰富的病变语义和位置信息**，而预训练视觉模型和LLM的成熟使得无监督跨模态对齐成为可能。最终生成的MIMIC-ILS数据集包含1.1M指令-回答对，源自192K张影像和91K个独特分割掩码，经四位放射肿瘤科专家评估，数据接受率高达96.4%。

### 模型设计的差异化定位

在模型层面，ROSALIA采用LLaVA作为VLM骨干，集成SAM作为分割解码器，并通过LoRA（rank=128）进行高效微调。其训练损失函数联合文本生成损失和掩码分割损失：

$$\mathcal{L} = \lambda_{\mathrm{txt}} \mathcal{L}_{\mathrm{txt}} + \mathcal{L}_{\mathrm{mask}}$$

$$\mathcal{L}_{\mathrm{mask}} = \lambda_{\mathrm{bce}} \mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}} \mathcal{L}_{\mathrm{dice}}$$

这一架构设计使得[SEG]标记的隐藏嵌入能够桥接VLM的语义理解和SAM的像素级分割能力。但与现有通用领域referring分割模型（如**LISA-7B/13B**、**PixelLM-7B/13B**）和医学分割模型（如**BiomedParse**、**RecLMIS**）相比，ROSALIA的差异化优势并非来自架构创新，而是源于**训练数据与任务定义的重新设计**：它首次将指令引导分割从“给定复杂描述输出掩码”升级为“理解简洁指令、同时输出掩码和文本解释、并判断病变存在性”的综合性任务。

## 整体框架

ROSALIA的整体框架由两大阶段构成：**自动数据集构建**与**指令引导分割模型训练**。其核心设计思路是：在无需任何人工标注的条件下，仅利用影像-报告对，自动生成大规模指令-掩码对数据集，进而训练一个能够理解自然语言指令并执行灵活病变分割的视觉语言模型。

### 数据生成管线

第一阶段的数据生成管线（图2）是全文的关键贡献。该管线以放射学报告和对应CXR图像为输入，通过四个串行模块自动产出带掩码标注的指令-回答对：

1. **报告结构化与位置映射**：利用LLM将放射学报告中的异常描述句子转化为六元组——`(实体, 句索引, 存在性, 确定性, 位置, 疑似病变类型)`，并将文本位置映射为解剖标签，确保与下游分割模型的兼容性。
2. **空间信息提取**：并行调用三个预训练视觉模型——**RadEdit**生成异常图（anomaly map）、**CXAS**生成解剖掩码、**预训练YOLO**检测病变候选框——为掩码生成提供多源视觉线索。
3. **病变掩码生成**：通过四个条件（解剖重合度、置信度、病变信号强度、框尺寸）过滤YOLO候选框，将其与异常图求交并经后处理，生成最终病变掩码（算法1）。
4. **位置验证**：显式验证生成掩码与报告中位置的一致性，区分出“已落地位置”（grounded location）和“空位置”（empty location），后者用于生成负样本。

最后，基于验证结果和预定义模板，自动生成三类指令-回答对（图3、表2）：
- **Basic**：针对特定位置的病变分割请求
- **Global**：全局病变分割请求
- **Lesion Inference**：根据视觉表现推断病变类型

正样本包含真实掩码和文本描述，负样本则返回空掩码和“不存在”的文本确认。该管线最终产出**MIMIC-ILS数据集**，涵盖7种主要病变类型（cardiomegaly、pneumonia、atelectasis、opacity、consolidation、edema、effusion），包含1.1M指令-回答对，源自192K张影像和91K个独立分割掩码。

### 模型架构

第二阶段的ROSALIA模型（图5）采用**VLM + SAM**的集成架构。输入为CXR图像和自然语言指令，VLM骨干（基于LLaVA）同时生成文本回答和特殊的`[SEG]`标记。该标记的隐藏嵌入被传递给SAM的解码器，结合图像特征生成最终的分割掩码。训练时在VLM上应用LoRA微调（rank=128），联合优化文本生成损失和掩码分割损失：

$$\mathcal{L} = \lambda_{\mathrm{txt}} \mathcal{L}_{\mathrm{txt}} + \mathcal{L}_{\mathrm{mask}}$$

其中掩码损失结合二元交叉熵和DICE系数：

$$\mathcal{L}_{\mathrm{mask}} = \lambda_{\mathrm{bce}} \mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}} \mathcal{L}_{\mathrm{dice}}$$

### 输入输出流

整体系统的输入输出流清晰：用户提供简洁的自然语言指令（如“Segment the pneumonia in the right lung.”），模型同时返回**分割掩码**和**文本解释**，并支持三种任务模式——特异性分割（指定位置）、全局分割（全图范围）和缺失确认（判断病变不存在）。这相较于现有方法（仅能处理单一病变类型且依赖专家级长句描述）构成了根本性的能力跃升。

### 补充图表

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/003_Figure_2.jpg]]
*Figure 2: An overview of grounded lesion mask generation. (Top-left) Textual information is extracted from the radiology report during the report structuring and location mapping. (Bottom-left and Center) Pretrained vision models are also employed to produce spatial information. (Right) Finally, a lesion mask is generated by integrating this information. The verification step then confirms the grounded location (l1), identifies the empty location*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/008_Figure_5.jpg]]
*Figure 5: Overview of ROSALIA. The architecture integrates a VLM with the SAM. The VLM takes a CXR image and a segmentation instruction as input, generating both a textual description and a special [SEG] token. The hidden embedding of this [SEG] token is then passed to SAM’s decoder to produce the final mask*

## 核心模块与公式推导

ROSALIA 的核心技术栈由两个阶段构成：**自动数据集构建管线**与**指令引导分割模型**。前者负责从影像-报告对中无监督地生成大规模的指令-掩码对数据集 MIMIC-ILS，后者基于该数据集训练视觉语言模型，使其能够理解自然语言指令并输出精确的病变分割掩码。

### 数据集构建管线：从报告到掩码的全自动生成

该管线是整篇工作的基石，其核心挑战在于：如何在不依赖任何人工像素级标注的前提下，仅利用放射学报告中的文本描述与对应的 CXR 影像，自动生成高置信度的病变分割掩码。管线由四个串行模块构成，其整体流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/004_Figure_3.jpg]]
*Figure 3: Instruction–answer pair generation process using the example report, “Bibasilar atelectasis. Cardiomegaly.” We utilize the elements extracted from the previous lesion mask generation process (see Fig. 2), indicated by the dashed box. Structured tuples (A&B in the top left) are converted to text instructions and mapped to their corresponding ground-truth masks and textual descriptions. Invalid instructions for lesions which lack a corresponding mask are excluded (colored as red), and only valid instructions are retained (colored as green). (ET: entity, PS: presence, CT: certainty, RL: reported location, GL: grounded location, EL: empty location)*

**报告结构化与位置映射** 首先使用大语言模型（LLM）将放射学报告中描述异常发现的每个句子转换为一个六元组：

$$
(\text{entity}, \text{sentence index}, \text{presence}, \text{certainty}, \text{location}, \text{predicted lesion type})
$$

其中 `location` 元素被进一步映射到一个或多个解剖标签（如“右肺上叶”），以确保与下游分割模型兼容。这一步将非结构化的自然语言报告转化为结构化的语义信息，为后续的跨模态对齐提供了文本锚点。

**空间信息提取** 从影像侧并行提取三类视觉线索：
- **异常图**：利用 RadEdit 模型生成编辑前后的差异图，通过阈值化得到异常像素集合 $\mathcal{A}$，定义为：

$$
\mathcal{A} = \{ (i,j) \mid (x_{\mathrm{ano}})_{i,j} \geq \tau_{\mathrm{ano}} \}, \quad x_{\mathrm{ano}} = \frac{x - \hat{x}}{I_{\mathrm{max}}}
$$

其中 $x$ 为原始 CXR，$\hat{x}$ 为 RadEdit 重建的正常影像，$I_{\mathrm{max}}$ 为最大像素强度。$\mathcal{A}$ 提供了病变的大致形态学边界。
- **解剖掩码**：由 CXAS 模型生成左右肺等解剖结构的语义分割掩码，用于空间约束。
- **病变检测框**：由预训练 YOLO 模型输出候选病变边界框及其置信度。

**病变掩码生成** 通过四个条件对 YOLO 候选框进行递进式过滤，并与异常图求交以生成最终掩码。关键过滤条件包括：

$$
c_1: \frac{|B_j \cap \mathcal{M}_{\mathrm{union}}|}{|B_j \cup \mathcal{M}_{\mathrm{union}}|} \ge \tau_{\mathrm{anatomy}}, \quad c_2: \mathrm{conf}_{B_j} \ge \tau_{\mathrm{conf}}
$$

$c_1$ 确保检测框与报告位置对应的解剖掩码 $\mathcal{M}_{\mathrm{union}}$ 有足够的空间重叠（IoU 阈值 $\tau_{\mathrm{anatomy}}$），$c_2$ 过滤低置信度框。随后通过 $c_3$ 和 $c_4$ 进一步保留包含强病变信号且尺寸足够大的框，最终将过滤后的框与异常图 $\mathcal{A}$ 取交集，经后处理得到病变掩码。

**位置验证** 将生成的掩码与报告中的位置进行一致性校验：成功匹配的标记为“已落地位置”，用于生成正样本；报告中提及但未能生成掩码的位置标记为“未落地位置”并丢弃；报告中未提及的区域标记为“空位置”，用于构造负样本。

### 指令-回答对生成：三类任务模板

基于验证后的结构化元组，管线自动生成三种类型的指令-回答对（如 Figure 3 和 Table 2 所示）：
- **Basic**：针对特定位置和病变类型的特异性分割指令（如“Segment the pneumonia in the right lung.”）。
- **Global**：对整张影像中所有可见病变的全局分割指令。
- **Lesion Inference**：仅给出位置描述，要求模型推断并分割可能的病变类型。

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/005_Table_2.jpg]]
*Table 2: Templates for each question type. Each type includes answer templates for both positive and negative cases, with the negative answers positioned in the last row of each cell*

正样本回答包含病变类型、位置描述和对应的掩码；负样本回答则声明“未发现目标”并返回空掩码。这一设计使模型同时具备了特异性分割、全局分割和缺失确认三种能力。

### ROSALIA 模型架构与训练损失

ROSALIA 的模型架构如 Figure 5 所示，采用 LLaVA 作为 VLM 骨干，集成 Segment Anything Model（SAM）作为分割解码器。VLM 接收 CXR 图像与文本指令，生成文本回答和一个特殊的 `[SEG]` 标记；该标记的隐藏嵌入随后被送入 SAM 的解码器，与图像特征融合后生成最终的分割掩码。为降低训练开销，在 VLM 上应用了秩为 128 的 LoRA 微调。

训练采用联合损失函数：

$$
\mathcal{L} = \lambda_{\mathrm{txt}} \mathcal{L}_{\mathrm{txt}} + \mathcal{L}_{\mathrm{mask}}
$$

其中 $\mathcal{L}_{\mathrm{txt}}$ 为文本生成损失，$\mathcal{L}_{\mathrm{mask}}$ 为分割掩码损失，定义为二元交叉熵与 DICE 系数的加权组合：

$$
\mathcal{L}_{\mathrm{mask}} = \lambda_{\mathrm{bce}} \mathcal{L}_{\mathrm{bce}} + \lambda_{\mathrm{dice}} \mathcal{L}_{\mathrm{dice}}
$$

这一联合优化目标使模型能够同时学习文本指令的语义理解和像素级分割的对齐能力。

## 实验与分析

### 1. 主实验结果：指令引导分割性能

ROSALIA在MIMIC-ILS测试集上对所有基线模型实现了压倒性优势。核心瓶颈在于：现有模型要么仅能处理单一病变类别，要么需要冗长的专家级医学描述作为输入，完全无法应对“简单指令→精确掩码+缺失确认”的联合任务。ROSALIA通过在大规模、高质量指令-掩码对上训练，从根本上解决了这一矛盾。

**Table 4** 报告了各模型的分割性能。ROSALIA取得了**gIoU 71.2%**、**cIoU 75.6%**，分别领先最强基线**+47.4**和**+57.1**个百分点。更关键的是**空目标准确率（N-Acc.）高达91.8%**，而所有基线模型在此指标上几乎完全失效（如BiomedParse仅为0.6%）。这意味着基线模型倾向于在任何输入下都“强行”生成一个掩码，缺乏判断病变是否真实存在的能力——这正是临床部署中不可接受的行为。

通用领域referring分割模型（LISA-7B/13B、PixelLM-7B/13B、Text4Seg）在CXR病变上的gIoU普遍低于25%，说明自然图像训练的视觉语言模型无法直接迁移到医学影像领域。即便是医学领域专用模型BiomedParse和RecLMIS，其gIoU也仅分别为23.8%和27.8%，远不及ROSALIA。这反证了MIMIC-ILS数据集的核心价值：并非任何医学VLM都能做好指令引导分割，关键在于训练数据的规模、质量和任务对齐程度。

### 2. 按病变类型的性能分析

**Table 5** 揭示了ROSALIA在不同病变类型上的性能差异，这直接反映了X光成像的固有物理限制：

- **局灶性、边界清晰的病变**表现优异：cardiomegaly（心脏扩大）gIoU达**87.0%**，effusion（胸腔积液）为**83.1%**，consolidation（实变）为**78.5%**。这些病变在CXR上具有明确的解剖边界和相对固定的位置特征。
- **弥漫性、边界模糊的病变**性能下降：opacity（不透光区）gIoU仅**55.7%**，edema（肺水肿）为**59.5%**。这类病变本身在X光上就缺乏清晰边界，即使对于放射科医生也难以精确勾画轮廓——这是模态限制，而非模型缺陷。
- 所有七种病变的gIoU均超过55%，cIoU均超过60%，表明模型具有广泛的病变覆盖能力。

### 3. 文本回答准确率

ROSALIA不仅输出掩码，还同时生成文本解释。**Table 6** 报告了不同问题类型下的文本回答准确率：

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/011_Table_6.jpg]]
*Table 6: Text response accuracy (%) of ROSALIA*

- **Basic指令**（如“Segment the pneumonia in the right lung.”）准确率较高，正负例判断准确。
- **Global指令**（如“Segment all cardiomegaly.”）同样表现稳健。
- **Lesion Inference指令**（如根据阴影推断具体病变类型）准确率有限，例如pneumonia推断仅**36.7%**。这并非模型设计缺陷，而是因为CXR本身无法提供确诊级别的信息——同一阴影可能对应多种病理，确定性诊断需要临床背景或CT确认。模型在此类任务上的“低准确率”恰恰反映了其输出与临床不确定性的合理对齐。

### 4. 消融实验：数据质量 vs. 数据数量

一项关键消融实验验证了“高质量掩码比高召回率更重要”的核心假设。当放宽数据生成阈值以提高召回率时，训练出的模型在MIMIC-ILS测试集上性能大幅下降：gIoU从71.2%降至**54.3%**，cIoU从75.6%降至**61.4%**。尽管N-Acc.从91.8%略微上升至95.8%，但整体分割质量的严重退化表明：引入噪声掩码对模型学习的破坏远大于额外正样本带来的收益。MIMIC-ILS的设计哲学——“追求高精度而非高召回”——在此得到实证支持。

另一项消融验证了数据集的泛化多样性。对MIMIC-ILS中的指令进行释义（paraphrasing）后重新训练，模型仍保持强健性能：gIoU **67.3%**，cIoU **73.1%**，N-Acc **96.5%**。这表明模型并未过拟合到固定的指令模板，而是真正学会了理解指令语义并映射到视觉特征。

### 5. 数据集质量与专家评估

MIMIC-ILS测试集经过严格的专家审核。**Table 3** 显示，四位放射肿瘤科专家对10.7K个掩码样本进行独立评估，**96.4%**被评定为可接受并纳入最终测试集。这一高接受率验证了全自动管线生成掩码的可靠性。需注意：训练集和验证集未经过同等人工过滤，可能存在少量噪声，这为未来通过弱监督或在线学习进一步提升留下了空间。

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/007_Table_3.jpg]]
*Table 3: Acceptance rate and number of evaluated samples for the human evaluation. Each sample corresponds to a unique combination of lesion mask, target, and location*

### 6. 可视化对比

**Figure 6** 提供了ROSALIA与基线模型的可视化对比。前三行为正样本（存在病变），ROSALIA生成的掩码与ground-truth高度吻合，而基线模型或产生粗糙边界，或错误分割非目标区域。最后一行展示了负样本（空目标），ROSALIA正确输出空掩码，而基线模型普遍产生假阳性分割——这与N-Acc.指标的低分一致，揭示了现有模型在“确认缺失”能力上的系统性缺陷。

### 7. 与现有数据集的规模对比

**Table 1** 将MIMIC-ILS与现有CXR空间标注数据集进行了对比。MIMIC-ILS包含**1.1M指令-回答对**，源自**192K张影像**和**91K个独特分割掩码**，覆盖**七种主要病变类型**。相比之下，现有数据集要么样本量小（通常数千级别），要么仅覆盖单一或少类病变，且均依赖人工标注。MIMIC-ILS首次实现了全自动、大规模、多病变的指令-掩码对构建，为指令引导的CXR病变分割奠定了数据基础。

### 补充图表

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/009_Table_4.jpg]]
*Table 4: Segmentation results (%) on the MIMIC-ILS test set. “N-Acc.” denotes the accuracy of correctly predicting empty targets. ¶ indicates medical domain baselines. The best and second-best results are marked in bold and underline, respectively*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/013_Figure_6.jpg]]
*Figure 6: Visualized inference results of ROSALIA and baseline models. The first three rows show results for positive cases, while the last row presents results for negative cases with an empty target mask. Additional examples are demonstrated in Appendix G*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/002_Table_1.jpg]]
*Table 1: Existing CXR datasets with spatial annotations for pathologic lesions*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/001_Figure.jpg]]
*Figure: (A) Specific Segmentation (C) Absence Confirmation*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/010_Figure.jpg]]
*Figure: LISA-13B PixelLM-13B GT*

![[assets/figures/papers/paper_list_l2743_https_arxiv_org_abs_2511_15186/figures/012_Figure.jpg]]
*Figure: “Segment the cardiomegaly.”*

## 方法谱系与知识库定位

### 任务定义与定位

ROSALIA 解决的是**指令引导的胸部X光（CXR）病变分割**（Instruction-guided Lesion Segmentation, ILS）任务：给定一张CXR图像和一句自然语言指令（如“Segment the pneumonia in the right lung.”），模型需同时输出病变分割掩码和文本回答，并能正确处理病变不存在的情况（空目标确认）。这一定位使 ROSALIA 处于**医学视觉语言模型**、**指代表达分割**和**半监督/无监督数据生成**三个领域的交叉点。

### 与基线方法的关系

#### 通用领域指代分割模型

论文将 ROSALIA 与四类通用领域模型直接对比（Table 4）：

- **LISA-7B/13B**：基于LLaVA+SAM架构的指代分割模型，是 ROSALIA 最直接的架构参照。在MIMIC-ILS测试集上，LISA-7B仅取得gIoU 23.8%、cIoU 18.5%、空目标准确率0.6%，表明通用模型在缺乏医学领域适配时，几乎完全无法处理CXR病变分割任务，尤其对空目标场景完全失效。
- **PixelLM-7B/13B**：像素级视觉语言分割模型，虽能生成掩码，但在医学领域同样表现不佳，且不具备空目标识别能力。
- **Text4Seg**：文本引导分割模型，未针对医学指令场景设计，性能有限。

这些对比揭示了一个关键发现：**通用指代分割模型的瓶颈不在于架构容量，而在于缺乏医学领域的大规模指令-掩码对齐训练数据**。ROSALIA 通过在MIMIC-ILS上微调LISA架构，将gIoU从23.8%提升至71.2%，验证了这一判断。

#### 医学领域分割模型

与医学专用模型的对比进一步凸显 ROSALIA 的差异化优势：

- **BiomedParse**：医学图像分割基础模型，支持文本提示，但设计目标为通用医学分割而非指令引导的CXR病变分割，在MIMIC-ILS上的空目标准确率极低。
- **RecLMIS**：专门针对CXR的文本引导病变分割模型，但其输入要求复杂的专家级医学描述，且仅能处理单一病变类型。相比之下，ROSALIA 接受简洁的日常语言指令，支持多病变类型、多位置的特异性分割和全局分割。

ROSALIA 相对于这两类医学基线，核心改进在于**交互范式的简化**——用户无需具备放射学专业知识即可通过自然语言指令获得精确分割结果。

### 方法谱系中的继承与创新

#### 继承的技术组件

ROSALIA 的方法栈可追溯至多个成熟技术线：

1. **VLM骨干**：采用 **LLaVA**（Liu et al., NeurIPS 2023）作为视觉语言模型骨干，负责理解图像-指令对并生成文本响应和[SEG]标记嵌入。
2. **分割解码器**：采用 **SAM**（Kirillov et al., ICCV 2023）的掩码解码器，接收[SEG]标记嵌入和图像特征生成最终掩码。
3. **参数高效微调**：在VLM上应用 **LoRA**（Hu et al., ICLR 2022），rank=128，降低训练成本。
4. **预训练视觉模型**：数据生成管线中集成了 **RadEdit**（异常图生成）、**CXAS**（解剖结构分割）和预训练YOLO检测器（病变框检测），均为已有工作的直接复用。

#### 核心创新点

ROSALIA 的方法论创新集中在**数据生成范式**而非模型架构：

1. **全自动指令-掩码对生成管线**：首次实现仅依赖影像-报告对、无需人工标注的大规模ILS数据集构建。管线通过四个串联模块（报告结构化→空间信息提取→病变掩码生成→位置验证）将放射学报告中的语义信息与视觉线索跨模态对齐，生成高置信度掩码。

2. **三类指令模板设计**：设计了Basic（基础定位分割）、Global（全局病变分割）、Lesion Inference（病变推理）三种指令类型，并分别为正负样本构建回答模板，使模型同时学习分割和“病变不存在”的确认能力。

3. **空目标处理机制**：通过位置验证步骤识别报告中提及但视觉上未定位到的“空位置”，显式生成负样本，使模型获得空目标准确率91.8%的能力——这是所有基线模型（最高仅0.6%）完全不具备的。

### 适用边界与限制

#### 数据层面

- **报告依赖性**：自动掩码生成的质量高度依赖放射学报告的完整性和准确性。若报告遗漏关键病变描述，将直接导致掩码漏检，且这种噪声在训练集中未经过滤（仅测试集经专家审核）。
- **体位限制**：数据集仅纳入PA和AP位胸片，未包含侧位片，模型对侧位或非常规角度的泛化能力未经验证。
- **病变类型覆盖**：虽覆盖7种主要病变，但临床CXR中仍存在大量其他异常（如结节、纤维化、胸腔积液之外的胸膜异常等），模型在这些病变上的行为未知。

#### 模型层面

- **弥漫性病变分割精度不足**：在opacity、edema等边界模糊的弥漫性病变上，gIoU约0.55-0.60，显著低于局灶性病变（如cardiomegaly gIoU 0.87），体现X光成像的固有局限性——弥漫性病变缺乏明确边界，即使人工标注也存在较大变异。
- **病变推理能力有限**：Lesion Inference指令（如根据阴影推断具体病变类型）准确率较低（pneumonia仅36.7%），这并非模型缺陷，而是CXR本身无法提供确诊信息的临床现实。该指令类型的实用价值更多体现在辅助筛查而非诊断。
- **训练噪声影响**：训练集未经人工过滤，尽管测试集经四位放射肿瘤科专家审核且接受率96.4%，训练噪声可能制约模型极限性能。

#### 任务层面

- **单轮交互**：当前仅支持单轮指令，无法通过多轮对话逐步细化分割需求。
- **二维限制**：方法设计针对二维X光片，尚未扩展至CT、MRI等三维模态。

### 开放问题与后续方向

1. **弥漫性病变精度提升**：如何通过改进异常图生成质量、引入不确定性建模或边界感知损失来提升opacity/edema等病变的分割精度，是临床实用化的关键瓶颈。

2. **跨模态扩展**：自动标注管线能否迁移至CT/MRI三维数据，利用三维报告中的空间描述生成体素级掩码，实现跨模态的指令引导分割。

3. **弱监督质量提升**：在保持全自动的前提下，能否引入放射科医生的隐式反馈（如报告修正行为）或在线学习机制，持续优化掩码质量和模型性能。

4. **对话式交互**：如何设计多轮对话机制，使用户可通过渐进式细化（如“再往左一点”“扩大范围”）获得更精确的分割结果。

5. **临床部署验证**：当前评估仅限于离线测试集，缺少前瞻性临床研究验证模型在实际工作流中对放射科医生效率、诊断准确性的影响。

6. **报告缺失场景**：对于报告质量差或缺失的影像，当前管线完全失效。探索仅依赖视觉线索的弱监督或无监督掩码生成，是提升数据覆盖面的重要方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Instruction_Guided_Lesion_Segmentation_for_Chest_X_rays_with_Automatically_Generated_Large_Scale_Dataset.pdf]]
