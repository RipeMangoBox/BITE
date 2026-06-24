---
title: "EditVerse: Unifying Image and Video Editing and Generation with In-Context Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EditVerse_Unifying_Image_and_Video_Editing_and_Generation_with_In_Context_Learning.pdf
openreview_forum_id: blJXE07r7I
aliases:
- EditVerse
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "将图像、视频和文本统一表示为交错的 token 序列，并引入四维旋转位置编码（RoPE），在全自注意力框架下实现上下文学习，从而将图像编辑知识迁移到视频。"
primary_logic: "通过统一序列表示和全自注意力机制，模型能够从大规模图像编辑数据中学习通用编辑能力，并自然迁移到视频编辑任务，有效缓解视频编辑数据稀缺问题，同时支持灵活的输入/输出配置。"
claims:
- "统一交错的 token 序列设计使模型能够感知不同模态间的关系"
- "四维 RoPE 区分序列、时间、高度和宽度维度"
- "图像数据在视频编辑训练中起关键作用"
- "数据管道生成的 232K 视频编辑样本提升了性能"
---

# EditVerse: Unifying Image and Video Editing and Generation with In-Context Learning

> [!tip] 核心洞察
> 通过统一序列表示和全自注意力机制，模型能够从大规模图像编辑数据中学习通用编辑能力，并自然迁移到视频编辑任务，有效缓解视频编辑数据稀缺问题，同时支持灵活的输入/输出配置。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EditVerse：基于上下文学习的图像与视频编辑及生成统一框架 |
| 英文题名 | EditVerse: Unifying Image and Video Editing and Generation with In-Context Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=blJXE07r7I) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | EditVerse |
| Dataset | EditVerseBench, TGVE+ |

> [!tip] 效果简介
> - EditVerseBench 上，编辑质量 (VLM) 为 7.65，对比 6.97 (Señorita-2M)，变化 +0.68。
> - EditVerseBench 上，视频质量 (Pick Score) 为 20.07，对比 19.73 (TokenFlow)，变化 +0.34。
> - EditVerseBench 上，帧文本对齐 为 26.73，对比 26.34 (Señorita-2M)，变化 +0.39。

## 概述

视频编辑领域长期受困于两个相互强化的瓶颈。其一，现有视频生成模型多针对单一任务（如文本到视频）设计，架构上难以灵活支持多样化的编辑任务与多模态输入。其二，高质量、多样化的指令式视频编辑数据严重稀缺，远落后于图像编辑数据的规模与质量。这两个问题形成恶性循环：架构的专用性限制了数据利用的效率，而数据的匮乏又阻碍了通用编辑能力的涌现。

**EditVerse** 的核心洞察在于：如果将所有模态——文本、图像、视频——统一表示为交错的 token 序列，并在全自注意力框架下进行上下文学习，那么从大规模图像编辑数据中学到的编辑能力便可以自然迁移到视频编辑任务。这一思路直接切中了数据稀缺的瓶颈：图像编辑数据丰富且多样，若能有效复用，视频编辑便不再受制于标注数据的规模。

为实现这一目标，EditVerse 在三个关键设计上做出了改变。**输入表示**上，它摒弃了各模态单独处理或简单通道拼接的方式，转而将所有文本和视觉输入 token 化后拼接为统一的 1D 交错序列。**位置编码**上，它引入四维旋转位置编码（RoPE），同时编码序列、时间、高度和宽度四个维度的位置信息，使模型能够感知跨模态 token 之间的时空关系。**训练范式**上，它采用 Flow Matching 的速度预测目标替代传统的 DDPM 或交叉注意力微调，在统一序列上进行端到端优化。

实验结果表明，这一统一框架在视频编辑任务上取得了显著提升。在 EditVerseBench 上，EditVerse 的编辑质量（VLM 评估）达到 7.65，超越此前最优的开源方法 Señorita-2M 的 6.97；视频质量（Pick Score）达到 20.07，优于 TokenFlow 的 19.73。在 TGVE+ 基准上，EditVerse 与闭源商业模型 Movie Gen Edit 在 ViCLIP_dir 上持平（0.225），在 ViCLIP_out 上以 0.252 略超 EVE 的 0.251。消融实验进一步证实，图像生成数据和视频生成数据对视频编辑性能均至关重要，且交错序列格式与顺序 RoPE 的结合是性能提升的关键设计选择。

