---
title: "VISTA: A Test-Time Self-Improving Video Generation Agent"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VISTA_A_Test_Time_Self_Improving_Video_Generation_Agent.pdf
project_link: "https://g-vista.github.io/"
code_link: null
aliases:
- VISTA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过多维度多代理反馈迭代优化提示词，将视频生成改进建模为可解释的、结构化自修正循环。
primary_logic: 将视频生成优化建模为人类式的迭代改进循环：分解为结构化规划、成对锦标赛选择、多维度多代理批判和深度思考提示优化，从而自动地改善视觉、音频和上下文的综合质量。
claims:
- VISTA 在单场景和多场景基准上相对于直接提示 (DP) 的成对胜率达到 45.9%（Δ=32%）和 46.3%（Δ=35.1%），远超其他测试时优化基线。
- 人类评估中，VISTA 在 66.4% 的比较中被偏好，表明其改进符合人类主观判断。
- Single-scene (MovieGenVideo, 100 prompts) 上 Win Rate over Direct Prompting = 45.9%
- Multi-scene (internal dataset, 161 prompts) 上 Win Rate over Direct Prompting = 46.3%
---

# VISTA: A Test-Time Self-Improving Video Generation Agent

> [!tip] 核心洞察
> 将视频生成优化建模为人类式的迭代改进循环：分解为结构化规划、成对锦标赛选择、多维度多代理批判和深度思考提示优化，从而自动地改善视觉、音频和上下文的综合质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | VISTA：测试时自优化的视频生成多代理系统 |
| 英文题名 | VISTA: A Test-Time Self-Improving Video Generation Agent |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.15831) · [Project](https://g-vista.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | VISTA |
| Dataset | Single-scene, Multi-scene, Human Evaluation |

> [!tip] 效果简介
> - Single-scene (MovieGenVideo, 100 prompts) 上，Win Rate over Direct Prompting 45.9% vs 0% (DP reference) (Δ = +32.0%)。
> - Multi-scene (internal dataset, 161 prompts) 上，Win Rate over Direct Prompting 46.3% vs 0% (DP reference) (Δ = +35.1%)。
> - Human Evaluation 上，Preference Rate 66.4% vs Baselines (DP, VSR, VSR++, Rewrite, VPO) (66.4% preferred VISTA)。

## 概述

文本到视频（T2V）生成模型近年来取得了显著进展，但其输出质量仍高度依赖用户提示的精确性，且缺乏在测试时自动、多维度优化视频的能力。现有方法通常仅关注视觉质量的单一维度，忽略了音频、上下文连贯性等关键因素，导致生成视频在整体表现力上存在瓶颈。

针对这一问题，本文提出 **VISTA**，一个测试时自优化的视频生成多代理系统。VISTA 的核心洞见在于将视频生成的质量改进建模为一个类人的迭代优化循环：通过结构化规划、成对锦标赛选择、多维度多代理批判和深度思考提示优化四个关键组件的协同，系统能够在测试时自动改善视频的视觉保真度、音频匹配度和上下文连贯性。

在方法定位上，VISTA 区别于传统的直接提示（Direct Prompting）或简单的提示重写（Rewrite），也超越了仅依赖单一模型进行自我优化的方案（如 Visual Self-Refine）。它通过引入 **PromptPlanner** 将用户输入分解为具有时序结构和九大属性的场景序列，利用 **PairwiseSelect** 以双向成对锦标赛机制筛选最优视频-提示对，再通过由正常法官、对抗法官和元法官构成的 **MMAC** 三元法庭进行多维度批判，最终由 **DTPA** 深度思考代理执行六步内省推理来优化提示，形成了一个完整的闭环自改进框架。

实验结果表明，VISTA 在两个基准测试上均显著优于现有基线。在单场景和多场景基准上，VISTA 相对于直接提示的成对胜率分别达到 **45.9%**（Δ=+32.0%）和 **46.3%**（Δ=+35.1%），远超其他测试时优化方法。人类评估进一步验证了其有效性，评估者在 **66.4%** 的比较中偏好 VISTA 的输出。消融实验证实，每个组件都对整体性能有独特贡献：PromptPlanner 提升了初始视频质量，PairwiseSelect 稳定了迭代改进过程，多法官协同平衡了批判的深度与实用性，DTPA 则显著增强了提示优化的效果。

## 背景与动机

文本到视频（T2V）生成领域近年来取得了显著进展，以 **Veo 3**、**Sora**、**MovieGen** 等模型为代表的生成系统已能产出视觉质量较高的视频内容。然而，这些模型的实际可用性仍受制于一个核心瓶颈：**生成质量高度依赖用户提示的精确性**。普通用户往往难以一次性撰写出能充分表达其意图的提示，而即使经验丰富的用户，也需要反复试错才能获得满意的结果。这种“提示工程”负担严重限制了视频生成技术的普及与创作效率。

现有研究在测试时优化方面已有所探索。在文本生成领域，**Visual Self-Refine**（Madaan et al., 2023）等方法利用大语言模型（LLM）对输出进行迭代评估与修正；在图像生成领域，基于多模态大语言模型（MLLM）的反馈优化提示也取得了初步成效。然而，这些方法在迁移到视频生成时面临根本性困难：**视频涉及视觉、音频和上下文（时序连贯性与叙事逻辑）三个交织的维度，单一模型或单一维度的评估无法提供足够的优化信号**。直接套用现有方法——如用 MLLM 重写提示（**Rewrite**，Google Cloud, 2024）或按预设原则扩展提示（**VPO**，Cheng et al., 2025b）——均未能在视频场景下实现稳定且可解释的迭代改进。

上述缺口揭示了两个深层问题：其一，缺乏一种**结构化的视频理解与规划机制**，将用户模糊意图分解为可操作、可评估的生成单元；其二，缺乏一种**多维度、多视角的批判与反思框架**，使系统能像人类创作者一样，从不同角度审视视频缺陷并有针对性地修正。VISTA 正是在这一背景下提出，将视频生成优化建模为**可解释的、结构化自修正循环**，通过多代理协作在测试时自动改进视觉、音频和上下文的综合质量，而无需重新训练或微调底层生成模型。

## 核心创新

VISTA 的核心创新在于将文本到视频生成的质量改进建模为一个**测试时可解释的、结构化自修正循环**，而非依赖单次提示工程或模型微调。其关键突破体现在以下四个 **changed slots** 上，它们共同构成了从“被动生成”到“主动优化”的范式转变。

### 1. 从原始提示到结构化时序场景分解

现有方法（如 **Direct Prompting**、**Rewrite** (Google Cloud, 2024)、**VPO** (Cheng et al., 2025b)）直接使用或简单改写用户提示，忽略了视频的时序结构和多维度属性。VISTA 的 **PromptPlanner** 模块将用户提示解析为具有时序约束的场景序列，每个场景由跨越**上下文、视觉、音频**三个维度的九个属性精确定义（包括时长、位置、主体、动作、镜头语言、光照、色彩风格、音效、情绪氛围）。这一结构化分解使得初始候选提示本身就具备更强的生成引导能力，为后续优化提供了可操作的语义基础。消融实验证实，移除 PromptPlanner 后，单场景初始化胜率从 35.5% 降至 25.2%，初始视频质量显著降低。

### 2. 从单一评分到成对锦标赛选择

传统测试时优化方法（如 **Visual Self-Refine** (Madaan et al., 2023)）依赖单一模型对视频进行绝对评分，容易引入模型偏差且与人类偏好对齐不足。VISTA 的 **PairwiseSelect** 采用**双向成对锦标赛机制**，通过多轮二元比较迭代筛选最优视频-提示对。其得分函数引入了违规惩罚项：

$$s_i \gets \frac { 1 } { k } \sum _ { C \in \mathcal{M}_{user}^{g} } ( \delta ( C , V _ { i } , V _ { j } ) - \lambda \cdot \mathbb{ 1 } ( C , V _ { i } ) ), \quad s _ { j } \gets \frac { 1 } { k } \sum _ { C \in \mathcal{M}_{user}^{g} } ( 1 - \delta ( C , V _ { i } , V _ { j } ) - \lambda \cdot \mathbb{ 1 } ( C , V _ { j } ) )$$

其中 $\delta$ 表示胜负平结果，$\lambda$ 为惩罚权重，$\mathbb{1}$ 为违规指示函数。这一设计不仅更贴合人类偏好，还通过探查批评机制确保选择的可靠性。消融表明，移除 PairwiseSelect 后迭代改进变得不稳定，第 5 轮单场景胜率从 45.9% 骤降至 33.3%。

### 3. 从单一评估到多维度多代理批判

现有方法通常使用单一模型进行视频评估，无法同时兼顾批评的深度与建设性。VISTA 的 **MMAC** 模块为每个评估维度（视觉、音频、上下文）构建了一个**三元法官法庭**：

$$\{ C _ { D } , S _ { D } \} = J _ { D } ( P , V ^ { * } , P ^ { * } ) \, (\mathrm{Normal}) \\ \{ C _ { D } ^ { - } , S _ { D } ^ { - } \} = J _ { D } ^ { - } ( P , V ^ { * } , P ^ { * } ) \, (\mathrm{Adversarial}) \\ \{ C _ { D } ^ { * } , S _ { D } ^ { * } \} = J _ { D } ^ { * } ( P , C _ { D } , S _ { D } , C _ { D } ^ { - } , S _ { D } ^ { - } ) \, (\mathrm{Meta})$$

- **Normal Judge** 提供建设性批评和正面评分；
- **Adversarial Judge** 主动寻找缺陷与不足；
- **Meta Judge** 综合两者形成最终的平衡性批判。

消融实验显示，仅使用单一法官（仅 Normal 或仅 Adversarial）均导致性能下降，验证了对抗性与建设性批判互补的必要性。

### 4. 从直接改写到底层深度思考提示优化

**Visual Self-Refine** 等方法仅通过 MLLM 直接改写提示，缺乏对视频问题根源的深入分析。VISTA 的 **DTPA** 执行**六步内省式推理链**：(1) 识别视频问题；(2) 追溯问题至提示缺陷；(3) 分析根本原因；(4) 提出针对性修改建议；(5) 评估修改的预期影响；(6) 审查并精炼建议。这一过程生成结构化修改集 $\mathcal{M} := \{ M_1, \ldots \} = \mathrm{DTPA}(P, P^*, \mathcal{F})$，随后由 MLLM 据此采样改进提示候选。移除 DTPA 后，单场景胜率从 45.9% 降至 37.8%，证明深层推理对提示优化至关重要。

### 创新瓶颈与因果机制

上述四个 changed slots 针对的核心瓶颈在于：**现有 T2V 系统高度依赖精确的用户提示，且缺乏能同时优化多维度质量的测试时自动改进框架**。VISTA 通过将视频生成改进建模为“结构化规划→锦标赛选择→多代理批判→深度思考优化”的闭环，实现了对视觉保真度、音频质量、上下文连贯性的联合提升。这一因果链条使得 VISTA 在单场景和多场景基准上分别取得了 45.9%（$\Delta=32\%$）和 46.3%（$\Delta=35.1\%$）的成对胜率，远超所有测试时优化基线。

## 整体框架

VISTA 将视频生成质量的测试时优化建模为一个**可解释的、结构化的自修正循环**，其核心洞察在于：将人类式的迭代改进过程——分解、比较、批判、反思——映射为由多个专用代理协作执行的计算流程。整个框架围绕一个统一的闭环工作流构建，如 Figure 1 所示，包含**初始化阶段**和**自改进阶段**两大组成部分，共四个关键模块协同运作。

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/002_Figure_1.jpg]]
*Figure 1: | The workflow of our proposed multi-agent framework, VISTA. : MLLM Agent; : Adversarial MLLM Agent; : Video Generation Agent*

