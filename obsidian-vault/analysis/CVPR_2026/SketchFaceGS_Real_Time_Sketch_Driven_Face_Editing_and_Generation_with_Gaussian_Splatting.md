---
title: "SketchFaceGS: Real-Time Sketch-Driven Face Editing and Generation with Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SketchFaceGS_Real_Time_Sketch_Driven_Face_Editing_and_Generation_with_Gaussian_Splatting.pdf
code_link: null
aliases:
- SketchFaceGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 前馈粗到细框架，通过并行Transformer提取几何与外观特征，并利用预训练3D GAN的调制能力注入真实感细节；编辑通过UV Mask融合与层级特征混合保证一致性。
primary_logic: 将Transformer编码的草图结构与基于StyleGAN的3D高斯生成先验结合，形成端到端无优化流水线，首次实现从草图直接生成和交互式编辑可实时渲染的真实感3D头部模型。
claims:
- 首次提出统一、端到端、无需优化的框架，从单张草图生成并交互式编辑照片级3D高斯头部模型。
- 粗到细流水线：粗阶段用两个并行Transformer分支分别提取几何和外观，3D‑GAN调制模块增强高频细节。
- UV Mask融合机制在生成器多尺度特征空间中执行层级混合，避免接缝并保持未编辑区域身份。
- 在草图生成集上达到最优的FID 92.65和KID 4.00；编辑时FID 44.60，端到端延迟0.3 s，渲染帧率高达243 FPS。
---

# SketchFaceGS: Real-Time Sketch-Driven Face Editing and Generation with Gaussian Splatting

> [!tip] 核心洞察
> 将Transformer编码的草图结构与基于StyleGAN的3D高斯生成先验结合，形成端到端无优化流水线，首次实现从草图直接生成和交互式编辑可实时渲染的真实感3D头部模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | SketchFaceGS：基于高斯泼溅的实时草图驱动面部编辑与生成 |
| 英文题名 | SketchFaceGS: Real-Time Sketch-Driven Face Editing and Generation with Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.19202) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SketchFaceGS |
| Dataset | 100幅手绘草图生成集 |

> [!tip] 效果简介
> - 100幅手绘草图生成集 上，FID 92.65；KID (×100) 4.00 ± 0.4。
> - 100次编辑样例集 上，FID 44.60；KID (×100) 0.69 ± 0.2。
> - 编辑身份保持测试 上，PSNR (未编辑区域) 31.12 vs SketchFaceNeRF (优于SketchFaceNeRF)。

## 概述

从稀疏、深度模糊的手绘草图实时重建具有几何一致性和高频真实感细节的3D头部模型，是计算机图形学与交互式内容创作中的核心瓶颈。传统方法或依赖逐实例优化（如基于NeRF的**SketchFaceNeRF**，Gao et al., ACM TOG 2023），或受限于单一编码器结构，难以在保证身份一致性的同时实现前馈式的实时生成与编辑。

**SketchFaceGS** 首次提出统一、端到端、无需优化的框架，从单张草图直接生成并可交互式编辑照片级3D高斯头部模型。其核心洞察在于：将Transformer编码的草图结构与基于StyleGAN的3D高斯生成先验（GGHead）相结合，通过前馈粗到细流水线，在并行提取几何与外观特征后，利用预训练3D GAN的调制能力注入高频真实感细节。编辑时，UV Mask融合机制在生成器多尺度特征空间中执行层级混合，从根本上避免接缝并保持未编辑区域的身份一致性。

实验表明，SketchFaceGS在手绘草图生成集上达到FID 92.65、KID 4.00，编辑FID 44.60，端到端延迟仅0.3秒，渲染帧率高达243 FPS，在生成保真度、编辑灵活性和实时交互性方面均显著优于现有方法。

## 背景与动机

### 问题背景：从二维草图到三维真实感头部的鸿沟

手绘草图是人类最直观、最自由的视觉表达方式之一，尤其在人脸设计与编辑场景中，用户往往希望通过寥寥数笔快速勾勒出期望的面部几何结构。然而，将这种稀疏、深度模糊且高度抽象的二维线条转化为具有几何一致性、高频细节和真实感材质的三维头部模型，始终是计算机图形学与视觉计算领域的一个核心挑战。

这一任务的本质困难在于信息维度的巨大跨越。一张手绘草图仅提供二维轮廓线索，缺乏显式的深度、法向、光照和纹理信息。人类观察者能够凭借先验知识“脑补”出完整的三维形态，但对机器而言，这意味着必须从极度欠约束的输入中恢复密集的三维几何与外观表示。传统方法通常依赖逐实例优化（per-instance optimization），将草图作为约束条件迭代拟合参数化头部模型或神经辐射场，这不仅耗时，而且对初始化和超参数高度敏感，难以满足实时交互式应用的需求。

近年来，三维高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其显式点云表示和高效可微光栅化管线，在实时新视角合成和静态场景重建中展现出显著优势。然而，将3DGS应用于“从草图生成可编辑头部”这一任务时，面临两个根本性瓶颈：其一，如何从稀疏的二维草图直接预测密集且几何一致的三维高斯原语（位置、协方差、颜色等）；其二，如何在对局部区域进行草图驱动的编辑时，保持未编辑区域的身份不变性和跨视角的视觉一致性。

