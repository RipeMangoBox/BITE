---
title: "PromptEnhancer: Taming Your Rewriter for Text-to-Image Generation via Fine-Grained Reward"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PromptEnhancer_Taming_Your_Rewriter_for_Text_to_Image_Generation_via_Fine_Grained_Reward.pdf
project_link: "https://hunyuan-promptenhancer.github.io/"
code_link: null
aliases:
- PromptEnhancer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过训练一个专用的链式思维（CoT）提示改写器，并利用细粒度奖励模型（AlignEvaluator）在24个关键点上提供的结构化反馈进行强化学习优化，从而系统性地提升提示的完整性和可解释性，间接改善图像-文本对齐。
primary_logic: 将提示改写与生成模型解耦，并通过针对T2I失败模式的细粒度反馈来优化改写策略，是提升任何预训练T2I模型对齐性的通用且有效的方法。
claims:
- PromptEnhancer在GenEval基准上将Qwen-Image的总体得分从0.84提升至0.86。
- PromptEnhancer在T2I-CompBench基准上将Qwen-Image的空间关系（Spatial）得分从0.3222提升至0.4472。
- 在训练阶段消融中，GRPO将模型得分从SFT（含CoT）的85.29%进一步提升至88.15%。
- AlignEvaluator基于24个细粒度关键点提供奖励，涵盖语言理解、视觉属性、动作交互、关系结构和知识等六大类别。
---

# PromptEnhancer: Taming Your Rewriter for Text-to-Image Generation via Fine-Grained Reward

