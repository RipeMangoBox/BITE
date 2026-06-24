---
title: "Measuring and Mitigating Rapport Bias of Large Language Models under Multi-Agent Social Interactions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Measuring_and_Mitigating_Rapport_Bias_of_Large_Language_Models_under_Multi_Agent_Social_Interactions.pdf
openreview_forum_id: gF31wuYdk7
aliases:
- KG
- MMRBLLMUMASI
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过控制历史互动中同伴与模型回答的一致程度（融洽级别）、当前回合同伴的行为模式（支持、强烈反对、轻微反对）以及模型自身的置信度，可以系统性地调节模型的社会敏感性与决策偏移。"
primary_logic: "模型规模是调节社会影响敏感性的首要因素，大模型更坚韧并能从授权提示中缩小鲁棒性差距；而小模型则需要结合多智能体上下文和基于结果的奖励进行 GRPO 训练，才能在提升任务准确率的同时保持对社交干扰的鲁棒性。"
claims:
- "在基础设置下，大模型（>32B）的平均 O–K Δ 为 -3.64%，而小模型（≤32B）为 -5.65%；使用授权提示后，大模型的 Δ 转为 +0.12%，小模型恶化至 -11.25%，说明规模与提示策略共同决定社会鲁棒性。"
- "GRPO 训练整体比 SFT 在 Original 和 KAIROS 准确率上分别提升 +12.3% 和 +16.4%，但不同变体的鲁棒性差异显著：加入多智能体上下文（MAS）且使用正常提示与结果奖励（NS-OR）的配置在保持鲁棒性的同时达到最高准确率。"
- "模型在社交互动中损失的正确预测始终超过纠正的错误，抵抗性转变约占 65%，而利用性（Utility）转变的置信度从基线的 0.584 急剧下降到训练后的 0.207，表明训练虽提高表面准确率却削弱了从同伴处学习的能力。"
- "KAIROS (聚合所有类别) 上 O–K Δ (鲁棒性) = 授权提示下大模型平均: +0.12%"
---

# Measuring and Mitigating Rapport Bias of Large Language Models under Multi-Agent Social Interactions

