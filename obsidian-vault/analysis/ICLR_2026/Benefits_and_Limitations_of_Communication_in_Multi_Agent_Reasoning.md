---
title: "Benefits and Limitations of Communication in Multi-Agent Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Benefits_and_Limitations_of_Communication_in_Multi_Agent_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: 0aPIVJUz5T
aliases:
- BLCMAR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "控制多智能体系统中的智能体数量(w)和通信预算(communication budget)，可以在计算深度（墙钟时间）和总体通信代价之间实现平衡。"
primary_logic: "通过形式化多智能体推理，证明存在三种不同体制：1) 关联回忆等任务可在恒定通信和深度下处理更大上下文；2) 状态跟踪等任务可通过增加智能体减少深度，但通信代价相应增加；3) 多跳推理等任务无法通过添加智能体减少深度，且通信成本高昂。这揭示了多智能体系统中深度与通信之间不可消除的折衷。"
claims:
- "提出了一个基于Transformer表达性理论的多智能体系统形式化框架。"
- "多智能体推理中深度的减少只有通过增加通信才能实现。"
- "关联回忆任务可以通过O(1)的深度和O(1)的通信解决，与智能体数量无关。"
- "在PARITY实验中，前缀和协议在序列长度增长时显著优于多数投票法。"
---

# Benefits and Limitations of Communication in Multi-Agent Reasoning

> [!tip] 核心洞察
> 通过形式化多智能体推理，证明存在三种不同体制：1) 关联回忆等任务可在恒定通信和深度下处理更大上下文；2) 状态跟踪等任务可通过增加智能体减少深度，但通信代价相应增加；3) 多跳推理等任务无法通过添加智能体减少深度，且通信成本高昂。这揭示了多智能体系统中深度与通信之间不可消除的折衷。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多智能体推理中通信的益处与局限 |
| 英文题名 | Benefits and Limitations of Communication in Multi-Agent Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0aPIVJUz5T) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Optimal Communication Protocols for Associative Recall, State Tracking (Prefix Sum), and k-hop Reasoning (Iterative Query) |
| Dataset | Needle-in-a-Haystack (associative recall), PARITY (state tracking), k-hop reasoning (100/500 facts) |

> [!tip] 效果简介
> - Needle-in-a-Haystack (associative recall) 上，Accuracy 为 CoA maintains ~1.0 accuracy across all context lengths，对比 Majority Voting degrades to low accuracy at extremes of context length and depth，变化 CoA avoids degradation, majority voting fails at long contexts。
> - PARITY (state tracking) 上，Accuracy 为 Prefix Sum accuracy remains high (~0.8 at max length)，对比 Majority Voting and CoA accuracy degrade as sequence length increases，变化 Prefix Sum consistently outperforms, especially at larger N。
> - k-hop reasoning (100/500 facts) 上，Accuracy 为 Iterative Query accuracy stays >0.90 at 20 hops (500 facts)，对比 Majority Voting accuracy drops to ~0.30 at 20 hops (500 facts)，变化 +0.60 at 20 hops。

## 概要

### 问题背景

大语言模型（LLM）在复杂推理任务中面临一个根本性瓶颈：随着问题复杂度和上下文长度的增加，单智能体Transformer的推理性能显著下降。尽管多智能体协作系统在实践中被广泛采用——通过让多个LLM实例分工合作来应对长上下文或复杂推理——但这类系统在计算深度（墙钟时间）与通信代价之间的基本折衷关系，长期缺乏严格的理论理解。现有方法如**多数投票法**（Majority Voting / Self-consistency, Wang et al., 2022）和**链式代理**（Chain-of-Agent / CoA, Zhang et al., 2024b）虽已展现出经验性优势，但其成功条件和内在局限仍未被系统刻画。

### 核心贡献

本文提出了一个基于Transformer表达性理论的多智能体系统形式化框架，首次从理论上揭示了多智能体推理中深度与通信之间不可消除的折衷关系。核心发现可概括为三种截然不同的推理体制：

1. **关联回忆（Associative Recall）**：此类任务可在恒定深度和恒定通信下处理更大的上下文，无需随着问题规模增长而增加计算或通信资源。
2. **状态跟踪（State Tracking）**：通过增加智能体数量可以减少计算深度，但通信代价会相应增加——深度减少的收益以通信开销为代价。
3. **多跳推理（k-hop Reasoning）**：无法通过添加智能体来减少计算深度，且通信成本随跳数线性增长，揭示了多智能体系统的根本性局限。

这一分类体系（总结于Table 1）为理解和设计多智能体系统提供了理论指南：并非所有任务都能从“增加智能体”中获益，而获益的任务也必然付出通信代价。

### 方法定位

本研究的方法论特色在于**理论先行、实验验证**的双轨路径：

