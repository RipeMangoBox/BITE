---
title: "Wide-In, Narrow-Out: Revokable Decoding for Efficient and Effective DLLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Wide_In_Narrow_Out_Revokable_Decoding_for_Efficient_and_Effective_DLLMs.pdf
project_link: null
code_link: https://github.com/Feng-Hong/WINO-DLLM
aliases:
- WNOW
- WNORDEED
- "Wide-In, Narrow-Out (WINO)"
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "用可撤销草稿验证机制并行解码扩散大语言模型token。"
primary_logic: "WINO先用宽松阈值并行草稿多个token，再用影子块和注意力掩码重新验证并撤销低置信token。"
claims:
- "标准DLLM解码不可逆，早期错误会被永久固化并限制并行加速质量。"
- "WINO通过低阈值Wide-In草稿和高阈值Narrow-Out验证在速度与质量间调节。"
- "影子块共享位置ID但受注意力掩码约束，可无信息泄露地验证当前块token。"
- "WINO在GSM8K、ARC和多模态任务上显著减少解码步数，同时保持或提升准确率。"
---

# Wide-In, Narrow-Out: Revokable Decoding for Efficient and Effective DLLMs

> [!tip] 核心洞察
> 核心洞察是：通过打破标准DLLM解码的不可逆性，允许模型在后续步骤中利用不断丰富的双向上下文信息来修正早期生成的token，从而在实现大幅加速的同时，甚至能提升生成质量。WINO 通过一个精心设计的影子块（shadow block）和注意力掩码，在不引入信息泄露的前提下，实现了高效的并行草稿与验证。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Wide-In, Narrow-Out：面向高效且有效 DLLM 的可撤销解码 |
| 英文题名 | Wide-In, Narrow-Out: Revokable Decoding for Efficient and Effective DLLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XtLQHlNLxy) · [GitHub](https://github.com/Feng-Hong/WINO-DLLM) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Wide-In, Narrow-Out (WINO) |
| Dataset | GSM8K, ARC-E |

> [!tip] 效果简介
> - GSM8K 上，Accuracy 为 75.82，对比 73.24，变化 +2.58。
> - GSM8K 上，Steps 为 41.93，对比 256.00，变化 6.10× reduction。
> - GSM8K 上，TPS 为 100.53，对比 17.76，变化 5.66× speedup。

## 概要

本文提出了一种名为 **Wide-In, Narrow-Out (WINO)** 的新型解码算法，旨在解决扩散大语言模型（Diffusion Large Language Models, DLLMs）在推理过程中面临的质量-速度两难困境。WINO 的核心思想是引入**可撤销解码**机制：通过一个并行的草稿-验证（draft-and-verify）流程，模型可以激进地生成多个候选 token（Wide-In），然后利用不断丰富的全局上下文重新评估这些 token，并将低质量的 token 重新掩码以进行后续精炼（Narrow-Out）。实验表明，WINO 在多种语言和视觉-语言任务上实现了显著的加速（最高达 10 倍），同时甚至提升了生成质量。例如，在 GSM8K 数学推理基准上，WINO 实现了 6 倍加速，同时准确率提升了 2.58%；在 Flickr30K 图像描述基准上，实现了 10 倍加速，同时性能更高。WINO 是一种无需训练、即插即用的解码算法。

### 2.1 标准解码的不可逆性

DLLMs（如 LLaDA 和 MMaDA）的标准解码过程是**不可逆的**。该过程通常从一个全 [MASK] 序列开始，然后在每一步贪婪地解码一个最自信的 token。一旦一个 token 被解码，该决策即最终确定，无法在后续步骤中修改。这种不可逆性导致早期错误被永久固化并累积传播，使得并行解码（一次生成多个 token）时质量严重下降，从而陷入质量-速度的两难困境。

标准贪婪解码步骤的数学形式化如公式 (1) 所示：

$$ \begin{array}{c} \begin{array} { r l } & { l ^ { ( k ) } = \underset { l \in \{ l | y _ { l } ^ { ( k - 1 ) } = \left[ \operatorname*{ I M A S K } \right] \} } { \arg \operatorname*{ m a x } } \left( \underset { v \in V } { \operatorname*{ m a x } } p _ { \theta } \big ( \hat { y } _ { l } = v | X , Y ^ { ( k - 1 ) } \big ) \right) , } \\\\ { y _ { l } ^ { ( k ) } = \left\{ \underset { y _ { l } ^ { ( k - 1 ) } , } { \arg \operatorname*{ m a x } } p _ { \theta } \big ( \hat { y } _ { l } = v | X , Y ^ { ( k - 1 ) } \big ) , \right.} & { \mathrm { i f } l = l ^ { ( k ) } , } \\\\ { \mathrm { o t h e r w i s e } , } \end{array}  \quad \forall l \in \{ 1 , 2 , \dots , L \} .  \end{array} $$

### 2.2 现有加速方法的局限

现有的 DLLM 加速方法，如朴素并行采样（一次解码 M 个 token）、Fast-dLLM-parallel（基于置信度阈值的并行解码）和 Entropy-Bounded (EB) Sampler（基于熵约束的并行解码），虽然能提升速度，但通常以牺牲质量为代价。这些方法本质上仍然遵循不可逆的解码范式，因此无法避免早期错误累积的问题。

## 核心方法与创新机理

WINO 的核心创新在于**打破标准 DLLM 解码的不可逆性**，通过引入一个并行的草稿-验证机制，使解码过程变得可撤销。具体来说：

1. **可撤销解码**：允许模型在后续步骤中利用不断丰富的双向上下文信息来修正早期生成的 token，从而在实现大幅加速的同时，甚至能提升生成质量。
2. **草稿-验证机制**：包含一个宽松的草稿阈值 τ1（用于快速生成候选 token）和一个严格的验证阈值 τ2（用于重新评估并撤销低质量 token）。通过调整这两个阈值，可以控制生成速度与质量之间的平衡。
3. **影子块（Shadow Block）与自定义注意力掩码**：在不引入信息泄露的前提下，实现了高效的并行草稿与验证。

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/001_Figure_1.jpg]]
*Figure 1: Demonstration of speedup and performance improvement of WINO over standard decoding and naive parallel sampling evaluated on GSM8K with LLaDA and Flickr30K with MMaDA. The standard decoding unmasks 1 token per decoding step, while the naive parallel sampling unmasks M(> 1) tokens per decoding step. We set M = 4 for GSM8K and M = 8 for Flickr30K.*

