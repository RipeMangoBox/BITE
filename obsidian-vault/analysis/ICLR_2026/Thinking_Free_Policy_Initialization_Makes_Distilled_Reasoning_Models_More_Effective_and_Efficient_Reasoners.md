---
title: "Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Thinking_Free_Policy_Initialization_Makes_Distilled_Reasoning_Models_More_Effective_and_Efficient_Reasoners.pdf
openreview_forum_id: RKYO6R8Jgb
aliases:
- TTFPI
- TFPIMDRMMEER
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "ThinkingFree操作：在输入查询中显式丢弃思考内容，通过直接附加</think>标记来减少推理时的token生成量，并在RLVR训练前应用此转换以降低rollout成本。"
primary_logic: "通过在标准RLVR训练前引入一个低成本的多阶段ThinkingFree初始化阶段（TFPI），可以加速RL收敛、提升最终性能上限，并生成更高效的token推理模型，无需复杂的奖励设计或训练流水线。"
claims:
- "TFPI在相同训练计算下显著优于直接RLVR：在Qwen3-4B上，TFPI Stage 3总体准确率达63.8%，而Direct RL仅为60.2%（+3.6%）。"
- "TFPI+RL在相同计算预算下进一步提升性能：Qwen3-4B TFPI+RL总体65.7%，对比Direct RL 62.0%（+3.7%）。"
- "ThinkingFree推理使token消耗减少70%以上，且TFPI训练在短上下文下仍能提升慢思维性能。"
- "TFPI表现出跨领域迁移性：在DS-1.5B上，GPQA准确率由16.3%提升至29.6%，IFEval由36.6%提升至40.8%。"
---

# Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners

