---
title: "InstantViR: Real-Time Video Inverse Problem Solver with Distilled Diffusion Prior"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InstantViR_Real_Time_Video_Inverse_Problem_Solver_with_Distilled_Diffusion_Prior.pdf
project_link: "https://ai4scientificimaging.org/instantvir"
code_link: null
aliases:
- II
- InstantViR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将双向视频扩散先验蒸馏为一步式因果自回归学生网络，通过摊销变分推断消除迭代采样，从而实现实时重建。
primary_logic: 利用教师-学生知识蒸馏框架，在无需配对训练数据的情况下，将强大视频扩散模型的时间一致性先验压缩进一个前馈网络；结合因果注意力与KV缓存实现流式处理，并通过教师空间正则化蒸馏引入高效VAE，大幅降低延迟。
claims:
- InstantViR在A100 GPU上超过35 FPS，比采样基线SVI快超过100倍，同时保持或超越扩散基线的重建质量。
- 训练无需外部配对干净/降质视频数据，仅依靠教师扩散模型与已知退化算子。
- 因果自回归架构与KV缓存使得视频流式推理成为可能。
- 教师空间正则化蒸馏将高效LeanVAE无缝集成到教师扩散先验中。
---

# InstantViR: Real-Time Video Inverse Problem Solver with Distilled Diffusion Prior

> [!tip] 核心洞察
> 利用教师-学生知识蒸馏框架，在无需配对训练数据的情况下，将强大视频扩散模型的时间一致性先验压缩进一个前馈网络；结合因果注意力与KV缓存实现流式处理，并通过教师空间正则化蒸馏引入高效VAE，大幅降低延迟。

