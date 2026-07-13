---
title: "FaceCam: Portrait Video Generation with Camera Control"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/FaceCam_Portrait_Video_Generation_with_Camera_Control.pdf
project_link: null
code_link: https://github.com/Wan-Video/Wan2.2
aliases:
- FaceCam
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 采用基于人脸关键点的尺度感知相机表示，通过图像像素对应消除单目尺度模糊，提供确定性、可精确控制的相机条件信号。
primary_logic: 图像空间中的点对应关系（人脸关键点）足以在未标定尺度下表征相机运动；将关键点渲染为像素通道作为条件，无需3D先验即可实现尺度不变且直观的相机控制。
claims:
- 基于外参的相机表示存在尺度模糊，同一图像可对应无穷多3D配置，导致重渲染漂移和可控性差。
- 人脸关键点提供可靠的像素对应关系，可直接作为相机表示，消除尺度模糊。
- 合成相机运动和多镜头拼接的训练数据生成策略使模型能从静态多视角数据中学习连续相机轨迹控制。
- 在Ava-256静态相机评估中，FaceCam在PSNR (15.85 vs 10.32) 和身份保留 (ArcFace 0.8574 vs 0.7014) 上显著优于基线。
---

# FaceCam: Portrait Video Generation with Camera Control

> [!tip] 核心洞察
> 图像空间中的点对应关系（人脸关键点）足以在未标定尺度下表征相机运动；将关键点渲染为像素通道作为条件，无需3D先验即可实现尺度不变且直观的相机控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | FaceCam: 具备相机控制的人像视频生成 |
| 英文题名 | FaceCam: Portrait Video Generation with Camera Control |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.05506) · [Code](https://github.com/Wan-Video/Wan2.2) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | FaceCam |
| Dataset | Ava-256, In-the-wild |

> [!tip] 效果简介
> - Ava-256 (静态多视角) 上，PSNR↑ 15.85 vs 10.32 (TrajectoryCrafter) (+5.53)。
> - Ava-256 上，SSIM↑ 0.7208 vs 0.5816 (FaceCam*) (+0.1392)；LPIPS↓ 0.2521 vs 0.5494 (FaceCam*) (-0.2973)；ArcFace↑ 0.8574 vs 0.7014 (ReCamMaster) (+0.1560)。
> - In-the-wild (动态相机) 上，Camera Correctness↑ 97.00 vs 99.00 (TrajectoryCrafter) (-2.00)。

## 概要

单目人像视频的相机控制面临一个根本性瓶颈：**尺度模糊**。现有方法将相机外参（旋转矩阵和平移向量）作为条件信号注入生成模型，但在未标定的单目拍摄中，场景的度量深度不可观测——同一段视频可以对应无穷多种“3D场景+相机轨迹”的组合，仅在全局相似变换下等价。这种尺度歧义导致基于外参的相机表示无法提供确定性的控制信号，模型在重渲染时容易出现几何漂移、人像扭曲甚至出框（Fig. 2A）。基于3D重建的方法（如 **TrajectoryCrafter**）试图通过估计动态点云来绕过这一问题，但点云估计本身存在误差，在大姿态变化下会累积为面部畸变。

**FaceCam** 的核心洞察是：图像空间中的点对应关系足以在未标定尺度下表征相机运动，无需任何3D先验。具体而言，人脸关键点提供了可靠、密集的2D像素对应，将其从锚帧渲染为像素通道作为条件信号，即可消除单目尺度模糊，实现确定性的相机控制（Fig. 2B）。这一尺度感知的相机表示是 FaceCam 区别于所有现有方法的**因果旋钮**——它直接编码“相机引起的图像形成变换的可观测部分”，而非推断不可观测的度量深度。

在方法定位上，FaceCam 处于**视频扩散模型 + 相机可控生成**的交叉点。其技术路线可概括为：以预训练视频扩散Transformer（基于 Wan2.2 的整流流框架）为生成骨干，将渲染的人脸关键点图作为额外的通道条件注入去噪网络，并通过三项关键的数据生成策略——尺度/颜色增强、合成相机运动、多镜头拼接（Algorithms 1-3）——使模型从静态多视角数据中学会连续相机轨迹的控制能力。

**主要结果**：在 Ava-256 静态多视角基准上，FaceCam 在 PSNR（15.85 vs. 10.32）、SSIM（0.7208 vs. 0.5816）和身份保留 ArcFace（0.8574 vs. 0.7014）上均显著优于最强基线。在自然场景动态相机评估中，FaceCam 在保持高相机正确性（97.00）的同时，身份相似度（83.94 vs. 78.92）和视觉质量（Imaging Quality 73.49 vs. 69.05）全面领先。消融实验证实，合成相机运动和多镜头拼接是模型获得连续角度变化能力的关键，移除其中任一策略都会导致相机正确性或身份保留的显著下降。

### 单目人像视频中的相机控制需求

人像视频的相机控制旨在从单一源视频出发，按给定的相机轨迹生成新视角下的目标视频。形式化地，给定源视频 $V^s$ 和目标相机轨迹 $C^t$，任务目标是生成 $V^t = \text{FaceCam}(V^s, C^t)$，使得 $V^t$ 在保持人物身份与动态的同时，精确遵循 $C^t$ 所定义的视角变化。这一能力在直播重摄、影视后期、虚拟主播等场景中具有广泛需求。

### 现有方法的瓶颈：尺度模糊与几何失真

当前相机控制方法主要沿两条技术路线展开，但均面临根本性挑战。

**基于外参的相机表示。** 以 **ReCamMaster**（Bai et al., ICCV 2025）为代表的方法将相机外参（旋转 $\mathbf{R}$ 与平移 $\mathbf{t}$）编码后注入扩散Transformer的注意力层。然而，在单目拍摄中，度量深度不可观测——场景仅在未知全局尺度因子 $\alpha$ 下被确定。如 Fig. 2A 与 Sec. 3.2 所揭示，同一张图像可对应无穷多种 $(\mathbf{R}, \alpha\mathbf{t})$ 配置，导致条件信号存在内在歧义。这种尺度模糊使模型难以学习确定的相机-像素映射，在实际生成中表现为重渲染漂移和可控性差，尤其在大姿态变化下头部常被推出画面。

**基于3D重建的方法。** **TrajectoryCrafter** 等方案尝试从单目视频中估计动态点云，再将其渲染为相机控制信号。该路径的致命弱点在于单目3D估计本身存在显著误差，点云重建质量不稳定，导致渲染出的条件信号携带几何失真。这些失真被直接传播至生成过程，造成面部扭曲和纹理扁平化（见 Fig. 5 定性对比）。

### 核心洞察：图像空间点对应作为尺度感知的相机表示

FaceCam 的核心洞察来自经典多视图几何：图像空间中的点对应关系足以表征相对相机运动，且天然规避尺度模糊。具体而言，给定至少7组2D对应点，可在未知内参下估计基础矩阵 $\mathbf{F}$；若内参 $\mathbf{K}$ 已知，则可进一步获得本质矩阵 $\mathbf{E} = \mathbf{K}^\top \mathbf{F} \mathbf{K}$。关键的是，透视投影方程

$$u = \frac{f_x x_c}{z_c} + c_x, \quad v = \frac{f_y y_c}{z_c} + c_y$$

在缩放变换 $\mathbf{x}_c' = \mathbf{R}(\alpha \mathbf{x}) + \alpha \mathbf{t} = \alpha \mathbf{x}_c$ 下保持像素坐标不变，从而消除了单目尺度模糊。

基于这一原理，FaceCam 采用**人脸关键点**作为天然、可靠的像素对应源——每帧检测468个MediaPipe关键点，通过将其从锚帧渲染为像素通道图作为条件信号，无需任何3D先验即可实现尺度不变且精确的相机控制。Fig. 2B 对比展示了这一尺度感知表示相较于外参表示的确定性优势。

### 从静态多视角到连续相机轨迹的数据生成挑战

即使拥有了正确的相机表示，训练模型实现平滑的连续相机轨迹控制仍面临数据瓶颈。现有大规模视频数据多为静态相机拍摄，缺乏显式的相机运动标注。FaceCam 为此设计了两种训练数据生成策略——**合成相机运动**与**多镜头拼接**——从静态多视角数据中构造出具有连续轨迹和离散视角切换的训练样本，使模型能够学习从单一源帧到任意目标相机姿态的映射。这一数据策略是连接静态表示与动态生成能力的关键桥梁。

## 核心方法与创新机理

FaceCam 的核心创新在于用**尺度感知的像素对应关系**替代传统的外参相机表示，从根本上解决了单目人像视频中相机控制的核心瓶颈——尺度模糊。

### 问题根源：外参表示的尺度模糊

现有相机控制方法（如 **ReCamMaster**，Bai et al., ICCV 2025）将相机外参 $[\mathbf{R} \mid \mathbf{t}]$ 作为条件信号注入扩散模型。然而，在单目拍摄中，度量深度不可观测——场景仅能被确定到相差一个全局相似变换的程度。这意味着：

- **同一张图像可对应无穷多种 3D 配置**：对世界点 $\mathbf{x}$ 和位移 $\mathbf{t}$ 同时缩放 $\alpha$ 倍，像素坐标保持不变（$\mathbf{x}_c' = \mathbf{R}(\alpha \mathbf{x}) + \alpha \mathbf{t} = \alpha \mathbf{x}_c$）。
- **模型学习到的是模糊的映射**：生成器被迫从外参中推测不可观测的尺度，导致重渲染时产生几何漂移和可控性下降（Fig. 2A, Sec. 3.2）。
- **基于 3D 重建的方法同样存在误差**：**TrajectoryCrafter** 等方法通过估计动态点云并渲染作为控制信号，但点云估计误差会直接导致面部几何失真。

### 核心突破：人脸关键点作为尺度感知的相机表示

FaceCam 的关键洞察在于：**图像空间中的点对应关系足以在未标定尺度下表征相机运动**。经典多视图几何表明，给定至少 7 对 2D 对应点，即可从两张未标定视图估计基础矩阵 $\mathbf{F}$；若已知内参 $\mathbf{K}$，则可升级为本质矩阵 $\mathbf{E} = \mathbf{K}^\top \mathbf{F} \mathbf{K}$，从而恢复相对相机运动。

基于此，FaceCam 将**锚帧渲染的人脸关键点图**作为相机条件信号（Fig. 2B, Sec. 3.3）：

- 使用 MediaPipe 检测每帧的 468 个人脸关键点 $\mathbf{U}_i = \{\mathbf{u}_{i,k}\}_{k=1}^{468}$。
- 将目标相机轨迹下的 3D 人脸关键点投影为 2D 像素坐标 $\mathbf{u}_k = \mathcal{N}(\mathbf{K}(\mathbf{R}\mathbf{x}_k + \mathbf{t}))$，渲染为多通道图像。
- 该表示**天然尺度不变**：关键点的像素位置直接编码了相机诱导的图像形成变换，无需显式恢复深度或尺度。

### Changed Slot：相机条件表示的范式转换

| 维度 | 基线方法 | FaceCam |
|------|----------|---------|
| **表示形式** | 相机外参 $[\mathbf{R} \mid \mathbf{t}]$（尺度模糊）或 3D 点云渲染（估计误差） | 锚帧渲染的人脸关键点图（尺度感知、像素空间对应） |
| **条件注入** | 外参编码注入 DiT 注意力层 | 关键点图作为额外通道条件直接输入 DiT |
| **3D 先验依赖** | 需要显式或隐式 3D 重建 | 无需 3D 先验，仅需 2D 关键点对应 |
| **可控性** | 大角度变化下失控、面部出框 | 精确跟随目标轨迹，保持面部在框内 |

### 配套创新：训练数据生成策略

为实现连续相机轨迹控制，FaceCam 引入两种数据生成策略（Sec. 3.4）：

1. **合成相机运动（Synthetic Camera Motion）**：对静态多视角数据，通过 PnP 求解器从关键点对应恢复相对位姿，合成平滑的相机轨迹，使模型学习连续运动控制。
2. **多镜头拼接（Multi-shot Stitching）**：将不同相机角度的视频片段拼接为长序列，引入大幅度的相机旋转变化，弥补静态数据视角覆盖不足的问题。

消融实验（Table 3, Fig. 9）表明：移除合成相机运动导致相机正确性下降、轨迹不平滑；移除多镜头拼接则使模型无法改变相机角度（正确性从 97.00 骤降至 86.00）。

### 推理管线的解耦设计

推理时，FaceCam 使用一个**与输入视频无关的代理 3D 头部模型**（FaceLift 生成的 3D Gaussian Head），沿目标相机轨迹渲染后检测关键点作为条件信号。消融实验（Table 3）证实，更换不同身份的代理头部对结果影响可忽略（ArcFace 在 84.45–84.74 之间），说明关键点表示成功将相机位姿与头部身份/表情解耦。

FaceCam 的整体框架围绕一个核心设计展开：**将相机控制问题转化为图像空间的点对应条件注入问题**，从而绕过传统基于外参或3D重建方法中固有的尺度模糊与估计误差。系统由四个关键模块串联构成，覆盖从数据准备到最终视频生成的完整流程。

### 任务定义

给定一段源人像视频 $V^s$ 和一条目标相机轨迹 $C^t$，FaceCam 的目标是生成目标视频 $V^t$：

$$V^t = \text{FaceCam}(V^s, C^t)$$

其中相机轨迹 $C^t$ 由一系列相机位姿（旋转 $\mathbf{R}$ 和平移 $\mathbf{t}$）组成，内参矩阵 $\mathbf{K}$ 假设已知且固定。这一公式化的核心挑战在于：模型必须在保持人物身份、表情和动态运动的同时，精确地改变观测视角。

### 模块架构与数据流

FaceCam 的 pipeline 分为训练和推理两个阶段，但共享相同的模块骨架（Figure 3）：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/004_Figure_3.jpg]]
*Figure 3: Training and inference pipeline of FaceCam*

