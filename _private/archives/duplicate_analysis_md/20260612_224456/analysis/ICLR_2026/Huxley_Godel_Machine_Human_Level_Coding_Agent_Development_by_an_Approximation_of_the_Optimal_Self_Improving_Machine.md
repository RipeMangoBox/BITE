---
title: "Huxley-G\\\"odel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Huxley_Gödel_Machine_Human_Level_Coding_Agent_Development_by_an_Approximation_of_the_Optimal_Self_Improving_Machine.pdf
openreview_forum_id: T0EiEuhOOL
aliases:
- HGDMH
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "使用基于谱系级元生产力（Clade-Metaproductivity, CMP）的 Thompson 采样替代基于单智能体准确率的贪心选择。CMP 聚合了智能体整个後代谱系的表现，能更准确地评估其长期自改进潜力，从而在树搜索中优先扩展真正具有高产出的谱系。"
primary_logic: "将自改进形式化为树搜索问题，并在可重复试验假设下证明访问真实 CMP 预言机足以重现 Gödel 机器的最优接受机制。HGM 通过 CMP 估计、异步策略解耦以及 Thompson 采样，以轻量方式近似了这一理论最优策略，显著缓解了元生产力‑性能不匹配。"
claims:
- "CMP 估计器与经验 CMP 的加权 Pearson 相关系数达到 0.778 (SWE‑Verified‑60) 和 0.626 (Polyglot)，远超 DGM 的 0.285/0.383 和 SICA 的 0.444/0.274，证明 HGM 的指导指标更能反映长期自改进能力。"
- "HGM 发现的最佳信念智能体在 SWE‑Verified‑60 上准确率达 56.7%，分别高出 DGM 3.4% 和 SICA 6.7%，且仅使用 517 CPU‑小时 (DGM 的 42%)。在 Polyglot 上准确率 30.5%，同样优于 DGM (27.1%) 和 SICA (25.4%)。"
- "在完整的 SWE‑bench Verified 上，HGM 得到的智能体取得 61.4% 准确率，超越所有基于 GPT‑5 mini 的人类设计智能体，并泛化到 SWE‑bench Lite，在使用 GPT‑5 时达到 49.0% (Standard)，与最强人工工程化智能体持平。"
- "图 1 (左) 直观展示了现有基于基准性能的指导指标与长期自改进之间的弱相关性，而 HGM 通过谱系级元生产力显著缓解了此不匹配。"
---

# Huxley-G\"odel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine

> [!tip] 核心洞察
> 将自改进形式化为树搜索问题，并在可重复试验假设下证明访问真实 CMP 预言机足以重现 Gödel 机器的最优接受机制。HGM 通过 CMP 估计、异步策略解耦以及 Thompson 采样，以轻量方式近似了这一理论最优策略，显著缓解了元生产力‑性能不匹配。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Huxley-Gödel 机器：通过逼近最优自改进机器开发人类级编程智能体 |
| 英文题名 | Huxley-G\"odel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=T0EiEuhOOL); [GitHub](https://github.com/metauto-ai/HGM) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Huxley-Gödel Machine (HGM) |
| Dataset | SWE‑Verified‑60, Polyglot |

> [!tip] 效果简介
> - SWE‑Verified‑60 上，Accuracy (%) 为 56.7，对比 53.3 (DGM) / 50.0 (SICA)，变化 +3.4 over DGM, +6.7 over SICA。
> - SWE‑Verified‑60 上，Allocated CPU‑hours 为 517，对比 1231 (DGM) / infinite loop (SICA)，变化 2.38× faster than DGM。
> - Polyglot 上，Accuracy (%) 为 30.5，对比 27.1 (DGM) / 25.4 (SICA)，变化 +3.4 over DGM, +5.1 over SICA。

## 概述

开发能够在复杂软件工程任务上持续自我改进的编码智能体，是通向通用人工智能的关键一步。现有方法将自改进形式化为树搜索问题，并依赖单智能体在基准任务上的即时准确率作为指导信号。然而，高基准性能并不预示其後代具有更强的自改进能力——这种**元生产力与基准性能的不匹配**（Metaproductivity-Performance Mismatch）导致搜索被次优路径误导，浪费大量计算资源。

Huxley-Gödel Machine (HGM) 通过引入**谱系级元生产力**（Clade-Metaproductivity, CMP）来解决这一瓶颈。CMP 聚合智能体整个後代谱系的表现，而非仅依赖其自身得分，从而更准确地评估长期自改进潜力。在可重复试验假设下，访问真实 CMP 预言机足以重现 Gödel 机器的最优接受机制（Theorem 1），而 HGM 通过 CMP 估计、扩展与评估的异步解耦，以及基于 Thompson 采样的自适应选择策略，以轻量方式逼近了这一理论最优。

