---
title: "Tackling the Generative Learning Trilemma with Denoising Diffusion GANs"
type: paper
paper_level: A
venue: ICLR
year: 2022
pdf_ref: paperPDFs/ICLR_2022/Tackling_the_Generative_Learning_Trilemma_with_Denoising_Diffusion_GANs.pdf
project_link: https://nvlabs.github.io/denoising-diffusion-gan/
aliases:
- DDG
- TGLTDDG
tags:
- ICLR_2022
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将去噪分布从简单高斯替换为表达能力更强的多模态分布（由条件 GAN 建模），从而允许使用大步长、极少的去噪步数，大幅提升采样速度。"
primary_logic: "当扩散步长较大且数据分布非高斯时，真实去噪分布变得复杂且多模态；因此采用条件 GAN 灵活建模每步的多模态条件分布，仅用 4 步即可生成高质量、高多样性的样本，同时实现约 2000 倍加速。"
claims:
- "在 CIFAR-10 上，Denoising Diffusion GAN (T=4) 仅需 4 次网络推理，生成 100 张图像耗时 0.21 秒，较 Score SDE 加速约 2000 倍，FID 为 3.75，Recall 为 0.57。"
- "当扩散步长增大时，真实去噪分布明显偏离高斯，呈现多模态特性。"
- "消融实验表明，移除隐变量 z 使去噪分布退化为单模态，FID 从 3.75 骤升至 20.6。"
- "在 StackedMNIST 上，本文模型覆盖全部 1000 个模式，KL 散度仅 0.071，显著优于 GAN 基线。"
---

# Tackling the Generative Learning Trilemma with Denoising Diffusion GANs

