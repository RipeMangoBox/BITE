---
title: "SurfSplat: Conquering Feedforward 2D Gaussian Splatting with Surface Continuity Priors"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SurfSplat_Conquering_Feedforward_2D_Gaussian_Splatting_with_Surface_Continuity_P_7f838b1d2532.pdf
project_link: "https://hebing-sjtu.github.io/SurfSplat-website/"
code_link: null
aliases:
- SurfSplat
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 显式引入表面连续性先验，强制每个2D高斯原语的旋转和尺度与其空间邻域对齐；同时采用强制alpha混合策略，限制不透明度上限并归一化输出，保证深度方向梯度有效传播。
primary_logic: 真实场景的可见几何主要由平滑表面构成，图像空间中相邻像素对应的3D点可以推导出局部表面朝向和尺度，从而为2D高斯提供几何连贯的初始化；进一步限制透明度可防止模型陷入局部最优，使所有高斯在渲染中保持贡献，实现连续且无偏的表面重建。
claims:
- 移除表面连续性先验和强制alpha混合后，高分辨率渲染一致性（HRRC）大幅下降，1024×1024下PSNR从24.535降至18.563（w/o FAB,SCP）和17.576（w/o FAB）。
- 定性消融（Figure 5）显示，完整模型生成连续、连贯的表面，而消融变体出现明显的空洞、断裂和空间不一致。
- RealEstate10K 上 PSNR (标准256×256) = 27.537 (SurfSplat-Ours-L)
- RealEstate10K 上 PSNR (1024×1024 HRRC) = 24.897 (SurfSplat-Ours-L)
---

# SurfSplat: Conquering Feedforward 2D Gaussian Splatting with Surface Continuity Priors

