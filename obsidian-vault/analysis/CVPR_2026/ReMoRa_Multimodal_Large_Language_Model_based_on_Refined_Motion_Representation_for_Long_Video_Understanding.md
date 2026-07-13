---
title: "ReMoRa: Multimodal Large Language Model based on Refined Motion Representation for Long-Video Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReMoRa_Multimodal_Large_Language_Model_based_on_Refined_Motion_Representation_for_Long_Video_Understanding.pdf
project_link: null
code_link: null
aliases:
- ReMoRa
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用压缩视频编解码器结构，以低成本的I帧和运动向量替代全解码RGB帧，实现密集时间覆盖并避免冗余。
primary_logic: 视频编解码器天然分离关键帧与运动描述符，块级运动向量可经细化模块逼近密集光流保真度，从而在压缩域高效捕获精细时空动态，同时通过状态空间模型实现线性复杂度的长程依赖建模。
claims:
- ReMoRa 在 LongVideoBench、NExT-QA、MLVU 上取得最高得分，平均分 69.8 超过所有基线。
- 去除 RMR 模块或光流预训练导致性能持续下降，证明 RMR 模块对运动质量至关重要。
- HMSS 聚合优于交叉注意力和相加融合，验证了结构化时间建模的有效性。
- LongVideoBench 上 Score = 60.8
---

# ReMoRa: Multimodal Large Language Model based on Refined Motion Representation for Long-Video Understanding

> [!tip] 核心洞察
> 视频编解码器天然分离关键帧与运动描述符，块级运动向量可经细化模块逼近密集光流保真度，从而在压缩域高效捕获精细时空动态，同时通过状态空间模型实现线性复杂度的长程依赖建模。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReMoRa：基于精细化运动表示的长视频多模态大语言模型 |
| 英文题名 | ReMoRa: Multimodal Large Language Model based on Refined Motion Representation for Long-Video Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.16412) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReMoRa |
| Dataset | LongVideoBench, NExT-QA, MLVU, Average |

> [!tip] 效果简介
> - LongVideoBench 上，Score 60.8 vs 59.5 (BIMBA) (+1.3)。
> - NExT-QA 上，Score 84.2 vs 83.2 (BIMBA / LLaVA-Video) (+1.0)。
> - MLVU 上，Score 72.1 vs 70.8 (LLaVA-Video) (+1.3)。

## 概要

长视频理解的核心瓶颈在于：完整解码 RGB 帧序列会引入极高的计算冗余，而 Transformer 自注意力的二次复杂度进一步限制了可处理的时长。视频编解码器天然将关键帧与帧间运动描述符分离，这一结构提供了在压缩域直接建模时空动态的可能性。ReMoRa 正是利用该性质，以稀疏 I 帧保留外观、以块级运动向量替代全解码帧，从而在密集时间覆盖与计算效率之间取得平衡。

**核心思路**：通过精细化运动表示（Refined Motion Representation, RMR）模块将粗糙、含噪的块级运动向量去噪并稠密化，使其逼近密集光流的保真度；再借助层次化运动状态空间（Hierarchical Motion State Space, HMSS）模块，以线性复杂度的状态空间模型（Mamba）在 GOP 内融合运动与外观，并在 GOP 间建模长程依赖，最终将压缩域的视频特征对齐到大语言模型。

**主要结果**：ReMoRa 在 LongVideoBench（60.8）、NExT-QA（84.2）、MLVU（72.1）三项长视频理解基准上均取得最高分数，五项基准平均分 69.8，超越最强基线 **BIMBA** 和 **LLaVA-Video**（Zhang et al., arXiv 2024）约 0.9 分。消融实验证实，去除 RMR 模块或光流预训练会导致性能持续下降，而 HMSS 的结构化时间聚合显著优于简单的交叉注意力或相加融合，验证了压缩域运动精细化与分层时序建模的有效性。



### 长视频理解的效率瓶颈