> [!tip] 核心洞察
> 将提示改写与生成模型解耦，并通过针对T2I失败模式的细粒度反馈来优化改写策略，是提升任何预训练T2I模型对齐性的通用且有效的方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | PromptEnhancer：通过细粒度奖励驯服文本到图像生成的改写器 |
| 英文题名 | PromptEnhancer: Taming Your Rewriter for Text-to-Image Generation via Fine-Grained Reward |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_PromptEnhancer_Taming_Your_Rewriter_for_Text-to-Image_Generation_via_Fine-Grained_Reward_CVPR_2026_paper.html) · [Project](https://hunyuan-promptenhancer.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PromptEnhancer |
| Dataset | GenEval, T2I-CompBench, T2I-Keypoints-Align |

> [!tip] 效果简介
> - GenEval 上，Overall Score 0.86 (Qwen-Image + PE) vs 0.84 (Qwen-Image, no rewriter) (+0.02)；Overall Score 0.82 (HY-Image 2.1 + PE) vs 0.80 (HY-Image 2.1, no rewriter) (+0.02)。
> - T2I-CompBench 上，Spatial 0.4472 (Qwen-Image + PE) vs 0.3222 (Qwen-Image, no rewriter) (+0.1250)；Color 0.8442 (Qwen-Image + PE) vs 0.7962 (Qwen-Image, no rewriter) (+0.0480)。
> - T2I-Keypoints-Align (Internal) 上，Average accuracy over 24 categories 87.1% (with PE) vs 82.0% (without PE) (+5.1 points)。

## 概要

### 问题瓶颈

当前文本到图像（T2I）生成模型在处理用户输入的短促、模糊提示时，普遍面临**组合性生成**的严峻挑战。具体表现为属性绑定错误、否定语义理解偏差、空间关系推理混乱等失败模式，导致生成的图像与用户真实意图之间存在显著的对齐差距。这一瓶颈并非源于生成模型本身的生成能力不足，而是提示的可解释性不足——模型难以从简略的提示中准确解析出隐含的语义约束和结构化关系。

### 核心思路

**PromptEnhancer** 提出了一条解耦路径：不修改任何预训练T2I模型的权重，而是训练一个专用的**链式思维（CoT）提示改写器**，将用户原始提示自动转换为结构清晰、语义完整、显式化隐含约束的改写提示。改写器生成的提示再送入冻结的T2I模型进行图像生成，从而在输入端系统性地弥合对齐差距。

这一策略的关键洞察在于：**通过细粒度奖励信号来驯服改写器**。PromptEnhancer引入了一个专用的奖励模型 **AlignEvaluator**，该模型基于覆盖六大类别（语言理解、视觉属性、动作交互、关系结构、结构完整性、知识）的24个细粒度关键点，对生成的图像-提示对提供结构化对齐评分，而非依赖粗粒度的CLIP相似度或通用人类偏好模型。这一细粒度反馈使得改写器的强化学习优化能够精准针对T2I的典型失败模式。

### 方法定位

PromptEnhancer是一个**通用、模型无关**的提示改写框架，其训练流程分为两个阶段：

1. **监督微调（SFT）初始化**：在蒸馏得到的（用户提示，改写提示）数据对上训练CoT改写器，使其学会生成结构化、链式思维风格的响应，建立改写能力的基础。
2. **策略对齐（GRPO强化学习）**：利用AlignEvaluator提供的标量奖励信号，通过组相对策略优化（GRPO）进一步精炼改写策略，使其生成的提示能最大化图像与用户意图的对齐程度。

在方法谱系中，PromptEnhancer区别于两类基线：一是**BeautifulPrompt**（Cao et al., EMNLP 2023 Industry）等基于评分筛选的自动提示优化方法，它们缺乏针对T2I失败模式的细粒度反馈；二是**GPT-4o**等通用大语言模型直接重写，它们未经过专门的T2I对齐训练。PromptEnhancer通过将提示改写与生成模型完全解耦，并引入细粒度奖励机制，实现了对任何预训练T2I模型的即插即用增强。

### 主要结果

在标准组合性基准上的定量评估验证了PromptEnhancer的有效性：

- **GenEval基准**：将Qwen-Image的总体得分从0.84提升至0.86，将HY-Image 2.1的总体得分从0.80提升至0.82（Table 3）。
- **T2I-CompBench基准**：在空间关系（Spatial）维度上，将Qwen-Image的得分从0.3222大幅提升至0.4472（+0.1250）；在颜色（Color）维度上从0.7962提升至0.8442（+0.0480）（Table 4）。
- **内部T2I-Keypoints-Align评估**：在24个细粒度类别上的平均提示跟随准确度从82.0%提升至87.1%（+5.1个百分点）（Figure 7）。

训练阶段的消融实验揭示了各阶段的关键贡献：SFT阶段使模型得分从基线81.0%大幅提升至85.29%（含CoT），而GRPO进一步将得分推高至88.15%，取得了最佳结果。值得注意的是，CoT监督在单独使用（SFT阶段）时收益有限，但与GRPO结合时才发挥出更大价值——这表明强化学习的探索-优化机制能够更充分地利用结构化推理的潜力（Table 5）。

文本到图像（T2I）生成模型近年来取得了显著进展，能够根据自然语言描述合成高质量、多样化的视觉内容。然而，一个持续存在的瓶颈在于**用户输入的提示（prompt）与模型理解能力之间的对齐差距**。现实场景中，用户往往提供简短、模糊甚至不完整的提示，而T2I模型在准确执行属性绑定、否定理解、空间关系推理等组合性任务时仍面临系统性困难。这导致生成的图像频繁出现语义错配——例如对象颜色错误、数量偏差、空间布局混乱——严重限制了可靠生成的应用边界。

现有应对这一问题的策略大致分为两类。一类是**直接优化T2I模型本身**，通过改进文本编码器、注入空间条件或增强跨模态注意力来提升组合理解能力。这类方法通常需要修改模型架构或重新训练生成器，计算成本高昂，且对已部署的预训练模型缺乏即插即用的兼容性。另一类是**提示工程与自动改写**，例如 **BeautifulPrompt**（Cao et al., EMNLP 2023 Industry）通过评分筛选优化提示，或直接调用 **GPT-4o** 等通用大语言模型进行重写。然而，这些方法的优化信号往往是粗粒度的——仅依赖CLIP相似度分数或通用人类偏好模型——缺乏对T2I具体失败模式的细粒度感知，导致改写方向不够精准，提升效果有限。

本文的**核心动机**在于：将提示改写与生成模型完全解耦，并通过**针对T2I失败模式的细粒度反馈**来训练一个专用的改写器，从而以模型无关的方式系统性提升任何预训练T2I模型的对齐性能。这一思路的直觉是：如果能让改写器学会识别并补全原始提示中缺失的语义要素——包括对象的视觉属性、动作交互、空间关系和隐含约束——那么即使底层生成器保持不变，图像质量和对齐度也能获得实质改善。为此，本文提出 **PromptEnhancer**，一个由细粒度奖励模型驱动的通用提示改写框架，其核心创新在于构建了覆盖24个评估关键点的结构化反馈信号，并通过链式思维（CoT）改写与强化学习的结合，驯服改写器朝着最大化图像-文本对齐的方向演进。

## 核心方法与创新机理

PromptEnhancer 的核心创新并非设计一个新的文本到图像（T2I）生成模型，而是**将提示理解与图像生成解耦**，通过训练一个专用的提示改写器来系统性地缩小用户意图与生成结果之间的对齐差距。其关键洞察在于：与其修改冻结的预训练 T2I 模型，不如将优化重心前移至输入端，通过提升提示的完整性和可解释性来间接改善图像-文本对齐。这一思路使 PromptEnhancer 成为一个**模型无关的通用框架**，可服务于任何预训练 T2I 模型。

### 1. 从粗粒度偏好到细粒度结构化反馈的奖励信号变革

传统提示优化方法通常依赖粗粒度的 CLIP 相似度分数或通用人类偏好模型作为奖励信号。这些信号虽然能反映整体语义一致性，但难以捕捉 T2I 生成中常见的细粒度失败模式——例如属性绑定错误、否定理解偏差、空间关系混淆等。

PromptEnhancer 的核心突破在于构建了 **AlignEvaluator**——一个专门针对 T2I 失败模式设计的细粒度奖励模型。AlignEvaluator 基于一套包含 **24 个细粒度关键点**的评估体系（Table 1），涵盖六大类别：语言理解、视觉属性、动作交互、关系结构、知识和结构完整性。对于每一对生成图像与改写提示，AlignEvaluator 在每个关键点上给出对齐分数，最终奖励定义为这些分数的均值：

$$r_{i} = \mathrm{AlignEvaluator}(\mathbf{x}_{i}, \mathbf{p}_{i}^{\prime}), \quad i = 1,2,\ldots,N.$$

这一设计将奖励信号从“整体像不像”升级为“具体哪里对、哪里错”的多维度诊断，使改写器能够在强化学习阶段获得明确的行为指引——这正是 PromptEnhancer 在空间关系（T2I-CompBench Spatial 得分从 0.3222 提升至 0.4472）和颜色属性（Color 得分从 0.7962 提升至 0.8442）等组合性任务上取得显著增益的根本原因。

### 2. 两阶段训练策略：SFT 初始化 + GRPO 在线策略对齐

与仅依赖单阶段监督微调（SFT）或直接调用通用大语言模型（如 GPT-4o）进行重写不同，PromptEnhancer 采用**两阶段训练策略**，将模仿学习与偏好优化有机结合：

- **阶段一（SFT 初始化）**：在人工管护的（用户提示，改写提示）数据集上进行监督微调，使 CoT Rewriter 初步掌握链式思维（Chain-of-Thought）风格的结构化重写能力。此阶段建立了“识别关键语义元素→消解歧义→显式化隐含约束”的推理基础。
- **阶段二（GRPO 策略对齐）**：以 SFT 初始化模型为起点，采用 Group Relative Policy Optimization（GRPO）进行在线强化学习优化。在每次 rollout 中，策略模型为同一用户提示生成多个候选改写，由冻结的 T2I 模型生成对应图像，AlignEvaluator 对每对（图像，用户提示）计算标量奖励，进而优化改写策略。

消融实验（Table 5）揭示了这一设计的精妙之处：SFT 阶段将模型得分从基线 81.0% 大幅提升至约 86.0%（无 CoT）或 85.29%（含 CoT），而 GRPO 进一步将含 CoT 的 SFT 模型得分推高至 88.15%。值得注意的是，**CoT 监督在 SFT 阶段单独使用时收益有限，但与 GRPO 结合后才真正释放其价值**——这表明细粒度奖励信号能够有效引导模型利用链式推理能力，而非仅仅模仿训练数据中的重写模式。

### 3. 链式思维提示表示：从短促模糊到结构化显式描述

用户输入的原始提示往往短促且模糊，缺乏对属性、关系和约束的明确描述。PromptEnhancer 通过 **CoT Rewriter** 将这类提示转化为富含细节的结构化文本，显式地补充了 T2I 模型难以从简短提示中推断的语义信息。

CoT Rewriter 基于 Hunyuan-7B-Instruct 初始化，遵循链式思维流程：首先识别提示中的关键语义元素，然后消解歧义，最后将隐含约束显式化。这一过程产生的改写提示不仅包含更丰富的视觉描述，还以结构化方式组织信息，使下游 T2I 模型更容易准确解析和执行。图 6 的定性对比直观展示了这一效果——同一原始提示经 PE 重写后，生成的图像在目标身份、动作、外观和风格上均更忠实于用户意图。

### 创新总结

PromptEnhancer 的方法论贡献可归纳为三个 **changed slots**：将奖励信号从粗粒度标量升级为 24 维细粒度结构化反馈，将训练策略从单阶段 SFT 重构为 SFT+GRPO 两阶段对齐，将提示表示从原始短文本转化为链式思维结构化描述。这三者形成因果闭环——细粒度奖励为 GRPO 提供精准优化方向，GRPO 释放 CoT 的推理潜力，CoT 重写则为 AlignEvaluator 提供更丰富的评估素材。在 GenEval 基准上，该框架将 Qwen-Image 和 HY-Image 2.1 的整体得分分别从 0.84 和 0.80 提升至 0.86 和 0.82，验证了其作为通用提示增强层的有效性与迁移性。

PromptEnhancer 的核心设计思想是将提示改写与图像生成解耦，在不修改任何预训练 T2I 模型权重的前提下，通过一个可训练的改写器系统性地提升图像-文本对齐质量。整个框架由三个模块串联构成一个闭环训练管线：

**CoT Rewriter（策略模型）** 接收用户输入的简短、模糊提示，通过链式思维（Chain-of-Thought）推理过程，识别关键语义元素、消解歧义并将隐式约束显式化，最终输出一个富含细节和结构化描述的重写提示。该模块基于 **Hunyuan-7B-Instruct** 初始化。

**Off-the-shelf T2I Model（冻结的图像生成器）** 使用 CoT Rewriter 输出的重写提示生成图像。该模块在整个训练过程中参数保持固定，仅作为图像生成的后端。

**AlignEvaluator（细粒度奖励模型）** 对生成的图像与原始用户提示之间的对齐程度进行评估。它基于一个包含 24 个细粒度关键点的评估体系（涵盖语言理解、视觉属性、动作交互、关系结构和知识等六大类别），为每对图像-提示输出一个标量奖励分数。该模块由 **Qwen2.5-VL-32B-Instruct** 在 T2I-Keypoints 标注集上微调得到。

训练采用两阶段策略：**第一阶段**通过监督微调（SFT）在蒸馏得到的（用户提示，重写提示）数据对上训练 CoT Rewriter，使其具备生成链式思维风格结构化响应能力；**第二阶段**采用 Group Relative Policy Optimization（GRPO）进行策略对齐——Rewriter 为每个输入提示采样多个候选重写提示，冻结的 T2I 模型据此生成图像，AlignEvaluator 对每对图像-提示对计算标量奖励 $r_i = \mathrm{AlignEvaluator}(\mathbf{x}_i, \mathbf{p}_i^{\prime})$，该奖励信号驱动 Rewriter 的策略优化，使其生成能最大化图像与用户意图对齐的提示。

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the training framework for PromptEnhancer. Our framework trains a universal Rewriter to enhance pretrained Text-to-Image (T2I) model without altering its weights. This is achieved through a two-stage process guided by a specialized reward model. Stage 1: SFT for Rewriter Initialization (Sec 3.1.1). The CoT Rewriter is first initialized via SFT on (user prompt, reprompt) pairs. This stage teaches the model to generate structured, chain-of-thought style responses using a standard next-token prediction loss, establishing a strong foundation for refinement. Stage 2: Policy Alignment with GRPO (Sec 3.1.2). The initialized rewriter is further refined using GRPO. The rewriter genera...*

### 模块一：CoT Rewriter（链式思维改写器）

CoT Rewriter 是 PromptEnhancer 的策略模型，负责将用户输入的简短、模糊提示转化为富含细节与结构化推理的文本描述。该模块基于 **Hunyuan-7B-Instruct** 初始化，遵循链式思维（Chain-of-Thought）流程：首先识别提示中的关键语义要素，消解歧义，并将隐含约束显式化，从而生成更易于下游 T2I 模型解释的改写提示。

### 模块二：AlignEvaluator（对齐评估器）

AlignEvaluator 是框架中的细粒度奖励模型，由 **Qwen2.5-VL-32B-Instruct** 在 T2I-Keypoints 标注集上微调得到。其核心能力是对图像-提示对在 **24 个细粒度关键点** 上进行逐项对齐评分，覆盖六大类别：语言理解、视觉属性、动作交互、关系结构、结构完整性与知识一致性（详见 Table 1）。该模块为后续强化学习阶段提供结构化、多维度的标量奖励信号。

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/005_Table_1.jpg]]
*Table 1: Our proposed evaluation of criteria for T2I Generation. TIC denotes Text-Image Consistency, SI denotes Structural Integrity, and TIC&SI denotes the evaluation of both dimensions*

