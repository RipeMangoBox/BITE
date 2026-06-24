---
title: "COIN: Control-Inpainting Diffusion Prior for Human and Camera Motion Estimation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation.pdf
aliases:
- COIN
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "COIN-SDS 利用多步 DDIM 去噪、动态控制信号和软修复策略，生成高质量且一致的伪真值运动；引入的人-场景深度关系损失为相机尺度提供独立于人体运动的约束。"
primary_logic: "通过控制信号引导扩散模型去噪过程，并结合软修复来保持观测一致性，可以显著提高运动质量；场景深度关系为相机尺度提供了独立于人体运动的约束，解耦了二者之间的影响。"
claims:
- "COIN introduces a novel control-inpainting score distillation sampling method to ensure well-aligned, consistent, and high-quality motion from the diffusion prior within a joint o..."
- "We introduce a new human-scene relation loss to alleviate the scale ambiguity by enforcing consistency among the humans, camera, and scene."
- "The pre-trained diffusion model is sensitive to the input; minor fluctuations in the input latent would substantially change the denoised motion, leading to inconsistency."
- "Dynamic controlled sampling iteratively refines the observed motions and updates the control signals to ensure effective distillation."
---

# COIN: Control-Inpainting Diffusion Prior for Human and Camera Motion Estimation

