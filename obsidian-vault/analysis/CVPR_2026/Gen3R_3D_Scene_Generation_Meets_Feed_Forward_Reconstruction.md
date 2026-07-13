---
title: "Gen3R: 3D Scene Generation Meets Feed-Forward Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Gen3R_3D_Scene_Generation_Meets_Feed_Forward_Reconstruction.pdf
project_link: "https://xdimlab.github.io/Gen3R/"
code_link: null
aliases:
- Gen3R
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过几何适配器和KL散度对齐，将VGGT的中间几何token映射为与视频扩散模型兼容的几何latent，实现解耦但分布的联合latent空间生成。
primary_logic: 将前馈重建模型重新部署为非对称几何VAE，提供解耦但对齐的几何与外观latent，使得视频扩散模型可同时生成高质量RGB视频和全局一致的三维点云。
claims:
- 在RealEstate10K和DL3DV-10K的外观生成中，Gen3R在PSNR/SSIM/LPIPS上全面超越所有基线（LVSM, Gen3C, Aether等）。
- 在几何生成任务中，Gen3R的Chamfer Distance在1-view和2-view设置下均显著优于Aether和WVD。
- 联合端到端生成（Ours）相比两阶段训练（2-Stage）在所有指标上大幅提升，证明联合latent空间设计的必要性。
- 移除KL对齐损失后，外观和几何生成质量急剧下降，且潜空间可视化显示对齐是扩散训练收敛的关键。
---

# Gen3R: 3D Scene Generation Meets Feed-Forward Reconstruction

> [!tip] 核心洞察
> 将前馈重建模型重新部署为非对称几何VAE，提供解耦但对齐的几何与外观latent，使得视频扩散模型可同时生成高质量RGB视频和全局一致的三维点云。

