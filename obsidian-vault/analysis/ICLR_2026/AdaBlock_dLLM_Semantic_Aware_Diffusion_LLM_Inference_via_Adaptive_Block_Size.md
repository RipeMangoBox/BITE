---
title: "AdaBlock-dLLM: Semantic-Aware Diffusion LLM Inference via Adaptive Block Size"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdaBlock_dLLM_Semantic_Aware_Diffusion_LLM_Inference_via_Adaptive_Block_Size.pdf
aliases:
- AdaBlock-dLLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过动态识别分隔符词元的置信度，自适应地调整块大小，使其与语义步骤的边界对齐，从而在运行时实现语义感知的块调度。"
primary_logic: "去噪过程中置信度动态呈现出高置信度平台、波动带（VB）与低置信度底层三个区域，波动带编码了局部语义结构；高置信度的语义分隔符（如换行、逗号、句点）可有效标记语义步骤边界，为自适应块大小调整提供可靠信号。"
claims:
- "固定块大小导致延迟解码开销与过早解码错误，两者在多个基准上均占大量步骤。"
- "波动带（VB）是当前解码步骤发生的核心区域，其内部置信度波动剧烈且宽度因样本而异。"
- "在采样窗口中选取具有最高置信度的分隔符词元作为块边界，能有效对齐语义步骤，降低错误。"
- "GSM8K 上 accuracy = 80.6%"
---

# AdaBlock-dLLM: Semantic-Aware Diffusion LLM Inference via Adaptive Block Size

