---
title: "Score-based Generative Modeling in Latent Space"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/Score_based_Generative_Modeling_in_Latent_Space.pdf
project_link: https://nvlabs.github.io/LSGM/
aliases:
- LSBGML
- SBGMLS
tags:
- NEURIPS_2021
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将SGM移至VAE的潜在空间，并通过混合分数参数化与重要性采样进行端到端训练，使模型仅需拟合编码分布与简单正态分布之间的残差，从而大幅简化反向SDE、加速采样，并借助编码器/解码器灵活处理非连续数据。"
primary_logic: "在VAE的潜在空间中训练SGM先验，配合混合正态-可学习分数函数与方差缩减技术，使生成模型能够同时获得高样本质量、快速采样和似然估计，并自然支持二值等离散数据。"
claims:
- "LSGM在CIFAR-10上取得最先进的FID分数2.10，优于当时所有生成模型。"
- "在CelebA-HQ-256上，采样速度比原始SGM提升两个数量级，但样本质量相当。"
- "混合分数参数化对端到端训练稳定性至关重要；未使用时模型极不稳定。"
- "推导出适用于LSGM的交叉熵定理(Theorem 1)，可仅基于去噪分数匹配优化编码分布，无需不可求解的边际分数。"
---

# Score-based Generative Modeling in Latent Space

> [!tip] 核心洞察
> 在VAE的潜在空间中训练SGM先验，配合混合正态-可学习分数函数与方差缩减技术，使生成模型能够同时获得高样本质量、快速采样和似然估计，并自然支持二值等离散数据。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 潜在空间分数生成模型 |
| 英文题名 | Score-based Generative Modeling in Latent Space |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2106.05931); [Project](https://nvlabs.github.io/LSGM); [Project](https://nvlabs.github.io/LSGM/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Latent Score-based Generative Model (LSGM) |
| Dataset | CIFAR-10, CelebA-HQ-256 |

> [!tip] 效果简介
> - CIFAR-10 上，FID (lower is better) 为 2.10，对比 previous state-of-the-art (e.g., DDPM 2.28)，变化 new state-of-the-art。
> - CIFAR-10 上，NELBO (bits/dim) 为 2.87，对比 previous likelihood-based models，变化 improved。
> - CelebA-HQ-256 上，FID 为 7.22，对比 7.23 (Original SGM, PC sampling)，变化 -0.01 (637× faster sampling)。

## 概述

**核心问题：** 直接在数据空间（像素级）应用分数生成模型（SGM）虽然生成质量高，但采样过程需要数千次网络评估，计算成本极高，且难以处理二值等非连续数据。

**核心方案：** 将SGM迁移至VAE的潜在空间中工作。通过编码器将数据压缩为低维潜在表示，在潜在空间内训练SGM先验，再通过解码器重建数据。这一设计配合三项关键技术——混合分数参数化、基于交叉熵定理的端到端训练、以及方差缩减策略——使模型仅需拟合编码分布与简单正态分布之间的残差，从而大幅简化反向SDE、加速采样，并借助编码器/解码器灵活处理离散数据。

**方法定位：** LSGM处于VAE与SGM的交叉地带。它以NVAE作为VAE骨干，以NCSN++构建潜在SGM先验，通过端到端联合训练将两者耦合，既保留了SGM的高样本质量，又获得了VAE的压缩效率和似然估计能力。

**主要结果：**
- 在CIFAR-10上取得FID 2.10，刷新当时所有生成模型的最高水平。
- 在CelebA-HQ-256上，采样速度比原始SGM提升约637倍（4.15秒 vs. 44.6分钟），样本质量相当（FID 7.22 vs. 7.23）。
- 在二值OMNIGLOT和MNIST上分别取得NELBO 87.79和78.47，均为当时最优似然。
- 消融实验证实：混合分数参数化对端到端训练稳定性至关重要，几何VPSDE与重要性采样显著降低了训练目标的方差。

## 背景与动机

生成模型的核心目标是学习数据分布 $p(\mathbf{x})$，使其既能生成高质量样本，又能提供精确的似然估计。近年来，基于分数的生成模型（Score-based Generative Models, SGMs）通过逐步向数据注入噪声并学习逆转该过程，在图像生成任务上取得了突破性进展。然而，这一范式面临一个根本性的效率瓶颈：**直接在数据空间（如像素空间）中执行扩散与去噪过程，导致采样阶段需要数千次网络评估，计算成本极高**。

具体而言，原始 SGM（Song et al.）在 CelebA-HQ-256 上生成一批 16 张图像需要约 45 分钟（4000 次函数评估），这严重限制了其在实际交互场景中的应用。此外，数据空间中的 SGM 天然适用于连续信号，难以直接处理二值图像等离散数据。

变分自编码器（VAE）通过将数据压缩到低维潜在空间，天然具备快速采样和处理离散数据的能力，但其样本质量长期落后于生成对抗网络（GAN）和 SGM。一个自然的思路是将 SGM 的强大建模能力与 VAE 的紧凑表示相结合——在潜在空间中训练 SGM 先验。然而，这一结合面临三个关键挑战：

1. **目标函数不可解**：潜在变量的边际分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t)$ 依赖于编码分布，无法直接计算。
2. **训练不稳定**：端到端联合训练编码器和 SGM 先验时，梯度方差极大，模型极易发散。
3. **先验-后验不匹配**：SGM 先验需要从纯噪声开始建模整个分布，而编码器输出的潜在分布已经接近标准正态分布，导致 SGM 需要拟合不必要的复杂映射。

