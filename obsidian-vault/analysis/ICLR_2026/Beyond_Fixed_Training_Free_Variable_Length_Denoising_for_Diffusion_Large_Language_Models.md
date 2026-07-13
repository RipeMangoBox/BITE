---
title: "Beyond Fixed: Training-Free Variable-Length Denoising for Diffusion Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Fixed_Training_Free_Variable_Length_Denoising_for_Diffusion_Large_Language_Models.pdf
project_link: null
code_link: https://github.com/Li-Jinsong/DAEDAL
openreview_forum_id: Ic2A2gCseC
aliases:
- BFTFVLDDLLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "模型在预测末尾EOS（序列结束）令牌时的置信度。该置信度能够作为全局长度是否充足的内部信号：高置信度表示当前长度足够，低置信度表示需要更多空间。"
primary_logic: "DLLM内部具有对任务所需生成长度的感知能力（体现为EOS令牌的预测置信度），在无需重新训练的情况下，通过监控这一信号并动态插入掩码令牌即可实现推理时的自适应长度扩展，从而突破固定长度的限制。"
claims:
- "EOS置信度与长度充足性呈正相关：在长度充足的问题上模型对EOS的预测置信度更高。"
- "DAEDAL 在统一初始长度（64）下，在四个基准上均达到或超越最佳固定长度基线的性能，且提高了有效令牌比率。"
- "两阶段设计（初始长度调整+迭代掩码插入）协同作用，单个阶段已带来显著提升，组合后效果最佳。"
- "DAEDAL 对超参数（初始长度、扩展因子、窗口大小、阈值）具有很强的鲁棒性，所有测试配置均与最佳基线可比或更优。"
---

# Beyond Fixed: Training-Free Variable-Length Denoising for Diffusion Large Language Models