多模态大语言模型（MLLM）在视频理解领域取得了显著进展，但现有方法普遍采用均匀采样 RGB 帧序列作为输入表示。这一范式在处理长视频时面临根本性的效率困境：自注意力机制的计算复杂度随序列长度呈二次增长，导致完整帧序列的处理成本极高。与此同时，视频帧间存在大量时间冗余，密集解码全部 RGB 帧不仅浪费计算资源，更限制了模型对长程时间依赖的建模能力。

问题的实质在于：**现有方法在“密集时间覆盖”与“计算可行性”之间难以兼顾**。均匀采样虽能降低帧数，却丢失了精细的时间动态；密集采样虽保留更多信息，却使自注意力计算不堪重负。这构成了长视频理解领域的核心瓶颈。

### 压缩视频表示的结构性机遇

现代视频编解码器（如 H.264/HEVC）天然提供了一种优雅的解决方案。压缩视频流将每段视频组织为图像组（Group of Pictures, GOP），每个 GOP 包含一个完整编码的 I 帧（关键帧）和若干仅记录运动信息的 P/B 帧。具体而言，P/B 帧中的块级运动向量定义为当前块与参考帧中最相似块之间的位移：

$$\mathbf{m}^{(k,t)}(u,v) = \mathbf{P}^{(k',t')}(u',v') - \mathbf{P}^{(k,t)}(u,v)$$

这一编解码器结构实现了外观信息与运动描述符的天然分离：I 帧承载空间外观，运动向量编码时间动态。更重要的是，运动向量可直接从压缩码流中提取，无需完整解码所有帧，从而以极低成本获得密集的时间运动线索。

### 从块级运动到精细化表示的技术缺口

尽管压缩域运动向量具备高效优势，但直接使用存在两个关键缺陷：其一，编解码器产生的运动向量本质上是面向压缩效率优化的块级匹配结果，包含大量噪声且空间粒度粗糙；其二，这些运动向量的保真度远低于密集光流，难以直接为 MLLM 提供足够精细的运动信息。

现有工作或完全依赖 RGB 帧序列（如 **LLaVA-Video**、**LLaVA-OneVision**、**Qwen2-VL** 等），或尝试引入压缩域信息但未解决运动质量与长程建模的双重挑战。这形成了一个明确的技术缺口：**如何在不牺牲效率的前提下，将粗糙的块级运动向量转化为可媲美光流的精细化运动表示，并实现线性复杂度的长程时间建模？**

### 本文动机

基于上述分析，本文提出 ReMoRa——一种直接在压缩视频表示上运行的多模态大语言模型。其核心动机在于：利用编解码器天然的关键帧-运动分离结构，通过精细化运动表示模块（RMR）弥合块级运动向量与密集光流之间的保真度鸿沟，并借助层次化运动状态空间模块（HMSS）以线性时间复杂度实现跨 GOP 的长程依赖建模，从而在密集时间覆盖与计算效率之间取得突破性平衡。



## 核心方法与创新机理

ReMoRa 的核心创新在于将长视频理解从“全解码 RGB 帧序列”范式迁移至“压缩域表示”范式，通过三个紧密耦合的 changed slots 系统性地解决了冗余计算、二次复杂度时间建模和粗糙运动信号三大瓶颈。

### 1. 输入表示：从 RGB 帧序列到压缩 GOP

传统视频 MLLM（如 **LLaVA-Video** (Zhang et al., arXiv 2024)、**Qwen2-VL** 等）依赖均匀采样 RGB 帧序列作为输入。这一策略存在根本性矛盾：密集采样带来二次增长的自注意力代价，稀疏采样则丢失精细时序动态。ReMoRa 直接利用压缩视频的编解码器结构，将视频组织为 GOP（Group of Pictures）序列，每个 GOP 包含一个 I 帧（完整关键帧）和若干 P/B 帧的运动向量场：

$$\operatorname{GOP}^{(k)} = \left( \mathbf{V}^{(k,0)}, \mathbf{m}^{(k,1)}, \dots, \mathbf{m}^{(k,T_g)} \right)$$

其中运动向量定义为当前帧块与参考帧中最相似块的位移：

