---
title: "CameraCtrl: Enabling Camera Control for Text-to-Video Generation"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.pdf
project_link: https://hehao13.github.io/projects-CameraCtrl/
code_link: https://github.com/hpcaitech/Open-Sora
aliases:
- CameraCtrl
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 采用Plücker嵌入作为相机姿态表示，并将其注入视频扩散模型的时间注意力层，实现对相机视角的精确操控。
primary_logic: Plücker嵌入为每个像素提供了三维几何解释，相比数值参数，能够更丰富地描述相机姿态；将相机特征注入时间注意力层而非空间层，更符合相机运动带来的全局帧间变化特性。
claims:
- 采用Plücker嵌入作为相机姿态条件的主要形式，以提供像素级的几何解释。
- 相机控制模块仅以Plücker嵌入为输入，与训练数据集的外观无关，避免了外观泄漏。
- 将相机特征注入到时间注意力层可以更好地捕获相机轨迹的时间关系，提升控制精度。
- 消融实验证实Plücker嵌入在相机控制指标（TransErr, RotErr）上优于原始数值、欧拉角及其他表示形式。
---

# CameraCtrl: Enabling Camera Control for Text-to-Video Generation

> [!tip] 核心洞察
> Plücker嵌入为每个像素提供了三维几何解释，相比数值参数，能够更丰富地描述相机姿态；将相机特征注入时间注意力层而非空间层，更符合相机运动带来的全局帧间变化特性。

