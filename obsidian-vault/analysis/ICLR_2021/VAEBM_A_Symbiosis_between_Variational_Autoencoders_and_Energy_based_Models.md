---
title: "VAEBM: A Symbiosis between Variational Autoencoders and Energy-based Models"
type: paper
paper_level: A
venue: ICLR
year: 2021
pdf_ref: paperPDFs/ICLR_2021/VAEBM_A_Symbiosis_between_Variational_Autoencoders_and_Energy_based_Models.pdf
aliases:
- VAEBM
tags:
- ICLR_2021
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过能量函数$E_{\\psi}(\\mathbf{x})$显式地降低非数据区域的可能性，并结合在VAE潜在空间中重新参数化的MCMC采样，从而加速混合并提高样本质量。"
primary_logic: "将VAE生成分布与EBM能量函数相乘，形成共生模型，其中VAE捕捉整体模态结构，EBM精炼细节并排除非数据区域；通过在噪声变量空间（$\\epsilon_{\\mathbf{z}}, \\epsilon_{\\mathbf{x}}$）中进行MCMC，避免了在像素空间中的缓慢混合，并可调整步长。"
claims:
- "在CIFAR-10上，VAEBM相比NVAE将FID从51.67降至12.19，IS从5.51提升至8.43。"
- "在LSUN Church 64上，VAEBM将FID从41.3（NVAE）降至13.51。"
- "在噪声空间中重新参数化MCMC对于获得高质量样本至关重要，因(x,z)空间直接采样无法产出好样本。"
- "VAEBM在StackedMNIST上实现了1000模式全覆盖，KL散度0.087。"
---

# VAEBM: A Symbiosis between Variational Autoencoders and Energy-based Models

> [!tip] 核心洞察
> 将VAE生成分布与EBM能量函数相乘，形成共生模型，其中VAE捕捉整体模态结构，EBM精炼细节并排除非数据区域；通过在噪声变量空间（$\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}}$）中进行MCMC，避免了在像素空间中的缓慢混合，并可调整步长。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VAEBM：变分自编码器与能量模型的共生组合 |
| 英文题名 | VAEBM: A Symbiosis between Variational Autoencoders and Energy-based Models |
| 会议/期刊 | ICLR 2021 |
| Links | [paper](https://arxiv.org/abs/2010.00654); [GitHub](https://github.com/NVlabs/VAEBM) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | VAEBM |
| Dataset | CIFAR-10, CelebA 64, LSUN Church 64 |

> [!tip] 效果简介
> - CIFAR-10 上，FID↓ 为 12.19 (w/ persistent)，对比 51.67 (NVAE)，变化 -39.48。
> - CIFAR-10 上，IS↑ 为 8.43，对比 5.51 (NVAE)，变化 +2.92。
> - CelebA 64 上，FID↓ 为 5.31，对比 14.74 (NVAE)，变化 -9.43。

## 概述

### 问题背景

深度生成模型的两大主流范式——变分自编码器（VAE）与能量模型（EBM）——各自存在结构性缺陷。VAE倾向于将高概率密度错误地分配给数据空间中的非数据区域，导致生成样本模糊或出现损坏伪影；纯EBM虽然在理论上能够精确建模数据分布，但其依赖的MCMC采样过程在像素空间中混合极其缓慢，计算代价高昂。这两种缺陷在复杂图像生成任务中尤为突出，限制了各自范式的实际表现。

### 核心思路

VAEBM提出了一种**共生组合框架**：将VAE的生成分布与EBM的能量函数相乘，构造联合生成模型

$$h_{\psi,\theta}(\mathbf{x},\mathbf{z}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x},\mathbf{z}) e^{-E_{\psi}(\mathbf{x})}$$

其中VAE负责捕捉数据的整体模态结构，EBM则通过能量函数显式压低非数据区域的概率密度，精细修正样本细节。关键的工程创新在于将MCMC采样从像素空间重新参数化到噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$，利用VAE解码器的确定性映射 $T_{\theta}$ 将标准高斯噪声转化为数据样本，从而大幅加速MCMC混合并允许统一步长调整。训练采用两阶段策略：先独立训练VAE至收敛，再固定VAE仅训练能量函数，避免了联合优化的不稳定性。

### 方法定位

VAEBM在方法谱系中处于VAE与EBM的交叉地带，与以下基线形成对比：

- **NVAE**（Vahdat & Kautz, NeurIPS 2020）：当时最先进的层次化VAE，作为VAEBM的生成器骨干及主要VAE基线。
- **IGEBM**（Du & Mordatch, ICML 2019）：纯EBM基线，依赖像素空间长链Langevin动力学采样。
- **NCSN**（Song & Ermon, NeurIPS 2019）：基于分数的生成模型，通过退火Langevin动力学生成样本。
- **SNGAN**（Miyato et al., ICLR 2018）：GAN基线，代表对抗训练范式。

与上述方法相比，VAEBM的核心差异在于：将EBM作为VAE生成器的“精炼器”而非独立生成模型，并在噪声空间而非像素空间执行MCMC，从而在保持VAE快速采样的同时获得EBM的精细建模能力。

### 主要结果

