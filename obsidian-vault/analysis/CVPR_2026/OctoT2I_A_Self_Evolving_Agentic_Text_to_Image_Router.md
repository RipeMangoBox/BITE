---
title: "OctoT2I: A Self-Evolving Agentic Text-to-Image Router"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OctoT2I_A_Self_Evolving_Agentic_Text_to_Image_Router.pdf
project_link: null
code_link: "https://github.com/JaxJiang2642081986/OctoT2I"
aliases:
- OctoT2I
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过自进化机制自主构建工具知识库，并结合有状态的动态多轮路由策略，将生成质量与推理成本联合优化，从而突破上述瓶颈。
primary_logic: 将 T2I 模型选择抽象为约束优化问题（在满足质量阈值下最小化推理成本），利用自进化探索自动发现每个工具的能力边界，并通过基于知识与记忆的“推理-执行-反思”循环实现自适应路由，无需任何外部监督。
claims:
- 在 GenEval 基准上，OctoT2I 以 0.96 的总体得分显著超越此前最优方法 Flow-GRPO (0.93) 及其他智能体方法。
- OctoT2I 相较 Flow-GRPO 实现 90.3% 推理加速和 56.6% 能效提升，证明了其性能-效率平衡优势。
- 自进化知识消融显示，OctoT2I 的自进化知识（0.96）明显优于基于 GPT 内部知识（0.85）和手工先验（0.93）的替代方案。
- 决策策略消融表明，知识驱动的决策相比随机工具选择在 T2ICompBench++ 上平均得分提升了 0.23，证实了路由策略的有效性。
---

# OctoT2I: A Self-Evolving Agentic Text-to-Image Router

> [!tip] 核心洞察
> 将 T2I 模型选择抽象为约束优化问题（在满足质量阈值下最小化推理成本），利用自进化探索自动发现每个工具的能力边界，并通过基于知识与记忆的“推理-执行-反思”循环实现自适应路由，无需任何外部监督。