> [!tip] 核心洞察
> DLLM内部具有对任务所需生成长度的感知能力（体现为EOS令牌的预测置信度），在无需重新训练的情况下，通过监控这一信号并动态插入掩码令牌即可实现推理时的自适应长度扩展，从而突破固定长度的限制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越固定长度：扩散大语言模型的无训练可变长度去噪 |
| 英文题名 | Beyond Fixed: Training-Free Variable-Length Denoising for Diffusion Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Ic2A2gCseC) · [GitHub](https://github.com/Li-Jinsong/DAEDAL) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DAEDAL |
| Dataset | GSM8K, MATH500, MBPP, HumanEval |

> [!tip] 效果简介
> - GSM8K 上，Acc (%) 为 85.8，对比 83.8 (best fixed-length at 1024)，变化 +2.0。
> - MATH500 上，Acc (%) 为 44.2，对比 39.6 (best fixed-length at 2048)，变化 +4.6。
> - MBPP 上，Acc (%) 为 40.8，对比 38.8 (best fixed-length at 2048)，变化 +2.0。

## 概要

扩散大语言模型（DLLM）在推理时要求**预先定义固定的生成长度**，这一约束带来了根本性的效率与性能矛盾：长度设置过短会导致模型无法充分展开推理，性能不足；长度设置过长则造成大量计算浪费，甚至可能因过度扩展而引发性能退化。现有方法（如 **LLaDA**，Nie et al., 2025）需要针对每个任务和基准手工调优生成长度，缺乏自适应能力。

本文揭示了 DLLM 内部存在一个关键信号——**序列末尾 EOS 令牌的预测置信度**——能够反映当前生成长度是否充足：当长度足够时，模型对 EOS 的预测置信度显著更高（Figure 2, Figure 6）。基于这一发现，论文提出 **DAEDAL**，一种**无需训练的、两阶段可变长度去噪策略**，使 DLLM 能够根据每个问题的复杂度动态调整生成长度。

DAEDAL 从统一的短初始长度（64）出发：**阶段一**通过监控 EOS 置信度循环扩展序列长度，直至达到任务所需的粗粒度长度；**阶段二**在去噪过程中识别低置信度的掩码位置，动态插入额外掩码令牌以扩展局部生成空间。两阶段协同作用，使模型在保持高性能的同时显著提升计算效率。

在四个基准测试（GSM8K、MATH500、MBPP、HumanEval）上，DAEDAL 以统一的初始长度达到或超越了经过精心调优的固定长度基线的最佳性能——平均准确率从 52.05% 提升至 54.75%（LLaDA-Instruct-8B），同时有效令牌比率大幅提高。该方法对超参数（初始长度、扩展因子、窗口大小、阈值）表现出极强的鲁棒性，所有测试配置均与最佳基线持平或更优。



扩散大语言模型（Diffusion Large Language Models, DLLMs）作为自回归模型之外的一条新兴生成范式，通过迭代去噪从完全掩码的序列中逐步恢复文本。然而，现有 DLLM 的推理过程存在一个根本性限制：**生成长度必须在去噪开始前预先固定**。这意味着无论面对简单的一步推理题还是需要长篇推导的复杂数学证明，模型都被强制在相同的令牌预算内完成生成。

这一固定长度策略带来了两个层面的问题。**性能层面**，当预设长度不足时，模型缺乏足够的生成空间来完成复杂推理，导致答案截断或推理链不完整；而当长度过长时，多余的掩码令牌会被强制去噪为无意义的填充内容，不仅浪费计算资源，还可能引入噪声干扰模型的预测质量。**效率层面**，为覆盖数据集中最困难的问题，固定长度通常需要设置为较大的值（如 1024 或 2048），这导致大量简单问题也被分配了远超实际所需的计算预算，造成显著的资源浪费。

本文的核心发现是：**DLLM 内部天然具有对任务所需生成长度的感知能力**。具体而言，模型在序列末尾对 EOS（序列结束）令牌的预测置信度，能够作为长度是否充足的可靠内部信号——当生成空间足够时，模型对 EOS 的预测置信度显著更高；当空间不足时，该置信度明显降低。这一发现为无需重新训练的自适应长度调整提供了关键的因果操作变量。

基于上述洞察，本文提出 **DAEDAL**，一个完全无需训练、在推理时动态调整生成长度的两阶段框架。DAEDAL 从统一的短初始长度出发，通过监控 EOS 置信度信号，自适应地为每个问题分配合适的生成空间，从而突破固定长度去噪的根本瓶颈。



## 核心方法与创新机理

扩散大语言模型（DLLM）在推理时面临一个根本性约束：生成序列的长度必须在去噪过程开始前预先固定。这一设计导致了一个尖锐的效率-性能权衡——长度过短时模型缺乏足够的推理空间，性能不足；长度过长时则造成大量计算浪费，甚至引发性能退化。DAEDAL 的核心创新在于**首次揭示了 DLLM 内部存在对任务所需生成长度的感知能力，并将其转化为一个无需重新训练的自适应长度控制机制**，从根本上突破了固定长度推理的瓶颈。

### 关键发现：EOS 置信度作为长度充足性的内部信号

DAEDAL 的核心洞察是：模型在预测序列末尾 EOS（End-of-Sequence）令牌时的置信度，能够作为当前生成长度是否充足的可靠内部信号。当给定的生成长度足以容纳完整推理过程时，模型对末尾位置应生成 EOS 的预测置信度较高；反之，当长度不足时，模型因缺乏足够空间而表现出较低的 EOS 置信度。这一发现通过热力图实验得到验证（Figure 2, Figure 6）：在长度充足的问题上，序列末尾的平均 EOS 置信度显著高于长度不足的问题，热力图中占主导的绿色区域（差值 > 0）直接证实了这一正相关关系。

### 方法创新：从固定长度到两阶段自适应扩展

基于上述洞察，DAEDAL 将传统的“固定长度一次去噪”范式重构为**两阶段自适应推理管线**，在无需任何重新训练的前提下实现了推理时的动态长度调整。

**阶段一：初始长度调整（Initial Length Adjustment）**。在去噪过程开始前，DAEDAL 从一个较短的初始长度（默认 64 个令牌）出发，通过评估序列末尾固定窗口内 EOS 令牌的平均预测置信度来判断当前长度是否充足。若置信度低于阈值 $\tau_{eos}$，则向序列末尾追加额外的 [MASK] 令牌以扩展生成长度，并循环重复此过程，直至 EOS 置信度超过阈值或达到预设的长度上限。这一阶段为每个问题粗略地分配一个任务适配的生成长度，避免了“一刀切”式的长度预设。

**阶段二：迭代掩码插入（Iterative Mask Insertion）**。在去噪过程的每一步，DAEDAL 识别出低置信度的掩码位置，并动态地将单个 [MASK] 令牌替换为一组多个 [MASK] 令牌，从而为复杂推理步骤提供局部扩展的额外空间。这一机制使得模型能够在去噪过程中按需“挤出”更多推理空间，而非受限于初始分配的长度。

### 与基线方法的本质差异

相较于原始 LLaDA（Nie et al., 2025）的固定长度推理，DAEDAL 在两个关键维度上实现了范式转变：

| 维度 | LLaDA 固定长度推理 | DAEDAL |
|------|---------------------|--------|
| **生成长度策略** | 所有问题使用同一预设长度 $L$，需针对每个基准单独调优 | 从短初始长度出发，根据 EOS 置信度自适应扩展，统一初始长度适用于所有基准 |
| **推理管线** | 单次完整前向去噪，从完全掩码的固定长度序列开始，无长度调整 | 两阶段管线：去噪前的长度估计循环 + 去噪过程中的动态掩码插入 |

这一设计使得 DAEDAL 能够在保持统一初始长度（64）的前提下，在四个基准上均达到或超越经过精心调优的固定长度基线的最佳性能，同时显著提升了有效令牌比率（Table 1）。更重要的是，两阶段设计具有协同效应：单独使用阶段一或阶段二均已带来显著提升，而二者结合后效果最佳（Table 2），验证了“全局长度估计 + 局部空间扩展”这一组合策略的有效性。



![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/007_Figure_3.jpg]]
*Figure 3: Inference process of Fixed-Length Denoising (Baseline) and DAEDAL. (a) The standard inference process for current DLLMs, which performs iterative denoising on a sequence of a predefined, static length. (b) Our proposed two-stage inference process, which first employs Initial Length Adjustment to determine an appropriate generation length before denoising, followed by Iterative Mask Insertion to expand the sequence on-demand during the denoising process*

