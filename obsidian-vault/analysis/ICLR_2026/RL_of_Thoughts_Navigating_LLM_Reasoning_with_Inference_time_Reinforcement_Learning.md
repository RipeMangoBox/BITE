---
title: "RL of Thoughts: Navigating LLM Reasoning with Inference-time Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RL_of_Thoughts_Navigating_LLM_Reasoning_with_Inference_time_Reinforcement_Learning.pdf
openreview_forum_id: Dw034qKrP5
aliases:
- RTR
- RTNLRITRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过强化学习训练一个轻量级导航器，使其学会在推理的每一步根据当前状态（由LLM自我评估得到）动态选择最合适的认知逻辑块，从而构建任务特定的推理链条。"
primary_logic: "将长序列推理过程建模为马尔可夫决策过程（MDP），定义五种受人类认知启发的逻辑块作为动作空间，利用过程奖励模型（PRM）提供逐步骤的稠密奖励，仅训练一个参数极少（<3K）的MLP导航器，在推理时引导LLM自适应地生成逻辑结构，显著提升小模型的推理能力并实现跨模型跨任务迁移。"
claims:
- "RLoT在多种LLM（Qwen、Llama、GPT、DeepSeek）上一致超越所有推理时基线，在GPQA上相对最佳基线提升高达13.4%。"
- "导航器仅用不到3K参数便可使7-8B模型达到与数十亿参数大模型（如Qwen2.5-72B）相当甚至更优的性能，展示显著的参数效率。"
- "导航器具备强大的迁移能力：在单任务/LLM上训练的RLoT可直接应用于未见过的LLM和任务，且性能与专门训练相当或更优。"
- "GPQA 上 Accuracy (%) = 46.88 (Llama3.1-8B)"
---

# RL of Thoughts: Navigating LLM Reasoning with Inference-time Reinforcement Learning