| 字段 | 内容 |
|------|------|
| 中文题名 | CameraCtrl: 实现文本到视频生成的相机控制 |
| 英文题名 | CameraCtrl: Enabling Camera Control for Text-to-Video Generation |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2404.02101) · [Project](https://hehao13.github.io/projects-CameraCtrl/) · [Code](https://github.com/hpcaitech/Open-Sora) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CameraCtrl |
| Dataset | RealEstate10K test set, User study |

> [!tip] 效果简介
> - RealEstate10K test set 上，TransErr 12.98 (CameraCtrlAD) vs 14.02 (MotionCtrlVC) (-1.04)；RotErr 1.29 (CameraCtrlAD) vs 1.58 (MotionCtrlVC) (-0.29)；TransErr (I2V) 9.02 (CameraCtrlSVD) vs 10.21 (MotionCtrlSVD) (-1.19)。
> - User study (T2V) 上，User Preference Rate (%) 43.6 (CameraCtrlAD) vs 37.0 (MotionCtrlVC) (+6.6)。
> - User study (I2V) 上，User Preference Rate (%) 73.1 (CameraCtrlSVD) vs 26.9 (MotionCtrlSVD) (+46.2)。

## 概要

**核心问题**：现有文本到视频（T2V）生成模型缺乏精确的相机视角控制能力。用户无法像导演一样通过镜头语言（推拉摇移、旋转跟随）表达深层叙事意图，这严重限制了视频内容的可控性和艺术表现力。

**关键瓶颈**：相机姿态的表示形式与注入位置是两大核心挑战。早期方法（如 **MotionCtrl**，Wang et al., 2023）直接使用相机内参矩阵 $K$ 和外参矩阵 $E$ 的数值参数作为条件，但这些纯数值缺乏像素级的几何解释，难以让模型理解三维空间中的射线映射关系；同时，将相机条件注入空间注意力层无法有效捕获相机运动带来的全局帧间变化。

**核心方案**：CameraCtrl 提出三项关键设计来突破上述瓶颈：
1. **Plücker 嵌入作为相机表示**：将相机姿态转换为逐像素的 Plücker 坐标（式 3），为每个像素提供从相机中心出发的方向向量，赋予模型三维几何感知能力。
2. **外观无关的相机编码器**：基于 T2I-Adaptor 架构构建相机编码器 $\Phi_c$，仅接收 Plücker 嵌入序列，不接触训练数据的 RGB 外观信息，从根本上避免外观泄露。
3. **时间注意力层注入**：将编码后的多尺度相机特征通过像素加法融合到 U-Net 的时间注意力层，使控制信号与视频帧间的全局运动动态自然对齐。

**主要结果**：在 RealEstate10K 测试集上，CameraCtrl 在 T2V 设置下将平移误差（TransErr）从 MotionCtrl 的 14.02 降至 **12.98**，旋转误差（RotErr）从 1.58 降至 **1.29**；在 I2V 设置（基于 SVD）下，TransErr 从 10.21 降至 **9.02**，RotErr 从 1.41 降至 **1.18**。用户偏好率在 T2V 和 I2V 场景分别达到 **43.6%** 和 **73.1%**，显著优于对比方法。

**方法定位**：CameraCtrl 属于视频扩散模型的可控生成范式，通过训练一个轻量级相机编码器冻结基础模型（AnimateDiff 或 SVD）的权重实现即插即用的相机控制。该方法可与个性化 T2V 生成器（如 RealisticVision、ToonYou）及其他视觉控制器（如 SparseCtrl）协同工作，展现出良好的泛化性和兼容性。

**局限性提示**：对于训练数据中未覆盖的大角度旋转轨迹（如 100° 垂直旋转或 150° 水平旋转），CameraCtrl 无法准确跟随，生成的旋转幅度明显不足。此外，评估指标依赖 COLMAP 估计地面真值，存在不可消除的下限误差（TransErr 下限 6.93，RotErr 下限 1.02）。



文本到视频（T2V）生成模型近年来取得了显著进展，但生成的视频在相机视角控制方面仍存在明显不足。现有模型通常只能产生固定或随机化的镜头运动，无法让创作者通过精确的相机轨迹来表达深层叙事意图。在电影语言中，推拉摇移等镜头运动本身就是叙事的一部分——缓慢推进传达紧张感，环绕拍摄展示空间关系，俯仰变化暗示权力结构。这种可控性的缺失，使T2V生成在专业内容创作场景中的应用受到严重制约。

**现有方法的缺口**：部分工作尝试通过有限的方式引入相机控制。**AnimateDiff**（Guo et al., 2023b）通过MotionLoRA支持少数预定义的相机运动类型（如左移、右移、缩放），但无法泛化到用户自定义的任意轨迹。**MotionCtrl**（Wang et al., 2023）将相机姿态参数序列作为条件信号注入视频扩散模型，提供了更高的灵活性，但其核心局限在于仅使用相机内参矩阵K和外参矩阵E的原始数值或欧拉角作为条件表示。这种纯数值表示缺乏对三维几何结构的显式编码，模型需要自行从抽象数值中“学习”像素与空间的对应关系，导致相机控制精度不足——尤其是在需要精确跟随复杂轨迹时。

**核心瓶颈**：问题的本质在于相机姿态的表示方式与视频扩散模型架构之间的不匹配。数值参数（如焦距、旋转角度、平移向量）虽然紧凑，但丢失了像素级的三维几何线索；而相机运动本质上是全局性的帧间变化，应当在模型架构中与时间维度的处理机制相结合，而非简单地注入空间注意力层。

**本文动机**：CameraCtrl旨在解决上述两个关键问题：一是设计一种能够为每个像素提供几何解释的相机姿态表示，二是将该表示注入视频扩散模型中最适合捕获帧间动态的模块。通过这种设计，模型可以在不依赖训练数据外观信息的前提下，实现对任意相机轨迹的精确跟随，从而将镜头语言的控制权交还给创作者。



## 核心方法与创新机理

CameraCtrl 的核心创新在于将**像素级几何可解释的相机姿态表示**与**视频扩散模型的时间注意力机制**进行系统性耦合，从而实现对文本到视频生成中相机视角的精确控制。相较于现有方法，其关键改进体现在三个紧密关联的“可替换模块”（changed slots）上。

### 1. 相机表示：从数值参数到 Plücker 嵌入

此前的方法（如 **MotionCtrl**，Wang et al., 2023）直接使用相机内参矩阵 $\mathbf{K}$ 和外参矩阵 $\mathbf{E}$ 的原始数值或欧拉角作为条件信号。这类数值表示缺乏对三维空间的几何解释，模型难以从中学习到像素与相机运动之间的精确映射关系。

CameraCtrl 转而采用 **Plücker 嵌入**（Plücker embeddings, Sitzmann et al., 2021）作为相机姿态的主要表示形式。对于每一帧的每个像素 $(u,v)$，利用相机内参 $\mathbf{K}$ 和外参 $\mathbf{R}, \mathbf{t}$ 计算其在世界坐标系下的方向向量：

$$\mathbf{d}_{u,v} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^T + \mathbf{t}$$

Plücker 嵌入本质上是为每个像素提供了一条从相机光心出发的射线映射，赋予了每个像素明确的三维几何含义。这一表示的核心优势在于：它为视频扩散模型提供了**逐像素的几何线索**，使模型能够更精确地理解相机运动如何改变画面中每个像素的位置和外观。

消融实验（Table 2a）有力地证实了这一选择的决定性作用：Plücker 嵌入在相机控制精度指标上显著优于原始数值表示（TransErr: 12.98 vs. 13.88; RotErr: 1.29 vs. 1.51）和欧拉角表示（TransErr: 13.71; RotErr: 1.43），验证了几何可解释性对控制精度的关键贡献。

### 2. 相机编码器：外观无关的专用架构

在编码器架构设计上，CameraCtrl 避免使用 **ControlNet** 这类同时接收图像潜变量和相机条件的结构，因为 ControlNet 在训练过程中会接触到训练数据的外观信息，存在**外观泄漏**（appearance leakage）风险——即模型可能将特定相机运动与训练数据的视觉风格不当关联，从而损害泛化能力。

CameraCtrl 的相机编码器 $\Phi_c$ 基于 **T2I-Adaptor** 架构构建，其关键设计原则是：**仅接收 Plücker 嵌入序列作为输入，与训练数据集的外观完全解耦**。该编码器包含 4 个下采样尺度，每个尺度后接一个时间注意力模块，以捕捉相机姿态在帧间的时序依赖关系。消融实验（Table 2b）表明，T2I-Adaptor 结合时间注意力模块的架构在视频质量（FVD: 222.1）和相机控制精度（TransErr: 12.98, RotErr: 1.29）上均优于 ControlNet 及其变体。

### 3. 注入位置：时间注意力层的精准定位

相机控制信号注入到视频扩散模型 U-Net 的哪个位置，是决定控制效果的关键设计选择。此前的方法倾向于将条件信号注入**空间自注意力或交叉注意力层**，但这些层主要处理单帧内的空间关系，难以有效捕获相机运动带来的**全局帧间变化**。

CameraCtrl 的核心洞察在于：相机运动本质上引发的是跨帧的全局视角变化，这与时间注意力层所建模的帧间动态特性高度吻合。因此，CameraCtrl 将多尺度相机特征通过**像素加法**与 U-Net 潜在特征融合后，经可学习线性层注入到各时间注意力块的**第一个时间注意力层**。消融实验（Table 2c）证实，注入时间注意力层相比注入空间注意力层能显著提升相机控制精度。进一步的实验（Table 4）还表明，将相机特征同时注入 U-Net 的编码器和解码器两侧，比仅注入一侧能获得更优的 TransErr 和 RotErr。

### 创新链条的因果逻辑

上述三个创新点构成了一条清晰的因果链条：**Plücker 嵌入提供了像素级的几何解释**，使得模型能够精确理解相机运动的空间含义；**外观无关的编码器架构**确保了这种几何理解不会与特定训练数据的视觉外观产生虚假关联；**时间注意力层的精准注入**则将几何信息作用于视频生成中最能体现相机运动动态特性的计算环节。三者协同作用，共同实现了 CameraCtrl 在相机控制精度上的显著提升。



CameraCtrl 的整体框架围绕一个核心设计：在冻结的预训练视频扩散模型之上，外挂一个可训练的相机编码器 $\Phi_c$，将相机姿态条件注入去噪 U-Net 的时间注意力层，从而实现对生成视频中相机轨迹的精确控制。

**输入流。** 系统的输入由三部分组成：
1. **文本条件 $c_t$**：标准的文本提示，通过 CLIP 编码后注入 U-Net 的交叉注意力层。
2. **噪声潜变量 $z_t^{1:N}$**：长度为 $N$ 的视频帧潜变量序列，遵循标准扩散过程。
3. **相机姿态序列**：由内参矩阵 $\mathbf{K}$ 和外参矩阵 $\mathbf{R}, \mathbf{t}$ 构成的逐帧相机参数。这些参数首先被转换为 Plücker 嵌入——一种为每个像素提供三维几何解释的射线表示，计算方式为 $\mathbf{d}_{u,v} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^T + \mathbf{t}$（式 3），从而将抽象的姿态数值转化为像素级的几何线索。

**相机编码器 $\Phi_c$。** 这是 CameraCtrl 唯一需要训练的核心模块。它采用 T2I-Adaptor 架构，包含 4 个下采样尺度，每个尺度后接一个时间注意力模块。编码器仅接收 Plücker 嵌入序列作为输入，输出多尺度的相机特征，与训练数据集的外观完全解耦，从而避免了外观泄漏问题（Figure 2a）。

**特征融合与注入。** 多尺度相机特征通过像素加法与 U-Net 对应尺度的潜变量特征融合，再经过一个可学习的线性层，最终注入到各时间注意力块的第一层时间注意力中（Figure 2b）。这一注入位置的选择基于一个关键洞察：相机运动本质上带来的是全局帧间变化，将其与时间注意力机制耦合，比注入空间注意力层更能有效捕捉相机轨迹的时间动态。

**训练目标。** 整个框架遵循可控视频扩散的标准训练范式：
$$\mathcal{L}(\theta) = \mathbb{E}_{z_0^{1:N}, \epsilon, c_t, s_t, t} [\| \epsilon - \hat{\epsilon}_\theta(z_t^{1:N}, c_t, \Phi_s(s_t), t) \|_2^2]$$
其中 $s_t$ 为相机控制信号，$\Phi_s$ 即相机编码器，基础视频扩散模型（如 AnimateDiff 或 SVD）的参数保持冻结。

**模块关系总结。** 整个 pipeline 形成一条清晰的条件注入链路：相机参数 → Plücker 嵌入 → 相机编码器（含时间注意力）→ 多尺度特征 → 像素加法融合 → 线性层 → U-Net 时间注意力层。这一设计使得 CameraCtrl 可以即插即用地部署于不同的预训练视频扩散模型之上（T2V 的 AnimateDiff 或 I2V 的 SVD），无需修改基础模型的权重。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/002_Figure_2.jpg]]
*Figure 2: Framework of CameraCtrl. (a) Given a pre-trained video diffusion model (e.g. AnimateDiff (Guo et al., 2023b)) and SVD (Blattmann et al., 2023a), CameraCtrl trains a camera encoder on*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of CameraCtrl. It can control the camera trajectory for both general T2V (Guo et al., 2023b) and personalized T2V generation (civitai), shown in the first two rows. Besides, illustrated in the third row, it can be used with I2V diffusion models, like Stable Video Diffusion (Blattmann et al., 2023a). The condition image is the first image of row 3. CameraCtrl can also collaborate with other visual controllers, such as the RGB encoder from SparseCtrl (Guo et al., 2023a) to generate videos condition on image and text conditions and manage camera movements*



