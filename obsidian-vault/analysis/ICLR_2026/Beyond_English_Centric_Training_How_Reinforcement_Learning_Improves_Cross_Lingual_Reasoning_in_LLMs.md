---
title: "Beyond English-Centric Training: How Reinforcement Learning Improves Cross-Lingual Reasoning in LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_English_Centric_Training_How_Reinforcement_Learning_Improves_Cross_Lingual_Reasoning_in_LLMs.pdf
project_link: null
code_link: null
openreview_forum_id: hdrG6SaTcA
aliases:
- BECTHRLICLRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "强化学习（RL）中的采样驱动探索与优化机制，以及由此产生的推理过程中的语言不一致性（模型在推理时不一定遵循训练语言），是提升跨语言推理泛化的关键调节因素。"
primary_logic: "强化学习通过奖励引导的探索，使模型学习到不依赖于特定语言的鲁棒推理策略，从而在跨语言泛化上显著优于SFT；并且，在非英语数据上进行RL训练能更有效地激发模型的潜在推理能力，挑战了以英语为中心的训练范式。"
claims:
- "RL在MGSM上的平均准确率比SFT高17.5–25.2个百分点，且泛化得分（Gen）大幅领先。"
- "非英语RL训练（如德语）系统性地优于英语RL训练，例如RL（De）在MGSM上平均准确率71.5% 对比RL（En）62.7%。"
- "强制语言一致性会严重损害RL模型的跨语言推理性能，表明语言不一致性是RL泛化优势的重要来源。"
- "RL在跨任务泛化上同样表现出优势，例如在MMLU-ProX-Lite和MGPQA-D上SFT出现负迁移，而RL维持正向泛化。"
---

# Beyond English-Centric Training: How Reinforcement Learning Improves Cross-Lingual Reasoning in LLMs

> [!tip] 核心洞察
> 强化学习通过奖励引导的探索，使模型学习到不依赖于特定语言的鲁棒推理策略，从而在跨语言泛化上显著优于SFT；并且，在非英语数据上进行RL训练能更有效地激发模型的潜在推理能力，挑战了以英语为中心的训练范式。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越以英语为中心的训练：强化学习如何提升大语言模型的跨语言推理能力 |
| 英文题名 | Beyond English-Centric Training: How Reinforcement Learning Improves Cross-Lingual Reasoning in LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hdrG6SaTcA) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | 基于GRPO的跨语言推理强化学习训练 |
| Dataset | MGSM, MMath500, MMLU-ProX-Lite, MGPQA-D |

> [!tip] 效果简介
> - MGSM 上，平均准确率 (Avg Accuracy) 为 RL (De): 71.5%，对比 SFT (De): 46.3%，变化 +25.2%。
> - MMath500 上，平均准确率 (Avg Accuracy) 为 RL (Zh): 61.3%，对比 SFT (Zh): 39.8%，变化 +21.5%。
> - MMLU-ProX-Lite 上，泛化得分 (Gen) 为 RL (De): 30.8，对比 SFT (De): 8.0，变化 +22.8。

## 概要

### 问题背景

大语言模型（LLM）的推理能力在监督微调（SFT）范式下取得了显著进展，但其跨语言泛化能力始终面临瓶颈。SFT通过模仿专家推理轨迹来提升模型表现，然而这种模仿学习方式容易使模型过拟合于训练语言的特定模式，缺乏充分的探索与泛化能力。当训练数据以英语为中心时，模型在非英语语言上的推理性能往往大幅衰减，这限制了LLM在全球多语言场景中的实际应用。

### 核心发现

本文首次系统性地对比了强化学习（RL）与监督微调在跨语言推理泛化上的表现，揭示两个关键发现：

1. **RL在跨语言推理泛化上全面优于SFT**。在数学推理（MGSM、MMath500）、常识推理（MMLU-ProX-Lite）和科学推理（MGPQA-D）等多个基准上，RL训练的模型在非训练语言上的准确率提升比SFT高出17.5–25.2个百分点（Table 1），且泛化得分（Gen）大幅领先。SFT在跨任务场景下甚至出现负迁移，而RL始终保持正向泛化优势（Table 3）。

2. **非英语数据在RL训练中比英语数据更有效**。这一发现挑战了以英语为中心的训练范式：使用德语数据进行RL训练（RL-De）在MGSM上平均准确率达71.5%，显著优于英语RL训练（RL-En）的62.7%（Table 7, Table 14）。类似地，中文RL训练同样展现出跨语言泛化优势。

### 机制洞察

分析表明，RL的跨语言泛化优势源于三个关键机制：

