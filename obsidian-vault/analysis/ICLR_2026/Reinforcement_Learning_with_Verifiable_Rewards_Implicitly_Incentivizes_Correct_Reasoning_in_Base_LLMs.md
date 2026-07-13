---
title: "Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reinforcement_Learning_with_Verifiable_Rewards_Implicitly_Incentivizes_Correct_Reasoning_in_Base_LLMs.pdf
project_link: null
code_link: null
openreview_forum_id: jGbRWwIidy
aliases:
- DDCDSPOGBR
- RLVRIICRBL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "RLVR 仅利用答案正确性作为奖励信号，但得益于预训练 LLM 的知识与逻辑先验（正确推理链推导出正确答案的概率 α 显著高于错误推理链的概率 β），在 GRPO 梯度更新中，正确推理链的期望优势为正、错误推理链的为负，从而隐式增加了正确推理链的生成概率。这一因果旋钮的关键在于答案奖励与预训练模型先验之间的相互作用。"
primary_logic: "即使 RLVR 仅提供答案正确性的二元奖励，预训练 LLM 内部的强先验使 GRPO 算法在优化奖励的同时，自然地引导模型产生更多正确的中间推理步骤。该效应可以通过新提出的 CoT‑Pass@K 指标（同时考核最终答案和推理链的正确性）得以显现，并解释了 RLVR 在数学和代码任务上扩展推理能力边界的根本原因。"
claims:
- "CoT‑Pass@K 在 AIME 2024 和 AIME 2025 上揭示了 RLVR 后模型（DAPO‑Qwen‑32B）与基座模型（Qwen2.5‑32B）之间显著且持续的差距，而传统 Pass@K 曲线则趋于重叠。"
- "定理 1 证明，在逻辑先验假设（α>β）下，GRPO 使正确推理链的期望优势为正、错误推理链的为负，从而单调增加正确推理链的生成概率。"
- "RLVR 训练动态显示，早在训练初期 P(CC|CA)（答案正确时推理链也正确的比例）就开始提升，表明优化奖励的同时自动提升了推理链的质量。"
- "仅使用 RLVR 模型生成的推理链进行 SFT，即可在 AIME 测试集上复现 RLVR 模型的 Pass@1 性能，印证推理链的内在质量得到根本提升。"
---

# Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs

> [!tip] 核心洞察
> 即使 RLVR 仅提供答案正确性的二元奖励，预训练 LLM 内部的强先验使 GRPO 算法在优化奖励的同时，自然地引导模型产生更多正确的中间推理步骤。该效应可以通过新提出的 CoT‑Pass@K 指标（同时考核最终答案和推理链的正确性）得以显现，并解释了 RLVR 在数学和代码任务上扩展推理能力边界的根本原因。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于可验证奖励的强化学习隐式激励基座大模型的正确推理 |
| 英文题名 | Reinforcement Learning with Verifiable Rewards Implicitly Incentivizes Correct Reasoning in Base LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jGbRWwIidy) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | DAPO (Decoupled Clip and Dynamic sAmpling Policy Optimization) 风格的 GRPO‑based RLVR |
| Dataset | AIME 2024, AIME 2025, LiveCodeBench v5, v6, LiveCodeBench‑v6 及难度子集, DAPO‑17k (训练集) |

> [!tip] 效果简介
> - AIME 2024, AIME 2025 上，CoT‑Pass@K (up to K=1024) 为 DAPO‑Qwen‑32B (post‑RLVR)，对比 Qwen2.5‑32B (base)，变化 显著且持续的提升（RLVR 曲线始终高于基线，差距不随 K 增大而缩小，而 Pass@K 曲线在高 K 处趋于相等）。
> - LiveCodeBench v5, v6 上，Pass@K 为 AceReason‑Nemotron‑7B (RLVR trained)，对比 DeepSeek‑R1‑Distill‑Qwen‑7B (distilled)，变化 在多数版本上展现 Pass@K 提升，尤其是在中等和困难题目上。
> - LiveCodeBench‑v6 及难度子集 上，Pass@K 为 Skywork‑OR1‑7B (RLVR trained)，对比 DeepSeek‑R1‑Distill‑Qwen‑7B (distilled)，变化 总体 Pass@K 提升，困难子集上尤为明显，证明了挑战性基准的重要性。

## 概要

### 问题瓶颈

大语言模型（LLM）在数学与代码推理任务上展现出令人瞩目的能力，但评估其推理质量的核心瓶颈长期被忽视：传统的 **Pass@K** 指标仅考核最终答案的正确性，无法捕捉中间推理链（Chain-of-Thought，CoT）的质量。基座模型可以通过生成错误推理链但偶然猜对答案的方式，在 Pass@K 曲线上追上甚至逼近经过强化学习训练的推理模型，从而掩盖了可验证奖励强化学习（RLVR）对真实推理能力的提升潜力。

### 核心发现

本文的核心洞察是：**即使 RLVR 仅以最终答案正确性作为二元奖励信号，预训练 LLM 内部的知识与逻辑先验仍能使优化过程隐式地激励正确推理**。具体而言，在 GRPO（Group Relative Policy Optimization）梯度更新中，正确的推理链推导出正确答案的概率（$\alpha$）显著高于错误推理链的概率（$\beta$），使得正确推理链的期望优势为正、错误推理链的期望优势为负，从而单调增加正确推理链的生成概率。这一效应通过新提出的 **CoT‑Pass@K** 指标得以显现——该指标同时考核最终答案与中间推理链的正确性，揭示了 RLVR 在数学和代码任务上扩展推理能力边界的根本原因。

### 方法定位

