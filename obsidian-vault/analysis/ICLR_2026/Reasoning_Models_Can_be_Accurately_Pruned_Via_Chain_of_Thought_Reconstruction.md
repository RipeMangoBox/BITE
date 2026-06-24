---
title: "Reasoning Models Can be Accurately Pruned Via Chain-of-Thought Reconstruction"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reasoning_Models_Can_be_Accurately_Pruned_Via_Chain_of_Thought_Reconstruction.pdf
openreview_forum_id: tyGfwG6xTh
aliases:
- RACR
- RMCBAPCTR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "剪枝校准时使用的激活分布：是否包含模型自身策略生成的思维链（CoT）激活。"
primary_logic: "在剪枝校准阶段，通过自回归生成并收集模型的链式思维（CoT）激活，将校准分布与推理时的解码分布对齐，从而显著提升剪枝后模型的推理能力。"
claims:
- "RAC在DeepSeek-R1-Distill-Qwen-7B上50%稀疏度下准确率达0.900，显著优于C4校准的0.744和Prompt-Only的0.812，同时将推理时间从135分钟降至35分钟。"
- "在MATH500基准上，RAC将剪枝模型准确率最高提升17%，并在50%稀疏度下保留高达95%的密集模型准确率。"
- "图2展示RAC在解码阶段的重建误差显著低于Prompt-Only方法，验证了其对齐解码分布的有效性。"
- "RAC无需重新训练，且可无缝集成至现有剪枝算法（SparseGPT、WANDA、ALPS）中。"
---

# Reasoning Models Can be Accurately Pruned Via Chain-of-Thought Reconstruction

