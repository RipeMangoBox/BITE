---
title: "Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Overcoming_Joint_Intractability_with_Lossless_Hierarchical_Speculative_Decoding.pdf
openreview_forum_id: LaVrNaBNwM
aliases:
- HSDH
- OJILHSD
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过层次分支重采样和上限前缀比机制，在不同分支间转移多余的概率质量以补偿不足的质量，从而在最后一枚接受令牌后仅用一次重采样即恢复完整的目标分布。"
primary_logic: "分支分歧度的不对称性使得来自“过度分配”分支的多余概率可以被递归地聚合，用于弥补“分配不足”分支的缺陷，因此即使单个分支无法自恢复，整个序列的目标分布也能被精确恢复，且在可访问分支内只需一次重采样即可完成，无需额外目标模型调用。"
claims:
- "HSD通过层次分支重采样和上限前缀比对概率质量进行平衡，从理论上保证了无损恢复。"
- "HSD在GSM8K、HumanEval等多个基准上一致提升块效率（BE）和解码速度（DS），并在集成EAGLE-3后获得超过12%的性能增益。"
- "上限分支重采样（Capped Branch Resampling）允许只进行一次重采样，验证阶段额外耗时不足总解码时间的1%，且HSD验证比块验证更快约20%。"
- "GSM8K 上 Block Efficiency (tokens/step) = 6.64 ± 0.04 (HSD)"
---

# Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding

> [!tip] 核心洞察
> 分支分歧度的不对称性使得来自“过度分配”分支的多余概率可以被递归地聚合，用于弥补“分配不足”分支的缺陷，因此即使单个分支无法自恢复，整个序列的目标分布也能被精确恢复，且在可访问分支内只需一次重采样即可完成，无需额外目标模型调用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无损层次推测解码：克服联合不可解性 |
| 英文题名 | Overcoming Joint Intractability with Lossless Hierarchical Speculative Decoding |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=LaVrNaBNwM); [GitHub](https://github.com/ZhouYuxuanYX/Hierarchical-Speculative-Decoding) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Hierarchical Speculative Decoding (HSD) |
| Dataset | GSM8K, HumanEval, GSM8K (Multi-draft, K=3 or 4), GSM8K (Draft length γ=15) |

> [!tip] 效果简介
> - GSM8K 上，Block Efficiency (tokens/step) 为 6.64 ± 0.04 (HSD)，对比 6.40 ± 0.10 (Tokenwise), 6.51 ± 0.09 (Blockwise)，变化 +3.75% vs Tokenwise, +2.0% vs Blockwise。
> - HumanEval 上，Block Efficiency improvement over Tokenwise 为 +9.5% (14B model), +12.3% (32B model)，对比 Tokenwise，变化 +9.5–12.3%。
> - GSM8K (Multi-draft, K=3 or 4) 上，Average Block Efficiency improvement over Tokenwise 为 +5.9%，对比 Tokenwise with RRS，变化 +5.9%。

## 概述

推测解码（Speculative Decoding）是加速大语言模型自回归生成的主流范式，其核心瓶颈已从草案生成转向**验证阶段**：现有逐令牌验证（Tokenwise Verification, Leviathan et al., 2023）和块验证（Blockwise Verification, Sun et al., 2024）均受制于**联合不可解性（Joint Intractability）**——即无法在保证无损的前提下，充分利用草案序列中多个令牌的联合信息来提升可接受令牌数量。具体而言，逐令牌验证在首个拒绝位置即停止并重采样，丢弃了后续位置的部分信息；块验证虽能联合处理连续令牌，但仅利用了部分信息，提升幅度有限。

本文提出**层次推测解码（Hierarchical Speculative Decoding, HSD）**，一种可证明无损的验证方法。其核心洞见在于**分支分歧度的不对称性**：草案模型在不同分支上的概率分配存在“过度分配”与“分配不足”的不对称现象，来自过度分配分支的多余概率质量可以被递归聚合，用于弥补分配不足分支的缺陷。基于此，HSD通过**层次分支重采样（Hierarchical Branch Resampling）**和**上限前缀比（Capped Prefix Ratio）**机制，在最后一枚接受令牌之后仅需**一次重采样**即可精确恢复完整的目标分布，无需额外调用目标模型。

HSD在方法谱系中位于推测解码的验证优化分支，与逐令牌验证和块验证构成直接对比。其关键改进在于将验证范式从“逐令牌独立接受/拒绝”转变为“从末端向前扫描、基于上限分支分歧度确定最长接受前缀、在单一位置进行上限分支重采样”。接受概率的计算从简单的逐令牌比率 $\min\{1, p(x_t)/q(x_t)\}$ 升级为基于上限分支分歧度 $D_{\mathrm{Branch}}^*$ 的层次接受概率 $h_t$，重采样分布也从原始词汇空间的 $\max(p-q, 0)$ 变为仅需在可访问分支内计算的上限分支重采样概率 $P_{\mathrm{res}}^*$。

实验结果表明，HSD在GSM8K、HumanEval等多个基准上一致提升块效率（Block Efficiency, BE）和解码速度（Decoding Speed, DS）。在GSM8K上，HSD的块效率达到 $6.64 \pm 0.04$ tokens/step，较逐令牌验证提升3.75%，较块验证提升2.0%；在HumanEval上，14B和32B模型分别获得9.5%和12.3%的块效率提升。集成EAGLE-3后，HSD带来超过12%的性能增益。消融实验表明，上限前缀比机制对保持分布保真度至关重要——去除上限后GSM8K任务精度从84.96%降至84.40%，HumanEval从82.47%降至80.61%。验证阶段的额外耗时不足总解码时间的1%，且HSD验证比块验证快约20%。

## 背景与动机

大型语言模型的自回归解码因逐令牌串行生成而成为推理延迟的主要瓶颈。推测解码（Speculative Decoding）通过引入一个轻量级草案模型（draft model）快速生成候选令牌序列，再由目标模型（target model）并行验证，从而在不牺牲输出质量的前提下提升推理速度。其核心在于验证阶段：如何高效地决定接受哪些草案令牌，并在拒绝位置进行重采样以恢复目标分布。

现有验证方法主要分为两类。**逐令牌验证**（Token-wise Verification，Leviathan et al., 2023）对每个草案令牌独立计算接受概率 $h(x_t) = \min\{1, p(x_t)/q(x_t)\}$，并在首次拒绝处从修正分布 $\max(p - q, 0)$ 重采样。该方法实现简单且保证无损，但接受决策仅依赖局部信息，导致可接受令牌数量受限。**块验证**（Blockwise Verification，Sun et al., 2024）尝试对连续令牌块进行联合验证以提升接受率，然而其面临一个根本性瓶颈——**联合不可解性**（joint intractability）：当草案块内存在多个拒绝位置时，需要计算高维联合分布上的重采样概率，这在计算上不可行。因此，现有块验证方法只能利用部分联合信息，实际增益有限。

上述瓶颈的深层原因在于，推测解码中草案分布 $q$ 与目标分布 $p$ 之间的概率质量不匹配呈现**分支不对称性**：在某些令牌序列分支上，草案分配的概率质量可能超过目标（“过度分配”），而在其他分支上则不足（“分配不足”）。逐令牌验证忽略了这种跨分支的可转移性——过度分配分支的多余质量本可以用于弥补分配不足分支的缺陷，从而接受更多令牌。块验证虽然试图捕捉这种联合结构，却因计算不可解而无法完整利用。

本文提出**层次推测解码**（Hierarchical Speculative Decoding，HSD），旨在从根本上克服联合不可解性。核心洞察是：通过从序列末端向前扫描，递归地聚合各分支的多余概率质量，可以在不显式计算高维联合分布的前提下，精确恢复整个序列的目标分布。HSD 在最后一个接受令牌之后仅需**一次重采样**即可完成无损恢复，无需额外调用目标模型。该方法从理论上保证了无损性，同时显著提升了期望接受令牌数量，为推测解码的验证范式提供了新的设计空间。

## 核心创新

HSD 的核心创新在于提出了一种**层次分支重采样（Hierarchical Branch Resampling）**的验证范式，从根本上克服了推测解码中验证阶段的**联合不可解性（Joint Intractability）**问题。与现有的逐令牌验证（Token-wise Verification; Leviathan et al., 2023）和块验证（Blockwise Verification; Sun et al., 2024）相比，HSD 在三个关键维度上实现了范式转变：

| 维度 | 逐令牌验证（基准） | 块验证（现有无损方法） | HSD（本文方法） |
|------|-------------------|---------------------|----------------|
| **验证范式** | 逐令牌独立接受/拒绝，在第一个拒绝位置进行单步重采样 | 对连续令牌块联合验证，利用部分信息 | **层次分支重采样**：从末端向前扫描，根据上限分支分歧度确定最长接受前缀，在最后一个接受位置之后进行一次上限分支重采样 |
| **接受概率** | $\min\{1, p(x_t)/q(x_t)\}$（逐令牌比率） | 基于块的联合接受概率 | 基于**上限分支分歧度** $D_{\mathrm{Branch}}^{*}$ 的层次接受概率 $h_t = \frac{D_{\mathrm{Branch}}^{*}(p, q \mid X_{1:t})}{D_{\mathrm{Branch}}^{*}(q, p \mid X_{1:t})}$，充分利用分支间信息 |
| **重采样分布** | $p_{\mathrm{res}}(x_t) \propto \max(p(x_t)-q(x_t), 0)$，在拒绝位置重采样原始词汇空间 | 块级重采样 | **上限分支重采样概率** $P_{\mathrm{res}}^{*}(x_t \mid X_{1:t-1})$，在接受的最后一个令牌之后**单一位置**重采样，且仅需对可访问分支计算 |

### 核心洞察：分支分歧度的不对称性

HSD 的理论基础建立在一个关键观察之上：**分支分歧度具有不对称性**。草案模型在某些分支上可能“过度分配”概率质量（即 $q > p$），而在另一些分支上“分配不足”（即 $p > q$）。HSD 的核心洞察在于：

> 来自“过度分配”分支的多余概率可以被递归地聚合，用于弥补“分配不足”分支的缺陷。因此，即使单个分支无法自恢复，整个序列的目标分布也能被精确恢复。

这一机制通过两个关键组件实现：

1. **上限前缀比（Capped Prefix Ratio）** $r^{*}(\mathbf{X}_{1:t})$：在不超过 1 的最大前缀比处进行上限截断，用于稳定层次接受和重采样过程，防止因局部概率比过大而导致的分布失真。

2. **上限分支重采样（Capped Branch Resampling）**：在接受的最后一个令牌之后仅需**一次重采样**即可无损恢复完整的目标分布，无需额外目标模型调用。验证阶段额外耗时不足总解码时间的 1%，且 HSD 验证比块验证更快约 20%（Table A.4）。

### 算法流程

HSD 的验证过程包含四个关键模块：

- **向后扫描与层次接受**：从草案序列末尾向前扫描，利用上限分支分歧度计算层次接受概率，确定最长接受前缀 $\tau$。
- **上限分支重采样**：在位置 $\tau+1$ 处，使用上限分支重采样概率进行一次重采样，以无损恢复目标分布。
- **目标模型前向**：对于剩余位置，直接从目标模型采样继续生成，可与下一次推测解码无缝衔接。

这一流程在理论上被证明是**无损的**（Theorem 4, Theorem 6），即 HSD 生成的序列分布与目标模型完全一致，同时在期望接受的令牌数量上优于逐令牌验证和块验证。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/001_Figure_1.jpg]]
*Figure 1: Overview of HSD. HSD accepts the draft Xτ by scanning backward from γ to τ , and then performs a single resampling at position τ + 1 using the corresponding distribution from the resampling hierarchy*