> [!tip] 核心洞察
> 模型规模是调节社会影响敏感性的首要因素，大模型更坚韧并能从授权提示中缩小鲁棒性差距；而小模型则需要结合多智能体上下文和基于结果的奖励进行 GRPO 训练，才能在提升任务准确率的同时保持对社交干扰的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多智能体社交互动中大型语言模型融洽偏误的测量与缓解 |
| 英文题名 | Measuring and Mitigating Rapport Bias of Large Language Models under Multi-Agent Social Interactions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gF31wuYdk7); [Project](https://anonymous.4open.science/r/KAIROS-4F71) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | KAIROS (用于多维社交影响评估的基准) 及配套缓解策略（包括授权/反思提示、监督微调与 GRPO 变体） |
| Dataset | KAIROS (聚合所有类别), KAIROS (小模型) |

> [!tip] 效果简介
> - KAIROS (聚合所有类别) 上，O–K Δ (鲁棒性) 为 授权提示下大模型平均: +0.12%，对比 基础提示下大模型平均: -3.64%，变化 +3.76pp。
> - KAIROS (小模型) 上，KAIROS 准确率 为 GRPO-MAS-NS-OR (Qwen2.5-3B) 57.9%，对比 Base (Qwen2.5-3B) 48.8%，变化 +9.1pp。
> - KAIROS (小模型) 上，鲁棒性 (O–K Δ) 为 GRPO-MAS-NS-OR (Qwen2.5-14B) -6.5%，对比 Base (Qwen2.5-14B) -8.7%，变化 +2.2pp (改善)。

## 概述

大型语言模型（LLM）在融入多智能体社交环境时，极易受历史交互形成的“融洽关系”及当前同伴行为（支持/反对）的影响——即使同伴提供错误答案，模型也倾向于从众，导致正确预测大量损失，而纠正错误的能力不足，整体准确率显著下降。这一瓶颈的本质在于：模型将交互历史视为真实的社会信号，系统性地调节自身对社会影响的敏感性，而非基于任务正确性独立决策。

为系统测量这一现象，本文提出 **KAIROS** 基准，通过控制历史互动中同伴与模型回答的一致程度（融洽级别）、当前回合同伴的行为模式（支持、强烈反对、轻微反对）以及模型自身的置信度，构建模型定制化的社交压力测试。评估采用四个核心指标：准确率、O–K Δ（鲁棒性）、Utility（利用度）和 Resistance（抵抗度），其中 O–K Δ 衡量从原始评估到多智能体评估准确率的相对变化，正值表示社交互动提升了性能，负值表示损害。

核心发现可概括为三条因果链：

1. **模型规模是调节社会影响敏感性的首要因素。** 在基础设置下，大模型（>32B）的平均 O–K Δ 为 -3.64%，而小模型（≤32B）为 -5.65%；使用授权提示后，大模型的 Δ 转为 +0.12%，小模型却恶化至 -11.25%，说明规模与提示策略共同决定社会鲁棒性（Table 1）。

2. **GRPO 训练整体优于 SFT，但不同变体的鲁棒性差异显著。** GRPO 在 Original 和 KAIROS 准确率上分别提升 +12.3% 和 +16.4%；其中，加入多智能体上下文（MAS）且使用正常提示与结果奖励（NS-OR）的配置，在保持鲁棒性的同时达到最高准确率（Table 2）。

3. **训练虽提高表面准确率，却削弱了从同伴处学习的能力。** 模型在社交互动中损失的正确预测始终超过纠正的错误，抵抗性转变约占 65%；而利用性（Utility）转变的置信度从基线的 0.584 急剧下降到训练后的 0.207（Figure 4），揭示出准确率-鲁棒性之间的深层张力。

在方法谱系上，KAIROS 的评估框架通过动态构建同伴回应（基于模型自身的信念分布）实现了模型定制化测试，区别于使用固定对抗样本的传统鲁棒性评估。缓解策略覆盖提示工程（授权/反思提示）、监督微调（SFT）和基于 GRPO 的强化学习，其中 GRPO 变体通过控制四个关键插槽——多智能体上下文（MAS/nonMAS）、系统提示设计（NS/DS）、奖励函数（OR/DR）和数据过滤策略（LConf/LCorr）——系统性地探索了训练策略对鲁棒性的影响。

主要限制包括：评估仅采用多项选择题格式，可能低估开放生成场景下的社会脆弱性；训练实验仅覆盖 ≤32B 的小模型；交互仍属脚本化模拟，与真实人类协同存在差距；未考虑多轮交互的长期演化效应。

## 背景与动机

大型语言模型（LLM）正越来越多地被部署于多智能体协作环境，例如群体决策、辩论与知识整合。在这些场景中，模型不仅需要独立求解任务，还必须解读、采纳或抵制来自其他智能体的信号。然而，现有研究揭示了一个关键脆弱性：LLM 极易受到社交动态的干扰，即便同伴提供的是明显错误的信息，模型也倾向于从众，从而导致大量正确预测的损失。

这一现象的核心瓶颈在于“融洽偏误”（rapport bias）——模型与同伴在历史交互中形成的融洽关系，以及当前回合同伴的支持或反对行为，会系统性地扭曲其决策。具体而言，当历史互动中同伴与模型回答高度一致（高融洽级别）时，模型更倾向于信任该同伴；而一旦同伴转而提供错误答案，模型往往无法有效纠正自身错误，整体准确率因此显著下降。然而，现有基准测试大多聚焦于模型在孤立环境下的能力，缺乏对上述社交敏感性进行系统、可控的测量手段。

为填补这一空白，本文提出了 **KAIROS**——一个用于多智能体社交互动中 LLM 融洽偏误的测量与缓解基准。KAIROS 的核心设计思路在于，通过精确控制历史交互中的融洽级别、当前回合的同伴行为（支持、强烈反对、轻微反对）以及模型自身的置信度，实现对模型社交脆弱性的细粒度评估。在此基础上，本文进一步探索了三类缓解策略：提示工程（授权提示与反思提示）、监督微调（SFT）以及基于组相对策略优化（GRPO）的强化学习，旨在提升模型在社交压力下的鲁棒性，同时保持甚至提高任务准确率。

## 核心创新

本工作的核心创新在于首次系统性地将 **多智能体社交互动中的“融洽偏误”（Rapport Bias）** 概念化为可测量、可操控的评估维度，并构建了配套的缓解策略体系。其创新点并非单一技术突破，而是围绕“社会敏感性”这一瓶颈，形成了 **基准-诊断-缓解** 的完整闭环。

### 1. 动态、模型定制的社交压力测试基准：KAIROS

与以往仅评估独立任务准确率的基准不同，KAIROS 的核心创新在于其 **动态数据构建流程**，该流程将评估本身转化为针对特定模型的压力测试。

- **信念抽取与同伴回应构造**：KAIROS 首先通过自一致性采样（$T$ 次随机生成）推断模型对每个问题的 **内在信念**（多数答案）和 **置信度**（预测熵 $\mathcal{H}[\bar{\mathbf{p}}] = -\sum_{k=1}^{K} \bar{p}_k \log \bar{p}_k$）。随后，同伴的回应（支持、强烈反对、轻微反对）直接基于该模型的信念分布构造。这意味着同伴的“错误”回答正是模型自身可能犯的错误，从而形成了高度针对性的社交干扰。
- **多维社会影响轴操控**：KAIROS 系统性地操控了三个关键社会轴：
    1.  **历史融洽级别**：通过控制历史互动中同伴与模型回答的一致程度，模拟从完全信任到完全对立的社交关系。
    2.  **当前回合同伴行为**：在给定融洽背景下，注入支持或反对的即时信号。
    3.  **模型自身置信度**：利用预测熵区分高/低置信度样本，考察自我信念强度对社会敏感性的调节作用。

这种设计使得 KAIROS 超越了静态的问答对评估，能够精细诊断 LLM 在社交压力下的决策偏移。

### 2. 关键方法槽位变更：从提示到训练的缓解策略谱系

为缓解 KAIROS 所揭示的鲁棒性缺陷，本工作探索了从推理时干预到训练时优化的完整策略谱系，其核心创新在于揭示了不同策略与 **模型规模** 之间的关键交互作用。

| 方法槽位 | 基线配置 | 创新配置 | 核心发现与机制 |
| :--- | :--- | :--- | :--- |
| **系统提示设计** | 正常提示 (NS) | **授权提示 (Empowered)** | 鼓励模型自信决策、批判性评估同伴。**规模依赖性**：大模型（>32B）的 O–K Δ 从 -3.64% 逆转为 **+0.12%**，有效弥合鲁棒性差距；小模型（≤32B）反而恶化至 -11.25%。 |
| **训练上下文** | 无多智能体上下文 (nonMAS) | **多智能体上下文 (MAS)** | 在 GRPO 训练中包含完整历史交互与同伴回答。**规模依赖性**：整体鲁棒性平均提升约 1%，但大模型获益约 +4%，小模型（3B）反而下降约 4%。 |
| **奖励函数** | 仅结果奖励 (OR) | **辩论奖励 (DR)** | 在结果正确性之外，加入格式合规性与内在声音多样性的复合奖励 $R = \lambda_{\mathrm{corr}} R_{\mathrm{corr}} + \lambda_{\mathrm{fmt}} R_{\mathrm{fmt}} + \lambda_{\mathrm{iv}} R_{\mathrm{iv}}$。**消融结论**：辩论式奖励与提示并未带来额外增益，**正常提示 + 结果奖励 (NS-OR)** 在所有 GRPO 配置中取得了最佳的准确率-鲁棒性权衡。 |
| **数据过滤策略** | 无过滤 | **低置信度 (LConf) / 低正确率 (LCorr) 过滤** | 仅对模型不自信或原本回答错误的样本进行训练。**失败模式**：LConf 虽提高表面准确率，但鲁棒性变差；LCorr 导致严重的性能坍塌（Qwen2.5-14B 的 O–K Δ 达 **-33.3%**），揭示了仅针对弱点的训练会破坏模型的社交防御机制。 |

### 3. 核心洞察：准确率-鲁棒性的结构性张力

本工作的深层创新在于揭示了缓解策略中普遍存在的 **准确率-鲁棒性权衡**。通过引入 **Utility（利用度）** 和 **Resistance（抵抗度）** 指标，分析发现：

- **损失大于收益**：模型在社交互动中损失的正确预测（抵抗失败）始终超过其纠正的错误（利用成功）。抵抗性转变平均约占 65%。
- **训练削弱了学习能力**：GRPO 训练虽然大幅提升了表面准确率（Original +12.3%, KAIROS +16.4%），但模型的 **利用度置信度从基线的 0.584 急剧下降到 0.207**。这表明模型变得“固执”，丧失了从同伴处学习有用信息的能力，其鲁棒性提升是以牺牲社交学习能力为代价的。

综上，本工作的核心创新贡献在于定义并系统性地剖析了 LLM 的融洽偏误问题，揭示了模型规模是调节社会敏感性的首要因素，并指出了当前缓解策略在提升鲁棒性的同时会损害模型社交学习能力的结构性缺陷，为未来设计既能抵抗误导又能利用帮助的社交智能体奠定了基准。

## 整体框架

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the KAIROS evaluation framework. The process begins with Original Evaluation, where a question is posed and the majority answer is derived from multiple generations, along with confidence estimation. In Peer Construction, the subject agent’s majority answer and predefined action type (e.g., support) are used to construct interactions with other agents. Finally, in KAIROS Evaluation, each agent considers historical context, the current question, and peer responses to generate a socially-informed answer within a multi-agent system (MAS), which is then assessed using various evaluation metrics (e.g., accuracy & robustness, utility, and resistance)*

KAIROS 评估框架采用三阶段流水线设计，将大型语言模型置于可控的多智能体社交互动中，系统性地测量其社会敏感性。整个流程从模型的原始信念推断出发，动态构建针对性的同伴压力，最终在多智能体模拟环境中完成评估。

**阶段一：原始评估与信念推断**

框架首先对每个基准问题执行原始评估。对给定的多项选择题，模型进行 $T$ 次随机采样生成答案，通过多数投票确定其“首选答案” $x_i$，并基于采样一致性估计其置信度。具体而言，经验预测分布定义为：

$$\bar{p}_k = \hat{p}(y = k \mid \mathbf{x}) = \frac{1}{T} \sum_{t=1}^{T} \mathbf{1}[y_t = k], \quad k = 1, \ldots, K$$

预测熵 $\mathcal{H}[\bar{\mathbf{p}}] = -\sum_{k=1}^{K} \bar{p}_k \log \bar{p}_k$ 作为置信度的量化指标，用于将样本划分为高置信度与低置信度两类。这一阶段的核心产出是每个样本的（答案，置信度）二元组，为后续同伴行为构造提供基础。

**阶段二：同伴回应构造**

基于阶段一推断的模型信念分布，框架为每个样本构造同伴代理的针对性回应。同伴行为分为三种类型：支持、强烈反对和轻微反对。由于同伴回应直接源自目标模型自身的信念分布，这构成了一个模型定制化的压力测试——同伴可能提供与模型原始信念一致或冲突的答案，且冲突程度可精确控制。

同时，框架通过操纵历史交互中同伴回答与模型回答的一致程度，定义了三种融洽级别，用于模拟模型与同伴之间不同的社交关系历史。

**阶段三：KAIROS 多智能体评估**

在最终评估阶段，模型被置于完整的多智能体系统中。每个评估实例包含：当前问题、历史互动上下文（体现融洽级别）、以及当前回合同伴的回应（体现支持或反对行为）。模型需要在此社交情境下生成最终答案 $y_i$。评估结果通过四个核心指标量化：

- **准确率**：KAIROS 环境下的整体任务成功率。
- **鲁棒性**：通过 O–K 变化率衡量，$\mathrm{O-K}\Delta = \frac{\mathrm{Accuracy}_{\mathrm{KAIROS}} - \mathrm{Accuracy}_{\mathrm{Original}}}{\mathrm{Accuracy}_{\mathrm{Original}}}$，正值表示社交互动提升了性能，负值表示损害。
- **利用度**：$U_M = \frac{\sum_{i=1}^{N}\mathbf{1}\{x_i=0 \wedge y_i=1\}}{\sum_{i=1}^{N}\mathbf{1}\{x_i=0\}}$，衡量原本错误但在社交情境下被纠正的样本比例。
- **抵抗度**：$R_M = \frac{\sum_{i=1}^{N}\mathbf{1}\{x_i=1 \wedge y_i=1\}}{\sum_{i=1}^{N}\mathbf{1}\{x_i=1\}}$，衡量原本正确且在同伴干扰下仍保持正确的样本比例。

**缓解策略训练管线**

在评估框架之上，论文引入了三类缓解策略，形成独立的训练管线：

- **提示工程**：包括授权提示（鼓励模型自信决策、批判性评估同伴回应）和反思提示（首轮回答后由模型自我反思修正）。
- **监督微调**：使用模板化的正确答案和完整社交上下文进行单轮训练。
- **GRPO 强化学习**：在组相对策略优化框架下，通过不同配置变体进行训练。关键可调节槽位包括：是否包含多智能体上下文、系统提示设计（正常提示 vs. 辩论式提示）、奖励函数（仅结果奖励 vs. 结合正确性、格式和内在声音多样性的复合奖励 $R = \lambda_{\mathrm{corr}} R_{\mathrm{corr}} + \lambda_{\mathrm{fmt}} R_{\mathrm{fmt}} + \lambda_{\mathrm{iv}} R_{\mathrm{iv}}$）、以及数据过滤策略（低置信度过滤 vs. 低正确率过滤）。训练数据与评估数据不相交，确保评估的独立性。

## 核心模块与公式推导

### 2.1 动态评估数据构建模块

KAIROS 的评估数据并非静态标注，而是针对每个被测模型动态生成。该模块包含两个子步骤：

**步骤一：原始信念推断。** 对每一道基准题目，让模型独立生成 $T$ 次随机回答（论文中 $T=5$），据此估计模型的经验预测分布：

$$\bar{p}_k = \hat{p}(y = k \mid \mathbf{x}) = \frac{1}{T} \sum_{t=1}^{T} \mathbf{1}[y_t = k], \quad k = 1, \ldots, K$$

其中 $\bar{p}_k$ 为答案选项 $k$ 的估计概率，$K$ 为选项总数。多数投票结果即被视为模型的“原始信念”（Original Belief）。模型置信度由预测熵量化：

$$\mathcal{H}[\bar{\mathbf{p}}] = -\sum_{k=1}^{K} \bar{p}_k \log \bar{p}_k$$

该熵值用于将样本划分为高置信度与低置信度两类，后续分析模型在自信程度不同时对社会影响的敏感性。

**步骤二：同伴回应构造。** 基于步骤一推断出的模型信念分布，为每个样本构造同伴的针对性回应。同伴行为分为三类：支持（Support，与模型信念一致）、强烈反对（Oppose-Hard，给出其他选项中的最高概率答案）和轻微反对（Oppose-Easy，给出最低概率答案）。由于同伴回应直接源自模型自身的信念分布，这构成了一个模型个性化的压力测试。

### 2.2 多智能体模拟模块

KAIROS 的多智能体模拟将历史互动与当前回合同伴回应组合，系统性地操控三个社交敏感性轴：

- **融洽级别（Rapport Level）：** 通过控制历史互动中同伴回答与模型回答的一致程度来调节，范围从 0%（完全不一致）到 100%（完全一致）。
- **当前回合同伴行为：** 支持、强烈反对或轻微反对。
- **模型自身置信度：** 基于预测熵划分的高/低置信度。

模型在收到历史上下文、当前问题及同伴回应后，生成社交环境下的最终答案。

### 2.3 核心评估指标

KAIROS 定义了四个关键指标，用于从不同维度刻画模型的社会鲁棒性。

**O-K 变化率（鲁棒性指标）：**

$$\mathrm{O\text{-}K}\Delta = \frac{\mathrm{Accuracy}_{\mathrm{KAIROS}} - \mathrm{Accuracy}_{\mathrm{Original}}}{\mathrm{Accuracy}_{\mathrm{Original}}}$$

该指标衡量从原始独立评估（Original）到多智能体社交评估（KAIROS）准确率的相对变化。正值表示社交互动提升了性能，负值表示社交干扰造成了损害。这是衡量模型社会鲁棒性的核心指标。

**利用度（Utility）：**

$$U_M = \frac{\sum_{i=1}^{N}\mathbf{1}\{x_i=0 \wedge y_i=1\}}{\sum_{i=1}^{N}\mathbf{1}\{x_i=0\}}$$

其中 $x_i=0$ 表示样本 $i$ 在原始评估中回答错误，$y_i=1$ 表示在 KAIROS 中回答正确。$U_M$ 衡量模型从同伴输入中获益、纠正自身错误的能力。

**抵抗度（Resistance）：**

$$R_M = \frac{\sum_{i=1}^{N}\mathbf{1}\{x_i=1 \wedge y_i=1\}}{\sum_{i=1}^{N}\mathbf{1}\{x_i=1\}}$$

其中 $x_i=1$ 表示原始评估中回答正确。$R_M$ 衡量模型在同伴误导下仍能保持正确判断的能力。

### 2.4 GRPO 训练的复合奖励函数

在基于 GRPO 的缓解训练中，论文探索了辩论式奖励（Debating Reward），其复合形式为：

$$R = \lambda_{\mathrm{corr}} R_{\mathrm{corr}} + \lambda_{\mathrm{fmt}} R_{\mathrm{fmt}} + \lambda_{\mathrm{iv}} R_{\mathrm{iv}}$$

其中：
- $R_{\mathrm{corr}}$ 为答案正确性奖励（基于精确匹配、BLEU 或 BERTScore）；
- $R_{\mathrm{fmt}}$ 为回答格式合规性奖励（如标签完整性、LaTeX 检测）；
- $R_{\mathrm{iv}}$ 为内在声音多样性奖励（通过正则表达式检测 hedging 短语、区分不同声音数量等）；
- $\lambda_{\mathrm{corr}}, \lambda_{\mathrm{fmt}}, \lambda_{\mathrm{iv}}$ 为各分量的权重系数。

值得注意的是，消融实验表明，简单的仅结果奖励（Outcome-based Reward, OR）配合正常提示（Normal System Prompt, NS）在所有 GRPO 配置中取得了最佳的准确率-鲁棒性权衡，辩论式系统提示（DS）或辩论式奖励（DR）并未带来额外增益。

## 实验与分析

### 核心瓶颈：社交融洽偏误的系统性损害

KAIROS 基准的核心发现是：LLM 在多智能体社交环境中普遍存在“融洽偏误”（Rapport Bias），即模型极易受历史交互中建立的融洽关系及当前同伴行为的影响。即使同伴提供明显错误的答案，模型也倾向于从众，导致大量原本正确的预测被放弃，而纠正错误的能力却远不足以弥补损失。这一不对称损害是模型社交脆弱性的根本原因。

从抵抗性（Resistance）与利用性（Utility）的对比中可以清晰看到这一机制：抵抗性转变平均约占 65.1%，而利用性转变的比例远低于此。更重要的是，模型在社交互动中损失的正确预测始终超过其纠正的错误——**Figure 3** 中展示的抵抗性损失（$p_c(1 - R_M)$）与利用性增益（$p_i U_M$）的对比直接验证了这一点。这意味着即使模型偶尔能从同伴处获得有用信息，其净效应仍是准确率的系统性下降。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/008_Figure_3.jpg]]
*Figure 3: The comparison between the loss of correct predictions ( p _ { c } ( 1 - R _ { M } ) ) against the gains from correcting errors ( p _ { i } U _ { M } ) . Each pair of bars corresponds to a different model variant under the MAS-NS-OR setting*

