---
title: "FlashVSR: Towards Real-time Diffusion-Based Streaming Video Super Resolution"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FlashVSR_Towards_Real_time_Diffusion_Based_Streaming_Video_Super_Resolution.pdf
project_link: "https://zhuang2002.github.io/FlashVSR"
code_link: null
aliases:
- FlashVSR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过三阶段蒸馏构建单步扩散模型，结合块稀疏因果注意力、局部窗口约束和轻量条件解码器，并利用VSR任务对低分辨率帧的强条件依赖设计并行训练范式，从而实现低延迟、高吞吐的实时流式超分。
primary_logic: 与视频生成不同，VSR的强条件来自低分辨率帧，模型的任务是内容重建而非运动合成，因此无需将先前预测的干净隐变量作为输入；通过KV-cache传递后期层的干净特征即可维持时间连续性，从而消除训练-推理间隙，支持高效的并行训练。
claims:
- FlashVSR在单张A100上以17 FPS处理768×1408视频，比最优单步扩散基线SeedVR2-3B快约12倍。
- 块稀疏注意力将每8帧推理时间从1.105秒降至0.355秒（3.1倍加速），质量几乎无损。
- 轻量条件解码器（TC Decoder）将解码时间缩短至原VAE解码器的约1/7，同时保持可比质量。
- 局部约束注意力消除超高分辨率下的重复伪影，PSNR从24.21提升至24.87（Boundary-Preserved）。
---

# FlashVSR: Towards Real-time Diffusion-Based Streaming Video Super Resolution

