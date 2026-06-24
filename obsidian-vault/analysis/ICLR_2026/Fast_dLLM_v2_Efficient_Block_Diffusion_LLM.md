---
title: "Fast-dLLM v2: Efficient Block-Diffusion LLM"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Fast_dLLM_v2_Efficient_Block_Diffusion_LLM.pdf
openreview_forum_id: 1NZ3DHF9nT
aliases:
- FDV
- FDVEBDL
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "块感知注意力掩码与互补掩码训练方案，在保留AR模型自回归结构的基础上，通过块内双向扩散和块间因果建模，使预训练模型仅需少量微调即可转换为块扩散模型，并利用分层缓存实现高效并行解码。"
primary_logic: "通过将序列划分为固定大小的块，在每个块内进行掩码扩散和双向上下文建模，而在块之间保持自回归因果关系，可以最大限度地复用预训练AR模型的权重和表示，并以极少的微调数据（~1B tokens）实现无损自适应；配合块级KV缓存和子块双缓存，推理时能获得最高2.5倍的加速，同时匹配或超越原AR模型的基准性能。"
claims:
- "Fast-dLLM v2 只需约1B tokens微调即可实现无损自适应，而Dream需约500B tokens。"
- "Fast-dLLM v2 在GSM8K上以0.9置信度阈值实现2.6倍加速，且精度损失极小。"
- "Fast-dLLM v2 (7B) 在多个基准上平均得分60.3，超越同数据微调的AR基线 Qwen2.5-7B-Nemo-FT (58.2) 和扩散基线 Dream (57.6)。"
- "互补掩码和填充策略（+pad+CM）使平均准确率提升+3.7点，超过朴素token移位方法。"
---

# Fast-dLLM v2: Efficient Block-Diffusion LLM