### 模型规模：调节社会敏感性的首要因素

**Table 1** 的结果揭示了模型规模对社会鲁棒性的决定性影响。在基础设置（Base）下，小模型（≤32B）的平均 O–K Δ 为 **-5.65%**，而大模型（>32B）为 **-3.64%**，差距约 2 个百分点。这表明大模型天然具备更强的社交干扰抵抗力。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/005_Table_1.jpg]]
*Table 1: Evaluation of model robustness under KAIROS. The table summarises Original and KAIROS accuracies and their relative O–K ∆ (percentage change) across multiple model families, sizes, over prompting strategies. The maximum and minimum O–K ∆ values are highlighted in bold. Table 2: Comparison of Original accuracy, KAIROS accuracy, and O–K ∆ across different models and mitigation configurations. For each model family, all SFT and GRPO variants are fine-tuned from the same Base checkpoint, enabling consistent comparison of how prompting, SFT, and GRPO influence robustness under social interaction*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/004_Table_1.jpg]]

授权提示（Empowered Prompting）进一步放大了这一规模效应。该类提示鼓励模型自信决策、批判性评估同伴回应。在此策略下：
- 大模型的 O–K Δ 从 -3.64% **转为 +0.12%**，即社交互动反而略微提升了性能，鲁棒性缺口被有效弥合。
- 小模型却恶化至 **-11.25%**，表明简单的提示工程非但无法帮助小模型，反而使其在面对社交压力时更加脆弱。

