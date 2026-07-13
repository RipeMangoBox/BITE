---
title: Generative Video Compression with One-Dimensional Latent Representation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generative_Video_Compression_with_One_Dimensional_Latent_Representation.pdf
project_link: "https://gvc1d.github.io/"
code_link: "https://vcgit.hhi.fraunhofer.de/ecm/ECM"
aliases:
- GVCODLR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将潜在表示从固定的2D网格替换为可学习的1D令牌，并结合1D记忆提供语义丰富的长程上下文。
primary_logic: 去除2D空间对应关系后，1D令牌能够自适应地关注语义区域，天然地减少令牌数量，形成紧凑的语义潜在空间，从而高效利用时空冗余。
claims:
- 在HEVC-B数据集上，GVC1D相比GLC-Video在LPIPS指标下节省60.4%码率，在DISTS指标下节省68.8%码率。
- 移除长程上下文（1D记忆）导致UVG数据集上BD-Rate恶化超过40%。
- 将1D记忆替换为2D特征管理的记忆导致UVG数据集上BD-Rate恶化超过16%。
- HEVC-B 上 LPIPS BD-Rate (%) = GVC1D
---

# Generative Video Compression with One-Dimensional Latent Representation

> [!tip] 核心洞察
> 去除2D空间对应关系后，1D令牌能够自适应地关注语义区域，天然地减少令牌数量，形成紧凑的语义潜在空间，从而高效利用时空冗余。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于一维潜在表示的生成式视频压缩 |
| 英文题名 | Generative Video Compression with One-Dimensional Latent Representation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.15302) · [Project](https://gvc1d.github.io/) · [Code](https://vcgit.hhi.fraunhofer.de/ecm/ECM) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GVC1D |
| Dataset | HEVC-B |

> [!tip] 效果简介
> - HEVC-B 上，LPIPS BD-Rate (%) GVC1D vs GLC-Video (-60.4%)；DISTS BD-Rate (%) GVC1D vs GLC-Video (-68.8%)；PSNR BD-Rate (%) GVC1D vs GLC-Video (-53.8%)。

## 概要

传统神经视频编解码器将视频帧压缩为密集的2D潜在网格，这种刚性空间结构保留了大量的帧内冗余，且不利于建模长程时间相关性和语义连贯性，导致需要更高的码率。本文提出 **GVC1D**，核心思路是将潜在表示从固定的2D网格替换为可学习的1D令牌：去除2D空间对应关系后，1D令牌能够自适应地关注语义区域，天然地减少令牌数量，形成紧凑的语义潜在空间，从而高效利用时空冗余。在此基础上，进一步引入基于1D潜在令牌的Transformer记忆模块，循环更新固定大小的记忆状态，为编解码提供语义丰富的长程上下文。

在HEVC-B数据集上，GVC1D相比此前最好的生成式视频编解码器 **GLC-Video**，在LPIPS指标下节省 **60.4%** 码率，在DISTS指标下节省 **68.8%** 码率。消融实验表明，移除长程1D记忆会导致BD-Rate恶化超过40%，将1D记忆替换为2D特征管理的记忆则使BD-Rate恶化超过16%，证实了1D令牌的语义紧凑性对压缩效率的决定性作用。方法目前适用于低码率有损压缩场景，有限的令牌容量使其难以保留极精细的高频细节，暂不支持无损扩展。



视频压缩是数字媒体传输和存储的核心技术。传统视频编解码标准（如 VVC、HEVC）依赖手工设计的预测、变换和熵编码模块，在 PSNR 指标上表现优异，但在极低码率下往往产生模糊或块效应等视觉伪影。近年来，神经视频编解码器（neural video codecs）通过端到端学习取得了显著进展，其中生成式视频编解码器（generative video codecs）进一步引入了感知损失和对抗训练，在低码率下能够重建出更自然、语义更完整的画面。

然而，现有生成式视频编解码器（如 **GLC-Video**）普遍采用一个共同的设计范式：将视频帧编码为**密集的 2D 潜在网格**（dense 2D latent grids）。这种 2D 潜在表示继承了图像的空间结构，虽便于与卷积或 Transformer 架构对接，却带来了两个根本性问题：

1. **刚性空间结构导致冗余**：2D 潜在网格保留了固定的空间对应关系（fixed spatial correspondences），即使平坦背景区域也需分配大量令牌，造成帧内编码冗余，限制了码率的进一步压缩。
2. **长程时间相关性建模受限**：2D 网格的刚性结构不利于建模跨越较长帧间隔的语义级时间相关性。现有方法通常仅依赖前一帧的解码特征作为短时上下文（short-term context），缺乏对长程语义上下文的显式利用，导致时间冗余未被充分挖掘。

这两个瓶颈在极低码率场景下尤为突出。当码率预算极度受限时，2D 潜在网格要么因令牌数量不足而丢失关键语义信息，要么因空间结构僵化而将有限的码率浪费在非语义区域。因此，**如何突破 2D 潜在网格的结构性限制，构建更紧凑、语义感知更强的潜在表示，并引入有效的长程上下文建模机制，是生成式视频压缩向更低码率推进的关键挑战**。

本文 GVC1D 正是针对上述问题提出了全新的解决方案：用**一维潜在令牌（1D latent tokens）**替代传统的 2D 潜在网格，并配套设计了一个基于 1D 令牌循环更新的**长程记忆模块（1D memory）**，为编解码提供语义丰富的长程上下文。这一设计从根本上解除了空间结构的束缚，使模型能够自适应地关注语义区域，在显著减少令牌数量的同时保持甚至提升感知重建质量。



## 核心方法与创新机理

GVC1D 的核心创新在于将视频压缩的潜在表示从传统的 **2D 潜在网格** 替换为 **1D 潜在令牌**，并配套设计了 **1D 记忆** 来提供语义丰富的长程上下文。这两个 changed slots 相互协同，共同构成了方法的技术突破。

### 从 2D 网格到 1D 令牌：去除空间刚性

传统生成式视频编解码器（如 GLC-Video）将视频帧编码为密集的 2D 潜在网格，这种结构保留了固定的空间对应关系，导致大量帧内冗余被重复编码，且不利于建模长程时间相关性。GVC1D 通过移除这种刚性的 2D 空间结构，将视频压缩为极少数量的灵活 1D 令牌。

编码器由局部和全局 Vision Transformer 构成，将图像嵌入与可学习的 1D 令牌及上下文拼接后，通过 $M_e$ 个编码块（每块含 $N_e$ 层局部 Transformer 和一层全局 Transformer）生成紧凑的 1D 潜在表示 $y_t$：

$$y_t = \mathrm{Enc}(E_t \oplus L \oplus C)$$

其中 $E_t$ 为图像嵌入，$L$ 为可学习的潜在令牌，$C$ 为长程与短程上下文的拼接。解码器采用对称架构，利用可学习的掩码令牌从量化后的 1D 令牌和上下文重建帧：

$$\hat{x}_t = \mathrm{Out}(\mathrm{Dec}(\hat{y}_t \oplus M \oplus C))$$

去除 2D 空间对应关系后，1D 令牌能够自适应地关注语义区域，天然地减少令牌数量（每帧仅 32 个），形成紧凑的语义潜在空间。Figure 4 和 Figure 5 的可视化表明，1D 令牌在物体运动时会持续追踪同一语义区域（如马的左前腿），而在新物体出现时能动态重新分配注意力权重。

### 1D 记忆：语义级长程上下文

GVC1D 的上下文模型由长程 1D 记忆和短程上下文缓冲两部分组成。其中 **1D 记忆** 是关键的创新组件：它维护一个固定大小的记忆状态，通过少量 1D 令牌循环更新和读出，利用 Transformer 层高效提取语义级长程上下文。

消融实验（Table 3）提供了决定性证据：
- **移除 1D 记忆**（即去掉长程上下文）导致 UVG 数据集上 BD-Rate 恶化超过 40%，证明长程语义上下文对压缩效率至关重要；
- **将 1D 记忆替换为 2D 特征管理的记忆**使 UVG 数据集上 BD-Rate 恶化超过 16%，证实 1D 令牌的语义紧凑性对记忆有效性起决定作用。

### 自回归熵模型：令牌间相关性利用

在熵编码阶段，GVC1D 采用自回归 Transformer 对量化后的 1D 潜在令牌逐令牌预测概率分布，用于算术编码。这与传统 2D 空间上的超先验或条件编码形成对比。消融实验表明，移除此自回归建模会导致 BD-Rate 上升，说明自回归结构对利用令牌间相关性降低码率是必要的。

### 与 baseline 的系统性差异

| 设计维度 | GLC-Video / 传统方法 | GVC1D |
|---------|---------------------|-------|
| 潜在表示结构 | 2D 潜在网格 | 1D 潜在令牌（32 个/帧） |
| 长时上下文 | 仅前一帧短时上下文 | 1D 记忆循环更新的语义长程上下文 |
| 熵模型 | 2D 空间超先验/条件编码 | 1D 自回归 Transformer |

这三个 changed slots 的协同效果在 HEVC-B 数据集上得到验证：相比 GLC-Video，GVC1D 在 LPIPS 指标下节省 60.4% 码率，在 DISTS 指标下节省 68.8% 码率，在 PSNR 和 MS-SSIM 下分别节省 53.8% 和 45.1% 码率。



GVC1D 的整体框架围绕“一维潜在表示”这一核心设计展开，将传统视频编解码中固定的 2D 潜在网格替换为紧凑的 1D 潜在令牌序列，并辅以长短期上下文模型进行条件编解码。整个 pipeline 由编码器、解码器、熵模型和上下文模型四大模块构成，其数据流关系如 Figure 2 所示。

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview. Q, AE and AD represent quantization, arithmetic encoder and decoder, respectively. The input image*

### 编码器：从 2D 图像到 1D 令牌

编码器的输入包含三部分：当前帧的图像块嵌入 $E_t$、一组可学习的 1D 潜在令牌 $L$，以及由上下文模型提供的时空上下文 $C$。三者拼接后送入编码器，输出紧凑的 1D 潜在表示 $y_t$：

$$y_t = \mathrm{Enc}(E_t \oplus L \oplus C)$$

其中上下文 $C$ 由长时上下文 $C_l$ 和短时上下文 $C_s$ 拼接而成（$C = C_l \oplus C_s$），为编码过程提供时序先验。

编码器本身采用局部-全局 Transformer 的层级架构：共 $M_e$ 个编码块，每个块包含 $N_e$ 层局部 Transformer 和一层全局 Transformer：

$$\mathrm{Enc} = \bigcup_{i=1}^{M_e} \left\{ \bigcup_{j=1}^{N_e} \mathrm{LocalTrans}_{i,j},\ \mathrm{GlobalTrans}_i \right\}$$

局部 Transformer 将令牌划分为 $N$ 个窗口并行处理，降低了计算复杂度；全局 Transformer 则负责跨窗口的信息交互，确保 1D 令牌能够自适应地聚合来自全图不同语义区域的信息（Figure 1d 展示了这种语义级注意力机制）。

### 量化与熵编码

编码器输出的 $y_t$ 经过量化后得到 $\hat{y}_t$。为进行算术编码，GVC1D 采用基于自回归 Transformer 的熵模型，对量化后的 1D 潜在令牌逐令牌预测概率分布。自回归建模能够有效利用令牌间的相关性，消融实验表明，移除此自回归机制会导致 BD-Rate 显著上升。

### 解码器：从 1D 令牌重建图像

解码器架构与编码器对称。其输入为量化后的 1D 令牌 $\hat{y}_t$、可学习的掩码令牌 $M$ 以及上下文 $C$，输出重建图像 $\hat{x}_t$：

$$\hat{x}_t = \mathrm{Out}\big(\mathrm{Dec}(\hat{y}_t \oplus M \oplus C)\big)$$

掩码令牌 $M$ 在解码端起到类似“查询”的作用，引导解码器从有限的 1D 令牌中恢复出完整的图像内容。

### 上下文模型：长短期时序建模

上下文模型是整个框架的时序信息枢纽，由两个组件构成：

- **短时上下文缓冲（short-term context buffer）**：存储前一帧解码后的特征，提供即时的时间关联。
- **长时 1D 记忆（long-term 1D memory）**：维持一个固定大小的记忆状态，通过少量 1D 令牌进行循环更新和读出（Figure 3 展示了其两阶段架构）。该记忆利用 Transformer 层高效提取语义级的长程上下文，为编解码全体提供跨越多个帧的丰富时序信息。

消融实验证实了这两个组件的关键作用：移除 1D 记忆（即去掉长程上下文）会导致 UVG 数据集上 BD-Rate 恶化超过 40%；而将 1D 记忆替换为基于 2D 特征管理的记忆，BD-Rate 也会恶化超过 16%，表明 1D 令牌的语义紧凑性对记忆的有效性至关重要。

### 训练策略

GVC1D 采用两阶段训练。第一阶段使用感知重建损失 $L_{\mathrm{stage1}}$ 进行预训练；第二阶段引入率失真联合优化，在 $T$ 帧上平均：

$$L_{\mathrm{stage2}} = \frac{1}{T} \sum_{t=1}^{T} \big(R + \lambda L_{\mathrm{stage1}}\big)$$

其中 $R$ 为码率，$\lambda$ 为平衡系数，通过调节 $\lambda$ 可在不同码率点获得编解码模型。

### 整体数据流总结

对于每一帧 $x_t$：图像嵌入 $E_t$ 与可学习令牌 $L$、上下文 $C$ 一同进入编码器，生成 1D 潜在表示 $y_t$；量化后经自回归熵模型进行算术编码得到码流；解码端从码流恢复 $\hat{y}_t$，结合掩码令牌 $M$ 和上下文 $C$ 重建 $\hat{x}_t$；上下文模型则利用解码结果更新短时缓冲和长时记忆，为下一帧提供时序上下文。这一闭环设计使得 1D 令牌能够在极低码率下保持语义连贯性和时序一致性。



GVC1D 的编码器由 $M_e$ 个编码块堆叠而成，每个块包含 $N_e$ 层局部 Transformer 和一层全局 Transformer：

$$
\mathrm{Enc} = \bigcup_{i=1}^{M_e} \left\{ \bigcup_{j=1}^{N_e} \mathrm{LocalTrans}_{i,j},\; \mathrm{GlobalTrans}_i \right\}
$$

局部 Transformer 将拼接后的令牌划分为 $N$ 个窗口并行处理，全局 Transformer 则在所有令牌间建立全连接注意力。编码器接收三部分拼接输入——图像块嵌入 $E_t$、可学习潜在令牌 $L$、以及上下文 $C$（由长程上下文 $C_l$ 与短程上下文 $C_s$ 拼接而成），输出紧凑的 1D 潜在表示：

$$
y_t = \mathrm{Enc}(E_t \oplus L \oplus C), \quad C = C_l \oplus C_s
$$

解码器采用与编码器对称的架构，通过可学习的掩码令牌 $M$ 和上下文 $C$ 从量化后的 1D 令牌 $\hat{y}_t$ 重建视频帧：

$$
\hat{x}_t = \mathrm{Out}(\mathrm{Dec}(\hat{y}_t \oplus M \oplus C))
$$

上下文模型由两个组件构成：**长程 1D 记忆**和**短程上下文缓冲**。1D 记忆维护固定大小的记忆状态，通过少量 1D 令牌循环执行更新和读出两个阶段，利用 Transformer 层高效提取语义级长程上下文。短程上下文缓冲则提供相邻帧间的即时时序信息。

熵模型采用自回归 Transformer，对量化后的 1D 潜在令牌逐令牌预测概率分布，供算术编码器使用。

训练分为两阶段。第二阶段采用率失真损失，在 $T$ 帧上平均：

$$
\mathcal{L}_{\mathrm{stage2}} = \frac{1}{T} \sum_{t=1}^{T} (R + \lambda \mathcal{L}_{\mathrm{stage1}})
$$

其中 $R$ 为码率，$\mathcal{L}_{\mathrm{stage1}}$ 为第一阶段训练得到的感知重建损失，$\lambda$ 为平衡系数。

### 补充图表

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/001_Figure_1.jpg]]
*Figure 1: Method comparison. (a) Previous generative video codecs [28, 34, 50] encode videos into dense 2D latent grids with rigid spatial structures using short-term context*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/003_Figure_3.jpg]]
*Figure 3: 1D memory*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of 1D latent token outflows across two frames during object motion. In the two figures, the lines connect points corresponding to the maximum attention weights of each token, with the numbers indicating token indices*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/005_Figure_5.jpg]]
*Figure 5: Visualization of the outflow variation of a 1D latent token (index 4) as a new object appears. The red boxes in the first row mark image patches with the highest attention weights, while the green lines in the second row link them to the top four 1D latent tokens with the strongest attention. The bottom row is the 1D latent tokens attention weights corresponding to the maximum weight image patch (red boxes). As new content emerges, attention weights gradually shift from previously active tokens to newly activated ones*



