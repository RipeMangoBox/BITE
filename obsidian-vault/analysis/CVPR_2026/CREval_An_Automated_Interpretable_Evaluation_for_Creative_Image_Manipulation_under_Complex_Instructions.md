---
title: "CREval: An Automated Interpretable Evaluation for Creative Image Manipulation under Complex Instructions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CREval_An_Automated_Interpretable_Evaluation_for_Creative_Image_Manipulation_under_Complex_Instructions.pdf
project_link: null
code_link: "https://github.com/ChonghuinanWang/CREval"
aliases:
- CREval
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入基于VQA的细粒度评估，将整体质量分解为指令遵循（IF）、视觉一致性（VC）和视觉质量（VQ）三个维度的针对性问答对，通过匹配参考答案进行客观评分，从而实现透明、可解释的自动评估。
primary_logic: 利用MLLM生成结构化的'是/否'问题，将主观质量评估转化为一系列可独立验证的二值判断，避免了直接打分带来的黑箱和不一致性，显著提升了评估的全面性和与人类偏好的一致性。
claims:
- 提出全自动的问答式评估管道，通过MLLM回答结构化问题而非直接打分来获得分数。
- 评估分解为指令遵循（IF）、视觉一致性（VC）和视觉质量（VQ）三个互补维度，各维度生成≥15个针对性问题以确保全面性。
- 用户研究证实CREval自动指标与人类偏好高度一致，例如Seedream 4.0在CREvalScore_GPT4o（84.31）和HumanScore（72.01）上均排名第一。
- "CREval-Bench 上 Overall Average Score = Seedream 4.0: 83.43"
---

# CREval: An Automated Interpretable Evaluation for Creative Image Manipulation under Complex Instructions

