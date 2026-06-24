---
title: Adaptive Anisotropic Gaussian Splatting for Multi-contrast MRI Arbitrary-Scale Super-Resolution with Anatomy Guidance
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adaptive_Anisotropic_Gaussian_Splatting_for_Multi_contrast_MRI_Arbitrary_Scale_Super_Resolution_with_Anatomy_Guidance.pdf
project_link: null
code_link: "https://github.com/Qiuhai-CV/GaussM2ASR"
aliases:
- Adaptive_Anisotr
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将图像生成范式从像素强度回归转变为学习各向异性2D高斯参数（均值、协方差、不透明度），使模型能自适应地调整核的方差：窄核用于高频边界，宽核用于低频平滑区域，从而将高频重建转化为更平滑的参数优化问题。
primary_logic: 利用一组可学习的各向异性2D高斯函数作为自适应的基函数，通过α混合渲染 MRI 图像，用基函数的组合替代逐像素预测，从根本上缓解了INR的频谱偏差，显著增强高频解剖细节的恢复能力。
claims:
- GaussM2ASR在定性上比INR模型（Dual-ArbNet、McASSR、DINet）恢复出更丰富的解剖边界。
- 在拟合高频结构方面，2DGS模型（GaussM2ASR）的收敛速度明显快于INR方法（DINet），且最终性能更高。
- IXI (T2, ref T1) 上 PSNR / SSIM (×4) = 32.03 / 0.9350
- fastMRI (FSPD, ref FD) 上 PSNR / SSIM (×4) = 34.65 / 0.9621
---

# Adaptive Anisotropic Gaussian Splatting for Multi-contrast MRI Arbitrary-Scale Super-Resolution with Anatomy Guidance

