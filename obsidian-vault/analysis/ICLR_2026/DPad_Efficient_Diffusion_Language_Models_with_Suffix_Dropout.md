---
title: "DPad: Efficient Diffusion Language Models with Suffix Dropout"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DPad_Efficient_Diffusion_Language_Models_with_Suffix_Dropout.pdf
project_link: null
code_link: https://github.com/Crys-Chen/DPad.git
openreview_forum_id: 0yOsSMU1eY
aliases:
- DPad
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过滑动窗口限制注意的后缀 token 数量，并结合距离衰减丢弃策略，在注意力计算前移除远距离 token。"
primary_logic: "发现后缀 token 充当了一个无语义的信息暂存器(scratchpad)，且大部分远距离后缀 token 是冗余的；通过稀疏化选择可以保留少量必要条件，从而在维持精确度的前提下大幅加速推断（扩散彩票假设）。"
claims:
- "距离衰减丢弃能够在保持精度同时大幅加速，DPad 实现高达61.4倍的加速比。"
- "后缀 token 的注意力随距离衰减，且剪除远距离高注意力 token 不影响精度，注意力会自适应地转移到邻近 token。"
- "后缀 token 充当跨层信息暂存器(Scratchpad)，仅需保留附近 token 即可保证生成质量。"
- "GSM8K (4-shot, LLaDA-Instruct) 上 Latency (s) = 18.35"
---

# DPad: Efficient Diffusion Language Models with Suffix Dropout