**1. 相机条件生成模块（Camera Conditioning）**
这是 FaceCam 区别于其他方法的标志性设计。该模块不直接使用相机外参 $[\mathbf{R} \mid \mathbf{t}]$ 作为条件信号，而是将目标相机轨迹转化为**从锚帧渲染的人脸关键点图**（rasterized facial landmark maps）。具体而言：
- 在训练阶段，从目标视频的锚帧中检测人脸关键点，将其渲染为像素空间的通道图，作为相机条件信号。
- 在推理阶段，使用一个代理3D高斯头部模型（由 FaceLift 生成，与输入视频人物身份无关）沿目标相机轨迹渲染，再通过 MediaPipe 检测每帧的 468 个人脸关键点 $\mathbf{U}_i = \{\mathbf{u}_{i,k}\}_{k=1}^{468}$，生成条件图序列。

这一设计的因果逻辑在于：图像空间中的点对应关系足以表征相机运动（在未标定全局尺度的意义下），且天然避免了外参表示中“同一图像对应无穷多3D配置”的尺度模糊问题（详见 Fig. 2 的对比分析）。

**2. 3D VAE 编码器/解码器**
源视频 $V^s$、目标视频 $V^t$ 以及相机条件图序列分别通过一个3D变分自编码器（VAE）压缩到低维潜在空间。编码后的潜在表示 $z$ 大幅降低了后续扩散模型的计算负担，同时保留时空结构信息。

