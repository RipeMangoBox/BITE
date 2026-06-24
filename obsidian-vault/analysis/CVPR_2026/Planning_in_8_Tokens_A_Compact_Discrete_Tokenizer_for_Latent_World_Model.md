---
title: "Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Planning_in_8_Tokens_A_Compact_Discrete_Tokenizer_for_Latent_World_Model.pdf
project_link: "https://kdwonn.github.io/CompACT"
code_link: null
aliases:
- P8TCDTLWM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用冻结的预训练视觉基础模型（DINOv3）作为编码骨干，通过可学习的潜在令牌与交叉注意力机制进行重采样，将图像压缩为8-16个离散语义令牌，彻底丢弃纹理、光照等高频重建细节。
primary_logic: 规划仅依赖于高层语义信息和空间关系，而非逼真的感知细节；放弃精准重建，换取极端压缩，从而将规划延迟降低1-2个数量级。
claims:
- 使用8/16个离散令牌实现与784个连续令牌相当的导航规划精度，同时规划速度提高40-80倍。
- 紧凑令牌保留的动作相关信息优于16倍令牌数的目标分词器（IDM R² 0.716 vs 0.684）。
- 冻结DINOv3编码器优于微调，强调保留语义而非重建特征。
- 生成式解码是压缩的关键：直接重建导致rFID从2.40剧增至28.80。
---

# Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model

> [!tip] 核心洞察
> 规划仅依赖于高层语义信息和空间关系，而非逼真的感知细节；放弃精准重建，换取极端压缩，从而将规划延迟降低1-2个数量级。

