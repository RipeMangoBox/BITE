---
title: "AbsTopK: Rethinking Sparse Autoencoders For Bidirectional Features"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidirectional_Features.pdf
project_link: null
code_link: null
aliases:
- AS
- AbsTopK
- "AbsTopK SAE"
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "稀疏正则项中隐含的非负指示函数（ι_{z≥0}）强制激活只留正值，直接导致了双向语义的碎片化。开关就是这个非负约束。"
primary_logic: "通过移除非负约束并直接使用ℓ₀稀疏硬阈值（保留绝对值最大的k个分量），AbsTopK让单个潜在特征可以同时携带正、负激活，从而编码双向语义轴，使表示更丰富、更紧凑。"
claims:
- "现有SAE的非负约束使对比性概念被分割成两个独立基，丢弃了语义轴的一个方向。"
- "AbsTopK通过ℓ₀约束的无约束硬阈值保留最大幅值的激活，允许正负共存，从而捕获双向概念。"
- "在Gemma-2-2B第12层，AbsTopK产生29.7%的双向特征，而TopK仅有5.3%，其中相对立含义的比例为20.2% vs 2.6%。"
- "Qwen3-4B, Layer 18 上 MMLU (↑) = 75.9"
---

# AbsTopK: Rethinking Sparse Autoencoders For Bidirectional Features

> [!tip] 核心洞察
> 通过移除非负约束并直接使用ℓ₀稀疏硬阈值（保留绝对值最大的k个分量），AbsTopK让单个潜在特征可以同时携带正、负激活，从而编码双向语义轴，使表示更丰富、更紧凑。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AbsTopK: 重新思考面向双向特征的稀疏自编码器 |
| 英文题名 | AbsTopK: Rethinking Sparse Autoencoders For Bidirectional Features |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EEs6I4cO7S) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | AbsTopK SAE |
| Dataset | Qwen3-4B, Layer 18 |

> [!tip] 效果简介
> - Qwen3-4B, Layer 18 上，MMLU (↑) 为 75.9，对比 77.3 (Original)，变化 -1.4。
> - Qwen3-4B, Layer 18 上，HarmBench (↑) 为 81.3，对比 17.0 (Original)，变化 +64.3。
> - Qwen3-4B, Layer 18 上，SCR (↑) 为 0.35，对比 0.26 (TopK)，变化 +0.09。

## 概要

当前主流稀疏自编码器（ReLU、JumpReLU、TopK）通过非负约束确保激活稀疏，但这一隐含强制丢弃了负激活，导致表示能力被限制：像“男性 ↔ 女性”这样的双向语义轴被强制拆分为两个独立、单向的基向量，且往往丢失一个方向。本文指出，核心瓶颈是非负指示函数 $\iota_{z \ge 0}$，其直接导致双向语义的碎片化。

方法定位：作者提出 AbsTopK SAE，在近端梯度框架下移除上述非负约束，代之以 ℓ₀ 稀疏硬阈值——保留绝对值最大的 $k$ 个分量（保留原符号），使单个潜在特征可同时携带正、负激活，从而编码双向语义轴。该方法保持端到端可微，与现有 TopK 架构兼容，不引入额外监督信号。

核心结论：在 Gemma‑2‑2B 第 12 层，AbsTopK 产生的双向特征占比达 29.7%（其中对对立含义的识别率为 20.2%），远超 TopK 的 5.3%（对立含义 2.6%）。在下游操控任务中，AbsTopK 在所有稀疏度水平下均取得更低重构误差（图 3），并在安全‑效用折中（HarmBench 与 MMLU 同时提升）方面优于所有无监督基线，在多项探针和操控指标（SCR、TPP 等）上达到或超过有监督 Difference‑in‑Means 方法。这些结果表明，移除无根据的非负约束可显著提升稀疏表示的紧凑性和表达能力。



大规模语言模型的内部表征历来难以解释。线性表征假说（linear representation hypothesis）认为，模型的隐藏状态可以分解为潜在概念向量的叠加：

$${\pmb x} = \sum_{p = 1}^{P} \alpha_p {\pmb h}_p \ + \ \mathrm{residual}$$

其中 ${\pmb h}_p$ 是概念方向，$\alpha_p$ 为对应的激活系数。稀疏自编码器（Sparse Autoencoder, SAE）正是基于这一假说，通过字典学习的方式将隐藏表示分解为一组可解释的、稀疏激活的潜在特征。其训练目标可统一写为带有稀疏正则项 $R(\mathbf{z})$ 的字典学习问题：