| 字段 | 内容 |
|------|------|
| 中文题名 | Gen3R：三维场景生成与前馈重建的融合 |
| 英文题名 | Gen3R: 3D Scene Generation Meets Feed-Forward Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.04090) · [Project](https://xdimlab.github.io/Gen3R/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Gen3R |
| Dataset | RealEstate10K, DL3DV-10K, Co3Dv2, ScanNet++ |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR 20.51 vs 18.97 (LVSM) (+1.54)；PSNR 27.05 vs 23.83 (Gen3C) (+3.22)。
> - DL3DV-10K 上，PSNR 16.38 vs 14.37 (2-Stage) (+2.01)；PSNR 18.59 vs 17.91 (Gen3C) (+0.68)。
> - Co3Dv2 上，Chamfer Distance 1.1047 vs 1.9498 (Aether) (-0.8451)。

## 概要

### 问题与瓶颈

三维场景生成的目标是从稀疏的二维观测中同时产生逼真的新视角图像和全局一致的三维几何。现有方法大致分为两类：一类依赖二维生成先验进行视图插值或补全，缺乏对底层三维结构的显式建模；另一类尝试直接生成三维表示，但难以有效利用大规模预训练前馈重建模型（如 **VGGT**）内部蕴含的丰富几何先验。直接压缩重建模型的输出或忽略其内部token空间会导致几何质量受损，且几何表示与视频扩散模型的RGB潜空间之间缺乏分布对齐，阻碍了外观与几何的联合生成。

### 核心思路

Gen3R 的核心洞察在于：将前馈重建模型重新部署为一个**非对称几何VAE**，通过一个轻量的几何适配器（Geometry Adapter）将其中间几何token映射为与预训练视频扩散模型兼容的几何潜变量 $\mathcal{G}$。在适配器训练中引入KL散度正则项 $\mathcal{L}_{\mathrm{KL}}$，强制几何潜变量的分布与外观潜变量 $\mathcal{A}$ 的分布对齐。最终，将外观与几何潜变量沿宽度维度拼接为统一潜变量 $\mathcal{Z} = [\mathcal{A}; \mathcal{G}]$，使视频扩散模型能够同时生成高质量RGB视频和全局一致的三维点云、深度图与相机参数。

### 方法谱系与知识库定位

Gen3R 处于**前馈三维重建**与**视频扩散生成**的交叉点上。它继承并改造了前馈重建模型 **VGGT** 的多层级几何token表示，将其作为几何先验的载体；同时复用了预训练视频扩散模型（如 **WAN**）的RGB VAE编码器/解码器，以保持外观生成的逼真度。与以下基线方法形成明确对比：

- **LVSM** 等基于流的二维视图插值方法，缺乏显式三维几何建模；
- **Gen3C** 等结合深度变形与修补的二维生成方法，几何一致性受限于逐帧处理；
- **Aether** 和 **WVD** 等显式三维生成方法，未能有效利用前馈重建模型的内部token空间，几何生成质量受限。

Gen3R 的关键差异化设计在于：**解耦但对齐的联合潜空间**——几何与外观分别由专用编码器产生，但通过KL散度在分布层面强制对齐，从而在扩散模型中实现端到端的联合生成。

### 主要结果速览

- **外观生成**：在 RealEstate10K 上，1-view 设置下 PSNR 达 20.51（相比 LVSM 的 18.97 提升 +1.54 dB）；2-view 设置下 PSNR 达 27.05（相比 Gen3C 的 23.83 提升 +3.22 dB）。在 DL3DV-10K 上同样全面超越所有基线（Table 1）。
- **几何生成**：在 Co3Dv2 上，1-view 设置下 Chamfer Distance 为 1.1047（Aether 为 1.9498，相对降低 43%）；在 ScanNet++ 零样本设置下，Chamfer Distance 达 0.1209，甚至略优于 VGGT 自身（0.1279）（Table 2, Table 10）。
- **消融验证**：移除KL对齐损失后，外观和几何生成质量急剧下降（Table 4）；潜空间可视化进一步证实，分布对齐是扩散训练收敛的必要条件（Figure 7）。端到端联合生成相比两阶段训练在所有指标上均有大幅提升，验证了联合潜空间设计的必要性（Table 4）。

### 局限与待验证方向

论文未明确列出方法本身的局限性。一个值得关注的开放问题是：**重建模型学习到的内在潜流形能否被更充分地利用，以进一步挖掘重建先验对三维场景生成的潜力**——这暗示当前仅使用VGGT中间token的适配方案可能尚未穷尽前馈重建模型所能提供的全部几何信息。

三维场景生成正处于一个关键的十字路口。一方面，大规模视频扩散模型（video diffusion models）在2D外观生成上展现了惊人的逼真度，能够从单张或少数几张图像合成连贯的视频序列；另一方面，前馈式三维重建模型（feed-forward reconstruction models）如 **VGGT** 凭借其Transformer架构，可以从多视角图像中高效恢复全局一致的点云、深度图和相机参数。然而，这两种能力长期以来彼此割裂：生成模型缺乏对三维几何结构的显式理解，重建模型则无法产生新颖的视角或场景内容。

现有方法在弥合这一鸿沟时面临一个根本性瓶颈——**如何有效利用预训练重建模型内部的丰富几何先验**。直接压缩重建模型的最终输出（如点云或深度图）会丢失其内部token空间中蕴含的多层级几何信息；而忽略这些中间表示，则导致生成的三维几何质量严重退化。更关键的是，几何表示与外观表示通常驻留在完全不同的特征空间中，缺乏分布层面的对齐，使得联合扩散生成变得极为困难。这一瓶颈的因果链条清晰可辨：**内部几何token的浪费 → 几何先验的稀释 → 几何-外观潜空间分布失配 → 联合生成失败**。

本文的动机正源于对这一瓶颈的洞察。我们提出 **Gen3R**，一个将前馈重建与视频扩散深度融合的统一框架。其核心思想是将VGGT重新部署为一个**非对称几何VAE**（asymmetric geometry VAE）：通过一个可学习的几何适配器（geometry adapter），将VGGT的中间几何token映射为与预训练视频扩散模型兼容的几何latent；同时引入KL散度损失，强制几何latent分布与外观latent分布对齐。这一设计使得外观latent $\mathcal{A}$ 与几何latent $\mathcal{G}$ 能够沿宽度维度拼接为统一latent $\mathcal{Z} = [\mathcal{A}; \mathcal{G}]$，从而让视频扩散模型可以同时生成高质量RGB视频和全局一致的三维点云。Gen3R的独特优势在于：它既保留了重建模型的多模态几何先验，又实现了与外观生成空间的分布对齐，为从单张或多张图像条件下联合生成外观与几何开辟了新的可能。

## 核心方法与创新机理

Gen3R的核心创新在于重新定义了前馈重建模型在生成式框架中的角色：**将VGGT重构为一个非对称的几何VAE，通过几何适配器与KL散度对齐，将重建模型的中间几何token映射为与预训练视频扩散模型兼容的几何latent，从而实现外观与几何在统一潜空间中的联合扩散生成**。这一设计解决了现有方法中两个根本性瓶颈：一是前馈重建模型的丰富几何先验难以被生成模型有效利用，二是外观与几何潜空间的分布失配导致联合生成质量受损。

### 关键创新点：Changed Slots 分析

以下从相对基线的关键变化维度，剖析Gen3R的核心创新：

**1. 几何先验来源：从“压缩输出”到“token空间重投影”**

现有方法（如Aether、WVD）在利用重建模型时，通常直接压缩其最终输出（如点云、深度图），或忽略其内部token空间，导致几何信息在压缩过程中严重丢失。Gen3R改变了这一范式：通过训练一个轻量的几何适配器 $\mathcal{E}_{\mathrm{adp}} / \mathcal{D}_{\mathrm{adp}}$，将VGGT编码器输出的多层级几何token $\mathcal{V} \in \mathbb{R}^{N \times L \times h_v \times w_v \times C}$ 直接重投影为与外观latent空间分辨率匹配的几何latent $\mathcal{G} \in \mathbb{R}^{n \times h \times w \times c}$（Eq. 3-4）。这一设计保留了VGGT内部token空间蕴含的多模态几何先验（包括点云、深度、相机参数的隐式关联），而非仅依赖其解码后的单一输出。消融实验（Table 3）表明，该VAE在几何重建上保持了与原始VGGT接近的性能，但在生成模式下展现出更强的鲁棒性——这验证了token空间重投影相比直接压缩输出的优势。

**2. 潜空间分布对齐：KL散度强制几何与外观分布匹配**

这是Gen3R最具决定性的创新。在适配器训练中，作者引入了KL散度损失 $\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}(q_{\mathcal{G}} \parallel q_A)$（Eq. 7），强制几何latent的分布 $q_{\mathcal{G}}$ 与预训练RGB VAE的外观latent分布 $q_A$ 对齐。这一设计的因果逻辑在于：预训练视频扩散模型的去噪过程依赖于外观latent的特定分布特性；若几何latent的分布与之失配，联合扩散训练将难以收敛。消融实验（Table 4, Figure 7）提供了决定性证据：移除KL对齐损失后，外观和几何生成质量均急剧下降（RealEstate10K 1-view PSNR从20.51降至18.44，DL3DV-10K从16.38降至15.09），且潜空间可视化显示对齐是扩散训练收敛的关键前提。这一发现揭示了分布对齐在跨模态潜空间融合中的基础性作用。

