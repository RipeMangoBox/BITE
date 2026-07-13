---
title: "PixelDiT: Pixel Diffusion Transformers for Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PixelDiT_Pixel_Diffusion_Transformers_for_Image_Generation.pdf
project_link: null
code_link: "https://github.com/blackforest-labs/flux"
aliases:
- PixelDiT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过双层级架构分离全局语义学习（patch-level）和像素级纹理细化（pixel-level），并结合像素级自适应层归一化（pixel-wise AdaLN）和像素token压缩（pixel token compaction）实现高效像素建模。
primary_logic: 将图像生成任务解耦为粗粒度语义规划和细粒度像素级优化，并设计高效的条件调制与压缩机制，使得端到端像素空间扩散模型能够兼顾高质量纹理细节和训练效率。
claims:
- PixelDiT在ImageNet 256×256上达到FID 1.61，显著超越现有像素空间模型。
- PixelDiT不使用任何自编码器，完全在像素空间端到端训练。
- 双层级架构和像素级AdaLN及token压缩是克服内存和计算瓶颈的关键。
- ImageNet 256×256 上 gFID↓ = 1.61
---

# PixelDiT: Pixel Diffusion Transformers for Image Generation

> [!tip] 核心洞察
> 将图像生成任务解耦为粗粒度语义规划和细粒度像素级优化，并设计高效的条件调制与压缩机制，使得端到端像素空间扩散模型能够兼顾高质量纹理细节和训练效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | PixelDiT：面向图像生成的像素扩散Transformer |
| 英文题名 | PixelDiT: Pixel Diffusion Transformers for Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.20645) · [Code](https://github.com/blackforest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PixelDiT |
| Dataset | ImageNet 256×256, ImageNet 512×512, Text-to-Image 1024×1024 |

> [!tip] 效果简介
> - ImageNet 256×256 上，gFID↓ 1.61 vs ADM-U (4.59) / PixelFlow-XL (1.98) (−2.98 vs ADM-U; −0.37 vs PixelFlow-XL)。
> - ImageNet 512×512 上，gFID↓ 1.81 vs DiT-XL (3.04) / EPG-L/32 (2.35) (−1.23 vs DiT-XL; −0.54 vs EPG-L/32)。
> - Text-to-Image 1024×1024 上，GenEval↑ 0.74 vs SDXL (0.55) / Flux-dev (0.67) (+0.19 vs SDXL; +0.07 vs Flux-dev)。

## 概要

图像生成领域长期存在一个根本性张力：**潜在扩散模型**（Latent Diffusion Models, LDMs）依赖预训练自编码器将图像压缩到低维潜在空间进行扩散建模，虽大幅降低了计算开销，却引入了**有损重建**和**细节丢失**的固有缺陷；而直接在像素空间建模的传统扩散模型虽能保留完整信息，却因高昂的计算代价和缺乏高效的高分辨率建模机制而长期落后。PixelDiT 直面这一瓶颈，提出了一种**端到端、纯Transformer架构的像素空间扩散模型**，完全摒弃预训练自编码器，在像素空间直接学习扩散过程。

其核心洞察在于将图像生成**解耦为两个层次**：粗粒度的全局语义规划与细粒度的像素级纹理优化。为实现这一目标，PixelDiT 设计了**双层级DiT架构**——patch-level DiT 负责捕获全局语义和布局，pixel-level DiT（PiT blocks）则专注于逐像素的纹理细节细化。这一架构的关键使能技术包括两项创新：(1) **像素级自适应层归一化**（Pixel-wise AdaLN），为每个像素生成独立的调制参数，将全局语义条件精确对齐到局部更新；(2) **像素token压缩**（Pixel Token Compaction），通过压缩patch内像素token的冗余信息，大幅降低全局注意力的序列长度，使像素级建模在计算上可行。

实验结果表明，PixelDiT 在多个基准上取得了极具竞争力的性能：在 ImageNet 256×256 类别条件生成上达到 **gFID 1.61**，显著超越此前的像素空间模型（ADM-U 4.59, PixelFlow-XL 1.98）；在 ImageNet 512×512 上达到 **gFID 1.81**，优于 DiT-XL (3.04) 等潜在扩散模型；在文本到图像生成（1024×1024）上也展现出与 SDXL、Flux-dev 等主流方法相当甚至更优的综合质量（GenEval 0.74, DPG-Bench 83.5）。消融实验进一步证实，移除像素token压缩将导致**内存溢出**而无法训练，移除表示对齐损失（REPA）则使 FID 从 2.36 骤升至 6.58，验证了各组件对训练稳定性和生成质量的关键作用。

PixelDiT 在方法谱系中处于**像素空间扩散模型**与**纯Transformer生成架构**的交汇点，其双层级设计为端到端高分辨率图像生成开辟了新路径，挑战了“潜在空间压缩是高效扩散建模必要条件”的既有范式。

### 像素空间扩散模型的核心瓶颈

扩散模型已成为视觉生成的主流范式，但现有高性能方法几乎全部依赖潜在扩散模型（Latent Diffusion Models, LDMs）。这类模型通过预训练自编码器将图像压缩至低维潜在空间，在潜在空间执行扩散过程，再解码回像素空间。这一设计带来了两个根本性问题：

**有损重建与细节丢失**。预训练自编码器本质上是一个有损压缩器，压缩-重建过程不可避免地丢弃高频纹理和精细结构。对于人脸、文字、复杂纹理等细节敏感的场景，潜在空间的表达能力成为质量上限。

**端到端训练的断裂**。自编码器通常需要单独预训练，与扩散模型本身形成松耦合的两阶段流水线。这不仅增加了训练复杂度，还限制了扩散模型直接感知和优化像素级信号的能力。

理论上，直接在像素空间执行扩散可以根治上述问题——模型能够端到端学习，无需任何有损中间表示。然而，像素空间扩散面临一个长期未解的矛盾：**全局语义建模需要大感受野和粗粒度表示，而像素级纹理生成需要细粒度的局部操作，二者对计算和内存的需求严重冲突**。传统像素空间模型（如ADM-U）要么因全像素自注意力导致计算爆炸，要么因激进的下采样丢失纹理细节，始终无法在质量和效率上与潜在模型抗衡。

### 现有方法的缺口

在PixelDiT之前，像素空间扩散模型的研究主要沿两条路径展开：

- **基于U-Net的像素扩散**（如ADM-U）：继承了早期扩散模型的卷积架构，但受限于卷积的感受野，全局语义捕获能力不足，在ImageNet 256×256上gFID仅达到4.59，与同期潜在模型差距显著。
- **基于Transformer的像素扩散**（如PixelFlow-XL、PixNerd-XL）：引入了Transformer的全局建模能力，但面临像素token序列长度随分辨率平方增长的困境。例如，256×256图像直接分patch为16×16时仍有256个token，若进一步细化到像素级则序列长度爆炸，使得全注意力计算不可行。

这些方法的核心缺口在于：**缺乏一种架构机制，能够同时高效处理全局语义和局部纹理，且不引发计算和内存的指数级膨胀**。

### 本文动机

PixelDiT的出发点是回答一个根本性问题：**能否设计一种端到端的像素空间扩散架构，使其在生成质量上媲美甚至超越潜在扩散模型，同时保持可接受的训练和推理成本？**

实现这一目标需要解决三个关键技术挑战：

1. **架构解耦**：如何将全局语义规划与像素级纹理细化分离，使二者各司其职而不互相掣肘？
2. **高效条件调制**：如何将全局语义信息精确传递到每个像素的更新中，而非简单广播？
3. **序列长度管理**：如何在保留像素级建模能力的前提下，将注意力序列长度控制在可行范围内？

PixelDiT通过双层级Transformer设计、像素级自适应层归一化（Pixel-wise AdaLN）和像素token压缩（Pixel Token Compaction）三项核心创新，系统性地回应了上述挑战，首次证明了端到端像素空间扩散模型可以在ImageNet 256×256上达到gFID 1.61的竞争力水平，并在文本到图像生成中超越SDXL等潜在模型。

## 核心方法与创新机理

PixelDiT 的核心创新在于通过**双层级 Transformer 架构**将图像生成任务解耦为粗粒度语义规划与细粒度像素级优化，并设计了**像素级自适应层归一化（Pixel-wise AdaLN）**与**像素 Token 压缩（Pixel Token Compaction）**两种关键技术，使得端到端像素空间扩散模型能够在兼顾高质量纹理细节的同时保持训练效率。以下从架构组织、条件调制策略和序列长度管理三个维度展开分析。

### 双层级架构：语义与纹理的解耦

传统扩散模型（如 DiT-XL、SiT-XL）在单一分辨率的 Transformer 中同时处理全局语义和局部纹理，导致两者相互干扰，难以在像素空间高效建模。PixelDiT 提出了一种**双层级 Transformer 组织**（Figure 2）：一个 **Patch-level DiT** 通路专门处理 patch token，负责捕获全局语义和布局；一个 **Pixel-level DiT** 通路（由 PiT 块组成）则专注于逐像素的纹理细化。这种“先规划后细化”的设计将全局理解与局部细节的学习分离开来，使得每个通路可以针对各自的任务进行优化，而非在单一模块中折中。

消融实验为这一设计的有效性提供了直接证据。从 Vanilla DiT 出发逐步添加组件（Table 5），引入双层级架构后，gFID 从 9.42 大幅降至 2.74（160 epoch），IS 从 148.5 提升至 202.5。进一步移除像素通路中的自注意力（即 PiT 块内的 Pixel-Pathway Attention）会导致 gFID 从 1.97 回升至 2.74，IS 从 209.4 降至 202.5（Table 6），表明像素级 Transformer 建模对纹理质量至关重要。

### 像素级自适应层归一化：从全局广播到逐像素调制

在条件调制策略上，PixelDiT 将传统的**全局/统一 AdaLN 广播**替换为**像素级 AdaLN**（Figure 3）。传统做法（如 DiT）将全局条件向量广播到所有像素，忽略了不同空间位置对语义条件的需求差异。Pixel-wise AdaLN 通过一个 MLP（$\Phi$）将语义条件 token $s_{\text{cond}}$ 扩展为逐像素的 scale、shift 和 gating 参数：

$$\Theta = \Phi(s_{\text{cond}}) \in \mathbb{R}^{(B \cdot L) \times p^2 \times 6 D_{\text{pix}}}$$

这使得每个像素都能获得与其空间位置和语义上下文对齐的独立调制信号，从而在保持全局语义一致性的同时实现精细的局部纹理控制。

### 像素 Token 压缩：突破内存与计算瓶颈

像素空间扩散模型面临的核心工程挑战是像素级 token 序列过长导致的全注意力计算爆炸。PixelDiT 提出的**像素 Token 压缩机制**通过“压缩-注意力-扩展”（compress–attend–expand）的策略解决了这一问题：在每个 patch 内部，将 $p^2$ 个像素 token 通过可学习的线性映射 $\mathcal{C}$ 压缩为一个紧凑的 patch token，再进行全局注意力计算，最后通过扩展映射 $\mathcal{E}$ 恢复像素级表示，并通过残差连接保留高频细节。

这一设计的决定性证据来自 Table 6 的消融：**移除 Pixel Token Compaction 直接导致训练内存溢出（OOM），无法完成训练**。这证明了该机制不是可选的优化，而是像素空间扩散模型可行的必要条件。进一步的分析显示，在 p=16 的配置下，压缩机制在质量与效率间取得了最佳平衡——p=32 虽能进一步降低计算量，但 gFID 从 2.23 显著恶化至 3.78（Table 13，120 epoch），表明过度的空间压缩会损害纹理建模能力。

### 创新总结

PixelDiT 的三个 changed slots 构成了一个相互依赖的创新体系：双层级架构提供了语义-纹理解耦的结构基础，像素级 AdaLN 为纹理细化提供了精确的条件调制，像素 Token 压缩则使整个系统在计算上可行。三者的协同使得 PixelDiT 成为首个在不使用预训练自编码器的情况下，在 ImageNet 256×256 上达到 gFID 1.61（Table 1）的像素空间扩散模型，显著超越了同类像素空间方法（如 ADM-U 的 4.59、PixelFlow-XL 的 1.98）。

PixelDiT 是一种**单阶段、端到端的像素空间扩散模型**，完全摒弃了预训练自编码器，直接在原始像素空间执行去噪过程。其核心设计理念是将图像生成任务解耦为**粗粒度语义规划**与**细粒度像素级优化**两个阶段，通过双层级 Transformer 架构实现高效建模。

### 双层级架构组织

模型整体采用**全 Transformer 架构**，由两条并行且相互协作的通路构成（Figure 2）：

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/002_Figure_2.jpg]]
*Figure 2: | Overview of PixelDiT: a dual-level, fully transformer-based diffusion architecture that operates directly in pixel space. The left figure shows the overall framework of PixelDiT, while the right figure illustrates the detailed structure of the PiT blocks*