> [!tip] 核心洞察
> 在剪枝校准阶段，通过自回归生成并收集模型的链式思维（CoT）激活，将校准分布与推理时的解码分布对齐，从而显著提升剪枝后模型的推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于思维链重建的推理模型精确剪枝方法 |
| 英文题名 | Reasoning Models Can be Accurately Pruned Via Chain-of-Thought Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tyGfwG6xTh); [GitHub](https://github.com/RyanLucas3/Reasoning-Aware-Compression) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Reasoning-Aware Compression (RAC) |
| Dataset | MATH500, AIME-25 |

> [!tip] 效果简介
> - MATH500 上，acc@1:1 (50% sparsity, DeepSeek-R1-Qwen-7B) 为 0.900，对比 0.744 (C4), 0.812 (Prompt-Only)，变化 +0.156 vs C4, +0.088 vs Prompt-Only。
> - MATH500 上，Runtime (min, 50% sparsity, DeepSeek-R1-Qwen-7B) 为 35.3，对比 135.0 (C4), 115.6 (Prompt-Only)，变化 -99.7 vs C4, -80.3 vs Prompt-Only。
> - MATH500 上，acc@1:1 (50% sparsity, Qwen3-8B) 为 0.862，对比 0.564 (C4), 0.470 (Prompt-Only)，变化 +0.298 vs C4, +0.392 vs Prompt-Only。

## 概述

### 问题背景

大语言模型（LLM）在复杂推理任务上表现出色，但其庞大的参数量和推理时的长链式思维（Chain-of-Thought, CoT）生成，导致部署成本极高。标准的后训练剪枝方法（如 SparseGPT）通过最小化输入激活的重建误差来压缩模型，然而推理模型的计算瓶颈主要发生在解码阶段——CoT 序列通常远长于提示词（prompt），使得剪枝时的校准分布与推理时的解码分布之间存在显著的**分布偏移**。直接应用传统剪枝方法不仅导致准确率大幅下降，还会引发模型生成序列长度膨胀，反而使推理速度变慢（Figure 1）。

### 核心方法

本文提出 **Reasoning-Aware Compression (RAC)**，一种无需重新训练的推理模型剪枝方法。RAC 的核心思想是在剪枝校准阶段，通过模型**自回归生成**自身的链式思维（CoT）激活，将校准分布与推理时的解码分布对齐。具体而言，RAC 在收集校准激活时，不仅包含提示词部分的隐藏状态，还包含模型基于自身策略（on-policy）采样生成的解码阶段隐藏状态，从而构建一个覆盖完整推理过程的校准矩阵。该矩阵随后可直接输入到现有的逐层剪枝算法（如 SparseGPT、WANDA、ALPS）中，无需修改剪枝算法本身。

### 主要结果

RAC 在多个推理基准上展现出显著的性能优势：

- **MATH500 基准**：在 DeepSeek-R1-Distill-Qwen-7B 上，50% 稀疏度下 RAC 准确率达到 **0.900**，相比 C4 校准的 0.744 提升 15.6 个百分点，相比 Prompt-Only 校准的 0.812 提升 8.8 个百分点。同时，推理时间从 135 分钟降至 **35 分钟**（Table 1）。
- **跨模型泛化**：在 Qwen3-8B 上，50% 稀疏度下 RAC 准确率达 0.862，较 C4 校准（0.564）提升近 30 个百分点（Table 2）；在 Qwen3-14B 的 AIME-25 基准上，结合 ALPS 剪枝算法，RAC 准确率达 0.667，较 C4 校准（0.267）提升 40 个百分点（Table 10）。
- **精度保持**：RAC 在 50% 稀疏度下可保留高达 **95%** 的密集模型准确率，且最大准确率提升达 **17%**。
- **算法兼容性**：RAC 可无缝集成至 SparseGPT、WANDA、ALPS 等主流剪枝算法中，且在半结构化 2:4 稀疏性下结合 FP8 量化可实现 1823 tok/s 的吞吐量，较密集模型提升 28%（Table 6）。

### 方法定位

RAC 属于**校准数据增强**方法，通过改变剪枝时的激活分布来提升压缩质量，而非设计新的剪枝算法。其关键创新在于首次将推理模型的**解码阶段激活**纳入剪枝校准，解决了传统方法在推理任务上的分布偏移问题。该方法适用于单次剪枝（one-shot pruning）场景，无需微调或重训练，校准过程可在单张 H100 GPU 上完成。

## 背景与动机

### 推理模型剪枝的独特困境

大型语言模型（LLM）的剪枝方法在过去几年取得了长足进展，诸如 **SparseGPT**（Frantar & Alistarh, ICML 2023）、**WANDA**（Sun et al., 2024）和 **ALPS**（Meng et al., 2024）等单次剪枝（one-shot pruning）算法，已能在通用任务上以较低的计算代价实现可观的稀疏度。这些方法的共同核心是逐层重建：对于第 $\ell$ 层权重 $\mathbf{W}_\ell$，它们通过求解以下约束优化问题来寻找压缩后的权重 $\widehat{\mathbf{W}}_\ell$：

$$
\operatorname*{min}_{\widehat{\mathbf{W}}_\ell} \|\mathbf{W}_\ell \mathbf{X}_\ell - \widehat{\mathbf{W}}_\ell \mathbf{X}_\ell\|_2^2 \quad \text{s.t.} \quad \|\widehat{\mathbf{W}}_\ell\|_0 \leq S
$$

其中 $\mathbf{X}_\ell \in \mathbb{R}^{d_\ell \times N}$ 是由校准数据中各 token 在第 $\ell-1$ 层的隐藏状态拼接而成的激活矩阵。这一范式的隐含假设是：校准阶段收集的激活分布与推理时的解码分布足够接近。

然而，当剪枝对象从通用 LLM 转向**推理模型**（reasoning models）时，这一假设出现了根本性裂痕。

### 分布偏移：校准与推理的失配

推理模型——如 DeepSeek-R1 系列——的核心特征是**长链式思维（Chain-of-Thought, CoT）**。这类模型在强化学习阶段通过 GRPO（Group-Relative Policy Optimization）等算法进行训练：

$$
\mathcal{L}_{\mathrm{GRPO}}(\theta) = -\frac{1}{K}\sum_{k=1}^K \mathrm{clip}\big(\rho_k(\theta), 1-\varepsilon, 1+\varepsilon\big)(r_k - \bar{r})
$$

训练使模型学会在给出最终答案前生成大量中间推理步骤。因此，在推理时，CoT 的 token 数量远超输入提示词（prompt）的 token 数量：$|\text{CoT}| \gg |\text{prompt}|$。这意味着推理模型的解码分布由模型**自身策略生成**的 CoT 激活所主导，而非来自外部语料的输入激活。

标准剪枝方法的校准策略恰恰忽视了这一关键差异。它们仅使用两类激活进行校准：
- **C4 校准**：从通用文本语料（如 C4）中收集激活，其分布与数学推理或代码生成场景几乎无关；
- **Prompt-Only 校准**：仅收集提示词部分的激活，完全忽略了占推理过程主导地位的 CoT 解码阶段。

这种校准-推理分布偏移的后果是严重的。如图 1 所示，当使用 SparseGPT 对 DeepSeek-R1-Distill-Qwen-7B 在 MATH-500 上进行剪枝时，C4 校准导致准确率急剧下降，同时推理时间反而增加——模型生成了更多低质量 token 却无法得出正确答案。这一现象揭示了剪枝后模型的一种失败模式：**“唠叨但低质量”输出**，即模型保留了生成能力，但推理质量严重退化。

### 核心洞察：对齐校准与解码分布

问题的根源在于剪枝时的重建目标与推理时的解码分布之间存在分布偏移。解决这一问题的因果杠杆是**校准时使用的激活分布**：如果校准阶段能够包含模型自身策略生成的 CoT 激活，重建目标就能与推理时的实际计算对齐。

基于这一洞察，本文提出 **Reasoning-Aware Compression（RAC）**，其核心思路简洁而直接：在剪枝校准阶段，不仅收集提示词的激活，还通过自回归生成收集模型自身的 CoT 激活，将两者拼接为完整的校准矩阵，从而使逐层剪枝的重建误差最小化过程能够感知到推理阶段的解码分布。

## 核心创新

### 问题瓶颈：推理模型的剪枝失效源于校准分布偏移

标准大语言模型的一步式剪枝方法（如 **SparseGPT**（Frantar & Alistarh, ICML 2023）、**WANDA**（Sun et al., 2024））在校准阶段仅使用通用文本（如 C4 数据集）或仅使用提示词（Prompt）的激活来构建重建目标。然而，推理模型的核心特征是长链式思维（Chain-of-Thought, CoT）——在 MATH500 等推理基准上，解码阶段生成的 CoT token 数量远超输入提示词。这一结构差异导致校准时的激活分布与推理时的解码分布之间存在严重的分布偏移：剪枝后的模型在解码阶段累积重建误差，表现为准确率大幅下降（Figure 1）且生成序列长度异常膨胀，推理速度反而变慢。

**因果调节变量**是剪枝校准时使用的激活分布是否包含模型自身策略生成的 CoT 激活。当校准仅覆盖提示词阶段时，剪枝算法对解码阶段的权重重要性估计存在系统性偏差。

### 核心洞察：通过自生成 CoT 对齐校准与推理分布

本工作提出的 **Reasoning-Aware Compression (RAC)** 方法基于一个简洁的洞察：在校准阶段，让密集模型自回归生成 CoT token，并收集这些解码阶段的隐藏状态作为校准矩阵的扩展部分，从而使剪枝时的重建目标与推理时的实际激活分布对齐。其关键创新在于改变了剪枝流程中的**校准数据构造方式**：

| 方法槽位 | 基线做法 | RAC 做法 |
|---------|---------|---------|
| 校准数据 | 仅使用 C4 数据集激活或仅使用提示词激活 | 同时使用提示词激活 + 模型自身策略生成的 CoT 激活 |

具体而言，RAC 在 Algorithm 1 中定义了三个流水线模块：

1. **激活收集阶段**：对每个校准样本的提示词部分，前向传播并收集各层的输入激活矩阵 $\mathbf{X}_\ell$。
2. **解码阶段激活收集（On-policy Generation）**：从提示词的最后一个隐藏状态出发，模型自回归采样下一 token $z_{t+1}^{(m)} \sim \pi_\theta(\cdot \mid z_{0:t}^{(m)})$，将采样 token 嵌入后继续前向传播，收集解码阶段每一步的激活，拼接到校准矩阵中，形成 $\mathbf{X}_\ell^{\mathrm{RAC}}$。
3. **逐层剪枝**：以扩展后的 RAC 校准矩阵为目标，使用 SparseGPT 等标准算法求解层剪枝目标函数 $\min_{\widehat{\mathbf{W}}_\ell} \|(\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{X}_\ell^{\mathrm{RAC}}\|_F^2$，约束稀疏度 $S$。

RAC 校准损失的 Frobenius 范数展开为：

$$\lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{X}_\ell^{\mathrm{RAC}} \rVert_F^2 = \sum_{m=1}^{M} \sum_{t\in\mathcal{P}_m\cup\mathcal{D}_m} \lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{x}_t^{(\ell-1,m)} \rVert_2^2$$

其中 $\mathcal{P}_m$ 和 $\mathcal{D}_m$ 分别表示提示词和解码阶段的 token 索引集合，确保重建目标覆盖推理全过程的激活。

### 方法特性：无需重训练、即插即用

RAC 不引入额外的训练步骤，校准阶段仅需在单张 H100 GPU 上完成密集模型的 CoT 生成。该方法可无缝集成至现有剪枝算法（SparseGPT、WANDA、ALPS（Meng et al., 2024））中，仅需替换校准数据构造逻辑，无需修改剪枝求解器本身。这一设计使其具有高度的工程可迁移性。

### 决定性证据

- **Figure 2** 的 token 级重建误差热图直接验证了核心洞察：在提示词阶段，Prompt-Only 校准与 RAC 的重建误差相当（比率 $r_t = e_t^{(\mathrm{Prompt})} / e_t^{(\mathrm{RAC})} \approx 1$）；但在解码阶段，RAC 的误差显著更低（$r_t > 1$，蓝色区域占据解码阶段的绝大部分 token 位置），证明 CoT 激活的重建有效降低了解码分布偏移。
- **Table 1** 显示，在 DeepSeek-R1-Distill-Qwen-7B 的 50% 稀疏度下，RAC 准确率达到 0.900，显著优于 C4 校准的 0.744（+0.156）和 Prompt-Only 的 0.812（+0.088），同时将推理时间从 135 分钟降至 35 分钟。
- 跨模型泛化：在 Qwen3-8B 50% 稀疏度下，RAC 准确率 0.862，相比 C4 的 0.564 和 Prompt-Only 的 0.470 提升超过 0.29（Table 2）。
- 跨算法泛化：RAC 与 ALPS 结合后在 Qwen3-14B 的 AIME-25 基准上达到 0.667，远超 C4 的 0.267（+0.400）（Table 10）。

## 整体框架

### 核心瓶颈与因果开关

标准大语言模型（LLM）的逐层剪枝方法在校准阶段仅收集输入提示词（prompt）的激活矩阵，以最小化层输出重建误差为目标进行权重压缩。这一范式对通用LLM有效，但在推理模型上暴露出根本性失效：推理模型以长思维链（Chain-of-Thought, CoT）为主导，解码阶段（decode phase）的token数远超提示词阶段（|D_m| >> |P_m|），导致校准分布与推理时的解码分布之间存在显著的**分布偏移**。直接后果是剪枝后模型准确率大幅下降，同时生成长度膨胀、推理变慢（Figure 1）。

**因果调节变量**是剪枝校准时所使用的激活分布——是否包含模型自身策略（on-policy）生成的思维链激活。**核心洞察**在于：在剪枝校准阶段，通过自回归生成并收集模型的链式思维激活，将校准分布与推理时的解码分布对齐，从而显著提升剪枝后模型的推理能力。

### 方法概览：推理感知压缩（Reasoning-Aware Compression, RAC）

RAC 是一种**无需重新训练**的校准数据构造策略，可无缝集成至现有剪枝算法（如 **SparseGPT** (Frantar & Alistarh, ICML 2023)、**WANDA** (Sun et al., 2024)、**ALPS** (Meng et al., 2024)）中。其核心改动在于将校准数据从“仅使用C4数据集或仅使用提示词激活”替换为“同时使用提示词激活和模型自身策略生成的链式思维激活”。

### 流水线模块

RAC 的整体流水线由三个顺序模块构成（参见 Algorithm 1）：

1. **激活收集阶段（Prompt Activation Collection）**：对每个校准提示词 $x^{(m)}$，前向传播并收集各层的输入激活矩阵 $\mathbf{X}_\ell^{\text{prompt}}$。

2. **解码阶段激活收集（Decode-time Activation Collection via On-policy Generation）**：在提示词之后，模型自回归生成思维链 token：
   $$z_{t+1}^{(m)} \sim \pi_\theta(\cdot \mid z_{0:t}^{(m)}), \quad \pi_\theta(\cdot \mid z_{0:t}^{(m)}) = \mathrm{softmax}(W_{\mathrm{out}} \mathbf{x}_t^{(L,m)})$$
   每生成一个 token，立即收集各层的隐藏状态 $\mathbf{x}_t^{(\ell,m)}$，并将其拼接至校准矩阵，形成完整的 RAC 校准矩阵 $\mathbf{X}_\ell^{\mathrm{RAC}}$。

3. **逐层剪枝（Layer-wise Pruning）**：使用 SparseGPT 等标准剪枝算法，基于 RAC 校准矩阵进行权重剪枝，目标函数为：
   $$\lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{X}_\ell^{\mathrm{RAC}} \rVert_F^2 = \sum_{m=1}^{M} \sum_{t\in\mathcal{P}_m\cup\mathcal{D}_m} \lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{x}_t^{(\ell-1,m)} \rVert_2^2$$
   即在稀疏度约束下，最小化所有提示词和解码阶段激活的重建误差。

### 输入输出流

- **输入**：校准提示词集合 $\{x^{(m)}\}_{m=1}^M$，密集模型权重 $\{\mathbf{W}_\ell\}_{\ell=1}^L$，目标稀疏度 $S$，最大解码token数 $T_{\max}$。
- **中间产物**：RAC 校准矩阵 $\mathbf{X}_\ell^{\mathrm{RAC}}$，包含提示词激活和自回归生成的 CoT 激活。
- **输出**：压缩后的稀疏权重 $\{\widehat{\mathbf{W}}_\ell\}_{\ell=1}^L$。

### 关键证据强度

RAC 的有效性在数学推理（MATH500、AIME-25）和代码生成（LiveCodeBench）基准上得到验证，覆盖 DeepSeek-R1 和 Qwen3 多个参数规模的模型：

- 在 DeepSeek-R1-Distill-Qwen-7B 上，50% 稀疏度下 RAC 准确率达 **0.900**，显著优于 C4 校准的 **0.744** 和 Prompt-Only 的 **0.812**，同时将推理时间从 135 分钟降至 **35.3 分钟**（Table 1）。
- 在 MATH500 基准上，RAC 将剪枝模型准确率最高提升 **17%**，并在 50% 稀疏度下保留高达 **95%** 的密集模型准确率（Abstract, Section 1）。
- Token 级重建误差分析（Figure 2）表明，RAC 在解码阶段的重建误差显著低于 Prompt-Only 方法，验证了其对齐解码分布的有效性。

### 局限性与开放问题

- RAC 仅适用于单次剪枝（one-shot pruning），未探索结合微调或重训练的场景。
- 校准时需运行密集模型生成思维链，增加了校准阶段的计算开销，但论文指出其仍可在单张 H100 GPU 上完成。
- 结构化剪枝的推理加速依赖于特定硬件支持（如 NVIDIA 2:4 稀疏性），在通用硬件上提升有限。
- 如何显式优化以防止剪枝后模型生成序列长度增加（即避免“唠叨但低质量”输出）仍是一个开放方向。

## 核心模块与公式推导

### 问题形式化：层剪枝目标函数

标准的大语言模型层剪枝方法通过独立求解每一层的重建问题来寻找压缩权重。给定层 $\ell$ 的原始权重 $\mathbf{W}_\ell$ 和校准激活矩阵 $\mathbf{X}_\ell$，剪枝目标是在稀疏度约束下最小化输出激活的重建误差：

$$\min_{\widehat{\mathbf{W}}_\ell} \|\mathbf{W}_\ell \mathbf{X}_\ell - \widehat{\mathbf{W}}_\ell \mathbf{X}_\ell\|_2^2 \quad \text{s.t.} \quad \|\widehat{\mathbf{W}}_\ell\|_0 \leq S$$

其中 $\widehat{\mathbf{W}}_\ell$ 为剪枝后的权重矩阵，$S$ 为允许的非零权重数量上限。校准激活矩阵 $\mathbf{X}_\ell$ 由校准数据的隐藏状态堆叠而成：

$$\mathbf{X}_\ell = [\mathbf{x}_0^{(\ell-1)}, \mathbf{x}_1^{(\ell-1)}, \ldots, \mathbf{x}_{N-1}^{(\ell-1)}] \in \mathbb{R}^{d_\ell \times N}$$

**关键瓶颈**：标准剪枝方法在校准时仅使用提示词（prompt）的激活，即 $t \in \mathcal{P}_m$。然而推理模型以长思维链（CoT）为主导，解码阶段 token 数远大于提示词 token 数（$|\mathcal{D}_m| \gg |\mathcal{P}_m|$），导致校准分布与推理分布之间存在显著偏移。

### RAC 核心模块

RAC（Reasoning-Aware Compression）通过在校准阶段自回归生成思维链激活，将剪枝时的重建问题与推理时的解码分布对齐。其流程包含三个关键模块：

**模块一：提示词激活收集（Prompt Activation Collection）**

对每个校准样本 $m$，将提示词输入模型，收集各层的输入激活矩阵，对应 Algorithm 1 的第 3–4 行。

**模块二：解码阶段激活收集（Decode-time Activation Collection via On-policy Generation）**

在校准阶段，模型根据自身策略自回归生成思维链 token，并实时收集各层激活。解码阶段的采样过程为：

$$z_{t+1}^{(m)} \sim \pi_\theta(\cdot \mid z_{0:t}^{(m)}), \quad \pi_\theta(\cdot \mid z_{0:t}^{(m)}) = \mathrm{softmax}(W_{\mathrm{out}} \mathbf{x}_t^{(L,m)}), \quad t \in \mathcal{D}_m$$

其中 $\mathbf{x}_t^{(L,m)}$ 为模型最后一层的隐藏状态，$W_{\mathrm{out}}$ 为输出投影矩阵。采样得到的 token 立即作为下一时间步的输入，其嵌入经过所有 Transformer 层产生新的隐藏状态：

$$\mathbf{x}_{t+1}^{(0,m)} = E e_{z_{t+1}^{(m)}}, \quad \mathbf{x}_{t+1}^{(\ell,m)} = f_\ell(\{\mathbf{x}_{\tau}^{(\ell-1,m)}\}_{\tau \leq t+1}), \quad \ell = 1,\ldots,L$$

该模块的核心设计在于：模型使用自身预测的 token 作为后续输入（on-policy 生成），而非依赖外部固定轨迹，从而更准确地模拟推理时的解码分布。

**模块三：逐层剪枝（Layer-wise Pruning）**

将提示词激活与解码阶段激活拼接为完整的 RAC 校准矩阵 $\mathbf{X}_\ell^{\mathrm{RAC}}$，然后使用标准剪枝算法（如 SparseGPT、WANDA、ALPS）基于该矩阵进行逐层权重剪枝。RAC 的层校准损失为：

$$\lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{X}_\ell^{\mathrm{RAC}} \rVert_F^2 = \sum_{m=1}^{M} \sum_{t \in \mathcal{P}_m \cup \mathcal{D}_m} \lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{x}_t^{(\ell-1,m)} \rVert_2^2$$

该损失同时重建提示词阶段和解码阶段所有 token 的激活误差，将校准分布与推理分布对齐。

### 重建误差度量

为量化不同校准方法的效果，论文定义了 token 级别的重建误差：

$$e_t^{(\mathrm{meth})} = \| \mathbf{x}_{\mathrm{dense}, t}^{(L)} - \mathbf{x}_{\mathrm{meth}, t}^{(L)} \|_2$$

即给定 token $t$，剪枝模型与密集模型最后一层隐藏状态的 L2 距离。进一步定义误差比率 $r_t = e_t^{(\mathrm{Prompt})} / e_t^{(\mathrm{RAC})}$：当 $r_t > 1$ 时表示 RAC 的重建误差更低。图 2（Figure 2）的热图显示，在提示词阶段两种方法误差接近（灰色区域），但在更长的解码阶段 RAC 的误差显著低于 Prompt-Only 方法（蓝色区域占主导），验证了校准分布对齐的有效性。

## 实验与分析

### 核心瓶颈：剪枝破坏推理分布

标准大语言模型剪枝方法（如 **SparseGPT**，Frantar & Alistarh，ICML 2023）在剪枝校准时仅使用通用语料（C4）或提示词（Prompt）的输入激活进行重建。对于推理模型，这一策略存在根本性的分布偏移：推理任务的绝大部分计算发生在模型自回归生成的思维链（CoT）解码阶段，而校准时从未见过这些激活。如图1所示，直接用C4校准剪枝DeepSeek-R1-Distill-Qwen-7B，在30%-70%稀疏度下不仅准确率急剧下降，总推理时间反而膨胀——模型生成了冗长但低质量的序列。这一现象揭示了**校准分布与推理分布的不对齐**是推理模型剪枝失败的根本原因。

### 方法定位：RAC的分布对齐机制

**Reasoning-Aware Compression（RAC）** 的核心操作仅改变一个关键变量：剪枝校准时使用的激活矩阵。标准方法仅收集提示词激活 $\mathbf{X}_\ell^{\text{prompt}}$，而RAC在校准阶段让密集模型自回归生成思维链，同时收集所有解码步的隐藏状态，构建包含提示和解码两阶段激活的完整校准矩阵 $\mathbf{X}_\ell^{\text{RAC}}$。剪枝目标函数随之变为：

$$\lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{X}_\ell^{\mathrm{RAC}} \rVert_F^2 = \sum_{m=1}^{M} \sum_{t\in\mathcal{P}_m\cup\mathcal{D}_m} \lVert (\mathbf{W}_\ell - \widehat{\mathbf{W}}_\ell) \mathbf{x}_t^{(\ell-1,m)} \rVert_2^2$$

其中 $\mathcal{P}_m$ 为提示词token集，$\mathcal{D}_m$ 为模型自身策略（on-policy）生成的解码token集。由于推理任务中 $|\mathcal{D}_m| \gg |\mathcal{P}_m|$，RAC实质性地将剪枝重建目标从输入激活转向了推理时主导的解码激活，从而对齐了校准与推理的分布。该方法无需重新训练，可无缝集成至SparseGPT、**WANDA**（Sun et al., 2024）、**ALPS**（Meng et al., 2024）等现有剪枝算法中。

### 主实验结果

#### 数学推理基准（MATH500）

Table 1展示了DeepSeek-R1-Distill-Qwen系列在MATH500上的核心结果。以7B模型50%稀疏度为例：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/002_Table_1.jpg]]
*Table 1: DeepSeek-R1 Qwen MATH500 acc@1:1 under one-shot pruning. Accuracy with standard error (SE) on the left, total evaluation time in minutes on the right. Best accuracy or fastest runtime in green*

