---
title: "SO-Bench: A Structural Output Evaluation of Multimodal LLM"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SO_Bench_A_Structural_Output_Evaluation_of_Multimodal_LLM.pdf
code_link: "https://github.com/apple/ml-sobench"
aliases:
- SB
- SO-Bench
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 输入 JSON 模式的深度与复杂性、视觉内容的多样性以及训练数据的模式分布是决定模型结构化输出性能的核心因素。
primary_logic: SO-Bench 首次系统量化了 MLLM 在视觉输入下遵循自定义嵌套模式的结构化输出能力，揭示了所有模型的全匹配准确率均不超过 19% 的巨大提升空间；通过大规模多源训练数据的有监督微调和基于可验证奖励的强化学习，可显著缩小这一差距。
claims:
- 最强模型 Gemini-2.5-Pro 在 SO-Bench 上的 Full Match (Fuzzy) 仅 18.91%，所有模型均低于 20%。
- GPT-5 相比 GPT-4o 在模式验证准确率上提升超过 15 个百分点。
- SFT 和 RLVR 训练可将模式验证和字段匹配准确率分别提升最高约 20% 和 13%。
- 结构化输出能力与代理工具调用、视觉指令遵循和通用视觉知识基准呈强正相关。
---

# SO-Bench: A Structural Output Evaluation of Multimodal LLM