1. **Patch-level DiT 通路**：负责处理图像 patch token，捕获全局语义、布局和对象结构。该通路以标准 DiT block 堆叠而成，输入为经过 patch 投影的语义 token，输出粗粒度的全局上下文表示。
2. **Pixel-level DiT 通路（PiT blocks）**：负责对每个像素 token 进行精细建模，恢复高频纹理细节。该通路由多个 Pixel Transformer（PiT）block 组成，每个 PiT block 包含两个核心技术组件——**像素级自适应层归一化（Pixel-wise AdaLN）** 和**像素 token 压缩（Pixel Token Compaction）**。

两条通路之间通过语义条件 token 进行信息传递：patch-level 通路产生的语义 token 作为条件信号注入 pixel-level 通路，指导逐像素的细节生成。

### 数据流与模块关系

输入图像 $x_{\text{patch}}$ 首先通过线性投影转换为 patch token $s_0 = W_{\text{patch}} x_{\text{patch}}$，同时时间步 $t$ 和类别/文本条件 $y$ 经 SiLU 激活融合为全局条件向量 $c = \text{SiLU}(W_t t + W_y y + b)$。随后：

- **Patch-level 处理**：patch token 经过多层带 AdaLN 调制和 2D RoPE 的 DiT block，输出富含全局语义的条件 token $s_{\text{cond}}$。
- **Pixel-level 处理**：原始图像经 reshape 和线性层嵌入为逐像素 token 序列 $\mathcal{X} \in \mathbb{R}^{B \times H \times W \times D_{\text{pix}}}$。在每个 PiT block 中：
  - **Pixel-wise AdaLN** 将语义条件 token $s_{\text{cond}}$ 通过 MLP $\Phi$ 扩展为每个像素独立的 scale、shift、gate 参数 $\Theta = \Phi(s_{\text{cond}}) \in \mathbb{R}^{(B \cdot L) \times p^2 \times 6 D_{\text{pix}}}$，实现全局上下文与局部像素更新的精确对齐。
  - **Pixel Token Compaction** 通过可学习的压缩映射 $\mathcal{C}$ 将每个 patch 内的 $p^2$ 个像素 token 压缩为一个紧凑 token，再执行全局注意力，最后通过扩展映射 $\mathcal{E}$ 恢复原始分辨率，并通过残差连接保留高频细节。

