---
title: "POLAR: A Portrait OLAT Dataset and Generative Framework for Illumination-Aware Face Modeling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/POLAR_A_Portrait_OLAT_Dataset_and_Generative_Framework_for_Illumination_Aware_Face_Modeling.pdf
project_link: "https://rex0191.github.io/POLAR/"
code_link: null
aliases:
- POLAR
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入公开的大规模POLAR数据集，并提出方向条件的流式生成模型POLARNet，从单张均匀光照肖像直接预测每灯OLAT响应，从而绕过物理采集限制。
primary_logic: 将光照变化建模为潜在空间中方向条件驱动的连续物理传输过程（Latent Bridge Matching），而非随机噪声扩散，在保持身份的同时学习方向感知的光传输模式；生成的OLAT图像通过线性组合可实现任意HDR环境的物理一致重光照，形成数据捕获与模型生成相互促进的闭环。
claims:
- POLARNet采用流式潜在桥匹配，从单张均匀光肖像一步生成方向准确的OLAT响应。
- POLAR数据集包含220名受试者、156个光源方向、32个视角、16种表情，总计28.8M张4K图像，为目前最大规模的开源OLAT人脸数据集。
- 在定量比较中，提出方法在LPIPS（0.115）和PSNR（22.12）上均超越SwitchLight、IC-Light、DreamLight等主流方法。
- 基于物理的OLAT重光照在环境旋转消融实验中保持一致的阴影和高光移动，而背景条件方法出现不一致。
---

# POLAR: A Portrait OLAT Dataset and Generative Framework for Illumination-Aware Face Modeling

> [!tip] 核心洞察
> 将光照变化建模为潜在空间中方向条件驱动的连续物理传输过程（Latent Bridge Matching），而非随机噪声扩散，在保持身份的同时学习方向感知的光传输模式；生成的OLAT图像通过线性组合可实现任意HDR环境的物理一致重光照，形成数据捕获与模型生成相互促进的闭环。