本文提出的潜在空间分数生成模型（Latent Score-based Generative Model, LSGM）正是针对上述缺口，通过理论创新与工程设计的协同，首次实现了在 VAE 潜在空间中稳定、高效地训练 SGM 先验，并同时获得最先进的样本质量、似然估计和采样速度。

## 核心创新

### 瓶颈诊断：数据空间SGM的代价

分数生成模型（SGM）在数据空间直接工作时面临两个根本性瓶颈。其一，采样过程依赖反向扩散的数值求解，通常需要数千次网络评估（NFEs），计算成本极高——例如，在CelebA-HQ-256上，原始SGM的PC采样需约4000次评估，耗时45分钟。其二，SGM天然假设连续数据，难以直接处理二值图像等离散数据。这两个问题共同限制了SGM在大规模生成任务中的实用性。

### 因果杠杆：将SGM迁入潜在空间并端到端训练

LSGM的核心创新在于将SGM从高维数据空间迁移到VAE的低维潜在空间中运行。这一迁移通过因果杠杆发挥作用：在潜在空间中，SGM先验只需要拟合编码器分布 $q_\phi(\mathbf{z}_0|\mathbf{x})$ 与简单正态分布之间的**残差**，而非完整的数据分布。这使得反向SDE的路径被大幅简化，采样所需的函数评估次数急剧下降，同时编码器/解码器对为处理离散数据提供了天然的桥梁。

### 关键设计：混合分数参数化

潜在空间SGM面临一个训练稳定性挑战：若直接使用常规分数网络参数化先验，端到端训练极易崩溃。LSGM提出**混合分数参数化**（mixed score parameterization），将先验在扩散时间 $t$ 的分数函数构造为固定正态分量与可学习神经网络的几何混合：

$$p(\mathbf{z}_t) \propto \mathcal{N}(\mathbf{z}_t; 0, \mathbf{I})^{1-\alpha} \, p_\theta'(\mathbf{z}_t)^\alpha$$

对应的去噪函数为 $\epsilon_\theta(\mathbf{z}_t, t) = \sigma_t (1-\alpha) \odot \mathbf{z}_t + \alpha \odot \epsilon_\theta'(\mathbf{z}_t, t)$。这一设计使SGM网络 $\epsilon_\theta'$ 仅需学习编码分布与正态先验的偏差，从根本上稳定了端到端训练。消融实验表明，缺少混合分数时，小模型的FID从7.60崩溃至34.71，大模型则完全无法训练。

### 理论突破：交叉熵的去噪分数匹配定理

LSGM的变分上界包含编码分布与SGM先验之间的交叉熵项 $\mathrm{CE}(q_\phi(\mathbf{z}_0|\mathbf{x}) \| p_\theta(\mathbf{z}_0))$。常规KL上界（Eq. 4）依赖不可解析的边际分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t)$，无法直接优化。LSGM的核心理论贡献（Theorem 1）证明该交叉熵可严格表达为去噪分数匹配形式：

$$\mathrm{CE}(q(\mathbf{z}_0|\mathbf{x})\|p(\mathbf{z}_0)) = \mathbb{E}_{t \sim \mathcal{U}[0,1]} \left[ \frac{g(t)^2}{2} \mathbb{E}_{q(\mathbf{z}_t,\mathbf{z}_0|\mathbf{x})} \left[ \|\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0) - \nabla_{\mathbf{z}_t} \log p(\mathbf{z}_t)\|_2^2 \right] \right] + \frac{D}{2} \log(2\pi e \sigma_0^2)$$

这一结果将不可解的边际分数替换为可解析的条件分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0)$，使得编码器、解码器和SGM先验可以在统一目标下联合优化，无需分阶段训练。

### 方差缩减：几何VPSDE与重要性采样

深度LSGM的训练面临另一个挑战：扩散时间 $t$ 的均匀采样导致训练目标方差过大。LSGM从两个层面解决这一问题：

