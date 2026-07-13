---
title: "Uni3R: Unified 3D Reconstruction and Semantic Understanding via Generalizable Gaussian Splatting from Unposed Multi-View Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Uni3R_Unified_3D_Reconstruction_and_Semantic_Understanding_via_Generalizable_Gaussian_Splatting_from_Unposed_Multi_View_Images.pdf
project_link: "https://horizonrobotics.github.io/robot_lab/uni3R/"
code_link: null
aliases:
- Uni3R
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入跨视图 Transformer（Cross-View Transformer）将任意多视图信息融合为全局一致的潜在表示，并从中解码出统一的 3D 高斯原语，该原语同时携带外观、几何和开放词汇语义特征，从而在一个前馈推理中实现多种任务。
primary_logic: 利用预训练的几何基础模型（VGGT）并扩展为跨视图 Transformer，既能注入强大的几何先验，又能融合多视图信息，使得无需每场景优化即可统一 3D 重建与开放词汇语义理解。
claims:
- Uni3R 在单次前馈推理中超越场景优化方法及先前的前馈方法，在新视角合成、深度估计和开放词汇语义分割上达到最先进水平
- 几何引导损失与跨视图 Transformer 对训练稳定性和性能至关重要；消融实验显示移除几何损失将导致 4 视图模型崩溃
- 在 RE10k 和 ScanNet 上大幅超越基线方法，并零样本泛化到 Mip-NeRF360
- ScanNet 上 PSNR (target view) = 25.53
---

# Uni3R: Unified 3D Reconstruction and Semantic Understanding via Generalizable Gaussian Splatting from Unposed Multi-View Images

