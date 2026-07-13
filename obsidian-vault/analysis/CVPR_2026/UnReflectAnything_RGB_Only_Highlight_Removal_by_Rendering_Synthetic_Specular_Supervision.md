---
title: "UnReflectAnything: RGB-Only Highlight Removal by Rendering Synthetic Specular Supervision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UnReflectAnything_RGB_Only_Highlight_Removal_by_Rendering_Synthetic_Specular_Supervision.pdf
project_link: "https://alberto-rota.github.io/UnReflectAnything/"
code_link: null
aliases:
- UnReflectAnything
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过单目几何估计与物理渲染合成逼真高光，为RGB-only高光去除生成像素级和token级监督信号；并通过冻结DINOv3特征上的token修复，解耦高光定位与外观恢复。
primary_logic: 将虚拟高光合成与token空间修复结合：利用任意RGB图像的单目几何、Fresnel感知着色和随机光照生成物理上合理的高光训练对，避免了对真实配对数据的依赖；在冻结的视觉Transformer特征空间中直接修复被破坏的patch token，保留全局语义并重建无高光的漫反射外观。
claims:
- 我们提出虚拟高光合成管道，利用单目几何、Fresnel感知着色和随机光照，使模型能够在任意RGB图像上训练而无需配对的无高光数据。
- Transformer修复器直接在特征空间中重建被遮盖的DINOv3 patch token，恢复具有全局上下文的漫反射外观。
- 将虚拟高光合成与token空间修复结合：利用任意RGB图像的单目几何、Fresnel感知着色和随机光照生成物理上合理的高光训练对，避免了对真实配对数据的依赖；在冻结的视觉Transformer特征空间中直接修复被破坏的patch token，保留全局语义并重建无高光的漫反射外观。
---

# UnReflectAnything: RGB-Only Highlight Removal by Rendering Synthetic Specular Supervision

> [!tip] 核心洞察
> 将虚拟高光合成与token空间修复结合：利用任意RGB图像的单目几何、Fresnel感知着色和随机光照生成物理上合理的高光训练对，避免了对真实配对数据的依赖；在冻结的视觉Transformer特征空间中直接修复被破坏的patch token，保留全局语义并重建无高光的漫反射外观。

