---
title: "HyperGaussians: High-Dimensional Gaussian Splatting for High-Fidelity Animatable Face Avatars"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HyperGaussians_High_Dimensional_Gaussian_Splatting_for_High_Fidelity_Animatable_Face_Avatars.pdf
project_link: "https://gserifi.github.io/HyperGaussians"
code_link: null
aliases:
- HyperGaussians
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将三维高斯扩展至更高维度，通过局部嵌入的条件分布对高斯属性进行动态调节，从而提升表达能力；配合逆协方差技巧实现高效计算。
primary_logic: HyperGaussians的本质是对3DGS场景的条件多变量高斯分布进行建模，通过MAP估计自适应地生成3D高斯属性；逆协方差技巧通过精度矩阵重参数化，将条件化计算复杂度从立方级降至线性级，使高维高斯溅射实时可行。
claims:
- HyperGaussians通过高维扩展和条件化局部嵌入，显著提升了对镜面反射、薄结构和复杂变形的渲染质量。
- 逆协方差技巧将条件化计算复杂度从O(n^3+mn^2)降至O(m^3+m^2n)，实现了高维高斯溅射的实时性。
- Monocular (19 subjects from 5 datasets) 上 PSNR ↑ = 29.99 (Ours FA)
- Monocular (19 subjects from 5 datasets) 上 SSIM (10⁻¹) ↑ = 9.510 (Ours FA)
---

# HyperGaussians: High-Dimensional Gaussian Splatting for High-Fidelity Animatable Face Avatars

> [!tip] 核心洞察
> HyperGaussians的本质是对3DGS场景的条件多变量高斯分布进行建模，通过MAP估计自适应地生成3D高斯属性；逆协方差技巧通过精度矩阵重参数化，将条件化计算复杂度从立方级降至线性级，使高维高斯溅射实时可行。