VAEBM在多个基准数据集上实现了生成质量的显著跃升：

- **CIFAR-10**：FID从NVAE的51.67降至12.19，IS从5.51提升至8.43（Table 1）。
- **CelebA 64**：FID从14.74降至5.31（Table 2）。
- **LSUN Church 64**：FID从41.3降至13.51。
- **CelebA HQ 256**：FID从45.11降至20.38（Table 3），在256×256分辨率上首次展示了VAE类模型生成逼真人脸的潜力。
- **StackedMNIST**：实现1000模式全覆盖，KL散度仅0.087（Table 5），验证了模式覆盖能力。
- **OOD检测**：在SVHN上AUROC达0.83，远超NVAE的0.42（Table 6），表明能量函数提供了有效的密度估计。

消融实验确认了关键设计选择：在噪声空间进行MCMC是获取高质量样本的必要条件（直接于 $(x,z)$ 空间采样无法产出好样本），且VAEBM显著优于基于WGAN的对抗训练变体。

## 背景与动机

### 深度生成模型的两条主线

深度生成模型的核心目标是学习数据分布 $p_d(\mathbf{x})$，以便生成逼真的新样本。近年来，该领域主要沿着两条技术路径发展：

**变分自编码器（VAE）** 通过最大化数据对数似然的变分下界（ELBO）进行训练：

$$\log p_{\theta}(\mathbf{x}) \geq \mathbb{E}_{\mathbf{z}\sim q_{\phi}(\mathbf{z}|\mathbf{x})}[\log p_{\theta}(\mathbf{x}|\mathbf{z})] - D_{\mathrm{KL}}(q_{\phi}(\mathbf{z}|\mathbf{x}) || p_{\theta}(\mathbf{z}))$$

VAE的优势在于训练稳定、能够覆盖数据分布的多个模态，但其生成样本往往模糊、缺乏细节。这一缺陷的根源在于：VAE倾向于将高概率质量分配给数据空间中的非数据区域，导致模型在生成时可能采样到这些无效区域，产生模糊或损坏的样本。

**能量模型（EBM）** 则通过定义非归一化的能量函数 $E_{\psi}(\mathbf{x})$ 来刻画数据分布：

$$p_{\psi}(\mathbf{x}) = \frac{\exp(-E_{\psi}(\mathbf{x}))}{Z_{\psi}}$$

其中 $Z_{\psi}$ 为配分函数。EBM的训练依赖于对比散度，需要从模型分布中采样以计算负相梯度：

$$\partial_{\psi} L(\psi) = \mathbb{E}_{\mathbf{x}\sim p_d(\mathbf{x})}[-\partial_{\psi} E_{\psi}(\mathbf{x})] + \mathbb{E}_{\mathbf{x}\sim p_{\psi}(\mathbf{x})}[\partial_{\psi} E_{\psi}(\mathbf{x})]$$

采样通常通过Langevin动力学实现：

$$\mathbf{x}_{t+1} = \mathbf{x}_t - \frac{\eta}{2} \nabla_{\mathbf{x}} E_{\psi}(\mathbf{x}_t) + \sqrt{\eta} \omega_t, \quad \omega_t \sim \mathcal{N}(0, \mathbf{I})$$

EBM能够精细地建模数据分布，生成高质量样本，但其致命弱点是MCMC采样在像素空间中混合极其缓慢，计算成本高昂。以**IGEBM**（Du & Mordatch, ICML 2019）为代表的纯EBM方法，虽然在某些任务上表现不错，但采样效率低下严重限制了其可扩展性。

### 现有方法的缺口

上述两条路径各自存在根本性瓶颈：

1. **VAE的模糊生成问题**：尽管**NVAE**（Vahdat & Kautz, NeurIPS 2020）等分层VAE大幅提升了生成质量，但VAE的底层机制——最大化似然下界——本质上无法有效惩罚非数据区域的高概率分配。在CIFAR-10上，NVAE的FID仍高达51.67，生成样本缺乏清晰纹理。

2. **EBM的采样效率瓶颈**：纯EBM在像素空间运行MCMC，需要数百甚至上千步Langevin动力学才能获得合理样本。例如，**NCSN**（Song & Ermon, NeurIPS 2019）生成50个CIFAR-10样本需要107.9秒，难以实用化。

3. **GAN的替代方案及其局限**：**SNGAN**（Miyato et al., ICLR 2018）等GAN方法虽然生成质量高，但存在模式坍塌、训练不稳定等问题，且缺乏显式的概率密度评估能力。

### 核心动机：共生组合

本文的核心洞察在于：VAE和EBM并非互斥的替代方案，而是可以互补的共生组件。VAE擅长捕捉数据的全局模态结构，能够提供一个“大致正确”的生成分布；EBM则擅长精细建模，能够通过能量函数显式地降低非数据区域的可能性。将二者结合，可以形成一种共生模型——**VAEBM**，其中VAE提供粗粒度的模态覆盖，EBM在此基础上精炼细节并抑制无效样本。

这一设计的关键优势在于：通过将VAE的生成分布与EBM的能量函数相乘，VAEBM的联合分布定义为：