> [!tip] 核心洞察
> 利用MLLM生成结构化的'是/否'问题，将主观质量评估转化为一系列可独立验证的二值判断，避免了直接打分带来的黑箱和不一致性，显著提升了评估的全面性和与人类偏好的一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CREval：面向复杂指令的创意图像编辑自动化可解释评估 |
| 英文题名 | CREval: An Automated Interpretable Evaluation for Creative Image Manipulation under Complex Instructions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.26174) · [Code](https://github.com/ChonghuinanWang/CREval) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CREval |
| Dataset | CREval-Bench, Human Preference Validation |

> [!tip] 效果简介
> - CREval-Bench 上，Overall Average Score Seedream 4.0: 83.43 vs Qwen-Image-Edit (open best): 79.78 (+3.65)；Instruction Following (IF) Score Seedream 4.0: 89.12 vs GPT-Image-1: 88.34 (+0.78)；Visual Consistency (VC) Score Gemini 2.5 Flash Image: 74.79 (best VC) vs Seedream 4.0: 73.44 (+1.35)。
> - Human Preference Validation 上，CREvalScore (GPT-4o) alignment CREvalScore rankings align with HumanScore; Seedream 4.0 top both vs Aesthetic Score, VIEScore, EditScore baselines (N/A)。

## 概要

复杂创意图像编辑（如风格迁移、物体替换、场景合成）的自动评估长期受困于两个瓶颈：**评估覆盖不完整**与**评分过程不可解释**。传统方法依赖多模态大语言模型（MLLM）直接输出整体分数，这种黑箱式打分无法定位具体错误来源，也难以与人类对创意任务的多维度判断对齐。

针对这一瓶颈，本文提出 **CREval**——一个全自动、基于问答（QA）的可解释评估框架。其核心调控变量在于**将主观质量评估转化为一系列可独立验证的结构化二值判断**：不再让 MLLM 直接打分，而是让它回答针对指令遵循（Instruction Following, IF）、视觉一致性（Visual Consistency, VC）和视觉质量（Visual Quality, VQ）三个维度精心设计的“是/否”问题，通过匹配参考答案累计得分。这一设计使得每次扣分都有明确的理由追溯，从根本上解决了评估的黑箱问题。

在此基础上，作者构建了 **CREval-Bench** 基准，包含超过 800 对高质量图像与复杂创意编辑指令，覆盖 3 大类 9 个创意维度。实验表明，CREval 的自动评分与人类偏好高度一致——例如 **Seedream 4.0** 在 CREvalScore（GPT-4o 评估器）上以 84.31 分排名第一，与人类评分 HumanScore 的 72.01 分排名完全吻合，显著优于 Aesthetic Score、VIEScore、EditScore 等基线指标。综合得分公式为：

$$S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$$

其中 VQ 权重被有意压低至 0.2，因为实验发现 MLLM 对细粒度视觉伪影的敏感度有限，该维度的区分度较弱。尽管如此，框架的整体排名鲁棒性在更换评估器（如从 GPT-4o 切换为 Qwen3-VL）后依然保持稳定。

**方法定位**：CREval 属于基于 VQA 的可解释评估范式，与直接打分方法（MLLM holistic scoring）、美学评分（Aesthetic Score）、以及 VIEScore、EditScore 等自动指标形成互补或替代关系。其核心贡献不在于提出新的生成模型，而在于为创意图像编辑领域提供了一套透明、可追溯、与人类对齐的评估基础设施。

### 创意图像编辑的评估困境

近年来，基于扩散模型和自回归模型的可控图像生成与编辑技术快速发展，催生了大量面向复杂指令的创意图像编辑模型。然而，如何系统、可靠地评估这些模型的输出质量，始终是一个悬而未决的问题。

传统的图像编辑评估通常依赖人工评分或简单的参考指标（如PSNR、SSIM），这些方法要么成本高昂且难以复现，要么无法捕捉创意编辑中语义层面的质量差异。随着多模态大语言模型（MLLM）的兴起，研究者开始尝试利用GPT-4o等模型直接对编辑结果进行整体打分。但这种“黑箱”式评估存在三个根本性缺陷：

1. **覆盖不完整**：单一整体分数无法反映模型在不同编辑维度上的具体表现差异。
2. **评分不可解释**：MLLM直接输出的分数缺乏明确的扣分依据，用户无法理解模型在何处成功或失败。
3. **与人类偏好不一致**：直接打分容易受到MLLM自身偏见和评分尺度漂移的影响，导致自动评估结果与人类判断之间的一致性不足。

### 现有基准的局限性

已有的指令式图像编辑基准（如MagicBrush、EditBench等）虽然推动了领域发展，但其指令设计往往偏向简单、直接的编辑操作（如“将猫替换为狗”），缺乏对创意性、叙事性和语义复杂性的考量。这导致两个问题：一是无法充分考验模型处理复杂创意指令的能力；二是评估结果难以反映模型在真实应用场景中的表现。

### 本文动机

针对上述缺口，本文提出**CREval**——一个面向复杂创意指令的、全自动的、可解释的问答式评估框架。其核心动机在于：

- **将主观评估转化为客观验证**：通过将整体质量分解为一系列结构化的“是/否”问答对，使评估过程透明化，每个得分或失分都有明确的逻辑依据。
- **构建多维评估体系**：从指令遵循（Instruction Following, IF）、视觉一致性（Visual Consistency, VC）和视觉质量（Visual Quality, VQ）三个互补维度全面衡量编辑质量，避免单一指标的片面性。
- **建立高难度基准**：构建CREval-Bench，覆盖3大类9个创意维度、超过800对图像-指令对，为模型在复杂创意场景下的能力评估提供统一标尺。

## 核心方法与创新机理

CREval的核心创新在于将创意图像编辑的质量评估从“黑箱打分”转变为“结构化问答验证”的范式。具体而言，该方法通过以下关键设计实现了评估的透明化与细粒度化。

### 从整体评分到可解释的VQA验证

传统评估方法（如MLLM直接输出整体分数）存在评分过程不透明、无法定位具体错误的问题。CREval的根本性改变在于**评分方式**的范式转换：不再要求MLLM直接给出一个整体分数，而是提示MLLM回答一系列结构化的“是/否”问题，通过匹配参考答案累计得分。如原文所述，“we prompt MLLMs to respond to these structured queries... instead of directly asking MLLMs to assign scores”。这一设计使每个问答对的结果都能明确指示得分或失分的理由，从而实现了**可解释性**的根本提升——评分不再是黑箱，而是一系列可独立验证的二值判断的集合。

### 多维度分解评估

CREval将评估过程分解为三个互补的**评估维度**，取代了传统的单一整体分数：

- **指令遵循（Instruction Following, IF）**：评估编辑结果是否准确执行了指令中的语义要求；
- **视觉一致性（Visual Consistency, VC）**：评估编辑区域与未编辑区域之间的视觉和谐度；
- **视觉质量（Visual Quality, VQ）**：评估生成图像的整体视觉真实感和伪影程度。

每个维度生成至少5个针对性问题，每对图像-指令的总问题数不少于15个，确保了评估的全面性。最终得分通过加权平均公式计算：

$$S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$$

其中IF和VC各占40%的权重，VQ占20%。这一权重分配（4:4:2）通过人类偏好实验验证，在自动评估与人类判断之间取得了最佳一致性（见Figure S.2）。VQ权重被有意降低，原因是MLLM对细粒度视觉伪影的敏感度有限，这一诚实的设计选择避免了不可靠的VQ评估对整体得分的过度影响。

### 与基线方法的本质差异

CREval与现有自动评估指标的差异不仅体现在评分机制上，更体现在评估哲学的根本不同。**Aesthetic Score**仅关注图像的审美质量，无法衡量指令执行的准确性；**VIEScore**和**EditScore**虽引入了MLLM评估，但仍依赖于直接打分范式，缺乏对评分依据的显式说明。CREval通过VQA机制将评估过程“展开”为一系列可审计的判断步骤，使得评估结果不仅是一个数字，更是一份细粒度的错误分析报告。用户研究（Table 3）证实，CREvalScore_GPT4o与HumanScore的排名一致性显著优于Aesthetic Score、VIEScore和EditScore等基线指标，验证了这一设计的人类对齐优势。

### 评估器的鲁棒性设计

为减少评估偏见，CREval在问题生成阶段使用与评估器不同的MLLM（如Qwen2.5-VL-72B），而非直接使用GPT-4o同时生成问题和评分。消融实验（Table 3）表明，当评估器从GPT-4o替换为Qwen3-VL时，各模型的相对排名保持稳定，验证了评估框架对不同MLLM评估器的鲁棒性。这一“生成-评估分离”的设计是确保评估公平性的关键工程决策。

CREval 提出了一套全自动、基于问答（QA）的评估管道，用于系统衡量复杂创意指令下图像编辑模型的表现。其核心设计动机在于：传统 MLLM 直接打分的评估方式存在过程不透明、覆盖不完整、评分不可解释的瓶颈，而 CREval 通过将整体质量拆解为可独立验证的结构化二值判断，实现了透明且与人类偏好高度一致的自动评估。

### 三阶段流水线

CREval 的完整工作流由三个顺序衔接的阶段构成（图 4），各阶段职责分明，形成“基准构建→问题生成→评估打分”的闭环。

**阶段一：基准构建（Benchmark Construction）**  
首先人工筛选高质量源图像，随后利用 GPT-4o 进行少样本学习，在 3 个大类、9 个创意维度上生成维度一致的编辑指令，最终构建超过 800 对图像‑指令对，形成 CREval‑Bench 基准。该基准覆盖的创意类型分布均衡（图 3），保证了评估的全面性与一致性。

**阶段二：问题生成（Question Generation）**  
为降低评估偏见，该阶段使用与后续评估器不同的 MLLM（如 Qwen2.5‑VL‑72B），通过思维链（Chain‑of‑Thought, CoT）方法为每对图像‑指令生成三个维度的评估问答对。每个维度至少包含 5 个问题，每对总计不少于 15 个问题，确保细粒度覆盖。

**阶段三：评估（Evaluation）**  
采用 GPT‑4o 作为评估器，基于阶段二生成的问答对逐题评判编辑图像：模型输出答案与参考答案匹配则得分，否则失分。最终性能指标通过加权平均计算得出：

$$S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$$

其中 $S_{\mathrm{IF}}$、$S_{\mathrm{VC}}$、$S_{\mathrm{VQ}}$ 分别代表指令遵循（Instruction Following）、视觉一致性（Visual Consistency）和视觉质量（Visual Quality）三个维度的得分。权重分配（4:4:2）经人类偏好消融实验验证，在该配比下自动评估与人类判断的一致性最佳。

### 模块关系与输入输出流

三个模块之间呈严格的数据依赖关系：阶段一的输出（图像‑指令对）作为阶段二的输入，驱动问答对生成；阶段二输出的结构化问答对（含参考答案）则构成阶段三的评分依据。评估阶段以“源图像 + 编辑指令 + 编辑后图像”为输入，通过问答匹配输出各维度得分及加权总分。

### 关键设计决策与局限性

- **可解释性**：每个问答对的匹配结果明确指示得分/失分理由，使评分过程完全透明，避免了直接打分带来的黑箱问题。
- **评估偏见控制**：问题生成与评估使用不同 MLLM，从设计上减少了单一模型偏好。
- **VQ 指标权重降低**：由于 MLLM 对细粒度视觉伪影的敏感度有限，VQ 权重被降至 0.2，这在一定程度上弱化了对图像真实度的精细考察，属于当前框架的已知局限。
- **权重泛化性**：当前 4:4:2 的权重仅通过有限的人类偏好实验确定，推广至其他类型的编辑任务时可能需要重新校准，该点需人工验证。

> 注：框架中涉及的“Thinking”模块有效性分析（如 Bagel、Step1X‑Edit 的 think 版本在 IF 上反而低于原版）属于消融实验范畴，将在后续实验分析章节详述。

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/005_Figure_4.jpg]]
*Figure 4: Overview of CREval. (1) In stage 1, we manually select high-quality images. We then construct several editing instruction examples and utilize the GPT-4o model for few-shot learning across 9 predefined dimensions, generating dimension consistent editing instructions and producing image–instruction pairs. (2) In stage 2, we use these image–instruction pairs to construct evaluation tasks. To reduce bias, we use different MLLMs such as Qwen2.5-VL-72B, to generate evaluation questions for 3 metrics using the Chain-of-Thought (CoT) method. Each metric contains at least 5 questions, with a total of no fewer than 15 questions per pair, completing the construction of the CREval-Bench. (3)In Stage 3...*

