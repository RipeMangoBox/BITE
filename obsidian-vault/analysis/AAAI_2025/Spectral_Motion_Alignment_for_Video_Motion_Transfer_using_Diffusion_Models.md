---
title: "Spectral Motion Alignment for Video Motion Transfer using Diffusion Models"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- SMAS
- SMAVMTUDM
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "在频谱域对齐运动向量：通过1D小波变换对齐多尺度全局运动动态（捕获长程依赖），并通过2D FFT对齐幅度与相位谱，同时通过加权函数优先考虑低空间频率成分（抑制高频伪影）。"
primary_logic: "视频运动动态可以有效地由其固有频率成分表示；通过在频谱域对齐运动表示，可以同时捕获全局多尺度运动模式并过滤掉与运动无关的噪声伪影，从而显著提升运动迁移的准确性和一致性。"
claims:
- "在运动向量估计中，高频成分往往对应与运动无关的空间伪影（如突发光照变化、背景不一致），而SMA通过低频优先的局部光谱对齐有效滤除了这些伪影。"
- "1D小波全局对齐损失使模型能够同时学习多尺度的时间运动模式，减轻了仅依靠帧间残差带来的全局运动理解不足（如运动反向）。"
- "在多种视频运动迁移框架（VMC/MotionDirector/Tune-A-Video/ControlVideo）上集成SMA均带来一致的性能提升，涵盖文本对齐、时间一致性、编辑准确性等指标。"
- "VMC (Cascaded VDM) 消融基准 上 Text-Align (CLIP) = VMC + SMA (ℓ_global + ℓ_local)"
---

# Spectral Motion Alignment for Video Motion Transfer using Diffusion Models