> [!tip] 核心洞察
> 通过在标准RLVR训练前引入一个低成本的多阶段ThinkingFree初始化阶段（TFPI），可以加速RL收敛、提升最终性能上限，并生成更高效的token推理模型，无需复杂的奖励设计或训练流水线。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无思维策略初始化：提升蒸馏推理模型的效果与效率 |
| 英文题名 | Thinking-Free Policy Initialization Makes Distilled Reasoning Models More Effective and Efficient Reasoners |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RKYO6R8Jgb); [GitHub](https://github.com/Tencent-Hunyuan/Thinking-Free_Policy_Initialization) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TFPI (Thinking-Free Policy Initialization) |
| Dataset | Overall Average (6 benchmarks), AIME 25, AIME 24 (Thinking-Free mode), GPQA Diamond |

> [!tip] 效果简介
> - Overall Average (6 benchmarks) 上，Overall Average accuracy (%) 为 63.8 (TFPI stage 3)，对比 60.2 (Direct RL)，变化 +3.6。
> - AIME 25 上，avg@32 accuracy (%) 为 76.0 (TFPI+RL)，对比 71.5 (Direct RL)，变化 +4.5。
> - AIME 24 (Thinking-Free mode) 上，avg@32 accuracy (%) and Tokens (K) 为 37.5%, 5.3K tokens (TFPI stage 3)，对比 29.6%, 16.7K tokens (DS-1.5B original Thinking mode)，变化 +7.9% accuracy, -11.4K tokens。

## 概述

在强化学习可验证奖励（RLVR）训练中，基于监督微调蒸馏的大推理模型（LRM）往往产生冗长的思考链响应，导致训练上下文长度需求过大、计算成本高昂，而直接缩短训练长度又会带来不可逆的性能下降。针对这一瓶颈，本文提出**TFPI（Thinking-Free Policy Initialization）**，一种低成本的多阶段策略初始化方法。其核心操作**ThinkingFree**在输入查询中显式丢弃思考内容，通过直接附加`</think>`标记来大幅减少推理时的token生成量，并在标准RLVR训练前应用此转换以降低rollout成本。

核心洞察在于：通过在标准RLVR训练前引入TFPI初始化阶段，可以加速RL收敛、提升最终性能上限，并生成更高效的token推理模型，无需复杂的奖励设计或训练流水线。实验表明，TFPI在相同训练计算预算下显著优于直接RLVR：在Qwen3-4B上，TFPI Stage 3总体准确率达63.8%，而Direct RL仅为60.2%（+3.6%）；进一步附加标准RLVR后（TFPI+RL），总体准确率提升至65.7%，对比Direct RL的62.0%提升3.7个百分点。在token效率方面，ThinkingFree推理使token消耗减少70%以上，且TFPI训练在短上下文（4K）下仍能提升慢思维性能。该方法还表现出跨领域迁移性：在DS-1.5B上，GPQA准确率由16.3%提升至29.6%，IFEval由36.6%提升至40.8%。

TFPI定位为RLVR训练前的低成本初始化阶段，可与现有RLVR算法（如DAPO）无缝衔接，其多阶段渐进增加输出长度的训练策略（如2K→4K→8K）是实现短上下文高效训练的关键。当前验证主要基于数学推理数据集，在中小规模模型（最高7B）上展现出稳定的性能增益与token效率优势，向更大模型及更广泛领域的扩展仍有待探索。

## 背景与动机

大推理模型（Large Reasoning Models, LRMs）通过在最终答案前生成显式的“思考链”（chain-of-thought）来提升复杂推理能力。当前主流训练范式通常包含两个阶段：首先通过监督微调（SFT）从强教师模型蒸馏长思考链数据，随后采用基于可验证奖励的强化学习（RLVR）进一步优化推理策略。

然而，这一范式面临一个关键瓶颈：**SFT蒸馏模型在RLVR训练中倾向于生成过长的思考链响应**。这种冗长性导致两个严重后果。其一，RLVR rollout阶段的计算开销急剧膨胀——训练上下文长度需求过大，显著推高了训练成本。其二，如果为降低成本而强行限制训练时的最大响应长度（例如从32K降至4K），则会导致不可逆的性能崩溃（见 Figure 2 Right 和 Table 4 中的多阶段直接RL结果）。

现有应对方案存在明显不足。**Polaris**（An et al., 2025）和**DeepScaleR**（Luo et al., 2025b）等方法采用多阶段RLVR训练，但未从根本上解决长上下文依赖问题。**TLMRE**（Arora & Zanette, 2025）、**AdaptThink**（Zhang et al., 2025b）和**L1Max**（Aggarwal & Welleck, 2025）等基线试图通过奖励设计或正则化控制生成长度，但引入了额外的复杂性，且性能与token效率的权衡不够理想。

本文的核心动机在于：**能否在RLVR训练前，通过一个低成本、无复杂奖励设计的初始化阶段，同时实现加速RL收敛、提升性能上限和降低推理token消耗？** 这一问题的关键在于如何打破“长思考链是RLVR训练的必要前提”这一隐含假设。

## 核心创新

### 瓶颈：RLVR训练中的长思考链困境

当前主流的推理模型训练范式是从监督微调（SFT）蒸馏的大推理模型（LRM）出发，通过强化学习可验证奖励（RLVR）进一步优化。然而，这一流程存在一个关键瓶颈：SFT蒸馏模型在RLVR训练中倾向于生成过长的思考链响应，导致训练上下文长度需求急剧膨胀，计算成本高昂。若直接缩短训练上下文长度以降低成本，则会导致不可逆的性能崩溃——标准RLVR在4K响应长度下，avg@32准确率下降超过40%（Figure 2 Right）。这一“长上下文依赖”与“计算效率”之间的冲突，构成了现有RLVR训练范式的核心矛盾。

### 核心操作：ThinkingFree查询变换

TFPI的核心创新在于引入了一个简洁而高效的**ThinkingFree操作**。该操作将原始输入查询 $x$ 显式转换为无思考版本 $x' = \text{ThinkingFree}(x)$：在聊天模板的助手前缀后直接附加 `</think>` 标记，从而禁止模型生成显式思考链（Template 2）。这一操作带来两个直接效果：

- **大幅降低生成token量**：对DS-1.5B和Qwen3-4B，ThinkingFree模式使输出token减少70%以上（Figure 2 Left）。
- **在短上下文下仍提升慢思维能力**：即使在4K训练响应长度下，ThinkingFree RL训练仍能使AIME25准确率提升约2%，同时减少约20%的输出token（Figure 2 Right），而标准RLVR在相同长度下性能崩溃。

### 关键机制：TFPI作为RLVR的低成本初始化阶段

TFPI将ThinkingFree操作嵌入到RLVR训练目标中，形成**多阶段策略初始化**流程。具体而言，TFPI使用改编后的DAPO目标函数：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(y_{i,t} \mid x', y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t} \mid x', y_{i,<t})}, \quad \widehat{A}_{i,t} = \widehat{A}_i = \frac{r(x', y_i) - \operatorname{mean}(\{r(x', y_j)\}_{j=1}^G)}{\operatorname{std}(\{r(x', y_j)\}_{j=1}^G)}$$

其中查询 $x$ 被替换为ThinkingFree版本 $x'$。TFPI通过渐进增加最大输出长度（如2K→4K→8K）的多阶段训练，实现以下关键效果：

1. **加速RL收敛**：TFPI所有三个阶段的总计算量不足标准32K上下文RL训练的20%（Figure 1 Left），却能提供高质量的初始策略。
2. **提升性能上限**：在相同训练计算预算下，TFPI Stage 3在Qwen3-4B上总体准确率达63.8%，显著优于直接RL的60.2%（+3.6%，Table 1）；附加标准RLVR后（TFPI+RL），性能进一步提升至65.7%，对比直接RL的62.0%（+3.7%，Table 2）。
3. **产生token高效模型**：TFPI训练的模型在ThinkingFree推理模式下展现出卓越的效率-准确率权衡。DS-1.5B在TFPI Stage 3下以仅5.3K平均token获得AIME24 37.5%准确率，而原始模型在思考模式下需16.7K token仅得29.6%（Table 3）。TFPI各阶段在准确率-token使用量的Pareto前沿上持续占据优势位置（Figure 1 Right）。
4. **跨领域迁移**：尽管仅在数学数据上训练，TFPI在GPQA（16.3%→29.6%）、LiveCodeBench（17.7%→19.9%）和IFEval（36.6%→40.8%）上均展现出显著的领域外提升（Table 1, DS-1.5B）。

### 与基线方法的本质区别

TFPI与现有方法的根本差异在于**改变RLVR的rollout查询格式**，而非修改奖励设计或添加长度惩罚：

| 对比维度 | Direct RL / 标准RLVR | TFPI |
|---------|---------------------|------|
| rollout查询格式 | 标准思维模板，允许完整思考链 | ThinkingFree模板，显式跳过思考内容 |
| 训练上下文效率 | 需长上下文（如32K）维持性能 | 短上下文（2K-8K）即可有效训练 |
| 收敛速度 | 慢，需大量计算 | 快，总计算量<标准RL的20% |
| token效率 | 生成冗长思考链 | 生成token减少70%+ |

与**Polaris**（An et al., 2025）的多阶段RLVR、**DeepScaleR**（Luo et al., 2025b）的迭代长度控制、**TLMRE**（Arora & Zanette, 2025）的token效率RL等方法不同，TFPI不需要复杂的奖励塑造、长度惩罚或动态思考控制机制。其核心洞察是：**通过在RLVR训练前引入一个低成本的ThinkingFree初始化阶段，可以同时实现加速收敛、提升性能上限和生成高效token推理模型的三重目标**（Figure 1）。多阶段直接RL（无TFPI）在相同长度计划下性能大幅下降（Qwen3-4B总体52.9% vs TFPI 63.8%，Table 4），进一步验证了ThinkingFree操作而非多阶段训练本身才是性能提升的关键因果因素。

## 整体框架

TFPI（Thinking-Free Policy Initialization）的整体框架围绕一个核心操作展开：**ThinkingFree查询变换**。该方法将标准RLVR训练流程重构为一个“低成本初始化 + 可选标准强化”的两阶段范式，其pipeline模块关系与输入输出流如下。

### 核心操作：ThinkingFree查询变换

ThinkingFree是一个输入查询层面的变换算子，定义为 $x' = \text{ThinkingFree}(x)$。其具体操作是：在原始查询 $x$ 的助手前缀后直接附加 `<think>\n\n</think>`，显式跳过思考内容的生成。这一变换在推理时将输出token量削减70%以上（Figure 2 Left），从而大幅降低rollout的计算成本。

### 三阶段TFPI训练

TFPI训练分为三个递进阶段，每个阶段使用ThinkingFree变换后的查询 $x'$ 进行RLVR训练，并采用修改后的DAPO目标函数：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(y_{i,t} \mid x', y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t} \mid x', y_{i,<t})}, \quad \widehat{A}_{i,t} = \widehat{A}_i = \frac{r(x', y_i) - \operatorname{mean}(\{r(x', y_j)\}_{j=1}^G)}{\operatorname{std}(\{r(x', y_j)\}_{j=1}^G)}$$

三个阶段逐步增加最大输出长度（典型配置为 2K → 4K → 8K，或 4K → 8K → 16K），使模型在低token预算下先学会高效推理，再渐进扩展思考能力。阶段边界的选择依赖启发式指标：当截断比例（clip ratio）和验证集性能（如MATH500准确率）出现拐点时进行切换（Figure 8）。

### 可选的标准RLVR阶段（TFPI+RL）

在TFPI三阶段完成后，可附加一个标准RLVR阶段，此时恢复使用原始思维模板（Template 1），允许模型生成完整思考链。该阶段与TFPI的总计算量之和被控制为与直接RLVR（Direct RL）相等，确保公平对比。实验表明，TFPI+RL在相同计算预算下显著优于Direct RL（Qwen3-4B总体65.7% vs 62.0%，Table 2）。

### 输入输出流总结

| 阶段 | 输入查询格式 | 训练目标 | 输出模型能力 |
|------|-------------|---------|-------------|
| TFPI Stage 1–3 | ThinkingFree变换后的 $x'$（Template 2） | 修改后的DAPO目标 | 高效推理能力，支持ThinkingFree和Thinking两种推理模式 |
| 可选RLVR | 原始思维查询 $x$（Template 1） | 标准DAPO目标 | 进一步提升慢思维性能上限 |

整个框架的关键设计在于：**TFPI作为RLVR的前置初始化阶段，以极低的计算成本（三阶段总计不到标准32K RL训练的20%，Figure 1 Left）为后续RL收敛提供了更优的起点**，同时自身即可产出token效率极高的推理模型。

## 核心模块与公式推导

### 3.1 ThinkingFree 查询转换模块

TFPI 的核心操作是 **ThinkingFree 查询转换**。给定原始输入查询 $x$，该模块将其映射为 $x' = \text{ThinkingFree}(x)$，具体方式是在对话模板的助手前缀后直接附加 `<think>\n\n</think>` 标记，显式禁止模型生成显式思考链。

**因果机制**：这一转换的瓶颈效应体现在两个层面。其一，它直接切断了模型在推理时生成冗长思考内容的能力，使输出 token 量减少 **70% 以上**（Figure 2 Left，在 DS-1.5B 和 Qwen3-4B 上均成立）。其二，它创造了一个“短上下文强化学习”的可行条件——在标准 RLVR 下将训练响应长度压缩至 4K 会导致 avg@32 下降超过 40%，但 ThinkingFree 模式下的 RL 训练不仅不会崩溃，反而能在 AIME25 上提升约 2% 准确率并减少约 20% 输出 token（Figure 2 Right）。这表明 ThinkingFree 并非简单地截断思考，而是迫使模型在有限 token 预算内学习更紧凑的推理模式。

### 3.2 TFPI 训练目标

TFPI 的训练阶段直接复用 DAPO 算法的目标函数，但将原始查询 $x$ 替换为 ThinkingFree 转换后的 $x'$。标准 DAPO 的期望目标为：

$$\mathcal{J}_{\mathrm{DAPO}}(\theta) \doteq \mathbb{\tilde{E}}_{x \sim \mathcal{D}} \left[ \mathcal{J}_{\mathrm{DAPO}}(\theta, x) \right]$$

其中每查询损失 $\mathcal{J}_{\mathrm{DAPO}}(\theta, x)$ 包含重要性比率裁剪和组内相对优势计算。TFPI 对此的**唯一修改**发生在重要性比率和优势函数的计算中，将条件变量从 $x$ 替换为 $x'$：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(y_{i,t} \mid x', y_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(y_{i,t} \mid x', y_{i,<t})}, \quad \widehat{A}_{i,t} = \widehat{A}_i = \frac{r(x', y_i) - \operatorname{mean}(\{r(x', y_j)\}_{j=1}^G)}{\operatorname{std}(\{r(x', y_j)\}_{j=1}^G)}$$

