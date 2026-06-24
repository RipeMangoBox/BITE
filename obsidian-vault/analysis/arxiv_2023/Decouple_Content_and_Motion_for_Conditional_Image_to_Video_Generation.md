---
title: Decouple Content and Motion for Conditional Image-to-Video Generation
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/Decouple_Content_and_Motion_for_Conditional_Image_to_Video_Generation.pdf
aliases:
- DCMCIVG
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将视频显式解耦为静态空间内容（起始帧）与动态时序运动（帧间差或运动矢量+残差），把扩散模型的生成目标从完整像素帧迁移到压缩的运动特征空间。
primary_logic: 借鉴视频压缩中运动补偿的思想，通过直接生成可逆的运动矢量和残差来表示时序变化，可在大幅降低空间维度（110倍加速）的同时保持生成视频的时序一致性，且过程完全可逆。
claims:
- D-VDM64在MHAD上FVD为145.41，优于此前最优的LFDM64（152.48），证明解耦到帧间差即可提升时序建模。
- ED-VDM128在MHAD上FVD为204.17，同时训练FLOPs从VDM的8814×10^9降至78×10^9，实现约110倍加速且保持竞争力。
- 在BAIR 64×64无条件生成上，D-VDM取得FVD 65.5，优于此前最优的LVDM（66.9），显示解耦策略的通用性。
- 残差压缩采用自编码器（PSNR 31.80/SSIM 0.96）比重建DCT（PSNR 17.08/SSIM 0.85）质量大幅提升，保证了ED-VDM的重建精度。
---

# Decouple Content and Motion for Conditional Image-to-Video Generation

> [!tip] 核心洞察
> 借鉴视频压缩中运动补偿的思想，通过直接生成可逆的运动矢量和残差来表示时序变化，可在大幅降低空间维度（110倍加速）的同时保持生成视频的时序一致性，且过程完全可逆。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解耦内容与运动的条件图像到视频生成 |
| 英文题名 | Decouple Content and Motion for Conditional Image-to-Video Generation |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2311.14294) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | D-VDM（Decoupled Video Diffusion Model）与 ED-VDM（Efficient Decoupled Video Diffusion Model） |
| Dataset | MHAD, NATOPS, BAIR |

> [!tip] 效果简介
> - MHAD (64×64) 上，FVD↓ 145.41 (D-VDM64) vs 152.48 (LFDM64) (-7.07)。
> - MHAD (128×128) 上，FVD↓ 204.17 (ED-VDM128) vs 214.39 (LFDM128) (-10.22)。
> - NATOPS (64×64) 上，FVD↓ 152.19 (D-VDM64) vs 160.84 (LFDM64) (-8.65)。

## 概述

条件图像到视频生成的核心瓶颈在于：RGB像素空间中视频帧间存在大量信息冗余，扩散模型难以从高维原始信号中捕捉关键时序变化，导致运动一致性与生成效率的双重不足。现有潜空间方法（如LDM）虽通过变分自编码器进行压缩，但压缩率有限，且未显式建模时序一致性，空间细节与运动连贯性难以兼顾。

本文提出**解耦视频扩散模型**（D-VDM 与 ED-VDM），核心思路借鉴视频压缩中运动补偿的思想：将视频显式解耦为静态空间内容（起始帧）与动态时序运动（帧间差，或运动矢量+残差），把扩散模型的生成目标从完整像素帧迁移到高度压缩的运动特征空间。这一策略在保持生成视频时序一致性的同时，大幅降低计算开销——ED-VDM在128×128分辨率下实现约110倍的训练加速。

主要结果如下：
- 在MHAD 64×64条件生成上，D-VDM取得FVD 145.41，优于此前最优的LFDM（152.48）；
- 在MHAD 128×128上，ED-VDM以FVD 204.17超越LFDM（214.39），同时训练FLOPs从VDM的8814×10⁹降至78×10⁹；
- 在BAIR 64×64无条件生成上，D-VDM取得FVD 65.5，优于LVDM（66.9），验证解耦策略的通用性。

方法上，D-VDM直接以帧间差为生成目标，ED-VDM进一步引入H.264运动矢量提取与残差VAE压缩，将运动特征空间维度压缩至原来的1/110。消融实验表明，仅将目标空间从RGB像素改为帧间差即可带来性能提升；残差的自编码器压缩（PSNR 31.80/SSIM 0.96）显著优于传统DCT方法（PSNR 17.08/SSIM 0.85），是ED-VDM保持重建精度的关键。