值得注意的是，EditVerse 并非在所有维度上都占据绝对优势。在图像生成（GenEval 综合评分 0.82，与 FLUX.1-dev 持平）和部分视频编辑子任务上，它与专用模型的表现相当而非超越，这反映了通用模型与专用模型之间的固有张力。此外，全自注意力机制处理长序列带来的计算开销，以及数据管道引入的噪声样本，仍是需要持续优化的方向。

## 背景与动机

视频编辑是视觉内容创作的核心需求之一。随着扩散模型在图像生成与编辑领域的成熟，研究者自然希望将这一能力扩展到视频。然而，视频编辑面临两个根本性瓶颈。

**架构限制：缺乏统一的编辑框架。** 现有视频生成模型通常为特定任务设计——例如文本到视频生成、首帧传播编辑或注意力注入编辑——每种方法都有其固定的输入/输出配置。**TokenFlow**（Qu et al., 2025）和 **STDF**（Yatim et al., 2024）依赖无训练的注意力操作，**Señorita-2M**（Zi et al., 2025）采用首帧传播策略，**InsV2V**（Cheng et al., 2023）则专注指令引导编辑。这些方法各自为政，难以灵活支持多样化的编辑任务（如物体添加、移除、风格迁移、背景替换等）和输入模态组合（图像+文本、视频+文本、多帧视频等）。用户被迫在不同工具间切换，缺乏一个能统一处理各类编辑需求的框架。

**数据稀缺：高质量视频编辑指令数据严重不足。** 与图像编辑领域拥有数百万级指令数据形成鲜明对比，视频编辑的高质量标注数据极为匮乏。视频编辑需要成对的源视频、编辑指令和目标视频，其采集和标注成本远高于图像。这一数据缺口直接制约了视频编辑模型的性能上限，使得现有方法难以充分学习复杂的时空编辑语义。

EditVerse 的动机正是从这两个瓶颈的交汇点出发：**能否通过架构设计，让模型从丰富的大规模图像编辑数据中学习通用编辑能力，并将其自然迁移到视频编辑任务？** 这一思路的核心洞察在于——编辑的本质是对视觉内容的语义理解和局部修改，这一能力在图像和视频之间具有高度可迁移性。关键在于设计一个统一表示框架，使模型能够同时“看到”文本指令、源图像/视频和目标图像/视频，并通过上下文学习建立它们之间的编辑映射关系。

具体而言，EditVerse 提出将文本、图像和视频统一表示为交错的 token 序列，在全自注意力机制下实现跨模态上下文学习。同时引入四维旋转位置编码（RoPE），区分序列、时间、高度和宽度维度，使模型能够精确感知时空位置关系。这一设计使得图像编辑知识得以有效迁移到视频编辑，从而缓解视频编辑数据稀缺的困境，同时天然支持灵活的输入/输出配置。

## 核心创新

EditVerse 的核心创新在于将图像、视频与文本统一为**交错的一维 token 序列**，并在全自注意力 Transformer 中引入**四维旋转位置编码（4D RoPE）**，从而实现对多模态输入的上下文学习（in-context learning）。这一设计解决了视频编辑领域的两大瓶颈：现有架构难以灵活支持多样化的编辑任务和输入模态，而高质量指令式视频编辑数据又严重稀缺。

### 从孤立模态到统一交错序列

传统视频编辑方法通常将各模态分开处理或通过通道拼接融合，限制了跨模态知识的有效传递。EditVerse 将文本、图像和视频 token 化后，以交错方式拼接为单一长序列（Figure 3），使模型能够直接感知不同模态 token 之间的上下文关系。消融实验表明，**仅当交错格式与顺序位置嵌入结合时**，模型才能充分建立模态间的关联，从而将图像编辑知识迁移到视频编辑任务中（Table 5）。

### 四维位置编码：分离序列、时间与空间

标准 RoPE 无法区分视频中的时间维度和空间维度。EditVerse 设计了**四维 RoPE**，将位置信息分解为序列维度（区分不同输入片段）、时间维度（视频帧索引）、高度维度和宽度维度（Figure 2 右侧）。这一设计使模型在统一序列中仍能保持对时空结构的感知，是跨模态上下文学习的关键支撑。

### 训练范式：Flow Matching 速度预测