- **理论层面**：以唯一硬注意力Transformer（UHAT）为计算模型，将多智能体系统形式化为有向无环图，其中节点表示智能体状态，边表示思维链（CoT）令牌或智能体间通信。在此框架下，针对三类算法任务族推导了计算规模（Size）、深度（Depth）和通信量（Communication）的紧确上下界。
- **实验层面**：在Llama-3.3-70B和Llama-3.1-8B等真实LLM上，通过构造性任务（Needle-in-a-Haystack、PARITY、k-hop推理）验证了理论预测的深度-通信折衷关系。实验采用硬编码的最优通信协议（前缀和协议、迭代查询协议等），并与多数投票法和链式代理等基线进行严格对比。

该方法谱系定位于**多智能体推理的理论基础**与**Transformer表达性分析**的交叉地带，区别于纯经验性的多智能体框架研究，也不同于仅关注单智能体Transformer能力边界的理论工作。

### 主要结果概览

| 任务类型 | 计算规模 | 计算深度 | 通信量 | 能否通过增加智能体减少深度？ |
|---------|---------|---------|--------|---------------------------|
| 关联回忆 | $\Theta(N)$ | $\Theta(1)$ | $\Theta(1)$ | 否（已最优） |
| 状态跟踪 | $\Theta(N)$ | $\Theta(N/w + \log w)$ | $\Theta(w)$ | 是，但需增加通信 |
| k-hop推理 | $\Theta(k)$ | $\Theta(k)$ | $\Theta(k)$ | 否 |

实验验证与理论高度一致：在PARITY任务中，前缀和协议在序列长度增长时显著优于多数投票法（Figure 4a）；在k-hop推理中，迭代查询协议在跳数增加时保持>0.90的准确率，而多数投票法降至约0.30（Figure 5b）。同时，计算深度与通信量之间的折衷曲线（Figure 4b）精确复现了理论预测的 $N/w(N)$ 与 $w(N)$ 关系。

### 局限与开放问题

当前理论分析基于UHAT模型假设，向实际软注意力Transformer的精确映射仍有待完善。实验局限于少数LLM和构造性任务，在更广泛的推理场景（如图可达性、约束满足）中的泛化性尚未建立。关键开放问题包括：如何将理论上的最优协议转化为可端到端学习的多智能体系统；在近似准确而非精确计算的要求下，投票方法的性能下界能否进一步放松；以及多令牌消息场景下通信预算的精确边界如何刻画。



### 单智能体推理的规模化瓶颈

大语言模型（LLM）在复杂推理任务上展现出了令人瞩目的能力，但其性能随着问题规模和上下文长度的增长而显著退化。这一瓶颈的根源在于Transformer架构的固有表达性限制：单智能体系统必须在固定的计算深度内处理全部输入，当输入长度 $N$ 增大时，所需的序列化计算步骤（即“墙钟时间”）呈超线性增长。更关键的是，**随着上下文长度增加，单智能体Transformer的推理准确率会系统性下降**——这一现象在长文档问答、多跳推理等任务中已被广泛观察到，但缺乏严格的理论解释。

### 多智能体系统的直觉与理论空白

为应对上述瓶颈，研究者提出了多智能体协作方案：将输入分发给多个智能体并行处理，通过智能体间的通信来整合局部推理结果。直觉上，增加智能体数量 $w$ 似乎能够减少每个智能体所需的计算深度，从而加速推理。这一思路催生了诸多经验性方法，如**多数投票（Majority Voting / Self-consistency）**（Wang et al., 2022）和**链式代理（Chain-of-Agent, CoA）**（Zhang et al., 2024b），它们在特定任务上取得了初步成效。

然而，**多智能体推理中深度与通信之间的基本折衷缺乏理论理解**。具体而言，以下核心问题悬而未决：
- 增加智能体数量是否总能减少计算深度？是否存在不可逾越的下界？
- 智能体间的通信代价如何随任务复杂度和智能体数量变化？
- 不同推理任务（如关联回忆、状态跟踪、组合推理）是否呈现根本不同的折衷模式？

### 本文动机：从形式化到可预测的设计原则

本文旨在填补上述理论空白，通过建立一个基于Transformer表达性理论的多智能体推理形式化框架，系统性地回答三个问题：

1. **任务可并行性分类**：不同推理任务在“深度-通信”平面上存在哪些体制？是否存在无法通过增加智能体来加速的任务？
2. **最优协议设计**：对于每类任务，能够同时最小化计算深度和通信代价的最优通信协议是什么？
3. **理论与实证的一致性**：理论预测的折衷关系能否在实际LLM（如Llama-3.3-70B）的实验中复现？

论文的核心洞察在于：**深度的减少只有通过增加通信才能实现**，且这种折衷在不同任务族中呈现质的差异——某些任务（如关联回忆）几乎不需要通信即可并行化，而另一些任务（如多跳推理）的深度下界与智能体数量无关，通信成本高昂且不可避免。这一发现为多智能体系统的设计提供了可预测的指导原则，而非依赖经验试错。



