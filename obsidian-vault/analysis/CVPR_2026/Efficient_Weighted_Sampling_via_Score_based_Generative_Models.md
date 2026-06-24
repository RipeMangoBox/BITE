---
title: Efficient Weighted Sampling via Score-based Generative Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Efficient_Weighted_Sampling_via_Score_based_Generative_Models.pdf
project_link: null
code_link: null
aliases:
- LAUAGSL
- EWSSBGM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用一阶泰勒展开近似引导项并利用有限差分避免二阶导数，同时设计基于时间不确定性分析的自适应调度器动态调制引导强度，在保持采样质量的前提下大幅降低计算成本。
primary_logic: 将引导项近似为权重函数在去噪条件均值处的一阶展开，并通过有限差分替代Hessian-向量乘积，使每步只需两次得分网络评估；进一步通过最小化得分近似均方误差，推导出闭合形式的时变调度函数，在误差大的时刻抑制引导，误差小的时刻增强引导，从而在无额外训练的情况下实现高效、稳定的加权采样。
claims:
- 在2维多模态加权采样任务中，LAGS取得了最低的Wasserstein距离和最快的运行时间（0.33秒），无需二阶导数或重采样。
- 在Stable Diffusion上，LAGS在PickScore和HPS两个指标上均取得最佳性能，且运行时间最短。
- 在Stable Diffusion XL上，LAGS在PickScore和HPS上保持领先，且相比DAS取得4.72倍加速。
- LAGS在SDXL上生成每张图片仅需85秒，比FreeDoM快1.9倍，比DAS快4.7倍，同时避免二阶导数和重采样操作。
---

# Efficient Weighted Sampling via Score-based Generative Models

> [!tip] 核心洞察
> 将引导项近似为权重函数在去噪条件均值处的一阶展开，并通过有限差分替代Hessian-向量乘积，使每步只需两次得分网络评估；进一步通过最小化得分近似均方误差，推导出闭合形式的时变调度函数，在误差大的时刻抑制引导，误差小的时刻增强引导，从而在无额外训练的情况下实现高效、稳定的加权采样。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于得分的生成模型的高效加权采样 |
| 英文题名 | Efficient Weighted Sampling via Score-based Generative Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kim_Efficient_Weighted_Sampling_via_Score-based_Generative_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Lightweight Approximation with uncertainty-adaptive Guidance Scheduling (LAGS) |
| Dataset | 2D multimodal weighted sampling, Stable Diffusion (SD) text-to-image, Stable Diffusion XL (SDXL) text-to-image, SDXL no-reference image quality |

> [!tip] 效果简介
> - 2D multimodal weighted sampling (synthetic) 上，Wasserstein Distance lowest WD vs DPS, FreeDoM, DAS (显著更低)；Runtime 0.33s vs DPS, FreeDoM, DAS (最快)。
> - Stable Diffusion (SD) text-to-image 上，PickScore highest PickScore vs DPS-1p, DPS-5p, FreeDoM, DAS-1p, DAS-5p, DAS-10p (最高)；HPS highest HPS vs 同上 (最高)。
> - Stable Diffusion XL (SDXL) text-to-image 上，PickScore highest PickScore vs DPS-1p, DPS-5p, FreeDoM, DAS-1p, DAS-5p, DAS-10p (最高)。

## 概述

**问题瓶颈**：基于得分的生成模型在加权采样任务中面临关键效率瓶颈——现有引导方法（如DPS、FreeDoM、DAS）在近似目标分布得分函数时，需要计算Hessian矩阵或依赖粒子重采样，导致推理计算开销大、延迟高，难以扩展至大规模扩散模型。

**核心方法**：本文提出**LAGS**（Lightweight Approximation with uncertainty-adaptive Guidance Scheduling），一种免训练的轻量级加权采样框架。其核心洞察在于：将引导项近似为权重函数在去噪条件均值处的一阶泰勒展开，并通过有限差分替代Hessian-向量乘积，使每步仅需两次得分网络评估；进一步，通过最小化得分近似均方误差，推导出闭合形式的时变调度函数，在误差大的时刻抑制引导、误差小的时刻增强引导，从而在无额外训练的情况下实现高效稳定的加权采样。

**方法定位**：LAGS属于**免训练引导近似**范式，与DPS（后验采样，需粒子重采样）、FreeDoM（能量引导，需得分微分与时间旅行重采样）、DAS（扩散自适应采样，依赖粒子重采样维持多样性）形成对比。其关键创新在于将引导项计算从二阶导数/重采样简化为两次得分网络前向传播，并引入不确定性感知的动态调度机制。

