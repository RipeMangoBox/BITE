---
title: "Multi-objective Large Language Model Alignment with Hierarchical Experts"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multi_objective_Large_Language_Model_Alignment_with_Hierarchical_Experts.pdf
project_link: null
code_link: https://github.com/lizhuolz/HoE
openreview_forum_id: UhmEdfAk46
aliases:
- HHME
- MOLLMAHE
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/online
core_operator: "将多目标对齐分解为一系列单偏好子问题，并为每个子问题分配专门的专家参数（LoRA和路由专家），通过分层路由实现任意偏好的动态组合。"
primary_logic: "采用分解策略，利用任务向量SVD提取轻量LoRA专家，结合模型合并生成多目标专家，再训练极少参数的路由专家进行细粒度动态选择，无需重训骨干模型即可覆盖完整帕累托前沿。"
claims:
- "HoE通过将多目标对齐分解为单偏好子问题并由专门专家处理，突破了单一模型无法覆盖整个帕累托前沿的瓶颈。"
- "HoE在二目标对齐中一致获得优于RS和MOD的帕累托前沿，并在多个基准上超过15个基线方法。"
- "HoE是最轻量、可帕累托操控、训练负担最低的方法，仅需存储一个模型且推理代价为1×。"
- "HelpSteer 上 Average Score (Helpful, Correctness, Coherence, Complexity,... = 62.1"
---

# Multi-objective Large Language Model Alignment with Hierarchical Experts

