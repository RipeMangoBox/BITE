---
title: Generative Diffusion Priors for 3D Mapping of the Dark Universe
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generative_Diffusion_Priors_for_3D_Mapping_of_the_Dark_Universe.pdf
project_link: null
code_link: null
aliases:
- CDD3WL
- GDP3MDU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 使用从高保真N体模拟Conicus3D中学习的数据驱动扩散模型先验，配合可微的物理前向模型，通过改进的DAPS后验采样框架，使重建密度场既能满足观测约束又保持宇宙学模拟的统计特性。
primary_logic: 利用先进宇宙学模拟构建大规模三维光锥数据集，训练红移条件扩散模型作为结构形成的强先验；将该先验与弱透镜线性前向模型集成到解耦退火后验采样框架，实现三维密度场的贝叶斯后验采样，从而在噪声观测下恢复高保真度、统计一致的宇宙网结构。
claims:
- 重建的二维收敛场和三维密度场与真实模拟的Pearson相关系数显著高于Wiener滤波器和Neural Ensemble基线。
- 后验样本的角功率谱和径向功率谱与真实模拟一致，避免了基线的过度平滑和虚假视线相关性。
- 在宇宙学参数不匹配（OOD）的情况下，后验样本仍然匹配真实功率谱，表明方法对先验错误具有鲁棒性。
- "Simulated JWST-scale lightcone volume 1 上 ρ^{2D} (↑) = 0.87"
---

# Generative Diffusion Priors for 3D Mapping of the Dark Universe

> [!tip] 核心洞察
> 利用先进宇宙学模拟构建大规模三维光锥数据集，训练红移条件扩散模型作为结构形成的强先验；将该先验与弱透镜线性前向模型集成到解耦退火后验采样框架，实现三维密度场的贝叶斯后验采样，从而在噪声观测下恢复高保真度、统计一致的宇宙网结构。

| 字段 | 内容 |
|------|------|
| 中文题名 | 暗宇宙三维映射的生成式扩散先验 |
| 英文题名 | Generative Diffusion Priors for 3D Mapping of the Dark Universe |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_Generative_Diffusion_Priors_for_3D_Mapping_of_the_Dark_Universe_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | 基于Conicus3D扩散先验的解耦退火后验采样（Diffusion-DAPS for 3D Weak Lensing） |
| Dataset | Simulated JWST-scale lightcone volume 1, Simulated JWST-scale lightcone volume 2, Simulated JWST-scale lightcone volume 3 |

> [!tip] 效果简介
> - Simulated JWST-scale lightcone volume 1 上，ρ^{2D} (↑) 0.87 vs Neural: 0.86, Wiener: 0.77 (+0.01 / +0.10)；ρ_{blur}^{3D} (↑) 0.83 vs Neural: 0.79, Wiener: 0.71 (+0.04 / +0.12)。
> - Simulated JWST-scale lightcone volume 2 上，ρ^{2D} (↑) 0.88 vs Neural: 0.87, Wiener: 0.83 (+0.01 / +0.05)；ρ_{blur}^{3D} (↑) 0.83 vs Neural: 0.80, Wiener: 0.72 (+0.03 / +0.11)。
> - Simulated JWST-scale lightcone volume 3 (OOD cosmology) 上，ρ^{2D} (↑) 0.98 vs Neural: 0.96, Wiener: 0.92 (+0.02 / +0.06)。

## 概述

**问题背景** 弱引力透镜效应通过测量背景星系形状的微弱相干畸变，提供了直接探测宇宙三维物质分布的关键探针。然而，从噪声主导的剪切观测中重建暗物质密度场是一个病态逆问题：形状噪声通常比剪切信号大两个数量级以上，且三维反演面临严重的视线方向简并性。

**核心瓶颈** 现有方法依赖手工设计的平滑先验（如高斯先验下的Wiener滤波）或单一视角的神经网络集成，无法捕捉宇宙网的非高斯、纤维状结构，且缺乏严格的贝叶斯不确定性量化。这些方法在噪声功率超过信号功率的小尺度上会过度平滑，并引入虚假的视线方向相关性。

**本文方案** 本文提出基于扩散模型的贝叶斯后验采样框架，核心思路是将先进N体模拟作为数据驱动先验的来源：从AbacusSummit模拟构建大规模三维光锥数据集**Conicus3D**，训练红移条件扩散模型以学习物质密度场的统计分布；随后将该先验与可微的弱透镜物理前向模型集成到改进的**DAPS**（解耦退火后验采样）框架中，实现三维密度场的严格贝叶斯后验采样。

