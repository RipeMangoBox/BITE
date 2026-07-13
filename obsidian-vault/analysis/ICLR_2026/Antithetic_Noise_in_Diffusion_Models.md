---
title: "Antithetic Noise in Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Antithetic_Noise_in_Diffusion_Models.pdf
project_link: null
code_link: https://github.com/jjia131/Antithetic-Noise-in-Diffusion-Models-page
aliases:
- ANDM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "The method pairs diffusion initial noise z with -z and uses the negatively correlated outputs in antithetic Monte Carlo estimates."
primary_logic: "Approximate affine anti-symmetry of the score network preserves negative correlation through deterministic sampling, reducing estimator variance without extra model calls."
claims:
- "Generated samples from paired antithetic noise exhibit strong negative correlation across architectures and datasets."
- "AMC narrows confidence intervals for image statistics compared with ordinary Monte Carlo."
- "The same noise design can improve image editing quality and diversity without added compute."
---

# Antithetic Noise in Diffusion Models

> [!tip] 核心洞察
> 学习到的分数函数 ε_θ^{(t)} 近似满足仿射反对称性：ε_θ^{(t)}(x) + ε_θ^{(t)}(-x) ≈ 2c_t。这一性质使得对偶噪声对 (z, -z) 在DDIM等确定性采样过程中始终保持强负相关，从而可作为控制变量实现方差缩减，且不增加计算开销。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散模型中的对偶噪声 |
| 英文题名 | Antithetic Noise in Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9yFORC1tu3) · [GitHub](https://github.com/jjia131/Antithetic-Noise-in-Diffusion-Models-page) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Antithetic Noise in Diffusion Models |
| Dataset | CIFAR-10, CelebA-HQ, DPS Inpainting, DPS Super-resolution |

> [!tip] 效果简介
> - CIFAR-10 上，Brightness CI length (efficiency) 为 0.35 (32.66)，对比 2.00，变化 效率提升32.66倍。
> - CelebA-HQ 上，Brightness CI length (efficiency) 为 0.15 (130.69)，对比 1.77，变化 效率提升130.69倍。
> - DPS Inpainting 上，L1 efficiency 为 1.54，对比 1.0，变化 效率提升54%。

## 概要

本文发现并系统验证了一个简单而普适的现象：在扩散模型中，将每个初始高斯噪声向量 z 与其相反数 -z 配对（对偶采样），生成的图像对之间存在强负相关。这一现象在 U-Net、DiT、一致性模型、VAE、Glow 等多种架构以及 CIFAR-10、CelebA-HQ、LSUN-Church、ImageNet 等多个数据集上均被观测到。基于此，作者提出了对偶蒙特卡洛（Antithetic Monte Carlo, AMC）估计器，用于扩散模型的不确定性量化，在像素级统计量上实现了相对于普通蒙特卡洛最高 136 倍的效率提升，置信区间最多缩窄 90%。此外，对偶噪声设计还能在不增加计算开销的前提下提升图像编辑质量和生成多样性。

扩散模型中的初始高斯噪声是采样过程的唯一随机性来源。然而，现有工作多针对特定任务优化初始噪声，缺乏对其普遍性质的理论认识。本文的核心动机是系统理解初始噪声的特性，并利用其内在结构实现方差缩减。

扩散模型的反向采样过程可通过概率流常微分方程（PF-ODE）描述：

\[
\mathrm { d } { \mathbf y } _ { t } = \left( - \mu ( { \mathbf y } _ { t } , t ) - \frac { 1 } { 2 } \sigma _ { t } ^ { 2 } \nabla \log p ( { \mathbf y } _ { t } , t ) \right) \mathrm { d } t
\]

本文主要关注确定性采样器（如DDIM），其离散更新规则为：

\[
\mathbf { y } _ { t - 1 } = \sqrt { \alpha _ { t - 1 } } \left( \frac { \mathbf { y } _ { t } - \sqrt { 1 - \alpha _ { t } } \epsilon _ { \theta } ^ { ( t ) } ( \mathbf { y } _ { t } ) } { \sqrt { \alpha _ { t } } } \right) + \sqrt { 1 - \alpha _ { t - 1 } } \epsilon _ { \theta } ^ { ( t ) } ( \mathbf { y } _ { t } )
\]

## 核心方法与创新机理

本文的核心创新在于：

1. **发现分数网络的仿射反对称性**：学习到的分数函数 ε_θ^{(t)} 近似满足仿射反对称性：ε_θ^{(t)}(x) + ε_θ^{(t)}(-x) ≈ 2c_t。这一性质使得对偶噪声对 (z, -z) 在DDIM等确定性采样过程中始终保持强负相关。

2. **提出对偶蒙特卡洛（AMC）估计器**：利用对偶噪声对的强负相关作为控制变量实现方差缩减，且不增加计算开销。

3. **推广到K-对偶和随机化拟蒙特卡洛（RQMC）**：将对偶思想推广到更一般的负相关噪声设计，进一步提升了方差缩减效果。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/001_Figure_1.jpg]]
*Figure 1: Use antithetic noise −z and z (with condition c) to generate visually “opposite” images.*

