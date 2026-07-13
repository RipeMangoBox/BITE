---
title: Decoupled Residual Denoising Diffusion Models for Unified and Data Efficient Image-to-Image Translation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Decoupled_Residual_Denoising_Diffusion_Models_for_Unified_and_Data_Efficient_Image_to_Image_Translation.pdf
project_link: null
code_link: "https://github.com/HKU-HealthAI/DRDD"
aliases:
- DDRDDM
- DRDDMUDEIIT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将耦合扩散解耦为两个独立阶段：先执行噪声扩散实现域协调，再在固定噪声域内完成残差扩散（语义映射）；逆向时先进行残差消除以保持协调，最后去噪。
primary_logic: 高斯噪声注入不仅能提升流形，还可作为“域协调器”隐式对齐不同域的分布；在核心语义变换完成前保留该噪声效应，能大幅简化统一图像翻译的学习。
claims:
- 注入高斯噪声能够缩小不同分布之间的KL散度，起到域协调作用
- 解耦框架在All-in-One-5和CDD-11等统一多任务基准上全面超越现有方法，尤其在感知指标上优势明显
- 解耦设计使核心映射在噪声域内完成，协调效应得以保持，在训练数据大幅减少时性能下降远小于其他方法
- All-in-One-5 上 SSIM / LPIPS / FID (average) = 0.916 / 0.073 / 18.3
---

# Decoupled Residual Denoising Diffusion Models for Unified and Data Efficient Image-to-Image Translation