> [!tip] 核心洞察
> 视频运动动态可以有效地由其固有频率成分表示；通过在频谱域对齐运动表示，可以同时捕获全局多尺度运动模式并过滤掉与运动无关的噪声伪影，从而显著提升运动迁移的准确性和一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于扩散模型的视频运动迁移：光谱运动对齐 |
| 英文题名 | Spectral Motion Alignment for Video Motion Transfer using Diffusion Models |
| 会议/期刊 | AAAI 2025 |
| Links | [paper](https://arxiv.org/abs/2403.15249) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Spectral Motion Alignment (SMA) |
| Dataset | VMC (Cascaded VDM) 消融基准, MotionDirector (T2V), Tune-A-Video / ControlVideo (T2I-based) |

> [!tip] 效果简介
> - VMC (Cascaded VDM) 消融基准 上，Text-Align (CLIP) 为 VMC + SMA (ℓ_global + ℓ_local)，对比 VMC (仅像素对齐)，变化 +0.026。
> - VMC (Cascaded VDM) 消融基准 上，Frame-Con (CLIP) 为 VMC + SMA (ℓ_global + ℓ_local)，对比 VMC (仅像素对齐)，变化 +0.016。
> - MotionDirector (T2V) 上，Motion-Acc (用户研究 1-5分) 为 MotionDirector + SMA，对比 MotionDirector (原始)，变化 显著提升 (见表1详细数值)。

## 概要

**核心问题**：现有视频运动迁移方法通常在像素空间或特征空间通过帧间残差表示运动，但这种表示存在两个瓶颈：一是无法捕获全局多帧运动上下文，导致运动方向反转、背景误运动等问题；二是残差中包含与运动无关的高频空间伪影（如突发光照变化、背景纹理不一致），干扰运动信息的准确提取。

**核心方法**：本文提出 **Spectral Motion Alignment (SMA)**，将运动对齐从像素/特征空间拓展到频谱域。SMA 包含两个互补的频谱约束：（1）基于 1D Haar 小波变换的全局运动对齐损失，在时间维度上匹配多尺度频率成分，捕获长程运动动态；（2）基于 2D FFT 的局部运动细化损失，对齐幅度谱与相位谱，并通过频率加权函数优先保留低频运动信息，抑制高频伪影。

**核心洞察**：视频运动动态本质上可以通过其固有频率成分有效表示；在频谱域对齐运动表示，能够同时捕获全局多尺度运动模式并滤除与运动无关的噪声伪影。

**方法定位**：SMA 是一种即插即用的频谱损失模块，不修改基础架构，可兼容多种运动迁移框架，包括：
- 基于级联视频扩散模型的像素空间方法 **VMC**
- 基于双路径 LoRA 的文本到视频方法 **MotionDirector**
- 基于扩散特征（DIFT）的特征空间方法 **DMT**
- 基于文本到图像扩散模型的编辑方法 **Tune-A-Video** 和 **ControlVideo**

**主要结果**：在 VMC 框架上，SMA 将文本对齐度（CLIP）提升 0.026，帧一致性提升 0.016（Table 3）；在 MotionDirector 框架上，运动准确性（用户研究）获得显著提升（Table 1）；在 Tune-A-Video 和 ControlVideo 上，全部五项评估指标均获改善（Table 2）。消融实验验证了全局小波损失和局部傅里叶损失的独立贡献（Table 3，Figure 7），并表明 2D FFT 局部细化优于 2D DWT，低频优先策略是抑制伪影的关键（Figure 8b）。

**资源开销**：SMA 训练仅需约 15GB 显存和约 5 分钟训练时间，额外计算开销主要来自小波变换和 FFT，论文称其可忽略。



### 视频运动迁移的核心挑战

视频运动迁移任务的目标是：给定一段输入视频（源视频），将其中的运动模式提取并迁移到一个新的文本提示或内容场景上，使生成视频既保留源视频的运动动态，又符合目标内容的语义。近年来，基于扩散模型（Diffusion Models）的视频生成方法在该任务上取得了显著进展，涌现出多种代表性框架，包括基于级联视频扩散模型的 **VMC**（Video Motion Customization）、基于双路径 LoRA 的 **MotionDirector**、基于扩散特征（DIFT）的 **DMT**（Diffusion Motion Transfer），以及面向视频编辑的 **Tune-A-Video** 和 **ControlVideo** 等。

然而，现有方法在运动表征的学习与迁移上存在一个关键瓶颈：**它们几乎完全依赖像素空间或特征空间的帧间残差作为运动向量，并直接在原始空间中对齐这些残差**。这种做法的根本缺陷在于：

1. **缺乏全局多帧运动上下文**：帧间残差本质上只编码了相邻两帧之间的局部变化，无法捕获跨越多个时间步的长程运动动态。当视频中存在周期性运动（如荡秋千）或需要保持运动方向一致性（如从左到右的平移）时，仅靠局部残差对齐容易导致运动方向反转、运动幅度衰减等问题。

2. **高频空间伪影的干扰**：从预训练视频扩散模型中估计的运动向量，其高频空间成分往往对应的是与运动无关的噪声伪影——例如突发光照变化、背景纹理不一致、压缩伪影等。这些高频成分在原始空间中被不加区分地与真实运动信号混合，导致运动迁移时出现背景误运动、运动边界模糊等现象。

### 核心洞察：运动动态的频域本质

本文的核心洞察是：**视频运动动态可以有效地由其固有频率成分表示**。一个完整的运动模式——无论是全局的平移、旋转，还是局部的变形——在频域中都具有可辨识的频谱特征。具体而言：

- **时间维度**：运动向量的逐帧变化构成了沿时间轴的信号序列，其多尺度动态（快变与慢变成分）可以通过小波变换在不同频率层级上解耦。
- **空间维度**：单帧运动向量的空间分布，其结构信息（边缘、轮廓、运动区域）主要由低频成分承载，而高频成分则倾向于编码噪声和伪影。

基于这一洞察，论文提出 **Spectral Motion Alignment（SMA）**——一种在频谱域中对齐运动表示的新框架。SMA 将运动对齐从原始像素/特征空间迁移到频域，通过两个互补的频谱约束实现更精确的运动迁移：

- **1D 小波全局对齐**：对帧序列的运动向量沿时间轴进行 Haar 小波变换，在多尺度小波域中对齐真实运动向量与估计运动向量，使模型能够同时学习不同时间尺度上的全局运动模式。
- **2D 傅里叶局部细化**：对单帧运动向量进行 2D FFT，分别对齐幅度谱和相位谱，并通过频率加权函数优先保留低频成分，从而滤除与运动无关的高频伪影。

### 方法定位与兼容性

SMA 被设计为一个**即插即用的频谱损失模块**，不修改任何基础架构的模型权重或推理流程。它可以在训练阶段作为额外的损失项注入到现有的运动迁移框架中，与像素空间或特征空间的原始对齐损失联合优化。论文在五种代表性框架（VMC、MotionDirector、DMT、Tune-A-Video、ControlVideo）上验证了 SMA 的兼容性，均观察到一致的性能提升（详见 Table 1、Table 2）。训练开销方面，以 VMC + SMA 为例，仅需约 15 GB 显存和约 5 分钟的训练时间，额外计算负担主要来自小波变换和 FFT，论文声称其开销可忽略。



## 核心方法与创新机理

### 1. 瓶颈洞察：现有运动表示的两类系统性缺陷

现有视频运动迁移方法（如 VMC、MotionDirector、DMT）的运动表示均构建于像素或特征空间的帧间残差之上。这种表示存在两个根本性问题：

**缺陷一：缺乏全局多帧运动上下文。** 帧间残差仅编码相邻两帧的局部差分，无法捕获跨越多帧的长程运动动态（如周期性往复运动、加速/减速模式）。这导致模型在蒸馏运动时容易出现运动方向反转或背景误运动——例如，当输入视频中相机与物体同向移动时，残差向量可能错误地将背景静态区域标记为运动区域。

**缺陷二：运动向量被高频空间伪影污染。** 预训练视频扩散模型在未微调时估计的运动向量包含大量与运动无关的高频成分（如突发光照变化、纹理噪声、背景不一致性）。这些伪影在像素/特征空间中对齐时会被模型一并学习，导致生成视频中出现非期望的运动模式。

### 2. 核心洞察：频谱域运动对齐

SMA 的核心思想是将运动对齐从像素/特征空间迁移到频谱域。其理论依据是：**视频运动动态可以有效地由其固有频率成分表示**——低频成分对应平滑、全局的运动趋势，高频成分则往往对应与运动无关的空间伪影。通过在频谱域对齐运动表示，可以同时实现两个目标：(1) 捕获全局多尺度运动模式（通过小波域的多分辨率分解）；(2) 过滤高频噪声伪影（通过傅里叶域的频率加权）。

### 3. 三个关键 changed slots

相对于仅使用像素空间对齐的基线方法，SMA 引入了三个结构性改进：

| 改进维度 | 基线方法 | SMA 方案 | 证据锚点 |
|---------|---------|---------|---------|
| **全局运动对齐** | 无全局约束，仅依赖帧间残差 | 1D Haar 小波多尺度时间频率对齐损失 $\ell_{\text{global}}$ | Section 3.2, eq(16) |
| **局部运动细化** | 直接对齐原始运动向量，无频谱处理 | 2D FFT 幅度/相位匹配损失 $\ell_{\text{local}}^A + \ell_{\text{local}}^P$，引入频率加权函数 $\omega(a,b)$ 优先学习低频成分 | Section 3.3, eq(17) |
| **对齐空间** | 仅在像素空间或特征空间计算损失 | 同时在像素域和频谱域（小波域 + 傅里叶域）联合优化 | Section 3.4, eq(18) |

#### 3.1 全局运动对齐：1D 小波变换

SMA 对每个空间像素位置沿时间轴抽取一维运动向量序列，应用 Haar 小波离散小波变换（DWT）进行多尺度分解：

$$L[n] = \frac{1}{\sqrt{2}}[1\quad 1], \quad H[n] = \frac{1}{\sqrt{2}}[-1\quad 1]$$

通过在各级小波系数上施加 L1 损失，模型被强制在多个时间尺度上匹配真实运动向量与估计运动向量的频率成分。这使模型能够同时学习短程（相邻帧）和长程（远隔帧）的运动动态，有效解决了运动反向问题（消融证据见 Figure 7）。

#### 3.2 局部运动细化：2D 傅里叶变换与频率加权

对单帧运动向量进行 2D FFT，分别对齐幅度谱和相位谱：

- **幅度匹配损失**：约束运动强度在频域的分布一致性
- **相位匹配损失**：保持运动结构的空间位置一致性

关键设计是引入频率加权函数 $\omega(a,b)$，该函数对低频区域赋予更高权重，对高频区域进行抑制。这一设计的因果机制是：运动向量的高频成分主要对应与运动无关的空间伪影（Figure 6(a)(b) 提供了频谱可视化证据），通过低频优先策略，模型能够专注于学习核心运动信息而非噪声。

#### 3.3 联合优化框架

整体训练目标将像素域对齐损失、全局小波损失和局部傅里叶损失联合优化：

$$\min_{\theta} \mathbb{E}_{t,n,\epsilon_t^n,\epsilon_t^{n+1}} \Big[ \ell_{\text{align}} + \lambda_g \ell_{\text{global}} + \lambda_l \ell_{\text{local}} \Big]$$

这种多域联合约束使运动表示既保持了像素空间的细粒度对齐，又获得了频谱域的全局一致性和噪声鲁棒性。

### 4. 设计选择的关键证据

消融实验（Table 3）验证了各组件的独立贡献：仅添加局部光谱损失（$\ell_{\text{local}}$）即可提升 Text-Align 和 Frame-Con 指标，进一步加入全局小波损失（$\ell_{\text{global}}$）带来额外增益。Figure 8(b) 表明 2D FFT 局部细化优于 2D DWT 方案，且超参数更易调节。



![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/003_Figure_3.jpg]]
*Figure 3: Comparison within MotionDirector framework*

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/004_Figure_4.jpg]]
*Figure 4: Comparison within VMC framework using Show-1 video model (top) and DMT framework using Zeroscope video model (bottom). Each demonstrate the compatibility of SMA in pixel-space and feature-space, respectively*

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/002_Figure_2.jpg]]
*Figure 2: Overview. The proposed Spectral Motion Alignment (SMA) framework distills the motion information in frequencydomain. Considering the (latent) frame residuals as motion vectors, we first derive the denoised motion vector estimates. Then, the motion vector $\delta \pmb { v } _ { 0 } ^ { n }$ and its estimate $\delta \hat { { \pmb v } } _ { 0 } ^ { n }$ are aligned in both pixel-domain and frequency-domain. Our regularization includes (1) global motion alignment based on 1D wavelet-transform, and (2) local motion refinement based on 2D Fourier transform

