---
title: "CDE: Curiosity-Driven Exploration for Efficient Reinforcement Learning in Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CDE_Curiosity_Driven_Exploration_for_Efficient_Reinforcement_Learning_in_Large_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 5rXN5knHKW
aliases:
- CCDE
- CDE
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入模型自身的好奇心信号——actor对生成答案的困惑度（perplexity）和critic对状态价值估计的不确定性（多值头方差）——作为探索奖励，动态调节优化信号，从而引导策略主动探索低置信度区域并抑制过度自信的错误。"
primary_logic: "PPL奖励本质上对过度自信的错误施加惩罚，并鼓励模型探索新颖的正确推理模式；多头critic的方差在数据覆盖稀少的区域会升高，相当于一个隐式的计数式探索奖励，帮助策略更均衡地覆盖状态-动作空间。两者结合无需额外复杂模块即可显著缓解RLVR的熵坍缩和校准退化问题。"
claims:
- "加入PPL奖励后，GRPO在多个数学基准上平均提升约2个点，AIME24 Pass@16提升约8个点。"
- "多头PPO（K≥4）始终优于标准PPO，平均提升约2个点，AIME Pass@16最高可提升10个点以上。"
- "阶梯式（Staircase）奖励权重衰减策略最有效，表明早期强探索对最终性能至关重要。"
- "PPL奖励显著缓解了校准坍缩，使模型对正确与错误答案的置信度在训练中保持分离。"
---

# CDE: Curiosity-Driven Exploration for Efficient Reinforcement Learning in Large Language Models

> [!tip] 核心洞察
> PPL奖励本质上对过度自信的错误施加惩罚，并鼓励模型探索新颖的正确推理模式；多头critic的方差在数据覆盖稀少的区域会升高，相当于一个隐式的计数式探索奖励，帮助策略更均衡地覆盖状态-动作空间。两者结合无需额外复杂模块即可显著缓解RLVR的熵坍缩和校准退化问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CDE：基于好奇心驱动的探索用于大语言模型的高效强化学习 |
| 英文题名 | CDE: Curiosity-Driven Exploration for Efficient Reinforcement Learning in Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5rXN5knHKW) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | CDE (Curiosity-Driven Exploration) |
| Dataset | AIME24, AIME25, Overall Avg (MATH, AMC23, AIME25), Overall Avg |

> [!tip] 效果简介
> - AIME24 上，Pass@16 为 GRPO + PPL bonus (Qwen3-4B-Base)，对比 GRPO (Qwen3-4B-Base)，变化 +6.6。
> - AIME25 上，Pass@16 为 GRPO + PPL bonus (Qwen3-4B-Base)，对比 GRPO (Qwen3-4B-Base)，变化 +3.3。
> - Overall Avg (MATH, AMC23, AIME24, AIME25) 上，Avg 为 GRPO + PPL bonus (Qwen3-4B-Base)，对比 GRPO (Qwen3-4B-Base)，变化 +2.4。

## 概要

当前基于可验证奖励的强化学习（RLVR）在训练大语言模型进行数学推理时，普遍存在**探索与利用的严重失衡**：策略过早收敛到少数高奖励路径，导致策略熵坍缩和校准崩塌——模型对错误回答依然保持高度自信，同时丧失了发现多样化正确解题路径的能力。

针对这一瓶颈，**CDE (Curiosity-Driven Exploration)** 提出了一种系统性的探索框架，其核心思路是**利用模型自身的好奇心信号来引导探索**，而非依赖外部计数或任务无关的熵奖励。具体而言：

- **Actor端**：以模型对生成响应的困惑度（PPL）作为好奇心度量，本质上对过度自信的错误施加惩罚，同时鼓励模型探索新颖的正确推理模式。
- **Critic端**：通过多头自举（bootstrap）结构近似值函数后验分布，以多头间的标准差作为隐式的计数式探索奖励——在数据覆盖稀少的区域，头间分歧自然升高，引导策略向欠探索区域移动。

两者均通过自适应裁剪机制整合到原始奖励或优势函数中，无需额外复杂模块即可显著缓解RLVR的熵坍缩和校准退化问题。

**主要实验结果**（基于Qwen3-4B-Base，DAPO-17K训练集，数学推理基准）：
- 在GRPO上加入PPL奖励，四个基准（MATH、AMC23、AIME24、AIME25）平均提升约**2.4个点**，AIME24 Pass@16提升**6.6个点**。
- 多头PPO（K≥4）始终优于标准PPO，平均提升约**2.0个点**，16头配置在AIME24 Pass@16上可提升**5.9个点**。
- 阶梯式（Staircase）奖励权重衰减策略最优，表明**早期强探索**对最终性能至关重要。
- PPL奖励显著缓解了校准崩塌：训练过程中正确与错误回答的PPL保持分离，模型置信度校准得到改善。

