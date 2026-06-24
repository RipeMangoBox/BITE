---
title: "Incentivizing Agentic Reasoning in LLM Judges via Tool-Integrated Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Incentivizing_Agentic_Reasoning_in_LLM_Judges_via_Tool_Integrated_Reinforcement_Learning.pdf
openreview_forum_id: AXNRILww9c
aliases:
- TJ
- IARLJTIRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过工具集成强化学习（RL）训练LLM法官在推理中自主生成代码并利用代码执行结果，从而将工具使用能力内化到模型策略中。"
primary_logic: "采用多轮强化学习（DAPO）和多样化奖励（正确性、格式、工具使用）可以教会LLM法官何时以及如何调用Python代码执行器进行精确验证。此外，迭代RL（TIR-Judge-Zero）能够无需教师蒸馏实现自提升，证明了纯RL在工具使用上的潜力。"
claims:
- "仅向模型增加代码执行工具几乎无提升甚至有害，而RL训练带来显著提升，表明RL是解锁工具使用能力的关键。"
- "TIR-Judge在PPE基准上的点对点评判中，超越同规模基线4.8%-9.9%；在成对评判中超越4.5%-8.8%。"
- "TIR-Judge-Zero（无蒸馏）在多个基准上达到与蒸馏版本相当或更好的性能，表明纯RL可实现自提升。"
- "TIR-Judge-8B在列表评判中达到Claude-Opus-4性能的96%，且参数量仅为其1/8。"
---

# Incentivizing Agentic Reasoning in LLM Judges via Tool-Integrated Reinforcement Learning

> [!tip] 核心洞察
> 采用多轮强化学习（DAPO）和多样化奖励（正确性、格式、工具使用）可以教会LLM法官何时以及如何调用Python代码执行器进行精确验证。此外，迭代RL（TIR-Judge-Zero）能够无需教师蒸馏实现自提升，证明了纯RL在工具使用上的潜力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过工具集成强化学习激励LLM评委中的代理推理 |
| 英文题名 | Incentivizing Agentic Reasoning in LLM Judges via Tool-Integrated Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=AXNRILww9c) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TIR-Judge |
| Dataset | PPE Correctness (Pointwise), PPE Correctness (Pairwise), RewardBench2 (Listwise), BigCodeBench (Best-of-N) |

> [!tip] 效果简介
> - PPE Correctness (Pointwise) 上，平均准确率 为 TIR-Judge-Distill 8B 71.0%，对比 Qwen3-8B 61.1%，变化 +9.9%。
> - PPE Correctness (Pairwise) 上，平均准确率 为 TIR-Judge-Zero 4B 76.3%，对比 Qwen3-4B-Instruct 60.4%，变化 +15.9%。
> - RewardBench2 (Listwise) 上，平均准确率 为 TIR-Judge-Zero 8B 73.4%，对比 Claude-Opus-4 76.5%，变化 96%性能匹配。

## 概述

### 问题瓶颈

LLM-as-a-Judge 已成为评估模型输出的主流范式，但现有评委存在根本性局限：它们仅依赖纯文本推理，缺乏对复杂约束的精确验证和计算能力。当面对需要严格计数、数值比较或格式检查的评判任务时，纯文本推理容易产生幻觉或疏忽。尽管已有工作尝试在推理时为模型添加代码执行等工具，但这些方法缺乏端到端训练，工具使用能力未能深度融入模型的推理策略中，导致增益有限甚至引入额外错误。

### 核心方法

本文提出 **TIR-Judge**，一个端到端的工具集成强化学习框架，通过训练让 LLM 评委在推理过程中自主生成 Python 代码并利用执行结果来支撑评判决策。方法建立在三个原则之上：

- **多样化训练**：混合可验证领域（数学、代码）与不可验证领域（对话、安全）的偏好数据。
- **灵活评判格式**：同时支持点对点（pointwise）、成对（pairwise）和列表（listwise）三种评判范式。
- **迭代强化学习**：采用 DAPO 多轮策略梯度优化，结合正确性、格式和工具使用的乘积式奖励函数，使模型学会何时以及如何调用代码执行器。

