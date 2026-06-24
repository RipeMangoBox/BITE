---
title: "SR3R: Rethinking Super-Resolution 3D Reconstruction With Feed-Forward Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SR3R_Rethinking_Super_Resolution_3D_Reconstruction_With_Feed_Forward_Gaussian_Splatting.pdf
project_link: "https://xiangfeng66.github.io/SR3R/"
code_link: null
aliases:
- SR3R
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将3DSR重新定义为从稀疏低分辨率视图到高分辨率3DGS的直接前馈映射，通过多场景数据学习广义映射函数，替代逐场景优化与2DSR伪监督。
primary_logic: 通过前馈映射网络从大规模多场景数据自主习得3D高频结构，取代继承自2D超分模型的有限先验，是实现高保真、可泛化且即插即用的3D超分的关键。
claims:
- SR3R直接从稀疏LR视图预测HR 3DGS，无需2DSR伪监督和逐场景优化。
- SR3R从大规模多场景数据学习跨场景广义映射，自主获取3D高频结构。
- 提出的高斯偏移学习和特征细化能锐化高频细节并稳定重建。
- RE10K (4× 3DSR, 64×64 → 256×256) 上 PSNR↑ = 26.250 (Ours, DepthSplat)
---

# SR3R: Rethinking Super-Resolution 3D Reconstruction With Feed-Forward Gaussian Splatting

