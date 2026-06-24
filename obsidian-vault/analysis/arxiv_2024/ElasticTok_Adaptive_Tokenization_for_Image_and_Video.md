---
title: "ElasticTok: Adaptive Tokenization for Image and Video"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/ElasticTok_Adaptive_Tokenization_for_Image_and_Video.pdf
project_link: https://largeworldmodel.github.io/elastictok/
code_link: https://github.com/LargeWorldModel/ElasticTok
aliases:
- ElasticTok
tags:
- arxiv_2024
- topic/vision_multimodal_applications
core_operator: 训练中随机截断尾部 token 的掩码策略，迫使模型根据输入内容自适应分配 token 数量，从而实现变长编码。
primary_logic: 通过在前帧条件下随机掩盖 token 序列的后段，让编码器学会将关键信息压缩到剩余 token 中，并根据重建难度自动分配不同数量的 token。
claims:
- 在图像和视频重建中，ElasticTok 在达到相同重建满足率时所需的 token 数量仅为固定 token 基线的 1/5 到 1/1.3，展示了自适应标记化的显著效率优势。
- 移除编码器对 token 掩码的条件会轻微降低重建质量，但可使推断速度提升 2 倍，证实了条件机制在质量和速度之间的因果作用。
- ImageNet (图像重建, FSQ) 上 Token efficiency (满足给定 MSE 阈值的样本比例 vs token 使用百分比) = 3.5x (较宽松阈值) / 1.3x (较严格阈值) 效率提升
- 视频 (FSQ) 上 Token efficiency (满足给定 MSE 阈值的样本比例 vs token 使用百分比) = 5x (较宽松) / 2.4x (较严格) 效率提升
---

# ElasticTok: Adaptive Tokenization for Image and Video

> [!tip] 核心洞察
> 通过在前帧条件下随机掩盖 token 序列的后段，让编码器学会将关键信息压缩到剩余 token 中，并根据重建难度自动分配不同数量的 token。