该方法属于**视频扩散模型的表示空间优化**路线，与光流引导生成（如LFDM）和潜空间压缩（如LDM、LVDM）形成互补。其核心贡献在于将视频压缩的工程智慧系统性地融入扩散生成框架，以可逆的运动表示替代不可逆的像素生成，为高效时序建模提供了新范式。

## 背景与动机

### 视频生成的核心瓶颈：时序冗余与运动一致性

条件图像到视频生成（给定首帧图像，预测后续帧序列）在计算机视觉中具有广泛应用前景，但其核心挑战在于如何同时保持空间质量与长程时序一致性。现有方法普遍在RGB像素空间中对完整视频帧进行建模，而视频帧间存在大量信息冗余——相邻帧中绝大部分像素仅发生微小位移或保持不变。这种冗余导致扩散模型将大量计算资源消耗在重建静态背景与不变纹理上，难以聚焦于捕捉关键的时序变化，最终表现为生成视频的运动模糊、抖动或语义漂移。

潜变量扩散模型（如**LDM**, Rombach et al., CVPR 2022）通过变分自编码器将视频压缩至低维潜空间，在一定程度上缓解了计算负担，但其压缩率有限（通常为8×），且潜空间压缩并未直接建模时序一致性——模型仍需从压缩表征中隐式学习运动模式，空间细节的损失与运动一致性的改善之间存在固有张力。

### 现有方法的局限与本文动机

此前的工作在提升视频生成质量方面做出了多种尝试：**VDM**（Ho et al., Arxiv 2022）直接在像素空间进行3D扩散建模，计算开销巨大；**LFDM**（Ni et al., CVPR 2023）引入光流作为运动先验，但光流估计本身存在误差且与生成过程分离；**LVDM**（He et al., Arxiv 2022）通过层次化潜变量建模长视频，但时序建模仍依赖隐式学习。这些方法的共同缺陷在于：**生成目标始终是完整的RGB像素帧或其潜变量，未对视频的内容（静态）与运动（动态）进行显式解耦**，导致模型必须在高维空间中同时处理空间外观和时序变化两个耦合的任务。

本文的核心动机源自视频压缩领域的经典洞察：在H.264等编码标准中，视频帧被分解为运动矢量（描述宏块的位移）与残差（补偿运动补偿后的像素差异），这种分解将时序变化从像素空间迁移到低维的运动特征空间，实现了极高的压缩比。**本文的关键思路是将这一解耦思想引入扩散生成模型**：将生成目标从完整像素帧转变为运动矢量与残差的联合分布，使扩散模型在高度压缩的运动特征空间中运行，从而在显著降低计算开销的同时，通过显式建模时序变化来提升运动一致性。

## 核心创新

### 瓶颈洞察：从RGB像素冗余到运动-内容解耦

传统视频扩散模型（如 **VDM** (Ho et al., Arxiv 2022)、**LDM** (Rombach et al., CVPR 2022)）直接在RGB像素空间或潜空间建模完整视频帧序列。其根本瓶颈在于：相邻帧之间在像素层面存在大量信息冗余，扩散模型被迫同时学习静态背景的重复编码和动态变化的微弱信号，导致计算资源严重浪费且时序一致性难以保证。潜空间方法（如LDM的8×压缩）虽缓解了计算压力，但压缩过程未显式建模时序关系，运动连贯性仍属隐式学习的副产物。

本文的核心洞察源自视频压缩领域的基本思想：**将视频显式解耦为静态空间内容与动态时序运动**，使扩散模型的生成目标从冗余的完整帧迁移到紧凑的运动特征空间。这一思路直接回应了上述瓶颈——当模型只需生成帧间变化量时，信息密度大幅提升，时序一致性成为显式建模对象而非隐式期望。

### 关键机制：两级解耦与目标空间迁移

方法包含两个递进的创新层次，对应两个模型变体：

**D-VDM：帧间差解耦。** 最直接的解耦方式是将视频表示为首帧 $v_0$ 与后续帧的差值序列 $\hat{v}_0$（见Figure 3）。扩散模型的生成目标从 $v \in \mathbb{R}^{T \times H \times W \times 3}$ 变为 $\hat{v} \in \mathbb{R}^{(T-1) \times H \times W \times 3}$，同时将首帧的空间语义通过ResNet瓶颈模块编码为条件特征 $\tau_\theta(v_0)$，拼接到去噪网络的输入通道维度。训练损失从标准DDPM目标修改为：

$$L = \mathbb{E}_{t, \hat{v}_0 \sim \mathcal{V}(\hat{v}_0), \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) ||\epsilon - \epsilon_\theta(\hat{v}_t, t, \tau_\theta(v_0))||^2]$$

这一改变看似简单，却将模型的注意力从“画完整画面”转移到“画变化部分”，在BAIR 64×64上将最优FVD从66.9降至65.5（Table 3），证实解耦策略本身即有效。