| 字段 | 内容 |
|------|------|
| 中文题名 | POLAR：面向光照感知人脸建模的肖像OLAT数据集与生成框架 |
| 英文题名 | POLAR: A Portrait OLAT Dataset and Generative Framework for Illumination-Aware Face Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13192) · [Project](https://rex0191.github.io/POLAR/) |
| Topic | #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/generative_models_diffusion/diffusion_image_video |
| Method | POLARNet |
| Dataset | POLAR relit portraits test set |

> [!tip] 效果简介
> - POLAR relit portraits test set 上，LPIPS↓ 0.115 vs SwitchLight: 0.168 (-0.053)；PSNR↑ 22.12 vs SwitchLight: 20.69 (+1.43)；SSIM↑ 0.82 vs SwitchLight: 0.84 (-0.02)。

## 概述

**核心问题**：大规模、物理一致的人脸OLAT（One-Light-at-a-Time）光照数据的稀缺性，长期制约着肖像重光照模型的发展与泛化能力。现有OLAT数据集规模有限、缺乏开源，基于物理的采集成本极高，使得数据驱动方法难以获得充分的训练支撑。

**核心洞察**：本文构建了一个“数据捕获—模型生成”相互促进的闭环（Figure 2）：一方面推出POLAR——目前最大规模的开源OLAT人脸数据集；另一方面提出POLARNet，一种方向条件的流式生成模型，从单张均匀光照肖像直接预测每灯OLAT响应，从而绕过物理采集限制。POLARNet将光照变化建模为潜在空间中方向条件驱动的连续物理传输过程（Latent Bridge Matching），而非传统扩散模型的随机噪声去噪，在保持身份的同时学习方向感知的光传输模式。

**方法定位**：POLARNet采用流式潜在桥匹配范式，以光源方向向量经正弦位置编码作为条件，通过VAE编码器-解码器与条件U-Net速度网络实现一步推理。训练目标融合速度场损失、身份保持损失（ArcFace）、能量感知像素损失与能量正则，确保生成OLAT图像的物理一致性与身份保真。生成的OLAT图像通过线性组合可实现任意HDR环境下的物理一致重光照。

**主要结果**：
- **数据集**：POLAR包含220名受试者、156个光源方向、32个视角、16种表情，总计28.8M张4K图像，全面开源（Table 1）。
- **定量性能**：在POLAR重光照测试集上，POLARNet在LPIPS（0.115）和PSNR（22.12）上均超越SwitchLight、IC-Light、DreamLight等主流方法（Table 2）。SSIM指标（0.82）略低于SwitchLight（0.84），需注意该指标并非全面占优。
- **物理一致性**：在环境旋转消融实验中，基于物理的OLAT重光照保持一致的阴影和高光移动，而背景条件方法出现光照伪影和不连续（Figure 8）。
- **能量感知损失消融**：去除能量感知加权和能量一致性项后，模型过度拟合低强度区域，输出偏暗且高光对比度丢失；添加后能保持全局曝光并恢复高光细节（Figure 9）。

**局限与开放问题**：生成的OLAT图像可能丢失高频细节（尤其在镜面高光和阴影边界）；在极端面部姿态或光照条件下性能下降；去光照预处理模块尚未完全成熟，可能移除细微身份特征。未来方向包括扩展至视频OLAT合成、增强去光照的鲁棒性、结合3D几何先验提升极端姿态下的生成质量，以及促进光照感知的数字人渲染等下游任务。

## 背景与动机

### 问题背景：人脸重光照的数据瓶颈

在视觉特效、数字人和视频会议等应用中，对人脸肖像进行任意环境光照下的物理一致重光照是一个长期目标。实现这一目标的核心技术路径是**光传输矩阵（OLAT, One-Light-at-A-Time）**：逐次点亮不同方向的光源，记录人脸在每个单灯下的反射响应，然后将这些响应按目标环境图线性组合，合成任意光照下的肖像。

然而，高质量OLAT数据的获取极度依赖昂贵的**Light Stage**球形灯光阵列设备，采集过程耗时且受控。这导致两个连锁困境：

1. **数据稀缺**：现有OLAT风格的人脸数据集在受试者数量、视角数、表情多样性和分辨率上均严重受限，且大多不开源。
2. **模型泛化受限**：数据匮乏直接制约了光照感知生成模型的发展，现有方法难以学习到覆盖广泛身份、姿态和表情的光传输模式。

### 现有方法缺口

当前主流的人脸重光照方法可归为两类，各自存在明显局限：

- **基于物理本征分解的方法**（如SwitchLight）：将输入图像分解为反照率、法向、粗糙度等物理分量，再重新渲染。这类方法依赖分解精度，在复杂材质或极端光照下容易产生伪影，且无法显式建模全局光传输效应。
- **背景条件扩散方法**（如IC-Light、DreamLight）：以目标HDR环境图作为条件，通过扩散模型直接生成重光照结果。这类方法缺乏对每个光源方向独立响应的显式建模，导致在环境光旋转等场景下出现**照明不一致**——阴影和高光的移动不符合物理规律，而是被外观驱动的统计相关性所主导。

更根本的问题在于：**大规模、物理一致的人脸OLAT光照数据的稀缺性，构成了整个领域发展的瓶颈**。没有足够的数据，模型无法学习到真正的光传输物理；而没有好的生成模型，又无法低成本地扩展数据。这是一个典型的“先有鸡还是先有蛋”的闭环困境。

### 本文动机

针对上述困境，本文的核心动机是**打破数据与模型之间的负反馈循环，构建一个数据捕获与模型生成相互促进的正向闭环**。具体而言：

- **数据侧**：构建并开源**POLAR数据集**——一个大规模、高质量的人脸OLAT数据集，包含220名受试者、156个光源方向、32个视角、16种表情，总计28.8M张4K图像，并提供校准后的HDR重光照真值。
- **模型侧**：提出**POLARNet**——一个方向条件的流式生成模型，从单张均匀光照肖像直接预测每个灯方向的OLAT响应。与扩散模型不同，POLARNet采用**潜在桥匹配（Latent Bridge Matching）**，将光照变化建模为潜在空间中方向条件驱动的连续物理传输过程，支持一步推理，在保持身份的同时学习方向感知的光传输模式。

通过这一“鸡生蛋”协同演化框架（Figure 2），OLAT数据指导模型学习光传输先验，而生成模型又能低成本扩展数据多样性，反哺下游任务，形成可规模化的光照感知人脸建模方案。

## 核心创新

POLARNet 的核心创新在于将人脸重光照问题从“背景条件扩散生成”重新定义为**方向条件的流式潜在桥匹配**，并依托大规模开源 POLAR 数据集，构建了一条从数据采集到模型生成相互增强的闭环路径。

### 1. 从扩散模型到流式潜在桥匹配

现有主流方法（如 **SwitchLight**、**IC-Light**、**DreamLight**）普遍采用扩散模型范式，从随机高斯噪声出发逐步去噪，或以背景图像为条件进行生成。这类方法存在两个固有问题：一是随机初始化导致生成过程不可控，难以保证身份一致性；二是背景条件方法在环境光旋转时容易出现照明伪影和不连续的高光移动。

POLARNet 改用**流式潜在桥匹配（Latent Bridge Matching, LBM）**，将光照变化建模为潜在空间中从均匀光肖像到目标 OLAT 图像的**连续物理传输过程**。具体而言，给定训练对 $(x_u, x_l^{(\theta,\phi)})$——均匀光肖像及其在方向 $(\theta,\phi)$ 下的 OLAT 响应——VAE 编码器 $E$ 将两者映射到潜在空间，得到端点 $z_u$ 和 $z_l$。潜在桥插值公式为：

$$z_t = (1-t) z_u + t z_l + \sigma \sqrt{t(1-t)} \epsilon$$

这一设计使得模型学习的是两个语义对齐端点之间的确定性与微量随机性结合的连续轨迹，而非从纯噪声出发。速度网络 $v_\theta$（条件 U-Net）以光源方向编码 $c_{\mathrm{dir}} = (\sin\theta, \cos\theta, \sin\phi, \cos\phi)$ 为条件，预测潜在漂移速度，训练目标为：

$$\mathcal{L}_{\mathrm{LBM}} = \mathbb{E}_{t,\epsilon} \big[ \| v_\theta(z_t, t, c_{\mathrm{dir}}) - (z_l - z_t)/(1-t) \|_2^2 \big]$$

推理时，仅需**一步前向传输**即可从 $z_u$ 到达方向特定的 $z_l$，经解码器 $D$ 重建出该方向的 OLAT 图像。这从根本上区别于扩散模型的多步去噪，实现了高效的物理一致生成。

### 2. 方向条件替代背景条件

传统方法以背景图像或 HDR 环境图作为条件输入，模型隐式地学习环境与肖像之间的光照映射。POLARNet 将条件输入替换为**显式的光源方向向量**，经正弦位置编码后注入速度网络。这一设计使模型直接学习方向感知的光传输模式，而非依赖背景图像的间接线索。消融实验（Figure 8）表明，在 HDR 环境旋转下，基于物理的 OLAT 重光照能保持一致的阴影移动和高光变化，而背景条件方法则出现明显不一致。

### 3. 多层级损失设计保障身份与曝光一致性

POLARNet 的训练目标在 LBM 损失之上叠加了三项关键正则化：

- **身份损失** $\mathcal{L}_{\mathrm{id}} = \| f_{\mathrm{id}}(D(z_t)) - f_{\mathrm{id}}(D(z_0)) \|_1$：利用 ArcFace 特征约束生成人脸的身份一致性，防止光照变化导致面部特征漂移。
- **能量感知像素损失** $\mathcal{L}_{\mathrm{pix}} = \| w \odot (\hat{I}_{\mathrm{olat}} - I_{\mathrm{olat}}) \|_1$，其中 $w(x) = \min(1, \kappa I_{\mathrm{olat}}(x)/\bar{I}_{\mathrm{olat}})$：按相对亮度加权，抑制暗区噪声的同时强调高光区域细节。
- **能量正则化** $\mathcal{L}_{\mathrm{energy}} = \left\| \frac{\|\hat{I}_{\mathrm{olat}}\|_1}{\|I_{\mathrm{olat}}\|_1} - 1 \right\|_1$：强制预测图像与真值之间全局曝光一致，防止亮度漂移。

总体训练目标为：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{LBM}} + \lambda_{\mathrm{id}}\mathcal{L}_{\mathrm{id}} + \lambda_{\mathrm{pix}}\mathcal{L}_{\mathrm{pix}} + \lambda_{\mathrm{energy}}\mathcal{L}_{\mathrm{energy}}$$

