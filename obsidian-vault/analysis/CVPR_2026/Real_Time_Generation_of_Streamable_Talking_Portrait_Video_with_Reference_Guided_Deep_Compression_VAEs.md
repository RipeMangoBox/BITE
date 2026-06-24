---
title: Real-Time Generation of Streamable Talking Portrait Video with Reference-Guided Deep Compression VAEs
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Real_Time_Generation_of_Streamable_Talking_Portrait_Video_with_Reference_Guided_Deep_Compression_VAEs.pdf
project_link: null
code_link: null
aliases:
- RGCVVBARFT
- RTGSTPVRGDCV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在VAE解码器中注入可变数量的参考图像作为引导，使网络专注于动态信息提取而非静态外观重建；同时采用因果残差视频自编码（CR-VA）提升压缩质量。
primary_logic: 将肖像视频的静态外观（主体与背景）通过参考图像显式提供给解码器，可大幅提高深度压缩VAE的重建质量和压缩比（768倍），再结合分块自回归Rectified Flow Transformer实现低延迟流式生成。
claims:
- 视频压缩率达768，比流行视频扩散模型VAE高10-15倍
- 生成速度达42 FPS，超过现有扩散说话人视频生成模型25倍以上
- 参考引导使PSNR在HDTF上从28.306提升至32.068 (+3.762 dB)
- CR-VA与参考引导协同，PSNR增益从3.695 dB提升至4.375 dB（VoxCeleb2）
---

# Real-Time Generation of Streamable Talking Portrait Video with Reference-Guided Deep Compression VAEs

> [!tip] 核心洞察
> 将肖像视频的静态外观（主体与背景）通过参考图像显式提供给解码器，可大幅提高深度压缩VAE的重建质量和压缩比（768倍），再结合分块自回归Rectified Flow Transformer实现低延迟流式生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于参考引导深度压缩VAE的实时流式说话人像视频生成 |
| 英文题名 | Real-Time Generation of Streamable Talking Portrait Video with Reference-Guided Deep Compression VAEs |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Real-Time_Generation_of_Streamable_Talking_Portrait_Video_with_Reference-Guided_Deep_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Reference-Guided Causal Video VAE with Blockwise Autoregressive Rectified Flow Transformer |
| Dataset | HDTF, PortraitOneMin |

> [!tip] 效果简介
> - HDTF 上，SC / SD / CAPP / FVD_25 / FPS 8.943 / 6.286 / 0.699 / 62.300 / 42.3 vs Hallo / FantasyTalking / VASA-1 / EMO (参见Table 1) (SC最佳，FPS超过所有基线一个数量级以上)。
> - PortraitOneMin 上，SC / SD / CAPP / FVD_25 8.537 / 6.619 / 0.648 / 91.964 vs Hallo / FantasyTalking / VASA-1 / EMO (参见Table 1) (在大多数指标上达到或超越现有最佳方法)。

## 概述

**问题瓶颈**：现有大规模视频扩散模型（如 **Hallo**、**FantasyTalking**、**AniPortrait** 等）计算成本过高，无法支持实时交互式应用；同时，普通 VAE 压缩率低且未利用肖像视频中主体与背景的静态外观信息，导致生成效率与重建质量受限。

**核心洞察**：将肖像视频的静态外观通过参考图像显式注入 VAE 解码器，使网络专注于动态信息提取而非静态外观重建，可大幅提升深度压缩 VAE 的重建质量与压缩比。在此基础上，结合分块自回归 Rectified Flow Transformer 实现低延迟流式生成。

**方法定位**：本文提出 **Reference-Guided Causal Video VAE with Blockwise Autoregressive Rectified Flow Transformer**，包含两个关键模块——参考引导因果视频 VAE（含因果残差视频自编码 CR-VA）负责高压缩比潜空间学习，以及分块因果注意力 Rectified Flow Transformer 负责自回归潜变量生成。该框架将视频压缩率推至 **768 倍**（比流行视频扩散模型 VAE 高 10–15 倍），在单张 H100 GPU 上实现 **42 FPS** 的 512×512 流式生成，速度超过现有扩散说话人视频生成模型 **25 倍以上**。