| 字段 | 内容 |
|------|------|
| 中文题名 | InstantViR：基于蒸馏扩散先验的实时视频逆问题求解器 |
| 英文题名 | InstantViR: Real-Time Video Inverse Problem Solver with Distilled Diffusion Prior |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.14208) · [Project](https://ai4scientificimaging.org/instantvir) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InstantViR / InstantViR† |
| Dataset | Video Inpainting, Video Deblurring, Video Super-Resolution, Inference Speed |

> [!tip] 效果简介
> - Video Inpainting (50% mask) 上，PSNR ↑ 30.54；SSIM ↑ 0.97；LPIPS ↓ 0.12。
> - Video Deblurring 上，FVD ↓ 110.51 (InstantViR) / 103.45 (InstantViR†)。
> - Video Super-Resolution (4×) 上，FVD ↓ 153.13 (InstantViR) / 156.43 (InstantViR†)。

## 概要

视频逆问题——如修复、去模糊和超分辨率——旨在从降质观测中恢复干净视频，其核心挑战在于同时满足**空间保真度**与**时间一致性**。传统方法依赖迭代扩散后验采样，虽能利用强大的视频扩散先验，但推理速度极慢，难以满足实时或流式应用需求；而基于图像扩散并外加强时间正则化的方案，则缺乏对复杂时空动态的建模能力，导致时间闪烁与不一致。

InstantViR 针对这一瓶颈提出了根本性的范式转换：**将双向视频扩散先验蒸馏为一步式因果自回归学生网络**，通过摊销变分推断消除迭代采样，从而实现实时重建。其核心洞察在于：利用教师-学生知识蒸馏框架，在无需配对训练数据的情况下，将强大视频扩散模型的时间一致性先验压缩进一个前馈网络；结合因果注意力与 KV 缓存实现流式处理，并通过教师空间正则化蒸馏引入高效 VAE，大幅降低延迟。

在 A100 GPU 上，InstantViR 以 832×480 分辨率实现超过 35 FPS 的推理速度，比采样基线 SVI 快超过 100 倍，同时在视频修复、去模糊和 4× 超分辨率等任务上保持或超越扩散基线的重建质量。该方法仅需教师扩散模型与已知退化算子即可训练，无需外部配对干净/降质视频数据，展现出极强的实用性与泛化潜力。

### 视频逆问题的核心挑战

视频逆问题旨在从退化的观测 $\pmb y$ 中恢复出干净的原始视频 $\pmb x$，其本质是一个病态的贝叶斯推断问题。根据贝叶斯公式，后验分布可以表示为：

$$p ( { \pmb x } | { \pmb y } ) \propto p ( { \pmb y } | { \pmb x } ) p ( { \pmb x } )$$

其中 $p ( { \pmb y } | { \pmb x } )$ 是似然项，编码了已知的退化过程（如模糊、掩码、下采样）；$p ( { \pmb x } )$ 是先验项，刻画了自然视频的时空统计规律。求解这一问题的难点在于：视频数据具有高维性和复杂的时空依赖结构，如何在保证重建质量的同时实现高效推理，始终是一个悬而未决的难题。

### 现有方法的两难困境

当前基于扩散模型的视频逆问题求解器大致分为两类，但各自存在显著瓶颈。

**迭代后验采样方法**通过逐步去噪来近似后验分布，能够利用强大的视频扩散先验获得高质量重建。这类方法在推理时需要对扩散模型进行多次迭代调用，例如 **SVI** 通过时间批处理施加一致性约束，**Vision-XL** 利用视频扩散先验进行迭代采样。然而，迭代过程带来的计算开销极大——以 SVI 为例，在 A100 GPU 上处理 832×480 分辨率的视频时，推理速度仅约 0.36 FPS，完全无法满足实时或流式应用的需求。

**基于图像扩散的快速方法**则试图规避视频扩散的计算负担，转而使用图像扩散模型逐帧重建，再通过时间正则化强行缝合帧间一致性。这类方法虽然推理速度较快，但由于缺乏对复杂时空动态的显式建模能力，往往导致时间维度上的闪烁、抖动和语义断裂等问题，难以保证重建视频的时间一致性。

### 核心瓶颈与本文动机

上述困境的根源在于一个根本性的权衡：**迭代视频扩散后验采样速度极慢，无法满足实时或流式应用需求；而基于图像扩散的强加时间正则化方法则缺乏对复杂时空动态的建模能力，导致时间不一致性。** 是否存在一种方法，既能继承视频扩散先验强大的时空建模能力，又能将推理速度提升至实时水平？

InstantViR 的核心洞察在于：**利用教师-学生知识蒸馏框架，在无需配对训练数据的情况下，将强大视频扩散模型的时间一致性先验压缩进一个前馈网络；结合因果注意力与 KV 缓存实现流式处理，并通过教师空间正则化蒸馏引入高效 VAE，大幅降低延迟。** 这一思路将视频扩散先验从“缓慢采样”的范式解放出来，转化为一步式的前馈映射，为实时视频逆问题求解开辟了新路径。

## 核心方法与创新机理

InstantViR 的核心创新在于将“迭代式视频扩散后验采样”重构为“单步摊销变分推理”，并通过三项关键设计（changed slots）将推理速度提升两个数量级，同时保持甚至超越扩散基线的重建质量。

### 推理范式：从迭代采样到单步摊销推理

传统视频逆问题方法（如 **DPS**、**SVI**、**Vision-XL**）依赖迭代后验采样（Iterative Posterior Sampling），需要在扩散模型的反向 SDE 上执行数百步去噪，每步都需计算分数网络并注入数据一致性梯度。这导致单帧处理时间以秒计，无法满足实时或流式需求。

InstantViR 将推理范式切换为**单步摊销变分推理**（Single-step Amortized Inference）。具体而言，它训练一个参数化求解器 $q_\phi(\mathbf{z}|\mathbf{y})$，将降质视频 $\mathbf{y}$ 直接映射到干净潜变量 $\mathbf{z}$，在单个前向传播中完成重建。这一设计的理论锚点是期望 KL 散度最小化：

$$\mathcal { L } = \mathbb { E } _ { \mathbf { y } \sim p ( \mathbf { y } ) } \Big [ D _ { \mathrm { K L } } \big ( q _ { \phi } ( \mathbf { x } | \mathbf { y } ) \| p ( \mathbf { x } | \mathbf { y } ) \big ) \Big ]$$

该目标被分解为数据保真项与先验正则化项，其中先验项通过教师扩散模型的分数匹配损失近似，从而在无需配对干净/降质视频数据的情况下完成蒸馏训练。

**效果**：在 A100 GPU 上，832×480 分辨率下，InstantViR 达到 13.91 FPS，InstantViR†（含 LeanVAE）达到 35.56 FPS，相比 SVI（约 0.36 FPS）实现超过 100 倍加速。

### 时间注意力：从全双向到块内双向＋块间因果

教师扩散模型使用**全双向时空注意力**（Bidirectional Spatiotemporal Attention），这要求处理完整视频序列，既无法流式推理，也导致计算复杂度随帧数平方增长。

InstantViR 将时间注意力重构为**块内双向＋块间因果注意力**（Intra-block Bidirectional + Inter-block Causal Attention）。视频被划分为长度为 $T$ 帧的时间块：

- **块内注意力**（Intra-block）：当前块内各帧之间进行双向自注意力，捕捉局部时空依赖：
  $$\mathrm { A t t } _ { \mathrm { i n t r a } } ( \mathbf { Q } _ { i } , \mathbf { K } _ { n } , \mathbf { V } _ { n } ) = \mathrm { s o f t m a x } \Bigg ( \frac { \mathbf { Q } _ { i } \mathbf { K } _ { n } ^ { \top } } { \sqrt { d _ { k } } } \Bigg ) \mathbf { V } _ { n }$$

- **块间注意力**（Inter-block）：当前块仅能关注过去块，形成因果约束：
  $${ \mathrm { A t t } } _ { { \mathrm { i n t e r } } } ( \mathbf { Q } _ { i } , \mathbf { K } _ { < n } , \mathbf { V } _ { < n } ) = { \mathrm { s o f t m a x } } \left( { \frac { \mathbf { Q } _ { i } \mathbf { K } _ { < n } ^ { \top } } { \sqrt { d _ { k } } } } \right) \mathbf { V } _ { < n }$$

结合标准的**自回归 KV 缓存**（KV Cache），历史块的键值对被存储并复用，将注意力复杂度从平方降至线性，理论上支持无限长度视频流式推理。这是 InstantViR 实现实时流式处理的关键架构创新。

### 特征 VAE：从 WanVAE 到 LeanVAE 的教师空间正则化蒸馏

教师扩散模型通常使用计算代价高昂的视频 VAE（如 WanVAE）进行潜空间编解码，这成为推理延迟的重要瓶颈。

InstantViR 引入**教师空间正则化蒸馏**（Teacher-Space Regularized Distillation），将高效的 LeanVAE 无缝集成到教师扩散先验中。核心挑战在于 LeanVAE 的潜空间 $\mathbf{z}'$ 与教师 VAE 的潜空间 $\mathbf{z}$ 并不对齐，直接替换会导致先验损失失效。

解决方案是构建一个可微分的“桥接”路径：将 LeanVAE 解码器 $\mathcal{D}'$ 的输出 $\hat{\mathbf{x}}_0$ 重新编码到教师潜空间 $\mathbf{z} = \mathcal{E}(\hat{\mathbf{x}}_0)$，在此空间中计算分数匹配损失：

$$\mathcal { L } \big ( q _ { \phi } ^ { \prime } \big ) = \mathbb { E } _ { y } \mathbb { E } _ { z ^ { \prime } \sim q _ { \phi } ^ { \prime } ( z ^ { \prime } \mid y ) } \big [ - \log p \big ( y \vert \mathcal { D } ^ { \prime } ( z ^ { \prime } ) \big ) \big ] + \mathbb { E } _ { t , \epsilon , z ^ { \prime } \sim q _ { \phi } ^ { \prime } ( \cdot \vert y ) } \Big [ w ( t ) \| s _ { \theta } ( z _ { t } , t ) - s _ { q ^ { \prime } } ( z _ { t } , t ) \| ^ { 2 } \Big ]$$

这一设计使得 InstantViR† 在保持重建质量的同时，将 FPS 从 13.91 进一步提升至 35.56，实现了实时推理。需要注意的是，LeanVAE 潜空间与教师潜空间尚未完全对齐，可能带来细微的重建质量损失——这是论文明确指出的局限性之一。

### 训练数据需求：无需配对数据

与许多需要大规模配对干净/降质视频数据的蒸馏方法不同，InstantViR 的蒸馏是**先验驱动**的：仅需要冻结的教师扩散模型 $s_\theta$ 和已知的退化算子 $\mathcal{A}$，不依赖外部配对数据。这使得框架可以灵活适配不同的逆问题任务（修复、去模糊、超分辨率），只需更换退化算子即可。

InstantViR 的核心设计思路是将一个强大的双向视频扩散先验（教师模型）蒸馏为一个单步因果自回归学生网络，从而在保持时间一致性的同时实现实时推理。整个框架围绕三个关键模块构建：冻结的教师扩散先验、可训练的摊销求解器，以及支持流式处理的因果注意力架构。

### 训练流程

训练阶段无需任何配对的干净/降质视频数据，仅依赖教师扩散模型与已知的退化算子。如图 2（上）所示，给定降质视频 $y$，摊销求解器 $q_\phi$ 以单步前馈方式直接输出干净潜变量 $z$。训练目标由两项组成：

1. **数据保真损失**：确保重建结果通过解码器 $\mathcal{D}$ 后与原始降质测量 $y$ 在观测空间上一致，即 $\mathbb{E}_{z \sim q_\phi(z|y)}[-\log p(y|\mathcal{D}(z))]$。
2. **先验蒸馏损失**：利用冻结的视频扩散先验 $s_\theta$（教师模型）对求解器输出的分布施加时间一致性和真实感约束。该损失通过分数匹配近似先验 KL 散度：

$$
\mathcal{L}_{\mathrm{prior}} \approx \mathbb{E}_{t, \epsilon, z \sim q_\phi(\cdot|y)} \big[ w(t) \| s_\theta(z_t, t) - s_{q_\phi}(z_t, t) \|^2 \big]
$$

其中 $s_\theta$ 为教师分数网络，$s_{q_\phi}$ 为辅助学生分数网络，二者在加噪潜变量 $z_t$ 上的分数差异被最小化。

整个训练目标源于最小化变分近似 $q_\phi(x|y)$ 与真实后验 $p(x|y)$ 之间的期望 KL 散度：

$$
\mathcal{L} = \mathbb{E}_{y \sim p(y)} \big[ D_{\mathrm{KL}} ( q_\phi(x|y) \| p(x|y) ) \big]
$$

该目标可分解为似然项与先验正则化项，在潜空间中表达为：

$$
\mathbb{E}_{\boldsymbol{y}} \big\{ \underbrace{ \mathbb{E}_{\boldsymbol{z} \sim q_\phi(\boldsymbol{z}|\boldsymbol{y})} [ -\log p(\boldsymbol{y}|\mathcal{D}(\boldsymbol{z})) ] }_{\mathcal{L}_{\mathrm{likelihood}}} + \underbrace{ D_{\mathrm{KL}} ( q_\phi(\boldsymbol{z}|\boldsymbol{y}) \| p(\boldsymbol{z}) ) }_{\mathcal{L}_{\mathrm{prior}}} \big\}
$$

### 推理流程

推理阶段，训练好的求解器 $q_\phi$ 作为纯前馈网络运行，以因果、分块、自回归的方式处理视频。图 2（下）展示了这一流式推理架构：

- **分块处理**：视频被划分为长度为 $T$ 帧的时间块，每个块内部使用双向自注意力（Intra-block Attention）捕获局部时空依赖：

$$
\mathrm{Att}_{\mathrm{intra}} ( \mathbf{Q}_i, \mathbf{K}_n, \mathbf{V}_n ) = \mathrm{softmax} \left( \frac{ \mathbf{Q}_i \mathbf{K}_n^\top }{ \sqrt{d_k} } \right) \mathbf{V}_n
$$

- **块间因果注意力**：当前块只能关注过去块的信息，通过因果注意力实现：

$$
\mathrm{Att}_{\mathrm{inter}} ( \mathbf{Q}_i, \mathbf{K}_{<n}, \mathbf{V}_{<n} ) = \mathrm{softmax} \left( \frac{ \mathbf{Q}_i \mathbf{K}_{<n}^\top }{ \sqrt{d_k} } \right) \mathbf{V}_{<n}
$$

- **KV 缓存**：在重建每个块后，将其注意力键值对存储并复用，避免对历史帧的冗余计算，将注意力复杂度降至线性，理论上支持无限长度的视频流式重建。

### 高效 VAE 集成

为进一步降低延迟，InstantViR 引入了高效 LeanVAE 替代原始视频扩散模型中的 WanVAE。由于 LeanVAE 的潜空间与教师潜空间不完全对齐，论文提出了一种**教师空间正则化蒸馏方案**：在 LeanVAE 空间训练求解器 $q'_\phi$ 时，通过将输出 $\hat{x}_0$ 经 LeanVAE 解码后再由教师编码器 $\mathcal{E}$ 映射回教师潜空间，从而在该空间计算有效的分数匹配损失：

$$
\mathcal{L}(q'_\phi) = \mathbb{E}_y \mathbb{E}_{z' \sim q'_\phi(z'|y)} [ -\log p(y|\mathcal{D}'(z')) ] + \mathbb{E}_{t, \epsilon, z' \sim q'_\phi(\cdot|y)} [ w(t) \| s_\theta(z_t, t) - s_{q'}(z_t, t) \|^2 ]
$$

这一设计使得 InstantViR† 能够在保持重建质量的同时，将推理速度从约 14 FPS 提升至超过 35 FPS（A100 GPU，832×480 分辨率）。

### 3.1 摊销变分推断框架

InstantViR 的核心目标是将迭代后验采样转化为单步前馈映射。给定降质视频测量 $\pmb{y}$ 和干净视频 $\pmb{x}$，视频逆问题的贝叶斯后验为：

$$p ( { \pmb x } | { \pmb y } ) \propto p ( { \pmb y } | { \pmb x } ) p ( { \pmb x } )$$

其中 $p(\pmb{y}|\pmb{x})$ 为已知退化算子的似然项，$p(\pmb{x})$ 为视频扩散先验。

为消除迭代采样，InstantViR 将求解器参数化为 $q_\phi(\pmb{x}|\pmb{y})$，通过最小化变分近似与真实后验之间的期望 KL 散度进行训练：

$$\mathcal { L } = \mathbb { E } _ { { \pmb { y } } \sim p ( { \pmb { y } } ) } \Big [ D _ { \mathrm { K L } } \big ( q _ { \phi } ( { \pmb { x } } | { \pmb { y } } ) \| p ( { \pmb { x } } | { \pmb { y } } ) \big ) \Big ]$$

该目标可分解为数据保真项与先验正则化项：

$$\mathbb { E } _ { \pmb { y } } \Big \{ \mathbb { E } _ { \pmb { x } \sim q _ { \phi } ( \pmb { x } | \pmb { y } ) } \Big [ - \log p ( \pmb { y } | \pmb { x } ) \Big ] + D _ { \mathrm { K L } } \big ( q _ { \phi } ( \pmb { x } | \pmb { y } ) \| p ( \pmb { x } ) \big ) \Big \}$$

将求解器置于视频 VAE 的潜空间中，得到潜空间目标：

$$\mathbb { E } _ { \boldsymbol { y } } \big \{ \underbrace { \mathbb { E } _ { \boldsymbol { z } \sim q _ { \phi } ( \boldsymbol { z } | \boldsymbol { y } ) } \left[ - \log p \big ( \boldsymbol { y } | \mathcal { D } ( \boldsymbol { z } ) \big ) \right] } _ { \mathcal { L } _ { \mathrm { l i k e l i h o o d } } } + \underbrace { D _ { \mathrm { K L } } \big ( q _ { \phi } ( \boldsymbol { z } | \boldsymbol { y } ) \| p ( \boldsymbol { z } ) \big ) } _ { \mathcal { L } _ { \mathrm { p i o r } } } \big \}$$

其中 $\mathcal{D}$ 为 VAE 解码器，$\mathcal{L}_{\mathrm{likelihood}}$ 确保重建与测量一致，$\mathcal{L}_{\mathrm{prior}}$ 利用教师扩散先验施加时间一致性。先验项通过分数匹配近似计算：

$$\mathcal { L } _ { \mathrm { p r i o r } } \approx \mathbb { E } _ { t , \epsilon , z \sim q _ { \phi } ( \cdot | y ) } \big [ w ( t ) \| s _ { \theta } ( z _ { t } , t ) - s _ { q _ { \phi } } ( z _ { t } , t ) \| ^ { 2 } \big ]$$

其中 $s_\theta$ 为冻结的教师分数网络，$s_{q_\phi}$ 为辅助学生分数网络，$w(t)$ 为时间加权函数。此蒸馏框架的关键特性是**无需配对干净/降质视频数据**，仅依赖教师扩散模型与已知退化算子。

### 3.2 因果自回归块式注意力

为实现流式视频处理，InstantViR 设计了因果自回归架构，将视频按 $T$ 帧的时间块进行处理。每个块内部使用双向自注意力：

$$\mathrm { A t t } _ { \mathrm { i n t r a } } ( \mathbf { Q } _ { i } , \mathbf { K } _ { n } , \mathbf { V } _ { n } ) = \mathrm { s o f t m a x } \Bigg ( \frac { \mathbf { Q } _ { i } \mathbf { K } _ { n } ^ { \top } } { \sqrt { d _ { k } } } \Bigg ) \mathbf { V } _ { n }$$

其中 $\mathbf{Q}_i$ 为当前块的查询，$\mathbf{K}_n$、$\mathbf{V}_n$ 为同一块的键和值，$d_k$ 为键的维度。

块间则采用因果注意力，仅允许当前块关注过去块的信息：

$${ \mathrm { A t t } } _ { { \mathrm { i n t e r } } } ( \mathbf { Q } _ { i } , \mathbf { K } _ { < n } , \mathbf { V } _ { < n } ) = { \mathrm { s o f t m a x } } \left( { \frac { \mathbf { Q } _ { i } \mathbf { K } _ { < n } ^ { \top } } { \sqrt { d _ { k } } } } \right) \mathbf { V } _ { < n }$$

其中 $\mathbf{K}_{<n}$、$\mathbf{V}_{<n}$ 为所有过去块的键值拼接。该设计配合标准自回归 **KV 缓存**机制：每完成一个块的重建，其注意力键值被存储并在后续块中复用，将注意力复杂度降至线性，理论上支持无限长度视频流。

### 3.3 教师空间正则化蒸馏

原始视频扩散模型使用高延迟 VAE（如 WanVAE）。为降低推理延迟，InstantViR 引入高效 **LeanVAE**（编码器 $\mathcal{E}'$，解码器 $\mathcal{D}'$），其潜变量记为 $\pmb{z}'$。然而 LeanVAE 的潜空间与教师潜空间未对齐，直接计算先验损失将失效。

为此，InstantViR 提出**教师空间正则化蒸馏**方案，在 LeanVAE 空间训练求解器 $q'_\phi(\pmb{z}'|\pmb{y})$，但将 $\pmb{z}'$ 解码后重新编码回教师潜空间以计算分数匹配损失：

$$\mathcal { L } \big ( q _ { \phi } ^ { \prime } \big ) = \mathbb { E } _ { y } \mathbb { E } _ { z ^ { \prime } \sim q _ { \phi } ^ { \prime } ( z ^ { \prime } \mid y ) } \big [ - \log p \big ( y \vert \mathcal { D } ^ { \prime } ( z ^ { \prime } ) \big ) \big ] + \mathbb { E } _ { t , \epsilon , z ^ { \prime } \sim q _ { \phi } ^ { \prime } ( \cdot \vert y ) } \Big [ w ( t ) \| s _ { \theta } ( z _ { t } , t ) - s _ { q ^ { \prime } } ( z _ { t } , t ) \| ^ { 2 } \Big ]$$

其中 $\pmb{z}_t$ 通过桥接路径 $\pmb{z}' \to \mathcal{D}'(\pmb{z}') \to \mathcal{E}(\cdot)$ 映射至教师空间后加噪得到。该方案使轻量 VAE 无缝集成到教师扩散先验中，显著降低延迟的同时保持时间一致性约束的有效性。

**关键模块总结**：整个框架由冻结教师先验 $s_\theta$、摊销求解器 $q_\phi$、因果自回归块式注意力、KV 缓存、以及教师空间正则化蒸馏桥接五个核心模块构成，共同实现从降质视频到干净潜变量的单步实时映射。

## 实验与关键发现

### 核心性能：速度与质量的代际跨越

InstantViR 在视频逆问题求解上实现了速度与质量的双重突破，其根本驱动力来自**摊销变分推断**对迭代扩散采样的彻底替代。传统方法如 **SVI** 需要在后验分布上进行数百步迭代采样以逼近干净视频，而 InstantViR 通过教师-学生知识蒸馏，将双向视频扩散先验压缩进一个单步前馈网络，推理时仅需一次前向传播即可输出重建结果。

在 NVIDIA A100 GPU、832×480 分辨率的标准测试条件下，InstantViR† 达到 **35.56 FPS**，相较于 SVI 的约 0.36 FPS 实现了超过 **100 倍**的加速（Table 1, Figure 1）。即便未使用高效 VAE 的 InstantViR 版本，也以 13.91 FPS 远超所有迭代采样基线。这一速度优势使得视频逆问题首次进入实时流式处理区间。

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of temporal quality and inference speed. The former is evaluated with FVD ↓ and the latter is with FPS ↑. Best results are in bold, suboptimal are underlined*

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/001_Figure_1.jpg]]
*Figure 1: We introduce InstantViR, a real-time video inverse problem solver that drastically outperforms slow sampling-based methods in both speed and quality. Bottom-right: At 832×480 resolution, our amortized framework is over 100× faster than sampling-based baselines like SVI [10], achieving over 35 FPS and the excellent quality. Left and Bottom-left: Qualitative examples demonstrate versatile, high-fidelity reconstruction for inpainting and deblurring, along with optional text-guided control (e.g., "pink lips", "light-blue collar")*

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/009_Figure_1.jpg]]
*Figure 1: Video Inpainting qualitative comparison. Each row shows a complete sequence reconstructed by a specific method. InstantViR (both WanVAE Ours and LeanVAE Ours† variants) produces coherent content for every frame while requiring only a single feed-forward pass*

