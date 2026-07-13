---
title: Score-Guided Diffusion for 3D Human Recovery
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery.pdf
project_link: null
code_link: https://github.com/statho/ScoreHMR
aliases:
- SSGHMR
- SGD3HR
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 使用扩散模型学习到的条件分布作为参数化先验，通过分数引导（score guidance）将观测信息注入去噪过程，从而实现数据驱动的迭代优化。
primary_logic: ScoreHMR 将优化拟合问题转化为扩散模型的逆问题求解，利用 DDIM 反演获得初始潜变量，然后通过引导确定性采样逐步对齐观测，避免传统优化的多局部极小问题，且无需针对不同任务重新训练扩散模型。
claims:
- ScoreHMR 利用扩散模型作为学习到的先验，并通过分数引导项进行迭代优化
- 该方法通过 DDIM 反演将回归估计映射到潜空间，然后进行引导 DDIM 采样
- 在单帧模型拟合任务中，ScoreHMR 显著优于 SMPLify 和 ProHMR-fitting 等优化基线
- 3DPW 上 PA-MPJPE (mm) = 51.1 (HMR2.0+ScoreHMR-b)
---

# Score-Guided Diffusion for 3D Human Recovery

> [!tip] 核心洞察
> ScoreHMR 将优化拟合问题转化为扩散模型的逆问题求解，利用 DDIM 反演获得初始潜变量，然后通过引导确定性采样逐步对齐观测，避免传统优化的多局部极小问题，且无需针对不同任务重新训练扩散模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于分数引导扩散的三维人体恢复 |
| 英文题名 | Score-Guided Diffusion for 3D Human Recovery |
| 会议/期刊 | CVPR 2024 |
| Links | [Code](https://github.com/statho/ScoreHMR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ScoreHMR (Score-Guided Human Mesh Recovery) |
| Dataset | 3DPW, EMDB 1, Human3.6M, Mannequin |

> [!tip] 效果简介
> - 3DPW 上，PA-MPJPE (mm) 51.1 (HMR2.0+ScoreHMR-b) vs 54.3 (HMR2.0) (-3.2)。
> - EMDB 1 上，PA-MPJPE (mm) 76.6 (HMR2.0+ScoreHMR-b) vs 78.7 (HMR2.0) (-2.1)。
> - Human3.6M 上，MPJPE (mm) 44.7 (HMR2.0+ScoreHMR-b) vs 52.8 (HMR2.0) (-8.1)。

## 概要

### 问题瓶颈

从单张图像恢复三维人体网格（3D Human Mesh Recovery）是计算机视觉的核心任务之一。现有方法主要分为两类：**回归方法**（如 **HMR 2.0**、**ProHMR**）直接从图像预测 SMPL 模型参数，速度快但常出现人体模型与图像观测之间的对齐偏差（Figure 1 中间）；**优化拟合方法**（如 **SMPLify**、**ProHMR-fitting**）通过最小化手工设计的能量函数来迭代对齐，但容易陷入局部最小值，且严重依赖大量人工先验项。这一“回归不准、优化不稳”的困境构成了领域的关键瓶颈。

### 核心方法：ScoreHMR

ScoreHMR 将人体模型拟合重新定义为**扩散模型的逆问题求解**。其核心洞察是：使用在通用人体姿态分布上训练的扩散模型作为**可学习的参数化先验**，通过**分数引导**将观测信息（如 2D 关键点）注入去噪过程，从而在潜空间中实现数据驱动的迭代优化。

具体流程为：首先用回归网络获得初始 SMPL 姿态估计，通过 **DDIM 反演**将其映射到扩散模型的潜变量空间；然后在确定性 DDIM 采样过程中，利用**观测损失梯度**修改噪声预测，逐步将潜变量引导至与图像观测对齐的姿态。整个过程在“反演—引导采样”的外层循环中迭代，直至收敛。

### 方法定位

在方法谱系中，ScoreHMR 处于**回归方法**与**优化方法**的交叉地带：它继承了回归方法的初始化能力和扩散模型的数据驱动先验，同时保留了优化方法对观测证据的精细对齐能力。不同于传统优化方法依赖手工设计的 GMM 姿态先验和 L-BFGS 优化器，ScoreHMR 的“先验”隐含在扩散模型的条件分布中，“迭代”通过 DDIM 采样的确定性动力学完成，从而避免了多局部极小问题，且无需针对不同任务（单帧拟合、多视图优化、时序平滑）重新训练扩散模型。

### 主要结果

在多个标准基准上，ScoreHMR 一致且显著地超越了各类优化基线：

| 任务 | 基准 | 指标 | 回归基线 | ScoreHMR | 提升 |
|------|------|------|----------|----------|------|
| 单帧模型拟合 | 3DPW | PA-MPJPE (mm) | 54.3 (HMR 2.0) | **51.1** | -3.2 |
| 单帧模型拟合 | Human3.6M | MPJPE (mm) | 52.8 (HMR 2.0) | **44.7** | -8.1 |
| 多视图优化 | Mannequin | MPJPE (mm) | 156.0 (HMR 2.0) | **148.3** | -7.7 |
| 时序运动细化 | 3DPW | Acc Err (mm/s²) | 14.1 (ProHMR-fitting) | **11.1** | -21.3% |

消融实验表明，较小的噪声水平（τ=50）和较大的 DDIM 步长（Δt=10）能获得最佳精度，但论文指出小步长对挑战性姿态更为鲁棒。值得注意的局限性包括：当 2D 关键点检测存在严重错误时，引导过程可能失效；方法依赖上游回归网络和关键点检测器的质量；包含 SMPL 形状参数（β）未带来显著的性能增益。



### 问题背景：三维人体重建中的图像-模型对齐困境

从单目图像或视频中恢复三维人体姿态与形状是计算机视觉领域的核心问题之一，其应用涵盖动作捕捉、人机交互、虚拟现实等场景。当前主流方法可归为两类：**回归方法**与**优化拟合方法**。

回归方法（如 **HMR 2.0**、**ProHMR**）通过端到端神经网络直接从图像预测 SMPL 模型参数，推理速度快，但存在一个根本性缺陷——**图像与人体模型之间的对齐误差**。如 Figure 1 所示，即便是最先进的单目回归方法，其重建结果在投影回图像平面时，关节位置与图像中的人体轮廓常出现明显偏差。这种不对齐源于回归网络对全局图像特征的压缩编码过程中丢失了精细的空间对应信息。

### 现有方法的瓶颈

**优化拟合方法**（如 **SMPLify**、**ProHMR-fitting**）试图弥补回归方法的不足：它们以回归结果为初始化，通过最小化二维关键点重投影误差等数据项与手工设计的先验项（如 GMM 姿态先验、正则化项）的加权和来迭代优化 SMPL 参数。然而，这类方法面临两个关键瓶颈：

1. **局部极小值陷阱**：优化目标函数高度非凸，传统梯度下降（如 L-BFGS）极易陷入局部极小值，导致优化结果对初始化敏感，且无法保证收敛到全局最优。
2. **手工先验的局限性**：姿态先验项（如高斯混合模型）需要大量手工设计与调参，难以准确捕捉真实人体姿态分布的复杂多模态特性。不同任务（如单帧拟合、多视图融合、时序平滑）往往需要重新设计先验项和损失权重，泛化能力受限。

### 核心动机：将优化拟合重构为扩散模型的逆问题求解

本文的核心洞察在于：**扩散模型学习到的条件分布可以作为参数化先验，而分数引导（score guidance）机制可以将观测信息注入去噪过程，从而实现数据驱动的迭代优化**。

具体而言，ScoreHMR 将传统优化拟合问题转化为扩散模型的**逆问题求解**：给定一个由回归网络产生的初始 SMPL 参数估计 $\mathbf{x}_{\text{reg}}$ 和额外的观测 $\mathbf{y}$（如二维关键点检测），目标是恢复与观测一致的 SMPL 参数 $\mathbf{x}_0$。这一过程被建模为：

$$ \mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \boldsymbol{\eta} $$

其中 $\mathcal{A}$ 为前向观测算子（如三维关键点到二维平面的投影），$\boldsymbol{\eta}$ 为观测噪声。

与传统优化方法直接对参数空间进行梯度下降不同，ScoreHMR 利用 DDIM 反演将初始回归估计映射到扩散模型的潜空间，然后通过**引导确定性采样**（guided deterministic sampling）逐步将观测信息注入去噪过程。这一范式的关键优势在于：

- **避免局部极小值**：扩散模型的去噪轨迹由学习到的分数函数引导，天然倾向于生成符合数据分布的样本，不易陷入优化曲面的局部极小值。
- **任务无关的先验学习**：扩散模型仅在通用任务上训练一次——学习以输入图像为条件的 SMPL 参数分布 $p(\boldsymbol{\theta} | I)$——随后可通过设计不同的引导损失函数（重投影损失、多视图一致性损失、时间一致性损失）适配多种下游任务，无需重新训练模型。
- **数据驱动的先验表达**：扩散模型通过大规模数据学习到的条件分布，比手工设计的 GMM 先验更准确地刻画了姿态空间的复杂结构。

### 方法定位

ScoreHMR 处于回归方法与优化方法的交叉地带：它以回归结果为起点，通过扩散模型驱动的迭代优化实现精细对齐。与 **LGD**（基于学习梯度下降的优化）和 **LFMM** 等优化基线相比，ScoreHMR 的核心区别在于优化过程发生在扩散模型的潜空间中，由学习到的分数函数而非手工设计的能量项驱动。与 **ProHMR-fitting** 相比，ScoreHMR 的先验是通过去噪过程隐式施加的，而非显式的概率密度正则化项。

简而言之，ScoreHMR 的目标不是替代回归网络，而是为任何现成的回归方法提供一个**通用、任务无关的后处理精炼框架**，通过扩散模型的分数引导实现鲁棒的图像-模型对齐。



## 核心方法与创新机理

### 问题瓶颈：从回归误差与优化困境到扩散先验

现有基于回归的 3D 人体重建方法（如 **HMR 2.0** 和 **ProHMR**）虽能取得显著的重建效果，但在图像与人体模型对齐方面仍存在误差——模型关节投影与图像观测之间常出现偏移。传统优化方法（如 **SMPLify**）试图通过最小化数据项与先验项的加权和来修正这一问题，但手工设计的能量项（如 GMM 姿态先验）容易使优化陷入局部最小值，且依赖大量手工调参。**ScoreHMR** 的核心洞察在于：将这一优化拟合问题重新定义为扩散模型的**逆问题求解**，利用扩散模型学习到的条件分布作为参数化先验，从而避免传统优化的多局部极小问题。

### 关键机制：分数引导的扩散逆问题求解

ScoreHMR 的核心创新体现在三个 **changed slots** 上，分别对应先验形式、对齐机制和迭代策略的根本性改变：

**1. 姿态先验：从手工能量项到扩散模型条件分布**

传统优化方法使用手工设计的能量项（如 GMM 姿态先验）或各类正则项作为先验。ScoreHMR 将其替换为基于扩散模型的条件概率分布 $p(\theta|I)$——一个在通用姿态估计任务上训练得到的、任务无关的学习型参数化先验。该扩散模型以图像 $I$ 为条件，学习 SMPL 姿态参数的分布，训练目标为标准扩散损失：

$$\mathcal{L}_{DM}(\phi) = \mathbb{E}_{(I,\mathbf{x}_0),t,\epsilon} ||\epsilon_{\phi}(\mathbf{x}_t, t, I) - \epsilon||^2$$

**2. 对齐机制：从梯度下降加权求和到分数引导**

传统优化通过梯度下降最小化数据项和先验项的加权和来实现对齐。ScoreHMR 则通过扩散模型的**分数引导**（score guidance）在潜空间中注入观测信息。具体而言，给定观测 $\mathbf{y}$（如 2D 关键点），将逆问题建模为 $\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \eta$，在观测噪声为高斯假设下，将对数似然梯度近似为观测残差的梯度：

$$\nabla_{\mathbf{x}_t} \log p(\mathbf{y} | I, \mathbf{x}_t) \simeq -\rho \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$$

该梯度被注入到噪声预测中，形成引导后的噪声预测：

$$\epsilon_{\phi}' = \epsilon_{\phi}(\mathbf{x}_t, t, I) + \rho \sqrt{1-\alpha_t} \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$$

随后通过确定性 DDIM 采样完成去噪，无需针对不同任务重新训练扩散模型。

**3. 迭代策略：从传统优化器到 DDIM 反演-引导采样循环**

传统方法通常采用 L-BFGS 等优化器迭代更新参数。ScoreHMR 则采用**外层 DDIM 反演-引导采样循环**：首先通过 DDIM 反演将回归网络的初始估计 $\mathbf{x}_{reg}$ 映射到噪声水平 $\tau$ 的潜变量 $\mathbf{x}_\tau$：

$$\mathbf{x}_{t+1} = \sqrt{\alpha_{t+1}} \hat{\mathbf{x}}_0(\mathbf{x}_t) + \sqrt{1-\alpha_{t+1}} \epsilon_{\phi}(\mathbf{x}_t, t, I)$$

然后执行引导 DDIM 采样（从 $t=\tau$ 到 $0$），循环迭代直至引导损失相对变化低于阈值。这一机制使得优化过程在扩散模型的平滑潜空间中进行，有效避免了传统优化的局部极小问题。

### 与 baseline 的本质差异

| 维度 | 传统优化方法（SMPLify 等） | ScoreHMR |
|------|---------------------------|----------|
| 先验来源 | 手工设计（GMM、正则项） | 数据驱动的扩散模型条件分布 |
| 优化空间 | 原始参数空间 | 扩散模型潜空间 |
| 信息注入方式 | 损失函数加权求和 | 分数引导修改去噪方向 |
| 任务适应性 | 需针对任务调整先验权重 | 扩散模型任务无关，仅更换引导损失 |

### 证据强度

决定性证据来自 Table 2 的模型拟合实验：以 HMR 2.0 回归结果为初始化，ScoreHMR-b 在 3DPW 上取得 PA-MPJPE 51.1 mm，而 HMR 2.0 + SMPLify 为 60.1 mm，提升达 9.0 mm（约 15%）。这一显著差距直接验证了扩散先验 + 分数引导机制相对于传统手工先验 + 梯度下降优化的优势。消融实验（Table 1）进一步确认，单独的 DDIM 反演-采样循环（无引导）性能有限，而加入分数引导后性能大幅提升，证实引导项是因果旋钮的核心。



ScoreHMR 将 3D 人体恢复问题转化为**扩散模型的逆问题求解**。其核心流程是一个交替执行 DDIM 反演与引导 DDIM 采样的外层精炼循环（Algorithm 1），直到人体模型与观测信息充分对齐为止。

### 输入与输出

- **输入**：单张 RGB 图像 $I$，以及可选的附加观测 $\mathbf{y}$（如 2D 关键点检测结果、多视图图像或视频序列）。
- **初始化**：由现成的回归网络（如 ProHMR 或 HMR 2.0）提供初始 SMPL 姿态参数估计 $\mathbf{x}_{reg}$。
- **输出**：经过迭代精炼的 SMPL 姿态参数，使得重投影后的 3D 人体模型与图像观测高度一致。

### 核心模块与数据流

整个框架由四个关键模块串联而成，形成闭环迭代：

#### 1. DDIM 反演模块

该模块将回归网络输出的初始姿态估计 $\mathbf{x}_{reg}$ 映射到扩散模型的潜空间。具体而言，通过确定性 DDIM 反演过程，将 $\mathbf{x}_{reg}$ 反演至噪声水平 $\tau$ 对应的潜变量 $\mathbf{x}_\tau$：

$$\mathbf{x}_{t+1} = \sqrt{\alpha_{t+1}} \hat{\mathbf{x}}_0(\mathbf{x}_t) + \sqrt{1-\alpha_{t+1}} \epsilon_{\phi}(\mathbf{x}_t, t, I)$$

这一步的**关键作用**在于：它不改变扩散模型本身，而是将回归估计“编码”为扩散模型可操作的潜空间起点，为后续的引导采样提供初始状态。

#### 2. 分数引导去噪模块

从潜变量 $\mathbf{x}_\tau$ 出发，执行确定性 DDIM 采样，但采样过程中的噪声预测被**观测梯度项修正**。核心操作是将条件对数似然的分数近似为观测残差的梯度：

$$\nabla_{\mathbf{x}_t} \log p(\mathbf{y} | I, \mathbf{x}_t) \simeq -\rho \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$$

修正后的噪声预测为：

$$\epsilon_{\phi}' = \epsilon_{\phi}(\mathbf{x}_t, t, I) + \rho \sqrt{1-\alpha_t} \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$$

随后执行确定性 DDIM 采样步：

$$\hat{\mathbf{x}}_0'(\mathbf{x}_t) = \frac{1}{\sqrt{\alpha_t}} (\mathbf{x}_t - \sqrt{1-\alpha_t} \epsilon_{\phi}'(\mathbf{x}_t, t, I)), \quad \mathbf{x}_{t-1} = \sqrt{\alpha_{t-1}} \hat{\mathbf{x}}_0'(\mathbf{x}_t) + \sqrt{1-\alpha_{t-1}} \epsilon_{\phi}'(\mathbf{x}_t, t, I)$$