$$\min_{D \in \mathbb{R}^{d \times P}, b \in \mathbb{R}^{d}} \mathbb{E}_{\mathbf{x}} \left[ \min_{\mathbf{z} \in \mathbb{R}^{P}} \frac{1}{2} \| \mathbf{x} - (D \mathbf{z} + b) \|_{2}^{2} + \lambda R(\mathbf{z}) \right]$$

通过展开近端梯度方法（proximal gradient），SAE 可以用一个单步更新来实现编码器，将输入 $\mathbf{x}$ 映射为稀疏编码 $\mathbf{z}$：

$$\mathbf{z}^{(1)} = \operatorname{prox}_{\lambda R} \big( W^{\top} \mathbf{x} + b_{\mathrm{e}} \big)$$

解码器则从稀疏编码重构原始激活：$\hat{\mathbf{x}} = D \mathbf{z} + b$。

### 现有方法的隐性瓶颈：非负约束导致语义碎片化

主流的 SAE 变体——ReLU SAE、JumpReLU SAE 和 TopK SAE——通过各自的激活策略实现稀疏性，但它们在设计上共同隐含了一个**非负约束**。具体而言：

$$(\mathrm{ReLU}_{\lambda}(\mathbf{u}))_i = \max\{u_i - \lambda, 0\}, \; (\mathrm{JumpReLU}_{\theta}(\mathbf{u}))_i = \begin{cases} 0, & u_i < \theta, \\ u_i, & u_i \geq \theta \end{cases}, \; (\mathrm{TopK}_k(\mathbf{u}))_i = \begin{cases} \max\{u_i, 0\}, & i \in \mathcal{T}_k(\mathbf{u}), \\ 0, & i \notin \mathcal{T}_k(\mathbf{u}) \end{cases}$$

这三种算子中，稀疏正则项隐含的非负指示函数 $\iota_{z \geq 0}$ 强制激活只保留正值。这一设计虽然简化了优化并保证了解的唯一性，却带来了一个严重的表示能力缺陷：**它将语义上对立的双向概念轴（如“男性 vs 女性”、“正向情感 vs 负向情感”）强制拆分为两个独立、单向的潜在特征**。也就是说，一个完整的语义轴无法用一个潜在维度来表示，而是需要占据两倍的特征容量，并且丢失了二者之间的对比关系。

这一缺陷并非理论猜测。论文明确指出：现有的非负 SAE “要么将对比性概念分裂为独立的单向基（如将‘男性’和‘女性’视为两个单独的特征），要么完全丢弃语义轴的一个方向”（*by enforcing non-negativity or retaining only the TopK activations, conventional SAEs either fragment such contrastive concepts into separate, unidirectional bases…or discard one direction of the semantic axis entirely*）。

### 本文动机：移除约束，释放双向表示能力

上述困境的根本原因在于**非负约束充当了一个隐性的“语义拆分开关”**：一旦关闭这个开关（即允许负激活参与稀疏编码），单个潜在特征就可以通过正负两个方向的激活自然地编码一个完整的双向语义轴。图 2（Figure 2）给出了直观示意：当 “man ≈ male + people” 且 “woman ≈ female + people” 时，非负 SAE 需要两个独立的性别特征，而允许负激活的 SAE 只需一个有符号的性别特征。

基于这一洞察，本文的核心动机是：**设计一个真正稀疏、同时保留激活原始符号的 SAE 变体，使其能够在一个潜在维度上捕获双向的对比性概念**。具体而言，本文提出 **AbsTopK SAE**，在 $\ell_0$ 稀疏约束下移除非负性，直接对预激活向量 $\mathbf{u}$ 应用绝对值的硬阈值操作，保留幅值最大的 $k$ 个分量的原值（包括符号）：

$$[\mathrm{AbsTopK}_k(\mathbf{u})]_i = \begin{cases} u_i, & i \in \mathcal{T}_k(|\mathbf{u}|), \\ 0, & i \notin \mathcal{T}_k(|\mathbf{u}|) \end{cases}$$

这一设计的预期收益在于：在同等稀疏度下，AbsTopK 的潜在空间承载更丰富的结构化语义。初步证据显示，在 Gemma-2-2B 第 12 层，AbsTopK 所产生的双向特征占比达到 29.7%，其中含义相对立的特征占 20.2%，而 TopK SAE 的对应比例仅为 5.3% 和 2.6%（Table 2），这直接验证了移除约束的必要性。



## 核心方法与创新机理

AbsTopK 的核心创新在于揭示了现有 SAE 变体（ReLU、JumpReLU、TopK）的一个隐藏瓶颈，并通过一个简洁的 slot 级修改将其消除，从而根本性提升了特征表示的语义密度。

### 瓶颈诊断：非负约束导致语义碎片化