本文的方法框架包含四个核心模块：

1. **对偶噪声生成**：生成 K 对对偶标准高斯噪声向量 (z_i, -z_i)，其中 z_i ~ N(0, I)，总样本数 N=2K。

2. **扩散模型采样**：使用确定性采样器（如DDIM）将每个初始噪声映射为生成样本。

3. **统计量计算**：对每对样本计算目标统计量 S(DM(z_i)) 和 S(DM(-z_i))。

4. **对偶平均与估计**：计算每对对偶样本的平均值，再对所有K个平均值取平均得到AMC估计。

### 5.1 对偶蒙特卡洛估计器

标准蒙特卡洛估计器为：

\[
\hat{\mu}_N^{MC} := \sum_{i=1}^N S_i / N
\]

对偶蒙特卡洛估计器为：

\[
\hat{\mu}_N^{AMC} := \sum_{i=1}^K \bar{S}_i / K
\]

其中 \(\bar{S}_i = 0.5(S_i^+ + S_i^-)\) 为每对对偶样本的平均值。

AMC估计器的置信区间为：

\[
\hat{\mu}_N^{AMC} \pm z_{1-\alpha/2} \sqrt{2(\hat{\sigma}_N^{AMC})^2 / N}
\]

当相关系数 ρ = Corr(S_i^+, S_i^-) 为负时，AMC的标准误差是MC标准误差的 √(1+ρ) 倍，因此产生更紧的置信区间。

### 5.2 K-对偶噪声构造

从K个独立标准高斯向量构造K个两两相关系数为 -1/(K-1) 的噪声变量：

\[
z_i = \sqrt{K/(K-1)} (w_i - \bar{w})
\]

### 5.3 分数网络仿射反对称性

**引理1**：若 Corr(f(Z), f(-Z)) = -1 对 Z ~ N(0, I_d) 成立，则 f 在 (0, c) 处仿射反对称，即 f(x) + f(-x) = 2c 对所有 x 成立。

**猜想**：对于每个时间步 t，分数网络 ε_θ^{(t)} 在 (0, c_t) 处近似仿射反对称，即 ε_θ^{(t)}(x) + ε_θ^{(t)}(-x) ≈ 2c_t。

DDIM一步更新可写为线性组合形式：

\[
F_t(x) = a_t x + b_t \epsilon_\theta^{(t)}(x)
\]

在猜想下，F_t(-x) ≈ -F_t(x) + 2b_t c_t，因此DDIM一步更新在 (0, b_t c_t) 处仿射反对称。

### 5.4 理论支持

**定理1（分数收敛到高斯分数）**：

\[
\mathbb{E}_{\mu_t}[\|s_t(X_t) + X_t\|^2] = \mathcal{I}(\mu_t \mid \gamma_d) \leq e^{-2t} \mathcal{I}(\mu_0 \mid \gamma_d)
\]

真实分数函数以指数速率收敛到高斯分数 -x。

**推论1（DDIM相关系数偏差界）**：

\[
|\mathrm{Corr}(F_{t,i}(X), F_{t,i}(-X)) + 1| \leq \frac{2|b_t|}{\sqrt{v_{t,i}}} \left( \sqrt{\eta_t} + e^{-t} \sqrt{\mathcal{I}(\mu_0 \mid \gamma_d)} \right)
\]

DDIM一步更新相关系数与-1的偏差受限于神经网络近似误差和指数衰减项。

