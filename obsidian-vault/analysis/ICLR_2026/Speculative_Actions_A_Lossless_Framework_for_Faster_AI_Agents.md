---
title: "Speculative Actions: A Lossless Framework for Faster AI Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Speculative_Actions_A_Lossless_Framework_for_Faster_AI_Agents.pdf
openreview_forum_id: P0GOk5wslg
aliases:
- SA
- SALFFAA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入一个快速的“推测器”（Speculator）模型，在慢速的“执行器”（Actor）等待时预测未来最可能的k个动作，并提前并行发起后续API调用，一旦预测命中即可立即推进，从而将顺序等待转化为并行预取。"
primary_logic: "代理系统的API调用具有内在的可预测性（命中率可达30%–55%），通过推测执行将慢速API的闲置时间与有用计算重叠，实现在不改变最终行为（无损）的前提下大幅降低端到端延迟。"
claims:
- "在象棋环境中，使用k=3个预测可获得平均54.7%的预测准确率和19.5%的端到端时间节省。"
- "在电商客服场景中，多模型推测器在平均用户打字时间（约30秒）内可实现约34%的API预测准确率，使约三分之一的交互得以即时响应。"
- "在HotpotQA多跳问答中，top-3推测的API调用预测准确率最高可达46%，该任务的主要瓶颈为信息检索延迟。"
- "在有损的OS超参数调优中，联合系统（Actor+Speculator）的p95延迟为37.93ms，远低于纯Actor系统的54.00ms，且收敛时间从约200s缩短至10-15s。"
---

# Speculative Actions: A Lossless Framework for Faster AI Agents

> [!tip] 核心洞察
> 代理系统的API调用具有内在的可预测性（命中率可达30%–55%），通过推测执行将慢速API的闲置时间与有用计算重叠，实现在不改变最终行为（无损）的前提下大幅降低端到端延迟。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 推测行动：一个加速AI代理的无损框架 |
| 英文题名 | Speculative Actions: A Lossless Framework for Faster AI Agents |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=P0GOk5wslg) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Speculative Actions (推测动作执行框架) |
| Dataset | Chess (TextArena环境), E-commerce (-bench retail), HotpotQA (多跳问答) |

> [!tip] 效果简介
> - Chess (TextArena环境) 上，Time saved (%) / Prediction accuracy (%) 为 19.5% (平均时间节省)，对比 0%，变化 +19.5%。
> - Chess (TextArena环境) 上，Prediction accuracy (top-3) 为 54.7%，对比 N/A，变化 54.7%。
> - E-commerce (-bench retail) 上，APIs prediction accuracy 为 22%–38% (单模型), 34% (多模型，在用户打字时间内)，对比 0% (无推测)，变化 +22%–38%。

## 概述

AI代理在交互式环境中执行任务时，每个动作都需要等待慢速API调用（如大语言模型推理、工具调用、甚至人工响应）返回后才能发起下一步操作。这种严格的顺序执行模式导致大量时间消耗在闲置等待上，成为端到端运行时的核心瓶颈。Table 1展示了当前最先进AI代理在不同任务中的估计耗时，直观反映了这一问题的普遍性。

本文提出**推测动作**（Speculative Actions）框架，核心思想是将推测执行从推理层面推广到整个代理环境循环。框架引入两个角色：**Actor**（执行器）是权威但慢速的执行单元，负责产生真实动作应答；**Speculator**（推测器）是快速、低成本的预测模型，在Actor等待期间提前预测未来最可能的$k$个动作，并并行预发起后续API调用。当Actor的真实响应返回后，若命中任一推测分支则直接提交，否则丢弃并按常规执行。通过将顺序等待转化为并行预取，该框架在不改变最终行为的前提下实现**无损加速**。

框架的安全性通过三重机制保障：(a) 语义检查（Actor在提交前确认状态转移的等价性），(b) 安全包络（仅允许幂等、可逆或沙盒化的推测副作用），(c) 修复路径（未命中时回退到常规顺序执行）。

理论分析表明，在指数延迟假设下，$k$分支推测的期望加速比极限为$1 - \frac{p(k)}{1+p(k)} \cdot \frac{\alpha}{\alpha+\beta}$，其中$p(k)=1-(1-p)^k$为至少一个分支命中的概率，$\alpha$和$\beta$分别为Actor和Speculator的延迟率。该比值不超过50%，揭示了推测执行的理论上限。

