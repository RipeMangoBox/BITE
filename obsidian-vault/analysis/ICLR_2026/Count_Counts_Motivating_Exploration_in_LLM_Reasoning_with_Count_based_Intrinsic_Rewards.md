---
title: "Count Counts: Motivating Exploration in LLM Reasoning with Count-based Intrinsic Rewards"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Count_Counts_Motivating_Exploration_in_LLM_Reasoning_with_Count_based_Intrinsic_Rewards.pdf
openreview_forum_id: 9xIBbfItGP
aliases:
- CCMELRCBIR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用LLM推理中已知且确定性的状态转移特性简化不确定性贝尔曼方程，将Q值的不确定性传播转化为局部奖励不确定性的累积，并通过Coin Flipping Network (CFN)估计状态伪计数作为内在奖励，驱动策略探索新颖的推理轨迹。"
primary_logic: "在自包含的自回归推理任务（如数学解题）中，状态转移函数是确定性且已知的，这消除了转移不确定性，使得认知不确定性传播仅依赖于局部奖励不确定性；基于此，可以将基于计数的状态新颖性（CFN）用作内在奖励，实现可靠且可扩展的深度探索。"
claims:
- "标准GRPO依赖稀疏结果奖励，导致过早收敛于次优解，而MERCI引入了基于计数的内在奖励鼓励探索。"
- "LLM的MDP具有已知和确定性的转移函数，这简化了不确定性贝尔曼方程。"
- "简化后的UBE将Q值不确定性传播转化为局部奖励不确定性的累积，并用CFN估计的伪计数代理。"
- "MERCI显著提升了复杂推理基准上的性能，缓解了标准算法陷入重复解的问题。"
---

# Count Counts: Motivating Exploration in LLM Reasoning with Count-based Intrinsic Rewards

> [!tip] 核心洞察
> 在自包含的自回归推理任务（如数学解题）中，状态转移函数是确定性且已知的，这消除了转移不确定性，使得认知不确定性传播仅依赖于局部奖励不确定性；基于此，可以将基于计数的状态新颖性（CFN）用作内在奖励，实现可靠且可扩展的深度探索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 计数重要：通过基于计数的内在奖励激励大语言模型推理探索 |
| 英文题名 | Count Counts: Motivating Exploration in LLM Reasoning with Count-based Intrinsic Rewards |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9xIBbfItGP) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MERCI |
| Dataset | Math Reasoning (6 benchmarks avg), Bird (SQL generation), Spider (SQL generation, OOD) |

> [!tip] 效果简介
> - Math Reasoning (6 benchmarks avg) 上，pass@k (average) 为 GRPO+MERCI 67.4，对比 GRPO 65.8，变化 +1.6。
> - Math Reasoning (6 benchmarks avg) 上，mean@k (average) 为 DAPO+MERCI 44.9，对比 DAPO 42.2，变化 +2.7。
> - Bird (SQL generation) 上，Greedy accuracy 为 GRPO+MERCI 63.0，对比 GRPO 60.7，变化 +2.3。

## 概述

### 问题瓶颈

当前主流的大语言模型（LLM）强化学习（RL）训练范式——如 **GRPO**（Shao et al., 2024）和 **DAPO**（Yu et al., 2025）——主要依赖稀疏的、基于结果的奖励信号。这种稀疏性导致模型在复杂多步推理中缺乏有效的*深度探索*机制：策略倾向于过早收敛到重复且次优的推理模式，而非持续发现更优的解题路径。虽然熵正则化或ε-greedy等方法提供了一定程度的探索，但它们通常是*无方向*的，无法引导策略系统性地探索认知不确定性的区域。

### 核心洞察与方法定位

MERCI 的核心洞察源于对LLM推理中马尔可夫决策过程（MDP）结构的重新审视：在自包含的自回归推理任务（如数学解题、SQL生成）中，状态转移是**确定性且已知**的——下一个状态 $s'$ 就是当前token序列 $s$ 与所选动作 $a$ 的拼接。这一性质从根本上简化了不确定性贝尔曼方程（Uncertainty Bellman Equation, UBE），将原本难以处理的全局Q值不确定性传播问题，**退化为局部奖励不确定性的简单累积**。

基于此，MERCI 引入了一个轻量级的 **Coin Flipping Network (CFN)**，通过估计状态伪计数来量化局部奖励的认知不确定性，并将其转化为鼓励探索新颖推理轨迹的内在奖励。该方法可无缝集成到GRPO等高级RL框架中，仅需修改优势估计的计算方式。

### 方法谱系与知识库定位

MERCI 处于**基于不确定性的探索**与**基于计数的探索**两条研究脉络的交汇点：

