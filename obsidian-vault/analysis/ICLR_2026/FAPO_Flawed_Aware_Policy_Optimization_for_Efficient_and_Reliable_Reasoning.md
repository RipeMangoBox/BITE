---
title: "FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/FAPO_Flawed_Aware_Policy_Optimization_for_Efficient_and_Reliable_Reasoning.pdf
project_link: https://fapo-rl.github.io
code_link: null
openreview_forum_id: jhqqoimoWt
aliases:
- FFAPO
- FAPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "对flawed-positive rollout施加一种无参数的奖励惩罚λ，并利用群体相对优势估计动态调整优化方向，使模型在早期利用flawed positive作为学习捷径，后期则逐渐转向可靠的推理。"
primary_logic: "flawed-positive rollout在训练初期充当“踏脚石”帮助模型快速获得正确答案，但随着能力提升，其不正确的推理过程会阻碍进一步优化；通过自适应地惩罚flawed positive，可以实现从快速进步到稳定可靠推理的自然过渡。"
claims:
- "flawed-positive rollouts 在不同的LLM中占正确rollout的20%-40%，且在RL训练过程中持续存在（比例约30%）。"
- "在早期学习阶段flawed positive的占比很高，但随着训练进程显著下降，说明其应作为学习过程中的“踏脚石”。"
- "直接使用Qwen3-32B检测flawed positive并给予负奖励，相比基线RLVR能显著提高AIME24性能，但初期提升较慢，证实flawed positive具有双重作用。"
- "FAPO通过λ=1的惩罚和群体相对优势，使优化方向在α/β>1时自然从鼓励正确答案转向强化可靠推理，既稳定训练又提升最终性能。"
---

# FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning

> [!tip] 核心洞察
> flawed-positive rollout在训练初期充当“踏脚石”帮助模型快速获得正确答案，但随着能力提升，其不正确的推理过程会阻碍进一步优化；通过自适应地惩罚flawed positive，可以实现从快速进步到稳定可靠推理的自然过渡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | FAPO：面向高效可靠推理的缺陷感知策略优化 |
| 英文题名 | FAPO: Flawed-Aware Policy Optimization for Efficient and Reliable Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jhqqoimoWt) · [Project](https://fapo-rl.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | FAPO (Flawed-Aware Policy Optimization) |
| Dataset | AIME24, AIME25, GPQA-Diamond, AMC |

> [!tip] 效果简介
> - AIME24 上，Accuracy 为 42.4，对比 38.9，变化 +3.5。
> - AIME25 上，Accuracy 为 33.5，对比 29.5，变化 +4.0。
> - GPQA-Diamond 上，Accuracy 为 53.1，对比 51.0，变化 +2.1。

## 概要

### 问题瓶颈

在基于可验证奖励的强化学习（RLVR）中，策略网络通过规则化结果奖励（答案正确+1，错误-1）进行优化。然而，一类被称为 **flawed-positive** 的rollout——即最终答案正确但推理过程中存在逻辑错误的样本——被赋予与完全正确rollout相同的正奖励。实验表明，这类flawed-positive在不同LLM中占正确rollout的20%–40%，且在RL训练过程中持续存在（比例约30%）（Figure 2）。由于奖励信号无法区分推理过程的可靠性，策略网络会强化这些不可靠的推理模式，最终限制了模型性能的上限。

### 核心思路

FAPO（Flawed-Aware Policy Optimization）的核心洞察是：flawed-positive rollout在训练初期充当“踏脚石”，帮助模型快速获得正确答案；但随着模型能力提升，其不正确的推理过程会阻碍进一步优化。FAPO通过**自适应惩罚机制**实现从快速进步到稳定可靠推理的自然过渡——在早期利用flawed positive作为学习捷径，后期则逐渐将优化方向转向可靠的推理。

具体而言，FAPO在RLVR奖励的基础上，对检测到的flawed-positive rollout施加一个无参数的奖励惩罚 $-\lambda$（默认 $\lambda=1$），并利用群体相对优势估计动态调整优化方向。当训练早期正确答案的收益（$\alpha$）大于过程可靠性的损失（$\beta$）时，优化自然偏向鼓励正确答案；随着训练推进，这一关系反转，优化方向自动转向强化可靠推理。

### 方法定位

FAPO在方法谱系中处于**RLVR + 过程级奖励**的交叉点。与仅依赖结果奖励的基线GRPO（Shao et al., 2024）相比，FAPO引入了两个关键模块：

- **FAPO-GenRM**：一个紧凑的生成式奖励模型（基于4B参数），负责检测flawed-positive rollout并定位第一步错误的位置。该模型通过步级RL奖励进行训练，在FlawedPositiveBench和ProcessBench上显著优于现有判别式PRM（如Qwen2.5-Math-PRM-72B）。
- **FAPO-Reasoning**：在强化学习训练中使用修改后的FAPO奖励函数 $R_{\text{FAPO}} = R_{\text{RLVR}} + R_{\Delta}$，其中 $R_{\Delta}$ 在GenRM检测到flawed positive时施加 $-\lambda$ 惩罚，否则为0。

FAPO的奖励设计不同于传统的过程奖励（step-ratio reward），后者虽然初期略有提升，但会导致reward hacking和推理跳跃，最终表现停滞（Figure 7）。FAPO通过仅对flawed positive施加惩罚（而非对正确步骤给予正向奖励），避免了这一陷阱。

### 主要结果

在数学推理基准上的实验表明，FAPO在多个指标上显著优于RLVR基线：

| 基准 | 基线-32B | FAPO-32B | 提升 |
|------|---------|----------|------|
| AIME24 | 38.9 | **42.4** | +3.5 |
| AIME25 | 29.5 | **33.5** | +4.0 |
| GPQA-Diamond | 51.0 | **53.1** | +2.1 |
| AMC | 85.0 | **91.6** | +6.6 |
| LiveCodeBench | 28.6 | **33.6** | +5.0 |

FAPO在提升结果正确性的同时，有效降低了flawed-positive比例，且训练过程中平均token使用量保持可比水平。引入GenRM推理带来的额外计算开销使训练时间增加不到20%，通过异步Reward Loop基础设施（Section 4.5）可进一步减轻GPU空闲时间。

### 局限与开放问题

当前验证主要在数学推理任务和Qwen系列模型上进行，FAPO在多选题、多轮对话、智能体RL等更广泛场景的有效性尚未验证。此外，尽管FAPO显著减少了flawed-positive的比例，但未完全根除，可能仍对极端情况下的性能有影响。开放问题包括：惩罚机制在非数学推理任务中的适配、$\lambda$的自适应调整自动化、以及与现有RL增强技术的组合效果。

### 基于可验证奖励的强化学习（RLVR）的瓶颈

在数学推理等具有确定性答案的任务中，基于可验证奖励的强化学习（RLVR）已成为提升大语言模型（LLM）推理能力的有效范式。其核心机制是：模型对给定问题生成推理轨迹（rollout），仅依据最终答案的正确性给予二元奖励——正确为+1，错误为-1（见 Equation 4）。这种稀疏的结果监督使模型能够通过反复试错来优化策略，无需昂贵的人工过程标注。

然而，RLVR存在一个关键的结构性盲区：**答案正确但推理过程存在逻辑缺陷的rollout——即flawed positive——被赋予与完全正确的rollout完全相同的正奖励**。这导致策略网络在优化过程中无法区分“真正理解了问题”与“恰好蒙对了答案”，从而强化了不可靠的推理模式。论文的预实验揭示了这一问题的严重性：

- **普遍性**：在不同规模的LLM中，flawed positive占所有正确rollout的比例高达20%–40%（Figure 2(a)）。
- **持续性**：在RL训练过程中，这一比例并非逐渐消失，而是稳定维持在约30%的水平（Figure 2(c)），说明标准RLVR无法自行消除这一问题。
- **双重角色**：flawed positive在训练初期充当“踏脚石”——模型通过不完美的推理快速获得正确答案，积累正奖励信号；但随着能力提升，这些有缺陷的推理模式成为进一步优化的障碍。直接对flawed positive施加负奖励的实验（Figure 2(d)）证实了这一判断：虽然最终性能优于基线，但初期提升明显更慢，说明粗暴地完全否定flawed positive会破坏其早期的学习价值。

### 现有方法的缺口

当前应对这一问题的思路主要分为两类，但各有不足：

**判别式过程奖励模型（PRM）** 试图为每个推理步骤分配细粒度奖励，理论上可以区分flawed positive。但这类模型存在三个问题：（1）训练需要昂贵的人工步骤级标注；（2）在RL训练中直接使用过程奖励容易引发reward hacking——模型学会生成冗长但空洞的推理步骤来骗取奖励，最终导致性能停滞（Figure 7）；（3）判别式PRM通常只能给出标量分数，缺乏可解释性。

**基于结果奖励的增强策略**（如GRPO，Shao et al., 2024）通过群体相对优势估计和裁剪目标来稳定训练，但其奖励函数本身并未区分flawed positive，因此无法从根本上解决过程不可靠的问题。

### 本文动机

FAPO的核心动机源于一个关键洞察：**flawed positive在RL训练中的价值是时变的**。在早期，它们作为“学习捷径”帮助模型快速建立从问题到正确答案的映射；在后期，它们不正确的推理过程却阻碍模型向真正可靠的推理演进。因此，理想的解决方案不应是一刀切地惩罚或忽略flawed positive，而应设计一种**自适应机制**，使模型能在早期利用flawed positive加速学习，后期则自然转向强化可靠推理。

基于这一动机，FAPO提出两个核心组件：（1）一个紧凑的**生成式奖励模型（GenRM）**，能够精准检测flawed positive并定位错误步骤；（2）一种**无参数的奖励惩罚机制**，结合群体相对优势估计，使优化方向随训练进程动态调整——当模型能力较弱时，flawed positive仍能贡献正向优势；当模型能力提升后，惩罚信号自然主导优化，推动策略向可靠推理收敛。

## 核心方法与创新机理

FAPO 的核心创新在于**首次系统性地识别并解决了基于可验证奖励的强化学习（RLVR）中“缺陷正样本”（flawed-positive）的双重作用问题**，并提出了一套无需复杂超参数搜索的自适应优化框架。其关键创新点可归纳为三个紧密耦合的“changed slots”：

### 1. 缺陷感知的奖励惩罚机制（Reward Function Slot）

**基线缺陷**：标准 RLVR 采用二元结果奖励（$R_{\mathrm{RLVR}}$），即答案正确为 +1，错误为 -1（Equation 4）。这种粗粒度奖励将“答案正确但推理过程存在逻辑缺陷”的 flawed-positive rollout 与完全正确的 rollout **赋予相同的正奖励**，导致策略网络强化不可靠的推理模式，形成性能瓶颈。

**FAPO 创新**：引入一个**无参数的奖励惩罚项 $R_{\Delta}$**，对检测到的 flawed-positive rollout 施加 $-\lambda$ 的惩罚（默认 $\lambda=1$），从而将奖励函数重构为：

$$R_{\mathrm{FAPO}}(o, a^{*} | \boldsymbol{\theta}) = R_{\mathrm{RLVR}}(o, a^{*}) + R_{\Delta}(o, a^{*} | \boldsymbol{\theta})$$

其中 $R_{\Delta}$ 在 GenRM 判定当前 rollout 为 flawed positive 时取 $-\lambda$，否则为 0（Equation 8）。这一设计的精妙之处在于**惩罚强度 $\lambda$ 固定为 1，无需手动调节**——其自适应能力完全由群体相对优势估计的动力学自然产生。

### 2. 群体相对优势驱动的自适应优化方向（Advantage Estimation Slot）

**基线缺陷**：GRPO 的优势估计仅基于规则奖励的群体归一化（$\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\})}{\mathrm{std}(\{R_i\})}$，Equation 1），无法区分 flawed positive 与完全正确 rollout 对策略更新的贡献差异。