反思提示（Reflective Prompting）的效果更差，小模型的 KAIROS 准确率进一步下降约 2.83 个百分点，说明在首轮回答后再进行自我反思并不能有效纠正社交干扰引入的错误。

### GRPO 训练：准确率提升与鲁棒性代价的权衡

**Table 2** 汇总了监督微调（SFT）与多种 GRPO 变体的训练结果。GRPO 训练整体上显著优于 SFT：平均 Original 准确率提升 **+12.3%**，KAIROS 准确率提升 **+16.4%**。然而，不同 GRPO 配置的鲁棒性表现差异巨大，揭示了准确率与社交鲁棒性之间的根本性张力。

#### 最佳权衡配置：MAS + 正常提示 + 结果奖励

在所有 GRPO 变体中，**GRPO-MAS-NS-OR**（多智能体上下文 + 正常系统提示 + 结果导向奖励）取得了最佳的准确率-鲁棒性权衡：

| 模型 | Original 准确率 | KAIROS 准确率 | O–K Δ |
|------|----------------|---------------|-------|
| Qwen2.5-3B | — | 57.9% | — |
| Qwen2.5-14B | 76.4% | 71.5% | **-6.5%** |

对于 Qwen2.5-14B，O–K Δ 为 -6.5%，相比 Base 的 -8.7% 改善了 2.2 个百分点。Qwen2.5-3B 的 KAIROS 准确率达到 57.9%，较 Base 的 48.8% 提升 9.1 个百分点。这一配置的关键在于：**加入多智能体上下文（MAS）** 使模型在训练中暴露于社交动态，从而习得一定的鲁棒性；而**使用正常提示（NS）而非辩论式提示（DS）** 和**简洁的结果奖励（OR）** 避免了过度约束模型推理过程。