| 字段 | 内容 |
|------|------|
| 中文题名 | ElasticTok：图像与视频的自适应标记化 |
| 英文题名 | ElasticTok: Adaptive Tokenization for Image and Video |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2410.08368) · [Project](https://largeworldmodel.github.io/elastictok/) · [Code](https://github.com/LargeWorldModel/ElasticTok) |
| Topic | #topic/vision_multimodal_applications |
| Method | ElasticTok |
| Dataset | ImageNet, 多模态 VQA |

> [!tip] 效果简介
> - ImageNet (图像重建, FSQ) 上，Token efficiency (满足给定 MSE 阈值的样本比例 vs token 使用百分比) 3.5x (较宽松阈值) / 1.3x (较严格阈值) 效率提升 vs 固定 100% token (4096) (相对基线 token 用量降低约 71% 和 23%)。
> - 视频 (FSQ) 上，Token efficiency (满足给定 MSE 阈值的样本比例 vs token 使用百分比) 5x (较宽松) / 2.4x (较严格) 效率提升 vs 固定 100% token (相对基线 token 用量降低约 80% 和 58%)。
> - 多模态 VQA (GQA, POPE, MSVD, MSRVTT) 上，Accuracy Ours: 54%, 82%, 52%, 37% vs Baseline (固定 100% token): 54%, 82%, 53%, 37% (持平或略低（差异在 1% 以内）)。

## 概述

### 问题瓶颈

当前视觉 tokenizer 普遍采用**固定长度编码**，无论输入内容的复杂程度如何，均分配相同数量的 token。这一设计在长视频建模中暴露出根本性效率矛盾：简单场景（如静态背景）浪费大量 token，而复杂场景（如快速运动、密集纹理）却因 token 预算固定而丢失关键信息。该瓶颈直接制约了长视频理解的扩展性——当序列长度增长时，固定 token 策略的计算开销线性膨胀，但信息收益并不对等。

### 核心方法

**ElasticTok** 提出了一种训练时即内建自适应能力的变长 tokenization 框架。其核心机制是**随机尾部截断掩码**：在训练过程中，对每帧编码后的 token 序列，均匀采样保留数量 $\ell \sim U(\{M_{min}, \dots, M_{max}\})$，并仅将前 $\ell$ 个 token 送入解码器重建。这一策略迫使编码器学会将关键信息压缩到序列前部，使模型天然具备根据内容复杂度分配不同数量 token 的能力。编码器还可选择性地接受掩码条件（通过可学习嵌入融入），以进一步提升编码质量，尽管这会带来约 2 倍的推断速度代价。

### 方法谱系与知识库定位

ElasticTok 属于**自适应视觉 tokenization** 这一新兴方向，其方法定位介于两类工作之间：

- **固定 token 自编码器**（如 VAE、FSQ 等标准视觉 tokenizer）：ElasticTok 直接复用其编码器-解码器架构（ViT backbone），仅在训练中引入掩码采样机制，使其获得变长编码能力。基线对比即采用相同架构但使用固定全量 token 的版本。
- **动态计算分配方法**：不同于在模型前向过程中动态决定计算量，ElasticTok 将自适应能力**内化于 tokenizer 训练阶段**，推断时可根据目标重建阈值选择最优 token 数，支持二分搜索、分箱搜索和神经回归等多种搜索策略。

在知识库层面，ElasticTok 的贡献在于**将“计算效率”问题转化为“编码压缩”问题**——通过训练目标的重新设计（随机掩码），使标准自编码器无需架构改动即可获得内容自适应的变长表示，为长视频的高效建模提供了一种即插即用的 tokenization 方案。

### 主要结果概要

- **重建效率**：在 ImageNet 图像重建中，达到相同重建满足率时，ElasticTok 所需 token 仅为固定 token 基线的 **1/5 到 1/1.3**（较宽松阈值下 3.5× 效率提升，较严格阈值下 1.3× 提升）；在视频重建中，效率提升更为显著，达到 **5× 和 2.4×**（Figure 4）。
- **表示质量**：在下游多模态 VQA 任务（GQA、POPE、MSVD、MSRVTT）上，ElasticTok 与固定 100% token 基线的准确率**持平或仅差 1% 以内**（Table 1），证明自适应标记化未损害学到的视觉表示质量。
- **推断灵活性**：用户可根据计算预算灵活调整 token 使用比例，在精度与效率之间实现连续权衡（Figure 7）。

### 局限与开放问题

- 极长序列（如 1M tokens）的尾部重建略低于固定 token 基线，可能源于训练不充分或不同长度下全局/局部特征需求的冲突。
- 当前未采用 GAN 损失，可能限制生成质量，但在极长序列训练中 GAN 的稳定性是已知挑战。
- 方法仅在视觉模态（图像/视频）上验证，向音频、决策轨迹等时序模态的扩展尚待探索。
- 极低 token 数（$M_{min}$ 以下）训练不稳定，需设置下限保护。

## 背景与动机

### 视觉标记化的效率瓶颈

现代视觉生成模型——无论是自回归的 Transformer 还是扩散模型——普遍依赖一种“标记化-重建”范式：先将高维图像或视频帧压缩为固定数量的离散或连续 token，再由生成模型在这些 token 上建模。这一范式在图像生成和短视频理解中取得了显著成功，但其固定长度的编码策略正日益成为长视频建模的瓶颈。

**核心矛盾在于信息密度与编码预算的错配。** 视频内容的信息复杂度在时间维度上剧烈波动：静止的背景区域、缓慢的镜头平移仅需极少 token 即可忠实重建，而快速运动、纹理丰富的场景或密集的文字信息则要求更高的编码精度。固定 token 数量的编码器无法感知这种差异——它要么为简单帧浪费大量冗余 token，要么在复杂帧上因编码容量不足而丢失关键信息。在长视频场景下，这种“一刀切”策略导致计算开销随帧数线性增长，却无法保证重建质量的均匀性，严重制约了视频生成和理解的扩展性。

### 现有方法的局限

当前主流的视觉 tokenizer 可分为两类：**离散 tokenizer**（如 VQ-VAE 及其变体 FSQ）和**连续 tokenizer**（如 VAE）。无论哪种实现，它们都继承了一个共同假设：每帧输出固定数量的 token。以 FSQ 为例，编码器将输入帧映射为 $N$ 个潜在向量，解码器再从中重建原图——$N$ 在训练和推断中始终不变。

这种设计在图像任务中尚可接受，但在视频领域暴露了两个结构性问题：

1. **计算冗余**：即使视频中大量帧几乎静态，仍需为每帧分配等量 token，导致注意力计算和存储开销线性膨胀。
2. **表示质量不均**：固定预算下，编码器被迫在“全局结构保留”和“局部细节刻画”之间做折中，无法根据内容自适应倾斜资源。

已有工作尝试通过时序压缩或 token 剪枝缓解上述问题，但这些方法本质上仍是在固定编码长度的框架内做后处理，未能从根本上赋予模型自适应分配编码预算的能力。

### 本文动机

ElasticTok 的出发点是一个直观但未被充分探索的问题：**能否让 tokenizer 学会“按需编码”——根据输入帧的信息复杂度，自动决定使用多少 token？**

这一动机源于两个关键观察：

- **条件编码的可能性**：在视频序列中，前帧已为当前帧提供了丰富的上下文信息。一个理想的编码器应能利用这种条件依赖，将“新信息”压缩到更少的 token 中，而非从头编码每一帧。
- **掩码训练的因果机制**：如果在训练时随机截断 token 序列的尾部，模型将被迫把最重要的信息优先排列在序列前端。这种“压缩压力”可以驱动编码器形成自然的优先级排序，使 token 数量成为可调节的连续控制变量，而非固定超参数。

ElasticTok 的核心假设是：通过在前帧条件下随机掩盖 token 序列的后段，编码器将学会将关键信息压缩到剩余 token 中，并根据重建难度自动分配不同数量的 token。这一机制将 token 数量从架构约束转变为数据驱动的自适应变量，为长视频的高效建模开辟了新路径。

## 核心创新

ElasticTok 的核心创新在于将传统视觉 tokenizer 的**固定长度编码**转变为**内容自适应的变长编码**，使 token 分配从“一刀切”转变为“按需分配”。这一转变通过三个相互配合的机制实现，每个机制对应一个关键的 changed slot。

### 创新一：随机尾部截断掩码——迫使模型学会优先级排序

传统 tokenizer 对每帧分配固定数量 $N$ 个 token。ElasticTok 在训练时引入随机掩码策略：对每个训练样本，从支持范围 $[M_{min}, M_{max}]$ 中均匀采样保留的 token 数量 $\ell$，然后仅保留编码器输出 $z$ 的前 $\ell$ 个 token，丢弃尾部：

$$\ell \sim U(\{M_{min}, \dots, M_{max}\})$$
$$z_m = z \odot m$$

这一设计的因果逻辑是：**通过随机截断尾部 token，迫使编码器在训练中学会将最重要的信息优先压缩到序列前部的 token 中**。当截断较多时，模型必须用更少的 token 表达全局结构和低频信息；当截断较少时，模型可以用更多 token 补充高频细节。这种“随机难度”训练使模型天然获得了根据内容复杂度自适应分配 token 的能力。

### 创新二：编码器掩码条件——质量与速度的因果开关

ElasticTok 将掩码 $m$ 显式注入编码器，通过可学习的嵌入向量将掩码信息融入编码过程。这使得编码器能够“知道”自己将保留多少 token，从而在编码阶段就做出适应性调整。

消融实验（Table 5）揭示了这一设计的因果效应：**移除掩码条件后，视频重建满足率从 79.6% 下降至 75.3%（在 0.003 MSE 阈值下），但推断速度提升 2 倍**。这表明掩码条件是一个“质量-速度”的因果旋钮——编码器利用掩码信息进行更优的信息压缩，但代价是需要为每个候选 $\ell$ 值重新运行编码器；无条件模式下编码器只需运行一次，解码器可共享中间结果，从而大幅加速推断。

### 创新三：自适应推断——从固定输出到按需搜索

传统 tokenizer 推断时使用固定的 token 数量。ElasticTok 支持多种自适应推断策略：
- **基于指定编码长度**：用户直接给定目标 token 数量
- **基于目标重建阈值**：自动搜索满足重建质量要求的最小 token 数
- **多目标损失**：可切换不同损失函数（如 MSE 或 CLIP 余弦距离）来引导 token 分配偏好，例如优先保证文本清晰度（Figure 8）

搜索算法提供了精度-速度的灵活权衡：全搜索（Full Search）误差为 0% 但需要 4096 次函数评估，而神经回归（Neural Regression）仅需 1 次评估但误差约 9%（Table 2）。这种多层次的推断灵活性使 ElasticTok 能够适应从离线高质量编码到实时低延迟应用的不同场景。

### 创新的本质：从“固定预算”到“自适应预算”

三个 changed slot 共同实现了一个根本转变：**将 token 预算从训练时固定、推断时不可调，变为训练时随机化、推断时可搜索**。训练时的随机掩码让模型内化了“用更少 token 做更多事”的能力，推断时的搜索机制则让用户可以根据实际需求在质量和效率之间做出显式权衡。这种设计使 ElasticTok 在图像重建上以 1/3.5 到 1/1.3 的 token 用量达到固定 token 基线的同等重建满足率，在视频上更是达到 1/5 到 1/2.4 的 token 节省（Figure 4），同时在下游 VQA 任务中保持与基线持平的表现（Table 1）。

## 整体框架

ElasticTok 的核心设计理念是将固定长度的视觉 tokenizer 改造为内容自适应的变长编码器，其整体框架围绕一个统一的编码器-解码器流水线构建，并通过随机掩码训练策略赋予模型弹性分配 token 的能力。框架分为单块（Single Block）和多块（Multi Block）两种模式，分别处理短序列和长视频场景。

### 单块模式

单块模式采用标准的 Encoder-Decoder 架构，包含三个核心模块：

1. **编码器（Encoder）**：基于 ViT 架构，接收输入帧 $x$ 和可选的掩码条件 $m$，将其编码为潜在表示 $z$。掩码条件通过可学习的嵌入向量融入编码器，使模型在编码阶段就感知到哪些 token 将被保留。

2. **掩码采样器（Mask Sampler）**：训练时从预设范围 $[M_{\text{min}}, M_{\text{max}}]$ 中均匀采样保留的 token 数量 $\ell$，并生成二进制前缀掩码 $m$（前 $\ell$ 个位置为 1，其余为 0）。掩码作用于编码器输出：

   $$z_m = z \odot m$$

   这一操作迫使编码器将关键信息压缩到前 $\ell$ 个 token 中，而后部 token 被随机丢弃，从而学会按信息重要性排序编码。

3. **解码器（Decoder）**：同样基于 ViT，接收掩码后的潜在表示 $z_m$，重建原始帧 $\hat{x}$。训练损失为标准重建损失（MSE），不依赖 GAN 损失以保证长序列训练的稳定性。

### 多块模式

为处理长视频，多块模式将视频切分为多个块（block），并在单块架构基础上引入**块因果掩码（Block Causal Mask）**。每个块的编码器可访问当前块及之前所有块的上下文信息，形成块级自回归编码。推断时，每个块独立执行自适应 token 搜索，并利用类似语言模型中的 KV-cache 机制实现块间高效缓存，避免重复计算。

### 推断时的自适应搜索

训练完成后，模型支持多种推断策略以根据目标重建质量动态确定 token 数量：

- **完整搜索（Full Search）**：遍历所有可能的 token 数量，选择满足重建阈值的最小值，精度最高但计算开销大（需 4096 次函数评估）。
- **分箱搜索（Binned Search）**：将 token 空间划分为若干区间，在区间内二分搜索，平衡精度与速度。
- **神经回归（Neural Regression）**：训练一个小型预测网络直接估计所需 token 数，速度最快（仅 1 次评估）但误差约 5–10%。

此外，编码器对掩码的条件输入可在推断时移除，牺牲轻微重建质量（满足率下降约 4.3 个百分点）换取 2 倍推断加速，为用户提供灵活的质量-速度权衡。

### 输入输出流总结

- **训练阶段**：输入帧 $x$ → 采样 $\ell$ 并生成掩码 $m$ → 编码器（含掩码条件）输出 $z$ → 掩码得 $z_m$ → 解码器重建 $\hat{x}$ → 计算 MSE 损失。
- **推断阶段**：输入帧 $x$ → 根据目标阈值搜索最优 $\ell$ → 编码器输出 $z$ → 保留前 $\ell$ 个 token → 解码器重建 $\hat{x}$。多块模式下，此过程按块自回归执行并缓存中间状态。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/002_Figure_2.jpg]]
*Figure 2: ElasticTok adaptively encodes image and video to variable length outputs based on the complexity of the input data. Single block uses an Encoder-Decoder pipeline with a sampled latent mask. Multi-block extends this with a Block Causal Mask to handle longer video sequences*