> [!tip] 核心洞察
> 通过前馈映射网络从大规模多场景数据自主习得3D高频结构，取代继承自2D超分模型的有限先验，是实现高保真、可泛化且即插即用的3D超分的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | SR3R：重新思考基于前馈高斯泼溅的超分辨率三维重建 |
| 英文题名 | SR3R: Rethinking Super-Resolution 3D Reconstruction With Feed-Forward Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24020) · [Project](https://xiangfeng66.github.io/SR3R/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SR3R |
| Dataset | RE10K, ACID, RE10K→DTU, RE10K→ScanNet++ |

> [!tip] 效果简介
> - RE10K (4× 3DSR, 64×64 → 256×256) 上，PSNR↑ 26.250 (Ours, DepthSplat) vs 23.147 (DepthSplat) (+3.103)。
> - ACID (4× 3DSR, 64×64 → 256×256) 上，PSNR↑ 27.018 (Ours, DepthSplat) vs 23.801 (DepthSplat) (+3.217)。
> - RE10K→DTU (zero-shot, 4× SR) 上，PSNR↑ 17.241 (Ours, NoPoSplat) vs 12.628 (NoPoSplat) (+4.613)。

## 概述

**瓶颈**：现有基于3DGS的三维超分辨率（3DSR）方法依赖预训练的二维超分模型提供高频先验，并采用逐场景优化，难以从大规模多场景数据中自主学习三维特异的高频几何与纹理，导致重建保真度、跨场景泛化性和实时性受限。

**核心思路**：SR3R将3DSR重新定义为从稀疏低分辨率视图到高分辨率3DGS的直接前馈映射，通过在大规模多场景数据上学习广义映射函数，替代逐场景优化与二维超分伪监督，使网络自主习得三维高频结构。

**方法定位**：SR3R是一种即插即用的前馈框架——首先利用任意预训练的前馈3DGS重建模型（如**NoPoSplat** (Ye et al., ICLR 2025) 或 **DepthSplat** (Xu et al., CVPR 2025)）从稀疏LR视图估计LR 3DGS骨架，经高斯洗牌分裂稠密化后，由映射网络预测残差偏移以恢复高频细节。关键创新包括：高斯偏移学习替代直接回归绝对参数，提升训练稳定性与纹理保真度；特征细化模块通过交叉注意力对齐二维编码特征与三维几何先验。

**主要结果**：在RE10K和ACID数据集上，SR3R以4倍超分（64×64→256×256）显著超越所有前馈基线（PSNR提升+3.1–3.2 dB），并展现出强零样本泛化能力——在DTU和ScanNet++上分别超越逐场景优化方法**SRGS** (Feng et al., arXiv 2024) 达+4.6 dB和+3.5 dB，同时推理速度远快于优化式方法。消融实验证实，高斯偏移学习是贡献最大的单一模块，且SR3R对不同上采样策略具有鲁棒性。

## 背景与动机

三维场景的超分辨率重建（3D Super-Resolution, 3DSR）旨在从低分辨率（LR）输入恢复高分辨率（HR）的三维表示，是增强沉浸式视觉体验和三维内容生成质量的关键技术。近年来，3D Gaussian Splatting（3DGS）凭借其显式点云结构和可微分光栅化的高效渲染能力，已成为三维重建的主流表示形式，并推动了3DSR方法的发展。

然而，现有基于3DGS的3DSR方法存在一个根本性瓶颈：**它们普遍依赖预训练的2D超分模型提供高频先验，并采用逐场景优化（per-scene optimization）策略**。具体而言，这类方法通常先利用2DSR模型对输入视图进行上采样，生成伪高分辨率图像作为监督信号，再通过密集多视图输入对每个场景独立优化3DGS参数。这种范式带来了三个核心缺陷：

1. **高频先验来源受限**：模型继承的是2DSR模型中嵌入的有限先验，而非直接从三维数据中习得的3D特异高频几何与纹理结构，导致重建保真度存在上限。
2. **跨场景泛化能力弱**：逐场景优化意味着每个新场景都需要重新运行完整的优化流程，无法从大规模多场景数据中学习广义的映射函数，泛化效率极低。
3. **实时性不足**：密集视图输入和迭代优化的计算开销巨大，难以满足即插即用的实时应用需求。

上述缺陷的根本原因在于，现有方法将3DSR视为一个“2DSR伪监督+3DGS自优化”的间接过程，而非一个可直接学习的映射问题。这限制了模型自主获取三维高频结构的能力，也阻碍了从数据驱动角度实现高效泛化的可能性。

针对这一缺口，**SR3R** 提出了一种范式层面的重新思考：将3DSR重新定义为从稀疏低分辨率视图到高分辨率3DGS的**直接前馈映射**问题。其核心洞察在于——通过一个可学习的映射网络从大规模多场景数据中自主习得3D高频结构，取代继承自2D超分模型的有限先验，是实现高保真、可泛化且即插即用的三维超分的关键。

具体而言，SR3R首先利用任意预训练的前馈3DGS重建模型（如 **NoPoSplat**（Ye et al., ICLR 2025）或 **DepthSplat**（Xu et al., CVPR 2025））从稀疏LR视图估计一个LR 3DGS骨架，随后通过所提出的映射网络将其上变换为HR 3DGS。该映射网络包含高斯偏移学习（Gaussian Offset Learning）和特征细化（Feature Refinement）两个核心机制，前者通过学习残差偏移而非直接回归绝对HR参数来稳定训练并锐化高频细节，后者通过双向交叉注意力对齐2D编码特征与3D几何感知令牌，增强结构一致性。整个流程无需2DSR伪监督和逐场景优化，仅需两幅LR视图即可完成前馈推理。

> **证据说明**：以下背景与动机分析基于论文摘要、引言及方法总述部分的声明。关于SR3R各模块的具体设计细节和实验验证，将在后续章节中详述。

## 核心创新

SR3R 的核心创新在于对 3D 超分辨率（3DSR）范式的根本性重构：**将 3DSR 从依赖 2DSR 伪监督的逐场景优化问题，重新定义为从稀疏低分辨率（LR）视图到高分辨率 3DGS 的直接前馈映射问题**。这一范式转换催生了三个关键 changed slots，共同构成了方法的技术骨架。

### 范式转换：从逐场景优化到跨场景前馈映射

现有 3DGS-based 3DSR 方法（如 **SRGS** (Feng et al., arXiv 2024)）遵循一条固定路径：以稠密多视图为输入，利用预训练 2DSR 模型提供高频先验，再通过逐场景的 3DGS 自优化生成 HR 重建。这条路径存在两个根本性瓶颈：

1. **高频知识来源受限**：模型继承的是 2DSR 模型中嵌入的有限先验，而非从 3D 数据中直接习得的 3D 特异高频结构。
2. **泛化性与实时性不足**：逐场景优化无法从大规模多场景数据中学习广义映射函数，导致跨场景泛化能力弱，且推理耗时。

SR3R 的解决方案是学习一个前馈映射网络 $f_{\pmb \theta} : \{ ( I_{lr}^v , K^v ) \}_{v=1}^V \mapsto \mathcal G^{\mathrm{HR}}$（Eq. 1），直接从稀疏 LR 视图预测 HR 3DGS 表示，**完全消除对 2DSR 伪监督和逐场景优化的依赖**。这一范式转换的因果作用在于：网络通过大规模多场景数据自主习得 3D 特异高频结构，而非继承 2DSR 模型的有限先验。证据来自 RE10K→DTU 零样本实验：SR3R 以 +4.613 PSNR 的显著优势超越前馈基线 NoPoSplat，甚至优于逐场景优化的 SRGS（Table 2），直接验证了跨场景映射函数的泛化能力。

### 高斯偏移学习：替代直接回归的稳定训练策略

第二个关键创新在于**高斯参数预测方式的改变**。基线方法直接回归绝对 HR 高斯参数，这在稀疏 LR 输入下容易导致训练不稳定和纹理模糊。SR3R 改为学习**残差偏移**（residual offsets）：先通过前馈 3DGS 骨干（如 **NoPoSplat** (Ye et al., ICLR 2025) 或 **DepthSplat** (Xu et al., CVPR 2025)）估计 LR 3DGS 骨架，经高斯洗牌分裂（Gaussian Shuffle Split）稠密化后形成结构骨架 $\mathcal{G}^{\mathrm{Dense}}$，再由映射网络预测从 $\mathcal{G}^{\mathrm{Dense}}$ 到 $\mathcal{G}^{\mathrm{HR}}$ 的残差偏移 $\Delta \mathcal{G}$（Eq. 7）。

这一设计带来双重收益：
- **训练稳定性**：学习偏移比直接回归完整参数更稳定，因为稠密骨架已提供合理的几何与纹理初始化。
- **高频保真度**：消融实验（Table 3）显示，高斯偏移学习是**效果提升最大的单一模块**，且将需要学习的高斯参数数量从 44.5M 降至 16.0M，显著降低了优化难度。

### 特征细化与空间推理：2D-3D 特征对齐

第三个创新点是**特征细化模块**（Feature Refinement Module），通过双向交叉注意力（Eq. 4）将 ViT 编码器的 2D 图像特征与预训练 3DGS 骨干的几何感知令牌对齐。这一设计解决了前馈映射中的核心矛盾：上采样后的 2D 特征缺乏 3D 几何一致性，而 3DGS 骨架的几何先验需要与纹理细节融合。

消融实验证明了该模块的因果作用：在基础模型上叠加交叉注意力后，PSNR 从 23.374 提升至 23.504（Table 3），定性结果（Figure 4）显示结构一致性明显改善。进一步引入 PointTransformerV3 进行空间推理后，模型达到最佳表现（PSNR 24.794），验证了 3D 空间推理对偏移预测精度的关键贡献。

### 创新点的协同效应

三个 changed slots 并非孤立改进，而是形成因果闭环：范式转换（前馈映射）提供了从多场景数据学习 3D 高频结构的可能性；高斯偏移学习确保了在稀疏 LR 输入下的训练稳定性与参数效率；特征细化弥合了 2D 特征与 3D 几何之间的模态鸿沟。三者共同实现了 SR3R 的核心洞察：**通过前馈映射网络从大规模多场景数据自主习得 3D 高频结构，取代继承自 2D 超分模型的有限先验**。

## 整体框架

SR3R 将三维超分辨率（3DSR）重新定义为一种前馈映射问题：从稀疏低分辨率（LR）视图直接预测高分辨率（HR）三维高斯泼溅（3DGS）表示。其核心映射关系为：

$$f_{\pmb \theta} : \{ ( I_{lr}^v , K^v ) \}_{v=1}^V \mapsto \mathcal G^{\mathrm{HR}}$$

给定 $V$ 幅 LR 视图 $\{I_{lr}^v\}$ 及其相机内参 $\{K^v\}$，网络 $f_{\pmb \theta}$ 直接输出目标 HR 3DGS $\mathcal G^{\mathrm{HR}}$，无需任何 2D 超分模型的伪监督或逐场景优化。这一范式转变的根本意义在于：高频知识的来源从“继承自预训练 2DSR 模型的有限先验”变为“从大规模多场景数据中自主习得的 3D 特异高频结构”。

框架整体由两条并行的信息流构成（见 Figure 2），最终通过残差组合汇合为 HR 3DGS。

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SR3R framework. Given two LR input views, a feed-forward 3DGS backbone produces an LR 3DGS, which is then densified via Gaussian Shuffle Split to form a structural scaffold. The LR views are upsampled and processed by our mapping network: a ViT encoder with feature refinement integrates LR 3DGS-aware cues, and a ViT decoder performs cross-view fusion. The Gaussian offset learning module then predicts residual offsets to the dense scaffold, yielding the final HR 3DGS for high-fidelity rendering*

**前馈 3DGS 骨干与稠密化骨架。** 首先，任意预训练的前馈 3DGS 重建模型（如 **NoPoSplat** (Ye et al., ICLR 2025) 或 **DepthSplat** (Xu et al., CVPR 2025)）从稀疏 LR 视图估计一个 LR 3DGS 作为初始表示。随后，通过高斯洗牌分裂操作对该 LR 3DGS 进行稠密化：对每个不透明度高于 0.5 的高斯核，沿其主轴方向生成 6 个子高斯，子高斯中心偏移量为：

$$\pmb{\mu}_{j,k} = \pmb{\mu}_{j} + \beta R_{j} \pmb{e}_{k} \odot \pmb{s}_{j}, \quad k = 1, \ldots, 6$$

聚合所有子高斯得到稠密结构骨架 $\mathcal G^{\mathrm{Dense}}$，为后续高频几何与纹理恢复提供空间支撑。

**映射网络。** 并行地，LR 输入视图被上采样至目标分辨率，进入映射网络。该网络采用基于 ViT 的编码器-解码器架构：
- **ViT 编码器**提取中层特征令牌 $\mathbf t_{\mathrm{en}}$；
- **特征细化模块**通过双向交叉注意力将编码器令牌与从 3DGS 骨干中提取的几何感知令牌 $\mathbf t_{\mathrm{pre}}$ 对齐，使 2D 特征融入 3D 几何先验；
- **ViT 解码器**执行视图内自注意力和视图间交叉注意力，融合跨视图特征以减少不一致性。

**高斯偏移学习模块。** 该模块是框架的核心创新。将 $\mathcal G^{\mathrm{Dense}}$ 中每个高斯的中心投影到图像平面，查询映射网络输出的局部特征，并与几何感知位置嵌入融合后送入 PointTransformerV3 进行空间推理：

$$\pmb{F} = \Phi_{\mathrm{PTv3}} \big( [\pmb{\mu}_i; \{\pmb{F}_i\}_{i=1}^N; \pmb{K}] \big)$$

随后轻量高斯头 MLP 预测各高斯参数的残差偏移：

$$\Delta G = (\Delta \mu, \Delta \alpha, \Delta r, \Delta s, \Delta c) = \Psi_{\mathrm{GH}}(\pmb{F})$$

最终，将残差偏移叠加到稠密骨架上得到 HR 3DGS：

$$\mathcal G^{\mathrm{HR}} = \mathcal G^{\mathrm{Dense}} + \Delta \mathcal G$$

**训练目标。** 预测的 HR 3DGS 通过可微高斯光栅化渲染为新视图图像，以像素级 MSE 损失与感知一致性 LPIPS 损失的组合进行监督，联合保持几何精度与视觉保真度。

这一设计的关键因果机制在于：学习偏移量而非直接回归绝对 HR 高斯参数，显著降低了需学习的高斯参数量（从 44.5M 降至 16.0M），使训练更稳定，并大幅提升高频纹理保真度。消融实验表明，高斯偏移学习是效果提升最大的单一模块。

### 补充图表

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/001_Figure_1.jpg]]
*Figure 1: We reformulate 3DGS-based 3DSR as a feed-forward mapping problem from sparse LR views to HR 3DGS representation. (a) Unlike existing methods that rely on dense multi-view inputs and per-scene 3DGS self-optimization, our method directly predicts HR 3DGS by a learned network from as few as two LR views. (b) This reformulation fundamentally changes how 3DSR acquires high-frequency knowledge. Instead of inheriting the limited priors embedded in 2DSR models, our SR3R learns a generalized crossscene mapping function from large-scale multi-scene data, enabling the network to autonomously acquire the 3D-specific high-frequency structures required for accurate HR 3DGS reconstruction. The bottom row...*

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/005_Figure.jpg]]

