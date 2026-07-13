---
title: "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GEPA_Reflective_Prompt_Evolution_Can_Outperform_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/gepa-ai/gepa
openreview_forum_id: RQm2KQTM5r
aliases:
- GGP
- GEPA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将学习信号从标量奖励切换为基于自然语言轨迹和评估文本的反思性反馈，并引入帕累托前沿选择机制进行遗传搜索，从而以极少 rollout 高效率地进化提示指令。"
primary_logic: "现代 LLM 生成的执行链和评估文本本身比压缩的标量奖励提供更密集、更具信息量的学习信号；通过模仿自然进化中的遗传变异和基于帕累托的探索策略，可以从有限的实际交互中持续提炼出泛化性强的高质量提示。"
claims:
- "GEPA 在六项任务上平均超过 GRPO 6 个百分点，最高达 19 pp，且 rollout 减少 35 倍。"
- "GEPA 在所有基准上均超越 MIPROv2，在 GPT-4.1 mini 上的综合提升达 +13.33 pp，是 MIPROv2 提升幅度（+5.64 pp）的两倍以上。"
- "帕累托候选选择策略使 GEPA 的综合提升达到 +12.44%，远优于贪心选择（+6.05%）和束搜索（+5.11%）。"
- "GEPA 优化出的提示比 MIPROv2 的提示短约 33% 甚至更短，但性能更高，表明其生成的指令更加精炼有效。"
---

# GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning

> [!tip] 核心洞察
> 现代 LLM 生成的执行链和评估文本本身比压缩的标量奖励提供更密集、更具信息量的学习信号；通过模仿自然进化中的遗传变异和基于帕累托的探索策略，可以从有限的实际交互中持续提炼出泛化性强的高质量提示。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GEPA：反思性提示进化能够超越强化学习 |
| 英文题名 | GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=RQm2KQTM5r) · [GitHub](https://github.com/gepa-ai/gepa) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | GEPA (Genetic-Pareto) |
| Dataset | HotpotQA (Qwen3 8B), IFBench (Qwen3 8B), HoVer (Qwen3 8B), AIME-2025 (GPT-4.1 Mini) |

> [!tip] 效果简介
> - HotpotQA (Qwen3 8B) 上，Test Score 为 62.33，对比 43.33 (GRPO)，变化 +19.00。
> - IFBench (Qwen3 8B) 上，Test Score 为 38.61，对比 35.88 (GRPO)，变化 +2.73。
> - HoVer (Qwen3 8B) 上，Test Score 为 52.33，对比 38.67 (GRPO)，变化 +13.66。

## 概要

**核心问题**：基于策略梯度的强化学习方法（如 **GRPO**, Shao et al., 2024）在优化复合 AI 系统时，将模型输出的标量奖励作为唯一学习信号，丢弃了执行轨迹和评估反馈中的丰富诊断信息。这导致优化样本效率极低——通常需要数万次 rollout 才能适应新任务，严重制约了在预算受限场景下的实际部署。

**核心方法**：**GEPA (Genetic-Pareto)** 是一种反思性提示进化优化器，其关键创新在于将学习信号从标量奖励切换为基于自然语言执行轨迹和评估文本的反思性反馈，并引入帕累托前沿选择机制进行遗传搜索。具体而言，GEPA 仅优化各模块的系统指令（提示），冻结模型权重，通过反馈函数 $\mu_f$ 提取执行过程中的自然语言痕迹，利用大语言模型反思性地提出改进后的指令，再以帕累托前沿“照亮”策略从候选池中平衡探索与利用地选择待进化个体。

**方法定位**：GEPA 属于提示优化（prompt optimization）范式，区别于更新模型权重的强化学习方法（GRPO）和基于贝叶斯优化的指令搜索方法（**MIPROv2**, Opsahl-Ong et al., 2024）。它融合了文本梯度优化（如 **TextGrad**, Yuksekgonul et al., 2025）的反思思想与进化搜索的多样性保持机制，但在候选选择策略上以帕累托前沿取代了贪心选择和束搜索。

**主要结果**：
- 在六项基准测试上，GEPA 平均超过 GRPO **6 个百分点**，最高达 **19 pp**（HotpotQA），同时 rollout 消耗减少最高 **35 倍**（Table 1, Figure 1）。
- 在 GPT-4.1 Mini 上，GEPA 综合提升达 **+13.33 pp**，是 MIPROv2 提升幅度（+5.64 pp）的两倍以上（Table 2）。
- 帕累托候选选择策略贡献显著，综合提升达 **+12.44%**，远优于贪心选择（+6.05%）和束搜索（+5.11%）（Table 3, Figure 4）。
- GEPA 优化出的提示比 MIPROv2 短约 **33%**，但性能更高，表明其生成的指令更加精炼有效（Figure 16）。

**证据强度**：上述核心结论均有高置信度实验证据支撑，主要结果来自多基准、多模型（Qwen3 8B、GPT-4.1 Mini）的严格对比，消融实验验证了关键设计选择的有效性。局限性方面，System Aware Merge 策略的效果对预算分配敏感，且当前验证集中在 3-4 个模块的复合系统上，向更大规模系统的推广仍有待验证。



复合 AI 系统通过编排多个模块（如检索器、推理器、验证器）协同解决复杂任务，其性能高度依赖各模块的提示指令（prompts）和模型权重的质量。形式化地，系统在任务分布 $\mathcal{T}$ 上的优化目标为联合最大化期望评测值：

$$
\langle \Pi ^ { * } , \Theta ^ { * } \rangle _ { \Phi } = \arg \operatorname* { m a x } _ { \langle \Pi , \Theta \rangle _ { \Phi } } \mathbb { E } _ { ( x , m ) \sim \mathcal { T } } \left[ \mu \big ( \Phi ( x ; \langle \Pi , \Theta \rangle _ { \Phi } ) , m \big ) \right]
$$

然而，在实际部署中，计算资源受到严格限制——每次系统执行（rollout）都消耗可观的算力与时间。这使得优化必须在有限的 rollout 预算 $B$ 内完成：

$$
\langle \Pi ^ { * } , \Theta ^ { * } \rangle _ { \Phi } = \arg \operatorname* { m a x } _ { \langle \Pi , \Theta \rangle _ { \Phi } } \mathbb { E } _ { ( x , m ) \sim T } \left[ \mu \big ( \Phi ( x ; \langle \Pi , \Theta \rangle _ { \Phi } ) , m \big ) \right] , \quad \mathrm { s . t . ~ } \ \# \mathrm { r o l l o u t s } \leq B
$$

### 现有方法的根本瓶颈

当前主流的优化范式存在一个被忽视的结构性缺陷：**学习信号的信息密度严重不足**。

基于策略梯度的强化学习方法（如 **GRPO**, Shao et al., 2024）通过 LoRA 微调模型权重，但其优化信号仅为标量奖励（如答案正确与否）。这一压缩过程丢弃了模型在执行过程中产生的丰富诊断信息——包括自然语言推理链、工具调用轨迹、编译器错误等。其直接后果是样本效率极低：GRPO 通常需要约 24,000 次 rollout 才能在单个任务上收敛，且每次更新需处理 12 个样本为一组、累积 20 步梯度后才进行一次权重更新（LoRA rank=16, α=64, 学习率 $1 \times 10^{-5}$）。

另一方面，现有的提示优化器如 **MIPROv2**（Opsahl-Ong et al., 2024）采用贝叶斯优化（TPE）联合搜索指令和少样本示例，**Trace (OptoPrime)**（Cheng et al., 2024）和 **TextGrad**（Yuksekgonul et al., 2025）则通过文本梯度传播优化提示。但这些方法在候选选择策略上普遍采用贪心策略——始终从当前得分最高的候选出发进行突变，导致搜索极易陷入局部最优，探索树在首次找到可行策略后便停滞不前。

### 核心动机与洞察

本文的核心洞察在于：**现代大语言模型在执行任务时产生的自然语言轨迹和评估反馈文本，本身就构成了比压缩标量奖励更密集、更具信息量的学习信号**。与其将这些文本丢弃、仅保留一个数字，不如将其反馈给优化器本身，驱动反思性的提示改进。

同时，借鉴自然进化中的遗传变异和基于帕累托前沿的“照亮”探索策略（Mouret & Clune, 2015），可以在有限的实际交互中持续提炼出泛化性强的高质量提示，从根本上规避贪心搜索的局部最优陷阱。这一思路将优化对象从模型权重切换为系统提示指令，在保持模型冻结的前提下，以极少的 rollout 实现高效的任务适应。



## 核心方法与创新机理

GEPA 的核心创新在于将复合 AI 系统的优化信号从**压缩的标量奖励切换为富含诊断信息的自然语言反馈**，并引入**基于帕累托前沿的遗传搜索策略**，从而在极低的交互预算下实现高效的提示进化。

### 从标量奖励到反思性反馈的学习信号升级

传统基于策略梯度的强化学习方法（如 **GRPO**，Shao et al., 2024）将模型输出的标量奖励作为唯一学习信号，丢弃了执行轨迹和评估过程中产生的丰富文本信息。这导致优化效率极低——GRPO 通常需要约 24,000 次 rollout 才能适应新任务，但最终性能仍显著落后于仅需数百次 rollout 的 GEPA（Table 1, Figure 1）。

GEPA 通过引入**反馈函数** $ \mu_f $ 彻底改变了这一范式：在评估候选提示时，$ \mu_f $ 不仅返回标量得分，还提取执行过程中的自然语言痕迹（如编译器错误信息、中间推理步骤的正确性判断、答案与参考答案的逐项对比等），将这些文本反馈与得分一同传递给反思模块。反思大语言模型据此分析成功或失败的原因，并**反思性地提出改进后的提示指令**（Section 3）。这种设计使得每次 rollout 提供的信息密度远高于单一标量，是 GEPA 实现 35 倍样本效率提升的根本原因。

### 帕累托前沿选择：平衡探索与利用的进化策略

现有提示优化方法普遍采用贪心策略——每次只从当前全局最优候选出发进行变异（如 **TextGrad**，Yuksekgonul et al., 2025），或维持固定大小的 Top-N 束（如 APO）。这类策略极易陷入局部最优：一旦某个候选在验证集上取得高分，后续搜索便围绕其反复微调，耗尽预算却无法发现更优方案（Figure 4 左）。

GEPA 采用**基于帕累托前沿的“照亮”策略**（Mouret & Clune, 2015）：对于每个任务实例，保留在该实例上得分最高的候选，形成帕累托最优集合；严格被支配的候选则被剪枝。在每轮迭代中，GEPA 从帕累托前沿中按候选出现频率加权随机采样，作为下一轮变异的父代（Algorithm 2）。这一机制确保搜索不会过早收敛于单一策略，而是持续探索在不同实例上各有优势的候选，最终收敛到性能更高且泛化性更强的解。

消融实验证实了这一设计的决定性作用：在 Qwen3 8B 上的综合提升对比中，帕累托选择策略带来 **+12.44%** 的提升，远超贪心选择的 **+6.05%** 和束搜索的 **+5.11%**（Table 3）。搜索树可视化进一步表明，贪心策略在首次改进后即停滞，而帕累托策略产生了平衡的搜索树，持续发现新策略（Figure 4）。

### 仅优化提示指令，保持模型权重冻结

与 GRPO 通过 LoRA 微调所有模块的模型权重 $ \Theta $ 不同，GEPA **仅优化各模块的系统指令 $ \Pi $**，保持底层大语言模型权重完全冻结（Section 3）。这一设计带来三重优势：

1. **极低的计算开销**：无需进行任何梯度计算或参数更新，仅需调用推理 API。
2. **开箱即用的闭源模型兼容性**：GEPA 可直接应用于 GPT-4.1 Mini 等闭源模型，无需访问模型内部权重。实验表明，GEPA 在 GPT-4.1 Mini 上的综合提升达 **+13.33 pp**，是 MIPROv2 提升幅度（+5.64 pp）的两倍以上（Table 2）。
3. **强大的跨模型迁移能力**：在 Qwen3 8B 上优化出的提示直接用于 GPT-4.1 Mini，无需任何修改即可获得 **+9.00%** 的综合提升，优于 MIPROv2 在原模型上的优化效果（Table 2, Observation 6）。

### 精炼高效的指令生成

GEPA 通过反思性突变生成的提示不仅性能更优，而且更加精炼。统计显示，GEPA 优化出的提示长度约为 MIPROv2 提示的 **33% 甚至更短**，但性能更高（Figure 16, Figure 17）。这表明反思机制能够有效提取任务核心要求，去除冗余表述，生成更具针对性的指令。



GEPA 是一个面向复合 AI 系统的样本高效型提示优化器，其核心设计围绕三个原则展开：**遗传式提示进化**、**基于自然语言反馈的反思**以及**帕累托前沿驱动的候选选择**。与 GRPO 等更新模型权重的方法不同，GEPA 仅进化系统中各模块的提示指令 $\Pi_\Phi$，而保持底层大语言模型权重 $\Theta_\Phi$ 冻结。这一设计使其能够直接应用于闭源模型（如 GPT-4.1 Mini），无需访问模型内部参数。

### 优化循环

GEPA 的优化过程构成一个迭代循环，每轮迭代包含四个核心步骤：

1. **候选选择**：从当前候选池中，依据帕累托前沿策略选取一个待进化的提示程序。该策略保留在所有实例上至少在一个维度上达到最优的候选，剔除被严格支配的候选，并按候选在帕累托前沿上出现的频率进行加权随机采样，以平衡探索与利用。

2. **小批量执行与反馈收集**：在训练集的一个小批量示例上执行所选候选，记录完整的执行轨迹（如多步推理链、工具调用结果）和评估反馈文本。GEPA 将传统的标量奖励函数 $\mu$ 扩展为反馈函数 $\mu_f$，在返回得分的同时提取评估过程中的自然语言痕迹（如编译器错误信息、答案比对细节），作为后续反思的学习信号。

3. **反思性提示突变**：将当前模块的提示指令、执行轨迹、得分以及反馈文本一并提供给一个反思大语言模型，要求其分析成功或失败的原因，并生成改进后的提示指令。模块的更新顺序采用轮询策略。

4. **帕累托更新**：在验证集上评估新生成的候选，若其性能优于原候选，则将其加入候选池，并更新帕累托前沿——保留在每个实例上得分最优的候选，剔除被严格支配的候选。

### 可选模块

GEPA 还包含一个可选的 **System Aware Merge** 策略，用于对互补模块进行遗传交叉。当不同分支的进化产生了针对不同模块的改进时，该策略将两个父代候选的提示指令进行合并，生成融合双方优势的子代候选。该策略的效果对预算分配和调用时机敏感，在部分任务上能进一步提升性能，但缺少自适应调度机制。

### 输入输出

- **输入**：复合 AI 系统 $\Phi$ 的初始提示集合 $\Pi_\Phi$、训练集 $D_\text{train}$、验证集 $D_\text{val}$、反馈函数 $\mu_f$、总 rollout 预算 $B$。
- **输出**：经过优化后的提示集合 $\Pi^*_\Phi$，可直接部署到目标系统中，无需修改模型权重。

整个流程在有限的 rollout 预算约束下运行，大部分预算消耗在验证集上的候选评估，而非直接用于产生学习信号。这一设计使得 GEPA 在仅需 79 至 737 次训练集 rollout 的条件下即可收敛到高质提示，展现出极高的样本效率。



### 复合AI系统的形式化建模

GEPA 将复合 AI 系统形式化为一个四元组 $\Phi = (M, C, \mathcal{X}, \mathcal{Y})$，其中 $M$ 为模块集合，$C$ 为模块间的控制流逻辑，$\mathcal{X}$ 和 $\mathcal{Y}$ 分别为输入空间和输出空间。每个模块 $M_i$ 由提示指令 $\pi_i$、模型权重 $\theta_i$、输入模式 $\chi_i$ 和输出模式 $\mathcal{V}_i$ 共同定义。

基于此形式化，GEPA 的优化目标是在不超过总 rollout 预算 $B$ 的约束下，最大化系统在任务分布上的期望评测值：

$$\langle \Pi^{*}, \Theta^{*} \rangle_{\Phi} = \arg\max_{\langle \Pi, \Theta \rangle_{\Phi}} \mathbb{E}_{(x, m) \sim \mathcal{T}} \left[ \mu \big( \Phi(x; \langle \Pi, \Theta \rangle_{\Phi}), m \big) \right], \quad \mathrm{s.t.} \ \#\mathrm{rollouts} \leq B$$

其中 $\Pi$ 为所有模块的提示指令集合，$\Theta$ 为所有模块的模型权重集合，$\mu$ 为评测指标函数，$\mathcal{T}$ 为任务分布。GEPA 的关键设计选择是**仅优化 $\Pi$ 而冻结 $\Theta$**，将优化对象从模型权重切换为提示指令，从而避免昂贵的大规模参数更新。

### 反馈函数：从标量奖励到自然语言学习信号

传统强化学习方法（如 GRPO）仅使用标量奖励 $\mu$ 作为优化信号，丢弃了执行过程中丰富的诊断信息。GEPA 将奖励函数扩展为反馈函数 $\mu_f$，该函数在返回标量得分的同时，提取评估过程中的自然语言执行轨迹和评估文本（如编译器错误信息、中间推理步骤的正确性判断），并将其作为 `feedback_text` 一并返回。

这一扩展是 GEPA 样本效率的核心来源：自然语言反馈比压缩后的标量奖励携带更密集的信息量，使后续的反思性突变模块能够进行细粒度的因果归因——明确区分成功或失败是由哪个模块、哪个具体决策步骤导致的。

### 反思性提示突变

反思性提示突变是 GEPA 生成新候选指令的核心机制。在每一轮迭代中，GEPA 按轮询策略选择一个待优化的模块，将该模块的**当前提示指令**、**完整执行轨迹**、**标量得分**和**自然语言反馈文本**一并提交给反思大语言模型。反思模型的任务是对成功或失败进行归因，并针对性地提出改进后的提示指令。

与直接使用标量梯度更新参数不同，这一过程模拟了人类工程师的调试行为：阅读执行日志和错误信息，定位问题根源，然后修改指令以修复缺陷或强化有效策略。Figure 26 展示了这一过程如何在 PUPA 任务上逐步累积任务特定的细微差别，从基础提示逐步演进到最优提示。

### 帕累托前沿选择策略

为避免贪心选择策略（如 TextGrad 的 SelectBestCandidate）陷入局部最优，GEPA 引入了基于帕累托前沿的“照亮”选择策略。其核心逻辑在 Algorithm 2 中定义：

- **帕累托保留**：对于每个任务实例，保留在该实例上取得最佳得分的候选提示程序；严格被支配的候选（在所有实例上均不优于至少一个其他候选）则被剪枝。
- **频率加权随机采样**：从帕累托最优候选集合中，按每个候选在任务实例上成为最优的频率进行加权随机采样，作为下一轮突变的父代。

这一策略在探索与利用之间建立了动态平衡：高频候选（在更多实例上表现最优）有更高概率被选中进行利用，而低频但独特的候选（在某些困难实例上唯一最优）仍保留被探索的机会。Figure 4 的可视化对比清晰地展示了这一差异：贪心选择在找到第一个有效策略后迅速停滞，而帕累托选择产生了平衡的搜索树，持续发现性能更高的解。

### 系统感知合并（可选模块）

对于包含多个互补模块的复合 AI 系统，GEPA 提供可选的系统感知合并操作。当不同分支的突变分别在各自模块上积累了互补的改进时，合并操作通过遗传交叉将这些改进整合到同一候选程序中。其有效性对预算分配和调用时机敏感——在 HotpotQA 上，GEPA+Merge 将得分进一步提升至 64.33，但在其他任务上增益并不稳定，表明该模块缺少自适应的调度机制。



## 实验与关键发现

### 主实验结果

GEPA 在两个模型家族（Qwen3 8B 与 GPT-4.1 Mini）上均展示了远超强基线的优化能力，同时保持极高的样本效率。

**与 GRPO 的对比（Qwen3 8B）。** 在六项基准测试中，GEPA 以冻结模型权重、仅优化提示指令的方式，在五项任务上显著超越基于策略梯度的 GRPO（LoRA 微调，24,000 次 rollout），平均领先 6 个百分点，最高领先 19 个百分点（HotpotQA: 62.33 vs 43.33），而 GEPA 仅消耗 79 至 737 次训练集 rollout，样本效率提升最高达 35 倍（Table 1）。唯一的例外是 AIME-2025，该任务上 GEPA 落后于 GRPO，提示该任务场景下权重微调可能仍具优势。引入 System Aware Merge 后，GEPA+Merge 在 HotpotQA 上进一步提升至 64.33，但该增益对预算分配敏感。

**与 MIPROv2 的对比（GPT-4.1 Mini）。** 在闭源模型 GPT-4.1 Mini 上，GEPA 的综合提升达 +13.33 个百分点，是 MIPROv2（+5.64 pp）的两倍以上（Table 2）。在 AIME-2025 上，GEPA+Merge 达到 59.33，领先 MIPROv2 达 8 个百分点。值得注意的是，GEPA 优化出的提示比 MIPROv2 的提示短约 33% 甚至更短，但性能更高，表明其生成的指令更加精炼有效（Figure 16）。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/018_Figure_16.jpg]]
*Figure 16: These plots visualize the final aggregate scores against the aggregate prompt size (across all benchmarks) of the final optimized system for each optimizer. It can be seen that GEPA consistently produces prompts that are around less than 33% of the size of MIPROv2’s prompts, while getting higher performance. Most of GEPA’s prompt tokens are used for providing instructions, whereas most of MIPROv2’s prompt tokens pertain to few-shot examples*