**变量含义**：
- $r_{i,t}(\theta)$：token 级别的重要性比率，衡量当前策略 $\pi_\theta$ 与旧策略 $\pi_{\theta_{\mathrm{old}}}$ 在 ThinkingFree 上下文 $x'$ 下生成第 $i$ 条响应的第 $t$ 个 token 的概率比。
- $\widehat{A}_{i,t}$：组归一化优势函数，对同一查询 $x'$ 下的 $G$ 条采样响应进行均值-标准差归一化，$r(x', y_i)$ 为可验证奖励（如数学答案正确性）。
- $x' = \text{ThinkingFree}(x)$：经转换的查询，其核心特征是助手前缀后紧跟 `</think>`，模型只能在此之后直接生成答案部分。

**关键设计选择**：TFPI 未引入任何额外的奖励塑形项或长度惩罚。其 token 效率的提升完全来自 ThinkingFree 查询格式对策略搜索空间的约束——模型被迫在“无思考”条件下学习，却意外地提升了“有思考”模式下的推理质量上限。

### 3.3 多阶段 TFPI 训练流程

TFPI 采用渐进式多阶段训练策略，逐步放宽最大输出长度限制：

1. **阶段 1（2K → 4K）**：在极短上下文下启动训练，利用 ThinkingFree 的低 token 特性使模型快速获得基础推理能力。此阶段验证步骤比例急剧下降（Figure 3），表明模型从初始的随机探索转向结构化推理。
2. **阶段 2（4K → 8K）**：扩展长度上限，验证步骤比例稳步回升，模型开始学习更复杂的推理模式。
3. **阶段 3（8K → 16K）**：进一步扩展，验证步骤比例急剧上升，标志着深度推理能力的涌现。

