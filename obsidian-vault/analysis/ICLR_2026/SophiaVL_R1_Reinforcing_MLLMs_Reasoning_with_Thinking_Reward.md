---
title: "SophiaVL-R1: Reinforcing MLLMs Reasoning with Thinking Reward"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SophiaVL_R1_Reinforcing_MLLMs_Reasoning_with_Thinking_Reward.pdf
project_link: null
code_link: https://github.com/kxfan2002/SophiaVL-R1
openreview_forum_id: 0tzvmjMcXC
aliases:
- SR
- SophiaVL-R1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入思考奖励模型（Thinking Reward Model）对完整推理过程进行整体质量评估，并在Trust-GRPO算法中通过可信度权重动态调节思考奖励的影响，同时采用退火策略逐步降低其作用。"
primary_logic: "通过对比同一问题中正确与错误回答组之间的平均思考奖励，可以评估思考奖励的可靠性，并据此动态调整权重，从而在强化学习中更稳健地利用过程反馈来引导模型学习可泛化的推理模式。"
claims:
- "SophiaVL-R1-7B在MathVista上达到71.3%的平均准确率，明显优于Qwen2.5-VL-7B + GRPO的67.5%。"
- "SophiaVL-R1-7B在MMMU上达到61.3%，比LLaVA-OneVision-72B（56.8%）高出4.5个百分点。"
- "消融研究表明，移除信任权重或退火策略会导致所有基准上的性能下降。"
- "训练过程中，SophiaVL-R1的平均结果奖励提升最快且最终值最高，表明其推理策略更优。"
---

# SophiaVL-R1: Reinforcing MLLMs Reasoning with Thinking Reward

