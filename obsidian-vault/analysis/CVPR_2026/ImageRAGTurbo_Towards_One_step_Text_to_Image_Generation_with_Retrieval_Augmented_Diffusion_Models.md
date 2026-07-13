---
title: "ImageRAGTurbo: Towards One-step Text-to-Image Generation with Retrieval-Augmented Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ImageRAGTurbo_Towards_One_step_Text_to_Image_Generation_with_Retrieval_Augmented_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- ImageRAGTurbo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
- topic/benchmarks_datasets_evaluation
core_operator: 通过检索与目标提示语义相关的文本-图像对，并将检索信息注入UNet去噪器的深层特征空间（H-space），可以降低去噪难度，提升提示忠实度。
primary_logic: UNet去噪器的H-space已编码高层语义信息；注入检索到的相关H-space特征可以简化从噪声到目标分布的映射，在极低步数（1步）下保持高保真度。
claims:
- 直接H-space注入（无训练）即可将TIFA分数从0.779提升至0.781；逐提示搜索最优混合强度后可达0.816，超越50步教师模型。
- ImageRAGTurbo在MS-COCO上CLIP分数0.323，优于SD Turbo (0.319)，FID更低 (25.59 vs 26.04)。
- ImageRAGTurbo在TIFA benchmark上达到0.801，接近50步教师模型(0.811)，且比SD Turbo提升2.2%，美学分数5.88 vs 5.83。
- MS-COCO 上 CLIP↑ = 0.323
---

# ImageRAGTurbo: Towards One-step Text-to-Image Generation with Retrieval-Augmented Diffusion Models

> [!tip] 核心洞察
> UNet去噪器的H-space已编码高层语义信息；注入检索到的相关H-space特征可以简化从噪声到目标分布的映射，在极低步数（1步）下保持高保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | ImageRAGTurbo：面向单步文本到图像生成的检索增强扩散模型 |
| 英文题名 | ImageRAGTurbo: Towards One-step Text-to-Image Generation with Retrieval-Augmented Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.12640) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video #topic/benchmarks_datasets_evaluation |
| Method | ImageRAGTurbo |
| Dataset | MS-COCO, TIFA benchmark |

> [!tip] 效果简介
> - MS-COCO 上，CLIP↑ 0.323 vs 0.319 (SD Turbo) (+0.004 (+1.3%))；FID↓ 25.59 vs 26.04 (SD Turbo) (-0.45)。
> - TIFA benchmark 上，TIFA↑ 0.801 vs 0.811 (SD v2-1 50-step Teacher) (-0.010)；TIFA↑ (vs SD Turbo) 0.801 vs ≈0.784 (SD Turbo) (+0.017 (+2.2%))；AES↑ 5.88 vs 5.83 (SD Turbo) (+0.05)。

## 概要

**核心问题**：少步扩散模型（如 **Stable Diffusion Turbo** (Sauer et al., ECCV 2024)）虽大幅降低了推理步数，但在单步生成时牺牲了图像质量和提示对齐度，尤其难以准确生成特定视觉概念。

**核心方法**：ImageRAGTurbo 提出一种检索增强的少步扩散微调框架——给定目标文本提示，从数据库检索语义相关的文本-图像对，将其注入 UNet 去噪器的深层 H-space 特征空间，以降低去噪难度并提升提示忠实度。

**核心发现**：UNet 去噪器的 H-space 已编码高层语义信息；注入检索到的相关 H-space 特征可以简化从噪声到目标分布的映射，在极低步数（1步）下保持高保真度。直接 H-space 注入（无训练）即可将 TIFA 分数从 0.779 提升至 0.781；逐提示搜索最优混合强度后可达 0.816，超越 50 步教师模型。

**主要结果**：
- 在 MS-COCO 上，ImageRAGTurbo 单步生成 CLIP 分数 0.323，优于 SD Turbo (0.319)，FID 更低 (25.59 vs 26.04)。
- 在 TIFA benchmark 上，TIFA 分数 0.801，接近 50 步教师模型 **Stable Diffusion v2-1-base** (Rombach et al., CVPR 2022) 的 0.811，比 SD Turbo 提升 2.2%；美学分数 5.88 vs 5.83。
- 仅需训练轻量 H-space 适配器（36M 参数，占模型 4%）和解码器 LoRA，冻结 UNet 主体，训练成本极低。