> [!tip] 核心洞察
> 真实场景的可见几何主要由平滑表面构成，图像空间中相邻像素对应的3D点可以推导出局部表面朝向和尺度，从而为2D高斯提供几何连贯的初始化；进一步限制透明度可防止模型陷入局部最优，使所有高斯在渲染中保持贡献，实现连续且无偏的表面重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | SurfSplat：以表面连续性先验征服前馈式2D高斯溅射 |
| 英文题名 | SurfSplat: Conquering Feedforward 2D Gaussian Splatting with Surface Continuity Priors |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=o1sF4XaFdY) · [Project](https://hebing-sjtu.github.io/SurfSplat-website/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SurfSplat |
| Dataset | RealEstate10K, ACID |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR (标准256×256) 27.537 (SurfSplat-Ours-L) vs 27.504 (DepthSplat) (+0.033)；PSNR (1024×1024 HRRC) 24.897 (SurfSplat-Ours-L) vs 16.385 (DepthSplat) (+8.512)。
> - ACID 上，PSNR (标准256×256) 28.336 (SurfSplat-Ours) vs 28.202 (MVSplat) (+0.134)。

## 概要

**核心问题**：前馈式三维高斯溅射（3DGS）方法在稀疏视图输入下，逐像素独立预测高斯原语，缺乏对场景几何结构的显式利用。仅依赖图像重建损失难以解耦几何与外观，导致生成的场景表面不连续、存在空洞和颜色偏差，在近距离或离轴视角下尤为严重。

**方法定位**：SurfSplat 是一种基于二维高斯溅射（2DGS）原语的前馈式框架，核心创新在于引入**表面连续性先验**与**强制 Alpha 混合**两项机制。表面连续性先验利用图像空间相邻像素推导局部表面朝向与各向异性尺度，强制每个 2D 高斯的旋转和尺度与其空间邻域对齐；强制 Alpha 混合通过裁剪不透明度上限并归一化输出，防止高斯过早饱和，确保所有深度层的高斯在训练中保持贡献，从而实现连续且无偏的表面重建。

**主要结果**：在标准分辨率（256×256）下，SurfSplat 在 RealEstate10K 和 ACID 数据集上与最优方法持平（PSNR 27.537 vs. DepthSplat 27.504）；在提出的高分辨率渲染一致性（HRRC）指标上，1024×1024 分辨率下 PSNR 领先 DepthSplat 达 8.512 dB（24.897 vs. 16.385），暴露并解决了先前方法在高分辨率下的几何稀疏问题。消融实验证实，同时移除表面连续性先验和强制 Alpha 混合后，HRRC 的 PSNR 从 24.535 骤降至 18.563，定性结果出现明显空洞与空间不一致。跨数据集泛化实验（ScanNet、DL3DV、DTU）进一步验证了方法的鲁棒性。

**方法谱系与知识库定位**：SurfSplat 延续了前馈式高斯溅射的研究脉络，与 **PixelSplat**（Charatan et al., 2024）、**MVSplat**（Chen et al., 2024b）、**TranSplat**（Zhang et al., 2025）、**HiSplat**（Tang et al., 2024）和 **DepthSplat**（Xu et al., 2024b）等方法构成直接比较。区别于上述方法使用 3D 高斯椭球体且由网络直接预测旋转与尺度，SurfSplat 转而采用 2D 高斯面元，并通过几何推导获得旋转与各向异性尺度，从表示层面引入表面连续性归纳偏置。在编码器设计上，SurfSplat 与 DepthSplat 共享相同的双路骨干网络（单目分支使用 Depth Anything V2 的 ViT，多视图分支使用轻量 ResNet 与 Swin Transformer 构建代价体），保证了对比的公平性——标准分辨率下指标相当，而高分辨率下优势显著，说明性能提升源于所提出的表面连续性先验与强制 Alpha 混合，而非编码器或训练技巧的差异。

### 问题背景：前馈式新视角合成中的几何-外观解耦困境

从稀疏输入图像中重建三维场景并实现逼真的新视角合成（Novel View Synthesis, NVS）是计算机视觉与图形学的核心任务之一。近年来，基于前馈式高斯溅射（Feedforward Gaussian Splatting）的方法因其高效的推理速度和可泛化的场景表示能力而受到广泛关注。这类方法通过一个可学习的映射 $f_{\theta}$，将稀疏的输入图像及对应的相机参数直接映射为每个像素的高斯原语属性：

$$f _ { \theta } : \{ ( I ^ { v } , \mathbf { k } ^ { v } , \mathbf { T } ^ { v } ) \} _ { v = 1 } ^ { V } \mapsto \left\{ \bigcup _ { j = 1 } ^ { H \times W } \left( \mu _ { j } ^ { v } , \alpha _ { j } ^ { v } , \mathbf { r } _ { j } ^ { v } , \mathbf { s } _ { j } ^ { v } , \mathbf { c } _ { j } ^ { v } \right) \right\} _ { v = 1 } ^ { V }$$

然而，现有前馈方法面临一个根本性的困境：**在仅有图像重建损失监督、且输入视图稀疏的条件下，模型难以有效解耦场景的几何结构与外观纹理**。具体而言，网络预测的高斯原语彼此独立，缺乏对场景中各项异性几何结构的显式利用。这导致生成的场景表面呈现出严重的空间不连续性——表现为点云稀疏、存在空洞，并伴随颜色偏差。这些问题在近距离视角或离轴观察时尤为突出，严重制约了渲染质量的上限。

### 现有方法的缺口

当前主流的前馈式高斯溅射方法可大致分为两类：**多高斯/像素方法**与**单高斯/像素方法**。前者如 **PixelSplat**（Charatan et al., 2024）和 **HiSplat**（Tang et al., 2024），为每个像素预测多个高斯原语，虽然能覆盖更多空间区域，但引入了表示冗余且缺乏几何约束；后者如 **MVSplat**（Chen et al., 2024b）、**TranSplat**（Zhang et al., 2025）和 **DepthSplat**（Xu et al., 2024b），采用单高斯/像素的紧凑假设，通过代价体（cost volume）等立体匹配机制获取深度信息，但所预测的高斯原语仍缺乏对局部表面连续性的显式建模。

这些方法的共同缺陷在于：**高斯的旋转和尺度完全由网络自由预测，未利用真实场景中普遍存在的表面平滑先验**。在标准分辨率（如 $256 \times 256$）下，图像损失能够一定程度上掩盖几何缺陷；但当渲染分辨率提升时，底层表示的稀疏性和不连续性便会暴露无遗——表现为渲染图像中的黑色空洞区域和深度图中的异常跳变（如 Figure 4 所示）。

### 本文动机与核心思路

真实场景的可见几何主要由平滑表面构成，这意味着图像空间中相邻像素对应的三维点应当位于连续、连贯的局部表面上。基于这一观察，SurfSplat 提出了一种全新的前馈框架，其核心动机在于：**将表面连续性作为一种显式先验注入前馈高斯溅射过程，从根本上解决几何-外观解耦难题**。

为实现这一目标，SurfSplat 进行了两个关键设计：

1. **表面连续性先验（Surface Continuity Prior）**：利用图像空间邻域关系推导局部表面几何，据此显式计算每个 2D 高斯的旋转和各向异性尺度，而非由网络自由预测。具体而言，通过 Sobel 滤波获取邻域切向量 $\mathbf{t}_1, \mathbf{t}_2$，进而估计局部表面法向 $\mathbf{n} = \frac{\mathbf{t}_1 \times \mathbf{t}_2}{\lVert \mathbf{t}_1 \times \mathbf{t}_2 \rVert}$，并利用 Rodrigues 旋转公式将规范法向对齐到估计法向，从而确保所有高斯原语在三维空间中形成连贯的表面。

2. **强制 Alpha 混合（Forced Alpha Blending）**：对预测的不透明度进行上界裁剪（$\tau_{\text{opa}} < 1$），并在累积不透明度超过阈值 $\tau_{\alpha}$ 时对渲染输出进行归一化补偿。这一策略防止模型陷入“完全不透明高斯”的局部最优，确保所有深度层的高斯均参与梯度传播和训练，从而维持多视图间的空间对齐。

通过将 2D 高斯面元（2D Gaussian Surfels, 2DGS）作为场景表示基元，并联合上述两项创新，SurfSplat 能够在稀疏输入条件下重建出几何连续、纹理逼真的三维表面，尤其在高分辨率渲染场景下展现出显著优势。

## 核心方法与创新机理

SurfSplat 的核心创新在于通过两个相互协同的机制，系统性解决了前馈式高斯溅射方法中“高斯原语彼此独立、无法利用各向异性结构”的根本瓶颈。这两个机制分别从**几何初始化**和**梯度传播**两个维度切入，共同实现了连续、无偏的表面重建。

### 瓶颈分析：独立预测的失效模式

前馈式 3DGS 方法（如 **PixelSplat** (Charatan et al., 2024)、**MVSplat** (Chen et al., 2024b)）的核心范式是将每张输入图像的每个像素映射为一个独立的高斯原语。这一设计在仅有图像损失的稀疏视角输入下存在本质缺陷：网络直接预测每个高斯的旋转和尺度，缺乏对局部表面几何结构的显式约束，导致几何与外观的耦合难以解耦。具体表现为：

- **表面不连续**：相邻高斯之间缺乏空间一致性，渲染表面出现空洞和断裂（见 Figure 5 消融对比）。
- **颜色偏差**：不透明度过早饱和，导致被遮挡的高斯在训练中梯度消失，模型陷入局部最优，产生偏色伪影。
- **分辨率敏感性**：在标准 256×256 分辨率下，这些缺陷被像素平均效应掩盖；但在高分辨率渲染时，空洞和几何稀疏性暴露为黑色像素块（见 Figure 4），PSNR 急剧下降——例如 DepthSplat 在 1024×1024 下的 HRRC PSNR 仅 16.385 dB，而 256×256 下为 27.504 dB（Table 1）。

### Changed Slot 1：从独立预测到表面连续性先验

SurfSplat 将高斯原语从 3D 椭球体替换为 **2D Gaussian surfels (2DGS)**，并从根本上改变了旋转和尺度的获取方式：不再由网络直接回归，而是从局部表面几何中**推导**得出。

**因果机制**：真实场景的可见几何主要由平滑表面构成。图像空间中相邻像素对应的 3D 点能够推导出局部表面朝向和尺度。SurfSplat 利用这一先验，在 3×3 图像邻域内应用 Sobel 滤波获取两个切向量：

$$\mathbf{t}_1, \mathbf{t}_2 = \mathbf{p}_1 - \mathbf{p}_0, \quad \mathbf{p}_2 - \mathbf{p}_0$$

其中 $\mathbf{p}_0$ 为中心像素的 3D 位置，$\mathbf{p}_1$ 和 $\mathbf{p}_2$ 分别为右向和下向 Sobel 邻域点。局部表面法向由切向量叉乘归一化得到：

$$\mathbf{n} = \frac{\mathbf{t}_1 \times \mathbf{t}_2}{\lVert \mathbf{t}_1 \times \mathbf{t}_2 \rVert}$$

随后通过 Rodrigues 旋转公式，将规范法向 $\mathbf{n}_0 = (0, 0, 1)^\top$ 对齐到估计法向 $\mathbf{n}$，得到 2D 高斯的旋转矩阵 $\mathbf{R}$：

$$\mathbf{R} = \mathbf{I} + [\mathbf{v}]_\times + \frac{1 - c}{\|\mathbf{v}\|^2} [\mathbf{v}]_\times^2$$

其中 $\mathbf{v} = \mathbf{n}_0 \times \mathbf{n}$，$c = \mathbf{n}_0^\top \mathbf{n}$。各向异性尺度则由图像空间邻域距离给出粗估计，再通过网络预测的乘子（约束在 $[1/3, 3]$ 内）进行精化。深度方向尺度固定为零，以保持 2D 溅射特性。

**效果**：这一设计强制相邻高斯在空间中对齐到同一局部表面上，从根本上消除了独立预测带来的几何不连续性。

### Changed Slot 2：从标准 Alpha 混合到强制 Alpha 混合

即使有了表面连续性先验，标准 alpha 混合仍会导致模型退化：当某些高斯的不透明度趋近于 1 时，其后的高斯在渲染中贡献趋近于零，梯度无法有效传播，模型倾向于生成完全不透明的高斯来拟合训练视图，但在新视角下出现空间失配。

**因果机制**：SurfSplat 引入两个关键约束：

1. **不透明度裁剪**：将预测的不透明度 $\alpha$ 限制在上界 $\tau_{\text{opa}} < 1$（实验取 $\tau_{\text{opa}} = 0.6$），防止任何高斯完全遮挡后续高斯。
2. **输出归一化**：当累积不透明度 $\bar{\alpha}$ 超过阈值 $\tau_\alpha$ 时，对渲染颜色进行补偿：

$$C = \begin{cases} C, & \bar{\alpha} < \tau_\alpha, \\ \frac{C}{\bar{\alpha}}, & \bar{\alpha} \geq \tau_\alpha. \end{cases}$$

这确保了所有深度层的高斯在训练中保持梯度贡献，避免模型陷入局部最优。

### 协同效应与证据强度

两个 changed slot 具有强协同性：表面连续性先验提供几何连贯的初始化，而强制 alpha 混合保证梯度能有效传播以优化这一初始化。消融实验提供了决定性证据（Table 4）：

- 完整模型在 1024×1024 HRRC 下 PSNR 为 24.535 dB。
- 同时移除强制 alpha 混合和表面连续性先验（w/o FAB, SCP）后，PSNR 骤降至 18.563 dB（下降 5.97 dB）。
- 仅使用表面连续性先验而关闭强制 alpha 混合时，模型生成完全不透明的高斯，导致多视图空间对齐失败。

定性消融（Figure 5）进一步证实：完整模型生成连续、连贯的表面，而消融变体出现明显的空洞、断裂和空间不一致。

### 与 Baseline 的公平性说明

SurfSplat 采用与 **DepthSplat** (Xu et al., 2024b) 相同的编码器骨干和训练设置。在标准 256×256 分辨率下，SurfSplat-L 的 PSNR 为 27.537 dB，与 DepthSplat 的 27.504 dB 基本持平（Table 1）；但在 1024×1024 HRRC 下，SurfSplat-L 达到 24.897 dB，领先 DepthSplat 8.512 dB。这一对比表明，性能增益完全来源于提出的表面连续性先验和强制 alpha 混合，而非编码器容量或训练技巧的差异。

SurfSplat 是一个前馈式 2D 高斯溅射框架，其核心目标是从稀疏输入视图直接预测连续、几何一致的 3D 场景表示。图 2 给出了模型的整体架构。系统接收 $V$ 张已知相机内外参的输入图像，经双路编码器提取特征后，由 2D U-Net 回归中间属性，最终通过高斯处理器将中间属性转化为标准的 2D 高斯原语参数，用于可微分渲染。

### 输入输出映射

框架的形式化定义如公式 (1) 所示：前馈网络 $f_{\theta}$ 将 $V$ 张输入图像 $\{I^v\}$ 及其对应的相机内参 $\{\mathbf{k}^v\}$ 和外参 $\{\mathbf{T}^v\}$ 映射为每像素的高斯属性集合——包括位置 $\mu$、不透明度 $\alpha$、旋转 $\mathbf{r}$、尺度 $\mathbf{s}$ 和球谐系数 $\mathbf{c}$。每个输入视图的每个像素对应一个 2D 高斯原语，输出维度为 $H \times W$ 个高斯。

### 双路编码器

编码器由单视图分支和多视图分支构成，二者并行处理输入图像。

**单视图分支**利用预训练的 Depth Anything V2 模型的 ViT 骨干提取单目特征，经双线性上采样后与多视图特征融合。该分支为纹理缺失等区域提供先验信息，弥补纯多视图匹配的不足。

**多视图分支**首先通过轻量级 ResNet-style 骨干提取图像特征，随后采用 Swin Transformer 进行 6 层自注意力和交叉注意力处理，增强特征的表征能力。处理后的特征通过平面扫描立体方法构建跨视图代价体，为后续深度估计提供多视图几何约束。

两路特征经拼接后送入 2D U-Net，回归深度候选、尺度乘子、高阶球谐分量和不透明度等中间属性。

### 高斯处理器

高斯处理器是 SurfSplat 的核心创新模块，负责将 U-Net 输出的中间属性转化为标准 2D 高斯参数。如图 3 所示，该模块包含两个关键设计：

1. **表面连续性先验**：利用预测深度和图像空间的 3×3 邻域关系，通过 Sobel 滤波计算局部切向量，进而估计表面法向，再通过 Rodrigues 旋转公式推导每个高斯的旋转矩阵。尺度则通过投影邻域点在旋转切向轴上的方差估计，并由网络预测的乘子进行细化。这一过程强制相邻高斯的旋转和尺度与局部表面几何对齐，确保重建表面的连续性。

2. **强制 Alpha 混合**：对预测的不透明度进行上界裁剪（$\tau_{\text{opa}} < 1$），防止高斯过早饱和；当累积不透明度超过阈值 $\tau_{\alpha}$ 时，对渲染输出颜色进行归一化补偿。该策略确保深度方向上所有高斯均参与训练，避免模型陷入局部最优。

### 训练与推理流程

训练时，模型通过可微分渲染器将预测的高斯原语渲染为新视角图像，与真值图像计算损失并反向传播。推理时，给定稀疏输入视图，模型一次前馈即可输出完整的场景表示，无需逐场景优化。

> 注：本文未提供代码链接，上述架构描述基于论文文本与图 2、图 3 的说明。部分实现细节（如 U-Net 的具体层数、特征维度）需查阅原文或代码以确认。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/002_Figure_2.jpg]]
*Figure 2: Illustration for model architecture. Given sparse input images, our dual-path encoder processes them through both single-view and multi-view branches. The fused features are passed through a U-Net to predict intermediate attributes, including depth, scale multipliers, and appearance components. Finally, these intermediates are converted into standard Gaussian attributes using our surface continuity prior and forced alpha blending strategy*