- **语言不一致性**：RL训练使模型在推理时自然地混合使用多种语言，这种语言不一致性对跨语言泛化具有促进作用。实验显示，强制语言一致性会严重损害RL模型的性能（Figure 2, Table 6）。
- **采样驱动的策略优化**：RL通过在线采样探索多样化解法路径，而仅使用正确答案进行SFT（RFT）无法达到RL的性能水平（Figure 3, Figure 5），证明负样本探索对泛化至关重要。
- **语义空间偏移**：RL训练后模型隐层表征发生有利于泛化的偏移，且这种偏移在引入语言约束后减弱（Figure 4, Table 10）。

### 方法定位

本研究提出的方法属于**基于GRPO的跨语言推理强化学习训练**，其核心改变是将训练范式从SFT的模仿学习切换为RL的奖励驱动探索。相较于SFT的最大似然估计优化，RL通过最大化期望奖励（以答案准确性为核心信号）引导模型自主发现不依赖于特定语言的鲁棒推理策略。该方法在Qwen2.5-3B-Base、SmolLM3-3B和Qwen2.5-7B等多个基座模型上均验证了有效性（Table 4, Table 13），展现出模型规模无关的鲁棒性。



大语言模型（LLM）在推理能力上取得了显著进展，但这一进步主要集中在英语场景。当面对非英语语言时，即便经过多语言预训练，模型的推理性能仍会出现明显下降。现有的跨语言推理增强方法主要依赖监督微调（SFT），通过模仿专家链式推理路径来提升目标语言的推理能力。然而，SFT的本质缺陷在于：它通过最大似然估计拟合训练数据的分布，容易过拟合于训练语言的特定推理模式，缺乏对多样化推理路径的探索能力，导致跨语言泛化受限。

强化学习（RL）为这一问题提供了新的视角。RL通过奖励驱动的探索与优化机制，允许模型在训练过程中主动采样和评估多种推理路径，而非被动模仿固定轨迹。这种范式差异构成了本文的核心动机：**RL能否突破SFT的跨语言泛化瓶颈？**

本文首次系统性地探究了RL与SFT在跨语言推理泛化上的差异。研究以Qwen2.5-3B-Base为基础模型，覆盖数学推理、常识推理和科学推理等多类型多语言基准。核心发现揭示了两个反直觉的现象：

1. **RL在跨语言推理上系统性地优于SFT**，在MGSM基准上平均准确率提升达17.5–25.2个百分点（Table 1），且泛化得分（Gen）大幅领先。

2. **非英语数据训练的RL模型反而优于英语数据训练的RL模型**。例如，德语RL训练（RL (De)）在MGSM上平均准确率达71.5%，而英语RL训练（RL (En)）仅为62.7%（Table 7, Table 14）。这一发现直接挑战了“以英语为中心”的训练范式。

为解释上述现象，本文进一步从三个机制层面展开分析：推理过程中的语言不一致性、采样驱动的策略优化，以及训练后的语义空间偏移。这些分析共同指向一个核心洞察：RL通过奖励引导的探索，使模型学习到不依赖于特定语言的鲁棒推理策略，而非英语数据在此过程中能够更有效地激发模型的潜在推理能力。



## 核心方法与创新机理

本研究的核心创新在于**用强化学习的探索机制替代监督微调的模仿范式，以解决跨语言推理中的泛化瓶颈**。相比于已有工作，这一创新体现在以下四个关键维度的“changed slots”上。

### 训练范式：从模仿学习到奖励驱动的探索

监督微调（Supervised Fine-Tuning, SFT）通过最大化专家推理轨迹的似然来提升模型能力，本质上是一种模仿学习。然而，该方法使模型容易过拟合于训练语言的特定推理模式，缺乏探索多样化解题路径的能力。

本研究将训练范式从SFT切换为基于GRPO算法的强化学习（Reinforcement Learning, RL）。在RL框架下，模型不再被动模仿固定的推理链，而是通过**在线采样**从当前策略生成多条回复，并由**准确率奖励函数** $r_{\text{acc}}$ 引导优化方向。这一改变使得模型能够主动探索更广泛的解空间，学习到不依赖于特定语言的鲁棒推理策略。实验证据表明，这一范式转换带来了显著的性能跃升：在MGSM基准上，RL的平均准确率比SFT高出17.5至25.2个百分点（Table 1），泛化得分（Gen）也大幅领先。

### 推理语言约束：从语言一致到语言不一致

SFT训练后的模型倾向于在推理过程中保持与训练数据一致的语言输出。本研究的关键发现是，**RL训练天然地打破了这一语言一致性约束**，使模型在推理时混合使用多种语言，而这种“语言不一致性”恰恰是跨语言泛化能力的重要来源。

