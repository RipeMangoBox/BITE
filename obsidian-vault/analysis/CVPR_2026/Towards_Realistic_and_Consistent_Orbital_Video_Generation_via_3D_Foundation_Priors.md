---
title: Towards Realistic and Consistent Orbital Video Generation via 3D Foundation Priors
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Realistic_and_Consistent_Orbital_Video_Generation_via_3D_Foundation_Priors.pdf
project_link: null
code_link: null
aliases:
- TRCOVG3FP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入三维基础生成模型的隐式形状特征（全局潜在向量和视图相关的体积特征），作为辅助约束条件指导视频生成。
primary_logic: 通过多尺度三维适配器将预训练三维模型的几何先验注入视频扩散模型，可以显著提升形状真实性和多视图一致性，同时保持原视频模型的时间先验和泛化能力。
claims:
- 仅使用单视图图像嵌入无法对未见部分的形状施加足够约束，导致在大视角变化下产生不真实的结构。
- 引入3D基础模型先验后，生成视频的形状真实性和多视图一致性显著提升。
- 消融实验表明全局潜在向量能明显改善多视图一致性（MEt3R降低），全局+局部特征组合达到最佳性能。
- Objaverse-XL 上 PSNR = 22.78 (Ours 21 frames)
---

# Towards Realistic and Consistent Orbital Video Generation via 3D Foundation Priors

> [!tip] 核心洞察
> 通过多尺度三维适配器将预训练三维模型的几何先验注入视频扩散模型，可以显著提升形状真实性和多视图一致性，同时保持原视频模型的时间先验和泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于三维基础先验的真实一致轨道视频生成 |
| 英文题名 | Towards Realistic and Consistent Orbital Video Generation via 3D Foundation Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12309) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Ours |
| Dataset | Objaverse-XL |

> [!tip] 效果简介
> - Objaverse-XL 上，PSNR 22.78 (Ours 21 frames) vs 20.48 (SV3D) (+2.30)；SSIM 0.92 vs 0.91 (+0.01)；LPIPS 0.09 vs 0.12 (-0.03)。

## 概述

从单张物体图像生成真实且一致的多视图轨道视频，是三维内容创作与具身智能等领域的关键需求。现有视频生成方法（如**SV3D**、**Hi3D**）虽然在相机可控性上取得了进展，但其核心瓶颈在于：**仅依赖像素级注意力机制和单视图图像嵌入，无法对物体的未观测部分施加充分的几何约束**。这使得模型在大视角变化下进行长程外推时，容易产生扭曲的形状和不真实的结构，严重损害生成结果的真实感与多视图一致性。

针对这一瓶颈，本文提出将**三维基础模型的形状先验**引入视频扩散生成管线，作为辅助的几何条件信号。核心思路是：利用预训练三维生成模型（**Hunyuan3D**）从输入图像中提取两个尺度的隐式形状特征——**全局潜在向量**提供整体结构引导，**视图相关的体积特征投影**提供细粒度的局部几何细节——并通过一个即插即用的**多尺度三维适配器**，以交叉注意力机制将这些先验注入基础视频扩散模型（**SVD**）的Transformer块中。这一设计既保留了原视频模型的时间先验和泛化能力，又显著增强了对未见区域的形状约束。

实验结果表明，该方法在Objaverse-XL等基准上全面超越现有轨道视频生成与新视图合成基线。定量上，**PSNR提升2.30 dB**（22.78 vs. 20.48），**LPIPS降低0.03**（0.09 vs. 0.12），多视图一致性指标**MEt3R降低至0.05**；定性上，生成结果的形状真实感和时序一致性均有显著改善。消融实验进一步验证了全局与局部特征组合的有效性，以及交叉注意力适配器相较于特征拼接等替代方案的优越性。该方法同时展现出对真实世界图像的良好泛化能力，并能支持非零仰角的复杂动态轨迹。

