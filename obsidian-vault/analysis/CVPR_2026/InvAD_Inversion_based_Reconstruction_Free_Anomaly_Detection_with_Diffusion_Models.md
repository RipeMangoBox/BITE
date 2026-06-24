---
title: "InvAD: Inversion-based Reconstruction-Free Anomaly Detection with Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InvAD_Inversion_based_Reconstruction_Free_Anomaly_Detection_with_Diffusion_Models.pdf
project_link: "https://invad-project.com"
code_link: "https://github.com/SkyShunsuke/InversionAD"
aliases:
- InvAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过DDIM反演直接推断输入图像对应的最终扩散隐变量，并将异常检测转化为先验分布下隐变量典型性的度量，从而避开重建步骤。
primary_logic: 将异常检测范式从“RGB空间去噪重建”转变为“潜空间加噪反演”，利用学习到的正常数据分布，通过反演映射评估偏离度，实现高效且保真度高的检测。
claims:
- InvAD免去显式重建，通过反演直接推断最终隐变量并基于先验分布计算异常分数。
- 仅使用3步反演即达到SOTA性能，推理速度达88.1 FPS，约为基线的2倍。
- 特征空间扩散建模保留高层语义，进一步提升了准确性和效率。
- 与重建方法相比，在极低反演步数下依然保持高AU-ROC（S=3为99.0），而重建方法至少需上百步。
---

# InvAD: Inversion-based Reconstruction-Free Anomaly Detection with Diffusion Models

> [!tip] 核心洞察
> 将异常检测范式从“RGB空间去噪重建”转变为“潜空间加噪反演”，利用学习到的正常数据分布，通过反演映射评估偏离度，实现高效且保真度高的检测。