> [!tip] 核心洞察
> 利用一组可学习的各向异性2D高斯函数作为自适应的基函数，通过α混合渲染 MRI 图像，用基函数的组合替代逐像素预测，从根本上缓解了INR的频谱偏差，显著增强高频解剖细节的恢复能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自适应各向异性高斯溅射用于多对比度MRI任意尺度超分辨率与解剖引导 |
| 英文题名 | Adaptive Anisotropic Gaussian Splatting for Multi-contrast MRI Arbitrary-Scale Super-Resolution with Anatomy Guidance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yan_Adaptive_Anisotropic_Gaussian_Splatting_for_Multi-contrast_MRI_Arbitrary-Scale_Super-Resolution_with_CVPR_2026_paper.html) · [Code](https://github.com/Qiuhai-CV/GaussM2ASR) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | GaussM2ASR |
| Dataset | IXI, fastMRI |

> [!tip] 效果简介
> - IXI (T2, ref T1) 上，PSNR / SSIM (×4) 32.03 / 0.9350 vs Best baseline (lower) (Consistently best across all datasets and scales)。
> - fastMRI (FSPD, ref FD) 上，PSNR / SSIM (×4) 34.65 / 0.9621 vs Best baseline (lower) (Superior performance across all metrics)。
> - IXI (T1, ref T2) 上，PSNR / SSIM (×2) 45.39 / 0.9959 vs Best baseline (lower) (Best performance, SSIM significantly higher)。

## 概述

### 1. 问题与瓶颈

多对比度磁共振成像（MRI）任意尺度超分辨率（SR）的核心挑战在于恢复高频解剖细节。现有基于隐式神经表示（INR）的方法——如 **McASSR**（Li et al., ICCV 2023）、**Dual-ArbNet**（Zhang et al., MICCAI 2023）和 **DINet**（Wei et al., TCSVT 2025）——将图像建模为连续函数 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$，通过坐标映射直接回归像素强度。然而，这类方法存在根本性的频谱偏差：过参数化网络在梯度优化下优先收敛到低频解，且特征网格插值充当低通滤波器，进一步削弱高频信息，导致解剖边界模糊。

### 2. 核心思想与因果机制

本文提出的 **GaussM2ASR** 将图像生成范式从逐像素强度回归转变为**学习各向异性2D高斯核参数**。具体而言，模型学习 $N$ 个高斯核的均值 $\boldsymbol{\mu}$、协方差 $\boldsymbol{\Sigma}$、不透明度 $\alpha$ 和灰度级 $r$，通过 $\alpha$ 混合渲染合成像素强度：

$$f(\mathbf{x}) = \sum_{i=1}^{N} \alpha_i r_i G_i(\mathbf{x})$$

其中 $G_i(\mathbf{x})$ 为由 $\boldsymbol{\mu}_i$ 和 $\boldsymbol{\Sigma}_i$ 参数化的2D高斯概率密度函数。协方差矩阵采用标准差 $\sigma_x$、$\sigma_y$ 和相关系数 $\rho$ 参数化，使核能自适应调整方差：窄核用于高频边界，宽核用于低频平滑区域。这一范式将高频重建转化为更平滑的参数优化问题，从根本上缓解了INR的频谱偏差。

**决定性证据**：Figure 1 显示，GaussM2ASR 在定性上比 INR 模型恢复出更丰富的解剖边界；Figure 2(c) 进一步表明，在拟合高频结构方面，2DGS 模型的收敛速度显著快于 INR 方法（DINet），且最终性能更高。

### 3. 方法定位

GaussM2ASR 并非孤立地学习高斯表示，而是构建了一套**解剖引导的多对比度融合流水线**，包含三个核心模块：

- **SPMF**（结构先验调制融合）：利用参考图像统计解剖先验增强目标特征，抑制背景干扰。
- **AG-DDCA**（解剖引导双域交叉注意力）：在空间域对齐解剖结构，在频域增强高频信息，并通过动态门控融合双域特征。
- **AGGP**（解剖引导高斯参数化器）：利用参考图像解剖梯度与 Top-T 稀疏注意力，引导高斯中心聚焦于关键解剖结构。

训练采用两阶段策略：先用 HR 目标图像预训练，再冻结 AGGP 模块，以 LR 输入微调。

### 4. 主要结果

在 IXI、BraTS 和 fastMRI 三个数据集上，GaussM2ASR 在不同缩放因子下均取得最优性能（Table 2）。例如，在 IXI（T2, ref T1）的 $\times 4$ 任务上，PSNR/SSIM 达到 32.03/0.9350；在 fastMRI（FSPD, ref FD）的 $\times 4$ 任务上，PSNR/SSIM 达到 34.65/0.9621。消融实验（Figure 7）验证了 SPMF、AG-DDCA 频率分支、AGGP Top-T 稀疏注意力以及两阶段训练策略的有效性。

### 5. 局限与开放问题

该方法要求目标与参考图像空间对齐，临床场景中的患者运动可能引入错位和伪影，需配准预处理。此外，高斯核数量固定且由参考图像分辨率决定，对纹理简单图像可能导致冗余计算。未来方向包括整合鲁棒的运动校正技术，以及开发自适应高斯分配策略以提升计算效率。

## 背景与动机

### 多对比度MRI与超分辨率需求

磁共振成像（MRI）通过调节扫描参数可生成多种组织对比度（如T1加权、T2加权、FLAIR等），不同对比度揭示了互补的解剖与病理信息。在临床实践中，受限于扫描时间、患者耐受度和设备条件，高分辨率（HR）多对比度MRI往往难以获取，而低分辨率（LR）图像则丢失了关键的解剖细节。因此，从LR图像恢复HR对应物——即MRI超分辨率（SR）——成为医学影像分析中的重要预处理步骤。

多对比度MRI超分辨率的关键洞察在于：不同对比度之间共享底层解剖结构。通过将某一对比度的HR图像作为参考（reference），引导另一对比度LR目标图像（target）的SR重建，理论上可以突破单图SR的信息瓶颈。近年来，基于隐式神经表示（Implicit Neural Representation, INR）的方法在这一任务中取得了显著进展，代表性工作包括**McASSR**（Li et al., ICCV 2023）、**Dual-ArbNet**（Zhang et al., MICCAI 2023）和**DINet**（Wei et al., TCSVT 2025）。

### INR方法的频谱偏差瓶颈

尽管INR框架在连续坐标建模和任意尺度重建方面展现出优势，但其面临一个根本性问题：**频谱偏差（spectral bias）**。过参数化的神经网络在梯度优化下倾向于首先收敛到低频解，而高频分量需要更长的训练时间才能被逐步拟合。在多对比度MRI SR中，这意味着INR模型难以有效捕获高频解剖边界细节——而这恰恰是临床诊断中最关键的结构信息。

具体而言，这一瓶颈体现在两个层面：

1. **优化动力学层面**：INR将图像生成建模为连续函数 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$，通过坐标映射直接回归像素强度。在训练早期，网络输出以低频成分为主，高频解剖边缘的拟合滞后且不充分。
2. **表示层面**：连续表示中的特征网格插值本质上充当低通滤波器，进一步削弱了高频信息的传递。

**确凿证据**：如Figure 2(c)所示，在拟合高频结构方面，基于INR的DINet收敛速度明显慢于本文提出的2DGS模型，且最终性能更低。定性结果（Figure 1）也表明，Dual-ArbNet、McASSR和DINet恢复的解剖边界较为模糊，缺乏锐利的高频细节。

### 范式转换：从像素回归到基函数组合

本文的核心动机源于一个范式层面的重新思考：**是否可以将图像生成从“逐像素强度回归”转变为“自适应基函数的组合”？**

受3D高斯溅射（3D Gaussian Splatting）在场景重建中成功的启发，GaussM2ASR将2D各向异性高斯核作为可学习的基函数。每个高斯核由其均值 $\pmb{\mu}$（空间位置）、协方差矩阵 $\Sigma$（形状与方向）、不透明度 $\alpha$ 和灰度级 $r$ 参数化。最终的MRI图像通过 $\alpha$ 混合渲染生成：

$$f(\mathbf{x}) = \sum_{i=1}^{N} \alpha_i r_i G_i(\mathbf{x})$$

这一范式转换的关键优势在于：**模型可以自适应地调整每个高斯核的方差——窄核用于高频边界，宽核用于低频平滑区域——从而将高频重建转化为更平滑的参数优化问题**，从根本上缓解了INR的频谱偏差。

### 解剖先验的缺失与引入

现有INR方法在多对比度融合时，通常采用简单的特征拼接或交叉注意力，缺乏对解剖结构的显式建模。这导致两个问题：（1）参考图像中的背景区域引入噪声干扰；（2）高斯中心无法有效聚焦于关键解剖结构。

为此，GaussM2ASR引入了三大解剖先验驱动模块：**SPMF**（结构先验调制融合）抑制背景并增强高频通道，**AG-DDCA**（解剖引导双域交叉注意力）在空间域和频域联合增强解剖细节，**AGGP**（解剖引导高斯参数化器）利用梯度引导的Top-T稀疏注意力将高斯中心聚焦于解剖边缘。这些模块共同构成了一个完整的解剖引导管线，使2D高斯溅射在医学影像场景中发挥最大效能。

## 核心创新

### 从像素回归到自适应基函数合成：范式转变

传统基于隐式神经表示（INR）的多对比度MRI超分辨率方法将图像重建建模为连续映射 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$，即从二维坐标直接回归像素强度。这类方法的根本瓶颈在于**频谱偏差**（spectral bias）：过参数化网络在梯度优化下优先收敛到低频解，且特征网格插值充当低通滤波器，进一步削弱高频信息，导致解剖边界模糊。**McASSR**（Li et al., ICCV 2023）、**Dual-ArbNet**（Zhang et al., MICCAI 2023）和**DINet**（Wei et al., TCSVT 2025）等代表性INR方法均受此制约。

GaussM2ASR的核心范式转变在于：**将图像生成从像素强度回归转化为学习一组各向异性2D高斯核的参数** $(\boldsymbol{\mu}, \Sigma, \alpha, r)$，并通过 $\alpha$ 混合渲染合成图像。具体而言，对于 $N$ 个高斯核，任意空间位置 $\mathbf{x}$ 处的渲染值为：

$$f(\mathbf{x}) = \sum_{i=1}^{N} \alpha_i r_i G_i(\mathbf{x})$$

其中每个高斯核 $G_i(\mathbf{x})$ 由均值 $\boldsymbol{\mu}$ 和协方差矩阵 $\Sigma$ 参数化：

$$G(\mathbf{x}) = \frac{1}{2\pi |\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^{\top} \Sigma^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)$$

协方差矩阵 $\Sigma$ 进一步分解为标准差 $\sigma_x, \sigma_y$ 和相关系数 $\rho$，赋予核各向异性能力：

$$\Sigma = \begin{bmatrix} \sigma_x^2 & \rho\sigma_x\sigma_y \\ \rho\sigma_x\sigma_y & \sigma_y^2 \end{bmatrix}$$

这一设计的因果机制在于：**模型可自适应调整核的方差——在解剖边界等高频区域学习窄核以保留锐利边缘，在平滑区域学习宽核以维持结构连续性**，从而将高频重建转化为更平滑的参数优化问题，从根本上规避了INR的频谱偏差。收敛行为分析（Figure 2(c)）提供了直接证据：GaussM2ASR在拟合高频结构时的收敛速度显著快于INR方法DINet，且最终性能更高。

### 三大解剖先验驱动模块：从无引导到结构化注入

现有INR方法通常缺乏显式的解剖先验集成，或仅进行简单的特征拼接融合。GaussM2ASR引入三个解剖引导模块，形成结构化的先验注入管线：

**（1）结构先验调制融合（SPMF）**：针对多对比度MRI融合中背景区域的无效信息和分布偏移，SPMF从参考图像统计中提取解剖先验。首先对参考特征进行全局平均池化，经卷积生成通道级仿射参数 $(\gamma, \beta)$，对目标特征执行调制：

$$\hat{F}_{\text{tar}} = (1 + \gamma) \odot F_{\text{tar}} + \beta$$

随后通过拼接特征的门控机制生成像素级权重 $g$，在结构显著区域保留调制特征，在无关区域采用参考特征，实现背景抑制：

$$\tilde{F}_{\text{tar}} = g \odot \hat{F}_{\text{tar}} + (1 - g) \odot F_{\text{ref}}$$

**（2）解剖引导双域交叉注意力（AG-DDCA）**：在空间域对齐解剖结构，在频域增强高频信息。空间注意力 $\text{Att}_{\text{spat}}$ 和频域注意力 $\text{Att}_{\text{freq}}$ 分别以高斯提示为查询，通过动态门控融合双域输出：

$$F = \epsilon_s \odot \text{Att}_{\text{spat}} + \epsilon_f \odot \text{Att}_{\text{freq}}$$

**（3）解剖引导高斯参数化器（AGGP）**：利用参考图像的解剖梯度特征作为查询，通过Top-T稀疏注意力机制引导高斯中心聚焦于关键解剖结构。每行仅保留前 $T$ 个最大注意力值：

$$M_{ij} = \begin{cases} 1, & \text{if } j \in \text{Top}_T(W_{i,:}) \\ 0, & \text{otherwise} \end{cases}$$

$$\text{Att}_{\text{top-T}}(Q, K, V) = \text{Softmax}(M \odot W) V$$

此外，高斯中心采用均匀初始化位置 $\boldsymbol{\mu}_i$ 加预测偏移 $\boldsymbol{\mu}_o$ 的方式获得 $\boldsymbol{\mu} = \boldsymbol{\mu}_i + \boldsymbol{\mu}_o$，避免直接预测坐标导致的优化空间过大和收敛无效问题。

### 两阶段训练策略

GaussM2ASR采用两阶段训练：首先使用高分辨率目标图像预训练整个网络，随后冻结AGGP模块，使用低分辨率输入微调其余部分。消融实验（Figure 7）表明，两阶段策略优于单阶段训练，验证了先让高斯参数化器在高质量监督下学习解剖聚焦，再适应降质输入的有效性。

## 整体框架

GaussM2ASR 的整体流水线将多对比度 MRI 任意尺度超分辨率重构为**可学习的各向异性 2D 高斯参数估计与 α 混合渲染**问题，从根本上区别于基于隐式神经表示（INR）的逐像素强度回归范式。其核心因果机制在于：INR 的过参数化网络在梯度优化下天然存在频谱偏差——优先收敛到低频解，且连续表示中的特征网格插值充当低通滤波器，进一步削弱高频解剖边界；GaussM2ASR 转而学习一组自适应基函数（各向异性高斯核），将高频重建转化为更平滑的参数优化问题，窄核捕获边界细节，宽核覆盖平滑区域。

### 两阶段训练策略

框架采用**两阶段训练**设计（Figure 3），以解耦高斯中心定位与 LR 输入退化的耦合关系：

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed GaussM2ASR, which adopts a two-stage training strategy: pre-training with HR target images, followed by fine-tuning with LR inputs while freezing the Anatomy Guided Gaussian Parametrizer (AGGP) module*

1. **第一阶段（预训练）**：以 HR 目标图像作为输入，训练完整的 GaussM2ASR 流水线，使各模块在无退化干扰的条件下学习高质量的解剖先验和高斯参数。
2. **第二阶段（微调）**：将输入切换为 LR 目标图像，同时**冻结解剖引导高斯参数化器（AGGP）**，仅微调其余模块以适应低分辨率输入的特征分布。

该设计的必要性由消融实验验证：单阶段训练相比两阶段策略在 PSNR/SSIM 上显著下降（Figure 7），表明直接以 LR 输入端到端训练会扩大高斯中心的优化空间，导致收敛失效。

### 模块化流水线

GaussM2ASR 的推理流水线由六个串行模块构成，输入为 LR 目标图像与 HR 参考图像（不同对比度），输出为任意尺度的 SR 重建：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **CSMF 编码器** | 提取 LR 目标与 HR 参考图像的多尺度深度特征 | LR 目标 + HR 参考 | 多尺度特征图 |
| **SPMF** | 利用参考解剖先验调制目标特征，抑制背景干扰 | 目标特征 + 参考特征 | 增强的目标特征 |
| **AG-DDCA** | 空间域对齐解剖结构 + 频域增强高频信息，动态门控融合 | SPMF 输出 + 高斯提示 | 双域增强特征 |
| **Gaussian Transformer** | 增强表示间的全局连贯性 | AG-DDCA 输出 | 全局上下文特征 |
| **AGGP** | 以参考梯度引导 Top-T 稀疏注意力，回归高斯参数（均值偏移、协方差、不透明度、灰度级） | Transformer 输出 + 参考梯度 | N 组高斯参数 |
| **2D Gaussian Splatting Renderer** | 通过 α 混合渲染连续空间中的高保真 SR 图像 | 高斯参数 + 查询坐标 | SR 重建图像 |

### 关键数据流与设计动机

**SPMF→AG-DDCA→AGGP 的级联解剖引导**：SPMF 通过通道仿射变换和像素级门控抑制背景无关区域的激活（Figure 6 验证了其有效性）；AG-DDCA 在空间域和频域分别执行交叉注意力，空间分支对齐跨对比度的解剖结构，频率分支增强高频分量，二者通过可学习的条件门控动态融合；AGGP 利用参考图像的解剖梯度作为 Query，通过 Top-T 稀疏注意力强制高斯中心聚焦于解剖边界，再以三层 MLP 从注意力特征中回归中心偏移量 $\pmb{\mu}_o$，与均匀初始位置相加得到最终高斯中心 $\pmb{\mu} = \pmb{\mu}_i + \pmb{\mu}_o$。

**渲染端的自适应基函数组合**：每个高斯核由均值 $\pmb{\mu}$、协方差矩阵 $\Sigma$（参数化为 $\sigma_x, \sigma_y, \rho$）、不透明度 $\alpha$ 和灰度级 $r$ 定义。最终像素强度由 N 个高斯核的 α 混合给出：

$$f(\mathbf{x}) = \sum_{i=1}^{N} \alpha_i r_i G_i(\mathbf{x})$$

其中 $G_i(\mathbf{x})$ 为 2D 高斯概率密度函数。Figure 5 的可视化证实：学习到的高斯中心密集分布于高频解剖边界区域，且方差根据局部频率特性自适应调整——边界处窄核产生锐利响应，平滑区域宽核维持连续性。

**训练目标**：总损失函数组合空间域 MAE、频域 MAE 和参考重建损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{spa}} + \lambda_{\mathrm{freq}} \mathcal{L}_{\mathrm{freq}} + \lambda_{\mathrm{ref}} \mathcal{L}_{\mathrm{ref}}$$

