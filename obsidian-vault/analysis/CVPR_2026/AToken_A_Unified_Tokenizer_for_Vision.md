---
title: "AToken: A Unified Tokenizer for Vision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/AToken_A_Unified_Tokenizer_for_Vision.pdf
project_link: null
code_link: null
aliases:
- AToken
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入稀疏 4D 表示与无对抗训练（Gram 矩阵损失），使得单一 Transformer 架构可以同时实现多模态的高保真重建和语义理解。
primary_logic: 所有视觉模态均可表示为 4D 空间中的稀疏(特征, 坐标)对，利用 Gram 矩阵直接优化特征协方差可替代 GAN 实现稳定且高质量的重建。
claims:
- GAN 训练在 Transformer 架构中失败，判别器迅速压倒生成器，导致模式崩溃和 rFID 恶化。
- rFID 误差中约 86.6% 来自协方差（纹理/风格），均值成分仅占 13.4%。
- Gram loss 直接优化二阶统计量，无需对抗训练即可实现稳定且更优的 rFID。
- ATOKEN-So/C 在 16×16 压缩下达到 0.209 rFID，同时保持 82.2% ImageNet 零样本分类准确率。
---

# AToken: A Unified Tokenizer for Vision

> [!tip] 核心洞察
> 所有视觉模态均可表示为 4D 空间中的稀疏(特征, 坐标)对，利用 Gram 矩阵直接优化特征协方差可替代 GAN 实现稳定且高质量的重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | ATOKEN: 统一的视觉分词器 |
| 英文题名 | AToken: A Unified Tokenizer for Vision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.14476) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ATOKEN |
| Dataset | ImageNet 256x256, ImageNet 零样本分类, DAVIS 视频重建, TokenBench 视频重建 |

> [!tip] 效果简介
> - ImageNet 256x256 (图像重建) 上，rFID 0.21 (ATOKEN-So/C) vs 0.49 (SD-VAE) (-0.28)；PSNR 29.72 (ATOKEN-So/C) vs 27.1 (SD-VAE) (+2.62)。
> - ImageNet 零样本分类 上，Accuracy 82.2% (ATOKEN-So/C) vs 80.9% (SigLIP2) (+1.3%)。
> - DAVIS 视频重建 (1080p) 上，PSNR 33.11 (ATOKEN-So/C) vs 33.11 (Cosmos) (持平)。

## 概述

### 问题背景与核心瓶颈

视觉信号的 token 化是连接原始像素与生成模型、多模态理解系统的关键桥梁。然而，现有视觉分词器面临三重割裂：**任务割裂**——重建（如 SD-VAE, Rombach et al., CVPR 2022）与理解（如 SigLIP2, Tschannen et al., 2025）各成体系；**模态割裂**——图像、视频、3D 资产各自使用专用分词器；**架构与训练割裂**——基于 Transformer 的分词器在 GAN 训练下极易模式崩溃，判别器迅速压倒生成器，导致 rFID 恶化（Figure 4a）。这些割裂迫使下游应用维护多套异构分词器，阻碍了统一视觉基础模型的发展。

### 核心洞察与方法定位

ATOKEN 的核心洞察是：**所有视觉模态均可表示为 4D 空间中的稀疏 (特征, 坐标) 对**。基于此，ATOKEN 提出三项关键设计：

1. **统一 4D 潜在空间**：将图像、视频、3D 资产统一编码为 $z = \{ (z_i, p_i) \}_{i=1}^{L}$，其中 $p_i \in \{0,1,\dots,N-1\}^4$ 表示 (t, x, y, z) 坐标，不同模态自然占据各自子空间（Section 3.1）。
2. **纯 Transformer 架构 + 4D RoPE**：摒弃卷积/混合架构，采用纯 Transformer 编码器-解码器，配合 4D Rotary Position Embeddings 统一处理任意分辨率和时间长度（Section 3.2）。
3. **无对抗训练**：发现 rFID 误差中约 86.6% 来自协方差（纹理/风格），均值成分仅占 13.4%（Figure 4b），因此引入 Gram 矩阵损失直接优化特征协方差，替代 GAN 实现稳定且更优的重建（Figure 4c）。

ATOKEN 是首个同时覆盖图像、视频、3D 重建与理解，并支持连续与离散 token 的统一分词器（Table 1）。

### 主要结果概要

- **图像重建**：在 ImageNet 256×256 上，ATOKEN-So/C 以 16×16 压缩比达到 **0.209 rFID**，显著优于 SD-VAE（0.49），PSNR 达 29.72 dB（Table 4）。
- **图像理解**：零样本 ImageNet 分类准确率 **82.2%**，超越专用理解编码器 SigLIP2（80.9%），且多模态联合训练后仅轻微下降（Table 5）。
- **视频重建**：在 TokenBench 上 rFVD 达 **3.01**，优于 Hunyuan（4.66）；DAVIS 1080p 上 PSNR 与专用视频分词器 Cosmos 持平（Table 6）。
- **3D 重建**：Toys4k 上 PSNR 28.28 dB，与专用 3D 分词器 Trellis-SLAT（28.37 dB）可比（Table 8）。
- **模型容量关键性**：大容量 So400m 模型在多模态扩展后图像 rFID 从 0.258 降至 0.209（提升 19%），而 Base 模型从 0.323 升至 0.483（退化 49%），表明充足容量是多模态统一的前提（Figure 7b）。

### 方法谱系与知识库定位