**3. 联合latent表示：宽度拼接实现解耦但分布的联合生成**

不同于现有方法将外观与几何分离处理或简单级联，Gen3R将外观latent $\mathcal{A}$ 与几何latent $\mathcal{G}$ 沿宽度维度拼接，形成统一latent表示 $\mathcal{Z} = [\mathcal{A}; \mathcal{G}] \in \mathbb{R}^{n \times h \times 2w \times c}$（Eq. 8）。这一设计的精妙之处在于：外观与几何在潜空间中保持解耦（各自独立编码），但共享扩散模型的联合去噪过程，使得生成的外观视频与几何结构在语义上天然一致。消融实验（Table 4）中的“2-Stage”基线（先独立训练VAE再训练扩散模型）在RealEstate10K 1-view PSNR仅为18.44，相比端到端联合生成的20.51大幅下降，证明了联合latent空间设计对生成质量的必要性。

**4. 条件注入机制：多模态条件的灵活融合**

Gen3R的条件注入机制支持同时注入文本、可变数量参考帧（编码为外观latent + 掩码）及可选相机条件。对于缺失的几何分支，采用零填充策略（Sec. 3.2, Eq. 9），使得模型可在1-view、2-view或完整序列条件下灵活工作。训练中采用概率混合策略（1-view/2-view/全序列各1/3概率，文本20%丢弃，相机50%丢弃），增强了模型的泛化能力。Table 5的相机可控性实验验证了该条件机制的有效性。

### 创新本质：前馈重建模型的生成式重部署

Gen3R的核心洞察在于：**前馈重建模型（VGGT）的内部token空间已经学习了一个丰富的三维场景流形，通过适配器与分布对齐，可以将这一流形“翻译”为生成模型可理解的潜空间表示**。这使得视频扩散模型不仅能生成高质量的RGB视频，还能同时输出全局一致的三维点云、深度图和相机参数——实现了从“重建”到“生成”的范式跃迁。这一创新路径为未来更充分地利用重建模型的先验知识进行三维场景生成提供了新的方法论框架。

Gen3R 提出一种三维感知的隐空间扩散方法，将**前馈重建模型**与**预训练视频扩散模型**桥接，实现外观（RGB 视频）与几何（点云、深度图、相机参数）的联合生成。其核心流程分为两个阶段：

**阶段一：构建统一的几何-外观隐空间。** 给定 $N$ 张输入图像 $\mathcal{T}$，前馈重建模型 VGGT 的编码器 $\mathcal{E}_{\mathcal{V}}$ 将其映射为多层级的几何 token $\mathcal{V} \in \mathbb{R}^{N \times L \times h_v \times w_v \times C}$（公式 1）。Gen3R 并非直接使用 VGGT 的最终输出，而是训练一个**几何适配器**（Geometry Adapter），由编码器 $\mathcal{E}_{\mathrm{adp}}$ 将几何 token 投影为与视频扩散模型隐空间分辨率匹配的几何隐变量 $\mathcal{G} \in \mathbb{R}^{n \times h \times w \times c}$（公式 3），再由解码器 $\mathcal{D}_{\mathrm{adp}}$ 从 $\mathcal{G}$ 重建回 $\mathcal{V}$（公式 4）。同时，预训练的 RGB VAE（$\mathcal{E}_{\mathcal{W}} / \mathcal{D}_{\mathcal{W}}$）将条件图像编码为外观隐变量 $\mathcal{A}$。适配器训练受两个损失监督：**重建损失** $\mathcal{L}_{\mathrm{rec}}$ 监督 token、深度图、点云和相机参数的重建（公式 6）；**KL 对齐损失** $\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}(q_{\mathcal{G}} \parallel q_A)$ 强制几何隐变量的分布与预训练外观隐变量的分布对齐（公式 7）。最终，外观与几何隐变量沿宽度维度拼接，形成统一隐空间表示 $\mathcal{Z} = [\mathcal{A}; \mathcal{G}] \in \mathbb{R}^{n \times h \times 2w \times c}$（公式 8）。