CREval 的核心设计在于将传统 MLLM 直接打分的黑箱评估，转化为一套结构化的问答式评估管道。其整体流程（图4）可拆解为三个关键阶段，每个阶段承担不同的功能角色。

### 阶段一：基准构建

该阶段的目标是生成覆盖广泛创意场景的图像‑指令对。首先人工筛选高质量源图像，然后利用 **GPT‑4o** 通过少样本学习，在预定义的9个创意维度上生成维度一致的编辑指令，最终构建包含超过800对图像‑指令对的 **CREval‑Bench** 基准。9个创意维度被组织为3个大类，样本数量保持平衡，以确保评估的全面性和一致性（图3）。

### 阶段二：问题生成

此阶段是 CREval 可解释性的关键。对于每对图像‑指令，系统使用与评估器不同的 MLLM（如 **Qwen2.5‑VL‑72B**）通过思维链方法，为三个评估维度各生成至少5个“是/否”式问答对，每对总计不少于15个问题。这三个维度分别为：

- **指令遵循**：评估编辑结果是否准确执行了指令中的各项要求；
- **视觉一致性**：评估编辑区域与非编辑区域在光照、风格、透视等方面的协调程度；
- **视觉质量**：评估生成图像是否存在伪影、模糊、不自然的纹理等质量问题。

