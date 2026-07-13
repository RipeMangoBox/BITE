---
title: "Beyond Scattered Acceptance: Fast and Coherent Inference for DLMs via Longest Stable Prefixes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Scattered_Acceptance_Fast_and_Coherent_Inference_for_DLMs_via_Longest_Stable_Prefixes.pdf
project_link: null
code_link: null
aliases:
- LSPLS
- BSAFCIDLSP
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "在扩散语言模型推理中识别并原子提交最长连续稳定前缀，用前缀优先拓扑替代分散 token 接受。"
primary_logic: |
  每步前向传播计算活动后缀 token 的 logit margin，通过自适应阈值找出连续稳定前缀，再用结构边界对齐确定提交长度并整体吸收到冻结前缀，使活动后缀单调缩短、KV 缓存连续追加并降低 token 翻转率。
claims:
- "DLM 中间去噪步骤常已包含最终正确答案片段，前缀级稳定提交可减少碎片化修复成本。"
- "LSP 在多个 DLM 基准上保持或略升质量，同时通过前缀吸收实现显著推理加速。"
---

# Beyond Scattered Acceptance: Fast and Coherent Inference for DLMs via Longest Stable Prefixes

> [!tip] 核心洞察
> 核心洞见在于：DLM在中间步骤的预测中，正确的最终答案往往已经出现（早期答案收敛）。通过利用这一特性，LSP调度器在单次前向传播中识别并原子化地提交最长的连续稳定前缀，并利用自适应阈值和结构边界对齐（structural snapping）来确保提交块的自然性和连贯性。这种前缀优先的拓扑结构使得KV缓存可以连续追加，活动后缀长度呈几何级数衰减，从而大幅减少token翻转率和去噪器调用次数。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越分散接受：通过最长稳定前缀实现扩散语言模型的快速与连贯推理 |
| 英文题名 | Beyond Scattered Acceptance: Fast and Coherent Inference for DLMs via Longest Stable Prefixes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zvw9Hiwa0i) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Longest Stable Prefix (LSP) Scheduler |
| Dataset | GSM8K, HumanEval |

> [!tip] 效果简介
> - GSM8K 上，Score (%) 为 77.6，对比 77.1，变化 +0.5。
> - GSM8K 上，Speedup 为 1.51×，对比 1.0×，变化 +0.51×。
> - HumanEval 上，pass@1 (%) 为 29.3，对比 30.5，变化 -1.2。

## 概要

本文提出了一种名为**最长稳定前缀（Longest Stable Prefix, LSP）调度器**的训练无关、模型无关的推理加速方法，用于扩散语言模型（Diffusion Language Models, DLMs）。LSP的核心思想是摒弃现有DLM中广泛采用的“分散接受”（Scattered Acceptance）策略——即独立地基于局部置信度提交分散的token——转而采用**整体前缀吸收**（Monolithic Prefix Absorption）范式：在单次前向传播中，识别并原子化地提交当前活动序列中最长的连续稳定前缀。

实验表明，LSP在LLaDA-8B和Dream-7B上实现了高达**3.4倍**的推理加速，同时匹配或略微提升了输出质量。在GSM8K上，LSP以77.6%的准确率实现了1.51倍加速；在TruthfulQA上，准确率从34.4%提升至45.8%，同时获得2.29倍加速。消融研究验证了自适应分块、结构边界对齐和前缀优先拓扑等核心组件的关键作用。

### 1 扩散语言模型（DLM）的推理瓶颈

扩散语言模型通过迭代去噪过程生成文本：从完全掩码的序列开始，逐步预测并替换掩码token。现有DLM（如LLaDA (Nie et al., 2025) 和 Dream (Ye et al., 2025)）通常采用**分散接受**策略——在每个去噪步骤中，模型独立地基于局部置信度（如logit margin）提交高置信度的token，而将低置信度的token保留为活动状态。

然而，这种策略存在两个根本性问题：

1. **算法层面**：它创建了一个由冻结token和可变token组成的碎片化序列。这些区域之间的众多边界不稳定，需要重复的局部修复，从而减缓了向全局连贯输出的收敛速度。
2. **系统层面**：这种碎片化破坏了键值缓存（KV Cache）的连续性，将其分割成小的、非连续的分段，破坏了高效Transformer推理所必需的内存局部性。

### 2 核心洞见：早期答案收敛

本文的核心洞见在于：DLM在中间步骤的预测中，正确的最终答案往往已经出现（早期答案收敛）。通过利用这一特性，LSP调度器可以在不牺牲质量的情况下进行训练无关的早期提交，从而减少计算量。

## 核心方法与创新机理

LSP的核心创新在于将**提交拓扑结构**（Commitment Topology）作为关键因果旋钮，从根本上改变了计算动态：