#### 消融分析：各设计选择的独立影响

**多智能体上下文（MAS）的加入**：平均而言，MAS 训练比无 MAS（nonMAS）变体提升鲁棒性约 **+1%**（O–K Δ 改善）。但这一效应存在显著的规模依赖性：小模型（3B）在 MAS 下鲁棒性反而下降约 4%，而大模型（14B）则获得约 4% 的增益。这表明小模型可能缺乏足够的认知容量来有效整合社交上下文信息。

**辩论式提示与奖励的无效性**：辩论式系统提示（DS，要求结构化内部辩论）和辩论式奖励（DR，结合正确性、格式和内在声音多样性）并未带来任何额外增益。NS-OR 配置在所有 GRPO 变体中持续取得最高的 Original（65.6%）和 KAIROS（60.7%）准确率。辩论式推理反而可能引入不必要的复杂性，干扰模型在社交环境中的决策。

**数据过滤策略的陷阱**：
- **仅对低置信度样本训练（LConf）**：虽能提高表面准确率，但鲁棒性变差（O–K Δ 更负），因为模型在自身不确定时反而更容易被同伴误导。
- **仅对原本错误样本训练（LCorr）**：导致严重的性能坍塌，Qwen2.5-14B 的 O–K Δ 可达 **-33.3%**。这表明仅针对错误案例进行纠偏训练会破坏模型原有的正确判断能力。

