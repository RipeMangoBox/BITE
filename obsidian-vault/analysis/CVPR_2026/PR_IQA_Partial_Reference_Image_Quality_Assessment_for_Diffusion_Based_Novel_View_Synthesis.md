---
title: "PR-IQA: Partial-Reference Image Quality Assessment for Diffusion-Based Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PR_IQA_Partial_Reference_Image_Quality_Assessment_for_Diffusion_Based_Novel_View_Synthesis.pdf
project_link: null
code_link: null
aliases:
- PIPRIQA
- PR-IQA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于几何对齐的局部质量图（部分参考）作为可靠锚点，通过参考条件交叉注意力网络将质量评估传播至全图，使模型能够在无真值监督下实现类似全参考的质量评估精度。
primary_logic: 将跨视图质量评估重新定义为质量补全问题：先利用多视图几何计算重叠区域的部分质量图，再通过三流交叉注意力编码器-解码器网络补全全图质量，从而突破传统CR-IQA无法评估非重叠区域的盲区，并在无真值监督下达到全参考级别的精度。
claims:
- PR-IQA在Mip-NeRF 360、Tanks and Temples和RealEstate10K三个数据集上，OursDINOv2的PLCC分别达到0.555、0.573、0.453，均大幅超越所有交叉参考基线（如PuzzleSim最高0.351），并且OursSSIM在SSIM目标上也显著优于CrossScore等基线。
- 消融实验表明，去除部分质量图会导致比去除参考图像更大的性能下降，确认部分质量图是模型最关键的输入。
- 在质量感知3DGS上，PR-IQA指导的训练在PSNR、SSIM、LPIPS上均优于其他IQA方法，证明了该质量图在下游重建任务中的实际有效性。
- 即使仅使用一张参考图像，PR-IQA仍能超越多个参考下的其他学习方法，展示了其鲁棒性。
---

# PR-IQA: Partial-Reference Image Quality Assessment for Diffusion-Based Novel View Synthesis

> [!tip] 核心洞察
> 将跨视图质量评估重新定义为质量补全问题：先利用多视图几何计算重叠区域的部分质量图，再通过三流交叉注意力编码器-解码器网络补全全图质量，从而突破传统CR-IQA无法评估非重叠区域的盲区，并在无真值监督下达到全参考级别的精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | PR-IQA：面向扩散模型新视图合成的部分参考图像质量评估 |
| 英文题名 | PR-IQA: Partial-Reference Image Quality Assessment for Diffusion-Based Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04576) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PR-IQA (Partial-Reference Image Quality Assessment) |
| Dataset | Mip-NeRF 360, Tanks and Temples, RealEstate10K |

> [!tip] 效果简介
> - Mip-NeRF 360 上，PLCC (DINOv2-SIM) 0.555 (Ours_DINOv2) vs 0.304 (PuzzleSim) (+0.251)；PLCC (SSIM) 0.535 (Ours_SSIM) vs 0.290 (CrossScore) (+0.245)。
> - Tanks and Temples 上，PLCC (DINOv2-SIM) 0.573 (Ours_DINOv2) vs 0.351 (PuzzleSim) (+0.222)；PLCC (SSIM) 0.625 (Ours_SSIM) vs 0.444 (CrossScore) (+0.181)。
> - RealEstate10K 上，PLCC (DINOv2-SIM) 0.453 (Ours_DINOv2) vs 0.410 (PuzzleSim) (+0.043)。

## 概要

### 问题与瓶颈

基于扩散模型的新视图合成（NVS）能够从稀疏输入生成任意视角的伪真值（pseudo-GT）图像，但这些生成视图普遍存在难以检测的光度与几何不一致（如模糊、错位、伪影），严重制约了下游3D重建的质量。现有的图像质量评估（IQA）方法在此场景中均存在根本性缺陷：全参考（FR）方法需要像素对齐的真值图像，在实际NVS中不可用；无参考（NR）方法仅依赖单图统计特征，无法感知跨视图的几何一致性；交叉参考（CR）方法虽可利用其他真实视角作为参考，但现有CR-IQA方法（如PuzzleSim、CrossScore）仅评估视图间的重叠区域，对非重叠区域的生成质量完全盲视，导致在稀疏视图3D重建中误用低质量信号。

### 核心思路

PR-IQA将跨视图质量评估重新定义为**质量补全问题**：首先利用多视图几何将参考视图的特征变形至查询视图，在重叠区域计算可靠的部分质量图（Partial Quality Map）；随后通过一个三流交叉注意力编码器-解码器网络，以参考图像为条件，将部分质量图传播至全图，生成密集的像素级质量图。这一设计使模型能够在无真值监督的条件下，达到与全参考方法相当的评估精度。

### 方法定位

PR-IQA属于**部分参考图像质量评估（Partial-Reference IQA）**方法，其核心创新在于：

- **质量评估范围**：从仅评估重叠区域的部分质量图，扩展为覆盖全图的密集质量图。
- **参考利用机制**：从基于补丁相似性（如CrossScore）或单一特征比较（如PuzzleSim）的浅层对齐，升级为参考条件交叉注意力注入多尺度编码器的显式跨视图特征对齐。
- **下游应用策略**：提出图像级最优选择与像素级阈值掩码的双重过滤策略，将质量图转化为3D高斯泼溅（3DGS）训练的有效监督信号。

在IQA方法谱系中，PR-IQA填补了CR-IQA无法评估非重叠区域的空白，同时避免了FR-IQA对真值图像的依赖和NR-IQA对跨视图几何的无知。