> [!tip] 核心洞察
> 高斯噪声注入不仅能提升流形，还可作为“域协调器”隐式对齐不同域的分布；在核心语义变换完成前保留该噪声效应，能大幅简化统一图像翻译的学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解耦残差去噪扩散模型：实现统一高效图像到图像翻译 |
| 英文题名 | Decoupled Residual Denoising Diffusion Models for Unified and Data Efficient Image-to-Image Translation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lin_Decoupled_Residual_Denoising_Diffusion_Models_for_Unified_and_Data_Efficient_CVPR_2026_paper.html) · [Code](https://github.com/HKU-HealthAI/DRDD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DRDD (Decoupled Residual Denoising Diffusion models) |
| Dataset | All-in-One-5, CDD-11, MNMD |

> [!tip] 效果简介
> - All-in-One-5 上，SSIM / LPIPS / FID (average) 0.916 / 0.073 / 18.3 vs 近期SOTA方法（参见Table 1） (显著优于所有对比方法，感知指标优势突出)。
> - CDD-11 上，SSIM (11种退化任务平均) 最高平均SSIM vs 近期SOTA模型 (在所有退化类型上一致超越，复合退化场景优势明显)。
> - MNMD (多域去噪) 上，SSIM / LPIPS Natural: 0.9391/0.0492, Medical: 0.9324/0.0629, Remote: 0.9300/0.0539 vs 其他对比方法（Table 2） (在自然、医学、遥感域均取得最高SSIM和最低LPIPS)。

## 概要

图像到图像（I2I）翻译旨在学习源域到目标域的映射，在图像修复、增强等底层视觉任务中应用广泛。然而，现有方法面临两个核心挑战：**统一性不足**——多数模型只能处理单一任务，难以在同一个框架内应对多种退化类型；**数据效率低下**——训练严重依赖成对的源-目标图像，限制了在数据稀缺场景下的应用。

本文提出**解耦残差去噪扩散模型（DRDD）**，从扩散过程的根本上解决上述瓶颈。传统耦合扩散模型在逆向过程中同时移除噪声和残差，过早削弱了噪声带来的域协调效应，阻碍统一且数据高效的I2I翻译。DRDD将耦合扩散**解耦为两个独立阶段**：先执行噪声扩散实现域协调与流形提升，再在固定噪声域内完成残差扩散（语义映射）；逆向时则先进行残差消除以保持协调，最后去噪生成清晰图像。

该设计的核心洞察在于：高斯噪声注入不仅能提升流形，还可作为**“域协调器”**隐式对齐不同域的分布——理论证明，注入噪声后两分布间的KL散度显著减小（Proposition 3.1）。在核心语义变换完成前保留这一噪声效应，大幅简化了统一图像翻译的学习。同时，噪声扩散/去噪阶段仅需非成对的目标域图像训练，显著提升了数据效率。

在统一多任务基准**All-in-One-5**上，DRDD取得平均SSIM 0.916、LPIPS 0.073、FID 18.3，全面超越近期SOTA方法，感知指标优势尤为突出（Table 1）。在**CDD-11**的11种退化任务中，DRDD在所有类型上一致超越对比模型，复合退化场景优势明显（Figure 3）。数据剪枝实验表明，当训练数据从100%降至25%时，DRDD的性能下降远小于RDDM、I2SB等方法（Figure 5），验证了解耦设计带来的数据效率提升。



图像到图像（I2I）翻译旨在将源域图像映射为目标域图像，是底层视觉的核心任务，涵盖图像修复、超分辨率、去雨、低光增强等众多子方向。近年来，扩散模型凭借其强大的生成能力在该领域取得了显著进展，涌现出**RDDM**（Liu et al., 2024）、**I2SB**（Liu et al., 2023）、**IR-SDE**（Luo et al., 2023）等代表性工作。

然而，现有扩散式I2I方法面临两个关键瓶颈：

**瓶颈一：耦合扩散过程阻碍统一多任务翻译。** 传统方法采用单一耦合的扩散过程，在逆向生成时同时移除噪声和源-目标残差（即域间差异）。这种设计在单一任务上表现良好，但面对多域、多任务的统一翻译场景时，不同源域之间存在显著的分布间隙（domain gap），耦合过程难以同时协调多个域的对齐，导致统一模型性能受限。如Figure 1(a)的t-SNE可视化所示，原始源域的特征表示在不同I2I任务间呈现明显的域间隙，这从根本上增加了统一翻译的难度。

**瓶颈二：噪声效应被过早削弱。** 现有方法将高斯噪声注入仅视为流形提升和训练信号增强的手段，在逆向过程早期即开始同时去除噪声和残差。然而，本文发现了一个被忽视的关键现象：**高斯噪声注入能够缩小不同分布之间的KL散度，起到“域协调器”的作用**。如Proposition 3.1所证明，注入高斯噪声后两分布间的KL散度严格减小（$D_{KL}(P_{\sigma} \parallel Q_{\sigma}) < D_{KL}(P \parallel Q)$），Figure 1(b)的t-SNE结果也直观展示了噪声注入后域间隙的显著缩小。耦合扩散在核心语义映射完成前就移除了噪声，过早丧失了这种域协调效应，使得统一翻译的学习难度大幅增加。

**核心动机：解耦扩散，保留噪声的域协调效应。** 基于上述洞察，本文提出将传统耦合扩散解耦为两个顺序独立的阶段——先执行噪声扩散实现域协调与流形提升，再在固定噪声域内完成残差扩散（语义映射）；逆向时先消除残差以保持协调效应，最后去噪生成清晰图像。这一解耦设计使核心语义变换始终在噪声协调后的统一域内完成，从根本上降低了统一I2I翻译的学习难度，同时噪声扩散阶段可仅使用非成对目标域图像训练，显著提升了数据效率。



## 核心方法与创新机理

DRDD的核心创新在于**将传统耦合扩散过程解耦为两个顺序且独立的阶段**，从根本上改变了噪声在图像到图像（I2I）翻译中的角色。传统扩散模型（如**RDDM**（Liu et al., 2024）、**I2SB**（Liu et al., 2023）、**IR-SDE**（Luo et al., 2023））采用单一耦合逆向过程，在从含噪输入恢复目标图像时**同时移除噪声和源-目标残差**。这种设计存在一个关键瓶颈：噪声在逆向早期就被消除，使其无法充分发挥“域协调器”的作用，从而阻碍统一且数据高效的I2I翻译。

DRDD通过三个核心机制突破这一瓶颈：

### 1. 扩散过程解耦：噪声扩散与残差扩散分离

DRDD将传统单一前向扩散过程彻底解耦为两个顺序且独立的阶段（Figure 2）：

- **噪声扩散阶段**：首先向目标图像逐步注入高斯噪声，实现流形提升和域协调。其前向步骤为 $I_t^{(1)} = I_0^{(1)} + \bar{\beta}_t \varepsilon$（Eq. 2）。该阶段仅需非成对目标域图像即可训练，显著提升了数据效率。
- **残差扩散阶段**：在固定噪声域内，通过确定性方式注入源-目标残差，完成核心语义映射。其前向步骤为 $I_t^{(2)} = I_0^{(2)} + \bar{\alpha}_t I_{\mathrm{res}}$（Eq. 3）。

逆向过程对应解耦为**先残差消除、后去噪**两个阶段（Figure 1右）。残差消除阶段在噪声域内完成语义变换：$I_{t-1}^{(2)} = I_t^{(2)} - \alpha_t I_{\mathrm{res}}^{\theta}(I_t^{(2)}, I_{\mathrm{in}}, t)$（Eq. 6），此时噪声效应得以完整保留。去噪阶段再从含噪目标中去除高斯噪声，生成最终清晰图像：$I_{t-1}^{(1)} = I_t^{(1)} - (\bar{\beta}_t - \sqrt{\bar{\beta}_{t-1}^2 - \sigma_t^2}) \epsilon_{\theta}(I_t^{(1)}, t) + \sigma_t \varepsilon_t$（Eq. 8）。

### 2. 噪声角色重塑：从流形提升到域协调

DRDD揭示了高斯噪声在I2I翻译中的一个新角色——**域协调器**。理论分析（Proposition 3.1）证明，注入高斯噪声能够缩小不同分布之间的KL散度：$D_{KL}(P_{\sigma} \parallel Q_{\sigma}) < D_{KL}(P \parallel Q)$。如Figure 1(a)-(b)的t-SNE可视化所示，原始源域存在显著的域间隙，而引入噪声后（Source+Noise域）特征表示明显更加接近，这为统一处理多种I2I翻译任务奠定了基础。

解耦设计的关键在于：核心语义映射（残差扩散/消除）在噪声域内完成，使得噪声的域协调效应在映射完成前得以保持。这与传统耦合扩散中噪声被过早移除形成鲜明对比。

### 3. 数据效率的结构性提升

解耦架构天然带来了数据效率优势。噪声扩散/去噪阶段仅使用**非成对目标域图像**进行训练，无需成对的源-目标数据。这意味着在面对训练数据大幅减少时，DRDD的性能下降远小于其他方法（Figure 5）。当训练数据量从100%降至25%时，DRDD在SSIM和LPIPS指标上的退化幅度显著低于RDDM、I2SB等耦合扩散方法，验证了解耦设计对数据效率的结构性改善。



DRDD 将传统耦合扩散模型的前向/逆向过程解耦为两个顺序独立阶段，从根本上改变了噪声与残差的交互方式。整体 pipeline 由三个核心模块串联构成：**噪声扩散阶段**、**残差扩散/残差消除阶段**和**去噪阶段**，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/002_Figure_2.jpg]]
*Figure 2: Proposed DRDD framework. DRDD decouples the traditional single forward diffusion processes into two sequential and independent process: a noise diffusion stage that injects Gaussian noise into the target image, followed by a residual diffusion stage that conducts deterministic target-to-source transformation, but now within a noise-carrying level. The reverse diffusion process is correspondingly decoupled into a residual removal stage and a denoising stage*

