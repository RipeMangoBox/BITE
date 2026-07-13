---
title: "GP-4DGS: Probabilistic 4D Gaussian Splatting from Monocular Video via Variational Gaussian Processes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GP_4DGS_Probabilistic_4D_Gaussian_Splatting_from_Monocular_Video_via_Variational_Gaussian_Processes.pdf
project_link: null
code_link: null
aliases:
- G4
- GP-4DGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将高斯过程（GP）作为显式概率运动先验整合到4DGS框架中，通过变分推断实现可扩展的概率建模，提供不确定性量化和数据自适应正则化。
primary_logic: 利用高斯过程的后验分布为每个高斯基元的形变提供均值和方差，自动根据观测置信度调整正则化强度；通过时空分解核与交替优化（GP‑GS Optimization）从可信观测中学习运动先验，并在未观测区域中传播约束。
claims:
- GP‑4DGS引入三项确定性方法不具备的能力：运动不确定性量化、未观测区域运动估计、训练帧以外的时间外推。
- 在DyCheck数据集上，GP‑4DGS在所有子集上均优于最强基线SoM，尤其在稀疏观测的挑战性子集上优势更明显。
- GP‑GS交替优化（置信度采样的GP训练 + GP引导的GS正则化）使重建质量相比单独优化显著提升。
- DyCheck (SoM 5 scenes) 上 mPSNR↑ = 16.92
---

# GP-4DGS: Probabilistic 4D Gaussian Splatting from Monocular Video via Variational Gaussian Processes

> [!tip] 核心洞察
> 利用高斯过程的后验分布为每个高斯基元的形变提供均值和方差，自动根据观测置信度调整正则化强度；通过时空分解核与交替优化（GP‑GS Optimization）从可信观测中学习运动先验，并在未观测区域中传播约束。

| 字段 | 内容 |
|------|------|
| 中文题名 | GP-4DGS：基于变分高斯过程的概率性单目视频4D高斯泼溅 |
| 英文题名 | GP-4DGS: Probabilistic 4D Gaussian Splatting from Monocular Video via Variational Gaussian Processes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02915) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GP-4DGS |
| Dataset | DyCheck, DyCheck Challenging subset |

> [!tip] 效果简介
> - DyCheck (SoM 5 scenes) 上，mPSNR↑ 16.92 vs 16.73 (SoM) (+0.19)；mSSIM↑ 0.66 vs 0.64 (SoM) (+0.02)；mLPIPS↓ 0.41 vs 0.43 (SoM) (-0.02)。
> - DyCheck Challenging subset 上，mPSNR↑ 15.02 vs 14.56 (SoM) (+0.46)。

## 概要

单目视频的动态场景重建是计算机视觉中的基础问题，现有方法普遍采用确定性建模范式——它们直接回归每个高斯基元的形变参数，却无法回答“这个预测有多可靠”。这种确定性假设在遮挡、稀疏观测或超出训练分布的区域暴露出根本性缺陷：模型缺乏对预测不确定性的感知，难以区分可信观测与不可信区域，也无法在未观测时空位置做出有意义的推断。

**核心瓶颈**：现有4DGS方法仅支持确定性重建，无法捕捉运动模糊，缺乏预测可靠性评估机制，在遮挡或观测不足区域性能显著下降。

**GP‑4DGS** 将高斯过程（Gaussian Process, GP）作为显式概率运动先验整合到4D Gaussian Splatting框架中，通过变分推断实现可扩展的概率建模。其核心洞察在于：利用GP后验分布为每个高斯基元的形变同时提供均值和方差，使模型能够自动根据观测置信度调整正则化强度——充分观测区域保持高保真重建，稀疏观测区域则由学到的运动先验提供合理约束。

**三项确定性方法不具备的新能力**：
- **运动不确定性量化**：渲染图像的同时生成逐像素的运动不确定性图，标识重建不可靠区域；
- **未观测区域运动估计**：通过时空GP先验将运动约束传播到观测不足的区域；
- **训练帧以外的时间外推**：查询训练时间范围外的GP模型，自然预测未来运动。

在DyCheck数据集上，GP‑4DGS在所有子集上均优于最强确定性基线**SoM**（Wang et al., ICCV 2025），尤其在稀疏观测的挑战性子集上优势更明显（mPSNR +0.46）。方法的核心创新——GP‑GS交替优化策略——通过置信度加权的GP训练与GP引导的GS正则化形成自我强化循环，使重建质量相比单独优化显著提升。



### 动态场景重建的确定性困境