**方法定位**：CDE处于RLVR探索策略的改进线上，区别于传统的熵奖励（Schulman et al., 2017）和基于哈希的计数式探索（后者在LLM上因嵌入表达性不足而失效），也与i-MENTOR（Gao et al., 2025）等外部好奇心驱动方法形成互补。其探索信号完全来自模型内部状态，兼具理论解释性（自举方差近似后验不确定性）和实践轻量性（多头critic的额外内存与计算开销可忽略）。

### 大语言模型的强化学习微调

近年来，强化学习已成为提升大语言模型（LLM）推理能力的核心技术路径。通过将数学问题求解等任务建模为马尔可夫决策过程，基于可验证奖励的强化学习（RLVR）方法——如近端策略优化（PPO，Schulman et al., 2017）和分组相对策略优化（GRPO，Guo et al., 2024）——能够利用答案正确性作为稀疏奖励信号，驱动模型自主发现有效的推理策略。

然而，RLVR的成功高度依赖于策略在训练过程中的探索能力。数学推理任务天然具有多解性：同一问题往往存在多种正确的推理路径。如果策略过早收敛到少数高奖励的解题模式，不仅会丧失发现更优解的机会，还可能导致模型对错误的推理路径产生虚假的自信。

### 探索-利用失衡：RLVR的核心瓶颈

当前RLVR方法面临一个根本性的困境：探索与利用之间的严重失衡。这种失衡表现为三个相互关联的退化现象：

**早熟收敛与策略熵坍缩。** 标准GRPO和PPO在训练过程中，策略的熵值持续下降，模型生成的响应迅速坍缩到少数高奖励模式。这并非因为模型已经找到了最优解，而是因为RLVR的优化信号天然偏向利用——一旦某条推理路径获得正奖励，策略就会被强化去重复相似路径，而缺乏动力去探索可能更优但尚未被发现的新路径。

**校准崩塌。** 更隐蔽但同样致命的问题是模型置信度校准的退化。在标准GRPO训练中，随着训练推进，模型对正确回答和错误回答的平均困惑度（PPL）差异逐渐消失——模型对错误答案的自信程度与正确答案几乎无异（Figure 8a）。这意味着模型不仅会犯错，还会以高度自信的方式犯错，丧失了自我评估不确定性的能力。这种校准崩塌与LLM幻觉现象存在深层关联（Kalai et al., 2025），构成了RLVR训练中一个被长期忽视的隐患。

**传统探索机制的失效。** 现有的探索增强手段在LLM推理场景中面临根本性困难。基于熵的奖励（Entropy Bonus，Schulman et al., 2017）是样本无关的——它仅鼓励策略输出分布更均匀，却无法区分“有益的多样性探索”和“高置信度的错误”（Figure 4）。换言之，当模型自信满满地输出一个错误答案时，熵奖励并不会施加任何惩罚。另一方面，基于计数的探索方法（如SimHash哈希计数）在LLM上效果不佳：由于推理路径的嵌入表达能力不足，大部分响应坍缩到相同或相邻的哈希网格中（Figure 1），导致计数分布高度集中，无法有效区分已探索和未探索的状态空间。

### 好奇心驱动探索的核心动机

上述困境指向一个清晰的改进方向：**探索信号应当来自模型自身，而非外部计数或样本无关的统计量。** 本文提出的好奇心驱动探索（Curiosity-Driven Exploration, CDE）正是基于这一洞察。

CDE的核心思想是：利用模型自身对生成内容的“意外程度”作为探索的内在驱动力。具体而言，Actor端使用生成响应的困惑度（PPL）作为好奇心信号——模型对某个回答越“意外”，说明该推理路径越偏离其当前认知，值得进一步探索。Critic端则通过多头值函数的预测方差来估计状态价值的不确定性——在数据覆盖稀少的区域，不同值头之间的分歧自然增大，这相当于一个隐式的计数式探索奖励，引导策略均衡地覆盖状态-动作空间。

这种设计具有两个关键优势。第一，PPL奖励天然地对过度自信的错误施加惩罚：当模型以高置信度生成错误答案时，PPL奖励为负，从而抑制这种有害行为；而正确但新颖的推理路径则获得正向探索奖励（Figure 3）。第二，好奇心信号伴随着自然的退火机制：随着训练推进和模型对常见推理路径的熟悉，PPL和Critic方差自然下降，探索强度自动衰减，无需手动设计复杂的奖励衰减策略。

## 核心方法与创新机理

