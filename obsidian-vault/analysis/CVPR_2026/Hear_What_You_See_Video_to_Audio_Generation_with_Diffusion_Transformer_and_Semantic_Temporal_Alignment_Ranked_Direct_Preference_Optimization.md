---
title: "Hear What You See: Video-to-Audio Generation with Diffusion Transformer and Semantic-Temporal Alignment-Ranked Direct Preference Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hear_What_You_See_Video_to_Audio_Generation_with_Diffusion_Transformer_and_Semantic_Temporal_Alignment_Ranked_Direct_Preference_Optimization.pdf
project_link: "https://kaiw7.github.io/VisioSonic/"
code_link: null
aliases:
- VSD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: VisioSonic引入多模态条件器（高帧率Synchformer视觉嵌入+CLIP语义嵌入）和音频-视频-文本共注意力扩散变换器，显式对齐音频与视频潜变量；进一步通过STAR-DPO利用预训练模型自动构造偏好数据进行偏好优化，强化语义与时序对齐。
primary_logic: 将音频与视频潜变量沿时间维度对齐并结合高帧率视觉条件，是实现精准音视频同步的关键；通过将ImageBind和Synchformer作为奖励模型自动生成偏好对，可以在无需人工标注的情况下持续优化生成质量。
claims:
- VisioSonic-Base在VGGSound测试集上以最少的可训练参数量（151M）取得了最高的IB-score（32.8）和最低的DeSync（0.45），显著优于包括MMAudio在内的现有方法。
- 加入STAR-DPO后，VisioSonic在所有指标上进一步提升，IB-score达到33.1，DeSync降至0.41，在用户研究中获得最高评分。
- 消融实验表明，联合使用语义奖励（IB-score）和时序奖励（DeSync）的STAR-DPO效果最佳，且第二次迭代即可收敛。
- VGGSound test set 上 IB-score = 33.1 (VisioSonic w/ STAR-DPO)
---

# Hear What You See: Video-to-Audio Generation with Diffusion Transformer and Semantic-Temporal Alignment-Ranked Direct Preference Optimization