> [!tip] 核心洞察
> SO-Bench 首次系统量化了 MLLM 在视觉输入下遵循自定义嵌套模式的结构化输出能力，揭示了所有模型的全匹配准确率均不超过 19% 的巨大提升空间；通过大规模多源训练数据的有监督微调和基于可验证奖励的强化学习，可显著缩小这一差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | SO-Bench：多模态大语言模型的结构化输出评估 |
| 英文题名 | SO-Bench: A Structural Output Evaluation of Multimodal LLM |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21750) · [Code](https://github.com/apple/ml-sobench) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | SO-Bench（视觉结构化输出基准及其数据生成与评估框架） |
| Dataset | SO-Bench |

> [!tip] 效果简介
> - SO-Bench 上，Schema Validation Accuracy (最高) 98.70 (GPT-5-mini) vs 16.28 (Qwen3-VL 2B) (大幅领先)；Field Match (Fuzzy, 最高) 73.14 (Gemini-2.5-Pro) vs 39.53 (Qwen3-VL 2B) (+33.61)；Full Match (Fuzzy, 最高) 18.91 (Gemini-2.5-Pro) vs 6.36 (Qwen3-VL 2B) (+12.55)。
> - SO-Bench (训练后) 上，Schema Validation Accuracy (3B 基座) 85.8 (SFT 50K) / 72.0 (RLVR) vs 65.1 (未训练基线) (+20.7 / +6.9)；Field Match Fuzzy (3B 基座) 56.5 (SFT 114K) / 52.7 (RLVR) vs 45.6 (未训练基线) (+10.9 / +7.1)。

## 概述

多模态大语言模型（MLLM）在通用视觉理解上取得了显著进展，但在面向下游应用的结构化输出任务中仍面临根本性瓶颈。当给定一张图像和一个由应用程序预先定义的自定义 JSON 模式（Schema），模型需要同时完成两项要求：**（1）生成的输出必须严格符合该模式的语法约束；（2）输出的字段内容必须准确反映图像中的信息**。这一“视觉结构化输出”问题对模型的模式遵循能力与细粒度视觉信息提取能力提出了双重挑战。

当前的核心瓶颈在于：**复杂的嵌套 JSON 模式导致结构合规性难以保证，而对图像中密集、分散或模糊文本的信息提取和数值预测仍存在较大误差，使得全局完全匹配率极低**。SO-Bench 正是针对这一空白提出的首个系统性基准。

SO-Bench 的核心洞察是：**通过大规模多源训练数据的有监督微调（SFT）和基于可验证奖励的强化学习（RLVR），可以显著缩小结构化输出的性能差距**。实验表明，SFT 和 RLVR 可将模式验证准确率提升最高约 20%，字段匹配准确率提升最高约 13%。此外，结构化输出能力与代理工具调用、视觉指令遵循和通用视觉知识基准呈强正相关，说明该能力是模型综合智能的重要维度。

在方法定位上，SO-Bench 并非提出新的模型架构，而是构建了一套完整的数据生成与评估框架：基于 6.5K+ 多样化 JSON 模式和 1.8K 人工验证的图像-模式对，通过多模态嵌入检索、多图像模式生成、用户意图多样化、渐进式响应生成与 Critic 优化等多阶段流水线，自动生成了 114K 高质量训练样本。评估采用基于抽象语法树（AST）的递归比较策略，支持精确匹配、模糊匹配（归一化编辑距离/相对误差）和字段忽略三种粒度。

主要结果揭示了该领域的巨大提升空间：**最强模型 Gemini-2.5-Pro 在 SO-Bench 上的 Full Match (Fuzzy) 仅为 18.91%，所有模型均低于 20%**；GPT-5 相比 GPT-4o 在模式验证准确率上提升超过 15 个百分点，但字段级内容质量仍有显著差距。训练实验进一步证实，增加训练数据量可单调提升性能，且训练数据的 Schema 深度分布与评估领域对齐至关重要——仅在浅层级 UI 数据上训练的模型在深层 Schema 的图表领域表现极差。

## 背景与动机

### 多模态大模型的结构化输出需求

多模态大语言模型（MLLM）正被广泛部署于需要从视觉输入中提取结构化信息的实际应用中。典型场景包括：从菜单照片中提取菜品名称与价格并填充到预定义的 JSON 格式中、从 UI 截图中解析界面元素层级、从文档扫描件中抽取表单字段等。这些下游应用通常要求模型不仅理解图像内容，还必须严格遵循用户指定的**自定义 JSON 模式（schema）**，生成语法合规且语义准确的键值对结构。这一任务被称为**视觉结构化输出**（visual structured output）。

图 1 展示了一个典型示例：给定一张菜单图像、一个由下游应用（如 MenuReader）定义的 JSON 模式以及一条自然语言指令，模型需要提取菜品信息并按模式要求输出结构化的 JSON 对象。

然而，当前 MLLM 在这一任务上面临**双重瓶颈**。一方面，复杂嵌套 JSON 模式下的结构合规性难以保证——模型经常输出字段名错误、层级错位或缺少必填字段的 JSON。另一方面，对于图像中密集、分散或模糊的文本信息，模型在数值预测和字段值提取上仍存在较大误差。这导致**全局完全匹配率极低**，即使是最强模型也难以在所有字段上同时做到正确。

### 现有评估体系的缺口

现有的 MLLM 评估基准主要关注以下能力维度，但均未系统覆盖视觉结构化输出这一关键场景：

- **通用视觉理解**（如 MMMU、MathVista）：评估模型对图像内容的整体理解与推理，但不涉及结构化输出格式约束。
- **文本丰富图像理解**（如 OCRBenchV2、DocVQA）：关注光学字符识别和文档问答，但输出形式通常为自由文本或简单答案，不要求遵循复杂 JSON 模式。
- **指令遵循**（如 IFEval、LiveBench）：评估模型遵循自然语言指令的能力，但主要在纯文本领域，不涉及视觉输入与结构化模式的双重约束。
- **代理工具调用**（如 BFCL）：评估模型生成函数调用参数的能力，虽涉及 JSON 输出，但其模式通常较浅且不依赖于视觉输入。

换言之，**视觉感知 + 深层嵌套模式遵循**这一组合能力长期缺乏专门的基准和系统评估。这导致两个后果：其一，研究者无法准确了解当前 MLLM 在真实结构化输出场景中的真实水平；其二，缺乏有针对性的训练数据和优化目标来提升这一能力。

### 本文动机与核心贡献

为填补上述空白，本文提出 **SO-Bench**——首个系统评估多模态大语言模型视觉结构化输出能力的基准。SO-Bench 的核心设计理念是：**真实世界的结构化输出需求由下游应用定义，因此评估必须覆盖多样化、复杂嵌套的自定义 JSON 模式**，而非仅使用固定的输出模板。

SO-Bench 的主要贡献包括：

1. **大规模基准构建**：从超过 6.5K 个多样化 JSON 模式和 1.8K 个经过人工验证的图像-模式对中构建评估集，覆盖 UI、文档、图表和自然图像四类视觉场景。
2. **多阶段自动标注流水线**：设计了包含多模态嵌入检索、多图像模式生成、用户意图多样化、渐进式响应生成与 Critic 优化等阶段的自动数据生成流水线，确保标注质量和多样性。
3. **细粒度评估指标**：基于抽象语法树（AST）递归比较，定义了模式验证准确率、字段匹配准确率（FMA）和全结构匹配准确率（FSMA），并支持精确匹配、模糊匹配和字段忽略三种策略。
4. **训练方案验证**：构建了 114K 规模的训练集，验证了有监督微调（SFT）和基于可验证奖励的强化学习（RLVR）对提升结构化输出能力的有效性。

初步实验揭示了一个关键发现：即使是当前最强的前沿模型（如 Gemini-2.5-Pro），其**全结构模糊匹配准确率也仅为 18.91%**，所有模型均低于 20%。这表明视觉结构化输出能力存在巨大的提升空间，亟需研究社区的关注。

## 核心创新

### 问题形式化与评估框架的系统性定义

SO-Bench 首次将多模态大模型的结构化输出能力形式化为一个可量化评估的问题：给定输入图像 $I$、预定义的 JSON 模式 $S$ 和用户指令 $X$，模型需自回归地生成结构化输出 $Y \sim p(Y|I, X, S)$，该输出必须同时满足两个约束——（1）语法上严格符合 $S$ 的嵌套结构定义；（2）语义上准确反映 $I$ 中的视觉信息。这一形式化将以往分散的“视觉信息提取”和“指令遵循”统一到结构化输出的框架下，填补了该领域缺乏系统性基准的空白。

### 多阶段自动标注流水线：从模式生成到响应精炼

与依赖人工标注或简单模板的传统基准不同，SO-Bench 的核心工程创新在于设计了一条 **多阶段自动标注流水线**（Figure 2），在保证数据质量的同时实现了大规模、高多样性的样本生成。该流水线包含以下关键模块：

1. **多模态嵌入与模式检索**：利用 CLIP 模型分别编码图像 $I$ 和 JSON 模式 $S$，通过加权余弦相似度 $\mathrm{sim}(I, S) = w_1 \cdot \cos(E_I, E_S) + w_2 \cdot \cos(E_T, E_S)$ 从 6.5K 模式库中检索最佳匹配的模式，解决了“什么模式适合这张图”的自动配对问题。

2. **多图像模式生成**：通过计算图像间的跨模态相似度 $\sin(I_i, I_j)$ 进行聚类，将相似图像联合输入生成更具概括性和深层嵌套的统一模式，提升了模式的抽象层级和覆盖广度。

3. **用户意图多样化**：基于 60K 合成用户画像和随机采样的对话风格，生成丰富多样的自然语言指令，模拟真实应用场景中的需求变异性。

4. **渐进式响应生成与 Critic 优化**：结合 OCR 辅助信号、模式约束校验、LLM critic 模型反馈和人工审查，迭代生成并精炼结构化输出真值。这一“生成-校验-修正”闭环显著提升了标注质量。

### AST 基础的多粒度评估策略

SO-Bench 的评估体系超越了简单的字符串匹配，采用基于抽象语法树（AST）的递归字典比较（遵循 BFCL 框架），并针对不同数据类型定义了三层匹配策略：**精确匹配**（Exact）、**模糊匹配**（Fuzzy，对字符串采用归一化编辑距离、对数值采用相对误差容忍）和**字段忽略**（Ignore）。在此基础上，设计了两个互补的聚合指标：

- **字段匹配准确率（FMA）**：$$\mathrm{FMA} = \frac{\sum_{k=1}^{N} |\{ f \in \mathcal{F}(G^{(k)}) : \exists f' \in \mathcal{F}(O^{(k)}), \mathrm{Match}(f, f') \}|}{\sum_{k=1}^{N} |\mathcal{F}(G^{(k)})|}$$，衡量所有真值字段中被成功匹配的比例，反映字段级的信息提取能力。

