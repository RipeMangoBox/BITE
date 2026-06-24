---
title: "THOR: Tool-Integrated Hierarchical Optimization via RL for Mathematical Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/THOR_Tool_Integrated_Hierarchical_Optimization_via_RL_for_Mathematical_Reasoning.pdf
openreview_forum_id: 0Af7UiJISU
aliases:
- TTIHOR
- THOR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "以中间工具调用（代码执行）成功与否作为细粒度反馈信号，驱动步骤级代码生成优化，并与回合级答案正确性联合训练，从而实现层次化RL，同时利用该信号在推理时进行自我纠正。"
primary_logic: "中间工具调用的成功是最终答案正确性的强预测器（χ²检验显著），因此引入步骤级执行反馈进行细粒度优化，并据此设计层次化强化学习与推理时的自我纠正机制，可显著提升数学推理性能。"
claims:
- "代码执行成功与最终答案正确性显著相关"
- "层次化RL（T5）相比仅回合级RL（T4）在多数基准上带来额外提升"
- "自我纠正（T6）在多个基准上进一步提升性能"
- "TIRGen生成的冷启动数据相比其他TIR数据集在pass@16上明显更优"
---

# THOR: Tool-Integrated Hierarchical Optimization via RL for Mathematical Reasoning

> [!tip] 核心洞察
> 中间工具调用的成功是最终答案正确性的强预测器（χ²检验显著），因此引入步骤级执行反馈进行细粒度优化，并据此设计层次化强化学习与推理时的自我纠正机制，可显著提升数学推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | THOR：基于强化学习的工具集成层次优化数学推理方法 |
| 英文题名 | THOR: Tool-Integrated Hierarchical Optimization via RL for Mathematical Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0Af7UiJISU); [GitHub](https://github.com/JingMog/THOR) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | THOR (Tool-Integrated Hierarchical Optimization via RL) |
| Dataset | MATH 500, AIME 2024, AMC 2023, Overall Average (推理模型) |

> [!tip] 效果简介
> - MATH 500 上，Accuracy (%) 为 87.5 (THOR-7B)，对比 62.6 (AutoTIR-7B, 使用工具); 82.2 (TORL-7B, 无工具)，变化 +24.9 / +5.3。
> - AIME 2024 上，Accuracy (%) 为 50.0 (THOR-7B)，对比 33.3 (AutoTIR-7B); 40.8 (TORL-7B, 无工具)，变化 +16.7 / +9.2。
> - AMC 2023 上，Accuracy (%) 为 81.3 (THOR-7B)，对比 73.8 (TORL-7B, 无工具)，变化 +7.5。

## 概述

数学推理任务中，将大语言模型与外部工具（如代码执行器）集成的工具集成推理（Tool-Integrated Reasoning, TIR）范式，正日益成为提升复杂问题求解能力的关键路径。然而，现有TIR方法面临三重瓶颈：

1. **数据对齐困境**：高质量TIR数据的构建依赖外部模型，导致其推理风格与目标策略模型不匹配，且难以适用于具有深度思考能力的推理模型。
2. **优化粒度粗糙**：传统强化学习仅以最终答案正确性作为稀疏奖励进行回合级优化，忽略了推理链中中间工具调用的细粒度反馈信号，在长程推理场景中优化效率低下。
3. **错误纠正缺失**：推理过程中，模型缺乏对即时工具反馈（如代码执行失败）的有效利用，无法动态察觉并修正错误。

针对上述挑战，本文提出**THOR（Tool-Integrated Hierarchical Optimization via RL）**，一个基于强化学习的工具集成层次优化框架。其核心洞察在于：**中间工具调用的成功与否，是最终答案正确性的强预测器**——卡方检验显示两者高度显著相关（$\chi^2 = 336.3$, $p = 4.09 \times 10^{-75}$）。基于这一因果性发现，THOR将工具执行反馈作为细粒度优化信号，驱动步骤级代码生成优化，并与回合级答案正确性联合训练，构建层次化强化学习范式；同时，在推理时利用该信号实现显式自我纠正。

方法上，THOR由三大模块构成：
- **TIRGen数据构造管道**：通过生成器-精炼器多智能体框架，自动合成策略对齐的高质量TIR冷启动数据。
- **层次化强化学习**：回合级采用GRPO优化最终答案正确性，步骤级针对代码执行失败的步骤进行回溯与重新生成，实现粗细粒度联合优化。
- **推理时自我纠正**：当代码执行失败时，回溯至出错步骤前缀，重新生成后续推理与动作。

在方法谱系中，THOR区别于仅使用工具调用（如**ARTIST-7B**、**TATA-7B**）或仅进行回合级工具增强RL（如**TORL-7B**、**ZTRL-7B**）的基线方法，首次将步骤级执行反馈系统性地引入工具集成推理的强化学习训练与推理过程。

实验结果表明，THOR在多个数学推理基准上取得显著提升：
- **THOR-7B**在MATH 500上达到87.5%准确率，较使用工具的AutoTIR-7B提升24.9个百分点，较无工具的TORL-7B提升5.3个百分点；在AIME 2024上达到50.0%，分别提升16.7和9.2个百分点。
- **THOR-Thinking-8B**（推理模型版本）在全部基准平均准确率达到79.8%，较DeepSeek-R1-Distill-Qwen-7B提升12.3个百分点，较Qwen3-8B提升5.3个百分点。
- 消融实验证实，层次化RL（回合级+步骤级）相比仅回合级RL带来额外增益，推理时自我纠正进一步持续提升性能，尤其在复杂基准上效果显著。

## 背景与动机

### 数学推理中的工具集成范式

数学推理任务要求模型进行多步逻辑演绎、数值计算与符号操作，纯语言模型在这些环节容易出错。工具集成推理（Tool-Integrated Reasoning, TIR）通过在推理过程中调用代码解释器等外部工具来执行计算密集型步骤，已成为提升数学推理可靠性的重要范式。一个典型的TIR轨迹可形式化为思维（reasoning）、动作（action）、观察（observation）的交替序列：

$$\tau = ( r ^ { 1 } , a ^ { 1 } , o ^ { 1 } , . . . , r ^ { t } , a ^ { t } , o ^ { t } , . . . , r ^ { n - 1 } , a ^ { n - 1 } , o ^ { n - 1 } , r ^ { n } )$$

其中 $r^t$ 为自然语言推理步骤，$a^t$ 为工具调用（如Python代码），$o^t$ 为执行返回结果。该序列的生成概率可分解为逐步的思想概率与动作概率之积。

### 现有方法的三大瓶颈

尽管TIR范式已展示出潜力，现有方法仍面临三个相互关联的瓶颈：

**瓶颈一：高质量TIR数据的构建困难。** 现有TIR数据集通常通过直接提示外部模型生成或基于规则的代码注入获得，导致数据风格与目标策略模型不匹配。更关键的是，当前推理模型（如DeepSeek-R1-Distill-Qwen-7B，Guo et al., 2025）普遍缺乏工具调用能力，因为现有TIR数据无法适配其长链推理（long CoT）风格。

**瓶颈二：强化学习的优化粒度粗糙。** 传统工具集成RL方法（如TORL-7B，Li et al., 2025b；ZTRL-7B，Mai et al., 2025）仅以最终答案正确性作为稀疏奖励进行回合级优化。在长推理链场景下，这种稀疏奖励信号难以有效指导中间步骤的学习，导致训练效率低下。

**瓶颈三：推理时缺乏即时反馈利用。** 现有方法在推理过程中若工具调用失败，要么无纠错机制，要么仅依赖模型自身的隐式修正能力，无法利用代码执行器返回的即时错误信息进行显式、结构化的自我纠正。

### 核心洞察：代码执行成功是答案正确性的强预测器

本文的核心动机源于一个关键统计发现：**中间工具调用的成功与否是最终答案正确性的强预测器**。通过对代码执行结果与答案正确性的联合分布进行 $\chi^2$ 检验，结果显示两者存在极显著的相关性（$\chi^2 = 336.3$，$p = 4.09 \times 10^{-75}$，Table 4）。这一发现揭示了步骤级执行反馈蕴含着丰富的监督信号，为细粒度优化提供了理论依据。

基于此洞察，本文提出THOR（Tool-Integrated Hierarchical Optimization via RL），通过三个关键设计系统性解决上述瓶颈：（1）TIRGen数据构造管道，生成策略对齐的高质量TIR数据；（2）层次化强化学习框架，联合优化回合级问题求解与步骤级代码生成；（3）基于工具即时反馈的推理时自我纠正机制。

## 核心创新

THOR 的核心创新围绕一个关键因果发现展开：**中间工具调用（代码执行）的成功与否，是最终答案正确性的强预测器**（Table 4，χ²=336.3，p=4.09e-75）。基于这一洞察，THOR 在三个相互耦合的维度上对现有工具集成推理（TIR）方法进行了系统性改造，形成了“数据构造→层次优化→推理纠错”的闭环。

### 1. 策略对齐的 TIR 数据构造：TIRGen

现有 TIR 数据构造方法存在两个结构性缺陷：一是直接提示外部模型生成的数据与策略模型的推理风格不一致；二是以规则注入代码的方式难以适用于推理模型的长思维链场景。THOR 提出 **TIRGen**，一个基于生成器-精炼器（Generator-Refiner）框架的自动化数据合成管道（Figure 2）。

- **Generator** 负责生成自然语言推理步骤，承担高层数学推理职责，仅需基础指令遵循能力。
- **Refiner** 识别可工具化的步骤，将其转换为 Python 代码并获取执行结果，仅需基础代码生成能力。

这一分工设计使得 TIRGen 能够生成与策略模型风格高度对齐的 TIR 数据。消融实验（Figure 4）表明，相比 Nemotron 的 Long CoT 和 ReTool 的 Short CoT 等 TIR 数据集，TIRGen 生成的冷启动数据在代码调用比率和 pass@16 上均有显著提升（推理模型 pass@16 提升约 10 个百分点）。这些数据为后续强化学习提供了高质量的基础。

### 2. 层次化强化学习：回合级 + 步骤级联合优化

传统 RL 仅以最终答案正确性作为稀疏奖励进行回合级优化，无法有效利用推理链中丰富的步骤级反馈信号。THOR 提出**层次化强化学习框架**（Figure 3），在回合级优化的基础上引入步骤级细粒度优化：

- **回合级优化**：采用 GRPO，以最终答案正确性为奖励，提升模型的整体问题求解能力。
- **步骤级优化**：针对代码执行失败的步骤，通过回溯机制（将出错步骤的推理内容分割为前缀 $r_{\text{pre}}^t$ 和后缀 $r_{\text{suf}}^t$），以执行反馈为奖励信号，重新生成推理后缀和修正动作，专门优化代码生成质量。

最终训练目标为两者的联合损失：
$$\mathscr{L}(\theta) = \mathcal{L}_{\pi_\theta}^{\text{epis}}(\theta) + \mathcal{L}_{\pi_\theta}^{\text{step}}(\theta)$$

消融实验（Table 3）清晰验证了这一设计的有效性：回合级工具集成 RL（T4）相比标准 CoT RL（T2）在所有数学基准上均取得大幅提升；加入步骤级 RL 后（T5），非推理模型平均准确率从 58.7 提升至 60.1，推理模型平均准确率从 76.1 提升至 78.3，验证了层次优化的增益。

### 3. 推理时显式自我纠正

现有方法在推理时缺乏对即时工具反馈的有效利用，难以动态纠正错误。THOR 设计了**基于工具反馈的显式自我纠正机制**（Figure 3c）：当代码执行失败时，模型回溯到出错步骤的前缀 $r_{\text{pre}}^t$，丢弃后缀 $r_{\text{suf}}^t$ 和失败动作 $a^t$，重新生成推理后缀 $\hat{r}_{\text{suf}}^t$ 和修正动作 $\hat{a}^t$。

在修复策略上，步骤后缀修复（step-suffix repair）优于仅修复动作或完全重新规划的策略（Table 5）。显式自我纠正（T6）在多个基准上持续带来额外提升，非推理模型平均准确率达 61.2，推理模型平均达 79.8。更重要的是，该机制将代码通过率提升至 98.7%（THOR-7B）和 99.0%（THOR-Thinking-8B），且不影响最终准确率（Table 6），有效解决了推理过程中的代码执行失败问题。

### 创新总结

THOR 的三个创新点构成了一个因果闭环：TIRGen 提供策略对齐的冷启动数据，使模型建立基本的工具调用能力；层次化 RL 利用步骤级执行反馈进行细粒度优化，将“代码执行成功”这一强预测信号注入训练过程；自我纠正机制则在推理时利用同一信号进行动态纠错，进一步提升推理的鲁棒性和准确性。这一设计使得 THOR 在多个数学基准上显著超越同类规模的工具使用模型和工具自由模型。

## 整体框架

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/003_Figure_3.jpg]]
*Figure 3: A hierarchical optimization framework comprising (a) episode-level RL for mathematical problem solving and (b) step-level optimization for code generation. In addition, we introduce (c) a self-correction mechanism for online error correction during inference*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/002_Figure_2.jpg]]
*Figure 2: The TIR data construction pipeline. In this pipeline, the Generator agent generates reasoning steps. The Refiner agent identifies tool-executable steps and converts them into tool-augmented reasoning steps. After multi-stage filtering, we obtain the cold start dataset $\mathcal { D } _ { S F T }$*