**主要结果**：
- 在2D多模态加权采样合成任务上，LAGS以**0.33秒**完成全部采样，取得最低Wasserstein距离，同时无需任何二阶导数或重采样操作。
- 在Stable Diffusion文本到图像任务上，LAGS在PickScore和HPS两项指标上均取得最优，且运行时间最短。
- 在Stable Diffusion XL上，LAGS在PickScore和HPS上保持领先，相比DAS实现**4.72倍加速**，相比FreeDoM实现**1.9倍加速**，每张图片生成仅需约85秒，打破了高分与高计算开销之间的传统权衡。

**局限性**：方法依赖于权重函数和得分函数导数有界、基分布支撑集有界的假设；调度器超参数需手动调节；目前仅在扩散模型上验证，对其他生成范式的适用性尚未探讨。

## 背景与动机

### 加权采样问题定义

给定一个基分布 $p(\mathbf{x})$ 和一个非负权重函数 $w(\mathbf{x})$，加权采样的目标是从如下目标分布中生成样本：

$$
q(\mathbf{x}) = \frac{w(\mathbf{x}) p(\mathbf{x})}{\int w(\mathbf{x}) p(\mathbf{x}) \mathrm{d}\mathbf{x}}
$$

该问题广泛存在于科学计算、统计推断和生成建模中，例如从贝叶斯后验中采样、强化学习中的偏好对齐、以及基于人类反馈的生成任务。当基分布 $p(\mathbf{x})$ 由预训练的扩散模型隐式定义时，如何高效地从加权目标分布 $q(\mathbf{x})$ 中采样成为一个关键挑战。

### 扩散模型与加权采样的结合

扩散模型通过正向随机微分方程（SDE）将数据逐步加噪，再通过逆向SDE从噪声恢复数据。对于任意目标分布 $q$，其正向扩散过程可写为：

$$
\mathrm{d} \mathbf{X}_t^q = f(\mathbf{X}_t^q, t) \mathrm{d} t + \sigma(t) \mathrm{d} \mathbf{W}_t
$$

对应的逆向采样SDE为：

$$
\mathrm{d} \mathbf{X}_t^q = b_1(\mathbf{X}_t^q, t) \mathrm{d} t + \sigma(t) \mathrm{d} \tilde{\mathbf{W}}_t
$$

其中逆向漂移项 $b_1$ 依赖于目标分布 $q_t$ 的得分函数 $\nabla_{\mathbf{x}} \log q_t(\mathbf{x})$。因此，从 $q$ 中采样的核心在于准确估计该得分函数。

### 现有方法的瓶颈

已有的基于引导的加权采样方法面临一个关键瓶颈：**在近似目标分布得分函数时，需要计算得分函数的Hessian矩阵或依赖粒子重采样**。具体而言：

- **DPS** 等基于后验采样的方法通常需要粒子重采样来维持候选多样性，计算开销随粒子数线性增长。
- **FreeDoM** 等免训练的能量引导方法涉及得分函数的微分运算和时间旅行重采样策略，引入了额外的二阶导计算和迭代开销。
- **DAS** 等扩散自适应采样方法通过多粒子重采样来近似目标得分，虽然避免了解析求导，但粒子数增加导致推理延迟显著上升。

这些方法的共同缺陷在于：**推理计算开销大、延迟高，难以扩展至大规模扩散模型**（如 Stable Diffusion XL）。在 SDXL 上，DAS 的运行时间可达 LAGS 的 **4.72 倍**，FreeDoM 也需 **1.9 倍**的时间，这严重制约了加权采样在实际部署中的可行性。

### 本文动机与核心思路

本文的动机在于**打破加权采样中采样质量与计算开销之间的权衡**。核心洞察是：将引导项近似为权重函数在去噪条件均值处的一阶展开，并通过**有限差分**替代 Hessian-向量乘积，使每步只需**两次得分网络评估**，从而彻底消除二阶导数和重采样的开销。进一步地，通过最小化得分近似均方误差，推导出**闭合形式的时变调度函数**，在误差大的时刻抑制引导、误差小的时刻增强引导，在无额外训练的情况下实现高效、稳定的加权采样。

基于上述思路，本文提出 **LAGS（Lightweight Approximation with uncertainty-adaptive Guidance Scheduling）**，一种免训练的轻量级加权采样框架，在 2D 合成任务上以 **0.33 秒**完成全部采样，在 SD 和 SDXL 上以最短运行时间取得最优 PickScore 和 HPS，实现了 **1.2× 至 4.7×** 的加速。

## 核心创新

### 瓶颈与动机

基于得分的生成模型在实现加权采样时，核心挑战在于目标分布得分函数的精确计算。给定基分布 $p(\mathbf{x})$ 与权重函数 $w(\mathbf{x})$，加权采样目标密度为：

$$q(\mathbf{x}) = \frac{w(\mathbf{x}) p(\mathbf{x})}{\int w(\mathbf{x}) p(\mathbf{x}) \mathrm{d}\mathbf{x}}$$

