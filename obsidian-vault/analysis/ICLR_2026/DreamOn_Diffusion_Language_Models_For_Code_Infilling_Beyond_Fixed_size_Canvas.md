---
title: "DreamOn: Diffusion Language Models For Code Infilling Beyond Fixed-size Canvas"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DreamOn_Diffusion_Language_Models_For_Code_Infilling_Beyond_Fixed_size_Canvas.pdf
openreview_forum_id: EQTPmqukiU
aliases:
- DreamOn
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "在扩散过程中引入两个新的特殊状态 [expand] 和 [delete]，使模型在生成时能够自主地扩展或收缩序列长度，无需外部指导或架构改动。"
primary_logic: "通过数据增强构建包含 [expand] 和 [delete] 的辅助序列，并在掩码扩散框架中预测这些状态，模型能端到端地学习长度控制行为。推理时，模型根据自身预测扩展或压缩掩码序列，从而解耦生成质量与初始掩码长度，实现可变长度生成。"
claims:
- "在 HumanEval-Infilling 和 SantaCoder-FIM 上，DREAMON 使扩散基线的平均绝对性能提升了 26.4%。"
- "DREAMON 与 DreamCoder-7B 结合，在 HumanEval-Infilling 多行子集上达到 63.8 Pass@1，与顶级自回归模型相当并超越。"
- "DREAMON 在不同初始掩码长度下保持稳定性能，接近使用真实长度的 Oracle 性能。"
- "删除损失的下权对于防止模型过拟合至关重要；移除损失平衡导致平均 Pass@1 下降至 84.6%。"
---

# DreamOn: Diffusion Language Models For Code Infilling Beyond Fixed-size Canvas