### 主要结果

PR-IQA在三个标准数据集上全面超越现有CR-IQA基线。以DINOv2特征相似度为评估目标时，在Mip-NeRF 360上PLCC达到0.555（PuzzleSim为0.304），在Tanks and Temples上达到0.573（PuzzleSim为0.351），在RealEstate10K上达到0.453（PuzzleSim为0.410）。以SSIM为目标时同样显著优于CrossScore等基线（Table 1）。消融实验确认，部分质量图是模型最关键输入，其移除导致的性能下降甚至超过移除参考图像（Table 2）。在质量感知3DGS重建任务中，PR-IQA指导的训练在PSNR、SSIM、LPIPS上均优于其他IQA方法，验证了质量图在下游应用中的实际有效性（Table 3）。

### 问题背景：扩散生成伪GT的“不可见”缺陷

稀疏视图三维重建与新颖视图合成（Novel View Synthesis, NVS）的核心挑战在于输入视图数量极度有限。近年来，基于扩散模型的视图生成器（如ViewCrafter）能够从稀疏输入中生成大量伪真值（pseudo-GT）视图，为3D重建提供稠密的监督信号。然而，这些扩散生成的伪GT视图并非完美——它们经常包含难以检测的光度不一致（如模糊、伪影）和几何不一致（如结构扭曲、错位），如图1(a)所示。

这些缺陷之所以“不可见”，是因为在没有真实真值图像的情况下，我们缺乏有效手段来评估生成视图的质量。若将这些低质量伪GT不加区分地用于下游3D重建，会直接导致重建结果出现模糊、几何畸变和纹理混叠等严重问题。因此，**在无真值监督的条件下，对扩散生成视图进行准确的质量评估，是保障稀疏视图3D重建质量的关键前提**。

### 现有IQA方法的局限性

图像质量评估（Image Quality Assessment, IQA）方法按参考信息的使用方式可分为三类，但它们在NVS场景中均存在根本性不足：

- **全参考IQA（FR-IQA）**：如PSNR、SSIM、LPIPS、DINOv2-SIM等，需要像素对齐的真值图像作为参考。在实际NVS场景中，真值图像不可得，因此这类方法无法直接应用。
- **无参考IQA（NR-IQA）**：如PAL4VST、PaQ-2-PiQ、PIQE等，仅从单张图像本身评估质量。然而，扩散模型生成的伪影（如局部模糊、纹理合成错误）往往难以与真实图像内容区分，NR-IQA缺乏跨视图的几何与光度一致性信息，评估精度严重受限。
- **交叉参考IQA（CR-IQA）**：如MEt3R、CrossScore、PuzzleSim等，利用来自其他视角的真实图像作为参考来评估查询视图的质量。这是NVS场景中最有前景的方向，因为稀疏输入中天然存在可用的真实参考视图。

然而，现有CR-IQA方法存在一个**根本性盲区**：

> **所有现有CR-IQA方法仅能评估查询视图与参考视图之间的重叠区域，无法对非重叠区域的质量进行有效评估。**

这一限制源于其核心设计：现有方法通过比较查询视图与参考视图在共视区域的补丁相似性或特征一致性来推断质量。当扩散模型生成查询视图中包含参考视图无法观测到的区域（如场景背面、遮挡解除后的新区域）时，这些方法完全失效。在稀疏视图3D重建中，非重叠区域恰恰是扩散模型最容易产生严重伪影（如物体凭空出现、结构幻觉）的地方，现有CR-IQA方法无法识别这些区域的低质量信号，导致重建过程误用不可靠的监督。

### 核心动机：从“部分评估”到“质量补全”

本文的核心洞察在于对CR-IQA问题的重新定义：

> **将跨视图质量评估重新定义为“质量补全”问题：先利用多视图几何计算重叠区域的部分质量图，再通过学习将质量评估传播至全图。**

这一重新定义的关键在于认识到：虽然非重叠区域无法通过直接比较来评估，但重叠区域提供的部分质量信息可以作为“可靠锚点”——扩散模型在同一张生成图像中的质量分布往往具有空间连续性，重叠区域的低质量信号通常预示着相邻非重叠区域也存在问题。因此，**通过几何对齐获得的部分质量图，结合参考图像的视觉线索，可以学习性地补全出全图的质量分布**。

基于这一动机，本文提出**PR-IQA（Partial-Reference Image Quality Assessment）**，其核心设计包含两个阶段：

1. **部分质量图生成**：利用多视图几何估计（VGGT）建立查询视图与参考视图之间的稠密对应关系，将参考视图的DINOv2语义特征变形至查询视图，在重叠区域计算归一化余弦相似度，得到几何一致的部分质量图$\hat{Q}$。
2. **质量补全网络**：设计三流编码器-解码器架构，以参考条件交叉注意力机制为核心，将查询图像、参考图像和部分质量图三路信息进行多尺度融合，最终输出全图密集质量图$Q$。

通过这一设计，PR-IQA能够在**无真值监督**的条件下，实现对扩散生成视图全图质量的准确评估，突破传统CR-IQA无法评估非重叠区域的盲区，并在下游质量感知3DGS重建中提供可靠的像素级置信度指导。

## 核心方法与创新机理

PR-IQA的核心创新在于将跨视图质量评估重新定义为一个**质量补全问题**，并通过三个紧密耦合的机制突破现有交叉参考IQA方法的根本局限。

