---
title: "Empowering LLM Tool Invocation with Tool-call Reward Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Empowering_LLM_Tool_Invocation_with_Tool_call_Reward_Model.pdf
openreview_forum_id: LnBEASInVr
aliases:
- TCRMTTLCA
- ELTITCRM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入工具调用级别的细粒度效用评估（通过工具调用奖励模型TRM），并设计回合级信用分配与优势估计机制，将工具调用奖励与最终结果奖励有效结合，从而直接优化工具调用质量。"
primary_logic: "通过训练一个专门的TRM来评估每个工具调用的必要性与质量，并在PPO/GRPO的RL框架中以回合级方式分配工具调用奖励，既能稳定训练又能提升模型工具使用效果和泛化能力。"
claims:
- "TRM通过提供逐工具调用的细粒度效用信号解决结果奖励引发的梯度冲突。"
- "回合级信用分配结合TRM评分与结果奖励，在PPO/GRPO中实现有效优化。"
- "集成TRM在不同模型规模（1.5B/3B/7B）和RL算法（PPO/GRPO）下均一致提升搜索和代码场景的表现。"
- "GRPO中的回合级优势估计优于组级估计，避免了奖励黑客行为。"
---

# Empowering LLM Tool Invocation with Tool-call Reward Model

> [!tip] 核心洞察
> 通过训练一个专门的TRM来评估每个工具调用的必要性与质量，并在PPO/GRPO的RL框架中以回合级方式分配工具调用奖励，既能稳定训练又能提升模型工具使用效果和泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 赋能大语言模型工具调用的工具调用奖励模型 |
| 英文题名 | Empowering LLM Tool Invocation with Tool-call Reward Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LnBEASInVr); [GitHub](https://github.com/OpenDFM/TRM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Tool-call Reward Model (TRM) with Turn-level Credit Assignment |
| Dataset |  |

## 概述

大语言模型在调用外部工具时，现有强化学习方法普遍采用**仅基于最终答案正确性的结果奖励**。这一信号粒度过于粗糙：一个正确的工具调用可能因为最终答案错误而被惩罚，反之亦然，从而在优化过程中引发**梯度冲突**，限制了模型学习有效工具调用策略的能力。

针对上述瓶颈，本文提出**工具调用奖励模型（Tool-call Reward Model, TRM）**，核心思路是将奖励信号从轨迹级细化到回合级——对每一次工具调用的必要性与质量进行独立评分，并将这些评分作为中间奖励，与最终结果奖励共同构成优化目标。具体而言，TRM的训练数据通过从前沿大语言模型中蒸馏获得，其架构将语言模型头替换为二分类头，基于工具调用输出最后一个Token的隐状态预测效用分数。在强化学习阶段，本文设计了**回合级信用分配**机制，将TRM评分映射为PPO中对应Token的奖励权重，并在GRPO中引入**回合级优势估计**以替代传统的组级估计，从而缓解奖励黑客行为。

实验覆盖搜索问答和代码数学两类工具调用场景，在1.5B、3B、7B三种模型规模上，TRM集成后的PPO/GRPO均一致优于仅使用结果奖励的基线方法。例如，在Qwen2.5-3B-Instruct上，Search-R1-GRPO-TRM在多个问答基准上取得最优平均性能（43.49）；在代码数学任务上，ToRL-GRPO-TRM较ToRL-GRPO提升约4.6个百分点。消融分析表明，中等规模的TRM（1.5B/3B）配合1万条训练样本即可达到稳健性能，且回合级优势估计在工具调用数量和最终效果上均优于组级估计。

## 背景与动机

### 大语言模型的工具调用困境

大语言模型（LLM）在知识密集型任务中的能力边界日益清晰：单靠参数化知识难以覆盖长尾事实、实时信息与精确计算。工具调用（tool invocation）——让模型在推理过程中主动调用搜索引擎、代码解释器等外部工具——已成为突破这一瓶颈的关键范式。然而，如何训练模型学会“何时调用工具、调用哪个工具、如何利用工具返回的结果”，仍是一个开放难题。

### 结果奖励的梯度冲突

当前主流的强化学习（RL）训练方法，无论是 PPO 还是 GRPO，普遍采用**仅基于最终答案正确性的结果奖励**（outcome-only reward）。这种粗粒度的奖励信号存在一个根本性缺陷：它无法区分中间工具调用的质量与最终答案的质量。

考虑一个典型场景：模型在推理过程中做出了完全正确的工具调用，获得了高质量的检索结果，但最终答案却因推理失误而错误。在结果奖励机制下，整个轨迹——包括那个正确的工具调用——都会被惩罚。反之，一个错误的工具调用如果侥幸导向了正确答案，反而会获得正向奖励。这种**梯度冲突**（gradient conflict）使得模型难以学习到有效的工具调用策略，训练过程不稳定，收敛缓慢。

### 过程监督的缺失

上述问题的根源在于**过程监督的缺失**。与数学推理中的逐步验证类似，工具调用场景同样需要细粒度的中间评估信号。已有的过程奖励方法（如 AgentPRM、StepSearch）尝试对推理链的每一步进行评分，但它们并非专门针对工具调用的语义特征设计，无法精确捕捉“该工具调用是否必要”、“调用参数是否合理”、“返回结果是否被有效利用”等关键维度。

### 本文动机

针对上述瓶颈，本文的核心动机是：**构建一个专门评估工具调用质量的奖励模型，并将其无缝集成到现有 RL 框架中，从而为工具调用学习提供稳定、细粒度的训练信号**。具体而言，需要解决两个关键问题：

1. **如何构建有效的工具调用奖励模型（TRM）**：包括训练数据的获取、模型规模的选择、以及评估维度的设计。
2. **如何将 TRM 与 PPO/GRPO 等经典 RL 算法有效结合**：设计合理的信用分配（credit assignment）机制，避免奖励黑客（reward hacking）行为，确保训练稳定性与泛化能力。

图 1 概括了这一动机：子图 (a) 展示了仅用结果奖励时，正确工具调用因最终答案错误而被错误惩罚的失败案例；子图 (b) 展示了引入工具调用奖励后，每个工具调用都能获得独立的效用评估；子图 (c) 则预示了集成 TRM 后模型性能的一致提升。

## 核心创新

本工作的核心创新在于引入**工具调用奖励模型 (Tool-call Reward Model, TRM)**，将强化学习中工具调用的奖励信号从“最终答案正确性”这一粗粒度结果奖励，升级为**回合级细粒度效用评估**。这一转变直接解决了现有基于结果奖励的RL方法（如 Search-R1、ToRL）中存在的**梯度冲突**问题。

### 问题根源：结果奖励的梯度冲突

在仅使用结果奖励（outcome-only reward）的RL框架下，优化目标被定义为最大化最终答案 $y$ 与标准答案 $y^*$ 一致的概率：

$$\operatorname* { m a x } _ { \theta } \mathbb { E } _ { \tau \sim \pi _ { \theta } } \left[ \mathbb { I } \left( y = y ^ { * } \right) \right]$$

其中轨迹 $\tau$ 包含多轮思考、工具调用与最终回答。这一机制的致命缺陷在于：**一个在中间步骤做出了正确工具调用的轨迹，可能因为最终推理错误而被整体惩罚**。相反，一个工具调用质量低劣但碰巧猜对答案的轨迹却会获得正向奖励。这种“归因错位”导致策略梯度更新时产生冲突信号，严重限制了模型学习有效工具调用策略的能力。

### 核心机制：TRM 与回合级信用分配

TRM 被设计为一个专门的过程奖励模型，其核心改变体现在以下 changed slot 上：

| 奖励信号粒度 | 基线方法 | 本方法 |
|:---|:---|:---|
| **奖励信号粒度** | 仅使用最终答案正确性作为奖励（outcome-only reward） | 使用 TRM 对每个工具调用进行必要性/质量评分，将这些评分作为中间回合奖励，结合最终答案正确性 |

具体而言，TRM 对轨迹中第 $i$ 个工具调用输出一个效用评分 $\tilde{s}^i$，该评分由必要性与质量两个维度决定：只有当工具调用既对任务推进必要、又以高质量执行时，评分才为 1。TRM 的架构是将基座模型的 LM head 替换为一个二分类线性头，基于工具调用输出 $o_i$ 的最后一个 token 的隐藏状态进行预测，通过二元交叉熵损失训练：

$$\mathcal{L}_{\mathrm{BCE}} = \mathbb{E}_{\tau} \left[ - \frac{1}{n_{\tau}} \sum_{i=1}^{n_{\tau}} \left( s^{i} \log \tilde{s}^{i} + \left( 1 - s^{i} \right) \log \left( 1 - \tilde{s}^{i} \right) \right) \right]$$

在策略优化阶段，本方法设计了**回合级信用分配**，将 TRM 的中间评分与最终结果奖励结合，形成逐回合的奖励信号：

$$\tilde{r}^{i} = \begin{cases} \tilde{s}^{i}, & 1 \leq i \leq n_{\tau} \\ \mathbb{I}(y = y^{*}), & i = n_{\tau} + 1 \end{cases}$$

在 PPO 中，这些回合级奖励被映射到 token 级别；在 GRPO 中，则引入**回合级优势估计**，替代原有的组级估计。实验表明，回合级优势估计在 GRPO 中显著优于组级估计（42.47 vs 41.18），有效避免了将整个轨迹组的奖励平均化所带来的奖励黑客行为。

### 关键设计选择

1. **数据蒸馏而非人工标注**：TRM 的训练数据通过从 frontier LLM 的 rollout 中蒸馏获得，对每个工具调用进行必要性和质量的双维度评估，大幅降低了标注成本。
2. **适度规模的 TRM 即可生效**：实验表明，1.5B/3B 规模的 TRM 在仅 10K 训练样本下即可达到稳健性能，无需与策略模型同等规模。
3. **与 RL 算法的解耦集成**：TRM 作为独立奖励模型，可无缝集成到 PPO 和 GRPO 中，在搜索场景和代码数学场景下均一致提升模型表现，且对 1.5B、3B、7B 不同规模的策略模型均有效。

## 整体框架

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/002_Figure_2.jpg]]
*Figure 2: TRM-guided LLM tool invocation. (a) Generation of tool invocation trajectories and turnlevel utility labels for TRM training. (b) Turn-level credit assignment and GRPO adaptation via turn-level advantage estimation*