> [!tip] 核心洞察
> 利用预训练的几何基础模型（VGGT）并扩展为跨视图 Transformer，既能注入强大的几何先验，又能融合多视图信息，使得无需每场景优化即可统一 3D 重建与开放词汇语义理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | Uni3R：从无姿态多视图图像实现统一3D重建与语义理解的通用高斯溅射方法 |
| 英文题名 | Uni3R: Unified 3D Reconstruction and Semantic Understanding via Generalizable Gaussian Splatting from Unposed Multi-View Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2508.03643) · [Project](https://horizonrobotics.github.io/robot_lab/uni3R/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Uni3R |
| Dataset | ScanNet, RE10K |

> [!tip] 效果简介
> - ScanNet 上，PSNR (target view) 25.53 vs 24.89 (PixelSplat) (+0.64)；SSIM 0.8727 vs 0.8392 (PixelSplat) (+0.0335)；LPIPS 0.1380 vs 0.1641 (PixelSplat) (-0.0261)。
> - RE10K (2-view) 上，PSNR 25.074 vs 23.430 (MVSplat) (+1.644)。
> - RE10K (4-view) 上，PSNR 26.360 vs 24.537 (VicaSplat) (+1.823)。

## 概要

现有3D场景理解方法通常将**几何重建**与**语义理解**视为两个独立任务，或依赖逐场景的迭代优化（如NeRF/3DGS类方法），严重制约了泛化能力与推理效率。基于两视图的前馈方法虽无需优化，却缺乏对任意多视图输入的全局一致性建模。这构成了一个根本性瓶颈：如何在一次前馈推理中，从**无姿态的多视图图像**直接获得同时包含外观、几何与开放词汇语义的统一场景表示？

Uni3R 针对上述瓶颈提出的核心机制是**跨视图Transformer（Cross-View Transformer）**。该方法将来自任意数量、无姿态的输入视图信息融合为全局一致的潜在表示，并从中解码出一组统一的3D高斯原语。每个高斯原语不仅携带传统的外观与几何属性，还内嵌了**开放词汇语义特征**，使得单一前馈模型即可支撑新视角合成、深度估计和零样本语义分割等多种下游任务。

其关键洞察在于：利用预训练的几何基础模型 VGGT 作为编码器骨架，并将其扩展为跨视图Transformer，既能注入强大的几何先验，又能实现多视图信息的深度融合，从而在无需任何3D标注（仅需2D特征蒸馏）的条件下，统一3D重建与开放词汇语义理解。

实验证据表明，Uni3R 在 RE10K 和 ScanNet 数据集上以单次前馈推理超越了先前的前馈方法及部分场景优化方法：在4视图与8视图设置下，PSNR 较 VicaSplat 平均提升约 2.0 dB；在 ScanNet 目标视图上的语义分割 mIoU 达到 0.5584，显著优于需3D标注的 LSM。消融实验进一步揭示了两个决定性因素：**几何引导损失**对于多视图训练稳定性至关重要——移除该损失将导致4视图模型崩溃；**语义蒸馏损失**的移除则使 mIoU 从 0.5484 骤降至 0.0183，证明了语义监督的不可或缺性。

在方法谱系中，Uni3R 相较于 PixelSplat、MVSplat 等需已知位姿的泛化3DGS方法，解除了位姿先验依赖；相较于 NoPoSplat 等无位姿图像对方法，突破了视图数量的限制；相较于 LSM 等统一辐射场与语义场的方法，摆脱了对3D标注的需求。其“任意多视图→统一高斯原语”的范式，为通用3D场景理解提供了一种高效且可泛化的前馈方案。

3D 场景理解与重建是计算机视觉的核心挑战，涉及从多视图图像中恢复场景的几何结构、外观属性与语义信息。近年来，3D 高斯溅射（3D Gaussian Splatting, 3DGS）凭借其高质量实时渲染能力，成为神经辐射场（NeRF）之外的主流场景表示方案。然而，现有方法在统一性与泛化性上存在显著瓶颈。

**现有方法的三大缺口。** 第一，**语义与几何分离**。当前 3DGS 方法大多仅关注新视角合成，将语义理解作为独立后处理步骤，缺乏端到端的统一建模。少数尝试融合语义的工作（如 **LSM** 将辐射场与语义场联合重建）依赖两视图输入，缺乏全局一致性，且需要 3D 语义标注进行训练。第二，**位姿依赖与场景优化**。主流泛化 3DGS 方法（如 **PixelSplat**、**MVSplat**）要求已知精确的相机位姿，限制了在无标定场景中的应用；而 **Feature-3DGS**、**NeRF-DFF** 等语义方法则依赖逐场景优化，推理效率低下。第三，**多视图融合受限**。基于图像对的方法（如 **NoPoSplat**）通过 pairwise 特征匹配处理无位姿输入，但无法有效利用任意多视图信息，导致全局几何一致性不足。

**Uni3R 的核心动机**在于打破上述壁垒：能否在一个前馈模型中，从无姿态的任意多视图图像出发，同时输出几何、外观与开放词汇语义的统一 3D 表示？这需要解决两个关键问题——如何将多视图信息融合为全局一致的潜在表示，以及如何让 3D 原语同时携带多模态属性。

为此，Uni3R 引入**跨视图 Transformer（Cross-View Transformer）**作为核心因果机制。该模块以预训练的几何基础模型 **VGGT** 为初始化，交替进行帧内自注意力与跨帧全局注意力，将任意数量的视图信息融合为视角无关的潜在编码。这一设计既注入了强大的几何先验，又实现了灵活的多视图聚合。在此基础上，Uni3R 通过 Dense Prediction Transformer（DPT）解码器与专用预测头，直接输出一组 3D 高斯原语，每个原语参数化为中心点 $\mu_j$、不透明度 $\alpha_j$、颜色 $c_j$、尺度 $s_j$、旋转 $r_j$ 和语义特征 $f_j^{\mathrm{sem}}$（公式 1），从而在单次前馈推理中统一支持新视角合成、深度估计与开放词汇语义分割。

## 核心方法与创新机理

Uni3R 的核心创新在于**首次将 3D 几何重建、新视角合成和开放词汇语义理解统一到单一前馈框架中**，且无需已知相机位姿或任何 3D 语义标注。这一突破通过以下关键设计实现。

### 1. 从两视图到任意多视图的泛化

现有前馈 3DGS 方法（如 **PixelSplat**、**MVSplat**、**NoPoSplat**）大多限定为两视图输入，依赖 pairwise 特征匹配，缺乏全局一致性。Uni3R 将输入扩展为**任意数量的无姿态多视图图像**（2 至 16+ 视角），通过跨视图 Transformer 一次性融合所有视角信息，产生全局一致的场景表征。这一设计使得模型能够利用更多观测来提升重建质量——实验表明，随着输入视角从 2 增至 8，PSNR 从 25.07 dB 提升至 28.32 dB（RE10k），充分验证了多视图融合的收益（Table 4）。

### 2. 统一几何、外观与语义的 3D 高斯原语

此前的泛化方法仅输出几何与外观（RGB/深度），语义理解需依赖独立的场景优化流程（如 **Feature-3DGS**、**NeRF-DFF**）或需要 3D 标注的模型（如 **LSM**）。Uni3R 将开放词汇语义特征直接嵌入 3D 高斯原语的参数化中：

$$G _ { j } = \\{ \\mu _ { j } , \\alpha _ { j } , c _ { j } , s _ { j } , r _ { j } , f _ { j } ^ { \\mathrm { s e m } } \\}$$

每个高斯原语同时携带中心点、不透明度、颜色、尺度、旋转四元数和语义特征向量。通过 alpha 混合渲染语义特征图后，利用 CLIP 文本原型计算余弦相似度即可实现零样本开放词汇分割，无需任何 3D 语义标注（Table 1 注释明确指出 Uni3R 训练不使用 3D 标注，而 LSM 需要）。

### 3. 几何引导的多视图训练稳定性

前馈方法通常仅依赖 RGB 渲染损失，缺乏对底层几何结构的约束，在多视图训练时容易崩溃。Uni3R 引入**点图引导的几何损失**——利用冻结的 VGGT 基础模型生成稠密点图作为软几何先验，通过带置信度掩码的单向 Chamfer 距离约束高斯中心的位置：

$$\\mathcal { L } _ { \\mathrm { g e o } } = \\sum _ { i = 1 } ^ { N } \\frac { 1 } { N _ { p t s } ^ { ( i ) } } \\sum _ { x \\in X _ { U } ^ { ( i ) } } \\operatorname* { m i n } _ { x ^ { \\prime } \\in X _ { V } ^ { ( i ) } } | | x - x ^ { \\prime } | | _ { 2 } ^ { 2 }$$

消融实验表明，移除几何损失会使 4 视图模型直接训练崩溃（Figure 5），深度相对误差从 3.9 增至 47.99（Table 9），证明了该约束对训练稳定性和几何准确性的关键作用。

### 4. 跨视图 Transformer 实现全局一致融合

区别于 pairwise 匹配或简单时序处理，Uni3R 采用**跨视图 Transformer 编码器**，交替进行帧内自注意力和跨帧全局注意力，将 VGGT 的几何先验与多视图外观信息融合为视角无关的潜在表征。这一设计使得后续的 DPT 解码器能够从全局一致的表示中预测统一的 3D 高斯原语，消除了逐场景优化的需求。

### 关键消融证据

Table 7 的消融实验揭示了各模块的因果作用：
- **移除语义损失**：mIoU 从 0.5484 骤降至 0.0183，证明语义蒸馏不可或缺；
- **移除渲染损失**：所有指标失效（mIoU 降至 0.2653），说明 RGB 监督对学习外观至关重要；
- **置信度掩码最优比例 90%**：在该设置下 mIoU、深度准确率和渲染质量均达到最佳（Table 9）。

这些消融共同验证了 Uni3R 的“统一监督”设计——语义、辐射场和几何场的联合学习是实现高保真、语义一致 3D 重建的核心机制。

Uni3R 的整体流水线围绕一个核心设计展开：**从无姿态的任意多视图图像中，通过单次前馈推理，直接预测一组统一的 3D 高斯原语**，这些原语同时携带几何、外观与开放词汇语义信息。流水线由四个关键模块串联构成，形成“编码—融合—解码—预测”的端到端架构（见图 2）。

**输入编码与内参注入。** 每个输入视图首先与一个内参嵌入（Intrinsic Embedding）拼接。具体而言，相机的焦距与主点坐标经线性投影编码为几何线索，逐通道拼接到对应图像上，再进行 patch 切分。随后，预训练的 DINOv2 ViT 编码器对每个增强后的视图独立提取 patch 级特征 token 序列。这一步将原始像素转化为富含语义与几何先验的潜在表示，为跨视图融合提供高质量的基础特征。

**跨视图 Transformer 编码器。** 这是流水线的核心瓶颈模块。它继承自预训练的几何基础模型 VGGT，并由 $L=24$ 层 Transformer 块组成，每层交替执行帧内自注意力和跨帧全局注意力。帧内注意力负责精炼单视图内的局部细节，跨帧注意力则将任意数量的视图信息融合为全局一致的、视点无关的潜在表示。正是这种交替注意力机制，使得 Uni3R 能够处理 2 至 16+ 的任意多视图输入，而无需限定固定的视图数量或顺序。

**稠密预测 Transformer 解码器。** 融合后的潜在表示被送入一个稠密预测 Transformer（DPT）解码器，将其精炼为稠密的逐像素特征图。DPT 解码器同样以 VGGT 的预训练权重初始化，继承了强大的几何解码能力。

**高斯参数预测头。** 解码后的特征图通过多个独立的 MLP 预测头，为每个像素对应的 3D 高斯原语预测其全部属性：

$$
G_{j} = \{ \mu_{j}, \alpha_{j}, c_{j}, s_{j}, r_{j}, f_{j}^{\mathrm{sem}} \}
$$

其中 $\mu_{j}$ 为中心点坐标，$\alpha_{j} = \sigma(f_{j}^{\alpha})$ 为经 sigmoid 约束的不透明度，$c_{j}$ 为颜色，$s_{j} = \exp(f_{j}^{s}) \cdot d_{\mathrm{median}}$ 为经指数激活并与预测深度中位数相乘归一化的尺度，$r_{j} = \mathtt{normalize}(f_{j}^{r})$ 为单位四元数旋转，$f_{j}^{\mathrm{sem}}$ 为高维语义特征向量。

**语义特征的压缩与渲染。** 为降低高维语义特征在渲染时的显存开销，Uni3R 引入了一个语义自编码器：$\hat{f}_{j}^{\mathrm{sem}} = \mathcal{F}_{\mathrm{enc}}(f_{j}^{\mathrm{sem}})$ 将高维特征压缩为低维特征；渲染时通过 alpha 混合在像素级累积低维特征 $\hat{F} = \sum_{i} \hat{f}_{i}^{\mathrm{sem}} \alpha_{i} \prod_{j=1}^{i-1}(1-\alpha_{j})$，再由解码器解压 $\hat{F}' = \mathcal{F}_{\mathrm{dec}}(\hat{F})$ 恢复为高维语义特征。最终，通过文本原型与渲染特征的余弦相似度计算开放词汇分割 logits：$S_{p} = \operatorname{softmax}(f^{\mathrm{txt}} \cdot \hat{F}')$。