**主要结果** 在模拟JWST COSMOS-Web巡天条件下，该方法在二维收敛场和三维密度场的重建精度上均显著优于Wiener滤波器和神经网络集成基线（Pearson相关系数提升0.01–0.12，Table 1）。后验样本的角功率谱和径向功率谱与真实模拟一致，且在宇宙学参数不匹配（分布外）的情况下仍能通过似然引导匹配真实功率谱（Figure 5），展现出对先验错误的有效鲁棒性。不确定性校准分析表明，后验样本标准差与实际误差高度相关（r=0.92，Figure 6），验证了贝叶斯框架的可靠性。

**方法定位** 该方法属于“模拟驱动先验 + 物理引导后验采样”的技术路线，将宇宙学模拟的统计知识以扩散模型形式编码为先验，通过可微前向模型和傅里叶对角协方差将物理约束注入采样过程，为三维弱透镜质量映射提供了兼具高保真度与严格不确定性的新范式。

## 背景与动机

**暗物质质量映射的核心挑战。** 暗物质占据宇宙物质总量的约 85%，其三维分布是理解结构形成和约束宇宙学参数的关键。弱引力透镜效应——前景物质对背景星系形状的微小扭曲——是目前绘制暗物质分布最有力的探针之一。这一反演问题的本质是：从被形状噪声严重污染的二维剪切观测中，重建三维密度场 $\delta$，其中形状噪声的幅度通常比透镜信号大两个数量级以上（Figure 2）。

**现有方法的瓶颈。** 当前主流的三维弱透镜质量映射方法存在根本性局限。基于解析先验的方法（如 **Wiener 滤波**，Simon et al., MNRAS 2009）依赖高斯平滑假设，无法捕捉宇宙网的非高斯、纤维状结构，导致重建结果过度平滑、小尺度功率严重衰减。基于深度学习的方法（如 **Neural Ensemble**，Zhao et al., ICLR 2025）虽然通过神经网络集成提供了近似后验，但其先验本质上是单一视角的隐式表征，缺乏对三维宇宙结构多尺度统计特性的完整建模能力，且难以提供严格的贝叶斯不确定性量化。

**核心洞察与动机。** 本文的核心洞察在于：高保真 N 体宇宙学模拟（如 AbacusSummit）已经能够生成高度逼真的三维暗物质光锥数据，这些模拟蕴含了结构形成的完整统计规律——包括非线性坍缩、纤维状网络和多尺度耦合。如果能将这些模拟转化为数据驱动的强先验，并与可微的物理前向模型统一到贝叶斯后验采样框架中，就有可能在噪声观测下恢复既满足数据约束、又保持宇宙学统计一致性的三维密度场。这一思路将质量映射问题从“手工设计先验”转变为“从物理模拟中学习先验”，有望突破现有方法的精度与不确定性量化瓶颈。

## 核心创新

本文的核心创新在于将**数据驱动的扩散模型先验**与**可微物理前向模型**统一到贝叶斯后验采样框架中，从而突破现有三维弱透镜质量映射方法的两大瓶颈：先验表达能力的不足与不确定性量化的缺失。

### 从手工先验到宇宙学模拟驱动的扩散先验

传统三维质量映射方法依赖手工设计的平滑先验。**Wiener滤波**（Simon et al., MNRAS 2009）隐含地假设密度场服从高斯分布，重建结果在噪声主导的小尺度上过度平滑，无法恢复宇宙网的纤维状结构与非高斯特征。**Neural Ensemble**（Zhao et al., ICLR 2025）虽引入深度学习，但其本质是训练多个神经网络给出点估计的集成，提供的仅是近似的后验均值和方差，而非严格的贝叶斯后验样本。

本文的关键突破在于**用从高保真N体模拟中学习到的扩散模型取代手工先验**。具体而言，作者基于AbacusSummit模拟构建了**Conicus3D**三维光锥数据集，并训练了一个**红移条件扩散模型**来学习各透镜平面的物质密度分布 $p(\delta^{(z)}|z)$。该先验能够捕捉宇宙学模拟中暗物质晕的层次聚集、纤维状网络以及多尺度功率谱等复杂统计特性——这些是高斯或稀疏先验无法表征的。

这一改变在因果机制上产生了根本性差异：Wiener滤波的先验仅提供功率谱水平的二阶统计约束，Neural Ensemble的先验隐式编码在有限训练样本中且缺乏严格的概率解释；而扩散先验通过去噪得分匹配学习到了密度场的完整分布，使得后验采样能够在满足观测似然的同时，保持与真实宇宙学模拟一致的样本级统计特性。