在方法谱系上，本工作位于**视频扩散生成**与**三维基础模型**的交叉地带。它区别于仅依赖二维扩散先验的轨道视频生成方法（如SV3D、Hi3D），也不同于需要显式三维表示（如NeRF、3DGS）或网格提取的新视图合成与三维生成管线（如**Wonder3D**、**Era3D**、**Trellis**），而是以隐式形状特征为桥梁，实现了二维视频生成与三维几何理解的深度融合。

## 背景与动机

### 轨道视频生成的任务定位

从单张物体图像生成环绕该物体的轨道视频（orbital video），是连接二维图像理解和三维内容创作的关键任务。给定一张输入图像，模型需要渲染出一系列围绕物体旋转的连续帧，每一帧都应当保持物体的形状真实性和多视图一致性。这一任务的核心难点在于，模型必须从有限的单视图观测中外推出物体被遮挡或不可见部分的结构和外观。

### 现有方法的瓶颈

当前主流的轨道视频生成方法，如 **SV3D** 和 **Hi3D**，通常基于视频扩散模型（video diffusion model）构建。这些方法将基础模型在合成视频数据上进行微调，以图像潜在编码（image latent）、CLIP 嵌入和相机位姿参数作为条件，通过像素级注意力机制生成视频帧。然而，这一范式存在两个根本性局限：

**第一，仅依赖单视图图像嵌入无法对物体未观测部分施加足够的结构约束。** 当相机视角发生大幅度变化时，模型需要生成输入图像中完全不可见的物体背面或侧面。由于缺乏显式的三维几何信息，像素级注意力难以建立跨视角的结构对应关系，导致生成的未知视图出现形状扭曲、结构不自然等伪影。原文明确指出：“*using only image embeddings from a single-view input does not impose sufficient constraints on the unobserved parts of the object, hence the model often produces unrealistic structures under large viewpoint changes*”。

**第二，仅在合成视频上微调的基础模型泛化能力有限。** 虽然合成数据能够提供精确的相机控制，但微调后的模型在面对真实世界中未见过的物体类别时，往往出现质量退化。这意味着，仅靠数据层面的扩展难以从根本上解决几何结构的外推问题。

### 三维基础模型的机遇

近年来，三维基础模型（3D foundation models）的兴起为解决上述瓶颈提供了新的可能。这类模型——如 **Hunyuan3D**、**Trellis** 等——能够从单张图像中学习将物体几何直接编码到原生三维潜在空间中（例如通过分词化的点云或体素表示）。它们内部蕴含的隐式形状特征，天然具备表达物体完整三维结构的能力，恰好可以弥补视频生成模型在几何推理上的不足。

### 本文的核心动机

基于上述观察，本文的核心动机是：**将预训练三维基础模型的几何先验引入视频扩散模型，作为辅助的形状条件来指导生成过程**。这一思路的关键优势在于：

- **互补性**：三维基础模型提供全局结构引导和视图相关的细粒度几何细节，而视频扩散模型保留其原有的时间先验和外观生成能力；
- **即插即用**：通过适配器模块实现条件注入，无需重新训练基础模型，保持了方法的效率和泛化性；
- **软约束特性**：形状先验作为“提示”而非硬性约束，使得模型在遵循几何结构的同时，仍能保留生成式模型的随机性和多样性。

这种“视频生成 + 三维先验”的融合范式，为解决大视角变化下的长程外推问题提供了一条新的技术路径。

## 核心创新

本文的核心创新在于将三维基础模型的几何先验作为额外条件引入轨道视频生成流程，从而解决现有方法仅依赖像素级注意力在大视角变化下无法有效约束未见区域形状的瓶颈问题。具体而言，方法在三个关键维度上对基线视频生成框架进行了改造：

**1. 形状条件注入（Shape Condition）**

