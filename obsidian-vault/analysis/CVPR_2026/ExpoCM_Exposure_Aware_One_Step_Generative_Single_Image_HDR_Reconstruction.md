---
title: "ExpoCM: Exposure-Aware One-Step Generative Single-Image HDR Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ExpoCM_Exposure_Aware_One_Step_Generative_Single_Image_HDR_Reconstruction.pdf
project_link: null
code_link: "https://github.com/AoyuLiu01/ExpoCM"
aliases:
- ExpoCM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过构建曝光感知的一致性轨迹（Exposure-Aware Consistency Trajectory），将输入LDR图像按曝光程度分区，为不同区域定制PF-ODE流形：过曝区从纯噪声生成细节，欠曝区注入低频先验并去噪，正常区可靠传递内容，从而在单一推理步中实现高质量重建。
primary_logic: 将HDR重建建模为条件生成问题，利用一致性模型框架，以曝光分区驱动的空间变化ODE轨迹替代均匀扩散过程，同时结合曝光引导的亮度-色度损失在感知均匀空间中进行自适应监督，达到快速且保真的一步式HDR生成。
claims:
- ExpoCM in one inference step achieves over 400× speedup vs DDPM (1000 steps) and 20× vs DDIM (50 steps).
- On HDR-REAL, ExpoCM achieves PSNR-μ 28.66 dB, surpassing second-best HDRDiff by 0.89 dB.
- Ablation shows Three-Mask EACT improves PSNR-μ over uniform baseline by +4.66 dB on HDR-REAL.
- ELC loss reduces ΔE2000 compared to uniform CIE L*a*b* loss, confirming exposure-aware weighting mitigates brightness/color bias.
---

# ExpoCM: Exposure-Aware One-Step Generative Single-Image HDR Reconstruction