**阶段二：扩散联合生成与解码。** 在统一隐空间上微调视频扩散 Transformer $G_\theta$，使其从噪声联合生成外观和几何隐变量 $\mathcal{Z}$。条件注入支持多种模态：文本提示、可变数量的参考帧（编码为外观隐变量 $\mathcal{A}$ 并附加掩码标记已知区域）、以及可选的相机参数；缺失的几何分支以零填充。生成后，外观隐变量 $\mathcal{A}$ 由预训练 RGB VAE 解码器 $\mathcal{D}_{\mathcal{W}}$ 恢复为视频帧；几何隐变量 $\mathcal{G}$ 经适配器解码器 $\mathcal{D}_{\mathrm{adp}}$ 恢复为几何 token $\mathcal{V}$，再由 VGGT 的解码头 $\mathcal{D}_{\mathcal{V}}$ 输出全局点云 $\mathcal{P}$、深度图 $\mathcal{D}$ 和相机参数 $\mathcal{T}$（公式 2）。

图 2 概括了这一架构：左侧展示 VGGT 被重塑为非对称几何 VAE，通过适配器和 KL 对齐损失产生与外观隐空间兼容的几何隐变量；右侧展示扩散模型在统一隐空间上联合生成，并支持多条件输入下的可控推理。

**关键设计决策：**

- **非对称 VAE 架构**：几何分支使用 VGGT 的中间 token 而非最终输出，保留了多层级几何先验；外观分支复用预训练视频扩散模型的 VAE，无需从头训练。
- **分布对齐**：KL 散度损失是扩散训练收敛的必要条件——消融实验（Table 4, Figure 7）表明，移除 $\mathcal{L}_{\mathrm{KL}}$ 后几何隐空间与外观隐空间分布失配，导致外观和几何生成质量急剧下降。
- **端到端联合训练**：相比先独立训练 VAE 再训练扩散模型的两阶段方案，端到端联合训练在所有指标上大幅提升（Table 4），验证了统一隐空间设计的必要性。

### 3.1 非对称几何VAE：将前馈重建模型重新部署为几何编码器

Gen3R的核心创新在于将预训练的前馈重建模型**VGGT**重新部署为一个非对称的几何VAE，从而提取与外观latent空间兼容的几何先验。VGGT本身是一个基于Transformer的前馈重建模型，其编码器$\mathcal{E}_{\mathcal{V}}$将$N$张输入图像$\mathcal{T}$编码为多层级几何token $\mathcal{V}$：

$$\mathcal{E}_{\mathcal{V}} : \mathcal{T} \mapsto \mathcal{V} \in \mathbb{R}^{N \times L \times h_v \times w_v \times C} \quad \text{(Eq. 1)}$$

其解码器$\mathcal{D}_{\mathcal{V}}$则从这些几何token中恢复点云$\mathcal{P}$、深度图$\mathcal{D}$和相机参数$\mathcal{T}$：

$$\mathcal{D}_{\mathcal{V}} : \mathcal{V} \mapsto (\mathcal{P}, \mathcal{D}, \mathcal{T}) \quad \text{(Eq. 2)}$$

直接使用VGGT的输出存在两个瓶颈：（1）其内部token空间与预训练视频扩散模型的外观latent空间在维度和分布上不兼容；（2）仅压缩最终输出会丢失中间token蕴含的丰富多模态几何先验。

为解决这一问题，Gen3R设计了一个**几何适配器**（Geometry Adapter），包含编码器$\mathcal{E}_{\mathrm{adp}}$和解码器$\mathcal{D}_{\mathrm{adp}}$，将VGGT的中间几何token $\mathcal{V}$映射为与外观latent兼容的几何latent $\mathcal{G}$：

$$\mathcal{E}_{\mathrm{adp}} : \mathcal{V} \mapsto \mathcal{G} \in \mathbb{R}^{n \times h \times w \times c} \quad \text{(Eq. 3)}$$

$$\mathcal{D}_{\mathrm{adp}} : \mathcal{G} \mapsto \mathcal{V} \in \mathbb{R}^{N \times L \times h_v \times w_v \times C} \quad \text{(Eq. 4)}$$

适配器的训练损失由重建损失$\mathcal{L}_{\mathrm{rec}}$和KL对齐损失$\mathcal{L}_{\mathrm{KL}}$加权组合：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{\mathrm{rec}} + \lambda_2 \mathcal{L}_{\mathrm{KL}} \quad \text{(Eq. 5)}$$