> [!tip] 核心洞察
> 将音频与视频潜变量沿时间维度对齐并结合高帧率视觉条件，是实现精准音视频同步的关键；通过将ImageBind和Synchformer作为奖励模型自动生成偏好对，可以在无需人工标注的情况下持续优化生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 所见即所听：基于扩散变换器和语义-时序对齐排序直接偏好优化的视频到音频生成 |
| 英文题名 | Hear What You See: Video-to-Audio Generation with Diffusion Transformer and Semantic-Temporal Alignment-Ranked Direct Preference Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wang_Hear_What_You_See_Video-to-Audio_Generation_with_Diffusion_Transformer_and_CVPR_2026_paper.html) · [Project](https://kaiw7.github.io/VisioSonic/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VisioSonic (with STAR-DPO) |
| Dataset | VGGSound test set, User Study |

> [!tip] 效果简介
> - VGGSound test set 上，IB-score 33.1 (VisioSonic w/ STAR-DPO) vs 32.27 (MMAudio-S) (+0.83)；DeSync 0.41 (VisioSonic w/ STAR-DPO) vs 0.444 (MMAudio-S) (-0.034 (lower better))；FDPaSST 55.48 (VisioSonic w/ STAR-DPO) vs 65.25 (MMAudio-S) (-9.77)。
> - User Study 上，Overall Rating (1-5) 4.60 (VisioSonic w/ STAR-DPO) vs Best among compared methods (Highest)。

## 概述

视频到音频（V2A）生成的核心瓶颈在于**语义一致性**与**时间同步性**难以兼得——模型既要理解画面中的物体与场景，又必须保证音频事件与视觉动态在毫秒级精确对齐。现有方法往往顾此失彼：基于低帧率视觉条件的模型丢失了关键的运动细节，而缺乏显式时序对齐机制的架构则难以捕捉声画之间的因果对应关系。

针对这一瓶颈，本文提出 **VisioSonic**，其核心调控变量是**多模态条件的高帧率时序对齐**与**基于偏好优化的精细化训练**。VisioSonic 包含两个关键设计：（1）多模态条件器同时提取低帧率 CLIP 语义嵌入和高帧率 Synchformer 视觉嵌入，通过 Token Aligner 将视频嵌入与音频潜变量沿时间维度对齐后，送入共注意力扩散变换器进行融合生成；（2）**STAR-DPO**（语义-时序对齐排序直接偏好优化）利用预训练的 ImageBind 和 Synchformer 作为奖励模型，自动生成偏好对并优化整流流匹配损失，在无需人工标注的情况下持续强化语义与时序对齐能力。

在 VGGSound 测试集上，VisioSonic-Base 以仅 151M 的可训练参数量取得了最高的 IB-score（32.8）和最低的 DeSync（0.45），显著优于包括 **MMAudio**（Cheng et al., CVPR 2025）在内的现有方法；加入 STAR-DPO 后进一步提升至 IB-score 33.1、DeSync 0.41，用户研究同样获得最高评分。消融实验证实，联合使用语义奖励与时序奖励的偏好优化效果最佳，且第二次 DPO 迭代即可收敛。

## 背景与动机

### 视频到音频生成的核心瓶颈

视频到音频生成（Video-to-Audio, V2A）旨在为静音视频自动合成语义匹配且时序同步的声音，是音视频理解与生成领域的关键任务。尽管近年来扩散模型和流匹配等生成范式大幅提升了音频质量，**现有方法在语义一致性与精细时间同步之间仍存在根本性张力**：模型要么能生成语义相关的音频类别，却无法精确对齐每一帧视觉动态的时间边界；要么能捕捉粗略的时间结构，却在复杂场景下丢失语义细节。这一瓶颈的根源在于视觉条件与音频潜变量之间缺乏显式的时序对齐机制，导致音频事件与视觉动态之间的时间对应关系常常无法保证。

### 现有方法的缺口

当前V2A方法可大致归为两类。一类以**MMAudio**（Cheng et al., CVPR 2025）为代表，采用多模态自注意力变换器联合处理视频与音频特征，但其依赖类别标签作为文本条件，且自注意力机制缺乏对音视频潜变量在时间维度上的显式对齐。另一类方法如**Diff-Foley**（Luo et al., NeurIPS 2023）和**Foley-Crafter**（Zhang et al., IJCV 2026）引入了时序控制器来增强同步性，但它们通常使用低帧率（如4–8 fps）的视觉特征，丢失了精细的帧间动态信息。此外，**Seeing-and-Hearing**（Xing et al., CVPR 2024）通过ImageBind实现跨模态对齐，**Frieren**（Wang et al., NeurIPS 2024）利用整流流匹配提升效率，但这些方法均未在训练过程中显式优化语义-时序的多维度偏好，导致生成结果在人类感知层面仍有明显不足。

### 本文的核心动机

针对上述缺口，本文提出两条核心动机：

1. **显式时序对齐与高帧率视觉条件**：将音频与视频潜变量沿时间维度对齐，并引入高帧率（24 fps）视觉嵌入，是实现精准音视频同步的关键。这需要设计一种新的跨模态融合机制，既能保留高帧率时序信息，又能高效融合语义上下文。

2. **自动化多维度偏好优化**：在无需人工标注的前提下，利用预训练模型自动评估生成音频的语义一致性和时序同步性，构建偏好数据以持续优化模型。这要求偏好信号本身具备可靠的多维度判别能力，且优化过程能够平衡语义与时序两个目标。

基于以上动机，本文提出**VisioSonic**：一个基于扩散变换器的V2A框架，通过多模态条件器与共注意力机制实现显式音视频对齐，并设计**STAR-DPO**（Semantic-Temporal Alignment-Ranked Direct Preference Optimization）流水线，利用ImageBind和Synchformer作为奖励模型自动生成偏好对，在整流流匹配范式下进行精细化偏好优化。

## 核心创新

VisioSonic 的核心创新在于系统性地解决了视频到音频生成中长期存在的“语义-时序双重对齐”瓶颈。现有方法（如 **MMAudio** (Cheng et al., CVPR 2025) 的自注意力联合训练、**Seeing-and-Hearing** (Xing et al., CVPR 2024) 的 ImageBind 对齐）往往在语义一致性和精细时间同步之间顾此失彼——要么生成语义正确但时序漂移的音频，要么时序准确但语义模糊。VisioSonic 通过三个相互耦合的关键设计突破这一瓶颈。

### 1. 高帧率视觉条件与显式时序对齐

传统 V2A 方法通常使用低帧率（4–8 fps）的视觉特征作为条件，导致快速视觉动态（如击鼓、敲击）的时序信息被严重压缩。VisioSonic 的关键改变在于**同时引入低帧率语义嵌入和高帧率时序嵌入**：一方面使用 CLIP 图像编码器提取语义级视觉特征，另一方面使用 Synchformer 以 24 fps 的高帧率提取帧级时序嵌入。这两种嵌入通过 Token Aligner 上采样后与音频潜变量沿时间维度显式拼接，迫使模型在生成过程中直接感知视频帧与音频帧的对应关系。这一设计是取得最低 DeSync（0.41）的核心因果机制——高帧率视觉流为音频事件的时间定位提供了精确的锚点。

### 2. 音频-视频-文本共注意力扩散变换器

不同于 MMAudio 使用的自注意力 MMDiT 架构或简单拼接融合，VisioSonic 设计了**音频-视频-文本共注意力机制**。该模块包含三个关键组件：
- **Token Aligner**：将视频嵌入上采样至与音频潜变量相同的时间分辨率，实现帧级对齐；
- **2D RoPE 位置编码**：在时频二维空间上编码位置信息，保留音频的频谱结构；
- **零初始化门控交叉注意力**：条件嵌入通过缩放和门控操作调控共注意力的输入与输出，确保训练初期稳定。

消融实验（Table 3）证实，同时使用文本和视频条件的共注意力变体（T+AV, Co-attn）在所有指标上均优于仅使用单一模态或自注意力融合的变体，验证了联合建模语义与时序信息的必要性。

### 3. STAR-DPO：语义-时序对齐排序直接偏好优化

这是 VisioSonic 最具特色的创新。传统 V2A 训练仅依赖流匹配损失，无法显式优化音视频同步质量。STAR-DPO 的核心洞察在于：**将预训练的 ImageBind 和 Synchformer 作为“奖励模型”，自动构造偏好数据，无需人工标注即可进行偏好优化**。具体流程为：
1. 使用预训练基线模型为每个视频生成五个音频候选；
2. 分别计算语义奖励（IB-score，基于 ImageBind 的音频-视频对齐分数）和时序奖励（DeSync，基于 Synchformer 的同步偏差）；
3. 联合单步排序（语义得分与时序得分直接求和）选出获胜与失败样本；
4. 使用 DPO 风格的排序损失结合流匹配正则化进行精细化训练：

$$L_{\mathrm{final}} = -\mathbb{E} \log \sigma \Bigg( -\beta \Big[ \big( L_{w} - L_{w}^{ref} \big) - \big( L_{l} - L_{l}^{ref} \big) \Big] \Bigg) + L_{\mathrm{RFM}}$$

其中 $L_{w}$ 和 $L_{l}$ 分别为获胜与失败样本的流匹配损失，$L_{w}^{ref}$ 和 $L_{l}^{ref}$ 为参考模型的对应损失。

消融实验揭示了两个关键结论：
- **联合使用语义和时序奖励优于单独使用任一奖励模型**（Table 4），说明语义一致性和时序同步性需要协同优化；
- **联合单步排序优于分步级联排序**（Table 6），表明多维度同步排名比串行过滤更有效；
- **第二次 DPO 迭代即可收敛**（Table 5），表明该方法高效且稳定。

### 4. 文本条件的语义增强

与 MMAudio 仅使用类别标签不同，VisioSonic 使用 LLM 生成的描述性标题（Auto-CAD）作为文本条件。这一改变使模型能够理解更丰富的场景语义（如“钢琴演奏者在昏暗灯光下弹奏柔和旋律”），而非仅依赖类别词（如“钢琴”），从而提升了生成音频的语义一致性。

### 创新总结

VisioSonic 的三个 changed slots——高帧率视觉条件、共注意力融合、STAR-DPO 偏好优化——形成了完整的因果链：高帧率条件提供精确时序信息，共注意力实现跨模态深度融合，STAR-DPO 在此基础上通过自动偏好优化进一步强化对齐质量。这一组合使 VisioSonic 以最少的可训练参数量（151M）取得了最高的 IB-score（33.1）和最低的 DeSync（0.41），在参数效率与生成质量之间实现了最优平衡。

## 整体框架

VisioSonic 的整体框架由两个阶段构成：**基础模型（Base Model）** 和 **STAR-DPO 偏好优化流水线**，如 Figure 2 所示。基础模型负责从视频和文本条件生成语义相关且时序同步的音频，STAR-DPO 则在无需人工标注的情况下，利用预训练模型自动构造偏好数据，对基础模型进行精细化优化。

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/002_Figure_2.jpg]]
*Figure 2: Overview of proposed VisioSonic: base model architecture (left) and STAR-DPO pipeline (right)*