| 字段 | 内容 |
|------|------|
| 中文题名 | 以8个令牌进行规划：一种用于潜在世界模型的紧凑离散分词器 |
| 英文题名 | Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05438) · [Project](https://kdwonn.github.io/CompACT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CompACT |
| Dataset | RECON Navigation, RoboNet IDM, RoboNet Video Prediction, ImageNet Reconstruction |

> [!tip] 效果简介
> - RECON Navigation 上，ATE↓ 1.330 (CompACT 16 tok) vs 1.262 (SD-VAE 784 tok) (略微增加5%，但延迟降低约40倍)；RPE↓ 0.390 (CompACT 16 tok) vs 0.354 (SD-VAE 784 tok) (略微增加10%)；Planning Latency (sec)↓ 5.78 (CompACT 16 tok) vs 178.78 (SD-VAE) (降低约31倍)。
> - RoboNet IDM 上，L1 error↓ 0.091 (CompACT 16 tok) vs 0.093 (Target tokenizer 256 tok) (略优)；R²↑ 0.716 (CompACT 16 tok) vs 0.684 (Target tokenizer) (提升4.7%)。
> - RoboNet Video Prediction 上，APE↓ 0.1122 (CompACT) vs 0.3383 (Target tokenizer) (降低约67%)。

## 概述

### 问题背景

视觉世界模型在决策时间规划中面临一个根本性的效率瓶颈：主流视觉分词器（如**SD-VAE**）将每张图像编码为数百个潜在令牌，导致基于注意力机制的世界模型在规划时计算成本随令牌数呈平方级增长。具体而言，784个连续令牌的规划延迟可达178秒以上，无法满足机器人导航与操控等实时控制需求。这一瓶颈并非源于模型架构本身，而是源于分词器对图像信息的冗余编码——纹理、光照等高频感知细节对规划决策并非必要，却占据了绝大部分计算资源。

### 核心思想

本文提出**CompACT**，一种将图像压缩为仅8个离散令牌的紧凑分词器，其核心洞察在于：**规划仅依赖于高层语义信息与空间关系，而非逼真的感知重建**。CompACT通过以下关键设计实现极端压缩而不牺牲规划能力：

- **冻结的语义骨干**：采用预训练的DINOv3视觉Transformer作为编码基础，保留强大的语义表示能力，同时避免微调导致的信息退化。
- **可学习的潜在重采样**：通过交叉注意力机制，使少量可学习查询令牌从冻结的语义特征中提取规划关键信息，彻底丢弃纹理、光照等高频细节。
- **生成式解码**：不直接重建像素，而是以紧凑令牌为条件，通过掩码生成模型学习生成目标分词器（MaskGIT-VQGAN）的令牌，从而在解码端保留感知质量的同时维持编码端的极端压缩。

### 方法定位

CompACT在方法谱系中占据独特位置：它不同于**SD-VAE**等追求高保真重建的连续分词器，也不同于**FlexTok**等支持可变令牌数的离散分词器——CompACT以无条件的极端压缩（8-16个令牌）实现规划效率的质变，同时通过生成式解码策略保留了必要的感知信息。其世界模型训练采用掩码生成范式，而非自回归或扩散模型，进一步降低了序列建模的计算开销。

### 主要结果

在RECON导航基准上，CompACT使用16个离散令牌即达到与SD-VAE（784个连续令牌）相当的规划精度（ATE: 1.330 vs 1.262），同时将规划延迟从178.78秒降至5.78秒，**加速约31倍**；使用8个令牌时延迟进一步降至4.83秒，**加速约37倍**。在RoboNet的逆向动力学评估中，CompACT的16个令牌保留的动作相关信息优于16倍令牌数的目标分词器（R²: 0.716 vs 0.684）。消融实验证实，生成式解码是压缩的关键——替换为直接重建会导致重建质量急剧恶化（rFID从2.40飙升至28.80），而冻结视觉编码器优于微调（ATE: 1.330 vs 1.500），印证了保留语义而非重建特征的设计原则。

## 背景与动机

### 决策时间规划中的效率瓶颈

在机器人导航与操作任务中，**决策时间规划**（decision-time planning）要求智能体在行动前通过世界模型模拟未来轨迹并优化动作序列。这一范式高度依赖两个关键能力：世界模型对场景动态的准确预测，以及规划过程本身的计算效率。

近年来，基于视频生成的世界模型取得了显著进展。以 **NWM** 为代表的方法将世界模型建模为像素空间中的条件生成模型：

$$f_{\theta} : (o_t, \mathbf{a}_t) \mapsto p_{\theta}(o_{t+1} | o_t, \mathbf{a}_t)$$

然而，这一范式面临一个根本性的效率瓶颈：**传统视觉分词器将每张图像编码为数百个潜在令牌**。以广泛使用的 **SD-VAE** 为例，每张图像被编码为 784 个连续令牌。在基于注意力机制的世界模型中，计算成本随令牌数呈平方级增长。当规划过程需要自回归地展开多条候选轨迹时：

$$z_{t+1} \sim f_{\phi}(z_t, a_t), \quad t \in \{0, \dots, H-1\}$$

数百个令牌的序列长度使得单次轨迹优化的延迟高达 **178 秒**（Table 4），无法满足实时控制的需求。

### 现有分词器的局限

当前用于世界模型的视觉分词器大致可分为两类：

- **连续分词器**（如 SD-VAE）：提供高保真重建，但令牌数固定为 784，导致规划延迟极高。
- **离散分词器**（如 FlexTok）：支持可变令牌数（1–256），但在极端压缩（如 16 个令牌）下，其规划精度显著劣于高令牌数方案（Table 4：FlexTok 64 tok ATE 1.484 vs CompACT 16 tok ATE 1.330）。

两类方法的共同问题在于：它们都致力于保留图像的感知细节（纹理、光照、高频信息），而这些信息对**规划任务而言并非必要**。规划仅依赖于高层语义信息和空间关系——物体的类别、位置、遮挡关系等——而非逼真的像素级重建。

### 核心洞察：用重建换取压缩

CompACT 的核心洞察是：**规划不需要看到每一个像素，它只需要理解场景中发生了什么**。如果分词器能够彻底丢弃纹理、光照等高频重建细节，仅保留语义和空间信息，那么图像可以被压缩到极少量的离散令牌中（8–16 个），从而将规划延迟降低 1–2 个数量级，同时保持与高令牌数方案相当的规划精度。

这一洞察的关键在于**语义优先于感知**：冻结的预训练视觉基础模型（DINOv3）天然提供语义丰富的特征表示，而可学习的潜在重采样模块通过交叉注意力从中提取任务关键信息，形成紧凑的离散令牌。实验表明，冻结 DINOv3 编码器优于微调（ATE：1.330 vs 1.500，Table 5 Right），进一步验证了“保留语义而非重建特征”的设计哲学。

### 本文的动机与目标

基于上述分析，本文提出 **CompACT**（Compact Action-Conditioned Tokenizer），旨在解决以下核心问题：**如何在保持规划精度的前提下，将每张图像压缩到极少量离散令牌，从而大幅降低决策时间规划的计算成本？**

具体而言，CompACT 的目标是：
1. 将每张图像编码为 **8–16 个离散令牌**（约 128 比特），相比 SD-VAE 的 784 个令牌压缩近 100 倍；
2. 通过**生成式解码**而非直接重建来验证压缩质量，确保紧凑令牌保留了足够的语义信息；
3. 在导航和操作任务上实现与高令牌数方案**相当的规划精度**，同时将规划延迟降低 **30–80 倍**。

## 核心创新

CompACT 的核心创新在于**将视觉分词器的设计目标从“精确重建”转向“规划保留”**，通过三个关键设计槽位的协同改变，实现了极端压缩下的高效决策时间规划。

### 1. 冻结语义编码器 + 可学习重采样

传统视觉分词器（如 **SD-VAE**）采用端到端训练的卷积 VAE 编码器，将每张图像编码为 784 个连续潜在令牌。CompACT 用**冻结的 DINOv3-B 视觉 Transformer** 替代可训练的编码器，彻底切断了梯度回传至视觉骨干的路径。紧凑潜在令牌不再从像素级重建损失中学习，而是作为**可学习的查询向量**，通过一个 5 层交叉注意力 Transformer 解码器（Latent Resampler）从冻结的语义特征图中进行重采样。这种设计的因果逻辑在于：规划仅依赖于高层语义信息和空间关系，而非纹理、光照等高频细节；冻结编码器强制令牌保留语义结构，而非适应重建目标。消融实验证实了这一点——冻结 DINOv3 编码器的 ATE 为 1.330，而微调编码器则劣化至 1.500（Table 5 Right），表明“保留语义”比“适应重建”对规划更关键。

### 2. 极端令牌压缩：从 784 到 8–16

基线方法 **SD-VAE** 每张图像使用 784 个连续令牌，**FlexTok** 支持 1–256 个离散令牌。CompACT 将令牌数压缩至 **16 或 8 个离散令牌**（约 128 bits/张），压缩比高达 49:1 至 98:1。这一改变的因果机制在于：基于注意力的世界模型（如 NWM 中的 CDiT）计算复杂度随令牌数平方级增长，令牌数减少直接带来规划延迟的平方级下降。实验表明，使用 8 个令牌时规划延迟从 178.78 秒降至 4.83 秒（约 37 倍加速），且 ATE 仅从 1.262 略微增至 1.330（Table 4）。值得注意的是，CompACT 的 16 令牌模型在 ATE 上甚至优于 FlexTok 的 64 令牌模型（1.330 vs 1.484），说明压缩本身并非牺牲性能——关键在于**保留什么信息**而非保留多少。

### 3. 生成式解码替代直接重建

传统分词器使用确定性一步前馈解码器直接生成像素。CompACT 采用**生成式解码策略**：紧凑令牌作为条件，通过掩码生成模型（Masked Generative Modeling）学习生成目标分词器 **MaskGIT-VQGAN** 的潜在令牌，再由目标解码器合成像素。这一设计将重建任务分解为“语义压缩”和“感知生成”两个阶段——紧凑令牌只负责语义瓶颈，感知细节由目标分词器的先验知识补全。消融实验揭示了这一改变的因果强度：将生成式解码替换为直接重建解码器后，rFID 从 2.40 飙升至 28.80（Table 2），证明生成式解码是极端压缩下维持重建质量的必要条件。

### 4. 离散潜在空间与掩码生成世界模型

CompACT 使用**有限标量量化（FSQ）** 将连续特征映射为离散令牌，使潜在空间天然适合掩码生成建模。世界模型 $f_{\phi}$ 在紧凑离散空间中采用掩码生成训练（Eq. 5），而非 SD-VAE 常用的扩散模型。离散空间带来的额外优势在于：规划中的潜在距离成本可直接基于 FSQ 基表示的 L1 距离高效计算（Eq. 8），将单次轨迹优化时间从像素空间的 5.78 秒进一步压缩至潜在空间的 2.15 秒（Table 5 Middle），且精度损失可忽略。

### 创新总结

三个槽位的协同改变形成了一条清晰的因果链：**冻结语义编码器**确保令牌保留规划相关信息 → **极端压缩**消除计算瓶颈 → **生成式解码**弥补感知细节的丢失。这一设计哲学的本质是将分词器从“通用图像压缩器”重新定位为“规划任务的信息瓶颈”，以放弃精准重建为代价，换取 1–2 个数量级的规划加速。

## 整体框架

CompACT 的整体框架由三个核心模块串联而成：**紧凑分词器**（CompACT Tokenizer）、**潜在世界模型**（Latent World Model）与**决策时间规划器**（CEM Planner）。该框架的核心思想是将高维图像观测压缩为极少量的离散语义令牌，在低维潜在空间中完成下一状态预测与动作序列优化，从而将规划延迟降低 1–2 个数量级，同时保持与高维连续分词器相当的规划精度。

### 模块关系与数据流

Figure 1 给出了框架的全景概览，其数据流可概括为以下三个步骤：

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed latent world model formulation (Sec. 3.1). (a) An image tokenizer is first trained with a reconstruction objective to map an input image into compact latent tokens z. (Fig. 2 and Sec. 3.2). (b) Using the learned tokenizer, latent world model*

1. **分词阶段（Figure 1a）**：给定当前观测图像 $o_t$ 与目标图像 $o_{\text{goal}}$，冻结的视觉基础模型（DINOv3）提取语义特征，经潜在重采样器（latent resampler）与有限标量量化（FSQ）后，将每张图像压缩为 $N$ 个离散令牌 $z_t, z_{\text{goal}} \in \mathbb{R}^{N \times D}$，其中 $N \in \{8, 16\}$。此阶段仅更新重采样器与生成式解码器，视觉编码器保持冻结。

2. **世界模型阶段（Figure 1b）**：在 CompACT 潜在空间中训练一个掩码生成式世界模型 $f_{\phi}$，建模条件分布 $p_{\phi}(z_{t+1} \mid z_t, \mathbf{a}_t)$。具体而言，导航任务采用基于 DiT 的自回归架构（Figure 10），操纵任务则使用块因果 Transformer 实现并行预测（Figure 11）。训练目标为掩码生成损失（Eq. 5），历史帧通过交叉注意力注入条件信号。

3. **规划阶段（Figure 1c）**：在测试时，利用训练好的 $f_{\phi}$ 在潜在空间中展开 $H$ 步轨迹 $z_{t+1} \sim f_{\phi}(z_t, a_t)$，通过交叉熵方法（CEM）搜索最优动作序列 $\mathbf{a}_{0:H-1}$，最小化预测终态 $z_H$ 与目标令牌 $z_{\text{goal}}$ 之间的距离。成本函数可在像素空间或潜在空间中计算——后者利用 FSQ 逆映射后的 L1 距离（Eq. 8），在规划精度损失可忽略的前提下将延迟进一步降低约 2.7 倍（Table 5 Middle）。

### 关键设计瓶颈

框架的因果杠杆在于**分词器的极端压缩策略**：传统方法（如 SD-VAE）将每张图像编码为 784 个连续令牌，导致基于注意力的世界模型在展开轨迹时计算成本随令牌数平方级增长。CompACT 通过以下三个设计选择打破这一瓶颈：

- **冻结语义编码器**：保留 DINOv3 的语义特征，丢弃纹理、光照等高频重建细节，因为规划仅依赖高层语义与空间关系（Table 5 Right：冻结优于微调，ATE 1.330 vs 1.500）。
- **潜在重采样**：以可学习查询令牌通过交叉注意力从冻结特征中提取紧凑表示，注意力可视化（Figure 4）表明令牌聚焦于模块化场景元素。
- **生成式解码**：紧凑令牌不直接重建像素，而是作为条件通过掩码生成模型（MM-DiT，Figure 8）生成目标分词器（MaskGIT-VQGAN）的令牌。直接重建会导致 rFID 从 2.40 飙升至 28.80（Table 2），验证了生成式解码是压缩的关键。

### 输入输出规范

| 模块 | 输入 | 输出 |
|------|------|------|
| CompACT Encoder $\mathcal{E}_{\text{compact}}$ | 图像 $o_t \in \mathbb{R}^{H \times W \times 3}$ | 离散令牌 $z_t \in \{1,\dots,K\}^N$ |
| Latent World Model $f_{\phi}$ | $z_t$，动作 $\mathbf{a}_t$ | 下一状态分布 $p_{\phi}(z_{t+1} \mid z_t, \mathbf{a}_t)$ |
| CEM Planner | $z_0$, $z_{\text{goal}}$ | 最优动作序列 $\mathbf{a}^*_{0:H-1}$ |
| CompACT Decoder $\mathcal{D}_{\text{compact}}$ | $z_t$（可选，仅用于可视化） | 重建图像 $\hat{o}_t$（经目标解码器 $\mathcal{D}_{\psi}$） |

> **注意**：解码器仅在训练分词器或需要可视化时使用；规划过程中完全在潜在空间中进行，无需像素级重建，这是实现 40–80 倍加速的根本原因。

## 核心模块与公式推导

### 3.1 潜在世界模型形式化

CompACT 的核心思想是将世界模型从高维像素空间迁移到极低维的离散潜在空间，从而在决策时间规划中实现数量级的计算加速。

传统像素空间世界模型定义为：

$$f_{\theta} : (o_t, \mathbf{a}_t) \mapsto p_{\theta}(o_{t+1} | o_t, \mathbf{a}_t) \tag{1}$$

其中 $o_t$ 为当前观测（图像），$\mathbf{a}_t$ 为动作，模型预测下一帧观测的条件分布。该形式化在规划时需对高维像素进行多次前向传播，计算成本极高。

CompACT 将世界模型映射到紧凑潜在空间：

$$f_{\phi} : (z_t, \pmb{a}_t) \mapsto p_{\phi}(z_{t+1} | z_t, \pmb{a}_t) \tag{2}$$

其中 $z_t \in \mathbb{R}^{N \times D}$ 为低维潜在令牌（$N \leq 16$，$D$ 为令牌维度），由 CompACT 分词器从图像编码得到。在规划过程中，利用训练好的潜在世界模型进行自回归展开：

$$z_{t+1} \sim f_{\phi}(z_t, a_t), \quad t \in \{0, \dots, H-1\} \tag{3}$$

CEM 规划器在潜在空间中搜索动作序列 $\pmb{a}_{0:H-1}$，以最小化预测终态与目标图像潜在令牌之间的距离。规划成本函数支持两种距离度量：像素空间距离（需通过解码器重建图像后计算）和潜在空间距离（直接在令牌层面计算），后者可进一步降低延迟（Table 5 Middle：2.15秒 vs 5.78秒）。

### 3.2 CompACT 分词器架构

CompACT 分词器由三个关键模块构成（Figure 2），实现从图像到 8/16 个离散令牌的极端压缩。

#### 3.2.1 编码器 $\mathcal{E}_{\mathrm{compact}}$

编码器采用冻结的 DINOv3-B 视觉 Transformer 作为语义特征提取骨干，通过潜在重采样模块将密集的 patch 表征压缩为少量可学习查询令牌，最后经有限标量量化（FSQ）离散化。

编码器架构经三种变体验证（Figure 3）：
- **(a) ViT (scratch) + [REG]**：从头训练的 ViT，将潜在令牌拼接至输入 patch 令牌，遵循先前 Transformer 分词器设计。
- **(b) DINOv3 + [REG]**：以预训练 DINOv3 权重初始化编码器，训练时更新全部参数。
- **(c) DINOv3 + latent resampler**：冻结 DINOv3 编码器，仅训练潜在重采样模块。该变体为最终采用方案，消融实验证实冻结编码器优于微调（ATE：1.330 vs 1.500，Table 5 Right）。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/005_Figure_3.jpg]]
*Figure 3: CompACT encoder*