> [!tip] 核心洞察
> 将HDR重建建模为条件生成问题，利用一致性模型框架，以曝光分区驱动的空间变化ODE轨迹替代均匀扩散过程，同时结合曝光引导的亮度-色度损失在感知均匀空间中进行自适应监督，达到快速且保真的一步式HDR生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | ExpoCM: 曝光感知的一步式生成单图HDR重建 |
| 英文题名 | ExpoCM: Exposure-Aware One-Step Generative Single-Image HDR Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.02464) · [Code](https://github.com/AoyuLiu01/ExpoCM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ExpoCM |
| Dataset | HDR-REAL, HDR-EYE, AIM2025, Inference speed |

> [!tip] 效果简介
> - HDR-REAL 上，PSNR-μ (dB) 28.66 vs 27.77 (HDRDiff) (+0.89)。
> - HDR-EYE 上，PSNR-μ (dB) 20.75 vs 20.23 (DMHDR) (+0.52)。
> - AIM2025 上，PSNR-μ (dB) 29.02 vs 28.71 (HDRDiff) (+0.31)。

## 概要

单图高动态范围（HDR）重建旨在从单张低动态范围（LDR）图像恢复丢失的高光与阴影细节。核心瓶颈在于空间异质性退化：过曝区域因饱和导致纹理完全丢失，欠曝区域噪声被放大，而正常区域仅需忠实传递内容。现有回归方法（如 **HDRCNN** (Eilertsen et al., ACM TOG 2017)、**HDRUNet** (Chen et al., CVPR 2021)）难以生成被饱和掩盖的细节；扩散模型（如 **HDRDiff** (Dalal et al., ICIP 2023)、**DMHDR** (Liu et al., IEEE TCSVT 2025)）虽具生成能力，但推理需数百步采样，且其均匀扩散轨迹忽视了不同曝光区域对生成强度的差异化需求。

**ExpoCM** 针对上述矛盾，将HDR重建建模为条件生成问题，并基于一致性模型（Consistency Models）实现一步式推理。其核心调控机制是**曝光感知一致性轨迹（Exposure-Aware Consistency Trajectory, EACT）**：根据亮度统计将LDR输入软分割为过曝、欠曝、正常三区，为各区定制PF-ODE流形——过曝区从纯噪声生成细节，欠曝区注入低频LDR先验并去噪，正常区可靠传递内容，再通过空间混合形成全局轨迹。配合在CIE L*a*b*感知均匀空间中施加的**曝光引导亮度-色度（ELC）损失**，框架以曝光自适应权重平衡亮度与色度重建精度。

**关键实证结果**：在HDR-REAL基准上，ExpoCM以单步推理取得PSNR-μ 28.66 dB，超越次优方法HDRDiff 0.89 dB，同时ΔE2000降至4.02。推理速度方面，相比DDPM（1000步）加速超400倍，相比DDIM（50步）加速约20倍。消融实验表明，三掩码EACT相比均匀轨迹基线提升PSNR-μ达+4.66 dB，ELC损失进一步降低感知色差，验证了曝光感知设计对重建保真度的决定性作用。

高动态范围（High Dynamic Range, HDR）成像旨在捕获和再现真实场景中宽广的亮度范围，避免因传感器动态范围受限而导致的过曝饱和与欠曝噪声。然而，HDR内容的采集通常依赖多帧不同曝光的LDR（Low Dynamic Range）图像进行融合，这对动态场景或手持拍摄极为不利。因此，从单张LDR图像重建HDR内容——即单图HDR重建——成为一个极具实用价值的研究方向。

该任务的核心瓶颈在于**空间异质性退化**：输入LDR图像中，过曝区域因像素饱和而丢失纹理细节，欠曝区域则因信噪比极低而放大噪声，正常曝光区域的信息相对可靠。这种随空间位置剧烈变化的退化模式，要求重建算法必须具备区域自适应的恢复能力。

现有方法大致可分为两类。**基于CNN的回归方法**，如**HDRCNN**（Eilertsen et al., ACM TOG 2017）、**ExpandNet**（Marnerides et al., Comput. Graph. Forum 2018）、**HDRUNet**（Chen et al., CVPR 2021）以及**Single-HDR**（Liu et al., CVPR 2020），通过端到端映射直接预测HDR图像。这些方法推理速度快，但在严重过曝或欠曝区域往往产生模糊或伪影，因为回归范式缺乏对缺失内容的生成能力。**基于扩散模型的生成方法**，如**HDRDiff**（Dalal et al., ICIP 2023）和**DMHDR**（Liu et al., IEEE TCSVT 2025），利用扩散过程的强先验来生成合理的细节，显著提升了重建质量。然而，它们存在两个根本性缺陷：一是推理需多步采样（DDPM需1000步，DDIM需50步以上），计算成本极高；二是其扩散轨迹在空间上是均匀的，忽视了不同曝光区域对生成过程的不同需求——过曝区需要从噪声中“创造”细节，欠曝区需要注入结构先验并去噪，而正常区则应尽可能保真传递内容。

上述缺口催生了本文的核心动机：**能否在保持生成能力的同时，实现一步式快速推理，并让生成过程显式地感知和适应曝光异质性？** 一致性模型（Consistency Models, CMs）提供了将多步扩散蒸馏为单步推理的理论框架，但其标准形式仍采用空间均匀的PF-ODE轨迹。本文的关键洞察在于：**将HDR重建建模为条件生成问题，以曝光分区驱动的空间变化ODE轨迹替代均匀扩散过程，从而在单一推理步中实现区域自适应的、高质量HDR生成。**

## 核心方法与创新机理

ExpoCM 的核心创新在于将单图 HDR 重建重新建模为**曝光感知的条件生成问题**，并通过三个相互耦合的 changed slots 突破现有方法的瓶颈：空间异质性退化下的保真度与效率矛盾。

### 瓶颈诊断：空间异质性退化与均匀轨迹的根本缺陷

单图 HDR 重建的困难源于 LDR 图像中**空间异质的退化模式**：过曝区域饱和导致细节不可逆丢失，欠曝区域噪声放大且信噪比极低，正常区域则相对可靠。现有回归方法（如 **HDRCNN** (Eilertsen et al., ACM TOG 2017)、**HDRUNet** (Chen et al., CVPR 2021)）难以从饱和像素中恢复真实纹理；扩散模型（如 **HDRDiff** (Dalal et al., ICIP 2023)、**DMHDR** (Liu et al., IEEE TCSVT 2025)）虽具备生成能力，但其条件轨迹（Eq. 3）隐含假设退化在空间上均匀分布——对过曝、欠曝和正常区域施加相同的扩散/去噪动力学，导致过曝区生成不足、欠曝区噪声残留，且多步采样（DDPM 1000 步、DDIM 50 步）计算成本极高。

### 创新点一：曝光感知的一致性轨迹（EACT）——从均匀流形到分区定制

ExpoCM 的核心操控变量是 **PF-ODE 轨迹的空间结构**。方法将传统的均匀条件轨迹替换为**曝光感知的一致性轨迹（Exposure-Aware Consistency Trajectory, EACT）**，其构建逻辑为：

1. **曝光掩码生成**：基于输入 LDR 的亮度通道 $Y$，利用百分位数 $q_{\mathrm{lo}}$、$q_{\mathrm{hi}}$ 和边距 $\tau$ 计算软分割掩码，将图像划分为过曝、欠曝和正常三个区域（Eq. 5–7）。
2. **区域定制轨迹**：为三种区域分别构造不同的 PF-ODE 流形——
   - **过曝区** $\mathbf{x}_t^o = (1 - \alpha(t)) \mathbf{x}_0 + \sigma_o(t) \boldsymbol{\epsilon}$：完全从纯噪声生成细节，不依赖不可靠的 LDR 输入；
   - **欠曝区** $\mathbf{x}_t^u = (1 - \alpha(t)) \mathbf{x}_0 + \alpha(t) \lambda_u \mathcal{F}_{\mathrm{low}}(\mathbf{y}_0) + \sigma_u(t) \boldsymbol{\epsilon}$：注入低通滤波的 LDR 先验提供粗略结构，同时保留噪声注入以增强生成能力；
   - **正常区** $\mathbf{x}_t^g$：可靠传递 LDR 内容信息。
3. **空间混合**：通过曝光感知权重图将三条轨迹混合为全局轨迹 $\mathbf{x}_t = w_{\mathrm{over}} \odot \mathbf{x}_t^o + w_{\mathrm{under}} \odot \mathbf{x}_t^u + w_{\mathrm{good}} \odot \mathbf{x}_t^g$（Eq. 11），使模型在单一推理步中同时完成过曝区的内容生成、欠曝区的结构恢复与去噪、正常区的内容保持。

这一设计的深层洞察在于：**将 HDR 重建从统一的回归/扩散问题解耦为不同曝光条件下的差异化生成子问题**，并以数学上精确的 ODE 混合实现统一的一步式框架。消融实验（Table 2）证实，Three-Mask EACT 相比均匀轨迹基线在 HDR-REAL 上 PSNR-μ 提升 **+4.66 dB**，且过曝区与高光区的重建误差显著降低（Figure 4）。

### 创新点二：曝光引导的亮度-色度损失（ELC Loss）——自适应感知监督

传统损失函数在像素空间或均匀颜色空间中施加均匀惩罚，无法区分不同曝光区域的感知重要性。ExpoCM 提出 **曝光引导的亮度-色度损失（Exposure-guided Luminance-Chromaticity Loss, ELC Loss）**，在感知均匀的 CIE L*a*b* 空间中引入曝光依赖的自适应权重：

$$\mathcal{L}_{\mathrm{ELC}} = \mathbb{E} \left[ w_L \cdot \rho(\Delta L^*) \right] + \mathbb{E} \left[ w_C \cdot \rho(\Delta C^*) \right]$$

其中亮度权重 $w_L$ 和色度权重 $w_C$ 根据曝光掩码动态调整：在欠曝区域加强亮度监督以抑制噪声，在过曝区域放宽亮度约束以容忍合理的高光偏移，同时保持色度保真度。消融实验（Table 3）表明，完整的 ELC loss 使 ΔE2000 降至 **4.02**（HDR-REAL），相比去除曝光加权的均匀 CIE L*a*b* 损失显著降低亮度和色度偏差（Figure 5）。

### 创新点三：两阶段训练策略——从轨迹学习到感知精调

ExpoCM 采用两阶段训练策略以平衡轨迹一致性与感知质量：第一阶段仅使用一致性训练损失 $\mathcal{L}_{\mathrm{CT}}$ 优化网络学习 EACT 的 PF-ODE 流形；第二阶段引入 ELC loss 进行精调，在已收敛的轨迹基础上注入曝光感知的颜色监督。这一策略避免了从随机初始化直接联合优化复杂损失可能导致的不稳定，确保了一步式推理的高质量输出。

### 创新协同效应：一步式高效生成

上述三个 changed slots 的协同效应体现在：EACT 提供了空间自适应的生成流形，ELC loss 在感知空间中进行曝光感知的精细监督，两阶段训练保证了优化稳定性。最终，ExpoCM 在**单步推理**中实现 SOTA 重建质量——PSNR-μ 28.66 dB（HDR-REAL），同时推理速度相比 DDPM 1000 步加速 **>400×**，相比 DDIM 50 步加速 **>20×**，从根本上解决了扩散模型在 HDR 重建中的效率瓶颈。

ExpoCM 将单图 HDR 重建建模为一个条件生成问题，并构建在一个一致性模型（Consistency Model, CM）框架之上。其核心思想是：将输入 LDR 图像 $\mathbf{y}_0$ 作为条件，通过一个曝光感知的一致性轨迹（Exposure-Aware Consistency Trajectory, EACT）来驱动概率流 ODE（PF-ODE）的生成过程，最终由一致性网络 $f_\theta$ 在**单步推理**内预测出干净的目标 HDR 图像 $\mathbf{x}_0$。

整体 pipeline 由四个关键模块串联构成，如图 Figure 2 所示：

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of our proposed ExpoCM framework. The exposure mask generation module first partitions the input LDR y0 into over-, under-, and well-exposed regions (Fig. 2(b)). Based on these masks, we construct the exposure-aware consistency trajectory (EACT) by formulating and blending three distinct, region-specific generative flows, and the consistency network*

1.  **曝光掩码生成模块（Exposure Mask Generation Module）**
    该模块接收输入的 LDR 图像 $\mathbf{y}_0$，基于其亮度通道的统计分布（百分位数）计算软分割掩码，将图像在空间上划分为**过曝（over-exposed）**、**欠曝（under-exposed）** 和**正常曝光（well-exposed）** 三个区域，生成对应的连续置信度图 $w_{\mathrm{over}}$、$w_{\mathrm{under}}$ 和 $w_{\mathrm{good}}$。

2.  **曝光感知一致性轨迹构造器（Exposure-Aware Consistency Trajectory Constructor）**
    这是框架的核心创新。针对上述三种曝光区域的空间异质性退化，该模块为每一类区域分别定制一条从噪声到干净 HDR 的 PF-ODE 轨迹：
    -   **过曝区域轨迹** $\mathbf{x}_t^o$：仅由干净 HDR 和噪声构成，不依赖 LDR 输入，旨在从纯噪声中重新生成因饱和而丢失的细节。
    -   **欠曝区域轨迹** $\mathbf{x}_t^u$：在干净 HDR 和噪声之外，额外注入经低通滤波的 LDR 先验，以提供粗略的结构信息并抑制噪声放大。
    -   **正常区域轨迹** $\mathbf{x}_t^g$：可靠地传递 LDR 中的内容信息。
    
    最终，利用第一步生成的曝光掩码作为空间混合权重，将三条区域特定的轨迹融合为一条全局的曝光感知轨迹：
    $$
    \mathbf{x}_t = w_{\mathrm{over}} \odot \mathbf{x}_t^o + w_{\mathrm{under}} \odot \mathbf{x}_t^u + w_{\mathrm{good}} \odot \mathbf{x}_t^g
    $$
    这一设计使得生成过程能够自适应地匹配 LDR 图像中不同位置的退化特性。

3.  **一致性网络 $f_\theta$（Consistency Network）**
    该网络基于 U-Net 架构，充当条件生成器。它在训练时学习将轨迹上任意带噪状态 $\mathbf{x}_t$ 直接映射回干净的 HDR 原点 $\mathbf{x}_0$，条件是输入的 LDR 图像 $\mathbf{y}_0$。在推理时，只需从初始噪声状态执行一次网络前向，即可一步生成 HDR 结果。

4.  **曝光引导的亮度-色度损失（Exposure-guided Luminance-Chromaticity Loss, ELC Loss）**
    为了在感知均匀的空间中实现自适应监督，该模块在 CIE L\*a\*b\* 颜色空间计算重建误差，并根据曝光条件为亮度和色度分量分配不同的权重 $w_L$ 和 $w_C$。例如，在欠曝区域加大对亮度误差的惩罚，在过曝区域则对色度偏移给予一定容忍。此损失与标准的一致性训练损失 $\mathcal{L}_{\mathrm{CT}}$ 结合，采用**两阶段训练策略**：第一阶段仅使用 $\mathcal{L}_{\mathrm{CT}}$ 进行基础训练，第二阶段引入 ELC Loss 进行微调，以精细优化视觉质量。

**输入输出流**：整个框架的输入为单张 LDR 图像 $\mathbf{y}_0$，输出为一步生成的高动态范围图像 $\mathbf{x}_0$。信息流依次经过曝光掩码生成、轨迹构造、一致性网络前向传播，并在训练阶段通过 ELC Loss 进行监督，形成一个端到端、曝光感知的一步式 HDR 重建系统。

### 3.1 问题建模与一致性训练基线

ExpoCM 将单图 HDR 重建形式化为一个条件生成任务，建立在一致性模型（Consistency Models, CMs）框架之上。设目标 HDR 图像为 $\mathbf{x}_0$，输入的 LDR 图像为 $\mathbf{y}_0$。前向加噪过程由以下随机微分方程（SDE）描述：

$$d \mathbf{x}_t = f(\mathbf{x}_t, t) dt + g(t) d\mathbf{w}_t$$

该 SDE 存在一条与之共享边缘概率密度的确定性概率流常微分方程（PF-ODE）：

$$d \mathbf{x}_t = \Big[ f(\mathbf{x}_t, t) - \frac{1}{2} g(t)^2 \nabla_{\mathbf{x}_t} \log p_t(\mathbf{x}_t) \Big] dt$$

一致性网络 $f_\theta$ 被训练为预测轨迹的起点 $\mathbf{x}_0$，并以 LDR 输入 $\mathbf{y}_0$ 作为条件。其核心思想是：在 PF-ODE 轨迹上的任意相邻点对 $(\mathbf{x}_{t_n}, \mathbf{x}_{t_{n+1}})$ 上，网络输出应保持一致性，即 $f_\theta(\mathbf{x}_{t_{n+1}}, t_{n+1}, \mathbf{y}_0) = f_\theta(\mathbf{x}_{t_n}, t_n, \mathbf{y}_0)$。

然而，基线条件轨迹（Eq. 3）虽然能实现一步生成，但其公式隐含地假设了空间均匀的退化模式——这意味着对所有像素区域施加相同的扰动和去噪过程。这一假设与 LDR 图像中过曝、欠曝、正常区域所面临的异质性退化严重不符，构成了方法改进的核心切入点。

### 3.2 曝光感知一致性轨迹（Exposure-Aware Consistency Trajectory, EACT）

**核心思想**：用空间变化的轨迹替代单一的均匀轨迹，使 PF-ODE 的生成过程自适应于局部曝光条件。

#### 曝光掩码生成模块

首先从 LDR 输入 $\mathbf{y}_0$ 的亮度通道 $Y$ 中计算曝光掩码。定义亮度分布的 $q_{\mathrm{lo}}$ 和 $q_{\mathrm{hi}}$ 百分位数，并引入边距参数 $\tau = 0.02$ 来确定正常曝光核心区间的上下界：

$$l_{\mathrm{core}} = q_{\mathrm{lo}} + \tau (q_{\mathrm{hi}} - q_{\mathrm{lo}}), \quad h_{\mathrm{core}} = q_{\mathrm{hi}} - \tau (q_{\mathrm{hi}} - q_{\mathrm{lo}})$$

基于像素亮度 $Y$ 与核心区间的归一化距离，生成连续的欠曝和过曝置信度图：

$$m_{\mathrm{low}} = \mathrm{clip}\left( \frac{l_{\mathrm{core}} - Y}{\tau (q_{\mathrm{hi}} - q_{\mathrm{lo}})}, 0, 1 \right)$$

$$m_{\mathrm{high}} = \mathrm{clip}\left( \frac{Y - h_{\mathrm{core}}}{\tau (q_{\mathrm{hi}} - q_{\mathrm{lo}})}, 0, 1 \right)$$

正常曝光掩码由 $m_{\mathrm{good}} = 1 - m_{\mathrm{low}} - m_{\mathrm{high}}$ 导出。这三个软掩码构成了空间变化轨迹的权重基础。

#### 区域特定轨迹构建

针对三种曝光区域，ExpoCM 分别构建定制的 PF-ODE 轨迹：

- **过曝区域轨迹**：过曝区域的饱和像素几乎不携带原始场景信息，因此其轨迹仅由干净 HDR 和纯噪声构成，不依赖 LDR 输入：

$$\mathbf{x}_t^o = (1 - \alpha(t)) \mathbf{x}_0 + \sigma_o(t) \boldsymbol{\epsilon}$$

- **欠曝区域轨迹**：欠曝区域虽暗但保留了一定的低频结构，轨迹中注入经低通滤波 $\mathcal{F}_{\mathrm{low}}$ 的 LDR 先验以提供粗略结构引导，同时保留噪声注入强度 $\sigma_u(t)$：

$$\mathbf{x}_t^u = (1 - \alpha(t)) \mathbf{x}_0 + \alpha(t) \lambda_u \mathcal{F}_{\mathrm{low}}(\mathbf{y}_0) + \sigma_u(t) \boldsymbol{\epsilon}$$

- **正常曝光区域轨迹**：正常区域信息可靠，轨迹设计为在内容保真与噪声注入间取得平衡。

#### 空间混合与全局轨迹

将三条区域特定轨迹通过曝光感知权重图进行空间混合，得到全局 PF-ODE 轨迹：

$$\mathbf{x}_t = w_{\mathrm{over}} \odot \mathbf{x}_t^o + w_{\mathrm{under}} \odot \mathbf{x}_t^u + w_{\mathrm{good}} \odot \mathbf{x}_t^g$$

其中 $w_{\mathrm{over}}$、$w_{\mathrm{under}}$、$w_{\mathrm{good}}$ 由上述掩码经归一化处理得到。这一混合机制使得 ExpoCM 成为一个统一的一步式框架——不同于现有曝光感知生成方法依赖解耦的两阶段管线，ExpoCM 在数学上通过 ODE 轨迹的混合同时解决恢复与生成问题。

### 3.3 曝光引导的亮度-色度损失（Exposure-guided Luminance-Chromaticity Loss, ELC）

为克服均匀颜色空间损失对曝光异质性的忽视，ELC 损失在感知均匀的 CIE $L^*a^*b^*$ 空间中施加曝光自适应的监督。

**亮度权重** $w_L$ 根据曝光条件动态调整：在暗区加强亮度监督，在过曝区容忍一定的亮度偏移：

$$w_L = \lambda_L^{(0)} \left( 1 + \kappa_L^{\mathrm{lo}} s_Y w_{\mathrm{under}}^{\alpha} + \kappa_L^{\mathrm{hi}} A_{\mathrm{spec}} w_{\mathrm{over}}^{\alpha} \right)$$

其中 $s_Y$ 为局部亮度显著性，$A_{\mathrm{spec}}$ 为镜面高光注意力，$\alpha$ 控制权重对掩码的敏感度。

**色度权重** $w_C$ 采用类似结构，在过曝和欠曝区域加强色度一致性约束，防止色彩偏移。

完整的 ELC 损失为亮度和色度残差的加权期望：

$$\mathcal{L}_{\mathrm{ELC}} = \mathbb{E} \left[ w_L \cdot \rho(\Delta L^*) \right] + \mathbb{E} \left[ w_C \cdot \rho(\Delta C^*) \right]$$

其中 $\rho(\cdot)$ 为 Charbonnier 惩罚函数，$\Delta L^*$ 和 $\Delta C^*$ 分别为预测 HDR 与真值在 CIE $L^*a^*b^*$ 空间中的亮度和色度差异。

### 3.4 两阶段训练策略

ExpoCM 采用两阶段训练以稳定优化过程：

- **第一阶段**：仅使用一致性训练损失 $\mathcal{L}_{\mathrm{CT}}$（Eq. 4）训练网络，建立稳定的 PF-ODE 轨迹映射能力。
- **第二阶段**：在 $\mathcal{L}_{\mathrm{CT}}$ 基础上引入 ELC 损失 $\mathcal{L}_{\mathrm{ELC}}$ 进行微调，使网络在保持轨迹一致性的同时，获得曝光自适应的亮度和色度重建精度。

网络在随机裁剪的 $256 \times 256$ 图像块上训练，总批次大小为 4，共训练 500,000 次迭代。推理时仅需单步前向传播即可完成 HDR 重建。

## 实验与关键发现

### 4.1 实验设置

ExpoCM 采用两阶段训练策略：第一阶段使用一致性训练损失 $\mathcal{L}_{\mathrm{CT}}$（Eq. 4）优化网络，第二阶段使用提出的曝光引导亮度-色度（ELC）损失 $\mathcal{L}_{\mathrm{ELC}}$ 进行微调。网络在随机裁剪的 256×256 图像块上训练，总批次大小为 4，共迭代 500,000 次。

推理阶段，ExpoCM 仅需**单步**即可完成 HDR 重建。在 512×512 分辨率下，单步推理耗时仅 **0.33 秒**，相比 1000 步 DDPM 的 174.10 秒实现 **超过 400 倍加速**，相比 50 步 DDIM 的 7.85 秒实现 **约 20 倍加速**。

### 4.2 主实验结果

表 1 汇总了 ExpoCM 与现有方法在三个基准数据集上的定量对比。ExpoCM 在所有数据集上均取得最优或次优结果。

**HDR-REAL 数据集**上，ExpoCM 在 PSNR-μ 指标上达到 **28.66 dB**，超过此前最佳的 HDRDiff（27.77 dB）**+0.89 dB**。在感知均匀编码指标 PSNR-PU 和 SSIM-PU 上同样取得最优（30.07 dB / 0.8935），表明重建结果在全亮度范围内均保持高保真度。在感知色差指标 ΔE2000 上，ExpoCM 取得 **4.02** 的最优值，显著优于其他方法。

**HDR-EYE 数据集**上，ExpoCM 以 PSNR-μ **20.75 dB** 超过 DMHDR（20.23 dB）**+0.52 dB**，并在 PSNR-PU 和 SSIM-PU 上保持领先。

**AIM2025 挑战赛数据集**上，ExpoCM 以 PSNR-μ **29.02 dB** 超过 HDRDiff（28.71 dB）**+0.31 dB**，ΔE2000 降至 **3.90**。

定性对比（Figure 3）进一步验证：ExpoCM 在过曝区域（如高光细节恢复）和欠曝区域（如暗部噪声抑制）的重建误差均明显小于 HDRCNN、ExpandNet、Single-HDR、HDRUNet 和 HDRDiff 等方法，误差图呈现更均匀的深色分布。

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons with state-of-the-art single-image HDR reconstruction methods on the AIM2025 and HDR-REAL datasets. For each method, we show the reconstructed HDR image and its corresponding error map, which visualizes the pixel-wise difference from the ground-truth HDR image (darker regions indicate smaller errors)*

### 4.3 消融实验：曝光感知一致性轨迹（EACT）

Table 2 报告了 EACT 设计的消融结果。基线模型使用空间均匀的一致性轨迹（Eq. 3），在 HDR-REAL 上仅取得 PSNR-μ 24.00 dB。引入**双掩码 EACT**（仅区分正常曝光与不良曝光区域）后，PSNR-μ 提升至 28.66 dB，**增益 +4.66 dB**。进一步采用**三掩码 EACT**（完整区分过曝、欠曝和正常区域）后，PSNR-μ 达到 28.66 dB，同时 LPIPS 和 ΔE2000 指标进一步改善，验证了为不同曝光区域定制独立 PF-ODE 轨迹的必要性。

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of the ablation study on our Exposure-Aware Consistency Trajectory (EACT). We compare: (1) Baseline, which uses a uniform, spatially-agnostic trajectory. (2) Two-Mask, a simplified variant that distinguishes only between well-exposed and ill-posed (over- and under-exposed combined) regions. (3) Three-Mask, our full framework using three distinct trajectories for over-, under-, and well-exposed regions*

Figure 4 的视觉消融显示：完整 EACT 在过曝区域（绿色框）和高光区域（红色框）的重建误差最低，基线模型的误差图中则呈现明显的亮色块，表明均匀轨迹无法有效处理空间异质性退化。

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/008_Figure_4.jpg]]
*Figure 4: Visual results of our ablation studies on the proposed exposure-aware consistency trajectory. Our full method exhibits the lowest reconstruction error in both the over-exposed (green box) and highlight (red box) regions*

