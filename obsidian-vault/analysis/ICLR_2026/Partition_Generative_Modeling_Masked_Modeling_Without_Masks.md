---
title: "Partition Generative Modeling: Masked Modeling Without Masks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Partition_Generative_Modeling_Masked_Modeling_Without_Masks.pdf
project_link: null
code_link: null
openreview_forum_id: vEh1ceS154
aliases:
- PGMPPT
- PGMMMWM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将序列划分为两个互不可见的互补组，并设计组间隔离的注意力机制（分区Transformer），使得模型仅依赖对方组的信息来预测当前组，从而在训练和推理中完全消除[MASK]令牌，并在推理时只处理干净令牌，实现高效并行生成。"
primary_logic: "通过分区代替掩码，分区生成模型（PGM）在保持任意顺序并行生成的同时，获得了类似自回归模型仅处理干净令牌的推理效率；同时，每组预测另一方给出双重梯度信号，训练方差降低，模型质量（困惑度）进一步提升。"
claims:
- "PGMs 用分组分区替代掩码，完全消除了训练和推理中的 [MASK] 令牌，并确保组间无信息流。"
- "在 OpenWebText 上，PGM 的生成困惑度优于 MDLM，且采样吞吐量提升 5–5.5 倍。"
- "在 ImageNet 上，PGM 以 7.5× 吞吐量提升达到与 MaskGIT 相当的 FID；增加步数后 FID 改善至 4.56，且仍比 MaskGIT 快 3.9×。"
- "PGM 训练时对所有位置计算损失，提供两倍梯度贡献，降低方差；在 LM1B 上困惑度降低 1.95 点。"
---

# Partition Generative Modeling: Masked Modeling Without Masks

