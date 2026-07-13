---
title: "TGSFormer: Scalable Temporal Gaussian Splatting for Embodied Semantic Scene Completion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TGSFormer_Scalable_Temporal_Gaussian_Splatting_for_Embodied_Semantic_Scene_Completion.pdf
project_link: null
code_link: null
aliases:
- TGSFormer
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入持久高斯记忆 (persistent Gaussian memory) 并联合置信度感知的双时序编码器 (DTE) 与置信度感知体素融合 (CAVF)，直接控制记忆的紧凑性、时序一致性和长时更新能力。
primary_logic: 将高斯基元表示与持续记忆结合，通过置信度感知的时序交叉注意力和体素融合，实现无边界具身探索中可扩展、紧凑且时序一致的 3D 语义场景补全。
claims:
- 在 Occ-ScanNet 和 Occ-ScanNet-mini 上，TGSFormer 的几何与语义完成精度均大幅超越先前最佳方法，IoU 提升达 1.59–4.72%，mIoU 提升达 2.90–6.95%。
- 在 EmbodiedOcc-ScanNet 具身场景补全中，TGSFormer 以大幅减少的基元数量取得 SOTA 性能 (66.19 IoU, 55.82 mIoU)，并在 7/11 语义类别上超越所有对比方法。
- CAVF 模块通过置信度加权合并基元，在维持性能的同时显著降低内存占用，基元特征数和内存大小分别最多降低 11.28× 和 9.92×。
- 置信度感知交叉注意力 (CCA) 的双调制策略（历史值调制和当前注意力输出调制）相比其他调制位置达到最佳性能。
---

# TGSFormer: Scalable Temporal Gaussian Splatting for Embodied Semantic Scene Completion

> [!tip] 核心洞察
> 将高斯基元表示与持续记忆结合，通过置信度感知的时序交叉注意力和体素融合，实现无边界具身探索中可扩展、紧凑且时序一致的 3D 语义场景补全。

| 字段 | 内容 |
|------|------|
| 中文题名 | TGSFormer：面向具身语义场景补全的可扩展时序高斯泼溅 |
| 英文题名 | TGSFormer: Scalable Temporal Gaussian Splatting for Embodied Semantic Scene Completion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00300) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TGSFormer |
| Dataset | Occ-ScanNet, Occ-ScanNet-mini, EmbodiedOcc-ScanNet |

> [!tip] 效果简介
> - Occ-ScanNet 上，IoU 64.42 vs 62.83 (SplatSSC) (+1.59)；mIoU 54.73 vs 51.83 (SplatSSC) (+2.90)。
> - Occ-ScanNet-mini 上，IoU 66.19 vs 61.47 (SplatSSC) (+4.72)；mIoU 55.82 vs 48.87 (SplatSSC) (+6.95)。
> - EmbodiedOcc-ScanNet 上，IoU 66.19 vs previous SOTA (see Tab. 2) (+1.10)。

## 概要

具身场景补全要求智能体在主动探索过程中从连续的局部观测中逐步构建完整、语义一致的 3D 场景表示。现有基于高斯泼溅的方法虽在稀疏性上具备优势，但面临两大根本瓶颈：其一，基元随机初始化依赖预定义的空间边界，导致大量冗余基元，难以拓展至无边界场景；其二，缺乏长期记忆机制，探索过程中的噪声持续积累、内存不断膨胀，无法实现时序一致的渐进式补全。

针对上述问题，本文提出 **TGSFormer**（Scalable Temporal Gaussian Splatting for Embodied Semantic Scene Completion），核心思路是将高斯基元表示与持久记忆机制深度融合，通过置信度感知的时序推理与体素融合，实现可扩展、紧凑且时序一致的 3D 语义场景补全。方法的关键因果调控节点包括：

- **持久高斯记忆（Persistent Gaussian Memory）**：以可增量更新的全局记忆替代逐帧独立预测，赋予模型长期场景保持能力。
- **双时序编码器（Dual Temporal Encoder, DTE）与置信度感知交叉注意力（Confidence-aware Cross Attention, CCA）**：通过置信度调制的时序交叉注意力融合当前与历史基元特征，控制信息流动的稳定性与可靠性。
- **置信度感知体素融合（Confidence-aware Voxel Fusion, CAVF）**：基于联合语义熵与几何不透明度的置信度评分，对同一体素内的基元进行加权合并，直接抑制基元数量与内存的持续增长。

在 **Occ-ScanNet** 与 **Occ-ScanNet-mini** 两个基准上，TGSFormer 的几何与语义完成精度均大幅超越先前最佳方法：IoU 提升 1.59–4.72%，mIoU 提升 2.90–6.95%（Tab. 1）。在 **EmbodiedOcc-ScanNet** 具身场景补全任务中，TGSFormer 以大幅减少的基元数量取得 SOTA 性能（66.19 IoU, 55.82 mIoU），并在 11 个语义类别中的 7 个上超越所有对比方法（Tab. 2）。消融实验进一步验证，CAVF 模块可在维持性能的同时将基元特征数与内存大小分别最多降低 11.28× 和 9.92×（Fig. 8, Tab. 3），CCA 的双调制策略（历史值调制与当前注意力输出调制）相比其他调制位置达到最佳性能（Tab. 6）。

