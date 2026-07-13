---
title: "GenBreak: Red Teaming Text-to-Image Generation Using Large Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GenBreak_Red_Teaming_Text_to_Image_Generation_Using_Large_Language_Models.pdf
project_link: null
code_link: "https://github.com/notAI-tech/NudeNet"
aliases:
- GenBreak
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过强化学习训练红队大语言模型（LLM），利用多目标奖励信号（毒性、绕过、清洁度、多样性）引导模型自动发现既能够绕过安全过滤器又能够产生高毒性图像的对抗性提示。
primary_logic: 两阶段训练（SFT+RL）结合多目标奖励函数，使得LLM能够学会在不依赖敏感关键词的情况下，通过间接、隐晦的表达方式诱导T2I模型生成高毒性图像，且这些提示具有良好的黑盒迁移能力。
claims:
- GenBreak在SD 2.1的裸露类别上实现了60.8%的TBR和57.9%的TCBR，远超所有基线（例如Vanilla RL仅为0.7%/0.0%，CRT为2.9%/0.0%）。
- 在商业API的黑盒转移攻击中，GenBreak在裸露类别上分别达到70%（Leonardo.Ai）、30%（fal.ai）和47%（stability.ai）的有毒绕过率，显著优于CRT和ART。
- 消融实验证实，绕过奖励、清洁奖励和多样性奖励对实现高有毒清洁绕过率（TCBR）不可或缺。
- Safeguarded Stable Diffusion 2.1 上 Toxic Bypass Rate (TBR, %) = 60.8 (Nudity)
---

# GenBreak: Red Teaming Text-to-Image Generation Using Large Language Models