### 现有方法缺口：优化依赖、身份冲突与编辑僵化

当前从草图生成三维头部的方法大致可分为两类，但各自存在明显局限。

**基于NeRF的优化方法**，如**SketchFaceNeRF**（Gao et al., ACM TOG 2023），将草图作为几何约束嵌入神经辐射场的优化过程中，能够生成具有一定真实感的三维头部。然而，这类方法需要针对每张输入草图进行独立的迭代优化，生成时间以分钟甚至小时计，完全无法满足实时交互需求。更关键的是，当用户希望对生成结果进行局部编辑时，必须重新执行完整的优化流程，编辑的灵活性和效率均受到严重制约。

**基于前馈网络的生成方法**，如**S3D**（Song et al., arXiv 2025）和**Nano-LAM**，试图通过单次前向传播直接从草图回归三维表示，从而避免逐实例优化。S3D依赖语义分割引导的生成策略，但在几何一致性上表现不佳，常出现结构扭曲和视角间的不连贯。Nano-LAM采用轻量级Transformer架构，虽然推理速度快，但生成结果往往偏向卡通化，缺乏照片级真实感所需的高频细节。这两类方法均未有效解决一个核心矛盾：草图的几何意图与参考图像的外观身份之间可能存在冲突——例如，用户可能用一张宽脸草图搭配一张窄脸参考图，现有方法缺乏显式的对齐机制来调和这种冲突。

在编辑层面，现有方案同样捉襟见肘。将二维图像编辑方法（如**MagicQuill**, Liu et al., CVPR 2025）直接应用于三维场景，会丢失跨视角一致性，在新视角下暴露出明显的拼接痕迹和模糊伪影。而基于3DGS的直接合成策略——将编辑区域的高斯原语简单替换或叠加——则会在边界处产生严重的几何不连续和外观接缝。SketchFaceNeRF虽然支持编辑，但如前所述，其实时性不足。

### 本文动机：迈向实时、无需优化的统一框架

上述分析揭示了一个明确的研究缺口：**缺少一个统一的、端到端的、无需优化的框架，能够从单张手绘草图直接生成照片级真实感的三维高斯头部模型，并支持实时的、保持身份一致性的局部编辑。**

SketchFaceGS正是为填补这一缺口而提出。其设计动机可归纳为三个层面：

1. **实时性动机**：摒弃逐实例优化的范式，采用纯前馈架构，使得从草图到可渲染三维头部的端到端延迟降至亚秒级，渲染帧率达到实时交互标准（>200 FPS），从而真正赋能草图驱动的即时三维内容创作。

2. **真实感动机**：通过在生成管线中显式注入预训练三维生成先验（3D-GAN），弥补前馈网络在合成高频细节方面的固有不足，使输出摆脱“卡通化”或“模糊化”的困境，逼近照片级真实感。

3. **编辑一致性动机**：将二维草图编辑操作映射到UV纹理空间，并在生成器的多尺度特征层级上进行按元素混合，从根本上避免三维空间中的拼接伪影和身份泄露，确保未编辑区域在任意视角下保持原貌。

简言之，SketchFaceGS试图在“抽象草图的自由度”与“三维真实感的约束”之间建立一座实时、可控的桥梁，为交互式三维头像创作和编辑提供新的技术范式。

## 核心创新

SketchFaceGS 的核心创新在于构建了首个统一、端到端、无需优化的前馈框架，将稀疏且深度模糊的2D草图实时转化为具有几何一致性的照片级3D高斯头部模型，并支持交互式自由视角编辑。该框架通过以下三个关键机制突破，实现了从抽象草图到密集3D高斯的直接映射，从根本上改变了以往依赖逐实例优化的生成范式。

### 1. 生成范式变革：从逐实例优化到前馈实时推理

传统草图到3D的生成方法（如 **SketchFaceNeRF**，Gao et al., ACM TOG 2023）通常需要针对每张输入草图进行耗时的逐实例优化，无法满足实时交互需求。SketchFaceGS 首次提出**无需优化的前馈框架**，从单张草图直接生成3D高斯头部，将端到端延迟压缩至0.3秒，渲染帧率高达243 FPS。这一范式转变的核心在于用数据驱动的先验学习替代了在线优化过程，使得3D生成从离线处理迈入实时交互时代。

### 2. 特征提取架构创新：双路并行Transformer与AdaIN对齐

现有方法多采用单一编码器或顺序处理方式提取草图特征，难以有效解耦几何结构与外观纹理。SketchFaceGS 设计了**双路并行Transformer架构**，分别处理草图和参考图像：

- **几何分支** $\mathbf{T}_{\mathrm{G}}$ 从草图特征中预测每顶点几何特征 $F_{\mathrm{G}}$ 和全局身份向量 $F_{\mathrm{ID-G}}$：
  $$F_{\mathrm{G}}, F_{\mathrm{ID-G}} = \mathbf{T}_{\mathrm{G}}((f_{\mathrm{g}}, f_{\mathrm{ID-g}}), F_{\mathrm{sketch}})$$

