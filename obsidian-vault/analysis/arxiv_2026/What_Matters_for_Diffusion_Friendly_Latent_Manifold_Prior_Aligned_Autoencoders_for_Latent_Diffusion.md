---
title: What Matters for Diffusion-Friendly Latent Manifold? Prior-Aligned Autoencoders for Latent Diffusion
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion.pdf
project_link: null
code_link: https://github.com/black-forest-labs/flux
aliases:
- PAAP
- WMDFLMPAALD
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过显式定义并正则化潜在流形的三个扩散友好属性——空间结构一致性（SSC）、局部流形连续性（LPC）和全局语义质量（GSQ）——可以显著提升扩散模型的训练效率和生成质量。
primary_logic: 一个扩散友好的潜在流形应同时具备连贯的空间结构、局部平滑性和良好的语义聚类，这些属性可以通过与视觉基础模型（VFM）先验对齐的正则化目标直接优化，而非依赖重建间接产生。
claims:
- 更好的重建质量（rFID）并不能保证更好的生成质量（gFID）。
- 实例级空间结构（SSC）、局部流形连续性（LPC）和全局语义质量（GSQ）的改善与生成质量呈正相关。
- PAE在80个训练轮次达到gFID 1.27，在800轮次达到新的SOTA gFID 1.03，同时收敛速度较RAE快13倍。
- 每个先验对齐目标（SSR、MCR、SCR）分别主要提升其对应的几何指标，组合三者可获得最佳生成性能。
---

# What Matters for Diffusion-Friendly Latent Manifold? Prior-Aligned Autoencoders for Latent Diffusion