## 核心方法与创新机理

本工作首次从**Transformer表达性理论**出发，对多智能体推理系统进行了严格的形式化分析，揭示了其根本性的**深度-通信折衷（depth-communication tradeoff）**。核心创新在于：不再将多智能体系统视为启发式工程实践，而是将其建模为可证明边界的计算协议，从而精确刻画了“何时多智能体有效”“何时无效”以及“代价是什么”。

### 形式化框架：从经验协议到可证明协议

此前多智能体系统的研究（如 **Majority Voting** (Wang et al., 2022)、**Chain-of-Agent (CoA)** (Zhang et al., 2024b)）缺乏对智能体数量、通信量和计算深度之间关系的理论理解。本工作提出了一套基于**UHAT（Unique Hard Attention Transformer）**的形式化框架，将多智能体系统定义为有向无环图：节点表示智能体在特定时间步的状态，边表示思维链（CoT）令牌的生成或智能体间的通信消息。该框架使得对通信预算、计算规模和墙钟时间（深度）的定量分析成为可能。

### 关键创新点：任务特化的最优协议与可证明边界

本工作针对三类代表性推理任务，分别设计了**具有可证明最优性（或紧界）的通信协议**，并由此揭示了三种截然不同的多智能体体制：

| 创新维度 | Baseline 做法 | 本工作做法 | 理论保证 |
|----------|-------------|----------|--------|
| **关联回忆的通信模式** | 无通信（单智能体）或独立多数投票 | 输入分块后，仅持有查询的智能体与管理者通信一次 | 深度 $O(1)$，通信 $O(1)$，与输入长度 $N$ 和智能体数 $w$ 无关 |
| **状态跟踪的计算深度** | 单智能体需 $O(N)$ 深度 | 基于**前缀和（Prefix Sum）** 的并行扫描协议，智能体分层组合局部结果 | 深度上界 $\mathcal{O}(\log w + N/w)$，下界 $\Omega(N/w)$，证明深度减少必然伴随通信增加 |
| **多跳推理的迭代机制** | 多数投票或链式传递 | **迭代查询（Iterative Query）**：管理者广播子查询，持有相关事实的智能体响应，逐跳推进 | 深度下界 $\Omega(k)$，通信下界 $\Omega(k)$，证明添加智能体无法减少深度 |

### 改变的关键维度（Changed Slots）

1. **智能体间通信模式**：从“无通信”或“独立投票”转变为**任务特化的结构化协议**——关联回忆仅需 $O(1)$ 通信，状态跟踪需 $O(w)$ 通信以换取深度缩减，多跳推理需 $O(k)$ 通信且深度不可缩减。

2. **状态跟踪的计算深度**：从单智能体的 $O(N)$ 线性深度，通过前缀和协议降为 $\mathcal{O}(N/w + \log w)$，实现了**智能体数量增加带来的亚线性加速**。这一加速的理论代价是通信量从 $O(1)$ 增至 $O(w)$，形成了不可消除的折衷。

3. **输入划分策略**：从“完整输入给每个智能体”（投票）或“顺序分块传递”（CoA）转变为**不相交的等大小分块**分发给各工作智能体，使得局部计算可并行执行，通信仅用于组合部分结果。

### 核心洞察：深度-通信折衷的三种体制

本工作的理论分析（Proposition 4.1）证明了一条基本守恒律：**任何多智能体协议的总计算规模（Size）与等效单智能体协议相同（至多常数因子差异）**，因此深度的减少只能通过增加通信来实现。由此导出了三种可行体制和一种不可能体制（Figure 2）：

- **体制1（关联回忆）**：深度和通信均可保持常数，多智能体可处理更长上下文而不增加延迟。
- **体制2（状态跟踪）**：深度可通过增加智能体减少，但通信代价相应增加，存在最优的 $N/w(N)$ vs $w(N)$ 折衷。
- **体制3（多跳推理）**：深度无法通过增加智能体减少，且通信成本与跳数线性相关，多智能体在此类任务上无加速优势。
- **不可能体制**：同时减少深度和通信是不可能的——这为多智能体系统的设计提供了明确的边界条件。

这些创新将多智能体推理从经验性探索提升到了**可预测、可优化、可证明**的理论层面，为后续的多智能体LLM系统设计提供了原则性指导。



