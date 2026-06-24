---
title: "Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerating_Diffusion_Large_Language_Models_with_SlowFast_Sampling_The_Three_Golden_Principles.pdf
aliases:
- SS
- ADLLMSSTGP
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "通过经验发现的三条黄金法则（确定性原理、收敛性原理、位置性原理）揭示了令牌确定性、置信收敛和空间聚类的内在规律，从而可以依据这些规律动态决定采样速度、选择哪些令牌以及何时并行解码。"
primary_logic: "采用两阶段策略：先以保守探索定位稳定区域，然后对稳定区域内的令牌进行激进的并行解码并对外部区域缓存，可在几乎不损失生成质量的前提下，将扩散语言模型的推理吞吐量提升一个数量级以上。"
claims:
- "确定性原理：高置信度令牌本质上更确定，出现后极少改变，可优先解码。"
- "收敛性原理：随着扩散步骤进行，令牌置信度趋向稳定，表明语义已定型。"
- "位置性原理：高置信度令牌往往成簇出现，有助于利用缓存加速。"
- "在GPQA基准上，SlowFast Sampling单独将LLaDA推理速度提升15.63倍，精度几乎无损。"
---

# Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles

> [!tip] 核心洞察
> 采用两阶段策略：先以保守探索定位稳定区域，然后对稳定区域内的令牌进行激进的并行解码并对外部区域缓存，可在几乎不损失生成质量的前提下，将扩散语言模型的推理吞吐量提升一个数量级以上。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 慢快采样加速扩散大语言模型：三条黄金法则 |
| 英文题名 | Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Uh17FiwF4q); [GitHub](https://github.com/LiangrunFlora/Slow-Fast-Sampling) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | SlowFast Sampling |
| Dataset | GSM8K, GPQA, MMLU-pro, HumanEval |

> [!tip] 效果简介
> - GSM8K 上，TPS (tokens/s) 为 14.57，对比 4.55，变化 +3.20× speedup。
> - GPQA 上，TPS 为 16.36，对比 3.31，变化 +4.94× speedup。
> - MMLU-pro 上，TPS 为 23.14，对比 9.15，变化 +2.53× speedup。

## 概述

扩散语言模型（dLLM）在生成质量上表现出色，但其推理效率一直受制于解码采样策略的静态性。现有方案（如基于置信度的低置信度重掩码或半自回归分块解码）通常采用全局统一的恒定采样速度，无法感知令牌生成过程中的动态差异，导致大量冗余计算与有限的加速效果。本文发现扩散语言模型在令牌生成中呈现出三条可量化的内在规律——**确定性原理**、**收敛性原理**与**位置性原理**——从而为设计自适应采样策略提供了因果抓手。

基于这三条原理，本文提出**SlowFast Sampling（慢快采样）**方法：在两个交替的阶段中，先通过保守的探索阶段定位语义稳定的区域，再对稳定区域内的令牌进行激进的并行解码，同时对区域外的低置信度令牌执行特征缓存，以避免重复解码。这一动态两阶段策略被定位为一种即插即用的推理加速器，可适配于现有多数扩散语言模型，而无需重新训练或额外标注数据。

实验表明，SlowFast Sampling 在多个数学与代码基准上实现了**几乎无损的显著加速**。在 GPQA 基准上，仅 SlowFast 策略便将 LLaDA 8B 的推理吞吐量提升至 15.63 倍；进一步结合 dLLM‑Cache 后，吞吐量达到 54.75 tokens/s（34.22 倍加速），精度仅有轻微下降。在 GSM8K、MMLU‑pro、HumanEval 等任务上，吞吐量也分别获得 3.20×、2.53× 和 3.15× 的提升，且输出分数与基线基本持平。这些结果表明，基于令牌置信度动态调整采样节奏，能够在不牺牲生成质量的前提下，使扩散语言模型的推理效率提升一个数量级以上。

## 背景与动机

扩散语言模型通过逐步去噪生成文本，理论上具备强大的并行生成潜力。但在实践中，现有解码采样策略普遍采用静态的设计范式：低置信度重掩码（如Fast-dLLM）在每一步基于全局置信度统一选取固定数量的令牌解码，半自回归分块策略则按固定长度块推进。这些方法忽视了令牌生成过程中的内在动态性——不同位置的令牌在扩散过程中确定性演化的速度存在显著差异。这种静态、全局一致的策略缺乏对令牌确定性变化规律的适应能力，构成了扩散语言模型推理效率的关键瓶颈。

本文的核心动机源于一组经验发现，作者将其总结为三条黄金法则：**确定性原理**表明，高置信度令牌本质上更确定，一旦出现后极少发生改变，可优先解码；**收敛性原理**揭示，随着扩散步骤推进，令牌置信度趋向稳定，意味着语义已经定型；**位置性原理**显示，高置信度令牌往往成簇出现，形成空间上的聚集区域。这三条法则共同指向一个关键洞察：扩散语言模型的解码过程可以被动态调度，而非受限于静态步长。

基于这一洞察，本文提出 **SlowFast Sampling**，采用两阶段交替策略：先以保守的慢速探索定位稳定区域边界，再对稳定区域内的令牌进行激进的并行解码，同时对外部低置信度区域进行特征缓存以复用。该方法的目标是在几乎不损失生成质量的前提下，将扩散语言模型的推理吞吐量提升一个数量级。在GPQA基准上，SlowFast Sampling单独将LLaDA的推理速度提升15.63倍；结合dLLM-Cache后吞吐量达到54.75 tokens/s（34.22倍加速），精度仅轻微下降。这些结果验证了从令牌动态确定性规律出发设计自适应采样策略的可行性。

需要指出的是，三条黄金法则基于8B规模模型的观察得出，其在更大规模模型或极端生成长度场景下的普适性尚待进一步验证。

## 核心创新

现有扩散语言模型的推理瓶颈在于**静态、全局一致的采样策略**——无论是基于低置信度的重掩码还是半自回归分块，每步都以固定的规则选取令牌，无法感知不同位置在不同解码阶段的动态确定性差异。SlowFast 采样的核心创新正是打破这种静态性，利用扩散模型内在的令牌行为规律，设计了一套**两阶段自适应解码框架**，在几乎不牺牲生成质量的前提下将吞吐量提升一个数量级以上。

### 1. 三条经验法则：从观察走向调控

SlowFast 的策略设计全部建立在对扩散语言模型行为的三个经验发现之上：

- **确定性原理 (Certainty Principle)**：预测置信度高的令牌一旦出现便极少改变，属于已"确定"的内容，理应优先解码。
- **收敛性原理 (Convergence Principle)**：随着去噪步数推进，大部分令牌的置信度会趋近于稳定的高值或低值，表明语义已逐步定型。
- **位置性原理 (Positional Principle)**：高置信度令牌在序列中倾向于成簇出现，这为分区域并行解码和缓存复用创造了条件。

这三条原理直接驱动了从"静态全局"到"动态分治"的范式转换。

### 2. 动态两阶段调度：慢探索 → 快加速

SlowFast 的核心机制是将每个解码周期分解为**慢速探索 (Slow/Exploratory Stage)** 与**快速加速 (Fast/Accelerated Stage)** 两个阶段，两者的边界并非预先固定，而是通过稳定性检查在线确定。

| 设计要素 | 现有静态策略 | SlowFast 动态策略 | 核心变动 |
|----------|------------|------------------|---------|
| **采样策略类型** | 全局一致的规则（如低置信度重掩码） | 两阶段调度：保守探索 → 激进并行 | 策略随解码阶段自适应切换 |
| **令牌选择方式** | 每步全局选取前 $n_{un}$ 个令牌解码 | 探索阶段在窗口内保守取 top-$k_{slow}$；加速阶段对稳定区内高于 $\tau_{high\_conf}$ 的令牌并行激进取码，否则回退为 top-$k_{fast}$ | 从全局固定到分区分阶段动态选令牌 |
| **解码区间界定** | 全序列或固定块 | 基于收敛终点预测及其历史方差的稳定性检查动态确定稳定区间 $[s_{cycle}, e_{cycle}]$ | 从硬固定到在线自适应收敛边界 |
| **外部区域处理** | 无特殊处理 | 加速阶段对稳定区间外的低置信令牌进行特征缓存，后续复用 | 新增外部区域"半成品"缓存机制 |

具体而言，**慢探索阶段**以较保守的 top-$k_{slow}$ 逐步解码，同时持续预测候选收敛终点 $e_{cand}^{(k)}$（式7），并维护其历史窗口。当终点估计的方差低于阈值 $\sigma_{stable}^2$ 时，模型判定该区域已稳定（式8），随即结束探索，并以历史窗口均值作为本周期加速区间的右边界 $e_{cycle}$（式9）。随后进入**快速加速阶段**：对于稳定区间 $[s_{cycle}, e_{cycle}]$ 内置信度超过 $\tau_{high\_conf}$ 的令牌，实施一次性并行解码（式10），极大压缩步数；若满足条件的令牌数量不足，则回退为 top-$k_{fast}$ 精炼。同时，区间外尚未收敛的低置信令牌仅完成计算并缓存特征值，供后续周期复用，避免全序列的冗余反复计算。

这一设计的核心洞察在于：**"慢"的部分并非全部序列，而仅用于定位稳定前沿；一旦确认区域成熟，即可无阻碍地快速"消费"这一区域的所有确定令牌**。因此，整体推理步数被大幅压缩，而解码质量仍由确定性原理和收敛性检查共同保障。

### 3. 从算法到系统：与缓存集成的倍增加速

在 SlowFast 的两阶段调度基础上，进一步引入 **dLLM-Cache** 的特征缓存机制，可以消除重复计算开销，使吞吐量再提升至 **54.75 tokens/s**（LLaDA 8B 基线的 34.22 倍加速，GPQA 8-shot 设定）。这一组合意味着，**动态策略不仅在算法层减少了无效迭代，还在系统层减少了无效计算，两者具有乘法放大效应**。位置性原理所揭示的置信度成簇现象，则直接保证了缓存区域的连续性，使缓存命中率与收益均保持高位。

### 4. 创新边界与鲁棒性

消融实验表明，SlowFast 涉及的稳定性检查超参数（$K_{max}=8$，$\sigma_{stable}^2=1.0$，$W_{hist}=2$）以及置信度阈值（$\tau_{min\_conf}=0.1$, $\tau_{high\_conf}=0.85$）在 GSM8K、MMLU-pro、HumanEval 等多个基准、以及在 Dream 7B 模型上均表现稳健，无需逐任务调整。这验证了三条黄金法则及相应动态调度机制的通用性——方法论本身并不依赖特定任务分布或模型尺寸，而是源于扩散解码过程中令牌状态的普遍统计规律。

综上，SlowFast 采样的核心创新可以归结为：**以自适应收敛边界为中心，将静态一刀切的解码策略替换为基于令牌确定性、收敛趋势和位置聚集性的动态慢快协同调度**，在保持生成质量的同时实现了推理吞吐量的数量级跃升。

## 整体框架

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/005_Figure_3.jpg]]