该模块的**核心机制**是：扩散模型提供学习到的参数化人体姿态先验 $p(\theta|I)$，而引导项将观测信息注入去噪过程，使采样轨迹同时满足先验分布和观测约束。

#### 3. 引导损失计算模块

根据具体应用场景，计算不同的观测一致性损失。在单帧模型拟合中，使用 2D 重投影损失：

$$\mathcal{L}_{repr} = \mathbf{y}_{conf} ||\Pi_K(W \mathcal{M}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \beta) + \gamma) - \mathbf{y}_{kp}||_2^2$$

在多视图场景中，加入跨视图一致性损失 $\mathcal{L}_{MV}$；在时序场景中，加入时间平滑损失 $\mathcal{L}_{temp}$。这些损失的梯度通过 $\nabla_{\mathbf{x}_t} \mathcal{L}$ 的形式注入去噪过程。

#### 4. 外层精炼循环

上述“反演→引导采样”过程被置于一个外层循环中。每轮迭代的输出作为下一轮的输入，循环终止条件为引导损失的相对变化低于预设阈值，或达到最大迭代步数。这一设计的**因果逻辑**是：单次引导采样可能无法完全消除初始回归误差，通过多轮交替反演与采样，逐步将估计拉向观测一致且先验合理的最优解。

### 方法定位