> [!tip] 核心洞察
> 通过控制信号引导扩散模型去噪过程，并结合软修复来保持观测一致性，可以显著提高运动质量；场景深度关系为相机尺度提供了独立于人体运动的约束，解耦了二者之间的影响。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | COIN：面向人体与相机运动估计的控制-修复扩散先验 |
| 英文题名 | COIN: Control-Inpainting Diffusion Prior for Human and Camera Motion Estimation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2408.16426); [Project](https://nvlabs.github.io/COIN/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | COIN |
| Dataset | RICH, HCM, EMDB |

> [!tip] 效果简介
> - RICH 上，W-MPJPE 为 254.5 (COIN)，对比 380.0 (PACE)，变化 -125.5 mm (-33%)。
> - HCM 上，W-MPJPE 为 COIN，对比 PACE，变化 44% improvement。
> - EMDB 上，W-MPJPE_100 为 407.3 (COIN)，对比 WHAM，变化 7% improvement。

## 概述

从动态相机视频中同时恢复全局人体运动和相机轨迹，是三维视觉领域的一个核心难题。现有方法面临两个关键瓶颈：其一，基于单步得分蒸馏采样（SDS）的扩散先验缺乏有效控制，生成的伪真值运动与视频观测不一致，且过于平滑；其二，相机尺度优化完全依赖不准确的全局人体运动，导致尺度估计容易失败。

COIN 通过两项核心创新突破上述瓶颈。在扩散先验层面，COIN 提出**控制-修复得分蒸馏采样（COIN-SDS）**，利用多步 DDIM 去噪、动态控制信号和软修复策略，生成高质量且与观测一致的伪真值运动。在尺度优化层面，COIN 引入**人-场景深度关系损失**，利用场景点云与人体关节之间的遮挡深度约束，为相机尺度提供独立于人体运动的监督信号，有效解耦二者之间的影响。

在 RICH、EMDB 和 HCM 三个数据集上，COIN 显著超越现有方法。相较于 SOTA 方法 **PACE**（Kocabas et al., 3DV 2024），COIN 在 HCM 上的世界关节位置误差（W-MPJPE）降低 44%，在 RICH 上降低 33%。与同期工作 **WHAM**（Shin et al., CVPR 2024）相比，COIN 在 RICH 上提升 49%，在 EMDB 上提升 7%。消融实验进一步验证：控制采样使 W-MPJPE 降低 570.5 mm（69.3%），软修复使 PA-MPJPE 降低 4.7 mm，人-场景关系损失使 W-MPJPE 从 273.0 mm 降至 254.5 mm。

## 背景与动机

从动态相机视频中同时恢复全局人体运动和相机运动是计算机视觉中的一个核心挑战。当相机本身在运动时，视频中的二维观测同时包含了人体运动和相机运动的耦合效应，使得二者的解耦变得极为困难。这一问题在滑板、跑酷等大幅度位移场景中尤为突出——即便局部身体姿态相对稳定，个体的全局位置也可能发生剧烈变化。

现有方法在处理此类分布外运动时暴露出明显的脆弱性。当前最优的全局人体与相机运动估计方法 **PACE**（Kocabas et al., 3DV 2024）和同期工作 **WHAM**（Shin et al., CVPR 2024）在滑板等场景中会灾难性地失败，无法正确恢复人体轨迹或行走方向（见图1）。

从方法论角度审视，现有工作的瓶颈集中在两个层面：

**运动先验的生成质量不足。** 以 PACE 为代表的现有方法使用单步 Score Distillation Sampling（SDS）从扩散模型中蒸馏运动先验，但缺乏对去噪过程的控制与约束。单步 SDS 生成的伪真值运动对输入噪声高度敏感——潜变量中的微小波动即会导致去噪结果发生显著变化，造成运动估计不一致。此外，缺乏修复机制使得模型无法有效利用视频中的高置信度观测区域，导致生成的伪真值与实际观测脱节。

**相机尺度的优化缺乏独立约束。** 在动态相机场景下，相机尺度的估计完全依赖于全局人体运动的重投影误差。当人体运动估计本身不准确时，尺度优化极易陷入失败——二者形成了一种脆弱的耦合关系，缺乏解耦的约束信号。

针对上述缺口，**COIN** 提出了两个核心改进方向：其一，通过控制-修复评分蒸馏采样（COIN-SDS）生成与视频观测一致的高质量运动先验；其二，引入人-场景深度关系损失，利用场景点云提供的独立几何约束来正则化相机尺度，从而解耦尺度优化与人体运动估计之间的相互干扰。

## 核心创新

COIN 的核心创新在于对扩散先验蒸馏机制的重新设计，以及引入场景几何约束来解耦相机尺度估计。与现有方法相比，COIN 在四个关键维度上做出了实质性改进，直接回应了单步 SDS 蒸馏导致的运动伪真值不一致、过度平滑以及相机尺度优化失败等问题。

### 1. 扩散先验蒸馏方法：从单步 SDS 到 COIN-SDS

现有方法（如 Vanilla SDS）采用单步去噪来生成伪真值运动，其核心缺陷在于预训练扩散模型对输入高度敏感——潜变量中的微小波动会导致去噪运动发生显著变化，从而破坏优化一致性。COIN 提出的 **COIN-SDS** 通过三项协同设计解决了这一问题：

- **多步 DDIM 去噪**：用多步确定性 DDIM 采样替代单步估计，生成更高质量、更稳定的伪真值运动 $\tilde{\mathbf{H}}_0$。具体而言，从时间步 $t$ 开始执行多步 DDIM 去噪，每一步沿公式 $\tilde{\mathbf{H}}_{t-\Delta t} = \sqrt{\bar{\alpha}_{t-\Delta t}} \cdot \hat{\mathbf{H}}_0^t + \sqrt{1-\bar{\alpha}_{t-\Delta t}} \cdot \epsilon_\phi^t$ 迭代，最终得到 $\tilde{\mathbf{H}}_0$ 作为 SDS 目标。实验表明，10 步去噪已足以产生高质量伪真值。

- **动态控制信号**：基线方法使用固定的初始运动估计（来自 HybrIK）作为控制信号，无法随优化进程自适应调整。COIN 在每轮迭代中，将上一轮优化后的人体运动作为新的控制信号输入受控去噪器 $\mathcal{D}_{\phi,\phi_c}$，实现控制信号与优化状态的同步更新，确保蒸馏过程持续有效。

- **软修复策略**：区别于无修复或硬修复方案，COIN 引入基于置信度分数 $\mathbf{S}$ 和去噪时间步 $t$ 的连续掩膜 $\tilde{\mathbf{M}} = w(t) * \mathbf{S} \odot \mathbf{M}$。已知区域（高置信度观测）直接使用观测值 $\mathbf{H}$，未知区域由扩散模型生成，两者通过掩膜加权融合，在保持观测一致性的同时最大化先验的生成能力。

这三项设计的组合效果在消融实验中得到了直接验证：受控采样使 RICH 数据集上的 W-MPJPE 降低 570.5 mm（69.3%），软修复进一步降低 PA-MPJPE 4.7 mm。

### 2. 去噪控制信号：从固定到动态

基线方法依赖 HybrIK 提供的初始相机空间姿态作为固定的控制信号，在优化过程中保持不变。当初始估计存在较大误差时，固定控制信号会将误差持续传播至扩散先验的采样过程，导致伪真值运动偏离真实观测。COIN 的解决方案是“用优化后的运动指导下一步采样”——将上一轮迭代优化得到的全局人体运动作为新的控制信号，形成闭环反馈。这种动态控制机制使扩散先验能够随着优化进程逐步逼近真实运动，而非被初始误差所束缚。

### 3. 修复策略：从硬约束到软融合

传统修复方法对已知区域施加硬约束（直接覆盖），忽略了观测本身的不确定性。COIN 的软修复策略引入两个关键改进：首先，利用 2D 关键点置信度分数 $\mathbf{S}$ 区分不同观测的可靠性；其次，通过时间步相关的权重 $w(t)$ 控制修复强度——在去噪早期（高噪声阶段），模型更依赖扩散先验生成；在去噪后期，观测约束逐渐增强。这种连续掩膜机制避免了硬修复可能引入的伪影，同时在优化过程中自然平衡了先验知识与观测证据。

### 4. 相机尺度正则化：从依赖人体运动到场景深度约束

现有方法（如 PACE）的相机尺度优化完全依赖全局人体运动的重投影误差，当人体运动估计不准确时，尺度优化会随之失败。COIN 提出 **人-场景关系损失** $\mathcal{L}_{\mathrm{HSR}}$，利用场景点云与人体关节之间的深度顺序关系提供独立于人体运动的尺度约束：

$$\mathcal{L}_{\mathrm{HSR}} = -\frac{1}{|\mathcal{P}|} \sum_{i=1}^{T} \sum_{p \in \mathcal{P}^*} \min(0, \mathcal{T}^{(i)}(p)_z - j^{(i)}(p)_z) \cdot \mathbb{1}(\mathcal{T}^{(i)}(p) \text{ is invisible})$$

该损失惩罚深度顺序错误：当一个场景点被人体遮挡（不可见）时，其深度应大于最近的人体关节深度。这一约束直接作用于相机尺度参数，使其不再完全耦合于人体运动估计质量。消融实验证实，移除 $\mathcal{L}_{\mathrm{HSR}}$ 会使 RICH 数据集上的 W-MPJPE 从 254.5 mm 上升至 273.0 mm，验证了场景几何约束在解耦尺度优化中的关键作用。

### 创新总结

COIN 的四项核心创新形成了一个互补体系：COIN-SDS 提供高质量运动先验，动态控制确保先验与优化协同进化，软修复在保持观测一致性的同时最大化先验效用，人-场景关系损失则为相机尺度提供独立约束。这一体系使 COIN 在 RICH 和 HCM 数据集上分别以 33% 和 44% 的幅度超越 SOTA 方法 PACE（Kocabas et al., 3DV 2024），并在 EMDB 数据集上以 7% 的优势超越同期工作 WHAM（Shin et al., CVPR 2024）。

## 整体框架

COIN 将动态相机下的人体与相机运动估计建模为一个**全局联合优化问题**，其核心思想是通过控制-修复扩散先验（COIN-SDS）提供高质量伪真值运动，并利用人-场景深度关系损失解耦相机尺度与人体运动之间的歧义。

### 输入与初始化

给定一段动态相机拍摄的视频，系统首先获取两项初始估计：
- **相机空间人体姿态**：由 **HybrIK** 提供相机坐标系下的 SMPL 参数化人体运动。
- **相机轨迹**：由 **DROID-SLAM** 提供初始相机位姿轨迹，但其尺度不准确。

### 优化变量

框架在全局坐标系下联合优化以下变量（见 Eq. 11）：

$$
\min_{\mathbf{H},\mathcal{C},s,h_0,R_0,\beta} \mathcal{L}_{\mathrm{body}} + \mathcal{L}_{\mathrm{COIN-SDS}} + \mathcal{L}_{\mathrm{HSR}}
$$

其中：
- $\mathbf{H}$：全局人体运动（SMPL 参数序列）。
- $\mathcal{C}$：相机轨迹。
- $s$：相机轨迹的全局尺度因子。
- $h_0, R_0$：第一帧人体的全局平移与旋转。
- $\beta$：人体形状参数。

### 三大损失模块

**1. 人体运动约束 $\mathcal{L}_{\mathrm{body}}$**（Eq. 12）

$$
\mathcal{L}_{\mathrm{body}} = \mathcal{L}_{\mathrm{2D}} + \mathcal{L}_{\mathrm{3D}} + \mathcal{L}_{\beta} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{contact}}
$$

