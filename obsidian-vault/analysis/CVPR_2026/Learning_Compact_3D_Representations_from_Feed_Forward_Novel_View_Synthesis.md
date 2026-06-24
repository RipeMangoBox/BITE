---
title: Learning Compact 3D Representations from Feed-Forward Novel View Synthesis
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Compact_3D_Representations_from_Feed_Forward_Novel_View_Synthesis.pdf
project_link: "https://cvlab-kaist.github.io/C3G"
code_link: null
aliases:
- CCGCF
- LC3RFFFNVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过可学习查询 token 与多视图图像特征进行全局自注意力聚合，用少量 token 生成紧凑高斯，从根本上消除了冗余。
primary_logic: 仅利用光度重建损失的端到端训练即可使查询 token 自发学习关注空间一致区域，从而在不需任何显式监督的情况下完成高质量新视图合成；此外，C3G-G 中学到的注意力模式可直接用于多视图特征聚合，消除特征不一致性，避免信息压缩，显著提升三维场景理解。
claims:
- C3G 仅使用约 2K 高斯（比 LSM 少约 65 倍）即可实现优越的内存效率和新视图合成质量。
- 在 ScanNet 开放词汇分割中，C3G 以更少高斯超越了 LSM：mIoU (LSeg) 0.513 vs 0.503。
- 渐进式低通滤波和解冻视觉编码器对训练至关重要，消融实验表明缺乏这些设计将导致模型崩溃。
- ScanNet 上 PSNR (新视图合成) = 23.612
---

# Learning Compact 3D Representations from Feed-Forward Novel View Synthesis