- **外观分支** $\mathbf{T}_{\mathrm{A}}$ 从参考图像特征中预测每顶点外观特征 $F_{\mathrm{A}}$ 和全局身份向量 $F_{\mathrm{ID-A}}$：
  $$F_{\mathrm{A}}, F_{\mathrm{ID-A}} = \mathbf{T}_{\mathrm{A}}((f_{\mathrm{a}}, f_{\mathrm{ID-a}}), F_{\mathrm{ref}})$$

两路特征经 **AdaIN对齐网络** 融合，生成几何与外观一致的粗UV特征图：
$$F_{\mathrm{UV-align}} = G_{c}(F_{\mathrm{UV-G}}, F_{\mathrm{UV-A}})$$

这种并行解耦设计使得几何约束（来自草图）与纹理风格（来自参考图）能够独立建模后再深度融合，避免了单一编码器中的信息混淆。

### 3. 真实感细节注入：基于预训练3D-GAN的调制增强

粗阶段生成的UV特征图虽具备几何一致性，但缺乏高频真实感细节。SketchFaceGS 创新性地引入**基于预训练GGHead的3D-GAN调制模块**：设计一个U-Net接收粗UV特征图，预测全局潜变量 $\mathcal{W}$ 和多尺度空间调制参数，注入到预训练的StyleGAN生成器中，从而将3D先验知识转化为高频细节增强。这一设计使得生成结果在保持草图几何约束的同时，具备照片级的皮肤纹理、光影等真实感细节，解决了以往方法（如Nano-LAM）产生卡通化或模糊结果的瓶颈。

### 4. 编辑融合策略创新：UV Mask融合与层级特征混合

在编辑场景中，现有方法或直接重新生成整个头部（导致未编辑区域身份丢失），或在3D高斯空间直接合成（产生接缝与几何不一致）。SketchFaceGS 提出了**UV Mask融合 + 层级特征混合**策略：

- 将2D像素空间的编辑操作转化为参数化UV空间的精确掩码，计算每个高斯的编辑影响权重：
  $$w_i = \sum_{p \in \mathcal{M}} \alpha_i(p) \cdot T_i(p)$$

- 在StyleGAN生成器的**多层级特征空间**中进行按元素混合，而非在最终输出层合成：
  $$\mathbf{f}_k^{\mathrm{fused}} = (1 - \mathbf{M}_{\mathrm{UV}}^{(k)}) \odot \mathbf{f}_k^{\mathrm{orig}} + \mathbf{M}_{\mathrm{UV}}^{(k)} \odot \mathbf{f}_k^{\mathrm{new}}$$

- 混合后的特征继续参与后续层的合成，保证编辑区域与未编辑区域的平滑过渡：
  $$\mathbf{f}_{k+1}^{\mathrm{new}} = \mathrm{Layer}_k(\mathbf{f}_k^{\mathrm{fused}}, \mathcal{W}_{\mathrm{new}})$$

这一策略在未编辑区域达到PSNR 31.12，显著优于SketchFaceNeRF，同时避免了直接3D高斯合成中的接缝问题，实现了真正意义上的实时、无缝、身份保持的局部编辑。

### 创新点总结

| 创新维度 | 现有方法局限 | SketchFaceGS突破 |
|---------|-------------|-----------------|
| **生成范式** | 逐实例优化（SketchFaceNeRF） | 前馈、无需优化的端到端框架 |
| **特征提取** | 单一编码器或顺序处理 | 双路并行Transformer + AdaIN对齐 |
| **细节增强** | 无额外增强或简单上采样 | 预训练3D-GAN调制模块注入高频细节 |
| **编辑融合** | 重新生成或直接3D高斯合成 | UV Mask融合 + 层级特征空间混合 |

这些创新共同构成了从稀疏2D草图到密集3D高斯的实时映射链路，在生成质量（FID 92.65, KID 4.00）和编辑质量（FID 44.60, KID 0.69）上均达到最优水平，同时保持了0.3秒的编辑延迟和最高243 FPS的渲染帧率。

## 整体框架

SketchFaceGS 提出了一套端到端、无需优化的前馈框架，首次实现从单张 2D 手绘草图直接生成照片级真实感 3D 高斯头部模型，并支持实时交互式编辑。该框架的核心设计思想是“粗到细”（coarse-to-fine），将抽象的草图结构与预训练 3D GAN 的强先验相结合，在保证几何一致性的同时注入高频真实感细节。

### 输入与输出

框架接收两类输入：一张手绘草图（提供几何形状约束）和一张参考图像（提供外观风格与纹理信息）。输出为可直接用于实时渲染的 3D 高斯泼溅（3DGS）头部表示，支持自由视角下超过 240 FPS 的光栅化渲染。

### 生成管线：粗到细两阶段架构

生成管线由两个级联阶段构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SketchFaceGS Framework. Our method consists of two core components: (a) a sketch-based generation pipeline that translates a 2D sketch and a reference image into a photorealistic 3D Gaussian head through a coarse-to-fine process, and (b) a real-time editing pipeline that leverages a novel UV Mask Fusion method and a layer-wise feature fusion strategy to enable precise, continuous, and view-independent modifications*

