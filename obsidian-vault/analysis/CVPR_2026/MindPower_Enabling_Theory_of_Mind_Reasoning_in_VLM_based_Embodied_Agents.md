---
title: "MindPower: Enabling Theory-of-Mind Reasoning in VLM-based Embodied Agents"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MindPower_Enabling_Theory_of_Mind_Reasoning_in_VLM_based_Embodied_Agents.pdf
project_link: "https://zhangdaxia22.github.io/MindPower/"
code_link: null
aliases:
- MindPower
tags:
- CVPR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 引入机器人中心视角（Robot-Centric Perspective），通过 MindPower 推理层次（从感知到动作的六层结构）连接心理状态推理与行动，并利用 Mind-Reward 强化优化框架对齐中间推理状态与最终动作，保证了推理与行为的一致性。
primary_logic: 将心理理论（ToM）形式化为信念-欲望-意图（BDI）认知结构，并将其与具身智能体的感知、决策和行动无缝衔接，通过显式的推理层次和一致性奖励强化学习，首次实现了从多模态感知到机器人中心辅助动作的端到端连贯推理。
claims:
- 去除 MindPower 推理层次导致 GPT-4o 的决策精度下降 1.24%，动作生成精度从 2.91% 降至 0.82%。
- 使用标准逐步推理替代 MindPower 层次，决策精度下降 4.89%，动作精度从 2.91% 降至 0.90%，证明该层次结构的有效性。
- 本文模型在决策制定上超越 GPT-4o 12.77%，在动作生成上超越 12.49%，验证了 Mind-Reward 和 Robot-Centric 设计的效果。
- MindPower Benchmark (Decision Making) 上 决策精度提升（相对GPT-4o） = Ours (SFT+Mind-Reward)
---

# MindPower: Enabling Theory-of-Mind Reasoning in VLM-based Embodied Agents