**跨模型迁移。** 将在 Qwen3 8B 上优化的 GEPA 提示直接迁移至 GPT-4.1 Mini 评估，仍获得 +9.00% 的综合提升，超过 MIPROv2 在原模型上优化的 +5.64%，验证了 GEPA 优化提示的强泛化性（Table 2, Observation 6）。

### 消融实验

消融实验围绕 GEPA 的核心设计选择——候选选择策略展开（Table 3, Figure 4）。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/007_Figure_4.jpg]]
*Figure 4: Comparing the impact of different candidate selection strategies. (Left) As can be seen, selecting the best-performing candidate in every iteration led to a local-optima after one iteration, leading to suboptimal search performance. (Right) On the other hand, using pareto-based candidate selection strategy, GEPA was able to generate a balanced search tree, finding a better performing program within the same budget*

- **帕累托选择 vs 贪心选择。** 贪心策略（SelectBestCandidate）每轮仅从当前得分最高的候选出发进行突变，综合提升仅 +6.05%，且在多数任务上迅速陷入局部最优。Figure 4（左）的搜索树显示，贪心策略在找到第一个改进后反复尝试精化却无法突破，最终耗尽预算。
- **帕累托选择 vs 束搜索。** 束搜索（BeamSearch）维持 Top-5 候选，综合提升为 +5.11%，同样远低于 GEPA 的 +12.44%。
- **帕累托选择的机制优势。** GEPA 的帕累托前沿“照亮”策略从所有实例上的帕累托最优候选中按出现频率加权随机采样，平衡了探索与利用。Figure 4（右）的搜索树呈现平衡的分支结构，避免了单一方向的过度开发。