从单目视频重建动态3D场景是计算机视觉与图形学中的核心挑战。近年来，以**3D Gaussian Splatting**（3DGS）为基础的4D扩展方法取得了显著进展，代表性工作包括**4DGS**（Wu et al., CVPR 2024）的HexPlane形变、**D-3DGS**（Yang et al., CVPR 2024）的MLP形变，以及**Gaussian Marbles**（Stearns et al., SIGGRAPH 2024）和**SoM**（Wang et al., ICCV 2025）等面向单目视频的确定性重建框架。这些方法通过将规范空间中的3D高斯基元经确定性形变场变换到各时间步，结合光度损失与平滑正则化进行端到端优化，在特定场景下取得了令人瞩目的渲染质量。

然而，现有方法共享一个根本性局限：**它们仅支持确定性重建，无法对运动预测的不确定性进行建模**。这一缺口的因果链条清晰可辨——当观测充分时，确定性形变场可以较好地拟合可见区域的运动；但当面临遮挡、稀疏视角或观测不足区域时，缺乏概率先验的模型既无法量化预测的可靠性，也无法利用学习到的运动结构进行合理推断，导致几何崩溃与渲染伪影。更关键的是，确定性框架天然不具备时间外推能力，无法对训练帧之外的运动做出任何有意义的预测。

### 概率运动先验的引入动机

上述困境的根源在于：确定性方法对形变场施加的是统一、固定的先验（如平滑性假设），而非从数据中自适应学习运动规律。这引出了一个自然的改进方向——**能否让模型从充分观测的基元中学习运动先验，并将这些先验以概率形式传播到观测不足的区域？**

高斯过程（Gaussian Process, GP）为此提供了理想的数学工具。GP定义在函数空间上的概率分布，其后验不仅给出预测均值，还天然提供预测方差作为不确定性的度量。将GP作为形变场的概率先验，意味着模型可以在观测充分的区域学习运动的相关结构（通过核函数编码空间平滑性与时间周期性），并在未观测区域中依据学到的相关结构进行带置信度的推断。

### GP-4DGS的核心主张

本文提出的**GP-4DGS**首次将高斯过程整合到4D Gaussian Splatting框架中，实现动态场景的概率性建模。与所有现有确定性方法相比，GP-4DGS引入了三项此前无法实现的关键能力：

1. **运动不确定性量化**：对每个高斯基元在每个时刻的运动预测提供方差估计，并通过alpha混合渲染为图像空间的不确定性图，使模型能够显式表达“对哪里不确定”。
2. **未观测区域的运动估计**：利用GP后验从充分观测基元中学习的时空相关结构，对稀疏采样或遮挡区域的运动进行带先验的推断，而非盲目外推。
3. **训练帧外的时间外推**：通过GP的查询机制，在训练时间范围之外预测未来运动，为动态场景的长期建模提供可能。

这一框架的核心洞察在于**数据自适应正则化**：GP后验的方差自动反映了观测置信度——充分观测区域的低方差意味着强约束，稀疏区域的高方差则允许更大的灵活性。这种“按需正则化”的机制，使GP-4DGS在DyCheck等基准上一致优于最强确定性基线SoM，尤其在稀疏观测的挑战性子集上优势更为显著（mPSNR提升+0.46 dB）。



## 核心方法与创新机理

### 问题瓶颈：确定性重建的失效边界

现有4DGS方法（如 **4DGS** (Wu et al., CVPR 2024)、**D-3DGS** (Yang et al., CVPR 2024)、**SC-GS**、**Gaussian Marbles** (Stearns et al., SIGGRAPH 2024)、**SoM** (Wang et al., ICCV 2025)）均为确定性框架：它们对形变场施加统一的显式或隐式先验（多项式、MLP、HexPlane等），并依赖光度与平滑损失进行端到端优化。这一范式存在两个根本性瓶颈：

1. **无法量化预测可靠性**：确定性方法输出的是点估计，无法区分“充分观测区域的可靠预测”与“遮挡/稀疏区域的不可靠猜测”，导致在观测不足区域的性能显著下降。
2. **先验与数据脱节**：固定的平滑先验无法自适应场景的局部观测密度——在强观测区域，先验可能过度约束导致欠拟合；在弱观测区域，先验可能不足以防止过拟合。

在DyCheck数据集的挑战性子集（视角重叠稀疏）上，最强确定性基线SoM的mPSNR仅为14.56 dB，而GP-4DGS达到15.02 dB（+0.46 dB），这一差距直接反映了确定性方法在稀疏观测场景下的失效。

### 核心洞察：概率运动先验的自适应正则化

GP-4DGS的核心创新在于将**高斯过程（GP）作为显式概率运动先验**整合到4DGS框架中，实现从“固定先验”到“数据自适应先验”的范式转换。其关键机制是：

