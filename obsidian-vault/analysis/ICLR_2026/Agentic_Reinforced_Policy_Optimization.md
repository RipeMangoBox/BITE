---
title: "Agentic Reinforced Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agentic_Reinforced_Policy_Optimization.pdf
aliases:
- ARPOA
- ARPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "ARPO在工具调用后的高熵token位置触发分支采样，并用优势归因训练多轮工具调用LLM智能体。"
primary_logic: "熵变化决定局部分支展开，分支与共享token再分别获得优势信号以优化工具使用轨迹。"
claims:
- "工具调用后token熵上升暴露了轨迹级RL缺少步骤级探索的问题。"
- "自适应分支采样以更少工具调用预算覆盖关键高不确定性决策。"
- "软优势归因和分层奖励使ARPO在推理与深度搜索任务上优于GRPO等轨迹级基线。"
---

# Agentic Reinforced Policy Optimization

> [!tip] 核心洞察
> 通过监测工具调用后token熵的变化，自适应地在高熵决策点进行分支采样，结合优势归因估计，使LLM能够内化步骤级工具使用行为的优势差异，从而以更少的工具调用预算实现更优性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 智能体强化策略优化 |
| 英文题名 | Agentic Reinforced Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=TX4k7BF6aO); [GitHub](https://github.com/RUC-NLPIR/ARPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Agentic Reinforced Policy Optimization (ARPO) |
| Dataset | 10个推理任务平均, AIME24, AIME25, HLE |

> [!tip] 效果简介
> - 10个推理任务平均 上，准确率 为 55.3 (Llama3.1-8B), 58.3 (Qwen2.5-7B)，对比 GRPO: 51.1 (Llama), 56.5 (Qwen)，变化 +4.2 (Llama), +1.8 (Qwen)。
> - AIME24 上，准确率 为 30.0 (Qwen2.5-7B)，对比 GRPO: 23.3，变化 +6.7。
> - AIME25 上，准确率 为 30.0 (Qwen2.5-7B)，对比 GRPO: 26.7，变化 +3.3。

## 概述

本文提出**智能体强化策略优化** (Agentic Reinforced Policy Optimization, ARPO)，一种专为训练多轮工具调用LLM智能体设计的强化学习算法。ARPO的核心创新在于：通过监测工具调用后token熵的变化，自适应地在高熵决策点进行分支采样，并结合优势归因估计，使LLM能够内化步骤级工具使用行为的优势差异。实验表明，ARPO在10个推理任务上的平均准确率（Llama3.1-8B: 55.3, Qwen2.5-7B: 58.3）优于最佳基线GRPO（51.1, 56.5），且在GAIA和WebwalkerQA上比GRPO提升6%，同时仅使用一半的工具调用预算。

## 背景与动机

当前基于轨迹级别的强化学习算法（如GRPO、DAPO）在训练多轮工具调用的LLM智能体时，存在两个关键瓶颈：

1. **工具调用后高熵步骤的细粒度探索不足**：如Figure 2所示，工具调用后前10-50个token的熵急剧上升，表明外部工具反馈显著增加了LLM推理的不确定性。然而，轨迹级RL算法对整个轨迹进行完整采样，不区分步骤，导致工具使用行为多样性不足。

2. **工具调用预算效率低下**：轨迹级RL需要大量工具调用才能获得有效学习信号，而ARPO通过自适应分支采样，以更少的工具调用预算实现更优性能（Figure 1右图）。

## 核心创新

ARPO的核心洞察是：通过监测工具调用后token熵的变化，自适应地在高熵决策点进行分支采样，结合优势归因估计，使LLM能够内化步骤级工具使用行为的优势差异，从而以更少的工具调用预算实现更优性能。

| 组件 | 基线值 | 提出值 | 证据锚点 |
|------|--------|--------|----------|
| 展开策略 | 轨迹级采样：对整个轨迹进行完整采样，不区分步骤 | 熵基自适应展开：在工具调用后的高熵步骤触发分支采样，生成部分推理路径 | Section 3.1 |
| 优势估计 | 组级优势（GRPO）：同一组内所有token共享平均优势 | 优势归因估计：共享token段分配平均优势，分支路径token分配独立优势（硬/软两种设置） | Section 3.2 |
| 计算复杂度 | O(n²)（轨迹级RL） | 介于O(n log n)和O(n²)之间 | Section 3.1 |

## 整体框架

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/001_Figure_1.jpg]]

