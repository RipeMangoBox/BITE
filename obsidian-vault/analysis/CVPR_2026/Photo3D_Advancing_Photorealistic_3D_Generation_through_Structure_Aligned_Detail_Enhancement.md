---
title: "Photo3D: Advancing Photorealistic 3D Generation through Structure-Aligned Detail Enhancement"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Photo3D_Advancing_Photorealistic_3D_Generation_through_Structure_Aligned_Detail_Enhancement.pdf
project_link: "https://liangsanzhu.github.io/photo3d-page/"
code_link: null
aliases:
- Photo3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 利用 GPT-4o-Image 增强 3D 渲染视图，构建与 3D 几何对齐、细节丰富且具有多视图一致性的 Photo3D-MV 数据集，并据此设计放松的细节增强方案以驱动真实感训练。
primary_logic: 通过随机裁剪 CLIP 感知特征适应和 DINOv3 语义结构匹配的放松监督，既能注入真实感纹理细节，又能保持与原有 3D 原生结构的一致性，避免像素级监督导致的几何失真。
claims:
- Photo3D 在 ImageNet 和 Real 3D 数据集上的所有真实感指标（MANIQA、MUSIQ、Gemini 胜率、人类评分）均显著优于现有 3D-native 生成器。
- 消融实验证实 L_adapt 和 L_match 联合使用是产生高真实感细节和稳定结构的关键，单独移除二者均导致质量明显下降。
- Photo3D 在不同 3D 生成范式（耦合式 Trellis、多视图纹理 Step1X-3D、单步纹理 TexGaussian）上均能一致提升真实感而不损害几何质量。
- ImageNet (selected top 1000 aesthetic) 上 MANIQA↑ / MUSIQ↑ = 0.470 / 72.385 (Photo3D (Trellis))
---

# Photo3D: Advancing Photorealistic 3D Generation through Structure-Aligned Detail Enhancement

> [!tip] 核心洞察
> 通过随机裁剪 CLIP 感知特征适应和 DINOv3 语义结构匹配的放松监督，既能注入真实感纹理细节，又能保持与原有 3D 原生结构的一致性，避免像素级监督导致的几何失真。