> [!tip] 核心洞察
> 与视频生成不同，VSR的强条件来自低分辨率帧，模型的任务是内容重建而非运动合成，因此无需将先前预测的干净隐变量作为输入；通过KV-cache传递后期层的干净特征即可维持时间连续性，从而消除训练-推理间隙，支持高效的并行训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | FlashVSR：迈向实时扩散式流式视频超分辨率 |
| 英文题名 | FlashVSR: Towards Real-time Diffusion-Based Streaming Video Super Resolution |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2510.12747) · [Project](https://zhuang2002.github.io/FlashVSR) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FlashVSR |
| Dataset | 101帧 768×1408 视频, REDS, TC Decoder 消融 |

> [!tip] 效果简介
> - 101帧 768×1408 视频 上，FPS (帧/秒) 16.92 (Ours-Tiny) vs 1.44 (SeedVR2-3B) (约11.8倍加速)；峰值显存 (GB) 11.13 (Ours-Tiny) vs 52.88 (SeedVR2-3B) (节省78.9%)。
> - REDS (综合质量) 上，PSNR / SSIM / LPIPS 24.11 / 0.6511 / 0.3432 (13.6%稀疏) vs 24.65 / 0.6630 / 0.3320 (Full Attn.) (PSNR 下降0.54，质量基本持平)。
> - TC Decoder 消融 (PSNR) 上，PSNR / SSIM / LPIPS 31.08 / 0.9244 / 0.1014 (Ours) vs 32.58 / 0.9417 / 0.0715 (Wan Decoder) (质量轻微下降，但速度提升约7倍)。

## 概述

扩散式视频超分辨率（VSR）近年来取得了显著的感知质量提升，但现有方法普遍存在推理延迟高、计算开销大的瓶颈，难以满足实时流式处理的需求。核心矛盾在于：多步扩散采样带来了高昂的每帧计算成本，而分块式（chunk-wise）处理模式又引入了长达约80帧的前瞻延迟，严重制约了在线应用场景的部署。此外，训练与推理阶段的分辨率失配常导致超高分辨率下的重复伪影和模糊，进一步削弱了模型的泛化能力。

针对上述问题，本文提出了 **FlashVSR**——首个面向实时流式VSR的单步扩散框架。其核心洞察在于：与视频生成任务不同，VSR的强条件信号来自低分辨率（LR）帧，模型的核心任务是内容重建而非运动合成，因此无需将先前预测的干净隐变量作为输入；只需通过KV-cache传递后期层的干净特征即可维持时间连续性，从而消除训练-推理间隙，支持高效的并行训练。

基于这一洞察，FlashVSR构建了一条三阶段蒸馏管线：（1）视频-图像联合训练建立强教师模型；（2）引入块稀疏因果注意力适配流式推理；（3）通过分布匹配蒸馏结合重建监督生成单步学生模型。同时，局部约束稀疏注意力机制将查询范围限制在局部窗口内，对齐训练与推理的位置编码范围，有效抑制超高分辨率下的伪影；轻量条件解码器（TC Decoder）以LR帧为条件，将解码时间压缩至原始VAE解码器的约1/7。

实验表明，FlashVSR在单张A100 GPU上以约17 FPS的速度处理768×1408视频，比当前最快的单步扩散基线**SeedVR2-3B**（Wang et al., 2025a）快约12倍，峰值显存仅需11.13 GB（节省约79%），前瞻延迟从约80帧降至仅8帧。在REDS等基准上，稀疏注意力以13.6%的计算量实现了与全注意力几乎持平的重建质量（PSNR仅下降0.54 dB），而局部约束注意力在超高分辨率下将PSNR从24.21提升至24.87，有效消除了重复纹理。用户研究进一步验证了其在感知质量上的竞争力。

FlashVSR首次将单步蒸馏、流式训练范式与局部约束稀疏注意力统一于扩散式VSR，为实时高分辨率视频增强提供了可行路径。项目代码与模型将开源。

## 背景与动机

### 扩散模型在视频超分辨率中的潜力与瓶颈

视频超分辨率（Video Super-Resolution, VSR）旨在从低分辨率（Low-Resolution, LR）视频帧中重建高保真的高分辨率（High-Resolution, HR）输出，是视频增强、云游戏、流媒体传输等应用中的核心任务。近年来，扩散模型凭借其强大的生成先验，在图像和视频恢复中展现出卓越的感知质量，但其高昂的计算开销和推理延迟严重制约了实际部署，尤其是在需要实时处理的流式场景中。

现有扩散式VSR方法面临三重瓶颈：

1. **多步扩散的高延迟**：主流扩散VSR模型（如 **Upscale-A-Video** (Zhou et al., 2024)、**STAR** (Xie et al., 2025)）依赖数十步迭代去噪，推理时间动辄数十秒，难以满足实时性要求。即便是目前最快的单步扩散基线 **SeedVR2-3B** (Wang et al., 2025a)，在768×1408分辨率下也仅能达到约1.44 FPS，距离实时处理（≥16 FPS）仍有数量级差距。

2. **训练-推理分辨率失配**：扩散模型通常在固定分辨率下训练，当推理时遇到更高分辨率的视频时，位置编码范围超出训练分布，导致重复纹理、模糊等严重伪影。这一问题在超高分辨率（如4K）场景下尤为突出，限制了模型的泛化能力。

3. **流式处理的设计空白**：传统分块（chunk-wise）处理方法需要缓存整个视频片段（约80帧）才能开始处理，引入巨大的前瞻延迟（lookahead latency），无法适应在线直播、视频会议等低延迟应用场景。而现有的流式视频扩散训练范式（如Teacher Forcing、Self-Forcing）在训练和推理之间存在输入分布不一致的间隙，导致性能退化。

### 核心洞察：VSR任务的独特条件结构

FlashVSR的关键洞察在于识别了VSR与视频生成之间的本质差异。在视频生成任务中，模型需要从噪声中合成全新的运动模式，因此依赖先前预测的干净隐变量来维持运动合理性。然而，VSR任务的强条件来自低分辨率帧本身——模型的核心职责是内容重建而非运动合成。这意味着：

- **历史干净隐变量并非必需**：LR帧已经提供了足够的结构信息来约束当前帧的重建，无需将先前预测的HR隐变量作为输入。
- **KV-cache可替代显式帧传递**：通过缓存Transformer后期层的键值对（KV-cache），可以在不引入训练-推理间隙的前提下传递干净特征，维持时间连续性。

基于这一洞察，FlashVSR设计了一种全新的并行训练范式：训练和推理阶段均仅依赖LR帧和噪声隐变量作为输入，彻底消除了传统流式方法中因串行依赖导致的分布偏移问题。

### 本文动机与目标

综上所述，本文的核心动机在于填补扩散式VSR在实时流式处理方面的空白，具体目标包括：

- **速度突破**：通过单步蒸馏将扩散推理压缩至一步，实现近实时（≥16 FPS）的高分辨率VSR。
- **流式友好设计**：构建因果注意力机制和KV-cache架构，将前瞻延迟从数十帧降至个位数帧，适配在线应用。
- **分辨率泛化**：引入局部约束注意力，对齐训练与推理的位置编码范围，消除超高分辨率下的伪影。
- **端到端效率优化**：设计轻量条件解码器，大幅降低VAE解码的计算瓶颈，同时保持重建质量。

这些目标共同驱动了FlashVSR的三阶段蒸馏框架和配套的系统优化策略，使其成为首个面向实时流式处理的单步扩散VSR方法。

## 核心创新

FlashVSR 的核心创新并非单一算法突破，而是围绕**实时流式扩散 VSR** 这一目标，对扩散模型推理管线进行系统性的效率重构。其关键创新可归纳为四个相互耦合的 changed slots。

### 1. 单步扩散蒸馏：从多步采样到一步生成

传统扩散式 VSR 依赖多步去噪（如 **Upscale-A-Video** 的 30 步、**STAR** 的 15 步），推理延迟与步数成正比。FlashVSR 通过三阶段蒸馏将模型压缩为单步模型：

- **Stage 1**：在 WAN2.1 1.3B 预训练视频扩散模型基础上进行视频-图像联合超分训练，构建强教师模型；
- **Stage 2**：引入因果遮罩和块稀疏注意力，适配流式推理；
- **Stage 3**：采用分布匹配蒸馏（DMD）结合流匹配损失和像素空间重建损失（L2 + LPIPS），将 Stage 2 的稀疏因果 DiT 精炼为单步学生模型。

蒸馏总损失为：

$$\mathcal { L } = \underbrace { \mathcal { L } _ { \mathrm { D M D } } ( z _ { \mathrm { p r e d } } , G _ { \mathrm { o n e } } , G _ { \mathrm { r e a l } } , G _ { \mathrm { f a k e } } ) } _ { \mathrm { d i s t r i b u t i o n - m a c h i n g ~ d i s t i l a t i o n } } + \underbrace { \mathcal { L } _ { \mathrm { F M } } ( z _ { \mathrm { p r e d } } , G _ { \mathrm { f a k e } } ) } _ { \mathrm { f l o w ~ m a c h i n g } } + \underbrace { { \| x _ { \mathrm { p r e d } } - x _ { \mathrm { g t } } \| _ { 2 } ^ { 2 } } + \lambda \mathcal { L } _ { \mathrm { l p i p s } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { g t } } ) } _ { \mathrm { d e c o d e r ~ r e c o n s t r u c t i o n } }$$