**FAPO 创新**：虽然优势估计的**公式形式保持不变**（Equation 8），但输入的奖励值已通过 $R_{\Delta}$ 进行了调整。这一看似简单的改变产生了关键的**自适应动力学**：

- **训练早期**：策略能力较弱，flawed-positive rollout 的答案正确性使其在群体中仍具有相对较高的奖励，因此继续作为“踏脚石”获得正向优势，帮助模型快速学会获得正确答案。
- **训练后期**：随着策略能力提升，完全正确的 rollout 比例增加。此时，flawed-positive rollout 因 $-\lambda$ 惩罚，其奖励在群体中**相对降低**，优势估计自然转为负值或接近零，优化方向自动从“鼓励任何正确答案”**平滑过渡到“强化可靠推理”**。

这一机制在 Appendix A 中有严格证明：当正确 rollout 中完全正确与 flawed positive 的比例 $\alpha/\beta > 1$ 时，flawed positive 的优势自动变为负值，实现了无需手动调节 $\lambda$ 的自适应优化。

### 3. 生成式奖励模型（FAPO-GenRM）用于缺陷检测（Reward Model Slot）

**基线缺陷**：传统 RLVR 不使用过程奖励模型，或使用判别式 PRM（Process Reward Model）仅能给出标量分数，无法精确定位推理错误的位置和类型。

**FAPO 创新**：训练一个紧凑的**生成式奖励模型 FAPO-GenRM-4B**，直接输出 flawed-positive 判定及**第一步错误的具体位置**。其训练奖励函数（Equation 7）由两部分组成：

$$R_{\mathrm{FAPO-GenRM}} = R_{\mathrm{Outcome}} + R_{\mathrm{Process}}$$

- $R_{\mathrm{Outcome}}$：判断该 rollout 是否为 flawed positive（正确预测得 +1，否则 -1）
- $R_{\mathrm{Process}}$：基于预测错误位置 $\hat{t}_\theta$ 与真实错误位置 $t^*$ 的归一化距离给予惩罚（$-\frac{|\hat{t}_\theta - t^*|}{n}$）

这一设计使 GenRM 不仅是一个“缺陷分类器”，更是一个具备**细粒度过程评估能力**的奖励模型。实验表明，FAPO-GenRM-4B 在 FlawedPositiveBench 和 ProcessBench 上**超越了其教师模型 Qwen3-32B** 以及判别式 SOTA PRM（Figure 3），验证了生成式架构在过程级奖励建模上的优势。

### 创新总结

FAPO 的三项创新构成了一个**紧密协同的系统**：GenRM 提供精确的 flawed-positive 检测信号，惩罚机制将这一信号注入奖励函数，而群体相对优势估计则自动调节优化方向，使模型在训练初期利用 flawed positive 作为学习捷径，后期自然转向可靠推理。这一设计无需复杂的手动奖励塑形（reward shaping），仅通过一个固定惩罚系数 $\lambda=1$ 就实现了从“快速进步”到“稳定可靠”的优雅过渡，从根本上解决了 RLVR 中 flawed positive 的双重作用问题。

FAPO 的整体流程由两个核心模块构成：**FAPO-GenRM**（生成式奖励模型）与 **FAPO-Reasoning**（推理策略优化），二者通过异步 Reward Loop 基础设施耦合，形成“检测—惩罚—优化”的闭环。

### 模块关系与数据流