现有 SAE 在追求稀疏性的过程中，无意间引入了一个支配性约束：激活必须非负。从近端梯度展开的视角看，ReLU$_{\lambda}$、JumpReLU$_{\theta}$ 和 TopK$_{k}$ 的稀疏编码步骤均等价于其对应正则项 $R(\mathbf{z})$ 在**附带非负指示函数** $\iota_{\mathbf{z} \ge 0}$ 时的近端算子。这强制编码 $\mathbf{z}$ 只能使用正系数。

这种硬性约束直接导致了一个严重的表示缺陷：一个本应作为单一连续体的双向语义轴（如“男性 ↔ 女性”）被迫拆分为两个孤立的、单向的特征基。一个非负字典无法用一个原子同时表达一个概念的正反两面，因为它“丢弃了表示空间的另一半”。这降低了特征的语义密度，也使后续的操控操作（如通过激活控制转向）变得低效——需要同时干预两个特征，而非仅调节一个特征的符号和强度。

### 关键改变：从“最大正值”到“最大幅值”

AbsTopK 对上述瓶颈的改变是直接且根本的：它移除了隐含在稀疏化步骤中的非负约束。具体的 changed slot 如下：

*   **稀疏激活/近端算子**：将 `TopK_k` (筛选最大正激活) 替换为 `AbsTopK_k` (根据激活的**绝对值**大小，筛选幅值最大的 $k$ 个分量，同时**保留其原始符号**)。

该算子的数学定义极其简洁：

$$ [\mathrm{AbsTopK}_k(\mathbf{u})]_i = \begin{cases} u_i, & i \in \mathcal{T}_k(|\mathbf{u}|), \\ 0, & i \notin \mathcal{T}_k(|\mathbf{u}|) \end{cases} $$

其中 $\mathcal{T}_k(|\mathbf{u}|)$ 是输入 $\mathbf{u}$ 的绝对值最大的 $k$ 个分量的索引集合。这一算子对应于无符号约束下的 $\ell_0$ 稀疏惩罚的近端投影。

这一修改使单个潜在特征能够同时承载正、负激活值，自然地编码整个双向语义轴。例如，一个特征可以通过强正激活表示“男性”输入，通过强负激活表示“女性”输入，而非像 TopK 那样将二者分配给两个不相干的特征。从几何上看，AbsTopK 将特征空间从单纯形（仅第一象限）拓展到了完整空间，使字典学习能够发掘更紧凑、信息更丰富的表示基。

### 创新有效性的直接证据

对特征语义结构的定量分析证实了 AbsTopK 设计意图的成功（Table 2）。在 Gemma-2-2B 的第 12 层，LLM 驱动的自动解释显示，AbsTopK 产生的**双向特征**（即在正、负激活下表达明确含义的特征）比例高达 **29.7%**，而 TopK 仅有 **5.3%**。更重要的是，在双向特征中，具有**相对立含义**（即正负激活代表截然相反的概念）的特征比例，AbsTopK 达到了 **20.2%**，远超 TopK 的 **2.6%**。

这表明，移除符号约束并非简单地保留了更多信息，而是创造了一种全新的、更符合人类认知的特征结构。这种结构上的优势直接转化为下游任务中的因果操控能力。在 Qwen3-4B 第 18 层，AbsTopK 在专门的转向鲁棒性评估任务上显著超越了 TopK（SCR: 0.35 vs. 0.26; TPP: 0.36 vs. 0.31），表明这些紧凑的双向特征让激活空间操控更精准、高效。



![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/002_Figure_2.jpg]]
*Figure 2: Toy example where man ≈ male + people and woman ≈ female + people: a non-negative SAE needs two separate gender features, whereas AbsTopK uses one signed gender feature*

AbsTopK SAE 的整体流程遵循稀疏自编码器的通用范式，即编码器-稀疏激活-解码器三段式管线，其核心创新在于将稀疏激活模块从非负约束改造为基于绝对值幅度的硬阈值。

### 1. 通用架构

框架基于从字典学习目标导出的单步近端梯度编码结构。给定隐藏状态 $\mathbf{x}$，编码器执行线性变换并加偏置以产生预激活：

$$
\mathbf{u} = W^{\top} \mathbf{x} + b_{\mathrm{e}}
$$

其中 $W \in \mathbb{R}^{d \times P}$ 和 $b_{\mathrm{e}} \in \mathbb{R}^{P}$ 是独立于解码字典的可学习参数。这一参数化编码器的设计避开了原始字典学习中困难的非凸优化问题，使得编码过程可高效计算。

随后，稀疏激活模块对 $\mathbf{u}$ 施加近端算子 $\operatorname{prox}_{\lambda R}(\cdot)$，得到稀疏编码 $\mathbf{z}$：

