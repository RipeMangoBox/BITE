---
title: "Thermal Diffusion Matters: Infrared Spatial-Temporal Video Super-Resolution through Heat Conduction Priors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thermal_Diffusion_Matters_Infrared_Spatial_Temporal_Video_Super_Resolution_through_Heat_Conduction_Priors.pdf
project_link: null
code_link: "https://github.com/ultralytics/ultralytics"
aliases:
- Thermal_Diffusio
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将热传导方程作为物理先验，在频域中通过热扩散核进行帧插值，并通过温度场建模损失强制执行物理一致性。
primary_logic: 利用红外像素强度与温度辐射之间的直接映射关系，将热传导方程嵌入到深度网络中以指导时空超分辨率，实现物理一致且时间连续的帧生成。
claims:
- 提出TDIM，将时序特征序列视为一维热场并进行频域扩散插值。
- 提出TSSM，通过可学习频谱滤波和选择性状态空间建模细化时空表示。
- 引入温度场建模损失以强制执行热传导方程。
- IRVAL 上 PSNR = 21.37
---

# Thermal Diffusion Matters: Infrared Spatial-Temporal Video Super-Resolution through Heat Conduction Priors

> [!tip] 核心洞察
> 利用红外像素强度与温度辐射之间的直接映射关系，将热传导方程嵌入到深度网络中以指导时空超分辨率，实现物理一致且时间连续的帧生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 热扩散至关重要：基于热传导先验的红外时空视频超分辨率 |
| 英文题名 | Thermal Diffusion Matters: Infrared Spatial-Temporal Video Super-Resolution through Heat Conduction Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhou_Thermal_Diffusion_Matters_Infrared_Spatial-Temporal_Video_Super-Resolution_through_Heat_Conduction_CVPR_2026_paper.html) · [Code](https://github.com/ultralytics/ultralytics) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | THERIS |
| Dataset | IRVAL, LLVIP, SGMP |

> [!tip] 效果简介
> - IRVAL 上，PSNR 21.37；SSIM 0.7872；MUSIQ 55.59。
> - LLVIP 上，PSNR 28.05；SSIM 0.9177。
> - SGMP 上，PSNR 37.83。

## 概要

红外视频时空超分辨率（Infrared Spatial-Temporal Video Super-Resolution, STVSR）面临一个双重瓶颈：红外成像系统同时受限于低空间分辨率和低帧率，而现有方法（如基于光流或可变形卷积的插值方案）缺乏热物理一致性约束，导致生成的时空细节在物理上不合理。本文的核心洞察在于：红外像素强度与温度辐射之间存在直接映射关系，因此可以将热传导方程作为物理先验嵌入深度网络，从而指导时空超分辨率过程，实现物理一致且时间连续的帧生成。

基于上述洞察，本文提出 **THERIS**（THERmal-physics inspired framework for Infrared spatial-temporal video Super-resolution），一个统一的热物理驱动框架。其核心因果调节机制包含三个关键组件：（1）**热扩散插值模块（TDIM）**，将时序特征序列视为一维热场，在频域中通过可学习的热扩散核进行帧插值，替代传统的光流或可变形卷积方案；（2）**热感知状态空间模块（TSSM）**，通过可学习频谱滤波和多种扫描顺序的选择性状态空间建模来细化时空表示；（3）**温度场建模损失（TFM Loss）**，基于二维热传导方程强制执行物理一致性约束，替代传统的 L1/L2 重建损失。

在实验验证方面，本文构建了 **IRVAL** 数据集，包含 108,512 帧 512×512 分辨率的高质量红外视频帧。在该基准上，THERIS 取得了 PSNR 21.37、SSIM 0.7872 的 SOTA 性能。消融实验表明，去除频谱掩码导致 PSNR 下降至 19.86，去除时间嵌入降至 20.54，省略 TFM Loss 降至 20.81，验证了各组件的因果贡献。跨数据集泛化实验（LLVIP 和 SGMP）以及下游目标检测任务（mAP@0.5:0.95 达 50.7）进一步证实了方法的有效性和物理先验的迁移价值。

在方法谱系上，THERIS 区别于现有的 STVSR 方法（如 **ZoomingSlowMo**（Xiang et al., CVPR 2020）、**TMNet**（Xu et al., CVPR 2021）、**VideoINR**（Chen et al., CVPR 2022）、**MoTIF**（Chen et al., CVPR 2023）和 **BF-STVSR**（Kim et al., CVPR 2025）），首次将热传导偏微分方程引入神经网络架构设计与损失函数，为红外视频增强提供了物理可解释的新范式。

### 红外视频超分辨率的双重瓶颈

红外成像在安防监控、自动驾驶和夜间感知等任务中具有不可替代的优势，但其面临**空间分辨率低**与**帧率低**的双重瓶颈。这两个问题并非孤立存在：空间细节的缺失会加剧时间维度的模糊，而低帧率导致的运动不连续又使得空间重建缺乏可靠的时序参考。因此，将空间超分辨率（Spatial SR）与时间帧插值（Temporal Frame Interpolation）联合建模，即**时空视频超分辨率（Spatial-Temporal Video Super-Resolution, STVSR）**，成为红外视频增强的核心挑战。

### 现有方法的物理盲区

当前主流的STVSR方法，如**ZoomingSlowMo**（Xiang et al., CVPR 2020）、**TMNet**（Xu et al., CVPR 2021）、**VideoINR**（Chen et al., CVPR 2022）、**MoTIF**（Chen et al., CVPR 2023）和**BF-STVSR**（Kim et al., CVPR 2025），在帧插值环节普遍依赖**光流估计**或**可变形卷积**来建模运动。这些方法在可见光视频上取得了显著进展，但迁移到红外场景时暴露出一个根本性缺陷：它们完全忽略了红外成像的**物理本质**。

红外图像中每个像素的强度值直接反映场景的温度辐射，这意味着红外视频的时空演化本质上受**热传导动力学**支配。现有数据驱动方法缺乏任何热物理一致性约束，其生成的中间帧在像素强度上可能满足统计意义上的相似性，但在物理上却可能违背温度场的扩散规律——例如，一个热源物体的降温过程在生成的帧序列中可能出现不符合指数衰减的伪影。这种“物理不合理性”在时序剖面可视化中尤为明显（见Figure 1），现有方法生成的时空剖面往往呈现不连续或违背扩散趋势的突变。

### 热传导先验的引入动机

本文的核心动机源于一个关键观察：**红外像素强度与温度辐射之间存在直接映射关系**。这一特性使得将热传导方程（Heat Conduction Equation）作为物理先验嵌入深度网络成为可能。具体而言，一维热传导方程：

$$\frac{\partial u(x,t)}{\partial t} = D \frac{\partial^2 u(x,t)}{\partial x^2}, \quad u(x,0) = f(x)$$

描述了一个温度场在空间中的扩散演化，其在频域中具有精确的指数衰减解形式。这意味着，如果我们将红外视频的时序特征序列视为一个一维热场，那么中间时刻的特征可以通过**频域热扩散核**以物理一致的方式进行插值，而非依赖数据驱动的运动估计。

### 本文的应对策略

基于上述动机，本文提出**THERIS**（THERmal-physics inspired framework for Infrared spatial-temporal video Super-resolution），一个统一的热物理驱动红外STVSR框架。其设计围绕三个核心原则：

1. **物理驱动的帧插值**：用频域热扩散建模取代光流或可变形卷积，通过热扩散插值模块（TDIM）在时间维度上进行物理一致的中间帧合成。
2. **热感知的时空细化**：设计热感知状态空间模块（TSSM），将热扩散过程的时间嵌入传播至选择性状态空间扫描，实现时空特征的协同细化。
3. **物理约束的损失函数**：引入温度场建模损失（TFM Loss），强制执行热传导方程的残差约束，使生成的红外视频在像素强度演化上严格遵循热扩散动力学。

通过将热传导方程从物理定律转化为网络设计中的结构化先验，THERIS旨在弥合现有STVSR方法在红外场景中的“物理-数据”鸿沟，实现时序连续且物理一致的红外视频重建。

## 核心方法与创新机理

### 1. 问题瓶颈与因果调控

红外视频时空超分辨率（STVSR）面临双重瓶颈：空间分辨率低与帧率不足并存，且现有方法缺乏热物理一致性约束，导致生成的时空细节在物理上不合理。THERIS的核心调控逻辑是：将红外像素强度与温度辐射之间的直接映射关系转化为可操作的物理先验，通过**热传导方程的频域解**指导帧插值，并以**温度场建模损失**强制执行物理一致性。

### 2. 关键创新点：Changed Slots 深度解析

相较于主流STVSR方法，THERIS在三个核心模块上实现了范式级替换：

#### 2.1 帧插值：从光流/可变形卷积到热扩散频域建模（TDIM）

现有方法（如 **ZoomingSlowMo** (Xiang et al., CVPR 2020)、**TMNet** (Xu et al., CVPR 2021)、**MoTIF** (Chen et al., CVPR 2023)）普遍依赖光流或可变形卷积进行帧间运动补偿与插值。这种方式在红外场景中面临根本性困难：红外纹理弱、对比度低，导致光流估计不可靠。

THERIS提出的**热扩散插值模块（TDIM）**完全绕开了运动估计。其核心机制是：
- 将时序特征序列视为一维热场，沿时间轴进行傅里叶变换
- 在频域中应用可学习的热扩散核 $W(n, e_i) = \exp(-\kappa(n; e_i) \omega_n^2 \Delta t)$，其中 $\omega_n = \frac{n\pi}{k+1}$，$\kappa$ 通过Softplus确保非负衰减
- 该扩散核直接建模热传导方程在频域的精确解 $\tilde{u}(\omega, t) = \tilde{f}(\omega) \exp(-D\omega^2 t)$，即频率依赖的指数衰减行为

这一设计的物理直觉是：热扩散过程中，高频温度波动衰减更快，低频趋势保留更久——这与视频帧间变化的时序平滑性高度一致。

#### 2.2 特征细化：从残差块/Transformer到热感知状态空间模块（TSSM）

传统STVSR方法使用残差块或Transformer进行特征细化，缺乏对红外时序特性的针对性建模。THERIS的**热感知状态空间模块（TSSM）**引入三重创新：

1. **可学习频谱滤波**：通过FFT-可学习频谱掩码-IFFT链路，选择性增强被抑制的频率分量
2. **多扫描顺序的状态空间建模**：交错排列空间优先、时间优先和Hilbert曲线扫描顺序的Selective State Space Block（分别对应SMB、TMB和HMB），从多维度捕获时空依赖
3. **热提示条件化**：将TDIM传播的时间嵌入注入状态空间模型，调制状态到输出的映射矩阵：$y_t = (\mathbf{C} + \mathbf{T})h_t + \mathbf{D}x_t$

这一设计使TSSM能够感知热扩散的时间结构，而非仅进行无差别的时空特征聚合。

#### 2.3 训练损失：从L1/L2重建损失到物理约束损失

传统方法仅使用L1或L2重建损失，无法保证生成结果的物理合理性。THERIS引入**温度场建模损失（TFM Loss）**，基于二维热传导方程 $\frac{\partial u(x,y,t)}{\partial t} = D\nabla^2 u(x,y,t)$ 构建物理约束残差：

$$r(x,y,t) = \frac{\tilde{I}_{t+1}^H - \tilde{I}_{t-1}^H}{2\Delta t} - D\nabla^2 u(x,y,t)$$

该损失强制预测帧序列满足热传导方程的时空演化规律，从而促进时序一致性和空间稳定性。

### 3. 消融证据：创新组件的因果贡献

消融实验（Table 3）量化验证了各创新组件的独立贡献（IRVAL基准，PSNR指标）：

- **去除频谱掩码**：PSNR从21.37降至19.86（-1.51），表明频域自适应滤波对红外特征增强至关重要
- **去除时间嵌入**：PSNR降至20.54（-0.83），验证了热扩散时间信息对状态空间建模的指导作用
- **省略TFM Loss**：PSNR降至20.81（-0.56），证明物理约束损失对生成质量的额外增益

值得注意的是，仅使用TDIM即可从两帧低分辨率输入生成高质量的中间时刻重建帧（Figure 5），表明热扩散插值本身已具备强大的时序生成能力。

### 4. 方法谱系与知识库定位

THERIS在STVSR方法谱系中占据独特位置：

- **相对于运动补偿范式**（ZoomingSlowMo, TMNet, MoTIF, BF-STVSR）：以物理驱动的频域扩散替代数据驱动的运动估计，避免了红外场景下光流不可靠的固有问题
- **相对于隐式神经表示范式**（VideoINR, Chen et al., CVPR 2022）：以显式热传导方程提供可解释的时序演化约束，而非纯粹的数据拟合
- **相对于通用状态空间模型**：通过热提示条件化和多扫描顺序设计，将通用Mamba架构适配到红外视频的物理特性

### 5. 局限与开放问题

当前创新存在以下待验证边界：
- 热扩散先验对快速相机运动或极端温度变化的鲁棒性尚未明确讨论
- 热扩散系数 $\kappa$ 的学习是否可基于场景材料属性自动确定，仍为开放问题
- 该物理先验框架是否适用于可见光等其他成像模态，需进一步验证

THERIS 是一个统一的热物理驱动框架，旨在解决红外视频时空超分辨率问题。其核心设计目标是从低帧率、低空间分辨率的红外视频中重建出高帧率、高空间分辨率且物理一致的视频序列。

### 问题建模与输入输出

给定 $k+1$ 帧低分辨率输入帧 $\mathcal{T}^L = \{I_{2t-1}^L\}_{t=1}^{k+1}$（尺寸为 $H \times W \times C$），THERIS 的目标是生成 $2k+1$ 帧高分辨率输出帧 $\mathcal{T}^H = \{I_t^H\}_{t=1}^{2k+1}$（尺寸为 $sH \times sW \times C$），其中 $s$ 为空间上采样倍数。这一过程同时实现了时间维度的帧率倍增和空间维度的分辨率提升。

### Pipeline 架构

整个框架由四个核心模块串联构成，数据流沿“编码—插值—细化—重建”的路径依次传递：

1. **浅层特征编码器（Shallow Feature Encoder）**：对每一帧输入的低分辨率红外图像独立提取嵌入特征图，将原始像素映射到高维特征空间。

2. **热扩散插值模块（Thermal Diffusion Interpolation Module, TDIM）**：将 $k+1$ 个输入时间步的特征序列视为一维热场，在频域中通过热扩散核进行时间轴上的扩散插值，生成 $2k+1$ 个时间对齐的特征图。该模块是框架实现物理感知帧插值的核心，其理论基础源于一维热传导方程在频域中的精确解——频率依赖的指数衰减行为。

3. **热感知状态空间模块（Thermo-Aware State Space Module, TSSM）**：对插值后的特征序列进行时空表示细化。每个 TSSM 首先通过快速傅里叶变换（FFT）将特征转换到频域，应用可学习的频谱掩码选择性增强被抑制的频率分量，再通过逆快速傅里叶变换（IFFT）重建空间表示；随后，多个选择性状态空间块（Selective State Space Blocks）以不同的扫描顺序（空间优先、时间优先、局部希尔伯特扫描）对特征进行序列建模，且状态更新受 TDIM 传播的时间嵌入条件控制。

4. **重建解码器（Reconstruction Decoder）**：将细化后的特征图上采样并进一步精炼，最终输出 $2k+1$ 帧高分辨率红外视频帧。

### 物理一致性约束

除上述模块外，框架引入了**温度场建模损失（Temperature Field Modeling Loss, TFM Loss）**作为训练约束。该损失基于二维热传导方程的离散残差计算，强制生成的高分辨率帧序列在时间演化和空间分布上满足热物理规律，从而提升时序连贯性和空间稳定性。这一损失与 TDIM 的热扩散插值形成闭环——前者在特征层面嵌入物理先验，后者在像素层面强制执行物理一致性。

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our proposed THERIS framework*

### 3.1 整体框架与问题定义

THERIS框架的目标是：给定 $k+1$ 帧低分辨率（LR）红外视频帧，生成 $2k+1$ 帧高分辨率（HR）输出。框架由四个核心模块串联构成：浅层特征编码器（Shallow Feature Encoder）、热扩散插值模块（TDIM）、热感知状态空间模块（TSSM）和重建解码器（Reconstruction Decoder）。其中，TDIM和TSSM是承载热物理先验的关键创新点。

### 3.2 热扩散插值模块（TDIM）

**物理动机。** 红外图像的像素强度与目标物体的温度辐射直接相关，因此红外视频中相邻帧之间的时序演化本质上遵循热传导过程。TDIM将时序特征序列建模为一维热场，利用热传导方程在频域中的精确解来实现物理一致的帧插值。

**一维热传导方程。** 基础控制方程为：

$$\frac{\partial u(x,t)}{\partial t} = D \frac{\partial^2 u(x,t)}{\partial x^2}, \quad u(x,0) = f(x)$$

其中 $u(x,t)$ 表示位置 $x$ 在时刻 $t$ 的温度，$D$ 为热扩散系数，$f(x)$ 为初始温度分布。

**频域解耦。** 对上述方程进行空间傅里叶变换后，得到解耦的常微分方程：

$$\frac{d}{dt} \tilde{u}(\omega,t) = -D\omega^2 \tilde{u}(\omega,t)$$

该ODE的精确解表现为频率依赖的指数衰减：

$$\tilde{u}(\omega,t) = \tilde{f}(\omega) \exp(-D\omega^2 t)$$

这一形式揭示了热扩散的核心机制：高频分量（对应空间细节）比低频分量衰减更快，扩散速率由 $D\omega^2$ 控制。

**可学习热扩散核。** TDIM在实现中将上述物理过程转化为可学习的频域扩散核。具体而言，模块首先沿时间轴对输入特征序列执行离散余弦变换（DCT），将 $k+1$ 个输入时间步的特征映射到频域。然后，通过一个参数化的扩散核对每个频率分量进行衰减调制：

$$W(n, e_i) = \exp(-\kappa(n; e_i) \omega_n^2 \Delta t), \quad \omega_n = \frac{n\pi}{k+1}$$

其中 $n$ 为频率索引，$\Delta t$ 为时间步长，$\kappa(n; e_i)$ 是通过Softplus激活函数保证非负的可学习扩散系数，$e_i$ 为时间嵌入。该扩散核使模型能够在保留热传导指数衰减形式的同时，自适应地学习不同场景下的最优扩散速率。

**逆变换重建。** 经过频域扩散调制后，TDIM通过逆DCT将特征重建回时域，生成 $2k+1$ 个时间对齐的特征图。逆变换基函数为：

$$\mathrm{CT}_{\mathrm{out}}[n,t] = \sqrt{\frac{2}{k+1}} \cos\left(\frac{n\pi}{k+1}t\right)$$

最终插值特征由下式给出：

$$\tilde{F}_{\hat{n}} = \sum_{t=1}^{2k+1} F_{\hat{n}} W(n, e_i) \mathrm{CT}_{\mathrm{out}}[n,t]$$

### 3.3 热感知状态空间模块（TSSM）

**设计动机。** TDIM输出的插值特征虽然具有时序连续性，但仍需进一步细化以增强空间细节和跨帧一致性。TSSM通过可学习频谱滤波和选择性状态空间建模来实现这一目标，同时引入来自TDIM的时间嵌入作为热提示（thermal prompt）来调节状态更新。

**频谱滤波。** 每个TSSM首先通过快速傅里叶变换（FFT）将特征变换到频域，应用可学习的频谱掩码（spectral mask）选择性地增强被抑制的频率分量，再通过逆FFT重建空间表示。这一设计直接针对热扩散过程中高频信息衰减的问题。

**选择性状态空间扫描。** TSSM内部集成了多个选择性状态空间块（Selective State Space Block），采用三种不同的扫描顺序以捕获多维依赖关系：
- **空间优先扫描（Space Mamba Block, SMB）**：沿空间维度展开，强化单帧内的空间结构。
- **时间优先扫描（Time Mamba Block, TMB）**：沿时间轴展开，建模跨帧时序动态。
- **局部Hilbert扫描（Local Hilbert Scan）**：通过Hilbert曲线保持局部空间连续性，同时引入全局上下文。

**热提示调制。** TSSM中的状态空间模型遵循Mamba的离散化形式：

$$h_t = \bar{\mathbf{A}} h_{t-1} + \bar{\mathbf{B}} x_t, \quad y_t = \mathbf{C} h_t + \mathbf{D} x_t$$

关键创新在于，TDIM生成的时间嵌入被用于调制状态到输出的映射矩阵，即 $y_t = (\mathbf{C} + \mathbf{T}) h_t + \mathbf{D} x_t$，其中 $\mathbf{T}$ 为热提示。这使得状态空间模型的输出显式地依赖于热扩散过程的时间结构，从而将物理先验贯穿整个特征细化流程。

### 3.4 温度场建模损失（TFM Loss）

**物理约束形式。** 为进一步强制执行热传导方程，论文将一维热传导推广到二维空间：

$$\frac{\partial u(x,y,t)}{\partial t} = D \nabla^2 u(x,y,t)$$

其中 $\nabla^2$ 为二维拉普拉斯算子。基于此，定义物理约束残差：

$$r(x,y,t) = \frac{\tilde{I}_{t+1}^H - \tilde{I}_{t-1}^H}{2\Delta t} - D \nabla^2 u(x,y,t)$$

该残差通过中心差分近似时间导数，并与空间扩散项比较，衡量预测帧对热传导方程的偏离程度。温度场建模损失即基于该残差构建，与重建损失联合优化，从而在训练中显式地施加热物理一致性约束。消融实验表明，移除TFM Loss会导致PSNR从21.37下降至20.81（Table 3），验证了物理约束对性能的实质性贡献。

## 实验与关键发现

### 主实验结果

**THERIS** 在三个红外视频数据集上全面验证了其时空超分辨率性能，涵盖 **IRVAL**、**LLVIP** 和 **SGMP** 三个基准。在 IRVAL 测试集上，THERIS 在所有评估指标上均取得最优结果：PSNR 达到 **21.37**，SSIM 达到 **0.7872**，无参考质量指标 MUSIQ 达到 **55.59**，时序一致性指标 DOVER 达到 **0.2990**（Table 1）。与现有 STVSR 方法相比，THERIS 在重建精度和时序连贯性两个维度上均展现出显著优势。

跨数据集泛化实验进一步验证了方法的鲁棒性。在 **LLVIP** 数据集上，THERIS 取得了 **28.05** 的 PSNR 和 **0.9177** 的 SSIM；在 **SGMP** 数据集上，PSNR 和 SSIM 分别达到 **37.83** 和 **0.9517**（Table 2）。值得注意的是，LLVIP 数据集包含大量低光照场景，而 SGMP 数据集涉及不同的红外传感器特性，THERIS 在这两个域偏移场景下仍保持最优性能，表明热传导先验并非对特定数据分布的过拟合，而是捕捉了红外成像的底层物理规律。

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/006_Table_2.jpg]]
*Table 2: Comparison on LLVIP and SGMP test sets. Our method achieves SOTA scores with respect to all metrics*