HSD 的整体流程围绕“草案生成—层次验证—单步重采样”三个核心阶段构建，在保证无损的前提下最大化可接受令牌数量。

### 输入与输出

- **输入**：前缀序列 $X_{1:t-1}$（已生成的目标分布令牌）。
- **草案模型**（如 Qwen2.5-0.5B）：自回归生成长度为 $\gamma$ 的候选序列 $X_{1:\gamma}$。
- **目标模型**（如 Qwen2.5-72B）：对草案序列进行一次前向传播，获取所有候选令牌的完整概率分布 $p$。
- **输出**：接受前缀 $X_{1:\tau}$ 及在位置 $\tau+1$ 处重采样的一个令牌，后续位置由目标模型直接采样继续生成。

### 三阶段 Pipeline

1. **草案生成（Drafting Phase）**
   小型草案模型 $q$ 以自回归方式生成 $\gamma$ 个候选令牌，构成完整草案块 $X_{1:\gamma}$。此阶段与传统推测解码一致，草案质量直接影响后续接受效率。

2. **向后扫描与层次接受（Backward Scan with Hierarchical Acceptance）**
   从序列末端 $\gamma$ 向前扫描至位置 $1$，逐位置计算层次接受概率 $h_t$：
   - 在末端位置 $\gamma$：$h_{\gamma} = \min\{r^*(X_{1:\gamma}), 1\}$，基于上限前缀比 $r^*$ 判断；
   - 在中间位置 $t < \gamma$：$h_t = \frac{D_{\mathrm{Branch}}^*(p, q \mid X_{1:t})}{D_{\mathrm{Branch}}^*(q, p \mid X_{1:t})}$，利用上限分支分歧度之比。
   
   通过向后扫描确定最长接受前缀 $X_{1:\tau}$，其中 $\tau$ 是满足层次接受条件的最远位置。这一机制充分利用了分支间概率质量的不对称性——来自“过度分配”分支的多余概率被递归聚合，用于弥补“分配不足”分支的缺陷。