> [!tip] 核心洞察
> 两阶段训练（SFT+RL）结合多目标奖励函数，使得LLM能够学会在不依赖敏感关键词的情况下，通过间接、隐晦的表达方式诱导T2I模型生成高毒性图像，且这些提示具有良好的黑盒迁移能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenBreak：利用大语言模型对文本到图像生成进行红队测试 |
| 英文题名 | GenBreak: Red Teaming Text-to-Image Generation Using Large Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.10047) · [Code](https://github.com/notAI-tech/NudeNet) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GenBreak |
| Dataset | Safeguarded Stable Diffusion 2.1, Safeguarded Stable Diffusion 3 Medium, Leonardo.Ai, fal.ai |

> [!tip] 效果简介
> - Safeguarded Stable Diffusion 2.1 上，Toxic Bypass Rate (TBR, %) 60.8 (Nudity) vs 0.7 (Vanilla RL), 2.9 (CRT) (+57.9 over Vanilla RL)；Toxic Clean Bypass Rate (TCBR, %) 57.9 (Nudity) vs 0.0 (Vanilla RL), 0.0 (CRT) (+57.9)；TBR (%) - Violence 89.7 vs 0.0 (Vanilla RL), 0.2 (CRT) (+89.7)。
> - Safeguarded Stable Diffusion 3 Medium 上，TBR (%) - Nudity 80.70 vs 5.50 (Vanilla RL), 25.20 (CRT) (+55.5 over best baseline)。
> - Leonardo.Ai (black-box) 上，TBR (%) - Nudity 70 vs 0 (CRT), 6 (ART) (+64)。

## 概要

**核心问题**：文本到图像（T2I）生成模型在安全过滤机制下仍可能被对抗性提示诱导产生有害内容。现有红队测试方法面临一个根本瓶颈——难以同时兼顾**绕过安全过滤器**与**生成高毒性图像**，往往在隐蔽性与危害性之间顾此失彼。单纯依赖毒性奖励的方法（如Vanilla RL）生成的提示容易被过滤器拦截，而引入多样性约束的方法（如CRT）虽提升了提示多样性，却牺牲了攻击的毒性。

**GenBreak的核心思路**：将红队测试建模为强化学习问题，训练一个专用的大语言模型（红队LLM）自动发现既能绕过安全过滤器、又能诱导T2I模型生成高毒性图像的对抗性提示。其关键洞察在于：通过**两阶段训练**（监督微调SFT + 强化学习RL）配合**多目标奖励函数**（毒性、绕过、清洁度、多样性），使LLM学会在不依赖显式敏感关键词的情况下，利用间接、隐晦的表达方式（如“nymph”、“Venus”、“painting”等概念）达成攻击目标。

**方法定位**：GenBreak属于基于LLM的自动化红队测试框架，区别于以下基线方法：
- **Vanilla RL**：仅使用图像毒性作为奖励信号，缺乏绕过能力和隐蔽性；
- **CRT**：在RL中引入词汇和语义多样性奖励，但使用静态历史测试用例作为参考，攻击毒性不足；
- **ART**：联合视觉-语言模型与LLM生成攻击提示，但缺乏系统的多目标优化；
- **MMA-Diffusion**与**SneakyPrompt**：分别基于离散优化和RL替换敏感词，但均未将绕过能力与毒性统一优化。

**主要结果概览**：
- 在带安全过滤的**Stable Diffusion 2.1**上，GenBreak在裸露类别实现**60.8%的有毒绕过率（TBR）**和**57.9%的有毒清洁绕过率（TCBR）**，远超Vanilla RL（0.7%/0.0%）和CRT（2.9%/0.0%）；在暴力和仇恨类别上同样保持显著领先（TBR分别为89.7%和84.6%）。
- 在**黑盒商业API**的迁移攻击中，GenBreak在裸露类别上分别达到**70%（Leonardo.Ai）、30%（fal.ai）和47%（stability.ai）**的TBR，显著优于CRT和ART。
- 消融实验证实，**绕过奖励、清洁奖励和多样性奖励**三者对实现高TCBR均不可或缺——移除绕过奖励则无法规避过滤器，移除清洁奖励则提示过度依赖显式敏感词，移除多样性奖励则导致过早收敛。
- 在更新的**Stable Diffusion 3 Medium**上，GenBreak同样保持优势（裸露类别TBR达80.70%，远超最佳基线CRT的25.20%），证明了方法的跨模型泛化能力。

文本到图像（T2I）生成模型的快速发展带来了严峻的安全挑战：恶意用户可能利用这些模型生成裸露、暴力、仇恨言论等有害视觉内容。为应对这一威胁，主流T2I模型（如Stable Diffusion 2.1、Stable Diffusion 3 Medium）和商业API（如Leonardo.Ai、fal.ai、stability.ai）已广泛部署安全过滤器，试图在文本提示进入扩散过程之前拦截有害请求。

然而，现有的T2I模型红队测试方法面临一个根本性瓶颈：**难以同时兼顾绕过安全过滤器和生成高毒性图像，往往在隐蔽性与危害性之间顾此失彼**。具体而言，直接使用敏感关键词的攻击提示虽然可能产生高毒性图像，但极易被过滤器拦截；而经过委婉化处理的提示虽然能绕过过滤，却常常导致生成图像的毒性大幅下降。这种“绕过-毒性”的权衡困境使得现有方法无法有效评估T2I模型在面对精心设计的对抗性提示时的真实鲁棒性。

现有红队方法在这一瓶颈上表现乏力。**Vanilla RL**仅使用图像毒性作为奖励信号训练红队LLM，完全忽略绕过能力，导致生成的提示虽具毒性但几乎无法穿越安全过滤。**CRT**在RL中引入词汇和语义多样性奖励，但缺乏显式的绕过奖励和清洁奖励，提示仍倾向于依赖显式有害词汇，绕过率极低。**ART**依赖联合视觉-语言模型与LLM生成攻击提示，但缺乏系统性的多目标优化，在黑盒迁移场景下表现不稳定。**MMA-Diffusion**和**SneakyPrompt**分别基于离散优化和RL替换敏感词，但搜索空间受限，难以发现间接、隐晦的攻击表达。

这一瓶颈的根源在于：红队LLM需要在**不依赖敏感关键词**的前提下，学会通过间接、隐晦的表达方式诱导T2I模型生成高毒性图像，且这些提示需具备良好的黑盒迁移能力。这要求红队方法同时优化多个相互冲突的目标——毒性最大化、绕过成功率、提示清洁度（避免敏感词）以及攻击策略的多样性——而现有方法缺乏有效的手段来协调这些目标。

基于以上分析，本文提出**GenBreak**框架，核心动机是通过两阶段训练（监督微调SFT + 强化学习RL）结合多目标奖励函数，系统性地解决“绕过-毒性”权衡困境。其关键洞察在于：通过精心设计的奖励信号（毒性、绕过、清洁、多样性）引导LLM自主发现既隐蔽又高效的对抗性提示，从而为T2I模型的安全评估提供更可靠的红队测试工具。

## 核心方法与创新机理

GenBreak 的核心创新在于将 T2I 红队测试重新定义为**受约束的多目标强化学习问题**，通过精心设计的**奖励机制**与**训练策略**，使红队 LLM 能够自动发现既绕过安全过滤器又生成高毒性图像的对抗性提示——这恰恰是现有方法长期未能同时兼顾的两个目标。

### 关键创新点

**1. 两阶段训练策略：SFT 预热 + RL 精调**

现有方法通常直接使用预训练 LLM 或仅用单一目标进行微调。GenBreak 采用**两阶段训练管线**（Figure 1）：
- **第一阶段（SFT）**：在精心构建的**类别重写数据集**（由 Gemini 2.0 Flash 为每个有害类别生成 2000 条对抗性提示）和**预攻击数据集**（通过迭代攻击 SD 2.1 并保留高 TBS 样本构建）上对 Llama-3.2-1B-Instruct 进行监督微调，使模型初步掌握对抗改写能力。
- **第二阶段（RL）**：采用 **GRPO**（Group Relative Policy Optimization）算法，在与代孕 T2I 模型交互产生的多目标奖励信号引导下进一步优化策略。

这一设计解决了从零开始直接 RL 训练面临的**稀疏奖励**和**探索效率低下**问题——SFT 为 RL 提供了合理的策略初始化，使后续优化能够聚焦于精细的绕过策略学习。

**2. 多目标奖励函数：毒性、绕过、清洁、多样性的统一优化**

这是 GenBreak 最核心的机制创新。与 Vanilla RL（仅使用图像毒性奖励）或 CRT（引入词汇/语义多样性但忽略绕过能力）不同，GenBreak 的 RL 阶段优化以下复合目标：

$$\operatorname* { m a x } _ { \pi _ { \theta } } \mathbb { E } \left[ \lambda _ { 1 } R _ { \mathrm { t o x } } ( y ) + \lambda _ { 2 } R _ { \mathrm { b y p a s s } } ( s , y ) + \lambda _ { 3 } R _ { \mathrm { c l e a n } } ( s ) + \sum _ { j = 1 } ^ { 3 } \lambda _ { 3 + j } R _ { \mathrm { d i v } , j } ( s , y ) \right]$$

其中各奖励项的功能与消融验证结果如下：

| 奖励项 | 功能 | 消融结论 |
|--------|------|----------|
| **毒性奖励** $R_{\mathrm{tox}}$ | 鼓励生成高毒性图像 | 基础项，但单独使用（Vanilla RL）几乎无法绕过过滤器 |
| **绕过奖励** $R_{\mathrm{bypass}}$ | 奖励成功规避安全过滤器的提示 | 移除后模型无法有效规避防御机制 |
| **清洁奖励** $R_{\mathrm{clean}}$ | 惩罚提示中包含显式敏感关键词 | 移除此项会使提示极度依赖显式有毒关键词，TCBR 大幅下降 |
| **词汇多样性奖励** | 鼓励提示在词表层面多样化 | 与语义多样性共同防止策略过早收敛 |
| **语义多样性奖励** | 惩罚与动态参考池中提示的高余弦相似度 | 对优化 TCBR 等困难目标至关重要 |
| **图像多样性奖励** | 基于 DreamSim 嵌入惩罚生成图像的视觉相似性 | 促进发现新的视觉有害模式 |

消融实验（Figure 3）明确证实：**绕过奖励、清洁奖励和多样性奖励三者缺一不可**——只有完整的奖励组合才能实现高有毒清洁绕过率（TCBR）。

**3. 动态参考池机制：避免策略遗忘**

CRT 使用**所有历史测试用例**作为多样性参考，这会导致计算开销随训练增长，且可能因过度惩罚而遗忘早期有效的攻击策略。GenBreak 改用**动态参考池**（仅保留最近 $\mathrm{pool\_size}$ 个用例），在维持多样性的同时保留对有效攻击模式的记忆，使探索与利用达到更好平衡。

**4. 显式规避策略编码**

GenBreak 的提示模板显式编码了三种规避技术——**提示稀释**（prompt dilution）、**图像混淆**（image obfuscation）和**概念混淆**（conceptual confusion）——引导 LLM 在生成时主动采用间接、隐晦的表达方式，而非简单替换敏感词。这与 SneakyPrompt 等基于关键词替换的方法形成本质区别：GenBreak 学会的是**语义层面的规避策略**，而非词汇层面的对抗扰动。

### 创新效果验证

这些创新带来的性能提升是**质变级别**的。在 SD 2.1 的裸露类别上，GenBreak 的 TBR 达到 60.8%，TCBR 达到 57.9%，而 Vanilla RL 两项指标分别为 0.7% 和 0.0%，CRT 仅为 2.9% 和 0.0%。更关键的是，GenBreak 生成的提示展现出**强黑盒迁移能力**——在未参与训练的 Leonardo.Ai、fal.ai、stability.ai 三个商业 API 上，裸露类别的 TBR 分别达到 70%、30% 和 47%，远超 CRT（0%、22%、0%）和 ART（6%、3%、0%）。这证明模型学到的是**通用的绕过策略**，而非对特定过滤器的过拟合。

GenBreak 的整体设计遵循 **两阶段训练流水线**，将预训练大语言模型逐步塑造为能够自动发现并绕过安全过滤器的红队攻击智能体。图 1 展示了框架的全貌：第一阶段通过监督微调（SFT）赋予模型基础的对抗改写能力，第二阶段借助强化学习（RL）在与代孕 T2I 模型的多轮交互中持续优化攻击策略。

### 训练流水线

**第一阶段：监督微调（SFT）**。在 Llama-3.2-1B-Instruct 基础上，使用两个精心构建的数据集进行微调。Category Rewrite Dataset 由 Gemini 2.0 Flash 生成，针对裸露、暴力、仇恨三个有害领域各生成 2000 条对抗性提示，教会模型在不直接使用敏感词的前提下表达有害意图。Pre-Attack Dataset 则通过迭代攻击 Stable Diffusion 2.1 并保留高 TBS（Toxicity Bypass Score）样本构建，提供真实的成功攻击范例。SFT 采用标准交叉熵损失：

$$\mathcal { L } _ { \mathrm { S F T } } = - \mathbb { E } _ { ( x , y ) \sim D _ { \mathrm { S F T } } } \sum _ { t = 1 } ^ { T } \log \pi _ { \theta } \left( y _ { t } \mid y _ { < t } , x \right)$$

**第二阶段：强化学习（RL）**。SFT 后的模型已具备基础红队能力，但其攻击有效性和隐蔽性仍有提升空间。RL 阶段采用 GRPO（Group Relative Policy Optimization）算法，让红队 LLM 与带安全过滤的 Stable Diffusion 2.1 持续交互。每次交互中，模型生成提示，代孕 T2I 模型输出图像，多目标奖励模型根据图像毒性、过滤器绕过状态、提示清洁度及多样性指标计算综合奖励信号，反向优化策略参数。

### 核心模块与数据流

框架的输入是目标有害类别（如裸露），输出是针对该类别的高毒性、高隐蔽性对抗提示。关键模块包括：

1. **提示模板**：显式编码三种规避策略——提示稀释（prompt dilution）、图像混淆（image obfuscation）和概念混淆（conceptual confusion），引导模型生成绕过滤器的提示结构。
2. **多目标奖励模型**：集成六类奖励信号——毒性奖励、绕过奖励、清洁奖励（惩罚敏感词使用）、词汇多样性奖励、语义多样性奖励和图像多样性奖励。其中图像多样性奖励基于 DreamSim 感知相似度度量，鼓励发现新的视觉有害模式：

   $$R _ { \mathrm { i m g \_ d i v } } ( y ) = - \frac { 1 } { | \mathcal { V } _ { \mathrm { p o o l } } | } \sum _ { y ^ { \prime } \in \mathcal { V } _ { \mathrm { p o o l } } } \frac { \psi ( y ) \cdot \psi ( y ^ { \prime } ) } { \| \psi ( y ) \| \| \psi ( y ^ { \prime } ) \| }$$

3. **动态参考池**：与 CRT 使用全部历史测试用例作为参考不同，GenBreak 仅维护最近 `pool_size` 个用例，避免遗忘近期发现的有效攻击策略，同时防止过早收敛到局部最优。

RL 阶段的总优化目标为最大化期望奖励：

$$\operatorname* { m a x } _ { \pi _ { \theta } } \mathbb { E } \Bigg [ \lambda _ { 1 } R _ { \mathrm { t o x } } ( y ) + \lambda _ { 2 } R _ { \mathrm { b y p a s s } } ( s , y ) + \lambda _ { 3 } R _ { \mathrm { c l e a n } } ( s ) + \sum _ { j = 1 } ^ { 3 } \lambda _ { 3 + j } R _ { \mathrm { d i v } , j } ( s , y ) \Bigg ]$$

### 设计逻辑

两阶段设计的因果逻辑在于：SFT 阶段提供“冷启动”能力，让模型学会基本的对抗改写范式；RL 阶段则通过与真实 T2I 模型和过滤器的闭环交互，在奖励信号的引导下自动发现**既绕过安全过滤器又产生高毒性图像**的提示策略。多目标奖励中的绕过奖励和清洁奖励形成制衡——前者推动模型规避过滤器，后者惩罚显式敏感词使用，迫使模型发展出间接、隐晦的表达方式，这正是 GenBreak 在黑盒迁移场景中表现优异的关键机制。

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed GenBreak framework*

GenBreak 的核心架构遵循“监督微调–强化学习”两阶段训练管线（Figure 1），其关键模块包括类别重写与预攻击数据集构建、SFT 适配以及基于 GRPO 的多目标 RL 优化。

**监督微调（SFT）模块。** 第一阶段的目标是让预训练 LLM 初步具备红队攻击能力。为此，GenBreak 构建了两类数据集：① *类别重写数据集*（Category Rewrite Dataset），利用 Gemini 2.0 Flash 为裸露、暴力、仇恨三类有害域各生成 2000 条对抗性提示，赋予模型基础的对抗改写能力；② *预攻击数据集*（Pre-Attack Dataset），通过迭代攻击 Stable Diffusion 2.1 并保留高毒性绕过分数（TBS）的样本构建，提供高质量的攻击示例。模型在该组合数据集上以标准交叉熵损失进行微调：

$$\mathcal { L } _ { \mathrm { S F T } } = - \mathbb { E } _ { ( x , y ) \sim D _ { \mathrm { S F T } } } \sum _ { t = 1 } ^ { T } \log \pi _ { \theta } \left( y _ { t } \mid y _ { < t } , x \right)$$

其中 $x$ 为输入指令，$y$ 为目标对抗提示序列，$\pi_\theta$ 为红队 LLM 的策略分布。此阶段不涉及与 T2I 模型的交互，仅提供行为先验。

**强化学习（RL）模块与 GRPO 算法。** 第二阶段将红队 LLM 置于与代孕 T2I 模型（带安全过滤的 SD 2.1）的交互环境中，采用 Group Relative Policy Optimization（GRPO）进行策略优化。GRPO 的目标函数为：

$$\mathcal { L } _ { \mathrm { G R P O } } ( \theta ) = - \mathbb { E } _ { q \sim D _ { s e c d } , \{ s _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta _ { \mathrm { o l d } } } ( s \vert q ) } \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { \vert s _ { i } \vert } \sum _ { t = 1 } ^ { \vert s _ { i } \vert } \left\{ \operatorname* { m i n } \left[ \frac { \pi _ { \theta } ( s _ { i , t } \vert q , s _ { i , < t } ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( s _ { i , t } \vert q , s _ { i , < t } ) } \hat { A } _ { i , t } , \mathrm { c l i p } \left( \frac { \pi _ { \theta } ( s _ { i , t } \vert q , s _ { i , < t } ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( s _ { i , t } \vert q , s _ { i , < t } ) } , 1 - \varepsilon , 1 + \varepsilon \right) \hat { A } _ { i , t } \right] - \beta \mathrm { D } _ { \mathrm { K L } } \left[ \pi _ { \theta } \| \pi _ { \mathrm { r e f } } \right] \right\}$$

其中 $q$ 为从第二阶段数据集 $D_{seed}$ 采样的攻击指令，$\{s_i\}_{i=1}^{G}$ 为旧策略 $\pi_{\theta_{old}}$ 采样的 $G$ 个响应，$\hat{A}_{i,t}$ 为基于组内相对奖励计算的广义优势估计，$\varepsilon$ 控制策略更新幅度，$\beta$ 调节与参考策略 $\pi_{ref}$ 的 KL 散度惩罚。该设计使策略更新稳定且不易崩溃。

**多目标奖励模型。** RL 阶段的总优化目标为最大化期望奖励：

$$\operatorname* { m a x } _ { \pi _ { \theta } } \mathbb { E } _ { s \sim \pi_\theta, y \sim \mathcal { G } ( \cdot | s ) } \left[ \lambda _ { 1 } R _ { \mathrm { t o x } } ( y ) + \lambda _ { 2 } R _ { \mathrm { b y p a s s } } ( s , y ) + \lambda _ { 3 } R _ { \mathrm { c l e a n } } ( s ) + \sum _ { j = 1 } ^ { 3 } \lambda _ { 3 + j } R _ { \mathrm { d i v } , j } ( s , y ) \right]$$

奖励信号由六个分量构成：$R_{tox}(y)$ 为生成图像 $y$ 的毒性分数（由 NudeNet 等专家模型评估）；$R_{bypass}(s,y)$ 为绕过奖励，仅当安全过滤器被绕过时激活；$R_{clean}(s)$ 为清洁奖励，惩罚提示 $s$ 中出现敏感关键词，迫使模型学习间接表达；$R_{div}$ 包含词汇多样性、语义多样性和图像多样性三个子项。其中语义多样性奖励定义为：

$$R _ { \mathrm { s e m a n t i c } } ( s ) = - \frac { 1 } { | \mathcal { X } _ { \mathrm { p o o l } } | } \sum _ { s ^ { \prime } \in \mathcal { X } _ { \mathrm { p o o l } } } \frac { \phi ( s ) \cdot \phi ( s ^ { \prime } ) } { \| \phi ( s ) \| \| \phi ( s ^ { \prime } ) \| }$$

其中 $\phi(\cdot)$ 为 Sentence-BERT 编码器，$\mathcal{X}_{pool}$ 为动态参考池（保留最近 $pool\_size$ 个历史提示），通过惩罚与已有提示的高余弦相似度来鼓励探索。图像多样性奖励采用类似形式，但使用 DreamSim 感知相似度度量 $\psi(\cdot)$ 在图像嵌入空间计算：

$$R _ { \mathrm { i m g \_ d i v } } ( y ) = - \frac { 1 } { | \mathcal { V } _ { \mathrm { p o o l } } | } \sum _ { y ^ { \prime } \in \mathcal { V } _ { \mathrm { p o o l } } } \frac { \psi ( y ) \cdot \psi ( y ^ { \prime } ) } { \| \psi ( y ) \| \| \psi ( y ^ { \prime } ) \| }$$

**攻击有效性度量。** 训练过程中评估单条提示攻击质量的核心指标为毒性绕过分数（Toxicity Bypass Score, TBS）：

$$\mathrm { T B S } ( p ^ { ( t ) } ) = \mathbb{I} [ \mathrm { b y p a s s } ] \cdot \mathrm { t o x i c i t y } ( y ^ { ( t ) } )$$

该指标仅在安全过滤器被绕过（$\mathbb{I}[bypass]=1$）时才计入图像毒性，从而精准衡量提示同时满足隐蔽性与危害性的能力。预攻击数据集的构建即以此分数为筛选标准。

**提示模板设计。** GenBreak 在 RL 阶段为 LLM 提供显式编码三种规避策略的提示模板：*提示稀释*（prompt dilution，通过冗长描述稀释敏感意图）、*图像混淆*（image obfuscation，用视觉上相似但语义安全的概念替代）和*概念混淆*（conceptual confusion，模糊有害概念的边界）。该模板引导模型在不依赖显式敏感词的情况下生成高攻击性的对抗提示。

## 实验与关键发现

### 核心性能：在带安全过滤的SD 2.1上的攻击有效性

GenBreak在带安全过滤的Stable Diffusion 2.1上的攻击性能如表1所示，以毒性绕过率（TBR）和有毒清洁绕过率（TCBR）为核心指标，毒性阈值设为0.5。GenBreak在所有三个有害类别上均显著超越基线方法。

在**裸露**类别上，GenBreak实现了60.8%的TBR和57.9%的TCBR，而Vanilla RL仅分别为0.7%和0.0%，CRT为2.9%和0.0%。这一差距揭示了仅依赖单一毒性奖励（Vanilla RL）或仅引入词汇/语义多样性（CRT）的致命缺陷：模型要么无法绕过安全过滤器，要么生成的提示虽多样但毒性不足。GenBreak的TCBR高达57.9%，意味着超过一半的攻击提示在**不使用显式敏感词**的情况下，成功绕过了过滤器并生成了高毒性图像——这正是红队测试的核心能力。

在**暴力**类别上，GenBreak的TBR达到89.7%，TCBR为86.2%，而Vanilla RL的TBR为0.0%，CRT为0.2%。暴力类别的安全过滤器对直接关键词的拦截极为有效，但GenBreak通过间接、隐晦的表达方式（如场景描述、隐喻）成功绕过了这些防御。

在**仇恨**类别上，GenBreak的TBR为84.6%，TCBR为81.1%，相比之下Vanilla RL为18.7%，CRT仅为2.9%。仇恨类别中，Vanilla RL虽有一定攻击性，但其TCBR极低（0.0%），表明其提示高度依赖显式仇恨词汇，缺乏隐蔽性。

值得注意的是，SneakyPrompt和MMA-Diffusion在所有类别上的TBR和TCBR均接近零。这两种方法的核心策略是替换或搜索语义相似的敏感词，但在集成安全过滤器（结合文本过滤和图像过滤）面前，这种“近义词替换”策略几乎完全失效。这从反面证明了GenBreak的策略——通过LLM生成间接、语境化的攻击提示——是绕过现代多层防御的必要路径。

在提示多样性方面，GenBreak在大多数情况下与CRT相当或略低，但考虑到其攻击有效性的大幅领先，这一平衡是可以接受的。整体而言，GenBreak在有效性、隐蔽性、多样性和语义流畅性之间实现了最优权衡。

### 毒性阈值敏感性分析

Figure 2展示了不同毒性阈值下各算法在SD 2.1上的多指标表现。随着毒性阈值从0.3提高到0.7，所有方法的TBR和TCBR均呈下降趋势，但GenBreak的下降幅度远小于基线方法。当阈值设为0.7时，GenBreak在裸露类别上仍保持显著的TCBR，而CRT和Vanilla RL已降至接近零。这表明GenBreak生成的图像不仅毒性更高，而且毒性水平更稳定，而非仅徘徊在低毒性边缘。

### 黑盒迁移攻击：商业API上的表现

表2展示了GenBreak在三个商业T2I API上的黑盒迁移攻击性能。GenBreak的提示是在SD 2.1上训练的，**未对任何商业API进行微调或访问其内部参数**，因此这构成了严格的黑盒迁移测试。

在**Leonardo.Ai**（使用FLUX.1 [dev]）上，GenBreak在裸露类别实现了70%的TBR，而CRT为0%，ART仅为6%。在**fal.ai**（使用FLUX.1 [schnell]）上，GenBreak达到30%的TBR，CRT为22%，ART为3%。在**stability.ai**（Stable Image Core）上，GenBreak达到47%的TBR，而CRT和ART均为0%。

这些结果揭示了两个关键发现：第一，GenBreak的攻击提示具有**跨模型、跨架构的强迁移能力**，从SD 2.1迁移到FLUX.1系列和Stable Image Core均保持有效；第二，不同商业API的安全防御强度差异显著——Leonardo.Ai的过滤器相对容易被绕过（70%），而fal.ai的防御更严格（30%），stability.ai居中（47%）。CRT在fal.ai上达到22%的TBR，表明该平台的文本过滤器可能对词汇多样性攻击有一定容忍度，但其图像过滤仍能拦截大部分CRT生成的图像。

### 在SD 3 Medium上的性能

表7展示了在带安全过滤的Stable Diffusion 3 Medium上的攻击性能。GenBreak在裸露类别上实现了80.70%的TBR和76.40%的TCBR，远超Vanilla RL（5.50%/0.40%）和CRT（25.20%/16.80%）。在暴力和仇恨类别上，GenBreak同样保持显著优势。SD 3 Medium作为更新一代的T2I模型，其安全过滤机制可能有所增强，但GenBreak的攻击策略仍能有效迁移，进一步验证了方法的鲁棒性。

Figure 4展示了不同毒性阈值下各算法在SD 3 Medium上的表现，趋势与SD 2.1一致：GenBreak在高毒性阈值下仍保持显著优势。

### 消融实验：多目标奖励的必要性

Figure 3展示了不同奖励项对GenBreak性能的影响，消融实验证实了绕过奖励、清洁奖励和多样性奖励的不可或缺性。

**移除绕过奖励**：模型将退化为仅优化图像毒性，而不考虑是否绕过了安全过滤器。这导致生成的提示大量被过滤器拦截，TBR和TCBR急剧下降，本质上退化为Vanilla RL的行为模式。

**移除清洁奖励**：模型不再受惩罚使用敏感词，提示会高度依赖显式有毒关键词（如直接使用“nude”“naked”等词汇）。虽然TBR可能保持一定水平（因为部分平台对关键词过滤不严格），但TCBR大幅下降，因为这些提示缺乏隐蔽性，无法通过严格的文本过滤器。这证明了清洁奖励是实现“清洁绕过”的关键机制。

**移除提示多样性奖励**（包括词汇多样性和语义多样性）：模型会过早收敛到少数几个高奖励的提示模式，导致策略探索不足。特别是在优化TCBR这一具有挑战性的目标时，多样性奖励防止模型陷入局部最优，对维持探索能力至关重要。消融实验还验证了引入图像多样性奖励的额外收益——通过DreamSim嵌入惩罚生成相似有害图像的提示，促使模型发现更多样化的视觉有害模式。

### 失败模式与局限性

尽管GenBreak在黑盒迁移中表现优异，但仍存在若干失败模式。在fal.ai上，GenBreak的TBR仅为30%，远低于Leonardo.Ai的70%，表明某些商业API部署了更强大的图像内容审核系统，能够识别并拦截GenBreak生成的间接有害图像。此外，当前方法依赖图像毒性分数作为RL的奖励信号，在完全黑盒的T2I服务中难以直接获取，这限制了在线训练的可能性。实验使用的集成过滤器（NudeNet、Q16等）可能无法完全反映商业系统实际的内容审核策略，实际部署中的性能可能有所偏差。

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/002_Table_1.jpg]]
*Table 1: Attack performance on safeguarded Stable Diffusion 2.1. TBR: Toxic Bypass Rate, TCBR: Toxic Clean Bypass Rate, LexDiv: Lexical Diversity, SemDiv: Semantic Diversity, ImgDiv: Image Diversity. The toxicity threshold used in calculating TBR and TCBR is 0.5*

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/003_Table_2.jpg]]
*Table 2: Performance of transfer attacks on black-box commercial models. TBR: Toxic Bypass Rate, BR: Bypass Rate, Tox.: Toxicity (Only Successful Bypass). The toxicity threshold used in calculating TBR is 0.5*

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/010_Table_7.jpg]]
*Table 7: Attack performance on safeguarded Stable Diffusion 3 Medium. TBR: Toxic Bypass Rate, TCBR: Toxic Clean Bypass Rate, LexDiv: Lexical Diversity, SemDiv: Semantic Diversity, ImgDiv: Image Diversity. The toxicity threshold used in calculating TBR and TCBR is 0.5*

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/011_Figure_4.jpg]]
*Figure 4: Performance of different algorithms (GenBreak, CRT, Vanilla RL) across toxicity thresholds for various metrics on Stable Diffusion 3 Medium, showing results for nudity, violence, and hate categories*