## 核心模块与公式推导

SR3R 将 3D 超分辨率重新定义为从前馈映射问题，其核心映射函数为：

$$f_{\pmb \theta} : \{ ( I_{lr}^v , K^v ) \}_{v=1}^V \mapsto \mathcal G^{\mathrm{HR}}$$

其中 $\{ ( I_{lr}^v , K^v ) \}_{v=1}^V$ 表示 $V$ 幅低分辨率输入视图及其对应的相机内参，$\mathcal G^{\mathrm{HR}}$ 为目标高分辨率 3DGS 表示。该映射通过以下关键模块级联实现。

### 前馈 3DGS 骨干与高斯洗牌分裂

框架首先利用任意预训练的前馈 3DGS 重建模型（如 **NoPoSplat** (Ye et al., ICLR 2025) 或 **DepthSplat** (Xu et al., CVPR 2025)）从稀疏 LR 视图估计一个低分辨率 3DGS 骨架。随后，通过高斯洗牌分裂操作对不透明度高于 0.5 的高斯点进行稠密化：每个高斯点 $j$ 沿其主轴方向生成 6 个子高斯，子高斯中心偏移定义为：

$$\pmb{\mu}_{j,k} = \pmb{\mu}_{j} + \beta R_{j} \pmb{e}_{k} \odot \pmb{s}_{j}, \quad k = 1, \ldots, 6$$