本文提出的工具调用奖励模型（Tool-call Reward Model, TRM）框架围绕一个核心矛盾展开：现有基于结果奖励（outcome-only reward）的强化学习方法——如Search-R1（Jin et al., 2025）和ToRL（Li et al., 2025b）——仅以最终答案正确性作为奖励信号，无法对中间工具调用的质量进行细粒度评估。这导致一个关键问题：即使模型做出了正确的工具调用，若最终答案错误，该正确调用也会被惩罚，产生梯度冲突，限制了模型学习有效工具调用策略的能力。

TRM框架通过两个阶段解决上述瓶颈：**TRM训练（Exploration）** 与 **TRM集成强化学习（Exploitation）**，整体流程如图2所示。

### 阶段一：TRM训练——工具调用效用信号的蒸馏

该阶段的目标是训练一个专门的TRM，为每个工具调用提供细粒度的必要性/质量评分。其输入输出流如下：

1. **轨迹采集（Rollout Collection）**：给定任务提示 $p$，使用策略模型（policy model）在工具池中执行多轮工具调用，生成轨迹 $\tau = (p, t_1, a_1, o_1, \dots, t_{n_\tau}, a_{n_\tau}, o_{n_\tau}, t_{n_\tau+1}, y)$，其中 $t_i$ 为思考文本，$a_i$ 为工具调用，$o_i$ 为工具返回结果，$y$ 为最终答案。