包含 2D 重投影误差、3D 关节约束、形状正则、时序平滑项和足部接触项，确保优化后的人体运动与视频观测一致。

**2. COIN-SDS 扩散先验损失 $\mathcal{L}_{\mathrm{COIN-SDS}}$**

这是 COIN 的核心创新。与现有方法使用单步 SDS（Score Distillation Sampling）且缺乏控制不同，COIN-SDS 通过三个关键设计生成高质量、与观测一致的伪真值运动：
- **多步 DDIM 去噪**：使用 10 步去噪产生稳定的伪真值，而非单步估计（Eq. 5-6）。
- **动态控制信号**：将上一轮优化结果作为控制信号输入扩散模型的控制分支，引导去噪过程朝向与观测对齐的方向（Eq. 7）。
- **软修复策略**：基于 2D 关键点置信度 $\mathbf{S}$ 和去噪时间步 $t$ 构建连续掩膜 $\tilde{\mathbf{M}}$（Eq. 9），对高置信度观测区域施加软约束，而非硬性替换（Eq. 8a-8c）。

最终 COIN-SDS 损失为（Eq. 10）：

$$
\min_{\mathbf{H}} \mathcal{L}_{\mathrm{COIN-SDS}} := \mathbb{E}_t\left[ \frac{\omega(t)\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \| \mathbf{H} - \tilde{\mathbf{H}}_0(\mathbf{H}, \mathbf{M}, \mathbf{S}, t) \|_2^2 \right]
$$

**3. 人-场景关系损失 $\mathcal{L}_{\mathrm{HSR}}$**（Eq. 13）

相机尺度优化是全局运动估计的瓶颈。现有方法（如 **PACE**, Kocabas et al., 3DV 2024）仅通过全局人体运动的重投影误差优化尺度，当人体运动估计不准确时尺度优化极易失败。

COIN 引入独立于人体运动的约束：利用 DROID-SLAM 提供的场景点云，惩罚深度顺序错误。具体而言，当场景点 $\mathcal{T}^{(i)}(p)$ 被人体遮挡（不可见）时，其深度应大于最近人体关节 $j^{(i)}(p)$ 的深度：

$$
\mathcal{L}_{\mathrm{HSR}} = -\frac{1}{|\mathcal{P}|} \sum_{i=1}^{T} \sum_{p \in \mathcal{P}^*} \min(0, \mathcal{T}^{(i)}(p)_z - j^{(i)}(p)_z) \cdot \mathbb{1}(\mathcal{T}^{(i)}(p) \text{ is invisible})
$$

该损失将相机尺度与人体运动解耦，即使人体运动估计存在误差，场景深度关系仍能为尺度优化提供有效约束。

### 迭代优化流程

整个框架采用多阶段迭代优化（见 **Figure 2** 和 **Algorithm 1**）：
1. 以 HybrIK 和 DROID-SLAM 的初始估计为起点。
2. 在每轮迭代中，COIN-SDS 模块以当前优化结果为控制信号，通过多步 DDIM 去噪和软修复生成伪真值运动，计算 $\mathcal{L}_{\mathrm{COIN-SDS}}$。
3. 同时计算 $\mathcal{L}_{\mathrm{body}}$ 和 $\mathcal{L}_{\mathrm{HSR}}$。
4. 联合优化所有变量，更新人体运动、相机轨迹和尺度。
5. 更新后的结果作为下一轮的控制信号，形成闭环迭代。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Given a video with a moving camera, we recover the global human motion H and camera motion C using an iterative optimization framework. We propose a novel Control-Inpainting SDS loss (LCOIN-SDS) to leverage motion diffusion models as a prior. COIN-SDS is designed such that the sampled motions from the motion prior are consistent with video observations. We achieve this by controlling and constraining the sampling process of the motion diffusion model through novel control and softinpainting branches. We also propose a novel human-scene relation loss $\left( \mathcal { L } _ { \mathrm { { H S R } } } \right$) to encourage consistency among the human motion, camera motion, and scene f...

消融实验验证了各模块的关键作用：移除 $\mathcal{L}_{\mathrm{HSR}}$ 使 RICH 数据集上的 W-MPJPE 从 254.5 mm 升至 273.0 mm；移除控制采样使 W-MPJPE 增加 570.5 mm（69.3%），相机 ATE-S 增加 167.9 mm（30.3%）；移除软修复使 PA-MPJPE 增加 4.7 mm（见 Table 1, Table 4）。

## 核心模块与公式推导

### 3.1 扩散先验的 SDS 基础

COIN 的核心目标是从单目视频中联合恢复全局人体运动 $\mathbf{H}$ 和相机运动 $\mathcal{C}$。为了利用运动扩散模型的先验知识，方法引入分数蒸馏采样（Score Distillation Sampling, SDS）框架。

给定人体运动 $\mathbf{H}$，前向扩散过程将其加噪为隐变量 $\mathbf{H}_t$：

$$q(\mathbf{H}_t | \mathbf{H}) = \mathcal{N}(\mathbf{H}_t; \sqrt{\bar{\alpha}_t} \mathbf{H}, (1 - \bar{\alpha}_t) \mathbf{I}) \tag{Eq. 1}$$

其中 $\bar{\alpha}_t$ 为噪声调度参数。原始 SDS 目标通过最小化加权去噪得分匹配损失来蒸馏运动先验：

$$\min_{\mathbf{H}} \mathcal{L}_{\mathrm{SDS}} := \mathbb{E}_{t,\epsilon}[\omega(t) \| \epsilon_\phi^t - \epsilon \|_2^2] \tag{Eq. 2}$$

其中 $\epsilon_\phi^t$ 是预训练扩散模型 $\mathcal{D}_\phi$ 在时间步 $t$ 预测的噪声，$\omega(t)$ 为权重函数。

通过重参数化，可将 SDS 目标等价转换为最小化 $\mathbf{H}$ 与单步去噪估计 $\hat{\mathbf{H}}_0^t$ 之间的差异：

$$\min_{\mathbf{H}} \mathcal{L}_{\mathrm{SDS}} := \mathbb{E}_t\left[ \frac{\omega(t)\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \| \mathbf{H} - \hat{\mathbf{H}}_0^t \|_2^2 \right] \tag{Eq. 3}$$

其中单步去噪伪真值运动为：

$$\hat{\mathbf{H}}_0^t = \frac{\mathbf{H}_t - \sqrt{1-\bar{\alpha}_t} \epsilon_\phi^t}{\sqrt{\bar{\alpha}_t}} \tag{Eq. 4}$$

这一重参数化揭示了原始 SDS 的瓶颈：**单步去噪产生的伪真值 $\hat{\mathbf{H}}_0^t$ 质量不足，且预训练扩散模型对输入高度敏感——隐变量 $\mathbf{H}_t$ 的微小波动会导致去噪运动发生显著变化，造成跨迭代的不一致性。**

### 3.2 COIN-SDS：控制-修复扩散先验

为克服上述瓶颈，COIN 提出三项关键改进，构成 COIN-SDS 模块。

**多步 DDIM 去噪。** 用多步 DDIM 采样替代单步去噪，生成高质量的伪真值运动。单步 DDIM 更新的形式为：

$$\tilde{\mathbf{H}}_{t-\Delta t} = \sqrt{\bar{\alpha}_{t-\Delta t}} \cdot \hat{\mathbf{H}}_0^t + \sqrt{1-\bar{\alpha}_{t-\Delta t}} \cdot \epsilon_\phi^t \tag{Eq. 5}$$

经过 $K$ 步迭代后获得伪真值 $\tilde{\mathbf{H}}_0$，COIN-SDS 目标变为：

$$\min_{\mathbf{H}} \mathcal{L}_{\mathrm{SDS}} := \mathbb{E}_t\left[ \frac{\omega(t)\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \| \mathbf{H} - \tilde{\mathbf{H}}_0 \|_2^2 \right] \tag{Eq. 6}$$

实验表明 10 步去噪即可产生高质量伪真值。

**动态控制采样。** 在预训练扩散模型 $\mathcal{D}_\phi$ 上附加控制分支 $\phi_c$，以当前优化得到的人体运动作为控制信号 $\mathbf{c}$，引导去噪过程生成与视频观测对齐的运动：

$$\tilde{\mathbf{H}}_0^t = \mathcal{D}_{\phi,\phi_c}(\tilde{\mathbf{H}}_t, t, \mathbf{c} \odot \mathbf{M}) \tag{Eq. 7}$$

其中 $\mathbf{M}$ 是基于 2D 关键点置信度的可见性掩膜。控制信号来自上一轮迭代的优化结果，实现动态更新，确保蒸馏过程随优化逐步精细化。

**软修复策略。** 将高置信度观测区域作为软约束注入去噪过程。已知区域直接使用观测值 $\mathbf{H}$，未知区域由扩散模型生成：

$$\tilde{\mathbf{H}}_0^{t,\mathrm{known}} = \mathbf{H} \tag{Eq. 8a}$$
$$\tilde{\mathbf{H}}_0^{t,\mathrm{unknown}} = \mathcal{D}_{\phi,\phi_c}(\tilde{\mathbf{H}}_t, t, \mathbf{H} \odot \mathbf{M}) \tag{Eq. 8b}$$

两者通过连续掩膜融合：

$$\tilde{\mathbf{H}}_0^t = \mathbf{M} \odot \tilde{\mathbf{H}}_0^{t,\mathrm{known}} + (1-\mathbf{M}) \odot \tilde{\mathbf{H}}_0^{t,\mathrm{unknown}} \tag{Eq. 8c}$$
$$\tilde{\mathbf{M}} = w(t) * \mathbf{S} \odot \mathbf{M} \tag{Eq. 9}$$

其中 $\mathbf{S}$ 为观测置信度得分，$w(t)$ 为时间步相关权重。连续掩膜使修复强度随置信度和去噪进度自适应调节，避免硬修复导致的边界伪影。

综合三项改进，COIN-SDS 的最终目标为：

$$\min_{\mathbf{H}} \mathcal{L}_{\mathrm{COIN-SDS}} := \mathbb{E}_t\left[ \frac{\omega(t)\sqrt{\bar{\alpha}_t}}{\sqrt{1-\bar{\alpha}_t}} \| \mathbf{H} - \tilde{\mathbf{H}}_0(\mathbf{H}, \mathbf{M}, \mathbf{S}, t) \|_2^2 \right] \tag{Eq. 10}$$

### 3.3 全局联合优化与人-场景关系损失

COIN 将人体运动 $\mathbf{H}$、相机轨迹 $\mathcal{C}$、尺度 $s$、第一帧人体朝向 $h_0$、第一帧相机位姿 $R_0$ 以及人体形状参数 $\beta$ 纳入统一的优化框架：

$$\min_{\mathbf{H},\mathcal{C},s,h_0,R_0,\beta} \mathcal{L}_{\mathrm{body}} + \mathcal{L}_{\mathrm{COIN-SDS}} + \mathcal{L}_{\mathrm{HSR}} \tag{Eq. 11}$$

其中人体运动损失 $\mathcal{L}_{\mathrm{body}}$ 包含重投影误差、3D 关节约束、形状正则、平滑项和足部接触约束：

$$\mathcal{L}_{\mathrm{body}} = \mathcal{L}_{\mathrm{2D}} + \mathcal{L}_{\mathrm{3D}} + \mathcal{L}_{\beta} + \mathcal{L}_{\mathrm{smooth}} + \mathcal{L}_{\mathrm{contact}} \tag{Eq. 12}$$

**人-场景关系损失（Human-Scene Relation Loss）** 是 COIN 解耦相机尺度与人体运动的关键模块。该损失利用场景点云与人体关节之间的深度顺序关系，为相机尺度提供独立于人体运动的约束：

$$\mathcal{L}_{\mathrm{HSR}} = -\frac{1}{|\mathcal{P}|} \sum_{i=1}^{T} \sum_{p \in \mathcal{P}^*} \min(0, \mathcal{T}^{(i)}(p)_z - j^{(i)}(p)_z) \cdot \mathbb{1}(\mathcal{T}^{(i)}(p) \text{ is invisible}) \tag{Eq. 13}$$

其中 $\mathcal{T}^{(i)}(p)$ 是经相机变换后的场景点 $p$，$j^{(i)}(p)$ 是距离该点最近的人体关节，$\mathcal{P}^*$ 为被人体遮挡的场景点子集。该损失惩罚错误的深度顺序：当场景点被人体遮挡时，其深度应大于对应关节的深度。通过这一约束，相机尺度优化不再完全依赖全局人体运动的重投影误差，从而有效缓解尺度模糊问题。

**因果机制总结：** COIN-SDS 通过多步 DDIM 去噪（Eq. 5-6）提升伪真值质量，通过动态控制信号（Eq. 7）确保运动与观测对齐，通过软修复（Eq. 8-9）保持高置信度区域的一致性；人-场景关系损失（Eq. 13）则为相机尺度提供了独立于人体运动的几何约束，解耦了两者之间的相互影响。

## 实验与分析

### 全局人体运动估计

COIN 在三个公开数据集上全面评估了全局人体运动估计性能，与当前最优方法 **PACE**（Kocabas et al., 3DV 2024）和同期工作 **WHAM**（Shin et al., CVPR 2024）进行了系统比较。

在 **RICH** 数据集上（Table 1），COIN 取得了 254.5 mm 的 W-MPJPE，相比 PACE 的 380.0 mm 降低了 125.5 mm（33%），相比 WHAM 的改进幅度达到 49%。这一显著提升的核心驱动力来自两个关键设计：控制采样（Controlled Sampling）将 W-MPJPE 从 825.0 mm 降至 254.5 mm，降幅达 69.3%；软修复（Soft Inpainting）进一步将 PA-MPJPE 降低了 4.7 mm。消融实验还表明，移除人-场景关系损失 $\mathcal{L}_{\mathrm{HSR}}$ 会导致 W-MPJPE 从 254.5 mm 恶化至 273.0 mm，验证了该损失对尺度解耦的独立贡献。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/003_Table_1.jpg]]
*Table 1: Global human motion estimation on the RICH dataset*

在 **EMDB** 数据集上（Table 2），COIN 在 W-MPJPE_100 指标上达到 407.3 mm，相比 WHAM 提升 7%。Table 5 的消融进一步确认了控制采样和软修复在该数据集上的增益一致性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/004_Table_2.jpg]]
*Table 2: Global human motion estimation on the EMDB dataset*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/009_Table_5.jpg]]
*Table 5: Global human motion estimation on the EMDB dataset*

