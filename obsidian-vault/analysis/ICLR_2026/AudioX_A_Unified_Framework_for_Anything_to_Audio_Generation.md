---
title: "AudioX: A Unified Framework for Anything-to-Audio Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AudioX_A_Unified_Framework_for_Anything_to_Audio_Generation.pdf
project_link: https://zeyuet.github.io/AudioX/
code_link: null
aliases:
- AudioX
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "用多模态自适应融合模块条件化DiT统一生成音效和音乐。"
primary_logic: "AudioX分别编码文本、视频和音频条件，经MAF门控与查询注意力融合后驱动扩散Transformer生成音频。"
claims:
- "AudioX统一支持文本、视频、音频及其组合到音效或音乐的生成任务。"
- "MAF通过门控、可学习查询交叉注意力和残差更新减少跨模态干扰。"
- "IF-caps的大规模高质量指令标注对细粒度指令跟随能力至关重要。"
- "数据和MAF消融显示更高质量文本监督与完整融合模块能联合提升多种条件模态表现。"
---

# AudioX: A Unified Framework for Anything-to-Audio Generation

> [!tip] 核心洞察
> 通过统一的多模态训练，可以产生跨模态正则化效应：提高文本监督的质量和粒度可以减少对齐噪声，从而联合提升所有条件模态的性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AudioX：面向任意输入到音频生成的统一框架 |
| 英文题名 | AudioX: A Unified Framework for Anything-to-Audio Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qjJWxK3yWo) · [Project](https://zeyuet.github.io/AudioX/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AudioX |
| Dataset | AudioCaps |

> [!tip] 效果简介
> - AudioCaps 上，KL↓ 为 1.39，对比 （见表1），变化 SOTA。
> - AudioCaps 上，IS↑ 为 10.22，对比 （见表1），变化 SOTA。
> - AudioCaps 上，FD↓ 为 13.29，对比 （见表1），变化 SOTA。

## 概要

本文提出 **AudioX**，一个基于 Diffusion Transformer (DiT) 的统一框架，旨在解决“任意输入到音频生成”（Anything-to-Audio Generation）问题。该框架能够灵活处理文本、视频、音频等多种输入模态的任意组合，并统一生成音效与音乐。核心贡献包括：(1) 提出轻量级的多模态自适应融合模块（Multimodal Adaptive Fusion, MAF），用于自适应加权和对齐多模态条件嵌入；(2) 构建大规模、高质量的多模态数据集 **IF-caps**（Instruction-Following），包含超过700万样本，通过结构化标注和数据增强生成；(3) 在多个基准测试中达到或超越现有技术水平，尤其在指令跟随能力上大幅领先。



现有音频生成模型通常局限于单一条件模态（如仅文本或仅视频）和单一输出域（仅音效或仅音乐），缺乏统一的框架来灵活处理多种模态组合的输入。此外，高质量、大规模的多模态训练数据也相对匮乏。这种碎片化的现状限制了模型在复杂多模态场景下的泛化能力和实用性。AudioX 旨在通过统一的多模态训练框架和高质量数据集，克服这些瓶颈。



## 核心方法与创新机理

1.  **统一框架**：基于 Diffusion Transformer (DiT) 构建，支持文本、视频、音频多种输入模态，统一生成音效和音乐。
2.  **多模态自适应融合模块 (MAF)**：提出轻量级的 MAF 模块，通过门控滤波、可学习查询交叉注意力和自注意力残差更新，自适应地加权和对齐多模态条件嵌入，减少跨模态干扰。
3.  **大规模多模态数据集 IF-caps**：通过结构化标注和数据增强管道构建，包含超过700万样本，支持细粒度的指令跟随。
4.  **跨模态正则化效应**：通过统一的多模态训练，产生跨模态正则化效应：提高文本监督的质量和粒度可以减少对齐噪声，从而联合提升所有条件模态的性能。



![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/001_Figure_1.jpg]]
*Figure 1: (a) Comprehensive performance comparison*

AudioX 的整体框架如 **Figure 4** 所示。其核心流程为：首先，视频、文本和音频模态分别通过专用编码器提取特征；然后，这些特征被送入 MAF 模块进行自适应融合，生成统一的多模态条件嵌入 H_c；最后，DiT 主干网络以 H_c 为条件，通过交叉注意力机制对噪声潜变量 z_t 进行去噪，生成高保真音频。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/005_Figure_4.jpg]]



### 5.1 多模态自适应融合模块 (MAF)