这一设计使 FlashVSR 在 768×1408 分辨率下达到 **16.92 FPS**，相比最优单步扩散基线 **SeedVR2-3B**（Wang et al., 2025a）的 1.44 FPS 加速约 **11.8 倍**（Table 2）。

### 2. 并行训练范式：消除训练-推理间隙

现有流式视频扩散模型的训练通常采用 Teacher Forcing 或 Student Forcing，将先前预测的干净隐变量作为后续帧的条件输入。FlashVSR 的核心洞察在于：**VSR 任务的强条件来自低分辨率帧，模型的核心任务是内容重建而非运动合成，因此无需将历史预测的干净隐变量作为输入**。

基于此，FlashVSR 设计了并行训练范式：训练和推理阶段均仅依赖低分辨率输入和噪声隐变量，通过 KV-cache 传递后期层的干净特征来维持时间连续性。这一设计消除了训练与推理之间的输入分布差异，使模型能够完全并行训练，同时将前瞻延迟从块处理方法的约 80 帧降至仅 **8 帧**，适合在线流式应用。

### 3. 块稀疏因果注意力 + 局部窗口约束

全时空密集注意力是扩散模型推理的主要计算瓶颈。FlashVSR 引入了两层稀疏化策略：

- **块稀疏因果注意力**：将注意力限制在因果时间窗口内的空间块中，使注意力计算量降至全注意力的 **13.6%**，推理时间从每 8 帧 1.105 秒降至 0.355 秒（**3.1 倍加速**），PSNR 仅从 24.65 降至 24.11，质量几乎无损（Table 3）。

- **局部约束注意力**：针对超高分辨率（如 1536×2688）下训练-推理位置编码范围失配导致的重复纹理和模糊伪影，将每个查询的注意力范围限制在局部空间邻域内。消融实验表明，Boundary-Preserved 策略将 PSNR 从全局注意力的 24.21 提升至 **24.87**，感知指标亦显著改善（Table 5）。

注意力掩码的片段约束形式为：

$$\alpha_{ij} = \frac { \exp \left( \frac { q_i k_j ^ { \top } } { \sqrt { d } } \right) \mathbf { 1 } [ \mathrm { s e g } ( i ) = \mathrm { s e g } ( j ) ] } { \sum _ { l } \exp \left( \frac { q_i k_l ^ { \top } } { \sqrt { d } } \right) \mathbf { 1 } [ \mathrm { s e g } ( i ) = \mathrm { s e g } ( l ) ] }$$

### 4. 轻量条件解码器（TC Decoder）

原始 3D VAE 解码器（Wan decoder）是推理管线的另一瓶颈：对 101 帧 768×1408 视频解码耗时 11.13 秒。FlashVSR 设计的 TC Decoder 以低分辨率帧为条件输入，结合隐变量进行重建，解码时间降至 **1.60 秒**（约 **7 倍加速**），PSNR 从 32.58 降至 31.08，质量下降有限（Table 4）。其训练损失同时监督真实图像和原始 VAE 解码器输出：

$$\mathcal { L } = \Vert x _ { \mathrm { p r e d } } - x _ { \mathrm { g t } } \Vert _ { 2 } ^ { 2 } + \lambda \mathcal { L } _ { \mathrm { L P I P S } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { g t } } ) + \Vert x _ { \mathrm { p r e d } } - x _ { \mathrm { w a n } } \Vert _ { 2 } ^ { 2 } + \lambda \mathcal { L } _ { \mathrm { L P I P S } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { w a n } } )$$

在相同参数量下，条件设计优于无条件变体（PSNR 31.08 vs 29.96），验证了 LR 帧作为辅助条件对轻量解码器重建质量的关键作用。

### 创新耦合与系统效应

上述四个 changed slots 并非孤立优化，而是形成正向耦合：单步蒸馏降低去噪步数，并行训练消除串行依赖，稀疏注意力压缩单步计算量，TC Decoder 加速像素空间重建。最终，FlashVSR 在单张 A100 上以 **17 FPS** 处理 768×1408 视频，峰值显存仅 **11.13 GB**（SeedVR2-3B 为 52.88 GB），节省约 **78.9%**，首次将扩散式 VSR 推至实时流式处理的门槛。