**主要结果**：在 HDTF 和 PortraitOneMin 基准上，唇音同步（SC）、头部对齐（CAPP）与视频质量（FVD）等指标达到或超越现有最佳方法，同时推理速度领先一个数量级以上。消融实验表明，参考引导在 HDTF 上带来 **+3.762 dB** PSNR 增益，CR-VA 与参考引导协同可将增益进一步提升至 **+6.696 dB**。

## 背景与动机

### 问题背景：实时交互式肖像视频生成的效率困境

音频驱动的说话人像视频生成旨在根据语音信号合成逼真的人物肖像视频，其应用涵盖虚拟助手、数字人直播、视频会议等实时交互场景。这类应用对生成质量与推理延迟提出了双重严苛要求：不仅需要自然的唇音同步、丰富的面部表情与头部运动，还必须在极低延迟下完成高分辨率视频的流式输出。

近年来，扩散模型在通用视频生成领域取得了显著进展，但其在肖像视频生成中的实际部署仍面临根本性效率瓶颈。以 **Hallo**（Xu et al., arXiv 2024）、**FantasyTalking**（Wang et al., ACM MM 2025）、**AniPortrait**（Wei et al., arXiv 2024）等为代表的扩散式方法，虽然能够生成高质量结果，但其多步去噪过程导致计算成本过高，推理速度远不能满足实时交互需求。即便 **VASA-1**（Xu et al., NeurIPS 2024）等面向实时场景的优化方案，其生成速度与压缩效率仍存在显著提升空间。

### 现有方法缺口：VAE压缩率不足与静态信息冗余

当前大规模视频生成模型通常依赖变分自编码器（VAE）将视频从像素空间压缩到低维潜空间以降低计算开销。然而，两个核心问题制约了效率的进一步提升：

**第一，压缩率瓶颈。** 流行视频扩散模型的VAE压缩率普遍较低——例如，主流方案仅达到约48倍的时空压缩比。这意味着潜变量序列仍然包含大量冗余信息，导致后续生成网络需要处理高维表征，直接限制了推理速度的上限。

**第二，静态外观信息的浪费。** 肖像视频具有独特的结构特性：主体身份、背景环境等静态外观信息在整个视频中保持高度一致，真正需要动态建模的仅是唇部运动、表情变化、头部姿态等时变信号。然而，现有VAE将静态与动态信息不加区分地压缩到统一的潜变量中，迫使生成网络“重复学习”重建本可预先提供的静态内容。这种信息混合不仅降低了压缩效率，还增加了生成网络的建模负担。

### 本文动机：以参考引导实现极致压缩与流式生成

针对上述缺口，本文提出一种全新的技术路线：**将肖像视频的静态外观信息通过参考图像显式注入VAE解码器，使压缩网络能够专注于动态信息的提取，从而实现极端压缩比下的高质量重建。** 这一核心洞察源于对肖像视频本质结构的重新审视——既然静态外观（主体、背景）在参考图像中已经完整呈现，VAE的潜变量只需编码时变动态即可。

在此基础上，本文进一步采用**Rectified Flow Transformer**替代传统的随机扩散模型作为生成器范式。Rectified Flow通过常微分方程（ODE）模拟从噪声到干净潜变量的确定性路径，相比多步随机去噪过程具有更高的采样效率。结合分块自回归生成策略与KV缓存机制，该方法能够在单个GPU上实现42 FPS的512×512分辨率视频流式输出，推理速度超过现有扩散式方法25倍以上。

综合来看，本文的核心动机是通过“参考引导的深度压缩VAE”与“高效流式生成器”的协同设计，突破实时交互式肖像视频生成的效率与质量瓶颈，使高保真数字人应用真正具备实用化部署的可行性。

## 核心创新

本文的核心创新在于将**参考引导的深度压缩VAE**与**分块自回归Rectified Flow Transformer**协同，构建了一个可实时流式生成的说话人像视频框架。其关键突破体现在以下四个维度的“changed slots”上。

### 1. 视频VAE架构：从通用压缩到参考引导的因果残差压缩

现有视频扩散模型（如**Hallo**（Xu et al., arXiv 2024）、**EMO**（Tian et al., ECCV 2024）等）普遍采用标准非因果VAE，压缩率通常仅为48倍左右，且未利用肖像视频中主体与背景高度静态的先验。本文提出的**因果残差视频VAE（CR-VA）** 从两个层面实现了根本性改变：

