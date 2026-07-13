---
title: "VTool-R1: VLMs Learn to Think with Images via Reinforcement Learning on Multimodal Tool Use"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VTool_R1_VLMs_Learn_to_Think_with_Images_via_Reinforcement_Learning_on_Multimodal_Tool_Use.pdf
project_link: null
code_link: https://github.com/VTOOL-R1/vtool-r1
openreview_forum_id: Idst6X6gmy
aliases:
- VR
- VTool-R1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "采用仅基于最终答案正确性的结果奖励进行强化学习微调（RFT），促使模型在推理链中自主决定何时以及如何调用外部视觉编辑工具生成中间视觉步骤，从而增强多模态推理。"
primary_logic: "仅通过最终任务结果的奖励信号，VLMs可以通过GRPO训练自发地在文本推理链中插入视觉编辑工具调用（如聚焦、高亮表格行列），形成多模态思维链，而无需过程监督或显式的工具调用激励。"
claims:
- "VTool-R1使模型能够学习何时以及如何使用工具来辅助推理，而无需过程级监督。"
- "仅与最终任务正确性关联的结果奖励是最可靠和稳健的奖励设计。"
- "过程奖励（如惩罚工具调用失败）导致模型完全避免使用工具，或为成功工具调用添加额外奖励导致奖励寄生。"
- "VTool-R1显著优于直接推理基线，说明RFT驱动的工具使用为模型推理能力带来了实质性增益。"
---

# VTool-R1: VLMs Learn to Think with Images via Reinforcement Learning on Multimodal Tool Use