ScoreHMR 在姿态先验和优化机制两个维度上与传统方法形成鲜明对比：

| 方法槽位 | 传统优化方法（如 SMPLify） | ScoreHMR |
|---------|--------------------------|----------|
| 姿态先验 | 手工设计的 GMM 姿态先验或正则项 | 扩散模型学习到的条件分布 $p(\theta \mid I)$ |
| 对齐机制 | L-BFGS 等优化器最小化加权能量函数 | 扩散模型潜空间中的分数引导 |
| 迭代策略 | 梯度下降直接更新 SMPL 参数 | DDIM 反演-引导采样交替循环 |

这种设计使得 ScoreHMR 既避免了传统优化方法容易陷入局部极小值的问题，又无需针对不同任务重新训练扩散模型——同一扩散模型可复用于模型拟合、多视图精炼和时序运动细化等多种应用。

### 补充图表

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/002_Figure_2.jpg]]
*Figure 2: Score-Guided Human Mesh Recovery and its applications. Top row: Overview of ScoreHMR, which iteratively refines an initial regression estimate in a DDIM inversion – DDIM guided sampling loop until the human body model aligns with the available observation. Bottom row: Applications. (a): Body model fitting to 2D keypoints. (b): Multi-view refinement of individual per-frame predictions with cross-view consistency guidance. (c): Recovering temporally consistent and smooth 3D human motion from a video sequence given initial per-frame estimates*