> [!tip] 核心洞察
> 通过将序列划分为固定大小的块，在每个块内进行掩码扩散和双向上下文建模，而在块之间保持自回归因果关系，可以最大限度地复用预训练AR模型的权重和表示，并以极少的微调数据（~1B tokens）实现无损自适应；配合块级KV缓存和子块双缓存，推理时能获得最高2.5倍的加速，同时匹配或超越原AR模型的基准性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Fast-dLLM v2：高效块扩散语言模型 |
| 英文题名 | Fast-dLLM v2: Efficient Block-Diffusion LLM |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1NZ3DHF9nT); [Project](https://nvlabs.github.io/Fast-dLLM/v2/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Fast-dLLM v2 |
| Dataset | GSM8K, HumanEval Base, Average (Avg.), Throughput on A100 |

> [!tip] 效果简介
> - GSM8K 上，accuracy 为 83.7 (Fast-dLLM v2 7B, best variant)，对比 71.4 (Qwen2.5-7B-Nemo-FT)，变化 +12.3。
> - HumanEval Base 上，pass@1 为 63.4 (Fast-dLLM v2 7B, best variant)，对比 51.2 (Qwen2.5-7B-Nemo-FT)，变化 +12.2。
> - Average (Avg.) 上，score 为 60.3 (Fast-dLLM v2 7B, best variant)，对比 58.2 (Qwen2.5-7B-Nemo-FT)，变化 +2.1。

## 概述

大语言模型的自回归（AR）解码范式以逐词串行生成为代价换取了强大的文本质量，这从根本上限制了推理并行度和吞吐上限。扩散语言模型（dLLM）虽能并行解码，但其普遍采用的双向注意力破坏了因果结构，导致无法有效复用KV缓存，推理效率反而不及AR模型。**Fast-dLLM v2** 的核心洞察在于：将序列切分为固定大小的块，在块内执行掩码扩散与双向上下文建模，而在块间保留严格的自回归因果关系——这一“块感知混合注意力”设计使预训练AR模型的权重与表示得以最大程度复用，仅需约**1B tokens**微调即可实现无损自适应，远低于Dream所需的约500B tokens。

在方法层面，Fast-dLLM v2 构建了一套完整的训练-推理协同优化体系：训练时采用互补掩码策略确保每个token均在可见与掩码两种上下文下被监督，配合移位标签预测保留AR模型的表示结构；推理时通过块级KV缓存复用已解码块，并在当前块内引入子块双缓存（DualCache）与置信度感知并行解码，实现高效的块间串行、块内并行生成。

实验表明，Fast-dLLM v2 (7B) 在多个基准上平均得分**60.3**，超越同数据微调的AR基线 Qwen2.5-7B-Nemo-FT（58.2）和扩散基线 Dream（57.6）；在GSM8K上以0.9置信度阈值实现**2.6倍**加速且精度损失极小，吞吐量达到**102.5 tokens/s**（A100，batch=1），较Qwen2.5-7B-Instruct提升2.54倍。消融研究进一步验证了互补掩码与填充策略（合计提升+3.7个平均准确率点）、子块解码以及分层缓存的关键作用。

## 背景与动机

自回归（Autoregressive, AR）大语言模型通过逐词顺序解码生成文本，这一机制从根本上限制了推理并行度。在标准自回归框架下，每个新token的生成必须等待之前所有token完成计算，导致长序列生成时吞吐量受限于单步延迟，无法充分利用现代GPU的并行计算能力。

为突破这一瓶颈，扩散语言模型（Diffusion Language Models, dLLMs）被提出作为替代方案。其核心思想是并行生成多个token，通过迭代去噪逐步恢复完整序列。然而，现有扩散语言模型普遍采用双向（全注意力）架构，这与主流AR模型的因果注意力结构存在根本性差异。这种结构差异带来两个关键问题：**其一**，双向注意力使得模型无法有效利用KV缓存（Key-Value Cache）——这是AR推理加速的核心技术——导致推理效率反而低于预期；**其二**，从零训练一个高质量的扩散语言模型需要海量数据和计算资源，例如Dream（Ye et al., 2025a）需要约500B tokens才能达到可用性能。

因此，该领域的核心矛盾在于：**如何在保持生成质量的前提下，将AR模型的成熟生态（预训练权重、缓存机制、推理优化）迁移到可并行解码的扩散框架中？** 现有方法要么牺牲了缓存效率（如全注意力dLLMs），要么需要高昂的从头训练成本，难以在实际部署中实现“无损加速”。

Fast-dLLM v2 正是针对这一困境提出的解决方案。其动机直指一个关键洞察：**通过将序列划分为固定大小的块，在块内进行双向扩散建模、块间保持自回归因果关系，可以最大程度地复用预训练AR模型的权重和表示结构。** 这种“块感知”的注意力设计使得预训练模型仅需约1B tokens的微调即可转换为块扩散模型——相比Dream所需的约500B tokens，数据效率提升了近500倍——同时天然兼容KV缓存机制。配合块级分层缓存和置信度感知并行解码，该方法在推理时能获得最高2.5倍的加速，且基准性能匹配甚至超越原AR模型。

## 核心创新

Fast-dLLM v2 的核心创新在于**以极低成本将预训练自回归（AR）大语言模型转换为块扩散模型，在保留生成质量的同时实现最高2.5倍的推理加速**。这一目标通过三个紧密耦合的技术槽位实现：块感知注意力掩码、互补掩码训练方案，以及分层缓存并行解码机制。

### 1. 块感知注意力掩码：从因果到混合的平滑过渡

传统AR模型使用因果注意力掩码（causal mask），确保每个token只能关注其前序token；而现有扩散语言模型（如**Dream**, Ye et al., 2025a；**LLaDA**, Nie et al., 2025）采用全双向注意力，彻底抛弃了自回归结构，导致无法利用KV缓存，推理效率低下，且需从零开始训练或海量数据微调（Dream需约500B tokens）。

Fast-dLLM v2 提出**块感知混合注意力掩码**，将序列划分为固定大小的块（block size=32），在块内进行双向自注意力建模，在块间保持自回归因果关系。具体而言，该掩码由三个子掩码构成（见公式分解，附录A.2）：
- **块对角掩码** $\mathcal{M}_{BD}$：允许噪声序列中同一块内所有token进行双向注意力，实现块内上下文充分交互。
- **偏移块因果掩码** $\mathcal{M}_{OBC}$：允许噪声token关注之前块中的干净token，建立跨块因果条件依赖。
- **块因果掩码** $\mathcal{M}_{BC}$：使干净序列中每个token关注所有先前及当前块，模拟自回归生成过程。

这一设计的关键洞察在于：**块内扩散、块间自回归的结构与原始AR模型的注意力模式高度兼容**，因此预训练权重和表示可以被最大限度地复用。实验表明，Fast-dLLM v2 仅需约1B tokens微调即可实现“无损自适应”（lossless adaptation），而Dream需约500B tokens——数据效率提升约500倍（置信度0.95）。

### 2. 互补掩码与移位标签训练方案

传统掩码扩散语言模型仅对被掩码token计算损失，导致每个训练样本中仅有部分token获得监督信号。Fast-dLLM v2 引入**互补掩码策略**：每个训练样本被复制为两个视图，分别使用掩码 $m$ 和其互补掩码 $\bar{m} = 1 - m$，确保序列中每个token在两个视图之一中处于被掩码状态，从而**所有token均获得监督**，无需额外归一化系数（附录A.3）。

同时，为保留AR模型的表示结构，采用**移位标签策略**：预测位置 $i$ 的被掩码token时，使用位置 $i-1$ 的隐含状态输出logit。这使模型在块扩散框架下仍能复用原始AR模型的“前一位置预测当前位置”的表示能力。

消融实验（Table 2）证实了该方案的有效性：
- 朴素token移位策略：平均准确率41.3
- 添加填充策略（+pad，防止跨样本注意力泄漏）：42.2（+0.9）
- 进一步引入互补掩码（+CM）：45.0（+3.7，相比朴素策略）

**完整方案（+pad+CM）在所有基准上实现最佳或次佳性能**，平均准确率提升+3.7点（置信度0.95）。

### 3. 分层缓存与置信度感知并行解码

推理阶段的核心创新在于**分层缓存机制**与**置信度感知并行解码**的协同设计：

- **块级KV缓存**：已完全解码的块将其KV表示缓存为只读上下文，后续块可直接复用，避免跨块重复计算。
- **子块双缓存（DualCache）**：在部分解码的块内，维护前缀和后缀KV缓存，加速迭代去掩码过程。子块大小可灵活设置（默认为8），在训练-推理块大小一致性约束下实现细粒度控制。
- **置信度感知并行解码**：块内所有被掩码token并行预测，预测置信度超过阈值（如0.9）的token立即解码并去掩码，低于阈值的保持掩码状态进入下一轮迭代。当阈值设为1.0时，退化为标准非并行解码。

该机制在GSM8K上以阈值0.9实现2.6倍加速（39.1→101.7 tokens/s），且精度损失极小（Figure 4，置信度0.95）。在H100上批量大小为64时，相比AR基线实现1.8倍吞吐量提升（Figure 5，置信度0.95）。子块缓存在大批量（32）下显著提升吞吐量，且对准确率无影响（Figure 6，置信度0.95）。

### 创新总结

Fast-dLLM v2 的创新本质是**通过块结构在AR模型和扩散模型之间建立了一座桥梁**：训练时以块为粒度进行双向上下文建模，推理时以块为单位进行自回归生成和缓存复用。这一设计使得预训练AR模型仅需极少微调即可转换为高效的块扩散模型，在多个基准上匹配或超越原AR模型性能（7B变体平均得分60.3，超越同数据微调的Qwen2.5-7B-Nemo-FT的58.2和Dream的57.6，Table 1），同时实现最高2.5倍推理加速。

## 整体框架

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/003_Figure_2.jpg]]
*Figure 2: Training process of Fast-dLLM-v2. The input sequence is decoded block by block. Within each block, the model performs next-token prediction with partial masking. To ensure every token is trained, complementary masks are introduced so that masked tokens in one view can be predicted from the other. We only apply loss to predicted tokens that are highlighted in green, and dashed curves connect Mask tokens to their corresponding predictions*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of the inference process. The sequence is decoded block-by-block. The decoded blocks are cached to speed up inference. Within each block, we adopt the parallel decoding and DualCache in Fast-dLLM to further accelerate inference*