## 实验与关键发现

### 主实验结果

GVC1D 在 HEVC-B、UVG 和 MCL-JCV 三个标准数据集上与传统编解码器（VTM-17.0、HM-16.25、ECM-5.0）及神经编解码器（DCVC-RT、DCVC-FM、GLC-Video）进行了系统对比。所有方法均在 RGB 色彩空间、低延迟设置（intra_period=-1）下评估 96 帧视频，传统编解码器使用官方配置文件并将 10-bit YUV444 输出转换为 RGB。

**Table 1** 汇总了在 HEVC-B、UVG 和 MCL-JCV 上的 BD-Rate 对比。GVC1D 在感知质量指标上展现出压倒性优势：与先前最好的生成式编解码器 GLC-Video 相比，在 HEVC-B 数据集上 LPIPS BD-Rate 节省 **60.4%**，DISTS BD-Rate 节省 **68.8%**。即使在 PSNR 和 MS-SSIM 等保真度指标上，GVC1D 仍分别节省 **53.8%** 和 **45.1%** 的码率。这一结果验证了核心洞察：去除 2D 空间对应关系后，1D 令牌能够自适应地关注语义区域，天然地减少令牌数量，形成紧凑的语义潜在空间，从而高效利用时空冗余。

值得注意的是，GVC1D 主要面向感知压缩。在 PSNR/MS-SSIM 比较中，GVC1D 虽不如面向 PSNR 优化的 DCVC 系列，但其感知指标和视觉质量大幅领先，且低码率下 PSNR 优值与感知质量无必然对应。**Figure 6** 的率失真曲线直观展示了 GVC1D 在 LPIPS 和 DISTS 指标上的显著优势，尤其在极低码率区间，GVC1D 的曲线明显低于所有对比方法。

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/006_Figure_6.jpg]]
*Figure 6: Rate-distortion curves on the HEVC-B, the UVG and the MCL-JCV datasets. 96 frames are tested in RGB colorspace with intra-period=–1*

