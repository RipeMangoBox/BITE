---
title: "DynVideo-E: Harnessing Dynamic NeRF for Large-Scale Motion- and View-Change Human-Centric Video Editing"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Change_Human_Centric_Video_Editing.pdf
aliases:
- DynVideo-E
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入动态 NeRF 作为视频-3D 表示，在 3D 动态人体空间和静态背景空间中进行编辑，并通过人体姿态引导的变形场将编辑结果传播至整个视频，从而实现高一致性的可动画视频编辑。"
primary_logic: "利用动态 NeRF 将复杂视频信息聚合到显式 3D 空间中，将视频编辑转化为 3D 编辑问题；通过多视角多姿态 Score Distillation Sampling 和重建损失，在 3D 空间中注入参考图像内容，结合文本引导局部超分辨率和风格迁移，实现高保真度的个性化视频编辑。"
claims:
- "提出将动态 NeRF 作为创新的视频表示，编辑在 3D 空间执行并通过变形场传播到整个视频。"
- "在 HOSNeRF 和 NeuMan 数据集上，人类偏好评比大幅领先现有 SOTA 方法 50% ∼ 95%。"
- "全模型在 Backpack 和 Lab 场景的 CLIP 分数分别为 0.756 和 0.647，移除任一组件性能下降。"
- "HOSNeRF & NeuMan datasets 上 Human Preference Rate = 显著优于所有基线"
---

# DynVideo-E: Harnessing Dynamic NeRF for Large-Scale Motion- and View-Change Human-Centric Video Editing

> [!tip] 核心洞察
> 利用动态 NeRF 将复杂视频信息聚合到显式 3D 空间中，将视频编辑转化为 3D 编辑问题；通过多视角多姿态 Score Distillation Sampling 和重建损失，在 3D 空间中注入参考图像内容，结合文本引导局部超分辨率和风格迁移，实现高保真度的个性化视频编辑。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DynVideo-E：利用动态 NeRF 进行大规模运动和视角变化的人体中心视频编辑 |
| 英文题名 | DynVideo-E: Harnessing Dynamic NeRF for Large-Scale Motion- and View-Change Human-Centric Video Editing |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2310.10624) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DynVideo-E |
| Dataset | HOSNeRF & NeuMan datasets |

> [!tip] 效果简介
> - HOSNeRF & NeuMan datasets 上，Human Preference Rate 为 显著优于所有基线，对比 SOTA 基线方法 (CoDeF, Rerender-A-Video 等)，变化 +50% ∼ +95% preference。
> - HOSNeRF & NeuMan datasets 上，CLIPScore 为 31.31，对比 所有基线方法均低于此值，变化 大幅领先。

## 概述

**问题瓶颈**：现有视频编辑方法在人体中心视频上面临根本性矛盾——逐帧编辑难以维持长程帧间一致性，而基于 2D 表示（如神经图集、规范图像）的方法无法有效表达大规模人体运动与视角变化，导致编辑质量下降、一致性崩溃。

**核心结论**：DynVideo-E 提出将动态 NeRF 作为视频的 3D 表示，将视频编辑转化为 3D 空间编辑问题。通过在 3D 动态人体空间和静态背景空间中执行编辑，并利用人体姿态引导的变形场将编辑结果传播至整个视频，实现了高一致性、可动画的人体中心视频编辑。

**方法定位**：该方法引入了一套图像驱动的视频-NeRF 编辑管线，核心创新包括：（1）多视角多姿态 Score Distillation Sampling，同时从个性化 2D 扩散先验和 3D 扩散先验中蒸馏编辑信号；（2）参考图像重建损失注入目标内容；（3）文本引导的局部人体部位超分辨率提升细节质量；（4）基于最近邻特征匹配的背景风格迁移。该方法将视频编辑从 2D 帧操作范式升级为 3D 空间编辑范式。

**主要结果**：在 HOSNeRF 和 NeuMan 数据集上，DynVideo-E 在人类偏好评比中领先现有 SOTA 方法 50% ∼ 95%，CLIP 分数大幅超越所有基线方法。消融实验验证了 2D 个性化先验、3D 多视角先验、重建损失和局部超分辨率等各组件的关键贡献。

## 背景与动机

