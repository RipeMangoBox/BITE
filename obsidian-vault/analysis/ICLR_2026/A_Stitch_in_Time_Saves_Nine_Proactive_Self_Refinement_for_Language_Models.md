---
title: "A Stitch in Time Saves Nine: Proactive Self-Refinement for Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Stitch_in_Time_Saves_Nine_Proactive_Self_Refinement_for_Language_Models.pdf
project_link: null
code_link: https://github.com/JinyiHan99/Proactive-Self-Refine-in-LLMs/
aliases:
- PSRP
- STSNPSRLM
- "ProActive Self-Refinement (PASR)"
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "强化学习训练策略，特别是基于比较的细粒度奖励函数，该函数鼓励及时、必要且上下文适当的优化行为。"
primary_logic: "通过在生成过程中引入结构化的<refine>标签，并利用GRPO算法和比较式奖励信号，模型可以学会在推理轨迹中自主触发优化，从而在不显著增加token消耗的情况下提升准确率。"
claims:
- "PASR在Qwen3-8B上平均token消耗降低41.6%，准确率提升8.2%。"
- "PASR在Qwen2.5-7B和Qwen3-8B上分别取得平均+4.8和+8.2的性能提升。"
- "在267个初始错误答案中，PASR修正了235个。"
- "GSM8K 上 Accuracy = 88.8"
---

# A Stitch in Time Saves Nine: Proactive Self-Refinement for Language Models