Spectral Motion Alignment (SMA) 是一个即插即用的运动对齐框架，其核心思想是将运动表征的学习从像素/特征空间迁移到频谱域，以同时捕获全局多尺度运动动态并抑制与运动无关的高频伪影。图2给出了SMA的整体pipeline。

**输入与运动向量定义**：给定一个包含 $N$ 帧的输入视频，SMA首先利用预训练视频扩散模型（如Show-1或Zeroscope）的潜变量序列 $\mathbf{v}_t^{1:N}$。对于每一对相邻帧，定义第 $n$ 帧的运动向量为它们在潜空间中的残差：

$$\delta \mathbf{v}_t^n := \mathbf{v}_t^{n+1} - \mathbf{v}_t^n$$

这一残差向量编码了帧间的运动信息，是后续所有频谱对齐操作的基础信号。

**去噪运动向量估计**：由于扩散模型在训练时处理的是加噪潜变量，直接从 $\delta\mathbf{v}_t^n$ 计算对齐损失会受到噪声干扰。SMA利用Tweedie公式从噪声潜变量中恢复干净的运动向量估计：

$$\hat{\mathbf{v}}_0^{1:N}(t) := \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \mathbf{v}_t^{1:N} - \sqrt{1-\bar{\alpha}_t} \boldsymbol{\epsilon}_\theta(\mathbf{v}_t^{1:N}, t, c) \big)$$