### 计算效率分析

在性能与计算效率的权衡上，THERIS 展现出明显的帕累托优势。在 IRVAL 数据集 ×4 空间超分和 ×2 时序超分的任务设定下，THERIS 在 PSNR-GFLOPs 散点图中处于右上角最优区域（Figure 4），在保持最高重建质量的同时，计算开销显著低于多数对比方法。这一效率优势源于两个设计选择：（1）TDIM 在频域进行扩散插值，避免了显式光流估计或可变形卷积的高昂计算成本；（2）TSSM 基于状态空间模型的线性复杂度特性，相比 Transformer 结构的二次复杂度具有天然效率优势。

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/005_Figure_4.jpg]]
*Figure 4: Performance and computational efficiency comparison on IRVAL dataset for ×4 spatial and ×2 temporal SR tasks*

### 消融实验

消融实验系统评估了 THERIS 三个核心组件的独立贡献（Table 3，IRVAL 基准）：

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/010_Table_3.jpg]]
*Table 3: Ablation study on components of our proposed method on the IRVAL benchmark*

- **频谱掩码（Spectral Mask）**：移除 TSSM 中的可学习频谱掩码后，PSNR 从 21.37 大幅下降至 **19.86**（−1.51），降幅最大。这表明频域自适应滤波对红外特征增强至关重要——红外图像的高频细节天然较弱，频谱掩码通过学习选择性放大被抑制的频率分量，直接补偿了红外成像的物理局限。

