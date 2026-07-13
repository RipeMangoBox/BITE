---
title: "ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ThinKV_Thought_Adaptive_KV_Cache_Compression_for_Efficient_Reasoning_Models.pdf
project_link: null
code_link: null
openreview_forum_id: M3CeHnZKNC
aliases:
- ThinKV
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "利用注意力稀疏性动态识别思维类型（推理、执行、过渡），根据思维重要性差异化分配量化精度和主动淘汰，消除token级启发式方法造成的关键信息意外丢失。"
primary_logic: "思维链可以分解为三种类型：推理（R）、执行（E）和过渡（T），其中过渡思维虽不直接贡献答案，却改变推理轨迹，若被完全消除会引发无限循环。注意力稀疏性自然地暴露了这些类型，并使系统能够针对性地进行压缩。"
claims:
- "注意力稀疏性在解码步上呈现三模态分布，对应推理、执行和过渡三种思维。"
- "思维类型的反事实重要性为 R > E > T，且存在异常重要的过渡思维。"
- "过渡思维的出现会削弱先前所有思维段的影响力，从而允许逐步淘汰。"
- "在1024 token预算下，ThinKV以低于3.67% full KV存储实现近无损精度，吞吐量提升最高达5.8倍。"
---

# ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models

> [!tip] 核心洞察
> 思维链可以分解为三种类型：推理（R）、执行（E）和过渡（T），其中过渡思维虽不直接贡献答案，却改变推理轨迹，若被完全消除会引发无限循环。注意力稀疏性自然地暴露了这些类型，并使系统能够针对性地进行压缩。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ThinKV：面向高效推理模型的思维自适应KV缓存压缩 |
| 英文题名 | ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=M3CeHnZKNC) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | ThinKV |
| Dataset | AIME (R1-Qwen-14B), LiveCodeBench (R1-Qwen-14B), A100 throughput (R1-Llama-8B, 32K gen), 2048 budget) |

> [!tip] 效果简介
> - AIME (R1-Qwen-14B) 上，pass@1 accuracy 为 50.00 (k=1024)，对比 53.33 (FullKV 16-bit)，变化 -3.33。
> - LiveCodeBench (R1-Qwen-14B) 上，pass@1 accuracy 为 45.84 (k=1024)，对比 47.90 (FullKV 16-bit)，变化 -2.06。
> - A100 throughput (R1-Llama-8B, 32K gen) 上，Throughput (tokens/s) 为 8412.2，对比 1450.5 (R-KV seq)，变化 5.8×。

## 概要

大型推理模型（LRM）在生成长思维链时，KV缓存随输出长度线性膨胀，迅速耗尽GPU显存，成为长推理任务部署的核心瓶颈。现有压缩方法或依赖token级注意力分数的启发式淘汰（如**H2O**、**R-KV**、**LazyEviction**），或采用统一量化策略（如**KIVI**、**PM-KVQ**），均忽视了思维链内部的推理动态结构，导致在保持精度与实现高压缩比之间难以兼顾。

ThinKV的核心洞察在于：思维链可被分解为三种功能类型——推理（R）、执行（E）和过渡（T），其中过渡思维虽不直接贡献最终答案，却改变推理轨迹，若被完全消除可能引发模型陷入无限循环。注意力稀疏性在解码步上呈现三模态分布（Figure 3），自然地暴露了这些思维类型，使系统能够针对性地进行差异化压缩。

基于此，ThinKV提出思维自适应的混合压缩框架，包含四个关键模块：（1）**Thought Decomposition**，通过离线校准与在线检测动态识别思维类型；（2）**TBQ**（Think Before You Quantize），根据思维重要性分配差异化量化精度；（3）**TBE**（Think Before You Evict），利用过渡思维的出现触发段粒度的渐进式淘汰；（4）**Continuous Thinking kernel**，扩展PagedAttention实现就地槽位复用，消除传统gather压缩带来的吞吐下降。

实验表明，ThinKV在仅使用不到3.67%原始KV缓存存储的条件下，在AIME和LiveCodeBench等推理基准上实现近无损精度（与FullKV相比精度损失小于3.33个百分点），推理吞吐量最高提升5.8倍（Table 2），TPOT降低最高达1.68倍。该方法在ISO-batch和ISO-compression的公平设置下，系统性地优于现有量化和淘汰基线，为长推理任务的规模化部署提供了可行路径。