> [!tip] 核心洞察
> 通过对比同一问题中正确与错误回答组之间的平均思考奖励，可以评估思考奖励的可靠性，并据此动态调整权重，从而在强化学习中更稳健地利用过程反馈来引导模型学习可泛化的推理模式。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SophiaVL-R1：通过思考奖励增强多模态大模型推理 |
| 英文题名 | SophiaVL-R1: Reinforcing MLLMs Reasoning with Thinking Reward |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0tzvmjMcXC) · [GitHub](https://github.com/kxfan2002/SophiaVL-R1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SophiaVL-R1 |
| Dataset | MathVista, MathVerse, MMMU, MME |

> [!tip] 效果简介
> - MathVista 上，Average Accuracy 为 71.3，对比 67.5 (Qwen2.5-VL-7B + GRPO)，变化 +3.8。
> - MathVerse 上，Average Accuracy 为 48.8，对比 44.9 (Qwen2.5-VL-7B + GRPO)，变化 +3.9。
> - MMMU 上，Accuracy 为 61.3，对比 56.8 (LLaVA-OneVision-72B)，变化 +4.5。

## 概要

### 问题瓶颈

当前基于强化学习（RL）的多模态大模型（MLLM）推理训练主要依赖**结果奖励（outcome reward）**，即仅根据最终答案是否正确来提供反馈。这种规则化范式忽视了对中间推理过程质量的监督，导致模型可能学到有缺陷的推理策略——即使最终答案正确，推理路径也可能存在逻辑漏洞。缺乏过程级反馈使得模型的泛化能力受限，难以在分布外场景下保持稳健推理。

### 核心方法定位

SophiaVL-R1 针对上述瓶颈提出了三个协同的技术组件：

1. **思考奖励模型（Thinking Reward Model, TRM）**：训练一个独立的奖励模型，从逻辑正确性、推理正确性、错误识别、语言流畅性和图文对齐五个维度对完整推理过程进行整体质量评估，为 RL 训练提供过程级反馈信号。

2. **Trust-GRPO 算法**：引入动态**信任权重（trustworthiness weight）** γ，通过对比同一问题下正确答案组与错误答案组的平均思考奖励差异来评估思考奖励的可靠性。当错误组的平均思考奖励反而更高时，γ 显著降低，从而抑制不可靠的过程反馈对策略更新的误导。

3. **退火调度策略**：采用指数衰减调度 $e^{-\mathrm{steps}/T}$ 逐步降低思考奖励在总奖励中的权重，使模型在训练后期更依赖可靠且精确的规则结果奖励，避免过程奖励在训练末期引入噪声。

SophiaVL-R1 属于**过程奖励引导的强化学习**方法谱系，区别于仅使用结果奖励的 GRPO 基线（如 Qwen2.5-VL-7B + GRPO）以及依赖过程奖励模型但缺乏信任机制的方案（如 InternVL2.5-8B-VisualPRM）。

### 主要结果

SophiaVL-R1-7B 在多个多模态推理基准上展现出显著优势：

- **数学推理**：在 MathVista 上达到 71.3% 的平均准确率，较 Qwen2.5-VL-7B + GRPO 基线（67.5%）提升 3.8 个百分点；在 MathVerse 上达到 48.8%，提升 3.9 个百分点（Table 1）。
- **通用能力**：在 MMMU 上达到 61.3%，超越参数量 10 倍的 LLaVA-OneVision-72B（56.8%）达 4.5 个百分点；在 MME 上达到 2403.8 分（Table 2）。
- **消融验证**：移除信任权重或退火策略均导致所有基准上的性能下降，证实两个组件的必要性（Table 4）。训练过程中，SophiaVL-R1 的平均结果奖励提升最快且最终值最高，表明其习得了更优的推理策略（Figure 5）。



多模态大语言模型（MLLMs）在视觉推理任务上已取得显著进展，但如何系统性地增强其推理能力仍是一个开放问题。近期研究表明，强化学习（RL）可以有效提升大语言模型的推理性能，代表性工作如 DeepSeek-R1 通过 GRPO（Group Relative Policy Optimization）算法在纯文本数学推理上取得了突破。然而，将这一范式迁移到多模态场景时，一个关键瓶颈逐渐浮现。

**核心瓶颈在于现有的规则化强化学习范式仅依赖结果奖励（outcome reward），忽视了对思考过程质量的监督。** 在典型的 GRPO 训练中，模型仅根据最终答案的正确性获得奖励信号，而推理链的中间步骤——无论逻辑是否严密、推理是否合理——都不受任何直接评估。这种“只看结果、不看过程”的奖励机制可能导致模型学习到有缺陷的推理策略：模型可能通过偶然正确但逻辑错误的推理路径获得正向奖励，从而强化了不可泛化的思维模式。当面临分布外样本时，这类策略极易失效。

这一问题的根源在于**思考过程监督信号的缺失**。纯文本领域已有工作尝试引入过程奖励模型（PRM）对推理步骤进行细粒度评分，但多模态场景下面临独特挑战：视觉推理的步骤边界模糊，难以定义统一的步骤粒度；同时，训练可靠的步骤级奖励模型需要大量人工标注，成本高昂。因此，如何在多模态 RL 训练中高效地引入过程质量反馈，同时避免奖励黑客（reward hacking）——即模型学会利用奖励模型的漏洞而非真正提升推理能力——成为亟待解决的问题。

SophiaVL-R1 正是针对上述缺口提出的。其核心动机可概括为三点：

1. **引入整体思考质量评估**：不追求步骤级细粒度监督，而是训练一个思考奖励模型（Thinking Reward Model），从逻辑正确性、推理连贯性等维度对完整推理过程进行整体打分，以较低标注成本提供过程反馈。

2. **动态可信度调节**：思考奖励本身并非绝对可靠——当错误回答组的平均思考奖励反而高于正确组时，意味着思考奖励与结果奖励之间存在错位。Trust-GRPO 算法通过对比两组平均思考奖励的差异，动态计算可信度权重 γ，在思考奖励不可靠时自动降低其影响。

3. **退火策略引导收敛**：训练初期，思考奖励为模型提供丰富的探索信号；随着训练推进，模型应逐步依赖更可靠的结果奖励。指数衰减调度使思考奖励的影响随训练步数递减，引导策略收敛到以结果正确性为最终目标的推理模式。

这一设计思路——以整体过程评估替代步骤级监督，以动态信任机制缓解奖励黑客，以退火策略平衡探索与收敛——构成了 SophiaVL-R1 的方法论基础。



## 核心方法与创新机理

SophiaVL-R1 的核心创新在于将**过程监督信号**引入规则化强化学习范式，并通过**动态可信度调节**与**退火调度**两个机制来稳定这一信号，从而引导多模态大模型学习更可泛化的推理策略。

### 瓶颈与因果机制

现有基于 GRPO 的强化学习方法仅依赖规则化的**结果奖励**（outcome reward）进行策略优化。这一范式存在一个关键瓶颈：模型可能通过“奖励黑客”（reward hacking）学到有缺陷的推理过程，却仍然获得正确的结果奖励——即思考过程与结果之间存在**错位**（misalignment）。这种错位导致模型在分布外场景下的泛化能力受限。

SophiaVL-R1 引入的因果调节变量是**思考奖励模型**（Thinking Reward Model, TRM），它对完整推理过程进行整体质量评估。但直接将思考奖励并入奖励函数会引入新的风险：思考奖励本身可能不可靠。因此，方法的核心在于通过**Trust-GRPO 算法**动态评估思考奖励的可信度，并据此调节其对策略更新的影响。

### 方法谱系与知识库定位

SophiaVL-R1 建立在 Qwen2.5-VL-7B-Instruct（Bai et al., 2025）基础模型之上，与以下基线方法形成对比：

| 方法 | 角色 | 关键差异 |
|------|------|----------|
| Qwen2.5-VL-7B + GRPO | 直接 RL 基线 | 仅使用结果奖励，无过程监督 |
| Qwen2.5-VL-7B + SFT+GRPO | 两阶段基线 | SFT 后接 GRPO，仍无过程奖励 |
| InternVL2.5-8B-VisualPRM（Wang et al., 2025b） | 过程奖励方法 | 使用过程奖励模型（PRM），但无动态可信度机制 |
| R1-OneVision-7B（Yang et al., 2025） | 推理 MLLM | 采用 R1 风格推理，但训练范式不同 |
| LLaVA-OneVision-72B（Li et al., 2024） | 大规模通用 MLLM | 参数规模 10 倍，无专项推理强化 |

SophiaVL-R1 的独特定位在于：**将思考奖励作为辅助信号，并通过可信度感知机制与退火策略使其可靠地融入 GRPO 框架**，而非简单地将过程奖励作为固定项加入。

### 三个关键 changed slots

#### Slot 1：奖励组成——从单一结果奖励到加权思考奖励

**基线值**：仅使用规则结果奖励 $R_i^o$。

**提出值**：添加加权思考奖励 $\gamma \alpha e^{-\text{steps}/T} \cdot R_i^t$，其中 $\gamma$ 为动态信任权重，$\alpha$ 为基础系数，退火项 $e^{-\text{steps}/T}$ 使思考奖励的影响随训练步数指数衰减。最终奖励形式为：

$$R_i = R_i^o + \gamma \alpha e^{-\frac{\text{steps}}{T}} \cdot R_i^t$$

这一设计的核心洞察在于：**思考奖励在训练初期提供有价值的过程引导，但随着模型推理能力的提升，结果奖励应逐渐成为主导信号**，以避免模型过度依赖可能存在噪声的过程评估。

#### Slot 2：信任评估机制——基于正确/错误组对比的动态权重

**基线值**：无信任评估，思考奖励直接合并。

**提出值**：引入动态信任权重 $\gamma$，其计算基于同一问题下正确回答组与错误回答组的平均思考奖励对比：

$$\mu_c = \frac{1}{|G_{\text{correct}}|} \sum_{i \in G_{\text{correct}}} R_i^t, \quad \mu_w = \frac{1}{|G_{\text{wrong}}|} \sum_{i \in G_{\text{wrong}}} R_i^t$$

$$\gamma = \begin{cases} 1, & \mu_c \geq \mu_w \\ e^{\mu_c - \mu_w}, & \mu_c < \mu_w \end{cases}$$

这一设计的因果逻辑是：**当错误回答组的平均思考奖励反而高于正确回答组时（$\mu_c < \mu_w$），说明思考奖励模型在当前批次中不可靠，应降低其权重**。$\gamma$ 通过指数衰减形式在 $[0, 1]$ 区间内平滑调节，避免了硬性阈值带来的不稳定性。消融实验（Table 7）表明，基于均值对比的信任权重设计优于基于方差的替代方案。

#### Slot 3：思考奖励影响退火——从恒定影响到指数衰减

**基线值**：恒定的思考奖励影响系数。

**提出值**：采用指数衰减调度 $e^{-\text{steps}/T}$，使思考奖励对总奖励的贡献随训练步数增加而逐渐减小。这一设计与信任权重 $\gamma$ 形成双层保护机制：$\gamma$ 在**批次级别**动态调节，衰减调度在**训练进程级别**逐步降低思考奖励的总体影响。消融实验（Table 8）表明，指数衰减略优于线性衰减。

### 证据强度总结

| 创新点 | 核心证据 | 证据强度 |
|--------|----------|----------|
| 思考奖励模型 | Table 3：TRM 在 VLRewardBench 上达到最高 Overall Accuracy（48.6）和 Macro Accuracy（48.9） | 中等（仅与有限基线对比） |
| Trust-GRPO 整体框架 | Table 1：MathVista 71.3 vs GRPO 基线 67.5（+3.8）；Table 2：MMMU 61.3 vs LLaVA-OneVision-72B 56.8（+4.5） | 强（多基准一致提升） |
| 信任权重机制 | Table 4：移除信任权重导致所有基准性能下降 | 强（消融验证） |
| 退火策略 | Table 4：同时移除信任权重和退火导致进一步下降；Table 8：指数衰减优于线性衰减 | 中等偏强 |
| 训练动态 | Figure 5：SophiaVL-R1 的平均结果奖励提升最快且最终值最高 | 中等（单一指标） |

### 局限与开放问题

当前的退火策略采用固定的指数衰减调度（$T$ 为常数），更复杂的调度策略——例如基于学习进度或奖励信号质量的自适应门控机制——可能带来进一步改进。这一问题在论文中被明确列为开放方向，表明退火策略的设计空间尚未被充分探索。



![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/004_Figure_3.jpg]]
*Figure 3: An illustration of our proposed Trust-GRPO*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/005_Figure_4.jpg]]
*Figure 4: Example of trustworthiness weight $\gamma$ . Incorrect responses (red) receive higher average thinking rewards than correct ones (green), indicating misalignment between $R ^ { t }$ and $R ^ { o \dot { } }$ and the need for a trustworthiness-aware adjustment