ATOKEN 在视觉分词器谱系中占据独特位置（Table 1）。与仅重建的方法（**SD-VAE**, **VQGAN** Esser et al., 2020; **Cosmos** Agarwal et al., 2025）和仅理解的方法（**SigLIP2**）不同，ATOKEN 联合优化重建与理解。与已有统一尝试（**VILA-U** Wu et al., 2024c; **UniTok** Ma et al., 2025a）相比，ATOKEN 首次将模态覆盖从图像扩展到视频和 3D，并采用纯 Transformer 架构配合无对抗训练，解决了 GAN 在 Transformer 上的训练不稳定问题。其 4D 稀疏表示和 Gram 损失设计为多模态统一分词提供了新的范式。

## 背景与动机

### 视觉分词器的割裂现状

视觉分词器（visual tokenizer）是连接原始视觉信号与生成/理解模型的核心组件，其质量直接决定下游任务的上限。然而，当前领域面临三重割裂：

**任务割裂**：重建导向的分词器（如 **SD-VAE**（Rombach et al., CVPR 2022）、**VQGAN**（Esser et al., 2020））追求像素级保真度，却缺乏语义判别能力；理解导向的编码器（如 **SigLIP2**（Tschannen et al., 2025））擅长零样本分类与检索，但无法从潜在表示重建出可识别的视觉内容。少数尝试统一重建与理解的方法，如 **VILA-U**（Wu et al., 2024c）和 **UniTok**（Ma et al., 2025a），仍局限于单一图像模态。

**模态割裂**：图像、视频、3D 资产各自拥有独立的分词器设计——图像使用 2D 网格或序列表示，视频引入时空压缩，3D 依赖多视图渲染与体素聚合。**Cosmos**（Agarwal et al., 2025）支持图像和视频重建，**Trellis-SLAT**（Xiang et al., 2024）专注 3D 重建，但没有任何方法能同时覆盖三种模态。

**架构与训练稳定性割裂**：基于卷积的分词器在重建任务上成熟稳定，但难以灵活扩展到多模态统一表示；纯 Transformer 架构表达能力强，却面临训练不稳定的核心障碍——GAN 训练在 Transformer 框架中极易模式崩溃，判别器迅速压倒生成器，导致 rFID 发散（见 Figure 4(a)）。

### 核心瓶颈与本文动机

上述割裂的根源在于缺乏一个**统一的表示空间**和**稳定的训练范式**。本文识别出两个关键因果机制：

1. **表示瓶颈**：所有视觉模态本质上都可以视为 4D 时空空间中的信号——图像是时间维度为 1 的特例，视频是密集时间采样，3D 资产可通过多视图渲染投影到 2D 平面。若能构建一个稀疏的 4D 潜在空间，让不同模态自然占据各自的子空间，就可以用单一架构处理全部视觉输入。

2. **训练瓶颈**：GAN 在 Transformer 架构中的失败，源于判别器对二阶统计量（纹理/风格）的过度敏感。实验表明，rFID 误差中约 **86.6%** 来自特征协方差，均值成分仅占 **13.4%**（Figure 4(b)）。这意味着如果能直接优化特征协方差矩阵，就可以绕过对抗训练的不稳定性。

基于以上分析，本文提出 **ATOKEN**——首个在图像、视频、3D 三种模态上同时实现高保真重建与语义理解的统一视觉分词器。其核心设计包括：（1）稀疏 4D 潜在表示，将任意视觉输入编码为 (特征, 坐标) 对；（2）纯 Transformer 架构配合 4D RoPE 位置编码；（3）以 Gram 矩阵损失替代 GAN 的无对抗训练目标，直接优化二阶统计量以实现稳定且高质量的重建。

### 方法谱系与知识库定位

ATOKEN 在现有工作谱系中的定位如 Table 1 所示：它是唯一同时覆盖重建与理解任务、支持图像/视频/3D 三种模态、兼容连续与离散 token 类型的方法。与仅重建的方法（SD-VAE、VQGAN、Cosmos、Trellis-SLAT）相比，ATOKEN 额外提供语义理解能力；与仅理解的方法（SigLIP2）相比，ATOKEN 额外支持高质量重建；与已有的统一方法（VILA-U、UniTok）相比，ATOKEN 将覆盖范围从单模态扩展到全模态。

## 核心创新

ATOKEN 的核心创新并非单一模块的改进，而是通过三个相互耦合的机制——**统一稀疏 4D 表示**、**纯 Transformer 架构**与**无对抗 Gram 损失训练**——系统性解决了现有视觉分词器在模态覆盖、任务统一和训练稳定性上的三重割裂。这些创新共同构成了一个“**全模态、全任务、全 token 类型**”的统一框架，其与基线方法的本质差异可归纳为以下七个关键维度的改变。

### 1. 模态覆盖：从单模态碎片化到 4D 统一空间

现有视觉分词器高度碎片化：**SD-VAE** (Rombach et al., CVPR 2022) 仅处理图像，**Cosmos** (Agarwal et al., 2025) 聚焦图像/视频，**Trellis-SLAT** (Xiang et al., 2024) 专攻 3D，无一能同时覆盖三种模态。ATOKEN 的核心洞察是：所有视觉模态均可表示为 4D 空间中的稀疏 `(特征, 坐标)` 对：

$$z = \{ ( z _ { i } , p _ { i } ) \} _ { i = 1 } ^ { L } , \quad z _ { i } \in \mathbb { R } ^ { C } , \quad p _ { i } \in \{ 0 , 1 , \dots , N - 1 \} ^ { 4 }$$

其中 $(t, x, y, z)$ 坐标使得不同模态自然占据不同子空间：图像为 $(0, x, y, 0)$ 的 2D 切片，视频为 $(t, x, y, 0)$ 的 3D 子空间，3D 资产为 $(0, x, y, z)$ 的体素网格。这一表示使得**单一编码器无需任何架构修改即可处理所有模态**（Section 3.1），从根本上消除了模态特定的分支设计。