3. **上限分支重采样（Capped Branch Resampling）**
   在接受的最后一个令牌位置 $\tau+1$ 处，仅执行**一次**重采样，使用上限分支重采样概率：
   $$P_{\mathrm{res}}^*(x_t \mid X_{1:t-1}) = \frac{\max\{q(X_{1:t})(\bar{r}^*(X_{1:t}) - 1), 0\}}{D_{\mathrm{Branch}}^*(p, q \mid X_{1:t-1})}$$
   该步从可访问分支内采样一个令牌，无需额外目标模型调用。理论保证（Theorem 4, Theorem 6）证明，此单步重采样即可精确恢复完整的目标分布。

4. **目标模型续生成**
   对于 $\tau+1$ 之后的剩余位置，直接从目标模型采样继续生成，可与下一轮推测解码无缝衔接。

### 关键机制：上限前缀比

上限前缀比 $r^*$ 是 HSD 区别于朴素层次重采样的核心设计。它通过在不超过 $1$ 的最大前缀比位置进行截断，稳定了层次接受和重采样过程：
$$r^*(\mathbf{X}_{1:t}) = \min\{r(\mathbf{X}_{1:m(\mathbf{X}_{1:t})}), 1\} \cdot r(\mathbf{X}_{m(\mathbf{X}_{1:t})+1:t})$$
其中 $m(\mathbf{X}_{1:t})$ 是前缀中联合概率比 $r$ 最大的位置索引。消融实验表明，去除上限机制会导致任务精度下降（GSM8K: 84.40% vs 上限版本 84.96%；HumanEval: 80.61% vs 82.47%），验证了上限前缀比对保持分布保真度的关键作用。

### 计算开销

HSD 的验证阶段额外耗时不足总解码时间的 $1\%$（Table A.4），且 HSD 验证比块验证（Blockwise）快约 $20\%$。上限分支重采样只需一次重采样操作，避免了逐令牌验证中多次重采样的累积开销。

## 核心模块与公式推导

### 方法总览

HSD 的验证流程由三个关键模块构成：**向后扫描与层次接受**、**上限前缀比**、以及**上限分支重采样**。其核心思想是将多个重采样分布按层次组织，每一层仅恢复其分支内的部分目标分布，最终通过一次重采样即在可访问分支内无损恢复完整的目标分布。

### 模块一：分支分歧度与层次接受

HSD 的接受决策基于**分支分歧度**（Branch Divergence），该量度刻画了草案分布 $q$ 在给定分支内相对于目标分布 $p$ 的概率质量缺失程度。

**分支定义**：给定前缀 $X_{1:t-1}$，其分支是下一位置所有可能令牌的集合：

$$\mathrm{Branch}(X_{1:t-1}) = \{X_{1:t} = (X_{1:t-1}, \tilde{x}_t) \mid \tilde{x}_t \in \mathcal{V}\}$$