方法定位上，TGSFormer 继承并发展了深度引导的高斯泼溅范式 **SplatSSC**（Qian et al., 2025），同时与基于三视角体素的 **TPVFormer**（Huang et al., CVPR 2023）、稀疏高斯 **GaussianFormer**（Huang et al., ECCV 2024）以及具身场景补全方法 **EmbodiedOcc**（Wu et al., ICCV 2025）等形成系统对比。其关键区分在于：将记忆机制、时序编码器与基元融合统一于置信度感知的持久高斯框架内，从而在可扩展性与时序一致性上实现质变。

当前方法仍存在若干局限：置信度估计主要依赖语义熵，未显式建模深度误差或提升漂移引起的几何不确定性；严重遮挡下的大幅深度误差可能导致提升基元错位，造成时序估计不一致；超长序列中基元数量仍呈线性增长。这些方向为未来的统一不确定性建模与记忆管理机制留下了开放研究空间。



### 具身场景感知中的语义场景补全

语义场景补全（Semantic Scene Completion, SSC）旨在从稀疏观测中同时推理三维几何占据与语义标签，是具身智能体实现环境理解、导航与交互的核心能力。早期 SSC 方法主要面向自动驾驶场景，依赖多相机环视设置与密集深度输入，代表性工作包括 **MonoScene**（Cao and de Charette, CVPR 2022）、**TPVFormer**（Huang et al., CVPR 2023）和 **SurroundOcc**（Wei et al., ICCV 2023）。然而，在室内具身探索场景中，智能体仅携带单目 RGB-D 传感器，需在未知环境中逐步移动并增量式构建完整的 3D 场景表示。这一设定对表示的可扩展性、时序一致性和内存效率提出了更高要求。

### 现有方法的瓶颈

当前面向具身 SSC 的方法大致可分为两类：基于体素/三视角平面的稠密表示方法，以及基于高斯基元的稀疏表示方法。

**稠密表示方法**如 **EmbodiedOcc**（Wu et al., ICCV 2025）和 **EmbodiedOcc++**（Wang et al., MM 2025），通过维护全局体素网格或三视角平面特征来累积观测信息。这类方法面临内存随探索范围线性增长的问题，难以拓展至大规模无边界场景。

**高斯基元方法**如 **GaussianFormer**（Huang et al., ECCV 2024）和 **SplatSSC**（Qian et al., 2025），利用各向异性 3D 高斯分布作为稀疏场景基元，在内存效率上具有天然优势。然而，这些方法存在两个根本性缺陷：

1. **基元初始化依赖预定义空间边界**：现有高斯方法在固定空间范围内随机初始化基元，导致大量冗余基元被分配至空白或不可见区域。当场景边界未知时，这种初始化策略难以有效拓展。

2. **缺乏长期记忆机制**：深度引导的高斯方法（如 SplatSSC）虽能利用深度先验改善基元定位，但缺乏对历史观测的持续记忆与更新能力。随着探索推进，噪声逐步积累，基元数量持续膨胀，导致内存占用不可控且时序一致性下降。

### 核心洞察与本文动机

本文的核心洞察在于：**将高斯基元表示与持续记忆机制结合，通过置信度感知的时序融合与基元合并，可以实现无边界具身探索中可扩展、紧凑且时序一致的 3D 语义场景补全。**

具体而言，TGSFormer 围绕以下三个关键设计展开：

- **持久高斯记忆（Persistent Gaussian Memory）**：维护一个随探索推进而增量更新的全局高斯记忆体，通过特征关联而非帧缓存实现场景表示的持续演化。
- **置信度感知的时序推理**：引入双时序编码器（Dual Temporal Encoder, DTE）与置信度感知交叉注意力（Confidence-aware Cross Attention, CCA），在融合当前与历史基元特征时，依据语义熵和几何不透明度动态调制信息流，抑制低置信度观测的干扰。
- **置信度感知体素融合（Confidence-aware Voxel Fusion, CAVF）**：通过置信度加权合并同一体素内的冗余基元，在维持补全精度的同时显著压缩基元数量与内存占用。

这一设计使得 TGSFormer 在单帧局部预测与具身序列全局补全两个层面均取得了显著提升：在 Occ-ScanNet 上，几何 IoU 与语义 mIoU 分别超越先前最佳方法 1.59% 和 2.90%；在 Occ-ScanNet-mini 上，提升幅度进一步扩大至 4.72% 和 6.95%（Tab. 1）。在具身场景中，TGSFormer 以大幅减少的基元数量取得 SOTA 性能，基元特征数和内存大小分别最多降低 11.28× 和 9.92×（Fig. 8, Tab. 3）。



## 核心方法与创新机理

TGSFormer 的核心创新在于将 **持久高斯记忆 (persistent Gaussian memory)** 引入具身语义场景补全，从根本上改变了现有高斯方法处理时序探索的方式。这一设计直接回应了当前方法面临的核心瓶颈：现有高斯方法（如 **GaussianFormer** (Huang et al., ECCV 2024) 和 **SplatSSC** (Qian et al., 2025)）要么依赖预定义空间边界内的基元随机初始化导致大量冗余，要么缺乏长期记忆机制，在探索过程中面临噪声积累与内存持续膨胀。TGSFormer 通过三个紧密耦合的机制——持久高斯记忆、置信度感知时序编码、置信度感知体素融合——构建了可扩展、紧凑且时序一致的 3D 场景表征。