> [!tip] 核心洞察
> 采用分解策略，利用任务向量SVD提取轻量LoRA专家，结合模型合并生成多目标专家，再训练极少参数的路由专家进行细粒度动态选择，无需重训骨干模型即可覆盖完整帕累托前沿。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于分层专家的多目标大语言模型对齐 |
| 英文题名 | Multi-objective Large Language Model Alignment with Hierarchical Experts |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UhmEdfAk46) · [GitHub](https://github.com/lizhuolz/HoE) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/online |
| Method | HoE (Hierarchical Mixture-of-Experts) |
| Dataset | HelpSteer, HelpAssistant, Reddit Summary, BeaverTails (two-objective alignment, Figure 3) |

> [!tip] 效果简介
> - HelpSteer 上，Average Score (Helpful, Correctness, Coherence, Complexity, Verbosity) 为 62.1，对比 58.3 (RS), 58.5 (RiC), 58.9 (MOD)，变化 +3.8。
> - HelpSteer 上，Average Score 为 62.08，对比 58.48 (RS), 58.48 (RiC), 58.48 (MOD)，变化 +3.6。
> - HelpSteer 上，Average Score 为 62.1，对比 58.9 (RS), 58.9 (RiC), 58.9 (MOD)，变化 +3.2。

## 概要

大语言模型的对齐通常需要在多个相互冲突的目标之间取得平衡，例如有用性、无害性和幽默性。现有方法难以同时优化这些冲突目标，且单一模型无法在任意用户偏好权重下达到帕累托最优，导致可操控性瓶颈。本文提出**HoE（Hierarchical Mixture-of-Experts）**，一种轻量级、参数高效、即插即用的多目标对齐框架，无需重新训练骨干模型即可覆盖完整的帕累托前沿。

HoE的核心洞察在于将多目标对齐分解为一系列单偏好子问题，并为每个子问题分配专门的专家参数。具体而言，框架由三个层次组件构成：**LoRA专家**从现成的单目标模型中通过任务向量奇异值分解（task-SVD）无训练提取，并通过模型合并合成多目标专家；**路由器专家**是插入每个Transformer块的轻量线性层，冻结LoRA专家后仅训练极少参数，利用Tchebycheff标量化实现特定偏好的细粒度动态选择；**偏好路由**根据用户偏好向量在偏好空间中选择最近邻专家子集并计算投票权重。

与现有方法相比，HoE在多个维度上展现出显著优势（Table 1）：仅需存储一个模型（vs. MORLHF需存储M个模型），推理代价归一化为1×（vs. MOD的N×或PAD的3×），训练模型数为0（仅训练轻量路由器），支持帕累托操控，具备多任务能力，且可扩展至新目标而无需重训已有专家。

在16个目标、200种不同偏好、8个基准上的实验表明，HoE一致地超越15个近期基线方法。二目标对齐中，HoE的帕累托前沿始终优于RS和MOD，并在7个设置中的5个上超过RiC（Figure 3）。三目标对齐中，HoE在14个评估设置中的11个上排名第一（Figure 4）。五目标对齐中，HoE在HelpSteer基准上取得最高平均分62.1，较最佳基线提升3.2–3.8分（Table 2）。成本分析显示，HoE训练仅需3.2小时×2轮、8M可训练参数，推理延迟仅为标准解码的1.23×，远优于需要2–3×推理代价的竞争方法（Table 3）。

消融实验进一步验证了设计的有效性：组合LoRA专家与路由器专家能实现近乎完整的帕累托前沿覆盖，而仅使用LoRA专家覆盖有限（Figure 5左）；LoRA秩为256即可在性能与效率间取得较好平衡（Figure 5中）；Tchebycheff标量化比线性标量化训练更稳定并能保持完整帕累托覆盖（Figure 5右）。案例研究可视化显示，路由器专家能在token级别动态选择不同的LoRA专家，实现对不同目标的细粒度控制（Figure 6）。

**局限性**方面，HoE依赖现成的单目标优化模型，若不可用则需从头训练，成本较高；模型合并与SVD压缩在部分场景下可能失效，泛化性受限。**待探索问题**包括：在高度非凸目标空间中插值偏好是否始终保持在帕累托前沿，以及在目标数量极多时专家数量的扩展性和内存效率。



### 多目标对齐的核心瓶颈

大语言模型（LLM）在实际部署中需要同时满足多个相互冲突的对齐目标——例如有用性（helpfulness）、无害性（harmlessness）、幽默感（humor）、简洁性（conciseness）等。现有对齐方法面临一个根本性瓶颈：**单一模型无法在任意用户偏好权重下达到帕累托最优**，导致可操控性（steerability）严重受限。

具体而言，当用户对多个目标的偏好权重发生变化时（例如某场景下无害性优先于有用性，另一场景则相反），传统方法要么需要为每种偏好组合重新训练一个独立模型，要么通过线性插值等粗糙手段在已有模型间折中，但线性组合往往偏离帕累托前沿，产生次优解。这一瓶颈的因果机制在于：多目标优化本质上是一个多策略问题，不同偏好对应帕累托前沿上的不同点，而单一模型参数集合只能编码一个点，无法覆盖整个前沿。

### 现有方法的缺口

表1系统对比了13种现有对齐方法在七个维度的能力。从中可以识别出三个结构性缺口：

**训练与存储负担过重。** MORLHF为每种偏好训练独立模型，需存储M个完整模型（M为偏好数量）；MODPO同样需存储多个模型。RS和MOD虽无需训练，但需存储N个单目标模型（N为目标数量）。这些方法的存储和训练成本随目标或偏好数量线性增长，可扩展性差。

**推理效率与帕累托可操控性无法兼得。** 解码时方法（如Args、GenARM、PARM）虽支持帕累托操控，但推理代价高达N倍以上，因为需要多次前向传播或候选生成。Steering和MetaAligner推理代价较低，但不支持帕累托操控——用户无法动态调整目标权重。LoraMoE和PAD仅存储单一模型，但同样不支持帕累托操控。

**多任务能力缺失。** 绝大多数方法在设计上仅针对特定对齐目标组合，无法同时保持多任务性能。仅RS和MOD因模型合并的天然特性具备多任务能力，但它们在帕累托前沿覆盖上表现有限。

综合来看，现有方法在“轻量存储—低推理代价—帕累托可操控—多任务能力—可扩展性”五个维度上存在不可能三角式的权衡，没有任何方法能同时满足所有需求。

### 本文动机与核心洞察

本文的核心洞察是采用**分解策略**来突破上述瓶颈：将多目标对齐问题分解为一系列单偏好子问题，每个子问题由专门的专家参数处理，再通过分层路由实现任意偏好的动态组合。

这一策略的技术可行性建立在三个关键观察之上：

1. **任务向量可压缩性**：单目标微调模型与预训练模型的参数差（任务向量）可通过SVD压缩为低秩LoRA适配器，且性能损失可控。这意味着可以用极少的参数存储每个目标的“对齐知识”。

2. **模型合并可合成多目标专家**：通过对单目标任务向量进行加权合并，可以为任意偏好向量合成对应的多目标专家参数，无需从头训练。

3. **路由专家可细粒度动态选择**：在Transformer每层插入极轻量的路由网络（仅8M可训练参数），通过Tchebycheff标量化优化，即可实现对不同偏好的token级动态专家选择，覆盖完整帕累托前沿。

基于以上观察，HoE（Hierarchical Mixture-of-Experts）框架以**几乎无需训练骨干模型**的方式，将多目标对齐的所有偏好统一存储于单一模型中，推理代价仅1倍，同时支持任意偏好的连续帕累托前沿遍历。



## 核心方法与创新机理

### 瓶颈突破：从单模型到分层专家解耦

现有大语言模型对齐方法面临一个结构性瓶颈：当优化目标多于一个时，单一模型无法在任意偏好权重下同时达到帕累托最优。基于奖励模型合并的RS（Rewarded Soups）和基于解码时logits融合的MOD（Multi-objective Decoding）虽然支持偏好操控，但受限于线性组合的粗糙表达；MORLHF虽能覆盖帕累托前沿，却需为每个偏好向量训练并存储独立模型（$M$个模型，$M \gg N$），存储和训练成本随目标数量爆炸式增长。

HoE的核心创新在于将多目标对齐问题**分解为一组单偏好子问题**，并为每个子问题分配专门的专家参数。通过分层路由机制，HoE实现了任意偏好向量的动态组合，从而在单一模型中覆盖完整的帕累托前沿（Fig. 1）。

### 三层分层架构

HoE由三个层次化的组件构成，形成从粗粒度偏好分解到细粒度动态路由的完整管线：

1. **LoRA专家（基础层）**：从现成的单目标优化模型中提取任务向量 $\tau_i = \theta_i - \theta_{pre}$，通过task-SVD压缩为轻量LoRA适配器。进一步通过模型合并合成多目标专家 $\tau_\lambda = \mathrm{Merge}(\{\tau_i\}_{i\in[N]}, \lambda)$，无需训练即可为任意偏好向量生成对应的专家参数。

2. **路由器专家（控制层）**：在每个Transformer块中插入轻量线性路由器，冻结所有LoRA专家，仅优化路由器参数。采用Tchebyscheff标量化 $J(\theta|\lambda) = \max_\theta \min_i \{\lambda_i (\mathbb{R}_i(\theta) - z_i^*) \}$ 而非线性标量化的关键设计，避免了训练偏向帕累托边缘的问题，保持完整的帕累托前沿覆盖（Fig. 5 Right）。

3. **偏好路由（调度层）**：推理时根据用户偏好向量在偏好空间中选择最近邻专家子集，计算投票权重，实现token级的细粒度专家选择。

### Changed Slots：与基线的系统性差异

Table 1的系统对比揭示了HoE在七个关键维度上相对于15个基线方法的突破性变化：

| 维度 | 基线典型值 | HoE | 创新实质 |
|------|-----------|-----|---------|
| **训练模型数** | $M$（MORLHF）、$>1$（RiC）、$1$（DPA） | $0$（仅训练轻量路由器） | 主体免训练，仅优化8M参数的路由器 |
| **存储模型数** | $M$（MORLHF）、$N$（RS/MOD）、$1$（DPA） | $1$（单一模型存储所有偏好） | 通过LoRA专家统一存储，消除多模型冗余 |
| **推理代价** | $1\times$（MORLHF）、$N\times$（MOD）、$2\times$（MetaAligner）、$3\times$（PAD） | $1\times$（仅激活少量轻量专家） | 单次解码，实际开销仅$1.23\pm0.2\times$ |
| **帕累托可操控** | 部分方法支持（MORLHF、RS、MOD等），部分不支持（Steering、MetaAligner） | **支持**，连续遍历帕累托前沿 | 任意偏好向量均可实时响应 |
| **多任务能力** | 仅RS和MOD支持 | **支持**，无需特殊设计即具竞争力 | 路由器专家的任务专业化机制 |
| **可扩展性** | 多数需重训（MORLHF、DPA等），少数可扩展（RS、MOD） | **可扩展**，新目标通过扩展偏好向量加入 | 无需重训已有专家 |
| **结构化提示依赖** | 多数依赖（RiC、DPA、PAD等） | **不依赖** | 消除提示工程负担 |

这些changed slots共同构成了HoE的差异化优势：**最轻量、可帕累托操控、训练负担最低的方法**，仅需存储一个模型且推理代价为$1\times$，同时具备最高的可扩展性。



![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/002_Figure_1.jpg]]
*Figure 1: (Left) HoE decomposes the multi-objective alignment problem into a series of single-preference subproblems, each handled by a specialized expert. (Right) HoE employs hierarchical experts, integrating LoRA and router experts to approach near-optimal Pareto frontier*