> [!tip] 核心洞察
> 通过在生成过程中引入结构化的<refine>标签，并利用GRPO算法和比较式奖励信号，模型可以学会在推理轨迹中自主触发优化，从而在不显著增加token消耗的情况下提升准确率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 未雨绸缪：语言模型的主动自我优化 |
| 英文题名 | A Stitch in Time Saves Nine: Proactive Self-Refinement for Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0GaCfBRFnf) · [GitHub](https://github.com/JinyiHan99/Proactive-Self-Refine-in-LLMs/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ProActive Self-Refinement (PASR) |
| Dataset | GSM8K, MATH, AIME24, ARC |

> [!tip] 效果简介
> - GSM8K 上，Accuracy 为 88.8，对比 88.8 (Vanilla Qwen2.5-7B)，变化 0.0。
> - MATH 上，Accuracy 为 73.6，对比 68.4 (Vanilla Qwen2.5-7B)，变化 +5.2。
> - AIME24 上，Accuracy 为 10.0，对比 6.7 (Vanilla Qwen2.5-7B)，变化 +3.3。

## 概要

本文针对现有语言模型自我优化方法普遍采用的“事后修复”范式——即先生成完整答案，再在固定迭代次数内依赖外部反馈进行修正——提出了核心问题：该范式无法在生成过程中自主判断是否、何时以及如何进行优化，导致错误传播、迭代僵化且额外开销高。

为突破这一瓶颈，论文提出**ProActive Self-Refinement (PASR)**，一种基于强化学习的主动自我优化方法。其核心洞察在于：通过在生成轨迹中引入结构化的`<refine>`标签，并利用**组相对策略优化（GRPO）** 算法配合**比较式细粒度奖励函数**，模型能够学会在推理过程中自主触发优化。该奖励函数由三部分组成：格式奖励（强制输出结构）、准确率奖励（基于LLM裁判的语义评分）和优化奖励（通过将优化后响应的准确率与组内标准响应的平均准确率比较，分别给予有效优化+1、有害优化-1、不必要优化-0.5的奖惩）。这一设计从根本上改变了优化行为的触发机制与时机决策。

实验验证了PASR的有效性。在Qwen2.5-7B和Qwen3-8B上，PASR分别取得平均+4.8和+8.2的性能提升，其中在MMLU上相对基线提升29.0个百分点，在Xsum上提升18.3个百分点。效率方面，PASR在Qwen3-8B上相比标准生成平均降低41.6%的token消耗，同时准确率提升8.2%；在Qwen2.5-7B上仅增加8.4%的token消耗便获得4.8个绝对性能提升。消融实验表明，基于比较的细粒度优化奖励优于简单二元奖励，且强化学习训练（PASR†）显著优于仅通过提示或指令微调的方式。在行为分析中，PASR在267个初始错误答案中成功修正了235个，表明其优化行为具有高度选择性而非无差别触发。



大语言模型（LLM）在复杂推理任务中常出现错误，且错误会在生成过程中累积传播。现有自我优化方法（如Self-Refine、STaR、SCoRe等）普遍采用**事后修复**范式：模型先生成完整答案，再通过外部反馈（工具、辅助模型或固定提示）进行多轮迭代修正。这种范式的根本瓶颈在于：模型无法在生成过程中自主判断是否、何时以及如何进行优化，导致（1）错误在生成阶段持续传播；（2）迭代次数固定，无法根据问题难度动态调整；（3）严重依赖外部反馈信号，限制了模型的自主性。

本文的动机是解决上述“事后修复”范式的结构性缺陷。核心洞察在于：如果将优化行为内嵌于生成过程，并通过强化学习让模型学会自主触发优化，就能在不显著增加计算开销的前提下提升准确率。具体而言，作者提出**ProActive Self-Refinement (PASR)**方法，其关键改变在于三个设计槽位：

1. **优化时机**：从固定迭代次数的事后优化，转变为生成过程中基于模型内部状态和上下文动态决定（即模型自主选择何时插入`<refine>`标签）。
2. **触发方式**：从依赖外部反馈（工具、辅助模型或固定提示），转变为通过强化学习策略自主触发，优化行为以`<refine>`标签形式内嵌于推理轨迹。
3. **奖励信号**：从简单的二元正确性奖励，转变为三部分组合奖励——格式奖励、准确率奖励和基于比较的优化奖励。其中优化奖励是关键因果旋钮：通过将优化后响应的准确率与组内多个标准响应的平均准确率比较，鼓励有效优化（+1）、惩罚有害优化（-1）、抑制不必要的无意义优化（-0.5）。

该设计的因果逻辑是：只有当模型学会在“需要优化”的时机触发优化，且优化确实提升了答案质量时，才能获得正向奖励；不必要的优化或有害优化都会受到惩罚。这种细粒度奖励信号迫使模型发展出对自身生成状态的元认知能力。



## 核心方法与创新机理

PASR 的核心创新在于将语言模型的自我优化从“事后修复”范式转变为“生成中主动触发”范式。现有方法（如 Self-Refine, SCoRe, PTR）均采用固定迭代次数的事后优化，依赖外部反馈或辅助模型，且无法在生成过程中自主决定优化的时机与必要性。PASR 通过强化学习训练，使模型学会在推理轨迹中动态插入 `<refine>` 标签，从而在不显著增加 token 消耗的前提下提升准确率。

**关键改变的三处 slots：**

1. **优化时机**：从“固定迭代次数的事后优化”变为“基于模型内部状态与上下文动态决定”。PASR 利用 on-policy rollout 探索是否、何时以及如何进行优化，而非在生成完整答案后再进行多轮修正。
2. **优化触发方式**：从“依赖外部反馈（工具、辅助模型）或固定提示”变为“通过强化学习自主触发，使用 `<refine>` 标签内嵌于推理轨迹”。模型在 `<think>` 与 `<answer>` 标签之间自主插入优化步骤，使优化行为成为生成过程的一部分。
3. **奖励信号**：从“二元正确性奖励或简单规则”变为“三部分求和奖励”。总奖励 `R_y' = r_format(y') + r_acc(y') + r_refine(y')` 中，最关键的创新在于**比较式优化奖励** `r_refine(y')`：它将优化后响应的准确率与组内多个标准响应的平均准确率进行比较——有效优化（准确率显著提升）奖励 +1，有害优化（准确率显著下降）惩罚 -1，不必要优化（准确率无显著变化）惩罚 -0.5。这一设计直接抑制了模型“为优化而优化”的倾向，引导其学会选择性触发优化。

**因果机制与证据强度：**

核心因果链为：比较式奖励信号 → GRPO 训练 → 模型学会在推理轨迹中自主触发 `<refine>` → 在不显著增加 token 消耗的前提下提升准确率。关键证据包括：在 Qwen3-8B 上平均 token 消耗降低 41.6% 的同时准确率提升 8.2%（置信度 1.0）；在 Qwen2.5-7B 上仅增加 8.4% 的 token 消耗便获得 4.8 个绝对性能提升（置信度 0.95）；在 267 个初始错误答案中修正了 235 个（置信度 0.9）。消融实验进一步证实：基于比较的细粒度优化奖励优于简单的二元奖励（置信度 0.95），且强化学习训练（PASR†）显著优于仅通过提示（PASR(+prompt)，平均 40.2 vs 61.7）或指令微调（PASR(+IFT)，平均 57.0 vs 61.7）的方式（置信度 1.0）。

**失败模式与开放问题：**

该方法在 Wino 基准上出现 -7.7 的性能下降，表明在需要常识推理的任务上，主动优化可能引入错误。此外，优化奖励中的容忍参数 ζ 需手动设定，其敏感性未充分分析；训练数据仅来自通用指令跟随数据集（约 40k 对），在特定领域任务上的泛化能力未充分验证。LLM 裁判评估本身可能引入裁判模型的偏差，这一环节的可靠性需要手动验证。



![[assets/figures/papers/iclr26_0004_0GaCfBRFnf_A_Stitch_in_Time_Saves_Nine_Proactive_Self-Refin/figures/001_Figure_1.jpg]]
*Figure 1: Comparison between the post-hoc refinement method (middle) and our proposed PASR (right). The post-hoc refinement method iteratively refines its initial answer. In contrast, PASR proactively refines its reasoning process during the generation*

PASR（主动自我优化）的核心创新在于将优化行为从生成后的固定迭代修复，转变为生成过程中由模型自主触发的自适应过程。其整体 pipeline 围绕一个核心洞察构建：模型不应在输出完整答案后再回头修改，而应在推理轨迹中动态决定是否需要、何时以及如何进行优化。

**模块关系与输入输出流**

PASR 的 pipeline 由四个紧密耦合的模块构成：

1.  **结构化输出格式**：模型被要求使用 `<think>`、`<refine>` 和 `<answer>` 三种专用标签组织输出。`<think>` 标签封装初始推理过程，`<refine>` 标签标记优化行为及其内容，`<answer>` 标签输出最终答案。这种结构化格式使得优化行为在 token 序列中可被明确识别和奖励，是后续强化学习训练的基础。

2.  **GRPO 训练算法**：采用组相对策略优化（GRPO）作为核心训练算法。对于每个输入问题，模型通过 on-policy rollout 生成一组响应（通常为 G 个），每个响应都包含上述结构化格式。GRPO 通过组内优势归一化（对组内每个响应的奖励进行归一化得到优势值）来稳定训练，平衡奖励最大化与策略稳定性（KL 散度惩罚系数 β=0.04，裁剪参数 ϵ=0.2）。

3.  **三部分奖励函数**：这是整个 pipeline 的因果旋钮。总奖励由三部分求和得到：
   - **格式奖励**（二元）：当且仅当所有格式约束（标签使用正确、结构完整）满足时奖励为 1，否则为 -1。
   - **准确率奖励**（连续）：使用高级 LLM 作为裁判，评估生成答案相对于参考答案的语义质量，输出 [0,1] 连续分数。
   - **优化奖励**（离散）：这是关键创新——通过将优化后响应的准确率与组内多个标准响应的平均准确率进行比较，奖励有效优化（+1）、惩罚有害优化（-1）、抑制不必要优化（-0.5）。容忍参数 ζ 控制比较的松弛程度。

4.  **LLM 裁判评估**：用于开放域问题的语义质量评分，替代简单的答案匹配。裁判模型本身可能引入偏差，但提供了比二元正确性奖励更细粒度的信号。

**数据流**：输入问题 → 模型生成结构化响应（包含 `<think>`、可选的 `<refine>`、`<answer>`）→ 三部分奖励计算 → GRPO 更新策略。训练数据来自 alpaca_evol_instruct_70k（经清洗约 40k 对），涵盖通用指令跟随任务。

**与传统方法的根本差异**：传统事后优化方法（如 Self-Refine+、SCoRe 等）在生成完整答案后，依赖外部反馈或固定提示进行固定次数的迭代修复。PASR 则将优化决策内化到生成过程中，模型自主决定是否触发 `<refine>` 标签，何时触发，以及如何修改之前的推理。这种设计使得 PASR 在 Qwen2.5-7B 上仅增加 8.4% 的 token 消耗便获得 4.8 个绝对性能提升，在 Qwen3-8B 上平均 token 消耗降低 41.6% 的同时准确率提升 8.2%。

**需要手动验证的点**：优化奖励中的容忍参数 ζ 的敏感性未充分分析；训练数据来自单一通用指令跟随数据集，在特定领域任务上的泛化能力未充分验证。



PASR 的核心创新在于将自我优化从“事后修复”范式转变为“生成过程中主动触发”范式。其技术栈围绕三个关键模块构建：结构化输出格式、基于 GRPO 的强化学习训练框架，以及一个由三部分组成的细粒度奖励函数。

**结构化输出格式**是模型学习自主优化的基础。系统提示强制模型使用三个专用标签组织输出：`<think>`、`<refine>` 和 `<answer>`。`<refine>` 标签作为优化行为的明确标记，使得模型可以在推理轨迹中插入优化步骤，也让后续的奖励计算能够精准定位并评估每次优化操作。这种格式化的输出是奖励信号能够分解并作用于不同行为的前提。

**GRPO 训练算法**是驱动模型学习优化策略的核心引擎。PASR 使用 Group Relative Policy Optimization 来稳定训练过程，其核心机制包括：
1.  **组内采样与奖励计算**：对于每个输入 $x$，模型生成 $G$ 个候选响应 $y'_i$，每个响应都包含可能的 `<refine>` 优化步骤。对每个响应计算总奖励 $R_{y'_i}$。
2.  **优势归一化**：计算组内奖励的均值 $\mu_x$ 和标准差 $\sigma_x$，将每个响应的奖励归一化为优势值：
    