- **全结构匹配准确率（FSMA）**：$$\mathrm{FSMA} = \frac{1}{N} \sum_{k=1}^{N} \mathbb{1}\left[ \forall f \in \mathcal{F}(G^{(k)}), \exists f' \in \mathcal{F}(O^{(k)}) : \mathrm{Match}(f, f') \right]$$，衡量所有真值字段均被正确匹配的样本比例，是评估全局结构化输出准确性的严格指标。

这种分层评估设计使 SO-Bench 能够同时诊断模型的“模式合规性”（结构层面）和“内容准确性”（语义层面），避免了单一指标掩盖的性能短板。

### 训练范式创新：SFT 与 RLVR 的对比验证

SO-Bench 不仅是一个评估基准，还通过构建大规模训练集（来自 HierText、AriaUI 和 COYO 的图像与模式库配对）探索了提升结构化输出能力的训练策略。在 **有监督微调（SFT）** 之外，论文提出了基于可验证奖励的强化学习（RLVR）方法，其奖励函数设计为：

$$R(O,G) = \begin{cases} -0.1 & \text{if } O \text{ is invalid JSON} \\ \alpha \cdot \mathrm{FMA}(O,G)^2 & \text{otherwise} \end{cases}$$

其中模式合规乘数 $\alpha = 1.0$（合法 JSON）或 $0.8$（轻微违规），通过平方项放大高匹配率输出的奖励差异。这一设计巧妙地将“结构合规”和“内容准确”两个目标统一到单一奖励信号中，无需人工偏好标注即可进行强化学习优化。

实验表明，SFT 在模式验证准确率上可带来最高约 20% 的绝对提升，RLVR 亦有约 7% 的增益；在字段匹配模糊准确率上，SFT 可提升约 11%，RLVR 提升约 7%。值得注意的是，仅使用 3B 参数基座模型经 SFT 训练后，其性能可媲美 10 倍参数量的未训练模型，揭示了**训练数据质量与规模对结构化输出能力的决定性作用**。

### 与现有工作的本质差异

相较于传统的 OCR 基准（仅关注文本识别）或指令遵循基准（仅关注格式合规），SO-Bench 的独特贡献在于将两者耦合到一个统一的视觉结构化输出框架中，并揭示了二者之间的深层张力：使用结构化输出 API 可提升模式合规率，但可能牺牲字段级内容质量（Table 3）；反之，指令遵循提示在强模型上效果更佳，但对弱模型收效甚微。这一发现为后续的模型设计与训练策略选择提供了关键指引。

## 整体框架

SO-Bench 的构建与评估围绕一个统一的形式化问题展开：给定输入图像 $I$、预定义的 JSON 模式 $S$ 和用户指令 $X$，多模态大模型需自回归地生成结构化输出 $Y$，使其同时满足对 $S$ 的语法合规性，并准确反映 $I$ 中的视觉信息。整个工作流可划分为两大核心阶段——**大规模数据生成流水线**与**多层次评估体系**，二者通过 CLIP 嵌入空间中的图像-模式关联紧密耦合。

### 数据生成流水线

数据生成采用多阶段、人机协同的自动化标注框架（Figure 2），各阶段以专有前沿模型（如 GPT-5 和 Gemini-2.5-Pro）作为生成器，并在阶段间引入领域专家审查。流水线包含五个关键模块：

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the multi-stage data generation pipeline for SO-Bench, including schema generation, user intent generation, and response generation stages. At each stage, we leverage proprietary frontier models (e.g., GPT-5 and Gemini-2.5-Pro) as generators with careful prompt design. Data from each stage is checked with human domain experts before passing to the next stage. Before the schema generation stage, input images and JSON schemas are embedded through a CLIP model for embedding search. Details of the pipeline is introduced in Section 3.3*

