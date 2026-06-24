---
title: "Probing to Refine: Reinforcement Distillation of LLM Reasoners via Explanatory Inversion"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Probing_to_Refine_Reinforcement_Distillation_of_LLM_Reasoners_via_Explanatory_Inversion.pdf
openreview_forum_id: rkIw2GqYEt
aliases:
- EEG
- PRRDLREI
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "引入认知科学启发的解释性反演（Explanatory Inversion, EI），生成强迫学生阐述答案背后逻辑的“解释性探测问题”，并利用带有对话结构效用奖励（Dialogue Structure Utility Bonus, r_dsu）的强化学习算法（ExGRPO）进行多轮交互训练，从而促使学生内化连贯的推理框架。"
primary_logic: "通过系统性的探测题挑战（而不是简单的数据增广）和对话结构层面的奖励（奖励完整多轮对话相对于部分对话的提分效果），学生模型从被动模仿转向主动构造可迁移的推理能力，从而显著提升鲁棒性和分布外泛化性能。"
claims:
- "ExGRPO使Gemma‑7b学生模型在平均准确率上相较零样本提升20.39%，超越SOTA蒸馏基线6.02%"
- "消融实验显示，移除对话结构效用奖励r_dsu会导致Qwen模型平均准确率从71.53%骤降至15.99%，证实该奖励是方法的核心组件"
- "在四个留存的分布外（OOD）数据集上，ExGRPO的平均准确率显著优于RevThink（Qwen: 82.34 vs 79.06; Gemma: 61.76 vs 56.87），展现了更强的泛化能力"
- "在样本效率实验中，仅使用10%训练数据的ExGRPO即可超越使用全部数据的监督微调（SFT），突显了方法的数据高效性"
---

# Probing to Refine: Reinforcement Distillation of LLM Reasoners via Explanatory Inversion