### 3.1 可控视频扩散训练目标

CameraCtrl 将相机姿态作为额外的控制信号 $s_t$ 注入预训练视频扩散模型。训练过程遵循标准的可控生成目标函数：

$$
\mathcal{L}(\theta) = \mathbb{E}_{z_0^{1:N}, \epsilon, c_t, s_t, t} [\| \epsilon - \hat{\epsilon}_\theta(z_t^{1:N}, c_t, \Phi_s(s_t), t) \|_2^2]
$$

其中，$z_0^{1:N}$ 表示 $N$ 帧视频的初始潜变量，$\epsilon$ 为标准高斯噪声，$c_t$ 为文本条件，$s_t$ 为相机姿态控制信号。编码器 $\Phi_s$ 将相机条件编码后集成到去噪网络 $\hat{\epsilon}_\theta$ 中，使模型在去噪过程中同时受文本语义和相机轨迹的约束。

### 3.2 Plücker 嵌入：像素级几何表示

相机姿态的表示形式是 CameraCtrl 的核心设计选择。传统方法直接使用内参矩阵 $\mathbf{K}$ 和外参矩阵 $\mathbf{E}$（或欧拉角）的数值作为条件输入，但这些标量参数缺乏与图像像素的几何对应关系。CameraCtrl 采用 Plücker 嵌入（Sitzmann et al., 2021）作为相机姿态的主要表示形式，为每个像素提供显式的三维几何解释。