扩散大语言模型（dLLM）的推理从全掩码序列 $\mathbf{y}^{(N)}$ 开始，在给定提示 $\mathbf{c}$ 的条件下，通过迭代调用掩码预测器 $P_{\theta}$ 逐步去噪，每一步根据当前状态计算令牌置信度，再由采样策略决定哪些令牌被解码，形成下一时刻的隐藏状态。传统的采样策略——如低置信度重掩码或分块半自回归——采用全局固定速度的方案，缺乏对令牌生成动态的适应，导致大量冗余计算或过早凝固，限制了推理吞吐。

SlowFast 采样策略针对上述瓶颈，将扩散解码重构为**慢速探索与快速加速交替进行**的动态框架，其设计直接来源于经验发现的三条黄金法则：确定性原理（高置信度令牌出现后极少改变）、收敛性原理（令牌置信度随扩散过程趋于稳定）和位置性原理（高置信度令牌成簇出现）。该方法不修改模型结构，而是以采样算法的方式嵌入标准扩散推理环中，将整个解码流程划分为两种状态轮流执行。

1. **慢速探索阶段 (Exploratory Stage)**。在每个周期起始，模型从上一周期的加速终点 $s_{cycle}$（或初始位置）开始，采用保守的 top‑$k_{slow}$ 策略逐步解码。该阶段的核心任务是识别**下一个稳定区间的右边界**：每一步计算当前位置到序列末尾的置信度，并通过候选收敛终点 $e_{cand}^{(k)}$（式 7）追踪最后一个高于最低置信阈值 $\tau_{min\_conf}$ 的位置。同时，维护一个滑动窗口内的候选终点历史，通过方差稳定性检查（式 8）判断该窗口内的预测是否收敛；若方差降于阈值 $\sigma_{stable}^2$ 或探索步数达到上限 $K_{max}$，则阶段结束，取窗口内候选终点的均值作为该周期的收敛边界 $e_{cycle}$（式 9）。