1. **多模态嵌入与模式检索**：利用 CLIP 模型将图像及其文本描述分别编码为视觉嵌入 $E_I$ 和文本嵌入 $E_T$，同时将 JSON 模式编码为 $E_S$。通过加权余弦相似度从 6.5K 模式库中检索最匹配的候选模式：
   $$\mathrm{sim}(I, S) = w_1 \cdot \cos(E_I, E_S) + w_2 \cdot \cos(E_T, E_S)$$
   这一机制确保了图像内容与模式语义的精确对齐，是整个流水线的入口模块。

2. **多图像模式生成**：对相似图像进行聚类，通过多图像联合输入生成更具概括性和深层嵌套的统一模式。图像间相似度采用跨模态余弦相似度的加权组合：
   $$\sin(I_i, I_j) = w_1 \cdot \cos(E_{I_i}, E_{I_j}) + w_2 \cdot \cos(E_{I_i}, E_{T_j}) + w_3 \cdot \cos(E_{T_i}, E_{I_j}) + w_4 \cdot \cos(E_{T_i}, E_{T_j})$$
   该模块显著提升了模式的复杂度和多样性，使基准覆盖从浅层 UI 结构到深度嵌套的图表描述。

3. **用户意图多样化**：合成 60K 多样化用户画像，并随机采样对话风格，生成丰富多变的自然语言指令，模拟真实应用场景中的需求差异。

4. **渐进式响应生成与 Critic 优化**：结合 OCR 辅助信号、模式约束校验、LLM critic 模型反馈和人工审查，迭代生成并精炼结构化输出。这一多信号融合机制是保证真值质量的关键。

5. **训练数据构建**：从 HierText、AriaUI 和 COYO 的训练集中采集图像，与模式库中的真实模式或合成模式配对，形成 114K 结构化图像-模式训练对，用于后续的有监督微调（SFT）和强化学习（RLVR）实验。

### 评估体系

评估采用基于抽象语法树（AST）的递归字典比较方法，遵循 BFCL（Patil et al., 2025）的评估范式。针对原始类型字段定义三种匹配策略：

- **精确匹配**：要求字段键与值完全一致。
- **模糊匹配**：对字符串采用归一化编辑距离，对数值采用相对误差阈值，容忍合理偏差。
- **忽略字段**：对标注为可忽略的字段不参与评估。

在此基础上定义两个核心指标：

- **字段匹配准确率（FMA）**：所有样本中成功匹配的真值字段数占总真值字段数的比例：
  $$\mathrm{FMA} = \frac{\sum_{k=1}^{N} |\{f \in \mathcal{F}(G^{(k)}) : \exists f' \in \mathcal{F}(O^{(k)}), \mathrm{Match}(f, f')\}|}{\sum_{k=1}^{N} |\mathcal{F}(G^{(k)})|}$$

- **全结构匹配准确率（FSMA）**：所有真值字段均被正确匹配的样本比例，是评估全局结构化输出能力的最严格指标：
  $$\mathrm{FSMA} = \frac{1}{N} \sum_{k=1}^{N} \mathbf{1}\left[\forall f \in \mathcal{F}(G^{(k)}), \exists f' \in \mathcal{F}(O^{(k)}) : \mathrm{Match}(f, f')\right]$$

### 训练优化模块

在基准评估之外，SO-Bench 还提供了训练优化管线。基于 3B 基座模型，采用两种训练策略：

- **SFT**：在 114K 训练对上执行标准的有监督微调。
- **RLVR**：采用基于可验证奖励的强化学习，奖励函数设计为：
  $$R(O,G) = \begin{cases} -0.1 & \text{if } O \text{ is invalid JSON} \\ \alpha \cdot \mathrm{FMA}(O,G)^2 & \text{otherwise} \end{cases}$$
  其中模式合规乘数 $\alpha$ 在输出符合模式时为 1.0，否则为 0.8，引导模型在维持结构合规性的同时提升字段匹配质量。

整个框架的模块间关系清晰：模式检索与生成为响应生成提供约束空间，评估体系为训练提供反馈信号，训练模块则通过 SFT 和 RLVR 闭合优化回路。

### 补充图表

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/001_Figure_1.jpg]]
*Figure 1: An example of visual structured output task. Given a customized JSON schema often specified by the downstream applications, e.g. MenuReader, a model is tasked to extract information from input image, following the schema definition and user instruction*

## 核心模块与公式推导

SO-Bench 的评估与训练框架围绕“视觉结构化输出”的形式化定义展开：给定输入图像 $I$、预定义 JSON 模式 $S$ 和用户指令 $X$，模型需自回归生成结构化输出 $Y$，使其同时满足对 $S$ 的语法合规性和对 $I$ 的语义忠实性。其概率形式为 $p(Y|I, X, S)$。

基于此定义，方法体系包含三个核心模块：**多模态嵌入与模式检索**、**多阶段数据生成流水线**，以及**AST 驱动的多策略评估**。训练部分则引入**有监督微调（SFT）** 与**可验证奖励强化学习（RLVR）**。

### 多模态嵌入与模式检索