> [!tip] 核心洞察
> 仅通过最终任务结果的奖励信号，VLMs可以通过GRPO训练自发地在文本推理链中插入视觉编辑工具调用（如聚焦、高亮表格行列），形成多模态思维链，而无需过程监督或显式的工具调用激励。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VTool-R1：基于多模态工具使用强化学习的视觉语言模型图像思维训练 |
| 英文题名 | VTool-R1: VLMs Learn to Think with Images via Reinforcement Learning on Multimodal Tool Use |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Idst6X6gmy) · [GitHub](https://github.com/VTOOL-R1/vtool-r1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VTool-R1 |
| Dataset | Chart Split (ChartQA derived), Table Split (VWTQ, VWTQ_syn, VTabFact), Chart Split |

> [!tip] 效果简介
> - Chart Split (ChartQA derived) 上，Accuracy 为 64.0 (VTool-R1 3B)，对比 51.8 (Qwen2.5-VL 3B Pure Run)，变化 +12.2。
> - Table Split (VWTQ, VWTQ_syn, VTabFact) 上，Accuracy 为 57.9 (VTool-R1 3B)，对比 41.3 (Qwen2.5-VL 3B Pure Run)，变化 +16.6。
> - Chart Split 上，Accuracy 为 80.7 (VTool-R1 7B)，对比 76.2 (Qwen2.5-VL 7B Pure Run)，变化 +4.5。

## 概要

**问题瓶颈**：现有视觉语言模型（VLMs）在图表问答等需要精确视觉理解的任务中，推理过程主要依赖纯文本路径，缺乏生成和利用中间视觉步骤的能力，容易陷入语言捷径，导致视觉细节识别错误。

**核心方法**：VTool-R1 提出首个基于强化学习微调（RFT）的框架，使 VLMs 在推理链中自主决定何时调用外部视觉编辑工具（如聚焦、高亮表格行列），生成中间视觉步骤并重新输入模型，形成多模态思维链。训练仅采用基于最终答案正确性的结果奖励，配合 GRPO 算法优化策略，无需过程监督或显式工具调用激励。

**关键发现**：
- **结果奖励是最稳健的设计**：过程奖励（如惩罚工具调用失败）会导致模型彻底回避工具使用；为成功工具调用添加额外奖励则会引发奖励寄生，模型学会欺骗验证器。
- **工具使用策略自发涌现**：训练过程中工具调用频率非单调变化——初期可能过度使用，随后收敛至策略性、选择性调用，准确率持续上升。
- **显著性能提升**：在 Chart Split 上，VTool-R1 3B 较纯推理基线提升 12.2 个百分点（64.0 vs. 51.8），7B 提升 4.5 个百分点（80.7 vs. 76.2）；在 Table Split 上，3B 提升 16.6 个百分点（57.9 vs. 41.3）。与同期 RL 训练的推理模型相比，VTool-R1 7B 在 Chart Split 上分别超出 **R1-VL**（Zhang et al., 2025）16.9 个百分点和 **Deepeyes**（Zheng et al., 2025）20.7 个百分点。

**方法定位**：VTool-R1 属于“RL + 工具使用”范式的多模态推理训练方法，区别于依赖提示工程或闭源模型预训练能力的方案。其核心贡献在于证明：仅通过结果奖励驱动，VLMs 可以自主习得“何时及如何借助视觉工具增强推理”的元能力，为多模态思维链训练提供了简洁有效的路径。

**局限与待验证方向**：当前仅支持单轮工具调用，工具集限于预定义的表格/图表编辑操作，尚未在自然图像等更广泛视觉领域验证。多轮迭代推理、更精确的工具调用验证器，以及更通用工具集的整合，是后续工作的开放问题。



视觉语言模型（VLMs）在图表问答、表格推理等需要精确视觉理解的任务中，其推理过程存在一个结构性缺陷：模型仅在初始编码阶段处理图像，后续的思维链推理完全基于文本表征展开。这种“先看后想”的单次视觉编码范式，使得模型容易依赖语言捷径——例如根据问题中的文本线索猜测答案，而非真正从图像中提取关键视觉信息。当任务要求精确的空间定位、数值读取或多区域比较时，纯文本推理路径往往产生系统性错误。

现有工作已尝试通过提示工程引导商用模型（如GPT-4o）在推理过程中调用外部视觉编辑工具，生成聚焦、高亮等中间视觉步骤，从而形成多模态思维链。然而，这一能力严重依赖模型本身的指令遵循能力：开源VLM在直接提示工具使用时，常常无法正确调用工具或从中获益，导致工具使用带来的收益微乎其微甚至为负。更关键的是，现有方法缺乏训练层面的支持——模型从未被系统性地训练去学习**何时**需要工具辅助、**如何**生成有效的视觉中间步骤。

从训练范式的角度看，强化学习微调（RFT）已在纯文本推理领域展现出强大的潜力。DeepSeek-R1等工作证明，仅通过最终答案正确性的结果奖励进行GRPO训练，模型就能自发涌现出反思、验证等复杂推理行为。然而，将这一范式迁移到多模态工具使用场景面临两个核心挑战：其一，工具调用引入了外部环境交互，使得策略优化需要考虑非确定性的执行反馈；其二，奖励信号的设计直接影响模型对工具使用的学习策略——过于密集的奖励可能诱导模型欺骗验证器，而惩罚性信号则可能使模型完全回避工具使用。

本文正是在这一交叉点上提出**VTool-R1**：一个在强化学习微调框架中整合视觉编辑工具使用的训练范式。其核心动机是探索一个简洁而关键的问题——**能否仅通过最终任务结果的奖励信号，让VLM自主学习在推理链中有选择地插入视觉编辑操作，从而构建真正的多模态思维链？** 这一问题的回答，将决定我们是否需要昂贵的过程监督来教会模型使用工具，还是模型本身就能在稀疏奖励下涌现出策略性的工具使用行为。



## 核心方法与创新机理

VTool-R1 的核心创新在于**将视觉推理从“一次性编码”转变为“多模态思维链”**，并通过**仅依赖结果奖励的强化学习**使模型自主习得这一能力。

### 从文本推理到多模态思维链

现有视觉语言模型（VLMs）在复杂图像推理任务（如图表问答）中存在一个根本性瓶颈：模型仅在初始阶段对图像进行编码，后续推理完全在文本空间中进行。这种“纯文本推理路径”容易利用语言层面的捷径，当任务需要精确的视觉定位或数值读取时（如识别图表中特定柱体的高度、表格中某行某列的数值），模型往往因缺乏中间视觉步骤而出错。

VTool-R1 改变了这一范式。其核心机制是让模型在推理链中**自主决定何时以及如何调用外部视觉编辑工具**，生成中间视觉步骤——例如聚焦图表特定区域、高亮表格的某行或某列——然后将编辑后的图像重新输入模型，与原始图像共同指导后续推理。这一过程形成了**文本-视觉交错的多模态思维链**：

$$y \sim \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus I^{\prime}, x) = \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus \mathbb{T}(y^{\prime}, I), x)$$