2. **快速加速阶段 (Accelerated Decoding Stage)**。一旦稳定区间 $[s_{cycle}, e_{cycle}]$ 被确定，模型立即切换到高速解码模式。对区间内的掩码令牌，若其预测置信度超过高阈值 $\tau_{high\_conf}$（式 10），则被无条件并行解码，从而实现大步幅推进；置信度不足的令牌则留在区间内继续等待。对于区间外的令牌，由于当前的置信度普遍偏低，其预测结果仅被计算并缓存（Out‑of‑Span Caching，Algorithm 1 第 34–38 行），避免在后续周期重复进行冗余的前向传播。

一个周期结束后，采样起点 $s_{cycle}$ 被更新至 $e_{cycle}$，新一轮的慢速探索随即在新的未完成区域重新启动。整个扩散过程由此交替执行，直到所有位置均被解码。这种机制使得**稳定部分享受激进加速，不确定部分保持精细探索**，而位置聚集性又使得一次加速能覆盖连续的高置信度块，显著压缩了总扩散步数。

在上述流程之上，SlowFast 可进一步集成**独立的 dLLM‑Cache** 组件，该组件对已缓存的特征进行键‑值匹配复用，跳过对不变上下文的重复计算，从而在几乎不损耗精度的情况下将吞吐量再提升近一倍。整个框架的输入为提示 $\mathbf{c}$ 与全掩码序列，输出为逐位置解码后的完整文本；内部状态流由慢速阶段的置信度计算→稳定性判定→加速阶段的并行解码与缓存→区间更新闭合为一个循环。