频域损失直接监督高频分量的重建质量，与频谱偏差缓解的设计目标一致。

## 核心模块与公式推导

### 3.1 各向异性2D高斯溅射渲染

GaussM2ASR 的核心范式转换在于将图像生成从像素强度回归转变为学习一组可学习的各向异性2D高斯核参数。对于空间位置 $\mathbf{x} \in \mathbb{R}^2$，每个高斯核由概率密度函数定义：

$$G ( { \bf x } ) = \frac { 1 } { 2 \pi | \Sigma | ^ { 1 / 2 } } \exp \left( - \frac { 1 } { 2 } ( { \bf x } - { \pmb \mu } ) ^ { \top } \Sigma ^ { - 1 } ( { \bf x } - { \pmb \mu } ) \right)$$

其中 $\pmb{\mu} \in \mathbb{R}^2$ 为高斯核的空间均值，控制核的中心位置；协方差矩阵 $\Sigma \in \mathbb{R}^{2 \times 2}$ 刻画核的各向异性形状，其参数化形式为：

$$\Sigma = \left[ \begin{array} { c c } { \sigma _ { x } ^ { 2 } } & { \rho \sigma _ { x } \sigma _ { y } } \\ { \rho \sigma _ { x } \sigma _ { y } } & { \sigma _ { y } ^ { 2 } } \end{array} \right]$$