1. **几何VPSDE**：设计新的方差保持SDE，使 $\frac{d}{dt} \log \sigma_t^2$ 在 $t \in [0,1]$ 上为常数，从而均匀化不同时间步的损失贡献。其漂移系数为 $\beta(t) = \log(\sigma_{\max}^2 / \sigma_{\min}^2) \frac{\sigma_t^2}{1-\sigma_t^2}$，其中 $\sigma_t^2 = \sigma_{\min}^2 (\sigma_{\max}^2 / \sigma_{\min}^2)^t$。

2. **重要性采样**：针对最大似然加权目标，解析推导最优建议分布 $r(t) \propto \frac{1}{\sigma_t^2} \frac{d\sigma_t^2}{dt}$，通过重参数化 $t = \mathrm{var}^{-1}((\sigma_1^2)^\rho (\sigma_\epsilon^2)^{1-\rho})$ 实现高效采样。

实验验证（Figure 2）表明，几何VPSDE与重要性采样的组合显著降低了训练目标的Monte Carlo方差，是深度LSGM稳定训练的必要条件。

### Changed Slots 总结

| 设计维度 | 基线方案 | LSGM方案 |
|---------|---------|---------|
| 运行空间 | 数据空间（像素） | VAE潜在空间 |
| 先验形式 | 数据空间SGM | 潜在空间SGM + 混合正态分量 |
| 分数匹配目标 | 依赖边际分数 | 基于交叉熵的去噪分数匹配（Theorem 1） |
| 时间采样 | 均匀采样 $t \sim \mathcal{U}[0,1]$ | 几何VPSDE + 重要性采样 |
| 训练策略 | 分阶段/固定VAE | 端到端联合训练 |

## 整体框架

LSGM 将分数生成模型（SGM）从数据空间迁移至 VAE 的潜在空间，构建了一个由三个核心模块组成的端到端生成框架：编码器 $q_\phi(\mathbf{z}_0|\mathbf{x})$、SGM 先验 $p_\theta(\mathbf{z}_0)$ 和解码器 $p_\psi(\mathbf{x}|\mathbf{z}_0)$（Fig. 1）。

**生成流程**分为两个阶段。在**前向编码阶段**，输入数据 $\mathbf{x}$ 通过编码器映射为潜在表示 $\mathbf{z}_0$。在**生成阶段**，模型从 SGM 先验中采样潜在变量，再经解码器重建为数据空间样本。具体而言，采样从基础分布 $p(\mathbf{z}_1)$（通常为标准正态分布）出发，通过数值求解反向 SDE 或概率流 ODE，逐步去噪得到 $\mathbf{z}_0$，最后经解码器生成 $\mathbf{x}$。

**训练流程**则围绕变分上界展开。整体目标函数为：

$$\mathcal{L}(\mathbf{x}, \phi, \theta, \psi) = \mathbb{E}_{q_\phi(\mathbf{z}_0|\mathbf{x})} \left[ -\log p_\psi(\mathbf{x}|\mathbf{z}_0) \right] + \mathbb{E}_{q_\phi(\mathbf{z}_0|\mathbf{x})} \left[ \log q_\phi(\mathbf{z}_0|\mathbf{x}) \right] + \mathbb{E}_{q_\phi(\mathbf{z}_0|\mathbf{x})} \left[ -\log p_\theta(\mathbf{z}_0) \right]$$

该目标由三项构成：**重建损失**（解码器）、**编码器熵**（正则化项）以及编码分布与 SGM 先验之间的**交叉熵**。其中，交叉熵项是连接 VAE 与 SGM 的关键桥梁——它通过 Theorem 1 被转化为可在潜在空间中独立优化的去噪分数匹配目标，从而避免了直接计算难以求解的边际分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t)$。

**模块间的数据流**如下：编码器输出 $\mathbf{z}_0$ 后，正向扩散过程根据选定的 SDE（如 VPSDE 或几何 VPSDE）向 $\mathbf{z}_0$ 注入噪声，生成不同时间步的 $\mathbf{z}_t$。混合分数网络 $\epsilon_\theta(\mathbf{z}_t, t)$ 接收 $\mathbf{z}_t$ 和时间 $t$，预测去噪方向，其输出与固定正态分量线性混合后构成最终的分数估计。训练时，编码器和解码器使用最大似然加权 $w_{\text{ll}}$ 联合优化（Eq. 8），SGM 先验则可采用非加权 $w_{\text{un}}$ 或重加权 $w_{\text{re}}$ 单独训练以获得更优的生成质量（Eq. 9）。端到端联合训练被证明显著优于分阶段训练（FID 5.19 vs. 9.00），而混合分数参数化对训练稳定性至关重要——缺少该设计时，小模型的 FID 从 7.60 崩溃至 34.71。

为降低训练目标的蒙特卡洛方差，LSGM 引入了两项关键设计：**几何 VPSDE** 使 $\mathrm{d}\log \sigma_t^2/\mathrm{d}t$ 在 $t \in [0,1]$ 上保持恒定，以及针对最大似然目标的**重要性采样**建议分布 $r(t)$。两者结合显著降低了训练方差（Fig. 2），使得深层 LSGM 的稳定训练成为可能。