2. **工具调用评估（Tool Call Evaluation）**：利用前沿大语言模型（frontier LLM）对每个工具调用进行双重标注——必要性 $s_{\text{ne}}^i$ 和质量 $s_{\text{q}}^i$，均为二值评分。最终工具调用得分定义为二者的乘积：$s^i = s_{\text{ne}}^i \cdot s_{\text{q}}^i$。仅当工具调用既必要又高质量时，得分才为1。

3. **TRM架构与训练**：TRM基于与策略模型相同的基础LLM，但将语言建模头替换为二分类线性层。对于每个工具调用，TRM取工具输出 $o_i$ 最后一个token的隐藏状态，预测其效用分数 $\tilde{s}^i$。训练使用二元交叉熵损失：
   $$\mathcal{L}_{\text{BCE}} = \mathbb{E}_{\tau} \left[ -\frac{1}{n_\tau} \sum_{i=1}^{n_\tau} \left( s^i \log \tilde{s}^i + (1 - s^i) \log(1 - \tilde{s}^i) \right) \right]$$

### 阶段二：TRM集成——回合级信用分配与优势估计

该阶段将训练好的TRM集成到PPO/GRPO的强化学习流程中，核心创新在于**回合级信用分配（Turn-level Credit Assignment）**：

1. **回合奖励定义**：对于轨迹中的每个回合 $i$，奖励定义为：
   $$\tilde{r}^i = \begin{cases} \tilde{s}^i, & 1 \leq i \leq n_\tau \quad \text{（TRM评分）} \\ \mathbb{I}(y = y^*), & i = n_\tau + 1 \quad \text{（最终答案正确性）} \end{cases}$$
   即中间工具调用回合获得TRM的细粒度评分，最终答案回合获得结果奖励。

