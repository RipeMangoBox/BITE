---
title: "SemanticGen: Video Generation in Semantic Space"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/SemanticGen_Video_Generation_in_Semantic_Space.pdf
project_link: null
code_link: https://github.com/
aliases:
- SemanticGen
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 将生成过程首先在紧凑的语义空间进行全局规划，随后再生成VAE潜码以补充高频细节，从而显著降低建模复杂度和计算开销。
primary_logic: 视频中蕴含大量冗余，生成应先在低维高层语义空间进行全局布局，再补充细节，而不是直接利用双向注意力建模海量低层视频token。
claims:
- 在语义空间训练收敛速度显著快于VAE潜空间。
- 语义空间压缩（MLP+KL正则）提升收敛速度与视频质量。
- 长视频生成中，SemanticGen在Subject Consistency（95.07%）和Δ_drift^M（3.58%）等指标上显著超越基线。
- 条件于压缩语义表示生成的视频保留了参考视频的空间布局和运动模式，验证了语义表示捕捉高层信息。
---

# SemanticGen: Video Generation in Semantic Space

> [!tip] 核心洞察
> 视频中蕴含大量冗余，生成应先在低维高层语义空间进行全局布局，再补充细节，而不是直接利用双向注意力建模海量低层视频token。

| 字段 | 内容 |
|------|------|
| 中文题名 | SemanticGen：语义空间视频生成 |
| 英文题名 | SemanticGen: Video Generation in Semantic Space |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.20619) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | SemanticGen |
| Dataset | VBench-Long, VBench short |

> [!tip] 效果简介
> - VBench-Long 上，Subject Consistency 95.07% vs all baselines (outperforms all)；Background Consistency 95.86% vs all baselines (outperforms all)；Motion Smoothness 98.26% vs all baselines (outperforms all)。
> - VBench short 上，Subject Consistency 97.79% vs top baseline (e.g., Wan2.2) (comparable (ranked 2nd))。

## 概要

**SemanticGen** 提出一种两阶段视频生成框架，将生成过程从高维VAE潜空间迁移至紧凑的语义空间。其核心动机在于：现有视频生成模型直接在VAE潜空间建模，低层级视频token维度极高且存在大量冗余，导致收敛速度慢、难以高效扩展至长视频生成。

**核心洞察**是视频中蕴含大量冗余——生成应先在低维高层语义空间进行全局布局，再补充细节，而非直接利用双向注意力建模海量低层视频token。基于此，SemanticGen采用“先语义规划，后细节生成”的范式：第一阶段由扩散模型从文本生成紧凑的语义表示，第二阶段以该语义表示为条件，通过另一个扩散模型生成VAE潜码。

**关键结论**包括：

- **收敛加速**：在语义空间建模的收敛速度远快于在同样压缩的VAE潜空间建模（Fig. 9, Sec. 3.3）。
- **压缩增益**：通过MLP将语义空间维度从2048降至8并施加KL正则化，显著提升视频质量——Subject Consistency从96.29%升至97.49%，Temporal Flickering从96.39%升至98.27%（Table 3）。
- **长视频优势**：在VBench-Long基准上，SemanticGen在Subject Consistency（95.07%）、Background Consistency（95.86%）、Motion Smoothness（98.26%）及漂移度量Δ_drift^M（3.58%）等指标上全面超越所有基线（Table 2, Sec. 4.2）。
- **短视频可比性**：在VBench短视频基准上，SemanticGen与当前SOTA方法（如**Wan2.2**，Team Wan et al., arXiv 2025）性能可比（Table 1, Sec. 4.2）。

**方法定位**上，SemanticGen区别于单阶段直接生成VAE潜码的扩散模型（如**CogVideoX-2B**，Yang et al., arXiv 2024；**Stable-VideoDiffusion**，Blattmann et al., arXiv 2023），也不同于自回归视频生成模型（如**MAGI-1**，Teng et al., arXiv 2025）。其两阶段语义空间生成范式在长视频场景下展现出显著的一致性保持和漂移抑制能力。