> [!tip] 核心洞察
> 当扩散步长较大且数据分布非高斯时，真实去噪分布变得复杂且多模态；因此采用条件 GAN 灵活建模每步的多模态条件分布，仅用 4 步即可生成高质量、高多样性的样本，同时实现约 2000 倍加速。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用去噪扩散生成对抗网络解决生成式学习三难问题 |
| 英文题名 | Tackling the Generative Learning Trilemma with Denoising Diffusion GANs |
| 会议/期刊 | ICLR 2022 |
| Links | [paper](https://arxiv.org/abs/2112.07804); [Project](https://nvlabs.github.io/denoising-diffusion-gan); [Project](https://nvlabs.github.io/denoising-diffusion-gan/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Denoising Diffusion GANs |
| Dataset | CIFAR-10 (unconditional), CIFAR-10 |

> [!tip] 效果简介
> - CIFAR-10 (unconditional) 上，FID↓ 为 3.75，对比 3.21 (DDPM)，变化 +0.54 (略高但接近)。
> - CIFAR-10 上，Recall↑ 为 0.57，对比 0.57 (DDPM)，变化 持平。
> - CIFAR-10 上，NFE↓ 为 4，对比 1000 (DDPM)，变化 减少 996 步。

## 概述

**生成式学习三难问题**：传统生成模型长期面临**采样速度、样本质量与模式覆盖**三者难以兼得的困境。扩散模型（如 DDPM、Score SDE）虽能生成高质量、高多样性的样本，但其采样过程需要成百上千次网络推理，速度极慢；生成对抗网络（GAN）虽能单步快速采样，却常因模式坍塌而牺牲多样性。这一“三难”构成了生成式学习的核心瓶颈。

**根本原因**：本文指出，扩散模型采样慢的根源在于**去噪步骤中采用高斯分布假设**（见 Figure 2）。该假设仅在相邻扩散步长极小时成立，因此传统方法必须将去噪过程拆分为大量小步长步骤（典型值 T=1000），导致采样效率低下。当步长增大、数据分布非高斯时，真实的去噪分布会变得**复杂且多模态**，高斯假设随之失效。

**核心方案**：**Denoising Diffusion GANs** 将扩散模型的去噪分布从简单高斯替换为由**条件 GAN 建模的多模态分布**。通过引入隐变量 $z$，每步的条件生成器能灵活捕捉大步长下真实去噪分布的复杂形态，从而将去噪步数从 1000 步骤降至 **4 步**，实现约 **2000 倍采样加速**，同时保持与扩散模型相当的样本质量和模式覆盖能力。

**方法定位**：该方法位于扩散模型与生成对抗网络的交叉地带。它保留了扩散模型的逐步去噪框架，但用对抗训练替代了原有的 KL 散度最小化，以软化逆 KL 散度匹配多模态条件分布。在方法谱系中，它区别于 **DDPM**（纯高斯去噪）、**Score SDE**（连续时间分数匹配）、**StyleGAN2 w/ ADA**（单步 GAN）以及 **FastDDPM**（非马尔可夫缩短步数），通过**多模态去噪分布**这一关键设计同时逼近三难问题的三个顶点。

**主要实证结果**：

| 基准 | 核心指标 | 本文 (T=4) | 对比基线 | 关键提升 |
|------|----------|------------|----------|----------|
| CIFAR-10 | FID / Recall / 推理步数 | 3.75 / 0.57 / 4 | DDPM: 3.21 / 0.57 / 1000 | 步数减少 996 步，质量接近 |
| CIFAR-10 | 采样时间 (100 张) | 0.21 秒 | Score SDE: 423.2 秒 | 约 2000× 加速 |
| StackedMNIST | 模式覆盖 (KL 散度) | 0.071 (覆盖全部 1000 个模式) | StyleGAN2 w/ ADA: 0.253 | 多样性显著优于 GAN 基线 |
| CelebA-HQ 256 | FID | 7.64 | DDPM: 7.16 | 接近扩散模型质量 |
| LSUN Church 256 | FID | 5.25 | ImageBART: 6.24 | 优于基线 |

消融实验进一步证实：移除隐变量 $z$ 使去噪分布退化为单模态，FID 从 3.75 骤升至 20.6；将扩散仅作为数据增强训练单步 GAN 的 FID 为 14.8，远逊于本文的 4 步方案。这些结果表明，**多模态去噪分布**是实现大步长高质量采样的关键因果机制。

**局限与展望**：在 CIFAR-10 上的 FID (3.75) 仍略低于最优扩散模型（Score SDE 的 2.20），保真度存在提升空间；训练计算成本较高（CIFAR-10 约 48 GPU 小时）；当前架构在 T 增大时性能下降，扩展性有待验证。未来方向包括进一步减少步数、设计更高效的条件生成器，以及将该思路推广至潜在扩散模型。

## 背景与动机

### 生成式学习的三难困境

深度生成模型领域长期面临一个根本性的权衡，本文将其概括为**生成式学习三难困境**（Figure 1）：现有方法难以同时实现高质量的样本生成、快速的采样速度以及充分的模式覆盖（多样性）。GAN 类方法通常具备快速采样的优势，但容易遭受模式坍塌，导致多样性不足；而基于似然的模型（如 VAE）和扩散模型虽然能够较好地覆盖数据分布的模式，却以高昂的采样计算成本为代价。

扩散模型近年来在图像生成质量上取得了突破性进展，但其**采样速度极慢**是制约实际应用的核心瓶颈。典型的去噪扩散概率模型（DDPM）需要数百至上千次网络推理才能生成一张图像，在 CIFAR-10 上生成 100 张图像耗时超过 400 秒（Table 1）。已有加速工作主要从两个方向入手：一是设计更快的数值求解器以缩短采样轨迹，二是在潜在空间中训练扩散模型以降低每步计算量。然而，这些方法本质上仍受限于扩散模型的一个核心假设——**去噪分布的高斯假设**。

### 瓶颈诊断：高斯假设与大步长去噪的矛盾

扩散模型的慢采样本质上源于其去噪步骤中对条件分布 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 的**高斯分布假设**。在标准扩散模型框架中，前向过程按预定义的方差调度 $\beta_t$ 逐步添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

反向去噪过程则被参数化为一个具有可训练均值 $\mu_\theta$ 和固定方差的高斯分布。这一高斯假设的合理性依赖于两个条件：**去噪步长足够小**，或**数据分布本身为高斯分布**。当步长很小时（如 $T=1000$），真实去噪分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 确实近似于高斯分布，因此高斯假设成立。但这迫使模型必须采用大量去噪步数，导致采样速度极慢。

**核心瓶颈在于**：当去噪步长增大、且数据分布非高斯时，真实去噪分布会变得**复杂且多模态**，高斯假设不再成立。Figure 2 通过一维数据分布的可视化清晰地展示了这一现象：对于较小的步长，真实去噪分布 $q(\mathbf{x}_4|\mathbf{x}_5=X)$ 接近高斯分布；但随着步长增大，该分布明显偏离高斯形态，呈现出多模态特性。这意味着，若要实现大步长、少步数的快速采样，就必须放弃高斯假设，转而采用**表达能力更强的多模态分布**来建模去噪分布。

### 本文动机与核心思路

基于上述诊断，本文提出一个直接而深刻的解决方案：**用条件生成对抗网络（GAN）灵活建模每步的多模态去噪分布**，从而允许使用大步长（$T \le 8$）、极少去噪步数（实验最优为 $T=4$）的扩散过程，在保持高样本质量和多样性的同时，实现约 2000 倍的采样加速。

这一思路的关键洞见在于：GAN 的生成器天然具备建模复杂多模态分布的能力。通过将去噪分布 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 定义为条件 GAN 生成器的隐式分布——即引入隐变量 $\mathbf{z}$，由生成器 $G_\theta(\mathbf{x}_t, \mathbf{z}, t)$ 预测干净数据 $\mathbf{x}_0$，再经后验采样得到 $\mathbf{x}_{t-1}$——模型可以灵活捕捉大步长下真实去噪分布的多模态结构。同时，采用非饱和 GAN 对抗损失替代传统扩散模型中的 KL 散度（证据下界），以软化逆 KL 散度的方式训练，有助于增强模式覆盖。

这种设计使得模型仅需 **4 次网络推理**即可完成采样，在 CIFAR-10 上生成 100 张图像仅需 0.21 秒，相比 Score SDE（VP）加速约 2000 倍，同时 FID 保持 3.75、Recall 保持 0.57，实现了生成质量、采样速度和模式覆盖三个维度的有效平衡。

## 核心创新

### 问题瓶颈：高斯去噪假设导致采样慢

扩散模型生成高质量样本的代价是采样速度极慢，典型模型（如 DDPM）需要数百至上千次网络推理。本文指出，这一瓶颈的**根本原因**在于去噪分布的高斯假设。在标准扩散模型中，逆向去噪步 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 被参数化为高斯分布 $\mathcal{N}(\mu_\theta(\mathbf{x}_t, t), \sigma_t^2\mathbf{I})$，该假设仅在去噪步长 $\beta_t$ 极小（即 $T$ 很大，如 $T=1000$）时成立。当步长增大、数据分布非高斯时，真实去噪分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 会变得复杂且多模态（见 Figure 2），高斯分布无法有效拟合，导致模型必须依赖大量小步长迭代来维持生成质量。这一因果链条构成了扩散模型“高质量-高多样性-高采样速度”三难困境的核心约束。

### 关键洞察：大步长下真实去噪分布是多模态的

本文的核心洞察来自对去噪分布本质的重新审视：**当扩散步长较大且数据分布非高斯时，真实去噪分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 不再是简单的高斯，而是呈现出明显的多模态特性**。Figure 2 在一维多模态数据上展示了这一现象——随着步长增大，条件于固定 $\mathbf{x}_5$ 的去噪分布从近似高斯逐渐演化为多模态复杂分布。这一观察直接动摇了传统扩散模型“每步去噪可用高斯近似”的理论前提，为使用更强大的条件分布建模提供了理论动机。

### 方法创新：用条件 GAN 建模多模态去噪分布

基于上述洞察，本文提出 **Denoising Diffusion GAN**，核心创新是将去噪分布从单模态高斯替换为**由条件 GAN 建模的多模态分布**。具体而言，模型发生以下关键变化（changed slots）：

| 设计要素 | 基线方法（DDPM 等） | 本文方法（Denoising Diffusion GAN） |
|---------|-------------------|-----------------------------------|
| **去噪分布建模** | 高斯分布 $\mathcal{N}(\mu_\theta, \sigma_t^2\mathbf{I})$（单模态） | 多模态隐式分布，通过条件 GAN 生成器 $G_\theta(\mathbf{x}_t, \mathbf{z}, t)$ + 隐变量 $\mathbf{z}$ 实现 |
| **去噪步数 $T$** | 典型值 1000 | $\le 8$，实验最优为 4 |
| **训练目标** | 证据下界（ELBO，等价于前向 KL 散度） | 非饱和 GAN 对抗损失（软化逆 KL 散度）+ R1 正则化 |
| **去噪网络结构** | 确定性映射 $f_\theta(\mathbf{x}_t, t)$（U-Net） | 随机生成器 $G_\theta(\mathbf{x}_t, \mathbf{z}, t)$ + 后验采样（U-Net + AdaGN + 隐变量映射网络） |

#### 多模态去噪分布参数化

去噪分布 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 通过引入隐变量 $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 实现多模态：

$$p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t) := \int p(\mathbf{z})\, q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0 = G_\theta(\mathbf{x}_t, \mathbf{z}, t))\, d\mathbf{z}$$

