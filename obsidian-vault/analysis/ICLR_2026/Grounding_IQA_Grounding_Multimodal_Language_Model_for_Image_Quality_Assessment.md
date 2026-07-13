---
title: "Grounding-IQA: Grounding Multimodal Language Model for Image Quality Assessment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Grounding_IQA_Grounding_Multimodal_Language_Model_for_Image_Quality_Assessment.pdf
project_link: null
code_link: https://github.com/zhengchen1999/Grounding-IQA
aliases:
- GI
- Grounding-IQA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/computer_vision_task
core_operator: "将多模态指称（referring）与定位（grounding）机制引入图像质量评价，让模型能够在质量描述和问答中提供并利用精确的边界框坐标，从而实现从整体到局部的精细化质量感知。"
primary_logic: "图像质量评估不仅需要语言描述，还需要类似人类视觉系统的空间对应能力；通过要求模型在生成质量描述或回答问题时输出关键对象的空间坐标（或依据坐标回答问题），可以迫使模型关注局部区域的低层视觉属性，从而获得更细粒度的质量理解。"
claims:
- "提出 grounding-IQA 新范式，将多模态指称与定位融入 IQA，支持带坐标的细粒度描述（GIQA-DES）和涉及局部区域的视觉问答（GIQA-VQA）。"
- "所构建的 GIQA-160K 数据集通过自动化标注流水线提供带边界框的质量描述和问答对，使得现有 MLLM 可通过微调获得 grounding-IQA 能力。"
- "在 GIQA-Bench 上，经过 GIQA-160K 微调的模型在描述质量（LLM-Score）、问答准确率和定位精度（mIoU/Tag-Recall）上均显著优于未微调基线和传统 IQA/grounding 模型。"
- "GIQA-Bench 上 GIQA-DES LLM-Score = 63.00 (mPLUG-Owl2-7B + GIQA-160K multi-task)"
---

# Grounding-IQA: Grounding Multimodal Language Model for Image Quality Assessment

