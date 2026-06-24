---
title: "A Simple \"Motivation\" Can Enhance Reinforcement Finetuning of Large Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Simple_Motivation_Can_Enhance_Reinforcement_Finetuning_of_Large_Reasoning_Models.pdf
aliases:
- MERFM
- SMCERFLRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在训练提示中直接注入奖励函数的自然语言描述（即“动机”），使模型在生成时就能感知优化目标。"
primary_logic: "利用LLM强大的上下文学习能力，将可验证奖励函数的规则以自然语言形式嵌入训练提示，让模型同时从内在动机（提示理解）和外部奖励（RL信号）两个渠道对齐生成行为，从而显著提升强化微调的效率和效果。"
claims:
- "MeRF在K&K逻辑谜题上显著优于RLVR基线，且训练效率更高"
- "MeRF在Qwen2.5-7B-Instruct上K&K平均准确率从0.51提升至0.63，在Qwen2.5-14B-Instruct上从0.72提升至0.83"
- "MeRF在MATH基准上平均pass@1提升3.40%，pass@8提升4.50%"
- "MeRF在训练过程中保持更高的熵，表明其鼓励更多探索"
---

# A Simple "Motivation" Can Enhance Reinforcement Finetuning of Large Reasoning Models

> [!tip] 核心洞察
> 利用LLM强大的上下文学习能力，将可验证奖励函数的规则以自然语言形式嵌入训练提示，让模型同时从内在动机（提示理解）和外部奖励（RL信号）两个渠道对齐生成行为，从而显著提升强化微调的效率和效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 简单的“动机”提示即可增强大型推理模型的强化微调 |
| 英文题名 | A Simple "Motivation" Can Enhance Reinforcement Finetuning of Large Reasoning Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3owSlsYDQf) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Motivation-enhanced Reinforcement Finetuning (MeRF) |
| Dataset | K&K Logic Puzzles (Qwen2.5-7B-Base), K&K Logic Puzzles (Qwen2.5-7B-Instruct), K&K Logic Puzzles (Qwen2.5-14B-Instruct), K&K Logic Puzzles (DeepSeek-R1-Distill-Llama-8B) |

> [!tip] 效果简介
> - K&K Logic Puzzles (Qwen2.5-7B-Base) 上，平均准确率 为 0.42，对比 0.35，变化 +0.07。
> - K&K Logic Puzzles (Qwen2.5-7B-Instruct) 上，平均准确率 为 0.63，对比 0.51，变化 +0.12。
> - K&K Logic Puzzles (Qwen2.5-14B-Instruct) 上，平均准确率 为 0.83，对比 0.72，变化 +0.11。

## 概述

本文针对大型推理模型在“可验证奖励强化学习”（RLVR）范式下的核心瓶颈——模型在生成时对优化目标一无所知，仅通过稀疏的奖励信号间接学习，导致探索效率低下——提出了一种极其简洁的改进方法：**动机增强强化微调（MeRF）**。其核心思路是利用大语言模型（LLM）强大的上下文学习能力，将可验证奖励函数的自然语言描述（即“动机”）直接注入训练提示的系统消息中，使模型在生成过程中就能感知优化目标，从而同时从内在动机（提示理解）和外部奖励（RL信号）两个渠道对齐生成行为。

实验在逻辑推理（K&K Puzzles）和数学推理（AIME24/25, AMC23, MATH500）等多个基准上验证了MeRF的有效性。在K&K逻辑谜题上，MeRF在多个模型（Qwen2.5-7B/14B-Instruct, DeepSeek-R1-Distill-Llama-8B）上均显著优于RLVR基线，平均准确率提升7到12个百分点，且训练效率更高（例如，在140步时即达到基线280步的性能）。在MATH基准上，MeRF平均pass@1提升3.40%，pass@8提升4.50%。消融实验表明，MeRF的性能提升主要源于训练过程而非推理时的上下文学习；其在训练过程中保持更高的熵，表明动机鼓励了更多探索；模型甚至能够通过强化微调适应误导性动机，逐渐忽略错误信号。

## 背景与动机

