---
title: "Attention Is All You Need for KV Cache in Diffusion LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Attention_Is_All_You_Need_for_KV_Cache_in_Diffusion_LLMs.pdf
project_link: https://vila-lab.github.io/elastic-cache-webpage/
code_link: null
aliases:
- EC
- AIAYNKCDL
- Elastic-Cache
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "Elastic-Cache uses attention-aware drift tests and layer-depth scheduling to update only necessary KV cache entries in diffusion LLMs."
primary_logic: "It caches distant MASK tokens, monitors the most-attended decoded token for drift, and recomputes KV only from layers where attention similarity falls below a threshold."
claims:
- "The method exploits observations that distant MASK tokens are cacheable, deeper layers drift more, and highly attended tokens drift least."
- "Sliding-window decoding and selective cache refresh reduce redundant QKV computation."
- "The note reports large throughput gains on GSM8K with preserved or improved accuracy."
---

# Attention Is All You Need for KV Cache in Diffusion LLMs

> [!tip] 核心洞察
> 通过三个观察：远距离MASK token可被块缓存；KV漂移随深度增加；最受关注token的漂移最小，从而设计出Elastic-Cache，一种无需训练、架构无关的自适应KV缓存更新策略。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散大语言模型中KV缓存的注意力机制 |
| 英文题名 | Attention Is All You Need for KV Cache in Diffusion LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zkUbhdAiFJ) · [Project](https://vila-lab.github.io/elastic-cache-webpage/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Elastic-Cache |
| Dataset | GSM8K, GSM8K (512 tokens, LLaDA-1.5), GSM8K (Dream-7B) |

> [!tip] 效果简介
> - GSM8K 上，throughput (tokens/sec) and accuracy 为 90.1 t/s, 77.71% accuracy，对比 Fast-dLLM: 44.0 t/s, 74.83% accuracy，变化 2.05× throughput, +2.88% accuracy。
> - GSM8K (512 tokens, LLaDA-1.5) 上，speedup and accuracy 为 45.1× speedup, 81.35% accuracy，对比 LLaDA baseline: 1×, 81.35% accuracy，变化 45.1× speedup, same accuracy。
> - GSM8K (512 tokens, LLaDA-1.5) 上，throughput and accuracy 为 139.4 t/s, 83.7% acc，对比 dLLM-Cache: 16.84 t/s, 80.97% acc，变化 8.28× throughput, +2.73% accuracy。

## 概要

本文提出**Elastic-Cache**，一种无需训练、架构无关的自适应KV缓存更新策略，旨在加速扩散大语言模型（Diffusion LLMs, DLMs）的推理过程。DLM在每一步去噪时对所有token和所有层重新计算QKV，导致大量冗余计算和延迟。Elastic-Cache通过三个关键观察——远距离MASK token可被块缓存、KV漂移随深度增加、最受关注token的漂移最小——设计出联合决定**何时**（通过注意力感知的漂移测试）以及**何处**（通过深度感知的调度）重新计算KV缓存的机制。实验表明，Elastic-Cache在GSM8K（256 tokens）上实现8.7倍加速，在更长序列上实现45.1倍加速，并在GSM8K上比现有基于置信度的方法实现6.8倍更高的吞吐量。



### 2.1 扩散大语言模型（DLM）的推理瓶颈

扩散大语言模型（如LLaDA、Dream-7B）通过掩码扩散过程生成文本：从全MASK序列开始，逐步去噪直至生成完整序列。与自回归Transformer不同，DLM在每一步去噪时对所有token和所有层重新计算QKV，导致计算复杂度为O(T·L·N²)，其中T为去噪步数，L为层数，N为序列长度。这造成了大量冗余计算，因为相邻去噪步之间的token表示变化通常很小。

### 2.2 现有方法的局限性

现有加速方法包括：
- **Fast-dLLM**：基于块的KV缓存和置信度感知解码，但采用固定块解码策略，无法自适应调整。
- **dLLM-Cache**：KV缓存方法，但性能有限。
- **DeepCache**：具有固定间隔更新的KV缓存方法，缺乏灵活性。

这些方法未能充分利用DLM推理过程中的两个关键特性：KV漂移随深度增加，以及最受关注token的漂移最小。

### 2.3 核心观察

本文基于三个关键观察（如Figure 1所示）：

1. **远距离MASK token可被块缓存**：MASK token对当前token的解码影响随距离增加而减小，远距离MASK token主要作为长度偏置先验，其KV可被块缓存。
2. **KV漂移随深度增加**：浅层表示稳定较快，深层表示持续演化，因此缓存更新应从深层开始。
3. **最受关注token的漂移最小**：每步中最受关注的已解码token的KV变化最小，可作为缓存陈旧度的保守指标。



## 核心方法与创新机理

Elastic-Cache的核心创新在于联合决策**何时**以及**何处**更新KV缓存：

1. **注意力感知的漂移测试**：通过最受关注token的注意力权重余弦相似度检测KV漂移，决定是否触发缓存更新。
2. **深度感知的调度**：当检测到漂移时，从发生显著变化的层开始，仅重新计算后续层的KV缓存，浅层重用缓存。
3. **滑动窗口解码**：仅对滑动窗口内的token计算注意力，窗口外的token（包括远距离MASK token）被块缓存。



![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/001_Figure_1.jpg]]