> [!tip] 核心洞察
> 通过数据增强构建包含 [expand] 和 [delete] 的辅助序列，并在掩码扩散框架中预测这些状态，模型能端到端地学习长度控制行为。推理时，模型根据自身预测扩展或压缩掩码序列，从而解耦生成质量与初始掩码长度，实现可变长度生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DreamOn：面向代码补全的突破定长生成扩散语言模型 |
| 英文题名 | DreamOn: Diffusion Language Models For Code Infilling Beyond Fixed-size Canvas |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EQTPmqukiU); [GitHub](https://github.com/DreamLM/DreamOn) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DREAMON |
| Dataset | HumanEval-Infilling single-line, HumanEval-Infilling multi-line, SantaCoder-FIM |

> [!tip] 效果简介
> - HumanEval-Infilling single-line 上，Pass@1 为 92.1，对比 55.5，变化 +36.6。
> - HumanEval-Infilling multi-line 上，Pass@1 为 63.8，对比 43.2，变化 +20.6。
> - SantaCoder-FIM 上，Exact Match 为 79.0，对比 59.3，变化 +19.7。

## 概述

**问题瓶颈**：现有扩散语言模型（DLMs）在代码补全等变长生成任务中存在根本性限制——它们要求输入和输出序列具有相同的固定长度。当预设掩码长度与真实补全长度不匹配时，模型无法动态决定输出长度，导致性能急剧下降。在 HumanEval-Infilling 上，这种长度不匹配使扩散基线的平均性能下降 38%（Table 2）。

**核心机制**：DREAMON 通过在扩散过程中引入两个新的特殊状态 `[expand]` 和 `[delete]`，使模型在生成时能够自主地扩展或收缩序列长度，无需任何外部指导或架构改动。训练阶段通过数据增强构建包含这些特殊令牌的辅助序列，并在掩码扩散框架中端到端地学习长度控制行为；推理阶段则根据模型自身预测动态调整掩码序列长度，从而解耦生成质量与初始掩码长度的依赖关系。

**方法定位**：DREAMON 是一种通用的变长扩散生成方法，可即插即用地应用于各类扩散语言模型。在方法谱系中，它区别于以下基线工作：**Deepseek-Coder-6.7B**（Guo et al., 2024b）、**Qwen2.5-Coder-7B**（Hui et al., 2024）等自回归模型，以及 **LLaDA-8B**（Nie et al., 2025）、**Dream-7B**（Ye et al., 2025）、**DiffuCoder-7B**（Gong et al., 2025b）、**DreamCoder-7B**（Xie et al., 2025）等固定长度扩散模型。

**关键结果**：DREAMON 使扩散基线在 HumanEval-Infilling 和 SantaCoder-FIM 上的平均绝对性能提升 26.4%（Table 1）。具体而言，在 HumanEval-Infilling 单行子集上，DiffuCoder-7B + DREAMON 达到 92.1 Pass@1，较基线提升 36.6 个百分点；在多行子集上，DreamCoder-7B + DREAMON 达到 63.8 Pass@1，与顶级自回归模型相当并有所超越。此外，DREAMON 在不同初始掩码长度下保持稳定性能，接近使用真实长度的 Oracle 性能（Table 2），有效解决了固定长度扩散模型对掩码长度敏感的核心痛点。

## 背景与动机

代码补全（code infilling）是生成式代码模型的核心能力之一，要求在给定的上下文前缀和后缀之间生成语法正确、语义连贯的代码片段。近年来，扩散语言模型（Diffusion Language Models, DLMs）凭借其在非自回归生成中展现的全局一致性和可控性，成为该任务的重要技术路线。然而，现有扩散模型在实际部署中面临一个根本性的瓶颈：**输入与输出序列必须保持相同的固定长度**。

这一约束在变长生成场景下造成了严重的性能退化。以 **DreamCoder-7B**（Xie et al., 2025）为例，当预设的掩码（mask）长度与真实补全长度不匹配时，模型表现急剧下降——在 HumanEval-Infilling 基准上，平均性能下降高达 38%。Figure 1 直观地展示了这一失败模式：掩码过少时，扩散模型缺乏足够的生成空间来容纳有意义的代码逻辑；掩码过多时，模型倾向于过度生成不必要的代码片段，导致语义错误。这种“定长画布”的刚性假设，本质上将生成质量与初始掩码长度的猜测耦合在一起，而真实场景中补全长度往往是未知的。

从方法谱系来看，当前主流的代码补全方案分为两条路径：自回归模型（如 **Deepseek-Coder-6.7B**、**Qwen2.5-Coder-7B**）天然支持变长生成，但缺乏扩散模型在迭代精炼和全局规划上的优势；而扩散模型（如 **LLaDA-8B**、**DiffuCoder-7B**）虽在生成质量上展现出竞争力，却受限于固定长度的掩码扩散框架，无法动态决定输出长度。这一结构性缺口意味着，扩散模型在代码补全任务上的潜力远未释放——问题的关键不在于生成能力本身，而在于缺乏一种原生机制，使模型能够在去噪过程中自主地调整序列长度。

DREAMON 的提出正是针对这一瓶颈。其核心动机在于：**将长度控制从外部超参数转变为模型内部的可学习行为**，使扩散模型在推理时能够根据自身预测动态地扩展或收缩掩码序列，从而解耦生成质量与初始长度假设。这一设计无需任何架构改动，仅通过引入两个特殊状态令牌和相应的训练-推理协议即可实现，为扩散语言模型在变长代码补全任务上的规模化应用铺平了道路。

## 核心创新

DreamOn 的核心创新在于为掩码扩散语言模型（DLM）引入了**原生的可变长度生成能力**，从而破解了现有扩散模型在代码补全等变长任务中因“固定长度画布”导致的性能崩塌。其创新围绕三个紧密耦合的 changed slots 展开。

### 1. 长度控制机制：从固定长度到动态伸缩

现有 DLM（如 **DreamCoder-7B** (Xie et al., 2025)、**DiffuCoder-7B** (Gong et al., 2025b)）的生成范式要求输入与输出序列长度严格相等。这一约束在代码补全场景中造成严重问题：当预设掩码长度与真实补全长度不匹配时，模型要么缺乏足够空间生成完整代码，要么被迫过度生成冗余片段。论文揭示，仅此长度不匹配即可导致 HumanEval-Infilling 上平均性能下降 38%（Table 2）。

DreamOn 通过引入两个专用特殊令牌 **`[expand]`** 和 **`[delete]`** 彻底解除了这一约束（§3.1）。模型在去噪过程中不再被动接受固定长度，而是能够根据自身预测主动扩展或收缩序列：
- 预测 `[expand]` 时，该位置被确定性展开为两个 `[mask]` 令牌，为生成提供额外空间；
- 预测 `[delete]` 时，该位置被移除，实现序列收缩。

这一机制无需任何架构改动，仅通过令牌层面的操作即赋予扩散模型动态长度控制能力。

### 2. 训练目标：带权重的掩码扩散损失

标准掩码扩散损失（式 1）对所有掩码位置一视同仁，无法处理 `[expand]` 和 `[delete]` 令牌在训练信号规模上的不对称性。DreamOn 引入**带权重的训练损失**（式 2），核心在于对 `[delete]` 令牌的损失贡献进行降权：

$$w_n = \frac{\mathscr{N}_{mask}}{\mathscr{N}_{mask} - \mathscr{N}_{delete} + 1} \times \begin{cases} 1, & \text{if } \mathbf{z}_0^n \neq [\text{delete}], \\ \frac{1}{\mathscr{N}_{delete}}, & \text{if } \mathbf{z}_0^n = [\text{delete}]. \end{cases}$$

该权重方案将 `[delete]` 令牌的总损失贡献归一化至与单个 `[mask]` 令牌相当的水平（§3.2）。消融实验证实，**移除损失平衡导致平均 Pass@1 从 90.8 骤降至 84.6**（Table 3），表明若不加以约束，模型会过拟合删除信号，严重损害生成质量。

### 3. 推理过程：自适应去掩码与广播删除

DreamOn 的推理过程（Algorithm 2, §3.3）摒弃了传统的固定掩码调度器，转而采用**自适应去掩码预算 $n$**，直接控制每步去噪的令牌数量。这使模型能够根据当前序列状态灵活调整生成节奏。

为进一步加速长度收敛，DreamOn 设计了**广播删除机制**（§3.4）：一旦模型预测出 `[delete]`，则将该位置右侧所有连续的 `[mask]` 令牌一并消除。这一策略将长度预测从逐令牌决策转化为块级操作，在几乎不影响性能（平均仅下降 0.6%）的前提下，将生成步骤减少约 **2.1 倍**（Figure 4, Table 3）。

### 创新总结

DreamOn 的三个 changed slots 形成完整闭环：数据增强构建包含伸缩信号的辅助序列 → 带权损失平衡伸缩令牌的训练贡献 → 自适应推理实现端到端的变长生成。这套机制使扩散模型首次在代码补全任务上摆脱了对预设长度的依赖，在不同初始掩码长度下均保持接近 Oracle 水平的稳定性能（Table 2, §5.1），为扩散语言模型在变长生成场景的实用化铺平了道路。

## 整体框架

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the augmented diffusion process. Top: the forward augmentation-andnoising procedure maps the input sequence $\mathbf { x } _ { \mathrm { 0 } }$ to an augmented latent $\mathbf { z } _ { 0 }$ containing [expand] and [delete] states, and then applies a standard masked diffusion process over $\mathbf { z } _ { 0 }$ to obtain $\mathbf { z } _ { t }$ and eventually $\mathbf { z } _ { T }$ . Bottom: a single denoising step where [mask] positions in $\mathbf { z } _ { t }$ can be predicted as either regular tokens or special states; [expand] deterministically expands into two [mask] tokens, while [delete] will remove the corresponding position, yielding a new sequence $\mathbf { z } _ { t - 1 }$ wit...

DreamOn 的整体框架围绕一个核心思想展开：在标准掩码扩散语言模型（Masked Diffusion Language Models, DLMs）中引入两个新的特殊状态 `[expand]` 和 `[delete]`，使模型在生成过程中能够自主地扩展或收缩序列长度，而无需任何架构改动或外部指导。整个 pipeline 由四个紧密协作的模块构成：数据增强模块、训练模块、变长生成推理模块，以及作为推理加速器的长度预测器（广播删除）。

### 数据流与模块关系

框架的输入是原始代码序列 $\mathbf{x}_0$，输出是经过长度自适应生成的补全序列。数据流依次经过以下阶段：

1. **数据增强模块** 将原始序列 $\mathbf{x}_0$ 转换为包含 `[expand]` 和 `[delete]` 状态的辅助增强序列 $\mathbf{z}_0$。具体而言，该模块随机将 $\mathbf{x}_0$ 中的若干 token 跨度合并为 `[expand]`，并在序列中随机位置插入 `[delete]` token。这一增强过程是训练阶段的关键前处理步骤，其参数（合并概率 $p_{\mathrm{merge}}$ 和合并调度器类型）直接影响模型对长度控制行为的学习效果。

2. **训练模块** 在增强序列 $\mathbf{z}_0$ 上施加标准的连续时间掩码扩散过程：正向过程中，`[expand]` 和 `[delete]` 总是被映射为 `[mask]`；模型则通过去噪过程学习预测这些特殊状态。训练目标采用带权重的掩码扩散损失（公式 2），其中引入每 token 权重 $w_n$ 对 `[delete]` 的损失贡献进行降权，使其总权重与单个 `[mask]` 相当，从而防止模型过拟合到删除信号。

3. **变长生成推理模块** 从全掩码序列开始，使用自适应去掩码预算 $n$（而非固定的掩码调度器）控制每步去噪的 token 数量。当模型在某个 `[mask]` 位置预测出 `[expand]` 时，该 token 立即确定性展开为两个 `[mask]`；预测出 `[delete]` 时，则移除该位置。这一机制使序列长度随模型预测动态变化，从根本上解耦了生成质量与初始掩码长度的绑定关系。

4. **长度预测器（广播删除）** 作为推理加速器嵌入生成过程：一旦模型预测出 `[delete]`，若其右侧所有 token 均为 `[mask]`，则一次性删除这些连续的掩码 token，使序列长度快速收敛到最终值。该机制在几乎不损失性能的前提下（平均 Pass@1 仅下降 0.6%），将生成步骤数压缩约 2.1 倍。

### 关键设计选择

- **合并调度器**：采用静态与动态逆调度器的 1:1 混合，在各类掩码长度下取得最佳平衡。
- **合并概率**：$p_{\mathrm{merge}} = 0.5$ 时达到最高平均 Pass@1。
- **长度上限**：掩码扩展上限设为 $L_{\max} = 128$，达到后禁用扩展。
- **训练计算量**：仅为基础模型预训练计算量的 0.15%。

## 核心模块与公式推导

### 3.1 数据增强与扩散过程

DREAMON 的核心机制围绕两个特殊状态 `[expand]` 和 `[delete]` 展开。训练前，首先从原始输入序列 $\mathbf{x}_0$ 构建辅助增强序列 $\mathbf{z}_0$：通过调度器将随机令牌跨度合并为 `[expand]`，并在序列中插入 `[delete]` 令牌。随后，在增强序列 $\mathbf{z}_0$ 上施加标准的掩码扩散过程——前向扩散中，`[expand]` 和 `[delete]` 始终被映射为 `[mask]`，模型在去噪阶段需预测这些特殊令牌。

### 3.2 带权重的训练损失

标准掩码扩散损失仅对 `[mask]` 位置计算交叉熵（式 1）。DREAMON 引入针对 `[delete]` 的损失权重下缩方案，防止模型过拟合删除信号。整体训练目标为：

$$\mathcal { L } ( \boldsymbol { \theta } ) = - \mathbb { E } \underset { \underset { \mathbf { t } \sim \boldsymbol { \mathcal { U } } ( \mathbf { \alpha } _ { 0 } | \mathbf { x _ { 0 } } ) } { \mathbf { \alpha } _ { \mathbf { t } \sim \boldsymbol { \mathcal { U } } ( \mathbf { \alpha } _ { 1 } ) } } } { \mathbf { \pi } _ { \mathbf { \mu } \sim \boldsymbol { \mathcal { U } } ( \mathbf { \alpha } _ { 0 } | \mathbf { x } ) } } \left[ w ( t ) \sum _ { n = 1 } ^ { N } \mathbf { 1 } _ { [ \mathbf { z } _ { t } ^ { n } = [ \boldsymbol { \mathrm { m a s k } } ] ] } \cdot w _ { n } \cdot \log p _ { \boldsymbol { \theta } } ( \mathbf { z } _ { 0 } ^ { n } \mid \mathbf { z } _ { t } ) \right]$$

其中 $w_n$ 为每令牌权重，专门对 `[delete]` 令牌的损失贡献进行降权：

$$w _ { n } = \frac { \mathscr { N } _ { m a s k } } { \mathscr { N } _ { m a s k } - \mathscr { N } _ { d e l e t e } + 1 } \times \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f ~ } \mathbf { z } _ { 0 } ^ { n } \neq \mathsf { \ell } [ \mathsf { d e l e t e } ] , } \\ { \frac { 1 } { \mathscr { N } _ { d e l e t e } } , } & { \mathrm { i f ~ } \mathbf { z } _ { 0 } ^ { n } = \mathsf { \ell } [ \mathsf { d e l e t e } ] , } \end{array} \right.$$