![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/004_Figure_2.jpg]]
*Figure 2: Illustration of our HoE approach. The left side illustrates the application scenario, where the model generates a response aligned with the prompt and given preferences. The bottom-right highlights its three hierarchical components - the LoRA experts, router experts, and a preference routing. The top-right depicts individual components, each serving as an expert for specific weightings, designed for seamless plug-and-play integration within the model*

![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/003_Table_1.jpg]]
*Table 1: Comparison with other alignment methods. M is number of preference, N is number of objectives and M $\gg$ N . Our HoE approach is a pareto-steerable and lightweight method with highest scalability, least storage cost and least inference cost, which eliminates the need for retraining any new models or any structed prompts. Each characteristic is empirically conformed in Section B.5*

HoE（Hierarchical Mixture-of-Experts）将多目标LLM对齐问题分解为一系列单偏好子问题，并为每个子问题分配专门的专家参数，通过分层路由实现任意偏好权重的动态组合。其核心洞察在于：**无需重训骨干模型，仅通过任务向量分解、模型合并和轻量路由训练即可覆盖完整帕累托前沿**。

### Pipeline 总览

HoE的完整pipeline由四个顺序模块构成，形成“提取—合成—路由—推理”的层次化流程：

1. **LoRA Experts（基础专家层）**：从现成的单目标优化模型中提取任务向量，经task-SVD压缩得到轻量LoRA适配器；再通过模型合并为任意偏好向量合成多目标专家。
2. **Router Experts（路由决策层）**：在每个Transformer块中插入轻量线性路由器，冻结所有LoRA专家，仅训练路由器以学习细粒度的专家选择策略。
3. **Preference Routing（偏好映射层）**：根据用户给定的偏好向量，在偏好空间中选择最近邻专家子集，并计算各专家的投票权重。
4. **Hierarchical Inference Assembly（推理组装）**：推理时依次执行偏好路由、路由器投票、LoRA专家加权组合，输出最终响应。

