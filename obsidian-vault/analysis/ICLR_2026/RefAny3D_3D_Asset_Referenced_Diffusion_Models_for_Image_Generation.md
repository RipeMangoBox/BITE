---
title: "RefAny3D: 3D Asset-Referenced Diffusion Models for Image Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RefAny3D_3D_Asset_Referenced_Diffusion_Models_for_Image_Generation_af40724eea65.pdf
project_link: https://judgementh.github.io/RefAny3D/
code_link: https://github.com/JudgementH/RefAny3D
aliases:
- RefAny3D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入点图作为3D几何代理，并通过空间对齐的双分支生成同时产生RGB与点图输出，配合域解耦机制避免纹理渗漏。
primary_logic: 联合建模RGB图像与点图的条件分布，点图提供几何一致性锚定；域特定LoRA与文本无关注意力实现RGB域与几何域的解耦，在保留细节的同时确保3D一致性。
claims:
- GPT-eval Overall得分7.123，显著超越所有基线。
- 去除共享位置编码、文本无关注意力或域特定LoRA均导致几何或纹理不一致。
- 点图与RGB共享位置编码使网络学习到像素级对应关系。
- GPT-eval (Overall) 上 GPT-eval Overall = 7.123
---

# RefAny3D: 3D Asset-Referenced Diffusion Models for Image Generation

