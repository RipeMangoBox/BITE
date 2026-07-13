---
title: "HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HandVQA_Diagnosing_and_Improving_Fine_Grained_Spatial_Reasoning_about_Hands_in_Vision_Language_Models.pdf
project_link: "https://kcsayem.github.io/handvqa/"
code_link: null
aliases:
- HPLFTP
- HandVQA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在包含超过160万个基于3D手部关节坐标的解剖学可视化问答（VQA）对的HandVQA基准上进行微调，VLMs可以习得可迁移的3D空间意识。
primary_logic: HandVQA不仅是一个诊断工具，更是一个稳健的训练资源；其生成的几何基础空间知识能够在零样本设定下显著提升下游任务（如手势识别和手-物交互识别）的性能。
claims:
- 基础模型在距离相关问题上表现远低于随机猜测（例如LLaVA和Qwen准确率低于33.3%），而在微调后距离精度提升至80-90%以上。
- 微调后，模型在零样本手势识别上绝对准确率提升10.33%，在手-物交互识别上提升2.63%。
- 在所有微调模型中，LLaVA Mistral 7B在InterHand2.6M上取得最佳综合表现（角度准确率74.35%，距离90.79%，相对位置97%以上）。
- InterHand2.6M (HandVQA angle sub-task) 上 Accuracy (%) = 74.35 (LLaVA fine-tuned)
---

# HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models

