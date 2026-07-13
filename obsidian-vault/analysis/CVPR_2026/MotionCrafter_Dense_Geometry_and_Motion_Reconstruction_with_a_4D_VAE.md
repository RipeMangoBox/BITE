---
title: "MotionCrafter: Dense Geometry and Motion Reconstruction with a 4D VAE"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionCrafter_Dense_Geometry_and_Motion_Reconstruction_with_a_4D_VAE.pdf
project_link: "https://ruijiezhu94.github.io/MotionCrafter_Page/"
code_link: null
aliases:
- MotionCrafter
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在世界坐标系下联合建模密集点图与场景流，并采用均值归一化与全VAE微调策略，放松对扩散模型RGB潜空间的对齐约束。
primary_logic: 通过视角一致的世界坐标4D表示（点图+场景流）和无需严格对齐扩散潜空间的训练策略，可有效迁移预训练视频扩散模型的时空先验，实现端到端的高质量几何与运动联合重建。
claims:
- 均值归一化与全VAE微调显著提升户外场景重建质量，远超最大归一化方案。
- 统一几何-运动融合策略在U-Net预测中表现优于分离VAE，尽管VAE重建指标略低。
- 在无需任何后优化的情况下，MotionCrafter在几何重建上平均提升38.64%，在运动估计上平均提升25.0%。
- 确定性训练范式相比扩散范式在几何重建上RelP降低约12.4%，δP提升约12.7%。
---

# MotionCrafter: Dense Geometry and Motion Reconstruction with a 4D VAE