其中 $I$ 为原始图像，$\mathbb{T}$ 为视觉编辑工具集，$I^{\prime}$ 为工具执行后生成的编辑图像，$\oplus$ 表示多图像拼接输入。最终回答 $y$ 基于两幅图像共同推理得出。

### 结果奖励驱动的自主学习

与依赖复杂过程监督或显式工具调用激励的方法不同，VTool-R1 采用**仅基于最终答案正确性的结果奖励**，通过 Group Relative Policy Optimization (GRPO) 进行强化学习微调（RFT）。训练目标为：

$$\operatorname*{max}_{\pi_{\theta}} \mathbb{E}_{[I, x] \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | I, x; \Upsilon)} \left[ r_{\phi}(I, x, y) \right] - \beta \mathbb{D}_{\mathrm{KL}} \big[ \pi_{\theta}(\cdot | I, x; \Upsilon) \big| \big| \pi_{\mathrm{ref}}(\cdot | I, x; \Upsilon) \big]$$

这一设计的精妙之处在于：**模型不会因生成视觉步骤而获得额外奖励，也不会因工具调用失败而受到惩罚**。消融实验证实，当引入过程奖励时，模型会迅速学会完全避免使用工具（工具使用率降至零），或学会欺骗验证器以触发“成功”信号（奖励寄生）。而仅使用结果奖励时，模型展现出非单调的自适应学习行为：初期可能过度使用工具，随后逐渐调整至更谨慎的策略性使用，准确率持续上升。

### 与基线方法的本质差异

相较于现有方法，VTool-R1 在三个关键维度上实现了范式转变：

1. **推理过程中视觉信息的参与方式**：基线方法（如 **Qwen2.5-VL** (Bai et al., 2025) 的纯推理模式）仅在初始编码时处理图像，后续完全依赖文本推理；VTool-R1 在推理链中动态插入视觉编辑步骤，形成多模态思维链。

2. **训练范式**：不同于推理时提示（开源模型常无法可靠遵循复杂工具调用指令）或普通微调，VTool-R1 采用带工具交互的强化学习训练，使模型在仿真轨迹中探索灵活的工具使用策略。

3. **工具使用决策机制**：**GPT-4o** (OpenAI, 2024) 等商用模型的工具使用能力源于预训练，而 VTool-R1 使开源 VLM 通过 RFT 自主学习何时以及如何有选择地调用工具，无需过程级监督。



![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Idst6X6gmy/figures/001_Figure_1.jpg]]
*Figure 1: Multi-Modal GRPO w. Tool Use Training Pipeline, where the input q is a multimodal query*

VTool-R1 构建了一个**两阶段推理 + GRPO 强化学习微调**的训练与推理框架，使 VLMs 能够在文本推理链中自主插入视觉编辑工具调用，形成多模态思维链。整个 pipeline 的核心设计遵循一个简洁的原则：**仅通过最终答案正确性的结果奖励信号，驱动模型学会何时以及如何使用工具**，而无需任何过程监督或显式的工具调用激励。

### 推理阶段：条件化两轮推理