| 字段 | 内容 |
|------|------|
| 中文题名 | UnReflectAnything：基于合成高光渲染的仅RGB高光去除 |
| 英文题名 | UnReflectAnything: RGB-Only Highlight Removal by Rendering Synthetic Specular Supervision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09583) · [Project](https://alberto-rota.github.io/UnReflectAnything/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UnReflectAnything |
| Dataset | PSD, SHIQ, SSHR, CroMo, HouseCat6D, SCRREAM, Cholec80, SCARED, StereoMIS-Tr |
> [!tip] 效果简介
> - Transformer修复器直接在特征空间中重建被遮盖的DINOv3 patch token，恢复具有全局上下文的漫反射外观。

## 概要

高光去除是图像复原中的经典难题。镜面反射在非朗伯体表面（如皮肤、湿润组织、抛光物体）上形成饱和亮斑，严重破坏纹理信息并干扰下游视觉任务。现有方法面临根本性瓶颈：**真实场景下配对的高光/无高光图像几乎无法获取**，尤其在手术内窥镜等复杂光照环境中。这导致基于监督学习的方法泛化性差，而基于GAN或物理先验的无监督方法则容易过度平滑纹理或产生色偏。

UnReflectAnything 针对这一瓶颈提出了两个关键机制。第一，**虚拟高光合成管道**：利用单目几何估计（MoGe-2）从任意RGB图像恢复深度与法线，通过Fresnel感知的Blinn-Phong着色和随机光照采样，在无需配对真值的情况下生成物理上合理的高光训练对。第二，**token空间修复**：将高光去除从像素空间迁移到冻结的DINOv3-Large特征空间，通过轻量级ViT修复器直接重建被高光破坏的patch token，利用全局语义上下文和局部均值先验恢复漫反射外观，从而解耦高光定位与纹理重建。

在方法定位上，UnReflectAnything 与 **StableDelight**（Stable-X, 2025）、**PolarAnything** 和 **PolarFree** 等近期工作形成对比：后者依赖偏振信息或扩散先验，而本方法仅需单张RGB图像即可跨自然场景和外科手术场景实现一致的高光抑制。消融实验证实，token空间修复是性能核心——若退化为RGB空间修复，SSIM从0.957骤降至0.816；移除局部均值先验则使大块高光区域的修复不稳定（SSIM降至0.911）。此外，排除数据集原始高光区域的监督策略至关重要：若不排除，网络会将饱和反射误认为漫反射，MSE_m升至0.022。

该方法的主要局限在于：对透明/折射物体上的高光处理能力有限；低梯度、平滑衰减的高光区域重建质量下降；依赖单目几何估计精度，几何错误会传导至合成高光质量。这些失败模式在论文的Figure 8中有具体展示。



高光去除是计算机视觉与图形学中长期存在的底层视觉问题。在非朗伯体表面，镜面反射会叠加在漫反射纹理之上，形成局部过曝区域，严重干扰下游任务——从3D重建、像素匹配到手术场景的视觉感知。尽管该问题已被研究数十年，现有方法仍面临一个根本性瓶颈：**缺乏真实场景下配对的高光/无高光图像**。这一瓶颈在非朗伯体表面和复杂光照条件下尤为突出，例如外科手术场景中的湿润组织表面，导致现有RGB高光去除方法的泛化性显著受限。

### 现有方法的缺口

当前高光去除方法大致沿三条技术路线展开，但各自存在结构性缺陷：

**基于物理模型的方法**（如**HighlightNet** 、**SpecularityNet** ）依赖对光照和材质的显式建模，通常需要多视角或多光照输入。这类方法在受控条件下表现良好，但在单张RGB图像、未知光照的真实场景中难以推广。

**基于学习的方法**则面临数据困境。配对监督方法需要同一场景的有高光和无高光图像对，采集成本极高；非配对方法（如**MG-CycleGAN** 、**DHAN-SHR** ）通过循环一致性等约束绕过配对需求，但容易产生过度平滑的纹理或色偏伪影。近期工作**StableDelight** 尝试利用扩散先验进行高光去除，但在保持细粒度纹理方面仍有不足。

**基于偏振的方法**（如**PolarAnything** 、**PolarFree** ）利用偏振信息分离镜面反射与漫反射分量，物理上更为合理，但需要额外的偏振成像硬件，限制了其应用范围。

此外，在手术场景中，**Endo-STTN** 等方法针对内窥镜图像进行了专门设计，但泛化到自然场景的能力有限。

### 核心矛盾与本文动机

上述方法的共同困境可归结为一个核心矛盾：**高质量的高光去除需要理解场景的几何与光照，但获取真实配对数据以训练这种理解恰恰极其困难**。这形成了一个闭环——没有数据就无法训练好模型，没有好模型就难以在真实场景中工作。

UnReflectAnything的动机正是打破这一闭环。其核心思路是：**如果无法获取真实配对数据，就通过物理渲染合成逼真的高光**。具体而言，利用单目几何估计从任意RGB图像恢复场景的三维结构，再通过Fresnel感知的着色模型和随机光照参数渲染物理上合理的高光，从而生成像素级配对的高光/无高光训练对。这一策略使模型能够在任意RGB图像上训练，无需任何真实配对数据。

更进一步，该方法将高光去除重新定义为**特征空间的修复问题**：在冻结的视觉Transformer（DINOv3）特征空间中，定位被高光破坏的patch token并进行修复，而非直接在RGB像素空间操作。这种设计将高光定位与外观恢复解耦，利用预训练ViT蕴含的全局语义先验来重建无高光的漫反射外观，避免了像素空间修复常见的模糊和伪影。



## 核心方法与创新机理

UnReflectAnything 的核心创新在于将**虚拟高光合成**与**token空间修复**相结合，从根本上绕过了RGB高光去除任务中长期存在的配对数据瓶颈。其关键改变（changed slots）体现在以下四个维度：

### 1. 训练数据来源：从配对真实数据到虚拟高光合成

传统方法（如 **HighlightNet**、**MG-CycleGAN** 等）依赖配对真实数据或非配对GAN训练，这在非朗伯体表面和复杂光照场景（如外科手术）下极难获取。UnReflectAnything 提出**虚拟高光合成管道**（Virtual Highlight Synthesis），利用单目几何估计（MoGe-2）从任意RGB图像重建3D点云与表面法线，再结合随机采样的点光源、Fresnel感知着色和Blinn-Phong反射模型，渲染物理上合理的高光训练对。这一管道使模型能够在无配对无高光真值的任意RGB图像上训练，直接消除了对真实配对数据的依赖。

### 2. 修复空间：从RGB像素空间到DINOv3 patch token空间

现有方法通常在RGB像素空间进行修复，容易导致纹理过度平滑或色偏。UnReflectAnything 将修复操作提升至**冻结的DINOv3-Large Vision Transformer的特征空间**：高光预测器 $H$ 生成软性高光概率图，用于在patch token序列中遮盖受高光影响的token；轻量级ViT-based Token Inpainter $T$ 直接在该特征空间中重建被破坏的token，利用全局语义上下文恢复漫反射外观。消融实验表明，若将token空间修复退化为RGB空间修复，SSIM从0.957骤降至0.816，MSE$_m$从0.003升至0.007，验证了特征空间修复的关键作用。

### 3. 编码器策略：从可训练特征提取器到冻结的DINOv3

传统方法使用可训练的CNN或Transformer作为特征提取器，需要在高光去除任务上端到端微调。UnReflectAnything 采用**冻结的DINOv3-Large**作为编码器 $E$，提取多尺度patch特征 $\mathcal{F} = \{\mathbf{F}_1, \mathbf{F}_2, \mathbf{F}_3, \mathbf{F}_4\}$。冻结策略保留了预训练模型强大的语义先验，使Token Inpainter能够利用全局上下文推断被高光遮挡的漫反射特征，而非从零学习视觉表征。

### 4. 监督策略：从全像素监督到排除数据集高光的token级监督

传统方法直接监督高光区域的像素重建，但数据集自带的真实高光区域缺乏对应的无高光真值，会误导网络将饱和反射当作漫反射。UnReflectAnything 采用**双掩码监督策略**：仅对合成高光区域与数据集高光区域的补集（即可靠patch）计算token修复损失 $\mathcal{L}_{\mathrm{inp}}$，显式排除数据集高光像素。消融实验证实，取消该排除策略会导致MSE$_m$从0.003飙升至0.022，说明错误监督的破坏性影响。

### 创新机制的内在耦合

上述四个changed slots并非孤立存在，而是形成了因果闭环：虚拟高光合成提供了可控的像素级监督信号，使模型能够定位高光区域；冻结的DINOv3编码器提供了语义丰富的特征空间；token空间修复在此空间中利用全局上下文重建漫反射外观；排除数据集高光的监督策略则确保修复器不会被错误信号误导。这种“合成监督—特征定位—token修复—可靠监督”的耦合机制，是UnReflectAnything在多个域（自然图像、手术内窥镜）上实现一致高光去除的根本原因。



UnReflectAnything 的整体设计围绕一个核心矛盾展开：真实场景下缺少配对的高光/无高光图像，尤其在非朗伯体表面和复杂光照下（如外科手术场景），导致现有 RGB 高光去除方法泛化性差，且容易过度平滑纹理或产生色偏。为解决这一问题，该方法将**虚拟高光合成**与**token 空间修复**解耦为两个协同的子系统：前者通过物理渲染生成逼真的训练监督信号，后者在冻结的视觉 Transformer 特征空间中修复被高光破坏的 patch token，从而恢复无高光的漫反射外观。

### Pipeline 总览

整体流程如 Figure 3 所示，由四个核心模块串联构成：

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/003_Figure_3.jpg]]
*Figure 3: UnReflectAnything model architecture. A pretrained DINOv3 encoder backbone E extracts a hierarchy of multi-scale patch features from the input image (only the last feature map in the hierarchy is shown for clarity). A DPT-inspired highlight predictor H produces a soft, pixel-level highlight map, serving as a mask on the feature maps. A lightweight ViT-based Token Inpainter T operates on these masked features, learning to reconstruct the underlying diffuse features in place of those corrupted by highlights. An RGB DPT decoder D transforms the inpainted feature maps into a reflection-free diffuse RGB image. This decoder is pre-trained in an autoencoderfashion to reconstruct the input RGB imag...*