SophiaVL-R1 的整体框架围绕一个核心矛盾展开：**仅依赖规则化结果奖励的强化学习（RL）会忽视推理过程的质量**，导致模型可能学会“蒙对答案”但推理存在缺陷的策略。为解决这一问题，SophiaVL-R1 构建了一个三模块协同的强化学习训练管线，其关键创新在于将**思考过程质量**显式纳入奖励信号，并通过**动态可信度机制**抑制奖励黑客（reward hacking）风险。

### 管线总览

整个训练管线由三个核心模块串联构成，其信息流与协作关系如下：

1.  **思考奖励模型（Thinking Reward Model, TRM）**：在每轮采样后，对策略模型生成的完整推理过程进行整体质量评估，输出一个标量思考奖励 $R_i^t$。该模型基于 Qwen2.5-VL-3B-Instruct 初始化，在 SophiaVL-R1-Thinking-156k 数据集上通过 SFT 训练得到，评估维度涵盖逻辑正确性、推理准确性、错误识别、语言一致性和冗余度五个方面（附录 Table 5）。
2.  **规则结果奖励模块（Rule-based Outcome Reward）**：根据任务输出格式（数值、选择题、OCR、自由文本）计算准确性奖励 $R_i^o$。这是传统 GRPO 中唯一使用的奖励信号。
3.  **Trust-GRPO 训练循环**：这是框架的核心调度器。它接收上述两个奖励信号，执行三个关键操作后更新策略：
    *   **计算动态信任权重 $\gamma$**：通过对比同一问题下正确回答组与错误回答组的平均思考奖励差异来评估 TRM 的可靠性。当错误组的平均思考奖励反而更高时（即 $\mu_c < \mu_w$），权重 $\gamma = e^{\mu_c - \mu_w}$ 会衰减思考奖励的影响，防止模型被不可靠的过程信号误导（公式 3，Figure 4）。
    *   **组合奖励**：将结果奖励与加权后的思考奖励相加，形成总奖励 $R_i = R_i^o + \gamma \alpha R_i^t$（公式 4）。
    *   **退火调度**：引入指数衰减因子 $e^{-\mathrm{steps}/T}$，使思考奖励的影响随训练步数逐步降低，让模型在后期更依赖稳定可靠的结果奖励（公式 5）。最终优势估计 $A_i$ 基于组内标准化后的总奖励计算（公式 6），并用于 GRPO 的剪切目标函数更新策略（公式 7）。