| 字段 | 内容 |
|------|------|
| 中文题名 | Photo3D：通过结构对齐细节增强推进照片级真实感 3D 生成 |
| 英文题名 | Photo3D: Advancing Photorealistic 3D Generation through Structure-Aligned Detail Enhancement |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.08535) · [Project](https://liangsanzhu.github.io/photo3d-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Photo3D |
| Dataset | ImageNet, Real 3D Datasets |

> [!tip] 效果简介
> - ImageNet (selected top 1000 aesthetic) 上，MANIQA↑ / MUSIQ↑ 0.470 / 72.385 (Photo3D (Trellis)) vs 0.438 / 69.108 (Trellis) (+0.032 / +3.277)。
> - Real 3D Datasets (GSO, Omni3D, DTC) 上，MANIQA↑ / MUSIQ↑ 0.459 / 65.724 (Photo3D (Trellis)) vs 0.427 / 64.155 (Trellis) (+0.032 / +1.569)。
> - ImageNet 上，Gemini-2.5 胜率% / 人类评分 (1–5) 95.0% / 4.4 (Photo3D (Trellis)) vs 68.1% / 3.4 (Trellis) (+26.9% / +1.0)。

## 概述

### 问题背景

近年来，3D 原生生成方法在物体几何建模上取得了显著进展，但在生成照片级真实感外观方面仍存在明显不足。现有 3D 生成器（如 **Trellis** (Xiang et al., CVPR 2025)、**3DTopia-XL** (Chen et al., arXiv 2024)、**Hunyuan3D 2.0** (Zhao et al., arXiv 2025) 等）通常依赖 Objaverse 等合成 3D 资产数据集进行训练，这些数据缺乏真实世界中丰富多样的纹理细节，导致生成结果在外观上呈现明显的“合成感”。根本瓶颈在于：缺乏一个与 3D 几何对齐、同时具备高质量真实感纹理细节的大规模数据集，以及能够有效利用此类数据驱动真实感训练的训练范式。

### 核心思路

Photo3D 的核心洞察是：**通过放松的感知与语义监督，可以在保持 3D 原生结构一致性的前提下，向生成器注入真实感纹理细节**。具体而言，Photo3D 构建了一个名为 **Photo3D-MV** 的数据集——利用 GPT-4o-Image 对 3D 渲染视图进行细节增强，生成与原始几何结构对齐但纹理更丰富、更具真实感的多视图图像。在训练阶段，Photo3D 设计了由两个互补损失组成的放松监督方案：

- **感知特征适应损失** $\mathcal{L}_{\mathrm{adapt}}$：通过随机裁剪的 CLIP 嵌入空间对齐，引导生成图像在语义层面逼近真实细节，而非逐像素匹配。
- **语义结构匹配损失** $\mathcal{L}_{\mathrm{match}}$：基于 DINOv3 的 patch 级特征匹配，在局部语义结构上建立生成图像与真值之间的对应关系，防止纹理漂移和几何失真。

这种“放松监督”策略的关键优势在于：它允许模型学习真实感外观的统计先验，同时避免像素级 L2 损失所导致的过约束和纹理崩塌问题。

### 方法定位

Photo3D 并非一个独立的 3D 生成器，而是一种**通用的真实感细节增强框架**，可适配三种主流的 3D 生成范式：

1. **几何-纹理耦合扩散模型**（如 Trellis）：将真实感损失直接注入扩散去噪过程，使生成器在采样时即输出具有真实感纹理的 3D 资产。
2. **单步 3D 原生纹理模型**（如 **TexGaussian** (Xiong et al., CVPR 2025)）：在纹理预测阶段施加真实感监督，提升前馈纹理生成的质量。
3. **扩散式多视图纹理模型**（如 **Step1X-3D** (Li et al., arXiv 2025)）：在多视图纹理合成过程中融入真实感先验，增强纹理的细节丰富度和跨视图一致性。

与 **Real3D** (Jiang et al., ICML 2023) 等采用单视图对抗监督的方法不同，Photo3D 通过多视图对齐的放松感知损失，实现了真实感与 3D 结构稳定性的更好平衡。

### 主要结果

在 ImageNet（精选 top 1000 高美学图像）和真实 3D 扫描数据集（GSO、Omni3D、DTC）上的实验表明，Photo3D 在各项真实感指标上均显著优于现有方法：

- **MANIQA** 得分从 Trellis 的 0.438 提升至 0.470（ImageNet），从 0.427 提升至 0.459（真实 3D 数据集）。
- **MUSIQ** 得分从 69.108 提升至 72.385（ImageNet），从 64.155 提升至 65.724（真实 3D 数据集）。
- **Gemini-2.5 胜率**达 95.0%（对比 Trellis 的 68.1%），**人类评分**从 3.4 提升至 4.4（1–5 量表）。

消融实验进一步证实：$\mathcal{L}_{\mathrm{adapt}}$ 和 $\mathcal{L}_{\mathrm{match}}$ 的联合使用是产生高真实感细节和稳定结构的关键——单独移除任一损失均导致质量明显下降，而用 L2 损失替代则会造成严重的纹理失真甚至崩塌。此外，Photo3D 在三种不同 3D 生成范式上均能一致提升真实感，且不损害几何质量，验证了其通用性。

## 背景与动机

### 3D 生成从几何走向真实感

近年来，3D 原生生成方法（3D-native generation）在几何重建和结构建模上取得了长足进步。以 **Trellis**（Xiang et al., CVPR 2025）为代表的耦合式扩散模型、以 **TexGaussian**（Xiong et al., CVPR 2025）为代表的单步纹理模型，以及 **Step1X-3D**（Li et al., arXiv 2025）等解耦式多视图纹理方法，已能生成结构完整、几何合理的 3D 资产。然而，这些方法普遍面临一个共同瓶颈：**生成物体的外观缺乏真实感，纹理细节粗糙、材质表现单薄**，与真实世界物体之间存在明显的视觉鸿沟。

### 根本瓶颈：高质量真实感 3D 数据的缺失

这一瓶颈的根源并非模型架构或训练策略的不足，而在于**缺乏多样化且具有丰富纹理细节的高质量真实世界 3D 资产数据集**。现有 3D 生成器主要依赖 Objaverse 等合成 3D 资产数据集进行训练，这些数据虽然规模庞大，但纹理保真度有限，难以提供足够丰富的真实感外观先验。直接使用像素级 L2 损失或对抗损失进行监督，又容易导致纹理失真甚至几何崩塌——因为像素级约束过于刚性，无法容忍合成图像与真实图像之间在细节层面的合理差异。

### 现有真实感增强路线的局限

为弥补这一缺口，已有工作尝试从不同角度注入真实感先验。**Real3D**（Jiang et al., ICML 2023）通过单视图监督引入真实感信息，但缺乏多视图一致性约束，容易产生视角间纹理不一致的问题。测试时优化（test-time optimization）方法虽然可以在推理阶段对生成结果进行细节增强，但计算开销巨大（单物体从约 10 秒激增至超过 4 分钟），且往往以牺牲整体质量为代价（MUSIQ 从 76.6 降至 71.5，见 Figure 8）。这些路线均未能从根本上解决训练阶段真实感先验缺失的问题。

### 本文动机：在生成过程中注入结构对齐的真实感细节

Photo3D 的核心动机在于：**将真实感增强从测试时的事后修补，前移至训练时的事前注入**，使 3D 生成器在生成过程中即具备产生照片级真实感外观的能力。这需要同时解决两个关键挑战：

1. **数据层面**：如何构建一个与 3D 几何结构对齐、细节丰富且具备多视图一致性的真实感数据集？
2. **监督层面**：如何设计一种放松的监督信号，既能注入真实感纹理细节，又不会因过度约束而损害原有的 3D 几何结构？

Photo3D 的解决方案是：利用 GPT-4o-Image 对 3D 渲染视图进行细节增强，构建 **Photo3D-MV** 数据集；并设计基于 CLIP 感知特征适应和 DINOv3 语义结构匹配的放松损失函数，在保持结构一致性的前提下，将真实感外观先验融入 3D 生成框架。该方法可适配耦合式、解耦式等多种 3D 生成范式，实现统一的真实感提升。

## 核心创新

Photo3D 的核心创新在于识别并突破了当前 3D 原生生成器在真实感外观上的根本瓶颈——高质量真实世界 3D 资产数据的匮乏。围绕这一瓶颈，该方法构建了一套从数据合成到监督范式再到训练策略的系统性方案，使其能够在不损害原有 3D 几何结构的前提下，为多种 3D 生成范式注入照片级真实感纹理细节。

### 1. 数据集创新：结构对齐的真实感多视图数据集 Photo3D-MV

现有 3D 生成器（如 **Trellis** (Xiang et al., CVPR 2025)、**3DTopia-XL** (Chen et al., arXiv 2024)、**Hunyuan3D 2.0** (Zhao et al., arXiv 2025)）通常依赖 Objaverse 等合成 3D 资产数据集进行训练，这些数据缺乏真实世界物体的丰富纹理细节和材质表现。Photo3D 构建了 **Photo3D-MV** 数据集，其关键设计在于“结构对齐”：利用 GPT-4o-Image 对 3D 渲染视图进行增强，生成与原始 3D 几何严格对齐、同时具备高真实感细节的多视图图像。数据集覆盖 10K 物体和 373 个类别，为真实感训练提供了多样化的先验（Figure 4）。

### 2. 监督范式创新：放松的真实感细节增强方案

传统 3D 纹理训练通常采用 L2 像素损失或对抗损失，但像素级监督在注入真实感细节时容易导致几何失真或纹理崩塌。Photo3D 提出了一种放松的监督方案，核心由两个互补的损失函数构成：

- **感知特征适应损失** $\mathcal{L}_{\mathrm{adapt}}$：对合成图像 $I_{\mathrm{syn}}$ 和 GT 图像 $I_{\mathrm{GT}}$ 进行随机裁剪 $\tau_c$，通过 CLIP 编码器 $\phi$ 提取特征后计算余弦相似度。该损失在语义嵌入空间而非像素空间中对齐，迫使生成图像在全局感知层面逼近真实细节，而不过度约束局部几何。

- **语义结构匹配损失** $\mathcal{L}_{\mathrm{match}}$：利用 DINOv3 提取的 patch 级特征，为合成图像的每个 token 寻找 GT 中最匹配的 token，最大化其相似度。该损失建立了细粒度的语义结构对应，确保注入的纹理细节与原有 3D 结构保持一致，避免纹理漂移。

总真实感损失为二者之和：$\mathcal{L}_{\mathrm{real}} = \mathcal{L}_{\mathrm{adapt}} + \mathcal{L}_{\mathrm{match}}$。消融实验证实，单独移除任一组件均导致质量显著下降：移除 $\mathcal{L}_{\mathrm{adapt}}$ 使纹理模糊、MANIQA 下降 27%；移除 $\mathcal{L}_{\mathrm{match}}$ 造成纹理错位和结构漂移；用 L2 损失替代则导致严重纹理失真甚至崩塌（Table 2, Figure 7）。

### 3. 范式适配创新：跨架构的训练策略

Photo3D 并非绑定于单一生成框架，而是针对三种主流 3D 生成范式分别设计了训练策略，将真实感先验融入各自的核心生成过程：

- **耦合式扩散生成器（Trellis）**：不再使用 GT 3D latents 进行重建，而是对加噪的 3D latent 进行去噪预测，解码为 3DGS 模型后渲染，施加 $\mathcal{L}_{\mathrm{real}}$ 监督，将真实感细节注入扩散空间。

- **单步 3D 原生纹理模型（TexGaussian）**：在纹理生成阶段直接施加 $\mathcal{L}_{\mathrm{real}}$，使前馈网络输出具备真实感外观的纹理。

- **扩散式多视图纹理模型（Step1X-3D）**：将 Photo3D-MV 的真实感多视图编码为 latent，通过扩散模型以渲染几何图像为条件恢复干净 latent，解码后施加 $\mathcal{L}_{\mathrm{real}}$ 监督。

实验表明，Photo3D 在这三种范式上均能一致提升真实感而不损害几何质量（Figure 6, Figure 12–14），验证了其作为通用真实感增强方案的范式无关性。

### 创新总结

Photo3D 的 changed slots 可归纳为三个维度：

| 维度 | 基线做法 | Photo3D 做法 |
|------|----------|-------------|
| 训练数据 | Objaverse 等合成 3D 资产 | Photo3D-MV：与 3D 几何对齐的 GPT-4o-Image 增强多视图 |
| 监督损失 | L2 像素损失 / 对抗损失 | $\mathcal{L}_{\mathrm{real}} = \mathcal{L}_{\mathrm{adapt}} + \mathcal{L}_{\mathrm{match}}$ |
| 训练范式 | 使用 GT latents 重建 | 去噪预测 → 解码渲染 → $\mathcal{L}_{\mathrm{real}}$ 监督 |

这一“数据-监督-训练”三位一体的创新链条，使得 Photo3D 无需修改生成器架构即可将真实感细节注入多种 3D 生成流程，同时保持结构稳定性。

## 整体框架

Photo3D 的核心目标是为现有的 3D 原生生成器注入照片级真实感外观，同时保持其固有的 3D 几何结构不受损害。这一目标的实现依赖于一个“数据构造—监督设计—范式适配”的三阶段整体框架。

### 数据构造：Photo3D-MV 数据集

真实感 3D 生成的根本瓶颈在于缺乏与几何结构对齐的高质量真实感多视图数据。Photo3D 首先构建了一个名为 **Photo3D-MV** 的细节增强多视图数据集，其构造流水线如下：

1.  **文本提示优化**：以 DiffusionDB 中的文本提示为起点，利用 **LLaMA-3-8B** 将其优化为以物体为中心、包含真实感属性（如材质、纹理、光照）的描述。
2.  **初始 3D 资产生成**：将优化后的文本提示输入 **Flux.1-Dev** 生成初始 2D 图像，再以该图像为条件，通过 **Trellis** 生成对应的 3D 资产。此时的 3D 资产具备合理的几何结构，但外观细节不足。
3.  **结构对齐的多视图真实感增强**：将 Trellis 生成 3D 资产的多视角渲染图输入商用图像生成器 **GPT-4o-Image**，利用其强大的图像编辑能力对渲染图进行细节增强，生成纹理丰富、光照自然的真实感图像。为保证增强后的图像与原始 3D 几何结构对齐，流水线引入了**色阶匹配**（tone matching）操作，将增强图像的色彩分布校准回原始渲染图的分布，从而抑制生成器可能引入的结构偏移。
4.  **数据组成**：最终，每个 3D 资产与其对应的增强多视图真实感图像、文本描述共同构成 Photo3D-MV 数据集。该数据集覆盖 10K 个物体、373 个类别，为后续训练提供了多样化的真实感先验。

### 监督设计：放松的真实感细节增强方案

在获得 Photo3D-MV 数据集后，核心问题转化为：如何利用这些与几何结构对齐的真实感图像来监督 3D 生成器的训练，使其学会生成逼真纹理，同时不破坏原有的 3D 结构。

Photo3D 的设计洞察是：**像素级的严格监督（如 L2 损失）会强制生成结果与 GT 图像逐像素对齐，而 GPT-4o-Image 增强的图像虽在结构上对齐，但在高频细节上不可避免地存在微小偏移，因此像素级监督极易导致纹理失真甚至几何崩塌**。为此，Photo3D 提出了一种放松的监督方案，包含两个互补的损失函数：

-   **感知特征适应损失 $\mathcal{L}_{\mathrm{adapt}}$**：对合成图像 $I_{\mathrm{syn}}$ 和 GT 图像 $I_{\mathrm{GT}}$ 进行多次随机裁剪 $\tau_c$，利用 CLIP 图像编码器 $\phi$ 提取裁剪区域的嵌入向量，并计算余弦相似度。该损失鼓励生成图像在语义感知空间中逼近 GT 的真实感特征，从而注入丰富的纹理细节，同时对局部像素偏移具有天然的鲁棒性。
    $$\mathcal{L}_{\mathrm{adapt}} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \Big( 1 - \langle \phi( \tau_c ( I_{\mathrm{syn}} ) ), \phi( \tau_c ( I_{\mathrm{GT}} ) ) \rangle \Big )$$

-   **语义结构匹配损失 $\mathcal{L}_{\mathrm{match}}$**：利用 DINOv3 作为特征提取器 $\psi$，分别提取合成图像和 GT 图像的 patch 级特征图 $F_p$ 与 $F_q$。对合成图像的每个 patch 特征 $f_p$，在 GT 特征图中寻找余弦相似度最高的匹配 patch $f_q$，并最大化这些匹配对的平均相似度。该损失在语义层级建立了细粒度的结构对应关系，确保生成纹理在语义上与 GT 保持结构一致性，防止纹理漂移或错位。
    $$\mathcal{L}_{\mathrm{match}} = 1 - \frac{1}{|P|} \sum_{p \in P} \max_{q \in Q} \langle f_p, f_q \rangle$$

最终的**真实感损失**为二者之和：
$$\mathcal{L}_{\mathrm{real}} = \mathcal{L}_{\mathrm{adapt}} + \mathcal{L}_{\mathrm{match}}$$

### 范式适配：面向三种 3D 生成范式的训练策略

Photo3D 并非一个独立的生成模型，而是一个可泛化的真实感增强方案。为覆盖主流的 3D 生成范式，作者针对三种代表性方法设计了专门的训练策略，将 $\mathcal{L}_{\mathrm{real}}$ 嵌入各自的训练流程：

-   **耦合式 3D 原生生成（Trellis）**：Trellis 是一个基于扩散的几何-纹理耦合生成器。Photo3D 在其扩散训练过程中，不再使用原始的 GT 3D latent 进行重建监督，而是对加噪的 3D latent 进行去噪预测，将预测结果解码为 3DGS 模型并渲染出多视图图像，最后对这些渲染图像施加 $\mathcal{L}_{\mathrm{real}}$ 监督。这使得真实感细节能够反向传播至扩散空间，从生成源头提升纹理质量。

-   **单步 3D 原生纹理生成（TexGaussian）**：TexGaussian 是一个前馈式纹理模型，输入 3D 几何和条件图像，直接输出带纹理的 3DGS。Photo3D 在 TexGaussian 的输出端直接施加 $\mathcal{L}_{\mathrm{real}}$，以微调的方式将真实感先验注入其纹理预测过程。

-   **扩散式多视图纹理生成（Step1X-3D）**：Step1X-3D 是一个几何-纹理解耦的扩散模型，其输入为 3D 几何渲染图和加噪的多视图 latent，输出为去噪后的纹理 latent。Photo3D 将预测的去噪 latent 解码为图像后，与 Photo3D-MV 中的 GT 图像计算 $\mathcal{L}_{\mathrm{real}}$，从而在纹理扩散过程中注入真实感。

通过这一“统一数据集 + 统一损失函数 + 范式特定适配”的框架，Photo3D 能够在保持各类 3D 生成器原有几何质量的前提下，一致性地提升其纹理的真实感和细节丰富度。

### 补充图表

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Photo3D. We first construct Photo3D-MV, a realistic, detail-enhanced multi-view dataset paired with 3D geometry, and propose associated schemes to learn realistic 3D appearance details. Paradigm-specific training strategies are designed for geometry–texture coupled and decoupled paradigms: (a) diffusion-based 3D-native generator (e.g., Trellis [69]); (b) single feed-forward 3D-native texturing model (e.g., TexGaussian [70]); and (c) diffusion-based multi-view texturing model (e.g., Step1X-3D [40])*

## 核心模块与公式推导

Photo3D 的核心由两个紧密耦合的模块构成：**结构对齐多视图合成流水线**（构建 Photo3D-MV 数据集）和**真实感细节增强方案**（设计放松的监督信号）。前者提供与 3D 几何对齐的高质量真实感多视图图像，后者则通过感知特征适应与语义结构匹配的联合优化，将这些真实感细节注入 3D 生成器的纹理空间，同时保持原有几何结构的稳定性。

### 结构对齐多视图合成流水线

该流水线的目标是生成与 3D 资产几何严格对齐、且具有丰富真实感细节的多视图图像。其构建过程分为四步（见 Figure 3）：

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/003_Figure_3.jpg]]
*Figure 3: The structure-aligned realistic multi-view synthesis pipeline for Photo3D-MV dataset. We first process text prompts from DiffusionDB [68] to obtain object-centric descriptions with realistic attributes. We then use Flux.1-Dev [35] to generate images, serving as inputs for 3D generation with Trellis [69]. Finally, we employ GPT-4o-Image [31] to refine the multi-view 3D renderings into structure-aligned, photorealistic images. These realistic multi-views, together with text descriptions and the generated 3D assets, constitute Photo3D-MV*

