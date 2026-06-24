---
title: "TokenHand: Discrete Token Representation for Efficient Hand Mesh Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TokenHand_Discrete_Token_Representation_for_Efficient_Hand_Mesh_Reconstruction.pdf
project_link: null
code_link: null
aliases:
- TokenHand
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 将手部三维模型表示为M个离散Token，每个Token编码手部的一个子结构，并将重建任务从连续回归转化为在码本上的分类问题。这既提供了结构先验，又保持了局部独立性，并实现了高效解码。
primary_logic: 通过两阶段训练：先使用Point Transformer编码器和共享码本学习手部点云的离散量化表示，再冻结解码器，将图像驱动的重建转化为Token分类。量化空间提供的强先验允许使用轻量级解码器，从而在保持高精度的同时达到实时推理。
claims:
- 在FreiHAND数据集上，PA-MPJPE达到5.7mm，PA-MPVPE为5.9mm，同时保持65 FPS实时推理速度。
- 在DexYCB数据集上，相比H2ONet，MPJPE降低1.7mm，MPVPE降低1.0mm。
- 消融实验表明，关键点引导的上采样点采样策略对性能至关重要，将特征图分辨率提升至28×28带来明显改善（PA-MPJPE从6.0mm降至5.7mm）。
- 参数量仅为先前基于Transformer方法的约10%，同时提高了精度和效率。
---

# TokenHand: Discrete Token Representation for Efficient Hand Mesh Reconstruction

> [!tip] 核心洞察
> 通过两阶段训练：先使用Point Transformer编码器和共享码本学习手部点云的离散量化表示，再冻结解码器，将图像驱动的重建转化为Token分类。量化空间提供的强先验允许使用轻量级解码器，从而在保持高精度的同时达到实时推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | TokenHand：面向高效手部网格重建的离散Token表示 |
| 英文题名 | TokenHand: Discrete Token Representation for Efficient Hand Mesh Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/He_TokenHand_Discrete_Token_Representation_for_Efficient_Hand_Mesh_Reconstruction_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | TokenHand |
| Dataset | FreiHAND, DexYCB |

> [!tip] 效果简介
> - FreiHAND 上，PA-MPJPE (mm) 5.7 vs Best real-time baseline (~6.7) (~14% improvement)；PA-MPVPE (mm) 5.9 vs – (–)；FPS 65 vs – (–)。
> - DexYCB 上，MPJPE (mm) – vs H2ONet (1.7 mm improvement)；MPVPE (mm) – vs H2ONet (1.0 mm improvement)。

## 概述

单视图手部网格重建面临一个根本性瓶颈：基于参数模型（如MANO）的方法对局部误差敏感，误差沿运动链分层累积；而直接回归网格顶点的方法缺乏结构先验，易产生不完整几何与伪影。现有方法难以在高精度与实时推理效率之间取得平衡。

**TokenHand** 提出了一种全新的重建范式：将手部三维模型表示为 $M$ 个离散Token，每个Token对应学习码本中的一个索引，编码手部的一个子结构。由此，手部网格重建从连续回归问题转化为Token分类问题。该设计同时提供了结构先验与局部独立性，并允许使用预训练冻结的轻量级解码器，在保持高精度的同时实现实时推理。

核心结论如下：

- **精度领先**：在FreiHAND数据集上，PA-MPJPE达到5.7 mm，PA-MPVPE为5.9 mm，较最佳实时基线提升约14%（Table 1）。
- **高效推理**：推理速度达65 FPS，参数量仅为先前基于Transformer方法的约10%（Table 2）。
- **泛化能力**：在DexYCB数据集上，相比**H2ONet**（Xu et al., CVPR 2023），MPJPE降低1.7 mm，MPVPE降低1.0 mm（Table 3）。
- **关键设计验证**：关键点引导的上采样点采样策略对性能至关重要，将特征图分辨率提升至28×28使PA-MPJPE从6.0 mm降至5.7 mm（Table 8）。

方法层面，TokenHand采用两阶段框架：第一阶段利用Point Transformer编码器和共享码本，从手部点云学习离散量化表示；第二阶段冻结解码器，将图像驱动的重建转化为Token分类。这一量化空间提供的强先验，使得轻量级解码器即可完成高质量网格重建，从而在精度-效率曲线上取得突破（Figure 3）。

## 背景与动机

### 手部网格重建的现实需求