### 核心因果机制

框架的关键设计意图在于**利用过程反馈引导可泛化推理模式的学习**，而非简单地奖励正确答案。其因果逻辑链为：

*   **瓶颈**：纯结果奖励 RL 无法区分“推理正确但答案错误”与“推理错误但答案正确”的样本，导致学到的策略泛化性差。
*   **调节变量**：引入 TRM 提供过程信号，但该信号本身可能不可靠（例如对错误推理打出高分）。因此，**信任权重 $\gamma$** 成为关键的调节变量——它动态评估 TRM 在当前批次中的可靠性，并据此缩放思考奖励的贡献。
*   **退火策略**：作为辅助机制，退火调度确保了训练早期模型能从过程信号中充分探索推理模式，而后期则收敛到以结果为导向的精确策略，避免对 TRM 的过度依赖。

### 证据支撑

*   **Figure 3** 给出了 Trust-GRPO 的完整流程示意图，清晰展示了从采样、双路奖励计算到信任权重调节与策略更新的闭环。
*   **Figure 4** 通过具体案例验证了信任权重的必要性：在错误回答组的平均思考奖励高于正确组时，$\gamma$ 有效压低了不可靠过程信号的权重。
*   **消融实验（Table 4）** 证实了框架各组件的因果贡献：移除信任权重（wo-trust）或同时移除信任权重与退火（wo-trust-and-annealing）均导致所有基准上的性能下降，其中 MathVista 从 71.3 分别降至 69.2 和 68.7。使用未经训练的 TRM（wo-trained-TRM）同样损害性能，表明高质量的过程奖励模型是框架生效的前提。