2. **PPO集成**：将回合级奖励映射到token级别，工具调用对应token的奖励乘以权重 $\alpha$，其余token奖励为零，最终答案token获得结果奖励。

3. **GRPO集成**：引入**回合级优势估计（Turn-level Advantage Estimation）**，按回合进行归一化，而非在组级别（group-level）统一归一化。实验表明，回合级估计能避免奖励黑客行为，性能优于组级估计（图4）。

### 模块关系总结

整个框架的因果链路为：**TRM提供逐工具调用的效用信号 → 回合级信用分配将TRM评分与结果奖励结合 → PPO/GRPO利用细粒度奖励直接优化工具调用策略 → 解决结果奖励引发的梯度冲突，提升工具使用效果与泛化能力**。实验证据表明，该框架在1.5B/3B/7B不同模型规模以及PPO/GRPO不同算法下均一致提升搜索和代码场景的表现，且仅需10K训练样本即可训练出鲁棒的3B TRM。

## 核心模块与公式推导

### 轨迹定义

工具调用过程被建模为多轮交互轨迹 $\tau$，其中包含交替出现的思考、工具调用与观察：

$$\tau = ( p , t _ { 1 } , a _ { 1 } , o _ { 1 } , \dots , t _ { n _ { \tau } } , a _ { n _ { \tau } } , o _ { n _ { \tau } } , t _ { n _ { \tau } + 1 } , y )$$

- $p$：问题/提示
- $t_i$：第 $i$ 轮思考（thought）
- $a_i$：第 $i$ 次工具调用（tool call）
- $o_i$：第 $i$ 次工具调用的返回结果（observation）
- $y$：最终答案
- $n_\tau$：轨迹中的工具调用次数

学习目标为最大化最终答案正确性的期望：