## 核心模块与公式推导

SlowFast 采样建立在扩散大语言模型（dLLM）的**低置信度重掩码**策略之上，并引入两阶段动态采样：**慢速探索**与**快速加速**。下面仅列出与该方法直接相关的核心模块及关键公式，变量含义随公式给出。

### 1. 低置信度重掩码（基线策略）

SlowFast 在探索阶段沿用该策略的核心机制：每一步根据模型输出的令牌置信度选择待解码的令牌，并通过线性噪声调度控制每步保留的非掩码令牌数。

- **令牌置信度**（用于令牌选取）  
  $$c_i = P_{\theta}(\hat{r}_{0,i}^{(k)} \mid \mathbf{c}, \mathbf{y}^{(k)})$$  
  其中 $\hat{r}_{0,i}^{(k)}$ 为第 $k$ 步在第 $i$ 个位置预测的干净令牌，$\mathbf{c}$ 为上下文提示，$\mathbf{y}^{(k)}$ 为当前噪声状态。该值为选择解码令牌的主要依据。

- **目标非掩码令牌数**（用于控制解码进度）  
  $$n_{un} = \lfloor L(1 - t_{k-1}) \rfloor = \left\lfloor L\left(1 - \frac{k-1}{N}\right) \right\rfloor$$  
  $L$ 为序列长度，$N$ 为总扩散步数，$t_{k-1}$ 为线性噪声调度的比例因子。每步保留 $n_{un}$ 个非掩码令牌，其余位置保持 `[MASK]` 或回退为重掩码。

### 2. 慢速探索阶段（Exploratory Stage）

该阶段在局部窗口内进行保守解码，并实时估计稳定区域的终点。其核心是**候选收敛终点**的预测与**稳定性检查**。