![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/001_Table_1.jpg]]
*Table 1: Summary of results. w denotes the number of agents. N represents the length of the input. Size corresponds to total computation. Depth loosely corresponds to wall-clock time. Communication refers to the overall amount of communication between agents. We will define these formally in Section 3. O(·) indicates existence of a protocol; Θ(·) indicates that we prove it optimal*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/002_Figure_1.jpg]]
*Figure 1: (a) Graphical representation of recall protocol (Sec. 4.2). T1, T2 and $\bar { T _ { 3 } }$ are worker agents given chunks of 2 key-value pairs. Only $T _ { 3 }$ has the query in its context and thus communicates the answer to the manager $T _ { M }$ after reasoning*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/003_Figure_2.jpg]]
*Figure 2: (b) Example of a prefix sum protocol for state tracking (Sec. 4.3) on input 11100100. Here T2 and T _ { 4 } act as intermediate managers composing together the answers of T _ { 1 } and T _ { 3 } with their own. T _ { 4 } also acts as the final manager, providing the final output*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/004_Figure_1.jpg]]
*Figure 1: (c) Example of the Iterative Query protocol (Sec. 4.4). Each agent holds one fact. The full query, friend(boss(b)), is managed by T _ { 2 } , , which receives answers at t = 3 , 5 and broadcasts followup queries at t = 2 , 4 . Figure 1: Graphical representations of the protocols analyzed in Section 4*

本文构建了一个面向多智能体推理系统的形式化分析框架，其核心目标在于从理论上刻画**计算深度（墙钟时间）**与**通信代价**之间的基本折衷。该框架将多智能体系统抽象为一个有向通信图，其中节点表示智能体在某一时刻的状态，边则编码两类信息流动：**思维链（CoT）令牌**（同一智能体内部的顺序推理）和**通信令牌**（跨智能体的消息传递）。

### 形式化基础

分析建立在**唯一硬注意力 Transformer（UHAT）**的表达性理论之上。UHAT 将标准软注意力在每一层替换为对注意力得分最高位置的独热选择：

$$\operatorname{UHAT}(\mathbf{A})_{i,j} = \begin{cases} 1 & \text{if } j = \arg\max \mathbf{A}_{i,:} \\ 0 & \text{else} \end{cases}$$

这一简化模型已被证明在固定精度下涵盖标准软注意力 Transformer 的表达能力（Jerad et al., 2025a），因此其理论下界对实际系统具有约束力。

### 系统架构：工作-管理范式

多智能体系统由两类角色构成：

1. **工作智能体（Worker Agent）**：输入被均匀划分为 $w$ 个不相交的块，每个工作智能体接收其中一块。工作智能体负责对本地上下文进行局部推理，并产生 CoT 令牌。在需要通信时，工作智能体可以向其他智能体发送单令牌消息。

2. **管理智能体（Manager Agent）**：协调通信流程，汇总各工作智能体的局部结果，最终输出答案。管理智能体本身也可以持有输入块，在部分协议中同时承担计算与协调职责（见 Figure 1(b) 中 T2 和 T4 的双重角色）。

系统完成计算的定义是：管理智能体的最后一条 CoT 边标签等于目标函数值 $f(x)$。

### 三个核心协议模块

框架针对三类代表性推理任务，分别给出了具有可证明边界的通信协议：

- **关联回忆协议（Associative Recall）**：工作智能体在各自输入块中查找与查询匹配的键值对。持有匹配结果的智能体将答案直接传递给管理智能体。该协议实现了 $\mathcal{O}(1)$ 的计算深度和 $\mathcal{O}(1)$ 的通信量，与输入长度和智能体数量无关（Proposition 4.2）。

- **前缀和协议（Prefix Sum，用于状态跟踪）**：借鉴并行扫描算法，智能体以二叉树结构递归组合局部计算结果。计算深度上界为 $\mathcal{O}(\log w(N) + N/w(N))$，下界为 $\Omega(N/w(N))$（Proposition 4.6, 4.7）。这揭示了深度减少必须以增加通信为代价的核心机制。

- **迭代查询协议（Iterative Query，用于多跳推理）**：工作智能体执行迭代查找——每跳一步，每个智能体在其本地上下文中寻找下一跳答案，并通过管理智能体广播后续查询。该协议的计算深度为 $\mathcal{O}(k)$，与跳数线性相关，且无法通过增加智能体来减少（Proposition 4.8）。

### 深度-通信折衷的三个体制

理论分析揭示了三种可行体制和一种不可能体制（Figure 2, Table 1）：

| 体制 | 深度 | 通信 | 典型任务 |
|------|------|------|----------|
| 体制 I | 恒定 $\mathcal{O}(1)$ | 恒定 $\mathcal{O}(1)$ | 关联回忆 |
| 体制 II | 随 $w(N)$ 增加而降低 | 随 $w(N)$ 增加而升高 | 状态跟踪（PARITY） |
| 体制 III | 固定下界，无法通过增加智能体降低 | 随任务复杂度线性增长 | 多跳推理 |

这一分类的理论基石是**规模守恒原理**（Proposition 4.1）：任何多智能体协议均可转换为总计算规模相同的单智能体协议，且深度的减少只有通过增加通信才能实现。由此导出规模-深度不等式：

$$\frac{\text{Size}(N)}{w(N)} \leq \text{Depth}(N)$$