DAEDAL 是一种无需额外训练的两阶段可变长度去噪策略，旨在解决扩散大语言模型（DLLM）在推理时因固定生成长度带来的性能与效率矛盾。其核心洞察在于：模型在序列末尾对 EOS（序列结束）令牌的预测置信度能够作为内部信号，指示当前生成长度是否充足——高置信度意味着长度足够，低置信度则提示需要更多生成空间。DAEDAL 利用这一信号，在不修改模型权重的前提下，实现了从固定长度到动态自适应长度的推理范式转换。

整个推理管线由两个协同阶段构成，如 Figure 3(b) 所示：

**阶段一：初始长度调整（Initial Length Adjustment）**。在去噪过程开始之前，DAEDAL 从一个较短的初始长度（默认 $L_{init}=64$）出发，循环评估序列末尾固定窗口内 EOS 令牌的平均预测置信度。若该置信度低于预设阈值 $\tau_{eos}$（默认 0.5），则判定当前长度不足，在序列末尾追加额外的 `[MASK]` 令牌以扩展生成空间。这一“评估—扩展”循环持续进行，直至 EOS 置信度超过阈值或达到最大长度上限 $L_{max}$（默认 2048）。该阶段为每个任务粗略分配一个任务适配的全局长度，避免了固定长度下“一刀切”的低效问题。

**阶段二：迭代掩码插入（Iterative Mask Insertion）**。在阶段一确定的长度基础上，进入标准的迭代去噪流程。与固定长度去噪不同的是，DAEDAL 在每一步去噪中动态监控各位置的置信度：对于置信度低于 $\tau_{low}$ 的掩码位置，判定其生成空间不足，将该位置的单个 `[MASK]` 令牌扩展为由多个 `[MASK]` 令牌组成的块（扩展因子 $E_{factor}$ 默认为 8）；对于置信度高于 $\tau_{high}$ 的位置，则直接进行令牌填充。这一机制为复杂推理步骤提供了局部扩展能力，使模型能够在需要的地方获得额外计算空间，而在简单位置保持紧凑。

两个阶段的协同关系在消融实验中得到验证（Table 2）：单独使用阶段一（初始长度 64）即可在 GSM8K 上达到 84.1% 的准确率，显著优于同长度固定基线；单独使用阶段二虽能在短初始长度下大幅提升性能（72.3%），但因缺乏全局长度规划而未能达到峰值；完整 DAEDAL 将两者结合，最终达到 85.8% 的最高准确率，证明了全局长度估计与局部空间扩展的互补性。

整个流程对超参数表现出极强的鲁棒性。在统一使用 $L_{init}=64$、$L_{max}=2048$、$\tau_{eos}=0.5$、$\tau_{high}=0.9$、$\tau_{low}=0.1$、$\tau_{expand}=0.9$、$E_{factor}=8$、$W_{eos}=32$ 的默认配置下，DAEDAL 在四个基准上均达到或超越各自精心调优的固定长度基线的最佳性能（Figure 1(a)），同时产生了按问题自适应的响应长度分布（Figure 1(b)），有效提升了有效令牌比率。