### 学习曲线与样本效率

Figure 1 展示了 GEPA、MIPROv2 和 GRPO 在不同 rollout 数量下的学习曲线。GEPA 在极少的 rollout 后即快速攀升，而 GRPO 在 24,000 次 rollout 后仍缓慢增长。GEPA 的大部分 rollout 预算消耗在验证集上的候选选择，而非直接用于产生学习信号——这一观察指向进一步优化空间：通过更小的验证集或动态验证子集选择可进一步提升样本效率。

### 泛化性分析

Figure 15 可视化了各优化器的泛化差距（测试集性能与最佳验证性能之差）。GEPA 的泛化差距保持在较低水平，表明其优化过程未对验证集过拟合，这与帕累托前沿维护多样候选池的机制一致。

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/017_Figure_15.jpg]]
*Figure 15: Generalization gaps for different optimization methods. Following Wan et al. (2024), we visualize the generalization gap (i.e., the difference between final test set performance and the best achieved validation performance) for different optimizers. While Wan et al. (2024) previously observed that exemplars tend to generalize better, our results suggest that instructions generated by reflective prompt evolution can achieve stronger generalization as well as improved overall performance. We hypothesize this difference may be due to the improving capabilities of the underlying LLMs, as more recent models are both better at adhering to instructions and capable of reflecting on their outputs*