$$\mathbf{m}^{(k,t)}(u,v) = \mathbf{P}^{(k',t')}(u',v') - \mathbf{P}^{(k,t)}(u,v)$$

这一设计的因果机制在于：编解码器天然将外观信息（I 帧）与运动描述符分离，使得模型仅需处理稀疏关键帧和轻量运动向量，即可覆盖密集时间跨度，从源头消除 RGB 帧冗余。

### 2. 运动特征质量：从块级噪声到密集光流保真度

编解码器直接输出的运动向量是块级、噪声化的粗糙信号，若直接使用将严重限制时序理解的精度。ReMoRa 引入 **Refined Motion Representation (RMR) 模块**，通过光流预训练将块级运动向量去噪并精化为密集运动表示，使其逼近密集光流的保真度。消融实验（Table 4）提供了决定性证据：去除光流预训练或整个 RMR 模块均导致性能持续下降，证实 RMR 模块是运动向量鲁棒视频理解的必要条件。

### 3. 时间建模复杂度：从二次自注意力到线性状态空间

传统 Transformer 的自注意力复杂度随序列长度二次增长，是长视频建模的核心计算瓶颈。ReMoRa 提出 **Hierarchical Motion State Space (HMSS) 模块**，基于 Mamba 状态空间模型实现线性复杂度的时间推理。HMSS 将时间建模显式分解为两个阶段：

- **GOP 内融合**：将 I 帧 patch 嵌入与运动嵌入拼接后送入双向 Mamba，实现外观与运动的局部混合，并选取前 $N_p$ 个 token 作为该 GOP 的运动感知摘要：

$$Z_{\mathrm{I}}^{(k)} = \mathrm{SSM}_{\mathrm{local}}\left(Z^{(k)}\right)_{[1:N_p]}$$

- **GOP 间长程建模**：将所有 GOP 摘要向量输入全局双向 Mamba，捕获跨 GOP 的长程依赖：

$$\pmb{H} = \mathrm{SSM}_{\mathrm{global}}\left([\pmb{Z}_1^{(0)}; \pmb{Z}_1^{(1)}; \dots; \pmb{Z}_1^{(K-1)}]\right)$$

消融实验（Table 5）表明，HMSS 的结构化时间聚合显著优于简单交叉注意力或相加融合，验证了编解码器感知的分层时序建模对 GOP 整合的关键作用。

### 创新点间的因果耦合

三个 changed slots 并非独立改进，而是形成因果链条：压缩 GOP 输入（slot 1）使得线性复杂度的时间建模成为可能（slot 2），而块级运动向量的低质量又迫使引入 RMR 精化模块（slot 3）以保证运动信号的保真度。这一耦合使得 ReMoRa 在 LongVideoBench（60.8）、NExT-QA（84.2）、MLVU（72.1）三项长视频基准上均取得最高得分，五基准平均分 69.8 超越所有基线模型。



ReMoRa 的核心设计理念是将长视频理解从高冗余的 RGB 像素空间迁移到天然解耦的压缩域。传统视频 MLLM 对完整 RGB 帧序列进行均匀采样，其自注意力复杂度随帧数呈二次增长，导致长视频建模的计算代价极高且信息高度冗余。ReMoRa 直接利用压缩视频码流的结构化特性，将视频表示为一组 **GOP (Group of Pictures)** 的序列，每个 GOP 由一个 I 帧（关键帧）和若干 P/B 帧的运动向量场构成。I 帧负责提供稀疏但完整的外观信息，运动向量则以极低的存储代价承载帧间的密集时间动态。这种输入表示从根本上改变了信息流：外观与运动在输入端即被分离，使得模型可以分别对二者进行高效编码与融合。

整个 pipeline 由四个核心模块串联构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of ReMoRa: The model operates directly in the compressed video representation for long-video understanding. (a) It consists of an image encoder, the Refined Motion Representation (RMR) module, the Hierarchical Motion State Space (HMSS) Module, and a pretrained LLM. Each clip is decomposed into group of pictures (GOPs) with a single I-frame and several P/B frames represented by motion vectors. The image encoder (Enc.) extracts patch embeddings from I-frames, while the RMR module converts coarse motion vectors into dense, high-fidelity representations. (b) The HMSS module fuses the refined motions and appearance features within each GOP and models long-range dependencies across G...*