速度的提升并未以牺牲质量为代价。在时间一致性指标 FVD 上，InstantViR 在所有任务上均取得最优或次优结果：视频修复（50% 随机掩码）FVD 为 136.06，InstantViR† 进一步降至 132.59；视频去模糊 FVD 为 110.51（InstantViR† 为 103.45）；4× 超分辨率 FVD 为 153.13（Table 1）。与迭代采样基线 **Vision-XL** 相比，InstantViR 在 FVD 上全面领先，同时推理速度快两个数量级以上。这验证了核心洞察：**蒸馏后的因果自回归学生网络不仅保留了教师模型的时间一致性先验，更通过单步推理消除了迭代采样的累积误差**。

在空间质量方面，InstantViR 同样展现出强竞争力。以视频修复任务为例，PSNR 达到 30.54，SSIM 0.97，LPIPS 0.12（Table 2）；4× 超分辨率的 PSNR 为 34.91，SSIM 0.96；去模糊任务的 PSNR 为 31.85，SSIM 0.97。这些指标表明，单步推理并未导致空间细节的显著退化，数据保真项与先验蒸馏损失的联合优化有效维持了逐帧重建精度。

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of spatial quality. Metrics include PSNR, SSIM, LPIPS. Best results are in bold, suboptimal are underlined*