| 字段 | 内容 |
|------|------|
| 中文题名 | HyperGaussians：面向高保真可驱动面部化身的高维高斯溅射表示 |
| 英文题名 | HyperGaussians: High-Dimensional Gaussian Splatting for High-Fidelity Animatable Face Avatars |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.02803) · [Project](https://gserifi.github.io/HyperGaussians) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HyperGaussians |
| Dataset | Monocular, Multi-view |

> [!tip] 效果简介
> - Monocular (19 subjects from 5 datasets) 上，PSNR ↑ 29.99 (Ours FA) vs 29.43 (FlashAvatar) (+0.56)；SSIM (10⁻¹) ↑ 9.510 (Ours FA) vs 9.466 (FlashAvatar) (+0.044)；LPIPS (10⁻²) ↓ 4.978 (Ours FA) vs 5.107 (FlashAvatar) (-0.129)。
> - Multi-view (10 subjects from NeRSemble) 上，PSNR ↑ 24.38 (Ours GHA) vs 24.10 (GaussianHeadAvatar) (+0.28)；SSIM (10⁻¹) ↑ 8.819 (Ours GHA) vs 8.819 (GaussianHeadAvatar) (0.000)；LPIPS (10⁻²) ↓ 19.768 (Ours GHA) vs 20.273 (GaussianHeadAvatar) (-0.505)。

## 概要

**问题瓶颈**：现有基于3D高斯溅射（3DGS）的面部化身方法在表达非线性变形、镜面反射和微细结构时受限，难以高效捕捉高频细节，导致渲染质量不足。

**核心方法**：HyperGaussians将三维高斯扩展至更高维度（属性维度 $m=3$，潜在维度 $n=8$），通过局部嵌入的条件分布对高斯属性进行动态调节。其本质是对3DGS场景的条件多变量高斯分布建模，利用最大后验（MAP）估计自适应生成3D高斯属性。关键创新是**逆协方差技巧**——通过精度矩阵重参数化，将条件化计算复杂度从 $O(n^3 + mn^2)$ 降至 $O(m^3 + m^2n)$，使高维高斯溅射实时可行。

**方法定位**：HyperGaussians是一种即插即用的增强模块，可无缝集成到现有面部化身流程中（如FlashAvatar、GaussianHeadAvatar），仅需将形变MLP的输出从直接偏移预测改为潜在编码预测，通过HyperGaussians条件化恢复等效3D高斯属性后送入可微光栅器。

**主要结果**：在29名受试者、6个面部数据集上，HyperGaussians以最小开销显著提升渲染质量。单目设置下，集成HyperGaussians的FlashAvatar相比原版PSNR提升0.56 dB（29.99 vs 29.43），LPIPS降低0.129；多视图设置下，集成HyperGaussians的GaussianHeadAvatar在LPIPS上降低0.505。定性上，HyperGaussians在镜面反射、薄结构（眼镜框、牙齿）和复杂变形（嘴部）等高频细节上表现突出。消融实验表明，单纯增加MLP深度（至40层）会导致LPIPS恶化15%且帧率下降47%，而HyperGaussians在保持渲染速度的同时实现了更优的表达能力。

### 问题背景：面部化身的实时高保真渲染

数字化身是沉浸式通信、虚拟现实和影视游戏等应用的核心技术。近年来，基于**3D Gaussian Splatting (3DGS)** 的显式表示方法凭借其可微光栅化带来的实时渲染能力，在面部化身重建领域展现出巨大潜力。这类方法通常将面部几何表示为一组三维高斯原语，每个原语由位置、旋转、缩放和不透明度等属性定义，并通过与FLAME等参数化面部模型的网格绑定来实现表情驱动。

然而，面部是人体最具表现力的区域，包含大量高频细节：镜面反射（如眼球光泽和眼镜反光）、薄结构（如眼镜框、牙齿缝隙）、以及由复杂非线性变形产生的微细皱纹。这些细节对渲染质量至关重要，却恰恰是现有3DGS方法难以有效捕捉的瓶颈。

### 现有方法的缺口：表达能力的根本限制

当前基于3DGS的面部化身方法面临一个根本性矛盾：**高斯原语的表达能力受限于其低维参数空间**。具体而言，标准3DGS中的每个高斯体由固定的位置、旋转和缩放参数表征，当需要适应不同表情时，现有方法通常通过一个MLP直接预测这些属性的偏移量（offsets）。这种直接预测方式隐含地假设属性变化是输入条件的线性或浅层非线性函数，难以建模复杂的条件依赖关系。

从概率视角看，现有方法实际上是在学习一个从表情参数到高斯属性的**确定性映射**，而忽略了属性之间以及属性与表情之间的**联合分布结构**。当面对镜面反射随头部姿态的非线性位移、或薄结构在不同表情下的复杂变形时，这种确定性、低维度的表示方式不可避免地导致细节丢失和渲染伪影。

此外，一个直观的改进思路是增加MLP的深度或宽度来提升表达能力，但消融实验表明，单纯将MLP深度增加至40层不仅导致LPIPS指标恶化15%，还使渲染帧率从300 FPS骤降至158 FPS（下降47%）。这说明**网络容量的粗暴扩张并非有效解法**，反而破坏了实时性这一核心优势。

### 核心动机：从“预测偏移”到“条件生成”

本文的核心动机源于一个关键洞察：**不应让MLP直接预测高斯属性的偏移量，而应让MLP输出一个潜在编码，通过一个条件概率模型来“生成”适应表情的高斯属性**。这一思路将问题从确定性回归提升为条件多变量高斯分布建模——即学习高斯属性与潜在编码的联合分布，在推理时通过条件化得到表情相关的属性后验。

这种条件生成范式天然具备更强的表达能力：条件均值等价于最大后验（MAP）估计，能够在全局先验和局部观测之间取得最优平衡；条件协方差则提供了对预测不确定性的自然度量，无需额外监督即可反映不同面部区域对表情变化的敏感程度差异。

### 技术挑战：高维条件化的计算瓶颈

将上述思路付诸实践面临一个关键障碍：**计算效率**。如果直接在3D高斯属性的基础上附加潜在维度，构成一个$(m+n)$维的多元高斯分布（其中$m=3$为属性维度，$n$为潜在维度），那么条件化计算涉及对$n \times n$协方差块求逆，复杂度为$\mathcal{O}(n^3 + m n^2)$。对于包含数万个高斯体的场景，这一成本将彻底摧毁实时渲染的可能性。

因此，本文的核心技术动机是：**如何在保持条件生成表达能力的同时，将计算复杂度降至实时可行的水平？** 这一问题的解决，是HyperGaussians能够成为即插即用增强模块的前提。

## 核心方法与创新机理

HyperGaussians 的核心创新在于对 3D 高斯溅射（3DGS）表示本身的重构：将高斯原语从三维属性空间扩展至**高维多元高斯**，并通过**条件化机制**和**逆协方差技巧**实现表达力与计算效率的双重突破。

### 1. 从三维到高维的高斯原语扩展

现有基于 3DGS 的面部化身方法将每个高斯原语定义在三维空间中，其属性（位置、缩放、旋转）由 MLP 直接预测偏移量 Δ 进行调节。这种低维表示难以高效捕捉镜面反射、薄结构和复杂变形等高频细节。

HyperGaussians 将高斯原语从 3 维扩展至 **(m+n) 维**，其中 m=3 为属性维度（μ_3D, s, q），n=8 为潜在维度 z。这一扩展的本质是对动态场景的**条件多变量高斯分布**进行建模——通过联合分布 p(A, z) 刻画属性与潜在编码之间的统计依赖，从而赋予每个高斯原语根据局部嵌入自适应调节的能力。

### 2. 条件化预测取代直接偏移回归

在 baseline 方法（如 **FlashAvatar** (Xiang et al., 2024)）中，变形 MLP 直接输出每个高斯体的偏移量 Δ。HyperGaussians 仅做一处修改：让 MLP 输出**潜在编码 z_ψ**，然后通过条件化高维高斯得到属性偏移的均值：

$$\mathbb{E}[\mathcal{A}|z] = \arg\max_{\mathcal{A}} p(\mathcal{A}|z)$$

对于高斯分布，条件均值等价于最大后验（MAP）估计。这意味着 HyperGaussians 并非简单地回归偏移量，而是从概率分布中推断最可能的属性配置。这种概率化建模不仅提升了表达能力，还天然提供了**不确定性估计**——条件协方差 Σ_{a|b} 的行列式 σ 可反映形变不确定性，无需额外监督信号。

### 3. 逆协方差技巧：从立方到线性的复杂度跃迁

高维高斯条件化的直接计算需要对 n×n 的协方差子块 Σ_{bb} 求逆，复杂度为 O(n³ + mn²)，这在高斯体数量庞大时（如 ~15k 个原语）将导致计算不可行。

HyperGaussians 提出**逆协方差技巧**：转而存储和操作精度矩阵（协方差的逆）Λ = Σ⁻¹，利用分块形式将条件化计算重新表达为：

$$\mu_{a|b} = \mu_a - \Lambda_{aa}^{-1} \Lambda_{ab} (\gamma_b - \mu_b), \quad \Sigma_{a|b} = \Lambda_{aa}^{-1}$$

此时仅需对 m×m 的 Λ_{aa}（m ∈ {3,4}）求逆，复杂度骤降至 **O(m³ + m²n)**，与潜在维度 n 呈线性关系。当 n=8 时，该技巧使条件化速度提升 150%，内存占用从 42 MB 降至 22 MB（降低 48%）；更高维度下收益更为显著。这是高维高斯溅射得以实时运行的关键使能技术。

### 4. 与高维高斯基线 NDGS 的差异

**NDGS** (引用[13]) 同样探索了高维高斯表示，但 HyperGaussians 与之的核心差异在于：NDGS 未采用逆协方差技巧，其条件化计算仍受限于 O(n³) 复杂度；而 HyperGaussians 通过精度矩阵重参数化，将条件化计算与潜在维度解耦，使得在实际面部化身任务中使用 n=8 甚至更高维度成为可能。

### 5. 插拔式设计

HyperGaussians 被设计为**即插即用**的增强模块。在 FlashAvatar 和 **GaussianHeadAvatar** (Xu et al., 2024) 上，仅需将 MLP 输出从偏移量改为潜在编码，并在光栅化前插入条件化步骤，无需修改网络架构、训练策略或损失函数。训练时间仅增加约 30 分钟（约 1%），渲染帧率保持 300 FPS，实现了表达力与效率的平衡。

HyperGaussians 的核心设计理念是对 3DGS 原语进行高维扩展，使其具备根据局部嵌入动态调节自身属性的能力。整个流水线由四个紧密耦合的模块构成：高维高斯表示、MLP 潜变量预测、条件化降维和可微光栅化，其输入输出流如图 2 所示。

**高维高斯表示 (HyperGaussians)** 将传统的 3D 高斯从 `(m=3)` 属性维度扩展至 `(m+n)` 维，其中 `m` 为 3D 高斯属性维度（位置 `μ_3D`、缩放 `s`、旋转 `q`），`n=8` 为潜在维度。每个高斯原语维护一个完整的 `(m+n)` 维多元高斯分布，通过联合分布建模属性与潜在变量之间的统计依赖关系。这一扩展使得高斯原语不再是一个静态的几何基元，而是一个能够表达丰富条件依赖的概率模型。

**MLP 潜变量预测** 取代了基线方法中直接预测偏移量 `∆` 的做法。具体而言，变形 MLP 接收 FLAME 表达参数 `ψ` 和网格位置作为输入，输出每个高斯体对应的潜在编码 `z_ψ`，而非直接输出位置、旋转和缩放的偏移量。这一修改是 HyperGaussians 与 FlashAvatar 等基线方法的唯一架构差异，其余模块保持不变。

**条件化降维** 是连接高维表示与标准渲染管线的关键桥梁。给定 MLP 预测的潜在编码 `z_ψ`，系统对 HyperGaussians 进行条件化，计算条件分布 `p(A|z)` 的均值，从而恢复等效的 3D 高斯属性。条件均值的计算等价于最大后验估计 `argmax_A p(A|z)`，为整个过程提供了坚实的概率解释。为实现高效计算，HyperGaussians 采用精度矩阵重参数化，将条件化计算复杂度从 `O(n³ + mn²)` 降至 `O(m³ + m²n)`，使得 `n=8` 时条件化速度提升 150%，内存占用降低 48%。

**可微光栅化** 直接复用标准 3DGS 的可微光栅器。条件化后的 3D 高斯与 vanilla 3DGS 完全兼容，无需任何修改即可送入光栅化管线进行渲染和梯度回传。

整个流水线的数据流可以概括为：FLAME 参数 → MLP 潜变量预测 → HyperGaussians 条件化 → 等效 3D 高斯属性 → 可微光栅化 → 渲染图像。HyperGaussians 以即插即用的方式集成到现有方法中，训练时间仅增加约 1%（约 30 分钟），渲染帧率保持在 300 FPS 以上，实现了表达能力与计算效率的平衡。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/002_Figure_2.jpg]]
*Figure 2: We propose an expressive extension to 3D Gaussians, dubbed HyperGaussians, and plug them into existing methods for face avatars, FlashAvatar [70] and GaussianHeadAvatar [71]. FlashAvatar modulates 3D Gaussian primitives with expression-dependent offsets ∆. We make a single modification to the pipeline: plugging HyperGaussians (Sec. 3.2) in between the MLP output and the rasterization, which modifies the offsets ∆ in higher dimensions. Instead of directly predicting offsets ∆, we predict a latent zψ that conditions HyperGaussians. Without any other modifications or hyperparameter tuning, this simple change leads to a performance boost in rendering high-frequency details in the final avatar (...*

### 3DGS 协方差构建（前置基础）

3DGS 将场景表示为三维高斯体集合，每个高斯体由位置 $\mu_{3D}$、缩放矩阵 $S$ 和旋转矩阵 $R$ 参数化。协方差矩阵按以下方式构造：

$$\Sigma_{3D} = R S S^{\top} R^{\top}$$

该公式确保 $\Sigma_{3D}$ 是半正定矩阵，从而定义了一个有效的三维高斯分布。缩放 $S$ 和旋转 $R$ 均可优化，使高斯体在渲染过程中自适应调整形状和朝向。

### HyperGaussians 高维扩展

HyperGaussians 将传统 3D 高斯体从 $m$ 维属性空间扩展至 $(m+n)$ 维联合空间，其中 $m$ 为属性维度（位置 $\mu_{3D}$、缩放 $s$、旋转 $q$），$n$ 为潜在维度。每个 HyperGaussian 的均值 $\boldsymbol{\mu}$ 和协方差 $\boldsymbol{\Sigma}$ 采用分块形式：

$$\boldsymbol{\mu} = \begin{bmatrix} \boldsymbol{\mu}_a \\ \boldsymbol{\mu}_b \end{bmatrix}, \quad \boldsymbol{\Sigma} = \begin{bmatrix} \boldsymbol{\Sigma}_{aa} & \boldsymbol{\Sigma}_{ab} \\ \boldsymbol{\Sigma}_{ba} & \boldsymbol{\Sigma}_{bb} \end{bmatrix}$$

其中下标 $a$ 对应属性块，$b$ 对应潜在块。这一扩展使高斯体能够通过条件化机制动态适应局部嵌入，从而表达镜面反射、薄结构和复杂变形等高频细节。

### 条件化降维与 MAP 估计

渲染前需将高维 HyperGaussians 条件化至属性维度，得到等效的 3D 高斯体。条件化过程具有明确的概率解释：对于高斯分布，条件均值等价于最大后验估计：

$$\mathbb{E}[\mathcal{A}|z] = \arg\max_{\mathcal{A}} p(\mathcal{A}|z)$$

这意味着 HyperGaussians 在给定潜在编码 $z$ 时，通过 MAP 估计自适应地生成 3D 高斯属性，而非直接预测偏移量。

### 逆协方差技巧

直接对协方差块 $\boldsymbol{\Sigma}_{bb}$ 求逆的条件化计算复杂度为 $\mathcal{O}(n^3 + mn^2)$，当潜在维度 $n$ 增大时不可行。逆协方差技巧通过精度矩阵（协方差的逆）重参数化解决该问题。定义精度矩阵 $\boldsymbol{\Lambda} = \boldsymbol{\Sigma}^{-1}$，其分块形式为：

$$\boldsymbol{\Lambda} = \begin{bmatrix} \boldsymbol{\Lambda}_{aa} & \boldsymbol{\Lambda}_{ab} \\ \boldsymbol{\Lambda}_{ba} & \boldsymbol{\Lambda}_{bb} \end{bmatrix}$$

利用精度矩阵块，条件均值和条件协方差可高效计算：

$$\mu_{a|b} = \mu_a - \boldsymbol{\Lambda}_{aa}^{-1} \boldsymbol{\Lambda}_{ab} (\gamma_b - \mu_b), \quad \Sigma_{a|b} = \boldsymbol{\Lambda}_{aa}^{-1}$$

**关键收益**：仅需存储和求逆较小的 $\boldsymbol{\Lambda}_{aa} \in \mathbb{R}^{m \times m}$（$m \in \{3,4\}$），将条件化复杂度从 $\mathcal{O}(n^3 + mn^2)$ 降至 $\mathcal{O}(m^3 + m^2 n)$，与潜在维度 $n$ 呈线性关系。实验表明，当 $n=8$ 时条件化速度提升 150%，内存占用降低 48%。

### 不确定性度量

HyperGaussians 的条件协方差行列式可自然导出不确定性度量，无需额外监督：

$$\sigma = \log\det\Sigma_{a|b} = -2\operatorname{tr}\log L_{11}$$

其中 $L_{11}$ 为 $\boldsymbol{\Lambda}_{aa}$ 的 Cholesky 分解因子。该度量反映形变预测的置信度，语义结构（如面部高变形区域）可自发涌现。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/003_Figure_3.jpg]]
*Figure 3: Benchmark Results on conditioning for ∼15k Hyper-Gaussians with attribute dimension*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/008_Figure_7.jpg]]
*Figure 7: Geometric interpretation of Gaussian conditioning on two examples with large (left) and small (right) uncertainty at different realizations of*