1. **冻结的 DINOv3-Large 编码器 E**：从输入 RGB 图像中提取多尺度 patch 特征 $\mathcal{F} = \{\mathbf{F}_1, \mathbf{F}_2, \mathbf{F}_3, \mathbf{F}_4\}$，其中 $\mathbf{F}_\ell \in \mathbb{R}^{N \times C}$。该编码器在整个训练过程中保持冻结，以保留预训练视觉 Transformer 的全局语义表征能力。

2. **高光预测器 H**：一个受 DPT（Dense Prediction Transformer）启发的轻量级头部，从编码器特征中预测软性高光概率图 $\mathbf{I}_{\mathrm{high}}$，用于定位镜面反射区域。该图同时作为后续 token 修复的掩码引导。

3. **Token 修复器 T**：一个轻量级 ViT 模块，在特征空间中直接对高光掩码覆盖的 patch token 进行修复。其核心逻辑（Figure 4）是：对每个待修复 token，利用其局部邻域计算均值先验，与可学习的掩码 token 和位置嵌入相加后送入 Transformer 块进行精炼，最终输出干净的漫反射特征。

4. **RGB DPT 解码器 D**：将修复后的特征图 $\mathbf{F}_{\mathrm{comp}}$ 转换为无高光的 RGB 图像 $\mathbf{I}_{\mathrm{diff}}$。解码器在训练前经过自编码器预训练，以 L1 和 SSIM 损失从冻结的 DINOv3 特征中重建原始 RGB 图像。

整个模型的形式化定义为：

$$(\mathbf{I}_{\mathrm{diff}}, \mathbf{I}_{\mathrm{high}}) = M(\mathbf{I})$$

