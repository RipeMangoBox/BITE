---
title: "A Step to Decouple Optimization in 3DGS"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Step_to_Decouple_Optimization_in_3DGS.pdf
aliases:
- AG
- SDO3
- AdamW-GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过解耦优化过程，将Sparse Adam、Re-State Regularization (RSR) 和 Decoupled Attribute Regularization (DAR) 三个组件分离并重新组合，形成AdamW-GS优化器。"
primary_logic: "3DGS优化中的耦合可以被解耦并重新组合：Sparse Adam实现异步更新，RSR通过状态衰减模拟隐式更新的有益部分，DAR通过梯度解耦实现可控的正则化。重新组合后的AdamW-GS在保持或提升重建质量的同时，显著减少冗余基元数量，无需额外的剪枝操作。"
claims:
- "Sparse Adam导致更少的死基元（0.048M vs 0.232M），表明Adam中的隐式更新有助于剪枝冗余基元。"
- "AdamW-GS (MC8)在MipNerf360上达到PSNR 28.219，SSIM 0.840，LPIPS 0.182，基元数量变化+4.52%，优于原始MCMC的PSNR 27.948，SSIM 0.833，LPIPS 0.199，基元数量变化-3.75%。"
- "在室外场景中，vanilla 3DGS+AdamW-GS (GS8)减少48.4%的基元，同时PSNR提升0.2 dB，SSIM提升0.01。"
- "梯度耦合导致正则化控制不稳定：当超参数放大10倍时，优化完全失败；而解耦后的DAR可以实现稳定控制。"
---

# A Step to Decouple Optimization in 3DGS