在 **HCM** 数据集上（Table 3），COIN 相比 PACE 在 W-MPJPE 上实现了 44% 的改进。Table 7 的消融实验再次验证了各模块的有效性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/005_Table_3.jpg]]
*Table 3: Global human motion estimation on the HCM dataset*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/013_Table_7.jpg]]
*Table 7: Global human motion estimation on the HCM dataset*

### 相机运动估计

Table 4 报告了 HCM 数据集上的相机运动估计结果。控制采样将相机轨迹误差 ATE-S 降低了 167.9 mm（30.3%），表明 COIN-SDS 生成的伪真值运动质量对相机优化同样至关重要。人-场景关系损失通过引入场景深度约束，为相机尺度提供了独立于人体运动的优化信号，有效缓解了尺度模糊问题。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/006_Table_4.jpg]]
*Table 4: Camera motion estimation on the HCM dataset*

### 关键消融发现

1. **控制采样是最强单一模块**：在 RICH 上，控制采样单独贡献了 570.5 mm 的 W-MPJPE 降幅（69.3%），在相机 ATE-S 上贡献了 167.9 mm 降幅（30.3%）。这证实了动态控制信号对引导扩散模型生成与观测一致的伪真值运动的核心作用。

2. **软修复的连续掩膜设计有效**：基于置信度分数 $\mathbf{S}$ 和去噪时间步 $t$ 的连续掩膜 $\tilde{\mathbf{M}} = w(t) * \mathbf{S} \odot \mathbf{M}$，在 PA-MPJPE 上带来 4.7 mm 的增益，验证了软约束优于硬修复。

