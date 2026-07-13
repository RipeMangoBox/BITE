---
title: "StoryDiffusion: Consistent Self-Attention for Long-Range Image and Video Generation"
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/StoryDiffusion.pdf
project_link: https://StoryDiffusion.github.io
code_link: null
aliases:
- StoryDiffusion
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 修改自注意力计算中的键（key）和值（value）的来源——从同一批次内的其他图像中随机采样 token 并拼接到当前图像的键值对中，从而在不训练额外参数的情况下建立跨图像的特征交互，控制生成内容的一致性。
primary_logic: 利用跨图像的自注意力（Consistent Self-Attention）以训练自由的方式共享视觉特征，可以在保持高文本可控性的同时实现主体一致的多图像生成；进一步通过在图像语义空间（而非潜空间）中预测过渡帧的运动，能够处理更大的动作变化并获得更稳定的长视频生成。
claims:
- Consistent Self-Attention 无需训练即可显著提升生成图像间的文本相似度和人物相似度。
- 所提方法在过渡视频生成中全面优于 SOTA 方法 SEINE 和 SparseCtrl，尤其在 LPIPS 和 CLIPSIM 指标上。
- 用户研究中，72.8% 的受试者在主体一致图像生成上更偏好 StoryDiffusion，82% 在过渡视频生成上更偏好 StoryDiffusion。
- 主体一致图像生成 上 Text-Image Similarity (CLIP) = 0.6586
---

# StoryDiffusion: Consistent Self-Attention for Long-Range Image and Video Generation

