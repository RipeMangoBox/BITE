---
title: Physics-Consistent Diffusion for Efficient Fluid Super-Resolution via Multiscale Residual Correction
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Physics_Consistent_Diffusion_for_Efficient_Fluid_Super_Resolution_via_Multiscale_Residual_Correction.pdf
project_link: null
code_link: "https://github.com/lizhihao2022/ReMD"
aliases:
- PCDEFSRMRC
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 在扩散逆过程中施加物理一致性多尺度残差校正（时间门控多网格V-cycle与多小波算子）。
primary_logic: 将流体超分视为从粗解开始的迭代残差校正过程，利用多网格思想在扩散每步中校正残差，可大幅提升效率与物理准确性。
claims:
- ReMD仅用5步逆过程，在NS和ERA5上生成更锐利的细丝/锋面和更小的误差图，且抑制了基线方法的环状/条带伪影。
- 多网格校正器主要减少大尺度偏差，频谱残差贡献最大的高频保真度，而平滑和各向异性扩散充当稳定器。
- 在NS、ERA5、Ocean三个基准上，ReMD均取得最低RMSE和最高或相当的PSNR/SSIM，同时采样步数远少于扩散基线。
- NS (2×) 上 RMSE = 0.0209 (ReMD-5)
---

# Physics-Consistent Diffusion for Efficient Fluid Super-Resolution via Multiscale Residual Correction