1. **文本提示优化**：从 DiffusionDB 中采样文本提示，利用 LLaMA-3-8B 将其转化为以物体为中心、包含真实感属性（如材质、光照、纹理）的描述。
2. **初始图像生成**：使用 Flux.1-Dev 根据优化后的提示生成物体图像。
3. **3D 资产构建**：将生成的图像输入 Trellis（Xiang et al., CVPR 2025），生成对应的 3D 原生资产。
4. **多视图真实感增强**：对 3D 资产的多视角渲染图，利用 GPT-4o-Image 进行细节增强，并通过色阶匹配对齐渲染图与增强图的色彩分布，最终得到与 3D 几何对齐的真实感多视图图像。

该流水线产出的 Photo3D-MV 数据集包含约 10K 物体，覆盖 373 个类别（Figure 4），为后续的真实感训练提供了关键的监督信号。

### 真实感细节增强方案

Photo3D 的核心创新在于设计了一套**放松的监督损失函数**，避免传统像素级损失（如 L2）导致的纹理崩塌和几何失真。该方案由两个互补的损失项组成，其计算方式如 Figure 5 所示。

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/005_Figure_5.jpg]]
*Figure 5: Computation of*

#### 感知特征适应损失 $\mathcal{L}_{\mathrm{adapt}}$