> [!tip] 核心洞察
> 发现后缀 token 充当了一个无语义的信息暂存器(scratchpad)，且大部分远距离后缀 token 是冗余的；通过稀疏化选择可以保留少量必要条件，从而在维持精确度的前提下大幅加速推断（扩散彩票假设）。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DPad：高效扩散语言模型的后缀丢弃方法 |
| 英文题名 | DPad: Efficient Diffusion Language Models with Suffix Dropout |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0yOsSMU1eY) · [GitHub](https://github.com/Crys-Chen/DPad.git) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DPad |
| Dataset | GSM8K (4-shot, LLaDA-Instruct), GSM8K (1024 tokens, 1-shot, LLaDA-1.5), HumanEval (0-shot |

> [!tip] 效果简介
> - GSM8K (4-shot, LLaDA-Instruct) 上，Latency (s) 为 18.35，对比 27.48，变化 1.50x 加速。
> - GSM8K (4-shot, LLaDA-Instruct) 上，Strict Match Accuracy 为 63.84，对比 37.38，变化 +26.46%。
> - GSM8K (1024 tokens, 1-shot, LLaDA-1.5) 上，Speedup (整体) 为 61.39×，对比 1.00× (Vanilla)，变化 61.39x 加速。

## 概要

块式扩散语言模型（dLLM）在推断时面临一个关键瓶颈：每一步需对所有未来后缀 token 进行注意力计算并预测，但最终仅保留其中一小部分，导致大量冗余计算。DPad 针对这一问题，提出了**无需训练的推断加速策略**，核心发现是后缀 token 实质上充当了一个无语义的“信息暂存器”（Scratchpad），且大部分远距离后缀 token 是冗余的——这一发现被概括为**扩散彩票假设**（Diffusion Lottery Tickets, DLT），即仅需保留少量“中奖”后缀 token 即可维持生成质量。

DPad 通过两个正交机制实现稀疏化：**滑动窗口**限定参与注意的后缀 token 数量，**距离衰减丢弃**在注意力计算前根据高斯采样概率移除远距离 token，从而避免计算其注意力分数。该方法可与并行解码、前缀缓存等现有优化方案叠加使用，在 LLaDA-1.5 上实现最高 **61.4 倍**的整体加速，同时保持可比精度。在短序列场景下，DPad 亦能带来约 1.5 倍的延迟改善，并因促使模型生成更精炼的回答而提升严格匹配（Strict Match）准确率。



### 块式扩散语言模型的推断瓶颈

扩散语言模型（diffusion Language Models, dLLMs）采用块式（block-wise）生成范式：每步迭代中，模型预测当前块内所有被遮蔽 token 的未来后缀，但仅保留置信度最高的一小部分进行更新，其余 token 被重新遮蔽并在后续步骤中继续迭代。这一机制意味着，每一步都必须对所有未来后缀 token 执行完整的注意力计算，而最终只有极少数 token 被真正“确认”。因此，**后缀 token 的冗余计算构成了 dLLM 推断的核心效率瓶颈**——模型在每一步花费大量计算资源处理最终会被丢弃的后缀信息。

从复杂度角度看，若生成长度为 $L$、块大小为 $B$，则每步需处理的后续 token 数量随生成推进呈二次增长，使得长序列生成场景下的延迟急剧膨胀。这一问题在原始扩散语言模型（如 LLaDA、Dream）中普遍存在，且现有的加速策略（如并行解码、前缀缓存）主要针对前缀计算进行优化，并未从根本上解决后缀冗余问题。

### 现有方法的缺口

针对 dLLM 推断效率的优化工作，现有方案主要集中在两个方向：

- **并行解码（Parallel Decoding）**：通过一次性预测多个 token 来减少总步数，但每步的后缀计算量并未减少。
- **前缀缓存（Prefix Caching）**：复用跨步的前缀键值缓存，避免重复编码已生成的 token，但对后缀注意力的计算开销无能为力。

此外，**Sparse-dLLM**（Song et al., 2025a）尝试基于注意力分数对后缀 token 进行剪枝，但该方法需要在注意力计算完成后才能判断哪些 token 可以丢弃，属于“先计算再筛选”的被动策略，无法消除注意力计算本身的开销。更重要的是，Sparse-dLLM 在极长序列（如 4096 tokens）上存在内存使用不稳定、峰值内存无法有效降低等问题。

### 本文动机：从“计算后丢弃”到“计算前剪枝”

本文的核心观察是：**后缀 token 在 dLLM 推断中充当了一个跨层信息暂存器（Scratchpad）**——它们在前一层收集来自前缀和当前块的信息，在下一层将这些信息回传给当前块，从而辅助去噪过程。然而，这一暂存机制并不需要完整的后缀序列：注意力分数随距离呈衰减趋势（Figure 3），且远距离后缀 token 的局部熵迅速趋近于零（Figure 6），表明它们携带的语义信息极为有限。

基于此，本文提出 **扩散彩票假设（Diffusion Lottery Tickets, DLT）**：在 dLLM 推断中，仅需保留一个稀疏的“中奖”后缀 token 子集，即可维持高质量的生成。这一假设为在注意力计算**之前**主动剪除冗余后缀 token 提供了理论依据——如果大部分远距离后缀 token 是冗余的，那么直接跳过它们的注意力计算，就能在不牺牲精度的前提下大幅加速推断。

DPad 正是在这一动机下设计的：通过**滑动窗口**限制后缀注意力的最大范围，结合**距离衰减丢弃**策略在注意力计算前移除远距离 token，将后缀计算从二次复杂度向线性复杂度压缩，实现训练无关（training-free）的高效推断。



## 核心方法与创新机理

### 瓶颈发现：后缀 token 的冗余计算

在块式扩散语言模型（dLLM）的推断过程中，模型每步需要预测当前块之后所有被遮蔽后缀 token 的概率，但最终仅保留置信度最高的少量 token 进行更新。这一“全量预测、少量保留”的机制导致大量冗余的注意力计算，成为推断延迟的主要瓶颈。

DPad 的核心洞察在于揭示了后缀 token 的功能本质：**后缀 token 并非承载语义信息，而是充当一个跨层的“信息暂存器”（Scratchpad）**。具体而言，在 Transformer 的注意力矩阵中，后缀 token 通过聚合前缀和当前块的信息（对应注意力矩阵的 Block 7 和 Block 8），并在下一层将这些信息回传给当前块（对应 Block 6），从而辅助去噪过程。这一发现意味着，后缀 token 的绝大部分是冗余的——仅需保留少数“必要条件”即可维持生成质量，DPad 将这一假设称为 **扩散彩票假设（Diffusion Lottery Tickets, DLT）**。

### 关键操控变量：后缀注意力范围的稀疏化

基于上述瓶颈，DPad 引入了一个训练无关（training‑free）的推断优化策略，核心改动槽位如下：

| 改动槽位 | 基线值 | DPad 方案 |
|---------|--------|----------|
| 后缀 token 注意力范围 | 全量（所有后缀 token 参与注意力计算） | 通过滑动窗口固定长度，结合距离衰减高斯采样剪除远距离 token |
| 后缀 token 保留概率 | 常数 1.0（全部保留） | 随距离指数衰减的高斯概率（Equation 7） |

具体而言，DPad 由两个正交组件构成：

1. **滑动窗口（Sliding Window）**：维持一个固定长度的后缀窗口，随当前块向前滑动，将参与注意力的后缀 token 数量从 $O(L)$ 限制为常数 $W$。
2. **距离衰减丢弃（Distance‑decay Dropout）**：在注意力计算**之前**，根据后缀 token 与当前块的距离 $d$，以高斯衰减概率 $P(d)$ 对其进行随机丢弃：

$$P(d) = a \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\left[-\frac{1}{2}\left(\frac{\frac{k\sigma}{W}\cdot d - \mu}{\sigma}\right)^2\right], \quad 0 < d \le W$$

其中 $k$ 控制衰减速率，$a$ 调节保留幅度。这一设计使得距离越远的后缀 token 被丢弃的概率越高，且无需计算注意力分数即可完成剪枝，从根源上避免了冗余计算。

### 证据支撑

- **注意力距离衰减**：Figure 3 显示，在 LLaDA‑1.5 的最后一层，后缀 token 的注意力分数随距离增加呈明显衰减趋势，为距离衰减丢弃提供了实证基础。
- **稀疏化不损精度**：Table 1 表明，强制剪除前 128 个位置以外注意力最高的 10 个后缀 token，GSM8K 严格匹配准确率反而从 40.5 提升至 41.7，HumanEval 从 37.8 提升至 39.0。Figure 4 进一步揭示，剪除远距离高注意力 token 后，注意力会自适应地转移到邻近 token，验证了邻近 token 足以吸收后缀信息。
- **加速效果**：DPad 在 LLaDA‑Instruct 上实现最高 1.50× 延迟加速（GSM8K, 4‑shot），与并行解码和前缀缓存叠加后，在 LLaDA‑1.5 上达到 **61.39×** 的整体加速比（GSM8K, 1024 tokens, 1‑shot），且准确率基本持平。

### 方法定位

DPad 属于训练无关的推断期稀疏化方法，与基于注意力分数的事后剪枝方法（如 **Sparse‑dLLM**, Song et al., 2025a）形成对比：后者需先计算完整注意力再剪枝，而 DPad 在注意力计算前即完成丢弃，从根本上降低了计算量。在极长序列生成（4096 tokens）场景下，DPad 相对 Sparse‑dLLM 实现 **39.64×** 的延迟加速，且保持相当精度。



![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of (a) autoregressive LLMs, (b) block-wise diffusion LLMs, and (c) our DPad. DPad restricts suffix attention via: (i) Sliding Window: fixed-length suffix window; (ii) Distance-decay Dropout: removes distant suffix tokens without computing attention scores*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/002_Figure_2.jpg]]
*Figure 2: Attention score maps illustrating the Scratchpad mechanism in dLLMs. The attention matrix is divided into 3×3 blocks over p r e f i x , current, and s u f f u x . Blocks 7 and 8 collect information from the prefix and current into the suffix at layer n, while Block 6 feeds this stored information back to the current block at layer (n+1)*

DPad 是一套**免训练的推断加速策略**，直接作用于块式扩散语言模型（dLLM）的逐块去噪过程。其核心目标是在不重新训练模型的前提下，消除每步推断中针对未来后缀 token 的冗余注意力计算，从而大幅降低延迟并维持生成质量。

### 核心瓶颈与设计动机

在标准 dLLM 推断中，每一轮去噪都需为当前块之后的所有后缀 token 计算注意力并预测其分布，但最终仅保留置信度最高的一小部分 token。这种“全量预测、少量保留”的模式导致大量计算被浪费在后缀 token 上，成为推断的主要瓶颈。DPad 的出发点正是**利用后缀注意力的固有稀疏性**，在注意力计算前主动剪除低价值后缀 token，将后缀相关计算从二次复杂度向线性复杂度压缩。

### 模块构成与数据流

DPad 的完整 pipeline 由四个功能模块串联而成，按执行顺序依次为：

1. **滑动窗口管理**  
   维护一个固定长度的后缀窗口，该窗口随当前块的位置同步前移。只有窗口内的后缀 token 才能进入后续的注意力计算，窗口外的 token 直接被排除。这一模块将参与注意的后缀 token 数量从“全部”限制为一个有界常数，从根本上控制了计算规模。

2. **距离衰减丢弃**  
   在窗口内部，根据每个后缀 token 与当前块的距离，通过高斯采样概率决定其是否被保留。保留概率 $P(d)$ 随距离 $d$ 增大而指数衰减：
   $$P(d) = a \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\left[-\frac{1}{2}\left(\frac{\frac{k\sigma}{W}\cdot d - \mu}{\sigma}\right)^2\right], \quad 0 < d \le W$$
   其中 $W$ 为窗口大小，$k$ 控制衰减速率，$a$ 调节整体保留幅度。这一丢弃操作在注意力分数计算之前完成，因此被剪除的 token 不会产生任何注意力计算开销。

3. **RoPE 位置修正**  
   被保留的 token 的位置 ID 会被重新映射回其在原始序列中的绝对位置，确保旋转位置编码（RoPE）的一致性不受窗口截断和丢弃操作的影响。

4. **提前终止**  
   一旦检测到 $\langle\text{eos}\rangle$ token，立即终止生成过程，避免按固定最大长度继续生成带来的冗余计算。该机制与 DPad 促使模型生成更精炼回答的特性形成协同效应。

### 输入输出与工作流

- **输入**：前序已解码的 prefix token 序列，以及当前待去噪的 masked block。
- **处理**：在每一轮去噪中，滑动窗口确定候选后缀范围，距离衰减丢弃从中采样出稀疏的“获胜”后缀 token 子集，RoPE 修正保证位置信息完整，随后仅对这些保留 token 执行注意力计算与 token 预测。
- **输出**：当前块中置信度最高的 token 被更新为确定值，窗口前移，进入下一轮去噪，直至所有块完成或提前终止。

整个流程无需修改模型权重或训练目标，可即插即用地部署到任意已有的 dLLM 推断框架中，并与并行解码、前缀缓存等正交优化技术叠加使用。



### 问题瓶颈与设计动机

块式扩散语言模型（dLLM）在推断的每一步都需要为**所有未来后缀 token** 预测概率分布，但最终仅保留置信度最高的一小部分 token 进行替换。这一“全量计算、少量保留”的机制导致了大量冗余的注意力计算，成为推断效率的核心瓶颈。DPad 的设计目标是在注意力计算之前，通过稀疏化选择移除冗余后缀 token，从而在不牺牲生成质量的前提下大幅降低计算开销。

### 核心洞察：Scratchpad 机制与扩散彩票假设

DPad 的方法设计建立在两个关键洞察之上：

**Scratchpad 机制**（Figure 2）：后缀 token 并不携带直接的语义信息，而是充当一个跨层的信息暂存器。注意力矩阵可划分为前缀（prefix）、当前块（current）和后缀（suffix）三个区域。在第 $n$ 层，Block 7 和 Block 8 分别将前缀和当前块的信息聚合到后缀 token 中；在第 $n+1$ 层，Block 6 将这些暂存的信息反馈回当前块。这一“写入-读取”循环使得后缀 token 成为信息中转站，而非语义载体。

**扩散彩票假设（Diffusion Lottery Tickets, DLT）**：基于 Scratchpad 机制，DPad 提出在 dLLM 推断中存在一组稀疏的“中奖”后缀 token，仅凭这些 token 即可保证高质量的去噪生成。这意味着大部分远距离后缀 token 是冗余的，可以被安全移除。

### 关键模块

DPad 是一个**无需训练**的推断策略，由以下四个模块协同工作：

#### 1. 滑动窗口管理

在每次迭代中，DPad 维护一个固定长度为 $W$ 的后缀窗口。该窗口紧随当前块移动，仅保留窗口内的后缀 token 参与注意力计算，窗口外的远距离 token 被直接丢弃。这一设计将后缀注意力的计算复杂度从二次方推向近似线性。

#### 2. 距离衰减丢弃

在滑动窗口内部，DPad 不采用均匀保留策略，而是根据后缀 token 与当前块的距离 $d$，通过高斯概率函数进行随机丢弃。距离越远，保留概率越低。丢弃操作在注意力计算**之前**完成，因此被剪除的 token 完全不参与后续的注意力矩阵运算，从根本上减少了计算量。

保留概率 $P(d)$ 定义为标准正态分布的右半部，经参数化调整：

$$P(d) = a \cdot \frac{1}{\sigma\sqrt{2\pi}} \exp\left[-\frac{1}{2}\left(\frac{\frac{k\sigma}{W}\cdot d - \mu}{\sigma}\right)^2\right], \quad 0 < d \le W$$

其中：
- $d$：后缀 token 与当前块的距离（$0 < d \le W$）
- $W$：滑动窗口大小
- $k$：衰减速率因子，控制概率随距离下降的陡峭程度
- $a$：幅度标量，控制保留概率的整体水平
- $\mu, \sigma$：标准正态分布的均值和标准差（$\mu=0, \sigma=1$）

该公式的核心作用是在窗口内实现**渐进式稀疏化**：邻近 token 以较高概率保留，远距离 token 以指数衰减的概率被丢弃。消融实验（Figure 5）证实，高斯丢弃函数在严格匹配精度上显著优于均匀丢弃，且窗口大小在 64–128 个后缀 token 附近达到最优性能。

#### 3. RoPE 位置修正

由于部分后缀 token 被丢弃，保留 token 的序列位置发生偏移。DPad 将保留 token 的位置 ID 重新映射到其原始绝对位置，确保 RoPE 位置编码的一致性，避免因位置信息错乱导致的生成质量下降。

#### 4. 提前终止

DPad 在检测到 `<eos>` token 后立即停止生成，避免固定长度生成模式下的冗余计算。这一机制与距离衰减丢弃形成互补：丢弃减少了每步的计算量，提前终止减少了总步数，二者叠加实现了端到端的延迟优化。

### 方法有效性验证

**注意力衰减与转移**（Figure 3, Figure 4）：实验表明，后缀 token 的注意力分数随距离呈整体衰减趋势，仅存在少量远距离的注意力尖峰。当强制剪除这些尖峰位置后，注意力会自适应地转移到邻近 token（Figure 4b），且精度不降反升（Table 1：Top-10 Pruning 使 GSM8K Strict 从 40.5 提升至 41.7）。这直接支持了扩散彩票假设——少数邻近 token 足以承载必要的去噪信息。

**局部熵衰减**（Figure 6）：后缀 token 的局部熵随距离快速衰减并趋近于零，从信息论角度证实远距离后缀 token 几乎不携带有效信息，进一步验证了距离衰减丢弃策略的合理性。



## 实验与关键发现

### 核心瓶颈与因果机制验证

块式扩散语言模型（dLLM）在每一生成步中需为所有未来后缀 token 计算注意力并预测其值，但最终仅保留置信度最高的一小部分 token。这一“全量计算、少量保留”的模式导致大量冗余计算，成为推断效率的根本瓶颈。DPad 的因果调节旋钮是：**在注意力计算前，通过滑动窗口限制参与计算的后缀 token 数量，并以距离衰减的高斯采样概率主动丢弃远距离 token**。这一设计的核心洞察来源于对后缀 token 功能的重新认识——它们并非承载独立语义，而是充当跨层信息暂存器（Scratchpad），且大部分远距离后缀 token 是冗余的。

**Scratchpad 机制**（Figure 2）揭示了后缀 token 的工作方式：注意力矩阵被划分为前缀、当前块、后缀三个区域，其中 Block 7 和 Block 8 在层 $n$ 将前缀和当前块的信息聚合到后缀中，Block 6 在层 $n+1$ 将这些暂存信息回传给当前块。这意味着后缀 token 本质上是信息中转站，而非语义载体。Figure 6 进一步证实，后缀 token 的局部熵随距离快速衰减并趋近于零，说明远距离后缀几乎不携带有效信息。

**注意力距离衰减**（Figure 3）在最后一层（Layer 31）上量化了这一现象：当前块 query 对后缀 key 的平均注意力随距离增加呈明显下降趋势，邻近 token 占据主导。更关键的是，当强制剪除远距离的高注意力“尖峰”位置后（Figure 4），注意力会自适应地转移到邻近 token 上，且 **Top-10 Pruning 实验**（Table 1）表明，剪除前 128 个后缀 token 之外注意力最高的 10 个 token 后，GSM8K Strict-Match 准确率反而从 40.5 提升至 41.7，HumanEval 从 37.8 提升至 39.0。这直接支持了**扩散彩票假设（Diffusion Lottery Tickets）**：只需保留稀疏的“中奖”后缀 token 即可维持甚至提升生成质量。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/006_Table_1.jpg]]
*Table 1: Accuracy Score of LLaDA-1.5 (Length = 512)*