> [!tip] 核心洞察
> 将流体超分视为从粗解开始的迭代残差校正过程，利用多网格思想在扩散每步中校正残差，可大幅提升效率与物理准确性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多尺度残差校正的物理一致性扩散模型用于高效流体超分辨率 |
| 英文题名 | Physics-Consistent Diffusion for Efficient Fluid Super-Resolution via Multiscale Residual Correction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00149) · [Code](https://github.com/lizhihao2022/ReMD) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | ReMD |
| Dataset | NS, ERA5, Ocean, NS2D (4×) 物理指标 |

> [!tip] 效果简介
> - NS (2×) 上，RMSE 0.0209 (ReMD-5) vs 0.0221 (ResShift-15) (-0.0012)；PSNR 49.94 (ReMD-5) vs 49.47 (ResShift-15) (+0.47)。
> - ERA5 (4×) 上，RMSE 0.0802 (ReMD-5) vs 0.0879 (ResShift-15) (-0.0077)；PSNR 58.19 (ReMD-5) vs 57.39 (ResShift-15) (+0.80)。
> - Ocean (4×) 上，RMSE 0.0132 (ReMD-2) vs 0.0136 (ResShift-15) (-0.0004)。

## 概述

流体超分辨率（Fluid SR）旨在从低分辨率（LR）物理场重建高分辨率（HR）细节，直接服务于天气预测、海洋建模和湍流分析等关键应用。现有图像超分方法和通用扩散模型在此任务上存在两个根本瓶颈：其一，它们对密集网格逐像素上采样，忽略了流体场的多尺度结构和物理一致性；其二，标准扩散模型需要上百步采样，计算开销极大，难以部署于实时或大规模模拟场景。这导致重建结果出现频谱不匹配、虚假散度以及环状/条带伪影——**Figure 1** 中 EDSR、FNO、SwinIR 等方法均暴露出这些问题。

本文提出的 **ReMD**（Residual-corrected Multi-scale Diffusion）将流体超分重新定义为从粗解开始的迭代残差校正过程。其核心思想是：在扩散逆过程的每一步，将更新方向分解为数据一致性残差与轻量物理残差的加权和，再通过一个时间门控的多网格校正器（multigrid corrector）在多尺度上校正该残差。多尺度层级由固定的多小波限制/延拓算子构建，无需学习参数即可实现频谱干净的上/下采样，从而同时捕获大尺度结构和细小涡旋细节。

这一设计带来了三重收益：

1. **极致的采样效率**：ReMD 仅需 2–5 步逆过程即可生成高质量结果，而扩散基线 ResShift 需要 15 步，SR3 则需 100+ 步。在 NS、ERA5、Ocean 三个基准上，ReMD 均取得最低 RMSE 和最高（或并列最高）的 PSNR/SSIM——**Table 1**。
2. **物理一致性**：可微分的拉普拉斯/双谐波平滑、各向异性边缘保持扩散和频谱对齐残差共同作用，显著抑制虚假散度。在 NS2D 上，涡度误差（VE）从 ResShift 的 3.26E-03 降至 2.34E-03，熵误差（EE）降低近一个数量级——**Table 4**。
3. **频谱保真度**：误差-能量谱分析（**Figure 3**）表明，ReMD 在从大尺度到高波数的全频段上保持最低误差，尤其在 Nyquist 带以上高频区域优势明显，这得益于频谱残差对高频保真度的主导贡献——消融实验（**Table 2**）证实移除频谱项导致最大性能衰退。

ReMD 在像素空间操作，当前针对单帧超分设计，尚未评估时间序列动态稳定性；其计算成本与 HR 网格大小线性相关，向潜在空间迁移是未来方向。代码已开源（https://github.com/lizhihao2022/ReMD）。

## 背景与动机

### 流体超分辨率的科学意义与工程需求

高分辨率流体动力学模拟与观测在天气预报、气候预测、海洋建模和湍流研究中至关重要。然而，直接运行高分辨率数值求解器或部署密集传感器网络成本极高：计算代价随网格点数超线性增长，存储和传输带宽也迅速膨胀。因此，从粗分辨率（LR）数据重建高分辨率（HR）流场——即流体超分辨率（SR）——成为一种经济高效的替代方案。

流体SR与自然图像SR存在根本差异。自然图像SR主要追求感知质量和纹理逼真度，而流体SR的核心目标是**恢复物理上一致的精细结构**：涡丝、锋面、剪切带和能量级串特征。这些结构在粗分辨率下被平滑或混叠，重建时若违反物理约束，会导致虚假散度、能量谱失真和动力学不稳定。

### 现有方法的瓶颈

当前流体SR方法大致分为三类，各自存在显著局限：

**（1）基于CNN和Transformer的图像超分方法。** 将流场视为多通道图像，直接应用EDSR（Kuriakose et al., 2023）、SwinIR（Liang et al., ICCV 2021）等架构。这类方法在频谱高频区域表现不佳，容易产生振铃伪影和条带伪影（图1），且对物理一致性无任何保证。

**（2）神经算子方法。** FNO（Li et al., JMLR 2023）、MWT（Gupta et al., NeurIPS 2021）、Galerkin Transformer（Cao, NeurIPS 2021）等通过在傅里叶域或多小波域学习映射，试图捕捉全局依赖。然而，它们通常仅做单步前向映射，缺乏迭代校正机制，在细尺度涡旋和锋面恢复上仍存在块状伪影或模糊。

**（3）扩散模型方法。** SR3（Saharia et al., TPAMI 2022）和ResShift（Yue et al., NeurIPS 2023）将扩散生成引入超分，取得了优于确定性方法的感知质量。但它们的核心瓶颈在于：**逆过程需要大量采样步数（100+或至少15步），且每一步仅依赖数据驱动的噪声/残差预测，未嵌入物理约束**。这导致三个问题：
- **采样效率低下**：推理时间随步数线性增长，难以满足实时或近实时需求。
- **频谱不匹配**：扩散过程的随机性在中高频引入虚假能量，偏离真实湍流能谱。
- **物理不可信**：缺乏对散度、涡度守恒等流体力学约束的显式建模，生成场可能违反基本物理定律。

### 核心洞察：超分即多尺度残差校正

本文的核心观察是：**流体超分辨率本质上可视为一个从粗解出发的迭代残差校正过程**。粗分辨率输入提供了大尺度结构的可靠估计，而缺失的精细尺度信息需要通过多尺度校正逐步恢复。这一视角直接启发了经典数值线性代数中的**多重网格（multigrid）思想**：在层级式网格上交替进行限制（restriction）、粗校正和平滑（smoothing），以高效消除不同尺度的误差分量。

将多重网格思想引入扩散逆过程，可以在每一步中同时对数据一致性和物理约束进行多尺度校正，从而：
- **大幅减少采样步数**：每步校正更精准，2–5步即可达到或超越15步基线的质量。
- **保证频谱保真度**：多小波基的限制/延拓算子天然保持频谱干净，避免混叠。
- **嵌入物理先验**：可微分的平滑、各向异性扩散和频谱对齐残差作为软约束，抑制非物理伪影。

### 本文动机与贡献

基于上述洞察，本文提出 **ReMD（Physics-Consistent Diffusion via Multiscale Residual Correction）**，一个物理一致的扩散超分框架。其设计围绕三个核心原则：

1. **残差驱动的逆过程**：将扩散逆过程的更新方向重新定义为数据一致性残差与物理残差的加权和，而非单纯的噪声预测。
2. **时间门控多网格校正器**：使用固定的多小波算子构建层级式V-cycle校正模块，通过可学习的时间门控动态调节粗-细尺度贡献。
3. **方程无关的物理残差**：引入拉普拉斯/双谐波平滑、各向异性边缘保持扩散和频谱对齐等通用物理残差，无需依赖特定控制方程。

实验表明，ReMD在NS、ERA5和Ocean三个流体基准上，以仅2–5步采样即取得最低RMSE和最高/相当的PSNR/SSIM，同时在涡度误差、能量谱等物理指标上显著优于扩散基线ResShift，验证了“多尺度残差校正+物理一致性”这一设计哲学的有效性。

## 核心创新

### 瓶颈与动机

现有流体超分辨率（SR）方法面临两个根本性瓶颈。其一，基于图像的超分模型（如 **EDSR**、**SwinIR** (Liang et al., ICCV 2021)）和神经算子（如 **FNO** (Li et al., JMLR 2023)）在流体数据上采样密集、忽略物理约束，导致频谱不匹配和虚假散度。其二，通用扩散模型（如 **SR3** (Saharia et al., TPAMI 2022)、**ResShift** (Yue et al., NeurIPS 2023)）虽然生成质量较高，但采样步数动辄 15–100+ 步，推理效率低下，且缺乏对流体物理一致性的显式建模。

ReMD 的核心洞察在于：**将流体超分视为从粗解开始的迭代残差校正过程，利用多网格思想在扩散每步中校正残差，可大幅提升效率与物理准确性。** 这一视角将扩散逆过程重新解释为一个逐级精炼的多尺度校正器，而非单纯去噪。

### 关键创新点（Changed Slots）

| 创新维度 | 基线方法 | ReMD 方案 | 证据锚点 |
|---------|---------|----------|---------|
| **逆过程更新方向** | 标准噪声预测或残差偏移去噪 | 数据一致性残差 + 物理残差，经时间门控多网格校正的多尺度残差漂移 | Eq. (9); Eq. (10) |
| **多尺度建模** | 无显式多尺度校正（仅 UNet 等单尺度结构） | 固定的多小波限制/延拓算子 + 时间门控层级平滑器（V-cycle） | Sec. 3.2; Eq. (11); Eq. (12) |
| **物理一致性** | 无物理约束或仅数据驱动 | 可微分的拉普拉斯/双谐波平滑、各向异性边缘保持扩散、频谱对齐等方程无关的物理残差 | Sec. 3.3; Eq. (13)–(16) |
| **采样步数** | 扩散基线需 100+ 或至少 15 步 | 仅需 2–5 步达到更优质量 | Table 1; Table 3; Fig. 5 |

#### 1. 多尺度残差漂移替代噪声预测

ReMD 对扩散逆过程的更新方向进行了根本性重构。标准扩散模型（如 SR3、ResShift）在每步预测噪声或残差偏移，而 ReMD 的更新方程（Eq. 9）为：

$$u_{t-1} = u_t + \alpha_t e_t + \beta_t g_{\theta}(u_t, t) + \sigma_t \varepsilon_t, \qquad \varepsilon_t \sim \mathcal{N}(0, I)$$

其中漂移项 $e_t$ 由**数据一致性残差**与**物理残差**的加权和经过多网格校正器处理得到（Eq. 10）：

$$r(u) = u^{\mathrm{LR}} - R(u) + \lambda(t)\rho(u), \qquad e_t = S_t\bigl(r(u_t)\bigr)$$

这一设计的因果机制在于：数据一致性项 $u^{\mathrm{LR}} - R(u)$ 确保重建结果与低分辨率输入在限制算子 $R$ 下一致，而物理残差 $\rho(u)$ 注入不可微物理约束，$\lambda(t)$ 时间门控则控制物理约束在不同扩散阶段的贡献权重。$g_\theta$ 为可选的轻量学习头（零初始化末层），仅提供微小细化。

#### 2. 时间门控多网格校正器

多网格校正器 $S_t$ 是 ReMD 效率与精度的核心引擎（Eq. 11）：

$$S_t(r) = \mathrm{Smooth}_0(r) + \sum_{\ell=1}^{L} w_\ell(t) P_\ell \mathrm{Smooth}_\ell(R_\ell r)$$

其工作流为：残差 → 多小波限制（$R_\ell$）→ 粗尺度校正（$\mathrm{Smooth}_\ell$）→ 多小波延拓（$P_\ell$）→ 逐层累加。时间门控 $w_\ell(t)$ 控制粗–细尺度的贡献比例：**早期步骤侧重粗尺度校正以消除大尺度偏差，后期步骤侧重细尺度以恢复高频结构**。

多尺度层级采用固定的多小波限制/延拓算子（Eq. 12）：

$$R \equiv I_h^{2h} = H_y \otimes H_x, \qquad P \equiv I_{2h}^h = R^{\top}$$

这是与现有方法的关键区别：限制和延拓算子**固定且可逆**，无需学习参数，频谱干净无混叠，保证了多尺度分解的数学严格性。平滑器使用轻量深度可分离卷积，每步计算复杂度为 $O(HW)$。

#### 3. 方程无关的物理残差族

ReMD 引入三类可微分的物理残差（Eq. 13）：

$$\rho(u) = \sum_k w_k \rho_k(u; u_0, M)$$

- **平滑残差**：基于拉普拉斯/双谐波算子，抑制高频噪声和伪影。
- **各向异性扩散残差**：边缘保持扩散，保护锋面和剪切带等不连续结构。
- **频谱对齐残差**（Eq. 16）：$\rho_{\mathrm{spec}}(u) = \mathcal{B}(W(k) \odot \mathcal{F}(u))$，在傅里叶域按频率分箱计算对数能量差异，加权校正频谱分布。

这些残差**不依赖特定 PDE 形式**，通过 FFT/iFFT 或深度可分离卷积实现，完全可微且高效。消融实验（Table 2）表明：频谱残差贡献最大的高频保真度，移除后 RMSE 从 1.33E-02 升至 1.41E-02；平滑和各向异性扩散充当稳定器，抑制伪影并保护锋面。

### 创新效果总结

ReMD 的创新带来三重收益：
1. **精度提升**：在 NS、ERA5、Ocean 三个基准上均取得最低 RMSE 和最高或相当的 PSNR/SSIM（Table 1），物理指标（涡度误差、熵误差、能量差异）同样最优（Table 4）。
2. **效率跃升**：仅需 2–5 步达到优于 ResShift-15 的质量，推理速度提升 1.4×–3.5×（Table 3）。
3. **频谱保真**：误差–能量谱（Figure 3）显示 ReMD 在全频段保持最低误差，尤其在低频大尺度偏差和高频细节恢复上优势显著。

## 整体框架

ReMD 将流体超分辨率重新表述为**从粗分辨率初始解出发的迭代残差校正过程**，并在扩散模型的逆扩散框架内实现。其核心思想是：在每一个逆扩散步骤中，不是单纯依赖噪声预测网络来更新高分辨率估计，而是**耦合数据一致性约束与轻量级物理先验，通过一个时间门控的多网格校正器对残差进行多尺度修正**，从而以极少的采样步数（2–5步）达到甚至超越传统扩散模型（15–100+步）的重建质量。

### 输入输出流

系统的输入是一个低分辨率（LR）流场 $\boldsymbol{u}^{LR} \in \mathcal{U}_c$，输出是对应的高分辨率（HR）估计 $\hat{\boldsymbol{u}}^{HR} \in \mathcal{U}$。整个流程可概括为以下阶段：

1. **初始化解**：以粗分辨率解作为起点，通过上采样获得初始 HR 估计 $u_T$。
2. **逆扩散迭代**：从 $t = T$ 到 $t = 1$，每一步执行：
   - 计算当前估计 $u_t$ 的**残差** $r(u_t)$——由数据一致性残差和物理残差两部分加权组成；
   - 将残差送入**时间门控多网格校正器** $S_t$，得到本步的漂移方向 $e_t = S_t(r(u_t))$；
   - 可选地通过一个轻量级学习头 $g_\theta$ 进行微调；
   - 按 DDIM 采样公式更新 HR 估计：$u_{t-1} = u_t + \alpha_t e_t + \beta_t g_\theta(u_t, t) + \sigma_t \varepsilon_t$。
3. **最终输出**：$u_0$ 即为超分辨率重建结果 $\hat{\boldsymbol{u}}^{HR}$。

### 模块关系与数据流

ReMD 的 pipeline 由以下核心模块串联构成（参见 Figure 2 的系统概览）：

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ReMD. Starting from a coarse LR initial solution, the reverse diffusion steps refine the HR estimate*

| 模块 | 角色 | 关键操作 |
|------|------|----------|
| **粗 LR 初始解** | 输入 | 上采样 LR 场得到初始 $u_T$ |
| **残差计算模块** | 耦合数据与物理 | $r(u) = u^{LR} - \mathcal{R}(u) + \lambda(t)\rho(u)$，其中 $\mathcal{R}$ 为限制算子（下采样），$\rho(u)$ 为方程无关的物理残差（平滑、各向异性扩散、频谱对齐） |
| **时间门控多网格校正器 $S_t$** | 多尺度残差校正 | 对残差执行 V-cycle：限制→粗层校正→延拓→平滑，利用固定的多小波限制/延拓算子 $R \equiv I_h^{2h} = H_y \otimes H_x$ 和 $P \equiv I_{2h}^h = R^\top$，层级权重 $w_\ell(t)$ 随时间步 $t$ 动态调整 |
| **学习头 $g_\theta$** | 可选的微小细化 | 零初始化末层，提供额外的可学习修正 |
| **逆扩散步** | 迭代更新 | 按 DDIM 采样将 $u_t$ 更新为 $u_{t-1}$，训练时使用标准 $\varepsilon$-预测损失 $\mathcal{L}(\theta) = \mathbb{E}_{t,u_t,\varepsilon}[\|\varepsilon - \hat{\varepsilon}_\theta(u_t,t)\|_2^2]$ |

### 关键设计决策

**时间门控机制**是多网格校正器的核心创新。在逆扩散早期（$t$ 较大），门控权重 $w_\ell(t)$ 倾向于激活较粗的网格层级，优先消除大尺度偏差；随着 $t$ 减小，权重逐渐向细层级倾斜，以恢复高频涡旋和锋面等精细结构。消融实验证实（Table 2），移除多网格校正器导致 RMSE 从 $1.33\times10^{-2}$ 升至 $1.38\times10^{-2}$，PSNR 下降 0.34 dB。

**多小波基**的选择保证了频谱干净且无参数。与需要学习的可训练限制/延拓算子不同，固定的多小波分解与重构（$H_y \otimes H_x$）天然具有可逆性和正交性，避免了频谱混叠，同时将每步计算复杂度控制在 $O(HW)$。

**物理残差**以可微分、方程无关的方式注入先验知识：拉普拉斯/双谐波平滑抑制高频噪声，各向异性扩散保留锋面等方向性结构，频谱对齐残差则通过频域加权最小化与目标谱的对数能量差异。消融实验表明，移除频谱残差造成的性能衰退最大（RMSE 升至 $1.41\times10^{-2}$，PSNR 降至 47.20），而平滑和各向异性扩散残差充当稳定器，抑制伪影并保护前沿结构。

## 核心模块与公式推导

### 3.1 问题形式化与逆扩散更新

ReMD 将流体超分辨率建模为从粗分辨率函数空间 $\mathcal{U}_c$ 到高分辨率函数空间 $\mathcal{U}$ 的算子学习问题：

$$
\mathcal{F}_{\theta} : \mathcal{U}_c \to \mathcal{U}, \qquad \hat{\boldsymbol{u}}^{HR} = \mathcal{F}_{\theta}(\boldsymbol{u}^{LR})
\tag{1}
$$

该映射通过有限步逆扩散过程实现。设 $u_t$ 为第 $t$ 步的高分辨率估计（$t = T, \dots, 1, 0$），每步更新遵循：

$$
u_{t-1} = u_t + \alpha_t e_t + \beta_t g_{\theta}(u_t, t) + \sigma_t \varepsilon_t, \qquad \varepsilon_t \sim \mathcal{N}(0, I)
\tag{9}
$$

其中：
- $e_t$：**多尺度残差漂移项**，是 ReMD 的核心创新，由时间门控多网格校正器 $S_t$ 对复合残差 $r(u_t)$ 处理得到；
- $g_{\theta}$：可选的轻量学习头，采用零初始化末层，提供微小细化；
- $\alpha_t, \beta_t, \sigma_t$：时间相关的步长系数，遵循 DDIM 采样调度。

### 3.2 复合残差构造

每步的残差 $r(u)$ 由两项加权构成——数据一致性残差与物理残差：

$$
r(u) = u^{\mathrm{LR}} - R(u) + \lambda(t)\rho(u)
\tag{10}
$$

- **数据一致性项** $u^{\mathrm{LR}} - R(u)$：$R$ 为限制算子（下采样），该项强制 HR 估计在降采样后与 LR 输入一致，锚定低频结构；
- **物理残差项** $\rho(u)$：由多个可微分物理约束加权组合（见 3.4 节），引导解满足流体物理先验；
- $\lambda(t)$：时间相关的权重系数，在逆过程早期（大 $t$）侧重数据一致性以消除大尺度偏差，后期（小 $t$）逐步引入物理约束以精修高频细节。

复合残差 $r(u_t)$ 随后送入时间门控多网格校正器 $S_t$，得到漂移方向 $e_t = S_t(r(u_t))$。

### 3.3 时间门控多网格残差校正器

$S_t$ 是 ReMD 的核心计算模块，它模拟经典多重网格 V-cycle，将残差在多尺度层级间传递并校正：

$$
S_t(r) = \mathrm{Smooth}_0(r) + \sum_{\ell=1}^{L} w_\ell(t) P_\ell \mathrm{Smooth}_\ell(R_\ell r)
\tag{11}
$$

**执行流程**：
1. **细层平滑**：$\mathrm{Smooth}_0(r)$ 在最细网格上对残差做局部平滑；
2. **逐层限制**：$R_\ell$ 将残差逐级限制到更粗的网格层级 $\ell$；
3. **粗层校正**：$\mathrm{Smooth}_\ell$ 在粗网格上对限制后的残差进行平滑校正；
4. **逐层延拓**：$P_\ell$ 将粗层校正结果延拓回细网格；
5. **时间门控**：$w_\ell(t)$ 为每层的可学习时间门控权重，控制不同尺度在逆过程各阶段的贡献比例——早期侧重粗尺度消除大偏差，后期侧重细尺度恢复高频结构。

**多小波限制/延拓算子**：层级间的 $R$ 和 $P$ 采用固定的多小波基实现，保证频谱干净且无参数：

$$
R \equiv I_h^{2h} = H_y \otimes H_x, \qquad P \equiv I_{2h}^h = R^{\top}
\tag{12}
$$

其中 $H_x, H_y$ 为多小波分解滤波器，$\otimes$ 表示张量积。该设计的优势在于：
- **固定算子**：无需学习参数，避免过拟合；
- **可逆性**：$P = R^\top$ 保证限制-延拓循环的信息守恒；
- **频谱分离**：多小波基天然实现频带分解，使粗层聚焦低频、细层聚焦高频。

### 3.4 物理残差项

物理残差 $\rho(u)$ 由多个方程无关的可微分约束加权组合，无需已知控制方程：

$$
\rho(u) = \sum_k w_k \rho_k(u; u_0, M)
\tag{13}
$$

包含三类互补的物理残差：

1. **平滑残差**（拉普拉斯/双谐波）：惩罚高频振荡，抑制网格尺度的数值噪声；
2. **各向异性扩散残差**：沿流场梯度方向保持边缘（锋面、剪切带），垂直于梯度方向平滑，实现结构保持的去噪；
3. **频谱对齐残差**：在傅里叶域对齐重建场的能谱与目标分布：

$$
\rho_{\mathrm{spec}}(u) = \mathcal{B}(W(k) \odot \mathcal{F}(u))
\tag{16}
$$

其中 $\mathcal{F}(u)$ 为傅里叶变换，$W(k)$ 为基于分箱对数能量差异的频域权重（通过 Huber 变换鲁棒化），$\mathcal{B}$ 为逆变换。该项是消融实验中影响最大的物理约束——移除频谱残差导致 RMSE 从 $1.33\times10^{-2}$ 升至 $1.41\times10^{-2}$，PSNR 下降至 47.20（Table 2）。

所有物理残差项均通过深度可分离卷积或 FFT/iFFT 实现，保持 $\mathcal{O}(HW)$ 的每步计算复杂度。

### 3.5 训练目标

ReMD 沿用标准 $\varepsilon$-预测扩散损失，配合多网格漂移进行端到端训练：

$$
\mathcal{L}(\theta) = \mathbb{E}_{t,u_t,\varepsilon}\Big[\|\varepsilon - \hat{\varepsilon}_{\theta}(u_t,t)\|_2^2\Big]
\tag{17}
$$

其中 $\hat{\varepsilon}_{\theta}$ 为噪声预测网络，$u_t$ 按前向扩散过程加噪得到。多网格校正器 $S_t$ 的时间门控权重 $w_\ell(t)$ 与学习头 $g_\theta$ 的参数一并通过该损失优化。

## 实验与分析

### 主实验结果

Table 1 汇总了 ReMD 在三个流体超分辨率基准上的定量对比：NS（×2）、ERA5（×4）和 Ocean（×4）。ReMD 在所有数据集上均取得最低 RMSE 和最优或并列最优的 PSNR/SSIM，同时仅需 2–5 步逆过程，而最强的扩散基线 ResShift 需 15 步，SR3 需 100 步以上。

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison on three fluid SR benchmarks. NS (2×), ERA5 (4×), and Ocean (4×). We report RMSE↓, PSNR↑, and SSIM↑. Bold denotes the best and underline the second-best within each dataset/metric block. ReMD attains the lowest errors and top (or tied) perceptual scores across datasets while using only 2–5 reverse steps, compared with 15 steps for the ResShift baseline*

具体而言，在 NS（×2）上，ReMD-5 的 RMSE 为 0.0209，PSNR 达 49.94 dB，分别比 ResShift-15 降低 0.0012 和提升 0.47 dB；ReMD-2 也以 RMSE 0.0211、PSNR 49.84 dB 超越所有非扩散基线。在 ERA5（×4）上，ReMD-5 将 ResShift-15 的 RMSE 从 0.0879 降至 0.0802，PSNR 从 57.39 dB 提升至 58.19 dB。在 Ocean（×4）上，ReMD-2 以 RMSE 0.0132、PSNR 47.72 dB 超过 ResShift-15 的 0.0136 和 47.50 dB。

Figure 1 的定性对比揭示了 ReMD 的视觉优势：在 NS 上，ReMD-5 仅用 5 步即恢复出更锐利的细丝结构和连贯锋面，而 EDSR、FNO、SwinIR 等基线出现明显的环状或条带伪影；在 ERA5 上，ReMD 保留了中尺度剪切带，误差图显著更暗。Figure 3 的误差-能量谱分析进一步证实，ReMD-5 在从低频到高频的全频段上保持最低的傅里叶域误差，尤其在 LR Nyquist 频带以上的高频恢复中，明显优于 ResShift-15 和 FNO 等神经算子基线。

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative comparison on NS ( ×2 ) and ERA5 ( ×4 ). Each block shows (left) a zoomed LR input u0, (top row) HR reconstructions, and (bottom row) absolute error maps w.r.t. ground truth (shared color scale per block). With only 5 reverse steps, ReMD yields (NS) sharper filaments/coherent fronts and (ERA5) preserved mesoscale shear bands while suppressing ringing/stripe artifacts seen in EDSR/FNO/SwinIR, and achieves lower errors than ResShift despite requiring 5 vs. 15 steps*

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/004_Figure_3.jpg]]
*Figure 3: Error–energy spectrum on ERA5 (,×4,). Radial average of the Fourier-domain error (log scale on y) versus frequency (x). Vertical dashed lines mark the LR Nyquist band and the transition toward the HR band. ReMD-5 (red) maintains the lowest error from large to high scales, remaining below ResShift-15, FNO and image-SR baselines (EDSR, SwinIR), indicating superior spectral fidelity*