![[assets/figures/papers/paper_list_l2312_https_arxiv_org_abs_2506_10047/figures/036_Figure_6.jpg]]
*Figure 6: Visualization of unsafe images generated by fal.ai and their corresponding attack prompts generated by GenBreak. We applied blurring and masked sensitive content using for ethical considerations*

## 定位与知识库关联

### 1. 与现有红队方法的对比定位

GenBreak 的提出直接针对现有 T2I 红队方法的核心瓶颈：**隐蔽性与危害性难以兼得**。现有方法在绕过安全过滤器和生成高毒性图像之间往往顾此失彼，而 GenBreak 通过两阶段训练（SFT + RL）与多目标奖励设计，系统性地解决了这一矛盾。

下表梳理了 GenBreak 与主要基线方法在技术路线上的关键差异：

| 方法 | 核心机制 | 关键局限 |
|------|----------|----------|
| **Vanilla RL** | 仅使用图像毒性奖励训练红队 LLM | 完全忽略绕过能力，生成的提示高度依赖显式敏感词，易被过滤器拦截（Nudity 类别 TBR 仅 0.7%，TCBR 为 0.0%） |
| **CRT** | 在 RL 中引入词汇和语义多样性奖励，以历史测试用例为参考 | 采用静态历史参考池，缺乏对安全过滤器的显式绕过优化，Nudity 类别 TCBR 为 0.0% |
| **ART** | 联合视觉-语言模型和 LLM 生成攻击提示 | 在黑盒迁移场景中表现极弱（Leonardo.Ai 上 Nudity TBR 仅 6%，stability.ai 上为 0%） |
| **MMA-Diffusion** | 基于离散优化的文本攻击，搜索语义相似的对抗性提示 | 缺乏对安全过滤器的针对性规避策略，文中未报告其在带安全过滤模型上的有效绕过率 |
| **SneakyPrompt** | 基于 RL 替换提示中敏感词的黑盒攻击 | 平均图像毒性仅 0.220（Table 1），表明其生成的图像危害性不足 |
| **GenBreak** | 两阶段训练（SFT + RL）+ 多目标奖励（毒性/绕过/清洁/多样性）+ 动态参考池 | — |