| 校准方法 | acc@1:1 | 推理时间（分钟） |
|---------|---------|----------------|
| C4 | 0.744 | 135.0 |
| Prompt-Only | 0.812 | 115.6 |
| **RAC** | **0.900** | **35.3** |

RAC相较C4校准提升15.6个百分点，相较Prompt-Only提升8.8个百分点，同时将推理时间从135分钟降至35分钟——这源于RAC剪枝模型生成的思维链更短且更高质量。在50%稀疏度下，RAC保留了密集模型约95%的准确率。

Table 2进一步验证了RAC在Qwen3系列上的泛化性。Qwen3-8B在50%稀疏度下，C4校准仅得0.564，Prompt-Only甚至降至0.470，而RAC达到0.862，分别提升29.8和39.2个百分点。值得注意的是，Prompt-Only在Qwen3上表现不如C4，说明仅用提示词激活校准可能引入额外的分布偏差，而RAC通过覆盖完整解码分布稳定地解决了这一问题。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/003_Table_2.jpg]]
*Table 2: Qwen3 MATH500 accuracy under one-shot pruning with SparseGPT. Accuracy with standard error (SE) on the left, total evaluation time in minutes on the right. Best accuracy or fastest runtime in green*

#### 编程基准（LiveCodeBench）

Table 5展示了代码生成任务上的结果。DeepSeek-R1-Distill-Qwen-7B在50%稀疏度下，RAC的pass@1:16达到0.710，远超C4的0.498和Prompt-Only的0.620。RAC在编程推理上同样显著优于基线，表明CoT重建策略对不同推理范式的通用性。