THOR 的整体框架围绕一个核心洞察构建：**中间工具调用（代码执行）的成功与否，是最终答案正确性的强预测器**（χ²=336.3, p=4.09e-75，见 Table 4）。基于这一统计显著的相关性，框架将代码执行反馈从推理时的副产品提升为贯穿训练与推理全流程的驱动信号。

框架由三个层次化阶段构成，形成一条从数据构造到策略优化再到推理时纠错的完整链路：

**阶段一：TIRGen 数据构造管道。** 针对现有工具集成推理（TIR）数据与策略模型风格不对齐、且难以适用于推理模型的瓶颈，THOR 提出 TIRGen——一个基于生成器-精炼器（Generator-Refiner）框架的自动化数据合成管道（Figure 2）。Generator 负责逐步骤生成自然语言数学推理，精炼器识别其中可工具化的步骤并转换为 Python 代码，获取执行结果。经过多阶段过滤后，产出与策略模型风格对齐的高质量 TIR 冷启动数据。消融实验表明，TIRGen 生成的冷启动数据在代码调用率和 pass@16 上显著优于 Nemotron、ReTool 等其他 TIR 数据集（Figure 4）。

**阶段二：层次化强化学习训练。** 传统 RL 仅以最终答案正确性作为回合级稀疏奖励，忽略了中间代码执行的细粒度反馈。THOR 将训练目标分解为两个层次：
- **回合级优化**：采用 GRPO，以答案正确性为奖励，提升模型的数学问题求解能力（Figure 3a）。
- **步骤级优化**：针对代码执行失败的动作，回溯到出错步骤前缀，重新生成推理后缀与新动作，以代码执行成功作为步骤级奖励进行细粒度优化（Figure 3b）。