> [!tip] 核心洞察
> 通过视角一致的世界坐标4D表示（点图+场景流）和无需严格对齐扩散潜空间的训练策略，可有效迁移预训练视频扩散模型的时空先验，实现端到端的高质量几何与运动联合重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionCrafter：基于4D VAE的密集几何与运动联合重建 |
| 英文题名 | MotionCrafter: Dense Geometry and Motion Reconstruction with a 4D VAE |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.08961) · [Project](https://ruijiezhu94.github.io/MotionCrafter_Page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionCrafter |
| Dataset | Kubric, Monkaa, Overall geometry, Overall motion |

> [!tip] 效果简介
> - Kubric (geometry) 上，RelP↓ 3.40 vs 8.79 (Zero-MSF+VGGT) (-5.39)。
> - Kubric (motion) 上，EPE↓ 3.40 vs 59.34 (ST4RTrack-S+VGGT) (-55.94)。
> - Monkaa (geometry) 上，RelP↓ 25.88 vs 56.42 (VGGT) (-30.54)。

## 概要

从单目视频中同时恢复密集的三维几何与运动，是视觉感知领域的一项基础性挑战。现有方法通常将几何重建与运动估计分离处理，或仅在相机坐标系下进行成对预测，缺乏全局世界坐标下的统一表示，且依赖后优化步骤对齐跨帧预测，导致长序列运动一致性差、计算效率低。

**MotionCrafter** 针对上述瓶颈，提出了一种基于视频扩散模型的联合重建框架。其核心思路是：在世界坐标系（以第一帧为参考）下统一建模密集点图（point map）与三维场景流（scene flow），并设计一个4D VAE将两者编码为统一的潜在表示，从而有效迁移预训练视频扩散模型的时空先验，实现端到端的高质量几何与运动联合重建。

方法层面的关键创新包括：采用均值归一化（canonical normalization）替代传统的最大归一化，以更好地适配扩散模型的潜空间分布；对VAE进行全微调而非仅微调解码器，放松对扩散模型RGB潜空间的严格对齐约束；在U-Net阶段采用几何与运动潜码的通道拼接融合策略，而非分离建模。

实验结果表明，在无需任何后优化的情况下，MotionCrafter在几何重建上平均相对提升 **38.64%**，在运动估计上平均相对提升 **25.0%**，在多个基准数据集上显著超越现有方法（如 **VGGT**、**MonST3R**、**Geo4D**、**Zero-MSF**、**ST4RTrack** 等）。消融研究进一步验证了均值归一化与全VAE微调策略对户外场景重建质量的决定性作用，以及确定性训练范式相比扩散范式在几何精度上的显著优势。



### 从稀疏重建到密集4D理解

从单目视频中恢复三维场景结构与运动，是计算机视觉长期以来的核心目标。传统方法集中在稀疏重建（如SfM与SLAM）或单帧深度估计，但这两类任务都只触及了完整场景理解的局部：前者仅输出稀疏点云与相机位姿，后者缺乏对跨帧运动与几何一致性的显式建模。近年来，随着大规模预训练视频扩散模型的出现，从视频中直接预测密集几何与运动成为可能，但现有方法仍存在两个根本性瓶颈。

### 现有方法的两个关键缺口

**分离式建模导致长序列不一致。** 当前主流方法通常将几何重建与运动估计作为独立任务处理：先用深度或点图模型估计每帧几何，再通过光流或场景流模型估计帧间运动，最后依赖后优化（如全局BA）对齐跨帧预测。这种分离范式不仅计算效率低，更致命的是，由于几何与运动在建模阶段缺乏联合约束，长序列中误差会逐步累积，导致运动漂移与几何塌缩。即便是一些尝试联合建模的工作（如**Zero-MSF**、**DELTA**、**ST4RTrack**），也大多在相机坐标系下成对预测，缺乏世界坐标系下的统一表示，难以保证全局一致性。

**对扩散潜空间的严格对齐约束损害泛化能力。** 利用预训练视频扩散模型（如Stable Video Diffusion, SVD）的时空先验是当前的主流思路。然而，现有方法通常要求新任务的潜空间分布与原始扩散模型的RGB潜空间严格对齐，这严重限制了VAE的表达能力与泛化性能。当面对与预训练数据分布差异较大的场景（如户外大深度变化场景）时，这种刚性约束会导致重建质量急剧下降。

### 本文动机：统一4D表示与松弛训练策略

针对上述缺口，MotionCrafter提出两个核心动机：

1. **在世界坐标系下联合建模密集几何与运动。** 通过定义统一的4D表示——每帧的世界坐标点图（point map）与相邻帧的场景流（scene flow）——将几何重建与运动估计融合为单一任务，从根本上消除分离式建模带来的不一致性问题。这一表示天然支持端到端预测，无需任何后优化步骤。

2. **放松对扩散潜空间的分布对齐约束。** 通过均值归一化（canonical normalization）与全VAE微调策略，允许4D潜空间偏离原始SVD潜空间的分布，从而更充分地释放预训练视频扩散模型的时空先验，同时保持对新场景的泛化能力。

这两个动机共同指向一个目标：在保持预训练先验优势的前提下，实现真正端到端的、无需后优化的高质量几何与运动联合重建。



## 核心方法与创新机理

MotionCrafter 的核心创新在于将**密集几何重建与运动估计统一到世界坐标系下的4D潜空间**中，并通过**放松对扩散模型RGB潜空间的对齐约束**，有效迁移预训练视频扩散模型的时空先验。以下从五个关键维度剖析其相对于 baseline 的方法论突破。

### 1. 世界坐标系下的统一4D表示

现有方法通常将几何重建与运动估计分离处理，或仅在相机坐标系下进行成对预测，缺乏全局一致的统一表示。MotionCrafter 将第一帧的相机坐标系定义为世界坐标系，同时预测每一帧在该坐标系下的**密集点图** $X_i$ 以及相邻帧间的**场景流** $V_i$，形成统一的4D几何-运动表示：

$$f _ { \theta } : \{ I _ { i } \} _ { i = 1 } ^ { N } \mapsto \{ X _ { i } , V _ { i \rightarrow i+1 } \} _ { i = 1 } ^ { N }$$

这一设计的核心约束是变形一致性：变形后的点图 $X_i^d = X_i + V_i$ 在空间上应与下一帧的点图 $X_{i+1}$ 对齐。如 Figure 3 所示，由于像素索引在帧间不匹配且存在遮挡，无法建立像素级的一一对应，但该约束在3D空间层面为网络提供了强几何监督信号。

**相对于 baseline 的改变**：此前的联合方法（如 **POMATO**、**ST4RTrack**）或仅在相机坐标系下成对预测，或依赖后优化对齐跨帧结果；**VGGT**、**Geo4D** 等方法虽输出世界坐标点图，但未同时建模密集场景流。MotionCrafter 首次在单一框架内实现世界坐标系下点图与场景流的端到端联合预测，无需任何后优化步骤。

### 2. 均值归一化：释放扩散先验的关键设计

点图的数值分布直接影响VAE的训练稳定性和扩散U-Net的预测质量。传统方法采用**最大归一化**（Max normalization）将点图线性映射到 $[-1, 1]$，但这一策略对深度变化剧烈的户外场景极不友好——少数远距离点会压缩大部分场景的数值动态范围。

MotionCrafter 提出**均值归一化**（Canonical normalization）：

$$\hat{X}_i = \frac{X_i - \mu}{S}$$

其中 $\mu$ 为所有可见点的均值中心，$S$ 为各点到中心的平均距离。这一设计使归一化后的点图分布更接近标准正态分布，与预训练视频扩散模型（SVD）的潜空间统计特性自然兼容。

**决定性证据**：Figure 4 和 Table 3 的消融实验表明，均值归一化配合全VAE微调，在户外场景的重建质量上远超最大归一化方案。原始VAE在深度变化大的场景中几乎无法恢复场景结构，即使微调解码器也改善有限；而均值归一化策略使VAE成功重建出合理的几何结构。

### 3. 全VAE微调：放松潜空间对齐约束

预训练视频扩散模型的VAE是为RGB图像设计的，其潜空间分布与4D几何-运动表示存在本质差异。传统迁移策略通常**冻结编码器**或**仅微调解码器**，试图保持与原始潜空间的对齐。

MotionCrafter 采取相反策略：**微调整个VAE（编码器与解码器）**，明确放弃对SVD RGB潜空间的严格对齐。其核心洞察是：只要4D潜码在通道维度上与视频条件潜码拼接后能被U-Net有效处理，严格的分布对齐并非必要。这一放松策略使VAE能够学习更适合几何-运动表示的潜空间，同时U-Net也能自适应地利用预训练先验。

**决定性证据**：Table 3 显示，全微调VAE + 均值归一化的组合在VAE重建和U-Net最终预测两个层面均取得最优结果。这一发现挑战了“迁移扩散模型必须保持潜空间对齐”的普遍假设。

### 4. 统一几何-运动融合策略

在4D VAE的设计中，几何（点图）与运动（场景流）的融合方式存在多种选择。MotionCrafter 对比了三种策略：**分离VAE**（Geometry VAE和Motion VAE独立编码解码）、**后期融合**（分别编码后在潜空间融合）、**统一融合**（联合编码为统一潜表示）。

实验发现一个反直觉现象：统一融合策略在VAE阶段的重建指标并非最优，但在下游**扩散U-Net的预测中表现显著优于分离方案**（Table 4）。这表明统一潜空间为U-Net提供了更丰富的跨模态交互信息，使其能更好地利用视频扩散模型的时空建模能力进行联合推理。

### 5. 确定性训练范式替代扩散范式

传统视频扩散模型采用**加噪-去噪**的训练范式，但MotionCrafter在实验中发现，对于密集几何与运动预测任务，**确定性训练**（直接预测潜码）在几何重建上平均提升约12.4%的RelP指标，δP提升约12.7%（Table 7）。

确定性训练的总损失为：

$$\mathcal{L}_{\mathrm{deterministic}} = \mathcal{L}_{\mathrm{latent}} + \lambda_G \mathcal{L}_G + \lambda_M \mathcal{L}_{\mathrm{M}}$$

其中 $\mathcal{L}_{\mathrm{latent}}$ 对几何和运动潜码施加MSE监督，$\mathcal{L}_G$ 和 $\mathcal{L}_M$ 分别为几何VAE和运动VAE的重建损失。这一范式避免了扩散过程中的随机性，使网络能够更稳定地学习从视频条件到4D表示的确定性映射。

**方法论意义**：这提出了一个开放问题——确定性训练范式是否在所有密集预测任务中均优于扩散范式？MotionCrafter的实践表明，当输出空间具有明确的几何约束时，直接回归可能比迭代去噪更有效。



MotionCrafter 的整体设计围绕一个核心目标展开：从单目视频序列中端到端地联合重建世界坐标系下的密集几何（点图）与密集运动（场景流）。其 pipeline 可概括为“4D VAE 编码-扩散 U-Net 预测-4D VAE 解码”的三阶段结构，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/002_Figure_2.jpg]]
*Figure 2: Overview of MotionCrafter. We first train a novel 4D VAE (bottom-right), consisting of a Geometry VAE and a Motion VAE. These two components jointly encode the point map and scene flow into a unified 4D latent representation. Within the Diffusion Unet, we leverage the pretrained VAE from SVD (Stable Video Diffusion) to encode video latents as conditional inputs, which are then channel-wise concatenated with our 4D latent to guide the denoising process. We only add noise to the 4D latents during model training for the Diffusion version. Note that we do not enforce the 4D latent distribution to strictly align with the original SVD VAE latent distribution. And we find that this relaxed trainin...*

