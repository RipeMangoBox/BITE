---
title: "ABBA-Adapters: Efficient and Expressive Fine-Tuning of Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ABBA_Adapters_Efficient_and_Expressive_Fine_Tuning_of_Foundation_Models.pdf
aliases:
- AA
- ABBA-Adapters
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "将Hadamard乘积与冻结的预训练权重解耦，并使乘积两侧均为独立可学习的低秩矩阵，在保持参数效率的同时显著提升更新的有效秩。"
primary_logic: "更新矩阵可以表示为两个独立优化的低秩矩阵的逐元素乘积，从而获得高秩更新（有效秩最高可达秩的乘积），且参数量仍与标准LoRA相当。"
claims:
- "ABBA在常识推理和算术推理基准上均达到最优，显著超过现有PEFT方法。"
- "在矩阵重建任务中，ABBA的重建误差始终低于LoRA。"
- "通过Khatri–Rao分解，ABBA可在不构建全秩矩阵的情况下实现高效前向/反向传播，内存开销与LoRA相当。"
- "COMMONSENSE170K (Llama-3.2 1B, 八项任务平均) 上 Accuracy = 75.03"
---

# ABBA-Adapters: Efficient and Expressive Fine-Tuning of Foundation Models

> [!tip] 核心洞察
> 更新矩阵可以表示为两个独立优化的低秩矩阵的逐元素乘积，从而获得高秩更新（有效秩最高可达秩的乘积），且参数量仍与标准LoRA相当。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ABBA适配器：高效且表达性强的基座模型微调 |
| 英文题名 | ABBA-Adapters: Efficient and Expressive Fine-Tuning of Foundation Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NvSRYp0oaX); [GitHub](https://github.com/CERT-Lab/abba) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | ABBA-Adapters |
| Dataset | COMMONSENSE170K (Llama-3.2 1B, 八项任务平均), COMMONSENSE170K (Llama-3.2 3B, GSM8K (Mistral-7B, 算术推理), MATH (Mistral-7B |

> [!tip] 效果简介
> - COMMONSENSE170K (Llama-3.2 1B, 八项任务平均) 上，Accuracy 为 75.03，对比 Full Fine-Tuning 74.17，变化 +0.86。
> - COMMONSENSE170K (Llama-3.2 3B, 八项任务平均) 上，Accuracy 为 84.08，对比 Full Fine-Tuning 82.39，变化 +1.69。
> - GSM8K (Mistral-7B, 算术推理) 上，Accuracy 为 66.26，对比 LoRA ~64.06 (best LoRA variant)，变化 +2.20。

## 概述

本文提出 **ABBA‑Adapters**，一种面向基座模型的高效参数微调范式，旨在突破标准低秩适配方法在表达能力上的固有限制。现有低秩适配（如 LoRA）将权重更新约束在低维子空间内，当目标更新为高秩或与预训练权重结构不一致时，难以充分捕捉所需的变换。ABBA 将权重增量重新参数化为 **两个独立可学习的低秩矩阵的 Hadamard 乘积**，使有效秩可达两个成分秩的乘积，从而在参数量与标准 LoRA 相当的前提下获得明显更高的表达能力。

该方法的核心技术路径包括：将 Hadamard 乘积与冻结的预训练权重解耦以换取完整的可学习自由度；利用 **Khatri–Rao 分解**在不物化全秩矩阵的情况下实现高效的前向/反向传播，使显存开销与 LoRA 基本持平；以及基于截断 SVD 的非对称初始化策略结合秩稳定缩放因子，确保训练稳定和收敛速度。

在实验层面，ABBA 在多项基准上取得了显著且一致的性能优势：
- 常识推理（COMMONSENSE170K）上平均准确率超越全量微调和全部对比 PEFT 方法，在 Llama‑3.2 1B/3B 上分别领先全量微调 **+0.86** 和 **+1.69** 个百分点（Table 1）。
- 算术推理（GSM8K 和 MATH）上超过最强 LoRA 变体，在 Mistral‑7B 上分别达到 **66.26** 和 **18.08**（Table 2）。
- 代码生成（HumanEval）上同样优于全量微调及 LoRA，在 Llama‑3.2 1B 上 Pass@1 领先 **+4.88**（Table 11）。

消融实验进一步验证了截断 SVD 初始化、对称秩分配以及 α∈[16,32] 的缩放因子是性能最优配置，而链式堆叠更多适配器对则未见收益甚至导致下降（Table 7）。总体而言，ABBA 在保持 LoRA 级参数和计算效率的前提下，有效提升了基座模型微调的容量上限。

*论文未涉及公平性、偏见或社会影响的专门评估，相关结论的可推广性需在具体场景中另行校验。另外，由于 Figure 1（右侧）和 Figure 2 等视觉证据仅提供摘要信息而未在分析数据中给出完整数值，此处的相应论断可根据论文正文进行手动核验。*

## 背景与动机

大语言模型等基础模型的全量微调因显存与算力开销巨大而难以推广，参数高效微调（PEFT）通过仅学习少量新增或修改的权重适配器，成为实际部署的主流范式。其中最广泛采用的形式是低秩适配器，它将权重增量ΔW参数化为两个低秩矩阵的乘积：ΔW = s B A （LoRA）。这种低秩约束大幅削减了可训练参数量，但天然地将更新限制在低维子空间内，当目标任务需要高秩变化或更新方向与预训练权重结构不一致时，表达能力出现瓶颈。

已有工作 HiRA 通过将低秩乘积与冻结的预训练权重做 Hadamard 乘积（ΔW = W₀ ⊙ (B A)），一定程度上提升了有效秩，但其更新仍受限于与固定权重的外积耦合，参数化本身无法完全脱离低秩假设。在矩阵重建实验中（Figure 2），LoRA 的重建误差高，表明典型低秩分解难以捕捉多种矩阵结构；HiRA 虽有改善，但未从参数化层面彻底解决秩受限问题。

本文的核心动机是：能否设计一种参数效率与 LoRA 相当、同时具备高秩表达能力的微调形式？ABBA 给出的回答是将单个低秩乘积扩展为两个独立可学的低秩矩阵的 Hadamard 乘积。这种参数化将权重增量表示为 ΔW = s (B₁A₁) ⊙ (B₂A₂) ，其中 B₁A₁ 和 B₂A₂ 各自为低秩矩阵，其逐元素乘积天然具有远高于单个分量的秩（有效秩可达两秩乘积量级）。由此，ABBA 在参数预算相当时获得了高秩更新能力，且通过 Khatri‑Rao 分解在实现层面完全避开了显式构造全秩矩阵，保持了与 LoRA 相当的内存效率。玩具实验（Figure 1）直观展示出这一参数化在损失曲面上的优化优势：从源任务向新类别迁移时，ABBA 收敛更快并达到更优的最终性能，暗示其在拟合高秩目标时具有更健壮的优化特性。

综上，ABBA 的动机在于突破低秩瓶颈，在可学习的 Hadamard 框架下实现**高效的宽秩表达**——既保留参数高效微调的轻量优势，又显著提升对复杂任务适配的表达力。

## 核心创新

ABBA-Adapters 解决的核心瓶颈是标准低秩适配（LoRA）的表达能力限制：LoRA 将权重更新 $\Delta W$ 强制约束在低秩子空间内（形式为 $\Delta W = sBA$），当目标任务需要高秩更新或更新方向与预训练权重的本征结构显著偏离时，这一假设直接限制了模型的可塑性和最终性能。

**核心洞察：通过 Hadamard 乘积解耦实现高秩表达。** ABBA 的关键创新在于将权重增量重新参数化为**两个可独立学习的低秩矩阵的 Hadamard 乘积**：

$$
\Delta W = s (B_1 A_1) \odot (B_2 A_2)
$$

这一形式化带来的根本性变化是：尽管每个因子 $B_i A_i$ 仍为低秩，但它们的逐元素乘积可以产生**有效秩高达 $r_1 \times r_2$ 的高秩更新**，且总参数量保持在 $(m + n)(r_1 + r_2)$，与标准 LoRA 可比。在矩阵重建任务中，ABBA 的误差始终显著低于 LoRA（Figure 2），证实了该参数化形式在表达力上的优势。

**关键机制一：与冻结权重的解耦。** 相比前身方法 HiRA（$\Delta W = W_0 \odot (BA)$），ABBA 移除了 Hadamard 乘积对冻结预训练权重 $W_0$ 的依赖，使乘积两侧均成为可学习的低秩矩阵。这一解耦使更新方向不再受 $W_0$ 结构的有偏约束，而是允许两对适配器在梯度下降中自由协调，覆盖更丰富的方向空间。

**关键机制二：Khatri–Rao 分解下的内存等效性。** 高秩物化（$m \times n$ 全秩矩阵）在显存上并不可行，但 ABBA 通过 Khatri–Rao 乘积重构前向传播，避免了全量构造：

$$
B_{\text{kr}} = B_1 \odot_r B_2,\quad A_{\text{kr}} = (A_1^\top \odot_r A_2^\top)^\top,\quad \Delta W x = B_{\text{kr}}(A_{\text{kr}} x)
$$

这使 ABBA 在训练时的显存开销与 LoRA 相当（Figure 4），训练时间仅增加 2–3%（Table 10），却享有显著更高的有效秩。

**关键机制三：初始化策略与秩稳定缩放。** 初始化和缩放方式对训练稳定性和最终性能至关重要（二者构成区别于 LoRA 的关键 changed slots）：

1. **初始化：** 第一对适配器 $B_1, A_1$ 由 $W_0$ 的 $r_1$‑秩截断 SVD 初始化（$B_1 \gets U_{r_1} \Sigma_{r_1}^{1/2}, A_1 \gets \Sigma_{r_1}^{1/2} V_{r_1}^\top$），第二对 $B_2, A_2$ 采用零与 Kaiming 均匀初始化。若两对适配器的 $B$ 均初始化为零，所有梯度将恒为零，导致训练完全失败。截断 SVD 提供的信息引导使 ABBA 在算术推理上超越其他初始化方案（GSM8K 66.26 vs. 次优方案，Table 3）。
2. **缩放因子：** 理论分析表明，为保持梯度范数在不同秩下的稳定性，缩放因子应取 $s \in \Theta(1/\sqrt{r_1 r_2})$，据此 ABBA 将缩放定义为 $\alpha^2 / \sqrt{r_1 r_2}$。超参数 $\alpha$ 的最优范围在 16–32（Table 4, Table 8），过大会导致性能衰退。

**实证强度评估：** ABBA 在多个基准上达到最优或与全量微调可比。在 Llama-3.2 1B/3B 的 COMMONSENSE170K 八任务平均上，ABBA（75.03 / 84.08）相较全量微调（74.17 / 82.39）增益 +0.86 / +1.69（Table 1）；在 Mistral-7B 上，GSM8K 达 66.26，超过最优 LoRA 变体约 +2.2 点（Table 2, Table 9）；HumanEval 代码生成上 Pass@1 为 25.61，高于全量微调的 23.17 和 LoRA 的 20.73（Table 11）。消融进一步确认对称秩分配 $r_1 = r_2 = r/2$ 在固定参数量下有效秩最大且准确率最优，而链式扩展（4 对适配器）反降性能（GSM8K 64.84 vs. 66.26），提示两对设置已足够。

**变更槽位总结：** ABBA 相对于 LoRA 的关键变更集中在四个维度：权重更新参数化形式（Hadamard 乘积双低秩 vs. 单低秩乘积）、初始化策略（截断 SVD + 标准 LoRA 初始化 vs. 全 Kaiming/零初始化）、计算实现（Khatri–Rao 分解避免全秩物化）、以及缩放因子（秩稳定 $\alpha^2 / \sqrt{r_1 r_2}$ vs. 简单 $\alpha/r$）。这四项设计协同实现了“低秩参数开销 + 高秩表达能力 + 训练稳定性”的三角平衡，构成了 ABBA 相较现有 PEFT 方法的核心优势。

## 整体框架

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/002_Figure_1.jpg]]
*Figure 1: Left: Illustration of ABBA's parameterization, where the update is expressed as the Hadamard product of two learnable low-rank matrices. Right: A toy experiment demonstrating ABBA's optimization behavior. We first train a 2-layer MLP to classify the first 8 MNIST digits, then fine-tune it to recognize the last 2. ABBA converges faster and achieves better final performance*

ABBA-Adapters 的核心设计是将权重增量参数化为两个独立可学习的低秩矩阵的 Hadamard 乘积，在保持参数效率的同时获得远高于标准低秩适配（LoRA）的有效秩。整体 pipeline 围绕“解耦 Hadamard 乘积 + 截断 SVD 初始化 + Khatri–Rao 高效计算 + 秩稳定缩放”四个机制展开，以适配器形式插入 Transformer 的各主要线性投影。

**参数化形式**：对于每个需要微调的线性层 $W_0 \in \mathbb{R}^{m \times n}$，ABBA 将增量 $\Delta W$ 建模为
$$
\Delta W = s \,(B_1 A_1) \odot (B_2 A_2),
$$
其中 $B_1 \in \mathbb{R}^{m \times r_1}, A_1 \in \mathbb{R}^{r_1 \times n}$ 和 $B_2 \in \mathbb{R}^{m \times r_2}, A_2 \in \mathbb{R}^{r_2 \times n}$ 是两组可训练的低秩矩阵，$s$ 为缩放因子。Hadamard 乘积 $\odot$ 将两个低秩矩阵的产物逐元素相乘，使得 $\Delta W$ 的有效秩可达 $r_1 r_2$（远大于 LoRA 的秩上限 $r$），而可训练参数总量仍近似于秩 $r_1 + r_2$ 的 LoRA。这种构造从表达力上突破了 LoRA 的低维子空间限制，尤其适于目标更新为高秩或与预训练权重结构不一致的场景。

**初始化策略**：第一组适配器 $(B_1, A_1)$ 利用预训练权重 $W_0$ 的截断 SVD 进行初始化——对 $W_0$ 做秩 $r_1$ 截断 SVD 得 $U_{r_1} \Sigma_{r_1} V_{r_1}^\top$，然后赋值 $B_1 \gets U_{r_1} \Sigma_{r_1}^{1/2}$，$A_1 \gets \Sigma_{r_1}^{1/2} V_{r_1}^\top$。第二组适配器 $(B_2, A_2)$ 则采用 LoRA 风格的初始化：$B_2 \gets \mathbf{0}$，$A_2$ 用 Kaiming 均匀分布初始化。这种非对称初始化既保留了预训练知识的方向信息，又保证训练初期更新从零开始，避免 Hadamard 乘积带来的零梯度陷阱。

**高效前向/反向传播**：尽管 $\Delta W$ 形式上为全秩，但通过 Khatri–Rao 乘积重写，可以完全避免存储 $m \times n$ 矩阵。定义 $B_{\text{kr}} = B_1 \odot_r B_2$（对列做 Khatri–Rao 乘积），$A_{\text{kr}} = (A_1^\top \odot_r A_2^\top)^\top$，则
$$
\Delta W x = B_{\text{kr}} (A_{\text{kr}} x)
$$
该计算仅需与 LoRA 相当的浮点运算和显存，不会物化完整的增量矩阵，从而保持与标准 LoRA 几乎相同的推断和训练开销。

**插入位置与数据流**：ABBA 以适配器形式并联到每个目标线性层的输出。对于输入 $x$，计算流程如下：
1. 冻结的原始投影 $h_0 = W_0 x$。
2. 两个低秩分支分别计算 $u_1 = B_1 (A_1 x)$，$u_2 = B_2 (A_2 x)$。
3. Hadamard 乘积与缩放：$\Delta h = s \cdot (u_1 \odot u_2)$。
4. 最终输出 $h = h_0 + \Delta h$（或等价地 $W_0 x + \Delta W x$）。

实践中，所有适配器均插入 Transformer 的关键位置：注意力层的 Query、Key、Value、Output 投影，以及前馈网络的 Up、Gate、Down 投影。所有适配器共享同一架构，但每层拥有独立的参数。

**秩稳定缩放**：为使梯度范数在改变秩时保持稳定，论文推导出缩放因子应满足 $s \in \Theta(1 / \sqrt{r_1 r_2})$。实际采用的参数化为
$$
s = \frac{\alpha^2}{\sqrt{r_1 r_2}},
$$
其中 $\alpha$ 为类似 LoRA 的可调缩放超参数，典型最优范围在 16–32。这一缩放与对称秩分配 $r_1 = r_2 = r/2$ 共同保证了训练稳定性和高有效秩。

整体而言，ABBA-Adapters 通过“Hadamard 乘积解耦 + 截断 SVD 初始化 + Khatri–Rao 高效实现 + 秩稳定缩放”形成一套紧凑的微调方案，在参数效率与 LoRA 持平的前提下，显著提升了更新的秩容量与优化轨迹（如玩具实验中 ABBA 收敛更快并达到更高最终精度），从而在常识推理、算术推理和代码生成等任务上稳定超越现有 PEFT 方法。

## 核心模块与公式推导

ABBA‑Adapters 将低秩适配的“瓶颈”从单一的低维矩阵乘积扩展为两个独立学习低秩矩阵的 Hadamard 乘积，从而在相同参数量下获得显著更高的有效秩，且仍可通过 Khatri–Rao 分解以与 LoRA 相当的计算与内存开销完成前向传播。下面给出该方法的关键公式及其变量含义；所有公式均来自论文原文推导，未做任何外推。

### 1. 基础低秩适配回顾

标准 LoRA 将权重增量参数化为两个低秩矩阵的乘积：

$$
\Delta W = s\,B A
$$

其中 $W_0 \in \mathbb{R}^{m \times n}$ 是冻结的预训练权重，$B \in \mathbb{R}^{m \times r}$、$A \in \mathbb{R}^{r \times n}$ 为可学习矩阵，$s$ 为缩放因子（通常 $s = \alpha / r$）。该形式将更新限制在秩至多为 $r$ 的子空间内。

HiRA 通过将低秩更新与预训练权重做逐元素乘积（Hadamard 乘积）来提升有效秩，但保留了与 $W_0$ 的绑定：

$$
\Delta W = W_0 \odot (B A)
$$

### 2. ABBA 的核心参数化

ABBA 将 Hadamard 乘积的两个因子均替换为可独立学习的低秩乘积，从而彻底解耦与预训练权重的直接绑定，并使得更新矩阵的有效秩可达 $r_1 r_2$：

$$
\Delta W = s\,(B_1 A_1) \odot (B_2 A_2) \tag{3}
$$

- $B_1 \in \mathbb{R}^{m \times r_1}$，$A_1 \in \mathbb{R}^{r_1 \times n}$ 构成第一对低秩矩阵；
- $B_2 \in \mathbb{R}^{m \times r_2}$，$A_2 \in \mathbb{R}^{r_2 \times n}$ 构成第二对低秩矩阵；
- $s$ 为全局缩放因子，其最优取值由秩稳定分析（见下文）决定；
- $\odot$ 表示逐元素乘积（Hadamard 乘积）。
- 当采用对称秩分配 $r_1 = r_2 = r/2$ 时，参数量与秩为 $r$ 的标准 LoRA 完全相同，但有效秩理论上可达 $r^2/4$。

该参数化是 ABBA 的核心创新：它将低秩表达能力的瓶颈从单个低秩矩阵的乘积转移到两个独立优化的低秩因子之间的交互，从而在不增加参数量的前提下大幅提升更新矩阵的表达能力。

### 3. 初始化策略

为了在训练初期保留与预训练权重一致的信息流向，第一对适配器通过截断 SVD 直接继承 $W_0$ 的结构，第二对保持标准的 LoRA 型零‑Kaiming 初始化：

$$
U_{r_1}, \Sigma_{r_1}, V_{r_1}^\top = \operatorname{SVD}_{r_1}(W_0) \tag{4}
$$

$$
B_1 \gets U_{r_1} \Sigma_{r_1}^{1/2}, \quad A_1 \gets \Sigma_{r_1}^{1/2} V_{r_1}^\top, \quad B_2 \gets \mathbf{0}, \quad A_2 \sim \mathcal{N}(0,\sigma^2) \tag{5}
$$

其中 $\sigma^2$ 由 Kaiming 均匀分布确定。这一混合初始化保证了首轮更新时 $\Delta W = 0$（因为 $B_2 = 0$），模型输出与冻结的预训练模型严格一致，同时第二对适配器的梯度正常流动，避免零梯度导致的训练失败。

### 4. 内存高效计算 (Khatri–Rao 分解)

直接计算式 (3) 会生成一个完整的 $m \times n$ 矩阵，破坏参数效率。利用 Khatri–Rao 乘积（列对列的 Kronecker 乘积）可将更新巧妙地重写为 LoRA 样式的双因子形式，而无需物化全秩矩阵：

$$
B_{\text{kr}} = B_1 \odot_r B_2, \qquad
A_{\text{kr}} = (A_1^\top \odot_r A_2^\top)^\top \tag{Theorem 1}
$$

其中 $\odot_r$ 表示 Khatri–Rao 乘积（按列配对做 Kronecker 乘积）。对于任意输入 $x$，更新可高效计算为

$$
\Delta W\,x = B_{\text{kr}} (A_{\text{kr}} x)
$$

这意味着前向传播只需存储低秩因子 $B_1, B_2, A_1, A_2$ 并按上述形式执行两次矩阵乘法，内存与计算开销与同秩 LoRA 严格可比较，显著低于需要对 $W_0$ 做逐元素乘积的 HiRA。

### 5. 秩稳定性与超参数缩放

当总可训练参数量固定但秩分配变化时，前向传播的数值尺度以及反向传播的梯度范数可能剧烈波动。论文证明了使前向/反向二阶矩与秩无关的缩放因子需满足：

$$
s_{\text{ABBA}} \in \Theta\!\left(\frac{1}{\sqrt{r_1 r_2}}\right) \tag{Theorem 2}
$$

据此引入超参数 $\alpha$ 后的最终 ABBA 参数化为

$$
\Delta W = \frac{\alpha^2}{\sqrt{r_1 r_2}} \,(B_1 A_1) \odot (B_2 A_2) \tag{7}
$$

- $\alpha$ 是控制更新幅度的超参数，实际最优范围通常为 $16 \sim 32$；
- 对称分配 $r_1 = r_2 = r/2$ 时，缩放因子退化为 $\alpha^2/(r/2) = 2\alpha^2/r$，形式上与 LoRA 的 $\alpha/r$ 相似，但包含了 Hadamard 乘积带来的额外秩稳定性。

该缩放策略使得 ABBA 在不同秩配置下均能保持稳定的梯度范数，无需针对不同秩手动调参，同时保证了训练初期的数值平稳性。

### 6. 适配器插入位置

ABBA‑Adapters 遵循与 LoRA 相同的插入范式，将可学习的 Hadamard 乘积层并行引入 Transformer 的注意力及前馈子层中的 **所有线性投影**：

- 注意力：Query、Key、Value、Output 投影；
- 前馈网络：Up、Gate、Down 投影。

即对每一个选定的线性层权重 $W_0$，均添加上述形式的侧分支 $\Delta W$，从而在不修改基础结构的情况下完成微调。具体模块选择对性能的影响详见消融实验，但核心公式与计算机制不因插入位置而改变。

## 实验与分析

ABBA‑Adapters 在覆盖常识推理、算术推理和代码生成三个维度的多个基准上表现出持续且一致的增益，其关键优势源于 Hadamard 乘积带来的高阶有效秩，同时通过 Khatri–Rao 分解保持了与 LoRA 相当的计算与内存效率。本节首先展示主要结果，随后通过系列消融实验揭示 ABBA 发挥效力的因果机制与边界条件。

### 主要结果

**常识推理。** 在 COMMONSENSE170K 的八项任务上，ABBA 在 Llama‑3.2 1B 和 3B 两个规模上均超越所有基线 PEFT 方法，并且优于全量微调（Full FT）。以参数效率版本（秩‑32）为例，ABBA 在 1B 模型上取得 75.03% 的平均准确率，较 Full FT 提高 0.86 个百分点；在 3B 上达到 84.08%，领先 Full FT 1.69 个百分点（Table 1）。这一结果支持核心主张：Hadamard 乘积参数化在匹配甚至超过全量微调表达能力的同时，仅需约 2% 的可训练参数。

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/004_Table_1.jpg]]
*Table 1: Comparison of multiple FT methods on Llama-3.2 1B and 3B across eight commonsense reasoning datasets. Best results among PEFT methods are in bold*