近年来，文本到视频（T2V）生成取得了显著进展，主流范式通常依赖变分自编码器（VAE）将视频压缩到低维潜空间，再由扩散模型（Diffusion Model）或自回归模型在该潜空间进行生成建模。然而，这一直接在高维VAE潜空间建模的路线正暴露出一个核心瓶颈：**低等级视频token维度极高且包含大量时空冗余，导致模型收敛速度慢，且难以高效扩展至长视频生成**。

具体而言，现有先进模型——如扩散模型 **Wan2.2**（Team Wan et al., arXiv 2025）、**CogVideoX-2B**（Yang et al., arXiv 2024）以及自回归模型 **MAGI-1**（Teng et al., arXiv 2025）——均直接在VAE潜空间进行生成。当视频时长增加时，潜空间token数量线性增长，若采用全双向注意力（full bidirectional attention），计算复杂度将随序列长度呈平方级膨胀，这严重制约了长视频生成的可行性与质量。即便引入滑动窗口等局部注意力机制以降低计算开销，缺乏全局信息建模又会导致严重的时序漂移（temporal drifting），表现为主体一致性下降、背景闪烁或色彩偏移等问题。

上述困境的根本原因在于：**视频数据中存在大量冗余，生成过程不应从一开始就陷入对海量低层细节的建模**。一个更合理的策略是先在低维高层语义空间进行全局布局，确定场景结构、运动趋势和主体关系，再补充高频纹理细节。然而，现有方法普遍缺乏这种“先规划、后细化”的生成范式。

SemanticGen 正是针对这一缺口提出的一套**两阶段语义空间生成框架**。其核心动机可概括为三点：

1. **降低建模复杂度**：将生成过程从高维VAE潜空间迁移至紧凑的语义表示空间，显著压缩待建模的token维度，从而加速收敛并降低计算开销。
2. **解耦全局规划与细节生成**：第一阶段在语义空间进行全局生成，确定视频的高层语义布局；第二阶段以语义表示为条件生成VAE潜码，补充纹理与高频细节。
3. **缓解长视频漂移**：利用语义空间的全局注意力捕捉长程依赖，同时在VAE空间采用shifted window attention（Swin attention）控制计算量，二者协同显著减轻长视频生成中的漂移问题。

简言之，SemanticGen 的出发点是将视频生成的焦点从“像素级重建”上移至“语义级规划”，以语义空间作为生成的核心战场，从而在保持生成质量的同时，实现向长视频的高效扩展。

## 核心方法与创新机理

SemanticGen 的核心创新在于将视频生成从传统的高维VAE潜空间迁移至紧凑的语义空间，构建了一个“全局布局—细节填充”的两阶段生成范式。这一设计从根本上改变了视频扩散模型的建模对象和计算方式，其关键创新点体现在以下三个**changed slots**上。

### 1. 生成空间：从VAE潜空间到压缩语义空间

现有视频生成模型（如**Wan2.2**、**CogVideoX-2B**等）直接在VAE潜空间建模视频token，面临维度极高、冗余信息密集的瓶颈，导致收敛缓慢且难以扩展至长视频。SemanticGen将生成的首要阶段置于语义空间——利用预训练的Qwen2.5-VL视觉塔提取视频高层语义特征，再通过一个可学习的MLP将语义维度从2048压缩至8，并施加KL高斯正则化。

这一压缩语义空间保留了视频的空间布局和运动模式等全局结构信息，同时丢弃了低层纹理和颜色等高频细节（Fig. 4）。消融实验（Table 3）表明，维度从2048降至8后，Subject Consistency从96.29%提升至97.49%，Temporal Flickering从96.39%改善至98.27%，证实了紧凑语义空间对生成质量的显著增益。

### 2. 生成范式：从单阶段扩散到两阶段语义-潜码生成

传统方法采用单阶段扩散模型直接生成视频潜码，缺乏对全局结构的显式规划。SemanticGen将生成过程解耦为两个阶段（Fig. 3）：

- **阶段一（语义表示生成器）**：一个DiT扩散模型从文本条件生成压缩语义表示 $z_{sem}$，完成视频的全局布局规划。
- **阶段二（VAE潜码生成器）**：另一个DiT扩散模型以 $z_{sem}$ 为条件，通过in-context conditioning（将噪声潜码 $z_t$ 与 $z_{sem}$ 拼接作为输入）生成最终的VAE潜码，补充高频细节。