$$
\mathbf{z} = \operatorname{prox}_{\lambda R}(\mathbf{u})
$$

解码器通过线性变换与偏置重构原始激活：

$$
\hat{\mathbf{x}} = D \mathbf{z} + b
$$

端到端训练时同时优化所有参数，损失函数为重构误差与稀疏正则项的组合。

### 2. 稀疏激活模块：从非负到双向

该模块是方法的核心。现有主流 SAE 变体（ReLU$_{\lambda}$、JumpReLU$_{\theta}$、TopK$_k$）的激活函数均隐式包含非负约束，即仅保留正值分量而将负值置零。这一设计使得一个语义轴上对立的概念（如“男性 vs 女性”）必须被拆分为两个独立的非负基向量，导致表示碎片化（Figure 2）。

AbsTopK 通过移除这一非负约束来解决该瓶颈。具体而言，其激活算子定义为保留 $\mathbf{u}$ 中**绝对值最大的 $k$ 个分量**，其余置零，同时保持这些分量的原始符号：

$$
[\mathrm{AbsTopK}_k(\mathbf{u})]_i = \begin{cases}
\nu_i, & i \in \mathcal{T}_k(|\mathbf{u}|), \\
0, & i \notin \mathcal{T}_k(|\mathbf{u}|)
\end{cases}
$$

其中 $\mathcal{T}_k(|\mathbf{u}|)$ 表示 $|\mathbf{u}|$ 中前 $k$ 个最大值的索引集合。该算子等价于 $\ell_0$ 稀疏约束下无符号限制的近端投影，在不牺牲稀疏性的前提下，使单个潜在特征可通过正负激活同时编码一个语义轴的两个方向。

### 3. 输入输出流总结

整个管线的信息流可概括为：

**输入：** 目标层 $\ell$ 的中间隐藏状态 $\mathbf{x} \in \mathbb{R}^{d}$（通常取自残差流、MLP 输出或 Attention 输出）。

**编码：** $\mathbf{u} = W^{\top} \mathbf{x} + b_{\mathrm{e}}$，将输入投影到 $P$ 维潜在空间。

**稀疏化：** $\mathbf{z} = \mathrm{AbsTopK}_k(\mathbf{u})$，仅保留 $k$ 个幅值最大的分量，正负均可存在。

**重构：** $\hat{\mathbf{x}} = D \mathbf{z} + b$，从稀疏编码恢复原始激活。

**训练信号：** 最小化 $\mathbb{E}_{\mathbf{x}} \big[ \frac{1}{2} \|\mathbf{x} - \hat{\mathbf{x}}\|_2^2 \big]$，通过重构质量驱动编码器与解码器的联合学习。稀疏度 $k$ 作为超参数控制表示紧凑性与重构保真度之间的权衡。

该框架保持了与 TopK SAE 相同的计算复杂度，唯一的差异在于稀疏选择从“最大的 $k$ 个正值”变为“最大的 $k$ 个绝对值”，从而实现了双向语义特征的捕获能力。



AbsTopK SAE 沿用了稀疏自编码器的通用结构，由编码器、稀疏激活模块和解码器三个核心部件构成。其关键创新在于将稀疏激活函数的近端算子由传统的非负阈值替换为 **绝对值 TopK（AbsTopK）**，从而解除激活非负的限制，使单个潜在特征能够同时携带正、负两个方向的信号，编码双向语义轴。

### 1. 字典学习与 SAE 的优化目标

所有 SAE 变体都可置于统一的字典学习框架下。对于隐藏状态 ${\mathbf{x}}$，训练目标为

$$
\min_{D \in \mathbb{R}^{d \times P}, b \in \mathbb{R}^{d}} \mathbb{E}_{\mathbf{x}} \Big[ \min_{\mathbf{z} \in \mathbb{R}^{P}} \frac{1}{2} \| \mathbf{x} - (D \mathbf{z} + b) \|_{2}^{2} + \lambda R(\mathbf{z}) \Big]
$$

其中 $D$ 是解码器字典（特征方向矩阵），$b$ 是偏置，$\mathbf{z}$ 是稀疏编码，$R(\mathbf{z})$ 为稀疏正则项。不同 $R$ 对应不同的近端算子，进而决定激活函数的形式。

### 2. 编码器：单步近端梯度

为避免内层最小化的非凸优化，SAE 采用参数化编码器，将输入 $\mathbf{x}$ 映射为预激活 $\mathbf{u} = W^{\top}\mathbf{x} + b_{\mathrm{e}}$，再通过一步近端梯度得到编码 $\mathbf{z}$：