### 推理模型的长输出瓶颈

大型推理模型（Large Reasoning Models, LRMs）通过生成显式思维链来求解复杂任务，显著提升了数学推理、代码生成等场景的准确率。然而，这种能力伴随着巨大的推理成本：思维链通常包含数千乃至数万个 token，导致 KV 缓存随生成过程急剧膨胀。对于典型的自回归生成过程，KV 缓存的内存占用量可表示为：

$$\operatorname{Mem}(KV) \propto (I + b L_{\mathrm{gen}}) \times a \beta$$

其中 $I$ 为提示长度，$L_{\mathrm{gen}}$ 为生成 token 数，$b$ 为淘汰缩减因子，$a$ 为量化缩减因子，$\beta$ 为每参数字节数。当 $L_{\mathrm{gen}}$ 达到数万时，即使单个请求的 KV 缓存也可能超出 GPU 显存边界，严重制约吞吐量和用户体验。

### 现有压缩方法的困境

当前针对 KV 缓存的压缩技术可分为两大类：**量化**和**淘汰**。

- **量化方法**（如 KIVI, Liu et al. 2024b; PM-KVQ, Liu et al. 2025）通过降低 KV 缓存中键值对的位宽来减少内存占用。KIVI 采用均匀量化策略，对所有 token 分配相同的精度；PM-KVQ 则为推理模型引入了逐 token 渐进式量化。然而，均匀量化忽视了不同 token 对推理结果的重要性差异，在追求高压缩比时容易丢失关键信息。

- **淘汰方法**（如 H2O, Zhang et al. 2023; RaaS, Hu et al. 2025; R-KV, Cai et al. 2025; LazyEviction, Zhang et al. 2025a）基于注意力分数或时间局部性等启发式规则，主动丢弃被认为不重要的 KV 缓存条目。这些方法在 token 粒度上操作，无法感知思维链中更高层次的推理结构，容易意外淘汰对后续推理至关重要的 token。

如 Figure 2 所示，单独使用量化或淘汰均存在精度-压缩比的权衡瓶颈：量化在中等压缩比下精度下降较快，淘汰在高压缩比下性能崩溃。混合策略虽然展现出帕累托最优前沿的潜力，但现有混合方法仍缺乏对推理模型思维链动态特性的系统性利用。

### 思维链的结构化特性

本文通过对推理模型注意力模式的深入分析，揭示了思维链的三个关键特性，构成了 ThinKV 的核心动机：

**三模态注意力稀疏性。** 如 Figure 3 所示，推理模型在不同解码步上的注意力稀疏度呈现明显的三模态分布。这一现象在不同模型规模（R1-Llama-8B 至 R1-Llama-70B）和不同任务类型（AIME 数学推理、LiveCodeBench 代码生成）中一致出现。据此，思维链可被分解为三种类型：

$$\phi: \{y_0, \ldots, y_{n-1}\} \to \mathcal{T}, \; |\mathcal{T}| = 3$$

- **推理思维（Reasoning, R）**：模型进行逻辑推导的核心步骤，注意力高度集中。
- **执行思维（Execution, E）**：模型执行计算或生成具体输出的步骤，注意力模式相对分散。
- **过渡思维（Transition, T）**：连接不同推理片段的"元认知"标记（如"等等"、"让我重新思考"），注意力稀疏度最高。

**差异化的反事实重要性。** Figure 4 展示了通过反事实移除实验测量的各类思维对最终答案的因果重要性。结果呈现清晰的层次：R > E > T。然而，过渡思维中存在少量异常重要的实例——这些思维虽不直接贡献答案内容，却改变了推理轨迹；若被完全消除，可能导致模型陷入无限循环。

**过渡思维的全局影响。** Figure 5 的思维间关联分析揭示了一个关键动态：过渡思维的出现会显著削弱先前所有思维段对后续推理的影响力。这一"注意力重置"效应为渐进式淘汰提供了自然依据——当过渡思维出现后，之前的缓存内容可以被安全压缩。

### 本文动机