为将图像与合适的 JSON 模式关联，框架利用预训练 CLIP 模型分别编码图像视觉特征 $E_I$、图像文本描述 $E_T$ 和模式文本 $E_S$。图像-模式相似度通过加权余弦相似度计算：

$$
\mathrm{sim}(I, S) = w_1 \cdot \cos(E_I, E_S) + w_2 \cdot \cos(E_T, E_S)
$$

其中 $w_1, w_2$ 为权重系数。该公式同时利用视觉和语义信号，从 6.5K 模式库中检索 top-k 最匹配的 JSON 模式，实现精确的图像-模式配对。

在多图像模式生成阶段，为聚类相似图像以合成更具概括性的深层嵌套模式，定义图像间相似度：

$$
\begin{aligned}
\sin(I_i, I_j) = &\; w_1 \cdot \cos(E_{I_i}, E_{I_j}) + w_2 \cdot \cos(E_{I_i}, E_{T_j}) \\
                + &\; w_3 \cdot \cos(E_{T_i}, E_{I_j}) + w_4 \cdot \cos(E_{T_i}, E_{T_j})
\end{aligned}
$$

该公式加权组合四种跨模态余弦相似度（图像-图像、图像-文本、文本-图像、文本-文本），以全面捕捉图像间的语义关联，支撑多图像联合模式生成。

### 多阶段数据生成流水线

数据生成遵循三阶段流水线（Figure 2）：
1. **模式生成**：基于检索到的模式库，结合多图像分组，利用前沿模型（如 GPT-5、Gemini-2.5-Pro）合成多样化且深层嵌套的 JSON 模式。
2. **用户意图多样化**：从 60K 用户画像中随机采样对话风格，生成丰富多样的自然语言指令。
3. **渐进式响应生成与 Critic 优化**：结合 OCR 辅助信号、模式约束校验、LLM critic 反馈和人工审查，迭代生成并精炼结构化输出真值。每阶段数据均经人类领域专家检查后方进入下一阶段。

### AST 驱动的多策略评估

评估采用基于抽象语法树（AST）的递归字典比较方法（遵循 BFCL 标准），对输出与真值进行结构化匹配。核心指标定义如下：

**字段匹配准确率（FMA）**：衡量所有样本中能够与输出字段匹配的真值字段比例。

$$
\mathrm{FMA} = \frac{\sum_{k=1}^{N} |\{ f \in \mathcal{F}(G^{(k)}) : \exists f' \in \mathcal{F}(O^{(k)}), \mathrm{Match}(f, f') \}|}{\sum_{k=1}^{N} |\mathcal{F}(G^{(k)})|}
$$

其中 $\mathcal{F}(\cdot)$ 表示 JSON 结构中的所有字段集合，$G^{(k)}$ 为第 $k$ 个样本的真值，$O^{(k)}$ 为对应输出，$\mathrm{Match}$ 为匹配函数。

**全结构匹配准确率（FSMA）**：所有真值字段均被正确匹配的样本比例，是评估全局结构化输出准确性的最严格指标。

$$
\mathrm{FSMA} = \frac{1}{N} \sum_{k=1}^{N} \mathbb{1}\left[ \forall f \in \mathcal{F}(G^{(k)}), \exists f' \in \mathcal{F}(O^{(k)}) : \mathrm{Match}(f, f') \right]
$$

对于原子类型字段，匹配策略支持三种模式：
- **精确匹配**：字符串完全相等，数值精确相等。
- **模糊匹配**：字符串采用归一化编辑距离阈值，数值采用相对误差阈值。
- **忽略匹配**：对特定字段标记为忽略，不参与评估。

### RLVR 奖励函数

在强化学习训练阶段，奖励函数设计如下：

$$
R(O, G) = \begin{cases}
-0.1 & \text{if } O \text{ is invalid JSON} \\
\alpha \cdot \mathrm{FMA}(O, G)^2 & \text{otherwise}
\end{cases}
$$

其中模式合规乘数 $\alpha$ 为：

$$
\alpha = \begin{cases}
1.0 & \text{if } O \text{ is valid w.r.t the schema} \\
0.8 & \text{otherwise}
\end{cases}
$$

该设计通过负惩罚抑制非法 JSON 输出，同时以字段匹配率的平方作为正向激励，并引入轻微的模式违规折扣（0.8），引导模型在维持结构合规性的同时提升内容准确性。

## 实验与分析

### 基准评估设置

SO-Bench 采用基于抽象语法树（AST）的递归字典比较评估方法，遵循 BFCL（Patil et al., 2025）的评估范式。针对原始类型字段，定义了三种匹配策略：**精确匹配**要求字段值与真值完全一致；**模糊匹配**对字符串采用归一化编辑距离（阈值 0.1），对数值采用相对误差（阈值 0.05）；部分字段标记为**忽略**，不参与评估。核心指标包括：

- **模式验证准确率**：输出是否为合法 JSON 且符合给定模式。
- **字段匹配准确率（FMA）**：所有样本中与输出字段匹配的真值字段数占总真值字段数的比例。
- **全结构匹配准确率（FSMA）**：所有真值字段均被正确匹配的样本比例，是评估全局结构化输出准确性的最严格指标。

### 主流模型性能全景对比