其中 $\sigma_x > 0$、$\sigma_y > 0$ 分别为 $x$ 和 $y$ 方向的标准差，$\rho \in (-1, 1)$ 为相关系数。这三个参数共同决定了高斯核的延展方向与各向异性程度：当 $\sigma_x \approx \sigma_y$ 且 $\rho \approx 0$ 时核近似各向同性，适用于平滑区域；当某一方向方差显著较小且 $|\rho|$ 较大时，核沿特定方向变窄，能够精准贴合高频解剖边界。

最终，图像在任意连续坐标 $\mathbf{x}$ 处的像素强度由 $N$ 个高斯核经 $\alpha$ 混合渲染得到：

$$f ( \mathbf { x } ) = \sum _ { i = 1 } ^ { N } \alpha _ { i } r _ { i } G _ { i } ( \mathbf { x } )$$

其中 $\alpha_i \in [0, 1]$ 为第 $i$ 个高斯核的不透明度，$r_i \in \mathbb{R}$ 为其灰度强度值。这一显式基函数组合的渲染方式，使模型能够自适应调整核的方差——窄核用于高频边界，宽核用于低频平滑区域——从而将高频重建转化为更平滑的参数优化问题，从根本上缓解了 INR 方法的频谱偏差。

### 3.2 解剖引导的三大核心模块