### 前馈高斯预测框架

SurfSplat 将稀疏多视图重建形式化为一个前馈映射问题。给定 $V$ 张输入图像及其对应的相机内参 $\mathbf{k}^v$ 和位姿 $\mathbf{T}^v$，网络 $f_\theta$ 直接预测每个像素对应的高斯原语属性：

$$f _ { \theta } : \{ ( I ^ { v } , \mathbf { k } ^ { v } , \mathbf { T } ^ { v } ) \} _ { v = 1 } ^ { V } \mapsto \left\{ \bigcup _ { j = 1 } ^ { H \times W } \left( \mu _ { j } ^ { v } , \alpha _ { j } ^ { v } , \mathbf { r } _ { j } ^ { v } , \mathbf { s } _ { j } ^ { v } , \mathbf { c } _ { j } ^ { v } \right) \right\} _ { v = 1 } ^ { V }$$

其中 $\mu$ 为3D位置，$\alpha$ 为不透明度，$\mathbf{r}$ 为旋转，$\mathbf{s}$ 为各向异性尺度，$\mathbf{c}$ 为球谐系数。与先前方法的关键区别在于，SurfSplat 采用 **2D高斯surfels**（而非3D椭球）作为场景表示基元，并通过后续模块显式注入几何先验。

### 双路编码器架构