| 维度 | 基线方法 | MERCI的改进 |
|------|----------|-------------|
| **探索信号** | 无内在奖励（仅依赖熵正则化）；或基于RND的内在奖励（**iMentor**, Gao et al., 2025） | 利用CFN估计的状态伪计数计算局部奖励方差，并通过UBE正确累积为轨迹级内在奖励 |
| **认知不确定性量化** | 无法在LLM规模上高效估计全局Q值不确定性 | 利用确定性转移简化UBE，仅需估计局部奖励不确定性，用轻量级CFN实现可扩展估计 |
| **优势估计** | GRPO使用组内归一化的结果奖励作为优势 $A_{\text{old}}$ | 在 $A_{\text{old}}$ 基础上增加由CFN估计的、经过预算控制和标准化的内在探索奖励 $A_{\text{exploration}}$，通过剪切机制合并为 $A_{\text{new}}$ |

与基于熵的优势塑造（**Entropy Adv.**, Cheng et al., 2025）等探索基线相比，MERCI的核心区别在于其探索信号具有*认知不确定性理论支撑*，而非简单的策略熵最大化。

### 主要结果概要

MERCI在多个复杂推理基准上一致地提升了强基线的性能：

- **数学推理**（6个基准平均）：GRPO+MERCI 将 pass@k 从 65.8 提升至 **67.4**（+1.6），DAPO+MERCI 将 mean@k 从 42.2 提升至 **44.9**（+2.7）。
- **SQL生成**：在Bird数据集上，GRPO+MERCI 将贪婪解码准确率从 60.7 提升至 **63.0**（+2.3）；在跨域泛化的Spider数据集上，从 74.8 提升至 **78.0**（+3.2）。
- **跨域迁移**：在GPQA上，DAPO+MERCI 将 pass@16 从 70.5 提升至 **73.7**（+3.2）。

消融实验进一步验证了关键设计选择：移除噪声过滤机制会导致平均 pass@k 从 67.4 骤降至 63.8；将GRPO基线训练步数扩展至260步反而使 pass@k 下降至 61.6（vs. 65.8），说明单纯增加训练无法解决过早收敛问题，而MERCI有效缓解了这一瓶颈。

### 局限与开放问题

1. **CFN预训练开销**：CFN需要在骨干模型生成的响应上进行预训练，增加了训练流程的复杂性。
2. **确定性转移假设**：当前方法针对自包含推理任务设计，直接推广到涉及工具调用、网络搜索等非确定性交互的开放域环境可能面临挑战。
3. **超参数敏感性**：内在奖励的预算控制超参数（百分位过滤比例、余弦衰减步数等）需要针对不同任务调整，缺乏自适应机制。
4. **规模验证缺失**：尚未在更大规模模型（如 >70B）上验证方法的有效性和计算开销。

## 背景与动机

### 大语言模型推理的强化学习瓶颈

近年来，强化学习（RL）已成为提升大语言模型（LLM）复杂推理能力的关键范式。以**GRPO**（Shao et al., 2024）为代表的算法通过组内归一化的结果奖励来优化策略，在数学推理、代码生成等任务上取得了显著进展。然而，这类方法面临一个根本性瓶颈：**奖励信号的稀疏性与探索机制的匮乏**。

在典型的多步推理场景中，模型仅在生成完整轨迹后才获得一个标量结果奖励（正确/错误）。这种稀疏的奖励结构使得标准RL算法高度依赖有限的探索策略——主要是熵正则化或隐式的ε-greedy行为。熵正则化本质上是一种无方向的探索：它均匀地鼓励所有非最优动作，而非有针对性地引导模型探索**认知不确定性高**的区域。当模型过早发现某些能获得正奖励的推理模式时，策略会迅速收敛到这些局部最优解，陷入重复且次优的推理轨迹，丧失了发现更优解的能力。

### 现有探索机制的局限

当前LLM推理中的探索增强方法主要沿两条路径展开：

- **基于熵的方法**（如Entropy Advantage Shaping）：通过熵正则化或优势塑造鼓励策略保持高熵，但其探索方向是无差别的，无法区分“值得探索的新颖状态”与“已知的次优状态”。
- **基于预测误差的方法**（如RND）：利用随机网络蒸馏的预测误差作为内在奖励，但在LLM的高维离散状态空间中，预测误差的估计方差大、计算开销高，难以可靠地指导探索。

这些方法的共同缺陷在于：**缺乏对认知不确定性的原则性量化与传播机制**。它们无法系统性地评估“模型对当前推理状态的知识缺乏程度”，因而无法将探索预算精准分配到最需要探索的推理分支上。

### 关键洞察：确定性转移带来的简化

本工作的核心动机源于一个关键的结构性观察：**在自包含的自回归推理任务（如数学解题、SQL生成）中，LLM的底层马尔可夫决策过程（MDP）具有已知且确定性的状态转移函数**。具体而言，给定当前token序列 $s$ 和选择的动作 $a$（下一个token），下一状态 $s'$ 是确定性的拼接结果：$s' = (s, a)$。