与主流扩散模型采用的 DDPM 噪声预测不同，EditVerse 使用 **Flow Matching** 目标，直接预测隐空间中从噪声 $X_0$ 到清洁数据 $X_1$ 的**速度向量** $V_t = X_1 - X_0$。损失函数为预测速度与真实速度的均方误差：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{X}_0, \mathbf{X}_1} \left| u_{\Theta}(\mathbf{X}_t, t) - (\mathbf{X}_1 - \mathbf{X}_0) \right|^2$$

其中 $\mathbf{X}_t = t \mathbf{X}_1 + (1-t) \mathbf{X}_0$ 为线性插值的噪声样本。这一范式简化了训练目标，并与统一序列表示自然兼容。

### 关键设计消融验证

Table 5 的消融直接量化了各设计组件的贡献：去除交错格式或顺序 RoPE 均导致编辑质量（VLM 评分）、视频质量（Pick Score）和帧文本对齐三项指标全面下降。**交错格式 + 顺序 RoPE 的组合**对文本对齐和编辑质量的提升最为显著，验证了统一序列表示与四维位置编码的协同效应。

## 整体框架

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/002_Figure_2.jpg]]
*Figure 2: Overview of EditVerse. We design a unified framework for image and video editing and generation, which processes text and vision inputs into a unified sequence. The right part of the figure shows our positional embedding design. This framework leverages full self-attention to facilitate robust in-context learning and effective knowledge transfer among modalities*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/001_Figure_1.jpg]]
*Figure 1: The strong video editing performance of EditVerse emerges from a unified framework trained on a diverse set of mixed image and video data. This teaser visualizes a selection of supported image and video editing tasks (Instructions in the Appendix). More results in our Project Page*

EditVerse 的核心设计理念是将文本、图像和视频统一表示为交错的 1D token 序列，通过全自注意力 Transformer 实现跨模态的上下文学习（in-context learning）。这一统一框架使模型能够从大规模图像编辑数据中学习通用编辑能力，并自然迁移到视频编辑任务，有效缓解视频编辑数据稀缺的瓶颈。

### 统一输入表示

框架的输入处理流程如下（参见 Figure 2）：

1. **视觉编码**：图像和视频帧通过 VAE Encoder 压缩到隐空间，得到视觉 token。
2. **文本编码**：编辑指令通过 **Flan-T5-XXL** 文本编码器转换为文本 token。
3. **模态投影**：不同模态的 token 经过各自的 Modality Projector 投影到共享维度空间。
4. **交错序列构建**：所有 token 按交错方式拼接为统一的 1D 序列（见 Figure 3），使模型能够感知不同模态间的时序和语义关系。

> 关键设计洞察：仅当交错输入格式与顺序位置嵌入相结合时，模型才能最佳地感知不同模态之间的关系（Table 5 消融实验证实）。

### 四维旋转位置编码（4D RoPE）

为区分序列中的不同维度信息，EditVerse 引入了四维 RoPE，同时编码以下四个维度的位置信息：

- **序列维度**：token 在整体序列中的顺序位置
- **时间维度**：视频帧的时间索引
- **空间高度和宽度维度**：视觉 token 的二维空间坐标

这一设计与标准 RoPE 形成关键差异——标准 RoPE 无法区分时空维度，而四维 RoPE 为视频编辑中的时序一致性和空间定位提供了必要的归纳偏置。

### 全自注意力 Transformer

EditVerse 采用 **2B 参数的密集 Transformer** 架构（类似 LLaMA 3），使用全自注意力机制处理统一序列。全自注意力的优势在于：

- 允许任意位置的 token 直接交互，实现跨模态的上下文学习
- 图像编辑知识可通过注意力机制自然迁移到视频 token
- 支持灵活的输入/输出配置（任意分辨率、时长和序列位置）

### Flow Matching 训练范式

与传统的 DDPM 或交叉注意力微调不同，EditVerse 采用 Flow Matching 速度预测目标进行训练：

- **速度定义**：$V_t = \frac{dX_t^{(i)}}{dt} = X_1^{(i)} - X_0^{(i)}$，即清洁数据与噪声的差
- **噪声样本插值**：$X_t^{(i)} = t X_1^{(i)} + (1-t) X_0^{(i)}$，在隐空间进行线性插值
- **训练损失**：$\mathcal{L} = \mathbb{E}_{t, \mathbf{X}_0, \mathbf{X}_1} \left| u_{\Theta}(\mathbf{X}_t, t) - (\mathbf{X}_1 - \mathbf{X}_0) \right|^2$，即预测速度与真实速度的均方误差