框架提供两种冷启动策略：**TIR-Judge-Distill** 利用强教师模型（Gemini-2.5-Flash）蒸馏高质量轨迹进行 SFT 初始化；**TIR-Judge-Zero** 则通过“RL → 拒绝采样 → SFT”的迭代循环实现无需蒸馏的自举训练，证明了纯 RL 在工具使用上的自提升潜力。

### 关键结论

1. **RL 是解锁工具使用能力的关键**：仅向模型增加代码执行工具几乎无提升甚至有害（<1% 增益），而经过 RL 训练后性能大幅跃升，表明端到端优化不可或缺。
2. **显著的性能优势**：TIR-Judge 在 PPE 基准上超越同规模文本推理评委 4.8%–9.9%（点对点）和 4.5%–8.8%（成对）；8B 模型在列表评判上达到 Claude-Opus-4 性能的 96%，参数量仅为其 1/8。
3. **自提升可行性**：TIR-Judge-Zero（无蒸馏）在多个基准上达到与蒸馏版本相当甚至更优的性能，验证了迭代 RL 循环的有效性。
4. **鲁棒性提升**：RL 训练显著降低了位置偏见（差异从 9% 降至 <2%）和冗长偏见，使评判更加公正。

### 方法定位

TIR-Judge 属于**工具增强型 LLM 评委**，区别于：

- 纯文本推理评委（如 RM-R1, Chen et al., 2025b），后者完全依赖语言推理。
- 推理时工具增强方法（如 AgentRM, Peng et al., 2025），仅在推理阶段添加工具而无训练。
- 标量奖励模型，直接输出分数而非可解释的评判轨迹。

其核心创新在于将工具调用能力通过 RL 内化到模型策略中，使“何时用工具、如何用工具”成为模型自主习得的推理行为，而非外部预设的规则。

## 背景与动机

### 现有LLM评委的局限性

大语言模型（LLM）作为评判者（LLM-as-a-Judge）已成为自动评估模型输出的主流范式。然而，现有方法存在一个根本性瓶颈：**纯文本推理缺乏对复杂约束的精确验证和计算能力**。当评估任务涉及数学证明的正确性、代码执行结果的比对、或指令遵循的细粒度检查时，仅依靠语言推理的评委往往无法给出可靠判断——它们可能在计数任务上出错，在逻辑一致性验证上产生幻觉，或在需要确定性计算的场景中给出模糊结论。

现有工具增强方法试图缓解这一问题，但它们通常采用“推理时添加工具”的策略，即在模型推理阶段被动地提供工具调用接口，而**缺乏端到端的训练**使工具使用能力无法深度融入模型的推理策略中。这导致模型不知道何时该调用工具、如何编写有效的验证代码、以及如何基于工具反馈修正判断，工具使用始终停留在浅层辅助层面。

### 动机：从工具辅助到工具内化的转变

本文的核心动机在于：**通过强化学习（RL）将工具使用能力内化到LLM评委的策略中**，使其能够自主决定何时生成代码、执行验证、并基于执行结果进行推理。这一转变的关键在于：

- **训练范式升级**：从监督微调或知识蒸馏转向多轮强化学习，使模型在试错中学会最优的工具调用策略。
- **多样化奖励信号**：通过正确性奖励、格式奖励和工具使用奖励的乘积组合，引导模型在保证判断准确性的同时，养成规范的工具使用习惯。
- **自提升潜力**：探索无需教师蒸馏的迭代RL路径（TIR-Judge-Zero），证明纯强化学习即可实现工具使用能力的自举式提升。

### 核心主张

基于上述动机，本文提出 **TIR-Judge**，一个端到端的工具集成强化学习框架。其核心洞察是：**采用多轮强化学习（DAPO）和多样化奖励可以教会LLM评委何时以及如何调用Python代码执行器进行精确验证**。实验表明，仅向模型增加代码执行工具几乎无提升甚至有害，而RL训练带来显著提升（Section 5.2），这证实了RL是解锁工具使用能力的关键机制。

## 核心创新