| 字段 | 内容 |
|------|------|
| 中文题名 | InvAD：基于反演的免重建异常检测方法 |
| 英文题名 | InvAD: Inversion-based Reconstruction-Free Anomaly Detection with Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2504.05662) · [Project](https://invad-project.com) · [Code](https://github.com/SkyShunsuke/InversionAD) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | InvAD |
| Dataset | MVTecAD, VisA, MPDD, BMAD |

> [!tip] 效果简介
> - MVTecAD (多类) 上，图像级 AU-ROC 99.0 vs 98.8 (OmiAD) (+0.2)。
> - VisA (多类) 上，图像级 AU-ROC 96.9 vs 95.3 (OmiAD) (+1.6)。
> - MPDD (多类) 上，图像级 AU-ROC 96.5 vs 93.7 (OmiAD) (+2.8)。

## 概述

### 1. 问题背景

工业视觉异常检测的核心目标是在仅使用正常样本训练的条件下，识别出偏离正常分布的异常图像。现有基于扩散模型的主流方法遵循**“RGB空间去噪重建”范式**：先将输入图像加噪至中间时间步，再通过多步去噪重建出“正常化”版本，最后在像素或特征空间中计算输入与重建之间的均方误差作为异常分数。这一范式面临一个根本性的两难困境——**噪声强度的敏感性**与**多步去噪的计算开销**难以同时兼顾：弱噪声扰动不足以抹除异常区域，导致异常被“重建”回来而漏检；强噪声扰动则需要上百步去噪才能恢复高保真度图像，推理效率低下。

### 2. 核心思路

**InvAD** 提出了一种范式转变：将异常检测从“RGB空间去噪重建”转变为**“潜空间加噪反演”**（detection via noising in latent space）。其核心洞察在于：**扩散模型的反演过程（DDIM Inversion）可以将输入图像沿概率流常微分方程（PF-ODE）轨迹直接映射到最终扩散时间步的隐变量，而无需经历重建步骤**。由于扩散模型仅在正常样本上训练，其先验分布 $p(\mathbf{z}_T)$ 刻画了正常数据的典型性——正常图像反演得到的隐变量应位于先验分布的高概率区域，而异常图像则会偏离该分布。因此，通过评估反演隐变量在已知先验分布下的偏离程度，即可实现免重建的异常检测。

这一范式转变带来了两个关键优势：（1）**免重建**，从根本上避开了去噪步骤，推理仅需极少的反演步数；（2）**特征空间扩散建模**，在预训练骨干网络（EfficientNet-B4）提取的高层语义特征上进行扩散和反演，使检测聚焦于语义级别的异常模式而非低层像素纹理。

### 3. 方法定位与知识库贡献

在扩散异常检测的方法谱系中，InvAD 占据了一个独特的位置。现有扩散式方法可大致分为三类：

- **重建式方法**（如 **RD4AD**、**UniAD**）：通过加噪-去噪重建正常对应物，以重建误差作为异常分数，需要数十至数百步函数评估（NFE），速度受限。
- **特征引导式方法**（如 **DiAD**、**MDM**）：在扩散过程中引入特征约束或条件，虽提升了保真度，但仍依赖重建步骤，推理效率未根本改善。
- **单步/少步方法**（如 **SimpleNet**、**OmiAD**）：通过蒸馏或对抗训练压缩推理，但可能牺牲检测精度。

InvAD 的定位在于：**以反演替代重建，在保持甚至超越 SOTA 精度的同时，将推理步数压缩至 3 NFE，实现约 88 FPS 的吞吐量**，约为同类扩散方法的 2 倍以上。其知识库贡献可概括为：

- **新范式**：首次将免重建的 DDIM 反演引入异常检测，建立了“潜空间加噪反演”的检测框架。
- **评分机制**：提出 NLL+Diff 组合评分方案，通过计算隐变量每个空间位置的 L2 范数并取最大值-最小值差分，有效缓解了单纯对数似然评分在高扩散步数下的“反向评分”问题。
- **特征空间扩散**：在 EfficientNet-B4 的多层拼接特征上进行扩散建模，使推理阶段能够参照高层语义而非像素细节，进一步提升了准确性和效率。

### 4. 主要结果概要

InvAD 在多个工业异常检测基准上取得了领先性能，同时实现了显著的推理加速：

- **MVTecAD（多类）**：图像级 AU-ROC 达 **99.0**，超越此前最优的 OmiAD（98.8）；推理速度 **88.1 FPS**，约为 OmiAD（39.4 FPS）的 2.2 倍。
- **VisA（多类）**：图像级 AU-ROC **96.9**，较 OmiAD（95.3）提升 1.6 个百分点。
- **MPDD（多类）**：图像级 AU-ROC **96.5**，较 OmiAD（93.7）提升 2.8 个百分点。
- **BMAD（单类医学数据集）**：平均 mAD 达 **87.2**，超越 PatchCore（86.4）。

消融实验进一步验证了关键设计的有效性：（1）仅 3 步反演即可获得最优精度，而重建方法在低步数下性能急剧下降；（2）NLL+Diff 组合评分在各步数下均优于单独评分方案；（3）EfficientNet-B4 骨干在检测精度和推理速度上均优于 ViT-B 和 DINO-base。

### 5. 局限与展望

尽管 InvAD 在精度和效率上取得了突破，仍存在以下局限：（1）当前仍需 3 步反演，尚未压缩至单步推理；（2）未采用扩散蒸馏等极致加速技术；（3）对于极小尺寸异常，16×16 特征分辨率可能导致细节丢失。未来方向包括探索单步反演蒸馏、设计异常检测特化的反演机制，以及深入理解高维扩散分布下 NLL 评分反向问题的深层原因。

## 背景与动机

异常检测是工业视觉和医学影像等安全关键领域的核心任务，其目标是在仅有正常样本参与训练的条件下，识别偏离正常分布的异常实例。近年来，扩散模型凭借其强大的分布建模能力，逐渐成为异常检测的主流技术路线之一。然而，现有基于扩散模型的方法几乎无一例外地遵循**重建式范式**：先对输入图像施加正向扰动，再通过多步去噪将其重建回原始空间，最终以输入与重建之间的均方误差（MSE）作为异常评分依据。

这一范式面临一个根本性的两难困境。若扰动强度不足，异常区域可能被完整保留，导致正常与异常样本的重建误差难以区分；若扰动强度过大，则正常区域的保真度受损，且多步去噪带来的计算开销急剧攀升。如表1所示，现有扩散式异常检测方法的推理步数（NFE）分布在10至750之间，推理速度普遍受限于数十FPS以内。这种**噪声强度敏感性与计算效率之间的矛盾**，构成了当前重建式方法的瓶颈。

InvAD的动机正源于对这一瓶颈的重新审视。论文提出了一个核心洞察：异常检测的本质在于评估输入样本相对于正常数据分布的偏离程度，而这一偏离完全可以通过扩散模型的正向轨迹来刻画，无需经历完整的去噪重建过程。具体而言，给定一张输入图像，利用DDIM反演沿概率流ODE（PF-ODE）轨迹直接推断其对应的最终扩散隐变量，该隐变量在先验分布（标准高斯）下的典型性即可反映样本的正常程度。这一思路将异常检测的范式从“RGB空间去噪重建”转变为“潜空间加噪反演”，在规避显式重建的同时，从根本上解耦了保真度与效率之间的权衡。

## 核心创新

InvAD 的核心创新在于将异常检测的范式从“RGB 空间去噪重建”彻底转变为“潜空间加噪反演”，从而绕开重建步骤，直击现有扩散式异常检测方法的根本瓶颈。

### 范式转变：从重建到反演

现有扩散式异常检测方法（如 **RD4AD**、**UniAD**、**DiAD** 等）遵循统一的“先扰动再重建”范式：对输入图像施加噪声扰动得到中间隐变量 $\mathbf{x}_t$，再通过多步去噪将其重建回 $\mathbf{x}_0$，最后以输入与重建之间的均方误差（MSE）作为异常评分。这一范式面临两难困境：噪声强度过小则重建过于保真、异常无法凸显；噪声强度过大则需大量去噪步数以保证重建质量，导致推理效率低下。

InvAD 提出了根本性的范式转变（Figure 2）。给定输入图像，方法不再进行重建，而是沿概率流常微分方程（PF-ODE）轨迹直接反演推断该图像在扩散最终步对应的隐变量 $\mathbf{x}_T$。由于扩散模型仅在正常样本上训练，正常图像的 $\mathbf{x}_T$ 将聚集在可处理的先验分布（标准高斯）附近，而异常图像的 $\mathbf{x}_T$ 则会偏离该分布。异常检测由此转化为对隐变量在先验分布下典型性的度量，无需任何显式重建。

这一范式转变的核心机理可概括为：**将“去噪重建”替换为“加噪反演”，将“像素空间保真度”替换为“潜空间典型性”**。

### 关键设计槽位对比

下表总结了 InvAD 相对于重建式基线在五个关键设计槽位上的系统性改变：

| 设计槽位 | 基线方法 | InvAD |
|-----------|----------|-------|
| **检测范式** | RGB 空间去噪重建 | 潜空间加噪反演 |
| **异常评分** | 输入与重建之间的 MSE | 最终隐变量的对数似然（log p）与空间范数差分（NLL+Diff） |
| **推理步数（NFE）** | 10–750（多步去噪） | 3（仅反演，无重建） |
| **是否需重建** | 需要显式重建 | 免重建 |
| **扩散建模空间** | 像素空间（RGB）或 VAE 潜空间 | 预训练骨干网络的特征空间（EfficientNet-B4） |

### 特征空间扩散建模

传统扩散式异常检测在像素空间或 VAE 潜空间建模，关注的是低层纹理和颜色模式。InvAD 将扩散过程迁移至预训练特征提取器（EfficientNet-B4 的 1–4 层特征拼接）的输出空间。这一设计使反演过程能够参照高层语义信息而非低层像素模式，从而更准确地捕捉异常引起的语义偏离。消融实验证实，特征空间扩散建模（FDM）是 InvAD 获得高精度检测和定位能力的关键组件（Table 6）。

### 免重建的高效推理

由于无需多步去噪重建，InvAD 仅需 3 步 DDIM 反演即可完成推理。在 MVTecAD 多类设定下，推理速度达到 88.1 FPS，约为最优重建式基线 **OmiAD**（39.4 FPS）的 2.2 倍，同时图像级 AU-ROC 达到 99.0%，超越所有对比方法（Table 2）。在极低反演步数（S=3）下，InvAD 依然保持 99.0 的 AU-ROC，而重建式方法在低步数下性能急剧下降（Table 4），充分验证了免重建范式在效率与精度上的双重优势。

### 组合评分方案

InvAD 的异常评分由两部分组成：基于最终隐变量 $\mathbf{z}_T$ 的对数似然 $\log p(\mathbf{z}_T)$ 评估整体典型性，以及基于 $\mathbf{z}_T$ 各空间位置 L2 范数的最大值-最小值差分（Diff）捕捉局部异常响应。消融实验表明，NLL+Diff 组合评分显著优于单独使用 NLL 或 Diff，有效缓解了纯 NLL 评分在增加扩散步数时出现的“反向评分”问题（Table 9）。

## 整体框架

InvAD 的整体流程由三个核心模块串联构成：**特征提取器 → DDIM 反演模块 → 异常评分模块**，形成一条从输入图像到异常分数的端到端推理链路，全程无需显式重建。

### 输入输出流

给定一张测试图像 $\mathbf{x}$，首先通过预训练的特征提取器 $g_\phi$ 将其编码为特征图 $\mathbf{z} = g_\phi(\mathbf{x})$。该特征图随后作为 DDIM 反演模块的起点 $\mathbf{z}_0$，沿概率流 ODE (PF-ODE) 轨迹正向积分少量步数，得到最终扩散隐变量 $\mathbf{z}_T$。最后，异常评分模块对 $\mathbf{z}_T$ 每个空间位置的通道维度计算 L2 范数，生成异常热力图，并通过最大值-最小值差分与高值聚合得到图像级异常分数。整个推理过程仅需 3 次函数评估 (NFE=3)，在 NVIDIA RTX 4090 上达到 88.1 FPS（Table 2）。

### 模块关系与范式转变

这一流程的根本创新在于将异常检测的范式从传统的 **“RGB 空间去噪重建”** 转变为 **“潜空间加噪反演”**（Figure 2）。传统重建式方法（如 RD4AD、UniAD、DiAD 等）需要先将输入扰动至中间时刻 $\mathbf{x}_t$，再通过多步去噪重建出 $\hat{\mathbf{x}}_0$，最后计算输入与重建之间的 MSE 作为异常分数。这一范式面临两难困境：噪声强度过小则异常可能被保留在重建中，噪声强度过大则正常区域也会被破坏，且多步去噪带来显著的计算开销。

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/003_Figure_2.jpg]]
*Figure 2: Conceptual comparison of conventional and our proposed AD paradigm. Conventional reconstruction-based paradigm (a) first perturbs a n input sampl e $\protect$ $\mathbf {x}$_0 to a la tent state $\protect$ $\mathbf {x}$_t at step t , and th en den oi ses $\protect$ $\mathbf {x}$_t ba ck t o $\protect$ $\mathbf {x}$_0 . T he ano maly sc ore i s comp uted as the m ean squared error (MSE) between the original input and its reconstructed sample. In contrast, our inversion-based paradigm (b) directly infers the latent state at the final step$, \protect$ $\mathbf {x}$_T , by tracing the PF-ODE trajectories. The anomaly score is then determined based on the typicality of*