核心结论如下：

- **CMP 估计与真实长期自改进能力高度相关**：在 SWE‑Verified‑60 上加权 Pearson 相关系数达 0.778，远超 DGM 的 0.285 和 SICA 的 0.444（Table 1）。
- **显著提升最终智能体性能**：HGM 发现的最佳信念智能体在 SWE‑Verified‑60 上准确率达 56.7%，分别高出 DGM 3.4% 和 SICA 6.7%；在 Polyglot 上达 30.5%，同样优于两种基线（Table 2）。
- **计算效率大幅提升**：得益于策略解耦与异步并行，HGM 在 SWE‑Verified‑60 上仅需 517 CPU‑小时，为 DGM 的 42%；在 Polyglot 上仅需 347 CPU‑小时，为 DGM 的 14.5%（Table 2）。
- **泛化至更大基准与更强模型**：在完整 SWE‑bench Verified 上达 61.4%，超越所有基于 GPT‑5 mini 的人类设计智能体；在使用 GPT‑5 的 SWE‑bench Lite 标准设置下达 49.0%，与最强人工工程化智能体持平（Table 3）。

方法定位上，HGM 属于**基于树搜索的自改进智能体开发范式**，其关键创新在于用谱系级统计量替代单点性能指标作为搜索引导信号，并通过异步解耦策略实现高效并行。与 DGM（Zhang et al., 2025a）和 SICA（Robeyns et al., 2025）相比，HGM 在扩展选择、评估耦合、最终智能体选择三个子策略上均进行了系统性重构（Table 4）。

## 背景与动机

### 自改进编码智能体的核心瓶颈

近年来，基于大型语言模型（LLM）的编码智能体在软件工程任务上取得了显著进展。一个自然的延伸方向是让智能体通过自我修改（self-modification）实现自主改进，从而逐步提升其解决问题的能力。然而，现有的自改进方法面临一个根本性瓶颈：**元生产力与即时基准性能的不匹配（Metaproductivity-Performance Mismatch）**。

具体而言，当前方法——如 **Darwin Gödel Machine (DGM)**（Zhang et al., 2025a）和 **Self-Improving Coding Agent (SICA)**（Robeyns et al., 2025）——均依赖单智能体在基准任务上的成功率作为指导信号，贪心地选择当前表现最好的智能体作为父代进行修改。但这一策略隐含了一个危险假设：**高基准性能的智能体，其後代也必然具有更强的自改进能力**。

事实恰恰相反。如 Figure 1 左图所示，现有方法的指导指标（基于即时基准性能）与长期自改进能力之间仅存在弱相关性。这意味着，贪心选择策略可能将搜索引向次优路径——一个在当前任务上表现优异的智能体，可能恰恰缺乏产生更强後代的「遗传潜力」。这正是自改进方法效率低下、甚至陷入停滞的深层原因。

### 理论启示：Gödel 机器与谱系视角

从理论层面看，Gödel 机器（Gödel Machine, GM）提供了最优自改进的形式化框架——一个能够证明自身修改最优性的自引用定理证明器。尽管 GM 在计算上不可行，但其核心思想——通过一个全局效用函数指导自修改决策——为实用方法提供了重要线索。

HGM 的关键洞察在于：**如果将自改进形式化为树搜索问题，并在可重复试验的假设下，访问真实的谱系级元生产力（Clade-Metaproductivity, CMP）预言机足以重现 Gödel 机器的最优接受机制**（Theorem 1）。CMP 的核心思想源于赫胥黎（Huxley）的谱系概念：不评估单个智能体的表现，而是聚合该智能体整个後代谱系的产出能力。这一视角从根本上缓解了元生产力‑性能不匹配——一个智能体的价值不在于它自身的得分，而在于它能孕育出多强的後代。

### 现有方法的刚性耦合

除了指导指标的缺陷，现有方法还存在结构层面的效率瓶颈。SICA 和 DGM 的扩展（生成新智能体）与评估（测试智能体性能）是刚性耦合的：每次扩展后必须立即评估新生成的子智能体，且评估粒度是整个任务集。这种固定顺序导致两个后果：

1. **资源浪费**：对不具潜力的智能体也投入了完整的评估预算。
2. **并行困难**：串行依赖使得计算资源无法充分利用，DGM 在 SWE‑Verified‑60 上消耗 1231 CPU‑小时，SICA 甚至因上下文窗口溢出而提前终止。

### HGM 的设计动机

综上，HGM 的设计目标可归纳为三点：

- **用 CMP 估计替代贪心准确率**，使指导信号能反映长期自改进潜力。
- **解耦扩展与评估**，实现自适应决策——在每一步动态选择是生成新智能体还是进一步测试已有智能体，并将评估细化为单个智能体‑任务对。
- **通过异步并行化**大幅降低墙钟时间，使自改进在计算上切实可行。