实验覆盖多个领域：在国际象棋中，$k=3$推测实现平均54.7%的预测准确率和19.5%的端到端时间节省；在电商客服场景中，多模型推测器在用户打字时间内达到约34%的API预测准确率；在HotpotQA多跳问答中，top-3推测准确率最高达46%；在操作系统超参数调优的有损扩展中，联合系统的p95延迟从纯Actor的54.00ms降至37.93ms，收敛时间从约200s缩短至10–15s。

该方法在方法谱系上定位于**推测执行与代理系统的交叉点**：它借鉴了推测解码（Speculative Decoding）中“先预测后验证”的思想，但将其从token级推理推广到完整的API调用与环境交互层面，涵盖了LLM调用、工具API、MCP服务器交互乃至人工响应的全链路加速。

## 背景与动机

AI代理（AI agents）在交互式环境中执行任务时，普遍面临一个核心瓶颈：每个动作都必须等待前一个缓慢的API调用（如大语言模型推理、工具调用、外部服务请求甚至人工响应）完成，才能发起下一个调用。这种严格的顺序执行模式导致大量时间浪费在等待上，成为端到端延迟的主要来源。Table 1展示了当前最先进AI代理在不同任务和环境中的典型耗时，直观地揭示了这一延迟瓶颈的普遍性。

现有加速AI推理的努力主要集中在单模型推理层面，例如推测解码（speculative decoding）利用小型草稿模型预测token序列以实现并行验证。然而，这些方法并未触及代理系统层面更宏观的延迟问题——代理的动作循环中，API调用的等待时间远超过单次推理的延迟。将推测执行的思想从token级别推广到整个代理环境循环，是一个尚未被系统探索的方向。

本文的核心动机在于：代理系统的API调用具有内在的可预测性。实验表明，在象棋、电商客服、多跳问答等多样化场景中，后续API调用的预测命中率可达30%–55%。这意味着，如果能在慢速的权威执行器（Actor）等待响应的同时，利用一个快速、低成本的推测器（Speculator）提前预测未来最可能的k个动作，并并行发起相应的API调用，一旦预测命中即可立即推进，从而将顺序等待转化为并行预取。这一思路旨在实现**无损加速**——在不改变最终行为的前提下，大幅降低端到端延迟。

本文提出的推测动作（Speculative Actions）框架正是基于这一洞察，将推测执行从规划层面推广到整个代理环境，涵盖LLM调用、内部与外部工具API、MCP服务器交互乃至人工响应。框架通过语义守卫、安全包络和修复路径三重机制保证无损性，并重点研究了以宽度推测（k分支并行单步预测）为核心的加速策略。

## 核心创新

### 瓶颈洞察：从顺序等待到并行预取

当前AI代理系统在执行交互式任务时，每个动作都必须等待慢速API调用（如大语言模型推理、工具调用、外部服务响应）返回后才能发起下一个动作。这种严格的串行执行模式使得大量时间消耗在闲置等待上，成为端到端延迟的核心瓶颈。**Speculative Actions** 框架的核心洞察在于：代理系统的API调用具有内在的可预测性——实验表明命中率可达30%–55%——因此可以将这种闲置等待时间与有用的计算重叠，在不改变最终行为的前提下大幅降低延迟。

### 核心机制：推测执行流水线

框架引入两个非对称角色来重构执行流水线：

- **Actor（执行器）**：权威但慢速的执行单元，产生真实的动作应答，其输出是正确性和副作用的唯一依据。
- **Speculator（推测器）**：快速、低成本的预测模型，根据当前状态推测最可能的未来动作及其参数，输出top-k候选。

两者并行运行，构成四个阶段的推测流水线：

1. **预测阶段**：Speculator在当前状态 $s_t$ 下产生 $k$ 个候选动作 $\{\hat{a}_t^{(i)}\}_{i=1}^k$。
2. **并行预启动**：为每个候选动作计算下一状态 $s_{t+1}^{(i)} = f(s_t, \hat{a}_t^{(i)})$，并提前发起相应的API调用，返回future存入缓存。
3. **验证阶段**：等待Actor的真实应答 $a_t$，检查是否命中任一推测分支。
4. **提交或重启**：命中则直接提交该分支并丢弃其余；未命中则按常规顺序执行。