Table 1 展示了当前主流多模态大模型在 SO-Bench 上的结构化输出性能。核心发现如下：

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/006_Table_1.jpg]]
*Table 1: A comparison of structured output performance among different models. We cluster models based on their model size (active parameters), as well as open-sourced or proprietary models*

**最强模型的全匹配率极低。** Gemini-2.5-Pro 在所有指标上均取得最佳结果，但其 Full Match (Fuzzy) 仅为 18.91%，Full Match (Exact) 更是低至 11.38%。所有模型的 Full Match (Fuzzy) 均未超过 20%，揭示了当前 MLLM 在视觉结构化输出任务上的巨大提升空间。

**模式合规与内容准确存在显著鸿沟。** 尽管前沿闭源模型的 Schema Validation 准确率普遍超过 95%（GPT-5-mini 达 98.70%），但 Field Match (Fuzzy) 最高仅 73.14%（Gemini-2.5-Pro），表明模型虽能生成合法 JSON 结构，但在精确提取图像中的字段内容时仍面临严峻挑战。

**代际提升显著但仍有差距。** GPT-5 相比 GPT-4o 在 Schema Validation 上提升超过 15 个百分点，体现了新一代模型在指令遵循和结构化输出方面的进步。开源模型中，Qwen2.5-VL-72B 表现最佳，但在 Field Match (Fuzzy) 上仍落后 Gemini-2.5-Pro 约 20 个百分点。

**模型规模并非唯一决定因素。** 部分中小规模模型（如 GPT-5-mini）在模式验证上表现优异，但在字段匹配上与大规模模型存在明显差距，说明结构化输出能力受模型架构、训练数据和优化策略的综合影响。

### 指标相关性分析

Table 2 展示了 SO-Bench 指标与多个外部基准的 Pearson 相关性。Schema Validation 和 Field Match 与 **BFCL**（代理工具调用）、**LiveBench (Coding)**、**MMMU**（通用视觉知识）和 **MIABench**（视觉指令遵循）呈强正相关（高置信度，低 p 值）。这表明结构化输出能力与模型的代理推理与工具使用、通用视觉知识及视觉指令遵循能力紧密关联，验证了 SO-Bench 作为综合能力探针的有效性。

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/007_Table_2.jpg]]
*Table 2: Pearson correlation (r ↑) and the p-value for testing non-correlation (p ↓) between structural output metrics (Schema Validation, Field Match) and external benchmarks. IFEval, LiveBench-250425 (IF) for text-only instruction following; BFCL for agentic tool use; OCRBenchV2, CC-OCR, DocVQA for text-rich image understanding; RefCOCO for image referring; MMMU for general knowledge; MathVista for math; MIABench for visual instruction following. High correlations with high confidence (low p values) are highlighted in blue*

### 模式深度对性能的影响

Figure 6 展示了不同模式深度下的模型性能变化。随着 JSON 模式嵌套深度增加，所有模型的 Schema Validation 和 Field Match (Fuzzy) 均呈现下降趋势。深层嵌套结构（深度 ≥ 6）对模型的结构遵循能力构成显著挑战，即使是 Gemini-2.5-Pro 在深度 ≥ 6 时的 Field Match 也明显低于浅层模式。这一发现揭示了当前 MLLM 在处理复杂嵌套输出格式时的系统性脆弱性。

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/009_Figure_6.jpg]]
*Figure 6: Model performance across different schema depths. The left panel reports schema validation accuracy, while the right shows fuzzy field-match accuracy. Number of examples per schema depth ≤ 4 with 204 frames, 5 with 746 frames, 6 with 557 frames and ≥ 6 with 262 frames*

### 结构化输出 API 与提示策略对比

Table 3 对比了使用原生结构化输出 API 与指令遵循提示两种策略的效果。关键发现：

- **GPT-4o 系列**：使用结构化输出 API 可略微提升 Schema Validation，但 Field Match (Fuzzy) 反而下降，表明强制 JSON 模式约束可能牺牲内容提取质量。
- **GPT-5 和 Gemini 系列**：指令遵循提示效果更佳，这些模型自身具备较强的格式遵循能力，无需依赖外部 API 约束。
- 这一差异揭示了不同模型在内部结构化输出能力上的异质性，提示实际部署时需根据模型特性选择最优策略。

### 训练实验：SFT 与 RLVR 的增益

为探索结构化输出能力的可提升空间，作者基于 3B 基座模型进行了有监督微调（SFT）和可验证奖励强化学习（RLVR）实验。

**整体增益显著。** Table 4 和 Figure 7 显示，SFT 可将 Schema Validation 从基线的 65.1% 提升至 85.8%（+20.7 个百分点），Field Match (Fuzzy) 从 45.6% 提升至 56.5%（+10.9 个百分点）。RLVR 同样带来明显增益，但整体弱于 SFT。

**数据规模单调递增。** Figure 7 显示，无论是 SFT 还是 RLVR，增加训练数据量均可单调提升性能。SFT 在 50K 数据时达到 Schema Validation 峰值，在 114K 数据时 Field Match 持续改善。

**SFT 与 RLVR 的差异。** SFT 在所有训练规模上均优于 RLVR，但 RLVR 在有限数据下也能提供有意义的增益。RLVR 的奖励函数设计为：当输出为非法 JSON 时给予 -0.1 惩罚，否则采用带模式合规乘数 α 的 FMA² 作为奖励。α 在输出符合模式时为 1.0，否则为 0.8，以此引导模型维持结构合规性。