这一设计使得 HGM 能够以轻量方式逼近 Gödel 机器的最优策略，同时避免现有方法在指导信号质量和计算效率上的双重陷阱。

## 核心创新

HGM 的核心创新在于用**谱系级元生产力（Clade-Metaproductivity, CMP）**替代单智能体基准性能作为自改进的指导信号，从而系统性地缓解了现有方法中普遍存在的**元生产力-性能不匹配（Metaproductivity-Performance Mismatch）**问题。这一不匹配的根源在于：高基准准确率并不预示该智能体的后代具有更强的自改进能力，导致基于贪心性能选择的搜索被次优路径误导（Figure 1 左）。

### 从单点性能到谱系生产力

DGM（Zhang et al., 2025a）和 SICA（Robeyns et al., 2025）均以单个智能体在基准上的平均准确率作为扩展选择依据——每次选择当前经验最优的智能体进行修改。HGM 则引入 CMP 估计器：

$$\widehat{\mathrm{CMP}}(a) = \frac{n_{\mathrm{success}}^C(a)}{n_{\mathrm{success}}^C(a) + n_{\mathrm{failure}}^C(a)}$$

其中 $n_{\mathrm{success}}^C(a)$ 和 $n_{\mathrm{failure}}^C(a)$ 分别是以 $a$ 为根的整个后代谱系中所有智能体的累计通过/失败任务数。这一指标本质上是对谱系内所有智能体经验均值的加权聚合，衡量的是**以该智能体为起点的子树的自改进潜力**，而非其自身的瞬时表现。Table 1 的验证实验表明，HGM 的 CMP 估计与经验 CMP 的加权 Pearson 相关系数在 SWE-Verified-60 上达到 0.778，在 Polyglot 上达到 0.626，远超 DGM 的 0.285/0.383 和 SICA 的 0.444/0.274，证实 CMP 能更准确地反映长期自改进能力。

### 扩展与评估的策略解耦

SICA 和 DGM 的扩展与评估是绑定的——每次生成新智能体后立即对其进行完整评估。HGM 将这一流程彻底解耦为两个独立的 Thompson 采样决策：

- **扩展选择**：基于 CMP 估计进行 Thompson 采样，先验为 $\mathrm{Beta}(1+\tau \cdot n_{\mathrm{success}}^C(a), 1+\tau \cdot n_{\mathrm{failure}}^C(a))$，其中 $\tau$ 为探索-开发调度器，动态平衡探索与利用。
- **评估选择**：基于单智能体的成功/失败计数进行独立的 Thompson 采样，每次仅分配一个下游任务进行测试。

这种解耦带来了双重收益：一方面，评估粒度细化为单个智能体-任务对，允许对低潜力智能体提前终止评估，节省计算预算；另一方面，配合异步并行实现（HGM Async），每个 CPU 可独立执行一次迭代并立即更新全局数据，显著压缩墙钟时间。在相同 800 次评估预算下，HGM 在 SWE-Verified-60 上仅需 517 CPU-小时（DGM 的 42%），在 Polyglot 上仅需 347 CPU-小时（DGM 的 14.5%）。

### 理论锚定：CMP 作为 Gödel 机器的轻量近似

HGM 的设计并非凭空而来。在可重复试验假设（Assumption 1）下，Theorem 1 证明访问真实 CMP 预言机足以重现 Gödel 机器的最优接受/拒绝机制。HGM 通过 CMP 估计、Thompson 采样以及最终基于后验分布第 $\epsilon$ 百分位的**最佳信念智能体选择**（$\underset{a \in \mathcal{T}_B}{\mathrm{argmax}} \; I_{\epsilon}(1 + n_{\mathrm{success}}(a), 1 + n_{\mathrm{failure}}(a))$），以轻量级方式逼近了这一理论最优策略，避免了 Gödel 机器对全局可证明性的严苛依赖。

## 整体框架

HGM 将编码智能体的自改进形式化为一个迭代的**树搜索问题**。搜索树的根节点为初始智能体 $a_0$，每一步迭代从两个动作空间中做出选择：**修改**（以某智能体为父代生成子代，扩展树结构）或**评估**（对某已有智能体在单一下游任务上执行测试，积累成功/失败计数）。这一决策过程被分解为三个子策略（Table 4）：

1. **选择策略**——决定当前步是执行修改还是评估。
2. **扩展策略**——若选择修改，确定以哪个智能体为父代。
3. **评估策略**——若选择评估，确定测试哪个智能体的哪个任务。