本文的方法属于 **基于 GRPO 的可验证奖励强化学习（RLVR）** 范式，采用 DAPO（Decoupled Clip and Dynamic sAmpling Policy Optimization）训练食谱。与依赖蒸馏或监督微调的方法不同，该方法仅需答案正确性的程序化二元奖励，无需人工标注推理链质量。为评估推理链正确性，本文构建了 **LLM‑as‑a‑CoT‑Judge** 多重验证系统，使用 DeepSeek‑R1‑0528‑Qwen3‑8B 等模型进行多次验证，并通过 Any‑correct、All‑correct、Majority‑correct 三种聚合策略降低假阳性与假阴性。

### 主要结果

在数学推理基准 AIME 2024 和 AIME 2025 上，CoT‑Pass@K 揭示了 RLVR 后模型（DAPO‑Qwen‑32B）与基座模型（Qwen2.5‑32B）之间显著且持续的差距，而传统 Pass@K 曲线在高采样数 K 下趋于重叠。在代码推理基准 LiveCodeBench 多个版本上，经 RLVR 训练的 AceReason‑Nemotron‑7B 相比其蒸馏前身 DeepSeek‑R1‑Distill‑Qwen‑7B 展现出明显的 Pass@K 提升。训练动态分析表明，早在训练初期，答案正确时推理链也正确的比例 P(CC|CA) 即开始提升，且仅使用 RLVR 模型生成的推理链进行监督微调（SFT）即可在测试集上复现 RLVR 模型的 Pass@1 性能，印证了推理链内在质量的根本提升。



### 推理能力评估的隐性危机

近年来，基于可验证奖励的强化学习（RLVR）在提升大语言模型推理能力方面取得了显著进展。然而，一个根本性的问题始终悬而未决：当仅以最终答案的正确性作为奖励信号时，模型究竟是在学习“正确地推理”，还是仅仅在“更准确地猜测”？

传统的评估范式以 Pass@K 为核心指标——给定一个问题，从模型中采样 K 条响应，只要其中至少有一条的最终答案正确，即视为成功。这一指标在代码生成等任务中具有天然的合理性，但在数学推理领域却暴露出一个关键的盲区：**Pass@K 无法区分“推理链正确且答案正确”与“推理链错误但答案巧合正确”这两种截然不同的情况**。基座模型完全可以通过产生大量包含逻辑漏洞或计算错误的推理链，却偶然命中正确答案，从而在 Pass@K 曲线上逼近甚至追上经过 RLVR 训练的模型。这种现象掩盖了 RLVR 对推理能力提升的真实程度，也使得学界对 RLVR 工作机制的理解长期停留在“调整已有推理路径的采样概率”这一表面解释上。

### 现有解释框架的局限

一种流行的假说认为，RLVR 并未赋予模型新的推理能力，而仅仅是重新分配了基座模型中已存在的正确与错误推理路径的采样权重。如果这一假说成立，那么 RLVR 的推理能力边界将完全受限于基座模型的先验知识——当采样预算 K 足够大时，基座模型理应能够覆盖所有正确的推理路径，从而在 Pass@K 上与 RLVR 模型持平。这一假说在 MATH-500、AMC23 等基准上得到了表面上的支持：基座模型在高 K 值下的 Pass@K 确实能够追上 RLVR 模型。

然而，这一假说无法解释一个更深层的现象：**即使在 Pass@K 曲线趋于重叠的基准上，RLVR 模型产生的推理链在逻辑结构、步骤完整性和错误模式上仍与基座模型存在本质差异**。这表明 Pass@K 作为一个评估工具，其灵敏度不足以捕捉 RLVR 带来的真实能力变化。真正的瓶颈在于缺乏对推理链正确性的严格评估，导致人们低估了 RLVR 隐式激励正确推理的潜力。

### 本文的核心动机

本文旨在从三个层面重新审视 RLVR 的工作机制：

1. **评估层面**：引入 CoT‑Pass@K 指标，将评估焦点从“答案是否正确”扩展至“推理链与答案是否同时正确”，从而揭示 RLVR 扩展推理能力边界的真实幅度。
2. **理论层面**：建立形式化框架，证明即使奖励信号仅依赖于答案正确性，只要基座模型具备合理的逻辑先验（正确推理链推导出正确答案的概率显著高于错误推理链），GRPO 梯度更新就会自然地提升正确推理链的生成概率。
3. **实证层面**：通过大规模推理链验证、训练动态分析以及 SFT 迁移实验，系统性地展示 RLVR 如何从根本上提升推理链的内在质量，而非仅仅优化采样策略。

这一研究路径的核心洞察在于：**预训练 LLM 内部蕴含的知识与逻辑先验，与 GRPO 算法的优势归一化机制之间存在着未被充分认识的协同效应**。理解并利用这一效应，不仅有助于更准确地评估 RLVR 的真实能力，也为设计更高效的推理增强方法提供了新的理论指引。



## 核心方法与创新机理

### 从 Pass@K 到 CoT‑Pass@K：揭示被掩盖的推理边界

本研究的首要创新在于指出传统评估范式对 RLVR 真实效果的遮蔽，并提出了对应的解决方案。传统上，人们依赖 **Pass@K**（在 K 次采样中至少有一次最终答案正确的概率）来衡量模型的推理能力。然而，这一指标存在根本缺陷：基座模型可能通过产生错误的中间推理链，却偶然猜对最终答案，从而在 Pass@K 曲线上追上经过 RLVR 训练的模型（Figure 2 上方行）。这种现象制造了一种错觉，即 RLVR 仅重新分配了基座模型中已有的推理路径的采样概率，而并未扩展其推理边界。