### 管道总览与模块关系

VISTA 的输入是用户的原始视频生成提示，输出是经过多轮迭代优化后的视频及其对应的精炼提示。管道沿以下主线展开：

1. **结构化视频提示规划（PromptPlanner）**：作为初始化阶段的入口，将用户提示解析为具有时序结构的场景序列，每个场景由跨越上下文、视觉和音频三个维度的九个属性定义（包括时长、场景描述、关键对象、镜头运动、音效、氛围音乐、光照、视觉风格、情绪基调）。这一分解过程生成多个候选提示，为后续优化提供多样化的起点。

2. **成对锦标赛选择（PairwiseSelect）**：在初始化阶段和每一轮自改进迭代中，对生成的候选视频执行双向成对比较。通过多轮二进制锦标赛逐步淘汰劣质视频，最终选出最优的视频-提示对。选择过程引入探查式批评和违规惩罚机制，以抑制模型偏见并提高选择可靠性。

3. **多维度多代理批评（MMAC）**：自改进阶段的核心评估引擎。针对视觉、音频和上下文三个维度，构建由**正常法官**、**对抗法官**和**元法官**组成的三元法庭。正常法官给出建设性批评和评分，对抗法官主动寻找缺陷和不足，元法官综合两者形成最终的批评反馈和分数。