> [!tip] 核心洞察
> 仅利用光度重建损失的端到端训练即可使查询 token 自发学习关注空间一致区域，从而在不需任何显式监督的情况下完成高质量新视图合成；此外，C3G-G 中学到的注意力模式可直接用于多视图特征聚合，消除特征不一致性，避免信息压缩，显著提升三维场景理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于前馈式新视图合成的紧凑三维表示学习 |
| 英文题名 | Learning Compact 3D Representations from Feed-Forward Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/An_Learning_Compact_3D_Representations_from_Feed-Forward_Novel_View_Synthesis_CVPR_2026_paper.html) · [Project](https://cvlab-kaist.github.io/C3G) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | C3G (C3G-G 和 C3G-F) |
| Dataset | ScanNet, N/A |

> [!tip] 效果简介
> - ScanNet 上，PSNR (新视图合成) 23.612 vs 21.262 (VGGT+NoPo) (+2.35)；mIoU (LSeg 开放词汇分割) 0.513 vs 0.503 (LSM) (+0.01)。
> - N/A (通用比较) 上，高斯数量 (↓) 2K vs ≈130K (LSM) (约 65 倍减少)。

## 概述

### 1. 问题与瓶颈

从多视图图像构建三维场景表示是计算机视觉的核心任务，但现有方法面临一个关键瓶颈：**逐像素预测范式产生大量冗余高斯原语**。以 LSM 为代表的密集预测方法为每个像素生成一个或多个 3D 高斯，导致高斯数量膨胀至约 130K，不仅内存开销高，更严重的是，在将 2D 语义特征提升到 3D 时，必须将高维特征压缩到低维嵌入以控制计算负担，造成不可逆的信息损失，制约了下游场景理解的性能上限。

### 2. 核心思路

本文提出 **C3G**（Compact 3D Gaussian Representations），其核心调控变量是**高斯的生成方式**：不再逐像素预测，而是引入一组可学习查询 token（仅约 2K 个），通过 Transformer 与多视图图像特征进行全局自注意力交互，使每个 token 自发聚合空间一致区域的信息，最终解码为紧凑且非冗余的 3D 高斯。这一设计从根源上消除了冗余，同时带来了一个关键涌现特性——**仅靠光度重建损失的端到端训练，查询 token 即可学会关注跨视图的空间对应区域**，无需任何显式监督。

在此基础上，C3G 进一步将学到的注意力模式复用于 2D 到 3D 的特征提升（C3G-F），直接聚合多视图特征而无需压缩，从根本上避免了信息瓶颈。

### 3. 方法谱系与知识库定位

C3G 处于**前馈式新视图合成**与**紧凑场景表示**的交叉点。其方法谱系可沿两个维度定位：

| 维度 | 现有方法 | C3G 的差异化 |
|------|----------|-------------|
| 高斯生成 | LSM、NoPo 等逐像素预测 | 查询 token 驱动的紧凑生成 |
| 特征提升 | Feature-3DGS 等逐场景优化 + 压缩 | 复用注意力权重的无压缩多视图聚合 |
| 表示紧凑性 | CF3 等紧凑特征场 | 以 3DGS 为基底，兼顾渲染速度与紧凑性 |

C3G 并非孤立改进某一模块，而是同时改变了高斯生成方式、特征提升方式和训练稳定性策略三个关键槽位，形成系统性的紧凑表示方案。

### 4. 主要结果概要

- **表示紧凑性**：仅使用约 2K 高斯，比 LSM（约 130K）减少约 65 倍，内存占用仅 4.1 MB。
- **新视图合成**：在 RealEstate10K 上，C3G 以更少高斯取得竞争性或更优的 PSNR；在 ScanNet 上，PSNR 达到 23.612，显著优于 VGGT+NoPo 的 21.262。
- **三维场景理解**：在 ScanNet 开放词汇分割中，mIoU 达到 0.513（LSeg），超越 LSM 的 0.503；在 Replica 上也以更少高斯超越所有前馈式方法。
- **训练稳定性**：渐进式低通滤波和解冻视觉编码器是训练成功的关键，消融实验表明缺失任一设计将导致模型崩溃。
- **特征提升质量**：C3G-F 无需自动编码器压缩即可取得与压缩方法相似的 mIoU 和更高的 PSNR，验证了紧凑表示与无压缩特征聚合的双重优势。

### 5. 局限与开放问题

C3G 的训练依赖已知目标相机姿态，限制了完全无姿态场景下的前馈应用；紧凑高斯在捕捉高复杂场景的精细细节时可能不足；C3G-F 需依赖已训练的 C3G-G 注意力权重，无法联合端到端训练。未来方向包括：扩展至动态场景、消除测试时优化实现零样本高质量合成、以及探索注意力模式向其他三维表示（如 NeRF）的迁移潜力。

## 背景与动机

### 前馈式新视图合成中的冗余困境

从稀疏多视图图像中重建三维场景是计算机视觉的核心问题。近年来，前馈式三维高斯泼溅方法因其推理速度快、无需逐场景优化而受到广泛关注。这类方法的核心流程是：给定多视图图像，直接通过网络前向传播预测一组三维高斯原语，随后利用可微光栅化渲染新视图。

然而，现有前馈式方法普遍采用**逐像素预测**策略——对每个输入图像的每个像素预测一个或多个三维高斯。这一设计导致了严重的冗余问题：以 **LSM** 为代表的方法为单个场景生成约 13 万个高斯原语，其中大量高斯分布在空间上重叠或位于对渲染贡献微弱的区域。这种冗余带来了两个连锁困境：

1. **内存开销高昂**：密集高斯存储占用了大量显存，限制了方法在资源受限场景下的部署。
2. **2D 到 3D 特征提升困难**：当需要将二维语义特征（如分割特征、对应特征）提升到三维空间时，逐像素高斯的冗余使特征压缩成为必要——必须将高维语义特征压缩为低维嵌入以匹配高斯数量。这一压缩过程不可避免地造成信息损失，损害下游场景理解任务的性能。

### 紧凑表示的结构性优势

直觉上，一个场景的三维几何结构可以用远少于像素数量的高斯原语来紧凑描述。关键挑战在于：**如何让网络自动发现哪些空间位置值得放置高斯，而非被动地为每个像素生成高斯？**

这种从“密集预测”到“稀疏发现”的范式转换具有多重优势：
- **消除冗余**：仅在场景的关键几何位置放置高斯，大幅减少原语数量。
- **避免特征压缩**：紧凑高斯可直接承载高维语义特征，无需降维，保留完整信息。
- **跨视图一致性**：稀疏高斯天然避免了逐像素方法中因视图不对齐导致的特征不一致问题。

### 本文动机

基于上述观察，本文提出 **C3G (Compact 3D Gaussian Representations)**，核心思想是：用一组可学习的查询 token 替代逐像素预测，通过 Transformer 的全局自注意力机制，让查询 token 从多视图图像特征中自主聚合信息，解码出紧凑的三维高斯原语。这一设计从根本上切断了高斯数量与像素数量的耦合，实现了约 65 倍的高斯压缩（从约 13 万降至约 2K），同时在新视图合成质量和三维场景理解性能上均超越现有前馈式方法。

## 核心创新

本工作围绕**紧凑三维表示**这一核心目标，提出了两个关键创新：**C3G-G**（紧凑高斯解码器）和**C3G-F**（视角不变特征解码器）。二者协同工作，从根本上改变了前馈式三维重建的范式——从“密集预测后筛选”转向“直接生成紧凑表示”。

### 从逐像素密集预测到查询驱动的紧凑生成

现有前馈式方法（如 **LSM**）的核心瓶颈在于“逐像素预测”范式：每个像素独立预测一个或多个高斯原语，导致生成的高斯数量随图像分辨率线性增长，产生大量冗余原语。这些冗余不仅带来高昂的内存开销，还使得后续的 2D 到 3D 特征提升面临沉重的计算负担和特征不一致性问题。

C3G-G 的核心创新在于**用可学习查询 token 替代逐像素预测**。具体而言，方法引入一组紧凑的可学习查询 token $Q \in \mathbb{R}^{N \times d}$（默认 $N=2048$），将其与多视图图像特征拼接后送入 Transformer 进行全局自注意力交互。精炼后的查询 token 通过轻量 MLP 头直接解码为单个 3D 高斯的属性：

$$\mathbf{G}_i = \{\mu_i, \sigma_i, \Sigma_i, c_i\}$$

这一设计的关键因果机制在于：**全局自注意力使每个查询 token 能够跨视图聚合空间一致区域的信息**，从而自发地“发现”场景中真正需要建模的关键位置。实验表明，C3G 仅需约 2K 个高斯即可完成高质量新视图合成，相比 LSM 的约 130K 个高斯减少了约 65 倍（Figure 1）。值得注意的是，这种空间注意力模式完全是在光度重建损失的端到端训练中自发涌现的，无需任何显式的位置监督（Figure 3b）。

### 从特征压缩到注意力复用的无损提升

现有方法的第二个关键局限在于 2D 到 3D 的特征提升过程。由于逐像素方法生成大量高斯，为每个高斯附加高维语义特征会导致内存爆炸。因此，现有方法不得不将高维特征压缩为低维嵌入，这一压缩过程不可避免地造成信息损失。

C3G-F 的创新在于**复用 C3G-G 已学到的注意力权重，实现无损的特征聚合**。其设计思路简洁而高效：

1. **架构复用**：C3G-F 复制 C3G-G 的完整架构和参数作为初始化。
2. **注意力冻结**：冻结 C3G-G 中学到的自注意力权重，仅训练值投影（value projection）层。
3. **特征聚合**：利用冻结的注意力模式，将任意 2D 特征图（如 LSeg、MaskCLIP、DINOv2）聚合为视角一致的 3D 特征，直接附加到对应高斯上。

这一设计的核心优势在于：**注意力权重已经编码了跨视图的空间对应关系，C3G-F 只需学习如何将 2D 特征值映射到 3D 空间，而无需重新学习特征聚合的结构**。由于高斯数量本身已高度紧凑（约 2K），附加的语义特征不会带来显著的内存增长，因此完全无需进行特征压缩。消融实验（Table 7）证实，C3G-F 即使不使用自动编码器压缩，也能取得与压缩方法相似的 mIoU 和更高的 PSNR，直接验证了紧凑表示和无压缩特征的双重优势。

### 训练稳定性关键设计

从密集预测转向查询驱动的紧凑生成并非简单的架构替换。消融实验（Table 5）揭示了一个关键发现：**如果直接训练，模型会崩溃**。这是因为训练初期，随机初始化的查询 token 无法有效定位场景结构，导致梯度信号混乱。

为解决这一问题，方法引入了**渐进式低通滤波**策略。具体而言，在 2D 高斯投影中引入尺寸控制参数 $s$：

$$\mathbf{G}_i^{2D}(p) = e^{-\frac{1}{2}(p - \mu_i^{2D})^T (\Sigma_i^{2D} + s\mathbf{I})^{-1} (p - \mu_i^{2D})}$$

训练初期将 $s$ 设为 300，使每个高斯覆盖极大的图像区域，提供平滑、稳定的梯度信号；随后逐步退火至 $s=0.3$，使高斯逐渐收缩到精确的局部位置。这一策略与解冻视觉编码器的配合使用，是训练成功的关键前提。

### 创新点总结

| 创新维度 | Baseline 做法 | C3G 做法 | 因果机制 |
|---------|-------------|---------|---------|
| 高斯生成 | 逐像素预测，数量与分辨率线性相关 | 可学习查询 token 通过自注意力解码，数量固定为 2K | 全局自注意力使 token 自发关注空间一致区域，消除冗余 |
| 特征提升 | 密集高斯 → 特征压缩 → 信息损失 | 复用 C3G-G 注意力权重直接聚合，无需压缩 | 注意力权重已编码跨视图对应关系，仅需学习值映射 |
| 训练稳定性 | 固定高斯尺寸 | 渐进式低通滤波（$s: 300 \to 0.3$） | 初期大尺寸提供平滑梯度，后期收缩至精确位置 |

## 整体框架

C3G 的整体 pipeline 围绕一个核心设计：**用少量可学习查询 token 替代逐像素预测，生成紧凑的 3D 高斯表示**。该框架由两个可独立训练的模块构成——C3G-G（高斯解码器）与 C3G-F（特征解码器），两者共享相同的注意力模式，分别服务于新视图合成与下游三维理解任务。

### 输入与特征提取

给定同一场景的 $V$ 张多视图图像 $\{I_v\}_{v=1}^V$，C3G 首先通过冻结的视觉编码器 $\mathcal{E}(\cdot)$ 提取每张图像的特征图。默认编码器采用 **VGGT**（Wang et al.），该编码器在大规模三维数据上预训练，具备丰富的几何先验，为后续的跨视图信息聚合提供了强基础。消融实验（Table 8）表明，视觉编码器的选择对最终性能有显著影响，VGGT 在所有候选编码器中表现最优。

### C3G-G：紧凑高斯解码器

C3G-G 是整个框架的核心，其目标是**从多视图特征中直接解码出少量但具有代表性的 3D 高斯原语**。具体流程如下：

1. **查询 token 初始化**：引入 $N=2048$ 个可学习的查询 token $\mathbf{Q} \in \mathbb{R}^{N \times d}$，每个 token 作为场景中一个潜在高斯原语的抽象表示。

2. **跨视图全局自注意力**：将查询 token 与所有视图的展平图像特征拼接为序列 $\mathbf{X} = [\mathbf{Q}; \mathbf{F}]$，送入 $L=2$ 层 Transformer 进行全局自注意力处理。这一设计使每个查询 token 能够自由地关注任意视图的任意空间位置，从而自发地发现场景中“值得建模”的关键区域。

3. **高斯参数解码**：精炼后的查询 token 通过轻量 MLP 头（Gaussian Head）分别解码为单个 3D 高斯的属性：
   $$\mathbf{G}_i = \{\mu_i, \sigma_i, \Sigma_i, c_i\}$$
   其中 $\mu_i \in \mathbb{R}^3$ 为高斯中心，$\sigma_i \in [0,1)$ 为不透明度，$\Sigma_i \in \mathbb{R}^{3\times3}$ 为协方差矩阵，$c_i$ 为球谐系数（训练时球谐阶数设为 0，仅建模 RGB 颜色以稳定训练）。

4. **新视图渲染与监督**：生成的高斯集合通过 alpha 混合渲染目标视角图像 $\hat{I}_t$：
   $$\hat{I}_t(p) = \sum_{i=1}^{N} c_i \sigma_i \mathbf{G}_i^{2D}(p) \prod_{j=1}^{i-1} (1 - \sigma_j \mathbf{G}_j^{2D}(p))$$
   训练损失结合 MSE 与 LPIPS 感知损失：
   $$\mathcal{L}_{\mathrm{novel}} = \lambda_{\mathrm{MSE}} \mathcal{L}_{\mathrm{MSE}}(\hat{I}_t, I_t) + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}}(\hat{I}_t, I_t)$$