**3. 扩散Transformer（DiT with Flow Matching）**
潜在空间中的去噪过程由基于流匹配（Flow Matching）的扩散Transformer完成。前向扩散过程沿整流流路径进行：

$$z_t = (1 - t) z_0 + t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

模型 $v_\theta$ 学习预测速度场，训练目标为条件流匹配损失：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, z_0, \epsilon} \big\| v_\theta(z_t, t, \mathbf{c}) - (\epsilon - z_0) \big\|_2^2$$

其中 $\mathbf{c}$ 为条件信号（包括源视频潜在表示和相机条件图）。推理时采用确定性ODE积分从噪声逐步恢复到干净潜在表示：

$$z_{t - \Delta t} = z_t - \Delta t \, v_\theta(z_t, t, \mathbf{c})$$

DiT 内部采用混合专家（MoE）层以提升模型容量，其输出形式为：

$$y = \sum_{k \in S(x)} g_k(x) E_k(x)$$

**4. 相机条件注入模块**
渲染的人脸关键点图作为额外的像素通道条件，直接与源视频的潜在表示拼接后输入 DiT。这种通道级注入方式使得相机信息在去噪的每一步都参与特征调制，确保生成视频的视角变换紧密跟随目标轨迹。

### 训练数据生成策略

FaceCam 的训练数据生成包含三种关键增强策略（Figure 4），共同构建了从静态多视角数据到连续相机轨迹控制的桥梁：