ARPO的整体框架如Figure 3所示，包含三个核心模块：

1. **熵基自适应展开** (Entropy-based Adaptive Rollout)：在展开阶段，根据工具调用后的熵变化自适应地触发分支采样，平衡全局和步骤级探索。

2. **优势归因估计** (Advantage Attribution Estimation)：对共享和分支token段分配不同优势值，使模型内化步骤级工具使用行为的差异。

3. **分层奖励设计** (Hierarchical Reward Design)：结合正确性、格式和多工具协作奖励，引导模型行为。

Figure 4展示了ARPO的两个核心组件：左图展示熵基自适应展开如何动态扩展采样，右图展示优势归因如何为组间推理路径中的token分配共享或独立值。

## 核心模块与公式推导

### 5.1 Token熵计算

Token级生成熵的计算公式为：

$$H_t = -\sum_{j=1}^V p_{t,j} \log p_{t,j}, \quad \mathrm{where} \quad p_t = \pi_\theta(\cdot \mid \mathcal{R}_{<t}, x; T) = \mathrm{Softmax}\left(\frac{z_t}{\tau}\right)$$

该公式计算步骤t的token级生成熵，反映token生成分布的不确定性。如Figure 2所示，工具调用后前10-50个token的熵急剧上升，表明外部工具反馈显著增加了LLM推理的不确定性。

### 5.2 熵基自适应展开

基于熵变化ΔH_t定义步骤t的分支概率：

$$P_t = \alpha + \beta \cdot \Delta H_t, \quad \mathrm{Action}(P_t) = \left\{ \mathrm{Branch}(Z), \quad \mathrm{if} \quad P_t > \tau; \right.$$

其中α为基础采样概率，β为稳定性熵。当P_t超过阈值τ时，触发Branch(Z)生成Z条部分推理路径。ARPO通过此机制将每次展开的计算复杂度从轨迹级RL的O(n²)降低到介于O(n log n)和O(n²)之间。

### 5.3 优势归因估计

ARPO探索了两种优势估计设置：

**硬优势估计**：对独立token使用归一化奖励计算优势：

$$\tilde{\hat{A}}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^{\tilde{G}})}{\mathrm{std}(\{R_i\}_{i=1}^{G})}$$

对共享token段，跨d条轨迹取平均优势：

$$\hat{A}_{i,t}^{\mathrm{shared}} = \frac{1}{d} \sum_{i=1}^{d} \hat{A}_{i,t}$$

**软优势估计**：基于GRPO目标函数，共享前缀token在不同轨迹中具有相同的重要性权重：

$$J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(q,a)\sim D, \{y_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot|q)} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|y_i|} \sum_{t=1}^{|y_i|} \min\left( r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t} \right) - \beta D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}}) \right]$$

其中重要性采样比为：

$$r_{i,t}(\theta) = \frac{\pi_\theta(y_{i,t} \mid x, y_{i,<t})}{\pi_{\mathrm{old}}(y_{i,t} \mid x, y_{i,<t})}$$

共享token条件为：

$$r_{i,t}(\theta) = r_{j,t}(\theta), \quad \mathrm{if} \ y_{i,<t} = y_{j,<t} \ (\mathrm{i.e., shared\ tokens})$$

如Figure 5所示，软优势估计在训练过程中产生更稳定的奖励，因此ARPO默认采用软优势估计。

### 5.4 分层奖励设计

奖励函数结合准确率、格式正确性和多工具使用奖励：