基线方法（如 SV3D、Hi3D）仅使用输入图像的潜在编码、CLIP 嵌入和相机位姿作为生成条件。当视角发生大幅度变化时，单视图图像嵌入无法对物体未观测部分施加足够的几何约束，导致模型产生不真实的结构。本文提出从预训练的三维基础模型（Hunyuan3D）中提取两种尺度的潜在特征作为额外的形状条件：
- **全局潜在向量**：通过整流流模型以 DINOv2 图像特征为条件去噪得到 $\hat{p}_0$，作为物体整体结构的全局引导；
- **投影体积特征**：从全局向量查询体积特征 $\hat{\pmb{f}}$，并投影为 $M$ 个规范视图的潜在图像，提供视图相关的细粒度几何细节。

**2. 多尺度三维适配器（Multi-Scale 3D Adapter）**

为实现上述形状条件的有效注入，本文设计了一个即插即用的多尺度三维适配器模块。该适配器插入基础视频扩散模型（SVD）的 Transformer 块中，通过交替的交叉注意力层分别融合全局和局部形状特征：
- **全局适配器**：$\mathbf{f}_i^{(1)} = \mathbf{f}_i^{(0)} + \mathrm{CrossAttn}(\mathbf{f}_i^{(0)} ; \mathrm{MLP}(\hat{p}))$，将基础视频特征与全局形状潜在向量进行交叉注意力融合；
- **局部适配器**：$\mathbf{f}_i^{(2)} = \mathbf{f}_i^{(1)} + \mathrm{CrossAttn}(\mathbf{f}_i^{(1)} ; \mathrm{MLP}(\hat{l}))$，进一步融合投影的潜在图像特征。

消融实验（Table 2）证实，基于交叉注意力的适配器设计优于特征拼接和帧堆叠等替代方案，因为它更好地保留了预训练视频模型的时间先验。

**3. 三维特征源的选择与冻结策略**

本文选择 Hunyuan3D 作为三维基础模型，其整流流模型和几何解码器均从预训练权重初始化并在训练和推理过程中保持冻结。这一设计的因果机制在于：利用潜在特征作为物体形状表示，避免了耗时的网格提取过程；同时冻结三维模型确保了其泛化能力的完整保留，而适配器仅需学习如何将这些先验映射到视频生成空间。

**与基线的本质差异**

| 改造维度 | 基线方法 | 本文方法 |
|---------|---------|---------|
| 形状条件 | 无（仅图像嵌入+相机位姿） | 三维基础先验（全局潜在向量+体积特征投影） |
| 适配器模块 | 无 | 多尺度三维适配器（交替交叉注意力） |
| 三维特征源 | 无 | 预训练 Hunyuan3D 模型（冻结） |
| 条件注入方式 | 标准 SVD 条件 | 交叉注意力注入全局和局部潜在特征 |

这一创新设计的核心洞察在于：通过多尺度三维适配器将预训练三维模型的几何先验注入视频扩散模型，可以在显著提升形状真实性和多视图一致性的同时，保持原视频模型的时间先验和泛化能力。实验结果表明，仅引入全局潜在向量即可使多视图一致性指标 MEt3R 显著下降，而全局与局部特征的组合达到了最佳整体性能（PSNR 22.78, CLIP-S 94.19, MEt3R 0.05）。

## 整体框架

本方法的目标是从单张物体图像生成真实且一致的轨道视频。核心思路是将预训练三维基础模型的形状先验注入视频扩散模型，以弥补纯像素级注意力在大视角变化下对未见区域几何约束不足的瓶颈。

整体流程如图2所示，由三个关键阶段串联构成：

1. **形状先验提取**：给定输入图像 $I$，冻结的3D基础模型 $\mathcal{F}(\cdot)$ 从单视图图像中推断物体的隐式形状表示，输出两个尺度的潜在特征——一个去噪后的**全局潜在向量** $\hat{p}_0$（提供整体结构引导）和一组从体积特征投影得到的**视图相关潜在图像**（提供细粒度几何细节）。这一阶段完全基于预训练权重，无需微调。