### 模块三：Off-the-shelf T2I Model（冻结的预训练生成器）

框架中的 T2I 模型（如 Hunyuan-Image 2.1 或 Qwen-Image）在整个训练过程中保持参数冻结，仅作为图像生成器使用。改写后的提示输入该模型得到生成图像，而 AlignEvaluator 则基于图像与原始用户提示的对齐程度计算奖励，从而间接优化改写策略。

### 核心公式：GRPO 阶段的奖励定义

在第二阶段策略对齐中，AlignEvaluator 为每对生成图像与改写提示输出标量奖励，作为 Group Relative Policy Optimization（GRPO）的优化目标：

$$r_{i} = \mathrm{AlignEvaluator}(\mathbf{x}_{i}, \mathbf{p}_{i}^{\prime}), \quad i = 1,2,\ldots,N.$$

其中：
- $\mathbf{x}_{i}$ 表示由冻结 T2I 模型根据第 $i$ 个改写提示生成的图像；
- $\mathbf{p}_{i}^{\prime}$ 表示 CoT Rewriter 为同一用户提示生成的第 $i$ 个候选改写提示；
- $r_{i}$ 为 AlignEvaluator 输出的标量奖励，取 24 个关键点评分的平均值；
- $N$ 为 GRPO 每次 rollout 采样的候选改写提示数量。