阶段边界的划分依赖启发式规则：截断比例（clip ratio）和 MATH500 验证准确率的转折点（Figure 8）。消融实验证实，4K→8K→16K 的三阶段计划在 Qwen3-4B 上取得 63.8% 的总体准确率，优于 8K→16K（62.4%）和 16K 单阶段（61.9%）方案（Table 4），验证了渐进式长度增长的必要性。

**与直接 RL 的关键区别**：若将相同的多阶段长度计划应用于标准 RLVR（即无 ThinkingFree 转换），Qwen3-4B 的总体准确率会从 63.8% 骤降至 52.9%（Table 4），降幅超过 10 个百分点。这说明 TFPI 并非简单的“短上下文训练技巧”，而是通过 ThinkingFree 查询格式从根本上改变了 RLVR 训练的优化景观，使短上下文下的策略更新与长上下文推理能力之间建立了正向迁移通道。

## 实验与分析

### 核心发现：TFPI在等计算预算下全面优于直接RL

TFPI的核心优势在严格控制的对比实验中得到了系统性验证。所有实验均确保TFPI三阶段的总训练计算量与直接RL（Direct RL）完全匹配，排除了计算预算差异带来的混淆。表1汇总了在三个模型规模（DS-1.5B、Qwen3-4B、DS-7B）和六个基准上的主结果。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/005_Table_1.jpg]]
*Table 1: Results of TFPI vs. direct RL across different benchmarks. “Avg@k” denotes the average accuracy (%) over k random generations (i.e., pass@1). All models are evaluated in thinking mode. The total training compute for the 3 stages of TFPI equals that of “Direct RL” for fair comparison. Darker colors in the cell background denote better results within each model group*