现有基于引导的方法（如 **DPS**、**FreeDoM**、**DAS**）通过将目标得分分解为基得分与引导项之和来近似该过程：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) = \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + g(\mathbf{x},t)$$

然而，精确计算引导项 $g(\mathbf{x},t)$ 需要计算得分函数关于输入的二阶导数（Hessian）或依赖粒子重采样来维持候选多样性。这导致两个关键瓶颈：**推理计算开销大**（每次采样需多次评估得分网络），且**延迟高**，难以扩展至 Stable Diffusion 等大规模扩散模型。

### 创新一：一阶泰勒展开与有限差分近似

LAGS 的第一个核心创新在于对引导项 $g(\mathbf{x},t)$ 的轻量级近似。传统方法需计算 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ 的 Hessian 矩阵，而 LAGS 采用**一阶泰勒展开**策略：

1. **Tweedie 去噪均值展开**：利用 Tweedie 公式获得去噪条件均值 $\bar{\mathbf{x}}_0|_{\mathbf{x},t}$，将权重函数在该均值处进行一阶展开，引导项近似为：

   $$g(\mathbf{x},t) \approx \nabla_{\mathbf{x}} \log w(\bar{\mathbf{x}}_0|_{\mathbf{x},t})$$

   这一步避免了直接计算条件期望中的高维积分。

2. **有限差分替代 Hessian-向量乘积**：关键突破在于用方向导数近似 Hessian 与梯度向量的乘积：

   $$\nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \epsilon H_{\log p_t}(\mathbf{x}) \mathbf{v} \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x} + \epsilon \mathbf{v})$$

   代入后得到一阶近似引导项的闭合形式：

   $$\tilde{g}^{(1)}(\mathbf{x},t) = \frac{\nabla_{\bar{\mathbf{x}}_0|_{\mathbf{x},t}} \log w}{\sqrt{\bar{\alpha}(t)}} + \frac{\nabla_{\mathbf{x}} \log p_t(\mathbf{x} + \epsilon \nabla \log w) - \nabla_{\mathbf{x}} \log p_t(\mathbf{x})}{\epsilon (1-\bar{\alpha}(t))^{-1} \sqrt{\bar{\alpha}(t)}}$$

   **每步仅需两次得分网络评估**，完全消除了二阶导数计算和粒子重采样的开销。

| 方法 | 引导项计算方式 | 每步得分评估次数 | 是否需要重采样 |
|------|---------------|-----------------|---------------|
| DPS | Hessian 或粒子重采样 | 多次 | 是 |
| FreeDoM | 得分函数微分 + 时间旅行重采样 | 多次 | 是 |
| DAS | 粒子重采样维持多样性 | 多次 | 是 |
| **LAGS** | **一阶泰勒展开 + 有限差分** | **2次** | **否** |

### 创新二：不确定性自适应调度器

单纯的近似引导项在不同时间步的精度存在差异：在扩散初期（高噪声阶段），去噪条件均值的估计不可靠，近似误差较大；在扩散末期（低噪声阶段），近似精度显著提高。LAGS 的第二个核心创新是设计了一个**时变调度函数** $\tau(t)$，动态调制引导项的贡献：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \tau(t) \tilde{g}^{(1)}(\mathbf{x},t)$$

该调度器通过最小化得分近似均方误差上界推导得出：

$$r(t; \tau) = \mathbb{E}\left[\|\nabla_{X_t^q} \log q_t(X_t^q) - \nabla_{X_t^q} \log p_t(X_t^q) - \tau(t) \tilde{g}^{(1)}(X_t^q, t)\|^2\right]$$

通过对误差上界的确定性分析，得到闭合形式的最优调度：

$$\tau^*(t) = \left(1 + \sum_{(i,j)\in\mathcal{T}} \frac{c_{(i,j)}}{c_1} \frac{(1-\bar{\alpha}(t))^i}{\bar{\alpha}(t)^j}\right)^{-1}$$

实用中简化为单参数形式：

$$\tau^*(t) \approx \left(1 + c \frac{(1-\bar{\alpha}(t))^2}{\bar{\alpha}(t)^2}\right)^{-1}$$

**调度行为**：当 $t$ 接近 $T$（高噪声），$\bar{\alpha}(t) \to 0$，$\tau^*(t) \to 0$，引导项被抑制；当 $t \to 0$（低噪声），$\bar{\alpha}(t) \to 1$，$\tau^*(t) \to 1$，引导项完全生效。这实现了**在误差大的时刻自动抑制引导，在误差小的时刻增强引导**的自适应行为。

### 创新三：免训练部署