最终训练目标为两者之和：$\mathscr{L}(\theta) = \mathcal{L}_{\pi_\theta}^{\mathrm{epis}}(\theta) + \mathcal{L}_{\pi_\theta}^{\mathrm{step}}(\theta)$。消融实验（Table 3）验证了层次化设计的有效性：加入步骤级 RL（T5）后，非推理模型平均准确率从 58.7 提升至 60.1，推理模型从 76.1 提升至 78.3。

**阶段三：推理时自我纠正。** 在推理过程中，当代码执行失败时，模型回溯到出错步骤，将推理文本分割为前缀和后缀，重新生成后缀与修正后的代码动作（Figure 3c）。这一机制将训练阶段学到的步骤级纠错能力延续到推理阶段，使代码执行通过率提升至 98.7%（THOR-7B）和 99.0%（THOR-Thinking-8B），且不影响准确率（Table 6）。

**模块间数据流关系：** TIRGen 冷启动数据 → 监督微调建立工具调用基本能力 → 回合级 RL 提升求解能力 → 步骤级 RL 利用执行反馈精细优化代码生成 → 推理时自我纠正闭环利用即时工具反馈。整个框架将代码执行成功这一中间信号贯穿始终，形成了从数据构造到训练优化再到推理纠错的统一闭环。