2. **多尺度条件注入**：基础视频扩散模型 $\mathcal{V}(\cdot)$ 以噪声潜在编码 $z_t$、图像潜在编码 $z_I$、CLIP嵌入 $\pmb{c}_I$ 以及相机参数（仰角 $\pmb{e}$、方位角 $\pmb{a}$）为条件进行去噪。在此基础上，引入**多尺度3D适配器**（Multi-Scale 3D Adapter），通过交替的交叉注意力层将全局和局部形状特征注入Transformer块中，使视频生成过程受到显式的几何约束。

3. **视频帧生成**：经过条件增强的扩散模型逐步去噪，最终解码为 $N$ 帧轨道视频 $\pmb{V}$，在保持原视频模型时间先验和泛化能力的同时，显著提升形状真实性与多视图一致性。

该框架的关键设计在于：形状先验以潜在特征形式传递，避免了耗时的网格提取过程；适配器采用即插即用设计，不改变基础模型的预训练权重，从而保留了其原有的相机控制能力和生成多样性。

### 补充图表

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the method. Given an input image I, we aim to generate a realistic and consistent orbital video V in a base video diffusion model*

## 核心模块与公式推导

### 基础视频扩散模型

本方法以 **SVD**（Stable Video Diffusion）作为基础视频生成模型。给定输入图像 $\mathbf{I}$，模型通过 VAE 编码器得到图像潜在编码 $z_I$，同时提取 CLIP 图像嵌入 $\pmb{c}_I$。在去噪过程中，模型以噪声潜在编码 $z_t$、图像潜在编码 $z_I$、CLIP 嵌入 $\pmb{c}_I$、仰角 $\pmb{e}$ 和方位角 $\pmb{a}$ 为条件，预测噪声 $\hat{\pmb{\epsilon}}_t$：

$$\hat{\pmb{\epsilon}}_t = \mathcal{V}(z_t | z_I, \pmb{c}_I, \pmb{e}, \pmb{a}) \quad t \in \{0, \cdots, T_0\}$$

训练目标为预测噪声与真实噪声之间的加权均方误差：

$$\mathcal{L} = \mathbb{E}_{\mathbf{I},\epsilon,t} [w(t) || \mathcal{V}_\sigma(z_t) - \epsilon ||_2^2]$$

其中 $w(t)$ 为时间步权重，$\mathcal{V}_\sigma$ 表示经预条件常数 $\sigma$ 参数化的去噪网络。

**瓶颈分析**：仅使用合成视频微调的基础模型泛化能力不足，在未见物体上质量退化。更关键的是，单视图图像嵌入无法对物体未观测部分施加足够的几何约束，导致大视角变化下产生不真实的结构。

### 三维基础先验提取

为解决上述瓶颈，方法引入预训练的 **Hunyuan3D** 作为三维基础模型（冻结），从输入图像提取两个尺度的形状先验。

**全局潜在向量**：以 DINOv2 图像特征 $d_I$ 为条件，通过整流流模型 $\mathcal{F}$ 迭代去噪得到全局形状潜在表示 $\hat{p}_0$：

$$\hat{p}_{t-1} = \mathcal{F}(p_t | d_I, t)$$

最终去噪向量 $\hat{p}_0$ 作为物体形状的全局潜在表示，提供整体结构引导。

**体积特征与视图投影**：以全局向量 $\hat{p}_0$ 为条件，通过交叉注意力几何解码器 $\mathcal{G}$ 从网格顶点位置 $\pmb{q}$ 查询体积特征 $\hat{\pmb{f}}$：

$$\hat{\pmb{f}} = \mathcal{G}(\mathrm{PE}(\pmb{q}); \hat{p}_0)$$

其中 $\mathrm{PE}(\cdot)$ 表示位置编码。随后将体积特征投影为 $M$ 个规范视图的潜在图像，提供视图相关的细粒度几何细节。

### 多尺度三维适配器