> [!tip] 核心洞察
> 图像质量评估不仅需要语言描述，还需要类似人类视觉系统的空间对应能力；通过要求模型在生成质量描述或回答问题时输出关键对象的空间坐标（或依据坐标回答问题），可以迫使模型关注局部区域的低层视觉属性，从而获得更细粒度的质量理解。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Grounding-IQA：结合定位的多模态语言模型用于图像质量评估 |
| 英文题名 | Grounding-IQA: Grounding Multimodal Language Model for Image Quality Assessment |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=yEpE0QPpf8) · [GitHub](https://github.com/zhengchen1999/Grounding-IQA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/computer_vision_task |
| Method | Grounding-IQA |
| Dataset | GIQA-Bench |

> [!tip] 效果简介
> - GIQA-Bench 上，GIQA-DES LLM-Score 为 63.00 (mPLUG-Owl2-7B + GIQA-160K multi-task)，对比 48.25 (mPLUG-Owl2-7B zero-shot)，变化 +14.75。
> - GIQA-Bench 上，GIQA-VQA Acc(Total) 为 0.7417 (mPLUG-Owl2-7B + GIQA-160K multi-task)，对比 0.5900 (mPLUG-Owl2-7B fine-tuned only on GIQA-DES, as an approximate weak baseline)，变化 +0.1517。

## 概要

现有基于多模态大语言模型（MLLM）的图像质量评价方法通常只产生通用文本描述，缺乏精确的空间定位能力，难以在局部物体或区域层面刻画失真成因，限制了其对精细质量感知的支持。为解决这一瓶颈，本文提出**Grounding‑IQA**——一种将多模态指称（referring）与定位（grounding）机制融入图像质量评价的新范式。该范式引入两个子任务：**GIQA‑DES**（带边界框坐标的质量描述）和**GIQA‑VQA**（面向局部区域的视觉问答），使模型在输出质量描述或回答问题时可同时提供或利用物体的精确空间坐标，从而具备类似人类视觉系统的细粒度质量感知。

为获得训练该类能力所需的大规模数据，作者设计了一条自动标注流水线，基于已有质量描述数据构造了包含约 16.8 万个指令样本的**GIQA‑160K**数据集。在该数据集上以多任务方式微调现有 MLLM（如 mPLUG‑Owl2‑7B），即可使模型获得 grounding‑IQA 能力，而无需从头训练专用模型。在精心构建的**GIQA‑Bench**评测平台上，经过 GIQA‑160K 微调的模型（Grounding‑GPT）在质量描述语言得分（LLM‑Score）、视觉问答准确率和边界框定位精度（mIoU/Tag‑Recall）上均大幅超越未微调基线以及传统的 IQA 或 grounding 模型；消融实验进一步表明，多任务联合训练、边界框后处理（IQA‑Filter 与 Box‑Merge）以及离散网格坐标表示均对最终性能有正向贡献。

尽管如此，该框架仍受限于自动标注流水线所依赖的外部模型质量、离散化造成的亚网格精度损失，以及评测基准规模较小等因素，相关结论在更大规模、更多样化场景下的稳健性尚需进一步验证。



图像质量评价（Image Quality Assessment, IQA）是计算机视觉中的基础任务，传统方法主要输出单一的全局质量分数，难以刻画影响质量的局部因素。近年来，随着多模态大语言模型（MLLM）的发展，研究者开始将 IQA 从数值回归拓展到语言生成与问答，例如利用模型给出自然语言的质量描述或回答关于图像属性的问题。然而，这些基于 MLLM 的 IQA 方案仍停留在“整体上下文描述”层面：它们缺乏精确的空间定位信息，无法明确指出图像中哪些区域或哪些对象存在怎样的质量缺陷，从而在细粒度质量感知上存在明显鸿沟。即便是部分工作尝试定位退化区域（如 Q-Ground），也未能支持用户通过指称方式交互地查询特定对象的低层视觉属性——这正是人类视觉系统固有的空间对应能力。

上述缺口的根本原因在于现有 IQA 范式没有将多模态指称（referring）与定位（grounding）机制引入质量评估流程。为了实现对局部失真的精准刻画和可交互的细粒度质量问答，需要一种能够同时处理语言描述和空间坐标的新任务范式。本文据此提出 **Grounding‑IQA**：通过要求模型在生成质量描述时给出关键对象的边界框坐标，或者在问答中依据坐标回答问题、输出特定区域的属性，迫使模型关注局部区域的低层视觉特征，从而获得类似人类的空间‑质量联合感知能力。具体而言，Grounding‑IQA 包含两个子任务——**GIQA‑DES**（带有精确边界框坐标的细粒度质量描述）和 **GIQA‑VQA**（涉及局部区域的视觉问答，包含指称与定位两种场景），全面覆盖从整体到局部的质量感知需求。

为使现有 MLLM 具备上述地面化 IQA 能力，本文构建了一个大规模数据集 **GIQA‑160K**。该数据集通过自动标注管线将已有的纯文本质量描述转化为带坐标的细粒度描述和问答对，从而为模型提供监督信号。初步实验表明，在 GIQA‑160K 上微调后的 MLLM 在描述质量、问答准确率和定位精度等指标上显著优于通用 MLLM、专用 IQA 模型以及传统 grounding 方法，验证了将空间定位融入 IQA 的有效性。



## 核心方法与创新机理

现有基于多模态大语言模型（MLLM）的图像质量评价（IQA）方法仅通过自然语言描述整体质量，缺乏将描述与图像中具体对象或区域对齐的空间定位能力，这成为制约细粒度质量感知的本质瓶颈。Grounding-IQA 的核心创新在于将多模态指称（referring）与定位（grounding）机制系统性地融入 IQA，通过四个关键设计变革（changed slots）使模型能够在质量描述和问答中输出或利用精确的边界框坐标，从而迫使模型关注局部低层视觉属性，实现从“看图说话”到“看图指物”的范式跃迁。

### 1. 新型任务范式：GIQA-DES 与 GIQA-VQA

传统 IQA 的多模态对话仅要求模型输出不带空间坐标的纯文本描述或答案。Grounding-IQA 将其分化为两个互补的子任务（Fig. 2, Sec. 3.1）：
- **GIQA-DES**：模型必须生成包含关键对象/区域边界框坐标的质量描述，将“哪里出了问题”与“出现了什么失真”在文本中统一表达。例如，答案中同时出现“……在 <grid-索引> 区域存在模糊……”，坐标以文本 token 形式嵌入（Fig. 5a, Sec. 3.2 Stage-4）。
- **GIQA-VQA**：问答对中的问题或答案包含离散边界框坐标，分别对应 **referring** 场景（给定坐标询问区域失真属性）与 **grounding** 场景（回答问题时输出坐标），从而同时训练模型的指称理解和定位输出能力（Fig. 5b）。

这一设计使得原本仅作为文本分类/回归的 IQA 任务转变为需要空间‑语言联合对齐的多模态任务，是方法相对于通用 MLLM（如 mPLUG-Owl2-7B zero-shot）和传统 IQA 描述模型（如 Q-Instruct）的最根本改变（changed slot “训练任务格式”）。

### 2. 离散网格坐标表示

模型输出的坐标形式决定了位置学习的难度与精度。基线 grounding 模型通常采用归一化连续值 `[x1, y1, x2, y2]`，每个数值需占用大量 token（如 21 个 token）且浮点表示复杂。Grounding-IQA 改用 **20×20 离散网格**，将框角点映射为两个整数索引（$\mathrm{idx}_l, \mathrm{idx}_r$）：
$$
\mathrm{idx}_l = y_1 \cdot m \cdot n + x_1 \cdot n, \quad \mathrm{idx}_r = y_2 \cdot m \cdot n + x_2 \cdot n \qquad (m=n=20)
$$
该设计将坐标压缩至最多 9 个 token，显著降低了文本生成模型的表示负担（changed slot “坐标数值表示”）。消融实验（Table 2b）证实：采用离散坐标（Disc-Coord）后，描述质量（BLEU@4 23.67、LLM-Score 61.75）和标签召回（Tag-Recall 0.5497）均优于连续坐标（Norm‑Coord），虽然 mIoU 略有下降（0.5851 vs 0.6046），但文本生成质量的提升证明了离散化在“语言‑坐标”协同优化中的优势。

### 3. 自动化多阶段数据构建管线与 GIQA-160K

现有 MLLM 缺乏 grounding-IQA 训练数据。为解决数据瓶颈，作者设计了一条四阶段自动标注管线（Fig. 3, Sec. 3.2）：
1. **Object Tag Extraction**：利用 Llama3 从现有质量描述中抽取关键对象及其失真类别（如“人物-模糊”）。
2. **Bounding Box Detection**：引入描述短语 $\mathcal{T}_r$（而非单纯对象名）作为 Grounding DINO 的提示，提升检测准确性（Fig. 4）。
3. **Box Refinement**：通过 IQA-Filter（基于 MLLM 的语义一致性验证）剔除错误框，再使用 Box-Merge 合并小且重叠的框，保证数据质量（Table 2a 显示 Ref‑Box 将 mIoU 从 0.5624 提升至 0.5851，Tag‑Recall 从 0.5045 提升至 0.5497）。
4. **Transformation & Fusion**：将过滤后的框离散化并嵌入描述，形成完整答案。

基于此管线构建的 **GIQA-160K** 数据集（包含 167,657 个指令样本，覆盖 42,960 张图像）是使预训练 MLLM 获得 grounding-IQA 能力的关键（changed slot “微调数据”）。多任务联合训练消融（Table 3）表明：同时使用 GIQA-DES 和 GIQA-VQA 数据（GIQA-160K）相比仅用单一子任务数据，能同时提升描述质量（LLM-Score 63.00 vs 仅 VQA 的 38.50）和问答准确率（Acc 0.7417 vs 仅 DES 的 0.6395），证实了多任务协同的必要性。

### 4. 相对于基线的联合增效

上述改变并非孤立作用：离散坐标降低了 grounding 学习的难度，自动管线提供了必需的大规模多任务数据，而多任务训练则使描述与问答能力相互促进。在 GIQA-Bench 上的综合对比（Fig. 1, Table 5）显示，经 GIQA-160K 微调的 mPLUG-Owl2‑7B 在 GIQA-DES 的 LLM-Score 上达到 63.00，远超零样本基线（48.25）和纯描述模型 Q-Instruct（57.61）；在 GIQA-VQA 的总体准确率上达到 0.7417，显著优于仅具备退化定位的 Q-Ground（0.4179）和通用 grounding 模型 Shikra-7B（0.4086）。这些结果表明，通过范式、表示和数据的联合创新，Grounding-IQA 首次使 MLLM 具备了兼备精细质量描述与空间定位的统一能力。



![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/006_Figure_3.jpg]]
*Figure 3: The illustration of the automated annotation pipeline. (a) GIQA-DES Pipeline: Constructs the answer from the given image and description via a four-stage process, while the question comes from a predefined question pool. (b) GIQA-VQA Pipeline: Generates the corresponding QA data utilizing descriptions from GIQA-DES and the LLM (Llama3 (Dubey et al., 2024))*