上述分析表明，推理模型的思维链具有可被利用的结构化规律，而现有方法在 token 粒度的操作无法捕捉这一高层语义。ThinKV 的核心动机在于：**利用注意力稀疏性动态识别思维类型，根据思维重要性差异化分配量化精度和主动淘汰，消除 token 级启发式方法造成的关键信息意外丢失**。通过在思维粒度上统一量化和淘汰策略，ThinKV 旨在以不到 5% 的原始 KV 缓存实现近无损精度，同时通过系统级优化实现显著的吞吐量提升。



## 核心方法与创新机理

ThinKV 的核心创新在于将 KV 缓存压缩的控制粒度从传统的 token 级别提升到**思维段（thought segment）级别**，通过动态感知推理模型在思维链中表现出的注意力稀疏性模式，实施差异化的量化精度分配与渐进式淘汰。这一思路从根本上改变了现有方法在精度保持与高压缩比之间的权衡困境。

### 瓶颈突破机制

大型推理模型（LRM）在长输出生成过程中，KV 缓存随生成 token 数 $L_{\mathrm{gen}}$ 线性膨胀，迅速超出 GPU 内存边界。现有压缩方法存在系统性缺陷：基于 token 级注意力的淘汰策略（如 **H2O** (Zhang et al., 2023)、**R-KV** (Cai et al., 2025)、**LazyEviction** (Zhang et al., 2025a)）忽视思维链内的推理结构，容易意外丢弃关键信息；统一量化方法（如 **KIVI** (Liu et al., 2024b)、**PM-KVQ** (Liu et al., 2025)）则对所有 token 施加相同精度，导致重要推理步骤的信息损失。

ThinKV 通过观察发现，注意力稀疏性在解码步上呈现**三模态分布**（Figure 3），分别对应三种思维类型：推理（R）、执行（E）和过渡（T）。这一现象揭示了推理模型生成过程的内在结构，为差异化压缩提供了可操作的信号。

### 三个关键 changed slots

**1. 量化策略：从统一量化到思维自适应精度分配**

基线方法采用统一量化（KIVI）或按 token 渐进式量化（PM-KVQ），对所有 token 一视同仁。ThinKV 的 TBQ（Think Before You Quantize）模块根据思维重要性分配差异化位精度：R 类思维分配 8-bit，E 类分配 4-bit，T 类分配 2-bit。这种分配基于反事实重要性分析（Figure 4）揭示的层级关系 $R > E > T$，确保高贡献思维段保留更多信息。实际运行中 ThinKV 的平均精度约为 3.4 bits，在难度更高的问题上因过渡思维频率增加而进一步降低。

**2. 淘汰策略：从 token 级启发式到思维段粒度渐进淘汰**

现有方法依赖 token 级的新近度或注意力分数进行逐 token 淘汰（如 H2O 的 heavy-hitter 保留、R-KV 的逐步驱逐），这导致两个问题：一是淘汰调用率极高（R-KV 达 82.93%，Table 5），二是可能误删关键 token。ThinKV 的 TBE（Think Before You Evict）模块利用过渡思维出现时会削弱先前所有思维段影响力的特性（Figure 5），以过渡思维为触发点，对整个思维段执行粗粒度渐进淘汰。其保留调度 $R = \{64, 32, 16, 8, 4\}$ 确保语义结构的保留，同时将淘汰调用率降至仅 4.59%（Table 5）。这种“以段为单位、以过渡为信号”的策略，从根本上避免了 token 级启发式方法的关键信息意外丢失。

**3. 内存管理：从 gather 压缩到就地槽位复用**

传统淘汰方法在物理移除 KV 缓存条目后，需要通过 gather 操作压缩内存碎片，这导致严重的吞吐下降——顺序 gather 可造成高达 37× 的 TPOT 膨胀（Figure 7）。ThinKV 的 Continuous Thinking kernel 扩展了 PagedAttention 机制，通过复用已淘汰的内存槽位直接写入新 token，消除了 gather 开销。这一系统级创新使得 ThinKV 在同等压缩比下实现显著更高的吞吐量：在 R1-Llama-8B 上达到 5.8× 于 R-KV (seq)、3.6× 于 R-KV (ovl) 的吞吐提升（Table 2），在 2048 token 预算下相较 FullKV 实现 15.8× 吞吐增益（Table 3）。

### 创新协同效应