### 从无记忆到持久高斯记忆

现有方法在每帧独立预测或简单拼接历史基元，缺乏对场景的持续记忆与增量更新能力。TGSFormer 引入全局高斯记忆 $\mathbb{M}_t$，在首帧以局部预测初始化 $\mathbb{M}_1 = \{\mathcal{G}_1, \mathcal{Q}_1\}$，随后通过递推更新 $\mathbb{M}_t = \mathcal{M}_{\mathrm{TGSFormer}}(x_t, \mathbb{M}_{t-1})$ 持续积累场景表征 (Eq.6-7)。这一记忆机制使模型能够在无边界探索中逐步完善对环境的理解，而非每帧从零开始。

### 置信度感知的双时序编码器 (DTE)

简单拼接或单路交叉注意力难以有效融合当前观测与历史记忆，容易引入时序噪声。TGSFormer 的 DTE 采用双路交叉注意力架构，并引入置信度感知调制 (CCA) 来显式控制信息流。具体而言，每个高斯基元的置信度 $C_i$ 由语义熵和几何不透明度联合定义 (Eq.12)：

$$C_i = (1 - \min(H(\tilde{\mathbf{c}}_i)/H_{\max}, 1))^p \cdot \mathbf{a}_i$$

该置信度在 CCA 中施加双重调制：历史值的线性投影被历史置信度 $\hat{C}$ 调制 ($V' = V \odot \hat{C}$)，聚合后的注意力输出被当前置信度 $C_t$ 调制 (Eq.14)。消融实验证实，这种双调制策略（同时作用于 value 和 attention output）相比仅在 query、key 或单位置调制，取得了最佳性能 (Tab. 6)。

### 置信度感知体素融合 (CAVF)

无融合或简单拼接历史基元会导致基元数量随探索线性增长，内存持续膨胀。CAVF 通过置信度加权求和，将落入同一体素内的基元合并为单个紧凑表示 (Eq.16)：

$$\mathcal{G}_s = \sum_{i: V_i = s} w_{i \to s} \mathcal{G}_i,\quad \mathcal{Q}_s = \sum_{i: V_i = s} w_{i \to s} \mathcal{Q}_i$$

这一设计在保持或提升性能的同时，将基元特征数和内存大小分别最多降低 **11.28×** 和 **9.92×** (Fig. 8, Tab. 3)，使 TGSFormer 在长序列探索中维持紧凑且有界的表征。

### 两阶段训练策略

与端到端联合训练不同，TGSFormer 采用两阶段训练：第一阶段在单帧 SSC 上预训练以建立强感知先验，第二阶段冻结其他模块、仅微调 DTE 以学习时序融合。多层监督 (Eq.17-18) 同时作用于 GSE 和 DTE 的输出，使中间表征向最终编码器空间对齐，PCA 可视化显示此策略使特征分布更加各向同性且语义组织更清晰 (Fig. 3)。

### 创新机制间的因果联动

这三个创新并非孤立设计，而是形成因果闭环：持久高斯记忆提供时序上下文，DTE 通过置信度感知交叉注意力实现可靠的时序融合，CAVF 则基于融合后的置信度压缩记忆规模，三者协同实现了无边界探索中可扩展且时序一致的场景补全。在 Occ-ScanNet-mini 上，TGSFormer 以 **66.19 IoU** 和 **55.82 mIoU** 大幅超越先前最佳方法 SplatSSC 达 +4.72% 和 +6.95% (Tab. 1)，并在具身场景中以更少的基元数量取得 SOTA 性能 (Tab. 2)。



TGSFormer 的整体 pipeline 遵循“单帧局部预测—持久记忆维护”两阶段范式，其架构如 **Figure 2** 所示。核心设计动机源于一个关键瓶颈：现有 3D 高斯场景补全方法依赖预定义空间边界内的基元随机初始化，导致大量冗余基元且难以拓展至无边界具身探索场景；而深度引导方法虽有所改进，却缺乏长期记忆机制，造成探索过程中噪声积累与内存持续膨胀。

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our proposed TGSFormer architecture. Our framework first employs parallel image and depth encoders to extract appearance features and geometry priors. These are passed to a Gaussian Lifter (Gs.Lifter) and a Gaussian Encoder (Gs.Encoder) to generate the current set of Gaussian primitives and embeddings. These primitives are then fed into our Dual Temporal Encoder (DTE). The DTE loads historical features queried from the global Gaussian Memory and processes both data streams using two weight-sharing Temporal Encoders. The fused representations are passed to our Confidence-aware Voxel Fusion (CAVF) module, which estimates perprimitive semantic and opacity uncertainty, then perfo...*

为解决这一问题，TGSFormer 引入**持久高斯记忆** (persistent Gaussian memory) 作为核心因果调节变量，并联合**置信度感知的双时序编码器** (Dual Temporal Encoder, DTE) 与**置信度感知体素融合** (Confidence-aware Voxel Fusion, CAVF)，直接控制记忆的紧凑性、时序一致性和长时更新能力。其核心洞察在于：将高斯基元表示与持续记忆结合，通过置信度感知的时序交叉注意力和体素融合，实现无边界具身探索中可扩展、紧凑且时序一致的 3D 语义场景补全。

### 模块关系与数据流

Pipeline 由以下模块按序构成：

1. **图像编码器与深度编码器** (Image Encoder + Depth Encoder)：并行提取外观特征与几何先验（Section 3.2, Fig. 2）。
2. **高斯提升器与高斯编码器** (Gaussian Lifter + Gaussian Encoder, GSE)：将当前帧特征提升为高斯基元及嵌入表示（Section 3.2, Fig. 2）。实验表明，在鲁棒深度先验的配合下，直接提升策略 (direct lifting) 极为有效（Tab. 5a）。
3. **全局高斯记忆** (Global Gaussian Memory)：持久化历史基元与特征，支持时序查询与更新。记忆在 $t=1$ 时由本地预测初始化 $\mathbb{M}_1 = \{\mathcal{G}_1, \mathcal{Q}_1\}$，后续通过 TGSFormer 记忆模块递推更新 $\mathbb{M}_t = \mathcal{M}_{\mathrm{TGSFormer}}(x_t, \mathbb{M}_{t-1})$（Section 3.3, Eq.(6)-(7)）。
4. **双时序编码器** (Dual Temporal Encoder, DTE)：融合当前与历史基元特征，其核心是**置信度感知交叉注意力** (Confidence-aware Cross Attention, CCA)。CCA 通过双调制策略——历史值 $\mathbf{V}$ 由历史置信度 $\hat{C}$ 调制形成 $\mathbf{V}' = \mathbf{V} \odot \hat{C}$，聚合注意力输出由当前置信度 $C_t$ 调制——实现可靠的时序推理（Section 3.3, Eq.(8)-(14)）。
5. **置信度感知体素融合** (CAVF)：通过置信度加权求和合并同一体素内的基元 $\mathcal{G}_s = \sum_{i: V_i = s} w_{i \to s} \mathcal{G}_i$，控制基元密度与内存占用（Section 3.3, Eq.(15)-(16)）。
6. **高斯到体素泼溅与聚合器** (Gaussian-to-Voxel Splatting & Aggregator)：将合并后的高斯基元渲染为语义体素网格，通过空概率渲染 $\alpha(\mathbf{x}) = 1 - \prod_{i \in \mathcal{N}(\mathbf{x})} (1 - \alpha(\mathbf{x}; G_i) \cdot \mathbf{a}_i)$ 和语义概率渲染完成场景补全（Section 3.1, Eq.(2)-(5)）。

### 训练策略

TGSFormer 采用**两阶段训练**策略（Section 3.4）：第一阶段在单帧 SSC 上预训练，建立强感知先验；第二阶段针对具身预测进行微调，仅更新 DTE 而冻结其余组件，促使 DTE 学习时序融合而不破坏已学到的单帧表示。训练损失采用多层监督下的加权 SSC 损失 $\mathcal{L}_{\mathrm{total}} = \sum_{j=1}^{n} w_j \mathcal{L}_{\mathrm{ssc}}^j$（Eq.(18)），其中 $\mathcal{L}_{\mathrm{ssc}} = \lambda_1 \mathcal{L}_{\mathrm{focal}} + \lambda_2 \mathcal{L}_{\mathrm{lovasz}} + \mathcal{L}_{\mathrm{scale}}^{\mathrm{geo}}$。

### 与基线方法的关键差异

相较于现有方法，TGSFormer 在四个关键维度上进行了系统性改进：

| 模块槽位 | 基线方法 | TGSFormer 方案 | 证据锚点 |
|---------|---------|---------------|---------|
| 记忆机制 | 无持续记忆/每帧独立预测（如 SplatSSC, Qian et al., 2025） | 持久高斯记忆 + 增量更新 | Section 3.3, Eq.(6)-(7) |
| 时序编码器 | 无时序融合或简单拼接 | DTE + 置信度感知交叉注意力 | Section 3.3, Eq.(8)-(14) |
| 基元融合 | 无融合或简单拼接历史基元 | 置信度感知体素融合 (CAVF) | Section 3.3, Eq.(15)-(16) |
| 训练策略 | 端到端联合训练 | 两阶段训练 + 多层监督 | Section 3.4, Eq.(17)-(18) |

这些设计使 TGSFormer 在 Occ-ScanNet 和 Occ-ScanNet-mini 上分别以 64.42 IoU / 54.73 mIoU 和 66.19 IoU / 55.82 mIoU 超越先前最佳方法 SplatSSC（Tab. 1），几何 IoU 提升达 1.59–4.72%，语义 mIoU 提升达 2.90–6.95%。在具身场景 EmbodiedOcc-ScanNet 中，TGSFormer 以大幅减少的基元数量取得 SOTA 性能（66.19 IoU, 55.82 mIoU），并在 7/11 语义类别上超越所有对比方法（Tab. 2, Section 4.1）。

### 补充图表

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/001_Figure_1.jpg]]
*Figure 1: Overview of embodied scene exploration and refinement. Our TGSFormer consistently expands its understanding of the environment as new views are observed and progressively refines previously seen regions, producing a complete and coherent 3D scene*

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/011_Figure.jpg]]
*Figure: (b) Modulate position illustration*