Figure 4 的补丁级细节对比显示，ReMD-5 在 NS（×4）上成功恢复了 HR 级别的锋面带和相干涡旋，而图像超分基线出现纹理/混叠伪影，FNO 则呈现块状失真。Figure 6 的能谱对比表明，ReMD 重建的湍流动能谱与真实 HR 最为吻合，尤其在惯性子区和耗散区。

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/005_Figure_4.jpg]]
*Figure 4: Patch-level comparison on NS (×4). Left: zoomed LR input. Black boxes highlight frontal bands; gray boxes mark small eddies. ReMD–5 recovers sharper, HR-like fronts and coherent vortices with fewer steps than ResShift–15, while avoiding texture/aliasing artifacts seen in image-SR baselines and blockiness in FNO, and remaining consistent with the LR content*

### 物理指标评估

Table 4 报告了物理一致性指标。在 NS2D（×4）上，ReMD 的涡度误差（VE）为 2.34×10⁻³，熵误差（EE）为 3.56×10⁻⁶，分别比 ResShift 降低 28.2% 和 67.9%。在 ERA5 uo（×4）上，ReMD 的能量差异（GED）为 4.24×10⁻³，优于 ResShift 的 4.51×10⁻³。在 ERA5 uo（×8）的极高倍率超分任务上，ReMD 同样取得最低 RMSE（0.323），验证了方法在更大缩放因子下的泛化能力。

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/009_Table_4.jpg]]
*Table 4: Physics-related metrics (lower is better ↓). VE/EE are vorticity/enstrophy errors on NS2D (×4). GED is the energy discrepancy on ERA5 uo (×4). The last column reports RMSE on ERA5 uo ×8 super-resolution*