给定相机内参 $\mathbf{K}$、旋转矩阵 $\mathbf{R}$ 和平移向量 $\mathbf{t}$，像素 $(u, v)$ 在世界坐标系下的方向向量计算为：

$$
\mathbf{d}_{u,v} = \mathbf{R} \mathbf{K}^{-1} [u, v, 1]^T + \mathbf{t}
$$

该方向向量捕获了从相机光心出发、穿过像素 $(u, v)$ 的射线几何信息。Plücker 嵌入在此基础上进一步编码射线的位置和方向，形成逐像素的几何特征图。与原始数值参数相比，这种表示具有两个关键优势：其一，它为每个像素提供了空间定位的几何线索，使模型更容易学习相机运动与画面变化之间的映射关系；其二，它仅依赖相机参数本身，与训练数据的外观无关，从而避免了外观泄漏问题。

### 3.3 相机编码器 $\Phi_c$ 与特征注入

相机编码器 $\Phi_c$ 负责将 Plücker 嵌入序列转换为多尺度相机特征，其架构设计遵循三个原则：

**编码器架构**：CameraCtrl 采用基于 T2I-Adaptor 的编码器结构，包含 4 个下采样尺度。每个尺度后额外引入时间注意力模块，以显式建模相机姿态在帧间的时序依赖关系。编码器仅接收 Plücker 嵌入序列作为输入，输出与 U-Net 各层级分辨率匹配的多尺度相机特征 $c_t$。

**特征融合方式**：在 U-Net 的每个时间注意力块中，相机特征 $c_t$ 与图像潜变量 $z_t$ 首先通过逐像素加法进行初步融合。随后，融合后的特征经过一个可学习的线性层，进一步整合两种表示。线性层的输出直接馈入该时间注意力块的第一个时间注意力层。

**注入位置选择**：相机特征被注入 U-Net 的时间注意力层而非空间注意力层。这一设计基于相机运动的本质特性——相机运动通常引起全局性的帧间视角变化，而非局部的空间形变。将相机条件与时间注意力机制结合，使模型能够更好地捕获相机轨迹的时序动态，从而提升控制精度。消融实验证实，时间注意力注入在 TransErr 和 RotErr 上均显著优于空间注意力注入。

### 3.4 相机控制评估指标

为量化相机控制精度，CameraCtrl 引入两个逐帧累积的几何误差指标。首先使用 COLMAP 从生成视频中估计相机姿态，再与输入的真实姿态进行比较。

**旋转误差（RotErr）**：衡量生成与真实旋转矩阵之间的角度偏差：