### 1. 从部分观察到全局补全的范式转换

现有交叉参考IQA方法（如CrossScore、PuzzleSim）的根本瓶颈在于**仅能评估参考视图与查询视图之间的重叠区域**。当扩散模型生成的新视图包含大量与参考视图无几何对应的非重叠区域时，这些方法完全失效，无法判断生成内容的质量。PR-IQA的关键洞察是：将这一局限转化为一个可控的补全问题——利用多视图几何建立重叠区域的可靠质量锚点，再通过网络学习将质量评估传播至全图。

具体而言，PR-IQA将质量评估拆分为两个阶段：
- **部分质量图生成**：利用VGGT建立3D对应关系，将参考视图的DINOv2特征变形至查询视图，在重叠区域计算归一化余弦相似度，得到几何一致的部分质量图 $\hat{Q}$。
- **质量补全**：将部分质量图作为可靠锚点，通过网络补全非重叠区域的质量分数，输出全图密集质量图 $Q$。

这一范式转换使PR-IQA能够在**无真值监督**的条件下，实现与全参考IQA方法相当的评估精度。

### 2. 参考条件交叉注意力：跨视图证据显式对齐

传统交叉参考方法通常依赖补丁相似度或单一特征比较，缺乏对跨视图语义对应的显式建模。PR-IQA设计了**三流编码器-解码器架构**，其核心是参考条件交叉注意力机制：

- **参考流**通过自注意力提取多尺度特征 $F_r^s$；
- **查询流**和**部分质量流**以参考特征为键值进行交叉注意力更新：
  $$\hat{F}_q^s = \mathrm{Enc}_{\mathrm{cross}}^{q,s}(F_q^{s-1}; F_r^s), \quad F_p^s = \mathrm{Enc}_{\mathrm{cross}}^{p,s}(F_p^{s-1}; F_r^s)$$
- 每层编码器后，查询特征与部分质量特征通过通道拼接卷积融合：
  $$F_q^s = \mathrm{ConvFuse}(\hat{F}_q^s, F_p^s)$$

这种设计使网络能够在**每个尺度**上显式对齐跨视图特征，将参考视图的语义信息系统性地注入质量补全过程。消融实验（Table 2）证实，完整的双门控注意力块（通道注意力+空间注意力）相较于仅使用单一注意力或简化的CBAM变体，在SRCC上提升尤为明显。

### 3. 伪GT双重过滤：图像级选择与像素级掩码

在质量感知3DGS训练中，PR-IQA引入了一种**双重过滤策略**，同时从图像级和像素级两个粒度过滤低质量伪GT信号：

- **图像级选择**：对每个训练视角，从扩散模型生成的多个候选视图中选择平均质量分数最高的图像：
  $$(\tilde{I}_v, \tilde{Q}_v) = \underset{(I_{v,n}, Q_{v,n}) \in \mathbb{Z}_v}{\mathrm{argmax}} (S_{v,n})$$
- **像素级掩码**：基于质量图阈值 $\tau$ 生成二值置信掩码，仅在高置信区域计算损失：
  $$M(p) = \mathbf{1}(Q(p) \geq Q_{\tau})$$

消融实验表明，掩码阈值 $\tau=50$ 在过滤伪影与保留足够监督信号之间取得最佳平衡（Table 12），且二值掩码与软权重策略的重建性能相当，验证了PR-IQA质量图提供的监督信号具有鲁棒性（Table 13）。

### 4. 关键创新与性能提升的因果关联

上述三个创新形成了紧密的因果链条：部分质量图提供了可靠的几何锚点（消融实验证实去除部分质量图导致的性能下降甚至大于去除参考图像），参考条件交叉注意力实现了跨视图证据的高效传播，双重过滤策略则将质量评估有效转化为下游重建的监督信号。这一链条使PR-IQA在Mip-NeRF 360、Tanks and Temples和RealEstate10K三个数据集上，OursDINOv2的PLCC分别达到0.555、0.573、0.453，均大幅超越所有交叉参考基线（PuzzleSim最高仅0.351），并在质量感知3DGS的PSNR、SSIM、LPIPS上全面优于其他IQA方法（Table 3）。

PR-IQA 的整体 pipeline 由两个核心阶段串联构成：**部分质量图生成** 与 **全图质量补全**，并在下游任务中扩展为 **质量感知的 3DGS 训练** 流程（Figure 1）。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed PR-IQA and quality-aware 3DGS. (a) Diffusion models generate novel views (pseudo-GTs) from sparse inputs, which often contain photometric or geometric artifacts. (b) We propose PR-IQA, a cross-reference method predicting a dense, pixel-level quality map from unaligned references. It produces a complete map correlating closely with FR-IQA metrics (e.g., DINOv2 feature-similarity map) without requiring a GT. (c) This quality map enables a dual-filtering strategy (image selection and pixel masking) for 3DGS training, reducing reconstruction errors and improving fidelity*

### 第一阶段：部分质量图生成

给定一对未对齐的查询视图 $I_q$（扩散模型生成的伪 GT）与参考视图 $I_r$（真实图像），系统首先利用 **VGGT** 建立两者间的稠密 3D 几何对应关系。随后，将参考视图的 DINOv2 特征通过该对应关系变形至查询视图坐标下，得到对齐后的参考特征 $F_{r \to q}^{\mathrm{DINO}}$。在重叠区域内，逐像素计算查询特征与变形参考特征之间的归一化余弦相似度，生成**部分质量图** $\hat{Q}$：