### 训练目标

模型采用 **Rectified Flow 速度匹配损失**在像素空间进行端到端训练：

$$\mathcal{L}_{\text{diff}} = \mathbb{E}_{t,x,\varepsilon}\left[ \| f_\theta(x_t, t, y) - v_t \|_2^2 \right]$$

同时引入表示对齐损失 $\mathcal{L}_{\text{repa}}$ 以稳定训练，总损失为 $\mathcal{L} = \mathcal{L}_{\text{diff}} + \lambda_{\text{repa}} \mathcal{L}_{\text{repa}}$（$\lambda_{\text{repa}}=0.5$，对齐施加于 patch-level 通路的第 8 个 block）。

### 关键设计决策的因果逻辑

| 设计选择 | 解决的问题 | 因果机制 |
|---------|-----------|---------|
| 双层级架构 | 单一分辨率 Transformer 难以同时高效建模全局语义和局部纹理 | 分离关注点：patch-level 专注语义规划，pixel-level 专注纹理细化 |
| Pixel-wise AdaLN | 全局/统一 AdaLN 广播无法为不同像素提供差异化条件信号 | 逐像素独立生成调制参数，使每个像素的更新与其语义上下文精确对齐 |
| Pixel Token Compaction | 全像素注意力导致序列长度爆炸（$O(HW)$），计算不可行 | 压缩冗余像素 token 后再做全局注意力，将复杂度从 $O((HW)^2)$ 降至可控范围 |
| 像素空间端到端训练 | 潜在扩散模型依赖预训练自编码器导致有损重建和细节丢失 | 直接在像素空间建模，消除编解码器带来的信息瓶颈 |