**ED-VDM：运动矢量+残差的双流压缩解耦。** 帧间差虽有效但仍包含空间冗余。ED-VDM借鉴H.264编码思想，将时序变化进一步分解为两个异构分量：
- **运动矢量 $\mathbf{m}$**：通过16×16宏块的SAD最小化块匹配提取，表示物体的粗略位移，空间分辨率仅为原帧的1/256（256×压缩）；
- **残差 $\mathbf{r}$**：运动补偿后剩余的像素级修正信息，通过一个独立训练的变分自编码器（VAE）压缩至与运动矢量对齐的潜空间（16×压缩）。

两者在潜空间拼接为 $[\mathbf{m}, \mathcal{E}(\mathbf{r})]$，由3D U-Net联合建模其分布，损失函数为：

$$L = \mathbb{E}_{t, \mathbf{m}, \mathbf{r} = f(v_0), v_0 \sim \mathcal{V}, \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) \mathrm{mse}], \quad \mathrm{mse} = \| \epsilon - \epsilon_\theta(\mathbf{m}_t, \mathcal{E}(\mathbf{r}_t), t, \tau_\theta(v_0^0)) \|^2$$

生成时，去噪后的运动矢量和残差通过H.264解码器与首帧进行运动补偿重建，整个过程完全可逆。

### Changed Slots：相对于基线的结构性差异

| 设计维度 | 基线方法（VDM/LDM） | 本文方法（D-VDM/ED-VDM） | 证据锚点 |
|---------|-------------------|------------------------|---------|
| **生成目标空间** | 完整RGB像素帧（如16×128×128×3） | D-VDM：帧间差；ED-VDM：运动矢量+残差潜表示 | Section Decoupled Video Diffusion Model, Efficient Decoupled Video Diffusion Model |
| **空间压缩倍率** | 无压缩（VDM）或8×潜空间压缩（LDM） | 运动矢量256×，残差16×，整体等效约110×加速 | Table 4, Introduction |
| **时序建模方式** | 隐式（通过3D卷积学习帧间关系） | 显式（运动矢量编码位移，残差补充细节） | Figure 3, Equation 8 |
| **条件注入** | 首帧直接拼接到输入帧序列 | 首帧经ResNet瓶颈编码为 $\tau_\theta(v_0)$，拼接到扩散输入通道 | Equation 7, Implementation Details |

### 创新价值与边界

**价值验证：** ED-VDM在MHAD 128×128上以204.17的FVD优于此前最优的**LFDM**（Ni et al., CVPR 2023）的214.39，同时训练FLOPs从VDM的$8814 \times 10^9$骤降至$78 \times 10^9$（约110倍），GPU内存从11.56 GB降至3.47 GB（Table 4）。残差VAE的重建质量（PSNR 31.80, SSIM 0.96）远优于传统DCT方法（PSNR 17.08, SSIM 0.85），保证了压缩-解压缩引入的失真可控（Table 5）。

**边界与局限：** 运动矢量提取依赖刚性块匹配，对复杂变形、遮挡或大运动的适应能力有限；残差VAE与扩散模型分开训练，非端到端优化；速度对比仅基于FLOPs和内存，未提供实际墙钟时间；验证数据集（MHAD、NATOPS、BAIR）规模较小，高分辨率自然场景下的泛化性尚需进一步验证。

## 整体框架

D-VDM 与 ED-VDM 的核心设计思路是将视频生成任务从高维 RGB 像素空间迁移到压缩的运动特征空间，通过显式解耦静态内容与动态运动来降低扩散模型的建模难度。整体框架如图 2 所示，包含两条并行的技术路径。

### 统一生成范式：内容-运动解耦

给定起始帧 $v_0$，模型的目标是生成后续 $N-1$ 帧。传统方法直接在 RGB 空间中建模完整帧序列，导致信息冗余严重。本工作将视频分解为两个正交分量：

- **空间内容**：由起始帧 $v_0$ 承载，通过 ResNet 瓶颈模块编码为条件特征 $\tau_\theta(v_0)$，注入扩散过程。
- **时序运动**：以帧间变化量作为生成目标，具体形式在 D-VDM 和 ED-VDM 中有所不同。

生成阶段，扩散模型从高斯噪声 $\mathbf{s} \sim \mathcal{N}(0, I)$ 出发，在条件特征引导下逐步去噪，得到运动表示。最后通过逆变换将运动表示与起始帧合成完整视频。

### D-VDM：帧间差扩散