DAEDAL 是一种训练无关的双阶段可变长度去噪策略，其核心在于将扩散大语言模型（DLLM）内部对生成长度的感知能力转化为可操作的推理时控制信号。该方法包含三个关键模块：**EOS 置信度计算**、**阶段一：初始长度调整**、**阶段二：迭代掩码插入**。

### EOS 置信度计算

DAEDAL 的核心洞察是：模型在序列末尾对 EOS（End-of-Sequence）令牌的预测置信度可以作为“生成长度是否充足”的内部信号。当当前长度足以容纳完整推理时，模型对 EOS 的预测置信度更高；反之则较低。这一现象在 Figure 2 的热力图中得到验证：长度充足的问题在序列末端展现出更高的 EOS 置信度（绿色区域表示差异 > 0）。

具体实现上，EOS 置信度的计算聚焦于序列末尾的一个固定窗口 $W_{eos}$（默认值为 32），计算该窗口内模型对 EOS 令牌的平均预测置信度。这一设计避免了仅依赖单个位置可能引入的噪声，同时保持了计算的高效性。

### 阶段一：初始长度调整

阶段一在去噪过程开始前执行，目标是快速确定一个粗粒度的任务适配长度。其工作流程如下：

1. **起始状态**：从一个较短的初始长度 $L_{init}$（默认 64）开始，序列全部由 `[MASK]` 令牌填充。
2. **长度评估**：执行一次完整的前向预测，调用 `ComputeEOSConfidence` 计算序列末尾窗口内的平均 EOS 置信度。
3. **循环扩展**：若 EOS 置信度低于阈值 $\tau_{eos}$（默认 0.5），则在序列末尾追加额外的 `[MASK]` 令牌以扩展生成长度。扩展的步长由当前长度和扩展因子 $E_{factor}$（默认 8）共同决定。
4. **终止条件**：当 EOS 置信度超过 $\tau_{eos}$ 或达到最大长度上限 $L_{max}$（默认 2048）时，循环终止。

这一阶段本质上是一个基于模型内部信号的贪心搜索过程，无需任何外部监督或训练。

### 阶段二：迭代掩码插入

阶段二在去噪过程中动态执行，旨在为复杂推理步骤提供额外的局部生成空间。其核心操作是在去噪的每一步中识别“低置信度”的掩码位置，并将其扩展为多个掩码令牌。

具体而言，在每个去噪步骤中：
- 对于序列中的每个 `[MASK]` 位置，模型预测其令牌分布并计算置信度。
- 若某位置的置信度低于低置信度阈值 $\tau_{low}$（默认 0.1），则将其标记为需要扩展的位置。
- 对于标记为扩展的位置，**动态地将单个 `[MASK]` 令牌替换为由 $E_{factor}$ 个 `[MASK]` 令牌组成的块**（Figure 3b 示意了此过程）。

这一机制使得模型能够在推理过程中按需“拉伸”序列，为需要更多推理步骤的区域提供额外空间。与之配合的是，高置信度位置（置信度超过 $\tau_{high}$，默认 0.9）会直接填充为预测令牌，类似于自信解码策略。

### 两阶段协同

两阶段的设计是互补的：阶段一提供全局性的长度规划，确保序列整体长度适配任务复杂度；阶段二提供局部性的动态调整，在去噪过程中按需扩展特定区域。消融实验（Table 2）证实，完整 DAEDAL（两阶段联合）在 GSM8K 上达到 85.8% 准确率，优于单独使用阶段一的 84.1% 和阶段二的 72.3%（初始长度 64 时），验证了两阶段的协同效应。

### 关键超参数

DAEDAL 涉及的核心超参数及其默认值如下：

| 参数 | 符号 | 默认值 | 含义 |
|------|------|--------|------|
| 初始长度 | $L_{init}$ | 64 | 阶段一的起始生成长度 |
| 最大长度 | $L_{max}$ | 2048 | 允许的最大生成长度 |
| EOS 置信度阈值 | $\tau_{eos}$ | 0.5 | 阶段一长度充足性的判断阈值 |
| 高置信度阈值 | $\tau_{high}$ | 0.9 | 阶段二中直接填充令牌的置信度门槛 |
| 低置信度阈值 | $\tau_{low}$ | 0.1 | 阶段二中触发掩码扩展的置信度门槛 |
| 扩展置信度阈值 | $\tau_{expand}$ | 0.9 | 控制扩展决策的辅助阈值 |
| 扩展因子 | $E_{factor}$ | 8 | 每次扩展时插入的掩码令牌数量 |
| EOS 置信度窗口 | $W_{eos}$ | 32 | 计算 EOS 置信度时考虑的序列末尾窗口大小 |