CDE的核心创新在于将RLVR中原本缺失的**探索信号**重新注入优化过程，且该信号完全源自模型自身——无需外部奖励模型或复杂的环境交互。具体而言，CDE在两个关键维度上改变了标准RLVR的优化机制：

### 1. 探索信号：从“无”到“双通道好奇心”

标准GRPO（Guo et al., 2024）和PPO（Schulman et al., 2017）在RLVR场景下仅依赖验证奖励进行优化，缺乏显式的探索驱动。传统的熵奖励（Entropy Bonus）虽然引入了探索概念，但它是**样本无关**的——仅基于策略在给定上下文下的整个词汇表分布计算，无法区分模型是自信地犯错还是犹豫地猜对（见图4）。基于SimHash的计数式探索则因推理路径嵌入的表达性不足而失效，大部分响应坍缩到少数哈希网格中（见图1）。

CDE将探索信号替换为两个**样本相关**的好奇心通道：

- **Actor端：PPL奖励（困惑度奖励）**。Actor对自身生成响应的负平均对数似然作为好奇心度量：
  
  $$B_{\mathrm{actor}}(q, o) = -\frac{1}{T}\sum_{t=1}^{T}\log\pi(o_t|o_{<t}, q)$$
  
  这一信号天然惩罚模型自信生成的错误答案（高置信度但低概率的token序列），同时奖励模型探索新颖的正确推理路径（见图3）。其核心机制在于：PPL奖励本质上是对过度自信错误的抑制和对未知正确模式的鼓励。

- **Critic端：多头方差奖励**。将标准单头值函数网络替换为共享LLM骨干的$K$个自举值头，以头间标准差作为探索奖励：
  
  $$B_{\mathrm{critic}}(q, o_{i,\leqslant t+1}) = \mathrm{std}\left(\{\widehat{V}_j(q, o_{i,\leqslant t+1}) \mid 1 \leqslant j \leqslant K\}\right)$$
  
  在数据覆盖稀少的区域，不同值头因自举子样本差异而产生高方差，相当于一个**隐式的计数式探索奖励**。实验证实，训练集（DAPO-17K）上的值头争议最小，而未见数据（AMC23、GPQA）上的争议显著更高（见图9），验证了这一解释。

两种信号均通过**自适应裁剪机制**整合到原始奖励或优势函数中，防止探索奖励主导学习信号：

$$\widehat{r}(q, o) = r(q, o) + \min\left(\frac{|r(q, o)|}{\kappa}, \alpha B_{\mathrm{actor}}(q, o)\right)$$

### 2. Critic架构：从“单头”到“自举多头”

标准PPO使用单个值函数网络估计状态价值，无法捕捉价值估计的不确定性。CDE将Critic扩展为**共享LLM骨干的$K$个值头**，每个值头在独立的自举子样本上通过最小化MSE损失进行训练：

$$\mathcal{L}_\phi = \frac{1}{\zeta K |\mathcal{D}|} \sum_{j=1}^K \sum_{(q,o,r) \in \mathcal{D}_j} \left(\widehat{V}_j(q,o) - r\right)^2$$

这一设计的精妙之处在于：**无需额外的探索模块或环境模型**，仅通过值头间的分歧即可获得对状态-动作空间覆盖度的隐式估计。优势估计也随之调整为使用多头平均值来计算时间差分误差和GAE，并加上裁剪后的critic探索奖励。

### 与基线方法的本质区别

| 维度 | GRPO/PPO | 熵奖励 | CDE |
|------|----------|--------|-----|
| 探索信号来源 | 无 | 策略分布熵（样本无关） | Actor困惑度 + Critic方差（样本相关） |
| 对自信错误的惩罚 | 无 | 无（见图4） | 有（PPL奖励天然惩罚） |
| 对新颖正确路径的鼓励 | 无 | 间接 | 有（PPL奖励天然奖励） |
| 状态空间覆盖估计 | 无 | 无 | 有（多头方差作为隐式计数） |
| 额外模块开销 | 无 | 无 | 极小（多头共享骨干，见表7、8） |

CDE的轻量性是其关键优势：相比i-MENTOR（Gao et al., 2025）等需要额外好奇心模块的方法，CDE仅需对现有训练架构进行微小修改，却能在数学推理基准上带来约2个点的平均提升，AIME24 Pass@16提升可达8个点以上（见表1）。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the multi-head critic framework*

CDE（Curiosity-Driven Exploration）是一个轻量级的探索增强框架，旨在解决现有RLVR方法中探索与利用严重失衡的问题。其核心思路是：将模型自身的好奇心信号——actor的困惑度（perplexity）和critic的价值估计不确定性——作为探索奖励，动态注入到强化学习的优化信号中，引导策略主动探索低置信度区域并抑制过度自信的错误。