多尺度三维适配器是方法的核心注入模块，通过交替交叉注意力层将全局和局部形状特征注入基础视频模型的 Transformer 块。

**全局适配**：将基础视频特征 $\mathbf{f}_i^{(0)}$ 与经 MLP 映射的全局潜在向量 $\hat{p}$ 进行交叉注意力融合：

$$\mathbf{f}_i^{(1)} = \mathbf{f}_i^{(0)} + \mathrm{CrossAttn}(\mathbf{f}_i^{(0)} ; \mathrm{MLP}(\hat{p}))$$

**局部适配**：在全局融合基础上，进一步与经 MLP 映射的投影潜在图像特征 $\hat{l}$ 进行交叉注意力融合：

$$\mathbf{f}_i^{(2)} = \mathbf{f}_i^{(1)} + \mathrm{CrossAttn}(\mathbf{f}_i^{(1)} ; \mathrm{MLP}(\hat{l}))$$

该设计的关键优势在于：以潜在特征作为形状表示，避免了耗时的网格提取过程；同时交叉注意力机制最大程度保留了基础视频模型的预训练时间先验，消融实验证实其优于特征拼接和帧堆叠等替代方案。

## 实验与分析

### 核心瓶颈与实验动机

现有视频生成方法（如 **SV3D** 和 **Hi3D**）依赖像素级注意力机制，无法有效处理大视角变化下的长程外推。仅使用单视图图像嵌入对物体不可见部分的形状约束不足，导致模型在生成未知视图时产生不真实的几何结构。本方法的核心假设是：**引入三维基础模型的隐式形状先验作为辅助约束，可显著改善形状真实性与多视图一致性**。

### 主实验结果

Table 1 展示了在 Objaverse-XL 基准上的定量比较。本方法在全部五项指标上均优于现有轨道视频生成基线：

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison with baseline methods. Best results are marked as bold. Our method achieves superior results than baseline methods [21, 25, 42, 46, 47, 55] in all visual quality, shape realism and view consistency metrics on multiple benchmarks [9, 10]*

- **视觉质量**：PSNR 达 22.78（SV3D 为 20.48，提升 +2.30），LPIPS 降至 0.09（SV3D 为 0.12）。
- **形状真实感**：CLIP-S 达 94.19（SV3D 为 92.84，提升 +1.35），表明生成帧与输入图像在语义上更一致。
- **多视图一致性**：MEt3R 降至 0.05（SV3D 为 0.07），几何一致性误差显著降低。

与新颖视图合成方法（**Wonder3D**、**Era3D**）和三维生成方法（**Trellis**、**Hunyuan3D**）相比，本方法同样展现出更好的视觉保真度和形状对齐能力。为确保公平比较，三维生成方法的渲染帧统一使用真实相机姿态并对齐方向。

### 消融实验

Table 2 报告了两组关键消融：

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/004_Table_2.jpg]]
*Table 2: Ablation studies. In top rows, we observe leveraging both scales of features achieves the best overall performance. In bottom rows, we show proposed cross-attention based adapter outperforms alternative feature conditioning approaches as it better preserves pretrained temporal priors*

**形状先验尺度的贡献**：
- 仅使用全局潜在向量时，MEt3R 指标明显下降，CLIP-S 提升，表明全局结构引导对多视图一致性有直接因果作用。
- 加入局部体积特征投影后（Global + Local），所有指标达到最优，说明视图相关的细粒度几何细节补充了全局引导的不足。

**适配器设计的影响**：
- 基于交叉注意力的多尺度适配器优于特征拼接和帧堆叠等替代方案。交叉注意力设计更好地保留了预训练视频模型的时间先验，避免了直接特征注入对生成质量的干扰。

### 定性分析