两阶段设计使得模型先在低维语义空间完成全局结构建模，再在VAE空间进行细节生成，显著降低了单阶段的建模复杂度。Fig. 9的消融实验直接对比了在语义空间与在压缩VAE潜空间建模的收敛速度：相同训练步数下，语义空间建模的生成质量远优于VAE潜空间建模，验证了语义空间作为生成起点的根本优势。

### 3. 长视频注意力机制：语义全注意力 + VAE Swin注意力

长视频生成中，全双向注意力的计算量随序列长度平方增长，是扩展至分钟级视频的核心瓶颈。SemanticGen提出了一种混合注意力策略（Fig. 5）：

- **语义空间**：在高度压缩的语义token上使用全注意力，以极低计算代价实现全局上下文建模。
- **VAE潜空间**：在映射到VAE潜空间时，采用shifted window attention（Swin），将计算量限制在局部窗口内。

这一设计的关键在于，全局语义建模为VAE空间的局部注意力提供了高层指导，有效抑制了长视频生成中的漂移问题。在VBench-Long基准上，SemanticGen的 $\Delta_{drift}^M$ 仅为3.58%，显著优于所有基线方法（Table 2），验证了“语义全局规划 + VAE局部生成”策略在长视频一致性上的决定性作用。

### 创新总结

SemanticGen的三个changed slots构成了一个因果链条：**紧凑语义空间**使得全局建模成为可能，**两阶段范式**将全局布局与细节填充解耦，**混合注意力**以语义全注意力指导VAE局部生成，三者协同实现了从短视频到长视频的高效扩展。这一设计哲学——先在低维高层语义空间进行全局规划，再补充高频细节——为视频生成模型提供了一个可泛化的架构范式。

SemanticGen 提出了一种**两阶段视频生成范式**，将传统的单阶段低层潜空间建模解耦为“高层语义规划→低层细节补充”的级联过程。其核心动机在于：现有视频生成模型直接在VAE潜空间建模，低等级视频token维度极高且存在大量冗余，导致收敛速度慢、难以高效扩展至长视频生成。SemanticGen通过在紧凑的语义空间完成全局布局，再生成VAE潜码以补充高频细节，从而显著降低建模复杂度和计算开销。

### 模块构成与数据流

整个框架由以下关键模块组成，其训练与推理流程如 Figure 3 所示：

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/004_Figure_3.jpg]]
*Figure 3: Overview of SemanticGen. (a) We optimize a latent diffusion model for denoising video VAE latents conditioned on their compressed semantic representations. (b) We train a semantic generator to fit the compressed semantic representation distribution of offthe-shelf semantic encoders. (c) During inference, we integrate the semantic generator and VAE latent generator to achieve high-quality T2V generation. Green: Input; Yellow: Output; Blue: Trainable models; Gray: Frozen models*

1. **语义编码器 (Semantic Encoder)**  
   采用预训练的 **Qwen2.5-VL vision tower** 作为语义编码器，从输入视频中提取紧凑的高层语义特征。该模块在训练和推理阶段均保持冻结。

2. **语义压缩 MLP (Semantic Compression MLP)**  
   一个可学习的轻量级 MLP，将高维语义特征压缩至极低维度（如 8 维），并通过 **KL 散度正则化** 鼓励压缩后的语义空间趋近于高斯分布。压缩后的语义表示作为后续生成的条件信号。

3. **语义表示生成器 (Semantic Representation Generator)**  
   基于 **DiT 架构** 的扩散模型，以文本为条件生成压缩语义表示。该阶段在语义空间中进行全局建模，确定视频的高层空间布局与运动模式。

4. **VAE 潜码生成器 (VAE Latent Generator)**  
   同样基于 **DiT 架构** 的扩散模型，以压缩语义表示为条件，通过 **Rectified Flow** 框架生成视频的 VAE 潜码。该阶段负责补充语义表示中缺失的纹理、颜色等低层细节。

### 训练与推理流程