## 整体框架

FlashVSR 的整体框架围绕**三阶段蒸馏**构建，将预训练视频扩散模型逐步转化为可实时流式推理的单步超分辨率系统。图 2 给出了端到端的训练与推理流程。

### 核心设计理念

与视频生成不同，VSR 任务的强条件来自低分辨率（LR）帧——模型的核心任务是内容重建而非运动合成。因此，FlashVSR **无需将先前预测的干净隐变量作为输入**，仅依赖 LR 帧和噪声隐变量即可维持时间连续性。这一洞察消除了训练与推理之间的架构间隙，使得**并行训练**成为可能：训练时所有帧可独立前向传播，推理时通过 KV-cache 传递后期层的干净特征来隐式对齐帧间内容。

### 三阶段蒸馏流水线

**Stage 1 — 视频-图像联合超分训练**：以预训练视频扩散模型 WAN2.1 1.3B 为起点，在自建数据集 VSR-120K 上进行视频与图像的联合训练。该阶段使用分块对角片段注意力掩码（公式 1），限制注意力在同一图像或视频片段内交互，建立强教师模型。

**Stage 2 — 块稀疏因果注意力适配**：为适配流式推理，将 Stage 1 的全注意力 DiT 改造为稀疏因果 DiT。核心改动包括：引入因果遮罩（确保当前帧仅关注历史帧）、采用块稀疏注意力模式（以 13.6% 的稀疏度实现 3.1 倍加速）、以及局部约束注意力（将查询限制在局部空间窗口内，对齐训练与推理的位置编码范围，消除超高分辨率下的重复伪影）。因果 LR 投影层（图 6）使用 2D pixel-shuffle 和 3D 因果卷积，配合因果缓存实现流式处理。

**Stage 3 — 分布匹配单步蒸馏**：将 Stage 2 的稀疏因果 DiT 精炼为单步模型。损失函数由三部分组成（公式 2）：分布匹配蒸馏损失 $\mathcal{L}_{\mathrm{DMD}}$、流匹配损失 $\mathcal{L}_{\mathrm{FM}}$，以及像素空间重建损失（L2 + LPIPS）。蒸馏后的单步模型 $G_{\mathrm{one}}$ 直接一步生成高分辨率隐变量。

### 轻量条件解码器（TC Decoder）

为加速 VAE 解码瓶颈，FlashVSR 设计了以 LR 帧为条件的轻量解码器（图 4）。TC Decoder 不仅接收 DiT 输出的隐变量，还将 LR 帧作为辅助条件输入，通过混合监督训练（公式 3）：同时蒸馏原始 Wan 解码器输出和真实图像，组合 L2 与 LPIPS 损失（λ=2）。在 768×1408 分辨率下，TC Decoder 解码 101 帧仅需 1.60 秒，约为原始 Wan 解码器的 1/7，且质量损失极小。

### 流式推理流程

推理时，FlashVSR 以流式方式逐帧处理，仅引入 8 帧前瞻延迟（对比分块方法的约 80 帧）。每帧推理遵循：

$$z_t = G_{\mathrm{one}}(\mathrm{LR}_t, \epsilon_t; \mathrm{KV}_{<t})$$

单步模型 $G_{\mathrm{one}}$ 以当前 LR 帧和噪声隐变量为输入，利用缓存的键值对 $\mathrm{KV}_{<t}$ 整合历史上下文，生成当前帧的高分辨率隐变量 $z_t$，再经 TC Decoder 解码为最终输出帧。KV-cache 在后期层传递干净特征，隐式维持时间一致性，无需显式输入历史预测帧。

### 补充图表

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the three-stage training pipeline of FlashVSR, covering video–image joint SR training, adaptation with block-sparse causal attention for streaming inference, and distributionmatching one-step distillation combined with reconstruction supervision*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/012_Figure_7.jpg]]
*Figure 7: Illustration of the sink attention effect in specific attention heads*

## 核心模块与公式推导

### 三阶段蒸馏流水线

FlashVSR 的核心训练流程分为三个阶段，逐步将预训练视频扩散模型压缩为单步流式推理模型。

**Stage 1：视频-图像联合超分训练。** 以预训练视频扩散模型 WAN2.1 1.3B 为基础，在 VSR-120K 数据集上进行视频与图像的联合训练。此阶段采用分块对角片段注意力掩码（block-diagonal segment mask），将注意力限制在同一图像或视频片段内部：

$$
\alpha_{ij} = \frac { \exp \left( \frac { q_i k_j ^ { \top } } { \sqrt { d } } \right) \mathbf { 1 } [ \mathrm { s e g } ( i ) = \mathrm { s e g } ( j ) ] } { \sum _ { l } \exp \left( \frac { q_i k_l ^ { \top } } { \sqrt { d } } \right) \mathbf { 1 } [ \mathrm { s e g } ( i ) = \mathrm { s e g } ( l ) ] }
$$