> [!tip] 核心洞察
> 联合建模RGB图像与点图的条件分布，点图提供几何一致性锚定；域特定LoRA与文本无关注意力实现RGB域与几何域的解耦，在保留细节的同时确保3D一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | RefAny3D：一种基于3D资产的图像扩散模型 |
| 英文题名 | RefAny3D: 3D Asset-Referenced Diffusion Models for Image Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fUO37EVR7j) · [Project](https://judgementh.github.io/RefAny3D/) · [Code](https://github.com/JudgementH/RefAny3D) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RefAny3D |
| Dataset | GPT-eval, Vision Foundation Models, GIM, User Study |

> [!tip] 效果简介
> - GPT-eval (Overall) 上，GPT-eval Overall 7.123 vs 次优基线值未公开列出，但本文方法显著更优 (显著提升)。
> - Vision Foundation Models 上，CLIP Image/Avg. 0.873 vs 次优基线值未公开列出 (提升)；DINO Avg. 0.720 vs 次优基线值未公开列出 (提升)。
> - GIM 上，GIM Count 3901.316 vs 次优基线值未公开列出 (提升)。

## 概述

**核心问题**：现有的基于参考的图像生成方法（如 **IP-Adapter** (Ye et al., 2023)、**DreamBooth** (Ruiz et al., 2023)、**DSD** (Cai et al., 2025)）仅能利用单张或多张 2D RGB 图像作为条件，无法显式利用 3D 资产的几何结构与纹理先验，导致生成结果与参照物在几何和纹理上缺乏一致性。

**核心思路**：RefAny3D 将 3D 资产引导的图像生成形式化为 RGB 图像与点图（point map，即归一化物体坐标的栅格化表示）的联合分布建模 $p ( x _ { I } , x _ { P } | y , c )$。通过点图作为 3D 几何代理，为生成过程提供显式的空间一致性锚定。

**方法定位**：RefAny3D 是一种跨域扩散模型，核心架构包含三个关键设计：
- **空间对齐双分支生成**：同时输出 RGB 图像与点图，两分支共享位置编码并通过位移 $( i - w , j )$ 避免条件 token 与目标 token 空间重叠，使网络学习到像素级对应关系。
- **域特定 LoRA**：引入 Reference-LoRA（通用外观）与 Domain-LoRA（几何特征）的双 LoRA 结构，由域切换器控制，解耦 RGB 域与几何域的知识学习，避免纹理渗漏。
- **文本无关注意力**：在点图分支中屏蔽文本 token，防止背景语义信息泄漏到几何生成中。

**主要结果**：在 GPT-eval 综合评估中，RefAny3D 取得 7.123 的 Overall 得分，显著超越所有基线方法；CLIP Image 平均相似度达 0.873，DINO 平均相似度达 0.720。用户调研中，3D 一致性（Faithful）、身份保持（ID）和美学质量（Aesthetic）均取得最优，综合排名（Rank）为 1.579。消融实验证实，共享位置编码、文本无关注意力和域特定 LoRA 三个组件对几何一致性和纹理保真度均起决定性作用——移除任一组件的会导致几何偏差或伪影。

**局限性**：方法主要面向刚性物体，未建模非刚性物理交互（如变形）；训练需 8 张 H800 GPU 约 8 天；数据集依赖自动化姿态估计与 3D 重建管线，可能引入纹理或几何误差。

## 背景与动机

**问题背景** 以3D资产为参考的图像生成在游戏开发、虚拟现实、电子商务等场景中具有重要应用价值。给定一个3D模型，用户期望生成与参考资产在几何结构和纹理外观上高度一致、且能响应文本提示语义的高质量2D图像。现有方法主要分为两类：基于文本反转的个性化生成（如**Textual Inversion** (Gal et al., 2022)、**DreamBooth** (Ruiz et al., 2023)）和基于图像提示的适配方法（如**IP-Adapter** (Ye et al., 2023)、**DSD** (Cai et al., 2025)、**OminiControl** (Tan et al., 2025)）。这些方法的共同局限在于：**仅能利用单张或少量2D RGB图像作为参考条件，无法显式利用3D资产所蕴含的完整几何结构与纹理先验**。

**现有方法缺口** 2D参考图像仅提供特定视角下的外观信息，缺乏对物体三维形状、遮挡关系、多视角一致性的显式建模。因此，基于2D参考的生成方法在面对视角变化、复杂几何或精细纹理时，**生成结果与3D参照物在几何和纹理上缺乏一致性**——这是当前技术路线的核心瓶颈。此外，现有方法未涉及RGB外观与几何坐标之间的像素级对应关系建模，难以保证生成图像中物体结构与参考资产的对齐。

**本文动机** 针对上述缺口，RefAny3D提出了一种**3D资产引用的扩散生成框架**。其核心思想是：将3D资产表示为多视角RGB图像与点图（point map，即归一化物体坐标）的配对数据，通过**联合建模RGB外观与点图的联合条件分布** $p(x_I, x_P \mid y, c)$，在生成过程中同时产生目标RGB图像及其对应的点图。点图作为3D几何代理，为生成过程提供显式的几何一致性锚定，从而从根本上解决2D参考方法中缺失的几何约束问题。

## 核心创新

RefAny3D 的核心创新在于将图像生成的条件从单张 2D 参考图像拓展到完整的 3D 资产，并通过一套精心设计的**双分支生成架构**与**域解耦机制**，在保留参照物外观身份的同时，强制施加几何一致性约束。以下从五个关键改造槽位（changed slots）展开分析。

### 1. 条件格式：从 2D 图像到多视角 RGB-点图对

现有基于参考的图像生成方法（如 **IP-Adapter** (Ye et al., 2023)、**DSD** (Cai et al., 2025)）仅接受单张或少量 2D RGB 图像作为条件输入，缺乏对参照物三维结构的显式感知。RefAny3D 将条件格式根本性地改造为**多视角 RGB 图像与对应点图（point maps）的配对**。点图本质上是物体在规范化空间中的三维坐标栅格化表示，充当 3D 几何代理。这一改造使得扩散模型在生成过程中能够直接访问参照物的几何先验，而非仅依赖 2D 外观特征进行隐式推断。

### 2. 生成分支：从单 RGB 分支到空间对齐的双分支

传统方法仅包含单一的 RGB 生成分支。RefAny3D 提出**空间对齐的双分支生成架构**，同时输出目标视角的 RGB 图像和对应的点图。两条分支共享扩散变压器骨干网络，但在输出端分别负责外观生成与几何生成。这种设计的关键在于：点图分支为 RGB 分支提供显式的像素级几何锚定，使得生成结果的纹理与参照物表面形成严格对应，从机制层面解决了单分支方法中常见的几何漂移问题。

### 3. 位置编码：从独立编码到跨域共享位移编码

在标准扩散变压器中，各 token 的位置编码相互独立。RefAny3D 引入**共享位置编码（Shared Positional Embedding）** 机制，使 RGB 分支和点图分支中位于相同空间位置的 token 获得一致的位置先验。同时，为防止条件 token 与目标 token 在空间上重叠，条件 token 的位置编码被统一位移为 $(i - w, j)$，其中 $w$ 为目标潜在图像的宽度。这一看似简单的位移操作，是网络学习像素级 RGB-点图对应关系的必要条件——消融实验表明，移除共享位置编码后，网络缺乏位置先验，无法准确建立跨域对应，导致明显的几何偏差（见 Figure 7b）。

### 4. 域知识学习：从共享参数到双 LoRA 域解耦

基线方法通常使用共享模型参数处理所有域的信息。RefAny3D 设计了**域特定 LoRA（Domain-specific LoRA）** 结构，包含两组低秩适配器：**Reference-LoRA** 负责学习参照物的一般外观特征，**Domain-LoRA** 专门学习点图的几何特征。通过域切换器（domain switcher）根据当前处理的域动态激活对应的 LoRA 模块，实现了外观学习与几何学习的参数级解耦。消融实验证实，若使用单一 LoRA 同时处理两个域，模型无法高质量地同时生成 RGB 和点图，整体生成质量显著下降（见 Figure 7d）。

### 5. 文本注意力：从标准注意力到文本无关注意力

在标准的多头注意力机制中，所有 token（包括文本 token）相互可见。RefAny3D 在点图分支中引入**文本无关注意力掩码（Text-agnostic Attention Mask）**，显式阻断文本 token 对点图 token 的注意力通路。这一设计的动机在于：点图分支仅应关注几何信息，文本中携带的背景语义（如场景描述）若渗漏到几何生成中，会导致点图背景区域与 RGB 分支产生错误对齐，引发伪影。消融实验表明，移除该掩码后，点图分支受文本语义干扰，生成质量明显下降（见 Figure 7c）。

### 创新机制的内在关联

上述五个改造并非孤立存在，而是围绕一个统一的生成目标——建模条件联合分布 $p(x_I, x_P \mid y, c)$——形成因果闭环。共享位置编码建立了 RGB 与点图之间的空间纽带；双分支架构将联合分布分解为外观和几何两个可协同优化的子任务；域特定 LoRA 和文本无关注意力则分别从参数空间和注意力空间阻断跨域信息污染，确保解耦的纯粹性。三者共同作用，使得模型能够在“保留纹理细节”与“维持 3D 一致性”这两个通常相互制约的目标之间取得平衡。

### 与基线的本质差异

相较于 **DreamBooth** (Ruiz et al., 2023) 或 **Textual Inversion** (Gal et al., 2022) 等通过微调或嵌入优化来记忆特定对象外观的方法，RefAny3D 不依赖对参照物的“过拟合式”记忆，而是通过点图这一几何代理实现可泛化的 3D 一致性约束。相较于 **OminiControl** (Tan et al., 2025) 等通用控制方法，RefAny3D 的域解耦设计专门针对 RGB-几何联合生成场景，避免了通用控制中常见的纹理渗漏问题。

## 整体框架

RefAny3D 提出了一种基于 3D 资产条件的图像生成框架，其核心思想是将生成过程形式化为对 RGB 外观与点图（point map）的联合分布建模。如 Figure 2 所示，给定一个 3D 参照资产，系统首先从多个视角渲染 RGB 图像及对应的点图作为条件信号，随后通过一个空间对齐的双分支扩散模型同时生成目标视角的 RGB 图像及其点图。点图在此充当 3D 几何代理，为 RGB 生成提供像素级的几何一致性锚定。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RefAny3D. Given a 3D asset, we render multi-view inputs as conditioning signals for the diffusion model and simultaneously generate the point map of the target RGB image. To ensure pixel-level consistency across different viewpoints, we adopt a shared positional encoding strategy. Moreover, to disentangle the RGB domain from the point map domain, we incorporate Domain-specific LoRA and Text-agnostic Attention. Benefiting from this 3D-aware disentanglement design, our method is able to generate high-quality images that maintain strong consistency with the underlying 3D assets*

整个 pipeline 由以下关键模块串联构成：

1. **多视角 RGB 与点图渲染**：从输入的 3D 资产（mesh）出发，渲染多个固定视角的 RGB 图像，并同步计算每个视角对应的点图——即物体在规范空间中的归一化坐标（canonical-space coordinates）的光栅化结果。这些 RGB-点图对构成后续扩散模型的条件输入。

2. **VAE 编码**：渲染得到的多视角 RGB 图像与点图分别通过 VAE 编码器被映射为潜在空间中的 token 序列，形成条件 token 序列。

3. **共享位置编码与位移**：为确保 RGB 分支与点图分支在生成过程中保持空间对齐，两个分支的 token 共享同一套位置编码。同时，为避免条件 token 与目标 token 在空间位置上发生重叠，对条件 token 施加统一的位移操作：对于空间位置 $(i, j)$ 的条件 token，其位置编码被设置为 $(i - w, j)$，其中 $w$ 为目标潜在图像的宽度。这一设计使网络能够学习到 RGB 与点图之间的像素级对应关系。

4. **MMDiT 骨干网络**：框架基于 Flux.1-dev 的 MMDiT（Multi-Modal Diffusion Transformer）架构。条件 token 序列与目标 token 序列拼接后送入 Transformer，在扩散过程中同时去噪 RGB 与点图两个域的信号。

5. **域解耦机制**：为避免纹理信息从 RGB 域渗漏到几何域，框架引入了两个关键设计：
   - **域特定 LoRA**：采用双 LoRA 结构——Reference-LoRA 负责学习一般外观特征，Domain-LoRA 负责学习几何特征，由域切换器根据当前域激活对应的 LoRA。
   - **文本无关注意力**：在点图分支中，通过注意力掩码屏蔽文本 token，防止背景语义信息干扰几何生成。

6. **联合输出**：扩散过程结束后，解码得到空间对齐的 RGB 图像与点图。点图提供了显式的 3D 几何约束，确保生成的 RGB 图像在几何结构与纹理映射上与参照 3D 资产保持一致。

整个框架的优化目标可形式化为学习条件分布 $p(x_I, x_P \mid y, c)$，其中 $x_I$ 为目标 RGB 图像，$x_P$ 为对应的点图，$y$ 为参照 3D 模型，$c$ 为文本提示。通过联合建模这两个域，RefAny3D 在生成过程中同时约束了外观与几何，从而实现对 3D 参照物的高保真一致图像生成。

## 核心模块与公式推导

RefAny3D 的核心思想是将图像生成形式化为对 RGB 外观与点图（canonical-space 坐标）联合分布的条件建模。给定一个 3D 参照资产 $y$ 和文本提示 $c$，模型学习目标 RGB 图像 $x_I$ 与对应点图 $x_P$ 的联合条件分布：

$$p ( x _ { I } , x _ { P } | y , c )$$

这一联合建模策略使点图成为 3D 几何的显式代理，在生成过程中为 RGB 分支提供空间锚定，从而强制实现几何-纹理一致性。

### 空间对齐的双分支生成架构

为实现上述联合建模，RefAny3D 采用空间对齐的双分支生成框架，同时输出 RGB 图像和点图。其关键设计在于跨域共享位置编码（Shared Positional Embedding for Cross-Domain）：RGB 分支与点图分支的 token 使用相同的位置编码，使网络能够学习像素级的跨域对应关系。对于条件 token（来自多视角渲染输入），其空间位置 $(i, j)$ 被统一位移为 $(i - w, j)$，其中 $w$ 为目标潜在图像的宽度。这一位移确保条件 token 与目标 token 在空间上不重叠，同时保持位置先验的一致性。

### 域解耦生成机制

为避免 RGB 纹理信息与点图几何信息相互干扰，RefAny3D 引入了两个关键的解耦模块：

**域特定 LoRA（Domain-specific LoRA）。** 模型采用双 LoRA 结构：Reference-LoRA 学习通用的物体外观特征，Domain-LoRA 专门学习点图的几何特征。通过域切换器（domain switcher）控制，两个 LoRA 分别在不同域中被激活，从而解耦外观学习与几何学习，防止纹理渗漏到点图分支。

**文本无关注意力（Text-agnostic Attention）。** 在点图分支中，文本 token 被显式屏蔽，不参与对点图 token 的注意力计算。这阻断了文本背景语义信息向几何生成分支的泄漏，避免点图背景与 RGB 分支产生错误对齐，从而消除由此引发的伪影。

### 消融验证

消融实验系统性地验证了上述模块的必要性（见 Figure 7 和 8）：
- 去除共享位置编码后，网络缺乏位置先验，无法准确学习 RGB 与点图的像素级对应关系，导致几何偏差。
- 去除文本无关注意力后，点图分支受文本语义干扰，点图背景与 RGB 分支对齐，产生伪影。
- 去除域特定 LoRA 后，单一 LoRA 无法同时高质量生成 RGB 和点图，整体生成质量下降。
- 完全移除点图分支使模型丧失显式 3D 几何信息，训练不稳定，且生成结果与 3D 资产严重不一致。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/009_Figure_7.jpg]]
*Figure 7: Ablation studies on different components of our method: (a) full model; (b) without Shared Positional Embedding for Cross-Domain; (c) without Text-agnostic Attention; (d) without Domain-specific LoRA*