> [!tip] 核心洞察
> 一个扩散友好的潜在流形应同时具备连贯的空间结构、局部平滑性和良好的语义聚类，这些属性可以通过与视觉基础模型（VFM）先验对齐的正则化目标直接优化，而非依赖重建间接产生。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散友好的潜在流形关键何在？面向潜在扩散的先验对齐自编码器 |
| 英文题名 | What Matters for Diffusion-Friendly Latent Manifold? Prior-Aligned Autoencoders for Latent Diffusion |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2605.07915) · [paper](https://arxiv.org/abs/2602.11401) · [Code](https://github.com/black-forest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Prior-Aligned AutoEncoder (PAE) |
| Dataset | ImageNet 256×256 class-conditional generation |

> [!tip] 效果简介
> - ImageNet 256×256 class-conditional generation (80 epochs) 上，gFID (with guidance)↓ 1.27 (PAE DINOv2) vs 1.44 (VTP), 1.48 (GAE) (↓0.17-0.21)。
> - ImageNet 256×256 class-conditional generation (800 epochs) 上，gFID (with guidance)↓ 1.03 (PAE DINOv2) vs 1.13 (RAE DiTDH-XL), 1.21 (Send-VAE w. REPA) (↓0.10-0.18)。

## 概要

### 问题背景

潜在扩散模型（Latent Diffusion Models, LDMs）已成为高分辨率图像生成的主流范式。其核心组件——标记器（tokenizer）——负责将图像压缩至低维潜在空间，扩散模型则在该空间中学习生成。然而，现有标记器的设计几乎完全围绕**重建保真度**展开：无论是以**VA-VAE**为代表的像素级重建导向方法，还是以**VTP**、**GAE**、**FAE**等为代表的视觉基础模型（VFM）特征继承方法，均未对潜在流形的几何属性进行显式组织。这导致一个关键瓶颈：**更好的重建质量并不保证更好的生成质量**（Figure 2(a)），扩散模型在缺乏良好组织的潜在空间中学习效率低下，生成质量受限。

### 核心洞察

本文通过先导实验（Figure 2(b-d)）揭示了**扩散友好的潜在流形应具备的三个基本属性**：

1. **空间结构一致性（Spatial Structure Coherence, SSC）**：实例级空间拓扑应得到保留；
2. **局部流形连续性（Local Manifold Continuity, LPC）**：潜在空间在局部邻域应平滑连续；
3. **全局语义质量（Global Semantic Quality, GSQ）**：潜在表示应形成良好的语义聚类。

这三个属性与生成质量（gFID）呈稳定正相关，而重建质量（rFID）与生成质量之间则无此关系。这一发现表明，**潜在流形的几何组织应作为标记器设计的显式目标**，而非依赖重建过程间接产生。

### 方法定位

基于上述洞察，本文提出**先验对齐自编码器（Prior-Aligned AutoEncoder, PAE）**。PAE 在方法谱系中占据独特位置：

- 不同于**重建导向**的标记器（如 VA-VAE）仅优化像素保真度；
- 不同于**表示导向**的标记器（如 VTP、GAE、FAE）直接继承 VFM 特征而缺乏流形塑造；
- 也不同于**表示对齐**方法（如 AlignTok）或**表示引导的扩散主干**（如 REPA）仅在扩散训练阶段施加约束。

PAE 的核心理念是：**利用精炼的 VFM 先验，将 SSC、LPC 和 GSQ 转化为标记器训练阶段的显式正则化目标**，直接塑造潜在流形的几何属性。具体而言，PAE 通过三个技术槽位实现这一目标：

| 设计槽位 | 基线做法 | PAE 做法 |
|---------|---------|---------|
| 编码器架构 | 标准 VAE 编码器或直接使用 VFM 特征 | 冻结 VFM 编码器 + 细节感知调制器（DAM），通过零初始化尺度位移注入像素细节，保持 VFM 语义主导 |
| 潜在空间正则化 | 仅像素级重建损失 + 可选 KL 散度 | 加入三个先验对齐目标：空间结构正则化（SSR）、流形连续性正则化（MCR）、语义一致性正则化（SCR） |
| 先验目标精炼 | 直接使用原始 VFM 特征 | 通过轻量级投影器压缩，并经过空间上采样与低通归一化精炼，获得瓶颈匹配的语义目标与空间干净的结构目标 |

### 主要结果

在 ImageNet 256×256 类别条件生成任务上，PAE 在相同训练配置下展现出显著的效率与质量优势（Table 1）：

- **收敛效率**：PAE 在 80 个训练轮次即达到 gFID 1.27，收敛速度较 RAE 快约 **13 倍**；
- **最终性能**：在 800 轮次达到 **gFID 1.03** 的新 SOTA，超越 RAE DiTDH-XL（1.13）和 Send-VAE w. REPA（1.21）；
- **重建能力**：PAE 同时保持竞争力的重建质量（rFID 0.26），在保真度-可学习性权衡曲线上占据明显优势（Figure 6(a)）。

消融实验（Table 2）证实，SSR、MCR 和 SCR 三个正则化目标各自主要提升其对应的几何指标（SSC、LPC、GSQ），组合三者可获得最佳生成性能，验证了流形组织作为显式设计目标的有效性。



### 潜在扩散模型的范式与瓶颈

潜在扩散模型（Latent Diffusion Models, LDMs）已成为高分辨率视觉生成的主流范式。其核心思路是将图像压缩到一个低维潜在空间，在该空间内训练扩散模型，再通过解码器重建回像素空间。这一范式将生成任务解耦为两个阶段：**标记器（tokenizer）** 负责图像-潜在空间的映射，**扩散生成器** 负责在潜在空间内建模数据分布。

然而，现有标记器的设计几乎完全聚焦于**重建保真度**——即压缩后的潜在码能否通过解码器精确还原原始图像。衡量这一能力的典型指标是 rFID（reconstruction Fréchet Inception Distance）。一个被广泛默认的假设是：更好的重建质量自然会带来更好的生成质量。但先导实验（Figure 2(a)）直接挑战了这一假设：**更好的 rFID 并不能保证更好的 gFID（generation FID）**。这意味着，一个对重建友好的潜在空间，未必对扩散模型的学习友好。

### 潜在流形的“扩散友好性”缺口

问题的根源在于，潜在空间不仅是图像的信息容器，更是一个**几何流形**——扩散模型需要在这个流形上学习从噪声到数据的复杂映射。现有标记器大致可分为两类：

- **重建导向型**（如 VAE、VQGAN 及其变体）：以像素级重建损失（L1 + LPIPS + GAN）为核心目标，潜在流形的几何属性完全由重建任务间接决定，缺乏显式组织。
- **表示导向型**（如 VTP、GAE、FAE、AlignTok）：直接使用或对齐预训练视觉基础模型（VFM）的特征作为潜在表示，虽然继承了 VFM 的语义结构，但流形的局部平滑性和空间结构一致性并未被显式优化。

这两类方法都回避了一个关键问题：**什么样的潜在流形几何属性对扩散模型是友好的？** 论文通过系统的先导实验（Figure 2(b-d)）识别出三个与生成质量正相关的流形属性：

1. **空间结构一致性（Spatial Structure Consistency, SSC）**：实例级别的空间拓扑是否在潜在空间中得以保持。该属性通过潜在码与 VFM 特征的 Gram 矩阵相似度衡量。
2. **局部流形连续性（Local Manifold Continuity, LPC）**：潜在空间中邻近点对应的解码图像是否语义一致。该属性通过在潜在码上施加扰动后解码图像的 LPIPS 距离衡量。
3. **全局语义质量（Global Semantic Quality, GSQ）**：潜在码是否形成良好的语义聚类。该属性通过全局池化后的潜在码与 VFM 语义特征的余弦相似度衡量。

实验表明，这三个指标的改善与 gFID 的下降呈一致的正相关趋势，而 rFID 的改善则没有这种一致性。这构成了本文的核心动机：**与其让扩散友好的流形属性从重建任务中被动涌现，不如将其作为显式的优化目标。**

### 本文的核心主张

基于上述观察，论文提出 **先验对齐自编码器（Prior-Aligned AutoEncoder, PAE）**，核心主张是：通过将 VFM 的表示先验精炼为显式的正则化目标，可以直接塑造潜在流形的空间结构、局部连续性和全局语义组织，从而构建一个**扩散友好的潜在流形**。

PAE 的设计围绕三个关键改变展开：

- **编码器架构**：冻结 VFM 编码器作为语义骨干，通过细节感知调制器（DAM）以零初始化的尺度-位移融合注入像素细节，保持 VFM 的语义主导地位。
- **先验目标精炼**：对原始 VFM 特征进行空间上采样与低通归一化获得干净的结构目标，通过瓶颈投影获得语义目标，使对齐目标与潜在空间分辨率匹配。
- **显式流形正则化**：引入三个先验对齐损失——空间结构正则化（SSR）、流形连续性正则化（MCR）和语义一致性正则化（SCR），分别对应 SSC、LPC 和 GSQ 三个扩散友好属性。

这一设计将潜在流形的组织从“重建的副产品”提升为“训练的一等公民”，在保持竞争性重建质量（rFID 0.26）的同时，显著提升了扩散模型的训练效率和生成质量：在 ImageNet 256×256 上，PAE 仅需 80 个训练轮次即达到 gFID 1.27，在 800 轮次达到新的 SOTA gFID 1.03，收敛速度较 RAE 快约 13 倍（Table 1）。



## 核心方法与创新机理

### 瓶颈发现：重建质量不等于扩散友好

现有潜在扩散标记器（tokenizer）的设计目标几乎完全围绕像素级重建保真度展开——无论是**VA-VAE**、**VTP**、**GAE**等重建导向或表示导向的方法，还是直接继承预训练特征的**RAE**、**AlignTok**等，其核心优化信号始终是 $L_1$、LPIPS 和 GAN 损失的组合。这些方法隐含地假设：更好的重建质量自然意味着更利于扩散模型学习的潜在空间。

先导实验（Figure 2）直接证伪了这一假设。**Figure 2(a)** 显示，重建质量（rFID）与下游生成质量（gFID）之间不存在单调正相关关系——更好的重建并不能保证更好的生成。相反，**Figure 2(b-d)** 揭示了三个与生成质量强正相关的潜在流形几何属性：

- **空间结构一致性（SSC）**：潜在码的实例级空间拓扑与视觉语义结构的一致程度
- **局部流形连续性（LPC）**：潜在流形在局部邻域内的平滑程度
- **全局语义质量（GSQ）**：潜在码在全局嵌入空间中的语义聚类质量

这一发现表明，**扩散友好的潜在流形需要被显式塑造，而非依赖重建目标间接涌现**。

### 核心创新：先验对齐的三维流形正则化

PAE 的核心创新在于将上述三个几何属性转化为可优化的训练目标，通过视觉基础模型（VFM）的先验知识来显式组织潜在流形。具体而言，PAE 引入了三个先验对齐正则化项，分别对应一个扩散友好属性：

**空间结构正则化（SSR）** 对齐潜在码与 VFM 目标特征的空间格拉姆矩阵：

$$\mathcal{L}_{\text{SSR}} = \| \mathbf{G}_z - \mathbf{G}_T \|_F^2$$

通过约束特征图各空间位置之间的内积关系，SSR 保持实例级的拓扑结构，使潜在码忠实地反映图像的语义布局。

**流形连续性正则化（MCR）** 采用级联扰动一致性设计，逐步正则化局部邻域：

$$\mathcal{L}_{\text{MCR}} = \underbrace{ \| \hat{x}_m - \text{sg}(\hat{x}_r) \|_1 + \text{LPIPS}(\hat{x}_m, \text{sg}(\hat{x}_r)) }_{\text{medium} \to \text{recon}} + \underbrace{ \| \hat{x}_l - \text{sg}(\hat{x}_m) \|_1 + \text{LPIPS}(\hat{x}_l, \text{sg}(\hat{x}_m)) }_{\text{large} \to \text{medium}}$$

该设计从重建图像出发，通过中等扰动和大扰动两个级联阶段，迫使潜在流形在局部邻域内平滑变化。消融实验（Table 7）证实，**级联扰动设计相比无扰动、单一小扰动或大扰动，实现了最佳的 LPC 和 gFID，且不损害 rFID**。

**语义一致性正则化（SCR）** 通过全局池化与补丁级别的余弦距离保持语义组织：

$$\mathcal{L}_{\text{SCR}} = (1 - \cos(\bar{\mathbf{z}}_{T,g}, \bar{\mathbf{z}}_g)) + (1 - \cos(\bar{\mathbf{z}}_T, \bar{\mathbf{z}}))$$

SCR 在全局和局部两个粒度上对齐潜在码与 VFM 语义目标，确保潜在空间具有良好的类别级语义聚类。

三者加权组合形成总先验对齐损失：

$$\mathcal{L}_p = \lambda_{ssr} \mathcal{L}_{\text{SSR}} + \lambda_{mcr} \mathcal{L}_{\text{MCR}} + \lambda_{scr} \mathcal{L}_{\text{SCR}}$$

消融实验（Table 2(a)）严格验证了每个正则化项的作用：**移除 SSR、MCR 或 SCR 中任何一个均导致 gFID 显著上升，且分别降低其对应的几何指标 SSC、LPC 或 GSQ**。三者组合使用可获得最佳生成性能。

### 架构创新：冻结 VFM 编码器 + 细节感知调制器

与直接微调 VFM 或使用 VFM 特征作为对齐目标的现有方法不同，PAE 提出了**冻结 VFM 编码器 + 细节感知调制器（DAM）** 的架构设计。DAM 通过交叉注意力从像素令牌向冻结的 VFM 特征注入细节信息，并采用零初始化的尺度位移融合：

$$\gamma_p, \beta_p = \text{split}(\mathbf{W} \Delta \mathbf{H}), \quad \mathbf{H}_z = \text{LayerNorm}(\mathbf{H}_{\text{vfm}} \odot (1 + \gamma_p) + \beta_p)$$

零初始化确保了训练初期 VFM 特征的主导地位，避免像素细节干扰语义结构。消融实验（Table 3(b)）表明，**DAM 优于直接微调 VFM 或简单残差融合，显著提升 gFID 和 IS，同时更好地保留语义结构**。

### 先验精炼：从原始 VFM 特征到匹配的对齐目标

PAE 进一步发现，原始 VFM 特征并非最优的对齐目标。通过轻量级投影器压缩 VFM 特征，并结合空间上采样与低通归一化精炼，PAE 获得了与瓶颈维度匹配的语义目标和空间干净的结构目标。**Figure 4** 显示，精炼后的结构目标展现出更清晰的逐块空间相关性，压缩后的语义目标在嵌入空间中保持良好的聚类结构。消融实验（Table 2(b)）证实，**精炼后的 VFM 目标相比原始特征，在 SSC、GSQ、rFID 和 gFID 上均有提升**。

### 效果验证：收敛效率与生成质量的双重突破

在 ImageNet 256×256 类别条件生成任务上，PAE 在 80 个训练轮次即达到 gFID 1.27，在 800 轮次达到新的 SOTA gFID 1.03（Table 1）。更关键的是，**PAE 达到与 RAE 相当的生成质量所需的训练轮次减少了 13 倍**，直接验证了扩散友好流形对扩散模型学习效率的根本性提升。



PAE 的整体设计围绕一个核心目标展开：**显式塑造扩散友好的潜在流形**，而非像现有 tokenizer 那样仅依赖重建损失间接产生流形属性。其 pipeline 由四个功能模块构成，形成“冻结 VFM 编码 → 细节注入 → 先验对齐正则化 → 重建解码”的端到端流程。

### Pipeline 概览

给定输入图像 $x$，PAE 首先通过**冻结的视觉基础模型编码器** $E$ 提取稳定的语义特征 $\mathbf{H}_{\text{vfm}} = E(x)$。该编码器在整个 tokenizer 训练过程中保持冻结，为后续的先验对齐提供不变的语义参考锚点。

随后，**细节感知调制器（Detail-Aware Modulator, DAM）** 以 $x$ 的像素级特征和 $\mathbf{H}_{\text{vfm}}$ 为输入，通过交叉注意力机制将重建所需的高频细节注入冻结特征。DAM 的核心设计在于其融合方式——采用零初始化的尺度-位移操作：

$$\gamma_p, \beta_p = \text{split}(\mathbf{W} \Delta \mathbf{H}), \quad \mathbf{H}_z = \text{LayerNorm}(\mathbf{H}_{\text{vfm}} \odot (1 + \gamma_p) + \beta_p)$$

由于 $\gamma_p, \beta_p$ 初始为零，训练初期 DAM 的输出完全由 VFM 特征主导，细节信息在训练过程中逐步注入，从而在语义保真度和重建精度之间取得平衡。

调制后的表示 $\mathbf{H}_z$ 经**投影器 $P_\theta$** 映射到紧凑的潜在空间，再通过 RMS 归一化投影到球面流形上，得到最终的潜在码 $\mathbf{z}$。这一设计提高了扩散模型的训练效率和扰动稳定性。在解码端，**反投影器 $Q_\theta$ 和像素解码器 $D_\theta$** 从 $\mathbf{z}$ 重建图像，训练目标为标准的三项重建损失：

$$\mathcal{L}_{\text{recon}} = \mathcal{L}_{\ell_1} + \lambda_{\text{lpips}} \mathcal{L}_{\text{LPIPS}} + \lambda_{\text{gan}} \mathcal{L}_{\text{GAN}}$$

### 先验对齐正则化

在重建骨干网络之上，PAE 引入三个先验对齐正则化目标，分别对应扩散友好流形的三个关键几何属性：

1. **空间结构正则化（SSR）**：对齐潜在码与 VFM 目标特征的空间格拉姆矩阵，保持实例级拓扑结构：
   $$\mathcal{L}_{\text{SSR}} = \| \mathbf{G}_z - \mathbf{G}_T \|_F^2$$

2. **流形连续性正则化（MCR）**：通过级联扰动一致性设计，从重建图像出发逐步施加中等和较大扰动，约束解码结果在局部邻域内平滑变化：
   $$\mathcal{L}_{\text{MCR}} = \underbrace{ \| \hat{x}_m - \text{sg}(\hat{x}_r) \|_1 + \text{LPIPS}(\hat{x}_m, \text{sg}(\hat{x}_r)) }_{\text{medium} \to \text{recon}} + \underbrace{ \| \hat{x}_l - \text{sg}(\hat{x}_m) \|_1 + \text{LPIPS}(\hat{x}_l, \text{sg}(\hat{x}_m)) }_{\text{large} \to \text{medium}}$$

3. **语义一致性正则化（SCR）**：在全局池化和补丁两个粒度上最大化潜在码与目标特征的余弦相似度，保持语义聚类质量：
   $$\mathcal{L}_{\text{SCR}} = (1 - \cos(\bar{\mathbf{z}}_{T,g}, \bar{\mathbf{z}}_g)) + (1 - \cos(\bar{\mathbf{z}}_T, \bar{\mathbf{z}}))$$

三个目标加权组合为总先验对齐损失 $\mathcal{L}_p$，与重建损失联合优化。

### VFM 先验精炼

原始 VFM 特征在空间分辨率和语义维度上与 tokenizer 瓶颈并不匹配。PAE 通过一个轻量级精炼阶段解决这一问题：对结构分支，对 VFM 特征进行空间上采样和低通归一化，获得更干净的空间结构目标；对语义分支，通过瓶颈投影将高维 VFM 特征压缩到潜在空间维度，同时保持嵌入空间的聚类结构。精炼后的目标为 SSR 和 SCR 提供了更匹配的监督信号。

### 模块间的因果依赖

整个 pipeline 的因果链可概括为：冻结 VFM 编码器提供稳定的语义基底 → DAM 在不破坏语义主导权的前提下注入像素细节 → 投影与归一化形成紧凑的球面流形 → 三个先验对齐正则化项显式塑造流形的空间结构、局部连续性和全局语义 → 重建损失保证解码保真度。消融实验表明，移除任一正则化项均导致对应几何指标和生成质量显著下降，验证了各模块对最终性能的必要贡献。

### 补充图表

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the PAE framework. A frozen VFM provides stable representation features for the input image. DAM injects pixel detail while preserving the VFM as the dominant semantic source. The modulated representation is projected into a compact latent space for downstream diffusion. On top of this backbone, three prior-alignment objectives explicitly shape the latent manifold: SSR preserves instance-level spatial structure, MCR enforces local continuity, and SCR preserves global semantic organization*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/001_Figure_1.jpg]]
*Figure 1: Prior alignment constructs a diffusion-friendly latent manifold. Left: a conceptual illustration of latent space under the manifold assumption [53]. Compared with the reconstruction-oriented counterpart, the prior-aligned latent manifold is more structurally coherent, locally continuous, and semantically organized. Right: PAE yields faster convergence, better generation quality, and robust few-step sampling performance*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/012_Figure_9.jpg]]
*Figure 9: Illustration of Spatial Structure Coherence (SSC). For each image, we construct a latent-token affinity graph from the tokenizer output, perform spectral clustering on the token graph, and compare the resulting token partition with object-aware panoptic labels projected to latent resolution. Higher SSC indicates better alignment between latent token grouping and object-level spatial structure*