通过消融实验，作者验证了这一机制：当通过一致性提示（Consistency Prompt）或一致性奖励（$r_{\text{consistency}}$）强制模型保持语言一致时，RL模型的跨语言推理性能出现大幅下降（Figure 2, Table 6）。具体而言，未约束的RL（Zh）模型在MMath500上的中文一致性为0.0%，但平均准确率达到61.3%；而施加一致性约束后，准确率降至53.7%。这表明，**语言不一致性是RL泛化优势的关键调节因素**，而非需要消除的缺陷。

### 优化目标：从似然最大化到期望奖励最大化

SFT的优化目标是最小化交叉熵损失，即最大化下一token预测的似然。本研究将其替换为RL框架下的期望奖励最大化目标，采用GRPO算法进行策略优化。

在语言一致性实验中，整体奖励函数被设计为准确率奖励与语言一致性奖励的组合：
$$r_{\text{overall}} = 0.5 r_{\text{acc}} + 0.5 r_{\text{consistency}}$$
其中 $r_{\text{consistency}}$ 通过 `langid` 工具检测生成回复的主语言来计算（Section 4.1, Equation 1）。这一奖励设计使得研究者能够精确控制语言一致性对模型性能的影响，从而揭示出奖励信号的结构对跨语言泛化的深远影响。

### 采样与探索：从静态样本到在线策略采样

SFT仅使用预先提供的静态训练样本，缺乏对模型自身生成能力的利用。本研究引入**在线策略采样机制**：在每次迭代中，以温度1.0、top-p 0.95的参数从当前策略采样多条回复，同时包含正确和错误的样本（Section 3.1, Section A.2.1）。

为隔离采样机制的贡献，作者设计了拒绝采样微调（Rejection Sampling Fine-Tuning, RFT）作为消融基线：仅使用RL训练后模型生成的正确答案进行SFT。结果显示，RFT的性能（MGSM平均准确率66.8%）虽优于SFT（46.3%），但仍显著低于RL（71.5%）（Figure 3）。这证明**RL的在线采样和负样本探索对性能至关重要**，单纯的正确答案蒸馏无法复现RL的泛化优势。

### 非英语RL训练的系统性优势

一个反直觉的发现是，**非英语数据上的RL训练系统性地优于英语RL训练**。例如，德语RL训练在MGSM上达到71.5%的平均准确率，而英语RL训练仅为62.7%（Table 7, Table 14）。这一现象挑战了“以英语为中心”的训练范式，表明特定非英语语言能更有效地激发模型的潜在跨语言推理能力。值得注意的是，混合多语言训练（En+Zh+De）的RL模型性能（Avg 68.1%）仍低于单语言德语RL，进一步凸显了非英语单语言训练的独特价值。

### 冷启动的局限性

进一步的消融实验显示，在RL之前进行SFT预训练（冷启动策略）往往导致最终性能下降。特别是短步SFT（100步）后再进行RL训练，反而损害了模型性能（Table 15）。这一现象暗示SFT可能将模型引入语言相关的局部最优，限制了RL的探索空间，从而削弱了其跨语言泛化潜力。



本工作构建了一套系统的跨语言推理训练与评估框架，旨在对比监督微调（SFT）与强化学习（RL）两种范式在跨语言泛化能力上的差异，并揭示其背后的关键机制。框架以预训练基座模型为起点，通过统一的训练数据、一致的训练步数和标准化的评估协议，确保方法比较的公平性。

### 训练管线

训练管线包含两个核心分支：SFT 分支与 RL 分支，二者共享相同的基座模型和训练数据，但在优化目标、采样策略和探索机制上存在本质差异。

**基座模型与数据流**：所有实验均以 Qwen2.5-3B-Base 作为基座模型，并在 SmolLM3-3B-Base 和 Qwen2.5-7B-Base 上进行鲁棒性验证。训练数据采用 MGSM8K（每语言 8K 样本）或 LUFFY（每语言 45K 样本）的翻译版本，翻译质量与 MGSM8K-Instruct 可比（Table 12）。数据以单语言（英语、中文或德语）或混合多语言形式输入，分别考察不同训练语言对跨语言泛化的影响。

**SFT 分支**：采用 LLaMAFactory 框架实现，使用学习率 $2 \times 10^{-5}$、余弦学习率调度器、批次大小 32，训练 3 个完整 epoch。SFT 通过最大似然估计（交叉熵损失）模仿专家链式推理路径，属于静态的模仿学习范式，无显式在线采样机制。