**算术推理。** 在 GSM8K 和 MATH 数据集上，ABBA 在 Mistral‑7B 与 Gemma‑2 9B 上均取得最优结果（Table 2）。Mistral‑7B 上 ABBA（秩‑32）的 GSM8K 准确率达到 66.26%，MATH 为 18.08%，相较最佳 LoRA 变体分别高出 2.20 和 0.48 个百分点。当将训练集扩充至 40K MetaMathQA 子集时，这一优势依然保持（Table 6），Mistral‑7B 对应指标提升至 67.04% 和 18.76%。该结果表明，ABBA 的高有效秩对于需要复杂推理链的数学问题具有实际益处。

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/005_Table_2.jpg]]
*Table 2: Comparison of multiple FT methods on Mistral-7B and Gemma-2 9B across arithmetic reasoning benchmarks. Best results among PEFT methods are in bold*

**代码生成。** 在 HumanEval 基准上，ABBA（秩‑32）在 Llama‑3.2 1B 上取得 25.61% 的 Pass@1，显著优于 LoRA 的 20.73%，提升幅度达 4.88 个百分点（Table 11）。在更大的 Llama‑3.1 8B 上进行的对比中，ABBA 同样超过 Full FT（49.39% vs 48.54%），而所有对比的 PEFT 方法均低于全量微调（Table 12）。这说明 ABBA 具备在真实生成任务中替代全量微调的潜力。

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/016_Table_11.jpg]]
*Table 11: Comparison of multiple FT methods across the coding benchmark - HumanEval. Best results among PEFT methods are in bold*