TIR-Judge 的核心创新在于将**工具调用能力内化到 LLM 评委的策略中**，而非仅在推理时附加工具。现有 LLM 评委（如基于 Qwen3 的基座模型、RM-R1 等）仅依靠纯文本推理，缺乏对复杂约束的精确验证和计算能力；而 AgentRM 等工具增强方法仅在推理时添加工具，缺少端到端训练，工具使用无法深度融入推理过程。TIR-Judge 通过工具集成强化学习，系统性地改变了以下关键维度：

### 推理模式：从纯文本到工具集成推理

**基线做法**：现有评委模型（Qwen3-8B、RM-R1 等）仅生成自然语言推理链，无法执行代码进行精确验证。部分方法（如 AgentRM、Gemini-2.5-Flash）虽支持工具调用，但仅在推理时附加，模型并未被训练来主动判断何时及如何调用工具。

**TIR-Judge 的变革**：评委的推理轨迹被重新定义为推理、代码与执行结果的交替序列：

$$s_k = \{ r_1, c_1, o_1, \dots, r_k, c_k, o_k \}$$

在每一步，评委根据历史轨迹生成推理 $r_k$ 和代码 $c_k$，通过 Python 执行器 $\mathbb{Z}$ 获得结果 $o_k$，并将其附加到轨迹中继续推理。这使得评委能够将决策建立在可验证证据之上——例如通过代码精确计数约束满足情况、验证数学等价性、或检查格式一致性。

**关键证据**：消融实验（Table 1）表明，仅向 Qwen3-8B 添加代码执行工具（Qwen3-8B-Tool）几乎无提升甚至有害（<1% 增益），而经过 RL 训练后性能大幅提升。这证明**RL 是解锁工具使用能力的关键**，而非简单的工具接入。

### 训练范式：从监督微调到多轮强化学习

**基线做法**：主流方法依赖监督微调（SFT）或知识蒸馏——如 TIR-Judge-Distill 使用 Gemini-2.5-Flash 教师生成高质量轨迹进行 SFT 初始化。这些方法预设了工具调用模式，模型仅模仿教师行为。

**TIR-Judge 的变革**：采用基于 DAPO 的组策略梯度优化，在采样轨迹中同时包含推理、代码和执行结果，通过重要性权重裁剪和 KL 惩罚更新策略。奖励函数采用乘积形式组合三个维度：

$$R = \begin{cases} 1, & \text{if } R_t = 1 \land R_f = 1 \land R_c = 1 \\ 0.1, & \text{if } R_c = 1 \text{ but } (R_t = 0 \lor R_f = 0) \\ 0, & \text{if } R_c = 0 \end{cases}$$

其中 $R_c$ 为正确性奖励（评判与真实偏好一致），$R_f$ 为格式奖励，$R_t$ 为工具使用奖励（无错误且不超调用次数）。这种设计迫使模型同时满足正确性、格式规范和工具使用规范。

**迭代自提升**：TIR-Judge-Zero 进一步证明了**无需教师蒸馏的纯 RL 自举能力**。其训练循环为：

$$\mathcal{T}_{t+1} \gets \mathrm{RS}(\pi_{\theta_t}), \quad \pi_{\theta_{t+1}} \gets \mathrm{SFT}(\pi_{\theta_0}, \mathcal{T}_{t+1}), \quad \pi_{\theta_{t+1}} \gets \mathrm{RL}(\pi_{\theta_{t+1}})$$

即从当前策略进行拒绝采样生成训练数据，用其对初始策略进行 SFT，再对 SFT 后的策略进行 RL，循环迭代。实验显示第二轮 RL 持续优于第一轮（Figure 5），且 TIR-Judge-Zero 在多个基准上达到与蒸馏版本相当或更好的性能（Table 1）。

### 评估格式：从单一到多格式统一支持

**基线做法**：大多数评委模型仅支持成对评判（pairwise），如 RM-R1 专门针对成对比较设计。

**TIR-Judge 的变革**：原生支持**点对点（pointwise）、成对（pairwise）和列表（listwise）**三种评判格式（Figure 2）。训练数据涵盖约 26k 偏好对，包含三种格式的标注。正确性奖励函数针对不同格式分别定义：

$$R_c = \begin{cases} \mathbb{I}(s_\theta(x, y_{pos}) > s_\theta(x, y_{neg})), & \text{点对点评判} \\ \mathbb{I}(J_\theta(x, \mathcal{Y}) = l), & \text{成对或列表评判} \\ 0, & \text{其他} \end{cases}$$