TGSFormer 的核心架构由五个关键模块串联构成，其设计围绕一个核心目标：在无边界具身探索中维持紧凑、时序一致的高斯场景记忆。图 Figure 2 给出了整体架构概览。

### 3.1 高斯泼溅与体素渲染

TGSFormer 将场景表示为各向异性的 3D 高斯基元集合。每个基元 $G_i$ 由位置 $\mu_i$、协方差 $\Sigma_i$、不透明度 $\mathbf{a}_i$ 和语义特征 $\tilde{\mathbf{c}}_i$ 定义。协方差矩阵由尺度 $\mathbf{s}_i$ 和旋转四元数 $\mathbf{q}_i$ 参数化：

$$
\pmb{\Sigma}_i = \mathbf{R}_i \mathbf{S}_i \mathbf{S}_i^T \mathbf{R}_i^T,\ \mathbf{S}_i = \mathrm{diag}(\mathbf{s}_i),\ \mathbf{R}_i = \mathrm{q2r}(\mathbf{q}_i) \tag{1}
$$

将高斯基元渲染为语义体素网格时，体素中心 $\mathbf{x}$ 处的空概率通过邻域基元的累积透射率计算：

$$
\alpha (\mathbf{x}) = 1 - \prod_{i \in \mathcal{N}(\mathbf{x})} \big(1 - \alpha (\mathbf{x}; G_i) \cdot \mathbf{a}_i\big) \tag{2}
$$