### 从点估计到解耦退火后验采样

第二个核心创新在于**后验推断方式的根本转变**。Wiener滤波给出的是最大后验点估计，Neural Ensemble提供的是多个确定性预测的经验均值和方差——两者都无法产生严格的贝叶斯后验样本，因而无法进行完整的不确定性传播。

本文改进并应用了**解耦退火后验采样**（DAPS）框架，将扩散先验与弱透镜物理前向模型统一为可微分的后验采样过程。该框架的核心机制是：

1. **似然梯度**通过可微前向模型 $e_{\mathrm{obs}} = \mathbf{P}\mathbf{Q}\delta + \varepsilon$ 反向传播，确保重建密度场与观测剪切数据一致；
2. **先验梯度**由扩散模型的得分函数 $\nabla_{\delta} \log p(\delta)$ 提供，将采样引向符合宇宙学模拟统计的密度场区域；
3. **物理信息协方差** $\mathbf{\Sigma} = \mathbf{F}^{-1} \mathrm{diag}(P_k) \mathbf{F}$ 基于物质功率谱在傅里叶空间对角化，为退火过程提供了符合宇宙学先验的扰动结构。

这一设计的直接后果是：方法能够产生**多样化的后验样本**，而非单一点估计。如Figure 5左图所示，本文方法的后验样本在角功率谱 $C_\kappa^\ell$ 上准确保留了小尺度（高$\ell$）功率，而两个基线在噪声功率超过信号功率的尺度上均出现过度平滑。更为关键的是，Figure 5中图的径向功率谱表明，本文样本在不同红移平面之间近乎平坦，避免了Neural Ensemble输出中虚假的视线相关性——这直接源于扩散先验对透镜平面之间统计独立性的正确建模。

### 先验错误鲁棒性：似然引导的自适应机制

一个值得注意的创新副产品是方法对**先验错误的内在鲁棒性**。如Figure 5右图所示，当真实宇宙学参数与训练先验不匹配时（无质量中微子情形，真实功率谱显著高于先验预期），后验样本仍能匹配真实功率谱。这一能力的因果机制在于：DAPS采样器中的似然梯度项会“修正”先验的偏差，将采样引向与观测数据一致的密度场区域。换言之，**似然作为锚点，防止了先验错误完全主导重建结果**——这是点估计方法或纯先验驱动方法所不具备的特性。

### 创新边界与待验证问题

上述创新的有效性依赖于一个关键前提：N体模拟能够准确反映真实宇宙的统计特性。若模拟存在系统性偏差，扩散先验学习的分布将与真实宇宙产生偏移，似然修正的能力也可能存在上限。此外，扩散采样的计算成本未在文中明确量化，这可能限制其在平方公里级巡天数据上的直接应用。这些构成了当前创新边界上的开放问题。

## 整体框架

本文提出了一套将扩散生成先验与可微物理前向模型统一于贝叶斯后验采样的三维弱透镜质量映射框架。其核心逻辑是：利用高保真N体模拟学习暗物质密度场的非高斯统计分布作为数据驱动先验，随后将该先验嵌入到已知的弱透镜测量似然中，通过改进的解耦退火后验采样（DAPS）方案生成三维密度场的后验样本。该流程由四个关键模块串联构成，形成从模拟数据构建到最终后验推断的完整链路。

### 1. Conicus3D数据集构建

框架的起点是一个专为三维弱透镜质量映射设计的大规模光锥数据集 **Conicus3D**。该数据集从 **AbacusSummit** 高精度N体模拟中提取暗物质粒子信息，沿过去光锥按共动距离切片生成一系列透镜平面（lens planes），每个平面记录对应红移处的物质过密度场 $\delta^{(z)}$。这种切片表示将三维宇宙网结构自然地分解为红移条件化的二维场，既保留了沿视线方向的演化信息，又为后续二维扩散模型的训练提供了结构化样本。

### 2. 红移条件扩散先验

在Conicus3D之上，框架训练一个**红移条件化的去噪扩散概率模型（DDPM）**来学习每个透镜平面的先验分布 $p(\delta^{(z)} \mid z)$。具体而言，该模型采用标准U-Net架构，在 $128 \times 128$ 的透镜平面图像上运行，通过将红移编码为one-hot条件向量注入去噪过程，使单一模型能够捕捉从低红移到高红移的全部统计特性。训练完成后，该扩散模型可以生成与真实N体模拟统计一致的物质过密度场，从而充当三维结构形成的强先验——既能保留纤维状宇宙网的多尺度形态，又能刻画非高斯密度分布。