$$
\mathbf{z} = \operatorname{prox}_{\lambda R}(W^{\top} \mathbf{x} + b_{\mathrm{e}})
$$

$W$ 和 $b_{\mathrm{e}}$ 与解码器参数一起端到端训练，因此编码器不需要与解码器共享权重。

### 3. 传统激活算子及其瓶颈

ReLU、JumpReLU 和 TopK 分别对应不同 $R$ 的近端映射（公式(7)）：

- **ReLU$_\lambda$**：$(\mathrm{ReLU}_{\lambda}(\mathbf{u}))_i = \max\{u_i - \lambda, 0\}$（软阈值，保留非负部分）。
- **JumpReLU$_\theta$**：$(\mathrm{JumpReLU}_{\theta}(\mathbf{u}))_i = u_i$ 若 $u_i \ge \theta$，否则 $0$（硬阈值，保留非负部分）。
- **TopK$_k$**：$(\mathrm{TopK}_k(\mathbf{u}))_i = \max\{u_i, 0\}$ 若 $i \in \mathcal{T}_k(\mathbf{u})$，否则 $0$（保留最大的 $k$ 个非负激活）。

这三种算子均隐式施加了非负约束（$\iota_{\mathbf{z} \ge 0}$）。这导致一个语义概念（如“男性 vs 女性”）必须被拆分为两个独立的非负原子，无法用一个特征表示完整的对比轴，造成 **表示碎片化**（图2玩具示例：非负 SAE 需要 `male`、`female` 和 `people` 三个原子，而 AbsTopK 只需 `gender` 一个带符号特征）。

### 4. AbsTopK 算子：解除非负约束

AbsTopK 直接使用 $\ell_0$ 硬阈值，但去除非负限制。其定义如下：

$$
[\mathrm{AbsTopK}_k(\mathbf{u})]_i = \begin{cases}
\nu_i, & i \in \mathcal{T}_k(|\mathbf{u}|), \\
0,   & i \notin \mathcal{T}_k(|\mathbf{u}|)
\end{cases}
$$

其中 $\mathcal{T}_k(|\mathbf{u}|)$ 表示 $\mathbf{u}$ 各分量绝对值最大的 $k$ 个下标。算子保留原值的符号，仅凭幅值决定是否被激活。它等价于投影到 **$k$-稀疏集合（无符号约束）** 的近端算子：

$$
\operatorname{prox}_{\lambda R}(\mathbf{u}) = \arg\min_{\mathbf{z} \in \mathbb{R}^{P}} \frac{1}{2} \|\mathbf{u} - \mathbf{z}\|_2^2 \quad \text{s.t.} \quad \|\mathbf{z}\|_0 \le k,\; \mathbf{z} \in \mathbb{R}^{P}
$$

因此，单个潜在维度可同时呈现正值和负值，分别对应概念的两极（例如正激活→男性，负激活→女性），实现双向编码。

### 5. 解码器与最终损失

解码器将稀疏编码 $\mathbf{z}$ 映射回原空间：

$$
\hat{\mathbf{x}} = D \mathbf{z} + b
$$

其中 $D$ 和 $b$ 为可学习参数。完整训练损失将编码器代入字典学习目标，同时优化编码器、解码器和稀疏正则的超参数：

$$
\min_{D, W, b, b_{\mathrm{e}}} \mathbb{E}_{\mathbf{x}} \Big[ \frac{1}{2} \| \mathbf{x} - (D \mathbf{z} + b) \|_2^2 + \lambda R(\mathbf{z}) \Big],\quad \mathbf{z} = \operatorname{prox}_{\lambda R}(W^{\top}\mathbf{x} + b_{\mathrm{e}})
$$

在实际训练中，稀疏度 $k$ 固定，端到端优化均方误差。AbsTopK 的策略同等适用于所有模型与层，无需额外的非负限制，从而在重构质量、下游操控任务和双向特征比例上均优于 TopK 和 JumpReLU（见表1、表2、图3、图4）。



## 实验与关键发现

### 安全‑效用折中与操控效果

表1报告了四款模型在不同层施加概念向量时的安全对齐（HarmBench）与通用能力维持（MMLU）结果。**AbsTopK在安全评分上与有监督的Difference‑in‑Means（DiM）并列最优，且普遍保留比TopK更高的通用能力。** 例如，在Qwen3‑4B第18层，AbsTopK将HarmBench从原始模型的17.0提升至81.3（+64.3），同时MMLU仅从77.3微降至75.9（‑1.4）；相比之下，TopK的HarmBench与MMLU分别为80.7与75.3，说明非负约束在保持同等安全性的同时付出了更多效用代价。在Gemma‑2‑2B第12层、Llama‑3.1‑8B和Gemma‑3‑12B等配置上，AbsTopK的MMLU‑HarmBench折中曲线始终位于TopK上方，证实双向编码带来的表示紧凑性直接转化为更优的操控性质。