## 核心模块与公式推导

### 2.1 工具集成推理的形式化建模

THOR 将工具集成推理过程建模为思维（Thought）、动作（Action）、观察（Observation）交替进行的交互轨迹。给定问题 $q$ 和工具接口指令 $I$，一条完整的交互轨迹定义为：

$$\tau = ( r ^ { 1 } , a ^ { 1 } , o ^ { 1 } , . . . , r ^ { t } , a ^ { t } , o ^ { t } , . . . , r ^ { n - 1 } , a ^ { n - 1 } , o ^ { n - 1 } , r ^ { n } )$$

其中 $r^t$ 表示第 $t$ 步的推理思维，$a^t$ 为对应的工具调用动作（代码执行），$o^t$ 为工具返回的观察结果，$r^n$ 为最终答案。轨迹的生成概率按思维和动作逐步分解：

$$P _ { \pi _ { \theta } } ( \tau \mid q , I ) = P _ { \pi _ { \theta } } ( r ^ { n } \mid q , I , \mathcal { H } ^ { 1 : n - 1 } ) \prod _ { t = 1 } ^ { n - 1 } \underbrace { P _ { \pi _ { \theta } } ( r ^ { t } \mid q , I , \mathcal { H } ^ { 1 : t - 1 } ) } _ { \mathrm { T h o u g h t } } \underbrace { P _ { \pi _ { \theta } } ( a ^ { t } \mid r ^ { t } , q , I , \mathcal { H } ^ { 1 : t - 1 } ) } _ { \mathrm { A c t i o n } }$$

该分解将每一步的思维生成与动作生成解耦，为后续的步骤级优化提供了概率基础。

### 2.2 TIRGen 数据构造管道

TIRGen 是用于生成策略对齐的工具集成推理数据的自动化管道，采用生成器-精炼器双代理框架（Figure 2）：

- **Generator**：负责高层数学推理，以自然语言生成推理步骤，单步长度受限于 $L_{\mathrm{step}}$。
- **Refiner**：识别可工具化的推理步骤，将其转换为包含 Python 代码的工具增强步骤，并获取执行结果。Refiner 仅需基本的指令遵循和代码生成能力，不要求复杂的数学推理。

该管道通过多轮交互生成完整的工具集成推理路径，经多阶段过滤后得到冷启动监督微调数据集 $\mathcal{D}_{\mathrm{SFT}}$。关键设计在于 Generator 与策略模型共享推理风格，确保数据与后续 RL 训练的风格对齐。

### 2.3 冷启动监督微调

使用 TIRGen 生成的数据进行标准监督微调，损失函数为负对数似然：

$$\mathcal { L } _ { \mathrm { S F T } } ( \theta ) = \mathbb { E } _ { ( q , I , y ) \sim \mathcal { D } _ { S F T } } \Big [ - \sum _ { t = 1 } ^ { T } \log \tilde { \pi } _ { \theta } ( y _ { t } \mid q , I , y _ { 0 : t - 1 } ) \Big ]$$

此阶段建立模型的基础工具调用能力，为后续强化学习提供有效初始化。

### 2.4 回合级强化学习

回合级优化采用 GRPO（Shao et al., 2024），以最终答案正确性作为奖励信号，提升模型的整体问题求解能力（Figure 3(a)）。对于从 $\mathcal{D}_{\mathrm{RL}}$ 采样的问题 $q$，采样 $G$ 条轨迹，损失函数为：

$$\mathcal { L } _ { \pi _ { \theta } } ^ { \mathrm { e p i s } } ( \theta ) = \mathbb { E } [ q \sim \mathcal { D } _ { R L } , \{ s _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta } ( S | q ) ] \frac { 1 } { G } \displaystyle \sum _ { i = 1 } ^ { G } \bigg ( \frac { 1 } { \sum _ { t = 1 } ^ { | s _ { i } | } I ( s _ { i , t } ) } \sum _ { t : I ( s _ { i , t } ) = 1 } ^ { | s _ { i } | } \operatorname* { m i n } \big ( \frac { \pi _ { \theta } \big ( s _ { i } | q \big ) } { \pi _ { \theta _ { \mathrm { o l d } } } \big ( s _ { i } | q \big ) } A _ { i } , \mathrm { c l i p } ( \frac { \pi _ { \theta } \big ( s _ { i } | q \big ) } { \pi _ { \theta _ { \mathrm { o l d } } } \big ( s _ { i } | q \big ) } , 1 - \varepsilon _ { \mathrm { l o w } } , 1 + \varepsilon _ { \mathrm { h i g h } } ) A _ { i } \big ) \bigg ) + \alpha \mathcal { L } _ { \mathrm { N L L } } ( \theta )$$