### 主实验结果

#### 短序列生成（多 shot 设置）

Table 2 汇总了 LLaDA-Instruct 和 Dream-Base 在四个基准上的综合表现。对于 **LLaDA-Instruct**，DPad 在 GSM8K（4-shot）上实现 1.50× 延迟加速（27.48s → 18.35s），同时 Strict-Match 准确率大幅提升 26.46%（37.38 → 63.84）；在 MATH 上 Strict-Match 提升 19.62%；在 HumanEval（0-shot）上 Strict-Match 从 43.90 提升至 47.56（+8.3%）。结合并行解码（+Par.）后，整体加速比达到 2.72×–10.32×。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/007_Table_2.jpg]]
*Table 2: Consolidated performance of LLaDA-Instruct and Dream-Base on four benchmarks*

**Dream-Base** 同样获得显著加速（GSM8K 4-shot 延迟加速 2.17×），但准确率增益相对有限——这与 Dream 模型预训练源自自回归模型、对后缀上下文依赖较弱有关，属于方法适用性边界而非失效。

> ⚠️ **公平性说明**：短序列多 shot 场景下，prompt 占据主要计算量，后缀优化受 Amdahl 定律限制，加速比相对保守。真实长序列生成中 DPad 的优势更为显著。

#### 长序列生成（1-shot 设置）