**分支分歧度**（Definition 2）：

$$D_{\mathrm{Branch}}(p, q \mid X_{1:t-1}) = \sum_{X_{1:t} \in \mathrm{Branch}(X_{1:t-1})} \max\{p(X_{1:t}) - q(X_{1:t}), 0\}$$

该值衡量的是分支内目标分布超出草案分布的概率质量总和，即草案的"缺失质量"。与之对称的 $D_{\mathrm{Branch}}(q, p \mid X_{1:t-1})$ 则衡量草案的"多余质量"。

**分支分歧度的不对称性**是 HSD 的理论基石：

$$\Delta_{\mathrm{Branch}}(X_{1:t-1}) = D_{\mathrm{Branch}}(p, q \mid X_{1:t-1}) - D_{\mathrm{Branch}}(q, p \mid X_{1:t-1})$$

当 $\Delta > 0$ 时，分支内存在概率质量净缺失，单靠该分支内部的重采样无法完全恢复目标分布；当 $\Delta \leq 0$ 时，草案拥有足够的冗余质量，可通过重采样实现完全恢复（Corollary 3）。

**层次接受概率**：HSD 从草稿序列末端向前扫描，对每个位置 $t$ 计算接受概率 $h_t$。在序列末端（$t = \gamma$），接受概率基于联合概率比 $r(X_{1:\gamma}) = p(X_{1:\gamma}) / q(X_{1:\gamma})$；在中间位置，接受概率基于分支分歧度之比：

$$h_\gamma = \min\{r(X_{1:\gamma}), 1\}, \quad h_t = \frac{D_{\mathrm{Branch}}(p, q \mid X_{1:t})}{D_{\mathrm{Branch}}(q, p \mid X_{1:t})}$$

这种层次化的接受机制使得 HSD 能够利用后续分支的冗余质量来补偿前序分支的缺失，从而接受比逐令牌验证更长的前缀。

### 模块二：上限前缀比

朴素层次接受存在一个关键问题：当某个前缀的联合概率比 $r(X_{1:i}) > 1$ 时，该前缀所在分支的 $D_{\mathrm{Branch}}(p, q \mid X_{1:i})$ 可能异常偏大，导致接受概率计算不稳定。HSD 引入**上限前缀比**（Capped Prefix Ratio）来解决这一问题。

**最大前缀比索引**：

$$m(\mathbf{X}_{1:t}) = \arg\max_{1 \leq i < t} r(\mathbf{X}_{1:i}) \quad \text{或 } 0 \text{ 若无前缀比超过 } 1$$

**上限前缀比**（Definition 5）：

$$r^{*}(\mathbf{X}_{1:t}) = \min\{r(\mathbf{X}_{1:m(\mathbf{X}_{1:t})}), 1\} \cdot r(\mathbf{X}_{m(\mathbf{X}_{1:t})+1:t})$$

该操作在联合概率比首次超过 1 的位置进行截断，将超出部分限制为 1，从而保证后续计算中概率质量不会因单一异常前缀而过度膨胀。基于 $r^{*}$ 可定义**上限分支分歧度** $D_{\mathrm{Branch}}^{*}$，其计算方式与原始分支分歧度相同，但将 $p(X_{1:t})/q(X_{1:t})$ 替换为 $r^{*}(X_{1:t})$。

### 模块三：上限分支重采样

HSD 在确定最长接受前缀 $\tau$ 后，仅在位置 $\tau+1$ 执行**一次重采样**，其重采样分布为：

$$P_{\mathrm{res}}^{*}(x_t \mid X_{1:t-1}) = \frac{\max\{q(X_{1:t})(\bar{r}^{*}(X_{1:t}) - 1), 0\}}{D_{\mathrm{Branch}}^{*}(p, q \mid X_{1:t-1})}$$

其中 $\bar{r}^{*}$ 是经上限截断后的归一化比率。该分布仅涉及可访问分支内的令牌，无需对整个词汇空间进行计算。

**理论保证**：Theorem 4 和 Theorem 6 证明，HSD 通过层次分支重采样和上限前缀比机制，能够在仅一次重采样的情况下精确恢复完整的目标分布，即 $P_{\mathrm{HSD}}(X_{1:\tau+1}) = p(X_{1:\tau+1})$，从而保证方法的无损性。