- **时间嵌入（Time Embeddings）**：移除从 TDIM 传播至 TSSM 的时间嵌入后，PSNR 降至 **20.54**（−0.83）。该结果验证了热扩散时间信息对状态空间模块的引导作用：TSSM 的状态更新依赖于时间嵌入来对齐视频序列的时间结构，缺少这一条件信号会导致时空特征细化的失准。

- **温度场建模损失（TFM Loss）**：省略基于热传导方程的物理约束损失后，PSNR 降至 **20.81**（−0.56）。TFM Loss 的贡献虽小于前两者，但其作用机制不同——它并非直接提升单帧重建精度，而是通过强制相邻帧服从热扩散方程来增强时序一致性。这一结论与 DOVER 指标的提升相呼应。

### 下游任务验证

为评估超分结果对实际应用的增益，论文在 LLVIP 数据集上进行了目标检测实验。将不同 STVSR 方法生成的超分帧输入 YOLOv8 检测器，THERIS 取得了最高的 **mAP@0.5:0.95 = 50.7**（Table 4）。可视化对比（Figure 6）显示，THERIS 重建的帧在目标边界清晰度和低对比度区域细节保留方面优于其他方法，使得检测器能够更准确地定位和识别行人目标。这一结果说明，物理一致性约束不仅提升了感知质量指标，也转化为下游任务的实际性能增益。

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/008_Table_4.jpg]]
*Table 4: Comparison of detection results on the LLVIP dataset*

