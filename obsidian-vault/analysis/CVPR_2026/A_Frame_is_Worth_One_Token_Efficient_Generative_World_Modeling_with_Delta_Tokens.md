---
title: "A Frame is Worth One Token: Efficient Generative World Modeling with Delta Tokens"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/A_Frame_is_Worth_One_Token_Efficient_Generative_World_Modeling_with_Delta_Tokens.pdf
aliases:
- DDTB
- FIWOTEGWMDT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过 DeltaTok 将 VFM 特征空间中连续帧间的差异压缩为单个增量令牌（delta token），使世界模型在仅包含时序变化的一维令牌序列上运行，并结合 Best-of-Many (BoM) 训练以在单次前向中产生多样化未来。
primary_logic: 预测未来只需编码帧间变化，而非完整空间特征；单个增量令牌足以捕获结构化低维的时序动态，配合 BoM 训练即可实现轻量且多样化的生成式世界模型。
claims:
- 逐步消融显示：从判别式基线到 BoM 训练，再到帧压缩，最终到增量压缩，DeltaWorld 在保持或提升准确率的同时大幅降低了计算开销。
- 在全量稠密预测基准上，DeltaWorld 的最佳预测一致超越先前生成式世界模型，且平均预测恢复至判别式基线水平，同时参数和 FLOPs 节省超过 35× 和 2,000×。
- 增量令牌同样能有效注入不同的判别式世界模型架构，在 DINO-Foresight 上以 2048× 更少的令牌匹配原有性能，验证了其通用性。
- VSPW segmentation (short, ~0.2s) 上 mIoU (best-of-20 / mean) = 55.4 (53.7)
---

# A Frame is Worth One Token: Efficient Generative World Modeling with Delta Tokens

> [!tip] 核心洞察
> 预测未来只需编码帧间变化，而非完整空间特征；单个增量令牌足以捕获结构化低维的时序动态，配合 BoM 训练即可实现轻量且多样化的生成式世界模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一帧一令牌：基于增量令牌的高效生成式世界建模 |
| 英文题名 | A Frame is Worth One Token: Efficient Generative World Modeling with Delta Tokens |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04913) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | DeltaWorld (含 DeltaTok tokenizer 及 BoM 训练目标) |
| Dataset | VSPW segmentation, Cityscapes segmentation, KITTI depth |

> [!tip] 效果简介
> - VSPW segmentation (short, ~0.2s) 上，mIoU (best-of-20 / mean) 55.4 (53.7) vs DINO-world 54.0 (deterministic) (+1.4 (best over baseline single; mean -0.3))。
> - VSPW segmentation (mid, ~0.6s) 上，mIoU (best-of-20 / mean) 50.1 (46.7) vs DINO-world 47.9 (deterministic) (+2.2 (best over baseline single; mean -1.2))。
> - Cityscapes segmentation (short, ~0.2s) 上，mIoU (best-of-20 / mean) 65.8 (63.9) vs DINO-world 62.0 (deterministic) (+3.8 (best over baseline; mean +1.9))。

## 概述

生成式世界模型旨在预测未来场景状态，为具身智能体提供规划依据。然而，现有方法面临一个根本瓶颈：它们以稠密空间特征图逐帧表示世界状态，且需多次前向传播才能生成多样化未来，未能利用连续帧间高度结构化的时空冗余，导致计算代价极高。

本文提出 **DeltaWorld**，一个轻量级生成式世界模型。其核心洞察是：预测未来只需编码帧间的**变化**，而非完整的空间特征。为此，DeltaWorld 引入 **DeltaTok**，将视觉基础模型（VFM）特征空间中连续帧间的差异压缩为单个增量令牌（delta token），使世界模型在一维令牌序列上运行；同时结合 **Best-of-Many（BoM）** 训练目标，在单次前向传播中即可生成多个多样化未来。

实验表明，DeltaWorld 在语义分割和深度估计的稠密预测基准上，最佳预测一致超越先前生成式世界模型（如 Cosmos-12B），且平均预测恢复至判别式世界模型基线水平，同时参数和 FLOPs 分别节省超过 **35×** 和 **2,000×**（Figure 2）。逐步消融研究证实，从判别式基线到 BoM 训练、再到帧压缩、最终到增量压缩，每一步都在保持或提升准确率的同时大幅降低计算开销（Table 2）。增量令牌同样可有效注入不同判别式世界模型架构，在 DINO-Foresight 上以 **2,048×** 更少的令牌匹配原有性能，验证了其通用性（Table D）。

## 背景与动机

### 生成式世界模型的核心瓶颈

世界模型旨在从历史观测中预测环境的未来状态，是具身智能与自主决策的关键组件。近年来，生成式世界模型取得了显著进展，能够合成逼真的未来帧，但其实际部署面临一个根本性瓶颈：**计算代价过高**。现有大规模生成式世界模型（如 Cosmos-4B 和 Cosmos-12B）需要多次前向传播，且以稠密的空间特征图逐帧表示世界状态，每帧需要数百甚至上千个 patch token。这种设计完全忽略了连续视频帧之间高度结构化的时空冗余——相邻帧的绝大多数空间信息是重复的，真正需要预测的仅是帧间变化。