> [!tip] 核心洞察
> 利用跨图像的自注意力（Consistent Self-Attention）以训练自由的方式共享视觉特征，可以在保持高文本可控性的同时实现主体一致的多图像生成；进一步通过在图像语义空间（而非潜空间）中预测过渡帧的运动，能够处理更大的动作变化并获得更稳定的长视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | StoryDiffusion：面向长程图像与视频生成的一致性自注意力 |
| 英文题名 | StoryDiffusion: Consistent Self-Attention for Long-Range Image and Video Generation |
| 会议/期刊 | NEURIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2405.01434) · [Project](https://StoryDiffusion.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | StoryDiffusion |
| Dataset |  |

> [!tip] 效果简介
> - 主体一致图像生成 上，Text-Image Similarity (CLIP) 0.6586 vs − (优于 IP-Adapter/PhotoMaker 等) (−)；Character Similarity 0.8950 vs − (优于 IP-Adapter/PhotoMaker 等) (−)。
> - 过渡视频生成 上，LPIPS-first 0.3794 vs − (优于 SEINE/SparseCtrl) (−)；CLIPSIM-first 0.9606 vs − (优于 SEINE/SparseCtrl) (−)。
> - 用户研究 上，用户偏好（图像一致性） 72.8% vs − (−)。

## 概要

**StoryDiffusion** 面向一个长程生成中的核心瓶颈：预训练扩散模型在生成多幅图像或视频帧时，无法在整个序列中维持人物身份、服装和场景的一致性，尤其当内容涉及复杂细节或大幅度运动时。为解决该问题，本文提出两项关键机制：

- **Consistent Self-Attention（一致性自注意力）**：一种训练自由、即插即用的自注意力修改方案。其核心思路是修改自注意力计算中键（key）和值（value）的来源——从同一批次内的其他图像中随机采样 token 并拼接到当前图像的键值对中，从而在不训练额外参数的情况下建立跨图像的特征交互，控制生成内容的一致性。
- **Semantic Motion Predictor（语义运动预测器）**：将过渡帧的运动预测从图像潜空间迁移到图像语义空间（使用预训练 CLIP 图像编码器），通过 Transformer 预测中间帧的语义嵌入，再将其作为控制信号注入视频扩散模型的交叉注意力中，从而处理更大的动作变化并获得更稳定的长视频生成。

该方法的核心洞察在于：利用跨图像的自注意力以训练自由的方式共享视觉特征，可以在保持高文本可控性的同时实现主体一致的多图像生成；而将运动建模上移到语义空间，则使过渡视频生成对大运动具有更强的鲁棒性。

在主体一致图像生成任务上，StoryDiffusion 在 Text-Image Similarity（0.6586）和 Character Similarity（0.8950）指标上优于 IP-Adapter、PhotoMaker、InstantID 等基线方法（Table 1）。在过渡视频生成任务上，该方法在 LPIPS 和 CLIPSIM 指标上全面超越 SEINE 和 SparseCtrl（Table 2）。用户研究中，72.8% 的受试者在主体一致性图像生成上更偏好 StoryDiffusion，82% 在过渡视频生成上更偏好 StoryDiffusion（Table 3）。

方法存在已知局限：服装细节（如领带）可能出现不一致，需要更详细的提示词来维持；尽管可通过滑动窗口生成长视频，但缺乏全局信息交换机制，在极长视频场景下仍非完美。



扩散模型在文本到图像生成领域的突破性进展，使得从自然语言描述自动合成高质量视觉内容成为现实。然而，当任务从单幅图像扩展到多幅图像序列或视频时，一个核心瓶颈浮现：**预训练扩散模型无法在整个序列中维持人物身份、服装和场景的一致性**，尤其当内容涉及复杂细节或大幅度运动时。这一瓶颈直接阻碍了扩散模型在漫画创作、故事可视化、长视频生成等实际应用中的落地。

现有工作试图从两个方向缓解该问题。一类方法如 **IP-Adapter**（Ye et al., 2023）、**PhotoMaker**（Li et al., 2023a）和 **InstantID**（Wang et al., 2024）通过引入额外的身份编码器或适配模块，将参考图像的主体特征注入生成过程。这些方法通常需要针对特定主体进行训练或微调，且在处理多主体交互或大幅度姿态变化时，一致性仍会退化。另一类方法如 **SEINE**（Chen et al., 2023）和 **SparseCtrl**（Guo et al., 2023）专注于视频帧间的过渡生成，但它们在图像潜空间中直接预测中间帧的运动，当首尾帧之间的运动幅度较大时，生成的过渡帧容易出现内容断裂或伪影。

上述方法的共同局限在于：它们要么依赖额外的训练参数来绑定主体特征，要么在表达能力受限的潜空间中进行运动建模，缺乏一种**训练自由且能灵活插入预训练模型**的机制来建立跨图像的特征交互。StoryDiffusion 正是针对这一缺口，提出了两个互补的模块——Consistent Self-Attention 和 Semantic Motion Predictor——分别从跨图像注意力共享和语义空间运动预测两个维度，在不增加训练负担的前提下实现长程图像与视频的一致性生成。



## 核心方法与创新机理

StoryDiffusion 的核心创新在于两个相互衔接的模块，分别解决“主体一致图像生成”和“大运动过渡视频生成”两个瓶颈问题。两项创新均以**训练自由（training‑free）**为设计原则，无需微调预训练扩散模型即可即插即用。

### 创新一：Consistent Self‑Attention —— 跨图像特征共享的主体一致性注入

预训练文生图扩散模型的标准自注意力仅在**单张图像内部**独立计算，查询（query）、键（key）和值（value）均来自同一图像特征 $I_i$：

$$O_i = \mathrm{Attention}(Q_i, K_i, V_i)$$

当批量生成多幅图像时，这种隔离机制导致人物身份、服装和场景无法跨图像保持一致。StoryDiffusion 的解决方案是**修改自注意力中键和值的来源**：从同一批次的其他图像中随机采样 token，拼接到当前图像的键值对中，而查询向量保持不变。

具体而言，对于批次中的第 $i$ 张图像，首先从其余 $B-1$ 张图像的特征中随机采样 token：

$$S_i = \mathrm{RandSample}(I_1, I_2, ..., I_{i-1}, I_{i+1}, ..., I_{B-1}, I_B)$$

随后将采样 token $S_i$ 与当前图像特征 $I_i$ 拼接，形成新的键 $K_{Pi}$ 和值 $V_{Pi}$，计算 Consistent Self‑Attention：

$$O_i = \mathrm{Attention}(Q_i, K_{Pi}, V_{Pi})$$

这一设计的精妙之处在于：**查询 $Q_i$ 始终来自当前图像，保证生成内容仍忠实于当前提示词**；而键和值中混入其他图像的特征，使当前图像在去噪过程中能够“看到”批次内其他图像的视觉信息，从而在主体外观上自发趋同。该模块直接插入预训练 U‑Net 的自注意力位置，复用原始权重，完全无需训练（Section 3.1）。

> **与 baseline 的根本差异**：IP‑Adapter（Ye et al., 2023）、PhotoMaker（Li et al., 2023a）、InstantID（Wang et al., 2024）等方法依赖额外的图像编码器或身份嵌入，需要训练或微调来注入主体信息；而 Consistent Self‑Attention 仅通过改变自注意力计算中键值的拼接来源，在**不引入任何新参数**的前提下实现了跨图像一致性。

### 创新二：Semantic Motion Predictor —— 语义空间中的运动预测

在获得主体一致的图像序列后，StoryDiffusion 需要在首尾帧之间生成平滑的过渡视频。现有方法（如 SEINE，Chen et al., 2023；SparseCtrl，Guo et al., 2023）通常在**图像潜空间（latent space）**中直接预测中间帧，但在处理大幅度运动时容易产生伪影和不稳定。

StoryDiffusion 将运动预测从潜空间**提升到图像语义空间**。首先使用预训练 CLIP 图像编码器 $E$ 将首尾帧映射到语义向量：

$$K_s, K_e = E(F_s, F_e)$$

随后对 $K_s$ 和 $K_e$ 进行线性插值得到 $L$ 个中间向量，并通过 Transformer 块 $B$ 预测中间帧的语义嵌入：

$$P_1, P_2, ..., P_l = B(K_1, K_2, ..., K_L)$$

这些预测的语义嵌入 $P_i$ 作为控制信号，与文本嵌入 $T$ 拼接后注入视频扩散模型的交叉注意力中：

$$V_i = \mathrm{CrossAttention}(V_i, \mathrm{concat}(T, P_i), \mathrm{concat}(T, P_i))$$

> **与 baseline 的根本差异**：SEINE 和 SparseCtrl 在潜空间中操作，对大幅度运动的建模能力受限于潜空间的表达能力；而 Semantic Motion Predictor 利用 CLIP 语义空间强大的空间编码能力，将运动预测抽象为语义级别的过渡，再通过交叉注意力解码回像素空间，从而**稳定处理更大的动作变化**。

### 两项创新的协同关系

Consistent Self‑Attention 和 Semantic Motion Predictor 并非孤立模块，而是形成了一条完整的“一致图像 → 平滑视频”生成链路：前者保证多幅图像中主体的身份、服装和场景高度一致；后者在这些一致图像之间生成运动自然、过渡平滑的视频帧。两者共同构成了 StoryDiffusion 从文本故事到主体一致漫画再到长视频的端到端生成能力。



StoryDiffusion 的整体框架由两个解耦但协同的模块构成，分别对应**主体一致的图像序列生成**与**平滑过渡视频生成**两个阶段。其核心设计思想是：在不引入额外训练参数的条件下，通过修改预训练扩散模型中自注意力的键值来源来建立跨图像的特征交互，从而维持生成内容的主体一致性；在此基础上，将首尾帧映射到语义空间进行运动预测，以处理大幅度动作变化并生成连贯的视频过渡。

### 第一阶段：主体一致的图像序列生成

该阶段的输入是一段故事文本，输出是一组主体（人物身份、服装、场景）保持一致的多幅图像。

**处理流程**（参见 Figure 2）：

1. **文本切分**：将故事文本按语义切分为多个提示词（prompts），每个提示词对应故事中的一个情节帧。
2. **批次生成**：将所有提示词放入同一个批次，送入预训练的文生图扩散模型（如 Stable Diffusion XL 或 Stable Diffusion 1.5）进行并行生成。
3. **Consistent Self-Attention 介入**：在扩散 U-Net 的原始自注意力位置，插入 Consistent Self-Attention 模块。该模块保持查询向量（query）不变，但从同批次内其他图像的 token 中随机采样，并将采样得到的 token 拼接到当前图像的键（key）和值（value）中，形成新的键值对 $K_{P_i}, V_{P_i}$，再执行自注意力计算：

$$O_i = \mathrm{Attention}(Q_i, K_{P_i}, V_{P_i})$$

其中采样操作定义为：

$$S_i = \mathrm{RandSample}(I_1, I_2, ..., I_{i-1}, I_{i+1}, ..., I_{B-1}, I_B)$$

这一机制使得每幅图像在生成过程中都能“看到”批次内其他图像的特征，从而在去噪过程中共享视觉信息，实现主体一致性。

**关键特性**：Consistent Self-Attention 是训练自由的（training-free）和即插即用的（pluggable），直接复用原始自注意力的权重，无需任何微调。默认的 token 采样率设为 0.5，以在对扩散过程影响最小的前提下维持一致性（消融实验证实，采样率 0.3 不足以维持一致性，而 0.5 是合理的平衡点）。

### 第二阶段：平滑过渡视频生成

在第一阶段获得主体一致的图像序列后，第二阶段的目标是在相邻图像之间生成平滑的过渡视频。该阶段的输入是首尾两帧图像，输出是包含中间过渡帧的视频片段。

**处理流程**（参见 Figure 3）：

1. **语义空间编码**：使用预训练的 CLIP 图像编码器 $E$ 将首帧 $F_s$ 和尾帧 $F_e$ 映射到图像语义空间，得到语义向量 $K_s$ 和 $K_e$：

$$K_s, K_e = E(F_s, F_e)$$

选择语义空间而非潜空间（latent space）进行运动预测，是因为语义空间能更好地编码空间信息，从而处理更大的动作变化。

2. **过渡嵌入预测**：在 $K_s$ 和 $K_e$ 之间进行线性插值，得到一个长度为 $L$ 的语义向量序列 $K_1, K_2, ..., K_L$，然后通过一个 Transformer 块 $B$ 预测中间帧的语义嵌入：

$$P_1, P_2, ..., P_l = B(K_1, K_2, ..., K_L)$$

3. **交叉注意力解码**：将预测的语义嵌入 $P_i$ 与文本嵌入 $T$ 拼接，作为视频扩散模型交叉注意力层的键和值，引导每一帧的生成：

$$V_i = \mathrm{CrossAttention}(V_i, \mathrm{concat}(T, P_i), \mathrm{concat}(T, P_i))$$

视频扩散模型基于 Stable Diffusion 1.5 并加载预训练的时间模块，以 50 步 DDIM 采样、CFG 7.5 进行推理。训练 Semantic Motion Predictor 时，使用预测过渡视频 $O$ 与真实视频 $G$ 之间的均方误差作为损失函数：

$$Loss = \mathrm{MSE}(G, O)$$

### 模块关系与数据流总结

两个阶段的数据流是串行的：第一阶段利用 Consistent Self-Attention 生成主体一致的图像序列，第二阶段以这些图像作为条件帧，通过 Semantic Motion Predictor 在语义空间中预测运动轨迹，最终由视频扩散模型解码为连贯的过渡视频。两个模块可以独立使用，也可以端到端串联。Consistent Self-Attention 还可与外部 ID 控制模块（如 PhotoMaker）或姿态控制模块（如 ControlNet）结合，在引入额外条件的同时仍保持主体一致性。

### 补充图表

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/002_Figure_2.jpg]]
*Figure 2: The Pipeline of StoryDiffusion to generating subject-consistent images. To create subjectconsistent images to describe a story, we incorporate our Consistent Self-Attention into the pretrained text-to-image diffusion model. We split a story text into several prompts and generate images using these prompts in a batch. Consistent Self-Attention builds connections among multiple images in a batch for subject consistency*

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of our method for generating transition videos for obtaining subjectconsistent images, as described in Sec. 3.1. To effectively model the character’s large motions, we encode the conditional images into the image semantic space for encoding spatial information and predict the transition embeddings. These predicted embeddings are then decoded using the video generation model, with the embeddings serving as control signals in cross-attention to guide the generation of each frame*