由此得到去噪后的运动向量估计 $\delta\hat{\mathbf{v}}_0^n(t)$ 和真实运动向量 $\delta\mathbf{v}_0^n$，二者构成对齐损失的计算对。

**双分支频谱对齐**：SMA的对齐过程分为两个互补的频谱分支，与像素空间的基线对齐损失联合优化：

1. **1D小波全局运动对齐**（Section 3.2）：将每个空间位置的逐帧运动向量抽取为1D时间序列，通过Haar小波的离散小波变换（DWT）将其分解为多尺度频率分量。在各级小波系数上施加L1损失 $\ell_{\text{global}}$，迫使模型学习跨帧的长程运动动态，从而缓解仅依赖帧间残差导致的运动反向或背景误运动问题。

2. **2D傅里叶局部运动细化**（Section 3.3）：对每一帧的运动向量进行2D快速傅里叶变换（FFT），分别对齐其幅度谱和相位谱。通过引入频率加权函数 $\omega(a,b)$ 优先学习低空间频率成分，抑制高频伪影（如突发光照变化、背景纹理不一致等），保留核心运动结构。

**联合优化目标**：SMA的完整训练目标将像素域对齐损失 $\ell_{\text{align}}$、全局小波损失 $\ell_{\text{global}}$ 和局部傅里叶损失 $\ell_{\text{local}}$ 联合优化：