其中 $A_i$ 为基于组内奖励归一化的优势函数，$\varepsilon_{\mathrm{low}}$ 和 $\varepsilon_{\mathrm{high}}$ 控制裁剪范围。额外引入的语言模型正则化损失 $\mathcal{L}_{\mathrm{NLL}}$ 对正优势示例施加似然最大化，加速收敛：

$$\mathcal { L } _ { \mathrm { N L L } } ( \theta ) = - \frac { 1 } { \sum _ { s _ { i } \in \mathcal { T } _ { \mathrm { p o s } } } \left| s _ { i } \right| } \sum _ { s _ { i } \in \mathcal { T } _ { \mathrm { p o s } } } \log \pi _ { \theta } ( s _ { i } | q )$$

### 2.5 步骤级强化学习

步骤级优化针对代码执行失败的步骤进行细粒度修正（Figure 3(b)）。核心机制是回溯重生成：对于出错动作 $a^t$，将其对应的思维 $r^t$ 分割为前缀 $r_{\mathrm{pre}}^t$ 和后缀 $r_{\mathrm{suf}}^t$（后缀长度为 $L_{\mathrm{suf}}$），以历史序列到 $r_{\mathrm{pre}}^t$ 为条件，重新生成推理后缀和修正动作。

步骤级数据集由失败动作的前缀构成：

$$\mathcal { D } _ { s t e p } = \{ \mathrm { p r e f } ( \tau , t ) \mid a ^ { t } \in \mathcal { A } _ { \mathrm { e r r } } , \tau \in \mathcal { T } \}$$

其中前缀构造方式为：

$$\mathrm { p r e f } ( \tau , t ) = ( q , r ^ { 1 } , a ^ { 1 } , o ^ { 1 } , . . . , r ^ { t - 1 } , a ^ { t - 1 } , o ^ { t - 1 } , r _ { \mathrm { p r e } } ^ { t } ) , \quad r ^ { t } = r _ { \mathrm { p r e } } ^ { t } \oplus r _ { \mathrm { s u f } } ^ { t }$$

步骤级优化的奖励 $r_i'$ 为代码执行是否成功（二元信号），组内归一化后得到优势：

$$A_i' = \frac{r_i' - \mathrm{mean}(r')}{\mathrm{std}(r')}$$

步骤级策略损失采用 PPO 风格的裁剪目标与负对数似然正则化：

$$\mathcal { L } _ { \pi _ { \theta } } ^ { \mathrm { s t e p } } ( \theta ) = \mathbb { E } [ p \sim \mathcal { D } _ { s t e p } , \{ s _ { i } ^ { \prime } \} _ { i = 1 } ^ { G } \sim \pi _ { \theta } ( S | p ) ] \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \big ( \min ( \frac { \pi _ { \theta } ( s _ { i } ^ { \prime } | p ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( s _ { i } ^ { \prime } | p ) } A _ { i } ^ { \prime } , \mathrm { c l i p } ( \cdots ) A _ { i } ^ { \prime } ) \big ) + \beta \mathcal { L } _ { \mathrm { N L L } } ^ { \prime } ( \theta )$$

### 2.6 联合训练目标

最终训练目标为回合级损失与步骤级损失的线性组合：

$$\mathscr{L}(\theta) = \mathcal{L}_{\pi_\theta}^{\mathrm{epis}}(\theta) + \mathcal{L}_{\pi_\theta}^{\mathrm{step}}(\theta)$$

该层次化目标同时优化全局问题求解能力和局部代码生成精度，使模型在长推理链中既能获得稀疏的回合级奖励，又能利用密集的步骤级执行反馈。

### 2.7 推理时自我纠正

推理阶段，当动作 $a^t$ 执行失败时，模型回溯到 $r^t$，将其分割为前缀 $r_{\mathrm{pre}}^t$ 和后缀 $r_{\mathrm{suf}}^t$，重新生成推理后缀 $\hat{r}_{\mathrm{suf}}^t$ 和修正动作 $\hat{a}^t$（Figure 3(c)）。最大纠正尝试次数设为 $N_{\mathrm{corr}} = 4$。该机制直接复用步骤级优化训练出的回溯重生成能力，无需额外模型或外部信号。

## 实验与分析

### 核心动机验证：代码执行成功是答案正确性的强预测器

THOR 的设计前提建立在一条关键的因果假设之上：中间工具调用（代码执行）的成功与否，能够有效预示最终答案的正确性。为验证这一假设，作者对模型生成的交互轨迹进行了统计分析，构建了代码执行结果与答案正确性的联合分布表。

**Table 4** 展示了这一分析的结论。在大量采样轨迹中，代码执行成功且答案正确的样本占据主体（3950例），而代码执行失败且答案错误的样本也高度集中（382例）。然而，两个“不一致”区域揭示了关键信息：存在139例代码执行成功但答案最终错误的情况，以及51例代码执行失败但答案正确的“侥幸”案例。卡方检验结果（$\chi^2=336.3, p=4.09\times 10^{-75}$）极其显著，强有力地支持了代码执行成功与最终答案正确性之间存在统计依赖关系。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/011_Table_4.jpg]]
*Table 4: Joint distribution between code execution result and answer correctness*

这一发现构成了 THOR 方法论的基石：既然代码执行成功是正确答案的强预测器，那么将其作为步骤级反馈信号引入强化学习优化，并在推理时用于驱动自我纠正，便具备了坚实的实证依据。同时，那些“不一致”案例也暗示了单纯依赖回合级答案奖励的局限性——模型可能通过错误路径“蒙对”答案，或正确计算后却输出错误格式，这正是引入步骤级细粒度优化的必要性所在。