| 变更槽位 | 基线值 | LSP提出值 |
|---------|--------|----------|
| **提交拓扑结构** | 分散接受：独立提交高置信度token，导致碎片化 | 整体前缀吸收：原子化提交最长的连续稳定前缀 |
| **分块大小策略** | 固定大小或基于局部置信度的独立决策 | 自适应阈值：动态选择阈值，使块长度落在目标分数范围内 |
| **提交边界对齐** | 无对齐，提交块可能中断在单词或句子中间 | 结构边界对齐：将候选块的右边界对齐到最近的结构分隔符 |
| **KV缓存策略** | 碎片化KV缓存，需要昂贵的收集操作或重计算 | 近似KV缓存：将已提交的前缀视为固定上下文，进行连续的KV追加 |

LSP调度器的迭代过程如Figure 1所示。在每个步骤中，LSP执行一次前向传播来评估当前活动后缀的预测稳定性，然后原子化地提交最长的连续稳定前缀，使冻结前缀（绿色）整体增长，活动后缀（白色）收缩。

![Figure 1]()

LSP的整体流程如下：

1. **稳定性诊断**：通过单次前向传播计算活动后缀中每个位置的logit margin。
2. **自适应分块**：动态选择一个阈值，确定满足条件的连续稳定前缀长度。
3. **结构边界对齐**：将候选块的右边界对齐到最近的结构分隔符。
4. **原子化提交**：将确定的最长稳定前缀作为一个原子操作提交到冻结前缀，并更新KV缓存。

### 1 稳定性诊断：Logit Margin

LSP使用**logit margin**作为模型在每个位置预测稳定性的代理指标：

$$\delta_i \triangleq z_{(1)}(i) - z_{(2)}(i)$$

其中 $z_{(1)}(i)$ 和 $z_{(2)}(i)$ 分别是位置 $i$ 上最高和次高的logit值。较大的margin表示模型在该位置的预测更加确定。

### 2 自适应分块

LSP高效地搜索一个阈值 $\tau_k$，使得满足条件的连续稳定前缀长度 $L'(\tau_k)$ 落在当前活动序列长度 $N_k$ 的目标分数范围内：

$$L'(\tau_k) \in [\alpha N_k, \beta N_k]$$

这种自适应阈值策略鼓励活动序列长度呈几何级数衰减，从而产生接近二次的总工作复杂度，随序列长度优雅地扩展。

### 3 结构边界对齐

为了增强全局连贯性，LSP将候选块的右边界对齐到最近的结构分隔符（如标点、换行符）。最终的提交块长度由以下公式确定：

$$\mathcal{L} \triangleq \max \{ L_{\mathrm{min}}, \max \{ j \leq L' : \hat{y}_j \in \mathcal{D} \wedge L' - j \leq W \} \}$$

其中 $L_{\mathrm{min}}$ 是最小保证长度，$\mathcal{D}$ 是结构分隔符集合，$W$ 是回看窗口大小。该公式确保提交块在保持自然边界的同时，至少提交一个token以保证单调进展。

## 实验与关键发现

### 1 主要结果

Table 1展示了LSP在LLaDA-8B和Dream-7B上的主要基准测试结果：

![Table 1]()

| 基准测试 | 指标 | LSP | Full基线 | 加速比 |
|---------|------|-----|---------|-------|
| GSM8K | 得分 (%) | **77.6** | 77.1 | **1.51×** |
| HumanEval | pass@1 (%) | 29.3 | 30.5 | **1.22×** |
| MBPP | pass@1 (%) | **37.6** | 37.6 | **1.33×** |
| TruthfulQA | 得分 (%) | **45.8** | 34.4 | **2.29×** |
| Countdown | 得分 (%) | **15.3** | 15.3 | **2.63×** |
| Sudoku (Dream-7B) | 得分 (%) | 88.0 | 89.0 | **3.36×** |

LSP在几乎所有基准测试上都实现了显著的加速，同时在多数任务上匹配或提升了输出质量。特别值得注意的是，在TruthfulQA上，LSP不仅实现了2.29倍加速，还将准确率从34.4%提升至45.8%。

### 2 消融研究

### 分块策略消融

Table 2比较了固定大小前缀提交策略与自适应LSP：

![Table 2]()

| 策略 | GSM8K得分 (%) | 平均步数 |
|------|--------------|---------|
| 固定1-token前缀 | 67.1 | 128 |
| 固定2-token前缀 | 66.8 | 64 |
| 固定4-token前缀 | 47.6 | 32 |
| 固定8-token前缀 | 19.3 | 16 |
| **自适应LSP** | **69.9** | **~68** |

固定大小策略是脆弱的，强制在推理步数（速度）和最终准确率之间进行权衡。LSP的自适应分块动态地找到了最有效的平衡点。

### 核心组件消融

Table 3展示了结构边界对齐和提交拓扑的消融研究：

![Table 3]()

| 配置 | GSM8K得分 (%) | 平均步数 |
|------|--------------|---------|
| 无结构边界对齐 | 67.8 | ~50 |
| Scattered-Margin基线 | 68.9 | 128 |
| **完整LSP** | **69.9** | **~68** |

结果表明，结构边界对齐和前缀优先拓扑都是实现高性能的关键组件。

### 3 Token翻转率分析

Figure 2通过token翻转率量化修复成本：