**训练监督。** 整个流水线由三项损失联合监督——光度损失（L1 + LPIPS）、语义蒸馏损失（以 LSeg 的 2D CLIP 特征为目标的余弦相似度）以及几何损失（以冻结 VGGT 生成的稠密点图为软先验的单向 Chamfer 距离），总损失为：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{sem}}\mathcal{L}_{\mathrm{sem}} + \lambda_{\mathrm{geo}}\mathcal{L}_{\mathrm{geo}}
$$

其中 $\lambda_{\mathrm{sem}}=0.02$，$\lambda_{\mathrm{geo}}=0.005$。这一统一监督范式使得 Uni3R 无需任何 3D 语义标注即可同时学习几何重建、外观渲染与开放词汇语义理解。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/002_Figure_2.jpg]]
*Figure 2: Architectural overview of the Uni3R pipeline. Uni3R predicts a set of Gaussian primitives with jointly integrated geometry, appearance, and open-vocabulary semantics in a single pass, eliminating the need for per-scene optimization*

Uni3R 的核心设计在于将多视图信息融合为全局一致的潜在表示，并从中解码出统一承载几何、外观与开放词汇语义的 3D 高斯原语。其流水线由五个关键模块串联构成，每个模块均承载明确的因果功能。

### 内参嵌入（Intrinsic Embedding）