上述三个 changed slots 并非孤立改进，而是形成因果链条：思维分解提供类型标签 → TBQ 据此差异化量化 → TBE 利用类型间动态关系触发淘汰 → Continuous Thinking kernel 在系统层面高效执行淘汰而不损失吞吐。单独使用 TBQ 会导致生成长度膨胀，抵消压缩收益；ThinKV 通过联合 TBE 避免了这一问题（Table 4, Figure 10(d)）。这种“感知-决策-执行”的闭环设计，使得 ThinKV 在仅使用不到 3.67% FullKV 内存的情况下，在 AIME 和 LiveCodeBench 上实现近无损精度（Figure 8），同时将吞吐量提升至最高 5.8 倍。



ThinKV 是一个面向大型推理模型（LRM）的思维自适应 KV 缓存压缩框架，其核心流程由四个关键模块串联构成：**Thought Decomposition**、**TBQ（Think Before You Quantize）**、**TBE（Think Before You Evict）** 和 **Continuous Thinking kernel**。整个 pipeline 的输入是模型在自回归生成过程中逐 token 产生的 KV 缓存，输出是经差异化量化和段粒度淘汰后的压缩缓存，最终由 Continuous Thinking 内核实现高效的内存复用。

### 模块关系与数据流

1. **Thought Decomposition（§4.1）** 作为上游感知模块，负责实时检测每个生成 token 的思维类型。它基于注意力稀疏性，通过离线校准阶段使用核密度估计（KDE）在标定集上学习稀疏度阈值 $\Theta$，并在解码时对选定层子集 $\mathcal{L}^*$ 的稀疏度取平均，将每个 token 分配到三种思维类别之一：推理（R）、执行（E）或过渡（T）——即 $\phi: \{y_0, \ldots, y_{n-1}\} \to \mathcal{T}, \; |\mathcal{T}| = 3$。这一分类结果是后续量化和淘汰决策的共同依据。

2. **TBQ（§4.2）** 接收思维类型标签，执行思维自适应量化。其核心映射 $\psi: \mathcal{T} \to B$ 将思维重要性转化为位精度分配：R 类 token 获得最高精度（8-bit），E 类居中（4-bit），T 类最低（2-bit），遵循 $\rho(c_{j_1}) > \rho(c_{j_2}) \Rightarrow \psi(c_{j_1}) \ge \psi(c_{j_2})$ 的单调性约束。量化策略上，Key 采用 per-channel 量化，Value 采用 per-token 量化（沿袭 **KIVI**，Liu et al., 2024b 的做法），在保持关键信息的同时最大化压缩比。

3. **TBE（§4.3）** 在 TBQ 之后执行思维自适应淘汰。与 token 级启发式淘汰（如 **H2O**、**R-KV**）不同，TBE 利用过渡思维（T）的独特属性——过渡思维的出现会削弱先前所有思维段的影响力（见 Figure 5）——触发段粒度的逐步收缩。具体机制为：TBE 维护一个保留调度 $R = \{64, 32, 16, 8, 4\}$，对每个思维段按调度逐步减少保留 token 数，并通过 K-means 聚类选取代表性 token，在激进压缩的同时保留语义结构。

4. **Continuous Thinking kernel（§5）** 作为系统层优化，扩展了 PagedAttention 机制。它通过复用 TBE 淘汰释放的内存槽位来存储新生成的 KV 缓存，从而避免传统淘汰方案中必需的 gather 操作（该操作可导致高达 37× 的 TPOT 膨胀，见 Figure 7），消除内存碎片并实现就地槽位重用。

### 关键设计决策

- **混合压缩路径**：ThinKV 选择量化与淘汰的混合策略（而非单一手段），是因为纯量化受限于精度下限，纯淘汰则面临关键 token 意外丢失的风险。两者协同使框架能够追踪帕累托最优前沿，在高压缩比下仍维持高精度（见 Figure 2）。

- **思维类型的三分类**：将思维链分解为 R/E/T 三类而非二分类或更多类别，是基于注意力稀疏度的三模态分布这一实证发现（Figure 3）。其中过渡思维虽不直接贡献答案，却改变推理轨迹——若被完全消除可能引发模型无限循环，因此 TBE 对其采取“触发淘汰但保留最少 token”的策略。