StoryDiffusion 的核心由两个模块构成：**Consistent Self-Attention**（用于主体一致图像生成）和 **Semantic Motion Predictor**（用于过渡视频生成）。两者均以训练自由（training-free）或轻量训练的方式运作，无需对预训练扩散模型进行全量微调。

### 3.1 Consistent Self-Attention

**设计动机**：标准扩散模型的自注意力仅在单张图像的特征 $I_i$ 内部计算，不同图像之间缺乏信息交互，导致批量生成时人物身份、服装等属性漂移。

**核心修改**：改变自注意力计算中键（Key）和值（Value）的来源。具体而言，对于批次中的第 $i$ 张图像，从同批次的其他图像中随机采样 token，与当前图像的 token 拼接，形成新的键值对，而查询（Query）向量保持不变。

**公式推导**：

原始自注意力定义为：

$$O_i = \mathrm{Attention}(Q_i, K_i, V_i)$$

其中 $Q_i, K_i, V_i$ 均由单张图像特征 $I_i$ 线性投影得到。

为建立跨图像交互，首先从批次内其他图像中随机采样 token：

$$S_i = \mathrm{RandSample}(I_1, I_2, ..., I_{i-1}, I_{i+1}, ..., I_{B-1}, I_B)$$

将采样 token $S_i$ 与当前图像 token $I_i$ 拼接，形成新的 token 集合 $P_i$，并据此计算新的键 $K_{P_i}$ 和值 $V_{P_i}$，而查询 $Q_i$ 保持原始值：