### 效率分析

Table 3 对比了各方法在 NS 数据集上的效率。ReMD-5 在取得最优 RMSE/PSNR 的同时，推理时间比 ResShift-15 快约 1.4 倍；ReMD-2 的推理速度约为 ResShift-15 的 3.5 倍，且精度仍优于 ResShift。扩散基线 SR3 因需 100 步采样，推理成本显著更高。Figure 5 的时间-RMSE 权衡曲线直观展示了 ReMD 在极低步数下的优势：仅需 2 步即可达到 ResShift 15 步的精度水平。

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/007_Table_3.jpg]]
*Table 3: Efficiency on the NS. We report accuracy (RMSE↓/PSNR↑), parameter size, and wall-time (training time per epoch; inference time in seconds). Diffusion baselines (SR3, ResShift-15) incur high sampling cost; ReMD-5 attains the best accuracy with fewer steps and lower inference time than ResShift, while ReMD-2 is the fastest with competitive accuracy*

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/010_Figure_5.jpg]]
*Figure 5: Time–RMSE trade-off on ERA5 uo (×4 SR). Each point varies the sampling steps; lower-left is better*

### 消融实验

Table 2 在 Ocean（×4）上的消融实验揭示了各组件的贡献：

![[assets/figures/papers/paper_list_l911_https_arxiv_org_abs_2603_00149/figures/006_Table_2.jpg]]
*Table 2: Ablation study (OCEAN, 4× SR). Removing the MG corrector (“w/o residual correction”) or any physics residual (smoothing, anisotropic diffusion, spectrum) degrades all metrics; dropping the spectrum term yields the largest deterioration*