ScoreHMR 将人体姿态优化问题形式化为一个逆问题：从观测 $\mathbf{y}$ 中恢复 SMPL 姿态参数 $\mathbf{x}_0$，其中 $\mathbf{y} = \mathcal{A}(\mathbf{x}_0) + \eta$，$\mathcal{A}$ 为前向算子（如相机投影），$\eta$ 为观测噪声。该方法的核心创新在于将扩散模型的条件分布 $p(\mathbf{x}_0|I)$ 作为学习到的参数化先验，并通过分数引导将观测信息注入去噪过程。

### 模块一：DDIM 反演

给定回归网络输出的初始姿态估计 $\mathbf{x}_{reg}$，首先通过确定性 DDIM 反演将其映射到噪声水平 $\tau$ 处的潜变量 $\mathbf{x}_\tau$：

$$
\mathbf{x}_{t+1} = \sqrt{\alpha_{t+1}} \hat{\mathbf{x}}_0(\mathbf{x}_t) + \sqrt{1-\alpha_{t+1}} \epsilon_{\phi}(\mathbf{x}_t, t, I) \tag{7}
$$

其中 $\hat{\mathbf{x}}_0(\mathbf{x}_t)$ 是从噪声样本 $\mathbf{x}_t$ 预测的干净姿态，$\epsilon_{\phi}$ 为条件扩散模型的噪声预测网络，$I$ 为输入图像。该反演过程将回归估计转化为扩散模型潜空间中的一个起点，为后续引导采样提供初始化。

### 模块二：分数引导近似

在逆问题框架下，需要计算观测的对数似然梯度 $\nabla_{\mathbf{x}_t} \log p(\mathbf{y} | I, \mathbf{x}_t)$ 以将观测信息注入去噪过程。假设观测噪声 $\eta$ 服从高斯分布，该梯度可近似为：

$$
\nabla_{\mathbf{x}_t} \log p(\mathbf{y} | I, \mathbf{x}_t) \simeq -\rho \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2 \tag{8}
$$

其中 $\rho$ 为引导强度系数，控制观测信息对去噪过程的影响力度。该近似将不可直接计算的对数似然梯度转化为观测残差关于潜变量 $\mathbf{x}_t$ 的梯度，使得引导项可通过反向传播高效计算。

### 模块三：引导去噪采样

将分数引导项融入噪声预测，得到修改后的噪声估计：