**输入与输出定义。** 给定一段包含 $N$ 帧的单目视频 $\{I_i\}_{i=1}^N$，网络 $f_\theta$ 直接输出每一帧在世界坐标系（以第一帧为参考）下的密集点图 $X_i$ 以及相邻帧之间的场景流 $V_{i,i+1}$：

$$f_{\theta} : \{I_i\}_{i=1}^N \mapsto \{X_i, V_{i,i+1}\}_{i=1}^N$$

其中变形后的点图 $X_i^d = X_i + V_i$ 在空间上应与下一帧的点图 $X_{i+1}$ 对齐（Figure 3），但由于像素索引变化和遮挡，二者之间无法建立一一对应关系。这一约束作为隐式正则项融入训练过程。

**模块化流水线。** 整个框架由四个核心模块串联而成：

1. **Video VAE Encoder**：利用预训练 Stable Video Diffusion (SVD) 的 VAE 编码器，将输入视频帧 $\{I_i\}$ 压缩为条件潜码，作为扩散 U-Net 的时空条件输入。

2. **4D VAE（Geometry VAE + Motion VAE）**：这是本文的核心创新模块。Geometry VAE 将各帧的世界坐标点图 $\{X_i\}$ 编码为几何潜码 $\{z_i^G\}$，Motion VAE 将场景流 $\{V_i\}$ 编码为运动潜码 $\{z_i^M\}$。二者在潜空间中以通道拼接的方式融合为统一的 4D 潜表示，同时送入扩散 U-Net 进行联合去噪预测。值得注意的是，本文不强制 4D 潜分布与原始 SVD VAE 的 RGB 潜分布严格对齐——这种“放松”的训练策略被证明能持续提升 VAE 和 U-Net 的泛化性能（Table 3）。