WINO 的整体框架如 Figure 2(a) 所示。该框架基于半自回归扩散解码策略，将响应序列分割成多个块（block），并按从左到右的顺序依次解码每个块。对于当前正在解码的块，WINO 执行一个迭代的草稿-验证循环，直到该块中的所有 token 都被解码且通过验证。

Figure 2: (a) An overview of WINO.

Figure 2: (b) Illustration of our designed attention mask.

WINO 的完整解码算法如 Algorithm 1 所示。

Algorithm 1 WINO Decoding for a Single Block

### 5.1 草稿模块（Draft Module）

草稿模块基于一个宽松的置信度阈值 τ1，并行地将多个 [MASK] token 解码为候选 token。其规则如公式 (2) 所示：

$$ y _ { \mathrm { c u r } , l } ^ { ( k ) } = \underset { v \in V } { \operatorname { a r g m a x } } p \theta ( \hat { y } _ { \mathrm { c u r } , l } = v | Y ) , \ \mathrm { i f } \ \underset { v \in V } { \operatorname*{ m a x } } p \theta ( \hat { y } _ { \mathrm { c u r } , l } = v | Y ) > \tau _ { 1 } \ \mathrm { a n d } \ y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } = \overset { \left[ \mathrm { I M A S K } \right] } { \left[ \mathrm { I M A S K } \right] } . $$

该公式的含义是：如果当前块中某个 [MASK] token 的最大预测概率超过阈值 τ1，则将其解码为 argmax token。较低的 τ1 值可以加速解码过程，但可能引入更多错误。

WINO 还支持通过 Gumbel-Max trick 实现随机采样，从而在草稿阶段引入多样性。

### 5.2 验证模块（Verify Module）

验证模块利用新丰富的全局上下文，重新评估所有已解码的 token，并将置信度低于阈值 τ2 的 token 重新掩码。为了实现无信息泄露的验证，WINO 设计了一个**影子块（Shadow Block）**——一个由 [MASK] token 组成的辅助块，附加到序列末尾。影子块中的 token 与当前块 token 共享相同的位置 ID，但被禁止关注当前块中对应位置的 token（如 Figure 2(b) 的注意力掩码所示）。