### 现有方法的缺口

从技术路径来看，当前世界模型可大致分为两类，各有其固有局限：

- **判别式世界模型**（如 DINO-world、DINO-Foresight）：直接在视觉基础模型（VFM）的特征空间中预测下一帧的完整特征图。这类方法计算效率相对较高，但本质上是确定性的——给定历史，只能输出单一未来预测，无法捕捉真实世界中固有的多模态不确定性（例如，行人可能向左或向右移动）。

- **生成式世界模型**（如 Cosmos 系列）：在像素空间中通过扩散或自回归方式生成多样化未来。这类方法能产生多个合理假设，但代价是巨大的参数量和计算开销——参数规模动辄数十亿，单次推理需数千 GFLOPs，且通常需要多次前向传播才能生成一组候选未来。

这种“效率-多样性”的张力构成了当前世界模型研究的核心矛盾：**如何在保持生成多样性的同时，将计算代价降低到可部署水平？**

### 核心洞察：预测变化而非状态

本文的核心洞察直接切中上述瓶颈：**预测未来只需编码帧间变化，而非完整空间特征**。连续视频帧之间的差异在 VFM 特征空间中呈现出高度结构化的低维特性——光照、纹理、背景等大量信息在帧间保持稳定，真正发生变化的仅是物体位置、相机运动等少数自由度。如果能够将这种“变化”压缩为紧凑的表示，世界模型就无需在庞大的空间 token 序列上运行，从而从根本上降低计算复杂度。

### 本文动机与目标

基于上述洞察，本文提出 DeltaWorld——一个高效的生成式世界模型，其核心思想是通过 **DeltaTok** 将 VFM 特征空间中连续帧间的差异压缩为**单个增量令牌（delta token）**，使世界模型在仅包含时序变化的一维令牌序列上运行。结合 **Best-of-Many（BoM）训练目标**，DeltaWorld 能够在单次前向传播中生成多个多样化的未来假设，从而在保持生成能力的同时，实现参数和计算开销的大幅缩减（相较 Cosmos 减少 35× 以上参数和 2,000× 以上 FLOPs），并恢复至判别式基线的平均预测精度。

> **注意**：本文的实验基准 DINO-world 由作者重新实现（原始代码和数据未公开），Cosmos 系列基线的输出被重新编码为 DINOv3 特征以进行公平比较，训练数据规模与原 DINO-world 不完全一致。这些因素在解读性能对比时需予以考量。

## 核心创新

DeltaWorld 的核心创新在于将生成式世界模型的输入表示从**稠密空间特征图**彻底重构为**一维增量令牌序列**，并结合 Best-of-Many (BoM) 训练目标，在单次前向传播中实现轻量且多样化的未来状态生成。其关键突破可分解为三个相互协同的技术槽位变更。

### 从空间冗余到时序变化的表示转换

传统判别式世界模型（如 DINO-world）需对每一帧提取 $H \times W$ 个空间 patch token（例如 512×512 输入下为 1024 个 token），并在预测时逐帧生成完整的空间特征图。这种设计忽略了连续帧间高度结构化的时空冗余——相邻帧的大部分空间内容保持不变，真正需要预测的仅是帧间的**变化量**。

DeltaWorld 通过 DeltaTok 模块实现了这一洞察：给定冻结 VFM（DINOv3 ViT-B）编码的连续两帧特征图 $x_{t-1}$ 和 $x_t$，DeltaTok 编码器将其差异压缩为**单个增量令牌**（delta token）：

$$z_t = g(x_{t-1}, x_t, z_{\mathrm{init}}) \in \mathbb{R}^D$$

解码时，仅需前一帧特征图 $x_{t-1}$ 和当前 delta token $z_t$ 即可重建当前帧特征：

$$\hat{x}_t = h(x_{t-1}, z_t)$$

这一设计将世界模型的输入从每帧数百至上千个空间 token 压缩为**每帧仅 1 个 token**，上下文序列长度大幅缩短。消融实验（Table 2, Step (3)）表明，相比将每帧独立压缩为单一帧 token（frame compression）的方案，增量压缩在最佳和平均 mIoU 上均取得显著提升，且平均预测恢复到与判别式基线持平的水平。

### 单次前向的多样化生成机制

传统生成式世界模型（如 Cosmos 系列）需多次前向传播才能产生多样化未来，计算代价高昂。DeltaWorld 引入 BoM 训练目标，在训练时从高斯分布采样 $K$ 个噪声查询向量：

$$q^k \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma}), \quad k = 1, \dots, K$$

每个噪声查询经预测器生成一个候选 delta token，仅监督与真值最接近的候选：

$$k^\star = \arg\min_k \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^k)$$
$$L_{\mathrm{BoM}} = \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^{k^\star})$$

推理时，预测器在 delta token 序列上执行时序预测，通过不同噪声查询在**单次前向**中产生多样化未来：

$$\hat{z}_{t+1} = f(q^k, Z_{1:t}, T_{1:t}, \tau_{t+1})$$