> [!tip] 核心洞察
> 将长序列推理过程建模为马尔可夫决策过程（MDP），定义五种受人类认知启发的逻辑块作为动作空间，利用过程奖励模型（PRM）提供逐步骤的稠密奖励，仅训练一个参数极少（<3K）的MLP导航器，在推理时引导LLM自适应地生成逻辑结构，显著提升小模型的推理能力并实现跨模型跨任务迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 思维强化学习：利用推理时强化学习导航大语言模型推理 |
| 英文题名 | RL of Thoughts: Navigating LLM Reasoning with Inference-time Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Dw034qKrP5); [GitHub](https://github.com/tsinghua-fib-lab/RL-LLM-Reasoning) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RL-of-Thoughts (RLoT) |
| Dataset | GPQA, Overall Average (7 tasks), Overall Average (5 tasks) |

> [!tip] 效果简介
> - GPQA 上，Accuracy (%) 为 46.88 (Llama3.1-8B)，对比 33.48 (CoT-SC, best baseline)，变化 +13.40。
> - Overall Average (7 tasks) 上，Average Accuracy (%) 为 82.92 (DeepSeek-R1-Distill-Qwen-7B)，对比 76.34 (Few-shot CoT, best baseline)，变化 +6.58。
> - Overall Average (5 tasks) 上，Average Accuracy (%) 为 71.70 (Llama3.1-8B)，对比 64.89 (CoT-SC, best baseline)，变化 +6.81。

## 概述

大语言模型（LLM）在复杂推理任务上的表现高度依赖推理时增强技术。现有方法（如链式思维 CoT、思维树 ToT）虽有效，但均依赖人工预定义的固定逻辑结构——线性链或两层五节点树——无法根据问题特征和推理过程的中间状态动态调整，导致在多样化任务上适应性不足。这一瓶颈在数学证明、STEM 问答等需要多步严谨推理的场景中尤为突出。

**RL-of-Thoughts (RLoT)** 针对上述瓶颈提出了一种推理时强化学习框架。其核心洞察是：将长序列推理过程建模为马尔可夫决策过程（MDP），定义五种受人类认知启发的**基本逻辑块**（Reason one step、Decompose、Debate、Refine、Terminate）作为动作空间，利用过程奖励模型（PRM）提供逐步骤的稠密奖励，仅训练一个参数极少（<3K）的 MLP 导航器，使其学会在推理的每一步根据当前状态动态选择最合适的逻辑块，从而为每个任务构建自适应的推理结构。

实验表明，RLoT 在多种 LLM（Qwen、Llama、GPT、DeepSeek）上一致超越所有推理时基线：在 GPQA 上相对最佳基线提升 **13.4%**，在 7 个任务的整体平均准确率上提升 **6.58%**（DeepSeek-R1-Distill-Qwen-7B）。该导航器仅用不到 3K 参数，便可使 7-8B 模型达到与数十亿参数大模型（如 Qwen2.5-72B）相当甚至更优的性能。更重要的是，在单任务/LLM 上训练的导航器可直接应用于未见过的 LLM 和任务，性能与专门训练相当或更优，展现出显著的跨模型跨任务迁移能力。

方法层面，RLoT 处于**推理时增强**与**强化学习引导生成**的交汇点。与固定模式的 CoT/ToT 不同，它通过 RL 学习推理逻辑结构的生成策略；与基于最终答案的稀疏奖励训练不同，它引入 PRM 提供步骤级反馈。这一设计使 RLoT 在保持极低参数开销的前提下，实现了对推理过程的自适应控制。

## 背景与动机

大语言模型（LLM）在数学推理、代码生成、科学问答等复杂任务上的表现，高度依赖于推理过程中所采用的逻辑结构。自回归生成范式下，LLM 通过最大化条件概率 $\prod_{t=1}^{T} P(w_t | w_1, w_2, ..., w_{t-1})$ 逐 Token 生成文本，但这一过程本身并不包含对推理路径的显式规划。

为弥补这一缺陷，研究者提出了多种推理时增强方法。**Zero-shot CoT**（Wei et al., 2022）和 **Few-shot CoT**（Wei et al., 2022）通过提示词诱导模型生成线性推理链；**CoT-SC**（Wang et al., 2023）进一步引入多次采样与多数投票机制以提升鲁棒性；**ToT**（Yao et al., 2023）则采用预设的树形结构（两层、每层五节点）进行多路径探索。这些方法的共同瓶颈在于：**推理逻辑结构是人工预定义的固定模式，无法根据问题特征和推理过程动态调整**。面对数学证明、多跳推理、科学论证等多样化任务时，固定的线性链或树结构难以匹配任务所需的认知操作组合，导致适应性不足。

RLoT（RL-of-Thoughts）的提出正是针对这一缺口。其核心动机在于：**将推理逻辑结构的生成从人工设计转变为可学习的自适应过程**。具体而言，RLoT 将长序列推理建模为马尔可夫决策过程 $(S, \rho, \mathcal{A}, P, R)$，设计五种受人类认知启发的逻辑块（单步推理、问题分解、自我辩论、步骤精炼、终止）作为动作空间，训练一个参数极少（<3K）的轻量级导航器。该导航器在推理的每一步根据当前状态动态选择最合适的逻辑块，从而为每个问题自动构建任务特定的推理链条，而非依赖预设的固定模板。

这一设计的直接效果是：**仅用不到 3K 参数的导航器，便可使 7-8B 规模的小模型在多项推理基准上达到与数十亿参数大模型（如 Qwen2.5-72B）相当甚至更优的性能**，同时展现出跨模型、跨任务的强迁移能力。

## 核心创新

RLoT的核心创新在于将大语言模型的长序列推理过程**显式建模为马尔可夫决策过程（MDP）**，并引入一个极轻量的强化学习导航器来动态编排推理逻辑结构，从而突破了现有推理时增强方法依赖人工预定义固定模式的根本瓶颈。

### 瓶颈突破：从固定结构到自适应编排

现有推理时增强方法——无论是零样本/少样本链式思维（Zero-shot/Few-shot CoT, Wei et al., 2022）、自一致性链式思维（CoT-SC, Wang et al., 2023）还是思维树（ToT, Yao et al., 2023）——均依赖人工设计的固定逻辑结构。CoT系列强制模型沿线性链条推理，ToT虽引入多路径探索，但采用预设的两层五节点树结构。这种"一刀切"的策略忽视了不同问题在难度、领域和推理路径上的本质差异，导致在多样化任务上适应性不足。

RLoT通过三个相互耦合的关键机制（changed slots）实现了从固定结构到自适应编排的范式转变：

**1. 推理逻辑结构的动态生成**

RLoT将动作空间定义为五种受人类认知启发的基本逻辑块：单步推理（Reason one step）、问题分解（Decompose）、自我辩论（Debate）、答案精炼（Refine）和终止（Terminate）。导航器在推理的每一步根据当前状态从这五种原子操作中动态选择最优动作，从而组合出任务特定的推理逻辑结构。例如，在数学推理任务（MATH）中，导航器自发形成了"推理-精炼"（Reason-Refine）的两步模式；而在常识推理任务（StrategyQA）中，则更倾向于"推理-辩论-推理"的三步模式（Table 5）。这种自适应能力是任何固定结构基线无法实现的。

**2. 推理状态的显式表征**

传统方法缺乏对推理中间状态的显式建模，仅将原始文本上下文作为隐式状态。RLoT创新性地引入**状态自评估模块**：通过提示固定LLM对当前推理步进行七个细粒度维度的自我评估（涵盖完整性、正确性、清晰度等三大方面，Table 1），输出一个低维状态向量。这一设计将高维、非结构化的文本推理状态压缩为RL导航器可直接处理的紧凑表征，为后续动作选择提供了信息丰富的决策依据。实验表明，对该状态向量添加噪声会系统性降低性能，但方法对30%噪声仍表现出较好鲁棒性（Table 14），验证了状态信号的有效性与稳定性。

**3. 步骤级稠密奖励的训练信号**

传统方法或无需训练，或仅基于最终答案正确与否的稀疏奖励。RLoT采用外部过程奖励模型（Math-Shepherd PRM）对每一步推理质量提供即时、稠密的评分信号，用于训练导航器的策略。消融实验证实，使用PRM训练导航器比仅用结果奖励模型（ORM）获得更高平均准确率（72.18 vs 69.14, Table 17），验证了步骤级反馈对学习有效推理编排策略的关键作用。

### 方法论定位：推理时RL的轻量化范式

RLoT在方法谱系中占据独特位置：它不同于训练时RLHF/DPO等方法直接微调LLM全部参数，也不同于纯推理时的提示工程方法。RLoT在**推理时**应用强化学习，但仅训练一个参数极少的MLP导航器（采用Dueling网络结构，总参数量<3K），而非LLM本身。这种"推理时轻量RL"范式使得小模型（如7-8B）在导航器的引导下，能够达到与数十亿参数大模型（如Qwen2.5-72B）相当甚至更优的性能（Table 9），展现出显著的参数效率。

### 证据强度与边界

核心创新的有效性由多维度实验支撑：在GPQA上相对最佳基线CoT-SC提升13.4%（Llama3.1-8B, Table 2），在七任务平均上提升6.58%（DeepSeek-R1-Distill-Qwen-7B, Table 2）。导航器展现出强大的跨模型和跨任务迁移能力——在单一LLM/任务上训练的导航器可直接应用于未见过的LLM和任务，且性能与专门训练相当或更优（Table 3, Table 4）。

然而，该创新存在明确边界：状态自评估模块在约82%的情况下准确，近20%的错误评估率可能引发动作选择的级联偏差（Figure 6, Figure 7）；训练依赖PRM质量，若PRM给出噪声较大的评分，可能误导策略学习；当前验证集中于数学、STEM和常识推理等文本任务，在多模态或需外部工具交互的场景下的表现尚待验证。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/001_Figure_1.jpg]]
*Figure 1: Framework of RL-of-Thoughts (RLoT). We train an RL agent as the navigator, which dynamically selects and combines basic logic blocks along the reasoning process, constructing task-specific logical structures for each task and thereby enhancing the LLMs’ ability to handle complex reasoning tasks*

