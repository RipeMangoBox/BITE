---
title: "SegMo: Co-Designing Content-Aware Sparsity and Locally-Cohesive Segment Parallelism for Efficient VLM Inference"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SegMo_Co_Designing_Content_Aware_Sparsity_and_Locally_Cohesive_Segment_Parallelism_for_Efficient_VLM_Inference.pdf
project_link: null
code_link: "https://github.com/LIHAOJUAN/SegMo"
aliases:
- SegMo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于算法-系统协同设计，利用注意力局部凝聚特性，通过内容感知稀疏化（CAS）生成非均匀计算负载以保持精度，同时通过局部凝聚段并行（LSP）消除通信瓶颈以实现高速推理。
primary_logic: VLM 注意力在语义场景内高度凝聚，场景间极度稀疏；查询相关性非均匀，首帧具有自然总结作用。因此可以场景为独立单元进行非均匀稀疏化和无通信并行化，并通过头部帧注入轻量全局上下文来弥补并行化带来的上下文损失。
claims:
- SegMo 通过 CAS 和 LSP 两组件统一优化稀疏化与并行化，打破精度-延迟权衡。
- LSP 利用局部凝聚实现通信免预填充，并通过头部帧注入全局上下文。
- CAS 采用分层策略，先用查询相关性评估场景级重要性，再用时间冗余修剪场景内静态冗余。
- 全系统（CAS+LSP）在 LVBench 等基准上实现最高 12.00% 精度提升和 3.55× 预填充加速，同时维持精度增益。
---

# SegMo: Co-Designing Content-Aware Sparsity and Locally-Cohesive Segment Parallelism for Efficient VLM Inference

> [!tip] 核心洞察
> VLM 注意力在语义场景内高度凝聚，场景间极度稀疏；查询相关性非均匀，首帧具有自然总结作用。因此可以场景为独立单元进行非均匀稀疏化和无通信并行化，并通过头部帧注入轻量全局上下文来弥补并行化带来的上下文损失。