$$
\mathrm{RotErr} = \sum_{i=1}^{n} \operatorname{arccos} \frac{tr(\mathbf{R}_{gen}^{i} \mathbf{R}_{gt}^{i T}) - 1}{2}
$$

**平移误差（TransErr）**：衡量生成与真实平移向量的 L2 距离平方和：

$$
\mathrm{TransErr} = \sum_{i=1}^{n} \| \mathbf{T}_{gt}^{i} - \mathbf{T}_{gen}^{i} \|_2^2
$$

其中 $n$ 为视频帧数，$\mathbf{R}_{gen}^{i}$、$\mathbf{T}_{gen}^{i}$ 为 COLMAP 从生成视频第 $i$ 帧估计的旋转矩阵和平移向量，$\mathbf{R}_{gt}^{i}$、$\mathbf{T}_{gt}^{i}$ 为对应的真实值。需注意 COLMAP 自身存在估计误差，导致这两个指标存在不可消除的下限（TransErr 下限约 6.93，RotErr 下限约 1.02）。



## 实验与关键发现

### 主实验结果

CameraCtrl 在两个基础模型（AnimateDiff 和 SVD）和两个任务设置（T2V 和 I2V）上均展现出优于基线方法的相机控制精度。**Table 1** 汇总了定量比较结果。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons. MotionCtrlVC and MotionCtrlSVD represent MotionCtrl with VideoCrafter (Chen et al., 2023a) and SVD (Blattmann et al., 2023a) as base model, respectively. Correspondingly, CameraCtrlAD and CameraCtrlSVD denote base models of AnimateDiff and SVD with CameraCtrl respectively*

在 T2V 设置下，CameraCtrlAD 在 RealEstate10K 测试集上的平移误差 **TransErr** 为 12.98，旋转误差 **RotErr** 为 1.29，分别优于 MotionCtrlVC 的 14.02 和 1.58。用户偏好率方面，CameraCtrlAD 以 43.6% 对 37.0% 领先 MotionCtrlVC，其余约 19.4% 的评估者认为两者质量相当。

在 I2V 设置下，CameraCtrlSVD 的优势更为显著：TransErr 9.02 vs. 10.21，RotErr 1.18 vs. 1.41。用户偏好率差距急剧拉大——CameraCtrlSVD 获得 73.1% 的偏好，而 MotionCtrlSVD 仅获得 26.9%，表明 Plücker 嵌入在图像条件驱动场景中带来的几何一致性优势更为突出。

**Figure 3** 的定性对比直观展示了差异：MotionCtrl 生成的视频在相机运动过程中常出现视角漂移或场景扭曲，而 CameraCtrl 能更忠实地跟随给定的相机轨迹，保持场景几何的稳定性。

> **公平性说明**：所有定量指标使用统一协议——FVD、CLIPSIM、FC、ODD 基于 WebVid10M 的 1000 个随机视频计算；TransErr 和 RotErr 基于 RealEstate10K 测试集的 1000 个视频及对应真实相机姿态。CameraCtrl 与 MotionCtrl 均基于各自的基础模型进行相同的 50K 步微调，未引入额外外观训练数据。

### 消融实验

**Table 2** 系统消融了相机表示、编码器架构、注入位置和训练数据集四个关键设计选择。

**（a）相机表示**：Plücker 嵌入在所有表示形式中表现最优（TransErr 12.98，RotErr 1.29）。相比之下，原始数值矩阵（Raw Values）的 TransErr 为 13.88、RotErr 为 1.51；欧拉角（Euler Angles）为 13.71/1.43；方向向量+原点（Direction+Origin）为 13.62/1.42。**Figure 7** 的定性对比进一步验证：使用原始数值矩阵生成的视频存在明显的视角偏移，方向+原点表示有所改善但仍不够精确，而 Plücker 嵌入能生成与目标轨迹高度一致的相机运动。这一优势源于 Plücker 嵌入为每个像素提供了三维几何解释，使模型能更好地理解相机姿态变化对画面的影响。

**（b）编码器架构**：T2I-Adaptor 结合时间注意力模块的架构在视频质量（FVD 222.1）和相机控制（TransErr 12.98，RotErr 1.29）上均优于 ControlNet 及其变体。ControlNet 由于接收图像潜变量作为输入，存在外观泄露风险，导致 FVD 升高。引入时间注意力模块后，编码器能更好地捕捉相机姿态序列中的帧间时间关系。

**（c）注入位置**：将相机特征注入时间注意力层显著优于注入空间注意力层。注入空间层时 TransErr 升至 14.28、RotErr 升至 1.41，而注入时间层则为 12.98/1.29。这一结果验证了核心设计直觉：相机运动本质上是全局的帧间变化，与时间注意力机制处理时序动态的特性天然契合。