其中 $R_j$ 为旋转矩阵，$\pmb{s}_j$ 为尺度向量，$\beta$ 控制偏移幅度。所有子高斯聚合构成稠密结构骨架 $\mathcal{G}^{\mathrm{Dense}}$：

$$\mathcal{G}^{\mathrm{Dense}} = \bigcup_{j=1}^{M} \bigcup_{k=1}^{6} G_{j,k}^{\mathrm{Dense}}, \quad G_{j,k}^{\mathrm{Dense}} = (\pmb{\mu}_{j,k}, \alpha_{j}, \pmb{r}_{j}, s_{j,k}, \pmb{c}_{j})$$

该骨架为后续高频几何与纹理恢复提供了结构先验。

### 映射网络：ViT 编码器与特征细化

LR 输入视图经上采样至目标分辨率后，由 ViT 编码器提取中级特征令牌 $t_{\mathrm{en}}$。为将 2D 特征与 3D 几何先验对齐，引入特征细化模块，通过双向交叉注意力在编码器令牌与从预训练骨干提取的几何感知令牌 $t_{\mathrm{pre}}$ 之间建立关联：

$$\mathbf{U}_{op} = \mathrm{softmax}\left( \frac{ (t_{\mathrm{en}} W_Q^o) (t_{\mathrm{pre}} W_K^p)^\top }{ \sqrt{d} } \right) (t_{\mathrm{pre}} W_V^p)$$