| 字段 | 内容 |
|------|------|
| 中文题名 | SegMo：面向高效视频大语言模型推理的内容感知稀疏性与局部凝聚段并行的协同设计 |
| 英文题名 | SegMo: Co-Designing Content-Aware Sparsity and Locally-Cohesive Segment Parallelism for Efficient VLM Inference |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_SegMo_Co-Designing_Content-Aware_Sparsity_and_Locally-Cohesive_Segment_Parallelism_for_Efficient_CVPR_2026_paper.html) · [Code](https://github.com/LIHAOJUAN/SegMo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SegMo |
| Dataset | LVBench, LongVideoBench |

> [!tip] 效果简介
> - LVBench 上，Accuracy Gain SegMo (CAS+LSP) vs Uniform Sampling + 2-GPU DP (+2.95% ~ +12.00%)。
> - LVBench (32 frames) 上，TTFT Speedup SegMo (CAS+LSP) vs Baseline (2.83×)。
> - LVBench (64 frames) 上，TTFT Speedup SegMo (CAS+LSP) vs Baseline (3.43×)。

## 概述

长视频理解任务中，视觉大语言模型（VLM）需处理海量视觉 token，其自注意力机制的 $O(N^2)$ Prefill 计算成本随视频长度急剧膨胀，形成难以逾越的推理延迟墙。现有方案或通过均匀采样牺牲精度换取速度，或依赖全量通信的模型并行引入高昂延迟，陷入精度与延迟的刚性权衡。

SegMo 提出了一种**算法-系统协同设计**方法论，从 VLM 注意力的内在结构切入，打破上述权衡。其核心洞察在于：VLM 的注意力在语义场景内高度凝聚（强对角块），场景间极度稀疏；同时，查询相关性在场景间非均匀分布，且每个场景的首帧具有天然的全局摘要作用。基于此，SegMo 统一了两项关键机制：

- **内容感知稀疏化（Content-Aware Sparsification, CAS）**：在 CPU 端以查询相关性与时间冗余为双重度量，为每个场景分配非均匀的帧预算——关键场景保留更多帧，静态场景大幅压缩，从而在压缩 token 总量的同时保持精度。
- **局部凝聚段并行（Locally-Cohesive Segment Parallelism, LSP）**：在 GPU 端以场景边界为分片依据，将同一场景的所有帧协同放置于单 GPU，消除 Prefill 阶段的跨 GPU 通信；并通过头部帧注入轻量全局上下文，弥补并行化带来的跨场景信息损失。

两组件协同工作：CAS 生成的非均匀计算负载由 LSP 的硬件感知贪心分片算法均衡分配，CPU 预处理与 GPU 计算通过生产者-消费者流水线重叠，隐藏预处理延迟。

在两个 VLM 模型（MiniCPM-o 2.6、Qwen2-VL-7B-Instruct）与三个长视频基准（LVBench、LongVideoBench、Video-MME）上的实验表明，SegMo 同时实现了**最高 12.00% 的精度提升**与**最高 3.55× 的 Prefill 加速**，在全系统集成下仍保持最高 8.31% 的精度增益，验证了协同设计在打破精度-延迟权衡上的有效性。

> **方法定位**：SegMo 属于推理系统层面的稀疏化-并行化联合优化方法，与单纯基于 token 剪枝或传统张量并行的方案正交，可视为对现有 VLM 推理栈的即插即用增强。其场景感知的稀疏化策略与 **MPGD**（He et al., CVPR 2023）等基于均匀采样的方案形成对比，而通信免并行的设计则区别于依赖全局 KV Cache 共享的全量并行方案。

## 背景与动机

### 长视频 VLM 推理的性能墙

视频大语言模型（Video LLM）通过将长视频编码为大量视觉 token 来理解时序内容，但这一范式带来了根本性的计算瓶颈：视觉 token 数量随视频长度线性增长，而标准 Transformer 自注意力的 Prefill 阶段计算复杂度为 $O(N^2)$。当输入视频长达数十分钟甚至数小时时，单次推理的 Prefill 延迟变得无法承受。这一**视觉 token 爆炸**问题构成了当前长视频 VLM 推理的性能墙，使模型在真实部署场景中难以满足延迟要求。

### 现有加速方法的精度-延迟权衡困境

为缓解上述瓶颈，已有研究主要沿两条路径展开：

- **稀疏化采样**：通过均匀采样或基于简单启发式的关键帧选择来减少输入帧数，从而降低 Prefill 计算量。这类方法虽然降低了延迟，但因忽略视频内容的语义结构和查询相关性，往往丢弃了关键信息，导致精度显著下降。
- **并行化推理**：利用多 GPU 进行张量并行或序列并行来加速计算。然而，标准并行策略需要全局的 all-to-all 注意力通信，在长序列场景下通信开销巨大，抵消了并行带来的计算收益。

这两类方法存在根本性的**精度-延迟权衡**：稀疏化以精度为代价换延迟，而并行化因通信瓶颈难以有效降低延迟。现有工作缺乏将两者协同优化的系统化方法论。

### 关键洞察：注意力局部凝聚与查询相关性的非均匀性

SegMo 的核心动机源自对 VLM 注意力模式的四项实证观察（见 Figure 2–4）：

1. **场景内凝聚（Intra-Scene Cohesion）**：VLM 的注意力矩阵在语义场景边界内形成强对角块，同一场景内的帧之间注意力高度集中。
2. **场景间稀疏（Inter-Scene Sparsity）**：不同场景之间的注意力信号极弱，几乎可以忽略。这意味着场景是天然的独立计算单元。
3. **查询相关性非均匀（Non-Uniform Query Relevance）**：用户查询仅与视频中少数几个场景高度相关（Top-5 场景即可覆盖绝大部分相关注意力），而非均匀分布。
4. **首帧偏向（Head-Frame Bias）**：每个场景的首帧获得显著更高的注意力分数，表明首帧具有自然的总结作用，可作为场景的轻量级代表。

这些观察揭示了两个可被利用的结构特性：**局部凝聚**（场景内密集、场景间稀疏）和**查询相关性的非均匀分布**。前者为无通信并行化提供了可能，后者为内容感知的非均匀稀疏化提供了依据。

### 本文动机与设计目标

基于上述洞察，SegMo 提出一种**算法-系统协同设计**方法论，目标是在保持甚至提升精度的前提下显著降低 Prefill 延迟。具体而言，系统通过两个协同组件实现这一目标：

- **内容感知稀疏化（Content-Aware Sparsification, CAS）**：利用查询相关性和时间冗余度对场景进行非均匀帧预算分配，将有限的计算资源集中在信息密度最高的帧上。
- **局部凝聚段并行（Locally-Cohesive Segment Parallelism, LSP）**：以场景边界为分片依据，将同一场景的所有帧协同放置在同一 GPU 上，消除 Prefill 阶段的跨 GPU 通信；同时通过首帧注入轻量级全局上下文，弥补并行化带来的跨场景信息损失。

通过将稀疏化和并行化统一在一个优化框架下，SegMo 旨在打破现有方法普遍存在的精度-延迟权衡困境。

## 核心创新

SegMo 的核心创新在于**算法-系统协同设计**：它不是孤立地优化稀疏化或并行化，而是通过两个深度耦合的组件——内容感知稀疏化（CAS）与局部凝聚段并行（LSP）——统一解决长视频 VLM 推理中精度与延迟的“跷跷板”困境。

### 创新一：内容感知的帧预算非均匀分配（CAS）

传统视频 VLM 推理采用均匀采样（如每段按长度比例分配帧数），忽略了不同场景对查询的信息贡献差异。SegMo 将帧采样策略从一个**均匀分配**问题转变为一个**信息价值驱动的非均匀预算分配**问题。

其核心机制是一个轻量级的分层评估算法：

1. **查询相关性评估（Query Relevance, RL）**：利用 CLIP 模型计算用户查询与各场景的语义相似度，识别对回答问题最关键的场景。实验观察表明，VLM 的注意力高度集中于少数相关场景（Figure 3），这为按需分配帧预算提供了依据。

2. **时间冗余评估（Temporal Redundancy, RD）**：通过帧间灰度差异检测场景内的静态程度，对视觉变化缓慢的场景减少采样，避免冗余计算。

3. **信息价值融合**：通过加权函数 $V(Q, C_k) = w \cdot \operatorname{RL}(Q, C_k) + (1-w) \cdot \operatorname{RD}(C_k)$ 将两者统一为场景的信息价值分数，并据此按比例分配帧预算（$m_k$）。权重 $w=0.5$ 在 LongVideoBench 和 Video-MME 上取得最佳精度（Table 3）。

这一设计的关键洞察在于：**CAS 在 CPU 端完成，不占用 GPU 计算资源**，且其输出（非均匀帧预算）直接为下游并行化提供负载感知的输入。

### 创新二：局部凝聚段并行与通信免预填充（LSP）

传统多 GPU 推理依赖张量并行或序列并行，需要在 Prefill 阶段进行全局 all-to-all 通信，通信开销随序列长度呈 $O(N^2)$ 增长。SegMo 的 LSP 策略从根本上改变了并行范式：

1. **场景边界分区**：利用 VLM 注意力在场景内高度凝聚、场景间极度稀疏的实证发现（Figure 2），将视频在场景边界处切分，每个场景的所有帧完整地分配至单一 GPU。这**消除了 Prefill 阶段的所有跨 GPU 通信**——这是延迟降低的核心来源。

2. **硬件感知的贪婪分区**：由于 CAS 产生的各场景帧预算 $m_k$ 是非均匀的，SegMo 采用动态贪婪算法求解 makespan 最小化目标 $\operatorname*{min}_{\pi, \{m_k\}} \max_{j} \left( \frac{\sum_{C_k \in P_j} W(C_k)}{Cap(g_j)} \right)$，在满足 GPU 显存约束下平衡各卡负载。

3. **头部帧全局上下文注入（GCI）**：并行化带来的上下文损失通过一个轻量级机制弥补——利用“场景首帧获得更高注意力”（Figure 4）的观察，从信息价值最高的 $\log_2 M$ 个场景中提取首帧，构建压缩的全局上下文序列注入每个 GPU。消融实验表明，GCI 将 LongVideoBench 整体准确率提升 1.37%，其中时间推理子任务（T2A）提升达 10.71%（Table 4）。

### 创新三：CPU-GPU 流水线协同

CAS 在 CPU 上运行，LSP 在 GPU 上运行，两者通过生产者-消费者流水线重叠执行（Figure 7）：当前请求的 GPU 计算与下一请求的 CPU 预处理并行，隐藏了 CAS 的预处理延迟。这使得端到端吞吐不受 CPU 预处理瓶颈的限制。

### 与 Baseline 的本质差异

| 设计维度 | Baseline（均匀采样 + 2-GPU 数据并行） | SegMo |
|---------|--------------------------------------|-------|
| 帧采样策略 | 均匀分配，忽略查询内容 | 查询相关性与时间冗余驱动的非均匀分配 |
| 并行策略 | 数据并行，需通信 | 场景边界分区，Prefill 零通信 |
| 负载均衡 | 静态均匀划分 | 硬件感知动态贪婪分区 |
| 全局上下文 | 全量 KV Cache 共享（通信重） | 头部帧压缩注入（轻量） |

这一系列 changed slots 的协同效应体现在：CAS 的非均匀帧分配天然适配 LSP 的场景级并行粒度，而 LSP 的通信免预填充特性使 CAS 的精度增益不因并行化而被延迟代价抵消。最终系统在 LVBench 上实现最高 12.00% 精度提升，同时达到 3.55× 的 Prefill 加速（Table 1, Table 2），打破了精度-延迟的固有权衡。

## 整体框架

SegMo 的推理流水线遵循**算法-系统协同设计**原则，将视频大语言模型（VLM）的长视频推理拆分为两个解耦的物理域：CPU 端的**内容感知稀疏化（Content-Aware Sparsification, CAS）** 与 GPU 端的**局部凝聚段并行（Locally-Cohesive Segment Parallelism, LSP）**，二者通过多线程生产者-消费者流水线重叠执行，以隐藏 CPU 预处理延迟（Figure 5, Figure 6）。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/004_Figure_5.jpg]]
*Figure 5: The SegMo System Architecture. Our system is composed of two co-designed core components (Sparsification and Parallelism) and a system optimization layer*

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/005_Figure_6.jpg]]
*Figure 6: The end-to-end inference pipeline of SegMo. Note that the CAS module running on CPU (covering step 1, 2, and 3) is pipelined with the LSP module running on GPU (covering step 4) to maximize the serving throughput and hide the CPU pre-processing latency*