1. **Image Encoder**：采用 SigLIP ViT-SO 作为图像编码器，对每个 GOP 的 I 帧提取 patch 嵌入 $\mathbf{E}_{\mathrm{I}}^{(k)}$，为后续模块提供空间外观特征。
2. **Refined Motion Representation (RMR) Module**：接收 P/B 帧的原始块级运动向量 $\mathbf{m}^{(k,t)}$，通过去噪与稠密化将其精炼为高质量的密集运动表示 $\mathbf{E}_{\mathrm{M}}^{(k,t)}$，使其保真度逼近稠密光流。该模块是连接“低成本粗糙运动信号”与“精细时空理解”的关键桥梁。
3. **Hierarchical Motion State Space (HMSS) Module**：这是 ReMoRa 的时序建模核心。它在两个粒度上运行：(a) **GOP 内融合**——将 I 帧 patch 嵌入与同一 GOP 内所有运动嵌入拼接为序列 $\mathbf{Z}^{(k)}$，经双向 Mamba 块混合外观与运动信息，并取前 $N_p$ 个 token 作为该 GOP 的运动感知 I 帧特征 $\mathbf{Z}_{\mathrm{I}}^{(k)}$；(b) **GOP 间聚合**——将所有 GOP 的摘要向量 $\mathbf{Z}_{\mathrm{I}}^{(k)}$ 串联后送入另一个双向 Mamba，完成跨 GOP 的长程依赖建模，输出最终视频特征 $\mathbf{H}$。由于 Mamba 的状态空间模型具有序列长度的线性复杂度，该模块避免了传统自注意力的二次瓶颈。
4. **Pretrained LLM**：以 Qwen2 为基础语言模型，接收 HMSS 输出的视频特征 $\mathbf{H}$ 与文本指令 $x_{\mathrm{txt}}$，通过自回归方式逐 token 预测答案 $\hat{y}_n$。

整个框架的信息流可概括为：**压缩视频 → 外观/运动解耦编码 → 运动精炼 → 分层时序融合 → 多模态文本生成**。这种设计使得 ReMoRa 在保持密集时间覆盖（64 个 I 帧及其关联运动向量）的同时，显著降低了计算开销，实现了长视频理解的线性复杂度推理。





### 压缩视频表示与输入构建

ReMoRa 的核心创新在于直接以压缩视频流作为输入，而非解码后的 RGB 帧序列。视频被组织为 $K$ 个图像组（Group of Pictures, GOP）的列表，每个 GOP 包含一个 I 帧（关键帧）和若干 P/B 帧的运动向量场：

$$
\operatorname{GOP}^{(k)} = \left( \mathbf{V}^{(k,0)}, \mathbf{m}^{(k,1)}, \dots, \mathbf{m}^{(k,T_g)} \right)
$$

其中 $\mathbf{V}^{(k,0)}$ 为第 $k$ 个 GOP 的 I 帧，$\mathbf{m}^{(k,t)}$ 为第 $t$ 个 P/B 帧的运动向量场。运动向量定义为当前帧块与参考帧中最相似块的位移：

$$
\mathbf{m}^{(k,t)}(u,v) = \mathbf{P}^{(k',t')}(u',v') - \mathbf{P}^{(k,t)}(u,v)
$$

这一表示天然分离了外观信息（I 帧）与时间动态（运动向量），避免了全解码 RGB 帧带来的冗余计算。

### 精细化运动表示模块（RMR）

原始编解码器提取的运动向量是块级的、含噪声的粗粒度表示。RMR 模块的核心作用是将这些粗糙的运动向量精化为密集的、高保真度的运动表示，使其逼近密集光流的质量。该模块通过光流预训练获得运动先验，从而在保持计算效率的同时提升运动信号的精细度。