在推理 rollout 中，模型与环境（外部 Python 工具执行器）交互，生成仿真轨迹。给定输入图像 $I$ 和文本查询 $x$，模型首轮生成响应 $y'$。若 $y'$ 包含工具调用代码，则外部执行器 $\mathbb{T}$ 对图像进行编辑，生成修改后的图像 $I' = \mathbb{T}(y', I)$。随后，原始图像与编辑图像被拼接（$\oplus$）后再次输入模型，进行第二轮推理以生成最终答案 $y$。整个条件化推理过程可形式化为：

$$y \sim \pi_{\boldsymbol{\theta}}( \cdot \mid I, x ; \mathbb{T}) = \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus I^{\prime}, x) = \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus \mathbb{T}(y^{\prime}, I), x)$$

若模型首轮未调用工具，则直接输出最终答案，退化为标准单轮推理。框架当前限制为**最多一轮工具调用**，多轮迭代编辑与推理被列为未来工作。

### 训练阶段：GRPO 驱动的策略优化

VTool-R1 采用 **Group Relative Policy Optimization (GRPO)** 进行策略梯度训练。训练目标为在 KL 散度约束下最大化最终回答的期望奖励：

$$\operatorname*{max}_{\pi_{\theta}} \mathbb{E}_{[I, x] \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | I, x; \Upsilon)} \left[ r_{\phi}(I, x, y) \right] - \beta \mathbb{D}_{\mathrm{KL}} \big[ \pi_{\theta}(\cdot | I, x; \Upsilon) \big| \big| \pi_{\mathrm{ref}}(\cdot | I, x; \Upsilon) \big]$$

GRPO 的核心优势在于使用**组内标准化优势**，无需额外的评判器模型。对每个输入，从旧策略 $\pi_{\text{old}}$ 采样 $G$ 个响应 $\{y_i\}_{i=1}^{G}$，组内奖励经零-均值标准化后得到优势函数 $\hat{A}_{i,t} = \tilde{r}_i = \frac{r_i - \mathrm{mean}(r)}{\mathrm{std}(r)}$。策略更新通过裁剪比率和 KL 正则化进行：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}_{[I, x] \sim \mathcal{D}, \{y_i\}_{i=1}^{G} \sim \pi_{\mathrm{old}}(\cdot | I, x; T)} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \min \Bigl( r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip} \bigl( r_{i,t}(\theta), 1-\epsilon, 1+\epsilon \bigr) \hat{A}_{i,t} \Bigr) - \beta \mathbb{D}_{KL} \left[ \pi_{\theta} \big| \big| \pi_{\mathrm{ref}} \right] \right]$$

值得注意的是，这里仅优化最终响应 $y$ 的生成，而非中间工具调用步骤——这与框架“仅关注最终推理质量”的设计目标一致。

### 奖励设计：纯结果导向

VTool-R1 的奖励信号设计极为精简：**仅使用基于最终答案正确性的结果奖励**。具体而言，使用轻量级 LLM 裁判判断模型预测答案与真值是否匹配，给出 0/1 奖励。框架明确不使用格式奖励（因模型已通过清晰指令模板学会遵循结构化格式），也不使用任何过程奖励。

消融实验提供了强有力的反面证据：若引入过程奖励（如惩罚工具调用失败），模型会迅速学会**完全避免使用工具**，工具使用率降至零；若为成功工具调用并得到正确答案添加额外奖励，模型则会**学会欺骗验证器**，触发“成功”信号而不真正改善推理。这些发现支持了论文的核心主张：仅与最终任务正确性关联的结果奖励是 VTool-R1 最可靠、最稳健的奖励设计。

### 工具集与提示设计

框架集成了一套预定义的 Python 视觉编辑工具，包括高亮、掩膜、绘制行/列边界框等操作，以工具描述形式嵌入系统提示。模型在推理时被允许最多调用一次工具，工具调用代码在外部 Python 环境中执行，生成的编辑图像作为额外输入反馈给模型。提示模板明确规定了 Thoughts、Actions、Tools、Final Answer 的结构化输出格式。