### 模块关系与数据流

整个框架以**偏好向量 $\lambda$** 作为统一控制信号，贯穿所有模块：

- **输入**：用户提示 $x$ 与偏好向量 $\lambda$（如 $[0.3, 0.7]$ 表示两个目标的权重分配）。
- **LoRA专家生成**：从单目标最优策略 $\pi_i^*$ 中提取任务向量 $\tau_i = \theta_i - \theta_{pre}$，经task-SVD压缩为低秩适配器 $B_i A_i$；给定 $\lambda$ 时，通过模型合并生成多目标专家 $\tau_\lambda = \text{Merge}(\{\tau_i\}_{i\in[N]}, \lambda)$。
- **路由器训练**：冻结LoRA专家后，路由器 $\eta_\lambda$ 通过Tchebyscheff标量化优化：

$$J(\theta|\lambda) = \max_\theta \min_i \{\lambda_i (\mathbb{R}_i(\theta) - z_i^*) \}$$

使策略聚焦于最差目标的改善，避免线性标量化偏向帕累托前沿边缘的偏差。

- **推理时**：偏好路由根据 $\lambda$ 选择Top-K最近邻专家，路由器输出投票权重 $w_j^{(2)}$，最终模块输出为：

$$O(x) = W_{pre} x + \sum_j w_j^{(2)} B_j A_j x$$

仅激活少数轻量专家，推理代价保持为 $1\times$。

### 关键设计决策

Table 1系统对比了HoE与13种基线方法的特性差异，HoE是唯一同时满足以下所有条件的方法：

- **存储成本最低**：仅需存储1个模型（所有偏好通过LoRA专家统一承载），而MORLHF需存储 $M$ 个模型，RS/MOD需存储 $N$ 个。
- **推理代价为 $1\times$**：单次解码仅激活少量专家，而MOD需 $N\times$，PAD需 $3\times$。
- **训练负担最低**：主要免训练，仅路由器需训练约8M参数；对比MORLHF需重训 $M$ 个模型，MODPO需为每个偏好训练独立模型。
- **帕累托可操控**：支持任意偏好权重的连续遍历，而Steering、MetaAligner等方法不具备此能力。
- **可扩展**：新增目标仅需扩展偏好向量维度，无需重训已有专家；而MORLHF、MODPO等方法需完全重训。