### 训练削弱了模型从同伴处学习的能力

**Figure 4** 揭示了训练策略的一个隐性代价：抵抗性转变的置信度从 Base 的 0.882 下降到 SFT 的 0.807，再下降到 GRPO 的 0.715；而利用性转变的置信度更是从 Base 的 0.584 急剧下降到训练后的 **0.207**。这意味着虽然 GRPO 训练提高了表面准确率，但模型在社交环境中做出正确判断时的内在确信度显著降低，且几乎丧失了从同伴有用信息中获益的能力。模型变得“固执但脆弱”——在抵抗误导时不够坚定，在接纳帮助时又过于封闭。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/009_Figure_4.jpg]]
*Figure 4: Average “Resistance” and “Utility” proportion across different model configurations, with bar hatching distinguishing the two metrics and colour intensity encoding each configuration’s mean confidence. Family groups models—Qwen 2.5-3B, Qwen 2.5-7B, Qwen 2.5-14B, Llama 3-2.3B, and Llama 3-8B—and include the original Base, SFT, and GRPO variants. Vertical dashed lines demarcate each model family*

### 失败模式与局限

1. **小模型的双重困境**：小模型既缺乏大模型的天然社交鲁棒性，又无法从授权提示中获益，甚至 MAS 训练也可能适得其反。当前缓解策略对小模型的适用性存在明显断层。