为弥补无姿态输入缺失的几何线索，Uni3R 将每张图像的焦距与主点经线性投影编码为内参嵌入向量，并在 patch 切分前与对应图像通道级拼接。这一设计使后续的跨视图 Transformer 能够隐式感知各视图的成像几何，从而在不显式求解相机外参的条件下实现多视图对齐。

### DINOv2 图像编码器

拼接内参嵌入后的每个视图首先通过冻结的 DINOv2 ViT 提取 patch 级特征 token 序列。选用 DINOv2 的动机在于其预训练特征具备强语义判别力与跨视图一致性，为后续的语义蒸馏和几何融合提供高质量的初始表示。

### Cross-View Transformer 编码器

这是 Uni3R 实现全局一致性的核心机制。编码器由 L=24 层 Transformer 块堆叠而成，每层交替执行**帧内自注意力**（intra-frame self-attention）与**跨帧全局注意力**（cross-frame attention）。帧内注意力在单视图内建模局部上下文，跨帧注意力则使所有视图的 token 相互交互，将分散的多视图信息融合为视角无关的潜在表征。该结构继承自 VGGT 的几何先验，并通过权重初始化注入预训练的几何知识。

### Dense Prediction Transformer（DPT）解码器

融合后的潜在表征送入 DPT 解码器，将其精炼为与像素对齐的稠密特征图。DPT 的多尺度重组能力确保解码特征同时保留全局结构一致性与局部细节，为后续高斯参数预测提供高质量的逐像素表示。

### 高斯参数预测头

解码后的逐像素特征通过独立的 MLP 头预测每个 3D 高斯原语的全部属性。每个原语 $G_j$ 的完整参数化如公式 (1) 所示：

$$G _ { j } = \{ \mu _ { j } , \alpha _ { j } , c _ { j } , s _ { j } , r _ { j } , f _ { j } ^ { \mathrm { s e m } } \}$$

其中 $\mu_j$ 为中心点坐标，$\alpha_j$ 为不透明度，$c_j$ 为颜色，$s_j$ 为尺度，$r_j$ 为旋转四元数，$f_j^{\mathrm{sem}}$ 为语义特征向量。各参数的激活函数设计如下：