RL-of-Thoughts (RLoT) 将大语言模型的长序列推理过程形式化为一个马尔可夫决策过程（MDP），其核心思想是**将“如何推理”本身作为一个可学习的序列决策问题**。框架由四个协同模块构成，形成闭环的推理时增强管线。

### 管线概览

给定一个输入问题，RLoT 在每一步执行以下循环：

1. **状态自评估模块**：固定 LLM 根据设计好的提示，对当前推理步从七个细粒度维度进行自我评估（Table 1），输出一个低维状态向量 $s_t$。这七个维度涵盖推理的完整性、正确性、信息充分性等关键方面。
2. **导航器（Dueling MLP）**：一个仅含不到 3K 参数的三层 MLP，采用 Dueling 网络结构（Wang et al., 2016），以状态向量 $s_t$ 为输入，输出离散动作 $a_t \in \mathcal{A}$，即从五种基本逻辑块中选择其一。
3. **逻辑块执行器（LLM）**：同一 LLM 根据导航器选中的动作 $a_t$，使用对应的提示模板执行一步推理操作。五种逻辑块分别为：
   - **Reason one step**：执行一步直接推理
   - **Decompose**：将当前问题分解为子问题
   - **Debate**：对当前推理进行多角度辩论
   - **Refine**：基于已有推理进行精炼修正
   - **Terminate**：终止推理并输出答案