> [!tip] 核心洞察
> 通过分区代替掩码，分区生成模型（PGM）在保持任意顺序并行生成的同时，获得了类似自回归模型仅处理干净令牌的推理效率；同时，每组预测另一方给出双重梯度信号，训练方差降低，模型质量（困惑度）进一步提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 分区生成模型：用分区取代掩码的掩码生成方法 |
| 英文题名 | Partition Generative Modeling: Masked Modeling Without Masks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=vEh1ceS154) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Partition Generative Model (PGM) / Partition Transformer |
| Dataset | OpenWebText (1024 tokens), LM1B (128 tokens), ImageNet 256×256 (32 步, Halton 采样), ImageNet 256×256 (64 步 |

> [!tip] 效果简介
> - OpenWebText (1024 tokens) 上，生成困惑度 (Gen. PPL) 和采样吞吐量 为 PGM 6/6 (dim=1024): Gen. PPL 21.43 (Val PPL), 吞吐 5518 tok/s (128步)，对比 MDLM: Gen. PPL 23.07, 吞吐 1043 tok/s，变化 生成困惑度降低 1.64 点；吞吐量提升约 5.3 倍。
> - LM1B (128 tokens) 上，验证困惑度 (Val. PPL) 为 PGM 6/6: 26.80，对比 MDLM: 27.67，变化 降低 1.95。
> - ImageNet 256×256 (32 步, Halton 采样) 上，FID 为 PGM 12/12 (w=3): 5.54，对比 MaskGIT (w=1): 5.35，变化 FID 稍高 (+0.19)，但吞吐量提升 7.5×。

## 概要

掩码生成模型（Masked Generative Models, MGMs）通过迭代去掩码实现并行生成，在文本和图像领域取得了显著进展。然而，这类模型存在一个根本性的效率瓶颈：在每次推理步骤中，模型必须处理整个序列——包括大量无信息的 [MASK] 令牌，导致大量计算资源被浪费在无效操作上。这使得 MGMs 在推理吞吐量上远逊于仅处理干净令牌的自回归模型（ARMs），尽管后者受限于严格的从左到右生成顺序。

本文提出**分区生成模型（Partition Generative Models, PGMs）**，以一种简洁而根本的方式解决了上述困境。其核心思想是：**用分区取代掩码**。具体而言，PGM 将序列划分为两个互补的、互不可见的组，并设计组间隔离的注意力机制（分区 Transformer），使得模型仅依赖对方组的信息来预测当前组，从而在训练和推理中完全消除 [MASK] 令牌。这一设计带来了双重收益：

- **推理效率跃升**：推理时仅处理干净令牌，序列长度随生成逐步增长，避免了无效计算。在 OpenWebText 上，PGM 的采样吞吐量达到 MDLM 的 **5–5.5 倍**；在 ImageNet 256×256 上，PGM 以 **7.5 倍**的吞吐量提升达到与 MaskGIT 相当的 FID，若增加采样步数，FID 可进一步改善至 **4.56**，同时仍比 MaskGIT 快 **3.9 倍**。

- **训练质量提升**：由于两组互相预测，每个前向传播为所有位置提供双重梯度信号，训练方差降低。在 LM1B 上，PGM 的验证困惑度较 MDLM 降低 **1.95 点**；在 OpenWebText 上，生成困惑度降低 **1.64 点**。

PGM 兼容现有的 MGM 采样器和蒸馏方法，可作为即插即用的替代方案。通过分区代替掩码这一关键操作，PGM 在保持任意顺序并行生成能力的同时，获得了类似自回归模型的推理效率，为生成模型在效率与质量之间的权衡提供了新的解决路径。

序列生成模型的核心任务是将离散序列 $\mathbf{x} \in \{1, \dots, N\}^L$ 的联合分布 $p(\mathbf{x})$ 参数化，以支持高效训练和高质量采样。当前主流范式分为两大阵营：**自回归模型（ARM）** 和 **掩码生成模型（MGM）**，二者在推理效率与生成灵活性之间形成根本性权衡。

**自回归模型** 将联合分布分解为前缀条件概率的乘积：

$$p_{\theta}(\mathbf{x}) = \prod_{i=1}^{L} p_{\theta}(\mathbf{x}_i \mid \mathbf{x}_{<i})$$

这种逐令牌生成的范式使模型在推理时仅处理干净令牌，计算效率高；但其顺序生成的本质限制了并行能力，且无法利用双向上下文进行全局推理。

**掩码生成模型** 则通过逐步去噪实现任意顺序的并行生成。以 **MDLM**（Sahoo et al., 2024）为例，其训练目标为：

$$\mathcal{L}_{\mathrm{MGM}} := \mathbb{E}_{\mathbf{x} \sim \mathcal{D}, t \sim \mathcal{U}[0,1]} \left[ w(t) \mathrm{CE}(\mathbf{x}_\theta(\mathbf{z}_t; t), \mathbf{x}) \right]$$

其中 $\mathbf{z}_t$ 是经前向破坏过程 $q_t(\cdot | \mathbf{x}) = \mathrm{Cat}(\cdot; \alpha_t \mathbf{x} + (1 - \alpha_t) \pi)$ 得到的含掩码序列。MGM 在训练时仅对被掩码位置计算损失，在推理时每一步必须将**完整序列**（包括大量无信息的 `[MASK]` 令牌）输入模型。这一设计导致了一个尖锐的瓶颈：**推理吞吐量显著受限于无效计算**——模型反复处理已生成令牌的同时，还需携带大量 `[MASK]` 令牌进行全序列前向传播。

以 OpenWebText（上下文长度 1024）为例，MDLM 的采样吞吐量仅为约 1043 tok/s，而同等规模的自回归模型可轻松突破数倍于此的速度。在图像生成领域，**MaskGIT**（Chang et al., 2022）面临同样困境：即使采用置信度解码策略，仍须在每一步处理含大量掩码令牌的完整特征图。

这一效率鸿沟的根本原因在于：**MGM 无法在保持任意顺序并行生成的同时，获得自回归模型“仅处理干净令牌”的推理优势**。现有加速手段（如蒸馏、减少采样步数）虽能缓解问题，但未触及架构层面的冗余计算本质。

本文的核心动机正是打破这一僵局：**能否设计一种生成范式，既保留 MGM 的并行、任意顺序生成能力，又在推理时仅处理干净令牌？** 这要求从根本上重新思考令牌破坏策略与信息流机制——不是优化掩码的使用方式，而是彻底消除掩码本身。

## 核心方法与创新机理

### 瓶颈诊断：掩码令牌的推理负担

掩码生成模型（MGM）面临一个根本性的效率瓶颈：每次采样迭代时，模型必须将**整个序列**（包括大量无信息的 `[MASK]` 令牌）输入模型进行前向计算。以 **MDLM**（Sahoo et al., 2024）为例，其推理过程从全掩码序列开始，逐步去掩码，每一步都需要处理全长序列。这意味着大量计算资源被浪费在对已知令牌的重复编码上，导致推理吞吐量显著受限。自回归模型（ARM）仅处理干净令牌，效率高但生成顺序固定；MGM 支持并行、任意顺序生成，却以牺牲推理效率为代价。如何在保持 MGM 并行生成优势的同时，获得接近自回归模型的推理效率，是这一领域的核心矛盾。

### 因果调控：用分区替代掩码

PGM 的核心操作是将序列划分为**两个互补且互不可见的组**，彻底消除 `[MASK]` 令牌。这一设计与 MGM 形成四个关键差异：

| 设计维度 | MGM（基线） | PGM（本文） |
|---------|-----------|-----------|
| **令牌破坏策略** | 随机将令牌替换为 `[MASK]` | 将序列划分为两个互补组，不使用任何 `[MASK]` |
| **注意力与信息流** | 标准双向自注意力，所有令牌互相可见 | 组内自注意力 → GroupSwap 跨注意力 → 解码器跨注意力，组间严格隔离 |
| **推理输入长度** | 每一步处理全长的含 `[MASK]` 序列 | 每一步只处理干净令牌（仅一组），长度随生成逐步增加 |
| **训练损失覆盖** | 仅对被掩码位置计算损失 | 对所有位置（两组均计算）计算损失，每批次提供双倍监督信号 |

### 核心洞察：双重收益

PGM 通过分区机制同时获得两类收益：

**推理效率跃升**。由于组间无信息流，推理时只需将当前要预测的那一组令牌输入模型，另一组作为条件上下文。生成过程从空序列开始，逐步将令牌分配到两组中，输入序列长度从 0 线性增长到全长。相比之下，MGM 每一步都必须处理全长序列。这一差异在长序列上尤为显著：在 OpenWebText（上下文长度 1024）上，PGM 的采样吞吐量达到 **5518 tok/s**，而 MDLM 仅为 **1043 tok/s**，提升约 **5.3 倍**（Table 1）；在上下文长度 4096 时，PGM 的速度优势进一步扩大（Table 10）。

**训练方差降低**。PGM 在单次前向传播中同时评估两个互补掩码率下的 MGM 训练目标——组 0 以掩码率 $t$ 被预测，组 1 以掩码率 $1-t$ 被预测。这意味着每个批次提供**两倍的梯度贡献**，等价于在不增加计算量的情况下扩大了有效批量大小，降低了训练方差。在 LM1B 上，PGM 的验证困惑度比 MDLM 降低 **1.95 点**（26.80 vs. 27.67）；在 OpenWebText 上，生成困惑度降低 **1.64 点**（21.43 vs. 23.07），同时保持匹配的生成熵（Table 1, Table 6）。

### 架构保障：分区 Transformer

实现组间隔离需要专门的架构设计。分区 Transformer 由三个模块组成（Figure 3）：

- **分区编码器**：采用组内自注意力，同一组内的令牌可以互相注意，但不同组的令牌之间完全隔离。这确保了编码阶段不会发生跨组信息泄漏。
- **GroupSwap 层**：通过跨注意力将每个位置的表示路由到对方组。查询向量可以是数据无关的（基于可学习向量和正弦位置编码）或数据依赖的（额外加入对方组的聚合表示）。消融实验表明，数据无关查询与数据依赖查询性能相当，因此采用更简单的数据无关版本（Table 5）。
- **解码器**：对编码器输出进行组级跨注意力，不包含自注意力，仅在被解码位置高效生成预测。

这一架构保证了预测组 0 的令牌时，模型只能看到组 1 的信息，反之亦然，从而在推理时只需处理干净令牌。

### 局限与待验证点

尽管 PGM 在推理效率上优势显著，仍需注意以下限制：在小数据集（如 OpenWebText）上，PGM 可能需要增加参数量（更多层数或更大嵌入维度）才能在困惑度上超越 MDLM（Table 5）；互补掩码训练中会出现损失尖峰，虽未导致发散，但可能影响训练稳定性（Figure 6）；分区 Transformer 依赖定制的块对角注意力掩码，现有优化计算核心对其支持有限，训练吞吐量约为 MDLM 的 75%（Table 3）。此外，当前仅在文本和图像生成上验证，多模态扩展仍有待探索。

分区生成模型（PGM）的核心设计思想是用**序列分区**替代掩码生成模型（MGM）中无处不在的 `[MASK]` 令牌，从而在保持并行、任意顺序生成能力的同时，获得类似自回归模型（ARM）仅处理干净令牌的推理效率。其整体 pipeline 围绕一个关键约束构建：序列被划分为两个互补的、互不可见的组，模型必须仅依赖对方组的信息来预测当前组。

### 模块架构与数据流

PGM 的完整 pipeline 由三个核心模块串联构成：**分区编码器（Partition-wise Encoder）**、**GroupSwap 层**和**解码器（Decoder）**，三者共同实现了组间严格隔离的信息流控制。

**1. 分区编码器**
编码器由多个分区自注意力（partition-wise self-attention）块堆叠而成。与标准双向 Transformer 不同，该模块对两组令牌分别执行组内自注意力，组间不存在任何注意力交互。这意味着编码器输出的每个令牌表示仅包含其所在组内部的上下文信息，为后续的跨组预测提供了干净的组表示基础。

**2. GroupSwap 层**
这是确保“组间无信息泄漏”的关键组件。GroupSwap 层通过跨注意力机制，将编码器输出的各组表示路由到对方组。具体而言，对于组 0 中的每个位置，其查询向量（query）会去关注组 1 中所有位置的键值对（key-value pairs），反之亦然。查询向量的初始化支持两种模式：
- **数据无关查询**：使用可学习向量与正弦位置编码的组合，经层归一化和线性投影生成，不依赖输入内容。
- **数据依赖查询**：在数据无关查询的基础上，加入对方组的聚合表示（如 logsumexp 或均值池化）。

消融实验表明两者性能相当，因此实际采用更简单的数据无关版本。

**3. 解码器**
解码器对 GroupSwap 层的输出执行组级跨注意力（group-wise cross-attention），且**不包含自注意力**。这意味着每个位置的预测仅依赖于对方组经编码和路由后的表示，完全无法访问本组内其他位置的信息。解码器最终输出所有位置的 logits，用于计算损失或生成采样。

### 输入输出流

**训练阶段**：
1. 输入序列 $\mathbf{x}$ 被随机划分为两组，由二进制组标签 $\mathbf{g} \in \{0,1\}^L$ 标记。
2. 完整序列（两组令牌均不添加 `[MASK]`）同时送入分区编码器，经组内自注意力处理后得到两组独立的隐藏表示。
3. GroupSwap 层将各组表示路由到对方组。
4. 解码器基于对方组信息预测当前组的所有位置，输出全部 $L$ 个位置的 logits。
5. 损失函数对所有位置计算加权交叉熵：
   $$\mathcal{L}_{\mathrm{PGM}} := \mathbb{E}_{\mathbf{x} \sim \mathcal{D}, t \sim \mathcal{U}[0,1]} \left[ w^{\mathrm{PGM}}(\mathbf{g}, t) \mathrm{CE}(\mathbf{x}_\theta(\mathbf{x}; \mathbf{g}; t), \mathbf{x}) \right]$$
   其中每令牌权重 $w^{\mathrm{PGM}}(\mathbf{g}, t)_i$ 为：组 0 权重 $w(t)$，组 1 权重 $w(1-t)$，模拟两个互补掩码率的 MDLM 目标。

**推理阶段**：
1. 初始时，一组令牌为空（待生成），另一组为已采样的干净令牌。
2. 每一步仅将**干净令牌所在组**送入模型，另一组位置以可学习的嵌入或零填充占位。
3. 模型输出待生成组所有位置的 logits，采样后更新该组令牌。
4. 两组角色交替：上一轮的预测组变为下一轮的干净条件组，反之亦然。
5. 整个过程处理的序列长度随生成逐步增长，但始终不包含 `[MASK]` 令牌，这是推理吞吐量大幅提升的根本原因。

### 与 MGM 的关键差异

与标准 MGM（如 **MDLM**、**MaskGIT**）相比，PGM 在 pipeline 层面有三处根本性改变：
- **令牌破坏策略**：用分区替代掩码，训练和推理中完全消除 `[MASK]` 令牌。
- **注意力信息流**：通过分区编码器 + GroupSwap + 解码器的组合，强制组间隔离，确保预测仅依赖对方组。
- **推理输入长度**：每一步只处理干净令牌（单组），而非全长含掩码序列，序列长度随生成逐步增长。

这些设计使得 PGM 在单次前向传播中同时评估两个互补掩码率的 MDLM 目标，提供双倍梯度信号以降低训练方差，并在推理时获得 5–7.5 倍的吞吐量提升。

### 分区生成建模：从掩码到分区

分区生成模型（PGM）的核心创新在于用**序列分区**替代掩码。给定长度为 $L$ 的序列 $\mathbf{x}$，PGM 将其划分为两个互补组：组 0（干净令牌）和组 1（待预测令牌）。与掩码生成模型（MGM）将令牌替换为 [MASK] 不同，PGM 中两组令牌均保持原始值，但通过**组间隔离的注意力机制**确保信息不能跨组流动——组 0 的预测只能依赖组 1，反之亦然。

这一设计在单次前向传播中同时评估了两个互补掩码率下的 MGM 训练目标，训练损失覆盖所有位置：

$$\mathcal{L}_{\mathrm{PGM}} := \mathbb{E}_{\mathbf{x} \sim \mathcal{D}, t \sim \mathcal{U}[0,1]} \left[ w^{\mathrm{PGM}}(\mathbf{g}, t) \mathrm{CE}(\mathbf{x}_\theta(\mathbf{x}; \mathbf{g}; t), \mathbf{x}) \right]$$

其中每令牌权重根据组别分配：

$$w^{\mathrm{PGM}}(\mathbf{g}, t)_i = \begin{cases} w(t) & \text{if } \mathbf{g}_i = 0 \\ w(1-t) & \text{if } \mathbf{g}_i = 1. \end{cases}$$

- $\mathbf{g}$：组分配向量，$\mathbf{g}_i = 0$ 表示令牌 $i$ 属于组 0（干净组），$\mathbf{g}_i = 1$ 表示属于组 1（预测组）
- $t \sim \mathcal{U}[0,1]$：从均匀分布采样的时间步
- $w(t)$：MGM 标准的时间相关权重函数
- $\mathrm{CE}$：交叉熵损失
- $\mathbf{x}_\theta$：模型预测的概率分布

组 0 权重为 $w(t)$，组 1 权重为 $w(1-t)$，模拟了互补掩码率的效果。这一机制提供了**双重梯度信号**，有效降低训练方差，在 LM1B 上困惑度降低 1.95 点（Table 1）。

### 分区 Transformer 架构

PGM 依赖专门设计的 **Partition Transformer**，确保组间无信息泄漏的同时实现高效推理。架构由三个模块组成（Figure 3）：

**编码器（Encoder）**：由多层分区自注意力块堆叠而成。与标准双向 Transformer 的关键区别在于，不同组的令牌之间不进行注意力交互——注意力掩码强制令牌只能关注同组成员。这保证了编码器输出中，每组表示仅包含本组信息。

**GroupSwap 层**：实现跨组信息路由的核心模块。通过跨注意力机制，将一组中每个位置的表示路由到对方组的对应位置。跨注意力查询（Query）有两种初始化方式：

**数据无关查询**（默认采用）：
$$V_{i;\cdot} = W \left[ \mathrm{LN} \left( u + \mathrm{pos}_{i;\cdot} \right) + b \right]$$

其中 $u$ 为可学习向量，$\mathrm{pos}_{i;\cdot}$ 为固定正弦位置编码：
$$\mathrm{pos}_{i,j} = \begin{cases} \cos\left(\frac{i}{10000^{2j/H}}\right) & \text{if } j < H/2 \\ \sin\left(\frac{i}{10000^{2j/H-1}}\right) & \text{otherwise} \end{cases}$$

$\mathrm{LN}$ 为层归一化，$W$ 和 $b$ 为线性投影参数。

**数据依赖查询**（可选）：
$$V_{i;\cdot}^{\prime} = V_{i;\cdot} + \begin{cases} Y_{1}, & \text{if } g_i = 0 \\ Y_{0} & \text{otherwise} \end{cases}$$

在数据无关查询基础上加入对方组的聚合表示 $Y_0$ 或 $Y_1$。消融实验表明两者性能相当，因此采用更简单的数据无关版本（Table 5）。

**解码器（Decoder）**：对编码器输出进行组级跨注意力，**不使用自注意力**。解码器仅在被解码位置高效生成预测，进一步减少计算量。

### 推理效率的关键机制

在推理阶段，PGM 仅需处理干净令牌。由于组间无信息流，当预测组 0 时，模型输入仅为组 1 的令牌（不含任何 [MASK]），序列长度随生成逐步增加。这与 MGM 每一步必须处理全长含 [MASK] 序列形成鲜明对比，是 PGM 实现 5–7.5× 吞吐量提升的根本原因。

## 实验与关键发现

### 核心实验结果

分区生成模型（PGM）在文本和图像生成任务上均展现出显著的推理效率优势，同时在生成质量上保持竞争力。

**文本生成：OpenWebText 与 LM1B**

在 OpenWebText（上下文长度 1024）上，PGM 8/8（8 层编码器、8 层解码器）以 128 步采样实现了生成困惑度 21.43，优于 MDLM 的 23.07，同时采样吞吐量从 1043 tok/s 提升至 5518 tok/s，加速约 5.3 倍（Table 1, Table 6）。在 LM1B（上下文长度 128）上，PGM 6/6 的验证困惑度为 26.80，较 MDLM 的 27.67 降低了 1.95 点，且延迟从 3.78 秒降至 2.12 秒（Table 1）。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/004_Table_1.jpg]]
*Table 1: Validation perplexity, sampling latency, and throughput (TP) on LM1B and OpenWebText. PGM k / m uses k encoder and m decoder layers. The best PGM per dataset is highlighted. Latency and TP are measured at batch size 32. † Trained with a 2× larger batch size (Sec. 5.3). See Table 5 for architecture ablations*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/012_Table_6.jpg]]
*Table 6: Sample quality and efficiency on OpenWebText with different numbers of sampling steps. We generate sequences of 1024 tokens with a batch size of 32 to measure the latency and throughput. PGM 6 / 6 with a hidden dimension of 1024 and uniform sampling achieves at least a 5× latency and throughput improvement over MDLM, with better Generative Perplexity and matching entropy*