> [!tip] 核心洞察
> 去噪过程中置信度动态呈现出高置信度平台、波动带（VB）与低置信度底层三个区域，波动带编码了局部语义结构；高置信度的语义分隔符（如换行、逗号、句点）可有效标记语义步骤边界，为自适应块大小调整提供可靠信号。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AdaBlock-dLLM：基于自适应块大小的语义感知扩散大语言模型推理 |
| 英文题名 | AdaBlock-dLLM: Semantic-Aware Diffusion LLM Inference via Adaptive Block Size |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0Cv9PwL7cI); [GitHub](https://github.com/lgxi24/AdaBlock-dLLM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | AdaBlock-dLLM |
| Dataset | GSM8K, Overall |

> [!tip] 效果简介
> - GSM8K 上，accuracy 为 80.6%，对比 77.6%，变化 +3.0%。
> - GSM8K 上，accuracy 为 80.7%，对比 74.5%，变化 +6.2%。
> - GSM8K 上，throughput (TPS) 为 51.3，对比 44.5，变化 +6.8 TPS。

## 概述

在半自回归（Semi-AR）扩散语言模型（dLLM）的解码中，固定块大小会导致两类根本性问题：**延迟解码开销**与**过早解码错误**。高置信度的词元因块边界限制而被推迟解码，造成不必要的推理步骤；低置信度的词元则被迫在当前块内提前提交，引发错误并沿序列传播，损害生成质量。这两个问题分别增加了计算开销和解码噪声，成为现有高效抽样方法（如Fast-dLLM）的性能瓶颈。

针对上述问题，本文提出 **AdaBlock-dLLM**，一种**无训练、即插即用**的推理时优化方法。其核心调节手段是：利用去噪过程中动态涌现的**词元置信度信息**，在运行时识别语义分隔符（如换行、逗号、句点）并以其最高置信度位置作为自适应块边界，从而使解码块的大小自然对齐局部语义步骤的边界，消除固定块大小所引入的对齐偏差。

该设计的有效性建立在两条核心观察之上：  
1. 去噪过程中，序列不同位置的置信度呈现**高置信度平台、波动带（VB）与低置信度底层**三个区域，波动带编码了当前解码步骤的局部语义结构，且其内部置信度分布因样本而异。  
2. 波动带内，换行等分隔符词元往往具有最高置信度，能够可靠地标示语义步骤的结束，为自适应块调度提供强信号。

方法层面上，AdaBlock-dLLM 仅对原有 Fast-dLLM 流程中的**块大小**和**分隔符阈值**两个插槽进行改进：将固定的块大小 $B_0$ 替换为基于最高置信度分隔符位置的自适应长度；引入分隔符置信度阈值 $\tau_D$ 控制调度的灵敏度。其余模块（去噪器、动态采样、块内循环解码与 KV 缓存）均保持原有架构，确保了方法的即插即用性。

主要实验结果表明：
- 在相同吞吐量预算下，AdaBlock-dLLM 在 GSM8K 等数学推理基准上相较 Fast-dLLM 的准确率提升最高达 **5.3%**，且几乎无额外吞吐开销，在多个基准上呈现帕累托最优。
- 对于 LLaDA-Instruct（$B_0=32$），加入 AdaBlock 使准确率从 77.6％ 提升至 **80.6％**；结合块级 KV 缓存后，在 $B_0=64$ 下达到 **80.7％**，相较仅为缓存的版本提升 6.2 个百分点。
- 在较小默认块大小（$B_0=4$）下，吞吐量从 44.5 TPS 提升至 **51.3 TPS**，同时准确率亦获改善。
- 消融实验确认：使用换行符作为唯一分隔符已可捕获大部分增益，进一步纳入逗号和句点可继续提升准确率；对从头训练的 dLLM（如 LLaDA），较低的阈值 $\tau_D=0.3$ 即可提供足够的语义引导，而自适应度更强的模型（如 Dream）则需更高阈值以应对波动带方差。

综上，AdaBlock-dLLM 通过语义感知的自适应块调度，在几乎不改变原始推理开销的情况下有效缓解了固定块解码的固有矛盾，为扩散语言模型的高效生成提供了一种简单而有效的范式。

## 背景与动机

扩散语言模型（dLLMs）通过迭代去噪生成文本，天然支持灵活的解码策略。半自回归解码（如 Fast‑dLLM）通过将生成过程划分为固定大小的块来兼顾质量与效率：在每个块内执行多步去噪‑采样，块间采用 KV 缓存复用。然而，固定块大小与自然语义步骤之间的失配引入了两类根本性损耗：**延迟解码开销**与**过早解码错误**（Section 4.2，Figure 1、Figure 5）。前者发生在高置信度词元因块边界限制而被推迟到后续块解码，浪费了计算与步骤；后者迫使尚未确定的低置信度词元在当前块内提前采样，产生错误并向后传播。量化分析显示，在 GSM8K 和 HumanEval 基准上，固定块大小导致大量解码步骤受这两类问题影响（Figure 5），直接削弱了生成质量与吞吐量。

深入观察 dLLM 的去噪过程，可以发现其置信度分布呈三层结构：**高置信度平台**（已完成语义区域）、**低置信度底层**（远期待解码区域）以及介于两者之间的**波动带（Volatility Band，VB）**（Section 4.1，Figure 4）。波动带紧邻已解码前缀，内部置信度剧烈波动，编码了局部语义结构与不确定性。更重要的是，该区域中高置信度的分隔符词元（如换行符 `\n`、逗号、句点）往往标记着语义步骤的自然边界（Figure 9，Table 7），它们表现出对上下文语义完成的高度确认。这些观察到的事实揭示了一个核心洞察：**在波动带内识别置信度最高的分隔符词元，可以近似获取语义边界的位置，从而为自适应调整块大小提供可靠信号**（Section 4.3，Algorithm 1）。据此，固定块大小的缺陷可通过"让块边界对齐语义步骤边界"这一因果机制得到系统性缓解。

上述发现直接构成了 AdaBlock‑dLLM 的设计动机：在不修改模型权重的条件下，通过运行时动态采样与置信度引导的块调度，使得解码器能够**语义感知地**自适应确定块大小，从而在保留半自回归加速优势的同时，显著降低延迟解码开销与过早解码错误。

## 核心创新

现有半自回归解码框架（如 Fast-dLLM）采用**固定块大小** $B_0$ 进行逐块去噪，这会在推理中引入两类根本性问题：当高置信度词元因块边界限制而无法在当前块中被解码时，产生**延迟解码开销**（Late Decoding Overhead）；而低置信度词元被迫在当前块内提前提交，则导致**过早解码错误**（Premature Decoding Error）并沿序列传播。定量分析表明，在 GSM8K 与 HumanEval 上，固定块大小下受这两类问题影响的采样步骤占比居高不下（Figure 5，Section 4.2）。

回答这一瓶颈的关键旋钮在于**将块大小与语义步骤的边界动态对齐**。论文发现，扩散语言模型在去噪过程中，各位置的置信度呈三区分布：已解码前缀附近形成一个不断扩展的**高置信度平台**，相邻的掩码区域则出现高方差的**波动带**（Volatility Band, VB），再远处为低置信度底层（Figure 3, Figure 4）。波动带内部置信度剧烈波动且宽度因样本而异，编码了丰富的局部语义结构。尤其地，高置信度的**语义分隔符词元**（如换行符 `\n`、逗号、句点）可有效标记语义步骤的自然边界——统计上，`\n` 是导致连续词元间置信度大幅下降的最频繁词元（Figure 9, Section A.4），其高置信度出现时刻恰好对应局部语义单元的完成。

基于此核心洞察，**AdaBlock-dLLM 提出基于分隔符置信度的自适应块调度机制**：在每一次外层解码步骤中，从当前掩码序列的预设窗口内，动态选取置信度最高的分隔符词元；若该词元的置信度不低于阈值 $\tau_D$，则以该词元的位置作为新块大小 $B$，否则退化为默认固定块大小（Algorithm 1）。这一设计本质上改变了半自回归解码的关键控制槽：

- **块大小**（`block_size`）：从固定的 $B_0$ 转变为**由当前预测中置信度最高的分隔符位置决定的自适应值**（Section 4.3, Algorithm 1）。
- **分隔符置信度阈值**（`delimiter_threshold` $\tau_D$）：引入全新控制参数 $\tau_D$，用于过滤不可靠的分隔符信号，防止调度器因低置信度分隔符而产生错误的对齐。消融实验表明，对从头训练的 dLLM（如 LLaDA），较低的 $\tau_D=0.3$ 已提供充分语义引导并取得最高准确率；过高的阈值则使调度器退化为固定块大小（Table 5）。

通过这一语义感知的自适应块大小调整，AdaBlock-dLLM 无需训练即可在推理时将块边界动态对齐于语义步骤的完成点，从根本上缓解了延迟解码开销与过早解码错误（Figure 1 右侧示意图），在几乎不损失吞吐量的前提下普遍提升准确率（最高达 5.3%，Figure 2）。

## 整体框架

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/001_Figure_1.jpg]]
*Figure 1: Illustrative examples of two fundamental issues (left) and how AdaBlock-dLLM addresses them (right). Appendix A.1 presents a case study from a real inference scenario*