4. **过程奖励模型（PRM）**：外部 Math-Shepherd PRM 对当前推理步的质量进行评分，提供即时奖励信号 $r_t$，用于导航器的 RL 训练。

上述循环持续进行，直至导航器选择 Terminate 动作或达到最大步数限制。最终，通过多次重复运行并利用自一致性（self-consistency）多数投票得到最终答案。

### 训练与推理的分离

RLoT 的关键设计在于**训练与推理的角色分离**：
- **训练阶段**：仅训练轻量级导航器（<3K 参数），LLM 和 PRM 均保持冻结。采用 Double-Dueling-DQN 算法优化，利用 PRM 提供的逐步骤稠密奖励作为训练信号。训练数据仅使用 LLM 无法直接正确回答的困难问题。
- **推理阶段**：训练好的导航器引导同一 LLM（或未见过的 LLM）在推理时动态构建任务特定的逻辑结构，无需额外训练。

### 核心洞察

该框架的根本创新在于将推理逻辑结构从**人工预定义的固定模式**（如 CoT 的线性链、ToT 的两层五节点树）转变为**由 RL 导航器根据问题特征和推理过程动态选择的自适应结构**。这使小模型（7-8B）在复杂推理任务上能够达到与数十倍参数量大模型（如 Qwen2.5-72B）相当甚至更优的性能。

## 核心模块与公式推导

### 推理过程的形式化建模

RLoT将长序列推理过程建模为马尔可夫决策过程（MDP），定义如下元组：

$$(S, \rho, \mathcal{A}, P, R)$$

其中 $S$ 为状态空间，$\rho$ 为初始状态分布，$\mathcal{A}$ 为动作空间，$P$ 为状态转移概率，$R$ 为奖励函数。在此框架下，推理的每一步对应MDP中的一个时间步，导航器的目标是最大化累积折扣奖励：

$$G_t = \sum_{k=0}^{\infty} \gamma^k r_{t+k}$$

其中 $\gamma$ 为折扣因子，$r_{t+k}$ 为第 $t+k$ 步的过程奖励。

### 核心模块设计

RLoT由四个关键模块构成推理闭环：

**状态自评估模块**：在每个推理步，固定LLM根据设计好的提示，对当前推理状态进行七个细粒度维度的自我评估（Table 1），输出一个低维状态向量。该向量编码了推理进度、中间结果正确性、逻辑一致性等关键信息，作为导航器的输入。实验表明，该模块在约82%的情况下评估准确，对约30%的噪声仍表现出较好鲁棒性（Table 14）。

**导航器（Dueling MLP）**：导航器是一个三层多层感知机，采用Dueling Network架构，总参数量不到3K。其输入为状态自评估模块产生的状态向量，输出为离散动作——五种基本逻辑块之一。训练采用Double-Dueling-DQN算法进行优化。

**逻辑块执行器（LLM）**：根据导航器选择的动作，使用对应的提示模板驱动同一LLM执行具体推理操作。五种基本逻辑块包括：Reason one step（单步推理）、Decompose（问题分解）、Debate（多角度辩论）、Refine（结果精炼）和Terminate（终止推理）。

**过程奖励模型（PRM）**：采用Math-Shepherd作为外部PRM，对当前推理步的质量进行即时评分，为RL训练提供稠密的步骤级奖励信号。消融实验表明，使用PRM训练导航器比仅用结果奖励模型（ORM）获得更高平均准确率（72.18 vs 69.14），验证了步骤级反馈的关键作用（Table 17）。

### 关键公式变量说明

自回归LLM生成Token序列的条件概率乘积为：

$$\prod_{t=1}^{T} P(w_t | w_1, w_2, ..., w_{t-1})$$