### 架构设计的消融效应

InstantViR 的性能优势可归因于三个关键设计选择，其效应在定量和定性结果中均有体现：

**1. 因果自回归块状注意力与 KV 缓存。** 该设计使推理过程天然支持流式处理。块内双向注意力保证了当前块内帧间的充分信息交互，块间因果注意力则确保时间顺序的一致性，同时 KV 缓存将历史帧的注意力复杂度降至线性。这一机制是实现 35+ FPS 实时推理的架构基础，也是 SVI 等全双向注意力方法无法达成的。在长视频场景下，KV 缓存理论上支持无限长度流式重建，无需重复计算历史帧。

**2. 教师空间正则化蒸馏。** InstantViR† 与 InstantViR 的核心差异在于是否采用 LeanVAE 替代原始 WanVAE。LeanVAE 显著降低了编解码延迟，但引入了潜在空间不匹配的问题——学生网络的输出位于 LeanVAE 空间，而教师分数网络 s_θ 期望的输入在 WanVAE 空间。教师空间正则化蒸馏通过在训练时将 z' 映射回教师潜在空间来计算分数匹配损失，有效弥合了这一鸿沟。实验结果表明，InstantViR† 在 FVD 上不仅未因 VAE 替换而退化，反而在修复和去模糊任务上进一步改善（132.59 vs 136.06，103.45 vs 110.51），证明该蒸馏方案成功将教师先验迁移至高效 VAE 空间。