这一特性深刻改变了认知不确定性传播的计算复杂性。在通用MDP中，Q值的不确定性传播需要同时考虑奖励不确定性和转移不确定性，导致不确定性贝尔曼方程（Uncertainty Bellman Equation, UBE）难以求解。然而，当转移函数是确定性且已知时，**转移不确定性消失**，UBE退化为一个简洁的形式：Q值的不确定性受限于即时奖励不确定性加上下一状态的期望不确定性，可以通过沿轨迹递归累积局部奖励不确定性来估计。

这一简化意味着：**如果能够高效估计每个推理状态的局部奖励不确定性，就可以原则性地构建轨迹级的内在探索奖励**——这正是MERCI方法的核心理论基础。

### 本文动机与目标

基于上述分析，本文提出**MERCI**（Motivating Exploration in LLM Reasoning with Count-based Intrinsic Rewards），目标是：

1. **利用确定性转移简化UBE**，将认知不确定性传播转化为局部奖励不确定性的累积，为LLM推理提供原则性的探索信号。
2. **引入基于计数的伪计数估计**（Coin Flipping Network, CFN），以轻量级的方式估计状态访问新颖性，作为局部奖励不确定性的代理。
3. **将内在探索奖励无缝集成到现有RL框架**（如GRPO、DAPO）中，通过预算控制和标准化机制，在不破坏结果奖励信号的前提下，驱动策略探索新颖的推理轨迹，缓解过早收敛问题。

## 核心创新

MERCI的核心创新在于将**基于计数的内在探索奖励**系统性地引入大语言模型（LLM）的强化学习（RL）推理训练中，以解决现有方法因依赖稀疏结果奖励而导致的**探索不足与过早收敛**问题。其关键洞察在于，LLM自回归生成过程的**状态转移是确定性且已知的**（即下一个状态 $s'$ 就是当前状态 $s$ 与动作 $a$ 的拼接），这一特性从根本上简化了认知不确定性传播的复杂性。

### 从全局不确定性到局部奖励不确定性的简化

传统强化学习中，基于**不确定性贝尔曼方程（Uncertainty Bellman Equation, UBE）** 的探索需要估计Q值函数的全局不确定性，这在LLM的巨量状态空间下是不可行的。MERCI利用确定性转移这一性质，将UBE简化为仅需估计**局部奖励不确定性**的递归累积：

$$U ^ { h } ( s , a ) \leq \mathbb { V } _ { t } [ \hat { r } ^ { h } ( s ) ] + \sum _ { s ^ { \prime } , a ^ { \prime } } \pi _ { s ^ { \prime } , a ^ { \prime } } ^ { h } P _ { s ^ { \prime } s a } ^ { h } U ^ { h + 1 } ( s ^ { \prime } , a ^ { \prime } )$$

这意味着，Q值的不确定性上界仅由当前状态的即时奖励不确定性加上下一状态的期望不确定性构成，从而将棘手的全局不确定性传播问题转化为可递归计算的局部量。

### 基于伪计数的局部奖励不确定性估计

为高效估计局部奖励不确定性 $\mathbb{V}[\hat{r}(s)]$，MERCI引入了一个轻量级的**硬币翻转网络（Coin Flipping Network, CFN）**。CFN通过一个简单的监督学习目标，预测每个状态对应的随机硬币翻转向量的均值，从而隐式编码状态的访问频次：

$$f _ { \phi } ^ { * } ( s ) = \underset { \phi } { \arg \min } \sum _ { i = 1 } ^ { | \mathcal { D } _ { \mathrm { c f n } } | } \| \mathbf { c } _ { i } - f _ { \phi } ( s _ { i } ) \| ^ { 2 }$$

训练完成后，CFN输出的平方范数即可作为状态访问次数倒数的近似估计：

$$\frac { 1 } { d } \| f _ { \phi } ( s ) \| ^ { 2 } \approx \frac { 1 } { \mathcal { N } ( s ) }$$

基于此，局部奖励不确定性 $\mathbb{V}[\hat{r}(s)]$ 可被直接代理为 $\frac{1}{d}\|f_\phi(s)\|^2$。这一设计使得MERCI无需维护庞大的计数表或复杂的密度模型，即可在LLM的隐藏状态空间上实现可扩展的伪计数估计。

### 从局部方差到轨迹级内在奖励的正确累积

MERCI严格遵循简化UBE所规定的方差传播规则，将轨迹上各token的局部奖励方差**先求和再开方**，而非简单地对每步标准差求和。对于经过过滤（详见“方法谱系与知识库定位”中的奖励过滤管线）后保留的token集合 $\mathbb{I}$，轨迹级的内在探索奖励定义为：

$$\mathcal { B } = \sqrt { \frac { 1 } { l } \sum _ { i \in \mathbb { I } } \Big ( \frac { 1 } { d } \| f _ { \phi } ( s _ { h i d d e n } ^ { i } ) \| ^ { 2 } \Big ) }$$

消融实验证实，若改用每步标准差直接求和的方式计算奖励，将导致性能显著下降，验证了这一基于UBE的方差累积方式的正确性。

### 与基础RL算法的优势整合