这使得同一模型可在不同场景下灵活切换评判模式。在 RewardBench2 的列表评判中，TIR-Judge-8B 达到 Claude-Opus-4 性能的 96%（Table 2），而参数量仅为其 1/8。

### 任务多样性：从特定领域到可验证/不可验证混合

**基线做法**：现有工具增强方法通常针对特定可验证任务（如数学、代码）设计，在对话、安全等不可验证领域表现受限。

**TIR-Judge 的变革**：训练数据混合了可验证领域（竞赛编程、数学推理）和不可验证领域（对话、安全、通用编码）。消融实验（Figure 3）表明，仅使用聊天或推理任务训练会导致跨子任务迁移差，而混合数据是关键。工具增强模型在推理和指令遵循基准上持续优于纯文本模型，尽管在纯文本中心任务（如 RMBench 的 Chat 和 Safety）上略逊（Section 5.3）。

### 偏见鲁棒性

TIR-Judge 展现出显著改善的偏见鲁棒性：位置偏见（A-B/B-A 顺序差异）通常 <1%，最多 2%，而 Qwen3 基座模型可达 9% 的差异（Table 9）；当正确回答更长或更短时，准确率差异很小，且在某些情况下抵消了基座模型的冗长偏差（Table 10）。这归因于工具集成推理使评判更依赖可验证证据而非表面特征。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of TIR-Judge variants. TIR-Judge natively supports tool use during judgment and is designed to handle diverse input formats*

TIR-Judge 的核心设计是将**工具调用能力内化到 LLM 评委的推理策略中**，而非仅在推理时被动附加工具。其整体框架围绕以下关键组件构建：

### 工具集成推理循环

TIR-Judge 将传统纯文本推理扩展为**推理-代码-执行**交织的轨迹。在每一步 $k$，评委根据当前上下文生成推理文本 $r_k$ 和代码 $c_k$，调用 Python 执行器 $\mathbb{Z}$ 获得结果 $o_k$，并将其附加到轨迹中继续推理，直至输出最终评判。这一循环可形式化为：

$$(r_k, c_k) \sim J(x \oplus s_{k-1}), \quad o_k = \mathbb{Z}(c_k), \quad s_k = s_{k-1} \oplus r_k \oplus c_k \oplus o_k$$

其中 $s_k = \{ r_1, c_1, o_1, \dots, r_k, c_k, o_k \}$ 为第 $k$ 步的完整轨迹（Section 3）。这种设计使评委能够将决策建立在可验证的计算证据之上，而非仅依赖语言推理。

### 训练管线四大模块

TIR-Judge 的训练流程由四个模块串联构成（Section 4）：

1. **数据收集与过滤**：构建约 26k 偏好对，涵盖可验证领域（竞赛编程、数学推理）与不可验证领域（对话、安全、通用编码），同时支持点对点、成对、列表三种评判格式，并通过 8-gram 去污染确保数据质量。
2. **工具集成 RL 训练**：基于 DAPO 算法进行组策略梯度优化，在采样轨迹中自然包含推理、代码和执行结果，通过重要性权重裁剪和 KL 惩罚提升训练稳定性。
3. **奖励设计**：组合正确性奖励 $R_c$（预测与标签一致）、格式奖励 $R_f$（遵循标签要求）和工具使用奖励 $R_t$（无错误且不超调用次数），最终奖励采用乘积形式——仅当三者全部满足时给满分 1，正确但格式或工具有缺陷时给 0.1，否则给 0。
4. **冷启动与迭代训练**：提供两条路径——**TIR-Judge-Distill** 使用 Gemini-2.5-Flash 教师模型通过拒绝采样生成高质量轨迹进行 SFT 初始化；**TIR-Judge-Zero** 则通过迭代 RL → 拒绝采样 → SFT 的循环实现无蒸馏自举。

### 输入输出流与评判格式

TIR-Judge 原生支持三种评判格式（Figure 2）：
- **点对点评判**：对单个回答打分，比较 $s_\theta(x, y_{pos})$ 与 $s_\theta(x, y_{neg})$
- **成对评判**：给定两个回答，直接判断孰优孰劣
- **列表评判**：对多个回答进行排序