## 实验与关键发现

### 核心定量结果

HyperGaussians作为一种即插即用的高维高斯扩展，在单目和多视图两种面部化身重建设定下均带来一致的性能提升。Table 1汇总了主要定量对比结果。

在单目设定下（19名受试者，来自5个数据集），将HyperGaussians插入**FlashAvatar**（Xiang et al., 2024）后，PSNR从29.43 dB提升至**29.99 dB**（+0.56 dB），SSIM从0.9466提升至**0.9510**（+0.0044），LPIPS从0.05107降至**0.04978**（-0.00129）。值得注意的是，方法间的**唯一差异仅在于高斯表示本身**——FlashAvatar的MLP输出被改为潜在编码，其余架构、训练策略和超参数完全保持一致。这意味着上述增益完全归因于HyperGaussians更强的表达能力。

在多视图设定下（NeRSemble数据集的10名受试者），将HyperGaussians插入**GaussianHeadAvatar**（Xu et al., 2024）后，PSNR从24.10 dB提升至**24.38 dB**（+0.28 dB），LPIPS从0.20273降至**0.19768**（-0.00505），SSIM保持持平（0.8819）。训练时间仅增加约30分钟（约1%），考虑到多视图训练总时长超过2天，这一开销几乎可以忽略。

### 定性分析