![[assets/figures/papers/paper_list_l2609_https_openaccess_thecvf_com_content_CVPR2026_html_Zhou_Thermal_Diffusion/figures/009_Figure_6.jpg]]
*Figure 6: Visual comparison of object detection performance on super-resolved frames produced by STVSR methods*

### 失败模式与局限性

尽管 THERIS 在定量和定性评估中均表现优异，论文未明确讨论模型在特定场景下的失效模式。基于方法设计可推断以下潜在局限，需在实际部署中手动验证：

1. **快速相机运动场景**：TDIM 假设时间维度上的特征演化遵循热扩散方程，该假设在帧间运动剧烈时可能不再成立。当相机快速平移或旋转时，像素强度的变化主要由场景内容位移驱动，而非热辐射的物理扩散过程，频域插值可能产生运动模糊或伪影。

2. **极端温度变化**：温度场建模损失基于热传导方程的线性假设，在温度梯度极大（如爆炸、火灾场景）或材料热属性剧烈变化时，线性扩散模型可能无法准确描述实际的热动力学过程，导致物理约束与真实观测失配。

3. **数据集覆盖偏差**：IRVAL 数据集虽包含 108,512 帧 512×512 分辨率的红外视频，规模可观，但可能未充分覆盖所有红外成像场景（如不同波段、不同环境温度范围、不同目标类型），模型的泛化边界仍需在更多样化的红外数据上进一步界定。