3. **人-场景关系损失解耦尺度优化**：移除 $\mathcal{L}_{\mathrm{HSR}}$ 导致 W-MPJPE 增加 18.5 mm（RICH），证明场景深度顺序约束为相机尺度提供了独立于人体运动的有效正则化。

4. **去噪步数效率**：使用 10 步 DDIM 去噪即可生成高质量伪真值运动，在计算效率与运动质量间取得良好平衡。

### 定性分析

Figure 3 展示了 COIN 与 PACE、WHAM 的定性对比。在滑板场景中（Figure 1），PACE 和 WHAM 因分布外运动（out-of-distribution）而完全失败，COIN 则凭借控制-修复扩散先验成功恢复了正确的人体轨迹和相机运动。在行走方向估计上，WHAM 给出了错误的方向预测，COIN 准确恢复了人体运动方向。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/001_Figure_1.jpg]]
*Figure 1: Capturing global human and camera motion from a dynamic camera presents unique challenges. In the input video, a person is riding a skateboard – while the local body motion may remain relatively constant, the global position of the individual changes significantly. Current state-of-the-art methods such as PACE [41] and WHAM [81] fail catastrophically on such out-of-distribution motions. Our approach, COIN, gracefully handles such challenging cases, owing to our control-inpainting motion diffusion prior and novel human-scene relation loss*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with state-of-the-art methods. PACE [41] fails to recover a correct trajectory (left). WHAM [81] estimates the wrong walking direction of the person (right). Our approach, COIN, recovers the human and camera motion accurately in both scenarios*