在Qwen3-4B上，TFPI Stage 3的总体平均准确率达到63.8%，而Direct RL仅为60.2%，提升幅度为+3.6个百分点。这一优势在DS-7B上更为显著（47.8% vs 43.0%，+4.8%），表明TFPI的收益随模型规模扩大而增强。值得注意的是，TFPI的增益并非仅来自训练后期——即便在Stage 1（仅使用2K响应长度），DS-1.5B的总体准确率已从初始模型的22.0%跃升至26.7%（+4.7%），证明短上下文下的ThinkingFree训练已能有效提升慢思维能力。

跨领域迁移是TFPI的另一关键特性。尽管TFPI仅在数学推理数据（Polaris-53K）上训练，其在GPQA Diamond（科学推理）、LiveCodeBench（代码）和IFEval（指令遵循）上均展现出显著提升。以DS-1.5B为例，GPQA准确率从16.3%提升至29.6%（+13.3%），IFEval从36.6%提升至40.8%（+4.2%）。这表明ThinkingFree操作所强化的推理模式具有领域通用性。

### TFPI作为RLVR前置阶段的增效作用

表2展示了将TFPI作为标准RLVR前置阶段（TFPI+RL）的效果。在Qwen3-4B上，TFPI+RL的总体准确率达到65.7%，对比Direct RL的62.0%有+3.7%的提升。在AIME 25上，TFPI+RL达到76.0%，Direct RL为71.5%（+4.5%）。这一结果说明，TFPI不仅本身是一个强基线，更能为标准长链思维RL提供更优的参数初始化，加速收敛并提升性能上限。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/006_Table_2.jpg]]
*Table 2: Results (%) of RL after TFPI (“TFPI+RL”) vs. “Direct RL” across different benchmarks. “Avg@k” denotes the average accuracy (%) over k random generations (i.e., pass@1). For LRMs marked with “*”, results are taken from the corresponding reports (see Appendix C.4); results of 4B models are from our own runs with 48K response length. All models are evaluated in thinking mode. The total training compute for “TFPI+RL” is matched to that of “Direct RL” for fair comparison. Darker colors in the cell background denote better results*