消融实验（Figure 9）证实，去除能量感知加权和能量一致性项后，模型过度拟合低强度区域，输出整体偏暗且高光对比度丢失；添加后能保持全局曝光并恢复高光细节。

### 4. 数据与模型协同演化的闭环

POLAR 数据集（220 名受试者、156 个光源方向、32 个视角、16 种表情，共 28.8M 张 4K 图像）是目前最大规模的开源 OLAT 人脸数据集。POLARNet 从单张均匀光肖像生成每灯 OLAT 响应后，通过线性组合即可实现任意 HDR 环境下的物理一致重光照：

$$I_E \approx \sum_i w_i I_i, \quad w_i = \int_{\Omega_i} E(\mathbf{l}) d\mathbf{l}$$

这一“数据采集→模型学习→生成扩展→反哺下游任务”的闭环（Figure 2），使得数据稀缺瓶颈被模型生成能力所弥补，形成可扩展的人脸光照建模范式。

**需要手动验证**：定量表中 SSIM 指标（Ours: 0.82 vs. SwitchLight: 0.84）并未达到最高，但论文正文声称“highest structural similarity”，存在表述不一致，建议读者核实原始数据。

## 整体框架

POLAR 提出了一套“数据采集—模型生成—下游应用”相互促进的闭环框架，其核心思想是 **以大规模物理一致的人脸 OLAT 数据驱动生成模型，再以生成模型扩展数据多样性，反哺下游任务**（Figure 2）。

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our “chicken-and-egg” co-evolution loop, where OLAT data guide model learning, and the generative model expands data diversity to benefit downstream tasks*