验证规则如公式 (3) 所示：

$$ y _ { \mathrm { c u r } , l } ^ { ( k ) } = [ \underline { { \mathrm { I M A S K } } } ] , \ \mathrm { i f } \ p _ { \theta } \big ( \hat { y } _ { \mathrm { s h a d } , l } = y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } | \tilde { Y } ) \big ) < \tau _ { 2 } \ \mathrm { a n d } \ y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } \neq [ \underline { { \mathrm { [ M A S K ] } } } ] , $$

该公式的含义是：如果影子块对当前已解码 token 的预测概率低于阈值 τ2，则将该 token 重新掩码。较高的 τ2 值可以确保最终输出的质量。

### 5.3 整体解码过程

草稿和验证在单次前向传播中完成。整体解码步骤如公式 (4) 所示：

$$ y _ { \mathrm { c u r } , l } ^ { ( k ) } = \left\{ \begin{array} { l l } { \underset { \boldsymbol { v } \in V } { \operatorname { a r g m a x } } p _ { \boldsymbol { \theta } } ( \hat { y } _ { \mathrm { c u r } , l } = \boldsymbol { v } | \tilde { Y } ) , } & { \mathrm { i f } \underset { \boldsymbol { v } \in V } { \operatorname*{ m a x } } p _ { \boldsymbol { \theta } } ( \hat { y } _ { \mathrm { c u r } , l } = \boldsymbol { v } | \tilde { Y } ) > \tau _ { 1 } \mathrm { ~ a n d ~ } y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } = \frac { \left[ \mathrm { M A S K } \right] } { \left[ \mathrm { M A S K } \right] } , } \\\\ { \frac { \left[ \mathrm { I R A S K } \right] } { \left[ \mathrm { M A } ^ { ( k - 1 ) } \right] } , } & { \mathrm { i f } p _ { \boldsymbol { \theta } } ( \hat { y } _ { \mathrm { s h a d } , l } = y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } | \tilde { Y } ) ) < \tau _ { 2 } \mathrm { ~ a n d ~ } y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } \neq \frac { \left[ \mathrm { M A S K } \right] } { \left[ \mathrm { M A S K } \right] } , } \\\\ { y _ { \mathrm { c u r } , l } ^ { ( k - 1 ) } , } & { \mathrm { o t h e r w i s e } . } \end{array} \right. $$

该过程迭代进行，直到当前块中不再有 [MASK] token。

## 实验与关键发现

### 6.1 主要结果

WINO 在多种语言和多模态基准上进行了评估，主要结果如 Table 1 和 Table 2 所示。

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/004_Table_1.jpg]]
*Table 1: Performance and inference speedup comparison on diverse language benchmarks.*

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/006_Table_2.jpg]]
*Table 2: Performance and inference speedup comparison across diverse multi-modal understanding and reasoning benchmarks. We use CIDEr for Flickr30k and accuracy for other benchmarks.*

Table 2: Performance and inference speedup comparison across diverse multi-modal understanding and reasoning benchmarks.

**语言任务（基于 LLaDA 模型）：**

| 基准 | 指标 | 标准解码 | WINO | 提升 |
|------|------|----------|------|------|
| GSM8K | 准确率 | 73.24 | **75.82** | +2.58 |
| GSM8K | 步数 | 256.00 | **41.93** | 6.10× 减少 |
| GSM8K | TPS | 17.76 | **100.53** | 5.66× 加速 |
| ARC-E | 准确率 | 59.13 | **81.19** | +22.06 |
| ARC-E | 步数 | 256.00 | **40.19** | 6.37× 减少 |
| ARC-C | 准确率 | 51.87 | **73.89** | +22.02 |
| ARC-C | 步数 | 256.00 | **47.41** | 5.40× 减少 |
| MATH-500 | 步数 | 256.00 | **74.44** | 3.44× 减少 |
| HumanEval | 步数 | 256.00 | **93.32** | 2.74× 减少 |

**多模态任务（基于 MMaDA 模型）：**

| 基准 | 步数减少 |
|------|----------|
| Flickr30k | **10.05×** |
| MATH-Vision | **5.73×** |

WINO 在 AI2D、MMMU 和 ScienceQA 上也提升了性能，同时在 Flickr30k、MATH-Vision 和 MathVista 上保持了可比的结果。

### 6.2 与先进动态采样器的比较