### 核心模块

SophiaVL-R1 的训练框架由三个关键模块构成：

**1. 思考奖励模型 (Thinking Reward Model, TRM)**

该模块负责对模型生成的完整推理过程进行整体质量评估。TRM 以 Qwen2.5-VL-3B-Instruct 为初始化权重，在 SophiaVL-R1-Thinking-156k 数据集上通过 SFT 训练 2 个 epoch 得到。给定问题与对应的思考过程，TRM 基于五个维度打分：逻辑正确性 (Logical Soundness)、推理正确性 (Correct Reasoning)、错误识别 (Error Identification)、语言一致性 (Language Consistency) 和冗余度 (Redundancy)，最终输出一个标量思考奖励 $R_i^t$。

**2. 规则结果奖励模块 (Rule-based Outcome Reward)**

该模块根据任务输出格式计算准确性奖励 $R_i^o$，覆盖四类任务：
- **数值类**：基于精确匹配给出二值奖励；
- **选择题**：基于选项匹配给出二值奖励；
- **OCR 类**：使用负词错误率 (negative WER) 作为连续奖励；
- **自由文本类**：通过答案相似度给出连续奖励。

**3. Trust-GRPO 训练循环**

该模块将上述两种奖励信号融合，核心创新在于引入动态信任权重 $\gamma$ 和退火策略，以缓解奖励黑客 (reward hacking) 问题。具体流程见 Figure 3：模型采样一组回答后，TRM 给出思考奖励，规则模块给出结果奖励；Trust-GRPO 计算信任权重并应用退火，得到组合奖励后更新策略。

---

### 关键公式推导

SophiaVL-R1 的核心机制围绕“思考奖励的可靠性”展开。直觉是：如果正确回答组的平均思考奖励反而低于错误回答组，说明 TRM 的判断与真实结果存在偏差，此时应降低思考奖励的影响权重。

**步骤一：分组统计**

首先，根据结果奖励 $R_i^o$ 将采样回答分为正确组和错误组（以 0.5 为阈值），分别计算两组的平均思考奖励：

$$\mu_c = \frac{1}{|G_{\mathrm{correct}}|} \sum_{i \in G_{\mathrm{correct}}} R_i^t, \quad G_{\mathrm{correct}} = \{ i \mid R_i^o \geq 0.5 \}$$

$$\mu_w = \frac{1}{|G_{\mathrm{wrong}}|} \sum_{i \in G_{\mathrm{wrong}}} R_i^t, \quad G_{\mathrm{wrong}} = \{ i \mid R_i^o < 0.5 \}$$

**步骤二：信任权重**

基于两组均值差定义信任权重 $\gamma$：当 $\mu_c \geq \mu_w$ 时，TRM 判断与结果一致，完全信任 ($\gamma = 1$)；当 $\mu_c < \mu_w$ 时，说明 TRM 存在偏差，信任度指数衰减：

$$\gamma = \begin{cases} 1, & \mu_c \geq \mu_w \\ e^{\mu_c - \mu_w}, & \mu_c < \mu_w \end{cases}$$

Figure 4 展示了一个典型案例：错误回答组（红色）的平均思考奖励高于正确组（绿色），此时 $\gamma < 1$，有效抑制了不可靠思考奖励的影响。

**步骤三：组合奖励与退火**

将信任权重作用于思考奖励，并与结果奖励相加，同时引入指数衰减调度，使思考奖励的影响随训练步数逐渐减弱：