### 数据流与模块关系

整个 pipeline 由两个关键阶段构成：

1. **POLAR 数据集构建阶段**：通过定制的 Light Stage（156 个 LED 光源 + 32 个同步相机，Figure 3）采集 220 名受试者在 16 种表情下的 OLAT 原始数据，经自动抠图、漫反射-镜面反射分离、光锥采样等后处理，合成大规模 HDR 重光照肖像。这一阶段为模型训练提供了配对监督信号。

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/003_Figure_3.jpg]]
*Figure 3: Our Light Stage consists of 156 LEDs and 32 synchronized cameras uniformly covering the full sphere. Each light is sequentially activated to produce OLAT captures*

2. **POLARNet 生成与重光照阶段**（Figure 5）：给定单张均匀光照肖像，模型在潜在空间中完成方向条件的光输运过程，一步生成对应光源方向的 OLAT 响应图像；随后通过线性组合模块，将生成的 OLAT 图像按任意 HDR 环境图加权求和，得到物理一致的重光照结果。

### 输入输出流

- **输入**：单张均匀光照的人脸肖像 $I_{\text{uni}}$，以及目标光源方向向量 $c_{\text{dir}} = (\sin\theta, \cos\theta, \sin\phi, \cos\phi)$。
- **核心变换**：VAE 编码器 $E$ 将输入肖像和目标 OLAT 图像分别映射到潜在空间，得到端点 $z_u$ 和 $z_l$；条件 U-Net（速度网络 $v_\theta$）在潜在桥 $z_t = (1-t) z_u + t z_l + \sigma\sqrt{t(1-t)}\epsilon$ 上预测漂移速度，通过一步前向积分将 $z_u$ 输运至 $\hat{z}_l$；VAE 解码器 $D$ 将 $\hat{z}_l$ 重建为 OLAT 图像 $\hat{I}_{\text{olat}}(\mathbf{L})$。
- **输出**：指定光源方向下的 OLAT 响应图像；进一步通过线性组合 $I_E \approx \sum_i w_i I_i$ 或漫反射-镜面反射分离组合 $I_E \approx \alpha \sum_i w_i^{\text{diff}} I_i + (1-\alpha) \sum_i I_i \odot w_i^{\text{spec}}$，合成任意 HDR 环境光照下的重光照肖像。

### 关键设计逻辑

与扩散模型从随机噪声去噪不同，POLARNet 采用 **流式潜在桥匹配（Latent Bridge Matching）**，直接在均匀光潜在与目标 OLAT 潜在之间建立连续的方向条件输运轨迹。这一设计的因果逻辑在于：光照变化本质上是物理输运过程，而非随机生成——方向条件驱动潜在沿确定性的桥路径移动，既保持身份一致性，又学习方向感知的光传输模式。训练时通过速度场损失 $\mathcal{L}_{\text{LBM}}$ 最小化预测速度与目标漂移的差异，推理时仅需一步前向即可完成生成，兼顾效率与物理一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/001_Figure_1.jpg]]
*Figure 1: POLAR captures high-resolution OLAT facial data with diverse subjects and expressions, from which we synthesize largescale HDR-relit portraits. POLARNet further learns to generate per-light OLAT responses from a single portrait, enabling scalable and physically consistent relighting under arbitrary HDR environments. Our project page: https://rex0191.github.io/POLAR/*

## 核心模块与公式推导

POLARNet 的核心设计思想是将光照变化建模为潜在空间中方向条件驱动的连续物理传输过程，而非从随机噪声出发的扩散生成。整个框架由四个关键模块构成：VAE 潜在编解码器、条件 U-Net 速度网络、潜在桥匹配训练机制，以及 OLAT 线性组合重光照模块。

### VAE 潜在编解码器 (E, D)