### 消融研究

**初始化策略。** 对第一对适配器 (B₁, A₁) 采用基于预训练权重 W₀ 截断 SVD 的初始化、第二对 (B₂, A₂) 沿用 LoRA 风格初始化（零 + Kaiming 均匀），在 GSM8K 上取得最优 66.26% 的准确率（Table 3）。纯 LoRA 式初始化（两对均用零 + Kaiming）会导致训练失败，原因在于此时所有梯度为 0；而两对均用 SVD 初始化则因过早注入强先验限制学习空间，造成性能下降。这一对比提示：ABBA 需要一侧从预训练知识中继承结构信息，另一侧保留充分的可塑性。

**秩分配。** 在固定总参数预算下，将总秩 r 均匀分配给两对低秩矩阵（即 r₁ = r₂ = r/2）使有效秩 r₁·r₂ 最大化，且实际准确率最高。非对称分配（如 r₁ = 3r/4, r₂ = r/4）会使有效容量向一侧倾斜，表达能力下降。该结果由正文 Section 4.2 报告（置信度：0.9），证实对称结构是最优配置。

**缩放因子 α。** α 的最佳区间为 16–32，过大或过小均致性能退化。在 Llama‑3.2 3B 常识推理任务上，α = 16–32 时平均准确率稳定在 84.0% 左右，而 α = 4 或 α = 64 分别降至约 83.5% 和 83.7%（Table 4）。Mistral‑7B 算术推理实验呈现相同趋势：GSM8K 在 α = 24 时达到峰值 66.26%，α = 64 时下降到 64.26%（Table 8）。这一行为符合秩稳定定理（Theorem 2）的预测——缩放因子必须与秩的乘积的开方成反比才能保持梯度范数稳定，偏离该比例会导致优化不稳定。