现有基于多模态大语言模型（MLLM）的图像质量评价方法主要依赖全局语义描述，无法在文本中显式编码对象或局部区域的空间位置，导致其在细粒度质量感知上存在明显不足。Grounding‑IQA 通过将多模态指称（referring）与定位（grounding）引入 IQA，构建了一个既能描述整体质量又能以离散坐标锚定关键局部区域的统一范式。该范式包含两个互补的子任务：**GIQA‑DES**（生成带有精确边界框坐标的质量描述）与 **GIQA‑VQA**（回答涉及局部区域的低层属性问题），二者的协同使得模型具备了类似人类视觉系统的空间对应能力。

为实现这一范式，作者设计了一套**自动化数据标注流水线**，并以该流水线产出的 **GIQA‑160K** 多任务指令数据集为桥梁，将通用预训练 MLLM 微调为具备 grounding‑IQA 能力的模型。Figure 3 给出了流水线的整体架构，其核心是一个四阶段过程，用于从已有的纯文本质量描述中反向构造包含坐标标注的高质量回答；GIQA‑VQA 的问答对则进一步利用 GIQA‑DES 描述与 Llama3 自动生成。

### 从文本描述到带坐标答案的自动构造（GIQA‑DES）

流水线的输入是一组图像及其对应的质量描述文本（如 Q‑Instruct 生成的描述），输出则是嵌入了离散边界框坐标的完整答案文本。四个阶段依次为：