4. **深度思考提示代理（DTPA）**：接收 MMAC 产出的多维度批评反馈，执行六步内省推理链——识别视频问题、分析根本原因、关联到提示缺陷、提出具体修改建议、评估修改的潜在影响、审查并精炼建议——最终生成一组有针对性的提示修改方案。

### 输入输出流与迭代机制

整个管道以 5 轮迭代运行：1 轮初始化加 4 轮自改进。每轮迭代中，系统采样 5 个提示，每个提示生成 3 个变体，每个变体生成 2 个视频，共计 30 个视频。初始化阶段以 PromptPlanner 产出的结构化提示作为起点，经 PairwiseSelect 选出最优视频-提示对；自改进阶段则在此对的基础上，由 MMAC 提供多维度批评，DTPA 生成修改建议，再由多模态 LLM 合成一组改进后的候选提示（包含当前最优提示的保留副本），进入下一轮迭代。

框架的关键设计在于**各模块的功能解耦与因果串联**：PromptPlanner 提供高质量的初始化基础，PairwiseSelect 确保迭代改进的稳定性（消融实验表明移除该模块后迭代性能大幅下降），MMAC 通过多角色对抗平衡批评的深度与实用性（仅使用单一法官会导致性能显著退化），DTPA 则将批评转化为可执行的、结构化的提示优化方案。这种模块化设计使得 VISTA 能够作为黑盒优化层适配不同的 T2V 模型（如 Veo 2 和 Veo 3），无需修改底层生成模型的参数。