Figure 4展示了自驱动场景下的定性对比。HyperGaussians在以下三类高难度细节上展现出明显优势：

1. **薄结构**：眼镜框和牙齿等细薄几何结构在基线方法中常出现断裂或模糊，HyperGaussians能保持清晰连续的边缘。
2. **镜面反射**：眼睛和眼镜上的高光反射随视角变化而自然位移，基线方法往往丢失或错误渲染这类与视角相关的效果。
3. **复杂变形**：嘴部区域的大幅度非刚性变形在基线方法中易产生伪影，HyperGaussians能优雅地处理这些形变。

跨驱动场景（Figure 5）进一步验证了HyperGaussians的泛化能力：当用未见过的表情参数驱动化身时，牙齿细节和整体面部形状得到更好保留。

多视图设定下的定性提升（Figure 6）同样显著：将GaussianHeadAvatar增强后，皱纹、眼睛反射、眼镜高光和牙齿细节等高频信息明显增强。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/007_Figure_6.jpg]]
*Figure 6: Enhancing GaussianHeadAvatars [71] with HyperGaussians boosts high-frequency details like wrinkles and reflections in the eyes, glasses, and teeth. See Tab. 1 for metrics*

### 消融实验

**与更深/更宽MLP的对比。** 一个自然的质疑是：HyperGaussians的性能提升是否仅仅来自参数量的增加？Table 4的消融实验给出了明确否定。将FlashAvatar的形变MLP深度增加至40层（参数量显著增大），LPIPS反而**恶化15%**（从0.0498升至0.0572），渲染帧率从300 FPS**骤降47%**至158 FPS。将MLP宽度加倍同样导致LPIPS恶化3%且帧率下降41%。相比之下，HyperGaussians在几乎不增加推理开销的前提下实现了更优的感知质量——这证明高维条件化建模比简单堆叠MLP参数更有效。