视频编辑旨在对视频内容进行局部或全局的修改，使其符合特定的视觉风格或语义目标。近年来，基于扩散模型的图像编辑方法取得了显著进展，然而将其直接迁移至视频领域仍面临核心挑战：**帧间长程一致性与逐帧编辑之间的矛盾**。现有的视频编辑方法大多将视频视为一系列独立帧的集合，或采用基于 2D 的紧凑表示（如神经图集、规范图像），在单帧或 2D 空间中进行编辑操作，再通过某种传播机制将修改扩散至整个视频。这种范式在处理常规视频时表现尚可，但一旦面对**包含大规模人体运动与显著视角变化的人体中心视频**，其局限性便暴露无遗——2D 表示本质上无法有效聚合跨越不同姿态和视角的复杂动态信息，导致编辑结果出现纹理粘连、身份漂移、时序闪烁等一致性问题。

具体而言，现有方法存在以下结构性缺口：

- **表示能力的瓶颈**：基于 2D 图集的方法（如 **CoDeF**、**Text2LIVE**、**StableVideo**）试图将视频内容展开到一张或多张规范图像上，但人体的大幅度非刚体变形和自遮挡使得这种展开难以保持语义完整性，规范图像上往往出现撕裂或混叠，编辑质量因此严重退化。
- **编辑范式的局限**：基于帧的扩散编辑方法（如 **Tune-A-Video**、**FateZero**、**Rerender-A-Video**、**TokenFlow**、**ControlVideo**）虽然在单帧编辑质量上表现出色，但其帧间一致性依赖于注意力机制或光流引导，缺乏对场景三维结构的显式建模，难以应对大视角变化下的遮挡关系和几何一致性。
- **个性化编辑的缺失**：大多数现有方法仅支持纯文本驱动的编辑，缺乏将特定参考图像（如人物身份、服装纹理）精确注入视频的能力，无法满足人体中心视频编辑中对个性化内容的高保真需求。

上述问题的根源在于：**视频本质上是对 3D 动态场景的 2D 投影，缺乏显式的 3D 结构使得编辑操作无法在物理一致的空间中进行**。因此，一个自然的思路是将视频“升维”——从 2D 帧序列中重建出底层的 3D 表示，在 3D 空间中执行编辑，再将编辑结果渲染回任意视角的视频帧。动态神经辐射场（Dynamic NeRF）恰好提供了这样一种表示：它能够将跨时间、跨视角的视频信息聚合到一个统一的 3D 动态空间中，并通过变形场建立不同姿态下的人体几何对应关系。

基于这一洞察，本文提出 **DynVideo-E**，核心动机是**利用动态 NeRF 作为视频的 3D 表示，将视频编辑问题转化为 3D 空间中的编辑问题**。通过在 3D 动态人体空间和静态背景空间中分别执行编辑，并借助人体姿态引导的变形场将编辑结果传播至整个视频，从根本上解决大规模运动与视角变化下的长程一致性问题。同时，引入多视角多姿态的 Score Distillation Sampling（SDS）机制，从 2D 个性化扩散先验和 3D 扩散先验中蒸馏编辑信息，结合参考图像重建损失和文本引导的局部超分辨率，实现高保真度的个性化人体中心视频编辑。

## 核心创新

DynVideo-E 的核心创新在于将视频编辑问题从 2D 帧空间迁移至 3D 表示空间，从根本上改变了编辑的执行域和一致性传播机制。其关键创新可归纳为以下三个层面的 changed slots：

### 1. 视频表示：从 2D 帧/图集到动态 NeRF

现有视频编辑方法（如 **CoDeF**、**StableVideo**、**Text2LIVE** 等）依赖逐帧处理或 2D 神经图集/规范图像作为视频表示。这些 2D 表示在面临大规模人体运动与视角变化时，难以将动态信息有效聚合，导致编辑结果出现严重的帧间不一致和伪影。

DynVideo-E 将视频表示为**动态 NeRF**，包含两个解耦的 3D 空间：
- **3D 动态人体空间**：通过规范空间 $\Psi_{\mathrm{c}}^{\mathrm{H}}$ 聚合所有帧的人体动态信息，并利用人体姿态引导的变形场 $\Psi_{\mathrm{d}}^{\mathrm{H}}$ 将规范空间映射回各帧的变形空间。变形场进一步分解为粗粒度骨架驱动变形和细粒度非刚体残差（Eq. 2），确保对复杂姿态的精确建模。
- **3D 静态背景空间**：独立建模背景场景，避免人体与背景编辑的相互干扰。