该损失旨在全局感知层面将合成图像 $I_{\mathrm{syn}}$ 拉向真实感 GT 图像 $I_{\mathrm{GT}}$，同时通过随机裁剪增强局部细节的对齐鲁棒性：

$$
\mathcal{L}_{\mathrm{adapt}} = \frac{1}{|\mathcal{C}|} \sum_{c \in \mathcal{C}} \Big( 1 - \langle \phi( \tau_c ( I_{\mathrm{syn}} ) ), \phi( \tau_c ( I_{\mathrm{GT}} ) ) \rangle \Big )
$$

其中：
- $\mathcal{C}$ 为随机裁剪操作集合，$\tau_c$ 表示从图像中随机裁剪一个区域；
- $\phi$ 为 CLIP 图像编码器，将裁剪区域映射到归一化的嵌入空间；
- $\langle \cdot, \cdot \rangle$ 表示余弦相似度。

通过在多组随机裁剪上最大化嵌入相似度，$\mathcal{L}_{\mathrm{adapt}}$ 强制生成图像在多个局部尺度上匹配 GT 的纹理丰富度和感知质量，从而注入真实感细节。

#### 语义结构匹配损失 $\mathcal{L}_{\mathrm{match}}$

$\mathcal{L}_{\mathrm{adapt}}$ 仅约束全局感知分布，无法保证局部语义结构的对应关系。为此，Photo3D 引入基于 DINOv3 的语义结构匹配损失。首先，使用冻结的 DINOv3 模型 $\psi$ 分别提取合成图像和 GT 图像的 patch 级特征图：