无论哪种格式，评委在推理过程中均可按需调用代码执行器进行精确验证（如计数约束检查、数学表达式求值、代码正确性验证），最终输出结构化评判结果。

## 核心模块与公式推导

### 工具集成推理循环

TIR-Judge 的核心推理机制是将 Python 代码执行器 $\mathbb{Z}$ 嵌入 LLM 法官的生成轨迹中。给定输入提示 $x$，法官在第 $k$ 步生成推理文本 $r_k$ 和代码块 $c_k$，随后执行代码获得输出 $o_k$，并将其追加到历史轨迹中：

$$(r_k, c_k) \sim J(x \oplus s_{k-1}), \quad o_k = \mathbb{Z}(c_k), \quad s_k = s_{k-1} \oplus r_k \oplus c_k \oplus o_k$$

其中轨迹 $s_k = \{ r_1, c_1, o_1, \dots, r_k, c_k, o_k \}$ 交替包含自然语言推理、代码和执行结果。这一设计使法官能够将决策建立在可验证的计算证据之上，而非仅依赖文本推理（Section 3）。

### 强化学习框架（DAPO）

TIR-Judge 采用基于 DAPO 的组策略梯度优化进行训练。对每个提示-答案对 $(q, a)$，从旧策略 $\pi_{\theta_{old}}$ 中采样 $G$ 条轨迹 $\{s_i\}_{i=1}^G$，优化目标为：

$$\mathcal{I}(\theta) = \mathbb{E}_{(q,a) \sim \mathcal{D}, \{s_i\}_{i=1}^G \sim \pi_{\theta_{old}}} \left[ \frac{1}{\sum_{i=1}^G |s_i|} \sum_{i=1}^G \sum_{t=1}^{|s_i|} \left( \min \left(r_{i,t}(\theta) \widehat{A}_{i,t}, \text{clip}(r_{i,t}(\theta), 1-\varepsilon_{low}, 1+\varepsilon_{high}) \widehat{A}_{i,t} \right) - \beta D_{KL}(\pi_\theta \| \pi_{ref}) \right) \right]$$

约束条件为 $0 < |\{s_i : \text{is\_equivalent}(a, s_i)\}| < G$，即排除批次内所有轨迹全对或全错的情况，以保持有效的梯度信号（Section 4.2）。

### 奖励设计

奖励函数由三个组件构成，采用乘积形式组合：

**正确性奖励 $R_c$**：判断法官决策是否与真实偏好一致。

$$R_c = \begin{cases} \mathbb{I}(s_\theta(x, y_{pos}) > s_\theta(x, y_{neg})), & \text{点对点评判} \\ \mathbb{I}(J_\theta(x, \mathcal{Y}) = l), & \text{成对或列表评判} \\ 0, & \text{其他} \end{cases}$$

**最终奖励 $R$**：当正确性、格式和工具使用三者全部满足时给予满分，仅正确性满足但格式或工具有缺陷时给予部分奖励。

$$R = \begin{cases} 1, & \text{if } R_t = 1 \land R_f = 1 \land R_c = 1 \\ 0.1, & \text{if } R_c = 1 \text{ but } (R_t = 0 \lor R_f = 0) \\ 0, & \text{if } R_c = 0 \end{cases}$$

消融实验证实，乘积形式在多数基准上优于求和形式（Table 8），其直觉在于工具使用和格式遵循是正确评判的必要条件而非加分项（Section 4.2）。

### 冷启动与迭代训练

TIR-Judge 提供两条训练路径：

**蒸馏路径（TIR-Judge-Distill）**：利用 Gemini-2.5-Flash 教师模型通过拒绝采样生成高质量轨迹，仅保留正确轨迹构成数据集 $\mathcal{T}_{SFT}$，对基座模型进行监督微调：

$$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(x, \tau) \sim \mathcal{T}_{\mathrm{SFT}}} \left[ \sum_{i=1}^{|y|} \log f_\theta(\tau_i \mid \tau_{<i}, x) \right]$$

SFT 后再进行 RL 训练（Section 4.3）。