这一表示的根本优势在于：编辑操作在 3D 规范空间执行后，可通过变形场自动传播至所有视频帧，从根本上解决了长程一致性问题。

### 2. 编辑范式：从 2D 编辑到多视角多姿态 3D 蒸馏

传统方法在 2D 帧或规范图像上直接编辑，缺乏对 3D 几何和多视角一致性的显式约束。DynVideo-E 将编辑转化为 3D 空间中的优化问题，通过以下机制从扩散先验中蒸馏编辑信号：

- **参考图像重建损失**（$\mathcal{L}_{\mathrm{REC}}$，Eq. 8）：在参考视角下同时监督 RGB、mask 和伪深度，将参考图像的身份信息注入 3D 模型。
- **3D SDS 损失**（$\mathcal{L}_{\mathrm{SDS}}^{\mathrm{3D}}$，Eq. 9）：利用 3D 扩散先验（Zero-1-to-3），以参考图像和相机位姿为条件，在多视角下进行 Score Distillation Sampling，显式保证多视角 3D 一致性。
- **2D 个性化 SDS 损失**（$\mathcal{L}_{\mathrm{SDS}}^{\mathrm{2D}}$，Eq. 10）：使用 Dreambooth-LoRA 在参考图像上微调的个性化 2D 扩散先验，以文本嵌入为条件，在多姿态下蒸馏个性化外观细节。

这种双先验蒸馏策略的关键因果机制在于：3D 先验提供多视角几何一致性约束，2D 个性化先验提供高保真外观细节，二者互补而非冗余（消融实验中移除任一项均导致性能显著下降，见 Table 2）。

### 3. 分辨率与背景编辑：文本引导局部超分 + 特征匹配风格迁移

- **文本引导局部人体超分辨率**：区别于全局固定分辨率渲染，该方法对局部人体部位进行放大渲染并监督，有效提升有效分辨率和细节质量。消融实验表明，移除该模块后平均 CLIP 分数从 0.674 降至 0.659（Table 3）。
- **基于 NNFM 的背景风格迁移**：使用最近邻特征匹配损失（$\mathcal{L}_{\mathrm{NNFM}}$），在 VGG 特征空间中最小化渲染特征图与参考风格图像间的余弦距离，将风格从 2D 参考图像迁移至 3D 背景模型，避免了对背景的逐帧独立编辑。

## 整体框架

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/002_Figure_2.jpg]]
*Figure 2: Overview of DynVideo-E. (1) Our video-NeRF model represents the input video as a 3D dynamic human space coupled with the deformation field and a 3D static background space. (2) Orange flowchart: Given the reference subject image, we edit the animatable 3D dynamic human space under multi-view multi-pose configurations by leveraging reconstruction losses, 2D personalized diffusion priors, 3D diffusion priors, and local parts super-resolution. (3) Green flowchart: A style transfer loss in feature spaces is utilized to transfer the reference style to our 3D background model. (4) Edited videos can be accordingly rendered by volume rendering in the edited video-NeRF model under source video camer...*

DynVideo-E 的整体编辑流程围绕一个核心表示展开：**Video-NeRF 模型**。该模型将输入的人体中心视频解耦为两个独立的 3D 空间——**3D 动态人体空间**（耦合姿态引导变形场）和 **3D 静态背景空间**（Figure 2）。这一设计将视频编辑问题从根本上转化为 3D 编辑问题：编辑操作在 3D 空间执行，再通过变形场传播至整个视频的所有帧，从而从根本上规避了逐帧编辑带来的长程一致性问题。

### 输入与输出

系统接受三类输入：一段包含大规模运动与视角变化的人体中心视频、一张**参考主体图像**（提供目标外观），以及一张**参考风格图像**（提供背景风格）。输出为编辑后的视频，可在源视频相机轨迹下渲染，也可在新视角下生成自由视点结果（Figure 2）。

### 管道模块与数据流

管道由三条并行的编辑流组成，分别对应 Figure 2 中的橙色、绿色和蓝色流程：

**1. 视频预处理与 Video-NeRF 构建**