该不等式构成了所有协议设计的根本约束。

### 实验验证流程

实验部分采用预训练大语言模型（Llama-3.3-70B-Instruct-Turbo 和 Llama-3.1-8B-Instruct-Turbo），通过提示词赋予模型在协议中的角色和任务指令。通信协议采用硬编码方式实现，与 **Chain-of-Agent**（Zhang et al., 2024b）的实现类似。基线方法包括**多数投票法**（Wang et al., 2022）和单智能体思维链。所有实验重复 100 次（随机种子 42），超参数在验证子集上调整，确保比较公平性。



### 3.1 多智能体系统的形式化定义

本研究将多智能体推理系统形式化为一个有向无环图（DAG）。系统由两类核心模块构成：

**工作智能体（Worker Agent）** 接收输入的一个不相交子块，执行局部推理并产生思维链（CoT）令牌。**管理智能体（Manager Agent）** 负责协调通信、汇总局部结果并输出最终答案。两者通过**通信边（Communication Edges）** 连接，每条边传输单令牌消息（通信令牌或CoT令牌）。

具体而言，给定输入 $x$，系统将其均匀划分为 $w$ 个不相交的块，第 $i$ 个智能体接收的子串为：

$$x_{\left\lceil |x| \cdot \frac{i}{w} \right\rceil, \cdots, \left\lceil |x| \cdot \frac{i+1}{w-1} \right\rceil}$$

系统计算函数 $f$ 当且仅当管理智能体的最后一条CoT边的标签为 $f(x)$。每个智能体的计算由构造字符串 $\xi(i)$ 定义，该字符串包含输入块、智能体ID及遍历节点信息。一个Transformer $T$ 实现该系统，当且仅当每个 $\xi(i)$ 适合上下文窗口，且 $T$ 能自回归地预测所有输出令牌。

### 3.2 基础计算模型：UHAT

理论分析基于**因果掩码的唯一硬注意力Transformer（UHAT）**。其注意力机制定义为：

$$\operatorname{UHAT}(\mathbf{A})_{i,j} = \begin{cases} 1 & \text{if } j = \arg\max \mathbf{A}_{i,:} \\ 0 & \text{else} \end{cases}$$

该机制将注意力完全集中在得分最高的位置，忽略其余所有位置。UHAT在表达能力上包含了固定精度下的普通softmax Transformer（Jerad et al., 2025a），因此理论下界同样适用于实际软注意力模型。

### 3.3 规模-深度不等式

多智能体系统存在一个基本约束——**规模守恒**（Proposition 4.1）：任何多智能体协议都可转化为等效的单智能体协议，且总计算规模（Size）至多相差常数因子。由此导出核心不等式：

$$\frac{Size(N)}{w(N)} \leq Depth(N)$$

该式表明：**总计算规模除以智能体数量，不超过计算深度**。换言之，深度的减少只有通过增加智能体数量才能实现，但这是以增加通信为代价的——这是贯穿全文的深度-通信折衷的理论根基。

### 3.4 三类任务的协议与边界

论文针对三类代表性推理任务，分别设计并分析了最优通信协议，其核心公式与边界汇总于Table 1。

#### 关联回忆（Associative Recall）

协议采用**并行查找**：输入被分割给 $k$ 个工作智能体，每个智能体在本地块中查找与查询匹配的键值对。持有查询的智能体找到答案后，通过单次通信将结果传递给管理智能体。

**深度上界**：$O(1)$，**通信上界**：$O(1)$。两者均与上下文长度 $N$ 和智能体数量 $w$ 无关。这是唯一一类可实现“零额外代价”并行化的任务。

#### 状态跟踪（State Tracking）与前缀和协议

核心思想是将**前缀和（Prefix Sum）** 算法映射到多智能体系统：工作智能体计算局部聚合结果，中间管理智能体递归组合，最终管理智能体输出全局结果。该协议对应Figure 1(b)所示的树状通信结构。

**深度上界**（Proposition 4.6）：

$$\mathcal{O}\left(\log w(N) + \frac{N}{w(N)}\right)$$

其中第一项来自树形归约的 $\log w(N)$ 层，第二项来自每个智能体处理长度为 $N/w(N)$ 的本地块。

**深度下界**（Proposition 4.7，针对非平凡群上的状态跟踪）：

$$\Omega\left(\frac{N}{w(N)}\right)$$

该下界表明：即使无限增加智能体，深度也无法压缩到 $O(1)$——每个智能体必须至少处理其本地块的线性计算量。同时，通信代价随 $w(N)$ 增长，形成 $N/w(N)$ 深度与 $w(N)$ 通信之间的显式折衷（Figure 4(b) 实验验证）。

#### 多跳推理（k-hop Reasoning）与迭代查询协议