| 字段 | 内容 |
|------|------|
| 中文题名 | OctoT2I：自进化的智能体文本到图像路由框架 |
| 英文题名 | OctoT2I: A Self-Evolving Agentic Text-to-Image Router |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang_OctoT2I_A_Self-Evolving_Agentic_Text-to-Image_Router_CVPR_2026_paper.html) · [Code](https://github.com/JaxJiang2642081986/OctoT2I) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | OctoT2I |
| Dataset | GenEval, T2ICompBench++, User Study |

> [!tip] 效果简介
> - GenEval 上，Overall↑ 0.96 vs 0.93 (Flow-GRPO) (+0.03)；推理加速 90.3% vs Flow-GRPO (—)；能效提升 56.6% vs Flow-GRPO (—)。
> - T2ICompBench++ 上，Average↑ 0.6618 vs 0.6556 (Flow-GRPO, previous best) (+0.0062)。
> - User Study 上，Voting Rate (%) 70.4 vs 29.6 (ChatGen) (+40.8)。

## 概述

**核心问题**：现有智能体文本到图像（T2I）方法在工具知识获取、决策灵活性与推理效率之间存在三重瓶颈——依赖手工先验或昂贵人工标注构建工具知识、采用静态单轮路由策略、仅追求生成质量而忽略成本，导致系统难以在性能与效率之间取得平衡。

**核心方法**：OctoT2I 提出一种自进化的智能体路由框架，将 T2I 模型选择形式化为约束优化问题（在满足质量阈值下最小化推理成本），并通过三个关键设计突破上述瓶颈：(1) 自进化机制自主构建工具知识库，无需外部监督；(2) 有状态的多轮“推理-执行-反思”循环实现自适应路由；(3) 生成质量与推理效率联合优化。

**核心结论**：
- 在 GenEval 基准上，OctoT2I 以 **0.96** 总体得分超越此前最优方法 **Flow-GRPO**（Liu et al., arXiv 2025）的 0.93，以及 FLUX.1-dev（0.82）、GenArtist（Wang et al., NeurIPS 2024，0.82）、ChatGen（Jia et al., arXiv 2024，0.82）等智能体方法。
- 相较 Flow-GRPO，OctoT2I 实现 **90.3%** 推理加速和 **56.6%** 能效提升，验证了性能-效率联合优化的有效性。
- 自进化知识消融显示，自进化构建的知识（0.96）显著优于基于 GPT 内部知识（0.85）和手工先验（0.93）的替代方案；探索空间剪枝策略在保持总体得分不变的同时，将探索提示数减少 70.9%、时间缩短 66.0%。

**方法定位**：OctoT2I 属于智能体 T2I 路由方法，其核心区别于现有工作在于将知识获取从“人工定义”转变为“自进化探索”，将决策从“静态单轮”升级为“有状态多轮”，并将优化目标从“质量优先”拓展为“质量约束下的成本最小化”。该方法与单模型 T2I 系统（如 Flow-GRPO、FLUX.1-dev）和智能体 T2I 系统（如 GenArtist、ChatGen、Idea2Img）均构成正交或替代关系。

## 背景与动机

文本到图像（T2I）生成领域近年来涌现出大量功能各异的模型——从专精于特定风格的小型高效模型，到具备通用生成能力的大型基础模型。然而，面对一个具体的用户提示，如何从众多候选工具中选出“最合适”的那个，仍然是一个悬而未决的挑战。这个问题的本质在于：不同 T2I 模型在能力边界上存在显著差异，单一模型很难在所有类型的提示上同时做到高质量与低成本。

现有智能体 T2I 方法试图通过引入工具选择机制来应对这一挑战，但其方案存在三个根本性瓶颈。**第一，知识获取依赖人工**：此前的智能体方法，如 **GenArtist**（Wang et al., NeurIPS 2024）、**ChatGen**（Jia et al., arXiv 2024）和 **Idea2Img**（Yang et al., arXiv 2023），其工具选择知识要么来自手工设计的先验规则，要么需要昂贵的人工标注数据进行监督微调。这种方式不仅难以规模化，还无法动态适应工具能力的更新。**第二，决策路径单一且静态**：现有方法通常采用单轮、固定的工具分配策略，缺乏根据实时生成反馈进行动态调整的能力，一旦初始选择失误便无法挽回。**第三，优化目标片面**：大多数方法仅以生成质量为唯一追求，完全忽略了推理效率，导致在实际部署中计算成本高昂。

这些瓶颈的共同后果是：现有智能体 T2I 系统在性能与效率之间难以取得令人满意的平衡。以当前最优的单模型方法 **Flow-GRPO**（Liu et al., arXiv 2025）为例，尽管其在 GenEval 基准上达到了 0.93 的总体得分，但其推理成本极高；而更轻量的模型虽然速度快，却在复杂提示（如精确计数、属性绑定）上表现不佳。这一矛盾揭示了一个核心问题：**如何在保证生成质量的前提下，最小化推理成本？**

OctoT2I 正是为回答这一问题而提出的。其核心动机在于将 T2I 工具选择形式化为一个约束优化问题——在满足质量阈值的工具集合中，选择推理成本最低者。这一形式化表述本身并不新鲜，但关键难点在于：每个工具的“质量-成本”画像并非先验已知，而是需要在实际使用中动态获取。OctoT2I 的核心洞察是：**这些画像可以通过智能体自主探索来构建，无需任何外部监督**。基于这一洞察，OctoT2I 设计了一个自进化机制，使智能体能够从零开始定义概念维度、探索工具能力边界，并将所学知识沉淀为可复用的知识库，最终支撑起一个有状态、多轮的自适应路由决策循环。

## 核心创新

OctoT2I 的核心创新在于将文本到图像（T2I）的模型选择问题重新定义为**约束优化问题**，并通过**自进化知识构建**与**有状态动态路由**两大机制联合求解，从而在生成质量与推理效率之间实现突破性平衡。相较于现有方法，OctoT2I 在三个关键维度上实现了范式转变：

### 1. 优化目标的根本转变：从单一质量到质量-效率联合优化

现有智能体 T2I 方法（如 **GenArtist** (Wang et al., NeurIPS 2024)、**ChatGen** (Jia et al., arXiv 2024)）以及单模型方法（如 **Flow-GRPO** (Liu et al., arXiv 2025)）均以最大化生成质量为唯一目标，忽略了不同工具间巨大的推理成本差异。OctoT2I 首次将工具选择形式化为约束优化问题：

$$ \operatorname { t } ^ { * } ( p ) = \underset { \operatorname { t } _ { i } \in \mathcal { T } } { \arg \operatorname* { m i n } } \ \mathrm { c } ( \mathrm { t } _ { i } ) \ \mathrm { s . t . } \ \mathrm { q } ( \mathbf { I } , p ) \geq \theta $$

其核心思想是：在满足预设质量阈值 $\theta$ 的工具子集中，选择推理成本最低者。这一公式化使得系统能够在性能与效率之间显式权衡——当质量要求宽松时优先使用轻量模型（如 sd-turbo），仅对复杂提示调用高成本模型（如 flow-grpo）。实验证明，OctoT2I 在 GenEval 上以 0.96 总体得分超越 Flow-GRPO (0.93) 的同时，实现了 **90.3% 推理加速**和 **56.6% 能效提升**（Table 1, Table 3），验证了联合优化的实际收益。

### 2. 知识获取的范式转变：从手工先验到自进化构建

现有方法的工具知识严重依赖两种不可扩展的途径：**手工先验**（如基于经验为不同模型预设适用场景）或**昂贵的人工标注**（如监督微调所需的海量标注数据）。这些静态知识不仅覆盖不全，还难以适应工具库的动态变化。

OctoT2I 提出的**自进化机制**彻底改变了这一范式。该机制通过 **PSEL 循环**（Propose–Solve–Evaluate–Learn）自主构建工具知识库，无需任何人工监督：

- **Propose**：LLM 自主定义基础概念维度（如风格、颜色、计数），并系统性地探索其组合（幂集 $\mathcal { C } _ { \mathrm { e x p l o r e } } = 2 ^ { D } \setminus \{ \varnothing \}$）。
- **Solve**：针对每个概念组合生成代表性提示，调用候选工具生成图像。
- **Evaluate**：利用 MLLM 提取 yes/no logits 并通过 softmax 计算连续质量分数，以 **Pass@1** 指标评估工具在该子任务上的掌握程度。
- **Learn**：将评估结果记录为结构化知识，包含工具画像与探索记录。

消融实验（Table 4）有力地证明了自进化知识的优越性：OctoT2I 的自进化知识在 GenEval 上达到 0.96，显著优于基于 GPT 内部知识（0.85）和手工先验（0.93）的替代方案。此外，**探索空间剪枝**（ESP）策略通过递归前置原则——仅当工具已掌握某概念组合的所有更简单子任务时，才探索该组合——将探索提示数减少 **70.9%**，时间缩短 **66.0%**，同时保持整体得分不变（Table 6），展示了自进化探索的高效性。

### 3. 决策机制的范式转变：从静态单轮到有状态多轮路由

传统智能体方法采用静态、单轮的决策流程，一旦选择工具便不再调整，无法应对生成失败的情况。OctoT2I 实现了**有状态、多轮的“推理-执行-反思”循环**：

$$ \mathrm { t } _ { r } = \pi ( p , { \mathcal K } , { \mathcal M } _ { r - 1 } ) $$

在第 $r$ 轮，决策策略 $\pi$ 基于用户提示 $p$、长时知识库 $\mathcal{K}$ 和短时工作记忆 $\mathcal{M}_{r-1}$（记录此前轮次的工具选择与评估反馈），通过 LLM 链式思维推理选择工具。生成图像后，评估模块提供连续质量评分；若未达到阈值 $\theta$，系统根据失败信息调整策略进入下一轮，直至满足要求或达到轮次上限。

决策策略消融（Table 5）揭示了这一机制的关键作用：移除知识驱动的决策策略（替换为随机工具选择）导致 T2ICompBench++ 平均得分从 0.6618 骤降至 0.5379（降幅 **0.23**），证实了基于证据的自适应路由远优于无引导的多轮试错。质量阈值 $\theta$ 的消融（Figure 4）进一步表明，$\theta$ 从 0.5 增至 0.9 时性能先升后降、推理时间持续增加，为实际部署中的阈值选择提供了指导。

### 创新总结

OctoT2I 的三项核心创新构成了一个有机整体：约束优化目标为系统提供了明确的性能-效率权衡准则；自进化机制为决策提供了精确、可扩展的工具能力知识；有状态多轮路由则利用这些知识实现自适应工具选择。三者协同作用，使得 OctoT2I 在无需任何外部监督的条件下，同时实现了最优生成质量和最高推理效率。

## 整体框架

OctoT2I 将文本到图像（T2I）的模型选择形式化为一个**约束优化问题**：在满足预设质量阈值的前提下，最小化推理成本。其核心公式为：

$$
\operatorname { t } ^ { * } ( p ) = \underset { \operatorname { t } _ { i } \in \mathcal { T } } { \arg \operatorname* { m i n } } \ \mathrm { c } ( \mathrm { t } _ { i } ) \ \mathrm { s . t . } \ \mathrm { q } ( \mathbf { I } , p ) \geq \theta
$$

其中 $p$ 为用户提示，$\mathcal{T}$ 为可用 T2I 工具集，$\mathrm{c}(\mathrm{t}_i)$ 和 $\mathrm{q}(\mathbf{I}, p)$ 分别表示工具的成本与生成质量。这一形式化将“选哪个模型”从启发式经验提升为可优化的决策目标（见 verified_analysis 中的 causal_knob）。

为实现上述优化，OctoT2I 构建了一个**有状态、多轮的“推理-执行-反思”循环**，其整体架构如 Figure 2 所示，包含推理工作流（上）与自进化机制（下）两大层次。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/003_Figure_2.jpg]]
*Figure 2: The overall architecture of OctoT2I. (Top) Inference Workflow. The agent takes a user prompt and executes a “reason-actreflect” loop: The decision policy leverages its memory and knowledge modules to select an appropriate tool. This tool is then used to generate an image, which is subsequently evaluated to obtain a quality score. The workflow terminates when the score meets the quality threshold or the round limit is reached. (Bottom) Self-Evolving Mechanism. The knowledge module is autonomously and adaptively constructed from scratch. It includes hierarchical high-level tool profiles and exploration records. This construction is driven by the “Propose–Solve–Evaluate–Learn” (PSEL) loop, whi...*