这一设计的因果逻辑在于：噪声查询空间隐式编码了未来的不确定性，而 BoM 损失鼓励不同查询覆盖不同的合理轨迹。实验表明，增大训练查询数 $K$ 可持续提升最佳评分而无饱和现象，且平均评分在 $K \geq 64$ 后保持稳定（Figure 5），验证了多样性与平均质量的可兼顾性。

### 效率与精度的协同优化

上述两个槽位变更产生了显著的复合效应。Table 2 的逐步消融清晰揭示了各步骤的贡献：

- **Step (1) — BoM 训练应用于判别式基线**：最佳预测有所提升，但平均预测大幅下降（Cityscapes 上从 45.4 降至 31.1 mIoU），且训练时间增加约 5×。这表明仅添加多样性机制而不改变表示会损害平均质量。
  
- **Step (2) — 帧压缩（frame compression）**：将每帧压缩为单一 token 使 BoM 采样加速超过一个数量级，内存占用降至 1/5，但表示容量不足，精度低于基线。这暴露了独立压缩每帧的局限性。

- **Step (3) — 增量压缩（delta compression）**：切换为增量 token 后，最佳和平均 mIoU 均显著提升，平均预测恢复到与判别式基线持平，且预测器仅占总推理 FLOPs 的 0.5%（Table B）。

最终，DeltaWorld 在全量稠密预测基准上，最佳预测一致超越 Cosmos-12B 等生成式基线（Cityscapes 中时程 +2.1 mIoU），平均预测恢复至判别式基线水平，同时参数和 FLOPs 节省超过 35× 和 2,000×（Table 3, Figure 2）。

### 架构普适性

增量令牌的设计并非局限于特定预测器架构。实验表明，将 delta token 注入 DINO-world 可在更低训练时间和内存下达到相近精度（Table C）；在 DINO-Foresight 上以 2048× 更少的令牌匹配原有性能（Table D），验证了该表示方法的通用性。

## 整体框架

DeltaWorld 的完整 pipeline 由四个核心模块串联构成：**冻结的视觉基础模型（VFM）骨干**、**DeltaTok 增量分词器**、**时序预测器**以及**Best-of-Many（BoM）训练/推理机制**。其根本设计原则是：**世界模型仅需在“变化”上运行，而非在完整的空间特征上运行**。

### 数据流与模块协作

整个系统的输入为一段 RGB 视频帧序列，输出为对未来帧的多样化稠密预测（语义分割或深度估计）。数据流遵循以下路径：

1. **VFM 骨干编码**：每一帧原始 RGB 图像首先通过一个**冻结的 DINOv3 ViT-B** 模型，被编码为空间特征图 $x_t \in \mathbb{R}^{H \times W \times D}$（例如 $512 \times 512$ 输入下产生 $32 \times 32$ 个 patch token）。该骨干在整个训练过程中保持冻结，仅作为语义特征提取器。

2. **DeltaTok 增量压缩**：连续两帧的特征图 $x_{t-1}$ 与 $x_t$ 同时送入 DeltaTok 编码器，将帧间差异压缩为**单个增量令牌** $z_t \in \mathbb{R}^D$（公式 8）。解码时，DeltaTok 解码器接收前一帧特征图 $x_{t-1}$ 与增量令牌 $z_t$，重建当前帧特征图 $\hat{x}_t$（公式 9）。这一设计将每帧的表示从 $H \times W$ 个空间令牌缩减为 **1 个令牌**，压缩比可达 1024×（$512 \times 512$ 输入时）。

3. **时序预测器**：预测器是一个基于交叉注意力的 Transformer，配备一维 RoPE 位置编码。它完全在增量令牌序列 $Z_{1:t}$ 上运行，接收噪声查询 $q^k$ 作为条件输入，预测下一个增量令牌 $\hat{z}_{t+1}$（公式 10）。由于每帧仅 1 个令牌，预测器的序列长度极短，其计算开销仅占总推理 FLOPs 的 0.5%（生成 20 个样本时，见 Table B）。

4. **BoM 训练与推理**：
   - **训练阶段**：从高斯分布 $\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ 中采样 $K$ 个噪声查询 $q^k$（公式 2），预测器并行生成 $K$ 个候选增量令牌。BoM 损失仅选择与真值最接近的候选 $k^\star$ 进行监督（公式 4），其余分支不参与梯度回传。
   - **推理阶段**：同样采样 $K$ 个噪声查询，在**单次前向传播**中同时生成 $K$ 个不同的未来预测。每个预测的增量令牌经 DeltaTok 解码器恢复为空间特征图后，由下游任务头（分割或深度头）产生最终稠密预测。

### 关键设计决策

- **增量压缩 vs. 帧压缩**：消融实验（Table 2, Step 2 vs. Step 3）表明，将每帧压缩为单一“帧令牌”虽大幅降低了计算开销，但表示容量不足导致精度显著低于基线。增量压缩通过仅编码帧间变化，在保持同等计算效率的同时，使平均预测恢复到与判别式基线持平的水平。