采用不同模型生成问题的设计，旨在减少评估阶段的模型偏见。

### 阶段三：评估与得分计算

在评估阶段，使用 **GPT‑4o** 作为评估器，对每张编辑图像逐一回答阶段二生成的结构化问题。每个问题的回答与预设参考答案进行匹配，正确回答累计得分。最终，三个维度的得分通过加权平均合成综合得分：

$$S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$$

其中，$S_{\mathrm{IF}}$、$S_{\mathrm{VC}}$、$S_{\mathrm{VQ}}$ 分别表示指令遵循、视觉一致性和视觉质量的得分。权重分配（4:4:2）通过人类偏好实验确定——消融实验表明，该比例下自动评估与人类偏好的一致性最佳（图 S.2）。视觉质量权重被降低至0.2，是因为 MLLM 对细粒度视觉伪影的敏感度有限，过高的 VQ 权重反而会削弱整体对齐性。

这种“问答匹配”而非“直接打分”的机制是 CREval 的核心创新：每个问答对的结果明确指示得分或失分的具体理由，使评估过程完全透明可追溯，从根本上解决了传统 MLLM 评分不可解释的瓶颈。

## 实验与关键发现

### 1. 实验设置与评估协议

CREval的评估流程严格遵循三阶段管道。在评估阶段，每个模型每次处理一个图像‑指令对并生成单张输出图像。所有开源模型在可复现的本地稳定环境中运行，闭源模型则通过官方API访问。最终得分由三个维度的加权平均给出，公式为：