$$
F_p = \psi( I_{\mathrm{syn}} ), \quad F_q = \psi( I_{\mathrm{GT}} )
$$

然后，对合成图像的每个 patch 特征 $f_p \in P$，在 GT 图像的 patch 特征集 $Q$ 中寻找最相似的匹配，并最大化其相似度：

$$
\mathcal{L}_{\mathrm{match}} = 1 - \frac{1}{|P|} \sum_{p \in P} \max_{q \in Q} \langle f_p, f_q \rangle
$$

该损失通过建立跨图像的 token 级语义对应，确保增强后的纹理在局部结构与原始 3D 几何保持一致，避免纹理漂移或错位。

#### 总真实感损失

最终的真实感监督信号为上述两项的简单求和：

$$
\mathcal{L}_{\mathrm{real}} = \mathcal{L}_{\mathrm{adapt}} + \mathcal{L}_{\mathrm{match}}
$$

消融实验（Table 2）表明，二者缺一不可：单独移除 $\mathcal{L}_{\mathrm{adapt}}$ 导致纹理模糊、MANIQA 下降 27%；单独移除 $\mathcal{L}_{\mathrm{match}}$ 则造成纹理错位和结构漂移；若替换为 L2 损失，则引发严重的纹理失真甚至崩塌。这验证了放松监督在注入真实感细节与维持 3D 结构稳定性之间的关键平衡作用。

### 范式特定训练策略

为将 $\mathcal{L}_{\mathrm{real}}$ 适配到不同的 3D 生成范式，Photo3D 设计了三种训练目标：

**耦合式 3D 原生生成（以 Trellis 为例）**：Trellis 原本使用 GT 3D latent 进行重建训练。Photo3D 改为对加噪的 3D latent $\boldsymbol{x}_t$ 进行去噪预测 $\hat{\boldsymbol{x}}_0$，解码为 3DGS 模型后渲染多视图图像，再施加 $\mathcal{L}_{\mathrm{real}}$ 监督：

$$
\min_{\theta, \phi} \mathbb{E}_{\boldsymbol{x}_0, t, I_{\mathrm{cond}}} \left[ \mathcal{L}_{\mathrm{real}} \left( D_{\phi}(\hat{\boldsymbol{x}}_0), I_{\mathrm{GT}} \right) \right]
$$

其中 $D_{\phi}$ 为 3DGS 解码器，$I_{\mathrm{cond}}$ 为条件图像。该设计将真实感细节直接注入扩散空间，使生成过程内在地产生照片级纹理。

**单步 3D 原生纹理（TexGaussian）与扩散式多视图纹理（Step1X-3D）**：对于纹理解耦范式，Photo3D 分别在其前馈纹理预测或多视图扩散去噪的输出端施加 $\mathcal{L}_{\mathrm{real}}$，使真实感先验融入各自的纹理生成流程，而不干扰几何生成阶段。具体训练目标见原文公式 (6)–(7)。