- **单次前向多样化生成**：不同于需要多次前向传播的扩散模型或自回归模型，DeltaWorld 通过 BoM 机制在单次前向中产生 $K$ 个候选未来。增大训练查询数 $K$ 可持续提升最佳评分，且平均评分在 $K \geq 64$ 后保持稳定（Figure 5），表明多样性与平均质量可兼顾。

- **模块解耦**：VFM 骨干、DeltaTok 和预测器是独立训练的。DeltaTok 先以 MSE 重建损失 $L_{\mathrm{tok}} = \|x_t - \hat{x}_t\|^2$ 单独训练（公式 7），随后冻结并接入预测器进行 BoM 训练。这种解耦使得增量令牌可以灵活注入不同的判别式世界模型架构（如 DINO-Foresight），以 2048× 更少的令牌匹配原有性能（Table D）。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/001_Figure_1.jpg]]
*Figure 1: Outline of DeltaWorld. Unlike large existing generative world models that require many forward passes and represent each frame with many spatial tokens, our small DeltaWorld generates multiple futures in a single forward pass by using a single delta token to encode the difference between consecutive frames*

## 核心模块与公式推导

### 3.1 整体架构概览

DeltaWorld 的核心设计思想是将生成式世界模型的预测空间从稠密的二维空间特征图迁移到一维的时序增量令牌序列上。如 Figure 1 所示，系统由三个关键模块串联构成：冻结的视觉基础模型（VFM）作为特征提取器、DeltaTok 作为帧间变化的压缩与重建器、以及基于 Transformer 的预测器在 delta token 序列上进行时序预测。

### 3.2 Best-of-Many 生成式训练目标

为使模型具备单次前向生成多样化未来的能力，DeltaWorld 采用了 Best-of-Many（BoM）训练范式。其核心机制如下：

**噪声查询采样**：从高斯分布中采样 $K$ 个独立的噪声向量作为查询输入：
$$q^k \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma}), \quad k = 1, \dots, K$$

每个噪声查询 $q^k$ 会引导预测器产生一个不同的未来假设。对于空间位置 $(h,w)$，第 $k$ 个候选预测为：
$$\hat{x}_{t+1,h,w}^k = f(q^k, X_{1:t}, T_{1:t}, \tau_{t+1}, h, w) \in \mathbb{R}^D$$
其中 $X_{1:t}$ 为历史帧特征，$T_{1:t}$ 为对应的时间编码，$\tau_{t+1}$ 为目标时间步。

**BoM 损失**：在 $K$ 个候选中，仅选择与真实未来最接近的那个进行监督：
$$k^\star = \arg\min_k \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^k)$$
$$L_{\mathrm{BoM}} = \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^{k^\star})$$

这种设计使得梯度仅通过最优分支回传，其余 $K-1$ 个分支虽不被直接监督，但通过共享的预测器参数隐式地探索了预测空间的多样性。推理时，仅需一次前向传播即可并行生成 $K$ 个不同的未来轨迹。

### 3.3 DeltaTok：增量令牌的压缩与重建

DeltaTok 是 DeltaWorld 实现效率突破的关键组件。其设计出发点在于：连续帧的 VFM 特征图之间存在高度结构化的时空冗余，直接预测完整特征图是低效的；而帧间的变化信息本质上是低维的，可被压缩为单个连续向量。

**编码器**：给定连续两帧的 VFM 特征图 $x_{t-1}$ 和 $x_t$，DeltaTok 编码器将其联合压缩为一个 delta token：
$$z_t = g(x_{t-1}, x_t, z_{\mathrm{init}}) \in \mathbb{R}^D$$
其中 $z_{\mathrm{init}}$ 为可学习的初始化向量，用于提供编码的归纳偏置。编码器 $g$ 是一个 Vision Transformer（ViT），其输入为两帧 patch tokens 的拼接，输出为单个聚合向量。

**解码器**：解码器利用前一帧的完整特征图 $x_{t-1}$ 和当前 delta token $z_t$ 重建当前帧特征：
$$\hat{x}_t = h(x_{t-1}, z_t)$$
解码器 $h$ 同样是一个 ViT，其交叉注意力机制以 $x_{t-1}$ 的 patch tokens 为 key/value，以 $z_t$ 扩展后的查询向量为 query，从而将帧间变化“注入”到前一帧的表示中。

**重建损失**：DeltaTok 的训练目标为最小化重建特征与原始特征之间的均方误差：
$$L_{\mathrm{tok}} = \|x_t - \hat{x}_t\|^2$$

如 Figure 3 所示，DeltaTok 的编码-解码过程是完全对称的：编码器提取变化信息，解码器将变化应用于参考帧。这种设计使得单个 delta token 在 512×512 分辨率下实现了约 1,024 倍的令牌压缩。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/003_Figure_3.jpg]]
*Figure 3: Overview of DeltaTok. Given two frames encoded by a frozen vision foundation model (VFM) into grids of patch tokens*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/004_Figure_4.jpg]]
*Figure 4: Overview of DeltaWorld. The predictor operates entirely on delta tokens (Fig. 3) rather than spatial tokens, enabling efficient generation of future hypotheses. Best-of-Many training (top) backpropagates only through the best predicted delta token, so that diverse futures can be sampled in a single forward pass at inference (bottom). Shown with two context frames and two queries for illustration*