### 推理工作流：Reason-Act-Reflect 循环

推理阶段由四个核心模块协同完成：

1. **知识模块（Knowledge Module）**：存储工具的长时知识，包括工具画像与探索记录，是决策的静态依据。
2. **记忆模块（Memory Module）**：维护当前任务的短时工作记忆 $\mathcal{M}_{r-1}$，记录已尝试的工具、生成图像及评估分数，为多轮路由提供上下文。
3. **决策策略 $\pi$（Decision Policy）**：基于 LLM 的链式思维推理，在第 $r$ 轮根据提示 $p$、知识 $\mathcal{K}$ 和记忆 $\mathcal{M}_{r-1}$ 选择工具 $\mathrm{t}_r$：
   $$
   \mathrm { t } _ { r } = \pi ( p , { \mathcal K } , { \mathcal M } _ { r - 1 } )
   $$
   其内部实现为从满足估计质量阈值 $\hat{\mathrm{q}}(\mathrm{t}_i(p), p) \geq \theta$ 的可行工具集中，选择估计成本 $\hat{\mathrm{c}}(\mathrm{t}_i)$ 最小的工具（见 Eq. (7)）。
4. **评估模块 $q_{\text{eval}}$（Evaluation Module）**：利用 MLLM 提取 “yes/no” 的原始 logits，经 softmax 得到连续质量分数 $s_r$，为决策策略提供量化反馈。

