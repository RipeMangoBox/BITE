---
title: "Improving 2D Diffusion Models for 3D Medical Imaging with Inter‑Slice Consistent Stochasticity"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Improving_2D_Diffusion_Models_for_3D_Medical_Imaging_with_InterSlice_Consistent_Stochasticity.pdf
openreview_forum_id: R5ETdN6ifA
aliases:
- ISCSI
- I2DM3MIISCS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "扩散采样重加噪步骤中注入的随机噪声的跨切片相关性。通过将该噪声从独立同分布的高斯噪声替换为沿超球面测地线平滑插值的相关噪声，可直接对齐相邻切片的采样轨迹，从根源上增强3D体积的层间一致性。"
primary_logic: "利用高维高斯分布概率质量集中在超球面薄壳上的浓度现象，采用球面线性插值（Slerp）在锚点噪声向量之间构建测地路径，生成既能满足每切片标准高斯分布又具有自然层间衰减相关性的噪声体积，从而在不引入额外损失项、超参数或计算开销的前提下，将2D扩散先验无缝提升为3D一致的生成过程。"
claims:
- "ISCS通过同步扩散采样中随机噪声组件并采用平滑插值，在不增加新损失项或优化步骤的情况下对齐采样轨迹。"
- "ISCS使用球面线性插值在超球面上生成平滑相关的噪声体积，从而在保持每切片分布统计特性的同时实现层间相关性控制。"
- "DDS+ISCS在SVCT、LACT和MRI SR三个任务上均取得了最佳的PSNR/SSIM和最低的LPIPS，且层间差异指标|Δ|最小。"
- "ISCS (Slerp噪声) 显著优于BCS (相同噪声)，后者会引入条状伪影，而ISCS保持自然层间过渡。"
---

# Improving 2D Diffusion Models for 3D Medical Imaging with Inter‑Slice Consistent Stochasticity