为穿透这一假象，本文提出了 **CoT‑Pass@K** 指标，其核心变更在于将评估条件从单一的“答案正确”扩展为“推理链与答案同时正确”。具体而言，该指标借助 **LLM‑as‑a‑CoT‑Judge** 系统（以 DeepSeek‑R1‑0528‑Qwen3‑8B 作为验证器），对每条推理链进行多次独立验证，并采用 Any‑correct、All‑correct、Majority‑correct 三种聚合策略来降低假阳性与假阴性。这一指标变更直接改变了实验结论的走向：在 AIME 2024 和 AIME 2025 上，CoT‑Pass@K 曲线揭示了 RLVR 模型（DAPO‑Qwen‑32B）与基座模型（Qwen2.5‑32B）之间持续且显著的差距，且该差距不随 K 增大而缩小（Figure 2 下方行），而传统 Pass@K 曲线在高 K 处趋于重叠。这一发现从根本上挑战了“RLVR 仅调整已有路径概率”的假说。

### 训练范式与奖励机制的理论重构

第二个关键创新在于为 RLVR 的有效性提供了严格的理论解释，将“答案奖励”与“推理链优化”之间的因果旋钮形式化。在训练范式层面，本文采用的 **DAPO 风格的 GRPO‑based RLVR** 并未引入任何显式的推理链奖励——奖励信号 $R(y_i)$ 完全由最终答案的正确性决定（二元可验证奖励）。然而，理论分析表明，预训练 LLM 内部存在一个关键的 **逻辑先验**（Logic Prior）：正确的推理链推导出正确答案的概率 $\alpha$ 显著高于错误推理链的概率 $\beta$，即：

$$P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1) = \alpha > P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0) = \beta$$

在这一假设下，**定理 1** 证明：在 GRPO 梯度更新中，正确推理链的期望优势为正（$\mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1] > 0$），而错误推理链的期望优势为负（$\mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0] < 0$）。这意味着，尽管奖励信号仅来自答案正确性，梯度更新却会单调地增加正确推理链的生成概率。这一理论框架将 RLVR 的成功归因于答案奖励与预训练模型内部知识先验之间的相互作用，而非任何显式的推理链监督。

### 推理链质量评估的方法论创新

第三个创新点在于引入了一套独立于奖励信号的推理链质量评估体系。本文通过 **SFT‑based CoT Quality Assessment** 方法，将不同 RLVR 训练阶段的模型生成的推理链作为监督微调数据，训练同一个基座模型（Qwen2.5‑32B），并以测试集上的 Pass@1 和 CoT‑Pass@K 作为推理链质量的代理指标。这一设计排除了 RLVR 训练过程中其他因素的干扰，直接衡量推理链本身的可学性与泛化价值。实验结果表明，仅使用 RLVR 模型生成的推理链进行 SFT，即可在 AIME 测试集上复现 RLVR 模型的 Pass@1 性能（Figure 6），这为“RLVR 从根本上提升了推理链质量”提供了独立证据，而非仅仅优化了采样策略。

### 从蒸馏模型到基座模型的范式迁移

在适用对象上，本文的另一个重要变更在于将 RLVR 的评估焦点从蒸馏模型（如 DeepSeek‑R1‑Distill‑Qwen‑7B）扩展至基座模型（如 Qwen2.5‑32B）。此前的工作多关注 RLVR 对已具备一定推理能力的蒸馏模型的增强效果，而本文通过 CoT‑Pass@K 指标证明，即使是从未经过推理专项微调的基座模型，RLVR 也能隐式地激励其产生更正确的推理链——这一效果在仅使用 Pass@K 时被完全掩盖。在代码领域，经 RLVR 训练的 AceReason‑Nemotron‑7B 相比其蒸馏前身 DeepSeek‑R1‑Distill‑Qwen‑7B 在 LiveCodeBench 多个版本上展现出明显的 Pass@K 提升（Figure 3），进一步验证了 RLVR 机制在不同模型起点上的普适性。

### 关键变更总结

| 变更维度 | 基线方案 | 本文方案 | 创新性质 |
|:---|:---|:---|:---|
| **核心评估指标** | Pass@K（仅考核最终答案正确性） | CoT‑Pass@K（同时考核推理链与答案正确性），结合 LLM‑as‑a‑CoT‑Judge 多重验证 | 方法创新：揭示被掩盖的推理边界 |
| **训练范式** | 预训练 / 监督微调（SFT），无显式奖励优化 | 基于 GRPO 的 RLVR，仅以答案正确性作为二元奖励 | 理论创新：证明隐式激励机制 |
| **理论框架** | 缺乏对 RLVR 工作机制的严格解释 | 基于逻辑先验假设的定理 1，证明 GRPO 梯度自然偏向正确推理链 | 理论创新：形式化因果旋钮 |
| **推理链质量评估** | 无独立于奖励信号的评估手段 | SFT‑based CoT Quality Assessment，以 SFT 后的泛化性能作为推理链质量的代理指标 | 方法论创新：解耦奖励与推理质量 |
| **适用对象** | 主要关注蒸馏模型 | 同时覆盖基座模型与蒸馏模型，证明 RLVR 对基座模型的隐式激励效果 | 范式迁移：扩展 RLVR 的适用范围 |



本文的研究框架围绕一个核心命题展开：**仅利用答案正确性作为奖励信号的强化学习（RLVR），能否隐式地激励基座大模型产生正确的中间推理链？** 为回答这一问题，作者构建了一个“理论分析—指标设计—实证验证”三位一体的研究管线，其模块关系与数据流如下。

### 核心组件与数据流

整个框架由五个关键模块串联而成：

1. **基座策略模型 (Base LLM Policy πθ)**  
   以 **Qwen2.5‑32B**（Qwen, 2024）作为策略模型。对于给定的输入问题 $q$（来自数学训练集 DAPO‑17k 或代码基准 LiveCodeBench），模型生成包含推理链 $c_i$ 和最终答案 $a_i$ 的完整响应 $y_i = (c_i, a_i)$。这是整个管线的起点，决定了初始推理路径的分布。

