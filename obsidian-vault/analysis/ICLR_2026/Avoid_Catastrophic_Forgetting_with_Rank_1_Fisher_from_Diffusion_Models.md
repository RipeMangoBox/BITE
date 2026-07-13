---
title: "Avoid Catastrophic Forgetting with Rank-1 Fisher from Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Avoid_Catastrophic_Forgetting_with_Rank_1_Fisher_from_Diffusion_Models.pdf
project_link: null
code_link: https://github.com/Teachable-AI-Lab/iclr2026-rank1-fisher
aliases:
- R1EGD
- ACFR1FFDM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "The method approximates diffusion-model empirical Fisher information by a mean-gradient rank-one direction and uses it in EWC."
primary_logic: "It estimates the dominant low-SNR curvature direction, penalizes parameter drift along that direction, and combines the penalty with generative distillation replay."
claims:
- "The note argues low-SNR diffusion gradients become nearly collinear, making rank-one Fisher effective."
- "Rank-one EWC captures a dominant curvature direction at cost comparable to diagonal EWC."
- "Combining rank-one EWC with generative distillation reduces forgetting on MNIST, FashionMNIST, CIFAR-10, and ImageNet-1k."
---

# Avoid Catastrophic Forgetting with Rank-1 Fisher from Diffusion Models

> [!tip] 核心洞察
> 扩散模型的低SNR区域使每样本梯度与均值近似共线，导致经验Fisher有效秩为一。基于此设计的秩一EWC惩罚项能更好地约束参数更新方向，与生成式蒸馏结合时，重放促进跨任务参数共享，EWC约束重放引起的漂移，两者互补。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用扩散模型的秩一Fisher避免灾难性遗忘 |
| 英文题名 | Avoid Catastrophic Forgetting with Rank-1 Fisher from Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zCZcbRsc4g) · [GitHub](https://github.com/Teachable-AI-Lab/iclr2026-rank1-fisher) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Rank-1 EWC with Generative Distillation |
| Dataset | MNIST, FashionMNIST |

> [!tip] 效果简介
> - MNIST 上，Average FID (AFID) 为 7.6 ± 0.1，对比 GD: 10.1 ± 0.9; Diag: 14.3 ± 1.3，变化 优于GD和Diag。
> - MNIST 上，Forgetting (F) 为 0.6 ± 0.1，对比 GD: 2.3 ± 0.8; Diag: 51.1 ± 4.2，变化 遗忘几乎消除。
> - FashionMNIST 上，Average FID (AFID) 为 15.4 ± 0.6，对比 GD: 19.1 ± 0.9; Diag: 27.7 ± 2.2，变化 优于GD和Diag。

## 概要

本文提出了一种针对扩散模型的持续学习方法，核心思想是利用扩散模型在低信噪比（SNR）区域中经验Fisher信息矩阵的秩一结构，设计了一种计算成本与对角近似相同但能捕获主导曲率方向的秩一EWC（Elastic Weight Consolidation）惩罚项。该方法与生成式蒸馏（Generative Distillation）结合，在类增量图像生成任务中显著减少了灾难性遗忘。实验表明，在MNIST和FashionMNIST上遗忘几乎被消除，在ImageNet-1k上遗忘相比仅使用生成式蒸馏减少了一半以上。

持续学习（Continual Learning）的核心挑战是灾难性遗忘（Catastrophic Forgetting, McCloskey & Cohen, 1989），即模型在学习新任务时丢失先前任务的知识。现有方法存在根本性局限：

- **重放（Replay）方法**：依赖强生成器生成重放样本，但生成器本身会受分布漂移影响，导致累积误差。
- **弹性权重巩固（EWC, Kirkpatrick et al., 2017）**：使用对角Fisher近似，忽略了参数间的相关性，在过参数化模型中难以找到任务间的共享最优解。

扩散模型（Ho et al., 2020; Song et al., 2021a）本身具备生成高质量重放样本的能力，但其梯度结构尚未被充分研究。本文的出发点是：扩散模型在低SNR区域是否具有特殊的梯度结构，从而可以设计更有效的EWC惩罚项？

## 核心方法与创新机理

本文的核心洞察是：扩散模型在低SNR区域，其经验Fisher信息矩阵近似为秩一结构，且主导特征方向与平均梯度对齐。基于此，本文提出：

1. **秩一Fisher近似**：利用扩散模型低SNR区域的梯度共线性，将经验Fisher近似为平均梯度的外积：$F = \mathbb{E}[gg^\top] \approx \alpha u u^\top, \quad u = \mathbb{E}[g]$
2. **秩一EWC惩罚项**：基于秩一Fisher近似设计EWC惩罚项，计算成本与对角近似相同，但能捕获主导曲率方向：$\mathcal{L}_{\mathrm{Rank-1}}(\theta) = \mathcal{L}_T(\theta) + \frac{\lambda}{2} \sum_{k=1}^{T-1} c_k^\star (\mu_k^\top (\theta - \theta_k^\star))^2$
3. **生成式蒸馏与秩一EWC的互补结合**：生成式蒸馏促进跨任务参数共享，秩一EWC约束重放引起的分布漂移，两者互补。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/001_Figure_1.jpg]]
*Figure 1: MSE between model input $x _ { t }$ and the scaled prediction $\hat { x _ { t } }$ at each timestep.*