**Figure 7** 和 **Figure 12** 提供了定性视觉对比。GVC1D 重建的视频帧在纹理细节和语义保真度上明显优于 GLC-Video 和 VTM，尤其在复杂场景和低码率下，传统方法出现明显的块效应和模糊，而 GVC1D 保持了更自然的视觉质量。

### 消融实验

**Table 3** 报告了关键模块的消融结果，揭示了 1D 记忆和自回归熵模型的因果作用。

**1D 记忆的长程上下文效应。** 移除 1D 记忆（即去掉长程上下文，仅保留短时上下文缓冲）导致 UVG 数据集上 BD-Rate 恶化超过 **40%**。这直接验证了 1D 记忆提供的语义丰富长程上下文对压缩效率至关重要，是因果旋钮的核心组成部分。

**1D 记忆 vs. 2D 记忆。** 将 1D 记忆替换为用 2D 特征管理的记忆，UVG 数据集上 BD-Rate 恶化超过 **16%**。这一对比排除了“记忆模块本身”的混淆效应，证实了 1D 令牌的语义紧凑性——而非记忆的存在与否——才是决定长程上下文有效性的关键。2D 特征保留了空间冗余，无法像 1D 令牌那样形成紧凑的语义表示。

**自回归熵模型。** 移除自回归 Transformer 熵模型（改用非自回归建模）导致 BD-Rate 上升，表明自回归建模对利用令牌间相关性降低码率是必要的。1D 潜在令牌序列天然适合自回归建模，这是 1D 表示相对于 2D 网格的另一结构优势。