**粗阶段（Coarse Stage）——Transformer 驱动的 UV 特征预测。** 该阶段采用双路并行 Transformer 架构，分别从草图和参考图像中提取特征：
- **Geometry Transformer** $\mathbf{T}_{\mathrm{G}}$ 从草图特征 $F_{\mathrm{sketch}}$ 中预测逐顶点几何特征 $F_{\mathrm{G}}$ 和全局几何身份向量 $F_{\mathrm{ID-G}}$；
- **Appearance Transformer** $\mathbf{T}_{\mathrm{A}}$ 从参考图特征 $F_{\mathrm{ref}}$ 中预测逐顶点外观特征 $F_{\mathrm{A}}$ 和全局外观身份向量 $F_{\mathrm{ID-A}}$。

几何与外观特征随后通过 **AdaIN 对齐网络** $G_c$ 进行融合，生成粗粒度的 UV 特征图 $F_{\mathrm{UV-align}}$。该 UV 图在参数化 UV 空间中已具备基本的几何一致性，但缺乏高频纹理细节。

**细阶段（Fine Stage）——3D-GAN 调制增强。** 粗 UV 特征图被送入一个 U-Net 结构，该网络以预训练的 **GGHead** 生成器为骨干，预测两组关键参数：
1. **全局潜变量** $\mathcal{W}$：通过 MLP 将 U-Net 提取的全局特征与身份向量 $F_{\mathrm{ID-G}}$、$F_{\mathrm{ID-A}}$ 拼接后映射到 StyleGAN 的 W+ 空间；
2. **多尺度空间调制参数**：在 GGHead 生成器的各层级注入，控制高频细节的生成。

这一设计使细阶段能够充分利用 GGHead 预训练期间学到的 3D 人脸先验，将粗 UV 图提升为富含照片级真实感细节的最终 UV 表示，进而解码为完整的 3D 高斯头部。

### 编辑管线：UV Mask 融合与层级特征混合

编辑管线建立在生成管线之上，核心创新在于 **UV Mask Fusion** 机制。用户对 2D 草图所做的局部编辑首先被转换为 UV 空间的精确掩码 $\mathbf{M}_{\mathrm{UV}}$。随后，在 GGHead 生成器的**多层级特征空间**中执行逐层混合：对于第 $k$ 层，融合后的特征图 $\mathbf{f}_k^{\mathrm{fused}}$ 由原始特征 $\mathbf{f}_k^{\mathrm{orig}}$ 和新生成特征 $\mathbf{f}_k^{\mathrm{new}}$ 按掩码加权组合得到：

$$\mathbf{f}_k^{\mathrm{fused}} = (1 - \mathbf{M}_{\mathrm{UV}}^{(k)}) \odot \mathbf{f}_k^{\mathrm{orig}} + \mathbf{M}_{\mathrm{UV}}^{(k)} \odot \mathbf{f}_k^{\mathrm{new}}$$

混合后的特征继续传入下一合成层，结合新的潜变量 $\mathcal{W}_{\mathrm{new}}$ 完成后续生成。这种层级融合策略在 StyleGAN 的特征空间中操作，天然避免了直接 3D 高斯合成时常见的接缝伪影，同时保证了未编辑区域的身份一致性。

### 设计优势总结

整个框架的关键瓶颈突破在于：将 Transformer 编码的草图结构与 StyleGAN 的 3D 高斯生成先验解耦并重新耦合，形成一条从 2D 草图到 3D 高斯的端到端映射通路。相比需要逐实例优化的 SketchFaceNeRF 等前置方案，SketchFaceGS 的前馈特性使端到端编辑延迟降至 0.3 秒，渲染帧率达到 243 FPS，首次实现了真正意义上的实时草图驱动 3D 面部编辑与生成。

### 补充图表

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/001_Figure_1.jpg]]
*Figure 1: SketchFaceGS presents a real-time, sketch-driven editing framework tailored for 3D Gaussian Splatting (3DGS) facial heads. Starting with an original 3D face (a), sequential editing operations (b) are applied to targeted local regions. Our approach delivers photorealistic editing results (c) while preserving the 3D consistency*

## 核心模块与公式推导

SketchFaceGS 的核心由三个紧密耦合的模块构成，分别对应**粗粒度 UV 特征预测**、**细粒度 3D UV 特征增强**和**实时 UV Mask 融合编辑**。整个流水线以前馈方式运行，无需任何逐实例优化。

---

### 3D 高斯泼溅预备知识

方法建立在 3D Gaussian Splatting (3DGS) 的显式表示之上。每个高斯基元定义为一个椭球体：

$$G ( x ) = e ^ { - \frac { 1 } { 2 } ( x - \mu ) ^ { \mathrm { T } } \Sigma ^ { - 1 } ( x - \mu ) } , \quad \mathrm { w i t h ~ } \Sigma = R S S ^ { \mathrm { T } } R ^ { \mathrm { T } }$$

其中 $x$ 为世界坐标，$\mu$ 为高斯中心位置，$\Sigma$ 是由缩放矩阵 $S$ 和旋转矩阵 $R$ 构造的协方差矩阵。渲染时，像素颜色 $C$ 通过对深度排序后的 $N$ 个重叠高斯点进行 $\alpha$ 混合计算：

$$C = \sum _ { i = 1 } ^ { N } c _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