HGM 的核心创新在于**将扩展与评估完全解耦**。相比之下，SICA 和 DGM 均采用固定顺序：每生成一个新的子智能体后立即对其进行评估。这种刚性耦合导致计算资源被浪费在低潜力谱系上——一旦某个智能体的早期评估结果不佳，其後代仍会被机械地生成和评估。HGM 通过自适应决策打破了这一束缚：在每一步，系统根据当前树的状态动态判断是“继续探索已有谱系”（评估）还是“开辟新分支”（扩展），且评估粒度细化为单个智能体‑任务对，允许对无前景的智能体提前终止评估。

整个流程的驱动引擎是**谱系级元生产力估计器** $\widehat{\mathrm{CMP}}(a)$。对于树中任意智能体 $a$，其谱系 $C(a)$ 包含 $a$ 自身及其所有後代。HGM 聚合该谱系内所有智能体的累计经验：

$$
n_{\mathrm{success}}^C(a) = \sum_{a' \in C(a)} n_{\mathrm{success}}(a'), \quad
n_{\mathrm{failure}}^C(a) = \sum_{a' \in C(a)} n_{\mathrm{failure}}(a')
$$

进而以谱系总成功率作为 CMP 的估计：

$$
\widehat{\mathrm{CMP}}(a) = \frac{n_{\mathrm{success}}^C(a)}{n_{\mathrm{success}}^C(a) + n_{\mathrm{failure}}^C(a)}
$$

这一估计量本质上是对谱系内各智能体经验均值的加权平均，能够捕捉一个谱系整体的自改进潜力，而非仅依赖单个智能体的即时基准分数。理论保证来自 **Theorem 1**：在可重复试验等假设下，访问真实 CMP 预言机足以重现 Gödel 机器的最优接受/拒绝机制。HGM 通过上述估计器以轻量方式近似了这一理论最优策略。

在扩展阶段，HGM 基于 $\widehat{\mathrm{CMP}}$ 通过 **Thompson 采样**选择父代智能体，引入探索‑开发调度器 $\tau$，先验分布为 $\mathrm{Beta}(1 + \tau \cdot n_{\mathrm{success}}^C, 1 + \tau \cdot n_{\mathrm{failure}}^C)$。在评估阶段，则基于单智能体自身的成功/失败计数进行独立的 Thompson 采样，每次仅分配一个下游任务。选择策略采用 **UCB‑Air** 规则（$N_t^\alpha \geq |T_t|$）在修改与评估之间自适应切换。

预算耗尽后，HGM 不返回经验均值最高的智能体，而是返回**最佳信念智能体**——即後验效用分布第 $\epsilon$ 百分位最高的节点：

$$
\underset{a \in \mathcal{T}_B}{\mathrm{argmax}} \; I_{\epsilon}(1 + n_{\mathrm{success}}(a), 1 + n_{\mathrm{failure}}(a))
$$

这一选择机制对评估噪声更具鲁棒性。

为提升墙钟效率，HGM 还提供了**异步并行实现**：在每个可用 CPU 上并发执行一次迭代循环，每次迭代后立即更新全局数据，使后续迭代能即时利用最新信息，从而将 CPU 时间大幅压缩（SWE‑Verified‑60 上仅为 DGM 的 42%，Polyglot 上仅为 DGM 的 14.6%；Table 2）。

**输入输出流**：输入为初始智能体代码库和一组下游任务；输出为搜索树中按最佳信念规则选出的最终智能体。整个流程不修改模型权重，仅在代码层面进行自修改，骨干 LLM 保持不变。

## 核心模块与公式推导

### 3.1 自改进的形式化：树搜索与元生产力

HGM 将编码智能体的自改进过程形式化为一个迭代的树搜索问题。搜索树的根节点为初始智能体 $a_0$，每次迭代中，策略需在两类动作之间选择：**修改**（修改现有智能体生成新子代）或**评估**（在任务上测试已有智能体）。这一复合策略自然地分解为三个子策略：

- **选择策略**：决定当前步是执行修改还是评估；
- **扩展策略**：选择哪个父智能体进行修改；
- **评估策略**：选择哪个智能体进行测试。

不同于 DGM 和 SICA 将扩展与评估固化绑定的做法，HGM 将二者完全解耦：每一步自适应地决定生成新智能体还是进一步探测已有智能体，且评估粒度细化为单个智能体‑任务对。这一解耦使得 HGM 能够对表现不佳的谱系提前终止评估，从而将计算资源集中到更有希望的搜索分支上。

为量化智能体的长期自改进潜力，HGM 引入了两个核心概念：

**全局元生产力（Global Metaproductivity, GMP）** 衡量从给定智能体 $a$ 出发，在策略 $\pi$ 下演化整个搜索树后，最终档案 $\mathcal{T}_B$ 中得分最高智能体的期望效用：