3. **Diffusion U-Net**：接收来自 Video VAE Encoder 的视频条件潜码和带噪的 4D 潜码，以确定性范式（直接预测潜码，而非逐步去噪）输出去噪后的 4D 潜码。实验表明，确定性训练范式在几何重建上 RelP 平均降低约 12.4%，δP 提升约 12.7%，优于扩散范式（Table 7）。

4. **4D VAE Decoder**：从 U-Net 预测的 4D 潜码中解码出最终的密集点图和场景流。

**关键设计决策的两条因果链。** 从 bottleneck 到性能提升，存在两条清晰的因果通路：

- **归一化与 VAE 微调策略**：现有方法多采用最大归一化（max normalization）将点图映射到 $[-1,1]$ 并冻结预训练 VAE，这在深度变化剧烈的户外场景中会导致严重的结构坍塌（Figure 4 第二行）。MotionCrafter 改用均值归一化（canonical normalization）——对每帧点图减去均值 $\mu$ 再除以平均距离尺度 $S$（$\hat{X}_i = \frac{X_i - \mu}{S}$，Eq.3），并全微调整个 VAE（编码器+解码器）。这一组合使户外场景的重建质量得到质的提升。

- **统一几何-运动融合**：与分离建模或仅预测目标时间点图的方案不同，MotionCrafter 在潜空间中将几何与运动潜码统一融合后送入 U-Net 联合预测。尽管这种融合策略在 VAE 阶段的重建指标略低于分离方案，但在下游 U-Net 预测中表现最优（Table 4），说明统一的 4D 潜表示更有利于扩散 U-Net 利用视频先验进行时空一致性推理。

**训练范式与损失函数。** 默认采用确定性训练，总损失为：

$$\mathcal{L}_{\text{deterministic}} = \mathcal{L}_{\text{latent}} + \lambda_G \mathcal{L}_G + \lambda_M \mathcal{L}_M$$

其中 $\mathcal{L}_{\text{latent}}$ 对几何和运动潜码施加 MSE 监督（Eq.7），$\mathcal{L}_G$ 联合点图 MSE、多尺度深度损失和法向一致性损失（Eq.4），$\mathcal{L}_M$ 包含场景流重建 MSE 和零流正则项（Eq.5）。解码器损失（decoder loss）在四个未见数据集上带来平均 15.01% 的提升（Table 6），多模态深度监督使世界坐标点图重建质量平均提升 13.55%（Table 5）。

**与基线方法的根本差异。** 相较于 POMATO、ST4RTrack、DELTA、Zero-MSF 等联合几何-运动估计方法，以及 VGGT、Geo4D、MonST3R 等纯几何重建方法，MotionCrafter 的核心区分点在于：(1) 在世界坐标系而非相机坐标系下统一建模；(2) 无需任何后优化（如 Geo4D 的全局对齐），所有结果由模型直接端到端输出；(3) 通过放松对扩散模型 RGB 潜空间的对齐约束，有效迁移了视频扩散模型的时空先验，在训练规模远小于 VGGT 的情况下仍展现出对动态场景的良好鲁棒性（Figure 10）。



MotionCrafter 的核心架构围绕一个统一的 4D 世界坐标表示展开，由三个关键模块构成：几何 VAE、运动 VAE 和基于预训练视频扩散模型的 U-Net 预测器。其设计目标是将密集几何重建与运动估计联合建模，而非分离处理。

### 统一 4D 表示与坐标系定义

网络映射函数定义为：

$$f _ { \theta } : \{ I _ { i } \} _ { i = 1 } ^ { N } \mapsto \{ X _ { i } , V _ { i \to i + 1 } \} _ { i = 1 } ^ { N }$$

其中 $I_i$ 为输入单目视频的第 $i$ 帧，$X_i$ 为第 $i$ 帧在世界坐标系（以第一帧为参考）下的密集点图，$V_{i \to i+1}$ 为从第 $i$ 帧到第 $i+1$ 帧的三维场景流。

该表示的核心约束在于变形一致性：变形后的点图 $X_i^d = X_i + V_i$ 应在空间上与下一帧点图 $X_{i+1}$ 对齐。然而，由于像素索引在帧间并不对应（$p_i$ 与 $p_{i+1}$ 可能指向不同物体，甚至 $p_{i+1}$ 已移出视野），无法建立逐像素的一一对应关系。这一约束通过后续损失函数隐式引导，而非强制逐像素匹配。

### 点图归一化策略

为适配预训练视频扩散模型的潜空间分布，MotionCrafter 采用均值归一化（Canonical Normalization），而非传统的最大归一化：

$$\hat{X}_i = \frac{X_i - \mu}{S}$$

其中 $\mu$ 为所有可见点的均值中心，$S$ 为所有点到中心的平均距离。这一设计的因果逻辑在于：最大归一化对深度范围极度敏感，户外场景的深度跨度巨大，导致归一化后的值域不稳定，阻碍 VAE 和扩散 U-Net 的有效训练。均值归一化则通过中心化和尺度归一化将点图映射到更稳定的分布，显著提升户外场景的重建质量。

### 几何 VAE 与多模态监督