Table 3 展示了 LLaDA-1.5 在 GSM8K（1024 tokens, 1-shot）上的表现。DPad 单独实现 **20.3× 加速**；结合并行解码（+Par.）和前缀缓存（+PC.）后，整体加速比达到 **61.39×**，同时 Strict-Match 准确率仅从约 78% 小幅下降至约 74%。这表明 DPad 的加速效应在长序列场景下与现有优化策略叠加，且精度损失可控。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/012_Table_3.jpg]]
*Table 3: Performance on LLaDA-1.5 with GSM8K (1024 tokens, 1-shot)*

在与 **Sparse-dLLM**（Song et al., 2025a）的直接对比中（Table 8），当最大生成长度 $L_{max}=4096$ 时，DPad 延迟仅为 5.39s，而 Sparse-dLLM 为 213.65s，加速比达 **39.64×**，且准确率相当。Figure 13 进一步显示，Sparse-dLLM 的主动内存在长序列生成中出现不稳定振荡，且无法降低峰值内存需求；DPad 则实现了实际内存节省。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/032_Table_8.jpg]]
*Table 8: Efficiency and accuracy evaluation of Sparse-dLLM vs. DPad using LLaDA-1.5 on 100 samples of GSM8K with different max generation length ( $l _ { \mathrm { m a x } }$ )*