这些消融结果共同证明：共享位置编码提供空间对齐基础，文本无关注意力阻断语义泄漏，域特定 LoRA 实现外观与几何的解耦——三者协同作用，是 RefAny3D 实现 3D 一致性生成的关键因果机制。

### 补充图表

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/010_Figure_8.jpg]]
*Figure 8: Comparisons of ablation studies and the editing-based baseline*

## 实验与分析

### 主实验设置

RefAny3D 以 **Flux.1-dev** 作为基础扩散模型，采用 **Prodigy** 优化器进行训练（Tan et al., 2025）。训练数据通过自动化管线构建：对 Subjects200k 数据集中的每张图像，使用 **GroundingDINO** (Liu et al., 2024) 提取目标物体，经 **Hunyuan3D** (Zhao et al., 2025) 重建为 3D 资产，最后用 **FoundationPose** (Wen et al., 2024) 估计姿态并渲染多视角 RGB-点图对（Figure 3）。训练在 8 张 H800 GPU 上约需 8 天。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/003_Figure_3.jpg]]
*Figure 3: (a) Data construction pipeline. We first use GroundingDINO (Liu et al., 2024) to extract the objects of interest, then convert the images into 3D models using Hunyuan3D (Zhao et al., 2025), and finally apply FoundationPose (Wen et al., 2024) to estimate the poses of the 3D models in the images. (b) Examples from the dataset*