> [!tip] 核心洞察
> 3DGS优化中的耦合可以被解耦并重新组合：Sparse Adam实现异步更新，RSR通过状态衰减模拟隐式更新的有益部分，DAR通过梯度解耦实现可控的正则化。重新组合后的AdamW-GS在保持或提升重建质量的同时，显著减少冗余基元数量，无需额外的剪枝操作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 解耦3DGS优化的一步 |
| 英文题名 | A Step to Decouple Optimization in 3DGS |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oapTMDy2Yh); [Project](https://eliottdjay.github.io/adamwgs/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AdamW-GS |
| Dataset | MipNerf360 |

> [!tip] 效果简介
> - MipNerf360 上，PSNR 为 28.219 (MC8)，对比 27.948 (Original MCMC)，变化 +0.271。
> - MipNerf360 上，SSIM 为 0.840 (MC8)，对比 0.833 (Original MCMC)，变化 +0.007。
> - MipNerf360 上，LPIPS 为 0.182 (MC8)，对比 0.199 (Original MCMC)，变化 -0.017。

## 概述

3DGS（3D Gaussian Splatting）的优化过程存在两种根本性的耦合问题：**更新步耦合**（Adam优化器与同步更新机制导致不可见视角下的基元仍被隐式更新）和**梯度耦合**（正则化损失与光度损失的梯度在Adam动量中混合，导致正则化控制不稳定且难以独立调节）。这两种耦合共同造成了优化效率低下、冗余基元难以自动去除、以及正则化超参数敏感等实际问题。

本文的核心洞察在于：**这些耦合可以被系统性地解耦并重新组合**，从而获得更优的优化器。作者提出AdamW-GS优化器，它由三个独立设计的组件构成：**(1) Sparse Adam**——仅更新当前视角下可见的基元，实现异步优化并消除隐式更新；**(2) Re-State Regularization (RSR)**——通过State Sampling Schedule (StSS)定期采样基元并衰减其动量状态，模拟Adam隐式更新中有益的部分；**(3) Decoupled Attribute Regularization (DAR)**——将正则化梯度与光度损失梯度在动量层面完全解耦，并通过第二动量归一化和裁剪阈值实现稳定可控的正则化。

实验结果表明，AdamW-GS在多个基准上取得了显著效果。在MipNerf360上，AdamW-GS (MC8)达到PSNR 28.219、SSIM 0.840、LPIPS 0.182，优于原始MCMC的27.948/0.833/0.199。更重要的是，在室外场景中，vanilla 3DGS+AdamW-GS (GS8)减少了48.4%的基元数量，同时PSNR提升0.2 dB、SSIM提升0.01；在室内场景中，同样能移除约50%的基元并保持PSNR提升0.1 dB。这种基元压缩完全通过DAR中的可控制正则化自动实现，**无需任何额外的剪枝操作**。此外，AdamW-GS作为即插即用组件，能够有效增强现有方法（如MaskGaussian、Taming-3DGS、Deformable Beta Splatting）的性能，例如将Taming-3DGS的训练时间减少近一半（从20.30分钟降至10.46分钟）。

## 背景与动机

3D高斯溅射（3DGS）在优化过程中存在两种深层耦合，严重制约了优化效率与模型精简能力。第一类是**更新步耦合**：Adam优化器与同步更新机制共同导致不可见视角下的基元也发生隐式更新。具体而言，标准Adam的动量更新（Eq. 2）对所有基元一视同仁，即使某基元在当前视角下不可见（梯度为零），其动量状态仍会因历史梯度的指数移动平均而持续变化，从而在不可见视角下产生非预期的参数漂移。第二类是**梯度耦合**：正则化损失（如不透明度和尺度的L1范数）与光度损失在Adam的动量中耦合（Eq. 6中的 $\nabla\ell + \lambda\nabla\mathcal{R}$）。这种耦合导致两个严重后果：一是正则化控制极不稳定——当超参数放大10倍时，优化完全失败，因为正则化梯度通过动量持续影响后续更新步，使得更新步过度依赖属性梯度而偏离光度梯度引导；二是冗余基元难以自动去除，因为耦合的动量状态模糊了正则化对冗余基元的定向惩罚效果。

现有方法试图通过修改密化过程（如Taming-3DGS）或引入可学习掩码（如MaskGaussian）来控制基元数量，但都未能触及优化器层面的根本问题。3DGS-MCMC虽然通过MCMC采样引入了额外的正则化，但其优化器仍为标准的Adam，梯度耦合问题依然存在。

本文的核心动机是：**解耦3DGS优化中的耦合，并通过重新组合解耦后的组件来构建更高效的优化器**。具体而言，作者识别出三个可解耦的组件：（1）Sparse Adam，通过修改beta参数（Eq. 4）仅更新可见视角下的基元，实现异步优化，消除不可见视角下的隐式更新；（2）Re-State Regularization (RSR)，通过State Sampling Schedule (StSS)定期采样基元并衰减其动量状态（Eq. 5），模拟隐式更新中对冗余基元的有益剪枝作用；（3）Decoupled Attribute Regularization (DAR)，将正则化梯度从动量中完全解耦（Eq. 7），并通过第二动量归一化和裁剪阈值 $C_t$ 实现稳定可控的正则化（Eq. 8）。这三个组件重新组合后形成AdamW-GS优化器，在保持或提升重建质量的同时，显著减少冗余基元数量，且无需额外的剪枝操作。

实验证据表明：Sparse Adam相比Adam产生更少的死基元（0.048M vs 0.232M，Table 1），说明Adam中的隐式更新确实有助于剪枝冗余基元，但Sparse Adam的探索性较差导致性能下降。AdamW-GS (MC8)在MipNerf360上达到PSNR 28.219、SSIM 0.840、LPIPS 0.182，基元数量变化+4.52%，优于原始MCMC的PSNR 27.948、SSIM 0.833、LPIPS 0.199、基元数量变化-3.75%（Table 3）。在室外场景中，vanilla 3DGS+AdamW-GS (GS8)减少48.4%的基元，同时PSNR提升0.2 dB，SSIM提升0.01。这些结果验证了解耦-重组策略的有效性。

## 核心创新

本文的核心创新在于识别并解构了3DGS优化中存在的两类耦合——**更新步耦合**（Adam与同步优化导致不可见视角下的隐式更新）与**梯度耦合**（正则化与光度损失在动量中混合）——并在此基础上提出了一种新的优化器 **AdamW-GS**。其核心洞察是：3DGS优化中的耦合可以被解耦并重新组合，从而在不依赖额外剪枝操作的情况下，实现更高效、可控的优化与冗余基元自动去除。

具体而言，AdamW-GS通过替换三个关键组件（`changed_slots`）实现了这一目标：

1.  **Sparse Adam**：将原始Adam的**同步更新**替换为**异步更新**。通过修改动量更新的beta参数（Eq. 4），Sparse Adam仅更新当前视角下可见的基元，而对不可见基元的梯度置零，从而冻结其动量状态。这直接消除了更新步耦合，使优化更稳定，并显著减少了死基元数量（Table 1: 0.048M vs. 0.232M）。然而，Sparse Adam也因探索性不足而导致重建性能下降（Table 1: PSNR 27.285 vs. 27.507）。

2.  **Re-State Regularization (RSR)**：为了弥补Sparse Adam丧失的探索性，RSR通过**State Sampling Schedule (StSS)** 定期采样基元，并衰减其动量状态（Eq. 5: $m(\theta)_t^{new} = \alpha_1 \times m(\theta)_t^{old}$）。这模拟了原始Adam中隐式更新的有益部分，有效放大了正则化效果并提升了重建质量。

3.  **Decoupled Attribute Regularization (DAR)**：为了解决梯度耦合问题，DAR将正则化梯度与光度损失梯度**解耦**。具体地，光度损失梯度单独维护动量（Eq. 7），而正则化梯度则通过第二动量归一化并受裁剪阈值 $C_t$ 限制后，直接加入到参数更新中（Eq. 8）。这使得正则化控制变得稳定且可预测——避免了耦合情况下超参数放大10倍导致优化完全失败的极端情况。DAR是实现可控冗余基元去除的关键，无需额外的剪枝操作。

这三个组件被重新组合成AdamW-GS优化器。实验证据表明，这一创新在多个基准上有效：在MipNerf360上，AdamW-GS (MC8) 达到了PSNR 28.219，SSIM 0.840，LPIPS 0.182，优于原始MCMC的27.948/0.833/0.199；在室外场景中，vanilla 3DGS+AdamW-GS (GS8) 在基元数量减少48.4%的同时，PSNR提升了0.2 dB，SSIM提升了0.01。这些结果共同支撑了核心创新点的有效性。

## 整体框架

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/016_Figure_3.jpg]]
*Figure 3: a-d: Reconstruction results visualization. More can be found in Appendix Sec.K. e-f: The Reallocated Primitive Number in 3DGS-MCMC Framework. For outdoor scenes, MC17 and MC8 differ only in the StSS sampling ratio, where MC8(StSSMC3)>MC17(StSSMC1)=MCMC-Sparse-RSR. For indoor scenes, MC8 uses StSSMC1. More information can be checked in Table 2*