## 核心模块与公式推导

### 整体框架与变分上界

LSGM 由三个核心模块串联构成：编码器 $q_{\phi}(\mathbf{z}_0|\mathbf{x})$、潜在空间 SGM 先验 $p_{\theta}(\mathbf{z}_0)$ 和解码器 $p_{\psi}(\mathbf{x}|\mathbf{z}_0)$（Fig. 1）。训练目标是最小化负对数似然 $-\log p(\mathbf{x})$ 的变分上界，其分解形式为：

$$\mathcal{L}(\mathbf{x}, \phi, \theta, \psi) = \mathbb{E}_{q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ -\log p_{\psi}(\mathbf{x}|\mathbf{z}_0) \right] + \mathbb{E}_{q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ \log q_{\phi}(\mathbf{z}_0|\mathbf{x}) \right] + \mathbb{E}_{q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ -\log p_{\theta}(\mathbf{z}_0) \right]$$

三项依次对应重建损失、编码器熵和编码分布与 SGM 先验之间的交叉熵。其中交叉熵项是端到端训练的关键——它同时连接编码器和 SGM 先验，迫使编码分布向可学习的扩散先验靠拢。

### 交叉熵的去噪分数匹配定理（Theorem 1）

直接优化上述交叉熵面临一个根本困难：SGM 的分数匹配目标需要编码分布的边际分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t)$，但对于非正态的编码分布（如基于 Normalizing flow 的编码器），该边际分数没有解析形式。Theorem 1 解决了这一问题：

$$\mathrm{CE}(q(\mathbf{z}_0|\mathbf{x}) \parallel p(\mathbf{z}_0)) = \mathbb{E}_{t \sim \mathcal{U}[0,1]} \left[ \frac{g(t)^2}{2} \mathbb{E}_{q(\mathbf{z}_t,\mathbf{z}_0|\mathbf{x})} \left[ \parallel \nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0) - \nabla_{\mathbf{z}_t} \log p(\mathbf{z}_t) \parallel_2^2 \right] \right] + \frac{D}{2} \log(2\pi e \sigma_0^2)$$

定理的核心价值在于将交叉熵转化为仅依赖**条件分数** $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0)$ 的去噪分数匹配目标。对于高斯前向扩散过程 $q(\mathbf{z}_t|\mathbf{z}_0) = \mathcal{N}(\mathbf{z}_t; \mu_t(\mathbf{z}_0), \sigma_t^2 \mathbf{I})$，该条件分数有闭式解 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0) = -(\mathbf{z}_t - \mu_t(\mathbf{z}_0)) / \sigma_t^2$，从而绕开了不可求解的边际分数。常数项 $\frac{D}{2} \log(2\pi e \sigma_0^2)$ 与模型参数无关，优化时可忽略。

### 混合分数参数化

直接在潜在空间中训练 SGM 先验存在严重的训练不稳定问题。LSGM 的解决方案是将先验构造为标准正态分布与可学习 SGM 的几何混合：

$$p(\mathbf{z}_t) \propto \mathcal{N}(\mathbf{z}_t; \mathbf{0}, \mathbf{I})^{1-\alpha} \, p'_{\theta}(\mathbf{z}_t)^{\alpha}$$

对应的分数函数为 $\nabla_{\mathbf{z}_t} \log p(\mathbf{z}_t) = -(1-\alpha) \odot \mathbf{z}_t + \alpha \odot \nabla_{\mathbf{z}_t} \log p'_{\theta}(\mathbf{z}_t)$。在去噪分数匹配框架下，这等价于引入一个混合噪声预测网络：

$$\epsilon_{\theta}(\mathbf{z}_t, t) := \sigma_t (1-\alpha) \odot \mathbf{z}_t + \alpha \odot \epsilon'_{\theta}(\mathbf{z}_t, t)$$

其中 $\epsilon'_{\theta}$ 是实际需要训练的神经网络，$\alpha \in [0,1]^D$ 控制每个维度上可学习分量与固定正态分量的混合比例。该参数化使 SGM 先验只需建模编码分布与标准正态之间的**残差**，大幅降低了学习难度。消融实验表明，不使用混合分数时，小模型的 FID 从 7.60 崩溃至 34.71，验证了其对训练稳定性的决定性作用。

### 端到端训练目标

将混合分数代入交叉熵表达式，得到可端到端优化的训练目标。对于 VAE 的编码器和解码器，采用最大似然加权 $w_{\mathrm{ll}}(t) = g(t)^2$：