$$h_{\psi,\theta}(\mathbf{x},\mathbf{z}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x},\mathbf{z}) e^{-E_{\psi}(\mathbf{x})}$$

其中 $p_{\theta}(\mathbf{x},\mathbf{z})$ 来自预训练的VAE，$E_{\psi}(\mathbf{x})$ 是待训练的能量函数。这种乘积形式使得训练可以自然地分解为两个阶段：先训练VAE至收敛，再固定VAE训练EBM。更重要的是，预训练的VAE提供了一个低维、平滑的潜在空间，使得MCMC采样可以在噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$ 中高效进行，从而避开像素空间的缓慢混合问题。

## 核心创新

VAEBM 的核心创新在于将 VAE 与 EBM 两种生成范式进行**共生组合**（symbiosis），而非简单的级联或替代。其关键洞察是：VAE 擅长捕捉数据的全局模态结构但倾向于在非数据区域分配概率质量，导致样本模糊；EBM 能够精细建模数据分布但 MCMC 采样在像素空间中混合缓慢。VAEBM 通过将两者相乘，使 VAE 提供整体结构，EBM 精炼细节并显式压低非数据区域的概率。

这一共生设计通过以下关键机制实现突破：

**1. 乘积形式的联合分布定义**

VAEBM 将生成模型定义为 VAE 生成分布与 EBM 能量项的乘积：
$$h_{\psi,\theta}(\mathbf{x},\mathbf{z}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x},\mathbf{z}) e^{-E_{\psi}(\mathbf{x})}$$

这与单独使用 VAE（$p_{\theta}(\mathbf{x})$）或 EBM（$\exp(-E_{\psi}(\mathbf{x}))/Z_{\psi}$）有本质区别。能量函数 $E_{\psi}(\mathbf{x})$ 直接作用于数据空间，通过梯度精细调整 VAE 生成的样本，同时显式降低非数据区域的可能性。这一设计的直接效果是：在 CIFAR-10 上，VAEBM 将 NVAE 的 FID 从 51.67 降至 12.19（Table 1），IS 从 5.51 提升至 8.43。

**2. 噪声空间中的重参数化 MCMC 采样**

这是 VAEBM 最具决定性的技术贡献。纯 EBM 在像素空间 $\mathbf{x}$ 中运行 Langevin 动力学，混合缓慢且计算成本高。VAEBM 利用预训练 VAE 的确定性映射，将采样重新参数化到标准高斯噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$：
$$\mathbf{z} = T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \quad \mathbf{x} = T_{\theta}^{\mathbf{x}}(\mathbf{z}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}})$$

在噪声空间中，目标分布变为：
$$h_{\psi,\theta}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}}) \propto e^{-E_{\psi}(T_{\theta}^{\mathbf{x}}(T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}}))} p_{\epsilon}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}})$$

这一设计的核心优势是：噪声变量具有统一的方差尺度，允许使用统一的 Langevin 步长，自动适应各变量的方差。消融实验（Appendix B.1, Figure 5）明确表明，在噪声空间中采样对于获得高质量样本**至关重要**——直接在 $(\mathbf{x}, \mathbf{z})$ 空间中采样无法产出好样本。

**3. 两阶段解耦训练策略**

VAEBM 采用先训练 VAE 至收敛、再固定 VAE 训练 EBM 的策略。这一设计的关键优势是：预训练 VAE 提供的潜在空间具有有效更低的维度和更平滑的分布，为 EBM 的 MCMC 采样提供了良好的初始化。训练 EBM 时，梯度分解为：
$$\partial_{\psi} L(\psi) = \mathbb{E}_{\mathbf{x}\sim p_d(\mathbf{x})}[-\partial_{\psi} E_{\psi}(\mathbf{x})] + \mathbb{E}_{\mathbf{x}\sim h_{\psi,\theta}(\mathbf{x},\mathbf{z})}[\partial_{\psi} E_{\psi}(\mathbf{x})]$$

正相来自数据，负相通过在噪声空间中运行短链 Langevin 动力学获得近似样本。消融实验（Table 4）证实，VAEBM（FID 12.96）显著优于仅在 $\mathbf{x}$ 上定义 EBM 的变体（FID 48.89），也优于基于 WGAN 的对抗训练版本（FID 20.39）。

**4. 能量函数正则化改进**

与纯 EBM（如 **IGEBM**，Du & Mordatch, ICML 2019）使用谱归一化不同，VAEBM 采用权重归一化配合数据相关初始化，并将激活函数换为 Swish（Appendix E），这些细节改进有助于稳定能量函数的训练。

**与基线方法的关键差异总结**

| 设计维度 | 基线方法 | VAEBM 创新 |
|---------|---------|-----------|
| 生成模型定义 | VAE: $p_{\theta}(\mathbf{x})$；EBM: $\exp(-E_{\psi}(\mathbf{x}))/Z_{\psi}$ | $h_{\psi,\theta}(\mathbf{x}) = p_{\theta}(\mathbf{x}) e^{-E_{\psi}(\mathbf{x})} / Z_{\psi,\theta}$ |
| MCMC 采样空间 | 像素空间 $\mathbf{x}$ | 噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$ |
| 训练流程 | VAE 或 EBM 单独训练 | 两阶段：先 VAE 后固定 VAE 训练 EBM |
| 步长调整 | 每变量单独调整 | 噪声空间中统一步长，自动适应方差 |
| 能量正则化 | 谱归一化 | 权重归一化 + 数据相关初始化 + Swish |