这一流水线的关键性质是**无损性**（losslessness）：最终轨迹与无推测的顺序执行完全一致，但通过并行化获得了时间节省。论文通过语义检查、安全包络和回滚路径三类机制来保证这一点。

### 与基线方法的关键差异

| 执行维度 | 顺序执行基线 | Speculative Actions |
|---------|------------|-------------------|
| **执行流水线** | 每个动作必须等待前一个API调用完成，严格串行 | Actor与Speculator并行运行，Speculator提前产生k个候选并预发起API调用，实现非阻塞推测流水线 |
| **状态推进机制** | 仅当真实响应返回后才计算 $s_{t+1} = f(s_t, a_t)$ | 在等待Actor响应的同时，利用推测应答预计算下一状态并预启动API调用，实现“先跑后验证” |
| **延迟特性** | 端到端延迟为各步延迟之和 | 通过并行预取将闲置时间与计算重叠，理论加速比极限为 $1 - \frac{p(k)}{1+p(k)} \cdot \frac{\alpha}{\alpha+\beta}$ |

### 推测策略的两个维度

框架支持两种互补的推测策略：

- **宽度推测（Breadth Speculation）**：在每个步骤并行推测 $k$ 个候选动作，利用 $p(k) = 1 - (1-p)^k$ 提升命中概率。这是论文实验的主要形式。
- **深度推测（Depth Speculation）**：沿单条路径向前推测多步，适用于动作序列高度可预测的场景。理论分析表明其期望延迟减少比例为 $\frac{T-1}{T} p (1 - \frac{b}{a})$。

此外，框架还引入了**置信度感知的动态选择性推测**，根据模型置信度动态决定每个步骤启动的分支数 $m_t^\star$，在延迟收益与额外成本之间形成帕累托最优权衡。

### 创新边界：与推测解码的差异

与LLM推理中的推测解码（Speculative Decoding）不同，本工作将推测执行从token级别的推理加速推广到**整个代理环境的动作层面**，覆盖LLM调用、内部与外部工具API、MCP-server交互甚至人工响应。这一泛化使得推测执行的应用范围从单一模型推理扩展到多组件、多API的复杂代理系统。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of our framework in a chess-playing environment. While the Actor issues an LLM call to decide the next move, the Speculator uses a faster model to guess it. These guesses enable parallel API calls for the next steps, and once a guess is verified, the system gains time through parallelization. The process runs in the backend, ensuring a lossless speedup for the user*

### 核心瓶颈与设计动机

当前AI代理在交互式环境中执行任务时，每个动作都必须等待慢速API调用（如LLM推理、工具调用、人机交互）返回后才能发起下一个动作。这种严格的**顺序执行**导致大量等待时间，成为端到端运行时的核心瓶颈。表1展示了不同任务/环境中代理的估计耗时，说明该问题的普遍性。

**Speculative Actions**框架的核心洞察在于：代理系统的API调用具有内在的可预测性（命中率可达30%–55%）。通过引入推测执行，将慢速API的闲置时间与有用计算重叠，可以在不改变最终行为（**无损**）的前提下大幅降低端到端延迟。

### 双角色架构

框架将环境交互循环中的角色解耦为两类：

- **Actor（执行器）**：权威但慢速的执行单元，负责产生真实的动作应答。其输出构成正确性和副作用的真实依据。可以是高推理预算的LLM、外部API，甚至是人工响应。
- **Speculator（推测器）**：快速、低成本的预测单元，根据当前状态推测可能的下一动作及其参数，输出top-$k$候选。其作用是在Actor等待期间提前“猜测”未来动作。

### 推测执行流水线

整个流水线由四个阶段组成，如Algorithm 1和图1所示：

1. **预测阶段（Prediction）**：Speculator根据当前状态$s_t$产生$k$个候选动作$\{\hat{a}_t^{(i)}\}_{i=1}^k$。
2. **并行预计算（Parallel Pre-computation）**：对每个推测动作，预计算下一状态$s_{t+1}^{(i)} = f(s_t, \hat{a}_t^{(i)})$，并提前发起相应的API调用$\bar{\hat{a}}_{t+1}^{(i)}$（返回future），存入缓存。
3. **验证阶段（Validation）**：等待Actor的真实应答$a_t$返回，检查是否命中任一推测分支。
4. **提交或重启（Commit or Restart）**：若命中，则提交该分支，丢弃其余；若未命中，则丢弃所有推测结果，按常规顺序执行。