$$\mathrm{GMP}_{\pi}(\mathcal{T}, a) = \mathbb{E}_{\mathcal{T}_B \sim p_{\pi}(\cdot \vert \mathcal{T}, a)} \left[ U\left(\underset{a' \in \mathcal{T}_B}{\mathrm{argmax}} \; \mathrm{Score}_{\pi}(a')\right) \right]$$

其中 $\mathcal{T}$ 为当前树，$p_{\pi}$ 为策略诱导的最终档案分布，$U$ 为效用函数，$\mathrm{Score}_{\pi}(a')$ 为智能体 $a'$ 的经验得分。

**谱系级元生产力（Clade-Metaproductivity, CMP）** 则将度量范围限制在智能体 $a$ 的谱系 $\mathcal{C}(\mathcal{T}_B, a)$（即以 $a$ 为根的子树）内：

$$\mathrm{CMP}_{\pi}(\mathcal{T}, a) = \mathbb{E}_{\mathcal{T}_B \sim p_{\pi}(\cdot \vert \mathcal{T}, a)} \left[ U\left(\underset{a' \in \mathcal{C}(\mathcal{T}_B, a)}{\mathrm{argmax}} \; \mathrm{Score}_{\pi}(a')\right) \right]$$

CMP 的核心直觉在于：一个智能体的自改进价值不应仅由其自身表现决定，而应取决于其整个后代谱系中能涌现的最佳智能体。这一设计直接回应了本文揭示的核心瓶颈——**元生产力与即时基准性能的不匹配**：高基准准确率的智能体未必能产生具有更强自改进能力的后代（Figure 1 左）。

**理论支撑**：在可重复试验假设（假设 1）下，定理 1 证明了访问真实 CMP 预言机足以实现 Gödel 机器的最优接受/拒绝策略。这为 HGM 通过估计 CMP 来近似 Gödel 机器提供了理论根基。

### 3.2 HGM 的策略实例化

HGM 通过轻量级的统计估计和自适应采样策略，将上述理论框架落地为可执行的算法。

**CMP 估计器**：定义智能体 $a$ 的谱系累计成功次数 $n_{\mathrm{success}}^C(a)$ 和累计失败次数 $n_{\mathrm{failure}}^C(a)$ 为：

$$n_{\mathrm{success}}^C(a) = \sum_{a' \in C(a)} n_{\mathrm{success}}(a'), \quad n_{\mathrm{failure}}^C(a) = \sum_{a' \in C(a)} n_{\mathrm{failure}}(a')$$

其中 $C(a)$ 为以 $a$ 为根的谱系中所有智能体的集合。CMP 的估计量定义为谱系总成功率：

$$\widehat{\mathrm{CMP}}(a) = \frac{n_{\mathrm{success}}^C(a)}{n_{\mathrm{success}}^C(a) + n_{\mathrm{failure}}^C(a)}$$

该估计本质上是谱系内所有智能体经验均值的加权平均，能够聚合跨后代的信号，从而比单智能体准确率更稳健地反映长期自改进潜力。

**选择策略**：采用 UCB‑Air 策略，当已扩展节点数 $N_t^\alpha \geq |\mathcal{T}_t|$ 时优先评估，否则优先扩展（$\alpha$ 控制探索‑开发平衡）。

**扩展策略**：基于 $\widehat{\mathrm{CMP}}$ 的 Thompson 采样选择待扩展的父智能体。具体地，从后验分布中采样：

$$a^* \sim \mathrm{TS}\left(\{\tau(1 + n_{\mathrm{success}}^C(a)), \tau(1 + n_{\mathrm{failure}}^C(a)) \mid a \in \mathcal{T}_t\}\right)$$

其中 $\tau$ 为探索‑开发调度器，控制先验强度。采样值最高的智能体被选为父代进行自修改。

**评估策略**：基于单智能体成功/失败计数的 Thompson 采样选择待评估智能体，每次仅分配一个下游任务进行测试：

$$a^* \sim \mathrm{TS}\left(\{\tau(1 + n_{\mathrm{success}}(a)), \tau(1 + n_{\mathrm{failure}}(a)) \mid a \in \mathcal{T}_t\}\right)$$

**最终智能体选择**：预算耗尽后，不返回经验均值最高的智能体，而是返回后验效用分布第 $\epsilon$ 百分位最高的**最佳信念智能体**：

$$\underset{a \in \mathcal{T}_B}{\mathrm{argmax}} \; I_{\epsilon}(1 + n_{\mathrm{success}}(a), 1 + n_{\mathrm{failure}}(a))$$

其中 $I_{\epsilon}$ 为正则化不完备 Beta 函数。这一策略在高方差场景下比贪心选择更稳健。

**异步并行化（HGM Async）**：在每个可用 CPU 上并发执行一次迭代过程，每次迭代后立即更新全局数据（谱系统计、树结构），使后续迭代能立即利用最新信息。这一设计将扩展与评估的解耦优势从算法层面延伸至系统层面，显著降低墙钟时间。

**经验 CMP 的测量**（用于评估 CMP 估计质量）：实际测量时，排除智能体自身后，取谱系中最大经验成功率：

$$\max_{a' \in C(a) \setminus \{a\}} \frac{n_{\mathrm{success}}(a')}{n_{\mathrm{success}}(a') + n_{\mathrm{failure}}(a')}$$