### 设计动机：噪声的域协调效应

传统耦合扩散在逆向过程中同时移除噪声和残差，导致噪声在语义映射完成前就被削弱。DRDD 的核心洞察在于：高斯噪声不仅能提升流形，还可作为**域协调器**（domain harmonizer）隐式拉近不同域的分布。这一效应在 Proposition 3.1 中得到形式化证明——注入高斯噪声后两分布间的 KL 散度严格减小：

$$D_{KL}(P_{\sigma} \parallel Q_{\sigma}) < D_{KL}(P \parallel Q)$$

Figure 1 的 t-SNE 可视化直观展示了这一现象：原始源域与目标域的特征表示存在显著间隙（Figure 1a），而注入噪声后，含噪域的特征表示明显靠拢（Figure 1b），为统一 I2I 翻译创造了有利条件。

### 前向扩散：两阶段顺序注入

DRDD 的前向过程将噪声注入与语义变换彻底分离：

1.  **噪声扩散阶段（Noise Diffusion Stage）**：向目标图像 $I_0^{(1)}$ 逐步注入高斯噪声，生成含噪目标 $I_t^{(1)}$。该过程为随机扩散，遵循：
    $$I_t^{(1)} = I_0^{(1)} + \bar{\beta}_t \varepsilon$$
    此阶段仅使用**非成对目标域图像**训练，无需源-目标配对数据，显著提升了数据效率。