$$
\epsilon_{\phi}' = \epsilon_{\phi}(\mathbf{x}_t, t, I) + \rho \sqrt{1-\alpha_t} \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2 \tag{10}
$$

随后执行确定性 DDIM 采样步：

$$
\hat{\mathbf{x}}_0'(\mathbf{x}_t) = \frac{1}{\sqrt{\alpha_t}} (\mathbf{x}_t - \sqrt{1-\alpha_t} \epsilon_{\phi}'(\mathbf{x}_t, t, I)), \quad \mathbf{x}_{t-1} = \sqrt{\alpha_{t-1}} \hat{\mathbf{x}}_0'(\mathbf{x}_t) + \sqrt{1-\alpha_{t-1}} \epsilon_{\phi}'(\mathbf{x}_t, t, I) \tag{9}
$$

该采样步从 $t=\tau$ 迭代至 $t=0$，每一步同时利用扩散先验和观测梯度，逐步将潜变量推向既符合图像条件分布又与观测对齐的姿态参数。

### 模块四：外层迭代优化

ScoreHMR 将 DDIM 反演与引导采样组织为一个外层循环（Algorithm 1）：每轮先通过反演将当前估计映射回潜空间，再执行引导采样更新姿态参数，直至引导损失 $\mathcal{L}_g = ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$ 的相对变化低于预设阈值或达到最大迭代轮次。

### 应用相关引导损失

根据不同任务，观测 $\mathbf{y}$ 和前向算子 $\mathcal{A}$ 的具体形式有所差异：

- **身体模型拟合**：采用 2D 关键点重投影损失，$\mathbf{y}_{kp}$ 为检测到的 2D 关键点，$\mathbf{y}_{conf}$ 为置信度权重：

$$
\mathcal{L}_{repr} = \mathbf{y}_{conf} ||\Pi_K(W \mathcal{M}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \beta) + \gamma) - \mathbf{y}_{kp}||_2^2 \tag{12}
$$

- **多视图一致性**：对 $N$ 个视角的姿态取均值 $\bar{\mathbf{x}}_{0,b}$，约束各视角身体姿态趋于一致：

$$
\mathcal{L}_{MV} = \sum_{n=1}^N ||\hat{\mathbf{x}}_{0,b}^{(n)}(\mathbf{x}_t^{(n)}) - \bar{\mathbf{x}}_{0,b}||_2^2 \tag{13}
$$

- **时间一致性**：鼓励相邻帧姿态平滑过渡：

$$
\mathcal{L}_{temp} = \sum_{n=2}^N ||\hat{\mathbf{x}}_0^{(n)}(\mathbf{x}_t) - \hat{\mathbf{x}}_0^{(n-1)}(\mathbf{x}_t)||_2^2 \tag{14}
$$

### 扩散模型训练

条件扩散模型 $\epsilon_{\phi}(\mathbf{x}_t, t, I)$ 采用标准去噪损失进行训练：

$$
\mathcal{L}_{DM}(\phi) = \mathbb{E}_{(I,\mathbf{x}_0),t,\epsilon} ||\epsilon_{\phi}(\mathbf{x}_t, t, I) - \epsilon||^2 \tag{11}
$$

该模型作为任务无关的姿态先验，训练完成后无需针对不同下游任务重新训练，仅需替换引导损失即可适配身体拟合、多视图优化、时序运动细化等场景。

### 补充图表

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/009_Figure_5.jpg]]
*Figure 5: Diffusion model architecture. Implementation of*



## 实验与关键发现

### 核心实验设计

ScoreHMR 的实验评估围绕三个递进的应用场景展开：**单帧身体模型拟合**（body model fitting）、**多视图姿态精化**（multi-view refinement）和**时序运动平滑**（temporal motion refinement）。所有实验遵循统一的公平性准则：模型拟合方法均使用相同的 2D 关键点检测器（OpenPose）进行初始化，评估指标采用领域标准的 PA-MPJPE 和 MPJPE（单位 mm），时序实验则使用相同的回归基线（ProHMR 和 HMR 2.0）作为初始估计。

扩散模型的训练损失为标准去噪目标：

$$ \mathcal{L}_{DM}(\phi) = \mathbb{E}_{(I,\mathbf{x}_0),t,\epsilon} ||\epsilon_{\phi}(\mathbf{x}_t, t, I) - \epsilon||^2 \tag{11} $$

该模型以图像条件 $I$ 和噪声水平 $t$ 为输入，预测所添加的噪声 $\epsilon$，从而隐式学习 SMPL 姿态参数的条件分布 $p(\theta|I)$。

### 单帧身体模型拟合

这是 ScoreHMR 最核心的测试场景：给定单张图像和 2D 关键点检测结果，通过迭代优化使 SMPL 模型的投影与观测对齐。引导损失为置信度加权的重投影损失：

$$ \mathcal{L}_{repr} = \mathbf{y}_{conf} ||\Pi_K(W \mathcal{M}(\hat{\mathbf{x}}_0(\mathbf{x}_t), \beta) + \gamma) - \mathbf{y}_{kp}||_2^2 \tag{12} $$

其中 $\Pi_K$ 为相机投影，$W$ 为全局旋转，$\mathcal{M}$ 为 SMPL 模型，$\beta$ 为形状参数，$\gamma$ 为平移，$\mathbf{y}_{kp}$ 和 $\mathbf{y}_{conf}$ 分别为检测到的 2D 关键点及其置信度。

**Table 2**（模型拟合对比结果表）汇总了 ScoreHMR 与多种优化基线的定量对比。核心发现如下：