### 基础模型架构

基础模型包含两大核心组件：**多模态条件器（Multimodal Conditioner）** 和 **基于共注意力的扩散变换器（Co-attention-based Diffusion Transformer）**。

**多模态条件器** 负责将视频和文本编码为条件嵌入，为音频生成提供语义和时序指导。具体而言，视觉条件采用双路编码：
- **语义嵌入**：使用 CLIP 图像编码器以低帧率提取视频帧的语义特征，捕捉全局场景和物体类别信息。
- **时序嵌入**：使用 Synchformer 以高帧率（24 fps）提取帧级视觉特征，保留精细的时间动态信息。

文本条件方面，VisioSonic 摒弃了传统的类别标签，转而使用 LLM 生成的描述性标题（Auto-CAD），为模型提供更丰富的上下文指导。这一设计相较于 **MMAudio**（Cheng et al., CVPR 2025）仅使用类别标签和自注意力机制的做法，提供了更细粒度的语义条件。

**Token Aligner** 是连接条件器与扩散变换器的关键模块。它将视频嵌入沿时间维度上采样，并与音频潜变量（audio latents）进行拼接，实现视频帧与音频 token 在时间维度上的显式对齐。这一设计直接回应了现有方法中音视频时间对应关系难以保证的瓶颈——通过将音频与视频潜变量沿时间维度对齐，并结合高帧率视觉条件，是实现精准音视频同步的核心机制。