**Table 2** 展示了令牌尺寸的消融。以 32×16（32 个令牌，每个 16 维）为锚点，实验表明该配置在码率-质量权衡上达到最优。令牌数量过少会限制表达能力，过多则削弱紧凑性优势。

### 注意力可视化与语义分析

**Figure 4** 和 **Figure 5** 提供了 1D 潜在令牌的注意力流出可视化，揭示了 1D 令牌如何自适应地关注语义区域。在物体运动场景中（Figure 4），特定令牌（如令牌 19）持续关注马的左前腿，即使该区域在两帧之间发生位移，令牌的语义关注点也随之移动，而非固定在 2D 空间位置。在新物体出现场景中（Figure 5），令牌 4 的注意力权重逐步转移到新出现的物体上，展示了 1D 令牌动态重分配注意力的能力。这些可视化直接支撑了核心洞察：去除 2D 空间对应关系后，1D 令牌能够自适应地关注语义区域。

### 复杂度分析

**Table 4** 报告了 GVC1D 在 NVIDIA A100 GPU 上使用 fp16 精度、1080P 分辨率下的复杂度。尽管引入了自回归 Transformer 和记忆模块，GVC1D 的编解码延迟仍保持在可接受范围内，具体数值需参见原表。

### 局限性与失败模式