- **移除多网格残差校正器**（W/O RESIDUAL CORRECTION）：RMSE 从 1.33×10⁻² 升至 1.38×10⁻²，PSNR 下降 0.34 dB，证实多网格校正器对减少大尺度偏差的关键作用。
- **移除频谱残差**（W/O SPECTRUM RESIDUAL）：造成最大性能衰退，RMSE 升至 1.41×10⁻²，PSNR 降至 47.20 dB，表明频谱对齐对高频保真度的核心贡献。
- **移除平滑残差或各向异性扩散残差**：均导致所有指标下降，但影响略小于频谱残差。这些组件充当稳定器，抑制伪影并保持锋面结构。

消融结果验证了论文的核心设计逻辑：多网格校正器主要减少大尺度偏差，频谱残差贡献最大的高频保真度，而平滑和各向异性扩散残差作为互补的稳定机制。

### 失败模式与局限性

尽管 ReMD 在全频段误差上整体最优，论文指出其中频误差的减少效果不如低频或高频。这是因为多网格校正器天然偏向于消除低频偏差，频谱残差侧重高频对齐，而中频区域缺乏针对性的残差约束。此外，当前方法在像素空间操作，限制了极高目标分辨率下的内存和计算可扩展性。论文还指出，当前仅评估了单帧超分性能，未验证时间序列上的动态稳定性。