PAE 的架构围绕一个核心原则构建：**显式塑造潜在流形的扩散友好属性**，而非依赖重建目标间接产生。整体框架由冻结的视觉基础模型编码器、细节感知调制器、投影器与解码器，以及三个先验对齐正则化目标组成（Figure 3）。

### 3.1 冻结 VFM 编码与细节感知调制

给定输入图像 $x$，PAE 首先通过冻结的视觉基础模型提取特征 $\mathbf{H}_{\text{vfm}} = E(x)$。这些特征提供稳定的语义参考，但缺乏重建所需的像素级细节。为此，PAE 引入**细节感知调制器（Detail-Aware Modulator, DAM）**，通过交叉注意力从像素令牌向 VFM 特征注入细节信息。

DAM 的核心操作是零初始化的尺度-位移融合：

$$\gamma_p, \beta_p = \text{split}(\mathbf{W} \Delta \mathbf{H}), \quad \mathbf{H}_z = \text{LayerNorm}(\mathbf{H}_{\text{vfm}} \odot (1 + \gamma_p) + \beta_p) \tag{1}$$

其中 $\Delta \mathbf{H}$ 是 DAM 通过多层自注意力和交叉注意力从像素令牌中提取的细节调制信号，$\mathbf{W}$ 为投影权重。由于 $\gamma_p$ 和 $\beta_p$ 从零初始化，训练初期 $\mathbf{H}_z \approx \text{LayerNorm}(\mathbf{H}_{\text{vfm}})$，确保 VFM 始终作为语义主导源，细节注入以残差方式逐步学习。