### 失败模式与局限性

1. **AIME-2025 上的相对劣势。** 在数学推理任务 AIME-2025 上，GEPA 在 Qwen3 8B 下未能超越 GRPO，说明当任务需要深层模型能力调整时，纯提示优化存在天花板。
2. **Merge 策略的敏感性。** System Aware Merge 的效果依赖于突变与交叉之间的预算分配和时机，缺乏自适应调度机制，在某些任务上未带来增益甚至略有下降。
3. **对抗性提示的脆弱性。** 实验表明通过反转奖励函数，GEPA 可以发现使模型性能大幅下降的对抗性提示，揭示了指令遵循的脆弱性，但未深入分析根本原因和防御策略。
4. **系统规模限制。** 当前验证仅限于包含 3–4 个模块的复合 AI 系统，向更大规模系统的推广仍有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/008_Figure.jpg]]

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/010_Figure_9.jpg]]
*Figure 9: (a) Final test set performance for aggregate and individual benchmarks for gpt-41-mini. Optimizer Performance on Qwen3 8B (b) Final test set performance for aggregate and individual benchmarks for qwen3-8b. Figure 9: Final test set performance for aggregate and individual benchmarks*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/012_Figure.jpg]]
*Figure: (a) GPT-4.1 Mini - MIPRO (b) Qwen3 8B - MIPRO (c) Qwen3 8B - GRPO*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/013_Figure_11.jpg]]
*Figure 11: Hotpot QA Bench: rollout vs. score for different models/settings. (a) GPT-4.1 Mini - MIPRO*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/014_Figure_12.jpg]]
*Figure 12: IFBench: rollout vs. score for different models/settings. (a) GPT-4.1 Mini - MIPRO*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/016_Figure_14.jpg]]
*Figure 14: PUPA: rollout vs. score for different models/settings*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/019_Figure.jpg]]
*Figure: Optimized Prompt Size across optimizers (lower is better), GPT-4.1 Mini (a) Comparing the token counts of the optimized programs across benchmarks for GPT-4.1 Mini. Optimized Prompt Size across optimizers (lower is better), Qwen3 8B (b) Comparing the token counts of the optimized programs across benchmarks for Qwen3 8B*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/020_Figure_18.jpg]]
*Figure 18: HotpotQA GPT-4.1 Mini (c) GEPA - Best Config*