> [!tip] 核心洞察
> HandVQA不仅是一个诊断工具，更是一个稳健的训练资源；其生成的几何基础空间知识能够在零样本设定下显著提升下游任务（如手势识别和手-物交互识别）的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | HandVQA：诊断并提升视觉语言模型中手部细粒度空间推理 |
| 英文题名 | HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26362) · [Project](https://kcsayem.github.io/handvqa/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HandVQA pipeline and LoRA fine-tuning protocol |
| Dataset | InterHand2.6M, HaGRID gesture recognition, H2O hand-object interaction |

> [!tip] 效果简介
> - InterHand2.6M (HandVQA angle sub-task) 上，Accuracy (%) 74.35 (LLaVA fine-tuned) vs 40.08 (LLaVA base) (+34.27)。
> - InterHand2.6M (HandVQA distance sub-task) 上，Accuracy (%) 90.79 (LLaVA fine-tuned) vs 16.20 (LLaVA base) (+74.59)。
> - InterHand2.6M (HandVQA relative position X) 上，Accuracy (%) 97.14 (LLaVA fine-tuned) vs 49.72 (LLaVA base) (+47.42)。

## 概要

视觉语言模型（VLMs）在通用视觉理解上取得了显著进展，然而它们在精细空间推理方面存在根本性瓶颈——尤其是对手部关节姿态的几何理解。现有模型在面对角度、距离和相对位置等细粒度空间问题时，往往依赖表面的统计关联而非真实的3D几何关系，导致性能接近甚至低于随机猜测。例如，基础模型在距离相关问题上准确率可低至16.20%（LLaVA）和33.3%以下（LLaVA、Qwen），暴露了当前VLM空间意识的系统性缺陷。

**核心洞察**：这种空间推理能力的缺失并非不可弥补。通过在包含超过160万道基于3D手部关节坐标的解剖学可视化问答（VQA）对的HandVQA基准上进行微调，VLMs可以习得可迁移的3D空间意识。HandVQA不仅是一个诊断工具，更是一个稳健的训练资源——其生成的几何基础空间知识能够在零样本设定下显著提升下游任务的性能。

**方法定位**：HandVQA提出了一套确定性流水线，将归一化的3D手部关节坐标自动转换为自然语言问答对。该流水线包含三个关键模块：**F_pose**（姿态描述符提取）——计算连续的角度、距离和各轴相对位置，并离散化为类别标签；**F_text**（句子生成）——用确定性模板将关节名称与离散类别组合成自然语言描述；**F_mcq**（多选题构建）——将图像与选项配对，形成标准化的VQA样本。微调采用LoRA适配器（秩8，alpha 32，学习率1e-4），以极低的参数开销实现空间意识的注入。

**主要结果**：在InterHand2.6M基准上，微调后的LLaVA Mistral 7B在角度任务上达到74.35%（基础模型40.08%），距离任务上达到90.79%（基础模型16.20%），相对位置任务上超过97%。更重要的是，这种空间推理能力展现出显著的零样本迁移效果：在HaGRID手势识别上绝对准确率提升10.33%，在H2O手-物交互识别上提升2.63%，无需任何任务特定的微调。

**知识库定位**：HandVQA填补了VLM评估体系中精细3D空间推理的空白。不同于现有的通用VQA基准（如VQAv2、GQA）或手部姿态估计数据集（如FreiHAND、InterHand2.6M），HandVQA将3D几何真值转化为语言推理任务，架起了视觉感知与空间语言理解之间的桥梁。其方法论与**MPGD**（He et al., CVPR 2023）等基于图的手部建模工作形成互补——前者关注视觉编码的精度，而HandVQA关注的是VLM对空间关系的语义理解与推理能力。

手部是人类与世界交互的核心媒介，理解手部姿态所蕴含的精细空间关系——关节的弯曲角度、指尖之间的距离、手指间的相对位置——对于手势识别、手-物交互理解、抓取规划等下游任务至关重要。然而，当前主流的视觉语言模型（VLMs）在这类细粒度空间推理上表现出系统性的缺陷。

一个关键瓶颈在于：现有VLMs的预训练数据以自然图像和通用图文对为主，缺乏对手部三维几何结构的显式建模。模型往往依赖表面的视觉统计模式进行“猜测”，而非基于真实的几何关系进行推理。这种缺陷在距离相关的判断上尤为突出：基础模型在距离问题上的准确率甚至显著低于随机猜测水平（例如LLaVA和Qwen的准确率低于33.3%，而随机基线为33.3%），暴露了模型对空间度量近乎盲目的状态。

更深层的问题在于，手部关节的空间关系是多维且连续的——一个关节的弯曲程度可以是“伸直”、“微曲”或“大幅弯曲”，两根手指的相对位置涉及X、Y、Z三个轴向的判别。这些精细的几何属性在通用VLM的训练范式中几乎不被触及，导致模型在面对手部图像时频繁表现出强烈的预测偏差，例如不加区分地将所有关节角度预测为“略微向内弯曲”。

现有的手部理解工作大多集中在纯视觉模型（如HaMeR）的三维姿态估计上，而缺乏将三维几何知识注入到视觉语言模型的训练资源。这使得VLMs在需要结合视觉感知和语言推理的手部场景中，始终存在一个从“看到”到“理解”的鸿沟。

本文的动机正是弥合这一鸿沟：通过构建一个大规模、可控的诊断基准，系统评估并提升VLMs对手部三维空间关系的理解能力。该基准将手部姿态估计分解为角度、距离和三个轴向的相对位置共五个子任务，使模型能够习得可迁移的三维空间意识，并在无需任务特定训练的情况下泛化到下游应用。

## 核心方法与创新机理

### 瓶颈诊断：从“看见手”到“理解手”的鸿沟

当前视觉语言模型（VLMs）在通用视觉理解上取得了显著进展，但HandVQA揭示了一个关键瓶颈：**这些模型缺乏对精细空间关系的几何理解，尤其在手部关节姿态的细粒度推理上，常依赖表面统计而非真实几何**。基础模型在距离相关问题上表现远低于随机猜测——例如LLaVA和Qwen在距离子任务上的准确率低于33.3%（Table 2），而相对位置X轴的左右判断也接近随机水平（Figure 11）。混淆矩阵进一步显示，基础模型存在强烈的预测偏差，倾向于将所有角度预测为“bent slightly inward”（Figure 8），所有距离预测为“close to”（Figure 10），这表明它们并未真正理解三维空间中的几何关系。

### 核心创新：从诊断到训练的三阶段确定性管线

HandVQA的核心创新在于**将诊断工具与训练资源统一**，通过一个完全确定性的三阶段管线，将归一化后的3D手部关节坐标自动转化为大规模、解剖学基础的视觉问答对（Figure 3）：

**Changed Slot 1：训练数据集——从通用视觉-语言预训练数据到160万+几何基础VQA对**

与依赖通用预训练数据的基线不同，HandVQA构建了超过160万个受控多选题，覆盖角度、距离和相对位置（X/Y/Z轴）五类子任务。管线从归一化的21个手部三维关节坐标 $P = \overline{\{ \mathbf{p}_i \in \mathbb{R}^3 \}}_{i=1}^{21}$ 出发，经过三个确定性阶段：

1. **$\mathcal{F}_{\text{pose}}$（姿态描述符提取）**：计算连续姿态描述符集合 $\Psi$，包括关节弯曲角度 $\theta_j$（通过相邻关节向量夹角计算）、关节点对距离 $d_{(i,k)}$ 以及各轴相对位置 $\Delta_a(i,k)$，随后通过固定阈值规则将其离散化为类别标签 $\Gamma$（Table 1）。
2. **$\mathcal{F}_{\text{text}}$（句子生成）**：用确定性模板将关节名称与离散类别标签填充为自然语言描述句，并过滤正误选项。
3. **$\mathcal{F}_{\text{mcq}}$（多选题构建）**：将图像与候选选项配对，每张图像每类描述符采样5个实例，生成最终的多选题提示。

**Changed Slot 2：微调方法——从零微调到LoRA适配器注入**

基线模型未经过任何微调，而HandVQA采用LoRA适配器（rank 8, alpha 32, 目标所有线性层, 学习率1e-4）进行高效微调。这一设计使得模型能够在不改变原始架构的前提下，习得可迁移的3D空间意识。

### 因果机制：几何知识习得与零样本迁移

HandVQA的核心因果链条在于：**通过在几何基础的空间推理任务上微调，VLMs习得了显式的3D手部几何理解，而非表面的视觉模式匹配**。这一习得的空间意识具有显著的迁移能力——在HandVQA上微调后的模型在零样本设定下，手势识别绝对准确率提升10.33%，手-物交互识别提升2.63%（Table 4）。消融实验进一步证实，在统一的HandVQA基准上微调的模型，其跨数据集泛化能力优于仅在单个数据集上微调的模型（Tables 7, 8），表明基准本身提供了鲁棒的几何知识基础。

### 与现有工作的本质差异

与纯视觉姿态估计方法（如**HaMeR**）不同，HandVQA不直接回归3D坐标，而是通过语言媒介让VLM理解空间关系；与现有VQA基准不同，HandVQA的问答对完全由3D几何确定性生成，避免了人工标注的歧义性和规模限制。这种“几何→语言”的映射机制，使得模型习得的是可解释、可迁移的空间推理能力，而非特定数据集的统计相关性。

HandVQA 的核心贡献在于构建了一条**确定性、可扩展的自动生成管线**，将归一化的 3D 手部关节坐标转化为解剖学上可解释的视觉问答对。该管线不依赖任何语言模型生成问题或答案，从而避免了幻觉和语义漂移，确保了基准的纯几何属性与可控性。

### 管线总览

整个管线由三个顺序执行的模块构成，如图 Figure 3 所示：

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the HandVQA pipeline. The pipeline converts normalized 3D hand joints into interpretable VQA pairs through three deterministic stages*

1. **F_pose：姿态描述符提取**  
   输入为归一化后的 21 个 3D 手部关节坐标 $P = \overline{\{ \mathbf{p}_i \in \mathbb{R}^3 \}}_{i=1}^{21}$。该模块计算三类连续姿态描述符的完整集合 $\Psi$：
   - **角度** $\theta_j$：测量指节 $j$ 处由其相邻关节形成的弯曲角度，定义为
     $$\theta _ { j } = \operatorname { a r c c o s } \frac { \left( \mathbf { p } _ { a \left( j \right) } - \mathbf { p } _ { j } \right) \cdot \left( \mathbf { p } _ { b \left( j \right) } - \mathbf { p } _ { j } \right) } { \left\| \mathbf { p } _ { a \left( j \right) } - \mathbf { p } _ { j } \right\| \left\| \mathbf { p } _ { b \left( j \right) } - \mathbf { p } _ { j } \right\| }$$
   - **距离** $d_{(i,k)}$：关节对之间的欧氏距离。
   - **相对位置** $\Delta_a(i,k)$：关节 $i$ 相对于关节 $k$ 在 $x, y, z$ 各轴上的坐标差。

   随后，每个连续描述符通过预定义的阈值规则被映射为离散类别标签，形成离散描述符集合 $\Gamma = \{ \gamma _ { n } | \psi _ { n } \in \Psi , n { = } 1 , 2 , { \ldots } , N \}$。例如，角度被分类为“bent slightly inward”“bent”“bent strongly inward”等，距离被分类为“close to”“spread from”“spread wide from”等。具体分类条件与阈值详见 Table 1。

2. **F_text：自然语言句子生成**  
   该模块使用确定性模板，将关节名称与离散类别标签填充为完整的自然语言描述句。例如，对于食指的 PIP 关节角度，生成“The proximal interphalangeal (PIP) joint of the index finger is bent slightly inward.”。同时，从同一描述符的其他可能类别中采样错误选项，形成候选答案池。

3. **F_mcq：多项选择题构建**  
   将手部图像与候选答案选项配对，指定正确标签 $y^\star$，构建标准 MCQ 提示，要求模型从选项中识别正确描述指定关节关系的句子。在过滤掉“对齐”情况之前，每张图像最多可生成 107 道 MCQ；最终通过每类描述符每张图像采样 5 道题的方式控制基准规模，总计超过 **160 万** 道受控多选题，覆盖角度、距离、相对位置 X/Y/Z 五个子任务（Figure 2）。

### 输入预处理：手部姿态归一化

为消除不同数据集在坐标系、尺度和手部朝向上的差异，管线在 F_pose 之前对所有 3D 关节坐标进行统一归一化。具体步骤为：以手部关节的质心为中心进行平移，并应用各向同性缩放。对于提供网格顶点信息的数据集（如 FreiHAND），缩放因子基于网格顶点范围计算：
$$s = \frac{1}{\max_a (v_a^{\max} - v_a^{\min})}$$
这一预处理保证了跨数据集的几何一致性，使得后续的离散分类阈值具有通用可比性。

### 下游迁移机制

HandVQA 管线的设计不仅服务于诊断，更构成了一个**空间感知训练资源**。如 Figure 1 所示，基础 VLM 在 HandVQA 上微调后，显式习得了 3D 手部几何和关节级空间推理能力。由此得到的空间感知 VLM 在无需任何任务特定训练的情况下，即可零样本泛化至手势识别和手-物交互识别等下游任务，实现一致的精度增益。这一迁移效应的因果机制在于：模型通过回答大量几何基础的 VQA 对，被迫学习从 RGB 图像中推断 3D 空间关系，而非依赖表面纹理统计。

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/001_Figure_1.jpg]]
*Figure 1: Overview of HandVQA’s transfer effect. Fine-tuning a base Vision-Language Model (VLM) on HandVQA teaches it explicit 3D hand geometry and joint-level spatial reasoning. The resulting Spatial-Aware VLM exhibits zero-shot generalization to novel downstream tasks: both image-based gesture recognition and video-based hand-object interaction recognition. Spatial-Aware VLM achieves consistent accuracy gains without task-specific training*

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/008_Figure_4.jpg]]
*Figure 4: The map of the hand skeleton used in our HandVQA benchmark generation pipeline*