2. **可验证奖励模块 (Verifiable Reward Module)**  
   该模块根据最终答案 $a_i$ 的正确性，程序化地给出二元奖励 $R(y_i) \in \{0, 1\}$。对于数学问题，奖励来自整数答案的精确匹配；对于代码问题，奖励来自测试用例的执行结果。**关键设计在于：奖励信号完全不依赖推理链 $c_i$ 的质量**，仅反映最终输出的对错。

3. **GRPO 优势计算 (GRPO Advantage Computation)**  
   对每个问题 $q$，策略模型采样一组 $G$ 个响应 $\mathbf{Y} = \{y_1, \dots, y_G\}$。基于奖励 $R(y_i)$ 计算组内均值 $\mu_{\mathbf{Y}}$ 和标准差 $\sigma_{\mathbf{Y}}$，得到归一化优势估计：
   $$\hat{A}(y_i) = \frac{R(y_i) - \mu_{\mathbf{Y}}}{\sigma_{\mathbf{Y}}}$$
   这一步骤将绝对奖励转化为相对优势，是 GRPO 算法区分“好”与“坏”响应的核心机制。

4. **策略梯度更新 (Policy Gradient Update)**  
   使用 GRPO 优势进行 REINFORCE 式梯度更新：
   $$\nabla_\theta J(\theta) \approx \frac{1}{G} \sum_{i=1}^{G} \hat{A}(y_i) \nabla_\theta \log \pi_\theta(y_i \mid q)$$
   本文采用 **DAPO**（Decoupled Clip and Dynamic sAmpling Policy Optimization）风格的训练食谱（Yu et al., 2025）来稳定这一过程。**理论关键**在于：尽管奖励仅依赖答案正确性，但得益于预训练 LLM 的逻辑先验——正确推理链推导出正确答案的概率 $\alpha$ 显著高于错误推理链的概率 $\beta$（即 $\alpha > \beta$）——GRPO 梯度更新会使得正确推理链的期望优势为正、错误推理链的期望优势为负，从而**隐式地提升正确推理链的生成概率**（Theorem 1, Section 4）。

5. **推理链验证与评估系统 (CoT Verification & Evaluation)**  
   为观测上述隐式激励效应，作者引入了 **CoT‑Pass@K** 指标，并构建了 **LLM‑as‑a‑CoT‑Judge** 验证流水线：
   - 使用 **DeepSeek‑R1‑0528‑Qwen3‑8B**（以及 GPT‑oss‑20b/120b 作为对照）对每条推理链 $c_i$ 进行多次独立验证。
   - 输出三种聚合判据：**All‑correct**（所有验证均通过）、**Majority‑correct**（多数验证通过）、**Any‑correct**（任一验证通过），以此构成 CoT‑Pass@K 的阴影区间。
   - 多重验证设计使假阳性率按 $p_{\mathrm{fp}}^n$、假阴性率按 $p_{\mathrm{fn}}^n$ 指数级衰减（Appendix A.2）。

6. **SFT 质量评估 (SFT‑based CoT Quality Assessment)**  
   作为对推理链质量的独立验证，作者将不同 RLVR 训练检查点（或不同模型）生成的推理链作为监督微调（SFT）数据，从同一基座模型出发进行微调，并以测试集上的 Pass@1 和 CoT‑Pass@K 作为推理链质量的代理指标。这一模块排除了 RL 训练动态的干扰，直接衡量推理链本身的“可学性”与泛化价值。

### 模块间的逻辑闭环

上述模块形成一条完整的“生成—奖励—更新—评估”闭环：
- **训练侧**：模块 1→2→3→4 构成标准的 GRPO‑based RLVR 训练循环，仅依赖答案奖励驱动策略优化。
- **评估侧**：模块 5 独立于训练过程，通过 LLM‑as‑a‑CoT‑Judge 揭示传统 Pass@K 无法捕捉的推理链正确性提升。
- **验证侧**：模块 6 通过 SFT 迁移实验，证明 RLVR 模型产生的推理链具有内在的高质量，而非仅仅是 RL 训练中策略采样的偶然产物。

### 与传统框架的关键差异

| 维度 | 传统视角（如 Yue et al., 2025） | 本文框架 |
|------|-------------------------------|----------|
| 核心评估指标 | Pass@K（仅考核最终答案） | CoT‑Pass@K（同时考核答案与推理链） |
| 对 RLVR 的解释 | 仅重新分配基座模型中已存在的推理路径的采样概率 | RLVR 隐式激励正确推理，扩展了推理能力边界 |
| 训练范式 | 预训练 / SFT，无显式奖励优化 | GRPO‑based RLVR，仅使用答案正确性作为奖励 |
| 推理链质量验证 | 依赖间接推断 | 直接使用 LLM‑as‑a‑CoT‑Judge 多重验证 |

### 适用边界与局限

该框架的有效性依赖于两个关键前提：① **逻辑先验假设**（$\alpha > \beta$）在预训练 LLM 中成立；② 奖励信号可被程序化验证（数学整数答案、代码执行结果）。当基座模型的先验存在严重偏差，或任务无法提供可靠的可验证奖励时，框架的隐式激励机制可能失效。此外，LLM‑as‑a‑CoT‑Judge 的可靠性受验证器模型偏差影响，尽管多重验证策略可部分缓解，但无法完全消除系统误差。



### 问题建模与符号定义

RLVR 的核心流程从基座 LLM 策略 $\pi_\theta$ 开始。对于给定的输入问题 $q$，策略模型生成包含推理链 $c_i$ 和最终答案 $a_i$ 的完整响应 $y_i = (c_i, a_i)$。正确性通过两个二元指示函数定义（Equation 1）：

$$
\mathcal{T}_{\mathrm{CoT}}(c_i) = \begin{cases} 1 & \text{if } c_i \text{ is correct} \\ 0 & \text{otherwise} \end{cases}, \quad \mathcal{T}_{\mathrm{Ans}}(a_i) = \begin{cases} 1 & \text{if } a_i \text{ is correct} \\ 0 & \text{otherwise} \end{cases}
$$