从单张RGB图像中恢复三维手部网格是计算机视觉与增强现实领域的基础任务，在虚拟现实交互、手势识别、远程协作等应用中具有广泛需求。然而，该任务面临一个核心矛盾：**高精度重建与实时推理效率难以兼得**。手部具有21个关节、超过15个自由度的复杂运动链结构，且经常出现自遮挡和与他物的交互遮挡，使得从二维图像中准确推断三维几何极具挑战。

### 现有方法的瓶颈

当前主流方法可归纳为两类范式，各自存在结构性缺陷：

**基于参数模型的方法**（如MANO回归路线）将手部重建转化为预测少量姿态参数和形状参数的回归问题。这类方法虽然具备运动链结构先验，但对局部关节的回归误差极为敏感——误差会沿运动链分层累积，导致末端手指关节出现显著偏移。同时，MANO的低维参数空间（通常约61维）难以表达手部表面的精细变形，如手指按压物体时的局部凹陷。

**直接回归网格顶点的方法**（如**METRO**（Zhang et al., ICCV 2019）、**MeshGraphormer**（Lin et al., ICCV 2021））通过Transformer或图卷积网络直接预测778个或更多顶点的三维坐标。这类方法虽然避免了对参数模型的依赖，但缺乏有效的结构先验，容易产生不完整的几何形状和表面伪影。更重要的是，Transformer的自注意力机制导致计算复杂度和参数量随顶点数平方增长，严重制约了实时推理的可能性。**FastMETRO**（Cho et al., ECCV 2022）通过分离token交互部分缓解了参数压力，但其核心范式仍是逐顶点回归，未能从根本上解决效率与精度的权衡问题。

以实时性为目标的轻量级方法，如**MobRecon**（Chen et al., CVPR 2022）和**H2ONet**（Xu et al., CVPR 2023），通过精简网络结构实现了高速推理，但精度上存在明显妥协——在FreiHAND数据集上，最佳实时基线方法的PA-MPJPE约为6.7mm，与非实时方法存在显著差距。

### 范式转换的动机

上述困境的根源在于**连续回归范式本身**：无论是回归MANO参数还是网格顶点坐标，模型都需要在高维连续空间中直接预测精确数值，这一过程对噪声敏感且缺乏中间结构化约束。一个自然的思路是：能否将手部三维模型表示为**一组离散的结构化基元**，将重建任务从连续数值回归转化为**在有限码本上的分类问题**？

这一思路受到两方面的启发：
1. **向量量化表示**在图像生成领域的成功（如VQ-VAE系列）表明，离散码本可以学习到数据中丰富的结构先验，且分类任务比回归任务更易优化、更稳定。
2. 手部本身具有天然的**组合性结构**——手掌、手指根部、指尖等子结构在功能和解剖上相对独立，若能用离散Token分别编码这些子结构，既能提供局部独立性以避免误差累积，又能通过Token间的交互捕捉全局姿态依赖。

基于此，TokenHand提出了一个关键洞察：**将手部三维模型表示为M个离散Token，每个Token编码手部的一个子结构，并将重建任务从连续回归转化为在共享码本上的Token分类问题。** 这种范式转换使得模型可以借助量化空间的强先验，使用轻量级解码器完成高效重建，从而在保持高精度的同时实现65 FPS的实时推理速度。

## 核心创新

TokenHand 的核心创新在于将手部三维重建从**连续回归问题重构为离散Token分类问题**，通过引入一个学习到的共享码本（codebook）作为量化结构先验，实现了精度与效率的双重突破。具体而言，该方法将手部模型表示为 M 个离散Token，每个Token对应码本中的一个索引，编码手部的一个子结构（见 Figure 1）。这一范式转变带来了以下关键改变：

### 1. 重建范式：从回归到分类

现有主流方法——无论是回归MANO参数的参数化路线（如 **METRO** (Lin et al., ICCV 2021)、**MeshGraphormer** (Lin et al., ICCV 2021)），还是直接回归顶点坐标的非参数路线——均在连续空间中优化，缺乏对可行手部形状的显式约束。TokenHand 则将重建目标转化为预测 M 个Token的离散类别（码本索引），将解空间限制在码本所刻画的合法手部形状流形内。这一设计使得网络无需在巨大的连续空间中搜索，而是从有限且结构化的候选集中进行选择，从根本上降低了任务难度。

### 2. 表示方式：离散Token替代连续坐标