> [!tip] 核心洞察
> 将心理理论（ToM）形式化为信念-欲望-意图（BDI）认知结构，并将其与具身智能体的感知、决策和行动无缝衔接，通过显式的推理层次和一致性奖励强化学习，首次实现了从多模态感知到机器人中心辅助动作的端到端连贯推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | MindPower: 在基于VLM的具身智能体中实现心理理论推理 |
| 英文题名 | MindPower: Enabling Theory-of-Mind Reasoning in VLM-based Embodied Agents |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.23055) · [Project](https://zhangdaxia22.github.io/MindPower/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | MindPower |
| Dataset | MindPower Benchmark |

> [!tip] 效果简介
> - MindPower Benchmark (Decision Making) 上，决策精度提升（相对GPT-4o） Ours (SFT+Mind-Reward) vs GPT-4o (+12.77%)。
> - MindPower Benchmark (Action Generation) 上，动作生成精度提升（相对GPT-4o） Ours (SFT+Mind-Reward) vs GPT-4o (+12.49%)。
> - MindPower Benchmark (Action Success Rate) 上，SR (Success Rate) 11.75 (SFT+Mind-Reward) vs 0.29 (Qwen2.5-VL-7B-Instruct, video-input) (+11.46)。

## 概述

具身智能体在家庭服务等交互场景中，不仅需要感知物理环境，更需理解自身与他人的心理状态，以做出连贯的决策与行动。这种能力被称为**心理理论（Theory of Mind, ToM）**。然而，现有视觉-语言模型（VLM）驱动的智能体普遍缺乏显式的ToM推理能力：它们要么仅从旁观者视角推断人类角色的心理状态，要么将感知到行动的映射视为黑箱，无法从**机器人中心视角（Robot-Centric Perspective）**同时推理智能体自身与人类的信念、欲望与意图，更无法基于此生成可执行的动作序列。这一瓶颈导致VLM在需要二阶信念推理、错误信念纠正与隐式目标推断的具身任务中表现极差——例如，GPT-4o在动作生成上的精度仅为2.91%。

针对上述问题，本文提出**MindPower**，一个面向VLM具身智能体的机器人中心ToM推理与决策框架。其核心思想是将心理理论形式化为**信念-欲望-意图（BDI）认知结构**，并将其与感知、决策、行动无缝衔接，通过显式的推理层次与一致性奖励优化，首次实现从多模态输入到辅助动作的端到端连贯推理。

MindPower的核心贡献包括：
- **MindPower推理层次**：设计了从`<Perception>`到`<Action>`的三层六步推理结构，将心理状态推理与具身行动生成统一在同一框架内。
- **MindPower基准测试**：构建了包含590个交互式家庭场景的评测集，涵盖错误信念纠正与隐式目标推断与完成两大任务，首次系统评估VLM在机器人中心ToM下的决策与动作生成能力。
- **Mind-Reward优化框架**：提出结合原子级准确性、局部一致性与全局一致性的强化奖励，显式约束中间推理状态与最终行动的对齐，并结合GRPO进行策略优化。

实验结果表明，MindPower在决策制定上超越GPT-4o **12.77%**，在动作生成上超越**12.49%**。消融研究进一步证实：移除MindPower推理层次或替换为标准逐步推理，均会导致性能大幅下降，验证了该层次结构的独特优势。

**方法定位**：MindPower属于具身智能体认知架构与VLM推理增强的交叉领域。其BDI形式化可追溯至经典认知科学，但将其与多模态VLM和强化学习结合，构建可评估、可优化的ToM推理管道，是本文的方法学创新。与现有ToM基准（如MuMA-ToM、TOMATE等）仅关注人类角色心理状态的多选题评估不同，MindPower首次引入机器人中心视角和Level-3决策与行动层评估，填补了从心理推理到具身执行之间的空白。

## 背景与动机

### 具身智能中的心理理论推理缺口

在真实世界的人机协作场景中，具身智能体（embodied agents）不仅需要理解物理环境，还必须理解人类伙伴的心理状态——例如信念、欲望和意图——才能做出恰当、连贯的决策与行动。这种能力在认知科学中被称为**心理理论**（Theory of Mind, ToM）。然而，当前基于视觉-语言模型（VLM）的具身智能体普遍缺乏显式的ToM推理能力，无法从机器人自身的视角同时推理自己和他人的心理状态，导致其决策与动作生成缺乏连贯性和情境适应性。

现有的ToM基准测试（如MuMA-ToM等）存在两个关键局限：**第一，视角单一**——它们仅关注视频中人类角色的心理状态推理，完全忽略了智能体自身的心理状态，从而无法评估智能体在交互中“换位思考”的能力；**第二，任务不完整**——这些基准通常仅要求模型通过选择题（MCQ）回答关于角色心理状态的问题，不涉及基于推理结果生成连贯决策和可执行动作的能力，割裂了“推理”与“行动”之间的闭环。

### 从推理到行动的断裂

具身智能的核心挑战在于将感知、心理推理、决策与行动无缝衔接。现有VLM即使具备一定的推理能力，其推理过程也往往是“角色中心”（Role-Centric）的——模型站在旁观者角度分析视频中的人类行为，而非以机器人第一人称视角（Robot-Centric）同时建模自身与交互对象的心理状态。这种断裂导致模型在需要**错误信念纠正**（False-Belief Correction）或**隐式目标推断与补全**（Implicit Goal Inference & Completion）等复杂社交场景中表现不佳，无法生成既符合社交规范又满足任务目标的动作序列。

### MindPower的动机与定位

针对上述缺口，本文提出**MindPower**框架，核心动机在于：将心理理论形式化为**信念-欲望-意图**（Belief-Desire-Intention, BDI）认知结构，并将其与具身智能体的感知、决策和行动无缝衔接。具体而言，MindPower引入三个关键设计：

1. **机器人中心视角**（Robot-Centric Perspective）：要求模型同时推理智能体自身和人类的信念、欲望与意图，实现真正的“换位思考”；
2. **MindPower推理层次**（MindPower Reasoning Hierarchy）：将推理过程结构化为从感知到行动的六层显式链——`<Perception>` → `<Belief>` → `<Desire>` → `<Intention>` → `<Decision>` → `<Action>`——为评估推理到行动的连贯性提供了标准化框架；
3. **Mind-Reward优化框架**：通过强化学习奖励信号，显式约束中间推理状态与最终动作的一致性，确保推理与行为对齐。

通过这些设计，MindPower首次实现了从多模态感知到机器人中心辅助动作的端到端连贯推理，为具身智能体的社交认知能力提供了可量化、可优化的基准与方法。

## 核心创新

MindPower 的核心创新在于将心理理论（Theory of Mind, ToM）从单纯的角色心理状态识别，推进到以机器人为中心的连贯推理与行动生成。其关键突破体现在三个维度。

### 推理视角：从角色中心到机器人中心

现有 ToM 基准（如 MuMA-ToM）仅要求模型从旁观者视角推理视频中人类角色的心理状态，且输出形式多为选择题。MindPower 首次提出**机器人中心（Robot-Centric）视角**，要求具身智能体同时推理自身和人类的信念、欲望与意图。具体而言，在 Level-2 心理推理层，模型不仅需要推断人类角色“认为物体在哪里”（一阶信念），还需推理“智能体预测人类认为物体在哪里”（二阶信念），并将这些心理状态直接服务于后续的决策与动作生成。这一设计使心理推理与具身行动之间建立了因果关联，而非彼此孤立。

### 推理结构：BDI 认知架构驱动的六层推理层次

MindPower 将心理理论形式化为**信念-欲望-意图（BDI）认知结构**，并构建了从感知到动作的六层推理层次：

1. **`<Perception>`**：从多模态输入中感知环境和人类行为；
2. **`<Belief>`**：推理智能体自身及人类角色的信念（含二阶信念）；
3. **`<Desire>`**：推导智能体的目标或期望状态；
4. **`<Intention>`**：形成具体的行动意图；
5. **`<Decision>`**：做出自主决策；
6. **`<Action>`**：生成可执行的原子动作序列。

该层次结构（Figure 2）将推理过程标准化为三个层级：感知层（Level-1）、心理推理层（Level-2）、决策与行动层（Level-3）。与通用逐步思考链（`<think> ... </think>`）相比，这一显式结构提供了可解释的推理轨迹，并允许对各层进行独立评估。消融实验证实了其独特价值：移除该层次后，GPT-4o 的决策精度下降 1.24%，动作生成精度从 2.91% 降至 0.82%；若替换为标准逐步推理，决策精度下降 4.89%，动作精度降至 0.90%。

### 优化目标：Mind-Reward 强化对齐框架

传统方法仅依赖监督微调（SFT）或通用最大似然估计，难以保证中间推理状态与最终动作的一致性。MindPower 提出 **Mind-Reward**，从三个互补维度评估推理质量：

- **原子准确性（Atomic Accuracy）**：通过 ROUGE-1 衡量单个动作的匹配度；
- **局部一致性（Local Consistency）**：通过 ROUGE-2 评估相邻动作对的连贯性；
- **全局一致性（Global Consistency）**：通过 ROUGE-L 评估整体推理序列与动作的协调性。

三者加权组合为 Mind-Reward：

$$R _ { \mathrm { M i n d } } = \alpha _ { 1 } R _ { \mathrm { a t o m i c } } + \alpha _ { 2 } R _ { \mathrm { l o c a l } } + \alpha _ { 3 } R _ { \mathrm { g l o b a l } }$$

该奖励与格式奖励（Format-Reward）叠加后，通过分组相对策略优化（GRPO）对模型进行强化学习训练。训练采用两阶段范式：先以 SFT 建立基础推理对齐，再以 GRPO 结合 Mind-Reward 进行优化。消融实验表明，仅用 SFT 可带来一定提升，但结合 Mind-Reward 后性能显著增强；若跳过 SFT 直接使用 Mind-Reward，整体性能仍不理想，验证了 SFT 作为冷启动的必要性。

### 训练范式：SFT + GRPO 两阶段训练

MindPower 采用**两阶段训练**策略，将监督微调与强化学习有机结合。第一阶段通过 SFT 使模型掌握 MindPower 推理层次的基本格式和推理逻辑；第二阶段利用 GRPO 结合 Mind-Reward 和 Format-Reward 进行策略优化，显式约束心理状态与行动的一致性。这种范式使模型在 MindPower Benchmark 上超越 GPT-4o：决策精度提升 12.77%，动作生成精度提升 12.49%，动作成功率（SR）从基座模型 Qwen2.5-VL-7B-Instruct 的 0.29 提升至 11.75。

## 整体框架

MindPower 构建了一个以机器人为中心（Robot-Centric）的心理理论推理与具身行动框架，其核心目标是将视觉-语言模型（VLM）从被动的感知与问答提升为能够自主推理自身与他人心理状态并据此生成连贯动作的具身智能体。该框架围绕三个关键设计展开：**MindPower 推理层次**（MindPower Reasoning Hierarchy）、**Mind-Reward 一致性优化**，以及**两阶段训练范式**。

### 推理层次：从感知到行动的六层结构

MindPower 推理层次是整个框架的认知骨架，它将心理理论（ToM）形式化为三层六步的递进结构（见 Figure 2），实现了从多模态输入到可执行动作的端到端推理链：

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/002_Figure_2.jpg]]
*Figure 2: MindPower Reasoning Hierarchy. The agent first receives multimodal input, then performs mental reasoning to form beliefs, desires, and intentions, and finally makes decisions and generate action plan based on this reasoning*