### 2. 架构范式：从卷积/混合架构到纯 Transformer

主流重建分词器（SD-VAE、VQGAN 等）普遍依赖卷积编码器-解码器，而理解模型（SigLIP2 等）使用 ViT。ATOKEN 首次在统一框架中采用**纯 Transformer 架构**（编码器与解码器均为 Transformer），并引入 **4D Rotary Position Embeddings (RoPE)** 替代传统的绝对或 2D 位置编码，以处理任意分辨率和时长的输入。这一架构选择的直接后果是：Transformer 对全局依赖的建模能力天然适合跨模态共享，但也带来了训练不稳定这一关键挑战——这正是下一项创新所要解决的核心问题。

### 3. 训练目标：从对抗训练到 Gram 矩阵损失

这是 ATOKEN 最具因果辨识度的创新。在纯 Transformer 架构上直接应用 GAN 训练会导致**判别器迅速压倒生成器，引发模式崩溃和 rFID 恶化**（Figure 4a）。ATOKEN 通过分解 rFID 误差发现：**约 86.6% 的误差来自协方差（纹理/风格），均值成分仅占 13.4%**（Figure 4b）。基于这一诊断，作者提出 **Gram 矩阵损失**，直接优化特征协方差矩阵的 Frobenius 范数：

$$\mathcal { L } _ { \mathrm { G r a m } } ( \boldsymbol { x } , \hat { \boldsymbol { x } } ) = \sum _ { l } \left\| \boldsymbol { G } ( \Phi _ { l } ( \boldsymbol { x } ) ) - \boldsymbol { G } ( \Phi _ { l } ( \hat { \boldsymbol { x } } ) ) \right\| _ { F } ^ { 2 }$$

该损失与 L1、LPIPS、CLIP 损失联合使用，完全替代 GAN，实现了**稳定且更优的 rFID**（Figure 4c）。这一“无对抗训练”方案是 ATOKEN 在 Transformer 架构上成功收敛的关键因果杠杆。

### 4. 任务覆盖：从重建/理解二选一到联合优化

现有方法要么仅重建（SD-VAE、Cosmos），要么仅理解（SigLIP2），少数统一方法（VILA-U、UniTok）也仅覆盖图像。ATOKEN 通过**双投影头设计**实现重建与理解的联合优化：重建投影 $W_r$ 将潜在特征映射到低维空间用于解码，语义投影 $W_s$ 结合注意力池化聚合全局表示并对齐到文本空间。图像语义对齐采用 KL 蒸馏（教师为 SigLIP2），视频/3D 采用 sigmoid 损失。这一设计使得 ATOKEN 在 16×16 压缩下同时达到 **0.209 rFID 和 82.2% ImageNet 零样本分类准确率**（Table 3/4/5），证明了重建质量与语义理解并非零和博弈。

### 5. 量化方式：从 VQ-VAE 到 FSQ 双模式

传统离散分词器（VQGAN）依赖 VQ-VAE 量化，训练复杂且易受码本崩溃影响。ATOKEN 采用 **FSQ (Finite Scalar Quantization)** 量化，支持连续 token（ATOKEN-So/C）和离散 token（ATOKEN-So/D）两种模式，为下游生成任务提供了灵活的选择空间。

### 6. 训练课程：渐进式多模态扩展

ATOKEN 采用四阶段渐进式训练课程（Figure 5）：从 SigLIP2 图像理解初始化出发，依次添加图像重建、视频能力、3D 理解，最后可选 FSQ 量化。这一课程设计的关键发现是：**模型容量是决定多模态统一成败的核心变量**。大容量 So400m 模型在多模态扩展后图像 rFID 从 0.258 降至 0.209（提升 19%），而 Base 模型从 0.323 升至 0.483（退化 49%）（Figure 7b）。这表明小模型在多模态联合训练中存在严重的任务间干扰，容量扩展是释放统一框架潜力的必要条件。

### 7. 3D 集成：从 DINOv2 特征到原生 RGB patch

在 3D 模态集成上，ATOKEN 对 Trellis-SLAT 做了两项关键改造（Figure 3）：一是直接对多视图渲染的 **RGB patch** 进行分词，而非使用预训练的 DINOv2 特征，从而保持与图像/视频统一的输入空间；二是每个体素从最近视角聚合特征，而非所有视角平均，以保留更精确的几何对应关系。这使得 3D 重建在 Toys4k 上达到与专用方法持平的 28.28 PSNR（Table 8），同时共享同一编码器。

---

**总结**：ATOKEN 的创新链呈现清晰的因果结构——4D 稀疏表示提供了模态统一的数学基础，纯 Transformer 架构赋予了跨模态共享的模型容量，而 Gram 损失则解决了 Transformer 在此设定下的训练稳定性瓶颈。三者缺一不可，共同构成了从“模态/任务碎片化”到“全模态统一”的范式跃迁。

## 整体框架

ATOKEN 的核心设计理念是：**所有视觉模态均可表示为 4D 空间中的稀疏特征-坐标对**，单一 Transformer 架构即可同时实现高保真重建与语义理解。图 2 展示了这一统一框架的完整数据流。

### 统一输入处理

任意视觉输入——图像、视频或 3D 资产——首先经过**统一时空分块化 (Unified Space-Time Patchification)**。对于图像，将其视为单帧视频进行时间零填充；对于视频，直接按 $t \times p \times p$ 的非重叠时空块进行划分；对于 3D 资产，则从球面采样相机渲染多视角图像，再应用标准时空分块化，每个 $64^3$ 网格体素通过反投影收集并平均来自最近视点的 patch 特征（图 3）。这一设计使得所有模态共享同一嵌入层，无需任何架构修改。