TokenHand 将手部三维模型表示为 M 个离散Token的集合 $\mathbf{L} = (l_1, l_2, \cdots, l_M)$，每个 $l_i \in \{1, \cdots, K\}$ 指向共享码本 $\mathbf{C} \in \mathbb{R}^{K \times D}$ 中的一个嵌入向量。与直接输出778个顶点坐标或MANO参数的连续表示相比，这种离散化表示具有两个优势：（1）**局部独立性**——每个Token仅负责手部的一个子结构，修改单个Token仅影响对应局部区域，避免了运动链分层误差累积问题；（2）**强结构先验**——码本通过第一阶段在大规模手部点云上训练得到，隐式编码了合法手部形状的分布，有效抑制了不完整几何与伪影的产生。

### 3. 解码器设计：冻结的轻量级级联上采样解码器

传统方法中，解码器需要从头端到端训练，参数量大且推理开销高。TokenHand 采用两阶段训练策略：第一阶段使用 Point Transformer 编码器和共享码本学习手部点云的离散量化表示，第二阶段将解码器**冻结**，仅训练图像编码器与Token分类头。由于量化空间提供了强先验，解码器可以被设计为轻量级的级联上采样网络（使用 MetaFormer 模块），无需承担学习手部结构先验的负担。这使得 TokenHand 的参数量仅为先前基于Transformer方法的约10%（见 Table 2），同时推理速度达到65 FPS。

### 4. 结构先验来源：学习到的码本替代运动链

MANO模型通过预定义的关节运动链提供结构先验，但该先验是固定的且对局部误差敏感。TokenHand 的结构先验完全来自数据驱动的码本学习——码本中的每个嵌入向量对应手部的一种局部子结构模式，Token之间的依赖关系由 MLP-Mixer 分类头捕获。这种学习到的先验比手工设计的运动链更灵活，且不受关节角度参数化的限制，能够更自然地表达手部的复杂形变。

### 5. 效率机制：Token分类替代顶点回归

在推理阶段，TokenHand 仅需通过轻量级分类头预测 M 个Token的类别（交叉熵损失 $\ell_{cls} = \mathrm{CE}(\hat{\mathbf{L}}, \mathbf{L})$），随后通过软推理 $\mathbf{S} = \hat{\mathbf{L}} \times \mathbf{C}$ 将预测logits与码本向量加权求和，送入冻结的解码器生成网格。这一流程避免了Transformer中昂贵的自注意力计算和GCNN中的图卷积操作，使得整体推理速度达到65 FPS，同时在 FreiHAND 数据集上取得 PA-MPJPE 5.7mm、PA-MPVPE 5.9mm 的精度，相比最佳实时基线提升约14%（见 Table 1 和 Figure 3）。

### 关键设计支撑

上述范式转变依赖于两个关键工程设计的支撑：
- **关键点引导的上采样点采样**：Token生成器受 **MobRecon** (Chen et al., CVPR 2022) 启发，从骨干网络输出的特征图中以2D关键点位置为引导进行点采样，并将特征图分辨率提升至28×28。消融实验表明，这一策略相比全局池化或网格采样将 PA-MPJPE 从6.2mm/6.0mm降至5.7mm（见 Table 8）。
- **MLP-Mixer分类头**：4个 MLP-Mixer 块用于捕获Token间的依赖关系，输出分类logits，在保持轻量化的同时有效建模了手部子结构之间的空间相关性。

## 整体框架

TokenHand 将手部网格重建从连续回归重新定义为离散Token分类问题。其核心思想是：将三维手部模型表示为 M 个离散Token，每个Token对应学习码本中的一个索引，编码手部的一个局部子结构（Figure 1）。整个框架分为两个阶段，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/002_Figure_2.jpg]]
*Figure 2: Two stages of the TokenHand representation (a, b). In Stage I, a compositional encoder maps the hand point cloud to M tokens, which are quantized using a codebook. Thus, each hand model is represented as a set of discrete codebook indices. In Stage II, hand reconstruction is formulated as a classification task by predicting the categories of the M tokens, corresponding to the codebook entries. The predicted tokens are then decoded by a decoder network to produce the final hand model*

**第一阶段：Token化表示构建。** 这一阶段的目标是学习一个可量化的手部表示空间，独立于图像输入。具体而言，使用一个 Point Transformer 编码器 $f_e$ 将手部点云 $\mathbf{H}$ 映射为 M 个Token特征 $\mathbf{T} = (\mathbf{t}_1, \mathbf{t}_2, \cdots, \mathbf{t}_M) = f_e(\mathbf{H})$。随后，这些Token特征通过一个共享的量化码本 $\mathbf{C} = (\mathbf{c}_1, \cdots, \mathbf{c}_K)^{\mathrm{T}} \in \mathbb{R}^{K \times D}$ 进行离散化——每个 $\mathbf{t}_i$ 通过最近邻查找被分配到一个码本索引：