### 实验设置说明

所有方法使用相同的 RealESRGAN 退化协议生成 LR-HR 对（NS ×2，ERA5/Ocean ×4）。训练统一采用 Adam 优化器，学习率 5×10⁻⁵，批量大小 64，训练约 100k 迭代。扩散基线按原文献配置采样步数，ReMD 使用 DDIM 采样且仅用 2–5 步。评估指标统一采用 RMSE/PSNR/SSIM，并额外评估涡度误差、能量谱等物理相关指标，确保对比的公平性。

## 方法谱系与知识库定位

### 核心思路溯源：从算子学习到物理约束扩散

ReMD 的方法谱系可沿两条线索追溯。**第一条线索是流体超分辨率中的算子学习范式**。传统图像超分方法（如 **EDSR**、**SwinIR** (Liang et al., ICCV 2021)）将流体场视为自然图像，忽略了流体动力学内在的频谱结构和物理不变量。神经算子方法（如 **FNO** (Li et al., JMLR 2023)、**MWT** (Gupta et al., NeurIPS 2021)、**Galerkin Transformer** (Cao, NeurIPS 2021)）将超分建模为函数空间之间的映射，能够更好地保持频谱特性，但通常是单步前馈映射，缺乏迭代精化机制，且在复杂涡旋结构处易产生块状伪影。