> [!tip] 核心洞察
> 通过系统性的探测题挑战（而不是简单的数据增广）和对话结构层面的奖励（奖励完整多轮对话相对于部分对话的提分效果），学生模型从被动模仿转向主动构造可迁移的推理能力，从而显著提升鲁棒性和分布外泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于解释性反演的LLM推理强化蒸馏 |
| 英文题名 | Probing to Refine: Reinforcement Distillation of LLM Reasoners via Explanatory Inversion |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rkIw2GqYEt); [GitHub](https://github.com/Zhen-Tan-dmml/ExGRPO.git) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ExGRPO (Explanatory GRPO) |
| Dataset | 8个领域内推理数据集（SQA, CSQA, ARC‑c, MATH, GSM8K, TabMWP, ANLI, Date）平均, 4个分布外（OOD）数据集（BoolQ, OpenbookQA, e‑SNLI, GSM8K‑Rev）平均, 样本效率：SQA和CSQA（10%训练数据）, 平均训练令牌效率对比（8数据集聚合） |

> [!tip] 效果简介
> - 8个领域内推理数据集（SQA, CSQA, ARC‑c, MATH, GSM8K, TabMWP, ANLI, Date）平均 上，准确率（%） 为 Qwen2.5‑7B: 82.54 / Gemma‑7B: 67.19，对比 Qwen2.5‑7B零样本: 77.99 / Gemma‑7B零样本: 46.80，变化 Qwen +4.55% / Gemma +20.39%。
> - 4个分布外（OOD）数据集（BoolQ, OpenbookQA, e‑SNLI, GSM8K‑Rev）平均 上，准确率（%） 为 Qwen2.5‑7B: 82.34 / Gemma‑7B: 61.76，对比 RevThink (最强基线): Qwen 79.06 / Gemma 56.87，变化 Qwen +3.28% / Gemma +4.89%。
> - 样本效率：SQA和CSQA（10%训练数据） 上，准确率（%） 为 ExGRPO (10%数据) 超过全量SFT的准确率，对比 SFT（全量100%数据），变化 定性超越。

## 概述

**问题瓶颈**：知识蒸馏是缩小大语言模型（LLM）规模的关键手段，但蒸馏得到的学生模型普遍存在表面模式记忆与泛化能力不足的问题。尤其在分布迁移场景下，模型表现出“反转诅咒”——能正确求解正向问题（如“5-2=3”），却无法求解其反向（“3+2=5”）。现有的A-to-Q反向数据增强方法（如RevThink）虽然试图缓解这一问题，但仍鼓励机械的方向映射，未能培养学生对深层逻辑的真正把握。

**核心思路**：本文提出**解释性反演**（Explanatory Inversion, EI）与**解释性GRPO**（ExGRPO）相结合的强化蒸馏框架。EI受认知科学启发，生成强迫学生阐述答案背后逻辑的“解释性探测问题”；ExGRPO则通过多轮交互训练，引入**对话结构效用奖励**（Dialogue Structure Utility Bonus, $r_{\text{dsu}}$），奖励完整探测对话相对于部分对话的性能提升，从而促使学生从被动模仿转向主动构造可迁移的推理能力。

**方法定位**：ExGRPO包含三个阶段——（1）EI探测问题生成与精选；（2）监督微调（SFT）热身；（3）基于GRPO的强化蒸馏，其中RL阶段融入对话结构奖励与辅助SFT损失以稳定训练。推理时仅需单次前向传播，多轮探测与奖励计算仅存在于训练阶段。

**主要结果**：
- 在8个领域内推理数据集上，ExGRPO使Gemma-7b学生模型的平均准确率相较零样本提升**20.39%**，超越SOTA蒸馏基线**6.02%**（Table 1）。
- 在4个留存的分布外（OOD）数据集上，ExGRPO平均准确率显著优于最强基线RevThink（Qwen: 82.34 vs 79.06; Gemma: 61.76 vs 56.87），展现更强的泛化能力（Table 2）。
- 消融实验证实：移除对话结构效用奖励$r_{\text{dsu}}$会导致Qwen模型平均准确率从71.53%骤降至15.99%，表明该奖励是方法的核心组件（Table 3）。
- 样本效率实验中，仅使用10%训练数据的ExGRPO即可超越使用全部数据的SFT，突显数据高效性（Figure 4）。

**关键贡献**：（1）提出解释性反演（EI）作为蒸馏数据增强的新范式；（2）设计对话结构效用奖励，从多轮交互结构中提取训练信号；（3）理论证明ExGRPO策略更新保证结果奖励单调不减；（4）在多个基准上取得显著的性能与泛化提升。

## 背景与动机

### 蒸馏学生模型中的“反转诅咒”与泛化脆弱性

大语言模型（LLM）的知识蒸馏旨在将大型教师模型的能力迁移到轻量级学生模型中，但现有蒸馏方法面临一个核心瓶颈：学生模型存在严重的**表面模式记忆**，导致泛化能力不足，尤其在分布迁移下表现脆弱。一个典型症状是“反转诅咒”（reversal curse）——模型能正确求解正向问题“5 − 2 = 3”，却无法求解反向问题“3 + 2 = 5”。Figure 1 直观展示了这一现象：蒸馏后的较小模型（如Gemma-7B）在原始测试集上的表现尚可，但在经过解释性反演（Explanatory Inversion, EI）增强的测试集上，性能显著低于教师模型（Gemini-1.5-Pro），暴露了学生对深层逻辑把握的缺失。

现有应对反转诅咒的方法，如RevThink为代表的A-to-Q反向推理数据增强，试图通过生成从答案到问题的逆思维数据来强化双向推理。然而，这类方法本质上仍鼓励**机械的方向映射**——学生学会的是在特定方向上的模式匹配，而非对推理逻辑本身的真正理解。因此，当面对分布外（OOD）的推理要求时，学生模型的表现依然脆弱。

### 现有蒸馏范式的局限

当前主流的蒸馏与数据增强策略可归纳为以下几类，各自存在固有局限：

- **知识蒸馏方法**（如Symbolic Knowledge Distillation、Distill Step-by-Step、On-Policy Distillation）：通过模仿教师输出或思维链来训练学生，但学生往往停留在对教师推理轨迹的表层复制，缺乏对因果结构的主动建构。
- **数据增强方法**（如Rephrase Question、Question Augmentation、Answer Augmentation）：通过改写或增广原始问题/答案来扩充训练数据，但增强的多样性受限于模板规则，且未改变学生被动接收信息的训练范式。
- **逆思维方法**（如RevThink）：虽引入了反向推理，但本质上仍是方向性的数据扩展，未能系统性地挑战学生去阐述“为什么”和“若非如此会怎样”等深层问题。

这些方法的共同缺陷在于：**训练范式以单轮直接问答为主，奖励信号仅依赖于最终答案的正确性**，无法区分学生是真正理解了推理过程，还是仅仅记忆了答案模式。

### 核心洞察：从被动模仿到主动解释

本文的核心洞察源于认知科学的启发：**真正的理解体现在能够解释、辩护和推广所学知识**。若能在蒸馏过程中系统性地向学生提出解释性挑战——迫使其阐述答案背后的逻辑、应对反事实假设、分解推理步骤——并通过强化学习奖励那些从完整解释序列中获益的行为，学生模型就有望从被动模仿转向主动构造可迁移的推理能力。

基于这一洞察，本文提出ExGRPO框架，通过两个关键创新解决上述瓶颈：

1. **解释性反演（Explanatory Inversion, EI）**：不满足于简单的A-to-Q反转，而是利用10种认知启发规则（反事实、解释挑战、因果强化等）生成多角度的“解释性探测问题”，系统性地挑战学生的深层理解。
2. **对话结构效用奖励（Dialogue Structure Utility Bonus, $r_{\text{dsu}}$）**：在强化学习过程中，不仅奖励最终答案的正确性，还额外奖励完整多轮解释对话相对于部分对话的提分效果，从而激励学生内化连贯的推理框架。

通过这种“探测以精炼”（Probing to Refine）的策略，ExGRPO使蒸馏过程从单向的知识传递转变为双向的解释性交互，为提升学生模型的鲁棒性和分布外泛化能力开辟了新路径。

## 核心创新

ExGRPO 的核心创新在于将认知科学启发的**解释性反演（Explanatory Inversion, EI）** 与带有**对话结构效用奖励（Dialogue Structure Utility Bonus, $r_{\text{dsu}}$）** 的强化学习算法深度融合，从根本上改变了蒸馏过程中学生模型的学习方式。

### 瓶颈洞察：从表面记忆到深层推理

现有蒸馏方法面临的核心瓶颈是学生模型倾向于记忆表面模式，而非内化推理框架。典型表现为“反转诅咒”：模型能正确求解正向问题“5-2=3”，却无法求解反向问题“3+2=5”。即便 RevThink 等 A-to-Q 反向数据增强方法，本质上仍在鼓励机械的方向映射（Section 1, Figure 1b-c），未能迫使学生掌握答案背后的深层逻辑。

### Changed Slot 1：数据增强策略——解释性反演（EI）

**Baseline 做法**：A-to-Q 反向推理或简单的问题改写/增广，仅改变问题表述或方向，不触及推理结构。

**ExGRPO 做法**：利用 10 种认知启发规则（反事实 R1、分解 R2、因果强化 R10 等）系统性地将原始问答 $(Q, A, R_T)$ 转化为**解释性探测问题** $Q_i^{\text{aug}}$，强迫学生阐述答案背后的推理逻辑（Section 3.1, Table 4）。这些探测问题经过两道严格过滤：

- **EI 一致性过滤**（Eq. 1）：确保探测题及其教师推理不会干扰原始问题的正确求解——当教师模型在给定探测题、推理、答案后仍能正确回答原始问题 $Q$ 时，该样本才被保留。
- **拒答过滤**（Eq. 2）：剔除基线学生模型全对（过于简单）或几乎全错（过于困难）的原始问题，仅保留难度适中的训练样本。

消融实验证实，全规则组合（81.50%）优于任一单类规则，其中反事实（R1）、原因导向（R10）和分解（R2）贡献最大（Table 4）。

### Changed Slot 2：交互协议——多轮解释性对话

**Baseline 做法**：单轮直接问答，模型仅需给出最终答案。

**ExGRPO 做法**：构建随机采样的 $k$ 轮解释性对话（Scenario A / Full Dialogue），学生需依次回答多个探测问题后再给出原始问题的最终答案。训练时同时采样部分对话（Scenario B / Partial Dialogue，仅前 $k'$ 轮）作为对比基线（Section 3.4.1）。这种设计为后续的对话结构奖励提供了信号来源。

### Changed Slot 3：奖励函数——对话结构效用奖励（$r_{\text{dsu}}$）

**Baseline 做法**：仅使用最终答案正确性的二元结果奖励 $R_{\text{outcome}}$。

**ExGRPO 做法**：在结果奖励之上引入**对话结构效用奖励** $r_{\text{dsu}}$（Eq. 5-6）。其核心机制为：

$$r_{\text{dsu}} = \begin{cases} \delta, & \text{if } P_{\text{full}} > \nu \cdot P_{\text{partial}} \\ 0, & \text{otherwise} \end{cases}$$

当完整 $k$ 轮对话的平均结果奖励 $P_{\text{full}}$ 超越部分 $k'$ 轮对话的 $P_{\text{partial}}$ 一定倍数 $\nu$ 时，给予固定额外奖励 $\delta$。这一设计的因果逻辑是：**奖励完整多轮对话相对于部分对话的提分效果**，从而激励模型从完整的探测序列中获益，内化连贯的推理框架。

**决定性证据**：消融实验显示，移除 $r_{\text{dsu}}$ 后，Qwen2.5-7B 的平均准确率从 71.53% 骤降至 15.99%，证实该奖励是方法的核心组件（Table 3）。定理 3.1 进一步证明，应用 $r_{\text{dsu}}$ 的 ExGRPO 策略更新保证结果奖励单调不减，且存在奖励触发时严格提升期望准确性（Appendix J）。

### Changed Slot 4：训练范式——三阶段强化蒸馏

**Baseline 做法**：单阶段监督微调（SFT）或标准 GRPO 仅基于结果奖励。

**ExGRPO 做法**：采用三阶段训练管线（Figure 2）：

1. **EI 数据生成**：基于 10 种模板规则生成解释性探测问题，经一致性与难度过滤得到精炼训练集 $D_{EI}$。
2. **SFT 热身**：在 $D_{EI}$ 上使用负对数似然损失微调学生模型，使其初步对齐教师的解释性推理风格（Eq. 3）。
3. **ExGRPO 强化蒸馏**：通过多轮探测对话采样、结果与对话结构奖励计算、GRPO 策略裁剪更新（Eq. 7），并结合辅助 SFT 损失 $\mathcal{L}_{\text{SFT-aux}}$（Eq. 8）稳定训练。

**关键发现**：跳过 SFT 热身直接进行 RL（冷启动）会导致灾难性性能崩溃——Qwen 降至 15.99%，Gemma 降至 12.34%（Table 3），表明 SFT 热身对于建立初始推理能力是必不可少的。辅助 SFT 损失进一步带来增益，例如 Gemma 在 SQA 上从 63.80 提升至 69.43。

### 创新效果的量化验证

| 维度 | 结果 | 证据锚点 |
|------|------|----------|
| 领域内性能 | Gemma-7b 平均准确率相较零样本提升 20.39%，超越 SOTA 蒸馏基线 6.02% | Table 1 |
| 分布外泛化 | 四个 OOD 数据集上显著优于 RevThink（Qwen: 82.34 vs 79.06; Gemma: 61.76 vs 56.87） | Table 2 |
| 样本效率 | 仅使用 10% 训练数据的 ExGRPO 即可超越使用全部数据的 SFT | Figure 4 |
| 令牌效率 | ExGRPO 的准确率-训练令牌数显著高于基线回归线 | Figure 5 |

这些结果表明，ExGRPO 通过系统性的探测题挑战和对话结构层面的奖励设计，成功促使学生模型从被动模仿转向主动构造可迁移的推理能力。

## 整体框架

![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/002_Figure_2.jpg]]