**证据强度评估**：噪声空间重参数化 MCMC 的关键作用有 Figure 5 和 Appendix B.1 的消融实验直接支撑（置信度 0.95）；乘积形式定义的有效性通过 CIFAR-10 上 FID 从 51.67 到 12.19 的巨大提升得到验证（置信度 0.95）；两阶段训练策略的合理性由 Table 4 中与联合训练变体的对比支持（置信度 0.95）。

## 整体框架

VAEBM 的生成模型定义为一个共生组合：将预训练 VAE 的生成分布与一个定义在数据空间的能量模型（EBM）相乘，形成一个联合分布：

$$h_{\psi,\theta}(\mathbf{x},\mathbf{z}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x},\mathbf{z}) e^{-E_{\psi}(\mathbf{x})}$$

其中 $p_{\theta}(\mathbf{x},\mathbf{z})$ 是 VAE 的生成分布，$E_{\psi}(\mathbf{x})$ 是能量函数，$Z_{\psi,\theta}$ 为配分函数。这一设计的核心洞察在于：**VAE 负责捕捉数据的整体模态结构，而 EBM 通过能量函数显式压低非数据区域的概率，精炼样本细节**。这是整个框架的瓶颈突破机制——纯 VAE 倾向于将高概率分配给数据空间中的无效区域，导致生成模糊或损坏；纯 EBM 在像素空间中的 MCMC 混合缓慢、计算代价极高。VAEBM 将二者优势耦合，VAE 提供低维、平滑的潜在空间，使 EBM 的 MCMC 采样得以高效进行。

### 两阶段训练流水线

框架采用解耦的两阶段训练策略（Figure 1）：

1. **阶段一：VAE 预训练**
   使用标准 VAE 目标（ELBO）训练 VAE 至收敛。此阶段仅优化 VAE 的参数 $\theta$，与能量函数无关。

2. **阶段二：固定 VAE，训练能量函数**
   VAE 参数冻结后，仅训练能量函数 $E_{\psi}(\mathbf{x})$。训练梯度由正相（数据）和负相（模型采样）组成：
   $$\partial_{\psi} L(\psi) = \mathbb{E}_{\mathbf{x}\sim p_d(\mathbf{x})}[-\partial_{\psi} E_{\psi}(\mathbf{x})] + \mathbb{E}_{\mathbf{x}\sim h_{\psi,\theta}(\mathbf{x},\mathbf{z})}[\partial_{\psi} E_{\psi}(\mathbf{x})]$$
   负相样本通过 MCMC 从模型分布中采样获得。

### 重新参数化与噪声空间采样

框架的关键创新在于 MCMC 采样的重新参数化。为避免在像素空间直接采样的低效，VAEBM 将 VAE 的生成过程表达为从标准高斯噪声到数据的确定性映射：

$$\mathbf{z} = T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \quad \mathbf{x} = T_{\theta}^{\mathbf{x}}(\mathbf{z}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}}) = T_{\theta}^{\mathbf{x}}(T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}})$$

其中 $\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}} \sim \mathcal{N}(0, \mathbf{I})$。在此噪声变量空间中，目标分布变为：

$$h_{\psi,\theta}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}}) \propto e^{-E_{\psi}(T_{\theta}^{\mathbf{x}}(T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}}))} p_{\epsilon}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}})$$

MCMC 采样（Langevin 动力学）在此噪声空间中进行，而非像素空间。这带来两个关键优势：**（1）VAE 的潜在空间比原始数据空间更平滑、维度更低，显著加速 MCMC 混合；（2）噪声空间中的步长可以统一设定，自动适应各变量的方差**。消融实验证实，在噪声空间中进行 MCMC 并适当调整步长是获得高质量样本的关键因素——直接在 $(\mathbf{x}, \mathbf{z})$ 空间采样无法产出好样本（Figure 5）。

### 采样与生成流程

测试时，从标准高斯噪声初始化 $\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}}$，运行短链 Langevin 动力学（通常 16 步）在噪声空间中采样，再通过确定性映射 $T_{\theta}$ 转换为图像。整个流程仅需约 8.79 秒生成 50 个 CIFAR-10 样本，远快于基于分数的模型 NCSN（107.9 秒）。

### 模块关系总结

| 模块 | 角色 | 输入 | 输出 |
|------|------|------|------|
| VAE 生成器 (NVAE) | 提供先验分布与基本生成能力 | 噪声 $\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}}$ | 初始样本 $\mathbf{x}$、潜在变量 $\mathbf{z}$ |
| 能量函数 $E_{\psi}(\mathbf{x})$ | 评估样本真实性，梯度精细调整 | 样本 $\mathbf{x}$ | 能量值、梯度 |
| 重新参数化映射 $T_{\theta}$ | 噪声空间到数据空间的确定性变换 | $\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}}$ | $\mathbf{z}, \mathbf{x}$ |
| Langevin 动力学采样器 | 在噪声空间中运行 MCMC | 初始噪声、能量梯度 | 精炼后的噪声样本 |