其中 $\mathbf{I}_{\mathrm{high}} = H(E(\mathbf{I}))$，$\mathbf{I}_{\mathrm{diff}} = D\big(T(E(\mathbf{I}), \mathbf{I}_{\mathrm{high}})\big)$。

### 训练数据流：虚拟高光合成管道

由于缺乏真实配对数据，UnReflectAnything 引入了一条**虚拟高光合成管道**（Figure 2），从任意单张 RGB 图像生成物理上合理的高光训练对。该管道的关键因果机制在于：利用单目几何估计将二维图像提升为三维场景，再通过 Fresnel 感知的 Blinn-Phong 着色模型渲染高光，使得合成高光与场景几何结构保持光度一致性。

具体而言（详见 Section 3.1），给定输入线性 RGB 图像 $\mathbf{I}$：
- 使用现成的单目几何估计方法（MoGe-2 ）推断逐像素的度量深度、表面法线 $\mathbf{n}$ 和内参；
- 从深度图构建三维点云 $\mathbf{X}$，在相机空间中随机采样点光源位置 $\mathbf{L}$，计算归一化的视线方向 $\mathbf{v}$ 和光源方向 $\mathbf{l}$；
- 通过 Schlick-Fresnel 近似计算反射系数 $R = R_0 + (1 - R_0)(1 - \mathbf{v} \cdot \mathbf{h})^5$，并渲染 Blinn-Phong 高光强度 $\mathbf{H} = K_H R (\mathbf{n} \cdot \mathbf{h})^S$；
- 最终通过 RGB 合成 $\mathbf{I}_{\mathrm{high}} = (1 - \mathbf{H})\mathbf{I} + \mathbf{H}(\mathbf{I} + \mathcal{K}_H \delta \mathbf{1}_3)$ 得到带高光的训练图像。

这一合成策略的巧妙之处在于：它将高光生成的物理约束（几何、材质、光照）与数据驱动的修复网络解耦，使模型能够在任意 RGB 图像上训练，而无需依赖稀缺的真实配对数据。

### 监督策略：可靠 token 的选择性监督

训练时，UnReflectAnything 并非对所有 patch 施加监督。如 Figure 5 所示，监督掩码 $\mathcal{M}$ 被限制在合成高光区域与数据集高光区域的交集之外——即**显式排除数据集原始高光像素**，仅对可靠的合成高光 patch 进行 token 级监督。这避免了将数据集中饱和的镜面反射区域误当作漫反射真值来训练，从而防止网络学习到错误的颜色或纹理。修复器仍需学习完成所有高光区域（包括合成高光和数据集高光），但监督信号仅来自可控的合成部分。

Token 修复损失 $\mathcal{L}_{\mathrm{inp}}$ 结合了 L1 距离和余弦相似度，对修复后的 token $\mathbf{F}_i^*$ 与目标 token $\mathbf{F}_i$ 进行约束。解码器预训练则采用自编码器损失 $\mathcal{L}_{\mathrm{AE}}$，最小化 $D(E(\mathbf{I}))$ 与 $\mathbf{I}$ 之间的 L1 和 SSIM 差异。

### 输入输出流总结

- **输入**：单张线性 RGB 图像 $\mathbf{I}$（可为自然场景或外科手术图像）。
- **中间表示**：DINOv3 多尺度 patch token $\mathcal{F}$，软性高光概率图 $\mathbf{I}_{\mathrm{high}}$，修复后的特征图 $\mathbf{F}_{\mathrm{comp}}$。
- **输出**：无高光的漫反射 RGB 图像 $\mathbf{I}_{\mathrm{diff}}$ 和高光预测图 $\mathbf{I}_{\mathrm{high}}$。

这一设计将高光定位（像素级预测）与外观恢复（token 级修复）分配到不同模块，并通过冻结的 DINOv3 编码器保留全局语义上下文，从而在无需配对真值的情况下实现跨域的高光去除。

### 补充图表

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/001_Figure_1.jpg]]
*Figure 1: UnReflectAnything removes specular highlights from RGB images without paired supervision. A Virtual Highlight Synthesis pipeline renders physically plausible reflections from estimated geometry, providing realistic pseudo-pairs across natural and surgical domains. The model predicts a soft highlight map and inpaints masked DINOv3 tokens, reconstructing reflection-free diffuse images. It generalizes across diverse scenes, achieving faithful highlight suppression and texture recovery*



UnReflectAnything 的核心架构由四个模块串联构成：冻结的 DINOv3-Large 编码器、高光预测器、Token 修复器以及 RGB DPT 解码器。其关键创新在于将修复操作从像素空间迁移至冻结的视觉 Transformer 特征空间，并通过物理渲染合成训练监督信号。

### 虚拟高光合成管道