> **注意**：文本到图像版本（PixelDiT-T2I）在 patch-level 通路采用 MM-DiT block，图像和文本 token 形成双流，使用独立的 QKV 投影，但整体双层级架构和像素建模机制保持一致（Figure 7）。

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/015_Figure_7.jpg]]
*Figure 7: | T2I architecture of PixelDiT with MM-DiT blocks on the patch-level pathway. The pixel-level pathway performs dense per-pixel modeling conditioned on semantic tokens*

PixelDiT 的核心设计围绕一个**双层级 Transformer 架构**展开，将图像生成任务解耦为粗粒度的语义规划与细粒度的像素级纹理优化。该架构由四个关键模块协同构成：Patch-level DiT、Pixel-level DiT (PiT)、像素级自适应层归一化（Pixel-wise AdaLN）和像素 Token 压缩机制（Pixel Token Compaction）。

### 3.1 双层级架构与 Patch Token 投影

输入图像首先被划分为 $p \times p$ 的非重叠 patch，每个 patch 通过线性投影转换为一个维度为 $D$ 的 patch token：

$$s_0 = W_{\mathrm{patch}} \, x_{\mathrm{patch}}$$

同时，时间步 $t$ 与类别/文本条件 $y$ 被融合为一个全局条件向量，用于后续所有调制操作：