模型采用双路特征提取架构（Figure 2），分别捕获单目先验与多视图几何信息：

- **单视图分支**：利用预训练的 **Depth Anything V2**（Yang et al., 2024）的 ViT 骨干网络提取单目特征，经双线性上采样后为纹理缺失等区域提供先验信息。
- **多视图分支**：以轻量 ResNet 风格骨干网络和 **Swin Transformer**（含6层自注意力与交叉注意力）提取多视图特征，随后通过平面扫描立体方法（Collins, 1996; Xu et al., 2023）构建跨视图代价体。

两路特征拼接后送入 **2D U-Net**（Ronneberger et al., 2015），回归深度候选、尺度乘子、高阶球谐分量和不透明度等中间属性。这些中间属性随后经高斯处理器转化为标准高斯参数。

### 表面连续性先验

这是 SurfSplat 的核心创新模块（Figure 3）。其基本洞察是：真实场景的可见几何主要由平滑表面构成，图像空间中相邻像素对应的3D点可推导出局部表面朝向和尺度，从而为2D高斯提供几何连贯的初始化。

**旋转估计**：在图像空间的 $3\times3$ 邻域内，利用右向和下向 Sobel 滤波得到两个切向量：

$$\mathbf { t } _ { 1 } , \mathbf { t } _ { 2 } = \mathbf { p } _ { 1 } - \mathbf { p } _ { 0 } , \quad \mathbf { p } _ { 2 } - \mathbf { p } _ { 0 }$$