## 实验与分析

### 核心定量结果：真实感指标的全面提升

Photo3D 的核心主张——通过结构对齐的细节增强将 3D 原生生成器推向照片级真实感——在 Table 1 中得到了系统验证。该表在两类互补的测试集上进行了评估：**ImageNet**（从 ImageNet 中筛选美学评分最高的 1000 张自然图像）和 **Real 3D Datasets**（由 GSO、Omni3D、DTC 组成的真实扫描 3D 物体集合）。前者测试模型对自然图像分布的拟合能力，后者直接评估生成 3D 资产在真实世界物体标准下的外观质量。

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/006_Table_1.jpg]]
*Table 1: Comparison on the ImageNet and Real 3D datasets. Quantitative metrics evaluate input fidelity (CLIP, KID), detail realism (MANIQA, MUSIQ), and overall aesthetic quality (NIMA, Aesthetic Score). Qualitative metrics include the Gemini-2.5-based winning rate and human-rated realism scores (1–5 scale, higher indicates greater realism) on 20 objects for each method*

以 Trellis 为骨干的 **Photo3D (Trellis)** 在所有真实感指标上均显著超越原始 Trellis 及其他基线：

| 测试集 | 指标 | Trellis (基线) | Photo3D (Trellis) | 提升幅度 |
|--------|------|---------------|-------------------|---------|
| ImageNet | MANIQA↑ | 0.438 | **0.470** | +0.032 |
| ImageNet | MUSIQ↑ | 69.108 | **72.385** | +3.277 |
| Real 3D | MANIQA↑ | 0.427 | **0.459** | +0.032 |
| Real 3D | MUSIQ↑ | 64.155 | **65.724** | +1.569 |

MANIQA 和 MUSIQ 是专门评估图像细节真实感和感知质量的指标，Photo3D 在两个数据集上的稳定提升表明其增强的纹理细节并非过拟合于某一特定域，而是具有跨域泛化能力。

更值得注意的是定性评估中的压倒性优势。在 **Gemini‑2.5 胜率**（Gemini‑2.5 作为评判者，比较 Photo3D 与各基线的生成质量）上，Photo3D (Trellis) 在 ImageNet 上达到 **95.0%**，远超 Trellis 的 68.1%。**人类评分**（1–5 分，20 个物体）同样从 Trellis 的 3.4 跃升至 **4.4**。这两个指标直接反映了人类和强视觉语言模型对真实感的一致认可，构成了 Photo3D 有效性的最强证据。

在输入保真度方面，Photo3D (Trellis) 的 CLIP 得分在 Real 3D 数据集上达到 **0.864**，在所有方法中最高，说明增强后的纹理并未偏离文本条件或原始语义。KID（Kernel Inception Distance）指标同样显示 Photo3D 生成图像的分布更接近真实图像分布。

### 消融实验：放松监督是真实感与结构平衡的关键

Table 2 的消融实验揭示了 Photo3D 损失函数设计的因果机制。以 Photo3D (Trellis) 为基准，系统移除了各损失分量并观察性能变化：

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/007_Table_2.jpg]]
*Table 2: Ablation study on different supervision types. We analyze the effect of each component of our method and other supervision approaches on Photo3D (Trellis)*

1. **移除 L_adapt（仅保留 L_match）**：MANIQA 下降约 **27%**，生成纹理明显趋于模糊。L_adapt 通过 CLIP 嵌入空间中的随机裁剪余弦相似度，迫使生成图像在语义特征层面逼近 GT 的丰富细节。没有这一信号，模型缺乏向高真实感纹理靠近的驱动力。

2. **移除 L_match（仅保留 L_adapt）**：CLIP 和 NIMA 得分下降，视觉上表现为纹理错位和结构漂移。L_match 在 DINOv3 的 patch 特征空间中建立合成图像与 GT 之间的局部语义对应，其作用是锚定纹理细节与底层 3D 几何结构的空间关系。失去这一约束后，L_adapt 注入的细节可能附着在错误的位置，破坏 3D 一致性。

3. **替换为 L2 像素损失**：这是最具揭示性的对照实验。直接用像素级 L2 损失监督渲染图像与 GT 之间的差异，导致**严重的纹理失真甚至训练崩塌**。这验证了论文的核心设计选择：像素级监督过于刚性，会迫使生成器复制 GT 图像中与 3D 几何不完全对齐的像素，从而扭曲底层 3D 结构。相比之下，L_adapt + L_match 的放松监督在特征空间和语义空间操作，允许一定程度的局部变化，既注入真实感细节，又保持几何完整性。

Figure 7 的消融渲染对比直观展示了这些差异：完整模型生成的 3D 资产具有清晰的纹理细节和正确的结构对应，而移除 L_adapt 的版本表面模糊，移除 L_match 的版本出现纹理错位，L2 损失版本则呈现严重的伪影和几何崩塌。

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/009_Figure_7.jpg]]
*Figure 7: Ablation results on rendered images of generated 3D models. Highlighted regions mark areas with noticeable detail and color variations for comparison*

### 跨范式泛化：真实感先验的通用性

Photo3D 的核心贡献之一是证明其真实感增强方案**不依赖于特定的 3D 生成架构**。实验覆盖了三种代表性范式：

- **耦合式扩散生成器**：Trellis（Xiang et al., CVPR 2025），在 3D latent 空间中联合建模几何与纹理。
- **单步 3D 原生纹理模型**：TexGaussian（Xiong et al., CVPR 2025），以前馈方式为给定几何生成纹理。
- **扩散式多视图纹理模型**：Step1X‑3D（Li et al., arXiv 2025），通过多视图扩散为几何表面生成纹理。