**第二条线索是扩散模型在超分辨率中的应用**。**SR3** (Saharia et al., TPAMI 2022) 将去噪扩散引入图像超分，但依赖数百步采样，且无物理约束。**ResShift** (Yue et al., NeurIPS 2023) 通过将扩散过程从噪声-图像空间迁移到残差空间，将采样步数压缩至约15步，成为扩散超分的高效基线。然而，ResShift 的残差漂移方向仅由数据驱动的 UNet 预测，未显式编码物理一致性，导致频谱中频段误差累积和虚假散度。

ReMD 的关键创新在于**将这两条线索融合**：它保留了扩散模型的迭代精化框架，但在每一步逆过程中，用**物理引导的多网格残差校正器**替代纯数据驱动的噪声/残差预测。具体而言：

- **从 ResShift 继承**：残差空间扩散范式，以及 DDIM 采样的高效推理骨架。
- **超越 ResShift**：ReMD 将每步漂移方向 $e_t$ 分解为数据一致性残差 $u^{LR} - R(u)$ 与物理残差 $\rho(u)$ 的加权和，再经时间门控多网格校正器 $S_t$ 处理（Eq. 10），而非由 UNet 直接预测。
- **与多网格方法的关系**：ReMD 的多网格层级（Eq. 11）借鉴了经典数值线性代数中的 V-cycle 思想，但将其实现为**固定多小波基**的限制/延拓算子（Eq. 12），避免了传统多网格中依赖网格几何的插值，同时天然适配流体场的多尺度频谱特性。