其中 $c_i$ 和 $\alpha_i$ 分别为第 $i$ 个高斯的颜色和不透明度。SketchFaceGS 采用 **GGHead** 作为核心生成先验，该先验将 3D 头部的高斯属性（位置、颜色、不透明度、缩放、旋转）参数化到 UV 空间中，形成一个结构化的 UV 流形表示。

---

### 粗粒度阶段：双路并行 Transformer 与 UV 特征预测

粗阶段的核心任务是从稀疏的 2D 草图和参考图像中提取几何与外观特征，并将其映射到一致的 UV 特征空间。该阶段包含两个并行 Transformer 分支和一个 AdaIN 对齐网络。

**几何 Transformer** 以草图的 DINOv2 特征 $F_{\mathrm{sketch}}$ 为输入，结合可学习的几何查询向量 $f_{\mathrm{g}}$ 和身份查询向量 $f_{\mathrm{ID-g}}$，通过交叉注意力预测每顶点几何特征 $F_{\mathrm{G}}$ 和全局几何身份向量 $F_{\mathrm{ID-G}}$：

$$F_{\mathrm{G}}, F_{\mathrm{ID-G}} = \mathbf{T}_{\mathrm{G}}((f_{\mathrm{g}}, f_{\mathrm{ID-g}}), F_{\mathrm{sketch}})$$

**外观 Transformer** 以参考图像的 DINOv2 特征 $F_{\mathrm{ref}}$ 为输入，结合外观查询向量 $f_{\mathrm{a}}$ 和身份查询向量 $f_{\mathrm{ID-a}}$，预测每顶点外观特征 $F_{\mathrm{A}}$ 和全局外观身份向量 $F_{\mathrm{ID-A}}$：

$$F_{\mathrm{A}}, F_{\mathrm{ID-A}} = \mathbf{T}_{\mathrm{A}}((f_{\mathrm{a}}, f_{\mathrm{ID-a}}), F_{\mathrm{ref}})$$

两个分支输出的特征被重塑为 UV 特征图 $F_{\mathrm{UV-G}}$ 和 $F_{\mathrm{UV-A}}$。由于几何和外观来自不同域，直接拼接会导致身份冲突（消融实验证实，去除对齐后生成结果出现明显身份不一致）。为此，引入 **AdaIN 对齐网络** $G_c$ 将几何 UV 特征图与外观 UV 特征图对齐：

$$F_{\mathrm{UV-align}} = G_{c}(F_{\mathrm{UV-G}}, F_{\mathrm{UV-A}})$$

对齐后的特征图 $F_{\mathrm{UV-align}}$ 即为粗粒度 UV 特征图，它具备几何一致性，但缺乏高频真实感细节。该特征图同时被压缩为全局潜特征 $F_{\mathrm{latent}}$，供细粒度阶段使用。

---

### 细粒度阶段：3D-GAN 调制增强

细阶段利用预训练 GGHead 生成器的调制能力，将粗 UV 特征图提升为富含高频细节的高保真 UV 表示。核心是一个 **U-Net 调制网络**，它以粗 UV 特征图为输入，预测两组参数：

1. **全局潜变量**：将 $F_{\mathrm{latent}}$ 与两个身份向量 $F_{\mathrm{ID-G}}$、$F_{\mathrm{ID-A}}$ 拼接后，通过 MLP 投影到 StyleGAN 的 $\mathcal{W}^+$ 空间：

$$\mathcal{W} = \mathrm{MLP}\big(\mathrm{concat}(F_{\mathrm{latent}}, F_{\mathrm{ID-G}}, F_{\mathrm{ID-A}})\big)$$

2. **多尺度空间调制参数**：U-Net 在多个分辨率层级预测调制参数（缩放和偏置），注入 GGHead 生成器的各合成层，从而在空间上自适应地增强局部细节。

这一设计的因果机制在于：预训练 GGHead 的生成器已编码了丰富的 3D 人脸先验（几何结构、纹理分布、光照模式），U-Net 只需预测轻量的调制信号即可“唤醒”这些先验，将其与输入草图的特定几何和参考外观对齐。消融实验表明，去除增强模块会导致细节严重丢失（FID 和 KID 显著恶化）。

---

### 编辑阶段：UV Mask 融合与层级特征混合

编辑的核心挑战在于：如何在修改局部区域的同时，精确保持未编辑区域的身份一致性。SketchFaceGS 的解决方案是将 2D 编辑操作转化为 UV 空间的掩码，并在 StyleGAN 生成器的**多层级特征空间**中进行混合。

**UV Mask 合成**：用户在任意视点对 2D 渲染结果进行草图编辑后，系统通过可微渲染将编辑区域反向映射到 UV 空间。具体而言，对每个高斯点计算其编辑影响权重：

$$w_i = \sum_{p \in \mathcal{M}} \alpha_i(p) \cdot T_i(p)$$

其中 $\mathcal{M}$ 为 2D 编辑掩码区域，$\alpha_i(p)$ 为高斯 $i$ 在像素 $p$ 处的不透明度，$T_i(p)$ 为累积透射率。权重高于阈值的高斯被标记为“待编辑”，形成 UV 掩码 $\mathbf{M}_{\mathrm{UV}}$。