几何 VAE 负责将世界坐标系下的点图编码为潜在表示并重建。其训练损失为三项联合监督：

$$\mathcal{L}_G = \mathcal{L}_{\mathrm{point}} + \lambda_d \mathcal{L}_{\mathrm{depth}} + \lambda_n \mathcal{L}_{\mathrm{normal}}$$

- $\mathcal{L}_{\mathrm{point}}$：点图重建的 MSE 损失。
- $\mathcal{L}_{\mathrm{depth}}$：投影深度图上的多尺度损失，提供二维几何约束。
- $\mathcal{L}_{\mathrm{normal}}$：法向一致性损失，增强局部表面几何的合理性。

多模态深度监督的消融实验表明，该设计使世界坐标点图重建质量平均提升 13.55%，验证了二维投影约束对三维几何学习的补充作用。

### 运动 VAE 与零流正则

运动 VAE 编码场景流并与几何潜码融合，形成统一的 4D 潜在表示。其损失函数为：

$$\mathcal{L}_{\mathrm{M}} = \frac{1}{|\mathcal{D}|} \sum_{d\in\mathcal{D}} \|\hat{V}_d - V_d\|_2^2 + \lambda_{\mathrm{reg}} \frac{1}{|\mathcal{N}|} \sum_{n\in\mathcal{N}} \|\hat{V}_n\|_2^2$$

- 第一项为场景流在动态区域 $\mathcal{D}$ 上的重建 MSE。
- 第二项为零流正则项，约束静态区域 $\mathcal{N}$ 的预测流趋于零，防止模型在无运动区域产生虚假流动。

### 确定性训练范式与潜空间监督

MotionCrafter 默认采用确定性训练范式，直接预测潜码而非通过加噪-去噪过程。总损失为：

$$\mathcal{L}_{\mathrm{deterministic}} = \mathcal{L}_{\mathrm{latent}} + \lambda_G \mathcal{L}_G + \lambda_M \mathcal{L}_{\mathrm{M}}$$

其中潜在监督损失 $\mathcal{L}_{\mathrm{latent}}$ 对几何和运动潜码分别施加 MSE 约束：

$$\mathcal{L}_{\mathrm{latent}} = \frac{1}{N} \sum_{N} \|\hat{\mathbf{z}}_i^{\mathrm{G}} - \mathbf{z}_i^{\mathrm{G}}\|_2^2 + \frac{1}{N-1} \sum_{N-1} \|\hat{\mathbf{z}}_i^{\mathrm{M}} - \mathbf{z}_i^{\mathrm{M}}\|_2^2$$

这里 $\mathbf{z}_i^{\mathrm{G}}$ 和 $\mathbf{z}_i^{\mathrm{M}}$ 分别为几何 VAE 和运动 VAE 编码得到的真实潜码，$\hat{\mathbf{z}}_i^{\mathrm{G}}$ 和 $\hat{\mathbf{z}}_i^{\mathrm{M}}$ 为 U-Net 的预测值。消融实验表明，确定性范式相比扩散范式在几何重建上 RelP 降低约 12.4%，$\delta$P 提升约 12.7%，因此被选为默认训练策略。

### 关键设计决策：放松潜空间对齐约束

MotionCrafter 的一个重要设计选择是不强制 4D 潜在分布与预训练 SVD VAE 的潜空间严格对齐。这一放松策略使 VAE 和扩散 U-Net 的泛化性能均得到持续改善。其因果机制在于：预训练视频扩散模型的潜空间是针对 RGB 视频帧优化的，强制对齐会限制几何和运动表示的灵活性；放松约束后，模型可以学习更适合密集几何-运动联合建模的潜在结构。

### 补充图表

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/003_Figure_3.jpg]]
*Figure 3: Geometry and Motion representation. For a pixel*

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/004_Figure_4.jpg]]
*Figure 4: Results of different normalization and VAE training strategies. For outdoor scenes with significant variations in depth (the second row), the original VAE fails to recover the scene structure. Even with decoder fine-tuning, the reconstruction quality remains poor. Our proposed mean normalization and VAE training strategy significantly improve reconstruction quality*



## 实验与关键发现

### 核心实验设置

MotionCrafter 以**确定性训练范式**作为默认配置（详见 3.3 节），VAE 与 U-Net 均采用 **SVD（Stable Video Diffusion）预训练权重**初始化。训练数据涵盖多个合成与真实场景数据集（Table 8），其中几何训练以随机步长采样视频帧，运动训练则固定步长为 1 以保持帧间连续性。所有对比方法均使用相同的世界坐标对齐流程（VGGT 相机姿态），且 MotionCrafter **不使用任何后优化**，确保公平性。

### 联合几何与运动重建主结果