协议采用**迭代查找**：每个工作智能体持有一个事实三元组，管理智能体广播当前子查询，持有匹配事实的智能体返回下一跳实体。此过程迭代 $k$ 轮。

**深度下界**：$\Theta(k)$，即计算深度随跳数线性增长。**通信下界**：$\Theta(k)$。关键结论是：**添加更多智能体无法减少深度**，因为每跳推理本质上是顺序依赖的。Figure 5(c) 的实验结果与此理论预测一致。

### 3.5 多数投票的电路复杂性下界

作为基线方法的分析，论文证明了多数投票（Majority Voting）精确计算PARITY所需的电路规模下界（Appendix H）：

$$s(N) = 2^{\Omega(N^{1/(4d)})}$$

其中 $d$ 为电路深度。该指数级下界解释了为什么多数投票在长序列状态跟踪任务中性能急剧下降（Figure 4(a)）：独立智能体无法通过简单投票有效聚合全局状态信息。



## 实验与关键发现

### 实验设置

论文在三个构造性任务上验证理论预测：**关联回忆**（Needle-in-a-Haystack）、**状态跟踪**（PARITY 和 S₅ 排列）以及 **k 跳推理**。所有实验采用预训练大语言模型作为智能体，通过提示词指定其在协议中的角色和任务指令。通信协议采用硬编码方式实现，类似于 **Chain-of-Agent**（Zhang et al., 2024b）的实现范式。基线方法包括：

- **单智能体 CoT**：无多智能体交互的独立推理；
- **多数投票法**（**Self-consistency**, Wang et al., 2022）：各智能体独立处理完整输入后投票；
- **链式代理**（**Chain-of-Agent / CoA**, Zhang et al., 2024b）：智能体间顺序传递通信。

实验重复 100 次，随机种子固定为 42，超参数在验证子集上调优。主要使用 **Llama-3.3-70B-Instruct-Turbo** 和 **Llama-3.1-8B-Instruct-Turbo** 进行比较。

### 主实验结果

#### 关联回忆：恒定深度与通信的理论最优性

在 Needle-in-a-Haystack 任务中（Figure 3），**多数投票法**在面对极长上下文和极端深度时准确率显著下降，而 **CoA** 在所有上下文长度和深度组合下均保持接近 1.0 的准确率。这与理论预测一致：关联回忆任务可通过 $O(1)$ 深度和 $O(1)$ 通信解决，与智能体数量无关。CoA 的令牌使用量也保持恒定，不受块大小和上下文长度影响（Figure 3c），进一步验证了理论上的通信上界。

#### 状态跟踪：前缀和协议的显著优势

在 PARITY 任务上（Figure 4a），**前缀和协议**在所有序列长度下一致优于多数投票法和 CoA，且优势随序列长度增长而扩大——在最大长度处准确率保持在约 0.8，而其他方法显著退化。这一结果与理论预测的深度上界 $\mathcal{O}(\log w(N) + N/w(N))$ 一致：前缀和协议通过并行归约将深度从 $O(N)$ 降至 $O(N/w(N) + \log w(N))$，以通信量换取计算深度的降低。

在 S₅ 排列任务上（Figure 9, 10），前缀和协议在 Llama-8B 和 Llama-70B 上均优于多数投票法和 CoA，且使用更大模型（Llama-70B）时所有方法的性能均有提升，但协议间的相对优势关系保持不变。

#### k 跳推理：迭代查询协议随跳数增加的优势

在 k 跳推理任务中（Figure 5），**迭代查询协议**在跳数增加时显著优于多数投票法。当事实数量为 500 时，迭代查询在 20 跳处准确率仍保持在 0.90 以上，而多数投票法则降至约 0.30（Figure 5b）。计算深度随跳数线性增长（Figure 5c），符合理论上 $O(k)$ 的下界——这表明多跳推理无法通过增加智能体来减少深度，且通信成本随跳数线性增长。

### 消融实验

#### 深度-通信折衷的实证验证

Figure 4b 展示了 PARITY 任务中计算深度与总通信量之间的关系：随着通信预算增加，计算深度下降，但存在最优的折衷点。这一趋势与理论预测的 $N/w(N)$ 计算深度与 $w(N)$ 总通信量之间的权衡关系一致。当智能体数量增加时，每个智能体的局部计算深度减少，但智能体间的通信总量相应增加，验证了“深度的减少只有通过增加通信才能实现”这一核心论断。

#### 模型规模的影响

使用 Llama-70B 替代 Llama-8B 能全面提升所有协议的性能（Figure 9 vs Figure 10），但不同协议之间的相对趋势依然成立：前缀和协议在状态跟踪任务上始终最优，迭代查询在 k 跳推理中始终优于多数投票。这表明理论预测的协议优势不依赖于特定模型规模。


![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/012_Figure_10.jpg]]
*Figure 10: (b) Accuracy vs number of hops in the query for 500 facts. The difference in performance is more pronounced in this regime*

