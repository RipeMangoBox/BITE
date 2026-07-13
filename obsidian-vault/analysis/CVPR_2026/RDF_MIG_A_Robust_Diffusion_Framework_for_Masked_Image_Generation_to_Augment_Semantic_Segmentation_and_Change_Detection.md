---
title: "RDF-MIG: A Robust Diffusion Framework for Masked Image Generation to Augment Semantic Segmentation and Change Detection"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/RDF_MIG_A_Robust_Diffusion_Framework_for_Masked_Image_Generation_to_Augment_Semantic_Segmentation_and_Change_Detection.pdf
project_link: null
code_link: null
aliases:
- RM
- RDF-MIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过最大相关熵鲁棒扩散（MCRD）损失对噪声预测误差进行自适应重加权，抑制离群值梯度，从而增强扩散模型训练的鲁棒性。
primary_logic: 联合建模图像特征与掩码的分布，并通过特征压缩融合（FCF）将多光谱数据转换为与预训练扩散模型兼容的三通道表示，同时采用相关熵准则的鲁棒训练目标，实现高质量、严格对齐的图像-掩码对生成。
claims:
- RDF-MIG 能同时生成适用于语义分割和变化检测的图像-掩码对，并支持多光谱图像生成。
- MCRD 损失在生成质量和下游任务性能上显著优于 MSE 和 Huber 损失，尤其在标签噪声下优势明显。
- MCRD 损失梯度在小误差下与 MSE 对齐，但在大误差时自适应衰减，理论分析保证该性质。
- Hi-CNA 语义分割 (SS) 上 IoU / F1 = Ours (MCRD) 44.13 / 61.24
---

# RDF-MIG: A Robust Diffusion Framework for Masked Image Generation to Augment Semantic Segmentation and Change Detection

> [!tip] 核心洞察
> 联合建模图像特征与掩码的分布，并通过特征压缩融合（FCF）将多光谱数据转换为与预训练扩散模型兼容的三通道表示，同时采用相关熵准则的鲁棒训练目标，实现高质量、严格对齐的图像-掩码对生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | RDF-MIG: 一种面向掩膜图像生成的鲁棒扩散框架，用于增强遥感语义分割与变化检测 |
| 英文题名 | RDF-MIG: A Robust Diffusion Framework for Masked Image Generation to Augment Semantic Segmentation and Change Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Cao_RDF-MIG_A_Robust_Diffusion_Framework_for_Masked_Image_Generation_to_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RDF-MIG |
| Dataset | Hi-CNA 语义分割, Hi-CNA 变化检测 (CD) - SNU-Net, WHU Building 语义分割 |

> [!tip] 效果简介
> - Hi-CNA 语义分割 (SS) 上，IoU / F1 Ours (MCRD) 44.13 / 61.24 vs Ours (MSE) 42.28 / 59.43 (+1.85 / +1.81)。
> - Hi-CNA 变化检测 (CD) - SNU-Net 上，IoU / F1 DMCRD 50.00 / 66.67 vs DMSE 45.62 / 62.66 (+4.38 / +4.01)。
> - WHU Building 语义分割 (SS) 上，IoU / F1 Ours (MCRD) 41.88 / 59.04 vs Ours (MSE) 40.59 / 57.74 (+1.29 / +1.30)。

## 概要

**问题瓶颈**：遥感图像生成方法长期面临三大割裂——语义分割（SS）与变化检测（CD）任务各用各的生成框架，无法统一；绝大多数方法仅支持 RGB 三通道，对多光谱数据无能为力；训练损失（MSE）对标注噪声和重尾离群值高度敏感，导致生成的图像-掩码对质量不稳定。现有代表性方法如 **SemGAN**（Li et al., CVPR 2021）、**SatSynth**（Toker et al., CVPR 2024）仅面向语义分割，**ChangeAnywhere**（Tang and Chen, arXiv 2024）、**Changen**（Zheng et al., ICCV 2023）、**ChangeDiff**（Zang et al., AAAI 2025）仅面向变化检测，且均缺乏对多光谱输入和噪声鲁棒训练的联合支持（Table 1）。