D-VDM（图 2 绿色路径）采用最直接的解耦方式：保留首帧，计算其与后续帧的逐像素差值 $\hat{v}_0 \in \mathcal{V}(\hat{v}_0)$，将差值序列作为扩散模型的生成目标。训练损失为：

$$L = \mathbb{E}_{t, \hat{v}_0 \sim \mathcal{V}(\hat{v}_0), \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) ||\epsilon - \epsilon_\theta(\hat{v}_t, t, \tau_\theta(v_0))||^2]$$

其中 $\epsilon_\theta$ 为 3D U-Net 去噪网络，$\tau_\theta(v_0)$ 为首帧编码条件。这一改动将生成目标从完整的 RGB 像素帧替换为稀疏的帧间差，在几乎不增加额外计算开销的前提下显著提升了时序一致性（BAIR 上 FVD 从 66.9 降至 65.5）。

### ED-VDM：运动矢量+残差扩散

ED-VDM（图 2 蓝色路径）进一步借鉴 H.264 视频压缩标准，将运动信息分解为运动矢量 $\mathbf{m}$ 和残差 $\mathbf{r}$（图 3）：

1. **运动矢量提取**：对每个 $16 \times 16$ 宏块 $B_i$，通过最小化绝对差值和（SAD）在前一帧中搜索最优匹配块，得到运动矢量：
   $$\mathbf{m}_i = \underset{\mathbf{u}, \mathbf{w}}{\operatorname{argmin}} \sum_{j,k} \left| B_i(j,k) - B_i'(j+\mathbf{u}, k+\mathbf{w}) \right|$$
   运动矢量空间分辨率仅为原始帧的 $1/256$，实现了极致的空间压缩。

2. **残差压缩**：残差 $\mathbf{r}$ 与原始帧同尺寸，为使其与运动矢量空间对齐，使用变分自编码器（VAE）将其压缩 16×。VAE 以 $L_1$ 损失训练，重建质量达到 PSNR 31.80、SSIM 0.96（Table 5），远优于传统 DCT 方法（PSNR 17.08、SSIM 0.85）。

3. **联合扩散**：将运动矢量和压缩残差的潜表示通道拼接为 $[\mathbf{m}, \mathcal{E}(\mathbf{r})]$，通过统一的扩散目标学习联合分布：
   $$L = \mathbb{E}_{t, \mathbf{m}, \mathbf{r} = f(v_0), v_0 \sim \mathcal{V}, \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) \mathrm{mse}], \quad \mathrm{mse} = \| \epsilon - \epsilon_\theta(\mathbf{m}_t, \mathcal{E}(\mathbf{r}_t), t, \tau_\theta(v_0^0)) \|^2$$

4. **视频重建**：生成的运动矢量和残差经解码后，通过运动补偿将首帧 warp 并与残差叠加，恢复完整视频帧序列。整个过程完全可逆，重建上界 R-FVD 仅为 13.5，PSNR 达 37.8（Table 2），表明压缩-解压缩引入的信息损失极小。

### 模块关系与数据流

两条路径共享相同的 3D U-Net 去噪骨干网络和首帧编码器，仅在生成目标的表示形式上不同。整体数据流为：

```
起始帧 v₀ → ResNet 编码器 → τ_θ(v₀)（条件特征）
                                    ↓
噪声 s ~ N(0,I) → 3D U-Net 去噪（条件注入）→ 运动表示
                                    ↓
                            逆变换 + 首帧 → 完整视频
```

ED-VDM 通过运动矢量的 256× 压缩和残差的 16× 压缩，将等效空间降采样率提升至约 110×，训练 FLOPs 从 VDM 的 $8814 \times 10^9$ 骤降至 $78 \times 10^9$（Table 4），同时保持了与 SOTA 方法相当的生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our proposed decoupled video diffusion model. (a) Pipeline. The green pathway represents the Decoupled Video Diffusion Model (D-VDM), which directly generates motion features in the compressed video domain, while the blue pathway illustrates the Efficient Decoupled Video Diffusion Model (ED-VDM), which includes a reversible compression function. (b) Compression techniques used in the ED-VDM model. Since the separated motion vectors and residuals are of unequal lengths, it is necessary for us to apply equal-length processing to both components. (c) The architecture of the 3D U-Net. We employed the 3D U-Net architecture in both models*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/001_Figure_1.jpg]]
*Figure 1: Motivations and our ideas. Conventional methods (see in (b)), involve extending the RGB space with time sequences, resulting in limited memory efficiency and temporal coherence. Latent Diffusion Models employ a variational autoencoder for compression (depicted in (a)), enhancing efficiency but potentially reducing spatial quality and poor temporal coherence because temporal consistency hasn’t been directly modeled. Our approach (refer to (c)) decouples the content and motion, capitalizing on existing temporal coherence in compressed video data, resulting in a memory-efficient and temporally consistent video generation approach*