- **因果残差编码**：将DC-AE的残差自编码范式扩展到视频域，采用分离的时空下/上采样与残差编码。第一帧独立处理以保持因果性（Figure 3），使VAE本身具备流式解码能力。
- **参考图像引导**：在解码器D₁将潜变量$\mathbf{z}$上采样至中级特征$\mathbf{f}_z$后，引入基于Transformer的融合网络$D_{ref}$，通过交叉注意力将可变数量的参考图像特征注入解码过程。这使得解码器专注于提取动态信息（唇动、表情、头部运动），而静态外观（身份、背景）由参考图像显式提供。

这一设计将视频压缩率推至**768倍**（空间64×、时间4×、潜变量通道64），比流行视频扩散模型VAE高出10–15倍。消融实验（Table 2）证实：参考引导在HDTF上带来**+3.762 dB PSNR**增益（单参考），且CR-VA与参考引导协同工作时，PSNR增益从4.843 dB进一步提升至**6.696 dB**（HDTF，M=3），验证了“静态外观显式注入”这一核心洞察的有效性。

### 2. 生成器范式：从随机扩散到Rectified Flow ODE模拟

传统说话人像生成方法（如**FantasyTalking**（Wang et al., ACM MM 2025）、**AniPortrait**（Wei et al., arXiv 2024））依赖多步随机扩散去噪，推理速度受限于数十至上百步的迭代采样。本文改用**Rectified Flow框架**，将生成过程形式化为求解ODE，用Transformer网络$G$逼近条件速度场：

$$\mathbb{E}_{t, \mathbf{z}^0, \epsilon, \mathbf{z}_r, \mathbf{a}'} \| G(\mathbf{z}^t, \mathbf{z}_r, \mathbf{a}', t) - (\epsilon^t - \mathbf{z}^0) \|_2^2$$

这一范式转换使生成过程从“逐步去噪”变为“沿直线路径从噪声流向干净潜变量”，大幅减少推理步数，为实时生成奠定基础。

### 3. 注意力机制：从双向注意力到分块因果注意力

为支持流式生成，本文将Transformer的注意力机制改为**分块因果注意力**（Figure 4）：将潜变量序列划分为大小为$k$的不重叠块，块内应用全自注意力，块间仅允许关注前序块。这既保留了长程时序建模能力，又使得推理时可复用前序块的KV缓存，避免重复计算。生成窗口设为32个潜变量帧（对应128视频帧），$k=4$，实现了低延迟的逐块自回归预测。

### 4. 训练策略：从标准扩散训练到Teacher-forcing加噪声增强

自回归生成训练中，本文采用**Teacher-forcing策略**：训练时以前序真实潜变量（而非预测值）为条件，并对真实潜变量施加高斯噪声增强，提升模型对推理时累积误差的鲁棒性。同时结合分类器自由引导，在采样时平衡生成质量与多样性。

### 创新协同效应

上述四个changed slots并非孤立改进，而是形成因果链条：**CR-VA提供高压缩比潜空间** → **参考引导降低解码器重建难度** → **Rectified Flow实现少步生成** → **分块因果注意力支持流式KV缓存**。最终，系统在单张H100 GPU上达到**42 FPS**的生成速度，超过现有扩散模型25倍以上（Table 1），同时唇音同步（SC 8.943）和头部对齐（CAPP 0.699）指标在HDTF上达到或超越现有最佳水平。

## 整体框架

本方法将说话人像视频生成分解为两个紧密协作的子任务：**紧凑潜变量生成**与**高效视频解码**。整体pipeline由两大核心模块串联构成——**参考引导因果视频VAE**（Reference-Guided Causal Video VAE）与**分块自回归Rectified Flow Transformer**，其架构总览见Figure 2。

### 输入输出流

给定一组参考图像 $\mathbf{r}$（至少一张，可多张）和一段语音音频 $\mathbf{a}$，系统以自回归方式逐块生成视频潜变量序列，再由VAE解码器实时重建出 $512\times512$ 的流式肖像视频 $\mathbf{y}$。整个过程可形式化为条件生成：

$$\mathbf{y} \sim p(\mathbf{y} \mid \mathbf{r}, \mathbf{a})$$

### 模块划分与数据流

**第一阶段：潜变量生成（Rectified Flow Transformer）**