### 开放问题

1. 热扩散先验是否适用于其他成像模态（如近红外、太赫兹成像）？不同波段的辐射传输机制差异可能影响物理模型的有效性。
2. 如何基于场景材料属性自动确定最佳的热扩散系数 $D$，而非依赖经验设定或可学习参数？
3. 模型在实时嵌入式红外系统（如无人机、安防摄像头）上的部署效率如何？当前 GFLOPs 评估未考虑内存带宽和硬件加速器适配等实际约束。

## 定位与知识库关联

### 红外STVSR的问题独特性

红外时空视频超分辨率（Infrared STVSR）面临可见光STVSR所不具备的双重挑战：红外传感器本身受限于低空间分辨率与低帧率，且红外像素强度直接由温度辐射决定，其时空演化本质上受热传导方程支配。现有STVSR方法——无论是基于光流或可变形卷积的帧插值方案（如 **ZoomingSlowMo** (Xiang et al., CVPR 2020)、**TMNet** (Xu et al., CVPR 2021)、**BF-STVSR** (Kim et al., CVPR 2025)），还是基于隐式神经表示的连续帧生成方法（如 **VideoINR** (Chen et al., CVPR 2022)、**MoTIF** (Chen et al., CVPR 2023)）——均缺乏热物理一致性约束，导致生成的时空细节在物理上不可靠。本文的核心瓶颈识别即在于此：现有方法将红外视频视为通用信号，忽略了其背后的热力学生成机制。