### 3.1 手部姿态归一化

HandVQA 管线的输入是归一化后的 21 个手部三维关节坐标：

$$P = \overline{\{ \mathbf{p}_i \in \mathbb{R}^3 \}}_{i=1}^{21}$$

归一化过程通过计算手部关节的质心进行中心化，并采用各向同性缩放将手部映射到统一尺度空间。对于基于网格的数据集（如 FreiHAND），缩放因子基于网格顶点范围计算：

$$s = \frac{1}{\max_a (v_a^{\max} - v_a^{\min})}$$

其中 $v_a^{\max}$ 和 $v_a^{\min}$ 分别表示网格顶点在坐标轴 $a$ 上的最大和最小值。这一归一化步骤消除了绝对尺度和全局平移对后续几何推理的干扰，使不同来源的手部数据具有可比性。

### 3.2 姿态描述符提取（F_pose）

管线第一阶段 $\mathcal{F}_{\text{pose}}$ 从归一化关节点计算三类连续姿态描述符，并将其离散化为自然语言类别。所有连续描述符构成集合 $\Psi$：

$$\Psi = \Big \{ \theta _ { j } \left| j \in \mathcal { T } _ { \mathrm { a n g l e } } \right. \Big \} \cup \Big \{ d _ { ( i , k ) } \left| \left( i , k \right) \in \mathcal { T } _ { \mathrm { p a i r } } \right. \Big \} \cup \Big \{ \Delta _ { a } ( i , k ) \left| \left( i , k \right) \in \mathcal { T } _ { \mathrm { p a i r } } , a \in \{ x , y , z \} \right. \Big \}$$