工作流从接收用户提示开始，决策策略依据知识与记忆选择工具；选中的工具生成图像后，评估模块给出质量分数。若分数达到阈值 $\theta$ 或达到轮次上限，循环终止；否则将本轮结果写入记忆，进入下一轮推理。这一闭环使系统能够在性能与效率之间动态平衡。

### 自进化机制：PSEL 循环

知识模块并非依赖手工先验或人工标注，而是通过**自进化机制**从零自主构建。该机制的核心是一个“提议-求解-评估-学习”（Propose–Solve–Evaluate–Learn, PSEL）循环：

- **提议（Propose）**：LLM 自主定义基础概念维度（如风格、颜色、计数），并生成维度组合 $\tau$ 对应的探索提示 $p_\tau$。探索空间为概念维度集合的幂集（去掉空集）：
  $$
  \mathcal { C } _ { \mathrm { e x p l o r e } } = 2 ^ { D } \setminus \{ \varnothing \}
  $$
- **求解（Solve）**：使用待评估工具 $\mathrm{t}_i$ 对 $p_\tau$ 生成图像。
- **评估（Evaluate）**：计算工具的 Pass@1 分数，即单次尝试满足质量阈值的概率估计：
  $$
  \mathrm { P a s s @ 1 } ( p _ { \tau } , \mathrm { t } _ { i } ) = \frac { 1 } { N _ { \mathrm { s o l } } } \sum _ { n = 1 } ^ { N _ { \mathrm { s o l } } } \mathbb { I } ( s _ { \tau , n } \ge \theta )
  $$
- **学习（Learn）**：将评估结果写入知识模块，形成工具在各概念维度组合上的能力边界。