**自举路径（TIR-Judge-Zero）**：无需教师蒸馏，通过迭代 RL 实现自提升。第 $t$ 轮循环为：

$$\mathcal{T}_{t+1} \gets \mathrm{RS}(\pi_{\theta_t}), \quad \pi_{\theta_{t+1}} \gets \mathrm{SFT}(\pi_{\theta_0}, \mathcal{T}_{t+1}), \quad \pi_{\theta_{t+1}} \gets \mathrm{RL}(\pi_{\theta_{t+1}})$$

即从当前策略进行拒绝采样生成训练数据，用其对初始策略进行 SFT，再进行 RL 优化，循环迭代。实验表明第二轮 RL 持续优于第一轮，验证了迭代自举的有效性（Figure 5, Section 5.3）。

## 实验与分析

### 核心发现：RL是解锁工具使用能力的关键

实验首先验证了一个关键因果机制：**单纯为模型增加代码执行工具几乎无提升甚至有害，而通过RL训练将工具使用内化到策略中才能带来显著增益**。在Qwen3-8B基座模型上直接添加工具（Qwen3-8B-Tool），在PPE基准上的准确率提升不足1%，部分子任务甚至出现退化；而经过RL训练的TIR-Judge-Distill 8B在点对点评判上超越基座模型9.9%（71.0% vs. 61.1%），在成对评判上超越8.8%（Table 1）。这一对比直接表明，工具使用能力的涌现依赖于端到端的策略优化，而非简单的推理时增强。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/003_Table_1.jpg]]
*Table 1: Main results on six benchmarks. † indicates results reported from the original papers, and are mainly used for reference. CJBench, RWBench, and JGBench denote CodeJudgeBench, RewardBench, and JudgeBench. “Distill?” specifies whether the model relies on additional judge data distilled from teacher models. Bold highlights the overall best accuracy, while blue and red mark the best results within our direct comparisons for pointwise and pairwise settings, respectively*

### 主实验结果

**点对点与成对评判**：在六个基准（PPE Correctness、IFBench、CodeJudgeBench、RewardBench、RMBench、JudgeBench）上，TIR-Judge在4B和8B两个规模均显著超越同类基线。具体而言：
- **TIR-Judge-Distill 8B**在点对点评判上超越同规模基线4.8%-9.9%，在成对评判上超越4.5%-8.8%（Table 1）。
- **TIR-Judge-Zero 4B**在成对评判的PPE Correctness上达到76.3%，相比Qwen3-4B-Instruct的60.4%提升15.9个百分点，验证了纯RL自举策略的有效性（Table 1）。
- 在RewardBench2的列表评判中，**TIR-Judge-Zero 8B**以73.4%的平均准确率达到Claude-Opus-4（76.5%）性能的96%，而参数量仅为其1/8（Table 2）。这一结果表明，工具集成RL训练可以在极小模型规模下逼近顶级闭源模型的评判能力。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/004_Table_2.jpg]]
*Table 2: Results on 5 tasks in RewardBench2, sorted by average performance*

**Best-of-N推理**：在AIME 2024/2025和BigCodeBench上，TIR-Judge作为重排序器进行Best-of-N选择时，点对点评判的TIR-Judge-Zero 4B相比成对评判的RRM-7B在BigCodeBench上获得6.7%的绝对增益（Figure 4b）。这验证了工具增强评判在精确验证场景下的独特优势。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/009_Figure_4.jpg]]
*Figure 4: Experimental results comparing tool-augmented judges against text-only judges under the same training data and settings, as well as the best-of-N inference performance. Figure 5: Accuracy of TIR-Judge across different training stages. Base denotes the backbone model without additional training. TIR-Judge-Zero-RS is a variant inspired by Zelikman et al. (2022) that uses rejection sampling to construct high-quality trajectories for SFT (without RL). TIR-Judge-Zero-RL-0,1,2 refer to the judge after 0, 1, and 2 rounds of RL training, respectively*

### 消融实验

**数据混合的因果作用**：仅使用聊天或推理任务数据进行RL训练会导致跨子任务迁移严重退化。Figure 3的消融显示，单一领域训练使模型在未见过领域的准确率大幅下降，而混合可验证（数学、代码）与不可验证（对话、安全）数据是发展通用工具使用能力的关键条件。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/005_Figure_3.jpg]]
*Figure 3: The effect of different data mixture used in RL training of TIR-Judge-Zero*