$$\min_\theta \mathbb{E}_{t,n,\epsilon_t^n,\epsilon_t^{n+1}} \Big[ \ell_{\text{align}} + \lambda_g \ell_{\text{global}} + \lambda_l \ell_{\text{local}} \Big]$$

其中 $\lambda_g$ 和 $\lambda_l$ 控制两个频谱损失的相对权重。

**特征空间扩展**：SMA的频谱对齐范式可进一步推广至扩散特征空间（DIFT），在语义特征维度上施加相同的全局和局部频谱损失，使其能够兼容基于特征空间的运动迁移方法（如DMT）。

**计算开销**：SMA作为一个轻量级微调模块，未修改基础视频扩散模型的架构。训练时仅需约15GB显存，训练时间约5分钟，额外引入的小波变换和FFT计算开销被论文声称可忽略。



### 3.1 去噪运动向量估计

SMA 的核心操作对象是**运动向量**（motion vector），定义为相邻帧潜变量的残差：

$$
\delta \pmb{v}_t^n := \pmb{v}_t^{n+1} - \pmb{v}_t^n \tag{10}
$$

其中 $\pmb{v}_t^n$ 表示第 $n$ 帧在扩散时间步 $t$ 的潜变量表示。为获得干净的运动表示，SMA 利用预训练视频扩散模型和 Tweedie 公式，从带噪观测中估计去噪后的视频帧：

$$
\hat{\pmb{v}}_0^{1:N}(t) := \frac{1}{\sqrt{\bar{\alpha}_t}} \big( \pmb{v}_t^{1:N} - \sqrt{1-\bar{\alpha}_t} \pmb{\epsilon}_{\theta}(\pmb{v}_t^{1:N}, t, c) \big) \tag{13}
$$

由此可进一步推导出干净的**像素空间运动向量** $\delta \pmb{v}_0^n$ 及其估计值 $\delta \hat{\pmb{v}}_0^n(t)$，作为后续频谱对齐的监督信号。

---

### 3.2 1D 小波全局运动对齐

为捕获跨帧的**多尺度全局运动动态**，SMA 对运动向量序列沿时间维度抽取逐像素的 1D 信号，应用 Haar 小波离散小波变换（DWT）。Haar 小波的低通 $L[n]$ 和高通 $H[n]$ 滤波器定义为：

$$
L[n] = \frac{1}{\sqrt{2}}[1, 1], \quad H[n] = \frac{1}{\sqrt{2}}[-1, 1] \tag{15}
$$

全局频率匹配损失约束估计运动向量与真实运动向量在小波域的多尺度系数一致：

$$
\ell_{\mathtt{global}}(\delta \pmb{v}_0, \delta \hat{\pmb{v}}_0(t)) = \mathbb{E}_{t, s, j, k} \Big[ \| \mathcal{W}_{\delta \pmb{v}_{0,s}}(j, k) - \mathcal{W}_{\delta \hat{\pmb{v}}_{0,s}(t)}(j, k) \|_1 \Big] \tag{16}
$$

其中 $\mathcal{W}$ 表示 Haar DWT 系数，$s$ 遍历所有空间像素位置，$(j,k)$ 为小波域的多尺度索引。该损失使模型同时学习不同时间尺度下的运动模式，有效缓解仅依靠帧间残差导致的运动反向和背景误运动问题（图 7）。

---

### 3.3 2D 傅里叶局部运动细化

单帧运动向量中，高频成分往往对应与运动无关的空间伪影（如突发光照变化、纹理不一致）。SMA 通过 2D FFT 将运动向量变换到频域，分别对齐**幅度谱**和**相位谱**，并引入频率加权函数 $\omega(a,b)$ 优先保留低频运动信息：

**幅度匹配损失：**

$$
\mathbb{E}_{t, n, a, b} \bigg[ \omega(a, b) \| |\mathcal{F}_{\delta v_0^n}(a, b)| - |\mathcal{F}_{\delta \hat{v}_0^n(t)}(a, b)| \|_1 \bigg] \tag{17-A}
$$

**相位匹配损失：**

$$
\mathbb{E}_{t, n, a, b} \bigg[ \omega(a, b) \| \angle\mathcal{F}_{\delta v_0^n}(a, b) - \angle\mathcal{F}_{\delta \hat{v}_0^n(t)}(a, b) \|_1 \bigg] \tag{17-P}
$$