两阶段训练虽然简化了优化，但也意味着 VAE 在 EBM 训练期间不被联合微调，这可能限制了模型的最终潜力。能量函数的训练需要人工判断停止时机（当生成样本不再真实时），引入了一定的研究者偏差。

## 核心模块与公式推导

### 1. 生成模型定义

VAEBM的核心思想是将VAE的生成分布与EBM的能量函数相乘，构建一个共生生成模型。其联合分布定义如下：

$$h_{\psi,\theta}(\mathbf{x},\mathbf{z}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x},\mathbf{z}) e^{-E_{\psi}(\mathbf{x})}$$

其中：
- $p_{\theta}(\mathbf{x},\mathbf{z})$ 是预训练VAE的联合分布
- $E_{\psi}(\mathbf{x})$ 是定义在数据空间上的能量函数
- $Z_{\psi,\theta}$ 是配分函数，用于归一化

对潜在变量 $\mathbf{z}$ 积分后，得到数据 $\mathbf{x}$ 的边缘分布：

$$h_{\psi,\theta}(\mathbf{x}) = \frac{1}{Z_{\psi,\theta}} p_{\theta}(\mathbf{x}) e^{-E_{\psi}(\mathbf{x})}$$

**设计动机**：VAE倾向于将高概率分配给数据空间中的非数据区域，导致生成样本模糊或损坏；纯EBM在像素空间中MCMC混合缓慢。通过乘积形式，VAE捕捉整体模态结构，EBM通过能量函数显式降低非数据区域的可能性，精炼细节。

### 2. 两阶段训练流程

VAEBM采用解耦的两阶段训练策略：

**阶段一：训练VAE**。使用标准VAE目标（变分下界ELBO）训练生成器至收敛：

$$\log p_{\theta}(\mathbf{x}) \geq \mathbb{E}_{\mathbf{z}\sim q_{\phi}(\mathbf{z}|\mathbf{x})}[\log p_{\theta}(\mathbf{x}|\mathbf{z})] - D_{\mathrm{KL}}(q_{\phi}(\mathbf{z}|\mathbf{x}) || p_{\theta}(\mathbf{z}))$$

**阶段二：固定VAE，训练能量函数**。此时训练目标简化为EBM的最大似然估计，梯度为：

$$\partial_{\psi} L(\psi) = \mathbb{E}_{\mathbf{x}\sim p_d(\mathbf{x})}[-\partial_{\psi} E_{\psi}(\mathbf{x})] + \mathbb{E}_{\mathbf{x}\sim h_{\psi,\theta}(\mathbf{x},\mathbf{z})}[\partial_{\psi} E_{\psi}(\mathbf{x})]$$

- **正相**：从真实数据分布 $p_d(\mathbf{x})$ 采样，降低真实样本的能量
- **负相**：从模型分布 $h_{\psi,\theta}(\mathbf{x},\mathbf{z})$ 采样，提高模型生成样本的能量

**关键设计**：两阶段分离使得VAE提供结构化的先验，EBM仅需修正VAE的偏差，避免了联合训练的稳定性问题。

### 3. 噪声空间重参数化与MCMC采样

这是VAEBM获得高质量样本的关键模块。标准EBM在像素空间 $\mathbf{x}$ 中运行Langevin动力学：

$$\mathbf{x}_{t+1} = \mathbf{x}_t - \frac{\eta}{2} \nabla_{\mathbf{x}} E_{\psi}(\mathbf{x}_t) + \sqrt{\eta} \omega_t, \quad \omega_t \sim \mathcal{N}(0, \mathbf{I})$$

但像素空间维度高、分布复杂，混合缓慢。VAEBM将采样转移到**噪声变量空间** $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$。

**重参数化映射** $T_{\theta}$ 将标准高斯噪声确定性地转换为潜在变量和数据：

$$\mathbf{z} = T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \quad \mathbf{x} = T_{\theta}^{\mathbf{x}}(\mathbf{z}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}}) = T_{\theta}^{\mathbf{x}}(T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}})$$

在噪声空间中，目标分布变为：

$$h_{\psi,\theta}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}}) \propto e^{-E_{\psi}(T_{\theta}^{\mathbf{x}}(T_{\theta}^{\mathbf{z}}(\epsilon_{\mathbf{z}}), \epsilon_{\mathbf{x}}))} p_{\epsilon}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}})$$

其中 $p_{\epsilon}(\epsilon_{\mathbf{x}}, \epsilon_{\mathbf{z}})$ 是标准高斯先验。

**核心优势**：
- 噪声空间维度更低、分布更平滑，MCMC混合效率显著提升
- 步长可在噪声空间中统一设定，自动适应各变量的方差
- 消融实验证实：在 $(x,z)$ 增强空间中采样相比仅在 $x$ 上定义的EBM，FID从48.89降至12.96（Table 4）；在噪声空间中重参数化是获得高质量样本的必要条件（Figure 5, Appendix B.1）