## 核心模块与公式推导

### 训练阶段：随机掩码策略

ElasticTok 的核心训练机制是在标准自编码器（Encoder-Decoder）的基础上引入一种**随机尾部截断掩码**策略。对每个训练样本 $x$，首先从支持范围内均匀采样本次保留的 token 数量：

$$\ell \sim U(\{M_{min}, \dots, M_{max}\})$$

其中 $M_{min}$ 和 $M_{max}$ 分别为允许的最小和最大 token 数量。根据采样得到的 $\ell$，生成一个二进制掩码 $m \in \{0,1\}^N$，其前 $\ell$ 个元素为 1，其余为 0。编码器输出 $z$ 与掩码逐元素相乘，得到被截断的潜在表示：

$$z_m = z \odot m$$

解码器仅基于 $z_m$ 重建原始输入。这一设计的因果逻辑是：训练过程中编码器无法预知每次会被保留多少 token，因此被迫将最重要的信息压缩到序列前端，从而学会根据输入内容的复杂度自适应分配信息密度。

### 编码器条件机制

编码器不仅接收视觉输入，还额外接收掩码 $m$ 作为条件。具体实现中，掩码通过可学习的嵌入向量融入编码器，使编码器在生成潜在表示时就能感知到当前允许的 token 预算。消融实验（Table 5）表明，移除该条件机制可使推断速度提升 2 倍，但视频重建满足率在 0.003 MSE 阈值下下降约 4.3 个百分点（79.6% vs 75.3%），证实了条件机制在编码质量与推断速度之间的因果调节作用。