**共注意力扩散变换器** 采用 16 个 DiT 块，每个块包含视频-文本-音频共注意力模块、前馈网络和条件投影器。其共注意力机制的具体运作方式为：
1. 将拼接后的视频-音频 token 序列与文本 token 分别进行注意力计算；
2. 将两次注意力的输出求和，得到最终的共注意力输出；
3. 条件嵌入通过两个独立层对共注意力块的输入和输出分别进行缩放（scaling）和门控（gating）操作。

此外，变换器还引入了 2D RoPE 位置编码和零初始化门控的交叉注意力，以增强位置感知和训练稳定性。整个去噪过程基于**整流流匹配（Rectified Flow Matching）**，训练模型预测噪声与数据之间的速度向量场：

$$L_{\mathrm{RFM}} = \mathbb{E}_{t, p_0(a_0), p_1(a_1)} \| v_{\theta}(t, a_t, C) - (a_1 - a_0) \|_2^2$$

其中 $a_0$ 为噪声，$a_1$ 为目标音频，$a_t$ 为中间状态，$C$ 为条件信息。

### STAR-DPO 偏好优化流水线

在基础模型预训练完成后，STAR-DPO（Semantic-Temporal Alignment-Ranked Direct Preference Optimization）流水线对其进行精细化优化。该流水线的核心洞察是：将 ImageBind 和 Synchformer 作为奖励模型自动生成偏好对，可以在无需人工标注的情况下持续优化生成质量。

流水线的工作流程如下：
1. **候选生成**：对于每个训练样本，将视频轨道和文本描述输入预训练的基础模型，生成五个音频候选。
2. **自动排序**：使用奖励模型对生成的视频-音频对进行排序。奖励信号包括语义奖励（基于 ImageBind 的 IB-score）和时序奖励（基于 Synchformer 的 DeSync），两者联合单步排序（直接求和）以构建偏好数据。
3. **偏好优化**：基于排序结果确定获胜样本（winner）和失败样本（loser），分别计算其流匹配损失 $L_w$ 和 $L_l$，并结合参考模型损失构造 DPO 排序损失。最终优化目标为：

$$L_{\mathrm{final}} = -\mathbb{E} \log \sigma \Bigg( -\beta \Big[ \big( L_{w} - L_{w}^{ref} \big) - \big( L_{l} - L_{l}^{ref} \big) \Big] \Bigg) + L_{\mathrm{RFM}}$$

其中 $L_{w} = \| u(a_{t}^{w}, t, C; \theta) - v_{t}^{w} \|_{2}^{2}$，$L_{l} = \| u(a_{t}^{l}, t, C; \theta) - v_{t}^{l} \|_{2}^{2}$，$\beta$ 控制偏好优化的强度，$L_{\mathrm{RFM}}$ 作为正则化项保留基础生成能力。

消融实验表明，联合使用语义奖励和时序奖励的 STAR-DPO 效果最佳，且第二次 DPO 迭代即可收敛（Table 4, Table 5）。联合单步排序（语义+时序得分直接求和）优于分步级联排序，表明多维度同步排名更有效（Table 6）。

### 输入输出流总结