**链式 Hadamard 扩展。** 将 ABBA 进一步扩展为四对低秩矩阵的链式 Hadamard 乘积反而使 GSM8K 准确率从 66.26% 降至 64.84%（Table 7）。同时，链式版本的梯度范数更加不稳定（Figure 6）。这说明两对独立学习的乘积已能提供足够的有效秩，更深的乘积链引入了冗余自由度，反而增大优化难度，导致性能下降。

**模块级消融。** 选择性微调实验（Figure 3）表明，对最终性能贡献最大的三个投影模块依次为：Gate 投影、注意力输出投影和前馈 Down 投影；而 Query 和 Key 投影的增益最小。该发现为实际部署中进一步减少可训练参数提供了方向：仅在这些高贡献模块上插入 ABBA 适配器即可接近全模块微调的性能。

**梯度和秩稳定性。** Figure 5 展示了 Mistral‑7B 中不同缩放策略下的梯度范数。当缩放因子取 $s_{\mathrm{ABBA}} = \alpha^2 / \sqrt{r_1 r_2}$ 时，梯度范数几乎不随秩变化，而固定缩放（如 LoRA 风格的 $\alpha/r$）则导致梯度范数随 r 急剧变化。这从经验上验证了 Theorem 2 所保证的秩稳定性，也是 ABBA 能够在不同秩下稳健训练的关键。