其中 $G_\theta$ 是一个条件 GAN 生成器，输入噪声观测 $\mathbf{x}_t$、隐变量 $\mathbf{z}$ 和时间步 $t$，直接预测干净数据 $\mathbf{x}_0$；随后通过后验分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0)$ 采样得到 $\mathbf{x}_{t-1}$。不同 $\mathbf{z}$ 产生不同的 $\mathbf{x}_0$ 预测，从而赋予去噪分布多模态表达能力——这正是大步长去噪所必需的特性。

#### 对抗训练目标

训练目标从 KL 散度切换为对抗散度：

$$\min_\theta \sum_{t\ge 1} \mathbb{E}_{q(\mathbf{x}_t)}\left[D_{\mathrm{adv}}\big(q(\mathbf{x}_{t-1}|\mathbf{x}_t) \,\|\, p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)\big)\right]$$

判别器 $D_\phi(\mathbf{x}_{t-1}, \mathbf{x}_t, t)$ 以时间步 $t$ 为条件，区分真实去噪样本与生成样本。采用非饱和 GAN 损失配合 R1 梯度正则化，避免模式坍塌并稳定训练。

### 创新效果：突破三难困境

这一设计使得模型仅需 **4 步去噪**即可生成高质量样本，从根本上打破了扩散模型对大量迭代步数的依赖。在 CIFAR-10 上，Denoising Diffusion GAN（$T=4$）以 4 次网络推理实现 FID 3.75、Recall 0.57，生成 100 张图像仅需 0.21 秒，相较 Score SDE（VP）加速约 **2000 倍**，同时保持与 DDPM（$T=1000$，FID 3.21）接近的保真度和持平的多样性（Table 1）。在 StackedMNIST 模式覆盖测试中，模型覆盖全部 1000 个模式，KL 散度仅 0.071，显著优于 GAN 基线（Table 3）。