该流水线是**无损的**：最终轨迹与非推测执行完全相同，但通过并行化推理获得了时间节省。

### 形式化建模

代理系统被建模为马尔可夫决策过程（MDP）$(s_t, a_t)$。每个动作被抽象为API调用：策略$\pi$将状态$s_t$映射到目标API $h_t$及其参数$q_t$，即$(h_t, q_t) \leftarrow \pi(s_t)$。异步调用返回future $\bar{a}_t \leftarrow h_t(q_t)$，通过$a_t \leftarrow \text{await}(\bar{a}_t)$取得最终应答。

### 理论保证

在指数延迟假设下，推测执行相对于顺序执行的期望时间比由Proposition 1给出：

$$\frac{E[T_s]}{E[T_{seq}]} = 1 - \frac{1}{T}\frac{\alpha}{\alpha+\beta}\left[\frac{(T-1)p(k)}{1+p(k)} + \frac{p(k)^2}{(1+p(k))^2} - \frac{p(k)^2}{(1+p(k))^2}(-p(k))^{T-1}\right]$$

当$T \to \infty$时，极限为$1 - \frac{p(k)}{1+p(k)} \cdot \frac{\alpha}{\alpha+\beta}$，其中$\alpha$是Actor延迟率，$\beta$是推测器延迟率，$p(k)=1-(1-p)^k$是$k$个独立推测分支中至少有一个正确的概率。该极限不超过50%，说明推测执行的理论加速上限。

### 扩展方向

框架支持两种扩展策略：
- **宽度推测（Breadth Speculation）**：每步并行推测$k$个候选动作，本文主要采用此策略。
- **深度推测（Depth Speculation）**：推测器不仅预测下一步，而是预测$s$步之后，形成多步推测链。此时活跃分支数受限于真实调用与推测调用的相对速度比$a/b$，确保复杂度不随时间跨度$T$增长。

### 无损性保障

为保证推测执行不引入错误副作用，框架设计了多层安全机制：
- **语义检查（Semantic Guards）**：Actor在提交前确认状态转移的等价性。
- **安全包络（Safety Envelopes）**：仅允许幂等、可逆或沙箱化的推测副作用。
- **回滚路径（Repair Paths）**：在非匹配情况下安全丢弃推测结果。

## 核心模块与公式推导

### 执行流水线模块

框架将一次代理交互分解为四个阶段，构成无损推测执行的核心闭环：

1. **预测阶段**：推测器（Speculator）根据当前状态 $s_t$，预测 $k$ 个可能的下一动作 $\{\hat{a}_t^{(i)}\}_{i=1}^k$。
2. **并行计算阶段**：对每个候选动作，预计算下一状态 $s_{t+1}^{(i)} = f(s_t, \hat{a}_t^{(i)})$，并异步发起对应的 API 调用，将返回的 future 存入缓存。
3. **验证阶段**：等待执行器（Actor）的真实应答 $a_t = \text{await}(\bar{a}_t)$，检查是否命中任一推测分支。
4. **提交或重启**：若命中，则提交该推测分支并丢弃其余；若未命中，则丢弃所有推测结果，按常规顺序执行。

该流水线的关键性质是**无损性**：最终轨迹与无推测的串行执行完全一致，但通过并行化推理获得时间节省。这一性质由语义检查、安全包络和回滚路径三重机制共同保障。

### 核心公式

**动作映射与异步调用**。策略 $\pi$ 将状态 $s_t$ 映射到目标 API $h_t$ 及其参数 $q_t$：

$$(h_t, q_t) \leftarrow \pi(s_t)$$

异步调用返回一个 future $\bar{a}_t$，await 操作阻塞直到获取最终应答：

$$\bar{a}_t \leftarrow h_t(q_t), \quad a_t \leftarrow \text{await}(\bar{a}_t)$$

**推测命中概率**。设单次推测正确概率为 $p$，则 $k$ 个独立推测分支中至少有一个命中的概率为：

$$p(k) = 1 - (1-p)^k$$

这是宽度推测加速的理论基础——通过增加并行分支数以指数方式提升命中率。

**期望加速比（宽度推测）**。在指数延迟假设下（Actor 延迟率为 $\alpha$，推测器延迟率为 $\beta$），推测执行与顺序执行的期望时间比满足：