该公式锚定于论文 Section 3.1.2 的 Equation (1)，是整个强化学习优化链路的核心信号来源。

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison of prompt rewriting. Starting from the same raw prompt, PE produces a more explicit and informative rewritten prompt, leading to a generated image that better matches the intended semantics and visual details*

## 实验与关键发现

### 核心定量结果：PromptEnhancer 在两个标准基准上一致提升多款 T2I 模型

PromptEnhancer 的核心主张——通过细粒度奖励驯服提示改写器，使冻结的预训练 T2I 模型生成更符合用户意图的图像——在两套广泛使用的组合性基准上得到了定量验证。表 3 和表 4 分别报告了 GenEval 和 T2I-CompBench 上的主要结果。

在 **GenEval** 基准上，PromptEnhancer 对两款不同架构的 T2I 模型均带来一致的总体得分提升：
- **Qwen-Image**：总体得分从 0.84 提升至 **0.86**（+0.02）。
- **HY-Image 2.1**：总体得分从 0.80 提升至 **0.82**（+0.02）。

这一提升幅度虽然绝对值不大，但考虑到 GenEval 已是高度优化的基准，且 PromptEnhancer 完全不修改 T2I 模型权重，仅通过改写输入提示实现增益，其结果具有实际意义。作为对比，**BeautifulPrompt**（Cao et al., EMNLP 2023 Industry）——一种基于提示评分筛选的自动优化方法——在相同设置下未能带来一致的提升，甚至在某些子指标上出现倒退，这从侧面印证了 PromptEnhancer 的细粒度奖励驱动策略的有效性。