### 端到端流水线

整个推理过程由四个顺序步骤构成，其中前三步在 CPU 上运行，第四步在 GPU 上并行执行（Figure 6）：

1. **结构分解（Structural Decomposition）**：将输入视频 $V$ 切分为 $K$ 个语义场景 $\mathcal{C} = \{C_1, \dots, C_K\}$。场景检测基于内容变化边界，使每个 $C_k$ 内部具有强注意力凝聚性，而场景间注意力极弱（Figure 2）。
2. **层次化信息价值评估（Hierarchical Information Value Assessment）**：对每个场景 $C_k$，分别计算其与用户查询 $Q$ 的**查询相关性（Query Relevance, RL）** 和场景内部的**时间冗余度（Temporal Redundancy, RD）**，并通过加权组合得到场景的信息价值：
   $$V(Q, C_k) = w \cdot \operatorname{RL}(Q, C_k) + (1-w) \cdot \operatorname{RD}(C_k)$$
   其中 RL 利用 CLIP 相似度衡量场景与查询的语义匹配程度（Figure 3），RD 通过帧间灰度差异量化场景内的静态程度。
3. **内容感知帧预算分配（Content-Aware Frame Budget Allocation）**：在总帧数上限 $M_{max}$ 约束下，根据 $V(Q, C_k)$ 按比例向各场景分配非均匀的帧预算 $m_k$，使高信息价值场景获得更多采样帧，低价值或高冗余场景获得更少帧。
4. **硬件感知动态分区与并行预填充（Hardware-Aware Dynamic Partitioning & Parallel Prefill）**：LSP 模块在场景边界处对视频进行分区，将每个分区的所有帧**共置在同一 GPU 上**，消除 Prefill 阶段的跨 GPU 通信。分区策略通过贪心算法求解 makespan 最小化目标：
   $$\operatorname*{min}_{\pi, \{m_k\}} \max_{j=1,\ldots,N} \left( \frac{\sum_{C_k \in P_j} W(C_k)}{Cap(g_j)} \right)$$
   同时，LSP 利用**头部帧优先（Head-Frame Primacy）** 洞察（Figure 4），从 Top-$\log_2 M$ 个场景中选取首帧构建轻量全局上下文映射，注入每个 GPU 的局部注意力计算中，以弥补场景隔离带来的跨场景上下文损失。Prefill 完成后，各 GPU 的局部 KV 缓存被聚合用于自回归解码阶段。