Table 1 报告了在 Kubric 数据集上世界坐标系联合几何与运动重建的定量结果。MotionCrafter 在几何指标 RelP↓ 上达到 **3.40**，相比 Zero-MSF + VGGT 的 8.79 降低 **5.39**；在运动指标 EPE↓ 上达到 **3.40**，相比 ST4RTrack-S + VGGT 的 59.34 降低 **55.94**。综合多个基准，论文报告几何重建平均相对改进 **38.64%**，运动估计平均相对改进 **25.0%**（Abstract）。

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/005_Table_1.jpg]]
*Table 1: Evaluation on joint world-centric geometry and motion reconstruction. All metrics are reported without percentage symbols for readability. * denotes not zero-shot scene flow evaluation. -S and -P denote the Sequence mode and Pair mode of ST4RTrack. Since ST4RTrack always compares with the first frame for motion, for a fair comparison, we run it on every pair of consecutive frames and then transform the results into the world coordinate system using VGGT poses. Plus, we add Zero-MSF + GT pose as a reference*

Table 2 进一步展示了世界坐标系几何重建的对比。在 Monkaa 数据集上，MotionCrafter 的 RelP↓ 为 **25.88**，显著优于 VGGT 的 56.42（降低 **30.54**），且优于使用后优化的 Geo4D† 等方法。值得注意的是，MotionCrafter 在**不使用任何后优化**的情况下达到这些结果，而 Geo4D 等方法依赖后优化步骤。

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/007_Table_2.jpg]]
*Table 2: Evaluation on world-centric geometric reconstruction. †denotes using post-optimization. Note that, our results are reported without any post-optimization*

**定性分析**（Figure 5, Figure 6, Figure 9, Figure 10）揭示了方法的优势来源：
- 相比 Zero-MSF，MotionCrafter 重建的场景结构更合理，几何细节更丰富，且预测的 3D 场景流方向更准确（Figure 5, Figure 9）。
- 相比 ST4RTrack，MotionCrafter 的场景流更清洁，无噪声漂移；变形点图（deformed point map）显示其时序一致性更好（Figure 6）。
- 对于动态物体（如手指），MotionCrafter 估计的尺度和运动变化更准确；对于室外场景，场景结构估计更精确（Figure 10）。

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison with Zero-MSF [54]. Zoom in for the details. Compared to Zero-MSF, we have a more reasonable scene structure and better geometric details. More importantly, our predicted 3D scene flow has a more accurate direction of motion*

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison with ST4RTrack [14]. In the first case, the pixel trajectory shows that we yield cleaner scene flow, while ST4RTrack suffers from noisy drift. In the second case, the deformed point map (with darker color) shows that our method predicts more temporally consistent geometry and motion*

### 消融研究

#### 1. 点图归一化与 VAE 训练策略（Table 3, Figure 4）

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/010_Table_3.jpg]]
*Table 3: Ablation study on geometry VAE. Here, we report geometry reconstruction results on both VAE and U-Net, as a better VAE may not always lead to better final results. The models are trained on a subset only for geometry reconstruction*

**关键发现**：均值归一化（Canonical normalization）结合全 VAE 微调显著优于最大归一化方案，尤其在室外场景中差距更为明显。

Table 3 的消融显示，所提出的归一化与 VAE 训练策略**一致提升了 VAE 和下游扩散 U-Net 的性能**。Figure 4 直观展示了这一差距：对于深度变化显著的室外场景，原始 VAE 完全无法恢复场景结构，即使仅微调解码器，重建质量仍然很差；而均值归一化与全微调策略使重建质量大幅提升。

**机制分析**：最大归一化将点图缩放至 `[-1, 1]`，对深度范围极端的室外场景会严重压缩几何信息。均值归一化通过均值中心化和平均距离缩放（Eq.3），保留了场景的相对结构信息，更适配预训练视频扩散模型的潜空间分布。

#### 2. 几何-运动融合策略（Table 4）

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/009_Table_4.jpg]]
*Table 4: Ablation study on motion VAE. Comparison of different designs across three dynamic scene flow datasets. Again, we report results on both VAE and U-Net*

**关键发现**：统一的通道拼接融合策略在 U-Net 阶段表现最优，尽管在 VAE 阶段的重建指标并非最佳。

Table 4 比较了三种融合设计：分离 VAE、统一 VAE（通道拼接）、统一 VAE（加法融合）。结果表明，通道拼接策略在 VAE 重建指标上略低于分离 VAE，但在下游扩散 U-Net 中取得了**显著更优的性能**。这说明 VAE 阶段的最优重建不等于下游任务的最优表示——通道拼接为 U-Net 提供了更丰富的联合特征交互空间。

#### 3. 多模态深度监督（Table 5）

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/011_Table_5.jpg]]
*Table 5: Ablation study on Geometry VAE components. Metrics are reported for ScanNet, Sintel, and Monkaa datasets: point accuracy (Relp ↓, δp ↑) and depth accuracy*

**关键发现**：多模态深度监督使世界坐标点图重建质量平均提升 **13.55%**。

Table 5 消融了 Geometry VAE 的各组件。在 ScanNet、Sintel、Monkaa 三个数据集上，加入多尺度深度损失和法向一致性损失后，点精度（RelP↓, δP↑）和深度精度均获显著提升。这验证了 Eq.4 中联合损失设计的有效性。