### 定量结果

Table 1 和 Table 2 汇总了与主流基线的定量对比。RefAny3D 在所有评估维度上均取得最优结果：

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/007_Table_2.jpg]]
*Table 2: Quantitative results of the user study. We evaluate 3D consistency (Faithful), identity preservation (ID), aesthetic quality, and overall ranking (Rank)*

- **GPT-eval 综合得分**：RefAny3D 的 GPT-eval Overall 达到 **7.123**，其中纹理一致性（Texture）**6.315**，几何一致性（Geometric）**7.368**，显著超越次优基线。
- **视觉基础模型指标**：CLIP Image/Avg. 为 **0.873**，DINO Avg. 为 **0.720**，GIM Count 为 **3901.316**，均优于对比方法。
- **用户调研**：在 3D 一致性（Faithful, **4.655**）、身份保持（ID, **4.737**）、美学质量（Aesthetic, **4.632**）和综合排名（Rank, **1.579**）四项指标上全面领先。

这些结果表明，联合建模 RGB 与点图的条件分布，并引入空间对齐的双分支生成，能有效将 3D 几何先验转化为生成结果中的几何与纹理一致性。

### 定性对比

Figure 4 展示了与 Textual Inversion、DreamBooth、IP-Adapter、DSD、OminiControl 等方法的定性对比。RefAny3D 在保持参照物几何结构和纹理细节方面具有明显优势：基线方法常出现视角不一致、纹理漂移或几何变形，而 RefAny3D 生成的图像与输入 3D 资产在几何和纹理上均保持高度一致。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with other methods. Our approach achieves superior geometric and texture consistency compared to alternative methods*