$$O_i = \mathrm{Attention}(Q_i, K_{P_i}, V_{P_i})$$

**变量含义**：
- $I_i$：第 $i$ 张图像在 U-Net 某层的特征图（token 序列）
- $B$：批次大小
- $S_i$：从除 $I_i$ 外的其他图像中随机采样的 token 子集
- $P_i$：$I_i$ 与 $S_i$ 拼接后的 token 集合
- $Q_i, K_{P_i}, V_{P_i}$：分别由 $I_i$ 和 $P_i$ 经线性投影得到的查询、键、值矩阵
- $O_i$：Consistent Self-Attention 的输出

**实现要点**：
- 该模块直接插入预训练文生图 U-Net 的原始自注意力位置，**复用原始自注意力权重**，无需任何训练（training-free）
- 采样策略采用**分块采样**（tiled sampling），以降低计算开销
- 默认采样率设为 **0.5**，在维持一致性的同时对扩散过程的干扰最小（消融实验证实采样率 0.3 无法维持主体一致性）

### 3.2 Semantic Motion Predictor

**设计动机**：在获得主体一致的图像序列后，需生成相邻帧之间的平滑过渡视频。直接在图像潜空间（latent space）预测中间帧难以处理大幅度运动。本模块将运动预测提升至**图像语义空间**，以编码更丰富的空间信息。