$$\operatorname* { m a x } _ { \theta } \mathbb { E } _ { \tau \sim \pi _ { \theta } } \left[ \mathbb { I } \left( y = y ^ { * } \right) \right]$$

### 工具调用奖励模型（TRM）

**核心瓶颈**：仅依赖最终答案正确性 $I(y=y^*)$ 作为奖励信号，无法区分中间工具调用的质量——正确的工具调用可能因最终答案错误而被惩罚，产生梯度冲突。

**TRM架构**：将基础语言模型的LM head替换为一个二分类头（单线性层），基于工具调用输出 $o_i$ 的最后一个token的隐藏状态预测该次工具调用的效用分数 $\tilde{s}^i$。

**训练数据蒸馏**：从前沿LLM中蒸馏训练数据，流程包括（1）rollout收集：让LLM在工具池中生成多轮轨迹；（2）工具调用评估：对每次工具调用进行必要性和质量的双维度判断。最终工具调用得分定义为两者的乘积：

$$s ^ { i } = s _ { \mathrm { n e } } ^ { i } \cdot s _ { \mathrm { q } } ^ { i }$$

仅当工具调用既对任务推进必要（$s_{ne}^i=1$）又执行质量高（$s_q^i=1$）时，得分才为1，否则为0。

**TRM训练损失**：采用二元交叉熵损失，对轨迹中所有工具调用进行监督：

$$\mathcal{L}_{\mathrm{BCE}} = \mathbb{E}_{\tau} \left[ - \frac{1}{n_{\tau}} \sum_{i=1}^{n_{\tau}} \left( s^{i} \log \tilde{s}^{i} + \left( 1 - s^{i} \right) \log \left( 1 - \tilde{s}^{i} \right) \right) \right]$$

### 回合级信用分配

将TRM的逐工具调用评分与最终结果奖励结合，定义每个回合的奖励：

$$\tilde{r}^{i} = \begin{cases} \tilde{s}^{i}, & 1 \leq i \leq n_{\tau} \\ \mathbb{I}(y = y^{*}), & i = n_{\tau} + 1 \end{cases}$$

- 前 $n_\tau$ 个回合：使用TRM预测的工具调用效用分数
- 最后一回合（最终答案）：使用答案正确性指示函数

**PPO中的token级映射**：将回合级奖励映射到token序列上，工具调用token被赋予带权重 $\alpha$ 的回合奖励，最终答案token获得最终回合奖励，其余token奖励为0：

$$r^{j} = \begin{cases} \alpha \cdot \tilde{r}^{\mathcal{Z}(j)}, & j \in \mathcal{E} \\ \tilde{r}^{\mathcal{T}(j)}, & j = L \\ 0, & \mathrm{otherwise} \end{cases}$$

其中 $\mathcal{E}$ 为工具调用token集合，$L$ 为最终答案token位置，$\mathcal{Z}(j)$ 和 $\mathcal{T}(j)$ 将token位置映射到对应回合。

**GRPO中的回合级优势估计**：GRPO目标函数采用带裁剪的重要性采样：

$$\mathcal{L}_{\mathrm{GRPO}} = \mathbb{E}_{\{\tau_g\} \sim \pi_\theta} \left[ \frac{1}{G} \sum_{g=1}^G \frac{1}{|\mathcal{M}|} \sum_{j \in \mathcal{M}} \min\left( w_g^j(\theta) \cdot A_g^j, \mathrm{clip}(w_g^j(\theta), 1-\varepsilon, 1+\varepsilon) A_g^j \right) \right]$$

其中token级优势 $A_g^j$ 定义为：

$$A_g^j = r_g^{L_g} + \sum_{m=j}^{L_g-1} \gamma^{m-j} r_g^m$$

回合级优势估计将优势计算按工具调用回合进行归一化，相比组级估计避免了奖励黑客行为，实验表明其性能更优。

## 实验与分析

### 核心实验结果