在 **T2I-CompBench** 基准上，PromptEnhancer 的优势在空间关系（Spatial）和颜色绑定（Color）等组合性任务上尤为突出：
- **空间关系**：Qwen-Image 的得分从 0.3222 跃升至 **0.4472**（+0.1250），相对提升约 38.8%。
- **颜色绑定**：Qwen-Image 的得分从 0.7962 提升至 **0.8442**（+0.0480）。

空间关系任务要求模型准确理解“在……左边”“在……上方”等介词结构，是当前 T2I 模型的公认短板。PromptEnhancer 在此维度上的大幅提升，说明其 CoT 改写器能够将模糊的空间描述转化为更显式、更易于模型解析的结构化语言，从而间接弥补了 T2I 模型在关系推理上的不足。

### 内部细粒度评估：24 个关键点上的类别级提升

除了公开基准，作者还在内部构建的 **T2I-Keypoints-Align** 数据集上进行了类别级评估。该数据集基于 24 个细粒度关键点（见表 1）对图像-提示对齐程度进行打分，涵盖语言理解、视觉属性、动作交互、关系结构和知识等六大超类。图 7 展示了应用 PromptEnhancer 前后，基础模型在各类别上的绝对准确率变化。

核心发现是：**PromptEnhancer 将平均类别准确率从 82.0% 提升至 87.1%（+5.1 个百分点）**。这一提升并非均匀分布——在涉及属性绑定、否定理解和空间关系的类别上增益最为显著，而在简单的物体识别类别上提升有限。这一模式与 PromptEnhancer 的设计目标高度吻合：改写器的核心价值在于将隐式约束显式化、将模糊指代具体化，而这些正是组合性任务中最需要的干预。