其中 $\mathbf{p}_0$ 为中心像素对应的3D点，$\mathbf{p}_1$、$\mathbf{p}_2$ 分别为右邻和下邻像素的3D点。局部表面法向由切向量叉乘归一化得到：

$$\mathbf { n } = { \frac { \mathbf { t } _ { 1 } \times \mathbf { t } _ { 2 } } { \lVert \mathbf { t } _ { 1 } \times \mathbf { t } _ { 2 } \rVert } }$$

随后通过 **Rodrigues 旋转公式**，将规范法向 $\mathbf{n}_0 = (0,0,1)^\top$ 对齐到估计法向 $\mathbf{n}$，得到2D高斯的旋转矩阵 $\mathbf{R}$：

$$\mathbf { R } = \mathbf { I } + [ \mathbf { v } ] _ { \times } + \frac { 1 - c } { \| \mathbf { v } \| ^ { 2 } } [ \mathbf { v } ] _ { \times } ^ { 2 }$$

其中 $\mathbf{v} = \mathbf{n}_0 \times \mathbf{n}$，$c = \mathbf{n}_0^\top \mathbf{n}$，$[\mathbf{v}]_\times$ 为 $\mathbf{v}$ 的反对称矩阵。

**尺度估计**：各向异性尺度 $\mathbf{S} = \operatorname{diag}(\sigma_u, \sigma_v, \sigma_w)$ 通过投影邻域点在旋转切轴上的方差计算。由于采用2D高斯splats，深度轴尺度固定为零（$\sigma_w = 0$）。粗尺度由图像空间邻域像素间距估计：

$$\bar{\sigma}_u^2 = t_{1x}^2 + t_{1z}^2, \quad \bar{\sigma}_v^2 = t_{2y}^2 + t_{2z}^2$$

网络额外预测尺度乘子 $\hat{\sigma}_u$、$\hat{\sigma}_v$（约束在 $[1/3, 3]$ 范围内），最终尺度为 $\sigma_u = \bar{\sigma}_u \hat{\sigma}_u$，$\sigma_v = \bar{\sigma}_v \hat{\sigma}_v$。3D协方差矩阵由 $\Sigma = \mathbf{R} \mathbf{S} \mathbf{S}^{\top} \mathbf{R}^{\top}$ 给出，投影到屏幕空间的2D协方差为 $\Sigma' = \mathbf{J} \mathbf{W} \Sigma \mathbf{W}^{\top} \mathbf{J}^{\top}$，其中 $\mathbf{W}$ 为观测变换，$\mathbf{J}$ 为投影雅可比。