**角度描述符**：测量指节 $j$ 处的弯曲程度，由其相邻关节形成的向量夹角定义：

$$\theta _ { j } = \operatorname { a r c c o s } \frac { \left( \mathbf { p } _ { a \left( j \right) } - \mathbf { p } _ { j } \right) \cdot \left( \mathbf { p } _ { b \left( j \right) } - \mathbf { p } _ { j } \right) } { \left\| \mathbf { p } _ { a \left( j \right) } - \mathbf { p } _ { j } \right\| \left\| \mathbf { p } _ { b \left( j \right) } - \mathbf { p } _ { j } \right\| }$$

其中 $\mathbf{p}_j$ 为目标关节坐标，$\mathbf{p}_{a(j)}$ 和 $\mathbf{p}_{b(j)}$ 为其相邻关节坐标。计算得到的连续角度值随后通过固定阈值映射为离散类别（如“bent slightly inward”“bent inward”“straight”等）。

**距离描述符**：计算指定关节对 $(i, k)$ 之间的欧氏距离 $d_{(i,k)}$，并按阈值分类为“close to”“spread from”“spread wide from”等语义标签。

**相对位置描述符**：对每对关节 $(i, k)$，分别计算沿 $x$、$y$、$z$ 轴的坐标差 $\Delta_a(i, k)$，映射为“at the left of / at the right of”“below / above”“in front of / behind”等空间关系类别。