![[assets/figures/papers/paper_list_l18_https_openreview_net_forum_id_RQm2KQTM5r/figures/022_Figure_19.jpg]]
*Figure 19: HotpotQA Qwen3 8B*



## 定位与知识库关联

### 瓶颈与核心洞察

当前基于策略梯度的强化学习方法（如 **GRPO**，Shao et al., 2024）在优化复合 AI 系统时，将模型输出的标量奖励作为学习信号，丢弃了自然语言执行轨迹和评估反馈中的丰富诊断信息。这导致优化样本效率极低：GRPO 通常需要约 24,000 次 rollout 才能适应新任务，且在计算资源受限的实际部署中难以快速迭代。

GEPA 的核心洞察在于：现代 LLM 生成的执行链和评估文本本身比压缩的标量奖励提供更密集、更具信息量的学习信号。通过模仿自然进化中的遗传变异和基于帕累托的探索策略，可以从有限的实际交互中持续提炼出泛化性强的高质量提示。这一思路将学习信号从标量奖励切换为基于自然语言轨迹和评估文本的反思性反馈，并引入帕累托前沿选择机制进行遗传搜索，从而以极少 rollout 高效率地进化提示指令。

### 在优化方法谱系中的位置

GEPA 位于提示优化（Prompt Optimization）与进化搜索（Evolutionary Search）的交叉地带，与以下方法形成对比：