**3. 无需配对数据的先验驱动蒸馏。** 训练仅需降质视频 y 和冻结的教师扩散模型 s_θ，无需外部配对干净/降质视频数据。这极大降低了数据获取门槛，使得方法可快速适配不同的退化算子。在 Open-Sora 数据集上训练后，模型在 REDS 数据集上展现出强大的零样本泛化能力（Figure 3），生成清晰、连贯的视频，感知上接近真值。

### 定性分析：时间一致性与可控性

定性结果进一步揭示了 InstantViR 的行为特征。在视频随机修复任务中（Figure 3），对于 50% 掩码的输入，InstantViR 重建出高保真且时间一致的视频。放大的人脸序列展示了单步结果的稳定性与细节丰富度——帧间无闪烁或纹理漂移，这归功于教师视频扩散先验提供的强时间正则化。

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison for video random inpainting. (Top) On the Open-Sora dataset [12], our model reconstructs a highfidelity and temporally consistent video from a 50% masked measurement. The zoomed-in face sequence demonstrates the stability and fine detail of our single-step result. (Bottom) We demonstrate strong zero-shot generalization on the REDS dataset [33], our method generates a sharp, coherent video that is perceptually close to the ground truth*

![[assets/figures/papers/paper_list_l889_https_arxiv_org_abs_2511_14208/figures/011_Figure_3.jpg]]
*Figure 3: Video Super-Resolution (4×) qualitative comparison. InstantViR restores temporally consistent structures, outperforming slower diffusion-based baselines in both sharpness and coherence*