调制后的表示 $\mathbf{H}_z$ 通过投影器 $P_\theta$ 映射到紧凑的潜在空间，并经过 RMS 归一化形成球面流形，以提高扩散效率与扰动稳定性。解码端由反投影器 $Q_\theta$ 和像素解码器 $D_\theta$ 完成重建，训练使用组合重建损失：

$$\mathcal{L}_{\text{recon}} = \mathcal{L}_{\ell_1} + \lambda_{\text{lpips}} \mathcal{L}_{\text{LPIPS}} + \lambda_{\text{gan}} \mathcal{L}_{\text{GAN}} \tag{2}$$

### 3.2 先验对齐正则化目标

PAE 的核心创新在于三个显式的先验对齐正则化项，分别对应扩散友好潜在流形的三个几何属性。

**空间结构正则化（Spatial Structure Regularization, SSR）** 对齐潜在码与目标特征的空间格拉姆矩阵，保持实例级拓扑结构：

$$\mathcal{L}_{\text{SSR}} = \| \mathbf{G}_z - \mathbf{G}_T \|_F^2 \tag{3}$$

其中 $\mathbf{G}_z$ 和 $\mathbf{G}_T$ 分别为潜在码 $\mathbf{z}$ 和目标特征 $\mathbf{T}$ 的空间格拉姆矩阵，$\|\cdot\|_F$ 为 Frobenius 范数。该损失强制潜在空间保留与 VFM 先验一致的补丁间空间关系。