结合上述两个创新，LAGS 的最终采样得分近似为：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \frac{\bar{\alpha}(t)^2}{\bar{\alpha}(t)^2 + c (1-\bar{\alpha}(t))^2} \tilde{g}^{(1)}(\mathbf{x},t)$$

该方法**无需任何额外训练**，仅需预训练得分网络 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ 和权重函数 $w(\mathbf{x})$，即可实现加权采样。超参数仅有两个：有限差分步长 $\epsilon$ 和调度强度 $c$。

### 效率增益的因果机制

LAGS 的效率优势源于三个层面的设计协同：

1. **计算层面**：有限差分近似将每步计算从 Hessian 的 $\mathcal{O}(d^2)$ 降至两次前向传播的 $\mathcal{O}(d)$；
2. **调度层面**：不确定性感知调度在高噪声阶段自动降低引导贡献，避免了在近似不可靠时浪费计算；
3. **架构层面**：免训练设计消除了对额外网络或微调的需求，可直接插入现有扩散模型。

在 Stable Diffusion XL 上的实测表明，LAGS 生成单张图片仅需约 85 秒，比 FreeDoM 快 **1.9 倍**，比 DAS 快 **4.7 倍**，同时避免了二阶导数和重采样操作。

## 整体框架

LAGS 的整体推理流程围绕一个核心分解展开：将目标加权分布 $q(\mathbf{x})$ 在扩散时间 $t$ 下的得分函数分解为预训练基模型的得分与一个引导项之和：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) = \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + g(\mathbf{x},t)$$

其中 $p_t(\mathbf{x})$ 是基分布（如 Stable Diffusion 的预训练得分网络）的噪声扰动得分，$g(\mathbf{x},t)$ 是捕捉权重函数 $w(\mathbf{x})$ 影响的引导项。LAGS 的核心设计在于用轻量级近似 $\tilde{g}(\mathbf{x},t)$ 替代精确的 $g(\mathbf{x},t)$，从而在无需额外训练、不计算二阶导数、不进行粒子重采样的前提下，实现高效的加权采样。

整个 pipeline 由四个关键模块串接而成：

1.  **得分分解与引导项定义**：将目标得分显式分解为基得分与引导项，明确加权采样的优化目标。
2.  **一阶泰勒近似与 Tweedie 去噪**：利用 Tweedie 公式从当前噪声状态 $\mathbf{x}$ 估计对应的去噪条件均值 $\bar{\mathbf{x}}_0|_{\mathbf{x},t}$，并在该均值处对权重函数的对数梯度进行一阶泰勒展开，将引导项近似为 $\nabla_{\mathbf{x}} \log w(\bar{\mathbf{x}}_0|_{\mathbf{x},t})$，从而避免计算对条件期望的复杂积分。
3.  **有限差分 Hessian-向量乘积近似**：在展开过程中出现的 Hessian-向量乘积项 $H_{\log p_t}(\mathbf{x}) \mathbf{v}$，通过方向导数近似 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x} + \epsilon \mathbf{v})$ 来替代，将每步所需的得分网络评估次数压缩至仅两次，彻底消除了对二阶导数的依赖。
4.  **不确定性自适应调度器**：引入时变调制函数 $\tau(t) \in [0,1]$，以最小化得分近似均方误差为目标，推导出闭合形式的调度函数 $\tau^*(t)$。该调度器在扩散早期（不确定性高、近似误差大）自动抑制引导强度，在末期（误差小）增强引导，从而在保持采样质量的同时稳定逆向扩散过程。

最终，逆向扩散过程使用的得分函数近似为：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \frac{\bar{\alpha}(t)^2}{\bar{\alpha}(t)^2 + c (1-\bar{\alpha}(t))^2} \tilde{g}^{(1)}(\mathbf{x},t)$$

其中 $c$ 是控制引导强度的超参数，$\tilde{g}^{(1)}(\mathbf{x},t)$ 是前述一阶近似引导项（式13）。整个推理过程仅需在预训练得分网络的基础上额外调用两次得分函数评估，无需任何微调或重采样操作，即可从基分布 $p(\mathbf{x})$ 中生成服从目标加权分布 $q(\mathbf{x}) \propto w(\mathbf{x}) p(\mathbf{x})$ 的样本。

## 核心模块与公式推导

LAGS 的核心思路是将目标分布得分函数分解为预训练基得分与引导项之和，随后通过一阶泰勒展开和有限差分构造轻量级引导近似，并引入不确定性自适应调度器动态调制引导强度。整个方法无需额外训练，仅依赖预训练得分网络和给定的权重函数。

### 得分分解与引导项定义

加权采样的目标分布 $q(\mathbf{x}) \propto w(\mathbf{x}) p(\mathbf{x})$，其噪声扰动版本 $q_t(\mathbf{x})$ 的得分函数可分解为：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) = \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + g(\mathbf{x},t)$$