为降低计算开销并在语义对齐的紧凑空间中建模光照传输，POLARNet 采用一个轻量变分自编码器将图像映射到潜在空间。编码器 $E$ 将均匀光照肖像 $x_u$ 和目标 OLAT 图像 $x_l$ 分别映射为潜在变量 $z_u$ 和 $z_l$，解码器 $D$ 则负责从潜在变量重建图像。这一设计使后续的光传输学习在低维、语义对齐的潜在空间中进行，避免了像素空间的高维冗余。

### 潜在桥匹配 (Latent Bridge Matching, LBM)

与扩散模型从高斯噪声逐步去噪不同，POLARNet 在均匀光潜在 $z_u$ 与目标 OLAT 潜在 $z_l$ 之间定义一条连续插值路径，称为“潜在桥”。给定时间步 $t \in [0,1]$，桥上的中间潜在变量定义为：

$$z_t = (1-t) z_u + t z_l + \sigma \sqrt{t(1-t)} \epsilon$$

其中 $\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$\sigma$ 控制随机性强度。当 $t=0$ 时 $z_t$ 接近均匀光潜在，$t=1$ 时接近目标 OLAT 潜在。训练目标是学习一个速度场 $v_\theta$，使其预测的漂移速度与真实漂移方向一致。LBM 损失函数为：

$$\mathcal{L}_{\mathrm{LBM}} = \mathbb{E}_{t,\epsilon} \big[ \| v_\theta(z_t, t, c_{\mathrm{dir}}) - (z_l - z_t)/(1-t) \|_2^2 \big]$$

其中 $c_{\mathrm{dir}} = (\sin\theta, \cos\theta, \sin\phi, \cos\phi)$ 为光源方向的四维正弦位置编码，$(z_l - z_t)/(1-t)$ 表示从当前点 $z_t$ 指向目标 $z_l$ 的真实漂移速度。通过最小化该损失，速度网络学会在任意中间时刻将潜在变量推向正确的光照方向。

### 条件 U-Net 速度网络 ($v_\theta$)

速度网络 $v_\theta$ 采用条件 U-Net 架构，以当前潜在变量 $z_t$、时间步 $t$ 和光源方向编码 $c_{\mathrm{dir}}$ 为输入，输出潜在空间中的漂移速度。训练完成后，推理阶段仅需一步前向传播：从均匀光潜在 $z_u$ 出发，令 $t=0$，计算 $\hat{z}_l = z_u + v_\theta(z_u, 0, c_{\mathrm{dir}})$，再经解码器 $D$ 即可生成对应方向的 OLAT 图像。这实现了单步、方向准确的光响应生成。

### 多任务训练目标

除 LBM 损失外，POLARNet 引入三项辅助损失以保证生成质量。身份保持损失利用 ArcFace 特征约束解码人脸的身份一致性：

$$\mathcal{L}_{\mathrm{id}} = \| f_{\mathrm{id}}(D(z_t)) - f_{\mathrm{id}}(D(z_0)) \|_1$$

能量感知像素损失按相对亮度加权像素误差，抑制暗区噪声并强调高光细节：

$$\mathcal{L}_{\mathrm{pix}} = \| w \odot (\hat{I}_{\mathrm{olat}} - I_{\mathrm{olat}}) \|_1, \quad w(x) = \min(1, \kappa I_{\mathrm{olat}}(x)/\bar{I}_{\mathrm{olat}})$$

能量正则化强制预测与真值之间全局曝光一致，防止亮度漂移：

$$\mathcal{L}_{\mathrm{energy}} = \left\| \frac{\|\hat{I}_{\mathrm{olat}}\|_1}{\|I_{\mathrm{olat}}\|_1} - 1 \right\|_1$$

总体训练目标为上述损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{LBM}} + \lambda_{\mathrm{id}}\mathcal{L}_{\mathrm{id}} + \lambda_{\mathrm{pix}}\mathcal{L}_{\mathrm{pix}} + \lambda_{\mathrm{energy}}\mathcal{L}_{\mathrm{energy}}$$

### OLAT 线性组合重光照

生成所有光源方向的 OLAT 响应后，利用漫反射的线性叠加性质，通过加权求和即可合成任意 HDR 环境光照下的重光照肖像。基础线性重光照公式为：

$$I_E \approx \sum_i w_i I_i, \quad w_i = \int_{\Omega_i} E(\mathbf{l}) d\mathbf{l}$$

其中 $I_i$ 为第 $i$ 个光源的单灯光响应，$w_i$ 为环境图 $E(\mathbf{l})$ 在对应立体角 $\Omega_i$ 内的积分权重。为进一步提升真实感，POLAR 引入漫反射-镜面反射分离策略：