GaussM2ASR 整体框架采用两阶段训练策略：第一阶段使用 HR 目标图像预训练，第二阶段冻结解剖引导高斯参数化器（AGGP）并以 LR 输入微调。框架包含三个关键模块，分别从特征增强、双域对齐和高斯参数引导三个层面注入解剖先验。

#### 3.2.1 结构先验调制融合（SPMF）

多对比度 MRI 融合面临两大挑战：背景等非信息区域的干扰，以及不同对比度间的分布偏移。SPMF 模块位于跨尺度多对比度融合（CSMF）编码器之后，通过通道级仿射变换与空间门控机制解决上述问题。

首先，对参考图像特征 $F_{\mathrm{ref}}$ 进行全局平均池化（GAP），经卷积网络 $\Phi$ 生成通道级缩放参数 $\gamma$ 和偏置参数 $\beta$：

$$( \gamma , \beta ) = \Phi ( \mathrm { G A P } ( F _ { \mathrm { r e f } } ) )$$

随后对目标特征 $F_{\mathrm{tar}}$ 施加通道仿射调制，增强与高频结构相关的通道响应：

$$\hat { F } _ { \mathrm { t a r } } = \left( 1 + \gamma \right) \odot F _ { \mathrm { t a r } } + \beta$$

为进一步抑制背景区域，SPMF 通过拼接调制后的目标特征与参考特征，经卷积与 Sigmoid 激活生成像素级门控权重：

$$g = \mathrm { S i g m o i d } ( \Phi ( \mathrm { C o n c a t } [ \hat { F } _ { \mathrm { t a r } } , F _ { \mathrm { r e f } } ] ) )$$

最终的空间精炼操作在结构显著区域保留调制目标特征，在无关区域采用参考特征：

$$\tilde { F } _ { \mathrm { t a r } } = g \odot \hat { F } _ { \mathrm { t a r } } + ( 1 - g ) \odot F _ { \mathrm { r e f } }$$

消融实验表明，移除 SPMF 模块导致 PSNR/SSIM 明显下降，验证了结构先验调制融合的有效性。

#### 3.2.2 解剖引导双域交叉注意力（AG-DDCA）

AG-DDCA 模块在空间域和频域分别执行交叉注意力，以同时对齐解剖结构并增强高频信息。空间域注意力以高斯提示 $Q$ 为查询，目标与参考的空间特征为键 $K_s$ 和值 $V_s$：

$$\mathrm { A t t _ { s p a t } } = \mathrm { S o f t m a x } ( Q K _ { s } ^ { \top } + B ) V _ { s }$$

频域注意力则将键 $K_f$ 和值 $V_f$ 替换为傅里叶幅度表示，以显式增强高频分量：

$$\mathrm { A t t } _ { \mathrm { f r e q } } = \mathrm { S o f t m a x } ( Q K _ { f } ^ { \top } + B ) V _ { f }$$

双域特征通过可学习的条件门控 $\epsilon_s$ 和 $\epsilon_f$ 进行动态融合：

$$F = \epsilon _ { s } \odot \mathrm { A t t } _ { \mathrm { s p a t } } + \epsilon _ { f } \odot \mathrm { A t t } _ { \mathrm { f r e q } }$$

消融实验中，移除频域分支会降低高频细节恢复，导致性能下降，证实了频域注意力对高频重建的关键作用。

#### 3.2.3 解剖引导高斯参数化器（AGGP）

AGGP 模块负责从增强后的特征中回归高斯核参数，其核心创新在于利用参考图像的解剖梯度引导高斯中心聚焦于关键解剖结构。具体而言，AGGP 计算梯度特征 $Q$ 与高维特征 $K$ 的缩放点积注意力分数：

$$W = \frac { Q K ^ { \top } } { \tau }$$

其中 $\tau$ 为温度系数。为避免注意力分散于均匀背景区域，AGGP 引入 Top-T 稀疏掩码，每行仅保留前 $T$ 个最大注意力值：