$$R = \left\{ \begin{array}{ll} \max(\mathrm{Acc.} + r_{\mathrm{M}}, \mathrm{Acc.}) & \mathrm{If\ Format\ is\ Good\ \&\ Acc. > 0;} \\ 0 & \mathrm{If\ Format\ is\ Good\ \&\ Acc. = 0;} \\ -1 & \mathrm{Otherwise.} \end{array} \right. \quad r_{\mathrm{M}} = \left\{ \begin{array}{ll} 0.1 & \mathrm{If\ \exists([<search>]\&[<python>]);} \\ 0 & \mathrm{Otherwise.} \end{array} \right.$$

### 5.5 广义策略梯度定理

ARPO的理论基础是广义策略梯度定理，使用宏动作（部分展开段）对Transformer策略进行策略梯度优化：

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \{ \sum_{T=1}^K [ \nabla_\theta \log \pi_\theta(MA_T | MS_T) A_T(\tau) ] \}$$

该定理断言，对于任何可微的基于Transformer的策略π_θ和任何目标函数J(θ)，可以使用宏动作有效进行优化。ARPO是该定理的高级实现。

## 实验与分析

### 6.1 主要结果

**推理任务**：Table 1展示了在10个挑战性推理任务上的整体性能。ARPO在Llama3.1-8B和Qwen2.5-7B上均优于所有轨迹级RL基线。


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/010_Table_1.jpg]]
*Table 1: Overall performances on 10 challenging reasoning tasks are presented. The top two outcomes are bolded and underlined. Dataset abbreviations are as follows: WebW (WebWalker), HQA (HotpotQA), 2Wiki. (2wikiMultiHopQA), MuSi. (MuSiQue), and Bamb (Bamboogle).*

| 基准 | 指标 | ARPO | GRPO (最佳基线) | 提升 |
|------|------|------|-----------------|------|
| 10个推理任务平均 | 准确率 | 55.3 (Llama3.1-8B), 58.3 (Qwen2.5-7B) | 51.1 (Llama), 56.5 (Qwen) | +4.2 (Llama), +1.8 (Qwen) |
| AIME24 | 准确率 | 30.0 (Qwen2.5-7B) | 23.3 | +6.7 |
| AIME25 | 准确率 | 30.0 (Qwen2.5-7B) | 26.7 | +3.3 |

**深度搜索任务**：Table 2展示了在深度搜索任务上的整体性能。ARPO在GAIA和WebwalkerQA上比GRPO提升6%，且仅使用一半的工具调用预算。


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/011_Table_2.jpg]]
*Table 2: Overall performance on various deep search tasks, with accuracy results for each dataset obtained using llm-as-judge. The best results are indicated in bold, and the second-best results are underlined. Results from larger or closed-source models are presented in gray for reference.*

| 基准 | 指标 | ARPO | GRPO | 提升 |
|------|------|------|------|------|
| GAIA | pass@1 | 43.2 (Qwen3-14B, 1K样本) | - | +6% |
| General AI Assistant (Qwen3-8B) | 平均准确率 | 38.8 | 32.0 | +6.8 |
| General AI Assistant (Qwen3-14B) | 平均准确率 | 43.7 | 36.9 | +6.8 |
| XBench (Qwen3-14B) | 平均准确率 | 32.0 | 27.0 | +5.0 |

### 6.2 消融研究

**浏览器智能体骨干模型**：Table 3显示，无浏览器智能体时深度搜索性能最差；使用更大浏览器智能体时性能显著提升。


![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/018_Table_3.jpg]]
*Table 3: Ablation studies of the backbone model of browser agents in deep search tasks.*

**超参数缩放分析**：Figure 8展示了ARPO超参数的缩放分析：
- 熵值缩放：性能在熵值0.4时达到峰值，在1.0时下降
- 初始采样大小缩放：性能在N=8时达到峰值，在N=16时下降
- 全局展开大小缩放：性能随M增大而提升

**优势估计方法**：Figure 5显示，软优势估计在训练过程中产生更稳定的奖励。

### 6.3 工具调用效率与展开多样性