潜在重采样的核心机制：$N$ 个可学习查询令牌通过交叉注意力机制，从冻结的 DINOv3 patch 表征中选择性地提取语义信息。注意力可视化（Figure 4）显示，不同紧凑令牌聚焦于场景中的模块化元素（如物体、边界），而非纹理细节，验证了“仅保留规划关键语义”的设计直觉。

#### 3.2.2 生成式解码器 $\mathcal{D}_{\mathrm{compact}}$

解码器不直接重建像素，而是以紧凑令牌为条件，通过掩码生成模型学习生成目标分词器（MaskGIT-VQGAN）的潜在令牌。该设计基于 MM-DiT 架构（Figure 8），训练损失为：

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/017_Figure_8.jpg]]

$$\mathcal{L}_{\mathrm{tok}} = - \mathbb{E}_{z^{\psi}} \big[ \log p(z^{\psi} | z, M(z^{\psi})) \big] \tag{4}$$

其中 $z$ 为 CompACT 编码器输出的紧凑令牌，$z^{\psi}$ 为目标分词器令牌，$M(z^{\psi})$ 为随机掩码后的目标令牌。训练时仅更新潜在重采样模块和 $\mathcal{D}_{\mathrm{compact}}$，目标分词器的编码器 $\mathcal{E}_{\psi}$ 仅用于生成掩码目标令牌，解码器 $\mathcal{D}_{\psi}$ 仅在推理时用于像素级重建。