- **Level-1 感知层（`<Perception>`）**：智能体从多模态输入（视频帧与环境状态）中感知场景中的物体、事件和人类行为，形成对当前情境的客观描述。
- **Level-2 心理推理层**：这是框架的认知核心，包含三个子层：
  - **`<Belief>`**：推理智能体自身的信念以及它对场景中人类角色信念的预测（即二阶信念推理）。例如，智能体需要判断人类是否持有错误信念。
  - **`<Desire>`**：基于信念状态，推导智能体自身的目标或期望状态（如“帮助人类纠正错误信念”）。
  - **`<Intention>`**：将欲望转化为具体的行动意图（如“引导人类查看正确的物品位置”）。
- **Level-3 决策与行动层**：
  - **`<Decision>`**：基于心理推理结果做出自主决策（如选择采取纠正性辅助行为）。
  - **`<Action>`**：将决策分解为可执行的原子动作序列（如 `walk_to_table` → `pick_up_object` → `show_to_human`）。

这一层次结构的关键创新在于其**机器人中心视角**（Robot-Centric Perspective）。现有 ToM 基准测试（如 MuMA-ToM）仅要求模型从第三方视角推理视频中人类角色的心理状态，而 MindPower 要求智能体同时推理**自身**和**人类**的信念、欲望与意图，并将这些心理状态直接桥接到自身的决策与行动生成。Figure 3 清晰展示了这一差异：现有基准仅覆盖视频的前两个阶段（物品被移动、人类离开），而 MindPower 新增了第三阶段（人类返回寻找物品），并要求智能体基于对双方心理状态的完整推理来规划辅助行为。

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/010_Figure_8.jpg]]
*Figure 8: Full Version of Fig. 3 in Manuscript*