$$I_E \approx \alpha \sum_i w_i^{\mathrm{diff}} I_i + (1-\alpha) \sum_i I_i \odot w_i^{\mathrm{spec}}$$

其中 $\alpha$ 为场景依赖的混合系数，$\odot$ 表示逐元素乘法。该分离处理有效避免了全局色彩偏差，使高光移动和阴影变化更加物理一致。

### 补充图表

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/006_Figure_5.jpg]]
*Figure 5: Overview of our flow-based OLAT data generation framework. Given a uniformly lit portrait, the encoder–decoder pair (E, D) maps both the input and its target OLAT image into latent space. Latent Bridge Matching learns a continuous, direction-conditioned transport between these endpoints, supervised by the velocity field loss*

## 实验与分析

### 主结果：定量与定性比较

POLARNet在POLAR数据集的合成重光照肖像测试集上，与三类代表性方法进行了定量对比：基于物理本征分解的**SwitchLight**、以及背景条件扩散方法**IC-Light**和**DreamLight**。如表2所示，POLARNet在感知质量和信号保真度上取得显著优势——LPIPS降至0.115，PSNR达到22.12 dB，分别较SwitchLight提升0.053和1.43 dB。在结构相似性SSIM上，POLARNet（0.82）略低于SwitchLight（0.84），但正文称其取得了“最高的结构相似性”，此处存在表述不一致，需读者注意。

定性结果（Figure 6）进一步揭示了不同方法在真实场景重光照中的行为差异。在给定同一张均匀光肖像和HDR环境图的情况下，POLARNet生成的OLAT响应序列展现出方向一致的阴影移动和高光变化，最终合成的重光照结果与真实OLAT数据渲染的参考图像高度吻合。相比之下，SwitchLight在极端光照方向下易出现本征分解误差导致的色彩偏移；IC-Light和DreamLight虽能生成视觉上可接受的结果，但其光照效果更多依赖于背景条件图中的外观线索，而非物理方向信息，导致阴影和高光的位置与环境光方向不完全一致。

Figure 7展示了生成OLAT与真实捕获OLAT的直接对比。在单灯光源条件下，POLARNet预测的OLAT图像在面部整体明暗分布、镜面高光位置和阴影投射方向上与真实数据高度一致，但在高频细节（如发丝级阴影、皮肤微结构高光）上仍存在可察觉的退化。当将这些生成OLAT按HDR环境图线性组合后，合成肖像在全局光照氛围和局部明暗过渡上与真实OLAT合成结果保持良好的一致性，验证了生成OLAT的物理可用性。

### 消融实验

**物理一致性验证（Figure 8）。** 为验证基于OLAT的重光照是否真正遵循物理光照规律，论文设计了一个环境光旋转实验：将HDR环境图逐步旋转，观察重光照结果中阴影和高光的移动是否与光源方向变化一致。POLARNet的物理OLAT重光照表现出连续的阴影移动和一致的高光位置变化，与真实物理过程吻合。而背景条件方法（IC-Light、DreamLight）在环境图旋转时，重光照结果的光影变化出现不连续或方向不一致的伪影——这是因为这些方法将环境图作为整体条件输入，并未显式建模光源方向与表面响应的对应关系，导致其输出更多受训练数据中的外观统计驱动，而非物理约束。

**能量感知损失消融（Figure 9）。** 去除能量感知加权项和能量一致性正则项后，模型出现两个典型退化模式：其一，网络过度拟合低强度区域（如阴影区），导致整体输出偏暗，高光区域的对比度和细节明显丢失；其二，全局曝光水平不稳定，不同光源方向下的预测亮度漂移。引入能量感知像素损失后，模型通过按相对亮度加权的L1损失，强制网络关注高光区域的细节重建；能量一致性正则则约束预测图像的总能量与真值一致，防止全局亮度偏移。消融结果证实，这两项设计对于保持高动态范围OLAT图像的曝光准确性和高光保真度至关重要。

**失败模式分析（Figure F，附录）。** 论文在附录中明确展示了一个关键失败模式：当输入肖像本身带有不均匀光照（如侧光或强阴影）时，POLARNet预测的OLAT图像会纠缠输入图像中已有的光照信息，导致生成的单灯光响应出现偏差——原本应均匀变化的阴影和高光被输入光照“污染”，产生不一致的光输运模式。为解决此问题，论文引入了一个去光照预处理模块，将输入肖像归一化至光照中性的外观。经过去光照处理后，模型能够生成更准确的OLAT响应。然而，论文同时指出该去光照模块尚未完全成熟，在某些情况下可能移除细微的身份特征（如眼窝深度、鼻梁轮廓等由光影塑造的几何线索），这是当前方法的一个已知局限。