生成式解码是压缩成功的关键：若替换为单步前馈解码器直接重建图像，rFID 从 2.40 飙升至 28.80（Table 2），表明紧凑令牌无法承载足够的感知细节，必须依赖生成式解码从目标分词器的先验中“补充”纹理和光照信息。

#### 3.2.3 离散量化

采用有限标量量化（FSQ）将连续潜在表征映射为离散令牌。FSQ 将每个维度的值截断并四舍五入到有限整数集，避免了 VQ-VAE 中码本坍塌和直通梯度估计的复杂性。离散化后的令牌间距离定义为：

$$d(z_i, z_j) = \lVert \mathbf{FSQ}^{-1}(z_i) - \mathbf{FSQ}^{-1}(z_j) \rVert_{1} \tag{8}$$

该距离直接基于 FSQ 的基表示计算 L1 距离，无需解码回像素空间，为潜在空间规划成本函数提供高效度量。

### 3.3 潜在世界模型训练

世界模型在 CompACT 潜在空间中采用掩码生成建模训练：

$$\mathcal{L}_{\mathrm{world}} = - \mathbb{E}_{z_t, a_t, z_{t+1}} \left[ \log p(z_{t+1} | z_t, a_t, M(z_{t+1})) \right] \tag{5}$$

其中 $M(z_{t+1})$ 为对目标令牌 $z_{t+1}$ 的随机掩码。该范式与分词器训练一致，均采用掩码生成而非扩散模型，避免了扩散模型的多步采样开销。