AdamW-GS 是一个解耦式优化器，其整体 pipeline 并非引入新的网络结构或渲染管线，而是将 3DGS 的标准 Adam 优化过程拆解为三个独立组件，再以特定方式重新组合，从而解决优化中的两种耦合问题：更新步耦合（同步Adam导致的不可见视角隐式更新）和梯度耦合（正则化与光度损失在动量中的混合）。

**输入输出流**：输入与 vanilla 3DGS 完全相同——多视角图像及对应的稀疏点云初始化。输出仍是一组高斯基元（位置、不透明度、尺度、旋转、颜色），通过标准的α混合渲染方程（附录 Eq. 13）生成新视角图像。变化仅发生在优化器的内部状态管理和参数更新规则上。

**模块关系**：三个核心模块按顺序组合，形成完整的 AdamW-GS 优化器：

1. **Sparse Adam**（异步更新层）：修改 Adam 的动量衰减系数，使得仅当前视角下可见的基元参与梯度更新（Eq. 4: `β' = β × V + (1 - V)`）。不可见基元的动量被冻结（β=1），从而消除不可见视角下的隐式更新。这是整个解耦的基石，直接导致更少的死基元（0.048M vs 0.232M），但单独使用时探索性下降，性能退化（Table 1: GS2 PSNR 27.285 vs GS1 27.507）。

2. **Re-State Regularization (RSR)**（状态衰减层）：在固定间隔（由 State Sampling Schedule (StSS) 定义）内，对采样到的基元的动量和二阶矩进行衰减（Eq. 5: `m_new = α₁ × m_old`, `v_new = α₂ × v_old`）。这模拟了 Adam 中隐式更新的有益部分——即对不可见基元状态的缓慢调整，但以可控的方式实现。RSR 有效放大了正则化的效果，弥补了 Sparse Adam 探索性不足的问题。

3. **Decoupled Attribute Regularization (DAR)**（梯度解耦层）：将正则化梯度从光度损失梯度中完全分离。光度损失梯度按照标准 Adam 方式更新动量（Eq. 7），而正则化梯度则通过第二动量归一化后，以裁剪阈值 `C_t` 限制幅度，直接加到更新步中（Eq. 8）。这解决了梯度耦合导致的正则化控制不稳定问题——当超参数放大10倍时，耦合版本优化完全失败，而 DAR 仍能稳定控制。