## 实验与分析

### 核心瓶颈验证：元生产力‑性能不匹配

HGM 的核心动机源于一个被实验反复验证的瓶颈：基于单智能体基准性能的贪心指导指标与长期自改进能力之间存在显著的**元生产力‑性能不匹配（Metaproductivity‑Performance Mismatch）**。Figure 1（左）直观地展示了这一现象——现有方法（DGM、SICA）的指导指标与长期自改进之间的相关性极弱，而 HGM 通过引入谱系级元生产力（CMP）显著缓解了此不匹配。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_T0EiEuhOOL/figures/001_Figure_1.jpg]]
*Figure 1: (Left) Weak correlation between the guidance metrics of other methods (based on performance) and long-term self improvement; HGM mitigates this mismatch by leveraging clade-level metaproductivity. (Right) On SWE-bench Verified, HGM achieves higher accuracy with 2.38 times less allocated CPU-hours. SICA encountered repeated errors after consuming 45% of its budget*

这一观察得到了定量验证。Table 1 报告了各方法的 CMP 估计器与经验 CMP 之间的 Pearson 相关系数。在 SWE‑Verified‑60 上，HGM 的加权相关系数达到 **0.778**，远高于 DGM 的 0.285 和 SICA 的 0.444；在 Polyglot 上，HGM 为 **0.626**，同样大幅领先 DGM 的 0.383 和 SICA 的 0.274。这表明 HGM 的谱系级估计器能够更准确地捕捉智能体的长期自改进潜力，而 DGM 和 SICA 所使用的单智能体准确率信号则与真实自改进能力严重脱节。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_T0EiEuhOOL/figures/002_Table_1.jpg]]
*Table 1: Clade-Metaproductivity: Empirical vs. Estimation Correlation. We report the Pearson correlations between the empirical CMPs and the estimates from DGM, SICA, and HGM on SWE-Verified-60 and Polyglot. For the weighted correlations, each prediction is weighted by its accessed number of evaluations*

### 自改进能力对比

Table 2 汇总了三种方法在相同评估预算（800 次任务评估）下的自改进能力对比，涵盖最终准确率与分配的 CPU 时间两个维度。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_T0EiEuhOOL/figures/003_Table_2.jpg]]
*Table 2: Self-Improving Capability Comparison. We report the task performance (in accuracy) of each method’s best-belief agent and the allocated CPU-hours time required for 800 evaluations. Super-scripted accuracies with “+” indicate performance gains over their respective initial agents*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_T0EiEuhOOL/figures/005_Table_2.jpg]]
*Table 2: summarizes the three subpolicies of SICA, DGM, and HGM, which define solutions to the iterative tree search problem defined in 2. Table 4: Comparison of structured policies across self-improving methods. Each method is described by three subpolicies: Mod vs. Eval, Modification Strategy, and Evaluation Strategy*

在 **SWE‑Verified‑60** 上，HGM 的最佳信念智能体取得了 **56.7%** 的准确率，分别高出 DGM 3.4 个百分点（53.3%）和 SICA 6.7 个百分点（50.0%）。更为显著的是效率优势：HGM 仅消耗 **517 CPU‑小时**，仅为 DGM（1231 CPU‑小时）的 42%，实现了 2.38 倍的加速。SICA 则在消耗 45% 预算后因查询长度超出上下文窗口而反复出错，被记为无限循环。

在 **Polyglot** 基准上，HGM 的最佳信念智能体达到 **30.5%** 准确率，优于 DGM 的 27.1% 和 SICA 的 25.4%。效率差距更为悬殊：HGM 仅需 **347 CPU‑小时**，相比 DGM 的 2385 CPU‑小时加速 6.86 倍，相比 SICA 的 572 CPU‑小时加速 1.65 倍。

这些结果表明，HGM 的谱系级元生产力估计与解耦策略不仅提升了最终智能体的质量，更大幅降低了搜索的计算成本。效率提升的核心机制在于：解耦扩展与评估使 HGM 能够自适应地决定何时生成新智能体、何时深入评估已有智能体，避免了对低潜力谱系的过度投入；而异步并行实现（HGM Async）则进一步将墙钟时间压缩到实用水平。

### 与人类设计智能体的对比