![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/007_Table_1.jpg]]
*Table 1: Performance comparison on MMLU (↑) and HarmBench (↑) across steering methods. Entries show the absolute score; colored values in parentheses indicate the change relative to the unsteered Original model (red: improvement, blue: drop). The best result among all methods for each metric is highlighted in bold. To more comprehensively characterize the safety–utility trade-off, we evaluate steering across four model and intervene at multiple layers spanning early, middle, and late blocks. This diversity in both architectures and intervention depths allows us to test whether our conclusions are robust to model scale and to the choice of steering layer, rather than being an artifact of a single mod...*

### 双向语义特征的量化证据

表2对Gemma‑2‑2B第12层的特征进行自动语义分类，结果表明**AbsTopK产生29.7%的双面（double‑sided）特征，远高于TopK的5.3%**；其中具有相反含义（opposite meaning）的双面特征占比为20.2%，而TopK仅2.6%。这一差异直接印证了理论机制：AbsTopK移除非负约束后，单隐式基可以同时承载正、负激活，从而完整编码“男性‑女性”这类双向语义轴，而非将其拆分为两个独立的单向原子。合成评估（表5）中，Gemini 2.5 Flash对双向/单向/无结构特征的分类准确率达96%，保证了上述自动分类结论的可靠性。

![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/008_Table_2.jpg]]

### 重构质量与消融实验

Figure 3（Qwen3‑4B第20层）和Figure 5（跨越Pythia70M、Gemma‑2‑2B、GPT‑2‑small、Qwen3‑4B等多模型多层）一致显示，**AbsTopK在所有稀疏度水平上均获得更低的训练MSE损失和归一化重构误差**，且在损失恢复率（Loss Recovered）上亦优于JumpReLU与TopK。这证明，用绝对值TopK替代非负投影并未损害稀疏编码的重构能力，反而因保留了被非负约束排斥的负激活而提高了解码精度。Table 4的自动可解释性（Automated Interpretability）和PS‑EVAL F1结果显示，在Llama‑3.1‑8B的残差流、注意力输出、MLP输出等多类激活上，AbsTopK的可解释性不低于甚至优于TopK，其中残差流的改善最为明显，支持AbsTopK产出的特征在语义上不输于非负基线。

![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/005_Figure_3.jpg]]
*Figure 3: Performance comparison of JumpReLU, TopK, and AbsTopK SAEs on Qwen3 4B Layer 20, showing (a) MSE Training Loss, (b) Normalized MSE, and (c) Loss Recovered. Additional results across models and layers are provided in Appendix D*

### 探针与操控任务全景比较

Figure 4（Qwen3‑4B第18层）和Table 3（扩展到Gemma‑2‑2B第12/16层、GPT‑2‑small第6/8层、Pythia‑70M第3/4层等）汇总了六项任务：反学习（Unlearning）、吸收（Absorption）、选择性因果召回（SCR）、多类探针退化（TPP）、RAVEL与稀疏探针。**AbsTopK在SCR（0.35 vs TopK 0.26）和TPP（0.36 vs 0.31）上的优势最为突出，且在其他任务上均保持领先或持平。** 特别地，双向操控指标SCR和TPP的大幅领先进一步验证了允许正负激活对编码对比性概念的关键作用。此外，深层干预（Gemma‑2‑2B第25层，表6）表明，AbsTopK能以更极致的MMLU下降为代价，将HarmBench从19.0推至85.4，而浅层（第1层）干预对MMLU影响极小，AbsTopK的安全性增益仍显著优于TopK。

![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/006_Figure_4.jpg]]
*Figure 4: Performance comparison of SAE variants (TopK, AbsTopK, and JumpReLU) across tasks on Qwen3-4B Layer 18. For all tasks, higher scores indicate better performance; the Unlearning and Absorption scores have been transformed as 1−original score to maintain this consistency. We report the mean across five runs (random seeds 40–44), with error bars indicating the standard deviation. For more details, see Appendix E*

![[assets/figures/papers/iclr26_0005_EEs6I4cO7S_AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidir/figures/009_Table_3.jpg]]
*Table 3: Performance comparison of SAE variants across tasks on all other models and layers. For all tasks, higher scores indicate better performance; the Unlearning and Absorption scores have been transformed as 1−original score to maintain this consistency*

### 失败模式与局限