> [!tip] 核心洞察
> 利用高维高斯分布概率质量集中在超球面薄壳上的浓度现象，采用球面线性插值（Slerp）在锚点噪声向量之间构建测地路径，生成既能满足每切片标准高斯分布又具有自然层间衰减相关性的噪声体积，从而在不引入额外损失项、超参数或计算开销的前提下，将2D扩散先验无缝提升为3D一致的生成过程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于切片间一致随机性的改进2D扩散模型用于3D医学成像 |
| 英文题名 | Improving 2D Diffusion Models for 3D Medical Imaging with Inter‑Slice Consistent Stochasticity |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=R5ETdN6ifA); [GitHub](https://github.com/duchenhe/ISCS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Inter-Slice Consistent Stochasticity (ISCS) |
| Dataset | SVCT (30 views), LACT ([0,100]°), MRI SR (5×), SVCT (30 views) - 层间差异 |

> [!tip] 效果简介
> - SVCT (30 views) 上，PSNR (Axial) 为 36.97，对比 34.76 (DDS)，变化 +2.21。
> - LACT ([0,100]°) 上，PSNR (Axial) 为 31.65，对比 29.07 (DDS)，变化 +2.58。
> - MRI SR (5×) 上，PSNR (Axial) 为 40.33，对比 39.32 (DDS)，变化 +1.01。

## 概述

**核心问题**：在3D医学成像（如稀疏CT重建、有限角CT、MRI超分辨率）中，直接使用逐切片的2D扩散模型作为生成先验会导致严重的层间结构不连续。其根本原因在于：反向扩散采样过程中，每个切片的随机噪声独立采样，而高度欠定的测量无法提供足够的层间约束，使得相邻切片的采样轨迹完全不相关。

**方法定位**：本文提出**Inter‑Slice Consistent Stochasticity (ISCS)**，一种即插即用的策略，通过控制扩散采样中随机噪声组件的跨切片一致性来对齐采样轨迹。ISCS 利用高维高斯分布概率质量集中在超球面薄壳上的浓度现象，采用球面线性插值（Slerp）在锚点噪声向量之间沿测地线生成平滑相关的噪声体积，从而在不引入任何额外损失项、优化步骤或模型重训练的前提下，将2D扩散先验无缝提升为3D一致的生成过程。

**方法谱系与知识库定位**：ISCS 构建于基于扩散模型的逆问题求解框架之上，其基础流程（去噪预测→数据保真更新→重加噪）继承自 **DDS**（Chung et al., arXiv 2024）。与依赖显式3D先验的方法（如利用正交平面一致性的 **TPDM**（Lee et al., MICCAI 2023）或多平面融合的 **DiffusionBlend**（Song et al., 2024））不同，ISCS 仅修改重加噪步骤中的噪声注入方式，无需模型架构变更或联合训练。与施加完全相同噪声的批一致采样策略 **BCS**（Kwon & Ye, CVPR 2025）相比，ISCS 通过 Slerp 插值保留了层间噪声的平滑过渡，避免了“复制伪影”。

**主要结果**：在稀疏CT（30视角）、有限角CT（[0,100]°）和MRI 5×超分辨率三个任务上，DDS+ISCS 在轴向/冠状/矢状面的 PSNR、SSIM 和 LPIPS 上均取得最优结果，且层间差异指标 |Δ| 显著低于所有对比方法。消融实验证实：Slerp 噪声策略在辅助视图质量上全面超越 BCS 的相同噪声策略；方法对锚点选择、切片厚度变化和随机性强度均表现出高度鲁棒性；在病理保留方面，ISCS 能够清晰保留小病灶的边界和内部纹理，而 TV 正则化可能导致病灶模糊或消失。

## 背景与动机

### 3D医学成像中的逆问题与2D扩散先验的困境

三维医学成像——包括稀疏视图CT（SVCT）、有限角度CT（LACT）和MRI各向同性超分辨率（SR）——本质上都是高度病态的逆问题：从欠定的测量 $\mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{n}$ 中恢复三维体积 $\mathbf{x}$。近年来，基于扩散模型（Diffusion Model）的逆问题求解器（如 **DDNM**，Wang et al., arXiv 2022；**DDS**，Chung et al., arXiv 2024）展现出强大的重建能力，其核心思路是利用预训练的2D扩散模型作为生成先验，通过迭代交替执行去噪预测、数据保真更新和重加噪三个步骤来逼近真实解。

然而，这类方法面临一个根本性瓶颈：**它们将3D体积视为一组独立的2D切片，逐切片进行扩散采样**。具体而言，在重加噪步骤中，每个切片注入的是独立同分布的高斯噪声 $\epsilon_i \sim \mathcal{N}(0, \mathbf{I})$。由于医学成像的逆问题高度欠定，测量数据提供的层间约束极为有限，这些独立噪声导致相邻切片的反向扩散采样轨迹完全不相关。结果是，重建体积在冠状面和矢状面上出现严重的层间结构不连续和伪影——这一缺陷在辅助视图的定量指标（PSNR、SSIM、LPIPS）中暴露无遗。

### 现有补救措施的局限

为缓解层间不一致，现有工作主要采取两类策略：

**后处理正则化**：在逐切片扩散重建后施加全变分（TV）等正则化项（如 **DDS+TV**）。这种方法虽然能平滑层间过渡，但本质上是在重建完成后“修补”不一致，而非从根源上解决问题。更重要的是，TV正则化倾向于过度平滑，可能导致小病灶模糊甚至消失（见Figure 6），这在医学诊断中不可接受。

**显式3D感知方法**：如 **TPDM**（Lee et al., MICCAI 2023）利用正交平面的一致性约束，**DiffusionBlend**（Song et al., 2024）融合多平面2D先验。这些方法引入了额外的模型组件、优化步骤或超参数，增加了复杂度和计算开销，且往往需要针对特定任务进行调参。

### 核心洞察与本文动机

本文的关键洞察在于：**层间不一致的根源并非扩散先验本身的能力不足，而是重加噪步骤中随机噪声的跨切片独立性**。扩散模型的采样过程可分解为确定性分量和随机噪声分量两部分（见Eq. (8)）。确定性分量由测量一致性约束主导，而随机噪声分量则控制着采样轨迹的探索方向。当每个切片的随机噪声独立采样时，它们的采样轨迹在高维空间中发散，最终呈现为体积的层间不连续。

因此，本文提出一个根本性的问题重塑：**如果能在保持每切片噪声统计特性（标准高斯分布）的前提下，使相邻切片的随机噪声具有平滑的相关性，能否在不引入任何额外损失项、优化步骤或模型重训练的情况下，从根本上对齐采样轨迹，实现3D一致的生成过程？**

这一动机催生了本文的核心方法——**切片间一致随机性（Inter-Slice Consistent Stochasticity, ISCS）**：一种即插即用的策略，通过在高维高斯分布的概率质量集中区域——超球面薄壳上——沿测地线进行球面线性插值（Slerp），生成既满足每切片标准高斯分布又具有自然层间衰减相关性的噪声体积，从而将2D扩散先验无缝提升为3D一致的生成过程。

## 核心创新

本文的核心创新在于提出了一种名为**层间一致随机性（Inter-Slice Consistent Stochasticity, ISCS）**的即插即用策略，从根本上解决了将2D扩散先验应用于3D医学成像逆问题时，因逐切片独立采样而导致的层间结构不连续问题。

该方法的创新点并非引入新的网络架构、损失函数或复杂的3D先验建模，而是对扩散采样过程中的一个基本组件——**重加噪步骤中注入的随机噪声**——进行了巧妙的重新设计。其核心洞察可分解为以下三个关键创新维度：

### 1. 问题根源的重新定位：从“先验不足”到“随机性失配”

传统方法将2D扩散先验在3D重建中的层间不一致归咎于先验本身缺乏3D感知能力，因此尝试通过添加TV正则化（如 **DDS+TV**）、融合多平面先验（如 **DiffusionBlend**, Song et al., 2024）、或利用正交平面一致性（如 **TPDM**, Lee et al., MICCAI 2023）来弥补。ISCS则揭示了一个更深层的机制：**在高度欠定的逆问题中，欠定测量无法提供足够的层间约束，而反向扩散过程中每个切片独立采样的随机噪声导致相邻切片的采样轨迹完全不相关，这是层间伪影的根本原因**。这一洞察将问题的焦点从先验设计转移到了采样过程的随机性控制上。

### 2. 噪声注入方式的根本性变革：从独立同分布到超球面测地线插值

这是ISCS最核心的changed slot。基线方法（如**DDS**, Chung et al., arXiv 2024）在反向采样的重加噪步骤中，为每个切片独立采样高斯噪声 $\epsilon_i \sim \mathcal{N}(0, \mathbf{I})$，导致相邻切片噪声完全无关。ISCS将其替换为一种**结构化的相关噪声体积 $\epsilon^{\mathrm{ISCS}}$**，生成方式如下：

- **理论基础**：利用高维高斯分布的浓度现象（Gaussian Annulus Theorem, Eq. (10)），即概率质量集中在半径为 $\sqrt{d}$ 的超球面薄壳上，因此噪声向量的方向比幅度更具信息量。
- **生成机制**：随机采样两个锚点噪声向量 $\mathbf{z}_1, \mathbf{z}_S$，通过**球面线性插值（Slerp）**在超球面上沿测地线生成中间切片的噪声：
  $$\epsilon_i^{\mathrm{ISCS}} = \mathrm{slerp}(\mathbf{z}_1, \mathbf{z}_S; \alpha_i) = \frac{\sin((1-\alpha_i)\Omega)}{\sin(\Omega)}\mathbf{z}_1 + \frac{\sin(\alpha_i\Omega)}{\sin(\Omega)}\mathbf{z}_S$$
  其中 $\alpha_i$ 为第 $i$ 个切片的归一化位置参数，$\Omega$ 为两锚点向量的夹角。

这一设计的精妙之处在于：它**既保证了每个切片噪声仍服从标准高斯分布（满足扩散模型的统计要求），又使相邻切片的噪声自然相关、远端切片的相关性平滑衰减**，从而对齐了采样轨迹。与**批一致采样（BCS, Kwon & Ye, CVPR 2025）**对所有切片施加完全相同噪声的策略相比，ISCS避免了过度刚性约束导致的“复制伪影”（Table 2, Figure 4），在冠状面和矢状面的LPIPS上分别取得0.074 vs 0.081和0.101 vs 0.112的显著优势。

### 3. 一致性的内在化：无需外部正则化的即插即用设计

ISCS的另一个关键创新在于其**零成本集成**的特性。与需要在扩散采样后额外添加TV正则化项（如DDS+TV）或需要重新训练3D模型的方法不同，ISCS将层间一致性直接内化到了采样过程中：

- **无需额外损失项或优化步骤**：ISCS仅修改了重加噪步骤中的噪声注入方式（Algorithm 1, Steps 9-10），不引入任何新的超参数或正则化项。
- **无需模型重训练或架构修改**：可直接集成到任意基于2D扩散的逆问题求解器（如DDNM、DDS）中，使用相同的预训练2D扩散先验。
- **计算开销可忽略**：Slerp插值的计算量相对于扩散模型的推理开销几乎可以忽略。

实验证据有力地支持了这一设计的有效性：DDS+ISCS在SVCT（30视图）上将轴向PSNR从34.76提升至36.97（+2.21 dB），在LACT（[0,100]°）上从29.07提升至31.65（+2.58 dB），同时将层间差异指标 $|\Delta|$ 从0.005588降至0.001835（SVCT）和从0.011592降至0.001966（LACT），达到了与真实值最为接近的层间一致性（Table 1, Table 3）。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/004_Figure_1.jpg]]
*Figure 1: Geometric interpretation of how different noise strategies in the re-noising step affect the stochasticity and resulting consistency in diffusion sampling. (a) Independent Noise (Conventional): Independently sampled noise for each slice, leading to uncorrelated sampling paths. (b) Identical Noise (BCS (Kwon & Ye, 2025)): Applying the same noise to all slices forces identical sampling paths. (c) Slerp Noise (Ours): Our proposed ISCS interpolates noise on the hypersphere, generating smoothly correlated information across slices*