值得注意的是，PGM 的效率优势随着上下文长度增加而扩大：在 4096 上下文长度下，PGM 的吞吐量优势更为显著（Table 10），这直接源于 PGM 在推理时仅处理干净令牌的核心设计，避免了 MDLM 每步处理全长 [MASK] 序列的冗余计算。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/016_Table_10.jpg]]
*Table 10: Throughput (TP) of MDLM and PGM with a context length of 4096, for varying number of inference steps. PGM is significantly faster than MDLM*

**图像生成：ImageNet 256×256**

在 ImageNet 256×256 上，PGM 12/12（宽度 w=3）使用 Halton 采样器在 32 步下达到 FID 5.54，与 MaskGIT（FID 5.35）相当，但吞吐量提升 7.5 倍（Figure 1 左, Table 9）。当采样步数增加至 64 步（w=2）时，PGM 的 FID 进一步改善至 4.56，显著优于 MaskGIT 的 6.76，且仍保持 3.9 倍的吞吐量优势（Figure 1 左, Table 9）。这表明 PGM 在质量-效率权衡曲线上占据明显优势位置：用户既可以用更少的计算获得相近质量，也可以用更多步数换取更高质量。

**蒸馏后性能**

经过自蒸馏时间（SDTT）蒸馏后，PGM 6/6 配合 nucleus 采样（p=0.9）在 OpenWebText 上达到生成困惑度 43.22，延迟仅 11.95 ms，而同等条件下 MDLM 的生成困惑度为 45.86，延迟为 62.54 ms——PGM 在质量更优的同时延迟降低约 5.2 倍（Table 7, Figure 4）。在下游任务评估中（Table 2），蒸馏后的 PGM 在 HellaSwag、OpenBook QA、Arc-easy 等 8 个 NLP 任务上继续优于 MDLM，表明效率增益未以牺牲表征质量为代价。