2.  **残差扩散阶段（Residual Diffusion Stage）**：在固定噪声域内，将源-目标残差 $I_{\mathrm{res}}$ 确定性注入含噪目标，完成从目标域到源域的语义映射：
    $$I_t^{(2)} = I_0^{(2)} + \bar{\alpha}_t I_{\mathrm{res}}$$
    由于残差注入发生在噪声域内，域协调效应得以完整保留，核心语义变换不再受噪声移除的干扰。

### 逆向推理：先残差消除，后去噪

逆向过程严格遵循前向的逆序，确保协调效应维持到语义映射完成：

1.  **残差消除阶段（Residual Removal Stage）**：基于网络预测的残差 $I_{\mathrm{res}}^{\theta}$，从含噪残差图像中逐步消除残差，恢复含噪目标图像：
    $$I_{t-1}^{(2)} = I_t^{(2)} - \alpha_t I_{\mathrm{res}}^{\theta}(I_t^{(2)}, I_{\mathrm{in}}, t)$$

2.  **去噪阶段（Denoising Stage）**：从含噪目标中去除高斯噪声，生成最终清晰图像：
    $$I_{t-1}^{(1)} = I_t^{(1)} - (\bar{\beta}_t - \sqrt{\bar{\beta}_{t-1}^2 - \sigma_t^2}) \epsilon_{\theta}(I_t^{(1)}, t) + \sigma_t \varepsilon_t$$

这一“先残差消除、后去噪”的顺序（Figure 1 的 (b) → (c) → (d)）与耦合扩散的“同时去除”（Figure 1 的 (b) → (d)）形成鲜明对比，是 DRDD 在统一多任务和数据高效场景下取得优势的结构性根源。

### 训练目标

两个阶段分别由独立的 L1 损失监督：

- 残差消除网络：$\mathcal{L}_{\mathrm{res}}(\theta) = \mathbb{E}[\|I_{\mathrm{res}} - I_{\mathrm{res}}^{\theta}(I_t^{(2)}, t, I_{\mathrm{in}})\|_1]$
- 去噪网络：$\mathcal{L}_{\epsilon}(\theta) = \mathbb{E}[\|\epsilon - \epsilon_{\theta}(I_t^{(1)}, t)\|_1]$

### 输入输出流总结

| 阶段 | 输入 | 输出 | 数据需求 |
|------|------|------|----------|
| 噪声扩散（前向） | 目标图像 | 含噪目标 | 非成对目标域图像 |
| 残差扩散（前向） | 含噪目标 + 残差 | 含噪残差图像 | 成对源-目标图像 |
| 残差消除（逆向） | 含噪残差图像 + 源图像 | 含噪目标 | — |
| 去噪（逆向） | 含噪目标 | 清晰目标 | — |



### 3.1 域协调的理论基础：噪声注入的KL散度消减

DRDD的核心出发点是一个被传统扩散模型忽略的洞察：高斯噪声不仅是流形提升工具，更是一个**域协调器（Domain Harmonizer）**。当向源域和目标域的图像分别注入等量高斯噪声后，两个含噪分布之间的KL散度严格小于原始分布之间的KL散度。这一性质由Proposition 3.1形式化给出：

$$D_{KL}(P_{\sigma} \parallel Q_{\sigma}) < D_{KL}(P \parallel Q)$$

其中 $P$ 和 $Q$ 分别表示源域和目标域的原始分布，$P_{\sigma}$ 和 $Q_{\sigma}$ 表示注入标准差为 $\sigma$ 的高斯噪声后的含噪分布。该不等式表明，噪声注入在分布层面缩小了域间隙，使得原本差异显著的源域和目标域在含噪空间中变得更加接近。Figure 1(a)-(b) 通过t-SNE可视化直观验证了这一效应：原始源域特征与目标域特征之间存在明显分离，而注入噪声后，两者的特征表征显著靠拢。

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/001_Figure_1.jpg]]
*Figure 1: Left: Domain gap reduction via noise introduction. t-SNE plot of feature representations across three I2I translation tasks. The original source domain (a) shows a significant domain gap, complicating unified I2I translation. Introducing noise (Source+Noise domain, b) reduces the domain gap, as shown by noticeably closer feature representation. Here, noise-carrying domains refer to domains with noise added to original images (e.g., Source+Noise and Target+Noise domains) as noise-carrying domains, excluding pure noise. Right: Reverse process comparison. During the inference stage, traditional coupled diffusion models perform domain shifting from the noise-carrying input to the target by simu...*