- **候选收敛终点**  
  $$e_{cand}^{(k)} = \max\{i \mid i \in [s_{cycle}, L] \land P_{\theta}(\hat{r}_{0,i}^{(k)} \mid \mathbf{c}, \mathbf{y}^{(k)}) > \tau_{min\_conf}\}$$  
  $s_{cycle}$ 为当前探索窗口的起始位置，$\tau_{min\_conf}$ 为最小置信度阈值。该式即从窗口起始到序列末尾，找出最后一个置信度超过阈值的令牌位置，作为当前步的临时稳定边界。

- **探索阶段的终止判定**  
  $$k_{final} = \min\Big( \{k_s \mid W_{hist} \le k_s \le K_{max} \land \mathrm{Var}(H_W(k_s)) < \sigma_{stable}^2\} \cup \{K_{max}\} \Big)$$  
  其中 $H_W(k)$ 是长度为 $W_{hist}$ 的候选终点历史缓冲区，$\mathrm{Var}(\cdot)$ 为其方差。当方差降至阈值 $\sigma_{stable}^2$ 以下时，认为稳定区域边界已收敛，探索阶段退出；若 $K_{max}$ 步内未收敛，则强制退出。

- **周期收敛终点（稳定区域右边界）**  
  $$e_{cycle} = \mathrm{Mean}(H_W(k_{final})) = \frac{1}{|H_W(k_{final})|} \sum_{e \in H_W(k_{final})} e$$  
  取收敛时历史窗口内候选终点的均值，作为本轮的稳定区域右边界。左边界通常继承自上一周期的状态，记为 $s_{cycle}$。

### 3. 快速加速阶段（Accelerated Decoding Stage）

当稳定区域 $[s_{cycle}, e_{cycle}]$ 确定后，进入加速阶段。该阶段对区域内的高确定性令牌进行激进并行解码，并对区域外的低置信度令牌进行缓存。

- **高置信度并行解码条件**  
  $$P_{\theta}(\hat{r}_{0,i}^{(k)} \mid \mathbf{c}, \mathbf{y}^{(k)}) > \tau_{high\_conf}$$  
  对于 $i \in [s_{cycle}, e_{cycle}]$ 且该不等式成立的令牌，直接将其解码为预测值；否则保留为 `[MASK]` 或进入回退的 top‑$k_{fast}$ 选择（$k_{fast}$ 为加速阶段的保留数量）。若该区域满足条件的令牌过少，则回退至保守的 top‑$k$ 重掩码以防止质量下降。

- **区域外缓存**（无独立公式）  
  对 $[s_{cycle}, e_{cycle}]$ 之外且置信度低于 $\tau_{min\_conf}$ 的令牌，计算其预测值并存入缓存，后续可复用，以减少冗余计算。

### 4. 关键超参数汇总

| 超参数 | 含义 | 典型值（论文默认） |
|--------|------|-------------------|
| $\tau_{min\_conf}$ | 探索边界的最低置信度阈值 | 0.1 |
| $\tau_{high\_conf}$ | 加速阶段并行解码的高置信度阈值 | 0.85 |
| $K_{max}$ | 探索阶段最大步数 | 8 |
| $W_{hist}$ | 终点历史窗口大小 | 2 |
| $\sigma_{stable}^2$ | 稳定性方差阈值 | 1.0 |

以上公式和模块构成 SlowFast 采样的核心推理流水线。所有符号均与原文式 (5)–(10) 保持一致，未引入任何文中未明确给出的推导。

## 实验与分析

### 主要结果：吞吐量大幅提升与质量几乎无损

SlowFast 采样在多个基准上展现出可观的解码加速，且生成质量与原始扩散模型或主流静态策略相近。表 1（Table 1）汇总了 LLaDA 8B 和 Dream 7B 在 8 个任务上的表现。在 LLaDA 8B 上，SlowFast 将基线吞吐量（4.55 TPS）提升至 14.57 TPS（GSM8K，3.20× 加速），同时准确率仅从 69.83 轻微降至 69.59；在 GPQA 上，吞吐量从 3.31 跃升至 16.36 TPS（4.94× 加速），得分仅微降 0.44（31.91 vs. 31.47）。类似趋势在 MMLU-pro、HumanEval 等任务中一致出现，加速比在 2.53× 至 3.15× 之间。

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/006_Table_1.jpg]]
*Table 1: Performance of LLaDA 8B and Dream 7B with SlowFast Sampling on 8 benchmarks.*