### 训练稳定性设计

直接训练上述框架面临严重的优化困难。为此，C3G 引入了两项关键的稳定性措施：

- **渐进式低通滤波**：受 RAIN-GS 启发，在训练初期对 2D 高斯投影施加极大的低通滤波（$\mathbf{G}_i^{2D}(p) = e^{-\frac{1}{2}(p - \mu_i^{2D})^T (\Sigma_i^{2D} + s\mathbf{I})^{-1} (p - \mu_i^{2D})}$），将尺寸控制参数 $s$ 从 300 逐步退火至 0.3。这使得梯度信号在训练早期能够覆盖大面积区域，引导查询 token 收敛到有效位置。

- **冻结视觉编码器**：训练 C3G-G 时，VGGT 编码器的权重保持冻结，仅更新查询 token 和 Transformer 层参数。

消融实验（Table 5）给出了决定性证据：**单独或同时缺失渐进式低通滤波和解冻编码器，模型将直接崩溃**，这验证了上述设计对于训练可行性的必要作用。

### C3G-F：特征解码器

在 C3G-G 训练完成后，C3G-F 复用其学到的注意力权重来实现 2D 到 3D 的特征提升。具体而言：

- C3G-F 复制 C3G-G 的完整架构和参数，但**冻结所有注意力权重，仅允许注意力操作中的值投影（value projections）可训练**。
- 引入可学习的特征查询 token $\mathbf{Q}_F$，通过相同的跨视图注意力模式聚合多视图特征，得到视角一致的 3D 特征。
- 聚合特征附加到对应高斯上作为额外属性，通过相同的 alpha 混合渲染目标视角特征图，以余弦相似度损失监督：
  $$\mathcal{L}_{\mathrm{feat}} = 1 - \cos(\hat{\mathbf{F}}_t / \|\hat{\mathbf{F}}_t\|, \mathbf{F}_t' / \|\mathbf{F}_t'\|)$$