### 4.4 消融实验：曝光引导亮度-色度损失（ELC）

Table 3 报告了 ELC 损失的消融结果。在 EACT 轨迹基础上，将均匀 CIE L\*a\*b\* 损失替换为完整的 ELC 损失后，HDR-REAL 上的 ΔE2000 从 4.32 降至 **4.02**，AIM2025 上从 4.04 降至 **3.90**，验证了曝光自适应权重对色度偏差的抑制效果。值得注意的是，单独使用 ELC 损失但采用均匀轨迹（w/o EACT）时，PSNR-μ 仅为 24.39 dB，说明 EACT 轨迹与 ELC 损失存在协同效应——前者提供结构级曝光感知，后者提供像素级自适应监督。

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/005_Table_3.jpg]]
*Table 3: Quantitative results of ablation studies about the proposed ELC loss. Baseline: Uniform Trajectory. ‘w/o’ EACT: Uniform Trajectory + Our full ELC loss. ‘w/o’ weighting: EACT Trajectory + Uniform CIE*

Figure 5 的视觉消融对比了各变体的亮度和色度误差图：完整 ELC 损失优化的模型在亮度误差图（左上）和色度误差图（右下）中均呈现最暗的分布，证实其在感知均匀空间中的曝光自适应惩罚有效减轻了过曝区域的高亮度偏差和欠曝区域的色度偏移。