AdaBlock‑dLLM 构建于扩散语言模型的半自回归解码范式之上，其核心改进在于将固定块大小替换为**语义感知的自适应块调度**。整体流程分为四个协同模块，通过置信度动态将块边界对齐到语义步骤的天然分界点，从根本上缓解延迟解码开销与过早解码错误。

1. **去噪器 (Denoiser)**  
   在每一解码步骤中，掩码序列 $\mathbf{y}^t$ 被送入扩散语言模型，输出每个掩码位置的词元分布 $p_\theta(v \mid \mathbf{y}^t, i)$。由此通过贪心解码得到当前预测 $\hat{y}_i^t = \arg\max_v p_\theta(v \mid \mathbf{y}^t, i)$，同时提取每个位置的置信度（即最高概率值）作为后续调度的核心信号。

2. **基于阈值的动态采样 (Threshold‑based Dynamic Sampling)**  
   依据置信度阈值 $\tau$，从当前掩码位置集合 $\mathcal{M}_t$ 中筛选本次需要解掩码的位置 $S_t$：优先选取置信度最高的位置，然后将所有置信度 $\ge \tau$ 的掩码位置纳入 $S_t$。状态更新遵循规则 $$y_i^{t-1} = \begin{cases} \hat{y}_i^t, & i\in S_t \\ [\mathsf{MASK}], & i\in\mathcal{M}_t\setminus S_t \\ y_i^t, & i\notin\mathcal{M}_t \end{cases}$$  
   该动态采样使解码进度由置信度驱动，避免一次性提交过多低置信度词元。