**RL 分支**：采用 verl 平台实现 GRPO 算法，使用统一超参数：学习率 $1 \times 10^{-6}$、rollout 批次大小 512、采样温度 1.0、top-p 0.95、KL 散度系数 0.001，同样训练 3 个完整 epoch。RL 的核心差异在于：
- **在线采样**：每次迭代从当前策略采样多条回复，探索多样化解法路径，同时利用正负样本进行策略优化；
- **奖励驱动**：以答案准确性（$r_{\text{acc}}$）作为主要奖励信号，引导模型学习不依赖于特定语言模式的鲁棒推理策略。

**消融变体**：为隔离各组件的影响，框架还包含以下变体：
- **RFT**：对 RL 训练后的模型进行多次采样，仅保留正确答案样本进行 SFT，用于隔离在线采样与负样本探索的贡献；
- **冷启动**：先进行 SFT 预训练（完整 3 epoch 或仅 100 步），再进行 RL 训练，用于考察 SFT 预训练是否限制 RL 的探索空间；
- **语言一致性约束**：在 RL 训练中引入组合奖励 $r_{\text{overall}} = 0.5 r_{\text{acc}} + 0.5 r_{\text{consistency}}$（其中 $r_{\text{consistency}}$ 通过 langid 检测回复主语言），或通过提示词强制语言使用，用于分析语言不一致性对泛化的因果作用。

### 评估管线

评估管线覆盖多语言数学推理、常识推理和科学推理任务，采用零样本设置（辅以 4-shot 鲁棒性验证），确保评估的标准化与可复现性。

**评估基准**：
- **MGSM**：10 种语言的数学推理基准，作为主要测试平台；
- **MMath500**：6 种语言的数学推理基准，用于跨数据集验证；
- **MMLU-ProX-Lite / MGPQA-D**：跨任务泛化测试，涵盖常识与科学推理；
- **Multilingual LogiQA**：多语言逻辑推理基准。

**核心指标**：
- **平均准确率**：所有测试语言上的算术平均准确率；
- **泛化得分（Gen）**：衡量微调模型在所有测试语言上相对于基座模型的归一化提升，定义为：
  $$\text{Gen}(M_{\text{tuned}}) = \frac{1}{|L|} \sum_{l \in L} \frac{\text{Acc}(M_{\text{tuned}}, l) - \text{Acc}(M_{\text{base}}, l)}{1 - \text{Acc}(M_{\text{base}}, l)}$$
  取值范围为 $(-\infty, 1]$，正值表示正向泛化，负值表示负迁移。

### 机制分析管线

为解释 RL 跨语言泛化优势的来源，框架设计了三个层次的机制分析：
1. **语言一致性分析**：统计模型在推理过程中使用训练语言的比例（通过 langid 检测），结合强制语言一致的消融实验，揭示语言不一致性与泛化性能的关系；
2. **采样机制隔离**：通过 RFT 与 RL 的对比，分离在线采样和负样本探索的独立贡献；
3. **语义空间偏移分析**：提取最终层隐状态，计算 RL 与基座模型的差向量 $\mathbf{h}_{\text{diff}} = \mathbf{h}_{\text{RL}} - \mathbf{h}_{\text{Base}}$，通过 PCA 降维可视化，量化不同训练配置下的语义空间偏移程度。

### 公平性保障

为确保 SFT 与 RL 比较的公平性，框架在以下维度进行了严格对齐：
- 训练数据量完全一致，使用相同的翻译版本；
- 训练步数统一为 3 个完整 epoch；
- RL 采用统一的超参数配置；
- 评估以零样本为主，同时提供少样本结果作为稳健性验证；
- 在 3B 和 7B 两种参数规模上验证结论的模型无关性。



### 泛化得分（Generalization Score）

为量化微调模型在跨语言场景下的泛化能力，本文定义了归一化的泛化得分：

$$
Gen(M_{\mathrm{tuned}}) = \frac{1}{|L|} \sum_{l \in L} \frac{\operatorname{Acc}(M_{\mathrm{tuned}}, l) - \operatorname{Acc}(M_{\mathrm{base}}, l)}{1 - \operatorname{Acc}(M_{\mathrm{base}}, l)}
$$

其中，$L$ 表示所有测试语言的集合，$\operatorname{Acc}(M, l)$ 为模型 $M$ 在语言 $l$ 上的准确率。该指标衡量微调模型在所有测试语言上相对于基座模型的归一化提升，取值范围为 $(-\infty, 1]$。当基座模型在某语言上已达满分时，分母为零，该语言不纳入计算。

### RL 奖励函数

#### 基础奖励

在标准 GRPO 训练中，奖励仅基于最终答案的正确性：

- **$r_{\mathrm{acc}}$**：答案准确性奖励，通过比对模型生成的最终答案与标准答案给出二值或连续奖励。