这一发现揭示了传统耦合扩散模型在统一I2I翻译中的根本瓶颈：耦合逆向过程同时去除噪声和残差，导致噪声带来的域协调效应在核心语义映射尚未完成时就被过早削弱。DRDD的解法是将噪声的协调效应保护到语义变换完成之后——即**先完成残差消除，再进行去噪**。

### 3.2 解耦扩散框架：两阶段前向过程

DRDD将传统单阶段耦合扩散彻底解耦为两个顺序独立的前向阶段（Figure 2）：

**阶段一：噪声扩散（Noise Diffusion）**。向目标域清晰图像 $I_0^{(1)}$ 逐步注入高斯噪声，前向步骤为：

$$I_t^{(1)} = I_0^{(1)} + \bar{\beta}_t \varepsilon$$

其中 $\varepsilon \sim \mathcal{N}(0, \mathbf{I})$ 为标准高斯噪声，$\bar{\beta}_t$ 为累积噪声调度系数，控制噪声注入强度。该阶段完全在目标域图像上执行，不涉及源域信息，因此训练仅需非成对的目标域图像，大幅提升数据效率。

**阶段二：残差扩散（Residual Diffusion）**。在阶段一结束后的固定噪声水平上，确定性注入源-目标残差 $I_{\mathrm{res}} = I_{\mathrm{source}} - I_{\mathrm{target}}$：

$$I_t^{(2)} = I_0^{(2)} + \bar{\alpha}_t I_{\mathrm{res}}$$

其中 $I_0^{(2)} = I_{T_1}^{(1)}$ 为阶段一终点处的含噪目标图像，$\bar{\alpha}_t$ 为残差注入的确定性调度系数。该阶段在噪声域内完成目标到源的语义映射，由于噪声的域协调效应仍在保持，分布间隙已被缩小，核心映射的学习难度显著降低。

### 3.3 逆向过程：先残差消除，后去噪

与两阶段前向过程严格对应，逆向过程同样解耦为两个独立阶段：

**阶段一：残差消除（Residual Removal）**。从含噪含残差的中间状态 $I_{T_2}^{(2)}$ 出发，逐步消除残差，恢复出含噪目标图像。单步逆向更新为：

$$I_{t-1}^{(2)} = I_t^{(2)} - \alpha_t I_{\mathrm{res}}^{\theta}(I_t^{(2)}, I_{\mathrm{in}}, t)$$

其中 $I_{\mathrm{res}}^{\theta}$ 为残差预测网络，以当前含噪含残差图像 $I_t^{(2)}$、输入源图像 $I_{\mathrm{in}}$ 和时间步 $t$ 为条件，预测当前步应消除的残差量。该阶段结束时，残差被完全消除，得到含噪目标图像 $I_0^{(2)}$，此时**噪声的域协调效应得以完整保留**。

**阶段二：去噪（Denoising）**。从含噪目标图像 $I_0^{(2)}$（即 $I_{T_1}^{(1)}$）出发，逐步去除高斯噪声，生成最终清晰目标图像。单步去噪更新为：

$$I_{t-1}^{(1)} = I_t^{(1)} - (\bar{\beta}_t - \sqrt{\bar{\beta}_{t-1}^2 - \sigma_t^2}) \epsilon_{\theta}(I_t^{(1)}, t) + \sigma_t \varepsilon_t$$

其中 $\epsilon_{\theta}$ 为噪声预测网络，$\sigma_t$ 控制采样的随机性（$\eta=0$ 时为确定性DDIM采样，$\eta=1$ 时为随机DDPM采样）。该阶段仅需从含噪目标恢复到清晰目标，不涉及跨域语义映射。

### 3.4 训练目标

两个阶段分别训练独立的网络，损失函数均采用L1范数：

**残差消除损失**：

$$\mathcal{L}_{\mathrm{res}}(\theta) = \mathbb{E}\left[\|I_{\mathrm{res}} - I_{\mathrm{res}}^{\theta}(I_t^{(2)}, t, I_{\mathrm{in}})\|_1\right]$$