输入视频首先被重建为 Video-NeRF 模型。动态人体部分采用规范空间加姿态引导变形场的架构，变形场被分解为粗粒度骨架驱动变形与细粒度非刚体残差（Eq. 1–2）；静态背景部分使用收缩高斯参数的集成位置编码进行建模（Eq. 3–4）。模型通过最小化渲染像素与真值之间的光度 MSE 损失、LPIPS 感知损失及 Mip-NeRF 360 正则化损失进行优化，最终沿光线积分颜色和密度得到渲染结果（Eq. 7）。

**2. 可动画 3D 动态人体编辑（橙色流）**

这是管道的核心编辑流。在参考主体图像提供的目标外观约束下，系统在**多视角多姿态**配置下编辑 3D 动态人体空间，具体包含四个关键子模块：

- **参考图像重建损失**（$\mathcal{L}_{\mathrm{REC}}$）：在参考视角下，对渲染结果的 RGB、人体 mask 和伪深度图进行监督，将参考图像的内容直接注入 3D 表示（Eq. 8）。
- **多视角多姿态 Score Distillation Sampling（SDS）**：同时利用两类扩散先验进行知识蒸馏——**3D 扩散先验**（Zero-1-to-3）以参考图像和相机位姿为条件，提供多视角一致性约束（Eq. 9）；**2D 个性化扩散先验**（Dreambooth-LoRA 在参考图像上微调）以文本嵌入为条件，保持个性化外观（Eq. 10）。
- **文本引导局部超分辨率**：对人体局部部位进行放大渲染和独立监督，提升有效分辨率和细节质量。
- **人体姿态采样策略**：训练过程中混合使用参考姿态、源视频随机姿态和随机采样姿态，增强编辑后模型的泛化动画能力。

**3. 背景风格迁移（绿色流）**

基于 ARF 的最近邻特征匹配损失（$\mathcal{L}_{\mathrm{NNFM}}$），将参考风格图像的 VGG 特征图迁移至 3D 背景模型。该损失最小化渲染特征图与风格图像特征图之间的余弦距离（Eq. NNFM），实现背景的风格化编辑。

**4. 源视频帧编辑渲染（蓝色流）**

在源视频帧的人体姿态下，仅使用 2D SDS 损失监督随机相机视角的渲染结果，确保编辑后的外观在原始视频轨迹上保持一致性。

编辑完成后，通过体积渲染即可在源视频相机位姿下生成编辑视频，亦可实现编辑后动态场景的高保真自由视点渲染。

## 核心模块与公式推导

### 视频-NeRF 表示（Video-NeRF Model）

DynVideo-E 的核心创新在于将输入视频表示为动态 NeRF，包含两个解耦的 3D 空间：**3D 动态人体空间**和**3D 静态背景空间**。

**3D 动态人体模型** $\Psi^{\mathrm{H}}$ 将所有帧的动态信息聚合到一个规范人体空间 $\Psi_{\mathrm{c}}^{\mathrm{H}}$ 中，并通过人体姿态引导的变形场 $\Psi_{\mathrm{d}}^{\mathrm{H}}$ 将规范空间点映射到各帧的变形空间：

$$
\Psi_{\mathrm{c}}^{\mathrm{H}}\left(\gamma\left(\mathbf{x}_{\mathrm{c}}\right)\right) \longmapsto \left(\mathbf{c}, d\right), \quad \Psi_{\mathrm{d}}^{\mathrm{H}}\left(\mathbf{x}_{\mathrm{d}}, \mathcal{I}, \mathcal{R}\right) \longmapsto \left(\mathbf{x}_{\mathrm{c}}\right)
$$

其中 $\mathbf{x}_{\mathrm{c}}$ 为规范空间点，$\mathbf{x}_{\mathrm{d}}$ 为变形空间点，$\mathcal{I}$ 和 $\mathcal{R}$ 分别为人体关节和旋转参数，$\mathbf{c}$ 和 $d$ 为颜色和密度。变形场进一步分解为粗粒度骨架驱动变形和细粒度非刚体残差：

$$
\mathbf{x}_{\mathrm{c}}^{\prime} = \Psi_{\mathrm{d}}^{\mathrm{H, coarse}}\left(\mathbf{x}_{\mathrm{d}}, \mathcal{I}, \mathcal{R}\right), \quad \mathbf{x}_{\mathrm{c}} = \mathbf{x}_{\mathrm{c}}^{\prime} + \Psi_{\mathrm{d}}^{\mathrm{H, fine}}\left(\mathbf{x}_{\mathrm{c}}^{\prime}, \mathcal{R}\right)
$$