尽管 GVC1D 在低码率感知压缩上取得了显著优势，但存在明确的局限性：

1. **高频细节丢失。** 由于每帧仅用 32 个 1D 令牌表示，模型存在固有限制，难以保留极精细的高频细节。这在高分辨率纹理区域（如草地、毛发）尤为明显，重建结果可能出现过度平滑。

2. **无损压缩不适用。** 有限的令牌容量使得模型目前无法直接扩展到无损压缩。1D 潜在表示的紧凑性天然与无损保真度相矛盾，需要探索可变令牌数量或可伸缩编码框架。

3. **内容复杂度适应性。** 当前所有帧使用固定数量的 1D 令牌，无法根据内容复杂度动态调整。对于场景剧烈变化或包含大量细节的视频片段，固定令牌数可能导致信息瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/007_Table_1.jpg]]
*Table 1: BD-Rate (%) comparison in the RGB colorspace on the HEVC-B, UVG, and MCL-JCV datasets (lower is better). 96 frames are evaluated with an intra-period of –1*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/009_Table_3.jpg]]
*Table 3: BD-Rate comparison of different model variants. AR denotes the autoregressive entropy model, and Memory denotes the memory component, where 1D and 2D indicate the use of 1D or 2D features to manage the memory. We use setting (4) as the anchor, which is finally adopted by our method*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/008_Table_2.jpg]]
*Table 2: BD-Rate comparison for different token sizes. The token size of 32 × 16 is used as the anchor*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/011_Table_4.jpg]]
*Table 4: Complexity analysis using fp16 precision at 1080P resolution. The tests are conducted on an NVIDIA A100 GPU*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/012_Figure_8.jpg]]
*Figure 8: Rate-distortion curves in terms of PSNR and MS-SSIM*