## 核心模块与公式推导

VISTA 将视频生成优化建模为一个可解释的、结构化的自修正循环，其核心由四个模块构成：**PromptPlanner**（结构化视频提示规划）、**PairwiseSelect**（成对锦标赛选择）、**MMAC**（多维度多代理批判）和 **DTPA**（深度思考提示代理）。这些模块协同工作，在测试时通过多轮迭代自动改进视频的视觉、音频和上下文质量。

---

### 初始化阶段

#### PromptPlanner：结构化视频提示规划

用户输入的原始提示 $P$ 首先被解析为具有时序关系的场景序列。每个提示候选定义为：

$$P_i := [S_{i,1}, S_{i,2}, \ldots]$$

其中每个场景配置 $S$ 包含九个属性，覆盖上下文、视觉和音频三个维度：(1) 时长，(2) 场景描述，(3) 关键对象，(4) 相机运动，(5) 光照，(6) 色彩调性，(7) 音效，(8) 背景音乐，(9) 情绪氛围。这种结构化分解将模糊的用户意图转化为可操作的、多属性的生成指令，为后续迭代优化提供了精细的调控手柄。

#### PairwiseSelect：成对锦标赛选择

从多个候选视频中选择最优视频-提示对时，VISTA 采用双向成对比较策略，而非简单的单次评分。如 Algorithm 2 所示，系统通过二进制锦标赛迭代缩减候选集，最终选出胜者。每对视频 $(V_i, V_j)$ 的得分基于多维度用户标准 $\mathcal{M}_{user}^g$ 进行聚合：

$$s_i \gets \frac{1}{k} \sum_{C \in \mathcal{M}_{user}^g} \left( \delta(C, V_i, V_j) - \lambda \cdot \mathbb{1}(C, V_i) \right)$$

$$s_j \gets \frac{1}{k} \sum_{C \in \mathcal{M}_{user}^g} \left( 1 - \delta(C, V_i, V_j) - \lambda \cdot \mathbb{1}(C, V_j) \right)$$

其中：
- $\delta(C, V_i, V_j)$ 表示在标准 $C$ 下视频 $i$ 相对于视频 $j$ 的比较结果（胜/平/负）；
- $\mathbb{1}(C, V)$ 为违规指示函数，当视频 $V$ 违反标准 $C$ 的硬性约束时触发；
- $\lambda$ 为惩罚权重，用于抑制违规行为；
- $k$ 为标准总数。

该机制的核心优势在于：双向比较消除了位置偏差，探查批评（probing critiques）提供了可解释的选择理由，惩罚项则确保生成结果满足基本约束。

---

### 自优化阶段

#### MMAC：多维度多代理批判

针对每一评价维度 $D \in \mathcal{D}$（视觉、音频、上下文），VISTA 构造一个三元法官法庭：

$$\{C_D, S_D\} = J_D(P, V^*, P^*) \quad \text{(Normal Judge)}$$

$$\{C_D^-, S_D^-\} = J_D^-(P, V^*, P^*) \quad \text{(Adversarial Judge)}$$

$$\{C_D^*, S_D^*\} = J_D^*(P, C_D, S_D, C_D^-, S_D^-) \quad \text{(Meta Judge)}$$