- **不透明度激活**：$\alpha _ { j } = \sigma ( f _ { j } ^ { \alpha } )$，通过 sigmoid 将值约束至 $[0,1]$。
- **尺度激活**：$s _ { j } = \exp ( f _ { j } ^ { s } ) \cdot d _ { \mathrm { m e d i a n } }$，指数激活后与预测深度的中位数相乘，实现尺度归一化，避免不同场景深度范围差异导致的训练不稳定。
- **旋转归一化**：$r _ { j } = \mathtt { n o r m a l i z e } ( f _ { j } ^ { r } )$，将预测的四元数归一化为单位长度，保证旋转表示的合法性。

### 语义自编码器

语义特征 $f_j^{\mathrm{sem}}$ 的维度较高，直接渲染将导致显著的内存开销。Uni3R 引入一个轻量自编码器，在渲染前将高维语义特征压缩为低维特征 $\hat{f}_j^{\mathrm{sem}}$：

$$\hat { f } _ { j } ^ { \mathrm { s e m } } = \mathcal { F } _ { \mathrm { e n c } } ( f _ { j } ^ { \mathrm { s e m } } )$$

渲染时，对排序后的高斯按公式 (6) 执行 alpha 混合，得到每个像素的压缩语义特征 $\hat{F}$：

$$\hat { F } = \sum _ { i } \hat { f } _ { i } ^ { \mathrm { s e m } } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

渲染完成后，解码器将压缩特征恢复为高维语义特征：

$${ \hat { F } } ^ { \prime } = { \mathcal { F } } _ { \mathrm { d e c } } ( { \hat { F } } )$$

最终，通过文本原型 $f^{\mathrm{txt}}$ 与恢复特征的余弦相似度计算语义 logits：

$$S _ { p } = \operatorname { s o f t m a x } ( f ^ { \operatorname { t x t } } \cdot { \hat { F } } ^ { \prime } )$$

这一压缩-渲染-解压流水线在保持语义精度的同时，大幅降低了高维特征渲染的显存占用。

### 训练目标

Uni3R 的总损失由三个互补的监督信号加权求和构成：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { r g b } } + \lambda _ { \mathrm { s e m } } \mathcal { L } _ { \mathrm { s e m } } + \lambda _ { \mathrm { g e o } } \mathcal { L } _ { \mathrm { g e o } }$$

其中 $\lambda_{\mathrm{sem}}=0.02$，$\lambda_{\mathrm{geo}}=0.005$。

**光度损失** $\mathcal{L}_{\mathrm{rgb}}$ 组合了 L1 损失与 LPIPS 感知损失（$\lambda_{\mathrm{LPIPS}}=0.05$）：

$$\mathcal { L } _ { \mathrm { r g b } } = \sum _ { i = 1 } ^ { N } \left( | | \widetilde { I } ^ { ( i ) } - \hat { I } ^ { ( i ) } | | _ { 1 } + \lambda _ { \mathrm { L P I P S } } \mathrm { L P I P S } ( \widetilde { I } ^ { ( i ) } , \hat { I } ^ { ( i ) } ) \right)$$

**语义损失** $\mathcal{L}_{\mathrm{sem}}$ 以 LSeg 提取的 2D CLIP 特征为监督，最小化渲染特征与目标特征之间的余弦距离：

$$\mathcal { L } _ { \mathrm { s e m } } = \sum _ { i = 1 } ^ { N } \left( 1 - \frac { \tilde { F } ^ { ( i ) } \cdot \hat { F } ^ { ( i ) ^ { \prime } } } { | | \tilde { F } ^ { ( i ) } | | \cdot | | \hat { F } ^ { ( i ) ^ { \prime } } | | } \right)$$

**几何损失** $\mathcal{L}_{\mathrm{geo}}$ 以冻结的 VGGT 生成的稠密点云为软几何先验，计算带置信度掩码的单向 Chamfer 距离：

$$\mathcal { L } _ { \mathrm { g e o } } = \sum _ { i = 1 } ^ { N } \frac { 1 } { N _ { p t s } ^ { ( i ) } } \sum _ { x \in X _ { U } ^ { ( i ) } } \operatorname* { m i n } _ { x ^ { \prime } \in X _ { V } ^ { ( i ) } } | | x - x ^ { \prime } | | _ { 2 } ^ { 2 }$$

置信度掩码选取 VGGT 预测置信度最高的前 90% 点参与损失计算，这一比例经消融实验验证为最优——移除几何损失将导致 4 视图模型训练崩溃，而 90% 的掩码比例在 mIoU、深度准确率和渲染质量上均取得最佳平衡。

## 实验与关键发现

### 主实验结果