### 关键洞察：注意力模式的自发涌现

C3G 框架最引人注目的特性是：**仅通过光度重建损失 $\mathcal{L}_{\mathrm{novel}}$ 的端到端训练，每个查询 token 便自发学会了关注跨视图的空间一致区域**（Figure 3b 可视化）。这种涌现的注意力模式构成了 C3G-G 与 C3G-F 之间的桥梁——它既保证了高斯原语被放置在几何有意义的位置，又为多视图特征的无压缩聚合提供了天然的对齐机制，从根本上避免了逐像素方法中因特征压缩导致的信息损失。

### 输入输出流总结

| 阶段 | 输入 | 处理 | 输出 |
|------|------|------|------|
| 特征提取 | $V$ 张多视图图像 | 冻结的 VGGT 编码器 | 多视图特征图 |
| C3G-G 解码 | 特征图 + 查询 token $\mathbf{Q}$ | $L$ 层 Transformer 全局自注意力 → MLP 头 | $N$ 个紧凑 3D 高斯 |
| C3G-F 解码 | 特征图 + 特征查询 $\mathbf{Q}_F$ + 冻结的注意力权重 | 可训练的值投影 → 特征聚合 | 视角一致的 3D 语义特征 |

### 补充图表

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/003_Figure_3.jpg]]
*Figure 3: Architecture and emergent attention behaviors of our 3D Gaussian decoder (C3G-G). (a) Our framework extracts features using VGGT, then processes them with learnable queries through transformer in our decoder (C3G-G). The refined queries are subsequently decoded into compact 3D Gaussians via a Gaussian head, trained with the novel view synthesis loss*