3. **块大小确定 (ComputeBlockLength)**  
   在进入新块之前，从当前已解码前缀后的采样窗口中寻找**置信度最高的分隔符词元**（如换行符、逗号、句点）。若该分隔符的置信度达到预设阈值 $\tau_D$，则将块大小设为该分隔符的位置；否则回退到默认固定块大小 $B_0$。这一机制将块边界与"局部语义意义已完整"的高置信度位置对齐，使每个块大致对应一个语义步骤。

4. **半自回归解码循环 (Semi‑AR Decoding Loop)**  
   外层循环按**自适应块大小**依次处理各块，内层循环在每个块内反复执行"去噪 → 动态采样"，直至该块内所有位置均已解掩码。内层循环支持**块级 KV 缓存**，可复用已解码前缀的键值表示，显著减少重复计算。解码完成后，算法以并行方式提交整个块的结果，既保留了扩散模型并行解码的优势，又通过语义感知边界提升了生成质量。

上述框架不修改模型权重，是一种**即插即用的推理时优化**。其输入为带掩码的 prompt 序列，输出为最终完全解掩码的生成序列；中间通过置信度驱动的采样与自适应块调度，将固定块大小的刚性解码转换为与语义节奏自适应的柔性过程。

## 核心模块与公式推导

**瓶颈与因果机制**  
在半自回归扩散语言模型（dLLM）解码中，固定块大小导致两个根本性问题：高置信度词元因块边界限制而被强行推迟解码（延迟解码开销），低置信度词元被迫在当前块内提前提交，引发错误并扩散（过早解码错误）。造成这一矛盾的本质原因是块大小与语义步骤长度失配：语义边界常出现于高置信度的分隔符词元（如换行、逗号、句点）处，而固定块大小无法感知这一动态结构。AdaBlock‑dLLM 的因果旋钮是在推理时动态识别波动带中置信度最高的分隔符词元，以其位置实时调整块大小，使去噪‑采样循环与语义步骤边界对齐，从而同时抑制延迟与过早错误，在几乎不损失吞吐量的前提下提升生成质量。

### 核心模块

1. **去噪器（Denoiser）**  
   基于掩码预测模型（如 LLaDA 的双向 Transformer），输入当前掩码序列 $\mathbf{y}^t$，输出每个位置 $i$ 的词元分布 $p_\theta(v | \mathbf{y}^t, i)$ 及对应的最高置信度 $c_i^t = \max_v p_\theta(v | \mathbf{y}^t, i)$。去噪器是后续所有置信度分析与采样决策的信号源。

2. **置信度动态与波动带识别**  
   在解码过程中，置信度沿序列自然呈现出三个区域：  
   - **高置信度平台**：已解码前缀附近的置信度随解码推进逐渐扩张，词元置信度普遍较高且稳定；  
   - **波动带（Volatility Band, VB）**：紧邻已解码前缀的位置，置信度剧烈波动，是当前解码活动发生的核心区域；  
   - **低置信度底层**：远未来位置的置信度普遍很低。  
   图 4 展示的 VB 内部置信度分布和宽度因样本而异，其波动性编码了局部语义结构的不确定性，而高置信度的分隔符词元（尤其是换行符 `\n`）频繁出现在 VB 内并导致大幅度的置信度下降（图 9），这使其成为标记语义步骤边界的可靠信号。

3. **动态采样模块（Threshold‑based Dynamic Sampling）**  
   基于置信度阈值 $\tau$ 的解掩码策略：首先选取全局置信度最高的一个位置，随后将所有置信度 $c_i^t \ge \tau$ 的掩码位置一并纳入解掩码集合 $S_t$。这一策略控制每步采样出词元的激进程度，公式为  
   $$S_t = \{i \in \mathcal{M}_t : c_i^t \ge \tau\} \cup \{\arg\max_{i\in\mathcal{M}_t} c_i^t\}.$$