### 多块扩展：块因果掩码

对于长视频序列，ElasticTok 采用多块（multi-block）架构。每个块内部执行上述单块编码-解码流程，块与块之间通过**块因果掩码**（Block Causal Mask）连接，使得当前块的编码可以条件于前序块的信息。推断时，对每个块迭代执行自适应 token 搜索，并利用类似语言模型中的 KV-cache 机制进行加速。

### 推断阶段：自适应搜索

训练完成后，ElasticTok 支持多种自适应推断策略，核心是在给定目标重建阈值（如 MSE 阈值）下搜索最小满足条件的 token 数量：

- **Full Search**：遍历所有可能的 token 数量，误差率为 0%，但需要最多 $N$ 次函数评估（NFE），适合离线高精度场景。
- **Binned Search**：将 token 空间分桶后进行二分搜索，在精度和速度之间折中。
- **Neural Regression**：训练一个轻量回归器直接预测所需 token 数，仅需 1 次 NFE，但误差率约 5–10%，适合实时应用。

此外，推断目标函数可替换为非像素级损失（如 CLIP cosine distance），从而引导 token 分配偏向特定语义内容（如文本区域），展示了框架的灵活性。

### 关键公式汇总

| 公式 | 含义 | 锚点 |
|------|------|------|
| $\ell \sim U(\{M_{min}, \dots, M_{max}\})$ | 均匀采样保留的 token 数量 | Section 3.1 |
| $z_m = z \odot m$ | 编码器输出与二进制掩码逐元素相乘，截断尾部 token | Section 3.1 |
| $\text{softmax}(Q_i^T [K_1, \ldots, K_S]) [V_1, \ldots, V_S]$ | 块环形注意力中每个序列并行秩的部分注意力计算 | Section 2.1 |