$$
A_i(y'_i|x) = \frac{R_{y'_i} - \mu_x}{\sigma_x + \xi}
$$

    其中 $\xi$ 是防止除零的小常数。这一归一化操作是 GRPO 的关键：它让模型关注于“相对于组内其他响应，我的这个响应有多好”，而不是绝对奖励值，从而稳定训练并减少对奖励函数绝对尺度的依赖。
3.  **策略更新**：GRPO 的目标函数在最大化优势奖励的同时，通过 KL 散度惩罚约束策略更新的幅度，防止模型在单次更新中偏离参考策略过远：
    
$$
J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_G \left[ \frac{1}{G} \sum_{i=1}^G A_i(y'_i|x) \cdot \min\left(r_i, \mathrm{clip}(r_i, 1-\epsilon, 1+\epsilon)\right) - \beta D_{\mathrm{KL}}(\pi_\theta(\cdot|x) || \pi_{\mathrm{ref}}(\cdot|x)) \right]
$$

    其中 $r_i = \pi_\theta(y'_i|x) / \pi_{\mathrm{ref}}(y'_i|x)$ 是重要性采样比，$\epsilon$ 是裁剪阈值（设为 0.2），$\beta$ 是 KL 惩罚系数（设为 0.04）。这种设计确保模型在探索优化策略时不会产生剧烈的策略震荡。

**比较式细粒度奖励函数**是 PASR 区别于简单二元奖励的核心创新。总奖励由三部分求和得到：

$$
R_{y'} = r_{\text{format}}(y') + r_{\text{acc}}(y') + r_{\text{refine}}(y')
$$

1.  **格式奖励** $r_{\text{format}}(y') = 2(C_1(y') C_2(y') C_3(y')) - 1$：这是一个二元奖励，当且仅当三个格式约束（如 `<think>`、`<refine>`、`<answer>` 标签的正确使用）全部满足时奖励为 1，否则为 -1。这强制模型学习结构化输出格式。
2.  **准确率奖励** $r_{\text{acc}}(y') = \mathcal{I}(x, \hat{y}, y')$：使用一个高级 LLM 作为裁判模型，评估生成答案 $y'$ 相对于参考答案 $\hat{y}$ 的语义质量，输出一个 $[0,1]$ 的连续分数。对于数学等有明确答案的任务，可直接比对最终答案；对于开放域问题，则依赖 LLM 裁判的语义判断。
3.  **优化奖励** $r_{\text{refine}}(y')$：这是 PASR 最关键的信号，用于区分“好的优化”和“坏的优化”：
    
$$
r_{\text{refine}}(y') = \begin{cases}
    1, & r_{\text{acc}}(y') > \bar{r}_{\text{acc}}(y) + \zeta \\
    -1, & r_{\text{acc}}(y') < \bar{r}_{\text{acc}}(y) - \zeta \\
    -0.5, & |r_{\text{acc}}(y') - \bar{r}_{\text{acc}}(y)| \leq \zeta
    \end{cases}
$$

    其核心逻辑是：将优化后响应 $y'$ 的准确率分数与组内所有标准响应（即未包含 `<refine>` 标记的响应）的平均准确率 $\bar{r}_{\text{acc}}(y)$ 进行比较。如果优化后准确率显著高于平均水平（超过容忍参数 $\zeta$），则给予正奖励（+1）；如果显著低于平均水平，则给予负惩罚（-1）；如果与平均水平无显著差异，则给予轻微惩罚（-0.5），以抑制不必要的优化行为。这种比较式设计直接编码了“及时、必要且上下文适当”的优化行为偏好。

**核心机制总结**：PASR 通过 GRPO 算法在组内进行 on-policy 探索，让模型自主决定是否插入 `<refine>` 标签以及如何修改推理内容。比较式优化奖励通过将优化后的结果与组内未优化的标准结果进行对比，提供了细粒度的学习信号：鼓励那些能带来实质性改善的优化，惩罚那些导致性能下降的优化，并抑制那些无意义的冗余优化。这种设计使得模型能够在推理过程中动态判断优化的时机和内容，从而在仅增加少量 token 消耗的情况下获得显著的性能提升。



## 实验与关键发现

### 主实验结果

PASR在Qwen2.5-7B和Qwen3-8B两个基座模型上均取得了显著的性能提升。在Qwen2.5-7B上，PASR在10个任务上的平均准确率从基线的55.9提升至61.7，获得了**+5.8**的绝对增益（Table 1）。在Qwen3-8B上，平均准确率从60.9提升至69.1，增益为**+8.2**。这一增益并非均匀分布：在MMLU（+29.0）、Xsum（+18.3）和Drop（+14.1 on Qwen3-8B）等任务上提升极为显著，但在Wino任务上反而出现**-7.7**的下降。这种任务间的差异性暗示PASR的优化行为在常识推理类任务上可能存在过拟合或奖励信号误导。

![[assets/figures/papers/iclr26_0004_0GaCfBRFnf_A_Stitch_in_Time_Saves_Nine_Proactive_Self-Refin/figures/003_Table_1.jpg]]
*Table 1: PASR vs. other baselines. Compared to the base model, PASR achieves an average performance improvement of +4.8 and +8.2 on the two models, respectively*

与现有事后自我优化方法（Self-Refine+, SCoRe, STaR, RISE等）相比，PASR在平均性能上全面领先。在Qwen2.5-7B上，PASR的61.7平均准确率显著高于次优的SCoRe（59.1）和RISE（57.9）。值得注意的是，仅通过提示（PASR(+prompt)）或指令微调（PASR(+IFT)）无法达到强化学习训练的效果——前者仅40.2，后者57.0，说明**强化学习训练策略是PASR效果的核心因果机制**。

### 效率分析

PASR的核心优势在于以极小的token开销换取性能提升。在Qwen2.5-7B上，PASR仅增加**8.4%**的token消耗便获得4.8个绝对性能提升（Figure 3）。相比之下，Self-Refine+的token消耗增加了**44.1%**，RISE增加了**11.8%**，但后两者的性能增益均低于PASR。在Qwen3-8B上，PASR甚至将token消耗降低了**41.6%**，同时准确率提升8.2%。这一反直觉的结果源于PASR的主动优化机制：模型在生成过程中及时修正错误，避免了事后方法中常见的“先产生长错误轨迹再重写”的低效模式。

### 消融实验

**奖励信号设计**是PASR的关键消融维度（Table 2）。比较式细粒度优化奖励（comparison-based fine-grained reward）在所有任务上均优于简单的二元奖励（binary reward）。具体而言，二元奖励在MATH上仅70.1（vs 细粒度73.6），在MMLU上仅72.3（vs 75.0）。细粒度奖励通过引入容忍参数ζ（论文设定为0.1），将优化行为分为三类：有效优化（奖励+1）、有害优化（惩罚-1）和不必要优化（惩罚-0.5）。这种三级惩罚机制有效抑制了模型“为优化而优化”的倾向——在训练初期，模型倾向于频繁触发<refine>标签，但比较式奖励会惩罚那些没有实际提升答案质量的优化行为，从而迫使模型学习何时优化是必要的。

![[assets/figures/papers/iclr26_0004_0GaCfBRFnf_A_Stitch_in_Time_Saves_Nine_Proactive_Self-Refin/figures/006_Table_2.jpg]]
*Table 2: PASR performance across datasets under different refinement reward signals. The comparison-based fine-grained reward better guides the model to learn adaptive and meaningful refinements*

**训练策略消融**进一步验证了强化学习的必要性。PASR(+prompt)仅通过提示模板让模型输出<refine>标签，平均准确率仅40.2，远低于基线的55.9，说明**没有训练信号支撑的结构化输出反而会破坏模型原有的生成能力**。PASR(+IFT)通过指令微调在40k清洗后的alpaca_evol_instruct_70k数据上进行监督学习，平均准确率57.0，略高于基线但远低于PASR†的61.7。这表明监督学习无法有效建模“何时优化”这一决策边界——模型学会了输出<refine>标签，但无法判断优化是否有益。

### 行为分析

PASR的优化行为表现出高度的选择性（Figure 4）。在267个初始错误答案中，PASR修正了**235个**（87.6%），但对正确答案几乎不做修改。这一行为模式与比较式奖励的设计目标一致：当初始答案已经正确时，任何优化尝试都会被惩罚（r_refine = -0.5），从而抑制不必要的修改。语义一致性分数（coherence score）显示，大部分优化（约70%）保持了与初始推理轨迹的连贯性，说明PASR的优化不是粗暴的重写，而是**基于已有推理过程的增量修正**。

对优化类型的进一步分类（Figure 5）揭示，PASR最常触发的优化类型是“错误修正”（Error Correction）和“信息补充”（Information Complement），而“方案改进”（Solution Improvement）和“任务对齐”（Task Alignment）较少。这暗示PASR的优化行为倾向于**修复具体错误而非重构推理策略**——前者更容易通过比较式奖励获得正向信号，后者可能需要更长的优化轨迹和更复杂的奖励设计。

### 扩展性与失败模式

在Qwen2.5-14B上（Table 3），PASR的平均性能提升为**4.9%**（从66.8到71.7），略低于7B模型上的5.8%。这一趋势暗示PASR的有效性可能随模型规模增加而边际递减——更大的模型本身具备更强的自纠正能力，留给PASR的增益空间变小。然而，论文未深入探讨这一现象的因果机制，也未报告不同规模模型上优化行为频率的变化。

![[assets/figures/papers/iclr26_0004_0GaCfBRFnf_A_Stitch_in_Time_Saves_Nine_Proactive_Self-Refin/figures/007_Table_3.jpg]]
*Table 3: PASR vs. other baselines. Compared to the base model, PASR achieves an average performance improvement of 4.9% on Qwen2.5-14B*

PASR的失败模式集中在两个方向：一是**Wino任务上的性能下降**（-7.7），该任务依赖常识推理和世界知识，PASR的优化可能破坏了初始答案中正确的常识假设；二是**AIME24上的有限提升**（+3.3，从6.7到10.0），说明在需要多步复杂推理的任务上，单次优化可能不足以修正累积的错误。论文未分析这些失败案例的优化轨迹，因此无法判断是优化时机选择不当还是优化内容本身错误。

### 重要图表结论

- **Table 1**（主结果表）：PASR在两个模型上均取得平均性能领先，但任务间方差大，Wino等任务上的负收益需要进一步分析。
- **Table 2**（消融表）：比较式细粒度奖励是PASR的核心设计要素，其三级惩罚机制有效抑制了不必要的优化行为。
- **Figure 3**（效率图）：PASR在Qwen3-8B上实现token消耗降低41.6%的同时准确率提升8.2%，验证了主动优化在效率上的优势。
- **Figure 4**（行为图）：PASR对错误答案的修正率高达87.6%，且优化行为与初始推理轨迹保持语义一致性，说明其优化是增量式的而非破坏性的。

### 补充图表

![[assets/figures/papers/iclr26_0004_0GaCfBRFnf_A_Stitch_in_Time_Saves_Nine_Proactive_Self-Refin/figures/008_Table_4.jpg]]
*Table 4: Important parameters for each baseline method*



## 定位与知识库关联

PASR（ProActive Self-Refinement）在自我优化方法谱系中占据了一个独特的位置：它从“事后修复”范式转向了“生成过程中主动优化”范式。这一转变的核心在于将优化时机从一个固定的后处理步骤，变成一个由模型内部状态和上下文动态决定的生成时行为。

**与基线方法的关系：从固定迭代到自适应决策**

现有自我优化方法（如Self-Refine+, SCoRe, STaR, ISC, RISE等）均采用事后修复范式：模型先生成完整答案，再通过外部反馈（工具、辅助模型）或固定提示进行迭代修正。这种范式的根本瓶颈在于：迭代次数固定、无法在生成过程中自主决定是否需要优化，导致错误传播和token浪费。PASR通过强化学习训练策略，特别是基于比较的细粒度奖励函数，使模型学会在推理轨迹中通过`<refine>`标签自主触发优化。在Qwen2.5-7B上，PASR仅增加8.4%的token消耗便获得4.8个绝对性能提升；在Qwen3-8B上，token消耗反而降低41.6%，同时准确率提升8.2%。这表明主动优化不仅能提升质量，还能通过减少不必要的生成步骤来节省计算资源。

**适用边界：数学推理与开放域任务表现分化**

PASR在不同任务类型上表现出显著分化。在数学推理任务（MATH: +5.2, AIME24: +3.3）和知识密集型任务（MMLU: +29.0, Xsum: +18.3）上提升显著，但在Wino（常识推理）上反而下降7.7个点。这种分化揭示了主动优化的关键瓶颈：当模型缺乏相关知识或元认知能力时，自我优化可能引入错误而非修正错误。在267个初始错误答案中，PASR修正了235个，但仍有32个未能修正，说明优化行为并非始终有益。此外，优化奖励中的容忍参数ζ需要手动设定，其敏感性未充分分析，这限制了方法的即插即用性。

**局限与开放问题**

1. **泛化边界不清晰**：训练数据仅来自alpaca_evol_instruct_70k（约40k对），在特定领域任务上的泛化能力未充分验证。Qwen2.5-14B上的平均提升为4.9%，低于7B模型的4.8%和8B模型的8.2%，说明有效性随模型规模变化，但根本原因未探讨。
2. **评估偏差**：使用LLM裁判评估开放域答案的语义质量，裁判模型本身可能存在偏见。在缺乏明确标准答案的场景下，比较式奖励策略如何调整尚不明确。
3. **开放问题**：如何定义生成过程中优化的最佳时机？模型如何将自适应优化行为泛化到未见过的任务？当模型缺乏相关知识或元认知能力时，自我优化的局限性是什么？这些问题的回答需要更深入的行为分析和跨任务泛化实验。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Stitch_in_Time_Saves_Nine_Proactive_Self_Refinement_for_Language_Models.pdf

![[paperPDFs/ICLR_2026/A_Stitch_in_Time_Saves_Nine_Proactive_Self_Refinement_for_Language_Models.pdf]]