该损失监督残差预测网络在任意时间步 $t$ 准确估计当前含噪含残差图像中的残差分量。$I_{\mathrm{res}} = I_{\mathrm{source}} - I_{\mathrm{target}}$ 为真实残差。

**去噪损失**：

$$\mathcal{L}_{\epsilon}(\theta) = \mathbb{E}\left[\|\epsilon - \epsilon_{\theta}(I_t^{(1)}, t)\|_1\right]$$

该损失监督噪声预测网络在任意时间步 $t$ 准确估计含噪目标图像中的高斯噪声分量。$\epsilon$ 为真实注入噪声。

两个网络独立训练：噪声预测网络仅使用非成对目标域图像，残差预测网络使用成对源-目标图像。这种解耦训练策略使得数据需求大幅降低——噪声扩散/去噪阶段可利用海量无标注目标域图像，仅残差扩散/消除阶段需要成对数据。



## 实验与关键发现

### 核心实验设置

DRDD 的去噪网络采用 U-Net 架构，通道深度 C=64，通道乘子为 (1, 2, 4, 8)。推理阶段统一使用 DDIM 采样策略，去噪与残差消除两阶段的采样步长均设为 2。所有对比方法在相同基准数据集上以标准指标（SSIM、LPIPS、FID、PSNR）进行评估。

### 统一多任务图像复原主结果

**All-in-One-5 基准**（Table 1）涵盖五种统一多任务图像复原场景。DRDD 在平均 SSIM 0.916、LPIPS 0.073、FID 18.3 上全面超越近期 SOTA 方法，感知指标优势尤为突出——相比基于扩散的基线（如 **RDDM**、**I2SB**、**IR-SDE**），DRDD 在 LPIPS 和 FID 上取得显著提升，验证了解耦设计对生成质量的关键作用。

**CDD-11 基准**（Figure 3）包含 11 种退化任务及其平均。DRDD 在所有退化类型上一致超越近期 SOTA 模型，尤其在复合退化场景（如低光+模糊+噪声）中优势明显，取得最高平均 SSIM。这表明噪声域内的残差映射有效保留了域协调效应，使单一模型能够灵活应对多样化的退化组合。

**多域去噪（MNMD）**（Table 2）覆盖自然、医学、遥感三个域。DRDD 在三个域上均取得最高 SSIM 和最低 LPIPS：自然域 0.9391/0.0492，医学域 0.9324/0.0629，遥感域 0.9300/0.0539。该结果直接支持 Proposition 3.1 的域协调理论——高斯噪声注入缩小了跨域分布间的 KL 散度，使解耦框架天然适配多域统一建模。

### 消融实验

**解耦 vs. 耦合 SDE**（Table 3）在单任务 I2I（人脸修复 CelebA-HQ、去雨 Rain100、去噪 BSD400）上对比了解耦 SDE 与传统耦合 SDE 方法。解耦 SDE 在图像修复和去雨任务上一致优于耦合 SDE，且 FID 指标更好，证实解耦结构本身——而非额外的模型容量——是性能增益的核心来源。

**噪声注入强度**（Figure 6）在 All-in-One-5 上扫描了不同噪声水平。最优注入强度约为 1.0，且在 0.8–1.3 范围内性能保持稳定，说明方法对噪声超参数不敏感，鲁棒性强。

**数据效率**（Figure 5）在 All-in-One-3 和低光增强数据集上进行数据剪枝实验。当训练数据从 100% 降至 25% 时，DRDD 的性能下降远小于 RDDM、I2SB 等耦合扩散方法。这一优势源于噪声扩散/去噪阶段仅需非成对目标域图像训练，大幅降低了对成对数据的依赖——在数据稀缺场景下，解耦框架的独立去噪模块仍能维持生成质量。

### 可视化结果

Figure 4 展示了低光增强（LoLV1）、模糊复原（GoPro）、人脸修复（CelebA-HQ）、超分辨率（FFHQ）等任务的视觉对比。DRDD 在纹理恢复和伪影抑制上表现更优，与感知指标的领先一致。

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/005_Figure_4.jpg]]
*Figure 4: Visual results of state-of-the-art methods and our proposed DRDD. (a) Comparison of low-light enhancement results on the LoLV1 dataset [61]. (b) Comparison of blur restoration results on the GoPro dataset [44]. (c) Face inpainting results (center and irregular mask) in CelebA-HQ [19]. (d) Super-Resolution result in FFHQ [20]. Zoom in for best view. More visual results are provided in Appendix D*