Figure 3 的定性比较显示，基线方法在大视角变化下常出现形状扭曲和不自然结构（如物体背面生成错误），而本方法产生的结果更真实、一致，伪影更少。Figure 4 展示了在真实世界图片上的泛化能力，本方法在视觉保真度和形状真实感上均优于 **SV3D** 和 **Hi3D**。

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison with baselines. Compared to NVS [21, 25] and video [42, 47] generation works, our method produces more realistic and consistent results with less artifacts, e.g. distorted shapes and unnatural structures. Moreover, we generate more accurate object colors and lighting effects compared to rendered textured meshes from 3D generation methods [46, 55]*

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/013_Figure_3.jpg]]
*Figure 3: Qualitative Comparisons with NVS methods [5, 13, 37] for completeness. Our method produces more realistic results with improved fidelity in shape and appearances details. Moreover, we directly output smooth video results leveraging temporal priors from general video model [3], as shown in supplementary videos*

Figure 6 揭示了三维基础先验的作用机制：从全局潜在向量解码并提取网格后，可见先验为被遮挡和不可见的物体部分提供了互补的几何引导。

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/016_Figure_6.jpg]]
*Figure 6: We show more results of generated frames on diverse input views and unseen objects*

### 失败模式与局限性

Figure 5（附录）展示了典型失败案例。由于基础视频模型和三维基础模型的分辨率限制，复杂场景的细粒度细节难以恢复，导致结果模糊且形状控制失效。当形状先验与真实视频内容不一致时，形状控制可能无效。此外，三维基础模型的纹理质量不够鲁棒，合成复杂未见面外观仍具挑战。

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/010_Figure_5.jpg]]
*Figure 5: Extension to dynamic orbits. Our method can follow complex camera trajectories with non-zero elevations, i.e. dynamic orbits defined by [42] to achieve accurate camera controls*

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/015_Figure_5.jpg]]
*Figure 5: Examples of failure cases. Due to the limited resolution, both base video model and 3D foundation model fail to recover fine-grained details on complex scenes, leading to blurry results and ineffective shape control particular when the shape priors disagree with ground truth videos*

### 关键结论

实验证据链支持以下因果路径：**三维基础先验（全局+局部）→ 多尺度交叉注意力适配器 → 形状真实性与多视图一致性提升**。该方法在不牺牲原视频模型时间先验和泛化能力的前提下，有效解决了大视角变化下的几何外推难题。

### 补充图表

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/001_Figure.jpg]]
*Figure: Input SV3D Ours*

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l2612_https_arxiv_org_abs_2604_12309/figures/008_Figure.jpg]]

## 方法谱系与知识库定位

### 1. 与基线方法的关系

本文工作处于**单视图轨道视频生成**与**三维先验注入**的交叉点。其核心基线可沿两条线索梳理：

**轨道视频生成基线。** 最直接的比较对象是 **SV3D** 和 **Hi3D**，二者均以 Stable Video Diffusion (SVD) 为基础模型，通过图像嵌入和相机位姿条件生成环绕物体的视频序列。本文继承其基础架构（SVD 作为去噪骨干、CLIP 图像嵌入作为语义条件、仰角/方位角作为视角控制），但揭示了一个关键瓶颈：仅依赖像素级注意力进行长程外推时，单视图图像嵌入无法对物体未观测部分施加足够的结构约束，导致大视角变化下产生不真实的几何形变。因此，本文在 SVD 管道中插入了一个额外的形状条件分支，构成“基础视频模型 + 三维形状先验”的混合架构。

**三维生成与先验利用基线。** 在条件注入层面，本文与 **Trellis** 和 **Hunyuan3D** 构成上下游关系。Hunyuan3D 被选作三维基础先验的来源——其整流流模型和几何解码器均以冻结权重使用，提供全局形状潜在向量和体积特征。Trellis 则代表了一类直接进行三维生成的方法。本文的差异化在于：不显式重建网格或辐射场，而是将三维模型的隐空间特征作为视频扩散模型的“软约束”，从而保留视频生成模型的时间先验和泛化能力，同时获得几何一致性收益。