其中 $\mathcal{F}$ 为 2D 傅里叶变换，$\omega(a,b)$ 为抑制高频的频率加权函数（依赖于超参数 $\delta$）。图 6(a)(b) 的可视化验证了高频分量确实对应运动无关伪影，低频优先策略是抑制伪影的关键。

---

### 3.4 整体优化目标

SMA 将像素域对齐损失、全局小波损失和局部傅里叶细化损失联合优化：

$$
\min_{\theta} \mathbb{E}_{t, n, \epsilon_t^n, \epsilon_t^{n+1}} \Big[ \ell_{\mathrm{align}}(\delta \pmb{v}_0^n, \delta \hat{\pmb{v}}_0^n(t)) + \lambda_g \ell_{\mathrm{global}}(\delta \pmb{v}_0, \delta \hat{\pmb{v}}_0(t)) + \lambda_l \ell_{\mathrm{local}}(\delta \pmb{v}_0^n, \delta \hat{\pmb{v}}_0^n(t)) \Big] \tag{18}
$$

其中 $\ell_{\mathrm{align}}$ 为原始像素空间对齐损失（继承自各 baseline），$\lambda_g$ 和 $\lambda_l$ 为平衡系数。该设计使 SMA 作为即插即用模块，无需修改基础架构即可注入频谱域约束。

---

### 3.5 特征空间扩展（可选）

SMA 的对齐范式可推广至扩散特征（DIFT）空间，在语义特征维度上施加全局和局部频谱损失，支持特征空间运动迁移（如 DMT 框架）。特征空间的频谱对齐目标为：

$$
\mathbb{E} \Big[ \ell_{\mathrm{DMT}}(f(v_t), f(\tilde{v}_t)) + \lambda_g \ell_{\mathrm{global}}(\delta f(\pmb{v}_t), \delta f(\tilde{v}_t)) + \lambda_l \ell_{\mathrm{local}}(\delta f(\pmb{v}_t), \delta f(\tilde{v}_t)) \Big] \tag{19}
$$

其中 $f(\cdot)$ 为扩散模型中间层提取的语义特征，$\ell_{\mathrm{DMT}}$ 为原始 DMT 的时空特征损失。



## 实验与关键发现

### 主实验结果

SMA 被集成为即插即用的频谱对齐模块，在多种视频运动迁移框架上均带来一致的性能提升，涵盖文本到视频（T2V）和文本到图像（T2I）两类基线。

**T2V 框架结果（Table 1）**。在 MotionDirector 和 VMC 上注入 SMA 后，四项核心指标——文本对齐度（Text-Align）、时间一致性（Temp-Con）、编辑准确性（Edit-Acc）和运动准确性（Motion-Acc）——全部获得提升。以 MotionDirector 为例，添加 SMA 后 Text-Align 达到 0.8081，Temp-Con 达到 0.9784，用户研究中的 Edit-Acc 和 Motion-Acc 分别达到 4.14 和 3.88（5 分制）。定性结果（Figure 3）进一步表明，SMA 有效解决了运动误对齐问题：在“鹰从右向左飞”的场景中，无 SMA 的基线错误地让背景地面也发生移动，而 SMA 仅让鹰产生正确的平移运动，实现了动态前景与静态背景的准确分离。

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/005_Table_1.jpg]]
*Table 1: Quantitative evaluation of SMA within text-tovideo based frameworks*

**T2I 框架结果（Table 2）**。在 Tune-A-Video 和 ControlVideo 上集成 SMA 后，所有五项评估指标（Text-Align、Temp-Con、Edit-Acc 及两项时间一致性/运动准确性指标）均获提升，验证了 SMA 对基于图像扩散模型的视频编辑方法同样有效。Figure 5 的定性对比显示，SMA 在保持编辑准确性的同时显著改善了帧间运动的一致性。

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of SMA within text-toimage based frameworks*

**跨空间兼容性（Figure 4）**。SMA 在像素空间（VMC + Show-1 视频模型）和扩散特征空间（DMT + Zeroscope 视频模型）均能稳定工作，证明频谱对齐范式不依赖于特定的运动表示空间。

### 消融实验

消融研究围绕 VMC 基准展开，系统验证了局部频谱细化损失（$\ell_{\text{local}}$）和全局小波对齐损失（$\ell_{\text{global}}$）的独立贡献。