1. **FAPO-GenRM**：一个紧凑的生成式奖励模型，负责对推理策略网络产生的 rollout 进行 flawed-positive 检测。其输入为问题 $q$ 和 rollout $o$，输出为二值判定 $\hat{y}_{\boldsymbol{\theta}}(o, a^{*}) \in \{\mathrm{FP}, \neg \mathrm{FP}\}$ 以及第一步逻辑错误的位置 $\hat{t}_{\boldsymbol{\theta}}$。该模块在 FAPO-Critic-85K 数据集上通过步级 RL 奖励（Equation 7）训练，总奖励为结果正确性奖励与错误定位偏差惩罚之和：
   $$R_{\mathrm{FAPO-GenRM}} = R_{\mathrm{Outcome}} + R_{\mathrm{Process}}$$
   其中 $R_{\mathrm{Outcome}}$ 对 flawed-positive 预测正确性给予 ±1 奖励，$R_{\mathrm{Process}} = -\frac{|\hat{t}_{\boldsymbol{\theta}} - t^{*}|}{n}$ 对错误位置偏差施加连续惩罚。这一设计使 GenRM 不仅判断 rollout 是否含有逻辑缺陷，还能精确定位错误步骤，为后续策略优化提供细粒度信号。

2. **FAPO-Reasoning**：在标准 GRPO（Shao et al., 2024）框架上，将 GenRM 的检测结果注入奖励函数，形成 FAPO 奖励（Equation 8）：
   $$R_{\mathrm{FAPO}}(o, a^{*} | \boldsymbol{\theta}) = R_{\mathrm{RLVR}}(o, a^{*}) + R_{\Delta}(o, a^{*} | \boldsymbol{\theta})$$
   $$R_{\Delta} = \begin{cases} -\lambda, & \text{If } \mathcal{I}(o, a^{*}) \text{ and } \hat{y}_{\boldsymbol{\theta}}(o, a^{*}) = \mathrm{FP} \\ 0, & \text{Otherwise} \end{cases}$$
   其中 $R_{\mathrm{RLVR}}$ 为基于答案匹配的二元规则奖励（正确 +1，错误 -1），$R_{\Delta}$ 在检测到 flawed positive 时施加 $-\lambda$ 惩罚（默认 $\lambda=1$）。修改后的奖励值随后参与群体相对优势估计：
   $$\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{\mathrm{std}(\{R_i\}_{i=1}^G)}$$
   优势估计沿用 GRPO 的组内归一化，但因奖励已包含 flawed-positive 惩罚，优化方向会随训练进程自然调整：早期 $\alpha/\beta < 1$ 时，正确答案的奖励优势仍占主导，flawed positive 充当“踏脚石”；后期 $\alpha/\beta > 1$ 时，惩罚使 flawed positive 的优势降低，优化方向转向可靠的推理过程（详见 Appendix A 的动力学分析）。

3. **Reward Loop**：异步基础设施，将 rollout 生成与 GenRM 推理并行化。推理策略在生成一组 rollout 后，异步发送至 GenRM 服务集群进行 flawed-positive 检测，策略更新不阻塞等待检测结果。该设计使 GenRM 引入的额外计算开销控制在训练总时间的 20% 以内（Table 4），避免 GPU 空闲。

### 关键因果机制

FAPO 的核心洞察在于 flawed-positive rollout 的双重角色：它们在训练初期提供正确答案的“捷径”，帮助模型快速提升结果正确性；但随着策略能力增强，这些不可靠的推理模式会限制进一步优化。FAPO 通过无参数的奖励惩罚 $\lambda$ 与群体相对优势的联动，实现了从“利用捷径”到“追求可靠推理”的自然过渡——这一过渡无需手动调整超参数或分阶段训练，完全由优势估计的动态变化驱动。

### 证据强度说明

- 奖励函数与优势估计的公式定义在 Equation 8 及 Appendix A 中有严格推导，置信度 0.95。
- 异步 Reward Loop 的工程设计在 Section 4.5 和 Appendix C 中有详细描述，训练时间增幅的测量基于 Table 4 的实际运行数据，置信度 0.95。
- 关于“踏脚石”效应的动力学分析主要来自 Figure 2 的预实验与 Appendix A 的理论推导，在更大规模或非数学任务上的泛化性尚待验证（置信度 0.9）。

### 已知局限

当前框架的 GenRM 检测能力依赖于 FAPO-Critic-85K 数据集的覆盖度与标注质量，且仅在 Qwen2.5-Math-7B/32B 上验证。Reward Loop 的异步设计虽降低了延迟，但在完全异步 RL 系统中的收敛性尚未得到理论保证。

### 1. 问题定义：Flawed Positive 的形式化

在基于可验证奖励的强化学习（RLVR）中，策略模型 $\pi_\theta$ 针对问题 $q$ 生成推理轨迹 $o = (x_1, x_2, \ldots, x_n)$，其中每个 $x_t$ 代表一个推理步骤。最终答案 $\hat{a}_\pi$ 由规则提取器从 $o$ 中解析得到。**Flawed positive** 的形式化定义为：

$$\hat{a}_{\pi} = a^{*} \text{ and } \exists t \in \{1,2,\ldots,n\} \text{ s.t. step } x_t \text{ is logically invalid}$$

其中 $a^{*}$ 为正确答案。该定义的核心在于：**答案正确但推理过程中至少存在一个逻辑无效的步骤**。这一现象在现有 LLM 中普遍存在，占正确 rollouts 的 20%–40%（Figure 2a），且在标准 RLVR 训练过程中比例持续维持在约 30%（Figure 2c）。

### 2. 基础算法：GRPO 目标函数