**新视角合成基线。** 本文还与 **Wonder3D**、**Era3D** 等新视角合成方法进行了定性和定量比较。这些方法通常针对离散视角输出，缺乏视频生成模型所具备的时间连续性和动态轨迹控制能力。本文在 Objaverse-XL 和 GSO 基准上的定量结果表明，所提方法在 PSNR（22.78 vs. SV3D 的 20.48）、LPIPS（0.09 vs. 0.12）和 CLIP-S（94.19 vs. 92.84）上均取得显著优势，多视图一致性指标 MEt3R 从 0.07 降至 0.05。

### 2. 适用边界与能力范围

本文方法的有效域由以下条件界定：

- **输入模态：** 单张物体图像，要求物体具有相对清晰的几何结构。对于复杂场景或微小物体区域，三维基础模型的形状先验可能失效，导致形状控制不精确。
- **相机轨迹：** 支持零仰角的环绕轨道和带非零仰角的动态轨道（如 Figure 5 所示），相机控制精度继承自基础 SVD 模型。
- **输出特性：** 生成 21 帧的轨道视频，可通过后处理重建带纹理的三维网格（如附录 Figure 4 所示），但三维重建并非方法的核心输出，而是多视图一致性的验证手段。
- **泛化能力：** 在真实世界图片（in-the-wild）上展现出鲁棒的泛化性，优于基线视频生成方法。这一泛化性来源于三维基础模型在多样化数据上的预训练，以及适配器对基础视频模型时间先验的保护。

### 3. 局限与失败模式

本文明确指出的局限包括：

1. **视觉保真度受限于基础模型分辨率。** 基础 SVD 模型和三维基础模型的分辨率有限，在处理复杂场景时细粒度细节会退化，产生模糊结果，形状控制的有效性也随之下降（见附录 Figure 5 失败案例）。
2. **纹理质量不足。** 仅利用了基础模型的形状先验，其纹理先验质量不够鲁棒，合成复杂的未见外观仍具挑战。
3. **形状先验与真实视频不一致。** 当三维基础模型产生的形状先验与真实视频中的物体结构不一致时，可能导致无效的形状控制——这是“软约束”注入方式的内在风险。
4. **严格同一性未解决。** 当前方法实现的是多视图一致性（软约束），而非严格的同一性（hard identity constraint），后者仍是开放问题。

### 4. 开放问题与未来方向

从本文的讨论和消融结果中可以提炼出以下开放方向：

- **更强基础模型的融合。** 将形状先验与更强大的基础视频模型结合，以突破当前分辨率和视觉保真度的上限。
- **复杂外观的合成。** 探索利用三维基础先验来合成复杂的、未见过的物体外观，补足当前纹理先验的不足。
- **推理效率优化。** 当前管道涉及三维基础模型的前向推理和适配器的交叉注意力计算，如何进一步提升推理效率以支持实时应用是一个工程性但重要的方向。
- **严格同一性约束。** 从软约束的多视图一致性走向严格的同一性一致性，可能需要引入显式的三维表示（如神经辐射场或高斯泼溅）作为中间监督，或设计更强的跨帧约束机制。

### 5. 知识库定位

本文在方法谱系中的位置可概括为：**以冻结的三维基础模型为条件先验源，通过多尺度交叉注意力适配器将其注入视频扩散模型，在不破坏预训练时间先验的前提下显著提升形状真实性和多视图一致性。** 其核心贡献不在于提出新的生成范式，而在于揭示并有效解决了“像素级注意力无法约束未观测几何”这一瓶颈，并验证了隐式三维特征作为视频生成条件的可行性与有效性。这一思路可泛化为“冻结的三维先验编码器 + 可训练的轻量适配器 + 冻结或微调的视频生成器”的插件式框架，为后续工作提供了清晰的扩展接口。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Realistic_and_Consistent_Orbital_Video_Generation_via_3D_Foundation_Priors.pdf]]