**奖励函数设计**：乘积形式的奖励（$R_t \land R_f \land R_c$）在多数基准上优于求和形式（Table 8）。该设计强制模型同时满足正确性、格式和工具使用三项要求，避免了模型在部分维度上投机取巧的行为。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_AXNRILww9c/figures/020_Table_8.jpg]]
*Table 8: Ablation Study on Reward Formulation (Multiplication vs. Addition)*

**迭代RL的持续提升**：TIR-Judge-Zero的迭代RL循环（RS → SFT → RL）带来持续的性能增益。Figure 5显示，第二轮RL在多个基准上优于第一轮，验证了“从当前策略进行拒绝采样获得更高质量训练数据 → SFT → RL”这一循环的正反馈效应。

**代码执行可靠性**：TIR-Judge-Zero的总代码执行错误率仅为1.37%，其中语法错误1.20%，运行时错误0%，格式错误0.17%（Table 4）。相比之下，TIR-Judge-Distill的错误率为3.81%，Qwen-3-Tool为5.12%。这表明RL训练不仅提升了评判准确率，还显著增强了代码生成的鲁棒性。

### 偏见分析

**位置偏见**：TIR-Judge在A-B/B-A顺序下的准确率差异通常小于1%，最多2%；而Qwen3基座模型可达9%的差异（Table 9）。RL训练有效抑制了模型对答案位置的非理性偏好。

**冗长偏见**：当正确回答更长或更短时，TIR-Judge的准确率差异很小，且在某些情况下抵消了Qwen3基座模型固有的冗长偏差（Table 10）。工具集成推理使评委能够基于可验证证据而非表面文本特征进行判断。

### 失败模式与局限

尽管整体表现优异，TIR-Judge仍存在可识别的失败模式：
- **代码覆盖不足**：生成的代码可能无法覆盖所有响应格式变体，导致计数或验证错误。Table 12展示了IFBench上的一个典型案例，其中TIR-Judge-Zero 8B因代码未处理特定格式而给出错误评判。
- **不可验证任务的相对劣势**：在RewardBench2的Safety子任务上，工具增强方法略逊于纯文本评委（Table 2），表明在缺乏可验证约束的场景下，代码执行带来的增益有限。
- **训练成本**：TIR-Judge-Zero虽然无需教师蒸馏，但训练成本约为蒸馏方法的两倍（29小时 vs. 11小时，8×H100，Table 11），这是纯RL自举策略的固有代价。

### 效率分析

Figure 6的推理效率分析表明，TIR-Judge在保持高准确率的同时，推理效率优于基线方法。这得益于SFT数据构建策略——教师模型生成的轨迹天然倾向于高效的工具调用模式，避免了冗余的代码生成和执行步骤。

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

现有LLM评委面临的核心瓶颈在于：纯文本推理缺乏对复杂约束的精确验证和计算能力。当评判任务涉及数学计算、代码正确性验证或结构化约束检查时，文本推理容易产生幻觉或错误判断。虽然部分方法尝试在推理时引入工具增强，但缺乏端到端的训练，使得工具使用无法深度融入模型的推理策略——模型不知道“何时”以及“如何”有效调用工具。

**TIR-Judge**的因果调节变量是：通过工具集成强化学习（RL）训练LLM评委在推理过程中自主生成代码并利用代码执行结果，将工具使用能力内化到模型策略中。其核心洞察在于：采用多轮强化学习（DAPO）和多样化奖励（正确性、格式、工具使用）可以教会LLM评委何时以及如何调用Python代码执行器进行精确验证。此外，迭代RL（TIR-Judge-Zero）能够无需教师蒸馏实现自提升，证明了纯RL在工具使用上的潜力。

### 2. 方法谱系定位

TIR-Judge在LLM评委的方法谱系中占据“工具集成+端到端RL训练”这一独特位置。其与现有工作的关系可沿两个维度展开：

**维度一：推理范式（纯文本 vs. 工具增强）**