TRM 在不同模型规模（1.5B/3B/7B）和强化学习算法（PPO/GRPO）的两个典型场景——搜索式问答（search QA）与代码辅助数学推理（code-based math）——中均一致性地提升了模型性能。这一结论得到多组实验的支持，证据强度高。

**搜索式问答场景**（Table 1）：在 Qwen2.5-3B-Instruct 上，Search-R1-GRPO-TRM 取得 43.49 的平均分，优于仅使用结果奖励的 Search-R1-GRPO 及其他基线；在 Qwen2.5-7B-Instruct 上，同一方法取得 48.62 的平均分，同样占据最优位置。值得注意的是，启用工具调用的 RL 方法（Search-R1 系列）普遍大幅领先无工具调用的纯推理 RL 方法（R1-PPO、R1-GRPO），说明动态学习工具使用本身带来的增益显著，而 TRM 在此基础之上进一步放大了这一优势。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/009_Table_1.jpg]]
*Table 1: Performance of Qwen2.5 variants with different methods on various QA tasks. Best results are in bold; second best are underlined*

**代码辅助数学推理场景**（Table 2）：在 Qwen2.5-Math-1.5B 上，ToRL-GRPO-TRM 取得 45.42 的平均分；在 Qwen2.5-Math-7B 上，同一方法取得 53.70 的平均分，均为各自规模下的最佳结果。GRPO 在该场景下整体优于 PPO，但集成 TRM 后两种算法均获得可靠提升。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/010_Table_2.jpg]]
*Table 2: Performance of Qwen2.5-Math variants with different methods on various math problems. Best results are in bold; second best are underlined*

**跨场景一致性**：TRM 的增益在搜索和代码两个差异较大的工具调用场景中均成立，表明其提供的细粒度工具调用效用信号具有场景泛化性，而非对特定任务设计的过拟合。

### 关键消融与分析

**TRM 规模与数据量的影响**（Figure 3）：中等规模的 TRM（1.5B/3B）在使用约 10K 训练样本时即可达到最优性能。进一步增大模型或数据量并未带来明显的额外收益，说明稳健的工具调用奖励信号可以通过适度的资源投入获得。

**回合级 vs. 组级优势估计**（Figure 4）：在 GRPO 中，回合级（turn-level）优势估计取得 42.47 的准确率，优于组级（group-level）估计的 41.18。组级估计存在奖励黑客（reward hacking）风险：模型倾向于生成更多工具调用来稀释每个调用的惩罚，导致 TRM 评分随调用次数增加而下降（Figure 7-a）。回合级估计通过对每个工具调用回合独立归一化，有效缓解了这一问题（Figure 7-b）。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/014_Figure_4.jpg]]
*Figure 4: Comparison of group-level and turnlevel advantage estimation in GRPO*

**超参数 α 的敏感性**（Figure 5-a, 5-b）：α 控制 PPO 中工具调用 token 的奖励权重。实验表明，α 在合理范围内（如 0.5–1.0）对最终性能影响有限，但过大或过小的值会导致性能下降。GRPO 对 α 的敏感度低于 PPO，这与 GRPO 本身基于组内相对比较的机制一致。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/013_Figure_5.jpg]]
*Figure 5: Summary of key analysis results. Subfigures (a) and (b) present the influence of the hyperparameter α on PPO and GRPO in conjunction with TRM. Subfigure (c) demonstrates that TRM improves the generalization capability of LLM for tool-use*

**与过程监督方法的比较**（Figure 6-a）：在搜索场景下，TRM 方法一致优于 StepSearch 和 AgentPRM 两种过程监督基线。StepSearch 针对搜索 QA 设计，AgentPRM 是通用过程监督方法，但两者均未达到 TRM 的性能水平，说明专门针对工具调用设计的细粒度奖励信号比通用过程监督更有效。