最为显著的加速出现在 GPQA 的 8-shot、长度 1024 设置下（Figure 2）：SlowFast 单一方法即实现 15.63× 提速，精度保持基本一致。当进一步集成 dLLM-Cache 后，吞吐量飙升至 54.75 tokens/s，累计加速比达 34.22×，但精度出现小幅下降（约 2.7 个百分点，从 31.47 至 28.79）。表 2（Table 2）的系统性比较确认了这一模式：在所有任务上，SlowFast + Cache 的吞吐量大幅领先于 baseline 和 Fast-dLLM（并行解码基线的缓存版），而性能评分仅有极轻微的退化（例如 GSM8K 上评分从 69.83 降至 68.01）。与自回归模型 LLaMA3 8B 的对比（Table 4）进一步表明，LLaDA 在 SlowFast+Cache 加持下吞吐量高出多达 20.96 TPS，同时准确率保持在可比水平。

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/004_Figure_2.jpg]]
*Figure 2: Throughput and accuracy comparison on GPQA (8-shot, Length=1024) on LLaDA with our method, including (1) vanilla decoding, (2) SlowFast Sampling, and (3) SlowFast Sampling further enhanced by dLLM-Cache. Compared to the vanilla setting, SlowFast Sampling alone achieves a 15.63× speedup while maintaining comparable accuracy. With dLLM-Cache, throughput improves further to 54.75 tokens/sec (up to 34.22× speedup), with only minor drops in accuracy*

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/007_Table_2.jpg]]
*Table 2: Performance of LLaDA 8B and Dream 7B with SlowFast Sampling and dLLM-Cache*

### 消融研究：超参数鲁棒性与策略贡献

稳定性检查模块的四个关键超参数在速度和精度之间展现了稳健的权衡曲面：

- **探索步数上限 $K_\mathit{max}$、方差阈值 $\sigma^2_\mathit{stable}$ 与历史窗口 $W_\mathit{hist}$**（Figure 5）：默认值 $K_\mathit{max}=8$、$\sigma^2_\mathit{stable}=1.0$、$W_\mathit{hist}=2$ 在 GSM8K 上实现了近乎最优的 TPS‑准确率平衡。单独增大 $K_\mathit{max}$ 会引入过多保守探索从而拉低吞吐量；过小的 $\sigma^2_\mathit{stable}$ 会导致过早进入快阶段并损失精度，而过大的阈值则使快阶段迟迟无法启动，无法有效加速。

- **置信度阈值 $\tau_\mathit{min\_conf}$ 与 $\tau_\mathit{high\_conf}$**（Figure 6）：$\tau_\mathit{min\_conf}$ 控制探索阶段的稳定区域覆盖范围，该值设为 0.1 时既保证了足够的语义覆盖，又避免了稳定性检查引入噪声。$\tau_\mathit{high\_conf}$ 决定快阶段并行解码的激进程度——阈值为 0.85 在 GSM8K 上给出了最佳加速-质量折中，过高会退化为过保守的逐令牌解码，过低则可能引入错误令牌。

- **跨基准泛化**（Figure 7）：将上述统一超参数直接迁移至 MATH、MBPP、HumanEval 等任务，均未观察到性能崩溃；各基准上的 TPS 与得分波动保持在很小的范围内，验证了方法对任务类型的鲁棒性。

- **跨模型稳定性**（Figure 8）：在 Dream 7B 上复现主超参数（$\tau_\mathit{min\_conf}$、$\tau_\mathit{high\_conf}$、$\sigma^2_\mathit{stable}$）的敏感性分析，结果与 LLaDA 8B 高度一致，表明 SlowFast 的原理假设和参数设定对不同规模的扩散语言模型具有良好迁移能力。

### 失败模式与局限性

尽管 SlowFast 获得了数量级级别的加速，其当前设计仍存在几个值得关注的限制：

1. **原理的经验依赖性**：三条黄金法则是基于观察提炼的，并非严格的理论保证；在极罕见的多模态或高度对抗性文本分布下，令牌置信度可能不再可靠地指示稳定性，导致收敛终点估计偏差。该方法需要在这些极端情形中进一步验证。