从计算效率角度看，图1（左）清晰展示了这一优势：TFPI三阶段的总计算成本不到标准32K上下文RL训练的20%，但TFPI+RL的最终性能却超越了直接使用全部计算预算进行RL训练的模型。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/002_Figure_1.jpg]]
*Figure 1: Our proposed TFPI accelerates the convergence of RLVR to a higher performance ceiling (left) and yields more token-efficient reasoning models (right). Left: avg@32 versus training compute, measured in H20 hours. “Direct RL” refers to directly training Qwen3-4B with a 32K context window using DAPO, while $\mathrm { ^ { 6 6 } T F P I } + \mathrm { R L } ^ { \prime }$ denotes running 32K-context DAPO after initialization with our 3-stage TFPI. The x-axis for TFPI uses a linear scale during the TFPI phase, followed by a logarithmic scale, with the transition indicated by a black vertical line. Right: Average accuracy on 4 reasoning datasets (AIME24/25, Beyond AIME, and GPQA) versus average output...

### Token效率：用更少的token获得更强的推理能力

TFPI最引人注目的特性之一是它自然地产出token效率极高的推理模型。图1（右）的散点图展示了准确率与平均输出token的关系——TFPI各阶段始终位于Pareto前沿，表明其在性能-效率权衡上达到了最优。

具体数据见表3。在Thinking-Free推理模式下，DS-1.5B经TFPI Stage 3训练后，在AIME24上达到37.5%的准确率，而平均输出token仅5.3K。作为对比，原始DS-1.5B在标准思维模式下需要16.7K token才能达到29.6%的准确率——TFPI以不到三分之一的token消耗实现了近8个百分点的准确率提升。与专门设计的token效率基线（如TLMRE、AdaptThink、L1Max等）相比，TFPI同样展现出更优的综合表现。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/007_Table_3.jpg]]
*Table 3: Comparison of the Thinking-Free inference mode of TFPI with efficient reasoning baselines across various reasoning tasks. “Avg@k” denotes the average accuracy (in %) over k generations (i.e., pass@1), and “Toks” indicates the average output length in thousands of tokens (K). Models with “*” are trained from DeepScaleR-1.5B, while the remaining are from DS-1.5B. Darker cell background colors indicate better results*

### 多阶段训练的必要性：消融实验

表4的消融实验揭示了TFPI设计中的关键因果机制。首先，**阶段长度计划**的选择至关重要：4K→8K→16K的三阶段计划在Qwen3-4B上达到63.8%的总体准确率，优于8K→16K的两阶段计划（62.4%）和16K单阶段计划（61.9%）。这验证了渐进式增加上下文长度的必要性——过早使用长上下文会浪费计算，而过晚则限制性能提升空间。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/014_Table_4.jpg]]
*Table 4: Additional results of TFPI. All models are evaluated in thinking mode*

更关键的消融是**多阶段直接RL（无ThinkingFree）**的对比。当直接使用标准RLVR进行4K→8K→16K的多阶段训练时，Qwen3-4B的总体准确率骤降至52.9%，比TFPI低近11个百分点，甚至远低于单阶段32K Direct RL的60.2%。这一结果揭示了TFPI的核心价值：**ThinkingFree操作是使短上下文多阶段训练可行的必要条件**。图2（右）的元实验为此提供了机制解释：标准RLVR在4K响应长度下会导致avg@32下降超过40%，而ThinkingFree RL在相同约束下反而能提升约2%的准确率并减少约20%的token消耗。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_RKYO6R8Jgb/figures/004_Figure_2.jpg]]
*Figure 2: Results of the meta-experiment on the ThinkingFree operation. Left: Average output tokens in thinking mode and ThinkingFree mode on AIME25. Right: Evolution of avg@32 and average output tokens on AIME24 with thinking-mode evaluation over training steps under 4K training response length (both training in thinking mode and ThinkingFree mode)*

### 行为级与参数级分析