Fast-dLLM v2 的核心设计思路是将预训练的自回归（AR）大语言模型转换为块扩散模型，从而在保持生成质量的同时获得推理并行度。整个框架分为**训练管线**与**推理管线**两大阶段，二者共享同一套块感知注意力机制，但输入输出流和缓存策略有所不同。

### 训练管线

训练管线建立在预训练 Qwen2.5-Instruct 模型（1.5B 和 7B）之上，仅需约 1B tokens 的微调数据即可实现无损自适应。其输入输出流如下：

1. **序列预处理**：将原始文本序列按固定块大小（$B=32$）进行块对齐打包，并在必要时填充非损失承载的 `<MASK>` token，使序列长度为块大小的整数倍，防止跨样本注意力泄漏。

2. **互补掩码生成**：对每个训练样本采样一个随机二进制掩码 $m$，并生成互补掩码 $\bar{m}=1-m$。原始序列被复制为两份视图——一份以 $m$ 掩码，另一份以 $\bar{m}$ 掩码——确保序列中每个 token 都在训练中被监督。

3. **噪声-干净序列拼接**：将噪声序列 $x_t$ 与对应的干净序列 $x_0$ 沿序列维度拼接，形成总长为 $2L$ 的联合输入，在单次前向传播中同时处理。

4. **块感知注意力掩码**：联合输入通过一个由三部分组成的注意力掩码矩阵处理：
   - **块对角掩码** $\mathcal{M}_{BD}$：允许噪声序列中同一块内所有 token 进行双向自注意力（块内双向上下文建模）。
   - **偏移块因果掩码** $\mathcal{M}_{OBC}$：允许噪声 token 关注之前块中的干净 token（跨块因果条件依赖）。
   - **块因果掩码** $\mathcal{M}_{BC}$：使干净序列中每个 token 关注所有先前及当前块（模拟自回归生成）。