在极高稀疏度（保留极少数激活）下，所有SAE的重构误差都会上升，AbsTopK的优势可能缩小，但没有出现突然的退化拐点。AbsTopK依然是一个单步近端梯度编码器，未探索多步迭代架构，可能丢失更精细的表示结构。此外，实验集中在中型LLM（≤12B），在大规模模型上的行为有待验证。基于LLM的自动可解释性评分仅作辅助证据，核心结论由操控任务和重构质量支撑。



## 定位与知识库关联

**核心瓶颈**：现有主流 SAE 变体（ReLU、JumpReLU、TopK）的稀疏化算子均隐式或显式地包含非负指示函数 $\iota_{z \ge 0}$，强制激活只保留正值。这一设计直接导致任何一个具有双向语义轴的概念（如“男性 ↔ 女性”、“安全 ↔ 危险”）必须被拆分为两个独立、单向的字典原子——一个携带正方向信息，另一个携带负方向信息，而原始语义轴的对立结构被碎片化甚至丢失（见 Figure 2 玩具示例与 Table 2 的定量证据：TopK 在 Gemma-2-2B 第 12 层仅有 5.3% 的双面特征，其中具有对立含义的比例仅 2.6%）。

---

### 与前人方法的关系与影响

**AbsTopK 的直接血统**来自 TopK SAE（Gao et al., 2025）与近端梯度展开框架的统一视角。从 Lemma 1 给出的近端算子等价性来看，ReLU、JumpReLU 和 TopK 的非线性均可解释为带非负约束的 $\ell_1$、$\ell_0$ 或组合型稀疏近端映射。AbsTopK 所做的修改是**移除该非负约束**，而保留 $\ell_0$ 稀疏的硬阈值结构：

$$\mathrm{AbsTopK}_k(\mathbf{u})_i = \begin{cases} u_i, & i \in \mathcal{T}_k(|\mathbf{u}|) \\ 0, & i \notin \mathcal{T}_k(|\mathbf{u}|) \end{cases}$$

其中 $\mathcal{T}_k(|\mathbf{u}|)$ 选择绝对值最大的 $k$ 个分量的索引。这一修改虽然看似微小，但它直接改变了编码空间的基本结构——从“非负稀疏编码”变为“无符号约束的稀疏编码”，使单个潜在维度天然具备正、负激活的双向表达能力。

**与有监督方法 Difference-in-Means（DiM）的定位关系**：DiM 利用正负标注样本构造单一概念向量，本质上是一个有监督、单概念、单向度的线性探针，其能力可视为概念提取的“上界”，但无法扩展为特征字典。AbsTopK 作为无监督方法，在多个安全操控任务（Table 1 的 HarmBench）和探针/操控综合指标（Table 3 的 SCR、TPP）上已达到或超过 DiM，说明**移除 SAE 的非负约束本身即已逼近有监督方法在单向概念操纵上的表现**，同时保持了字典学习的可扩展性和无监督特性。

**与更广的稀疏编码和可解释性研究的关系**：AbsTopK 可被视为对“非负性是否为稀疏表示必需”这一基本问题的实验性否定回答。在稀疏编码传统中，非负约束常被引入以增强可解释性（非负矩阵分解的“部分-整体”解释），但 AbsTopK 的发现表明，**在 LLM 隐藏表示这一特定域中，取消非负约束反而释放了更丰富的语义结构**。这一结论不会直接推翻非负 SAE 的设计价值，但强烈提示现有设计因非负性而系统性地牺牲了双向语义轴。

---

### 适用边界与理论局限

1. **单步近端梯度的根本限制**：AbsTopK 仍然采用单步近端梯度作为编码器 $\mathbf{z}^{(1)} = \operatorname{prox}_{\lambda R}(W^\top \mathbf{x} + b_e)$，这意味着编码过程是前馈线性映射后跟一次阈值化。从优化角度看，这等价于进行一次近端梯度迭代后即停止，并未收敛到字典学习的真正稀疏编码解。当字典原子间存在强相关时（现实 LLM 表示中极可能如此），单步编码会产生系统性的编码偏差，且 AbsTopK 并未从理论上证明其在此情况下的收敛或泛化保证优于非负方案。论文本身也指出多步近端梯度（即多层编码器）是自然的未来扩展方向。

2. **极高稀疏度下的优势衰减**：虽然 Figure 3 和 Figure 5 显示 AbsTopK 在所有稀疏度水平上重建误差均低于 TopK 和 JumpReLU，但所有方法在激活数量极端减少时性能均剧烈下降。AbsTopK 的双向特性在极低 $k$ 值时可能不再形成显著优势，因为此时每个特征都必须承载极强的压缩，正负共存带来的富余表达空间被稀疏性本身所吞没。这一边界效应尚未被系统研究。