### 优化机制：Mind-Reward 一致性约束

单纯的监督微调（SFT）无法保证推理链中各层之间以及推理与最终行动之间的一致性。为此，MindPower 引入了 **Mind-Reward** 强化优化框架（见 Figure 5），从三个维度显式约束推理质量：

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/006_Figure_5.jpg]]
*Figure 5: Reward Formulation. The overall reward integrates both the Mind-Reward and the Format-Reward components*

- **原子准确性（Atomic Accuracy）**：通过 ROUGE-1 衡量每个原子动作与真值的匹配度。
- **局部一致性（Local Consistency）**：通过 ROUGE-2 评估相邻动作对之间的连贯性。
- **全局一致性（Global Consistency）**：通过 ROUGE-L 评估整个推理序列与行动序列之间的整体对齐程度。

Mind-Reward 的计算公式为：
$$R _ { \mathrm { M i n d } } = \alpha _ { 1 } R _ { \mathrm { a t o m i c } } + \alpha _ { 2 } R _ { \mathrm { l o c a l } } + \alpha _ { 3 } R _ { \mathrm { g l o b a l } }$$

在训练中，Mind-Reward 与 **Format-Reward**（检查六层输出格式是否正确）相加构成总奖励：
$$R = R _ { \mathrm { M i n d } } + R _ { \mathrm { F o r m a t } }$$

这一设计确保了中间推理状态（信念、欲望、意图）不仅自身合理，而且与最终的行动决策保持因果一致，从而避免“推理正确但行动错误”或“行动正确但推理脱节”的断裂问题。

### 训练范式：SFT 冷启动 + GRPO 强化优化

MindPower 采用两阶段训练流程：

1. **监督微调（SFT）**：首先在构建的 MindPower 数据集上进行监督微调，使模型建立基本的推理格式对齐和 BDI 认知结构。消融实验表明，跳过 SFT 直接进行强化学习会导致性能显著低于完整流程，验证了 SFT 作为冷启动的必要性。
2. **分组相对策略优化（GRPO）**：在 SFT 基础上，使用 GRPO 算法结合 Mind-Reward 和 Format-Reward 进行强化优化。GRPO 通过组内标准化优势函数 $A _ { i } = { \frac { R _ { i } - \operatorname* { m e a n } ( \{ R _ { j } \} ) } { \operatorname* { s t d } ( \{ R _ { j } \} ) } }$ 对策略进行裁剪更新，同时加入 KL 散度惩罚以防止策略偏离参考模型过远。

### 数据构建与任务设计

框架的训练和评估建立在两个核心任务之上（见 Figure 1 和 Figure 7）：

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/001_Figure_1.jpg]]
*Figure 1: MindPower Benchmark Overview. We evaluate Robot-Centric ToM through two tasks: False-Belief Correction and Implicit Goal Inference & Completion, assessing whether VLM-based embodied agents can generate correct decisions and actions. We further propose the MindPower Reasoning Hierarchy, comprising three levels and six layers. Existing VLMs perform poorly across layers, especially in action reasoning, while our model shows substantial improvements. A detailed example is provided in Supp. Sec. B*

- **错误信念纠正（False-Belief Correction）**：人类角色对物品位置持有错误信念，智能体需要识别这一错误信念并采取行动帮助纠正。
- **隐式目标推断与完成（Implicit Goal Inference & Completion）**：智能体需要从人类行为中推断其未明确表达的意图，并主动协助完成目标。

数据集基于 VirtualHome 仿真器构建，遵循三个原则：（1）**真实性**——场景和动作贴近日常家庭交互；（2）**BDI 一致性**——确保信念、欲望、意图与行动之间的因果逻辑自洽；（3）**仿真器约束下的多样性**——在可用环境和动作集范围内最大化场景变化。最终数据集涵盖 590 个交互式家庭场景，按 8:2 划分训练和测试集。

### 整体输入输出流

整个框架的运行时流程可以概括为：
1. **输入**：多模态视频帧序列（闭源模型平均采样 64 帧，开源模型可选视频直接输入或平均帧输入）。
2. **推理**：模型按照 `<Perception>` → `<Belief>` → `<Desire>` → `<Intention>` → `<Decision>` → `<Action>` 的固定层次生成结构化推理链。
3. **输出**：包含完整的六层推理文本和最终的可执行原子动作序列。
4. **评估**：在感知层和心理推理层使用 BERTScore 和 Sentence Transformer 评分，在决策层使用语义相似度，在动作层使用成功率（SR）和动作正确率（AC）指标，同时引入 **BPC（BDI and Perspective Consistency）** 评分和人工评估作为参照。

这一框架的核心洞察在于：将心理理论形式化为 BDI 认知结构，并将其与具身智能体的感知、决策和行动无缝衔接，通过显式的推理层次和一致性奖励强化学习，首次实现了从多模态感知到机器人中心辅助动作的端到端连贯推理。