### 3.4 DeltaWorld 预测器

在 DeltaTok 将每帧压缩为单个 delta token 后，预测器的任务转变为在 delta token 序列上进行时序预测。给定历史 delta token 序列 $Z_{1:t}$ 和噪声查询 $q^k$，预测器输出下一个 delta token：
$$\hat{z}_{t+1} = f(q^k, Z_{1:t}, T_{1:t}, \tau_{t+1})$$

预测器采用 Transformer 架构，包含交叉注意力层以注入噪声查询，并使用一维旋转位置编码（1D RoPE）对 delta token 序列进行时序位置编码。如 Figure 4 所示，训练阶段仅对最优分支的预测 delta token 计算损失并回传梯度；推理阶段则通过 DeltaTok 解码器将预测的 delta token 恢复为空间特征图，进而输入下游任务头（分割或深度估计）。

这种设计的核心优势在于：预测器处理的序列长度从每帧 $H \times W$ 个 token 缩减为每帧仅 1 个 token，使得预测器的计算开销在生成 20 个样本时仅占总推理 FLOPs 的 0.5%（Table B），从而实现了超过 2,000 倍的总体 FLOPs 节省。

## 实验与分析

### 评估设置与数据集

实验覆盖语义分割与单目深度估计两大稠密预测任务，评估数据集如 Table 1 所示。语义分割在 **VSPW** 和 **Cityscapes** 上进行，深度估计在 **KITTI** 上进行。所有任务均设定了两个预测时程：**短时程**（约 0.2 秒，直接预测下一帧）与 **中时程**（约 0.6 秒，三步自回归 rollout）。这种分时程设计能够同时考察模型在瞬时预测与累积误差场景下的表现。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/005_Table_1.jpg]]
*Table 1: Evaluation datasets. We evaluate segmentation and depth at short (∼0.2 s) and mid (∼0.6 s) prediction horizons*

判别式基线 **DINO-world** 由本文重新实现，因为原始代码与训练数据未公开，其性能可能与原论文存在差异。生成式基线 **Cosmos-4B** 与 **Cosmos-12B** 受限于其推理约束（固定 9 帧上下文，24 帧生成），且主要面向像素级生成而非 VFM 特征预测；为公平比较，其输出被重新编码为 DINOv3 特征。所有方法的 FLOPs 统计均基于作者框架，Cosmos 的 FLOPs 未计入 tokenizer 和 KV 预填充等固定开销（预期较小）。

### 逐步消融：从判别式基线到高效生成式世界模型

Table 2 展示了将判别式世界模型逐步扩展为生成式世界模型的过程，报告了中时程（约 0.6 秒）的 mIoU。消融实验使用 100K 次迭代、256×256 输入分辨率、训练时 K=16 的设置，评估时报告 best-of-20 与均值（括号内）。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/007_Table_2.jpg]]
*Table 2: Towards an efficient generative world model. Reporting mid-horizon (∼0.6 s) mIoU. Steps (1-3) use K=16 during training and report best-of-20 during evaluation (mean in parentheses). GFLOPs for steps (1-3) reflect generating all 20 samples, and a single prediction for step (0). Time and Mem report training time and GPU memory relative to step (0). Using 256 × 256 crops*

**Step (1)：引入 Best-of-Many 训练。** 在判别式 DINO-world 基线上直接应用 BoM 目标（Section 3.2），使预测器基于噪声查询生成多个候选未来。结果呈现典型的两极分化：best-of-20 的 mIoU 在 VSPW 上从 44.8 升至 47.0，在 Cityscapes 上从 45.4 升至 46.8，证明至少有一个候选显著优于确定性预测；但平均 mIoU 急剧下降（VSPW 从 44.8 降至 39.4，Cityscapes 从 45.4 降至 31.1），表明多数候选质量较差。更关键的是，训练时间增加约 5 倍，因为每个空间位置的 K 个候选均需计算损失并反向传播。

**Step (2)：帧压缩。** 将每帧的 H×W 个空间 token 压缩为单个帧 token（frame tokenizer），使 BoM 采样加速超过一个数量级，内存占用降至约 1/5。然而，单一 token 的表示容量不足以完整编码一帧的语义信息，导致 best-of-20 mIoU 反而低于原始判别式基线（VSPW 降至 43.0，Cityscapes 降至 43.9），说明帧级压缩的瓶颈在于信息丢失而非计算效率。

**Step (3)：增量压缩（DeltaWorld）。** 将帧 token 替换为增量 token——仅编码连续帧间的变化而非完整帧信息。这一关键转变使 best-of-20 mIoU 大幅回升并超越帧压缩结果（VSPW 升至 46.8，Cityscapes 升至 48.7），同时平均 mIoU 恢复至与判别式基线持平的水平（VSPW 44.4 vs. 44.8，Cityscapes 45.5 vs. 45.4）。预期训练计算极小，因为预测器仅需处理每帧一个 token 的序列。