### 系统优化层

为最大化服务吞吐，SegMo 引入系统优化调度器（Figure 7），将 CPU 上的 CAS 预处理（步骤 1–3）与 GPU 上的 LSP 计算（步骤 4）构建为**多线程生产者-消费者流水线**：当前请求在 GPU 上执行 Prefill 时，CPU 线程同步处理下一个请求的场景检测与帧预算分配，从而完全隐藏 CAS 的预处理延迟。

### 输入输出流

- **输入**：原始长视频 $V$、用户文本查询 $Q$、总帧数预算 $M_{max}$、可用 GPU 数量 $N$ 及其计算能力 $Cap(g_j)$。
- **输出**：VLM 对查询 $Q$ 的文本回答。
- **中间产物**：CAS 输出的非均匀关键帧集合（各场景 $m_k$ 帧）及场景分区方案 $\pi = \{P_1, \dots, P_N\}$；LSP 输出的聚合 KV 缓存用于解码阶段。

### 补充图表

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/001_Figure_1.jpg]]
*Figure 1: SegMo unifies CAS (Accuracy) and LSP (Latency) to break the Accuracy-Latency Trade-off. The system utilizes Local Cohesion for communication-free parallelism. Validated on longvideo benchmarks, SegMo achieves a peak accuracy and prefill acceleration gains of 12.00% and 3.55×, respectively*