文本引导重建实验（Figure 4）展示了框架的可控性。给定相同的掩码输入，通过不同的文本提示（如 "black headband"、"wear glasses"），InstantViR 可生成语义不同但均合理的高质量重建。更值得注意的是，模型能够生成多模态输出（如 "close eyes" 与 "open eyes"），表明蒸馏过程保留了教师扩散先验的生成多样性和细粒度可控性。

### 局限性与失败模式

尽管整体性能优异，分析中仍识别出以下局限：

- **潜在空间对齐不完全。** 教师空间正则化蒸馏虽有效，但 LeanVAE 与 WanVAE 的潜在空间尚未达到完美对齐。在 4× 超分辨率任务上，InstantViR† 的 FVD（156.43）略差于 InstantViR（153.13），暗示在需要精细空间细节的任务中，VAE 替换可能带来微弱的保真度损失。这一现象需进一步验证，但方向明确：联合微调轻量级 VAE 以更好地对齐教师潜在空间，有望完全消除该质量差距。

- **退化算子的已知性假设。** 当前框架在训练和推理中均依赖已知的退化算子（掩码模式、模糊核、下采样倍数）。对于未知或混合退化场景，似然项无法直接计算，需扩展至盲逆问题范式。这是方法泛化性的一个边界条件。

- **教师先验的上限约束。** 蒸馏学生模型的质量天花板由教师视频扩散模型决定。若教师先验对特定场景（如极端运动模糊、严重遮挡）的建模能力不足，学生模型亦无法超越。这一依赖性在结论中已被作者明确承认。