MERCI作为一种即插即用的探索增强模块，可无缝集成到GRPO等主流LLM强化学习框架中。其核心改动在于**优势估计**环节：在GRPO原有的组内归一化结果优势 $\hat{A}_{\mathrm{old}}$ 基础上，叠加由CFN内在奖励标准化后得到的探索优势 $\hat{A}_{\mathrm{exploration}}$，并通过剪切机制防止内在奖励淹没负优势轨迹的信号：

$$\hat { A } _ { \mathrm { n e w } } ^ { i } = \begin{cases} \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1+\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } \ge 0 \\ \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1-\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } < 0 \end{cases}$$

这一设计使得MERCI在保持原有RL算法优化目标的前提下，为策略提供了有方向性的探索激励——鼓励模型访问CFN判定为新颖的推理状态，从而逃离重复且次优的推理模式。与依赖熵正则化或ε-greedy等无方向探索的基线方法相比，MERCI的探索信号由认知不确定性驱动，理论上更具针对性。实验也表明，单纯扩展GRPO的训练步数反而导致pass@k下降（从65.8降至61.6），而MERCI则有效缓解了这一过早收敛问题。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the MERCI framework. Two separate networks are used: a policy network $\pi _ { \theta }$ trained with RL, and a CFN network that provides an intrinsic reward. The CFN network, initialized from the same SFT checkpoint $\pi _ { 0 }$ , estimates state novelty to guide the exploration of $\pi _ { \theta }$

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/002_Figure_2.jpg]]
*Figure 2: The entire pipeline of bonus filtering. Step 1: We rank all tokens within a response by their associated bonus values and retain only those falling within a predefined top percentile (e.g., the top 50% in this figure). Step 2: We only preserve clusters of adjacent tokens that consistently exhibit elevated bonuses ( $\mathrm { e . g . , }$ 3 consecutive tokens in this figure). Step 3: For example, in a math reasoning task without external tools, any Python code potentially generated during LLM rollouts is semantically irrelevant and noisy, so we exclude them from the overall bonus calculation*

MERCI框架的核心设计理念是将基于计数的内在探索奖励注入到标准的LLM强化学习流程中，以解决稀疏结果奖励导致的过早收敛与探索不足问题。其整体架构由两个独立网络和一条奖励过滤管线构成，如图1所示。

### 双网络协作架构

框架维护两个独立的神经网络，二者从同一个SFT检查点 $\pi_0$ 初始化，但在训练中承担不同角色：

- **策略网络 $\pi_\theta$**：负责生成推理轨迹，由底层RL算法（如GRPO或DAPO）基于增强后的优势信号进行参数更新。该网络执行标准的自回归生成，每步动作 $a$ 是选择下一个token，状态转移是确定性的：$s' = (s, a)$，即新状态为当前token序列与所选动作的拼接。

- **Coin Flipping Network (CFN)**：一个轻量级网络，用于估计状态伪计数并输出局部奖励不确定性。CFN的核心机制源自Lobel等人2023年的“Flipping Coins”方法：对每个状态 $s$，CFN学习预测一组随机硬币翻转向量 $\mathbf{c}_i$ 的均值，其学习目标为：

$$f _ { \phi } ^ { * } ( s ) = \underset { \phi } { \arg \min } \sum _ { i = 1 } ^ { | \mathcal { D } _ { \mathrm { c f n } } | } \| \mathbf { c } _ { i } - f _ { \phi } ( s _ { i } ) \| ^ { 2 }$$

CFN输出的平方范数近似于状态访问次数的倒数，从而隐式编码了访问计数信息：

$$\frac { 1 } { d } \| f _ { \phi } ( s ) \| ^ { 2 } \approx \frac { 1 } { \mathcal { N } ( s ) }$$

在训练前，CFN需先在骨干模型生成的响应上进行预训练，使其获得对稀有状态的基本识别能力。在RL训练阶段，CFN与策略网络协同训练，持续更新其对状态新颖性的估计。

### 信息流与模块关系

框架的信息流可概括为以下步骤：

1. **轨迹生成**：策略网络 $\pi_\theta$ 对每个输入问题采样一组候选推理轨迹。
2. **结果奖励计算**：对每条完整轨迹，根据最终答案的正确性计算稀疏的结果奖励 $r_i$，并通过GRPO的组内归一化得到原始优势 $\hat{A}_{\mathrm{old}}^i$。
3. **不确定性估计**：CFN对轨迹中每个token的隐藏状态 $s_{\mathrm{hidden}}^i$ 输出局部奖励方差 $\frac{1}{d}\|f_\phi(s_{\mathrm{hidden}}^i)\|^2$，作为认知不确定性的代理。
4. **奖励过滤管线 (Bonus Filtering Pipeline)**：如图2所示，内在奖励经过三级过滤以控制预算并稳定训练：
   - **百分位过滤**：仅保留每个响应中奖励值处于预设前百分位（如top 30%）的token。
   - **空间连贯性过滤**：仅保留持续表现出高奖励的相邻token簇，过滤孤立的高奖励噪声点。
   - **噪声抑制过滤**：排除异常波动token，防止其干扰整体奖励计算。