### 主实验结果：在数学推理基准上达到同等规模模型最优

THOR 在六个数学推理基准上进行了系统评估，涵盖 MATH 500、AIME 2024、AIME 2025、AMC 2023、Minerva Math 和 Olympiad Bench。**Table 1** 汇总了 THOR 与现有方法的全面对比，所有结果均采用 Avg@4 以减少采样随机性。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/004_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on mathematical benchmarks, the best results are in bold and the second-best are underlined. Code use indicates whether code tools are employed. † denotes our reimplementation results of Avg@4, ‡ indicates results from their official releases*

在非推理模型（non-reasoning model）类别中，**THOR-7B** 取得了 61.2 的平均准确率，显著超越了所有同等规模的工具使用基线。具体而言，相比工具集成推理方法 **AutoTIR-7B**（Wei et al., 2025），THOR-7B 在 MATH 500 上领先 24.9 个百分点（87.5 vs. 62.6），在 AIME 2024 上领先 16.7 个百分点（50.0 vs. 33.3）。即使与不显式使用工具的强基线 **TORL-7B**（Li et al., 2025b）相比，THOR-7B 仍保持明显优势（MATH 500: 87.5 vs. 82.2; AIME 2024: 50.0 vs. 40.8）。值得注意的是，THOR-7B 甚至超越了更大规模的模型 **GPT-4o**（Hurst et al., 2024）在 AIME 2024 上的表现（50.0 vs. 47.5）。

在推理模型（reasoning model）类别中，**THOR-Thinking-8B** 以 79.8 的平均准确率位居榜首。相比强大的推理基线 **DeepSeek-R1-Distill-Qwen-7B**（Guo et al., 2025）的 67.5 和 **Qwen3-8B**（Yang et al., 2025）思维模式的 74.5，THOR-Thinking-8B 分别提升了 12.3 和 5.3 个百分点。在最具挑战性的 AIME 2025 基准上，THOR-Thinking-8B 达到 62.5，远超 DeepSeek-R1-Distill-Qwen-7B 的 42.5 和 Qwen3-8B 的 53.3，显示出工具集成层次优化在复杂推理任务上的突出优势。

轻量级模型 **THOR-1.5B** 同样表现出色，以 49.1 的平均准确率超越了所有同规模非推理模型，验证了方法的可扩展性。

### 消融实验：各组件贡献的逐层解构

**Table 3** 提供了严格的消融分析，通过逐步叠加系统组件（T1→T6），量化了每个设计选择的边际贡献。实验同时在非推理模型（Qwen2.5-Math-7B 基础）和推理模型（Qwen3-8B 基础）上进行。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/006_Table_3.jpg]]
*Table 3: Results of the ablation on each component. Cold start uses the data generated by TIRGen in Section 2.2. EpisRL and StepRL correspond to episode-level and step-level optimization defined in Section 2.3. SelfCorr denotes self-correction during inference in Section 2.4*

**冷启动阶段（T1→T3）**：在基础模型（T1）上引入代码工具使用（T2）后，非推理模型平均准确率从 40.5 提升至 43.9，推理模型从 67.5 提升至 69.5。进一步使用 TIRGen 生成的冷启动数据进行监督微调（T3），非推理模型跃升至 53.6，推理模型达到 74.3。这一跳跃验证了 TIRGen 管道生成策略对齐数据的关键作用——它不仅建立了工具调用的基本能力，更为后续 RL 阶段提供了良好的初始化。

**回合级工具集成 RL（T3→T4）**：应用基于 GRPO 的回合级工具集成强化学习后，非推理模型平均准确率从 53.6 大幅提升至 58.7（+5.1），推理模型从 74.3 提升至 76.1（+1.8）。作为对比，若采用标准 CoT RL 而非工具集成 RL（T2→T2+CoT RL），非推理模型仅从 43.9 提升至 46.7，远不及 T4 的增益。这明确表明，将代码工具纳入 RL 优化循环本身就能带来超越纯文本推理的显著收益。

**步骤级层次优化（T4→T5）**：在回合级 RL 基础上加入步骤级代码执行反馈优化后，非推理模型平均准确率进一步提升至 60.1（+1.4），推理模型提升至 78.3（+2.2）。这一增益虽然在绝对数值上小于冷启动和回合级 RL 的贡献，但它在多个基准上表现一致，尤其在 AIME 2024（推理模型：73.3→76.7）和 AIME 2025（推理模型：53.3→57.5）等复杂任务上效果更为明显。这证实了步骤级细粒度优化能够有效利用回合级奖励无法捕捉的中间信号，缓解长推理链中的稀疏奖励问题。

**推理时自我纠正（T5→T6）**：在推理阶段引入基于工具反馈的显式自我纠正机制后，非推理模型达到最终平均准确率 61.2（+1.1），推理模型达到 79.8（+1.5）。自我纠正在所有基准上均带来一致的正向增益，且无需额外训练，验证了即时工具反馈在推理时动态修正错误的有效性。