三个法官各司其职：
- **正常法官** $J_D$：基于原始提示 $P$、当前视频 $V^*$ 和当前提示 $P^*$，给出建设性批评 $C_D$ 和分数 $S_D$；
- **对抗法官** $J_D^-$：主动寻找视频中的缺陷和违规，生成对抗性批评 $C_D^-$ 和分数 $S_D^-$；
- **元法官** $J_D^*$：综合前两者的输出，平衡批评的深度与实用性，生成最终批评 $C_D^*$ 和分数 $S_D^*$。

消融实验证实，仅使用单一法官（如仅 Normal 或仅 Adversarial）会导致性能显著下降——单场景 Win 率分别降至 17.2% 和 42.0%，远低于完整三元结构的 45.9%，说明正常与对抗视角的互补性是批判质量的关键。

#### DTPA：深度思考提示代理

获得多维度反馈 $\mathcal{F}$ 后，DTPA 不直接生成新提示，而是执行六步内省推理链来建议提示修改：

$$\mathcal{M} := \{M_1, \ldots\} = \mathrm{DTPA}(P, P^*, \mathcal{F})$$

六步推理包括：(1) 识别视频问题，(2) 追溯问题到提示层面的根本原因，(3) 生成候选修改方案，(4) 评估每个方案的预期效果，(5) 选择最优修改，(6) 审查并精炼。随后，多模态 LLM 根据修改建议集 $\mathcal{M}$ 生成一组改进的提示候选：

$$\mathcal{P} := \{P_1, \ldots, P_n, P^*\} \gets \mathrm{MLLM}(P, P^*, \mathcal{M})$$

其中保留当前提示 $P^*$ 作为候选之一，确保迭代过程不会退化。消融实验表明，移除 DTPA 后单场景 Win 率从 45.9% 降至 37.8%，验证了深度推理对提示优化质量的决定性作用。

---

### 模块间因果机制

四个模块形成一条因果链：**PromptPlanner** 提供高质量初始化（消融中 Init 单场景 Win 率从 35.5% 降至 25.2%），**PairwiseSelect** 稳定迭代改进（移除后 Iter 5 从 45.9% 降至 33.3%），**MMAC** 提供多维度、多视角的精准反馈，**DTPA** 将反馈转化为可执行的提示修改。任一模块缺失都会导致性能显著退化，表明它们各自承担不可替代的功能。

### 补充图表

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/024_Figure_12.jpg]]
*Figure 12: | Examples of prompts optimized by VISTA across iterations. Blue parts are updated*

## 实验与分析

### 主要定量结果：VISTA 在单/多场景基准上显著超越所有基线

VISTA 的核心性能通过**成对胜率（Win Rate）** 相对于直接提示（Direct Prompting, DP）来度量。DP 作为参考基线，其胜率定义为 0%。在单场景和多场景两个基准上，VISTA 均展现出显著的测试时自我改进能力，且改进幅度随迭代次数持续增长。

**Table 2** 汇总了 VISTA 与各基线方法在 5 轮迭代（1 轮初始化 + 4 轮自我改进）中的胜/平/负率及 Δ（Win − Loss）值。在单场景基准（MovieGenVideo，100 条提示）上，VISTA 在初始化阶段即获得 **35.5% 胜率、50.1% 平局率、14.4% 负率，Δ = 21.1%**；经过 4 轮自我改进后，最终胜率达到 **45.9%，Δ = 32.0%**。在多场景基准（内部数据集，161 条提示）上，VISTA 的初始化胜率为 **37.8%，Δ = 27.9%**，最终胜率达到 **46.3%，Δ = 35.1%**。

相比之下，其他测试时优化基线表现显著逊色：
- **Visual Self-Refine (VSR)**（Madaan et al., 2023）在单场景最终 Δ 仅为 4.0%，多场景为 6.2%；
- **VSR++**（扩展至匹配 VISTA 的视频生成数量）在单场景 Δ 为 7.3%，多场景为 10.0%；
- **Rewrite**（基于 Vertex AI 指南的提示重写）在单场景 Δ 为 5.0%，多场景为 6.2%；
- **VPO**（Cheng et al., 2025b）在单场景 Δ 为 8.0%，多场景为 6.8%。

VISTA 相对于最强基线的胜率增量（Δ 差值）在单场景达 **+24.0%**，多场景达 **+25.1%**，表明其多维度多代理自优化框架在测试时计算扩展方面具有显著优势。