### 公平性讨论

需要指出，上述定量评估仅在POLAR数据集的自有测试划分上进行，未在公开独立基准（如其他OLAT数据集或真实拍摄的重光照测试集）上与其他方法进行公平对比。由于POLARNet在POLAR数据分布上训练，而对比方法可能未使用该数据集，因此报告的数值优势可能部分源于训练域匹配带来的性能增益，而非方法本身的绝对优越性。此外，SSIM指标上的表述不一致提示读者在引用该结论时需审慎核实。

### 补充图表

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison with state-of-the-art imagebased relighting methods*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/005_Table_1.jpg]]
*Table 1: Comparison of POLAR with existing OLAT-style face datasets. For Accessibility, ✓and ✗ indicate whether the dataset is or is not open source, while ◦ means partially open source. POLAR uniquely combines large-scale OLAT captures, calibrated HDR-relit portraits, and full open-source availability, offering a more complete resource for illumination learning*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/009_Figure_8.jpg]]
*Figure 8: Comparison of relighting consistency under environment rotation. Our Physical OLAT-based relighting preserves consistent shading and highlight movement, while background-conditioned methods show appearance-driven inconsistencies*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/011_Figure_9.jpg]]
*Figure 9: Ablation study on energy and uncertainty-aware loss*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/010_Figure_7.jpg]]
*Figure 7: Comparison between generated and captured OLAT data, and their corresponding environment-lit synthesis results. The top part shows OLAT images produced by our model compared with the captured OLAT data. The bottom part presents relit portraits synthesized using the generated OLATs and real OLAT captures under different environment illuminations*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/007_Figure.jpg]]

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/019_Figure.jpg]]
*Figure: H. Generated OLAT sequence of test set by our POLARNet (selected 48 frontal LEDs)*

![[assets/figures/papers/paper_list_l2046_https_arxiv_org_abs_2512_13192/figures/020_Figure.jpg]]
*Figure: I. Generated OLAT sequence of in-the-wild portraits by our POLARNet (selected 48 frontal LEDs)*

## 方法谱系与知识库定位

### 1. 问题定位：OLAT光照数据的稀缺与物理一致性瓶颈

人脸重光照（Portrait Relighting）的核心挑战在于，如何从单张输入图像合成任意新光照环境下物理一致的外观。现有方法大致分为两条技术路径：

- **基于物理本征分解的方法**：将输入图像分解为法向、漫反射率、镜面反射率、环境遮蔽等本征层，再根据新光照重新合成。代表工作如 **SwitchLight**，其优势在于物理可解释性，但在复杂材质（如皮肤半透明、细发高光）下分解精度有限，且高度依赖训练数据的物理准确性。
- **背景条件扩散生成方法**：将目标光照信息（如HDR环境图或背景图像）作为条件输入扩散模型，直接生成重光照结果。代表工作如 **IC-Light** 和 **DreamLight**。这类方法在视觉质量上表现优异，但生成过程缺乏物理约束，容易在环境光旋转时出现阴影/高光移动不一致的伪影（见Figure 8）。

**核心瓶颈**：上述两类方法均受限于大规模、物理一致的人脸OLAT（One-Light-at-A-Time）光照数据的稀缺性。OLAT数据是训练物理感知重光照模型的理想监督信号，但现有公开OLAT人脸数据集在受试者数量、光源密度、视角多样性、表情覆盖和分辨率上均存在明显不足（见Table 1）。这一数据瓶颈直接制约了模型对复杂光传输效应的学习与泛化。

### 2. 核心因果机制：数据与模型协同演化的闭环

POLAR工作的核心洞察是构建一个**数据捕获与模型生成相互促进的闭环**（Figure 2），从根本上突破上述瓶颈：

1. **大规模物理数据捕获**：构建POLAR数据集——220名受试者、156个LED光源方向、32个同步相机视角、16种表情，总计28.8M张4K分辨率的OLAT图像，并开源发布。这为光照建模提供了目前最大规模的物理一致训练和评估基准。
2. **方向条件的流式生成模型POLARNet**：从单张均匀光照肖像出发，通过潜在桥匹配（Latent Bridge Matching）学习光源方向到OLAT响应的连续物理传输过程，实现一步推理生成每灯响应。
3. **物理一致重光照合成**：生成的OLAT图像通过线性组合（漫反射-镜面反射分离策略）可渲染任意HDR环境下的重光照结果，形成“数据→模型→合成数据→下游任务”的正反馈循环。