### 框架总览

CDE的整体pipeline由两个并行的探索模块和一个自适应裁剪机制构成，分别作用于actor端和critic端：

1. **Actor Exploration Module**：在生成响应后，计算actor对该响应的负平均对数似然（即PPL奖励），并将其与原始验证奖励结合，形成总奖励信号。该模块通过自适应裁剪防止PPL奖励主导学习信号。
2. **Multi-Head Critic**：将标准单头值函数网络扩展为共享LLM骨干的K个自举值头。每个值头在独立的自举子样本上训练，头间标准差作为critic好奇心奖励，反映状态-动作对的不确定性。
3. **Adaptive Clipping Mechanism**：使用超参数κ和α控制探索奖励的相对幅度，防止奖励黑客和过度探索。

在GRPO变体中，CDE仅需在奖励计算阶段加入PPL奖励即可；在PPO变体中，CDE进一步用多头值函数的平均值估计时间差分误差和优势，并将critic奖励裁剪后加入优势估计。

### 输入输出流

**输入**：问题 $q$ 从训练数据集 $\mathcal{D}$ 中采样，actor策略 $\pi_\theta$ 生成响应序列 $o = (o_1, o_2, \dots, o_T)$。

**Actor端处理流程**：
1. 计算原始验证奖励 $r(q, o)$（如数学推理中的答案正确性奖励）。
2. 计算actor好奇心奖励 $B_{\mathrm{actor}}(q, o) = -\frac{1}{T}\sum_{t=1}^{T}\log\pi(o_t|o_{<t}, q)$（式1），衡量模型对自身生成响应的“意外”程度。
3. 通过自适应裁剪组合总奖励：
   $$\widehat{r}(q, o) = r(q, o) + \min\left(\frac{|r(q, o)|}{\kappa}, \alpha B_{\mathrm{actor}}(q, o)\right)$$
   其中 $\kappa$ 控制奖励缩放，$\alpha$ 控制探索奖励幅度（式2）。
4. 将 $\widehat{r}(q, o)$ 作为GRPO的响应级奖励，或作为PPO中令牌级奖励的基础。

**Critic端处理流程**（仅PPO变体）：
1. K个值头共享LLM骨干，每个值头 $j$ 在自举子集 $\mathcal{D}_j$ 上通过最小化MSE损失训练：
   $$\mathcal{L}_\phi = \frac{1}{\zeta K |\mathcal{D}|} \sum_{j=1}^K \sum_{(q,o,r) \in \mathcal{D}_j} \left( \widehat{V}_j(q,o) - r \right)^2$$
   其中 $\zeta$ 为子采样分数。
2. 计算critic好奇心奖励：
   $$B_{\mathrm{critic}}(q, o_{i,\leqslant t+1}) = \mathrm{std} \left( \{ \widehat{V}_j(q, o_{i,\leqslant t+1}) \mid 1 \leqslant j \leqslant K \} \right)$$
   即K个值头对当前状态价值估计的标准差。
3. 用多头均值估计时间差分误差和优势，并将裁剪后的critic奖励加入优势估计：
   $$\widehat{A}_{i,t} = \underbrace{\sum_{l=t}^{|o_i|} (\gamma\lambda)^{l-t} \widehat{\delta}_{i,l}}_{\approx \tilde{A}_{i,t}} + \omega \min\left(\frac{|\tilde{A}_{i,t}|}{\kappa}, \alpha B_{\mathrm{critic}}(q, o_{i,\leq t+1})\right)$$
   其中 $\omega$ 为动态权重，通常采用阶梯式衰减策略。

**输出**：修正后的奖励信号（GRPO）或优势估计（PPO），直接送入策略梯度更新，驱动actor策略向低置信度、高不确定性的区域探索。

### 模块间关系

两个探索模块在机制上互补：PPL奖励在令牌级别惩罚过度自信的错误并鼓励新颖的正确推理模式（见Figure 3），而多头critic的方差在数据覆盖稀少的区域升高，起到隐式计数式探索的作用（见Figure 5和Figure 9）。两者均通过自适应裁剪与原始优化信号耦合，无需额外复杂模块即可缓解RLVR的熵坍缩和校准退化问题。实验表明，框架对超参数 $\kappa, \alpha, \zeta$ 具有一定鲁棒性（见Table 3-5），且额外计算和内存开销极小（见Table 7-8）。

CDE 框架由两个互补的探索模块构成：**Actor 端的好奇心奖励**（基于模型对自身生成响应的困惑度）和 **Critic 端的多头方差奖励**（基于值函数后验分布的不确定性）。两者通过自适应裁剪机制整合到强化学习的优化信号中。