$$R_i = R_i^o + \gamma \alpha e^{-\frac{\mathrm{steps}}{T}} \cdot R_i^t$$

其中 $\alpha$ 为思考奖励的基础缩放系数，$T$ 为衰减温度，$\mathrm{steps}$ 为当前训练步数。消融实验 (Table 8) 表明指数衰减略优于线性衰减。

**步骤四：优势估计与策略更新**

组合奖励经组内标准化得到优势 $A_i$：

$$A_i = \frac{R_i - \operatorname{mean}(\{R_1, R_2, \cdots, R_N\})}{\operatorname{std}(\{R_1, R_2, \cdots, R_N\})}$$

最终 Trust-GRPO 的目标函数为带 KL 惩罚的剪切目标：

$$\begin{array} { l } { { \displaystyle \mathcal { J } _ { G R P O } ( \theta ) = \mathbb { E } \left[ q \sim P ( Q ) , \left\{ o _ { i } \right\} _ { i = 1 } ^ { N } \sim \pi _ { \mathrm { o l d } } ( O | q ) \right] } } \\ { { \displaystyle \quad \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \left( \operatorname* { m i n } \left( \frac { \pi _ { \theta } \left( o _ { i } | q \right) } { \pi _ { \mathrm { o l d } } \left( o _ { i } | q \right) } A _ { i } , \mathrm { c l i p } \left( \frac { \pi _ { \theta } \left( o _ { i } | q \right) } { \pi _ { \mathrm { o l d } } \left( o _ { i } | q \right) } , 1 - \epsilon , 1 + \epsilon \right) A _ { i } \right) - \beta \mathbb { D } _ { \mathrm { K L } } [ \pi _ { \theta } | \pi _ { \mathrm { r e f } } ] \right) . } } \end{array}$$

---

### 设计要点总结

信任权重的核心在于利用“正确组 vs 错误组”的思考奖励对比来动态评估 TRM 的可靠性，而非简单地将思考奖励直接合并。这一设计在消融实验 (Table 4) 中得到验证：移除信任权重 (wo-trust) 会导致所有基准性能下降；同时移除信任权重和退火 (wo-trust-and-annealing) 则进一步恶化。此外，Table 7 表明基于均值对比的信任权重设计优于基于方差的替代方案。



## 实验与关键发现

### 主要结果

SophiaVL-R1-7B 在数学推理与通用多模态基准上均展现出显著的性能优势。在数学推理方面，如 Table 1 所示，SophiaVL-R1-7B 在 MathVista 上达到 **71.3%** 的平均准确率，相较于同样基于 Qwen2.5-VL-7B 的 GRPO 基线（67.5%）提升 **+3.8 个百分点**；在 MathVerse 上达到 **48.8%**，比 GRPO 基线（44.9%）提升 **+3.9 个百分点**。这一增益在 MathVista 的多数子任务上均有体现，尤其在科学推理（SCI: 70.5 vs. 65.6）和数学应用题（MWP: 76.9 vs. 73.1）上表现突出。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/006_Table_1.jpg]]
*Table 1: Comparison of models on MathVista and MathVerse. The best is bold, and the runner-up is underline. 1Scientific Reasoning, 2Textbook Question Answering, 3Arithmetic Reasoning, 4Math Word Problem, 5Logical Reasoning, 6Vision Intensive, 7Vision Only, 8Vision Dominant, 9Text Dominant, 10Text Lite*

在通用多模态能力方面，Table 2 显示 SophiaVL-R1-7B 在 MMMU 上达到 **61.3%**，不仅大幅超越同规模的 Qwen2.5-VL-7B + SFT+GRPO（57.2%），还比参数量为其 10 倍的 **LLaVA-OneVision-72B**（Li et al., 2024）高出 **4.5 个百分点**（56.8%）。在 MME 上，SophiaVL-R1-7B 取得 **2403.8** 分，优于 Qwen2.5-VL-7B + SFT+GRPO（2344.1）；在 MMBench（85.4%）和 MMStar（66.7%）上也均保持领先。ChartQA 上以 88.5% 位居第二，仅次于 InternVL2.5-8B-VisualPRM（89.0%）。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/007_Table_2.jpg]]
*Table 2: Comparison on general ability benchmarks. The best is bold, and the runner-up is underline*