$$\frac{E[T_s]}{E[T_{\text{seq}}]} = 1 - \frac{1}{T}\frac{\alpha}{\alpha+\beta}\left[\frac{(T-1)p(k)}{1+p(k)} + \frac{p(k)^2}{(1+p(k))^2} - \frac{p(k)^2}{(1+p(k))^2}(-p(k))^{T-1}\right]$$

当 $T \to \infty$ 时，极限加速比收敛于：

$$\lim_{T\to\infty} \frac{E[T_s]}{E[T_{\text{seq}}]} = 1 - \frac{p(k)}{1+p(k)} \cdot \frac{\alpha}{\alpha+\beta}$$

该极限值不超过 50%，揭示了宽度推测的理论加速上限取决于命中概率 $p(k)$ 和 Actor 延迟占比 $\frac{\alpha}{\alpha+\beta}$。

**相对成本增加（宽度推测）**。宽度推测的期望相对成本增加有闭式上界：

$$\lim_{T\to\infty} \frac{\mathbb{E}[M_{\text{spec}} - M_{\text{seq}}]}{\mathbb{E}[M_{\text{seq}}]} \leq k - \left(k + \frac{\alpha}{\alpha+\beta}\right)\frac{p(k)}{1+p(k)}$$

该式刻画了并行分支数 $k$ 与命中概率 $p(k)$ 之间的成本权衡。

**置信度感知的选择性推测**。当可获得每条推测的置信度估计时，最优分支选择由以下动态规划给出：

$$m_t^\star(\mathbf{p}) \in \arg\max_{m \in \{0,\dots,k\}} \{q(m; \mathbf{p})\Delta_t - c m\}$$

其中 $q(m; \mathbf{p})$ 为前 $m$ 个分支至少有一个命中的概率，$\Delta_t$ 为命中带来的延迟节省，$c$ 为单分支成本。该策略在延迟节省与额外开销之间实现帕累托最优。

**深度推测的延迟减少**。对于深度推测（沿单条链向前推测多步），期望延迟减少比例为：

$$\frac{\mathbb{E}[T_{\text{seq}} - T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]} = \frac{T-1}{T} p\left(1 - \frac{b}{a}\right)$$

其中 $p$ 为每步推测正确的概率，$a$ 为真实 API 延迟，$b$ 为推测延迟。深度推测的关键约束是系统最多可领先 $\lfloor a/b \rfloor$ 步，确保活跃分支数有界且不随 horizon $T$ 增长。

## 实验与分析

### 核心瓶颈与实验设计逻辑

当前AI代理在交互式环境中的核心瓶颈在于严格的顺序执行模型：每个动作都必须等待缓慢的API调用（如LLM推理、工具调用）返回后才能发起下一个调用，导致大量闲置等待时间（Table 1展示了SOTA代理在不同任务中的耗时估计）。Speculative Actions框架通过引入快速推测器（Speculator）与慢速执行器（Actor）并行工作，将顺序等待转化为并行预取，在不改变最终行为（无损）的前提下降低端到端延迟。实验设计围绕三个维度展开：预测准确率、端到端时间节省、以及成本-延迟权衡。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/001_Table_1.jpg]]
*Table 1: Estimated time state-of-the-art AI agents spend on various tasks/environments*

### 主要实验结果

#### 象棋环境：宽度推测的有效性

在TextArena象棋环境中，系统使用快速Speculator与慢速Actor配对实现Algorithm 1的推测流水线。该流水线包含四个阶段：预测、并行计算、验证、提交或重启，整个过程保证无损——最终轨迹与非推测玩法完全一致，但通过并行化推理节省时间。

**Figure 2**展示了不同预测数量k下的时间节省与预测准确率。使用k=3个预测可获得**平均54.7%的预测准确率**和**平均19.5%的端到端时间节省**。从k=1到k=3，预测准确率和时间节省均呈明显增长趋势，验证了宽度推测（k-way parallel）的收益递增特性。

#### 电商客服场景：多模型推测的优势

在电商零售场景中，Speculator需同时预测用户查询内容和目标API调用及其参数。实验对比了单模型推测器与多模型推测器（如GPT-5-nano + Gemini并行运行，输出聚合为共享候选池）的预测准确率。