### 方法谱系中的定位

THERIS 在方法谱系中占据一个独特的位置——它将物理先验驱动的生成范式引入红外STVSR，而非单纯依赖数据驱动的插值或表示学习。具体而言，其与现有工作的关系可从三个维度定位：

**帧插值范式的转变。** 传统STVSR方法（ZoomingSlowMo、TMNet等）依赖光流估计或可变形卷积来建模帧间运动，进而合成中间帧。这类方法在红外场景中面临两个根本性困难：一是低纹理红外图像使得光流估计不可靠；二是运动插值无法捕捉温度场固有的扩散性演化。THERIS 的 TDIM 模块完全绕开了显式运动估计，转而将时序特征序列视为一维热场，在频域中通过热扩散核进行插值——这一思路源自热传导方程在频域的精确解 $\tilde{u}(\omega, t) = \tilde{f}(\omega) \exp(-D \omega^2 t)$，其核心机制是频率依赖的指数衰减，而非运动补偿。

**时序建模机制的演进。** VideoINR 和 MoTIF 代表了基于隐式神经表示的连续帧生成路线，它们通过学习时间坐标到像素值的连续映射来获得任意时刻的帧。THERIS 的 TSSM 模块则采用了不同的技术路线——选择性状态空间模型（Mamba），其理论复杂度为 $\mathcal{O}(N)$，通过线性递归操作捕获长程交互。TSSM 与通用 Mamba 的关键区别在于其“热感知”设计：时间嵌入从 TDIM 传播至状态空间块，调制状态到输出的映射矩阵 $y_t = (\mathbf{C} + \mathbf{T}) h_t + \mathbf{D} x_t$，使状态更新与视频序列的热力学时间结构对齐。此外，TSSM 内部交织了多种扫描顺序（空间优先、时间优先、Hilbert 曲线局部扫描），分别对应 Space Mamba Block、Time Mamba Block 和 Local Mamba Block，以从不同维度捕获时空依赖。