MAF 模块是 AudioX 的核心组件，其工作流程如下：
1.  **门控滤波**：来自各模态的初始特征嵌入首先通过门控（gates）进行滤波和重新加权，以抑制噪声并保留最具信息量的线索。
2.  **交叉注意力**：门控后的嵌入被拼接，并通过可学习查询（learnable queries）进行交叉注意力计算，以聚合多模态上下文。
3.  **自注意力与残差更新**：最后，通过自注意力层整合聚合后的上下文，并将精炼后的信息通过残差更新（residual updates）分发回各模态路径。

该过程产生校准后的、模态特定的输出，然后拼接形成最终的多模态条件嵌入 H_c，如公式 (1) 所示：

$$
\tilde { \mathbf { H } } _ { \mathrm { v } } , \tilde { \mathbf { H } } _ { \mathrm { t } } , \tilde { \mathbf { H } } _ { \mathrm { a } } = \mathrm { M A F } ( \mathbf { H } _ { \mathrm { v } } , \mathbf { H } _ { \mathrm { t } } , \mathbf { H } _ { \mathrm { a } } ) , \quad \mathbf { H } _ { \mathrm { c } } = \mathrm { C o n c a t } \Big ( \tilde { \mathbf { H } } _ { \mathrm { v } } , \tilde { \mathbf { H } } _ { \mathrm { t } } , \tilde { \mathbf { H } } _ { \mathrm { a } } \Big ) .
$$

### 5.2 扩散过程

AudioX 采用标准的扩散模型框架。前向扩散过程是一个马尔可夫链，逐步向数据添加噪声：

$$
q ( \mathbf { z } _ { t } | \mathbf { z } _ { t - 1 } ) = \mathcal { N } ( \mathbf { z } _ { t } ; \sqrt { 1 - \beta _ { t } } \mathbf { z } _ { t - 1 } , \beta _ { t } \mathbf { I } )
$$

反向去噪过程训练一个变换器网络 ε_θ 来逐步去除噪声，其条件为噪声潜变量 z_t、时间步 t 和多模态嵌入 H_c：

$$
p _ { \theta } \left( \mathbf { z } _ { t - 1 } | \mathbf { z } _ { t } \right) = \mathcal { N } \left( \mathbf { z } _ { t - 1 } ; \mu _ { \theta } \left( \mathbf { z } _ { t } , t , \mathbf { H } _ { \mathrm { c } } \right) , \boldsymbol { \Sigma } _ { \theta } \left( \mathbf { z } _ { t } , t , \mathbf { H } _ { \mathrm { c } } \right) \right)
$$

训练目标是最小化真实噪声与预测噪声之间的均方误差：

$$
\operatorname* { m i n } _ { \theta } \mathbb { E } _ { t , \mathbf { z } _ { t } , \epsilon } \left\| \epsilon - \epsilon _ { \theta } \left( \mathbf { z } _ { t } , t , \mathbf { H } _ { \mathrm { c } } \right) \right\| _ { 2 } ^ { 2 }
$$

### 5.3 编码器与训练细节

- **视频编码**：使用 CLIP-ViT-B/32 (Radford et al., 2021) 以 5 fps 提取视频帧特征，并使用 Synchformer (Iashin et al., 2024) 以 25 fps 提取同步特征。
- **文本编码**：使用 T5-base (Raffel et al., 2020)。
- **音频编码/解码**：使用音频自编码器 (Evans et al., 2024b)。
- **时间动态**：视频和音频特征通过时间变换器处理。
- **投影**：所有模态特征通过投影头映射为域特定嵌入 (H_v, H_t, H_a)。
- **模型规模**：总参数量 2.4B（可训练 1.1B），MAF 模块仅 60M 参数。
- **训练配置**：使用 AdamW 优化器，基础学习率 1e-5，权重衰减 0.001，批次大小 48，推理步数 250，CFG 尺度 7.0。训练在三个 NVIDIA H800 GPU 集群上进行，约需 4k GPU 小时。



## 实验与关键发现

### 6.1 主要结果

**Table 1** 展示了 AudioX 在多个任务和数据集上的性能评估，包括文本到音频（T2A）、视频到音频（V2A）、文本+视频到音频（TV2A）、文本到音乐（T2M）、视频到音乐（V2M）和文本+视频到音乐（TV2M）。AudioX 在多个基准测试中达到或超越现有技术水平。


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/006_Table_1.jpg]]
*Table 1: Performance evaluation across various tasks and datasets. Task abbreviations are: T2A (Text-to-Audio), V2A (Video-to-Audio), TV2A (Text-and-Video-to-Audio), T2M (Text-to-Music), V2M (Video-to-Music), and TV2M (Text-and-Video-to-Music). For alignment (Align.), we use the CLAP score for text and the Imagebind AV score for video inputs.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/006_Table_1.jpg]]