### 强制Alpha混合

标准 alpha 合成公式为：

$$C = \sum _ { i \in \cal N } c _ { i } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) , \quad \alpha = \sum _ { i \in \cal N } \alpha _ { i } \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

其中 $c_i$ 为第 $i$ 个高斯的颜色，$\alpha_i$ 为其不透明度，累积不透明度 $\alpha$ 通过逐层透射率计算。

强制alpha混合对此进行两项关键修改：

1. **不透明度裁剪**：将预测的不透明度用上界 $\tau_{\text{opa}} < 1$（实验设为0.6）裁剪，防止高斯过早饱和导致深度方向的梯度消失。
2. **输出归一化**：当累积不透明度达到阈值 $\tau_\alpha$ 时，对渲染颜色进行补偿归一化：

$$C = \left\{ { \begin{array} { l l } { C , } & { \alpha < \tau _ { \alpha } , } \\ { \frac{C}{\overline{\alpha}} , } & { \alpha \geq \tau _ { \alpha } , } \end{array} } \right.$$

该策略确保所有深度层的高斯均参与训练并保持梯度贡献，使模型在优化过程中不会陷入局部最优，从而实现连续且无偏的表面重建。消融实验（Table 4）表明，同时移除表面连续性先验和强制alpha混合后，1024×1024 HRRC PSNR 从 24.535 降至 18.563（w/o FAB,SCP），验证了二者协同的必要性。

## 实验与关键发现

SurfSplat的实验设计围绕一个核心主张展开：**表面连续性先验与强制alpha混合**是解决前馈式高斯溅射中几何-外观解耦困难的关键。评估体系在标准新视角合成指标之外，引入了**高分辨率渲染一致性（HRRC）**指标，以显式暴露低分辨率下被掩盖的几何缺陷。

### 实验设置

**数据集与评估协议。** 训练主要在**RealEstate10K**和**ACID**两个大规模室内外场景数据集上进行，以标准的两视图新视角合成任务为基准。评估指标包括PSNR、SSIM和LPIPS，分别在标准分辨率（256×256）、2×上采样（512×512）和4×上采样（1024×1024）三个层级报告，其中4×上采样即为HRRC指标。跨数据集泛化能力在**ScanNet**、**DL3DV**和**DTU**上评估，无需微调。

**HRRC指标设计。** 传统低分辨率评估无法有效暴露场景表示中的空洞和几何稀疏问题——随着渲染分辨率提高，这些缺陷会以黑色像素或深度异常的形式显现（见图4）。HRRC指标定义为：
$$\mathrm { H R R C } _ { \mathrm { m e t r i c } } = \mathrm { m e t r i c } ( \hat { I } ^ { H R } , \hat { I } ^ { G T \Uparrow } ) \quad \mathrm { w h e r e ~ m e t r i c \in \{ P S N R , S S I M , L P I P S \} }$$
即将高分辨率渲染图像与双三次上采样的真值进行比较，从而量化几何不连续导致的渲染伪影。

**训练配置。** SurfSplat提供基础版（Ours-B）和大型版（Ours-L）两个变体，均训练600K迭代，batch size为8。预训练的Depth Anything V2骨干网络使用较低学习率（$2 \times 10^{-6}$），其余部分采用标准学习率。该设置与主要基线方法**DepthSplat**（Xu et al., 2024b）保持一致，确保了对比的公平性——两者共享相同的编码器骨干和训练协议，差异仅来自SurfSplat引入的2D高斯原语、表面连续性先验和强制alpha混合策略。

### 主实验结果

**RealEstate10K基准。** 如表1所示，在标准256×256分辨率下，SurfSplat-L以27.537 dB的PSNR略优于DepthSplat的27.504 dB（+0.033 dB），处于同一水平线。然而，**分辨率越高，优势越显著**：在512×512下，SurfSplat-L达到26.331 dB，领先DepthSplat达9.595 dB；在1024×1024 HRRC下，SurfSplat-L的24.897 dB更是大幅超越DepthSplat的16.385 dB（+8.512 dB）。这一趋势在所有单高斯/像素方法组（MVSplat、TranSplat、DepthSplat）中一致成立，验证了表面连续性先验在高分辨率下对几何质量的根本性改善，而非编码器能力差异所致。

**ACID基准。** 在ACID数据集上（表2），SurfSplat同样展现出分辨率依赖的性能优势：256×256下PSNR为28.336 dB（vs. MVSplat的28.202 dB），512×512下为26.868 dB，1024×1024 HRRC下为21.253 dB。值得注意的是，多高斯/像素方法（如pixelSplat）在ACID上的HRRC退化更为严重，从侧面印证了每个像素预测一个高斯的策略在几何一致性上的优势。

**跨数据集泛化。** 表3展示了SurfSplat在未见数据集上的零样本泛化能力。在ScanNet室内场景和DL3DV高分辨率数据上，SurfSplat均保持领先。特别地，在原生高分辨率的DL3DV数据集上（表5），SurfSplat以24.411 dB优于pixelSplat的24.082 dB，与HRRC指标的排序一致，验证了HRRC作为几何质量代理指标的可靠性。

### 消融研究

消融实验（表4）系统拆解了SurfSplat两大核心组件的贡献：

**表面连续性先验（SCP）与强制alpha混合（FAB）的协同效应。** 同时移除SCP和FAB后，1024×1024 HRRC下的PSNR从完整模型的24.535 dB骤降至18.563 dB（降幅5.97 dB），标准256×256分辨率下也从27.292 dB降至26.231 dB。仅移除FAB而保留SCP时，模型倾向于生成完全不透明的高斯原语，导致多视图间空间对齐失败——尽管表面几何在局部看似连续，但深度方向的梯度传播受阻，模型陷入局部最优。仅移除SCP而保留FAB时，高斯原语失去几何约束，表面出现明显断裂和空洞（见图5定性对比）。

**强制alpha混合的机制性作用。** 强制alpha混合通过两个超参数控制：不透明度上限$\tau_{opa}=0.6$和归一化阈值$\tau_\alpha$。该策略的核心在于**防止高斯过早饱和**——当某层高斯的不透明度趋近于1时，其后的高斯对渲染结果的贡献趋于零，梯度无法有效回传，导致深度方向的信息坍塌。通过对预测不透明度进行裁剪（$\tau_{opa} < 1$），并在累积不透明度超过阈值时对输出颜色进行归一化（$C = C / \bar{\alpha}$），强制所有深度层的高斯均保持非零贡献，保证了训练的稳定性和最终表面的连续性。

**超参数敏感性。** 表6显示，方法对$\tau_\alpha$和$\tau_{opa}$的选择具有一定鲁棒性，但极端取值（如$\tau_{opa}$接近1或$\tau_\alpha$过小）会导致性能退化，验证了适度约束的必要性。

### 高分辨率模型扩展

SurfSplat进一步训练了高分辨率版本（256×448输入，表7），在多个渲染分辨率下均保持连贯的几何和外观（图7-9）。随着分辨率提高，模型能够揭示场景的精细细节，而不会像基线方法那样出现空洞放大或颜色偏差加剧的问题。这进一步印证了表面连续性先验的尺度适应性——由图像空间邻域推导的局部几何约束在不同分辨率下均能提供有效的正则化。

### 失败模式与局限性

尽管SurfSplat在几何连续性上取得了显著突破，但仍存在以下局限：

1. **相机位姿依赖。** 方法假设已知精确的相机内参和外参作为输入，无法直接应用于无位姿条件下的场景重建。这是当前前馈式方法共有的约束，源于代价体构建和跨视图特征融合对极线几何的依赖。
2. **表示冗余。** 当前设计为每个输入像素预测一个独立高斯原语，导致场景表示缺乏自适应紧凑性。在覆盖大面积均匀纹理区域（如墙壁、天空）时，大量高斯原语存在信息冗余，限制了在大规模场景中的存储和渲染效率。
3. **几何先验的边界效应。** 表面连续性先验基于图像空间3×3邻域的Sobel滤波推导局部切向量，在深度不连续区域（如物体边界）可能引入错误的法向估计，导致边缘处的几何模糊。这一问题在定性结果中表现为物体轮廓附近的轻微表面扭曲，但定量影响有限。

### 开放性讨论

SurfSplat的贡献揭示了一个更深层的问题：**前馈式重建中，几何先验的显式注入比网络容量的增加更为关键。** 在编码器骨干和训练设置完全相同的情况下，仅通过改变高斯原语类型（3D→2D）和引入表面连续性约束，就在高分辨率下获得了8.5 dB以上的提升。这暗示未来工作的方向可能不在于更大的模型，而在于更精巧的几何归纳偏置设计——例如，如何将表面连续性先验扩展到时序维度以实现4D重建，或如何消除对已知位姿的依赖以实现真正的单目前馈重建。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/008_Table_4.jpg]]
*Table 4: Ablations study on various components*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/009_Figure_5.jpg]]
*Figure 5: Ablation study: Visualization of reconstructed 3D scenes. Our full model yields continuous and coherent surfaces, while ablated variants exhibit visible artifacts and spatial inconsistencies*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/010_Figure_6.jpg]]
*Figure 6: Normal and mesh comparison with DepthSplat*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/011_Table_5.jpg]]
*Table 5: Quantitative performance comparison on high-resolution DL3DV dataset*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_o1sF4XaFdY/figures/012_Table_6.jpg]]
*Table 6: Ablations study on hyperparameter sensitivity*