### 消融验证：隐变量多模态是关键

消融实验（Table 2）提供了因果证据：**移除隐变量 $\mathbf{z}$ 使去噪分布退化为单模态，FID 从 3.75 骤升至 20.6**，Recall 从 0.57 降至 0.42。这直接验证了多模态去噪分布是大步长扩散生成质量的核心保障。此外，$T=1$（退化为无条件 GAN）的 Recall 仅 0.19，远低于 $T=4$，表明扩散过程提供的条件信息对维持多样性至关重要——单纯用扩散做数据增强训练 GAN（FID 14.8）也无法达到本文方法的效果。

## 整体框架

Denoising Diffusion GANs 的整体 pipeline 由三个核心阶段构成：**前向扩散过程**、**多模态去噪模块**和**对抗训练与采样流程**。其根本设计动机源于一个关键观察：传统扩散模型采样慢的瓶颈在于去噪分布的高斯假设——该假设仅在小步长下成立，迫使模型采用成百上千步迭代（Figure 2 可视化地展示了当扩散步长增大时，真实去噪分布明显偏离高斯、呈现多模态特性）。本文通过将去噪分布从简单高斯替换为由条件 GAN 建模的表达能力更强的多模态分布，从而允许使用大步长和极少的去噪步数（T ≤ 8），在保持生成质量与多样性的同时实现约 2000 倍加速。

### 前向扩散过程

前向过程遵循经典扩散模型的设定，逐步向数据 $x_0$ 添加高斯噪声，生成一系列噪声版本 $x_1, x_2, \dots, x_T$：

$$q(x_t | x_{t-1}) = \mathcal{N}(x_t; \sqrt{1-\beta_t} x_{t-1}, \beta_t \mathbf{I})$$

与标准扩散模型的关键区别在于：本文设定总步数 $T$ 很小（$T \leq 8$），且每步的方差 $\beta_t$ 更大。这意味着中间状态 $x_t$ 的噪声水平跳跃更大，为后续大步长去噪创造条件。该模块的角色是提供具有不同噪声水平的条件信号 $x_t$，作为去噪模块的输入。

### 多模态去噪模块（每步）

这是框架的核心创新。对每个时间步 $t$，不再使用参数化的高斯分布 $p_\theta(x_{t-1}|x_t)$ 来近似真实去噪分布，而是采用条件 GAN 来灵活建模可能的多模态分布。具体而言，去噪分布定义为：

$$p_\theta(x_{t-1} | x_t) := \int p(z) \, q(x_{t-1} | x_t, x_0 = G_\theta(x_t, z, t)) \, dz$$

其中 $G_\theta$ 是条件生成器，输入为噪声图像 $x_t$、隐变量 $z \sim \mathcal{N}(0, \mathbf{I})$ 和时间步 $t$，输出预测的干净图像 $x_0$；随后通过后验分布 $q(x_{t-1}|x_t, x_0)$ 采样得到 $x_{t-1}$。隐变量 $z$ 的引入使得生成器能够为同一 $x_t$ 产生不同的 $x_0$ 预测，从而赋予去噪分布多模态表达能力——消融实验证实，移除 $z$ 会使模型退化为单模态，FID 从 3.75 骤升至 20.6。

该模块的判别器 $D_\phi$ 以三元组 $(x_{t-1}, x_t, t)$ 为输入，区分来自真实去噪分布的样本与生成器产生的样本，其非饱和损失为：

$$\min_\phi \sum_{t \ge 1} \mathbb{E}_q \left[ -\log D_\phi(x_{t-1}, x_t, t) + \mathbb{E}_{p_\theta} [-\log(1 - D_\phi(x_{t-1}, x_t, t))] \right]$$

### 对抗训练与采样流程

训练时，对每个时间步 $t$ 交替优化生成器和判别器，目标是最小化真实去噪分布与参数化去噪分布之间的对抗散度：

$$\min_\theta \sum_{t \ge 1} \mathbb{E}_{q(x_t)} \left[ D_{\text{adv}} \big( q(x_{t-1}|x_t) \,\|\, p_\theta(x_{t-1}|x_t) \big) \right]$$