其中 $\nabla_{\mathbf{x}} \log p_t(\mathbf{x})$ 是预训练基分布的得分（由扩散模型提供），$g(\mathbf{x},t)$ 是引导项，编码了权重函数 $w$ 对采样方向的修正。直接计算 $g(\mathbf{x},t)$ 涉及条件期望和得分函数的二阶导数，计算代价高昂。

### 一阶泰勒近似与 Tweedie 去噪

为规避条件期望的复杂计算，LAGS 利用 Tweedie 公式从噪声样本 $\mathbf{x}$ 估计对应的去噪条件均值 $\bar{\mathbf{x}}_0|_{\mathbf{x},t}$，然后将权重函数在该均值处进行一阶泰勒展开，得到引导项的近似：

$$g(\mathbf{x},t) \approx \nabla_{\mathbf{x}} \log w(\bar{\mathbf{x}}_0|_{\mathbf{x},t})$$

该近似将引导项转化为权重函数在确定性估计点处的梯度，避免了在高维空间中求条件期望。

### 有限差分 Hessian-向量乘积近似

上述近似在链式求导展开后，仍包含得分函数的 Hessian 与权重梯度向量的乘积项 $H_{\log p_t}(\mathbf{x}) \mathbf{v}$。LAGS 通过方向导数的有限差分替代该 Hessian-向量乘积：

$$\nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \epsilon H_{\log p_t}(\mathbf{x}) \mathbf{v} \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x} + \epsilon \mathbf{v})$$

其中 $\epsilon > 0$ 是充分小的步长。代入后得到一阶引导近似 $\tilde{g}^{(1)}(\mathbf{x},t)$，其计算仅需两次得分网络评估（分别在 $\mathbf{x}$ 和 $\mathbf{x} + \epsilon \nabla \log w$ 处），完全消除了对二阶导数的显式依赖。

### 不确定性自适应调度器

一阶近似在不同时间步的精度存在差异：噪声较大时（$t$ 接近 $T$），去噪条件均值估计不可靠，引导近似误差较大；噪声较小时（$t$ 接近 $0$），近似精度较高。LAGS 引入时变调度函数 $\tau(t) \in [0,1]$ 来调制引导项的贡献：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \tau(t) \tilde{g}^{(1)}(\mathbf{x},t)$$

通过最小化得分近似均方误差的上界，推导出闭合形式的最优调度：

$$\tau^*(t) = \left(1 + \sum_{(i,j)\in\mathcal{T}} \frac{c_{(i,j)}}{c_1} \frac{(1-\bar{\alpha}(t))^i}{\bar{\alpha}(t)^j}\right)^{-1}$$

其中 $\bar{\alpha}(t)$ 是扩散过程的累积信噪比参数，$\mathcal{T}$ 是与导数有界性假设相关的指标集。该调度函数在 $\bar{\alpha}(t)$ 较小（高噪声）时自动抑制引导项，在 $\bar{\alpha}(t)$ 较大（低噪声）时增强引导项。

### 实用单参数调度与最终采样公式

为便于部署，LAGS 将调度器简化为单参数形式：

$$\tau^*(t) \approx \left(1 + c \frac{(1-\bar{\alpha}(t))^2}{\bar{\alpha}(t)^2}\right)^{-1}$$

其中 $c > 0$ 是控制引导强度的超参数：$c$ 越大引导越弱，在时间步初期 $\tau(t) \approx 0$，末期 $\tau(t) \approx 1$。最终加权采样得分近似为：

$$\nabla_{\mathbf{x}} \log q_t(\mathbf{x}) \approx \nabla_{\mathbf{x}} \log p_t(\mathbf{x}) + \frac{\bar{\alpha}(t)^2}{\bar{\alpha}(t)^2 + c (1-\bar{\alpha}(t))^2} \tilde{g}^{(1)}(\mathbf{x},t)$$

将该近似得分代入逆向扩散过程的 SDE 或 ODE 求解器，即可生成服从目标加权分布的样本。整个流程无需对基模型进行微调或重训练，仅需给定预训练得分网络和权重函数 $w(\mathbf{x})$。

## 实验与分析

### 核心实验设置

为验证 LAGS 的有效性与效率，作者在三个递进式实验场景中进行了系统评估：(1) 2D 合成多模态加权采样任务，用于在可控条件下精确度量采样质量与计算开销；(2) Stable Diffusion (SD) 文本到图像生成任务，评估中等规模扩散模型上的引导质量与推理速度；(3) Stable Diffusion XL (SDXL) 大规模文本到图像生成，检验方法在高维生成场景下的可扩展性。