### 消融分析

**编码器-解码器层数配置**

Table 5 系统消融了不同编码器/解码器层数分配方案。结果表明，平衡配置（如 6/6、8/8）始终优于不平衡配置（如 10/6、6/10）。例如在 LM1B 上，PGM 6/6 的验证困惑度为 26.80，而 PGM 10/6 为 27.12，PGM 6/10 为 27.24。这一趋势在 OpenWebText 上同样成立。核心原因在于：编码器负责为两组令牌分别建立内部表征，解码器负责基于对方组信息进行预测，两者能力需要匹配才能有效利用双重梯度信号。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/011_Table_5.jpg]]
*Table 5: Perplexity evaluations. Validation perplexity of the Masked Diffusion Language Model (MDLM) and PGMs (ours) on LM1B and OpenWebText (OWT). The row MDLM (Compl. masking) denotes an MDLM trained with the complementary masking strategy discussed in Section 5.3. The row PGM k / m denotes a PGM with k encoder and m decoder layers, and we highlighted the best PGM results in gray. lsm and mean denote the logsumexp and mean queries initializations (Section 4). Takeaway: using the same number of layers in the encoder and decoder, and data-independent queries performed best. On LM1B, our PGM reaches 1.95 lower perplexity than MDLM after 1M steps. On OWT, we grow the embedding dimension or the number...*