### 4. 能量函数正则化

为确保训练稳定性，能量函数 $E_{\psi}$ 采用以下正则化技术（Appendix E）：
- 使用**权重归一化**（Weight Normalization）替代谱归一化
- 采用**数据相关初始化**（data-dependent initialization）
- 激活函数替换为**Swish**

### 5. 训练目标下界

VAEBM的对数似然下界由VAE损失和EBM损失共同构成：

$$\log h_{\psi,\theta}(\mathbf{x}) \geq \mathcal{L}_{\mathrm{vae}}(\mathbf{x},\theta,\phi) - E_{\psi}(\mathbf{x}) - \log Z_{\psi,\theta}$$

该下界将训练自然分解为VAE优化和EBM优化两部分，支撑了两阶段训练策略。

## 实验与分析

### 核心定量结果

VAEBM在多个基准数据集上以显著优势超越其直接基线NVAE，并在FID指标上逼近或达到当时最先进生成模型的水准。**Table 1** 汇总了CIFAR-10无条件生成的主要对比：

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/002_Table_1.jpg]]
*Table 1: IS and FID scores for unconditional generation on CIFAR-10*

- **相对NVAE的飞跃**：VAEBM将FID从NVAE的51.67骤降至12.19（使用持续链），降幅达39.48；IS从5.51提升至8.43。这一提升源于能量函数显式抑制了VAE生成的非数据区域样本，同时噪声空间中的MCMC精炼了样本细节。
- **与纯EBM的对比**：纯EBM基线IGEBM（Du & Mordatch, ICML 2019）的FID为40.58，VAEBM的12.19体现了在VAE潜在空间中进行重参数化MCMC对采样效率与质量的根本性改善。
- **与基于分数的模型对比**：NCSN（Song & Ermon, NeurIPS 2019）的FID为25.32，VAEBM显著更优，且生成速度远快于NCSN（见下文效率分析）。

在更大尺寸图像上，VAEBM同样表现出色。**Table 2** 显示，在CelebA 64上，VAEBM的FID为5.31（NVAE为14.74），已接近当时最佳GAN的水平。**Table 3** 表明，在CelebA HQ 256上，FID从NVAE的45.11降至20.38。在LSUN Church 64上，FID从41.3（NVAE）降至13.51（Section 5.1）。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results on CelebA 64, LSUN Church 64 and CelebA HQ 256. For CelebA HQ 256, we initialize the MCMC chains with low temperature NVAE samples (t = 0.7) for better visual quality. On this dataset samples are selected for diversity. See Appendix H for additional qualitative results and uncurated CelebA HQ 256 samples obtained from higher temperature initializations. Note that the FID in Table 3 is computed with full temperature samples*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/006_Table_2.jpg]]
*Table 2: Generative performance on CelebA 64 Table 3: Generative performance on CelebA HQ 256*

### 消融实验：共生机制的必要性

**Table 4** 的消融实验验证了VAEBM设计中的关键选择：

- **仅在x空间定义EBM vs. 在(x,z)增强空间定义EBM**：仅在像素空间x上定义能量函数（即不利用VAE的潜在变量）导致FID从12.96恶化至48.89。这证实了在联合空间中运行MCMC对于有效采样至关重要——VAE的潜在空间提供了更平滑、维度更低的流形，使Langevin动力学能高效混合。
- **EBM vs. WGAN判别器**：将能量函数替换为WGAN判别器（以NVAE解码器初始化）得到的FID为20.39，远差于VAEBM的12.96。这表明对抗训练的判别器无法像EBM那样通过显式概率密度梯度精细调整样本。
- **联合微调VAE的尝试**：在EBM训练阶段额外最小化$D_{\mathrm{KL}}(p_{\theta}||h_{\psi,\theta})$损失以更新解码器，并未带来性能提升（FID 14.0 vs. 12.96），说明固定预训练VAE的两阶段策略已足够有效，且避免了联合训练的优化不稳定性。

### 采样效率

VAEBM在生成速度上具有显著优势。在CIFAR-10上生成50个样本，VAEBM仅需8.79秒，而基于分数的模型NCSN需要107.9秒（Section 5.5）。这一加速归因于VAEBM仅需运行短链Langevin动力学（通常16步），且采样在低维噪声空间进行，避免了像素空间中昂贵的梯度计算。

### 模式覆盖与分布外检测

**Table 5** 展示了VAEBM在StackedMNIST上的模式覆盖能力：VAEBM实现了全部1000个模式的覆盖，KL散度仅为0.087，证明共生模型有效结合了VAE捕获全局模态结构的能力与EBM精炼局部细节的优势。

在分布外（OOD）检测任务上，**Table 6** 显示VAEBM在CIFAR-10作为分布内数据集、SVHN作为OOD数据集时，AUROC达到0.83，远超NVAE的0.42。这表明能量函数为分布内样本赋予更高似然，为OOD样本赋予更低似然，使模型具备了实用的不确定性估计能力。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/010_Table_6.jpg]]
*Table 6: Table for AUROC↑ of log p(x) computed on several OOD datasets. In-distribution dataset is CIFAR-10. Interp. corresponds to linear interpolation between CIFAR-10 images*