#### 组合奖励（语言一致性实验）

在分析语言不一致性对泛化影响的消融实验中，引入语言一致性奖励，并与准确性奖励组合：

$$
r_{\mathrm{overall}} = 0.5 r_{\mathrm{acc}} + 0.5 r_{\mathrm{consistency}}
$$

- **$r_{\mathrm{consistency}}$**：语言一致性奖励，使用 `langid` 检测生成回复的主语言，当回复主语言与训练数据语言一致时给予正向奖励，否则惩罚。该奖励的核心目的是强制模型在推理过程中保持语言一致性，以观察其对泛化性能的影响。

### 表征偏移向量

为分析 RL 训练带来的语义空间变化，提取模型最后一层的隐状态，计算 RL 模型与基座模型之间的差异向量：

$$
\mathbf{h}_{\mathrm{diff}} = \mathbf{h}_{\mathrm{RL}} - \mathbf{h}_{\mathrm{Base}}
$$

随后通过 PCA 将高维隐状态投影至二维空间，可视化不同训练配置下语义空间的偏移程度与方向。该分析用于探究语言一致性约束对模型内部表征稳定性的影响。

### 训练管线关键模块

| 模块 | 功能 | 关键配置 |
|------|------|----------|
| **GRPO Trainer** | 在线策略强化学习优化器，基于 verl 平台实现 GRPO 算法 | lr=1e-6, rollout batch=512, KL 系数=0.001 |
| **Sampling Module** | 每次迭代从当前策略采样多条回复，探索多样化解法路径 | 温度 1.0, top-p 0.95 |
| **Accuracy Reward** | 基于最终答案正确性计算奖励 | 比对模型输出与标准答案 |
| **Language Consistency Reward** | 基于 `langid` 检测回复主语言，强制语言一致性（仅消融实验） | 与 $r_{\mathrm{acc}}$ 等权组合 |
| **Base Model** | 预训练基座模型（如 Qwen2.5-3B-Base），提供初始隐层特征 | 冻结或全参数训练 |



## 实验与关键发现

### 核心发现一：RL 在跨语言推理上系统性地优于 SFT

在 MGSM 基准上，RL 训练模型在所有 10 种测试语言上均显著优于 SFT 训练模型。以中文训练为例，RL（Zh）的平均准确率达到 66.0%，而 SFT（Zh）仅为 46.9%，提升幅度达 +19.1 个百分点；泛化得分（Gen）方面，RL（Zh）为 52.6，SFT（Zh）仅 20.4（Table 1）。当使用德语数据进行训练时，RL（De）的平均准确率进一步攀升至 71.5%，相比 SFT（De）的 46.3% 提升了 +25.2 个百分点，这一结果在 Table 7 中得到完整呈现。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/003_Table_1.jpg]]
*Table 1: Performance of base, SFT, and RL models on MGSM. “Base” denotes Qwen2.5-3B-Base. “SFT (zh)” and “RL (zh)” indicate tuning on Chinese data. We report accuracy on 10 linguistic settings; ∆ (RL–SFT) denotes the performance gap. Each value is averaged over six runs.$^ { \mathrm { \bullet } } \mathrm { A v g } ^ { \mathrm { \bullet } }$ and “Gen” refer to the mean accuracy and generalization score, respectively

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/013_Table_7.jpg]]
*Table 7: Performance of base model, SFT, and RL tuning models on MGSM. Base denotes the original Qwen2.5-3B-Base model. SFT (zh) and RL (zh) mean we tune the base model in Chinese data through SFT and RL, respectively. We report the accuracy score on 10 linguistic settings. ∆ (RL-SFT) represents the performance difference between RL and the corresponding SFT score. Each score represents the average accuracy over six measurements. Avg represents the average of the scores of 10 language settings and Gen represents the generalization score*

这一优势在跨数据集验证中保持稳健。在 MMath500 上，RL（Zh）平均准确率为 61.3%，SFT（Zh）为 39.8%（+21.5 个百分点，Table 2）；在跨任务泛化测试中，RL 同样展现出正向迁移能力——MMLU-ProX-Lite 上 RL（De）的 Gen 得分为 30.8，而 SFT（De）仅为 8.0；MGPQA-D 上 RL（De）的 Gen 得分为 7.1，SFT（De）则出现负迁移（-13.9，Table 3）。这表明 SFT 在跨任务场景下容易过拟合于训练任务的特定模式，而 RL 学习到了更通用的推理策略。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/005_Table_3.jpg]]
*Table 3: Performance comparison on MMLU-ProX-Lite and MGPQA-D. “Avg” denotes the average score across languages (En/Zh/De), and “Gen” represents the generalization score*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/004_Table_2.jpg]]
*Table 2: Performance of base, SFT, and RL models on MMath500. We report the accuracy score on 6 linguistic settings*