### 训练阶段消融：SFT 奠定基础，GRPO 释放 CoT 潜力

表 5 报告了训练阶段的消融实验结果，揭示了 SFT 和 GRPO 两个阶段各自的贡献及其交互效应。实验以内部评估集上的平均得分为指标，基线（无改写器）得分为 81.0%。

| 训练配置 | 得分 |
|---------|------|
| 基线（无改写器） | 81.0% |
| SFT（无 CoT） | 86.0% |
| SFT（含 CoT） | 85.29% |
| SFT（含 CoT）+ GRPO | **88.15%** |

消融结果揭示了两个关键洞察：

1. **SFT 阶段是性能提升的主要驱动力**：仅通过监督微调，模型得分就从 81.0% 大幅跃升至 86.0%（无 CoT）或 85.29%（含 CoT）。这表明，在高质量改写数据上的行为克隆已经足以让改写器掌握基本的提示增强能力。

2. **CoT 的价值需要 GRPO 来释放**：有趣的是，在 SFT 阶段引入 CoT 监督并未带来额外收益，甚至略低于无 CoT 的 SFT 模型（85.29% vs 86.0%）。然而，当进一步应用 GRPO 强化学习后，含 CoT 的模型得分跃升至 88.15%，成为所有配置中的最优结果。这一现象说明：CoT 推理链为策略模型提供了更丰富的探索空间，但仅靠模仿学习无法有效利用这一空间；GRPO 通过 AlignEvaluator 的细粒度奖励信号，引导模型在 CoT 框架内进行策略优化，才真正释放了结构化推理的潜力。

### 定性分析：改写如何改善图像-文本对齐

图 5 和图 6 从定性角度展示了 PromptEnhancer 的改写效果。图 5 将 PromptEnhancer 与 GPT-4o、Seedream 3.0、Kolors 2.1、Recraft V3 等基线改写器进行对比，结果显示 PromptEnhancer 改写后的提示在语义保真度、属性绑定准确性和组合一致性上均优于基线。图 6 进一步放大单个案例：对于同一原始提示，PromptEnhancer 生成的改写版本显式指定了目标身份、动作、外观和风格等细节，使得 T2I 模型能够生成更贴合意图的图像。

这些定性结果与定量发现相互印证：PromptEnhancer 的改写并非简单的文本扩写，而是针对 T2I 模型常见失败模式（如属性混淆、空间关系错误、否定忽略）的结构化补全。

### 方法谱系与知识库定位