Figure 5 进一步展示了不同 3D 资产作为参照时的生成结果。模型以统一方式同时输出目标视角的 RGB 图像与点图，通过强制点图与 RGB 输出的像素级空间对齐，确保跨视角的几何-纹理对应关系。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results with different 3D assets as references. Our method takes a given 3D mesh as input and generates both RGB images and point maps in a unified manner. By enforcing pixel-level spatial alignment between the point maps and RGB outputs, the framework ensures consistent geometry–texture correspondence across views. Moreover, the incorporation of point maps enhances the model’s 3D structural awareness, thereby improving the fidelity and consistency of image generation with respect to the reference 3D assets*

### 消融实验

Figure 7 和 Figure 8 系统消融了各核心组件的作用：

- **去除共享位置编码**（Figure 7b）：网络失去位置先验，无法准确学习 RGB 与点图之间的像素级对应关系，导致生成结果出现几何偏差。
- **去除文本无关注意力**（Figure 7c）：点图分支受文本背景语义干扰，点图背景与 RGB 分支错误对齐，产生伪影。
- **去除域特定 LoRA**（Figure 7d）：单一 LoRA 无法同时高质量生成 RGB 与点图两个域的内容，整体生成质量明显下降。
- **完全移除点图分支**（Figure 8）：模型丧失显式 3D 几何信息，训练不稳定，且生成结果与 3D 资产严重不一致。
- **减少输入视角数**（Figure 8）：即使仅使用 6 或 4 个视角，方法仍可有效工作，但性能随视角数增加而持续提升，验证了多视角条件对几何一致性的正向贡献。