## 实验与分析

### 核心定量结果：自适应标记化的效率优势

ElasticTok 的核心主张——根据内容复杂度自适应分配 token 数量——通过重建满足率与 token 使用百分比的权衡曲线得到直接验证。Figure 4 展示了 ElasticTok-FSQ 在 ImageNet 图像和视频上的表现：纵轴表示达到给定重建 MSE 阈值的样本比例，横轴表示使用的 token 百分比。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/004_Figure_4.jpg]]
*Figure 4: Performance comparison between baseline and ElasticTok-FSQ on ImageNet and Video. The y-axis shows the percentage of samples that satisfy the reconstruction threshold, while the x-axis represents the percentage of tokens used. (Left) On image, ElasticTok achieves a 3.5x and 1.3x efficiency boost at different reconstruction thresholds. (Right) On video, ElasticTok shows a 5x and 2.4x improvement over the baseline, maintaining superior performance while using fewer tokens. Figure 10 in Appendix D shows reference examples of reconstruction quality for an image at different thresholds*

在图像重建中，当采用较宽松的重建阈值时，ElasticTok 仅需固定 token 基线约 1/3.5 的 token 即可达到相同的满足率；在更严格的阈值下，效率提升仍达 1.3 倍。视频场景的效率优势更为显著——宽松阈值下 token 用量降至基线的 1/5，严格阈值下为 1/2.4。这表明视频中帧间冗余为自适应编码提供了更大的压缩空间。