5. **移位标签预测**：对每个被掩码位置 $i$，使用前一位置 $i-1$ 的隐含状态预测 token $x_0^i$，从而最大限度地复用预训练 AR 模型的表示。

6. **损失计算**：仅对被掩码 token 计算交叉熵损失，不施加归一化系数。互补掩码下的总损失为两个时刻 $t$ 和 $1-t$ 的掩码 token 预测损失之和，每个样本总贡献 token 数为 $L$。

### 推理管线

推理时采用逐块自回归解码，结合分层缓存和置信度感知并行解码实现加速。其输入输出流如下：

1. **块级自回归解码**：生成过程逐块推进。每个块首先被完全掩码，然后通过多步去噪迭代逐步揭示 token。

2. **分层缓存机制**：
   - **块级 KV 缓存**：已完全解码的块被缓存为只读上下文，后续块直接复用其 KV 表示，避免重复计算。
   - **子块双缓存（DualCache）**：在部分解码的块内，维护前缀和后缀 KV 缓存，加速迭代式置信度感知解码。

3. **置信度感知并行解码**：在当前块内，所有仍被掩码的 token 并行预测。当某个 token 的预测置信度超过预设阈值时，该 token 被解码并去掩码；低于阈值的 token 保持掩码状态，进入下一轮细化。阈值设为 1.0 时恢复标准非并行解码。

4. **子块解码**：引入子块解码策略，允许在推理时灵活控制解码粒度，同时保持与训练块结构的一致性，解决训练-推理块大小不匹配导致的性能退化问题。

### 模块关系总览

整个框架的核心模块及其协作关系如下：

| 模块 | 阶段 | 功能 |
|------|------|------|
| 块填充与打包工具 | 训练 | 序列对齐与防泄漏 |
| 互补掩码采样器 | 训练 | 生成互补掩码对，确保全 token 监督 |
| 块感知注意力掩码施加器 | 训练/推理 | 构建块对角、偏移块因果和块因果注意力模式 |
| 移位标签预测器 | 训练 | 利用前一位置隐含状态预测当前掩码 token |
| 块级缓存管理器 | 推理 | 缓存已解码块的 KV 表示 |
| 子块双缓存引擎 | 推理 | 维护部分解码块的前后缀 KV 缓存 |
| 置信度感知并行解码器 | 推理 | 基于置信度阈值并行解码与去掩码 |

这种设计使 Fast-dLLM v2 能够以极少的微调代价，将预训练 AR 模型转化为高效的块扩散模型，在推理时获得最高 2.6 倍的加速，同时匹配或超越原 AR 模型的基准性能。

## 核心模块与公式推导

### 块扩散训练目标

Fast-dLLM v2 的核心训练目标建立在掩码扩散语言模型的期望损失之上，但进行了块感知改造。标准掩码扩散损失仅对被掩码token计算交叉熵，并按掩码比例 $t$ 进行反权重归一化：

$$\mathcal { L } ( \theta ) = - \mathbb { E } _ { t , x _ { 0 } , x _ { t } } \left[ \frac { 1 } { t } \sum _ { i = 1 } ^ { L } \mathbf { 1 } [ x _ { t } ^ { i } = \mathrm { [ M A S K ] } \big ] \log p _ { \theta } ( x _ { 0 } ^ { i } \mid x _ { t } ) \right]$$

Fast-dLLM v2 将其改造为**块扩散训练损失**，核心变化在于：仅对被掩码token计算交叉熵，但预测条件从“完整噪声序列”变为“前缀因果上下文 + 当前块内双向上下文”，且**省略归一化系数**：

$$\mathcal { L } _ { \mathrm { b l o c k } } ( \theta ) = - \mathbb { E } _ { x , m } \left[ \sum _ { i = 1 } ^ { L } \mathbf { 1 } [ x _ { t } ^ { i } = [ \boldsymbol { \mathrm { M A S K } } ] \ : ] \log p _ { \theta } ( x _ { 0 } ^ { i } \mid x _ { < i } , x _ { \mathrm { b l o c k } ( i ) } ) \right]$$