### 期望接受令牌数

HSD 的期望接受令牌数为：

$$\mathbb{E}[\tau]_{\mathrm{branch}} = \sum_{i=1}^{\gamma} \left[1 - \prod_{k=i}^{\gamma} (1 - h_k)\right]$$

该表达式表明，HSD 通过层次化接受概率 $h_k$ 的乘积结构，能够接受比逐令牌验证和块验证更多的令牌。实验验证了这一理论优势：在 GSM8K 上，HSD 的块效率达到 $6.64 \pm 0.04$ tokens/step，优于 Tokenwise 的 $6.40 \pm 0.10$ 和 Blockwise 的 $6.51 \pm 0.09$（Table A.1）。

## 实验与分析

### 主实验设置

实验在单张NVIDIA H20 GPU（96 GB）上运行，采用GPTQ 8-bit量化的Qwen2.5模型族。默认配置下，草案模型为Qwen2.5-0.5B，目标模型为Qwen2.5-72B，采样温度设为1。所有实验使用5个不同随机种子重复，报告平均值与标准差。比较基线包括两个无损验证方法：逐令牌验证（Tokenwise，Leviathan et al., 2023）和块验证（Blockwise，Sun et al., 2024），均采用相同的草案-目标模型对与硬件条件。

### 块效率与解码速度

HSD在多个基准上一致提升块效率（BE）和解码速度（DS）。在GSM8K上，HSD的块效率达到6.64±0.04 tokens/step，相比逐令牌验证的6.40±0.10提升3.75%，相比块验证的6.51±0.09提升2.0%（Table A.1）。在HumanEval上，HSD在14B模型上块效率提升9.5%，在32B模型上提升12.3%（Table 1）。在CNN/DailyMail摘要任务上，HSD同样展现出稳定的解码加速。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/002_Table_1.jpg]]
*Table 1: Comparison of Block Efficiency (BE) and Decoding Speed (DS) across datasets and model scales. Values in parentheses show percentage improvement over Tokenwise*

多草稿设置下（K=3或4），HSD结合递归拒绝采样（RRS）相比逐令牌验证平均块效率提升5.9%（Table 2），验证了HSD与多草稿策略的兼容性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/003_Table_2.jpg]]
*Table 2: Comparison of our HSD and tokenwise verification in Multi-draft setting. Table 3: Ablations on temperature, draft length, and target model size on GSM8K. Except for the ablation on target model size, we adopt Qwen2.5-0.5B and Qwen2.5-72B as the draft and target pair*

### 跨模型规模的一致性

HSD在不同目标模型规模（14B、32B、72B）下均一致提升块效率和解码速度。在14B和32B模型上提升更为显著（GSM8K上分别提升5.2%和5.4%），而在72B模型上提升幅度收窄至3.3%（Table 1）。这一趋势与草案-目标模型分布相似性随规模差距变化的规律一致：草案质量相对越低，分支分歧度普遍偏大，HSD可转移的多余概率质量减少，增益相应下降。

### 消融实验

**温度消融**：在温度t∈{0.6, 0.8, 1.0}下，HSD的块效率分别为6.86、6.79、6.65，在所有温度设置下均优于逐令牌验证和块验证（Table 3(a)）。温度降低时，目标分布更集中，草案与目标的分歧度减小，HSD的接受率提升更为明显。

**草稿长度消融**：随着草稿长度γ从5增至15，HSD相对于块验证和逐令牌验证的优势持续扩大，在γ=15时达到峰值7.88 tokens/step，解码速度达52.95 steps/second（Table 3(b)）。更长的草稿为层次分支重采样提供了更多可利用的分支间概率质量转移机会。

**上限机制消融**：去除上限前缀比机制（HSD without capping）会导致任务精度下降：GSM8K准确率从84.96%降至84.40%，HumanEval从82.47%降至80.61%（Table A.3）。这表明上限前缀比对维持分布保真度至关重要——无上限时，个别分支的极端比率会扭曲重采样分布，破坏无损性。

### 扩展实验：LLaMA模型族与EAGLE-3集成