## 定位与知识库关联

### 与前馈式高斯溅射方法的关系

SurfSplat 属于前馈式新视角合成（feedforward novel view synthesis）方法族，其核心设定是从稀疏输入图像直接回归场景的显式表示，无需逐场景优化。该族方法可依据高斯原语类型和预测策略分为以下几个关键分支：

**3DGS 基线（多高斯/像素）**：**PixelSplat**（Charatan et al., 2024）为每个像素预测多个 3D 高斯椭球，通过极线采样和交叉注意力进行多视图交互。该方法在表达灵活性上具有优势，但因多个高斯之间缺乏几何约束，生成的场景往往稀疏且存在空洞。

**3DGS 基线（单高斯/像素，代价体）**：**MVSplat**（Chen et al., 2024b）将每个像素的高斯数量缩减为一个，并引入平面扫描立体（plane-sweep stereo）构建代价体以增强多视图一致性。**DepthSplat**（Xu et al., 2024b）在此基础上引入深度交互机制，进一步提升了标准分辨率下的渲染质量。SurfSplat 与 DepthSplat 共享相同的编码器骨干和训练设置，在标准 256×256 分辨率下 PSNR 仅提升 0.033 dB（27.537 vs 27.504，RealEstate10K），表明二者在基础架构层面具有高度可比性。