4. **块大小确定模块（ComputeBlockLength）**  
   在动态采样选择的解掩码窗口中，模块计算所有预设分隔符词元（集合 $\mathcal{D}$，默认 $\{\backslash\text{n}, \text{,}, .\}$）的置信度，选取置信度最高的分隔符。若其置信度 $c_i^t \ge \tau_D$（$\tau_D$ 为分隔符阈值），则块大小 $B$ 设为该分隔符的位置（即窗口边界截断于此）；否则退化到默认固定块大小 $B_0$。该模块无显式封闭公式，核心逻辑由 Algorithm 1 描述。

5. **半自回归解码循环（Semi‑AR Decoding Loop with In‑block Cycles）**  
   外层循环按自适应块大小依次处理序列片段：对当前块内所有掩码位置反复执行去噪→动态采样，直到该块内已无掩码位置，然后移动到下一块。内层复用块级 KV 缓存以降低计算量。整体流程见 Algorithm 4。

### 关键公式与变量含义

设生成序列总长度为 $L$，位置索引集合 $\mathcal{I} = \{1,\dots,L\}$，词表为 $\mathcal{V}$。在解码步骤 $t$，序列状态为 $\mathbf{y}^t = (y_1^t,\dots,y_L^t)$，其中已解码位置为具体词元，未解码位置为 `[MASK]`。

- **贪婪预测**（公式 (1)）  
  $$\hat{y}_i^t = \underset{v\in\mathcal{V}}{\arg\max}\, p_\theta(v \mid \mathbf{y}^t, i),$$  
  对每个位置 $i$，选置信度最高的词元作为候选。$p_\theta$ 为预先训练好的掩码预测模型。

- **掩码位置集合**（公式 (2)）  
  $$\mathcal{M}_t \triangleq \{i\in\mathcal{I}: y_i^t = [\mathsf{MASK}]\},$$  
  记录当前步骤中尚未解码的位置，采样与块调度仅作用于 $\mathcal{M}_t$。

- **状态更新规则**（公式 (3)）  
  $$y_i^{t-1} = \begin{cases}
  \hat{y}_i^t, & i\in S_t \quad \text{(解掩码)}, \\
  [\mathsf{MASK}], & i\in\mathcal{M}_t\setminus S_t \quad \text{(保持掩码)}, \\
  y_i^t, & i\notin\mathcal{M}_t \quad \text{(已解码，不变)}.
  \end{cases}$$  
  根据采样集合 $S_t$ 更新序列：选中的位置用预测词元替换 `[MASK]`，未选中的掩码位置保持掩码，已解码位置不变。这一更新为下一轮去噪提供新输入 $\mathbf{y}^{t-1}$（公式 (4)）。

- **序列状态**（公式 (4)）  
  $$\mathbf{y}^{t-1} = (y_i^{t-1})_{i\in\mathcal{I}} \in \mathcal{V}^{L},$$  
  更新后的完整序列。

上述公式构成了置信度驱动解码的基础，而自适应块大小调度的核心（分割符词元选择与阈值决策）建立在置信度序列 $\{c_i^t\}$ 的动态分析之上，无需额外训练，即插即用地将固定半自回归解码转换为语义感知的自适应解码。

## 实验与分析

### 主实验结果：准确率与吞吐量提升