其中 $q_i$、$k_j$ 分别为查询和键向量，$d$ 为特征维度，$\mathbf{1}[\mathrm{seg}(i) = \mathrm{seg}(j)]$ 为片段身份指示函数，确保注意力仅在相同片段内计算。该阶段产出全注意力教师模型。

**Stage 2：块稀疏因果注意力适配。** 将 Stage 1 的全注意力 DiT 改造为稀疏因果 DiT（Sparse-Causal DiT）。核心改动包括引入因果遮罩（causal masking）和块稀疏注意力（block-sparse attention），使模型仅依赖当前及历史帧的信息，适配流式推理的因果约束。

**Stage 3：分布匹配单步蒸馏。** 将 Stage 2 的稀疏因果 DiT 精炼为单步模型。总损失函数为：

$$
\mathcal { L } = \underbrace { \mathcal { L } _ { \mathrm { D M D } } ( z _ { \mathrm { p r e d } } , G _ { \mathrm { o n e } } , G _ { \mathrm { r e a l } } , G _ { \mathrm { f a k e } } ) } _ { \mathrm { d i s t r i b u t i o n - m a c h i n g ~ d i s t i l a t i o n } } + \underbrace { \mathcal { L } _ { \mathrm { F M } } ( z _ { \mathrm { p r e d } } , G _ { \mathrm { f a k e } } ) } _ { \mathrm { f l o w ~ m a c h i n g } } + \underbrace { { \| x _ { \mathrm { p r e d } } - x _ { \mathrm { g t } } \| _ { 2 } ^ { 2 } } + \lambda \mathcal { L } _ { \mathrm { l p i p s } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { g t } } ) } _ { \mathrm { d e c o d e r ~ r e c o n s t r u c t i o n } }
$$

其中 $z_{\mathrm{pred}}$ 为预测隐变量，$G_{\mathrm{one}}$ 为单步生成器，$G_{\mathrm{real}}$ 和 $G_{\mathrm{fake}}$ 为判别器特征。第一项 $\mathcal{L}_{\mathrm{DMD}}$ 为分布匹配蒸馏损失，迫使单步模型输出分布逼近教师模型；第二项 $\mathcal{L}_{\mathrm{FM}}$ 为流匹配损失，提供额外的训练信号；第三项为像素空间重建损失，由 L2 距离和 LPIPS 感知损失组成，直接监督解码后的图像质量。

---

### 局部约束稀疏注意力

超高分辨率下，推理时空间分辨率超出训练阶段位置编码的有效范围，导致重复纹理或模糊等伪影。局部约束稀疏注意力（Locality-Constrained Sparse Attention）通过将每个查询的注意力范围限制在局部空间邻域内，使训练与推理的位置编码范围保持一致。

具体实现提供两种局部窗口规则：
- **边界截断（Boundary-Truncated）**：严格将注意力限制在固定窗口内，超出部分的 token 直接丢弃。
- **边界保留（Boundary-Preserved）**：在窗口边界处保留与边界 token 的交互，避免边缘信息丢失。

最终的稀疏注意力掩码在因果掩码与局部窗口掩码的交集上计算。消融实验表明，Boundary-Preserved 策略在 PSNR 上从全局注意力的 24.21 提升至 24.87，感知指标亦显著改善。

---

### 轻量条件解码器（TC Decoder）

原始 VAE 解码器（Wan decoder）在 101 帧 768×1408 视频上解码耗时 11.13 秒，成为推理瓶颈。TC Decoder 以低分辨率帧为条件输入，与隐变量联合驱动重建，在仅 1.60 秒内完成解码（约 7 倍加速）。

训练损失同时监督真实图像和原始 VAE 解码器输出：

$$
\mathcal { L } = \Vert x _ { \mathrm { p r e d } } - x _ { \mathrm { g t } } \Vert _ { 2 } ^ { 2 } + \lambda \mathcal { L } _ { \mathrm { L P I P S } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { g t } } ) + \Vert x _ { \mathrm { p r e d } } - x _ { \mathrm { w a n } } \Vert _ { 2 } ^ { 2 } + \lambda \mathcal { L } _ { \mathrm { L P I P S } } ( x _ { \mathrm { p r e d } } , x _ { \mathrm { w a n } } )
$$

其中 $x_{\mathrm{pred}}$ 为 TC Decoder 输出，$x_{\mathrm{gt}}$ 为真实高清帧，$x_{\mathrm{wan}}$ 为原始 VAE 解码器输出，$\lambda=2$。前两项为对真实图像的监督，后两项为对教师解码器的蒸馏。消融显示，同等参数量下，条件设计相比无条件变体 PSNR 从 29.96 提升至 31.08，验证了 LR 条件信号的关键作用。

---

### 因果 LR 投影层与 KV-cache 机制

**因果 LR 投影层（Causal LR Projection-In Layer）** 使用 2D pixel-shuffle 和 3D 因果卷积（CausalConv），将低分辨率输入帧映射到 DiT 的隐空间。因果卷积配合因果缓存（causal cache）确保每帧仅依赖历史信息，支撑流式处理。