**潜在维度鲁棒性。** HyperGaussians对潜在维度n表现出良好的鲁棒性。实验表明，n=8取得最佳综合性能，但即使n=1（仅增加一个潜在维度），性能也超过vanilla 3DGS基线。这表明高维扩展的收益并非简单线性累积，而是源于条件化机制本身对表达空间的扩充。

**逆协方差技巧的效率。** Figure 3的基准测试量化了逆协方差技巧的计算收益。对于约15k个HyperGaussians（属性维度m=3），当潜在维度n=8时，条件化计算速度**提升150%**，内存占用从42 MB降至22 MB（**降低48%**）。随着n增大，收益更加显著——这正是将高维高斯溅射推向实时应用的关键使能技术。该技巧将条件化复杂度从原始的O(n³ + m n²)降至O(m³ + m² n)，由于m∈{3,4}远小于n，实际计算量大幅缩减。

**与高维高斯基线NDGS的对比。** Table 3显示，直接使用**NDGS**的高维高斯表示无法匹配HyperGaussians的改进幅度：在多视图设定下，NDGS在PSNR和LPIPS上均逊于HyperGaussians，仅在SSIM上有微弱提升。这凸显了HyperGaussians设计中条件化机制和逆协方差技巧的独特价值——并非所有高维扩展都能等效地提升渲染质量。