实际训练采用非饱和 GAN 损失，并辅以 R1 正则化来稳定训练动态。采样时，从纯噪声 $x_T \sim \mathcal{N}(0, \mathbf{I})$ 开始，依次用训练好的条件生成器执行大步去噪，每步采样隐变量 $z$ 并通过后验采样得到 $x_{t-1}$，直至生成最终图像 $x_0$。以 CIFAR-10 上 T=4 的配置为例，仅需 4 次网络推理即可完成生成，耗时 0.21 秒（批量为 100），较 Score SDE 加速约 2000 倍。

### 模块间关系与数据流

整体数据流可概括为：**前向扩散**产生噪声状态序列 $\{x_t\}$ → **多模态去噪模块**在每步接收 $x_t$ 和随机隐变量 $z$，通过生成器预测 $x_0$ 并经后验采样输出 $x_{t-1}$ → **判别器**对每步的去噪结果进行真伪判断，驱动生成器学习匹配真实多模态去噪分布。三个阶段的协同使得模型在仅 4 步的条件下，实现了与千步扩散模型相当的生成质量（FID 3.75 vs 3.21）和多样性（Recall 均为 0.57），同时保持了远优于纯 GAN 的模式覆盖能力（在 StackedMNIST 上覆盖全部 1000 个模式，KL 散度仅 0.071）。

## 核心模块与公式推导

### 问题瓶颈：高斯去噪假设的失效

扩散模型采样慢的根本原因在于其去噪分布的高斯假设。标准扩散模型（DDPM）将反向去噪过程建模为：

$$p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_\theta(\mathbf{x}_t, t), \sigma_t^2\mathbf{I})$$

该高斯假设仅在去噪步长极小（即 $T$ 很大，通常为 1000）时成立。当步长增大时，真实去噪分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 变得复杂且多模态，高斯近似严重失效，这正是扩散模型需要成百上千次迭代去噪的本质原因。

### 核心模块：多模态条件去噪分布

**Denoising Diffusion GANs** 的核心创新在于将去噪分布从简单的高斯分布替换为表达能力更强的多模态分布。具体而言，采用条件 GAN 来建模每步的去噪分布 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$，使模型能够使用大步长（$T \leq 8$）进行去噪，从而将采样步数从千次量级压缩至个位数。

#### 前向扩散过程

前向过程沿用标准扩散模型的形式，但步数 $T$ 极小（$T \leq 8$），且每步的噪声方差 $\beta_t$ 更大：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1-\beta_t}\mathbf{x}_{t-1}, \beta_t\mathbf{I})$$

#### 多模态去噪分布参数化

去噪分布通过一个随机生成器 $G_\theta$ 来隐式定义。生成器输入含噪数据 $\mathbf{x}_t$、隐变量 $\mathbf{z} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 和时间步 $t$，预测干净数据 $\mathbf{x}_0$，再通过后验分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0)$ 采样得到 $\mathbf{x}_{t-1}$：

$$p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t) := \int p(\mathbf{z})\, q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0 = G_\theta(\mathbf{x}_t, \mathbf{z}, t))\, d\mathbf{z}$$

其中后验分布的均值和方差由扩散过程的解析形式给出：

$$\tilde{\mu}_t(\mathbf{x}_t,\mathbf{x}_0) = \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1-\bar{\alpha}_t}\mathbf{x}_0 + \frac{\sqrt{\alpha_t}(1-\bar{\alpha}_{t-1})}{1-\bar{\alpha}_t}\mathbf{x}_t, \quad \tilde{\beta}_t = \frac{1-\bar{\alpha}_{t-1}}{1-\bar{\alpha}_t}\beta_t$$

隐变量 $\mathbf{z}$ 的引入是关键——消融实验表明，移除 $\mathbf{z}$ 使去噪分布退化为单模态，FID 从 3.75 骤升至 20.6，Recall 从 0.57 降至 0.42，验证了多模态建模的必要性。

#### 生成器与判别器架构

- **生成器 $G_\theta$**：采用 NCSN++ 的 U-Net 结构，并通过自适应组归一化（AdaGN）将隐变量 $\mathbf{z}$ 注入归一化层的偏移和缩放参数中。
- **判别器 $D_\phi$**：接收三元组 $(\mathbf{x}_{t-1}, \mathbf{x}_t, t)$，区分真实的去噪样本与生成器产生的样本。

### 对抗训练目标

传统扩散模型使用证据下界（ELBO），即前向 KL 散度来匹配去噪分布：

$$\mathcal{L} = -\sum_{t\ge 1} \mathbb{E}_{q(\mathbf{x}_t)} [D_{\mathrm{KL}}(q(\mathbf{x}_{t-1}|\mathbf{x}_t) \| p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t))] + C$$