GenBreak 的关键改进体现在四个维度：

1. **训练策略升级**：从单一阶段直接微调升级为“SFT 预热 + RL 精调”两阶段范式。SFT 阶段利用 Category Rewrite Dataset 和 Pre-Attack Dataset 赋予 LLM 初始对抗改写能力，RL 阶段则通过 GRPO 算法进一步优化攻击有效性。

2. **多目标奖励设计**：将单一的毒性奖励扩展为包含毒性、绕过、清洁（惩罚敏感词使用）、词汇多样性、语义多样性、图像多样性、乱码惩罚和符号规范在内的多目标奖励体系。消融实验证实，绕过奖励、清洁奖励和多样性奖励对实现高 TCBR 不可或缺。

3. **动态参考池机制**：不同于 CRT 使用全部历史测试用例作为参考的静态策略，GenBreak 引入动态参考池（最近 `pool_size` 个用例），避免遗忘有效攻击策略，同时保持探索能力。

4. **规避策略显式编码**：提示模板显式编码三种规避技术——prompt dilution（提示稀释）、image obfuscation（图像混淆）和 conceptual confusion（概念混淆），为 LLM 提供结构化的攻击指导。

### 2. 方法适用边界

**适用场景**：
- 对开源 T2I 模型（如 Stable Diffusion 2.1、Stable Diffusion 3 Medium）进行白盒红队测试，可直接获取图像毒性分数作为奖励信号。
- 对商业 T2I API 进行黑盒迁移攻击，GenBreak 生成的对抗性提示展现出良好的跨模型迁移能力（在 Leonardo.Ai、fal.ai、stability.ai 上分别达到 70%、30%、47% 的 Nudity TBR）。