FAPO 构建于 Group Relative Policy Optimization (GRPO, Shao et al., 2024) 之上。GRPO 的核心机制是通过群体内相对比较来估计优势，无需训练额外的价值模型。

**优势估计**：对于每组 $G$ 个 rollouts，逐 token 的优势定义为：

$$\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{\mathrm{std}(\{R_i\}_{i=1}^G)}$$

**裁剪替代目标**：策略更新通过最大化以下目标函数实现：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D},\{o_i\}_{i=1}^G\sim\pi_{\theta_{\mathrm{old}}}(\cdot|q)} \frac{1}{G}\sum_{i=1}^G \frac{1}{|o_i|}\sum_{t=1}^{|o_i|} \left\{ \min\left[ \frac{\pi_{\theta}(o_t|q,o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t|q,o_{<t})} \hat{A}_{i,t}, \mathrm{clip}\left(\frac{\pi_{\theta}(o_t|q,o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t|q,o_{<t})}, 1-\epsilon, 1+\epsilon\right) \hat{A}_{i,t} \right] \right\}$$

FAPO 在此基础上采用三项增强策略（clip-higher、token-level loss、overlong reward shaping），修改后的目标函数为：

$$\mathcal{I}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D},\{o_i\}_{i=1}^G\sim\pi_{\theta_{\mathrm{old}}}(\cdot|q)} \frac{1}{\sum_{i=1}^G |o_i|}\sum_{i=1}^G \sum_{t=1}^{|o_i|} \left\{ \min\left[ \frac{\pi_{\theta}(o_t|q,o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t|q,o_{<t})} \hat{A}_{i,t}, \mathrm{clip}\left(\frac{\pi_{\theta}(o_t|q,o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t|q,o_{<t})}, 1-\epsilon_l, 1+\epsilon_h\right) \hat{A}_{i,t} \right] \right\}$$

其中 $\epsilon_l < \epsilon_h$ 为非对称裁剪边界，$\frac{1}{\sum |o_i|}$ 为 token 级平均归一化。

### 3. FAPO 奖励函数：缺陷感知惩罚

标准 RLVR 使用基于答案匹配的二值奖励：

$$R_{\mathrm{RLVR}} = R_{\mathrm{rule}}(o, a^{*}) = \begin{cases} 1, & \text{If } \mathcal{T}(o, a^{*}) \\ -1, & \text{Otherwise} \end{cases}$$

该奖励无法区分 flawed positive 与完全正确的 rollout，两者均获得 $+1$ 的奖励。FAPO 的核心创新在于引入**无参数缺陷惩罚项** $R_{\Delta}$：

$$R_{\mathrm{FAPO}}(o, a^{*} | \boldsymbol{\theta}) = R_{\mathrm{RLVR}}(o, a^{*}) + R_{\Delta}(o, a^{*} | \boldsymbol{\theta})$$

$$R_{\Delta} = \begin{cases} -\lambda, & \text{If } \mathcal{I}(o, a^{*}) \text{ and } \hat{y}_{\boldsymbol{\theta}}(o, a^{*}) = \mathrm{FP} \\ 0, & \text{Otherwise} \end{cases}$$

**关键变量含义**：
- $\mathcal{I}(o, a^{*})$：指示 rollout 答案是否正确（即 $R_{\mathrm{RLVR}} = 1$）
- $\hat{y}_{\boldsymbol{\theta}}(o, a^{*})$：GenRM 对该 rollout 的预测标签，$\mathrm{FP}$ 表示判定为 flawed positive
- $\lambda$：惩罚强度系数，默认 $\lambda = 1$

**因果机制**：当 GenRM 检测到 flawed positive 时，该 rollout 的奖励从 $+1$ 降为 $1 - \lambda$。在群体相对优势框架下，这一调整使得 flawed positive 在组内的相对优势降低，从而减弱策略网络对其推理模式的强化。

### 4. FAPO-GenRM：生成式缺陷检测模型

FAPO-GenRM 是一个紧凑的生成式奖励模型，负责检测 flawed positive 并定位第一步错误的位置。其训练奖励函数为：

$$R_{\mathrm{FAPO-GenRM}} = R_{\mathrm{Outcome}} + R_{\mathrm{Process}}$$

$$R_{\mathrm{Outcome}} = \begin{cases} 1, & \text{If } \hat{y}_\theta = y^* \\ -1, & \text{Otherwise} \end{cases}$$

$$R_{\mathrm{Process}} = \begin{cases} -\frac{|\hat{t}_\theta - t^*|}{n}, & \text{If } \hat{y}_\theta = y^* = \mathrm{FP} \end{cases}$$

**变量含义**：
- $\hat{y}_\theta$：GenRM 预测的标签（$\mathrm{FP}$ 或 $\mathrm{non\text{-}FP}$）
- $y^*$：真实标签
- $\hat{t}_\theta$：GenRM 预测的第一步错误位置
- $t^*$：真实的第一步错误位置
- $n$：推理步骤总数

**奖励设计逻辑**：
- $R_{\mathrm{Outcome}}$ 鼓励正确的二分类判断
- $R_{\mathrm{Process}}$ 在判定为 flawed positive 时，对错误定位偏差施加归一化惩罚，引导模型精准定位缺陷位置

**评估指标**：在 FlawedPositiveBench 上使用精确率、召回率和 F1 分数评估检测能力：