### 5.5 仿射反对称性得分

为量化仿射反对称程度，引入仿射反对称性得分：

\[
AS(f) = 1 - \frac{\int_{-1}^{1} (0.5 f(-x) + 0.5 f(x) - \bar{f})^2 dx}{\int_{-1}^{1} (f(x) - \bar{f})^2 dx}
\]

该得分衡量一维函数仿射反对称程度，1表示完美仿射反对称，0表示仿射对称。

## 实验与关键发现

### 6.1 核心实验结果

**Table 1** 展示了不同模型和数据集上对偶噪声对（PN）与随机噪声对（RR）的相关系数。PN对在所有测试的模型和数据集上均产生显著更强的负相关。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/005_Table_1.jpg]]
*Table 1: Correlation results across different models and datasets, shown are means (SD). Rows 1–3 are pretrained unconditional diffusion models on different datasets. Rows 4–5 are conditional diffusion models. Rows 6–8 are pretrained consistency models on different datasets. Rows 9–10 are generative models that are not diffusion-based.*

| 模型 | 数据集 | PN标准相关系数 | RR标准相关系数 | PN中心化相关系数 | RR中心化相关系数 |
|------|--------|---------------|---------------|-----------------|-----------------|
| 无条件扩散模型 | CelebA-HQ | -0.34 | 0.26 | -0.78 | 0.01 |
| 无条件扩散模型 | LSUN-Church | -0.62 | 0.02 | -0.41 | -0.01 |
| 无条件扩散模型 | LSUN-Bedroom | -0.74 | 0.05 | -0.62 | -0.01 |
| 条件扩散模型 (DiT) | ImageNet | -0.07 | 0.11 | -0.45 | -0.01 |
| 条件扩散模型 (SD1.5) | COCO | -0.62 | 0.08 | -0.73 | -0.00 |
| 一致性模型 | LSUN-Cat | -0.88 | 0.03 | -0.91 | -0.01 |
| 一致性模型 | LSUN-Bedroom | -0.78 | 0.05 | -0.84 | -0.01 |
| 一致性模型 | ImageNet-64 | -0.71 | 0.03 | -0.75 | -0.01 |
| VAE | MNIST | 0.21 | 0.42 | -0.41 | -0.00 |
| Glow | CIFAR-10 | -0.52 | 0.08 | -0.57 | -0.01 |

**Figure 3** 展示了扩散时间步上 x_t 和 ε_θ^{(t)} 的相关系数演化。对偶对的相关系数从 -1 开始，始终保持强负相关，仅在最后几步略有上升。

**Figure 4** 验证了分数网络的仿射反对称性：CIFAR-10上分数网络第一坐标的输出关于插值标量 c 的曲线呈现整体仿射反对称性，即使在小 t 时存在非线性振荡，两侧也近似镜像。

**Table 10** 显示仿射反对称性得分在CIFAR-10和Church数据集上均值超过0.99，10%分位数高于0.97，表明对偶配对消除了绝大部分方差。

### 6.2 不确定性量化结果

**Table 2** 展示了AMC、K-AMC、RQMC与MC在像素级统计量上的置信区间长度和相对效率：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/008_Table_2.jpg]]
*Table 2: CI lengths and efficiency ( $\mathrm { C I _ { M C } / C I ) ^ { 2 } }$ (in parentheses), using MC as baseline.*

| 数据集 | 统计量 | MC CI长度 | AMC (k=2) CI长度 (效率) | AMC (k=8) CI长度 (效率) |
|--------|--------|-----------|------------------------|------------------------|
| CIFAR-10 | Brightness | 2.00 | 0.35 (32.66) | 0.35 (32.05) |
| CelebA-HQ | Brightness | 1.77 | 0.35 (25.56) | 0.15 (130.69) |
| LSUN-Church | Brightness | 1.82 | 0.33 (30.42) | 0.22 (68.44) |
| Stable Diffusion | Brightness | 1.80 | 0.32 (31.64) | 0.22 (66.94) |
| DiT | Brightness | 1.82 | 0.33 (30.42) | 0.22 (68.44) |