**重新组合逻辑**：三个组件并非简单串联。Sparse Adam 提供异步更新的基础框架；RSR 在其上增加可控的状态衰减，模拟隐式更新的好处；DAR 则独立于前两者，专门处理正则化与光度损失的耦合。最终形成 AdamW-GS 优化器，其整体更新规则为：`θ_{t+1} = θ_t - η × [ m̂(θ)_t' / (√v̂(θ)_t' + ε) + min( λ_θ ∇R(θ)/N_I / (√v̂(θ)_t' + ε), C_t ) ]`（Eq. 8），其中第一项来自解耦后的光度损失动量，第二项是裁剪后的正则化项。

**关键因果链**：Sparse Adam 消除隐式更新 → 减少死基元但降低探索性 → RSR 通过状态衰减恢复探索性并放大正则化效果 → DAR 确保正则化可控且不干扰光度损失优化 → 最终实现：在保持或提升重建质量（MipNerf360 PSNR 28.219 vs 27.948）的同时，显著减少冗余基元（室外场景 -48.4%），且无需额外的剪枝操作。

**与基线方法的集成方式**：AdamW-GS 作为即插即用的优化器替换，可无缝集成到 vanilla 3DGS、3DGS-MCMC、MaskGaussian、Taming-3DGS、Deformable Beta Splatting 等不同框架中。实验表明，在所有集成场景中均观察到重建质量的提升或基元数量的减少（Table 3-9），且训练时间减少近一半（Taming-3DGS: 20.30 min → 10.46 min）。

## 核心模块与公式推导

### 总损失函数与优化瓶颈

3DGS 优化的总损失函数为：

$$
\mathcal { L } = \underbrace { ( 1 - \lambda _ { 1 } ) \mathcal { L } _ { 1 } + \lambda _ { 1 } \mathcal { L } _ { D S S I M } } _ { \mathrm { p h o t o m e t r i c ~ l o s s : ~ } \ell } + \underbrace { \lambda _ { o } | o | _ { 1 } + \lambda _ { s } | s | _ { 1 } } _ { \mathrm { r e g u l a r i z a t i o n ~ l o s s : ~ } \mathcal { R } }
$$

其中 $\ell$ 是光度损失（L1 和 D-SSIM），$\mathcal{R}$ 是正则化损失（不透明度 $o$ 和尺度 $s$ 的 L1 范数）。该论文的核心洞察是：标准 Adam 优化器在 3DGS 中引入了两种有害的耦合——**更新步耦合**（同步优化导致不可见视角下的基元发生隐式更新）和**梯度耦合**（正则化与光度损失的梯度在动量中混合，导致正则化控制不稳定）。这导致冗余基元难以自动去除，且正则化超参数鲁棒性差。

### Sparse Adam：解耦更新步

标准 Adam 的参数更新为：

$$
\theta_{t+1} = \theta_t - \eta \times \frac{\hat{m}(\theta)_t}{\sqrt{\hat{v}(\theta)_t} + \epsilon}
$$

其中 $m(\theta)_t = \beta_1 m(\theta)_{t-1} + (1-\beta_1)g(\theta)_t$ 和 $v(\theta)_t = \beta_2 v(\theta)_{t-1} + (1-\beta_2)g(\theta)_t^2$ 是梯度的指数移动平均。

Sparse Adam 通过修改动量更新中的 $\beta$ 系数来实现异步更新：

$$
\beta^{\prime} = \beta \times \mathcal{V} + (1-\mathcal{V})
$$

其中 $\mathcal{V}$ 是可见性指示器（基元在当前视角下可见时为 1，否则为 0）。当 $\mathcal{V}=0$ 时 $\beta^{\prime}=1$，这意味着不可见基元的动量被冻结，从而消除了隐式更新。实验证据（Table 1）表明，Sparse Adam 导致更少的死基元（0.048M vs 0.232M），表明 Adam 中的隐式更新实际上有助于剪枝冗余基元，但 Sparse Adam 本身探索性较差，性能有所下降。

### Re-State Regularization (RSR)：模拟隐式更新的有益部分

为了保留隐式更新的有益部分（即剪枝冗余基元的能力），RSR 在固定间隔内对采样基元的优化器状态进行衰减：