其中 $x_{<i}$ 表示位置 $i$ 之前的前缀token，$x_{\mathrm{block}(i)}$ 表示与位置 $i$ 处于同一块内的所有token。这一设计使模型在每个块内进行双向上下文建模，而在块间保持自回归因果关系，从而**最大限度地复用预训练AR模型的权重和表示**。

### 互补掩码策略

为确保训练中所有token均被监督，Fast-dLLM v2 引入**互补掩码策略**：每个训练样本被复制为两份视图，分别使用掩码 $m$ 及其互补掩码 $\bar{m} = 1 - m$。两个时刻 $t$ 和 $1-t$ 的被掩码token均参与损失计算，保证每个样本的总贡献token数为 $L$，无需额外归一化：

$$- \left[ \sum _ { i = 1 } ^ { L } \mathbf { 1 } [ x _ { t } ^ { i } = \mathrm { [ M A S K ] } ] \log p \theta ( x _ { 0 } ^ { i } \mid x _ { < i } , x _ { \mathrm { b l o c k ( i ) } } ) \right] + \left[ \sum _ { i = 1 } ^ { L } \mathbf { 1 } [ x _ { 1 - t } ^ { i } = \mathrm { [ M A S K ] } ] \log p \theta ( x _ { 0 } ^ { i } \mid x _ { < i } , x _ { \mathrm { b l o c k ( i ) } } ) \right]$$

消融实验证实，完整配方（+pad + CM）使平均准确率相比朴素token移位方法提升 **+3.7点**（Table 2），是方法有效性的决定性证据。

### 块感知注意力掩码分解

训练时的注意力掩码将噪声序列 $x_t$ 和干净序列 $x_0$ 沿序列维度拼接为总长 $2L$ 的输入，其完整掩码 $\mathcal{M}_{\mathrm{full}}$ 分解为三个子掩码（Figure 7, Appendix A.2）：

$$\mathcal { M } _ { \mathrm { f u l l } } = \left[ \begin{array} { c c c } { \mathcal { M } _ { B D } } & { \mathcal { M } _ { O B C } } \\ { 0 } & { \mathcal { M } _ { B C } } \end{array} \right]$$