### 补充图表

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/022_Figure_14.jpg]]
*Figure 14: Illustration of the Environment from Different Perspectives*

## 核心模块与公式推导

### MindPower 推理层次：三层六步的认知流水线

MindPower 的核心是将心理理论（ToM）形式化为一个从感知到行动的显式推理层次，共包含三个层级、六个步骤（Figure 2）。该层次结构将信念-欲望-意图（BDI）认知模型与具身智能体的决策-行动生成无缝衔接，首次实现了从多模态感知到机器人中心辅助动作的端到端连贯推理。

**Level-1 感知层**：`<Perception>` 模块从多模态输入（视频帧序列）中提取环境状态和人类行为信息，为后续心理推理提供事实基础。

**Level-2 心理推理层**：这是 MindPower 区别于现有 ToM 基准的核心创新。该层采用**机器人中心视角（Robot-Centric Perspective）**，同时推理智能体自身和场景中人类的心理状态：
- `<Belief>`：推理智能体自身的信念以及**二阶信念**——即智能体预测人类角色对环境的信念。这是错误信念纠正任务的基础能力。
- `<Desire>`：推导智能体在当前情境下的目标或期望状态。
- `<Intention>`：基于信念和欲望，形成具体的行动意图。

**Level-3 决策与行动层**：将心理推理结果转化为可执行输出：
- `<Decision>`：做出自主决策（如选择帮助人类纠正错误信念）。
- `<Action>`：生成可执行的原子动作序列（如 `walk to table`, `pick up cup`）。

该层次结构的必要性已通过消融实验得到验证：去除 MindPower 推理层次后，GPT-4o 的决策精度下降 1.24%，动作生成精度从 2.91% 降至 0.82%；若用标准逐步推理（`<think> ... </think>`）替代，决策精度进一步下降 4.89%，动作精度降至 0.90%。

### Mind-Reward：心理一致性的强化优化

为约束推理链中中间心理状态与最终动作的一致性，MindPower 提出了 **Mind-Reward** 奖励函数，从三个互补维度评估推理质量：

$$R_{\mathrm{Mind}} = \alpha_{1} R_{\mathrm{atomic}} + \alpha_{2} R_{\mathrm{local}} + \alpha_{3} R_{\mathrm{global}}$$

其中：
- **原子准确性（Atomic Accuracy）** $R_{\mathrm{atomic}}$：基于 ROUGE-1 衡量单个推理步骤与真值的匹配度，确保每一步推理的独立正确性。
- **局部一致性（Local Consistency）** $R_{\mathrm{local}}$：基于 ROUGE-2 评估相邻推理步骤对之间的连贯性，约束推理链的逻辑平滑过渡。
- **全局一致性（Global Consistency）** $R_{\mathrm{global}}$：基于 ROUGE-L 衡量整个推理序列与真值序列的全局对齐，保证从感知到行动的端到端一致性。

总奖励函数结合了心理一致性奖励与格式正确性奖励：

$$R = R_{\mathrm{Mind}} + R_{\mathrm{Format}}$$

其中 $R_{\mathrm{Format}}$ 检查输出是否严格遵循六层格式（`<Perception>` 至 `<Action>` 的标签完整性）。

### 两阶段训练范式与 GRPO 优化

MindPower 采用**监督微调（SFT）+ 分组相对策略优化（GRPO）**的两阶段训练范式：

1. **SFT 冷启动**：在构建的 MindPower 数据集上进行监督微调，建立基础的推理对齐能力。消融实验表明，仅有 Mind-Reward 而无 SFT 初始训练时，模型性能仍远低于完整流程，验证了 SFT 作为冷启动的必要性。

2. **GRPO 强化优化**：使用 Mind-Reward 和 Format-Reward 的组合奖励进行策略优化。GRPO 通过组内标准化优势函数进行策略更新：

$$A_{i} = {\frac {R_{i} - \operatorname*{mean}(\{R_{j}\})} {\operatorname*{std}(\{R_{j}\})}}$$

GRPO 的优化目标为：

$$\begin{array}{rl} {J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_{i}\}_{i=1}^{G} \sim \pi_{\theta_{\mathrm{old}}}({\cal O} | q)}} \\ {\left[ \frac{1}{G} \sum_{i=1}^{G} \operatorname*{min} \left( \frac{\pi_{\theta}(o_{i} | q)}{\pi_{\theta_{\mathrm{old}}}(o_{i} | q)} A_{i}, \right. \right.} \\ {\left. \left. \mathrm{clip} \left( \frac{\pi_{\theta}(o_{i} | q)}{\pi_{\theta_{\mathrm{old}}}(o_{i} | q)}, 1 - \epsilon, 1 + \epsilon \right) A_{i} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \right].} \end{array}$$

该目标包含重要性采样裁剪（防止策略更新过大）和 KL 散度惩罚项（约束策略不偏离参考模型过远），确保训练稳定性。

### 评估指标设计

动作层面的评估采用两个互补指标：

**动作成功率（Success Rate, SR）**：

$$\mathrm{SR} = \frac{2R_{1} + 3R_{2} + 5R_{L}}{10}$$

加权组合 ROUGE-1、ROUGE-2 和 ROUGE-L 得分，其中 ROUGE-L 权重最高（5/10），强调全局序列一致性。

**动作正确率（Action Correctness, AC）**：

$$\mathrm{AC} = \left\lfloor {\frac{|A^{*} \cap {\hat{A}}|}{|{\hat{A}}|}} \right\rfloor$$

衡量生成的动作序列 $\hat{A}$ 与真值 $A^{*}$ 中匹配的原子动作比例，直接反映动作生成的精确度。

### 补充图表

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/005_Figure_4.jpg]]
*Figure 4: Experiments on MindPower Benchmark*

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/009_Figure_7.jpg]]
*Figure 7: Story Construction Pipeline for False-Belief Correction Task*