**（d）训练数据集**：RealEstate10K 在视觉质量和相机控制之间取得了最佳平衡（FVD 1088.9，TransErr 12.99，RotErr 1.39）。MVImageNet 和 Objaverse 虽然包含更多样化的物体外观，但其相机姿态分布与目标应用场景不匹配，导致控制精度下降。值得注意的是，添加 ACID 等小数据集联合训练未能提高控制精度，暗示数据分布质量比数据量更为关键。

**Table 4** 进一步消融了相机特征在 U-Net 中的注入位置：将特征同时注入编码器和解码器（TransErr 12.98，RotErr 1.29）优于仅注入编码器（13.56/1.36）或仅注入解码器（13.42/1.33），表明多尺度、双向的特征融合对精确相机控制至关重要。

### 失败模式与局限性

**Figure 20** 展示了 CameraCtrl 的主要失败模式：当相机旋转角度过大时，模型无法准确跟随轨迹。例如，100° 垂直均匀旋转和 150° 水平均匀旋转的场景下，生成的视频出现明显的视角滞后或场景崩溃。这是因为训练集 RealEstate10K 主要包含房地产漫游视频，缺乏极端旋转的样本，模型在推理时无法外推到训练分布之外的相机姿态。

此外，评估指标本身存在不可消除的下限。**Table 5** 显示，使用 COLMAP 在 RealEstate10K 测试集上估计的 TransErr 下限为 6.93，RotErr 下限为 1.02。这意味着即使完美重建了真实视频的相机轨迹，由于 COLMAP 自身的估计误差，指标也不会降至零。因此，CameraCtrl 的 TransErr 12.98 与下限 6.93 之间的差距部分源于评估噪声，实际控制精度可能高于数值所示。

其他局限包括：模型需要输入精确的相机参数序列（内参和外参），无法直接应用于无已知相机姿态的真实视频；当泛化到与 RealEstate10K 视觉差异巨大的场景时，性能受限于基础视频扩散模型的先验。

### 关键图表结论

- **Table 1**：CameraCtrl 在 T2V 和 I2V 设置下均一致优于 MotionCtrl，I2V 场景下的用户偏好率优势尤为显著（73.1% vs. 26.9%）。
- **Table 2**：Plücker 嵌入、T2I-Adaptor+时间注意力架构、时间层注入、RealEstate10K 数据集四个设计选择共同构成了 CameraCtrl 的性能基础，每个选择在消融中均被验证为最优。
- **Figure 3**：定性展示 CameraCtrl 生成的视频在相机运动跟随的准确性和场景几何一致性上明显优于 MotionCtrl。
- **Figure 7**：Plücker 嵌入相比原始数值矩阵和方向+原点表示，在相机轨迹跟随的精确度上有质的提升。
- **Figure 20**：暴露了模型在极端旋转角度下的泛化瓶颈，指明了未来改进方向——获取具有更大相机姿态分布的训练数据。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons between CameraCtrl and MotionCtrl. The first two rows are in the T2V setting, representing MotionCtrl with VideoCrafter and CameraCtrl with AnimateDiffV3 as base model, respectively. The last two rows are MotionCtrl and CameraCtrl with SVD as base model taking the image as a condition signal. Condition images are the first images of each row*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/005_Table_2.jpg]]
*Table 2: Ablation study on camera representation, condition injection and effect of various datasets*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative comparison of using different camera representations. The first row shows the result using the raw camera matrix values as camera representation. Result of the second row adopts the ray directions and camera origin as camera representation. The last row exhibits the result taking the Plücker embedding as the camera representation. All the results use the same camera trajectory and the text prompt*

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/009_Table_4.jpg]]
*Table 4: Ablation study of the camera feature injection place*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/006_Figure_4.jpg]]
*Figure 4: Applications of CameraCtrl. The first row represents a video generated by the base AnimateDiff. The Following two rows showcase the results of two personalized T2V generators, RealisticVision and ToonYou. The fourth row expresses the video generated by CameraCtrl integrated with another video control method, SparseCtrl (Guo et al., 2023a). The video of the last row is produced by a I2V generator, SVD, taking the first image of last row as a condition*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/014_Figure_10.jpg]]
*Figure 10: Qualitative comparison between MotionCtrl and CameraCtrl in I2V setting. The condition images are shown in the first images of each row. These images are generated with the SDXL (Podell et al., 2023) taking the text prompts located below of every two rows as input. Note that, both MotionCtrl and CameraCtrl only condition on the conditioning images, not include the text prompts. The rows 1, 3, 5, and 7 are the results of MotionCtrl, while the results of CameraCtrl are in rows 2, 4, 6, and 8. Every two adjacent rows are generated with the same condition image and the same camera trajectory*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/017_Figure_13.jpg]]
*Figure 13: Visual results of natural objects and scenes. The natural video generation results of CameraCtrl. CameraCtrl can be used to control the camera poses during the video generation process of natural objects and scenes*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/020_Figure_15.jpg]]
*Figure 15: Visual results of cartoon characters. With the personalized generator ToonYou (Brad-Catt), CameraCtrl can be used in the video generation process of cartoon character videos*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2404_02101/figures/023_Figure_18.jpg]]
*Figure 18: Camera movement intensity. The first two rows taking the pan down camera trajectory as input, with the camera translation interval in the second row being four times that of the first row. The camera trajectory for the third and fourth rows are zoom in, with the camera translation interval in the fourth row being four times that of the third row*