变量含义：$\mathscr{N}_{mask}$ 为当前样本中 `[mask]` 令牌的数量，$\mathscr{N}_{delete}$ 为 `[delete]` 令牌的数量。该归一化因子使所有 `[delete]` 令牌的总损失贡献与单个 `[mask]` 令牌相当，确保训练信号的平衡。消融实验证实，移除该损失平衡机制会导致平均 Pass@1 从 90.8% 降至 84.6%（Table 3）。

### 3.3 变长生成推理

推理时，DREAMON 不再依赖固定掩码调度器，而是通过自适应去掩码预算 $n$ 直接控制去噪轨迹。核心流程（Algorithm 2）为：
- 从全掩码序列开始，每步预测 $n$ 个令牌；
- 预测为 `[expand]` 的令牌立即展开为两个 `[mask]`，实现序列扩展；
- 预测为 `[delete]` 的令牌被移除，实现序列收缩；
- 序列长度随模型预测动态变化，直至所有 `[mask]` 被填充。

### 3.4 广播删除（长度预测器）

为加速长度收敛，DREAMON 引入广播删除机制：一旦模型预测出 `[delete]`，若其右侧所有令牌均为 `[mask]`，则一并消除这些 `[mask]` 令牌。该机制将多行补全子集上的平均推理步数从 122.8 步降至 52.4 步（加速约 2.1 倍），而性能仅下降 0.6%（Table 3）。