对于第 $k$ 个 GOP，图像编码器（SigLIP ViT-SO）提取 I 帧的 patch 嵌入 $\mathbf{E}_{\mathrm{I}}^{(k)}$，RMR 模块则将各 P/B 帧的运动向量转换为运动嵌入 $\mathbf{E}_{\mathrm{M}}^{(k,t)}$。GOP 内的完整输入序列由 I 帧嵌入与所有运动嵌入拼接而成：

$$
\mathbf{Z}^{(k)} = \left[ \mathbf{E}_{\mathrm{I}}^{(k)} ; \mathbf{E}_{\mathrm{M}}^{(k,1)} ; \dots ; \mathbf{E}_{\mathrm{M}}^{(k,T_g-1)} \right]
$$

### 层次化运动状态空间模块（HMSS）

HMSS 模块将时间推理显式分解为两个阶段，以匹配视频编解码器的自然结构，并通过状态空间模型（SSM）实现序列长度的线性复杂度。

**第一阶段：GOP 内局部融合。** 将式 (4) 得到的完整 token 序列 $\mathbf{Z}^{(k)}$ 送入双向 Mamba 块，高效混合 I 帧外观嵌入与对应的运动向量嵌入。从双向 Mamba 输出中选取前 $N_p$ 个 token 作为该 GOP 的运动感知 I 帧特征：

$$
\mathbf{Z}_{\mathrm{I}}^{(k)} = \mathrm{SSM}_{\mathrm{local}}\left(\mathbf{Z}^{(k)}\right)_{[1:N_p]}
$$

**第二阶段：GOP 间全局聚合。** 对所有 GOP 的摘要向量取均值得到 $\mathbf{Z}_1^{(k)}$，将其拼接后送入另一个双向 Mamba 块，实现跨 GOP 的长程依赖建模：

$$
\mathbf{H} = \mathrm{SSM}_{\mathrm{global}}\left([\mathbf{Z}_1^{(0)}; \mathbf{Z}_1^{(1)}; \dots; \mathbf{Z}_1^{(K-1)}]\right)
$$

最终视频特征 $\mathbf{H}$ 与文本指令 $x_{\mathrm{txt}}$ 对齐后送入预训练 LLM（Qwen2），以自回归方式生成回答：

$$
\hat{y}_n = \arg\max_{\tilde{y}\in\mathcal{V}} p_\theta\left(\tilde{y} \mid \mathcal{H}, x_{\mathrm{txt}}, \hat{y}_{<n}\right)
$$

模型使用标准的交叉熵损失进行训练。

### 关键设计要点

1. **线性复杂度时间建模**：HMSS 基于 Mamba 的状态空间模型，避免了传统自注意力的二次复杂度，使长视频处理在计算上可行。
2. **编解码器结构感知**：GOP 内融合与 GOP 间聚合的两阶段设计与视频压缩结构对齐，消融实验表明该结构化建模显著优于简单的交叉注意力或相加融合（Table 5）。
3. **运动质量保障**：RMR 模块的光流预训练对运动向量的去噪和精细化至关重要——去除该预训练或整个 RMR 模块均导致性能持续下降（Table 4）。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/007_Table_4.jpg]]
*Table 4: Ablation study on the Refined Motion Representation (RMR) module. Removing optical-flow–based pretraining (f) or the RMR module (g) consistently degrades performance, showing that the RMR module with optical-flow pretraining is important for robust video understanding when using motion vectors*

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/008_Table_5.jpg]]
*Table 5: Ablation study on the GOP aggregation strategy. Model (a) outperforms variants that rely on simple cross-attention (h) or naive additive fusion (i) on both benchmarks, highlighting the importance of structured temporal modeling for GOP integration*

### 补充图表

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/013_Figure_5.jpg]]
*Figure 5: Example of scene-aware video preprocessing. Frames 0 and 18 are scene-adaptive I-frames used as keyframes, and the remaining frames are P/B-frames with overlaid codec motion vectors*



## 实验与关键发现

### 主实验结果