## 实验与分析

### 核心定量结果

Table 2 总结了 MindPower 在感知、心理推理、决策与行动三个层次上的全面评估。在 Sentence Transformer 语义相似度指标上，本文模型（SFT + Mind-Reward）相较基座模型 **Qwen2.5-VL-7B-Instruct**（Bai et al., arXiv 2025）在感知层（<Perception>）提升 20.04%，在决策层（<Decision>）提升 23.33%。在更严格的动作执行指标上，成功率（SR）从 0.29 提升至 11.75，动作正确率（AC）从 0.22 提升至 15.40，验证了 MindPower 推理层次与 Mind-Reward 优化框架在具身动作生成上的实质性增益。

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/007_Table_2.jpg]]
*Table 2: Quantitative Evaluation. We evaluate our model against both image-based and video-based VLMs. “B” denotes the BERTScore, “S” represents the Sentence Transformer score, and “BPC” means BDI and Perspective Consistency. The BPC score ranges from 0 to 10, while all other metrics are normalized to a range of 0 to 100*

与闭源 VLM 的对比进一步凸显了方法优势：本文模型在决策制定精度上超越 **GPT-4o**（Achiam et al., arXiv 2023）12.77%，在动作生成精度上超越 12.49%。值得注意的是，尽管 **Gemini-2.5 Pro**（Comanici et al., arXiv 2025）和 GPT-4o 在感知与心理推理层表现强劲，但在需要生成可执行动作序列的 Level-3 任务上，所有基线模型均表现极差——这恰好是 MindPower 通过显式推理层次与一致性奖励所攻克的核心瓶颈。

Figure 10 的雷达图从人类基线视角提供了参照：在错误信念纠正（False-Belief Correction）和隐式目标推断与完成（Implicit Goal Inference & Completion）两个子任务上，人类参与者在 BDI 推理、决策和动作各维度均显著领先于所有 VLM，表明机器人中心的心理理论推理仍是一个高难度开放问题。

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/013_Figure_10.jpg]]
*Figure 10: Radar Charts Comparing Human and VLM Performance on MindPower. (a) False-Belief Correction, (b) Implicit Goal Inference & Completion, (c) Dialogue-driven examples, (d) Overall performance across all tasks*

### 消融实验

**推理层次的必要性。** 为验证 MindPower 推理层次的结构性贡献，作者在 GPT-4o 上进行了两项消融：完全移除推理层次（直接输出决策与动作）以及替换为标准逐步推理（`<think> ... </think>` 格式）。结果显示，移除推理层次导致 GPT-4o 决策精度下降 1.24%，动作生成精度从 2.91% 骤降至 0.82%；使用标准逐步推理替代后，决策精度进一步下降 4.89%，动作精度降至 0.90%。这表明，精心设计的六层 BDI 推理结构并非简单的提示工程技巧，而是对连贯决策与动作生成具有因果性贡献。

**Mind-Reward 与冷启动的必要性。** 在训练范式层面，仅使用监督微调（SFT）已能带来一定程度的性能提升，但结合 Mind-Reward 的 GRPO 阶段后，各层指标均出现显著跃升。若跳过 SFT 直接使用 Mind-Reward 进行强化优化，模型整体性能仍远低于完整两阶段流程，证实 SFT 是有效的冷启动手段。这一发现与当前大模型强化学习的主流实践一致：奖励信号需要在一个已经具备基本格式遵循和语义对齐能力的基座上才能发挥最大效用。

**机器人中心评分的模型对比。** Figure 4(b) 展示了各模型在机器人中心（Robot-Centric, RC）评分上的对比。该评分专门衡量模型是否同时推理了智能体自身和人类角色的心理状态，而非仅从旁观者视角推断人类意图。本文模型在该指标上显著优于所有开源和闭源基线，直接验证了 MindPower 推理层次中 Level-2 的机器人中心设计——即同时推理智能体与人类的信念、欲望和意图——的实际效果。

### 失败模式与局限性

尽管 MindPower 在各项指标上取得了显著提升，其动作执行成功率（SR 11.75）和动作正确率（AC 15.40）的绝对值仍然较低，反映出具身动作生成任务的固有难度。主要失败模式包括：