ExGRPO 的整体训练管线由三个顺序阶段构成：**解释性反演（EI）数据生成与精选 → 监督微调（SFT）热身 → 解释性 GRPO 强化蒸馏**。其核心设计理念是：不依赖简单的数据增广，而是通过系统性的多角度探测问题迫使学生在多轮交互中内化连贯的推理框架。

### 阶段一：EI 探针生成与数据精选

此阶段的目标是从原始问答对 $(Q, A, R_T)$（$R_T$ 为教师推理链）出发，生成高质量的解释性探测训练数据。

1. **探针生成**：利用 $N=10$ 种认知启发的变换规则 $\mathcal{F} = \{f_1, \ldots, f_N\}$（包括反事实、因果强化、分解、解释挑战等），将每个原始问题转化为多个探测问题 $Q_i^{\text{aug}} = f_i(Q, A, R_T)$。教师模型对每个探测问题生成相应的推理 $R_{T,i}^{\text{aug}}$ 和答案 $A_{T,i}^{\text{aug}}$，构成候选数据元组 $d_k = (Q, Q_k^{\text{aug}}, R_{T,k}^{\text{aug}}, A_{T,k}^{\text{aug}})$。

2. **EI 一致性过滤**：为确保探测问题不会干扰原始任务的求解，对每个候选元组施加一致性条件：
   $$\zeta_{EI}(d_k) \Leftrightarrow \mathcal{T}([Q_k^{\text{aug}} \,||\, R_{T,k}^{\text{aug}} \,||\, A_{T,k}^{\text{aug}} \,||\, Q]) = A$$
   即教师模型在完整看到探测题及其推理答案后，仍能正确回答原始问题 $Q$ 时，该样本才被保留。