**3D 静态背景模型** $\Psi_{\mathrm{S}}$ 采用合同高斯参数化，通过集成位置编码将高斯参数映射为颜色和密度：

$$
\Psi_{\mathrm{s}}\left(\widehat{\gamma}\left(\widehat{\pmb{\mu}}, \widehat{\Sigma}\right)\right) \longmapsto \left(\mathbf{c}, \sigma\right)
$$

其中集成位置编码 $\hat{\gamma}$ 显式建模了高斯的空间不确定性，公式为：

$$
\hat{\gamma}(\pmb{\hat{\mu}}, \hat{\Sigma}) = \left\{ \begin{array}{l} {\left[ \sin(2^{\ell} \pmb{\hat{\mu}}) \exp\left(-2^{2\ell-1} \operatorname{diag}\left(\hat{\Sigma}\right)\right) \right]} \\ {\left\lfloor \cos(2^{\ell} \pmb{\hat{\mu}}) \exp\left(-2^{2\ell-1} \operatorname{diag}\left(\hat{\Sigma}\right)\right) \right\rfloor} \end{array} \right\}_{\ell=0}^{L-1}
$$

**体积渲染**：最终像素颜色通过沿光线积分颜色和密度得到，采用标准体积渲染方程：

$$
\hat{\mathbf{C}}\left(\mathbf{r}\right) = \sum_{i=1}^{N} T_{i} \left(1 - e^{-\sigma_{i} \delta_{i}}\right) \mathbf{c}_{i}, \quad T_{i} = e^{-\sum_{j=1}^{i-1} \sigma_{j} \delta_{j}}
$$

### 图像驱动的 3D 动态人体编辑

编辑的核心是在 3D 空间中进行，通过多视角多姿态的 Score Distillation Sampling（SDS）和重建损失将参考图像内容注入视频-NeRF。

**参考图像重建损失** $\mathcal{L}_{\mathrm{REC}}$：在参考视角 $V^{\mathrm{r}}$ 下，同时监督 RGB、mask 和伪深度，确保参考图像内容被准确注入 3D 模型：

$$
\mathcal{L}_{\mathrm{REC}} = \lambda_{\mathrm{rgb}} \left\| \mathbf{M} \odot \left( \hat{\mathbf{I}}^{\mathrm{r}} - \mathbf{I}^{\mathrm{r}} \right) \right\|_{2}^{2} + \lambda_{\mathrm{mask}} \left\| \hat{\mathbf{M}}^{\mathrm{r}} - \mathbf{M}^{\mathrm{r}} \right\|_{2}^{2} + \frac{1}{2} \lambda_{\mathrm{depth}} \left( 1 - \frac{\mathrm{cov}\left( \mathbf{M}^{\mathrm{r}} \odot \mathbf{D}^{\mathrm{r}}, \mathbf{M}^{\mathrm{r}} \odot \hat{\mathbf{D}}^{\mathrm{r}} \right)}{\sigma(\mathbf{M}^{\mathrm{r}} \odot \mathbf{D}^{\mathrm{r}}) \sigma\left( \mathbf{M}^{\mathrm{r}} \odot \hat{\mathbf{D}}^{\mathrm{r}} \right)} \right)
$$

其中 $\hat{\mathbf{I}}^{\mathrm{r}}$、$\hat{\mathbf{M}}^{\mathrm{r}}$、$\hat{\mathbf{D}}^{\mathrm{r}}$ 分别为渲染的 RGB 图像、mask 和深度图，$\mathbf{M}$ 为人体 mask。

**3D SDS 损失** $\mathcal{L}_{\mathrm{SDS}}^{\mathrm{3D}}$：利用 3D 扩散先验（Zero-1-to-3）在多视角下进行 Score Distillation Sampling，以参考图像 $\mathbf{I}^{\mathrm{r}}$ 和相机位姿 $(\mathbf{R}, \mathbf{T})$ 为条件，保证多视角一致性：