### 问题定位与核心矛盾

在3D医学成像重建（如稀疏CT、有限角CT、MRI超分辨率）中，直接训练3D扩散模型面临数据稀缺和计算资源高昂的双重困境。因此，主流做法是将预训练的2D扩散模型逐切片（slice‑wise）应用于3D体积，即对每个轴向切片独立执行扩散逆问题求解（Diffusion Inverse Solver, DIS）。然而，这一策略引入了一个根本性瓶颈：**每个切片的扩散反向采样过程各自注入独立同分布的高斯噪声，导致相邻切片的采样轨迹完全不相关**。在测量信息高度欠定的条件下，数据保真项无法提供足够的层间约束来弥合这种差异，最终表现为冠状面和矢状面上的严重条纹伪影与结构不连续。

### ISCS 的整体设计思路

针对上述矛盾，本文提出 **切片间一致随机性（Inter‑Slice Consistent Stochasticity, ISCS）**，一种即插即用（plug‑and‑play）的策略。其核心思想是：**直接操控扩散采样重加噪步骤中注入的随机噪声的跨切片相关性**，从而在根源上对齐各切片的采样轨迹，而无需引入任何额外的损失项、超参数调优或模型重训练。

ISCS 的整体流程可概括为三步迭代：

1. **去噪预测（Denoising Prediction）**：利用 Tweedie 公式从当前噪声状态 $\mathbf{x}_t$ 预测清洁图像 $\mathbf{x}_{0\mid t}$。
2. **数据保真更新（Data Fidelity Update）**：通过求解测量一致性的邻近优化问题，获得与采集数据 $\mathbf{y}$ 一致的校正估计 $\hat{\mathbf{x}}_{0\mid t}$。
3. **ISCS 重加噪（Re‑noising via ISCS）**：使用球面线性插值（Slerp）生成层间相关的噪声体积 $\boldsymbol{\epsilon}^{\mathrm{ISCS}}$，并执行 DDIM 风格的反向重加噪，得到下一时间步的状态 $\mathbf{x}_{t-1}$。

### 噪声相关性的几何实现

ISCS 的关键技术路径建立在**高维高斯分布的浓度现象（Gaussian Annulus Theorem）**之上：各向同性高维高斯向量的范数以极高概率集中在半径 $\sqrt{d}$ 的超球面薄壳上。因此，ISCS 抛弃了“每切片独立采样”或“所有切片强制相同噪声”的两种极端策略，转而**在超球面测地线上进行球面线性插值（Slerp）**：

- 首先在超球面上随机采样两个锚点噪声向量 $\mathbf{z}_1, \mathbf{z}_S$（分别对应首尾切片）；
- 对于第 $i$ 个切片，沿 $\mathbf{z}_1$ 与 $\mathbf{z}_S$ 之间的测地路径取插值系数 $\alpha_i$，生成该切片的噪声 $\boldsymbol{\epsilon}_i^{\mathrm{ISCS}}$；
- 相邻切片的噪声高度相关，远端切片的相关性自然衰减，形成**平滑过渡的噪声体积**。