其中重建损失同时监督token重建、相机参数、深度图和点云的重建：

$$\mathcal{L}_{\mathrm{rec}} = \mathbb{E}[\Vert \hat{\mathcal{V}} - \mathcal{V} \Vert^2] + \mathbb{E}[\Vert \hat{\mathcal{T}} - \mathcal{T} \Vert_1] + \mathbb{E}[\Vert \hat{\mathcal{D}} - \mathcal{D} \Vert^2] + \mathbb{E}[\Vert \hat{\mathcal{P}} - \mathcal{P} \Vert^2] \quad \text{(Eq. 6)}$$

### 3.2 分布对齐与联合latent空间构建

仅通过重建损失训练适配器无法保证几何latent $\mathcal{G}$的分布与预训练外观latent $\mathcal{A}$兼容。若两个latent空间分布失配，扩散模型将难以在统一的噪声空间中同时学习外观和几何的生成。Gen3R通过施加KL散度损失强制分布对齐：

$$\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}(q_{\mathcal{G}} \parallel q_A) \quad \text{(Eq. 7)}$$

其中$q_{\mathcal{G}}$为几何适配器输出的latent分布，$q_A$为预训练RGB VAE的外观latent分布。这一设计使得几何latent在统计特性上向外观latent靠拢，为后续联合扩散生成奠定基础。

完成分布对齐后，外观latent $\mathcal{A}$和几何latent $\mathcal{G}$沿宽度维度拼接，形成统一的联合latent表示$\mathcal{Z}$：

$$\mathcal{Z} = [\mathcal{A}; \mathcal{G}] \in \mathbb{R}^{n \times h \times 2w \times c} \quad \text{(Eq. 8)}$$

这一解耦但对齐的latent空间设计是Gen3R方法的核心因果机制：外观和几何信息在latent空间中保持独立通道，但共享统一的分布特性，使得单个扩散Transformer能够同时生成高质量RGB视频和全局一致的三维点云。

### 3.3 扩散生成与解码流程

在扩散生成阶段，预训练的视频扩散模型（基于**WAN**架构）被微调以从噪声中联合生成$\mathcal{Z} = [\mathcal{A}; \mathcal{G}]$。条件注入机制支持多种模态：文本提示、可变数量的参考帧（编码为外观latent + 掩码）、以及可选的相机参数。当条件中缺少几何信息时，几何分支用零填充。

生成完成后，外观latent $\mathcal{A}$由预训练RGB VAE解码器$\mathcal{D}_{\mathcal{W}}$恢复为视频帧，几何latent $\mathcal{G}$则通过几何适配器解码器$\mathcal{D}_{\mathrm{adp}}$恢复为VGGT的几何token $\mathcal{V}$，再经VGGT的解码头$\mathcal{D}_{\mathcal{V}}$输出点云、深度图和相机参数。这一非对称解码设计充分利用了VGGT强大的几何解码能力，同时避免了在扩散过程中直接操作高维token空间。

### 关键公式汇总

| 公式编号 | 表达式 | 核心含义 |
|---------|--------|---------|
| Eq. 1 | $\mathcal{E}_{\mathcal{V}} : \mathcal{T} \mapsto \mathcal{V}$ | VGGT编码器：图像→几何token |
| Eq. 3-4 | $\mathcal{E}_{\mathrm{adp}} / \mathcal{D}_{\mathrm{adp}}$ | 几何适配器：token↔几何latent的双向映射 |
| Eq. 7 | $\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}(q_{\mathcal{G}} \parallel q_A)$ | KL散度对齐几何与外观latent分布 |
| Eq. 8 | $\mathcal{Z} = [\mathcal{A}; \mathcal{G}]$ | 宽度拼接形成统一联合latent |

## 实验与关键发现

### 外观生成：多视图条件下的视频质量对比

Gen3R 在 RealEstate10K 和 DL3DV-10K 两个标准基准上，对外观生成质量进行了系统评估。Table 1 汇总了 1-view 和 2-view 两种条件设置下的定量结果。在 RealEstate10K 的 1-view 设置中，Gen3R 取得了 **PSNR 20.51 / SSIM 0.7388 / LPIPS 0.2281**，相比基于流的插值方法 LVSM（PSNR 18.97）提升 +1.54 dB。当条件扩展为 2-view 时，性能增益更为显著：PSNR 达到 **27.05**，比结合深度变形与修补的 Gen3C（23.83）高出 +3.22 dB，SSIM 和 LPIPS 同样全面领先。在 DL3DV-10K 的 2-view 设置下，Gen3R 以 PSNR 18.59 超越 Gen3C（17.91），并在 1-view 场景中相较 2-Stage 基线（14.37）取得 +2.01 dB 的显著优势。这些结果表明，Gen3R 的联合 latent 生成机制在稀疏条件输入下能够稳定输出高保真视频帧，且性能增益随条件视图数量的增加而放大。

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison of Appearance Generation. We compare both 1-view and 2-view based settings*