**Figure 3**显示，单模型推测器的API预测准确率在22%–38%之间，而多模型配置在平均用户打字时间（约30秒）的阈值下可实现约**34%的预测准确率**。低预算推测模型仅需2–3秒完成推测，远低于用户打字时间，使约三分之一的交互得以即时响应。多模型推测器在准确率上持续优于单模型，验证了推测器多样性的价值。

#### HotpotQA多跳问答：信息检索延迟的缓解

在多跳问答任务HotpotQA中，主要瓶颈为信息检索API的延迟。**Figure 4**展示了以gemini-2.5-flash为Actor时，top-1与top-3推测的API调用预测准确率对比。top-3推测的准确率最高可达**46%**，显著优于top-1，再次验证了宽度推测在多分支场景中的优势。

#### OS超参数调优：有损扩展中的快速响应

在sysbench cpu的OS超参数调优中，系统采用了有损扩展——牺牲严格无损性，依靠最后写入赢（last-writer-wins）机制避免复杂回滚。Speculator每秒根据最新性能指标提出参数更新，Actor每10–15秒分析压缩的历史（测量值，动作）对后做出响应。

**Figure 5（左）**展示了三种系统的收敛曲线对比：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/007_Figure_5.jpg]]
*Figure 5: (Left) Comparison of Speculator-Actor, Speculator-only, and Actor-only convergence. The Speculator shortens time spent exploring poor settings. The Speculator-only agent stabilizes quickly but at a worse final value. (Right) Average p95 latency over a 20-second tuning experiment showing that rapid reaction offers immediate performance benefits (see §B.3.3). Lower is better*

- **Speculator-only**：反应迅速但陷入次优配置
- **Actor-only**：最终收敛到最优配置但需约200秒
- **联合系统（Actor + Speculator）**：兼具快速响应与最优稳态，在**10–15秒内**达到最优设置

**Figure 5（右）**的p95延迟测量进一步量化了响应优势：联合系统的平均p95延迟为**37.93 ms**，显著低于纯Actor系统的**54.00 ms**，也远低于未调优基线的102.97 ms。

**Table 2**和**Figure 9**的成本分析揭示了推测执行的经济性：联合系统在约13秒时收敛，总成本仅**0.17美分**；而Actor-only在约200秒收敛时累计成本达**2.18美分**。虽然推测执行瞬时成本更高，但快速收敛避免了长期资源浪费。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/011_Figure_9.jpg]]
*Figure 9: Cumulative token usage and cost over time. The left and right plots show the cumulative cost (USD) and total tokens used, respectively, for all three configurations. The vertical lines mark the observed convergence point for each system. The Actor-only model converges at 200s*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/012_Table_2.jpg]]
*Table 2: Cumulative tokens and cost (in cents) at selected time marks. While Speculation incurs higher instantaneous costs, its rapid convergence (bolded) prevents long-term resource waste compared to the slower Actor-only baseline. Table 3*

**Figure 7**通过受控扰动实验展示了系统的阶跃响应：在t=0手动注入劣化设置后，Actor-Speculator系统在**一秒内**完成修正，而Actor-only需等待超过10秒的下一个决策周期。


![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/009_Figure_7.jpg]]
*Figure 7: A controlled experiment showing the system’s step response after a manual perturbation at t = 0. The Actor-Speculator system corrects the poor setting within a second, while the Actoronly system must wait over 10 seconds for its next decision cycle. The quantitative results of this experiment are summarized in Figure 5 (Right) in the main text*

### 消融实验分析

1. **推测数量k的影响**：在象棋环境中，从k=1增加到k=3，预测准确率和时间节省均显著提升（Figure 2），验证了宽度推测的收益。
2. **top-1 vs top-3推测**：HotpotQA中top-3准确率（46%）显著优于top-1（Figure 4），说明多分支推测在多跳检索场景的必要性。
3. **单模型 vs 多模型推测器**：电商场景中多模型推测器组合持续优于单一模型（Figure 3），推测器多样性提升预测覆盖。
4. **系统组件消融**：OS调优中，Speculator-only快速但次优，Actor-only慢但最优，联合系统兼得两者优势（Figure 5），验证了双角色架构的必要性。
5. **成本-延迟权衡**：宽度推测和动态选择性推测（基于置信度）形成帕累托前沿（Figure 6）。常数阈值近似策略以最低额外token成本实现显著延迟降低，优于简单固定k=1或k=2的策略。