### 初始化方法对比

Table 6 比较了 SLAM 与 ParticleSfM 在 EMDB 收敛子集上的初始化效果。结果表明，ParticleSfM 在部分序列上提供了更可靠的相机初始化，但 COIN 的联合优化框架能够在一定程度上容忍初始化的不完美。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/012_Table_6.jpg]]
*Table 6: SLAM vs. ParticleSfM on the converged subset of the EMDB dataset*

### 失败模式与局限

尽管 COIN 在多个数据集上大幅领先现有方法，其性能仍依赖于 SLAM 或 ParticleSfM 初始化的基本可靠性。当初始化完全失败时，联合优化的收敛性可能受到影响。此外，当前方法使用离线优化框架，尚不支持实时估计。如何通过少步 DDIM 采样实现实时联合人体-相机扩散模型估计，仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2408_16426/figures/010_Table.jpg]]

## 方法谱系与知识库定位

### 1. 问题定位与基线谱系

COIN 聚焦于**动态相机下全局人体运动与相机运动的联合估计**，其核心瓶颈在于：现有方法使用单步 SDS 且缺乏控制，导致运动伪真值不一致、过于平滑，无法对齐视频观测；相机尺度优化完全依赖不准确的全局人体运动，容易导致失败。

该问题的基线谱系可沿两条线索梳理：