PromptEnhancer 在提示优化与 T2I 对齐这一交叉领域中占据了独特位置。与 **BeautifulPrompt**（Cao et al., EMNLP 2023 Industry）等基于评分的筛选式方法不同，PromptEnhancer 通过强化学习主动优化改写策略；与直接使用 **GPT-4o** 等通用 LLM 进行提示重写的做法相比，PromptEnhancer 的 CoT 改写器专门针对 T2I 失败模式进行了微调和偏好对齐。其核心创新——AlignEvaluator 提供的 24 维细粒度奖励信号——填补了从粗粒度 CLIP 相似度到结构化对齐评估之间的空白，为提示改写器的训练提供了更精确的优化目标。

从知识库定位来看，PromptEnhancer 属于“模型无关的提示增强”范式：它不修改 T2I 模型权重，不依赖特定架构，理论上可适配任何预训练 T2I 模型。这一特性使其具有较高的实用价值，但同时也意味着其性能上限受限于底层 T2I 模型的能力——改写只能弥补提示表达上的不足，无法修复 T2I 模型本身的生成缺陷。

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/009_Table_3.jpg]]
*Table 3: GenEval results with different prompt rewriter*

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparisons of PromptEnhancer against baseline prompt rewriters on text-to-image generation. For each raw prompt, we compare the rewritten prompt produced by PromptEnhancer with those generated by GPT-4o, Seedream 3.0, Kolors 2.1, Recraft V3, Qwen-Image, and Hunyuan Image, and show the corresponding synthesized images. PromptEnhancer produces rewritten prompts that lead to images with stronger semantic fidelity, more accurate attribute binding, and better compositional consistency*