## 核心模块与公式推导

### 3.1 问题形式化与3D高斯表示

给定一组捕捉同一场景的多视图图像 $\{I_v\}_{v=1}^V$，目标是从中学习一组紧凑的3D高斯原语 $\{\mathbf{G}_i\}_{i=1}^N$，使其能够最佳地表征该场景。每个3D高斯 $\mathbf{G}_i$ 由以下属性定义：

$$\mathbf{G}_i = \{\mu_i, \sigma_i, \Sigma_i, c_i\}$$

其中 $\mu_i \in \mathbb{R}^3$ 表示高斯中心位置，$\sigma_i \in [0,1)$ 表示不透明度，$\Sigma_i \in \mathbb{R}^{3\times3}$ 为协方差矩阵，$c_i \in \mathbb{R}^{3(L+1)}$ 为球谐系数（在C3G实现中，为稳定训练将球谐阶数设为0，仅建模RGB颜色）。

### 3.2 多视图特征编码

C3G采用预训练的VGGT作为默认视觉编码器 $\mathcal{E}(\cdot)$，从多视图图像中提取具有丰富几何先验的特征图。VGGT编码器为每个输入视图生成特征表示，这些特征随后与可学习查询token一同输入Transformer解码器。

### 3.3 C3G-G：紧凑高斯解码器

C3G-G的核心创新在于用一组可学习查询token $\mathbf{Q} \in \mathbb{R}^{N \times d}$（默认 $N=2048$）替代逐像素预测范式。具体流程如下：

1. **序列构建**：将查询token与多视图图像特征拼接为 $\mathbf{X} = [\mathbf{Q}; \mathbf{F}]$。
2. **全局自注意力**：序列通过 $L=2$ 层Transformer进行全局自注意力处理，使每个查询token能够跨视图聚合空间一致区域的信息。
3. **高斯参数解码**：精炼后的查询token通过轻量MLP头解码为单个3D高斯的全部属性。

**新视图合成与训练损失**：通过alpha混合渲染目标视图像素颜色：

$$\hat{I}_t(p) = \sum_{i=1}^{N} c_i \sigma_i \mathbf{G}_i^{2D}(p) \prod_{j=1}^{i-1} (1 - \sigma_j \mathbf{G}_j^{2D}(p))$$

训练目标结合MSE损失和感知损失：

$$\mathcal{L}_{\mathrm{novel}} = \lambda_{\mathrm{MSE}} \mathcal{L}_{\mathrm{MSE}}(\hat{I}_t, I_t) + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}}(\hat{I}_t, I_t)$$

### 3.4 渐进式低通滤波

为稳定训练初期优化，C3G引入低通滤波2D高斯投影，在投影协方差矩阵上添加尺寸控制项 $s\mathbf{I}$：

$$\mathbf{G}_i^{2D}(p) = e^{-\frac{1}{2}(p - \mu_i^{2D})^T (\Sigma_i^{2D} + s\mathbf{I})^{-1} (p - \mu_i^{2D})}$$