- GP后验同时输出形变的**均值**（最佳预测）和**方差**（预测不确定性），方差自动编码了每个基元在每帧的观测置信度。
- 在GP-GS交替优化中，只有高置信度基元（累积α-blending权重超过阈值τ_C）参与GP训练，确保运动先验从可信观测中学习。
- GP引导的正则化损失 $\mathcal{L}_\mathrm{GP} = \frac1{NT}\sum_{k=1}^{N}\sum_{t=1}^{T} \delta_{(k,t)} \cdot \|\mathbf{y}_{(k,t)} - \bar{\pmb{\mu}}_{(k,t)}^*\|^2$ 惩罚GS变形与GP后验均值的偏离，但通过阈值δ选择性施加——在观测充分的区域，GP预测更可信，正则化更强；在观测稀疏区域，GP预测不确定性高，正则化自动减弱。

这种“自我强化循环”（GP从GS的置信基元学习运动先验，再用学到的先验正则化GS优化）是方法的核心因果旋钮。消融实验证实：去除GP-GS交替优化后，paperwindmill场景的mPSNR从19.88降至19.22，mSSIM从0.560降至0.541，mLPIPS从0.19升至0.17，甚至低于基线方法。

### 方法谱系与知识库定位

GP-4DGS在4DGS方法谱系中占据“概率性动态重建”这一空白位置：

| 维度 | 确定性4DGS（4DGS/D-3DGS/SC-GS） | 概率性4DGS（GP-4DGS） |
|------|-------------------------------|----------------------|
| **形变建模** | 确定性函数（多项式/MLP/HexPlane） | 高斯过程后验分布（均值 + 方差） |
| **先验类型** | 统一平滑先验 | 数据自适应运动先验 |
| **优化策略** | 端到端光度+平滑损失 | GP-GS交替优化（置信度采样 + GP引导正则化） |
| **不确定性** | 无 | 逐基元运动方差 + 可渲染不确定性图 |
| **时间外推** | 不支持 | GP查询未来时间戳 |

值得注意的定位差异：
- 与**Gaussian Marbles**和**SoM**相比，GP-4DGS不依赖手工设计的运动约束，而是从数据中学习运动先验。
- 与NeRF系列中的概率方法（如S-NeRF、CF-NeRF）不同，GP-4DGS将概率建模直接作用于显式高斯基元的形变空间，而非隐式辐射场的颜色/密度空间。

### 三项新增能力

GP-4DGS引入的三项确定性方法不具备的能力，直接源于GP概率框架：

1. **运动不确定性量化**：通过MC采样计算每基元形变位置的方差 $U_{k,t} = \mathrm{Var}(\{p_{k,t}^{(s)}\}_{s=1}^{S})$，并通过α-blending渲染为图像空间的不确定性图 $\hat{\mathbf{U}}(\mathbf{r}) = \sum_{k=1}^{N} U_{k,t} \omega_{k,t}^{\pi}(\mathbf{r})$。AUSE-MSE评估（Table 3）表明，GP-4DGS的不确定性估计与重建误差的匹配度在所有设置下均优于基线。