本文将其替换为对抗散度，采用非饱和 GAN 损失：

$$\min_\theta \sum_{t\ge 1} \mathbb{E}_{q(\mathbf{x}_t)} [D_{\mathrm{adv}}(q(\mathbf{x}_{t-1}|\mathbf{x}_t) \| p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t))]$$

具体训练时，判别器损失为时间条件的非饱和损失：

$$\min_\phi \sum_{t\ge 1} \mathbb{E}_{q}[ -\log D_\phi(\mathbf{x}_{t-1}, \mathbf{x}_t, t) + \mathbb{E}_{p_\theta}[ -\log (1-D_\phi(\mathbf{x}_{t-1}, \mathbf{x}_t, t))] ]$$

同时加入 R1 正则化以稳定训练。生成器和判别器交替优化。

### 采样过程

采样从纯噪声 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 开始，依次对 $t = T, T-1, \ldots, 1$ 执行大步去噪：采样 $\mathbf{z} \sim p(\mathbf{z})$，计算 $\mathbf{x}_0 = G_\theta(\mathbf{x}_t, \mathbf{z}, t)$，再从后验 $q(\mathbf{x}_{t-1}|\mathbf{x}_t, \mathbf{x}_0)$ 采样得到 $\mathbf{x}_{t-1}$。最终输出 $\mathbf{x}_0$ 为生成样本。整个过程仅需 $T \leq 8$ 次网络推理，在 CIFAR-10 上 $T=4$ 时生成 100 张图像仅需 0.21 秒，较 Score SDE 加速约 2000 倍。

## 实验与分析

### 核心瓶颈与设计动机验证

本文的核心假设是：扩散模型采样慢的根源在于去噪分布的高斯假设，该假设仅在小步长下成立。当扩散步长增大、数据分布非高斯时，真实去噪分布变得复杂且多模态（见 Figure 2）。这一理论动机在实验中得到直接验证：**Table 2** 的消融实验显示，当移除隐变量 $z$、使去噪分布退化为单模态时，FID 从 3.75 骤升至 20.6，Recall 从 0.57 降至 0.42，充分证明多模态建模是保持生成质量的关键因果杠杆。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/007_Table_2.jpg]]
*Table 2: Ablation studies on CIFAR-10*

### CIFAR-10 主实验结果

**Table 1** 汇总了无条件 CIFAR-10 生成的核心指标对比。Denoising Diffusion GAN（$T=4$）仅需 **4 次网络推理（NFE=4）**，生成 100 张图像耗时 **0.21 秒**，FID 为 **3.75**，IS 为 **9.63**，Recall 为 **0.57**。这一采样速度较 Score SDE（VP）的 423.2 秒实现约 **2000 倍加速**，同时 FID 与 DDPM（3.21）接近，Recall 持平（0.57）。在质量-速度权衡上，本文模型显著优于同等速度的 FastDDPM 等方案（见 Figure 4）。

需注意，FID 3.75 仍略逊于最优扩散模型（如 Score SDE 的 2.20），表明大步长去噪在保真度上仍有提升空间。

### 消融实验：步数、隐变量与参数化

**Table 2** 系统消融了三个关键设计选择：

- **去噪步数 $T$**：$T=1$ 退化为无条件 GAN，FID 高达 14.6，Recall 仅 0.19，多样性极差；$T=4$ 为最优平衡点；$T>4$ 时性能略有下降，论文推测当前架构容量不足以支撑更大 $T$。
- **隐变量 $z$**：移除 $z$ 后模型丧失多模态表达能力，FID 升至 20.6，直接验证了多模态去噪分布的必要性。
- **参数化方式**：预测 $x_0$（本文采用）优于直接预测去噪结果或预测噪声的变体。
- **对比“扩散作为数据增强”**：用扩散过程为一步 GAN 提供数据增强（FID 14.8）远逊于本文方案（FID 3.75），说明多步条件去噪的结构性优势并非仅来自数据增强。

### 模式覆盖与多样性评估

在 **StackedMNIST**（1000 个模式）上的模式覆盖实验（**Table 3**）中，Denoising Diffusion GAN 覆盖全部 **1000 个模式**，KL 散度仅 **0.071**，显著优于 StyleGAN2 w/ ADA（KL 散度 0.253，覆盖 928 个模式）等 GAN 基线。这一结果直接证明多模态去噪分布能有效缓解 GAN 的模式坍塌问题。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/008_Table_3.jpg]]
*Table 3: Mode coverage on StackedMNIST*

### 高分辨率数据集扩展

- **CelebA-HQ 256**（**Table 4**）：FID 为 **7.64**，接近 DDPM（7.16），优于 LSGM（7.22）和 StyleGAN2 w/ ADA（5.66 的 FID 更低，但本文强调 Recall 优势）。
- **LSUN Church 256**（**Table 5**）：FID 为 **5.25**，优于 ImageBART（6.24），进一步验证方法在场景级生成上的有效性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/010_Table_4.jpg]]
*Table 4: Generative results on CelebA-HQ-256*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/011_Table_5.jpg]]
*Table 5: Generative results on LSUN Church 256*