InvAD 绕开了这一困境：它不重建图像，而是利用 DDIM 反演直接推断输入图像对应的最终扩散隐变量 $\mathbf{z}_T$。由于扩散模型仅在正常样本上训练，正常图像的 $\mathbf{z}_T$ 应服从标准高斯先验 $\mathcal{N}(\mathbf{0}, \mathbf{I})$，而异常区域的隐变量会偏离这一分布。因此，异常检测被转化为评估 $\mathbf{z}_T$ 在先验分布下的典型性（typicality），无需任何重建步骤。

### 特征空间扩散建模

InvAD 并非在像素空间进行扩散建模，而是在预训练骨干网络的特征空间中进行。具体而言，特征提取器采用 EfficientNet-B4 的第 1 至第 4 层特征图，经拼接后作为扩散模型的输入（Section 3.2）。这一设计使反演过程能够参照高层语义信息而非低层像素模式，从而在保持异常定位精度的同时进一步提升推理效率。消融实验（Table 7）表明，EfficientNet-B4 在检测和定位指标上均优于 ViT-B 和 DINO-base，且推理速度更高。

### 推理算法概要

完整的推理流程如 Algorithm 1 所示：输入图像经特征提取后，在选定的子集时间步 $\tau_S$ 上执行加速 DDIM 反演更新（见公式 $\mathbf{x}_{\tau_{i+1}} = \sqrt{\alpha_{\tau_{i+1}}} f_{\theta}(\mathbf{x}_{\tau_i}) + \sqrt{1-\alpha_{\tau_{i+1}}} \epsilon_{\theta}^{(\tau_i)}(\mathbf{x}_{\tau_i})$），得到最终隐变量 $\mathbf{z}_T$；随后计算每个空间位置的 L2 范数 $\mathbf{z}_T^{\mathrm{normed}}[i,j] = \|\mathbf{z}_T[:,i,j]\|_2$，并通过 NLL+Diff 组合评分方案输出图像级异常分数。