**KV-cache 机制** 是流式推理的关键设计。核心洞察在于：与视频生成不同，VSR 任务受低分辨率帧的强条件约束，模型的核心任务是内容重建而非运动合成，因此无需将先前预测的干净隐变量作为输入。FlashVSR 通过缓存历史帧的键值对（KV-cache），在后期层传递干净特征以维持时间连续性，从而消除训练-推理间隙：

$$
z_t = G_{\mathrm{one}}(\mathrm{LR}_t, \epsilon_t; \mathrm{KV}_{<t})
$$

其中 $z_t$ 为当前帧的预测隐变量，$\mathrm{LR}_t$ 为当前低分辨率帧，$\epsilon_t$ 为噪声，$\mathrm{KV}_{<t}$ 为缓存的历史键值对。此设计使训练和推理均可仅依赖低分辨率帧和噪声隐变量，支持高效的并行训练，同时将前瞻延迟从传统分块方法的约 80 帧降至仅 8 帧。

### 补充图表

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/004_Figure_4.jpg]]
*Figure 4: Training pipeline of the TC Decoder*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/011_Figure_6.jpg]]
*Figure 6: Architecture of the Causal LR Projection-In Layer*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/003_Figure_3.jpg]]
*Figure 3: Locality-Constrained Sparse Attention. Left: At ultra-high resolutions, performing inference beyond the trained positional encoding range produces artifacts (e.g., repetition or blur). Restricting each query to a local attention window keeps the positional encoding range consistent between training and inference, thereby preventing artifacts. Right: Two local window rules, namely boundary-preserved and boundary-truncated, are illustrated. The final sparse attention mask is computed within these local masks*

## 实验与分析

### 主实验结果

FlashVSR 在多个合成与真实世界基准上进行了定量评估，涵盖 YouHQ40、REDS、SPMCS（合成退化）、VideoLQ（真实退化）和 AIGC30（AIGC 退化）五个数据集（Table 1）。在感知质量指标（MUSIQ、CLIPIQA、DOVER）上，FlashVSR 在所有数据集上一致优于对比方法，体现了扩散模型在纹理生成和细节恢复上的优势。在重建指标（PSNR/SSIM）上，FlashVSR 在多数数据集上取得最优或次优结果，与专门优化的回归式方法相比差距较小。

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison on YouHQ40, REDS, SPMCS (synthetic), VideoLQ (real) and AIGC30 (AIGC). Best in red, second-best in blue*

效率方面（Table 2），FlashVSR 在单张 A100 GPU 上处理 101 帧 768×1408 视频时，**Ours-Tiny** 配置仅需 5.97 秒，对应 **16.92 FPS**，接近实时推理门槛。相比之下，多步扩散模型 **Upscale-A-Video**（Zhou et al., 2024）需 30 步推理，耗时 811.83 秒（约 136 倍加速）；**STAR**（Xie et al., 2025）需 15 步，耗时 680.42 秒（约 114 倍加速）；单步扩散模型 **SeedVR2-3B**（Wang et al., 2025a）需 70.36 秒（约 11.8 倍加速）。峰值显存方面，Ours-Tiny 仅占用 **11.13 GB**，而 SeedVR2-3B 高达 52.88 GB，节省约 **78.9%**。

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/006_Table_2.jpg]]
*Table 2: Efficiency comparison (peak memory, runtime, and parameters) on*

流式处理模式下，FlashVSR 的前瞻延迟仅为 **8 帧**，而传统分块方法（如 STAR 的 32 帧，其他方法的约 80 帧）需等待完整片段才能输出，这使得 FlashVSR 更适合在线应用场景。

用户研究（Table 7）采用盲评 GSB 测试，覆盖五个单步 VSR 模型在 32 个测试集（含真实与 AIGC 退化视频）上的表现。FlashVSR 在总体质量、视频保真度和视频质量三个维度上均获得最高偏好分数，验证了其感知质量优势。

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/018_Table_7.jpg]]
*Table 7: User study results (GSB scores, in %) for five one-step VSR models on 32 test sets, including both real-world and AIGC-degraded videos. Higher values indicate stronger user preference*

### 消融实验

**稀疏注意力消融**（Table 3）：将全注意力替换为 13.6% 稀疏度的块稀疏因果注意力后，PSNR 从 24.65 降至 24.11（下降 0.54 dB），SSIM 从 0.6630 降至 0.6511，LPIPS 从 0.3320 升至 0.3432，质量基本持平。但推理时间从每 8 帧 1.105 秒降至 0.355 秒，实现 **3.1 倍加速**，验证了稀疏注意力在效率与质量之间的有效平衡。

**局部约束注意力消融**（Table 5）：在超高分辨率（1536×2688）下，全局注意力因训练-推理位置编码范围失配产生重复纹理和模糊伪影，PSNR 仅为 24.21。引入局部窗口约束后，**Boundary-Truncated** 和 **Boundary-Preserved** 两种策略在所有指标上均优于全局注意力，其中 Boundary-Preserved 取得最优 PSNR **24.87**，感知指标（LPIPS、DISTS）亦显著改善。这证实了局部约束注意力是弥合训练-推理分辨率差距的关键机制。