训练分为两个独立阶段：

- **第一阶段 (Figure 3a)**：训练 VAE 潜码生成器。将噪声化的 VAE 潜码 $z_t$ 与压缩语义表示 $z_{sem}$ 拼接作为模型输入，即 $z_{input} := [z_t, z_{sem}]$，通过 in-context conditioning 的方式使生成器学会在语义引导下恢复视频细节。

- **第二阶段 (Figure 3b)**：训练语义表示生成器。冻结语义编码器和压缩 MLP，仅微调 DiT 扩散模型，使其学习从文本到压缩语义表示的映射。

推理时 (Figure 3c)，语义表示生成器首先从文本生成压缩语义表示，随后 VAE 潜码生成器以该语义表示为条件生成视频潜码，最终经 VAE 解码器还原为视频帧。

### 长视频扩展机制

对于长视频生成，SemanticGen 采用**混合注意力策略** (Figure 5)：在极度压缩的语义空间中使用全注意力进行全局建模，而在映射到 VAE 潜空间时使用 **shifted window attention (Swin)** 交替处理，从而避免全双向注意力随视频长度平方增长的计算开销，同时保持长程一致性。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/014_Figure_10.jpg]]
*Figure 10: Overview of the base text-to-video generation model*

### 基础生成框架：Rectified Flow

SemanticGen 的底层生成模型建立在 Rectified Flow 框架之上。给定数据分布 $p(z_0)$ 和标准高斯噪声 $\epsilon \sim \mathcal{N}(0, I)$，前向过程沿直线路径插值：

$$z_t = (1 - t) z_0 + t \epsilon$$

其中 $t \in [0, 1]$。去噪过程通过一个由参数 $\Theta$ 参数化的速度场 $v_{\Theta}(z_t, t)$ 驱动，遵循常微分方程（ODE）：

$$d z_t = v_{\Theta}(z_t, t) d t$$

训练目标为条件流匹配（Conditional Flow Matching）损失：

$$\mathcal{L}_{LCM} = \mathbb{E}_{t, p_t(z, \epsilon), p(\epsilon)} \| v_{\Theta}(z_t, t) - u_t(z_0 | \epsilon) \|_2^2$$

其中 $u_t(z_0 | \epsilon) = \epsilon - z_0$ 是条件概率路径的目标速度。推理时采用欧拉离散化迭代采样：

$$z_t = z_{t-1} + v_{\Theta}(z_{t-1}, t) \cdot \Delta t$$

### 两阶段生成管线

SemanticGen 的核心创新在于将视频生成从单一的高维 VAE 潜空间解耦为两个阶段，其整体流程如 Figure 3 所示。

**第一阶段：VAE 潜码生成器条件于语义表示（Figure 3a）。** 给定一段视频，首先使用冻结的语义编码器（Qwen2.5-VL 视觉塔）提取紧凑的语义特征，再通过一个可学习的 MLP 将其压缩至极低维度（如 8 维），并施加 KL 散度正则化以鼓励压缩后的语义空间趋近高斯分布。随后，训练一个基于 DiT 的扩散模型，以压缩语义表示 $z_{sem}$ 为条件对 VAE 潜码进行去噪。条件注入方式为上下文条件化（in-context conditioning），即将加噪的 VAE 潜码 $z_t$ 与压缩语义表示 $z_{sem}$ 沿序列维度拼接作为模型输入：

$$z_{input} := [z_t, z_{sem}]$$

**第二阶段：语义表示生成器（Figure 3b）。** 在第一阶段模型训练完成后，冻结语义编码器和 MLP，仅微调另一个 DiT 扩散模型，使其从文本条件直接学习压缩语义表示的分布。推理时（Figure 3c），先由语义表示生成器从文本生成压缩语义特征，再由 VAE 潜码生成器条件于该语义特征生成最终的视频潜码，经 3D VAE 解码器重建为视频。

### 语义压缩模块