### 失败模式与局限性

论文未明确报告HyperGaussians的失败案例，但可从方法设计推断潜在局限：

1. **对3DMM先验的依赖**：当前实现依赖FLAME网格提供空间锚点和形变先验，在无参数化面部模型的场景（如全身、通用物体）中尚需验证。
2. **高维存储开销**：尽管逆协方差技巧大幅降低了条件化的计算和内存，每个HyperGaussian仍需存储精度矩阵块Λ_aa和Λ_ab。当高斯体数量或潜在维度进一步增大时，存储成本可能成为瓶颈。
3. **不确定性估计的利用不足**：论文推导了条件协方差行列式作为不确定性度量σ，但未在实验中展示其实际应用价值（如主动学习、稀疏视角重建等），这一潜力有待后续工作挖掘。

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | HyperGaussians在单目和多视图设定下一致提升PSNR/SSIM/LPIPS，且训练开销可忽略 |
| Figure 4 | 薄结构、镜面反射、复杂变形三类高难度细节的定性优势 |
| Figure 5 | 跨驱动场景下牙齿细节和面部形状保持更好 |
| Figure 6 | 多视图设定下皱纹、反射等高频细节显著增强 |
| Table 4 | 加深/加宽MLP无法复现HyperGaussians的增益，反而损害感知质量和推理速度 |
| Figure 3 | 逆协方差技巧在n=8时提速150%、内存降低48%，是实现实时高维溅射的关键 |
| Table 3 | NDGS的高维扩展无法匹配HyperGaussians的性能，条件化机制不可或缺 |

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art digital avatar reconstruction methods from monocular video across 19 subjects from 5 datasets [15, 17, 21, 76, 79] (top) and from multi-view video across 10 subjects from NeRSemble [28] (bottom). Ours (FA) and Ours (GHA) correspond to FlashAvatar and GaussianHeadAvatar with 8-dimensional HyperGaussians without any other modifications. Please see Sec. 3.3 for details*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/012_Table_4.jpg]]
*Table 4: MLP and Latent Dimensionality Ablations. Simply increasing the parameter count for the FlashAvatar MLP does not improve the metrics. Our HyperGaussians, however, improve the performance of the original MLP out-of-the-box. As an additional benefit, HyperGaussians render at around 300 FPS while the deeper MLPs, with comparable parameter counts, drop to 158 FPS (256×40) and 178 FPS (512×11), respectively. Note that the drop of 10 FPS for 1D is likely due to memory bottlenecks caused by poor cache and vector load/store locality. Green denotes the best and Yellow the second best*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/013_Table_3.jpg]]
*Table 3: Quantitative comparison with GHA and NDGS in the multi-view setting. Notice that NDGS is unable to match the improvements of HyperGaussians in terms of PSNR and LPIPS, and performs only marginally better on SSIM. This highlights the limited capabilities of NDGS due to its reduced degrees of freedom*

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/009_Table_2.jpg]]
*Table 2: Differences to the most closely related works. GaussianAvatars [57] and SuRFHead [31] deform 3D Gaussians based on an underlying FLAME mesh [38] without local embeddings or dynamic inputs like facial expressions. SplattingAvatar [60] optimizes local embeddings, but the Gaussian properties are not dependent on expressions or pose. MonoGaussianAvatar [10], FlashAvatar [70], and GaussianHeadAvatar [71] predict expression-dependent offsets to the Gaussian properties, but their lack of local context leads to blurry or distorted results, see comparison in the main paper. Our proposed representation (HGS) attaches high-dimensional Gaussians to the mesh and optimizes learnable local embeddings for...*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/011_Figure_9.jpg]]
*Figure 9: Comparison with NDGS integrated into FlashAvatar. The limited degrees of freedom in NDGS lead to misalignments of thin structures and edges. The numbers show PSNR, SSIM*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/015_Figure_11.jpg]]
*Figure 11: Qualitative comparison for varying latent dimensionalities. We find that HyperGaussians are robust towards different latent dimensions. A latent dimension of 8 performs best, but we already observe an improvement for a single latent dimension (n = 1) over the vanilla 3DGS variant*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2507_02803/figures/005_Figure.jpg]]