$$\hat{Q}(i) = \mathrm{CosSim}(F_q^{\mathrm{DINO}}(i), F_{r \to q}^{\mathrm{DINO}}(i))$$

其中 $\mathrm{CosSim}(\mathbf{u}, \mathbf{v}) = \frac{1}{2} \left( \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} + 1 \right)$，将相似度映射至 $[0, 1]$ 区间。该部分质量图仅在几何可对应的重叠区域具有可靠分数，非重叠区域则存在大面积盲区——这正是现有交叉参考 IQA 方法无法逾越的根本瓶颈。

### 第二阶段：全图质量补全

为解决上述盲区问题，PR-IQA 将跨视图质量评估重新定义为**质量补全问题**：以部分质量图为可靠锚点，通过参考条件交叉注意力网络将质量评估传播至全图。该质量补全网络采用**三流编码器-解码器架构**（Figure 2），包含三条并行的特征流：

- **参考流**：对参考图像 $I_r$ 进行自注意力编码，提取多尺度参考特征 $F_r^s$；
- **查询流**：以参考特征为键值对查询图像 $I_q$ 进行交叉注意力编码，生成跨视图对齐后的查询特征 $\hat{F}_q^s$；
- **部分质量流**：同样以参考特征为键值对部分质量图 $\hat{Q}$ 进行交叉注意力编码，提取质量上下文特征 $F_p^s$。

在每个编码器尺度 $s$ 上，查询流与部分质量流的输出通过通道拼接后卷积融合：

$$F_q^s = \mathrm{ConvFuse}(\hat{F}_q^s, F_p^s)$$

编码器共包含三个下采样阶段，最终融合特征 $F_q^3$ 经解码器上采样恢复至全分辨率，输出密集的**全图质量图** $Q$：

$$Q = \mathrm{Dec}(F_q^3)$$

各编码器/解码器阶段的核心模块为**双门控注意力块**，在通道注意力和空间注意力两个维度上对特征进行选择性增强。该设计使得模型能够在无真值监督的条件下，实现类似全参考 IQA 的评估精度。

### 第三阶段：质量感知 3DGS 训练

在全图质量图的基础上，PR-IQA 进一步指导 3D Gaussian Splatting 的重建优化。具体而言，采用**双重过滤策略**：

1. **图像级选择**：对每个训练视角的多个候选伪 GT 图像，选取平均质量分数最高者作为训练目标；
2. **像素级掩码**：基于质量图阈值 $\tau$ 生成二值置信掩码 $M(p) = \mathbf{1}(Q(p) \geq Q_{\tau})$，仅在高置信区域计算 L1 损失，联合 SSIM 项构成最终优化目标。

该策略有效抑制了扩散生成伪 GT 中的光度与几何不一致对重建的负面影响，使 3DGS 能够聚焦于可靠区域进行优化。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/008_Figure_5.jpg]]
*Figure 5: Detailed architecture of the proposed model. The network employs an encoder–decoder design featuring cross- and self-attention modules, query fusion, and mask-aware pixel-shuffle downsampling. Key specifications, including stage-wise block counts, attention heads, and the status of component sharing (frozen vs. trainable), are explicitly annotated*

PR-IQA 的核心创新在于将跨视图质量评估重新定义为**质量补全问题**：首先利用多视图几何约束在重叠区域计算可靠的部分质量锚点，再通过参考条件交叉注意力网络将质量评估传播至全图。整个流程由三个关键模块串联构成。

### 1. 部分质量图生成器（Partial Quality Map Generator）

该模块的目标是在查询视图 $I_q$ 与参考视图 $I_r$ 的**可见重叠区域**内，建立像素级的几何对应关系，并计算局部质量分数。

**核心机制**：利用 VGGT 等几何估计模块建立 3D 对应关系，将参考视图的 DINOv2 特征 $F_r^{\mathrm{DINO}}$ 变形（warp）至查询视图坐标系，得到对齐后的特征 $F_{r \to q}^{\mathrm{DINO}}$。随后，在重叠区域的每个像素 $i$ 处，计算查询特征与变形参考特征的归一化余弦相似度，作为该像素的部分质量估计：

$$\hat{Q}(i) = \mathrm{CosSim}\left(F_q^{\mathrm{DINO}}(i),\; F_{r \to q}^{\mathrm{DINO}}(i)\right)$$

其中归一化余弦相似度定义为：

$$\mathrm{CosSim}(\mathbf{u}, \mathbf{v}) = \frac{1}{2} \left( \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|} + 1 \right)$$

该映射将相似度值归一化至 $[0, 1]$ 区间。$\hat{Q}$ 即为**部分质量图**——它在几何可靠的重叠区域提供了高质量锚点，但在非重叠区域存在大量缺失值（无效区域）。

**关键洞察**：部分质量图 $\hat{Q}$ 是后续质量补全网络的**最核心输入**。消融实验（Table 2）表明，移除部分质量图导致的性能下降甚至超过移除参考图像，确认了其作为可靠锚点的关键地位。

### 2. 质量补全网络（Quality Completion Network）

该模块将稀疏的部分质量图 $\hat{Q}$ 补全为覆盖全图的密集质量图 $Q$。其架构为**三流编码器-解码器**，核心是参考条件交叉注意力机制。