- **尺度与颜色增强**：对源视频施加随机缩放和色彩扰动，提升数据多样性。
- **合成相机运动（Synthetic Camera Motion）**：在静态多视角数据中插值生成平滑的相机轨迹，使模型学会连续视角变化。
- **多镜头拼接（Multi-shot Stitching）**：将不同相机角度的片段拼接成完整轨迹，引入大幅度的相机旋转变化。

消融实验证实，移除合成相机运动会导致轨迹不平滑、相机正确性下降；移除多镜头拼接则使模型完全无法改变相机角度（Table 3, Fig. 9）。自然场景视频数据的加入进一步提升了身份保留和图像质量，使模型泛化至真实光照环境。

### 推理管线

推理时，用户只需提供一段源视频和一条目标相机轨迹。系统自动完成以下步骤：
1. 使用代理3D高斯头部沿目标轨迹渲染，获得每帧的代理视图；
2. 通过 MediaPipe 检测每帧的 468 个人脸关键点，生成相机条件图序列；
3. 将源视频和条件图序列编码后送入 DiT 进行流匹配采样；
4. 3D VAE 解码器将去噪后的潜在表示恢复为像素空间的目标视频。

消融研究表明，代理3D头部的身份和表情选择对最终生成结果影响可忽略（ArcFace 在 84.45–84.74 之间波动，相机正确性保持 97.00），验证了关键点条件信号对代理头部的不敏感性（Table 3, Fig. 8）。