Uni3R 在 ScanNet 数据集上全面验证了新视角合成、深度估计和开放词汇语义分割三项任务的统一性能。如 Table 1 所示，在目标视角合成上，Uni3R 以 PSNR 25.53 dB、SSIM 0.8727、LPIPS 0.1380 的成绩超越了所有前馈基线，包括依赖已知位姿的 **PixelSplat**（PSNR 24.89）和 **MVSplat**。在语义分割任务上，Uni3R 在源视角和目标视角的 mIoU 分别达到 0.5403 和 0.5584，显著优于需要 3D 标注训练的 **LSM**（分别为 0.5034 和 0.5078）。值得注意的是，Uni3R 完全无需 3D 语义标注即可实现这一性能，而 LSM 则依赖标注数据。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison on ScanNet. We evaluate performance on novel view synthesis, depth estimation, and open-vocabulary semantic segmentation. (*) Unlike LSM, Uni3R is trained without any 3D annotations*

在 RealEstate10k 数据集上，Uni3R 在不同视角数设置下均展现出显著优势。2 视角设置下（Table 3），Uni3R 以 PSNR 25.074 dB 超越依赖位姿的 **MVSplat**（23.430 dB）达 1.644 dB，同时略优于无需位姿的 **NoPoSplat**（25.038 dB）。在 4 视角和 8 视角设置下（Table 4），Uni3R 相比 **VicaSplat** 平均提升约 2.0 dB：4 视角 RE10k 上 PSNR 26.360 vs 24.537，8 视角 RE10k 上 PSNR 28.324 vs 26.807。这一趋势在 ScanNet 上同样成立，4 视角和 8 视角的 PSNR 分别达到 26.629 和 26.019，验证了跨视图 Transformer 在多视图融合中的有效性。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/008_Table_4.jpg]]
*Table 4: Comparison with 4 and 8-view settings on the RE10k [46] and ScanNet [6] datasets*

### 与场景优化方法的对比

Uni3R 作为前馈方法，在推理效率上具有压倒性优势。如 Table 2 所示，Uni3R 单场景平均重建时间仅为秒级，而场景优化方法如 **Feature-3DGS** 和 **NeRF-DFF** 需要数分钟至数十分钟的逐场景迭代。在精度方面，Uni3R 甚至超越部分场景优化方法：在 ScanNet 深度估计上，Uni3R 的相对误差（rel）达到 3.87，优于多数优化基线（Table 10）。这归功于冻结的 VGGT 提供的强几何先验和点图引导的几何损失。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/005_Table_2.jpg]]
*Table 2: Comparison with Per-Scene Optimized Methods. Time corresponds to the average reconstruction time per scene*

### 零样本泛化与跨域鲁棒性

Uni3R 展现出优异的泛化能力。在 Mip-NeRF360 数据集上的零样本测试中（Table 5），仅使用 RE10k 训练的模型在 8 视角设置下达到 PSNR 19.196 dB，验证了其对室外复杂场景的适应能力。跨域评估（Table 8）进一步表明，在 DTU 和 ScanNet++ 数据集上，Uni3R 的零样本性能显著优于 **NoPoSplat** 和 **VicaSplat**，说明内参嵌入与跨视图 Transformer 的设计有效缓解了域间差异。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/013_Table_8.jpg]]
*Table 8: Out-of-distribution performance comparison. Our method shows superior performance when zero-shot evaluation on DTU and ScanNet++ using the model solely trained on RE10k*

### 任意视角数训练

Table 6 展示了 Uni3R 在 ScanNet 上以 2–16 个随机视角数混合训练的结果。模型在 2 视角到 16 视角的评估中均保持稳定的渲染质量（PSNR 24.35–25.53）和语义分割精度（mIoU 0.5403–0.5584），证明跨视图 Transformer 能够灵活处理任意数量的输入，无需为不同视角数训练独立模型。

### 消融实验

消融实验揭示了三个关键设计的作用。

**语义损失**：移除语义损失后（Table 7），mIoU 从 0.5484 骤降至 0.0183，语义能力完全丧失。这表明 2D CLIP 特征蒸馏是赋予 3D 高斯原语开放词汇语义理解的唯一有效途径，仅靠 RGB 监督无法隐式学习语义表征。

**几何损失**：移除几何损失（w/o geo loss）导致深度相对误差从 3.9 升至 5.8，且在 4 视角训练中直接引发模型崩溃（Figure 5）。置信度掩码比例消融（Table 9）显示，top-90% 的置信度掩码在 mIoU（54.03）、深度误差（rel 3.87）和渲染质量（PSNR 24.35）上取得最优平衡，过高或过低的比例均会损害性能。