#### 4. 解码器损失（Table 6）

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/012_Table_6.jpg]]
*Table 6: Ablation study on Unet components for Geometry Reconstruction. We compare models trained with different strategies, rescaling methods, and decoder losses*

**关键发现**：解码器损失在四个未见数据集上带来平均 **15.01%** 的提升。

Table 6 消融了 U-Net 组件的不同训练策略、重缩放方法和解码器损失。加入解码器端到端损失后，模型在未见场景上的泛化能力大幅增强，说明直接监督解码输出有助于约束潜空间学习。

#### 5. 训练范式：确定性 vs 扩散（Table 7）

![[assets/figures/papers/paper_list_l968_https_arxiv_org_abs_2602_08961/figures/014_Table_7.jpg]]
*Table 7: Ablation on different training paradigm*

**关键发现**：确定性训练范式在几何重建上 RelP 平均降低约 **12.4%**，δP 平均提升约 **12.7%**。

Table 7 直接比较了两种范式。确定性训练直接预测潜码（Eq.6），而扩散范式对潜码加噪后去噪。实验表明确定性范式在所有几何指标上均优于扩散范式，论文因此将其设为默认配置。这一发现与直觉相反——扩散模型通常被认为具有更强的生成能力，但在密集预测任务中，确定性训练可能避免了去噪过程中的信息损失。

### 零样本泛化

Figure 8 展示了在 Davis 数据集上的零样本结果。尽管场景流估计的训练样本非常有限，MotionCrafter 在不同场景类型上均展现出良好的泛化能力。这归因于端到端的模型设计和世界坐标系下几何与运动的统一定义，所有结果均由模型直接输出，无需后优化。

### 失败模式与局限

1. **单模态输入限制**：当前方法仅利用单目视频输入，未整合相机参数、深度图等多模态几何线索。在极端几何歧义场景下，这可能限制重建精度。
2. **合成数据依赖**：场景流估计的训练依赖合成数据集（如 Kubric），在真实世界复杂动态场景（如非刚性形变、透明物体）上的泛化能力尚待验证。
3. **长期一致性**：虽然世界坐标系设计缓解了帧间不一致问题，但在长序列遮挡和快速运动场景下，点图和场景流的长期一致性仍可能退化。

### 关键图表索引

- **Table 1**：联合世界坐标系几何与运动重建主结果（Kubric 数据集）
- **Table 2**：世界坐标系几何重建对比（含 Monkaa 等数据集）
- **Table 3**：几何 VAE 消融——归一化与训练策略
- **Table 4**：运动 VAE 消融——融合策略设计
- **Table 5**：几何 VAE 组件消融——多模态监督
- **Table 6**：U-Net 组件消融——解码器损失与重缩放
- **Table 7**：训练范式消融——确定性 vs 扩散
- **Table 8**：训练数据集概览
- **Figure 4**：不同归一化与 VAE 训练策略的定性对比
- **Figure 5**：与 Zero-MSF 的定性比较
- **Figure 6**：与 ST4RTrack 的定性比较
- **Figure 8**：Davis 数据集零样本结果
- **Figure 9**：与 Zero-MSF 和 DELTA 的定性比较
- **Figure 10**：与 VGGT、Geo4D、ST4RTrack 的定性几何比较



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

单目视频的密集几何重建与运动估计长期面临一个结构性矛盾：**几何与运动的分离建模**。现有方法通常将两者视为独立任务——几何重建依赖多视图立体匹配或单目深度估计，运动估计则依赖光流或点轨迹追踪——导致在长序列中缺乏全局一致性，且需要复杂的后优化步骤（如全局BA或点云对齐）来融合跨帧预测。这一分离范式的根本瓶颈在于**缺乏世界坐标系下的统一表示**：相机坐标系下的成对预测无法直接传递时序约束，而逐帧独立估计的深度图或点云在尺度、位姿上天然不一致。

MotionCrafter 的切入点正是这一瓶颈：**在世界坐标系（第一帧）下联合定义密集点图与场景流**，将几何重建与运动估计统一为“同一场景在不同时刻的空间状态”建模问题，从而从表示层面消除了跨帧对齐的需求。

### 2. 在相关工作中的坐标定位

#### 2.1 与几何重建方法的对比

在几何重建维度，MotionCrafter 与以下方法构成直接对比：

- **VGGT**：基于Transformer的密集几何重建方法，可直接输出世界坐标点云，但主要针对静态场景设计，对动态物体的尺度与运动变化估计不够鲁棒。MotionCrafter 在训练规模远小于VGGT的情况下，在动态场景中表现出更好的鲁棒性（Figure 10），这归因于视频扩散模型的预训练先验。
- **Geo4D**：利用时序信息进行4D重建，但需要后优化步骤对齐跨帧预测。MotionCrafter 无需任何后优化即可直接输出世界坐标点云（Table 2）。
- **MonST3R**：基于成对帧的几何估计方法，在扩展到视频序列时性能退化明显。

在定量对比中，MotionCrafter 在 Monkaa 数据集上达到 RelP↓ 25.88，显著优于 VGGT 的 56.42（Table 2），在 Kubric 上达到 RelP↓ 3.40，优于 Zero-MSF+VGGT 组合的 8.79（Table 1）。