#### 竞赛级数学基准（AIME-25）

Table 4显示，Qwen3-14B在AIME-25上50%稀疏度时，RAC准确率达0.667，而C4仅0.267，Prompt-Only为0.533。在更困难的推理任务上，RAC的优势进一步放大——C4校准几乎使模型完全失效，而RAC保留了密集模型的大部分推理能力。

### 关键消融分析

#### Token级重建误差：解码阶段是核心战场

Figure 2通过token级重建误差比率热图揭示了RAC生效的精确机制。定义token $t$ 的重建误差为剪枝模型与密集模型最后一层隐藏状态的L2距离：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/007_Figure_2.jpg]]
*Figure 2: Tokenwise reconstruction error ratio on MATH500 test problems for pruned DeepSeek-R1-Distill-7B. Each row is a held-out problem, columns are token indices, and the black vertical line marks the prompt/decoding boundary. Colors show the ratio $r _ { t } = e _ { t } ^ { ( \mathrm { P r o m p t } ) } / e _ { t } ^ { ( \mathrm { R A C } ) }$ : grey ≈ 1 indicates equal error, red < 1 indicates lower error from prompt-only calibration, and blue > 1 indicates lower error from RAC. Prompt-only slightly outperforms on the input tokens, but RAC has smaller error throughout the much longer decode phase