### 3. 弱透镜前向模型

先验定义了密度场的合理分布空间，而观测约束则由一个可微的**线性弱透镜前向模型**提供。该模型分为两个子步骤：

- **投影算子 $\mathbf{Q}$**：将三维物质过密度场沿视线方向积分，得到二维收敛场 $\kappa$：
  $$\kappa(\pmb{\theta}, w) = \mathbf{Q}\delta = \frac{3 H_0^2 \Omega_m}{2 c^2} \int_0^w dw' \frac{w'(w-w')}{w} \frac{\delta(w'\pmb{\theta}, w')}{a(w')}$$

- **卷积算子 $\mathbf{P}$**：将收敛场通过复核 $\mathcal{D}(\pmb\theta) = -1/(\theta^*)^2$ 的二维卷积转换为剪切场 $\gamma$：
  $$\gamma(\pmb\theta, w) = \mathbf{P}\kappa = \frac{1}{\pi} \int_{\mathbb{C}^2} d^2\pmb\theta' \mathcal{D}(\pmb\theta - \pmb\theta') \kappa(\pmb\theta', w)$$

最终的观测似然将剪切场与形状噪声叠加：$e_{\mathrm{obs}} = \mathbf{P}\mathbf{Q}\delta + \varepsilon$，其中 $\varepsilon \sim \mathcal{N}(0, \sigma_{\mathrm{shape}})$。整个前向模型保持可微性，这是后续基于梯度的后验采样的必要条件。

### 4. 改进的DAPS后验采样器

框架的推理核心是**改进的DAPS（Decoupled Annealing Posterior Sampling）采样器**。给定剪切观测 $\gamma$，目标是从后验分布中采样：
$$p(\delta \mid \gamma) \propto p(\gamma \mid \delta) \, p(\delta)$$

DAPS将扩散先验的分数估计 $\nabla_{\delta} \log p(\delta)$ 与似然梯度 $\nabla_{\delta} \log p(\gamma \mid \delta)$ 解耦，在退火过程中交替施加先验引导和观测约束。本文的关键改进在于引入了一个基于物质功率谱 $P(k)$ 的**物理信息协方差矩阵**，该矩阵在傅里叶空间对角化：
$$\pmb{\Sigma} = \pmb{F}^{-1} \, \mathrm{diag}(P_k) \, \pmb{F}$$

这一设计使得采样过程中的噪声调度与宇宙学结构形成的真实尺度分布保持一致，从而在满足观测似然的同时，生成与N体模拟统计特性一致的后验样本。

### 输入输出流

整体框架的输入输出流可概括为：

- **输入**：模拟或实测的星系形状目录（椭圆率测量），附带红移信息与形状噪声估计。
- **处理**：形状目录经前向模型的逆过程转化为对密度场的似然约束；扩散先验提供密度场的生成式正则化；DAPS采样器在两者之间迭代协调。
- **输出**：三维物质过密度场的后验样本集合，每个样本是一个完整的 $128 \times 128 \times M$ 光锥体（$M$ 为透镜平面数）。这些样本可直接用于点估计（后验均值）、不确定性量化（体素级标准差），以及下游宇宙学统计推断（如峰值计数、空隙统计、功率谱分析）。

该框架的关键优势在于其**模块化解耦设计**：先验训练仅需模拟数据，前向模型仅依赖物理定律，采样器则作为通用接口将两者统一。这意味着当更精确的N体模拟或更复杂的观测似然可用时，各模块可独立升级而无需重构整体流程。

### 补充图表

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/001_Figure_1.jpg]]
*Figure 1: Lightcone structure and redshift-conditional diffusion model. Left: The large-scale matter distribution is represented as a 3D lightcone, built from a sequence of lens planes slicing the dark matter density field at increasing comoving distance (redshift). Right: Each lens plane is modeled with a redshift-conditional 2D diffusion prior that learns the statistics of simulated overdensity maps at that redshift. During generation, we start from Gaussian noise on each plane, append one-hot redshift encodings, and denoise with a U-Net score model to obtain a coherent 3D lightcone. This redshift-conditioned factorization enables efficient generation of realistic volumetric dark matter fields cons...*

## 核心模块与公式推导

### 弱透镜前向模型

弱透镜测量建立在剪切可加性的近似之上。星系的内禀椭圆率 $e_{\mathrm{int}}$ 与观测椭圆率 $e_{\mathrm{obs}}$ 之差即为剪切 $\gamma$：