语义压缩 MLP 是整个框架的关键瓶颈设计。原始语义编码器输出的特征维度高达 2048，直接在其上建模扩散过程计算开销巨大。MLP 压缩器输出压缩后分布的均值与方差，并通过 KL 散度目标进行正则化，使压缩空间逼近标准高斯分布。这一设计带来了双重收益：一方面极大降低了语义空间生成器的建模难度，另一方面高斯化的语义空间与扩散模型的先验假设天然对齐，显著加速收敛（Fig. 8, Table 3）。

### 长视频生成：Swin-Attention 混合注意力机制

对于长视频生成，全双向注意力在 VAE 潜空间的计算复杂度随帧数平方增长，成为主要瓶颈。SemanticGen 利用语义空间的高压缩比特性，设计了一种混合注意力策略（Figure 5）：

- **语义空间**：对所有帧的语义 token 施加全注意力（full attention），实现全局布局和运动的统一规划。
- **VAE 潜空间**：将语义 token 与 VAE 潜码 token 交错排列，在 VAE 潜码 token 之间使用 shifted window attention（Swin attention），限制每个窗口内的注意力范围，从而将计算量控制在线性级别。

这种设计使模型既能通过语义空间的全局注意力保持长程时空一致性，又能在 VAE 空间以可承受的计算代价补充高频细节，从机制层面缓解了长视频生成中的漂移问题（Fig. 13, Supplementary B.2）。

## 实验与关键发现

### 核心实验设置

SemanticGen 在两阶段框架下评估：第一阶段，冻结 Qwen2.5-VL 视觉塔与语义压缩 MLP，仅微调语义表示生成器（DiT）；第二阶段，以压缩语义表示为条件训练 VAE 潜码生成器。短视频生成在 16 帧、256×256 分辨率下进行，长视频生成则通过自回归扩展至一分钟级别。评估指标覆盖 VBench 短视频与 VBench-Long 长视频基准，后者额外引入漂移度量 $\Delta_{drift}^{M}$（视频首尾 15% 段指标差的绝对值），以量化长时序一致性退化。

### 主结果分析

**短视频生成**：在 VBench 基准上，SemanticGen 与当前最强 T2V 模型 **Wan2.2**（Team Wan et al., arXiv 2025）、**Seaweed-7B**（Team Seawead et al., arXiv 2025）等相比，整体质量可比。其中 Subject Consistency 达 97.79%，位列第二（Table 1）。这表明在常规时长下，语义空间生成并未牺牲视频质量。

**长视频生成**：SemanticGen 在 VBench-Long 上全面领先所有基线（Table 2）。关键指标包括：Subject Consistency 95.07%、Background Consistency 95.86%、Motion Smoothness 98.26%，漂移度量 $\Delta_{drift}^{M}$ 仅 3.58%，远低于 **LongLive**（Yang et al., arXiv 2025）、**HoloCine**（Xi et al., arXiv 2025）等长视频方法。定性结果（Figure 7）进一步显示，SemanticGen 在长达一分钟的视频中保持了主体一致性与背景稳定性，显著缓解了漂移问题。

**因果机制**：长视频优势源于两阶段设计中的注意力分工——语义空间采用全注意力进行全局布局规划，VAE 潜码空间采用 shifted window attention（Swin）映射细节，避免了全双向注意力随长度平方增长的计算瓶颈（Sec. 3.4, Figure 5）。全局语义建模为每一帧提供高层结构锚点，从而抑制了逐帧生成中的累积漂移。

### 消融实验

**语义空间压缩**：将语义表示维度从原始的 2048 压缩至 8，并施加 MLP + KL 高斯正则化，显著提升视频质量（Table 3）。具体而言，Subject Consistency 从 96.29% 提升至 97.49%，Temporal Flickering 从 96.39% 改善至 98.27%。定性消融（Figure 8）显示，压缩后生成视频的结构更稳定、伪影更少。因果解释是：高维语义空间包含冗余信息，压缩相当于强制模型学习更紧凑、更具判别力的高层表征，KL 正则化则使语义空间分布更接近高斯先验，利于扩散模型训练。

**生成空间对比**：在相同训练步数下，语义空间建模的收敛速度远快于同等压缩的 VAE 潜空间建模（Figure 9）。这验证了核心假设：语义空间维度低、冗余少，扩散模型能更高效地学习视频的全局结构分布；而 VAE 潜空间虽经压缩，仍包含大量低层细节，建模难度更高。