**Table 3** 展示了扩散后验采样（DPS）中AMC与MC的对比：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/009_Table_3.jpg]]
*Table 3: Comparison of AMC vs. MC across tasks in DPS with efficiency ( $\mathrm { C I _ { M C } / C I ) ^ { 2 } }$ in parentheses*

| 任务 | 指标 | MC CI长度 | AMC CI长度 (效率) |
|------|------|-----------|------------------|
| Inpainting | L1 | 0.013 | 0.010 (1.54) |
| Inpainting | PSNR | 0.74 | 0.55 (1.84) |
| Super-resolution | L1 | 0.017 | 0.014 (1.41) |
| Super-resolution | PSNR | 0.87 | 0.70 (1.54) |
| Gaussian Deblur | L1 | 0.016 | 0.014 (1.34) |
| Gaussian Deblur | PSNR | 0.82 | 0.66 (1.56) |

### 6.3 消融实验与扩展

**DDPM随机采样器**：对偶噪声对在DDPM中同样产生强负相关，但需要同时取反每一步的噪声。CIFAR-10上PN标准相关系数为-0.73，中心化后为-0.80。

**无分类器引导（CFG）**：随着CFG尺度增大，PN和RR的相关系数均增大，但PN始终远低于RR。

**局部对偶噪声**：仅取反噪声向量上半部分时，生成图像对应上半部分呈强负相关，下半部分呈强正相关，表明负相关效应在噪声空间中局部作用。

**图像编辑（FlowEdit）**：对偶噪声对提升了CLIP得分（胜率56.59%）并降低了LPIPS（胜率81.58%）。

**多样性提升**：**Table 4** 显示PN对相比RR对在SSIM和LPIPS上均有显著提升，CIFAR-10无条件模型上SSIM改进达88.78%。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/010_Table_4.jpg]]
*Table 4: Average percentage improvement of PN pairs over RR pairs on SSIM and LPIPS.*

### 6.4 公平性说明

所有实验均使用公开预训练模型，未涉及模型训练或数据偏见分析。DDS实验数据来自NYU fastMRI Initiative数据库，该数据库可能包含特定人群的医学图像，但本文仅用于评估不确定性量化方法，未对模型公平性进行专门分析。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_9yFORC1tu3_Antithet/figures/011_Table_5.jpg]]
*Table 5: DDPM standard Pearson correlation coefficients for PN and RR pairs*

## 定位与知识库关联

本文的方法属于**扩散模型不确定性量化**与**蒙特卡洛方差缩减**的交叉领域。与现有工作的关系如下：

- **与初始噪声优化的关系**：现有工作多针对特定任务（如图像编辑、风格迁移）优化初始噪声，而本文首次系统揭示了初始噪声的普遍性质——对偶噪声对产生强负相关。

- **与蒙特卡洛方法的关系**：对偶采样是经典蒙特卡洛方差缩减技术，本文将其创新性地应用于扩散模型，并发现了分数网络的仿射反对称性这一理论基础。

- **与扩散模型理论的关系**：本文的仿射反对称性猜想为理解扩散模型的内部结构提供了新视角，与OU过程、Hermite展开等理论工具建立了联系。

- **与逆问题求解的关系**：本文展示了AMC在DPS和DDS等逆问题求解器中有效降低了不确定性估计的方差，为医学图像重建等高风险应用提供了实用工具。

**局限性**：
- 主要关注确定性采样器，对随机采样器的扩展需要同时取反每一步噪声，增加实现复杂度。
- 仿射反对称性猜想主要基于实验验证，尚未给出严格数学证明。
- 在无分类器引导尺度较大时，负相关程度减弱。
- RQMC方法在不同配置下表现不一致，需要针对具体任务调优。
- 未探讨在视频生成、3D生成等更复杂任务中的适用性。
- 对VAE等非扩散生成模型的普适性有限。

**开放问题**：
- 能否为分数网络的仿射反对称性猜想提供更严格的数学证明？
- 对偶噪声方法在更复杂的生成任务（如视频、3D、音频）中是否同样有效？
- 如何自适应地选择最优的K-对偶或RQMC配置以最大化方差缩减？
- 对偶噪声方法能否与其他初始噪声优化技术结合以取得更好效果？

## 原文 PDF

![[paperPDFs/ICLR_2026/Antithetic_Noise_in_Diffusion_Models.pdf]]