- **GRPO**（Shao et al., 2024）：基于策略梯度的强化学习基线，通过 LoRA 微调模型权重，使用标量奖励作为优化信号。GEPA 与其关键区别在于：(1) 仅优化模块的系统指令，保持模型权重冻结；(2) 将标量奖励扩展为反馈函数 $\mu_f$，提取评估过程中的自然语言痕迹用于反思性提示更新。
- **MIPROv2**（Opsahl-Ong et al., 2024）：领先的指令和少样本联合优化器，采用贝叶斯优化。GEPA 在所有基准上均超越 MIPROv2，在 GPT-4.1 mini 上的综合提升达 +13.33 pp，是 MIPROv2 提升幅度（+5.64 pp）的两倍以上。此外，GEPA 优化出的提示比 MIPROv2 的提示短约 33% 甚至更短，但性能更高，表明其生成的指令更加精炼有效。
- **Trace (OptoPrime)**（Cheng et al., 2024）：使用文本梯度优化的提示优化方法。
- **TextGrad**（Yuksekgonul et al., 2025）：通过文本梯度传播优化提示的方法，其候选选择策略为贪心选择当前最佳候选进行突变。GEPA 的帕累托选择策略相比贪心选择（+6.05%）和束搜索（+5.11%），带来了显著更高的综合提升（+12.44%），验证了帕累托前沿“照亮”策略在平衡探索与利用方面的优势。