1. **前置推理层错误传播。** 当 <Belief> 层错误推断人类角色的信念（尤其是二阶信念）时，后续的 <Desire>、<Intention> 和 <Action> 层往往随之偏离真值。这一级联效应在隐式目标推断任务中尤为突出，因为该任务要求模型从行为线索中推断未明确表达的意图。
2. **仿真器约束下的动作空间限制。** 实验基于 VirtualHome 和 ThreeDWorld 仿真环境，其原子动作集和类人智能体模型无法完全覆盖真实世界的交互多样性，导致部分正确推理无法映射为有效的可执行动作。
3. **长推理链的效率代价。** MindPower 要求模型输出完整的六层推理链，令牌数量显著增加。在需要实时响应的具身场景中，这种显式推理可能引入不可忽略的延迟。

### 实验设置与公平性

数据集按 8:2 随机划分为训练集和测试集，所有模型在相同测试分割上评估。闭源模型（GPT-4o、Gemini-2.5 Pro/Flash）采用平均采样 64 帧作为输入，开源模型分别测试了平均帧输入和直接视频输入两种模式。评估指标覆盖四个层次：感知层与心理推理层使用 BERTScore 和 Sentence Transformer 语义相似度；决策层额外引入 BDI 与视角一致性（BPC）评分（0-10 分）；动作层使用成功率（SR）和动作正确率（AC）两个公式化指标。人工评估作为参照基线，确保了自动化指标的可解释性。

### 补充图表

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/004_Table_1.jpg]]
*Table 1: Comparison of Theory-of-Mind (ToM) Benchmarks. “MCQ” denotes Multiple Choice Question. “Level-3 Ability” indicates whether each dataset involves False-Belief Correction, Implicit Goal Inference & Completion, and Decision Making and Action level*

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative Evaluation. We compare our model with GPT-4o and Qwen2.5-VL-7B-Instruct. Although GPT-4o outputs the correct format, it incorrectly infers that the human intends to open the refrigerator. In contrast, Qwen2.5-VL-7B-Instruct fails to follow the required format and also produces incorrect mental reasoning. Detailed outputs are provided in Sec. D of the Supplementary Material*

![[assets/figures/papers/paper_list_l2404_https_arxiv_org_abs_2511_23055/figures/003_Figure_3.jpg]]
*Figure 3: Robot-Centric MindPower Reasoning Hierarchy. Existing benchmarks, such as MuMA-ToM, include only Stage 1 and Stage 2 of the video, and focus solely on inferring the mental reasoning of the human (Alice) in the input video. Our dataset additionally includes Stage 3, where Alice returns to search for the item. Moreover, in Level-2 (Mental Reasoning) of MindPower, we infer the mental reasoning of both the embodied agent and the human, whereas existing ToM Benchmarks only infer the role’s mental state through multiple-choice questions. Detailed example is provided in Sec. B of the Supplementary Material*

## 方法谱系与知识库定位

### 1. 核心基线及其与 MindPower 的关系

MindPower 的基线体系可从三个维度划分：闭源 VLM、开源 VLM 以及消融变体。这些基线在“推理视角”“推理结构”和“优化目标”三个关键槽位上与 MindPower 形成对照。

**闭源 VLM 基线**：以 **GPT-4o**（Achiam et al., arXiv 2023）和 **Gemini-2.5 Pro / Flash**（Comanici et al., arXiv 2025）为代表。这类模型在感知层（Perception）和心理推理层（Mental Reasoning）的 BERTScore 和 Sentence Transformer 得分上表现较强（Table 2），但其推理本质上是**角色中心（Role-Centric）**的——仅推断视频中人类角色的心理状态，而完全忽略具身智能体自身的信念、欲望和意图。这导致它们在需要“机器人中心”视角的决策与动作层上性能急剧退化：GPT-4o 的动作成功率（SR）仅为 0.29，动作正确率（AC）仅为 0.22（Table 2）。定性分析（Figure 6）进一步揭示，即使 GPT-4o 输出格式正确，它也会错误推断人类意图（例如将“走向厨房”误判为“意图打开冰箱”），说明缺乏机器人中心视角会导致心理推理与行动生成之间的因果断裂。

**开源 VLM 基线**：包括 **Qwen2.5-VL-7B-Instruct**（Bai et al., arXiv 2025）、**Video-R1**（Feng et al., NeurIPS 2025）、**VideoChat-R1**（Li et al., arXiv 2025）、**InternVL3.5-8B**（Wang et al., arXiv 2025）、**LLaVA-OV-8B**（Li et al., TMLR 2024）、**Video-LLaVA3**（Lin et al., EMNLP 2024）和 **Video-ChatGPT**（Maaz et al., ACL 2024）。这些模型在 MindPower Benchmark 上整体表现显著弱于闭源模型，尤其在动作层（SR 和 AC）上几乎完全失效——多数开源模型的 SR 和 AC 接近零（Table 2）。其根本瓶颈在于：它们要么直接输出决策而缺乏显式的心理推理结构，要么仅依赖通用的逐步思考链（chain-of-thought），无法将信念-欲望-意图（BDI）认知结构与具身行动衔接。MindPower 选择 **Qwen2.5-VL-7B-Instruct** 作为训练基座，正是因为它代表了开源 VLM 的典型能力上限，且其 7B 参数量适合进行两阶段训练（SFT + GRPO）的实验验证。