## 核心模块与公式推导

### 方法总览

本文提出 D‑VDM 与 ED‑VDM 两种解耦视频扩散模型，其核心思想是将视频显式分解为静态空间内容（首帧）与动态时序运动（帧间差或运动矢量+残差），并将扩散模型的生成目标从完整 RGB 像素帧迁移到压缩的运动特征空间。整体框架如 Figure 2 所示，绿色通路对应 D‑VDM，蓝色通路对应 ED‑VDM。

### 关键模块

**3D U‑Net 去噪网络**是两种模型共用的骨干架构（Figure 2(c)），负责对噪声化的运动特征进行逐步去噪，预测噪声 $\epsilon_\theta$。该网络接收噪声化的运动表示、时间步 $t$ 以及首帧条件编码作为输入，输出与输入同维度的噪声预测。

**首帧图像编码器**采用 ResNet 瓶颈模块（He et al., 2016），将起始帧 $v_0$ 编码为空间语义特征 $\tau_\theta(v_0)$，并沿通道维度拼接到扩散模型的输入中，作为条件信号引导运动生成。该模块确保生成的运动特征在语义上与首帧保持一致。

**运动矢量提取模块**（仅 ED‑VDM）借鉴 H.264 压缩标准，通过块匹配算法从前一帧中为每个 $16 \times 16$ 宏块搜索最优运动矢量。具体地，对宏块 $B_i$，最小化绝对差值和（SAD）得到运动矢量 $\mathbf{m}_i$：

$$\mathbf{m}_i = \underset{\mathbf{u}, \mathbf{w}}{\operatorname{argmin}} \sum_{j,k} \left| B_i(j,k) - B_i'(j+\mathbf{u}, k+\mathbf{w}) \right|$$

该过程将帧间运动压缩为低分辨率的运动矢量场，空间降采样倍率达 256×。

**残差变分自编码器**（仅 ED‑VDM）负责将运动补偿后的残差 $\mathbf{r}$ 从原始帧分辨率压缩到与运动矢量空间对齐的潜表示。残差自编码器采用 $L_1$ 重建损失训练，实现 16× 空间压缩。压缩后的运动矢量 $\mathbf{m}$ 与残差潜表示 $\mathcal{E}(\mathbf{r})$ 沿通道维度拼接为 $[\mathbf{m}, \mathcal{E}(\mathbf{r})]$，作为扩散模型的联合学习目标。

### 核心公式推导

**扩散基础**。DDPM 的前向过程逐步向数据 $\mathbf{x}_0$ 添加高斯噪声：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_{t-1}; \sqrt{\alpha_t} \mathbf{x}_{t-1}, \beta_t I)$$

逆向过程的条件后验可近似为高斯分布：

$$q(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{x}_0) := \mathcal{N}(x_t; \hat{\mu}(\mathbf{x}_t, \mathbf{x}_0), \hat{\sigma})$$

其中均值可由噪声预测表示：

$$\hat{\mu}(\mathbf{x}_t, \mathbf{x}_0) = \frac{1}{\sqrt{\alpha_t}} \Bigl( \mathbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\epsilon}_t \Bigr)$$

训练目标为最小化噪声预测的均方误差：

$$\mathbb{E}_{t \sim \mathcal{U}(0,T), \mathbf{x}_0 \sim q(\mathbf{x}_0), \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) \lVert \epsilon - \epsilon_\theta(\mathbf{x}_t, t) \rVert^2]$$

**D‑VDM 损失**。D‑VDM 将生成目标从 RGB 像素替换为帧间差 $\hat{v}_0$，并将首帧编码 $\tau_\theta(v_0)$ 作为条件拼接到扩散输入：

$$L = \mathbb{E}_{t, \hat{v}_0 \sim \mathcal{V}(\hat{v}_0), \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) ||\epsilon - \epsilon_\theta(\hat{v}_t, t, \tau_\theta(v_0))||^2]$$

其中 $\hat{v}_t$ 为噪声化的帧间差，$\tau_\theta(v_0)$ 为首帧的 ResNet 编码特征。该公式的因果机制在于：网络不再需要从噪声中恢复完整的 RGB 像素，而只需预测相邻帧之间的差异信号，显著降低了学习难度。

**ED‑VDM 损失**。ED‑VDM 进一步将运动矢量 $\mathbf{m}$ 与压缩后的残差 $\mathcal{E}(\mathbf{r})$ 联合建模：