## 实验与分析

### 核心瓶颈：固定掩码长度导致的性能崩溃

在深入主实验之前，有必要先量化现有扩散语言模型（DLMs）的致命缺陷。实验观察到，当预设的掩码长度与真实补全长度不匹配时，扩散模型在 HumanEval-Infilling 上的平均性能下降高达 **38%**（Table 2）。Figure 1 直观地展示了这一失败模式：掩码过少时，模型缺乏足够的生成空间来完成有意义的代码补全；掩码过多时，模型则倾向于过度生成无关代码片段（如错误的 `depth > 0` 条件）。这一瓶颈构成了 DREAMON 方法设计的核心动机。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/004_Table_2.jpg]]
*Table 2: Infilling performance across different designs for diffusion language models. Oracle: performance with the oracle target length for reference. †: We use an AST parser to compute exact match to normalize huge syntactic differences between the model output and the ground truth*

### 主实验结果

Table 1 汇总了在 HumanEval-Infilling 和 SantaCoder-FIM 两个基准上的核心对比结果。DREAMON 在多个扩散基线模型上均实现了显著且一致的性能提升，**平均绝对性能提升达 26.4%**。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/003_Table_1.jpg]]
*Table 1: Pass@1 on HumanEval-Infilling and exact match on Santacoder-FIM, comparing opensource auto-regressive and diffusion model baselines.The best results across diffusion models are shown in bold, and the second best are underlined*