大型语言模型（LLM）在推理任务上的强化微调（Reinforcement Finetuning, RFT）近期取得了显著进展，尤其是基于可验证奖励的强化学习（Reinforcement Learning with Verifiable Rewards, RLVR）范式。然而，当前RLVR范式存在一个根本性的瓶颈：模型在生成过程中对优化目标完全“无知”，只能通过碎片化的奖励信号间接学习目标。具体而言，RLVR以试错方式工作——模型生成一系列输出，奖励函数对这些输出进行评分，然后通过策略优化（如GRPO）更新模型参数。这种间接学习方式导致探索效率低下，尤其在奖励稀疏或任务复杂时，模型难以从有限的奖励信号中推断出全局优化目标，从而陷入局部最优。

现有方法的缺口在于，它们完全依赖外部奖励信号作为模型学习的唯一渠道，忽视了LLM自身强大的上下文学习（In-Context Learning）能力。LLM在推理时能够理解并遵循自然语言指令，但这一能力在RLVR的训练过程中未被有效利用——模型在训练时只看到任务问题，而不知道奖励函数的具体规则。

本文的动机是：能否在训练过程中直接“告诉”模型优化目标，让模型同时从内在动机（对提示的理解）和外部奖励（RL信号）两个渠道对齐生成行为？具体而言，作者提出**Motivation-enhanced Reinforcement Finetuning (MeRF)**方法，其核心洞察是：将可验证奖励函数的自然语言描述（即“动机”）直接注入训练提示的系统消息中，使模型在生成时就能感知优化目标。这一简单修改利用了LLM的上下文学习能力，将奖励函数的规则（如正确性评分和格式评分标准）以自然语言形式嵌入训练过程，从而让模型在生成时就有明确的优化方向。

MeRF的因果机制在于：动机提示为模型提供了一个明确的“游戏规则”描述，使模型在采样阶段就能生成更符合优化目标的输出，从而获得更高的初始奖励，进而加速策略优化过程。与标准RLVR相比，MeRF不改动强化学习算法（同样使用GRPO），仅改变训练提示的内容——在系统提示中增加奖励函数的自然语言描述。这种改动极其轻量，但实验证据表明其效果显著：在K&K逻辑谜题上，MeRF的验证准确率提升远超RLVR基线，且收敛速度更快（Figure 1）；在Qwen2.5-7B-Instruct模型上，平均准确率从0.51提升至0.63，在14B模型上从0.72提升至0.83（Table 1）；在MATH基准上，平均pass@1提升3.40%，pass@8提升4.50%（Table 2）。这些结果表明，通过简单的动机提示注入，可以显著提升强化微调的效率和效果。

## 核心创新

MeRF（Motivation-enhanced Reinforcement Finetuning）的核心创新在于识别并修复了当前RLVR范式中一个根本性的瓶颈：模型在生成时对优化目标一无所知，只能通过碎片化的奖励信号间接学习。这种间接学习方式导致探索效率低下，尤其在奖励稀疏时难以达到全局最优。

**因果旋钮**：MeRF将可验证奖励函数的自然语言描述（即“动机”）直接注入训练提示的系统消息中，使模型在生成时就能感知优化目标。这一简单修改利用了LLM强大的上下文学习能力，让模型同时从内在动机（提示理解）和外部奖励（RL信号）两个渠道对齐生成行为。

**Changed Slot**：唯一的改变是训练提示内容。基线RLVR仅包含系统指令和任务问题，不包含奖励函数描述；MeRF则在系统提示中直接注入奖励函数的自然语言描述，包括正确性评分和格式评分规则。所有K&K结果均在无动机的验证设置下报告，排除了推理时上下文学习的干扰。

**核心洞察**：MeRF通过将可验证奖励函数的规则以自然语言形式嵌入训练提示，让模型从“试错学习”转变为“目标感知学习”。分析表明（Figure 6），MeRF在训练过程中保持更高的熵，表明上下文动机鼓励了更多探索。Figure 15的注意力热图进一步证实，MeRF训练的模型在生成答案时显著关注动机标记（如“correct”、“score”、“format”、“exactly”），说明模型有效利用了动机信息。消融实验（Figure 8）显示，当动机与真实奖励函数一致时性能最佳；即使面对误导性动机，模型也能通过强化微调逐渐适应并忽略错误信号。

**证据强度**：核心证据来自Figure 1（K&K逻辑谜题上MeRF显著优于RLVR基线，且收敛更快）、Table 1（Qwen2.5-7B-Instruct上平均准确率从0.51提升至0.63，Qwen2.5-14B-Instruct上从0.72提升至0.83）和Table 2（MATH基准上平均pass@1提升3.40%，pass@8提升4.50%）。所有证据置信度≥0.95。