**公式推导**：

首先，利用预训练 CLIP 图像编码器 $E$ 将首帧 $F_s$ 和尾帧 $F_e$ 映射到语义空间：

$$K_s, K_e = E(F_s, F_e)$$

对 $K_s$ 和 $K_e$ 进行线性插值，得到长度为 $L$ 的序列 $K_1, K_2, ..., K_L$，再由 Transformer 块 $B$ 预测中间帧的语义嵌入：

$$P_1, P_2, ..., P_l = B(K_1, K_2, ..., K_L)$$

预测的语义嵌入 $P_i$ 作为控制信号，与文本嵌入 $T$ 拼接后注入视频扩散模型的交叉注意力中，引导每一帧的生成：

$$V_i = \mathrm{CrossAttention}(V_i, \mathrm{concat}(T, P_i), \mathrm{concat}(T, P_i))$$

训练 Semantic Motion Predictor 时，使用预测过渡视频 $O$ 与真实视频 $G$ 之间的均方误差（MSE）作为损失函数：

$$Loss = \mathrm{MSE}(G, O)$$

**变量含义**：
- $F_s, F_e$：首帧和尾帧的 RGB 图像
- $E$：预训练 CLIP 图像编码器
- $K_s, K_e$：首尾帧在语义空间的嵌入向量
- $L$：线性插值后的序列长度
- $B$：Transformer 块，用于从插值序列预测过渡嵌入
- $P_i$：第 $i$ 个预测的中间帧语义嵌入
- $T$：文本提示的嵌入
- $V_i$：视频扩散模型第 $i$ 帧的特征
- $O, G$：预测视频和真实视频