$$S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$$

其中 $S_{\mathrm{IF}}$、$S_{\mathrm{VC}}$、$S_{\mathrm{VQ}}$ 分别代表指令遵循（Instruction Following）、视觉一致性（Visual Consistency）和视觉质量（Visual Quality）得分。权重分配（4:4:2）通过人类偏好实验确定，在该配置下自动评估与人类判断的一致性达到最优（Fig. S2, Section A）。

评估覆盖了11个主流模型，包括四个闭源模型（GPT-Image-1、Seedream 4.0、FLUX.1 Kontext pro、Gemini 2.5 Flash Image）和七个开源模型（OmniGen2、ICEdit、UniWorld-V1、Bagel、Step1X-Editv1p2-preview、FLUX.1 Kontext dev、Qwen-Image-Edit-2509）。主评估器为GPT-4o，消融实验中使用Qwen3-VL验证评估器的鲁棒性。

### 2. 主实验结果

#### 2.1 整体性能排名

Table 2展示了所有模型在CREval-Bench上的综合评估结果。**Seedream 4.0** 以83.43的总体平均分在所有模型中排名第一，领先开源最佳模型**Qwen-Image-Edit-2509**（79.78）3.65分。这一差距揭示了当前开源模型在处理复杂创意指令方面仍存在显著的性能瓶颈。

在闭源阵营中，GPT-Image-1（82.33）和Gemini 2.5 Flash Image（81.83）分列第二、三位，三者之间的差距较小，反映顶级闭源模型在创意编辑能力上的竞争已进入胶着状态。

#### 2.2 分维度性能分析

**指令遵循（IF）** 维度上，Seedream 4.0以89.12分位居榜首，GPT-Image-1（88.34）紧随其后，仅差0.78分。这表明两者在精确理解并执行复杂语义指令方面能力接近，均显著优于其他模型。

**视觉一致性（VC）** 维度呈现不同的竞争格局：**Gemini 2.5 Flash Image** 以74.79分夺得该维度第一，超越Seedream 4.0（73.44）1.35分。这说明Gemini在保持编辑区域与源图像非编辑区域的结构、纹理一致性方面具有独特优势。

**视觉质量（VQ）** 维度的区分度相对有限，这是该工作的一个已知局限——MLLM对细粒度视觉伪影的检测敏感度不足，导致VQ权重被下调至0.2。这一设计虽然提升了整体评估与人类偏好的一致性，但可能弱化了对生成图像真实度的精细考察。

#### 2.3 创意维度雷达图分析

Figure 5以雷达图形式展示了各模型在9个创意维度上的性能分布。闭源模型（顶行）在各维度上表现更为均衡，尤其Seedream 4.0在多数维度上保持领先；开源模型（底行）则呈现出明显的“偏科”现象，部分维度（如风格迁移）表现尚可，但在需要深度语义理解和复杂场景重构的维度上大幅落后。这种不均衡性恰恰印证了CREval-Bench设计的必要性——单一整体分数会掩盖模型在具体创意能力上的强弱分布。

### 3. 人类偏好验证

Table 3是验证CREval有效性的核心证据。研究选取了六个代表性模型（三个开源、三个闭源），对比了四种自动指标（Aesthetic Score、VIEScore、EditScore、CREvalScore）与人类评分（HumanScore）的一致性。

关键发现如下：
- **Seedream 4.0** 在HumanScore（72.01）和CREvalScore_GPT4o（84.31）上均排名第一，CREvalScore_Qwen3-VL（88.47）同样将其排在首位，表明CREval的排名与人类偏好高度一致。
- 相比之下，**Aesthetic Score** 和 **VIEScore** 给出的排名与HumanScore存在明显偏差，这些传统指标无法有效捕捉创意编辑任务中“指令是否被正确执行”这一核心维度。
- **EditScore** 作为同为编辑任务设计的指标，与人类偏好的一致性优于美学类指标，但仍不及CREval。这是因为CREval通过结构化问答对实现了对IF、VC、VQ三个维度的解耦评估，避免了黑箱打分的模糊性。

### 4. 消融研究

#### 4.1 评估器鲁棒性