**Figure 2** 进一步展示了 VISTA 与 DP 在两个基准上的平均胜/平/负率，直观呈现了 VISTA 在绝大多数案例中优于或持平于直接提示，且负率维持在较低水平。

### 传统指标评估：视觉、音频与文本-视频对齐的全面提升

除成对胜率外，VISTA 在传统自动评估指标上也展现出持续改进趋势。**Figure 3** 和 **Tables 5-6** 报告了使用 VBench 的 any-video 评估指标（视觉质量）、NISQA 指标（音频质量）以及 CLIP-Score（文本-视频对齐）的结果。

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/005_Figure_3.jpg]]
*Figure 3: | Evaluation results using conventional metrics on single-scene (a) and multi-scene (b) benchmarks. Numerical results are provided in Tables 5 and 6*

在单场景和多场景基准上，VISTA 的视觉质量分数和音频质量分数均随迭代轮次单调上升，CLIP-Score 也呈现正向改进趋势。这表明 VISTA 的优化不仅提升了 MLLM-as-a-Judge 评估下的相对偏好，也切实改善了视频的底层视觉保真度、音频质量和语义对齐程度。

### 人类评估：VISTA 在 66.4% 的比较中被人类偏好

为验证自动评估结果与人类主观判断的一致性，作者进行了人类评估实验。**Figure 4** 总结了人类评估结果：在 VISTA 与各基线（DP、VSR、VSR++、Rewrite、VPO）的成对比较中，人类评估者在 **66.4%** 的比较中偏好 VISTA 的输出。这一结果与自动评估的胜率趋势高度一致，表明 VISTA 的改进切实符合人类对视频质量、音频质量和上下文连贯性的主观期望。

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/006_Figure_4.jpg]]
*Figure 4: | Summary of human results. The individual annotators’ results are in Appx.-Table 7*

### 消融实验：四个核心组件各自贡献独特且不可替代

**Table 3** 报告了在半个基准上进行的消融实验结果，系统验证了 VISTA 四个核心组件的独立贡献：

1. **移除 PromptPlanner（结构化提示规划）**：初始化阶段的单场景胜率从 **35.5% 降至 25.2%**，多场景从 37.8% 降至 31.1%。这表明结构化时序场景分解和九属性场景配置对生成高质量初始视频至关重要。

2. **移除 PairwiseSelect（成对锦标赛选择）**：迭代改进过程变得不稳定，最终单场景胜率从 **45.9% 降至 33.3%**，多场景从 46.3% 降至 38.9%。双向成对比较、探查批评和惩罚机制共同保障了视频选择的质量和迭代优化的稳定性。

3. **仅使用单一法官**：当仅使用 Normal Judge 时，单场景胜率降至 **17.2%**，多场景降至 33.3%；当仅使用 Adversarial Judge 时，单场景胜率为 42.0%，多场景为 26.7%。结果表明，Normal Judge 和 Adversarial Judge 的组合能平衡批评的深度与有用性，Meta Judge 的整合进一步提升了批评质量。

4. **移除 DTPA（深度思考提示代理）**：提示优化效果显著下降，单场景胜率从 **45.9% 降至 37.8%**，多场景从 46.3% 降至 42.2%。六步内省推理机制对生成有针对性的提示修改建议起到了关键作用。

### 迭代次数扩展分析

**Figure 6** 展示了迭代次数对性能的影响。在单场景和多场景基准上，VISTA 的胜率随迭代次数增加而持续提升，未出现明显的性能饱和或退化迹象。这验证了 VISTA 框架在测试时计算扩展方面的有效性，也暗示了进一步增加迭代次数可能带来额外收益。

### 跨模型泛化：Veo 2 上的性能验证

**Table 4** 报告了 VISTA 在 Veo 2 视频生成模型上的泛化性能。结果表明，VISTA 框架能够有效适配不同的 T2V 后端模型，在 Veo 2 上同样实现了显著的测试时自优化增益。这验证了 VISTA 作为黑盒提示优化框架的模型无关特性。但需注意，不同模型上的提升幅度存在差异，对更多架构的泛化性仍需进一步验证。

### 失败模式与局限性

尽管 VISTA 在多数案例中实现了显著改进，但仍存在以下局限和失败模式：

1. **计算成本高昂**：VISTA 每次迭代消耗约 **0.7M tokens** 并生成约 **28 个视频**（Figure 5），完整的 5 轮迭代需要大量 MLLM API 调用和视频生成资源，可能不适用于资源受限场景。

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/007_Figure_5.jpg]]
*Figure 5: | Cost analysis. Left: total token consumption, including both input and output tokens per iteration. Right: number of newly sampled videos per iteration. Results are averaged over two datasets. Tokens for video generation are unavailable and thus excluded*