**设计优势**：在语义空间而非潜空间预测运动，使模型能处理更大的动作幅度，同时 CLIP 编码器提供的丰富语义先验有助于生成更稳定的过渡帧。

### 补充图表

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/009_Figure_6.jpg]]
*Figure 6: Ablation study. (a) Evaluations of the impact of different sampling rates in Consistent Self-Attention. (b) We explore the introduction of external control IDs to govern the generation of characters. Our StoryDiffusion can generate consistent images that conform to the ID images*



## 实验与关键发现

### 主体一致图像生成

StoryDiffusion 在主体一致图像生成任务上与多个专用方法进行了定量比较，包括 **IP-Adapter**（Ye et al., 2023）、**PhotoMaker**（Li et al., 2023a）和 **InstantID**（Wang et al., 2024）。这些基线方法通常需要额外的训练或微调来实现身份保持，而 StoryDiffusion 的 Consistent Self-Attention 以训练自由的方式直接插入预训练扩散模型。

Table 1 报告了两项核心指标：**Text-Image Similarity**（文本-图像相似度）和 **Character Similarity**（人物相似度）。StoryDiffusion 在 Text-Image Similarity 上达到 **0.6586**，在 Character Similarity 上达到 **0.8950**，均优于上述基线方法。这一结果的关键在于：Consistent Self-Attention 通过跨图像共享键-值对，使批次内不同图像在生成过程中相互参照视觉特征，从而在保持高文本可控性的同时实现主体一致性——而这一切无需任何训练。

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons of consistent image generation. Our StoryDiffusion achieves better text similarity and subject similarity even without any training*

定性结果（Figure 4）进一步表明，基线方法在连续生成多张图像时，人物面部特征、服装颜色和款式往往出现明显漂移，而 StoryDiffusion 能够在不同姿态和场景下维持稳定的视觉身份。

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/005_Figure_4.jpg]]
*Figure 4: Comparison of consistent image generation with recent methods*

### 过渡视频生成

在过渡视频生成任务上，StoryDiffusion 与 **SEINE**（Chen et al., 2023）和 **SparseCtrl**（Guo et al., 2023）进行了系统对比。Table 2 报告了四项指标：LPIPS-first、LPIPS-frames、CLIPSIM-first 和 CLIPSIM-frames。StoryDiffusion 在所有指标上均取得最优结果，其中 LPIPS-first 达到 **0.3794**，CLIPSIM-first 达到 **0.9606**。

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparisons with state-of-the-art transition video generation models*

这一优势源于 Semantic Motion Predictor 的设计选择：将运动预测从潜空间（latent space）迁移到图像语义空间。CLIP 图像编码器提供的语义嵌入能够更有效地编码空间信息和大范围运动，而 Transformer 预测的过渡嵌入通过交叉注意力注入视频扩散模型，为每一帧生成提供结构化的运动引导。定性对比（Figure 5）显示，SEINE 和 SparseCtrl 在处理大幅度动作变化时容易出现形变或内容断裂，而 StoryDiffusion 的过渡更加平滑自然。

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/008_Figure_5.jpg]]
*Figure 5: Comparisons of transition video generation with the recent state-of-the-art methods*

### 用户研究

Table 3 报告了用户研究结果。在主体一致图像生成方面，**72.8%** 的受试者更偏好 StoryDiffusion 的结果；在过渡视频生成方面，这一比例达到 **82.0%**。用户研究从主观感知层面验证了定量指标所反映的趋势——训练自由的跨图像注意力机制和语义空间运动预测确实带来了可感知的质量提升。

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/010_Table_3.jpg]]
*Table 3: User Study on subject-consistent image generation and transition video generation*

### 消融实验