**流形连续性正则化（Manifold Continuity Regularization, MCR）** 采用级联扰动一致性设计，逐步正则化局部邻域：

$$\mathcal{L}_{\text{MCR}} = \underbrace{ \| \hat{x}_m - \text{sg}(\hat{x}_r) \|_1 + \text{LPIPS}(\hat{x}_m, \text{sg}(\hat{x}_r)) }_{\text{medium} \to \text{recon}} + \underbrace{ \| \hat{x}_l - \text{sg}(\hat{x}_m) \|_1 + \text{LPIPS}(\hat{x}_l, \text{sg}(\hat{x}_m)) }_{\text{large} \to \text{medium}} \tag{4}$$

其中 $\hat{x}_r$ 为原始重建图像，$\hat{x}_m$ 和 $\hat{x}_l$ 分别为对潜在码施加中等和大扰动后的重建结果，$\text{sg}(\cdot)$ 为停止梯度操作。级联设计使模型先学习中等扰动到重建的连续性，再学习大扰动到中等扰动的连续性，相比单一扰动策略更有效地提升局部流形平滑性（Table 7）。

**语义一致性正则化（Semantic Consistency Regularization, SCR）** 通过余弦距离保持全局语义组织：

$$\mathcal{L}_{\text{SCR}} = (1 - \cos(\bar{\mathbf{z}}_{T,g}, \bar{\mathbf{z}}_g)) + (1 - \cos(\bar{\mathbf{z}}_T, \bar{\mathbf{z}})) \tag{5}$$