- **块对角掩码** $\mathcal{M}_{BD}$：允许噪声序列中同一块内所有token进行双向自注意力。
$$[ \mathcal { M } _ { B D } ] _ { i j } = \left\{ \begin{array} { l l } { 1 } & { \mathrm { i f } \ i , j \mathrm { \ b e l o n g \ t o \ t h e \ s a m e \ b l o c k } } \\ { 0 } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

- **偏移块因果掩码** $\mathcal{M}_{OBC}$：允许噪声token关注之前块中的干净token，实现跨块因果条件依赖。
$$[ \mathcal { M } _ { O B C } ] _ { i j } = \left\{ \begin{array} { l l } { 1 } & { \mathrm { i f ~ } j \mathrm { ~ i s ~ i n ~ a ~ b l o c k ~ b e f o r e ~ } i } \\ { 0 } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

- **块因果掩码** $\mathcal{M}_{BC}$：使干净序列中每个token关注所有先前及当前块，模拟自回归生成。
$$[ M _ { B C } ] _ { i j } = \left\{ { \begin{array} { l l } { 1 } & { { \mathrm { i f ~ } } j { \mathrm { ~ i s ~ i n ~ t h e ~ s a m e ~ o r ~ a n ~ e a r l i e r ~ b l o c k ~ a s ~ } } i } \\ { 0 } & { { \mathrm { o t h e r w i s e } } } \end{array} } \right.$$

这一混合注意力结构是方法的核心因果旋钮：块内双向扩散提供并行解码能力，块间因果建模保留AR模型的自回归结构，使预训练模型仅需~1B tokens微调即可转换为块扩散模型。

### 移位标签预测

为保留AR模型“前一位置预测当前位置”的表示形式，Fast-dLLM v2 采用**移位标签策略**：对掩码位置 $i$ 的token预测，使用其前一位置 $i-1$ 的隐含状态产生的logit。这一设计使模型在训练目标上与原始AR模型的next-token prediction保持结构兼容，是实现**无损自适应**（lossless adaptation）的关键机制之一。

### 分层缓存与并行解码

推理阶段的核心模块包括：

- **块级KV缓存管理器**：已解码块的KV表示被缓存为只读上下文，后续块无需重复计算跨块注意力。
- **子块双缓存引擎**：在部分解码的块内维护前缀和后缀KV缓存（DualCache），加速迭代式的置信度感知解码。
- **置信度感知并行解码器**：在每个块内，预测置信度超过阈值的token被并行解码和去掩码，低于阈值的保持掩码状态等待后续迭代。阈值设为1.0时恢复标准非并行解码。

消融实验表明，子块缓存在大批量（32）下显著提升吞吐量，且对准确率无影响（Figure 6）；分层缓存在长上下文（1K-8K tokens）下延迟和吞吐与标准AR缓存相当（Figure 8）。

## 实验与分析

### 核心结果：推理加速与质量保持

Fast-dLLM v2 在多个基准上实现了推理吞吐量的显著提升，同时匹配或超越了同数据微调的自回归基线。在 A100 GPU 上，7B 模型以置信度阈值 0.9 进行并行解码时，吞吐量达到 101.7 tokens/s，相比阈值 1.0 时的标准解码（39.1 tokens/s）提升 **2.6 倍**，且 GSM8K 精度损失极小（图 4）。在 H100 上，批量大小为 64 时，扩散生成吞吐量比自回归基线高出 **1.8 倍**（图 5）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/006_Figure_4.jpg]]
*Figure 4: Accuracy and throughput under different thresholds on GSM8K. Threshold 0.9 is selected, offering a 2.6× speedup with minimal accuracy drop*

从基准得分来看，Fast-dLLM v2 7B 在多个任务上的平均得分为 **60.3**，超越了同数据微调的 Qwen2.5-7B-Nemo-FT（58.2）和全注意力扩散基线 Dream（57.6）（表 1）。在数学推理任务 GSM8K 上，最佳变体达到 **83.7**，比 Qwen2.5-7B-Nemo-FT（71.4）高出 12.3 分；在代码生成 HumanEval Base 上，pass@1 达到 **63.4**，比 Qwen2.5-7B-Nemo-FT（51.2）高出 12.2 分。1.5B 版本同样表现稳健，平均得分 45.0，优于同规模的 Qwen2.5-1.5B-Nemo-FT（41.3）和 Dream（41.5）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/005_Table_1.jpg]]
*Table 1: Benchmark results of various language models across a range of evaluation tasks. Models are grouped by parameter scale into 1B and 7B+ categories. Evaluation metrics include code generation (HumanEval, MBPP), mathematical reasoning (GSM8K, MATH), instruction following (IFEval), knowledge-intensive QA (MMLU, GPQA), and general average score (Avg.). ”Base” and ”Plus” refer to different evaluation settings for code benchmarks using EvalPlus. The best results per column are in bold, and the second-best are underlined. are evaluated using the LM-Eval framework, ensuring consistency and reliability of performance measurements across different tasks*

### 训练策略消融：互补掩码与填充的关键作用

表 2 的系统消融揭示了训练策略中各组件对性能的贡献。基线策略（朴素 token 移位）的平均准确率仅为 41.3。引入**填充策略**（+pad）后，平均准确率提升至 42.2——该策略将每个训练样本填充至块大小的整数倍，防止跨样本注意力泄漏。进一步加入**互补掩码**（+CM）后，平均准确率跃升至 **45.0**，相比朴素策略提升了 +3.7 点。互补掩码的核心机制是：每个训练样本被复制为两个视图，分别使用掩码 $m$ 和其互补掩码 $1-m$，确保序列中所有 token 都在训练中被监督，无需额外的损失归一化系数。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/008_Table_2.jpg]]
*Table 2: Benchmark results for different token shift strategies. ”+ CM” stands for ”+ complementary mask”. The best performance for each benchmark is shown in bold, while the second-best is underlined*

### 推理策略消融：子块解码与缓存机制

**子块大小选择**：表 3 显示，子块大小为 8 时获得最佳平均性能，但不同任务存在偏好差异——GSM8K 偏好较小的子块尺寸（2），而 HumanEval 在尺寸 8 时达到峰值。这一差异可能源于数学推理任务对局部上下文的更高敏感性。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/011_Table_3.jpg]]
*Table 3: Sub-Block size decoding improves performance, with size 8 being optimal*

**训练-推理块大小一致性**：表 4 揭示了一个关键约束：推理时直接改变块大小而不与训练对齐会导致性能大幅下降。例如，GSM8K 准确率从训练块大小 32 时的 62.0 降至不匹配时的 58.5。这一发现表明，块扩散模型的注意力模式与训练块结构强耦合，推理时需保持一致性或通过子块解码机制间接调整粒度。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/012_Table_4.jpg]]
*Table 4: Inference with mismatched sizes reduces performance*