**方法定位**：ImageRAGTurbo 属于检索增强生成与扩散模型效率优化的交叉方向，区别于 **RDM** (Blattmann et al., NeurIPS 2022) 的多步检索增强和 **LCM** (Luo et al., arXiv 2023) 的自一致性蒸馏路线，首次将检索增强引入少步/单步扩散模型微调，且通过 H-space 特征融合而非外部条件注入实现高效适配。

### 扩散模型加速的核心瓶颈

扩散模型在文本到图像生成领域取得了显著进展，但其推理过程需要多次迭代去噪，计算成本高昂。以 **Stable Diffusion v2-1-base**（Rombach et al., CVPR 2022）为例，标准配置需要50步去噪函数评估（NFE）才能生成高质量图像。为降低推理延迟，研究者提出了多种加速策略：

- **对抗蒸馏路线**：**Stable Diffusion Turbo (SD Turbo)**（Sauer et al., ECCV 2024）通过对抗蒸馏将步数压缩至2步，但单步生成时图像质量和提示对齐度显著下降。
- **自一致性训练路线**：**Latent Consistency Model (LCM)**（Luo et al., arXiv 2023）通过约束相邻时间步的预测一致性实现少步生成，但在极低步数下仍面临保真度损失。
- **其他蒸馏方法**：**ECCV-SD**（Kang et al., ECCV 2024）等蒸馏方案同样在单步场景下难以维持教师模型的生成质量。

这些方法的共同缺口在于：当步数压缩至极限（1-2步）时，去噪器缺乏足够的上下文信息来准确还原复杂视觉概念，导致**提示忠实度**和**图像质量**的双重退化。具体而言，少步扩散模型在生成特定对象、属性或空间关系时容易出现遗漏或错位，这在TIFA benchmark上表现为约2-3%的分数差距。

### 检索增强的潜在机遇

与此同时，**检索增强生成（Retrieval-Augmented Generation, RAG）**在自然语言处理领域已证明其有效性——通过从外部知识库检索相关信息来增强生成质量。在文本到图像生成中，**Retrieval-Augmented Diffusion Model (RDM)**（Blattmann et al., NeurIPS 2022）率先将检索机制引入多步扩散模型，但其设计依赖完整去噪过程，未针对少步场景进行优化。

本文的核心洞察在于：UNet去噪器的**H-space**（即编码器最深层的特征空间）已编码高层语义信息，通过注入从检索数据库中获取的相关文本-图像对的特征，可以有效降低从噪声到目标分布的映射难度。这一机制在极低步数下尤为关键——检索提供的额外语义上下文弥补了因步数减少而损失的迭代细化能力。

### 本文动机与目标

基于上述分析，本文提出 **ImageRAGTurbo**，旨在解决以下核心问题：

1. **少步生成的质量瓶颈**：如何在仅1步推理的条件下，维持与50步教师模型相当的提示忠实度和图像质量？
2. **检索增强的高效融合**：如何设计轻量级机制，将检索信息无缝注入少步扩散模型的去噪流程，同时避免引入过大的计算开销？
3. **训练效率**：能否通过参数高效微调（而非全模型重训练）实现检索增强适配，降低训练成本？

初步实验验证了该方向的可行性：在无训练条件下，直接通过球形归一化插值将检索H-space特征注入目标去噪分支，即可将TIFA分数从0.779提升至0.781；逐提示搜索最优混合强度后，TIFA分数可达0.816，**超越50步教师模型**。这一结果表明，检索增强有潜力从根本上改变少步扩散模型的性能上限。

## 核心方法与创新机理

ImageRAGTurbo 的核心创新在于将**检索增强生成（RAG）**范式系统性地引入少步扩散模型，通过改造 UNet 去噪器的深层特征空间（H-space）实现高效、低成本的提示忠实度提升。其关键创新点可归纳为三个相互耦合的 changed slots。

### 1. 检索增强机制：从单一提示到多模态上下文注入

传统少步扩散模型（如 **Stable Diffusion Turbo**，Sauer et al., ECCV 2024）仅依赖目标文本提示进行生成，在单步或极少步数下难以准确还原细粒度视觉概念。ImageRAGTurbo 改变了这一范式：给定目标提示，系统首先从外部数据库中检索语义最相关的文本-图像对，并将检索信息作为额外条件注入生成流程。这一机制的本质是**用检索到的“范例”降低从纯噪声到目标分布的映射难度**——去噪器不再需要从零开始“想象”一个罕见概念，而是可以从检索到的相似视觉-语义特征中获得引导。该设计直接对应分析中识别的瓶颈：少步模型在单步生成时牺牲了提示对齐度，尤其难以生成准确的视觉概念。