### Actor 好奇心模块

Actor 的好奇心被建模为策略对自身生成动作的“意外”程度——即当前策略下该响应的低概率程度。直觉上，令模型感到意外的响应通常位于探索不足的区域，因此值得被鼓励。具体而言，对于问题 $q$ 和生成的响应 $o$，Actor 好奇心奖励定义为该响应的负平均对数似然：

$$B_{\mathrm{actor}}(q, o) = -\frac{1}{T}\sum_{t=1}^{T}\log\pi(o_t|o_{<t}, q)$$

其中 $T$ 为响应长度，$\pi(o_t|o_{<t}, q)$ 为当前策略在给定上文条件下生成第 $t$ 个令牌的概率。该奖励本质上是对模型“自信程度”的惩罚：当模型以高概率生成某个令牌时，$B_{\mathrm{actor}}$ 较小；反之，低概率的令牌会获得较高的探索奖励。

这一设计与传统的熵奖励有本质区别。传统熵奖励基于整个下一令牌概率分布的熵 $\mathcal{H}_t = -\sum_{v\in\mathcal{V}}\pi_{\theta}(v\mid q, o_{<t})\log\pi_{\theta}(v\mid q, o_{<t})$，是**样本无关**的——即使模型做出了高置信度的错误选择（如采样了某个错误令牌），熵奖励也无法对其施加惩罚。而 PPL 奖励通过将样本特定的对数似然纳入信号，能够内在地惩罚“自信的错误”并鼓励“新颖的正确回答”。

### 自适应裁剪与总奖励

直接将 $B_{\mathrm{actor}}$ 加到原始验证奖励上可能导致奖励黑客或过度探索——模型可能为了最大化好奇心奖励而生成无意义的低概率序列。为解决这一问题，CDE 引入了自适应裁剪机制，将总响应级奖励定义为：

$$\widehat{r}(q, o) = r(q, o) + \min\left(\frac{|r(q, o)|}{\kappa}, \alpha B_{\mathrm{actor}}(q, o)\right)$$

其中 $r(q, o)$ 为原始验证奖励（如数学答案的正确性评分），$\kappa$ 和 $\alpha$ 为超参数。裁剪项 $\frac{|r(q, o)|}{\kappa}$ 确保好奇心奖励的幅度不会超过原始奖励的固定比例，防止探索信号主导学习过程。$\alpha$ 控制好奇心奖励的整体缩放。

### 多头 Critic 与方差奖励

在 Critic 端，CDE 通过多头自举结构近似值函数的后验分布，并将头间标准差作为隐式的计数式探索奖励。具体而言，框架在共享 LLM 骨干网络上维护 $K$ 个值头 $\{\widehat{V}_j\}_{j=1}^{K}$，每个值头在独立的自举子样本 $\mathcal{D}_j$ 上训练，损失函数为：

$$\mathcal{L}_\phi = \frac{1}{\zeta K |\mathcal{D}|} \sum_{j=1}^K \sum_{(q,o,r) \in \mathcal{D}_j} \left( \widehat{V}_j(q,o) - r \right)^2$$

其中 $\zeta$ 为子采样比例。Critic 好奇心奖励定义为 $K$ 个值头在给定状态-动作对上的标准差：

$$B_{\mathrm{critic}}(q, o_{i,\leqslant t+1}) = \mathrm{std}\left( \{\widehat{V}_j(q, o_{i,\leqslant t+1}) \mid 1 \leqslant j \leqslant K\} \right)$$

其直觉是：在数据覆盖充分的区域，各值头的估计趋于一致，方差较低；而在探索不足的区域，值头间的分歧增大，方差升高，从而为策略提供指向未充分探索区域的探索信号。

### PPO 中的多头优势估计

在 PPO 框架下，CDE 将多头 Critic 的均值和方差奖励同时整合到优势估计中。首先，使用 $K$ 个值头的均值计算时间差分误差：

$$\widehat{\delta}_{i,l} = r_{i,l} + \frac{\gamma}{K}\sum_{j=1}^{K}\widehat{V}_j(q, o_{i,\leqslant l+1}) - \frac{1}{K}\sum_{j=1}^{K}\widehat{V}_j(q, o_{i,\leqslant l})$$

然后通过 GAE 累积得到基础优势估计 $\tilde{A}_{i,t} = \sum_{l=t}^{|o_i|} (\gamma\lambda)^{l-t} \widehat{\delta}_{i,l}$，最终优势为：