**重建能力。** 在合成矩阵重建任务中，ABBA 在相同参数预算下的重建误差始终显著低于 LoRA（Figure 2）。对于多种矩阵类型（均匀、高斯、低秩等），ABBA 均能以更低的误差逼近目标矩阵，且经验上观察到 $\mathcal{E}_{\mathrm{ABBA}, r} \lesssim \mathcal{E}_{\mathrm{LoRA}, 2r}$ 的趋势，间接证明其有效秩接近参数量的平方根而非线性。

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/003_Figure_2.jpg]]
*Figure 2: Empirical Reconstruction Errors. We compare ABBA and LoRA decompositions across various matrix types by measuring reconstruction error $\mathcal{E}$(r)$ under equal parameter budgets. For each LoRA rank r, we set ABBA ranks to $r_$1 = $r_$2 = r/2$ for a fair comparison. ABBA consistently achieves significantly lower reconstruction error than LoRA, across all matrix types*

**训练开销。** ABBA 仅引入约 2–3% 的额外训练时间（Table 10），前向传播通过 Khatri–Rao 分解 $\Delta W x = B_{\text{kr}} (A_{\text{kr}} x)$ 实现，无需构造完整尺寸的权重矩阵，显存消耗与 LoRA 持平（Figure 4）。这一效率使得高秩表达能力的提升几乎零成本。