### 2. H-space 特征融合方式：从固定插值到可学习适配器

检索增强的核心技术挑战在于**如何将检索到的信息有效融入去噪过程**。ImageRAGTurbo 经历了从简单到自适应的两阶段探索：

- **球形归一化插值（无训练基线）**：直接在 H-space 中沿测地线混合检索特征 $h_t^{\mathrm{retr}}$ 和目标特征 $h_t^{\mathrm{tgt}}$，公式为：
  $$\pmb{h}_t^{\mathrm{blend}} = \frac{\sin[(1-w)\Omega_t]}{\sin\Omega_t} \pmb{h}_t^{\mathrm{retr}} + \frac{\sin[w\Omega_t]}{\sin\Omega_t} \pmb{h}_t^{\mathrm{tgt}}$$
  其中 $w$ 控制混合强度。实验表明，固定 $w=0.8$ 可将 TIFA 分数从 0.779 提升至 0.781，但提升幅度有限。

- **可训练 H-space 适配器（核心方案）**：引入一个轻量级交叉注意力模块 $g_{\varphi}$，自动学习检索特征与目标特征之间的相关性：
  $$g_{\varphi}(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}}) = \mathrm{softmax}(\frac{Q K^{\top}}{\sqrt{d_k}}) V$$
  其中 $Q$ 由目标特征投影得到，$K$、$V$ 由检索特征投影得到。适配器的输出作为残差更新：
  $$h_t^{\mathrm{retr}} = h_t^{\mathrm{tgt}} + \lambda \cdot g_{\varphi}(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}})$$
  $\lambda$ 设为检索文本与目标文本 CLIP 嵌入的余弦相似度，起到门控作用——检索越相关，注入强度越大。这一设计使逐提示搜索最优混合强度后 TIFA 可达 0.816，**超越了 50 步教师模型**，验证了自适应融合的必要性。

### 3. 训练策略：冻结 UNet 的极低参数微调

与 SD Turbo 等需要对整个 UNet 进行对抗蒸馏的方法不同，ImageRAGTurbo 采用**冻结 UNet 主干、仅训练 H-space 适配器和解码器 LoRA** 的策略。具体而言：
- H-space 适配器仅增加 36M 参数，占模型总参数的 4%；
- 解码器通过低秩适配（LoRA）进行参数高效微调；
- 训练目标融合了对抗损失 $\mathcal{L}_{\mathrm{adv}}$、蒸馏损失 $\mathcal{L}_{\mathrm{distill}}$ 和潜在 LPIPS 损失 $\mathcal{L}_{\mathrm{latentLPIPS}}$：
  $$\mathcal{L} = \mathcal{L}_{\mathrm{adv}} + 2.5 \cdot \mathcal{L}_{\mathrm{distill}} + 1.0 \cdot \mathcal{L}_{\mathrm{latentLPIPS}}$$

这一策略大幅降低了训练成本，同时保持了生成质量。消融实验表明，移除检索增强（即退化为标准 SD Turbo）会导致 CLIP 和 TIFA 分数显著下降，验证了检索模块对提示忠实度的关键贡献。

### 创新点之间的因果链条

上述三个创新点构成一条清晰的因果链：**检索增强**提供额外的语义上下文 → **H-space 适配器**自适应地将检索信息融入去噪过程 → **轻量训练策略**使这一增强在极低计算开销下实现。三者共同支撑了核心洞察：UNet 的 H-space 已编码高层语义信息，注入检索到的相关 H-space 特征可以简化从噪声到目标分布的映射，在单步生成下保持高保真度。

ImageRAGTurbo 的核心思想是在少步扩散模型的去噪过程中注入检索增强信息，从而在不增加推理步数的前提下提升生成质量与提示忠实度。框架由两条并行的处理分支构成：**标准去噪分支**（绿色）和**检索分支**（紫色），二者在 UNet 去噪器的 H‑space 中通过一个可训练的适配器进行融合（见 Figure 2）。

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed ImageRAGTurbo framework for efficiently finetuning the few-step diffusion models with retrievalaugmented generation. The framework involves two main branches: i) a standard denoising branch (highlighted by green), and ii) a retrieval branch (highlighted by purple). For a target prompt*