- **纯文本推理评委**：以**RM-R1**（Chen et al., 2025b, Deepseek-Distill-7B）为代表，经过RL训练的文本推理评委，但仅支持成对评判格式，缺乏工具验证能力。TIR-Judge在PPE基准上的点对点评判中超越同规模基线4.8%-9.9%，在成对评判中超越4.5%-8.8%，直接证明了工具集成推理的优势。

- **推理时工具增强**：**AgentRM**（Peng et al., 2025）仅在推理时添加工具，未经过工具使用的端到端训练。TIR-Judge的消融实验表明，仅向模型增加代码执行工具（无RL训练）几乎无提升甚至有害（<1%增益或负面效果），而RL训练带来显著提升，表明RL是解锁工具使用能力的关键。

- **闭源工具增强评委**：**Gemini-2.5-Flash**（Comanici et al., 2025）支持可选的代码执行工具，但作为闭源模型，其训练细节不可知。TIR-Judge-8B在列表评判中达到Claude-Opus-4性能的96%，且参数量仅为其1/8，展现了开源小模型通过RL训练逼近顶级闭源模型的潜力。

**维度二：训练范式（SFT/蒸馏 vs. 纯RL自举）**

TIR-Judge提供了两种初始化策略，形成了方法谱系中的两条路径：
- **TIR-Judge-Distill**：使用Gemini-2.5-Flash教师模型进行拒绝采样生成高质量轨迹，经SFT后再进行RL训练。这属于“教师蒸馏+RL微调”范式。
- **TIR-Judge-Zero**：通过迭代“RL→拒绝采样→SFT→RL”循环实现无蒸馏自举。实验表明，TIR-Judge-Zero在多个基准上达到与蒸馏版本相当或更好的性能（在6个基准中的4个点对点任务和3个成对任务上超越蒸馏版本），证明了纯RL可实现自提升，无需依赖更强的教师模型。

### 3. 适用边界与失败模式

**适用边界**：
- **可验证领域优势明显**：在数学推理、代码验证等可验证任务上，工具增强模型始终优于纯文本评委。在BigCodeBench的Best-of-N推理中，TIR-Judge-Zero 4B点对点评委超越RRM-7B成对评委6.7%。
- **不可验证领域略有劣势**：在安全等不可验证任务上，工具增强方法可能略逊于纯文本评委（RewardBench2的Safety子任务得分较低），因为此类任务更依赖语义理解而非精确计算。
- **数据混合至关重要**：仅使用聊天或推理任务训练导致跨子任务迁移差，混合可验证/不可验证数据是RL训练成功的关键。

**失败模式**：
- **代码覆盖不完整**：生成的代码可能无法覆盖所有响应格式变体，导致计数或验证错误（IFBench上的失败案例，Table 12）。
- **工具类型受限**：当前仅支持Python代码执行器，未扩展到其他工具（如网络搜索、数据库查询等），限制了在信息检索类评判任务上的应用。
- **极长/极复杂提示**：训练任务覆盖仍有限，在极长或极复杂的提示下可能表现不佳。

### 4. 训练效率与成本

TIR-Judge-Zero虽然无需蒸馏，但训练成本约为蒸馏方法的两倍（29小时 vs. 11小时，8×H100）。代码执行错误率极低：TIR-Judge-Zero总错误率1.37%，其中语法错误1.20%，运行时错误0%，格式错误0.17%，表明RL训练有效抑制了错误代码生成。

### 5. 开放问题

- **工具生态扩展**：当前仅支持Python执行器，未来可扩展到网络搜索、数据库查询、API调用等多类型工具，以覆盖更广泛的评判场景。
- **策略模型训练增强**：探索将TIR-Judge用于增强策略模型训练（如RLHF中的奖励建模），形成“评判-策略”协同提升的闭环。
- **更长上下文的工具推理**：在极长提示或复杂多步推理场景下，工具调用的时机和频率优化仍需进一步研究。
- **安全与不可验证任务的工具设计**：如何为安全对齐等“软”评判任务设计合适的验证工具，是工具增强评委走向通用化的关键挑战。

## 原文 PDF

![[paperPDFs/ICLR_2026/Incentivizing_Agentic_Reasoning_in_LLM_Judges_via_Tool_Integrated_Reinforcement_Learning.pdf]]