其中 $w_t$ 为第 $t$ 个Token，$T$ 为序列总长度。该公式描述了LLM逐Token生成的本质，RLoT通过在此生成过程中插入逻辑块选择动作，在不修改LLM参数的前提下改变推理路径。

## 实验与分析

### 核心实验设置

RLoT的实验设计遵循严格的公平性原则：所有基线方法使用与RLoT相同的提示策略和底层LLM，并在统一的自一致性设置下（4次采样多数投票）评估。RLoT的训练仅使用对应LLM无法直接解答的困难问题，不引入额外数据优势。计算开销对比在相同硬件和推理框架下进行。

### 总体性能：一致超越推理时基线

Table 2展示了RLoT在五种LLM、七个推理基准上的全面对比。RLoT在所有LLM上一致超越五种推理时基线方法（Direct QA、Zero-shot CoT、Few-shot CoT、CoT-SC、ToT），核心结果如下：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/005_Table_2.jpg]]
*Table 2: Overall evaluation of RLoT’s capability to enhance multiple LLMs’ reasoning across different tasks. The bold numbers indicate the best performance in each group of experiments, and the underlined numbers indicate the best baseline method*

- **GPQA（STEM推理）**：RLoT在Llama3.1-8B上达到46.88%，相对最佳基线CoT-SC（33.48%）提升**13.4个百分点**，这是所有实验中最大的单项提升。
- **DeepSeek-R1-Distill-Qwen-7B**：在七个任务上的总体平均准确率达82.92%，相对最佳基线Few-shot CoT（76.34%）提升6.58个百分点。
- **Llama3.1-8B**：在五个任务上的平均准确率达71.70%，相对最佳基线CoT-SC（64.89%）提升6.81个百分点。

这一性能提升的关键机制在于：RLoT的导航器能够根据问题特征动态选择逻辑块组合，而非依赖人工预定义的固定推理结构。在GPQA这类需要深度STEM推理的任务上，动态结构的优势尤为显著。

### 参数效率：<3K参数弥合数十亿参数差距

RLoT的导航器模型仅为一个三层MLP，采用Dueling Network架构，总参数量不足3,000个。Table 9表明，这一轻量级导航器使7-8B参数的小模型达到与数十亿参数大模型相当甚至更优的性能：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/021_Table_9.jpg]]
*Table 9: Performance comparison between sub-10B LLMs enhanced by RLoT, and larger LLMs with several times of parameters*

- Qwen2.5-14B配合RLoT在五个基准上平均准确率达79.21，与Qwen2.5-72B（80.92）的差距不足2个百分点。
- Llama3.1-8B配合RLoT在五个基准上平均准确率71.70，显著超越未经增强的Qwen2.5-14B（67.71）。

这一发现表明，推理能力的瓶颈并非完全在于模型参数规模，而在于推理时逻辑结构的生成方式。RLoT以极小的参数代价实现了推理策略的智能调度。

### 跨模型与跨任务迁移

RLoT展现出强大的迁移能力。Table 3显示，在MATH基准上训练的导航器可直接应用于未见过的LLM，且性能与专门训练相当或更优：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/006_Table_3.jpg]]
*Table 3: Evaluation of RLoT’s transferability across different LLMs. We train navigator models with three different LLMs on the MATH benchmark and cross-test the obtained navigator models with other LLMs. We also list CoT-SC, the best baseline method, for comparison*

- 在Qwen2.5-14B上训练的导航器，直接应用于Llama3.1-8B时，MATH准确率达56.56%，显著超越CoT-SC（51.74%）。
- 在GPT-4o-mini上训练的导航器应用于Qwen2.5-14B时，准确率达68.39%，同样超越CoT-SC（65.32%）。

Table 4进一步展示了跨任务迁移：在MATH上训练的导航器应用于GPQA时准确率达51.34%（CoT-SC为45.54%）；在GPQA上训练的导航器应用于MATH时准确率达61.27%（CoT-SC为57.00%）。这表明导航器学到了任务无关的推理调度策略，而非特定任务的表面模式。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/007_Table_4.jpg]]
*Table 4: Evaluation of RLoT’s transferability across different tasks. We train navigator models with Qwen2.5-14B-Instruct on three different tasks and cross-test the obtained navigator models on other tasks. We also list CoT-SC, the best baseline method, for comparison*

### 逻辑块消融：精炼步骤至关重要