- **离线校准与在线推理的解耦**：稀疏度阈值 $\Theta$ 和层子集 $\mathcal{L}^*$ 通过离线 KDE 一次性确定，在线推理时仅需对选定层计算稀疏度并查表分类，将额外计算开销控制在可忽略范围（Table 5 显示 ThinKV 的淘汰调用率仅为 4.59%，远低于 R-KV 的 82.93%）。

整体而言，ThinKV 将“思维类型感知”作为统一的设计主线，贯穿量化精度分配、淘汰时机与粒度、以及内存管理三个维度，形成了一个从语义理解到系统实现的端到端压缩框架。



ThinKV 的核心洞察在于：推理模型的思维链可依据注意力稀疏性分解为**推理（R）、执行（E）与过渡（T）**三种思维类型。此三模态分布在多模型、多任务上稳定出现（Figure 3），且反事实重要性呈 R > E > T 的层级关系（Figure 4）。过渡思维虽不直接贡献答案，却能改变推理轨迹——完全消除将引发无限循环。基于此，ThinKV 构建了四个关键模块。

### 思维分解（Thought Decomposition）

思维分解模块将每个生成 token $y_i$ 映射到思维类型集合 $\mathcal{T} = \{\text{R}, \text{E}, \text{T}\}$：

$$\phi: \{y_0, \ldots, y_{n-1}\} \to \mathcal{T}, \; |\mathcal{T}| = 3$$

其实现分为离线校准与在线检测两步。离线阶段，在标定提示集上计算每层的注意力稀疏度，使用核密度估计（KDE）推导出 $|\mathcal{T}|-1$ 个稀疏度阈值 $\Theta = \{\theta_1, \theta_2\}$ 以分离三种思维。在线阶段，在选定的最优层子集 $\mathcal{L}^*$（通常 $|\mathcal{L}^*|=4$）上平均稀疏度，与阈值比较以实时判定当前 token 的思维类型。

### 思维自适应量化（TBQ: Think Before You Quantize）

TBQ 根据思维重要性分配差异化位精度，形式化为映射：

$$\psi: \mathcal{T} \to B, \quad \rho(c_{j_1}) > \rho(c_{j_2}) \Rightarrow \psi(c_{j_1}) \ge \psi(c_{j_2})$$

其中 $\rho(\cdot)$ 表示思维重要性，$B = \{2, 4, 8\}$ 为可选位宽。具体分配为：R 思维 8-bit、E 思维 4-bit、T 思维 2-bit。键（Key）采用逐通道量化，值（Value）采用逐 token 量化，遵循 **KIVI**（Liu et al., 2024b）的量化范式。此策略使 ThinKV 在推理过程中维持平均约 3.4-bit 精度，更困难的问题因过渡思维更频繁而获得更低的平均精度。

### 思维自适应淘汰（TBE: Think Before You Evict）

TBE 利用过渡思维的出现作为信号，触发段粒度的渐进式淘汰。核心机制包括：

- **保留调度**：定义保留 token 数序列 $R = \{64, 32, 16, 8, 4\}$，对所有思维类型统一适用，确保语义结构在激进压缩下仍被保留。
- **K-means 聚类**：在淘汰时对候选段进行聚类，保留各簇代表 token，避免关键信息的意外丢失。
- **触发条件**：当检测到过渡思维段时，TBE 对先前所有思维段执行一次粗粒度淘汰，而非逐 token 的细粒度驱逐。

TBE 的淘汰调用率仅为 4.59%，远低于 **R-KV**（Cai et al., 2025）的 82.93%（Table 5），大幅降低了运行时开销。

### Continuous Thinking 内核

传统淘汰方法需通过 gather 操作将幸存 token 压缩到连续内存，导致严重的吞吐下降——顺序 gather 可造成高达 37× 的 TPOT 膨胀（Figure 7(a)）。Continuous Thinking 内核扩展了 PagedAttention 机制，通过复用已淘汰的内存槽位直接写入新 token，消除了 gather 开销和内存碎片。此设计在 ISO 压缩条件下实现了显著更高的吞吐量（Table 2）。

### KV 缓存内存模型

ThinKV 的压缩效果可由以下内存模型刻画：

$$\operatorname{Mem}(KV) \propto (I + b L_{\mathrm{gen}}) \times a \beta$$