### 与基线方法的关键差异

| 维度 | 图像超分基线 (EDSR, SwinIR) | 神经算子基线 (FNO, MWT) | 扩散基线 (SR3, ResShift) | **ReMD** |
|------|---------------------------|------------------------|--------------------------|----------|
| 物理约束 | 无 | 隐式（通过算子结构） | 无 | 显式可微物理残差（平滑、各向异性扩散、频谱对齐） |
| 多尺度机制 | 单尺度CNN/Transformer | 傅里叶/小波基 | UNet层次结构 | 时间门控多网格V-cycle + 多小波基 |
| 采样步数 | N/A（单步） | N/A（单步） | 100+ (SR3) / 15 (ResShift) | **2–5步** |
| 残差处理 | 直接预测HR | 直接映射 | 噪声/残差预测 | 数据一致性 + 物理残差的多尺度校正 |

### 适用边界与局限

1. **像素空间操作的内存瓶颈**：ReMD 在像素空间执行所有操作（物理残差计算、多网格校正），其每步复杂度虽为 $O(HW)$，但当目标分辨率极高时（如 2048×2048 以上），内存占用和绝对计算量仍构成瓶颈。论文明确指出的开放问题之一是将 ReMD 迁移到潜在空间，以解耦计算成本与 HR 网格大小。

2. **中频误差的“灰色地带”**：消融实验（Table 2）和频谱误差分析（Figure 3）表明，ReMD 在低频（多网格校正器主导）和高频（频谱残差主导）均表现优异，但**中频段误差减少幅度相对有限**。论文将此归因于当前物理残差集合缺乏针对中频的带通机制，建议引入带通残差和频谱感知损失。

3. **时间动态未评估**：当前 ReMD 为单帧超分模型，未在时间序列上验证动态稳定性。对于湍流等时间敏感场景，逐帧独立超分可能引入时间不一致的伪影。论文将此列为未来工作方向。

4. **物理残差的通用性边界**：当前物理残差（拉普拉斯平滑、各向异性扩散、频谱对齐）是方程无关的（equation-agnostic），适用于广泛的流体场景。但对于强激波、相变界面等需要强形式物理约束（如守恒律残差）的问题，现有残差集可能不足以完全抑制非物理解。

### 开放问题与未来方向

1. **潜在空间迁移**：如何将多网格校正器和物理残差迁移到潜在扩散框架（如 LDM），在低维潜在空间执行多尺度校正，从而将计算成本与 HR 网格解耦？

2. **中频增强**：如何设计带通频谱残差或频谱感知损失函数，针对性地减少中频误差？

3. **时间序列集成**：能否将 ReMD 作为“校正器”嵌入预测框架（如自回归神经算子），在时间推进的每一步对粗预测进行物理一致性超分，并评估长期稳定性？

4. **非结构化网格推广**：当前多小波限制/延拓算子依赖规则张量积网格。能否将其推广到非均匀网格或不规则区域（如球面海洋模型、有限元网格），保持频谱干净性和计算效率？

## 原文 PDF

![[paperPDFs/CVPR_2026/Physics_Consistent_Diffusion_for_Efficient_Fluid_Super_Resolution_via_Multiscale_Residual_Correction.pdf]]