**核心思路**：RDF-MIG 通过三个相互咬合的模块打通上述瓶颈。**特征压缩融合（FCF）** 将任意数量的多光谱波段通过加权融合压缩为单通道特征图，与掩码拼接成三通道张量，从而无缝接入预训练扩散模型（DDPM/LDM），实现图像特征与掩码的联合分布建模。**最大相关熵鲁棒扩散（MCRD）损失** 取代传统的 MSE 目标，利用相关熵准则对噪声预测误差进行自适应重加权——小误差时梯度与 MSE 对齐，大误差（离群值）时指数衰减权重，从根源上抑制错误梯度更新。**pix2pix 解码器** 将扩散生成的特征图还原为多光谱图像，完成从联合隐空间到完整数据的映射。

**关键结论**：
- **任务统一性**：RDF-MIG 是首个同时支持语义分割和变化检测图像-掩码对生成的框架，且原生兼容多光谱输入（Table 1）。
- **鲁棒性优势**：在 Hi-CNA 变化检测任务上，MCRD 损失相较 MSE 损失使下游 SNU-Net 的 IoU 提升 **+4.38**（45.62 → 50.00），F1 提升 **+4.01**；语义分割任务上 IoU 提升 **+1.85**（Table 4）。在 15% 标签噪声条件下，MSE 生成数据训练的下游模型性能大幅下降，而 MCRD 仅轻微衰减（Table 5）。
- **理论保证**：MCRD 梯度的泰勒展开（Eq. 8）和二阶导数分析（Eq. 9）严格证明了小误差下与 MSE 的一致性，并给出了核宽 σ 的选择准则 $\sigma \ge e_{\max} \sqrt{3 / (2\beta)}$（Eq. 10），使鲁棒性与精度之间的权衡可控。

**方法定位**：RDF-MIG 属于“生成数据增强”路线，但与现有方法的关键区别在于其**损失函数层面的鲁棒性改造**和**输入层面的多光谱兼容设计**，而非简单的架构堆叠。它不改变下游分割/检测模型本身，而是通过提供高质量、严格对齐的合成图像-掩码对来提升下游性能，具有模型无关的即插即用特性。

遥感图像的语义分割与变化检测是环境监测、城市规划、灾害评估等应用的核心任务。然而，构建高质量的像素级标注数据集成本极高，尤其在变化检测任务中，需要成对的双时相图像及其精确的变化区域掩码，标注难度远大于单时相语义分割。这一数据瓶颈严重制约了下游模型性能的提升。

近年来，基于生成模型的数据增强方法为解决标注稀缺问题提供了新的思路。在语义分割方向，**SemGAN** (Li et al., CVPR 2021) 和 **SatSynth** (Toker et al., CVPR 2024) 等方法尝试生成图像-掩码对；在变化检测方向，**ChangeAnywhere** (Tang and Chen, arXiv 2024)、**Changen** (Zheng et al., ICCV 2023) 和 **ChangeDiff** (Zang et al., AAAI 2025) 等方法则专注于生成双时相变化数据。此外，**SegDiff** (Amit et al., arXiv 2021) 探索了利用扩散模型生成语义分割掩码。

然而，现有方法存在三个关键瓶颈：

**第一，任务支持单一。** 如表1所示，现有方法要么仅支持语义分割，要么仅支持变化检测，没有一个统一的框架能够同时服务于这两类核心遥感任务。这迫使研究者针对不同任务维护独立的生成模型，增加了工程复杂度和资源开销。

**第二，光谱波段受限。** 绝大多数现有方法仅支持RGB三通道图像生成，无法利用遥感影像中丰富的多光谱信息（如近红外NIR波段）。多光谱波段往往携带对地物分类和变化判别至关重要的物理信息，放弃这些波段意味着生成数据的判别性不足。

**第三，对训练噪声敏感。** 现有扩散模型普遍采用均方误差（MSE）损失进行训练。MSE损失对重尾噪声和标注错误极为敏感——在真实遥感数据中，由于传感器差异、配准误差和人工标注偏差，这类噪声普遍存在。当训练数据中存在离群值时，MSE损失会驱动模型过度拟合噪声样本，导致生成的图像-掩码对质量下降，进而损害下游任务性能。

针对上述问题，本文提出 **RDF-MIG**（Robust Diffusion Framework for Masked Image Generation），一个统一的鲁棒扩散生成框架。其设计动机源于以下核心洞察：通过联合建模图像特征与掩码的分布，并引入信息论意义下的相关熵准则作为扩散训练目标，可以在抑制离群值影响的同时，生成高质量、严格对齐的图像-掩码对，从而同时增强语义分割和变化检测任务。

## 核心方法与创新机理