对比基线涵盖三类代表性方法：基于后验采样的 **DPS**（需粒子重采样）、免训练能量引导方法 **FreeDoM**（涉及得分函数微分与时间旅行重采样），以及扩散自适应采样方法 **DAS**（通过多粒子重采样维持候选多样性）。其中 DPS 和 DAS 分别以 1-particle、5-particle 和 10-particle 变体参与对比，以揭示粒子数量对质量-效率权衡的影响。评估指标包括 PickScore、ImageReward、CLIP Score、HPS 等文本-图像对齐指标，以及 BRISQUE 和 MANIQA 等无参考图像质量指标；所有引导方法的运行时间均以 LAGS 为基准进行归一化。

### 2D 合成任务：精度与速度的双重验证

在 2D 多模态加权采样合成任务中，基分布为多模态高斯混合，目标分布通过非均匀权重函数对基分布进行重新加权得到。该任务的核心挑战在于：目标分布与基分布的模式结构存在显著偏移，要求采样方法能够准确捕捉权重函数引入的密度调制。

如 Figure 1 所示，LAGS 生成的估计样本密度在视觉上与目标分布高度一致，而 DPS 和 FreeDoM 在部分模式区域出现明显的密度偏差。定量结果表明，LAGS 取得了所有方法中最低的 Wasserstein Distance，同时仅需 **0.33 秒**即可完成全部样本生成——无需计算任何二阶导数或执行重采样操作。相比之下，DAS 虽在密度估计精度上接近 LAGS，但其运行时间显著更高；FreeDoM 和 DPS 则在精度和速度两方面均处于劣势。这一结果直接验证了核心主张：一阶泰勒展开结合有限差分近似能够在保持采样精度的前提下，大幅降低计算成本。

![[assets/figures/papers/paper_list_l866_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Efficient_Weighted/figures/001_Figure_1.jpg]]
*Figure 1: Left to Right: Base distribution, target distribution, and estimated sample densities. Wasserstein Distance and runtime (in seconds) are reported for DPS, FreeDoM, DAS, and LAGS (ours). Our method achieves the lowest Wasserstein Distance (WD) and fastest runtime*

### Stable Diffusion 实验结果

在 Stable Diffusion 文本到图像生成任务中，采用来自现有基准的标准提示集进行评估。Figure 2 展示了各方法在四个文本-图像对齐指标上的对比结果，运行时间以 LAGS 为 1× 基准进行归一化。

![[assets/figures/papers/paper_list_l866_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Efficient_Weighted/figures/003_Figure_2.jpg]]
*Figure 2: Results on SD: Comparative performance across PickScore, ImageReward, CLIP Score, and HPS (left to right), with runtime normalized to LAGS. Our method achieves the best performance in PickScore and HPS with the lowest runtime among the guidance methods. We adopt the benchmark set of prompts from [19]*

![[assets/figures/papers/paper_list_l866_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Efficient_Weighted/figures/002_Figure_3.jpg]]
*Figure 3: Results on SDXL: Evaluation on the same metrics as in Fig. 2. LAGS consistently achieves the best performance in PickScore (target metric) and HPS with the lowest runtime among the guidance methods, breaking the typical trade-off between high score and computation complexity*

LAGS 在 **PickScore** 和 **HPS** 两个指标上均取得最佳性能，同时在所有引导方法中保持最低的运行时间。值得注意的是，DAS-10p 和 DAS-5p 通过增加粒子数量在部分指标上接近或达到较高分数，但其运行时间分别约为 LAGS 的 5 倍和 3 倍以上，呈现出典型的“高分高开销”权衡。FreeDoM 在 ImageReward 指标上表现突出，但运行时间同样显著高于 LAGS。CLIP Score 方面，各方法差异相对较小，表明该指标对引导策略的敏感度有限。

这一结果揭示了 LAGS 的关键优势：通过不确定性自适应调度器动态调制引导强度，在扩散过程早期（近似误差较大时）自动抑制引导贡献，在后期（误差较小时）充分释放引导信号，从而在不牺牲采样质量的前提下避免了冗余计算。

### Stable Diffusion XL 实验结果

在更大规模的 SDXL 模型上，计算效率的差异被进一步放大。Figure 3 显示，LAGS 在 PickScore 和 HPS 上持续保持领先，且运行时间在所有引导方法中最短。具体而言，**LAGS 在 SDXL 上生成每张图片约需 85 秒**，相比 FreeDoM 实现 **1.9 倍加速**，相比 DAS 实现 **4.7 倍加速**。这一结果打破了“高分必须高开销”的常规权衡——LAGS 以最低的计算成本取得了最优的文本-图像对齐性能。