**三流设计**：
- **参考流**：处理参考图像 $I_r$，通过自注意力提取多尺度参考特征 $F_r^s$
- **查询流**：处理查询图像 $I_q$，以参考特征为键值进行交叉注意力
- **部分质量流**：处理部分质量图 $\hat{Q}$，同样以参考特征为键值进行交叉注意力

**多尺度编码器更新**（$s = 0, 1, 2, 3$ 表示编码器层级）：

$$F_r^s = \mathrm{Enc}_{\mathrm{self}}^{r,s}(F_r^{s-1})$$

$$\hat{F}_q^s = \mathrm{Enc}_{\mathrm{cross}}^{q,s}(F_q^{s-1}; F_r^s)$$

$$F_p^s = \mathrm{Enc}_{\mathrm{cross}}^{p,s}(F_p^{s-1}; F_r^s)$$

参考流通过自注意力独立提取特征；查询流和部分质量流则通过**参考条件交叉注意力**显式对齐跨视图特征——查询特征和部分质量特征作为 Query，参考特征作为 Key/Value，使模型能够从参考视图中检索相关证据来推断查询视图的质量。

**特征融合**：在每个编码器层级，查询流输出 $\hat{F}_q^s$ 与部分质量流输出 $F_p^s$ 通过通道拼接后卷积融合：

$$F_q^s = \mathrm{ConvFuse}(\hat{F}_q^s,\; F_p^s)$$

**解码器**：融合后的最高层特征 $F_q^3$ 通过解码器逐步上采样，最终输出全分辨率质量图：

$$Q = \mathrm{Dec}(F_q^3)$$

**双门控注意力块**：每个编码器/解码器层级内部采用双门控注意力块（源自 CBAM），同时包含通道注意力和空间注意力分支。消融实验（Table 2）显示，完整的双门控设计在 SRCC 上显著优于仅使用单一注意力或简化变体。

### 3. 训练损失函数

PR-IQA 的训练目标由三项损失的加权组合构成：

$$\mathcal{L} = \lambda_{\mathrm{IQA}} \mathcal{L}_1^{\mathrm{IQA}} + \lambda_{\mathrm{JSD}} \mathcal{L}_{\mathrm{JSD}} + \lambda_{\mathrm{PLCC}} \mathcal{L}_{\mathrm{PLCC}}$$

- **$\mathcal{L}_1^{\mathrm{IQA}}$**：预测质量图与真值质量图（如 DINOv2-SIM 或 SSIM 图）之间的 L1 损失，权重 $\lambda_{\mathrm{IQA}} = 0.5$
- **$\mathcal{L}_{\mathrm{JSD}}$**：Jensen-Shannon 散度损失，用于对齐预测质量分布与真值分布，权重 $\lambda_{\mathrm{JSD}} = 1.0$
- **$\mathcal{L}_{\mathrm{PLCC}}$**：Pearson 线性相关系数损失，直接优化全局相关性，权重 $\lambda_{\mathrm{PLCC}} = 0.25$

**关键消融**：去除 JSD 损失会导致 PLCC 和 SRCC 变为负值（Table 9），表明分布对齐对训练至关重要——仅靠像素级 L1 和相关性损失无法使模型收敛到有意义的解。

### 4. 质量感知 3DGS 训练中的公式

PR-IQA 输出的质量图被用于指导 3D Gaussian Splatting 的重建优化，通过双重过滤策略抑制伪 GT 中的低质量信号。

**伪 GT 选择**：对每个训练视角 $v$，从多个候选生成视图中选择平均质量分数最高的图像及其质量图：

$$(\tilde{I}_v, \tilde{Q}_v) = \underset{(I_{v,n}, Q_{v,n}) \in \mathbb{Z}_v}{\mathrm{argmax}} (S_{v,n})$$

其中 $S_{v,n}$ 为候选图像 $I_{v,n}$ 的平均质量分数。

**二值置信掩码**：基于质量图阈值 $Q_{\tau}$ 生成像素级掩码，仅在高置信区域计算损失：

$$M(p) = \mathbf{1}(Q(p) \geq Q_{\tau})$$

实验设定 $\tau = 50$（即保留质量分数前 50% 的像素），该阈值在过滤伪影与保留足够监督信号之间取得最佳平衡（Table 12）。

**质量感知损失**：3DGS 训练的总损失仅在掩码区域计算 L1 损失，并联合 SSIM 项：

$$\mathcal{L}_{\mathrm{total}} = \sum_{k=1}^{|\mathcal{Z}_{\mathrm{train}}|} \left( (1-\lambda_{\mathrm{dssim}}) \mathcal{L}_{1,k}^{\mathrm{3DGS}} + \lambda_{\mathrm{dssim}} \mathcal{L}_{\mathrm{dssim}}(\hat{I}_k, I_k) \right)$$

其中 $\lambda_{\mathrm{dssim}} = 0.2$。消融实验（Table 13）表明，二值掩码与软加权策略（$W(p) = Q(p)$ 直接作为损失权重）的重建性能相当，验证了 PR-IQA 质量图提供的监督信号具有鲁棒性。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/002_Figure_2.jpg]]
*Figure 2: (a) Overview of the PR-IQA pipeline. The framework operates in two stages. First, we warp DINOv2 features from the reference*

## 实验与关键发现

### 实验设置概述