RDF-MIG 的核心创新围绕一个瓶颈和三个技术支点展开：**现有遥感图像生成方法无法同时支持语义分割（SS）与变化检测（CD）两种任务，且缺乏对多光谱数据的原生支持和对训练噪声的鲁棒性**。本文通过联合建模图像特征与掩码分布，并在扩散训练中引入相关熵准则，从任务泛化性、光谱兼容性、训练鲁棒性三个维度实现了系统性突破。

### 任务统一：从单一任务到 SS/CD 双任务生成

现有方法在任务支持上存在严格分裂——**SemGAN** (Li et al., CVPR 2021)、**SatSynth** (Toker et al., CVPR 2024)、**SegDiff** (Amit et al., arXiv 2021) 仅能生成语义分割图像或掩码，而 **ChangeAnywhere** (Tang and Chen, arXiv 2024)、**Changen** (Zheng et al., ICCV 2023)、**ChangeDiff** (Zang et al., AAAI 2025) 仅服务于变化检测（Table 1）。RDF-MIG 通过扩散模型学习图像特征与掩码的联合分布，使同一框架可同时输出单时相分割标注图像和双时相变化标注图像，在 Hi-CNA 语义分割（IoU 44.13）和变化检测（IoU 50.00）上均取得领先（Table 2），填补了统一生成框架的空白。

### 光谱兼容：FCF 多光谱压缩融合

预训练扩散模型（如 LDM）的输入通道固定为三通道，直接限制了多光谱遥感图像（如 RGB+NIR）的利用。RDF-MIG 提出 **特征压缩融合（Feature Compression Fusion, FCF）** 机制：将 $a$ 个光谱波段通过加权求和压缩为单通道特征图 $y(i,j) = \sum_{k=1}^{a} w_k \cdot x_k(i,j)$，再与语义掩码和变化掩码拼接为三通道张量输入扩散模型（Eq. (4)）。该设计使扩散模型在保持预训练权重兼容性的同时，隐式编码了多光谱结构信息。实验表明，加入 NIR 波段后语义分割 IoU 从 44.13 提升至 45.20（Table 2），验证了 FCF 的多光谱扩展能力。FCF 与具体扩散模型（DDPM/LDM/DDIM）和下游任务解耦，具有通用性。

### 鲁棒训练：MCRD 损失与自适应梯度调控

这是 RDF-MIG 最深层的理论创新。标准扩散模型使用 MSE 损失训练去噪器（Eq. (3)），对重尾噪声和标签噪声敏感——大误差样本产生超大梯度，主导参数更新，导致生成质量退化。本文提出 **最大相关熵鲁棒扩散损失（Maximum Correntropy Robust Diffusion, MCRD）**：

$$\text{Loss}_{\text{MCRD}} = \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}[\rho(1 - \exp(-\|\mathbf{f}_\theta(\mathbf{x}_t, t) - \boldsymbol{\varepsilon}\|^2 / (2\sigma^2)))]$$

其梯度具有自适应指数衰减特性（Eq. (7)）：

$$\mathbf{g}_{\text{mcrd},\theta} = \mathbb{E}[\rho \sigma^{-2} \exp(-\frac{e^2}{2\sigma^2}) e \frac{\partial e}{\partial \theta}]$$

当预测误差 $e$ 较小时，泰勒展开 $\mathbf{g}_{\text{mcrd}} \approx \rho\sigma^{-2}(e - e^3/(2\sigma^2))\frac{\partial e}{\partial\theta}$ 表明梯度与 MSE 梯度方向对齐（Eq. (8)），保证了正常样本的学习效率；当 $e > \sigma$ 时，指数权重 $\exp(-e^2/(2\sigma^2))$ 急剧衰减，梯度在 $[\sigma, \sqrt{3}\sigma]$ 区间内从上升转为下降（Fig. 1(c)），有效抑制离群值的破坏性更新。核宽 $\sigma$ 的选择遵循 $\sigma \ge e_{\max} \sqrt{3/(2\beta)}$（Eq. (10)），其中 $\beta$ 为斜率容忍度，提供了可操作的理论指导。

**消融实验直接验证了 MCRD 的因果效应**：在相同训练设置下，仅将 MSE 替换为 MCRD（$\sigma=0.2, \rho=0.08$），Hi-CNA 语义分割 IoU 从 42.28 提升至 44.13（+1.85），变化检测 IoU 从 45.62 提升至 50.00（+4.38）（Table 4）；在标签噪声场景下，MCRD 相对 MSE 的优势进一步扩大（Table 5），且持续优于 Huber 损失（$\delta=0.2$），证实了相关熵准则在扩散训练中的鲁棒性优势。