Elastic-Cache的整体框架如Figure 2所示，包含三个主要模块：

1. **滑动窗口解码与KV缓存**：在每一步t，仅对滑动窗口M_β^{t-1}内的token计算注意力，窗口外的token使用缓存的KV。
2. **注意力感知的KV缓存更新**：通过最受关注token的注意力权重余弦相似度检测漂移，决定是否触发缓存更新。
3. **层感知的KV缓存更新**：当检测到漂移时，从层l+1到最后一层重新计算KV缓存，浅层重用缓存。



### 5.1 前向过程与训练损失

掩码扩散模型的前向过程定义为：

$$q_{t|0}(\pmb{x}_t|\pmb{x}_0) = \prod_{i=1}^L q_{t|0}(x_t^i|x_0^i) = \prod_{i=1}^L \mathrm{Cat}(x_t^i; (1-t)\delta_{x_0^i} + t\delta_{\mathrm{MASK}})$$

训练损失为掩码位置上的重加权交叉熵损失：

$$\mathcal{L}_{\mathrm{MDM}} = \int_0^1 \frac{1}{t} \mathbb{E}_{q_{t\mid 0}(\pmb{x}_t|\pmb{x}_0)} \left[ \sum_{i: \pmb{x}_t^i = \mathrm{MASK}} -\log p_\theta(\boldsymbol{x}_0^i|\pmb{x}_t) \right] \mathrm{d}t$$

### 5.2 滑动窗口注意力计算

在步骤t、层l，仅对滑动窗口M_β^{t-1}内的token计算注意力：

$$\mathbf{A}_{[M_\beta^{t-1}]}^{t,l} = \operatorname{softmax}\left( \frac{\mathbf{Q}_{[M_\beta^{t-1}]}^{t,l} (\tilde{\mathbf{K}}_{[\mathcal{L}]}^{t,l})^\top}{\sqrt{d_k}} \right) \tilde{\mathbf{V}}_{[\mathcal{L}]}^{t,l}$$

其中$\tilde{\mathbf{K}}_{[\mathcal{L}]}^{t,l}$和$\tilde{\mathbf{V}}_{[\mathcal{L}]}^{t,l}$是缓存的键和值。

### 5.3 最受关注token选择

选择从滑动窗口接收总注意力最高的已解码token：

$$\mathcal{T}^{t,l} = \arg\max_{k \in \mathcal{D}^{<t}} \sum_{q \in \mathcal{M}_\beta^t} \mathbf{S}_{[q,k]}^{t,l}$$

### 5.4 注意力变化的余弦相似度

测量最受关注token在步骤t-1和t之间注意力权重的变化：