**Figure 4** 进一步消融了冷启动数据的质量影响。相比使用 Nemotron 的长 CoT 数据和 ReTool 的短 CoT 数据，TIRGen 生成的数据在代码调用比率和 pass@16 指标上均有显著优势。对于推理模型，TIRGen 数据的 pass@16 提升约 10 个百分点，表明生成器-精炼器管道能够产生更高质量、更贴近策略模型风格的 TIR 数据。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_0Af7UiJISU/figures/009_Figure_4.jpg]]
*Figure 4: Ablation on cold-start efficiency. We compare our TIRGen against other TIR datasets, including Long CoT from Nemotron and Short CoT from ReTool. Results are reported as code ratio in (a) and pass@16 in (b) and (c), demonstrating the effectiveness of TIRGen and cold start*

### 自我纠正策略与效率分析

**Table 5** 对比了四种推理时修复策略：无纠正、仅修复动作（action-only）、修复步骤后缀（step-suffix）、完全重新规划（full re-plan）。步骤后缀修复策略（即回溯到出错步骤前缀，重新生成推理后缀与动作）在两个模型类型上均取得最高平均准确率。仅修复动作效果次之，完全重新规划则因丢失过多有效上下文而表现最差。这一结果表明，局部修复优于全局重规划，保留正确的推理前缀对维持解题方向至关重要。

**Table 6** 量化了显式自我纠正对代码执行质量的影响。在 THOR-7B 上，显式自我纠正将失败的代码执行次数从 158 大幅降至 55，代码通过率提升至 98.7%，同时准确率从 60.1 提升至 61.2。在 THOR-Thinking-8B 上，失败次数从 101 降至 24，通过率达到 99.0%，准确率从 78.3 提升至 79.8。值得注意的是，显式自我纠正不仅没有因额外计算开销损害性能，反而同时提升了准确率和代码可靠性。

**Table 7** 报告了推理效率。相比各自的基础模型（Qwen2.5-Math-7B 和 Qwen3-8B），THOR 变体在平均 token 消耗上分别减少了 6% 和 13%。工具集成使模型能够将繁琐的计算卸载给代码解释器，从而生成更简洁的推理链，在提升准确率的同时降低了推理成本。

### 测试时缩放：基于代码执行反馈的自奖励策略

**Table 2** 探索了测试时计算扩展方法。作者提出了一种不依赖外部过程奖励模型（PRM）的自奖励 Best-of-N 策略：采样 N 条独立轨迹，选择代码执行通过率最高的作为最终输出。在计算预算 N=8 的条件下，该策略在 THOR-7B 上达到 64.4 的平均准确率（相比单次推理的 61.2 提升 3.2 个百分点），在 THOR-Thinking-8B 上达到 84.3（相比 79.8 提升 4.5 个百分点）。自奖励策略在 AIME 2024 和 AIME 2025 等挑战性基准上的增益尤为显著。

更关键的是，纯粹基于代码执行通过率的自奖励策略在性能上匹配甚至超越了基于外部 PRM（InternLM2-RM）的选择方法，且完全消除了对外部奖励模型的依赖。当候选轨迹的代码通过率相同时，可进一步引入 PRM 进行混合选择，获得微小的额外增益（THOR-Thinking-8B: 84.3→84.6）。这一发现揭示了工具执行反馈本身即可作为强内在奖励信号，为测试时计算扩展提供了轻量且有效的方案。

### 代码生成泛化能力

**Figure 5** 展示了 THOR 在代码生成基准上的迁移表现。经过数学工具集成 RL 训练后，模型在 HumanEval+、MBPP+ 和 LiveCodeBench v6 上的 pass@1 准确率均显著优于冷启动前的基模型。这表明，以数学推理为训练场景的层次优化所培养的代码生成与纠错能力，能够有效泛化到通用代码生成任务。

### 需要人工核验的边界

部分结论的证据强度存在差异，需注意以下限制：
- HumanEval+ 等代码基准上的提升幅度未在正文中精确量化，仅通过 **Figure 5** 的柱状图呈现，具体数值需从图中读取或查阅附录。
- TIRGen 与其他 TIR 数据集的对比（**Figure 4**）中，pass@16 的“约 10 个百分点提升”为视觉估计值，精确数字需核实。
- 所有实验均基于 Qwen 系列基础模型，方法在其他模型家族上的迁移效果有待进一步验证。

## 方法谱系与知识库定位

### 问题域与核心瓶颈

THOR 聚焦于**工具集成推理（Tool-Integrated Reasoning, TIR）**在数学问题求解中的应用。现有 TIR 方法面临三重瓶颈：

1. **数据构建困境**：高质量 TIR 训练数据稀缺，现有数据通常由外部大模型直接生成，其推理风格与目标策略模型不匹配，且难以适配推理模型（reasoning model）的长思维链范式。
2. **优化粒度粗糙**：传统强化学习仅以最终答案正确性作为回合级稀疏奖励，在长推理链中无法有效利用中间步骤的即时反馈信号，导致训练效率低下。
3. **推理时纠错缺失**：推理过程中代码执行失败时，模型缺乏基于工具反馈的显式纠正机制，只能依赖自身隐式修正，错误传播风险高。

THOR 的核心洞察在于：**中间工具调用（代码执行）的成功与否是最终答案正确性的强预测器**（χ²=336.3, p=4.09e-75, Table 4），因此可将执行反馈作为细粒度优化信号。

### 方法谱系定位

THOR 处于 TIR 方法谱系中从“工具使用”到“工具集成推理与优化”的演进路径上，其关键创新在于将**数据构造、层次化强化学习、推理时自我纠正**三个环节系统性地整合。