**子块缓存效率**：图 6 展示了子块缓存在不同批量大小下的效果。在批量大小为 32 时，子块缓存显著提升吞吐量，且对准确率无影响。在长上下文场景（1K-8K tokens）下，分层缓存（块级 KV 缓存 + 子块 DualCache）的延迟和吞吐与标准自回归 KV 缓存相当，优于仅使用块缓存的方案（图 8）。

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/010_Figure_6.jpg]]
*Figure 6: Effect of small block size and sub-block cache on model performance. (a) Accuracy remains largely unaffected by the use of sub-block cache across different block sizes and batch sizes. (b) Throughput increases as small block size grows due to higher decoding parallelism. While sub-block cache has negligible effect when batch size is small, it significantly improves throughput under compute-bound settings (e.g., batch size = 32)*

### 加速-质量权衡

置信度感知并行解码是控制加速-质量权衡的核心旋钮。阈值设为 1.0 时恢复标准非并行解码，获得最高质量但无加速；阈值降至 0.9 时，GSM8K 上实现 2.6 倍加速且精度损失极小（图 4）。这一机制允许部署时根据场景需求灵活调节：对延迟敏感的应用可降低阈值获取更高吞吐，对精度要求严格的场景可提高阈值保证质量。

### 数据效率优势

Fast-dLLM v2 仅需约 **1B tokens** 的微调数据即可实现无损自适应，而 Dream 需要约 500B tokens。这一数量级差异源于方法设计的根本不同：Fast-dLLM v2 的块感知注意力掩码结构更接近原始自回归模型，使得预训练权重和表示能够被最大限度地复用，仅需少量微调即可完成从逐词因果解码到块内扩散解码的转换。

### 公平性说明

所有非代码基准测试使用 LM-Eval 框架，代码任务使用 EvalPlus 评估。除 GPQA 采用 5-shot 外，其余均为零样本设置，使用贪婪解码。推理时默认块大小 32、子块大小 8，并行解码阈值设为 1 以保持训练-推理一致性。微调数据为 LLaMA-Nemotron post-training dataset，基线模型 Qwen2.5-Nemo-FT 使用相同的指令微调数据和训练步数，确保可比性。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/002_Figure_1.jpg]]
*Figure 1: Performance comparison of Fast-dLLM v2. (a) Comparison of throughput and GSM8K accuracy among baseline models and the Fast-dLLM variants in A100. Fast-dLLM v2 (7B) achieves 2.54× higher throughput than Qwen2.5-7B-Instruct while offering comparable accuracy. Additionally, it improves accuracy by +5.2% over Fast-dLLM-LLaDA, which is based on optimized LLaDA. (b) Throughput comparison under different batch sizes. Fast-dLLM v2 significantly outperforms all baselines at both batch size 1 and 4, demonstrating superior scalability and efficiency*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/017_Table_5.jpg]]
*Table 5: Single-turn Dialogue Cases of Fast-dLLM v2 (7B)*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_1NZ3DHF9nT/figures/018_Table_6.jpg]]
*Table 6: Multi-turn Dialogue Cases of Fast-dLLM v2 (7B)*

## 方法谱系与知识库定位

### 方法演进脉络

Fast-dLLM v2 处于自回归（AR）语言模型与扩散语言模型（dLLM）的交叉地带，其核心设计动机来自两个方向的效率瓶颈：

1. **AR 模型的推理串行瓶颈**：Qwen2.5-Instruct（Qwen et al., 2025）等标准 AR 模型逐词解码，KV 缓存虽能复用前缀状态，但每步仅生成一个 token，推理并行度受限于序列长度。Fast-dLLM v2 直接以 Qwen2.5-1.5B-Instruct 和 Qwen2.5-7B-Instruct 为预训练基座，通过块级扩散改造突破这一限制。

2. **全注意力扩散模型的适配代价**：Dream（Ye et al., 2025a）采用全局双向注意力的掩码扩散框架，虽支持并行生成，但注意力结构与 AR 模型差异巨大，需约 500B tokens 微调才能实现“无损自适应”。LLaDA（Nie et al., 2025）同样基于掩码扩散，但未针对 AR 预训练权重复用进行优化。Fast-dLLM v2 通过块感知注意力掩码（块内双向 + 块间因果），将结构差异压缩到最小，仅需约 1B tokens 微调即可完成适配，数据效率提升约 500 倍。

3. **先前加速方案的缓存局限**：Fast-dLLM（Wu et al., 2025）提出了 DualCache 和块内并行解码，但缺乏块级分层缓存机制，无法在长序列场景下高效复用已解码块的 KV 状态。Fast-dLLM v2 在此基础上引入块级缓存与子块双缓存的分层架构，将加速能力从单块内扩展到跨块全局。