细化后的特征随后进入 ViT 解码器，依次执行视图内自注意力和视图间交叉注意力以融合跨视图特征，减少多视图不一致性。

### 高斯偏移学习模块

这是 SR3R 效果提升最大的单一模块。其核心思想是学习稠密骨架 $\mathcal{G}^{\mathrm{Dense}}$ 到目标 $\mathcal{G}^{\mathrm{HR}}$ 的残差偏移，而非直接回归绝对 HR 高斯参数，从而显著提升训练稳定性和高频纹理保真度。

具体流程：对每个高斯点，将其三维中心 $\pmb{\mu}_i$ 通过相机投影映射到图像平面以获得二维坐标 $p_i$：

$$\tilde{p}_i = \mathbf{K} \mathbf{P} \tilde{\mu}_i, \quad u_i = \frac{\tilde{u}_i}{\tilde{w}_i}, \quad v_i = \frac{\tilde{v}_i}{\tilde{w}_i}$$

在 $p_i$ 处查询 ViT 特征得到局部特征 $\pmb{F}_i$，并与位置嵌入融合后送入 PointTransformerV3 进行空间推理编码：

$$\pmb{F} = \Phi_{\mathrm{PTv3}} \big( [\pmb{\mu}_i; \{\pmb{F}_i\}_{i=1}^N; \pmb{K}] \big)$$

编码特征 $\pmb{F}$ 通过轻量高斯头 MLP 预测各参数的残差偏移：

$$\Delta G = (\Delta \mu, \Delta \alpha, \Delta r, \Delta s, \Delta c) = \Psi_{\mathrm{GH}}(\pmb{F})$$

最终 HR 3DGS 由稠密骨架与残差偏移组合得到：

$$\mathcal{G}^{\mathrm{HR}} = \mathcal{G}^{\mathrm{Dense}} + \Delta \mathcal{G}, \quad \Delta \mathcal{G} = \{ \Delta G_i \}_{i=1}^N$$

### 训练目标

预测的 $\mathcal{G}^{\mathrm{HR}}$ 通过可微高斯光栅化渲染为新视角图像，采用像素级重建损失（MSE）与感知一致性损失（LPIPS）的联合监督，以同时保持几何精度和视觉保真度。

> **证据强度说明**：上述公式均来自原文明确给出的定义（Eq. 1–9），模块间的因果关系由消融实验（Table 3）支撑——高斯偏移学习使 PSNR 从 23.504 提升至 24.447，且将需学习的高斯参数量从 44.5M 降至 16.0M；加入 PTv3 后达到最优 24.794。

### 补充图表

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/009_Figure_S.1.jpg]]
*Figure S.1: Detailed Gaussian Offset Learning pipeline. Each Gaussian center is projected to the image plane to query local ViT features. The queried token is fused with a geometry-aware position embedding and processed by PTv3 blocks for spatial reasoning. A lightweight Gaussian Head predicts residual offsets to refine the initial 3DGS template*