## 核心模块与公式推导

### 问题形式化

SegMo 将长视频 VLM 推理建模为一个 **makespan 最小化问题**。给定一段视频被切分为 $K$ 个场景 $\mathcal{C} = \{C_1, C_2, \ldots, C_K\}$，系统需在 $N$ 个 GPU 上分配这些场景，并为每个场景 $C_k$ 确定采样帧数 $m_k$。目标是在总帧数约束下，最小化最繁忙 GPU 的计算时间。

GPU $j$ 上分配的分区 $P_j$ 的计算负载定义为：

$$W(P_j) = \sum_{C_k \in P_j} W(C_k) = \sum_{C_k \in P_j} (\alpha \cdot m_k) \quad \text{(Eq. 1)}$$

其中 $\alpha$ 为每帧计算量系数。端到端延迟近似为各 GPU 计算时间与聚合开销的 makespan：

$$L_{e2e} \approx \max_{j=1,\dots,N} \left( \frac{\sum_{C_k \in P_j} W(C_k)}{Cap(g_j)} \right) + T_{agg} \quad \text{(Eq. 2)}$$

其中 $Cap(g_j)$ 为 GPU $j$ 的计算能力，$T_{agg}$ 为 KV 缓存聚合开销。由此得到核心优化目标：

$$\operatorname*{min}_{\pi, \{m_k\}} \max_{j=1,\ldots,N} \left( \frac{\sum_{C_k \in P_j} W(C_k)}{Cap(g_j)} \right) \quad \text{(Eq. 3)}$$

$$\text{s.t.}\quad \sum_{k=1}^K m_k \leq M_{max},\quad \bigsqcup_{j=1}^N P_j = \mathcal{C} \quad \text{(Eq. 4)}$$

其中 $\pi = \{P_1, \ldots, P_N\}$ 为场景分区方案，$M_{max}$ 为最大采样帧数上限。该问题的核心挑战在于：**帧预算分配 $\{m_k\}$ 影响精度，场景分区 $\pi$ 影响并行负载均衡，两者耦合且需协同优化**。

### 核心模块一：内容感知稀疏化（CAS）

CAS 模块运行在 CPU 端，通过分层评估为每个场景分配非均匀帧预算，在保持精度的前提下压缩视觉 token 数量。其核心设计基于两个互补的度量维度。

**信息价值函数。** 对于用户查询 $Q$ 和场景 $C_k$，定义信息价值为查询相关性（Relevance, RL）和时间冗余（Redundancy, RD）的加权组合：

$$V(Q, C_k) = w \cdot \operatorname{RL}(Q, C_k) + (1-w) \cdot \operatorname{RD}(C_k) \quad \text{(Eq. 5)}$$

其中 $w \in [0,1]$ 为平衡因子（消融实验表明 $w=0.5$ 在 LongVideoBench 和 Video-MME 上获得最佳精度）。该公式的直觉是：**高查询相关性场景值得保留更多帧以捕捉细节，而高时间冗余场景可被激进压缩而不损失信息**。

**查询相关性度量。** 原始相关性分数通过 CLIP 模型计算查询文本与场景帧的相似度得到，随后归一化为概率分布：

$$RL(Q, C_k) = \frac{RL'(Q, C_k) - \min_k RL'(Q, C_k)}{\sum_{k=1}^K \{RL'(Q, C_k) - \min_k RL'(Q, C_k)\}} \quad \text{(Eq. 6)}$$

其中 $RL'(Q, C_k)$ 为原始 CLIP 相似度分数。归一化确保了帧预算分配的比例性——相关性越高的场景获得越多的采样配额。

**时间冗余度量。** 基于场景内帧间灰度差异统计，量化视觉内容的静态程度。高冗余场景（如静止对话镜头）即使查询相关，也无需保留过多帧。