$$
\nabla_{\theta} \mathcal{L}_{\mathrm{SDS}}^{\mathrm{3D}}\left(\phi, F_{\theta}\right) = \lambda_{\mathrm{3D}} \cdot \mathbb{E}_{t,\epsilon} \left[ w(t) \left( \epsilon_{\phi}\left( \mathbf{z}_{t}; \mathbf{I}^{\mathrm{r}}, t, \mathbf{R}, \mathbf{T} \right) - \epsilon \right) \frac{\partial \mathbf{I}}{\partial \theta} \right]
$$

**2D SDS 损失** $\mathcal{L}_{\mathrm{SDS}}^{\mathrm{2D}}$：引入个性化 2D 扩散先验，先在参考图像上使用 Dreambooth-LoRA 微调，再以文本嵌入 $\boldsymbol{y}$ 为条件进行 SDS，实现个性化编辑：

$$
\nabla_{\boldsymbol{\theta}} \mathcal{L}_{\mathrm{SDS}}^{\mathrm{2D}}(\boldsymbol{\phi}', \boldsymbol{F}_{\boldsymbol{\theta}}) = \lambda_{\mathrm{2D}} \mathbb{E}_{t,\epsilon} \left[ w(t) \left( \epsilon_{\boldsymbol{\phi}'}(\mathbf{z}_t; \boldsymbol{y}, t) - \epsilon \right) \frac{\partial \mathbf{I}}{\partial \boldsymbol{\theta}} \right]
$$

**文本引导的局部超分辨率**：对局部人体部位进行放大渲染并监督，提升有效分辨率和细节质量。消融实验（Table 3）表明，移除该模块后平均 CLIP 分数从 0.674 降至 0.659；同时移除超分辨率和重建损失后进一步降至 0.650；再移除 2D SDS 后骤降至 0.572，验证了个性化 2D 先验的关键作用。

### 背景风格迁移

背景编辑采用基于最近邻特征匹配（NNFM）的风格损失，将参考风格图像迁移至 3D 背景模型。损失函数最小化渲染特征图与参考风格图像的 VGG 特征图间余弦距离：

$$
\mathcal{L}_{\mathrm{NNFM}} = \lambda_{\mathrm{NNFM}} \cdot \frac{1}{N} \sum_{i,j} \min_{i',j'} D(\mathbf{F}(i,j), \mathbf{F}^{\mathrm{s}}(i',j'))
$$

其中余弦距离定义为：

$$
D(\mathbf{v}_1, \mathbf{v}_2) = 1 - \frac{\mathbf{v}_1^{\mathrm{T}} \mathbf{v}_2}{\sqrt{\mathbf{v}_1^{\mathrm{T}} \mathbf{v}_1 \mathbf{v}_2^{\mathrm{T}} \mathbf{v}_2}}
$$

### 人体姿态采样策略

训练过程中采用三种姿态采样策略：参考姿态（与参考图像对齐）、源视频随机姿态（保持与原视频的一致性）和随机采样姿态（增强可动画性），共同构成多视角多姿态训练流程。

## 实验与分析

### 主实验结果

DynVideo-E 在 HOSNeRF 和 NeuMan 两个数据集上与九种 SOTA 视频编辑方法进行了定量比较。Table 1 报告了两项核心指标：**CLIPScore** 和 **Human Preference Rate**。

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons of our DynVideo-E against SOTA approaches on HOSNeRF dataset [28] and NeuMan dataset [18]*

在 CLIPScore 上，DynVideo-E 取得 31.31，大幅领先所有基线方法，表明编辑结果与目标文本描述在语义层面高度一致。在人类偏好评比中，DynVideo-E 相较 SOTA 方法的优势达到 **+50% ∼ +95%** 的偏好率，验证了其在视觉质量和编辑一致性上的显著提升。

参与比较的基线方法涵盖主流视频编辑范式：逐帧扩散编辑（**Tune-A-Video**、**FateZero**）、光流与空间图引导编辑（**Rerender-A-Video**，Yang et al., arXiv 2023）、可控编辑（**ControlVideo**）、神经场引导编辑（**TokenFlow**）、视频-2D 规范表示（**CoDeF**）、分层神经图集编辑（**StableVideo**、**Text2LIVE**）以及零样本文本驱动编辑（**Text2Video-Zero**）。这些方法在处理大规模人体运动和视角变化时，均表现出不同程度的帧间不一致或编辑内容漂移，而 DynVideo-E 通过在 3D 空间编辑并利用姿态引导变形场传播编辑结果，从根本上规避了逐帧编辑的长程一致性问题。