ReMoRa 在五个长视频理解基准上进行了系统评估，其核心结果汇总于 Table 1。模型在 **LongVideoBench**（60.8）、**NExT-QA**（84.2）和 **MLVU**（72.1）三个基准上均取得最高得分，分别超出次优模型 1.3、1.0 和 1.3 分。五项基准的平均分为 **69.8**，超过此前最强基线模型 0.9 分。在 VideoMME 和 Perception Test 上，ReMoRa 也保持了高度竞争力。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of recent video MLLMs across multiple benchmarks. ReMoRa achieved the best performance on LongVideoBench, NExT-QA, and MLVU, and obtains the highest overall average score of 69.8, while remaining highly competitive on VideoMME and Perception Test. Bold indicates the best performance, and underline indicates the second best in each column*

在开放式视频问答任务（Table 2）中，ReMoRa 在 **ActivityNet-QA** 上以准确率 60.5、得分 3.7 大幅领先，较前最佳模型分别高出 8.4 和 0.2 分；在 MSVD-QA 上同样取得强竞争力得分。

与强基线模型的对比揭示了一个关键趋势：ReMoRa 仅使用 64 个 I 帧和压缩运动向量，却能在多数长视频基准上超越使用密集 RGB 帧的 **LLaVA-Video**（Zhang et al., arXiv 2024）和 **Qwen2-VL** 等模型。这表明压缩域运动表示在长程时间理解中的信息密度优势——稀疏关键帧配合精细化运动信号，比冗余 RGB 帧序列更高效地捕获了时空动态。

### 定性分析

Figure 3 展示了 ReMoRa 与 LLaVA-Video 在 NExT-QA 上的定性对比。在两个示例中，ReMoRa 正确回答了涉及细粒度、时间上下文化的人类动作和物体运动问题，而 LLaVA-Video 失败。这直观体现了 RMR 模块精化后的运动表示对精细动作理解的贡献——模型能够追踪时间维度上的细微动态变化，而非仅依赖静态外观线索。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison between ReMoRa and LLaVA-Video on NExT-QA. In both examples, ReMoRa correctly answers questions about fine-grained, temporally contextualized human actions and object motions, while LLaVA-Video fails, highlighting ReMoRa’s superior use of motion cues for fine-grained action understanding*

Figure 4 进一步展示了 LongVideoBench 上的定性比较。ReMoRa 成功整合了空间细节与长程时间理解，例如追踪场景和物体在时间中的变化模式，并一致地识别活动参与者，而基线模型在这些需要跨时间推理的任务上出现错误。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/012_Figure_4.jpg]]
*Figure 4: Further qualitative comparison between ReMoRa and LLaVA-Video on LongVideoBench. In both examples, ReMoRa correctly answers questions that require integrating spatial details with long-range temporal understanding, such as tracking how the scene and objects change over time and consistently identifying the person involved in the activity, while the baseline model fails*

### 消融研究

#### 采样策略与帧选择

Table 3 报告了采样和帧选择策略的消融结果。使用 **CVR 感知的 64 个 I 帧选择**（配置 a）取得最佳性能。减少 I 帧数量导致性能下降，尤其在 VideoMME 上退化明显，表明充分的时间覆盖对长视频理解至关重要。简单均匀采样（配置 d）得分低于 CVR 感知选择，验证了压缩域场景自适应采样策略的有效性——编解码器结构天然标识了信息量高的关键帧位置，利用这一先验比均匀采样更有效。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/006_Table_3.jpg]]
*Table 3: Ablation study on sampling and frame selection strategies. Using our Compressed Video Representation (CVR)-aware selection of 64 I-frames (a) achieved the best performance. Reducing the number of I-frames degrades results, especially on VideoMME, indicating the importance of sufficient temporal coverage. Simple uniform sampling (d) leads to lower scores, showing that our method is more effective than uniform sampling for long-video understanding*

#### 精细化运动表示模块

Table 4 针对 RMR 模块进行了消融。去除基于光流的预训练（配置 f）或完全移除 RMR 模块（配置 g）均导致性能持续下降。这一结果确立了 RMR 模块的因果作用：原始块级运动向量噪声大、分辨率低，直接使用会损害时间理解；经过光流预训练的 RMR 模块能将其精化为接近密集光流保真度的表示，从而在保持计算效率的同时提升运动质量。