推理时，从标准正态分布采样 $X_0 \sim \mathcal{N}(0,1)$，使用 ODE 求解器以离散时间步生成最终输出。

### 模块关系总结

| 模块 | 功能 | 关键设计 |
|------|------|----------|
| VAE Encoder | 视觉输入压缩 | 将图像/视频帧映射到隐空间 |
| Flan-T5-XXL | 文本编码 | 将指令转换为 token |
| Modality Projectors | 维度对齐 | 统一不同模态的 token 维度 |
| Interleaved Sequence Builder | 序列构建 | 交错拼接文本和视觉 token |
| 4D RoPE | 位置编码 | 区分序列、时间、空间维度 |
| 2B Self-Attention Transformer | 特征融合 | 全自注意力实现上下文学习 |
| Flow Matching Head | 生成输出 | 速度预测与 ODE 求解 |

这一统一框架的核心因果机制在于：交错序列表示提供了跨模态信息交互的结构基础，四维 RoPE 赋予了时空位置感知能力，全自注意力则驱动了从图像到视频的知识迁移——三者协同使得在图像数据上学习的编辑能力能够泛化到视频任务。

## 核心模块与公式推导

EditVerse 的核心架构由七个模块串联构成，共同实现从多模态输入到编辑/生成输出的端到端流水线。以下按数据流向逐一说明。

**VAE Encoder** 负责将图像和视频的像素空间压缩至低维隐空间，降低后续 Transformer 的计算负担。**Flan-T5-XXL Text Encoder** 则将文本指令编码为 token 序列。两类 token 分别通过各自的 **Modality Projectors** 投影到共享的嵌入维度，消除模态间的表示鸿沟。

**Interleaved Sequence Builder** 将文本 token 与视觉 token 按交错方式拼接为统一的一维序列（见 Figure 3）。该设计是上下文学习能力的关键：只有交错格式才能让模型感知不同模态之间的关系，从而支持图像编辑知识向视频的自然迁移（Table 5 消融验证）。

**4D RoPE Embedding** 为序列中的每个 token 注入四维位置信息：序列维（区分不同输入/输出片段）、时间维（视频帧索引）、高度维和宽度维（空间坐标）。标准 RoPE 仅编码序列维，无法区分视频帧间的时空关系；四维 RoPE 使全自注意力能够同时建模跨模态、跨帧和跨空间的依赖。

**Self-Attention Transformer (2B)** 采用类似 LLaMA 3 的密集架构，对统一序列执行全自注意力，实现上下文学习与跨模态特征融合。与交叉注意力方案不同，全自注意力允许任意 token 直接交互，是图像-视频知识迁移的结构基础。

**Flow Matching Head** 将 Transformer 输出映射为速度场预测，用于去噪生成。

训练目标为 Flow Matching 损失，定义如下。设 $X_0^{(i)} \sim \mathcal{N}(0,1)$ 为噪声，$X_1^{(i)}$ 为清洁数据，噪声样本在隐空间线性插值：

$$X_t^{(i)} = t X_1^{(i)} + (1 - t) X_0^{(i)}$$

真实速度定义为清洁数据与噪声之差：

$$V_t = \frac{d X_t^{(i)}}{dt} = X_1^{(i)} - X_0^{(i)}$$

模型 $u_\Theta$ 预测速度场，损失为预测速度与真实速度的均方误差：

$$\mathcal{L} = \mathbb{E}_{t, \mathbf{X}_0, \mathbf{X}_1} \left| u_\Theta(\mathbf{X}_t, t) - (\mathbf{X}_1 - \mathbf{X}_0) \right|^2$$

推理时，从标准正态分布采样 $X_0$，使用 ODE 求解器以离散时间步从 $X_0$ 生成 $X_1$。

**关键设计消融证据**（Table 5）：仅使用交错格式而不使用顺序 RoPE，或仅使用顺序 RoPE 而不使用交错格式，编辑质量和文本对齐均显著下降。两者结合时，文本对齐和编辑质量达到最优，证实了统一序列表示与四维位置编码的协同效应。

## 实验与分析