## 整体框架

MeRF（Motivation-enhanced Reinforcement Finetuning）的整体管道是对标准RLVR（Reinforcement Learning with Verifiable Rewards）范式的直接扩展。其核心改动仅在于**训练提示的内容**：标准RLVR在系统提示中仅包含系统指令和任务问题，不包含奖励函数描述；而MeRF则在系统提示中直接注入可验证奖励函数的自然语言描述，称为“动机”（motivation）。这一动机包含正确性评分规则和格式评分规则的文字说明。

MeRF的管道由三个核心模块组成：

1. **动机注入模块**：将奖励函数的自然语言描述嵌入训练提示的系统消息中。该描述明确说明了“什么是正确的答案”以及“如何正确格式化输出”，使模型在生成时就能感知优化目标，而非像标准RLVR那样只能通过碎片化的奖励信号间接学习。

2. **GRPO强化学习模块**：使用Group Relative Policy Optimization算法进行策略优化。对于每个输入问题，GRPO从旧策略 $\pi_{\theta_{old}}$ 中采样一组 $G$ 个输出 $\{y_i\}_{i=1}^G$，然后基于组内归一化的优势值进行策略更新。其目标函数为：

   $$\mathcal{L}_{GRPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{old}}(\cdot|x)} \left[\frac{1}{G} \sum_{i=1}^G \min(\rho_i A_i, \mathrm{clip}(\rho_i, 1-\varepsilon, 1+\varepsilon) A_i)\right] - \beta \mathbb{D}_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$$

   其中重要性比率 $\rho_i = \frac{\pi_\theta(y_i|x)}{\pi_{\theta_{old}}(y_i|x)}$，优势值 $A_i = \frac{r_i - \mathrm{mean}(\{r_1, r_2, \cdots, r_G\})}{\mathrm{std}(\{r_1, r_2, \cdots, r_G\})}$ 通过组内奖励归一化计算。

3. **可验证奖励函数模块**：基于规则验证的奖励函数，包含两个组成部分：(i) 正确性分数——验证答案是否与标准答案匹配；(ii) 格式分数——验证输出是否符合指定的格式要求（如将答案包裹在特定标记中）。

MeRF的输入输出流为：输入是一个包含系统提示（含动机描述）和任务问题的完整提示 → 模型生成一组候选输出 → 奖励函数模块对每个输出进行评分 → GRPO模块基于组内归一化优势更新策略参数。这一过程与标准RLVR的区别仅在于**训练提示的内容**：MeRF的提示中包含奖励函数的自然语言描述，而标准RLVR的提示中不包含。

值得注意的是，所有K&K逻辑谜题的验证结果均在**无动机的验证设置**下报告，排除了推理时上下文学习的干扰。实验表明，MeRF在训练过程中保持更高的熵（Figure 6），表明动机鼓励了更多的探索行为，这是其性能提升的关键机制之一。

## 核心模块与公式推导

MeRF的核心改动极为简洁：在RLVR训练过程中，将可验证奖励函数的自然语言描述直接注入到训练提示（prompt）的系统消息（system message）中，作为模型的“上下文动机”（in-context motivation）。这一修改使得模型在生成每个回答时，就能感知到优化目标的具体规则（如正确性评分和格式评分标准），从而将生成行为与奖励信号直接对齐。

### 强化学习算法：GRPO

MeRF采用Group Relative Policy Optimization（GRPO）作为强化学习算法。GRPO的核心特点是无需批评者（critic）网络，而是通过组内相对比较来估计优势。其训练过程为：对于每个问题 $x$，从旧策略 $\pi_{\theta_{old}}$ 中采样一组 $G$ 个输出 $\{y_i\}_{i=1}^G$，然后基于每个输出的奖励 $r_i$ 计算组内归一化优势。

**目标函数**：

$$
\mathcal{L}_{GRPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, \{y_i\}_{i=1}^G \sim \pi_{\theta_{old}}(\cdot|x)} \left[ \frac{1}{G} \sum_{i=1}^G \min\left( \rho_i A_i, \text{clip}(\rho_i, 1-\varepsilon, 1+\varepsilon) A_i \right) \right] - \beta \mathbb{D}_{KL}(\pi_\theta \| \pi_{\text{ref}})
$$