Figure 7比较了GRPO和ARPO：
- (a) 工具调用效率：ARPO在实现更高整体准确率的同时，仅使用GRPO一半的工具调用次数
- (b) 展开多样性：ARPO的采样轨迹形成更多不同的聚类中心（54个聚类）相比GRPO（48个聚类）

Figure 6展示了Qwen3-8B和Qwen3-14B使用ARPO在Pass@1到Pass@5指标上的扩展分析。Qwen-14B在GAIA上达到Pass@5性能61.2%，在HLE上达到24.0%，在xBench-DR上达到59.0%。

### 6.4 公平性说明

- 所有实验均使用相同的冷启动SFT数据集（Tool-Star的54K样本 + STILL的0.8K样本）和RL训练数据（Tool-Star的10K样本用于推理任务，1K混合硬搜索样本用于深度搜索任务）
- 基线方法（GRPO、DAPO、REINFORCE++）均使用其官方或广泛采用的实现，并在相同计算资源（8或16块NVIDIA H800 GPU）下训练
- 对于深度搜索任务，仅使用1K RL样本，以展示ARPO在数据效率上的优势

### 补充图表

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/022_Table_7.jpg]]
*Table 7: An example from ARPO on HLE dataset, with special symbols used in think content, search queries, Python codes, returned results and final answer highlighted with purple box , green box blue box and red box , respectively.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_TX4k7BF6aO_Agentic_Reinforced_Polic/figures/002_Figure_1.jpg]]
*Figure 1: Overview of tool-use token entropy exploration and ARPO algorithm performance. Left: High entropy observed in the LLM following tool usage. Right: LLM performance comparison on deep search tasks using only 1k RL samples, along with a comparison of training tool-use budgets.*


## 方法谱系与知识库定位

ARPO属于**智能体强化学习** (Agentic Reinforcement Learning) 领域，该领域专注于使用RL训练LLM智能体进行多轮工具交互。与轨迹级RL算法（如GRPO、DAPO、REINFORCE++）不同，ARPO通过熵基自适应展开实现步骤级探索，解决了工具调用后高熵步骤的细粒度探索问题。

ARPO的理论基础是**广义策略梯度定理** (Generalized Policy Gradient Theorem)，该定理将传统策略梯度定理扩展到基于Transformer的策略，允许使用宏动作（部分展开段）进行优化。ARPO是该定理的高级实现。

与相关工作的关系：
- **RLVR (Reinforcement Learning with Verifiable Rewards)**：如OpenAI o1、DeepSeek-R1等，主要关注单轮推理任务，而ARPO针对多轮工具调用场景
- **段级RL目标**：如Guo et al. (2025) 的工作，ARPO的优势归因估计提供了更细粒度的信用分配
- **工具集成RL**：如ToolRL、ToRL等，ARPO通过熵基自适应展开提高了工具调用效率

**局限性**：
- 论文未明确报告所有13个基准测试的完整结果，部分结果仅以平均或相对提升形式呈现
- 超参数（α, β, τ, Z, M, N）的具体值仅在附录中部分给出，且缺乏敏感性分析
- 软优势估计的理论优势（正则化效应）仅作为假设提出，缺乏严格的数学证明
- 实验仅在Llama和Qwen系列模型上进行，未验证在其他架构（如Mistral、Gemma）上的泛化性
- 深度搜索任务仅使用1K训练样本，可能无法充分代表真实世界场景的复杂性

**开放问题**：
- ARPO的熵基自适应展开机制是否能在更广泛的工具集（如数据库查询、API调用）上保持有效性？
- 硬优势估计与软优势估计之间的理论联系能否进一步形式化？
- ARPO在更大规模模型（如70B+）上的扩展性如何？
- 分支数量Z和阈值τ的最优选择是否依赖于具体任务？是否存在自适应调整策略？
- ARPO能否与过程奖励模型（PRM）结合，以提供更细粒度的步骤级反馈？

## 原文 PDF

![[paperPDFs/ICLR_2026/Agentic_Reinforced_Policy_Optimization.pdf]]