2. **模型能力依赖**：框架性能高度依赖于底层 MLLM 和 T2V 模型的能力。当底层模型本身存在严重缺陷时，提示优化可能无法完全弥补生成质量的不足。

3. **场景过渡与复杂提示**：多场景视频中场景过渡的完全流畅性仍有提升空间；对于高度复杂或内部矛盾的用户提示，结构化规划可能无法完美分解所有语义要素。

4. **评估主观偏差**：尽管采用了双向成对比较和位置交换等公平性措施，完全自动化的 MLLM-as-a-Judge 评估策略仍可能存在与人类偏好不完全一致的主观偏差。

### 补充图表

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/003_Table_2.jpg]]
*Table 2: | Win/Tie/Loss rates and Δ = Win − Loss across 5 iterations. † refers to our scaled-up results, and underlines are results evaluated on half of the benchmark*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/004_Figure_2.jpg]]
*Figure 2: | Average win/tie/lose between VISTA and Direct Prompting (DP) on two benchmarks. The individual benchmark results are in Section A.5*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/008_Table_3.jpg]]
*Table 3: | Ablation results evaluated on half of the benchmarks. Each module in VISTA contributes uniquely: PromptPlanner enhances initialization, PairwiseSelect stabilizes iterative improvements, combining both Judges balances critiques’ depth and usefulness, and DTPA enables effective prompt refinement*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/009_Figure_6.jpg]]
*Figure 6: | Effect of scaling the #iterations on performance. Left: Single-scene. Right: Multi-scene*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/010_Table_4.jpg]]
*Table 4: | Veo 2 performance with VISTA on both datasets*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/011_Table_5.jpg]]
*Table 5: | Single-scene: Evaluation results using VBench’s any-video evaluation metrics for visual quality, NISQA metrics for audio quality, and CLIP-Score for text-video alignment*

![[assets/figures/papers/paper_list_l2625_https_arxiv_org_abs_2510_15831/figures/012_Table_6.jpg]]
*Table 6: | Multi-scene: Evaluation results using VBench’s any-video evaluation metrics for visual quality, NISQA metrics for audio quality, and CLIP-Score for text-video alignment*

## 方法谱系与知识库定位

### 测试时优化：从文本到视频的迁移

VISTA 的核心贡献在于将**黑盒测试时优化**的思路从大语言模型和图像生成领域系统性地迁移到文本到视频（T2V）生成。在 LLM 领域，**Visual Self-Refine**（Madaan et al., 2023）等工作已证明，通过多模态大语言模型（MLLM）对生成结果进行迭代评估和反馈，可以在不更新模型参数的前提下显著提升输出质量。VISTA 继承了这一“生成-评估-优化”的闭环范式，但面临视频生成独有的挑战：视频质量涉及视觉保真度、音频同步、场景过渡和叙事连贯性等多个正交维度，单一维度的反馈不足以驱动有效改进。

在图像生成领域，**VPO**（Cheng et al., 2025b）等方法通过无害性、准确性和有用性等原则扩展用户提示，展示了提示优化在视觉生成中的潜力。Google Cloud 的 **Rewrite** 基线（2024）则基于 Vertex AI 指南直接重写用户提示。然而，这些方法本质上仍是单次重写或单维度评估，缺乏对视频多维度质量的联合建模和结构化迭代机制。VISTA 首次在视频生成领域将测试时优化建模为**多代理协作的迭代自修正系统**，填补了这一空白。

### 多代理批判架构的谱系定位

VISTA 的三元法官系统（Normal Judge、Adversarial Judge、Meta Judge）在多代理协作的方法谱系中占据独特位置。与简单的多模型投票或单模型多轮评估不同，VISTA 为每个评估维度（视觉、音频、上下文）构建了具有明确角色分工的批判法庭：

- **Normal Judge** 负责正面评估，给出建设性批评和分数；
- **Adversarial Judge** 主动寻找缺陷和违规，扮演“魔鬼代言人”角色；
- **Meta Judge** 综合两者输出，形成平衡的最终批评。

这种三元结构的设计动机在于：单一法官容易陷入评估偏差——过于宽容则无法发现深层问题，过于苛刻则可能产生无用反馈。消融实验证实了这一设计直觉：仅使用 Adversarial Judge 时，单场景 Δ 降至 42.0（完整 VISTA 为 45.9%），多场景降至 26.7；仅使用 Normal Judge 时，单场景 Δ 仅为 17.2，多场景为 33.3。两者结合才能平衡批评的深度和有用性。