$$c = \mathrm{SiLU}(W_t t + W_y y + b) \in \mathbb{R}^{B \times 1 \times D}$$

**Patch-level DiT** 仅处理上述 patch token，通过一系列标准 DiT 块（含 AdaLN 调制与 2D RoPE 位置编码）捕获图像的全局语义和布局：

$$\overline{s}_i = s_i + \alpha_1(c) \odot \mathrm{Attn}\big(\gamma_1(c) \odot \tilde{s}_i + \beta_1(c); \mathrm{RoPE}\big)$$

该通路输出的语义 token 将作为条件信号，指导像素级通路的纹理细化。

### 3.2 像素级通路与 PiT 块

像素级通路的核心是 **Pixel Transformer (PiT) 块**。图像被嵌入为逐像素的 token 序列 $\mathcal{X} \in \mathbb{R}^{B \times H \times W \times D_{\mathrm{pix}}}$，每个 PiT 块包含两个关键组件：

**Pixel-wise AdaLN**：与传统的全局广播式 AdaLN 不同，Pixel-wise AdaLN 为每个像素独立生成调制参数。具体而言，来自 patch-level 通路的语义条件 token $s_{\mathrm{cond}}$ 通过一个 MLP $\Phi$ 扩展为 $p^2$ 组 scale、shift 和 gate 参数：