RDF‑MIG 的整体 pipeline 围绕一个核心目标构建：**联合建模多光谱图像特征与语义掩码的分布**，从而同时生成适用于语义分割（SS）和变化检测（CD）的高质量、严格对齐的图像‑掩码对。整个框架由三个关键模块串联组成，形成“压缩‑生成‑重建”的信息流。

### 模块串联与信息流

1. **特征压缩融合（Feature Compression Fusion, FCF）**  
   多光谱遥感图像通常包含超过三个波段（如 RGB + NIR），无法直接输入基于 RGB 预训练的扩散模型。FCF 模块通过对各波段进行通道加权求和，将 $a$ 个多光谱波段压缩为一张单通道特征图 $y \in \mathbb{R}^{H \times W \times 1}$：
   $$y(i,j) = \sum_{k=1}^{a} w_k \cdot x_k(i,j), \quad \sum_{k=1}^{a} w_k = 1$$
   随后，该特征图与对应的语义掩码 $m$ 拼接，构成一个三通道张量，作为扩散模型的输入。这一设计使得 RDF‑MIG 能够兼容任意波段数的多光谱数据，同时保持与 RGB 预训练扩散模型的接口一致性。

2. **扩散模型（DDPM / LDM）**  
   扩散模型负责学习 $(y, m)$ 的联合分布。在前向过程中，逐步向清洁的拼接张量 $\mathbf{x}_0$ 添加高斯噪声：
   $$\mathbf{x}_t = \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1-\bar{\alpha}_t} \boldsymbol{\varepsilon}$$
   去噪器 $\mathbf{f}_\theta(\mathbf{x}_t, t)$ 被训练来预测添加的噪声 $\boldsymbol{\varepsilon}$。**核心创新在于训练目标**：传统 DDPM 使用 MSE 损失，而 RDF‑MIG 采用最大相关熵鲁棒扩散（MCRD）损失：
   $$\mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}\left[\rho\left(1 - \exp\left(-\frac{\|\mathbf{f}_\theta(\mathbf{x}_t, t) - \boldsymbol{\varepsilon}\|^2}{2\sigma^2}\right)\right)\right]$$
   该损失通过核宽 $\sigma$ 控制的自适应指数权重，在大噪声预测误差时自动衰减梯度，抑制离群值对模型更新的干扰，从而提升对训练数据中重尾噪声的鲁棒性。

3. **解码器（pix2pix: U‑Net 生成器 + PatchGAN 判别器）**  
   扩散模型生成的是压缩后的特征图，而非最终的多光谱图像。解码器采用 pix2pix 架构，以生成的特征图为条件，重建出完整的多光谱图像。生成器使用 U‑Net 结构，判别器采用 PatchGAN 对局部图像块进行真伪判断，训练目标为对抗损失与 L1 重建损失的组合：
   $$\mathcal{L}_G = -\mathbb{E}_{\mathbf{y}}[\log D(\mathbf{y}, G(\mathbf{y}))] + \lambda \mathbb{E}_{\mathbf{y},\mathbf{x}}[\|\mathbf{x} - G(\mathbf{y})\|_1]$$

### 训练与推理流程

- **训练阶段**（Figure 1a）：将真实多光谱图像经 FCF 压缩后与对应掩码拼接，输入扩散模型学习联合分布；同时训练解码器将扩散模型生成的特征图重建为原始多光谱图像。
- **推理阶段**（Figure 1b）：从随机噪声出发，扩散模型通过迭代去噪生成特征‑掩码对；解码器将特征图重建为多光谱图像，掩码直接作为语义标签或变化标签输出。

### 关键设计决策

| 设计选择 | 解决的问题 | 证据锚点 |
|---------|-----------|---------|
| FCF 多光谱→三通道压缩 | 使预训练扩散模型兼容多光谱输入 | Section 4.2, Table 1 |
| 联合建模 $(y, m)$ 分布 | 同时支持 SS 和 CD 任务 | Table 1, Abstract |
| MCRD 损失替代 MSE | 提升对标签噪声和重尾噪声的鲁棒性 | Section 4.3, Table 4–5 |
| pix2pix 解码器重建 | 从压缩特征恢复完整多光谱图像 | Section 4.4, Figure 1a |