Table 1 进一步验证了自适应编码未损害表示质量：在 GQA、POPE、MSVD、MSRVTT 四个 VQA 基准上，ElasticTok-VAE 与使用 100% 固定 token 的基线准确率差异均在 1% 以内（如 GQA 上均为 54%，MSVD 上分别为 52% 和 53%）。这意味着下游任务性能得以保持，同时获得了变长编码带来的效率收益。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/008_Table_1.jpg]]
*Table 1: Comparison of our method with baseline on image and video benchmarks (ElasticTok-VAE). Our method can match the performance of the baseline trained on a fixed number (100%) of tokens. However, baseline models are restricted to a fixed token output, and require full pretraining a new model for every possible token length, whereas ElasticTok only requires a single model to generalize to all token lengths*

### 重建质量随 token 数量的单调性

Figure 5 展示了重建损失随 token 使用量增加而单调下降的趋势，且下降速度在低 token 区间尤为剧烈。定性示例显示，文本清晰度和图像锐度随 token 增加逐步改善，这为推断时的自适应搜索提供了可靠基础——模型确实将更多 token 用于提升重建质量，而非产生不可预测的输出。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/005_Figure_5.jpg]]
*Figure 5: Loss progressively declines as more tokens are used (ElasticTok-FSQ). The top row illustrates the impact on text clarity, while the bottom row shows the effect on image sharpness. The graphs on the right quantify the reconstruction loss relative to token usage percentage, showing a rapid decline as more tokens are consumed*

### 序列长度对性能的影响

Figure 6 揭示了重建性能随视频帧数（即序列长度）的变化规律：性能在约 100 帧时达到峰值，此后略有下降。这一发现对长视频应用有直接指导意义——并非帧数越多越好，存在一个信息增益与建模难度之间的最优区间。注意该图的 x 轴采用对数刻度。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/006_Figure_6.jpg]]
*Figure 6: Progressive performance increase with more frames (ElasticTok-FSQ). Performance improves with increasing sequence length, peaking around 100 frames before a slight decline. (Note the log scale for the x-axis)*

### 推断方法的精度-速度权衡

Table 2 系统比较了三种推断搜索策略。Full Search 通过遍历所有可能的 token 数量实现 0% 误差率，但需要 4096 次函数评估（NFEs）；Binned Search 将误差率控制在 5% 以内，同时大幅降低计算量；Neural Regression 仅需 1 次 NFE，但误差率升至 9%。这为用户提供了根据计算预算灵活选择推断策略的空间。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/009_Table_2.jpg]]
*Table 2: Comparison of inference methods showing their respective error rates, number of function evaluations (NFEs) (ElasticTok-FSQ. Note that while Full and Binned Search are more computationally expensive, they could also benefit more from parallel function evaluations if compute is available*

### 编码器掩码条件的因果作用

Table 5 的消融实验直接验证了编码器掩码条件的因果效应。在视频重建中，带条件的模型在 0.003 MSE 阈值下的满足率为 79.6%，比无条件模型（75.3%）高出 4.3 个百分点。然而，这一质量提升以推断速度为代价——无条件模型的推断速度是条件模型的两倍。这证实了掩码条件在质量与速度之间建立了一个可调节的因果杠杆：当应用场景对延迟敏感时，可移除该条件以换取速度；当质量优先时，保留条件以获得更好的重建效果。

### 频率分析与 token 分配机制

Figure 9 通过频率分析揭示了 token 分配的底层机制：token 使用量与视频帧的高频幅度之间存在强正相关（单块设置 Pearson r=0.77，多块设置 r=0.67）。这为 ElasticTok 的自适应行为提供了可解释性——模型倾向于为包含更多高频细节（纹理、边缘、文字等）的帧分配更多 token，而平滑区域则被高效压缩。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/011_Figure_9.jpg]]
*Figure 9: Comparison of token usage versus frequency magnitude in single-block and multiblock frequency analysis (ElasticTok-FSQ). Both scatter plots show a strong positive correlation between frequency magnitude and token usage in a single-block setting a multi-block setting. The red lines represent the linear regression fits for each case*