1. **目标标签抽取（Stage‑1：Object Tag Extraction）**  
   利用 Llama3 从质量描述中抽取出关键对象名称、其质量标签（如“锐度不足”“噪声”）以及效果类别（增强/退化）。这为后续检测提供了富有语义的提示，亦使坐标输出与具体质量属性形成对应。

2. **边界框检测（Stage‑2：Bounding Box Detection）**  
   采用 Grounding DINO，以抽取出的描述短语 $\mathcal{T}_r$（而非仅对象名称）作为查询，生成候选边界框。使用描述短语可显著提升检测精度（Figure 4 显示，短语“the man wearing a white t‑shirt”比单独使用名称“man”更准确），从而降低标注噪声。

3. **框的精细化（Stage‑3：Box Refinement – IQA‑Filter & Box‑Merge）**  
   这一阶段是保证标注质量的关键瓶颈。首先，通过 MLLM（如 Q‑Instruct）对候选框区域进行质量验证，过滤掉不符合描述语义的错误框（IQA‑Filter）。随后，对面积过小或高度重叠的框进行合并（Box‑Merge），以减少冗余并提升标注的稳定性。消融实验（Table 2a）证实，经精细化后的框（Ref‑Box）在 mIoU 上从原始框（Raw‑Box）的 0.5624 提升至 0.5851，Tag‑Recall 亦从 0.5045 提升至 0.5497，同时文本质量指标（BLEU@4 和 LLM‑Score）均有显著改善。

4. **坐标离散化与融合（Stage‑4：Transformation and Fusion）**  
   为便于语言模型以少量 token 生成坐标，归一化的连续边界框角点被离散化为 $20\times20$ 网格索引：
   $$\mathrm{idx}_l = y_1 \cdot m \cdot n + x_1 \cdot n, \quad \mathrm{idx}_r = y_2 \cdot m \cdot n + x_2 \cdot n \quad (\text{Eq. 1})$$
   下游任务中，可通过式 (2) 从网格索引近似还原连续中心坐标。消融结果（Table 2b）表明，离散坐标表示在文本生成质量（BLEU@4 23.67，LLM‑Score 61.75）和 grounding 精度（Tag‑Recall 0.5497）上全面优于归一化连续坐标（Norm‑Coord），尽管 mIoU 略降。这一设计本质是在坐标精度与语言模型可学习性之间作出的权衡，降低了原始连续坐标所需的 21‑token 开销，使模型更易收敛。

最终，离散坐标被直接嵌入原始描述文本中，形成 GIQA‑DES 的标准答案格式（Figure 5a 示例）。

### GIQA‑VQA 数据生成与多任务指令微调

GIQA‑VQA 旨在评估模型在局部区域的属性问答能力，涵盖两类场景：**referring**（问题中给出坐标，要求判断该区域的质量属性）和 **grounding**（问题询问某个质量属性的空间位置，答案需输出坐标）。问答对通过已构建的 GIQA‑DES 描述与 Llama3 自动生成（Figure 3b），问题模板包括退化类型、区域属性等多种类别，答案则可包含坐标（grounding 场景）或仅为质量文本（referring 场景）。GIQA‑160K 最终汇集了 167 657 条指令微调样本，覆盖 42 960 幅图像，并额外构建了包含 100 幅图像的人工标注测试基准 GIQA‑Bench 用于标准化评估（Table 1 统计）。

微调阶段采用**多任务指令训练**，将 GIQA‑DES 和 GIQA‑VQA 的样本混合，在统一的目标下微调 MLLM。训练使用交叉熵损失，优化器为 AdamW（$\beta_1=0.9, \beta_2=0.999$），学习率 $2\times10^{-5}$，cosine 衰减，batch size 64，共 2 个 epoch。消融实验（Table 3）明确显示，仅用单一子任务数据（如 Only‑DES 或 Only‑VQA）训练会导致另一子任务性能大幅下降（例如 Only‑VQA 的 DES LLM‑Score 仅 38.50），而多任务联合训练（GIQA‑160K）则能同时提升描述与问答能力。进一步，该数据集对多种 MLLM 基座（LLaVA‑1.5‑7B/13B、LLaVA‑1.6‑7B、mPLUG‑Owl2‑7B）均表现出良好的通用性（Table 4），表明所提数据与训练框架不依赖于特定模型架构。