$$q(\mathbf{t}_i = k | \mathbf{H}) = \begin{cases} 1 & \text{if } k = \arg\min_j \|\mathbf{t}_i - \mathbf{c}_j\|_2 \\ 0 & \text{otherwise} \end{cases}$$

量化后的Token嵌入 $\mathbf{Z}$ 送入一个级联上采样解码器 $f_d$，重建出手部网格 $\hat{\mathbf{H}} = f_d(\mathbf{Z})$。该解码器在后续阶段被冻结，不再更新。

**第二阶段：图像驱动的Token分类。** 给定单张裁剪手部图像，重建任务被转化为预测 M 个Token的码本索引。流程如下：

1. **骨干网络提取特征**：采用 FastViT-MA36 作为骨干网络，从输入图像中提取特征图。
2. **Token生成器采样**：受 MobRecon（Chen et al., CVPR 2022）启发，采用关键点引导的点采样策略，从特征图中提取空间对齐的Token特征。特征图首先进行4倍上采样，再基于关键点位置进行采样，得到 M 个Token特征 $\mathbf{X}_f$。这一步骤对最终精度至关重要——消融实验表明，相比全局池化或网格采样，关键点引导采样将 PA-MPJPE 从 6.2/6.0 mm 降至 5.7 mm（Table 8）。
3. **分类头预测**：Token特征经过四个 MLP-Mixer 块处理，捕捉Token间依赖关系，输出分类 logits $\hat{\mathbf{L}} = \mathcal{M}(\mathbf{X}_f)$。训练时使用交叉熵损失 $\ell_{cls} = \mathrm{CE}(\hat{\mathbf{L}}, \mathbf{L})$ 进行监督。推理时，将预测的 logits 对码本向量进行软加权求和 $\mathbf{S} = \hat{\mathbf{L}} \times \mathbf{C}$，以替代硬选择并保证梯度可回传。
4. **冻结解码器重建**：将预测的Token嵌入送入第一阶段预训练好并冻结的级联上采样解码器，直接输出最终手部网格。

**输入输出流总结**：输入为单张裁剪手部图像 → 骨干网络提取特征图 → 关键点引导采样生成 M 个Token特征 → MLP-Mixer 预测 M 个码本索引 → 冻结解码器重建手部网格。两阶段设计的关键优势在于：量化码本提供了强结构先验，使得图像驱动的重建仅需学习Token分类，从而允许使用轻量级解码器，在保持高精度的同时实现 65 FPS 的实时推理。

## 核心模块与公式推导

TokenHand 将手部网格重建从连续回归重构为离散Token分类问题，其核心由两个阶段构成：**第一阶段**在点云域学习手部的离散Token表示与码本；**第二阶段**冻结解码器，将图像驱动的重建转化为Token类别预测。以下分模块阐述关键设计与公式。

### 第一阶段：Token化与量化

给定手部点云 $\mathbf{H}$，使用 **Point Transformer 编码器** $f_e$ 将其映射为 $M$ 个Token特征：

$$\mathbf{T} = (\mathbf{t}_1, \mathbf{t}_2, \cdots, \mathbf{t}_M) = f_e(\mathbf{H})$$

其中每个Token $\mathbf{t}_i \in \mathbb{R}^D$ 对应手部的一个子结构。随后，引入一个可学习的共享码本：

$$\mathbf{C} = (\mathbf{c}_1, \cdots, \mathbf{c}_K)^{\mathrm{T}} \in \mathbb{R}^{K \times D}$$

码本包含 $K$ 个 $D$ 维嵌入向量。每个Token特征通过最近邻查找实现离散化：

$$q(\mathbf{t}_i = k | \mathbf{H}) = \begin{cases} 1 & \text{if } k = \arg\min_j \|\mathbf{t}_i - \mathbf{c}_j\|_2 \\ 0 & \text{otherwise} \end{cases}$$

量化后的Token嵌入 $\mathbf{Z}$ 送入**级联上采样网格解码器** $f_d$（基于MetaFormer），重建手部网格：

$$\hat{\mathbf{H}} = f_d(\mathbf{Z})$$