针对不同任务，世界模型采用不同架构：
- **导航任务**：基于 CDiT（Figure 10），动作通过自适应层归一化注入，历史帧通过交叉注意力条件化，自回归生成下一帧。
- **操纵任务**：采用块因果 Transformer（Figure 11），支持并行预测多帧未来状态，动作令牌通过 AdaLN 和线性层条件化解码头。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/020_Figure_10.jpg]]
*Figure 10: World model*

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/022_Figure_11.jpg]]
*Figure 11: World model*

历史掩码训练策略对规划精度有显著影响：在训练时随机掩码部分历史帧，迫使模型学习更鲁棒的时序推理，将导航 ATE 从 1.480 降至 1.330（Table 5 Left）。

### 3.4 逆向动力学模型（IDM）

为评估紧凑令牌中动作相关信息的保留程度，CompACT 引入逆向动力学模型（Figure 9）：输入连续帧的令牌序列，经 Transformer 帧编码器后平均池化为单一条件向量，驱动基于扩散策略的动作去噪器，预测帧间动作。IDM 性能（Table 3）直接反映令牌表征的动作判别能力——CompACT 16 令牌的 R² 达 0.716，超过 256 令牌的目标分词器（0.684），证明语义压缩并未损害动作相关信息。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/018_Figure_9.jpg]]
*Figure 9: Inverse Dynamics Model (IDM) architecture. Consecutive frames are tokenized and processed through a transformerbased frame encoder, which produces a single conditioning vector via average pooling. This vector conditions an action denoiser implemented as a diffusion policy [11], which predicts the action taken between the two frames*