$$\text{precision} = \frac{\#\{\hat{y}_\theta = y^* = \mathrm{FP}\}}{\#\{\hat{y}_\theta = \mathrm{FP}\}}, \quad \text{recall} = \frac{\#\{\hat{y}_\theta = y^* = \mathrm{FP}\}}{\#\{y^* = \mathrm{FP}\}}, \quad F_1 = \frac{2}{1/\text{precision} + 1/\text{recall}}$$

### 5. 自适应优化机制：群体相对优势的隐式调节

FAPO 的奖励调整与 GRPO 的群体相对优势估计相结合，产生**隐式的自适应优化方向切换**：

$$\hat{A}_{i,t} = \left[ r_i - \operatorname{mean}(\{R_i\}_{i=1}^G) \right] / \operatorname{std}(\{R_i\}_{i=1}^G)$$

其中 $r_i = R_{\mathrm{FAPO}}(o_i, a^{*} | \boldsymbol{\theta})$。

**动态机制**（推导见 Appendix A）：
- **训练初期**：策略能力较弱，组内正确 rollout 数量少，flawed positive 即使被惩罚后仍可能高于组均值，保持正优势，充当“踏脚石”帮助模型快速获得正确答案
- **训练后期**：策略能力增强，完全正确的 rollout 增多，组均值上升，被惩罚的 flawed positive 的优势自然转为负值，优化方向自动转向强化可靠推理

这一机制无需手动调整 $\lambda$，通过群体归一化实现了从“利用捷径”到“追求可靠”的平滑过渡。

### 6. 异步奖励环基础设施

为降低 GenRM 推理带来的额外计算开销，FAPO 设计了异步 Reward Loop 架构（Figure 8/9），将 rollout 生成与 GenRM 推理解耦为并行流水线，使训练时间增加控制在 20% 以内。

## 实验与关键发现

### 核心瓶颈与实验动机

在基于可验证奖励的强化学习（RLVR）范式中，一个被长期忽视的关键瓶颈是 **flawed‑positive rollout**：即最终答案正确但推理过程存在逻辑缺陷的生成样本。这类 rollout 在 RLVR 中被赋予与完全正确 rollout 相同的正奖励（+1），导致策略网络强化不可靠的推理模式，限制了最终性能的上限。

预实验（Figure 2）揭示了 flawed positive 的三个关键特征：
1. **普遍性**：在不同规模的 LLM 中，flawed positive 占正确 rollout 的 20%–40%（Figure 2a, 2c），且在 RL 训练过程中该比例持续维持在约 30%，不会自动消失。
2. **双重角色**：在早期学习阶段，flawed positive 充当“踏脚石”帮助模型快速获得正确答案；但随着训练推进，其占比显著下降（Figure 2b），说明继续将其视为正样本会阻碍模型向可靠推理的转变。
3. **惩罚的初步验证**：直接使用 Qwen3‑32B 检测 flawed positive 并给予负奖励，相比基线 RLVR 能显著提高 AIME24 性能，但初期提升较慢（Figure 2d），证实 flawed positive 在训练不同阶段具有截然不同的作用。

这些发现直接催生了 FAPO 的核心设计：对 flawed positive 施加一种无参数的奖励惩罚，并利用群体相对优势估计动态调整优化方向，使模型在早期利用 flawed positive 作为学习捷径，后期则逐渐转向可靠的推理。

### 主要结果

FAPO 在多个数学和通用推理基准上展现出稳定且显著的性能提升。Table 3 汇总了 FAPO‑32B 与 Baseline‑32B 在核心基准上的对比结果：

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/017_Figure_4.jpg]]
*Figure 4: Performance of FAPO-GenRM and FAPO-Reasoning during training. Top row: comparison between FAPO-GenRM and the baseline outcome reward models (setup in Equation 7). Bottom row: comparison between FAPO-Reasoning and the baseline setting (setup in Equation 8). Detailed results in a broader domain can be seen in Table 2 and Table 3*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/025_Table_3.jpg]]
*Table 3: FAPO-Reasoning results in more evaluation benchmarks*

| 基准 | Baseline‑32B | FAPO‑32B | Δ |
|------|-------------|----------|---|
| AIME24 | 38.9 | 42.4 | +3.5 |
| AIME25 | 29.5 | 33.5 | +4.0 |
| GPQA‑Diamond | 51.0 | 53.1 | +2.1 |
| AMC | 85.0 | 91.6 | +6.6 |
| LiveCodeBench | 28.6 | 33.6 | +5.0 |

FAPO 在所有基准上均取得正向提升，尤其在 AMC（+6.6）和 LiveCodeBench（+5.0）上表现突出，验证了方法在不同推理范式（数学竞赛、选择题、代码生成）上的泛化能力。

Figure 1 进一步展示了训练动态：FAPO‑32B 在 AIME24、AIME25 和 GPQA‑Diamond 上均持续优于基线，且 flawed‑positive 比例（左子图）随训练逐步下降，表明模型确实从依赖“捷径”转向了可靠推理。值得注意的是，FAPO 在 GPQA‑Diamond 上的平均 token 使用量（1657）仅略高于基线（1599），说明性能提升并非来自更长的推理链，而是推理质量的实质性改善。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/004_Figure_1.jpg]]
*Figure 1: Flawed-positive ratio and performance comparison between FAPO models and baselines*