综上，Grounding‑IQA 的整体框架由**数据自动标注**与**多任务联合微调**两大模块紧密衔接：前者解决了细粒度位置标注难以获取的瓶颈，通过离散坐标设计和两级框优化在精度与可学习性之间取得平衡；后者则使通用 MLLM 在不改变原始结构的前提下获得 grounding‑IQA 能力，从而在质量描述、问答准确率和定位精度等维度均大幅超越传统 IQA 和 grounding 基线。该流水线的主要局限在于标注质量受限于外部模型性能，且离散网格表示牺牲了亚网格精度，对极小目标或高精度定位场景可能存在不足；更大规模模型的泛化性亦有待进一步验证。



**关键模块**  
Grounding‑IQA 的核心能力来自一套自动标注流水线，用于从已有的图像质量描述中构建包含空间坐标的训练数据。流水线分为四个阶段：

1. **对象标签提取（Stage‑1）**  
   利用 Llama3 从 Q‑Instruct 生成的质量描述中抽取出关键对象、对象的质量标签（如“blurry”“noisy”）以及对应的效果类别。提取结果形成 `<object, tag, effect>` 三元组，为后续定位提供语义锚点。

2. **边界框检测（Stage‑2）**  
   使用 Grounding DINO 对每个对象在图像中进行检测。为提高检测的准确性，输入并非仅使用对象名称，而是将描述中的上下文短语（如“the man wearing a white t‑shirt”）作为文本提示，从而获得更精确的候选框。

3. **边界框精炼（Stage‑3）**  
   该阶段包含两个子步骤：  
   - **IQA‑Filter**：通过调用一个预训练的多模态大模型（例如 Q‑Instruct）对每个候选框进行质量验证，只有当模型判断该框内确实存在所述的质量问题时，框才被保留。  
   - **Box‑Merge**：对过小面积（小于画幅 0.256%）或高度重叠（IoU > 95%）的框进行合并，消除冗余，使数据分布更接近人工标注（见 Figure 6）。实验表明，经精炼的 Ref‑Box 在 GIQA‑DES 任务上的 mIoU 从 0.5624 提升至 0.5851，Tag‑Recall 从 0.5045 提升至 0.5497（Table 2a）。

4. **坐标变换与融合（Stage‑4）**  
   将精炼后的边界框转换为一组离散网格索引，并嵌入原始质量描述文本中，形成带有坐标信息的完整答案。对应的输入问题则来自预定义的问题模板（例如 “Describe the image quality in detail and provide bounding box coordinates of the mentioned objects”）。最终生成 GIQA‑DES 样本。  
   对于 GIQA‑VQA，则利用 Llama3 从 GIQA‑DES 描述出发自动生成包含坐标的问答对，场景覆盖“指称”（问题中含框）和“定位”（答案中含框）两类。

在此基础上，**多任务指令微调**将 GIQA‑160K（包含 GIQA‑DES 与 GIQA‑VQA 的混合数据）用于同时训练模型的描述与问答能力，使得一个通用 MLLM 获得 grounding‑IQA 能力。

**关键公式推导**  
坐标离散化是将连续归一化坐标转化为少 token 序列的核心操作。Grounding‑IQA 使用 20 × 20 的网格划分图像，令 m = n = 20。  
给定一个归一化边界框，其左上角坐标 (x₁, y₁) 和右下角坐标 (x₂, y₂) 均在 [0, 1] 内，先将它们映射到网格单元索引（整数值）。映射规则为：

$$\mathrm{idx}_l = y_1 \cdot m \cdot n + x_1 \cdot n, \quad \mathrm{idx}_r = y_2 \cdot m \cdot n + x_2 \cdot n \tag{1}$$

其中 idx_l、idx_r 分别代表左上角和右下角所在的网格编号（0‑based）。该映射实质上是将二维网格线性展开为一维序列，使得每个角点仅用一个整数表示。  
为了评估或下游任务需要近似连续坐标时，通过两步从索引重建中心坐标：

$$x_1' = (\mathrm{idx}_l \bmod n + 0.5) / n, \quad y_1' = \left(\lfloor \mathrm{idx}_l / n \rfloor + 0.5\right) / m \tag{2}$$
$$x_2' = (\mathrm{idx}_r \bmod n + 0.5) / n, \quad y_2' = \left(\lfloor \mathrm{idx}_r / n \rfloor + 0.5\right) / m$$