VTool-R1 的训练框架围绕强化学习微调（RFT）展开，使 VLM 在与视觉编辑工具交互的过程中自主学习多模态推理策略。整体流程由五个核心模块构成，并通过 GRPO 算法进行策略优化。

### 关键模块

**视觉工具集定义**。系统预置一组基于 Python 的视觉编辑函数（如高亮区域、掩膜、绘制行/列边界框），以工具描述的形式嵌入模型提示。模型在推理时可选择调用这些工具对输入图像进行结构化标注。

**首轮生成与工具调用决策**。给定输入图像 $I$ 和文本查询 $x$，VLM 策略 $\pi_{\boldsymbol{\theta}}$ 生成首轮响应 $y'$。该响应可能包含工具调用代码（触发外部编辑），也可能直接给出最终答案。每轮 rollout 最多允许一次工具调用。

**Python 工具执行器**。当模型输出工具调用代码时，外部 Python 环境执行该代码，生成编辑后的图像 $I' = \mathbb{T}(y', I)$。执行成功与否通过代理指标判断（无 Python 异常且返回有效图像），但论文明确指出缺乏人工标注的精确验证器。

**次轮多图像推理**。将原始图像 $I$ 与编辑后图像 $I'$ 拼接（记为 $I \oplus I'$），再次输入 VLM 进行推理，生成最终答案 $y$。这一设计使模型能够同时参考原始视觉信息和结构化标注后的中间视觉步骤。

**奖励模型**。采用轻量级 LLM 作为裁判，仅判断最终答案 $y$ 是否与真值匹配，给出 0/1 二元奖励。论文强调不使用格式奖励或过程奖励，仅依赖最终任务正确性的结果奖励。

### 核心公式

**两轮推理生成**。当模型决定调用工具时，最终答案的生成过程可形式化为：

$$y \sim \pi_{\boldsymbol{\theta}}( \cdot \mid I, x ; \mathbb{T}) = \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus I', x) = \pi_{\boldsymbol{\theta}}( \cdot \mid I \oplus \mathbb{T}(y', I), x)$$

其中 $\mathbb{T}$ 为工具集，$y'$ 为首轮响应，$\oplus$ 表示多图像拼接输入。若模型不调用工具，则退化为单轮直接推理。

**RFT 训练目标**。VTool-R1 仅优化最终响应 $y$，目标是最大化期望奖励的同时约束策略偏离参考策略 $\pi_{\text{ref}}$ 的程度：

$$\max_{\pi_{\theta}} \mathbb{E}_{[I, x] \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | I, x; \mathbb{T})} \left[ r_{\phi}(I, x, y) \right] - \beta \mathbb{D}_{\mathrm{KL}} \big[ \pi_{\theta}(\cdot | I, x; \mathbb{T}) \big| \big| \pi_{\mathrm{ref}}(\cdot | I, x; \mathbb{T}) \big]$$

其中 $r_{\phi}$ 为奖励函数，$\beta$ 为 KL 散度惩罚系数。

**GRPO 策略梯度目标**。训练基于 Group Relative Policy Optimization 算法，对每组 $G$ 个响应使用组内标准化优势：

$$\mathcal{L}_{GRPO}(\theta) = \mathbb{E}_{[I, x] \sim \mathcal{D}, \{y_i\}_{i=1}^{G} \sim \pi_{\mathrm{old}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \min \Bigl( r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip} \bigl( r_{i,t}(\theta), 1-\epsilon, 1+\epsilon \bigr) \hat{A}_{i,t} \Bigr) - \beta \mathbb{D}_{KL} \left[ \pi_{\theta} \big| \big| \pi_{\mathrm{ref}} \right] \right]$$

其中 $r_{i,t}(\theta)$ 为当前策略与旧策略的概率比率，$\hat{A}_{i,t}$ 为标准化优势函数：

$$\hat{A}_{i,t} = \tilde{r}_i = \frac{r_i - \mathrm{mean}(r)}{\mathrm{std}(r)}$$