**损失函数的物理约束引入。** 传统STVSR方法仅使用 L1 或 L2 重建损失，缺乏对生成帧之间物理一致性的约束。THERIS 引入的温度场建模损失（TFM Loss）基于二维热传导方程 $\frac{\partial u(x,y,t)}{\partial t} = D \nabla^2 u(x,y,t)$，通过中心差分近似时间导数 $\frac{\partial u}{\partial t} \approx \frac{\tilde{I}_{t+1}^H - \tilde{I}_{t-1}^H}{2\Delta t}$，计算物理约束残差 $r(x,y,t)$，强制生成帧序列满足热传导规律。这一设计将物理先验从网络结构层面延伸到了优化目标层面。

### 适用边界与局限

尽管 THERIS 在 IRVAL、LLVIP 和 SGMP 三个红外数据集上均取得了 SOTA 性能（Table 1、Table 2），其适用边界仍存在若干可辨识的局限：

1. **运动场景鲁棒性未验证。** 论文未明确讨论模型对快速相机运动或场景中物体高速移动的鲁棒性。热扩散先验假设像素强度的时间演化主要由热传导驱动，但在剧烈运动场景中，像素值的帧间变化可能更多来自几何位移而非热扩散，此时频域扩散插值的有效性可能下降。这一局限需要手动验证。