2. **未观测区域运动估计**：时空分解核 $k_i(\mathbf{x},\mathbf{x}') = k_i^\mathrm{spatial}(\mathbf{p},\mathbf{p}') + k_i^\mathrm{temporal}(\mathbf{x},\mathbf{x}')$ 使GP能够在空间维度（通过Matérn核的几何平滑性）和时间维度（通过周期核的循环结构）上传播运动约束，即使某区域从未被观测，也能从邻近基元和相邻帧推断合理运动。DAVIS数据集极端视角偏移下的定性结果（Figure 4）验证了这一能力。

3. **训练帧外时间外推**：通过查询训练好的GP在 $t_f > T_\text{train}$ 的预测，实现未来运动预测。Table 2显示，在周期性场景（如paperwindmill）上，GP-4DGS的外推PSNR显著优于线性外推基线；周期性核支持短期外推，周期性均值支持长期外推。

### 技术突破：变分GP的可扩展性

将GP应用于4DGS面临的核心计算挑战是：精确GP后验的时间复杂度为 $\mathcal{O}(N^3)$，其中N为高斯基元数量（通常数千至数万）。GP-4DGS通过引入M个诱导点（$M \ll N$）和变分推断，将复杂度降至 $\mathcal{O}(NM^2 + M^3)$。变分后验均值的查询复杂度仅为 $\mathcal{O}(M)$：$\bar{\mu}_i^* = \mathbf{k}_*^{(i)\top}(\mathbf{K}_{ZZ}^{(i)})^{-1}\mathbf{m}_i$。这一可扩展设计使得GP训练能够以每2000次GS迭代一次的频率进行，在计算可行性与先验质量之间取得平衡。

诱导点的初始化策略同样关键：基于Chronos时序特征的初始化相比随机初始化或速度KNN获得更高的ELBO（Table 4），表明时序感知的诱导点分布有助于GP更有效地捕捉运动模式。



GP-4DGS 的核心思路是将**高斯过程（Gaussian Process, GP）**作为显式的概率运动先验，嵌入到 4D 高斯泼溅（4D Gaussian Splatting, 4DGS）框架中，从而将确定性动态重建升级为概率性建模。整个 pipeline 由四个关键模块构成，形成从场景表示、运动建模、联合优化到不确定性输出的闭环。

**输入与基础表示。** 系统接收单目视频序列作为输入，以一组规范空间（canonical space）下的 3D 高斯基元 $\{\mathcal{G}_k\}_{k=1}^N$ 作为场景表示。每个基元通过形变函数 $f(\mathbf{x})$ 被变换到目标时刻 $t$ 的位置和朝向，其中 $\mathbf{x} = (\mathbf{p}, t)$ 为时空坐标，$\mathbf{p}$ 为规范空间位置。形变后的基元经可微光栅化渲染为图像，并与观测帧进行光度比较。

**概率运动先验。** 区别于现有方法使用的确定性多项式、MLP 或 HexPlane 形变，GP-4DGS 将每个形变输出通道 $f_i(\mathbf{x})$ 建模为独立的高斯过程：
$$f_i(\mathbf{x}) \sim \mathcal{GP}(m_i(\mathbf{x}), k_i(\mathbf{x}, \mathbf{x}'))$$
其中核函数采用**时空分解核**（composite kernel）：
$$k_i(\mathbf{x},\mathbf{x}') = k_i^{\mathrm{spatial}}(\mathbf{p},\mathbf{p}') + k_i^{\mathrm{temporal}}(\mathbf{x},\mathbf{x}')$$
空间部分使用 Matérn 核捕捉几何平滑性，时间部分使用周期核建模运动的循环结构。这一设计使模型能够从充分观测的基元中**自动学习数据自适应的运动先验**，而非施加统一的固定约束。

**可扩展变分推断。** 为应对精确 GP 推理 $\mathcal{O}(N^3)$ 的计算瓶颈，GP-4DGS 引入 $M$ 个诱导点（inducing points, $M \ll N$）进行变分近似，将复杂度降至 $\mathcal{O}(NM^2 + M^3)$。通过最大化证据下界（ELBO）训练变分后验，模型可高效输出每个基元在任意时空位置的形变后验均值 $\bar{\mu}_i^*$ 和方差。

**GP-GS 协同优化。** 这是整个框架的“发动机”。优化过程在 GP 训练与 GS 优化之间交替进行：
1. **置信度加权 GP 训练**：仅选取累积 alpha 混合权重 $C_k > \tau_C$ 的高置信度基元作为训练数据，确保 GP 从可靠观测中学习运动先验。
2. **GP 引导的 GS 正则化**：将 GP 预测缓存在查找表中，通过 GP 引导损失 $\mathcal{L}_{\mathrm{GP}}$ 惩罚 GS 形变对后验均值的偏离，且仅在预测方差低于阈值时施加约束。该损失与光度损失 $\mathcal{L}_{\mathrm{rgb}}$、SSIM 损失 $\mathcal{L}_{\mathrm{ssim}}$ 和局部刚性损失 $\mathcal{L}_{\mathrm{rigid}}$ 联合优化 GS 参数。

这种交替机制形成了**自我强化循环**：更准确的 GS 形变为 GP 提供更干净的训练信号，而更精确的 GP 先验又反过来正则化 GS 优化，两者相互促进直至收敛。

**输出与可解释性。** 训练完成后，GP-4DGS 不仅输出高质量的动态新视图合成结果，还提供三项确定性方法不具备的能力：
- **运动不确定性量化**：通过 Monte Carlo 采样计算每个基元的形变位置方差 $U_{k,t}$，并经 alpha 混合渲染为图像空间的运动不确定性图 $\hat{\mathbf{U}}(\mathbf{r})$。
- **未观测区域运动估计**：GP 后验可在缺乏直接观测的时空区域进行外推，传播运动约束。
- **时间外推**：将 GP 查询点的时间坐标延伸至训练帧范围之外，自然实现未来运动预测。

整体而言，GP-4DGS 的 pipeline 将 4DGS 从“静态先验 + 确定性拟合”范式转变为“数据驱动概率先验 + 置信度感知优化”范式，为动态场景重建赋予了内在的不确定性感知能力和外推泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/001_Figure_1.jpg]]
*Figure 1: We propose GP-4DGS, a novel integration of Gaussian Processes (GPs) [37] into 4D Gaussian Splatting (4DGS). Unlike existing deterministic approaches, this formulation enables robust uncertainty quantification, future motion prediction, and prior estimation for unobserved regions*



GP‑4DGS 的核心架构建立在 3D Gaussian Splatting (3DGS) 的显式表示之上，通过引入概率性运动先验，将确定性形变建模升级为可量化不确定性的概率框架。整个方法围绕四个关键模块展开：

### 3D 高斯基元与形变表示

场景由一组规范空间中的 3D 高斯基元表示，每个基元 $k$ 由位置 $\pmb{p}_k$、协方差矩阵 $\pmb{\Sigma}_k$（分解为旋转 $\mathbf{R}_k$ 和缩放 $\mathbf{S}_k$）、颜色和不透明度参数定义。基元的非归一化核函数为：

$$\mathcal{G}_k(\mathbf{x}_s;\pmb{p}_k,\pmb{\Sigma}_k) = \exp\left(-\frac12(\mathbf{x}_s-\pmb{p}_k)^\top\pmb{\Sigma}_k^{-1}(\mathbf{x}_s-\pmb{p}_k)\right)$$

其中协方差分解为 $\Sigma_k = \mathbf{R}_k \mathbf{S}_k \mathbf{S}_k^\top \mathbf{R}_k^\top$。在动态场景中，基元通过形变操作从规范空间变换到目标时刻 $t$，形变后的位置和旋转用于后续的 alpha 混合渲染。

### 时空高斯过程核

GP‑4DGS 的核心创新在于将每个形变输出通道 $f_i(\mathbf{x})$ 建模为独立的高斯过程：

$$f_i(\mathbf{x}) \sim \mathcal{GP}(m_i(\mathbf{x}), k_i(\mathbf{x}, \mathbf{x}'))$$

为捕捉形变场的多尺度相关结构，方法采用时空分解的复合核，将空间平滑性与运动周期性显式分离：

$$k_i(\mathbf{x},\mathbf{x}') = k_i^\mathrm{spatial}(\mathbf{p},\mathbf{p}') + k_i^\mathrm{temporal}(\mathbf{x},\mathbf{x}')$$

其中空间分量采用 Matérn 核以建模几何平滑性，时间分量采用周期核以捕捉重复运动模式。这种分解设计使得模型能够从充分观测区域学习运动规律，并将其传播到稀疏观测区域——当查询点超出观测范围时，分解核确保预测不会坍缩到无信息的先验均值。

### 变分推断与诱导点

精确 GP 推理的复杂度为 $\mathcal{O}(N^3)$（$N$ 为基元数量），对于包含数万基元的 4DGS 场景不可行。GP‑4DGS 通过变分推断和诱导点机制将复杂度降至 $\mathcal{O}(NM^2 + M^3)$（$M \ll N$ 为诱导点数量）。变分后验的形变均值查询仅需 $\mathcal{O}(M)$ 复杂度：

$$\bar{\mu}_i^* = \mathbf{k}_*^{(i)\top}(\mathbf{K}_{ZZ}^{(i)})^{-1}\mathbf{m}_i$$

训练通过最大化证据下界（ELBO）进行：

$$\mathbb{E}_{q(\mathbf{u}_i)}[\log p(\mathbf{y}_i|\mathbf{u}_i)] - \mathrm{KL}[q(\mathbf{u}_i)\|p(\mathbf{u}_i)]$$

诱导点的初始化对收敛质量至关重要。GP‑4DGS 采用基于 Chronos 时序特征的选择策略，相比随机初始化和速度 KNN 方法获得更高的 ELBO 值（见 Table 4），确保诱导点在规范空间和时间轴上的良好分布（见 Figure 8）。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/008_Figure_8.jpg]]
*Figure 8: Visualization of inducing points (paper-windmill). Inducing points (red) are well-distributed across the canonical space and temporal axis to ensure comprehensive coverage of the scene*

### GP‑GS 协同优化

GP‑4DGS 的关键工程贡献是 GP‑GS 交替优化策略（Algorithm 1），形成自我强化的训练循环：

**置信度加权的 GP 训练**：仅选择累积 alpha 混合权重 $C_k > \tau_C$ 的高置信度基元构建训练子集 $\mathcal{D}_C$。这些基元在训练视角中充分可见，其形变观测更为可靠，从而确保 GP 从干净信号中学习运动先验。

**GP 引导的 GS 正则化**：训练后的 GP 为所有基元提供形变后验预测，通过 GP 引导损失惩罚 GS 优化中偏离 GP 预测的形变：

$$\mathcal{L}_\mathrm{GP} = \frac1{NT}\sum_{k=1}^{N}\sum_{t=1}^{T} \delta_{(k,t)} \cdot \|\mathbf{y}_{(k,t)} - \bar{\pmb{\mu}}_{(k,t)}^*\|^2$$

其中 $\delta_{(k,t)}$ 为选择性激活阈值，仅在 GP 预测方差较低时施加约束。这种机制实现了数据自适应的正则化强度——在充分观测区域 GP 方差低、约束强；在稀疏区域方差高、约束自动放松，避免错误先验干扰。

消融实验（Table B）证实：去除 GP‑GS 交替优化后，重建质量（mPSNR 19.22）显著低于完整方法（mPSNR 19.88），验证了联合训练对学习准确运动先验的必要性。

### 不确定性量化与外推

GP‑4DGS 通过蒙特卡洛采样实现运动不确定性量化。对每个基元 $k$ 在时刻 $t$ 进行 $S$ 次 GP 后验采样，计算形变位置的方差：

$$U_{k,t} = \mathrm{Var}(\{p_{k,t}^{(s)}\}_{s=1}^{S})$$

将基元级不确定性通过 alpha 混合投影到图像空间，生成运动不确定性图：

$$\hat{\mathbf{U}}(\mathbf{r}) = \sum_{k=1}^{N} U_{k,t} \omega_{k,t}^{\pi}(\mathbf{r})$$

时间外推则通过直接查询训练好的 GP 在 $t_f > T$ 时刻的预测实现，无需额外训练。周期性核支持短期外推，周期性均值支持长期外推，但后者在非周期性运动场景中会引入虚假振荡（详见 Figure A 和 Table A 的消融分析）。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/012_Figure_6.jpg]]
*Figure 6: Trajectory comparison on the (left) paper-windmill and (right) block scene. GP guidance effectively regularizes motion trajectories, reducing noise and producing physically plausible motion patterns, compared to the baseline approach*



## 实验与关键发现

### 核心定量结果：DyCheck 数据集

GP‑4DGS 在 DyCheck 数据集上进行了全面的新视图合成评估，与多个确定性基线方法进行对比，包括 **Gaussian Marbles**（Stearns et al., SIGGRAPH 2024）、**SoM**（Wang et al., ICCV 2025）、**SC‑GS**、**D‑3DGS**（Yang et al., CVPR 2024）以及 **4DGS**（Wu et al., CVPR 2024）。评估遵循标准协议，采用预定义掩码版本的 mPSNR、mSSIM 和 mLPIPS 衡量共视区域的渲染质量，训练/测试划分严格遵循原始数据集设置。

如 Table 1 所示，GP‑4DGS 在所有评估子集上均取得最优结果。在 SoM 方法所使用的 5 个场景子集上，GP‑4DGS 的 mPSNR 达到 16.92，mSSIM 为 0.66，mLPIPS 为 0.41，分别优于最强基线 SoM 的 16.73、0.64 和 0.43。在全部 7 个场景上，mPSNR 进一步提升至 17.38，验证了方法的整体有效性。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on the DyCheck dataset. We evaluate performance on all seven scenes (All), the five scenes used in SoM [46] (SoM 5), and a challenging subset with reduced viewpoint overlap. GP-4DGS consistently achieves superior results, particularly under sparse observations*

**稀疏观测下的优势尤为显著。** 在挑战性子集（Challenging subset）上——该子集采用与扩散方法相同的降采样策略以减少视角重叠——GP‑4DGS 的 mPSNR 达到 15.02，相比 SoM 的 14.56 领先 0.46 dB。这一结果表明，高斯过程运动先验在观测稀疏时能够有效传播运动约束，弥补确定性方法因缺乏先验而导致的性能退化。

定性比较（Figure 3）进一步印证了数值结果：GP‑4DGS 在观测较少的区域展现出更精确的几何重建，而基线方法在这些区域往往出现模糊或形变伪影。在 DAVIS 数据集的极端视角偏移场景下（Figure 4），时空 GP 先验通过将运动约束忠实地传播到观测不足的区域，有效正则化了场景表示，基线方法则因缺乏此类先验而重建失败。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison of novel view synthesis on the DyCheck dataset. GP-4DGS shows more accurate geometry compared to baselines, particularly in regions with less observation*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison on the DAVIS dataset under extreme viewpoint shifts from training view. Unlike the baseline, our spatiotemporal GP prior effectively regularizes the scene by faithfully propagating motion constraints into poorly observed regions*

### 不确定性量化评估

GP‑4DGS 的核心创新之一在于提供有原则的运动不确定性估计。Table 3 报告了基于 AUSE‑MSE（↓）的不确定性量化结果，该指标衡量重建误差与预测不确定性之间稀疏化曲线的面积差距。GP‑4DGS 在所有设置下均取得最低的 AUSE，表明其不确定性估计与真实重建误差的匹配度最高。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/009_Table_3.jpg]]
*Table 3: Uncertainty quantification results in terms of AUSE-MSE (↓), measured as the area gap between the reconstruction error- and predicted uncertainty-based sparsification curves. Top 20 and 40 denote the frames with the lowest MSEs. GP-4DGS achieves the lowest AUSE across all settings*