![Figure 2]()

LSP将活动后缀中的token翻转率从分散基线的**14.2%**降低到**4.3%**（在生成中期阶段，即25%-75%完成度）。这表明LSP通过锁定早期连贯前缀，显著稳定了未来的生成上下文，减少了token振荡和修复成本。

### 4 可视化分析

Table 4展示了LSP在数学推理中的整体前缀吸收过程：

![Table 4]()

每个彩色块代表在单步中原子化提交的最长稳定前缀。提交边界与自然语言或数学单元（如从句、计算步骤）对齐，展示了LSP的结构边界对齐在实践中的效果。

## 定位与知识库关联

### 1 与现有方法的关系

LSP属于DLM推理加速方法谱系，但与现有方法有本质区别：

- **与固定大小分块策略的区别**：固定大小策略（如1-token、8-token前缀）是脆弱的，在速度和准确率之间强制权衡。LSP的自适应分块动态调整提交长度，在置信区域激进提交，在不确定区域谨慎精炼。

- **与分散接受策略的区别**：分散接受（如LLaDA使用的策略）创建碎片化的KV缓存和不稳定的边界。LSP的前缀优先拓扑维护单一、干净的边界，使模型能够专注于连贯地扩展稳定前缀。

- **与推测解码的区别**：LSP是训练无关且模型无关的，而推测解码通常需要额外的草稿模型或训练。LSP被设计为与扩散过程本身正交的改进，可以与推测解码等其他加速技术协同。

### 2 局限性

1. **非顺序任务**：LSP的连续前缀假设本质上不适用于非顺序任务，如文本填充（text in-filling）或不受限制的编辑。
2. **启发式边界检测**：当前的结构边界对齐实现依赖于启发式分隔符集，虽然对英语和CJK领域鲁棒，但未来可以集成轻量级的学习边界检测头。
3. **任务适用性**：LSP的有效性在具有清晰分隔符的任务（代码、推理步骤）上得到验证，其在更开放式的创意生成任务上的影响有待进一步研究。

### 3 开放问题

1. 如何将LSP的拓扑原理扩展到支持“稳定岛”（stable islands）以实现双向填充？
2. LSP能否与推测解码或近似缓存方法等其他加速技术协同，以实现复合增益？
3. 更复杂的、时间感知的稳定性指标能否在提交激进性和准确性之间提供更好的权衡？
4. LSP在更长序列生成任务上的具体计算成本（FLOPs）和延迟表现如何？

### 整体框架

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/001_Figure_1.jpg]]
*Figure 1: Figure 1: The iterative process of the Longest Stable Prefix (LSP) scheduler. In each step, LSP performs a single forward pass to assess the stability of predictions for the current active suffix, measured by the logit margin ( $\delta _ { i }$ ) . Instead of accepting scattered tokens, it atomically commits the longest contiguous prefix of tokens that meet an adaptively determined stability threshold (τ ). As shown, the frozen prefix (green) grows monolithically, causing the active suffix (white) to shrink.*

### 实验与分析

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/002_Table_1.jpg]]
*Table 1: Table 1: Main benchmark results on LLaDA-8B and Dream-7B. We report the task-specific score (%) and the inference speedup over the ‘Full‘ baseline. LSP delivers substantial speedups while maintaining or even improving task performance.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/003_Table_2.jpg]]
*Table 2: Table 2: Ablation on Sizing Strategy (GSM8K, LLaDA-8B). Fixed-size commitment strategies are brittle, forcing a trade-off between the number of inference steps (speed) and final accuracy. LSP’s adaptive sizing dynamically finds the most effective balance.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/004_Table_3.jpg]]
*Table 3: Table 3: Ablation studies on core LSP components (GSM8K, LLaDA-8B). Both structural snapping and the prefix-first topology are crucial for achieving high performance. Each component is compared against the full LSP method.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/006_Table_4.jpg]]
*Table 4: Table 4: Visualization of LSP’s monolithic prefix absorption for math reasoning (Granular View). Each colored block represents the Longest Stable Prefix atomically committed in a single step. This more detailed breakdown shows how LSP iteratively extends the solution by committing shorter, coherent chunks. The strict left-to-right, contiguous growth (light to dark green) is maintained, and commit boundaries align with natural linguistic or mathematical units (e.g., clauses, calculations), demonstrating LSP’s structural snapping in action.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zvw9Hiwa0i_Beyond_S/figures/005_Figure_2.jpg]]
*Figure 2: Figure 2: Quantifying Repair Costs via Token Flip Rate. We measure the percentage of tokens in the active suffix that change their top prediction between consecutive diffusion steps. While the scattered baseline forces the model to constantly reconcile a fragmented context (maintaining high flip rates), LSP locks in a coherent prefix early. This stabilizes the future generation context, drastically reducing token oscillations and repair costs in the mid-to-late stages (from 14.2% down to 4.3%).*

## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Scattered_Acceptance_Fast_and_Coherent_Inference_for_DLMs_via_Longest_Stable_Prefixes.pdf]]