### 训练成本与稳定性

论文报告训练时间较长：CIFAR-10 约需 **48 GPU 小时**，CelebA-HQ 和 LSUN Church 各约 **180 小时**（8 块 V100）。尽管对抗训练存在潜在不稳定性，作者在附录中展示了各去噪步的判别器损失曲线（Figure 10），未观察到发散现象，但更大规模数据集上的稳定性仍需验证。

### 失败模式与局限性

1. **保真度天花板**：CIFAR-10 FID 3.75 仍不及 Score SDE（2.20），大步长去噪的细节恢复能力有待提升。
2. **$T$ 扩展性受限**：当前架构在 $T>4$ 时性能下降，表明需要更高容量的生成器设计来支持更多步数。
3. **多样性评估不全面**：Recall 指标仅在 CIFAR-10 和 StackedMNIST 上详细报告，其他数据集缺乏系统多样性评估。
4. **公平性未量化**：论文强调模式覆盖对减少社会偏见的积极意义，但未引入群组公平性指标或约束，需手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative results on CelebA-HQ 256 and LSUN Church Outdoor 256*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/013_Figure_8.jpg]]
*Figure 8: Multi-modality of denoising distribution given the same noisy observation. Left: clean image x0 and perturbed image x1. Right: Three samples from $p _ { \theta } ( \mathbf { x } _ { 0 } | \mathbf { x } _ { 1 }$ ) . Figure 9: Qualitative results on stroke-based synthesis. Top row: stroke paintings. Bottom two rows: generated samples corresponding to the stroke painting (best seen when zoomed in)

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/006_Table_1.jpg]]
*Table 1: Results for unconditional generation on CIFAR-10*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/014_Table_6.jpg]]
*Table 6: Hyper-parameters for the generator network*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/015_Table_7.jpg]]
*Table 7: Network structures for the discriminator. The number on the right indicates the number of channels in each residual block*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2112_07804/figures/016_Table_8.jpg]]
*Table 8: Optimization hyper-parameters*

## 方法谱系与知识库定位

### 1. 问题定位：扩散模型“三难困境”中的关键瓶颈

生成式学习领域长期面临一个“三难困境”（**Figure 1**）：生成质量（保真度）、采样速度与模式覆盖（多样性）难以兼得。**去噪扩散概率模型（DDPM）** 及其连续时间形式 **Score SDE (VP)** 虽在图像保真度（FID）与模式覆盖上达到顶尖水平，但其采样过程需要数百至上千次网络推理，速度极慢。本文的核心诊断是：**扩散模型采样速度慢的根本原因在于去噪分布的高斯假设**。

在经典扩散模型中，反向去噪过程 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 被参数化为一个高斯分布。这一假设仅在去噪步长 $\beta_t$ 极小（即 $T$ 很大，通常为 1000）时近似成立。当步长增大、数据分布非高斯时，真实的去噪分布 $q(\mathbf{x}_{t-1}|\mathbf{x}_t)$ 会变得**复杂且多模态**（**Figure 2** 可视化证实了这一点），高斯分布无法有效拟合，导致生成质量急剧下降。因此，现有扩散模型被迫采用极小步长，以牺牲采样速度为代价来维持高斯假设的合理性。

### 2. 方法谱系与基线对比

**Denoising Diffusion GANs** 在方法谱系上处于扩散模型与生成对抗网络（GAN）的交汇点，其核心创新在于用**多模态条件 GAN 替代单模态高斯分布**来建模去噪分布，从而打破“小步长”的约束。

#### 2.1 与经典扩散模型的对比

| 维度 | DDPM / Score SDE (VP) | Denoising Diffusion GANs |
|------|----------------------|--------------------------|
| **去噪分布** | 高斯分布（单模态） | 多模态条件 GAN（通过隐变量 $z$ 实现） |
| **去噪步数 $T$** | 典型值 1000 | $\le 8$，实验最优为 4 |
| **训练目标** | 证据下界（ELBO，即前向 KL 散度） | 非饱和 GAN 对抗损失（软化逆 KL 散度）+ R1 正则化 |
| **去噪网络** | 确定性映射 $f_\theta(\mathbf{x}_t, t)$（U-Net） | 随机生成器 $G_\theta(\mathbf{x}_t, z, t)$ + 后验采样 |
| **采样速度 (CIFAR-10)** | 423.2 s / 100 张（Score SDE） | 0.21 s / 100 张（约 **2000× 加速**） |
| **NFE** | 1000–2000 | 4 |
| **FID (CIFAR-10)** | 3.21 (DDPM) / 2.20 (Score SDE) | 3.75（略高但接近） |
| **Recall** | 0.57 (DDPM) | 0.57（持平） |