这一闭环的关键创新在于：**将光照变化建模为潜在空间中方向条件驱动的连续物理传输，而非随机噪声扩散**。与扩散模型从高斯噪声出发逐步去噪不同，POLARNet的潜在桥匹配在语义对齐的均匀光潜变量与目标OLAT潜变量之间建立确定性路径，从而在保持身份一致性的同时，学习方向感知的光传输模式。

### 3. 方法谱系中的关键差异点

| 维度 | 扩散重光照方法 (IC-Light, DreamLight) | 物理分解方法 (SwitchLight) | **POLARNet (本文)** |
|------|--------------------------------------|---------------------------|---------------------|
| **生成范式** | 扩散模型（噪声→图像去噪） | 本征分解→物理合成 | 流式潜在桥匹配（连续传输，一步推理） |
| **条件输入** | 背景图像或HDR环境图 | 法向/材质/光照参数 | 光源方向向量 $(\sin\theta, \cos\theta, \sin\phi, \cos\phi)$，经正弦位置编码 |
| **物理一致性** | 弱（外观驱动，环境旋转时出现不一致） | 强（受限于分解精度） | 强（OLAT线性组合保证物理一致性，Figure 8验证） |
| **身份保持** | 依赖扩散模型先验 | 依赖分解精度 | ArcFace身份损失显式约束（Eq. 5） |
| **训练监督** | 像素重建损失为主 | 本征层监督 | 速度场损失 + 身份损失 + 能量感知像素损失 + 能量正则（Eq. 8） |
| **推理效率** | 多步去噪 | 单步分解+合成 | 单步潜在传输 |

**能量感知损失设计**是另一个关键差异点。传统像素损失对所有区域等权处理，导致模型过度拟合低强度暗区，输出整体偏暗且高光细节丢失。POLARNet引入按相对亮度加权的能量感知像素损失（Eq. 6）和全局能量一致性正则（Eq. 7），强制网络在保持全局曝光的同时恢复高光区域细节。消融实验（Figure 9）证实，去除这些损失项后模型输出明显偏暗，高光区域对比度丢失。

### 4. 适用边界与局限性

尽管POLAR在数据规模和生成范式上取得了显著进展，其当前版本存在以下明确边界：

- **高频细节丢失**：生成的OLAT图像在镜面高光和阴影边界区域可能丢失高频细节，这源于VAE潜在空间的压缩瓶颈。
- **极端姿态与光照退化**：在极端面部姿态或极端光照条件下性能下降，模型训练数据覆盖的姿态和光照分布决定了其泛化上限。
- **去光照预处理不成熟**：为处理非均匀光照的in-the-wild输入，模型依赖去光照（delighting）预处理模块，但该模块可能移除细微身份特征（如雀斑、痣），导致身份信息损失（见Figure F）。
- **静态图像限制**：当前框架仅支持静态图像，未扩展至视频OLAT合成，无法保证时序一致性。

### 5. 开放问题与未来方向

基于上述局限性，可识别出以下开放研究问题：

1. **视频OLAT合成**：如何将潜在桥匹配框架扩展至视频域，实现时序一致的光照传输与重光照？这需要解决帧间潜变量平滑性和运动条件下的光传输建模问题。
2. **鲁棒去光照与身份保留**：如何在消除不均匀输入照明的同时，更鲁棒地保留被移除的细微身份特征？可能需要联合优化去光照与OLAT生成，而非级联处理。
3. **3D几何先验融合**：能否结合3D人脸几何先验（如3DMM或神经辐射场）进一步提升极端姿态下的生成质量？3D信息可提供更准确的可见性、法向和光传输约束。
4. **下游任务促进**：该数据集和模型是否能够促进光照感知的视频生成、数字人渲染、或面部识别在极端光照下的鲁棒性等下游任务？这需要进一步的跨任务验证。

> **公平性说明**：定量评估仅在POLAR数据集划分的测试集上进行，未在公开独立基准（如现有OLAT数据集或真实拍摄数据集）上与其他方法公平对比。SSIM指标上（Ours: 0.82 vs. SwitchLight: 0.84）并未达到最高，但论文正文声称“highest structural similarity”，可能存在不一致，需读者注意。

## 原文 PDF

![[paperPDFs/CVPR_2026/POLAR_A_Portrait_OLAT_Dataset_and_Generative_Framework_for_Illumination_Aware_Face_Modeling.pdf]]