## 实验与分析

### 核心范式转换的定量验证

SR3R的核心主张是将3D超分辨率（3DSR）从“逐场景优化+2DSR伪监督”重新定义为“从稀疏低分辨率视图到高分辨率3DGS的直接前馈映射”。这一范式转换在RE10K和ACID两个大规模数据集上得到了系统验证。在4倍超分辨率设定下（64×64 → 256×256），SR3R以DepthSplat为前馈骨干时，在RE10K上达到**PSNR 26.250**，较DepthSplat基线的23.147提升**+3.103 dB**；在ACID上达到**PSNR 27.018**，较基线23.801提升**+3.217 dB**（Table 1）。LPIPS指标同样显著改善（RE10K: 0.165 vs 基线0.257），表明SR3R不仅提升了像素精度，更实质性地增强了感知质量。

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of 4× 3DSR on the large-scale RE10K and ACID datasets. SR3R consistently and substantially outperforms all baselines and their upscaled-input versions across PSNR, SSIM, and LPIPS, with only moderate Gaussian complexity and training memory. Bold indicates the best results and underline the second best*

值得注意的是，SR3R的优势并非依赖于特定骨干网络。以NoPoSplat为骨干时，SR3R在RE10K上达到PSNR 24.794，同样大幅超越NoPoSplat基线的21.326（+3.468 dB）。这种跨骨干的一致性表明，SR3R的增益来源于其核心设计——前馈映射网络从多场景数据中自主习得3D高频结构——而非特定架构的偶然适配。

### 零样本泛化：从室内到室外的跨域迁移

SR3R的另一个关键优势在于其跨场景泛化能力。在RE10K→DTU的零样本设定下（Table 2），SR3R以NoPoSplat为骨干达到**PSNR 17.241**，较NoPoSplat基线的12.628提升**+4.613 dB**，甚至超越了需要逐场景优化的**SRGS**（Feng et al., arXiv 2024）和**FSGS+SRGS**（Zhu et al., ECCV 2024）组合方法。在RE10K→ScanNet++的零样本设定下（Table S1），SR3R达到PSNR 21.743，较NoPoSplat基线的18.284提升+3.459 dB。

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/007_Table_2.jpg]]
*Table 2: Zero-shot generalization results from RE10K to DTU. Feed-forward models are trained on RE10K and tested on DTU without fine-tuning. SRGS and FSGS+SRGS use per-scene optimization. SR3R delivers the best reconstruction quality while remaining significantly faster than optimization-based methods. Bold indicates the best results and underline the second best*

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/012_Table_S.1.jpg]]
*Table S.1: Zero-shot generalization results from RE10K to Scanet++. Feed-forward models are trained on RE10K and tested on Scanet++ without fine-tuning. SRGS and FSGS+SRGS use per-scene optimization. SR3R delivers the best reconstruction quality while remaining significantly faster than optimizationbased methods. Bold indicates the best results*

这一结果揭示了SR3R范式转换的深层机理：逐场景优化方法（如SRGS）虽然可以在单个场景上通过迭代优化获得较好结果，但其高频先验受限于预训练的2D超分模型，缺乏对3D几何结构的理解。SR3R通过从大规模多场景数据中学习广义映射函数，获得了可迁移的3D高频知识，在未见场景上展现出更强的泛化能力。定性结果（Figure S2, Figure S3）进一步证实，SR3R在零样本场景下恢复的纹理更清晰、几何更稳定，而优化方法常出现模糊和几何伪影。

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/010_Figure_S.2.jpg]]
*Figure S.2: Zero-shot qualitative comparison on the DTU dataset. Per-scene optimization and feed-forward baselines show blurring and geometric artifacts, while SR3R recovers significantly sharper textures and consistent geometry, highlighting its strong generalization to unseen scenes*

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/011_Figure_S.3.jpg]]
*Figure S.3: Zero-shot qualitative comparison on the ScanNet++ dataset. Per-scene optimization and feed-forward baselines show blurring and geometric artifacts, while SR3R recovers significantly sharper textures and consistent geometry, highlighting its strong generalization to unseen scenes*

### 模块消融：增益来源的因果解耦

Table 3通过累积添加各模块，清晰揭示了SR3R各组件的贡献权重：

1. **上采样模块**（+Upsampling）：将LR视图上采样至目标分辨率后送入ViT编码器，PSNR从基线的21.326提升至23.374（**+2.048 dB**）。这一增益主要来自为映射网络提供了更高分辨率的2D特征空间，减少了从极低分辨率直接推断高频细节的难度。