$$
m(\theta)_t^{\mathrm{new}} = \alpha_1 \times m(\theta)_t^{\mathrm{old}}, \quad v(\theta)_t^{\mathrm{new}} = \alpha_2 \times v(\theta)_t^{\mathrm{old}}, \quad 0 \leq \alpha_1 < 1, 0 \leq \alpha_2 < 1
$$

RSR 通过 State Sampling Schedule (StSS) 控制采样频率和衰减强度。论文表明，RSR 能有效放大正则化效果并提升重建质量，但它仍然保留了梯度耦合问题。

### Decoupled Attribute Regularization (DAR)：解耦梯度耦合

梯度耦合的核心问题在于正则化梯度与光度损失梯度在动量中混合。解耦后的光度损失动量更新为：

$$
m(\theta)_t^{\prime} = \beta_1^{\prime} \times m(\theta)_{t-1}^{\prime} + (1-\beta_1^{\prime}) \times \frac{\nabla \ell(\theta)}{N_I}, \quad v(\theta)_t^{\prime} = \beta_2^{\prime} \times v(\theta)_{t-1}^{\prime} + (1-\beta_2^{\prime}) \times \left(\frac{\nabla \ell(\theta)}{N_I}\right)^2
$$

其中 $N_I$ 是当前视角下的可见基元数量。注意这里只包含光度损失梯度，正则化梯度被完全分离。

DAR 的最终参数更新规则为：

$$
\theta_{t+1} = \theta_t - \eta \times \left[ \frac{\hat{m}(\theta)_t^{\prime}}{\sqrt{\hat{v}(\theta)_t^{\prime}} + \epsilon} + \min\left( \lambda_\theta \frac{\nabla \mathcal{R}(\theta) / N_I}{\sqrt{\hat{v}(\theta)_t^{\prime}} + \epsilon}, \mathcal{C}_t \right) \right]
$$

关键设计包括：
1. **正则化梯度通过光度损失的二阶矩归一化**：$\nabla \mathcal{R}(\theta) / \sqrt{\hat{v}(\theta)_t^{\prime}}$，这确保了正则化步长与光度更新步长具有可比性。
2. **裁剪阈值 $\mathcal{C}_t$**：限制正则化步长的最大值，防止过强的正则化导致优化崩溃。实验表明，当超参数放大 10 倍时，未解耦的优化完全失败，而 DAR 可以实现稳定控制。

对于不透明度和尺度属性，具体更新为：

不透明度（logit $\tau$，激活函数 $\upsilon = \sigma(\tau) = 1/(1+e^{-\tau})$）更新：