$$e_{\mathrm{obs}} - e_{\mathrm{int}} = \gamma$$

其中复椭圆率的大小与相位由轴比 $r$ 和方位角 $\phi$ 定义：

$$|e| = \frac{1-r}{1+r} \qquad \angle e = 2\phi$$

收敛场 $\kappa$ 是物质密度扰动 $\delta$ 沿视线方向的加权投影：

$$\kappa(\pmb{\theta}, w) = \mathbf{Q}\delta = \frac{3 H_0^2 \Omega_m}{2 c^2} \int_0^w dw' \frac{w'(w-w')}{w} \frac{\delta(w'\pmb{\theta}, w')}{a(w')}$$

剪切场由收敛场通过二维卷积得到：

$$\gamma(\pmb\theta, w) = \mathbf{P}\kappa = \frac{1}{\pi} \int_{\mathbb{C}^2} d^2\pmb\theta' \mathcal{D}(\pmb\theta - \pmb\theta') \kappa(\pmb\theta', w)$$

其中 $\mathcal{D}(\theta) = -1/(\theta^*)^2$ 为复核。完整的前向模型将观测椭圆率表示为密度扰动经投影和卷积后叠加高斯形状噪声：

$$e_{\mathrm{obs}} = \mathbf{P}\mathbf{Q}\delta + \varepsilon \qquad \varepsilon \sim \mathcal{N}(0, \sigma_{\mathrm{shape}})$$

### Conicus3D 数据集构建

从 AbacusSummit 高保真 N 体模拟中生成暗物质光锥，沿共动距离（红移）方向切分为一系列透镜平面。每个透镜平面对应一个二维密度扰动场 $\delta^{(z)}$，构成三维光锥体积。数据集参数匹配 JWST COSMOS-Web 巡天：足迹 0.54 deg²、星系面密度约 261 arcmin⁻²、形状噪声 $\sigma_e \approx 0.25$、测光红移散布 $\sigma_z = 0.11(1+z)$。

### 红移条件扩散先验

在 Conicus3D 上训练条件扩散模型，学习各透镜平面的先验分布 $p(\delta^{(z)}|z)$。扩散模型采用标准 DDPM UNet 架构，在 $128 \times 128$ 透镜平面图像上运行，以红移作为条件输入。该先验捕捉了宇宙网的非高斯纤维状结构和多尺度统计特性，避免了手工设计平滑先验的过度平滑问题。

### 改进的 DAPS 后验采样器

目标是采样密度场的贝叶斯后验分布：

$$p(\delta | \gamma) \propto p(\gamma | \delta) p(\delta)$$

其中 $p(\gamma|\delta)$ 为上述弱透镜前向模型定义的似然，$p(\delta)$ 为扩散模型学习的数据驱动先验。改进的 DAPS（Decoupled Annealing Posterior Sampling）框架将扩散先验的得分函数 $\nabla_{\delta} \log p(\delta)$ 与似然梯度统一，在采样过程中逐步退火。为稳定高维反演，引入基于物质功率谱 $P(k)$ 的物理信息协方差矩阵：

$$\pmb{\Sigma} = \pmb{F}^{-1} \mathrm{diag}(P_k) \pmb{F}$$

该矩阵在傅里叶空间对角化，为采样过程提供尺度感知的正则化，使重建密度场既满足观测约束又保持宇宙学模拟的统计特性。

### 补充图表

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/002_Figure_2.jpg]]
*Figure 2: Weak Lensing Measurements. (Left) As light from distant galaxies propagates through the universe, it is deflected by intervening matter, producing small differences between the intrinsic (unlensed) shape*

## 实验与分析

### 实验设定

为验证方法在实际巡天条件下的表现，实验设定严格参照JWST COSMOS-Web巡天的关键参数：天区面积0.54 deg²，平均红移源星系密度约261 arcmin⁻²，内禀形状噪声弥散σ_e ≈ 0.25，测光红移散布σ_z = 0.11(1+z)（高斯形式）。这一设定确保形状噪声比剪切信号高出两个数量级以上，使弱透镜信号提取具有真实的挑战性。

评估数据来自三个模拟JWST尺度光锥体积，其中两个与扩散先验训练的基准宇宙学一致，第三个采用无质量中微子的偏移宇宙学参数，用于测试分布外（OOD）泛化能力。对比基线包括两个公开可用的三维质量映射方法：解析形式的**Wiener滤波器重建**（Simon et al., MNRAS 2009），依赖高斯先验；以及**神经网络集成估计器**（Zhao et al., ICLR 2025），通过集成网络提供近似不确定性。