**（1）全局人体运动估计方法**

- **PACE**（Kocabas et al., 3DV 2024）：当前 SOTA，联合优化人体与相机运动，但依赖单步 SDS 蒸馏且缺乏控制信号，在分布外运动上表现脆弱。COIN 在 HCM 和 RICH 数据集上分别以 44% 和 33% 的 W-MPJPE 提升超越 PACE。
- **WHAM**（Shin et al., CVPR 2024）：同期工作，COIN 在 RICH 和 EMDB 上分别以 49% 和 7% 的优势超越。
- **SLAHMR**（Ye et al., CVPR 2023）：利用 SLAM 与运动先验进行全局人体运动估计的先驱工作。
- **GLAMR**（Yuan et al., CVPR 2022）：全局人体运动估计方法，但忽略相机运动。

**（2）扩散先验使用方法**

- **Vanilla SDS**：朴素得分蒸馏采样，单步去噪、无控制信号、无修复策略，导致伪真值质量低且与观测不一致。
- **Guided Sampling**：在去噪过程中嵌入解析引导，但缺乏动态控制信号。
- **Noise Optimization**：通过优化噪声来生成运动，同样缺乏控制与修复机制。

### 2. 核心变更槽位

COIN 相对于上述基线的方法变更可归纳为四个关键槽位：