**消融基线**：论文设计了三个关键消融来验证 MindPower 各组件的因果作用：
- **移除 MindPower 推理层次**：直接要求 GPT-4o 输出决策和动作，结果决策精度下降 1.24%，动作生成精度从 2.91% 降至 0.82%。
- **替换为标准逐步推理**：用通用的 `<think> ... </think>` 标签替代 MindPower 的六层结构化推理，决策精度下降 4.89%，动作精度从 2.91% 降至 0.90%。
- **仅使用 SFT 而无 Mind-Reward**：SFT 带来一定提升，但性能显著低于 SFT + Mind-Reward 的完整流程；反之，仅使用 Mind-Reward 而无 SFT 冷启动，整体性能仍不理想。

这些消融共同证明：MindPower 的推理层次结构（而非单纯的“推理行为”）和 Mind-Reward 的一致性约束（而非单纯的监督信号）是性能提升的因果杠杆。

### 2. 与现有 ToM 基准的谱系关系

Table 1 系统对比了 MindPower 与现有心理理论（ToM）基准的差异。传统 ToM 基准（如 MuMA-ToM、ToMi、Social-IQ 等）存在三个共同局限：
- **视角单一**：仅评估对人类角色心理状态的推断，忽略智能体自身的心理建模。
- **输出形式受限**：多为多项选择题（MCQ），无法评估从推理到行动的连贯生成能力。
- **缺乏 Level-3 能力**：不涉及错误信念纠正、隐式目标推断与完成、以及自主决策与动作生成。

MindPower 的定位是填补“从心理推理到具身行动”的空白。其核心创新在于引入 **Level-3（决策与行动层）**，并要求模型在机器人中心视角下完成完整的六层推理链（Figure 2, Figure 3）。这使得 MindPower 不仅是一个新的基准，更是一个**推理范式的转变**：将 ToM 从被动的“理解他人”升级为主动的“理解自己与他人并据此行动”。

### 3. 适用边界与局限

**适用边界**：
- MindPower 当前严格限定在**家庭交互场景**（590 个交互场景），且依赖 VirtualHome 和 ThreeDWorld 仿真器的环境、类人智能体模型和原子动作集。这决定了其推理层次和动作空间是封闭且预定义的。
- 方法假设模型能够完整输出从 `<Perception>` 到 `<Action>` 的六层推理链，因此**要求模型具备较强的长文本生成能力**和格式遵循能力。对于参数量较小或未经过指令微调的模型，这种显式层次结构可能引入额外的格式负担。
- Mind-Reward 的原子级、局部和全局一致性评估均基于 ROUGE 指标，这隐式假设动作序列的语义相似性可通过 n-gram 重叠捕获。对于语义等价但表述差异较大的动作序列，该奖励信号可能不够精确。

**明确局限**（来自论文自身声明）：
- **环境与动作集的封闭性**：受限于开源仿真器的能力，实验设定无法覆盖真实世界的物理交互、动态环境和开放动作空间。
- **推理效率与令牌开销**：显式的六层推理链导致输出令牌数量显著增加，可能影响实时交互场景中的推理延迟。
- **前置层错误的传播**：论文未系统研究当 `<Perception>` 或 `<Belief>` 层出现错误时，模型是否仍能做出部分正确的决策或执行有帮助的动作——这是一个需要手动验证的开放问题。

### 4. 开放问题与后续工作方向

论文明确提出了三个开放问题，为后续研究提供了直接锚点：
1. **错误传播的鲁棒性**：当推理链的前置层（如感知或信念推理）出错时，模型是否仍能生成部分正确的决策或动作？这涉及推理层次的可解耦性，是一个尚未探索的重要问题。
2. **向真实世界场景的泛化**：如何将 MindPower 基准扩展到真实机器人平台和开放环境，从而验证模型在非仿真条件下的心理推理与行动生成能力？
3. **隐式心理状态建模**：未来是否可以开发基于当前显式层次结构的隐式建模方法，在缩短推理长度的同时保持可解释性？这将直接回应推理效率的局限。

此外，从方法谱系角度看，MindPower 的 Mind-Reward 框架与 **Visual-RFT**（Liu et al., 2024）和 **DeepSeek-Math**（Shao et al., 2024）的 GRPO 训练范式存在继承关系，但其将强化奖励显式分解为原子准确性、局部一致性和全局一致性的设计，为“推理一致性驱动强化学习”提供了可复用的模板。后续工作可探索将 Mind-Reward 的分解思想推广到其他需要结构化推理与行动对齐的具身任务中。

## 原文 PDF

![[paperPDFs/CVPR_2026/MindPower_Enabling_Theory_of_Mind_Reasoning_in_VLM_based_Embodied_Agents.pdf]]