这一设计既保证了每切片噪声仍服从标准高斯分布（统计特性不变），又赋予了噪声体积天然的层间衰减相关性，从几何根源上对齐了相邻切片的扩散采样轨迹。

### 与基线方法的对比定位

| 噪声策略 | 机制 | 层间一致性 | 缺陷 |
|----------|------|-----------|------|
| 独立噪声（常规2D DIS） | 每切片独立采样 $\boldsymbol{\epsilon}_i \sim \mathcal{N}(0,\mathbf{I})$ | 无 | 冠状/矢状面条纹伪影严重 |
| 相同噪声（BCS, Kwon & Ye, CVPR 2025） | 所有切片注入完全相同的噪声 | 过强 | 引入“复制伪影”，抑制解剖结构变化 |
| **ISCS（本文）** | 超球面 Slerp 插值生成相关噪声 | 适度且平滑 | 无明显伪影，保留自然层间过渡 |

ISCS 可无缝集成到任意基于2D扩散的逆问题求解器（如 **DDNM** (Wang et al., arXiv 2022)、**DDS** (Chung et al., arXiv 2024)）中，仅需将重加噪步骤中的独立噪声 $\boldsymbol{\epsilon}$ 替换为 $\boldsymbol{\epsilon}^{\mathrm{ISCS}}$，不改变网络架构、不增加推理计算量、不需要后处理正则化。

## 核心模块与公式推导

### 3.1 问题根源：逐切片独立随机性导致的层间不一致

当使用逐切片的2D扩散先验进行3D医学成像重建时，反向扩散过程中每个轴向切片独立采样随机噪声，导致相邻切片的采样轨迹完全不相关。在高度欠定的逆问题（如稀疏视角CT、有限角度CT）中，测量数据无法提供足够的层间约束来弥合这种随机性分歧，最终表现为冠状面和矢状面的层间结构不连续和条纹伪影。

形式上，对于包含 $S$ 个切片的3D体积 $\mathbf{x} \in \mathbb{R}^{S \times H \times W}$，逐切片去噪近似为：

$$
\tilde{\boldsymbol{\epsilon}}_{\theta}(\mathbf{x}_t) := [\epsilon_{\theta}(\mathbf{x}_{t,1}), \epsilon_{\theta}(\mathbf{x}_{t,2}), \dots, \epsilon_{\theta}(\mathbf{x}_{t,S})] \tag{9}
$$

其中每个 $\mathbf{x}_{t,i}$ 是第 $i$ 个切片的当前噪声状态，$\epsilon_{\theta}$ 是预训练的2D去噪网络。在标准DDIM重加噪步骤中，每个切片注入独立同分布的高斯噪声 $\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$：

$$
\mathbf{x}_{t-1} = \sqrt{\bar{\alpha}_{t-1}}\hat{\mathbf{x}}_{0\mid t} + \sqrt{1 - \bar{\alpha}_{t-1} - \eta^2\tilde{\beta}_t^2}\boldsymbol{\epsilon}_{\theta^*}^{(t)}(\mathbf{x}_t) + \eta\tilde{\beta}_t\boldsymbol{\epsilon} \tag{8}
$$

其中 $\hat{\mathbf{x}}_{0\mid t}$ 是通过邻近优化获得的数据一致估计，$\eta$ 控制随机性强度。正是最后一项中 $\boldsymbol{\epsilon}$ 的切片间独立性构成了层间不一致的根本原因。

### 3.2 ISCS核心机制：超球面测地线插值的相关噪声生成

ISCS的核心思想是将重加噪步骤中的独立噪声 $\boldsymbol{\epsilon}$ 替换为一个沿 $z$ 轴平滑变化的相关噪声体积 $\boldsymbol{\epsilon}^{\mathrm{ISCS}}$，从而直接对齐相邻切片的采样轨迹。

**理论依据**：高维各向同性高斯分布的概率质量高度集中在半径为 $\sqrt{d}$ 的超球面薄壳上，这一性质由Gaussian Annulus定理刻画：

$$
\mathbb{P}\big(|||\boldsymbol{z}||_2 - \sqrt{d}| \geq \beta\big) \leq 2 \exp(-c\beta^2) \tag{10}
$$

这意味着高维高斯随机向量几乎位于超球面上。因此，在超球面上而非欧氏空间中进行插值，能够保留每个切片噪声向量的范数和分布统计特性。

**Slerp噪声生成**：ISCS首先独立采样两个锚点噪声向量 $\mathbf{z}_1, \mathbf{z}_S \sim \mathcal{N}(0, \mathbf{I})$，分别对应第一个和最后一个切片。对于第 $i$ 个切片，其相关噪声 $\boldsymbol{\epsilon}_i^{\mathrm{ISCS}}$ 通过球面线性插值（Slerp）生成：

$$
\boldsymbol{\epsilon}_i^{\mathrm{ISCS}} = \mathrm{slerp}(\mathbf{z}_1, \mathbf{z}_S; \alpha_i) = \frac{\sin((1-\alpha_i)\Omega)}{\sin(\Omega)}\mathbf{z}_1 + \frac{\sin(\alpha_i\Omega)}{\sin(\Omega)}\mathbf{z}_S \tag{11}
$$

其中 $\alpha_i = (i-1)/(S-1)$ 是归一化的切片位置，$\Omega = \arccos(\langle \mathbf{z}_1, \mathbf{z}_S \rangle / \|\mathbf{z}_1\|\|\mathbf{z}_S\|)$ 是两锚点向量在超球面上的夹角。该插值沿测地线路径生成中间噪声向量，保证相邻切片的噪声高度相关，而远端切片的相关性自然衰减。

**集成到反向采样**：将生成的 $\boldsymbol{\epsilon}^{\mathrm{ISCS}}$ 直接替换标准DDIM重加噪步骤中的独立噪声项：