AdaBlock‑dLLM 在四个数学推理基准（GSM8K、HumanEval、MATH、MBPP）上稳定提升准确率。在 LLaDA‑Instruct 的默认块大小配置下，+Ada 使 GSM8K 准确率从 Dynamic 的 77.6% 提升至 80.6%（+3.0%），配合缓存后效果更显著：B₀=64 时 +Ada+Cache 达到 80.7%，相较于仅 +Cache 的 74.5% 提升 **+6.2%**（Table 1）。在生成预算相同的条件下，该方法在较小默认块上还带来吞吐量增益——例如 B₀=4 时，+Ada 将吞吐量从 44.5 TPS 提升至 51.3 TPS，同时准确率由 79.4% 升至 81.6%（Table 2）。Figure 2 的散点图进一步表明，AdaBlock‑dLLM 在准确率‑吞吐量平面上形成了对 Fast‑dLLM 的帕累托改进，**最高准确率增益可达 5.3%**。将 AdaBlock 嵌入 Fast‑dLLM 后，GSM8K 和 MATH 上甚至实现帕累托最优（Figure 6），验证了"语义感知块调度"在兼顾质量与效率方面的有效性。

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/016_Table_1.jpg]]
*Table 1: Accuracy (%) across sampling methods, evaluated on LLaDA-1.5, LLaDA-Instruct, and Dream-Base under default block sizes $\bar{B}_$0 $\in \{$16, 32, 64$\}$. Differences are shown in gray. Comparisons are reported relative to Dynamic and +Cache (Wu et al., 2025)

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/017_Table_2.jpg]]
*Table 2: Performance comparison across default block sizes $B_$0$ under a generation budget of $L = 512$. The product of throughput and NFE is nearly identical across methods and block sizes, indicating an approximately inverse relationship between these quantities when no block-wise KV caching is applied. AdaBlock-dLLM yields throughput gains for $B_$0 $\in \{$4, 8$\}$. Boldface indicates superior performance; this convention applies to all tables unless noted otherwise.*

### 性能增益来源：语义感知的块边界

AdaBlock‑dLLM 的增益根源于对固定块边界所引起两类错误的消解：**延迟解码开销**与**过早解码错误**。固定块强制在同一边界处截断语义，使高置信度的词元被推迟、低置信度的词元被提前提交（Figure 1、Figure 7）。这两种情形在采样步骤中占据相当比例——GSM8K 上固定块 B=8 时，延迟解码开销和过早解码错误分别影响约 15% 和 12% 的步骤（Figure 5）。AdaBlock‑dLLM 通过动态选取窗口中置信度最高的分隔符词元（如换行、逗号、句点）作为实际块边界，使块大小自适应地对齐语义步骤（Algorithm 1）。当默认块尺寸较小时，自适应块长度倾向于大于 B₀；默认块较大时则倾向于小于 B₀（Table 2）。这种对齐显著降低了两类错误的发生频率，从而同时提升输出质量与解码效率。

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/011_Figure_5.jpg]]
*Figure 5: Proportion of sampling steps affected by late decoding overhead and premature decoding error on GSM8K and HumanEval for fixed block sizes*

置信度动态分析为该机制提供了基础：LLaDA 的解码过程呈现出**高置信度平台、波动带（VB）和低置信度底层**的三区域结构（Figure 3、Figure 4），波动带宽窄且分布因样本而异，是当前解码步骤的核心发生区。高置信度的分隔符（尤其是换行符）常位于波动带末端，标记局部语义的完成。统计发现，换行符是相邻位置间置信度大幅下降最频繁的词元（Figure 9），因此用它作为块边界具有高可靠性。

### 消融实验：关键设计选择

| 消融维度 | 关键结论 | 证据锚点 |
|---------|---------|---------|
| **分隔符集合** | 单独使用换行符已贡献大部分精度提升（GSM8K 准确率 78.5%），进一步加入逗号和句点将达到最高准确率 **78.7%**（均基于缓存配置）。仅使用逗号或句点效果衰减明显。 | Table 7 |
| **分隔符置信度阈值 τ_D** | 对从头训练的 LLaDA，较低阈值（τ_D=0.3）即可提供足够语义引导，准确率达 **80.59%**；过高阈值（如 0.7）使调度器退化为固定块行为，增益消失。适应型模型 Dream 因波动带方差更大，需更高 τ_D（如 0.5）来提供更强的语义约束（Figure 8）。 | Table 5 |
| **缓存策略** | +Ada 与块级 KV 缓存正交，叠加后进一步提升准确率。例如 B₀=16 时 +Ada+DualCache 达到 81.5%，较仅 DualCache 高出 +1.5%（Table 3）。 | Table 3 |
| **生成长度预算** | 在 L=256、512、1024 三种预算下，+Ada 均一致优于 Dynamic，且组合 Cache 后稳定性更强（Table 4）。 | Table 4 |
| **任务扩展** | 在 IFEval 指令遵循评测上，AdaBlock‑dLLM 同样提升准确率，B₀=64 时 +Ada 带来 **+3.2%** 的提升（Table 6），证实方法的泛化性。 | Table 6 |

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/020_Table_5.jpg]]
*Table 5: Accuracy (%) on GSM8K for LLaDA and Dream across delimiter thresholds $\tau_$D $\in \{$0.3, 0.5, 0.7$\}$ with $B_$0 = 32$. A smaller $\tau_$D$ provides sufficient semantic guidance for dLLMs trained from scratch (e.g., LLaDA).