PR-IQA在三个多视图数据集上进行评估：**Mip-NeRF 360**（室内外场景）、**Tanks and Temples**（复杂户外场景）和**RealEstate10K**（房地产场景）。评估场景的完整列表见Table 5。训练使用ViewCrafter扩散模型生成的伪GT视图，真值质量图由全参考IQA指标（DINOv2特征相似度和SSIM）计算得到。评价指标采用PLCC（Pearson线性相关系数）和SRCC（Spearman秩相关系数），衡量预测质量图与真值质量图之间的相关性。所有排名均排除全参考（FR）方法，因为FR方法依赖像素对齐的真值图像，在实际NVS场景中不可用。

### 主实验结果

Table 1报告了PR-IQA与各类IQA基线在不同数据集和目标指标上的定量比较。核心发现如下：

**在DINOv2-SIM目标上**，Ours_DINOv2在所有三个数据集上均取得最优结果：
- Mip-NeRF 360：PLCC达到**0.555**，SRCC达到**0.622**，分别领先最强交叉参考基线PuzzleSim **+0.251**和**+0.216**；
- Tanks and Temples：PLCC达到**0.573**，SRCC达到**0.638**，领先PuzzleSim **+0.222**和**+0.183**；
- RealEstate10K：PLCC达到**0.453**，SRCC达到**0.579**，领先PuzzleSim **+0.043**和**+0.071**。

**在SSIM目标上**，Ours_SSIM同样显著超越所有基线：
- Mip-NeRF 360：PLCC **0.535**，SRCC **0.556**，领先CrossScore **+0.245**和**+0.228**；
- Tanks and Temples：PLCC **0.625**，SRCC **0.592**，领先CrossScore **+0.181**和**+0.120**；
- RealEstate10K：PLCC **0.510**，SRCC **0.562**，领先CrossScore **+0.062**和**+0.069**。

值得注意的是，PR-IQA在无真值监督的条件下，其性能已接近甚至在某些指标上匹配全参考方法的水平（如Table 1中灰色标注的identity cases）。Figure 3的定性比较进一步显示，PR-IQA生成的质量图能忠实地恢复物体轮廓和精细结构，而基线方法（如CrossScore、PuzzleSim）在非重叠区域产生噪声或不一致的预测。

Table 6补充了以PSNR和LPIPS为目标的评估结果，PR-IQA在这些传统指标上同样保持领先，验证了方法的通用性。

### 消融实验

**架构组件消融（Table 2）**揭示了几个关键设计选择的重要性：

1. **部分质量图的关键性**：移除部分质量图（w/o partial map）导致性能大幅下降，PLCC从0.555降至0.309，SRCC从0.622降至0.334，降幅甚至超过移除参考图像（w/o reference）的变体。这确认了部分质量图是模型最关键的输入信号，验证了“质量补全”范式的核心假设。

2. **双门控注意力块的有效性**：完整的双门控注意力（通道注意力+空间注意力）相较于仅使用通道注意力（w/o spatial attn）、仅使用空间注意力（w/o channel attn）或简化的CBAM变体，在SRCC上提升尤为明显。这表明跨视图特征对齐需要同时在通道和空间两个维度上进行显式建模。

3. **损失函数的重要性（Table 9）**：去除JSD损失（w/o JSD loss）导致PLCC和SRCC变为负值，表明分布对齐损失对训练稳定性至关重要。去除PLCC损失（w/o PLCC loss）也会导致性能显著下降，验证了直接优化相关性指标的必要性。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/017_Table_9.jpg]]
*Table 9: Ablation study on the contribution of loss components. We compare the full model with variants trained without the JSD loss (w/o*

4. **训练目标的选择（Table 11）**：在质量感知3DGS中，采用DINOv2特征相似度作为指导目标，在PSNR、SSIM、LPIPS上均优于使用PSNR、SSIM或LPIPS自身作为指导目标。这验证了高级语义对齐相较于像素级指标在下游重建任务中的优越性。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/019_Table_11.jpg]]
*Table 11: Comparison of FR-IQA metrics as guidance signals for Quality-Aware 3DGS training. We evaluate the 3DGS modeling quality (PSNR, SSIM, LPIPS) when guiding the optimization using different IQA targets (PSNR, SSIM, LPIPS, and DINOv2). The results demonstrate that DINOv2 feature similarity consistently outperforms traditional metrics, even surpassing methods that directly optimize for the target metric itself, thereby justifying its selection as our primary prediction target*

**质量感知3DGS的消融（Table 12-13）**：
- 掩码阈值τ=50在过滤伪影与保留足够监督信号之间取得最佳平衡，优于τ=30（过于激进，丢失有效监督）和τ=70（过于保守，保留过多噪声）。
- 二值掩码与软权重策略的重建性能相当（Table 13），表明PR-IQA质量图提供的监督信号鲁棒，对具体掩码形式不敏感。

### 下游任务验证：质量感知3DGS

Table 3报告了不同IQA方法指导3DGS训练的重建质量。PR-IQA指导的训练在PSNR、SSIM、LPIPS上均优于其他IQA方法，包括全参考方法指导的变体。Figure 4的定性比较显示，基线方法产生伪影、模糊或未对齐的高斯体，而PR-IQA指导的方法避免了这些失败模式，产生更清晰、更连贯的重建结果。

图像选择评估（Table 7）进一步表明，PR-IQA的每图像质量分数与真值质量标量之间具有强相关性，在Tanks and Temples和RealEstate10K上取得最高性能。

![[assets/figures/papers/paper_list_l2574_https_arxiv_org_abs_2604_04576/figures/012_Table_7.jpg]]
*Table 7: Image selection evaluation. We report the correlation (PLCC, SRCC) between per-image quality scores and ground-truth quality scalars derived from DINOv2 feature similarity and SSIM across three datasets. OursDINOv2 demonstrates strong alignment with featurebased quality, achieving the highest performance on Tanks and Temples and RealEstate10K, and competitive results on Mip-NeRF 360*