#### 2.2 与运动估计方法的对比

在运动估计维度，主要对比方法包括：

- **ST4RTrack**（Sequence/Pair模式）：基于点追踪的运动估计方法，始终以第一帧为参考进行成对比较。MotionCrafter 将其结果通过 VGGT 相机姿态转换到世界坐标系以进行公平对比，在 Kubric 上 EPE↓ 3.40 vs ST4RTrack-S+VGGT 的 59.34（Table 1）。定性结果显示，ST4RTrack 存在噪声漂移问题，而 MotionCrafter 的场景流更干净（Figure 6）。
- **Zero-MSF**：零样本场景流估计方法，在动态场景中表现出色。MotionCrafter 在未使用其训练数据（dynamic replica）的情况下，场景流估计精度与之可比，且在几何结构与运动方向上更优（Figure 5, Figure 9）。
- **DELTA**：联合几何与运动估计的方法，MotionCrafter 在几何结构与运动模式估计上均显著优于 DELTA（Figure 9）。
- **POMATO**：联合几何与运动估计的对比方法，在 Table 1 中作为基线之一。

#### 2.3 方法谱系中的独特位置

MotionCrafter 在方法谱系中的独特贡献可概括为三个层次：

**表示层创新**：从“相机坐标系下的成对预测”转向“世界坐标系下的统一4D表示”（点图 + 场景流），这一转变使几何与运动从两个独立任务变为同一空间状态的不同侧面。变形点图 $X_i^d = X_i + V_i$ 应与下一帧点图空间对齐的约束（Eq.2），天然桥接了几何一致性与运动连续性。

**架构层创新**：设计了4D VAE（Geometry VAE + Motion VAE），将点图与场景流联合编码至统一潜空间。与分离建模相比，统一融合策略在U-Net预测阶段表现更优，尽管VAE重建指标略低（Table 4）。这一“VAE阶段略差、U-Net阶段更优”的现象揭示了潜空间结构对下游扩散模型的重要性——更紧凑的联合表示可能更适配预训练视频扩散模型的先验分布。

**训练策略创新**：均值归一化（Eq.3）与全VAE微调的组合，放松了对扩散模型RGB潜空间的严格对齐约束。这一“放松约束反获泛化”的策略是方法成功的关键：通过不强制4D潜分布与SVD VAE潜分布严格对齐，模型获得了更大的表示灵活性，在户外深度变化剧烈的场景中表现尤为突出（Figure 4, Table 3）。

### 3. 适用边界与局限

**输入模态边界**：当前方法仅利用单目RGB视频作为输入，未整合相机内参、深度图、点轨迹等多模态几何线索。在极端视角变化或纹理稀疏区域，纯视觉信号可能不足以约束几何重建。

**训练数据依赖**：场景流估计的训练依赖合成数据集（Kubric、Monkaa等），真实世界复杂动态场景（如非刚性形变、透明物体运动、快速旋转）的泛化能力尚待系统验证。尽管在 Davis 数据集上展示了零样本泛化能力（Figure 8），但该数据集规模有限。

**长序列一致性**：虽然世界坐标表示消除了逐帧对齐需求，但长序列中的累积误差问题未明确讨论。第一帧世界坐标系的选择意味着远离第一帧的帧可能面临更大的重建不确定性。

**动态-静态权衡**：方法在动态场景中优于VGGT等静态方法，但在纯静态场景中是否保持同等精度，文中未提供充分对比。

### 4. 开放问题

1. **归一化策略的进一步优化**：均值归一化显著优于最大归一化，但是否存在更优的归一化策略（如自适应归一化、分区域归一化）能进一步释放扩散模型先验的潜力？

2. **多模态几何线索的融合路径**：如何有效地将相机内参、点轨迹、新视图合成等显式几何信息融入4D潜空间？是通过条件注入、特征拼接，还是设计专门的交叉注意力机制？

3. **确定性 vs 扩散范式的适用边界**：确定性训练范式在几何重建上平均提升约12.4% RelP（Table 7），但是否在所有密集预测任务中均优于扩散范式？在需要多模态输出的任务中，扩散范式的随机性可能具有独特价值。

4. **真实世界大规模动态场景的鲁棒性**：在自动驾驶、机器人操作等真实世界大规模动态场景下，如何提升世界坐标系点图和场景流的长期一致性与鲁棒性？是否需要引入闭环检测或全局优化机制？

5. **计算效率与实时性**：基于视频扩散模型的方法在推理速度上可能难以满足实时应用需求，是否存在轻量化路径（如蒸馏、一步生成）？

6. **与3D基础模型的整合**：MotionCrafter 的4D输出（点图+场景流）可作为3D基础模型（如3D Gaussian Splatting、NeRF）的初始化或约束，这一方向尚未探索。



## 原文 PDF

![[paperPDFs/CVPR_2026/MotionCrafter_Dense_Geometry_and_Motion_Reconstruction_with_a_4D_VAE.pdf]]