$$\sigma^{t,l} = \frac{\|\mathbf{S}_{[\mathcal{T}^{t-1}]}^{t-1,l} \cdot \mathbf{S}_{[\mathcal{T}^{t-1}]}^{t,l}\|}{\|\mathbf{S}_{[\mathcal{T}^{t-1}]}^{t-1,l}\| \cdot \|\mathbf{S}_{[\mathcal{T}^{t-1}]}^{t,l}\|}$$

### 5.5 缓存更新触发条件

当余弦相似度低于阈值γ时，从该层开始触发缓存更新：

$$l^* = \{ l \text{ if } \sigma^{t,l} < \gamma \}$$

### 5.6 理论分析

**KV漂移定义**：token i在层ℓ从步骤t-1到t的键和值向量的总变化：

$$\Delta_i^{t,\ell} := \|\mathbf{K}_i^{t,\ell} - \mathbf{K}_i^{t-1,\ell}\|_2 + \|\mathbf{V}_i^{t,\ell} - \mathbf{V}_i^{t-1,\ell}\|_2$$

**层间KV漂移单调性**（Theorem A.8）：在过渡层ℓ*之后，期望KV漂移随层深度非递减：

$$\mathbb{E}_t[\Delta^{t,\ell}] \leq \mathbb{E}_t[\Delta^{t,\ell'}], \quad \forall \ell \leq \ell^* < \ell' \leq L$$

**最受关注token漂移界**（Theorem A.9）：最受关注token的KV漂移受平均漂移加上一个小的误差项约束：

$$\Delta_{\mathcal{T}^{t,\ell}}^{t,\ell} \leq \bar{\Delta}^{t,\ell} + O\left(\frac{\sqrt{d_k}}{R_\ell \sqrt{N}}\right)$$



## 实验与关键发现

### 6.1 主要结果

**Table 1**展示了在LLaDA-Instruct套件上的综合基准结果。Elastic-Cache在GSM8K（512 tokens）上达到90.1 t/s（25.2倍加速），准确率77.71%，显著优于Fast-dLLM的44.0 t/s和74.83%准确率。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/006_Table_1.jpg]]
*Table 1: Comprehensive benchmark results on the LLaDA-Instruct suite. Each cell shows accuracy (top) and decoding throughput in tokens/sec with relative speedup to the LLaDA baseline (bottom, blue: t/s / orange: speedup). Highlighted cells denote the highest throughput and speedup per configuration. The highest accuracy is bolded.*

**Table 2**展示了与额外KV缓存方法的比较。在GSM8K（512 tokens）上使用LLaDA-1.5，Elastic-Cache达到139.4 t/s，准确率83.7%，优于dLLM-Cache（16.84 t/s, 80.97%）和DeepCache变体（58.4-60.9 t/s, 81.4-83.1%）。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/007_Table_2.jpg]]
*Table 2: Comparison with additional KV caching methods on GSM8K (5-shot, 512 tokens) using LLaDA-1.5. Each cell shows accuracy (top) and throughput in t/s with relative speedup (bottom, blue: t/s; orange: speedup).*

**Table 3**展示了在LLaDA-1.5套件上的结果。Elastic-Cache在GSM8K（512 tokens）上实现45.1倍加速，准确率81.35%（与基线相同）。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/008_Table_3.jpg]]
*Table 3: Comprehensive benchmark results on the LLaDA-1.5 suite. Each cell shows accuracy (top) and decoding throughput in tokens/sec with relative speedup to the LLaDA baseline (bottom, blue: t/s; orange: speedup). Bold cells denote the highest throughput and speedup per configuration.*

**Table 4**展示了在Dream-v0-Base-7B套件上的结果。Elastic-Cache在GSM8K上实现21.4倍加速，在HumanEval上实现5.5倍加速。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/009_Table_4.jpg]]
*Table 4: Comprehensive benchmark results on the “Dream-v0-Base-7B” suite. Each cell shows accuracy (top) and decoding throughput in tokens/sec with relative speedup to the Dream baseline (bottom, blue: t/s; orange: speedup).*