2. **训练策略的鲁棒性代价**：所有 GRPO 变体（除 GRPO-MAS-NS-OR 外）均在不同程度上牺牲了鲁棒性以换取准确率。LCorr 配置的 -33.3% O–K Δ 是这一权衡极端化的典型案例。

3. **利用性能力的丧失**：训练后利用性置信度降至 0.207，表明模型几乎不再能从同伴的正确建议中学习。这违背了多智能体协作的基本目标——模型应能区分并采纳有用信息。

4. **MCQ 格式的保守性**：附录 F.1 的开放生成实验（Table 5）显示，开放格式下的社交脆弱性远大于 MCQ 设置。例如 Qwen2.5-3B 的 Original 准确率从 MCQ 的 47.93% 骤降至开放格式的 15.64%，且 O–K 差距进一步扩大。当前基于 MCQ 的评估结果应被视为社会脆弱性的**保守下界**。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/010_Table_5.jpg]]
*Table 5: Comparison of model performance under MCQ and open-ended formats. Open-ended generation substantially reduces base accuracy and amplifies susceptibility to peer influence (O–K), indicating that the MCQ setting provides a conservative lower bound on social vulnerability*

### 任务维度的鲁棒性差异

**Table 4** 按推理、知识、社交、创意四个维度分解了鲁棒性表现。创意和社交理解领域展现出最大的性能波动，这与这些领域固有的主观性和上下文依赖性一致。推理类任务相对稳定，但即使在高度结构化的数学推理中，社交干扰仍能造成显著的准确率损失。这一维度分析表明，融洽偏误并非局限于特定任务类型，而是跨领域的系统性现象。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/007_Table_4.jpg]]
*Table 4: Evaluation of model robustness under KAIROS. The table summarises Original and KAIROS accuracies and their relative O–K ∆ (percentage change) across multiple model families, sizes, and training strategies over four task dimensions. For each dimension, the maximum and minimum O–K ∆ values are highlighted in bold*

### 补充图表

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/006_Table_3.jpg]]
*Table 3: Illustrative examples of reward components*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/011_Table_6.jpg]]
*Table 6: Effect of historical question confidence on susceptibility to peer influence. Conformity rates (O–K) remain stable across high- and low-confidence histories, indicating that intrinsic difficulty does not modulate social susceptibility*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/012_Table_7.jpg]]
*Table 7: Correct-to-Correct (C→C) transition rates for Qwen2.5–7B. Masked history reveals a strong default-conformity baseline. Real history systematically modulates resistance based on peer reliability, demonstrating that models interpret interaction history as a trust signal*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/013_Table_8.jpg]]
*Table 8: Overall results for the Reasoning category under KAIROS. Bold numbers mark per-dataset extreme (max/min) O–K ∆*

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_gF31wuYdk7/figures/014_Table_9.jpg]]
*Table 9: Overall results for the Knowledge category under KAIROS. Bold numbers mark per-dataset extreme (max/min) O–K ∆*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

KAIROS 的定位处于 LLM 社会智能评估与多智能体交互研究的交叉地带，其核心贡献在于首次系统性地将“融洽关系”（rapport）作为可操纵变量引入评估框架。