- **HMR 2.0 + ScoreHMR-b** 在 3DPW 上取得 **51.1 mm** 的 PA-MPJPE，相比纯回归的 HMR 2.0（54.3 mm）降低 3.2 mm，相比 HMR 2.0 + SMPLify（60.1 mm）降低 9.0 mm。
- 在 EMDB 1 上，ScoreHMR-b 达到 **76.6 mm**，优于 HMR 2.0 的 78.7 mm 和 ProHMR-fitting 的 78.9 mm。
- 以 ProHMR 为回归基线的 ScoreHMR 同样表现优异：3DPW 上 PA-MPJPE 为 52.1 mm（ProHMR 回归为 54.3 mm），优于 ProHMR-fitting（53.7 mm）和 SMPLify（59.4 mm）。

值得注意的是，ScoreHMR 在两种不同的回归初始化（ProHMR 和 HMR 2.0）上均一致地优于所有优化基线，包括基于学习梯度下降的 **LGD** 和 **LFMM**。这表明扩散模型先验的引导机制具有跨回归器的泛化能力。

**Figure 4**（身体模型拟合定性比较）展示了 ScoreHMR（绿色）与 ProHMR-fitting（蓝色）、SMPLify（灰色）的可视化对比。在具有挑战性的姿态（如大幅度手臂运动、自遮挡）下，ScoreHMR 能更好地保持图像-模型对齐，而传统优化方法容易出现局部极小导致的错位。

### 多视图姿态精化

在多视图场景中，ScoreHMR 对每个视角独立执行 DDIM 反演和引导采样，同时引入跨视图一致性损失：

$$ \mathcal{L}_{MV} = \sum_{n=1}^N ||\hat{\mathbf{x}}_{0,b}^{(n)}(\mathbf{x}_t^{(n)}) - \bar{\mathbf{x}}_{0,b}||_2^2 \tag{13} $$

其中 $\hat{\mathbf{x}}_{0,b}^{(n)}$ 为第 $n$ 个视角的身体姿态预测，$\bar{\mathbf{x}}_{0,b}$ 为所有视角的均值。该损失鼓励不同视角下的 3D 姿态趋于一致，从而利用多视图互补信息修正单视图中的歧义。

**Table 3**（多视图优化结果表）报告了 Human3.6M 和 Mannequin 数据集上的结果：

- Human3.6M 上，HMR 2.0 + ScoreHMR-b 的 MPJPE 为 **44.7 mm**，相比单视图 HMR 2.0（52.8 mm）降低 8.1 mm（相对提升 15.3%）。
- Mannequin 上，MPJPE 从 156.0 mm 降至 **148.3 mm**（降低 7.7 mm）。

**Figure 8**（多视图优化示例）展示了一个典型案例：第一视角中右手被身体自遮挡，单视图回归产生错误的手部姿态；通过多视图一致性引导，ScoreHMR 成功利用其他视角的信息修正了该错误。

### 时序运动平滑

对于视频序列，ScoreHMR 在逐帧估计的基础上引入时间一致性损失：

$$ \mathcal{L}_{temp} = \sum_{n=2}^N ||\hat{\mathbf{x}}_0^{(n)}(\mathbf{x}_t) - \hat{\mathbf{x}}_0^{(n-1)}(\mathbf{x}_t)||_2^2 \tag{14} $$

该损失鼓励相邻帧的姿态平滑过渡，抑制逐帧独立估计产生的抖动。

**Table 4**（运动细化结果表）显示：

- 3DPW 上，HMR 2.0 + ScoreHMR-b 的加速度误差（Acc Err）为 **11.1 mm/s²**，相比 HMR 2.0 + ProHMR-fitting（14.1 mm/s²）降低 21.3%，表明时序一致性引导有效抑制了运动抖动。
- EMDB 1 上，PA-MPJPE 从 ProHMR-fitting 的 78.9 mm 降至 **72.9 mm**（降低 6.0 mm）。

### 消融实验

**Table 1**（消融实验表）系统分析了 ScoreHMR 各组件的贡献，所有结果以 PA-MPJPE（mm）报告：

- **噪声水平 $\tau$ 的影响**：$\tau=50$ 时取得最优 PA-MPJPE（51.1 mm），随着 $\tau$ 增加至 300，误差上升至 54.5 mm。这表明适中的噪声水平为引导优化提供了足够的探索空间，而过大的噪声会破坏初始回归估计中的有用信息。
- **DDIM 步长 $\Delta t$ 的影响**：在 $\Delta t \in [2, 12]$ 范围内，较大的步长进一步降低误差（$\Delta t=10$ 时 PA-MPJPE 降至 48.2 mm）。但论文指出，小步长对挑战性姿态更为鲁棒，因为大步长可能使采样路径偏离数据流形。
- **形状参数 $\beta$ 的影响**：在扩散模型中额外包含 SMPL 形状参数 $\beta$ 并未带来显著的性能增益（**Table 5**，SMPL β 参数消融实验表）。论文分析认为，单帧回归对形状估计而言已足够简单，扩散模型的表达能力主要体现在姿态分布建模上。

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/013_Table_5.jpg]]
*Table 5: ScoreHMR with and without the inclusion of SMPL shape parameters β. Numbers are PA-MPJPE in mm. Parenthesis denotes the number of body joints used to compute PA-MPJPE*

### 失败模式与局限性

**Figure 7**（失败案例展示）揭示了 ScoreHMR 的主要失效场景：当 2D 关键点检测存在严重错误时（如错误的脚部关键点定位），所有方法（包括 ScoreHMR、ProHMR-fitting、SMPLify）的性能均显著下降。尽管扩散模型的图像条件在一定程度上帮助保持 3D 姿态与图像证据的一致性，但引导过程本身依赖于观测质量，错误的观测信号会将优化引向错误方向。