**关键差异**：本文模型在保持与 DDPM 相当的多样性和接近的保真度的同时，将采样速度提升了约三个数量级。FID 略逊于最优扩散模型（如 Score SDE 的 2.20），但 Recall 持平，表明模式覆盖能力未受损。

#### 2.2 与加速扩散模型变体的对比

- **FastDDPM**：通过非马尔可夫前向过程减少去噪步数，但本质上仍依赖高斯去噪分布。本文模型在 CIFAR-10 上采样速度比 FastDDPM 快约 **20 倍**（0.21 s vs. 约 4 s），且 FID 更优（3.75 vs. 约 3.4）。
- **LSGM**：在潜在空间中训练扩散模型，通过压缩维度加速采样，但去噪分布仍为高斯。本文方法与之正交，理论上可结合潜在空间建模进一步加速。

#### 2.3 与 GAN 基线的对比

- **StyleGAN2 w/ ADA**：当前最优 GAN 基线，具有自适应数据增强。在 CIFAR-10 上，StyleGAN2 的 FID 约为 2.92，但 Recall 显著低于本文模型（**Table 1** 中 Recall 0.41 vs. 0.57），表明 GAN 存在严重的模式坍塌问题。
- **无条件 GAN（T=1 消融）**：当 $T=1$ 时，本文模型退化为无条件 GAN，FID 升至 14.6，Recall 骤降至 0.19（**Table 2**）。这直接证明了扩散过程提供的多步条件信息对维持多样性的关键作用。

#### 2.4 核心消融：隐变量 $z$ 的必要性

移除隐变量 $z$ 后，去噪分布退化为单模态，FID 从 3.75 骤升至 20.6，Recall 从 0.57 降至 0.42（**Table 2**）。这直接验证了**多模态去噪分布是本文方法有效性的核心因果机制**——单模态分布无法捕捉大步长下的复杂去噪分布。

### 3. 适用边界与局限

#### 3.1 适用边界

1. **大步长少步数扩散场景**：方法适用于 $T \le 8$ 的设置，在此范围内采样速度与生成质量达到最佳权衡。
2. **无条件与条件图像生成**：在 CIFAR-10、CelebA-HQ 256、LSUN Church 256 等数据集上验证有效，FID 接近或优于同期扩散模型。
3. **模式覆盖敏感任务**：在 StackedMNIST（1000 个模式）上，本文模型覆盖全部模式，KL 散度仅 0.071，显著优于 GAN 基线（**Table 3**），适用于对多样性要求高的场景。

#### 3.2 已知局限

1. **保真度仍有差距**：CIFAR-10 上 FID 3.75 仍逊于 Score SDE 的 2.20，在大步长下如何进一步提升保真度是待解问题。
2. **训练计算成本高**：CIFAR-10 需约 48 GPU 小时，CelebA-HQ 和 LSUN Church 各需约 180 小时（8 块 V100），训练开销显著高于单步 GAN 和部分加速扩散模型。
3. **架构扩展性受限**：当 $T$ 增大时（$T > 8$），性能反而下降，表明当前生成器/判别器容量不足以支撑更大步数下的去噪分布建模。
4. **对抗训练稳定性**：尽管本文未观察到训练发散，但对抗训练本质上的不稳定性仍需在更多数据集和更长训练周期下验证。
5. **多样性评估不全面**：Recall 指标仅在 CIFAR-10 和 StackedMNIST 上详细报告，其他数据集缺乏全面的模式覆盖评估。

### 4. 开放问题与未来方向

1. **能否进一步减少 $T$ 至 1–2 步？** 当前 $T=1$ 时模型退化为无条件 GAN 且效果很差，如何设计更强大的条件机制使极少数步数下仍保持多模态去噪能力，是实现“单步高质量生成”的关键。
2. **如何提升大步长去噪的保真度？** 需要设计更高效的生成器架构（如更大容量或更优的条件注入方式），以更精确地拟合大步长下的复杂去噪分布。
3. **能否推广到连续时间或潜在扩散模型？** 将多模态去噪分布的思想引入 Latent Diffusion 等模型，有望在潜在空间中实现更大步长、更少步数的采样。
4. **对抗损失与扩散目标的更优对齐？** 当前对抗损失替代了 KL 散度，是否存在更优的散度形式或混合训练策略，能同时提升训练效率和最终质量？
5. **多模态去噪分布与公平性的关系？** 多模态去噪分布理论上能更好地覆盖数据中的少数群体模式，但尚未有定量公平性评估。未来可引入群组公平性指标，验证该方法在减少生成偏见方面的潜力。

## 原文 PDF

![[paperPDFs/ICLR_2022/Tackling_the_Generative_Learning_Trilemma_with_Denoising_Diffusion_GANs.pdf]]