值得注意的是，DAEDAL 在所有实验和模型中使用完全相同的超参数配置，未针对特定模型或基准进行调优。消融实验（Table 3、Table 4、Figure 5）表明，该方法对上述超参数具有极强的鲁棒性：在初始长度 32 至 512、扩展因子 8 至 32、以及 32 种阈值组合的测试中，性能均与最佳固定长度基线持平或更优。



## 实验与关键发现

### 核心发现：EOS置信度作为长度充足性的内部信号

DAEDAL 的设计根植于一个关键发现：扩散大语言模型（DLLM）内部天然具有对生成长度是否充足的感知能力。具体而言，模型在序列末尾预测 EOS（序列结束）令牌的置信度，能够作为当前令牌空间是否足够的可靠信号。

图2通过热力图直观验证了这一发现。在 GSM8K 和 MATH500 两个基准上，研究者将问题分为“长度充足”和“长度不足”两组，测量了模型在完全掩码的128令牌输入上首次预测时末尾EOS令牌的平均置信度差异。热力图呈现大面积绿色（差异>0），表明在长度充足的问题上，模型对EOS的预测置信度系统性更高。这一因果机制构成了DAEDAL无需训练即可实现自适应长度扩展的理论基础：高EOS置信度意味着当前空间足够，低置信度则发出需要更多令牌空间的信号。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/006_Figure_2.jpg]]
*Figure 2: Visualization of the DLLM’s awareness of length sufficiency. The heatmaps show the difference in average EOS token confidence at the sequence terminus, measured after the first prediction on a fully masked 128-token input. This difference is the result of subtracting the average confidence on length-insufficient problems (those answered correctly only with a much longer sequence) from that on length-sufficient problems (those answered correctly under 128 tokens). The experiment is conducted with LLaDA-Instruct-8B. The predominantly green color (difference > 0) indicates that EOS confidence is higher for length-sufficient problems, validating our core insight*

### 主实验结果：统一初始长度下的性能超越

表1展示了DAEDAL在LLaDA-Instruct-8B模型上的主实验结果。DAEDAL采用统一的短初始长度（$L_{init}=64$），在所有四个基准上均达到或超越了需要逐任务精细调优的固定长度基线的最佳性能：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/008_Table_1.jpg]]
*Table 1: Main Results of DAEDAL on LLaDA-Instruct-8B. We compare the baseline performance at various generation lengths (64 to 2048) against DAEDAL. Acc denotes accuracy, $E _ { t o k e n }$ is the average effective tokens (the response length excluding trailing padding), $N _ { t o k e n }$ is the average total tokens, and $\mathbf { E } _ { r a t i o }$ is the effective token ratio. The best configuration for the baseline is highlighted in orange. The best results are bold and underlined, and the second-best results are underlined*

- **GSM8K**：DAEDAL 达到 85.8% 准确率，超越最佳固定长度基线（1024长度下83.8%）**+2.0个百分点**。
- **MATH500**：DAEDAL 达到 44.2%，超越最佳固定长度基线（2048长度下39.6%）**+4.6个百分点**，提升幅度最大。
- **MBPP**：DAEDAL 达到 40.8%，超越最佳固定长度基线（2048长度下38.8%）**+2.0个百分点**。
- **HumanEval**：DAEDAL 达到 48.2%，略超最佳固定长度基线（1024长度下47.6%）**+0.6个百分点**。

四个基准的平均准确率上，DAEDAL 以 54.75% 对 52.05% 的优势显著领先。更为关键的是，DAEDAL在性能提升的同时大幅改善了计算效率：有效令牌比率（$E_{ratio}$，即去除末尾EOS填充后的净响应长度占总生成长度的比例）达到64.3%，而固定长度基线在长序列配置下有效令牌比率严重偏低——例如在2048长度下，大量令牌被浪费为无意义的填充。