该框架将多目标对齐的核心瓶颈——**冲突目标的联合优化**——转化为层次化的专家组合问题，通过分解策略规避了单一模型在任意偏好下无法帕累托最优的根本限制。



HoE 的核心架构由三个层次化组件构成：**LoRA 专家（LoRA Experts）**、**路由器专家（Router Experts）** 和 **偏好路由（Preference Routing）**。其设计目标是将多目标对齐问题分解为一系列单偏好子问题，并通过分层路由实现任意偏好的动态组合，从而突破单一模型无法覆盖完整帕累托前沿的瓶颈。

### 3.1 LoRA 专家：从单目标模型到多目标组合

LoRA 专家是 HoE 的基础适配单元，其构建过程分为两步：单目标专家提取与多目标专家合成。

**单目标最优策略**定义为在给定目标 $i$ 下最大化奖励函数并约束与预训练模型 $\pi_{\text{pre}}$ 的 KL 散度：

$$\pi_i^* = \arg\max_{\pi_\theta} \mathbb{E}_{x\sim D} [\mathbb{R}_i(\theta) - \beta \mathbb{KL}(\pi_\theta || \pi_{\text{pre}})] \tag{1}$$

其中 $\mathbb{R}_i(\theta)$ 为目标 $i$ 的奖励函数，$\beta$ 控制偏离预训练模型的程度。

**任务向量（Task Vector）** 定义为微调后参数 $\theta_i$ 与预训练参数 $\theta_{\text{pre}}$ 的差值：

$$\tau_i = \theta_i - \theta_{\text{pre}} \tag{2}$$

HoE 通过 **task-SVD** 过程将全秩任务向量 $\tau_i$ 压缩为低秩 LoRA 适配器 $B_i A_i$，从而以极少的参数量保留单目标对齐能力。

**LoRA 专家组合输出** 将预训练权重与加权 LoRA 残差结合：

$$O_\lambda(x) = W_{\text{pre}} x + \sum_{i=1}^N \lambda_i B_i (A_i x) \tag{3}$$

其中 $\lambda_i$ 为用户指定的偏好权重，$N$ 为目标数量。

**多目标专家合成** 通过模型合并（Model Merging）为任意偏好向量 $\lambda$ 生成专用专家参数：

$$\tau_\lambda = \mathrm{Merge}(\{\tau_i\}_{i\in[N]}, \lambda) \tag{4}$$

这使得 HoE 无需为每个偏好重新训练模型，仅通过组合现有任务向量即可覆盖连续偏好空间。

### 3.2 路由器专家：细粒度动态选择

路由器专家是插入到每个 Transformer 块中的轻量线性层，负责在 token 级别动态选择激活哪些 LoRA 专家。所有 LoRA 专家参数在路由器训练阶段保持冻结。

路由器专家的优化目标为最大化标量化后的多目标奖励：

$$\eta_\lambda = \arg\max_\eta \mathbb{E}_{y\sim \pi_\eta(\cdot|x)} [R_\lambda(x, y)] \tag{5}$$

HoE 采用 **Tchebycheff 标量化** 替代线性标量化，以保持训练稳定性并完整覆盖帕累托前沿：

$$J(\theta|\lambda) = \max_\theta \min_i \{\lambda_i (\mathbb{R}_i(\theta) - z_i^*) \} \tag{6}$$

其中 $z_i^*$ 为参考点（理想点）。该标量化聚焦于最差目标与参考点的差距，避免线性标量化偏向帕累托前沿边缘的问题。

路由器专家的策略梯度使用 **在线镜像下降（Online Mirror Descent, OMD）** 权重 $w_i$ 加权多目标优势函数：

$$\nabla_\theta J(\theta|\lambda) = \mathbb{E}_{s_t,a_t\sim\pi} \left[\left(\sum_{i=1}^N w_i A_i^{\pi_\theta}(s_t,a_t)\right) \nabla_\theta \log \pi_\theta(a_t|s_t)\right] \tag{8}$$

### 3.3 偏好路由与推理组装

推理阶段，偏好路由根据用户偏好向量在偏好空间中选择最近邻专家子集并计算投票权重。最终 LoRA 组合输出为：

$$O(x) = W_{\text{pre}} x + \sum_j w_j^{(2)} B_j A_j x \tag{11}$$

其中 $w_j^{(2)}$ 为路由器投票后的专家权重。整个推理过程仅需单次解码，仅激活少量轻量专家，推理代价归一化为 $1\times$。