Figure 3 展示了在 Backpack 和 Jogging 场景上的定性比较。DynVideo-E 在保持人物身份一致性的同时，实现了背景风格迁移和人物外观编辑的高保真度，而基线方法在剧烈姿态变化下普遍出现纹理撕裂、身份丢失或编辑效果退化。

### 消融实验

Table 2 报告了在 Backpack 和 Lab 两个场景上的逐组件消融结果，以 CLIP 图像嵌入余弦相似度作为评价指标。全模型在 Backpack 场景取得 **0.756**，在 Lab 场景取得 **0.647**，均为所有消融变体中最高。

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/006_Table_2.jpg]]
*Table 2: Quantitative ablation results of our method for the Backpack and Lab scene (higher score means better performance)*

消融路径沿组件重要性递减方向展开：

- **移除局部超分辨率**（w/o Super-resolution）：平均 CLIP 分数从 0.674 降至 0.659（Table 3），表明文本引导的局部放大渲染对细节质量有正向贡献。
- **进一步移除参考图像重建损失**（w/o Super-resolution, Rec）：平均 CLIP 分数降至 0.650，说明参考视角的 RGB、mask 和深度监督对注入参考图像内容不可或缺。
- **进一步移除 2D SDS**（w/o Super-resolution, Rec, 2D SDS）：平均 CLIP 分数骤降至 **0.572**，降幅最大。该结果验证了个性化 2D 扩散先验（Dreambooth-LoRA 微调）在保持人物身份和编辑语义方面的关键作用。
- **移除 3D SDS**（w/o Super-resolution, Rec, 3D SDS）：平均 CLIP 分数降至 0.641。3D 扩散先验（Zero-1-to-3）以参考图像和相机位姿为条件，对多视角一致性至关重要；移除后编辑结果在不同视角下出现明显不一致。
- **进一步移除 2D LoRA**（w/o Super-resolution, Rec, 3D SDS, 2D LoRA）：性能进一步下降，表明个性化微调对编辑质量的贡献独立于 2D SDS 损失本身。

Figure 4 提供了定性消融可视化。移除 2D SDS 后，编辑人物失去参考图像的身份特征；移除 3D SDS 后，新视角渲染出现纹理错位；同时移除重建损失和超分辨率后，细节模糊且参考内容注入不充分。

### 编辑效率

Table 4 比较了各方法的编辑操作时间。基于 NeRF 的表示天然比逐帧扩散方法更耗时，但 DynVideo-E 通过将编辑集中在 3D 空间一次性完成，避免了逐帧推理的累积开销。具体时间数据需查阅原表确认。

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/013_Table_4.jpg]]
*Table 4: Editing operation time comparison of our method against other approaches*

### 公平性说明

所有基线方法均按其原始代码或默认设置运行，并在相同视频片段上进行评估，确保比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/008_Figure_5.jpg]]
*Figure 5: DynVideo-E network designs: (a) Editing Background model, (b) Original human-object model, (c) Editing human model*

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l37_DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Chang/figures/007_Table.jpg]]

## 方法谱系与知识库定位

### 1. 问题定位：视频编辑的表示瓶颈

现有视频编辑方法的核心矛盾在于**帧间长程一致性**与**逐帧编辑灵活性**的权衡。主流方法将视频视为 2D 帧序列或 2D 神经图集/规范图像，在 2D 空间执行编辑后反向映射到视频帧。这种范式在以下场景中失效：

- **大规模运动**：人体姿态剧烈变化时，2D 图集无法有效聚合所有帧信息，导致编辑内容在不同帧间出现撕裂、错位。
- **视角变化**：相机运动使得同一人体部位在不同帧中呈现不同外观，2D 表示难以建立跨视角的对应关系。

基于扩散模型的视频编辑方法（如 **Tune-A-Video**、**FateZero**、**Rerender-A-Video** (Yang et al., arXiv 2023)、**ControlVideo**、**TokenFlow**）通过注意力机制或光流引导注入编辑内容，但在人体中心视频中，注意力图在剧烈运动下容易漂移，光流估计也会失效。基于图集的方法（如 **CoDeF**、**StableVideo**、**Text2LIVE**）试图将视频压缩到 2D 规范空间，但规范图像的构建本身依赖帧间对应，在大运动场景下无法形成干净的规范表示（见 Figure 9 的可视化验证）。