$$
\tau_{t+1} = \tau_t - \eta_\tau \times \left[ \frac{\hat{m}(\tau)_t'}{\sqrt{\hat{v}(\tau)_t'} + \epsilon} + \min\left(\lambda_o \frac{\nabla\sigma(\tau)/N_I}{\sqrt{\hat{v}(\tau)_t'} + \epsilon}, \mathcal{C}_t\right) \right]
$$

尺度（log $\kappa$，激活函数 $s = \exp(\kappa)$）更新：

$$
\kappa_{t+1} = \kappa_t - \eta_\kappa \times \left[ \frac{\hat{m}(\kappa)_t'}{\sqrt{\hat{v}(\kappa)_t'} + \epsilon} + \min\left(\lambda_s \frac{\nabla\exp(\kappa)/N_I}{\sqrt{\hat{v}(\kappa)_t'} + \epsilon}, \mathcal{C}_t\right) \right]
$$

### AdamW-GS：重新组合

AdamW-GS 将上述三个组件重新组合：Sparse Adam 实现异步更新，RSR 通过状态衰减模拟隐式更新的有益部分，DAR 通过梯度解耦实现可控的正则化。论文强调，该方法的基元剪枝完全依赖于 opacity DAR，不包含额外的剪枝操作。在 MipNerf360 上，AdamW-GS (MC8) 达到 PSNR 28.219，SSIM 0.840，LPIPS 0.182，基元数量变化 +4.52%，优于原始 MCMC 的 PSNR 27.948，SSIM 0.833，LPIPS 0.199，基元数量变化 -3.75%（Table 3）。在室外场景中，vanilla 3DGS + AdamW-GS (GS8) 减少 48.4% 的基元，同时 PSNR 提升 0.2 dB，SSIM 提升 0.01。

## 实验与分析

### 主结果：AdamW-GS在多个基准上实现重建质量与基元效率的双赢

AdamW-GS的核心优势在于：在不引入额外剪枝操作的前提下，通过优化器层面的解耦设计，同时提升或保持重建质量并显著减少冗余基元。在MipNerf360基准上，3DGS-MCMC框架下的AdamW-GS变体MC8达到了PSNR 28.219、SSIM 0.840、LPIPS 0.182，基元数量变化ΔNa为+4.52%，全面优于原始MCMC的PSNR 27.948、SSIM 0.833、LPIPS 0.199、ΔNa -3.75%（Table 3）。这一结果的关键在于：MC8虽然基元总数略有增加（+4.52%），但死基元（dead primitives）数量从Adam的0.232M骤降至Sparse Adam的0.048M（Table 1），表明优化器状态解耦后，基元被更有效地利用，而非被隐式更新“杀死”。

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/001_Table_1.jpg]]

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/018_Table_3.jpg]]
*Table 3: Quantitative results in MipNerf360 of different methods. MC8 and GS8/GS7 denote our proposed AdamW-GS variants. More information of MC8 is provided in Table 2. All variants share the same hyperparameters except for the StSS schedule. Following the design used in 3DGS-MCMC, outdoor scenes for vanilla 3DGS use a high-ratio StSS, while indoor scenes use a lowratio StSS. As discussed in Sec. 4.4, GS7 is the noise without opacity reset version to study the effectiveness of exploration. A per-scene organization of results, including detailed configurations and additional experiments, is presented in Sec. K*

在vanilla 3DGS框架下，AdamW-GS（GS8）的效果更为显著：室外场景基元减少48.4%，同时PSNR提升0.2 dB、SSIM提升0.01；室内场景基元减少50%，PSNR仍提升0.1 dB。这种“减量提质”的反直觉现象揭示了原始Adam优化器中耦合的负面效应——同步更新和动量耦合导致大量基元在不可见视角下被隐式更新，形成冗余的死基元，而这些死基元不仅消耗计算资源，还可能干扰有效基元的优化。

在Deep Blending和Tank & Temples数据集上（Table 4），3DGS-MCMC + AdamW-GS分别达到PSNR 30.417和24.726，均优于3DGS + AdamW-GS（PSNR 30.260和24.303），说明AdamW-GS在不同框架和数据集上具有一致的提升效果。值得注意的是，在Tank & Temples上，3DGS-MCMC + AdamW-GS的基元数量变化为+6.7%，而vanilla 3DGS + AdamW-GS为-48.5%，这表明MCMC框架本身具有更强的基元分配能力，而AdamW-GS在其中主要起质量提升作用。

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/019_Table_4.jpg]]
*Table 4: Quantitative results in Deep Blending and Tank & Temples. (m: million.)*

### 消融实验：三个组件的因果拆解

消融实验揭示了每个组件的独立贡献和相互作用机制（Table 2）。Sparse Adam是性能提升的基石：它通过仅更新可见视角下的基元，将死基元从0.232M降至0.048M（Table 1），但单独使用时性能下降（PSNR从27.507降至27.285，Table 1中GS2 vs GS1）。这种“更稳定但探索性更差”的特性（Observation 1 & 2）表明，Sparse Adam虽然消除了隐式更新的负面影响，但也失去了Adam中隐式更新带来的有益探索能力。

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/017_Table_2.jpg]]
*Table 2: Quantitative results in MipNerf-360 with different components. Detailed descriptions of Sparse Adam, AIU/RSR, and DAR are provided in Sec. 4.1, Sec. 4.2, and Sec. 4.3, respectively. All RSR and DAR settings remain fixed across experiments, except for the StSS schedule. The StSS sampling ratios used in this table are as follows: for outdoor scenes, MC8 (StSSMC3) > MC7 (StSSMC2) > others (StSSMC1), while for indoor scenes, MC8 = MC7 = others (StSSMC1). The complete StSS schedules for each configuration are illustrated in Figure 9. Appendix Sec. K provides per-scene experimental results, including detailed configurations and additional experiments with a broader range of settings*