在 **HumanEval-Infilling 单行子集**上，DREAMON 将扩散基线的 Pass@1 从 55.5 提升至 **92.1**（+36.6），其中 DiffuCoder-7B + DREAMON 的组合达到了 92.2 Pass@1。在多行子集上，DreamCoder-7B + DREAMON 取得了 **63.8 Pass@1**，不仅远超扩散基线（43.2），还超越了多个顶级自回归模型，包括 Deepseek-Coder-6.7B（Guo et al., 2024b）和 Qwen2.5-Coder-7B（Hui et al., 2024）。

在 **SantaCoder-FIM** 上，DREAMON 将精确匹配率从 59.3 提升至 **79.0**（+19.7），进一步验证了该方法在不同补全风格基准上的泛化能力。

值得注意的是，DREAMON 的训练计算量仅为预训练基础模型计算量的 **0.15%**，表明该方法以极低的额外成本实现了大幅性能跃升。

### 长度鲁棒性消融

Table 2 的核心发现是：**DREAMON 在不同初始掩码长度下均保持稳定性能，接近使用真实长度的 Oracle 性能**。在单行补全场景中，无论初始掩码长度如何变化，DREAMON 的 Pass@1 始终维持在 88.7 至 92.1 的窄幅区间内，而固定长度的扩散基线则在掩码长度偏离真实值时出现剧烈波动。