值得注意的是，SophiaVL-R1-7B 在多数基准上超越了多个专门设计的开源推理 MLLM，包括 **R1-OneVision-7B**（Yang et al., 2025）、**Curr-ReFT-7B**（Deng et al., 2025a）以及采用过程奖励的 **InternVL2.5-8B-VisualPRM**（Wang et al., 2025b），表明思考奖励与 Trust-GRPO 的组合在引导可泛化推理方面具有独特优势。

### 消融研究

为验证各设计组件的贡献，Table 4 报告了系统的消融实验结果。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/009_Table_4.jpg]]
*Table 4: Ablation Study*

**信任权重的作用。** 移除信任权重（wo-trust，保留退火策略）导致所有基准上的性能下降：MathVista 从 71.3 降至 69.0，MMMU 从 61.3 降至 58.8，MMBench 从 85.4 降至 83.7。这表明，动态评估思考奖励的可靠性对于防止错误过程信号误导训练至关重要。

**信任权重与退火的联合作用。** 同时移除信任权重和退火策略（wo-trust-and-annealing）导致性能进一步恶化，在 MathVista 上降至 68.5，MMMU 降至 57.5，证实了二者协同保护的必要性——信任权重在训练全程调节信号质量，退火则确保训练后期模型逐步依赖更可靠的结果奖励。

**思考奖励模型质量的影响。** 使用未经训练的思考奖励模型（wo-trained-TRM）同样损害性能，MathVista 降至 69.2，MMMU 降至 59.0。这验证了在高质量标注数据上训练 TRM 是有效过程监督的前提。

**训练动态分析。** Figure 5 展示了不同方法在训练过程中平均规则结果奖励的变化曲线。SophiaVL-R1 的奖励提升速度最快且最终收敛值最高，表明其习得了更优的推理策略。相比之下，移除信任权重或退火策略的变体奖励增长较慢且最终值较低，说明这些机制有助于稳定训练并加速收敛。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_0tzvmjMcXC/figures/010_Figure_5.jpg]]
*Figure 5: Training curves of mean rule-based outcome reward across different methods*

**信任权重设计选择。** Table 7 对比了基于均值对比的信任权重（本文方案）与基于方差的替代方案。均值对比方法在所有基准上均优于方差方法，验证了通过对比正确组与错误组平均思考奖励来评估可靠性的设计更为有效。

**退火调度选择。** Table 8 对比了指数衰减与线性衰减调度。指数衰减在 MathVista（71.3 vs. 70.2）和 MMBench（85.4 vs. 84.1）上均优于线性衰减，表明在训练后期更平滑地降低思考奖励影响有利于模型稳定过渡到依赖结果奖励。

### 失败模式与局限性

尽管 SophiaVL-R1 取得了显著性能提升，分析揭示了以下局限：

1. **退火策略的刚性。** 当前的退火采用固定的指数衰减调度，缺乏对训练状态的自适应能力。在思考奖励质量波动较大的训练阶段，固定衰减可能过早或过晚降低其影响，导致次优的信号利用。更复杂的调度策略（如基于奖励门控或学习型衰减）可能带来进一步改进，这仍是一个开放问题。

2. **思考奖励模型的偏差。** Figure 6 和 Figure 7 展示了思考奖励模型的典型错误模式：当模型给出错误推理过程但恰好得到正确答案时，TRM 可能给出中等偏高的评分（如 0.7），而正确推理过程获得 0.9。这种“结果导向”的评分偏差在训练早期尤为明显，可能削弱过程监督的有效性。信任权重机制部分缓解了这一问题，但无法完全消除 TRM 自身的系统性偏差。

3. **跨任务泛化的边界。** 尽管在 MathVista 和 MMMU 等基准上表现优异，但在某些子任务（如 MathVista 的逻辑推理 LOG 子集，35.1%）上绝对分数仍然较低，提示思考奖励模型在纯逻辑推理场景下的评估能力可能不足。



## 定位与知识库关联

### 技术脉络与基线关系

SophiaVL-R1 的核心贡献在于将**过程级思考质量监督**引入多模态大模型（MLLM）的规则化强化学习（RL）范式。传统方法——如 **Qwen2.5-VL-7B-Instruct** (Bai et al., 2025) 直接应用 GRPO——仅依赖规则结果奖励 $R_i^o$，忽视了对推理过程本身的评估。这导致模型可能习得“答案碰巧正确但推理有缺陷”的策略，泛化能力受限。

该方法与现有 MLLM 推理增强工作的关系可从三个维度定位：