$$e_t^{(\mathrm{meth})} = \| \mathbf{x}_{\mathrm{dense}, t}^{(L)} - \mathbf{x}_{\mathrm{meth}, t}^{(L)} \|_2$$

误差比率 $r_t = e_t^{(\mathrm{Prompt})} / e_t^{(\mathrm{RAC})}$ 表明：在提示词阶段（黑线左侧），$r_t < 1$（红色），Prompt-Only略优；但在更长的解码阶段（黑线右侧），$r_t > 1$（蓝色）占据主导，RAC的重建误差显著更低。这直接证实了RAC通过重建CoT激活来对齐解码分布的核心假设。

#### On-policy vs. Off-policy校准

Table 7对比了使用自身模型生成（on-policy）与使用更强模型（DeepSeek-R1-Distill-14B）生成（off-policy）的CoT进行校准。50%稀疏度下，on-policy RAC达到0.900，off-policy为0.876。on-policy校准的优势在高稀疏度下更为明显，表明**模型自身策略生成的激活分布**对于精确剪枝至关重要，使用外部模型生成的CoT无法完全替代。

#### 解码长度约束的影响

Table 8展示了限制最大解码token数的影响。当测试时解码预算限制为4096 tokens时，RAC 40%稀疏度模型的准确率（0.836）甚至超过了密集模型（0.824），且推理时间相近（10.4 vs 10.5分钟）。这表明RAC剪枝模型在受限解码场景下具有更强的效率-准确率权衡优势。同时，随着解码预算收紧，C4和Prompt-Only校准导致的推理时间膨胀问题也自然缓解，进一步凸显了RAC在生成质量控制上的价值。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/010_Table_8.jpg]]
*Table 8: MATH500 accuracy and runtime (minutes) across different test-time maximum decode budgets (number of tokens) for 7B models*