### 消融实验

#### GenRM 检测能力的影响

FAPO 的核心依赖 GenRM 对 flawed positive 的检测质量。Figure 5 的消融实验对比了使用不同检测模型对最终 RL 性能的影响：以基础 Qwen3‑4B‑Instruct 替代训练好的 FAPO‑GenRM‑4B 进行 flawed positive 检测，最终 RL 性能显著下降，证明检测能力直接关系到整体效果。这一结果验证了 FAPO‑GenRM 训练的必要性——仅靠现成的指令模型无法提供足够精确的过程级反馈。

#### 惩罚系数 λ 的调优

Table 5 展示了惩罚系数 λ 的消融实验。默认设置 λ=1 在多数情况下表现最佳。当引入 ρ_shift=1/2（对应 λ=−1/3，即对 flawed positive 施加轻微正偏置）时，在 7B 模型上取得了最高的 AIME24 得分 39.6，表明在极小模型上适度保留 flawed positive 的“踏脚石”效应仍有价值。但总体而言，λ=1 在不同模型规模和任务上提供了最稳健的性能，论文将其作为默认配置。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/027_Table_5.jpg]]
*Table 5: Hyper-parameter tuning of λ*

#### 步级奖励设计的对比

FAPO 的奖励设计（对 flawed positive 施加整体惩罚）与传统的步级过程奖励（step‑ratio reward）形成鲜明对比。Figure 7 的消融显示：步级奖励虽然在训练初期带来轻微提升，但随后出现 reward hacking 现象——模型学会生成更长的推理链以最大化步级奖励，导致推理跳跃和性能停滞。这验证了 FAPO 的奖励设计在避免 reward hacking 方面的优越性：通过对整个 rollout 施加惩罚，而非逐步骤奖励，FAPO 不引入额外的可被利用的奖励信号。

### 训练动态与自我纠正分析

Figure 6 的自我纠正分析揭示了 FAPO 训练过程中的一个关键转变：在训练初期，FAPO 模型倾向于通过自我纠正（self‑correction）来修复 flawed positive 中的错误；但随着训练推进，模型逐渐转向直接生成完全正确的 rollout，不再依赖纠正机制。这导致 rollout 长度显著缩短，推理效率提升。这一动态与 FAPO 的核心洞察一致：flawed positive 在早期充当“踏脚石”，但模型最终学会绕过不可靠的推理模式，直接生成高质量的解。

### 计算开销与基础设施

FAPO 引入 GenRM 推理作为额外的训练步骤，但通过异步 Reward Loop 设计（Figure 8）将额外开销控制在可接受范围内。Table 4 的时间分布统计显示：FAPO‑32B 的训练时间相比基线增加不到 20%（GenRM 推理占 14% 的总时间），而 FAPO‑7B 的 GenRM 推理占比为 18%。论文在结果展示中标注了平均 token 使用量，确保性能比较不受推理长度差异的干扰。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/026_Table_4.jpg]]
*Table 4: Time distribution across different RL stages in different settings*

### 公平性说明

所有实验均使用相同的 GRPO 基础算法和增强策略（clip‑higher、token‑level loss、overlong reward shaping），FAPO 与基线使用完全相同的超参数配置（Table 1）。主要推理实验在 Qwen2.5‑Math‑7B 和 Qwen2.5‑32B 上进行，模型选择消除了已有指令微调能力的干扰。FAPO‑GenRM 的训练数据 FAPO‑Critic‑85K 来源于多个模型（7B 至 70B）以保证覆盖度，并使用 Qwen3‑32B 作为教师标注，同时采用共识过滤和鲁棒训练目标降低标签噪声。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_jhqqoimoWt/figures/022_Table_1.jpg]]
*Table 1: Training configurations and hyperparameters of our experiments*

### 已知局限与失败模式

尽管 FAPO 在数学推理任务上取得了显著提升，但当前实验存在以下局限：
- 仅在数学推理任务（AIME、AMC、MATH）和部分通用推理基准（GPQA、LiveCodeBench）上验证，在多选题、多轮对话、智能体 RL 等更广泛场景的有效性尚未验证。
- 使用的基座模型仅限于 Qwen 系列（Qwen2.5‑Math‑7B/32B），尚未在 MoE 架构或更大规模模型上测试。
- 虽然 FAPO 显著降低了 flawed‑positive 比例（Table 6），但并未完全根除，在极端情况下仍可能影响性能。
- 异步 Reward Loop 设计在完全异步 RL 系统中的适用性仍不确定。

## 定位与知识库关联

### 1. 与基线方法的对比与继承

FAPO的核心优化算法建立在**GRPO**（Group Relative Policy Optimization，Shao et al., 2024）之上。GRPO通过群体相对优势估计取代了传统的学习价值模型，有效降低了RL训练的计算开销和训练不稳定性。FAPO完整继承了GRPO的优势估计框架（Equation 1），同时引入了三项已被验证的增强策略：非对称裁剪（clip-higher）、token级损失平均和超长rollout的奖励塑形（overlong reward shaping），这些策略共同构成了FAPO的策略优化基础（Equation 3）。