### 应用拓展与可控性

Figure 6 表明 RefAny3D 可无缝集成到现有多视图图像到 3D 的生成管线中，增强其 3D 一致性。Figure 9 展示了从不同视点可控生成物体图像的能力，进一步验证了模型对视角条件的鲁棒响应。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/012_Figure_9.jpg]]
*Figure 9: An example of controllable generation of object images from different viewpoints*

### 失败模式与局限

Figure 10 揭示了方法的主要局限：RefAny3D 面向**刚性物体**设计，未建模场景中的非刚性物理交互（如布料变形、软体挤压），导致此类场景下生成结果与参照物出现不一致。此外，自动化数据管线依赖姿态估计与 3D 重建，可能引入纹理或几何误差，影响模型性能上限。训练所需的 8×H800 GPU 约 8 天的计算开销，也限制了方法在更大规模或更高视角数条件下的直接扩展。

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/011_Figure_10.jpg]]
*Figure 10: Limitation on non-rigid objects. While our method achieves high fidelity to the input 3D assets, it does not account for physical interactions in the scene*

### 补充图表

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/001_Figure_1.jpg]]
*Figure 1: Results of our RefAny3D. Given a 3D asset, our method can generate high-quality and 3D asset-consistent images*

![[assets/figures/papers/paper_list_l58_https_openreview_net_forum_id_fUO37EVR7j/figures/013_Figure_11.jpg]]
*Figure 11: Qualitative results with different 3D assets as references*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

RefAny3D 处于“参考驱动图像生成”与“3D感知生成”的交汇点。其核心贡献在于将条件信号从单张2D图像升级为多视角RGB-点图对，并以此建模RGB外观与3D几何的联合分布。这一设计直接回应了现有方法的瓶颈：基于2D参考的方法缺乏显式3D先验，导致生成结果在几何和纹理上与参照物不一致。