#### 不同模型架构的泛化性

在 k 跳推理任务中，使用 EXAONE 模型（Figure 11-13）的结果与 Llama 系列一致：迭代查询协议在不同跳数和事实数量下均优于多数投票法，验证了协议优势的跨模型泛化性。

### 失败模式与局限

尽管理论预测的协议在多数场景下表现优越，实验中仍存在以下值得注意的失败模式：

1. **极端序列长度下的退化**：在 PARITY 任务中，即使是最优的前缀和协议，在序列长度超过 256 时准确率也开始下降（Figure 4a），表明实际 LLM 在处理长序列组合操作时存在能力瓶颈，与理论上的渐近上界存在差距。

2. **多数投票法的系统性失效**：多数投票法在关联回忆的长上下文极端深度处、PARITY 的长序列处以及 k 跳推理的高跳数处均出现显著退化。理论分析表明，对于 PARITY 任务，多数投票精确计算所需的电路规模下界为 $s(N) = 2^{\Omega(N^{1/(4d)})}$，这解释了其根本性的扩展限制。

3. **硬编码协议的能力浪费**：通信协议采用硬编码方式，未涉及自适应学习或动态路由，可能未充分利用 LLM 的推理能力。在更复杂的真实场景中，固定的通信模式可能不是最优的。

4. **均匀分块的假设**：理论分析假设输入被均匀划分为 $w$ 个不相交的块，实际应用中负载均衡和分块策略可能更为复杂，不均匀的信息分布可能破坏理论上的深度-通信上界。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_0aPIVJUz5T/figures/009_Figure_7.jpg]]
*Figure 7: (a) Llama-70B accuracy on PARITY for different sequence lengths. Prefix Sum represents the theoretically optimal communication protocol*




## 定位与知识库关联

### 核心贡献与理论定位

本文的核心贡献在于首次为多智能体推理系统建立了严格的**表达能力理论框架**，并据此揭示了计算深度（墙钟时间）与通信成本之间不可消除的折衷关系。这项工作植根于Transformer表达性理论的丰富文献，特别是基于**唯一硬注意力Transformer（UHAT）** 模型（Jerad et al., 2025a）构建形式化分析。UHAT被证明在固定精度下包含普通软注意力Transformer的表达能力，因此理论下界同样适用于实际系统。

论文的核心洞察在于证明：**多智能体推理中深度的减少只有通过增加通信才能实现**（Proposition 4.1）。这一“规模守恒”原理将多智能体系统的设计空间划分为三种可行体制与一种不可能体制（Figure 2），为理解现有方法和设计新协议提供了统一的理论透镜。

### 与基线方法的关系

论文将现有主流多智能体方法映射到其理论框架中，并揭示了各自的适用边界：

- **单智能体思维链（Single-Agent CoT）**：作为无通信基线，其计算深度随问题规模线性增长。在状态跟踪任务中深度为 $O(N)$，在多跳推理中为 $O(k)$。理论表明，任何多智能体协议都可转化为等效的单智能体协议且总规模不变（Proposition 4.1），因此单智能体方法在总计算量上并无劣势，其瓶颈在于深度（延迟）而非规模。

- **多数投票法（Majority Voting / Self-Consistency）**（Wang et al., 2022）：每个智能体独立处理完整输入后投票。本文从理论上证明了该方法在PARITY等状态跟踪任务上的根本性局限：精确计算所需的电路规模下界为 $s(N) = 2^{\Omega(N^{1/(4d)})}$（Appendix H, Eq 26），这意味着随着序列长度增长，多数投票法的表达能力呈指数级衰减。实验证实了这一预测：在Needle-in-a-Haystack任务中，多数投票法在长上下文极端条件下准确率显著下降（Figure 3(a)）；在PARITY任务中准确率随序列长度增长而持续衰减（Figure 4(a)）；在k跳推理中，当事实数量增至500、跳数达20时准确率跌至约0.30（Figure 5(b)）。

- **链式代理（Chain-of-Agent, CoA）**（Zhang et al., 2024b）：智能体顺序传递中间结果。本文将其识别为关联回忆任务的理论最优协议，可实现 $O(1)$ 深度和 $O(1)$ 通信（Proposition 4.2）。实验证实CoA在Needle-in-a-Haystack任务中保持接近完美的准确率，不受上下文长度影响（Figure 3(b)），且令牌使用量恒定（Figure 3(c)）。然而，CoA在状态跟踪任务中表现不佳，因为顺序传递无法并行化前缀计算，其深度仍为 $O(N)$。

### 提出的最优协议及其理论保证

针对三类算法任务族，论文提出了具有可证明边界的最优通信协议：