### 二维与三维重建精度

Table 1汇总了三个模拟光锥体积上的重建质量定量对比，采用Pearson互相关系数作为核心指标。ρ²ᴰ衡量投影收敛场κ的点估计质量，ρ_{blur}³ᴰ衡量经视线方向高斯平滑（σ = 4透镜平面）后的三维过密度场质量。

在两个分布内体积上，本文方法在二维收敛场重建上取得ρ²ᴰ = 0.87和0.88，分别优于神经网络集成的0.86和0.87，以及Wiener滤波的0.77和0.83。三维重建的优势更为显著：ρ_{blur}³ᴰ = 0.83（两体积均为0.83），而神经网络集成为0.79和0.80，Wiener滤波仅为0.71和0.72。这一差距表明数据驱动扩散先验有效捕捉了宇宙网的非高斯纤维状结构，而高斯先验和集成近似均导致过度平滑。

在分布外体积上，本文方法表现出更强的鲁棒性：ρ²ᴰ = 0.98（神经网络集成0.96，Wiener滤波0.92），ρ_{blur}³ᴰ = 0.92（神经网络集成0.86，Wiener滤波0.84）。尽管先验训练于不同的宇宙学参数，似然引导使后验采样仍能追踪真实密度场结构。

Figure 3和Figure 4分别展示了二维和三维重建的可视化对比。在二维收敛图上，本文方法恢复了锐利的星系团峰值和纤维状结构，与真实κ图高度吻合，而基线方法在高密度区域对比度明显降低。在三维过密度场上，本文方法准确地将结构放置在正确的红移切片上，而基线方法倾向于沿视线方向涂抹过密度区或丢失小尺度特征。在宇宙学失配的第三个体积上，本文方法仍能忠实追踪真实三维结构。

### 样本质量与统计保真度

Figure 5从功率谱角度评估后验样本的统计质量。左图展示收敛场κ的角功率谱C_κ^ℓ：本文样本保留了正确的高ℓ（小尺度）功率，而神经网络集成和Wiener滤波在噪声功率超过信号功率的区域过度平滑小尺度模。中心图展示过密度场δ的径向功率谱：本文样本近乎平坦，表明不同红移平面之间解相关，避免了神经网络集成输出中出现的虚假视线相关性。这一性质对于下游非线性统计量（如峰值计数、空隙统计）的无偏宇宙学推断至关重要。

右图测试分布外泛化：当真实宇宙学与训练宇宙学匹配时，先验样本和重建样本再现相同的功率谱；在无质量中微子的OOD情形下，真实功率显著更高，但本文后验样本仍匹配真实谱，证明似然引导使方法能适应观测宇宙，即使先验宇宙学存在误设。

### 不确定性校准

Figure 6评估后验样本的不确定性校准质量。对每个体素，计算后验样本的标准差（"样本标准差"）与后验均值相对于真实值的平均绝对误差（MAE）。按样本标准差分箱后，绘制每箱的平均MAE及体素占比。本文方法的样本标准差与实际误差之间的相关系数r = 0.92，与神经网络集成估计器的r = 0.90相当，但关键区别在于本文样本对应严格定义的贝叶斯后验分布，而非集成的近似不确定性。

### 失败模式与局限性

尽管方法在定量指标和视觉质量上均显著优于基线，仍需注意以下局限：第一，重建质量依赖于N体模拟的保真度，若Conicus3D未能准确反映真实宇宙的统计特性，先验偏差将传播至后验推断。第二，对极端宇宙学偏移或使用不同模拟代码（如不同子网格物理模型）的影响尚未充分研究。第三，扩散采样过程的计算成本未明确报告，可能限制其直接应用于千万星系量级的特大巡天数据。上述局限需在实际部署前通过更大规模测试和采样加速策略加以验证。