### 实验公平性说明

所有推理速度测量均在 NVIDIA A100 GPU 上以 832×480 分辨率进行，比较在 Open-Sora 和 REDS 数据集上采用相同的退化设置展开，确保了对比的公平性。

## 定位与知识库关联

### 1. 问题谱系：从迭代采样到摊销推理

视频逆问题（Video Inverse Problems）的核心挑战在于从降质观测 $y$ 中恢复干净视频 $x$，其贝叶斯后验为 $p(x|y) \propto p(y|x) p(x)$。传统求解范式可分为两条路径：

- **迭代扩散后验采样**：以 **DPS**、**SVI**、**Vision‑XL** 等为代表，利用预训练视频扩散模型作为强先验 $p(x)$，通过迭代求解反向 SDE 逐步逼近后验。这类方法在时间一致性和感知质量上表现优异，但推理速度极慢——SVI 在 A100 上处理 832×480 视频仅约 0.36 FPS，无法满足实时或流式应用需求。
- **图像扩散 + 时间正则化**：将视频逐帧视为独立图像，辅以光流或时序平滑约束。此类方法推理较快，但缺乏对复杂时空动态的显式建模能力，导致严重的时间不一致性。

InstantViR 的根本洞察在于：**迭代采样并非利用扩散先验的唯一方式**。通过知识蒸馏，可以将双向视频扩散模型的强时间一致性先验“压缩”进一个前馈网络，从而在单步推理中同时获得高质量重建与实时速度。这一思路将视频逆问题从“采样范式”推入“摊销推理范式”，在方法论上连接了扩散模型蒸馏（如一致性模型、变分分数蒸馏）与视频逆问题的交叉地带。