连续描述符经分类器映射后得到离散标签集合：

$$\Gamma = \{ \gamma _ { n } | \psi _ { n } \in \Psi , n { = } 1 , 2 , { \ldots } , N \}$$

### 3.3 文本生成与多选题构建（F_text 和 F_mcq）

第二阶段 $\mathcal{F}_{\text{text}}$ 使用确定性模板将离散姿态标签填充为自然语言句子。模板结构固定，仅替换关节名称和类别标签，例如“The [joint A] is [category] relative to [joint B]”。每个描述符类型生成正确选项的同时，从其他类别中采样若干错误选项构成候选集。

第三阶段 $\mathcal{F}_{\text{mcq}}$ 将图像与候选选项组合为多选题提示，要求模型识别正确描述指定关节空间关系的句子。每张图像在每个描述符类型上采样 5 个实例，过滤掉因遮挡导致空间关系模糊的“aligned”情形后，最多可生成 107 个 MCQ。整个管线完全确定性，无需人工标注或语言模型参与生成，保证了问题质量的可控性和可复现性。

### 3.4 微调协议

下游微调采用 LoRA 适配器，秩 $r=8$，缩放因子 $\alpha=32$，作用于模型所有线性层，学习率设为 $1 \times 10^{-4}$。这一轻量级微调策略在保持基座模型通用能力的同时，有效注入了从 HandVQA 习得的 3D 空间几何知识。

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/002_Figure_2.jpg]]
*Figure 2: Overview of HandVQA Question Format. This figure illustrates the structure of our benchmark, which divides hand pose estimation into five sub-tasks: Angle, Distance, and Relative Position along X, Y, and Z axes. A hand image with annotated joint indices (top left) supports multiple-choice questions per task type, derived from 3D joint coordinates and the correct answers are shown in green*