**重要性比率**：

$$
\rho_i = \frac{\pi_\theta(y_i|x)}{\pi_{\theta_{old}}(y_i|x)}
$$

该比率衡量当前策略相对于旧策略在输出 $y_i$ 上的概率变化。

**优势计算**：

$$
A_i = \frac{r_i - \text{mean}(\{r_1, r_2, \cdots, r_G\})}{\text{std}(\{r_1, r_2, \cdots, r_G\})}
$$

通过对组内奖励进行标准化得到每个输出的优势值，使得优势的正负和大小完全取决于该输出在组内的相对位置。

### 可验证奖励函数

奖励函数由两个可验证的规则组件构成：

1. **正确性分数（Correctness Score）**：基于答案是否与标准答案完全匹配给出二进制分数（正确为1，错误为0）。
2. **格式分数（Format Score）**：基于输出是否遵循预定义的格式规范（例如将最终答案包裹在特定标记如 `<answer>` 中）给出二进制分数。

这两个分数共同构成最终的奖励值 $r_i$。值得注意的是，这些规则以自然语言形式直接写入训练提示，使模型在生成时就能“看到”奖励函数的完整描述。

### 核心因果机制

MeRF的因果链并不依赖于新的公式推导，而是通过改变信息流来实现：在标准RLVR中，模型只能通过参数更新间接学习奖励模式；而MeRF通过上下文动机，让模型在生成每个token时就能直接利用奖励函数的自然语言描述。这种“内在动机”（提示理解）与“外部奖励”（RL信号）的双通道对齐，使模型能够更高效地探索奖励空间。实验证据（Figure 6）表明，MeRF在训练过程中保持更高的熵（entropy），说明上下文动机鼓励了更多的探索行为，这被确认为性能提升的关键机制。

## 实验与分析

### 主实验结果

**逻辑谜题（K&K Puzzles）**：MeRF在所有模型规模和指令微调阶段上均显著超越标准RLVR基线。在Qwen2.5-7B-Base上，平均准确率从0.35提升至0.42（+0.07）；在Qwen2.5-7B-Instruct上从0.51提升至0.63（+0.12）；在Qwen2.5-14B-Instruct上从0.72提升至0.83（+0.11）；在DeepSeek-R1-Distill-Llama-8B上从0.79提升至0.86（+0.07）。这些结果均在不包含动机提示的验证设置下报告，排除了推理时上下文学习的干扰。Figure 1展示了训练过程中验证准确率的动态对比：MeRF不仅最终性能更高，收敛速度也显著更快——在约140步时就已超过RLVR基线在280步时的最终性能（Figure 3）。

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/012_Figure_3.jpg]]
*Figure 3: Pass@k performance of MeRF and RLVR baseline during the training process (from 0 to 280 steps) on K&K Logic Puzzle. We compare the pass@1, pass@2, pass@4, and pass@8 performance at each step, where MeRF consistently outperforms the RLVR baseline in all metrics. More importantly, MeRF demonstrates a significant training efficiency over RLVR baseline, for example, achieving better pass@4 and pass@8 performance at step 140 than the final RLVR model (at step 280), while RLVR’s performance of pass@4 and pass@8 hardly improves after step 140*

**数学推理基准（MATH）**：在AIME24&25、AMC23和MATH500四个数据集上，MeRF在pass@1/2/4/8四个指标上均取得一致提升。平均而言，pass@1从33.38提升至36.78（+3.40%），pass@8从50.45提升至54.95（+4.50%）。值得注意的是，pass@8的提升幅度（4.50%）大于pass@1（3.40%），表明动机注入对提升模型生成多样性和候选集质量有更显著的效果。Figure 4显示在MATH500上RLVR基线的pass@8在80步后几乎停滞，而MeRF持续改善。

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/014_Figure_4.jpg]]
*Figure 4: Comparison of Pass@8 and Pass@1 performance of MeRF and RLVR baseline on MATH500 dataset during the training process. MeRF outperforms the RLVR baseline consistently in both pass@8 and pass@1 metrics, while RLVR pass@8 performance hardly improves after step 80, demonstrating the effectiveness of MeRF in improving the math reasoning capabilities of LLMs*