本文方法的整体框架包含以下模块：

| 模块 | 角色 |
|------|------|
| 扩散模型（DDPM/DDIM） | 作为生成模型，用于生成高质量重放样本 |
| 秩一Fisher估计器 | 从模型梯度中计算平均梯度μ和标量c*，构建秩一Fisher近似 |
| 秩一EWC惩罚项 | 在持续学习过程中，对参数更新施加沿主导曲率方向的约束 |
| 生成式蒸馏模块 | 鼓励当前模型在重放样本上匹配教师模型的去噪行为 |

整体训练流程为：在每个新任务上，使用生成式蒸馏损失和秩一EWC惩罚项联合优化模型参数。生成式蒸馏鼓励当前模型在重放样本上匹配教师模型的去噪行为，而秩一EWC则约束参数更新沿主导曲率方向。

### 5.1 扩散模型基础

扩散模型的前向过程定义为马尔可夫链，逐步向数据添加高斯噪声：

$$q(x_t | x_{t-1}) \sim \mathcal{N}(\sqrt{1-\beta_t} x_{t-1}, \beta_t \mathbf{I}), \quad q(x_t | x_0) \sim \mathcal{N}(\sqrt{\bar{\alpha}_t} x_0, (1-\bar{\alpha}_t) \mathbf{I})$$

训练目标是最小化去噪分数匹配损失的加权变分下界：

$$\mathcal{L}_{\mathrm{simple}}(\theta) = \frac{1}{2} \mathbb{E}_{t, x_0, \varepsilon \sim \mathcal{N}(0, \mathbf{I})} \left[ \| \varepsilon - \varepsilon_\theta(x_t, t) \|_2^2 \right], \quad x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1-\bar{\alpha}_t} \varepsilon$$

### 5.2 秩一Fisher的理论推导

**命题1**：随着SNR降低，噪声数据分布的分数近似为缩放后的恒等映射：$s_t^*(x_t) \approx -x_t/(1 - \bar{\alpha}_t)$。

**假设1**：模型分数$s_\theta(x_t, t)$在模型学习到缩放后的恒等映射时近似为线性函数$A_\theta x_t$。

**命题2**：随着SNR降低且模型收敛，每样本梯度$\nabla_\theta \mathcal{L}_{DSM}(\theta; x_t)$与其总体均值共线。