### 与基线方法的关系定位

| 方法 | 注意力机制 | 解码方式 | 与 Fast-dLLM v2 的关系 |
|------|-----------|---------|----------------------|
| Qwen2.5-Instruct（Qwen et al., 2025） | 因果自回归 | 逐词串行 | 预训练基座，提供初始权重和表示 |
| Dream（Ye et al., 2025a） | 全局双向 | 全序列并行扩散 | 同为 dLLM，但适配代价高（~500B tokens），Fast-dLLM v2 以块结构降低适配门槛 |
| LLaDA（Nie et al., 2025） | 全局双向掩码 | 迭代去掩码 | 同为掩码扩散，Fast-dLLM v2 在 GSM8K 上精度高出 +5.2%（Figure 1a） |
| Fast-dLLM（Wu et al., 2025） | 块内扩散 | 块内并行解码 | 直接前身，v2 新增分层缓存、互补掩码训练和子块解码 |

在 7B 规模上，Fast-dLLM v2 以平均得分 60.3 超越同数据微调的 AR 基线 Qwen2.5-7B-Nemo-FT（58.2）和扩散基线 Dream（57.6）（Table 1），证明块扩散结构在保持生成质量的同时具备竞争力。

### 方法适用边界

1. **训练-推理块大小一致性约束**：模型在训练时块大小固定为 32，推理时若直接改变块大小而不启用子块解码，性能会显著下降——GSM8K 从 62.0 降至 58.5（Table 4）。子块解码机制部分缓解了这一限制，但最优子块大小（8）仍需通过消融实验确定。

2. **吞吐量优势的批量依赖性**：在单 batch 场景下，Fast-dLLM v2 相较 AR 基线可获得约 2.6 倍加速（A100, batch=1, threshold=0.9）；大批量（64）时加速比降至约 1.5-1.8 倍（Figure 5），因为 AR 解码的批量并行化本身已能利用 GPU 算力。

3. **置信度阈值的质量-速度权衡**：并行解码通过置信度阈值控制 token 提前释放，阈值 1.0 恢复标准非并行解码（无加速），阈值 0.9 在 GSM8K 上实现 2.6 倍加速且精度损失极小（Figure 4）。更低阈值可进一步提升吞吐量，但精度下降曲线需根据具体任务评估，论文未给出通用阈值建议。

4. **模型规模与任务类型**：当前验证集中于 1.5B 和 7B 的 Qwen2.5 架构，覆盖代码生成（HumanEval, MBPP）、数学推理（GSM8K, MATH）和通用指令遵循（IFEval, MMLU, GPQA）。对更大规模模型（>7B）或其他架构（如 LLaMA-3.2, SmolLM-2）的迁移效果尚未验证。

### 局限与开放问题

1. **长序列生成的缓存效率边界**：分层缓存在 1K-8K tokens 范围内延迟和吞吐与标准 AR 缓存相当（Figure 8），但超过 8K 后缓存管理开销是否线性增长，论文未提供数据。块级缓存需要在每个块边界进行状态切换，极长序列下这一开销可能侵蚀加速收益。

2. **互补掩码的计算冗余**：训练时每个样本被复制为互补掩码的两个视图，有效序列长度翻倍至 2L，虽确保所有 token 被监督，但也使单步前向计算量翻倍。论文未讨论这一冗余是否可通过更高效的掩码调度策略缩减。

3. **子块大小的任务敏感性**：消融实验显示 GSM8K 偏好较小子块（2），HumanEval 偏好尺寸 8（Table 3），表明最优子块大小可能与任务的结构特性（如推理链长度、代码块粒度）相关。目前缺乏自动选择子块大小的机制。

4. **扩散步数的自适应调度**：当前并行解码使用固定置信度阈值判断 token 是否提前释放，但未探索动态调整扩散步数（如根据序列位置或上下文复杂度变化去掩码步数）。这可能是进一步提升效率的方向。

5. **与其他加速技术的兼容性**：论文未讨论块扩散框架与投机解码（speculative decoding）、模型量化、FlashAttention 等技术的组合效果。分层缓存与这些技术的交互可能存在非平凡的工程挑战。

6. **训练数据偏差**：微调使用 LLaMA-Nemotron post-training dataset，基线 Qwen2.5-Nemo-FT 使用相同数据和步数以保证可比性。但该数据集的具体构成和分布未详细披露，可能影响结论的外部有效性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Fast_dLLM_v2_Efficient_Block_Diffusion_LLM.pdf]]