其中 $\mathcal{T}_{\mathrm{CoT}}$ 评估推理链的正确性，$\mathcal{T}_{\mathrm{Ans}}$ 评估最终答案的正确性。在 RLVR 训练中，奖励信号仅由答案正确性决定：$R(y_i) = \mathcal{T}_{\mathrm{Ans}}(a_i)$，为二元可验证奖励。

### GRPO 优势计算与策略梯度

训练采用 GRPO（Group Relative Policy Optimization）风格的更新。对每个问题 $q$，采样一组 $G$ 个响应 $\mathbf{Y} = \{y_1, y_2, ..., y_G\}$，计算每个响应的归一化优势（Equation 2）：

$$
\hat{A}(y_i) = \frac{R(y_i) - \mu_{\mathbf{Y}}}{\sigma_{\mathbf{Y}}}, \quad \mu_{\mathbf{Y}} = \frac{1}{G}\sum_{j=1}^{G} R(y_j), \quad \sigma_{\mathbf{Y}} = \sqrt{\frac{1}{G}\sum_{j=1}^{G}(R(y_j)-\mu_{\mathbf{Y}})^2}
$$

其中 $\mu_{\mathbf{Y}}$ 为组内平均奖励，$\sigma_{\mathbf{Y}}$ 为标准差。优势 $\hat{A}(y_i)$ 衡量单个响应相对于组内平均水平的优劣：正确答案获得正优势，错误答案获得负优势。

策略梯度更新采用 REINFORCE 形式的估计（Equation 3）：

$$
\nabla_\theta J(\theta) \approx \frac{1}{G} \sum_{i=1}^{G} \hat{A}(y_i) \nabla_\theta \log \pi_\theta(y_i \mid q)
$$

该梯度通过增大正优势响应的对数概率、减小负优势响应的对数概率来优化策略。

### 隐式激励的核心机制：逻辑先验假设

RLVR 仅使用答案正确性作为奖励，却能隐式提升推理链质量，其理论根基在于**逻辑先验假设**（Equation 4）：

$$
P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1) = \alpha > P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0) = \beta
$$

该假设断言：正确的推理链推导出正确答案的概率 $\alpha$，显著高于错误推理链推导出正确答案的概率 $\beta$。这一先验源于预训练 LLM 在大量文本中习得的知识与逻辑一致性——尽管模型可能通过错误推理偶然猜对答案，但正确推理通往正确答案的概率系统性地更高。

### 定理 1：GRPO 隐式激励正确推理

基于逻辑先验假设，定理 1 给出了 GRPO 优势的期望性质（Equation 5）：

$$
\mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1] > 0, \quad \mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0] < 0
$$

**因果机制**：当 $\alpha > \beta$ 时，正确推理链更可能产生正确答案，从而在组内获得正优势；错误推理链更可能产生错误答案，获得负优势。策略梯度更新因此单调地提升正确推理链的生成概率，同时抑制错误推理链——尽管奖励信号从未显式知晓推理链的正确性。

这一机制的**瓶颈**在于：当某些错误推理链恰好产生正确答案时（概率为 $\beta$），它们也会获得正优势，从而被错误强化。这就是 DAPO 训练后期 $P(CA) \to 1$ 但 $P(CC|CA)$ 中位数仅约 0.7 的根本原因——奖励饱和使得剩余的错误推理链无法被区分和消除。

### 评估指标：从 Pass@K 到 CoT‑Pass@K

传统 Pass@K 仅考核最终答案正确性，无法区分“真正推理正确”与“错误推理但猜对答案”。为捕捉推理链质量，引入 CoT‑Pass@K。

定义每提示统计量（Section 5）：

$$
C = \sum_{i=1}^{G} \mathcal{T}_{\mathrm{Ans}}(a_i), \quad D = \sum_{i=1}^{G} \mathcal{T}_{\mathrm{CoT}}(c_i) \cdot \mathcal{T}_{\mathrm{Ans}}(a_i)
$$

其中 $C$ 为答案正确的响应数，$D$ 为推理链与答案同时正确的响应数。基于此，Pass@K 和 CoT‑Pass@K 的每提示估计分别为：

$$
\mathrm{Pass@K}^{(q)} = 1 - \frac{\binom{G-C}{K}}{\binom{G}{K}}, \quad \mathrm{CoT‑Pass@K}^{(q)} = 1 - \frac{\binom{G-D}{K}}{\binom{G}{K}}
$$

两者均从 $G$ 个响应中无放回采样 $K$ 个，估计至少有一个满足条件的概率。Pass@K 的条件是答案正确，CoT‑Pass@K 的条件是推理链与答案同时正确。CoT‑Pass@K 揭示了 Pass@K 掩盖的推理能力差距：基座模型在高 $K$ 时可通过多次猜测追上 RLVR 模型的 Pass@K，但 CoT‑Pass@K 持续显示显著差距。

### 推理链验证系统

CoT‑Pass@K 的实现依赖 LLM‑as‑a‑CoT‑Judge 验证系统。使用 DeepSeek‑R1‑0528‑Qwen3‑8B 作为验证器，对每条推理链进行多次独立验证，并采用三种聚合策略：

- **All‑correct**：所有验证均判定正确才标记为正确，假阳性率按 $p_{\mathrm{fp}}^n$ 指数衰减
- **Any‑correct**：任一验证判定正确即标记为正确，假阴性率按 $p_{\mathrm{fn}}^n$ 指数衰减
- **Majority‑correct**：多数验证判定正确才标记为正确，在假阳性与假阴性之间折中

三种策略构成 CoT‑Pass@K 图中的阴影区域，反映了验证不确定性的范围。使用不同验证器（DS‑8B、gpt‑oss‑20b、gpt‑oss‑120b）得到的趋势高度一致，验证了该系统的鲁棒性。