### 核心发现二：非英语 RL 训练系统性地优于英语 RL 训练

一个反直觉的发现是，使用非英语数据进行 RL 训练比使用英语数据更能激发模型的跨语言推理潜力。Table 7 显示，RL（De）在 MGSM 上的平均准确率为 71.5%，而 RL（En）仅为 62.7%，差距达 8.8 个百分点；RL（Zh）为 66.0%，同样高于 RL（En）。这一趋势在 SmolLM3-3B-Base 上得到复现：RL（De）平均准确率 69.9%，RL（En）为 64.6%（Table 4）；在 Qwen2.5-7B-Base 上，RL（De）同样优于 RL（En）（Table 13），验证了结论的模型规模无关性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/006_Table_4.jpg]]
*Table 4: Performance of base model, SFT, and RL tuning models on MGSM. Base denotes the original SmolLM3-3B-Base model. We report the accuracy score on 10 linguistic settings*

进一步的混合语言训练实验表明，将英语、中文、德语数据混合进行 RL 训练（RL Mix）的平均准确率为 68.1%，虽然优于 RL（En），但仍低于单语言 RL（De）的 71.5%（Table 14）。这说明特定非英语单语言数据在 RL 框架下具有独特优势，而非简单的数据量增加所能替代。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/022_Table_14.jpg]]
*Table 14: Performance of base model, SFT, and RL tuning models on MGSM. Base denotes the original Qwen2.5-3B-Base model. Mix means using the mixture of English, Chinese and German data to tune the base model*

### 机制分析一：语言不一致性是 RL 泛化优势的关键因素

RL 模型在推理过程中表现出显著的语言不一致性——即模型生成的推理链不一定使用与训练数据相同的语言。Table 6 显示，未加约束的 RL（Zh）和 RL（De）模型在 MMath500 上的语言一致性均为 0.0%，表明模型在推理时几乎完全偏离了训练语言。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/008_Table_6.jpg]]
*Table 6: Language consistency of models on MMath500. We test 6 times and report the average percentage of language consistency*

为验证语言不一致性的因果作用，研究者通过两种方式强制语言一致性：（1）在训练和推理时使用约束提示（Consistency Prompt）；（2）在奖励函数中引入语言一致性奖励 $r_{\mathrm{overall}} = 0.5 r_{\mathrm{acc}} + 0.5 r_{\mathrm{consistency}}$。结果如 Figure 2 所示：RL（Zh）的平均准确率从 61.3% 骤降至 53.7%；RL（De）从 61.4% 降至 60.5%（仅提示约束），进一步降至 52.0%（提示+奖励约束）。Table 9 的完整数据显示，强制语言一致性在所有测试语言上均导致性能下降，且约束越强，性能损失越大。这表明语言不一致性并非 RL 训练的副作用，而是其跨语言泛化能力的重要来源。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/007_Figure_2.jpg]]
*Figure 2: Scores on MMath500. The chart compares the average accuracy of different models. “RL (Zh)” indicates training on Chinese data*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/017_Table_9.jpg]]
*Table 9: Performance of models on MMath500. “RL (zh)” denotes the model trained with Reinforcement Learning on Chinese data. “+ Consistency Prompt” indicates the addition of language control prompts during both the training and the inference. “+ Consistency Prompt and Reward” further incorporates a language consistency reward into the training objective. “+ Inconsistency Prompt and Reward” incorporates the inconsistency prompt and inconsistency reward into the training objective. We report the accuracy score on 6 linguistic settings. We test 6 times and report the average accuracy scores and pass@k scores*

### 机制分析二：在线采样与负样本探索至关重要

为隔离 RL 中采样机制的影响，研究者引入了拒绝采样微调（Rejection Sampling Fine-Tuning, RFT）：使用 RL 训练后的模型进行多次采样，仅保留正确答案的样本进行 SFT。Figure 3 显示，在德语训练设置下，Base 模型平均准确率为 45.8%，SFT 为 46.3%，RFT 提升至 66.8%，而 RL 达到最高的 71.5%。RFT 虽然优于 SFT，但仍显著低于 RL，说明 RL 的优势不仅来自正确答案的利用，更来自训练过程中对负样本（错误推理路径）的在线探索。GRPO 算法通过持续从当前策略采样多样化的回复，使模型能够从错误中学习，避免陷入 SFT 的局部最优。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/009_Figure_3.jpg]]
*Figure 3: Model performance comparisons among the Base, SFT, RFT, and RL models on MGSM. We use German data in LUFFY in SFT, RL, RFT for training*