整体 pipeline 的输入输出流可概括为：
- **输入**：视频帧序列 + 文本描述（Auto-CAD 生成）
- **条件编码**：CLIP 语义嵌入（低帧率）+ Synchformer 时序嵌入（高帧率 24 fps）+ 文本嵌入
- **Token 对齐**：视频嵌入上采样后与音频潜变量沿时间维度拼接
- **扩散生成**：共注意力 DiT 在整流流匹配框架下迭代去噪
- **偏好优化**：STAR-DPO 利用自动排序的偏好数据进一步精细化模型
- **输出**：与视频语义一致且时序同步的音频波形

### 补充图表

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/001_Figure_1.jpg]]
*Figure 1: Comparison with other V2A models*

## 核心模块与公式推导

VisioSonic 的整体架构由两大核心组件构成：**多模态条件器 (Multimodal Conditioner)** 与基于**共注意力的扩散变换器 (Co-attention Diffusion Transformer)**，如 Figure 2 左侧所示。其生成过程建立在整流流匹配 (Rectified Flow Matching) 框架之上。

### 整流流匹配基础

VisioSonic 在音频潜空间中进行流匹配生成。给定音频波形 $A$，首先通过短时傅里叶变换 (STFT) 和预训练的 VAE 编码器 $\mathcal{E}_a$ 将其压缩为潜变量 $z_a$：

$$z_a = \mathcal{E}_a(A)$$

潜变量维度为 $\dot{z}_a \in \mathbb{R}^{N \times D}$，其中 token 数量 $N = \frac{T}{r_a} \times \frac{F}{r_a}$，$T$ 和 $F$ 分别为时间和频率维度，$r_a$ 为压缩比。

模型训练的核心目标是学习速度向量场 $v_\theta$，以从噪声 $a_0$ 恢复数据 $a_1$。整流流匹配损失函数定义为：

$$L_{\mathrm{RFM}} = \mathbb{E}_{t, p_0(a_0), p_1(a_1)} \| v_{\theta}(t, a_t, C) - (a_1 - a_0) \|_2^2$$

其中 $a_t = t a_1 + (1-t) a_0$ 为时间 $t$ 处的插值样本，$C$ 为条件信息。

### 多模态条件器

多模态条件器负责将视频和文本编码为条件嵌入，为音频生成提供语义和帧级时序指导。其关键设计在于**同时使用两种互补的视觉嵌入**：

- **语义嵌入**：使用 CLIP 模型以低帧率（如 4-8 fps）提取视频帧特征，捕获全局语义信息。
- **时序嵌入**：使用 Synchformer 模型以高帧率（24 fps）提取视觉特征，保留精细的时间动态信息。

这种双流设计解决了现有方法中“语义理解”与“时序同步”难以兼顾的瓶颈——低帧率嵌入提供丰富的语义上下文，高帧率嵌入则为精确的音视频时间对齐提供必要的视觉线索。

### Token 对齐器与共注意力块

**Token Aligner** 将视频嵌入沿时间维度上采样，使其与音频潜变量的时间分辨率匹配，然后将两者沿时间轴拼接。这一显式对齐操作是确保音视频同步的关键机制。

**Co-attention Block** 是扩散变换器的核心计算单元。与 MMAudio 等采用自注意力或简单拼接的方法不同，VisioSonic 设计了音频-视频-文本共注意力机制：

1. 对齐后的视频-音频拼接序列与文本条件嵌入共同进入共注意力模块。
2. 条件嵌入通过两个独立的全连接层，分别对共注意力块的输入进行**缩放 (scaling)** 和输出进行**门控 (gating)** 操作。
3. 最终输出为两路注意力结果之和。

去噪骨干网络包含 16 个 DiT 块，每个块均配备视频-文本-音频共注意力模块、前馈网络和条件投影器。此外，模型引入 2D RoPE 位置编码和零初始化门控的交叉注意力，以稳定训练并增强时序建模能力。

### STAR-DPO 偏好优化

在基础模型之上，VisioSonic 进一步提出 **STAR-DPO (Semantic-Temporal Alignment-Ranked Direct Preference Optimization)**，在无需人工标注的情况下自动构造偏好数据并优化生成质量。

**偏好数据构造**：对每个训练样本，使用预训练基线模型生成五个音频候选，然后利用奖励模型对候选进行排序。奖励模型包括：
- **语义奖励**：基于 ImageBind 的 IB-score，评估音视频语义一致性。
- **时序奖励**：基于 Synchformer 的 DeSync 指标，评估音视频时间同步性。