### 2. 核心设计空间与基线对比

InstantViR 在四个关键设计维度上相对于迭代采样基线做出了系统性改变：

| 设计维度 | 迭代采样基线 | InstantViR | 因果机制 |
|----------|-------------|-----------|---------|
| **推理范式** | 迭代后验采样（数百步） | 单步摊销变分推理 | 将 $q_\phi(x|y)$ 直接参数化为前馈网络，消除迭代 |
| **时间注意力** | 全双向时空注意力 | 块内双向 + 块间因果注意力 | 块间因果注意 + KV 缓存实现流式处理，避免冗余计算 |
| **特征 VAE** | 原始视频 VAE（如 WanVAE） | LeanVAE + 教师空间正则化蒸馏 | 通过 $z' \to \hat{x}_0 \to z$ 桥接两个潜空间，大幅降低编解码延迟 |
| **训练数据需求** | 依赖外部配对数据（部分蒸馏方法） | 无需配对数据，仅需教师模型与退化算子 | 先验驱动的蒸馏：教师扩散模型提供监督信号 |

**关键差异的因果解释**：

1. **推理范式切换**：迭代采样基线的速度瓶颈在于每一步都需要评估分数网络 $s_\theta$。InstantViR 通过最小化 $D_{\mathrm{KL}}(q_\phi(x|y) \| p(x|y))$ 将整个后验采样过程摊销为单次前向传播，本质上是将计算负担从推理阶段转移到训练阶段。

2. **因果自回归架构**：全双向注意力要求处理完整视频后才能输出，无法流式处理。InstantViR 将视频划分为 $T$ 帧的时间块，块内保留双向注意力以建模局部动态，块间采用因果注意力仅关注历史块，配合 KV 缓存使注意力复杂度从 $O(N^2)$ 降至 $O(N)$，理论上支持无限长度视频流。

3. **LeanVAE 集成**：原始 WanVAE 的编解码延迟是实时推理的隐性瓶颈。教师空间正则化蒸馏（Eq. 11）通过将 LeanVAE 重建的 $\hat{x}_0$ 重新编码回教师潜空间计算分数匹配损失，使得轻量 VAE 能够无缝继承教师扩散先验，而无需重新训练教师模型。

### 3. 适用边界与局限性

基于论文提供的证据与实验设置，InstantViR 的适用边界可总结如下：

**明确适用场景**：
- 已知退化算子的视频逆问题：修复（50% 随机掩码）、高斯去模糊、4× 超分辨率
- 需要实时或流式处理的场景（> 35 FPS @ 832×480, A100）
- 可选的文本引导可控重建（如“戴眼镜”、“粉色嘴唇”）

**已验证的局限性**（需在后续工作中关注）：
- **潜空间对齐不完美**：LeanVAE 的潜空间与教师 WanVAE 潜空间尚未完全对齐，可能带来细微的重建质量损失。论文未提供该损失的定量消融分析，需手动验证。
- **教师先验依赖**：模型性能受限于教师视频扩散模型的先验强度和泛化能力。在教师模型未见过的分布外退化上，性能可能显著下降。
- **退化算子限制**：当前框架仅支持已知的显式退化算子，对于盲去噪、压缩伪影去除等未知或混合退化，需进一步扩展框架。

**证据强度说明**：
- 速度与质量的核心声明（> 35 FPS，~100× 加速）有 Figure 1 和 Table 1 的明确数据支持，置信度较高。
- 训练无需配对数据的声明在 Abstract 和 Section 3.1 中反复出现，但论文未展示与配对数据训练的对比实验，该声明的相对优势需结合具体应用场景判断。
- LeanVAE 带来的质量损失程度在现有图表中未做独立消融，需手动核实。

### 4. 开放问题

1. **VAE 联合微调**：是否可以通过联合微调 LeanVAE 的编解码器，使其潜空间更好地对齐教师潜空间，从而完全消除重建质量差距？这涉及在保持教师先验冻结的前提下，对 VAE 进行对抗或对比学习。

2. **退化泛化**：框架能否推广到更广泛的逆问题（如盲去模糊、压缩感知、去噪），同时保持高效推理？这可能需要引入退化估计模块或元学习策略。

3. **跨教师蒸馏**：当前蒸馏绑定单一教师模型。是否可以将多个教师先验（如不同架构或不同退化特化的扩散模型）蒸馏到统一的学生网络中，实现多任务实时求解？

4. **资源受限部署**：35 FPS 的指标在 A100 上测得，在边缘设备（如移动端 GPU）上的实际吞吐量与精度权衡尚未探索。LeanVAE 的选择为此提供了可能性，但缺乏系统性的硬件效率分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/InstantViR_Real_Time_Video_Inverse_Problem_Solver_with_Distilled_Diffusion_Prior.pdf]]