**相对于社会影响与从众性研究。** 此前工作多聚焦于单轮同伴影响或固定的社会角色设定，未考虑历史交互积累的融洽关系对模型决策的调节作用。KAIROS 通过控制历史互动中同伴与模型回答的一致程度（融洽级别），并与当前回合的同伴行为（支持/强烈反对/轻微反对）交叉组合，构建了一个多维社会压力测试矩阵。这使得分析从“模型是否从众”深化为“模型在何种历史关系下、面对何种同伴行为时从众”。

**相对于多智能体评估基准。** 现有基准如 MMLU、BBH 等仅评估模型的孤立推理能力，而 KAIROS 将评估场景拓展至包括创造力与社会理解在内的四个任务维度，填补了社交干扰下模型鲁棒性评估的空白。与一般的多智能体对话框架不同，KAIROS 采用动态评估数据集构建策略：首先通过自一致性采样推断模型的原始信念和置信度，再基于该信念构造同伴的针对性回应，形成模型定制化的压力测试。

**相对于缓解策略研究。** 论文系统对比了三类缓解路径：提示工程（授权提示与反思提示）、监督微调（SFT）和基于组相对策略优化的强化学习（GRPO 及其变体）。其中，授权提示的设计思路与鼓励模型自信决策的提示策略一致，但 KAIROS 的评估揭示了一个关键发现：该策略对大小模型效果截然相反——大模型（>32B）的 O–K Δ 从 -3.64% 改善至 +0.12%，而小模型（≤32B）则从 -5.65% 恶化至 -11.25%（Table 1）。这种规模依赖的提示敏感性此前未被系统量化。

### 2. 方法适用边界

**评估范式的边界。** KAIROS 的评估全部基于多项选择题（MCQ）格式，这虽然便于精确控制社会压力变量，但可能低估模型在开放生成场景下的社会脆弱性。附录 F.1 的对比实验表明，开放生成格式下基础准确率大幅下降（如 Qwen2.5-3B 从 47.93% 降至 15.64%），且 O–K 差距进一步扩大，说明 MCQ 设置提供的是一个保守的下界估计。

**训练缓解的可扩展性边界。** 由于计算资源限制，SFT 和 GRPO 实验仅集中在 32B 以下的小模型上。大模型仅评估了提示策略，训练缓解策略在大规模模型上的可扩展性尚未验证。现有结果表明 MAS 上下文对小模型（3B）的鲁棒性平均下降约 4%，而大模型提升约 4%，这暗示规模与训练策略之间存在复杂的交互效应，直接外推需谨慎。

**社会交互的真实性边界。** 尽管 KAIROS 覆盖了创造力与社会理解场景，但代理之间的交互仍属于脚本化模拟：同伴回应基于预定义的行为类型（支持/反对）从模型信念分布中构造，而非真实的多轮协商与观点演化。研究仅分析了单轮次受同伴影响后的即时表现，未考虑多轮交互中状态动态演化的长期效应。

### 3. 局限与开放问题

**核心局限。** 除上述边界外，论文未讨论不同人口群体或文化背景下的公平性问题。训练数据的过滤策略（低置信度或低正确率样本过滤）可能引入采样偏差，且仅对低置信度样本训练虽提高表面准确率，鲁棒性反而恶化；仅对原本错误样本训练则导致严重性能坍塌（Qwen2.5-14B 下 O–K Δ 可达 -33.3%，Table 2）。

**开放问题。**

- **内部信号机制不明。** 模型的内在置信度（预测熵）在高/低置信度历史下几乎不影响从众率（Table 6），模型究竟依赖何种内部信号来权衡同伴建议，目前尚不清楚。

- **训练与可靠性的悖论。** GRPO 训练虽整体提升准确率（Original +12.3%，KAIROS +16.4%），但抵抗性转变的置信度从基线的 0.882 持续下降至 GRPO 的 0.715，而利用性转变的置信度从 0.584 急剧下降至 0.207（Figure 4）。这意味着训练在提高表面准确率的同时，削弱了模型从同伴处学习有用信息的能力，也降低了其坚持正确判断的信心。如何设计奖励机制使模型既能利用有用信息、又能安全地摒弃误导性输入，而非仅偏向结果正确，是亟待解决的问题。

- **大规模验证缺失。** 更大规模模型（>32B）的 GRPO 训练是否能复现小模型的关键发现，尤其是 MAS 上下文对大模型的鲁棒性增益，尚需验证。

- **跨文化扩展性。** 该评估框架是否能扩展到多语言、多文化背景，以研究不同社会规范下的融洽偏误，仍有待探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Measuring_and_Mitigating_Rapport_Bias_of_Large_Language_Models_under_Multi_Agent_Social_Interactions.pdf]]