第一阶段训练完成后，解码器被**冻结**，码本作为强结构先验保留，为第二阶段的高效分类提供基础。

### 第二阶段：图像驱动的Token分类

给定裁剪后的输入图像，使用 **FastViT-MA36** 骨干网络提取特征图。**Token生成器**采用关键点引导的点采样策略（继承自 **MobRecon**，Chen et al., CVPR 2022），从特征图中提取空间对齐的Token特征。具体而言，特征图先经4倍上采样，再以2D关键点位置为引导进行采样，得到初始Token特征 $\mathbf{X}_m$。随后经过残差卷积块精炼、展平与线性投影：

$$\mathbf{X}_f = \mathcal{L}(\operatorname{Flatten}(\mathcal{C}(\mathbf{X}_m)))$$

精炼后的特征 $\mathbf{X}_f$ 通过**4个MLP-Mixer块** $\mathcal{M}$ 捕获Token间依赖关系，输出分类logits：

$$\hat{\mathbf{L}} = \mathcal{M}(\mathbf{X}_f)$$

训练时使用交叉熵损失监督Token类别预测：

$$\ell_{cls} = \mathrm{CE}(\hat{\mathbf{L}}, \mathbf{L})$$

其中 $\mathbf{L}$ 为第一阶段产生的伪标签（码本索引）。

### 软推理机制

为保证端到端梯度回传，推理时采用**软加权求和**替代硬选择——用预测logits对码本向量进行加权：

$$\mathbf{S} = \hat{\mathbf{L}} \times \mathbf{C}$$

得到的软嵌入 $\mathbf{S}$ 送入冻结的解码器生成最终手部网格。这一设计使分类logits的梯度可经码本嵌入反向传播，实现端到端优化。

### 模块设计要点总结

| 模块 | 关键设计 | 作用 |
|------|---------|------|
| 编码器 $f_e$ | Point Transformer | 将点云映射为结构化Token特征 |
| 码本 $\mathbf{C}$ | $512 \times 512$，共享可学习 | 提供量化结构先验，离散化表示空间 |
| 解码器 $f_d$ | 级联上采样 + MetaFormer，第一阶段后冻结 | 从Token嵌入高效重建网格 |
| 骨干网络 | FastViT-MA36 | 高效图像特征提取 |
| Token生成器 | 关键点引导采样 + 4×上采样特征图 | 空间对齐的Token特征提取 |
| 分类头 | 4层MLP-Mixer | 捕获Token间依赖，输出类别logits |
| 软推理 | logits加权码本嵌入 | 保证梯度回传，端到端训练 |

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/001_Figure_1.jpg]]
*Figure 1: Our approach represents a hand model using M discrete tokens, each corresponding to an index in the learned codebook (top). Each token encodes a specific sub-structure of the hand. In each row, changing the value of a single token consistently modifies the same sub-structure (bottom)*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/016_Figure_5.jpg]]
*Figure 5: An illustration demonstrates various designs of token generators*

## 实验与分析

TokenHand 在两个主流手部网格重建基准——FreiHAND 和 DexYCB——上进行了系统评估。实验设计围绕三个核心问题展开：离散 Token 表示能否在保持实时推理的前提下实现高精度重建？各模块设计选择对性能的贡献如何？方法在不同条件下的泛化能力与效率表现如何？

### 实验设置

**数据与指标**。训练在 FreiHAND 数据集上进行，该数据集包含约 130K 张真实场景手部图像，提供 MANO 模型标注。泛化测试在 DexYCB 数据集上进行，该数据集包含手-物交互场景，侧重评估方法在遮挡条件下的鲁棒性。主要评估指标包括 PA-MPJPE（Procrustes 对齐后的平均每关节位置误差）、PA-MPVPE（Procrustes 对齐后的平均每顶点位置误差）以及 FPS（帧率）。在 DexYCB 上使用未对齐的 MPJPE 和 MPVPE 评估绝对精度。

**训练配置**。Tokenization 网络使用 AdamW 优化器，基础学习率 6e-3，权重衰减 0.05，批量大小 128，训练 200 轮。3D 手部重建网络使用 AdamW 优化器，学习率初始化为 5e-4，50 轮后降至 5e-5，批量大小 64，训练 300 轮。码本尺寸固定为 512×512。骨干网络采用 FastViT-MA36。

### 主实验结果