$$
\mathbf{x}_{t-1} = \sqrt{\bar{\alpha}_{t-1}}\hat{\mathbf{x}}_{0\mid t} + \sqrt{1-\bar{\alpha}_{t-1}-\sigma_t^2} \cdot \boldsymbol{\epsilon}_{\theta}(\mathbf{x}_t) + \sigma_t \cdot \boldsymbol{\epsilon}^{\mathrm{ISCS}} \tag{12}
$$

其中 $\sigma_t = \eta\tilde{\beta}_t$ 控制随机噪声的强度。该替换无需引入额外损失项、超参数或模型重训练，可直接嵌入任意基于2D扩散的逆问题求解器。

### 3.3 与BCS（相同噪声策略）的本质区别

BCS（Batch-Consistent Sampling）对所有切片施加完全相同的噪声 $\boldsymbol{\epsilon}^{\mathrm{BCS}} = \mathbf{z}_1$，迫使所有切片的采样轨迹完全相同。这在医学体积中构成过度刚性约束——它压制了相邻切片间应有的解剖结构渐变，导致特征被不当地跨切片复制，产生“复制伪影”（copying artifacts）。ISCS通过Slerp插值实现平滑过渡，在保持层间一致性的同时保留了自然的层间解剖变化。

### 3.4 算法流程

完整的ISCS增强重建流程包含三个迭代模块：

1. **去噪预测**（Tweedie公式）：利用当前噪声状态 $\mathbf{x}_t$ 和预训练网络预测清洁图像 $\mathbf{x}_{0\mid t}$：
   $$
   \mathbf{x}_{0\mid t} = \frac{1}{\sqrt{\bar{\alpha}_t}}(\mathbf{x}_t - \sqrt{1-\bar{\alpha}_t}\boldsymbol{\epsilon}_{\theta^*}(\mathbf{x}_t)) \tag{6}
   $$

2. **数据保真更新**：通过求解邻近优化问题获得与测量 $\mathbf{y}$ 一致的估计 $\hat{\mathbf{x}}_{0\mid t}$：
   $$
   \hat{\mathbf{x}}_{0\mid t} = \underset{\mathbf{z}}{\arg\min} \|\mathbf{y} - \mathbf{A}\mathbf{z}\|_2^2 + \lambda\|\mathbf{z} - \mathbf{x}_{0\mid t}\|_2^2 \tag{7}
   $$

3. **ISCS重加噪**：使用Slerp生成层间相关噪声体积 $\boldsymbol{\epsilon}^{\mathrm{ISCS}}$，按公式(12)执行反向重加噪得到 $\mathbf{x}_{t-1}$。

## 实验与分析

### 核心定量结果：ISCS 在三种 3D 医学成像任务上一致提升重建质量

Table 1 汇总了各方法在稀疏 CT (SVCT 30 视图)、有限角 CT (LACT [0,100]°) 和 MRI 5× 超分辨率三个任务上的轴向、冠状、矢状面 PSNR/SSIM/LPIPS 以及层间差异指标 |Δ|。核心发现如下：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of compared methods and slice-to-slice difference for three 3D medical imaging tasks: SVCT of 30 views, LACT of [0, 100]◦, and MRI SR of 5×. The best performance is highlighted in bold. |∆| denotes the absolute gap between the inter-slice difference of the reconstruction and that of the ground truth (smaller is better; see Sec. C.1 for details)*

**SVCT 任务**：DDS+ISCS 在轴向 PSNR 上达到 36.97，较 DDS 基线 (34.76) 提升 +2.21 dB；冠状 SSIM 从 0.939 提升至 0.961，LPIPS 从 0.073 降至 0.047；矢状 LPIPS 从 0.114 降至 0.073。层间差异 |Δ| 从 0.005588 降至 0.001835，降幅达 67%。值得注意的是，DDNM+ISCS 同样显著优于 DDNM 基线（轴向 PSNR 33.97 vs 32.55），表明 ISCS 对不同的扩散逆问题求解器均有效。

**LACT 任务**：该任务因角度缺失严重，DDS 基线在冠状/矢状面表现较差（LPIPS 分别为 0.116/0.159）。DDS+ISCS 将冠状 LPIPS 降至 0.091，矢状 LPIPS 降至 0.105，轴向 PSNR 提升 +2.58 dB（从 29.07 到 31.65）。层间差异 |Δ| 从 0.011592 大幅降至 0.001966，降幅达 83%，表明 ISCS 在极欠定条件下对层间一致性的修复尤为显著。

**MRI SR 任务**：DDS+ISCS 轴向 PSNR 达 40.33（+1.01 dB），冠状 LPIPS 从 0.038 降至 0.019，矢状 LPIPS 从 0.061 降至 0.032。与 CT 任务相比，MRI 任务的基线层间不一致问题相对较轻（DDS 的 |Δ| 为 0.001593），但 ISCS 仍将 |Δ| 进一步压缩至 0.001076。

**跨方法一致性**：TV 正则化（DDS+TV）在降低层间差异方面有效（SVCT |Δ| 0.002038），但代价是引入过度平滑，导致 SSIM 和 LPIPS 劣化（冠状 LPIPS 0.083 vs DDS+ISCS 的 0.047）。传统方法 ADMM-TV 和 FDK 在所有指标上均远逊于基于扩散的方法。

### ISCS vs BCS：球面插值噪声为何优于相同噪声