## 定位与知识库关联

### 一、核心问题与差异化定位

现有基于3DGS的面部化身方法面临一个共同瓶颈：3D高斯原语仅能表达静态的3D协方差结构，难以高效建模非线性变形、镜面反射和微细结构等高频细节。这导致渲染质量在面对复杂表情变化或视角变化时明显不足。

HyperGaussians的差异化策略在于**将3D高斯扩展至更高维度**，通过局部嵌入（local embedding）的条件分布对高斯属性进行动态调节。其本质是对3DGS场景的条件多变量高斯分布进行建模——将属性维度（位置、缩放、旋转）与潜在维度联合建模为一个 $(m+n)$ 维多元高斯，再通过条件化 $p(\mathcal{A}|z)$ 自适应地生成3D高斯属性。这一设计使得每个高斯原语具备了根据局部编码动态调整的能力，从而显著提升了对镜面反射、薄结构和复杂变形的表达能力。

### 二、与现有工作的关系矩阵

#### 2.1 直接集成的基线方法

HyperGaussians被设计为即插即用的增强模块，直接嵌入两个代表性基线：

- **FlashAvatar**（Xiang et al., 2024）：单目面部化身方法。原方法使用MLP直接预测每个高斯体的偏移量 $\Delta$（位置、旋转、缩放），HyperGaussians将其替换为：MLP输出潜在编码 $z_\psi$，通过HyperGaussians条件化得到偏移量的均值。这是唯一的架构修改。
  
- **GaussianHeadAvatar**（Xu et al., 2024）：多视图面部化身方法。同样将偏移量预测替换为潜在编码预测+HyperGaussians条件化。

实验表明，这一最小化修改在两个基线上均带来一致的性能提升：在单目设置下PSNR提升0.56 dB，LPIPS降低0.129；在多视图设置下LPIPS降低0.505（Table 1）。