其中 $\bar{\mathbf{z}}_g$ 和 $\bar{\mathbf{z}}_{T,g}$ 分别为潜在码和目标特征的全局池化向量，$\bar{\mathbf{z}}$ 和 $\bar{\mathbf{z}}_T$ 为补丁级表示。该损失同时在全局和局部层面保持语义聚类质量。

总先验对齐损失为三者的加权组合：

$$\mathcal{L}_p = \lambda_{ssr} \mathcal{L}_{\text{SSR}} + \lambda_{mcr} \mathcal{L}_{\text{MCR}} + \lambda_{scr} \mathcal{L}_{\text{SCR}} \tag{6}$$

标记器训练使用联合目标 $\mathcal{L}_{\text{recon}} + \mathcal{L}_p$。

### 3.3 VFM 先验精炼

原始 VFM 特征并非直接适合作为对齐目标。PAE 通过两步精炼获得更好的监督信号（Figure 4）：对结构目标，通过空间上采样和低通归一化获得更清晰的补丁间空间相关性；对语义目标，通过轻量级投影器压缩到瓶颈维度，在保持语义聚类的同时实现维度匹配。消融实验表明，精炼后的目标在 SSC、GSQ、rFID 和 gFID 上均优于直接使用原始特征（Table 2(b)）。

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/004_Figure_4.jpg]]
*Figure 4: Refined VFM priors provide better-matched alignment targets for PAE*

### 补充图表

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/002_Figure_2.jpg]]
*Figure 2: Pilot experiments on diffusion-friendly latent manifold properties. (a) Better reconstruction alone (rFID) does not guarantee better generation quality (gFID). (b–d) In contrast, improvements in instance-level structure, local manifold continuity, and global manifold semantics consistently correlate with better generation across controlled tokenizer variants. Together, these motivate latent-manifold organization as an explicit objective for designing tokenizers. Full settings and metric definitions are provided in Appendix B*



## 实验与关键发现

### 先导实验：重建质量不能保证生成质量

现有潜在扩散标记器普遍以重建保真度（如 rFID）为核心优化目标，但 **Figure 2(a)** 的先导实验揭示了一个关键反直觉现象：更好的重建质量并不能保证更好的生成质量（gFID）。在受控的标记器变体上，rFID 与 gFID 之间不存在单调正相关关系。这一发现直接动摇了“重建越好则扩散生成越好”的默认假设。

进一步地，**Figure 2(b–d)** 表明，三个潜在流形的几何属性——实例级空间结构一致性（SSC）、局部流形连续性（LPC）和全局语义质量（GSQ）——的改善与下游生成质量呈现一致的正相关。这意味着，扩散模型的生成性能并非由重建精度间接决定，而是由潜在流形本身的组织方式直接塑造。这一洞察构成了 PAE 显式正则化潜在流形的动机基础。

### 主要生成性能

在 ImageNet 256×256 类别条件生成任务上，PAE 在收敛效率和最终生成质量两个维度均展现出显著优势。所有生成器均采用相同的 LightningDiT-XL/1 架构与训练配置，确保比较公平。

**Table 1** 报告了核心结果。在 80 个训练轮次下，PAE（DINOv2 骨干）即达到 **gFID 1.27**（含引导），显著优于同期表示导向标记器 VTP（1.44）和 GAE（1.48），降幅达 0.17–0.21。在 800 个轮次的长训练设置下，PAE 进一步达到 **gFID 1.03**，刷新了该设置下的最优生成质量，超越 RAE DiTDH-XL（1.13）和结合 REPA 的 Send-VAE（1.21），降幅达 0.10–0.18。值得强调的是，PAE 在 80 轮次即达到与 RAE 可比的质量水平，而后者需要约 13 倍的训练轮次，收敛效率提升显著。

在少步采样场景下，**Table 6** 和 **Figure 13** 显示 PAE 在 4 步至 16 步推理中持续优于 FAE，gFID 与 IS 曲线均保持明显优势，表明扩散友好流形对快速采样同样具有鲁棒性。

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/018_Table_6.jpg]]
*Table 6: Few-step sampling under the same long-training setting. Results are reported for PAE (DINOv2) with LightningDiT-XL/1 trained for 800 epochs using classifier-free guidance. FAE is evaluated under the same generator setting*

### 保真度-可学习性权衡分析

**Figure 6(a)** 刻画了跨标记器的重建保真度与下游可学习性之间的权衡关系。PAE 位于该权衡曲线的最优区域：在保持竞争性重建质量（rFID 0.26）的同时，实现了最优的生成可学习性。相比之下，单纯追求极低 rFID 的标记器往往在 gFID 上表现不佳，进一步印证了先导实验的结论。

**Figure 6(b)** 从五个维度——rFID、SSC、LPC、GSQ 和有效秩（eRank）——对比了不同标记器的潜在几何属性。PAE 在三个扩散友好指标（SSC、LPC、GSQ）上均取得最优或接近最优的值，同时保持了较高的潜在空间利用率（eRank），这解释了其在保真度-可学习性权衡中的优势地位。

**Figure 6(c)** 展示了 PAE 在不同 VFM 骨干（DINOv2、SigLIP2、DINOv3）上的性能剖面，表明该方法对编码器选择具有良好的泛化性。