语义类别 $l$ 的概率则通过高斯核加权聚合：

$$
e^l(\mathbf{x}) = \frac{\sum_{i \in \mathcal{N}(\mathbf{x})} p(\mathbf{x}|G_i) \cdot \tilde{\mathbf{c}}_i^l}{\sum_{j \in \mathcal{N}(\mathbf{x})} p(\mathbf{x}|G_j)} \tag{3}
$$

其中归一化高斯核权重为：

$$
p(\mathbf{x}|G_i) = \frac{1}{(2\pi)^{3/2} |\Sigma_i|^{1/2}} \alpha (\mathbf{x}; G_i) \tag{4}
$$

### 3.2 图像/深度编码器与高斯提升器

当前帧 $x_t$ 首先经过并行的图像编码器和深度编码器，分别提取外观特征与几何先验。随后，高斯提升器 (Gaussian Lifter) 利用深度先验将 2D 特征直接提升为 3D 高斯基元，高斯编码器 (Gaussian Encoder, GSE) 进一步将其编码为基元嵌入 $\mathcal{Q}_t$。论文指出，当配合鲁棒的深度先验时，这种直接提升策略极为有效（消融验证见 Table 5a）。

### 3.3 持久高斯记忆与双时序编码器

这是 TGSFormer 区别于现有方法的核心创新。传统高斯方法缺乏持续记忆，导致探索过程中噪声积累与内存膨胀。TGSFormer 引入**持久高斯记忆** (persistent Gaussian memory) $\mathbb{M}_t$，在时间维度上累积并更新场景表示：

$$
\mathbb{M}_1 = \{\mathcal{G}_1, \mathcal{Q}_1\} \tag{6}
$$

$$
\mathbb{M}_t = \mathcal{M}_{\mathrm{TGSFormer}}(x_t, \mathbb{M}_{t-1}) \tag{7}
$$

记忆的更新由**双时序编码器** (Dual Temporal Encoder, DTE) 完成。DTE 从全局高斯记忆中查询历史特征 $\hat{\mathcal{Q}}$，与当前帧特征 $\mathcal{Q}_t$ 分别送入两个权重共享的时序编码器。融合过程的核心是**置信度感知交叉注意力** (Confidence-aware Cross Attention, CCA)，其关键设计是双调制策略：

1. **值调制**：历史 Value $\mathbf{V}$ 经线性投影后，与历史置信度 $\hat{C}$ 逐元素相乘，形成 $\mathbf{V}' = \mathbf{V} \odot \hat{C}$，抑制低置信度历史信息的干扰。
2. **输出调制**：多头注意力聚合后的输出，再与当前置信度 $C_t$ 逐元素相乘，确保当前帧中不确定区域的贡献被削弱。

完整的 CCA 计算为：