$$\Theta = \Phi(s_{\mathrm{cond}}) \in \mathbb{R}^{(B \cdot L) \times p^2 \times 6 D_{\mathrm{pix}}}$$

这使得全局语义能够以像素级粒度对齐局部更新，解决了传统 AdaLN 在像素空间建模中条件信号过于粗糙的问题。

**Pixel Token Compaction**：为降低全局注意力的计算复杂度，该机制将每个 patch 内的 $p^2$ 个像素 token 压缩为一个紧凑的 patch token。压缩操作通过一个可学习的线性映射 $\mathcal{C}$ 实现，在全局注意力计算后再通过扩展操作 $\mathcal{E}$ 恢复为像素 token，并通过残差连接保留高频细节。消融实验表明，移除该压缩机制直接导致训练内存溢出（OOM），无法完成训练（Table 6）。

### 3.3 训练目标

PixelDiT 采用 Rectified Flow 框架，直接在像素空间进行速度匹配训练：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{t, x, \varepsilon}\left[ \| f_\theta(x_t, t, y) - v_t \|_2^2 \right]$$

此外，为稳定训练并提升表示质量，模型在 patch-level 通路的第八个块处引入了表示对齐损失（REPA），最终训练目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diff}} + \lambda_{\mathrm{repa}} \mathcal{L}_{\mathrm{repa}}$$

其中 $\lambda_{\mathrm{repa}} = 0.5$。消融实验证实，移除 REPA 损失会导致 gFID 从 2.36 骤升至 6.58（80 epoch），训练稳定性显著下降（Table 11）。

## 实验与关键发现

### 核心定量结果

PixelDiT在类别条件生成和文本到图像生成两个维度上均展现出竞争力。在ImageNet 256×256类别条件生成任务上，PixelDiT-XL经过320 epoch训练后达到 **gFID 1.61**，显著超越现有像素空间扩散模型（如ADM-U的4.59和PixelFlow-XL的1.98），同时与主流潜在扩散模型（DiT-XL的2.27、SiT-XL的2.06）相比也有明显优势（Table 1）。在更高分辨率的ImageNet 512×512任务上，PixelDiT取得 **gFID 1.81**，优于DiT-XL（3.04）和EPG-L/32（2.35）等方法（Table 2）。

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/004_Table_1.jpg]]
*Table 1: | Quantitative results on ImageNet 256×256 for class-conditioned generation*

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/006_Table_2.jpg]]
*Table 2: | Quantitative comparison on ImageNet 512×512*

在文本到图像生成任务上，PixelDiT-T2I在1024×1024分辨率下达到 **GenEval 0.74** 和 **DPG-Bench 83.5**，整体表现优于SDXL（GenEval 0.55）和Flux-dev（GenEval 0.67），与DALLE3在DPG-Bench上持平（均为83.5），略低于Flux-schnell的84.8（Table 4）。

### 架构消融：组件贡献的因果链

Table 5的系统消融揭示了从Vanilla DiT到完整PixelDiT的性能增益路径。消融从基线DiT-XL开始，逐步添加关键组件：

- **添加像素级路径（双层级架构）**：将单一patch-level DiT扩展为双层级设计后，性能提升显著，但若不引入像素token压缩机制，训练会因显存溢出（OOM）而无法完成，直接验证了压缩机制是双层级架构可行的必要条件。
- **引入像素级AdaLN**：在双层级架构基础上使用像素级自适应层归一化，进一步提升了生成质量，证明逐像素的细粒度条件调制对纹理细化至关重要。
- **加入REPA表示对齐**：添加REPA对齐损失后，gFID从2.36提升至1.61（80 epoch对比），IS也有相应改善。Table 11的独立消融显示，移除REPA会导致gFID从2.36骤升至6.58，训练稳定性严重恶化，表明表示对齐在像素空间扩散训练中起到了关键的稳定和加速收敛作用。
- **推理策略（CFG）**：在训练完成的模型上应用分类器自由引导，进一步压缩gFID至最终值。