**层级特征融合**：编辑时，系统同时运行两条生成路径——一条使用原始潜变量 $\mathcal{W}_{\mathrm{orig}}$ 生成原始特征，另一条使用编辑后的新潜变量 $\mathcal{W}_{\mathrm{new}}$ 生成新特征。在生成器的第 $k$ 层，通过 UV 掩码按元素混合：

$$\mathbf{f}_k^{\mathrm{fused}} = (1 - \mathbf{M}_{\mathrm{UV}}^{(k)}) \odot \mathbf{f}_k^{\mathrm{orig}} + \mathbf{M}_{\mathrm{UV}}^{(k)} \odot \mathbf{f}_k^{\mathrm{new}}$$

混合后的特征作为下一合成层的输入：

$$\mathbf{f}_{k+1}^{\mathrm{new}} = \mathrm{Layer}_k(\mathbf{f}_k^{\mathrm{fused}}, \mathcal{W}_{\mathrm{new}})$$

这种**逐层融合**策略的关键优势在于：StyleGAN 的不同层控制不同尺度的属性（粗层控制姿态和脸型，中层控制五官布局，细层控制纹理细节），在特征空间而非最终高斯属性空间进行混合，天然避免了直接 3D 高斯合成产生的接缝和几何不连续问题。消融实验证实，层级特征融合的编辑 FID（44.60）显著优于直接重新生成和 3D 高斯合成策略。

### 补充图表

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/012_Figure_7.jpg]]
*Figure 7: Ablation study on the generation pipeline. (a) Input sketch. (b) Input appearance. (c) Without AdaIN alignment, identity conflicts arise. (d) Without the enhancement module, details are lost. (e) Without identity vectors, identity is inconsistent. (f) With a simple CNN for appearance, style transfer fails. (g) Our full model yields the best result*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/013_Figure_8.jpg]]
*Figure 8: Ablation study on the editing module. Our method (e) achieves the superior results compared with re-generation (c) and direct 3DGS composition (d)*

## 实验与分析

### 核心定量结果

SketchFaceGS在草图驱动的3D头部生成与编辑两个核心任务上均取得了最优性能，且实现了实时交互。

**生成任务**：在100幅手绘草图的测试集上，SketchFaceGS取得了**FID 92.65**和**KID 4.00 ± 0.4**（×100）的最佳成绩（Table 1）。这一结果验证了粗到细流水线在弥合抽象草图与真实感3D头部之间巨大域鸿沟方面的有效性——并行Transformer提取的几何与外观特征，经AdaIN对齐后，为后续的3D-GAN调制模块提供了高质量的初始UV特征图。

**编辑任务**：在100次编辑样例集上，方法取得了**FID 44.60**和**KID 0.69 ± 0.2**（×100）的优异表现（Table 2）。更关键的是，编辑的端到端延迟仅为**0.3秒**，渲染帧率高达**243 FPS**，真正实现了实时交互式编辑。身份保持测试（Table 3）进一步表明，UV Mask融合机制在未编辑区域的PSNR达到**31.12 dB**，显著优于基于优化的SketchFaceNeRF。

### 消融实验分析

消融实验从生成和编辑两个维度揭示了各模块的因果贡献。

**生成流水线消融**（Table 4, Figure 7）：
- **去除AdaIN对齐**：几何与外观特征之间出现严重的身份冲突，导致生成结果的身份不一致（Figure 7c）。这表明AdaIN网络在协调来自草图的几何约束与来自参考图的外观风格之间起着关键的桥梁作用。
- **去除3D-GAN增强模块**：高频真实感细节大量丢失，生成结果呈现模糊、缺乏纹理的退化状态（Figure 7d）。这证实了预训练GGHead的调制能力是注入照片级细节的瓶颈模块——仅靠Transformer的粗阶段预测无法恢复皮肤毛孔、光照等高维细节。
- **去除身份向量**：生成结果的身份一致性显著下降（Figure 7e），说明从几何和外观分支分别提取的全局身份向量，通过MLP投影到StyleGAN W+空间，是维持跨视角身份一致性的因果机制。
- **用简单CNN替代外观Transformer**：风格迁移失败（Figure 7f），表明Transformer的全局注意力对于捕获参考图中的细粒度外观特征不可或缺。

**编辑模块消融**（Table 5, Figure 8）：
- **重新生成策略**：直接根据编辑草图重新生成整个头部，虽然能忠实于编辑指令，但完全丢失了未编辑区域的身份信息。
- **直接3D高斯合成**：在3D高斯层面进行组合，由于缺乏对生成器内部特征空间的访问，产生明显的接缝和几何不连续（Figure 8d）。
- **层级特征融合（完整方法）**：在StyleGAN生成器的多尺度特征空间中，利用UV掩码逐层混合新特征与保留的原始特征，从根本上避免了空间组合带来的接缝问题，同时保证了编辑区域的精确修改和未编辑区域的完美保持（Figure 8e）。这一定量优势在编辑FID上体现为显著优于其他策略。

### 定性分析与可视化

Figure 3展示了方法的生成与编辑能力：给定手绘草图与参考图像，生成的3D头部在几何结构上高度忠实于草图，在外观纹理上精准复现参考图的风格。局部编辑（如改变鼻子形状、调整嘴唇厚度）精确限定在目标区域，未编辑区域保持原样。