#### 2.2 同属高维高斯扩展的方法

**NDGS**是唯一明确的高维高斯基线。HyperGaussians与NDGS的关键区别在于**逆协方差技巧**：NDGS直接对协方差矩阵 $\Sigma_{bb}$ 求逆，计算复杂度为 $O(n^3 + mn^2)$；HyperGaussians采用精度矩阵重参数化，仅需对 $\Lambda_{aa} \in \mathbb{R}^{m \times m}$（$m \in \{3, 4\}$）求逆，复杂度降至 $O(m^3 + m^2 n)$。这一技巧使得高维高斯溅射的实时渲染成为可能——在 $n=8$ 时条件化速度提升150%，内存占用降低48%。

#### 2.3 其他面部化身方法的对比定位

Table 2对最相关的工作进行了系统区分：

- **GaussianAvatars**和 **SuRFHead**：基于FLAME网格变形3D高斯，但缺乏局部嵌入或动态输入（如面部表情），无法自适应地调节高斯属性。
  
- **SplattingAvatar**：优化局部嵌入但使用标准3D高斯，未扩展到高维空间。

- **MonoGaussianAvatar**：单目方法，采用传统3DGS表示。

HyperGaussians的核心区别在于**将局部嵌入与高维高斯联合建模**，通过条件化实现属性维度的动态生成，而非直接预测偏移量。

### 三、适用边界与局限

#### 3.1 已验证的适用场景

- **单目面部重建**：19个受试者、5个数据集的广泛验证，PSNR 29.99，SSIM 0.9510，LPIPS 0.04978。
- **多视图面部重建**：NeRSemble数据集10个受试者，PSNR 24.38，LPIPS 0.19768。
- **跨驱动（cross-reenactment）**：保留牙齿细节和整体形状（Figure 5）。
- **即插即用集成**：训练时间仅增加约30分钟（1%开销），渲染速度保持300 FPS。

#### 3.2 已知局限

从消融实验可推断以下边界：

- **MLP深度/宽度增加无法替代高维扩展**：将MLP深度增至40层导致LPIPS恶化15%，渲染帧率从300 FPS降至158 FPS（下降47%）；增加宽度导致LPIPS恶化3%，帧率降至178 FPS（下降41%）。这表明单纯增加网络容量无法达到HyperGaussians的表达能力。

- **潜在维度稳健但存在最优区间**：$n=8$ 取得最佳性能，$n=1$ 已超过基线，但更高维度可能带来边际收益递减。

#### 3.3 需要人工验证的开放问题

以下问题在论文中未被实验覆盖，需要进一步研究：

1. **泛化到非面部场景**：HyperGaussians能否扩展至全身化身或其他动态场景（如手部、衣物）？当前验证仅限于面部数据。

2. **无3DMM先验的应用**：当前方法依赖FLAME参数模型提供表达编码 $\psi$，是否可以在无3DMM先验的情况下应用HyperGaussians（例如直接从图像特征预测 $z$）？

3. **内存与维度的权衡**：逆协方差技巧已将内存从42 MB降至22 MB（$n=8$），但更高维度的潜变量或更多高斯体仍可能成为瓶颈。如何进一步压缩？

4. **不确定性估计的下游应用**：HyperGaussians可无监督地输出不确定性度量 $\sigma = \log\det\Sigma_{a|b}$（Eq. 13），该信号能否用于主动学习、稀疏视角重建或异常检测？

### 四、方法谱系总结

HyperGaussians在3DGS表示谱系中占据**条件化高维扩展**的位置：

- **表示维度**：从3D高斯（$m=3, n=0$）扩展到高维高斯（$m=3$属性维度，$n=8$潜在维度）。
- **动态预测范式**：从“MLP→偏移量 $\Delta$”的直接预测，转变为“MLP→潜在编码 $z$→条件化→均值偏移”的概率生成范式。
- **计算效率**：通过逆协方差技巧，将条件化计算复杂度从立方级降至线性级，使高维表示实时可行。

这一设计使得HyperGaussians在保持3DGS渲染效率的同时，显著提升了高频细节的表达能力，为动态场景的高斯表示提供了一个可扩展的概率框架。

## 原文 PDF

![[paperPDFs/CVPR_2026/HyperGaussians_High_Dimensional_Gaussian_Splatting_for_High_Fidelity_Animatable_Face_Avatars.pdf]]