**定量消融（Table 3）**。仅添加 $\ell_{\text{local}}$ 已使 Text-Align 和 Frame-Con 分别提升 0.020 和 0.008，在此基础上进一步加入 $\ell_{\text{global}}$ 带来额外增益，最终两项指标分别累计提升 0.026 和 0.016。这表明局部频谱细化和全局多尺度对齐是互补的：前者抑制单帧内的空间伪影，后者捕获跨帧的长程运动动态。

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation of $\mathcal { L } _ { \mathrm { l o c a l } }$ and ${ \mathcal { L } } _ { \mathrm { g l o b a l } }$

**全局对齐的定性验证（Figure 7）**。移除 $\ell_{\text{global}}$ 后，生成视频出现明显的运动方向错误（如反向运动）和背景误运动；引入全局小波对齐后，模型能够正确学习输入视频的整体运动模式，输出的运动方向与源视频一致。这证实了 1D Haar 小波变换在捕获多尺度时间运动动态方面的关键作用。

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/010_Figure_7.jpg]]
*Figure 7: Ablation study on global alignment. Global motion alignment facilitates motion transfer*

**局部细化的频谱分析（Figure 6）**。Figure 6(a)(b) 展示了预训练模型在无微调时估计的运动向量频谱：高频区域存在大量与运动无关的伪影（如突发光照变化、背景纹理不一致）。SMA 通过频率加权函数 $\omega(a,b)$ 优先保留低频成分，有效滤除了这些高频噪声，使学习到的运动表示更干净。Figure 8(b) 进一步比较了 2D FFT 与 2D DWT 在局部细化中的效果，结果表明 2D FFT 更优且超参数更易调节。

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/007_Figure_6.jpg]]
*Figure 6: Visualization of (a) spatial frequency spectrum and (b) motion vectors estimated from the pre-trained Show-1 (Zhang et al. 2023a) without fine-tuning. (c) Ablation study on spectral motion alignment based on VMC (Jeong, Park, and Ye 2023)*

### 计算开销与公平性

SMA 的训练开销轻量：在 VMC 框架上仅需约 15 GB 显存，训练时间约 5 分钟。额外计算主要来自小波变换和 FFT，论文称其开销可忽略，但未提供与基线的绝对时间/显存对比消融。所有对比实验均沿用原始 baseline 的优化器、学习率和训练步数，仅添加 SMA 损失项，保证了实验的公平性。

### 失败模式与局限性

尽管 SMA 在多个基准上表现稳健，仍存在以下局限：

1. **超参数敏感性**：局部细化中的频率加权依赖于超参数 $\delta$，不同视频可能需要手动调节才能获得最佳低频保留效果。
2. **微调范式限制**：SMA 仍需为每个新输入视频进行定制训练，尚未实现零样本运动迁移。
3. **泛化边界未验证**：当前评估集中在自然场景和常见物体运动，对于极端视角变化、大规模遮挡或抽象运动模式，SMA 的有效性缺乏实验支撑。
4. **计算开销细节不足**：虽然声称小波变换和 FFT 开销可忽略，但缺少与其他方法的绝对时间/显存对比数据，该点需读者自行验证。

### 补充图表

![[assets/figures/papers/paper_list_l27_Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Mode/figures/011_Figure.jpg]]



## 定位与知识库关联

### 1. 方法定位与核心差异

SMA 属于视频运动迁移（Video Motion Transfer）中的**运动表示学习**方法，其核心创新在于将运动对齐的空间从像素/特征域迁移至频谱域。与现有工作的关键差异如下：

**像素空间运动迁移基线**——**VMC** (Jeong, Park, and Ye, 2023) 和 **MotionDirector** (Zhao et al., 2024) 等方法——直接对齐帧间残差（运动向量）的像素值或潜变量，这种表示存在两个结构性缺陷：(1) 单帧残差仅捕获局部相邻帧的瞬时变化，缺乏对整段视频全局运动动态（如运动方向、速度趋势）的感知能力；(2) 残差向量中混入了与运动无关的高频空间伪影（如突发光照变化、背景纹理不一致），导致运动迁移时出现背景误运动或运动反向等失效模式（见 Figure 7 消融证据）。

**特征空间运动迁移基线**——**DMT** (Yatim et al., 2024) 将运动对齐拓展至扩散模型中间层的语义特征（DIFT, Tang et al., 2023），虽然提升了语义一致性，但同样未解决全局运动上下文缺失和高频噪声干扰的问题。