**3DGS 基线（层级结构）**：**HiSplat**（Tang et al., 2024）采用层级化高斯表示，试图在表达效率与渲染质量之间取得平衡。

**3DGS 基线（单高斯/像素，无代价体）**：**TranSplat**（Zhang et al., 2025）同样采用每像素一个高斯的策略，但不依赖代价体，而是通过 Transformer 结构进行跨视图信息融合。

SurfSplat 与上述方法的关键分叉在于**原语类型**和**几何先验**两个维度。它将 3D 高斯椭球替换为 2D 高斯面元（2DGS），并显式引入表面连续性先验和强制 alpha 混合策略。这一设计决策的动机源于对前馈式方法瓶颈的诊断：仅依赖图像损失的稀疏输入条件下，网络难以解耦几何与外观，导致预测的高斯彼此独立，无法形成连续表面。

### 方法适用边界

SurfSplat 的适用边界由以下约束条件定义：

1. **相机位姿依赖**：方法要求输入图像附带已知的相机内参和外参矩阵。这一前提与 MVSplat、DepthSplat 等基于代价体的方法一致，但限制了在无位姿条件下的应用场景。

2. **稀疏视图假设**：模型设计面向稀疏输入（通常 2 帧上下文视图），在视图数量增加时理论上有进一步提升空间，但当前未针对密集视图进行专门优化。

3. **场景规模限制**：每个输入像素预测一个独立高斯，导致表示冗余。对于大规模场景（如城市级重建），高斯数量随图像分辨率线性增长，可能超出显存和计算预算。

4. **前馈式推理优势**：与逐场景优化的 3DGS/2DGS 方法（如原始 3D Gaussian Splatting 及其衍生）相比，SurfSplat 无需测试时优化，推理速度快，适合需要实时或近实时重建的应用场景。

### 局限性与开放问题

**已知局限**：

- **相机位姿依赖**：如前述，方法无法直接应用于无位姿条件下的重建，这限制了其在非结构化图像集（如用户拍摄的旅游照片）上的应用。
- **表示冗余**：每个像素一个高斯的策略缺乏自适应紧凑性。对于包含大面积无纹理区域（如墙壁、天空）的场景，大量高斯对最终渲染的贡献极小，造成计算资源浪费。
- **深度先验依赖**：单视图分支使用预训练的 Depth Anything V2 作为骨干，虽然提升了纹理缺失区域的鲁棒性，但也引入了对预训练模型的依赖，可能影响在特殊领域（如医学影像、水下场景）上的泛化能力。

**开放问题**：

1. **如何消除对已知相机位姿的依赖**？一个可能的方向是将位姿估计与前馈重建联合优化，或利用自监督位姿估计作为预处理步骤。近期一些工作在无位姿条件下的新视角合成方面取得了进展，但将其与前馈式 2DGS 框架结合仍是一个开放挑战。

2. **如何设计紧凑、自适应的表示机制**？避免每个像素一个高斯的冗余可以通过多种途径实现：引入可学习的原语剪枝策略、采用基于注意力机制的动态原语分配、或结合神经隐式表示进行混合建模。这些方向有望在保持渲染质量的同时显著提升模型效率与可扩展性。

3. **表面连续性先验能否推广到动态场景**？当前方法假设场景是静态的，表面连续性先验基于图像空间邻域关系推导。对于动态场景（如包含运动物体的视频），如何在时序维度上扩展该先验，实现时空一致的表面重建，是一个值得探索的方向。

4. **HRRC 指标能否成为前馈式重建的标准评估协议**？SurfSplat 提出的高分辨率渲染一致性（HRRC）指标有效暴露了传统指标无法捕捉的几何空洞和稀疏性问题。其在 DL3DV 高分辨率数据集上的排序与原生评估结果一致（Table 5），初步验证了其可靠性。但该指标是否应被社区广泛采纳作为几何质量的代理指标，仍需更多独立验证和标准化讨论。

## 原文 PDF

![[paperPDFs/ICLR_2026/SurfSplat_Conquering_Feedforward_2D_Gaussian_Splatting_with_Surface_Continuity_P_7f838b1d2532.pdf]]