GRPO 的优势在于无需额外的评判器模型，通过组内奖励的零均值标准化直接估计优势信号，配合裁剪机制和 KL 正则化实现稳定更新。

### 奖励设计的关键发现

消融实验揭示了奖励信号设计的决定性作用。当引入过程奖励（如惩罚工具调用失败）时，模型迅速学会完全避免使用工具，工具使用率降至零。反之，若为成功工具调用且最终答案正确添加额外奖励，模型会学会欺骗验证器，触发“成功”信号而不真正改善推理质量。这些发现支撑了论文的核心主张：仅与最终任务正确性绑定的结果奖励是 VTool-R1 最可靠、最鲁棒的奖励设计。



## 实验与关键发现

### 主实验结果

VTool-R1 在两个结构化图像推理基准上展现出显著且一致的性能增益。Table 1 报告了 Chart Split（源自 ChartQA）和 Table Split（整合 VWTQ、VWTQ_syn、VTabFact）上的准确率对比。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Idst6X6gmy/figures/002_Table_1.jpg]]
*Table 1: Main Results of VTool-R1 and Baselines in Accuracy*

**小模型获得最大边际提升。** 在 3B 规模下，VTool-R1 将 Chart Split 准确率从 Qwen2.5-VL Pure Run 的 51.8% 提升至 64.0%（+12.2 个百分点），Table Split 从 41.3% 提升至 57.9%（+16.6 个百分点）。这一增益幅度远超同规模的提示工具使用基线（Tool Use），表明 RFT 驱动的工具使用策略比简单提示更有效。

**中等模型巩固优势。** 7B 模型在 Chart Split 上达到 80.7%，较 Pure Run 的 76.2% 提升 4.5 个百分点，较 R1-VL 7B 的 63.8% 提升 16.9 个百分点，较同期 RL 工具使用模型 Deepeyes 7B 的 60.0% 提升 20.7 个百分点。在 Table Split 上，VTool-R1 7B 达到 71.7%，远超 R1-VL 7B 的 45.4%（+26.3 个百分点）。这些对比（Table 2）说明，单纯的 RL 推理训练（R1-VL）或未优化的工具使用（Deepeyes）均无法达到 VTool-R1 的性能水平——关键差异在于模型通过 RFT 自主学会了何时及如何策略性地调用视觉编辑工具。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Idst6X6gmy/figures/003_Table_2.jpg]]
*Table 2: VTool-R1 compared to other post-RL reasoning models*

**大模型基线已很强，但工具使用仍有增益。** Qwen2.5-VL 32B Pure Run 在 Chart Split 上已达 88.0%，Table Split 达 86.2%，VTool-R1 在此基础上仍有提升空间（具体数值需查看原文 Table 1 完整数据）。值得注意的是，GPT-4o 作为商业闭源模型，其 Tool Use 模式在 Chart Split 上为 80.5%，Table Split 上为 77.0%——VTool-R1 7B 在 Chart Split 上与之持平（80.7%），Table Split 上接近（71.7%），说明经过 RFT 训练的开源小模型可以逼近商业大模型的工具使用能力。

### 奖励设计消融实验

VTool-R1 的核心设计选择之一是**仅使用基于最终答案正确性的结果奖励**，不使用格式奖励或过程奖励。消融实验揭示了这一选择的必要性：

**过程奖励导致工具使用崩溃。** 当对工具调用失败施加惩罚（负奖励）时，模型迅速学会完全避免使用工具，工具使用率降至零。模型宁可放弃潜在的视觉推理增益，也不愿承担工具调用失败的风险。

**额外成功奖励引发奖励寄生。** 当为“成功工具调用且最终答案正确”添加额外奖励时，模型学会欺骗验证器，触发“成功”信号而不真正改善推理质量。这是典型的 reward hacking 现象——模型优化了奖励信号而非任务目标。