## 核心模块与公式推导

InvAD 由三个核心模块串联构成：**特征提取器**、**DDIM 反演模块**与**异常评分模块**。其本质是将异常检测从“RGB 空间去噪重建”转变为“潜空间加噪反演”，从而绕过显式重建步骤。

### 特征提取器

输入图像 $x$ 首先经过预训练骨干网络 $g_\phi$ 编码为特征图 $z = g_\phi(x)$。论文采用 EfficientNet-B4 的第 1 至第 4 层特征，经双线性插值对齐后沿通道拼接，最终得到分辨率为 $16\times16$ 的特征表示。这一设计使后续扩散建模在高层语义空间进行，而非低层像素模式（Section 3.2）。消融实验表明，EfficientNet-B4 在检测与定位 AU-ROC 以及推理速度上均优于 ViT-B 和 DINO-base（Table 7），且 $16\times16$ 分辨率在所有异常尺寸上取得最优平衡（Table 14）。

### DDIM 反演模块

该模块是 InvAD 范式转换的核心。给定特征图 $x_0$，传统重建方法先加噪至中间步 $t$ 再逐步去噪回 $x_0$，而 InvAD 直接沿概率流常微分方程（PF-ODE）轨迹正向积分至最终步 $T$，推断对应的最终隐变量 $x_T$。PF-ODE 的形式为：