$$L = \mathbb{E}_{t, \mathbf{m}, \mathbf{r} = f(v_0), v_0 \sim \mathcal{V}, \epsilon \sim \mathcal{N}(0,1)} [\lambda(t) \mathrm{mse}]$$

$$\mathrm{mse} = \| \epsilon - \epsilon_\theta(\mathbf{m}_t, \mathcal{E}(\mathbf{r}_t), t, \tau_\theta(v_0^0)) \|^2$$

其中 $\mathbf{m}_t$ 和 $\mathcal{E}(\mathbf{r}_t)$ 分别为噪声化的运动矢量和残差潜表示，$v_0^0$ 为视频的首帧。该联合扩散损失使模型同时学习运动矢量和残差的联合分布，以首帧为条件，从而实现可逆的视频重建：生成的运动矢量和残差经 CodeC 解码器与首帧合成即可恢复完整视频序列。

**压缩效率的因果机制**。运动矢量场的空间分辨率仅为原始帧的 $1/256$（每个 $16 \times 16$ 宏块对应一个运动矢量），残差经 VAE 压缩 16×，二者拼接后整体等效空间降采样约 110×。这一压缩比直接转化为训练 FLOPs 从 VDM 的 $8814 \times 10^9$ 降至 ED‑VDM 的 $78 \times 10^9$（Table 4），GPU 内存从 11.56 GB 降至 3.47 GB。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/004_Figure_3.jpg]]
*Figure 3: Different ways to represent video temporal feature between frames. Frame difference used by D-VDM, a simple technique, calculates direct frame discrepancies, encompassing both fundamental and advanced temporal alterations. D-VDM findings reveal its potency in refining the temporal consistency of a generated video. Motion Vector and Residual used by ED-VDM, as in H.264, disentangles temporal shifts into intermediate motion blocks and pixel residuals. Notably, correlated with motion vectors, these residuals offer a sparse representation with potent compression potential. In our experiments, ED-VDM attains an impressive 110x compression ratio*

## 实验与分析

### 核心瓶颈与解耦策略的有效性验证

本文的核心假设是：RGB 像素空间中的视频帧间存在大量信息冗余，导致扩散模型难以捕捉关键时序变化。为验证这一假设，作者设计了两级解耦方案——D-VDM 将生成目标从完整像素帧迁移至帧间差，ED-VDM 进一步分解为运动矢量与残差——并在多个基准上进行了系统性验证。

#### 条件图像到视频生成主结果

Table 1 报告了在 MHAD 和 NATOPS 两个人体动作数据集上的条件生成结果。在 64×64 分辨率下，**D-VDM64** 在 MHAD 上取得 FVD 145.41，优于此前最优的 **LFDM**（Ni et al., CVPR 2023）的 152.48；在 NATOPS 上，D-VDM64 的 FVD 为 152.19，同样优于 LFDM64 的 160.84。当分辨率提升至 128×128 时，**ED-VDM128** 在 MHAD 上取得 FVD 204.17，优于 LFDM128 的 214.39。值得注意的是，ED-VDM128 在保持竞争力的同时，训练 FLOPs 从 VDM（Ho et al., Arxiv 2022）的 8814×10⁹ 降至 78×10⁹，实现了约 **110 倍加速**（Table 4），内存占用也从 11.56 GB 降至 3.47 GB。

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of conditional Image-to-Video generation on MHAD and NATOPS datasets. We compare FVD, sFVD, and cFVD on 16 frames clip. The 64 and 128 in the subscript indicate that the resolution of synthesized video frames is 64 × 64 and*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/010_Table_4.jpg]]
*Table 4: FLOPs and memory usage for our model to train on 1 batch of 16 × 128 × 128 × 3 resolution videos*

Table 3 展示了在 BAIR 机器人推杆数据集上的无条件生成结果。**D-VDM** 取得 FVD 65.5，优于此前最优的 **LVDM**（He et al., Arxiv 2022）的 66.9。作者明确指出，仅将目标空间从 RGB 像素改为帧间差这一简单操作，便带来了可观的性能提升，直接验证了解耦策略本身的有效性。

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/005_Table_3.jpg]]
*Table 3: Image-to-Video Generation Results on BAIR dataset. Our method surpasses the SOTA methods with regard to FVD score*

#### 压缩重建质量上界

ED-VDM 的生成质量受限于其压缩-解压缩过程的信息保真度。Table 2 报告了 ED-VDM 的重建上界：R-FVD 为 13.5，PSNR 为 37.8，SSIM 为 0.98。这一结果表明，运动矢量与残差的压缩-解压缩过程引入的失真极小，为扩散模型在该压缩空间中的生成提供了高质量的上界保证。

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/006_Table_2.jpg]]
*Table 2: The upper bound of our ED-VDM method. R-FVD score is evaluated with 2,048 samples. PSNR and SSIM are evaluated on an average of 16 frames with 100 samples*