### 失败模式与局限

论文未明确报告失败模式或局限性分析。从方法设计推断，潜在风险包括：当源-目标域间隙极大时，固定噪声域内的残差映射可能不足以完整刻画语义变换；两阶段解耦增加了推理步数，可能影响实时性。这些推断需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/003_Table_1.jpg]]
*Table 1: Performance comparisons of five unified multi-task image restoration tasks on All-in-One-5 dataset [8]. Denoising results are reported at the noise level σ = 25. SSIM (↑), LPIPS (↓) and FID (↓) are reported. Best results are highlighted in red, while the second-best results are blue. Diffusion-based methods are denoted by “*”. Our DRDD demonstrates superior or competitive performance compared to recent models, especially in perceptual metrics. Due to space limitation, PSNR results and computational costs are provided in Appendix C.5*

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/004_Figure_3.jpg]]
*Figure 3: Quantitative comparison to state-of-the-art on 11 degradation tasks and their average. SSIM (↑) is reported. Our DRDD method consistently outperforms recent SOTA models, with favorable results in complex composited degradation scenarios. All experiments are conducted on the CDD11 dataset [15]*

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/006_Table_2.jpg]]
*Table 2: Performance comparison of several methods on MNMD dataset. Best results are highlighted in Bold*

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/007_Figure_5.jpg]]
*Figure 5: Data Pruning on All-in-One-3 [8] and Low-Light dataset. SSIM (↑) and LPIPS (↓) are reported. As the training data decreases, DRDD’s performance drop is much smaller than other methods*

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/008_Table_3.jpg]]
*Table 3: Performance comparison of decoupled and coupled SDEbased diffusion methods on single task I2I. Results are evaluated on the CelebA-HQ [19], Rain100 [49], and BSD400 [2] datasets*

![[assets/figures/papers/paper_list_l855_https_openaccess_thecvf_com_content_CVPR2026_html_Lin_Decoupled_Residual/figures/009_Figure_6.jpg]]
*Figure 6: Performance comparison on the All-in-One-5 dataset[8] under varying noise injection level*



## 定位与知识库关联

### 与耦合残差扩散模型的演进关系

DRDD 直接继承自残差去噪扩散模型（Residual Denoising Diffusion Models, RDDM）的架构范式。RDDM（Liu et al., 2024）首次将图像到图像（I2I）翻译建模为残差扩散过程，在逆向阶段同时完成去噪与残差消除。然而，这一耦合设计存在根本性瓶颈：逆向过程中残差的逐步消除会过早削弱噪声带来的域协调效应，使得模型难以在统一框架下处理多种 I2I 任务。

DRDD 的核心突破在于将这一耦合过程彻底解耦为两个顺序独立阶段：**噪声扩散**与**残差扩散**。在正向过程中，先执行随机噪声扩散实现域协调和流形提升，再在固定噪声域内完成确定性的残差注入；逆向时则先消除残差——在噪声域内完成核心语义映射——最后执行去噪。这一解耦设计的关键洞察在于：**高斯噪声不仅是流形提升的工具，还充当“域协调器”**，在核心语义变换完成前保持噪声效应，能够隐式拉近不同域之间的分布距离。

与 I2SB（Liu et al., 2023）和 IR-SDE（Luo et al., 2023）等扩散基线方法相比，DRDD 在三个关键维度上实现了结构性改进：

| 维度 | 耦合扩散基线（RDDM/I2SB/IR-SDE） | DRDD 解耦设计 |
|------|--------------------------------|--------------|
| **扩散过程结构** | 单一耦合逆向过程同时去除噪声和残差 | 解耦为顺序的噪声扩散/残差扩散两阶段，逆向时先残差消除后去噪 |
| **噪声的角色** | 仅用于流形提升和训练信号增强 | 额外作为域协调器，在核心映射完成前保持噪声以拉近域分布 |
| **训练数据需求** | 整体过程依赖成对源-目标图像训练 | 噪声扩散/去噪阶段仅使用非成对目标域图像，显著提升数据效率 |

### 域协调的理论基础

DRDD 的域协调机制具有严格的理论支撑。**Proposition 3.1** 证明了注入高斯噪声能够缩小不同分布之间的 KL 散度：