Table 1 进一步汇总了各方法的无参考图像质量指标。在 BRISQUE（越低越好）上，DAS 取得 19.55 的最佳值，LAGS 为 26.40；在 MANIQA（越高越好）上，DAS-1P 以 0.728 领先，LAGS 为 0.627。这表明 DAS 的多粒子重采样策略在图像感知质量方面具有一定优势，但代价是约 4.7 倍的推理时间。LAGS 在图像质量指标上的轻微劣势，可归因于其一阶近似在捕捉权重函数高阶变化时的固有精度损失——这是轻量化设计所接受的合理折衷。

![[assets/figures/papers/paper_list_l866_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Efficient_Weighted/figures/005_Table_1.jpg]]
*Table 1: Runtime and no-reference image quality measures (BRISQUE, MANIQA). Values are mean standard deviation. Bold indicates best among guidance methods*

### 定性分析

Figure 4 展示了 LAGS 在多个文本提示下生成的最高和最低 PickScore 样本。在“坐在窗边纸箱里的猫”“桌上三个苹果”“梵高风格红色跑车”等多样化提示下，LAGS 生成的最高分样本展现出良好的文本-图像一致性和视觉质量，定性验证了所提轻量级引导项在高维域的有效性。值得关注的是，对于所有展示的提示，最高 PickScore 样本均由 LAGS 方法生成，进一步佐证了其引导策略在提升文本对齐方面的实际效果。

![[assets/figures/papers/paper_list_l866_https_openaccess_thecvf_com_content_CVPR2026_html_Kim_Efficient_Weighted/figures/004_Figure_4.jpg]]
*Figure 4: Sampling results with the proposed lightweight guidance g˜(x, t) on a high-dimensional domain. Top row: Samples with the lowest PickScore; Bottom row: those with the highest PickScore, selected from all generations. Prompts (left to right): “A cat sitting inside a cardboard box next to a window”, “Three apples on a table”, “A majestic, photorealistic alien spaceship drifting before a vast galaxy”, “A photo-realistic image of flying lion with blue butterfly wings”, “A red sports car in the style of Vincent van Gogh”. Notably, for all prompts, the highest PickScore samples are achieved by our method. Additional qualitative results are provided in Appendix C.2.2*

### 消融与超参数分析

LAGS 的核心超参数为调度器中的标量 **c**，用于控制引导强度的时间调制曲线。根据 Remark 3 和 Remark 4 的理论分析，c 越大则引导越弱：在扩散过程初期（时间步 t 较大时），调度函数 τ*(t) 趋近于零，几乎完全抑制引导项；随着 t 减小，τ*(t) 单调递增并逐渐趋近于 1。这一行为与不确定性分析的理论预测一致——早期阶段的得分近似误差较大，应降低引导贡献以避免误差累积。

实际部署中，c 的取值需根据具体任务手动调整：过小的 c 会过度信任近似引导项，可能在早期引入噪声；过大的 c 则会导致引导不足，使采样结果退化为基分布。目前该方法尚缺乏自动化或自适应的 c 选择机制，这构成了实际应用中的一个工程瓶颈。

### 失败模式与局限性

尽管 LAGS 在效率与主流指标上表现优异，实验也揭示了若干值得关注的局限：

1. **图像感知质量的折衷**：在 BRISQUE 和 MANIQA 等无参考质量指标上，LAGS 略逊于 DAS 的多粒子变体。这暗示一阶近似在捕捉权重函数的细粒度变化时存在精度上限，当应用场景对图像质量有极高要求时，可能需要结合轻量级后处理或混合策略。

2. **超参数敏感性**：调度器参数 c 对最终性能有显著影响，且最优值依赖于具体任务和数据分布。当前缺乏自动调参机制，增加了实际部署的调优成本。

3. **理论假设的边界**：方法建立在权重函数和得分函数的导数有界、基分布支撑集有界的假设之上。当权重函数非光滑（如指示函数）或数据分布无界时，近似精度可能显著下降。实验中的权重函数（基于 PickScore 等可微奖励模型）满足光滑性条件，但更一般的应用场景需谨慎评估。

4. **范式局限性**：所有实验均在扩散模型框架（SD 和 SDXL）下进行，方法对其他生成范式（如 GAN、归一化流）的适用性尚未验证。此外，尽管每步仅需两次得分网络评估，但对于极低延迟的实时应用场景，额外的网络前传仍可能构成瓶颈。

## 方法谱系与知识库定位

### 问题定位：加权采样与引导方法的效率瓶颈

加权采样（weighted sampling）是生成建模中的基础问题，目标是从形如 $q(\mathbf{x}) \propto w(\mathbf{x}) p(\mathbf{x})$ 的目标分布中采样，其中 $p(\mathbf{x})$ 为预训练的基分布（如扩散模型的先验），$w(\mathbf{x})$ 为任务相关的权重函数。该范式广泛存在于条件生成、逆问题求解、偏好对齐等场景。