**GroupSwap 查询初始化**

数据无关查询（data-independent queries）与数据依赖查询（logsumexp 聚合和 mean 聚合）在性能上相当（Table 5），因此论文在所有后续实验中采用更简单的数据无关版本。这一消融结论降低了架构复杂度，同时验证了位置编码加可学习向量足以实现有效的跨组信息路由。

**互补掩码的独立贡献**

当将互补掩码策略直接应用于 MDLM 训练时（即每批次同时计算两个互补掩码率的损失），在 LM1B 上观察到了困惑度改善，但在 OpenWebText（上下文 1024）上提升有限，且需要增加参数量（更多层数或更大嵌入维度）才能超越原始 MDLM（Table 1, Table 5, Section 5.3）。这说明互补掩码的方差缩减效应在较短序列上更为显著，而长序列场景下的收益需要配合分区 Transformer 的架构设计才能充分释放。

### 训练稳定性与开销

互补掩码训练会引入偶发性的损失尖峰（loss spikes），但未导致模型发散（Figure 6, Section D.1）。这一现象可能与两组交替预测时梯度信号的阶段性不协调有关，是当前方法的已知局限。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/009_Figure_6.jpg]]
*Figure 6: Training loss of MDLM, MDLM with Complementary Masking (Section 5.3) and PGM. Complementary masking seems to introduce spikes in the loss, even though it did not cause the models to diverge*