图3从行为层面追踪了DS-1.5B在TFPI三阶段训练中的动态变化。在训练集的ThinkingFree模式下，验证步骤比例在Stage 1经历快速下降后趋于稳定，在Stage 2稳步增长，在Stage 3急剧上升。与此同时，AIME25思维模式评估下的输出token在Stage 1快速下降，随后在Stage 2和Stage 3保持相对稳定。这一模式表明：**Stage 1主要负责压缩冗余思考，而Stage 2和Stage 3则在压缩后的基础上重建并增强推理深度**。

图4的参数级分析提供了收敛性证据。PCA投影显示，TFPI从初始模型（点A）出发，依次经过B1、B2、B3，最终收敛至Direct RL最终检查点（点C）附近。余弦相似度分析进一步表明，TFPI各阶段产生的参数更新与Direct RL的最终更新方向高度一致，说明TFPI并未将模型引向完全不同的参数子空间，而是以更高效的方式实现了相似的收敛目标。

### 训练稳定性与超参数鲁棒性

附录中的消融实验（图7）表明，TFPI对训练温度不敏感——温度1.4与1.0在TFPI Stage 1和Direct RL上均产生相当的性能，结果具有鲁棒性。此外，图8展示了Stage 1的截断比例变化：在约100步时，截断比例和输出token出现转折点，MATH500验证准确率同步趋于稳定，这为阶段切换的启发式规则提供了经验依据。

### 局限性与失败模式

尽管TFPI效果显著，仍需注意以下几点限制。第一，ThinkingFree推理模式在准确率上略低于慢思维模式（如Stage 3总体63.9% vs 60.0%），本质上是**用轻微准确率换取大幅token效率**的策略，在精度敏感场景下需谨慎使用。第二，多阶段训练的阶段边界划分仍依赖启发式规则（截断比例和验证性能），缺乏自动化机制，可能在不同模型或数据分布上需要重新调参。第三，当前验证集中在1.5B至7B规模，更大模型（如14B以上）的扩展性虽在表4中有初步验证（Qwen3-14B上TFPI达到67.8% vs Direct RL 66.9%），但潜力尚未充分探索。

## 方法谱系与知识库定位

### 1. 核心方法定位