给定任意线性 RGB 图像 $\mathbf{I}$，首先通过单目几何估计网络（MoGe-2）恢复场景的度量深度 $D$、表面法线 $\mathbf{n}$ 及相机内参 $K$，由此构建三维点云 $\mathbf{X}$。随后在相机空间中随机采样点光源位置 $\mathbf{L}$，计算归一化的视线方向 $\mathbf{v}$ 与光源方向 $\mathbf{l}$：

$$
\mathbf{v} = \frac{\mathbf{X}}{\|\mathbf{X}\|}, \qquad \mathbf{l} = \frac{\mathbf{L} - \mathbf{X}}{\|\mathbf{L} - \mathbf{X}\|} \tag{1}
$$

基于 Blinn-Phong 光照模型，引入 Schlick-Fresnel 反射系数以调制掠射角处的镜面反射强度。半向量 $\mathbf{h} = \frac{\mathbf{v} + \mathbf{l}}{\|\mathbf{v} + \mathbf{l}\|}$，Fresnel 系数为：

$$
R = R_0 + (1 - R_0)(1 - \mathbf{v} \cdot \mathbf{h})^5 \tag{2}
$$

其中 $R_0 = 0.04$ 为正入射时的 Fresnel 反射率近似。合成高光强度图 $\mathbf{H}$ 为：

$$
\mathbf{H} = K_H R (\mathbf{n} \cdot \mathbf{h})^S \tag{3}
$$

其中 $K_H$ 控制高光幅度，$S$ 控制高光锐度。最终通过 alpha 合成将高光叠加至原图：

$$
\mathbf{I}_{\mathrm{high}} = (1 - \mathbf{H})\mathbf{I} + \mathbf{H}(\mathbf{I} + \mathcal{K}_H \delta \mathbf{1}_3) \tag{4}
$$

$\mathcal{K}_H$ 为亮度增量因子，$\delta$ 为随机扰动，$\mathbf{1}_3$ 为三维全1向量。此管道无需配对的无高光真值，即可从任意 RGB 图像生成物理上合理的高光/无高光训练对。

### 冻结编码器与多尺度特征提取

采用冻结的 DINOv3-Large Vision Transformer 作为编码器 $E$，从输入图像中提取四层多尺度 patch token 特征：

$$
\mathcal{F} = \{\mathbf{F}_1, \mathbf{F}_2, \mathbf{F}_3, \mathbf{F}_4\} = E(\mathbf{I}), \qquad \mathbf{F}_\ell \in \mathbb{R}^{N \times C} \tag{5}
$$

冻结编码器的核心优势在于：其预训练特征空间已编码丰富的语义与几何先验，高光破坏的仅是局部 token，而非全局语义结构，这为后续 token 空间修复提供了基础。

### 高光预测器

DPT 风格的高光预测器 $H$ 接收编码器多尺度特征，输出像素级软性高光概率图 $\mathbf{I}_{\mathrm{high}}$。该概率图经池化后转化为 patch 级二值掩码 $\mathbf{P}$，标记哪些 token 受到高光污染需要修复。

### Token 修复器

Token 修复器 $T$ 是方法的核心模块，直接在 DINOv3 特征空间中重建被高光破坏的 patch token。其关键设计包括：

**局部均值先验**：对每个待修复 token，取其空间邻域内可见 token 的均值 $\mathbf{F}_{\mathrm{mean}}$ 作为初始猜测，缓解大面积高光区域的信息缺失。

**种子 token 构建**：将掩码 token $\mathbf{f}_{\mathrm{mask}}$（可学习参数）与局部均值先验按 $\lambda$ 混合，与位置编码 $\mathbf{E}_{\mathrm{pos}}$ 相加，形成 ViT 修复器的输入：

$$
\mathbf{F}_{\mathrm{seed}} = \mathbf{P} \odot [\lambda \mathbf{f}_{\mathrm{mask}} + (1-\lambda) \mathbf{F}_{\mathrm{mean}}] + (1-\mathbf{P}) \odot \mathbf{F} + \mathbf{E}_{\mathrm{pos}} \tag{6}
$$

**修复与合并**：轻量 ViT 对种子 token 序列进行自注意力处理，输出修复后的特征。最终将修复 token 与原始可见 token 合并：

$$
\mathbf{F}_{\mathrm{comp}} = \mathbf{P} \odot \mathrm{ViT}(\mathbf{F}_{\mathrm{seed}}) + (1-\mathbf{P}) \odot \mathbf{F} \tag{7}
$$

### 训练监督与损失函数

**Token 修复损失**：仅对可靠区域 $\mathcal{M}$（合成高光区域与数据集高光区域的差集）进行监督，避免将数据集原有的饱和高光当作漫反射真值：

$$
\mathcal{L}_{\mathrm{inp}} = \frac{1}{|\mathcal{M}|} \sum_{i \in \mathcal{M}} [\alpha \|\mathbf{F}_i^* - \mathbf{F}_i\|_1 + (1-\alpha)(1 - \mathbf{F}_i^* \mathbf{F}_i^\intercal)] \tag{8}
$$