3. **拒答过滤**：使用基线学生模型 $S_{\text{base}}$ 对每个原始问题 $Q$ 的所有 EI 一致性探针进行作答。保留那些既不“太简单”（学生全对）也不“太难”（答对数低于阈值 $\tau_{\text{hard}}$）的原始问题及其关联探针，形成精炼训练集 $D_{EI}$。

### 阶段二：SFT 热身

在精选的 $D_{EI}$ 上对学生模型 $\pi_\theta$ 进行监督微调，损失函数为标准负对数似然：
$$\mathcal{L}_{\text{SFT}}(\theta) = -\sum_{(Q_i^{\text{aug}}, T_i) \in D_{EI}} \sum_{t=1}^{|T_i|} \log P(T_{i,t} \mid Q_i^{\text{aug}}, T_{i,<t}; \theta)$$
其中 $T_i$ 为教师对探测问题的完整响应（推理链 + 答案）。此阶段使学生模型初步对齐教师的解释性推理风格，为后续强化学习提供稳定的策略起点。

### 阶段三：ExGRPO 强化蒸馏

这是方法的核心阶段，将 GRPO 算法适配到多轮解释性对话场景中。

1. **多轮交互协议**：对训练批次中的每个原始问题 $Q$，随机采样 $k$ 轮 EI 探针，构建解释性对话。训练时采样两种交互场景：
   - **Scenario A（完整对话）**：使用全部 $k$ 轮探针；
   - **Scenario B（部分对话）**：仅使用前 $k' < k$ 轮探针。
   两种场景的对比为对话结构效用奖励提供信号。

2. **双层奖励机制**：
   - **结果奖励 $R_{\text{outcome}}^{(g)}$**：学生轨迹 $g$ 中最终答案与真值 $A$ 匹配时给予二元奖励 1，否则为 0。
   - **对话结构效用奖励 $r_{\text{dsu}}$**：当完整对话（Scenario A）的平均结果奖励 $P_{\text{full}}$ 超过部分对话（Scenario B）的 $\nu$ 倍时，额外给予固定奖励 $\delta$：
     $$r_{\text{dsu}} = \begin{cases} \delta, & \text{if } P_{\text{full}} > \nu \cdot P_{\text{partial}} \\ 0, & \text{otherwise} \end{cases}$$
   - **总增强奖励**：仅当学生在 Scenario A 中答对原题且触发 $r_{\text{dsu}}$ 时，总奖励为基础奖励加 $\delta$；否则仅为基础奖励。

3. **策略优化**：采用带裁剪的重要性采样更新，结合 KL 散度正则化防止策略偏离参考模型：
   $$\mathcal{L}_{\text{ExGRPO}}(\theta) = \mathbb{E}_{\text{traj}_g \sim \pi_{\theta_{\text{old}}}} \left[ \sum_{g=1}^{G} \min\left( \rho^{(g)}(\theta) U^{(g)}, \text{clip}(\rho^{(g)}(\theta), 1-\epsilon, 1+\epsilon) U^{(g)} \right) \right] - \beta \mathbb{D}_{\text{KL}}(\pi_\theta || \pi_{\text{ref}})$$
   其中 $U^{(g)}$ 为基于组内归一化的优势函数。