### 核心表示空间

分块后的特征通过**稀疏 Transformer 编码器**映射到统一的 4D 潜在空间：

$$
z = \{ ( z _ { i } , p _ { i } ) \} _ { i = 1 } ^ { L } , \quad z _ { i } \in \mathbb { R } ^ { C } , \quad p _ { i } \in \{ 0 , 1 , \dots , N - 1 \} ^ { 4 }
$$

其中 $p_i$ 为 $(t, x, y, z)$ 坐标，不同模态自然占据相应子空间：图像为 $(0, x, y, 0)$，视频为 $(t, x, y, 0)$，3D 为 $(0, x, y, z)$。编码器采用纯 Transformer 架构，在每一注意力层注入**4D Rotary Position Embeddings (RoPE)**，为稀疏坐标对提供相对位置信息。

### 双路投影与多任务解耦

编码后的潜在表示分两路输出：

- **重建支路**：通过重建投影矩阵 $W_r$ 将高维特征映射到低维空间，随后送入**模态特定解码器**。图像/视频使用像素解码器 $\mathcal{D}_{\mathrm{P}}$ 恢复 RGB 帧，3D 使用高斯溅射解码器 $\mathcal{D}_{\mathrm{GS}}$ 生成每体素 $K$ 个高斯球的参数（位置偏移、颜色、尺度、不透明度、旋转），实现高效可微渲染。
- **语义支路**：通过**注意力池化 (Attention Pooling)** 聚合全局表示，经语义投影矩阵 $W_s$ 映射到文本对齐空间，支持零样本分类与检索。

### 训练目标与稳定性设计

总损失函数为三项加权组合：

$$
\mathcal { L } = \lambda _ { \mathrm { r e c } } \mathcal { L } _ { \mathrm { r e c } } + \lambda _ { \mathrm { s e m } } \mathcal { L } _ { \mathrm { s e m } } + \lambda _ { \mathrm { K L } } \mathcal { L } _ { \mathrm { K L } }
$$

其中**重建损失** $\mathcal{L}_{\mathrm{rec}}$ 针对不同模态采用差异化组合。以图像为例：

$$
\mathcal { L } _ { \mathrm { r e c } } ^ { \mathrm { I } } = \lambda _ { 1 } \mathcal { L } _ { 1 } + \lambda _ { \mathrm { L P I P S } } \mathcal { L } _ { \mathrm { L P I P S } } + \lambda _ { \mathrm { G R A M } } \mathcal { L } _ { \mathrm { G R A M } } + \lambda _ { \mathrm { C L P } } \mathcal { L } _ { \mathrm { C L I P } }
$$

关键创新在于 **Gram 矩阵损失**：

$$
\mathcal { L } _ { \mathrm { G r a m } } ( \boldsymbol { x } , \hat { \boldsymbol { x } } ) = \sum _ { l } \left\| \boldsymbol { G } ( \Phi _ { l } ( \boldsymbol { x } ) ) - \boldsymbol { G } ( \Phi _ { l } ( \hat { \boldsymbol { x } } ) ) \right\| _ { F } ^ { 2 }
$$

该损失直接优化预训练网络各层特征的 Gram 矩阵（即二阶协方差统计量），替代传统 GAN 对抗训练。实验证据表明，这一选择具有因果必然性：rFID 误差中约 **86.6% 来自协方差分量**（纹理/风格），均值分量仅占 13.4%（图 4b）；而 GAN 训练在纯 Transformer 架构下失败，判别器迅速压倒生成器导致模式崩溃（图 4a）。Gram loss 无需对抗训练即可实现稳定且更优的 rFID（图 4c）。

**语义损失** $\mathcal{L}_{\mathrm{sem}}$ 针对图像采用 KL 蒸馏，最小化学生与教师模型（SigLIP2）之间温度缩放视觉-文本相似度分布的 KL 散度；视频和 3D 则使用 sigmoid 损失。此外，对重建潜在变量施加 **KL 正则化**以稳定训练。

### 可选量化

框架在 Stage 4 引入 **FSQ (Finite Scalar Quantization)**，将连续潜在变量量化为离散 token，使 ATOKEN 同时支持连续与离散两种表示类型，适配不同的生成范式。

### 补充图表

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our method. All modalities undergo unified space-time patchification and encoding into sparse 4D latents, which support both reconstruction through modality-specific decoders and understanding through attention pooling and text alignment. The architecture jointly optimizes reconstruction and understanding losses, maintaining sparse structured representations throughout for efficient multimodal processing*

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our method on different visual modalities. Given images, videos, and 3D assets, ATOKEN leverages a shared 4D latent space (left) to produce high-fidelity reconstructions (middle: zoomed regions with red boxes for images, temporal frames for videos, multiple viewpoints for 3D) while preserving strong semantic understanding (right: showing text-aligned representations for zero-shot text retrieval)*

## 核心模块与公式推导

### 统一稀疏 4D 表示空间

ATOKEN 的核心洞察在于：所有视觉模态均可表示为共享 4D 空间中的稀疏特征-坐标对。该表示形式化为：

$$z = \{ ( z _ { i } , p _ { i } ) \} _ { i = 1 } ^ { L } , \quad z _ { i } \in \mathbb { R } ^ { C } , \quad p _ { i } \in \{ 0 , 1 , \dots , N - 1 \} ^ { 4 }$$

其中 $z_i$ 为 $C$ 维特征向量，$p_i$ 为 $(t, x, y, z)$ 四维坐标。图像天然占据 $(t=0, x, y, z=0)$ 子空间，视频扩展至 $t>0$ 维度，3D 资产则利用 $(x, y, z)$ 三维空间。这一设计使得单一编码器 $\mathcal{E}$ 无需任何架构修改即可处理所有模态输入。