Table 6的消融实验揭示了各逻辑块对性能的差异化贡献：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_Dw034qKrP5/figures/009_Table_6.jpg]]
*Table 6: Ablation study results for each logic block*

- **移除Refine块**在Qwen2.5-7B上导致GPQA性能从44.64降至41.29，降幅最大。这说明在复杂计算任务中，对中间推理步骤的精炼和纠错至关重要。
- **所有三种核心逻辑块（Decompose、Debate、Refine）**均对最终性能有正向贡献；移除任何一个均使平均分数降低。
- 在GPT-4o-mini上，移除Debate块的降幅最大（从71.35降至68.66），暗示更强的基座模型可能从多角度辩论中获益更多。

### 典型推理模式

Table 5统计了RLoT在不同任务上生成的典型逻辑结构模式：

- **MATH和GPQA**：最常见的两步模式是Reason-Refine（先推理一步，再精炼结果），三步模式则以Reason-Debate-Refine为主。这反映了数学和STEM任务对验证和修正的强需求。
- **StrategyQA（常识推理）**：以Reason-Decompose-Refine为主要三步模式，说明常识推理需要先将问题分解为子问题再逐步精炼。

这些模式并非人工预设，而是导航器通过RL训练自主发现的，体现了任务自适应的逻辑结构生成能力。

### 奖励信号选择：PRM优于ORM

Table 17对比了使用过程奖励模型（PRM）与结果奖励模型（ORM）训练导航器的效果。PRM训练的平均准确率达72.18，显著高于ORM的69.14。步骤级的稠密反馈使导航器能够更精确地评估每一步推理的质量，从而学习到更优的动作选择策略。

### 状态噪声鲁棒性

Table 14显示，对自我评估状态添加噪声会降低性能，但RLoT对30%噪声仍表现出较好的鲁棒性。这证明状态信号的稳定性对RLoT有效，但方法并非完全依赖完美的状态评估——约82%准确率的状态自评估模块（见Table 13示例）已足以支撑有效的策略学习。

### 计算开销分析

Table 7和Table 8对比了各方法的Token消耗和求解时间。RLoT的导航器能直接生成任务特定的逻辑轨迹，减少了LLM交互成本。轻量级MLP导航器的推理开销几乎可忽略不计，整体计算效率优于需要大量并行采样的ToT等方法。

### 失败模式分析

RLoT的主要失败来源有两类：

1. **状态自评估错误**（Figure 6）：当LLM对当前推理状态的自我评估出现偏差（约18%的错误率），导航器基于错误状态选择动作，导致推理偏离正确方向。
2. **动作选择错误**（Figure 7）：即使状态评估正确，导航器仍可能选择次优的逻辑块，尤其在复杂推理的早期阶段。

这两类失败模式指向了RLoT的核心瓶颈：导航器的决策质量受限于状态表示的质量和PRM奖励信号的准确性。

## 方法谱系与知识库定位

### 1. 与现有推理时增强方法的谱系关系

RLoT 处于“推理时增强”这一方法谱系中，该谱系的共同目标是在不修改大语言模型参数的前提下，通过外部机制提升推理质量。RLoT 与谱系内各方法的本质差异在于**推理逻辑结构的生成方式从静态、人工预定义转向动态、自适应学习**。

*   **静态推理结构方法**：这类方法使用固定的逻辑模板引导 LLM 推理。
    *   **Zero-shot CoT** (Wei et al., 2022) 和 **Few-shot CoT** (Wei et al., 2022) 通过单一的“逐步思考”提示或少量示例，将推理过程强制约束为线性链。这种结构在所有任务上保持不变，无法根据问题难度或推理阶段进行适应性调整。
    *   **CoT-SC** (Wang et al., 2023) 在 CoT 的基础上引入了多样性和自一致性，通过对同一线性链的多次采样和多数投票来提升鲁棒性，但其底层逻辑结构依然是固定的线性链。
    *   **ToT** (Yao et al., 2023) 引入了树状结构进行多路径探索，但其树结构（如两层、每层五节点）是预定义的，不具备问题自适应性。

*   **RLoT 的定位：自适应逻辑结构学习**：RLoT 与上述方法的根本区别在于，它将推理过程建模为马尔可夫决策过程（MDP），并训练一个轻量级强化学习导航器来动态构建逻辑结构。该导航器在推理的每一步，根据 LLM 的当前状态，从五种受人类认知启发的**基本逻辑块（Reason one step, Decompose, Debate, Refine, Terminate）** 中选择一个动作。这使得 RLoT 能够为不同任务甚至同一任务的不同推理阶段，生成完全不同的逻辑结构（如“推理-精炼”、“分解-推理-辩论”等模式），实现了从“一刀切”到“因题制宜”的转变。