这一消融链条揭示了核心因果机制：**BoM 训练提供多样性但牺牲平均质量并引入计算开销，帧压缩降低开销但损失表示能力，增量压缩在两者间取得平衡——仅编码变化信息既保留了足够的语义用于准确预测，又将序列长度压缩至极简，使 BoM 的多样性生成变得真正高效。**

### 稠密预测主结果

Table 3 报告了全量稠密预测基准结果，使用 300K 次迭代、512×512 输入分辨率、训练时 K=256 的设置。生成式模型报告 best-of-20 评估（括号内为均值），FLOPs 反映生成全部 20 个样本的总开销。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/008_Table_3.jpg]]
*Table 3: Dense forecasting. Reporting short (∼0.2 s, direct) and mid (∼0.6 s, 3-step rollout) prediction horizons. Generative models report best-of-20 evaluation (mean in parentheses). GFLOPs reflect generating all 20 samples for generative models and a single prediction for DINO-world. Using 512 × 512 crops. †Our reimplementation. ‡Both variants use another 7B diffusion decoder, dominating FLOPs*

**语义分割。** 在短时程 VSPW 上，DeltaWorld 的 best-of-20 mIoU 达 55.4，超越 DINO-world 的确定性预测 54.0（+1.4），均值 53.7 仅略低于基线（-0.3）。在中时程 VSPW 上，best-of-20 达 50.1，较 DINO-world 的 47.9 提升 2.2 个点。在 Cityscapes 短时程上，DeltaWorld 的 best-of-20 达 65.8，较 DINO-world 的 62.0 提升 3.8 个点，均值 63.9 亦超越基线（+1.9）。在中时程 Cityscapes 上，DeltaWorld 的 best-of-20 达 55.4，超越 Cosmos-12B 的 53.3（+2.1），均值 51.3 与 Cosmos-12B 的 51.2 持平。

**深度估计。** 在 KITTI 短时程上，DeltaWorld 的 best-of-20 RMSE 为 3.00，优于 DINO-world 的 3.16（-0.16），均值 3.17 与基线 3.16 基本持平。在中时程上，best-of-20 RMSE 为 3.88，优于 Cosmos-12B 的 4.01（-0.13），均值 4.17 与 Cosmos-12B 的 4.14 接近。

**效率对比。** 如 Figure 2 所示，DeltaWorld 相较 Cosmos 系列生成式世界模型，参数减少超过 35 倍，FLOPs 减少超过 2,000 倍，同时在最佳预测上一致超越后者，平均预测恢复至判别式基线水平。这一效率优势源于两个设计选择：增量令牌将预测器序列长度压缩至每帧一个 token（预测器仅占 20 样本推理总 FLOPs 的 0.5%，见 Table B），以及 BoM 训练使多样化未来在单次前向传播中生成，无需多次采样。

### BoM 采样规模分析

Figure 5 展示了 BoM 训练查询数 K 对 Cityscapes 中时程 mIoU 的影响。增大训练时的 K 可持续提升 best-of-20 评分，且无饱和现象，表明模型能够利用更多噪声查询产生更优的候选未来。同时，平均评分在 K≥64 后保持稳定，说明多样性的增加并未以牺牲平均预测质量为代价——模型学会将低质量候选推至分布边缘，而非在所有候选间平均分配概率质量。这一特性是 DeltaWorld 实用性的关键：用户只需增加推理时的采样数即可获得更好的最佳预测，而无需重新训练。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/006_Figure_5.jpg]]
*Figure 5: Best-of-Many sample scaling. Effect of the number of training and evaluation queries on Cityscapes mid-horizon (∼0.6 s) mIoU. Using 256 × 256 crops*

### 增量令牌的架构普适性

增量令牌并非仅适用于本文的 DeltaWorld 架构。Table C 显示，将增量令牌注入判别式 DINO-world 后，以更低的训练时间和内存占用达到相近精度。Table D 进一步验证了在 **DINO-Foresight** 上的迁移效果：在 Cityscapes 上，增量令牌以 2,048 倍更少的 token 数量匹配了原始架构的性能。这表明增量令牌作为一种帧间变化压缩策略，具有跨架构的通用性——只要世界模型的核心操作是时序预测，将稠密空间表示替换为增量表示即可大幅降低计算开销而不显著损失精度。

### 局限性与失败模式

尽管 DeltaWorld 在效率与精度上取得了显著进展，仍存在若干值得关注的局限：

1. **BoM 训练缺乏分布建模目标。** 不同于扩散模型或 VAE 等具有明确概率解释的生成框架，BoM 仅通过选择最优候选来隐式地塑造生成分布，不保证对真实预测分布的覆盖。多样性受限于训练查询数 K，且无机制鼓励噪声查询空间的全利用——部分查询可能坍缩到相似预测，导致有效多样性低于 K。这解释了为何平均预测质量在 K 较小时明显低于判别式基线。