| 槽位 | 基线值 | COIN 方案 | 证据锚点 |
|------|--------|-----------|----------|
| 扩散先验蒸馏方法 | 单步 SDS 无控制与修复 | COIN-SDS（多步 DDIM、动态控制、软修复） | Sec. 3.1, 3.2, Algorithm 1 |
| 去噪控制信号 | 固定初始运动估计（来自 HybrIK） | 基于上一轮优化结果的动态控制信号 | Sec. 3.2 |
| 修复策略 | 无修复或硬修复 | 基于置信度和时间步的软修复连续掩膜 | Eq. 9, Sec. 3.2 |
| 相机尺度正则化 | 仅通过全局人体运动的重投影误差优化尺度 | 人-场景深度关系损失，解耦相机尺度与人体运动 | Sec. 3.3, Eq. 13 |

### 3. 方法因果机制

COIN 的核心因果链可拆解为两个相互增强的机制：

**机制一：COIN-SDS 提升伪真值质量**

扩散模型对输入高度敏感，潜在变量的微小波动即可显著改变去噪结果，导致不一致。COIN-SDS 通过三条路径解决此问题：

1. **多步 DDIM 去噪**：将单步去噪替换为 10 步 DDIM 采样（Eq. 5），生成高质量伪真值 $\tilde{\mathbf{H}}_0$，作为 SDS 损失的目标（Eq. 6）。消融实验表明 10 步足以产生高质量伪真值。
2. **动态控制信号**：在受控去噪器 $\mathcal{D}_{\phi,\phi_c}$ 中，使用上一轮优化结果作为控制信号 $\mathbf{c} \odot \mathbf{M}$（Eq. 7），引导扩散模型生成与观测对齐的运动。消融显示控制采样使 W-MPJPE 降低 570.5 mm（69.3%），ATE-S 降低 167.9 mm（30.3%）。
3. **软修复策略**：高置信度区域直接使用观测值 $\mathbf{H}$，未知区域由扩散模型生成（Eq. 8a-8c），通过连续掩膜 $\tilde{\mathbf{M}} = w(t) * \mathbf{S} \odot \mathbf{M}$（Eq. 9）平滑过渡。消融表明软修复使 PA-MPJPE 降低 4.7 mm。

**机制二：人-场景关系损失解耦尺度优化**

传统方法仅通过人体运动的重投影误差优化相机尺度，当人体运动估计不准确时尺度优化必然失败。COIN 引入 $\mathcal{L}_{\mathrm{HSR}}$（Eq. 13），利用场景点云深度关系独立约束相机尺度：当场景点被遮挡时，其深度应大于最近人体关节的深度。该损失为人-相机-场景三者提供一致性约束，消融显示移除 $\mathcal{L}_{\mathrm{HSR}}$ 会使 RICH 上 W-MPJPE 从 254.5 上升至 273.0。

### 4. 适用边界与局限

**适用边界**：

- COIN 依赖 HybrIK 提供初始相机空间姿态，依赖 DROID-SLAM 提供初始相机轨迹。当 SLAM 初始化灾难性失败时，方法性能可能显著下降（此点需手动验证，论文未提供直接证据）。
- 多阶段优化框架（Sec. 3.3, Eq. 11-12）中，ParticleSfM 可能在某些场景下无法收敛，影响整体性能（此点需手动验证）。
- 掩膜 $\mathbf{M}$ 基于 2D 关键点置信度分数构建，其精确公式在现有证据中未明确给出。

**局限与开放问题**：

1. **相机与人体运动的解耦**：如何在一般意义上解耦相机运动与人体运动仍是一个开放问题。
2. **SLAM 失败的鲁棒性**：当 SLAM 初始化灾难性失败时，COIN 的表现如何？论文未提供此类分析。
3. **实时性**：联合人-相机扩散模型是否可通过少步 DDIM 采样实现实时估计？这是一个有前景的方向。
4. **多阶段优化的收敛性**：当 ParticleSfM 无法收敛时，多阶段优化的处理策略尚不明确。
5. **掩膜设计细节**：基于 2D 关键点置信度分数的掩膜 $\mathbf{M}$ 的确切公式需查阅补充材料或代码确认。

## 原文 PDF

![[paperPDFs/ECCV_2024/COIN_Control_Inpainting_Diffusion_Prior_for_Human_and_Camera_Motion_Estimation.pdf]]