4. **辅助 SFT 损失**：在 RL 阶段的每个对话轮次中，附加最大化教师推理响应的对数似然，用于稳定训练并引导中间推理步骤：
   $$\mathcal{L}_{\text{SFT-aux}} = -\sum_{j=1}^{k} \log \pi_{\theta}(R_{T,j}^{\text{aug}} \mid Q_j^{\text{aug}}, \text{context})$$

### 推理阶段

训练完成后，学生模型在推理时仅需单次前向传播：对输入问题 $Q$ 直接生成推理链和最终答案。多轮探测对话、规则采样及奖励计算（包括 $r_{\text{dsu}}$）均为训练时专用机制，不增加推理开销。

### 关键模块关系

整个管线的信息流可概括为：**原始问答 → EI 规则生成探测题 → 一致性与难度过滤 → SFT 初步对齐 → ExGRPO 多轮交互强化 → 单轮推理部署**。其中，对话结构效用奖励 $r_{\text{dsu}}$ 是连接多轮交互协议与策略优化的核心纽带——它显式奖励完整探测序列相对于部分序列的提分效果，从而驱动学生模型从被动模仿转向主动构建可迁移的推理能力。定理 3.1 进一步从理论上保证：应用 $r_{\text{dsu}}$ 的 ExGRPO 策略更新可使期望结果奖励单调不减，且在奖励触发时严格提升期望准确性。

## 核心模块与公式推导

### 整体框架

ExGRPO 框架由三个顺序阶段构成：**解释性反演（EI）数据生成与筛选** → **监督微调（SFT）热身** → **ExGRPO 强化蒸馏**。图 2 给出了框架总览。

### 模块一：EI 探针生成与数据筛选

**EI 探针生成**：给定原始问答 $(Q, A)$ 及教师推理 $R_T$，系统应用 $N=10$ 类认知启发的转换规则 $\mathcal{F} = \{f_1, \dots, f_N\}$，生成解释性探测问题 $Q_i^{\text{aug}} = f_i(Q, A, R_T)$。10 类规则包括反事实（R1）、分解（R2）、解释挑战（R3）、因果强化（R10）等（完整规则见附录 E）。

**EI 一致性过滤**：并非所有探测问题都有益——某些探测可能干扰原始任务的求解。因此对每个候选样本 $d_k = (Q_k^{\text{aug}}, R_{T,k}^{\text{aug}}, A_{T,k}^{\text{aug}}, Q, A)$，执行一致性检查：

$$\zeta_{EI}(d_k) \Leftrightarrow \mathcal{T}([Q_k^{\text{aug}} \,||\, R_{T,k}^{\text{aug}} \,||\, A_{T,k}^{\text{aug}} \,||\, Q]) = A$$

该条件确保：教师模型 $\mathcal{T}$ 在看到探测题及其推理与答案后，仍能正确回答原始问题 $Q$。若不能，说明该探测可能引入干扰，予以剔除。

**拒答过滤**：进一步筛选难度适中的原始问题。设基线学生模型 $S_{\text{base}}$ 在问题 $Q$ 的 $N'_Q$ 个 EI 一致性探针上作答，$\Lambda_{Q, S_{\text{base}}}$ 为答对数量。过滤条件为：