> **注意**：FCF 中的融合权重 $w_k$ 在实验中采用均匀权重（$w_k = 1/a$），但框架本身支持可学习的权重，这一扩展方向被列为开放问题。MCRD 损失的核宽 $\sigma$ 在实验中固定为 0.2，其自适应选择策略的自动化也是未来工作方向之一。

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/002_Figure_1.jpg]]
*Figure 1: Method Workflow: (a) training, (b) inference, (c) comparison of MCRD vs. other losses (curves and gradients). With a carefully designed FCF strategy and robust loss, RDF-MIG effectively models the joint distribution of image features and masks, enabling the generation of high-quality, strictly aligned image–mask pairs for training semantic segmentation and change detection models*

RDF-MIG 的核心由三个模块串联构成：**特征压缩融合（FCF）**、**扩散模型** 和 **pix2pix 解码器**。其中，扩散模型的训练目标被重新设计为**最大相关熵鲁棒扩散（MCRD）损失**，这是本文最关键的创新点。

### 特征压缩融合（FCF）

遥感图像通常包含多个光谱波段，无法直接输入预训练于 RGB 图像的扩散模型。FCF 模块将多光谱数据压缩为与预训练模型兼容的三通道表示。

具体而言，给定多光谱图像 $\mathbf{X} \in \mathbb{R}^{H \times W \times a}$（$a$ 为波段数），FCF 通过通道加权融合生成单通道特征图：

$$y(i,j) = \sum_{k=1}^{a} w_k \cdot x_k(i,j), \quad \sum_{k=1}^{a} w_k = 1$$

其中 $w_k$ 为各波段的融合权重，文中默认采用均匀权重 $w_k = 1/a$。随后，该特征图与语义分割掩码或变化检测掩码拼接，形成三通道张量，作为扩散模型的输入。FCF 被设计为通用机制，独立于具体的扩散模型（DDPM、LDM、DDIM）和下游任务。

### 扩散模型与 MCRD 损失

扩散模型的核心是学习去噪器 $\mathbf{f}_\theta$，使其能从噪声图像 $\mathbf{x}_t$ 中预测所添加的噪声 $\boldsymbol{\varepsilon}$。标准 DDPM 采用 MSE 损失：

$$\min \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}} \left[ \| \mathbf{f}_\theta(\mathbf{x}_t, t) - \boldsymbol{\varepsilon} \|^2 \right]$$

然而，当训练数据中存在重尾噪声或离群值时，MSE 的二次惩罚会赋予大误差样本过高的梯度，导致模型被离群值“绑架”。为解决此问题，本文提出 **MCRD 损失**，基于相关熵（correntropy）准则构建：

$$\text{Loss}_{\text{MCRD}}(x) = \mathbb{E}[\rho(1 - \exp(-x^2 / (2\sigma^2)))]$$

其中 $\rho$ 为缩放因子，$\sigma$ 为核宽。代入扩散训练，期望损失为：

$$\mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}\left[\rho\left(1 - \exp\left(-\frac{\| \mathbf{f}_\theta(\mathbf{x}_t, t) - \boldsymbol{\varepsilon} \|^2}{2\sigma^2}\right)\right)\right]$$

**MCRD 的梯度自适应机制** 是其鲁棒性的根源。令 $e = \mathbf{f}_\theta(\mathbf{x}_t, t) - \boldsymbol{\varepsilon}$，MCRD 损失对参数 $\theta$ 的梯度为：

$$\mathbf{g}_{\text{mcrd},\theta} = \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}\left[\rho \sigma^{-2} \exp\left(-\frac{e^2}{2\sigma^2}\right) e \frac{\partial e}{\partial \theta}\right]$$

梯度中引入了指数衰减因子 $\exp(-e^2 / (2\sigma^2))$：
- **小误差时**，$\exp(-e^2 / (2\sigma^2)) \approx 1$，梯度近似于 MSE 梯度，保证收敛效率。
- **大误差时**，指数项趋近于 0，梯度被自适应抑制，离群值对参数更新的影响被阻断。

**MSE-一致性校准**：对小误差情形做泰勒展开可进一步验证此性质：

$$\mathbf{g}_{\text{mcrd},\theta} = \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}\left[\rho \sigma^{-2} \left(e - \frac{e^3}{2\sigma^2} + o(e^3)\right) \frac{\partial e}{\partial \theta}\right]$$