生成器 $G$ 是一个基于Transformer的Rectified Flow网络，在VAE学习到的紧凑潜空间中建模条件速度场。它以参考图像的潜变量 $\mathbf{z}_r$ 和音频特征 $\mathbf{a}'$ 为条件，从高斯噪声出发，通过求解ODE逐步生成视频潜变量 $\mathbf{z}$。为实现流式输出，生成过程采用**分块因果注意力**（blockwise causal attention）：潜变量序列被划分为大小为 $k$ 的非重叠块，块内执行全自注意力，块间仅允许单向（前序块到当前块）注意力，并配合KV缓存复用历史上下文以降低推理开销。训练时采用teacher-forcing策略，以真实潜变量加高斯噪声增强作为条件，并引入分类器自由引导（classifier-free guidance）。

**第二阶段：视频解码（参考引导因果VAE）**

VAE采用两阶段对称编码器-解码器架构，并引入两项关键设计：

- **因果残差视频自编码（CR-VA）**：编码器 $E_1$ 执行时空下采样至中级特征，$E_2$ 进一步空间压缩得到潜变量 $\mathbf{z}$（空间下采样64倍，时间下采样4倍，潜通道数64，总压缩比达768）。解码器 $D_1$ 将 $\mathbf{z}$ 空间上采样至中级特征 $\mathbf{f}_z$，随后 $D_2$ 联合时空上采样重建视频帧。整个过程采用分离的时空残差编码，首帧独立处理以严格保持因果性（Figure 3）。

- **参考图像融合**：在 $D_1$ 与 $D_2$ 之间插入基于Transformer的融合模块 $D_{\text{ref}}$，通过交叉注意力将参考图像特征注入 $\mathbf{f}_z$。这使解码器能显式利用肖像视频的静态外观信息（主体身份、背景），从而专注于动态信息（唇动、表情、头部运动）的重建，大幅提升深度压缩下的重建质量。

### 流式推理

推理时，Rectified Flow Transformer逐块自回归预测潜变量，每生成一个窗口的潜变量即送入VAE解码器实时渲染为视频帧。一个生成窗口包含32个潜变量帧（对应128视频帧，首窗口为125帧），块大小 $k=4$。这一设计使系统在单张H100 GPU上达到**42 FPS**的生成速度，超过现有扩散模型25倍以上。

### 补充图表

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our framework. Left: The proposed reference-guided causal video VAE*

## 核心模块与公式推导

本节聚焦于构成该框架的两个核心组件：参考引导因果视频VAE（Reference-Guided Causal Video VAE）与分块自回归Rectified Flow Transformer。前者负责将高维视频压缩至极低维的潜空间，后者在该潜空间中进行高效的条件生成。

### 3.1 参考引导因果视频VAE

生成过程被分解为两个子任务：在音频条件下生成紧凑潜表示 $\mathbf{z}$，以及将 $\mathbf{z}$ 解码为最终视频 $\mathbf{y}$。整个条件视频生成问题可表述为：

$$\mathbf{y} \sim p(\mathbf{y} \mid \mathbf{r}, \mathbf{a})$$

其中 $\mathbf{r}$ 为参考图像集，$\mathbf{a}$ 为音频条件。VAE采用因果两阶段对称架构，如图2左侧所示：

- **编码阶段**：编码器 $E_1$ 执行时空下采样至中级别特征；$E_2$ 进一步进行空间压缩，得到潜变量 $\mathbf{z}$。整体空间下采样倍率为64，时间下采样倍率为4，潜通道维度为64，综合压缩率达768。
- **解码阶段**：解码器 $D_1$ 将 $\mathbf{z}$ 上采样至中级别特征 $\mathbf{f}_z$；随后基于Transformer的融合网络 $D_{\text{ref}}$ 通过交叉注意力机制注入参考图像特征；最后 $D_2$ 联合时空上采样重建视频帧。

该VAE的关键创新在于**因果残差视频自编码（CR-VA）**：将DC-AE的残差自编码范式扩展至因果视频VAE，采用分离的时空下/上采样与残差编码，首帧独立处理以保持因果性（见图3）。VAE的训练损失为：

$$\mathbb{E}_{\hat{\mathbf{y}}} \left[ \lambda_1 \| \hat{\mathbf{y}} - \mathbf{y} \|_1 + \lambda_2 \mathrm{LPIPS}(\hat{\mathbf{y}}, \mathbf{y}) \right]$$