### 标准去噪分支

给定目标文本提示 $p^{\mathrm{tgt}}$，首先通过冻结的文本编码器 $\tau_\phi$ 将其编码为嵌入向量。同时，从标准正态分布采样初始噪声潜在变量 $z_T$，与时间步 $t$ 一同送入 UNet 编码器 $f_\theta^{\mathrm{enc}}$，提取出目标 H‑space 特征：

$$h_t^{\mathrm{tgt}} = f_\theta^{\mathrm{enc}}\big(\tau_\phi(p^{\mathrm{tgt}}), t, z_t\big)$$

该特征编码了目标提示在当前去噪阶段的高层语义信息，是后续融合的基础。

### 检索分支

检索分支负责为生成过程提供外部上下文。具体流程如下：

1. **检索**：使用目标文本的 CLIP 嵌入在预构建的数据库中检索语义最相似的文本‑图像对。
2. **编码**：将检索到的文本‑图像对（以潜在变量形式存储）与目标提示嵌入拼接后，送入同一个 UNet 编码器，得到检索 H‑space 特征 $h_t^{\mathrm{retr}}$。
3. **融合**：$h_t^{\mathrm{retr}}$ 通过 H‑space 适配器 $g_\varphi$ 与目标特征 $h_t^{\mathrm{tgt}}$ 进行交叉注意力交互，产生适应性特征更新 $\Delta h_t$。最终检索增强特征为：

$$h_t^{\mathrm{aug}} = h_t^{\mathrm{tgt}} + \lambda \cdot g_\varphi(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}})$$

其中 $\lambda$ 为检索文本与目标文本 CLIP 嵌入的余弦相似度，用于自适应调节检索信息的注入强度——当检索结果与目标语义高度相关时，注入更多外部信息；反之则减少干扰。

### H‑space 适配器

适配器 $g_\varphi$ 是整个框架中唯一需要从零训练的核心模块（参数约 36M，仅占模型总参数的 4%）。它通过交叉注意力机制自动学习目标特征与检索特征之间的相关性：

$$g_\varphi(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}}) = \mathrm{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V$$

其中 $Q = W_Q \cdot h_t^{\mathrm{tgt}}$，$K = W_K \cdot h_t^{\mathrm{retr}}$，$V = W_V \cdot h_t^{\mathrm{retr}}$。这种设计使适配器能够根据目标提示的不同部分，有选择地关注检索特征中的相关语义区域，避免了早期实验中固定混合强度 $w$ 需要逐提示穷举搜索的局限——实验表明，固定 $w=0.8$ 仅将 TIFA 分数从 0.779 提升至 0.781，而逐提示搜索最优权重可提升至 0.816，充分说明了自适应融合的必要性。

### 解码与训练策略

融合后的特征 $h_t^{\mathrm{aug}}$ 进入 UNet 解码器，结合目标提示嵌入预测去噪后的潜在变量 $\hat{z}_0$，最终由冻结的 VAE 解码器投影回图像空间。为在极低步数下保持生成质量，训练策略采用了“冻结主干、轻量微调”的方案：

- **冻结 UNet 编码器**：保留教师模型（Stable Diffusion v2‑1‑base）的预训练知识。
- **训练 H‑space 适配器**：学习检索特征与目标特征的最优融合方式。
- **LoRA 微调解码器**：以参数高效的方式适配解码器，提升少步去噪能力。
- **对抗训练**：鉴别器由冻结的教师 UNet 编码器和可训练投影层组成，在潜在空间中对学生模型输出与教师模型输出进行判别（见 Figure 4）。

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/004_Figure_4.jpg]]
*Figure 4: The architecture of the discriminator used for latent adversarial training, which adds noise to the samples*

最终训练目标为三项损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{adv}} + \alpha \mathcal{L}_{\mathrm{distill}} + \beta \mathcal{L}_{\mathrm{latentLPIPS}}$$

其中 $\alpha=2.5$，$\beta=1.0$ 为经验设定的权重。对抗损失提供分布层面的监督，蒸馏损失对齐学生与教师的预测输出，潜在 LPIPS 损失则在 VAE 潜在空间中保持感知相似度。

### 推理流程