Figure 4展示了连续编辑能力：在五个连续步骤中逐步修改草图，方法能够累积编辑效果，在不同视角下均保持照片级真实感和3D一致性。这得益于UV Mask融合机制的无缝特性——每次编辑操作都在特征空间中进行混合，而非在图像空间叠加，避免了误差累积。

Figure 5的生成对比显示：**S3D**（Song et al., arXiv 2025）存在几何不一致问题；**Nano-LAM**产生卡通化结果；**SketchFaceNeRF**（Gao et al., ACM TOG 2023）缺乏细粒度细节。SketchFaceGS通过直接合成高斯属性，恢复出更锐利的几何和更清晰的纹理，同时忠实于输入草图。

Figure 6的编辑对比显示：**MagicQuill**（Liu et al., CVPR 2025）产生风格化/模糊结果；**Nano-LAM**在新视角下编辑不精确；**SketchFaceNeRF**需要逐实例优化，无法实时交互。SketchFaceGS的实时高质量编辑能力源于其前馈架构与层级特征融合策略的协同。

### 失败模式与局限性

尽管整体性能优异，方法存在以下已知失败模式：

1. **身份冲突**：当几何草图与参考外观之间存在显著差异时（例如，草图描绘宽鼻子而参考图是窄鼻子），方法可能产生身份模糊或折中的结果。这是因为预训练GGHead先验对身份空间的约束，使得极端偏离训练分布的输入难以被准确映射。

2. **分布外输入退化**：对于罕见配饰（如特殊眼镜、面纱）、严重遮挡或非标准人脸姿态的输入，生成质量明显下降。当前框架未在多种族、多年龄数据上进行系统评估，泛化性有待验证。

3. **静态头部限制**：框架仅支持静态头部编辑，尚未扩展到面部动画和动态表情控制。将编辑能力融入动态3D头部动画流水线是重要的未来方向。

4. **非皮肤区域编辑受限**：当前方法对发型、眼镜等非皮肤区域的精细编辑支持有限，这受限于GGHead先验的建模范围。

这些失败模式指向了核心瓶颈：**固定的预训练3D-GAN先验在提供强正则化与高频细节的同时，也限制了模型对分布外输入的适应能力**。缓解这一矛盾——例如通过引入可微的几何变形模块或可学习的先验更新机制——是提升鲁棒性的关键方向。

### 补充图表

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison for sketch-based 3D head generation. Lower values indicate better performance*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/009_Table_2.jpg]]
*Table 2: Quantitative comparison for sketch-based 3D head editing. We report image quality (FID, KID) and interaction/rendering performance*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/010_Table_3.jpg]]
*Table 3: Quantitative comparison of identity preservation in unedited regions with SketchFaceNeRF. Higher values indicate better preservation of the original content outside the edited area*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/015_Table_4.jpg]]
*Table 4: Quantitative ablation study for the generation pipeline. All ablated versions show a significant drop in performance compared to our full model. Lower values are better*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/014_Table_5.jpg]]
*Table 5: Quantitative ablation study for the editing module. Our layer-wise feature fusion significantly outperforms alternative strategies. Lower values are better*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison for sketch-based 3D head editing. Given an original head (a) and an edit sketch (b), MagicQuill (c) produces stylized/blurry results; Nano-LAM (d) suffers from imprecise editing with poor novel-view quality. SketchFaceNeRF (e) is optimization-based and non-interactive. Our method (f) achieves real-time, high-quality editing that faithfully follows the sketch*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison for sketch-to-3D generation. In each example, (a) is the input sketch and (c) is the reference appearance. S3D (b) shows geometric inconsistencies. Nano-LAM (d) produces cartoonish results. SketchFaceNeRF (e) lacks fine-grained detail and realism. Our method (f) generates superior results with high fidelity to both geometry and appearance*

![[assets/figures/papers/paper_list_l2269_https_arxiv_org_abs_2604_19202/figures/004_Figure_3.jpg]]
*Figure 3: Given a hand-drawn sketch and a reference image, our method produces a photorealistic 3D head (Top). Our method also support detailed local editing (Bottom)*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

SketchFaceGS 处于**草图驱动 3D 面部生成与编辑**这一交叉领域，其核心贡献在于首次将前馈式推理、3D 高斯泼溅（3DGS）与预训练 3D GAN 先验统一为端到端无优化框架。为理解其技术定位，本节从生成范式、表示选择和编辑机制三个维度梳理其与现有工作的关系。

**从 NeRF 到 3DGS 的表示跃迁。** 早期草图到 3D 面部的工作主要基于 NeRF 表示。**SketchFaceNeRF**（Gao et al., ACM TOG 2023）是该方向的代表性工作，但其生成过程需要逐实例优化，无法满足实时交互需求。SketchFaceGS 以 3D 高斯泼溅替代 NeRF，不仅实现了 243 FPS 的实时渲染，更关键的是通过 GGHead 这一预训练 3D GAN 先验，将生成过程从优化范式转变为前馈范式。这一转变的本质是将“从稀疏草图推断密集 3D 表示”这一病态问题，转化为在预训练生成模型的潜空间中进行条件映射的结构化预测问题。