其中 $\mathbf{F}_i^*$ 为修复后的 token，$\mathbf{F}_i$ 为对应的无高光目标 token。损失结合 L1 距离与余弦相似度，$\alpha$ 为平衡系数。

**解码器预训练损失**：RGB DPT 解码器 $D$ 在冻结编码器特征上以自编码器方式预训练，重建原始 RGB 图像：

$$
\mathcal{L}_{\mathrm{AE}} = \|D(E(\mathbf{I})) - \mathbf{I}\|_1 + (1 - \mathrm{SSIM}(D(E(\mathbf{I})), \mathbf{I})) \tag{9}
$$

预训练使解码器学会从 DINOv3 特征恢复像素级细节，为后续高光去除阶段的解码提供初始化。

### 补充图表

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/002_Figure_2.jpg]]
*Figure 2: Synthetic Highlight Generation Pipeline from any image. Given a single RGB image (left), a per-pixel depth and surface normals is first estimated using a monocular geometry network. The recovered geometry defines a 3D point cloud X with associated surface normals n and view directions v. The light source position L is sampled in camera coordinates, producing local illumination vectors l. These geometric quantities drive a physically based Blinn–Phong [18] rendering mode generating a synthetic highlight intensity map that is photometrically consistent with the inferred scene structure. The highlight is finally composited with the input RGB*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/005_Figure_4.jpg]]
*Figure 4: Patch token inpainting logic. A local neighborhood (purple borders) for each token to be inpainted is used to compute the local mean priors. This mean priors are summed with the Positional Embeddings and a learned mask token and fed into a sequence of transformer blocks which refine the tokens to the final feature*



## 实验与关键发现

### 主实验结果

UnReflectAnything 在多个基准数据集上进行了全面评估，涵盖提供配对无高光真值的数据集（**Table 1**）和无配对真值的数据集（**Table 2**）。

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/007_Table_1.jpg]]
*Table 1: Comparison across datasets that provide paired diffuse-only ground truth. The best score in each metric is highlighted in bold*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/008_Table_2.jpg]]
*Table 2: Comparison across datasets that do not provide paired diffuse-only ground truth. The best score in each metric is highlighted in bold. For all metrics, lower is better*

**配对真值数据集评估**（PSD、SHIQ、SSHR）：在这三个数据集上，UnReflectAnything 在 MSE_m、PSNR 和 SSIM 三项指标上均取得了最优或竞争性性能。具体而言，在 PSD 数据集上，方法达到 MSE_m 0.004、PSNR 17.230、SSIM 0.911。与基线方法相比，UnReflectAnything 在非朗伯体表面和复杂光照场景下展现出更稳定的高光抑制和纹理保持能力，避免了传统方法常见的过度平滑和色偏问题。

**无配对真值数据集评估**（CroMo、HouseCat6D、SCRREAM、Cholec80、SCARED、StereoMIS-Tr）：使用 LSR（Light Suppression Ratio）和 NIQE 作为无参考评价指标。在 CroMo 数据集上，UnReflectAnything 取得 LSR 0.012、NIQE 0.061。值得注意的是，该方法在外科手术场景（Cholec80、SCARED、StereoMIS-Tr）上同样表现出色，证明了虚拟高光合成管道在跨域泛化方面的有效性——合成高光不依赖于特定场景的先验，使得模型能够适应从自然图像到医学内窥镜的广泛场景。

**下游任务评估**：**Table 3** 展示了高光去除对像素匹配任务的促进作用。以极线误差（E_ep，越低越好）和内点率（IR，越高越好）为指标，UnReflectAnything 处理后的图像在特征匹配质量上优于其他方法，表明该方法在去除高光的同时有效保留了底层几何纹理信息，对于 SfM、SLAM 等下游视觉任务具有实际价值。

**定性比较**：**Figure 6** 展示了多域高光去除的输入-输出对，覆盖自然场景、室内物体、外科手术等不同领域，UnReflectAnything 均能一致地去除或衰减镜面高光。**Figure 7** 与 PolarAnything/PolarFree 和 StableDelight 的定性对比显示，UnReflectAnything 在高光衰减的一致性和伪影抑制方面具有明显优势，尤其在跨域场景下表现更为稳定。

### 消融实验

**Table 4** 报告了在 PSD、SSHR、SHIQ 三个数据集上平均的消融实验结果，系统验证了各核心设计的作用。

**Token 空间修复 vs. RGB 空间修复**：将 token 空间修复模块替换为 RGB 空间修复，SSIM 从 0.957 骤降至 0.816，MSE_m 从 0.003 升至 0.007。这一显著退化表明，在冻结的 DINOv3 特征空间中进行修复能够利用预训练 ViT 的全局语义上下文，而 RGB 空间修复缺乏这种高层理解，难以恢复被高光遮挡的复杂纹理。