### 核心实验设置

EditVerse 基于 2B 密集 Transformer 架构（类似 LLaMA 3），使用 AdamW 优化器（β₁=0.9, β₂=0.95，峰值学习率 8e⁻⁶，权重衰减 0.01），并采用 KnapFormer 的打包策略进行训练。评估涵盖自建基准 EditVerseBench（200 个编辑对，均匀分布在 20 个编辑类别，包含横竖屏方向）、TGVE+、V2VBench 等外部基准，以及图像生成（GenEval）、视频生成（VBench）和图像编辑（ImgEdit-Bench）的跨任务评估。

### 视频编辑主结果

在 EditVerseBench 上，EditVerse 在全部指标上超越已有开源研究模型。具体而言，编辑质量（VLM 评估）达到 7.65，比次优方法 Señorita-2M（6.97）提升 +0.68；视频质量（Pick Score）20.07，超越 TokenFlow（19.73）；帧文本对齐 26.73，优于 Señorita-2M（26.34）。与闭源商业模型 Runway Aleph 相比，EditVerse 在编辑忠实度（VLM 编辑质量评估）上胜出，但因基座模型差异在生成质量上稍逊——这一点在用户调研（Figure 5）中得到进一步验证，表明 VLM 评估与人类判断更为一致。

在 TGVE+ 基准上，EditVerse 的 ViCLIP_dir 达到 0.225（与 Movie Gen Edit 持平），ViCLIP_out 达到 0.252（略优于 EVE 的 0.251），展现出与最先进视频编辑模型相当的性能。在 V2VBench 上，EditVerse 的帧语义一致性达到 0.959，与 ControlVideo 持平。

### 跨任务泛化能力

统一框架在非视频编辑任务上也展现出竞争力。在图像生成基准 GenEval 上，EditVerse 综合评分 0.82，与 FLUX.1-dev 持平。在视频生成基准 VBench 上，EditVerse 以仅 2B 参数量取得总分 80.97，超越若干更大模型（如 ModelScope 1.7B、LaVie 3B、Show-1 6B），体现了小模型的参数效率优势。但在纯图像编辑任务 ImgEdit-Bench 上，EditVerse 仍落后于专用图像编辑模型（Table 6），这是统一模型在特定高质量数据丰富任务上的已知局限。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/022_Table_6.jpg]]
*Table 6: Quantitative comparison on ImgEdit-Bench (Ye et al., 2025a)*

### 数据消融：图像与视频生成数据的关键作用

Table 4 的数据消融实验揭示了训练数据构成对视频编辑性能的因果影响。完整数据配置（图像生成 + 视频生成 + 视频编辑）取得最佳编辑质量（VLM 评估 6.95）；若去除图像生成数据，编辑质量骤降至 6.12；若去除视频生成数据，同样出现显著下降。Figure 8 的可视化消融进一步印证：图像数据在视频编辑中扮演关键角色——模型从大规模图像编辑/生成数据中习得的通用编辑能力，通过上下文学习机制有效迁移至视频域，这正是缓解视频编辑数据稀缺瓶颈的核心机制。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/020_Figure_8.jpg]]
*Figure 8: Visualization of ablation on training data. Image data plays a critical role. Table 4: Ablation study on training data. We run 20K steps with the same setup as in Section 5.1. Results indicate that both image and video generation data are crucial to video editing performance*

### 设计消融：交织格式与顺序 RoPE 的协同效应

Table 5 的设计消融对比了三种配置：仅使用交织格式、仅使用顺序 RoPE、两者结合。结果表明，两者结合在编辑质量（6.95）、视频质量（Pick Score 19.99）、帧文本对齐（26.26）上全面优于单一设计。仅使用交织格式时编辑质量仅为 6.42，仅使用顺序 RoPE 时为 6.84。论文明确指出：“只有交织输入格式与顺序位置嵌入相结合，才能最好地使模型感知不同模态间的关系，从而实现图像到视频的知识迁移”。这一消融强有力地支撑了统一序列表示作为因果旋钮的核心地位。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/021_Table_5.jpg]]
*Table 5: Ablation study on interleaved formation and sequential RoPE. We run 20K steps with the same experimental setting detailed in Section 5.1 for the ablation to save compute*

### 失败模式分析