## 实验与分析

### 核心实验设计逻辑

CompACT 的实验体系围绕一个核心主张展开：**极端压缩的离散语义令牌足以支撑决策时间规划，且能带来 1–2 个数量级的延迟降低**。为验证这一主张，作者设计了三条递进的实验线索：

1. **分词器重建质量评估**（ImageNet）：验证极端压缩下语义信息的保留程度。
2. **动作相关信息保留评估**（RoboNet IDM）：验证紧凑令牌中是否保留了规划所需的动作相关信息。
3. **下游规划性能评估**（RECON 导航、RoboMimic 操纵）：验证紧凑令牌在实际规划任务中的有效性，并测量延迟收益。

这种"重建→信息保留→规划"的三层验证结构，使得结论具有从感知到决策的完整证据链。

### 分词器重建质量（ImageNet）

Table 1 展示了 CompACT 在 ImageNet 验证集上的重建性能。CompACT 使用仅 16 个离散令牌（约 256 bits/图像）达到了 rFID 2.40 和 IS 209.0，使用 8 个令牌时 rFID 为 3.21、IS 为 207.5。作为参照，目标分词器 MaskGIT-VQGAN 使用 256 个令牌获得 rFID 1.83。考虑到令牌数压缩了 16–32 倍，重建质量的下降幅度相对温和。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/003_Table_1.jpg]]
*Table 1: Reconstruction performance of CompACT on ImageNet validation split. Metrics are computed using open-sourced checkpoints. rFID is measured using clean-fid [54]. †: Measured using 16 tokens*

**关键消融（Table 2）**揭示了压缩机制的本质：当将生成式解码器替换为单步前馈解码器（直接重建像素）时，rFID 从 2.40 急剧恶化至 28.80。这表明 **CompACT 的压缩能力并非来自编码器本身，而是来自"编码语义令牌 + 生成式解码恢复细节"的协同设计**。编码器负责保留高层语义锚点，解码器则通过掩码生成模型从目标分词器的先验中"补全"感知细节。

此外，Table 2 还验证了冻结 DINOv3 编码器的必要性：微调编码器反而导致 rFID 上升，支持了"保留预训练语义特征比适应重建目标更重要"的设计直觉。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/004_Table_2.jpg]]
*Table 2: Ablation on CompACT tokenizer. rFID is measured on ImageNet [15] validation split using clean-fid [54]*

### 动作相关信息保留（RoboNet IDM）

Table 3 通过逆向动力学模型（IDM）评估不同分词器令牌中动作相关信息的保留程度。CompACT 16 令牌在 RoboNet 上取得了 L1 error 0.091 和 R² 0.716，优于使用 256 个令牌的目标分词器（L1 0.093, R² 0.684）。这意味着 **16 个语义令牌比 256 个感知令牌保留了更多的动作相关信息**。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/007_Table_3.jpg]]
*Table 3: Performance of Inverse Dynamics Model (IDM) trained with different tokenizers on RoboNet [13]. L1 error and*

这一反直觉结果的可能解释是：目标分词器的令牌分布在整幅图像上，包含大量与动作无关的背景和纹理信息，这些信息在 IDM 训练中构成噪声；而 CompACT 的潜在重采样机制（Figure 4）通过交叉注意力主动聚焦于语义相关的图像区域，天然过滤了无关信息。

### 导航规划性能（RECON）

Table 4 是全文最核心的实验结果。在 RECON 导航基准上，CompACT 16 令牌取得了 ATE 1.330 和 RPE 0.390，与 SD-VAE 784 连续令牌的 ATE 1.262 和 RPE 0.354 相比，精度损失仅约 5–10%。但规划延迟从 178.78 秒骤降至 5.78 秒（**约 31 倍加速**），8 令牌版本进一步降至 4.83 秒（**约 37 倍加速**）。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/008_Table_4.jpg]]
*Table 4: Planning performance of NWM on RECON benchmark with different tokenizers. Latency (sec) represents single trajectory optimization time using a single RTX 6000 ADA GPU*

与离散分词器 FlexTok 的对比更具说服力：CompACT 16 令牌的 ATE 1.330 优于 FlexTok 64 令牌的 1.484，且令牌数仅为其 1/4。这证明 **CompACT 的压缩效率并非单纯来自减少令牌数，而是来自语义聚焦的编码策略**。

Figure 7 的延迟分解进一步揭示了加速来源：SD-VAE 的规划延迟主要消耗在世界模型 rollout（在 784 个连续令牌上运行注意力）和解码器（将 784 个潜在向量解码为像素）。CompACT 将令牌数压缩 49–98 倍后，注意力计算量呈平方级下降，解码也从像素生成简化为目标令牌生成。