训练过程中，$s$ 从 $s=300$ 逐步退火至 $s=0.3$。消融实验（Table 5）证实，缺乏此设计将导致模型崩溃。

### 3.5 C3G-F：视角不变特征解码器

C3G-F复用C3G-G中已学到的注意力权重，实现2D特征到3D的高效提升，消除逐像素方法中的信息压缩瓶颈。

**训练方案**：初始化时复制C3G-G的架构和参数，但仅允许注意力操作中的值投影（value projections）可训练，冻结注意力权重。通过最小化渲染特征图 $\hat{\mathbf{F}}_t$ 与真实特征图 $\mathbf{F}_t'$ 之间的余弦距离进行训练：

$$\mathcal{L}_{\mathrm{feat}} = 1 - \cos(\hat{\mathbf{F}}_t / \|\hat{\mathbf{F}}_t\|, \mathbf{F}_t' / \|\mathbf{F}_t'\|)$$

聚合后的多视图特征作为高斯的附加属性，可通过相同的alpha混合渲染管线生成新视图特征图。

### 3.6 关键设计决策的因果机制

| 模块 | 设计选择 | 因果作用 |
|------|----------|----------|
| 查询token | $N=2048$，全局自注意力 | 从根本上消除逐像素预测的冗余，每个token自发学习关注空间一致区域 |
| 渐进式低通滤波 | $s: 300 \to 0.3$ | 训练初期提供粗粒度优化信号，防止梯度不稳定导致崩溃 |
| 注意力权重复用 | C3G-F冻结C3G-G注意力 | 避免特征压缩，实现无信息损失的多视图特征聚合 |
| 球谐阶数 | 设为0 | 简化训练，仅建模RGB颜色以稳定优化 |

### 补充图表

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of per-pixel and compact scene representations. (Left): Existing per-pixel estimators [16, 54] predict one or multiple Gaussians per pixel, resulting in redundant Gaussians with misalignments across views. (Right): Our method uses learnable Gaussian queries to discover and decode only compact 3D Gaussians at essential locations, achieving a compact representation with only 2K Gaussians and 4.1M memory while avoiding redundancy and achieving superior segmentation and novel view synthesis performance*

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/004_Figure_4.jpg]]
*Figure 4: C3G-F training scheme. We leverage the learned attention patterns from the Gaussian decoder C3G-G (top) to efficiently learn a 3D feature decoder C3G-F(bottom) for feature lifting. We initialize C3G-F by copying C3G-G’s architecture and copy the attention weights from C3G-G, using learnable feature queries*

## 实验与分析

### 新视图合成质量与紧凑性

C3G 的核心优势在于以极少的 3D 高斯实现竞争性的新视图合成质量。在 RealEstate10K 数据集上，C3G 仅需约 2K 高斯即可完成场景建模——比逐像素方法 LSM 少约 65 倍（Table 1）。在 2 视图输入设置下，C3G 的 PSNR 达到 23.612，显著优于 VGGT+NoPo 组合基线的 21.262（Table 2）。当扩展到 36 视图输入并辅以测试时优化（TTO）时，C3G 的 PSNR 进一步提升至 30.250，高斯数量也仅需 26K（Table 1），展现出优异的可扩展性。

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/005_Table_1.jpg]]
*Table 1: Comparison of novel view synthesis with multi-view input images on RealEstate10K [62]. Our method generates fewer Gaussians while achieving competitive or superior quality. TTO denotes that test-time optimization is applied to the Gaussians*

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/006_Table_2.jpg]]
*Table 2: Comparison of 3D scene understanding on ScanNet [7]. We lift LSeg [26] and MaskCLIP [60] features from two input views and evaluate open-vocabulary segmentation on target views. Our method generates fewer Gaussians while outperforming feed-forward and per-scene optimization methods trained with substantially more posed inputs. ∗: Features directly extracted from target view images*

这种紧凑性直接转化为内存效率优势：C3G 仅需 4.1M 内存即可完成场景表示（Figure 2），而逐像素方法因产生大量冗余高斯导致内存开销高昂。

### 三维场景理解性能

C3G 的紧凑高斯表示天然适配 2D 到 3D 的特征提升任务。在 ScanNet 开放词汇分割评估中，C3G 以更少的高斯数量超越了前馈式密集高斯方法 LSM：LSeg 特征的 mIoU 为 0.513 vs 0.503（Table 2）。在 Replica 数据集上，C3G 同样优于所有前馈式方法，并与使用更多姿态输入的逐场景优化方法（如 Feature-3DGS）取得可比结果（Table 3）。

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/007_Table_3.jpg]]
*Table 3: Comparison of 3D scene understanding on Replica [43]. We lift LSeg [26] and MaskCLIP [60] features from two input views and evaluate open-vocabulary segmentation on target views. Our method generates fewer Gaussians while outperforming feed-forward methods and achieving comparable results to per-scene optimization methods trained with substantially more posed inputs. ∗: Features directly extracted from target view images*