在训练效率方面（Table 3），PGM 在 LM1B 上的单步前向+反向传播延迟与 MDLM 几乎持平（开销可忽略），但在 OpenWebText 上，PGM 6/6（嵌入维度 1024）的训练吞吐量约为 MDLM 的 75%。这一差距源于分区 Transformer 中定制的块对角注意力掩码与现有优化计算核心（kernels）的兼容性不足。然而，考虑到推理端 5 倍以上的吞吐量优势，这一训练开销在多数应用场景下是可接受的。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_vEh1ceS154/figures/008_Table_3.jpg]]
*Table 3: Latency and throughput for a single forward+backward pass of the MDLMs and PGMs, computed on a single A100-SXM4-80GB GPU. On LM1B, PGM introduces a negligible overhead over MDLM. On OWT, our PGM with 6 encoder and decoder layers and an embedding dimension of 1024 achieves around 75% of the training throughput of MDLM. Recall that at inference, the same PGM is around 5× faster than MDLM*

### 关键图表导航

- **Figure 1**：核心结果总览，左图展示 ImageNet 上 PGM 与 MaskGIT 的 FID-吞吐量权衡，右图展示 OpenWebText 上 PGM 与 MDLM 的生成困惑度-吞吐量权衡。
- **Table 1**：LM1B 和 OpenWebText 上的验证困惑度、采样延迟及吞吐量汇总，包含不同 PGM 变体的完整对比。
- **Table 5**：架构消融核心表，涵盖层数配置、查询初始化方式和互补掩码的独立效果。
- **Table 6**：OpenWebText 上不同采样步数下的生成质量与效率细节。
- **Table 9**：ImageNet 上 Halton 采样器在不同步数和 CFG 权重下的 FID、IS、延迟与吞吐量。
- **Figure 4**：蒸馏后 PGM 与 MDLM 的速度-质量对比，展示 nucleus 采样下的优势。
- **Figure 6**：训练损失曲线，展示互补掩码引入的损失尖峰现象。