在全部三种范式上，Photo3D 均实现了真实感的显著提升（Figure 6, 12–14）。定量结果（Table 1）显示，Photo3D (TexGaussian) 和 Photo3D (Step1X‑3D) 同样在 MANIQA、MUSIQ 和 Gemini 胜率上超越各自基线。这一跨范式的一致性验证了 Photo3D 的因果旋钮——Photo3D‑MV 数据集提供的真实感先验和放松监督方案——是范式无关的通用机制，而非针对特定架构的工程技巧。

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/008_Figure_6.jpg]]
*Figure 6: Visual comparison of generated 3D assets between existing methods and our Photo3D models built upon different 3D generation paradigms. For TexGaussian and Photo3D (TexGaussian), we use the generated captions of the input images as text conditions*

值得注意的是，在几何-纹理解耦范式（TexGaussian、Step1X‑3D）中，Photo3D 仅增强纹理生成阶段，不修改几何生成模块。这意味着纹理质量的提升是在**不损害几何质量**的前提下实现的——这是一个关键约束，因为解耦方法中纹理阶段无法修正上游几何缺陷（见后文失败模式分析）。

### 失败模式与边界条件

实验和消融分析同时揭示了 Photo3D 的若干边界条件和失败模式：

**1. 视角覆盖不全导致的模糊区域（Figure 9a）**  
当输入图像的视角覆盖不完整时，Photo3D‑MV 数据集中对应视角的增强图像可能缺乏足够的几何约束，导致生成 3D 资产的某些表面区域出现模糊纹理。这是数据驱动方法的固有局限：模型只能从训练分布中学习，无法凭空补全未观测视角的细节。

**2. 多视图不一致引发的结构畸变（Figure 9b）**  
GPT‑4o‑Image 在独立增强各视图时可能引入轻微的跨视图不一致性——例如同一物体在不同视角下呈现略微不同的纹理模式或光照。当这些不一致信号被 L_adapt 和 L_match 吸收并反向传播到 3D 表示时，可能造成局部几何结构的扭曲。Figure 9b 展示了这类失败案例：不一致的细节跨视图累积，最终导致 3D 结构出现可察觉的畸变。

**3. 几何-纹理解耦范式的级联局限**  
在 TexGaussian 和 Step1X‑3D 的解耦设置中，Photo3D 仅优化纹理阶段。如果上游几何生成器产生了缺陷（如不对称、缺失部件），纹理增强无法弥补这些几何错误。这是一个架构性限制，而非 Photo3D 方法本身的失败，但限制了端到端质量的提升上限。

**4. 测试时优化 vs. 训练时优化的权衡（Figure 8）**  
Figure 8 对比了测试时优化基线（在推理时对每个物体单独优化纹理）与 Photo3D 的训练时优化策略。测试时优化可能针对单个物体达到更极致的真实感，但计算成本高昂且无法泛化。Photo3D 的训练时优化在保持推理效率的同时实现了泛化能力，但在个别物体的极致细节上可能略逊于逐物体优化方案。

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/010_Figure_8.jpg]]
*Figure 8: Comparison between the test-time optimization baseline and Photo3D (training-time optimization)*

**5. 2D 生成器的依赖性（Figure 10）**  
Figure 10 对比了不同 2D 生成器增强的多视图效果。GPT‑4o‑Image 在细节丰富度和结构保持方面显著优于其他生成器，这意味着 Photo3D 的真实感上限高度依赖于底层 2D 增强模型的能力。使用较弱的 2D 生成器会导致增强图像质量下降，进而影响最终 3D 资产的真实感。

### 几何校正的意外收益

一个值得注意的发现是 Photo3D (Trellis) 展现出的**几何校正能力**（Figure 11）。在耦合式扩散训练中，L_real 的放松监督不仅增强了纹理细节，还通过反向传播间接修正了原始 Trellis 生成的部分几何缺陷（如不对称、比例失调）。这一现象的可能机制是：Photo3D‑MV 中与几何对齐的高质量多视图图像为扩散模型提供了更强的几何-纹理联合先验，使得去噪过程倾向于生成几何更合理的 3D latent。这一发现暗示真实感增强与几何质量提升可能并非独立目标，而是可以通过联合优化相互促进。

### 补充图表

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/014_Figure_12.jpg]]
*Figure 12: Comparison of 3D generation results between TexGaussian [70] and Photo3D trained on the TexGaussian’s 3D-native texturing model. The results demonstrate the realistic appearance of geometry-texture decoupled 3D-native generation achieved by Photo3D*

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/015_Figure_13.jpg]]
*Figure 13: Comparison of 3D generation results between Step1X-3D [40] and Photo3D trained on the Step1X-3D’s multi-view texturing model. The results demonstrate the realistic appearance of geometry-texture decoupled 3D-native generation achieved by Photo3D*

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/004_Figure_4.jpg]]
*Figure 4: Diverse distribution of top categories in Photo3D-MV*

![[assets/figures/papers/paper_list_l2565_https_arxiv_org_abs_2512_08535/figures/011_Figure_9.jpg]]
*Figure 9: (a) Incomplete view coverage causes blurred regions. (b) Inconsistent details across views lead to distorted 3D structures*

## 方法谱系与知识库定位

### 核心问题定位：3D 原生生成器的真实感瓶颈

当前 3D 原生生成器（3D-native generators）能够产出几何结构合理的物体，但在外观真实感上存在系统性短板。其根本瓶颈不在于生成架构本身，而在于训练数据的质量鸿沟：现有方法普遍依赖 Objaverse 等合成 3D 资产数据集，这些数据缺乏真实世界中丰富、多样的纹理细节。Photo3D 的核心洞察在于，与其从零设计更复杂的生成器，不如从数据端为 3D 生成注入真实感先验——通过构建与 3D 几何对齐、细节增强的多视图数据集，并设计放松的监督信号，使 3D 生成器学会"看到"真实世界的纹理复杂度。

### 在 3D 生成方法谱系中的位置