其中 $I$ 为提示长度，$L_{\mathrm{gen}}$ 为生成 token 数，$a$ 为量化缩减因子，$b$ 为淘汰缩减因子，$\beta$ 为每参数字节数。ThinKV 通过联合优化 $a$ 和 $b$，在 1024 token 预算下将内存占用降至 FullKV 的 3.67% 以下（Figure 8）。



## 实验与关键发现

### 主要结果

ThinKV 在推理模型（LRM）的 KV 缓存压缩任务上，以极低的存储开销实现了近无损的精度保持。核心实验结果如下：

**精度对比。** 在 AIME 和 LiveCodeBench 两个主流推理基准上，ThinKV 以 1024 token 的缓存预算（不足 FullKV 的 3.67% 存储）实现了与无压缩 FullKV 高度接近的 pass@1 精度。具体而言，R1-Qwen-14B 在 AIME 上仅下降 3.33 个百分点（50.00 vs 53.33），在 LiveCodeBench 上仅下降 2.06 个百分点（45.84 vs 47.90）（Table 1）。与量化基线相比，ThinKV 的平均量化精度仅为 3.4-bit，但在精度保持上显著优于 KIVI（Liu et al., 2024b）和 PM-KVQ（Liu et al., 2025）等基线方法。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/013_Table_1.jpg]]
*Table 1: Comparison of ThinKV with KV quantization baselines*

**淘汰基线对比。** 与针对 LRM 设计的淘汰方法相比，ThinKV 在同等缓存预算下展现出明显优势。Figure 8 显示，ThinKV 在 R1-Llama-8B 和 AceReason-14B 上仅以约 1.3% 的 KV 缓存实现了不足 4% 的精度下降，而 R-KV（Cai et al., 2025）和 LazyEviction（Zhang et al., 2025a）在相同预算下精度衰减更为严重。这一优势源于 ThinKV 的思维自适应淘汰策略：它基于思维段粒度进行主动粗粒度淘汰，而非依赖 token 级的启发式规则，从而更好地保留了推理结构中的关键信息。

**吞吐量提升。** 系统层面的吞吐量测试表明，ThinKV 在 A100-80GB GPU 上实现了显著的推理加速。在 32K 生成长度下，ThinKV 的吞吐量达到 8412.2 tokens/s，是 R-KV 顺序淘汰方案的 5.8 倍，是 R-KV 重叠淘汰方案的 3.6 倍（Table 2）。当缓存预算进一步收紧至 2048 token 时，ThinKV 相比 FullKV 实现了 15.8 倍的吞吐量增益（Table 3）。这一加速主要得益于 Continuous Thinking 内核的内存重用机制，它消除了传统 gather 操作带来的碎片整理开销。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/014_Table_2.jpg]]
*Table 2: Throughput (tokens/s) comparison on GPUs. ∗Mem. ftprnt: Memory footprint (%) normalized to FullKV*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/015_Table_3.jpg]]
*Table 3: ThinKV throughput on R1-Llama-8B (A100-80GB, 32K generation) with 2048 token budget*

### 消融实验

**TBQ 与 TBE 的协同效应。** 单独使用 TBQ（思维自适应量化）虽然可以压缩缓存，但会导致生成长度膨胀，部分抵消压缩带来的吞吐收益。Table 4 显示，ThinKV（TBQ+TBE）联合方案在同等精度下实现了比纯 TBQ 方案高 1.51 倍的吞吐量和 0.42 倍的延迟降低。Figure 10(d) 进一步证实，TBE 的加入有效抑制了生成长度的异常增长。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/023_Table_4.jpg]]
*Table 4: Impact of ThinKV components on accuracy, performance (iso-batch) for GPT-OSS-20B on LiveCodeBench*

**淘汰机制效率。** Table 5 的逐层时间分解揭示了 TBE 的高效性：ThinKV 的淘汰调用率仅为 4.59%，而 R-KV 高达 82.93%。这意味着 TBE 的段粒度淘汰策略大幅减少了运行时的淘汰操作频率，降低了系统开销。Figure 10(a) 的注意力召回率曲线表明，ThinKV 在不同 token 预算下均能维持接近 FullKV 的 Top-10 注意力 token 召回率，而 R-KV 和 LazyEviction 的召回率随预算收紧迅速衰减。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/024_Table_5.jpg]]
*Table 5: Per-layer time breakdown (%) and call rates across decode steps*