### 鲁棒性与泛化分析

**参考视图数量的影响（Figure 6）**：即使仅使用一张参考图像，PR-IQA仍能超越多个参考下的其他学习方法（CrossScore、PuzzleSim），展示了其鲁棒性。随着参考视图数量增加，性能持续提升并逐渐接近全参考方法的上限。

**跨生成器泛化（Table 8）**：在未见过的生成器GEN3C和SEVA上，PR-IQA无需任何重新训练即可保持领先性能，验证了其作为即插即用模块的泛化能力。

**几何鲁棒性（Table 10）**：在VGGT深度置信度过滤和相机姿态噪声扰动下，PR-IQA始终优于基线方法（CrossScore、PuzzleSim），默认配置（20%深度过滤）取得最优性能，表明方法对几何输入质量具有较好的容忍度。

**低重叠场景（Table 14-15, Figure 8-9）**：在重叠率低至16%-22%的极端场景中，PR-IQA仍能有效评估非重叠区域的质量，而基线方法在这些区域产生大量误判。FPR@Top-X%指标（Table 15）量化了PR-IQA在非重叠区域误判率的显著降低。

### 失败模式与局限性

尽管PR-IQA在整体上表现优异，分析揭示了以下局限：

1. **训练目标的感知上限**：PR-IQA的训练目标来源于FR-IQA指标（DINOv2特征相似度或SSIM），这些代理指标并未完全捕捉人眼感知质量。在需要精细视觉评估的任务上，这一代理目标的偏差可能限制性能上限。

2. **几何依赖的脆弱性**：部分质量图$\hat{Q}$的生成依赖VGGT和稠密立体匹配的几何对应。在大面积无纹理区域或剧烈光照变化等极端场景中，几何对应可能失效，进而影响质量补全的可靠性。Table 10的几何扰动实验虽显示一定鲁棒性，但未覆盖所有退化模式。

3. **生成器和重建基元的覆盖范围**：实验验证主要基于ViewCrafter生成器和标准3DGS重建流程。Table 8虽展示了跨生成器泛化，但对更多样化的多视图扩散模型和新兴重建基元（如2DGS、Scaffold-GS）的通用性仍需进一步验证。

### 计算成本

Table 16报告了PR-IQA各组件及3DGS优化的平均运行时间和内存占用。部分质量图生成（VGGT推理+特征变形）和网络推理构成主要计算开销，但整体仍在可接受范围内，适合作为预处理步骤集成到现有管线中。

## 定位与知识库关联

### 1. 问题定位：从交叉参考到部分参考的范式迁移

PR-IQA 的核心贡献在于重新定义了交叉参考图像质量评估（CR-IQA）的问题边界。传统 CR-IQA 方法——如 **CrossScore**、**PuzzleSim** 和 **MEt3R**——均受限于一个根本性假设：参考视图与查询视图之间存在足够大的重叠区域，使得基于补丁相似性或特征比较的质量推断得以进行。这一假设在稀疏视图三维重建场景中频繁失效：扩散模型生成的伪GT视图往往包含大面积非重叠区域，这些区域的光度与几何一致性无法通过现有CR-IQA方法评估，形成“评估盲区”。

PR-IQA 将这一瓶颈转化为可操作的因果杠杆：**将跨视图质量评估重新定义为质量补全问题**。具体而言，方法首先利用多视图几何计算重叠区域的部分质量图（partial quality map），再通过参考条件交叉注意力网络将可靠的质量信号传播至全图。这一范式迁移的关键在于：部分质量图作为“几何锚点”，为后续的质量补全提供了无需真值监督的可靠基础。

### 2. 与基线方法的系统性差异

#### 2.1 与全参考IQA（FR-IQA）的关系

FR-IQA 方法（**PSNR**、**SSIM**、**LPIPS**、**DINOv2-SIM**）依赖像素对齐的真值图像，在实际新视图合成场景中不可用。PR-IQA 的创新之处在于：**在无真值监督的条件下，逼近FR-IQA的评估精度**。论文明确将FR-IQA指标作为训练目标（DINOv2特征相似度或SSIM），使模型学习预测与FR-IQA高度相关的质量图。Table 1 的实验结果表明，PR-IQA 在三个数据集上的PLCC显著超越所有CR-IQA基线，且与FR-IQA的差距大幅缩小——例如在Mip-NeRF 360上，Ours_DINOv2 的 PLCC 达到 0.555，而次优的 CR 方法 PuzzleSim 仅为 0.304。

#### 2.2 与无参考IQA（NR-IQA）的关系

NR-IQA 方法（**PAL4VST**、**PaQ-2-PiQ**、**PIQE**）完全不使用参考信息，仅从单张图像预测质量。这类方法在扩散生成伪GT的评估中面临根本性困难：生成伪影（如模糊、几何错位）往往在单张图像中难以检测，需要跨视图的一致性信息才能暴露。PR-IQA 通过引入部分参考（partial reference）——即几何对齐后的参考特征——弥补了这一信息缺口，同时避免了FR-IQA对像素对齐真值的依赖。

#### 2.3 与交叉参考IQA（CR-IQA）的核心差异

PR-IQA 与现有 CR-IQA 方法（**CrossScore**、**PuzzleSim**、**MEt3R**）的关键差异体现在三个维度：