图4从另一个维度揭示了DAEDAL的自适应特性。固定长度基线对所有问题分配相同的1024令牌空间（蓝色柱状图），而DAEDAL（橙色柱状图）根据每个问题的实际复杂度动态分配长度，生成长度呈现出从256到1024+的多样化分布。这种“按需分配”的机制是DAEDAL在短初始长度下仍能超越长序列固定基线的根本原因。

### 消融实验：两阶段设计的协同效应

表2对DAEDAL的两阶段设计进行了拆解分析。在GSM8K上：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/013_Table_2.jpg]]
*Table 2: Ablation Results of DAEDAL’s Two Stages. Experiments are conducted on GSM8K with LLaDA-Instruct-8B. We compare the performance of the full DAEDAL method, as well as its individual stages (Stage 1 and Stage 2), against the baseline. The baseline is evaluated at multiple fixed lengths, with its best configuration highlighted in orange. Stage 1 and DAEDAL evaluated with an initial length of 64, while Stage 2 is evaluated with varying initial lengths (64, 128, 256)*

- **仅阶段一（初始长度调整）**：从初始长度64开始，准确率达到84.1%，已显著优于同长度固定基线（72.3%），但仍略低于最佳固定长度基线（83.8%）。
- **仅阶段二（迭代掩码插入）**：从初始长度64开始，准确率为72.3%——虽然远超同长度基线，但因初始长度过短限制了全局规划空间，未能达到最佳固定长度基线的峰值性能。
- **完整DAEDAL（两阶段联合）**：准确率达到85.8%，超越所有单独阶段和所有固定长度配置。

这一结果揭示了两个阶段的互补关系：阶段一提供粗粒度的全局长度估计，为后续去噪过程划定合理的操作空间；阶段二在去噪过程中进行细粒度的局部空间扩展，处理复杂推理步骤中突发的令牌需求。单独使用任一阶段均无法达到完整方法的性能上限。

### 超参数鲁棒性分析

DAEDAL展现出对关键超参数的高度鲁棒性，这一特性对其实际部署至关重要。

**初始长度不敏感性**（表3）：在GSM8K上，初始长度从32到512变化时，准确率保持在84.1%-85.8%的狭窄区间内；在HumanEval上，准确率在所有设定下完全一致（48.2%）。这表明用户无需针对不同任务调整初始长度，使用统一的短初始长度（默认64）即可获得稳定性能。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/014_Table_3.jpg]]
*Table 3: Ablation Results on DAEDAL’s Initial Length. Experiments are conducted on GSM8K and HUMANEVAL using LLaDA-Instruct-8B. DAEDAL is evaluated with initial lengths ranging from 32 to 512. We highlight our default setting ( L _ { i n i t } = 6 4 ) in blue*

**扩展因子与EOS窗口大小**（表4）：扩展因子（$E_{factor}$，控制每次插入的掩码令牌数量）从8到32变化时，性能保持稳定，默认值8即取得最优效果（85.8%）。EOS置信度窗口大小（$W_{eos}$）在较大范围内表现稳健，仅在窗口过小（如4）时出现性能退化——这是因为过小的窗口无法稳定估计EOS置信度，导致长度调整决策出现噪声。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/015_Table_4.jpg]]
*Table 4: Ablation Results on DAEDAL’s Expansion Factor and EOS Confidence Window Size. Both ablation studies are conducted on GSM8K using LLaDA-Instruct-8B. The left panel shows results for varying $E _ { f a c t o r }$ ranging from 8 to 32, and the right panel for varying $W _ { e o s }$ ranging from 8 to 32. We highlight our default setting ( $E _ { f a c t o r }$ = 8 and $\breve { W } _ { e o s }$ = 3 2 ) in blue*

**阈值组合的网格搜索**（图5）：研究者对两组相互依赖的阈值对——($\tau_{high}$, $\tau_{low}$) 和 ($\tau_{eos}$, $\tau_{expand}$)——进行了4×4网格搜索，共32种配置。所有32种配置的性能均与最佳固定长度基线（83.8%准确率）持平或更优，部分配置超越基线。默认阈值设置（$\tau_{eos}=0.5$, $\tau_{expand}=0.9$, $\tau_{high}=0.9$, $\tau_{low}=0.1$）在所有基准上均表现优异，且未针对特定模型或任务进行调优。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/017_Figure_5.jpg]]
*Figure 5: Ablation Results on DAEDAL’s Thresholds. The two 4x4 heatmaps present a grid search over two interdependent threshold pairs: ( $\tau _ { h i g h } , \tau _ { l o w }$ ) and ( $\tau _ { e o s } , \tau _ { e x p a n d }$ ) . All 32 configurations were evaluated on GSM8K using LLaDA-Instruct-8B. Higher accuracy is indicated by a darker green. The color bar also provides reference color for performance of baseline. Our default settings are in blue boxes. The results demonstrate remarkable stability, with all configurations comparable to the best-performing baseline, and some even outperforming it