消融进一步揭示，性能增益来源于**掩码扩展与收缩机制的协同作用**。单独启用任一机制均无法达到完整 DREAMON 的性能水平，证实了双向长度控制对于补全任务是不可或缺的。

### 关键设计选择的消融分析

Table 3 和 Figure 5 系统性地检验了 DREAMON 各设计组件的贡献：

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/006_Table_3.jpg]]
*Table 3: Ablation study for mask deletion mechanism implementations*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/012_Figure_5.jpg]]
*Figure 5: (a) Result with different scheduler merging ratio. (b) Result with different merging probability pmerge Figure 5: Performance on single-line subset of HumanEvalInfilling-FIM with different hyperparameters during training. The performance is computed as the average pass@1 with mask length 4, 8, 16, 32 and 64*

**删除损失平衡（Loss Balancing）**：移除对 `[delete]` 令牌的损失降权后，模型平均 Pass@1 从 90.8 骤降至 **84.6**。这一结果表明，若不进行损失平衡，模型会过拟合删除信号，严重损害生成质量。该发现验证了公式（2）和（3）中每令牌权重 $w_n$ 设计的必要性。

**广播删除（Broadcasting Deletion）**：禁用广播删除导致平均性能下降 0.6%（90.2 vs 90.8），但生成过程加速约 **2.1 倍**——在多行补全子集上，掩码长度为 64 时，总推理步数从 122.8 降至 52.4（Figure 4）。这一微小性能代价换来了显著的效率提升，使广播删除成为实用的默认选择。

**掩码合并调度器设计**：Figure 5a 显示，静态与动态逆调度器的 **1:1 混合**在不同掩码长度下取得了最佳平衡。Figure 5b 进一步表明，合并概率 $p_{\text{merge}} = 0.5$ 时单行补全的 Pass@1 达到峰值（约 90.5%），过高或过低的合并概率均导致性能下降。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_EQTPmqukiU/figures/010_Table_4.jpg]]
*Table 4: Rouge-L scores on the ROCStories corpus across variable initial mask lengths*

## 方法谱系与知识库定位

### 扩散语言模型的定长瓶颈与 DREAMON 的定位

现有掩码扩散语言模型（Masked Diffusion Language Models, DLMs）的共同前提是输入和输出序列共享相同的固定长度。这一约束在文本生成任务中尚可通过填充（padding）缓解，但在**代码补全**等需要动态决定输出长度的场景中成为关键瓶颈。当预设的掩码长度与真实补全长度不匹配时，模型性能会出现大幅退化——在 HumanEval-Infilling 上，平均性能下降达 38%（Table 2）。Figure 1 展示了这一失效模式：掩码过少时模型缺乏足够的生成空间，掩码过多时则会产生冗余甚至错误的代码片段。

DREAMON 在这一谱系中的定位是**首个在掩码扩散框架内实现原生可变长度生成的方法**，无需修改模型架构，仅通过引入两个特殊令牌（`[expand]` 和 `[delete]`）和配套的训练-推理机制，使预训练扩散语言模型能够自主控制序列长度。该方法在训练计算量仅为预训练基础模型 0.15% 的条件下，使扩散基线模型的平均绝对性能提升 26.4%（Table 1）。

### 与基线方法的关系

#### 扩散模型基线

DREAMON 直接建立在以下扩散语言模型之上，并显著提升了它们的代码补全性能：

- **DreamCoder-7B**（Xie et al., 2025）：DREAMON 将其在 HumanEval-Infilling 多行子集上的 Pass@1 从 43.2 提升至 63.8（Table 1），达到与顶级自回归模型相当的水平。
- **DiffuCoder-7B**（Gong et al., 2025b）：DREAMON 将其在 HumanEval-Infilling 单行子集上的 Pass@1 从 55.5 提升至 92.2（Table 1），在所有扩散模型中取得最佳结果。
- **LLaDA-8B**（Nie et al., 2025）和 **Dream-7B**（Ye et al., 2025）：作为扩散基线参与对比，DREAMON 同样展现了对其性能的显著提升。