## 定位与知识库关联

### 核心创新与基线对比

分区生成模型（PGM）的核心创新在于用**分区替代掩码**，从根本上改变了掩码生成模型（MGM）的令牌破坏策略。传统 MGM 方法——包括 **MDLM**（Sahoo et al., 2024）在文本领域和 **MaskGIT**（Chang et al., 2022）在图像领域——均依赖将部分令牌替换为 `[MASK]` 令牌，并在推理时每一步处理全长序列（含大量无信息掩码令牌）。PGM 将序列划分为两个互补组，通过分区 Transformer 确保组间无信息流，使得模型仅依赖对方组信息预测当前组，从而在训练和推理中完全消除 `[MASK]` 令牌。

这一设计带来三个关键变化：

1. **推理效率的结构性提升**：推理时每一步只处理干净令牌（仅一组），序列长度随生成逐步增加，而非始终处理全长含掩码序列。这使得 PGM 在 OpenWebText 上采样吞吐量达到 MDLM 的 5–5.5 倍，在 ImageNet 上达到 MaskGIT 的 7.5 倍（Figure 1）。

2. **训练信号的双重利用**：PGM 对所有位置（两组均计算）计算损失，每批次提供两倍监督信号，而传统 MGM 仅对被掩码位置计算损失。这降低了训练方差，在 LM1B 上验证困惑度降低 1.95 点（Table 1, Table 5）。