**关键超参数。** Figure 10(c) 的刷新间隔消融表明，τ=128 在精度和开销之间取得了最佳权衡。过小的 τ 导致频繁的思维重检测，增加计算开销；过大的 τ 则无法及时捕捉思维类型的变化。Figure 11(a) 显示，选择 4 层进行思维分解（|L*|=4）能在精度和效率之间取得最优平衡。此外，最小保留 token 数设为 4 可在激进压缩的同时保留语义结构。

**内存重用消除 gather 开销。** Figure 7 对比了顺序 gather 和重叠 gather 的性能。顺序 gather 在最坏情况下可导致高达 37 倍的 TPOT 膨胀，而重叠 gather 仍会使注意力时间膨胀约 35%。ThinKV 的 Continuous Thinking 内核通过复用淘汰槽位完全消除了 gather 操作，从而在同等压缩比下实现了更高的吞吐量。

### 失败模式与局限性

尽管 ThinKV 在长输出推理场景中表现优异，但其设计存在以下局限：

1. **长输入场景不适用。** 当前方法假设推理任务以长输出为主，思维分解和淘汰策略均针对解码阶段设计。当未来 LRM 更依赖长输入上下文时，需要扩展预填充阶段的压缩策略。

2. **注意力稀疏性模式不稳定。** 思维分解依赖注意力稀疏性的三模态分布，但在某些层中可能出现多于三个的稀疏区域，导致类型判定模糊。虽然通过选择最优层子集可以缓解，但在极端情况下仍可能影响分解准确性。

3. **异常过渡思维的潜在风险。** 部分过渡思维虽不直接贡献答案，却具有极高的反事实重要性（Figure 4）。若这些异常过渡思维被激进淘汰，可能引发模型陷入无限循环。当前方案通过保留调度保留少量过渡 token 作为缓冲，但未提供理论保证。

### 重要图表结论

- **Figure 2**：纯量化在低压缩比下精度高但压缩上限受限，纯淘汰在高压缩比下精度崩溃，ThinKV 的混合策略沿帕累托前沿实现了精度与压缩比的最优权衡。
- **Figure 4**：思维类型的反事实重要性排序为 R > E > T，但存在少量异常重要的过渡思维，其淘汰会导致显著的 KL 散度上升。
- **Figure 5**：过渡思维的出现会系统性地削弱先前所有思维段的影响力，为渐进式淘汰提供了因果依据。
- **Figure 8**：ThinKV 以 <3.67% 的 FullKV 存储实现了跨模型、跨数据集的近无损精度，显著优于所有淘汰基线。
- **Table 2**：Continuous Thinking 内核的内存重用使 ThinKV 在同等压缩下实现了比 R-KV 高 3.6–5.8 倍的吞吐量。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/027_Table_6.jpg]]
*Table 6: Summary of notation used in the paper*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/029_Table_7.jpg]]
*Table 7: Keyword list to interpret different thought types*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/046_Table_8.jpg]]
*Table 8: Comparison of ThinKV and R-KV on GSM8K using MobileLLM-R1-950M*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/047_Table_9.jpg]]
*Table 9: Accuracy of ThinKV vs FullKV across reasoning effort levels for GPT-OSS-120B on Live-CodeBench*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/048_Table_10.jpg]]
*Table 10: Impact of data format choices on accuracy for R1-Llama-8B*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/049_Table_11.jpg]]
*Table 11: LLM accuracy comparison on LongWriter task*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_M3CeHnZKNC/figures/051_Table_12.jpg]]
*Table 12: Throughput comparison under different batch sizes implemented in vLLM*



## 定位与知识库关联

### 问题定位：长推理输出的KV缓存瓶颈

大型推理模型（LRM）在生成长思维链时，KV缓存随输出长度线性膨胀，迅速超出GPU内存界限。现有压缩方法主要沿两条路径演进：**量化**（quantization）和**淘汰**（eviction），但二者均存在根本性局限。

量化方法如 **KIVI**（Liu et al., 2024b）对LLM采用统一精度量化，**PM-KVQ**（Liu et al., 2025）针对LRM引入逐token渐进量化。这些方法虽然控制了内存占用，但忽视了推理链内部不同token的重要性差异——关键推理步骤与填充性过渡语句被赋予相同精度，导致在低比特下精度急剧下降。