**FreiHAND 数据集**。TokenHand 在 FreiHAND 上取得了 PA-MPJPE 5.7mm、PA-MPVPE 5.9mm 的精度，同时保持 65 FPS 的实时推理速度（Table 1）。相比最佳实时基线方法，精度提升约 14%，在精度-速度权衡曲线中占据明显优势区域（Figure 3）。值得注意的是，TokenHand 的推理速度已超过部分非实时方法（≤40 FPS），而精度仍保持领先。

**DexYCB 数据集**。在更具挑战性的 DexYCB 手-物交互场景中，TokenHand 相比 H2ONet（Xu et al., CVPR 2023）在 MPJPE 上降低 1.7mm，MPVPE 上降低 1.0mm（Table 3），验证了离散 Token 表示在遮挡条件下的泛化优势。这一结果表明，量化码本提供的强结构先验有助于在复杂交互场景中保持几何一致性。

**效率对比**。Table 2 展示了与基于 Transformer 方法的参数量对比。TokenHand 的参数量仅为先前 Transformer 方法的约 10%，同时精度和效率均有提升。这一效率优势源于两个设计选择：冻结的轻量级级联上采样解码器避免了逐顶点回归的冗余计算；离散 Token 分类范式将重建任务从连续空间回归转化为码本上的分类，大幅降低了预测空间维度。

### 消融实验

**码本尺寸**。Table 4 显示，码本尺寸在 384 到 640 范围内对重建精度影响较小，PA-MPJPE 波动在 4.9–5.1mm 之间。这表明 512 维的量化空间已能充分覆盖手部结构的表达能力，方法对码本超参数不敏感。

**回归器层数与 Token 数量**。Table 5 的消融表明，4 层级联回归层配合 Token 数 [48, 97, 194, 389] 的渐进式上采样策略取得最佳性能（PA-MPJPE 5.7mm）。过少的层数或 Token 数会导致几何细节丢失，而过多的层数则带来边际收益递减。

**特征维度与 MetaFormer 块数**。Table 6 显示，渐进降低特征维度至 32 并配合适当数量的 MetaFormer 块，可在精度与效率之间取得最优平衡。特征维度过低会限制表达能力，过高则增加计算开销而无明显精度收益。

**骨干网络选择**。Table 7 对比了多种骨干网络，FastViT-MA36 在所有候选中取得最强结果，验证了轻量级高效骨干与 TokenHand 分类范式的良好适配性。

**Token 生成器设计**。Table 8 的消融最为关键：将特征图进行 4 倍上采样后进行关键点引导采样，相比全局池化或网格采样策略，PA-MPJPE 从 6.2/6.0mm 显著降至 5.7mm。这一结果揭示了空间对齐的特征提取对 Token 质量的决定性作用——关键点引导采样确保了每个 Token 特征与手部子结构的空间对应关系，而高分辨率特征图则保留了细粒度几何信息。进一步增加卷积层未带来额外收益，表明当前设计已达到特征提取的饱和点。

### 定性分析

Figure 4 展示了 FreiHAND 上的定性对比。TokenHand 重建的手部网格在手指弯曲、手掌姿态等细节上更接近真值，尤其在手指间相对位置和指尖方向上表现出更好的结构一致性。这归因于离散 Token 表示中每个 Token 编码特定子结构的机制——改变单个 Token 值仅影响对应的局部区域（Figure 1），从而避免了回归方法中常见的全局误差传播。

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/013_Figure_4.jpg]]
*Figure 4: Qualitative comparison between our method and other state-of-the-art approaches on the FreiHAND dataset*

### 讨论与局限

尽管 TokenHand 在精度和效率上均表现优异，但分析中仍存在若干值得关注的方面。首先，DexYCB 上的评估虽显示了泛化优势，但严重遮挡场景下的极限性能仍需进一步验证。其次，离散 Token 表示的粒度由 Token 数量 M 决定，当前设置（M=389）是否足以表达极度精细的手指姿态差异（如手指间亚毫米级变化）尚需考察。此外，码本训练依赖于覆盖充分的手部姿态数据，在数据稀缺的特定手势类别上可能出现量化误差。最后，不同基线方法使用的骨干网络和训练方案存在差异，虽在各自设定下报告最佳结果，但严格受控的公平比较仍需统一实验条件。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/003_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on the FreiHAND dataset. ”–” indicates results not reported. The best performance is highlighted in bold. Second best performance is underlined*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/004_Figure_3.jpg]]
*Figure 3: Trade-off between accuracy and inference speed. Our method exceeds non–real-time approaches (≤ 40 FPS) in both speed and precision. Compared with real-time methods (≥ 60 FPS), it achieves noticeably higher accuracy while maintaining comparable inference speed*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/005_Table_2.jpg]]
*Table 2: Comparison of transformer-based approaches*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/006_Table_3.jpg]]
*Table 3: Comparison with state-of-the-art methods on the DexYCB dataset. ”–” indicates results not reported. The best performance is highlighted in bold. Second best performance is underlined*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/018_Table_8.jpg]]
*Table 8: Ablation study of sampling strategies and resolution settings used in the token generator*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/014_Table_5.jpg]]
*Table 5: Effect of regressor layers and token counts*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/015_Table_6.jpg]]
*Table 6: Ablation on feature dimensions and the number of MetaFormer blocks in the regressor layer*