$$\widehat{A}_{i,t} = \underbrace{\sum_{l=t}^{|o_i|} (\gamma\lambda)^{l-t} \widehat{\delta}_{i,l}}_{\approx \tilde{A}_{i,t}} + \omega \min\left( \frac{|\tilde{A}_{i,t}|}{\kappa}, \alpha B_{\mathrm{critic}}(q, o_{i,\leq t+1}) \right)$$

其中 $\omega$ 为 Critic 奖励的动态权重（可通过阶梯式衰减等策略调节），裁剪机制与 Actor 端一致，防止 Critic 探索奖励过度干扰优势估计。

## 实验与关键发现

### 核心瓶颈：RLVR中的探索-利用失衡

当前基于验证奖励的强化学习（RLVR）方法，如 GRPO（Guo et al., 2024）和 PPO（Schulman et al., 2017），在数学推理训练中存在严重的探索与利用失衡。这种失衡表现为三个相互关联的退化现象：

1. **早熟收敛**：策略过早锁定于少数高奖励的解题路径，丧失了对更优解空间的覆盖能力。
2. **策略熵坍缩**：模型生成响应的多样性急剧下降，输出分布坍缩到极少数模式上。
3. **校准崩塌**：模型对错误回答保持高度自信，正确与错误响应的生成概率差异在训练后期趋于消失，即模型无法“意识到”自己犯了错。

这些现象的根本原因在于：标准 RLVR 的奖励信号仅来自结果验证（答案正确与否），缺乏对探索行为的内在激励。传统的熵奖励（entropy bonus）虽然鼓励多样性，但它是样本无关的——即使模型做出了高置信度的错误预测，熵奖励也无法施加惩罚（见 Figure 4）。基于 SimHash 的计数式探索同样失败，原因在于推理路径的嵌入表达性不足，导致大多数响应坍缩到相同的哈希网格中（见 Figure 1），计数信号失去区分度。

### 方法核心：双重好奇心驱动的探索信号

CDE 的核心洞察是：**利用模型自身对生成内容的不确定性作为探索的内在驱动力**。具体而言，CDE 从 Actor 和 Critic 两个维度引入好奇心信号：

- **Actor 好奇心（PPL 奖励）**：定义为生成响应的负平均对数似然，即困惑度（perplexity）。其因果机制是双重的——对高置信度的错误回答施加惩罚（高概率但错误 → 低 PPL → 负奖励），同时鼓励模型探索新颖的正确推理模式（低概率但正确 → 高 PPL → 正奖励）。如 Figure 3 所示，PPL 奖励天然地区分了“自信的错误”与“新颖的正确”，从而引导策略远离校准崩塌。

- **Critic 好奇心（多头方差奖励）**：通过自举重采样训练 $K$ 个共享 LLM 骨干的值头，计算头间标准差作为状态价值的不确定性估计。其机制等价于隐式的计数式探索——在数据覆盖稀少的区域，不同值头因自举采样的差异而产生高方差，从而引导策略向这些欠探索区域分配更多概率质量。Figure 5 和 Figure 9 提供了实证支持：训练集（DAPO-17K）上的值头标准差最低，而未见数据（AMC23, GPQA）上的争议显著更高。

两种好奇心信号通过自适应裁剪机制整合到原始奖励中，防止奖励黑客和过度探索：

$$
\widehat{r}(q, o) = r(q, o) + \min \left( \frac{|r(q, o)|}{\kappa}, \alpha B_{\mathrm{actor}}(q, o) \right)
$$

其中 $\kappa$ 控制裁剪阈值，$\alpha$ 控制奖励幅度。对于 PPO 变体，Critic 好奇心奖励以类似方式注入优势估计。

### 主实验结果

**Table 1** 报告了零样本精度主实验。核心发现如下：

- **PPL 奖励一致提升 GRPO 性能**：在 Qwen3-4B-Base 模型上，GRPO + PPL bonus 相比标准 GRPO 在四个基准（MATH, AMC23, AIME24, AIME25）上的整体平均提升约 **+2.4 点**。在更具挑战性的 Pass@16 指标上，AIME24 提升约 **+8 点**，AIME25 提升约 **+3.3 点**。

- **多头 PPO 一致优于标准 PPO**：当 $K \geq 4$ 时，多头 PPO 的整体平均提升约 **+2.0 点**。在 AIME24 Pass@16 上，16 头 PPO 相比标准 PPO 提升约 **+5.9 点**，最高可达 **+10 点以上**。值得注意的是，多头 PPO（$K \geq 4$）的表现超过了 PPO + PPL bonus，表明 Critic 的不确定性反映了更高层次的长期价值不确定性。