### 统一时空 Patch 嵌入与 4D RoPE

给定输入 $\mathbf{x} \in \mathbb{R}^{T \times H \times W \times 3}$，将其划分为大小为 $t \times p \times p$ 的非重叠时空 patch。对于图像，时间维度为零填充以统一维度。每个 patch 通过线性投影得到初始嵌入，并叠加 4D Rotary Position Embeddings (RoPE)，在每一注意力层提供 $(t, x, y, z)$ 四维相对位置信息。

对于 3D 资产，从球面采样相机渲染多视图图像后应用标准时空 patch 化；$64^3$ 网格中的每个体素通过反投影从最近视图中聚合 patch 特征，而非对所有视图取平均（Figure 3）。

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/004_Figure_3.jpg]]
*Figure 3: 3D tokenization pipeline. We extend Trellis-SLAT (Xiang et al., 2024) for multimodal unification through two modifications: directly tokenizing raw RGB patches from multiview renderings (as opposed to using DINOv2 features), and aggregating each voxel’s features from its nearest viewpoint (as opposed to averaging across all views). Combined with Gaussian decoding, this approach integrates 3D assets into our unified token space alongside images and videos*

### 双投影解耦：重建与语义

编码器输出的潜在表示 $z$ 通过两个独立投影矩阵解耦为重建分支和语义分支：

- **重建投影** $W_r$：将特征投影到低维空间（如 48 维），供 Transformer 解码器重建像素（图像/视频）或高斯 splatting 参数（3D）。
- **语义投影** $W_s$：通过注意力池化聚合全局表示，并投影到文本对齐空间，用于零样本分类与检索。

### 模态特定解码器

图像/视频解码器将结构化潜在变量映射回像素空间，将图像视为单帧视频处理：

$$\mathcal{D}_{\mathrm{P}} : \{ ( z_{i}, \pmb{p}_{i} ) \}_{i=1}^{L} \to \pmb{x} \in \mathbb{R}^{T \times H \times W \times 3}$$

3D 解码器则从每个体素位置生成 $K$ 个高斯球，包含位置偏移、颜色、尺度、不透明度和旋转参数：

$$\mathcal{D}_{\mathrm{GS}} : \{ ( z_{i}, p_{i} ) \}_{i=1}^{L} \to \{ \{ ( o_{i}^{k}, c_{i}^{k}, s_{i}^{k}, \alpha_{i}^{k}, r_{i}^{k} ) \}_{k=1}^{K} \}_{i=1}^{L}$$

高斯位置通过 $\mathbf{x}_i^k = \mathbf{p}_i + \tanh(\mathbf{o}_i^k)$ 约束在源体素附近，保证渲染稳定性。

### 无对抗训练目标

总损失函数由重建损失、语义损失和 KL 正则项加权组成：

$$\mathcal { L } = \lambda _ { \mathrm { r e c } } \mathcal { L } _ { \mathrm { r e c } } + \lambda _ { \mathrm { s e m } } \mathcal { L } _ { \mathrm { s e m } } + \lambda _ { \mathrm { K L } } \mathcal { L } _ { \mathrm { K L } }$$

#### 图像重建损失

$$\mathcal { L } _ { \mathrm { r e c } } ^ { \mathrm { I } } = \lambda _ { 1 } \mathcal { L } _ { 1 } + \lambda _ { \mathrm { L P I P S } } \mathcal { L } _ { \mathrm { L P I P S } } + \lambda _ { \mathrm { G R A M } } \mathcal { L } _ { \mathrm { G R A M } } + \lambda _ { \mathrm { C L P } } \mathcal { L } _ { \mathrm { C L I P } }$$

四项分别对应：L1 像素损失、LPIPS 感知损失、Gram 纹理损失和 CLIP 语义一致性损失。其中 Gram 损失是替代 GAN 训练的关键创新。

#### Gram 矩阵损失

$$\mathcal { L } _ { \mathrm { G r a m } } ( \boldsymbol { x } , \hat { \boldsymbol { x } } ) = \sum _ { l } \left\| \boldsymbol { G } ( \Phi _ { l } ( \boldsymbol { x } ) ) - \boldsymbol { G } ( \Phi _ { l } ( \hat { \boldsymbol { x } } ) ) \right\| _ { F } ^ { 2 }$$

该损失计算预训练网络 $\Phi$ 第 $l$ 层特征 Gram 矩阵的 Frobenius 范数，直接优化二阶统计量（纹理/风格）。**决定性证据**（Figure 4）表明：GAN 训练在纯 Transformer 架构中失败，判别器迅速压倒生成器导致模式崩溃；rFID 误差中约 86.6% 来自协方差成分，均值成分仅占 13.4%；Gram loss 无需对抗训练即可实现稳定且更优的 rFID。

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/008_Figure_4.jpg]]
*Figure 4: Adversarial-free training with Gram loss achieves stable, high-fidelity reconstruction. (a) GAN training fails in our setting: the discriminator overpowers the generator, causing diverging logits and degraded rFID. (b) Decomposing rFID reveals ≈ 86.6% of error stems from covariance (texture/style) vs. ≈ 13.4% from mean components. (c) Gram loss directly optimizes second-order statistics (i.e., feature covariance) without adversarial training, achieving superior and stable rFID throughout training*

#### 语义蒸馏损失（图像）