为提高探索效率，OctoT2I 引入**探索空间剪枝（ESP）**策略：仅当工具已掌握某维度组合 $\tau$ 的所有更简单子任务（$\forall \tau' \subset \tau, \tau' \neq \emptyset$，其历史平均 Pass@1 超过 $\theta$）时，才对该组合进行探索。消融实验证实，ESP 在保持 GenEval 总体得分 0.96 不变的前提下，将探索提示数减少 70.9%、时间缩短 66.0%（Table 6）。

### 输入输出流总结

- **输入**：用户自然语言提示 $p$。
- **知识准备**：自进化机制离线构建工具知识库 $\mathcal{K}$。
- **推理过程**：决策策略 $\pi$ 以 $p$、$\mathcal{K}$ 和动态记忆 $\mathcal{M}$ 为输入，输出选定的工具 $\mathrm{t}_r$；工具生成图像 $\mathbf{I}_r$；评估模块输出质量分数 $s_r$。
- **输出**：满足质量阈值（或达到轮次上限）的最终图像。

这一设计将知识获取、决策推理与效率优化统一在一个无需外部监督的框架内，使 OctoT2I 能够在 GenEval 上以 0.96 总体得分超越 Flow-GRPO（0.93），同时实现 90.3% 的推理加速和 56.6% 的能效提升（见 verified_analysis 中的 decisive_evidence）。

### 补充图表

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/002_Figure_1.jpg]]
*Figure 1: The core advantages of OctoT2I in performance, decision-making, and knowledge acquisition. (a) OctoT2I (Ours) achieves an exceptional performance-efficiency balance on GenEval. (b) This superior performance stems from its intelligent, evidence-based decisions, which route each user prompt to the most suitable T2I model. For example, it selects the most efficient tool (sd-turbo) for “a photo of a snowboard” while allocating the most justifiable tool (flow-grpo) for “Generate an image containing 5 hamburgers”. (c, d, e) This intelligent decision-making capability is enabled by our novel (e) self-evolving mechanism, which overcomes the limitations of previous (c) handcrafted priors or (d) cost...*

## 核心模块与公式推导

### 问题形式化：约束优化视角

OctoT2I 将文本到图像（T2I）模型选择抽象为一个约束优化问题。给定用户提示 $p$，理想工具 $t^*(p)$ 是在满足质量阈值 $\theta$ 的前提下，推理成本最小的工具：

$$
\operatorname{t}^{*}(p) = \underset{\operatorname{t}_i \in \mathcal{T}}{\arg\min} \ \mathrm{c}(\mathrm{t}_i) \quad \mathrm{s.t.} \ \mathrm{q}(\mathbf{I}, p) \geq \theta
$$

其中 $\mathcal{T}$ 为候选工具集，$\mathrm{c}(\mathrm{t}_i)$ 表示工具 $\mathrm{t}_i$ 的推理成本，$\mathrm{q}(\mathbf{I}, p)$ 为生成图像 $\mathbf{I}$ 相对于提示 $p$ 的质量评分。这一形式化将“性能-效率联合优化”从经验设计提升为可操作的数学目标，是该工作的核心建模贡献。

### 推理工作流：有状态多轮路由

OctoT2I 的推理过程是一个“推理-执行-反思”循环。在第 $r$ 轮，决策策略 $\pi$ 根据用户提示 $p$、长期知识库 $\mathcal{K}$ 和上一轮积累的工作记忆 $\mathcal{M}_{r-1}$ 选择工具：

$$
\mathrm{t}_r = \pi(p, \mathcal{K}, \mathcal{M}_{r-1})
$$

工作记忆 $\mathcal{M}_{r-1}$ 记录了此前各轮所选工具、生成图像及评估反馈，使路由具备状态感知能力。决策策略由 LLM 驱动，通过链式思维推理估计各工具的质量和成本，从满足 $\hat{\mathrm{q}}(\mathrm{t}_i(p), p) \geq \theta$ 的可行工具集中选择成本最小者：

$$
\mathrm{t}_r = \pi(\boldsymbol{p}, \boldsymbol{K}, \mathcal{M}_{r-1}) = \underset{\mathrm{t}_i \in \mathcal{T},\ \hat{\mathrm{q}}(\mathrm{t}_i(\boldsymbol{p}), \boldsymbol{p}) \geq \theta}{\arg\min} \ \hat{\mathrm{c}}(\mathrm{t}_i)
$$

该流程持续迭代，直到评估分数达到阈值 $\theta$ 或达到预设轮次上限。

### 评估模块：连续概率评分