## 定位与知识库关联

### 1. 问题瓶颈与核心因果旋钮

现有文本到视频（T2V）生成模型虽在视觉质量上取得了显著进展，但普遍缺乏精确的相机视角控制能力。这一瓶颈使得生成内容无法通过镜头语言（如推拉摇移、跟拍环绕）表达深层叙事意图，严重限制了视频内容的可控性和艺术表现力。CameraCtrl 识别出的**真实瓶颈**在于：视频扩散模型需要一种既能精确编码相机姿态、又能与生成过程无缝融合的条件机制，而现有方案要么仅支持有限的预定义运动类型，要么因条件表示过于粗糙而无法实现精确控制。

CameraCtrl 的**核心因果旋钮**是采用 **Plücker 嵌入**（Plücker embeddings）作为相机姿态表示，并将其注入视频扩散模型的**时间注意力层**。这一设计背后的核心洞察是双重的：其一，Plücker 嵌入为每个像素提供了从相机光心出发的射线方向的三维几何解释，相比纯数值参数（如内参矩阵 $\mathbf{K}$ 和外参矩阵 $\mathbf{E}$ 的原始数值，或欧拉角）包含更丰富的空间结构信息；其二，相机运动本质上是全局性的帧间变化，将相机特征注入时间注意力层而非空间层，更符合这一动态特性，使模型能够更好地捕获相机轨迹的时间依赖关系。

### 2. 方法谱系与基线关系

CameraCtrl 的方法谱系可追溯至两条主要的技术脉络：基于扩散模型的视频生成基础架构，以及视频生成中的运动控制方法。

**基础视频扩散模型。** CameraCtrl 并非从头训练视频生成器，而是以预训练的视频扩散模型为基础进行条件控制模块的增量训练。在 T2V 设置下，其基座模型为 **AnimateDiff**（Guo et al., 2023b）；在 I2V 设置下，其基座模型为 **Stable Video Diffusion (SVD)**（Blattmann et al., 2023a）。这种"冻结基座、外挂控制"的范式使得 CameraCtrl 能够继承基座模型的强泛化能力，同时仅需训练轻量的相机编码器即可实现相机控制。

**直接竞争基线：MotionCtrl。** CameraCtrl 最直接的对比方法是 **MotionCtrl**（Wang et al., 2023），后者同样以相机姿态参数序列作为条件控制视频扩散模型。两者的关键差异体现在三个"变化槽位"上：

| 变化槽位 | MotionCtrl（基线） | CameraCtrl（本文） |
|----------|-------------------|-------------------|
| **相机表示** | 原始内参 $\mathbf{K}$ 和外参 $\mathbf{E}$ 的数值矩阵，或欧拉角 | Plücker 嵌入（像素级射线映射，含几何解释） |
| **编码器架构** | ControlNet（接受图像潜变量和相机条件输入，存在外观泄露风险）或简单图像适配器 | 基于 T2I-Adaptor 的相机编码器，仅接收 Plücker 嵌入，并引入时间注意力模块以捕捉帧间关系 |
| **相机注入层** | 空间自注意力或交叉注意力层 | U-Net 的时间注意力层（通过像素加法融合，经可学习线性层后接入第一层时间注意力） |

这些设计差异直接导致了性能差距。在 RealEstate10K 测试集上，CameraCtrl 在 T2V 设置下将平移误差（TransErr）从 MotionCtrl 的 14.02 降至 12.98，旋转误差（RotErr）从 1.58 降至 1.29；在 I2V 设置下，TransErr 从 10.21 降至 9.02，RotErr 从 1.41 降至 1.18。用户偏好率方面，CameraCtrl 在 T2V 和 I2V 设置下分别达到 43.6% 和 73.1%，显著优于 MotionCtrl 的 37.0% 和 26.9%（见 Table 1）。

**与 AnimateDiff 原生能力的对比。** AnimateDiff 本身通过 MotionLoRA 模块支持有限的相机运动类型（如"向左平移""放大"等离散类别），但无法泛化到用户自定义的连续相机轨迹。CameraCtrl 将相机控制从"离散类别选择"提升为"连续轨迹精确跟随"，实现了从运动先验到精确控制的范式升级。

### 3. 关键设计决策的消融证据

CameraCtrl 的最终架构由一系列消融实验支撑，每一项决策都经过严格的定量验证：