- **CDE 的训练动态呈现“先抑后扬”**：Figure 6 展示了 AIME25 上 Avg@16 精度随训练步数的变化。CDE 方法在训练初期落后于标准 GRPO/PPO 基线，但最终达到更高的准确度并持续上升。这验证了 CDE 通过牺牲短期利用效率换取更优长期探索策略的机制。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of Avg@16 accuracy on AIME25 over training of vanilla GRPO and PPO (Baseline methods) and GRPO with PPL bonus and 16 head multi-head PPO (Our methods)*

### 关键消融与分析

**奖励权重衰减策略至关重要**。Table 2 对比了四种 PPL 奖励权重衰减计划：无衰减、线性衰减、余弦衰减和阶梯式（Staircase）衰减。阶梯式衰减取得最高平均精度（50.6 vs 48.2-49.7），表明两个关键原则：① 早期强探索对最终性能至关重要；② 训练后期移除探索奖励、让策略回归纯利用是必要的。Figure 11 进一步显示，阶梯式衰减在缓解熵坍缩方面比无衰减更稳定。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/010_Table_2.jpg]]
*Table 2: Zero-shot accuracy of GRPO models under different PPL bonus weight decay schedules. The schedules follow those illustrated in Figure 7*

**PPL 奖励缓解校准崩塌**。Figure 8 展示了训练过程中正确与错误响应的平均 PPL 变化。在标准 GRPO 下（Figure 8a），正确与错误响应的 PPL 差异在训练后期消失，模型对错误回答保持与正确回答相当的置信度——即校准崩塌。加入 PPL 奖励后（Figure 8b），两条曲线始终保持分离，模型对错误回答的置信度显著低于正确回答，有效恢复了校准能力。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/012_Figure_8.jpg]]
*Figure 8: Average response PPL per training step, stratified by correctness*

**多头 Critic 的头数效应**。Table 1 显示，$K=2$ 时增益可忽略，$K \geq 4$ 后达到明显提升并趋于平稳。Table 7 和 Table 8 表明，多头架构的内存和计算开销极小——从 1 头到 16 头，参数量增加约 0.001%，每次迭代的反向传播时间仅增加约 4ms。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/018_Table_7.jpg]]
*Table 7: Memory Usage for Different Critic Heads*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_5rXN5knHKW/figures/019_Table_8.jpg]]
*Table 8: Average Computation Time per Iteration (ms)*

**子采样分数 $\zeta$ 具有鲁棒性**。Table 3 的消融显示，$\zeta = 0.5$ 与 $\zeta = 1.0$ 在 16 头和 4 头配置下的性能差异极小，表明模型对自举采样的具体比例不敏感。

### 失败模式与局限

**计数式探索在 LLM 推理中失效**。Table 9 显示，基于 SimHash 的计数式探索奖励未能显著提升 GRPO 性能。如 Figure 1 所示，推理路径的嵌入坍缩到少数哈希网格中，计数信号失去区分度。这揭示了 LLM 推理轨迹的有效嵌入表示仍是开放问题。

**超参数敏感性**。Table 4 和 Table 5 的敏感性分析显示，$\kappa$ 和 $\alpha$ 的选择对性能有显著影响。极端设置（如 $\kappa=1, \alpha=1$）会导致性能崩溃（平均精度从 50.6 降至 8.67），表明探索奖励的幅度需要仔细调控。虽然推荐设置（GRPO: $\kappa=3, \alpha=1$；PPO: $\kappa=3, \alpha=0.5$）表现稳健，但最优值可能因任务和模型而异。



**领域泛化未验证**。所有实验仅限于数学推理领域（MATH, AMC23, AIME24, AIME25），CDE 在代码生成、多模态推理等领域的有效性有待验证。此外，实验主要使用 3B-4B 规模模型，在更大模型（如 70B+）上的扩展性尚不明确。

## 定位与知识库关联

### 核心瓶颈与因果机制

当前基于可验证奖励的强化学习（RLVR）方法——无论是无critic的 **GRPO**（Guo et al., 2024）还是actor-critic架构的 **PPO**（Schulman et al., 2017）——在数学推理训练中普遍面临探索-利用失衡。其根本瓶颈在于：标准RLVR仅依赖外部验证奖励（如答案正确性）优化策略，导致策略迅速坍缩至高置信度的少数解题路径，表现为策略熵持续下降、模型对错误答案仍保持高度自信（校准坍缩），以及无法有效探索多样化的正确推理模式。

CDE的核心因果干预在于引入**模型自身的好奇心信号**作为探索奖励，从两个维度动态调节优化信号：