**定理1**：在命题1和2下，经验Fisher $F_t(\theta)$近似为秩一，其特征向量为$\mu_t(\theta) = \mathbb{E}[g(x_t';\theta)]$，特征值为$\mu_t^\top F_t \mu_t / \|\mu_t\|^4$。

### 5.3 秩一EWC惩罚项

EWC将持续学习视为近似贝叶斯更新，其目标函数为：

$$\mathcal{L}_{\mathrm{EWC}}(\theta) = \mathcal{L}_T(\theta) + \frac{\lambda}{2} \sum_{k=1}^{T-1} (\theta - \theta_k^*)^\top F^{(k)} (\theta - \theta_k^*)$$

利用秩一Fisher近似，本文推导出实用的秩一EWC惩罚项：

$$\mathcal{L}_{\mathrm{Rank-1}}(\theta) = \mathcal{L}_T(\theta) + \frac{\lambda}{2} \sum_{k=1}^{T-1} c_k^\star (\mu_k^\top (\theta - \theta_k^\star))^2$$

其中最优标量$c^\star = \frac{\mathbb{E}[(\mu^\top g)^2]}{\|\mu\|^4}$。

### 5.4 生成式蒸馏

生成式蒸馏损失鼓励当前模型在重放样本上匹配教师模型的去噪行为：

$$\mathcal{L}_{\mathrm{GD}}(\theta) = \mathbb{E}_{\tilde{x} \sim \tilde{\mathcal{D}}} \left[ \frac{1}{2} \| \varepsilon_\theta(\tilde{x}) - \varepsilon_{\theta_{T-1}^\star}(\tilde{x}) \|_2^2 \right]$$

完整目标函数为：$\mathcal{L}_{\mathrm{total}}(\theta) = \mathcal{L}_{\mathrm{Rank-1}}(\theta) + \mathcal{L}_{\mathrm{GD}}(\theta)$

## 实验与关键发现

### 6.1 主要结果

Table 1展示了各方法在所有数据集上的最终平均FID（AFID）和平均遗忘（F）：

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/011_Table_1.jpg]]
*Table 1: Average FID at the final task and average forgetting across methods and datasets. Standard errors are reported over 3 random seeds.*

| 数据集 | 指标 | 仅GD | 对角EWC+GD | 秩一EWC+GD |
|--------|------|------|------------|------------|
| MNIST | AFID | 10.1 ± 0.9 | 14.3 ± 1.3 | **7.6 ± 0.1** |
| MNIST | F | 2.3 ± 0.8 | 51.1 ± 4.2 | **0.6 ± 0.1** |
| FashionMNIST | AFID | 19.1 ± 0.9 | 27.7 ± 2.2 | **15.4 ± 0.6** |
| FashionMNIST | F | 3.9 ± 0.5 | 81.7 ± 4.7 | **0.9 ± 0.3** |
| CIFAR-10 | AFID | 61.2 ± 3.2 | 72.6 ± 3.2 | **50.5 ± 1.2** |
| CIFAR-10 | F | 16.6 ± 0.6 | 74.4 ± 3.5 | **7.4 ± 1.2** |
| ImageNet-1k | AFID | 69.0 ± 2.2 | 73.8 ± 2.8 | **48.5 ± 1.9** |
| ImageNet-1k | F | 46.2 ± 12.9 | 34.2 ± 3.6 | **15.2 ± 4.8** |

关键发现：
- 秩一EWC+GD在所有数据集上均取得最佳AFID和最低遗忘。
- 在MNIST和FashionMNIST上遗忘几乎消除（F < 1.0）。
- 在ImageNet-1k上，遗忘相比仅GD减少一半以上（15.2 vs 46.2）。
- 对角EWC+GD在多数数据集上表现不如仅GD，说明对角Fisher近似在扩散模型中不适用。

### 6.2 消融实验

**无正则化基线**（Table 6）：移除正则化（λ=0）导致所有数据集上生成质量显著下降和严重遗忘（CIFAR-10: FID=115.4, F=72.5; MNIST: FID=102.6, F=93.7）。

**无生成式蒸馏**（Table 1）：EWC（对角或秩一）单独使用在所有数据集上遗忘严重（MNIST: F=51.1-58.3; FashionMNIST: F=81.7-82.1），说明EWC需要与重放结合。