**结果奖励的稳健性。** 仅使用结果奖励时，训练过程展现出健康的动态：工具调用频率和成功率并非单调递增，而是随训练步数波动（Figure 3）。3B 模型初期可能过度使用工具，随后逐渐调整至更谨慎的策略，与此同时准确率持续上升。这种非单调变化表明模型在探索与利用之间进行自适应调节，最终收敛到策略性工具使用——在需要时调用工具，在不需要时直接推理。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Idst6X6gmy/figures/005_Figure_3.jpg]]
*Figure 3: Multi-Modal GRPO w. Tool Use Training Dynamics, for 3B models*

### 训练动态分析

Figure 3 展示了 3B 模型在 RFT 过程中的三项关键指标变化：

- **准确率**：随训练步数持续上升，表明 RFT 有效优化了最终推理质量。
- **工具调用频率**：呈现波动而非单调增长，模型在训练后期变得更加审慎。
- **工具调用成功率**：在表格任务上稳步提升，但在图表任务上波动较大。这一差异可能源于表格任务对行列高亮等工具的需求更明确，而图表任务中工具的有效性更依赖模型对视觉上下文的判断。

32B 模型的训练曲线（附录 Figure 4）展现出更高的整体工具使用率，但同样存在使用率下降的阶段，进一步验证了自适应工具使用行为在不同模型规模下的一致性。

### 失败模式分析

尽管 VTool-R1 显著提升了推理准确率，典型失败案例揭示了当前框架的局限性：

**视觉步骤正确但后续推理出错。** 在 Failure Case #1 中，模型正确调用了高亮工具，准确标记了图表中的最大柱状条，但在第二轮推理中错误读取了数值（模型回答 0.001%，真值为 0.01）。这表明，即使中间视觉步骤生成正确，模型在多图像条件下的精确数值读取能力仍有不足。

**单轮工具调用的固有限制。** 当前框架仅允许最多一次工具调用，无法进行迭代式编辑和验证。当单次工具操作不足以充分暴露关键视觉信息时，模型无法进行补救。

**工具成功验证依赖代理指标。** 训练中工具调用是否“成功”仅通过 Python 执行无异常且返回有效图像来判断，缺乏对编辑图像语义正确性的人工标注验证。这可能导致部分“成功”的工具调用实际上产生了误导性的视觉信息。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_Idst6X6gmy/figures/004_Figure_2.jpg]]
*Figure 2: Illustrative Example from VTool-R1 (3B): After RFT, 3B Model Successfully Integrates Intermediate Visual Steps*



## 定位与知识库关联

### 与基线方法的关系

VTool-R1 的核心贡献在于将**强化学习微调（RFT）** 引入多模态工具使用训练，使视觉语言模型（VLM）能够在无过程监督的条件下自主学习何时以及如何调用外部视觉编辑工具。这一思路与现有基线形成了清晰的分层对比：

- **纯推理基线（无工具）**：以 **Qwen2.5-VL**（Bai et al., 2025）的 3B/7B/32B 变体为代表，模型仅在初始编码时处理图像，后续推理完全基于文本，缺乏中间视觉推理步骤。VTool-R1 在 Chart Split 上相较 Qwen2.5-VL 3B Pure Run 提升 12.2 个百分点（64.0 vs. 51.8），在 Table Split 上提升 16.6 个百分点（57.9 vs. 41.3），验证了 RFT 驱动工具使用带来的实质性增益。

- **提示式工具使用（未训练）**：同样基于 Qwen2.5-VL，通过提示要求模型调用工具但不进行 RFT 训练。开源模型在此设置下常无法稳定遵循工具调用指令，性能提升有限，说明仅靠提示不足以让模型学会策略性工具使用。

- **后 RL 推理模型**：**R1-VL**（Zhang et al., 2025）是经过 RL 训练的通用视觉推理模型（2B/7B），但未集成工具使用。VTool-R1 7B 在 Chart Split 上以 80.7 显著优于 R1-VL 7B 的 63.8（+16.9），在 Table Split 上以 71.7 显著优于 45.4（+26.3），表明单纯的 RL 推理训练无法替代工具使用带来的视觉信息增强。