定性结果（Figure 5）进一步验证了这一优势：C3G 渲染的新视图具有更高的保真度，且分割图与真值更为一致，而逐像素方法因跨视图特征不一致性产生了明显的分割伪影。

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of 3D scene understanding on ScanNet [7]. We conduct qualitative comparison for 3D scene understanding via novel view synthesis and open-vocabulary segmentation. When compared to both per-scene optimization ((a), (b)) and feed-forward ((c), (d)) methods, ours show the most high-fidelity renderings and accurate segmentation maps compared to the ground-truth*

### 多视图对应估计

C3G-F 学习的跨视图一致特征在对应估计任务中展现出强大泛化能力。在 ScanNet 上，C3G 的特征聚合策略在 VGGT-Tracking、DINOv2 和 DINOv3 三种特征骨干上均显著提升了 PCK@10px 指标（Table 4），证明注意力权重复用机制有效消除了多视图特征的不一致性。

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/009_Table_4.jpg]]
*Table 4: Correspondence estimation on ScanNet [7]. We evaluate PCK@10px across two images from different angles. Our feature aggregation significantly improves correspondence accuracy across the VGGT-Tracking, DINOv2, and DINOv3*

### 关键消融实验

**渐进式低通滤波与编码器解冻**（Table 5）：这是训练稳定性的关键设计。消融实验表明，同时移除渐进式低通滤波（从 s=300 退火至 s=0.3）和编码器冻结策略将导致模型崩溃，验证了两者对收敛的必要性。单独缺失任一组件的性能也显著下降。

**高斯数量**（Table 6）：重建质量随高斯数量增加而提升，在 2048 时达到最优。继续增加到 4096 时 PSNR 反而下降，暗示过多的查询 token 可能引入优化困难或过拟合。这一发现为紧凑表示的设计提供了明确的上界参考。

**C3G-F 特征解码器**（Table 7）：即使不采用自动编码器压缩，C3G-F 也能取得与压缩方法相似的 mIoU 和更高的 PSNR，验证了紧凑表示本身即可避免信息压缩损失，无需额外的降维手段。

**视觉编码器选择**（Table 8）：VGGT 作为默认编码器显著优于其他选择，这归因于其预训练过程中习得的丰富几何先验，为查询 token 的跨视图聚合提供了高质量的特征基础。

### 失败模式与局限性

尽管 C3G 在紧凑性上优势显著，但训练时依赖已知的目标相机姿态进行新视图渲染损失计算，限制了在完全无姿态场景下的前馈应用。当前解决方案是引入测试时优化来补偿姿态缺失，但这增加了推理成本。此外，紧凑高斯表示在捕捉高复杂场景的精细细节时存在上限——当高斯数量受限时 PSNR 会下降，表明极少数量的高斯可能无法覆盖场景中的所有高频信息。C3G-F 的特征解码器依赖已训练好的 C3G-G 注意力权重，无法与高斯解码器联合端到端训练，这限制了灵活性和可能的联合优化收益。

### 补充图表

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/010_Table_5.jpg]]
*Table 5: Ablation studies for C3G-G on RealEstate10K [62]*

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/011_Table_7.jpg]]
*Table 7: Ablation studies for C3G-F on Scannet [7]*

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/012_Table_6.jpg]]
*Table 6: Ablation studies on the number of Gaussian*

![[assets/figures/papers/paper_list_l2535_https_openaccess_thecvf_com_content_CVPR2026_html_An_Learning_Compact_3D/figures/013_Table_8.jpg]]
*Table 8: Ablation stuides on visual encoder choice*

## 方法谱系与知识库定位

### 与前馈式密集高斯预测方法的对比

C3G 的核心突破在于将逐像素高斯预测范式转变为基于查询 token 的紧凑生成范式。现有前馈式方法如 **LSM** 和 **NoPo** 遵循“每像素一个或多个高斯”的策略，直接从图像特征图的每个空间位置回归高斯属性。这一设计导致两个根本性问题：其一，大量高斯原语落在非必要区域，产生严重冗余——LSM 通常生成约 130K 个高斯，而 C3G 仅需约 2K 个（减少约 65 倍）；其二，不同视图独立预测的高斯在空间上无法对齐，造成多视图特征提升时的信息冲突与压缩损失。