#### GOP 聚合策略

Table 5 比较了不同的 GOP 聚合策略。基于 HMSS 的结构化时间建模（配置 a）显著优于简单交叉注意力（配置 h）和朴素相加融合（配置 i）。这验证了 HMSS 模块设计的核心动机——编解码器天然形成的 GOP 结构蕴含了层次化时间先验，利用 Mamba 状态空间模型在 GOP 内融合运动与外观、在 GOP 间建模长程依赖，比扁平化的注意力或融合操作更能捕获结构化时间关系。

### 计算效率

Table 6 报告了吞吐量和峰值 GPU 内存使用。ReMoRa 的每秒样本数和每秒 token 数与 **BIMBA** 相当，内存占用也处于同一水平；相比 **LLaVA-Video**，峰值内存使用减少了一半以上。这一效率优势源于两个设计选择：压缩域输入避免了完整 RGB 帧解码，以及基于 Mamba 的状态空间模型将时间建模复杂度从自注意力的二次级降为线性级。

![[assets/figures/papers/paper_list_l981_https_arxiv_org_abs_2602_16412/figures/009_Table_6.jpg]]
*Table 6: Throughput and peak GPU memory usage for different video MLLMs. ReMoRa achieves comparable samples per second and tokens per second throughput to BIMBA while matching its memory footprint, and it reduces peak memory usage by more than half compared with LLaVA-Video. Note that max memory is in GB*

### 错误模式分析

Table 8 基于 NExT-QA 上 ReMoRa 失败而 LLaVA-Video 成功的 50 个随机采样案例，对 67 个标注错误实例进行了分类。主要失败模式包括：

- **空间理解错误**：对物体空间关系、定位和存在性的推理存在偏差，表明在结合稀疏运动信息时空间定位精度仍有不足。
- **时间理解错误**：在长时间跨度和多场景条件下，对事件顺序、活动阶段和情境演变的跟踪可能出现混淆。
- **运动理解错误**：对细微手势、小物体操作等极细粒度动作的识别能力有限，说明当前精细化运动信号在极端精细动态上仍不够充分。
- **标注错误**：部分基准样本存在不正确或不一致的标注，导致合理预测被计入错误。

这些失败模式指向了当前方法的边界：压缩域运动向量虽然高效，但在需要精确空间定位和极细粒度运动辨识的场景中，信息量仍不及全解码 RGB 帧。



## 定位与知识库关联

### 1. 方法谱系：从密集 RGB 帧到压缩域运动表征

ReMoRa 的核心技术路线是将视频理解从“密集 RGB 帧序列”迁移至“压缩视频域”，其方法谱系可从三个维度定位：

**（1）输入表示：压缩域视频理解**

传统视频多模态大语言模型（Video MLLM）普遍采用均匀采样 RGB 帧作为输入，如 **LLaVA-Video**（Zhang et al., arXiv 2024）、**LLaVA-OneVision**、**Qwen2-VL** 等强基线均遵循此范式。这一范式在长视频场景下面临根本性瓶颈：完整解码 RGB 帧序列的计算代价高昂，且自注意力复杂度随序列长度二次增长，密集帧间存在高度冗余。

ReMoRa 直接处理压缩视频流，利用编解码器天然分离的关键帧（I 帧）与运动描述符（P/B 帧的运动向量），仅保留稀疏 I 帧用于外观建模，将时间动态编码为轻量运动表示。这一设计在输入层面实现了“密集时间覆盖”与“低计算冗余”的兼顾，与 **BIMBA** 等同样探索压缩域建模的工作形成对比——BIMBA 虽也关注压缩视频，但 ReMoRa 在运动特征质量和时间建模效率上进一步突破。

**（2）运动特征质量：从块级运动向量到密集运动表示**