**优化目标**：对于偏好对中的获胜样本 $a_t^w$ 和失败样本 $a_t^l$，分别计算其流匹配损失：

$$L_w = \| u(a_t^w, t, C; \theta) - v_t^w \|_2^2$$

$$L_l = \| u(a_t^l, t, C; \theta) - v_t^l \|_2^2$$

以及参考模型（冻结的基础模型参数 $\theta_{\mathrm{ref}}$）下的对应损失 $L_w^{ref}$ 和 $L_l^{ref}$。最终 STAR-DPO 损失结合 DPO 排序目标与流匹配正则化：

$$L_{\mathrm{final}} = -\mathbb{E} \log \sigma \Bigg( -\beta \Big[ \big( L_w - L_w^{ref} \big) - \big( L_l - L_l^{ref} \big) \Big] \Bigg) + L_{\mathrm{RFM}}$$

其中 $\beta$ 控制偏好优化的强度，$\sigma$ 为 sigmoid 函数。该损失函数的核心洞察在于：通过最小化获胜样本相对于参考模型的损失增量，同时最大化失败样本的损失增量，驱动模型向更优的音视频对齐方向更新。

## 实验与分析

### 主实验结果

VisioSonic在VGGSound测试集上进行了全面的定量评估，与多个最新的视频到音频生成方法进行了对比，包括**MMAudio** (Cheng et al., CVPR 2025)、**Frieren** (Wang et al., NeurIPS 2024)、**Diff-Foley** (Luo et al., NeurIPS 2023)、**Foley-Crafter** (Zhang et al., IJCV 2026)、**Seeing-and-Hearing** (Xing et al., CVPR 2024)、**V2A-Mapper** (Wang et al., AAAI 2024)、**Kling-Foley** (Wang et al., arXiv 2025)和**HunyuanVideoFoley** (Shan et al., arXiv 2025)。评估指标涵盖音频保真度（FDPaSST、FDPANNs、FDvGG、KLPANNs、KLPaSST）、语义对齐（IS、IB-score）和时间同步性（DeSync）。

如Table 1所示，VisioSonic-Base以最少的可训练参数量（151M）在关键指标上取得了显著优势。其IB-score达到32.8，DeSync降至0.45，均优于包括MMAudio-S（IB-score 32.27，DeSync 0.444）在内的所有对比方法。在音频保真度方面，VisioSonic-Base的FDPaSST为58.27、FDPANNs为4.41，同样表现最佳。这表明高帧率视觉条件与音频-视频-文本共注意力机制的设计有效提升了语义一致性和时序同步精度。

加入STAR-DPO后，VisioSonic在所有指标上进一步提升：IB-score达到33.1，DeSync降至0.41，FDPaSST降至55.48，FDvGG降至0.99。这表明基于预训练模型自动构造偏好数据的偏好优化策略能够持续改善生成质量，且无需额外的人工标注成本。

在零样本跨域评估（Table 2）中，VisioSonic在多个域外基准上同样展现出较强的泛化能力，验证了模型对未见场景的适应性。

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/004_Table_2.jpg]]
*Table 2: Zero-shot evaluation on out-of-domain benchmarks. The best results are marked with bold, and the second ones are marked with underline*

用户研究（Table 7）进一步证实了VisioSonic的主观优势。VisioSonic w/ STAR-DPO在整体评分（1-5分制）上获得4.60分，为所有方法中最高，表明自动评价指标的提升与人类感知一致。

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/009_Table_7.jpg]]
*Table 7: Comparison results from the user study*

### 消融实验

**模态融合策略分析**（Table 3）：消融实验对比了多种模态融合变体，包括仅使用文本条件（T）、仅使用视频条件（V）、以及文本与视频联合条件下的不同注意力机制。结果表明，同时使用文本和视频条件的共注意力变体（T+AV, Co-attn）在所有指标上全面领先，验证了多模态联合建模和共注意力机制对生成质量的关键作用。

**奖励模型选择**（Table 4）：STAR-DPO支持使用不同的奖励模型生成偏好对。实验对比了仅使用语义奖励（IB-AV）、仅使用时序奖励（DeSync）以及两者联合使用的效果。结果显示，联合使用语义和时序奖励模型在所有指标上均优于单一奖励模型，表明多维度的同步排名能更全面地衡量生成质量。

**DPO迭代次数**（Table 5）：实验考察了STAR-DPO的迭代次数对性能的影响。结果表明，第二次DPO迭代即可达到最优性能，继续迭代未见显著提升，说明偏好优化过程具有快速收敛的特性。