### 失败模式与已知局限

尽管整体效率优势显著，ElasticTok 在两种极端情况下表现欠佳：

1. **极低 token 数（低于 M_min）**：训练不稳定，需人为设置下限以保证收敛。这暗示模型在极度压缩时难以在全局低频特征和局部高频特征之间找到一致的表示。
2. **极长序列尾部**：在 1M token 级别的序列中，尾部帧的重建质量略低于固定 token 基线。论文推测可能源于不同编码长度所需特征（全局 vs 局部）的冲突，或训练不充分。

此外，当前模型未采用 GAN 损失，虽避免了长序列训练中的稳定性问题，但可能限制了生成质量的上限。所有实验仅覆盖图像和视频模态，向音频等时序数据的扩展尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/007_Figure_7.jpg]]
*Figure 7: The accuracy and compute tradeoff with varying percentages of tokens used (ElasticTok-VAE). This allows users to adjust the accuracy based on computational budget*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/015_Table_3.jpg]]
*Table 3: Performance of ElasticTok-VAE on videos. Values in the table show the percentage of reconstructed video blocks that satisfy a given reconstruction threshold. The baseline is a 50% fixed token baseline, and our method uses variable token lengths with an average of 50% token usage over the dataset*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/010_Table.jpg]]
*Table: due to slight decorrelation from being able to leverage past frames (conditional encoding) in videos*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/001_Figure_1.jpg]]
*Figure 1: ElasticTok adaptively represent video based on information available. (Top) Groundtruth video frames. (Middle) Reconstructed frames with varying token usage. (Bottom) The bottom section depicts how ElasticTok dynamically adjusts token allocation over time, with the percentage of tokens used correlating to different content complexities in the video*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_08368/figures/003_Figure_3.jpg]]
*Figure 3: ElasticTok adaptively encodes image and video to variable length outputs based on the complexity of the input data (using ElasticTok-VAE). The top rows shows examples of ElasticTok on images. Below shows a video example with: (Top) Ground-truth video frames. (Middle) Reconstructed frames with varying token usage. (Bottom) The bottom section depicts how ElasticTok dynamically adjusts token allocation over time, with the percentage of tokens used 0 60 192 293 349 420 480 511correlating to different content complexities in the video*

## 方法谱系与知识库定位

### 与固定长度 Tokenizer 的关系

ElasticTok 的核心突破在于将视觉 tokenizer 从“固定码长”范式推进到“内容自适应码长”范式。传统视觉自编码器（VAE/FSQ）对每帧输出固定数量 $N$ 的 token，编码器仅以视觉数据为输入，解码器始终消费完整的 $N$ 个 token。ElasticTok 通过两个关键改动颠覆了这一设定：

1. **Token 数量掩码**：训练时从均匀分布 $\ell \sim U(\{M_{\text{min}}, \dots, M_{\text{max}}\})$ 采样保留的 token 数，生成二进制掩码 $m$，将编码器输出截断为 $z_m = z \odot m$（Section 3.1）。这迫使模型将关键信息压缩到前 $\ell$ 个 token 中，形成“前缀即精华”的隐式排序。
2. **编码器条件化**：编码器额外接收掩码 $m$ 作为输入，通过可学习嵌入向量融入（Section 3.1, Table 5）。