该损失结合L1距离与LPIPS感知损失，用于优化重建质量。

### 3.2 分块自回归Rectified Flow Transformer

在潜空间生成阶段，采用Rectified Flow框架，将生成过程建模为ODE求解。Transformer网络 $G$ 用于近似条件速度场，其训练采用条件流匹配损失：

$$\mathbb{E}_{t, \mathbf{z}^0, \epsilon, \mathbf{z}_r, \mathbf{a}'} \| G(\mathbf{z}^t, \mathbf{z}_r, \mathbf{a}', t) - (\epsilon^t - \mathbf{z}^0) \|_2^2$$

其中 $\mathbf{z}^0$ 为干净潜变量，$\epsilon$ 为噪声，$\mathbf{z}^t$ 为时间 $t$ 处的含噪潜变量，$\mathbf{z}_r$ 为参考潜变量，$\mathbf{a}'$ 为音频特征。

为实现流式生成，该Transformer采用**分块因果注意力**机制：将潜序列划分为大小为 $k$ 的非重叠块，块内应用全自注意力，块间注意力仅限前序块（见图4）。生成窗口包含32个潜帧（对应128个视频帧），块大小 $k=4$ 个潜帧。训练采用教师强制策略，模型以前序真实潜变量为条件，并施加高斯噪声增强；推理时自回归逐块预测潜变量，通过KV缓存复用历史上下文，潜变量流式送入解码器生成视频帧。

### 补充图表

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/003_Figure_3.jpg]]
*Figure 3: Causal residual video auto-encoding. We apply separate temporal and spatial down/up-sampling with residual encoding. The first frame is handled independently to preserve causality*

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/004_Figure_4.jpg]]
*Figure 4: The causal blockwise attention mask*

## 实验与分析

### 主实验结果

Table 1 报告了在 HDTF 和 PortraitOneMin 两个基准上 512×512 分辨率音频驱动肖像视频生成的定量对比。所提方法在单参考图像设置下（M=1）取得 SC 8.943、SD 6.286、CAPP 0.699、FVD_25 62.300（HDTF），在 PortraitOneMin 上为 SC 8.537、SD 6.619、CAPP 0.648、FVD_25 91.964。与基于扩散的基线方法 **Hallo**（Xu et al., arXiv 2024）、**FantasyTalking**（Wang et al., ACM MM 2025）、**VASA-1**（Xu et al., NeurIPS 2024）和 **EMO**（Tian et al., ECCV 2024）相比，所提方法在唇音同步（SC）和头部-音频对齐（SD）指标上达到最佳或接近最佳水平，同时视频质量指标（FVD_25）具有竞争力。

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/006_Table_1.jpg]]
*Table 1: Quantitative results of audio-driven portrait video generation on two benchmarks at*

推理速度方面，所提方法在单张 H100 GPU 上达到 **42.3 FPS**，超过现有扩散模型一个数量级以上。这一速度优势源于两个关键设计：768 倍视频压缩率（比流行视频扩散模型 VAE 的压缩率高出约 10–15 倍）使得潜空间维度极低；分块自回归 Rectified Flow Transformer 配合 KV 缓存机制实现流式生成，避免扩散模型的多步迭代去噪过程。

### 消融实验

Table 2 系统分析了参考引导（reference guidance）和因果残差视频自编码（CR-VA）对 VAE 重建质量的影响。

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the effects of reference guidance and video residual auto-encoding (VRA) for our VAE. M denotes the number of reference images, and ∆PSNR indicates the PSNR improvement obtained by using reference guidance*

**参考引导的效果**：在 VoxCeleb2 上，单参考图像（M=1）将 PSNR 从 29.071 提升至 31.676（+2.605 dB）；在 HDTF 上，PSNR 从 28.306 提升至 32.068（+3.762 dB）。增加参考图像数量（M=3）带来进一步增益，VoxCeleb2 上 PSNR 达 32.766（+3.695 dB），HDTF 上达 33.149（+4.843 dB）。这一结果表明，参考图像显式提供静态外观信息（主体身份、背景），使解码器可将容量集中于动态信息重建，从而在高压缩比下仍保持重建质量。