![[assets/figures/papers/iclr26_0006_0Cv9PwL7cI_AdaBlock-dLLM_Semantic-Aware_Diffusion_LLM_Infer/figures/022_Table_7.jpg]]
*Table 7: Accuracy (%) on GSM8K across eight different delimiter sets with $B_$0 = 32$. Results show that using the newline token ($\n$) as the delimiter accounts for most of the accuracy gains, while additionally including the comma and period further improves performance*

### 失败模式与局限

尽管 AdaBlock‑dLLM 作为无训练推理优化具有即插即用的优势，但仍存在若干局限：

1. **分隔符启发式设计**：分隔符集合（如换行、逗号、句点）和阈值 τ_D 需手动设定，缺乏自动化选取机制。不同模型的最佳 τ_D 不同（LLaDA 宜低，Dream 宜高），增加了调参开销。
2. **语义边界推断的脆弱性**：方法仅通过置信度动态间接捕捉语义边界，未显式建模语义结构。在复杂、多义或高度非自回归的生成场景中，波动的置信度可能使得分隔符无法准确标记步骤终点，导致边界失准。
3. **吞吐量增益受限**：吞吐量提升主要出现在较小默认块（B₀=4,8）下；当 B₀≥32 时，自适应块长度带来的加速效果不明显，有时甚至略低于固定块（Table 2）。
4. **适应型模型的高方差**：对于 Dream 等适应型模型，波动带内置信度方差更大（Figure 8），需更高 τ_D 才能抑制错误的提前解掩码，但过高的 τ_D 可能使调度器频繁回退到默认块行为，削弱自适应优势。

### 关键图表结论速览

- **Table 1 & Table 2**：AdaBlock‑dLLM 在几乎不牺牲吞吐量的前提下，为多模型多块尺寸带来最高 +6.2% 的准确率增益，并在小默认块下获得额外吞吐量加速。
- **Figure 5**：固定块导致的延迟解码开销与过早解码错误占采样步骤的显著比例，量化了固定边界的代价。
- **Figure 1 & Figure 7**：通过真实案例展示两类错误的发生机理，以及 AdaBlock 如何通过语义边界截断来规避。
- **Table 7 & Table 5**：消融证实换行符是最具信息量的分隔符，且合理的阈值范围对释放语义引导至关重要。
- **Figure 6**：AdaBlock‑dLLM 在 LLaDA‑Instruct 的准确率‑吞吐量前沿上实现了帕累托最优，表明语义感知调度兼具高质与高效。

## 方法谱系与知识库定位

AdaBlock-dLLM 作为面向扩散大语言模型（dLLM）的半自回归解码策略，直接建立在 Fast-dLLM（Wu et al., 2025）所引入的置信度动态采样与块级 KV 缓存框架之上。Fast-dLLM 采用固定块大小（B₀）执行半自回归解码，其核心瓶颈已由本文明确揭示：在解码过程中，高置信度词元因块边界限制而被推迟解码（延迟解码开销），低置信度词元则被迫在当前块内提前提交，引发错误传播（过早解码错误）。在 GSM8K 和 HumanEval 上，这两个问题占据了大量采样步骤（Figure 5）。AdaBlock-dLLM 将基线方法中的固定 `block_size`（B₀）替换为由当前预测置信度最高的语义分隔符位置决定的自适应值，从而在不修改模型权重的前提下实现推理时语义感知的块调度（Algorithm 1）。因此，其与 Fast-dLLM 的关系是 **无训练、即插即用的改进**，继承了原有动态采样与缓存机制，仅改变块边界决策逻辑。