**渲染损失**：仅保留语义和几何损失而移除渲染损失（w/o rendering loss）时，所有指标均失效（Table 7），mIoU 降至 0.2653。这说明 RGB 监督是学习外观、几何和语义三者统一表征的基础，缺少它将破坏整个联合训练框架。

### 关键图表结论

- **Figure 3**：在 RealEstate10k 的 8 视角新视角合成中，Uni3R 生成的图像在细节保真度和结构一致性上明显优于 VicaSplat 和 NoPoSplat，尤其在高频纹理区域（如家具边缘和地毯图案）表现突出。
- **Figure 4**：ScanNet 上的新视角语义分割定性对比显示，Uni3R 能够在目标视角准确分割物体边界，对“椅子”“桌子”等类别保持语义一致性，而 LSM 在视角变化时出现明显的语义漂移。
- **Figure 5**：4 视角训练曲线直观展示了移除几何损失后的模型崩溃现象——训练损失在初期正常下降后突然发散，验证了 Chamfer 距离约束对训练稳定性的关键作用。

![[assets/figures/papers/paper_list_l2613_https_arxiv_org_abs_2508_03643/figures/010_Table_7.jpg]]
*Table 7: Ablation Study on different modules. We evaluate the ablated variants of Uni3R, by recording their rendering quality, segmentation performance and geometric accuracy*

## 定位与知识库关联

### 1. 与基线方法的关系

Uni3R 处于**泛化式（feed-forward）3D 场景重建**与**开放词汇语义理解**的交叉点，其核心突破在于将二者统一到单次前馈推理中，并摆脱了对已知相机位姿的依赖。以下从三个维度梳理其与基线工作的关系。

#### 1.1 泛化式 3D 高斯溅射（3DGS）方法

泛化式 3DGS 旨在通过前馈网络直接从输入图像预测 3D 高斯原语，避免每场景迭代优化。该方向的主要基线包括：

- **需已知位姿的方法**：**PixelSplat** 和 **MVSplat** 是典型的泛化 3DGS 方法，但它们依赖精确的相机外参与内参。Uni3R 在 ScanNet 2 视图设定下以 PSNR 25.53 dB 超越 PixelSplat 的 24.89 dB（+0.64 dB），在 RE10K 2 视图设定下以 25.074 dB 超越 MVSplat 的 23.430 dB（+1.644 dB），表明即使在位姿已知的设定下，Uni3R 的跨视图融合机制仍具有显著优势。

- **无需位姿的方法**：**NoPoSplat** 是首个无需位姿的 pairwise 前馈 3DGS 方法，但仅限于两视图输入。Uni3R 在 RE10K 2 视图设定下以 25.074 dB 略超 NoPoSplat 的 25.038 dB（+0.036 dB），差异较小，但在多视图设定下 Uni3R 的优势急剧扩大——NoPoSplat 无法原生处理 4 视图以上的输入，而 Uni3R 的跨视图 Transformer 可自然融合任意多视图信息。

- **基于 Transformer 的多视图方法**：**VicaSplat** 采用 Transformer 架构处理多视图输入，但仍需已知位姿。在 4 视图和 8 视图设定下，Uni3R 平均超越 VicaSplat 约 2.0 dB，核心差异在于 Uni3R 的跨视图 Transformer 编码器交替进行帧内与跨帧注意力，产生全局一致的表征，而 VicaSplat 缺乏这种显式的跨视图融合设计。

#### 1.2 统一辐射场与语义场的方法

将语义理解嵌入 3D 表示是该方向的另一条主线：

- **场景优化方法**：**Feature-3DGS** 和 **NeRF-DFF** 分别通过场景特定的 3DGS 优化和 NeRF 蒸馏将语义特征嵌入场景表示。这类方法需要每场景数分钟甚至数小时的优化（Table 2 显示 Uni3R 单次前馈仅需数十毫秒），且泛化能力有限。Uni3R 在无需任何 3D 语义标注的情况下（仅使用 2D 特征蒸馏），在 ScanNet 目标视角语义分割 mIoU 上达到 0.5584，超越需要 3D 标注的 LSM（0.5078），同时保持与场景优化方法可比的渲染质量。

- **前馈语义辐射场**：**LSM** 是首个统一辐射场与语义场的前馈方法，但仅限于两视图输入且需要 3D 语义标注。Uni3R 在 ScanNet 源视角和目标视角的 mIoU 上分别以 0.5403 和 0.5584 超越 LSM 的 0.5034 和 0.5078，且训练完全不需要 3D 标注，仅依赖 LSeg 的 2D CLIP 特征蒸馏。这一公平性优势（Table 1 注释明确标注）表明 Uni3R 的跨视图融合与统一高斯原语设计在语义理解上具有更强的数据效率。

#### 1.3 几何先验的注入方式