C3G 通过引入 N 个可学习查询 token，利用 Transformer 的全局自注意力机制跨视图聚合信息，使每个 token 自发学会关注空间一致的区域（见 Figure 3 的注意力可视化）。这种“场景抽象”能力使得生成的高斯天然具有跨视图一致性，从根本上消除了逐像素方法的冗余与对齐问题。实验表明，在 ScanNet 开放词汇分割任务中，C3G 以更少高斯超越了 LSM（mIoU 0.513 vs 0.503），验证了紧凑表示对下游任务的优势。

### 与紧凑特征场方法的对比

**CF3** 是另一类追求紧凑性的方法，通过将密集特征压缩为少量特征场来降低存储开销。C3G 的紧凑性来源与之不同：CF3 在已生成的密集表示上进行后验压缩，而 C3G 在前馈推理阶段即直接生成紧凑高斯，避免了“先生成冗余再压缩”的信息损失路径。从结果看，C3G 在更少高斯数量下实现了更高的新视图合成质量与分割精度，表明前馈式紧凑生成比后验压缩更具优势。

### 与逐场景优化方法的对比

逐场景优化方法如 **Feature-3DGS** 通过对每个场景进行迭代优化来获得高质量高斯表示，通常需要大量已知姿态的输入视图。C3G 作为前馈式方法，仅需 2 个输入视图即可一次性推理出场景表示，在推理效率上具有数量级优势。值得注意的是，C3G 在 ScanNet 和 Replica 上的开放词汇分割性能已经超越或持平于使用更多姿态输入的逐场景优化方法（见 Table 2、Table 3），表明学习到的紧凑表示具有强大的泛化能力。若对 C3G 的输出高斯进行短时测试时优化（TTO），新视图合成质量可进一步提升至 30.250 PSNR（RealEstate10K 36 视图设置），同时仅使用 26K 高斯。

### 与 VGGT+NoPo 组合基线的对比

论文将 VGGT 编码器与 NoPo 高斯预测头组合作为直接基线，以剥离编码器选择的影响。C3G 使用相同的 VGGT 编码器，但在高斯解码策略上的差异带来了显著提升：ScanNet 上新视图合成 PSNR 从 21.262 提升至 23.612（+2.35）。这直接归因于查询 token 机制替代逐像素预测所带来的冗余消除与跨视图一致性。

### 适用边界与局限

1. **训练时依赖目标姿态**：C3G 的训练需要已知目标相机姿态以计算新视图合成损失。在完全无姿态场景下，前馈应用受限，可能需要测试时优化来补偿。这是当前前馈式高斯方法（包括 NoPo）的共性局限。

2. **高复杂场景的细节捕捉**：紧凑高斯表示（约 2K 个）在捕捉精细几何细节方面存在上限。消融实验显示，将高斯数量从 2048 增加到 4096 时，重建质量反而下降（Table 6），表明当前架构在更高斯数量下的优化存在瓶颈。对于需要极高保真度的应用场景，逐场景优化方法可能仍具优势。

3. **C3G-F 的训练耦合性**：C3G-F 特征解码器依赖于已训练好的 C3G-G 注意力权重，且这些权重在特征训练阶段被冻结。这种两阶段训练策略虽然保证了特征一致性，但限制了联合优化的灵活性，可能阻碍端到端性能的进一步提升。

4. **编码器依赖性**：视觉编码器的选择对性能影响显著（Table 8）。C3G 默认使用 VGGT 编码器，其强大的几何先验是紧凑高斯生成的关键支撑。若替换为较弱的编码器，查询 token 的注意力学习可能退化，导致紧凑性优势减弱。

### 开放问题

- **动态场景扩展**：C3G 的查询 token 机制天然适合建模场景级抽象，但其在动态场景（如运动物体、时变外观）下的紧凑表示能力尚未验证。查询 token 能否同时编码时空一致性是一个值得探索的方向。

- **零样本高质量合成**：当前方法在无 TTO 时的新视图合成质量与逐场景优化方法仍有差距。如何完全消除测试时优化，实现零样本高质量新视图合成，是前馈式方法走向实用的关键挑战。

- **注意力模式的跨表示迁移**：C3G 学习到的注意力模式本质上是场景几何与外观的隐式编码。这些模式能否迁移到其他三维表示（如 NeRF、体素网格）中，作为通用场景先验，是一个开放的理论问题。

- **多模态感知的潜力**：紧凑高斯表示在视觉任务中展现了效率与精度的平衡。其在触觉、音频等多模态感知任务中的适用性，以及查询 token 能否学习跨模态的场景抽象，有待进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Compact_3D_Representations_from_Feed_Forward_Novel_View_Synthesis.pdf]]