评估函数 $\mathrm{q_{eval}}$ 从多模态大模型（MLLM）的原始 logits 中提取连续质量信号。具体而言，它获取 MLLM 对“yes”和“no”两个 token 的原始 logits，经 softmax 归一化后得到连续概率评分 $s_r$。相比离散的二元判断，连续评分能提供更细粒度的反馈，支撑路由决策和知识构建中的阈值比较。

### 知识模块与记忆模块

- **Knowledge Module（知识模块）**：存储工具的长期知识，包含分层的高层工具画像和细粒度的探索记录。知识库通过自进化机制从零构建，无需人工标注或手工先验。
- **Memory Module（记忆模块）**：维护当前任务执行历史的短时工作记忆 $\mathcal{M}$，使多轮路由能参考此前尝试的成败经验，避免重复选择已证明不适用的工具。

### 自进化机制与探索空间剪枝

自进化机制通过“提议-求解-评估-学习”（Propose–Solve–Evaluate–Learn, PSEL）循环自主构建工具知识。其核心步骤为：

1. **概念维度定义**：LLM 自主定义基础概念维度 $D$（如风格、颜色、计数等），探索空间定义为维度集合的幂集（去掉空集）：

   $$
   \mathcal{C}_{\mathrm{explore}} = 2^{D} \setminus \{\varnothing\}
   $$

2. **子任务掌握评估**：对每个概念维度组合 $\tau$，生成对应提示 $p_\tau$，用工具 $\mathrm{t}_i$ 生成 $N_{\mathrm{sol}}$ 次，计算 Pass@1 指标——单次尝试满足质量阈值的概率：

   $$
   \mathrm{Pass@1}(p_\tau, \mathrm{t}_i) = \frac{1}{N_{\mathrm{sol}}} \sum_{n=1}^{N_{\mathrm{sol}}} \mathbb{I}(s_{\tau, n} \ge \theta)
   $$

   若 $\mathrm{Pass@1} \ge \theta$，则认为工具已掌握该子任务。

3. **探索空间剪枝（ESP）**：遵循递归前提原则——只有当工具已掌握 $\tau$ 的所有真子集 $\tau' \subset \tau$（$\tau' \neq \varnothing$）时，才探索更复杂的维度组合 $\tau$。这一策略大幅缩减探索空间，消融实验表明 ESP 将探索提示数减少 70.9%，时间缩短 66.0%，同时保持 GenEval 总体得分 0.96 不变（Table 6）。

## 实验与分析

### 核心性能与效率权衡

OctoT2I 在 GenEval 基准上取得了 **0.96** 的总体得分（Table 1），显著超越此前最优方法 **Flow-GRPO**（Liu et al., arXiv 2025）的 0.93，以及大型模型 **FLUX.1-dev**（Black Forest Labs, 2024）的 0.82。这一性能优势并非以牺牲效率为代价：相较 Flow-GRPO，OctoT2I 实现了 **90.3%** 的推理加速和 **56.6%** 的能效提升（Abstract），验证了其“质量-成本联合优化”设计目标的有效性。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation on GenEval benchmark. Throughout this paper, the best and second-best results are marked in bold red and underlined blue, respectively. ↑ indicates higher is better. Obj.: Object; Attr.: Attribution*

在更细粒度的组合生成基准 T2ICompBench++ 上，OctoT2I 的平均得分达到 **0.6618**（Table 2），略高于 Flow-GRPO 的 0.6556。尽管绝对提升幅度较小（+0.0062），但考虑到 Flow-GRPO 本身是当前单模型最优基线，这一结果进一步支持了路由策略在复杂组合场景下的稳健性。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/006_Table_2.jpg]]
*Table 2: Quantitative evaluation results on T2ICompBench++. ↑ indicates higher is better*

效率对比（Table 3）进一步量化了 OctoT2I 的优势：在 GenEval 全量提示集上，OctoT2I 的推理时间远低于 Flow-GRPO 等单模型方法，也优于其他智能体 T2I 方法（如 **ChatGen**, Jia et al., arXiv 2024），证明其有状态多轮路由策略并未引入显著额外开销。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/008_Table_3.jpg]]
*Table 3: Efficiency comparison with other competitive methods on GenEval. ↓ indicates lower is better*

### 消融研究

#### 自进化机制的有效性