2. **增量令牌的误差积累。** 由于 DeltaTok 解码器需基于前一帧特征顺序重建当前帧，tokenizer 的重建误差与预测器的预测误差会随自回归步数累积，导致特征漂移。文中提及了可行的缓解方向（如 tokenizer 的重建自我一致性训练或引入校正机制），但未在实验中实现。中时程结果中均值评分的轻微下降（如 VSPW 从 44.8 降至 44.4）可能部分源于此效应。

3. **公平性约束。** DINO-world 基线由本文重新实现，与原始论文的性能差异无法完全排除；Cosmos 基线受限于其推理约束，且其 FLOPs 统计未包含全部固定开销。这些因素使效率对比的绝对数字需谨慎解读，但数量级上的优势（35× 参数、2,000× FLOPs）远超可能的统计偏差范围。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/002_Figure_2.jpg]]
*Figure 2: Performance comparison. Compared to the generative world model Cosmos [1], our DeltaWorld forecasts futures that better align with real-world outcomes while having over 35× fewer parameters and using 2,000× fewer FLOPs*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/011_Table.jpg]]
*Table: D. Delta tokens in the discriminative DINO-Foresight. Results on Cityscapes show that delta tokens transfer effectively to a different discriminative architecture, matching performance with 2048× fewer tokens. The token count indicates the total number of tokens used by the world model. Using 448×896 frames. †Numbers reported in the DINO-Foresight paper *

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/012_Table.jpg]]
*Table: B. GFLOPs breakdown. In DeltaWorld, the backbone and DeltaTok encoder run once, while the predictor and DeltaTok decoder are applied per generated sample. Using a three-step rollout and a four-frame context (mid-horizon), ViT-B components, and 256 × 256 crops. Table C. Delta tokens in the discriminative DINO-world. Delta tokens also perform well within a discriminative world model. Time and Mem report per-iteration training time and GPU memory relative to the discriminative baseline. Reporting mid-horizon (∼0.6 s) mIoU using 256 × 256 crops. †Our reimplementation*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/010_Table.jpg]]
*Table: A. Training data statistics. For DINO-world, we report the duration range and FPS from their paper. For ours, we report the mean duration, and all videos have the same frame rate*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2604_04913/figures/009_Figure_6.jpg]]
*Figure 6: Diverse sampled futures. Top row: four context frames and the future frame. Bottom row: four sampled DeltaWorld predictions and the oracle. In this VSPW [47] example, the pedestrian’s position and ego-camera motion lead to multiple plausible futures*

## 方法谱系与知识库定位

### 问题脉络：从判别式到生成式世界模型的效率瓶颈

世界模型的核心任务是根据历史观测预测未来的环境状态。判别式世界模型，如 **DINO-world** 和 **DINO-Foresight**，直接在视觉基础模型（VFM）的特征空间中预测下一帧的稠密空间特征图，取得了可观的预测精度。然而，这类方法本质上是确定性的——给定历史，它们只输出单一的未来预测，无法刻画真实世界中固有的多模态不确定性（例如，一个行人可能向左或向右移动）。

为捕获这种多样性，现有生成式世界模型（如 **Cosmos-4B** 和 **Cosmos-12B**）转向像素级生成，通过大规模扩散模型或自回归模型采样多个可能的未来帧。但这种能力付出了极高的计算代价：模型参数量动辄数十亿，且需要多次前向传播才能产生多样化的预测。更根本的是，这些方法以稠密的空间特征图（如 256 或 1024 个 patch token）逐帧表示世界状态，完全忽略了连续帧之间高度结构化的时空冗余——相邻帧中绝大部分空间信息是重复的，真正需要预测的只是帧间的变化量。

### 核心洞见：预测变化而非完整状态

DeltaWorld 的方法论突破在于将上述观察转化为一个简洁的设计原则：**世界模型只需要编码和预测帧间的变化，而非完整的空间特征**。这一洞见通过两个关键组件实现：

1. **DeltaTok**：一个轻量的 tokenizer，将 VFM 特征空间中连续两帧的差异压缩为单个连续的增量令牌（delta token）。与每帧需要 $H \times W$ 个空间令牌的稠密表示相比，DeltaTok 实现了上千倍的令牌压缩（例如，在 512×512 分辨率下减少 1,024×）。

2. **Best-of-Many (BoM) 训练**：通过从高斯分布采样 $K$ 个噪声查询 $q^k \sim \mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$，模型在单次前向传播中并行生成 $K$ 个候选未来，并仅对最接近真实值的预测进行监督：
   $$k^\star = \arg\min_k \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^k)$$
   $$L_{\mathrm{BoM}} = \sum_{h,w} \ell(x_{t+1,h,w}, \hat{x}_{t+1,h,w}^{k^\star})$$

这种设计的因果逻辑是：帧间变化构成一个结构化的低维流形，单个连续向量足以捕获其核心动态；而 BoM 目标则在不引入复杂分布建模（如扩散或 VAE）的前提下，赋予模型生成多样化未来的能力。

### 与基线方法的关键差异