#### 相对于工具使用基线

早期工具使用基线如 **ARTIST-7B**（Singh et al., 2025）、**TATA-7B**（Xu et al., 2025）主要关注让模型学会调用工具，但缺乏对工具调用质量的系统性优化。THOR 在此基础上引入步骤级执行反馈驱动的优化，将工具使用的“能否调用”提升为“调用是否正确”。

#### 相对于工具集成推理基线

**AutoTIR-7B**（Wei et al., 2025）代表了工具集成推理的自动化尝试，但在数据质量和优化粒度上存在局限。THOR 的 TIRGen 数据构造管道（Generator-Refiner 多智能体框架）专门解决了策略对齐问题：Generator 负责高层数学推理，Refiner 识别可工具化步骤并转换为代码，生成的数据在代码调用比率和 pass@16 上显著优于 Nemotron、ReTool 等现有 TIR 数据集（Figure 4）。

#### 相对于工具增强 RL 基线

**TORL-7B**（Li et al., 2025b）和 **ZTRL-7B**（Mai et al., 2025）已将强化学习引入工具使用场景，但仅进行回合级优化。THOR 的层次化 RL 框架在此基础上新增步骤级优化：当代码执行失败时，通过回溯机制（backtracking）对出错步骤的前缀进行条件化，重新生成推理后缀和修正动作，形成回合级（答案正确性）+ 步骤级（代码执行成功）的联合优化目标。

#### 相对于工具自由基线

与不使用工具的强基线对比，THOR 展现出工具集成带来的增益。在推理模型上，THOR-Thinking-8B 平均准确率 79.8%，显著优于 **DeepSeek-R1-Distill-Qwen-7B**（Guo et al., 2025）的 67.5% 和 **Qwen3-8B**（Yang et al., 2025）的 74.5%（Table 1）。与工具自由的 RL 方法 **Eurus-2-PRIME-7B**（Cui et al., 2025）和搜索方法 **rStar-Math-7B**（Guan et al., 2025）相比，THOR 通过工具调用将复杂计算卸载给 Python 解释器，在相同模型规模下取得更优性能。

### 关键技术槽位对比

| 技术槽位 | 基线方法 | THOR 方案 | 证据锚点 |
|---------|---------|----------|---------|
| 数据构造 | 外部模型直接生成或基于规则的代码注入 | TIRGen 生成器-精炼器管道，策略对齐 | Section 2.2, Figure 2 |
| RL 优化粒度 | 仅回合级（最终答案正确性） | 层次化：回合级 + 步骤级（代码执行成功） | Section 2.3.2, Figure 3 |
| 推理时纠错 | 无或隐式修正 | 基于工具反馈的显式自我纠正，回溯重生成 | Section 2.4, Figure 3(c) |

### 技术边界与适用条件

1. **工具类型限定**：当前框架仅验证了 Python 代码执行作为工具调用形式，其层次化优化和自纠正机制依赖于代码执行结果的可验证性（成功/失败二值信号）。对于其他类型工具（如搜索引擎、知识库查询），若缺乏明确的可验证反馈，框架的适用性需进一步验证。

2. **领域边界**：主要实验集中在数学推理基准（MATH 500、AIME、AMC、MinervaMath、OlympiadBench），代码生成基准（HumanEval+、MBPP+、LiveCodeBench）上观察到泛化能力（Figure 5），但在非数学-代码交叉领域的适用性尚未充分验证。

3. **计算开销**：层次化 RL 训练和推理时自我纠正均引入额外计算成本。自我纠正的最大尝试次数设为 N_corr=4，实际推理延迟和吞吐量受此参数影响（Table 7 显示 THOR 变体在 token 消耗上反而减少 6%-13%，但需考虑代码执行时间）。

4. **模型规模**：实验覆盖 1.5B、7B、8B 参数规模，在更大规模模型上的缩放行为未报告。

### 局限与开放问题

1. **步骤级奖励的稀疏性**：步骤级优化依赖代码执行失败作为触发条件。对于执行成功但逻辑错误的代码，当前框架无法提供纠正信号（Table 4 显示 139 例代码成功但答案错误的情况）。

2. **自我纠正策略的次优性**：消融实验（Table 5）表明步骤后缀修复（step-suffix repair）优于仅修复动作或完全重新规划，但该策略本质上是局部贪婪修复，未考虑全局推理路径的一致性优化。

3. **工具调用的必要性判断**：TIRGen 的 Refiner 负责识别可工具化步骤，但何时不应调用工具的决策边界未被显式建模，可能导致不必要的工具调用开销。

4. **多工具协同**：当前仅支持单一 Python 代码工具，多工具协同调用（如符号计算 + 数值验证 + 知识检索）场景下的层次化优化策略有待探索。

5. **开放式数学推理**：评测集中在有明确答案的基准测试，对于证明题、开放式数学探索等场景，执行反馈与正确性之间的相关性可能减弱，框架的有效性需要重新审视。

> **注**：部分基线的具体会议/期刊信息（如 Singh et al. 2025、Xu et al. 2025、Wei et al. 2025 等）在提供材料中未明确标注发表 venue，建议人工核实补充。

## 原文 PDF

![[paperPDFs/ICLR_2026/THOR_Tool_Integrated_Hierarchical_Optimization_via_RL_for_Mathematical_Reasoning.pdf]]