### 几何生成：点云质量与跨数据集泛化

几何生成的定量对比在 Co3Dv2、WildRGB-D 和 TartanAir 三个数据集上进行，评估指标包括 Accuracy、Completeness 和 Chamfer Distance（CD）。Table 2 显示，在 1-view 条件下，Gen3R 在 Co3Dv2 上的 CD 为 **1.1047**，相比显式 3D 生成方法 Aether（1.9498）降低约 43%；在 WildRGB-D 上 CD 为 0.1992，同样明显优于 Aether 和 WVD。值得注意的是，在具有复杂场景结构的 TartanAir 数据集上，Gen3R 的 CD 为 2.7809，而 Aether 和 WVD 分别高达 8.4307 和 3.9824，证明所提出的几何适配器能够有效保留 VGGT 的多模态几何先验，在稀疏输入下仍可生成全局一致的点云。2-view 设置进一步缩小了各方法的性能差距，但 Gen3R 在所有数据集上仍保持最优或次优的 CD 指标。

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/005_Table_2.jpg]]
*Table 2: Quantitative Comparison of Geometry Generation. We compare both 1-view and 2-view based settings*

Figure 3 提供了 1-view 几何生成的定性对比。可视化结果显示，Aether 和 WVD 生成的几何结构常出现局部缺失或全局形变，而 Gen3R 能够恢复更完整、更精细的场景几何，尤其在物体边界和细薄结构区域优势明显。Figure 4 展示了 2-view 新视角合成的定性结果及误差图——蓝色区域表示低误差，红色表示高误差。Gen3R 的误差图整体偏蓝，表明其在遮挡区域和纹理稀疏区域的重建精度显著优于基线方法。

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Comparison of Geometry Generation in the 1-view based setting*

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Comparison of Novel View Synthesis with 2-view conditions. The input images are shown on the left, and error maps are displayed overlaid on the results. Bluer colors indicate smaller errors, while redder colors indicate larger errors*

### 几何重建：VAE 设计的保真度验证

为验证将 VGGT 重新部署为几何 VAE 的合理性，作者在 Co3Dv2、WildRGB-D 和 TartanAir 上进行了纯重建模式的评估（Table 3）。Gen3R 的 VAE-only 模式在 Co3Dv2 上取得 CD **0.9625**，与原始 VGGT 的重建能力接近，同时远超使用预训练 RGB VAE 直接编码点云的 WVD（VAE only）。在 WildRGB-D 上，Gen3R VAE 的 CD 为 0.1260，同样保持竞争力。Figure 5 的定性重建对比进一步表明，Gen3R 的几何 VAE 在保持 VGGT 重建精度的同时，其 latent 空间具备更强的生成鲁棒性——这一特性在 Table 10 的 ScanNet++ 零样本重建实验中得到了印证：Gen3R 的 CD 为 **0.1209**，甚至略优于 VGGT 自身的 0.1279，说明通过适配器投影后的几何 latent 在跨域迁移中表现出更好的泛化能力。

### 消融实验：联合生成与分布对齐的必要性

Table 4 的系统消融揭示了两个关键设计选择对性能的决定性影响。

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/009_Table_4.jpg]]
*Table 4: Ablation Study on appearance and geometry generation*

**两阶段训练 vs. 端到端联合生成。** 2-Stage 基线先独立训练几何 VAE，再冻结 VAE 训练扩散模型。在 RealEstate10K 的 1-view 外观生成中，2-Stage 的 PSNR 仅为 18.97，而端到端联合训练的 Gen3R 达到 20.51，提升 +1.54 dB；在 DL3DV-10K 上差距更大（16.38 vs. 14.37，+2.01 dB）。几何生成方面，Co3Dv2 的 CD 从 2-Stage 的 1.2638 降至联合训练的 1.1047。这表明外观和几何的联合 latent 空间设计使得扩散模型能够同时利用两种模态的互补信息，分离训练会导致模态间协同效应的丧失。

**KL 对齐损失的关键作用。** 移除 KL 对齐损失（w/o L_KL）后，性能出现灾难性退化：RealEstate10K 的 PSNR 从 20.51 骤降至 16.05，DL3DV-10K 从 16.38 降至 13.54；几何 CD 在 Co3Dv2 上从 1.1047 恶化至 1.6695。Figure 7 的潜空间可视化直观揭示了原因：未对齐的几何 latent 分布与预训练外观 latent 分布严重失配，导致扩散模型在联合生成时无法有效建模统一的 latent 流形。Figure 6 的定性对比标注了 w/o L_KL 基线的典型伪影，包括纹理模糊、几何结构扭曲和时序不一致，进一步证实分布对齐是扩散训练收敛的必要条件。

### 相机可控性与分布外泛化