$$(\neg(\Lambda_{Q,S_{\text{base}}} = N'_Q \wedge N'_Q > 0)) \wedge (\neg(\Lambda_{Q,S_{\text{base}}} \geq \tau_{\text{hard}} \wedge N'_Q > 0))$$

即：基线学生不能全对（至少有一题有挑战），且至少答对 $\tau_{\text{hard}}$ 题（避免过难）。通过双重筛选的数据集记为 $D_{EI}$。

### 模块二：SFT 热身

在 $D_{EI}$ 上对学生模型 $\pi_\theta$ 进行监督微调，损失为负对数似然：

$$\mathcal{L}_{\text{SFT}}(\theta) = - \sum_{(Q_i^{\text{aug}}, T_i) \in D_{EI}} \sum_{t=1}^{|T_i|} \log P(T_{i,t} \mid Q_i^{\text{aug}}, T_{i,<t}; \theta)$$

目标序列 $T_i$ 包含教师的推理链与最终答案。此阶段使学生初步对齐教师的解释性推理风格，为后续 RL 提供稳定初始化。消融实验（Table 3）证实：跳过 SFT 直接从冷启动 RL 会导致灾难性退化（Qwen 平均准确率降至 15.99%，Gemma 降至 12.34%）。

### 模块三：ExGRPO 强化蒸馏

#### 交互协议

对每个原始问题 $Q$，从 $D_{EI}$ 中随机采样 $k$ 个 EI 探针，构造 $k$ 轮解释性对话。训练时采样两种轨迹：
- **Scenario A（完整对话）**：学生依次回答所有 $k$ 个探针后，回答原始问题 $Q$。
- **Scenario B（部分对话）**：仅使用前 $k' < k$ 个探针（随机截断）。

#### 奖励函数

**结果奖励**（Outcome Reward）：二元奖励，学生最终答案与真值 $A$ 匹配时为 1，否则为 0。

$$R_{\text{outcome}}^{(g)}(Q, A) = \begin{cases} 1, & \text{学生最终答案与真值 } A \text{ 匹配} \\ 0, & \text{否则} \end{cases}$$

**对话结构效用奖励**（Dialogue Structure Utility Bonus, $r_{\text{dsu}}$）：这是方法的核心创新。设 $P_{\text{full}}$ 为 Scenario A 的平均结果奖励，$P_{\text{partial}}$ 为 Scenario B 的平均结果奖励。当完整对话显著优于部分对话时，给予固定额外奖励 $\delta$：

$$r_{\text{dsu}} = \begin{cases} \delta, & \text{if } P_{\text{full}} > \nu \cdot P_{\text{partial}} \\ 0, & \text{otherwise} \end{cases}$$

其中 $\nu \geq 1$ 为倍数阈值。该奖励显式鼓励模型从完整的探测序列中获益，而非机械记忆单轮问答。

**总增强奖励**：

$$R_{\text{total}}^{(g)} = \begin{cases} R_{\text{base}}^{(g)} + r_{\text{dsu}}, & \text{if } R_{\text{outcome}}^{(g)} = 1 \text{（来自 Scenario A）且 Eq. (5) 产生 } \delta \\ R_{\text{base}}^{(g)}, & \text{otherwise} \end{cases}$$

#### 策略优化

ExGRPO 基于 GRPO 进行策略更新，对每组 $G$ 条轨迹计算优势函数 $U^{(g)}$，并通过裁剪重要性采样比率 $\rho^{(g)}(\theta)$ 稳定更新：

$$\mathcal{L}_{\text{ExGRPO}}(\theta) = \mathbb{E}_{\text{traj}_g \sim \pi_{\theta_{\text{old}}}} \left[ \sum_{g=1}^{G} \min\left( \rho^{(g)}(\theta) U^{(g)}, \text{clip}(\rho^{(g)}(\theta), 1-\epsilon, 1+\epsilon) U^{(g)} \right) \right] - \beta \mathbb{D}_{\text{KL}}(\pi_\theta || \pi_{\text{ref}})$$

其中 KL 散度正则化防止策略偏离参考模型 $\pi_{\text{ref}}$ 过远。

#### 辅助 SFT 损失

为稳定训练并引导中间推理，在每个对话轮次附加辅助损失，最大化教师推理响应的对数似然：

$$\mathcal{L}_{\text{SFT-aux}} = - \sum_{j=1}^{k} \log \pi_{\theta}(R_{T,j}^{\text{aug}} \mid Q_j^{\text{aug}}, \text{context})$$

消融实验（Table 3）显示，引入 $\mathcal{L}_{\text{SFT-aux}}$ 带来进一步增益（如 Gemma 在 SQA 上从 63.80 提升至 69.43）。

#### 理论保证

定理 3.1（附录 J）证明：应用 $r_{\text{dsu}}$ 的 ExGRPO 策略更新保证结果奖励单调不减，且当 $r_{\text{dsu}} > 0$ 触发时，期望准确率严格提升。这为对话结构奖励的有效性提供了理论支撑。

#### 推理阶段

推理时，训练好的学生模型 $\pi_\theta$ 对输入 $Q$ 进行单次前向传播，直接生成推理链与最终答案。多轮探测对话、随机规则采样及 $r_{\text{dsu}}$ 计算仅存在于训练阶段，推理无额外开销。

## 实验与分析

### 核心瓶颈与设计动机

蒸馏得到的学生LLM普遍存在表面模式记忆和泛化能力不足的问题，尤其在分布迁移下表现脆弱。典型表现是“反转诅咒”：模型能正确求解正向问题“5-2=3”，却无法求解反向问题“3+2=5”。现有的A-to-Q反向数据增强方法（如RevThink）仍鼓励机械的方向映射，未能培养学生对深层逻辑的把握。本文引入认知科学启发的解释性反演（Explanatory Inversion, EI），生成强迫学生阐述答案背后逻辑的“解释性探测问题”，并利用带有对话结构效用奖励（Dialogue Structure Utility Bonus, $r_{\text{dsu}}$）的强化学习算法ExGRPO进行多轮交互训练，促使学生从被动模仿转向主动构造可迁移的推理能力。

### 主实验结果

Table 1展示了在8个领域内推理数据集（SQA, CSQA, ARC-c, MATH, GSM8K, TabMWP, ANLI, Date）上的主实验结果。ExGRPO在两个学生模型上均取得显著提升：Qwen2.5-7B的平均准确率达到82.54%，相较零样本（77.99%）提升4.55个百分点；Gemma-7B达到67.19%，相较零样本（46.80%）提升20.39个百分点，且超越最强蒸馏基线6.02个百分点。


![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/003_Table_1.jpg]]
*Table 1: Main results comparing our ExGRPO against zero-shot performance and various knowledge distillation and data augmentation baselines across eight held-in reasoning datasets for Qwen2.5-7B-Instruct and Gemma-7B-it student models. Teacher model performance is also shown for reference. ExGRPO shows consistent improvements. Scores are reported in percentage (%). * indicates the score is quoted from RevThink (Chen et al., 2025a).The contribution of each rule is studied in Appendix F*

ExGRPO在所有数据集上一致优于知识蒸馏基线（SKD、Distill Step-by-Step、On-Policy Distillation）和数据增强基线（Rephrase Question、Question Aug、Answer Aug、RevThink、Divide-or-Conquer）。值得注意的是，RevThink作为解决反转诅咒的代表方法，在Gemma上仅达到61.17%，而ExGRPO达到67.19%，差距达6.02个百分点，表明简单的A-to-Q反向推理远不如系统性探测题挑战有效。

### 分布外泛化

Table 2展示了在4个留存的分布外（OOD）数据集（BoolQ, OpenbookQA, e-SNLI, GSM8K-Rev）上的泛化结果。ExGRPO在Qwen上平均准确率为82.34%，显著优于RevThink的79.06%（+3.28%）；在Gemma上为61.76%，优于RevThink的56.87%（+4.89%）。这一结果表明，通过解释性探测训练获得的可迁移推理框架，在未见过的数据分布上同样具有鲁棒性。


![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/007_Table_2.jpg]]
*Table 2: OOD generalization on four held-out datasets. ExGRPO significantly improves generalization across both Qwen2.5-7B and Gemma-7B*