Figure 2 展示了渲染图像与对应的运动不确定性图。不确定性图通过将每个基元的运动方差 $U_{k,t}$ 经 alpha 混合投影到图像空间得到：

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/002_Figure_2.jpg]]
*Figure 2: Uncertainty quantification. GP-4DGS provides principled uncertainty estimates for motion, a capability inherently lacking in existing 4DGS methods*

$$\hat{\mathbf{U}}(\mathbf{r}) = \sum_{k=1}^{N} U_{k,t} \omega_{k,t}^{\pi}(\mathbf{r})$$

高不确定性区域与遮挡、快速运动或观测稀疏区域高度吻合，验证了 GP 后验方差作为可靠性指示器的有效性。这一能力是现有确定性 4DGS 方法所不具备的。

### 未来运动外推

Table 2 报告了未来运动外推性能。实验将最后 5 帧和 15 帧排除在训练之外，评估方法对未见时间帧的预测能力。GP‑4DGS 显著优于朴素的线性外推基线，尤其在周期性运动场景（如 paperwindmill）中优势明显——时间周期核有效捕捉了循环运动结构，使外推轨迹保持物理合理性。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/007_Table_2.jpg]]
*Table 2: Future motion extrapolation performance in terms of PSNR (↑). We evaluate performance on the last 5 and 15 frames excluded for training. GP-4DGS outperforms na¨ıve linear extrapolation, especially in periodic scenes where the temporal kernel effectively captures cyclic structures*