**低秩消融**（Table 5）：增加近似秩超过1（rank-2到rank-5）对性能提升很小，支持曲率已由主导方向充分捕获的观点。例如，在CIFAR-10上，rank-2的FID为57.5±2.6，遗忘为15.9±1.8，均不如秩一方法（FID=50.5±1.2, F=7.4±1.2）。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/026_Table_5.jpg]]
*Table 5: Low-rank ablations using rank-k Fisher approximations (estimated via stochastic power iteration) versus our mean-gradient rank-1 estimate. We report final FID and average forgetting (mean ± standard error).*

### 6.3 秩一Fisher的实证验证

**Figure 1**：随着时间步增加（SNR降低），模型输入$x_t$与缩放预测$\hat{x_t}$之间的MSE趋近于0，验证了命题1。

**Figure 2**：每样本梯度与均值之间的绝对余弦相似度热图显示，中后期时间步共线性更强（更深红色），验证了命题2。

**Figure 3**：
- (a) 不同时间步的$\mu_t(\theta)$之间高度对齐，允许蒙特卡洛采样时间步。
- (b) 前5大特征值显示$\lambda_1$主导，幅度随时间步降低。
- (c) 特征值比$r_t = \lambda_2/\lambda_1$在t=700时最小（0.022），表明低SNR区域秩一行为最强。
- (d) 秩一近似的相对Frobenius误差在中后期时间步低于对角近似；对角近似误差接近1.0，表明曲率集中在非对角项。

**Figure 6**：缩减UNet变体的特征值分析显示，秩一行为随模型规模增大而更明显。

### 6.4 持续学习过程分析

**Figure 4**：平均FID曲线显示，秩一EWC+GD在所有数据集上保持更低FID。在ImageNet-1k上，仅GD和对角EWC+GD在任务10附近发散，而秩一EWC+GD的FID仅逐渐增加。

**Figure 5**：ImageNet-1k选定类别的生成图像示例显示，秩一方法在持续学习过程中保持图像清晰度，而仅GD和对角方法在后期任务中生成噪声图像。

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/023_Table_2.jpg]]
*Table 2: Training configurations used across datasets.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/024_Table_3.jpg]]
*Table 3: Average training runtime (hours) and GPU used per dataset/method.*

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_zCZcbRsc4g_Avoid_Ca/figures/025_Table_4.jpg]]
*Table 4: Detailed dataset configurations and task partitions used in our experiments.*

## 定位与知识库关联

本文方法属于持续学习中的正则化方法，具体定位如下：

- **基础方法**：EWC（Kirkpatrick et al., 2017）使用对角Fisher近似，本文改进为秩一Fisher近似。
- **重放策略**：生成式蒸馏（Masip et al., 2025）用于生成重放样本，本文与之结合。
- **理论支撑**：利用扩散模型低SNR区域的梯度结构（Vincent, 2011; Song et al., 2021b），与去噪自编码器的PCA-like行为（Vincent et al., 2010）相关。

**局限性**：
- 理论分析依赖于低SNR区域和模型收敛的假设，在训练初期或高SNR区域可能不完全成立。
- 秩一Fisher近似对扩散模型特有，可能不直接适用于其他生成模型架构（如标准VAE）。
- 实验仅在图像生成任务上验证，未涉及文本、音频等其他模态。
- ImageNet-1k使用32×32下采样版本，全分辨率下的性能尚待验证。
- 生成式蒸馏需要存储教师模型，增加了内存开销。

**开放问题**：
- 秩一Fisher近似在更大规模、更高分辨率的扩散模型上是否仍然有效？
- 该方法能否扩展到其他持续学习场景（如类增量分类、语义分割）？
- 如何理论证明跳跃连接使U-Net更倾向于在PCA-like子空间中操作？
- 是否可以将秩一Fisher近似与其他正则化方法（如SI、MAS）结合以获得更好效果？
- 在非扩散模型（如GAN、VAE）中，是否也存在类似的低秩Fisher结构？

## 原文 PDF

![[paperPDFs/ICLR_2026/Avoid_Catastrophic_Forgetting_with_Rank_1_Fisher_from_Diffusion_Models.pdf]]