FaceCam 的核心设计围绕一个关键洞察展开：**图像空间中的点对应关系足以在未标定尺度下表征相机运动**。基于此，方法构建了三个紧密耦合的模块——尺度感知的相机表示、相机条件注入机制、以及训练数据生成策略——共同解决了单目人像视频中尺度模糊导致的几何失真问题。

### 尺度感知的相机表示

现有相机控制方法（如 **ReCamMaster**，Bai et al., ICCV 2025）普遍采用外参 $[\mathbf{R} \mid \mathbf{t}]$ 作为相机条件信号。然而，在单目捕获中，度量深度不可观测，场景仅能确定到一个全局相似变换（未知尺度 $\alpha$）。这意味着同一图像可对应无穷多组 $(\mathbf{R}, \mathbf{t})$ 配置，导致条件信号具有内在模糊性（Fig. 2A, Sec. 3.2）。

FaceCam 转而采用**图像空间点对应**作为相机表示。经典多视图几何表明，给定至少七对 2D 对应点，可在未标定视图间估计基础矩阵 $\mathbf{F}$；若内参 $\mathbf{K}$ 已知，则可通过本质矩阵转换 $E = \mathbf{K}^\top F \mathbf{K}$ 恢复相对位姿。这一表示的核心优势在于**尺度不变性**：缩放世界点 $\alpha \mathbf{x}$ 和位移 $\alpha \mathbf{t}$ 后，像素坐标保持不变，即 $\mathbf{x}_c' = \mathbf{R}(\alpha \mathbf{x}) + \alpha \mathbf{t} = \alpha \mathbf{x}_c$（Sec. 3.2）。

在人脸场景中，**人脸关键点**天然提供可靠的点对应关系。FaceCam 使用 MediaPipe 检测的 468 个人脸关键点集 $\mathbf{U}_i = \{ \mathbf{u}_{i,k} \}_{k=1}^{K}$，通过关键点投影公式将其与相机运动关联：

$$\mathbf{u}_k = \mathcal{N}(\mathbf{K}(\mathbf{R}\mathbf{x}_k + \mathbf{t}))$$

其中 $\mathbf{x}_k$ 为 3D 人脸关键点，$\mathcal{N}$ 为透视投影（含归一化）。给定 3D 关键点 $\mathbf{X}$ 及其 2D 投影 $\mathbf{U}$，PnP 求解器可恢复相机旋转 $\mathbf{R}$ 和平移 $\mathbf{t}$（至全局尺度）。但 FaceCam **不显式输出位姿**，而是将渲染的关键点图直接作为像素通道条件输入生成器（Sec. 3.3–3.4）。

### 相机条件注入与生成框架

FaceCam 的视频生成框架基于扩散 Transformer（DiT）与 Flow Matching。视频首先经 3D VAE 编码器压缩至潜在空间，随后在潜在空间中进行条件去噪。前向扩散过程采用整流流框架：

$$z_t = (1 - t) z_0 + t \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

训练目标为条件流匹配（CFM）损失：

$$\mathcal{L}_{\mathrm{CFM}} = \mathbb{E}_{t, z_0, \epsilon} \big\| v_\theta(z_t, t, \mathbf{c}) - (\epsilon - z_0) \big\|_2^2$$

推理时通过确定性 ODE 积分从噪声恢复数据：

$$z_{t - \Delta t} = z_t - \Delta t \, v_\theta(z_t, t, \mathbf{c})$$

相机条件 $\mathbf{c}$ 以**渲染的关键点图**形式注入 DiT。具体而言，从目标视频的锚帧渲染 2D 关键点图，将其作为额外通道与视频潜在表示拼接，送入 DiT 注意力层。这一设计使模型直接从像素对应关系中学习相机运动与外观变化之间的映射，无需显式 3D 先验（Fig. 3, Sec. 4.1）。

### 训练数据生成策略

为从静态多视角数据中学习连续相机轨迹控制，FaceCam 引入两种数据增强策略（Sec. 3.4）：

- **合成相机运动（Synthetic Camera Motion）**：在训练视频片段内插值生成平滑的相机轨迹，使模型学习连续视角变化。
- **多镜头拼接（Multi-shot Stitching）**：将不同相机角度下拍摄的片段拼接为长序列，强制模型学习大幅度的相机旋转。