### 限制与边缘情形

尽管 ABBA 在主流任务上表现优异，实验中仍然观察到几种性能饱和或下降的情形，这可以被视为该方法的“失败模式”边缘：

1. **过高秩的收益递减：** 在 Mistral‑7B 上，总秩从 32 提高到 64 乃至 128 时，GSM8K 准确率从 66.26% 略微退步至 65.26%（Table 9），说明额外的自由度可能导致过拟合或优化困难，并非无限提升。

![[assets/figures/papers/iclr26_0005_NvSRYp0oaX_ABBA-Adapters_Efficient_and_Expressive_Fine-Tuni/figures/014_Table_9.jpg]]
*Table 9: Performance comparison of ABBA on Mistral-7B across varying total rank values r*

2. **极端缩放因子导致退化：** 当 α 超出 16–32 的最佳区间时，性能单调下降，尤其 α 过大（如 64）会显著损害准确率。这是因为过大的缩放打破秩稳定条件，致使梯度爆炸或不稳定。

3. **链式扩展的有害性：** 四对适配器的链式 ABBA 不仅未带来增益，反而降低了性能，提示直接的 Hadamard 乘积链并未有效提升表达能力，可能需探索新的结构化分解方式。

4. **部分模块贡献微小：** Query 和 Key 投影的增益极低，对这些模块应用 ABBA 可能纯属冗余，若不加区分地全部替换将有参数浪费。