![[assets/figures/papers/paper_list_l24_https_openaccess_thecvf_com_content_CVPR2026_html_He_TokenHand_Discrete/figures/017_Table_7.jpg]]
*Table 7: Ablation on backbone selection and its impact on reconstruction performance*

## 方法谱系与知识库定位

### 1. 问题定位：从连续回归到离散分类的范式转换

单视图手部网格重建长期面临“精度-效率”的跷跷板困境。主流路线可归纳为两条：

**参数化回归路线**以 **MANO** 模型为核心，通过预测低维姿态参数间接生成网格。此类方法受益于强运动学先验，但对局部关节误差高度敏感——误差沿手指运动链逐级放大，导致指尖漂移等典型失败模式。代表性工作如 **METRO** (Lin et al., ICCV 2021) 和 **MeshGraphormer** (Lin et al., ICCV 2021) 将 Transformer 引入网格顶点回归，虽提升了全局建模能力，但参数量与计算开销急剧膨胀。

**非参数直接回归路线**放弃 MANO 先验，直接从图像特征预测顶点坐标或体素占用。这类方法避免了运动链误差累积，却因缺乏结构约束而容易产生不完整几何、异常拓扑和表面伪影。**MobRecon** (Chen et al., CVPR 2022) 通过关键点引导的 2D-to-3D 提升实现了实时推理，但在精度指标上仍与离线方法存在差距。**H2ONet** (Xu et al., CVPR 2023) 针对遮挡场景优化，但精度-速度权衡仍未根本突破。

**TokenHand 的核心范式转换**在于将重建任务从连续空间中的回归问题重新定义为离散码本上的分类问题。这一转换的因果机制可概括为：连续回归需要在无界输出空间中学习复杂的非线性映射，而离散分类将输出空间压缩为有限个码本索引的组合，大幅降低了学习难度。同时，每个 Token 对应手部的一个局部子结构（见 Figure 1），使得局部修改不会通过全局耦合传播误差，从而在保持结构先验的同时实现了局部独立性。

### 2. 技术谱系：VQ-VAE 与组合编码的交叉

TokenHand 的方法论血统可追溯至两条独立发展线：

**离散表示学习线**：受 VQ-VAE 系列工作的启发，TokenHand 将手部点云编码为一组离散 Token，并在共享码本中进行最近邻量化。与原始 VQ-VAE 用于图像生成不同，TokenHand 将量化空间作为一种强结构先验注入重建流水线。码本中每个条目隐式编码了手部某一子结构的典型形态，这种“量化先验”使得后续解码器可以保持轻量化——因为解码器只需学习从码本向量到网格的确定性映射，而非从零开始重建几何。

**组合编码线**：将复杂对象分解为局部部件的组合表示是计算机视觉中的经典思路。TokenHand 的创新在于将这种组合性编码为可学习的离散 Token 集合，而非手工定义的部件模板或参数化模型。Figure 1 的可视化证据表明，改变单个 Token 的值会一致性地修改同一手部子结构，验证了码本确实学到了语义上有意义的局部表示。

**与基线方法的关键差异点**（changed slots）：

| 维度 | 基线方法 | TokenHand |
|------|---------|-----------|
| 重建范式 | 回归 MANO 参数或顶点坐标 | 分类离散 Token 索引 |
| 表示方式 | 连续参数空间或顶点坐标 | M 个离散 Token（码本索引）集合 |
| 解码器 | 每顶点独立预测或模型前向传播 | 预训练并冻结的轻量级级联上采样解码器 |
| 结构先验 | MANO 运动链或非参数插值 | 学习到的共享码本量化先验 |
| 效率 | Transformer/GCNN 高参数成本 | 参数约为基础 Transformer 方法的 10%，推理 65 FPS |