### 补充图表

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/003_Figure_3.jpg]]
*Figure 3: Two-dimensional mass reconstruction results from simulated WL data. For three representative lightcone volumes (rows), we show the projected convergence (κ) maps for the ground truth, our method, the Neural Ensemble baseline, and the Wiener filter reconstruction (columns); for each method, we use the posterior mean as a point estimate. Our reconstructions recover sharp cluster peaks and filamentary features that closely match the true κ maps, while the baselines exhibit oversmoothing and reduced contrast in high-density regions. The third row highlights performance under a cosmology mismatch; even in this out-of-distribution setting, our method maintains high-fidelity 2D mass reconstruction...*

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/004_Figure_4.jpg]]
*Figure 4: Three-dimensional mass reconstruction results from simulated WL data. Each row corresponds to a different simulated lightcone volume, and columns compare the ground-truth overdensity field to reconstructions from our diffusion-based posterior sampler, the Neural Ensemble baseline [46], and the Wiener filter method [39]; for each method, we use the posterior mean as a point estimate. Our reconstructions better recover the spatial morphology of clusters and filaments and place structures at the correct redshift slices, whereas the baselines tend to smear overdensities along the line of sight or miss small-scale features. The third row illustrates the challenging case of a misspecified cosmolo...*

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/006_Figure_5.jpg]]
*Figure 5: Sample quality. Our diffusion-based posterior sampler produces 3D mass-field realizations whose statistics match those of realistic dark matter simulations. Left: Angular PS Cκℓ of the convergence κ for individual samples. Our samples retain the correct high-ℓ (small-scale) power, whereas the Neural Ensemble [46] and Wiener filter [39] baselines over-smooth small-scale modes when the noise power exceeds the signal power and the reconstruction becomes prior-dominated. Center: Radial PS of the overdensity δ across lens planes. Our samples are nearly flat in this radial spectrum, indicating decorrelation between different redshift planes and avoiding the spurious line-of-sight correlations see...*

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of reconstruction quality. We summarize 3D and 2D mass-mapping performance for three simulated JWST-scale lightcone volumes. We report the Pearson crosscorrelation coefficients averaged over lensplanes between reconstructed and ground-truth maps*

![[assets/figures/papers/paper_list_l2501_https_openaccess_thecvf_com_content_CVPR2026_html_Zhao_Generative_Diffus/figures/008_Figure_6.jpg]]
*Figure 6: Uncertainty calibration. For each voxel, we compute the standard deviation of the posterior samples (“sample std”) and the mean absolute error (MAE) between the posterior mean and the ground truth. We then bin voxels by sample std and plot the average MAE per bin, along with the fraction of voxels in each bin. Both our method (r = 0.92) and the neural ensemble estimator (r = 0.90) [46] show a strong correlation between predicted uncertainty and actual error, but only our samples correspond to a well-defined Bayesian posterior distribution*

## 方法谱系与知识库定位

### 方法谱系

本文提出的基于扩散先验的三维弱透镜质量映射方法，处于**物理信息深度学习与贝叶斯逆问题**的交叉点上，其核心创新在于将数据驱动的生成式先验与可微物理模型解耦，并通过后验采样实现严格的不确定性量化。

**先验建模的演进**。传统三维质量映射方法依赖手工设计的平滑先验。**Wiener滤波器**（Simon et al., MNRAS 2009）假设密度场服从高斯先验，在傅里叶空间施加基于功率谱的正则化，但无法捕捉宇宙网的非高斯纤维状结构，导致重建结果过度平滑。近年来，深度学习方法试图突破这一限制：**Neural Ensemble**（Zhao et al., ICLR 2025）通过训练多个神经网络提供近似后验分布，但其集成策略本质上仍是单一视角的近似，缺乏对完整贝叶斯后验的严格采样能力。本文的方法通过从高保真N体模拟Conicus3D中学习红移条件扩散模型，首次将宇宙学模拟的完整统计特性编码为数据驱动先验，直接解决了上述两类基线的根本缺陷——手工先验的表达力不足与近似后验的不严格性。

**后验采样框架的继承与改造**。本文的后验采样方案建立在**DAPS（Decoupled Annealing Posterior Sampling）**框架之上，该框架的核心思想是将扩散先验的去噪过程与似然梯度解耦，通过退火策略在二者之间平衡。本文针对三维弱透镜场景做了关键改造：将二维扩散先验扩展为红移条件的多平面结构，使先验能够感知宇宙学红移演化；在DAPS的似然步骤中引入基于物质功率谱 $P(k)$ 的傅里叶对角协方差 $\mathbf{\Sigma} = \mathbf{F}^{-1} \mathrm{diag}(P_k) \mathbf{F}$，利用物理信息加速收敛并稳定采样。这一改造使DAPS框架首次适用于三维光锥重建这一高维逆问题。

**弱透镜前向模型的标准化程度**。本文采用的前向模型——物质密度投影（$\mathbf{Q}$ 算子）、剪切卷积（$\mathbf{P}$ 算子）以及高斯形状噪声——是弱透镜宇宙学的标准线性模型（参见公式 (3)–(5)）。这一选择保证了物理上的可解释性，同时其可微性使其能无缝嵌入扩散后验采样的梯度计算流程。与端到端黑箱方法不同，这种显式物理建模使得先验与似然的贡献可以分别追踪和诊断。