### 消融实验

#### 丢弃函数选择：高斯 vs. 均匀

Figure 5 的消融热力图系统比较了均匀丢弃与高斯丢弃在不同滑动窗口大小和保留 token 数量下的表现。**高斯丢弃在 Strict-Match 准确率上显著优于均匀丢弃**，尤其在窗口大小 64–128 个后缀 token 附近性能达到最优。Figure 14 对高斯超参数 $k$ 和 $a$ 的消融表明，$k=2$ 或 $k=3$、保留密度 25%–37.5% 的设置在各任务上鲁棒性最佳。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/011_Figure_5.jpg]]
*Figure 5: Ablation Study on Sliding Window Size and Dropout Function for DPad on LLaDA-1.5/GSM8K (512, 4-shot). Heatmaps showing Flexible-Match Accuracy scores with (a) uniform and (b) Gaussian dropout, and Strict-Match Accuracy scores with (c) uniform and (d) Gaussian dropout, across varying sliding window sizes and number of preserved suffix tokens. The (tokens, window size) = (512, 512) configuration corresponds to the baseline, as it involves no token dropout*

#### 随机丢弃 vs. 确定性丢弃

Table 10 的对比结果具有决定性：**随机距离衰减丢弃（DPad）**在 Flexible-Match 上达到 79.98、Strict-Match 68.84；而**固定远距离丢弃**（Fixed Distant）导致性能崩溃——Flexible 降至 28.51、Strict 降至 21.83。固定近距离丢弃虽保持一定精度，但丧失了加速效果。这证实了随机采样的必要性：它允许模型在不同生成步自适应地选择不同的后缀子集，避免确定性模式导致的系统性信息丢失。