#### 残差压缩方法的消融

ED-VDM 中残差压缩方案的选择对最终重建质量至关重要。Table 5 对比了基于自编码器（VAE）的方法与传统 DCT 方法：自编码器方法重建 PSNR 达 31.80、SSIM 达 0.96，而 DCT 方法仅为 17.08 和 0.85。这一显著差距说明，传统 DCT 压缩会严重损失空间细节，而可学习的 VAE 压缩能够更好地保留残差中的精细纹理信息，是 ED-VDM 保持生成质量的关键组件。

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/009_Table_5.jpg]]
*Table 5: Image quality comparison between our proposed autoencoder method and traditional DCT method*

### 失败模式与局限性分析

尽管解耦策略在效率和质量上均展现出优势，但分析中仍暴露出若干值得关注的局限：

1. **低分辨率下的质量折损**：ED-VDM 在 BAIR 64×64 上的 FVD 为 92.4，虽然仍具竞争力，但相较于 D-VDM 的 65.5 有明显退化。这表明在极低分辨率下，运动矢量和残差的联合压缩可能损失了对生成质量至关重要的空间细节。

2. **评估范围的限制**：所有实验均在较小规模的动作数据集（MHAD、NATOPS、BAIR）上进行，尚未在高分辨率真实场景视频（如 WebVid、Kinetics）上验证。模型对复杂背景、相机运动和大尺度物体变形的适应能力仍有待检验。

3. **效率指标的局限性**：Table 4 仅报告了 FP32 训练时的 FLOPs 和 GPU 内存占用，未提供相同硬件下的实际训练或推理墙钟时间。此外，运动矢量量化误差在长序列生成中的累积效应未被讨论。

4. **压缩模块的独立训练**：ED-VDM 的残差自编码器与扩散模型分开训练，未能实现端到端优化，可能限制了整体生成质量的进一步提升。

### 图表结论摘要

- **Table 1**：D-VDM 和 ED-VDM 在 MHAD/NATOPS 上均优于或持平于此前最优方法，且 ED-VDM 以约 110 倍加速保持竞争力。
- **Table 3**：仅将目标空间改为帧间差（D-VDM）便在 BAIR 上将最优 FVD 从 66.9 降至 65.5，证实解耦策略的通用性。
- **Table 2**：ED-VDM 的重建上界（R-FVD 13.5, PSNR 37.8, SSIM 0.98）表明压缩过程失真极小。
- **Table 5**：VAE 压缩残差的 PSNR/SSIM（31.80/0.96）远超 DCT（17.08/0.85），是 ED-VDM 保持空间细节的关键。
- **Table 4**：ED-VDM 训练 FLOPs 从 VDM 的 8814×10⁹ 降至 78×10⁹，内存从 11.56 GB 降至 3.47 GB。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/008_Figure_5.jpg]]
*Figure 5: Video quality on residual reconstruction*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2311_14294/figures/007_Figure_4.jpg]]
*Figure 4: Selected samples on BAIR, NATOPS, and MHAD dataset. First two rows are the results of unconditionally generation results on BAIR, and the down four rows are text conditional generation results on MHAD and NATOPS. The visualization results show our method generated realistic and temporally consistent video frames*

## 方法谱系与知识库定位

### 1. 与条件图像到视频生成基线的关系

本文提出的 **D-VDM / ED-VDM** 处于条件图像到视频生成（conditional Image-to-Video generation）这一研究脉络中，其核心创新在于将扩散模型的生成目标从完整的 RGB 像素帧迁移到压缩的运动特征空间。与现有基线的关系可归纳为以下几条线索：

**像素空间扩散基线**：**VDM**（Ho et al., Arxiv 2022）直接在原始 RGB 像素空间进行视频扩散建模，其训练 FLOPs 在 128×128 分辨率下高达 $8814 \times 10^9$（Table 4），且时序一致性受限于像素空间的冗余信息。D-VDM 仅通过将目标空间从 RGB 像素改为帧间差，便在 BAIR 64×64 上将最优 FVD 从 66.9（LVDM）降至 65.5（Table 3），证明了去冗余本身即可提升时序建模能力。

**潜空间压缩基线**：**LDM**（Rombach et al., CVPR 2022）通过 VAE 将视频压缩到潜空间（约 8× 降采样），提升了效率但未直接建模时序一致性。ED-VDM 在此基础上进一步将运动矢量压缩 256×、残差压缩 16×，整体等效约 110× 加速（Table 4），同时保持了有竞争力的 FVD 指标（MHAD 128×128 上 204.17 vs LFDM 的 214.39，Table 1）。这表明显式解耦运动与内容比单纯的潜空间压缩更有利于时序一致性。