### 跨模型泛化验证

DAEDAL的通用性在两个额外模型上得到验证。在LLaDA-1.5-8B（表5）和Dream-Instruct-7B（表6）上，DAEDAL同样使用统一的短初始长度（64）和完全相同的超参数设置，在所有四个基准上均达到或接近最佳固定长度基线的性能，同时保持显著更高的有效令牌比率。这一跨模型的一致性表明，EOS置信度作为长度充足性信号的机制是DLLM的普遍特性，而非特定模型的偶然现象。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/016_Table_5.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/018_Table_5.jpg]]
*Table 5: Main Results of DAEDAL on LLaDA-1.5-8B. We compare the baseline performance at various generation lengths (64 to 2048) against DAEDAL. Acc denotes accuracy, $E _ { t o k e n }$ is the average effective tokens (the response length excluding trailing padding), $N _ { t o k e n }$ is the average total tokens, and $\mathbf { E } _ { r a t i o }$ is the effective token ratio. The best configuration for the baseline is highlighted in orange. The best results are bold and underlined, and the second-best results are underlined*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/019_Table_6.jpg]]
*Table 6: Main Results of DAEDAL on Dream-Instruct-7B. We compare the baseline performance at various generation lengths (64 to 2048) against DAEDAL. Acc denotes accuracy, $E _ { t o k e n }$ is the average effective tokens (the response length excluding trailing padding), $N _ { t o k e n }$ is the average total tokens, and $\mathbf { E } _ { r a t i o }$ is the effective token ratio. The best configuration for the baseline is highlighted in orange. The best results are bold and underlined, and the second-best results are underlined*

### 公平性说明

所有实验均未使用后续工作提出的加速或缓存优化技术（如Ma et al., 2025; Israel et al., 2025; Ben-Hamu et al., 2025等），仅对比原生固定长度去噪基线，确保性能增益完全归因于DAEDAL的长度自适应机制本身。此外，DAEDAL在所有实验中使用完全相同的超参数配置，未针对特定模型或基准进行任何调优。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Ic2A2gCseC/figures/005_Figure_1.jpg]]
*Figure 1: Overview of DAEDAL’s effectiveness on LLaDA-Instruct-8B. (a) DAEDAL uses a unified and short initial length, consistently surpassing the baseline, which needs its length meticulously tuned for each benchmark to achieve peak performance. (b) DAEDAL dynamically adjusts length and adaptively expands on a per-problem basis, resulting in a varied distribution of response lengths. In contrast, the baseline is constrained to a fixed length for all problems*



## 定位与知识库关联

DAEDAL 的核心贡献在于提出了一种**无需训练**的推理时可变长度去噪策略，直接解决了扩散大语言模型（DLLM）必须预先固定生成长度的根本性瓶颈。其方法定位可以从以下几个维度进行梳理：

### 1. 相对于原生的固定长度去噪基线

DAEDAL 直接建立在 **LLaDA**（Nie et al., 2025）这类原生扩散大语言模型的固定长度去噪范式之上。基线方法的推理过程要求在所有问题上使用相同的预定义长度 $L$，从完全掩码的序列开始进行迭代去噪，期间序列长度不发生任何变化。这一范式存在两个固有缺陷：长度过短导致性能不足，长度过长则造成计算浪费且可能引发性能退化。

DAEDAL 将这一“固定长度策略”替换为“动态自适应长度策略”，核心改变体现在两个层面：
- **推理前**：从短初始长度（默认 64）开始，通过评估序列末尾 EOS 令牌的预测置信度，循环扩展序列长度，直至达到任务所需的粗粒度长度。
- **推理中**：在去噪的每一步，识别低置信度位置并将其扩展为多个掩码令牌，为复杂推理提供局部空间。

实验表明，DAEDAL 在统一初始长度 64 的设置下，在 GSM8K、MATH500、MBPP、HumanEval 四个基准上均达到或超越了各自需要精心调优固定长度才能获得的峰值性能（Table 1），同时有效令牌比率 $E_{ratio}$ 提升至 64.3%，显著改善了计算效率。

### 2. 方法的核心洞察与因果机制