$$D_{KL}(P_{\sigma} \parallel Q_{\sigma}) < D_{KL}(P \parallel Q)$$

这一命题揭示了一个此前被忽视的现象：高斯噪声注入后，原本分离的源域和目标域分布在特征空间中显著靠拢（如 **Figure 1** 的 t-SNE 可视化所示）。传统的耦合扩散模型在逆向过程中同时移除噪声和残差，实际上过早地破坏了这一协调效应；而 DRDD 通过将残差消除阶段完全置于噪声域内，最大化了域协调带来的学习便利性。

### 统一 I2I 翻译的能力边界

DRDD 在统一多任务 I2I 翻译场景下展现了全面的性能优势。在 **All-in-One-5** 基准上，DRDD 在去噪、去雨、低光增强、去模糊和图像修复五项任务的平均 SSIM 达 0.916，LPIPS 为 0.073，FID 为 18.3，全面超越近期 SOTA 方法，尤其在感知指标上优势突出（**Table 1**）。在 **CDD-11** 的 11 种退化任务上，DRDD 在所有退化类型上一致超越对比方法，在复合退化场景中优势尤为明显（**Figure 3**）。

跨域泛化能力方面，**MNMD** 多域去噪基准（**Table 2**）显示 DRDD 在自然图像（SSIM 0.9391/LPIPS 0.0492）、医学图像（0.9324/0.0629）和遥感图像（0.9300/0.0539）三个截然不同的域上均取得最优结果，验证了解耦框架对域偏移的鲁棒性。

### 数据效率与鲁棒性

DRDD 的一个显著优势在于其数据效率。由于噪声扩散和去噪阶段仅需非成对目标域图像，DRDD 对成对训练数据的依赖大幅降低。**Figure 5** 的数据剪枝实验表明，当训练数据从 100% 降至 25% 时，DRDD 的性能下降远小于 RDDM、I2SB 等方法。这一特性源于解耦设计：核心的语义映射（残差扩散/消除）在噪声协调后的简化域内进行，即使成对样本稀少，学习难度也显著降低。

### 消融验证的关键发现

**Table 3** 在单任务 I2I 设定下直接比较了解耦 SDE 与耦合 SDE 的性能。在 CelebA-HQ 人脸修复、Rain100 去雨和 BSD400 去噪任务上，解耦框架在 SSIM 和 FID 上均一致优于耦合方案，证实解耦本身——而非其他架构因素——是性能提升的核心驱动力。

**Figure 6** 的噪声注入水平消融实验揭示了域协调效应的最优区间：噪声注入强度约 1.0 时性能最佳，且在 0.8–1.3 范围内保持稳定。过低的噪声不足以有效协调域分布，过高则可能淹没图像细节信息，这一发现为实际部署中的超参数选择提供了明确指导。

### 局限与开放问题

尽管 DRDD 在统一 I2I 翻译和数据效率方面取得了显著进展，当前论文未明确讨论其局限性。基于方法设计的分析，以下几点值得关注并需要进一步验证：

1. **推理效率**：解耦框架在逆向过程中需要依次执行残差消除和去噪两个阶段，虽然每个阶段采用 DDIM 采样（步长设为 2）加速，但整体采样步骤仍多于单阶段方法。论文提及计算成本数据见附录 C.5，但正文未给出具体推理时间对比，此点需查阅附录确认。

2. **极端域偏移场景**：域协调机制依赖于高斯噪声注入对分布的拉近效应。当源域和目标域之间的差异极大（如医学图像到自然图像的跨模态翻译）时，仅靠噪声注入是否足以有效协调域分布，论文未提供消融证据。

3. **噪声注入强度的任务依赖性**：Figure 6 显示最优噪声强度在 All-in-One-5 上约为 1.0，但不同任务（如低光增强 vs. 去模糊）对噪声强度的敏感度可能存在差异，论文未提供逐任务的噪声消融分析。

4. **与最新生成式基线的对比**：Table 1 对比的方法列表截至投稿时，随着扩散模型和生成式方法的快速演进，与后续出现的更强基线（如基于 flow matching 或 consistency model 的统一框架）的性能关系有待后续工作验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Decoupled_Residual_Denoising_Diffusion_Models_for_Unified_and_Data_Efficient_Image_to_Image_Translation.pdf]]