## 实验与关键发现

### 基础模型的系统性空间推理缺陷

实验首先在 HandVQA 基准上评估了三种未经微调的基础视觉语言模型——**LLaVA Mistral 7B**、**DeepSeek Janus Pro 7B** 和 **Qwen 2.5 VL 7B Instruct**——对手部精细空间关系的理解能力。结果揭示了当前 VLM 在几何推理上的结构性盲区。

在角度子任务上，基础模型的表现普遍接近或略高于随机猜测水平（三选一，随机基线 33.3%）。LLaVA 在 InterHand2.6M 上仅取得 40.08% 的准确率（Table 2）。更严峻的是距离子任务：LLaVA 基线的准确率暴跌至 16.20%，DeepSeek 为 14.90%，Qwen 为 20.75%，三者均远低于随机猜测的 33.3% 基线（Table 2）。这意味着基础模型在判断手部关节点之间的距离关系时，不仅没有几何理解，反而被某种系统性偏差所误导。

相对位置子任务呈现出明显的不对称性。在 X 轴（左右）方向上，LLaVA 基础模型仅取得 49.72% 的准确率，接近随机水平（Table 3）；Y 轴（上下）和 Z 轴（前后）方向的表现虽稍好，但混淆矩阵（Figure 11–13）显示模型存在强烈的预测偏向——例如在 Z 轴上几乎所有基础模型都倾向于预测 "in front of"（Figure 13）。角度混淆矩阵（Figure 8）进一步证实了这一现象：三种基础模型几乎将所有样本预测为 "bent slightly inward"，无论真实标签是什么，表明模型依赖的是表层语言统计而非视觉几何。

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/018_Figure_11.jpg]]
*Figure 11: Relative Position X confusion matrix comparison between base and fine-tuned VLMs. The base models exhibit near-random predictions between “at the*

### 微调后的几何推理能力跃升

在 HandVQA 基准上使用 LoRA（rank 8, alpha 32, 学习率 1e-4）对三种 VLM 进行微调后，所有空间推理指标均出现大幅度提升，验证了 HandVQA 作为训练资源的有效性。

**LLaVA Mistral 7B** 在 InterHand2.6M 上取得最佳综合表现：角度准确率从 40.08% 跃升至 74.35%（+34.27 个百分点），距离准确率从 16.20% 飙升至 90.79%（+74.59 个百分点）（Table 2）。相对位置子任务中，X 轴准确率达到 97.14%，Y 轴 96.09%，Z 轴 97.77%，均接近饱和（Table 3）。**DeepSeek Janus Pro 7B** 和 **Qwen 2.5 VL 7B** 同样展现出显著增益，例如 DeepSeek 在 InterHand2.6M 上的角度准确率从 34.10% 提升至 68.00%，距离准确率从 14.90% 提升至 88.02%（Table 2）。

混淆矩阵的对比直观展示了微调的效果。角度混淆矩阵（Figure 9）显示，微调后模型的对角线对齐显著增强，"bent slightly inward" 的主导偏差被有效抑制。距离混淆矩阵（Figure 10）中，"close to" 的预测偏差大幅减少，但 "spread from" 与 "spread wide from" 之间仍存在一定混淆，提示离散类别边界可能不足以完全捕捉感知上的连续过渡。相对位置 X 轴（Figure 11）的左右判别能力从接近随机提升至近乎完美。

![[assets/figures/papers/paper_list_l2395_https_arxiv_org_abs_2603_26362/figures/016_Figure_10.jpg]]
*Figure 10: Distance confusion matrix comparison between base and fine-tuned VLMs. The base models exhibit a strong bias toward predicting “close to” across multiple ground-truth categories, leading to a skewed prediction distribution. In contrast, fine-tuning produces a more balanced distribution with increased alignment along the diagonal, indicating improved discrimination between distance categories. However, residual confusion persists between “spread from” and “spread wide from”, suggesting continued difficulty in distinguishing fine-grained spatial separations*