**额外任务泛化**：在CountDown数字组合任务上，MeRF同样在验证准确率和pass@4上优于RLVR基线（Figure 9）。在基于搜索引擎的智能体推理任务（Natural Questions数据集）上，MeRF也展现出更优性能（Figure 14），表明该方法可推广到更复杂的多步推理场景。

### 机制分析：为什么MeRF有效？

**探索效率提升**：训练过程中模型输出熵的对比（Figure 6）揭示了核心机制——MeRF在整个训练过程中保持比RLVR基线更高的熵。更高的熵意味着模型在生成时保持更大的多样性，即更积极的探索行为。这一发现与Figure 5和Figure 11中MeRF训练集正确率始终更高的观察一致：动机提示使模型在早期就能生成更多符合奖励函数的候选答案，从而获得更密集的有效奖励信号，加速策略收敛。

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/020_Figure_6.jpg]]
*Figure 6: Entropy of models during the training process. MeRF maintains a higher entropy than the RLVR baseline, indicating that MeRF encourages more exploration by the in-context motivation during the training process, which contributes to its improved performance*

**探索与性能的解耦**：通过对比实验（Figure 12），将RLVR基线的温度从1.0提升至1.2后，其熵确实提升至与MeRF相当的水平，但性能并未相应改善。这表明MeRF的性能提升不仅仅是“增加探索”所能解释的——动机提示提供的定向引导（即告诉模型“什么是对的”）使得探索更具目标性，而非盲目随机采样。

**训练过程的主导作用**：Figure 7验证了MeRF模型在有/无动机的验证设置下性能相当，说明性能提升主要来自训练过程中的参数更新，而非推理时上下文学习的直接贡献。这与Section 5的消融结论一致。

### 消融与边界条件

**动机质量的影响**：Figure 8（左图）对比了三种动机设置的效果：(1) 真实奖励函数动机（最佳性能）；(2) 次优动机（仅描述正确性分数，忽略格式要求）；(3) 对抗性动机（提供与真实奖励相反的评分规则）。真实动机效果最佳；次优动机仍优于无动机基线；对抗性动机在训练初期误导模型，但模型通过强化微调能够逐渐适应并忽略错误信号（Figure 10展示了多次运行中相似的不稳定学习动态，最终模型均恢复并超越初始性能）。

**奖励密度的影响**：Figure 13a显示，无论奖励函数是密集（每步评分）还是稀疏（仅最终结果评分），MeRF均一致优于RLVR基线，且优势在稀疏奖励场景下更为明显——这正是动机注入的核心价值所在：当外部奖励信号稀少时，内在动机（提示理解）提供了额外的优化导向。

**提示变体的鲁棒性**：Figure 13b验证了MeRF在不同提示模板变体下均一致优于RLVR基线，排除了提示工程偶然性的干扰。

### 失败模式与开放问题

**对抗性动机的适应机制**：虽然模型最终能适应对抗性动机，但训练过程出现明显的性能波动（Figure 10），且收敛速度慢于真实动机设置。这表明动机与真实奖励函数的一致性对训练效率有显著影响。注意力热图（Figure 15）显示，MeRF模型在生成最终答案时对动机标记（如“correct”、“score”、“format”）表现出显著注意力，且能区分真实动机与对抗性动机中的有用信息。

**温度与熵的局限**：单纯提高温度增加熵但无法提升性能（Figure 12），说明动机提示提供的“定向探索”信号是MeRF成功的关键，而非熵本身。

**泛化能力边界**：实验主要覆盖逻辑推理和数学任务，在代码生成、科学推理等更复杂场景上的表现有待验证。对于泛化能力较弱的模型，如何设计更有效的动机注入策略仍是一个开放问题。

### 补充图表

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/009_Table_1.jpg]]

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/010_Table_1.jpg]]
*Table 1: Performance comparison across models on tasks with varying difficulty by number of people of K&K Puzzles. MeRF demonstrates a significant improvement over the RLVR baseline in both in-domain and OOD scenarios. Notably, all the results are validated without in-context motivation*

![[assets/figures/papers/iclr26_0004_3owSlsYDQf_A_Simple_Motivation_Can_Enhance_Reinforcement_Fi/figures/011_Table_2.jpg]]
*Table 2: Comparison of RLVR baseline and MeRF across math reasoning datasets. Each dataset occupies one row, with both methods displayed in vertical blocks (pass@1/2/4/8). The last row summarizes the average performance*