$$M _ { i j } = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f ~ } j \in \operatorname { T o p } _ { T } ( W _ { i , : } ) , } \\ { 0 , } & { \mathrm { o t h e r w i s e } } \end{array} \right.$$

最终的稀疏交叉注意力为：

$$\operatorname { A t t } _ { \operatorname { t o p } \cdot \mathrm { T } } ( Q , K , V ) = \operatorname { S o f t m a x } \left( M \odot W \right) V$$

消融分析表明，移除 Top-T 稀疏注意力会显著降低性能，验证了稀疏注意力对引导高斯中心聚焦于解剖边界的关键作用。此外，高斯中心 $\pmb{\mu}$ 由均匀初始化位置 $\pmb{\mu}_i$ 与三层 MLP 预测的偏移 $\pmb{\mu}_o$ 相加得到（$\pmb{\mu} = \pmb{\mu}_i + \pmb{\mu}_o$）；若去除均匀初始化位置直接预测坐标，优化空间扩大将导致高斯中心无法有效收敛。

### 3.3 训练目标

总损失函数由三项加权组合构成：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { s p a } } + \lambda _ { \mathrm { f r e q } } \mathcal { L } _ { \mathrm { f r e q } } + \lambda _ { \mathrm { r e f } } \mathcal { L } _ { \mathrm { r e f } }$$

其中 $\mathcal{L}_{\mathrm{spa}}$ 为空间域 MAE 损失，$\mathcal{L}_{\mathrm{freq}}$ 为频域 MAE 损失（在傅里叶幅度上计算），$\mathcal{L}_{\mathrm{ref}}$ 为参考图像的重建损失。$\lambda_{\mathrm{freq}}$ 和 $\lambda_{\mathrm{ref}}$ 为平衡超参数。两阶段训练策略（预训练 HR 目标 + 冻结 AGGP 微调 LR 输入）在消融实验中优于单阶段训练，进一步验证了该设计的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/002_Figure_2.jpg]]
*Figure 2: Compared with INR models that directly regress pixel intensities, our GaussM2ASR learns a set of Gaussian parameters and reconstructs the image as a composition of adaptive basis functions, enabling more effective modeling of high-frequency anatomical structures*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/007_Figure_5.jpg]]
*Figure 5: Illustration of how the generated Gaussians render the MRI image, by showing their spatial distribution in (c) and a random subset in (d). The distribution in (c) concentrates on HF regions, particularly along anatomical boundaries, while the subset in (d) demonstrates the adaptive adjustment of their variances to local frequency characteristics*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/009_Figure_6.jpg]]
*Figure 6: Feature responses before and after the SPMF module, along with their residual map. The results demonstrate the module’s efficacy in suppressing activations in background and other irrelevant regions*

## 实验与分析

### 主实验结果

GaussM2ASR 在三个公开数据集（IXI、BraTS、fastMRI）上，针对多对比度 MRI 任意尺度超分辨率任务，全面评估了其性能。实验设置涵盖 ×2、×3、×4 的尺度内（in-scale）和跨尺度（out-of-scale）超分辨率。表 2 汇总了 GaussM2ASR 与现有方法的定量对比结果。

在 IXI 数据集上，以 T2 为目标、T1 为参考的 ×4 超分辨率任务中，GaussM2ASR 取得了 **32.03 dB PSNR / 0.9350 SSIM** 的最佳性能。在 fastMRI 数据集上（FSPD 为目标、FD 为参考，×4），模型同样以 **34.65 dB PSNR / 0.9621 SSIM** 显著领先。在 ×2 的简单尺度下，GaussM2ASR 的 SSIM 优势尤为突出，例如 IXI T1（参考 T2）任务上达到 **45.39 dB PSNR / 0.9959 SSIM**，表明其在低倍率放大时几乎完美地保留了结构信息。

**关键对比**：相较于 INR 类方法（如 **McASSR** (Li et al., ICCV 2023)、**Dual-ArbNet** (Zhang et al., MICCAI 2023)、**DINet** (Wei et al., TCSVT 2025)），GaussM2ASR 在所有尺度和数据集上均一致取得最优。其核心优势源于将图像生成范式从像素强度回归转变为各向异性 2D 高斯参数学习，从而将高频解剖边界的重建转化为更平滑的参数优化问题。图 2(c) 的收敛行为分析直接验证了这一机制：GaussM2ASR 在拟合高频结构时，收敛速度显著快于 INR 方法 DINet，且最终性能更高。

定性对比（图 4）进一步佐证了定量结果。在 ×4 缩放因子下，GaussM2ASR 重建的解剖边界更清晰锐利，误差图（error map）中的绝对重建误差更小。尤其在脑沟回、白质-灰质交界等高频区域，INR 方法普遍存在模糊或振铃伪影，而 GaussM2ASR 则恢复了更丰富的纹理细节。

### 学习的高斯核特性分析

图 5 直观展示了 GaussM2ASR 所学习的高斯核的空间分布与自适应方差特性。高斯中心（图 5c）高度集中于高频区域，尤其是解剖边界沿线，这验证了 AGGP 模块中 Top-T 稀疏注意力机制的有效性——它成功引导高斯核聚焦于关键结构。随机采样的高斯核子集（图 5d）进一步表明，模型能根据局部频率特性自适应调整核的方差：窄核用于锐利边界，宽核用于平滑区域。这种自适应基函数的组合从根本上缓解了 INR 的频谱偏差问题。