这一设计使 ElasticTok 在架构层面与固定 token 基线（相同 ViT 编码器-解码器，仅掩码策略不同）形成对照。因果旋钮在于：随机截断尾部 token 的策略迫使编码器学会按信息密度降序排列潜在表示，从而在推断时可动态选择 token 数量。

**效率优势的证据强度**：Figure 4 显示，在 ImageNet 上 ElasticTok-FSQ 达到相同重建满足率时仅需固定基线的 1/3.5（宽松阈值）至 1/1.3（严格阈值）的 token；视频上优势更显著，达 1/5 至 1/2.4。Table 4 进一步表明，在相同最差情况 MSE 下，ElasticTok 的平均 token 用量远低于固定基线。这些结果置信度较高（0.95），但需注意效率增益的具体倍数依赖于重建阈值的选择。

### 与序列建模方法的衔接

ElasticTok 并非孤立存在，而是设计为长视频自回归生成模型的“前端编码器”。论文明确将其置于 Blockwise RingAttention 框架（Section 2.1）的下游：多块 ElasticTok 通过块因果掩码（Block Causal Mask）处理长视频序列，每个块的 token 搜索以块自回归方式进行，并利用类似语言模型的 KV 缓存加速（Section 3.2）。

这一设计使 ElasticTok 与现有长序列建模方法形成互补而非替代关系。其贡献在于降低进入自回归模型的 token 总量，而非改进注意力机制本身。Figure 7 展示了这种衔接的实际意义：用户可根据计算预算灵活调整 token 使用百分比，在下游 VQA 准确率与计算开销之间取得权衡。

### 适用边界

ElasticTok 的适用性受以下边界约束：

- **模态范围**：当前仅在图像和视频上验证。论文明确指出方法“一般性地与模态无关”，可扩展至其他时序数据（如音频、决策轨迹），但尚未提供实验证据。**此扩展方向需手动验证。**
- **训练稳定性**：极低 token 数（$M_{\text{min}}$ 以下）训练不稳定，需设置下限。论文推测这源于极短编码需要全局低频特征，而长编码需要局部高频特征，二者表示可能存在冲突（Section 6）。
- **序列长度**：Figure 6 显示重建性能随帧数增加而提升，约在 100 帧达到峰值后略有下降。极长序列（如 1M tokens）的尾部重建略低于固定 token 基线，可能因训练不充分或掩码冲突所致。
- **生成质量**：未采用 GAN 损失，可能限制生成质量。论文指出 GAN 损失在极长序列训练中更难稳定，这构成了效率与感知质量之间的权衡。

### 局限与开放问题

**已识别的局限**：
1. 尾部 token 重建质量略低于固定基线，根本原因尚不明确。
2. 编码器掩码条件化带来约 2 倍推断速度损失（Table 5），移除此条件可提速但重建满足率下降约 4.3 个百分点（79.6% vs 75.3%）。这构成了质量-速度的因果权衡。
3. 仅在像素级 MSE 损失下训练，未探索语义感知损失对编码效率的影响。

**开放问题**（需后续工作验证）：
- 掩码方案在 token 极少或极多时性能下降的深层原因是什么？是否确实源于全局与局部表示需求的冲突？
- 如何将 ElasticTok 迁移至音频、决策轨迹等时序模态，并保持类似的效率增益？
- 引入语义感知训练目标（如 CLIP 损失）能否鼓励更有意义的自适应编码？Figure 8 的初步定性结果显示 CLIP 损失可引导模型优先重建文本，但缺乏系统定量评估。

### 知识库定位

ElasticTok 在视觉 tokenizer 谱系中占据“自适应码长编码器”这一新兴位置。与固定 token 的 VAE/FSQ 基线相比，它以训练时的随机掩码策略换取推断时的灵活 token 分配，在保持下游任务性能（Table 1 显示 VQA 准确率持平或差异在 1% 以内）的同时大幅降低 token 消耗。该方法不依赖特定架构，论文声称可应用于“任何标准自编码器”，这为其在更大视觉生成系统中的集成提供了灵活性。

## 原文 PDF

![[paperPDFs/arxiv_2024/ElasticTok_Adaptive_Tokenization_for_Image_and_Video.pdf]]