![[assets/figures/papers/paper_list_l2194_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_PromptEnhancer_Ta/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the data curation pipeline for PromptEnhancer. Starting from an image set, we simulate user prompts, generate CoT reasoning and rewritten prompts with Gemini, perform automated verification to remove low-quality samples, and finally apply human-in-the-loop selection to construct high-quality training triplets for SFT*

## 定位与知识库关联

### 核心思路：解耦式提示改写作为通用对齐增强层

PromptEnhancer 的核心思想是将**提示改写**与**图像生成**完全解耦：训练一个专用的链式思维（CoT）改写器，在不修改任何预训练 T2I 模型权重的前提下，通过提升输入提示的可解释性来间接改善图像-文本对齐。这一思路将问题从“如何让生成模型更好地理解提示”转化为“如何让提示更容易被生成模型理解”，从而获得天然的模型无关性——同一改写器可服务于不同架构的 T2I 模型。

从因果机制看，该方法的有效性依赖于一个关键假设：**T2I 模型的组合性失败（属性绑定错误、否定理解偏差、空间关系混淆）在很大程度上源于提示本身的欠指定或歧义，而非生成模型能力的绝对上限**。通过训练改写器系统性地消除这些歧义——将隐式约束显式化、将模糊指代具体化、将空间关系结构化——可以在不触及生成模型参数的情况下显著缩小意图-图像对齐差距。

### 与现有提示优化方法的对比

#### 基于评分筛选的自动提示优化

**BeautifulPrompt**（Cao et al., EMNLP 2023 Industry）代表了提示优化中的“筛选”范式：通过生成多个候选提示并基于预设评分函数选择最优者。这类方法的瓶颈在于**奖励信号的粒度**——通常依赖粗粒度的 CLIP 相似度分数或通用人类偏好模型，难以针对 T2I 特定的失败模式（如属性绑定、空间关系）提供精准反馈。PromptEnhancer 的关键差异在于引入 **AlignEvaluator** 这一专用奖励模型，在 24 个细粒度关键点上提供结构化对齐评估，使奖励信号能够区分“颜色正确但空间错误”与“空间正确但属性遗漏”等不同失败类型，从而引导 GRPO 强化学习进行针对性优化。

#### 通用大语言模型的直接改写

使用 **GPT-4o** 等通用 LLM 直接重写提示是一种直观的基线方法。然而，通用 LLM 缺乏对 T2I 模型特定失败模式的感知——它们可能生成语法优美但并未解决实际对齐瓶颈的改写。PromptEnhancer 通过两阶段训练（SFT + GRPO）使改写器内化了 T2I 对齐的结构化知识：SFT 阶段注入链式思维改写模式，GRPO 阶段则通过 AlignEvaluator 的反馈使改写策略直接面向“生成图像与用户意图的对齐程度”进行优化。消融实验（Table 5）表明，单独的 SFT（含 CoT）将得分从基线 81.0% 提升至 85.29%，而 GRPO 进一步推高至 88.15%，证实了强化学习对齐阶段的独立贡献。

#### 与端到端 T2I 模型内部优化的关系

另一类相关工作直接在 T2I 模型内部增强组合性理解能力（如通过改进文本编码器或引入空间条件）。PromptEnhancer 与这些方法**正交且互补**：它作为外部改写层运作，可以与任何内部优化叠加使用。实验证据支持这一判断——在 Qwen-Image 和 HY-Image 2.1 两个独立训练的 T2I 模型上，PromptEnhancer 均带来一致的性能提升（GenEval Overall 分别从 0.84→0.86 和 0.80→0.82），表明其收益不依赖于特定生成模型的内部机制。

### 适用边界与条件

基于现有证据，PromptEnhancer 的适用边界可从以下几个维度界定：

1. **对基础模型能力的依赖**：改写器只能消除提示层面的歧义，无法弥补 T2I 模型的根本性生成缺陷。若某类视觉概念完全超出生成模型的训练分布，再精准的提示改写也无法产生正确图像。Table 4 中 Spatial 维度的大幅提升（0.3222→0.4472）表明改写对空间关系理解有显著帮助，但 Color 维度的提升幅度较小（0.7962→0.8442），暗示当基础模型的颜色绑定能力已较高时，改写带来的边际收益递减。

2. **对提示类型的敏感度**：该方法对**短促、模糊、欠指定的用户提示**最为有效——这类提示正是 CoT 改写发挥结构化推理优势的典型场景。对于已经高度详细和精确的提示，改写可能仅产生微调效果甚至引入冗余。论文未提供按提示长度或复杂度分层的性能分析，这一点需要人工验证。

3. **计算开销的权衡**：两阶段训练流程（SFT + GRPO）以及推理时的 CoT 生成引入了额外计算成本。改写器基于 Hunyuan-7B-Instruct 初始化，AlignerEvaluator 基于 Qwen2.5-VL-32B-Instruct 微调，两者合计的参数量和推理延迟在实际部署中需要与对齐收益进行权衡。论文未提供详细的延迟分析或轻量化变体。

### 局限性与开放问题

从方法论角度，以下局限和开放问题值得关注：

1. **奖励模型的偏差传播**：AlignEvaluator 本身是基于 T2I-Keypoints 标注集训练的模型，其评估标准可能继承标注数据的分布偏差。如果某些关键点类别在训练数据中代表性不足（参考 Figure 3 的分布），对应维度的奖励信号可能不够可靠，进而影响 GRPO 阶段的优化方向。

2. **CoT 推理质量的稳定性**：链式思维改写虽然提升了提示的结构化程度，但也引入了推理错误的可能性——改写器可能“过度解读”用户意图或引入幻觉性细节。论文的定性示例（Figure 5、Figure 6）展示了成功案例，但未系统报告改写失败或退化的比例。

3. **跨领域泛化验证**：现有评估集中在 GenEval 和 T2I-CompBench 两个组合性基准，以及内部的 T2I-Keypoints-Align 测试。对于更广泛的开放域提示分布（如高度抽象的艺术描述、文化特定概念、长叙事场景），改写器的泛化能力尚待验证。

4. **多语言和低资源场景**：论文未涉及非英语提示的改写效果。CoT 推理和 AlignEvaluator 的训练数据语言分布直接影响跨语言迁移能力。

5. **与生成模型协同优化的潜力**：当前框架将 T2I 模型完全冻结，但改写器和生成器的联合微调是否可能带来更大的对齐增益，是一个开放问题。这种协同优化需要在保持模型无关性的优势和追求更高对齐精度之间做出权衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/PromptEnhancer_Taming_Your_Rewriter_for_Text_to_Image_Generation_via_Fine_Grained_Reward.pdf]]