当 $e \ll \sigma$ 时，高阶项可忽略，MCRD 梯度退化为与 MSE 梯度成比例的形式，保证两者在小误差下行为一致。梯度斜率分析给出：

$$\frac{\partial g_{\text{mcrd},\theta}}{\partial e} = \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\varepsilon}}\left[\rho \sigma^{-2} \left(1 - \frac{3e^2}{2\sigma^2} + o(e^2)\right) \frac{\partial e}{\partial \theta}\right]$$

核宽 $\sigma$ 的选择决定了“大误差”与“小误差”的分界。文中从理论上推导了核宽选择准则：给定最大允许误差 $e_{\max}$ 和斜率容忍度 $\beta$，应满足：

$$\sigma \ge e_{\max} \sqrt{3 / (2\beta)}$$

实验设置中，MCRD 采用 $\sigma = 0.2$，$\rho = 0.08$。

### pix2pix 解码器

扩散模型输出的是三通道特征-掩码融合张量，需要解码为最终的多光谱图像。解码器采用 pix2pix 架构，包含：
- **生成器 G**：U-Net 结构，从融合特征图重建多光谱图像。
- **判别器 D**：PatchGAN 结构，对局部图像块进行真伪判别。

判别器损失为：

$$\mathcal{L}_D = -\mathbb{E}_{\mathbf{y},\mathbf{x}}[\log D(\mathbf{y},\mathbf{x})] - \mathbb{E}_{\mathbf{y}}[\log(1 - D(\mathbf{y}, G(\mathbf{y})))]$$

生成器损失结合对抗损失与 L1 重建损失：

$$\mathcal{L}_G = -\mathbb{E}_{\mathbf{y}}[\log D(\mathbf{y}, G(\mathbf{y}))] + \lambda \mathbb{E}_{\mathbf{y},\mathbf{x}}[\| \mathbf{x} - G(\mathbf{y}) \|_1]$$

其中 $\mathbf{y}$ 为扩散模型输出的融合特征图，$\mathbf{x}$ 为真实多光谱图像。

## 实验与关键发现

### 实验设置

**数据集。** 语义分割实验使用 Hi-CNA 和 WHU Building 数据集，变化检测实验使用 Hi-CNA 双时相数据集。所有生成方法在相同条件下训练，学习率 1e-4，batch size 20。下游分割/检测模型架构完全一致以确保公平比较。MCRD 损失使用核宽 $\sigma = 0.2$ 和缩放系数 $\rho = 0.08$；Huber 损失使用 $\delta = 0.2$。FCF 中多光谱通道融合采用均匀权重 $w_k = 1/a$。

### 主实验结果

**下游任务性能。** Table 2 给出了各生成方法在语义分割和变化检测下游任务上的完整对比。RDF-MIG（Ours）在 Hi-CNA 语义分割上取得 IoU 44.13、F1 61.24；加入 NIR 波段后（Ours+NIR）进一步提升至 IoU 45.20、F1 62.26。在 WHU Building 语义分割上，Ours 达到 IoU 41.88、F1 59.04。变化检测方面，Ours 在 Hi-CNA CD 上取得 IoU 50.00、F1 66.67。

**方法适用性对比。** Table 1 系统总结了现有方法的任务适应性和数据需求。SemGAN（Li et al., CVPR 2021）和 SatSynth（Toker et al., CVPR 2024）仅支持语义分割图像生成；SegDiff（Amit et al., arXiv 2021）仅生成分割掩码；ChangeAnywhere（Tang and Chen, arXiv 2024）、Changen（Zheng et al., ICCV 2023）和 ChangeDiff（Zang et al., AAAI 2025）仅面向变化检测。这些方法均不支持多光谱图像生成。RDF-MIG 是唯一同时覆盖语义分割和变化检测、且支持多光谱输入的统一框架。

**生成图像质量。** Table 3 对比了各方法的生成图像质量指标。由于部分变化检测生成器直接复用原始数据集的 T1 图像而仅合成 T2，评估聚焦于生成 T2 的质量。RDF-MIG 在 FID、sFID 等指标上表现优异，验证了 FCF 融合策略和 MCRD 鲁棒损失对生成质量的贡献。

### 消融实验