#### 窗口大小与位置修正

滑动窗口将后缀注意力复杂度从二次降低为近线性。RoPE 位置修正确保保留 token 映射回原始绝对位置，维持位置编码一致性。消融显示，窗口过小（< 32）会导致信息不足，过大（> 256）则加速效果递减，64–128 是精度-效率的最佳平衡区间。

### 失败模式与局限性

1. **极长序列精度波动**：在 Dream-Base 的 HumanEval 2048-token 生成中（Figure 12），DPad 出现约 7.32% 的精度下降。推测原因是训练时的全量后缀条件与推理时的稀疏后缀条件之间存在分布偏移，尤其对自回归预训练模型更为明显。

2. **模型类型依赖性**：Dream 模型从 DPad 获得的精度增益远小于 LLaDA，因其预训练基础不同，对后缀上下文的依赖程度较低。DPad 的效果与底层模型的训练策略强相关。

3. **吞吐率指标失真**：DPad 促使模型生成更精炼的回答并触发提前终止（<eos> 检测），导致 TPS（每秒生成 token 数）增益偏低甚至为负。但端到端延迟改善显著，社区需要更合理的效率-精度联合评价指标。

4. **实验设置局限**：当前实验主要基于块大小 32、批量 1 的设置，不同块大小和批量下的泛化性有待验证。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 2 | 后缀 token 充当跨层信息暂存器，通过 Block 6/7/8 实现信息中转 |
| Figure 3 | 最后一层注意力随距离衰减，邻近 token 占主导 |
| Figure 4 | 剪除远距离高注意力 token 后注意力自适应转移至邻近 token |
| Table 1 | Top-10 剪枝反而提升 Strict-Match 准确率，支持扩散彩票假设 |
| Figure 5 | 高斯丢弃优于均匀丢弃，窗口 64–128 性能最优 |
| Table 2 | DPad 在四基准上实现 1.18×–3.91× 加速，LLaDA-Instruct Strict-Match 最高提升 26.46% |
| Table 3 | 结合并行解码与前缀缓存，整体加速达 61.39× |
| Table 8 | 4096-token 长序列上相对 Sparse-dLLM 加速 39.64× |
| Table 10 | 随机丢弃远优于确定性丢弃，固定远距离丢弃导致性能崩溃 |
| Figure 13 | DPad 实现实际峰值内存节省，优于 Sparse-dLLM 的被动淘汰策略 |

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/013_Table_4.jpg]]
*Table 4: Representative examples of the Countdown (Ye et al., 2024) and Sudoku (Seely et al., 2025) benchmarks. Sudoku (4 × 4) serves as a rigorous test for global planning, requiring the model to fill empty cells (’0’) while maintaining strict consistency across rows, columns, and subgrids*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/014_Table_5.jpg]]
*Table 5: Quantitative verification of the scratchpad mechanism on planning benchmarks. We compare performance across three levels of memory availability. The results show that Sudoku performance collapses to 0.0 without the full scratchpad (AR models and Semi-AR dLLMs) and recovers only when the suffix memory is fully enabled (Semi-AR+SD+PD and Global-Diffusion)*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/028_Table_6.jpg]]
*Table 6: Performance of LLaDA-1.5 with DPad on four benchmarks*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/031_Table_7.jpg]]
*Table 7: Comparison of Operational Paradigm and Memory Complexity for Suffix Tokens*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_0yOsSMU1eY/figures/037_Table_9.jpg]]
*Table 9: The hyperparameters for Gaussian Sampler used in main experiments in Sec. 4.2*