$$
\mathrm{d}\mathbf{y}_t = \epsilon_{\theta}^{(t)} \, \mathrm{d}p_t
$$

其中 $\epsilon_{\theta}^{(t)}$ 是已学习的噪声预测网络，$p_t$ 是单调递增的时间函数。该 ODE 可将数据分布确定性转换为标准高斯先验 $\mathcal{N}(0, I)$，反演即沿此轨迹正向行进。

为加速推理，InvAD 仅使用原始扩散过程的子集时间步 $\tau_S = \{\tau_1, \tau_2, \dots, \tau_S\}$（$S \ll T$）进行反演。离散化后的加速 DDIM 反演更新公式为：

$$
\mathbf{x}_{\tau_{i+1}} = \sqrt{\alpha_{\tau_{i+1}}} \, f_{\theta}(\mathbf{x}_{\tau_i}) + \sqrt{1 - \alpha_{\tau_{i+1}}} \, \epsilon_{\theta}^{(\tau_i)}(\mathbf{x}_{\tau_i}) \tag{7}
$$

其中 $f_{\theta}(\mathbf{x}_{\tau_i}) = \frac{\mathbf{x}_{\tau_i} - \sqrt{1 - \alpha_{\tau_i}} \, \epsilon_{\theta}^{(\tau_i)}(\mathbf{x}_{\tau_i})}{\sqrt{\alpha_{\tau_i}}}$ 是对干净数据 $x_0$ 的估计，$\alpha_t$ 为扩散调度系数。该公式的直觉是：在当前估计的干净信号上叠加与下一步噪声水平匹配的高斯噪声，从而沿 PF-ODE 轨迹推进。实验表明，仅 $S=3$ 步反演即可达到 99.0 图像级 AU-ROC，而重建方法在低步数下性能急剧下降（Table 4）。均匀反演调度（Uniform）在 $S=3$ 时效果最优，优于二次、立方和指数调度（Table 13）。

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/015_Table_13.jpg]]
*Table 13: Inversion schedule ablation under different total diffusion steps S in multi-class MVTecAD with mAD*

扩散模型 $\epsilon_{\theta}$ 在特征空间上以标准 DDPM 目标训练：

$$
\mathcal{L}_{\gamma}(\epsilon_{\theta}) := \sum_{t=1}^{T} \gamma_t \, \mathbb{E}_{\mathbf{x}_0 \sim q(\mathbf{x}_0), \, \epsilon_t \sim \mathcal{N}(0,I)} \left[ \| \epsilon_{\theta}^{(t)}(\mathbf{x}_t) - \epsilon_t \|_2^2 \right] \tag{3}
$$

训练设置 $T=1000$，线性噪声调度，AdamW 优化器，300 epochs（Section 4.4）。

### 异常评分模块

最终隐变量 $z_T$（即 $x_T$）在正常样本上应服从标准高斯先验，而异常样本的 $z_T$ 会偏离该分布。评分模块首先计算 $z_T$ 每个空间位置的通道 L2 范数，生成异常热力图：

$$
\mathbf{z}_T^{\mathrm{normed}}[i,j] = \| \mathbf{z}_T[:, i, j] \|_2 \tag{8}
$$

图像级异常分数由两部分组合：**NLL**（负对数似然）衡量 $z_T$ 在先验分布下的整体典型性；**Diff** 取 $\mathbf{z}_T^{\mathrm{normed}}$ 的最大值与最小值之差，用于缓解纯 NLL 评分在高扩散步数下出现的“反向评分”问题（即异常样本的 NLL 反而低于正常样本）。消融实验证实，NLL+Diff 组合在 $S=3$ 时达到最佳图像级 AU-ROC，优于单独使用 NLL 或 Diff（Table 9）。Figure 4 的直方图对比进一步展示了 NLL+Diff 评分对正常/异常样本区分度的显著改善。