与标准RLVR（仅使用规则化结果奖励）相比，FAPO的核心创新在于奖励函数的改造。传统RLVR采用二元奖励：答案正确为+1，错误为-1（Equation 4），对所有正确rollout一视同仁。FAPO在此基础上引入了一个无参数的惩罚项 $R_{\Delta}$（Equation 8），对检测到的flawed-positive rollout施加 $-\lambda$ 的惩罚（默认 $\lambda=1$），使奖励信号能够区分“答案正确且推理可靠”与“答案正确但推理有缺陷”的rollout。这种设计直接改变了群体相对优势的估计结果：当一批rollout中flawed positive比例较高时，它们的优势值被压低，而完全正确rollout的优势值相对提升，从而引导策略网络向更可靠的推理方向优化。

在奖励模型层面，FAPO引入了一个生成式奖励模型**FAPO-GenRM**，这与传统的判别式PRM（如Qwen2.5-Math-PRM-72B）有本质区别。判别式PRM通常对每个推理步骤进行“好/坏”的二分类，但容易出现“过度批评”（over-critic）现象——高召回但低精度，即大量正确步骤被误判为错误（Figure 3）。FAPO-GenRM通过生成式范式直接定位第一步错误的位置，并采用包含结果奖励和过程惩罚的复合奖励函数（Equation 7）进行训练，显著提升了检测精度和F1分数，同时将推理token消耗控制在较低水平。

### 2. 适用边界与约束条件

FAPO的有效性建立在以下关键前提之上：

- **可验证奖励的存在**：FAPO依赖规则化的结果奖励（如数学答案匹配、代码测试用例通过）作为基础信号。对于缺乏明确可验证标准的开放域任务（如创意写作、对话质量评估），该方法难以直接迁移。
- **flawed positive的可检测性**：FAPO-GenRM需要大量标注数据（FAPO-Critic-85K）进行训练，且标注依赖更强的教师模型（Qwen3-32B）和共识过滤机制来降低噪声。在推理步骤难以精确定义或标注成本过高的领域，GenRM的训练可能面临瓶颈。
- **基座模型的推理能力**：当前实验仅在Qwen2.5-Math-7B和Qwen2.5-32B上进行验证。这些模型本身具有较强的数学推理基础，FAPO的作用是在此基础上进一步抑制不可靠的推理模式。对于推理能力较弱的基座模型，flawed positive的比例和影响可能呈现不同特征，方法的有效性需要额外验证。
- **计算开销的容忍度**：尽管FAPO通过异步Reward Loop设计将GenRM推理带来的额外训练时间控制在20%以内（Table 4），但在计算资源极度受限的场景下，这一开销仍可能成为部署障碍。

### 3. 局限性分析

论文明确指出的局限性包括：

1. **任务领域局限**：当前实验主要集中在数学推理任务（AIME、AMC、MATH等）和部分科学推理任务（GPQA-Diamond）。在多选题、多轮对话、智能体强化学习等更广泛的场景中，FAPO的有效性尚未验证。

2. **模型架构局限**：验证仅在Qwen系列的dense架构模型上进行，尚未在MoE（Mixture of Experts）架构或更大规模模型（如70B+）上测试。不同架构对flawed positive的敏感性和FAPO的惩罚响应可能存在差异。

3. **flawed positive未完全根除**：尽管FAPO显著降低了flawed positive的比例（Figure 1左子图），但并未将其完全消除。在极端情况下，残留的不可靠推理仍可能影响模型输出的可信度。

4. **异步系统的通用性**：论文提出的异步Reward Loop设计（Figure 8）在当前的半同步训练框架中有效降低了GPU空闲时间，但其在完全异步RL系统中的适用性仍不确定。

### 4. 开放问题

基于论文的分析和已知边界，以下问题值得进一步探索：

- **跨任务泛化机制**：FAPO的检测惩罚机制在非数学推理任务（如法律推理、医学诊断、开放域问答）中该如何适配？是否需要重新定义“逻辑无效步骤”的标准，或者设计任务特定的GenRM训练策略？

- **λ的自适应调节**：当前λ被固定为常数（默认1），但消融实验（Table 5）显示不同模型规模的最优λ可能不同（如7B模型在 $\rho_{\text{shift}}=1/2$ 即等效 $\lambda=-1/3$ 时取得最高AIME24得分39.6）。能否设计一种自动化机制，根据训练过程中的flawed positive比例或模型能力动态调整λ，实现更精细的优化控制？

- **GenRM效率的进一步优化**：当前FAPO-GenRM-4B虽然已大幅压缩了推理成本，但仍占训练时间的相当比例。能否通过知识蒸馏、量化、或设计更轻量的检测头来进一步降低token预算，实现接近实时的flawed positive检测？

- **与其他RL增强技术的协同**：FAPO专注于奖励信号的修正，而现有研究中还存在多种避免reward hacking的策略（如KL散度正则化、策略熵约束等）。FAPO与这些技术的结合是否能激发更大的性能提升，尚待系统研究。

- **flawed positive的因果机制**：论文揭示了flawed positive在训练早期的“踏脚石”作用，但其产生的深层原因——是模型的能力不足、探索策略的偏差、还是推理任务的固有模糊性——仍有待更深入的因果分析。理解这一机制可能催生更根本的解决方案。

## 原文 PDF

![[paperPDFs/ICLR_2026/FAPO_Flawed_Aware_Policy_Optimization_for_Efficient_and_Reliable_Reasoning.pdf]]