推理时，整个流程仅需一次 UNet 前向传播（单步生成），即可完成从噪声到图像的映射。检索分支的引入虽然增加了额外的编码开销，但由于检索特征提取可与目标分支并行执行，且适配器计算量极小，整体推理延迟仍显著优于多步扩散模型（见 Figure 6 的延迟对比）。

ImageRAGTurbo 的核心设计围绕一个关键洞察展开：UNet 去噪器的 H-space（深层特征空间）已编码高层语义信息，注入检索到的相关 H-space 特征可以简化从噪声到目标分布的映射，从而在极低步数下保持高保真度。基于此，方法在冻结的少步扩散模型上引入两条分支和一个轻量级适配器，以检索增强的方式引导生成。

### 双分支架构与 H-space 特征提取

框架由两条并行的 UNet 编码器通路构成（Figure 2）：

1. **目标去噪分支**：接收噪声潜在变量 $z_t$、时间步 $t$ 和目标提示 $p^{\mathrm{tgt}}$ 的文本嵌入 $\tau_\phi(p^{\mathrm{tgt}})$，经过 UNet 编码器 $f_\theta^{\mathrm{enc}}$ 提取目标 H-space 特征：
   $$h_t^{\mathrm{tgt}} = f_\theta^{\mathrm{enc}}(\tau_\phi(p^{\mathrm{tgt}}), t, z_t)$$

2. **检索分支**：基于目标文本的 CLIP 嵌入从数据库中检索最相似的文本-图像对，将其文本-潜在嵌入输入同一 UNet 编码器，得到检索 H-space 特征 $h_t^{\mathrm{retr}}$。

### 球形归一化插值（直接注入基线）

在引入可训练适配器之前，论文首先验证了直接 H-space 特征融合的有效性。采用球形归一化插值（而非线性插值），沿测地线混合检索与目标特征，实现更平滑的语义过渡：

$$h_t^{\mathrm{blend}} = \frac{\sin[(1-w)\Omega_t]}{\sin\Omega_t} h_t^{\mathrm{retr}} + \frac{\sin[w\Omega_t]}{\sin\Omega_t} h_t^{\mathrm{tgt}}$$

其中 $\Omega_t = \arccos(\langle h_t^{\mathrm{retr}}, h_t^{\mathrm{tgt}} \rangle)$ 为两特征向量之间的角度，$w \in [0,1]$ 控制混合强度。实验表明，固定 $w=0.8$ 即可将 TIFA 分数从 0.779 提升至 0.781；逐提示搜索最优 $w^*$ 后可达 0.816，超越 50 步教师模型（Figure 3）。这一结果直接证实了 H-space 语义注入的有效性，但固定权重无法适应不同提示的语义差异，因此需要自适应融合机制。

### H-space 适配器（可训练融合模块）

为解决固定权重的局限，论文引入可训练适配器 $g_\varphi$，通过交叉注意力自动学习检索特征与目标特征之间的相关性。适配器以目标 H-space 特征作为查询（Query）、检索 H-space 特征作为键（Key）和值（Value），计算适应性特征更新：

$$g_{\varphi}(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}}) = \mathrm{softmax}\left(\frac{Q K^{\top}}{\sqrt{d_k}}\right) V$$

其中 $Q = W_Q \cdot h_t^{\mathrm{tgt}}$，$K = W_K \cdot h_t^{\mathrm{retr}}$，$V = W_V \cdot h_t^{\mathrm{retr}}$，$W_Q, W_K, W_V$ 为可训练的投影矩阵。

适配器的输出 $\Delta h_t = g_\varphi(h_t^{\mathrm{tgt}}, h_t^{\mathrm{retr}})$ 表示检索特征对目标特征的语义增强量，最终通过残差连接与缩放因子 $\lambda$ 更新目标 H-space 特征：

$$h_t^{\mathrm{retr}} = h_t^{\mathrm{tgt}} + \lambda \cdot \Delta h_t$$

其中 $\lambda$ 被设置为检索文本与目标文本 CLIP 嵌入的余弦相似度，起到门控作用：当检索内容与目标提示语义高度相关时，增强量较大；反之则减小检索影响，避免引入无关信息。

### 训练策略与损失函数

为高效微调少步扩散模型，ImageRAGTurbo 冻结 UNet 的主体参数，仅训练以下组件：