### 消融实验

为系统评估各组件的贡献，在 IXI 数据集 ×4 任务上进行了消融研究（图 7）。

**SPMF 模块**：移除结构先验调制融合（w/o SPMF）导致 PSNR/SSIM 明显下降。图 6 的特征响应可视化揭示了其作用机制——SPMF 有效抑制了背景及无关区域的激活，使模型聚焦于解剖结构区域。该模块通过通道级仿射变换和像素级门控，利用参考图像的统计先验增强了目标特征中的高频结构通道。

**AG-DDCA 模块**：移除频域分支（w/o freq）后性能下降，证实了频域交叉注意力对增强高频信息的重要性。AG-DDCA 在空间域对齐解剖结构，在频域通过傅里叶幅度表示增强高频分量，并通过动态门控融合双域特征，这一设计对恢复精细边界至关重要。

**AGGP 模块**：对 AGGP 的深入分析揭示了两个关键设计选择。移除 Top-T 稀疏注意力（w/o Top-T）显著影响性能，表明稀疏注意力对引导高斯中心聚焦于解剖边缘不可或缺。放弃均匀初始位置并直接预测高斯中心（w/o μᵢ）会扩大优化空间，导致高斯中心无法有效收敛。这验证了“初始位置 + 学习偏移”的参数化策略对稳定训练的必要性。

**训练策略**：两阶段训练策略（预训练 HR 目标 + 冻结 AGGP 微调 LR 输入）优于单阶段训练。这一发现表明，先在高分辨率目标上学习稳定的高斯参数先验，再适配低分辨率输入，能有效降低优化难度。

### 失败模式与局限性

尽管 GaussM2ASR 在定量和定性上均表现优异，但其存在两个已知局限：

1. **空间对齐依赖**：模型假设目标与参考图像已精确配准。在临床实际中，患者运动可能引入错位和伪影，因此多对比度图像配准是必要的预处理步骤。当配准质量下降时，解剖先验的引导作用可能减弱甚至引入误导信息。
2. **固定高斯核数量**：高斯核数量由参考图像分辨率决定且固定不变。对于纹理简单的图像区域，这会导致冗余计算，降低推理效率。当前缺乏根据图像内容动态调整核数量的自适应分配策略。

### 开放问题

基于上述局限性，值得进一步探索的方向包括：
- 如何整合鲁棒的运动校正技术，使模型能处理未对齐或存在运动伪影的多对比度图像？
- 如何开发自适应的高斯分配策略，根据局部纹理复杂度动态调整高斯核数量，以提升纹理简单图像的计算效率？

### 补充图表

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on IXI, BraTS, and fastMRI datasets under different scaling factors. Red indicates the best and blue the second best performance*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/004_Table_1.jpg]]
*Table 1: Details of three datasets used in experiments*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/001_Figure_1.jpg]]
*Figure 1: The proposed GaussM2ASR recovers richer anatomical boundaries than INR-based models, e.g., Dual-ArbNet [41], McASSR [16], and DINet [36]*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/008_Figure_7.jpg]]
*Figure 7: Ablation study of GaussM2ASR, with all models trained on the IXI dataset and tested at a 4× upscaling factor*