值得注意的是，尽管距离和相对位置任务在微调后达到了 90% 以上的准确率，角度任务的最佳准确率仍停留在 74.35%。这一瓶颈暗示视觉编码器在提取精细关节角度信息方面存在根本性限制，可能受限于图像分辨率、遮挡或 3D 到 2D 投影的信息损失。

### 零样本迁移：从空间推理到语义理解

HandVQA 微调所习得的 3D 空间意识能够零样本迁移至完全不同的下游任务，无需任何任务特定的训练。在 **HaGRID** 手势识别任务上，LLaVA 微调模型取得 69.58% 的准确率，相较于基础模型的 57.42% 提升了 12.16 个百分点（Table 4）。在 **H2O** 手-物交互识别任务上，Qwen 微调模型取得 82.89% 的准确率，相较于基础模型的 80.26% 提升了 2.63 个百分点（Table 4）。这一迁移效应表明，HandVQA 注入的并非简单的模式匹配，而是可泛化的 3D 几何理解——模型学会了从手部关节的空间配置中推断手势语义和交互类型。

### 统一基准微调与跨数据集泛化

消融实验比较了在单个数据集上微调与在统一 HandVQA 基准（合并 FreiHAND、InterHand2.6M、FPHA）上微调的效果差异。结果表明，统一基准微调在跨数据集评估中始终优于单数据集微调（Tables 7, 8），验证了多样化手部姿态数据对空间推理泛化的重要性。

跨数据集迁移实验进一步揭示了泛化的边界。在 FreiHAND 上微调的模型迁移至 InterHand2.6M 时，DeepSeek 的角度准确率从 34.10% 提升至 56.15%，LLaVA 从 40.08% 提升至 56.81%（Table 9），显示出一定的跨数据集泛化能力。然而，在以自我为中心视角采集的 FPHA 数据集上，增益并不一致，提示视角差异可能是影响迁移效果的关键因素。

### 失败模式与校准问题

微调后的模型在置信度校准方面存在系统性欠置信问题——模型倾向于给出低于实际准确率的置信度估计。这一现象需要在部署时予以关注，尤其是在需要可靠不确定性估计的安全关键应用中。此外，角度任务的剩余混淆（最佳仅 74.35%）和距离任务中 "spread from" 与 "spread wide from" 的持续混淆，指向了固定阈值离散化方法的固有局限：连续姿态空间的硬边界划分可能无法与人类感知的类别边界对齐。

## 定位与知识库关联

### 1. 方法定位与核心贡献

HandVQA 并非提出一种新的视觉语言模型架构，而是一种**诊断工具与训练资源**的双重设计。其核心贡献在于：

- **诊断维度**：首次系统性地揭示当前主流视觉语言模型（VLMs）在手部细粒度空间推理上的根本性缺陷——基础模型在距离相关问题上表现远低于随机猜测（LLaVA 和 Qwen 准确率低于 33.3%），在角度推理上同样挣扎（约 40%）。
- **训练维度**：通过一个包含超过 160 万道基于 3D 手部关节坐标的解剖学可视化问答对（VQA）的基准，配合 LoRA 微调协议，使 VLMs 习得可迁移的 3D 空间意识。

这一双重定位使 HandVQA 区别于纯粹的基准工作（仅评测）或单纯的训练数据工作（仅增强），而是在诊断瓶颈的同时提供因果性解决方案。

### 2. 与基线方法的对比关系

论文选取了三类代表性的 7B 级 VLMs 作为基线评测对象：

| 基线模型 | 架构特点 | 在 HandVQA 上的关键表现 |
|----------|----------|--------------------------|
| **LLaVA Mistral 7B** | 通用视觉语言对话模型 | 微调后角度准确率 74.35%，距离 90.79%，综合最优 |
| **Qwen 2.5 VL 7B Instruct** | 指令微调视觉语言模型 | 微调后在 H2O 手-物交互零样本任务上最优（82.89%） |
| **DeepSeek Janus Pro 7B** | 统一多模态理解与生成 | 微调后角度准确率 68.00%，距离 88.02% |