### 关键定性观察

**Figure 2** 可视化了CIFAR-10上MCMC采样链的演化过程：初始样本来自预训练NVAE，存在模糊和伪影；经过16步Langevin动力学后，样本细节显著锐化，背景噪声被清除。**Figure 5** 及附录B.1揭示了在噪声空间中进行MCMC并适当调整步长的决定性作用——若步长不当或直接在(x,z)空间采样，样本会出现严重失真或无法收敛。**Figure 6** 的直方图显示，VAEBM为训练集和测试集图像分配的未归一化对数似然分布高度重叠，表明模型未过拟合训练数据，具有良好的泛化性。

### 失败模式与局限

尽管VAEBM大幅提升了VAE的生成质量，论文明确指出了若干局限：

- **长链混合困难**：Langevin动力学在长链下混合缓慢，样本倾向于停留在局部模式，无法有效遍历不同模态。这限制了模型在需要多样性和模式间插值的场景中的表现。
- **复杂数据集上的质量差距**：在CelebA HQ 256上，VAEBM的FID（20.38）仍落后于当时最先进的GAN（如PGGAN），表明对于高分辨率、高细节的图像，共生模型的生成保真度仍有提升空间。
- **训练停止依赖人工判断**：能量函数的训练没有自动收敛准则，需要研究者手动观察生成样本质量来停止训练，否则可能过度拟合导致样本失真。这引入了研究者偏差，并限制了方法的可复现性和自动化程度。
- **两阶段训练未充分释放潜力**：固定VAE训练EBM的策略虽简化了优化，但未能联合微调两个组件，可能限制了模型最终性能的上限。附录C.2的初步尝试表明联合训练未带来增益，但更先进的联合优化策略仍有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/014_Figure.jpg]]
*Figure: (a) Step size 8e-4 (b) Step size 8e-5*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/022_Figure_9.jpg]]
*Figure 9: Additional visualizations of MCMC chains when sampling from the model for CIFAR-10*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/019_Figure.jpg]]
*Figure: (a) NVAE baseline (b) WGAN, initialized with NVAE decoder (c) EBM on x, MCMC initialized with NVAE samples (d) VAEBM with DKL(pθ0 (x)||hψ,θ(x)) loss*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/007_Table.jpg]]

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/008_Table_5.jpg]]
*Table 5: Mode coverage on StackedMNIST*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/009_Table_4.jpg]]
*Table 4: Comparison for IS and FID on CIFAR-10 between several related training methods*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/017_Table_7.jpg]]
*Table 7: Network structures for the energy function $E _ { \psi } ( \mathbf { x }$ )

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2010_00654/figures/018_Table_8.jpg]]
*Table 8: Important hyper-parameters for training VAEBM*

## 方法谱系与知识库定位

### 1. 方法沿革与基线关系

VAEBM 处于显式似然生成模型（VAE、EBM）与隐式模型（GAN）的交汇点，其核心动机在于克服两类模型各自的根本性缺陷：VAE 倾向于将高概率分配给数据空间中的非数据区域，导致生成样本模糊；纯 EBM 则在像素空间中依赖 MCMC 采样，混合缓慢且计算成本高昂。VAEBM 通过将 VAE 的生成分布与 EBM 的能量函数相乘，构建共生模型，在保留显式似然框架的同时，显著提升了样本质量。

**与 VAE 基线的关系**：VAEBM 直接以 **NVAE**（Vahdat & Kautz, NeurIPS 2020）作为其 VAE 生成器组件，这是当时最先进的 VAE 架构。在 CIFAR-10 上，NVAE 的 FID 为 51.67，IS 为 5.51；VAEBM 将 FID 降至 12.19，IS 提升至 8.43（Table 1）。在 CelebA 64 上，FID 从 14.74 降至 5.31（Table 2）；在 LSUN Church 64 上，FID 从 41.3 降至 13.51；在 CelebA HQ 256 上，FID 从 45.11 降至 20.38（Table 3）。这种改进并非来自 VAE 架构的修改，而是源于能量函数对 VAE 解码器输出的精炼——能量网络显式地降低了非数据区域的概率，使样本细节更加清晰。

**与纯 EBM 基线的关系**：VAEBM 与 **IGEBM**（Du & Mordatch, ICML 2019）形成直接对比。IGEBM 在像素空间中运行 Langevin 动力学，需要长链才能混合，且样本质量受限于高维空间中的 MCMC 效率。VAEBM 的关键创新在于将 MCMC 采样重新参数化到噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$ 中，利用 VAE 学到的低维流形结构加速混合。实验表明，仅在 $\mathbf{x}$ 空间定义 EBM 的变体 FID 高达 48.89，而 VAEBM 在增强空间 $(\mathbf{x}, \mathbf{z})$ 中采样可将 FID 降至 12.96（Table 4），验证了潜在空间辅助采样的必要性。