Uni3R 的另一个关键创新在于几何监督策略：

- **传统方法**：大多数泛化 3DGS 方法仅依赖 RGB 渲染损失（L1 + LPIPS）进行训练，缺乏对 3D 点云结构的直接约束。Uni3R 引入基于 VGGT 稠密点图的几何损失（单向 Chamfer distance），作为软几何先验。消融实验（Table 9）显示，移除几何损失后深度相对误差从 3.9 急剧恶化至 47.99，且在 4 视图设定下模型直接崩溃（Figure 5），证明该损失对训练稳定性和几何精度至关重要。

- **与 VGGT 的关系**：Uni3R 的跨视图 Transformer 编码器和 DPT 解码器均以预训练 VGGT 的权重初始化，但 Uni3R 并非简单复用 VGGT——VGGT 仅输出点图和位姿，而 Uni3R 将其扩展为统一的 3D 高斯原语解码器，同时预测外观、几何和语义特征。

### 2. 适用边界与局限

尽管 Uni3R 在多个基准上取得领先性能，其适用边界和潜在局限值得关注：

#### 2.1 已知边界

- **视角数的下限**：Uni3R 在 2 视图设定下性能仍具竞争力，但其跨视图 Transformer 的设计优势在多视图（4 视图以上）设定下更为显著。Table 6 显示模型在不同输入视角数下具有较好的稳定性，但极端稀疏视角（如单视图）场景不在当前方法的设计范围内。

- **场景类型的泛化**：Uni3R 在 RE10K（室内外房地产场景）、ScanNet（室内场景）上训练，零样本泛化到 Mip-NeRF360（室外复杂场景）时性能下降明显（8 视图 PSNR 仅 19.196 dB，Table 5），表明模型对训练分布外的场景几何和外观仍存在泛化瓶颈。跨域泛化实验（Table 8）在 DTU 和 ScanNet++ 上同样显示性能衰减，但相对基线方法仍保持优势。

- **语义粒度的限制**：Uni3R 的语义特征通过 LSeg 的 2D CLIP 特征蒸馏获得，语义粒度受限于教师模型的能力。对于细粒度类别或开放世界中罕见的语义概念，分割精度可能下降——这一问题在分析中未给出定量证据，需手动验证原始论文中是否有相关讨论。

#### 2.2 潜在局限（需手动验证）

- **计算开销**：跨视图 Transformer 的帧内与跨帧交替注意力机制在视角数增加时计算复杂度呈二次增长。论文未明确报告推理延迟随视角数的 scaling 行为，这一信息对实际部署至关重要。

- **动态场景**：Uni3R 假设输入多视图图像来自静态场景，对于包含运动物体的动态场景，跨视图融合可能产生不一致的几何和语义预测。论文未涉及动态场景的实验评估。

- **几何损失对 VGGT 的依赖**：几何损失依赖冻结的 VGGT 生成稠密点图作为监督信号。若 VGGT 在特定场景类型（如无纹理区域、重复纹理）上预测质量下降，Uni3R 的几何精度可能受到间接影响。论文未分析 VGGT 失败模式对 Uni3R 的传导效应。

### 3. 开放问题

基于上述分析，以下开放问题值得后续工作探索：

1. **语义-几何联合优化的理论理解**：消融实验表明语义损失、几何损失和渲染损失三者缺一不可（Table 7），但三者之间的协同机制尚缺乏深入的理论分析。例如，语义特征蒸馏为何能间接提升几何精度（Table 7 中移除语义损失后深度误差增大），其因果路径值得进一步研究。

2. **跨视图 Transformer 的 scaling 性质**：当前方法在 24 层 Transformer 设定下取得最佳性能，但层数、注意力头数、特征维度等超参数对多视图融合质量的影响未系统探索。特别是视角数增加时，是否存在信息饱和点或冗余融合的问题。

3. **3D 语义特征的可编辑性与可迁移性**：Uni3R 预测的 3D 高斯原语内嵌语义特征，这些特征是否支持下游任务（如 3D 场景编辑、物体操作、导航）的直接调用，以及能否迁移到其他 3D 表示（如 Mesh、NeRF），是连接感知与决策的关键问题。

4. **无位姿设定下的位姿估计与重建的联合优化**：Uni3R 当前通过跨视图 Transformer 隐式处理位姿不确定性，未显式输出相机位姿。将位姿估计与 3D 重建统一到同一框架中，可能进一步提升几何一致性并支持 SLAM 类应用。

## 原文 PDF

![[paperPDFs/CVPR_2026/Uni3R_Unified_3D_Reconstruction_and_Semantic_Understanding_via_Generalizable_Gaussian_Splatting_from_Unposed_Multi_View_Images.pdf]]