Table 2 和 Figure 4 系统比较了两种噪声同步策略——BCS（所有切片注入完全相同噪声）与 ISCS（Slerp 插值噪声）。ISCS 在冠状和矢状面全面超越 BCS：冠状 PSNR 38.16 vs 38.00，矢状 LPIPS 0.099 vs 0.107。差异在定性结果中更为直观：BCS 沿 z 轴产生明显的“复制伪影”（Figure 4 红箭头指示），表现为相邻切片间解剖结构被不当复制；ISCS 则保持自然的层间过渡，在保持一致性的同时避免了这一伪影。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/009_Table_2.jpg]]
*Table 2: Quantitative results of adopting identical (BCS) and slerp noise (ISCS) during re-noising*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results of adopting identical (BCS) and slerp noise (ISCS) during re-noising, where the red arrows denote the noticeable “copying artifacts”. The display window is set as [-480, 820] HU*

这一对比揭示了核心机制差异：BCS 强制所有切片共享完全相同的采样轨迹，对医学体积中固有的层间解剖变化施加了过度刚性约束；ISCS 通过沿超球面测地线插值，在保持每切片噪声统计特性（标准高斯分布）的同时，引入沿 z 轴自然衰减的相关性，使相邻切片采样轨迹对齐但非完全相同。

### 采样轨迹动态分析：ISCS 早期建立层间一致性

Figure 5 展示了 PSNR、LPIPS 和层间差异随反向采样步数 (T→0) 的演变曲线。关键发现是：DDS+ISCS（橙色曲线）的层间差异在采样早期即快速下降并趋近真值参考线（黑色虚线），而 DDS 基线（蓝色曲线）的层间差异始终维持在高位。这表明 ISCS 的噪声相关性在扩散过程的粗粒度阶段（高 t 值）就已有效引导各切片朝向一致的解空间区域收敛，而非仅在后期精细调整。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/012_Figure_5.jpg]]
*Figure 5: Performance curves across the sampling process, where a higher PSNR and lower LPIPS and inter-slice difference reflect improved data fidelity and better inter-slice consistency*

### 确定性采样下的表现：仅初始化噪声相关即有效

Table 6 展示了在完全确定性采样（DDIM, η=0）下，仅对初始噪声施加 ISCS 相关性的效果。结果显示，即使整个反向过程无随机噪声注入，ISCS 仍显著改善辅助视图质量：冠状 LPIPS 从 0.239 降至 0.065，矢状 LPIPS 从 0.241 降至 0.102。这证明 ISCS 的一致性机制不仅作用于重加噪步骤，也可通过初始化噪声的层间相关性为整个采样轨迹提供一致性引导。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/016_Table_6.jpg]]
*Table 6: ISCS with Deterministic Sampling. Effect of ISCS on initial noise under DDIM $\eta$ = 0 (SVCT-30). Significant improvements in auxiliary views demonstrate successful consistency enforcement. Table 7: Stochasticity Ablation. Performance vs. η on SVCT-30. Higher stochasticity yields better reconstruction*

### 随机性强度的消融：适当随机性对重建至关重要

Table 7 的 η 消融实验表明，重建性能随随机性强度单调提升：η=0.2 时轴向 PSNR 为 36.48，η=1.0 时达到最佳 37.08。这一趋势说明，虽然 ISCS 控制了噪声的层间相关性，但保留适当的随机性对逃逸局部极小和恢复高频结构细节至关重要。完全确定性采样（η=0）反而限制了模型探索解空间的能力。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/017_Table_7.jpg]]

### 锚点选择鲁棒性：对夹角不敏感

Table 8 验证了 ISCS 对 Slerp 插值中两个锚点噪声向量之间夹角的鲁棒性。在 30° 至 175° 的广泛范围内，10 次独立运行的 PSNR 均值波动极小（轴向 36.97 ± 0.02），标准差可忽略。这从实证角度验证了高维高斯分布的浓度现象——任意两个独立采样的高维噪声向量间夹角高度集中于 90° 附近，使得 ISCS 在实际使用中无需精细调节锚点选择策略。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/018_Table_8.jpg]]
*Table 8: Stability of Anchor Selection Strategy. Quantitative results ( $\mathrm { M e a n } \pm \mathrm { S t d }$ ) of ISCS under different anchor angles (10 independent runs each) on SVCT-30 task. The method shows minimal sensitivity to the specific geometric configuration of the latent noise

### 切片厚度鲁棒性：无需参数调整

Table 9 展示了在不同切片厚度（3mm、5mm、7.5mm）下，DDS+ISCS 在所有三个解剖面一致优于 DDS 基线。以 7.5mm 厚层为例，冠状 PSNR 从 31.13 提升至 32.52，矢状 LPIPS 从 0.192 降至 0.160。ISCS 无需针对不同 z 间距调整任何参数，这得益于 Slerp 插值仅依赖切片索引的相对位置（通过 α_i 参数），自然适应任意等距网格。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/020_Table_9.jpg]]
*Table 9: Quantitative Results under Varying Slice Thicknesses. ISCS demonstrates consistent performance gains over the baseline (DDS) across all slice thicknesses (3mm, 5mm, 7.5mm). The method effectively mitigates inter-slice discontinuities regardless of z-spacing, confirming its robustness to variations in acquisition protocols*

### 病理保留能力：ISCS 避免 TV 的病灶模糊

Figure 6 和附录 C.5.1 展示了含病灶病例的定性对比。在 1mm 薄层和 5mm 厚层两个案例中，DDS+ISCS 清晰保留了病灶边界和内部纹理，而 DDS+TV 导致小病灶模糊甚至接近消失。这一差异源于 TV 正则化对梯度幅值的全局惩罚，倾向于平滑低对比度小结构；ISCS 的一致性机制仅约束层间噪声相关性，不影响数据保真项对局部结构的恢复能力。

### 与显式 3D 感知方法的对比