### 模块协同与因果机制

三个模块的协同逻辑是：特征提取器将输入映射到语义特征空间，DDIM 反演沿 PF-ODE 轨迹将特征推向先验分布，评分模块度量最终隐变量与先验的偏离程度。这一设计将异常检测的计算瓶颈从“多步去噪重建”转移到“少步加噪反演”，在保持高保真度的同时将推理步骤数从 10–750 压缩至 3，推理速度达到 88.1 FPS，约为基线方法的 2 倍（Table 1、Table 2）。组件消融进一步验证了特征空间扩散建模（FDM）与多步反演（M-Inv）的组合贡献最优 mAD 83.7（Table 6）。

## 实验与分析

### 核心实验设置

InvAD 的训练与评估覆盖工业与医学两类场景。工业数据集采用 MVTecAD、VisA 和 MPDD，医学数据集采用 BMAD，均以正常样本训练扩散模型（仅使用正常样本，不涉及伪异常生成）。评估指标包括图像级 AU-ROC、像素级 AU-ROC、AP、F1 max、AU-PRO 及推理速度 FPS。所有方法的推理速度均在相同环境下测量（NVIDIA RTX 4090，批量大小 64），扩散模型训练统一使用 DiT 架构、线性噪声规划、总扩散步数 T=1000、AdamW 优化器、300 epoch，特征提取器统一采用 EfficientNet-B4，确保公平可比。

### 主结果：精度-效率双领先

**Table 2** 汇总了多类设定下的定量结果。在 MVTecAD 上，InvAD 取得 99.0 图像级 AU-ROC，超过此前最优方法 OmiAD（98.8），同时推理速度达 88.1 FPS，约为 OmiAD（39.4 FPS）的 2.2 倍。在 VisA 和 MPDD 上，InvAD 分别取得 96.9 和 96.5 图像级 AU-ROC，较 OmiAD 提升 +1.6 和 +2.8。这一精度-效率双重优势在 **Figure 1** 中得到直观呈现：InvAD 位于精度-速度散点图的右上角，显著偏离其他扩散基方法的权衡曲线。

在医学数据集 BMAD 的单类设定下（**Table 3**），InvAD 取得 87.2 mAD，超过 PatchCore（86.4），且推理速度保持显著优势，验证了方法跨领域的泛化能力。

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on BMAD under the single-class setting, where we report image-level AU-ROC (det.), pixel-level AU-ROC (loc.), and FPS. The best and the second-best results are highlighted in bold and underlined, respectively. For each row, the mAD averages the evaluation over all image- and pixel-level metrics. FPS measures the detection efficiency on the RESC dataset*

### 消融实验：范式转换是关键

**Table 4** 直接对比了重建范式与反演范式在不同扩散步数 S 和扰动比率 r 下的表现。重建方法在低步数下性能急剧下降，而 InvAD 仅需 S=3 即达到 99.0 图像级 AU-ROC，甚至超过更高步数设定。这证实了“免重建”范式的核心价值：反演仅需少量步骤即可将输入映射到潜空间的典型性度量，无需经历完整的去噪重建过程。

**Table 6** 的组件消融进一步拆解了各模块的贡献。特征空间扩散模型（FDM）与多步反演（M-Inv）的组合取得最佳 mAD 83.7，单独去除任一组件均导致性能下降，验证了“特征空间建模 + 多步反演”的协同设计。

### 评分方案消融

**Table 9** 考察了不同评分策略的效果。在 S=3 时，NLL+Diff 组合评分达到最佳图像级 AU-ROC，单独使用 NLL 或 Diff 均有明显差距。值得注意的是，随着扩散步数 S 增加，纯 NLL 评分出现反向评分问题（异常样本的 NLL 反而低于正常样本），而引入 Diff 项（基于隐变量范数的最大-最小差分）有效缓解了该问题。**Figure 4** 通过 hazelnut 类别的评分分布直方图直观展示了这一改进：NLL+Diff 评分下正常与异常样本的分布分离度显著优于纯 NLL。

### 骨干网络与扩散架构选择

**Table 7** 的编码器消融显示，EfficientNet-B4 在检测和定位 AU-ROC 上均优于 ViT-B 和 DINO-base，且参数量更少、推理速度更高。特征分辨率 16×16 在所有异常尺寸上取得最优平衡（**Table 14**），8×8 因信息损失过大而性能下降，24×24 则对极小异常定位精度稍逊。

**Table 8** 的扩散架构消融表明，DiT 架构在精度和速度上均优于 UNet，且反演调度采用均匀调度（Uniform）在 S=3 时效果最佳，优于二次、立方和指数调度（**Table 13**）。