### 失败模式与局限

1. **副作用不可逆环境**：推测执行要求副作用可逆或隔离（语义检查、安全包络、回滚路径），在支付、删除等不可逆动作的真实系统中尚无法保证安全。
2. **多步推测缺乏实证**：当前实验主要使用单步宽度推测（k-way parallel），多步深度推测和自适应推测仅在理论分析中讨论（Section 5.3, Appendix C.4），缺乏全面实证验证。
3. **API延迟的随机性**：实时API负载波动导致延迟测量存在难以复现的方差，作者明确说明了这种随机性。
4. **收敛后的冗余开销**：在OS有损扩展中，系统收敛后可能仍存在不必要的推测开销，尚未完全优化。
5. **理论假设的局限**：成本-延迟理论分析基于指数延迟假设（Proposition 1），实际环境可能不符合该假设，理论加速比极限不超过50%。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_P0GOk5wslg/figures/010_Figure_8.jpg]]
*Figure 8: Prediction Accuracy against Speculator’s Cost across different models. (a) Accuracy–Speculator time cost trade-off across models. The dashed line shows average user typing time. (d) Accuracy–Speculator price trade-off across models, reflecting the monetary cost of speculative execution*

## 方法谱系与知识库定位

### 1. 与已有工作的关系

**Speculative Actions** 框架的核心思想——用轻量模型预测未来步骤并提前执行，以重叠计算与等待——在计算机体系结构和自然语言生成领域均有先例，但本工作将其系统性地推广到了**通用AI代理的完整交互循环**中。

**体系结构领域的推测执行**：现代CPU中的分支预测与推测执行是直接的灵感来源。CPU在遇到条件分支时，预测最可能的路径并提前执行，若预测正确则获得加速，否则回滚。Speculative Actions 将这一思想映射到代理系统：Actor 相当于慢速的“主执行单元”，Speculator 相当于“分支预测器”，API调用相当于“长延迟指令”，验证与提交机制相当于“退休（retirement）”阶段。关键区别在于，代理系统的“指令”（API调用）延迟可达秒级甚至分钟级，远高于CPU的纳秒级，因此推测命中带来的绝对收益更为显著。

**推测解码（Speculative Decoding）**：在LLM推理层面，推测解码使用小模型生成多个候选token，再由大模型并行验证，已成为成熟的加速技术。Speculative Actions 与推测解码共享“小模型预测、大模型验证”的范式，但将其从**token级**提升至**动作级**：推测的对象不再是单个token，而是完整的API调用（包括目标函数及其参数）。论文明确将这一区别作为核心贡献：*"we generalize speculation beyond planning to the entire agentic environment, including LLM calls, internal and external tool APIs, MCP-server interactions, and even human responses"*（Section 1.1）。

**与规划领域的关系**：在AI规划中，前瞻搜索（lookahead search）和蒙特卡洛树搜索等方法也会预演未来状态。但Speculative Actions 的关键差异在于：(1) 推测不仅限于规划推理，而是覆盖所有阻塞式API调用；(2) 推测结果通过**实际发起API调用并获取真实响应**来验证，而非仅依赖模拟或启发式评估；(3) 框架设计了语义守卫、安全包络和修复路径三种机制来保证无损性，这在传统规划中通常不是首要约束。

**基线对比**：论文的直接基线是**顺序执行（Sequential execution）**——每个动作必须等待前一API调用完成后才能发起下一个。在消融实验中，还引入了**Actor-only**（仅慢速执行器，无推测器）作为对照，以分离推测器带来的增益。这些基线均未引入任何推测机制，代表了当前主流代理系统的运行方式。

### 2. 适用边界与关键假设

Speculative Actions 的有效性依赖于以下核心假设，这些假设同时定义了方法的适用边界：

**假设1：API延迟显著高于推测延迟**。推测执行的时间节省来源于 $p(k) \cdot \frac{\alpha}{\alpha+\beta}$ 项（见 Proposition 1），其中 $\alpha$ 为 Actor 延迟率，$\beta$ 为推测器延迟率。当 $\alpha \gg \beta$ 时，理论加速上限接近 $\frac{p(k)}{1+p(k)}$（不超过50%）。若 API 调用本身极快（如本地函数调用），推测开销可能抵消收益。论文在电商场景中验证了这一假设：低预算推测模型仅需2-3秒完成预测，而用户平均打字时间约30秒，推测开销远低于等待时间。