## 实验与关键发现

### 核心发现：RLVR 扩展了基座模型的推理边界

本节从数学推理与代码推理两个领域，系统展示 RLVR 如何超越传统 Pass@K 指标所暗示的能力上限。核心发现是：当使用同时考核最终答案与中间推理链正确性的 **CoT‑Pass@K** 指标时，RLVR 训练的模型相对于基座模型展现出持续且显著的推理优势，这一优势在传统 Pass@K 曲线趋于重叠的高采样预算下依然存在。

#### 数学推理：CoT‑Pass@K 揭示被掩盖的推理能力提升

Figure 2 在五个数学基准上对比了基座模型 **Qwen2.5‑32B**（Qwen, 2024）与经 DAPO 食谱 RLVR 训练的 **DAPO‑Qwen‑32B** 的表现。上半行展示传统 Pass@K：在 AIME 2024 和 AIME 2025 上，随着采样数 K 增大，基座模型的 Pass@K 曲线逐渐逼近甚至追平 RLVR 模型——这一现象曾被解释为“基座模型已具备所有正确的推理路径，RLVR 仅调整了采样概率”。然而，下半行的 CoT‑Pass@K 揭示了完全不同的图景：RLVR 模型的 CoT‑Pass@K 曲线始终显著高于基座模型，且差距不随 K 增大（至 1024）而缩小。这表明基座模型在高采样预算下追平 Pass@K 的机制是**产生错误推理链但偶然猜对答案**，而非真正具备正确推理能力。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/002_Figure_2.jpg]]
*Figure 2: Comparisons of Pass@K (the top row) and CoT-Pass@K (the bottom row) on five math benchmarks (different columns) to show how RLVR could improve base LLMs. Here the base LLM is Qwen2.5-32B, and the post-RLVR model is DAPO-Qwen-32B. For CoT-Pass@K, we perform multiple verifications for each CoT using DeepSeek-R1-0528-Qwen3-8B, and display the results determined by any-correct, all-correct, and majority-correct strategies, which constitute the shaded area in lower subplots*

在 MATH‑500 和 AMC23 上，基座模型的高 Pass@K 表现可能源于训练数据污染或题目本身较简单，使得仅凭答案正确性无法区分真实推理能力。这进一步印证了 CoT‑Pass@K 作为评估指标的必要性。

逐问题细粒度分析（Table 2 和 Table 3，使用 gpt‑oss‑120b 验证器，Majority‑correct 判据，N=1024）显示：在 AIME 2024 的 30 题中，RLVR 模型在 24 题上实现 CoT‑Pass@k=1，而基座模型仅 14 题；在 AIME 2025 上，RLVR 模型在多数题目上 #CC（同时具备正确推理链和正确答案的响应数）高达数百甚至上千，基座模型则普遍较低。这从题目级别确认了 RLVR 对推理链质量的根本性提升。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/036_Table_2.jpg]]
*Table 2: gpt-oss-120b verification results on AIME 2024. Metrics per problem are aggregated over N = 1024 CoTs using the Majority-correct criterion*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/037_Table_3.jpg]]
*Table 3: gpt-oss-120b verification results on AIME 2025. Metrics per problem are aggregated over N = 1024 CoTs using the Majority-correct criterion*

#### 代码推理：Pass@K 直接体现推理边界扩展

与数学推理不同，代码推理中 RLVR 的提升在传统 Pass@K 上即可直接体现。Figure 3 在 LiveCodeBench 六个版本上对比了蒸馏模型 **DeepSeek‑R1‑Distill‑Qwen‑7B**（Guo et al., 2025）与经 RLVR 训练的 **AceReason‑Nemotron‑7B**。RLVR 模型在多数版本上展现出清晰的 Pass@K 提升，尤其在中等和困难题目上更为显著。另一开源 RLVR 模型 **Skywork‑OR1‑7B**（He et al., 2025）在 LiveCodeBench‑v6 及困难子集上也相对于蒸馏基线展现了 Pass@K 增益（Figure 8），进一步验证了 RLVR 在代码领域扩展推理边界的普适性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/003_Figure_3.jpg]]
*Figure 3: Comparisons of Pass@K across six LiveCodeBench versions to show how much RLVR could enhance distilled LLMs. Here the distilled LLM is DeepSeek-R1-Distill-Qwen-7B, and the post-RLVR model is AceReason-Nemotron-7B*

代码与数学领域在指标敏感性上的差异，可能源于任务结构的不同：代码执行验证直接反馈执行正确性，而数学答案正确性允许更多的“猜测”空间。这一差异本身也暗示了 CoT‑Pass@K 在数学推理评估中的不可替代性。

---

### 训练动态：奖励优化与推理链质量提升的耦合

Figure 4 展示了 DAPO 训练过程中，训练集上答案正确率 P(CA) 与条件推理链正确率 P(CC|CA) 的演变。P(CA) 在训练早期快速趋近 1，表明模型迅速学会产生正确答案。与此同时，P(CC|CA) 的中位数从基座模型的极低水平（约 0.1）持续提升至约 0.7，说明**即使在答案正确率饱和后，推理链质量仍在持续改善**。这一动态直接印证了理论分析的核心论断：GRPO 在仅优化答案奖励的同时，隐式地增加了正确推理链的生成概率。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/004_Figure_4.jpg]]
*Figure 4: The evolution of P ( C A ) ^ { ( q ) } (the fraction of correct answers for prompt q) and P ( C C | C A ) ^ { ( q ) } (the fraction of correct CoTs within the correct answers for prompt q) for fully optimized training questions over the course of DAPO training*