**长视频注意力机制**：与仅使用 Swin attention 而无全局语义规划的基线（Base-Swin-CT）相比，SemanticGen 的“语义全注意力 + VAE Swin attention”组合显著减轻了长视频漂移（Figure 13, Supplementary B.2）。这证明全局语义建模是长时序一致性的关键瓶颈，而非 Swin attention 本身。

### 失败模式分析

Figure 14 揭示了两个主要失败模式：

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/017_Figure_14.jpg]]
*Figure 14: Visualization of failure cases*

1. **高频时间信息丢失**：语义编码器以低 fps 采样视频帧，导致无法捕捉闪电、快速闪烁等高频动态变化。这源于语义空间的时间压缩率过高，牺牲了时间分辨率。
2. **细粒度纹理不一致**：长视频生成中，语义特征无法完全保留纹理、小物体等低层细节，导致局部区域出现纹理漂移或不一致。这表明语义表示在压缩过程中丢弃了部分对视觉保真度至关重要的高频空间信息。

### 方法谱系与知识库定位

SemanticGen 在视频生成方法谱系中占据“语义先验驱动”的新位置。传统扩散模型（**Stable-VideoDiffusion**, Blattmann et al., arXiv 2023；**CogVideoX-2B**, Yang et al., arXiv 2024）直接在 VAE 潜空间建模，属于单阶段低层生成范式；自回归模型 **MAGI-1**（Teng et al., arXiv 2025）虽采用离散 token 预测，仍面向低层表示。

SemanticGen 的核心创新在于将生成过程解耦为“语义规划—细节填充”两阶段，与 **Base-CT**（无语义建模的继续训练基线）形成鲜明对比：后者在长视频上漂移严重，而 SemanticGen 通过全局语义注意力有效抑制了漂移。该方法与 **LongLive** 等交互式长视频方法的目标一致，但实现路径不同——LongLive 依赖实时交互控制，SemanticGen 则通过架构层面的语义分工实现长时序一致性。

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods on short video generation*

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art methods on long video generation*

![[assets/figures/papers/paper_list_l84_https_arxiv_org_abs_2512_20619/figures/012_Figure_8.jpg]]
*Figure 8: Qualitative ablation on semantic space compression. Row 1: SemanticGen without compression; Row 2: Compress the semantic space using an MLP with 64 output channels; Row 3: Compress the semantic space using an MLP with 8 output channels*

## 定位与知识库关联

### 生成空间迁移：从VAE潜空间到语义空间

当前主流视频生成模型（如 **Wan2.2** (Team Wan et al., arXiv 2025)、**Seaweed-7B** (Team Seawead et al., arXiv 2025)、**CogVideoX-2B** (Yang et al., arXiv 2024)）均直接在3D VAE压缩的潜空间上进行扩散或自回归建模。这一范式面临的核心瓶颈在于：低层级视频token维度极高且包含大量时空冗余，导致模型收敛缓慢，并难以高效扩展至长视频生成。

SemanticGen的核心谱系突破在于**生成空间的层级迁移**：将生成过程分解为“先在紧凑语义空间进行全局规划，再映射至VAE潜空间补充高频细节”的两阶段范式。具体而言，该方法引入预训练的视觉-语言模型（Qwen2.5-VL vision tower）作为语义编码器，提取视频的高层语义特征，并通过一个可学习的MLP将其压缩至极低维度（如8维），同时施加KL高斯正则化以规整语义空间分布。随后，第一阶段训练一个以压缩语义表示为条件的VAE潜码扩散生成器（DiT + Rectified Flow），第二阶段再训练一个从文本生成压缩语义表示的扩散模型。

这一设计直接回应了现有方法的根本矛盾：**视频中蕴含大量冗余，生成应先在低维高层语义空间进行全局布局，再补充细节，而非直接利用双向注意力建模海量低层视频token**。消融实验提供了决定性证据：在语义空间建模的收敛速度远快于在同样压缩的VAE潜空间建模（Fig. 9），且将语义维度从2048压缩至8后，Subject Consistency从96.29%提升至97.49%，Temporal Flickering从96.39%改善至98.27%（Table 3）。