$$
\operatorname{CCA}(\mathcal{Q}_t, \hat{\mathcal{Q}}, C_t, \hat{C}) = \bigl(\operatorname{Concat}(\operatorname{MHA}(\mathrm{Q}, \mathrm{K}, \mathrm{V}')) \odot C_t\bigr) W_o \tag{14}
$$

### 3.4 基元置信度估计

置信度 $C_i \in [0,1]$ 是控制信息流的关键旋钮，它联合评估语义不确定性与几何稳定性。语义不确定性由预测类别概率的香农熵量化：

$$
H(\tilde{\mathbf{c}}_i) = -\sum_{k=1}^{C-1} \tilde{\mathbf{c}}_i^k \log(\tilde{\mathbf{c}}_i^k) \tag{11}
$$

最终置信度将归一化熵与几何不透明度 $\mathbf{a}_i$ 结合：

$$
C_i = (1 - \min(H(\tilde{\mathbf{c}}_i)/H_{\max}, 1))^p \cdot \mathbf{a}_i \tag{12}
$$

其中幂指数 $p$ 控制置信度对熵的敏感程度。这一设计使语义模糊或几何不稳定的基元在后续融合中自动降权。

### 3.5 置信度感知体素融合

为抑制基元数量的持续增长，TGSFormer 在 DTE 之后引入**置信度感知体素融合** (Confidence-aware Voxel Fusion, CAVF)。落入同一体素 $s$ 的基元通过置信度加权求和合并：

$$
\mathcal{G}_s = \sum_{i: V_i = s} w_{i \to s} \mathcal{G}_i,\quad \mathcal{Q}_s = \sum_{i: V_i = s} w_{i \to s} \mathcal{Q}_i \tag{16}
$$

其中权重 $w_{i \to s}$ 由基元置信度决定。合并后的基元再经高斯泼溅渲染为最终语义体素网格。CAVF 在维持性能的同时，将基元特征数和内存占用分别最多降低 11.28× 和 9.92×（见 Table 3 和 Figure 8）。

### 3.6 训练策略与多层监督

TGSFormer 采用两阶段训练策略：第一阶段在单帧 SSC 上预训练，建立强感知先验；第二阶段冻结除 DTE 外的所有组件，仅微调 DTE 以学习时序融合。训练损失为多层监督下的加权 SSC 损失：

$$
\mathcal{L}_{\mathrm{total}} = \sum_{j=1}^{n} w_j \mathcal{L}_{\mathrm{ssc}}^j \tag{18}
$$

其中 $\mathcal{L}_{\mathrm{ssc}}$ 由 focal loss、Lovász loss 和几何尺度损失组成，对 GSE 和 DTE 的输出均施加监督（Stages 0–2），以促进中间特征向最终编码器空间对齐。Figure 3 的 PCA 可视化表明，该多阶段监督使高斯特征分布更加各向同性且在语义上更有组织。

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/003_Figure_3.jpg]]
*Figure 3: Feature alignment visualization with Principal Component Analysis (PCA). PCA projections of Gaussian features show that our multi-stage objective not only aligns intermediate representations toward the final encoder space, but also makes their distributions more isotropic and semantically organized*



## 实验与关键发现

### 主实验结果

**单帧场景补全。** TGSFormer 在 Occ-ScanNet 和 Occ-ScanNet-mini 两个基准上均取得最优性能（Tab. 1）。在 Occ-ScanNet 上，几何 IoU 达到 64.42，较先前最佳方法 **SplatSSC**（Qian et al., 2025）的 62.83 提升 1.59%；语义 mIoU 达到 54.73，较 SplatSSC 的 51.83 提升 2.90%。在更具挑战性的 Occ-ScanNet-mini 上，优势进一步扩大：IoU 提升 4.72%（66.19 vs. 61.47），mIoU 提升 6.95%（55.82 vs. 48.87）。这一结果表明，TGSFormer 的深度引导提升策略与高斯编码器设计在单帧语义场景补全中已具备显著优势，为后续时序推理提供了强感知先验。

**具身场景补全。** 在 EmbodiedOcc-ScanNet 基准上（Tab. 2），TGSFormer 以 66.19 IoU 和 55.82 mIoU 取得最优性能，在 11 个语义类别中的 7 个上超越所有对比方法。相较于 **EmbodiedOcc**（Wu et al., ICCV 2025）、**EmbodiedOcc++**（Wang et al., MM 2025）等专门设计的具身 SSC 方法，TGSFormer 在几何完整性和语义一致性上均表现更优。值得注意的是，该性能是在基元数量大幅减少的前提下实现的（见下文效率分析），验证了持久高斯记忆与置信度感知融合机制在无边界探索场景中的有效性。

### 消融实验

**CAVF 模块。** Tab. 3 系统消融了置信度感知体素融合（CAVF）的设计选择。实验表明，采用 0.12m 体素尺寸并引入置信度加权的设定达到最佳性能-效率权衡：相比不融合的基线，基元特征数和内存占用分别最多降低 11.28× 和 9.92×，同时 mIoU 保持稳定甚至略有提升。仅依赖空间合并（无置信度加权）会导致语义精度明显下降，验证了置信度评分在区分可靠基元与噪声基元中的关键作用。

**训练策略与特征对齐。** Tab. 4 验证了多阶段监督策略的贡献。对高斯场景编码器（GSE）和双时序编码器（DTE）的输出均施加 SSC 监督（Stages 0,1,2）可获得最佳具身补全性能。PCA 可视化（Fig. 3）进一步表明，多阶段目标不仅使中间表示向最终编码器空间对齐，还使其分布更加各向同性和语义结构化，从而为时序融合提供更稳定的特征基础。

**时序编码器设计。** Tab. 5b 对比了不同时序处理策略。无时序建模的基线性能最低；引入单路交叉注意力（single CA）带来显著提升；双路交叉注意力（dual CA）进一步改善；在此基础上加入置信度调制（dual CA + conf.）达到最优。这表明，双向信息流动与置信度感知门控对于稳定时序推理缺一不可。

**CCA 调制策略。** Tab. 6 详细消融了置信度感知交叉注意力（CCA）中的调制位置。实验对比了仅调制 Query、仅调制 Key、仅调制 Value、仅调制 Attention Output，以及同时调制 Value 和 Attention Output 五种策略。结果表明，同时对历史 Value 进行置信度调制（$V' = V \odot \hat{C}$）和对聚合后的注意力输出进行当前置信度调制（$C_v$ 和 $C_a$）的双调制策略取得最佳性能，验证了在信息流入和流出两端同时施加置信度控制的设计合理性。

### 效率分析

Fig. 7 展示了具身序列中单帧推理延迟与 mIoU 的关系。EmbodiedOcc 因持续累积高斯特征和记忆条目导致延迟最高；TGSFormer 受益于轻量级高斯提升器、DTE 和 CAVF 模块，在取得最高 mIoU 的同时保持最低推理延迟。

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/015_Figure_7.jpg]]
*Figure 7: Single-frame inference latency versus mIoU in Embodied Sequence. All models share comparable parameter counts. EmbodiedOcc incurs the highest latency due to accumulating Gaussian features and memory entries. TGSFormer achieves both the lowest latency and the highest mIoU, benefiting from its lightweight Gaussian Lifter, DTE, and CAVF modules*