Table 4 和 Table 5 将 DDS+ISCS 与两种显式 3D 感知方法（**TPDM**, Lee et al., MICCAI 2023; **DiffusionBlend**, Song et al., 2024）进行了比较。在分布内（1mm 层厚）SVCT 任务上，DiffusionBlend 轴向 PSNR 达 38.21，略高于 DDS+ISCS 的 36.97，但在分布外（5mm 层厚）场景下，DDS+ISCS 的轴向 PSNR 为 31.85，优于 DiffusionBlend 的 31.64，且冠状/矢状 LPIPS 全面更优。在 LACT 任务上，DDS+ISCS 在 1mm 层厚的冠状 PSNR（33.03 vs 32.08）和矢状 PSNR（30.07 vs 29.09）上均超越 DiffusionBlend。这表明 ISCS 作为一种即插即用策略，在保持 2D 扩散先验优势的同时，在跨层厚泛化方面展现出独特优势。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/014_Table_4.jpg]]
*Table 4: Quantitative comparison on the SVCT task of 30 views. Higher PSNR/SSIM and lower LPIPS indicate better performance*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/015_Table_5.jpg]]
*Table 5: Quantitative comparison on the LACT task of [0, 100]°. Higher PSNR/SSIM and lower LPIPS indicate better performance*

### 失败模式与局限

尽管 ISCS 在多数场景下表现优异，分析揭示了以下边界条件：

1. **对 2D 先验质量的依赖**：ISCS 本质上是 2D 扩散先验的一致性增强策略，当 2D 先验对罕见解剖结构或病理覆盖不足时，重建质量的上限受限于预训练模型的能力。

2. **单轴一致性假设**：当前 ISCS 仅沿 z 轴施加噪声相关性，对于需要同时增强 x 和 y 方向一致性的各向异性重建场景（如严重欠采样的多平面问题），单轴约束可能不足。

3. **等距网格假设**：Slerp 插值通过 α_i 参数隐式假设切片等距分布，对于极度不均匀的网格间距，插值权重与物理距离的对应关系缺乏理论保证（尽管 Table 9 已展示对常见层厚变化的鲁棒性）。

4. **病理评估规模有限**：病灶保留能力的验证仅基于 DeepLesion 数据集的两个案例（Figure 6），缺乏大规模、多类型病灶的系统性量化评估，该结论需谨慎外推。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_R5ETdN6ifA/figures/013_Table_3.jpg]]
*Table 3: Slice-to-slice difference of compared methods for three 3D medical imaging tasks: SVCT of 30 views, LACT of [0, 100]◦, and MRI SR of 5×. $\operatorname { S D i f f } _ { \operatorname { r e c o n } }$ and SDiffGT denote the mean absolute difference between adjacent slices for the reconstruction and ground truth, respectively; $\Delta = \mathrm { S D i f f _ { r e c o n } - S D i f f _ { G T } }$ measures the signed gap, and |∆| is its absolute value (smaller is better)

## 方法谱系与知识库定位

### 问题定位：2D扩散先验的3D一致性断层

在3D医学成像重建中，直接训练3D扩散模型面临计算开销巨大和数据稀缺的双重困境，因此主流做法是将预训练的2D扩散模型逐切片（slice-wise）应用于3D体积。然而，这一策略存在一个根本性瓶颈：反向扩散过程中，每个切片的随机噪声组件独立采样（$ \epsilon_i \sim \mathcal{N}(0, I) $），导致相邻切片的采样轨迹完全不相关。在欠定测量条件下（如稀疏角CT或有限角CT），数据保真项提供的层间约束极为薄弱，无法弥合这种内在随机性造成的轨迹发散，最终表现为严重的层间结构不连续和条纹状伪影。

本文提出的**层间一致随机性（Inter-Slice Consistent Stochasticity, ISCS）**正是针对这一瓶颈设计的即插即用策略。其核心因果调控旋钮是扩散采样重加噪步骤中注入的随机噪声的跨切片相关性——通过将该噪声从独立同分布的高斯噪声替换为沿超球面测地线平滑插值的相关噪声，直接对齐相邻切片的采样轨迹，从根源上增强3D体积的层间一致性。

### 方法谱系中的位置

ISCS处于**扩散模型逆问题求解器（Diffusion-based Inverse Problem Solver, DIS）**与**3D一致性增强策略**的交汇点。其方法谱系可沿以下维度展开：

**上游基础：扩散逆问题求解框架。** ISCS建立在两类代表性DIS之上：
- **DDNM**（Wang et al., arXiv 2022）：利用零域分解（range-null space decomposition）将测量一致性约束注入去噪过程，更新规则为 $ \mathbb{E}[\mathbf{x}_0 \mid \mathbf{x}_t, \mathbf{y}] \approx (\mathbf{I} - \mathbf{A}^{\dagger}\mathbf{A}) D_{\theta^*}(\mathbf{x}_t) + \mathbf{A}^{\dagger}\mathbf{y} $。
- **DDS**（Chung et al., arXiv 2024）：通过求解邻近优化问题 $ \arg\min_{\mathbf{x}_0} \frac{\gamma}{2} \|\mathbf{y} - \mathbf{A}\mathbf{x}_0\|_2^2 + \frac{1}{2} \|\mathbf{x}_0 - D_{\theta^*}(\mathbf{x}_t)\|_2^2 $ 实现数据一致性校正，相比DDNM具有更强的保真能力。

ISCS直接作用于这两类求解器的重加噪步骤（DDIM风格的 $ \mathbf{x}_{t-1} $ 更新），将其中原本独立采样的 $ \epsilon $ 替换为层间相关的 $ \boldsymbol{\epsilon}^{\mathrm{ISCS}} $，因此可视为对DIS框架的**噪声注入通道的通用增强**。