此外，还对源视频施加尺度和颜色增强以提升数据多样性（Fig. 4）。消融实验表明，移除合成相机运动会降低轨迹平滑性；移除多镜头拼接则使模型完全无法改变相机角度（Table 3, Fig. 9）。

### 推理管线

推理时，FaceCam 使用一个与输入视频无关的**代理 3D 高斯头部模型**（由 FaceLift 生成），沿目标相机轨迹渲染代理视频，再通过 MediaPipe 提取每帧关键点作为相机条件信号。这一设计解耦了相机控制与源视频身份，消融实验证实代理头部选择对结果影响可忽略（ArcFace 84.45–84.74，相机正确性均为 97.00，Table 3）。

## 实验与关键发现

FaceCam 在两个基准上进行了系统评估：**Ava-256** 静态多视角数据集和**自然场景（In-the-wild）视频**，涵盖重建质量、身份保留、相机控制正确性和视觉质量等多个维度。以下从主结果、消融实验和失败模式三个层面展开分析。

### 主结果分析

#### Ava-256 静态相机评估

Table 1 汇报了在 Ava-256 上的定量对比。FaceCam 在所有指标上均显著优于基线方法：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/006_Table_1.jpg]]
*Table 1: Quantitative results on Ava-256. FaceCam outperforms the baselines on both reconstruction metrics and facial identity metric, indicating stronger stationary camera control ability and better preservation of identity and motion*

- **重建质量**：FaceCam 的 PSNR 达到 **15.85**，相比 TrajectoryCrafter 的 10.32 提升了 **+5.53 dB**；SSIM 为 0.7208，LPIPS 降至 0.2521。这一差距的核心原因在于 TrajectoryCrafter 依赖动态点云估计，当相机视角变化较大时，点云重建误差会导致严重的人脸几何失真（见 Figure 5 定性结果）。
- **身份保留**：ArcFace 相似度达到 **0.8574**，远超 ReCamMaster 的 0.7014（+0.1560）。ReCamMaster 在大姿态变化下常将头部推出画面外，导致身份信息丢失；而 FaceCam 的尺度感知关键点表示能精确约束人脸在画面中的位置和姿态。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results on Ava-256. FaceCam produces more realistic, ground-truth-aligned novel views than baselines. ReCamMaster [3] often fails under large pose changes, pushing the head out of frame, while TrajectoryCrafter [57] frequently shows facial distortions from dynamic point-cloud errors*

> **公平性说明**：为公平对比，对 ReCamMaster 强制第一帧为恒等旋转以获取有效结果，所有方法均评估前 29 帧。FaceCam* 使用通用 3D 头部渲染关键点而非真实目标视频关键点，保证在目标视频不可用时的公平性。

#### 自然场景动态相机评估

Table 2 汇报了在自然场景视频上的结果，FaceCam 在身份保留和视觉质量上优势明显：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on In-the-wild videos. FaceCam demonstrates superior identity preservation and camera trajectory correctness. It also generates videos with better visual quality and consistency as evidenced by VBench [25] scores*

- **相机控制正确性**：FaceCam 达到 **97.00**，略低于 TrajectoryCrafter 的 99.00（-2.00），但仍处于高水平。TrajectoryCrafter 的高正确性是以牺牲人脸纹理质量为代价的——其输出常出现扁平化人脸和弱纹理（Figure 6 panel 2）。
- **身份保留**：ArcFace 相似度为 **83.94**，领先 ReCamMaster 的 78.92（+5.02）。这表明在真实场景的光照、背景和动态变化下，FaceCam 的尺度感知条件仍能稳定绑定身份特征。
- **视觉质量**：Imaging Quality 为 **73.49**（vs. ReCamMaster 69.05），Aesthetic Quality 为 **59.91**（vs. ReCamMaster 55.85），验证了 FaceCam 生成结果在清晰度和美观度上的优势。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results on in-the-wild videos. We present three camera motions: (1) Arc Left, (2) Pan Right, and (3) Zoom In. ReCamMaster [3] often loses camera control in angle changes (panel 1) and produces blurry outputs under zoom in (panel 3). TrajectoryCrafter [57] yields flattened faces with weak facial texture (panel 2). FaceCam delivers higher visual quality and trajectory correctness, and more faithfully captures human geometry, including hands, hair, and facial features*

值得注意的是，ReCamMaster 在相机角度变化时经常失去控制（Figure 6 panel 1），在缩放操作下产生模糊输出（panel 3）。这些失败源于其基于外参的相机表示无法消除单目尺度模糊，导致生成过程中出现重渲染漂移。

### 消融实验