Figure 9 展示了 EditVerse 的典型失败案例，主要包括两类问题：（1）**空间定位错误**——模型未能将添加的物体（如宝箱）放置在正确位置（指令要求“在男人脚边”）；（2）**编辑区域模糊伪影**——编辑区域内产生模糊或不自然的纹理。这些失败模式与全自注意力处理长序列时的注意力分散、以及数据管道生成的编辑指令简短且含噪声（自动化方法成功率约 65%）有关。

### 效率分析

Figure 10 和 Table 11 分析了 GPU 显存占用和推理延迟随 token 长度的变化。全自注意力机制处理长序列导致较高的 FLOPs 和推理时间，这是统一框架的计算代价。论文指出可通过更高压缩率的 VAE（如 16× 空间压缩）、动态 token 选择、模型蒸馏和高效注意力机制（如线性注意力、Mamba）来缓解。

### 补充图表

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/006_Table_2.jpg]]

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/011_Table_3.jpg]]
*Table 3: Quantitative comparison on TGVE+. Results show superior performance of EditVerse*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/024_Table_8.jpg]]
*Table 8: Image Generation. We evaluate the image generation capability of EditVerse using the GenEval benchmark (Ghosh et al., 2023) shown in Table 8, which is designed to comprehensively assess textto-image models across multiple aspects of visual reasoning and compositional fidelity. Our method achieves state-of-the-art performance when compared against a wide range of both open-source and commercial systems, highlighting better semantically aligned generation*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/004_Table_1.jpg]]

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/023_Table_7.jpg]]
*Table 7: Comparison with text-to-video models on the VBench (Zhang et al., 2024). # Params. is the number of total parameters. EditVerse shows competitive performance with a small model size*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/025_Table_9.jpg]]
*Table 9: Quantitative comparison on V2VBench (Sun et al., 2024). Methods are grouped into three categories: (i) Network and Training Paradigm, (ii) Attention Feature Injection, and (iii) Diffusion Latent Manipulation. Local best are in bold. Global best are underlined*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_blJXE07r7I/figures/030_Table_10.jpg]]

## 方法谱系与知识库定位

### 1. 核心设计定位

EditVerse 并非现有视频编辑方法的渐进式改进，而是在**统一序列建模**范式下对多模态编辑与生成任务的根本性重构。其核心设计选择——将文本、图像和视频统一表示为交错的 1D token 序列，并通过全自注意力机制进行上下文学习——使其在方法谱系中处于一个独特位置：它既不同于传统的扩散模型编辑方法，也不同于针对特定任务设计的专用架构。

这一设计的因果机制在于：当不同模态被表示为统一的 token 序列时，模型能够从大规模图像编辑数据中学习通用的编辑能力（如对象移除、风格迁移），并通过全自注意力机制将这些能力自然迁移到视频编辑任务。消融实验（Table 4）明确证实，去除图像生成数据或视频生成数据均导致编辑质量显著下降，验证了跨模态知识迁移的有效性。

### 2. 与现有方法的关系

#### 2.1 相对于无训练注意力操作方法

**TokenFlow**（Qu et al., 2025）和 **STDF**（Yatim et al., 2024）属于无训练方法，通过操作预训练扩散模型中的注意力图来实现视频编辑。这类方法无需训练数据，但编辑能力受限于底层模型的能力边界，且难以处理复杂的多轮指令。EditVerse 采用端到端训练范式，通过大规模混合数据学习编辑行为，在 EditVerseBench 上编辑质量（VLM 评估）达到 7.65，显著优于 TokenFlow 和 STDF（Table 2）。

#### 2.2 相对于首帧传播方法

**Señorita-2M**（Zi et al., 2025）采用首帧编辑后传播的策略，本质上是将图像编辑能力扩展到视频的工程化方案。EditVerse 的编辑质量（7.65 vs 6.97）和帧文本对齐（26.73 vs 26.34）均优于 Señorita-2M（Table 2），说明统一序列建模比逐帧传播能更好地保持时序一致性。

#### 2.3 相对于指令引导视频编辑方法

**InsV2V**（Cheng et al., 2023）和 **Lucy Edit**（Team, 2025）是专门的指令引导视频编辑方法。EditVerse 在编辑质量上显著超越 InsV2V（7.65 vs 6.08，Table 2），但其优势更多来自训练数据规模和统一架构的泛化能力，而非指令理解机制的创新。