$$\min_{\phi,\psi} \mathbb{E}_{q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ -\log p_{\psi}(\mathbf{x}|\mathbf{z}_0) + \log q_{\phi}(\mathbf{z}_0|\mathbf{x}) \right] + \mathbb{E}_{t, \epsilon, q(\mathbf{z}_t|\mathbf{z}_0), q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ \frac{w_{\mathrm{ll}}(t)}{2} \parallel \epsilon - \epsilon_{\theta}(\mathbf{z}_t, t) \parallel_2^2 \right]$$

SGM 先验则可独立采用不同加权策略训练：

$$\min_{\theta} \mathbb{E}_{t, \epsilon, q(\mathbf{z}_t|\mathbf{z}_0), q_{\phi}(\mathbf{z}_0|\mathbf{x})} \left[ \frac{w(t)}{2} \parallel \epsilon - \epsilon_{\theta}(\mathbf{z}_t, t) \parallel_2^2 \right]$$

其中 $w(t)$ 可选三种机制（Table 1）：最大似然加权 $w_{\mathrm{ll}}$（优化 NELBO）、非加权 $w_{\mathrm{un}}$（优化样本质量）和重加权 $w_{\mathrm{re}}$。消融实验表明，$w_{\mathrm{un}}$ 或 $w_{\mathrm{re}}$ 倾向于获得更低的 FID，而 $w_{\mathrm{ll}}$ 配合几何 VPSDE 获得最优似然。

### 方差缩减：几何 VPSDE 与重要性采样

训练目标的 Monte Carlo 估计方差过大是深度 LSGM 训练不稳定的另一瓶颈。论文从两个层面进行方差缩减：

**几何 VPSDE** 通过设计漂移系数使 $\frac{d}{dt} \log \sigma_t^2$ 在 $t \in [0,1]$ 上为常数：

$$\beta(t) = \log\left(\frac{\sigma_{\max}^2}{\sigma_{\min}^2}\right) \frac{\sigma_t^2}{1 - \sigma_t^2}, \quad \sigma_t^2 = \sigma_{\min}^2 \left(\frac{\sigma_{\max}^2}{\sigma_{\min}^2}\right)^t$$

这使得不同时间步的损失贡献更加均匀，避免原始 VPSDE 在 $t$ 接近 0 或 1 时方差急剧膨胀（Fig. 2）。

**重要性采样** 针对最大似然加权目标，推导出理论最优的建议分布 $r(t)$：

$$r(t) = \frac{1}{\log \sigma_1^2 - \log \sigma_{\epsilon}^2} \cdot \frac{1}{\sigma_t^2} \cdot \frac{d\sigma_t^2}{dt}$$

该分布通过逆变换采样实现：$t = \mathrm{var}^{-1}\left((\sigma_1^2)^{\rho} (\sigma_{\epsilon}^2)^{1-\rho}\right)$，其中 $\rho \sim \mathcal{U}[0,1]$。Fig. 2 定量验证了两种技术组合使用时可显著降低训练目标方差，是深度 LSGM 稳定训练的必要条件——缺少重要性采样时大型模型变得不稳定。

## 实验与分析

### 主要生成结果

LSGM 在多个标准基准上同时实现了当时最优的样本质量与似然估计，并在采样效率上展现出数量级的优势。

**CIFAR-10 自然图像生成。** LSGM 在该数据集上取得 FID 2.10，刷新了当时所有生成模型的纪录（此前最优为 DDPM 的 2.28）。在似然方面，LSGM 同样获得 NELBO 2.87 bits/dim，优于此前基于似然的模型。这些结果来自 Table 2，原文在 Abstract 中将其定位为“state-of-the-art”。

**CelebA-HQ-256 高分辨率人脸生成。** LSGM 以 FID 7.22 与原始 SGM（PC 采样，FID 7.23）持平，但采样速度提升约 **637 倍**：LSGM 仅需 23 次函数评估（NFEs）、4.15 秒即可生成一批 16 张图像，而原始 SGM 需要 4000 NFEs、耗时 44.6 分钟。Figure 4 绘制了 FID 随 NFE 变化的权衡曲线，直观展示了 LSGM 在极低 NFE 下仍能保持竞争力的样本质量。

**二值离散数据。** 在动态二值化 OMNIGLOT 上，LSGM 取得 NELBO 87.79 nats；在动态二值化 MNIST 上取得 NELBO 78.47 nats，均达到当时最优似然水平（Table 4、Table 5）。这验证了 VAE 框架赋予 LSGM 处理非连续数据的天然灵活性。

### 消融实验与关键设计选择

Table 6 系统消融了 SDE 类型、训练目标、加权机制与方差缩减技术的影响，揭示了以下因果链：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/011_Table_6.jpg]]
*Table 6: Ablations on SDEs, objectives, weighting mechanisms, and variance reduction. Details in App. G*