Figure 5 展示了 AIME 2024 和 2025 上不同训练检查点的 Pass@K 与 CoT‑Pass@K 泛化曲线。RLVR 训练早期（步骤数较少时），模型在测试集上的 Pass@K 和 CoT‑Pass@K 即开始提升，表明推理能力的泛化改善与训练集上的奖励优化几乎同步发生。这一观察与定理 1 的“训练分布上的优化动力学”一致，但泛化本身仍仅由经验证据支持，理论上尚未提供形式化保证。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/005_Figure_5.jpg]]
*Figure 5: The evolution of Pass@K (the top row) and CoT-Pass@K (the bottom row) performance on AIME 2024 and 2025 for different model checkpoints during the DAPO training*

---

### 推理链质量评估：SFT 实验的因果证据

为进一步排除 RLVR 模型的高 CoT‑Pass@K 可能来自“强化学习阶段的搜索或采样策略”而非推理链本身质量提升的替代解释，作者设计了 SFT 评估实验（Figure 6）。核心思路是：从同一基座模型 **Qwen2.5‑32B** 出发，仅使用不同来源的推理链数据进行监督微调，以测试集 Pass@1 和 CoT‑Pass@K 作为推理链质量的代理指标。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/006_Figure_6.jpg]]

Figure 6(a) 显示，随着 RLVR 训练步数增加，使用对应检查点推理链进行 SFT 的模型在 AIME 测试集上的 Pass@1 单调提升，并最终追平 DAPO‑Qwen‑32B 自身的 Pass@1 性能。Figure 6(b) 进一步表明，仅使用 RLVR 模型生成的推理链进行 SFT，即可在 CoT‑Pass@K 上接近复现 RLVR 模型的表现，而使用基座模型自身推理链的 SFT 效果远逊于此。这一结果提供了强因果证据：**RLVR 从根本上提升了推理链的内在质量，而非仅改变了推理时的采样分布**。

---

### 验证器鲁棒性与推理链特征分析

CoT‑Pass@K 的可靠性依赖于 LLM‑as‑a‑CoT‑Judge 验证系统的准确性。Figure 11 展示了使用三种不同验证器（DS‑8B、gpt‑oss‑20b、gpt‑oss‑120b）在 AIME 24‑25 上得到的 CoT‑Pass@K 曲线，三者趋势高度一致，验证了评估系统的鲁棒性。更强大的验证器倾向于更严格的评判（CoT‑Pass@K 绝对值更低），但 RLVR 模型与基座模型之间的相对排序保持不变。

Figure 12 的验证器间相关性热图揭示了另一重要现象：基座模型产生的正确答案推理链中，不同验证器对其错误的判断一致性较高；而 RLVR 模型的推理链中，验证器间的一致性略低。这说明 RLVR 模型的错误推理链更为细微、更难以被一致识别，暗示随着推理链质量提升，评估本身也变得更加困难。

Table 1 对比了基座模型与 RLVR 模型在 DAPO‑17k 训练集上正确与错误推理链的长度分位数。RLVR 模型的推理链（无论正确与否）均显著长于基座模型。Figure 13 进一步显示，在 AIME 2025 上，RLVR 模型在正确答案推理链中的各类错误（计算错误、逻辑跳跃、符号误用等）频率均低于基座模型。这些结构性差异解释了为何即使被标记为“错误”的 RLVR 推理链，仍能通过 SFT 带来泛化性能提升——它们包含更多有效的逻辑片段和结构化推理模式。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/035_Table_1.jpg]]
*Table 1: Token-length quantiles of correct and incorrect CoTs for Qwen2.5-32B (base) and DAPO-Qwen-32B (RLVR) on DAPO-17k train set*

---

### 现有方法的瓶颈与失败模式

尽管 RLVR 展现出显著的推理能力提升，训练动态分析揭示了明确的瓶颈。Figure 4 显示，在 DAPO 训练后期，当 P(CA) 趋近 1 时，GRPO 优势估计中的组内方差消失，导致部分训练问题不再提供有效梯度信号。然而此时 P(CC|CA) 中位数仅约 0.7，意味着仍有约 30% 的正确答案伴随着错误推理链。**现有二元答案奖励机制无法进一步消除这些残留的错误推理链**，因为它们在奖励空间上与正确推理链不可区分。这一饱和现象构成了当前 RLVR 方法的根本性局限。

此外，在 MATH‑500 和 AMC23 等可能存在训练数据污染的基准上，基座模型的高 Pass@K 使得评估 RLVR 的真正增益变得困难。这提示需要开发更健壮、更少受数据污染影响的评估基准。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_jGbRWwIidy/figures/023_Figure_23.jpg]]
*Figure 23: (c) Generalization performance on AIME 2024 across different training steps*



## 定位与知识库关联

### 1. 核心方法定位：GRPO‑RLVR 与 DAPO 训练范式

本文的核心技术路线是**基于 GRPO 的可验证奖励强化学习**，具体采用 DAPO（Decoupled Clip and Dynamic sAmpling Policy Optimization）训练食谱。该范式在 RLVR 谱系中具有以下定位特征：

**训练范式变革**：传统基座大模型（如 **Qwen2.5‑32B**，Qwen, 2024）仅经过预训练或监督微调，缺乏显式的奖励优化机制。本文引入的 RLVR 训练仅使用**答案正确性的二元奖励**作为唯一奖励信号，通过 GRPO 优势估计进行策略梯度更新。这一设定与依赖过程奖励模型或蒸馏数据的方法形成根本差异——RLVR 不要求任何中间推理步骤的标注或奖励塑形。

**与蒸馏路线的对比**：在代码推理实验中，本文的基线模型 **DeepSeek‑R1‑Distill‑Qwen‑7B**（Guo et al., 2025）代表了当前主流的蒸馏路线——通过从更强的推理模型蒸馏来提升小模型的推理能力。本文训练的 **AceReason‑Nemotron‑7B** 和 **Skywork‑OR1‑7B**（He et al., 2025）则在蒸馏模型基础上进一步应用 RLVR，在 LiveCodeBench 多个版本上展现出超越纯蒸馏的 Pass@K 提升，表明 RLVR 能够扩展蒸馏模型已有的推理边界。