编解码器提供的运动向量是块级、有噪且粗糙的。直接使用这类运动信息会限制对细粒度时空动态的感知能力。ReMoRa 引入 **Refined Motion Representation (RMR) 模块**，通过光流预训练将块级运动向量去噪并细化为密集运动表示，使其保真度逼近密集光流。这一设计填补了“压缩域运动信息”与“高质量运动理解”之间的鸿沟，是 ReMoRa 相对于直接使用原始运动向量的方法的本质提升。

消融实验（Table 4）提供了决定性证据：去除光流预训练或整个 RMR 模块会导致性能持续下降，证实 RMR 模块对运动质量至关重要。

**（3）时间建模复杂度：从二次自注意力到线性状态空间模型**

传统 Video MLLM 依赖自注意力机制进行跨帧时间建模，其二次复杂度在长视频场景下成为严重瓶颈。ReMoRa 提出 **Hierarchical Motion State Space (HMSS) 模块**，基于 Mamba 状态空间模型实现线性复杂度的时间推理。HMSS 将时间建模分解为两个阶段：先在每个 GOP 内部融合运动与外观特征（局部 SSM），再跨 GOP 进行长程依赖建模（全局 SSM）。这一设计充分利用了编解码器产生的 GOP 结构，在保持线性复杂度的同时实现了结构化时间建模。

消融实验（Table 5）表明，HMSS 聚合显著优于简单的交叉注意力或相加融合，验证了结构化时间建模对 GOP 整合的关键作用。

### 2. 知识库定位：适用边界与局限

**适用场景**

ReMoRa 在以下场景展现出明确优势：
- **长视频理解**：在 LongVideoBench、NExT-QA、MLVU 上取得最高得分（60.8、84.2、72.1），平均分 69.8 超过所有基线，证明其在长时程视频问答中的领先性。
- **开放域视频问答**：在 ActivityNet-QA 上获得最高 Accuracy 和 Score（60.5 / 3.7），显著超越次优模型（+8.4 / +0.2）。
- **计算效率敏感场景**：ReMoRa 的峰值 GPU 内存使用较 LLaVA-Video 降低一半以上，吞吐量与 BIMBA 相当（Table 6），适合资源受限环境。

**已知局限与失败模式**

基于 67 个标注错误实例的分析（Table 8），ReMoRa 的失败模式可归纳为四类：

1. **空间理解错误**：对物体空间关系、定位和存在性的推理存在错误。这表明在结合稀疏运动信息时，空间定位的精确性仍有不足。
2. **时间理解错误**：在长时间跨度和多场景下，对事件顺序、活动阶段和情境演变的跟踪可能出现混淆。
3. **运动理解错误**：对细微手势、小物体操作等细粒度动作的识别能力有限，说明精细化运动信号在极精细动态上仍不够充分。
4. **标注错误**：部分基准样本存在不正确或不一致的标注，导致合理预测被计入错误。

### 3. 开放问题

ReMoRa 揭示了压缩域视频理解的潜力，但也留下了若干待解决问题：

1. **空间定位增强**：如何进一步增强空间定位能力，使其在稀疏运动信息下保持精确？可能的路径包括引入残差信息或显式空间注意力机制。
2. **时间上下文一致性**：如何在关键帧和编解码器运动线索之间维持一致的时间上下文？当前 GOP 级别的聚合可能在跨场景切换时丢失细粒度时序关联。
3. **运动信号保真度边界**：如何使精细化运动信号对更细粒度的动态（如微表情、小物体交互）更具信息量？RMR 模块的光流逼近能力是否存在理论上限？
4. **残差信息利用**：能否结合编解码器残差信息进一步提升压缩域运动表示的保真度？当前方法仅利用运动向量，而忽略了预测残差中可能蕴含的补充信息。

**手动验证提示**：上述局限和开放问题的部分论述基于论文中有限的错误分析样本（67 例），其统计显著性和泛化性需进一步验证。具体基线工作的完整元数据（如 BIMBA 的作者/会议/年份）在提供的分析材料中缺失，建议查阅原始论文补充。



## 原文 PDF

![[paperPDFs/CVPR_2026/ReMoRa_Multimodal_Large_Language_Model_based_on_Refined_Motion_Representation_for_Long_Video_Understanding.pdf]]