DAEDAL 的方法设计建立在一个关键的内部发现之上：**DLLM 内部对任务所需生成长度具有感知能力**。具体而言，模型在序列末尾对 EOS 令牌的预测置信度能够作为长度充足性的内部信号——当生成空间足够时，EOS 置信度更高；当空间不足时，置信度更低。这一洞察通过热力图实验得到验证（Figure 2, Figure 6），在长度充足与不足的问题上，EOS 置信度的差异以绿色（正值）为主，表明两者呈正相关。

基于这一因果机制，DAEDAL 将 EOS 置信度作为**控制变量**，驱动两个阶段的长度调整决策：
- **阶段一**（Initial Length Adjustment）：监控 EOS 置信度是否超过阈值 $\tau_{eos}$（默认 0.5），若未达到则追加掩码令牌并重新评估，形成闭环控制。
- **阶段二**（Iterative Mask Insertion）：监控每个掩码位置的预测置信度，对低于 $\tau_{low}$（默认 0.1）的位置进行局部扩展，为模型提供额外的推理空间。

### 3. 两阶段设计的协同效应

消融实验（Table 2）明确揭示了两阶段的互补关系：
- **单独使用阶段一**（仅初始长度调整）在初始长度 64 时达到 84.1% 准确率，已显著优于同长度基线（72.3%），但仍略低于最佳固定长度基线（83.8%）。
- **单独使用阶段二**（仅迭代掩码插入）在初始长度 64 时达到 72.3%，虽优于同长度基线，但因缺乏全局长度规划，仍未能达到基线峰值性能。值得注意的是，阶段二的性能对初始长度敏感——当初始长度过短时，全局规划能力受限。
- **完整 DAEDAL**（两阶段联合）达到 85.8%，超越了最佳固定长度基线（83.8%），证明两阶段存在协同效应：阶段一提供粗粒度的全局长度规划，阶段二提供细粒度的局部空间扩展。

### 4. 方法的适用边界与鲁棒性

DAEDAL 展现出对超参数的强鲁棒性，这降低了其实际部署的调优成本：
- **初始长度**：在 32 至 512 的范围内性能保持稳定，HumanEval 上准确率完全一致（Table 3）。
- **扩展因子** $E_{factor}$：在 8 至 32 范围内性能稳定，默认值 8 即取得最优效果（Table 4 左）。
- **EOS 置信度窗口大小** $W_{eos}$：对较大窗口值表现鲁棒，仅在极小窗口时出现退化（Table 4 右）。
- **阈值组合**：32 种 $(\tau_{high}, \tau_{low})$ 和 $(\tau_{eos}, \tau_{expand})$ 的网格搜索配置均与最佳固定长度基线持平或更优（Figure 5）。

所有实验使用完全相同的超参数配置（$L_{init}=64$, $L_{max}=2048$, $\tau_{eos}=0.5$, $\tau_{high}=0.9$, $\tau_{low}=0.1$, $\tau_{expand}=0.9$, $E_{factor}=8$, $W_{eos}=32$），未针对特定模型或基准进行调优。

### 5. 与后续工作的关系及公平性说明

为确保公平比较，DAEDAL 的实验明确排除了后续工作提出的加速或缓存优化方法（如 Ma et al., 2025; Israel et al., 2025; Ben-Hamu et al., 2025 等），仅与原生固定长度去噪基线进行对比。这意味着 DAEDAL 的性能增益完全来自其长度自适应策略本身，而非外部加速技术的叠加。在方法谱系中，DAEDAL 可以视为一种**正交于加速技术**的推理策略改进——理论上可与上述加速方法结合使用，获得进一步的效率提升。

### 6. 局限与开放问题

当前分析中未提供 DAEDAL 的明确局限性讨论或开放问题列表。从方法设计本身可以推断几个潜在边界：
- **阶段二的局部扩展依赖于置信度阈值**，在模型本身校准不佳的场景下，低置信度信号的可靠性可能下降。
- **最大长度上限** $L_{max}$ 仍然存在（默认 2048），对于需要超长生成的任务，DAEDAL 无法突破这一硬性约束。
- 方法目前仅在 LLaDA-Instruct-8B 单一模型上验证，跨模型、跨规模的泛化性需要进一步确认。

这些边界点需要结合论文的 Limitations 章节（如有）进行手动核实。



## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Fixed_Training_Free_Variable_Length_Denoising_for_Diffusion_Large_Language_Models.pdf]]