$$\mathcal { L } _ { \mathrm { s e m } } ^ { \mathrm { I } } = \mathrm { K L } \left( \mathrm { s o f t m a x } ( \tau ^ { - 1 } s ^ { \mathrm { t e a c h e r } } ) \| \mathrm { s o f t m a x } ( \tau ^ { - 1 } s ^ { \mathrm { s t u d e n t } } ) \right)$$

最小化教师模型（SigLIP2）与学生模型之间温度缩放视觉-文本相似度分布的 KL 散度。视频和 3D 模态则使用 sigmoid 损失进行语义对齐。

### FSQ 量化（可选阶段）

在 Stage 4，通过 Finite Scalar Quantization (FSQ) 将连续潜在变量量化为离散 token，使 ATOKEN 同时支持连续（ATOKEN-So/C）和离散（ATOKEN-So/D）两种 token 类型，适配不同类型的生成模型。

### 补充图表

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/009_Figure_6.jpg]]
*Figure 6: Overview of the video encoding and decoding process. During encoding, we use KV-caching across temporal tiles to eliminate redundant computation while maintaining temporal coherence, providing significant efficiency gains over overlapping tile methods*

## 实验与分析

### 核心发现：Gram 损失替代对抗训练实现稳定高质量重建

ATOKEN 在纯 Transformer 架构上实现多模态统一分词的关键突破，在于用 Gram 矩阵损失完全替代了传统视觉分词器依赖的对抗训练（GAN）。Figure 4 系统性地揭示了这一设计的必要性：

1. **GAN 训练在纯 Transformer 架构中失败**：如 Figure 4(a) 所示，当采用对抗训练时，判别器迅速压倒生成器，导致判别器 logits 发散和 rFID 持续恶化——这是典型的模式崩溃现象。这一发现直接排除了在 ATOKEN 架构中使用 GAN 的可能性。

2. **rFID 误差的协方差主导性**：Figure 4(b) 对 rFID 误差进行了分解，发现约 86.6% 的误差来自特征协方差（纹理/风格）成分，而均值成分仅占约 13.4%。这表明重建质量的核心瓶颈在于二阶统计量的对齐，而非像素级均值偏差。

3. **Gram 损失的稳定优化**：Figure 4(c) 证明，直接优化特征 Gram 矩阵的 Frobenius 范数（即二阶统计量）可以在无对抗训练的条件下实现稳定且更优的 rFID。Gram 损失直接针对误差的主导成分进行优化，从根本上解决了 Transformer 架构下的训练不稳定问题。

这一发现构成了 ATOKEN 训练策略的理论基础：通过公式 $\mathcal{L}_{\mathrm{Gram}}(\boldsymbol{x}, \hat{\boldsymbol{x}}) = \sum_{l} \|\boldsymbol{G}(\Phi_l(\boldsymbol{x})) - \boldsymbol{G}(\Phi_l(\hat{\boldsymbol{x}}))\|_F^2$ 直接优化特征协方差，配合 L1、LPIPS 和 CLIP 损失，实现了无需判别器的稳定训练。

### 跨模态主结果总览

Table 3 汇总了 ATOKEN 在图像、视频、3D 三个模态上的综合性能。ATOKEN-So/C（连续 token 模式）在 16×16 的高压缩比下，同时实现了：

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/011_Table_3.jpg]]
*Table 3: Performance comparison of visual tokenizers across modalities. We evaluate on ImageNet for image reconstruction and zero-shot classification, TokenBench for video reconstruction with MSR-VTT for zero-shot retrieval, and Toys4k for 3D reconstruction and classification. Methods are grouped by capability: reconstruction-only, understanding-only, and unified approaches. Discrete tokenizers are indicated with gray shading. † OmniTokenizer does not work well on high-resolution videos where tiling is needed*

- **图像**：0.209 rFID 的重建质量和 82.2% 的 ImageNet 零样本分类准确率
- **视频**：3.01 rFVD 的重建质量（TokenBench），显著优于 Hunyuan 的 4.66
- **3D**：28.28 PSNR 的重建质量（Toys4k），与专用方法 Trellis-SLAT 的 28.37 基本持平

值得注意的是，ATOKEN 是唯一同时覆盖重建与理解任务、支持连续与离散两种 token 类型、且跨图像/视频/3D 三个模态的方法。

### 图像重建与理解的深度评估

**图像重建**（Table 4）：在统一的 256×256 评测协议下，ATOKEN-So/C 以 0.209 rFID 和 29.72 PSNR 显著超越 SD-VAE（0.49 rFID, 27.1 PSNR），rFID 相对降低 57.3%。即便与离散方法 VQGAN 相比，ATOKEN-So/D 也以 0.38 rFID 展现出竞争力。Figure 9 的定性对比进一步显示，ATOKEN 在更高压缩比下仍能更好地保留高频纹理、细节和复杂文字元素。

**图像理解**（Table 5）：ATOKEN-So/C 在 ImageNet 零样本分类上达到 82.2%，不仅高于专用语义编码器 SigLIP2 的 80.9%，且在经历多模态多任务联合训练后，准确率仅从 82.7% 轻微下降至 82.2%，语义理解能力基本保持。这表明联合训练并未显著损害单一任务的语义表达能力。

### 视频与 3D 重建评估

**视频重建**（Table 6）：在 DAVIS 1080p 上，ATOKEN-So/C 以 33.11 PSNR 与专用视频分词器 Cosmos 持平；在 TokenBench 720p 上，ATOKEN-So/C 的 3.01 rFVD 显著优于 Hunyuan 的 4.66。Figure 10 的定性对比证实了其与专用视频方法相当的视觉质量。

**视频文本检索**（Table 7）：在 MSRVTT 上，ATOKEN-So/C 的 R@1 为 40.2，虽低于 VideoPrism 的 44.8，但考虑到 ATOKEN 同时优化三个模态的重建与理解任务，这一性能仍属合理水平。