**与基于分数的生成模型的关系**：**NCSN**（Song & Ermon, NeurIPS 2019）同样使用 Langevin 动力学采样，但需要大量迭代步骤（CIFAR-10 上约 1000 步）。VAEBM 仅需 16 步即可生成高质量样本，生成速度优势显著：在 CIFAR-10 上，VAEBM 生成 50 个样本需 8.79 秒，而 NCSN 需 107.9 秒（Section 5.5）。这归因于 VAE 先验提供了一个接近数据分布的初始化点，使得 MCMC 链只需进行局部精炼，而非从纯噪声开始探索整个数据空间。

**与 GAN 基线的关系**：VAEBM 在多个基准上接近或达到 GAN 的性能水平。在 CIFAR-10 上，**SNGAN**（Miyato et al., ICLR 2018）的 FID 为 21.7，VAEBM 为 12.19；在 CelebA 64 上，VAEBM 的 FID 为 5.31，与当时最佳 GAN 可比（Table 2）。值得注意的是，论文还尝试了用 WGAN 对抗训练替代 EBM 的变体（WGAN initialized with NVAE decoder），其 FID 为 20.39，显著劣于 VAEBM 的 12.96（Table 4），表明能量函数的细粒度梯度信号比判别器损失更适合精炼 VAE 输出。

### 2. 核心设计决策的消融证据

**采样空间选择**：在噪声变量空间 $(\epsilon_{\mathbf{z}}, \epsilon_{\mathbf{x}})$ 中进行 MCMC 是 VAEBM 成功的关键。Appendix B.1 和 Figure 5 显示，直接在 $(\mathbf{x}, \mathbf{z})$ 空间采样无法产出好样本，即使调整步长也难以获得合理结果。噪声空间中的重新参数化使得 Langevin 动力学可以在各向同性的标准高斯基底上运行，步长可以统一设置，自动根据 VAE 学到的方差进行调整，避免了逐变量调参的复杂性。

**两阶段训练策略**：VAEBM 采用先训练 VAE、再固定 VAE 训练 EBM 的策略（Section 3.1），这简化了优化过程，避免了两者联合训练的不稳定性。消融实验（Appendix C.2）表明，额外最小化 $D_{\mathrm{KL}}(p_{\theta}||h_{\psi,\theta})$ 损失以更新解码器并不会提高性能（FID 14.0 vs 12.96），支持了固定 VAE 的合理性。然而，这也意味着 VAE 的缺陷（如某些模态的遗漏）无法被后续训练纠正，构成了模型的固有上限。

**能量网络正则化**：VAEBM 使用权重归一化（Weight Normalization）及数据相关初始化，激活函数采用 Swish，替代了纯 EBM 中常用的谱归一化（Spectral Normalization）（Appendix E）。这一选择与两阶段训练中能量网络仅需在 VAE 输出附近进行局部校正的需求相匹配。

### 3. 适用边界与局限

**采样混合的局限**：尽管 VAEBM 在噪声空间中加速了 MCMC，长链 Langevin 动力学仍然混合缓慢，样本倾向于停留在局部模式，难以遍历不同模态。在 StackedMNIST 上，VAEBM 虽实现了 1000 模式的全覆盖（KL 散度 0.087，Table 5），但在更复杂的数据集上，模态间的遍历能力仍受限于 MCMC 的固有缺陷。

**高分辨率生成的差距**：在 CelebA HQ 256 上，VAEBM 的 FID 为 20.38，仍落后于当时最先进的 GAN（如 PGGAN）。论文指出，为获得更好的视觉质量，需要使用低温度（$t=0.7$）的 NVAE 样本初始化 MCMC 链，且需要对生成样本进行人工筛选以展示多样性（Figure 3 caption），这暗示模型在无条件生成高分辨率图像时的一致性和多样性仍有不足。

**训练停止的依赖**：能量网络的训练需要人工观察生成样本质量来判断停止时机，否则可能过度拟合导致失真。这一过程引入了研究者偏差，使得训练流程难以完全自动化，限制了方法的可复现性和规模化应用。

**两阶段训练的固有限制**：固定 VAE 虽然简化了优化，但也意味着 VAE 的生成分布上限决定了 VAEBM 的上限。VAE 遗漏的模态或结构偏差无法被 EBM 完全补偿，因为 EBM 仅在 VAE 输出的邻域内进行精炼。

### 4. 开放问题与后续方向

- **更先进的 MCMC 方法**：能否使用 Hamiltonian Monte Carlo (HMC) 或其他更高效的采样器来改善混合，支持更长链而不会导致模式坍缩？
- **跨模态扩展**：VAEBM 框架是否可扩展到文本、音频等其他模态？在这些领域中，VAE 的潜在空间结构和 EBM 的能量函数设计需要如何调整？
- **自动化收敛检测**：如何自动检测能量网络训练的收敛或过拟合，而不依赖人工判断生成样本质量？
- **条件生成与可控编辑**：能否将条件生成或可控属性编辑纳入共生模型，在保持生成质量的同时实现对特定属性的精确控制？
- **联合微调策略**：是否存在稳定联合微调 VAE 和 EBM 的方法，在不引入训练不稳定性的前提下，进一步提升模型潜力？

## 原文 PDF

![[paperPDFs/ICLR_2021/VAEBM_A_Symbiosis_between_Variational_Autoencoders_and_Energy_based_Models.pdf]]