从机制层面分析，ScoreHMR 的因果链路为：回归初始化 → DDIM 反演 → 引导 DDIM 采样 → 对齐观测。该链路的薄弱环节在于：
1. **上游依赖**：方法依赖于现成的回归网络和 2D 关键点检测器，最终性能受限于这些组件的质量。
2. **观测噪声假设**：引导项基于高斯观测噪声假设（Eq. 8），当关键点检测误差不满足该假设时（如系统性偏移），引导效果可能退化。
3. **迭代效率**：多轮 DDIM 反演和采样循环增加了计算开销，论文未明确报告推理时间，在实时应用中可能成为瓶颈。

### 关键图表结论速览

| 图表 | 核心结论 | 证据强度 |
|------|----------|----------|
| Table 2 | ScoreHMR 在单帧拟合上一致优于 SMPLify、ProHMR-fitting 等优化基线，3DPW 上 PA-MPJPE 降低 3.2–9.0 mm | 强（多数据集、多基线） |
| Table 3 | 多视图精化带来 8.1 mm（Human3.6M）和 7.7 mm（Mannequin）的 MPJPE 提升 | 强（标准多视图基准） |
| Table 4 | 时序一致性引导使加速度误差降低 21.3%，有效抑制运动抖动 | 中强（两个数据集） |
| Table 1/5 | $\tau=50$ 和适中步长最优；包含 $\beta$ 无显著增益 | 中（消融实验） |
| Figure 7 | 关键点检测错误是主要失败模式，扩散模型提供一定鲁棒性但无法完全补偿 | 中（定性分析） |

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/004_Table_2.jpg]]
*Table 2: Evaluation of different model fitting methods. The fitting algorithms are initialized by the corresponding regression results, except LGD [53] and LFMM [8]. All numbers are PA-MPJPE in mm. Parenthesis denotes the number of body joints used to compute PA-MPJPE*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/005_Table_3.jpg]]
*Table 3: Evaluation of multi-view refinement. We compare our proposed approach with the single-view 3D reconstruction and an optimization-based method [32]. Parenthesis denotes the number of body joints used to compute MPJPE and PA-MPJPE*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/006_Table_4.jpg]]
*Table 4: Evaluation of human motion refinement. We compare different model fitting algorithms and our proposed approach in a temporal setting. Parenthesis denotes the number of body joints used to compute PA-MPJPE and Acc Err*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/003_Table_1.jpg]]
*Table 1: Ablation study. ScoreHMR is initialized by the corresponding regression results. All numbers are PA-MPJPE in mm. Parenthesis denotes the number of body joints used to compute PA-MPJPE*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/015_Figure_7.jpg]]
*Figure 7: Failure cases of model fitting. Pink: ProHMR regression. White: HMR 2.0b regression. Green: Regression + ScoreHMR (ours). Blue: Regression + ProHMR-fitting. Grey: Regression + SMPLify. While all methods encounter challenges when incorrect keypoints are detected, our image-conditioned diffusion model tries to keep the 3D pose aligned with the available image evidence*

### 补充图表

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/008_Figure_4.jpg]]
*Figure 4: Body model fitting results. Pink: Regression (ProHMR [32]). White: Regression (HMR 2.0 [15]). Green: Regression + ScoreHMR (ours). Blue: Regression + ProHMR-fitting [32]. Grey: Regression + SMPLify [4]*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative evaluation of ScoreHMR Pink: Regression with ProHMR [32]. White: Regression with HMR 2.0 [15]. Green: Regression + ScoreHMR (ours)*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/001_Figure_1.jpg]]
*Figure 1: Although achieving remarkable 3D human reconstructions, a recent state-of-the-art monocular regression approach [15] may encounter challenges in aligning the human body model to the image (middle image). To address this, we propose an iterative refinement approach that utilizes image observations (e.g., 2D keypoint detections) and achieves better image-model alignment (right image)*

![[assets/figures/papers/paper_list_l16_ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery_motion20v2/figures/012_Figure_6.jpg]]
*Figure 6: Model fitting results. We compare our approach (green) with ProHMR-fitting (blue) and SMPLify (grey). All model fitting algorithms are initialized with regression from ProHMR (pink) or HMR 2.0b (white)*



## 定位与知识库关联

### 1. 方法定位与核心创新

ScoreHMR 本质上属于**参数化人体模型的优化拟合**范式，但其创新在于将传统优化问题转化为**扩散模型的逆问题求解**。与现有优化方法（如 SMPLify）依赖手工设计的能量项和梯度下降不同，ScoreHMR 使用扩散模型学习到的条件分布 $p(\theta|I)$ 作为参数化先验，并通过分数引导（score guidance）将观测信息注入去噪过程。

传统优化拟合方法存在两个核心瓶颈：
- **回归方法**（如 **HMR 2.0**、**ProHMR**）直接从图像预测 SMPL 参数，速度快但缺乏图像-模型对齐的显式约束，容易产生“漂浮”或穿透等伪影。
- **优化方法**（如 **SMPLify**、**ProHMR-fitting**）通过最小化重投影误差等数据项来改善对齐，但目标函数高度非凸，容易陷入局部最小值，且需要大量手工先验项（如 GMM 姿态先验、关节角度限制等）来约束解空间。

ScoreHMR 的核心洞察在于：扩散模型的去噪过程天然具有从粗糙到精细的逐步生成特性，配合 DDIM 反演和引导采样，可以在潜空间中实现数据驱动的迭代优化，避免传统优化的多局部极小问题。该方法的关键因果调控变量是**分数引导项**——它通过近似对数似然梯度 $\nabla_{\mathbf{x}_t} \log p(\mathbf{y}|I, \mathbf{x}_t) \simeq -\rho \nabla_{\mathbf{x}_t} ||\mathbf{y} - \mathcal{A}(\hat{\mathbf{x}}_0(\mathbf{x}_t))||_2^2$，将观测约束注入去噪过程，从而在保持扩散先验的同时实现与观测的对齐。