**CR-VA 与参考引导的协同效应**：在无参考引导条件下，CR-VA 单独使用带来轻微重建质量提升。关键发现是两者协同工作时增益显著放大：在 VoxCeleb2 上 M=3 时，开启 CR-VA 使 PSNR 增益从 3.695 dB 升至 4.375 dB；在 HDTF 上 M=3 时，增益从 4.843 dB 升至 6.696 dB。这表明因果残差架构与参考引导机制在信息流上互补——CR-VA 的分离时空残差编码保留更多动态细节，参考引导则减轻静态外观重建负担。

### 关键图表结论

**Figure 1** 展示了由参考图像和语音生成的 512×512 流式肖像视频效果，体现唇音同步、表情变化、头部/躯干运动、发丝动态以及光影效果等丰富视觉动态。

**Figure 5** 进一步展示定性结果，方法生成的自然肖像视频全面捕捉了说话人视频的动态细节，包括音频同步的口型、自然的面部表情和头部运动。

**Table 1** 的核心结论是：所提方法在实时性上具有压倒性优势（42 FPS vs. 扩散模型的 ≤2 FPS），同时保持有竞争力的生成质量。**Table 2** 的核心结论是：参考引导是提升高压缩比 VAE 重建质量的关键因素，且与 CR-VA 架构产生正向协同。

### 局限性分析

论文未明确讨论方法局限性。根据实验设置和设计特征推断，可能存在以下限制：参考图像与目标说话人外观差异较大时，参考引导可能引入身份混淆或纹理失真；分块自回归生成中窗口边界的一致性（尤其是长视频场景）未经充分压力测试；训练采用教师强制策略，长序列推理时暴露偏差（exposure bias）的影响未量化。这些点需要进一步实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/001_Figure_1.jpg]]
*Figure 1: Our method synthesizes streamable talking portrait videos given speech audio and one or multiple reference images, enabling generation of 512 × 512 videos at 42 FPS on a single GPU. The results exhibit rich visual dynamics, including audio-synchronized lip motion, facial expressions, head and torso movement, hair dynamics, and lighting and shadow effects, advancing the level of realism and liveliness for real-time talking portraits. Identities presented in the paper are non-existent and created by Gemini 2.5 flash image [16]*

![[assets/figures/papers/paper_list_l917_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Real_Time_Generatio/figures/005_Figure_5.jpg]]
*Figure 5: Talking portrait videos generated by our method, which naturally and comprehensively capture portrait video dynamics. (Best viewed with zooming in; see the supplementary videos for a more comprehensive evaluation.)*

## 方法谱系与知识库定位

### 技术路线定位

本工作处于**实时高压缩视频生成**与**肖像动画**两条技术路线的交叉点，其核心贡献在于将深度压缩视频VAE与流式自回归生成范式引入说话人肖像合成，从而在生成速度与压缩效率两个维度上形成对现有扩散模型路线的系统性替代。

**与扩散模型路线的对比**。当前主流的音频驱动肖像视频生成方法几乎全部建立在扩散模型之上：**Hallo** (Xu et al., arXiv 2024)、**FantasyTalking** (Wang et al., ACM MM 2025)、**AniPortrait** (Wei et al., arXiv 2024)、**EMO** (Tian et al., ECCV 2024) 等方法均采用多步去噪的随机扩散范式。这些方法在生成质量上取得了显著进展，但推理速度受限于扩散采样的迭代特性，通常需要数十秒甚至更长时间生成一段视频。本文以Rectified Flow Transformer替代扩散去噪过程，将生成建模为ODE模拟而非随机微分方程求解，从根本上绕开了多步采样的计算瓶颈，实现了42 FPS的流式生成速度——**超过现有扩散模型25倍以上**。

**与实时方法的对比**。**VASA-1** (Xu et al., NeurIPS 2024) 是少数明确以实时生成为目标的说话人脸方法。本文在Table 1中与VASA-1进行了直接比较，在多个指标上达到或超越其表现，同时在推理速度上保持显著优势。值得注意的是，VASA-1仍依赖于扩散模型或其变体，而本文的Rectified Flow框架提供了更直接的ODE模拟路径，在速度与质量的权衡上具有天然优势。

**压缩效率的代际差异**。现有视频扩散模型（如Stable Video Diffusion、Open-Sora等）中使用的VAE通常仅提供约48倍的压缩率。本文通过引入**因果残差视频自编码（CR-VA）**和**参考图像引导**两个机制，将压缩率提升至768倍，较主流方案高出10–15倍。这一代际差异的意义不仅在于存储和传输效率：极致的压缩率使得潜变量序列长度大幅缩短，从而降低了后续自回归Transformer的序列建模难度和计算开销，是流式生成得以实现的关键使能因素。