需要指出，论文未报告公平性、偏见或社会影响评估，因此上述分析不涉及这类指标。总体而言，ABBA 的优势建立在 Hadamard 乘积解耦所带来的高有效秩之上，而其边缘退化主要源于过参数化和优化不稳定性，这为未来进一步改进指明了方向。

## 方法谱系与知识库定位

ABBA-Adapters 处于低秩适配（Low-Rank Adaptation）研究脉络中的高秩扩展分支。其核心因果关系可概括为：低秩瓶颈 → 双Hadamard乘积解耦 → 高有效秩与参数效率并存 → 多任务性能超越全量微调。

### 与直接基线的关系

**对 LoRA 的根本改进。** LoRA 将权重更新参数化为 $\Delta W = sBA$，其中 $B \in \mathbb{R}^{m \times r}$、$A \in \mathbb{R}^{r \times n}$，有效秩上限为 $r$。当目标更新矩阵实际秩较高或与预训练权重 $W_0$ 的结构偏离较大时，LoRA 的表达力瓶颈成为限制因素。ABBA 不增加参数预算，而将更新重参数化为两个独立低秩矩阵的 Hadamard 乘积：

$$\Delta W = s (B_1 A_1) \odot (B_2 A_2)$$

此形式的有效秩理论上可达 $r_1 \cdot r_2$，在总参数量 $m r_1 + n r_1 + m r_2 + n r_2$ 与 LoRA（$m r + n r$，$r = r_1 + r_2$）相当的条件下，实现了秩的乘积式扩展。矩阵重建实验（Figure 2）提供了直接证据：在等参数预算下，ABBA 的 Frobenius 重建误差 $\mathcal{E}(r)$ 在所有矩阵类型上均显著低于 LoRA，且满足 $\mathcal{E}_{\text{ABBA}, r} \lesssim \mathcal{E}_{\text{LoRA}, 2r}$ 的趋势，意味着用秩 $r$ 的 ABBA 可匹配秩 $2r$ SVD 的重建能力。

**对 HiRA 的超越。** HiRA 的更新形式为 $\Delta W = W_0 \odot (BA)$，通过 Hadamard 乘积将低秩更新与冻结的预训练权重耦合，可提升有效秩。然而其瓶颈在于：乘积一侧为不可学习的 $W_0$，更新自由度仍受单一低秩对 $(B,A)$ 约束。ABBA 的解耦设计使两侧均可学习，自由度翻倍。从优化轨迹看（Figure 1 玩具实验），ABBA 收敛速度与最终性能均优于 HiRA，验证了双侧可学习带来的优化优势。

**与其他 LoRA 变体的关系。** 在 $r=32$ 的公平比较条件下（Table 1、Table 2），ABBA 在常识推理八任务平均和算术推理（GSM8K/MATH）上一致超越 rsLoRA、PiSSA、DoRA、LoRA-Pro 等近期方法，在 Mistral-7B 的 GSM8K 上以 66.26 超出最佳 LoRA 变体约 +2.20 个百分点。参数效率方面，ABBA 在 $r=32$ 时仅引入约 $22.54\text{M}$ 可训练参数，远低于全量微调（$1.24\text{B}$），且训练内存与 LoRA 持平（Figure 4）。

### 计算等价性的理论锚点

ABBA 面临的核心工程挑战是：Hadamard 乘积 $\Delta W = s (B_1 A_1) \odot (B_2 A_2)$ 看似需要先构造完整的 $m \times n$ 中间矩阵才能计算 $\Delta W x$，这将失去低秩分解的效率优势。定理 1 提供了关键解决方案——利用 Khatri–Rao 乘积重写：