### 消融实验：数据组成的影响

**合成模式 vs. 真实模式。** Figure 8 显示，仅在合成 JSON 模式上训练的模型在真实模式子集上表现显著恶化，表明合成模式与真实应用模式之间存在分布偏移，训练数据的模式多样性至关重要。

**领域偏差的影响。** Figure 9 对比了随机采样训练与仅使用 AriaUI（浅层 UI 数据）训练的模型。后者在 Charts 领域表现极差，根本原因在于训练数据的模式深度分布与评估集不匹配——UI 数据以浅层结构为主，而 Charts 领域需要深层嵌套输出。这一发现强调了训练数据领域覆盖和模式深度多样性的重要性。

### 典型失败模式分析

通过对模型预测的定性分析，SO-Bench 揭示了以下关键失败模式：

**结构合规失败。** Figure 12 展示了仅用 AriaUI 数据训练的模型在图表样本上的典型错误：尽管提取的数值本身正确，但输出完全未遵循模式结构，导致所有指标得分为零。这反映了训练数据领域偏差导致的系统性结构遵循能力缺失。

**感知与推理盲区。** Figure 14 展示了 SFT 模型在文档图像上的错误：输出虽符合模式，但字段匹配得分为零，表明模型在密集文本或信息分散的图像上仍存在感知和推理盲区，训练增益有限。

**部分匹配与合规并存。** Figure 13 和 Figure 15 分别展示了 SFT 模型在自然图像和 UI 图像上的案例：输出符合模式且获得部分字段匹配分数，但仍有字段提取错误或遗漏，反映了内容级准确性的持续挑战。

### 公平性讨论

当前评估存在若干公平性考量：固定阈值的模糊匹配可能无法完全公平地比较语义正确但表述不同的输出；部分字段的忽略标记由专有 MLLM 生成，可能引入标注偏差；基准主要面向英文视觉场景，多语言公平性尚未验证。这些限制提示未来需要设计更灵活的语义匹配函数（如 VLM-as-a-judge）以提升评估的公平性和覆盖度。

### 补充图表

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/010_Figure_7.jpg]]
*Figure 7: Performance of models trained with different scales of data. Field Match and Full Structure Match are fuzzy version*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/012_Figure_8.jpg]]
*Figure 8: Performance of models on two subsets of SO-Bench. Field Match and Full Structure Match are fuzzy version*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/013_Figure_9.jpg]]
*Figure 9: The results breakdown by the data categories for the model trained with 20K randomly sampled data and model trained with Aria-UI subset of the data. In the left figure, we show the schema validation accuracy and in the right figure, we show the field match accuracy (fuzzy)*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/015_Figure_12.jpg]]
*Figure 12: An example error (Chart image) from the model trained on AriaUI subset of data. Although the extracted values themselves are correct, the output does not follow the schema structure at all, leading to 0 scores on all metrics in this case*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/016_Figure_13.jpg]]
*Figure 13: An example error (Natural image) from the SFT model trained on full data. This example gets partial score on field match but is invalid w.r.t. the schema*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/017_Figure_14.jpg]]
*Figure 14: An example error (Document) from the SFT model trained on full data. This example gets 0 score on field match while being valid w.r.t the schema*

![[assets/figures/papers/paper_list_l2748_https_arxiv_org_abs_2511_21750/figures/018_Figure_15.jpg]]
*Figure 15: An example error (UI image) from the SFT model trained on full data. This example gets partial score on field match while also being valid w.r.t the schema*

## 方法谱系与知识库定位

### 问题定位：视觉结构化输出的新基准

SO-Bench 首次系统性地定义了**视觉结构化输出**（Visual Structured Output）问题：给定输入图像 I、预定义的 JSON 模式 S 和用户指令 X，模型需生成既在语法上符合 S、又在语义上准确反映图像信息的结构化输出 Y。该问题的形式化概率表示为 $p(Y | I, X, S)$，将模式遵循（schema following）与视觉信息提取（visual extraction）统一在同一框架下。

这一任务定位填补了现有基准的关键空白。传统视觉问答和 OCR 基准仅评估自然语言输出的语义正确性，而代理工具调用（如 **BFCL**，Patil et al., 2025）和指令遵循（如 **IFEval**）基准则聚焦于纯文本域的结构化输出或函数调用。SO-Bench 的独特贡献在于将**视觉感知、模式理解和结构化生成**三个维度耦合在单一任务中，使评估更贴近现实应用（如菜单识别、文档解析、图表数据提取）中“按需定制输出格式”的需求。

### 与现有工作的关系

#### 上游数据与模式来源

SO-Bench 的构建深度依赖多个现有数据集和工具：
- **图像来源**：覆盖 UI（RICO, Deka et al., 2017; WebUI, Wu et al., 2023; ScreenSpot Pro, Li et al., 2025）、文档（OmniDocBench, Ouyang et al., 2025; DocVQA, Mathew et al., 2021; InfographicVQA, Mathew et al., 2022）、图表（ChartQA-Pro, Masry et al., 2025; ChartMuseum, Tang et al., 2025）和自然图像（HierText, Long et al., 2022）四类场景。
- **模式检索**：利用 **CLIP**（Radford et al., 2021）的图像和文本编码器计算多模态嵌入，通过加权余弦相似度实现图像与 JSON 模式的自动匹配。
- **评估框架**：沿用 **BFCL**（Patil et al., 2025）的 AST 递归字典比较方法，并在此基础上扩展了模糊匹配和字段忽略策略。