**采样率的影响。** Consistent Self-Attention 中的采样率（sampling rate）控制从批次内其他图像中采样的 token 比例。Figure 6(a) 展示了不同采样率下的生成效果：采样率设为 0.3 时，跨图像交互不足，无法有效维持主体一致性；采样率设为 0.5 时，能在对扩散过程影响最小的前提下实现稳定的一致性保持。因此，**0.5 被设定为默认采样率**。

**与外部 ID 控制的兼容性。** Consistent Self-Attention 并非封闭系统——它可以与外部身份控制方法协同工作。Figure 6(b) 展示了将 Consistent Self-Attention 与 PhotoMaker 结合的场景：PhotoMaker 提供指定身份的人脸参考，Consistent Self-Attention 则确保该身份在多张图像中保持一致。结果表明，两者结合能够生成既符合指定身份又保持跨图像一致性的图像序列。

**与 ControlNet 的兼容性。** 进一步地，Consistent Self-Attention 还可以与 ControlNet 结合（Figure 8），在引入姿态、边缘等空间控制的条件下，仍然生成主体一致的图像。这验证了该模块的热插拔特性——它不干扰其他控制信号的注入路径。

### 失败模式与局限性

尽管 StoryDiffusion 在主体一致性和运动过渡方面表现突出，论文也明确指出了若干局限：

1. **服装细节不一致。** 对于精细的服饰配件（如领带、纽扣样式），仅靠跨图像自注意力可能无法完全维持一致性，需要更详细的文本提示来约束细节生成。
2. **长视频生成的局限。** 虽然可以通过滑动窗口方式扩展视频长度，但该方法并非专为极长视频设计。滑动窗口之间缺乏全局信息交换机制，导致长视频中可能出现累积漂移或前后不一致。
3. **采样率固定的问题。** 当前采样率 0.5 是全局默认值，未根据生成内容的自适应调节，这可能在一致性-多样性权衡上存在优化空间。

### 小结

StoryDiffusion 的核心实验结论可归纳为：通过修改自注意力中键-值的来源（从批次内其他图像采样并拼接），以训练自由的方式实现了跨图像的主体一致性；通过将运动预测迁移到语义空间，有效处理了大幅度动作的过渡视频生成。定量指标、定性对比和用户研究三方证据均支持这一设计的有效性，而消融实验进一步明确了采样率等关键超参数的作用边界。

### 补充图表

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/004_Figure.jpg]]
*Figure: Unwrapping a birthday gift Folding origami paper into shapes*

![[assets/figures/papers/StoryDiffusion_08e33f41766b/figures/011_Figure_8.jpg]]
*Figure 8: Generation results of our Consistent Self-Attention combined with ControlNet*



## 定位与知识库关联

### 核心定位

StoryDiffusion 处于**训练自由的主体一致图像生成**与**基于语义空间的过渡视频生成**两条技术路线的交汇点。其核心贡献——Consistent Self-Attention——是一种“热插拔”式的自注意力修改方案，无需任何训练或微调即可插入预训练扩散模型，通过批次内跨图像的 token 交互来维持多幅生成图像间的主体一致性。这一思路与当前主流的基于适配器（Adapter）或身份编码器（ID Encoder）的主体控制方法形成互补而非替代关系。

### 与基线方法的关系

**主体一致图像生成方面**，StoryDiffusion 与三类代表性方法形成对照：

1. **IP-Adapter**（Ye et al., 2023）和 **PhotoMaker**（Li et al., 2023a）：这两类方法通过额外训练适配器模块或身份编码器，将参考图像的身份信息注入扩散模型的交叉注意力层。其优势在于可以精确控制生成人物的身份，但需要额外的训练数据和计算开销。StoryDiffusion 的 Consistent Self-Attention 则完全绕开了训练环节，通过修改自注意力中键（key）和值（value）的来源——从同批次其他图像中随机采样 token 并拼接到当前图像的键值对中——来实现跨图像的特征共享。这种训练自由的特性使其可以作为上述方法的补充：消融实验（Figure 6b）证实，Consistent Self-Attention 可与 PhotoMaker 等外部 ID 控制方法结合，生成既符合指定身份又保持跨帧一致性的图像序列。