这些基线模型均使用标准掩码扩散损失（式 1）进行训练，在推理时依赖固定的掩码调度器逐步去噪，掩码长度不可变。DREAMON 的核心改动在于将训练目标替换为带权重的损失（式 2），并在推理中引入自适应去掩码预算 $n$ 和序列扩展/收缩操作（Algorithm 2），从而解耦生成质量与初始掩码长度。

#### 自回归模型基线

DREAMON 与以下自回归代码模型进行了对比：

- **Deepseek-Coder-6.7B**（Guo et al., 2024b）
- **Qwen2.5-Coder-7B**（Hui et al., 2024）
- **Seed-Coder-8B**（Seed et al., 2025）

在 HumanEval-Infilling 多行子集上，DreamCoder-7B + DREAMON 以 63.8 Pass@1 超越了 Deepseek-Coder-6.7B（61.3）和 Qwen2.5-Coder-7B（59.0），与 Seed-Coder-8B（64.4）接近（Table 1）。这表明扩散模型在引入动态长度控制后，在代码补全任务上已具备与自回归模型竞争的能力。

### 方法谱系中的关键设计选择

DREAMON 的方法贡献可分解为三个相互依赖的模块，消融实验揭示了各模块的必要性：

1. **数据增强与特殊令牌**：通过合并随机令牌跨度为 `[expand]` 并插入 `[delete]` 构建辅助序列 $z_0$。消融显示，仅使用扩展机制或仅使用收缩机制均无法达到完整的性能增益，二者的组合使用是性能提升的根本来源（§5.1）。

2. **删除损失的下权**：式（3）定义的每令牌权重 $w_n$ 将 `[delete]` 令牌的总损失贡献归一化至与单个 `[mask]` 令牌相当。移除该损失平衡导致平均 Pass@1 从 90.8 降至 84.6（Table 3），证实了防止模型过拟合删除信号的关键性。

3. **广播删除机制**：推理时，一旦预测 `[delete]`，则删除其右侧所有连续的 `[mask]` 令牌。该机制使生成步骤从 122.8 步降至 52.4 步（约 2.1 倍加速），同时性能仅下降 0.6%（Table 3, Figure 4），在效率与质量之间取得了有利的权衡。

### 适用边界

- **任务范围**：DREAMON 在代码补全任务（HumanEval-Infilling、SantaCoder-FIM）上得到了充分验证，并在 ROCStories 文本补全上展示了初步的泛化能力（Table 4）。但其在更广泛生成任务（如开放式文本生成、翻译）上的适用性尚未系统评估。
- **长度上限**：推理时掩码扩展被限制在 $L_{\text{max}} = 128$，扩展次数达到上限后禁用进一步扩展（§4.1）。对于需要更长补全的场景，该方法需要调整超参数或引入多级扩展机制。
- **训练数据依赖**：`[expand]` 的构建依赖于合并调度器（静态与动态逆调度器的 1:1 混合）和合并概率 $p_{\text{merge}} = 0.5$ 的选择（Figure 5），这些超参数可能需要针对不同领域进行调整。

### 局限与开放问题

尽管 DREAMON 在代码补全上取得了显著进展，论文明确指出了以下局限和未来方向：

1. **应用范围的拓展**：当前验证集中在代码补全和有限的文本补全任务上。将 DREAMON 扩展到更广泛的应用场景以评估其通用性是必要的开放问题。

2. **推理效率的进一步优化**：虽然广播删除将生成步骤减少了约 2.1 倍，但扩散模型的迭代生成本质仍使其推理速度落后于自回归模型。论文提出探索更丰富的令牌词汇（如多级扩展因子）或将扩展与显式长度预测头耦合，以减少去噪迭代次数。

3. **更原则性的推理公式**：当前的推理过程（Algorithm 2）依赖于启发式的自适应去掩码预算 $n$ 和广播删除规则。论文指出，为掩码扩散模型中的灵活推理开发更具原则性的公式化方法是一个重要的理论方向。

4. **长度预测的精度**：广播删除机制虽然高效，但在某些情况下可能过度删除（当 `[delete]` 右侧并非全部为 `[mask]` 时不会触发广播）。更精细的长度预测策略（如独立的长度预测模块）可能进一步提升性能，但需要额外的设计复杂度和训练成本。

## 原文 PDF

![[paperPDFs/ICLR_2026/DreamOn_Diffusion_Language_Models_For_Code_Infilling_Beyond_Fixed_size_Canvas.pdf]]