### 先验对齐消融实验

**Table 2(a)** 系统消融了三个先验对齐目标的作用（所有消融均使用 25 轮标记器训练）。结果表明：

- **SSR（空间结构正则化）**单独使用时主要提升 SSC 指标，验证了其在保持实例级拓扑方面的针对性作用。
- **MCR（流形连续性正则化）**单独使用时主要提升 LPC 指标，验证了其在增强局部邻域平滑性方面的针对性作用。
- **SCR（语义一致性正则化）**单独使用时主要提升 GSQ 指标，验证了其在保持全局语义聚类方面的针对性作用。
- 移除任一目标均导致 gFID 显著上升，而**组合三者**可获得最佳的总体生成性能，证明三个属性对扩散友好流形是互补且必要的。

**Table 2(b)** 进一步验证了先验精炼的重要性。相较于直接使用原始 VFM 特征作为对齐目标，经过空间上采样与低通归一化精炼的结构目标以及经过瓶颈投影压缩的语义目标，在 SSC、GSQ、rFID 和 gFID 上均有提升。**Figure 4** 定性展示了精炼后结构目标的补丁间空间相关性更加清晰，语义目标在嵌入空间中仍保持良好的聚类结构。

### 核心设计选择消融

**Table 3** 消融了 PAE 的关键设计选择：

- **先验对齐 vs. 通用正则化**：将 SSR/MCR/SCR 替换为对比损失或 KL 散度等通用正则化器，gFID 显著恶化，表明扩散友好流形的塑造需要针对性目标，而非任意正则化。
- **DAM vs. 微调 VFM**：相比于直接微调 VFM 编码器或简单残差融合，DAM 的零初始化尺度位移融合设计显著提升了 gFID 和 IS，同时更好地保留了语义结构，验证了“冻结 VFM 主导、细节注入辅助”策略的有效性。
- **全令牌 SCR vs. 池化 SCR**：使用补丁级全令牌余弦距离的 SCR 优于仅使用全局池化特征的版本，表明细粒度的语义对齐对全局语义组织更为有效。

### MCR 扰动设计消融

**Table 7** 专门消融了 MCR 中的扰动一致性设计。结果表明：

- 无扰动一致性正则化时，LPC 和 gFID 均较差。
- 引入单一小扰动或大扰动的一致性损失可带来一定改善，但效果有限。
- **级联扰动设计**（Cascaded Perturb）——从重建到中等扰动再到较大扰动的逐步正则化——实现了最佳的 LPC 和 gFID，且不损害 rFID。这表明逐步扩展局部邻域范围是构建连续流形的更有效策略。

### 编码器泛化性

**Table 8** 验证了 PAE 在不同冻结 VFM 编码器上的泛化能力。在 DINOv2、SigLIP2、DINOv3 和 MAE 四种骨干上，添加先验对齐损失（L_p）后，PAE 均一致地提升了对应标记器骨架的生成性能，表明该方法不依赖于特定的 VFM 选择。

### 定性结果

**Figure 7** 展示了重建与生成的定性对比。在重建方面，PAE 在细薄结构、文字和人脸等细节上优于其他标记器。在生成方面，**Figure 5** 展示了 PAE 配合 LightningDiT-XL/1 在 80 轮次下的类别条件样本，图像展现出优秀的保真度和结构连贯性。

### 局限性与失败模式

尽管 PAE 在 ImageNet 256×256 上取得了显著成果，但当前验证仍存在以下局限：

1. **分辨率与领域局限**：所有主实验均在 256×256 分辨率下进行，未在更高分辨率或更多样视觉领域（如文本到图像、视频生成）中验证。
2. **固定分辨率架构**：当前框架仅考虑固定分辨率的潜在扩散，未涉及可变空间尺度或动态令牌分配。
3. **对手工正则化的依赖**：方法仍依赖精炼的 VFM 监督和多个精心设计的正则化项，尚未证明这些流形属性能否通过更强的预训练或更大规模数据自然涌现。

### 补充图表

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/006_Table_1.jpg]]
*Table 1: Generation performance on ImageNet 256×256. PAE improves both convergence efficiency and final generation quality under the same training setup. In particular, PAE (DINOv2) achieves 1.27 gFID at 80 epochs and a new state-of-the-art 1.03 gFID at 800 epochs. ∗ indicates results obtained with AutoGuidance [38] as reported in the original work*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/010_Table_2.jpg]]
*Table 2: Ablation study on prior alignment. All ablations use 25 tokenizer epochs. (a) Each objective most strongly improves its intended dimension, and combining all three gives the best overall generation performance. (b) Refining the VFM targets further improves structure and semantics*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/020_Table_7.jpg]]
*Table 7: Ablation on perturbation design for MCR. Generic perturbation consistency helps, but the proposed cascaded design gives the best continuity and generation quality*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/008_Figure_6.jpg]]
*Figure 6: Understanding PAE’s fidelity–learnability advantage. (a) Trade-off between reconstruction fidelity and downstream learnability across tokenizers. ∗ denotes generative performance measured at 64 training epochs. (b) Comparison of reconstruction, latent geometry, and utilization using rFID, SSC, LPC, GSQ, and eRank. (c) Profiles of PAE built on different VFM backbones*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative Comparison. (a) Reconstruction: PAE outperforms other tokenizers in reconstructing details (e.g., thin structures, text, and faces). (b) Generation*