### 适用边界与局限

1. **验证集预算消耗**：GEPA 的大部分 rollout 预算消耗在验证集中的候选项选择上，而非直接用于学习信号。进一步的小批量或动态验证集选择可提升效率。
2. **合并策略的敏感性**：System Aware Merge 策略的有效性对预算分配和调用时机敏感，缺少自适应调度机制。在部分任务上融合 GEPA+Merge 能够进一步提升性能（如 HotpotQA 上提升至 64.33），但其效果依赖于突变与交叉之间的预算分配和时机。
3. **系统规模限制**：当前仅在最多包含 3-4 个模块的复合 AI 系统上进行验证，向更大规模系统的推广仍有待验证。
4. **对抗性脆弱性**：对抗性提示搜索揭示了对指令遵循的脆弱性，但未深入分析其根本原因和防御策略。

### 开放问题

1. 反思性提示进化是否可推广到需要更新模型权重的场景，与参数高效微调解耦？
2. 在实时交互或极少 rollouts 的部署环境中，GEPA 的帕累托历史如何有效初始化以加速适应？
3. 自然语言反馈的质量（如人类编写的少量解释）对优化效果的影响如何？
4. 能否将 GEPA 的思想用于自动发现复合 AI 系统中模块间的控制流逻辑？



## 原文 PDF

![[paperPDFs/ICLR_2026/GEPA_Reflective_Prompt_Evolution_Can_Outperform_Reinforcement_Learning.pdf]]