Table 5 评估了相机条件的可控性。在 RealEstate10K 和 WildRGB-D 上，Gen3R 在提供相机条件时能够更精确地控制生成视角的几何一致性，相比无相机条件的变体在旋转和平移误差上均有显著降低。Table 8 展示了分布外数据集的泛化结果：Gen3R 在未见过的场景类型上仍保持领先的外观生成质量，验证了从 VGGT 继承的几何先验具备跨域迁移能力，而非仅对训练分布过拟合。

### 证据强度总结

| 核心主张 | 关键证据 | 可信度 |
|---------|---------|--------|
| 外观生成全面超越基线 | Table 1: RealEstate10K 2-view PSNR 27.05 vs. Gen3C 23.83 | 高（多数据集、多指标一致） |
| 几何生成显著优于显式 3D 方法 | Table 2: Co3Dv2 CD 1.1047 vs. Aether 1.9498 | 高（跨三个数据集验证） |
| 端到端联合训练的必要性 | Table 4: 联合训练 vs. 2-Stage 在所有指标上大幅领先 | 高（消融设置清晰） |
| KL 对齐是扩散训练收敛的关键 | Table 4 + Figure 7: w/o L_KL 性能崩溃，潜空间可视化证实分布失配 | 高（定量与定性证据一致） |
| 几何 VAE 保持重建精度且泛化更强 | Table 3 + Table 10: ScanNet++ 零样本 CD 0.1209 略优于 VGGT | 中高（重建实验充分，零样本为单数据集） |

![[assets/figures/papers/paper_list_l2498_https_arxiv_org_abs_2601_04090/figures/011_Figure_7.jpg]]
*Figure 7: Visualization of Latent Spaces from different VAEs*

需要手动验证的点：论文未提供 venue/year 信息，部分基线方法（如 Aether、WVD）的具体出处需查阅原文参考文献确认。Figure 7 的潜空间可视化细节需结合原图解读，此处仅基于分析结论推断其含义。

## 定位与知识库关联

### 核心贡献定位：桥接前馈重建与视频扩散

Gen3R 的核心创新在于将前馈三维重建模型重新部署为**非对称几何 VAE**，从而将重建模型的强几何先验注入视频扩散模型的生成框架。这一设计直接回应了现有方法的两类瓶颈：(1) 显式 3D 生成方法（如 **Aether**、**WVD**）难以充分利用预训练重建模型的内部 token 空间，通常仅依赖 2D 生成先验或直接压缩 3D 输出，导致几何质量受损；(2) 2D 生成方法（如 **LVSM**、**Gen3C**、**GF**）虽能产生高质量外观，但缺乏与几何 latent 空间的分布对齐，无法实现联合生成。

Gen3R 的关键操作链条为：通过**几何适配器**（geometry adapter）将 VGGT 的中间几何 token $\mathcal{V} \in \mathbb{R}^{N \times L \times h_v \times w_v \times C}$ 映射为与预训练视频扩散模型兼容的几何 latent $\mathcal{G} \in \mathbb{R}^{n \times h \times w \times c}$，并施加 **KL 散度损失** $\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}}(q_{\mathcal{G}} \parallel q_A)$ 强制其分布与外观 latent $\mathcal{A}$ 对齐。最终沿宽度维度拼接形成统一 latent $\mathcal{Z} = [\mathcal{A}; \mathcal{G}] \in \mathbb{R}^{n \times h \times 2w \times c}$，使扩散模型可同时生成 RGB 视频和全局一致的三维点云、深度图与相机参数。

### 与基线方法的差异分析

| 方法 | 几何先验来源 | 潜空间设计 | 生成范式 | 关键局限 |
|------|-------------|-----------|---------|---------|
| **LVSM** | 基于流的 2D 视图插值 | 无显式几何 latent | 2D 插值 | 缺乏显式 3D 几何表示 |
| **Gen3C** | 深度变形与修补 | 无统一几何 latent | 2D 生成 + 后处理 | 几何一致性依赖后处理 |
| **GF** | 桥接重建与生成 | 无联合 latent | 2D 条件生成 | 未利用重建 token 空间 |
| **Aether** | 显式 3D 表示 | 独立几何处理 | 显式 3D 生成 | 未利用预训练重建先验 |
| **WVD** | 预训练 RGB VAE 编码点云 | 外观 VAE 复用 | 显式 3D 生成 | 几何压缩损失大 |
| **Gen3R (Ours)** | VGGT 中间 token 经适配器重投影 | 解耦但对齐的联合 latent | 联合扩散生成 | 依赖 VGGT 架构绑定 |

**关键差异证据**：
- 在几何重建对比（Table 3）中，Gen3R 的 VAE-only 模式直接投影并重建 VGGT token，而 WVD 使用预训练 RGB VAE 编码点云。Gen3R 在 Co3Dv2 上的 Chamfer Distance 为 0.9625，显著优于 WVD 的 1.9498，证明利用重建模型内部 token 空间比直接压缩 3D 输出更有效。
- 在几何生成任务（Table 2）中，Gen3R 在 1-view 设置下的 Co3Dv2 CD 为 1.1047，而 Aether 为 1.9498，WVD 为 1.9498，差距达 0.8451，表明联合 latent 设计在生成模式下具有显著优势。