5. **轨迹内在奖励合成**：基于简化不确定性贝尔曼方程（UBE）的方差传播原理，将过滤后保留的局部方差累积后取平方根，得到轨迹级探索奖励：

$$\mathcal { B } = \sqrt { \frac { 1 } { l } \sum _ { i \in \mathbb { I } } \Big ( \frac { 1 } { d } \| f _ { \phi } ( s _ { h i d d e n } ^ { i } ) \| ^ { 2 } \Big ) }$$

   该设计遵循了正确的方差累积方式（先求和再开方），而非逐token标准差的简单相加。
6. **优势合并模块 (Advantage Combination Module)**：将标准化后的探索奖励 $\hat{A}_{\mathrm{exploration}}^i$ 与原始优势线性组合，并通过剪切因子 $\alpha$ 防止内在奖励淹没负优势轨迹的信号：

$$\hat { A } _ { \mathrm { n e w } } ^ { i } = \begin{cases} \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1+\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } \ge 0 \\ \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1-\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } < 0 \end{cases}$$

   其中 $\gamma$ 为探索系数，在训练过程中按余弦衰减至初始值的10%（约在第200步），以逐步收缩探索预算。

### 理论根基：简化不确定性贝尔曼方程

MERCI的设计建立在一个关键洞察之上：在自包含的LLM推理任务中，状态转移函数 $P$ 是已知且确定性的。这一性质将通用的不确定性贝尔曼方程简化为可递归估计的形式：

$$U ^ { h } ( s , a ) \leq \mathbb { V } _ { t } [ \hat { r } ^ { h } ( s ) ] + \sum _ { s ^ { \prime } , a ^ { \prime } } \pi _ { s ^ { \prime } , a ^ { \prime } } ^ { h } P _ { s ^ { \prime } s a } ^ { h } U ^ { h + 1 } ( s ^ { \prime } , a ^ { \prime } )$$

该方程表明，在确定性转移下，Q值的不确定性受限于即时奖励不确定性加上下一状态的期望不确定性，而转移不确定性被完全消除。这使得原本难以在LLM规模上估计的全局Q值不确定性，退化为局部奖励不确定性的累积问题——这正是CFN伪计数估计能够有效代理的核心原因。

## 核心模块与公式推导

MERCI 的核心架构由四个协同模块构成，其设计根植于一个关键洞察：在自包含的 LLM 推理任务中，状态转移函数是确定性且已知的，这从根本上简化了认知不确定性的传播机制。

### 确定性转移下的不确定性贝尔曼方程简化

在标准强化学习中，认知不确定性（Epistemic Uncertainty）通过不确定性贝尔曼方程（UBE）传播，其一般形式涉及对转移函数不确定性的积分，在 LLM 规模下难以处理。MERCI 的关键突破在于识别出：对于自回归生成任务，下一状态 $s'$ 就是当前状态 $s$ 与动作 $a$ 的拼接，即 $s' = (s, a)$，转移函数 $P$ 是确定且已知的。这一性质将 UBE 简化为：

$$U ^ { h } ( s , a ) \leq \mathbb { V } _ { t } [ \hat { r } ^ { h } ( s ) ] + \sum _ { s ^ { \prime } , a ^ { \prime } } \pi _ { s ^ { \prime } , a ^ { \prime } } ^ { h } P _ { s ^ { \prime } s a } ^ { h } U ^ { h + 1 } ( s ^ { \prime } , a ^ { \prime } )$$

其中 $U^h(s,a)$ 是 Q 值的后验方差（认知不确定性），$\mathbb{V}_t[\hat{r}^h(s)]$ 是即时奖励的局部不确定性。该公式表明：在确定性转移下，Q 值的不确定性传播退化为**局部奖励不确定性的累积**——不再需要估计转移不确定性，只需沿轨迹累加每一步的奖励方差。这为使用基于计数的状态新颖性作为探索奖励提供了理论依据：奖励不确定性 $\mathbb{V}[\hat{r}(s)]$ 与状态访问次数成反比，即 $\mathbb{V}[\hat{r}(s)] \propto 1/\mathcal{N}(s)$。

### Coin Flipping Network (CFN) 与伪计数估计

CFN 是实现上述理论的可扩展引擎。它是一个轻量级网络，从策略网络的隐藏状态出发，通过监督学习估计状态的伪计数。其学习目标为：

$$f _ { \phi } ^ { * } ( s ) = \underset { \phi } { \arg \min } \sum _ { i = 1 } ^ { | \mathcal { D } _ { \mathrm { c f n } } | } \| \mathbf { c } _ { i } - f _ { \phi } ( s _ { i } ) \| ^ { 2 }$$