## 方法谱系与知识库定位

MeRF（Motivation-enhanced Reinforcement Finetuning）的核心贡献在于揭示了一个被现有RLVR范式忽略的瓶颈：模型在生成时对优化目标一无所知，只能通过碎片化的奖励信号间接学习，导致探索效率低下，尤其在奖励稀疏时难以达到全局最优。MeRF的因果干预极为简洁——在训练提示中直接注入奖励函数的自然语言描述（即“动机”），利用LLM强大的上下文学习能力，让模型同时从内在动机（提示理解）和外部奖励（RL信号）两个渠道对齐生成行为。

**与基线的对比关系**：MeRF的直接基线是标准RLVR（Reinforcement Learning with Verifiable Rewards），两者的唯一区别在于训练提示内容——RLVR仅包含系统指令和任务问题，而MeRF额外注入了正确性评分和格式评分的自然语言描述。这一改变带来了系统性的性能提升：在K&K逻辑谜题上，MeRF在Qwen2.5-7B-Instruct上平均准确率从0.51提升至0.63（+23.5%），在Qwen2.5-14B-Instruct上从0.72提升至0.83（+15.3%）；在MATH基准上平均pass@1提升3.40%，pass@8提升4.50%（Table 2）。更重要的是，MeRF展现出显著的训练效率优势——在K&K任务上，MeRF在step 140时的pass@4和pass@8已超过RLVR最终模型在step 280时的表现，而RLVR在step 140后几乎不再提升（Figure 3）。这种效率提升的机制在于：动机注入使模型在训练过程中保持更高的熵（Figure 6），鼓励更多探索，从而避免过早陷入局部最优。

**与后续工作的关系**：MeRF为“提示工程+强化学习”的交叉方向提供了一个清晰的实证锚点。其核心洞见——将奖励函数以自然语言形式嵌入训练提示——可被视为一种轻量级的“可微分提示”替代方案，无需修改RL算法本身（采用GRPO），仅通过改变输入格式即可获得显著收益。这为后续研究打开了几个关键方向：一是动态动机的探索，即根据模型当前表现自适应调整动机内容，而非使用静态描述；二是将动机注入与更复杂的奖励塑造（如过程奖励模型）结合；三是将MeRF扩展到更复杂的多步推理任务（如代码生成、科学推理、智能体任务），论文已在基于搜索引擎的智能体推理任务上初步验证了泛化性（Figure 14）。

**适用边界与局限**：MeRF的适用条件依赖于两个前提：（1）任务具有可验证的奖励函数，能够用自然语言准确描述；（2）模型具备足够的上下文学习能力来理解并利用动机信息。对于泛化能力较弱的模型，如何高效实现RLVR并更好地利用上下文动机仍是开放问题。此外，MeRF中的动机在训练过程中是静态的，这限制了其自适应能力——当模型能力提升后，初始动机可能不再是信息最优的。论文通过对抗性动机实验（Figure 8, Figure 10）揭示了模型的鲁棒性：即使注入误导性动机，模型也能通过强化微调逐渐忽略错误信号并恢复性能，但这一过程伴随着不稳定的学习动态，且最终性能仍低于使用真实动机的MeRF。这表明动机的质量直接影响收敛速度和最终性能。

**开放问题**：（1）动态动机策略——如何根据模型当前策略的探索状态自适应调整动机内容，以实现更高效的探索-利用平衡？（2）弱泛化模型的动机注入——对于上下文学习能力有限的模型，是否需要更显式的动机编码方式（如结构化提示、示例引导）？（3）动机与奖励信号之间的交互机制——论文通过注意力热图（Figure 15）初步显示模型在生成答案时显著关注动机标记（如“correct”、“score”、“format”），但动机信息如何与GRPO的组内优势计算相互作用，从而影响策略梯度更新的方向，仍需更深入的理论分析。（4）MeRF在更广泛任务上的泛化性——目前实验主要基于逻辑推理和数学任务，在代码生成、科学推理、多模态推理等领域的表现有待验证。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Simple_Motivation_Can_Enhance_Reinforcement_Finetuning_of_Large_Reasoning_Models.pdf

![[paperPDFs/ICLR_2026/A_Simple_Motivation_Can_Enhance_Reinforcement_Finetuning_of_Large_Reasoning_Models.pdf]]