### 2. 核心机制与知识库定位

RLoT 的知识贡献并非提出全新的推理理论，而在于**将强化学习的决策能力与 LLM 的生成能力进行了解耦和高效结合**，解决了“如何用极小的计算开销实现推理逻辑的自主导航”这一工程问题。

*   **MDP 建模与状态表示**：RLoT 将长序列推理形式化为 MDP。其关键创新在于状态表示：它不直接使用冗长的文本上下文，而是设计了一个**状态自评估模块**，通过提示 LLM 对当前推理步进行七个细粒度维度（如“当前步骤的确定性”、“是否偏离主题”等）的自我评估，输出一个低维状态向量。这为导航器提供了一个简洁、信息丰富的决策依据。
*   **训练信号与参数效率**：RLoT 使用外部**过程奖励模型（PRM, Math-Shepherd）** 提供逐步骤的稠密奖励，而非仅依赖最终答案的稀疏奖励。这使得一个仅有不到 3K 参数的 Dueling MLP 导航器就能被有效训练。该设计在知识库中的定位是：**极低成本的推理策略适配器**。它证明了通过 RL 学习一个微小的策略网络来调度一个冻结的大模型，可以在极低的参数和训练开销下，显著提升推理性能，甚至使 7-8B 模型达到与 72B 模型相当的水平（Table 9）。

### 3. 适用边界与局限性

RLoT 的性能和适用性受限于其设计前提和组件质量，存在明确的边界。

*   **对 PRM 质量的依赖**：RLoT 的训练高度依赖于 PRM 提供的奖励信号。如果 PRM 对中间步骤的评分存在噪声或系统性偏差，会直接误导导航器的策略学习，使其学到次优甚至错误的逻辑选择模式。这是一个上游依赖风险。
*   **状态自评估的准确率瓶颈**：状态自评估模块是导航器决策的基础。论文指出其准确率约为 82%，这意味着有接近 20% 的推理步可能被输入了错误的状态信息，从而导致后续动作选择偏差（Figure 6）。虽然方法对一定程度的噪声具有鲁棒性（Table 14），但该错误率仍是性能上限的一个硬约束。
*   **任务域限制**：当前验证集中在数学、STEM 和常识推理等具有明确客观答案的文本任务上。对于多模态任务、需要调用外部工具或涉及长程对话管理的开放式生成任务，RLoT 的 MDP 建模、状态定义和动作空间是否依然有效，尚未得到验证。
*   **训练数据前提**：RLoT 的训练需要预先筛选出 LLM 无法正确回答的困难问题集。这个前提在标准基准测试中容易满足，但在开放域、实时交互场景下，如何动态定义和获取“困难问题”是一个未解决的挑战。

### 4. 开放问题与未来方向

基于 RLoT 的框架，以下问题值得进一步探索：
1.  **动作空间的丰富性**：当前五种逻辑块是粗粒度的认知操作。能否将其扩展为更丰富的集合，例如加入“假设生成”、“反事实推理”或“类比推理”等模块，以处理更复杂的科学发现或创造性写作任务？
2.  **导航器与 LLM 的深度融合**：目前的导航器通过 Prompt 来控制 LLM，这是一种外部干预。更深度地融合方式，如让导航器直接调整 LLM 的解码 Logits 或控制其注意力头，是否能实现更精细、更高效的推理控制？
3.  **策略的可解释性**：RL 导航器学到的策略是一个黑盒 MLP。如何解释其在不同状态下选择特定逻辑块的原因，并从中提炼出人类可理解的推理启发式，是一个重要的研究方向，有助于增强系统的可信度和可控性。
4.  **规模定律的验证**：实验证明 RLoT 能极大提升小模型的性能，缩小与大模型的差距。但当基座模型本身达到数百亿甚至更大规模时，RLoT 带来的相对增益是否会趋于饱和，还是能持续解锁新的推理能力，这需要进一步的实验验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/RL_of_Thoughts_Navigating_LLM_Reasoning_with_Inference_time_Reinforcement_Learning.pdf]]