Photo3D 并非一个独立的 3D 生成器，而是一种**可插拔的真实感增强框架**，适用于当前主流的三大 3D 生成范式：

1. **几何-纹理耦合扩散模型**：以 **Trellis**（Xiang et al., CVPR 2025）为代表，在统一的扩散空间中同时生成几何与纹理。Photo3D 在 Trellis 的去噪预测阶段插入 $\mathcal{L}_{\text{real}}$ 监督，使扩散模型学会从噪声中恢复具有真实感细节的 3D latent，而非仅仅重建 Objaverse 的合成外观。

2. **单步前馈 3D 纹理模型**：以 **TexGaussian**（Xiong et al., CVPR 2025）为代表，在给定几何的前提下一次性预测纹理。Photo3D 通过 $\mathcal{L}_{\text{real}}$ 微调纹理解码器，使其输出从"合成感"向"照片级"迁移。

3. **扩散式多视图纹理模型**：以 **Step1X-3D**（Li et al., arXiv 2025）为代表，通过扩散模型为多视图生成纹理。Photo3D 在此范式下将真实感损失施加于去噪后的解码图像，使纹理生成过程融入真实世界的外观分布。

与测试时优化方法（如 **Real3D**，Jiang et al., ICML 2023 的单视图监督方案）不同，Photo3D 选择在训练阶段注入真实感先验。这种设计带来了两个关键优势：一是避免了测试时逐样本优化的高昂计算开销；二是训练时优化的模型能学到泛化的真实感表示，而非对单一样本的过拟合。Figure 8 的对比证实，训练时优化在保持几何一致性的同时，实现了更稳定的真实感提升。

### 监督信号的范式创新：从像素约束到语义放松

Photo3D 的方法论贡献在于重新定义了"真实感监督"的形式。传统方法使用 L2 像素损失或对抗损失直接约束渲染图像与 GT 的逐像素差异，这在 3D 场景中极其危险——合成渲染与真实 GT 之间存在不可避免的几何偏差，强制像素对齐会导致纹理失真甚至几何崩塌（Table 2 中 w/ L2 loss 的实验证实了这一点）。

Photo3D 的解决方案是将监督信号从像素空间**放松**到语义空间：

- **$\mathcal{L}_{\text{adapt}}$** 在 CLIP 嵌入空间中通过随机裁剪计算余弦相似度，迫使生成图像在全局感知特征上逼近 GT，从而注入纹理丰富度；
- **$\mathcal{L}_{\text{match}}$** 在 DINOv3 的 patch 级语义空间中建立局部对应，确保注入细节的同时不破坏原有的 3D 结构。

这种"放松监督"的设计哲学与近期图像翻译和风格迁移领域中的感知损失一脉相承，但 Photo3D 将其首次系统性地引入 3D 原生生成器的训练流程，并证明了联合使用 CLIP 感知损失和 DINO 语义匹配损失是产生高真实感且结构稳定结果的关键（Table 2 中单独移除任一损失均导致质量显著下降）。

### 适用边界与已知局限

**数据依赖性**：Photo3D 的真实感增强能力高度依赖 Photo3D-MV 数据集的质量和覆盖范围。该数据集目前包含约 10K 物体、373 个类别，虽然类别分布多样（Figure 4），但可能难以泛化到训练集外的罕见物体类别或具有复杂拓扑结构的对象。对于这些长尾场景，Photo3D 的增强效果可能退化甚至引入不合理的纹理。

**对闭源生成器的依赖**：Photo3D-MV 的构建流水线依赖 GPT-4o-Image 进行多视图真实感增强。该模型的闭源性质带来了两个问题：一是可复现性受限，不同时间调用同一模型可能产生不同的增强结果；二是潜在的政策限制可能影响数据集的合法使用和分发。虽然论文使用 Flux.1-Dev 作为初始图像生成器，但关键的细节增强步骤仍绑定于闭源 API。

**几何-纹理解耦范式的先天限制**：在 TexGaussian 和 Step1X-3D 等解耦范式中，Photo3D 仅作用于纹理生成阶段，无法修正前一阶段几何生成中的缺陷。如果几何生成器产出了畸变或不完整的结构，Photo3D 只能在其上"绘制"真实感纹理，而无法纠正底层的几何错误。

**计算资源门槛**：所有受微调模型均在 8 块 NVIDIA H20 GPU 上训练，对于资源有限的研究者而言，完整复现实验的门槛较高。

### 开放问题与潜在延伸方向

1. **开源替代方案的可复现性验证**：能否用 FLUX.2-dev 等开源 2D 生成器完全替代 GPT-4o-Image 完成多视图增强，在保持真实感水平的同时实现完全可复现？Figure 10 展示了不同 2D 生成器的增强效果对比，但尚未给出系统性的定量评估。

2. **动态与非刚性场景的扩展**：Photo3D 当前聚焦于静态刚体物体的真实感生成，其放松监督机制能否迁移至动态场景、可变形物体或复杂背景下的对象，是一个值得探索的方向。

3. **多视图不一致性的形式化建模**：解耦视角增强不可避免地引入轻微的多视图不一致（Figure 9 展示了不一致导致的 3D 结构问题）。如何将这种不一致性形式化地建模为一种数据增强手段，而非简单地视为需要消除的噪声，可能为提升模型鲁棒性提供新思路。

4. **与更大规模 3D 基础模型的整合**：**3DTopia-XL**（Chen et al., arXiv 2024）和 **Hunyuan3D 2.0**（Zhao et al., arXiv 2025）代表了向大规模 3D 基础模型发展的趋势。Photo3D 的放松监督方案是否能无缝集成到这些更大规模的训练流程中，以及在大规模数据下是否仍能保持结构对齐的优势，尚待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Photo3D_Advancing_Photorealistic_3D_Generation_through_Structure_Aligned_Detail_Enhancement.pdf]]