### 关键设计决策的证据支撑

消融实验（Fig. 5）证实了上述设计的有效性：组合 3 个 LoRA 专家与 1 个路由器专家即可实现近乎完整的帕累托前沿覆盖，而仅使用 LoRA 专家覆盖有限；LoRA 秩为 256 即可在性能与效率间取得平衡；Tchebyscheff 标量化相比线性标量化训练更稳定且保持完整前沿覆盖。在五目标对齐中，增加路由器专家数量（1→5）进一步提升多偏好性能（Table 5）。



## 实验与关键发现

### 主结果：二目标对齐的帕累托前沿

HoE 在 HelpAssistant、Reddit Summary 和 BeaverTails 三个任务的二目标对齐中，一致获得了优于基线的帕累托前沿（Fig. 3）。与模型合并基线 RS 和多目标解码基线 MOD 相比，HoE 在所有偏好权重下均实现帕累托支配；与 RiC 相比，在 7 个设置中的 5 个表现更优。这一结果验证了核心洞察：将多目标对齐分解为单偏好子问题，并通过分层专家动态组合，能够突破单一模型无法覆盖完整帕累托前沿的瓶颈。


![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/005_Figure_3.jpg]]
*Figure 3: Results of two-objective alignment on HelpAssistant, Reddit Summary and BeaverTails Task with 10 objectives. Compared to the baselines, HoE consistently achieves superior Pareto frontiers*

### 主结果：三目标对齐

在 Psoups 和 HelpSteer2 数据集上的三目标对齐（Helpful–Harmless–Humor）中，HoE 在 14 个评估设置中的 11 个排名第一（Fig. 4）。与 PAD、RS、RiC、MOD、MetaAligner 等 11 个基线相比，HoE 展现出跨偏好权重的鲁棒优势。GPT-4 评估的胜率进一步确认了定性表现（Fig. 9）：HoE 在 helpfulness、harmlessness 和 humor 三个维度的平均胜率约为 76%，仅次于 PAD 和 MORLHF，但后两者需要显著更高的训练和存储成本。

### 主结果：五目标对齐

在 HelpSteer 的五目标对齐中（Table 2），HoE 在三种偏好权重设置下均取得最高平均分：

![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/011_Table_2.jpg]]
*Table 2: Five-objective alignment results on HelpSteer. Preference weighting settings are shown in gray. The best results are bolded and second best ones are underlined*

- 均匀权重 (0.2, 0.2, 0.2, 0.2, 0.2)：HoE 62.1 vs RS 58.3、RiC 58.5、MOD 58.9（+3.8）
- 偏重 Coherence/Verbosity (0.17, 0.17, 0.17, 0.25, 0.25)：HoE 62.08 vs 基线 58.48（+3.6）
- 进一步偏重 (0.11, 0.11, 0.11, 0.33, 0.33)：HoE 62.1 vs 基线 58.9（+3.2）

HoE 在所有五个子维度（Helpful、Correctness、Coherence、Complexity、Verbosity）上均优于或持平最强基线，证明分层专家架构在多目标场景下的可扩展性。

### 成本分析

Table 3 的系统成本对比揭示了 HoE 的核心效率优势：

![[assets/figures/papers/iclr26_0010_UhmEdfAk46_Multi-objective_Large_Language_Model_Alignment_w/figures/012_Table_3.jpg]]
*Table 3: Comparison of training, storage, and inference costs across different baselines, using Llama-2-7B as the base model aligned on three objectives with the same datasets. Inference cost is normalized to the end-to-end latency of a single decoding pass with one LLM backbone, denoted as 1×; values such as 2× indicate proportionally longer latency. Training cost is reported as wall-clock hours measured on 4×A100-80GB GPUs, where an entry of x $\times$ y denotes y separate training runs with an average cost of x hours each. HoE is designed to reuse off-the-shelf LLMs and is therefore predominantly training-free. However, for completeness, we also report the cost of training three single-objective mo...*

- **训练参数**：仅 8M（路由器专家），远低于 MORLHF（0.16B–0.8B）和 MODPO 等需要重训骨干的方法。
- **存储**：单模型 7.64B 参数统一存储所有偏好，而 MORLHF 需存储 M 个独立模型。
- **推理延迟**：1.23× 单次解码（激活 3 个专家），远优于 Args（>N×）、PAD（3×）和 MetaAligner（2×）。
- **训练时间**：HoE 主要免训练，仅路由器需 3.2h × 2 次运行；若从头训练单目标模型则需额外 13–42h × 5–7 次运行。