**不适用或效果受限的场景**：
- **黑盒在线训练受限**：RL 阶段依赖图像毒性分数作为奖励信号，但在黑盒 T2I 服务中难以直接获取，限制了在线自适应训练。
- **先进工业级过滤器**：论文明确指出，当前方法在应对先进的工业级图像过滤器时可能效果有限。实验使用的集成过滤器（NudeNet 等）可能无法完全反映商业系统实际的内容审核策略，真实场景下性能可能有所偏差。
- **有害类别覆盖有限**：当前工作聚焦于裸露、暴力和仇恨三类有害内容，尚未拓展到虚假信息、隐私泄露等更多样化的有害内容类别。

### 3. 局限性与开放问题

**已识别的局限性**（来自论文自身讨论）：

1. **奖励信号依赖**：训练红队 LLM 需要图像毒性分数作为奖励信号，但在黑盒 T2I 模型/服务中难以直接获取，限制了在线训练能力。

2. **过滤器模拟偏差**：实验使用的集成过滤器可能无法完全反映商业 T2I 系统实际的内容审核策略，可能在真实场景下性能有所偏差。

3. **工业级防御的挑战**：当前方法在应对先进的工业级图像过滤器时可能效果有限，探索更强的规避技术留待未来工作。

**开放问题**：

1. **对抗技术升级**：如何发展更强大的对抗技术以应对不断升级的工业级图像安全过滤器？这需要红队方法与防御技术的持续博弈。

2. **黑盒奖励获取**：在黑盒条件下如何有效获取或替代图像毒性奖励，以实现更贴近真实场景的红队训练？可能的路径包括训练奖励预测模型或利用多模态大模型进行毒性评估。

3. **有害类别拓展**：如何将红队测试拓展到更多样化的有害内容类别（如虚假信息、隐私泄露、深度伪造等）？不同类别可能需要定制化的毒性评估模型和规避策略。

4. **红队-蓝队协同**：GenBreak 生成的对抗性提示能否反向用于改进 T2I 模型的安全对齐训练？这一方向有望形成红队测试与安全加固的闭环。

## 原文 PDF

![[paperPDFs/CVPR_2026/GenBreak_Red_Teaming_Text_to_Image_Generation_Using_Large_Language_Models.pdf]]