如 Table 6 所示，WINO 在质量-速度权衡上显著优于 Fast-dLLM-parallel 和 EB Sampler。

Table 6: Comparison with advanced dynamic samplers (Fast-dLLM-parallel and EB Sampler) on GSM8K and MMMU-val.

| 方法 | GSM8K 准确率 | GSM8K 加速 | MMMU-val 准确率 | MMMU-val 加速 |
|------|-------------|------------|-----------------|---------------|
| Fast-dLLM-parallel | 72.33% | 3.16× | 19.89% | 7.18× |
| EB Sampler | 70.37% | 2.63× | 17.87% | 4.13× |
| **WINO** | **75.82%** | **5.66×** | **24.00%** | **6.00×** |

### 6.3 消融实验

**验证模块的必要性：** 如 Table 4 所示，移除验证模块（"Only Draft"）在激进阈值（τ1=0.6）下会导致显著的性能下降。

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/008_Table_4.jpg]]
*Table 4: Experiment results on the variant of WINO without the verification module.*

**注意力掩码设计：** 允许影子块直接关注当前块对应位置（信息泄露）会导致准确率显著下降（例如在 GSM8K 上下降 3.57%）。

**阈值消融：** Figure 4 展示了草稿阈值 τ1 和验证阈值 τ2 的影响。较低的 τ1 加速解码，较高的 τ2 确保质量。

Figure 4: Ablation study on the drafting threshold τ1 and the verification threshold τ2

**延迟分析：** 如 Table 7 所示，WINO 的自定义注意力掩码在控制总序列长度时，与标准全注意力相比不会引入额外延迟。

Table 7: Per-step wall-clock latency ablation (ms).

**随机采样：** 如 Table 5 所示，WINO 在随机采样（温度=0.5）下，在 GSM8K 上达到 76.06% 的准确率，步骤减少 6.05 倍。

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/012_Table_5.jpg]]
*Table 5: Performance comparison using stochastic sampling (temperature = 0.5). We report the mean and standard deviation over 3 runs.*

**内存开销：** 如 Figure 6 所示，WINO 在 GSM8K 的半自回归设置下，GPU 内存增加约 2.4%（16.18GB vs 16.57GB）。

Figure 6: GPU memory usage.

### 6.4 案例研究

Figure 5 展示了一个 GSM8K 的案例研究。标准解码（LLaDA）在第 162 步产生了一个错误 token，导致最终答案为 96（正确答案为 84）。而 WINO 通过迭代的草稿-验证机制，逐步修正了早期错误，最终得到了正确答案 84。

Figure 5: Case Study: GSM8K Example.

![[assets/figures/papers/iclr26_0001_XtLQHlNLxy_Wide-In_Narrow-Out_Revokable_Decoding_for_Effici/figures/007_Table_3.jpg]]
*Table 3: Experiment results on different generation lengths and full diffusion setting, respectively.*

## 定位与知识库关联

WINO 属于**扩散大语言模型（DLLMs）推理加速**这一研究方向。其核心思想——通过可撤销解码打破标准解码的不可逆性——与以下方法形成对比：

- **标准贪婪解码**：不可逆，每步解码一个 token，质量高但速度慢。
- **朴素并行采样**：每步解码 M 个 token，速度快但质量下降严重。
- **动态采样器（Fast-dLLM-parallel, EB Sampler）**：通过置信度或熵约束进行并行解码，但仍不可逆，质量-速度权衡有限。
- **WINO**：通过草稿-验证机制实现可撤销解码，在加速的同时甚至能提升质量。

WINO 是一种**无需训练、即插即用**的解码算法，可以应用于任何基于半自回归扩散解码的 DLLM（如 LLaDA 和 MMaDA）。其加速程度与基础模型的能力固有相关：更熟练的模型能产生更好的草稿，需要的精炼步骤更少，从而获得更大的加速。

**局限性：**
- 加速程度与基础模型的能力相关。
- 影子块会引入线性内存开销（半自回归设置下约 2.4%，全扩散设置下低于 8%）。
- 未探讨在极长序列生成或对延迟极度敏感的场景下的表现。
- 未讨论在不同架构或规模的基础模型上的泛化能力。

## 原文 PDF

![[paperPDFs/ICLR_2026/Wide_In_Narrow_Out_Revokable_Decoding_for_Efficient_and_Effective_DLLMs.pdf]]