### 像素Token压缩的计算与收敛分析

Table 6对比了不同压缩策略的计算开销和收敛行为。移除像素token压缩（No Pixel Token Compaction）直接导致训练OOM，无法在实验规模下完成。采用压缩机制后，模型在80和160 epoch的gFID分别为2.74和1.97，计算量（GFLOPs）保持在可训练范围内。移除像素路径中的自注意力（No Pixel-Pathway Attention）虽然降低了计算量，但gFID明显退化（80 epoch时从2.74升至3.12），IS也有所下降，说明像素级token间的注意力交互对纹理细节建模不可或缺。

### Patch Size与模型规模的收敛特性

Figure 5展示了不同patch size（p=8, 16, 32）和模型规模（B/L/XL）下的收敛曲线。**Patch size p=16** 在质量与效率间取得最佳平衡：p=32虽降低计算量，但gFID显著变差（Table 13显示120 epoch时p=32的gFID为3.78，远差于p=16的2.23）。模型规模方面，从B到L再到XL的扩展带来了持续的性能增益，且未见明显饱和迹象，表明PixelDiT架构具有良好的可扩展性。

### 失败模式与局限性

尽管PixelDiT在基准测试上表现优异，论文明确指出了以下局限：

1. **复杂几何与纹理的生成困难**：受限于模型容量（1.3B参数）和高质量训练数据的不足，PixelDiT-T2I在生成人手、复杂建筑等几何和纹理复杂的对象时仍存在明显困难。
2. **训练不稳定性**：使用速度预测（velocity prediction）训练像素空间扩散模型容易出现损失尖峰（loss spikes），尤其在更深架构和长训练过程中。虽然论文采用了一些稳定化技巧，但完全消除尖峰而不牺牲训练效率仍是一个未解决的挑战。
3. **公平性注意事项**：需要指出，PixelDiT不使用预训练自编码器，而部分baseline（如LDM系列）依赖大规模自编码器，这体现了不同的设计哲学。在文本到图像生成中，不同模型采用不同的文本编码器和训练数据规模，量化比较需要在更一致的条件下进一步验证。

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/011_Table_5.jpg]]
*Table 5: | Ablations of PixelDiT-XL on ImageNet 256×256. Results start from Vanilla DiT and incrementally add architectural improvements and inference strategies. OOM indicates the dual-level variant without token compaction exceeds memory limits. Labels A–C match the design schematic in Figure 3*

![[assets/figures/papers/paper_list_l2073_https_arxiv_org_abs_2511_20645/figures/005_Figure_4.jpg]]
*Figure 4: | Qualitative results on ImageNet*

## 定位与知识库关联

### 像素空间扩散模型的技术脉络

PixelDiT 处于像素空间扩散模型这一研究脉络的前沿位置。传统扩散模型（如 **ADM-U**）虽直接在像素空间操作，但受限于 UNet 架构对全局语义建模能力的不足，生成质量长期落后于潜在空间方法。PixelDiT 的核心突破在于：**通过双层级 Transformer 架构解耦全局语义学习与局部纹理细化**，使像素空间扩散模型首次在 ImageNet 256×256 上达到 FID 1.61，显著超越同属像素空间阵营的 **PixelFlow-XL**（FID 1.98）和 **PixNerd-XL**（FID 2.09），并逼近最优潜在扩散模型的水平。