- **H-space 适配器 $g_\varphi$**（约 36M 参数，仅占模型总参数的 4%）
- **UNet 解码器的 LoRA 低秩适配**（参数高效微调）
- **鉴别器 $D$ 的可训练投影层**（鉴别器主体使用冻结的教师 UNet 编码器，Figure 4）

训练损失由三项加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{adv}} + \alpha \mathcal{L}_{\mathrm{distill}} + \beta \mathcal{L}_{\mathrm{latentLPIPS}}$$

- $\mathcal{L}_{\mathrm{adv}}$：潜在空间对抗损失，使用带噪声增强的鉴别器区分学生生成样本与教师真实样本
- $\mathcal{L}_{\mathrm{distill}}$：蒸馏损失，约束学生输出与教师输出的分布一致性
- $\mathcal{L}_{\mathrm{latentLPIPS}}$：潜在空间 LPIPS 感知损失，保持生成图像的感知质量

权重经验性地设为 $\alpha=2.5$，$\beta=1.0$。这种轻量级训练策略在保持生成质量的同时大幅降低了计算开销，使方法能够高效适配已有的少步扩散模型。

### 关键设计选择总结

| 设计选择 | 动机 | 效果 |
|---------|------|------|
| 在 H-space 而非像素空间融合 | H-space 编码高层语义，融合更高效 | 直接注入即可提升 TIFA |
| 球形插值而非线性插值 | 测地线路径提供更平滑的语义过渡 | 避免语义突变 |
| 交叉注意力适配器 | 自适应学习检索-目标相关性 | 逐提示动态调整融合强度 |
| 余弦相似度门控 $\lambda$ | 抑制不相关检索的负面影响 | 提升鲁棒性 |
| 冻结 UNet + LoRA 解码器 | 减少可训练参数，保持预训练知识 | 适配器仅占 4% 参数 |

## 实验与关键发现

### 核心定量结果

ImageRAGTurbo在MS-COCO和TIFA两个基准上均展现出相对于少步基线的显著提升，尤其在提示忠实度维度上实现了对教师模型的逼近甚至超越。

**MS-COCO基准（Table 1）**：在单步生成设定下，ImageRAGTurbo取得CLIP分数0.323，优于**SD Turbo**（Sauer et al., ECCV 2024）的0.319（+1.3%），同时FID降至25.59（SD Turbo为26.04）。这一结果验证了检索增强在提升文本-图像语义对齐的同时，并未牺牲图像质量。与检索增强多步基线**RDM**（Blattmann et al., NeurIPS 2022）相比，CLIP分数提升约10%（0.323 vs 0.293），表明H-space注入策略比早期检索增强方法更有效。值得注意的是，ImageRAGTurbo仅需1次去噪函数评估（NFE），而教师模型需50次，推理效率提升50倍。

**TIFA基准（Table 2）**：ImageRAGTurbo的TIFA分数达到0.801，比SD Turbo提升约2.2%（绝对提升约0.017），接近50步教师模型**Stable Diffusion v2-1-base**（Rombach et al., CVPR 2022）的0.811（差距仅0.010）。美学分数（AES）方面，ImageRAGTurbo达到5.88，略高于SD Turbo的5.83，表明检索增强在提示忠实度和美学质量上均带来正向增益。

### 消融实验与机制验证

**检索增强的必要性**：移除检索增强（即退化为标准SD Turbo）导致CLIP分数和TIFA分数均显著下降（Table 1和Table 2中SD Turbo的对应指标），直接验证了检索信息对提示忠实度的关键贡献。这一消融本质上证明了“仅靠目标提示”在少步去噪中的信息不足问题——检索提供的相关文本-图像对有效降低了从噪声到目标分布的映射难度。

**H-space直接注入的潜力与局限（Figure 3）**：在无训练设定下，使用固定混合强度w=0.8的球形归一化插值（Eq. 3）直接将检索H-space特征注入去噪分支，即可将TIFA分数从0.779提升至0.781。这一微小但稳定的提升表明：UNet的H-space确实编码了高层语义信息，且检索特征与目标特征在该空间中的简单线性混合已能带来边际收益。然而，当对每个提示进行穷举搜索以确定最优混合强度w*时，TIFA分数跃升至0.816，甚至超越50步教师模型。这一发现揭示了两个关键洞察：其一，最优混合强度高度依赖于具体提示的语义特性，固定权重无法充分发挥检索潜力；其二，H-space特征的语义信息密度远超预期，精确的融合控制可以弥补少步去噪的信息损失。这直接驱动了可训练适配器g_φ的设计——通过交叉注意力机制（Eq. 4）自动学习目标与检索特征之间的相关性，替代手工调参。