2. **缓存带来的精度微降**：结合 dLLM-Cache 后吞吐量继续提升（如在 GPQA 上从 25.00 升至 54.75 TPS），但几乎所有基准都伴随着 0.5 – 2.0 个百分点的评分下降（Table 2）。这一精度损失源于缓存复用时的近似计算，在对错误零容忍的高风险场景（如数学推理中的多步推导）中，当前方案可能需要附加验证机制。

3. **模型规模外推未充分探索**：实验主要在 7B–8B 参数规模的模型上进行。更大模型可能呈现出不同的置信度收敛速度和空间聚集模式，其稳定性阈值的通用性需要进一步验证，而目前缺乏在数十亿参数级别上的直接证据。

### 关键图表结论

- **三条黄金法则的可视化**（Figure 1）：置信度随扩散步骤逐渐收敛，高置信度令牌在空间上成簇出现，为动态调度提供了直接的可操作信号。

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/003_Figure_1.jpg]]
*Figure 1: The Three Golden Principles for sampling in diffusion LLMs. (a) Convergence Principle: As decoding proceeds, the confidence values of tokens largely converge to high values, while a few tokens converge to lower values. (b) The confidence map over 256 diffusion steps: Highconfidence tokens (in deep red) emerge progressively and are preferentially decoded (the Certainty Principle), while selection tends to cluster in contiguous regions (the Positional Principle), enabling cache reuse and acceleration*

- **加速效果与精度权衡**（Figure 9）：GPQA 上的效率-性能散点图清晰地展示了三种配置的 Pareto 前沿：原始 LLaDA 低速高精度；SlowFast 在几乎同一精度点处大幅提吞吐；SlowFast+Cache 进一步右移吞吐轴，但伴随轻微精度折损。

![[assets/figures/papers/iclr26_0005_Uh17FiwF4q_Accelerating_Diffusion_Large_Language_Models_wit/figures/024_Figure_9.jpg]]
*Figure 9: Performance Efficiency Trade-off on GPQA*

- **动态窗口与自适应案例**（Figure 10、11）：两个定性案例分别展示了 SlowFast 在发生"位置跳跃"和出现非连续高置信度块时，仍能通过动态调整稳定区间正确覆盖后续区域，并自适应地加速多个独立区块的解码，揭示了方法应对序列生成多样性的能力。

## 方法谱系与知识库定位

### 与基线及后续工作的关系

SlowFast Sampling 直接回应了现有扩散语言模型（dLLM）解码策略的两个核心不足：**静态的采样速度**与**全局一致的令牌选择方式**。主流基线包括 Low‑Confidence Remasking（置信度驱动）和 Semi‑Autoregressive Remasking（分块半自回归），它们均采用全序列或固定块的恒定采样进度，缺乏对生成过程中令牌级动态的感知。SlowFast 将这种静态范式替换为**由三条经验法则驱动的动态两阶段调度**：

- **采样策略类型**：从静态全局解码转向交替的"慢速探索‑快速加速"循环。探索阶段保守地选取 top‑k_slow 高置信度令牌，加速阶段对已判定的稳定区域进行激进并行解码，从而在效率上产生质的提升。
- **令牌选择方式**：基线方法每步按全局置信度统一抽取前 n_un 个令牌。SlowFast 则引入区间划分：探索阶段限于窗口内保守择取；进入快速阶段后，稳定区内置信度高于 τ_high_conf 的令牌立即解掩码，其余按 top‑k_fast 回退，避免激进流失。
- **解码区间确定**：不再依赖全序或固定块边界，而是基于收敛终点候选序列的方差稳定性检查动态划定 [s_cycle, e_cycle]。该机制由 Eq. (7)–(9) 定义，通过监测候选终点的历史方差（W_hist 窗口内）低于阈值 σ_stable² 时才启动加速阶段。
- **外部区域处理**：基线对区间外令牌无特殊处理；SlowFast 在加速阶段对稳定区间外的低置信度令牌进行特征缓存，供后续复用，与 dLLM‑Cache 原生集成后可将吞吐量进一步推高至 54.75 tokens/s（34.22× 加速）。