消融实验（附录 Table A 和 Figure A）揭示了周期性成分的差异化作用：
- **周期性核**（periodic kernel）支持短期外推，使 GP 能够在训练时间范围附近进行平滑预测；
- **周期性均值**（periodic mean）支持长期外推，使预测能够延续到远离训练帧的未来时刻，但在非周期性运动场景中会引入虚假的局部振荡。

因此，通用场景下仅使用周期性核更为安全，但外推能力受限；周期性均值则适用于已知运动具有强周期性的特定场景。

### 关键消融实验

**GP‑GS 交替优化的必要性。** 附录 Table B 在 paperwindmill 场景上对比了有无 GP‑GS 交替优化的重建质量。完整方法（w/ GP‑GS optimization）的 mPSNR 为 19.88，mSSIM 为 0.560，mLPIPS 为 0.19；而去除交替优化后（w/o），三项指标分别降至 19.22、0.541 和 0.17。这一显著差距表明，置信度加权的 GP 训练与 GP 引导的 GS 正则化之间的自我强化循环对学习准确的运动先验至关重要。单独优化 GS 或 GP 均无法实现充分收敛。

**时空分解核的关键作用。** 消融实验证实，空间 Matérn 核与时间周期核的相加分解（$k_i(\mathbf{x},\mathbf{x}') = k_i^\mathrm{spatial}(\mathbf{p},\mathbf{p}') + k_i^\mathrm{temporal}(\mathbf{x},\mathbf{x}')$）对外推能力是不可或缺的。缺少分解时，任何轴值超出观测范围后预测将坍缩到先验均值，丧失有意义的泛化能力。

**诱导点初始化的影响。** Table 4 对比了不同诱导点初始化方法对 ELBO 收敛的影响。基于 Chronos 时序特征的诱导点选择在 ELBO 上优于随机初始化和基于速度的 KNN 初始化，验证了利用时序特征提取进行诱导点布局的有效性。

### 失败模式与局限性

尽管 GP‑4DGS 在多项任务上表现优异，但存在以下已知局限：

1. **周期性假设的通用性限制。** 周期性均值虽然带来长期外推能力，但在非周期性运动场景中会引入虚假的局部振荡。通用部署时仅使用周期性核更为安全，但外推能力相应受限。

2. **运动先验质量依赖观测充分性。** 运动先验的学习依赖于从高置信度基元中提取信号——置信度通过累积 alpha 混合权重 $C_k > \tau_C$ 筛选。在极端稀疏观测或严重遮挡的场景下，可用的强观测基元数量可能不足，导致 GP 先验质量下降。

3. **计算开销。** 变分 GP 的推理虽然通过诱导点将复杂度从 $\mathcal{O}(N^3)$ 降至 $\mathcal{O}(NM^2+M^3)$，但 GP 训练每 2000 次迭代更新一次，仍带来额外的计算开销。这在大规模场景或长序列中可能成为瓶颈。

4. **输入模态限制。** 方法目前仅针对单目视频重建设计，未探索多视图或多传感器输入场景下的扩展性。

### 补充图表


![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/015_Table.jpg]]
*Table: B. Ablation study on GP-GS optimization for the paperwindmill scene. Our GP-GS optimization enables proper convergence and produces accurate priors that improve reconstruction*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2604_02915/figures/011_Table_4.jpg]]
*Table 4: Comparison of inducing point initialization methods in terms of ELBO (↑). Our time-series-based selection achieves superior convergence with higher ELBO than baselines*