Figure 14 展示了 ATE、规划延迟与 GPU 显存占用的三维权衡：CompACT 在精度–延迟–显存的帕累托前沿上占据绝对优势位置。

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/025_Figure_14.jpg]]
*Figure 14: Plot for ATE, planning latency, and memory peak usage on RECON [60]. Latency and memory usage is mesaured for single trajectory optimization, using a single RTX 6000 ADA GPU*

### 设计选择消融（Table 5）

![[assets/figures/papers/paper_list_l2570_https_arxiv_org_abs_2603_05438/figures/011_Table_5.jpg]]
*Table 5: Effect of design choices in terms of planning accuracy on RECON. (Left): Effect of the history masking in the world model fθ (Sec. 3.3). (Middle): Comparison between the different cost function (Sec. 3.1). (Right): Effect of the freezing vision encoder during tokenizer training (Sec 3.2.1)*

Table 5 从三个维度消融了影响规划精度的关键设计：

- **历史掩码训练**：在世界模型训练中随机掩码历史帧（而非始终使用完整历史）将 ATE 从 1.480 降至 1.330。这类似于训练时的正则化，迫使模型学习更鲁棒的时序预测。
- **成本函数选择**：在 CEM 规划中使用潜在空间 L1 距离（基于 FSQ 基表示，Eq. 8）替代像素空间距离，规划延迟从 5.78 秒进一步降至 2.15 秒，且精度损失可忽略。这是 CompACT 离散设计的直接收益——无需解码即可在潜在空间内计算语义距离。
- **冻结编码器**：冻结 DINOv3 编码器（ATE 1.330）优于微调编码器（ATE 1.500），再次验证了保留预训练语义特征对下游规划的重要性。

### 动作条件视频预测（RoboNet）

Table 6 将评估扩展到操纵场景。在 RoboNet 动作条件视频预测任务上，CompACT 取得了 APE 0.1122，远优于目标分词器的 0.3383（降低约 67%），生成延迟也从 3.826 秒降至 0.740 秒（约 5.2 倍加速）。这表明紧凑令牌在需要时序一致性的生成任务中同样具有优势——更少的令牌意味着更低的时序建模难度。

### 闭环操纵（RoboMimic Lift）

Table 8 报告了在 RoboMimic Lift 任务上的闭环操纵结果。需要注意的是，该评估仅在最简单的 Lift 任务上进行，且未集成本体感知。CompACT 在此任务上展示了可行性，但作者明确指出这属于初步验证，复杂操纵场景下的闭环性能仍需进一步研究。

### 失败模式与局限性

综合实验结果和作者自述，CompACT 的主要失败模式包括：

1. **高频细节丢失**：极端压缩必然牺牲纹理、光照等感知细节，Table 1 中 rFID 与目标分词器的差距（2.40 vs 1.83）反映了这一固有限制。因此 CompACT 不适合需要摄影真实感重建的任务。
2. **CEM 规划的轨迹假设限制**：CEM 规划假设轨迹为直线且仅优化端点，这限制了机动自由度。在需要复杂避障或精细路径规划的场景中，这一假设可能导致次优解。
3. **操纵任务的评估有限**：闭环评估仅在简单 Lift 任务上进行，未覆盖需要接触力感知或长时序精确控制的复杂操纵。
4. **对预训练视觉模型的依赖**：Table 7 的跨骨干消融显示，不同视觉基础模型（DINOv3、DINOv2、CLIP 等）的重建性能存在差异，CompACT 的性能与所选视觉骨干高度耦合。

### 实验公平性说明

NWM 基线复现时使用了 CDiT-B（原始论文使用 CDiT-XL），并排除了 Tartan 和 Ego4D 数据集以控制资源消耗。尽管如此，复现的基线 ATE 1.262 与原始报告值 1.13 处于可比范围。所有延迟测量均在单张 RTX 6000 Ada GPU 上完成，实际部署时可能因硬件差异而变化。

## 方法谱系与知识库定位

### 问题域定位：从像素世界模型到语义压缩

CompACT 解决的核心矛盾是**决策时间规划（decision-time planning）中视觉表征的极端压缩与规划精度之间的权衡**。传统视觉世界模型（如 NWM）依赖 SD-VAE 等连续分词器，将每张图像编码为 784 个潜在令牌。基于注意力的世界模型在展开轨迹时，计算成本随令牌数平方级增长，导致单条轨迹优化延迟高达 178 秒，无法满足实时控制需求（Table 4）。

CompACT 的突破性假设是：**规划仅依赖于高层语义信息和空间关系，而非逼真的感知细节**。这一假设将问题从“如何压缩图像”重新定义为“如何保留规划关键信息”。方法上，CompACT 采用冻结的 DINOv3-B 作为语义骨干，通过可学习的潜在重采样器将图像压缩为 8-16 个离散令牌，彻底丢弃纹理、光照等高频重建细节。这种“语义保留、感知丢弃”的策略在方法谱系中开辟了一条新路径：**不是追求更好的重建，而是追求更高效的规划**。