其中 $\mathbf{c}_i$ 是随机生成的硬币翻转向量（维度 $d$），$f_\phi(s)$ 是 CFN 对状态 $s$ 的输出。训练后，CFN 输出的平方范数近似于状态访问次数的倒数：

$$\frac { 1 } { d } \| f _ { \phi } ( s ) \| ^ { 2 } \approx \frac { 1 } { \mathcal { N } ( s ) }$$

这个值直接作为局部奖励方差的代理估计，即 $\mathbb{V}[\hat{r}(s)] = \frac{1}{d}\|f_\phi(s)\|^2$。CFN 的维度 $d$ 直观上对应硬币翻转的次数，论文中设置为 20。

### 轨迹级内在奖励与预算控制

根据简化 UBE 的方差累积原则，轨迹级的内在奖励不是各步标准差的简单求和，而是先累积方差再开方：

$$\mathcal { B } = \sqrt { \frac { 1 } { l } \sum _ { i \in \mathbb { I } } \Big ( \frac { 1 } { d } \| f _ { \phi } ( s _ { h i d d e n } ^ { i } ) \| ^ { 2 } \Big ) }$$

其中 $\mathbb{I}$ 是经过三层过滤后保留的 token 索引集合。过滤流程（Figure 2）包括：(1) **百分位过滤**：仅保留奖励值处于前 30% 的 token；(2) **空间连贯性过滤**：仅保留形成连续簇的高奖励 token；(3) **噪声抑制过滤**：排除孤立的高奖励 token，防止噪声干扰。

过滤后的奖励 $\mathcal{B}$ 经过组内标准化得到探索优势 $\hat{A}_{\mathrm{exploration}}$，然后与 GRPO 的原始优势 $\hat{A}_{\mathrm{old}}$ 线性组合，并通过剪切因子 $\alpha$ 防止内在奖励淹没负优势轨迹：

$$\hat { A } _ { \mathrm { n e w } } ^ { i } = \begin{cases} \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1+\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } \ge 0 \\ \min(\hat { A } _ { \mathrm { o l d } } ^ { i } + \gamma \hat { A } _ { \mathrm { e x p l o r a t i o n } } ^ { i }, (1-\alpha)\hat { A } _ { \mathrm { o l d } } ^ { i }) & \text{if } \hat { A } _ { \mathrm { o l d } } ^ { i } < 0 \end{cases}$$

其中 $\gamma$ 是探索系数，采用余弦衰减策略（在第 200 步衰减至初始值的 10%），实现预算感知的探索控制。

## 实验与分析

### 核心瓶颈的实证验证：GRPO的过早收敛问题

MERCI的核心动机源于一个关键的实证观察：标准GRPO在复杂推理任务上存在严重的过早收敛问题。如Table 8(a)所示，将GRPO基线的训练步数从常规的200步**扩展到260步**，不仅未能带来性能提升，反而导致平均pass@k从**65.8下降至61.6**。这一现象揭示了一个深层问题——单纯增加训练计算量无法解决探索不足的困境，模型在稀疏结果奖励的引导下会迅速锁定某些次优推理模式，并反复生成相似的解路径。

MERCI通过引入基于计数的内在奖励，有效缓解了这一瓶颈。在相同扩展训练设置下，GRPO+MERCI的pass@k显著优于普通GRPO，证明了内在探索信号对于跳出局部最优的因果作用。

### 主要结果：数学推理与SQL生成

MERCI在数学推理和SQL生成两大领域均实现了对强基线的稳定提升。Table 1(a)的pass@k结果显示，在六个数学推理基准（AIME2024/2025、MATH500、OlympiadBench、College Math、Minerva）上，**GRPO+MERCI的平均pass@k达到67.4，较GRPO基线的65.8提升了+1.6**，在RL模型中取得最优。Table 1(b)的mean@k结果进一步验证了方法的鲁棒性：**DAPO+MERCI的平均mean@k为44.9，较DAPO基线的42.2提升+2.7**，在所有RL方法中同样位居第一。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/003_Table_1.jpg]]
*Table 1: Performance on mathematical reasoning benchmarks with pass@k and mean@k. The highlighted color represents the best within RL models, while underlined represents the second best. (a) pass@k results*

在SQL生成任务上，MERCI展现了更强的跨域泛化能力。Table 2显示，在Bird（域内）测试集上，GRPO+MERCI的贪婪解码准确率从60.7提升至**63.0（+2.3）**；而在Spider（域外）测试集上，提升幅度更大，贪婪准确率从74.8跃升至**78.0（+3.2）**。这种域外增益放大的现象，与MERCI鼓励模型探索多样化推理路径的内核机制高度一致——当面对与训练分布不同的查询模式时，具备更丰富探索经验的策略能够更灵活地适应。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/004_Table_2.jpg]]
*Table 2: (b) mean@k results*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/005_Table_2.jpg]]
*Table 2: Performance on SQL generation benchmarks with greedy sampling and pass@k*