### 3. 效率-精度权衡的突破点

TokenHand 在效率与精度两个维度上同时取得突破，这打破了“实时即妥协精度”的固有认知。Figure 3 的精度-速度散点图清晰展示了这一优势：TokenHand 不仅超越了所有实时方法（≥60 FPS），甚至优于部分非实时方法（≤40 FPS）。

**效率来源的因果链**：两阶段训练策略是关键。第一阶段使用 Point Transformer 编码器学习 Token 表示并训练码本，该阶段的计算开销集中在离线训练中。第二阶段冻结解码器，将图像驱动的重建简化为 Token 分类——这是一个计算量极低的前向过程。具体而言，分类头仅包含 4 个 MLP-Mixer 块用于捕获 Token 间依赖，而解码器是预训练的轻量级级联上采样网络。Table 2 的对比表明，TokenHand 的参数量仅为基础 Transformer 方法的约 10%。

**精度来源的因果链**：量化空间提供的强先验使得轻量级解码器也能产生高质量网格。消融实验（Table 4）表明，码本尺寸在 384 到 640 范围内对 PA-MPJPE 的影响极小（波动在 4.9–5.1 mm），说明码本学习的表示具有高度紧凑性。关键点引导的上采样点采样策略（Table 8）将特征图分辨率提升至 28×28 后，PA-MPJPE 从 6.0 mm 降至 5.7 mm，验证了空间对齐特征对 Token 分类精度的关键作用。

### 4. 适用边界与潜在局限

尽管 TokenHand 在 FreiHAND 和 DexYCB 基准上展现出领先性能，其方法设计隐含了若干适用边界：

**遮挡与手物交互的鲁棒性未充分验证**。DexYCB 数据集包含手-物交互场景，TokenHand 在该数据集上相比 H2ONet 有 1.7 mm MPJPE 和 1.0 mm MPVPE 的提升（Table 3），但严重遮挡场景下的定性表现未在论文中详细展示。离散 Token 表示在部分可观测条件下的稳定性需要进一步检验——当输入图像缺失关键局部信息时，Token 分类可能产生“幻觉式”预测。

**表示粒度的上限问题**。TokenHand 使用 M=389 个 Token 表示手部网格，每个 Token 对应一个局部子结构。对于极度精细的手部姿态（如手指间细微交错或复杂手势），这种固定粒度的离散表示是否足够表达，论文未给出明确分析。码本尺寸的消融实验（Table 4）仅测试了 384–640 的范围，更大码本是否带来边际收益尚不清楚。

**码本覆盖的完备性假设**。第一阶段训练使用的点云数据需要覆盖足够多样的手部姿态，以确保码本学到完备的表示空间。如果训练数据中缺少某些极端姿态，对应的码本条目可能缺失，导致第二阶段分类时无法正确表达这些姿态。论文未讨论码本训练的覆盖度要求或对分布外姿态的泛化能力。

### 5. 开放问题与未来方向

1. **多模态扩展的可能性**：离散 Token 表示天然适合与其他离散模态（如文本 Token）对齐。能否借鉴视觉-语言模型中的对比学习范式，将手部 Token 与手势语义描述关联，实现文本驱动的手部姿态生成或编辑？

2. **遮挡下的鲁棒推理**：当前框架假设输入图像包含完整手部信息。引入不确定性建模（如对每个 Token 预测置信度）或基于扩散模型的迭代细化，可能是提升遮挡鲁棒性的方向。

3. **动态手部重建的时序扩展**：离散 Token 表示的低维度特性使其适合时序建模。将 Token 序列作为视频帧的紧凑中间表示，结合时序 Transformer 进行运动平滑与预测，是自然的延伸方向。

4. **码本的自适应扩展**：当前码本在训练后固定。能否设计增量学习机制，使码本在遇到新姿态时动态扩展，同时保持已有表示的稳定性？这对手部重建在开放世界场景中的部署至关重要。

5. **与其他结构先验的融合**：TokenHand 完全依赖学习到的码本先验，放弃了 MANO 等显式运动学约束。将运动学约束作为正则化项融入 Token 分类过程，可能进一步提升解剖学合理性，尤其是在数据稀缺的姿态区域。

## 原文 PDF

![[paperPDFs/CVPR_2026/TokenHand_Discrete_Token_Representation_for_Efficient_Hand_Mesh_Reconstruction.pdf]]