**训练策略的效率验证**：冻结UNet主体参数，仅训练H-space适配器（36M参数，仅占总模型参数的4%）和解码器LoRA，在保持生成质量的同时大幅降低了训练开销。这一设计使得检索增强可以作为一种轻量级“插件”应用于已有的少步扩散模型，无需从头进行全模型对抗蒸馏。

### 失败模式与局限性分析

尽管整体性能优异，ImageRAGTurbo仍存在若干可识别的失败模式：

1. **检索质量依赖性**：当前实现依赖基于CLIP的全局文本嵌入进行检索，当目标提示涉及复杂组合概念（如“一只戴着红色帽子的猫在蓝色沙发上睡觉”）或细粒度属性（如特定材质、纹理）时，全局检索可能返回语义相关但视觉细节不匹配的图像，导致生成结果中视觉概念的准确性下降。论文明确指出“探索组合式检索是一个有前景的方向”。

2. **类别间性能不均衡（Figure 5）**：在TIFA基准的各类别细分中，1步ImageRAGTurbo在object、activity和material等类别上达到甚至略超50步教师模型，但在color、counting等需要精确属性绑定的类别上仍明显落后。这表明H-space特征融合在传递“存在性”语义（某物体是否存在）方面表现优异，但在传递“约束性”语义（物体的具体属性值）方面仍有不足。

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/007_Figure_5.jpg]]
*Figure 5: Detailed histogram of TIFA scores across various categories. Despite still lagging behind 50-step Stable Diffusion v2-1-base model, our 1-step ImageRAGTurbo achieves comparable or even slightly higher TIFA score in certain categories such as object, activity, and material*

3. **基础模型迁移未验证**：所有训练和评估均基于Stable Diffusion v2-1-base，该框架在其他基础模型（如SDXL、扩散Transformer架构）上的泛化性尚未经验证。不同模型的H-space语义结构可能存在差异，适配器设计可能需要相应调整。

4. **噪声检索鲁棒性未分析**：论文未深入探讨当检索数据库覆盖度不足或检索结果高度噪声时，H-space注入是否会引入伪影或错误语义。在极端情况下，检索到完全不相关的图像可能导致生成质量劣于无检索基线，这一风险在实际部署中需要关注。

### 推理效率

在推理延迟方面（Figure 6），ImageRAGTurbo在单张NVIDIA L40S GPU上、512×512分辨率下的平均推理时间与SD Turbo处于同一量级（具体数值需参考原图，论文未在文本中给出精确毫秒数），检索和H-space适配器的额外计算开销被控制在极小范围内。这得益于检索过程在CLIP嵌入空间中完成（仅需一次前向传播），且适配器仅涉及轻量级交叉注意力运算。

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/008_Figure_6.jpg]]
*Figure 6: Comparison of inference time (ms/image). We report the average inference time calculated over the same set of 100 prompts at 512 × 512 resolution on a single NVIDIA L40S GPU*

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of text-to-image generation models on the MS-COCO benchmark measured by the FID and CLIP scores, as well as the number of function evaluations (NFE) in the denoising process*