这里 `/` 表示整数除法（向下取整），`%` 表示取模。公式 (2) 将网格索引重新解释为二维阵列中的行列号，并加上 0.5 偏移以落到网格中心，最后除以 m 或 n 恢复到归一化坐标。  
这种离散化表示（Disc‑Coord）仅需最多 9 个 token（每个角点用一个整数，加上特殊分隔符），而直接的归一化连续坐标则需要约 21 个 token；消融实验（Table 2b）表明，离散表示在文本质量（BLEU @4 23.67，LLM‑Score 61.75）和召回率（Tag‑Recall 0.5497）上均优于连续表示，尽管 mIoU 稍有损失（0.5851 vs. 0.6046），整体更利于多模态语言模型的训练。



## 实验与关键发现

### 主要结果：GIQA-Bench 上的整体性能

我们在 GIQA-Bench 上评估了 Grounding-IQA 方法（以 mPLUG-Owl2-7B 为基座，在 GIQA-160K 上多任务微调得到的 Grounding-GPT）。图 1 的雷达图与表 5 的定量结果一致表明，该方法在综合文本质量描述（GIQA-DES）和区域级视觉问答（GIQA-VQA）两类子任务内均取得了最优或次优性能。具体而言，在 GIQA-DES 上，LLM-Score 达到 63.00，相较未经过任何 grounding‑IQA 训练的 mPLUG-Owl2-7B 零样本基线提升 +14.75，较仅进行描述仿真的 Q‑Instruct 亦具明显优势；在 GIQA-VQA 上，总体准确率 Acc(Total) 达到 0.7417，较仅使用 GIQA-DES 数据微调的同类模型提升约 0.15。传统 grounding 模型（如 Shikra‑7B）虽具备坐标输出能力但缺乏质量感知，其 GIQA-DES 指标显著落后；而专注退化定位的 Q‑Ground 无法完成指称类问答，导致 VQA 子任务性能受限。Grounding‑GPT 则首次在单一框架内有效结合了定位精度与质量理解能力。

![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparisons on GIQA-Bench. Our proposed grounding-GPT effectively combines grounding and IQA*

![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/016_Table_5.jpg]]
*Table 5: Quantitative results on GIQA-Bench. Best and second-best results are colored red and blue*

**注意**：GIQA‑Bench 规模仅包含 100 张人工标注图像（250 个高质量样本），覆盖的失真类型和场景有限，当前性能结论的统计稳健性需在更大基准上进一步检验。部分对比模型（如通用多模态模型）本身不具备坐标输出能力，在 mIoU 和 Tag‑Recall 上记为 N/A，直接比较时需考虑此能力差异。

### 消融实验

消融研究围绕三个关键因素展开：标注管线中的边界框优化、坐标离散化表示策略以及训练任务组合，分别对应表 2–4 与附录图 6 等。

![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/011_Table_2.jpg]]
*Table 2: Ablation study on box optimization (refinement and representation) in the automated annotation pipeline. We conduct experiments on the GIQA-DES task. (a) Box refinement*

**边界框细化（Box Refinement）**。在自动化标注流程中，经由 IQA‑Filter 与 Box‑Merge 处理得到的精炼框（Ref‑Box）相比原始检测框（Raw‑Box）在 GIQA‑DES 任务上带来的改善：mIoU 由 0.5624 提升至 0.5851，Tag‑Recall 由 0.5045 提升至 0.5497（表 2a）。同时，BLEU@4 和 LLM‑Score 亦同步提高，说明去除错误框和合并冗余框有效提升了训练信号的准确性，使微调模型能生成更可靠的质量描述和坐标定位。

**坐标表示方式**。我们将连续归一化坐标（Norm‑Coord，占用约 21 个 token）转化为 20×20 网格索引（Disc‑Coord，最多 9 个 token）。表 2b 显示，虽是离散化牺牲了部分精确定位能力（mIoU 由 0.6046 降至 0.5851），但在文本生成质量和召回率上反超：BLEU@4 达到 23.67（Norm‑Coord 为 21.19），LLM‑Score 61.75（vs. 59.00），Tag‑Recall 0.5497（vs. 0.5305）。这一结果验证了更简洁的离散表示有利于模型学习将坐标与语义相融合，尤其适合语言生成与粗定位并存的场景。

**多任务训练**。仅用 GIQA‑DES 数据微调（Only‑DES）会导致 GIQA‑VQA 能力大幅弱化（Acc 仅 0.3475），反之若仅训练 VQA，描述质量严重下降（Only‑VQA 的 LLM‑Score 仅 38.50，表 3）。而使用完整 GIQA‑160K 进行多任务联合微调，DES 和 VQA 的各项指标均达到最优，表明描述与问答两类知识在 grounding‑IQA 中相互促进。此外，GIQA‑160K 对 LLaVA‑1.5‑7B/13B、LLaVA‑1.6‑7B 等不同规模的多模态基座模型均有显著提升效果（表 4），证实了数据集的通用性。