TFPI 的核心创新在于**将训练阶段的查询格式变换（ThinkingFree）作为强化学习初始化的低成本预训练阶段**，而非设计新的奖励函数、长度惩罚或训练算法。其技术本质是：在标准 DAPO RLVR 训练之前，对输入查询执行 `ThinkingFree(x)` 操作——在助手前缀后直接附加 `## 方法谱系与知识库定位

### 1. 核心方法定位

TFPI 的核心创新在于**将训练阶段的查询格式变换（ThinkingFree）作为强化学习初始化的低成本预训练阶段**，而非设计新的奖励函数、长度惩罚或训练算法。其技术本质是：在标准 DAPO RLVR 训练之前，对输入查询执行 `ThinkingFree(x)` 操作——在助手前缀后直接附加 `<think>\n\n</think>` 标记，显式禁止模型生成显式思考链。这一操作将重要性比率和优势函数中的查询 $x$ 替换为 $x'$（公式 3），从而大幅降低 rollout 时的 token 生成量（减少 70% 以上，Figure 2 Left），使短上下文（如 4K）下的 RL 训练成为可能。

TFPI 与现有工作的关系可从三个维度定位：

**（1）与 RLVR 训练框架的关系：作为前置初始化阶段**

TFPI 直接建立在 DAPO（Yu et al., 2025）的基础上，使用相同的组归一化优势函数和裁剪损失（公式 1-2），但将查询格式从标准思维模板（Template 1）切换为 ThinkingFree 模板（Template 2）。它不替代 DAPO，而是作为其**低成本前置阶段**：TFPI 三个阶段的总计算量不足标准 32K 上下文 RL 训练的 20%（Figure 1 Left），却能显著加速后续 RL 的收敛并提升性能上限。在 TFPI 之后附加标准 RLVR（TFPI+RL）可进一步获得性能增益（Qwen3-4B 总体 65.7% vs Direct RL 62.0%，Table 2）。

**（2）与多阶段 RLVR 训练的关系：短上下文多阶段的关键使能技术**

多阶段 RLVR 训练（如 **Polaris**, An et al., 2025）通常通过逐步增加训练上下文长度来提升性能。然而，直接对 SFT 蒸馏模型应用短上下文多阶段 RL 会导致性能崩溃：消融实验表明，Qwen3-4B 在 4K→8K→16K 的直接多阶段 RL 下总体准确率仅 52.9%，远低于 TFPI 的 63.8%（Table 4）。TFPI 通过 ThinkingFree 操作使模型在短上下文下仍能有效学习，是多阶段短上下文训练得以成功的关键使能条件。

**（3）与 token 效率推理方法的关系：无需显式长度控制的替代路径**

现有 token 效率推理方法通常依赖显式机制控制生成长度：
- **TLMRE**（Arora & Zanette, 2025）：基于 RL 的 token 效率推理
- **AdaptThink**（Zhang et al., 2025b）：动态思考控制
- **L1Max**（Aggarwal & Welleck, 2025）：L1 正则化控制生成长度
- **DeepScaleR**（Luo et al., 2025b）：迭代训练与长度控制

TFPI 采取根本不同的路径：它不引入任何长度惩罚或显式控制信号，而是通过 ThinkingFree 查询格式变换**自然诱导**模型学习更紧凑的推理模式。在 token 效率-准确率 Pareto 前沿上，TFPI 各阶段持续位于前沿位置（Figure 1 Right），且其 ThinkingFree 推理模式在 DS-1.5B 上以 5.3K tokens 获得 AIME24 37.5% 准确率，远超原始思维模式下 16.7K tokens 的 29.6%（Table 3）。

### 2. 适用边界

**已验证的适用范围：**
- **模型规模**：1.5B 至 14B 参数（DS-1.5B、Qwen3-4B、DS-7B、Qwen3-14B），在 14B 上仍保持优势（TFPI 总体 67.8% vs Direct RL 66.9%，Table 4）
- **训练数据**：数学推理数据集 Polaris-53K，包含约 53K 数学问题
- **RL 算法**：DAPO，但方法本身对 RLVR 算法不敏感（论文指出 RLVR 启发式可直接应用于 TFPI）
- **推理模式**：同时提升标准思维模式和 ThinkingFree 模式下的性能

**已知的边界条件：**
- **跨领域迁移存在波动**：虽在 GPQA（科学推理）和 IFEval（指令遵循）上观察到迁移提升（DS-1.5B GPQA 16.3%→29.6%，IFEval 36.6%→40.8%，Table 1），但 LiveCodeBench 提升有限（17.7%→19.9%），表明纯数学训练数据的跨领域泛化存在领域依赖性
- **ThinkingFree 推理模式存在准确率折损**：以轻微准确率下降换取显著 token 效率提升（如 Stage 3 总体思维模式 63.9% vs ThinkingFree 模式 60.0%），是一种效率-准确率权衡策略
- **阶段长度选择依赖启发式**：阶段边界通过截断比例和验证性能的转折点（Figure 8）人工确定，缺乏自动化机制

### 3. 局限与开放问题

**已识别的局限：**

1. **训练数据领域单一**：TFPI 仅在数学推理数据上训练，跨领域迁移虽有正向信号但幅度不均。论文明确指出"纳入更多样化的多领域训练数据可能对 TFPI 有益"。

2. **模型规模验证有限**：最大验证模型为 14B，向更大规模（>30B）的扩展性未知。论文提出开放问题："在更大规模模型上，TFPI 的可扩展性如何？是否存在新的瓶颈？"

3. **阶段调度依赖人工启发式**：阶段长度计划（如 4K→8K→16K）通过截断比例和 MATH500 验证准确率的转折点确定（Figure 8），缺乏自适应切换机制。

4. **ThinkingFree 操作的适用范围未充分探索**：当前仅验证了在 RLVR 训练前和推理时的应用，其在离线推理、测试时计算缩放等其他场景的潜力尚未探索。

**开放问题：**

- **数据课程设计**：如何设计数据课程或引入多领域数据来进一步提升 TFPI 的跨领域泛化能力？
- **大规模扩展性**：TFPI 在更大规模模型（>10B）上的可扩展性如何？是否存在新的瓶颈？
- **操作泛化**：ThinkingFree 操作是否可以推广到其他 RLVR 算法之外的应用，例如离线推理或测试时计算缩放？
- **自适应阶段切换**：能否通过自适应阶段切换机制进一步优化 TFPI 训练效率？
- **高质量数据的影响**：论文提出"使用更具挑战性、更高质量的数据，TFPI 能否进一步释放其在更大模型上的可扩展潜力？"

## 原文 PDF

![[paperPDFs/ICLR_2026/Thinking_Free_Policy_Initialization_Makes_Distilled_Reasoning_Models_More_Effective_and_Efficient_Reasoners.pdf]]