跨域实验（Table 7）进一步佐证了这一结论。在GPQA（科学推理）上，**DAPO+MERCI的pass@16达到73.7，较DAPO基线的70.5提升+3.2**；在MMLU-Pro上，pass@1从37.4提升至39.5（+2.1）。这些结果表明，MERCI所激励的探索行为并非过拟合于数学推理的表面模式，而是促进了更具泛化性的推理能力。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_9xIBbfItGP/figures/022_Table_7.jpg]]
*Table 7: Results of cross-domain experiments on MMLU-Pro and GPQA*

### 消融研究：奖励过滤机制的关键作用

MERCI的内在奖励管线包含三个关键过滤阶段：百分位过滤、空间连贯性过滤和噪声抑制过滤。Table 9的消融实验揭示了各模块的贡献：

- **移除噪声过滤**导致平均pass@k从67.4骤降至**63.8（-3.6）**，是所有消融中性能退化最严重的操作。这证实了内在奖励的预算控制对于训练稳定性的核心作用——未经约束的探索信号会引入高方差梯度，干扰策略对结果奖励的有效学习。
- 正确的方差累积方式同样至关重要。附录G.2.4的消融显示，若将每个token的局部标准差直接求和（而非先累积方差再开方），性能显著下降。这从实证角度验证了基于UBE推导的方差传播公式的正确性——不确定性应以方差形式沿轨迹累积，而非简单线性叠加。

### 探索动态与不确定性可视化

Figure 3-6展示了CFN对推理轨迹中每个token分配的认知不确定性。红色高亮区域主要集中在三类位置：（1）新颖的推理路径分支点；（2）Python代码及其输出；（3）专门数学术语。这一模式表明，CFN并非简单地对所有低频token赋予高不确定性，而是有选择性地识别对推理结果有实质性影响的决策节点。

Figure 7的统计分析进一步量化了这一现象：在响应中排名前30%的高奖励token片段，其出现频率分布呈现长尾特征，说明内在奖励确实在引导策略访问训练中罕见的推理状态。

训练动态图（Figure 13）从宏观视角揭示了MERCI的探索效果。与普通GRPO相比，MERCI在训练过程中维持了更高的响应多样性，同时验证集准确率的提升曲线更加平滑，未出现GRPO常见的“准确率攀升后骤降”的过拟合-崩溃模式。这印证了内在奖励通过“密集化”多条有效推理轨迹，增强了策略的校准能力。

### 探索系数调度的影响

Table 10考察了内在奖励系数γ的余弦衰减速度对性能的影响。结果显示，**在200步时将γ衰减至初始值的10%**，在pass@k和mean@k上均取得了最佳的整体表现。过快衰减（如100步衰减至10%）导致探索不足，策略过早收敛；过慢衰减（如400步衰减至10%）则使内在奖励过度干扰后期策略精化，损害最终性能。这一发现为内在奖励的生命周期管理提供了实用指南。

### 失败模式与局限

尽管MERCI在整体上表现优异，但从实验细节中可识别出若干边界情况：

1. **CFN预训练依赖性**：CFN需要先在骨干模型生成的响应上进行预训练，才能有效估计伪计数。当骨干模型本身生成能力较弱时，CFN对“新颖性”的初始判断可能存在偏差，导致早期训练阶段的内在奖励信号质量下降。
2. **超参数敏感性**：奖励过滤的百分位阈值、空间连贯性窗口大小、噪声抑制强度等参数需要针对任务进行调整。Table 5和Table 6显示，数学推理和SQL生成任务使用了不同的过滤配置，表明这些参数的迁移性有限，缺乏自适应机制。
3. **确定性转移假设的边界**：当前方法在数学和SQL等自包含推理任务上验证有效，但在涉及外部工具调用或对话交互的场景中，确定性转移假设不再成立，UBE的简化推导需要重新审视。跨域实验（Table 7）虽展现了泛化潜力，但GPQA和MMLU-Pro本质上仍属于自包含推理范畴，尚未触及真正的非确定性交互场景。

## 方法谱系与知识库定位

### 基础RL算法：GRPO与DAPO

MERCI并非独立的强化学习算法，而是作为探索增强模块嵌入到已有的策略优化框架中。论文选用了两个代表性基础算法：

- **GRPO**（Group Relative Policy Optimization, Shao et al., 2024）：通过组内归一化结果奖励计算优势函数，其核心优势估计公式为 $\hat{A}_t^i = \frac{r_i - \text{mean}(\{R_i\}_{i=1}^G)}{\text{std}(\{R_i\}_{i=1}^G)}$。GRPO依赖稀疏的、基于结果的奖励信号，缺乏对中间推理步骤的探索引导。

- **DAPO**（Yu et al., 2025）：在GRPO基础上引入了额外的优化技巧，作为更先进的RL基线。

MERCI的核心改动在于**优势估计**和**探索信号**两个关键槽位：在原始优势 $\hat{A}_{\text{old}}$ 基础上，增加由Coin Flipping Network（CFN）估计的、经过预算控制和标准化的内在探索奖励 $\hat{A}_{\text{exploration}}$，通过剪切机制合并为增强优势 $\hat{A}_{\text{new}}$（公式8）。