**轻量条件解码器消融**（Table 4）：TC Decoder 在相同参数量下显著优于无条件轻量解码器（PSNR 31.08 vs 29.96），验证了以低分辨率帧作为条件输入的有效性。与原始 Wan VAE 解码器相比，TC Decoder 的 PSNR 从 32.58 降至 31.08（下降约 1.5 dB），但解码时间从 11.13 秒降至 1.60 秒，实现约 **7 倍加速**，以较小的保真度代价换取了显著的效率提升。

**KV-cache 驱逐策略消融**（Table 6）：对比滑动窗口、均匀驱逐和头部独立驱逐三种策略。滑动窗口策略取得最优 PSNR 24.11。均匀驱逐策略 PSNR 为 24.31，与滑动窗口接近但无显著改进。头部独立驱逐策略因注意力头中的沉没效应（sink attention effect，见 Figure 7）导致性能显著下降，PSNR 降至 23.61，说明某些注意力头对全局上下文高度敏感，不可简单驱逐。

### 失败模式与局限性

1. **TC 解码器的重建精度损失**：TC Decoder 在 PSNR 上比原始 VAE 解码器低约 1.5 dB，在需要精确像素还原的场景（如文字、细线结构）中可能出现可察觉的模糊或失真。这是轻量化设计的内在权衡。

2. **超高分辨率下的伪影残留**：虽然局部约束注意力有效抑制了重复纹理和模糊，但在极端分辨率（如 4K）下，窗口大小与位置编码范围的匹配仍需谨慎调参，否则仍可能出现边界处的伪影。

3. **固定文本提示的局限**：模型采用固定文本提示进行条件生成，无法根据视频内容动态调整。对于场景类型差异较大的视频（如夜景与日景交替），固定提示可能导致局部区域的纹理风格不匹配。动态提示可能进一步提升感知质量，但需额外设计提示选择或生成机制。

4. **KV-cache 管理的优化空间**：头部独立驱逐策略的失败表明当前的缓存管理方法尚未充分利用注意力头的特性差异。更精细的逐头缓存策略（如基于注意力权重的自适应驱逐）可能进一步压缩显存而不损失质量。

5. **训练资源消耗**：三阶段蒸馏流程需 32 张 A100 GPU 和数天训练时间，对资源受限的研究者构成一定门槛。模型压缩（量化、剪枝）与轻量化架构设计是未来降低训练和部署成本的方向。

### 补充图表

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/007_Table_3.jpg]]
*Table 3: Sparse vs. Full Attention*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/008_Table_4.jpg]]
*Table 4: Ablation of tiny conditional decoder*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/010_Table_5.jpg]]
*Table 5: Ablation of Locality-constrained Attention. Both Boundary-Truncated and Boundary-Preserved outperform Global Attention across all metrics. Best in red, second-best in blue*

![[assets/figures/papers/paper_list_l873_https_arxiv_org_abs_2510_12747/figures/013_Table_6.jpg]]
*Table 6: Quantitative results of different KV-cache eviction strategies on the REDS dataset*

## 方法谱系与知识库定位

### 1. 任务定位与核心瓶颈

FlashVSR 面向的是**实时扩散式流式视频超分辨率（Streaming VSR）**任务。现有扩散式 VSR 模型面临三重瓶颈：

1. **推理延迟高**：多步扩散采样（如 15–30 步）导致单帧处理时间远超实时要求。
2. **内存开销大**：全时空注意力随帧数和分辨率平方级增长，峰值显存可达 50 GB 以上。
3. **训练-推理分辨率失配**：模型在固定分辨率下训练，在高分辨率推理时位置编码范围溢出，产生重复纹理和模糊伪影。

这些瓶颈使扩散式 VSR 难以部署到在线流式场景。FlashVSR 的核心洞察在于：**VSR 的强条件来自低分辨率帧，模型的任务是内容重建而非运动合成，因此无需将先前预测的干净隐变量作为输入**。这一洞察从根本上改变了流式扩散模型的训练范式。

### 2. 与基线方法的关系

#### 2.1 扩散式 VSR 谱系

FlashVSR 在扩散式 VSR 方法谱系中处于**单步蒸馏 + 流式推理**的交汇点。其直接对比的基线包括：

- **SeedVR2-3B**（Wang et al., 2025a）：当前最强的单步扩散 VSR 基线，采用分块处理（chunk-wise）模式，推理延迟约 80 帧。FlashVSR 在效率上实现约 12 倍加速，峰值显存从 52.88 GB 降至 11.13 GB，同时将前瞻延迟从约 80 帧压缩至 8 帧。
- **DOVE**（Chen et al., 2025b）：开源单步 VSR 基线，FlashVSR 在感知质量指标（MUSIQ、CLIPIQA、DOVER）上一致优于 DOVE。
- **STAR**（Xie et al., 2025）：扩散 VSR 模型，FlashVSR 在速度上实现约 114 倍加速。
- **Upscale-A-Video**（Zhou et al., 2024）：基于流引导的多步扩散 VSR（30 步），FlashVSR 实现约 136 倍加速。

#### 2.2 流式训练范式的突破