Table 3 和 Figure 9 系统消融了训练数据生成策略和代理 3D 头部的影响：

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2603_05506/figures/012_Table_3.jpg]]
*Table 3: Ablation study. We conduct ablation studies to quantify the impact of different training data components on the final performance of our model. We also vary the choice of proxy head and show that this selection has negligible effect on the generated results*

#### 合成相机运动（Synthetic Camera Motion）

移除合成相机运动后，相机正确性从 97.00 降至 **96.00**，ArcFace 从 83.94 降至 **81.19**。更关键的是，生成轨迹出现不连续或突变（Figure 9），说明合成相机运动对轨迹平滑性至关重要。该策略通过在静态多视角数据中插值生成连续相机轨迹，弥补了真实数据中相机运动稀疏的不足。

#### 多镜头拼接（Multi-shot Stitching）

这是影响最大的消融项：移除多镜头拼接后，相机正确性骤降至 **86.00**（-11.00），ArcFace 降至 **76.38**（-7.56）。模型完全无法学习改变相机角度（Figure 9）。多镜头拼接通过将同一场景的不同视角片段拼接为连续视频，强制模型学习视角变化与关键点位移之间的映射关系，是实现角度控制的核心机制。

#### 自然场景视频数据（In-the-wild Videos）

移除自然场景视频后，相机正确性反而达到 **100%**，但身份保留降至 77.73，图像质量也下降。这是因为模型仅在受控光照的 NeRSemble 数据上训练，虽能精确控制相机，但光照和外观无法泛化到真实场景，导致与源视频不一致（Figure 9）。这揭示了相机控制能力与域泛化之间的权衡。

#### 代理 3D 头部选择

更换不同的代理 3D 头部对结果影响可忽略：ArcFace 在 84.45–84.74 之间波动，相机正确性均为 97.00（Table 3）。Figure 8 进一步验证，代理头部的身份和表情不影响最终生成结果。这证明 FaceCam 的关键点条件信号仅编码相机姿态和尺度信息，与代理头部的个体特征解耦。

### 失败模式与局限性

1. **后视图盲区**：FaceCam 无法处理相机旋转到头部后方的视角，因为人脸关键点在该角度下不可见。这是基于关键点对应的表示方法的固有限制。
2. **场景泛化边界**：该方法仅适用于人脸场景，无法扩展至无关键点的通用场景。其核心假设——人脸关键点提供可靠对应——在非人脸场景中不成立。
3. **背景生成质量**：背景区域未专门优化，生成质量有限。论文指出可通过合成多视角数据改善，但当前版本未实现。
4. **推理效率**：推理速度慢，不适合实时应用。论文提出未来可通过模型蒸馏或采用更高效的视频生成骨干来解决。

### 关键图表结论

- **Table 1**：FaceCam 在 Ava-256 上的 PSNR 和 ArcFace 分别领先基线 5.53 dB 和 0.1560，验证了尺度感知关键点表示在静态相机控制上的决定性优势。
- **Table 2**：在自然场景中，FaceCam 以 83.94 的 ArcFace 和 73.49 的 Imaging Quality 显著优于基线，同时保持 97.00 的相机正确性，证明了方法的实用鲁棒性。
- **Table 3 + Figure 9**：多镜头拼接是相机角度控制的关键使能因素（移除后正确性下降 11 点），合成相机运动保障轨迹平滑性，自然场景数据提供域泛化能力——三者缺一不可。
- **Figure 5/6**：定性对比直观展示了基线方法的典型失败模式：ReCamMaster 的姿态漂移和 TrajectoryCrafter 的几何失真，与 FaceCam 的稳定输出形成鲜明对比。

## 定位与知识库关联

### 核心问题：单目人像视频中的尺度模糊与几何失真

现有相机控制方法在人像视频生成中面临一个根本性的瓶颈：**单目捕获中的尺度模糊**。当使用相机外参（旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$）作为条件信号时，由于单目视频无法观测到绝对的度量深度，同一个二维图像可以对应无穷多种三维场景配置——世界点和相机位移可以任意缩放而像素坐标保持不变（见尺度不变性证明：$\mathbf{x}_c' = \mathbf{R}(\alpha \mathbf{x}) + \alpha \mathbf{t} = \alpha \mathbf{x}_c$）。这导致模型在训练和推理时面临一对多的映射歧义，表现为重渲染漂移、相机轨迹不可控以及几何失真（Fig. 2A, Sec. 3.2）。

基于三维重建的替代方案则引入另一类误差。以 **TrajectoryCrafter** 为代表的方法先估计动态点云，再将点云渲染作为相机控制信号。然而，动态点云估计本身带有显著的几何误差，这些误差在视频生成中被进一步放大，导致面部扭曲和纹理退化（Fig. 5, Fig. 6）。