### 2. 与基线工作的关系

ScoreHMR 与以下工作构成直接比较或技术关联：

**2.1 回归基线**

- **HMR 2.0**：作为当前最强的单目回归方法之一，为 ScoreHMR 提供初始姿态估计。在 3DPW 上，HMR 2.0 的 PA-MPJPE 为 54.3 mm，经 ScoreHMR 优化后降至 51.1 mm（Table 2），表明扩散先验引导的优化能有效纠正回归误差。
- **ProHMR**：基于归一化流的概率回归方法，输出姿态分布而非单点估计。其拟合变体 **ProHMR-fitting** 使用学习到的姿态先验进行优化，但 ScoreHMR 在模型拟合任务上显著优于它（Table 2）。

**2.2 优化拟合基线**

- **SMPLify**：经典的优化拟合方法，使用 GMM 姿态先验和手工设计的正则项。ScoreHMR 在所有基准上均显著优于 SMPLify，例如在 3DPW 上 PA-MPJPE 降低 9.0 mm（HMR 2.0 + SMPLify: 60.1 mm vs. HMR 2.0 + ScoreHMR-b: 51.1 mm，Table 2）。
- **LGD**（Learning Gradient Descent）和 **LFMM**：基于学习的优化方法，试图用神经网络替代手工设计的优化过程。ScoreHMR 同样优于这些方法（Table 2）。
- **ProHMR-fitting**：将 ProHMR 的归一化流先验用于优化拟合。ScoreHMR 在时序运动细化任务上，Acc Err 降低 21.3%（Table 4: 11.1 vs. 14.1 mm/s²）。

**2.3 技术谱系**

ScoreHMR 的技术路线可追溯到两个方向：
- **扩散模型用于逆问题求解**：借鉴了扩散模型在图像修复、超分辨率等逆问题中的分数引导策略，将其迁移到人体姿态参数的优化中。
- **扩散模型用于人体姿态估计**：与直接使用扩散模型生成姿态分布的工作不同，ScoreHMR 将扩散模型作为先验，通过引导采样实现观测对齐，而非从头生成。

### 3. 适用边界与局限性

基于论文中的实验证据和消融研究，ScoreHMR 的适用边界如下：

**3.1 适用场景**

- **单帧模型拟合**：给定 2D 关键点检测，ScoreHMR 能有效改善回归估计的图像-模型对齐（Table 2）。
- **多视图优化**：通过多视图一致性引导 $\mathcal{L}_{MV}$，ScoreHMR 能融合多视角信息修正单视角的遮挡和歧义（Table 3）。
- **时序运动细化**：通过时间一致性引导 $\mathcal{L}_{temp}$，ScoreHMR 能生成平滑的 3D 人体运动序列（Table 4）。

**3.2 已知局限**

1. **关键点检测依赖性**：当 2D 关键点检测存在严重错误时，引导过程可能失效。Figure 7 展示了失败案例，尽管扩散模型有助于保持一定图像一致性，但性能依然下降。这一局限是**所有基于关键点的优化方法**共有的，非 ScoreHMR 独有。

2. **上游回归网络依赖性**：ScoreHMR 以回归网络的输出为初始化点，最终性能受上游组件影响。Table 1 的消融实验显示，使用 ProHMR 初始化比使用 HMR 2.0 初始化在某些场景下表现更好，说明初始估计质量会影响优化结果。

3. **形状参数优化有限**：消融实验（Appendix F, Table 5）表明，在扩散模型中额外包含 SMPL 形状参数 $\beta$ 并未带来显著的性能提升。论文推测这是因为对单帧回归而言，形状估计已足够简单，但对需要精确形状的任务（如虚拟试衣）可能不是最优。

4. **推理效率**：迭代优化需要多轮 DDIM 反演和采样，可能比单步回归慢。论文未明确报告推理时间，**该点需要手动验证**。

### 4. 开放问题

基于论文的分析和未覆盖的实验设置，以下问题值得进一步探索：

1. **实时性优化**：ScoreHMR 的迭代采样能否通过减少反演步数、使用更小的噪声水平 $\tau$ 或蒸馏技术进一步加速，以满足实时或近实时应用需求？消融实验显示 $\tau=50$ 和 $\Delta t=10$ 时 PA-MPJPE 可降至 48.2 mm（Appendix C），但论文指出小步长对挑战性姿态更鲁棒，需要在速度和鲁棒性之间权衡。

2. **多人物与严重遮挡场景**：当前实验集中在单人物场景，ScoreHMR 在多人物交互、严重遮挡场景下的泛化能力尚未验证。

3. **端到端训练**：当前 ScoreHMR 的扩散模型与回归网络是分离训练的。是否可以将 ScoreHMR 与基于 Transformer 的更强回归网络（如 HMR 2.0）进行端到端训练，使初始估计和优化过程协同优化？

4. **多模态观测融合**：当 2D 关键点不可靠时，是否可以融合其他传感器（如深度相机、IMU）的引导信号？论文的引导框架理论上支持任意可微的观测损失，但多模态融合的具体实现和性能增益尚未探索。

5. **扩散先验的泛化能力**：扩散模型在训练数据覆盖的姿态分布之外的表现如何？对于极端姿态、罕见动作，扩散先验是否仍能提供有效的约束，还是会引入偏差？



## 原文 PDF

![[paperPDFs/CVPR_2024/ScoreHMR_Score_Guided_Diffusion_for_3D_Human_Recovery.pdf]]