![[assets/figures/papers/paper_list_l2480_https_arxiv_org_abs_2605_02464/figures/007_Figure_5.jpg]]
*Figure 5: Visual comparisons of our ablation studies on the proposed ELC loss. Compared to all variants, the model optimized with our full ELC loss demonstrates the minimal luminance (topleft) and chrominance (bottom-right) error*

### 4.5 关键发现总结

1. **一步式高效生成**：ExpoCM 将 HDR 重建从多步扩散过程压缩为单步推理，在保持甚至超越 SOTA 精度的同时实现 400 倍以上加速，消除了生成式方法在实际部署中的计算瓶颈。
2. **曝光感知轨迹是核心增益来源**：三掩码 EACT 相比均匀轨迹带来 +4.66 dB PSNR-μ 提升，证明空间异质性退化必须通过曝光分区的定制化 PF-ODE 流形来解决，简单的均匀条件轨迹无法胜任。
3. **感知均匀空间的自适应监督**：ELC 损失在 CIE L\*a\*b\* 空间中施加曝光依赖的亮度-色度权重，有效降低了感知色差 ΔE2000，解决了传统损失函数对过曝/欠曝区域惩罚不当的问题。
4. **模块协同**：EACT 与 ELC 的组合使用产生了“1+1>2”的效果——EACT 提供曝光感知的结构生成路径，ELC 提供曝光自适应的细节监督，二者缺一不可。