**排序流水线设计**（Table 6）：对比了分步级联排序（先按语义排序再按时序排序）与联合单步排序（语义和时序得分直接求和）两种策略。联合单步排序在所有指标上均优于级联排序，表明多维度同步排名比分步筛选更有效。

### 失败模式与局限性

尽管VisioSonic在主流基准上取得了最优性能，分析中仍揭示了若干需要注意的边界条件：

1. **训练数据同步性限制**：VGGSound数据集中部分样本的原始音视频同步性可能较弱，这导致模型在某些场景下仍可能产生非剧情性声音，即生成的音频与视频事件之间的因果关系不够紧密。这是数据驱动的固有局限，需要更高质量的训练数据来缓解。

2. **偏好排序的评估偏差**：STAR-DPO的性能上限受限于ImageBind和Synchformer作为奖励模型的质量。若这些预训练模型在某些音频-视频对上的评估存在系统性偏差，可能引导偏好优化朝着次优方向进行。这一风险在当前实验中尚未被充分量化。

3. **长视频与复杂场景未验证**：用户研究规模有限，且所有测试样本均为10秒短视频。模型在长视频、多事件交替、背景噪声复杂等场景下的音视频同步稳定性尚未得到验证，这是实际部署前需要进一步评估的关键问题。

4. **计算资源与部署权衡**：尽管VisioSonic-Base的可训练参数量最少（151M），但高帧率视觉条件（24fps Synchformer嵌入）和STAR-DPO的候选生成-排序流程增加了推理成本。在资源受限设备上的部署需要额外的工程优化。

### 补充图表

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/003_Table_1.jpg]]
*Table 1: Comparison results with existing SOTA video-to-audio models on VGGSound [3] test set. The best results are marked with bold, and the second ones are marked with underline*

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/005_Table_3.jpg]]
*Table 3: Comparison results on modality fusion variants*

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/007_Table_4.jpg]]
*Table 4: Effects of various reward models*

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/010_Table_5.jpg]]
*Table 5: Performance across DPO iterations*

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/008_Table_6.jpg]]
*Table 6: Comparison results with different ranking pipelines*

![[assets/figures/papers/paper_list_l2683_https_openaccess_thecvf_com_content_CVPR2026_html_Wang_Hear_What_You_See/figures/006_Figure_3.jpg]]
*Figure 3: Visualization of generated audio spectrograms. “SAH” means the Seeing&Hearing method [47]. More subjective results are referred to the video demo in the supplementary material*

## 方法谱系与知识库定位

### 1. 与现有方法的差异化定位

VisioSonic 的核心贡献在于同时解决视频到音频生成（V2A）中的**语义一致性**与**时序同步性**两大瓶颈，其设计路线与现有工作形成了清晰的演进关系。

**与基于联合训练的方法对比。** **MMAudio**（Cheng et al., CVPR 2025）是同期最具竞争力的多模态联合训练方法，采用自注意力变换器融合视频与音频特征，但其仅依赖类别标签作为文本条件，且视觉条件帧率较低。VisioSonic 在此基础上做了三个关键改进：（1）用**共注意力（co-attention）**替代自注意力，显式建模视频-文本-音频三模态间的交叉关系；（2）引入**LLM生成的描述性标题**（Auto-CAD）替代简单的类别标签，提供更丰富的语义上下文；（3）同时使用低帧率CLIP语义嵌入和高帧率（24fps）Synchformer嵌入，弥补了低帧率条件在时序精度上的不足。这些改进使 VisioSonic-Base 在仅 151M 可训练参数的条件下，即在 VGGSound 测试集上取得了最高的 IB-score（32.8）和最低的 DeSync（0.45），显著优于 MMAudio-S（IB-score 32.27，DeSync 0.444）（Table 1）。

**与基于整流流/扩散的方法对比。** **Frieren**（Wang et al., NeurIPS 2024）和 **Diff-Foley**（Luo et al., NeurIPS 2023）分别代表了整流流匹配和潜在扩散在 V2A 中的应用。VisioSonic 继承了整流流匹配的高效采样特性，但在条件注入方式上有本质区别：Frieren 等方法的视觉条件通常以拼接或简单交叉注意力的方式融入，而 VisioSonic 通过 **Token Aligner** 将视频嵌入沿时间维度上采样后与音频潜变量显式对齐，再送入共注意力模块，从根本上强化了音视频的时序对应关系。