**SDE 选择：几何 VPSDE 对似然最优。** 在 VPSDE、Sub-VPSDE 与几何 VPSDE 的对比中，几何 VPSDE 配合最大似然加权（w_ll）获得最佳 NELBO。其核心机制是使 d log σ_t²/dt 为常数，从而降低时间采样的方差（Sec. 3.4）。Figure 2 定量验证了该设计对训练目标方差的显著压缩效果。

**加权策略决定优化偏好。** 非加权（w_un）或重加权（w_re）训练 SGM 先验倾向于获得更低的 FID，而最大似然加权（w_ll）则优化 NELBO。这一发现表明，通过切换加权函数，同一 LSGM 架构可在样本质量与似然之间灵活权衡。

**端到端联合训练不可替代。** 冻结 VAE 仅训练 SGM 先验时，FID 从 5.19 急剧恶化至 9.00（Sec. 5.2）。这表明编码分布与先验的协同适配对生成质量至关重要，分阶段训练无法弥补两者间的失配。

**混合分数参数化是稳定性的必要条件。** 在小模型实验中，不使用混合分数时 FID 从 7.60 崩溃至 34.71（Sec. 5.2）。原文明确指出：“We generally found training LSGM without our proposed 'mixed score' formulation to be unstable during end-to-end training.” 混合分数通过将固定正态分量与可学习神经网络输出按元素线性组合，使 SGM 仅需拟合编码分布与正态分布间的残差，大幅降低了端到端训练的优化难度。

**重要性采样对大规模模型不可或缺。** 附录 G.5.1 指出，缺少重要性采样时大型 LSGM 变得不稳定。Figure 3 展示了针对不同加权函数解析推导的最优建议分布 r(t)，这些分布能有效降低 Monte Carlo 估计的方差。

### 失败模式与局限性

尽管 LSGM 取得了显著进展，原文揭示了若干需要关注的问题：

1. **采样仍需百次以上网络评估。** 虽较原始 SGM 加速两个数量级，但距离单步生成仍有差距，限制了交互式应用场景。

2. **训练资源消耗巨大。** 主要模型训练累计约 350,000 GPU 小时，能耗成本高昂。

3. **对 SDE 与加权选择敏感。** VESDE 等部分 SDE 变体存在训练不稳定性，模型性能依赖于 SDE 类型与加权函数的恰当组合。

4. **架构依赖性。** 在大型 VAE 骨架上若不使用混合分数参数化则训练不稳定，方法对底层 VAE 架构有一定依赖。

5. **数据模态覆盖有限。** 当前验证仅限自然图像与简单二值数据集，向音频、图结构等模态的推广有待探索。

### 重要图表结论

- **Figure 1**：LSGM 整体架构，由编码器 q_φ(z₀|x)、潜在空间 SGM 先验 p_θ(z₀) 和解码器 p_ψ(x|z₀) 组成，数据经编码进入低维潜在空间后执行扩散与去噪过程。
- **Table 2 & Table 3**：CIFAR-10 与 CelebA-HQ-256 上的全面生成性能对比，确立 LSGM 在样本质量与似然上的双重优势。
- **Figure 4**：FID-NFE 权衡曲线，LSGM 在极低函数评估次数下仍接近原始 SGM 的样本质量，验证了潜在空间扩散的采样效率优势。
- **Table 6**：消融实验核心表格，量化了 SDE 选择、加权策略与方差缩减技术对 NELBO 和 FID 的独立贡献。
- **Figure 2 & Figure 6**：分别验证几何 VPSDE 与重要性采样对训练目标方差的缩减效果，为方法设计提供实证支撑。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/025_Figure.jpg]]
*Figure: (a) Evolution of latent variables under the SDE (b) Evolution of latent variables under the SDE (c) Evolution of latent variables under the ODE*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/005_Table_2.jpg]]
*Table 2: Generative performance on CIFAR-10*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/006_Table_3.jpg]]
*Table 3: Generative results on CelebA-HQ-256*

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/019_Figure_9.jpg]]
*Figure 9: The effect of ODE solver error tolerance on the quality of samples. In contrast to the original SGM [2] where high error tolerance results in pixelated images (see Fig. 3 in [2]), in our case high error tolerances create low-frequency artifacts. Reducing the error tolerance improves subtle details slightly*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/010_Figure_5.jpg]]
*Figure 5: Generated samples for different datasets. For binary datasets, we visualize the decoder mean. LSGM successfully generates sharp, high-quality, and diverse samples (additional samples in appendix)*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/002_Table.jpg]]

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/008_Table_4.jpg]]
*Table 4: Dyn. binarized OMNIGLOT results*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/009_Table_5.jpg]]
*Table 5: Dynamically binarized MNIST results*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/013_Table_7.jpg]]
*Table 7: Hyperparameters for our main models. We use the same notations and abbreviations as in Tab. 6 in main paper*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/014_Table_8.jpg]]
*Table 8: Experiment with a small VAE architecture on dynamically binarized MNIST*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2106_05931/figures/015_Table_9.jpg]]
*Table 9: Number of function evaluations (NFE) of ODE solver during probability flow-based latent SGM prior sampling and corresponding sampling time for our main CIFAR-10 models. Sampling was done in batches of size 16 using a single Titan V GPU. Results are averaged over 20 sampling runs. See Tab. 2 in main text for generative performance metrics*