## 定位与知识库关联

### 问题域与核心瓶颈

单图HDR重建（Single-Image HDR Reconstruction）旨在从单张低动态范围（LDR）图像恢复出高动态范围（HDR）内容。该任务的核心挑战在于**空间异质性退化**：过曝区域因传感器饱和导致高光细节完全丢失，欠曝区域则因光子计数不足而被强噪声淹没，而正常曝光区域仅需相对温和的色调映射。现有方法在面对这种空间变化剧烈的退化模式时，普遍存在以下瓶颈：

- **回归方法**（如HDRCNN、ExpandNet、HDRUNet）直接学习LDR到HDR的确定性映射，但在过曝/欠曝饱和区域缺乏生成能力，无法“创造”被截断的细节，导致重建结果模糊或存在伪影。
- **扩散模型方法**（如HDRDiff、DMHDR）虽具备强生成能力，能够为缺失区域合成合理内容，但其推理需多步采样（DDPM需1000步，DDIM需50步以上），计算开销巨大，且其扩散过程通常假设空间均匀的噪声退化，忽视了曝光条件对局部生成需求的差异性。

ExpoCM的切入点正是这一“效率-质量”矛盾：**如何在单步推理中实现具有空间自适应生成能力的高保真HDR重建？**

### 方法谱系定位