在扩散模型框架下，实现加权采样的核心挑战在于获取目标分布随时间演化的得分函数 $\nabla_{\mathbf{x}} \log q_t(\mathbf{x})$。已有方法大致分为两类：

- **基于后验采样的方法**，如 **DPS**（Diffusion Posterior Sampling），通过粒子重采样（particle resampling）来近似目标分布得分，但重采样操作引入显著的计算开销和内存负担，且在高维空间中粒子多样性维持困难。
- **免训练的能量引导方法**，如 **FreeDoM**，通过对得分函数进行微分来估计引导项，但需要计算得分函数的 Hessian 或 Jacobian，导致每步推理的计算成本高昂。**DAS**（Diffusion Adaptive Sampling）则结合粒子重采样来维持候选多样性，但同样面临二阶导数计算或重采样的效率问题。

**核心瓶颈**：上述方法在近似目标分布得分时，或需计算 Hessian，或依赖粒子重采样，导致推理计算开销大、延迟高，难以扩展至大规模扩散模型（如 Stable Diffusion XL）。

### LAGS 的方法定位

本文提出的 **LAGS**（Lightweight Approximation with uncertainty-adaptive Guidance Scheduling）在方法谱系中属于**免训练的引导近似方法**，但其核心创新在于通过两个关键设计打破了精度与效率的传统权衡：

1. **一阶泰勒展开 + 有限差分 Hessian 近似**：将引导项 $g(\mathbf{x}, t)$ 近似为权重函数在去噪条件均值 $\bar{\mathbf{x}}_0|_{\mathbf{x},t}$ 处的梯度，并通过有限差分替代 Hessian-向量乘积，使每步仅需两次得分网络评估，完全避免了二阶导数的显式计算。这与 FreeDoM 等需要 Hessian 的方法形成鲜明对比。

2. **不确定性自适应调度器 $\tau(t)$**：基于时间步的近似误差上界分析，推导出闭合形式的调度函数，在误差大的时刻（如扩散早期）抑制引导，误差小的时刻增强引导，从而在无额外训练的情况下稳定采样过程。相比之下，DPS 和 DAS 的引导强度通常是固定的或仅依赖启发式调整。

### 与基线方法的关系与适用边界

| 方法 | 引导机制 | 是否需要二阶导数 | 是否需要重采样 | 推理效率 | 适用场景 |
|------|----------|------------------|----------------|----------|----------|
| DPS | 后验采样 + 粒子重采样 | 否 | 是 | 低 | 小规模逆问题 |
| FreeDoM | 能量引导 + 得分微分 | 是（Hessian） | 部分（时间旅行重采样） | 中 | 免训练条件生成 |
| DAS | 自适应采样 + 粒子重采样 | 否 | 是 | 低 | 需要高多样性的任务 |
| **LAGS** | 一阶引导近似 + 不确定性调度 | 否（有限差分） | 否 | 高 | 大规模加权采样/偏好对齐 |

**适用边界**：
- LAGS 建立在权重函数和得分函数的导数有界以及基分布支撑集有界的假设之上。当权重函数非光滑（如指示函数）或数据分布无界时，一阶近似的精度可能下降，需要手动验证。
- 调度器超参数 $c$ 需要根据具体任务手动调整，目前缺乏自动化或自适应选择机制。
- 仅在扩散模型（Stable Diffusion 和 SDXL）上验证了加权采样效率，对其他生成范式（如 GAN、归一化流）的适用性尚未探讨。

### 局限与开放问题

**已知局限**：
1. 尽管显著降低了计算开销，但每步仍需额外的得分网络评估（两次前向传播），对于极低延迟场景可能仍存在瓶颈。
2. 无参考图像质量指标（BRISQUE、MANIQA）上，LAGS 略逊于 DAS 的某些变体（Table 1），表明一阶近似在感知质量维度上可能存在精度折损。
3. 方法对权重函数的平滑性有一定要求，在权重函数包含离散或非可微成分时，近似误差可能增大。

**开放问题**：
1. **高阶扩展**：能否将一阶近似推广到更高阶（如二阶）以进一步提升引导精度，同时保持计算可行性？
2. **自适应调度器学习**：如何自适应地学习调度器参数 $c$ 以及可能引入的额外参数，使其无需手动调参即可在不同任务上达到最优？
3. **跨范式泛化**：在更复杂的条件生成任务（如线性/非线性逆问题求解、蛋白质设计）中，该方法是否仍能保持效率与质量优势？是否可以将这种免训练的引导近似思想应用于扩散模型以外的其他生成模型？
4. **理论紧致性**：当前调度器的推导基于误差上界的最小化，该上界的紧致性及其对实际采样质量的影响仍需更深入的理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Efficient_Weighted_Sampling_via_Score_based_Generative_Models.pdf]]