Table 4 展示了自进化知识构建的消融结果。OctoT2I 的自进化知识（Overall 0.96）明显优于两种替代方案：基于 GPT 内部知识的决策（0.85）和手工先验（0.93）。其中，手工先验虽已接近自进化知识，但仍存在 0.03 的差距，说明自动化探索能够发现人工设计难以覆盖的工具能力边界。GPT 内部知识的显著落后（差距 0.11）则表明，LLM 对 T2I 工具的“直觉”判断远不如系统化探索获得的证据可靠。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/009_Table_4.jpg]]
*Table 4: Ablation on self-evolving mechanism on GenEval*

#### 决策策略的关键作用

Table 5 揭示了知识驱动决策策略的核心价值。将决策策略替换为随机工具选择后，T2ICompBench++ 平均得分从 0.6618 骤降至 0.5379（下降 0.23），证实了基于知识与记忆的自适应路由远优于无引导的多轮试错。这一结果直接支撑了 OctoT2I 的核心主张：工具选择的质量取决于对工具能力的精确建模，而非简单的随机探索。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/010_Table_5.jpg]]
*Table 5: Ablation on decision policy (DP)*

#### 探索空间剪枝的效率增益

Table 6 展示了探索空间剪枝（ESP）策略的效果。启用 ESP 后，自进化阶段所需的探索提示数从 1270 减少至 370（**减少 70.9%**），探索时间从 6857.4 秒缩短至 2328.7 秒（**缩短 66.0%**），而 GenEval 总体得分保持 0.96 不变。这验证了 ESP 的递归前提原则——只有当工具已掌握某概念组合的所有较简单子任务时，才探索该组合——能够在几乎不损失知识覆盖度的前提下大幅提升知识获取效率。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/011_Table_6.jpg]]
*Table 6: Ablation on exploration space pruning (ESP) strategy*

#### 质量阈值 θ 的敏感性

Figure 4 展示了质量阈值 θ 对性能与推理时间的影响。随着 θ 从 0.5 增加到 0.9，GenEval 总体得分呈现先升后降的趋势，而推理时间单调增加。这表明：过低的阈值使系统过早接受低质量图像，无法充分发挥多轮路由的优化潜力；过高的阈值则迫使系统频繁进行多轮重试，增加推理成本却未必带来质量提升。该结果揭示了质量-效率权衡的一个可调“旋钮”，也为实际部署中的阈值选择提供了经验依据。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/007_Figure_4.jpg]]
*Figure 4: Ablation study of θ on performance (green, left axis) and inference time (purple, right axis) on the GenEval benchmark*

### 泛化性与鲁棒性

OctoT2I 在 Wise 基准（Table 7）上展现了良好的泛化能力，表明自进化知识并非过拟合于 GenEval 的提示分布。此外，高效新工具学习实验（Table 8）显示，当工具库中引入新模型时，OctoT2I 能够以较低成本快速更新知识，无需完整的重新自进化。对不同 LLM 的鲁棒性测试（Table 9）进一步表明，决策策略对底层 LLM 的选择具有一定容忍度，降低了系统对特定模型版本的依赖。

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/013_Table_7.jpg]]
*Table 7: Generalization performance on the Wise benchmark*

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/014_Table_8.jpg]]
*Table 8: Efficient New Tool Learning on the Wise benchmark*

![[assets/figures/papers/paper_list_l2174_https_openaccess_thecvf_com_content_CVPR2026_html_Jiang_OctoT2I_A_Self_E/figures/015_Table_9.jpg]]
*Table 9: Robustness to other LLMs on the Wise benchmark*

### 失败模式与局限性

尽管 OctoT2I 在整体指标上表现优异，分析中仍存在若干需要人工验证的潜在弱点：

- **低质量阈值下的性能退化**：当 θ 设置过低时，OctoT2I 可能过早终止路由循环，导致复杂计数和属性绑定等场景的失败率上升。具体失败案例的定性分析需进一步验证。
- **自进化知识覆盖的偏差**：初始概念维度的定义依赖 LLM 的生成能力，可能引入系统性偏见，导致某些工具能力维度未被充分探索。
- **评估模块的校准度**：MLLM 的连续概率评分（从 yes/no logits 经 softmax 计算）与人类判断的一致性尚未充分验证，可能在某些提示类型上引入噪声。
- **动态工具库适应性**：当前自进化机制假设工具库相对稳定，对于频繁迭代的模型生态，增量更新策略的有效性仍需进一步检验。

## 方法谱系与知识库定位

### 问题定位：智能体 T2I 路由的三大瓶颈

当前智能体文本到图像（T2I）方法面临三个相互交织的瓶颈：