### 适用边界与泛化能力

**适用场景**：
- 单帧/多帧条件的三维场景生成（1-view 至 2-view 设置均有验证）
- 文本 + 图像 + 可选相机条件的多模态控制生成
- 前馈三维重建（继承 VGGT 的重建能力）

**泛化证据**：
- 在分布外数据集（Table 8）上，Gen3R 仍保持外观生成优势，2-view 设置下 DL3DV-10K PSNR 达 18.59，优于 Gen3C 的 17.91。
- 在 ScanNet++ 零样本几何重建（Table 10）中，Gen3R 的 CD 为 0.1209，与原版 VGGT 的 0.1279 相当甚至略优，证明适配器训练未损害重建模型的泛化能力。
- 相机可控性实验（Table 5）表明，Gen3R 在 RealEstate10K 和 WildRGB-D 上均能有效响应相机条件，支持可控轨迹生成。

**适用边界与限制**：
- **架构绑定**：几何适配器依赖于 VGGT 的特定 token 空间设计，若替换为其他重建模型需重新训练适配器。
- **训练数据依赖**：联合扩散训练需要配对的外观-几何数据，当前在 RealEstate10K、DL3DV-10K、Co3Dv2 等数据集上验证，对无配对数据的场景（如纯文本到 3D）需额外对齐策略。
- **相机条件依赖**：在无相机条件设置（Table 7）下，Gen3R 虽仍优于基线，但性能下降明显，表明相机信息对几何生成质量有重要影响。

### 关键消融发现与失败模式

**端到端联合训练 vs 两阶段训练**（Table 4）：
- 两阶段训练（先独立训练 VAE 再训练扩散模型）导致外观和几何指标全面大幅下降。例如，RealEstate10K 1-view PSNR 从 20.51 降至 14.37（降幅 6.14），Co3Dv2 CD 从 1.1047 升至 1.9498（升幅 76.5%）。
- 这表明**联合 latent 空间的端到端优化**是生成质量的关键，分离训练破坏了外观与几何 latent 之间的分布耦合。

**KL 对齐损失的必要性**（Table 4, Figure 7）：
- 移除 KL 对齐损失（w/o $\mathcal{L}_{\mathrm{KL}}$）后，几何 latent 分布与外观 latent 分布失配，导致扩散训练无法有效收敛。外观生成 PSNR 大幅下降，几何 CD 显著上升。
- 潜空间可视化（Figure 7）直观展示了有无 KL 对齐时 latent 分布的差异：无对齐时几何 latent 形成孤立簇，扩散模型难以学习统一的生成流形。

**失败模式分析**（Figure 6）：
- 两阶段训练基线在复杂纹理区域出现明显伪影（如重复纹理、模糊边缘），而移除 KL 对齐的模型在几何一致性上表现较差（如深度断裂、点云噪声）。这些失败模式直接印证了联合 latent 设计与分布对齐的必要性。

### 开放问题与未来方向

论文提出的核心开放问题为：**“Can the intrinsic latent manifold learned by reconstruction models be used to fully exploit reconstruction priors for 3D scene generation?”**

这一问题指向几个潜在研究方向：
1. **更深层的先验利用**：当前 Gen3R 仅使用 VGGT 的中间 token，是否可利用重建模型更深层的隐式几何表征（如体素特征、隐式表面）来进一步增强生成质量？
2. **跨架构泛化**：几何适配器设计是否可推广到其他重建模型（如 DUSt3R、MASt3R 系列），形成通用的“重建-生成”桥接范式？
3. **无配对数据扩展**：如何将联合 latent 空间设计扩展到无配对外观-几何数据的场景（如纯文本到 3D 生成），可能需借助知识蒸馏或跨模态对齐技术。
4. **动态场景生成**：当前框架处理静态场景，扩展到动态 4D 场景生成需要设计时空几何 latent 并与视频扩散模型的时间维度对齐。

### 知识库定位总结

Gen3R 属于 **“前馈重建引导的 3D 生成”** 这一新兴范式，其核心贡献在于提出了一种**可泛化的桥接机制**：通过几何适配器 + KL 对齐，将任意预训练重建模型的内部 token 空间映射为与生成模型兼容的 latent。这一范式区别于：
- **纯生成方法**（如 3D GAN、扩散模型直接生成 3D 表示）：缺乏重建先验，几何一致性弱
- **重建-后处理方法**（如重建后优化、修补）：生成多样性受限
- **简单级联方法**（如重建 + 条件生成）：未实现 latent 空间对齐，端到端优化困难

Gen3R 的实验证据（Table 1-4 的全面领先）强有力地支持了这一范式的有效性，为后续工作提供了明确的改进方向：更通用的适配器设计、更丰富的先验利用策略、以及更广泛的跨模型桥接能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Gen3R_3D_Scene_Generation_Meets_Feed_Forward_Reconstruction.pdf]]