Re-State Regularization (RSR) 正是为恢复这种探索能力而设计。通过State Sampling Schedule (StSS)定期衰减采样基元的动量状态（Eq. 5），RSR模拟了隐式更新的有益部分——即对不可见基元状态的适度调整。实验显示，在Sparse Adam基础上加入RSR后（Table 2中MC4 vs MC3），PSNR从27.948提升至28.014，同时基元数量变化从-25.73%变为-22.90%，说明RSR有效放大了正则化效果并提升了重建质量。

Decoupled Attribute Regularization (DAR) 解决了梯度耦合问题。原始Adam中，正则化梯度与光度损失梯度在动量中耦合（Eq. 6），导致正则化控制不稳定——当超参数放大10倍时，优化完全失败。DAR通过将正则化梯度从动量中解耦（Eq. 7），并使用二阶动量归一化和裁剪阈值C_t（Eq. 8），实现了稳定可控的正则化。实验表明，加入DAR后（Table 2中MC6 vs MC5），PSNR从27.962提升至28.219，基元数量变化从-12.89%变为+4.52%，说明DAR不仅稳定了优化，还通过可控制的正则化自动实现了冗余基元的去除。

三个组件的组合效果是协同而非加和的：Sparse Adam提供了稳定的基础优化，RSR恢复了必要的探索能力，DAR则实现了精确的正则化控制。这种“解耦-重新组合”的策略使得AdamW-GS在保持优化效率的同时，避免了原始Adam中耦合带来的负面效应。

### 跨框架泛化：AdamW-GS作为即插即用优化器

AdamW-GS的通用性通过在多个现有方法上的集成实验得到验证。在MaskGaussian上（Table 5），AdamW-GS不仅保持了PSNR提升，还在室内场景中额外剪枝约7%的基元。这一结果的关键在于：MaskGaussian的可学习掩码与AdamW-GS的异步更新机制协同工作——Sparse Adam避免了同步掩码更新导致的“破坏性剪枝行为”，而DAR则提供了更稳定的正则化控制。

![[assets/figures/papers/iclr26_0004_oapTMDy2Yh_A_Step_to_Decouple_Optimization_in_3DGS/figures/020_Table_5.jpg]]
*Table 5: Quantitative results for MaskGaussian*

在Taming-3DGS上（Table 8），AdamW-GS将训练时间减少近一半（从20.30分钟降至10.46分钟），同时PSNR从27.386提升至27.537。时间减少的主要原因是Sparse Adam将更新步骤时间降低了约50%（Table 6），因为只需更新可见基元而非全部基元。在Deformable Beta Splatting上（Table 9），AdamW-GS在9个场景中的8个上提升了重建质量（PSNR从29.362提升至29.643），唯一的例外Treehill场景出现了过拟合，这提示AdamW-GS在特定场景下可能需要调整StSS调度。

### 失败模式与局限性

尽管整体表现优异，AdamW-GS仍存在系统性失败模式（Figure 7）：边界区域伪影（Room场景）、背景模糊（Garden场景）、几何不一致（Bosai场景的深度图异常）以及漂浮物问题（Bicycle场景的椭球体可视化）。这些失败案例的共同特征是：在视角覆盖不足或几何结构复杂的区域，优化器解耦虽然提升了效率，但无法弥补数据本身的信息缺失。例如，边界区域的伪影源于视角覆盖稀疏，导致基元在这些区域无法获得足够的光度梯度约束；几何不一致则反映了当前框架缺乏显式的几何先验。

此外，PSNR误差棒图（Figure 8）显示，AdamW-GS在九个场景上的PSNR方差与基线方法相当，说明其稳定性并未因解耦而降低。但这也意味着，优化器层面的改进无法解决数据驱动的根本限制——当场景本身存在视角稀疏或几何复杂区域时，任何优化器都无法凭空创造信息。

### 关键图表结论

- **Table 1 & Figure 1**：Sparse Adam通过消除隐式更新，将死基元从0.232M降至0.048M，但单独使用时性能下降（PSNR -0.222 dB），说明隐式更新虽有害但包含有益探索成分。
- **Table 2**：三个组件的消融显示，DAR是实现基元数量控制的关键（ΔNa从-12.89%变为+4.52%），而RSR主要贡献于质量提升（PSNR +0.066 dB）。
- **Table 3 & Figure 2**：AdamW-GS（MC8/GS8）在MipNerf360上达到与MaskGaussian相当甚至更优的性能，且无需额外剪枝操作，基元数量变化曲线显示DAR在密化阶段后持续发挥作用。
- **Table 4 & Figure 3**：在Deep Blending和Tank & Temples上的泛化验证表明，AdamW-GS在不同数据集和框架上具有一致的提升效果，且MCMC框架下的基元重分配更高效。
- **Table 6 & Figure 4**：Sparse Adam将更新步骤时间降低约50%，使AdamW-GS在减少训练时间的同时保持或提升质量，这是其实用性的关键优势。