#### 剪枝算法兼容性

Table 9和Table 10验证了RAC与不同剪枝算法的兼容性。在Qwen3-8B 50%稀疏度下，ALPS+RAC达到0.940准确率，WANDA+RAC达到0.932，均显著优于各自的C4基线。在AIME-25上，ALPS+RAC在Qwen3-14B 50%稀疏度下达到0.667，远超C4的0.267。RAC作为一个校准数据层面的改进，与底层剪枝算法正交，可即插即用。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/012_Table_10.jpg]]
*Table 10: Qwen3 AIME-25 accuracy under one-shot pruning with ALPS. Accuracy with standard error (SE) in parentheses. Best accuracy in each row in green*

#### 结构化剪枝与量化

Table 6展示了半结构化2:4稀疏性结合FP8量化的吞吐量分析。在DeepSeek-R1-Distill-14B上，RAC+FP8全模型剪枝达到1823 tok/s的吞吐量，较密集模型（1426 tok/s）提升28%，同时保持0.940的准确率。这证明了RAC在实用部署场景下的价值——不仅保持准确率，还能在支持稀疏计算的硬件上实现实际加速。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_tyGfwG6xTh/figures/008_Table_6.jpg]]
*Table 6: Actual throughput gains and accuracy with semi-structured 2:4 sparsity of MLP layers. Pruned model is Deepseek-R1-Distill-14B on MATH-500. Each pruning scope has two columns: Accuracy (acc@1:1 (SE)) and throughput (tok/s). Dense baseline throughput = 1426 tok/s*