### 消融实验

**专家数量与组合**（Fig. 5 Left, Table 4）：仅使用 LoRA 专家（无路由器）时，帕累托前沿覆盖有限；引入 1 个路由器专家后，3 个 LoRA 专家即可接近完整前沿。4 个 LoRA 专家的边际收益递减，验证了“LoRA 专家 + 路由器专家”组合的必要性。Table 4 的三目标消融显示，完整 HoE（4LoRA & 1router）在 HelpSteer2 和 Psoups 上显著优于纯 LoRA 配置。

**LoRA 秩**（Fig. 5 Middle）：秩 256 在性能和效率间取得较好平衡。更大秩持续提升性能，但数学任务对秩更敏感——这提示在涉及推理能力的对齐目标上可能需要更高的秩。

**标量化方法**（Fig. 5 Right）：线性标量化常使策略偏向帕累托前沿边缘，而 Tchebyscheff 标量化保持训练稳定并覆盖完整前沿。这是路由器专家训练的关键设计选择。

**路由器专家数量**（Table 5）：在五目标对齐中，将路由器专家从 1 增至 3 时，所有 6 个偏好设置均有提升；增至 5 个路由器专家时，偏好 4–6 进一步提升（63.5, 63.9, 64.0），但偏好 1–3 趋于饱和。这表明更多路由器专家可提供更细粒度的偏好控制，但存在边际递减。

### 多任务学习

Fig. 7 的雷达图显示，HoE 在 Helpful Assistant、Safety Assistant、Math 和 Summary 四个多任务维度上均达到或超过单目标模型的 100% 归一化性能，优于 LoRAMoE、RS、MOD 等合并方法。这验证了 Table 1 中 HoE 具备多任务能力的声明。

### 泛化性

Table 6 展示了 HoE 在未见数据集 HelpSteer2 和 Psoups 上的三目标对齐结果，性能保持领先。Fig. 8 的三目标帕累托对比进一步确认 HoE 对 RS、MOD 和 RiC 的一致优势。

### 失败模式与局限

1. **对现成单目标模型的依赖**：HoE 假设已有高质量的单目标对齐模型。若不可用，从头训练的成本较高（Table 3 中“from scratch”部分），削弱了“免训练”优势。
2. **模型合并与 SVD 压缩的边界**：在部分场景下，任务向量的 SVD 压缩可能丢失关键信息，模型合并可能无法精确合成目标偏好的专家参数。Table 7 的合并方法对比中，PCB-Merging 优于 Task Arithmetic，但两者均非完美。
3. **极端偏好的覆盖**：Fig. 5 的消融显示，即使完整 HoE 配置，帕累托前沿的极端区域仍可能存在微小间隙，需要更多专家或更精细的路由策略。



## 定位与知识库关联

### 与现有方法的系统对比

Table 1 提供了 HoE 与 13 种对齐方法的七维度系统对比，揭示了当前多目标对齐领域的关键瓶颈：**现有方法在帕累托可操控性、存储开销、推理代价和可扩展性之间难以同时兼顾**。具体而言：

- **MORLHF** 为每个偏好训练独立模型，虽支持帕累托操控，但需存储 $M$ 个模型且新偏好需重训，扩展性最差。
- **MODPO** 和 **RiC** 同样需为每个偏好独立训练，存储 $M$ 个模型，且缺乏多任务能力。
- **RS (Rewarded Soups)** 和 **MOD** 通过线性组合任务向量或 logits 实现零训练开销和可扩展性，但需存储 $N$ 个模型，且 MOD 的推理代价为 $N\times$，多目标场景下不可接受。
- **解码时方法**（Args、GenARM、PARM）虽无需存储模型，但推理代价高达 $>N\times$ 或 $2\times$。
- **Steering**、**MetaAligner**、**LoraMoE**、**PAD** 仅需存储单一模型，但均不支持帕累托操控，即无法根据用户偏好连续调整输出。

HoE 的核心定位在于**填补了“帕累托可操控 + 单模型存储 + $1\times$ 推理代价 + 免重训扩展”这一方法空白**。其关键设计决策是将多目标对齐分解为单偏好子问题，通过分层专家架构实现：