#### 2.4 相对于视频编辑适配器方法

**EVE**（Singer et al., 2024a）通过适配器将编辑能力注入预训练视频模型。在 TGVE+ 基准上，EditVerse 的 ViCLIP_out（0.252）略优于 EVE（0.251），ViCLIP_dir（0.225）与 **Movie Gen Edit**（Polyak et al., 2025）持平（Table 3），表明统一序列方法在编辑方向保持上具有竞争力。

#### 2.5 相对于商业模型

与闭源商业模型 **Runway Aleph**（Runway, 2025）相比，EditVerse 在编辑忠实度（VLM 评估的编辑质量）上表现更优，但在生成质量（Pick Score）上受限于基础模型差异而有所落后（Table 2）。用户调研（Figure 5）进一步验证了编辑忠实度优势更符合人类判断。

#### 2.6 相对于经典扩散编辑方法

**SDEdit**（Meng et al., 2021）和 **Tune-A-Video**（Wu et al., 2023a）代表了早期的扩散模型编辑范式。EditVerse 采用 Flow Matching 速度预测替代 DDPM 噪声预测（Section 3.3），训练目标为：

$$\mathcal { L } = \mathbb { E } _ { t , \mathbf { X } _ { 0 } , \mathbf { X } _ { 1 } } \left| u _ { \Theta } ( \mathbf { X } _ { t } , t ) - ( \mathbf { X } _ { 1 } - \mathbf { X } _ { 0 } ) \right| ^ { 2 }$$

这一选择使模型能够更灵活地处理不同模态的去噪过程。

### 3. 适用边界

EditVerse 的适用边界由以下因素共同界定：

1. **任务泛化范围**：模型支持图像/视频编辑与生成的统一处理，包括对象添加/移除/变换、风格迁移、背景替换、相机运动变换等 20 余种编辑类别（Figure 1, Figure 4）。在 GenEval 图像生成基准上综合评分 0.82，与 **FLUX.1-dev** 持平（Table 8）；在 V2VBench 视频编辑基准上帧语义一致性达 0.959，与 **ControlVideo** 持平（Table 9）。

2. **输入灵活性**：支持任意分辨率、时长和序列位置的图像与视频输入（Figure 3），但全自注意力机制导致计算开销随 token 长度增长（Figure 10）。

3. **数据依赖性**：性能高度依赖训练数据的多样性和质量。视频编辑数据管道生成的 232K 样本中自动化方法成功率约 65%，引入噪声样本可能影响特定场景的编辑精度。

### 4. 已知局限与失败模式

1. **空间定位错误**：模型可能在错误位置添加物体，例如在"将宝箱放在男人脚边"的指令中，宝箱被放置在错误位置（Figure 9a）。

2. **编辑区域模糊伪影**：编辑区域可能产生模糊伪影，影响局部视觉质量（Figure 9b）。

3. **计算开销**：全自注意力处理长序列导致高 FLOPs 和长训练/推理时间。论文提出可通过 16× 空间压缩 VAE、动态 token 选择、模型蒸馏和高效注意力机制（如线性注意力、Mamba）缓解。

4. **图像编辑未达 SOTA**：虽然统一模型泛化能力强，但在纯图像编辑任务上仍落后于专用模型，可通过数据混合策略和微调优化。

5. **通用-专用权衡**：对于高质量数据丰富的特定任务，专用模型可能仍优于统一模型。

### 5. 开放问题

1. **效率优化**：能否通过 16× 空间压缩 VAE 将 token 长度降为四分之一，从而大幅降低注意力开销？动态 token 选择机制能否在不损害跨模态学习的前提下有效剪枝冗余上下文 token？线性注意力和 Mamba 等高效注意力机制能否在保持性能的同时降低计算负担？

2. **质量提升**：如何通过针对性的数据混合或微调缩小图像编辑与 SOTA 专用编辑器之间的差距？如何进一步减少视频编辑中的错误位置和模糊区域等失败案例？

3. **生成加速**：模型和步长蒸馏能否明显加速生成速度？

4. **数据质量**：如何提升自动化数据管道的成功率（当前约 65%），减少噪声样本对训练的负面影响？

## 原文 PDF

![[paperPDFs/ICLR_2026/EditVerse_Unifying_Image_and_Video_Editing_and_Generation_with_In_Context_Learning.pdf]]