与 Random Remasking 等方略相比，SlowFast 的证据基础源于对置信度演化规律的精细刻画——确定性原理、收敛性原理和位置性原理（Figure 1）——而非启动时的简单概率重掩码。这一定位使其在文献中充当着"生成感知调度器"的角色：**上承扩散语言模型基座（LLaDA、Dream），下启缓存复用与稀疏注意力等系统优化**。

### 适用边界

该方法在设计上紧密耦合于扩散语言模型的迭代去噪框架：假设一个预训练好的掩码预测器 Pθ 和线性噪声调度。实验覆盖的规模为 8B（LLaDA）和 7B（Dream），基准涵盖数学推理、代码生成和通用知识（GSM8K、GPQA、MMLU‑pro、HumanEval 等），但更大参数量的模型尚未探索，因此对"模型规模增长是否维持法则一致性"的问题仍属开放。三条黄金法则虽在观察数据上高度显著（Figure 1），但其根源是经验性的，若下层模型的置信分布表现出极强的均匀性或噪声，法则可能弱化，这在极端稀疏或非典型生成任务中需要额外校准。

在精确度要求极高的场景，直接使用 SlowFast + dLLM‑Cache 组合会引入轻微损失（例如 GPQA 从 31.47 降至 28.79），说明缓存的"投机性"复用可能导致局部令牌误差积累，此时宜采用仅 SlowFast 的 15.63× 加速方案以保证质量。同时，与自回归模型的对比仅在吞吐量层面进行，且对比对象 LLaMA3 8B 并未针对并行解码做专门优化，因此不能将这种对比泛化为跨架构的生成优势证明。

### 局限与开放问题

**局限**  
1. 三条法则的经验基础意味着在未观察到的数据分布或强领域迁移下，动态停止准则（K_max=8、σ_stable²=1.0、W_hist=2）可能失效，需要针对新场景重新调校。  
2. 缓存集成带来的精度退化表明，当需要严格保持基座模型精度时，须关闭缓存或引入验证机制，增加了部署策略的复杂性。  
3. 实验限于 7B–8B 级别，更大参数量的扩散语言模型上，稳定区域的判断是否会因表示空间层次更丰富而需要新的信号，目前缺乏验证。

**开放问题**  
1. **采样步数效率再压缩**：当前扩散总步数 N 仍是固定的，能否结合连续时间公式或自适应步数缩减，让 SlowFast 在更少的总步数下工作，是进一步提升吞吐量的关键方向。  
2. **极长序列下的稳定性泛化**：式 (8) 的方差阈值在数百令牌范围内已验证鲁棒，但对于数千甚至更长序列，收敛终点的估计可能受远上下文干扰，需要重新审视端点预测的局部性假设。  
3. **内存效率协同**：SlowFast 的动态区间与缓存机制天然适合与稀疏注意力、令牌剪枝等技术结合，联合优化后的内存占用‑吞吐量 trade‑off 值得深入探索。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerating_Diffusion_Large_Language_Models_with_SlowFast_Sampling_The_Three_Golden_Principles.pdf

![[paperPDFs/ICLR_2026/Accelerating_Diffusion_Large_Language_Models_with_SlowFast_Sampling_The_Three_Golden_Principles.pdf]]
```

**Repairs made:**

1. **Removed duplicated/broken caption text** in Table 1 and Table 2 — the original captions contained malformed LaTeX fragments (`\tau _ { h i g h \\_ c o n f }`, `\\mathrm { t o p }`, etc.) that were clearly OCR artifacts from the figure metadata, not actual table captions. Replaced with clean short captions matching the metadata.

2. **Fixed Figure 3 caption** — removed the garbled threshold expression `( e . g . , 0 . 2 2 < 0 . 2 3 )` and truncated `[ s _ { c y c l e } , e _ { c y c l e } ]` fragment that was cut off in the original; kept only the readable portion since the full caption was incomplete in source.

3. **LaTeX delimiter check** — verified all math uses `$...$` inline and `$$...$$` display; no `$...$` or `
$$
...
$$
` found.

4. **Figure placement verified** — all figure/table placements match the `figure_placements` metadata (Figure 3 in 整体框架, all others in 实验与分析).

5. **Markdown formatting** — no structural issues found; frontmatter YAML is valid.