**从顺序编码到并行双路特征提取。** 在特征提取架构上，**S3D**（Song et al., arXiv 2025）采用基于语义分割的草图到 3D 生成流程，**Nano-LAM** 则使用轻量级 Transformer 进行头部重建。SketchFaceGS 的差异化设计在于**双路并行 Transformer**：几何分支 $\mathbf{T}_{\mathrm{G}}$ 从草图特征 $F_{\mathrm{sketch}}$ 中预测每顶点几何特征 $F_{\mathrm{G}}$ 和全局身份向量 $F_{\mathrm{ID-G}}$，外观分支 $\mathbf{T}_{\mathrm{A}}$ 从参考图像特征 $F_{\mathrm{ref}}$ 中预测 $F_{\mathrm{A}}$ 和 $F_{\mathrm{ID-A}}$，再通过 AdaIN 网络 $G_{c}$ 进行特征对齐。这种设计使得几何约束和外观风格可以独立编码、灵活组合，避免了单一编码器中信息纠缠导致的身份冲突。

**从直接合成到层级特征融合的编辑策略。** 在编辑机制上，直接方案包括重新生成整个头部或对 3D 高斯进行空间组合。消融实验（Table 5）表明，重新生成和直接 3DGS 组合的编辑 FID 均显著劣于 SketchFaceGS 的层级特征融合策略（FID 44.60）。其关键在于 UV Mask Fusion 机制：将 2D 像素空间的编辑映射到参数化 UV 空间，计算每个高斯的影响权重 $w_i = \sum_{p \in \mathcal{M}} \alpha_i(p) \cdot T_i(p)$，然后在 StyleGAN 生成器的第 $k$ 层按元素混合原始特征与新特征：
$$\mathbf{f}_k^{\mathrm{fused}} = (1 - \mathbf{M}_{\mathrm{UV}}^{(k)}) \odot \mathbf{f}_k^{\mathrm{orig}} + \mathbf{M}_{\mathrm{UV}}^{(k)} \odot \mathbf{f}_k^{\mathrm{new}}$$
这种在生成器多尺度特征空间中进行层级混合的策略，从根本上避免了空间拼接带来的接缝问题，同时保持了未编辑区域的身份一致性。与之对比，**MagicQuill**（Liu et al., CVPR 2025）作为 2D 图像编辑方法，在 3D 编辑场景下会产生风格化/模糊的结果（Figure 6），无法保证新视角下的几何一致性。

### 2. 适用边界与局限

SketchFaceGS 的性能建立在以下关键假设之上，这些假设同时定义了其适用边界：

**先验依赖性。** 方法的核心生成能力源于预训练的 GGHead 3D GAN 先验。这带来了双重约束：（1）生成质量的上限受限于 GGHead 的表达能力，当输入草图与参考图像的身份差异过大时，模型可能无法调和几何草图与外观参考之间的冲突，导致身份漂移；（2）GGHead 的训练数据分布决定了模型的泛化边界——文中明确指出，极端姿态、非标准人脸结构、罕见配饰和严重遮挡等超出训练分布（OOD）的输入会导致质量下降。此外，模型对不同种族、年龄群体的泛化性尚未经过系统评估。

**静态表示限制。** 当前框架仅支持静态头部几何的生成与编辑，尚未扩展到面部动画和动态表情控制。这意味着 SketchFaceGS 不适用于需要表情驱动或时序一致性的应用场景（如虚拟角色动画、视频会议中的实时表情迁移）。

**编辑粒度的结构性约束。** UV Mask Fusion 机制依赖于参数化 UV 空间进行编辑区域定位，这使得编辑操作天然受限于 UV 展开的结构连续性。对于发型、眼镜等非皮肤区域或与 UV 参数化对齐较差的几何结构，编辑精度可能受限。文中将“支持对发型、眼镜等非皮肤区域的精细编辑”列为开放问题，暗示当前方法在这些区域的编辑效果可能不够理想。

### 3. 开放问题与未来方向

基于上述局限，SketchFaceGS 揭示了若干值得进一步探索的方向：

1. **身份冲突的缓解机制。** 当几何草图与参考外观存在显著差异时，如何设计更鲁棒的身份解耦与融合策略？可能的路径包括引入显式的身份嵌入约束，或在训练阶段增加跨身份的数据增强。

2. **先验的可替换性与泛化扩展。** 能否将固定的 GGHead 先验替换为其他 3D 生成先验，从而将框架扩展到全身或通用对象？这需要设计与先验无关的条件映射接口，使得框架具有即插即用的模块化特性。

3. **动态编辑与表情控制。** 如何在保持实时性能的前提下，将编辑能力融入动态 3D 头部动画流水线？这涉及将 UV Mask Fusion 机制与时序一致的形变场或 blendshape 参数化相结合。

4. **OOD 鲁棒性与公平性评估。** 针对罕见配饰、严重遮挡等 OOD 输入，以及不同种族、年龄群体的公平性表现，需要构建更具挑战性和多样性的测试基准，并探索针对性的鲁棒训练策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/SketchFaceGS_Real_Time_Sketch_Driven_Face_Editing_and_Generation_with_Gaussian_Splatting.pdf]]