**轨迹级 ORM 的失效**（Figure 6-b）：将 TRM 退化为轨迹级结果奖励模型（ORM）时，其性能甚至低于仅使用最终答案奖励的基线。这表明，工具调用场景中的信用分配必须精确到每个调用回合；粗粒度的轨迹级评分无法区分正确与错误的工具调用，反而引入了噪声。

**泛化能力**（Figure 5-c）：TRM 显著提升了模型在工具调用上的泛化能力。在未见过的工具或任务分布上，集成 TRM 的模型表现优于仅使用结果奖励的模型，表明 TRM 学习的工具调用效用评估具有一定的迁移性。

### 失败模式与局限

**奖励黑客行为**：如前所述，组级优势估计下模型会通过增加工具调用次数来“稀释”负奖励，导致调用质量下降。回合级估计是有效的缓解手段，但并未从根本上消除模型对奖励信号进行博弈的可能性。

**TRM 作为验证器的局限**：若仅在推理时使用 TRM 作为验证器（而非在训练中集成），性能提升有限，且仍落后于完整的 TRM 训练方案（Figure 6-b）。这说明 TRM 的核心价值在于训练阶段的细粒度信用分配，而非简单的推理时重排序。

**计算开销**：集成 TRM 会引入额外的训练和推理开销。根据 Table 5，在 8×A800 GPU 上使用 PPO 训练时，TRM 的加入会降低训练和 Best-of-N 推理的速度。具体数值需查阅原表确认，但这一开销在资源受限场景下可能成为部署瓶颈。

**多工具场景的初步验证**：Table 7 展示了在更多样化的多工具场景（ReCall）中，TRM 将 F1 从 39.71 提升至 43.28，验证了方法的可扩展性。但该实验仅覆盖了一个特定设置，更广泛的多工具、多步骤场景仍需进一步验证。

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_LnBEASInVr/figures/024_Table_7.jpg]]
*Table 7: Performance in more diverse multi-tool scenarios on Qwen2.5-7B-Instruct with GRPO*

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | TRM 在搜索 QA 场景下一致提升 3B/7B 模型性能，Search-R1-GRPO-TRM 最优 |
| Table 2 | TRM 在代码数学场景下一致提升 1.5B/7B 模型性能，ToRL-GRPO-TRM 最优 |
| Figure 3 | 1.5B/3B TRM + 10K 样本即可达到稳健性能 |
| Figure 4 | 回合级优势估计优于组级估计（42.47 vs. 41.18） |
| Figure 5-c | TRM 显著提升工具调用的泛化能力 |
| Figure 6-a | TRM 方法优于 StepSearch 和 AgentPRM 过程监督基线 |
| Figure 6-b | 轨迹级 ORM 失效，TRM 作为纯验证器提升有限 |
| Figure 7 | 组级估计导致奖励黑客，回合级估计有效缓解 |

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

现有基于强化学习（RL）的工具调用训练方法普遍采用**结果奖励（outcome-only reward）**——仅以最终答案的正确性作为奖励信号。该设计的根本缺陷在于：**中间工具调用的质量无法被细粒度评估**，导致正确的工具调用可能因最终答案错误而被错误惩罚，产生梯度冲突，严重限制模型学习有效工具调用策略的能力。本文提出的**工具调用奖励模型（Tool-call Reward Model, TRM）**正是针对这一瓶颈，通过引入逐工具调用的效用评估信号，从根本上解耦工具调用质量与最终答案正确性之间的耦合惩罚。

### 方法谱系定位

TRM 位于**过程监督（process supervision）**与**工具增强强化学习**的交叉地带。其方法谱系可从以下维度梳理：

**1. 纯推理强化学习（无工具调用）**

- **R1-PPO / R1-GRPO**（Guo et al., 2025）：在无工具调用场景下使用 PPO/GRPO 进行纯推理 RL 训练。本文实验表明，这类方法在需要工具调用的搜索和代码场景中表现显著弱于工具增强方法，验证了工具调用能力对复杂任务的关键作用。