与潜在扩散模型（如 **DiT-XL**、**SiT-XL**、**SDXL**、**Flux-dev**）相比，PixelDiT 的根本差异在于**扩散空间的选择**：前者依赖预训练自编码器将图像压缩至低维潜在空间进行扩散，虽降低了计算开销，但自编码器的有损重建会丢失高频纹理细节；PixelDiT 则完全在像素空间端到端训练，消除了对自编码器的依赖，从原理上避免了信息瓶颈。这一设计哲学使其在需要高保真纹理的下游任务（如免训练图像编辑）中展现出独特优势。

### 适用边界与约束条件

1. **计算资源需求**：尽管 Pixel Token Compaction 机制有效降低了注意力序列长度，但像素空间建模的计算量仍显著高于同规模的潜在空间模型。Table 6 的消融实验表明，移除压缩机制会直接导致训练内存溢出（OOM），说明该设计是**训练可行性的必要条件而非锦上添花**。

2. **训练稳定性**：像素空间的速度预测训练易出现损失尖峰，尤其在深层架构和长训练周期中。论文虽提出了稳定化技巧（如 REPA 表示对齐），但完全消除尖峰而不牺牲训练效率仍是开放问题。Table 11 显示，移除 REPA 对齐损失会使 FID 从 2.36 骤升至 6.58（80 epoch），说明外部表示监督在当前框架中扮演着关键的稳定化角色。

3. **模型容量与数据规模瓶颈**：当前 PixelDiT-T2I 模型仅 1.3B 参数，在生成几何结构复杂或纹理精细的对象（如人手、复杂建筑）时仍存在困难。论文明确指出高质量训练数据的不足限制了文本到图像模型的进一步提升，这意味着**扩大模型容量与数据规模是突破当前质量天花板的关键路径**。

4. **Patch Size 的权衡**：Patch size $p=16$ 在质量与效率间取得最佳平衡（Table 13）；$p=32$ 虽可降低计算量，但 FID 显著恶化（3.78 vs 2.23 at 120 epochs），说明过大的 patch 会损害像素级细化的粒度优势。

### 在扩散模型知识库中的定位

PixelDiT 的贡献可映射到扩散模型设计的三个关键维度：

| 维度 | 传统像素扩散（ADM-U） | 潜在扩散（DiT/SiT） | PixelDiT |
|------|----------------------|---------------------|----------|
| 扩散空间 | 像素空间 | 潜在空间 | 像素空间 |
| 架构范式 | UNet | 单层 Transformer | 双层级 Transformer |
| 条件调制 | 全局 AdaLN | 全局 AdaLN | 像素级 AdaLN |
| 序列压缩 | 无/大 patch | 潜在压缩 | 像素 token 压缩 |

这种定位揭示了 PixelDiT 的**方法论本质**：它并非简单地回归像素空间，而是将潜在扩散模型中成熟的 Transformer 架构和条件调制策略**重新设计以适应像素空间的高分辨率特性**。像素级 AdaLN 和 Pixel Token Compaction 可视为对“如何在保持全局语义建模能力的同时实现高效的逐像素条件化”这一核心问题的系统性回答。

### 局限与开放问题

1. **损失尖峰的根治**：如何在像素空间扩散训练中完全消除损失尖峰而不牺牲训练效率，是当前方法面临的核心优化挑战。

2. **规模扩展的极限**：进一步扩大模型参数和训练数据规模能否突破当前质量瓶颈，达到并超越最优潜在扩散模型（如 Flux-dev 在 DPG-Bench 上的 84.8）的水平，尚待验证。

3. **下游任务的泛化优势**：像素空间扩散模型在免训练编辑中已展现初步优势，但其在可控生成、图像翻译等更广泛下游任务中是否具有超越潜在模型的系统性优势，仍需进一步探索。

4. **与其他像素空间方法的融合潜力**：如 **EPG-XXL/16** 和 **JiT-G** 等同样探索像素空间生成的工作，其技术路线（如高效采样策略、替代架构设计）与 PixelDiT 的双层级设计是否存在互补空间，是值得关注的交叉方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/PixelDiT_Pixel_Diffusion_Transformers_for_Image_Generation.pdf]]