HGM 发现的智能体展现出超越同期人类工程化智能体的能力。在完整的 **SWE‑bench Verified** 上，经过 8000 次评估后，HGM 的最佳信念智能体取得了 **61.4%** 的准确率，比基于 GPT‑5 mini 的最强人类设计智能体 SWE‑agent（53.2%）高出 8.2 个百分点。

泛化实验（Table 3）进一步验证了 HGM 智能体的鲁棒性。在完全未见过的 **SWE‑bench Lite（Filtered）** 设置下，HGM 智能体在 GPT‑5 mini 上取得 **40.1%** 准确率；当切换到更强的 **GPT‑5** 模型并采用标准排行榜设置时，准确率提升至 **49.0%**，与最强的人工工程化智能体持平。在 **SWE‑Bench‑Live Lite** 上，HGM 智能体配合 GPT‑5.1 Codex mini 取得 **27.0%** 准确率，超越了此前的领先成绩 24.7%，达到了新的 state‑of‑the‑art。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_T0EiEuhOOL/figures/004_Table_3.jpg]]
*Table 3: Generalization on SWE-Lite and GPT-5. We report the accuracy of HGM’s best-belief SWE-Verified agent on SWE-Lite with GPT-5 mini and GPT-5 under two settings: filtered (completely unseen) and standard (leaderboard setting)*

### 消融分析：策略解耦与效率增益

虽然论文未提供逐组件的严格消融实验，但 Table 2 的效率对比本身构成了对策略解耦的强有力验证。DGM 和 SICA 均采用扩展与评估绑定的固定流程——每次扩展后立即评估新生成的子智能体，且通常评估所有任务。这种刚性导致大量计算资源被浪费在低潜力谱系上。

HGM 的复合策略将扩展与评估完全解耦：每一步自适应决定是扩展还是评估，评估粒度细化为单个智能体‑任务对。这一设计使得 HGM 在相同评估次数下所需 CPU 时间仅为 DGM 的几分之一（SWE‑Verified‑60 上 2.38 倍加速，Polyglot 上 6.86 倍加速），直接证明了策略解耦带来的效率增益。

### 失败模式与局限性

尽管 HGM 展现出显著优势，仍需注意以下局限：

1. **CMP 估计的早期方差**：CMP 估计的质量依赖于已评估的样本数量。在搜索早期或评估预算极低时，谱系统计量稀疏，估计可能具有较大方差，导致 Thompson 采样的探索方向不够精准。
2. **理论假设的脆弱性**：Theorem 1 将 CMP 预言机与 Gödel 机器的最优接受机制联系起来，但其证明严重依赖于假设 1（可重复试验、证明不消耗预算、每步修改消耗固定单位等）。在实际环境中，这些假设可能不完全成立，HGM 的近似质量可能下降。
3. **基准泛化性有限**：实验仅在 SWE‑bench 和 Polyglot 两个以软件工程任务为主的基准上验证。对更广泛的编程任务（如算法竞赛、系统编程）或其他类型智能体系统的泛化性尚待考察。
4. **超参数敏感性未充分探索**：探索‑开发调度器 τ、ϵ 百分位、UCB‑Air 的 α 等超参数在当前实验中表现良好，但未开展系统的灵敏度分析，其最优设置可能依赖于具体任务和预算规模。
5. **计算成本仍较高**：尽管效率大幅优于基线，HGM 仍需要较大量 LLM 调用，整体实验成本约 5000 USD，对资源有限的用户可能不够友好。

### 图表结论摘要

| 图表 | 核心结论 |
|------|---------|
| Figure 1（左） | 单智能体性能指标与长期自改进能力相关性弱，HGM 通过 CMP 显著缓解此不匹配 |
| Figure 1（右） | HGM 在 SWE‑bench Verified 上以更少 CPU 时间取得更高准确率 |
| Table 1 | HGM 的 CMP 估计器与经验 CMP 的加权相关系数（0.778/0.626）远超 DGM 和 SICA |
| Table 2 | HGM 在准确率（56.7%/30.5%）和效率（2.38×–6.86× 加速）上全面领先基线 |
| Table 3 | HGM 智能体泛化到 SWE‑Lite，在 GPT‑5 上达到与最强人类设计智能体持平的性能（49.0%） |
| Table 4 | HGM 通过解耦扩展与评估、Thompson 采样选择、最佳信念最终选择，实现了结构化树搜索策略的系统性改进 |

## 方法谱系与知识库定位

### 1. 与先前自改进方法的关系

HGM 的核心贡献在于将自改进形式化为树搜索问题，并通过谱系级元生产力（Clade-Metaproductivity, CMP）指导搜索，显著缓解了元生产力与即时基准性能的不匹配。在方法谱系上，HGM 直接继承并重构了两个先前工作的关键设计：