在LLaMA-3.1模型对上（70B目标，8B草案，非量化版本，8张H20 GPU分布式），HSD同样表现出块效率和解码速度的稳定提升（Table 4(a)），验证了方法跨模型族的泛化性。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/004_Table_4.jpg]]
*Table 4: Extended experimental results using the LLaMA model family and EAGLE-3 framework on GSM8K. Note that we replace EAGLE-3’s tokenwise verification with our HSD, yielding EAGLE-3H*

将HSD集成到EAGLE-3框架中（替换其逐令牌验证，得到EAGLE-3H），在GSM8K上获得超过12%的性能增益（Table 4(b)）。这表明HSD的层次验证机制可与树状注意力等高级草稿策略无缝结合，在不增加验证计算复杂性的前提下进一步提升效率。

### 验证阶段开销

HSD的验证阶段额外耗时不足总解码时间的1%（Table A.4, Appendix H）。与块验证相比，HSD验证速度更快约20%。这是因为上限分支重采样只需在最后一个接受位置之后进行一次重采样，且仅需对可访问分支计算，避免了逐位置重采样的累积开销。上限前缀比和分支分歧度的计算虽需额外张量操作，但经过并行化优化后，在典型batch size=1场景下几乎不构成瓶颈。

### 失败模式与边界条件

HSD的增益依赖于草案模型与目标模型之间的分布相似性。当草案质量过低时，分支分歧度普遍偏大，可转移的多余概率质量不足，接受令牌的增量收益会显著下降。这一现象在72B目标模型上已有体现（增益从14B/32B的5%+降至3.3%），在草案-目标分布差异更大的场景下可能进一步弱化。此外，上限前缀比的截断方式采用固定规则（在不超过1的最大前缀比处截断），是否存在自适应上限变体以在保持无损的同时进一步提高接受率，仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/005_Table.jpg]]
*Table: (a) Evaluation using the LLaMA-3 model family. (b) Integration with EAGLE-3*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/007_Table.jpg]]
*Table: A.1: Comparison of different algorithm performance on GSM8K with Qwen-2.5. We list the average and standard deviation across 5 runs with different seeds. Table A.2: Comparison of task performance across model sizes and methods. Table A.3: Ablation on capping mechanism*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_LaVrNaBNwM/figures/008_Table.jpg]]
*Table: A.4: Runtime breakdown of Blockwise and HSD*

## 方法谱系与知识库定位

### 推测解码验证范式的演进

推测解码（Speculative Decoding）的核心效率瓶颈并非草案生成，而是**验证阶段如何在不损失目标分布的前提下最大化可接受令牌数量**。现有方法在此问题上形成了两条主要路线：

- **逐令牌验证（Token-wise Verification）**（Leviathan et al., 2023）：对草案序列中的每个令牌独立计算接受概率 $h(x_t) = \min\{1, p(x_t)/q(x_t)\}$，在首次拒绝位置进行重采样。该方法保证了无损性，但其“首次拒绝即截断”的机制导致后续即使与目标分布完全一致的令牌也被丢弃，可接受令牌数量的期望值受限于逐令牌比率的连乘效应。

- **块级验证（Blockwise Verification）**（Sun et al., 2024）：对连续令牌块进行联合验证，试图利用块内部分信息提升接受率。该方法同样保证无损，但由于仅利用块级别的聚合信息，对分支间概率质量不平衡的利用仍不充分，提升幅度有限。

HSD 的定位在于**突破上述两类方法的根本性限制——联合不可解性（Joint Intractability）**。逐令牌验证和块验证之所以无法充分利用草案信息，根本原因在于它们未能系统性地处理分支间概率质量的不对称性：某些分支上草案模型“过度分配”了概率质量（$q > p$），而另一些分支上则“分配不足”（$q < p$）。HSD 通过层次分支重采样机制，首次实现了在保证无损的前提下，将过度分配分支的多余质量递归聚合以弥补不足分支的缺陷。

### 核心机制差异

HSD 与两类基线方法的关键差异体现在验证范式、接受概率计算和重采样策略三个维度：