使用Qwen3-VL替换GPT-4o作为评估器后，各模型的相对排名保持稳定（Table 3），Seedream 4.0依然位列第一。这一结果验证了CREval框架的评估器鲁棒性——评估质量不依赖于特定MLLM的选择，而是源于结构化问答对的设计本身。

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/008_Table_3.jpg]]
*Table 3: Human preference verification. Aesthetic Score, VIEScore, and EditScore serve as baselines to evaluate six representative models (three open-source and three closed-source). $CREvalScore_{Qwen3-VL}$ and $CREvalScore_{GPT4o}$ use Qwen3-VL and GPT-4o as evaluators. Bold denotes the highest score, and underlining indicates the second-highest score*

#### 4.2 “Thinking”模块的有效性

Table 2中一个值得注意的发现是：Bagel和Step1X-Edit的“think”版本在IF得分上反而低于其原始版本。这说明在创意编辑任务中，额外的推理模块（thinking module）并未带来预期的指令理解增益，甚至可能引入不必要的推理噪声。这一反直觉的结果提示：当前“思维链”增强策略在视觉编辑领域的有效性仍需审慎评估。

### 5. 基准对比

Table 1将CREval-Bench与现有编辑基准进行了系统对比。CREval-Bench的核心差异化优势在于：（1）采用VQA-based评分机制，实现了透明、可解释的评估；（2）覆盖3大类、9个创意维度，指令复杂度远超以往基准（如Figure 2所示）。Figure 3进一步展示了9个维度的样本分布，各维度样本量保持均衡，确保了评估的全面性和一致性。

### 6. 失败模式与讨论

尽管CREval在人类对齐性上表现优异，但实验揭示了若干值得关注的局限：

**MLLM的视觉质量感知瓶颈**：VQ指标区分度有限，根源在于当前MLLM对细微视觉伪影（如纹理模糊、边缘锯齿、色彩偏差）的感知能力不足。这迫使作者将VQ权重降至0.2，但这一妥协方案可能掩盖模型在图像真实度上的真实差距。如何提升MLLM对细粒度视觉缺陷的检测能力，是未来改进的关键方向。

**权重泛化性问题**：4:4:2的权重配置仅通过有限的人类偏好实验确定，其在不同编辑类型（如纯风格迁移 vs. 复杂场景合成）上的泛化性尚未验证。设计自适应权重分配策略——根据编辑指令的语义复杂度动态调整IF/VC/VQ权重——是一个值得探索的开放问题。

**基准构建的潜在偏差**：CREval-Bench的指令生成依赖GPT-4o的few-shot学习，这可能引入对GPT系列模型的隐性偏好。尽管通过多模型生成问题（Qwen2.5-VL-72B）和人工审核进行了部分缓解，但完全消除这一偏差仍需更大规模的跨模型指令生成验证。

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/001_Figure_1.jpg]]
*Figure 1: Evaluation of state-of-the-art image generation and editing models using CREval, with GPT-4o serving as the evaluator. Each edited image is evaluated across three metrics: Instruction Following (IF), Visual Consistency (VC), and Visual Quality (VQ). The results indicate that the complex and creative instructions in CREval-Bench pose substantial challenges for current image manipulation models*

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/002_Table_1.jpg]]
*Table 1: Comparison to other existing benchmark. Our benchmark provides a comprehensive evaluation of creative image manipulation by leveraging VQA-based scoring*

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/003_Figure_2.jpg]]
*Figure 2: Comparison with previous benchmark. The CREval-Bench dataset extends existing instruction-based editing benchmarks by incorporating more complex, creative, and semantically rich instructions. Such design facilitates a comprehensive evaluation of model performance in handling imaginative and complex instruction editing tasks. In (b), the edited image examples on the right correspond one-to-one with the image-instruction pairs on the left*

![[assets/figures/papers/paper_list_l816_https_arxiv_org_abs_2603_26174/figures/006_Figure_5.jpg]]
*Figure 5: Performance comparison across all creative dimensions under different metrics. Top row: closed-source models; bottom row: open-source models*

## 定位与知识库关联

### 与现有评估范式的对比定位