传统流式视频扩散模型的训练范式存在严重的训练-推理间隙：

- **Teacher Forcing**：训练时使用真实历史帧，推理时使用预测帧，误差累积严重。
- **Student Forcing / AAPT**：训练时使用自身预测的历史帧，但需串行生成，无法并行训练，效率极低。

FlashVSR 的关键创新在于**并行训练范式**：由于 VSR 任务中低分辨率帧提供强条件，模型无需依赖历史预测的干净隐变量。训练时仅使用低分辨率帧和噪声隐变量，推理时通过 KV-cache 传递后期层的干净特征维持时间连续性。这一设计使训练完全可并行，同时消除了训练-推理间隙。

### 3. 技术组件与方法定位

FlashVSR 构建在一个三阶段蒸馏框架之上，每个阶段对应特定的方法贡献：

| 阶段 | 方法组件 | 解决的问题 | 与现有工作的关系 |
|------|---------|-----------|----------------|
| Stage 1 | 视频-图像联合超分训练 | 建立强教师模型 | 继承 WAN2.1 1.3B 预训练权重，引入分块对角片段注意力掩码 |
| Stage 2 | 块稀疏因果注意力 | 适配流式推理，降低计算开销 | 将全注意力替换为 13.6% 稀疏度的因果注意力，3.1 倍加速 |
| Stage 3 | 分布匹配单步蒸馏 | 实现单步生成 | 结合 DMD 蒸馏、流匹配损失和像素空间重建损失 |

在推理侧，两个关键组件进一步弥合效率-质量间隙：

- **局部约束稀疏注意力**：将每个查询的注意力范围限制在局部窗口内，使推理时的位置编码范围与训练对齐。在高分辨率（1536×2688）下，PSNR 从全局注意力的 24.21 提升至边界保留模式的 24.87，有效消除重复伪影。
- **轻量条件解码器（TC Decoder）**：以低分辨率帧为条件的轻量解码器，解码速度约为原始 Wan VAE 解码器的 1/7（1.60s vs 11.13s），PSNR 仅下降约 1.5 dB。

### 4. 适用边界与局限

FlashVSR 的适用边界和局限可从以下几个维度审视：

1. **分辨率边界**：论文验证的最高分辨率为 768×1408（17 FPS）和 1536×2688。在 4K 及以上分辨率下，局部约束注意力的窗口大小与位置编码范围的平衡关系尚待验证，可能需重新设计窗口策略。

2. **资源需求**：训练需 32 张 A100 GPU 和数天时间，对学术复现构成一定门槛。推理端显存已压缩至 11.13 GB，但仍需高端 GPU（A100），尚未适配消费级或边缘设备。

3. **质量权衡**：TC Decoder 在 PSNR 上较原始 VAE 解码器低约 1.5 dB（31.08 vs 32.58），在需要极高保真度的场景（如医学影像）可能不适用。

4. **固定文本提示**：模型使用固定文本提示进行条件生成，无法针对不同场景（如夜景、运动场景）自适应调整。动态提示可能进一步提升感知质量，但尚未探索。

5. **KV-cache 管理**：头部独立的驱逐策略因注意力头中的沉没效应（sink attention effect）而失败，当前滑动窗口策略虽有效，但缓存管理仍有优化空间——均匀驱逐无改进，头部独立驱逐反而下降（PSNR 23.61 vs 24.11）。

6. **数据集依赖**：训练依赖自建的 VSR-120K 数据集，模型在分布外退化类型上的泛化能力未经充分验证。真实世界测试仅覆盖 VideoLQ 和 AIGC30 两个数据集。

### 5. 开放问题

1. **模型压缩与边缘部署**：能否通过量化、剪枝或知识蒸馏进一步压缩模型，使其适配移动端或边缘设备？当前 11 GB 显存仍是部署瓶颈。

2. **不规则稀疏注意力**：当前采用规则的块稀疏模式，能否设计内容自适应的不规则稀疏注意力，在保持速度的同时进一步提升质量？

3. **场景自适应提示**：引入基于场景内容的自适应动态文本提示，能否在感知质量（如 MUSIQ、DOVER）上获得显著提升？

4. **4K 实时性**：在 4K 分辨率下，局部约束注意力的窗口大小需如何调整？是否需要分层注意力或渐进式超分策略来维持实时性？

5. **缓存驱逐策略优化**：鉴于沉没效应的存在，能否设计注意力头感知的混合驱逐策略（如保留沉没头、驱逐非沉没头），在更低的缓存占用下维持质量？

6. **多帧融合上限**：当前流式设计仅缓存 8 帧历史信息，更长的时间窗口（如 16 或 32 帧）是否能带来质量增益？增益的边际递减点在哪里？

7. **跨退化类型泛化**：在不同于 RealBasicVSR 退化管线的真实世界退化（如压缩伪影、传感器噪声）上，模型的鲁棒性如何？是否需要退化感知的条件注入？

## 原文 PDF

![[paperPDFs/CVPR_2026/FlashVSR_Towards_Real_time_Diffusion_Based_Streaming_Video_Super_Resolution.pdf]]