**与带显式控制器的方法对比。** **FoleyCrafter**（Zhang et al., IJCV 2026）设计了独立的语义和时序控制器，但控制器与生成主干之间的耦合较为松散。VisioSonic 将语义与时序条件统一于共注意力框架内，避免了多控制器之间的协调问题，结构更为紧凑。

**与基于表示对齐的方法对比。** **Seeing-and-Hearing**（Xing et al., CVPR 2024）利用 ImageBind 实现开放域的音视频对齐，**V2A-Mapper**（Wang et al., AAAI 2024）则将视频特征映射为文本嵌入空间。VisioSonic 借鉴了表示对齐的思想，但将其应用于偏好优化阶段（STAR-DPO），而非生成主干本身——通过 ImageBind 和 Synchformer 作为奖励模型自动构建偏好数据，实现了无需人工标注的精细化训练。

**与同期多模态扩散变换器方法对比。** **Kling-Foley**（Wang et al., arXiv 2025）和 **HunyuanVideoFoley**（Shan et al., arXiv 2025）同样探索了多模态扩散变换器在 V2A 中的应用，但均未引入偏好优化机制。VisioSonic 的 STAR-DPO 为这一技术路线提供了可扩展的后训练优化范式。

### 2. 适用边界与局限性

尽管 VisioSonic 在 VGGSound 基准上取得了 SOTA 性能，其适用边界受以下因素制约：

**训练数据的同步性上限。** VGGSound 数据集中部分样本的原始音视频同步性较弱，模型可能从数据中学习到不精确的同步关系。这意味着即使模型设计上强化了时序对齐，在某些场景下仍可能产生非剧情性声音（non-diegetic sound）。这是数据驱动的 V2A 方法共有的瓶颈，而非 VisioSonic 特有的缺陷。

**偏好优化的奖励模型偏差。** STAR-DPO 的偏好排序完全依赖 ImageBind 和 Synchformer 的评估质量。若这两个预训练模型在特定音频类别或视觉场景上存在系统性偏差，将直接影响偏好数据的质量，进而误导 DPO 的优化方向。例如，ImageBind 对某些语义类别的敏感度可能高于其他类别，导致偏好排序在跨类别场景下不够均衡。

**时间尺度的限制。** 当前验证均在 10 秒短视频上进行（用户研究亦仅限于此长度）。对于长视频场景，维持全局语义一致性和长时间范围的精细同步仍是未经验证的挑战。长视频中的音频事件密度变化、场景切换等因素可能使现有架构面临新的困难。

**用户研究规模有限。** 用户研究虽显示 VisioSonic w/ STAR-DPO 获得了最高主观评分（4.60/5.00），但研究规模有限，且评估场景受限于 10 秒短视频。在更复杂的音频场景（如重叠声源、动态背景噪声变化）下的人类感知偏好尚待系统验证。

### 3. 开放问题

VisioSonic 的设计框架为 V2A 领域留下了若干值得探索的方向：

- **长视频与开放域扩展。** 如何将 VisioSonic 的共注意力对齐机制和 STAR-DPO 扩展到开放域长视频生成，并在场景切换、事件密度剧烈变化时维持稳定的音视频同步，是下一步的核心挑战。这可能需要对 Token Aligner 进行层次化改造，或引入记忆机制来处理长时序依赖。

- **多模态大模型融入评价体系。** 当前 STAR-DPO 依赖 ImageBind 和 Synchformer 作为奖励模型，其评估能力受限于预训练任务。能否将视频-语言大模型（如 Video-LLaMA 等）融入偏好排序，利用其更强的语义理解和推理能力实现更精细的偏好优化，是一个有前景的方向。

- **部署效率与精度的权衡。** VisioSonic 的共注意力模块和 STAR-DPO 的多轮采样在计算资源受限的设备上部署时面临挑战。如何在保持同步精度的前提下降低推理成本——例如通过蒸馏、量化或减少 DPO 迭代中的候选采样数——是实用化道路上的关键问题。

- **偏好优化的理论收敛性。** 消融实验表明 STAR-DPO 在第二次迭代即可收敛（Table 5），但这一经验观察背后的理论原因尚不明确。理解 DPO 在流匹配框架下的收敛性质，有助于设计更高效的迭代策略和更合理的奖励模型组合方式。

## 原文 PDF

![[paperPDFs/CVPR_2026/Hear_What_You_See_Video_to_Audio_Generation_with_Diffusion_Transformer_and_Semantic_Temporal_Alignment_Ranked_Direct_Preference_Optimization.pdf]]