此外，论文还将纯视觉模型 **HaMeR** 作为对比参照，以区分视觉编码器能力与语言推理能力的贡献边界。

**关键发现**：所有基础 VLM 在未微调时，空间推理能力均接近或低于随机猜测水平，这表明当前的视觉语言预训练数据普遍缺乏对精细空间关系的几何理解，模型倾向于依赖表面统计模式而非真实的 3D 几何。

### 3. 方法谱系中的位置

HandVQA 处于以下几个研究脉络的交汇点：

- **空间推理基准**：继承自 VQA 基准（如 GQA、CLEVR）对组合空间推理的评测传统，但将焦点缩小到单一对象类别（人手）的关节级细粒度几何理解，填补了现有基准在解剖学空间推理上的空白。
- **3D 感知与视觉语言对齐**：与 3D-LLM、PointLLM 等将 3D 点云与语言对齐的工作形成互补——HandVQA 通过 2D 图像间接注入 3D 几何知识，避免了对 3D 编码器的依赖。
- **参数高效微调（PEFT）**：采用 LoRA（秩 8，alpha 32，覆盖所有线性层，学习率 1e-4）作为统一的微调协议，验证了通过轻量适配器即可将几何知识注入冻结的视觉语言骨干网络。

### 4. 适用边界与局限

论文明确承认以下局限性，需要在实际应用中审慎考量：

1. **固定阈值分类的感知盲区**：角度、距离和相对位置的离散化依赖预定义阈值（Table 1），可能无法捕捉连续姿态的细微感知差异，例如“稍微弯曲”与“弯曲”的界限在现实中是渐变的。

2. **角度任务的性能天花板**：即使在微调后，角度准确率仍低于 75%（LLaVA 最佳为 74.35%），远低于距离（90.79%）和相对位置（97%+）任务。这表明视觉编码器在处理精细关节角度方面存在根本性瓶颈，可能受限于图像分辨率或特征提取的粒度。

3. **静态单帧限制**：基准仅涵盖静态图像，未涉及视频中的运动线索和接触动态，无法评估模型对时序手部动作的理解能力。

4. **不确定性校准不足**：微调后的模型表现出系统性低估置信度（欠校准），在需要可靠置信度估计的下游任务中存在风险。

5. **跨数据集泛化的不一致性**：消融实验显示，跨数据集微调的增益并不均匀——例如在 FreiHAND 上微调的模型在 InterHand2.6M 上角度准确率有显著提升（DeepSeek 从 34.10 到 56.15，LLaVA 从 40.08 到 56.81），但在以自我为中心的数据集 FPHA 上增益不一致（Table 9），提示领域偏移（第三人称 vs. 第一人称视角）仍是泛化的障碍。

### 5. 开放问题

基于论文的分析和局限声明，以下开放问题值得后续研究关注：

1. **自适应离散化策略**：如何开发自适应或学习的映射函数以替代固定阈值，从而更好地捕捉感知差异并支持更丰富的几何推理？

2. **视频扩展与动态推理**：如何将 HandVQA 范式扩展到视频领域，以支持对运动线索、接触动态和动作序列的推理？

3. **视觉-语言-动作（VLA）集成**：如何将 HandVQA 习得的空间意识与 VLA 模型集成，以改进机器人抓取规划和灵巧控制等具身智能任务？

4. **不确定性校准**：如何实现微调模型中良好校准的不确定性估计，以解决当前观察到的欠置信问题？

5. **角度推理的突破**：是否存在更具表现力的提示方式、训练策略或视觉编码器改进方案，以根本克服剩余的角度混淆？

6. **领域自适应**：如何弥合第三人称与第一人称视角之间的领域鸿沟，实现更稳健的跨数据集泛化？

## 原文 PDF

![[paperPDFs/CVPR_2026/HandVQA_Diagnosing_and_Improving_Fine_Grained_Spatial_Reasoning_about_Hands_in_Vision_Language_Models.pdf]]