### 方法谱系中的继承与创新

**继承自DC-AE的残差自编码范式**。本文的CR-VA架构明确继承自DC-AE（Chen et al., 2024）的残差自编码设计思想，将其从图像域扩展到视频域，并引入因果约束以支持流式解码。这一继承关系表明，本文的VAE设计并非从零构建，而是在已有高效图像压缩架构的基础上进行时空维度的扩展和因果性改造。

**继承自Rectified Flow的生成框架**。潜变量生成器采用了Rectified Flow框架（Liu et al., 2023; Albergo et al., 2023），将生成过程形式化为从噪声分布到目标潜变量分布的条件速度场匹配问题。本文的创新在于将该框架与分块自回归生成、KV缓存等流式推理技术结合，使其适用于长视频的实时生成场景。

**参考引导的独特贡献**。在VAE解码器中注入参考图像作为引导是本文最具原创性的设计。这一机制利用了肖像视频的一个关键先验：视频中的静态外观（主体身份、背景环境）在参考图像中已经充分呈现，解码器只需从潜变量中提取动态信息（表情、唇动、头部运动等）。消融实验（Table 2）表明，仅添加一张参考图像即可在HDTF上带来+3.762 dB的PSNR增益，在VoxCeleb2上带来+2.605 dB的增益，证明了这一设计的有效性。

### 适用边界与局限

论文未设专门的局限性讨论章节，但基于方法设计和实验设置，可以推断以下适用边界：

**静态外观依赖**。参考引导机制的有效性建立在参考图像与目标视频共享静态外观的假设之上。当参考图像与目标人物的身份、背景、光照条件存在显著差异时，解码器可能面临参考信息与潜变量动态信息之间的冲突，导致重建失真。论文未对此类场景进行系统的鲁棒性测试。

**极端动态场景的未知表现**。实验主要在HDTF和PortraitOneMin两个标准基准上进行，这些数据集中的视频通常包含相对受控的头部运动和表情变化。对于快速大幅度的头部转动、剧烈的手势遮挡、多人交互等复杂场景，方法的生成质量尚未经过验证。

**教师强制训练的暴露偏差**。自回归生成器在训练阶段采用教师强制策略——以真实历史潜变量（加噪后）作为条件输入，而在推理阶段则使用模型自身预测的历史潜变量。这种训练-推理的不一致可能导致误差累积，尤其在长视频生成中。论文未量化分析这一暴露偏差的影响程度。

**窗口边界的一致性问题**。分块自回归生成在块边界处仅依赖单向注意力，可能引入块间过渡的不连续性。虽然论文采用了重叠窗口等策略缓解此问题，但边界效应的量化评估仍不充分。

### 开放问题

1. **泛化能力验证**。方法在HDTF和PortraitOneMin之外的数据分布（如野外视频、不同文化背景的面孔、极端光照条件）上的表现如何？参考引导机制是否会在背景复杂的场景中引入干扰？

2. **与扩散蒸馏技术的结合**。Rectified Flow本质上与扩散模型共享速度场/得分匹配的理论基础。能否将现有的扩散模型蒸馏技术（如对抗蒸馏、渐进蒸馏）应用于本文框架，进一步降低Transformer生成器的参数量或推理成本？

3. **多人场景的扩展**。参考引导机制假定视频中仅包含一个主要人物。对于多人对话场景，如何扩展该机制以支持多个参考主体和对应的动态区域解耦？

4. **压缩率的上限探索**。768倍压缩率是否接近肖像视频的信息论极限？进一步增加压缩率（例如通过更激进的时空下采样）会导致哪些类型的重建失效？

5. **实时交互场景的延迟分析**。42 FPS的生成速度是在H100 GPU上测量的。在消费级GPU或移动设备上，端到端延迟（包括音频特征提取、VAE编解码、Transformer自回归生成）的瓶颈在哪个模块？是否存在针对特定硬件的优化空间？

## 原文 PDF

![[paperPDFs/CVPR_2026/Real_Time_Generation_of_Streamable_Talking_Portrait_Video_with_Reference_Guided_Deep_Compression_VAEs.pdf]]