**局部均值先验**：移除局部均值先验后，SSIM 降至 0.911，MSE_m 升至 0.004。该先验通过聚合邻近可见 token 的信息为被遮盖 token 提供初始化，对大块高光区域的修复稳定性至关重要——缺乏该先验时，修复器难以从远距离上下文推断缺失的漫反射特征。

**解码器预训练**：取消解码器预训练（从头联合训练），SSIM 降至 0.873，MSE_m 升至 0.006。解码器预训练阶段通过自编码器重建损失（L1 + SSIM）使 DPT 解码器学会从冻结的 DINOv3 特征重建 RGB 图像，为后续的 token 修复训练提供了稳定的解码基础。

**数据集高光排除策略**：不对数据集原始高光区域进行监督排除，MSE_m 急剧升至 0.022。这一结果揭示了训练中的关键陷阱：数据集中的真实高光区域在合成高光图像对中表现为饱和像素，若将其纳入监督，网络会错误地将饱和反射当作漫反射外观进行学习，严重损害模型对真实高光的去除能力。

**几何估计精度**：用深度梯度法线代替 MoGe-2 估计的法线，MSE_m 升至 0.012，SSIM 降至 0.909。这表明虚拟高光合成的物理合理性高度依赖单目几何估计的精度——更准确的表面法线能够产生与场景结构一致的高光分布，从而提供更有效的训练监督。

### 失败模式分析

**Figure 8** 展示了 UnReflectAnything 的典型失败模式，主要包括以下几类：

1. **透明/折射物体**：模型对透明或折射物体上的高光处理能力有限，这类表面的反射特性超出了 Blinn-Phong 模型的描述范围，合成高光无法提供有效的训练信号。

2. **非高光区域的结构保持**：在部分非高光区域，输出图像的结构和分辨率保持可能不佳，token 修复器可能对未受高光影响的区域产生不必要的修改。

3. **低梯度平滑高光**：对于边界模糊、平滑衰减的高光区域，重建质量下降。基于亮度阈值的数据集高光检测方法可能无法准确标记这类区域，同时 token 修复器缺乏明确的修复边界引导。

4. **亮度误分类**：在医学内窥镜场景中，基于亮度阈值的方法可能将明亮的白色解剖结构（非镜面反射）错误分类为高光，导致不必要的修复，可能改变组织的真实外观。

### 训练配置

**Table 5** 列出了训练时各损失函数的权重配置。模型在单张 NVIDIA A100 GPU（80 GB）上训练，batch size 为 32，共训练 50 个 epoch。几何估计采用 MoGe-2 模型获取度量深度、表面法线和内参；Fresnel 反射系数 R₀ 设为 0.04；数据集高光检测的亮度阈值 τ_L 设为 0.95。Token 修复器采用 ViT 层序列，解码器预训练阶段使用 L1 和 SSIM 的组合重建损失。

### 补充图表

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/009_Table_3.jpg]]
*Table 3: Comparison of each method’s impact on pixel-matching, evaluated using the epipolar error*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/011_Table_4.jpg]]
*Table 4: Ablation study on supervision, model architecture, and training strategy. The reported*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison between UnReflectAnything, PolarAnything & PolarFree (PA+PF), and StableDelight. OURS provides more consistent and effective attenuation of specular highlights across domains, while avoiding noticeable artefacts*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative examples for pairs of raw images with highlights (left) and their UnReflectAnything-processed counterpart (right). Our framork consistently removes, inpaints or attenuates specular highlights from images in several different domains*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/012_Figure_8.jpg]]
*Figure 8: Representative failure modes of UnReflectAnything*

![[assets/figures/papers/paper_list_l2145_https_arxiv_org_abs_2512_09583/figures/013_Table_5.jpg]]
*Table 5: Loss function weights used at training time*



## 定位与知识库关联

**UnReflectAnything** 的核心贡献在于将单目几何估计驱动的物理渲染与冻结视觉Transformer特征空间中的token修复解耦，从而绕过了RGB高光去除任务中长期存在的配对数据瓶颈。其方法定位可以从数据范式、修复空间和特征利用三个维度进行谱系梳理。

### 1. 数据范式：从配对监督到合成伪配对

传统RGB高光去除方法依赖两类数据范式：一是基于物理模型的分离方法，通常需要多视角或多光照条件，在单目RGB设置下受限；二是基于学习的方法，如 **HighlightNet** 、**SpecularityNet** 、**MG-CycleGAN** 和 **DHAN-SHR**，它们或依赖配对的真实高光/无高光图像，或采用非配对GAN训练。配对数据在真实场景中极难获取，尤其在非朗伯体表面和复杂光照下（如外科手术场景），导致这些方法的泛化能力受限。