### 消融实验：核心组件分析

Table 3的消融实验揭示了ExGRPO各组件的关键作用，所有变体均使用相同的EI增强数据集训练。


![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/004_Table_3.jpg]]
*Table 3: Ablation study on the impact of SFT warm-up training and RL components for ExGRPO. We evaluate performance across eight reasoning datasets. All model variants are trained using the same augmented datasets with EI probes. RL without $r _ { \mathrm { d s u } }$ treats each EI probe as an independent training sample without grouping across reasoning paths*

**对话结构效用奖励 $r_{\text{dsu}}$ 的不可替代性**：移除 $r_{\text{dsu}}$（仅保留结果奖励 $R_{\text{outcome}}$）导致Qwen模型平均准确率从71.53%骤降至15.99%，Gemma从63.80%降至12.34%。这证实了仅按独立样本训练RL无法学习有效推理——模型需要从完整探测序列相对于部分序列的提分效果中获得结构层面的奖励信号，才能内化连贯的推理框架。Theorem 3.1从理论上证明，应用 $r_{\text{dsu}}$ 的ExGRPO策略更新保证结果奖励单调不减，且当奖励触发时严格提升期望准确性。

**SFT热身的必要性**：跳过SFT热身直接进行RL（冷启动）导致灾难性性能崩溃——Qwen降至15.99%，Gemma降至12.34%。这表明EI探测数据分布与原模型训练分布存在显著差异，需要SFT阶段完成初步对齐，RL阶段才能在此基础上进行有效的策略优化。

**辅助SFT损失的增益**：在ExGRPO中引入辅助SFT损失（$\mathcal{L}_{\text{SFT-aux}}$）带来进一步提升。例如Gemma在SQA上从63.80提升至69.43，在CSQA上从63.80提升至70.31。该损失在每个对话轮次中附加最大化教师推理响应的对数似然，有效稳定了RL训练并引导中间推理步骤的质量。

### 单类EI规则贡献

Table 4展示了10种单类EI规则在Qwen上的SFT性能。所有单类规则均优于基线（Rephrase Question, 78.88%），其中反事实（R1, 80.13%）、原因导向（R10, 80.00%）和分解（R2, 79.88%）贡献最大。全规则组合达到81.50%，显著优于任一单类规则，验证了多样化探测角度对推理能力培养的互补性。


![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/013_Table_4.jpg]]
*Table 4: Performance (Accuracy %) of SFT with single EI probe types on Qwen2.5-7B-Instruct. All EI rules outperform the baseline, and the full EI combination yields the best results*

### 样本效率与令牌效率

Figure 4展示了样本效率对比：ExGRPO在所有训练数据比例（10%、25%、50%、100%）下均超越标准SFT，且仅使用10%训练数据的ExGRPO即可超越使用全量数据的SFT（在SQA和CSQA上尤其显著），突显了方法的数据高效性。


![[assets/figures/papers/iclr26_0012_rkIw2GqYEt_Probing_to_Refine_Reinforcement_Distillation_of/figures/009_Figure_4.jpg]]
*Figure 4: Sample efficiency comparison on eight datasets. Our ExGRPO method achieves higher accuracy than standard SFT across all training data fractions ( p $\in \{$ 0 . 1 , 0 . 2 5 , 0 . 5 , 1 . 0 $\}$ ) , often surpassing SFT trained on the full dataset with only 10 − 25% of the data*

Figure 5展示了令牌效率对比：以平均准确率对平均训练令牌数作图，ExGRPO显著高于基线回归线，表明在相同计算预算下，ExGRPO的推理蒸馏效率大幅领先于SKD、Distill Step-by-Step、RevThink等方法。

### 训练动态

Figure 3展示了Gemma作为学生模型时ExGRPO训练过程中的奖励曲线。基础奖励 $R_{\text{base}}$ 随训练稳步上升，而 $r_{\text{dsu}}$ 在训练中后期逐渐触发并增长，表明模型逐渐学会了从完整探测序列中获益，验证了对话结构奖励机制的有效性。

### 局限性与待验证问题