**假设2：动作具有可预测性**。框架要求代理的行为序列存在规律性，使得轻量模型能够以非平凡概率预测真实动作。实验表明，在国际象棋中 top-3 预测准确率达54.7%，HotpotQA 中达46%，电商场景中达22%–38%。若环境完全随机或代理行为无模式可循，推测命中率趋近于零，框架退化为纯开销。

**假设3：副作用可逆或可隔离**。这是保证**无损性**的核心前提。论文提出了三层保障机制：(a) **语义守卫**——Actor 在提交前确认状态转换的等价性；(b) **安全包络**——仅允许幂等、可逆或沙盒化的推测副作用；(c) **修复路径**——在检测到不一致时回滚状态。这意味着框架不适用于包含不可逆操作（如支付、删除、发送）且缺乏沙盒隔离的环境。在OS超参数调优的有损扩展中，论文明确放弃了严格无损性，转而采用“最后写入赢”的简化策略。

**假设4：并行API调用无冲突**。k路并行推测会同时发起多个API调用，要求这些调用之间不存在资源竞争或互斥约束。在高并发场景下，API提供方的速率限制（rate limit）可能抵消并行带来的收益。

### 3. 局限性与已知失效模式

**副作用安全性的根本限制**：尽管论文设计了多层安全机制，但推测执行在本质上仍无法完全消除错误推测带来的外部影响。当前方法依赖环境的配合（沙盒、快照、幂等性），在开放、不可控的生产环境中，这一假设可能不成立。论文将此列为明确局限：*"推测执行要求副作用可逆或隔离，否则可能导致不可接受的外部影响"*。

**推测深度与广度的实证覆盖不足**：当前实验主要验证了**单步宽度推测**（k-way parallel at each step），而多步深度推测和自适应选择性推测主要在理论层面进行了分析（Section 5.2–5.3）。深度推测的延迟减少比例为 $\frac{T-1}{T} p (1 - \frac{b}{a})$，但其在实际复杂环境中的加速效果和级联错误放大效应缺乏系统实证。

**实时延迟的测量方差**：API调用的端到端延迟受网络波动、服务端负载等内生随机性影响，导致延迟测量存在难以复现的方差。论文承认了这一局限，但未提供方差量化或统计显著性检验。

**有损模式下的持续开销**：在OS超参数调优中，系统收敛后推测器仍可能继续发起不必要的推测调用，产生浪费。论文未对收敛后的推测策略进行优化（如自适应降低推测频率）。

**理论分析的分布假设**：Proposition 1 的期望加速比推导基于指数延迟假设，实际API延迟分布可能呈现长尾、突发等特征，理论界限的适用性需要进一步验证。

### 4. 开放问题

**安全性泛化**：如何将推测执行扩展到包含不可逆动作的真实系统（如金融交易、医疗决策），同时保证安全性和经济性？可能的路径包括：形式化验证推测动作的安全性、引入人工确认节点、或设计细粒度的补偿事务机制。

**全栈推测优化**：当前工作聚焦于代理层面的动作推测，与LLM推理层面的推测解码相互独立。是否可以将两者无缝结合——即底层使用推测解码加速单次LLM调用，上层使用推测动作加速代理循环——构成全栈推测优化？这需要解决两层推测之间的协调和资源分配问题。

**推测器训练与自适应**：当前推测器主要依赖现成的轻量模型，未针对特定代理任务进行微调。是否可以通过在线学习或蒸馏，持续提升推测器对特定代理行为模式的预测准确率？自适应推测（Section 5.2）的理论框架为此提供了基础，但缺乏大规模实证验证。

**大规模并发下的成本效益**：在多租户、高并发的生产环境中，k路并行推测的API调用量呈倍数增长。API提供方的速率限制和计费模式可能使得推测执行的经济性发生质变。需要建立更贴近生产环境的成本模型。

**多代理协同推测**：当前框架假设单个Actor-Speculator对。在多代理系统中，代理之间的交互可能提供额外的可预测性信号，是否可以利用跨代理的上下文信息提升推测准确率？

## 原文 PDF

![[paperPDFs/ICLR_2026/Speculative_Actions_A_Lossless_Framework_for_Faster_AI_Agents.pdf]]