![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/012_Table_3.jpg]]
*Table 3: (b) Box representation*

![[assets/figures/papers/iclr26_0016_yEpE0QPpf8_Grounding-IQA_Grounding_Multimodal_Language_Mode/figures/013_Table_3.jpg]]
*Table 3: Ablation study on multi-task training. The baseline is the pre-trained model, mPLUG-Owl2-7B, without fine-tuning*

### 失败模式与局限性

1. **标注噪声传导**。GIQA‑160K 的质量受限于 Llama3、Grounding DINO、Q‑Instruct 等外部模型的性能，在语义模糊或对象重叠的场景下，IQA‑Filter 可能保留错误框或被过滤掉正确框，导致训练信号偏差。  
2. **离散网格的精度瓶颈**。20×20 网格虽利于模型学习，但对小目标（宽度不足网格分辨率的 1/20）或细长结构可能产生不可忽略的定位偏移，进而影响细粒度质量判断的可靠性（如模糊边界的小型缺陷）。  
3. **基准覆盖不足**。GIQA‑Bench 仅 100 张图像，难以反映真实世界多样的失真分布与场景复杂性；当前实验结论的泛化性需要更大规模且来源多样的测试集验证。  
4. **模型规模限制**。目前仅在 7–13B 参数的 MLLM 上验证了 grounding‑IQA 范式的有效性，更大模型（如 50B 以上）是否可进一步突破上述瓶颈仍是开放问题。

### 重要图表结论小结

- **图 1（雷达图）**直观展示了 Grounding‑GPT 在 DES 和 VQA 各子指标上的全面领先，尤其在描述质量（LLM‑Score）和 VQA 准确率上建立大幅度优势。  
- **图 6（框面积分布）**表明经批注管线处理后的 Ref‑Box 分布与人工标注基准更为一致，佐证了 Box‑Merge 算法（面积阈值 0.256，重叠阈值 95%）对过小或冗余框的修正作用。  
- **图 7（定性对比）**通过实例说明，Grounding‑IQA 不仅能输出带坐标的质量描述（如指出“白 T 恤男子面部的模糊区域”），还能在问答中准确回应用户对局部区域的指称，而传统方法仅提供纯文本的粗略描述或无法处理坐标相关的查询。  
- **表 2–4** 定量阐释了上述消融现象，且所有差异均具备一致性方向，实验证据强度较高；但表格内的“最佳/次佳”标记（表 5）依赖于特定的指标组合，在单独关注某一指标时排名可能发生变化。



## 定位与知识库关联

**核心突破与现有工作的关系**
Grounding-IQA 的提出，是针对现有多模态大语言模型（MLLM）在图像质量评估（IQA）任务中的一个根本性缺失：现有方法（如 Q-Instruct、通用 MLLM 的零样本描述）能够生成高层次的自然语言质量描述，但缺乏精确的空间对应能力，难以指代和定位影响质量的局部区域。这一瓶颈使 IQA 无法从整体泛泛的评价下沉到细粒度的对象/区域级分析（evidence anchor: “real_bottleneck”）。Grounding‑IQA 通过将多模态指称（referring）和定位（grounding）机制显式注入 IQA，让模型在描述或问答中输出／利用边界框坐标，从而迫使模型学会将语言描述与低层视觉属性在空间上对准，这是该方法对 IQA 范式的一次“因果性”改造（causal knob）。

相比于几个关键基线，这种改造体现在：
- **通用 MLLM 基线（mPLUG‑Owl2‑7B、Shikra‑7B）**：它们要么完全不具备坐标输出能力（mPLUG‑Owl2 零样本），要么仅有一般性的指称对话能力（Shikra）但未针对 IQA 场景优化。Grounding‑IQA 通过 GIQA‑160K 数据集的多任务微调，将描述和问答任务格式从“纯文本”改为“文本＋离散坐标”（changed_slots: 训练任务格式、坐标表示），从而在 GIQA‑Bench 上的描述质量（LLM‑Score 从 48.25 提升至 63.00）和问答准确性（Acc 从约 0.59 提升到 0.7417）都取得显著增益（Table 2a, Table 3）。
- **专用 IQA/定位模型（Q-Instruct、Q-Ground）**：Q-Instruct 仅生成纯文本质量描述，不包含坐标；Q-Ground 虽能定位退化区域，却无指称能力。Grounding‑IQA 同时支持双向坐标交互（输入坐标以指定区域问质量、输出坐标以指出质量问题所在），将单一退化定位扩展为通用的、带坐标的多任务质量感知（Figure 2）。对比中，由于基线不具备同等的坐标输出能力，部分指标为 N/A，直接比较时需注意能力差距，但 Grounding‑IQA 在自身擅长的 grounding 指标（mIoU、Tag‑Recall）和语言生成质量上全面占优（Table 5）。
- **自动标注管线带来的数据增益**：Grounding‑IQA 不仅提出任务，还通过一个四阶段自动标注管线（对象标签提取→检测→IQA‑Filter/Box‑Merge 精细化→离散化融合）构建了 GIQA‑160K 数据集。这一数据集使多个 MLLM 基座（LLaVA‑1.5‑7B/13B、LLaVA‑1.6‑7B、mPLUG‑Owl2）在微调后均获得显著性能提升（Table 4），表明任务范式本身具有较好的基座泛用性，而非某种特定模型的技巧。