### 方法谱系中的定位

FaceCam 在相机控制视频生成的谱系中占据一个独特的位置：**利用图像空间的点对应关系替代参数化的相机表示，从而在未标定尺度下提供确定性的条件信号**。这一思路与现有方法形成清晰的分野：

| 方法 | 相机表示 | 尺度处理 | 核心局限 |
|------|---------|---------|---------|
| **ReCamMaster** (Bai et al., ICCV 2025) | 场景无关的外参，注入 DiT 注意力层 | 尺度模糊 | 大幅位姿变化下失控，头部移出画面（Fig. 5） |
| **TrajectoryCrafter** | 基于三维重建的动态点云渲染 | 依赖重建精度 | 点云估计误差导致面部扭曲（Fig. 5, Fig. 6） |
| **FaceCam** (本文) | 从锚帧渲染的人脸关键点图 | 尺度感知（像素空间对应） | 仅适用于人脸场景，无法处理头部后视图 |

FaceCam 的方法论根基来自经典多视图几何：给定至少七组二维点对应，可以估计未标定视图之间的基础矩阵 $\mathbf{F}$；若内参 $\mathbf{K}$ 已知，则可升级为本质矩阵 $\mathbf{E} = \mathbf{K}^\top \mathbf{F} \mathbf{K}$。点对应关系编码了“可观测的相机诱导的图像形成变换”，因此是相机运动的充分表示（Sec. 3.2）。FaceCam 将这一原理实例化为人脸关键点：使用 MediaPipe 检测的 468 个关键点提供密集、可靠的对应关系，将其渲染为像素通道作为扩散模型的条件输入（Fig. 3）。

### 训练数据生成策略的方法论贡献

FaceCam 的另一个关键创新在于**训练数据生成策略**，解决了从静态多视角数据学习连续相机轨迹控制的问题：

1. **合成相机运动（Synthetic Camera Motion）**：在静态多视角视频的相邻帧之间插值生成平滑的相机轨迹，使模型学会连续的相机控制。消融实验表明，移除该策略导致相机正确性下降（97.00 → 96.00），身份保留退化（ArcFace 83.94 → 81.19），且轨迹出现不连续或突变（Table 3, Fig. 9）。

2. **多镜头拼接（Multi-shot Stitching）**：将来自不同相机角度的视频片段拼接成一段连续视频，引入大幅度的相机角度变化。这是模型能够改变相机角度的关键——移除该策略后，相机正确性急剧下降（97.00 → 86.00），身份保留严重退化（ArcFace 83.94 → 76.38），模型几乎无法改变相机视角（Table 3, Fig. 9）。

这两种策略共同构成了 FaceCam 数据管线的核心，使得仅使用静态多视角数据（NeRSemble）训练的模型就能泛化到自然场景中的动态相机控制。

### 适用边界与局限

FaceCam 的设计决定了其适用边界：

- **人脸场景锁定**：方法依赖人脸关键点作为对应关系的载体，因此无法直接扩展至无关键点的通用场景。这是其核心的适用范围限制。
- **头部后视图盲区**：当相机旋转到头部后方时，人脸关键点不可见，相机条件信号失效。这是一个根本性的几何约束，需要重新定义对应点的编码方式才能突破。
- **背景生成未专门优化**：当前管线的背景生成质量有限，论文指出可通过合成多视角数据改善，但尚未实现。
- **推理速度瓶颈**：基于扩散 Transformer 的生成过程计算量大，不适合实时应用。论文提出未来可通过模型蒸馏或采用更高效的视频生成骨干来缓解。

### 开放问题

1. **超越前视图的对应点编码**：如何重新定义对应点编码方式，使其在头部后视图或更广泛的场景中仍然有效？这可能需要引入多模态的对应关系（如深度图、法线图）或学习式的对应点表示。

2. **合成数据驱动的背景一致性**：能否利用合成多视角数据（如三维场景渲染）来提升背景生成质量？这需要解决合成数据与真实视频之间的域差距问题。

3. **实时推理的可行性**：模型蒸馏或轻量化骨干能否在保持相机控制精度的同时实现实时推理？这需要在效率与可控性之间找到平衡点。

4. **相机表示的理论完备性**：关键点对应关系在遮挡、大角度旋转等极端条件下的信息完备性如何？是否存在需要额外条件信号（如可见性掩码）的场景？

## 原文 PDF

![[paperPDFs/arxiv_2026/FaceCam_Portrait_Video_Generation_with_Camera_Control.pdf]]