ExpoCM处于**生成式HDR重建**与**一致性模型（Consistency Models, CMs）**的交汇点。下表梳理其与关键基线工作的关系：

| 方法 | 范式 | 核心机制 | 空间自适应 | 推理步数 | 关键局限 |
|------|------|----------|------------|----------|----------|
| **HDRCNN** (Eilertsen et al., ACM TOG 2017) | CNN回归 | 从LDR直接预测HDR | 无 | 单步 | 无法生成过曝区缺失细节 |
| **ExpandNet** (Marnerides et al., Comput. Graph. Forum 2018) | CNN扩展 | 多分支扩展LDR范围 | 无 | 单步 | 对极端曝光鲁棒性差 |
| **Single-HDR** (Liu et al., CVPR 2020) | 相机管线反演 | 反演ISP管线恢复HDR | 无 | 单步 | 依赖相机模型假设 |
| **HDRUNet** (Chen et al., CVPR 2021) | CNN+后处理 | U-Net结合去噪/去量化 | 无 | 单步 | 生成能力有限 |
| **HDRDiff** (Dalal et al., ICIP 2023) | 扩散生成 | 条件扩散模型生成HDR | 无（均匀扩散） | 多步（≥50） | 推理慢，忽视曝光异质性 |
| **DMHDR** (Liu et al., IEEE TCSVT 2025) | 不确定性感知扩散 | 扩散+不确定性引导 | 隐式（不确定性图） | 多步 | 仍受限于扩散采样效率 |
| **ExpoCM** (本文) | 一致性生成 | 曝光感知一致性轨迹+ELC损失 | **显式三区域分区** | **单步** | — |