Fig. 8 进一步揭示了基元与内存的增长模式。EmbodiedOcc 呈现无界增长，SplatSSC 因缺乏时序调控而稳定累积，而 TGSFormer 通过 CAVF 维持紧凑且有界的高斯表示，基元特征数和内存大小分别最多降低 11.28× 和 9.92×。

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/017_Figure_8.jpg]]
*Figure 8: Efficiency comparison in Embodied Sequence. EmbodiedOcc shows unbounded growth in Gaussian features and memory, while SplatSSC exhibits steady accumulation due to the lack of temporal regulation. TGSFormer maintains a compact and bounded Gaussian representation through CAVF, resulting in up to 11.28× and 9.92× reductions in feature count and memory size, respectively*

### 失败模式与局限

Fig. 9 展示了严重遮挡场景下的典型失败案例。当深度估计在遮挡区域产生大幅误差时（图中 GT 深度以彩色标注，预测深度以粉色标注），提升的高斯基元发生空间错位，导致当前帧的占据预测与历史估计不一致。这一现象揭示了当前方法的两个根本局限：其一，置信度估计主要基于语义熵（Eq. 12），未显式建模深度误差或提升漂移引起的几何不确定性；其二，尽管 CAVF 大幅减缓了基元增长，但在超长序列探索中基元数量仍线性增加，长期记忆的紧凑性与一致性仍需进一步增强。

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/018_Figure_9.jpg]]
*Figure 9: Failure case on Temporal-Occ-ScanNet-mini. Large depth errors under severe occlusion (GT in color vs. prediction in pink) lead to misaligned lifted Gaussians, causing inconsistent occupancy between the current frame and the historical estimate*

初步尝试将渲染置信度用于训练损失重加权（Tab. 9）反而导致性能微降，表明高斯基元表示下的不确定性驱动损失设计仍需深入研究。

### 补充图表

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/010_Table_3.jpg]]
*Table 3: Ablation on CAVF. The results of our proposed setting are highlighted in light gray*

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/006_Table_1.jpg]]
*Table 1: Local Prediction Performance on the Occ-ScanNet and Occ-ScanNet-mini dataset. The best results are highlighted in bold , while the second-best are underlined*

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/007_Table_2.jpg]]
*Table 2: Embodied Prediction Performance on the EmbodiedOcc-ScanNet dataset. The best results are highlighted in bold , while the second-best are underlined*

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/009_Table_5.jpg]]
*Table 5: Ablation on Gaussian Initialization and Temporal Encoder. (a) Different settings for depth cue. (b) Study on different temporal processing strategies. Including the baseline without temporal modeling, single cross attention (ca), and dual cross attention (dual ca) variants, with or without confidence modulation*

![[assets/figures/papers/paper_list_l2280_https_arxiv_org_abs_2512_00300/figures/012_Table_6.jpg]]
*Table 6: Ablation on CCA modulation strategies. We compare the confidence modulation on the query*



## 定位与知识库关联

### 1. 方法谱系：从稀疏高斯到持久记忆

TGSFormer 处于“稀疏高斯基元 × 具身语义场景补全”的交汇点，其直接前驱是 **SplatSSC**（Qian et al., 2025）和 **EmbodiedOcc**（Wu et al., ICCV 2025）。

**与 SplatSSC 的关系——继承与突破。** SplatSSC 首次将深度引导的高斯提升引入 SSC，证明直接提升策略在鲁棒深度先验下高度有效。TGSFormer 在单帧局部预测阶段基本沿用该范式（Image Encoder + Depth Encoder → Gaussian Lifter → Gaussian Encoder），但在两个关键维度上实现突破：其一，SplatSSC 缺乏持续记忆机制，每帧独立预测，无法利用时序信息；其二，SplatSSC 对基元增长无约束，探索过程中内存持续膨胀。TGSFormer 通过引入 **持久高斯记忆** 和 **置信度感知体素融合（CAVF）** 直接解决这两个瓶颈。