3. **与现有生态的兼容性**：PGM 兼容现有 MGM 采样器（如 Halton 采样、置信度采样）和蒸馏方法（如 SDTT，Deschenaux & Gulcehre, 2025），可作为即插即用的替代方案。

### 架构层面的差异化设计

PGM 的分区 Transformer 由三个关键模块构成（Figure 3）：

- **分区编码器**：通过组内自注意力独立处理各组，不进行跨组信息交互。这与标准双向 Transformer 的全注意力形成对比。
- **GroupSwap 层**：使用数据无关或数据依赖的查询进行跨注意力，将信息从一组路由到另一组。数据无关查询（可学习向量 + 正弦位置编码）与数据依赖查询（加入对方组聚合表示）性能相当，因此采用更简单的数据无关版本（Table 5）。
- **解码器**：对编码器输出进行组级跨注意力（无自注意力），仅在被解码位置高效生成预测。

这种架构设计确保了 PGM 在保持任意顺序并行生成能力的同时，获得了类似自回归模型仅处理干净令牌的推理效率——这是 MGM 和自回归模型此前无法兼得的特性。

### 适用边界与局限

1. **小数据集上的参数量需求**：在 OpenWebText 上，PGM 需要增加参数量（更多层数或更大嵌入维度）才能超越 MDLM 的验证困惑度，尽管推理速度优势始终显著（Section 5.3, Table 1）。

2. **训练稳定性**：互补掩码训练中会出现损失尖峰（Figure 6），虽未导致模型发散，但可能给大规模训练带来稳定性挑战。这一现象的深层原因尚不明确。

3. **模态覆盖范围有限**：当前仅在文本（LM1B, OpenWebText）和图像（ImageNet 256×256）生成上验证，尚未扩展到音频、视频等多模态任务。

4. **训练吞吐量开销**：分区 Transformer 依赖定制的块对角注意力掩码，现有优化计算核心对其支持有限。在 OpenWebText 上，PGM 的训练吞吐量约为 MDLM 的 75%（Table 3），尽管推理速度优势足以弥补这一开销。

5. **蒸馏策略的适配性**：当前蒸馏直接借用 MGM 的方法（将一组视为 `[MASK]`），专门为 PGM 设计的蒸馏方法仍有待探索。

### 开放问题

1. **互补掩码的上下文长度效应**：为什么互补掩码在 LM1B（上下文 128）上改善显著，而在 OpenWebText（上下文 1024）上提升有限？这可能与长序列下组间信息冗余度变化有关，但缺乏严格的理论分析。

2. **PGM 专用蒸馏方法**：能否设计利用 PGM 分区结构的蒸馏策略，进一步压缩步数并提升生成质量？

3. **多模态扩展**：PGM 的分区机制能否在多模态场景（如文本到图像、视频生成）中扩展应用？组间信息隔离的设计在跨模态条件下是否仍有效？

4. **训练稳定性的理论解释**：互补掩码引入的损失尖峰是否源于梯度冲突（两组预测方向不一致）？如何在大规模模型上管理这一现象？

5. **专用计算优化**：可否开发针对块对角注意力模式的专用高效 kernel，以缩小训练吞吐量与 MDLM 的差距？

6. **方差缩减的理论分析**：PGM 的双重梯度信号降低训练方差的机制目前仅凭经验验证，能否从优化理论角度给出更严格的分析？

## 原文 PDF

![[paperPDFs/ICLR_2026/Partition_Generative_Modeling_Masked_Modeling_Without_Masks.pdf]]