### 长视频生成中的注意力机制演进

长视频生成的核心挑战在于如何平衡全局一致性与计算效率。传统方案采用全双向注意力（如 **Stable-VideoDiffusion** (Blattmann et al., arXiv 2023)），计算量随视频长度平方增长，难以扩展。近期工作如 **LongLive** (Yang et al., arXiv 2025) 和 **HoloCine** (Xi et al., arXiv 2025) 分别从实时交互和3D感知角度探索长视频生成，但未系统解决注意力机制的效率-效果权衡。

SemanticGen提出了一种**混合注意力架构**：在语义空间使用全注意力建模全局依赖，在VAE潜空间使用shifted window attention（Swin）进行局部映射。这一设计的因果逻辑在于：语义表示维度极低（如8维），全注意力的计算开销可忽略不计，却能有效捕捉全局布局和运动模式；而VAE潜空间的Swin attention则将计算复杂度从平方级降至线性级。实验表明，结合全局语义建模的Swin attention显著减轻了长视频中的漂移问题（Δ_drift^M = 3.58%，Table 2），优于仅使用Swin attention而无全局语义规划的基线 **Base-Swin-CT**（Fig. 13, Supplementary B.2）。

### 与自回归视频生成模型的关系

值得关注的是，**MAGI-1** (Teng et al., arXiv 2025) 作为自回归视频生成模型，同样面临长序列建模的效率挑战。SemanticGen的两阶段框架提供了一种正交的解决思路：通过在语义空间进行自回归或扩散规划，再条件生成VAE潜码，有望在不牺牲全局一致性的前提下降低自回归解码的累积误差。然而，论文未提供与自回归模型的直接对比，该方向的交叉探索仍属开放问题。

### 适用边界与局限性

**高频时间信息丢失**。语义编码器以低帧率（low fps）采样视频帧，导致无法捕捉闪电、闪烁等快速变化的高频时间信息（Fig. 14）。这一局限根植于当前视觉-语言模型的固有时空分辨率权衡，并非SemanticGen框架本身可解。

**细粒度纹理不一致**。压缩语义特征（如8维）虽能保留高层布局和运动模式，但无法完全编码纹理、小物体等细粒度细节，导致长视频生成中出现局部纹理不一致（Fig. 14）。这是“先全局后局部”两阶段范式的固有张力：语义压缩越激进，细节丢失越严重。

**语义编码器依赖性**。框架依赖特定的预训练视觉-语言模型（Qwen2.5-VL），其预训练数据分布和训练范式直接影响语义表示的质量和泛化性。论文未系统评估其他语义编码器（如V-JEPA 2、VideoMAE 2、4DS）的影响，这一局限性在原文中被明确列为未来工作。

**训练数据与公平比较**。基模型为内部预训练模型，训练数据和部分训练细节未公开，可能影响完全可复现性。此外，部分消融基线（如Base-CT）的训练规模未完全披露，可能影响公平比较的可靠性——这一点需要读者在解读实验结果时保持审慎。

### 开放问题

1. **语义编码器的范式影响**：不同训练范式（视觉-文本对齐、自监督、纯视觉预训练）的语义编码器对生成性能有何影响？能否通过语义编码器的选择或微调来缓解高频信息丢失问题？

2. **高时间分辨率语义分词器**：当前语义编码器的时间压缩率与采样率存在根本矛盾。能否开发同时具备高时间压缩率和高采样率的视频理解分词器，以更好捕捉快速动态？

3. **跨任务泛化性**：语义空间生成框架在无文本条件、图像条件或可控编辑任务上的泛化性如何？语义表示的紧凑性是否天然适用于细粒度可控生成？

4. **分布偏移的弥合**：两阶段训练中，语义表示生成器（第二阶段）的输出分布与条件VAE潜码生成器（第一阶段）的输入分布之间存在偏移。如何进一步缩小这一分布差异，以提升端到端生成质量？

## 原文 PDF

![[paperPDFs/arxiv_2025/SemanticGen_Video_Generation_in_Semantic_Space.pdf]]