### 知识库定位与适用边界

**适用场景**。本文方法针对的是**类JWST COSMOS-Web巡天的三维弱透镜质量映射**：足迹约0.54 deg²、星系密度约261 arcmin⁻²、形状噪声 $\sigma_e \approx 0.25$、测光红移散布 $\sigma_z = 0.11(1+z)$。在这一设定下，方法在二维收敛场和三维密度场的Pearson相关系数上均显著优于Wiener滤波和Neural Ensemble基线（Table 1）。具体而言，在分布内体积上，二维相关系数 $\rho^{2D}$ 达到0.87–0.88（vs. Neural 0.86–0.87, Wiener 0.77–0.83），三维模糊相关系数 $\rho_{blur}^{3D}$ 达到0.83（vs. Neural 0.79–0.80, Wiener 0.71–0.72）。

**先验依赖与分布外鲁棒性**。方法的强先验来自特定宇宙学参数下的AbacusSummit模拟。这引入了一个核心张力：先验越强，分布内重建越精确，但对宇宙学参数偏移的敏感性可能越高。本文在第三个测试体积中考察了分布外（OOD）场景——真实宇宙学包含无质量中微子，与训练先验的宇宙学不匹配。结果表明，尽管先验功率谱与真实功率谱存在显著差异，后验样本仍然匹配真实功率谱（Figure 5 right），二维和三维相关系数分别达到0.98和0.92（Table 1）。这表明似然引导在DAPS框架中起到了有效的校正作用，方法对中等程度的先验错误具有鲁棒性。然而，这一结论仅基于单一OOD场景，对更极端的宇宙学偏移或使用不同模拟代码（如IllustrisTNG、Millennium）的影响**尚未充分研究**，需要手动验证。

**计算成本的隐忧**。扩散采样过程涉及数百至数千步的去噪迭代，每步需要计算扩散先验梯度和似然梯度。论文未明确报告采样时间或GPU消耗，这使得方法的实用边界难以精确评估。对于当前JWST-scale的小足迹数据，计算成本可能尚可接受，但扩展到Euclid或LSST等万平方度量级巡天时，采样效率可能成为瓶颈。这一点在论文的开放问题中也有所体现——加速采样过程被列为未来方向之一。

**对下游宇宙学推断的增益**。本文的核心论证之一是：匹配样本级别的功率谱（角功率谱和径向功率谱）对于无偏宇宙学推断至关重要。Figure 5左图和中图显示，本文方法的后验样本在高 $\ell$ 小尺度上保留了正确功率，且径向功率谱近乎平坦，表明不同红移平面之间没有虚假的视线相关性——而Neural Ensemble输出了显著的非物理视线相关。这意味着本文的样本可直接用于峰值计数、空隙统计等非线性统计量的下游推断，而不需要额外的偏差校正。然而，**这一增益的实际宇宙学参数约束力尚未量化**，论文仅展示了统计一致性，未报告使用后验样本进行参数推断的具体结果。

### 局限与开放问题

基于上述分析，本文的核心局限可归纳为三个层次：

1. **先验保真度依赖**：重建质量直接依赖于N体模拟对真实宇宙统计特性的复现精度。若模拟在非线性小尺度、重子物理反馈等方面存在系统偏差，先验偏差将不可避免地影响后验结果。论文未分析重建对不同模拟先验的敏感性。

2. **OOD鲁棒性的上限未知**：虽然方法在单一OOD场景下表现良好，但扩散先验本质上是一个强先验。当真实宇宙学参数与训练先验差异过大时，似然引导可能不足以完全校正，导致后验样本偏离真实分布。系统性地刻画方法的OOD失效边界是一个重要的开放问题。

3. **可扩展性未验证**：扩散采样的计算成本与采样步数、似然评估复杂度直接相关。对于更大足迹、更高分辨率的巡天数据，当前框架可能需要显著的工程优化（如蒸馏加速、变分替代）才能实用。

此外，论文提出的框架具有向其他宇宙学探针扩展的潜力——例如将弱透镜与FRB色散测量、CMB次级各向异性联合反演，利用扩散先验统一描述不同探针共享的三维物质场。这一多探针联合推断方向是该方法在知识库中的自然延伸。

## 原文 PDF

![[paperPDFs/CVPR_2026/Generative_Diffusion_Priors_for_3D_Mapping_of_the_Dark_Universe.pdf]]