- **Darwin Gödel Machine (DGM)**（Zhang et al., 2025a）：同样将自改进视为树搜索，但依赖单智能体在基准上的准确率作为贪心选择信号。HGM 保留了 DGM 的树搜索框架，但将其指导指标从“单智能体经验均值”替换为“谱系级元生产力估计器 $\widehat{\mathrm{CMP}}(a)$”，并将扩展选择从贪心策略改为基于 CMP 的 Thompson 采样。这一改动是性能提升的因果枢纽——Table 1 显示 DGM 的指标与经验 CMP 的加权相关系数仅为 0.285（SWE‑Verified‑60），而 HGM 达到 0.778。

- **Self-Improving Coding Agent (SICA)**（Robeyns et al., 2025）：通过自修改代码库进行自我改进，但其扩展与评估严格耦合（每次扩展后立即评估所有新子智能体）。HGM 将扩展与评估完全解耦，每一步自适应决定是生成新智能体还是进一步探测已有智能体，评估粒度细化为单个智能体‑任务对。Table 2 显示，HGM 在 SWE‑Verified‑60 上仅需 517 CPU‑小时，而 DGM 需 1231 CPU‑小时，SICA 则因查询超长而提前终止——解耦策略是效率提升的关键。

Table 4 系统对比了三者在选择策略、扩展策略、评估策略上的结构化差异，HGM 在每个子策略上均引入了基于 Thompson 采样的自适应机制，而非固定的贪心或顺序策略。

### 2. 理论根基

HGM 的理论锚点是 Gödel 机器的最优自修改机制。在假设 1（可重复试验、证明不消耗预算、每步修改消耗固定单位）下，Theorem 1 证明：访问真实 CMP 预言机足以实现 Gödel 机器的接受/拒绝策略。HGM 通过 CMP 估计器 $\widehat{\mathrm{CMP}}(a) = n_{\mathrm{success}}^C(a) / (n_{\mathrm{success}}^C(a) + n_{\mathrm{failure}}^C(a))$ 近似该预言机，以轻量方式逼近理论最优。

与 Gödel 机器的纯理论框架不同，HGM 将自改进落地为可操作的树搜索策略，其“谱系”概念借鉴了 Huxley 的进化生物学隐喻——CMP 聚合智能体整个后代谱系的表现，而非仅看其自身基准得分。

### 3. 适用边界

HGM 的设计假设和实验设置定义了其当前适用边界：

- **任务域**：实验仅在 SWE‑bench（软件工程修复任务）和 Polyglot（多语言编程任务）上验证。对更广泛的编程任务（如算法竞赛、代码生成）或其他类型智能体系统（如机器人控制、电子设计自动化）的泛化性尚待考察。
- **骨干模型**：实验使用 GPT‑5/GPT‑5 mini 和 Qwen3‑Coder 系列。HGM 的 CMP 估计质量可能依赖于底层 LLM 的自修改能力——若模型本身难以产生有意义的后代变异，谱系级统计将失去信息量。
- **计算预算**：完整实验成本约 5000 USD，HGM 虽比 DGM 快 2.38–6.86 倍，但仍需大量 LLM 调用，对资源有限的用户不友好。
- **理论假设**：Theorem 1 的保证严重依赖假设 1。在真实环境中，任务可能不可重复、证明可能消耗预算、修改成本可能非均匀，这些都会削弱 CMP 预言机与 Gödel 机器之间的等价性。

### 4. 局限与开放问题

**已知局限**：
1. CMP 估计的质量受限于已评估样本数量。在搜索早期或评估预算极低时，$\widehat{\mathrm{CMP}}(a)$ 可能具有较大方差，导致 Thompson 采样的探索效率下降。
2. 超参数（探索‑开发调度器 τ、ϵ 百分位、UCB‑Air 的 α）虽在当前实验中表现良好，但未系统开展灵敏度分析，其最优设置在跨域迁移时可能不稳健。
3. HGM 仅在两个以软件工程为主的基准上验证，对需要长期规划、多轮交互或开放式探索的编程任务的适用性未知。

**开放问题**：
- HGM 能否从代码层自修改扩展到直接修改模型权重，从而释放更深层的元学习潜力？
- 在非重复试验或动态环境中，CMP 的估计是否仍然可靠？是否需要引入时间衰减或上下文感知的谱系统计？
- 能否通过更高效的代理模型（如小型预测网络）估计 CMP，进一步降低计算成本？
- CMP 的收敛性质和后悔界能否从理论上进行更精细的分析，以指导超参数的自适应调整？
- 谱系级元生产力的概念能否推广到其他智能体开发范式（如电子设计自动化中的电路优化、机器人策略搜索中的行为树演化）？

## 原文 PDF

![[paperPDFs/ICLR_2026/Huxley_Gödel_Machine_Human_Level_Coding_Agent_Development_by_an_Approximation_of_the_Optimal_Self_Improving_Machine.pdf]]