ExpoCM的方法论创新在于**将一致性模型的单步生成能力与曝光感知的空间自适应轨迹设计相结合**。一致性模型（CMs）本身旨在通过将PF-ODE轨迹上的任意点直接映射回原点来实现少步甚至单步生成，但其标准条件轨迹（Eq. 3）假设空间均匀的退化。ExpoCM通过以下两个关键机制突破这一限制：

1. **曝光感知一致性轨迹（EACT）**：将输入LDR按亮度统计量软分割为过曝、欠曝、正常三个区域，为每个区域定制不同的PF-ODE流形——过曝区从纯噪声生成细节（Eq. 8），欠曝区注入低通滤波的LDR先验并保留噪声（Eq. 9），正常区则可靠传递内容信息（Eq. 10）。三者通过空间混合（Eq. 11）形成全局轨迹，实现“分区生成、统一推理”。

2. **曝光引导亮度-色度损失（ELC Loss）**：在感知均匀的CIE L*a*b*空间中，根据曝光条件自适应加权亮度和色度的监督强度（Eq. 15）——暗区强化亮度监督，过曝区容忍亮度偏移而收紧色度约束，从而避免传统均匀损失在极端曝光区域产生的偏差。

### 与同类工作的本质差异

- **vs. 扩散模型（HDRDiff, DMHDR）**：ExpoCM从原理上不同于扩散模型的迭代去噪范式。扩散模型需要从纯噪声出发逐步采样，而ExpoCM通过一致性训练学习从轨迹上任意点直接跳回干净HDR的映射，在推理时仅需一步前向传播。更重要的是，ExpoCM的轨迹是**空间变化**的，不同曝光区域沿不同的PF-ODE流形演化，而扩散模型通常使用空间均匀的噪声调度。