3. **模型规模与模态的未验证外推**：实验仅覆盖了 Qwen3-4B、Gemma2-2B、Llama-3.1-8B 等中型开源 LLM，尚未在 70B+ 模型或多模态模型上进行验证。无法确定双向特征的出现丰富度是否随模型规模单调增长，也无法断定 AbsTopK 的 $\ell_0$ 硬阈值在计算上是否适用于千亿参数模型的训练。

4. **自动评估指标的辅助性地位**：Table 4 和 Table 5 的自动可解释性评分虽显示了 AbsTopK 的优势，但论文自身承认近期工作对基于 LLM 的自动评估存在可靠性争议（如“合理化偏见”）。合成评估（Table 5，Gemini 2.5 Flash 对双向/单向/无结构特征的 96% 分类准确率）缓解了部分风险，但仍未完全解决“LLM 打分可能迎合人类可解释性期望”的根本问题。因此，自动可解释性指标仅应作为辅助证据引用，主要结论的安全性应依赖于下游操控任务（Table 1、Table 6）和安全-效用折衷曲线（Figure 4 的 SCR、TPP）中提供的行为证据。

---

### 实验有效性与证据强度分类

| 证据类型 | 支持强度 | 关键参考 | 需注意的边界 |
|----------|----------|----------|-------------|
| **双向特征的存在比例** | 强 | Table 2：AbsTopK 双面特征 29.7% vs TopK 5.3%；对立含义 20.2% vs 2.6% | 自动语义分类由 LLM 执行（虽然合成验证表明其可靠），需要更多人工标注复核 |
| **重建误差的系统性降低** | 强 | Figure 3(a)/Figure 5(a)：所有模型和层上 MSE 均最低 | 只在标准 MSE 损失下比较；未探索感知损失或对抗性重构指标 |
| **安全操控任务的优势** | 中等-强 | Table 1：HarmBench 较原始模型提升 +64.3（Qwen3-4B）；Table 6：深层 AbsTopK 将 HarmBench 从 19.0 提升至 85.4 | 效用代价（MMLU 下降）在深层干预时更明显，安全-效用曲线的前沿形状需逐模型评估 |
| **自动化可解释性** | 辅助 | Table 4：优势恒定但幅度不大 | 可靠性有争议，不应独立作为核心论据 |
| **跨模型/多层的一致性** | 强 | Table 1/Table 3 覆盖 4 个模型、多层层级 | 中型模型范围有限；更大规模模型未验证 |

---

### 开放问题

1. **非负性到底是不是“偶然的设计遗产”？** 非负激活被引入 SAE 的最初动机是否仅是为了与 ReLU 的生物学类比，还是在 LLM 表示的某个尚未发现的层面上确有存在的必要性？AbsTopK 的经验成功促使我们重新考虑“稀疏 + 非负”的约束组合是否应解耦为两个独立设计的维度。

2. **多步近端梯度编码的潜力是否被低估？** 单步编码的信息瓶颈是明知的。将编码器扩展为多层、多阈值或迭代式的稀疏编码过程，有可能捕获更深层的表示结构，同时保持双向特性。这种扩展可能与 Matryoshka 分层表示方法自然结合，实现在不同粒度级别上的分层次特征组织。

3. **$\ell_0$ 硬阈值的可扩展性瓶颈**：绝对值的 TopK 选择在 GPU 上的实现依赖排序操作，对于包含数百万字典原子的超大模型，这将成为计算瓶颈。是否存在 $\ell_0$ 的平滑或随机近似方法，既能保持双向稀疏特性，又能在实现上更亲和于大规模并行计算？

4. **双向特征在不同语义结构上的适用性差异**：当前实验主要聚焦于“对立轴”型概念（性别、安全/危害、情感极性）。对于具有内在层次结构的概念（如“金门大桥”由“桥”、“金门”、“旧金山”等多级属性构成），双向特征是否仍然保持紧凑，还是会导致新的碎片化形式？这一点缺乏系统性的语义结构分类研究。

5. **安全操控的双刃剑效应**：Figure 4 和 Table 6 显示深层 AbsTopK 在提升 HarmBench 安全分数的同时显著降低了 MMLU 效用分数。这是稀疏操控技术的固有张力，还是 AbsTopK 的双向特征在特定层上过度泛化所导致的副作用？需要通过更细粒度的层间干预权重调谐和概念向量分解来深度分析。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidirectional_Features.pdf

![[paperPDFs/ICLR_2026/AbsTopK_Rethinking_Sparse_Autoencoders_For_Bidirectional_Features.pdf]]