### 与连续分词器的对比：效率瓶颈的根源

SD-VAE 是当前先进世界模型（如 NWM）的标准分词器。其 784 个连续令牌提供了丰富的感知信息，但直接导致规划延迟随令牌数平方级增长。CompACT 在 RECON 导航基准上的对比实验（Table 4）揭示了这一权衡的量化边界：

- **精度代价可忽略**：CompACT 16 令牌的 ATE 为 1.330，相比 SD-VAE 的 1.262 仅增加 5%；RPE 从 0.354 增至 0.390，增加 10%。
- **效率收益巨大**：规划延迟从 178.78 秒降至 5.78 秒（16 令牌）或 4.83 秒（8 令牌），加速约 31-37 倍。

延迟分解（Figure 7）进一步表明，加速主要来自两个环节：潜在空间展开（rollout）不再受令牌数平方级增长的影响，以及生成式解码器仅在规划终点执行一次（而非每步解码）。这种“延迟解码”策略是 CompACT 效率优势的关键设计。

### 与离散分词器的对比：压缩水平与语义质量的差异

FlexTok 是支持可变令牌数（1-256）的离散分词器，与 CompACT 在压缩水平上直接可比。Table 4 显示，CompACT 16 令牌的 ATE（1.330）优于 FlexTok 64 令牌（1.484），且仅用 1/4 的令牌数。这表明 CompACT 的压缩并非简单的降采样，而是**语义选择性压缩**——通过冻结 DINOv3 保留的语义特征比端到端训练的离散分词器更有利于规划。

逆向动力学模型（IDM）实验（Table 3）提供了更直接的证据：CompACT 16 令牌的 R² 为 0.716，高于目标分词器 256 令牌的 0.684。这意味着 CompACT 的紧凑令牌中**动作相关信息的密度更高**，尽管令牌数减少了 16 倍。注意力可视化（Figure 4）进一步揭示，潜在重采样器的不同令牌自发聚焦于场景中的模块化元素（如墙壁、障碍物），形成结构化的语义表征，而非无结构的压缩。

### 核心技术贡献的消融证据

CompACT 的三个关键设计选择均有明确的消融支撑：

1. **冻结视觉编码器优于微调**：Table 5（Right）显示，冻结 DINOv3 的 ATE 为 1.330，微调后反而升至 1.500。这表明保留预训练语义特征比适应重建目标更重要，验证了“语义保留”的核心假设。

2. **生成式解码是压缩的前提**：Table 2 显示，将生成式解码器替换为直接重建解码器，rFID 从 2.40 飙升至 28.80。这说明极端压缩的令牌无法直接编码重建所需的感知细节，必须依赖生成式解码器“补全”目标令牌。

3. **历史掩码训练提升规划精度**：Table 5（Left）显示，在世界模型训练中对历史帧进行掩码，ATE 从 1.480 降至 1.330。这一设计迫使模型更依赖当前状态和动作进行预测，减少了历史信息的过度依赖。

### 适用边界与局限

CompACT 的设计假设决定了其适用边界：

- **任务类型限制**：仅针对导航和简单操纵任务（RoboMimic 的 Lift 任务）进行了评估。CEM 规划假设轨迹为直线且仅优化端点，限制了机动自由度。对于需要精细操作或复杂动态交互的任务，8-16 个令牌可能不足以编码必要的空间精度。
- **感知细节丢失**：极端压缩必然丢失纹理、光照等高频信息。Table 1 显示 CompACT 16 令牌的 rFID（2.40）高于 MaskGIT-VQGAN（1.83），表明重建质量存在差距。因此 CompACT 不适合需要摄影真实感生成的应用。
- **闭环评估不足**：操纵任务的闭环评估仅在简单任务上进行，且未集成本体感知。实际部署中的闭环性能仍有待验证。

### 开放问题

CompACT 开辟了多个值得探索的方向：

1. **表征迁移**：冻结 DINOv3 的效果已验证，但冻结其他视觉基础模型（如 DINOv2、CLIP、甚至机器人专用表征）时的规划性能变化尚不明确。
2. **规划算法升级**：当前 CEM 规划仅优化端点距离，利用时间距离信息或更复杂的成本函数可能突破直线轨迹假设。
3. **端到端整合**：CompACT 的紧凑令牌能否直接整合到端到端强化学习策略中，实现全闭环控制，而非仅用于模型预测控制？
4. **扩散世界模型加速**：紧凑令牌是否也能加速基于扩散的世界模型（如视频生成模型）中的规划，将 CompACT 的压缩思想推广到更广泛的生成式规划框架？
5. **本体感知融合**：将实时观察和本体感知纳入 IDM 和规划循环，可能显著提升闭环操纵性能，这是从仿真到真实部署的关键一步。

## 原文 PDF

![[paperPDFs/CVPR_2026/Planning_in_8_Tokens_A_Compact_Discrete_Tokenizer_for_Latent_World_Model.pdf]]