尽管ExGRPO表现优异，仍需注意以下局限：解释性探测问题依赖人工设计的10种模板规则，自动化程度有限；训练计算开销约为单阶段SFT基线的1.5倍；实验验证集中在文本推理任务，尚未扩展到多模态或极长上下文推理场景。此外，对话结构效用奖励完全基于最终答案正确性，未引入对中间推理步骤的语义监督，在某些需要精细推理评分的任务上可能不够敏感。这些方向有待后续工作探索。
## 方法谱系与知识库定位

### 与基线方法的关系

ExGRPO 在知识蒸馏和数据增强两条技术路线上均与现有方法形成明确对比。

**知识蒸馏基线**方面，Symbolic Knowledge Distillation (SKD)、Distill Step‑by‑Step 和 On‑Policy Distillation 代表了从教师模型向学生模型传递推理能力的经典范式。这些方法的核心瓶颈在于学生模型倾向于记忆教师输出的表面模式，而非内化深层推理结构——典型表现为“反转诅咒”：模型能正确求解“5−2=3”，却无法求解“3+2=5”。ExGRPO 通过引入解释性反演（EI）生成的探测问题，迫使学生在多轮对话中阐述答案背后的逻辑，从而突破被动模仿的局限。在 Gemma‑7b 学生模型上，ExGRPO 相较零样本提升 20.39%，超越最强蒸馏基线 6.02%（Table 1）。

**数据增强基线**方面，Rephrase Question、Question Aug / Answer Aug 等方法通过改写或增广问题来丰富训练数据，但本质上仍鼓励机械的模式匹配。RevThink 作为解决反转诅咒的代表方法，采用 A‑to‑Q 反向推理进行数据增强，但其方向映射策略未能培养学生对深层逻辑的把握。ExGRPO 的 EI 探测则基于 10 种认知启发规则（反事实、因果强化、分解等）生成多角度解释性挑战，并通过一致性与难度过滤精选高质量样本。在四个留存的分布外（OOD）数据集上，ExGRPO 的平均准确率显著优于 RevThink（Qwen: 82.34 vs 79.06; Gemma: 61.76 vs 56.87），展现了更强的泛化能力（Table 2）。

### 适用边界

ExGRPO 的适用边界由以下几个维度界定：

1. **任务域**：当前验证集中在文本推理任务（常识推理、数学推理、表格推理、自然语言推理），尚未扩展到多模态推理或极长上下文推理场景。论文明确将此列为开放问题。

2. **学生模型规模**：实验覆盖 Qwen2.5‑7B‑Instruct 和 Gemma‑7B‑it 两个 7B 级模型。对于更小或更大的学生模型，方法的有效性有待验证。

3. **教师模型依赖**：EI 探测问题的生成和质量过滤均依赖教师模型的能力。教师模型的规模、预训练领域和推理水平直接影响探测质量，进而影响学生模型的蒸馏上限。论文在附录中展示了使用 Llama‑3‑70B‑Instruct 和 Gemini‑1.5‑Pro 作为教师的结果，但未系统探讨教师能力与蒸馏效果之间的定量关系。

4. **计算开销**：ExGRPO 的训练计算开销约为单阶段 SFT 基线的 1.5 倍。虽然换取了更高的泛化性能，但在资源受限场景下仍需权衡。

### 局限与开放问题

**方法层面的局限**：

- **模板依赖**：EI 探测问题依赖人工设计的 10 种模板规则，自动化程度有限。论文指出未来可探索学习型探针生成器或自我对弈机制。
- **奖励粒度粗糙**：对话结构效用奖励 $r_{\mathrm{dsu}}$ 完全基于最终答案的正确性，未引入对中间推理步骤的语义监督。在某些需要精细推理评分的任务上，该奖励信号可能不够敏感。
- **探测深度与最终决策的衔接**：消融实验揭示了“探测回答正确但最终选择错误”的现象，表明探测级别的深层理解尚未稳健地传递到最终答案选择步骤。

**理论层面的开放问题**：

- 定理 3.1 证明了应用 $r_{\mathrm{dsu}}$ 的 ExGRPO 策略更新保证结果奖励单调不减，且存在奖励触发时严格提升期望准确性。但该理论保证的前提是完整对话相对于部分对话的效用优势能够被可靠检测——这依赖于阈值 $\nu$ 和奖金 $\delta$ 的设定。这些超参数是否可自适应调整以进一步优化训练效率和最终性能，仍是一个开放问题。

**扩展方向的开放问题**：

- 该方法在多模态（图文混合推理）和超长上下文推理任务上的表现如何？模型是否能从多轮解释性对话中获取长期依赖学习？
- 能否开发出无需人工模板的自动化探针生成方法（例如基于学习的探针控制器或自我对弈机制）？
- 教师模型的能力如何定量影响 EI 探测的质量以及学生模型的蒸馏上限？

**需要人工验证的点**：论文未提供 ExGRPO 在非英文推理任务上的实验，跨语言泛化能力尚不明确。此外，对话结构效用奖励的阈值 $\nu$ 和奖金 $\delta$ 的敏感性分析未在主实验中展开，相关超参数调优策略需要进一步查阅附录确认。

## 原文 PDF

![[paperPDFs/ICLR_2026/Probing_to_Refine_Reinforcement_Distillation_of_LLM_Reasoners_via_Explanatory_Inversion.pdf]]