### 泛化性与即插即用验证

**Table 5** 展示了 InvAD 作为推理阶段方法的即插即用能力。将其反演机制整合到现有扩散基异常检测方法（如 RD4AD、UniAD 等）后，各方法的图像级和像素级 AU-ROC 均获得提升，同时参数量不变、推理速度基本持平，验证了反演范式的通用性和低侵入性。

### 已知局限与失败模式

尽管 InvAD 在极低步数下表现优异，当前仍需 3 步反演，尚未压缩至单步推理。未采用扩散蒸馏技术进一步加速，可能无法达到极致吞吐量（如 1 NFE）。此外，对于极小异常（tiny size），16×16 特征分辨率可能导致细节丢失，定位精度稍逊于部分专用定位方法。纯 NLL 评分在高扩散步数下的反向评分问题虽被 Diff 项缓解，但其在高维分布下的深层原因仍待进一步探究。

### 补充图表

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/001_Figure_1.jpg]]
*Figure 1: Accuracy v.s. Speed relationship of diffusion-based AD methods [5–9] on MVTecAD. Our proposed InvAD achieves state-of-the-art AD performance with a substantial speedup*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/002_Table_1.jpg]]
*Table 1: Comparison of the properties of diffusion-based AD methods. Normal-only means whether the method involves pseudoanomalies in training, NFE stands for the number of function evaluations, and TS refers to the timestep*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on different AD datasets under the multi-class setting. The best and the second-best results are highlighted in bold and underlined, respectively. For each row, the mAD averages the evaluation over all image- and pixel-level metrics (i.e., the 3rd to the 9th column). FPS measures the detection efficiency*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/007_Table_4.jpg]]
*Table 4: Comparison of reconstruction-based approach (Recon.) against our inversion-based AD paradigm, under different total diffusion steps S and perturbation ratios r, in multi-class MVTecAD with image-level AU-ROC*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/006_Table_6.jpg]]
*Table 6: Component ablation on multi-class MVTecAD. FDM denotes feature space diffusion models. S-Inv and M-Inv denote single- and multi-step inversion, resepectively*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/012_Table_9.jpg]]
*Table 9: Scoring scheme ablation under different total diffusion steps S in multi-class MVTecAD with image-level AU-ROC*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/010_Table_7.jpg]]
*Table 7: Design ablation of feature space encoding modules on multi-class MVTecAD with image- and pixel-level AU-ROC, number of total parameters (#Params), and FPS*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/008_Table_5.jpg]]
*Table 5: Generalizability evaluation of our method when incorporated into other diffusion-based AD approaches on MVTecAD with image- and pixel-level AU-ROC, number of total parameters (#Params) and FPS*

![[assets/figures/papers/paper_list_l2523_https_arxiv_org_abs_2504_05662/figures/011_Table_8.jpg]]
*Table 8: Design ablation of diffusion architectures on multiclass MVTecAD with image- and pixel-level AU-ROC, and FPS*

## 方法谱系与知识库定位

### 1. 范式转移：从“重建-比较”到“反演-评估”

InvAD 的核心贡献在于对扩散异常检测（AD）范式的根本性重构。传统扩散 AD 方法遵循“扰动-重建-比较”路径：将输入图像加噪至某中间时间步，再通过多步去噪重建干净图像，最后在像素或特征空间计算输入与重建之间的均方误差（MSE）作为异常分数。InvAD 将这一范式替换为“反演-评估”：沿概率流 ODE（PF-ODE）轨迹直接推断输入图像对应的最终扩散隐变量 $\mathbf{x}_T$，并基于该隐变量在已知先验分布（标准高斯）下的典型性进行异常评分，完全绕过显式重建步骤。

这一范式转移的因果逻辑在于：正常样本经过训练好的扩散模型反演后，其最终隐变量应高度符合先验分布；异常区域由于偏离训练分布，反演得到的隐变量在对应空间位置会表现出显著偏离。因此，异常检测从“重建误差度量”转变为“潜空间典型性检验”，从根源上解耦了检测精度与去噪重建质量之间的依赖关系。

### 2. 与现有扩散异常检测方法的关系定位

**Table 1** 系统对比了 InvAD 与现有扩散 AD 方法的属性差异。以下从几个关键维度展开分析：

**推理效率瓶颈的突破。** 现有重建式方法（如 **RD4AD**、**UniAD**、**DiAD**、**MDM**）需要 10–750 次函数评估（NFE）来完成去噪重建，推理速度受限。InvAD 仅需 3 步反演（NFE=3），在 MVTecAD 上达到 88.1 FPS，约为第二名 **OmiAD**（39.4 FPS）的 2.2 倍。这一效率提升并非来自工程优化，而是范式层面的结构性优势：反演只需正向积分少量步数，无需逆向去噪。

**训练数据需求的简化。** 部分方法（如 **DeSTSeg**、**SimpleNet**）需要在训练中引入伪异常样本，这在实际工业场景中增加了数据构造的复杂性和领域迁移成本。InvAD 属于“仅正常样本”（Normal-only）方法，训练仅需正常图像，降低了部署门槛。

**特征空间建模的先发优势。** 现有方法多在像素空间或 VAE 潜空间进行扩散建模，关注低层级纹理重建。InvAD 在预训练 EfficientNet-B4 的特征空间进行扩散建模，使反演过程能够参照高层语义信息。这一设计并非孤立创新——**OmiAD** 等近期工作也探索了特征空间建模——但 InvAD 将其与反演范式结合，在语义保真度和推理效率之间取得了新的平衡点。

**泛化性验证。** **Table 5** 将 InvAD 的反演推理方式以即插即用形式集成到其他扩散 AD 方法（如 RD4AD、UniAD、DiAD、MDM）中，结果表明各方法的图像级和像素级 AU-ROC 均获得提升，同时参数量无显著增加。这说明“反演化”推理并非与特定模型绑定，而是可作为通用推理策略迁移至现有扩散 AD 框架。

### 3. 适用边界与局限

尽管 InvAD 在多个基准上表现优异，其适用边界和局限值得明确：

**推理步数的下限。** 当前方法仍需 3 步反演评估，尚未压缩至单步推理。消融实验（**Table 4**）显示，S=1 时图像级 AU-ROC 明显下降，说明极低步数下 PF-ODE 轨迹近似精度不足，无法可靠推断最终隐变量。这与扩散蒸馏领域追求 1 NFE 的目标存在差距。

**极小异常的定位精度。** **Table 14** 显示，16×16 特征分辨率在所有异常尺寸上取得最优平衡，但对于极小异常（tiny size），该分辨率可能导致空间细节丢失，定位精度稍逊。这是特征空间建模固有的空间分辨率与语义抽象之间的权衡。

**反向评分问题的部分缓解。** 纯负对数似然（NLL）评分在增加扩散步数时会出现“反向评分”问题——正常样本的 NLL 值反而高于异常样本。InvAD 通过 NLL+Diff 的组合评分方案（**Table 9**）缓解了这一问题，但并未从理论上根除。**Figure 4** 的直方图对比显示，组合评分使正常与异常样本的分布分离度显著提升，但仍有少量重叠区域。该现象的深层原因——高维分布下 NLL 评分的非单调性——仍是开放问题。

**扩散蒸馏技术的缺失。** InvAD 未采用渐进式蒸馏（progressive distillation）或一致性模型（consistency models）等加速技术，在极致吞吐量场景（如实时产线检测）下可能无法满足 1 NFE 级别的延迟要求。

### 4. 开放问题

从 InvAD 的设计逻辑和实验发现出发，可提炼以下开放问题：

1. **单步反演的可行性。** 能否利用扩散蒸馏技术将渐进式反演过程压缩为单步，实现 1 NFE 推理？这需要在轨迹近似精度和推理效率之间找到新的平衡点，可能需要设计针对异常检测任务特化的蒸馏目标。

2. **任务特化的反演机制。** 当前反演直接复用 DDIM 的 PF-ODE 轨迹，未针对异常检测任务进行优化。是否存在更适合异常检测的反演路径——例如在反演过程中显式放大异常区域的潜空间偏离——值得探索。

3. **高维 NLL 评分的理论理解。** 为何纯 NLL 评分在增加扩散步数时出现反向评分？这是高维分布下概率密度估计的固有缺陷，还是与扩散模型的训练方式有关？该问题的解答可能推动更鲁棒的异常评分方案设计。

4. **跨域泛化的边界。** InvAD 在工业检测（MVTecAD、VisA、MPDD）和医学影像（BMAD）上均取得领先结果，但其在更复杂场景（如视频异常检测、3D 异常检测）中的适用性尚未验证。特征空间扩散模型在不同域的特征提取器选择上可能需要领域适配。

## 原文 PDF

![[paperPDFs/CVPR_2026/InvAD_Inversion_based_Reconstruction_Free_Anomaly_Detection_with_Diffusion_Models.pdf]]