- **vs. 两阶段生成方法**：部分曝光感知生成方法采用“检测-修复”的两阶段流水线，先定位问题区域再分别处理。ExpoCM通过数学上统一的空间轨迹混合（Eq. 11），将“恢复”与“生成”融合在单个一致性网络中，避免了级联误差和额外的计算开销。

- **vs. 回归方法（HDRUNet等）**：回归方法在过曝/欠曝饱和区域缺乏“想象”能力，只能输出模糊的插值结果。ExpoCM的生成范式使其能够从噪声中合成合理的纹理和结构，这在过曝区域的高光细节恢复中尤为关键。

### 适用边界与局限

基于论文提供的实验证据，ExpoCM的适用边界可归纳如下：

**已验证的有效范围**：
- 在HDR-REAL、HDR-EYE、AIM2025三个公开基准上，单步推理即达到或超越多步扩散模型的指标（PSNR-μ 28.66 dB on HDR-REAL，超越HDRDiff +0.89 dB）。
- 推理速度优势显著：512×512输入下单步仅需0.33秒，相比DDPM（1000步，174.10秒）加速超400倍，相比DDIM（50步，7.85秒）加速超20倍。
- 消融实验证实EACT和ELC Loss各自贡献显著：三掩码EACT相比均匀轨迹基线提升PSNR-μ +4.66 dB；ELC Loss相比均匀CIE L*a*b*损失显著降低ΔE2000。

**需注意的局限与开放问题**（论文中未明确讨论，需手动验证）：
- **极端曝光场景的泛化性**：论文实验集中在三个特定数据集上，对于超出训练分布的超极端过曝/欠曝场景（如近乎全白或全黑的区域），三区域软分割的阈值设定（基于百分位数q_lo, q_hi和τ=0.02）是否仍能提供合理的轨迹混合，尚需进一步验证。
- **高分辨率场景的推理开销**：虽然单步推理已大幅降低计算成本，但一致性网络f_θ基于U-Net架构，在高分辨率（如4K）输入下的内存占用和推理延迟仍需评估。
- **与其他生成范式的对比缺失**：论文未与基于GAN的生成式HDR方法或最新的少步扩散蒸馏方法进行对比，ExpoCM在这些范式下的相对优势尚不明确。
- **训练稳定性与收敛性**：一致性训练对超参数（如噪声调度、离散化步数N）敏感，论文未详细讨论训练过程中的稳定性问题或失败模式。
- **感知质量与保真度的权衡**：ELC Loss在CIE L*a*b*空间中优化，旨在平衡亮度和色度的感知误差，但在某些场景下是否会出现“过度平滑”或“纹理虚构”等生成模型常见问题，论文未提供相关分析。

### 对知识库的贡献定位

ExpoCM为HDR重建领域贡献了一种**高效生成范式**：它证明了通过显式建模曝光异质性并融入一致性训练框架，可以在单步推理中实现空间自适应的生成式重建。其核心洞察——“将曝光分区驱动的空间变化ODE轨迹替代均匀扩散过程”——为其他面临空间异质性退化的图像恢复任务（如去雨、去反射、低光增强）提供了可迁移的方法学思路。同时，ELC Loss中曝光依赖的自适应加权策略也为感知导向的图像恢复损失函数设计提供了参考范例。

## 原文 PDF

![[paperPDFs/CVPR_2026/ExpoCM_Exposure_Aware_One_Step_Generative_Single_Image_HDR_Reconstruction.pdf]]