| 任务 | 协议 | 规模（Size） | 深度（Depth） | 通信（Communication） |
|------|------|-------------|--------------|----------------------|
| 关联回忆 | 分区检索 | $\Theta(N)$ | $\Theta(1)$ | $\Theta(1)$ |
| 状态跟踪 | 前缀和 | $\Theta(N)$ | $\mathcal{O}(\log w(N) + \frac{N}{w(N)})$ | $\Theta(w(N))$ |
| k跳推理 | 迭代查询 | $\Theta(k)$ | $\Theta(k)$ | $\Theta(k)$ |

- **关联回忆**（Proposition 4.2）：将输入不相交地分块分配给 $w$ 个智能体，每个智能体同时拥有查询。持有目标键值对的智能体直接向管理器通信答案。深度和通信均为常数，与智能体数量和上下文长度无关。

- **状态跟踪/前缀和**（Proposition 4.5-4.7）：采用递归并行扫描算法，智能体形成二叉树结构进行局部组合。深度上界为 $\mathcal{O}(\log w(N) + \frac{N}{w(N)})$，下界为 $\Omega(\frac{N}{w(N)})$。这揭示了深度-通信折衷的核心机制：增加智能体数量 $w(N)$ 可减少深度，但总通信量 $\Theta(w(N))$ 相应增加。实验在PARITY任务上验证了这一预测（Figure 4(b)），前缀和协议在所有序列长度上显著优于多数投票法和CoA（Figure 4(a)）。

- **k跳推理/迭代查询**（Proposition 4.8）：每个智能体持有一个事实，管理器智能体迭代广播子查询并收集答案。深度和通信均为 $\Theta(k)$，与跳数线性相关。理论证明该任务的深度**无法**通过增加智能体来减少——这是不可消除的串行依赖。实验证实迭代查询在跳数增加时保持高准确率（500事实、20跳时仍>0.90），而多数投票法大幅下降至约0.30（Figure 5(b)），且计算深度随跳数线性增长（Figure 5(c)）。

### 适用边界与局限

1. **理论模型的假设限制**：理论分析基于UHAT硬注意力模型。虽然UHAT在固定精度下包含软注意力Transformer的表达能力，但实际软注意力模型的精确映射关系仍有待完善。论文给出了推广方向，但严格的理论保证尚未建立。

2. **任务覆盖范围有限**：理论结果仅覆盖三个算法任务族（关联回忆、状态跟踪、k跳推理）。对于更广泛的推理问题——如图可达性、约束满足、数学推理等——深度-通信折衷可能呈现不同的体制，泛化性尚未建立。

3. **实验生态的局限性**：实验局限于少数大语言模型（Llama-3.3-70B-Instruct-Turbo、Llama-3.1-8B-Instruct-Turbo）和构造性任务（PARITY、S5排列、合成多跳推理）。真实世界的多智能体应用场景（如开放域问答、代码生成、多步规划）可能引入额外的复杂性，如非均匀输入分布、动态任务分解等。

4. **通信协议的硬编码性质**：所有协议采用硬编码的通信模式，智能体角色和交互顺序由人工预设。这未涉及自适应学习、动态路由或基于置信度的通信决策，可能未充分利用LLM的推理能力。如何将理论上的最优协议转化为可端到端学习或微调的系统仍是开放问题。

5. **输入分块的简化假设**：理论假设输入被均匀划分为 $w$ 个不相交的块（Definition 3.3, case 1）。实际应用中，负载均衡和语义感知的分块策略可能更为棘手，尤其是在信息密度不均匀的自然语言场景中。

### 开放问题

- **可学习协议的转化**：如何将理论上的最优通信模式转化为可端到端微调或强化学习优化的多智能体系统，使其适应非结构化任务和动态环境？

- **更广泛任务类的理论刻画**：在一般图推理、对抗性合作、约束满足等任务中，深度-通信折衷是否会呈现不同的体制？是否存在新的不可能性结果？

- **共享输入场景的建模**：当所有智能体共享同一输入（如多数投票或集体讨论）时，如何更准确地建模其通信成本？当前的框架主要针对输入分块场景。

- **近似计算的边界**：对投票方法的性能下界（如PARITY的指数级电路下界）能否推广到近似准确的情形，而不仅限于精确计算？这对理解实际LLM的近似推理能力至关重要。

- **多令牌消息的影响**：当前形式化假设单令牌通信消息。多令牌消息（如自然语言中间结果）是否会影响通信预算的精确边界，特别是在长消息场景中？前缀和协议中的中间组合步骤可能受益于更丰富的消息表示。

- **实际系统设计的启示**：论文提出的前缀和式级联（prefix-sum–style cascade）和迭代查询协议对实际多智能体系统设计具有潜在指导意义。前者通过迭代摘要减少最终智能体的瓶颈，后者为多跳推理提供了结构化的查询-响应模式。这些思想如何融入现有的多智能体框架（如AutoGen、CrewAI）值得进一步探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Benefits_and_Limitations_of_Communication_in_Multi_Agent_Reasoning.pdf]]