![[assets/figures/papers/paper_list_l2437_https_openaccess_thecvf_com_content_CVPR2026_html_Yan_Adaptive_Anisotrop/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on IXI, BraTS, and fastMRI datasets at a 4× scaling factor. Enlarged views of regions within green boxes are provided alongside their error maps, which display the absolute reconstruction error (darker shades indicate smaller errors)*

## 方法谱系与知识库定位

### 1. 问题域定位：从隐式神经表示到显式基函数合成

GaussM2ASR 的核心贡献在于将多对比度 MRI 任意尺度超分辨率（Arbitrary-scale Multi-contrast MRI SR）的图像生成范式，从**隐式神经表示（INR）的像素强度回归**，根本性地转变为**显式各向异性 2D 高斯溅射的参数学习与 α 混合渲染**。这一转变瞄准了 INR 方法在该任务中长期存在的结构性瓶颈。

#### 1.1 INR 范式的频谱偏差瓶颈

基于 INR 的方法，如 **Dual-ArbNet**（Zhang et al., MICCAI 2023）、**McASSR**（Li et al., ICCV 2023）和 **DINet**（Wei et al., TCSVT 2025），将图像建模为从 2D 坐标到像素强度的连续函数 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$。尽管这类方法天然支持任意尺度重建，但存在一个根本性缺陷：**频谱偏差（spectral bias）**。过参数化的网络在梯度优化下倾向于优先收敛到低频分量，导致重建结果中高频解剖边界模糊。此外，连续表示中的特征网格插值操作本质上充当低通滤波器，进一步削弱了高频信息的保留。Figure 2(c) 的收敛分析直接验证了这一机制：INR 方法（DINet）在拟合高频结构时收敛缓慢且最终性能受限，而 GaussM2ASR 在高频恢复上展现出显著加速和更优的收敛行为。

#### 1.2 范式转换的因果机制

GaussM2ASR 的因果调控点在于：**将高频重建这一困难任务，转化为更平滑的参数优化问题**。具体而言，模型不再逐像素预测强度值，而是学习 $N$ 个各向异性 2D 高斯核的参数——均值 $\pmb{\mu}$、协方差矩阵 $\Sigma$（由标准差 $\sigma_x, \sigma_y$ 和相关系数 $\rho$ 参数化）、不透明度 $\alpha$ 和灰度级 $r$。每个高斯核作为一个自适应的基函数，其形状可随局部频率特性动态调整：窄核捕获高频解剖边界，宽核覆盖低频平滑区域。最终图像通过 α 混合渲染合成：

$$f(\mathbf{x}) = \sum_{i=1}^{N} \alpha_i r_i G_i(\mathbf{x})$$

这种“基函数组合”策略从根本上缓解了 INR 的频谱偏差。Figure 5 的可视化直接证实了这一机制：学习到的高斯中心在空间上高度集中于解剖边界等高频区域，且核的方差自适应地匹配局部频率特征。

### 2. 与基线方法的结构化差异

GaussM2ASR 与现有 INR 方法在三个关键维度上存在结构性差异：

| 维度 | INR 基线（McASSR, Dual-ArbNet, DINet） | GaussM2ASR |
|------|----------------------------------------|------------|
| **图像生成范式** | 隐式函数 $f: \mathbb{R}^2 \rightarrow \mathbb{R}$，逐像素回归强度 | 显式 2D 各向异性高斯溅射，通过 α 混合渲染合成图像 |
| **高频处理机制** | 依赖网络隐式学习，受频谱偏差制约 | 通过自适应核方差显式建模：窄核增强边界，宽核平滑区域 |
| **解剖先验集成** | 无显式解剖引导或简单特征融合 | 三大解剖先验驱动模块：SPMF（结构先验调制融合）、AG-DDCA（解剖引导双域交叉注意力）、AGGP（解剖引导高斯参数化器） |

#### 2.1 SPMF：结构先验调制融合

SPMF 模块解决多对比度融合中两个关键问题：无信息背景区域的干扰和模态间的分布偏移。其机制是通过参考图像特征 $F_{\mathrm{ref}}$ 的全局统计量生成通道级仿射参数 $(\gamma, \beta)$，对目标特征进行调制：

$$\hat{F}_{\mathrm{tar}} = (1 + \gamma) \odot F_{\mathrm{tar}} + \beta$$

随后通过像素级门控 $g$ 在结构显著区域保留调制特征，在无关区域采用参考特征，实现背景抑制。Figure 6 的特征响应可视化证实了 SPMF 有效抑制了背景区域的激活。

#### 2.2 AG-DDCA：双域交叉注意力

AG-DDCA 在空间域和频域同时执行交叉注意力。空间分支 ${\mathrm{Att}_{\mathrm{spat}}}$ 对齐解剖结构，频率分支 ${\mathrm{Att}_{\mathrm{freq}}}$ 通过傅里叶幅度表示增强高频分量。双域特征通过动态门控 $\epsilon_s, \epsilon_f$ 融合：

$$F = \epsilon_s \odot \mathrm{Att}_{\mathrm{spat}} + \epsilon_f \odot \mathrm{Att}_{\mathrm{freq}}$$

消融实验表明，移除频率分支会显著降低高频细节恢复，导致 PSNR/SSIM 下降。

#### 2.3 AGGP：解剖引导高斯参数化器

AGGP 利用参考图像的解剖梯度作为查询 $Q$，通过 Top-T 稀疏注意力机制引导高斯中心聚焦于关键解剖结构。稀疏掩码 $M$ 每行仅保留前 $T$ 个最大注意力值：

$$M_{ij} = \begin{cases} 1, & \text{if } j \in \operatorname{Top}_T(W_{i,:}) \\ 0, & \text{otherwise} \end{cases}$$

消融实验揭示了两个关键设计：移除 Top-T 稀疏注意力会显著影响性能；去掉均匀初始位置 $\pmb{\mu}_i$ 并直接预测高斯坐标会扩大优化空间，导致高斯中心无法有效收敛。

### 3. 训练策略与损失函数

GaussM2ASR 采用两阶段训练策略：第一阶段使用 HR 目标图像预训练，第二阶段冻结 AGGP 模块并用 LR 输入微调。消融实验证实两阶段策略优于单阶段。总损失函数组合了空间 MAE 损失、频域 MAE 损失和参考重建损失：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{spa}} + \lambda_{\mathrm{freq}} \mathcal{L}_{\mathrm{freq}} + \lambda_{\mathrm{ref}} \mathcal{L}_{\mathrm{ref}}$$

### 4. 适用边界与局限

#### 4.1 空间对齐假设

GaussM2ASR 要求目标图像与参考图像在空间上严格对齐。在临床实际场景中，患者运动可能引入错位和伪影，因此多对比图像配准是必要的预处理步骤。这一约束限制了模型在未配准数据上的直接应用。

#### 4.2 高斯核数量固定

高斯核的数量固定且由参考图像分辨率决定。对于纹理较简单的图像区域，固定数量的高斯核可能导致冗余计算，降低推理效率。这一问题在临床部署中需要考虑。

#### 4.3 开放问题

基于上述局限，两个核心开放问题值得关注：

1. **鲁棒运动校正集成**：如何整合鲁棒的运动校正技术，使模型能处理未对齐或存在运动伪影的多对比图像，从而扩展临床适用性？
2. **自适应高斯分配**：如何开发自适应的高斯分配策略，根据图像内容动态调整高斯核数量，在保持重建质量的同时提升纹理简单图像的计算效率？

## 原文 PDF

![[paperPDFs/CVPR_2026/Adaptive_Anisotropic_Gaussian_Splatting_for_Multi_contrast_MRI_Arbitrary_Scale_Super_Resolution_with_Anatomy_Guidance.pdf]]