**光流引导基线**：**LFDM**（Ni et al., CVPR 2023）利用光流作为运动先验来引导视频生成。D-VDM64 在 MHAD 上 FVD 为 145.41，优于 LFDM64 的 152.48（Table 1）；ED-VDM128 的 FVD 为 204.17，同样优于 LFDM128 的 214.39。与光流这种稠密运动表示相比，本文的运动矢量 + 残差表示更稀疏、更易于压缩，且直接与 H.264 编解码器兼容，实现了可逆的视频重建。

**其他条件生成基线**：**CCVS**（Moing et al., NeurIPS 2021）和 **ImaGINator** 等早期方法在 FVD 指标上明显落后于扩散模型系列（Table 1），本文方法在 MHAD 和 NATOPS 数据集上均取得了最优或次优的 FVD 分数。

### 2. 适用边界

根据论文提供的实验证据和局限性分析，D-VDM / ED-VDM 的适用边界可归纳如下：

- **数据集规模与场景复杂度**：当前验证仅在较小规模的动作数据集（MHAD、NATOPS、BAIR）上进行，这些数据集以人体动作为主，背景相对简单。模型尚未在高分辨率真实场景视频（如 WebVid、Kinetics）上进行测试，其在复杂背景、相机运动场景下的泛化能力未知。
- **分辨率上限**：实验覆盖了 64×64 和 128×128 两种分辨率。ED-VDM 在 128×128 下的 FVD 为 204.17，虽优于 LFDM128，但绝对数值仍较高，暗示向 256×256 或更高分辨率扩展时可能面临运动失真累积的挑战。
- **运动类型限制**：运动矢量提取依赖基于 SAD 最小化的刚性块匹配（16×16 宏块），对复杂变形、遮挡或大幅度运动的适应能力有限。此外，该方法未显式分离相机运动与物体运动，在包含显著相机运动的自然视频中，运动矢量的稀疏性假设可能不再成立。
- **端到端优化的缺失**：ED-VDM 的残差自编码器与扩散模型分开训练（L1 目标），而非端到端联合优化。尽管重建质量上界评估显示 R-FVD 为 13.5、PSNR 为 37.8、SSIM 为 0.98（Table 2），但压缩-解压缩过程仍会引入轻微信息损失，可能限制生成质量的进一步提升。

### 3. 局限与开放问题

**已知局限**：

1. **验证范围有限**：仅在小规模动作数据集上评估，缺乏大规模、高分辨率真实视频的实验证据。
2. **压缩-生成分离训练**：残差 VAE 与扩散模型独立训练，无法端到端优化整体生成质量。
3. **运动表示刚性**：块匹配运动矢量对复杂运动（变形、遮挡）的建模能力有限，且未区分相机与物体运动。
4. **效率评估不完整**：速度比较仅基于 FLOPs 和 GPU 内存（Table 4），未提供实际墙钟时间，也未讨论运动矢量量化误差在生成过程中的累积效应。
5. **ED-VDM 在低分辨率下的质量折损**：ED-VDM 在 BAIR 64×64 上的 FVD 为 92.4，显著高于 D-VDM 的 65.5（Table 3），说明在较低分辨率下压缩带来的信息损失对生成质量的影响更为明显。

**开放问题**：

1. **长视频与高分辨率扩展**：解耦表示能否扩展到生成长视频或 256×256 / 512×512 分辨率，而不引发运动失真累积？
2. **与大规模潜变量视频扩散模型的结合**：运动矢量与残差的压缩策略是否可与当前的大规模潜变量视频扩散模型（如 VideoLDM、Sora）结合，进一步提升效率？
3. **文本到运动的语义控制**：如何将文本条件更细致地注入运动生成过程，以实现对动作类型、幅度和速度的细粒度语义控制？
4. **自然视频中的稀疏性假设**：在具有复杂背景和相机运动的自然视频中，运动矢量和残差表示是否仍然稀疏且可有效预测？
5. **跨任务通用性**：ED-VDM 的压缩表示能否应用于其他生成任务（如视频预测、视频修复），其解耦策略是否具有任务无关的通用性？
6. **实际推理速度**：110× 的 FLOPs 加速在真实硬件上的墙钟时间收益如何？量化误差在自回归生成多帧时是否会逐步累积？

## 原文 PDF

![[paperPDFs/arxiv_2023/Decouple_Content_and_Motion_for_Conditional_Image_to_Video_Generation.pdf]]