2. **特征细化交叉注意力**（+Cross Attention）：在ViT编码器特征与前馈骨干的几何感知令牌之间引入双向交叉注意力，PSNR进一步提升至23.504（+0.130 dB）。该模块的增益虽相对温和，但其作用在于对齐2D纹理特征与3D几何先验，为后续偏移学习提供更一致的特征表示。

3. **高斯偏移学习**（+G. Offset w/o PTv3）：这是效果提升最大的单一模块，PSNR跃升至24.447（**+0.943 dB**），同时将需要学习的高斯参数数量从44.5M降至16.0M。这一消融直接验证了论文的核心设计选择：学习从稠密骨架到HR高斯的残差偏移，而非直接回归绝对HR参数，既稳定了训练，又显著增强了高频纹理保真度。

4. **PointTransformerV3空间推理**（+PTv3, 完整SR3R）：在偏移学习中加入PTv3进行显式3D空间推理，PSNR达到24.794（+0.347 dB）。PTv3使模型能够利用高斯点之间的空间关系进行上下文感知的偏移预测，进一步锐化了局部几何细节。

定性消融（Figure 4）与定量结果一致：上采样减少粗粒度模糊，交叉注意力改善特征对齐，高斯偏移学习增强局部几何，PTv3产生最清晰、最一致的重建结果。

### 上采样策略的鲁棒性

Table 4展示了SR3R对不同上采样策略的鲁棒性。在使用Bilinear插值（24.586）、Bicubic插值（24.683）和SwinIR学习型上采样（24.794）三种策略下，SR3R的PSNR波动仅约0.2 dB。这一稳定性表明，SR3R的性能增益并非依赖于特定的上采样算法，而是源自其核心的偏移学习与特征细化机制。即使使用最简单的双线性插值，SR3R仍能通过映射网络有效恢复高频细节。

### 计算开销的公平性考量

SR3R在取得显著性能提升的同时，保持了合理的计算开销。以DepthSplat为骨干时，SR3R的高斯参数数量为11.3M，训练显存约17GB，与DepthSplat Upsampled（10.7M参数，12GB显存）相比增加可控。考虑到PSNR提升超过3 dB，这一开销在实际部署中是可以接受的。论文明确报告了所有方法的参数量和训练显存，确保了对比的公平性。

### 局限性与待验证场景

论文未设专门的局限性章节，但综合实验结果可识别以下边界：

- **骨干依赖性**：SR3R的性能受前馈骨干网络能力制约。在极端域外场景（如DTU的某些稀疏纹理区域），重建质量仍存在下降，这源于骨干网络本身在零样本条件下的预测误差被传播至偏移学习模块。
- **超分倍率限制**：当前实验仅验证了4倍超分（64×64 → 256×256）。更高倍率（如8×、16×）下，LR视图中的信息量急剧减少，前馈映射网络能否从极稀疏的输入中恢复可信的高频结构，尚待验证。
- **显存需求**：训练显存约17GB，可能限制在消费级GPU（如RTX 3080 10GB）上的直接训练。推理阶段的显存需求论文未明确报告，需要手动验证。

### 待解决问题

1. SR3R框架能否扩展到更高倍率（8×、16×）的超分辨率重建，同时保持训练稳定性和重建保真度？
2. 高斯偏移学习机制是否可以泛化到其他三维表示（如NeRF、3D Gaussian的变体）的超分辨率任务？
3. 在实际采集噪声、光照变化和有限视角重叠条件下，前馈映射网络的鲁棒性如何？
4. 是否可以与基于扩散模型的高频生成先验结合，在极低分辨率输入下进一步丰富纹理细节？

### 补充图表

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/006_Table_3.jpg]]
*Table 3: Component-wise ablation on RE10K (4× 3DSR). Modules are added cumulatively to the NoPoSplat baseline. Each component improves performance, and Gaussian Offset Learning yields the largest gain with fewer learnable Gaussians. The full SR3R achieves the best results*

![[assets/figures/papers/paper_list_l2602_https_arxiv_org_abs_2602_24020/figures/008_Table_4.jpg]]
*Table 4: Ablation on upsampling strategies on RE10K (4× 3DSR). SR3R maintains consistently strong performance across all interpolation and learning-based upsampling methods*

## 方法谱系与知识库定位

SR3R 将基于 3D Gaussian Splatting (3DGS) 的三维超分辨率（3DSR）重新定义为从稀疏低分辨率（LR）视图到高分辨率（HR）3DGS 的直接前馈映射问题。这一范式转换使其在方法谱系中处于一个独特位置：它既不同于依赖逐场景优化和 2DSR 伪监督的传统 3DSR 方法，也不同于仅做前馈重建而不具备超分能力的 3DGS 模型。