#### 对比的基线模型

SO-Bench 在评估中覆盖了当前主流的开源和闭源多模态大模型：
- **闭源模型**：**GPT-4o / GPT-4o-mini**（Hurst et al., 2024）、**GPT-5 / GPT-5-mini**（OpenAI, 2025）、**Gemini-2.5-Pro / Flash**（Comanici et al., 2025）。其中 Gemini-2.5-Pro 在 Full Match (Fuzzy) 上以 18.91% 领先，GPT-5 相比 GPT-4o 的模式验证准确率提升超过 15 个百分点。
- **开源模型**：**Qwen2.5-VL** 系列（3B, 32B, 72B; Bai et al., 2025）、**Intern3.5-VL**（4B, 38B; Wang et al., 2025b）。开源模型在模式验证和字段匹配上普遍落后于同等规模的闭源模型，尤其在深层嵌套模式下差距显著。

#### 训练数据与优化方法对比

SO-Bench 不仅是一个评估基准，还提供了训练改进的实证路径：
- **基线方法**：预训练模型 zero-shot 推理，无额外结构化输出训练。
- **有监督微调（SFT）**：在 114K 结构化图像-模式对上进行微调，将 3B 基座模型的 Schema Validation Accuracy 从 65.1% 提升至 85.8%（+20.7 个百分点），Field Match (Fuzzy) 从 45.6% 提升至 56.5%（+10.9 个百分点）。
- **可验证奖励强化学习（RLVR）**：采用基于字段匹配准确率的奖励函数 $R(O,G) = \begin{cases} -0.1 & \text{if } O \text{ is invalid JSON} \\ \alpha \cdot \mathrm{FMA}(O,G)^2 & \text{otherwise} \end{cases}$，其中模式合规乘数 $\alpha = \begin{cases} 1.0 & \text{if } O \text{ is valid w.r.t the schema} \\ 0.8 & \text{otherwise} \end{cases}$。RLVR 在有限数据下也带来明显增益，但整体效果弱于 SFT。

### 适用边界与核心局限

#### 评估指标的语义盲区

当前评估基于固定阈值的编辑距离和相对误差匹配，**无法捕获语义等价但表述形式不同的正确输出**。例如，数值“1.0”与“1.00”在模糊匹配下可能被判定为不同，而“New York”与“NYC”则完全无法匹配。论文作者也承认，开发更灵活的语义匹配函数（如 VLM-as-a-judge）是未来改进方向。

#### 语言与模态的覆盖限制

- **语言限制**：训练和评估均以英文数据为主，多语言及跨文化视觉场景尚未验证。
- **模态限制**：当前基准仅覆盖静态图像，未扩展至视频、多轮交互等更复杂的 agentic 环境。

#### 训练实验的规模约束

训练实验仅基于 3B 参数规模的模型，缩放至更大模型（如 32B、72B）时 SFT 和 RLVR 的相对增益如何变化仍是开放问题。此外，人类验证虽确保了数据质量，但规模受限，可能引入主观偏差；自动 critic 模型自身也存在错误。

#### 感知与推理的固有盲区

模型在高分辨率、密集文本或信息分散的图像上仍存在感知和推理盲区。训练增益在这些场景下有限：即使经过 SFT，模型在自然图像上仍可能出现 schema 非法错误，在文档图像上可能出现字段完全失配，在 UI 图像上可能仅获得部分匹配分数。

### 开放问题与未来方向

1. **语义匹配函数的改进**：如何设计更灵活的评估策略（如 VLM-as-a-judge）以提升评估的公平性和覆盖度？
2. **推理增强训练**：能否通过融入 chain-of-thought 推理或设计更精细的奖励函数，进一步缩小 Full Match 的巨大差距（当前最优仅 18.91%）？
3. **深层嵌套与密集文本的针对性优化**：针对深层嵌套模式和高分辨率密集文本场景，什么类型的训练数据和模型架构改进最为有效？
4. **多模态与多步扩展**：如何将 SO-Bench 扩展至更多模态（如视频、音频）和需要多步工具调用的复杂 agentic 任务？
5. **模型规模缩放效应**：训练实验仅基于 3B 模型，缩放至更大模型时 RLVR 和 SFT 的增益如何变化？是否需要调整训练策略？

### 知识库定位总结

SO-Bench 在知识谱系中处于**多模态评估基准**和**结构化输出训练**的交叉节点。它向上继承 CLIP、BFCL 等基础工具，横向覆盖 GPT-5、Gemini-2.5-Pro 等前沿模型的评估，向下通过 SFT 和 RLVR 训练实验为后续改进提供了实证基线。其核心洞察——所有模型的 Full Match 准确率均不超过 19%——为社区指明了明确的提升空间：模式合规性可通过 API 约束或指令提示部分解决，但**视觉感知精度与深层结构推理的耦合**仍是尚未攻克的瓶颈。

## 原文 PDF

![[paperPDFs/CVPR_2026/SO_Bench_A_Structural_Output_Evaluation_of_Multimodal_LLM.pdf]]