**相机表示的选择（Table 2a）。** 在 Plücker 嵌入、原始数值矩阵、欧拉角、以及方向向量+相机原点四种表示中，Plücker 嵌入在 TransErr（12.98）和 RotErr（1.29）上均取得最优。原始数值矩阵（TransErr 13.88, RotErr 1.51）和欧拉角（TransErr 13.71, RotErr 1.43）因缺乏像素级的几何解释而精度不足。这一结果验证了核心洞察：为每个像素提供三维几何上下文的表示形式，比扁平化的数值参数更适合作为相机控制的条件信号。

**编码器架构的选择（Table 2b）。** 在比较 ControlNet、T2I-Adaptor 及其变体时，T2I-Adaptor 结合时间注意力模块的架构在视频质量（FVD 222.1）和相机控制精度（TransErr 12.98, RotErr 1.29）上均达到最佳。ControlNet 架构因接受图像潜变量作为额外输入，引入了训练数据集的外观信息，导致外观泄露风险；而 T2I-Adaptor 仅以 Plücker 嵌入为输入，实现了外观无关的相机控制。

**注入位置的选择（Table 2c）。** 将相机特征注入时间注意力层相比注入空间注意力层，显著提升了相机控制精度（FVD 222.1 vs 更高，TransErr 12.98 vs 更差）。这一结果支持了设计假设：相机运动引起的全局视角变化本质上是帧间时间动态，时间注意力层是处理此类信号的天然位置。

**注入范围的选择（Table 4）。** 将相机特征同时注入 U-Net 的编码器和解码器，相比仅注入一侧能进一步降低 TransErr 和 RotErr，表明多尺度、双向的相机特征融合对于精确控制是必要的。

### 4. 适用边界与限制

CameraCtrl 的适用边界受以下因素制约：

**极端相机运动的失效。** 对于旋转角度过大的相机轨迹（如 100° 垂直旋转、150° 水平旋转），CameraCtrl 无法准确生成对应视角（见 Figure 20）。这是因为训练集 RealEstate10K 的相机姿态分布以室内外漫游为主，缺乏极端旋转样本。该限制本质上是数据分布外推能力的不足，而非方法本身的根本缺陷。

**评估指标的固有误差。** TransErr 和 RotErr 依赖 COLMAP 进行地面真值估计，而 COLMAP 自身存在不可消除的估计误差。在 RealEstate10K 测试集上，TransErr 的下限约为 6.93，RotErr 的下限约为 1.02（见 Table 5）。这意味着即使完美控制，指标也无法降至零，在解读定量结果时需考虑这一噪声基底。

**对精确相机参数的依赖。** CameraCtrl 需要输入精确的相机参数序列（内参 $\mathbf{K}$ 和外参 $\mathbf{R}, \mathbf{t}$），对于无已知相机姿态的真实视频无法直接应用。这限制了其在非受控场景下的即插即用能力。

**外观泛化的局限。** 尽管 Plücker 嵌入减少了外观泄露，CameraCtrl 在泛化到与 RealEstate10K 视觉差异巨大的场景时可能仍存在性能下降。其控制能力受限于基础视频扩散模型的先验知识——如果基座模型对某类场景的生成质量本身较差，相机控制的精度也会受到影响。

### 5. 开放问题

CameraCtrl 的工作为视频生成中的相机控制开辟了新的技术路径，但也留下了若干值得深入探索的开放问题：

1. **数据分布扩展。** 如何获取或生成具有更大相机姿态分布（尤其是大角度旋转、快速变向）的训练数据，以突破 RealEstate10K 的分布限制？初步实验表明，添加 ACID 等小数据集联合训练未能提高控制精度，这暗示数据多样性可能比数据量更为关键，但具体的平衡机制尚不明确。

2. **内参动态控制。** 当前 CameraCtrl 仅控制外参（旋转和平移），能否将其扩展到同时控制相机内参变化（如动态焦距、主点偏移），以实现变焦、镜头畸变等电影级效果？这需要重新设计相机表示以编码内参的动态变化。

3. **无监督/自监督扩展。** 如何在没有已知相机参数的真实视频上训练相机控制模块？借助 NeRF 或 SfM 技术提取伪监督信号是一条可能的路径，但如何保证伪标签的精度和一致性仍是一个挑战。

4. **运动解耦。** 在复杂动态场景中，相机运动与物体运动相互纠缠，如何实现更精细的运动解耦，使模型能够独立控制相机视角而不影响场景中的物体运动？这可能需要引入额外的运动分离机制或分层控制架构。

5. **与可控生成的融合。** CameraCtrl 已展示了与 SparseCtrl 等视觉控制器的初步协作能力（Figure 4），但如何系统性地将相机控制与内容控制（如布局、姿态、深度）统一到一个框架中，实现真正意义上的"全方位可控视频生成"，仍是一个开放的体系架构问题。



## 原文 PDF

![[paperPDFs/ICLR_2025/CameraCtrl_Enabling_Camera_Control_for_Text_to_Video_Generation.pdf]]