### 结构化规划与深度思考的协同

VISTA 的另一个方法创新在于将**结构化视频规划**（PromptPlanner）与**深度思考提示优化**（DTPA）耦合。PromptPlanner 将用户提示分解为具有时序和 9 种属性（时长、视觉元素、音频、情绪等）的场景序列，为后续迭代提供了高质量的初始化。这与直接使用原始提示的基线（DP、Rewrite、VPO）形成鲜明对比——后者缺乏对视频时间结构的显式建模。

DTPA 则进一步引入六步内省推理链：（1）识别视频问题，（2）分析根本原因，（3）提出修改假设，（4）预测修改效果，（5）评估潜在副作用，（6）审查和优化建议。这种深度思考机制超越了简单的“根据反馈重写提示”模式，使提示优化具有因果推理能力。消融实验表明，移除 DTPA 后单场景 Δ 从 45.9% 降至 37.8%，验证了深度思考对提示优化的关键作用。

### 成对锦标赛选择的设计逻辑

在视频选择策略上，VISTA 采用**双向成对锦标赛**（PairwiseSelect）而非单次评分或简单排序。这一设计借鉴了强化学习中基于人类偏好的比较范式，并通过两个机制增强鲁棒性：

1. **双向比较**：交换视频位置以避免位置偏差；
2. **探查批评与惩罚机制**：在比较过程中主动识别违规行为并施加惩罚项 λ。

成对比较的评分公式为：

$$s_i \gets \frac { 1 } { k } \sum _ { C \in \mathcal{M}_{user}^{g} } ( \delta ( C , V _ { i } , V _ { j } ) - \lambda \cdot \mathbb{ 1 } ( C , V _ { i } ) ) , \quad s _ { j } \gets \frac { 1 } { k } \sum _ { C \in \mathcal{M}_{user}^{g} } ( 1 - \delta ( C , V _ { i } , V _ { j } ) - \lambda \cdot \mathbb{ 1 } ( C , V _ { j } ) )$$

其中 δ 表示胜负平结果，1 为违规指示函数。消融实验中，移除 PairwiseSelect 后迭代改进变得不稳定，单场景 Iter 5 的 Δ 从 45.9% 降至 33.3%，说明成对锦标赛对稳定迭代优化至关重要。

### 适用边界与局限

VISTA 的适用边界受以下因素制约：

1. **计算成本**：每次迭代消耗约 0.7M tokens 和 28 次视频生成（5 个提示 × 3 个变体 × 2 个视频，加上选择阶段的额外生成），在资源受限场景下不适用。成本分析（Figure 5）显示，token 消耗和视频采样数随迭代线性增长。

2. **底层模型依赖**：VISTA 的性能上限受限于所使用的 MLLM 和 T2V 模型。在 Veo 2 上的泛化实验（Table 4）显示，虽然 VISTA 仍能带来提升，但增益幅度因底层模型能力而异，尚未在更多 T2V 架构（如扩散模型之外的方案）上验证。

3. **评估维度的覆盖**：当前 MMAC 覆盖视觉、音频和上下文三个维度，但可能无法完全捕捉用户偏好的所有细微差异（如风格一致性、文化适配性等）。完全自动化的评估策略存在主观偏差。

4. **多场景过渡**：多场景视频中场景过渡的完全流畅性仍有提升空间，高度复杂或矛盾的用户提示处理能力有限。

### 开放问题

当前工作留下若干待探索方向：

- **惩罚机制的细粒度设计**：惩罚项 λ 和违规指示函数 1(C,V) 的具体定义及在不同场景下的最优设置尚未系统研究，可能影响选择策略的鲁棒性。
- **用户自定义评估标准**：如何将用户自定义的评估标准和约束融入 MMAC 框架，实现个性化视频优化，是一个有前景的方向。
- **更大规模扩展**：VISTA 在 5 次迭代内已展示扩展定律（Figure 6），但能否扩展到更多迭代次数或适应更大规模的视频生成模型（如超越 Veo 3）仍需验证。
- **评估可扩展性**：当前人类评估依赖独立注释者，如何使视频质量的人类评估更具可扩展性和更低成本，以适应更大规模实验，是实际部署中的关键挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/VISTA_A_Test_Time_Self_Improving_Video_Generation_Agent.pdf]]