2. **极端温度变化的泛化能力未知。** 热传导方程中的扩散系数 $D$ 在 TDIM 中通过可学习参数 $\kappa(n; e_i)$ 实现，经 Softplus 确保非负衰减，但该参数是从数据中隐式学习的，而非基于材料热属性显式设定。当测试场景的物体材质、环境温度与训练分布显著不同时，学习到的扩散特性是否仍然适用，论文未提供跨温度域的泛化实验。

3. **数据集覆盖范围。** IRVAL 数据集虽包含 108,512 帧 512×512 分辨率的红外视频，规模在红外STVSR领域首屈一指，但可能无法涵盖所有红外成像场景（如长波红外与中波红外的差异、不同探测器的噪声特性等）。LLVIP 和 SGMP 上的跨数据集实验（Table 2）提供了初步的泛化证据，但两个数据集的场景类型仍有限。

### 开放问题

1. **跨模态可迁移性。** 热扩散先验是否适用于其他成像模态？可见光图像的像素强度与温度之间不存在红外成像中那样直接的物理映射关系，但某些医学成像模态（如热成像、光声成像）可能共享类似的热力学生成机制。这一方向的探索尚未展开。

2. **扩散系数的物理可解释性。** 当前 TDIM 中的热扩散核 $W(n, e_i) = \exp(-\kappa(n; e_i) \omega_n^2 \Delta t)$ 通过神经网络隐式学习 $\kappa$，缺乏与材料热扩散率的直接对应。如何基于场景中的物体材质信息自动确定物理上有意义的热扩散系数，是提升模型可解释性和泛化能力的关键开放问题。

3. **实时部署效率。** 尽管 Figure 4 展示了 THERIS 在性能-效率权衡上的优势，但 TSSM 中 FFT/IFFT 操作和多扫描顺序的 Mamba 块引入了额外的计算开销。模型在资源受限的嵌入式红外系统（如无人机载红外、车载夜视）上的部署效率尚未评估，这对其实际应用至关重要。

4. **物理先验与数据驱动的理论平衡。** TFM Loss 强制输出帧满足热传导方程，但该方程本身是对真实热力学过程的简化（忽略了对流、辐射等效应）。在何种条件下物理约束会过度正则化、反而损害重建质量，缺乏理论分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/Thermal_Diffusion_Matters_Infrared_Spatial_Temporal_Video_Super_Resolution_through_Heat_Conduction_Priors.pdf]]