### 与前馈 3DGS 重建基线的关系

SR3R 并非从零构建 3DGS 重建能力，而是以一种即插即用的方式建立在现有前馈 3DGS 重建模型之上。论文明确使用两个 SOTA 前馈模型作为骨干网络和基线：

- **NoPoSplat** (Ye et al., ICLR 2025)：作为主要的即插即用骨干和基线。
- **DepthSplat** (Xu et al., CVPR 2025)：作为替代骨干和基线。

SR3R 的核心贡献不在于改进这些骨干的视图编码或深度估计能力，而在于在其上叠加了一个可学习的映射网络，使整个系统能够从 LR 输入直接产出 HR 3DGS。在 RE10K 和 ACID 的 4× 3DSR 设定下，SR3R 相较于原始 NoPoSplat 和 DepthSplat 均有大幅提升（PSNR 增益约 +3.1 dB），且显著优于这些骨干的“先上采样输入再重建”的朴素变体。这表明 SR3R 的增益并非来自简单的图像分辨率提升，而是来自网络自主习得的 3D 高频映射能力。

### 与逐场景优化 3DSR 基线的关系

在零样本泛化实验中，SR3R 与两类逐场景优化的 3DSR 方法进行了对比：

- **SRGS** (Feng et al., arXiv 2024)：逐场景优化的 3DSR 方法，用于零样本比较。
- **FSGS+SRGS** (Zhu et al., ECCV 2024；与 SRGS 结合)：稀疏视图下的逐场景优化基线。

在从 RE10K 到 DTU 的零样本设定下，SR3R（基于 NoPoSplat 骨干）的 PSNR 达到 17.241，显著高于 SRGS 和 FSGS+SRGS，同时推理速度远快于后者——后者需要在新场景上进行迭代优化。这验证了 SR3R 的核心主张：从大规模多场景数据中学到的广义映射函数，能够替代逐场景优化所依赖的 2DSR 伪监督和场景级微调，实现即插即用的高保真超分。

### 方法适用边界与局限

尽管 SR3R 在多个基准上取得了显著提升，但其适用边界和局限性值得关注：

1. **骨干网络依赖性**：SR3R 的性能受限于前馈 3DGS 骨干的重建能力。在极端域外场景（如与训练数据差异极大的几何结构或外观）下，LR 3DGS 骨架本身质量不足时，偏移学习模块难以完全弥补底层重建误差。零样本实验中 DTU 的绝对 PSNR（17.241）仍远低于域内结果，说明跨域泛化仍存在明显性能下降。

2. **计算资源需求**：训练 SR3R 需要约 17 GB 显存，这可能限制其在资源受限设备上的直接应用。虽然推理阶段为前馈模式，但显存占用仍需进一步优化。

3. **超分倍率限制**：当前工作仅验证了 4× 超分（64×64 → 256×256）。更高倍率（如 8×、16×）下，LR 视图中的信息量急剧减少，高斯洗牌分裂产生的稠密骨架是否仍能提供足够的结构先验，以及偏移学习模块的预测误差是否会累积放大，均未经验证。

4. **输入视图数量**：论文主要展示了两视图输入的设定。在更稀疏（单视图）或更密集（多视图）输入下，框架的性能和训练稳定性尚未系统探索。

### 开放问题

SR3R 的提出为 3DSR 领域打开了若干值得深入的方向：

- **更高倍率扩展**：能否将 SR3R 框架扩展到 8× 或 16× 超分，同时保持训练稳定和重建保真度？这可能需要重新设计骨架稠密化策略或引入级联式偏移预测。
- **与生成先验的结合**：当前 SR3R 完全依赖前馈映射学习高频细节，是否可以与基于扩散模型的高频生成先验结合，以进一步丰富纹理细节，尤其是在信息严重缺失的区域？
- **鲁棒性验证**：在实际采集条件下的噪声、光照变化和有限视角重叠等退化因素下，SR3R 的鲁棒性如何？当前实验均在相对干净的合成或受控数据上进行。
- **表示泛化性**：高斯偏移学习的思想——即从粗粒度表示学习残差偏移而非直接回归目标参数——是否可以泛化到其他三维表示（如 NeRF、3D Gaussian 的其他变体）的超分辨任务中？

## 原文 PDF

![[paperPDFs/CVPR_2026/SR3R_Rethinking_Super_Resolution_3D_Reconstruction_With_Feed_Forward_Gaussian_Splatting.pdf]]