**3D 重建**（Table 8）：ATOKEN-So/C 在 Toys4k 上达到 28.28 PSNR，与专用 3D 分词器 Trellis-SLAT 的 28.37 几乎一致。Figure 11 显示 ATOKEN 在颜色一致性上甚至优于专用方法。

### 模型容量对多模态统一的关键作用

Figure 7 的缩放实验揭示了一个重要发现：**模型容量是多模态统一训练的必要条件**。

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/016_Figure_7.jpg]]
*Figure 7: Architectural scaling comparison: Base vs. So400m models. (a) ImageNet rFID during Stage 1 training. (b) ImageNet rFID across training stages. (c) ImageNet zero-shot classification accuracy in Stage 1. (d) Video PSNR on DAVIS in Stages 2 and 3. The So400m model maintains or improves performance across all stages, while the Base model shows significant degradation when extending beyond single-modality training, indicating that sufficient model capacity is critical for successful multimodal visual tokenization*

- **大容量模型（So400m）从多模态扩展中获益**：从 Stage 1（仅图像）到 Stage 3（加视频和 3D），So400m 的图像 rFID 从 0.258 持续改善至 0.209（提升 19%），视频 PSNR 也保持稳定。
- **小容量模型（Base）在多模态扩展后退化**：Base 模型的图像 rFID 从 0.323 升至 0.483（退化 49%），表明容量不足时多模态联合训练会引入负迁移。

这一发现对实际部署具有重要指导意义：统一视觉分词器需要足够的模型容量来容纳多模态知识的共享与分化。

### 表征空间的可视化分析

Figure 8 的 t-SNE 可视化展示了不同训练阶段表征的语义聚类特性：

- **密集特征阶段（Stage 1-3 编码器输出）**：类别语义聚类清晰，表明联合训练未破坏语义结构。
- **投影降维后（48 维潜在空间）**：类别分布趋于混合，揭示了压缩比与语义可分离性之间的固有权衡。
- **FSQ 量化前（Stage 4）**：离散化进一步模糊了类别边界。

这一分析表明，ATOKEN 的高压缩比（16×16）虽然带来了效率优势，但也以牺牲部分语义可分离性为代价——这是当前方法的内在局限。

### 下游生成任务的验证

**类别条件图像生成**（Table 11, 12）：ATOKEN-So/C 配合 Lightning-DiT 在 ImageNet 256×256 上达到 1.78 gFID，ATOKEN-So/D 配合 TokenBridge-L 达到 2.32 gFID，证明了连续和离散 token 均能支撑高质量的生成任务。

**文本到图像/视频生成**（Table 13）：在资源受限的公平对比下，ATOKEN 的 Stage 2-3 模型在多项指标上超越 Cosmos、Hunyuan 等专用视频分词器，验证了统一分词器在生成任务上的泛化能力。

### 主要失败模式与局限

1. **离散 token 的视频重建退化**：ATOKEN-So/D 在视频重建上 rFVD 为 22.16，远劣于连续模式的 3.01，离散视频生成仍有较大提升空间。

2. **高维潜在空间的扩散训练不稳定**：连续 token 的 48 维潜在空间（相比典型 VAE 的 8 维）使得图像到 3D 合成时扩散模型训练困难，需要精细调整条件强度和扩散调度。

3. **长视频理解性能不足**：在 MLVU 等长视频理解基准上，ATOKEN 的性能仍有提升空间，可能与训练时长和数据集分布有关。

4. **计算资源需求高**：训练需要 256 张 H100 GPU，推理时尽管使用了 KV-caching 等加速策略，高分辨率视频处理仍面临效率挑战。

### 补充图表

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/002_Table_1.jpg]]
*Table 1: Comparison between existing visual tokenizers and AToken. We categorize methods by task capabilities (reconstruction, understanding, or both) and evaluate their modality coverage, architectural choices, token representations, and key features. ATOKEN is the only method providing support across all dimensions*

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/012_Table_4.jpg]]
*Table 4: Image reconstruction comparison on ImageNet and COCO. We evaluate all methods using a unified protocol with official implementations to ensure fair comparison. All images are resized and centercropped to 256×256, with metrics computed using identical scripts. Note that our reproduced results may differ from original papers due to standardized evaluation settings, but provide consistent cross-model comparison*

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/013_Table_5.jpg]]
*Table 5: Image understanding comparison with semantic encoders. We evaluate zero-shot classification on ImageNet, ImageNet-v2, and cross-modal retrieval on COCO and Flickr30k. ATOKEN maintains competitive performance across all stages despite joint training on multiple modalities and tasks*

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/014_Table_6.jpg]]
*Table 6: Video reconstruction comparison on high-resolution benchmarks. We evaluate quality on DAVIS at 1080p and TokenBench at 720p. All methods are re-evaluated using official implementations with consistent protocols for fair comparison. ATOKEN achieves competitive performance with specialized video-only tokenizers while uniquely supporting both continuous and discrete representations across modalities*

![[assets/figures/papers/paper_list_l2068_https_arxiv_org_abs_2509_14476/figures/017_Table_8.jpg]]
*Table 8: 3D reconstruction comparison on Toys4k. We average metrics across rendered multi-view images. ATOKEN achieves comparable performance to specialized Trellis-SLAT despite jointly optimizing for three modalities, demonstrating unified training maintains strong 3D capabilities*

## 方法谱系与知识库定位

### 1. 基线谱系与差异化定位

ATOKEN 的核心定位在于**首次实现跨模态（图像/视频/3D）与跨任务（重建/理解）的统一视觉分词**。为清晰呈现其在领域中的位置，Table 1 将现有工作按任务能力与模态覆盖进行了系统分类。