## 方法谱系与知识库定位

### 方法关系图谱：从数据空间SGM到潜在空间生成

LSGM 的方法谱系根植于两条主线的交汇：**分数生成模型（SGM）** 与**变分自编码器（VAE）**。理解 LSGM 的创新，需要首先审视其试图解决的核心瓶颈——直接在数据空间应用 SGM 所导致的高昂计算代价与对非连续数据的适配困难。

**上游基线：数据空间 SGM 的成就与代价。** LSGM 直接继承自 Song 等人提出的原始 SGM 框架（NCSN++ 骨干），该框架通过逐步注入噪声并学习去噪分数函数来建模数据分布。原始 SGM 在 CelebA-HQ-256 等任务上取得了当时领先的样本质量（FID 7.23），但其采样过程需要数千次网络评估（例如预测器-校正器采样约需 4000 次函数评估，耗时约 45 分钟/批），这成为其实用化的根本障碍。LSGM 的核心因果干预在于将 SGM 的运行空间从数据空间迁移至 VAE 的潜在空间，从而将高维像素级的扩散过程压缩为低维潜在表示的扩散过程，直接降低了单次函数评估的计算量，并大幅减少了收敛所需的扩散步数。

**VAE 骨干：NVAE 的架构继承与角色转变。** LSGM 的编码器-解码器架构基于 **NVAE**（Vahdat & Kautz），这是一个层次化 VAE，本身已具备较强的生成能力。在 LSGM 框架中，NVAE 的角色发生了根本性转变：它不再依赖简单的正态先验，而是作为一个可微分的特征提取器，将数据映射到适合 SGM 建模的连续潜在空间。这一设计使得 LSGM 天然继承了 VAE 处理离散数据的能力——编码器将二值图像映射为连续潜在变量，SGM 先验在连续空间建模，解码器再将采样结果映射回离散观测空间，从而无需像原始 SGM 那样对离散数据做特殊处理。

**下游影响与定位。** LSGM 发表于 2021 年，处于扩散模型从数据空间向潜在空间迁移的关键转折点。其后续影响力体现在两个方向上：一是潜在扩散模型（Latent Diffusion Models, LDM）的兴起，LDM 同样采用 VAE 潜在空间进行扩散，但使用了不同的训练目标和条件机制；二是对 SGM 训练理论的贡献——LSGM 首次系统性地建立了 VAE 编码分布与 SGM 先验之间交叉熵的去噪分数匹配等价关系（Theorem 1），为端到端训练潜在扩散模型提供了理论支撑。

### 关键技术贡献的因果机制

LSGM 的方法创新并非简单的模块拼接，而是围绕一个核心因果链条展开：**如何让 SGM 先验与 VAE 编码器在端到端训练中稳定协同**。这一链条上的每个技术组件都解决了一个具体的失败模式。

**交叉熵定理（Theorem 1）：移除边际分数障碍。** 端到端训练的第一个理论障碍在于，VAE 的变分下界需要计算编码分布 $q_\phi(\mathbf{z}_0|\mathbf{x})$ 与 SGM 先验 $p_\theta(\mathbf{z}_0)$ 之间的交叉熵。直接使用标准去噪分数匹配需要编码分布的边际分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t)$，这在编码器为复杂神经网络时无法解析求解。Theorem 1 证明了交叉熵可以等价地表示为仅依赖条件分数 $\nabla_{\mathbf{z}_t} \log q(\mathbf{z}_t|\mathbf{z}_0)$ 的期望形式，加上一个与模型无关的常数项。这一等价性使得编码器分布与先验的匹配可以完全通过可计算的条件分数来完成，是端到端训练的基石。

**混合分数参数化：稳定训练的必需设计。** 即使有了 Theorem 1，直接让神经网络学习完整的去噪函数在实践中被证明极不稳定——消融实验显示，小型 LSGM 的 FID 会从 7.60 崩溃至 34.71。混合分数参数化通过将先验建模为标准正态分布与可学习残差的几何混合 $p(\mathbf{z}_t) \propto \mathcal{N}(\mathbf{z}_t; 0, \mathbf{I})^{1-\alpha} p_\theta'(\mathbf{z}_t)^\alpha$，使得 SGM 网络 $\epsilon_\theta'$ 只需拟合编码分布与正态分布之间的“残差”，而非完整的分数函数。最终的分数估计为 $\epsilon_\theta(\mathbf{z}_t, t) = \sigma_t (1-\alpha) \odot \mathbf{z}_t + \alpha \odot \epsilon_\theta'(\mathbf{z}_t, t)$。这一设计显著降低了学习难度，因为正态分量提供了稳定的基础信号。