## 定位与知识库关联

### 确定性4DGS的演进与局限

动态场景的新视图合成经历了从神经辐射场（NeRF）到基于高斯泼溅（3DGS）的范式转变。在4DGS框架下，形变建模是核心设计维度，现有方法可沿此轴分为三个技术代际：

- **多项式形变**：**SC-GS** 等早期工作使用显式多项式参数化运动轨迹，表达力有限，难以捕捉复杂非线性运动。
- **MLP形变**：**D-3DGS** (Yang et al., CVPR 2024) 采用多层感知机隐式编码形变场，提升了表达能力，但缺乏对运动平滑性或周期性的结构化归纳偏置。
- **HexPlane形变**：**4DGS** (Wu et al., CVPR 2024) 将时空分解为六平面表示，实现了高效压缩，但本质上仍施加统一的确定性先验。

上述方法的共同瓶颈在于：它们均为**确定性重建**，无法为预测提供置信度评估，在遮挡、稀疏观测或视角偏移区域性能显著退化。**Gaussian Marbles** (Stearns et al., SIGGRAPH 2024) 和 **SoM** (Wang et al., ICCV 2025) 代表了当前确定性方法的最高水平，但同样缺乏不确定性感知机制。

### GP-4DGS的定位：概率性运动先验的首次引入