1. **Actor端**：以生成响应的困惑度（PPL）作为好奇心度量。PPL奖励本质上对“自信的错误”（高置信度但答案错误）施加惩罚，同时鼓励模型探索新颖的正确推理路径。这直接缓解了校准坍缩——实验显示，标准GRPO训练后期正确与错误回答的PPL分布完全重叠，而加入PPL奖励后两者始终保持分离（Figure 8）。
2. **Critic端**：通过多头值函数的标准差度量状态价值估计的不确定性。该方差在数据覆盖稀少的区域自然升高，起到隐式计数式探索奖励的作用，引导策略更均衡地覆盖状态-动作空间，而无需显式维护访问计数表。

### 与基线方法的差异化对比

| 方法 | 探索信号来源 | 信号粒度 | 关键局限 |
|------|-------------|---------|---------|
| **GRPO / PPO**（原版） | 无探索奖励 | — | 早熟收敛、熵坍缩、校准崩塌 |
| **Entropy Bonus**（Schulman et al., 2017） | 策略熵 | 样本无关 | 无法区分正确与错误的高置信度输出（Figure 4），对自信错误无惩罚 |
| **i-MENTOR**（Gao et al., 2025） | 好奇心驱动探索 | 样本相关 | 具体实现细节与CDE的差异需查阅原文对比 |
| **CDE（本文）** | Actor PPL + Critic多头方差 | 样本相关 | 引入额外超参数（κ, α, ω, ζ），最优设置可能因任务而异 |

**关键改进槽位**：

- **探索信号**：从无奖励或样本无关的熵奖励，转变为样本相关的PPL奖励（actor端）和多头critic方差奖励（critic端），并伴随自适应裁剪机制（Eq 2）防止奖励黑客。
- **Critic架构**：从标准单头值函数网络，转变为共享LLM骨干的K个自举值头，以头间标准差作为隐式计数式探索奖励。

### 方法适用边界与局限

**已验证的适用范围**：
- 数学推理领域（MATH、AMC23、AIME24、AIME25），在3B-4B规模模型（Qwen3-4B-Base、Llama-3.2-3B-Instruct）上验证有效。
- 可与GRPO和PPO两种主流RLVR框架无缝集成，仅需对原始训练架构进行微小修改。

**已知局限**：
1. **领域泛化未验证**：实验仅限于数学推理，未在代码生成、多模态推理等任务上评估CDE的有效性。
2. **计数式探索的嵌入瓶颈**：基于SimHash的显式计数式探索在LLM上效果不佳（Table 9），表明推理轨迹的有效嵌入表示仍是开放问题，限制了该类方法的直接应用。
3. **超参数敏感性**：CDE引入κ、α、ω、ζ等额外超参数。敏感性分析（Table 4、Table 5）显示κ=3、α=1（GRPO）和κ=3、α=0.5（PPO）为较优设置，但最优配置可能因任务和模型而异。
4. **大规模模型的可扩展性**：多头critic虽开销极小（Table 7、Table 8显示内存和计算时间增加可忽略），但在极大K或极大规模模型（如70B+）上的边际成本和收益有待验证。

### 关键消融发现

- **奖励权重衰减策略至关重要**：阶梯式（Staircase）衰减在早期维持高探索强度、后期移除奖励，取得最高平均精度50.6，显著优于无衰减（48.2）和线性/余弦衰减（Table 2）。这表明早期强探索对最终性能起决定性作用。
- **多头critic的头数效应**：K=2时增益可忽略，K≥4后性能明显提升并趋于平稳（Table 1），且子采样分数ζ（0.5 vs 1.0）对最终性能影响不大（Table 3），模型对ζ具有鲁棒性。
- **探索奖励的自然退火**：随着训练推进，critic值估计逐渐收敛，多头方差自然减小，使探索奖励无需外部调度即可部分衰减（Figure 9、Figure 12）。

### 开放问题

1. **校准坍缩与幻觉的因果关系**：CDE揭示的校准效应能否系统性地用于减少LLM幻觉？校准坍缩与幻觉之间的深层因果机制是什么？
2. **更丰富的好奇心信号源**：除PPL和预测方差外，注意力模式、梯度信息等模型内在信号是否可作为有效的探索奖励？
3. **复杂任务的可扩展性**：在多步推理、对话或交互式任务中，CDE的探索机制是否能保持高效与稳定？
4. **推理轨迹的嵌入表示**：如何设计更优的嵌入表示，使得显式计数式或预测式探索在LLM上变得可行？
5. **与对齐方法的结合**：CDE的探索策略是否可以与离线RL、基于人类反馈的偏好对齐等方法结合，进一步提升对齐性和泛化能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/CDE_Curiosity_Driven_Exploration_for_Efficient_Reinforcement_Learning_in_Large_Language_Models.pdf]]