| 维度 | 逐令牌验证 | 块级验证 | HSD |
|------|-----------|---------|-----|
| 验证范式 | 逐令牌独立接受/拒绝，首次拒绝处截断 | 对连续块联合验证 | 从末端向后扫描，层次化确定最长接受前缀 |
| 接受概率 | $\min\{1, p(x_t)/q(x_t)\}$ | 块级联合比率 | 上限分支分歧度之比 $h_t = D^*_{\text{Branch}}(p,q \mid X_{1:t}) / D^*_{\text{Branch}}(q,p \mid X_{1:t})$ |
| 重采样位置 | 首次拒绝位置 | 块级拒绝后 | 最后一个接受令牌之后，仅一次重采样 |
| 重采样分布 | $\propto \max(p-q, 0)$ 在原始词汇空间 | 块级调整 | $P^*_{\text{res}}$ 在可访问分支内，利用上限前缀比截断 |

HSD 的关键创新在于**上限前缀比（Capped Prefix Ratio）机制**：$r^*(\mathbf{X}_{1:t}) = \min\{r(\mathbf{X}_{1:m(\mathbf{X}_{1:t})}), 1\} \cdot r(\mathbf{X}_{m(\mathbf{X}_{1:t})+1:t})$，其中 $m(\mathbf{X}_{1:t})$ 是前缀中联合比率最大且不超过1的位置。这一截断操作保证了分支分歧度的计算稳定性，使得即使单个分支无法自恢复（即 $D_{\text{Branch}}(p,q) > D_{\text{Branch}}(q,p)$），来自其他分支的过剩质量也能通过层次聚合来弥补，从而在最后一个接受令牌之后仅需一次重采样即可恢复完整的目标分布。

### 适用边界与局限

HSD 的增益高度依赖于草案模型与目标模型之间的**分布相似性**。当草案质量过低时，分支分歧度普遍偏大，层次聚合的补偿空间缩小，接受令牌的增量收益会下降。这一特性与所有推测解码方法一致，但 HSD 通过上限前缀比机制在一定程度上缓解了低质量草案的负面影响——截断操作防止了极端比率值对重采样分布的扭曲。

在工程实现层面，当前 HSD 需要从目标模型获取所有候选令牌的完整概率分布（即一次目标模型前向传播后得到整个词汇空间的分布），这在批量处理或极端大词汇表场景下可能增加少量中间存储开销。不过，在典型批量大小为1的推测解码场景中，该开销已被验证为低于总解码时间的1%，且 HSD 的验证阶段比块验证快约20%。

上限前缀比和分支分歧度的计算引入了额外的张量操作。尽管经过并行化优化，在缺乏高效张量并行支持的特殊硬件（如边缘设备）上可能引入微小延迟。这一局限在当前主流 GPU 部署中不构成实质性瓶颈，但限制了 HSD 向资源极度受限场景的直接迁移。

### 开放问题

1. **极长序列下的可扩展性**：实验验证集中在草稿长度 $\gamma \in \{5, 10, 15\}$ 的设置，HSD 在数千令牌级别的极长序列下的接受概率衰减特性和并行化策略是否需要进一步优化，尚待验证。

2. **上限前缀比的变体设计**：当前采用固定截断策略（在最大前缀比处上限为1），是否存在自适应上限变体——例如根据分支分歧度的全局分布动态调整截断阈值——以在保持无损的同时进一步提高接受率，是一个开放的理论问题。

3. **与复杂草稿策略的耦合**：HSD 的验证机制是否可与动态草稿长度、树状注意力（Tree Attention）等更复杂的草稿生成策略无缝结合，而不会显著增加验证计算的复杂性，值得进一步探索。初步实验表明 HSD 与 EAGLE-3 的集成是可行的（替换其逐令牌验证后获得超过12%的性能增益），但更广泛的兼容性尚未被系统验证。

4. **多草稿场景下的最优分支数**：在多草稿设置中，HSD 结合递归拒绝采样（RRS）已展现出约5.9%的平均块效率提升，但最优草稿分支数 $K$ 与目标/草案模型分布差异之间的定量关系尚未被刻画。

## 原文 PDF

![[paperPDFs/ICLR_2026/Overcoming_Joint_Intractability_with_Lossless_Hierarchical_Speculative_Decoding.pdf]]