![[assets/figures/papers/paper_list_l2317_https_arxiv_org_abs_2602_12640/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative results of ImageRAGTurbo. ImageRAGTurbo can generate high-quality images in a single step (Left) and achieves better text-to-image alignment compared to other competing few-step methods (Right)*

## 定位与知识库关联

### 核心问题定位：少步扩散的语义瓶颈

少步扩散模型通过在仅1–4步的推理中逼近多步教师模型的生成分布，大幅降低了延迟，但其代价是图像质量与提示对齐度的显著下降。以 **Stable Diffusion Turbo**（Sauer et al., ECCV 2024）为代表的对抗蒸馏方法，在单步生成时尤其难以准确渲染复杂或罕见的视觉概念。这一瓶颈的根源在于：从纯噪声到目标分布的映射在极低步数下变得高度病态，去噪器缺乏足够的计算预算来解析提示中的细粒度语义约束。

### 方法谱系中的位置

ImageRAGTurbo 处于“少步扩散生成”与“检索增强生成”两条技术路线的交汇点。其直接对标的方法包括：

- **少步扩散基线**：**Stable Diffusion Turbo**（Sauer et al., ECCV 2024）作为对抗蒸馏的两步模型，是本文的核心对比对象；**Latent Consistency Model (LCM)**（Luo et al., arXiv 2023）基于自一致性训练实现少步生成；**ECCV-SD**（Kang et al., ECCV 2024）采用另一种蒸馏策略。这些方法的共同特征是完全依赖目标提示进行生成，缺乏外部知识注入机制。

- **检索增强扩散基线**：**Retrieval-Augmented Diffusion Model (RDM)**（Blattmann et al., NeurIPS 2022）率先将检索信息引入多步扩散流程，但其设计面向标准的多步推理，未针对少步场景进行适配或优化。

ImageRAGTurbo 的关键区别在于：它在少步扩散模型的**特征空间（H-space）**层面进行检索增强，而非在输入空间或文本嵌入层面。这一选择基于一个核心洞察——UNet 去噪器的 H-space 已编码高层语义信息，注入检索到的相关 H-space 特征可以直接简化从噪声到目标分布的映射路径，从而在极低步数（1步）下保持提示忠实度。

### 技术贡献的适用边界

**适用前提**：
1. 需要预训练的去噪扩散模型作为教师（本文使用 **Stable Diffusion v2-1-base**，Rombach et al., CVPR 2022），且其 UNet 的 H-space 结构可被访问和修改。
2. 需要一个覆盖目标概念域的文本-图像检索数据库；检索质量直接影响生成效果。
3. 训练策略假设冻结 UNet 主体，仅训练轻量级 H-space 适配器（36M 参数，仅占模型总量的 4%）和解码器 LoRA 模块，大幅降低了计算开销。

**已验证的边界**：
- 在 MS-COCO 和 TIFA benchmark 上，ImageRAGTurbo 在单步推理下实现了 CLIP 分数 0.323（vs SD Turbo 0.319，+1.3%）和 FID 25.59（vs SD Turbo 26.04），TIFA 分数 0.801（vs SD Turbo 约 0.784，+2.2%），美学分数 5.88（vs SD Turbo 5.83）。
- 直接 H-space 注入（无训练）即可将 TIFA 从 0.779 提升至 0.781；逐提示搜索最优混合强度后可达 0.816，**超越 50 步教师模型**（0.811），表明 H-space 特征的语义信息密度极高，且自适应融合策略至关重要。

**未经验证的边界**：
1. **基础模型泛化性**：所有实验均基于 Stable Diffusion v2-1-base，该方法在 SDXL、扩散 Transformer（如 DiT）等架构上的有效性尚待验证。
2. **检索鲁棒性**：论文未分析噪声检索或检索失败（如数据库覆盖不足）情况下的性能退化程度。
3. **复杂组合提示**：当前基于 CLIP 的全局检索可能无法精确捕捉涉及多个对象、属性或空间关系的组合式提示，这限制了其在细粒度可控生成场景中的适用性。

### 局限与开放问题

**已识别的局限**：
- 检索机制依赖 CLIP 全局相似度，对组合式概念和细粒度属性的捕捉能力有限。
- 训练和评估均绑定于单一教师模型，跨架构迁移的可行性未知。

**值得探索的开放方向**：
1. **细粒度检索增强**：设计图像区域级或属性级的检索与注入机制，以提升对复杂提示的忠实度。这可能需要将检索粒度从“整图”下推到“语义区域”或“属性-值对”。
2. **动态检索策略**：在推理时自适应地决定检索数量、混合强度或是否触发检索，以平衡性能与鲁棒性。当前逐提示搜索最优权重的方案（TIFA 0.816）虽然有效，但不可部署。
3. **多模态大语言模型（MLLM）集成**：将 MLLM 引入检索筛选和评估环节，在保持低延迟的前提下实现更智能的检索增强，可能是将框架推向实用化的关键一步。
4. **跨架构扩展**：验证该框架在更高分辨率生成任务（如 1024×1024）和其他基础模型（如 SDXL、扩散 Transformer）上的迁移能力，将决定其技术影响力的广度。

## 原文 PDF

![[paperPDFs/CVPR_2026/ImageRAGTurbo_Towards_One_step_Text_to_Image_Generation_with_Retrieval_Augmented_Diffusion_Models.pdf]]