**适用边界与数据/方法依赖性**
Grounding‑IQA 的影响力受限于自动标注流程的可靠性和所选表示的精度：
- **上游模型质量决定数据天花板**：管线依赖 Llama3（对象抽取）、Q-Instruct（质量描述）、Grounding DINO（边界框检测）的输出。当这些外部模型在特定失真或歧义描述下出错时，GIQA‑160K 中的样本会带有噪声标签，最终框定位的准确性和语义一致性可能下降（IQA‑Filter 的过滤虽能缓解，但无法彻底消除）。在公平性注意点中已指出这种依赖性是当前方法的隐忧。
- **离散网格表示的精度折衷**：为了简化坐标学习，Grounding‑IQA 将连续归一化坐标映射为 20×20 的离散网格索引（Eq. 1, 2），使表示长度从约 21 个 token 降至最多 9 个。消融实验（Table 2b）表明，离散坐标在描述质量（BLEU@4, LLM‑Score）和 Tag‑Recall 上优于连续坐标，但 mIoU 从 0.6046 降至 0.5851。这意味着对于极小或细长目标，网格量化可能造成可察觉的定位模糊，在需要高精度空间诊断的应用中是一种局限。
- **基准规模与泛化性**：当前的核心评估集 GIQA‑Bench 仅包含 100 张图像，所覆盖的失真类型和内容场景有限。所有主要结论均建立在此小规模基准之上，统计稳健性不足，推广到真实世界多源失真图像时的性能尚待验证。
- **模型尺度的探索区间**：目前仅在 7B‑13B 规模的 MLLM 上进行实验。更大规模模型（如数十 B 或 100B+）是否仍能从 GIQA‑160K 中获益，或是否需要针对大模型设计不同的坐标表示策略，均未涉及。

**方法局限与开放问题**
论文本身明确指出的局限性（limitations）与实验中的公平性注意点，结合未解问题，可归纳为以下几条关键路径：
- **Bound‑框质量控制的鲁棒性**：IQA‑Filter 算法利用 MLLM 判断框是否符合质量描述，当描述本身具有歧义（如“模糊”、“不自然”）时，过滤决策的可靠性存疑。Box‑Merge 的面积和重叠阈值（0.256 / 95%）是否在不同数据域均适用，也需要进一步验证。
- **网格分辨率能否自适应**：20×20 的固定网格对重要小目标可能损失关键位置信息，是否可以引入多分辨率、可动态调整的网格编码，是一个直接性能提升途径。
- **从语言‑坐标交互到传统 IQA 指标**：Grounding‑IQA 目前的能力主要体现在语言生成和问答层面，其习得的空间‑质量对应是否能够蒸馏到传统的 score‑based IQA 模型，或用于检测合成图像的局部伪影，是拓展其影响力的开放方向。
- **交互性与可解释性的深化**：当前模型在 GIQA‑VQA 中指称区域由预定义问题提供，用户尚无法自由通过自然语言指定关心的局部范围。将 grounding 能力扩展为真实交互式的局部质量分析（例如：“请指出图像中过曝最严重的区域”），将使系统更加贴近实际应用需求。
- **数据集噪声的系统性分析**：自动标注流程中每一步引入的误差类型（假阳性框、漏检、语义标签错误）对最终微调效果的敏感性，目前只有粗粒度的消融（Raw vs Ref‑Box），缺乏对各类噪声的分解与控制实验，这使得优化方向不够清晰。

总体而言，Grounding‑IQA 构建了一个连接 IQA 与多模态定位的初始框架，但其可靠性严重受制于上游模型与离散表达的选择，而小样本基准和有限模型规模使之尚处在概念验证阶段。未来的工作需要系统性地解耦自动化管线中的误差源，探索动态坐标表示，并在更大、更多样的失真场景和模型尺度下验证方法的泛化能力，方能使 grounding 成为 IQA 中可信赖的组件。



## 原文 PDF

![[paperPDFs/ICLR_2026/Grounding_IQA_Grounding_Multimodal_Language_Model_for_Image_Quality_Assessment.pdf]]