从知识库定位看，该工作属于扩散语言模型推理优化的第一环。与 Vanilla dLLM（LLaDA 线性调度）相比，AdaBlock-dLLM 集成了动态采样和块调度双层策略，显著提升了准确率‑吞吐量帕累托前沿（Figure 6）。在主流基准上，其相对于 Fast-dLLM 的准确率提升最高可达 5.3%（Figure 2），且在吞吐量上几乎无额外开销（特别是默认块大小 B₀=4 时吞吐量增益达 51.3 TPS，Table 2）。值得注意的是，该方法在 LLaDA 家族（从头训练的 dLLM）上获益更大，因为其波动带（VB）方差较低，置信度平台扩展更有规律，从而对语义边界的推断更稳定（Figure 3, 4）。然而，对于适应型扩散模型（如 Dream‑Base），其波动带方差显著升高（Figure 8），迫使调度器需要更高的分隔符置信度阈值 τ_D（Table 5），这增加了跨模型调参的负担，也暗示了方法对底层模型全局自回归性强度的敏感度。

**适用边界**主要体现在两个方面。  
- **模型假设**：AdaBlock-dLLM 依赖扩散语言模型的去噪预测具有置信度局域性——dLLM 在局部语义结构完整的区域展现出更高置信度（Section 4.1），且解码过程呈现全局自回归倾向。当模型不具备这一性质（例如方差极高、置信度平台不明显）时，调度器的块大小可能频繁退化回固定值，削弱自适应收益（要求更高的 τ_D）。  
- **任务特性**：该方法将换行符、逗号、句点作为语义分隔符，根据 GSM8K 和 HumanEval 上置信度下降统计，换行符是最频繁导致大幅度置信度下降的词元（Figure 9），因而在代码、数学推理等强结构化生成任务上表现优异。但在文本连贯性要求高、标点与内容边界不一致的复杂多义场景（如长句内微妙转折），仅凭标点符号推断语义边界可能引入错误，论文未提供此类场景的专门验证。

**局限性与后续工作**  
论文明确承认以下局限（Section 5.4）：
1. 分隔符集合与阈值 τ_D 依赖**启发式手动设定**，尚未实现自动化选择。后续需探索数据驱动或自适应的分隔符选取机制。
2. 吞吐量增益主要集中在较小默认块大小（B₀=4, 8），在大块情形下提升不明显，限制了在极低延迟场景下的加速幅度。
3. 方法仅利用置信度动态**隐式推断**语义边界，缺乏对语义结构的显式建模，可能在复杂多义叙事中失效。
4. 当面对与 LLaDA 系列差异较大的 dLLM（如 Dream）时，需要独立调整阈值，增加了部署维护成本。

**开放问题**  
围绕语义感知调度与扩散语言模型的深度融合，本工作引出以下开放方向：
- **训练‑调度联合设计**：能否将自适应块边界思想融入训练目标，通过波动带感知的正则化强化解码过程中的语境连贯性？（相关联于问题列表的第二个问题）
- **自动化分隔符学习**：如何自动学习分隔符集合及其对应的置信度阈值，避免人工标注和跨模型手工调参？（直接对应论文提出的"automating the choice of delimiter tokens and their associated threshold"）
- **更广泛的语义边界信号**：除标点外，能否利用更丰富的语言学单元（如依存句法边界、语义组块）来提升块调度精度？这需要结合额外的知识源或预测头。

最后，论文未专门讨论伦理公平性议题。鉴于 AdaBlock-dLLM 不改变模型本身的参数与训练数据，其公平性表现完全取决于底层预训练扩散模型，在敏感应用场景下需单独评估。"无训练、即插即用"的特性使其可直接叠加于任何现有 dLLM，但同时也意味着它不能修复底层模型存在的偏差。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AdaBlock_dLLM_Semantic_Aware_Diffusion_LLM_Inference_via_Adaptive_Block_Size.pdf

![[paperPDFs/ICLR_2026/AdaBlock_dLLM_Semantic_Aware_Diffusion_LLM_Inference_via_Adaptive_Block_Size.pdf]]