1. **相对于纯结果奖励方法**：**Qwen2.5-VL-7B + GRPO** 和 **Qwen2.5-VL-7B + SFT+GRPO** 代表了仅使用结果监督的基线。SophiaVL-R1 在相同基础模型上通过添加思考奖励，在 MathVista 上取得 71.3% 的平均准确率（对比 67.5%），验证了过程监督的增益。

2. **相对于过程奖励方法**：**InternVL2.5-8B-VisualPRM** (Wang et al., 2025b) 同样探索了过程奖励，但 SophiaVL-R1 的区别在于：（a）使用整体思考奖励而非逐步 PRM 标注；（b）引入信任权重 $\gamma$ 动态评估思考奖励的可靠性，而非无条件信任过程信号。这一设计直接回应了“过程奖励可能与结果奖励不一致”的风险。

3. **相对于其他推理 MLLM**：**R1-OneVision-7B** (Yang et al., 2025) 和 **Curr-ReFT-7B** (Deng et al., 2025a) 属于同期开源推理 MLLM。SophiaVL-R1-7B 在参数规模更小的情况下，在 MMMU 上达到 61.3%，甚至超过 72B 参数的 **LLaVA-OneVision-72B**（56.8%），表明思考奖励引导的 RL 训练在推理效率上具有优势。

### 适用边界与前提条件

该方法的设计隐含以下适用前提：

- **需要可标注的推理过程数据**：思考奖励模型（TRM）依赖 **SophiaVL-R1-Thinking-156k** 数据集进行 SFT 训练。该数据集从 GRPO 训练轨迹中收集推理回答并通过 GPT-4o 标注，因此方法适用于能生成显式推理链（chain-of-thought）的 MLLM 架构。
- **信任权重依赖于组内统计**：$\gamma$ 的计算需要同一问题的一组采样回答（论文中组大小 $N=8$），且依赖正确/错误组平均思考奖励的对比。当组内回答多样性不足或结果奖励分布极端时，$\gamma$ 的估计可能不稳定。
- **退火策略的固定性**：当前采用指数衰减 $\alpha e^{-\mathrm{steps}/T}$ 逐步降低思考奖励影响，使训练后期更依赖结果奖励。这一设计假设结果奖励在训练后期已足够可靠，但未根据实际训练动态自适应调整衰减速率。

### 局限性与开放问题

**已验证的局限**：

- 消融实验（Table 4）表明，移除信任权重（wo-trust）或同时移除信任权重与退火策略（wo-trust-and-annealing）会导致所有基准上性能下降，证实两个组件均为必要。然而，使用未经训练的 TRM（wo-trained-TRM）同样损害性能，说明思考奖励的质量高度依赖 TRM 的训练数据质量与标注一致性。
- 信任权重的均值对比设计优于基于方差的替代方案（Table 7），但该设计仅在 $\mu_c < \mu_w$ 时通过指数衰减降低权重。当两组均值接近时，$\gamma \approx 1$，思考奖励几乎不受抑制，可能在边界情况下仍引入噪声。
- 指数衰减调度略优于线性衰减（Table 8），但论文承认“更复杂的调度（如学习型或奖励门控）可能带来进一步改进”。

**开放问题**：

1. **思考奖励调度的自适应机制**：当前退火策略使用固定的指数衰减，是否存在基于训练动态（如结果奖励的方差、TRM 的校准度）自适应调整衰减速率的方法？奖励门控（reward-gating）策略——仅在思考奖励与结果奖励一致时激活过程监督——可能是更稳健的替代方案。
2. **TRM 的跨模型泛化性**：TRM 基于 Qwen2.5-VL-3B-Instruct 训练，其在其他架构 MLLM（如 LLaVA 系列）生成的推理链上的评分一致性尚未验证。若 TRM 对特定模型族存在偏好，可能限制方法的通用性。
3. **信任权重在多轮交互中的扩展**：当前 $\gamma$ 基于单轮采样的组内统计。在多轮对话或交互式推理场景中，如何累积历史信任信息来动态调整思考奖励权重，仍需探索。
4. **思考奖励的维度解耦**：TRM 从五个维度（逻辑正确性、推理正确性、错误识别、语言一致性、冗余度）综合评分。各维度对最终性能的贡献是否均衡？是否存在某些维度与结果奖励更易对齐，而其他维度需要不同的信任权重策略？这一问题尚未被系统研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/SophiaVL_R1_Reinforcing_MLLMs_Reasoning_with_Thinking_Reward.pdf]]