## 方法谱系与知识库定位

AdamW-GS 的贡献在于识别并解耦了 3DGS 优化中的两类耦合，而非提出全新的网络架构或渲染范式。该方法直接挑战了 vanilla 3DGS 和 3DGS-MCMC 中默认的 Adam 优化器，其设计动机源于对优化过程中“更新步耦合”与“梯度耦合”的因果分析。

**与基线方法的关系**：AdamW-GS 作为优化器替换，可即插即用地应用于多种 3DGS 变体。在 vanilla 3DGS 上，它通过 Sparse Adam 实现异步更新，仅更新可见视角下的基元，避免了不可见视角下的隐式更新。实验表明，Sparse Adam 导致更少的死基元（0.048M vs 0.232M），表明 Adam 中的隐式更新有助于剪枝冗余基元，但 Sparse Adam 本身探索性较差，性能下降。为此，Re-State Regularization (RSR) 通过 State Sampling Schedule (StSS) 定期衰减采样基元的动量状态，模拟了隐式更新的有益部分。在 3DGS-MCMC 框架上，AdamW-GS 进一步解决了梯度耦合问题：原始 Adam 中，正则化损失与光度损失的梯度在动量中耦合（Eq. 6），导致正则化控制不稳定（超参数放大10倍时优化完全失败）。Decoupled Attribute Regularization (DAR) 通过将正则化梯度与光度损失梯度解耦，并使用第二动量归一化和裁剪阈值 `C_t` 实现稳定可控的正则化。重新组合后的 AdamW-GS 在 MipNerf360 上达到 PSNR 28.219，SSIM 0.840，LPIPS 0.182，基元数量变化+4.52%，优于原始 MCMC 的 PSNR 27.948，SSIM 0.833，LPIPS 0.199，基元数量变化-3.75%（Table 3）。在室外场景中，vanilla 3DGS+AdamW-GS 减少48.4%的基元，同时 PSNR 提升0.2 dB，SSIM 提升0.01。

**与后续方法的兼容性**：AdamW-GS 的通用性在其与多种先进方法的组合中得到验证。在 MaskGaussian 上，它额外剪枝约7%的室内场景基元并提升 PSNR。在 Taming-3DGS 上，它将训练时间减少近一半（20.30分钟→10.46分钟）。在 Deformable Beta Splatting 上，它在9个场景中的8个上提升重建质量。这种兼容性源于 AdamW-GS 仅修改优化器状态管理，不改变基元表示或渲染方程。

**适用边界**：该方法的核心假设是优化耦合是性能瓶颈。这适用于需要大量基元且优化不稳定的场景（如室外场景基元减少48.4%）。然而，在 Treehill 场景中，Deformable Beta Splatting 出现过拟合，AdamW-GS 未能改善，表明当基元表示本身存在缺陷时，仅优化器层面的改进可能不足。此外，ABE-Split 和 Densification Extending 等策略表明，密化策略与优化器存在交互，需要联合调整。

**局限与开放问题**：首先，RSR 的 StSS 调度依赖于场景类型（室内/室外）的手工设计，缺乏自适应机制。其次，DAR 对不透明度和尺度使用相同的裁剪阈值 `C_t`，但不同属性的梯度分布差异可能要求差异化处理。第三，AdamW-GS 虽减少了死基元，但未能完全消除，部分边界区域仍存在伪影（Figure 7）。开放问题包括：(1) 能否进一步解耦不同属性的正则化，实现更精细的控制？(2) 能否设计自适应 StSS 调度，无需手动区分场景类型？(3) 当基元表示本身存在局限时（如 Treehill 场景），优化器层面的改进能否与表示学习协同？(4) 该方法在更大规模场景或动态场景中的泛化性尚未验证。这些问题的解决需要超越优化器设计，进入基元表示和场景理解的更深层次。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Step_to_Decouple_Optimization_in_3DGS.pdf

![[paperPDFs/ICLR_2026/A_Step_to_Decouple_Optimization_in_3DGS.pdf]]