**同级对比：层间一致性策略。** 现有增强3D一致性的方法可分为三类：
1. **后处理正则化**：如 **DDS+TV**（在DDS输出上施加总变分正则化），通过惩罚相邻切片差异来抑制不连续性，但会引入模糊和"卡通化"伪影，且对小病灶有抹除风险（见Figure 6）。
2. **相同噪声强制对齐**：**BCS**（Batch-Consistent Sampling, Kwon & Ye, CVPR 2025）对所有切片施加完全相同的噪声，强制采样轨迹完全同步。然而，这在医学体积中过于刚性——真实解剖结构沿z轴存在自然变化，相同噪声会导致特征被不当复制，产生"复制伪影（copying artifacts）"和条状伪影（Table 2, Figure 4）。
3. **显式3D感知先验**：**TPDM**（Lee et al., MICCAI 2023）利用正交平面（axial/coronal/sagittal）的一致性约束；**DiffusionBlend**（Song et al., 2024）融合多平面2D先验。这类方法通过修改网络架构或训练目标来引入3D感知，但计算开销较大，且泛化到分布外切片厚度时性能下降明显（Table 4: TPDM在5mm切片上LPIPS劣化至0.137，而DDS+ISCS为0.071）。

ISCS在谱系中的独特位置在于：**它既不修改网络架构，也不添加损失项或后处理步骤，仅通过操控噪声的几何结构实现一致性**。这使其兼具"即插即用"的便利性和"从根源解决问题"的优雅性。

### 核心机理：高维高斯浓度与球面插值

ISCS的理论基础是高维高斯分布的**浓度现象（concentration of measure）**：各向同性高斯向量 $ \mathbf{z} \sim \mathcal{N}(0, \mathbf{I}_d) $ 的概率质量集中在半径为 $ \sqrt{d} $ 的超球面薄壳上（Gaussian Annulus Theorem, Eq. 10）。因此，在相邻切片间进行线性插值会离开高概率区域，破坏每切片噪声的统计特性。

ISCS采用**球面线性插值（Slerp）**在锚点噪声向量 $ \mathbf{z}_1, \mathbf{z}_S $ 之间沿超球面测地线生成中间切片噪声：
$$ \epsilon_i^{\mathrm{ISCS}} = \mathrm{slerp}(\mathbf{z}_1, \mathbf{z}_S; \alpha_i) = \frac{\sin((1-\alpha_i)\Omega)}{\sin(\Omega)}\mathbf{z}_1 + \frac{\sin(\alpha_i\Omega)}{\sin(\Omega)}\mathbf{z}_S $$
其中 $ \Omega = \arccos(\mathbf{z}_1^\top \mathbf{z}_S) $ 为锚点间夹角，$ \alpha_i $ 为切片位置参数。这一构造同时满足两个关键性质：(1) 每切片噪声仍服从标准高斯分布，保持扩散过程的统计正确性；(2) 相邻切片噪声高度相关，远端相关性自然衰减，与真实解剖结构的层间变化模式一致。

### 适用边界与局限

**已验证的适用场景：**
- 稀疏角CT（SVCT, 30 views）、有限角CT（LACT, [0,100]°）、MRI各向同性超分辨率（5×）三类任务
- 不同切片厚度（1mm, 3mm, 5mm, 7.5mm）下均稳定优于DDS基线，无需参数调整（Table 9）
- 可与DDNM和DDS两类DIS无缝集成，也可与确定性采样（DDIM, η=0）结合使用（Table 6）
- 对锚点向量间夹角不敏感（30°至175°范围内性能标准差极小，Table 8）

**已知局限与待验证边界：**
1. **先验依赖性**：ISCS的性能上限受制于预训练2D扩散先验的质量。对于2D先验难以覆盖的罕见解剖结构或病理类型，重建效果可能受限。这一局限在DeepLesion数据集上仅有两个案例的初步验证（Figure 6），缺乏大规模、多类型病灶的系统性评估。
2. **单轴一致性假设**：当前仅对z轴（切片方向）建模噪声相关性。对于需要多轴一致性的各向异性重建场景（如同时增强x和y方向），ISCS尚未扩展。Slerp插值本质上假设切片等距分布，对极度不均匀的网格间距缺乏理论保证。
3. **与3D感知方法的集成**：论文仅将ISCS与显式3D感知方法（TPDM, DiffusionBlend）的集成列为开放问题，实际组合后的性能增益和计算开销尚未量化。
4. **生成多样性影响**：引入层间噪声相关是否会限制生成多样性？在需要多种可能解的任务（如不确定性估计）中是否存在负面影响，尚未探讨。

### 开放问题

1. **多轴联合一致性**：ISCS能否从单轴（z）扩展到多轴联合控制（x, y, z），以解决更复杂的各向异性分辨率重建问题？这可能需要将Slerp从一维插值推广到三维流形上的多锚点插值。

2. **非线性前向模型适配**：在动态成像、非刚性运动校正等非线性前向模型下，ISCS的轨迹对齐机制是否仍然有效？当前验证仅限于线性正向模型 $ \mathbf{y} = \mathbf{A}\mathbf{x} + \mathbf{n} $。

3. **非均匀网格推广**：Slerp假设等距切片，对于非均匀间距或任意切片方向（如倾斜切片），是否可采用更高级的流形插值（如基于核方法的测地线回归）替代？

4. **与3D感知框架的协同**：将ISCS与DiffusionBlend或TPDM集成，能否在保持计算效率的同时进一步提升层间一致性？ISCS的噪声相关策略与多平面一致性约束是否存在互补或冗余？

5. **病理鲁棒性系统验证**：当前病灶保留能力的评估仅基于两个案例，需在更大规模、更多类型的病理数据上系统验证ISCS是否确实优于TV正则化等后处理方法。

## 原文 PDF

![[paperPDFs/ICLR_2026/Improving_2D_Diffusion_Models_for_3D_Medical_Imaging_with_InterSlice_Consistent_Stochasticity.pdf]]