### 机制分析三：RL 训练带来更稳定的语义空间偏移

通过提取模型最后一层隐状态并投影到二维 PCA 空间，研究者分析了不同训练配置下的语义偏移特征。Figure 4 和 Table 10 显示，未约束的 RL（De）模型在不同语言输入上的隐状态分布保持相对紧凑，而加入语言一致性约束（+Prompt 和 +Prompt+Reward）后，模型中心距离和偏移距离均增大，语义空间变得更加分散。这表明强制语言一致性破坏了 RL 自然形成的稳定跨语言语义表征，从表示层面解释了性能下降的原因。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/018_Table_10.jpg]]
*Table 10: Numerical results corresponding to Figure 4, reporting the model center distance and shift distance under different RL configurations*

### 冷启动策略的负面影响

SFT + RL 的冷启动策略（先进行 SFT 预训练再进行 RL）并未带来性能提升，反而可能损害最终效果。Table 15 显示，RL（De）的平均准确率为 71.5%，而 SFT + RL（De）仅为 52.6%；即使只进行 100 步 SFT 后再 RL，性能也降至 67.9%。这表明 SFT 可能使模型过早收敛到与特定语言相关的局部最优，限制了 RL 阶段的探索空间，进一步支持了 RL 从基座模型直接训练的必要性。

### 跨模型与跨任务鲁棒性验证

主要发现在多个维度上得到验证：
- **模型规模**：Qwen2.5-7B-Base 上 RL 相比 SFT 平均提升 18–24 个百分点，非英语 RL 优势同样存在（Table 13）。
- **模型架构**：SmolLM3-3B-Base 上 RL（De）相比 SFT（De）提升约 26–35 个百分点（Table 4）。
- **少样本设置**：4-shot 评估下 RL 仍显著优于 SFT，趋势与零样本一致（Table 16）。
- **推理任务类型**：在逻辑推理任务 Multilingual LogiQA 上，RL（De）平均准确率 47.6%，SFT（De）仅 25.9%（+21.7 个百分点，Table 18）。

### 公平性保障说明

所有对比实验均在严格控制下进行：SFT 和 RL 使用相同的数据量（MGSM8K 每语言 8K 样本或 LUFFY 每语言 45K 样本），训练均为 3 个完整 epoch；RL 采用统一的超参数（学习率 1e-6，批次大小 512，温度 1.0，KL 系数 0.001）；翻译质量与 MGSM8K-Instruct 可比（Table 12）；评估以零样本为主，同时提供 4-shot 结果作为稳健性验证。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_hdrG6SaTcA/figures/014_Table_8.jpg]]
*Table 8: Performance of base model, SFT, and RL tuning models on MAIME2024. Base denotes the original Qwen2.5-3B-Base model. SFT (zh) and RL (zh) mean we tune the base model in Chinese data through SFT and RL, respectively. We report the Pass@16 score on 10 linguistic settings. ∆ (RL-SFT) represents the performance difference between RL and the corresponding SFT score*



## 定位与知识库关联

### 核心训练范式的转换

本工作将跨语言推理能力的提升从**模仿学习**范式迁移至**探索驱动优化**范式。监督微调（SFT）通过最大化专家链式推理路径的似然来学习，其本质是行为克隆——模型被训练为在给定问题下复现训练数据中的推理模式。然而，这种范式在跨语言场景中暴露出根本性瓶颈：SFT容易过拟合于训练语言的特定推理模式，缺乏对解空间的充分探索，从而限制了泛化能力。

强化学习（RL）通过GRPO算法引入了一种根本不同的优化机制。其关键差异体现在以下维度：

| 维度 | SFT（模仿学习） | RL（GRPO，探索驱动） |
|------|----------------|---------------------|
| **优化目标** | 最大化下一token预测似然（交叉熵损失） | 最大化期望奖励（答案准确性驱动） |
| **采样机制** | 无显式在线采样，使用静态训练样本 | 每次迭代从当前策略在线采样多条回复 |
| **信号来源** | 仅来自正例（专家轨迹） | 正负例混合，奖励信号引导策略改进 |
| **探索范围** | 受限于训练数据分布 | 温度1.0、top-p 0.95的随机采样，探索多样化解法路径 |

这一范式转换的因果效应在实验中得到了系统验证。在MGSM基准上，RL的平均准确率比SFT高出17.5–25.2个百分点（Table 1）；在MMath500上，RL（Zh）达到61.3%，而SFT（Zh）仅为39.8%（Table 2）。更重要的是，泛化得分（Gen）的差距更为显著——RL（Zh）的Gen为52.6，而SFT（Zh）仅为20.4（Table 1），表明RL不仅提升了绝对性能，更从根本上增强了模型的跨语言泛化能力。