CAS 的三步流水线为：(1) 使用 PySceneDetect 进行结构分解，将视频切分为语义场景；(2) 逐场景计算 $RL$ 和 $RD$，得到信息价值 $V(Q, C_k)$；(3) 按 $V(Q, C_k)$ 比例分配帧预算 $m_k$。该过程与 GPU 端的 LSP 模块通过生产者-消费者流水线重叠执行，隐藏 CPU 预处理延迟。

### 核心模块二：局部凝聚段并行（LSP）

LSP 模块运行在 GPU 端，利用 VLM 注意力的局部凝聚特性实现通信免预填充并行。其关键洞察来自实证观察：**VLM 注意力在场景内形成强对角块，场景间注意力极弱**（Figure 2）。这意味着将同一场景的所有帧协同定位在同一 GPU 上，场景边界处几乎不需要跨 GPU 通信。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/003_Figure_2.jpg]]
*Figure 2: Intra-Scene Cohesion: Strong diagonal blocks (high intra-scene attention) and negligible inter-scene attention*

**硬件感知贪婪分区。** 给定 CAS 输出的非均匀帧预算 $\{m_k\}$，LSP 采用贪婪算法近似求解 Eq. 3 的 makespan 最小化问题。算法在满足各 GPU 显存容量的前提下，按场景顺序将帧分配到当前负载最小的 GPU，动态平衡各 GPU 的计算负载。

**全局上下文注入（GCI）。** 场景级并行化虽然消除了 Prefill 阶段的通信，但也切断了跨场景的全局上下文。LSP 利用"头部帧优先"洞察（Figure 4：每场景首帧获得更高注意力分数）来弥补这一损失：从信息价值最高的 $\log_2 M$ 个场景中各取首帧，构建轻量全局上下文序列注入到每个 GPU 的输入中。这一设计以极小的计算开销（仅增加数个 token）替代了传统方法中庞大的 KV 缓存共享或全对全注意力通信。消融实验表明，GCI 将 LongVideoBench 整体准确率从 48.46% 提升至 49.83%（+1.37%），其中时序动作理解（T2A）准确率提升达 10.71%（Table 4）。

**系统优化层。** 多线程生产者-消费者流水线将 CPU 端的 CAS 预处理与 GPU 端的 LSP 推理重叠：当前请求在 GPU 上执行 Prefill 时，下一请求的场景检测和帧预算计算已在 CPU 上并行进行（Figure 7），有效隐藏了预处理延迟，提升服务吞吐。

### 补充图表

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/002_Figure_3.jpg]]
*Figure 3: Non-Uniform VLM Attention: Highlighted Top-5 relevant scenes (e.g., 1, 7, 8, 10, 16) motivate the Relevance metric*

## 实验与分析

### 实验设置

实验在 2 张 NVIDIA H100 GPU（NVLink 互联）上开展，评估模型包括 **MiniCPM-o 2.6 (8B)** 和 **Qwen2-VL-7B-Instruct**。基线采用均匀采样 + 2-GPU 数据并行（Uniform Sampling + 2-GPU DP）方案。评测基准涵盖 LVBench、LongVideoBench 和 Video-MME 三个长视频问答数据集，指标同时报告准确率增益和首 token 延迟（TTFT）加速比。

### 主实验结果

#### 精度提升

Table 1 汇总了 SegMo 在三个基准上的 VideoQA 准确率。CAS 模块单独启用（配合 2-GPU 数据并行）时，在 LVBench 上相对基线实现 **2.95% 至 12.00%** 的精度增益。全系统（CAS + LSP）在保持显著精度优势（最高 +8.31%）的同时，进一步释放并行加速潜力。CAS 的核心优势在于其层次化采样策略能够跨越视觉冗余，高效保留与查询最相关的帧信息——这一能力在涉及长视频跨场景推理的 LVBench 上尤为突出。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/007_Table_1.jpg]]
*Table 1: Video Question Answering (VideoQA) accuracy results of SegMo compared to the baseline with two VLMs on three benchmarks*

#### 延迟加速

Table 2 报告了 Qwen2-VL-7B-Instruct 模型下的 TTFT 加速比。在 LVBench 上，32 帧配置下 SegMo 实现 **2.83×** 加速，64 帧配置下提升至 **3.43×**；在 LongVideoBench 上，32 帧和 64 帧配置分别达到 **3.55×** 和 **3.38×** 加速。加速比随帧数增加而提升的趋势，验证了 LSP 通过场景边界划分消除 Prefill 阶段跨 GPU 通信的设计有效性——帧数越多，通信开销的节省越显著。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/008_Table_2.jpg]]
*Table 2: Latency results of SegMo (CAS+LSP) compared to the baseline with Qwen2-VL-7B-Inst model on two benchmarks*