SMA 的因果调控旋钮在于：**将运动向量变换到频谱域，利用频率成分的天然解耦特性**——低频成分编码运动的主体结构与方向，高频成分则对应空间细节和噪声伪影——从而在统一框架内同时实现全局多尺度运动建模和运动无关伪影抑制。具体而言：

- **1D 小波全局对齐**（Section 3.2）：对逐像素的帧间运动向量序列施加 Haar 小波变换，在多尺度时间频率上对齐小波系数，使模型学习到跨帧的长程运动动态，从根本上缓解运动反向问题。
- **2D 傅里叶局部细化**（Section 3.3）：对单帧运动向量进行 2D FFT，分别对齐幅度谱和相位谱，并通过频率加权函数 $\omega(a,b)$ 优先保留低频分量，显式抑制高频伪影。

### 2. 与现有工作的关系

SMA 并非替代现有运动迁移框架，而是作为**即插即用的频谱正则化模块**叠加于其上。论文在五类代表性基线上验证了兼容性：

| 基线方法 | 框架类型 | SMA 注入方式 |
|---------|---------|------------|
| **VMC** (Jeong, Park, and Ye, 2023) | 级联视频扩散模型，像素空间 | 在像素运动向量上施加全局+局部频谱损失 |
| **MotionDirector** (Zhao et al., 2024) | 双路径 LoRA，T2V 扩散模型 | 同上，替换原始运动对齐损失 |
| **DMT** (Yatim et al., 2024) | 扩散特征空间 | 将频谱损失扩展至 DIFT 特征维度（Section 3.5） |
| **Tune-A-Video** (Wu et al., 2023) | T2I 单样本微调 | 在潜变量运动向量上施加频谱约束 |
| **ControlVideo** (Zhang et al., 2023) | ControlNet 零样本编辑 | 同上 |

所有实验均保持原始基线的优化器、学习率和训练步数不变，仅添加 SMA 损失项（$\ell_{\text{global}} + \ell_{\text{local}}$），训练开销约 15GB 显存、5 分钟（基于 VMC + Show-1 级联模型）。

### 3. 适用边界

**有效场景**：
- 自然场景中常见物体运动（如动物奔跑、车辆行驶、人体动作）的迁移，尤其适用于需要保持全局运动方向一致性的长程运动模式。
- 基于文本到视频（T2V）和文本到图像（T2I）扩散模型的多种运动定制/视频编辑框架。

**已知局限**：
1. **微调范式依赖**：SMA 需要为每个输入视频进行模型定制训练，无法实现零样本推理时的运动迁移。频谱损失目前以训练目标形式注入，尚未设计为推理阶段的引导项。
2. **超参数敏感性**：局部细化中的频率加权函数依赖超参数 $\delta$（控制高低频分界），不同视频内容可能需要手动调节才能获得最佳伪影抑制效果（Section 3.3）。
3. **运动模式泛化未验证**：现有评估集中于自然场景和常规物体运动，对于相机运动剧烈、存在大规模遮挡或极端视角变化的输入视频，SMA 的有效性缺乏实验支撑。
4. **计算开销的绝对对比缺失**：论文声称小波变换和 FFT 引入的额外开销“可忽略”，但未提供与基线方法在绝对训练时间/显存上的详细消融对比，该声称需要独立验证。

### 4. 开放问题

1. **频谱对齐策略的维度扩展**：当前 SMA 在 2D 空间+1D 时间上分别进行频谱变换，能否推广到统一的 3D 运动表示（如 3D FFT 或球谐变换），以支持 NeRF 或 4D 生成任务中的运动迁移？
2. **推理阶段解耦**：能否将 SMA 的频谱约束设计为无训练的引导项（类似于 classifier guidance），从而在推理时直接控制运动迁移，消除微调需求？
3. **小波族的选择**：论文仅探索了 Haar 小波，是否存在更适合视频运动建模的其他小波族（如 Daubechies 系列、Morlet 复小波），能在运动模式保真度和计算效率之间取得更优平衡？
4. **频谱对齐的理论保证**：当前方法依赖经验性的频率加权函数，缺乏对“哪些频率成分编码运动信息”的理论刻画。能否通过信息瓶颈或频域解耦理论，给出运动相关频率成分的可识别性条件？



## 原文 PDF

![[paperPDFs/AAAI_2025/Spectral_Motion_Alignment_for_Video_Motion_Transfer_using_Diffusion_Models.pdf]]