**纯重建基线**：
- **SD-VAE**（Rombach et al., CVPR 2022）与 **VQGAN**（Esser et al., 2020）是图像重建领域的标杆，但二者均依赖卷积架构与对抗训练（GAN），且不支持视频或 3D 模态。
- **Cosmos**（Agarwal et al., 2025）与 **Hunyuan** 等视频专用分词器在视频重建上表现强劲，但无法处理 3D 资产，且缺乏语义理解能力。
- **Trellis-SLAT**（Xiang et al., 2024）是 3D 重建的代表方法，但其编码器依赖 DINOv2 特征，与 RGB 域存在语义鸿沟，难以直接迁移至图像/视频理解。

**纯理解基线**：
- **SigLIP2**（Tschannen et al., 2025）在图像零样本分类与检索上性能优异，但完全不具备重建能力，无法作为生成模型的潜在空间。

**统一重建与理解的初步尝试**：
- **VILA-U**（Wu et al., 2024c）与 **UniTok**（Ma et al., 2025a）试图在单一框架内同时支持图像理解与重建，但其覆盖范围仍限于图像模态，未触及视频与 3D。
- **OmniTokenizer** 虽支持图像与视频，但在高分辨率视频上因需要分块（tiling）而表现不佳（Table 3 中以 † 标注），且不支持 3D 与离散 token。

**ATOKEN 的差异化体现在五个关键“槽位”的全面替换**：
1.  **模态覆盖**：从单模态扩展至图像、视频、3D 的统一处理。
2.  **表示空间**：从 2D/3D 网格序列升级为**稀疏 4D 空间**中的(特征, 坐标)对，使得不同模态自然地占据 4D 子空间（图像为 2D 空间子空间，视频为 3D 时空子空间，3D 为 3D 空间子空间）。
3.  **架构**：从卷积或混合架构全面转向**纯 Transformer**（编码器与解码器均为 Transformer），并引入 **4D Rotary Position Embeddings (RoPE)** 以处理任意分辨率与时长的输入。
4.  **训练目标**：**彻底移除对抗训练（GAN）**，代之以 Gram 矩阵损失直接优化二阶统计量（纹理/风格），结合 L1、LPIPS、CLIP 损失实现稳定且高质量的重建。
5.  **任务覆盖**：通过注意力池化（attention pooling）与分离投影（重建投影 $W_r$ 与语义投影 $W_s$），在单一编码器内同时支持重建与理解，且支持 **FSQ 量化**以生成离散 token。

### 2. 适用边界与局限

尽管 ATOKEN 在统一性上取得了突破，其设计仍存在明确的适用边界与已知局限：

1.  **连续 token 的生成稳定性**：在图像到 3D 合成任务中，ATOKEN 的连续 token 为 48 维（vs. Trellis-SLAT 的 8 维），高维潜在空间使得扩散模型的训练不稳定，需要针对性地调整条件强度与扩散调度。这表明 ATOKEN 的连续表示在直接适配现有扩散模型时可能需要额外的超参数搜索。

2.  **离散 token 的模态退化**：离散模式（ATOKEN-So/D）在视频重建上质量显著下降（rFVD 22.16 vs. 连续模式 3.01），说明 FSQ 量化在视频场景下的信息损失远大于图像场景，离散视频生成仍有较大提升空间。

3.  **计算资源需求**：训练需 256 张 H100 GPU，推理时尽管使用了 KV-caching 等加速策略，高分辨率视频处理仍面临效率挑战。这限制了其在资源受限场景下的直接复现与应用。

4.  **长视频理解**：在 MLVU 等长视频理解基准上，ATOKEN 的性能仍有提升空间，可能与训练时长和数据集分布有关。其视频语义对齐采用 sigmoid 损失而非图像所用的 KL 蒸馏，可能在一定程度上限制了视频理解的精度。

5.  **模型容量依赖**：Figure 7(b) 的消融实验揭示了一个关键瓶颈：**大容量 So400m 模型在多模态扩展后图像 rFID 从 0.258 降至 0.209（提升 19%），而 Base 模型从 0.323 升至 0.483（退化 49%）**。这表明多模态统一训练存在显著的容量门槛——小模型在多任务联合训练中遭遇严重的模态间干扰，统一框架的收益仅在充足容量下才能显现。

### 3. 开放问题

论文在结尾提出了若干值得探索的方向，这些开放问题构成了该领域的潜在研究前沿：

1.  **高维潜在空间的扩散优化**：如何在更高维度的潜在空间上系统性地优化扩散模型的训练与推理超参数，以保证生成质量与条件一致性？这是连续 token 从重建走向生成的核心工程挑战。

2.  **端到端全能模型（Omni-Model）**：是否可以构建一个覆盖所有模态和任务的端到端全能模型，以完全展现 ATOKEN 的统一潜力？当前 ATOKEN 的解码器仍是模态特定的，一个真正的统一解码器可能进一步释放跨模态迁移的收益。

3.  **有限容量下的干扰缓解**：在模型容量有限时，多模态联合训练带来的干扰是否可以通过更精巧的课程学习或正则化方法来缓解？Figure 7 中 Base 模型的退化现象提示，容量瓶颈可能是统一框架走向普惠化的主要障碍。

4.  **长视频语义理解的提升**：长期的、开放域的视频理解任务中，如何进一步提升 ATOKEN 的语义表达能力？是否需要更长的训练时长、更丰富的视频-文本数据，或更先进的时序聚合机制？

## 原文 PDF

![[paperPDFs/CVPR_2026/AToken_A_Unified_Tokenizer_for_Vision.pdf]]