### 失败模式与局限性

尽管RAC在多数场景下表现优异，但分析中仍存在若干值得注意的局限：

1. **低稀疏度下的边际收益递减**：在20%-30%稀疏度下，RAC与Prompt-Only的差距缩小。例如DeepSeek-R1-Distill-7B在20%稀疏度时，RAC为0.934，Prompt-Only为0.930。当剪枝比例较低时，模型容错空间较大，分布对齐的收益相对有限。

2. **小模型的极端稀疏崩溃**：DeepSeek-R1-Distill-1.5B在50%稀疏度下，即使RAC也仅达到0.664，密集模型为0.832。小参数量的推理模型在高稀疏度下仍存在显著的容量瓶颈，RAC无法完全弥补参数减少带来的能力损失。

3. **校准计算开销**：RAC需要运行密集模型生成思维链以收集激活，增加了校准阶段的计算成本。论文指出这仍可在单张H100 GPU上完成，但对于更大规模模型（如671B DeepSeek-R1），这一开销可能成为瓶颈——而论文未在如此规模的模型上验证。

4. **序列长度膨胀的隐性风险**：虽然RAC大幅缓解了C4校准导致的推理时间膨胀，但在部分场景下，剪枝模型仍倾向于生成更长的思维链。论文明确指出“设计显式优化以防止剪枝后模型生成序列长度增加”仍是一个开放方向。

5. **结构化剪枝的硬件依赖**：Table 6中的吞吐量提升依赖于NVIDIA 2:4稀疏性等特定硬件支持，在通用硬件上加速效果有限。

### 开放问题

* RAC能否与量化、知识蒸馏等压缩技术协同，实现更高效的推理模型部署？
* 在更复杂的多步逻辑推理、程序合成等任务上，RAC的性能保持能力如何？
* 如何设计显式的正则化或训练目标，防止剪枝模型生成冗余的长思维链？

## 方法谱系与知识库定位

### 1. 方法在剪枝谱系中的定位

RAC（Reasoning-Aware Compression）的核心贡献在于**重新定义了剪枝校准阶段的激活分布**，而非提出新的剪枝算法本身。它属于**校准数据增强**范式，与现有的一次性（one-shot）剪枝算法是正交的、可插拔的关系。论文明确验证了RAC与以下三种主流剪枝算法的兼容性：