DynVideo-E 将这一瓶颈诊断为**表示维度不足**：2D 表示无法承载 3D 动态场景的几何和外观信息，因此编辑必须在 3D 空间完成。

### 2. 方法谱系中的位置

DynVideo-E 处于**视频编辑**、**动态 NeRF**和**扩散先验蒸馏**三个领域的交叉点。

**相对于视频编辑方法**：DynVideo-E 将编辑范式从"在 2D 帧/图集上编辑"升级为"在 3D 动态人体空间 + 静态背景空间中编辑"。这一转变使得编辑结果天然具备多视角一致性和时序一致性，因为编辑后的 3D 表示通过体积渲染生成任意视角和姿态的视频帧。与 **Text2Video-Zero** 等零样本文本驱动方法相比，DynVideo-E 额外引入了参考图像作为个性化条件，实现了身份保持的编辑。

**相对于动态 NeRF 重建方法**：DynVideo-E 的视频-NeRF 模型（Section 3.1）继承了人体 NeRF 的标准架构——规范人体空间配合姿态引导变形场，并引入粗-细变形分解（Eq. 2）和合同高斯静态场景表示（Eq. 3-4）。但 DynVideo-E 的创新在于**将重建模型转化为可编辑表示**：在重建损失之外，叠加多视角多姿态 SDS 蒸馏、参考图像重建约束和局部超分辨率监督，使得 NeRF 的参数空间同时满足"忠实于参考图像"和"保持 3D 一致性"两个目标。

**相对于扩散先验蒸馏方法**：DynVideo-E 同时利用 3D 扩散先验（Zero-1-to-3，Eq. 9）和个性化 2D 扩散先验（Dreambooth-LoRA，Eq. 10）。3D SDS 以参考图像和相机位姿为条件，确保编辑后的人体在新视角下与参考图像一致；2D SDS 以文本嵌入为条件，提供语义层面的个性化引导。这种双先验设计的关键洞察是：3D 先验保证几何一致性但缺乏个性化细节，2D 先验提供丰富外观但缺乏视角泛化能力，两者互补。

### 3. 适用边界与局限

**适用场景**：DynVideo-E 专为**人体中心视频**设计，要求输入视频包含可检测的人体姿态序列（用于驱动变形场），且需要一张清晰的参考主体图像和一张背景风格图像。在 HOSNeRF 和 NeuMan 数据集上的实验覆盖了背包、慢跑、实验室、舞蹈等场景，人体运动和视角变化幅度较大。

**已知局限**：
- **计算开销**：基于 NeRF 的表示和编辑流程较为耗时（见 Table 4 的操作时间对比），论文明确指出未来可探索使用体素或哈希网格加速视频-NeRF 模型。
- **姿态依赖**：变形场的质量依赖于人体姿态估计的准确性，在遮挡严重或姿态估计失败的场景下可能出现变形伪影。
- **背景编辑的独立性**：背景风格迁移（基于 ARF 的 NNFM 损失，Eq. 11-12）与人体编辑在 3D 空间独立进行，未建模人-物交互（如阴影、反射），在复杂交互场景下可能产生不一致。

### 4. 开放问题

- **表示效率**：如何将动态 NeRF 替换为更高效的显式 3D 表示（如 3D Gaussian Splatting），在保持编辑质量的同时大幅降低训练和渲染时间？
- **多主体扩展**：当前方法仅处理单人场景，能否扩展到多人交互场景？多人场景需要同时建模多个变形场和主体间的遮挡关系。
- **时间一致性保证**：虽然 3D 编辑天然提供时序一致性，但 SDS 蒸馏的随机性可能引入帧间闪烁，是否需要额外的时序正则化？
- **编辑可控性**：当前编辑依赖参考图像和文本提示，能否支持更精细的局部编辑（如仅更换上衣颜色）或运动编辑（如改变动作风格）？

## 原文 PDF

![[paperPDFs/CVPR_2024/DynVideo_E_Harnessing_Dynamic_NeRF_for_Large_Scale_Motion_and_View_Change_Human_Centric_Video_Editing.pdf]]