淘汰方法则分为两个分支：LLM淘汰基线如 **H2O**（Zhang et al., 2023）基于注意力分数和最近性进行token级淘汰；LRM专用方法如 **RaaS**（Hu et al., 2025）、**R-KV**（Cai et al., 2025）和 **LazyEviction**（Zhang et al., 2025a）尝试利用推理动态，但本质上仍停留在token级启发式策略。这些方法的核心缺陷在于：它们无法识别思维链的宏观结构，导致关键信息被意外淘汰，或需频繁调用淘汰操作（R-KV的淘汰调用率高达82.93%，见Table 5），严重损害吞吐性能。

### ThinKV的方法突破

ThinKV的核心突破在于将压缩策略从**token级**提升到**思维级**。其关键洞察是：思维链可分解为三种类型——推理（R）、执行（E）和过渡（T），且注意力稀疏性自然地暴露这些类型（Figure 3）。基于此，ThinKV构建了四个协同模块：

**思维分解**（§4.1）利用注意力稀疏度将每个token分配到R/E/T类别，通过离线KDE校准获得稀疏度阈值，解码时在线检测思维类型。

**思维自适应量化TBQ**（§4.2）根据思维重要性差异化分配精度：R为8-bit，E为4-bit，T为2-bit，整体平均精度仅3.4 bits。这比KIVI的统一量化和PM-KVQ的逐token渐进量化更精准地匹配了信息密度分布。

**思维自适应淘汰TBE**（§4.3）利用过渡思维的出现作为淘汰信号：当检测到过渡思维时，先前思维段的影响力被削弱（Figure 5），可安全地以段粒度逐步淘汰，而非逐token操作。这从根本上解决了H2O、R-KV等方法频繁调用淘汰操作导致的吞吐下降问题——TBE的淘汰调用率仅4.59%（Table 5），且采用保留调度（R = {64, 32, 16, 8, 4}）确保语义结构不被破坏。

**Continuous Thinking内核**（§5）扩展PagedAttention，通过复用淘汰槽位实现就地内存重用，消除了传统gather-based压缩的碎片整理开销——实验表明，sequential gather可导致高达37×的TPOT减速（Figure 7）。

### 适用边界与局限

**适用场景**：ThinKV设计假设推理任务以长输出为主（如数学推理、代码生成），KV缓存膨胀主要由生成阶段驱动。在此场景下，其以不到3.67%的FullKV内存实现近无损精度（Figure 8），吞吐提升最高达5.8×（Table 2）。

**已知局限**：
1. **不直接适用于长输入场景**：当前设计未优化预填充阶段的压缩。当未来LRM更依赖长输入上下文时，需要将思维自适应策略扩展到预填充压缩。
2. **思维分解依赖注意力稀疏性模式**：在某些层中，注意力分布可能呈现多于三个稀疏区域（Figure 3），虽然通过选择最优层子集（|L*|=4, Figure 11a）可缓解，但模式的模糊性仍是局限。
3. **过渡思维的异常重要性**：反事实分析（Figure 4）揭示存在异常重要的过渡思维——若被完全消除会引发模型无限循环。当前TBE通过保留调度保留少量过渡token，但未对这些异常token进行专门识别和保护。

### 开放问题

1. **思维类型数量的自动发现**：当前依赖预定义的三类思维（R/E/T）和关键词辅助校准。能否从注意力稀疏性中自动学习思维类型数量，使方法更普适？

2. **异常过渡思维的精确保护**：如何在不显著增加内存开销的前提下，识别并保留那些稀疏出现但具有极高反事实重要性的过渡思维？

3. **向非推理LLM的迁移**：思维分解的核心机制依赖推理链的结构化动态。对于通用长输出生成（如故事创作、长文档生成），注意力稀疏性是否仍能暴露有意义的宏观结构？

4. **混合长输入-长输出场景的协同优化**：当输入和输出均很长时，预填充压缩和ThinKV的自适应策略如何协同？预填充阶段是否也能利用思维类型信号进行差异化压缩？

5. **与新兴推理架构的兼容性**：ThinKV的思维分解假设自回归生成中的注意力稀疏性模式。对于采用不同推理范式（如并行推理、树搜索）的未来LRM，该方法的有效性需要重新验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/ThinKV_Thought_Adaptive_KV_Cache_Compression_for_Efficient_Reasoning_Models.pdf]]