$$B_{\text{kr}} = B_1 \odot_r B_2, \quad A_{\text{kr}} = (A_1^\top \odot_r A_2^\top)^\top, \quad \Delta W x = B_{\text{kr}} (A_{\text{kr}} x)$$

这一重构将此问题转换为两个 Khatri–Rao 矩阵的乘积，前向传播完全无需构造完整秩矩阵，从而在数学上精确地匹配了 LoRA 的计算效率。实测训练时间（Table 10）证实该理论：ABBA 在 Mistral-7B 上的训练时间仅比 LoRA 增加约 2–3%（如 $1:18:22$ vs $1:15:55$），非瓶颈级开销。

### 初始化策略的因果作用

ABBA 的双对结构对初始化高度敏感。若采用朴素的 LoRA 风格初始化（两对 $B$ 均置零），所有梯度将归零，训练完全失败（Appendix C）。ABBA 的方案是将初始化与预训练权重的结构对齐：对 $W_0$ 执行 $r_1$ 秩截断 SVD，取 $B_1 \gets U_{r_1} \Sigma_{r_1}^{1/2}$、$A_1 \gets \Sigma_{r_1}^{1/2} V_{r_1}^\top$；第二对采用标准 LoRA 初始化（$B_2 \gets \mathbf{0}$、$A_2 \gets \mathcal{N}(0, \sigma^2)$）。消融实验（Table 3）确认该方案在 GSM8K/MATH 上最优，表明第一对 SVD 初始化提供了合理的更新起点，第二对零初始化保证了微调起始时 $\Delta W = 0$ 的保真性。

### 秩稳定性与缩放律

定理 2 揭示了缩放因子与梯度范数的依秩关系：当 $s_{\text{ABBA}} \in \Theta(1 / \sqrt{r_1 r_2})$ 时，前向/反向传播的二阶矩与秩无关，梯度范数最稳定。论文据此引入超参数 $\alpha$ 并设定 $s = \alpha^2 / \sqrt{r_1 r_2}$，将秩无关行为显式化。实验证实（Figure 5）：该缩放策略在变化秩时梯度范数最平稳。$\alpha$ 的最佳区间为 16–32（Table 4、Table 8），在这一范围内性能鲁棒，过大（$\geq 48$）或过小均导致精度下降。

### 适用边界

**证据覆盖的任务类型。** 强证据集中在三类下游任务：常识推理（COMMONSENSE170K 的八项子任务，Table 1）、算术推理（GSM8K、MATH，Table 2 和 Table 6）、代码生成（HumanEval，Table 11）。在这些设定中，ABBA 的优越性在 Llama-3.2 1B/3B、Mistral-7B、Gemma-2 9B、Llama-3.1 8B 等多个模型尺度上得到跨模型验证。

**秩与参数的饱和行为。** 秩消融（Table 9）显示 Mistral-7B 上 $r = 32$ 为性能峰值（GSM8K 66.26, MATH 18.08），提升至 $r=64$ 或 $128$ 时收益递减甚至轻微退化。这表明有效秩的乘积式扩展在中等秩区间已足够捕获任务更新，更高秩可能引入冗余自由度或增加优化难度。

**模块选择性的实践指导。** 选择性微调分析（Figure 3）表明：Gate、Output、Down 投影对性能贡献最大，Query、Key 贡献最小。该结果指示在实际部署中可将适配器优先插入高贡献模块以获得更高效的参数利用率。

### 局限与开放问题

**链式扩展的失败。** 将 ABBA 扩展为四对矩阵（"chained" 变体）在 GSM8K 和 MATH 上反而下降（Table 7：GSM8K 64.84 vs 66.26），且梯度范数更不稳定（Figure 6）。这表明双对结构已捕获核心表达力增益，简单堆叠无法线性扩展收益，更深层的 Hadamard 链式分解的优化动力学尚未被理解。

**公平性与社会影响评估的缺失。** 论文未涉及任何公平性、偏见或社会影响方面的专门评估。该缺口使得在敏感应用场景中的行为未知，需用户在部署前自行完成额外的审计。

**闭式解的缺失。** Appendix B 明确指出：由于 Hadamard 乘积破坏了正交不变性且因子位于 Segre 簇上，ABBA 重构问题不存在类似截断 SVD 的闭式解，优化仅可通过梯度下降等迭代方法进行。这意味着实际的收敛质量依赖于优化器和超参数的选择，缺乏类似 SVD 的最优性保证。

**超参数敏感性的未解边界。** $\alpha$ 的最佳范围虽被实证确定，但其与模型结构、任务复杂度之间的关系未获理论分析。不同模型尺度下是否需调整 $\alpha$ 的最佳区间，以及该缩放律在更广泛的 Transformer 组件（如 cross-attention）中是否持有，均为开放问题。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/ABBA_Adapters_Efficient_and_Expressive_Fine_Tuning_of_Foundation_Models.pdf

![[paperPDFs/ICLR_2026/ABBA_Adapters_Efficient_and_Expressive_Fine_Tuning_of_Foundation_Models.pdf]]