| 维度 | 基线CR-IQA | PR-IQA |
|------|-----------|--------|
| **评估覆盖区域** | 仅重叠区域（部分质量图本身即为最终输出） | 全图密集质量图（通过质量补全网络扩展至非重叠区域） |
| **参考利用方式** | 基于补丁相似性或单一特征比较 | 参考条件交叉注意力注入多尺度编码器，显式对齐跨视图特征 |
| **伪GT过滤策略** | 无过滤或仅图像级得分 | 图像级最优选择 + 像素级阈值掩码的双重过滤 |

消融实验（Table 2）强有力地验证了这些设计选择的关键性：**移除部分质量图导致的性能下降甚至大于移除参考图像**，确认部分质量图是模型最关键的输入。这一发现颠覆了直觉——在CR-IQA中，参考图像通常被认为是最重要的信息源，但PR-IQA表明，经过几何对齐的部分质量图比原始参考图像提供了更直接、更可靠的质量信号。

### 3. 方法谱系中的技术渊源

PR-IQA 的技术架构融合了多个研究脉络的成果：

- **多视图几何与特征变形**：部分质量图的生成依赖 **VGGT** 建立的3D对应关系，将参考视图的 DINOv2 特征变形至查询视图。这一策略继承了基于几何对应进行跨视图特征对齐的传统，但将其应用于质量评估而非重建或匹配。

- **交叉注意力机制**：参考条件交叉注意力的设计借鉴了 Transformer 架构在多模态对齐中的成功经验（如跨模态注意力在视觉-语言模型中的应用），但将其适配于跨视图质量评估的特定需求——以参考特征为键值，引导查询特征和部分质量特征的更新。

- **双门控注意力块**：编码器中的双门控注意力块源自 **CBAM**（Convolutional Block Attention Module）的设计范式，但PR-IQA将其扩展为通道注意力与空间注意力的协同组合。消融实验表明，完整的双门控设计相较于仅使用单一注意力或简化变体，在SRCC上提升尤为明显。

- **质量感知三维重建**：PR-IQA 指导的 3DGS 训练策略与置信度感知的神经渲染方法（如基于不确定性的NeRF优化）共享哲学基础，但PR-IQA的关键创新在于使用**跨视图质量图**而非单视图不确定性作为置信度信号，从而更准确地识别扩散生成伪GT中的系统性伪影。

### 4. 适用边界与局限

#### 4.1 训练目标的代理性质

PR-IQA 的训练目标来源于 FR-IQA 指标（DINOv2 特征相似度或 SSIM），这些代理指标并未完全捕捉人眼感知质量。论文承认这一局限：**模型的上限受限于所选FR-IQA指标与人类主观质量评估之间的差距**。在需要精细视觉评估的任务上（如艺术风格保真度、语义一致性），当前训练目标可能不足以提供充分的监督信号。

#### 4.2 几何依赖的脆弱性

部分质量图 $\hat{Q}$ 的生成依赖 VGGT 和稠密立体匹配的几何对应，其可靠性在以下场景中可能显著下降：
- 大面积无纹理区域（如白墙、天空）
- 剧烈光照变化（如室内外过渡）
- 重复纹理或镜面反射表面

在这些极端场景中，几何对应的失效将直接导致部分质量图的噪声增加，进而影响质量补全的可靠性。论文的实验（Table 10）表明，PR-IQA 对几何噪声具有一定鲁棒性——在引入5%-10%的相机参数噪声后，性能仍优于 CrossScore 和 PuzzleSim——但这一鲁棒性的边界尚需在更极端的几何退化场景中验证。

#### 4.3 生成器与重建方法的泛化性

实验验证主要基于 **ViewCrafter** 生成器和标准 3DGS 重建流程。虽然论文在 Table 8 中展示了在 **GEN3C** 和 **SEVA** 两个未见生成器上的跨生成器泛化结果（无需重新训练），但对新兴的多视图扩散模型（如基于视频扩散的生成器）和重建基元（如 2DGS、3D Gaussian Splatting 变体）的通用性尚未全面评估。作为即插即用模块的泛化能力仍需在更广泛的生成-重建管线中验证。

### 5. 开放问题

1. **极端几何场景的鲁棒性边界**：在大面积无纹理区域或立体匹配完全失效的场景下，PR-IQA 的性能如何？是否可以通过引入语义先验或单目深度估计来补充几何对应？

2. **端到端联合优化的可能性**：当前几何对齐（VGGT）与质量估计（PR-IQA）是分离的两阶段流程。端到端联合训练是否会降低对外部几何估计模块的依赖，同时提升质量补全的精度？

3. **感知质量对齐**：如何将人类主观质量评价融入训练目标，以突破FR-IQA代理指标的上限？是否需要构建针对扩散生成伪影的专用主观质量数据集？

4. **多参考融合策略**：Figure 7 探索了四种质量图融合策略（Max、Min、Median、Mean），但最优策略是否随场景特性（如重叠率、纹理复杂度）自适应变化？是否存在学习式的融合机制？

5. **计算效率与实时性**：Table 16 报告了各模块的计算成本，但PR-IQA在实时或交互式应用场景（如在线3D重建）中的可行性仍需进一步优化。

## 原文 PDF

![[paperPDFs/CVPR_2026/PR_IQA_Partial_Reference_Image_Quality_Assessment_for_Diffusion_Based_Novel_View_Synthesis.pdf]]