| 特性 | HoE | 最接近的竞争者 |
|------|-----|--------------|
| 训练模型数 | 0（仅训练轻量路由器，8M参数） | RS/MOD: 0；LoraMoE: 1 |
| 存储模型数 | 1 | DPA/LoraMoE/PAD: 1 |
| 推理代价 | $1\times$（实际 $1.23\times$） | MORLHF/RS: $1\times$；MOD: $N\times$ |
| 帕累托可操控 | ✓ | RS/MOD/MORLHF: ✓；LoraMoE/PAD: ✗ |
| 多任务能力 | ✓ | 仅 RS 和 MOD |
| 可扩展性 | 可扩展（新增目标仅扩展偏好向量） | RS/MOD: 可扩展；多数需重训 |

### 适用边界

HoE 的适用性建立在以下前提之上：

1. **现成单目标模型可用**：LoRA 专家的提取依赖已对齐的单目标模型。若无可用的单目标模型，需从头训练，Table 3 显示从头训练三目标模型需 $3.2\text{h}\times 2$ 次运行，成本虽低于多数基线但仍不可忽略。这是方法的核心依赖。
2. **奖励信号可获取**：路由器专家训练使用 Tchebycheff 标量化（Eq. 6），需明确的奖励函数 $\mathbb{R}_i(\theta)$。在纯文本偏好对齐场景（如仅有人类偏好排序而无显式奖励），方法的直接适用性存疑。
3. **目标空间可插值**：多目标 LoRA 专家通过模型合并合成（Eq. 4），隐含假设目标空间在参数层面上是线性可插值的。在高度非凸的目标空间中，插值得到的偏好可能偏离帕累托前沿，Figure 5 (Left) 的消融显示仅 3 个 LoRA 专家 + 1 个路由器即可接近完整前沿，但并未在极端非凸场景下验证。
4. **目标数量适中**：当前验证覆盖 2、3、5 个目标，Table 5 显示路由器专家从 1 增至 5 时性能持续提升，暗示目标数增加可能需要更多路由器专家，扩展规律尚不明确。

### 局限与开放问题

**已识别的局限**：

1. **单目标模型依赖**：方法假设现成的单目标优化模型可用。若不可用，Table 3 的从头训练成本（$3.2\text{h}\times 2$）虽低于 MODPO（$42\text{h}\times 5$）和 MORLHF（$13\text{h}\times 7$），但仍构成实际部署障碍。
2. **模型合并泛化性**：论文在 Table 7 中对比了 Task Arithmetic 与 PCB-Merging，验证了 PCB-Merging 在中文-数学-代码三目标对齐中的优势，但未系统评估合并策略在不同目标组合下的失效模式。SVD 压缩的秩选择（Figure 5 Middle 显示秩 256 足够，但数学任务更敏感）也缺乏跨任务的理论指导。
3. **公平性评估缺失**：论文提示可能包含冒犯性文本用于无害性评估，但未专门讨论数据或模型的公平性偏差，这是对齐研究的常见盲区。

**待解决的开放问题**：

1. **非凸目标空间的前沿保真度**：Eq. 4 的模型合并和 Eq. 11 的 LoRA 组合均基于参数线性插值，在高度非凸的目标空间中，合成专家是否始终保持在帕累托前沿上？Figure 5 的消融仅覆盖有限配置，缺乏理论保证。
2. **大规模目标扩展性**：当目标数量增至数十个时，偏好空间的维度爆炸将导致：(a) 偏好路由的最近邻搜索开销增大；(b) 路由器专家数量需求可能超线性增长。Table 5 仅验证到 5 个路由器，扩展规律未知。
3. **参考点 $z^*$ 的敏感性**：Tchebycheff 标量化（Eq. 6）依赖参考点 $z_i^*$ 的选择。论文未消融不同参考点选择策略对训练稳定性和前沿覆盖的影响。
4. **无奖励信号的扩展**：当前路由器训练依赖显式奖励函数。能否将 HoE 扩展到仅有人类偏好排序的场景（如 DPO 风格的对齐），是一个具有实际价值的方向。
5. **未见数据集的泛化机制**：Table 6 展示了 HoE 在 HelpSteer2 和 Psoups 上的泛化结果，但泛化成功的归因尚不清晰——是源于 LoRA 专家的任务向量保留了通用能力，还是路由器专家的动态选择提供了鲁棒性？



## 原文 PDF

![[paperPDFs/ICLR_2026/Multi_objective_Large_Language_Model_Alignment_with_Hierarchical_Experts.pdf]]