UnReflectAnything通过**虚拟高光合成管道**切断了这一依赖：它利用现成的单目几何估计方法（MoGe-2）从任意RGB图像恢复深度、法线和相机内参，进而在相机空间中随机采样点光源位置，通过Fresnel调制的Blinn-Phong着色模型渲染物理上合理的高光图，并与原图合成得到伪配对训练样本。这使得模型可以在任意RGB图像上训练，无需任何真实配对的无高光数据。

### 2. 修复空间：从RGB像素到DINOv3 patch token

另一条技术路线是在特征或图像空间中进行修复。**StableDelight** 等近期工作尝试了基于扩散模型的高光去除。UnReflectAnything的关键创新在于将修复操作从RGB像素空间提升到**DINOv3 patch token空间**。

消融实验直接验证了这一设计的因果效应：将token空间修复替换为RGB空间修复后，SSIM从0.957骤降至0.816，MSE_m从0.003升至0.007。这表明在语义丰富的冻结特征空间中操作，能够利用全局上下文进行更稳定的漫反射外观重建，而像素空间修复则容易产生纹理模糊和伪影。

### 3. 特征利用：冻结ViT与轻量化解码

在编码器选择上，UnReflectAnything采用**冻结的DINOv3-Large Vision Transformer**作为多尺度特征提取器，这与许多端到端训练CNN或ViT的方法形成对比。冻结编码器带来的优势有两方面：一是保留了预训练模型中的强语义先验，有助于高光区域的定位与修复；二是大幅降低了可训练参数量，使得整个框架在单张A100 GPU上即可完成训练。

解码器部分采用DPT架构，并引入了**解码器预训练**策略——先以自编码器方式重建输入RGB图像（最小化L1+SSIM损失），再联合训练高光预测和token修复模块。消融实验表明，取消解码器预训练会导致SSIM从0.957降至0.873，MSE_m升至0.006，验证了分阶段训练对稳定收敛的必要性。

### 4. 监督策略：排除数据集高光的token级监督

UnReflectAnything的监督策略也值得关注：模型在token修复阶段**显式排除了数据集原有高光区域的监督**，仅对合成高光覆盖的可靠patch计算修复损失（L1与余弦相似度）。这一设计的逻辑在于，数据集中的真实高光区域缺乏漫反射真值，若将其纳入监督会误导网络将饱和反射当作漫反射——消融实验中取消该排除策略后，MSE_m飙升至0.022。

同时，token修复器被要求**对所有高光区域进行修复**（包括合成高光和数据集原有高光），但仅在前者上接受监督。这种“全修复、部分监督”的策略使得模型能够泛化到真实高光，同时避免被噪声标签污染。

### 5. 适用边界与局限

尽管UnReflectAnything在多个基准上展示了跨域泛化能力，其方法存在明确的适用边界：

- **几何估计依赖性**：虚拟高光合成的质量高度依赖单目几何估计的精度。消融实验显示，用深度梯度法线替代MoGe-2法线会使MSE_m从0.003升至0.012，SSIM降至0.909。当单目几何估计在透明物体、细薄结构或极端视角下失效时，合成的高光将不再物理合理，进而污染训练信号。

- **透明与折射物体**：模型对透明或折射物体上的高光处理能力有限，这是Blinn-Phong反射模型的内在局限——该模型仅建模表面反射，无法处理次表面散射和折射。

- **低梯度高光区域**：对于边界模糊、平滑衰减的高光区域，重建质量下降。这可能与高光预测器产生的软性概率图在低对比度区域不够精确有关。

- **亮度阈值误分类**：基于亮度阈值检测数据集高光的方法可能将明亮但非镜面反射的表面（如内窥镜图像中的白色解剖结构）错误标记为高光，导致不必要的修复。

- **非高光区域保真度**：在非高光区域，输出图像的结构和分辨率保持可能不佳，这暗示token修复器的感受野可能在不必要时修改了正常区域的特征。

### 6. 开放问题

- **时序扩展**：当前方法仅处理单帧图像。能否将虚拟高光合成与token修复扩展到视频序列，利用时序一致性进一步稳定高光去除，是一个自然且具有实际价值的方向。

- **几何线索替代**：在无需单目深度估计（如使用其他几何线索或自监督几何学习）的情况下，模型是否仍然有效？这直接关系到方法在计算资源受限场景下的部署可行性。

- **反射类型泛化**：该方法能否泛化到其他类型的反射，如环境反射或次表面散射？当前的Blinn-Phong渲染管道仅建模点光源的直接镜面反射，扩展渲染模型可能是解决这一问题的关键。



## 原文 PDF

![[paperPDFs/CVPR_2026/UnReflectAnything_RGB_Only_Highlight_Removal_by_Rendering_Synthetic_Specular_Supervision.pdf]]