2. **InstantID**（Wang et al., 2024）：同样聚焦于身份保持，但 StoryDiffusion 的差异化在于其处理的是“无参考图像”场景——仅凭文本提示即可在批次内自动维持主体一致性，而不需要提供目标身份的先验图像。

**过渡视频生成方面**，StoryDiffusion 的 Semantic Motion Predictor 与以下方法形成对比：

1. **SEINE**（Chen et al., 2023）和 **SparseCtrl**（Guo et al., 2023）：这两类方法通常在图像潜空间（latent space）中预测中间帧。StoryDiffusion 的关键创新在于将运动预测的编码空间从潜空间迁移到**图像语义空间**——利用预训练 CLIP 图像编码器将首尾帧映射为语义向量，经过线性插值和 Transformer 预测中间帧的语义嵌入，再通过视频扩散模型的交叉注意力将这些嵌入作为控制信号解码。这一设计使得方法能够处理更大的运动幅度，在 LPIPS 和 CLIPSIM 指标上全面优于 SEINE 和 SparseCtrl（Table 2）。

### 方法谱系中的位置

从技术架构角度，StoryDiffusion 可被归类为：

- **自注意力操控类方法**：通过修改扩散模型 U-Net 中自注意力层的键-值来源来实现跨实例交互。这与 Prompt-to-Prompt 等通过注意力图操控实现编辑的思路在技术哲学上有相通之处，但应用目标从“编辑”转向“一致性生成”。
- **语义空间运动建模类方法**：将运动预测从像素/潜空间提升到语义空间，与近年利用 CLIP 嵌入空间进行视频理解与生成的趋势一致，但在过渡帧生成这一特定任务上具有独创性。

### 适用边界与局限

基于论文提供的证据，StoryDiffusion 的适用边界和局限可归纳如下：

1. **细节一致性的上限**：论文明确指出，服装细节（如领带）可能出现不一致，需要更详细的提示词来辅助维持。这表明 Consistent Self-Attention 在粗粒度特征（身份、体型、服装颜色）上表现良好，但在细粒度配件上仍有提升空间。

2. **长视频生成的局限**：尽管可通过滑动窗口策略生成更长的视频，但方法并非专为极长视频设计。滑动窗口之间缺乏全局信息交换机制，导致长视频生成时可能出现累积误差或风格漂移。论文将此列为开放问题。

3. **采样率的敏感性**：消融实验（Figure 6a）表明，采样率对一致性-多样性的平衡至关重要。采样率 0.3 无法维持主体一致性，采样率 0.5 被设为默认值，因其在“对扩散过程影响最小”的前提下保持了足够的一致性。这一参数在不同场景下是否可自适应调节，仍是一个开放问题。

4. **对预训练模型的依赖**：Consistent Self-Attention 复用了原始自注意力权重以保持训练自由，这意味着其性能上限受限于底层预训练模型的能力。在基础模型本身对特定主体或风格生成能力较弱时，一致性效果可能受限。

### 开放问题

1. **细粒度一致性的提升路径**：如何在服饰配件、纹理细节等细粒度层面进一步提升一致性？是否需要引入额外的局部注意力机制或显式的部件级约束？

2. **全局信息交换机制**：为任意长时间的视频生成设计有效的全局信息交换机制，使滑动窗口之间能够共享主体状态，避免累积漂移。

3. **采样率的自适应调节**：采样率在一致性-多样性权衡中的作用是否可在不同场景（如不同主体复杂度、不同运动幅度）下自适应调节？

4. **多模态条件扩展**：Semantic Motion Predictor 当前仅以首尾帧图像为条件，是否可以扩展到更多模态的条件输入，如文本动作描述、音频节奏信号或草图轨迹？

5. **计算资源可行性**：Consistent Self-Attention 的批次内跨图像交互增加了自注意力计算的 token 数量，Semantic Motion Predictor 则需要额外的 CLIP 编码和 Transformer 推理。在计算资源有限的设备上，这些模块的可行性如何？是否存在轻量化替代方案？



## 原文 PDF

![[paperPDFs/NEURIPS_2024/StoryDiffusion.pdf]]