**与个性化/主体驱动生成的对比。** 早期工作如 **Textual Inversion** (Gal et al., 2022) 和 **DreamBooth** (Ruiz et al., 2023) 通过优化文本嵌入或微调模型来绑定特定主体，但条件来源仍是少量2D图像，无法利用3D资产的结构化信息。**IP-Adapter** (Ye et al., 2023) 和 **DSD** (Cai et al., 2025) 引入了图像提示适配器或共享注意力机制，增强了2D参考的利用效率，但本质上仍以RGB外观为唯一条件通道，缺乏对几何一致性的显式约束。RefAny3D 将条件格式从“单张/少量RGB图像”替换为“多视角RGB-点图对”，使模型能够同时感知外观和规范空间坐标，从而在生成过程中锚定3D几何。

**与可控生成的对比。** **OminiControl** (Tan et al., 2025) 提供了对扩散变压器的通用控制框架，但其控制信号仍限于2D空间（如深度图、边缘图）。RefAny3D 在架构层面借鉴了类似的条件注入思想，但通过双分支生成和域解耦机制，将控制维度拓展到了3D规范空间。与OminiControl的单分支条件注入不同，RefAny3D 的空间对齐双分支架构要求RGB与点图共享位置编码，这构成了方法间的关键分叉点。

**与3D生成方法的对比。** 现有3D资产生成方法（如基于Score Distillation Sampling的方法）通常从文本或单图重建3D表示，再渲染为2D图像。RefAny3D 反其道而行之：将3D资产作为输入条件，直接生成2D图像及其对应的点图。这使得它天然适配“给定3D资产、生成一致2D内容”的下游任务，而非3D重建本身。

### 2. 适用边界与能力定位

RefAny3D 的能力边界由以下设计选择划定：

- **刚性物体假设。** 方法依赖点图提供规范空间坐标，这要求参考物体在生成过程中保持刚性。对于非刚性物体（如衣物、软体动物），规范空间坐标无法准确描述变形状态，导致生成失败（参见 Figure 10）。这是当前方法的核心局限。
- **多视角条件依赖。** 方法需要从3D资产渲染多视角RGB-点图对作为条件。虽然消融实验表明减少视角数（如6或4个）仍可工作，但性能随视角数增加而持续提升。这带来了计算开销与条件质量之间的权衡。
- **数据管线的上限约束。** 训练数据依赖自动化管线（GroundingDINO + Hunyuan3D + FoundationPose）从2D图像重建3D资产并估计姿态。该管线可能引入纹理或几何误差，这些误差会通过训练数据传播，成为模型性能的上限约束。
- **可控视角生成。** 方法支持从指定视角生成目标图像（Figure 9），但其视角可控性受限于训练数据中的视角分布，而非任意自由视角。

### 3. 局限与开放问题

**已知局限。**
1. **非刚性物体不适用。** 方法未建模场景中的物理交互（如布料褶皱、弹性形变），对非刚性物体的生成保真度显著下降。
2. **计算开销。** 训练需8张H800 GPU约8天，多视角条件增加了推理时的token序列长度，对实时应用不够友好。
3. **数据质量依赖。** 自动化3D重建管线引入的误差可能限制模型上限，尤其是在纹理复杂或被遮挡物体的场景中。

**开放问题。**
1. **扩展到非刚性物体。** 如何将参考条件从刚性点图推广到可变形几何表示（如骨架驱动变形、神经场），以支持更广泛的物体类别？
2. **降低多视角条件开销。** 能否通过视角选择策略、条件压缩或知识蒸馏，在保持3D一致性的前提下减少条件视角数？
3. **与视频/场景生成的结合。** 能否将RefAny3D的点图一致性约束扩展到视频生成或3D场景生成，实现动态一致的3D资产引导内容创作？
4. **条件鲁棒性。** 当输入的3D资产质量较低（如稀疏重建、噪声纹理）时，方法的表现如何？是否需要额外的条件增强或鲁棒训练策略？

## 原文 PDF

![[paperPDFs/ICLR_2026/RefAny3D_3D_Asset_Referenced_Diffusion_Models_for_Image_Generation_af40724eea65.pdf]]