- **SparseGPT**（Frantar & Alistarh, ICML 2023）：作为主要实验载体，RAC在SparseGPT框架下仅替换校准数据即可实现显著提升。
- **WANDA**（Sun et al., 2024）：在Qwen-3系列模型上，RAC+WANDA同样展现出优于C4和Prompt-Only校准的性能（Table 9）。
- **ALPS**（Meng et al., 2024）：在Qwen3-8B 50%稀疏度下，ALPS+RAC达到0.940准确率；在AIME-25基准上，Qwen3-14B的ALPS+RAC准确率达0.667，远超C4校准的0.267（Table 10）。

这种“校准插件”式的设计使RAC的方法学贡献清晰：**它不改变剪枝算法的数学形式，而是将层剪枝目标函数**
$$
\min_{\widehat{\mathbf{W}}_\ell} \|\mathbf{W}_\ell \mathbf{X}_\ell - \widehat{\mathbf{W}}_\ell \mathbf{X}_\ell\|_2^2 \ \text{s.t.} \|\widehat{\mathbf{W}}_\ell\|_0 \leq S
$$
**中的校准激活矩阵 $\mathbf{X}_\ell$ 从仅含提示词激活扩展为同时包含提示词和模型自生成的思维链（CoT）激活**，即 $\mathbf{X}_\ell^{\mathrm{RAC}}$。

### 2. 与相关工作的关系

**相对于标准LLM剪枝**：现有方法（如SparseGPT、WANDA）默认使用通用语料（如C4）或仅输入提示词进行校准。这类方法隐含假设校准分布与推理分布一致，但推理模型以长思维链为主导解码阶段，导致严重的分布偏移。RAC通过**在策略（on-policy）生成**收集CoT激活，首次将校准分布与推理时的解码分布对齐。

**相对于Prompt-Only校准**：Prompt-Only是RAC的直接前身——它使用任务提示词的激活进行校准，但忽略了占绝对token多数的解码阶段。Figure 2的token级重建误差热图提供了因果证据：Prompt-Only在输入token上误差略低（红色区域），但在解码阶段（黑色垂直线右侧）RAC的重建误差显著更小（蓝色区域），且解码阶段token数量远超输入阶段，因此RAC在整体上实现了更低的误差累积。

**相对于Off-policy校准**：Table 7的消融实验表明，使用同一模型自生成的CoT（on-policy）优于使用其他模型（如DeepSeek-R1-Distill-14B）生成的CoT（off-policy），在50%稀疏度下准确率分别为0.900 vs 0.876。这验证了**策略一致性**对校准质量的关键影响。

### 3. 适用边界与局限

RAC的设计和验证存在以下明确边界：

1. **仅限于一次性剪枝**：论文未探索RAC与微调、重训练或迭代剪枝的结合。校准阶段需要运行密集模型生成CoT，增加了计算开销（但论文指出可在单张H100 GPU上完成）。

2. **结构化剪枝的硬件依赖**：Table 6展示了半结构化2:4稀疏性下的吞吐量提升（RAC+FP8全模型剪枝达1823 tok/s，较密集模型提升28%），但此类加速依赖于NVIDIA的专用稀疏计算单元，在通用硬件上提升有限。

3. **模型规模验证范围**：实验覆盖DeepSeek-R1蒸馏版本（1.5B–70B）和Qwen3系列（1.7B–14B），但未在更大规模模型（如671B原始DeepSeek-R1）上验证，公开可用的仅为其蒸馏版本。此点需要读者自行评估在更大模型上的泛化性。

4. **任务类型覆盖**：主要验证集中在数学推理（MATH500、AIME-25）和代码生成（LiveCodeBench），未涉及多步逻辑推理、程序合成等更复杂场景。

### 4. 开放问题

论文和当前分析揭示以下开放方向：

1. **序列长度膨胀问题**：Table 8显示，在无token预算限制时，RAC剪枝模型倾向于生成更长的序列（这解释了C4/Prompt-Only剪枝模型运行时间反而增加的异常现象）。限制解码长度至4096 tokens时，RAC 40%稀疏度模型的准确率甚至超过密集模型（0.836 vs 0.824）。如何设计压缩方法以**显式优化避免生成长度增加**，而非依赖后验截断，仍是一个开放问题。

2. **与其他压缩技术的协同**：RAC能否与量化、知识蒸馏等方法联合使用，实现更高效的推理模型部署，论文未做探索。Table 6中RAC+FP8的初步结果暗示了这种协同的潜力。

3. **更复杂推理任务的保持能力**：在多步逻辑推理、定理证明、程序合成等需要更长、更复杂CoT的任务上，RAC的性能保持能力如何，尚待验证。

4. **校准效率优化**：当前RAC需要为每个待剪枝模型单独运行密集模型生成CoT。是否可以通过跨模型迁移（如Table 7的off-policy设置）或更高效的采样策略降低校准成本，值得进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Reasoning_Models_Can_be_Accurately_Pruned_Via_Chain_of_Thought_Reconstruction.pdf]]