**损失函数消融。** Table 4 对比了 RDF-MIG 在不同损失函数下生成数据训练的下游模型性能。将 MSE 替换为 MCRD 损失在所有任务中持续提升下游性能：Hi-CNA SS 上 IoU 从 42.28 提升至 44.13（+1.85），F1 从 59.43 提升至 61.24（+1.81）；Hi-CNA CD（SNU-Net）上 IoU 从 45.62 提升至 50.00（+4.38），F1 从 62.66 提升至 66.67（+4.01）；WHU Building SS 上 IoU 从 40.59 提升至 41.88（+1.29），F1 从 57.74 提升至 59.04（+1.30）。MCRD 在所有设置下均优于 Huber 损失，验证了相关熵准则相对于传统鲁棒损失的优越性。

**多光谱波段贡献。** Table 2 中 Ours+NIR 与 Ours 的对比表明，引入近红外波段进一步提升了语义分割性能（IoU +1.07, F1 +1.02），验证了 FCF 模块对多光谱信息的有效利用。

**合成数据比例影响。** Figure 2 展示了合成数据比例对下游 IoU 的影响曲线。随着合成数据比例增加，语义分割（U-Net）和变化检测（SNU-Net）的 IoU 均持续提升，直至达到饱和。这表明 RDF-MIG 生成的合成数据能有效增强训练集，且在一定范围内比例越高增益越明显。

### 鲁棒性实验

**标签噪声下的鲁棒性。** Table 5 展示了在训练数据引入标签噪声时，不同损失函数训练的 RDF-MIG 生成数据对下游性能的影响。MCRD 损失在所有噪声水平下均显著优于 MSE 和 Huber 损失，且噪声越大优势越明显。这归因于 MCRD 损失梯度在大误差时自适应衰减的机制（Eq. (7)-(9)）：当预测误差 $e$ 超过核宽 $\sigma$ 时，指数权重 $\exp(-e^2/2\sigma^2)$ 迅速衰减，抑制离群值对模型更新的影响，从而保护正常样本的学习过程。

**损失函数行为分析。** Figure 1(c) 对比了 MCRD、MSE 和 Huber 的损失曲线及梯度曲线。MCRD 梯度在小误差下与 MSE 对齐（由 Eq. (8) 的泰勒展开保证），但在大误差时梯度从递增转为递减（转折点 $e = \sigma$），并沿 $[\sigma, \sqrt{3}\sigma]$ 区间快速衰减。这一性质使 MCRD 兼具 MSE 在小误差下的收敛效率和相关熵准则对大误差的鲁棒抑制。Figure 4 的可视化对比进一步印证了 MCRD 训练数据在下游分割/检测结果上的质量优势。

### 可视化分析

Figure 3 展示了真实样本与 RDF-MIG 合成样本的视觉对比。合成图像在保持遥感场景结构特征的同时，实现了图像与掩码的严格对齐。Figure 4 展示了不同损失函数训练数据在下游任务上的分割/检测结果可视化，MCRD 对应的结果在边界精细度和误检率上均优于 MSE 和 Huber。

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/009_Figure_4.jpg]]
*Figure 4: Visualizations of downstream results (different losses)*

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/004_Figure_3.jpg]]
*Figure 3: Visual comparison of real and synthetic samples*

### 局限性与讨论

尽管 RDF-MIG 在遥感语义分割和变化检测任务上展现了统一的生成能力和鲁棒性，仍存在以下局限：（1）目前仅在遥感数据集上验证，尚未推广到其他视觉领域；（2）生成多时相变化检测数据需要双时相多光谱图像，对数据源有一定要求；（3）使用 MCRD 损失和 pix2pix 解码器训练扩散模型的计算成本较高，文中未提供效率对比。核宽 $\sigma$ 的选取目前依赖 Eq. (10) 的准则结合经验调节，其自适应策略有待进一步研究。

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/001_Table_1.jpg]]
*Table 1: This table summarizes data requirements and task adaptability of remote sensing image generation methods. Seg. masks denote semantic segmentation masks and Multispec. gen. denotes support for multispectral image generation. Compared with existing methods, ours is more general*

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/007_Table_4.jpg]]
*Table 4: Comparison of downstream performance using data generated by the RDF-MIG trained with different loss functions*

![[assets/figures/papers/paper_list_l916_https_openaccess_thecvf_com_content_CVPR2026_html_Cao_RDF_MIG_A_Robust_D/figures/008_Table_5.jpg]]
*Table 5: Comparison of downstream performance using data generated by the RDF-MIG trained with different loss functions*

## 定位与知识库关联

### 任务定位：遥感图像-掩码联合生成的统一框架