### 与相关基线的消融关系

为隔离RL各组成部分的贡献，本工作设计了多层次的消融基线：

**拒绝采样微调（RFT）** 用于隔离在线采样与负样本探索的影响。RFT首先使用RL训练后的模型进行多次采样，然后仅用产生正确答案的样本进行SFT。这一设计将RL的采样能力与优化机制解耦。实验结果表明，RFT的性能介于SFT和RL之间——在MGSM上，SFT（De）为46.3%，RFT（De）为66.8%，RL（De）为71.5%（Figure 3）。这说明在线采样和正负例混合的优化过程各自贡献了RL优势的一部分，但两者结合才能达到最佳效果。

**冷启动策略（SFT + RL）** 用于检验SFT预训练是否能为RL提供更好的初始化。实验揭示了一个反直觉的发现：在RL之前进行SFT往往导致最终性能下降，尤其是短步SFT（100步）后再进行RL反而损害性能（Table 15）。这一现象表明，SFT可能将模型引入语言相关的局部最优，限制了RL的探索空间——这与RL的核心优势（通过探索突破局部最优）形成鲜明对比。

**语言一致性约束实验** 用于检验RL泛化优势是否依赖于推理过程中的语言不一致性。通过提示约束和一致性奖励强制模型在推理时保持单一语言，RL的性能出现显著下降——RL（De）在MMath500上的平均准确率从61.4%降至52.0%（Figure 2, Table 6）。这一定量证据表明，语言不一致性并非RL训练的副作用，而是其跨语言泛化优势的重要来源。

### 适用边界与局限

本工作的结论建立在以下实验条件之上，其适用边界需要审慎界定：

1. **任务类型的边界**：分析主要集中于数学推理任务（MGSM、MMath500、MAIME2024），虽然跨任务泛化实验（MMLU-ProX-Lite、MGPQA-D、Multilingual LogiQA）也展示了RL的优势，但这些任务的分析深度有限。在常识推理和科学推理场景中，RL的优势机制是否与数学推理一致，尚需更系统的验证。

2. **语言覆盖的边界**：实验覆盖了10种语言（MGSM）或6种语言（MMath500），但主要集中在高资源语言。低资源语言场景下RL的泛化行为尚未被充分探索——这是评估该方法普适性的关键缺口。

3. **模型规模与架构的边界**：结论在Qwen2.5-3B-Base、SmolLM3-3B-Base和Qwen2.5-7B-Base上得到验证（Table 4, Table 13），但在更大规模模型（>10B）上的泛化性尚待确认。不同架构家族（如非Qwen系列）是否同样适用，也需要进一步检验。

4. **机制分析的深度局限**：语言不一致性与泛化之间的因果关系虽有强相关性证据，但缺乏严格的因果干预实验（如反事实操控）。语义空间偏移的分析（Figure 4, Table 10）提供了初步观察，但偏移量与泛化性能之间的因果链条尚未建立。

### 开放问题

本工作揭示的现象引出若干待解决的核心问题：

1. **语言不一致性的最优程度**：RL模型在推理时自然产生语言混合，强制一致性则损害性能。是否存在最优的语言不一致程度？是否可以通过设计更精细的奖励机制（如软约束而非硬约束）来进一步激发泛化潜力？

2. **非英语优势的深层原因**：德语RL训练系统性地优于英语RL训练（MGSM上71.5% vs 62.7%，Table 7），这一现象挑战了“英语中心”的训练范式。其深层原因可能与预训练数据分布、语言结构特征或语义空间的几何性质有关，但当前分析尚未给出确切解释。

3. **过程奖励与多层级奖励**：当前RL仅使用基于最终答案准确性的奖励信号。在跨语言推理中，过程奖励（如推理步骤的正确性）或多层级奖励（如语言一致性、推理连贯性、答案正确性的组合）是否能进一步提升泛化能力，是一个值得探索的方向。

4. **低资源语言的泛化行为**：当前实验集中在高资源语言。RL在低资源语言上的表现是否同样优于SFT？非英语训练优势是否在低资源语言上依然成立？这些问题对于评估该方法的实际应用价值至关重要。

5. **语义空间稳定性的因果作用**：RL训练带来的语义空间偏移（Figure 4）与泛化性能之间的因果关系需要更严格的因果实验来确证。如果稳定性是泛化的原因而非结果，那么直接优化语义空间稳定性是否能成为新的训练目标？



## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_English_Centric_Training_How_Reinforcement_Learning_Improves_Cross_Lingual_Reasoning_in_LLMs.pdf]]