| 设计维度 | 判别式世界模型 (DINO-world) | 生成式世界模型 (Cosmos) | DeltaWorld |
|---------|---------------------------|----------------------|------------|
| **输入表示** | 逐帧 $H \times W$ 个空间 token | 像素级生成 | 每帧 1 个 delta token |
| **预测输出** | 单一确定性特征图 | 多个像素级未来帧 | 多个 delta token，经解码器恢复特征图 |
| **生成机制** | 无（确定性） | 扩散/自回归采样（多次前向） | BoM 噪声查询（单次前向） |
| **训练目标** | Smooth L1 回归 | 扩散损失 / 交叉熵 | BoM 损失（仅监督最佳分支） |
| **上下文长度** | 随帧数线性增长 | 随帧数线性增长 | 每帧仅 1 个 token，序列极短 |

### 方法演进路径与消融证据

DeltaWorld 并非一步到位，而是通过三个渐进的消融步骤从判别式基线演化而来（Table 2）：

**Step (1)：在判别式基线上引入 BoM 训练。** 这使模型具备了生成多样化未来的能力——在 20 个候选预测中，最佳预测的 mIoU 确实有所提升。但代价显著：平均预测质量大幅下降（Cityscapes 上从 45.4 降至 31.1），且训练时间增加约 5 倍。这表明，在稠密空间特征图上直接应用 BoM 会导致预测器在噪声空间中难以有效学习，多数候选预测质量低下。

**Step (2)：将每帧压缩为单一帧 token。** 通过将空间特征图压缩为单个向量 $z_t = g(x_t, z_{\mathrm{init}})$，预测器的序列长度从 $H \times W$ 降至 1，使得 BoM 采样加速超过一个数量级，内存占用降至 1/5。然而，单个帧 token 的表示容量有限，无法充分保留空间细节，导致预测精度低于未压缩的判别式基线。

**Step (3)：替换为增量压缩（delta compression）。** 这是决定性的一步。DeltaTok 编码器 $z_t = g(x_{t-1}, x_t, z_{\mathrm{init}})$ 仅压缩帧间差异，解码器 $\hat{x}_t = h(x_{t-1}, z_t)$ 则利用前一帧的完整特征图恢复当前帧。这既保留了 Step (2) 的计算效率，又通过依赖前一帧的空间信息弥补了单 token 的容量瓶颈。结果表明，最佳和平均 mIoU 均显著提升，平均预测恢复到与判别式基线持平的水平。

### 方法的适用边界与局限

**1. BoM 训练的分布建模缺陷。** 不同于扩散模型或 VAE，BoM 目标不保证对真实预测分布的覆盖。多样性完全受限于训练时的查询数 $K$——模型只学会了在 $K$ 个候选中有至少一个好的预测，但并未被鼓励探索整个可能的输出空间。当真实未来落在训练查询未能覆盖的区域时，即使增加推理时的采样数，也无法保证捕获该模态。Figure 5 显示增大 $K$ 可持续提升最佳评分，但这是通过“覆盖更多可能性”而非“更精确地建模分布”实现的。

**2. 增量令牌的自回归误差积累。** DeltaTok 的解码过程依赖于前一帧的特征图：$\hat{x}_t = h(x_{t-1}, z_t)$。在多步 rollout 中，tokenizer 的重建误差和预测器的预测误差会逐步累积——第 $t$ 帧的重建误差会污染第 $t+1$ 帧的解码输入，导致特征漂移。论文仅指出了这一问题的存在和可行的缓解方向（如 tokenizer 的重建自我一致性训练），但未给出具体解决方案。

**3. 对 VFM 质量的依赖。** DeltaWorld 完全构建在冻结的 VFM（DINOv3 ViT-B）特征之上。如果 VFM 对某些场景或物体的特征表示不够判别性，增量令牌将无法捕获关键的语义变化，且这一误差会传播到下游任务。

### 开放问题与未来方向

1. **有原则的分布建模。** 如何为 BoM 或类似的单次前向生成方法引入具有理论保证的分布目标？可能的方向包括结合能量模型（EBM）以鼓励模态覆盖、引入对比散度以推开相似的候选预测，或设计轻量的拒绝采样机制以在推理时过滤低质量样本。

2. **长时自回归的误差抑制。** 如何有效控制 delta token 在长序列 rollout 中的漂移？可行的路径包括：在 tokenizer 训练中引入循环一致性约束（解码后重新编码应与原始 delta token 一致）、在预测器中加入纠错模块，或采用 scheduled sampling 策略在训练时逐步引入自回归误差。

3. **可控生成与语义解耦。** 噪声查询空间是否隐含了某种“动作条件”的结构？如果相似的噪声向量能跨场景产生语义一致的未来变化（例如，“向左漂移”的噪声始终导致物体向左运动），则可以通过操纵噪声查询实现可控的未来生成，而无需显式的动作标签。

4. **增量令牌的通用性验证。** 论文已初步证明 delta token 可迁移至 DINO-Foresight 等不同架构（Table D，以 2,048× 更少的令牌匹配原有性能），但其在更广泛的世界模型范式（如基于视频预测的强化学习、具身智能中的规划）中的有效性仍有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/A_Frame_is_Worth_One_Token_Efficient_Generative_World_Modeling_with_Delta_Tokens.pdf]]