1. **知识获取依赖外部监督**：现有方法如 **GenArtist**（Wang et al., NeurIPS 2024）、**ChatGen**（Jia et al., arXiv 2024）和 **Idea2Img**（Yang et al., arXiv 2023）依赖手工先验或昂贵的人工标注来获取工具能力知识，难以规模化扩展。
2. **决策路径单一且静态**：这些方法通常采用固定工具链或单轮选择策略，无法根据实时反馈动态调整。
3. **忽略推理效率**：优化目标仅聚焦生成质量，缺乏对计算成本的显式建模，导致性能与效率之间失衡。

OctoT2I 的核心洞察是将 T2I 模型选择形式化为**约束优化问题**：在满足质量阈值的前提下最小化推理成本（见 Eq. 1）。这一形式化使得系统能够联合优化性能与效率，突破了传统方法的单目标局限。

### 方法谱系中的位置

OctoT2I 处于**智能体路由**与**自进化知识构建**的交叉点，与以下工作形成对比：

- **单模型优化路线**：**Flow-GRPO**（Liu et al., arXiv 2025）通过强化学习微调单一模型达到当前最优（GenEval 0.93），但缺乏工具选择的灵活性，推理成本固定。OctoT2I 在 GenEval 上以 0.96 超越 Flow-GRPO，同时实现 90.3% 推理加速和 56.6% 能效提升（Table 1、Table 3），证明了路由策略的“性能-效率”双重优势。

- **智能体 T2I 路线**：GenArtist、ChatGen 等方法利用 LLM 编排多工具，但工具知识依赖手工设计。OctoT2I 通过自进化机制（PSEL 循环）自主构建知识库，消融实验显示自进化知识（Overall 0.96）显著优于 GPT 内部知识（0.85）和手工先验（0.93）（Table 4），验证了自动化知识获取的有效性。

- **多轮决策 vs. 随机选择**：移除知识驱动的决策策略后，T2ICompBench++ 平均得分从 0.6618 降至 0.5379（下降 0.23，Table 5），说明有状态的多轮“推理-执行-反思”循环是性能增益的关键来源，而非简单的多轮尝试。

### 适用边界

OctoT2I 在以下条件下表现最优：

- **工具库相对稳定**：当前路由策略假设工具集 $\mathcal{T}$ 固定，自进化知识构建针对特定工具库进行。对于快速变化的模型生态（如每日更新的社区模型），可能需要频繁重新自进化。
- **英文提示为主**：实验主要在 GenEval 和 T2ICompBench++ 等英文基准上进行，多语言和低资源场景的泛化性尚未验证。
- **质量阈值适中**：阈值 $\theta$ 消融（Figure 4）显示，$\theta$ 从 0.5 增至 0.9 时，性能先升后降，推理时间单调增加。过低阈值下 OctoT2I 可能无法充分发挥性能优势，部分复杂计数与属性绑定案例仍有改进空间。

### 局限与开放问题

**已识别的局限**（需手动验证具体程度）：

1. **知识覆盖偏差**：自进化知识构建依赖 LLM 定义的初始概念维度，维度选择可能偏向 LLM 的偏见，导致知识覆盖不完整。论文未讨论如何检测和纠正这种偏差。
2. **评估函数的校准度**：评估模块使用 MLLM 的 yes/no logits 经 softmax 得到连续质量分数，但其与人类判断的一致性未充分验证，可能引入系统性噪声。
3. **首次构建成本**：尽管探索空间剪枝（ESP）将探索提示数减少 70.9%、时间缩短 66.0%（Table 6），但首次知识构建仍需一定计算资源，论文未给出绝对成本数据。
4. **低阈值下的失败模式**：在低质量阈值设置下，OctoT2I 与 ChatGen 等方法的不足体现在哪些具体失败案例上，论文未详细分析。

**开放问题**：

- **持续学习**：当用户提示分布发生变化时，自进化机制如何增量更新工具知识，而无需完全重建？
- **大规模工具库**：如何将自进化知识构建扩展到数十甚至上百个工具，并处理工具版本迭代？
- **决策可解释性**：OctoT2I 的决策过程是否能为用户提供工具选择的理由，增强系统透明度？
- **多模态输入**：自进化机制是否可以从纯文本提示拓展到草图、参考图像等多模态输入？
- **探索-利用平衡**：在动态工具库中，如何平衡新工具的能力探索与已掌握工具的稳定利用？

## 原文 PDF

![[paperPDFs/CVPR_2026/OctoT2I_A_Self_Evolving_Agentic_Text_to_Image_Router.pdf]]