## 定位与知识库关联

### 1. 方法在扩散语言模型谱系中的位置

DPad 属于**训练无关的块式扩散语言模型（dLLM）推断加速方法**，其核心操作对象是后缀 token 的注意力计算。在方法谱系上，它位于以下两条路线的交汇点：

**路线一：dLLM 推断效率优化。** 原始块式扩散模型（如 LLaDA、Dream）在每步推断中需对所有未来后缀 token 执行完整注意力计算，但仅保留置信度最高的一小部分 token 进行下一轮去噪，导致大量冗余计算。已有优化工作包括：
- **并行解码（+Par.）**（Wu et al.）：通过并行预测多个 token 减少迭代步数，但不改变单步计算量。
- **前缀缓存（+PC.）**（Wu et al.）：缓存前缀的 KV 状态以复用计算，但后缀部分仍需完整计算。
- **Sparse-dLLM**（Song et al., 2025a）：基于注意力分数动态剪枝后缀 token，但需要先计算注意力再决定剪枝，无法消除注意力计算本身的开销。

DPad 的关键区别在于**在注意力计算之前**即通过距离衰减策略丢弃远距离后缀 token，从根本上减少参与注意力计算的 token 数量。这使得 DPad 可以与上述方法叠加：实验表明，DPad 单独使用时在 GSM8K（1024 tokens, 1-shot）上实现 20.3× 加速，结合并行解码和前缀缓存后整体加速达 61.39×（Table 3）。

**路线二：注意力稀疏化。** DPad 的滑动窗口 + 距离衰减丢弃可视为一种结构化的注意力稀疏模式。与通用稀疏注意力（如 Longformer、BigBird）不同，DPad 的稀疏模式是**任务和模型结构驱动的**：它基于对 dLLM 中后缀 token 功能的机制性理解——即后缀 token 充当跨层信息暂存器（Scratchpad），且其信息含量随距离快速衰减。

### 2. 核心机制：扩散彩票假设与 Scratchpad 暂存器

DPad 的理论基础是作者提出的**扩散彩票假设（Diffusion Lottery Tickets, DLT）**：在 dLLM 推断中，仅需保留一个稀疏的“中奖”后缀 token 集合即可维持生成质量。该假设由以下机制性发现支撑：