![[assets/figures/papers/paper_list_l83_https_arxiv_org_abs_2605_07915/figures/021_Table_8.jpg]]
*Table 8: Encoder generalization across frozen teachers. PAE consistently improves over the corresponding tokenizer scaffold without*



## 定位与知识库关联

### 1. 从重建导向到流形组织导向的范式转换

现有潜在扩散（Latent Diffusion）的tokenizer设计主要沿两条技术路线演进：**重建导向**与**表示导向**。VA-VAE等早期工作将tokenizer视为纯粹的有损压缩器，仅优化像素级重建保真度（L1+LPIPS+GAN）；VTP、GAE、FAE等方法则直接继承或对齐预训练视觉基础模型（VFM）的特征表示，试图将语义先验注入潜在空间。RAE作为表示原生tokenizer的代表，在重建与语义保留之间寻求折中；AlignTok进一步引入显式表示对齐。

然而，**本工作的核心发现揭示了上述路线的共同盲区**：无论是重建质量（rFID）还是表示相似度，均无法可靠预测下游扩散模型的生成质量（gFID）。Figure 2(a)的先导实验明确显示，更好的rFID并不保证更好的gFID——这一反直觉现象构成了方法学上的关键转折点。PAE的贡献不在于提出新的tokenizer架构，而在于**将优化目标从“潜在空间应该像什么（重建/表示）”转换为“潜在流形应该具备何种几何属性（扩散友好性）”**，并据此定义了三个可量化、可优化的流形属性：空间结构一致性（SSC）、局部流形连续性（LPC）和全局语义质量（GSQ）。

### 2. 方法定位：流形正则化与VFM先验的协同

PAE在技术谱系中占据一个独特位置，其核心设计由两个正交维度构成：

**（1）VFM先验的利用方式**。与VTP、GAE等直接使用VFM特征作为潜在码或将VFM编码器微调的方法不同，PAE采用**冻结VFM编码器 + 细节感知调制器（DAM）**的混合架构。DAM通过零初始化尺度-位移融合（Eq. 1）注入像素细节，但保持VFM作为语义主导源。Table 3(b)的消融表明，DAM优于直接微调VFM或简单残差融合，在gFID和IS上均有显著提升，同时更好地保留语义结构。这一设计与REPA的表示引导DiT形成互补——前者在tokenizer端塑造流形，后者在扩散模型端引入表示监督。

**（2）流形正则化的显式设计**。PAE的三个先验对齐目标（SSR、MCR、SCR）分别对应三个扩散友好属性，构成一个完整的流形组织框架。Table 2(a)的消融实验证实，每个目标主要提升其对应的几何指标（SSR→SSC，MCR→LPC，SCR→GSQ），且三者组合获得最佳生成性能。其中MCR的级联扰动一致性设计（Cascaded Perturb）尤为关键：Table 7显示，相比无扰动或单一扰动，级联设计在提升局部连续性的同时不损害重建质量，揭示了**多尺度邻域平滑对于扩散学习的重要性**。

此外，PAE引入的**先验精炼策略**（空间上采样与低通归一化获得结构目标，瓶颈投影获得语义目标）进一步提升了对齐质量。Figure 4和Table 2(b)证实，精炼后的目标在SSC、GSQ、rFID和gFID上均优于原始VFM特征。

### 3. 适用边界与局限

当前PAE的验证范围存在明确边界：

- **分辨率与任务域受限**：所有主实验均在ImageNet 256×256的类别条件生成下进行，尚未在更高分辨率（>256×256）、文本到图像等多模态生成、视频生成等场景中验证。Figure 8的泛化性分析虽表明PAE在不同VFM编码器（DINOv2、SigLIP2、DINOv3、MAE）下均有效，但任务域的泛化仍属开放问题。
- **固定分辨率潜在扩散**：当前框架假设固定尺度的潜在表示，未涉及可变空间尺度、动态令牌分配或分辨率自适应生成，这限制了其在需要灵活空间压缩率场景中的应用。
- **对精炼VFM监督的依赖**：方法仍依赖精炼的VFM特征作为对齐目标，以及多个精心设计的正则化项。这引入了额外的计算开销和超参数调优负担（SSR、MCR、SCR的损失权重）。

### 4. 开放问题与未来方向

PAE将潜在扩散tokenizer的设计从“间接涌现”推向“显式塑造”，但这一范式转换同时开启了若干深层问题：

1. **流形属性的自然涌现可能性**：类似的扩散友好流形属性能否通过更强的tokenizer预训练、更大规模数据或更统一的自监督目标自然涌现，而不需要手工设计的对齐损失？这与自监督学习领域“涌现表示”的讨论形成呼应。

2. **扰动策略的自适应性**：局部连续性正则化的最优扰动尺度和策略是否因任务和模型而异？能否设计自适应调整机制，根据潜在流形的局部曲率动态确定扰动幅度？

3. **与扩散架构的深度协同**：当前PAE与扩散模型（LightningDiT-XL/1）的训练是分离的。能否将流形组织原则与DiT变体的架构改进（如REPA的表示引导）更深度地结合，实现tokenizer与扩散模型的联合优化？

4. **跨模态与高分辨率扩展**：PAE的流形组织原则能否迁移到文本到图像生成、视频生成等场景？在高分辨率下，空间结构正则化（SSR）的计算开销（Gram矩阵的Frobenius范数）可能成为瓶颈，需要更高效的近似方法。



## 原文 PDF

![[paperPDFs/arxiv_2026/What_Matters_for_Diffusion_Friendly_Latent_Manifold_Prior_Aligned_Autoencoders_for_Latent_Diffusion.pdf]]