GP-4DGS的核心贡献是将**高斯过程（GP）作为显式概率运动先验整合到4DGS框架中**，这是该方向的首个概率性方法。其方法学定位可从两个维度理解：

1. **形变建模方式的根本转变**：从“施加固定约束”转向“从数据中学习自适应先验”。GP的后验分布同时提供形变的均值（最佳估计）和方差（不确定性），使模型能够自动根据观测置信度调整正则化强度——充分观测区域保持高保真度，稀疏区域则由GP先验进行合理外推。

2. **优化策略的协同设计**：GP-GS交替优化（Algorithm 1）形成自我强化循环——仅用高置信度基元训练GP以获得可靠的运动先验，再用GP预测引导GS的正则化。消融实验（Table B）表明，去除该联合优化后重建质量显著下降（paperwindmill场景mPSNR从19.88降至19.22），验证了协同训练对学习准确运动先验的关键作用。

### 适用边界与失效模式

GP-4DGS的能力边界受以下因素制约：

- **运动周期性假设**：时间核采用周期性结构，在周期性运动场景（如旋转的风车）中表现优异，支持长期外推。但对于非周期性运动，周期性均值会引入虚假的局部振荡。消融实验（Figure A）表明，仅使用周期性核（不加周期性均值）更为安全，但外推能力受限。这一设计选择揭示了当前方法在“长期外推”与“通用性”之间的内在权衡。

- **观测充分性依赖**：运动先验的质量依赖于从高置信度基元学习。在极端稀疏观测或严重遮挡场景下，满足置信度阈值（$C_k > \tau_C$）的基元数量可能不足，导致GP训练信号薄弱。DyCheck挑战性子集上的性能提升（mPSNR +0.46 vs. SoM）表明方法具备稀疏观测鲁棒性，但极端退化场景仍需人工验证。

- **计算开销**：变分GP推理通过诱导点将复杂度从 $\mathcal{O}(N^3)$ 降至 $\mathcal{O}(NM^2 + M^3)$，但GP训练每2000次迭代更新一次，仍带来额外计算负担。对于大规模场景或长序列，诱导点数量 $M$ 的选择需要在精度与效率间权衡。

- **输入模态限制**：方法目前仅针对单目视频重建设计，未探索多视图或多传感器（如深度、IMU）输入场景下的概率建模扩展。

### 开放问题与未来方向

1. **运动先验的跨场景泛化**：当前学习的GP先验是场景特定的。如何将运动先验迁移到未见过的物体或场景，甚至跨任务泛化（如从重建到跟踪），是一个开放挑战。

2. **通用时态核设计**：在非周期性运动广泛存在的真实世界长序列中，需要设计更灵活的时态核以兼顾长期外推与短期适应性。可能的路径包括组合核学习、深度核或神经过程。

3. **置信度驱动的主动感知**：GP-4DGS提供的不确定性信号可自然用于主动视图选择或机器人探索中的信息规划，将重建从被动观测推向主动信息获取。

4. **多模态诱导点初始化**：当前基于Chronos时序特征的诱导点初始化已证明优于随机和速度KNN（Table 4），将其扩展到多模态信号（如音频、文本描述）可能增强场景语义理解。



## 原文 PDF

![[paperPDFs/CVPR_2026/GP_4DGS_Probabilistic_4D_Gaussian_Splatting_from_Monocular_Video_via_Variational_Gaussian_Processes.pdf]]