![[assets/figures/papers/paper_list_l880_https_arxiv_org_abs_2603_15302/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative examples on the MCL-JCV datasets*



## 定位与知识库关联

### 1. 方法沿革：从2D潜在网格到1D潜在令牌

GVC1D的核心贡献在于对神经视频压缩中**潜在表示结构**的根本性重新设计。传统神经视频编解码器——无论是面向PSNR的DCVC系列（**DCVC-RT**、**DCVC-FM**），还是面向感知质量的生成式方法（**GLC-Video**）——均沿用了将视频帧编码为**2D潜在网格**（2D latent grid）的范式。这种2D网格保留了刚性的空间对应关系，每个空间位置的潜在向量固定对应输入图像的特定区域。该设计的优势在于天然保留了空间局部性，但代价是：(1) 大量令牌被浪费在冗余的背景或静态区域；(2) 令牌间的长程时间相关性难以被有效建模。

GVC1D的突破在于**彻底移除2D空间结构**，将视频帧压缩为少量（如32个）可学习的**1D潜在令牌**。这一转变的因果机制在于：当令牌不再被绑定到固定空间位置时，模型可以通过交叉注意力机制自适应地关注语义显著区域，天然地实现令牌数量的压缩。Figure 1(c-d)直观展示了这一差异——2D潜在网格保留固定的空间对应关系，而1D令牌则自适应地聚合来自语义区域的视觉信息。

在上下文建模方面，GLC-Video仅使用前一帧的解码特征作为短时上下文，缺乏对长程时间依赖的显式建模。GVC1D在此基础上引入了**1D记忆模块**，通过循环更新固定大小的记忆状态，为编解码全过程提供语义丰富的长程上下文。该记忆模块同样基于1D令牌设计，利用Transformer层高效地管理长期信息，避免了2D特征管理记忆带来的空间冗余（消融实验证实，将1D记忆替换为2D特征管理的记忆会导致BD-Rate恶化超过16%）。

### 2. 与基线方法的适用边界对比

| 维度 | 传统编解码器 (VTM/ECM/HM) | 神经PSNR编解码器 (DCVC系列) | 神经感知编解码器 (GLC-Video) | **GVC1D (本文)** |
|------|--------------------------|----------------------------|------------------------------|------------------|
| 潜在空间结构 | 变换系数块 | 2D潜在网格 | 2D潜在网格 | **1D潜在令牌** |
| 优化目标 | PSNR | PSNR | 感知质量 (LPIPS/DISTS) | 感知质量 (LPIPS/DISTS) |
| 长程上下文 | 参考帧缓存 | 特征域条件编码 | 仅短时上下文 | **1D记忆 + 短时上下文** |
| 令牌数量 | 与分辨率相关 | 与分辨率相关 | 与分辨率相关 | **固定少量 (如32个)** |
| 适用码率范围 | 全码率 | 中低码率 | 低码率 | **极低码率** |

GVC1D的适用边界明确限定于**低码率有损压缩**场景。由于每帧仅用32个1D令牌表示，模型天然存在信息容量的上限，难以保留极精细的高频细节。作者明确指出，当前方法无法直接扩展到无损压缩，这构成了方法的基本边界。在PSNR/MS-SSIM等保真度指标上，GVC1D不如面向PSNR优化的DCVC系列（见Figure 8），但在感知指标（LPIPS、DISTS、FID、KID）和视觉质量上大幅领先，且低码率下的PSNR优势与感知质量并无必然对应关系。

### 3. 关键设计选择的因果证据

消融实验（Table 3）揭示了三个关键设计选择的因果效应：

- **1D记忆（长程上下文）的必要性**：移除1D记忆导致UVG数据集上BD-Rate恶化超过40%，证明语义级长程上下文对压缩效率的贡献远超短时上下文单独作用。
- **1D令牌对记忆管理的决定性**：将1D记忆替换为2D特征管理的记忆使BD-Rate恶化超过16%，证实1D令牌的语义紧凑性是记忆有效性的关键——2D特征中的空间冗余会稀释记忆模块的语义提取能力。
- **自回归熵模型的必要性**：移除自回归Transformer熵模型（改用非自回归）导致BD-Rate上升，表明令牌间的条件依赖关系对降低码率具有实质性贡献。

### 4. 局限性与开放问题

**已确认的局限**：
1. **令牌容量瓶颈**：固定数量的1D令牌（32个）限制了模型对高频细节的保留能力，使其仅适用于低码率有损压缩，无法扩展到无损场景。
2. **内容复杂性适应**：当前设计对所有帧使用相同数量的令牌，无法根据内容复杂性动态调整，可能导致简单场景浪费容量、复杂场景信息丢失。

**待探索的开放问题**：
1. **自适应令牌分配**：能否根据帧内容的复杂性动态调整1D令牌数量，实现更智能的码率分配？这需要在保持1D表示灵活性的同时引入内容自适应的令牌预算机制。
2. **高分辨率鲁棒性**：在4K/8K分辨率或场景剧烈变化时，1D令牌的语义聚合能力是否依然鲁棒？当前实验主要在1080P分辨率下进行，更高分辨率下的行为尚待验证。
3. **可伸缩编码扩展**：能否将1D潜在表示与无损压缩框架结合，构建感知一级的可伸缩编码方案？这需要在令牌表示中引入层次化的信息结构。
4. **解码延迟优化**：自回归熵模型在长序列解码时存在顺序依赖，其解码延迟是否可以通过并行解码策略或非自回归近似进一步优化？



## 原文 PDF

![[paperPDFs/CVPR_2026/Generative_Video_Compression_with_One_Dimensional_Latent_Representation.pdf]]