### 消融实验

#### 信息价值权重 w

Table 3 探究了公式 (5) 中平衡查询相关性（RL）和时间冗余（RD）的权重 w 对精度的影响。结果表明 **w=0.5** 在 LongVideoBench（51.83%）和 Video-MME（69.00%）上均取得最佳精度，验证了两类信号同等重要的设计假设。极端取值（w=0 仅用冗余，w=1 仅用相关性）均导致精度下降，说明单一信号无法充分刻画场景的信息价值。

#### 全局上下文注入

Table 4 验证了 LSP 中全局上下文注入（GCI）机制的贡献。启用 GCI 后，LongVideoBench 整体准确率从 48.46% 提升至 49.83%（**+1.37%**），其中时间到动作（T2A）子任务准确率提升高达 **+10.71%**。这一结果证实了头部帧作为轻量全局映射的有效性：仅选取 top log₂M 个场景的首帧，即可部分弥补场景并行化带来的跨段上下文损失，且几乎不引入额外通信开销。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/009_Table_4.jpg]]
*Table 4: Accuracy results with and without Global Context Injection (GCI) with Qwen2-VL-7B-Inst model on LongVideoBench*

### 系统优化效果

Figure 7 展示了 SegMo 的多线程生产者-消费者流水线设计。CAS 模块运行在 CPU 端（场景分解、信息价值评估、帧预算分配），LSP 模块运行在 GPU 端（硬件感知分片、通信免预填充、KV 缓存聚合）。通过将下一个请求的 CPU 预处理与当前请求的 GPU 计算重叠，系统有效隐藏了 CAS 的预处理延迟，最大化服务吞吐。

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/006_Figure_7.jpg]]
*Figure 7: System optimizations for hiding CPU pre-processing time consumed by the proposed CAS module. The pipeline overlaps CPU pre-processing for the next request with the GPU computation for the current request*

### 公平性与局限性说明

当前实验仅在 **2 张 H100 GPU** 配置下验证，且限于两个 VLM 模型。SegMo 在更多 GPU 规模（如 4/8 卡）或不同互联拓扑（如 PCIe）下的扩展效率，以及在其他 video-LLM 任务（如 dense captioning、temporal grounding）上的适用性，有待进一步验证。此外，CAS 依赖 CLIP 相似度和手工灰度差异特征，其端到端可学习性仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l782_https_openaccess_thecvf_com_content_CVPR2026_html_Li_SegMo_Co_Designing/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative visualization*

## 方法谱系与知识库定位

### 问题定位：长视频 VLM 推理的精度-延迟权衡

长视频理解任务中，视觉 token 数量随视频时长线性增长，导致 Transformer 的 Prefill 阶段计算复杂度呈 $O(N^2)$ 膨胀，形成性能墙。现有加速方案主要分为两条技术路线：**稀疏化采样**（如均匀采样、关键帧提取）和**并行化推理**（如张量并行、序列并行）。然而，这两类方法长期处于割裂状态——稀疏化方法在降低计算量的同时可能丢失关键信息，并行化方法则面临跨 GPU 通信瓶颈，且两者缺乏协同优化，导致精度与延迟之间形成难以调和的权衡。

SegMo 的核心定位是**首次将内容感知稀疏化与局部凝聚段并行进行算法-系统协同设计**，从注意力机制的局部凝聚特性出发，统一解决精度与延迟的矛盾。其方法论根基建立在四个关键实证洞察之上：(1) VLM 注意力在场景内高度凝聚，场景间极度稀疏（见图 2 的对角块模式）；(2) 查询相关性在场景间呈非均匀分布，少数场景承载了绝大部分与查询相关的信息（见图 3）；(3) 每个场景的首帧自然获得更高注意力分数，具备全局摘要能力（见图 4）；(4) 场景边界可作为并行化的天然分割点，消除跨 GPU 通信。

### 与现有稀疏化方法的谱系关系