**方差缩减体系：几何 VPSDE 与重要性采样。** 端到端训练的另一个失败模式来自训练目标的蒙特卡洛估计方差过大。LSGM 从两个层面进行方差控制：(1) 设计几何 VPSDE，使得 $\frac{d}{dt} \log \sigma_t^2$ 在 $t \in [0,1]$ 上为常数，从而避免原始 VPSDE 在扩散早期和末期方差剧烈变化的问题；(2) 针对最大似然加权 $w_\text{ll}(t)$，推导出理论最优的重要性采样分布 $r(t)$，将采样集中于对训练目标贡献最大的时间区间。Figure 2 的实验证实，这两种技术组合可将训练目标方差降低一个数量级以上，是训练深层 LSGM 的必要条件。

### 适用边界与局限

尽管 LSGM 在多个基准上取得了显著成果，其方法存在明确的适用边界：

**采样速度的下限。** 虽然 LSGM 将 CelebA-HQ-256 的采样时间从 45 分钟降至 4.15 秒（约 637 倍加速），但其采样仍需要 23-138 次网络评估（取决于 ODE 求解器公差），远未达到单步生成或实时交互的要求。这一局限根植于扩散模型的本质——反向过程需要逐步去噪，LSGM 通过压缩空间维度降低了单步成本，但未改变扩散步数的根本需求。

**训练资源的高消耗。** 原文报告 LSGM 的训练消耗约 350,000 GPU 小时，这一成本远超同期许多生成模型。高消耗主要来自三个方面：端到端训练需要同时优化编码器、解码器和 SGM 先验；SGM 先验的训练需要对多个噪声水平进行采样；大型 VAE 骨干（如 NVAE）本身就需要大量计算。这使得 LSGM 的直接复现和应用受到计算资源的强约束。

**对 SDE 类型与加权的敏感性。** 消融实验（Table 6）揭示了 LSGM 性能对 SDE 选择和训练加权的显著依赖：几何 VPSDE 在似然指标（NELBO）上最优，但 VESDE 在某些 FID 指标上可能更好；最大似然加权 $w_\text{ll}$ 有利于 NELBO，而非加权 $w_\text{un}$ 或重加权 $w_\text{re}$ 有利于 FID。此外，部分 SDE 变体（如 VESDE）存在训练不稳定性。这种敏感性意味着在实际部署中需要针对具体指标进行 SDE 和加权的调优。

**对 VAE 架构的依赖性。** 混合分数参数化对于大型 VAE 骨干的稳定训练至关重要，但该方法是否适用于其他类型的编码器架构（如 VQ-VAE、离散潜在空间）尚未验证。LSGM 的成功部分依赖于 NVAE 提供的层次化潜在表示，将其迁移到其他 VAE 架构可能需要重新设计分数参数化策略。

**数据模态的验证范围有限。** 当前实验覆盖自然图像（CIFAR-10、CelebA-HQ-256）和二值图像（MNIST、OMNIGLOT），但在文本、音频、图结构数据等模态上的适用性尚待探索。潜在空间 SGM 的核心假设——数据可以压缩到低维连续潜在空间——在这些模态上可能面临不同的挑战。

### 开放问题

LSGM 开启的研究方向仍存在若干待解决的关键问题：

**如何进一步加速潜在空间扩散？** 当前 LSGM 的采样仍需百次级别的网络评估。可能的路径包括：为潜在空间扩散设计专用的轻量级反向求解器，利用潜在空间的低维特性减少步数；通过知识蒸馏将多步扩散过程压缩为单步或几步生成；或探索潜在空间中的常微分方程（概率流 ODE）的高阶求解策略。

**混合分数系数 $\alpha$ 的自适应策略。** 当前 $\alpha$ 是预定义的固定系数，其取值对训练稳定性和最终性能有直接影响。是否可以通过元学习或自适应机制在训练过程中动态调整 $\alpha$，以平衡正态先验的稳定性和可学习残差的表达能力，是一个开放的理论问题。

**向更高维度和更复杂数据的扩展。** 在视频生成、3D 内容生成等高维任务中，潜在空间的设计（维度、层次结构）与 SGM 先验的训练策略应如何调整？潜在空间的压缩率与生成质量之间的权衡曲线在更复杂的数据上会如何变化？

**与其他生成范式的深度融合。** LSGM 建立了 VAE 与 SGM 的紧密耦合，但尚未探索与 GAN 判别器、自回归先验或流模型的进一步结合。例如，是否可以在潜在空间中加入判别器来提升样本的感知质量，同时保持似然估计的能力？

## 原文 PDF

![[paperPDFs/NEURIPS_2021/Score_based_Generative_Modeling_in_Latent_Space.pdf]]