**Scratchpad 暂存器机制（Figure 2）。** 注意力矩阵被划分为 3×3 块（前缀、当前块、后缀）。在层 $n$，后缀通过 Block 7（后缀→前缀注意力）和 Block 8（后缀→当前块注意力）从前缀和当前块收集信息；在层 $n+1$，Block 6（当前块→后缀注意力）将这些暂存信息反馈给当前块。这意味着后缀 token 本身不携带语义信息，而是作为**无语义的信息中转站**。

**注意力距离衰减（Figure 3, Figure 4）。** 在最后一层，后缀 token 的注意力分数随距离呈明显衰减趋势。即使存在偶尔的远距离注意力尖峰，强制剪枝这些尖峰位置后，注意力会自适应地转移到邻近 token（Table 1：Top-10 Pruning 后 GSM8K Strict Match 从 40.5 升至 41.7）。这证明**邻近 token 可以吸收远距离 token 的信息负载**。

**局部熵快速衰减（Figure 6）。** 后缀 token 的局部熵随距离迅速下降并趋近于零，确认远距离后缀 token 的信息含量极低，是冗余的。

### 3. 与基线方法的适用边界对比

| 方法 | 是否训练无关 | 剪枝时机 | 剪枝依据 | 与并行解码/前缀缓存叠加 |
|------|-------------|---------|---------|----------------------|
| Sparse-dLLM (Song et al., 2025a) | 是 | 注意力计算后 | 注意力分数 | 可叠加 |
| DPad（本方法） | 是 | 注意力计算前 | 距离衰减概率 | 可叠加，加速叠加效应显著 |

DPad 的核心优势在于**前置剪枝**：Sparse-dLLM 仍需为所有后缀 token 计算注意力分数再决定保留哪些，而 DPad 通过距离衰减概率直接丢弃远距离 token，完全避免其注意力计算开销。在极长序列（$L_{max}=4096$）上，DPad 相对 Sparse-dLLM 的延迟加速达 39.64×，且保持相当精度（Table 8）。

**适用边界差异：**
- **LLaDA 模型**：DPad 效果显著，不仅在效率上大幅提升，在 GSM8K 和 MATH 的严格匹配准确率上还分别提升 26.46% 和 19.62%（Table 2），这归因于 DPad 促使模型生成更精炼、格式更规范的输出。
- **Dream 模型**：DPad 的精度提升有限。Dream 的预训练基于自回归模型，对后缀上下文的依赖模式与 LLaDA 不同，导致距离衰减丢弃的信息损失更难被邻近 token 补偿。在 2048-token HumanEval 上甚至出现 7.32% 的精度下降（Figure 12）。

### 4. 局限性与开放问题

**已识别的局限性：**

1. **训练-推断分布偏移。** 在极长序列生成（如 2048 tokens）中，DPad 可能导致精度下降，推测原因是训练时模型始终看到完整后缀，而推断时后缀被稀疏化，这种条件分布差异在长序列中累积放大。

2. **模型类型依赖性。** Dream 模型从 DPad 获得的精度收益有限，表明方法效果受底层模型训练策略（是否为原生扩散训练）的显著影响。

3. **实验设置覆盖有限。** 当前实验主要基于块大小 32、批量 1 的设置，不同块大小和批量下的表现有待验证。

4. **吞吐率指标失真。** DPad 通过提前终止和简洁生成减少总生成长度，导致 TPS（每秒生成 token 数）增益偏低（有时仅 1.04×），但端到端延迟改善显著（1.50×–61.39×）。社区需要更合理的效率-精度联合评价指标。

**开放问题：**

1. **训练阶段整合。** 距离衰减丢弃能否直接整合到预训练阶段，使训练与推断条件对齐，从而获得更优的效率-精度折衷？

2. **最优衰减函数。** 高斯采样是否为最优选择？是否存在自适应或学习型的稀疏模式选择方案？消融实验（Figure 5）表明高斯函数优于均匀函数，但未探索指数衰减、阶梯截断等其他形式。

3. **Dream 模型精度波动根因。** 为什么 Dream 在 DPad 下出现部分任务的精度波动（如 2048-token HumanEval 精度下降 7.32%）？这是否与 Dream 的自回归预训练基础导致的注意力模式差异有关？

4. **评价指标改进。** 如何设计新的效率指标，以更好地奖励生成精炼和提前终止带来的实际效率提升，而非仅关注原始 TPS？



## 原文 PDF

![[paperPDFs/ICLR_2026/DPad_Efficient_Diffusion_Language_Models_with_Suffix_Dropout.pdf]]