在帧采样策略维度，现有工作普遍采用**均匀采样**或**基于启发式的关键帧选择**。均匀采样按视频长度等比例分配帧预算（$m_k \propto |C_k|$），完全忽略内容的语义差异，导致信息密度低的场景浪费帧预算，而关键场景采样不足。SegMo 的 CAS 模块通过引入**信息价值函数** $V(Q, C_k) = w \cdot \operatorname{RL}(Q, C_k) + (1-w) \cdot \operatorname{RD}(C_k)$，将帧预算分配建模为查询相关性（RL）与时间冗余（RD）的加权优化问题，实现了非均匀的、内容感知的帧预算分配。这一设计的本质是将采样决策从“均匀覆盖”转变为“信息密度导向”，使得有限帧预算聚焦于对查询最有价值的视觉内容。

CAS 的分层设计也区别于传统方法：先以场景为粗粒度单元评估全局重要性，再在场景内部基于时间冗余进行细粒度修剪。这种“先选场景，再选帧”的策略有效避免了全局均匀采样的信息稀释问题，同时保持了计算轻量性（仅依赖 CLIP 相似度和灰度差异等手工特征）。

### 与现有并行化方法的谱系关系

在并行化策略维度，现有方案主要包括**数据并行**（DP）、**张量并行**（TP）和**序列并行**（SP）。数据并行虽无通信开销，但无法降低单卡的计算负载；张量并行和序列并行虽能分摊计算，但引入大量 all-to-all 通信，在 Prefill 阶段尤为昂贵。SegMo 的 LSP 模块提出了一种**通信免预填充**的并行范式：利用注意力局部凝聚特性，将同一场景的所有帧协同定位到单张 GPU 上，以场景边界作为分区点，使得 Prefill 阶段各 GPU 的计算完全独立，无需任何跨 GPU 通信。这一设计的理论依据是：场景内注意力密集（需要完整 KV Cache），场景间注意力稀疏（可近似为零），因此按场景边界切割不会引入显著的精度损失。

为弥补并行化带来的全局上下文损失，LSP 引入了**头部帧全局上下文注入**（GCI）机制：选取信息价值最高的前 $\log_2 M$ 个场景的首帧，构建轻量级全局映射序列注入各 GPU，替代传统方案中庞大的全量 KV Cache 共享。这一设计直接源于“首帧具有自然摘要作用”的实证洞察，以极低的额外开销恢复了跨场景的上下文关联。

### 系统层面的协同设计

SegMo 的方法论贡献不仅在于稀疏化和并行化的独立创新，更在于两者的**协同优化**。CAS 输出的非均匀帧预算直接决定了各场景的计算负载，LSP 的硬件感知贪婪分区算法据此进行 GPU 负载均衡，最小化 makespan 目标函数 $\min_{\pi, \{m_k\}} \max_{j=1,\ldots,N} \left( \frac{\sum_{C_k \in P_j} W(C_k)}{Cap(g_j)} \right)$。此外，系统优化层通过多线程生产者-消费者流水线，将 CPU 端的 CAS 预处理与 GPU 端的 LSP 计算重叠执行，隐藏了预处理延迟（见图 7）。

### 适用边界与局限

**适用场景**：SegMo 的方法设计高度依赖“场景内凝聚、场景间稀疏”的注意力特性，因此最适用于**具有明确场景边界的叙事性长视频**（如电影、纪录片、教学视频）。对于注意力分布更均匀的视频类型（如监控视频、体育直播），场景切分的有效性可能下降，需要手动验证。

**硬件约束**：当前实验仅在 2 张 H100 GPU（NVLink 互联）上验证，更多 GPU 规模（如 4/8 卡）或不同互联拓扑（如 PCIe）下的扩展效率有待进一步验证。LSP 的通信免预填充优势在 NVLink 环境下可能不如在低带宽互联环境下显著。

**特征依赖**：CAS 依赖 CLIP 嵌入和手工设计的灰度差异特征进行查询相关性和时间冗余评估，这些特征虽轻量但可能无法捕获复杂的语义关系。是否可通过端到端学习的方式优化信息价值评估，是一个开放问题。

**全局上下文完整性**：GCI 仅使用头部帧作为全局映射，可能遗漏需要跨场景密集推理的任务（如跨场景人物关系推理、长时序因果链分析）。对于此类任务，轻量级全局上下文可能不足以替代完整的跨场景注意力。

**任务泛化性**：当前验证集中在视频问答（VideoQA）任务上，方法对视频描述生成（captioning）、视频定位（grounding）等其他 video-LLM 应用的适用性尚未得到实验检验。

## 原文 PDF

![[paperPDFs/CVPR_2026/SegMo_Co_Designing_Content_Aware_Sparsity_and_Locally_Cohesive_Segment_Parallelism_for_Efficient_VLM_Inference.pdf]]