**评估范式的突破**：传统推理能力评估依赖 Pass@K 指标（仅考核最终答案正确性）。本文提出的 **CoT‑Pass@K** 指标同时考核最终答案与中间推理链的正确性，通过 LLM‑as‑a‑CoT‑Judge 系统实现自动化验证。这一评估框架的引入，使得 RLVR 对推理链质量的隐式提升得以被量化捕捉，而此前这类提升被 Pass@K 的“猜测效应”所掩盖。

### 2. 理论框架：逻辑先验假设与 GRPO 隐式激励

本文的理论贡献在于揭示了 RLVR 工作的**因果机制**，而非仅停留在经验观察层面。核心假设是**逻辑先验**：

$$P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1) = \alpha > P(\mathcal{T}_{\mathrm{Ans}}(a_i)=1 \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0) = \beta$$

即正确的推理链推导出正确答案的概率 $\alpha$ 显著高于错误推理链的概率 $\beta$。这一先验源于预训练 LLM 内部的知识与逻辑结构，是 RLVR 能够隐式激励正确推理的根本前提。

**定理 1** 证明，在该先验假设下，GRPO 梯度更新中正确推理链的期望优势为正、错误推理链的为负：

$$\mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=1] > 0, \quad \mathbb{E}[\hat{A}(y_i) \mid \mathcal{T}_{\mathrm{CoT}}(c_i)=0] < 0$$

这意味着即使奖励信号仅来自答案正确性，策略梯度仍会**单调增加正确推理链的生成概率**。这一机制解释了为何 RLVR 能够在优化奖励的同时，自然提升推理链的内在质量。

### 3. 适用边界与领域限制

**已验证的有效领域**：
- **数学推理**（整数答案）：基于 DAPO‑17k 训练集，在 AIME 2024/2025 上通过 CoT‑Pass@K 揭示了显著的推理边界扩展。训练数据仅限于数学领域且只接受整数答案，与 Minerva 等包含物理题或自由文本答案的基准存在 domain gap。
- **代码推理**（可执行验证）：在 LiveCodeBench 多个版本上验证了 RLVR 对蒸馏模型的有效提升。代码任务的答案可通过执行直接验证，奖励信号的可靠性高于数学推理中依赖 LLM 验证的设定。

**适用前提与限制**：
- **逻辑先验的依赖**：RLVR 的有效性依赖于基座模型具备足够强的知识与逻辑先验（$\alpha > \beta$）。若基座模型存在严重的系统性错误知识或偏差，RLVR 可能反而强化有害推理模式。文中未对此风险进行实证检测。
- **模型规模的局限**：实验主要基于 7B‑32B 规模的模型，向更大规模 LLM 或不同架构的推广需谨慎。定理 1 的证明未涉及模型规模的影响。
- **奖励饱和瓶颈**：DAPO 训练后期，答案正确率 P(CA) 趋近 1，部分训练问题不再提供有效梯度，但此时 P(CC|CA) 中位数仅约 0.7，表明仍有大量错误推理链无法被消除。这是现有 RLVR 机制的根本瓶颈。

### 4. 局限性与开放问题

**评估可靠性的局限**：
- LLM‑as‑a‑CoT‑Judge 系统使用 DeepSeek‑R1‑0528‑Qwen3‑8B 等模型进行推理链验证，存在假阳性/假阴性风险。虽通过多重验证、多个验证器和三种聚合策略（All/Majority/Any）进行缓解，但仍无法完全消除系统误差。完全人工验证成本过高，难以大规模实施。
- 部分基准（如 MATH‑500、AMC23）上基座模型的高 Pass@K 可能源于训练数据污染，使得在这些基准上评估 RLVR 的真正增益变得困难。

**理论框架的局限**：
- 定理 1 仅说明 RLVR 在**训练分布上**的优化动力学，未提供对未见数据的泛化保证。推理能力的泛化提升仅通过经验观察支持。
- 逻辑先验假设本身缺乏严格的实证验证方法——如何独立测量 $\alpha$ 和 $\beta$ 仍是开放问题。

**关键开放问题**：
1. **推理链质量的加速提升**：如何加速 P(CC|CA) 的提升，以在更少训练步数内实现更高质量的推理？
2. **奖励饱和后的持续优化**：当 P(CA)→1 导致 GRPO 优势为零时，如何继续消除剩余的错误推理链？可能的路径包括引入更细粒度的奖励（如推理步骤级别的验证）或额外的正则化。
3. **推理链直接奖励机制**：能否设计新的 RLVR 算法，直接利用推理链本身的质量作为奖励，而不仅是最终答案，从而更高效、更直接地激励正确推理？
4. **领域泛化**：RLVR 机制在多模态推理、科学推理等更广泛的场景中是否仍然有效？如何设计对应的可验证奖励？
5. **数学与代码任务的差异**：数学推理需要 CoT‑Pass@K 才能观察到的推理能力提升，与代码推理中 Pass@K 直接体现提升的差异，其深层原因是什么？是否与任务结构和验证方式有关？
6. **污染检测与基准健壮性**：如何区分基座模型在基准上的表现源于真正推理能力还是训练数据记忆？需要开发更健壮的评估基准。
7. **轻量级验证器设计**：能否设计轻量级且高可靠性的推理链验证器（尤其针对非结构化、长链条的数学推理），以降低评估成本并提高规模？



## 原文 PDF

![[paperPDFs/ICLR_2026/Reinforcement_Learning_with_Verifiable_Rewards_Implicitly_Incentivizes_Correct_Reasoning_in_Base_LLMs.pdf]]