### 与现有探索方法的对比

论文将MERCI与两类探索基线进行了系统比较：

- **Entropy Adv.**（Cheng et al., 2025）：基于熵的优势塑造方法，通过鼓励策略输出的高熵来促进探索。这是一种无方向的探索策略——它鼓励多样性，但不区分哪些探索方向更有价值。实验表明，Entropy Adv.在数学推理平均pass@k上（GRPO基础）仅为63.8，显著低于MERCI的67.4（Table 9），验证了基于认知不确定性的有向探索优于无向熵最大化。

- **iMentor**（Gao et al., 2025）：基于Random Network Distillation（RND）的内在奖励方法，通过蒸馏误差衡量状态新颖性。iMentor在数学推理平均pass@k上（GRPO基础）为66.3，虽优于纯GRPO的65.8，但仍低于MERCI的67.4（Table 9）。这一差距源于RND缺乏对LLM推理MDP结构的利用——MERCI通过确定性转移假设简化了不确定性贝尔曼方程（UBE），将Q值不确定性传播转化为局部奖励不确定性的累积，提供了更准确的新颖性估计。

### 理论根基：CFN伪计数与简化UBE

MERCI的理论基础可追溯到两个源头：

1. **CFN伪计数估计**（Lobel et al., 2023）：通过训练轻量级网络预测随机硬币翻转向量的均值，利用输出平方范数 $\frac{1}{d}\|f_\phi(s)\|^2$ 隐式编码状态访问次数的倒数 $\frac{1}{\mathcal{N}(s)}$。相比于传统的密度模型（如PixelCNN），CFN计算开销极低，适合嵌入LLM训练循环。

2. **不确定性贝尔曼方程（UBE）**：在通用MDP中，Q值认知不确定性的传播需要同时考虑转移不确定性和奖励不确定性。MERCI的关键洞察在于：自回归推理任务的**状态转移函数是确定性且已知的**（$s' = (s, a)$，即下一个状态就是当前token序列拼接所选动作），这消除了转移不确定性，使UBE简化为：
   $$U^h(s,a) \leq \mathbb{V}_t[\hat{r}^h(s)] + \sum_{s',a'} \pi_{s',a'}^h P_{s'sa}^h U^{h+1}(s',a')$$
   其中仅需估计局部奖励不确定性 $\mathbb{V}_t[\hat{r}^h(s)]$，而这恰好可由CFN的伪计数代理。这一简化使得在LLM规模上的认知不确定性估计从不可行变为可行。

### 适用边界与局限

**适用条件**：
- 任务必须是**自包含的、确定性转移的推理场景**，如数学解题、SQL生成。在这些任务中，下一个状态完全由当前token序列和下一个token决定，不存在外部工具调用、网络搜索等非确定性交互。
- 骨干模型需要具备一定的推理能力基础（如Qwen2.5-Math-7B），CFN从SFT检查点初始化以获取基本的语义理解。

**已知局限**：
1. **CFN预训练开销**：CFN需要事先在骨干模型生成的响应上进行预训练，增加了训练流程的复杂性和时间成本。论文未报告CFN预训练的具体时间开销。
2. **超参数敏感性**：内在奖励的预算控制涉及多个超参数（百分位过滤比例、余弦衰减步数、剪切因子α），需要针对不同任务进行调整。消融实验（Table 9, 10）显示，移除噪声过滤导致pass@k从67.4降至63.8，余弦衰减速度的选择也显著影响性能，表明方法缺乏自适应机制。
3. **确定性转移假设的局限**：直接推广到具有随机外部工具或对话的开放域环境可能面临挑战。CFN在跨域SQL任务上的泛化（Figure 8-11）虽然展示了初步的语义迁移能力，但论文未在更开放的任务上验证。

### 开放问题

1. **非确定性交互扩展**：如何将MERCI的确定性转移假设扩展到使用工具调用、网络搜索等非确定性交互的LLM任务？这可能需要对UBE进行修正，重新引入转移不确定性项。

2. **多模态泛化**：CFN的伪计数估计是否能在更广义的多模态推理场景（如视觉推理）中提供有意义的不确定性？这需要验证CFN对视觉token序列的语义建模能力。

3. **细粒度信用分配**：当前内在奖励的信用分配基于相邻token簇的空间连贯性过滤，是否可以进一步细化到语法结构级别（如数学表达式的子式、代码的语句块）？

4. **大规模模型验证**：论文仅在7B-8B规模模型上进行了实验。在更大规模模型（如>70B）上，CFN的伪计数估计是否仍然可靠？内在奖励信号是否会因模型自身强大的推理能力而变得冗余？这些都需要进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Count_Counts_Motivating_Exploration_in_LLM_Reasoning_with_Count_based_Intrinsic_Rewards.pdf]]