**Table 5**展示了在多模态LLaDA-V上的结果。在MathVerse-256上，Elastic-Cache达到32.3 t/s，准确率29.2%，优于Fast-dLLM的30.3 t/s和26.8%准确率。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zkUbhdAiFJ_Attentio/figures/010_Table_5.jpg]]
*Table 5: Performance and Speedup Comparison of LLaDA-V on MathVista and MathVerse. Each benchmark presents results from LLaDA-V (base) using Fast-dLLM, and our method.*

### 6.2 消融研究

**Figure 3**展示了消融研究结果：
- (a) 滑动窗口机制与块解码的比较：滑动窗口在吞吐量和准确率上均优于块解码。
- (b) 不同γ下的缓存更新频率：γ=0.95时缓存更新频率仅增加到20%。
- (c) 不同ϵ下的置信度感知解码：增加模型置信度可减少缓存更新频率。

**Table 15**展示了块缓存机制的消融：在β=16时，块缓存提供显著的吞吐量提升（从82.7 t/s到119.8 t/s），准确率影响极小。

**Table 18**验证了最受关注token的稳定性：最受关注token的余弦相似度（0.948-0.985）高于平均缓存token（0.947-0.980），验证了其作为缓存陈旧度指标的保守性。

### 6.3 扩展性分析

**Table 12**展示了峰值GPU内存占用：Elastic-Cache在256/512/1024生成长度上分别占用18.11/18.13/19.37 GB，低于基线的19.04/19.62/20.79 GB和Fast-dLLM的20.49/21.42/23.26 GB。

**Table 14**展示了多GPU可扩展性：在2 GPU和batch size 8下，Elastic-Cache达到225.5 t/s，而Fast-dLLM为68.0 t/s。

**Table 20**展示了与基于一致性的加速方法的比较：Elastic-Cache保持79.2%准确率和109.6 t/s吞吐量，优于一致性LLM的56.5%准确率和35.5 t/s。



## 定位与知识库关联

### 7.1 方法谱系

Elastic-Cache属于扩散大语言模型加速方法，其方法谱系包括：

1. **扩散模型基础**：基于Sohl-Dickstein et al. (2015)的扩散模型公式和Ho et al. (2020)的去噪扩散概率模型。
2. **离散扩散模型**：Austin et al. (2021a)的结构化去噪扩散模型和Nie et al. (2025a)的LLaDA。
3. **DLM加速方法**：Wu et al. (2025)的Fast-dLLM、Ma et al. (2025)的dKV-Cache、Ma et al. (2024)的DeepCache。
4. **Transformer推理优化**：Vaswani et al. (2017)的KV缓存机制。

### 7.2 知识库定位

Elastic-Cache的核心贡献在于：
- **无需训练**：与基于蒸馏的方法（如一致性模型）不同，Elastic-Cache无需额外训练。
- **架构无关**：可应用于任何基于Transformer的DLM。
- **自适应**：自动检测KV漂移并调整缓存更新策略，无需手动调整。
- **理论保证**：提供了KV漂移的严格理论分析，包括层间单调性和最受关注token的漂移界。

### 7.3 局限性

1. Elastic-Cache的有效性高度依赖于模型预测的准确性；当模型预测不准确时，缓存更新频率可能增加，降低加速效果。
2. 在短生成序列（如256 tokens）上的加速比有限（1.1倍），因为缓存重用机会较少。
3. 注意力阈值γ需要针对不同任务和模型进行调整，以平衡速度与准确率。
4. 理论分析依赖于若干假设（如层间表示动态、注意力集中性），这些假设在极端情况下可能不成立。

### 7.4 开放问题

1. 如何自动确定最优的注意力阈值γ和滑动窗口大小β，而无需手动调整？
2. Elastic-Cache是否可以扩展到其他类型的扩散模型（如连续扩散模型）？
3. 理论分析中的常数c和过渡层ℓ*的具体值是多少？
4. 该方法在更大规模模型（如70B参数）上的性能如何？
5. 是否可以结合其他加速技术（如模型剪枝、量化）以进一步减少延迟？



## 原文 PDF

![[paperPDFs/ICLR_2026/Attention_Is_All_You_Need_for_KV_Cache_in_Diffusion_LLMs.pdf]]