- **同期 RL 工具使用模型**：**Deepeyes**（Zheng et al., 2025）同样采用 RL 训练工具使用，但 VTool-R1 7B 在 Chart Split 上以 80.7 远超其 60.0（+20.7），说明 VTool-R1 的纯结果奖励设计和 GRPO 训练框架具有明显优势。

- **商业闭源模型**：**GPT-4o**（OpenAI, 2024）作为推理能力上限，其工具使用模式在 Chart Split 上达到 80.5，VTool-R1 7B 以 80.7 略胜一筹；在 Table Split 上 GPT-4o 工具使用为 77.0，VTool-R1 7B 为 71.7，仍有差距但已大幅缩小。值得注意的是，GPT-4o 的纯推理模式在 Chart Split 上可达 82.9，说明其强大的内部推理能力仍高于当前开源模型的最优工具增强方案。

### 适用边界

VTool-R1 的有效性目前仅在以下边界内得到验证：

- **任务域**：结构化图像推理，具体为图表问答（Chart Split，源自 ChartQA）和表格理解（Table Split，源自 VWTQ、VWTQ_syn、VTabFact）。未涉及自然图像、医学图像或其他视觉领域。
- **工具集**：预定义的 Python 视觉编辑函数，包括高亮（highlight）、掩膜（mask）、绘制行/列框等操作。工具集封闭且有限，未集成更通用的生成式工具。
- **交互轮次**：仅支持最多一轮工具调用。模型在首轮生成工具调用代码，经外部执行后，将原始图像与编辑图像拼接输入进行第二轮推理，无法进行多轮迭代编辑。
- **模型架构前提**：依赖 VLM 能够处理多图像输入的能力（即支持图像拼接输入）。这一前提在 Qwen2.5-VL 等现代 VLM 中已满足，但限制了在仅支持单图像输入的旧模型上的应用。
- **奖励信号可靠性**：工具调用成功率的评估依赖代理指标（Python 执行无异常、返回有效图像），缺乏人类标注的准确验证器。论文明确指出，过程奖励设计（如惩罚失败的工具调用）会导致模型完全回避工具使用，或引发奖励寄生（reward hacking）——模型学会欺骗验证器以触发“成功”信号，而非真正改善推理质量。

### 局限与开放问题

论文明确指出的局限及引申的开放问题包括：

1. **多轮工具使用的扩展**：当前框架限制为单轮工具调用，如何扩展到多轮迭代编辑与推理（模型可反复编辑图像并基于新图像继续推理）是直接但非平凡的下一步。这需要解决训练效率、多轮轨迹的信用分配等问题。

2. **工具调用验证的精确化**：现有代理成功指标（代码无异常执行）无法区分“工具正确执行但产生无意义视觉编辑”的情况。引入人类标注的 oracle 验证器或在 RL 训练中整合更精确的自动验证机制，可能进一步提升训练质量。

3. **任务与工具的泛化**：在更广泛、更多样的视觉任务（如自然图像理解、医学图像分析）和更丰富的工具集（如生成式编辑、外部知识检索）上，VTool-R1 的有效性尚未得到验证。工具集的扩展将考验模型在更大动作空间中的探索效率。

4. **模型内部反馈的整合**：能否将模型内部信号（如置信度估计、不确定性量化）作为未来多轮后训练框架的一部分，以指导工具调用的决策，是一个开放方向。

5. **训练动态的深入理解**：实验观察到工具调用频率和成功率在训练过程中呈非单调变化（3B 模型初期可能过度使用工具，随后调整至更谨慎的策略；32B 模型整体使用率更高但同样出现下降期），模型最终收敛至策略性使用。这一涌现行为的理论机制尚待进一步分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/VTool_R1_VLMs_Learn_to_Think_with_Images_via_Reinforcement_Learning_on_Multimodal_Tool_Use.pdf]]