RDF-MIG 的核心定位是**统一遥感语义分割（SS）与变化检测（CD）的图像-掩码对生成**。现有方法普遍存在任务割裂的问题：语义分割图像生成方法（如 **SemGAN** (Li et al., CVPR 2021)、**SatSynth** (Toker et al., CVPR 2024)）和掩码生成方法（如 **SegDiff** (Amit et al., arXiv 2021)）无法用于变化检测；而变化检测数据生成方法（如 **ChangeAnywhere** (Tang and Chen, arXiv 2024)、**Changen** (Zheng et al., ICCV 2023)、**ChangeDiff** (Zang et al., AAAI 2025)）则无法生成语义分割数据。RDF-MIG 通过联合建模图像特征与掩码的分布，首次实现了单一框架同时支持两类任务（Table 1，置信度 0.95）。

### 技术谱系：从标准扩散到鲁棒扩散

在扩散模型训练范式上，RDF-MIG 的基线是标准 DDPM 的 MSE 损失（Eq. 3）。该损失对噪声预测误差施加均匀的二次惩罚，在训练数据含离群噪声时会导致梯度被大误差样本主导。RDF-MIG 引入的 **MCRD（最大相关熵鲁棒扩散）损失**（Eq. 5-6）将这一范式从“矩惩罚”升级为“信息势惩罚”：其梯度包含自适应指数权重 $\exp(-e^2/2\sigma^2)$，在大误差时自动衰减，从而抑制离群值对参数更新的影响（Eq. 7）。这是**首次将相关熵准则引入扩散模型训练**（Section 2.3，置信度 0.95）。

MCRD 与 MSE 的关系并非对立，而是**小误差下的渐进对齐**：泰勒展开（Eq. 8）表明，当误差 $e \ll \sigma$ 时，MCRD 梯度退化为 $\rho\sigma^{-2} e \cdot \partial e/\partial\theta$，与 MSE 梯度形式一致。这一“MSE-一致性”性质通过核宽选择准则 $\sigma \ge e_{\max}\sqrt{3/(2\beta)}$（Eq. 10）得到保证，使 MCRD 在正常样本上保持 MSE 的收敛效率，仅对离群值施加衰减。

### 多光谱支持：特征压缩融合的通用性

现有方法普遍仅支持 RGB 三通道输入（Table 1）。RDF-MIG 提出的 **FCF（特征压缩融合）** 机制（Eq. 4）通过加权融合将任意 $a$ 个光谱波段压缩为单通道特征图，再与掩码拼接成三通道张量，从而**无缝兼容各类预训练扩散模型**（DDPM、LDM、DDIM）。论文明确指出 FCF 是“独立于具体扩散模型和任务的通用机制”（Section 4.3，置信度 0.95），其权重可固定（如均匀权重 $w_k=1/a$）或通过学习获得。

### 适用边界与局限

1. **领域验证范围有限**：目前仅在遥感数据集（Hi-CNA、WHU Building）上验证，尚未推广到其他视觉领域（如医疗影像、工业检测）。该框架对非遥感场景的迁移能力需要手动验证。

2. **数据源依赖**：生成多时相变化检测数据需要双时相多光谱图像，对数据获取条件有一定要求。

3. **计算成本未量化**：MCRD 损失训练扩散模型叠加 pix2pix 解码器（U-Net 生成器 + PatchGAN 判别器）的计算开销高于标准 MSE 训练，但论文未提供训练时间或显存占用的对比数据。

4. **核宽调节依赖人工**：MCRD 的核宽 $\sigma$ 目前基于理论准则（Eq. 10）和实验调节（实验中 $\sigma=0.2$），尚未实现自适应选择。

### 开放问题

- 该框架能否扩展到其他模态（如医学影像的器官分割与病变变化检测）或更复杂的生成任务？
- MCRD 核宽 $\sigma$ 的自适应选择策略（如基于数据噪声水平自动估计）能否进一步减少人工调节？
- 在更大规模数据集上，FCF 的可学习融合权重是否比固定均匀权重带来显著提升？
- 当前解码器采用 pix2pix 架构，更先进的图像重建模型（如扩散解码器）能否进一步提升生成质量？

## 原文 PDF

![[paperPDFs/CVPR_2026/RDF_MIG_A_Robust_Diffusion_Framework_for_Masked_Image_Generation_to_Augment_Semantic_Segmentation_and_Change_Detection.pdf]]