**Table 2** 展示了在 T2A-bench 和 AudioTime 上的指令跟随能力评估。AudioX 在所有维度上大幅超越基线方法，尤其在 T2A-bench 上，Category Accuracy (Cat-acc) 达到 34.20，Count Accuracy (Cnt-acc) 达到 12.40，Ordering Accuracy (Ord-acc) 达到 23.60，Timestamp Accuracy (TS-acc) 达到 28.20。在 AudioTime 的 Ordering 指标上达到 0.34。


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/007_Table_2.jpg]]
*Table 2: Evaluation of instruction-following T2A ability on the T2A-bench and AudioTime.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/007_Table_2.jpg]]

**Figure 1** 直观展示了 AudioX 在综合基准测试（Inception Score）和指令跟随基准测试上的性能优势。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/002_Figure_1.jpg]]

### 6.2 消融研究

**数据策略消融 (Table 3)**：完整的数据标注流程（GeminiCap-aug）在所有通用任务（T2A, V2A, TV2A）上取得最佳性能，并且是实现细粒度控制的关键。


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/008_Table_3.jpg]]
*Table 3: Ablation study on data curation strategies. We compare our model’s performance when trained with captions from different sources. The results show a clear trend of improvement with higher-quality data. Our full pipeline (GeminiCap-aug) not only achieves the best performance on all general tasks (T2A, V2A, TV2A) but is also essential for enabling fine-grained control.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/008_Table_3.jpg]]

**MAF 架构消融 (Table 4)**：完整的 MAF 模块（包含门控和查询机制）在大多数指标上取得最佳性能，证实了完整设计对于有效多模态融合的必要性。


![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/009_Table_4.jpg]]
*Table 4: Ablation study of the MAF architecture components. We evaluate the contribution of the Gate and Query mechanisms by removing them individually. The results show that the Full MAF, which includes both components, achieves the best performance across most metrics. This confirms that our complete design is essential for effective multimodal fusion.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/009_Table_4.jpg]]

**统一模型消融 (Figure A.3)**：
- 统一模型在模态内任务（T2A, V2A, 音频修补）上持续优于专门模型。
- 在音乐生成中，随着条件模态的增加（如从仅视频到视频+文本），性能逐步提升。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/023_Figure_13.jpg]]

### 6.3 额外任务

- **音频修补 (Table A.4)**：在 AudioCaps 和 AVVP 数据集上，AudioX 在音频和文本条件下优于基线方法。
- **音乐完成 (Table A.5)**：随着输入模态的增加，模型性能逐步提升。
- **图像到音频 (Table A.6)**：零样本评估中，AudioX 在 FAD 指标上优于基线方法。

### 6.4 用户研究

**Figure A.2** 展示了用户研究结果，10 名专业音频专家对生成样本的总体质量（OVL）和与提示的相关性（REL）进行评分（1-100 分）。AudioX 在大多数任务上取得了主观 SOTA 性能。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/022_Figure_12.jpg]]

### 6.5 公平性说明

- 用户研究涉及 10 名专业音频专家，对随机选取的样本进行 OVL 和 REL 评分，但未报告评分者间信度。
- T2A-bench 的自动评估使用 Gemini 2.5 Pro 作为评判者，可能存在模型偏见。
- 未讨论模型在不同音频类型（如音乐与音效）或不同语言/文化背景下的公平性表现。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_qjJWxK3yWo_AudioX_A_Unifie/figures/010_Table_5.jpg]]
*Table 5: Table A.1: Comprehensive overview of training and test datasets, detailing the number of clips (# Clips), average duration per clip (Dur./Clip in seconds), and total duration (Dur. in hours) for each task and split. T2A: Text-to-Audio, V2A: Video-to-Audio, TV2A: Text-and-Video-to-Audio, T2M: Text-to-Music, V2M: Video-to-Music, TV2M: Text-and-Video-to-Music.*




## 定位与知识库关联

AudioX 属于多模态生成模型领域，特别是“任意输入到音频生成”这一新兴方向。它与以下工作密切相关：

- **文本到音频/音乐**：AudioLDM-L-Full, AudioLDM-2-Full-Large, MAGNET-large, MuMu-LLaMA, CMT。
- **视频到音频/音乐**：VidMuse, Video2Music, Seeing&Hearing, Im2Wav。
- **多模态融合**：MMAUDIO (Cheng et al., 2025) 等。

AudioX 的核心定位是提供一个统一的、可扩展的框架，通过创新的 MAF 模块和高质量数据集 IF-caps，在保持模态内任务高性能的同时，显著提升跨模态任务和指令跟随能力。其提出的跨模态正则化效应为多模态生成模型的训练提供了新的理论视角。



## 原文 PDF

![[paperPDFs/ICLR_2026/AudioX_A_Unified_Framework_for_Anything_to_Audio_Generation.pdf]]