**与 EmbodiedOcc 的关系——范式继承与架构重构。** EmbodiedOcc 建立了“帧无关具身范式”，将 SSC 从固定边界场景拓展到无边界探索。但其基元随机初始化策略导致大量冗余基元，且缺乏长期记忆管理，造成噪声积累与内存线性增长。TGSFormer 继承其具身设定，但以 **双时序编码器（DTE）** 替代简单拼接，以 **置信度感知交叉注意力（CCA）** 替代无差别特征融合，以 CAVF 替代无约束基元累积，在架构层面实现了从“帧缓存”到“特征关联”的范式转换。

**与其他基线的对比定位。** 在单帧 SSC 维度，TGSFormer 显著超越基于体素/三视角表示的 **TPVFormer**（Huang et al., CVPR 2023）、单目方法 **MonoScene**（Cao and de Charette, CVPR 2022）以及室内 SSC 方法 **ISO**（Yu et al., ECCV 2024），表明稀疏高斯表示在几何-语义联合建模上的优势。在具身维度，TGSFormer 同样优于 **EmbodiedOcc++**（Wang et al., MM 2025）和 **RoboOcc**（Zhang et al., 2025），证明置信度感知时序融合与记忆压缩的有效性。

### 2. 核心因果机制

TGSFormer 的性能优势源于一个因果闭环（causal knob）：**置信度估计 → 信息流调制 → 记忆紧凑性控制**。

**置信度作为统一门控信号。** 基元置信度 $C_i$ 由语义熵和几何不透明度联合定义（Eq. 12），同时承载“该基元知道什么”和“该基元是否稳定”两类信息。这一设计使置信度成为贯穿 DTE 和 CAVF 的统一门控信号——在 CCA 中，历史置信度 $\hat{C}$ 调制 Value 投影（$V' = V \odot \hat{C}$），当前置信度 $C_t$ 调制聚合后的注意力输出（Eq. 14），形成双调制策略；在 CAVF 中，置信度作为融合权重控制同体素内基元的合并（Eq. 16）。消融实验证实：双调制优于仅在 Query 或 Key 处调制（Tab. 6），且置信度加权的体素融合在 0.12m 体素尺寸下达到性能-效率最佳权衡（Tab. 3）。

**两阶段训练作为特征对齐机制。** 第一阶段单帧预训练建立强感知先验，第二阶段仅微调 DTE 而冻结其他组件，迫使 DTE 在几何和语义两个维度上对齐当前与历史特征。PCA 可视化（Fig. 3）显示，多阶段监督不仅使中间表示向最终编码器空间对齐，还使其分布更加各向同性和语义结构化，这解释了为何同时对 GSE 和 DTE 输出施加监督（Stages 0,1,2）能获得最佳具身补全性能（Tab. 4）。

### 3. 适用边界

**强适用场景。** TGSFormer 在以下条件下表现最优：(1) 深度先验相对可靠（如室内 RGB-D 序列），直接提升策略能产生高质量初始基元；(2) 探索轨迹覆盖场景主要区域，时序信息可有效互补单帧遮挡；(3) 场景语义类别分布相对均衡，语义熵能有效反映预测不确定性。

**弱适用场景与已知失效模式。** (1) **严重遮挡下的深度误差**——当深度估计大幅偏离真值时，提升的高斯基元空间位置错位，导致当前帧与历史估计不一致（Fig. 9 失败案例）；(2) **超长序列探索**——尽管 CAVF 将基元特征数和内存大小分别最多降低 11.28× 和 9.92×（Fig. 8），基元数量仍呈线性增长，长期一致性未彻底解决；(3) **几何不确定性盲区**——当前置信度仅基于语义熵，未显式建模深度误差或提升漂移引起的几何不确定性，可能影响时序对齐精度。

### 4. 局限与开放问题

**已识别的局限。** (1) 置信度估计的单模态缺陷——语义熵无法感知几何噪声，深度误差较大的基元可能被赋予高置信度，污染记忆更新；(2) 直接使用渲染置信度对训练损失重加权的初步尝试导致性能微降，表明高斯基元下的不确定性感知损失设计仍需探索；(3) CAVF 的体素划分粒度是固定的超参数，缺乏对场景局部密度的自适应能力。

**开放问题。** (1) 如何设计统一的语义-几何不确定性估计器，使其与高斯记忆的读写操作深度集成？(2) 能否引入类 RNN 或状态空间机制（如 Mamba）来管理高斯记忆的隐状态，以彻底抑制长期序列中的基元漂移与线性增长？(3) 当前两阶段训练策略在 DTE 微调时冻结其他组件，是否存在更优的端到端联合训练方案，在保持单帧能力的同时提升时序适应性？



## 原文 PDF

![[paperPDFs/CVPR_2026/TGSFormer_Scalable_Temporal_Gaussian_Splatting_for_Embodied_Semantic_Scene_Completion.pdf]]