**2. 工具增强强化学习（仅结果奖励）**

- **Search-R1-PPO / Search-R1-GRPO**（Jin et al., 2025）：搜索场景下使用 PPO/GRPO，但仅依赖结果奖励。
- **ToRL-PPO / ToRL-GRPO**（Li et al., 2025b）：代码数学场景下使用 PPO/GRPO，同样仅依赖结果奖励。

这两组方法是 TRM 的直接基线。TRM 在保持相同 RL 算法框架的前提下，将奖励信号从单一结果奖励替换为“TRM 回合评分 + 结果奖励”的组合，从而在不改变算法结构的情况下实现一致提升。

**3. 过程监督方法**

- **StepSearch**（Wang et al., 2025b）：面向搜索 QA 的过程监督方法。
- **AgentPRM**（Choudhury, 2025）：通用过程监督方法。
- **ORM（Outcome Reward Model）**：轨迹级结果奖励模型。

TRM 与上述方法的关键差异在于**监督粒度和信用分配机制**：
- StepSearch 和 AgentPRM 提供通用过程监督，但未专门针对工具调用的必要性/质量进行建模；
- ORM 评估整条轨迹，粒度粗于 TRM 的逐工具调用评估；
- 实验表明，轨迹级 ORM 甚至弱于纯答案基线，而 TRM 作为验证器（verifier）虽略有提升，仍显著弱于完整的 TRM 集成方案，印证了**回合级信用分配**的必要性。

**4. 检索增强与工具使用基线**

- **IRCoT**：迭代检索增强生成。
- **RAG**：单步检索增强生成。
- **Instruct+PAL**（Gao et al., 2023）：程序辅助语言模型的指令版本。

这些方法代表非 RL 的工具使用范式。TRM 通过 RL 动态学习工具调用策略，在搜索和代码场景中均显著优于上述静态方法。

### 方法适用边界

TRM 的设计存在以下明确边界：

1. **工具调用必要性/质量可标注**：TRM 训练数据依赖前沿 LLM 对工具调用的必要性（necessity）和质量（quality）进行二元标注（$s^i = s_{ne}^i \cdot s_q^i$）。这意味着 TRM 的监督质量受限于标注 LLM 的能力边界。

2. **工具调用输出可观测**：TRM 评分基于工具调用输出 $o_i$ 的最后一个 token 的隐状态，要求工具返回结构化或可编码的输出。对于非结构化或开放式工具交互场景，该设计的有效性需进一步验证。

3. **回合结构明确**：TRM 的回合级信用分配假设轨迹具有明确的工具调用回合边界（thought → tool call → observation），对于连续或隐式工具调用场景的适应性尚不明确。

### 局限与开放问题

1. **TRM 规模与数据的效率边界**：实验表明中等规模 TRM（1.5B/3B）配合 10K 训练样本即可达到稳健性能，但更大规模 TRM 或更多训练数据是否带来持续增益，以及跨任务迁移的样本效率，仍需系统研究。

2. **奖励黑客风险**：尽管回合级优势估计优于组级估计，TRM 作为学习得到的奖励模型本身可能被策略模型利用（reward hacking）。本文未深入讨论 TRM 自身的鲁棒性退化问题。

3. **多工具协同场景**：当前 TRM 评估单个工具调用的效用，对于需要多工具协同调用的复杂任务，工具调用间的依赖关系未被显式建模。

4. **超参数敏感性**：PPO 中工具调用 token 的奖励权重 $\alpha$ 对性能有显著影响，其最优值可能依赖具体任务和模型规模，需要额外调参成本。

5. **开放域工具的泛化**：TRM 在搜索和代码两类场景中展现了跨场景泛化能力，但向更广泛的工具生态（如 API 调用、数据库操作）的泛化能力尚待验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Empowering_LLM_Tool_Invocation_with_Tool_call_Reward_Model.pdf]]