**CREval** 的核心贡献在于将创意图像编辑的自动化评估从“直接打分”范式迁移至“结构化问答”范式。传统评估方法，如直接使用 MLLM 输出整体分数（例如 GPT-4o holistic score）或基于美学评分的 **Aesthetic Score**，其评分过程不透明，无法定位具体错误来源，导致评估结果缺乏可解释性。**VIEScore** 和 **EditScore** 等基于 MLLM 的自动评估指标虽然尝试改进，但仍未系统性地解决覆盖完整性和评分可解释性问题。

CREval 通过以下关键设计实现了范式转变：

1. **评分方式**：将整体质量评估转化为一系列可独立验证的“是/否”二值判断。MLLM 不再直接输出分数，而是回答针对性的结构化问答对，根据匹配正确答案累计得分。这一设计使每个得分/失分点都有明确的理由支撑，实现了透明评分。

2. **评估维度**：将评估分解为指令遵循（IF）、视觉一致性（VC）和视觉质量（VQ）三个互补维度。每个维度生成至少 5 个针对性问题，每对图像-指令总计不少于 15 个问题，确保评估的全面性。

3. **可解释性**：每个问答对的结果明确指示得分或失分的具体原因，提供细粒度错误分析能力，克服了传统黑箱打分的局限。

4. **最终得分计算**：采用加权平均 $S = 0.4 \times S_{\mathrm{IF}} + 0.4 \times S_{\mathrm{VC}} + 0.2 \times S_{\mathrm{VQ}}$，其中 IF 和 VC 各占 40%，VQ 占 20%。

### 适用边界与局限

尽管 CREval 在人类偏好对齐上表现出色，其设计仍存在明确的适用边界和已知局限：

- **VQ 指标的区分度有限**：MLLM 对细粒度视觉伪影的检测敏感性不足，导致 VQ 指标在区分模型间的视觉质量差异时能力受限。这也是 VQ 权重被降低至 0.2 的直接原因，但该调整可能弱化了对生成图像真实度的考察。Figure S.1 展示了 VQ 失效案例，直观说明了这一局限。

- **权重系数的泛化性存疑**：当前 4:4:2 的权重分配仅通过有限的人类偏好实验确定（Fig. S2 展示了权重消融实验）。当评估任务从创意编辑扩展到其他类型（如实景修复、风格迁移）时，该权重配置可能需要重新校准。

- **基准构建的潜在偏差**：CREval-Bench 的指令生成依赖 GPT-4o 的 few-shot 学习，可能引入对 GPT 系列模型的偏好。虽然通过使用不同于评估器的 MLLM（如 Qwen2.5-VL-72B）生成问题来减少评估偏见，且人工审核部分缓解了指令偏差，但基准本身对特定模型家族的偏好仍需关注。

- **评估器鲁棒性的验证范围**：虽然使用 Qwen3-VL 替换 GPT-4o 后各模型相对排名保持稳定，验证了框架的鲁棒性，但该验证仅覆盖了两种评估器，更广泛的评估器泛化性尚待证实。

### 开放问题与未来方向

CREval 的提出为创意图像编辑评估开辟了新的路径，同时也揭示了若干待探索的开放问题：

1. **细粒度视觉伪影检测**：如何进一步提高 MLLM 对局部伪影、纹理失真、边缘不连续等细粒度视觉问题的检测能力，以增强 VQ 指标的有效性和区分度？

2. **自适应权重分配**：能否设计自适应权重策略，根据不同编辑类型（如属性编辑、场景合成、风格迁移）动态调整 IF、VC、VQ 的权重比例，而非固定使用 4:4:2？

3. **“视觉一致性”的定义边界**：在更开放、更主观的创意任务中（如超现实主义编辑），如何定义和量化“视觉一致性”？当前基于问答对的评估方式是否足以捕捉人类对一致性的主观感知？

4. **跨模态扩展**：CREval 的 VQA 评估框架是否可以扩展至视频编辑或其他模态（如 3D 场景编辑、音频-视觉联合编辑）？这需要重新设计问题生成策略和评估维度。

5. **“Thinking”模块的有效性悖论**：实验中发现 Bagel 和 Step1X-Edit 的 think 版本在 IF 得分上反而低于原版，说明额外的 thinking 模块在创意编辑任务中未带来增益。这一现象的内在原因及其对评估框架设计的启示值得深入研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/CREval_An_Automated_Interpretable_Evaluation_for_Creative_Image_Manipulation_under_Complex_Instructions.pdf]]
