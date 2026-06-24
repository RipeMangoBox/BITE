---
title: "SpeeDiff: Scalable Pixel-Anchored End-to-End Latent Diffusion Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpeeDiff_Scalable_Pixel_Anchored_End_to_End_Latent_Diffusion_Model.pdf
project_link: null
code_link: null
aliases:
- SpeeDiff
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: Tweedie Pixel Reconstruction (TPR)损失通过解码Tweedie公式估计的干净潜在并施加像素级重建监督，为VAE提供了额外的约束，将扩散损失梯度与像素空间内容锚定，从而防止潜在崩溃。
primary_logic: 利用Tweedie公式从任意噪声时间步的潜在变量中预测干净潜在，再将其解码与原图比较，可在不中断梯度回传的前提下为VAE注入语义保持的生成式监督，实现了稳定、高效的端到端联合训练。
claims:
- Vanilla E2E训练导致潜在误差几乎为零而像素误差仍然很大，说明潜在空间已退化。
- 添加TPR损失后，FID从33.95大幅降至5.79，生成质量显著提升。
- TPR损失能维持潜在空间的标准化分布，避免出现尖锐峰态和极大偏置。
- ImageNet 256x256 (80 epochs) 上 gFID (no guidance) = 1.69 (SpeeDiff-XL w/ REPA++)
---

# SpeeDiff: Scalable Pixel-Anchored End-to-End Latent Diffusion Model

> [!tip] 核心洞察
> 利用Tweedie公式从任意噪声时间步的潜在变量中预测干净潜在，再将其解码与原图比较，可在不中断梯度回传的前提下为VAE注入语义保持的生成式监督，实现了稳定、高效的端到端联合训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | SpeeDiff：可扩展的像素锚定端到端潜在扩散模型 |
| 英文题名 | SpeeDiff: Scalable Pixel-Anchored End-to-End Latent Diffusion Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_SpeeDiff_Scalable_Pixel-Anchored_End-to-End_Latent_Diffusion_Model_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SpeeDiff |
| Dataset | ImageNet 256x256, ImageNet 512x512 |

> [!tip] 效果简介
> - ImageNet 256x256 (80 epochs) 上，gFID (no guidance) 1.69 (SpeeDiff-XL w/ REPA++) vs 21.80 (Vanilla SiT) / 6.88 (REPA) (显著提升)；gFID (no guidance) 3.35 (SpeeDiff-XL w/o REPA++) vs 约9-10 (DiT, SiT two-stage) (大幅提升)。
> - ImageNet 512x512 (80 epochs) 上，gFID (no guidance) 1.53 (SpeeDiff-XL w/ REPA++) vs — (state-of-the-art)。
> - ImageNet 512x512 上，IS (with guidance) 322.55 vs — (—)。

## 概述

**问题瓶颈**：传统潜在扩散模型（LDM）采用两阶段训练——先独立训练VAE，冻结后再训练扩散模型。若尝试直接端到端联合训练VAE与扩散模型（Vanilla E2E），扩散损失会朝向退化方向驱动潜在空间，导致**潜在表示崩溃**：通道方差被极度压制、偏置极大，扩散模型可通过输出接近常数的预测来最小化损失，却丢失了图像重建所需的语义信息。实验显示，此时潜在误差几乎为零，而像素误差仍然很大（Fig. 3a），FID高达33.95。

**核心方法**：SpeeDiff提出一种**像素锚定的端到端潜在扩散框架**，核心创新在于**Tweedie Pixel Reconstruction (TPR)损失**——利用Tweedie公式从任意噪声时间步的潜在变量中估计干净潜在，解码后与原图进行像素级MSE比较。该损失在不中断梯度回传的前提下，为VAE注入语义保持的生成式监督，将扩散损失梯度与像素空间内容锚定，从而**稳定、高效地实现从零开始的端到端联合训练**。

**训练效率**：在ImageNet 256×256生成任务上，SpeeDiff相比Vanilla SiT加速超过**140倍**，相比REPA加速**61倍**（Fig. 1c）。添加TPR损失后，FID从33.95大幅降至5.79（80 epochs）。

**主要结果**：SpeeDiff-XL在ImageNet 256×256上无引导FID达到**1.69**（w/ REPA++），在512×512上达到**1.53**，Inception Score达322.55（with guidance），均为当前最优水平。预训练的VAE可冻结后独立使用，收敛速度与端到端训练几乎一致（gFID 1.73 vs 1.69）。

**方法定位**：SpeeDiff属于**端到端潜在扩散模型**，与两阶段方法（DiT-XL/2、SiT-XL/2）和表示对齐方法（REPA）形成对比。其技术栈包括ViT-VAE、Refined-DiT扩散骨干、TPR损失和REPA++表示对齐，形成完整的单阶段训练范式。

## 背景与动机

### 潜在扩散模型的两阶段范式及其困境

潜在扩散模型（Latent Diffusion Models, LDMs）已成为高分辨率图像生成的主流框架。其核心思想是将生成过程分解为两个阶段：首先训练一个变分自编码器（VAE）将图像压缩到低维潜在空间，然后冻结VAE，在该潜在空间上训练扩散模型。这一范式在Stable Diffusion等大规模系统中取得了显著成功。

然而，这种两阶段分离训练存在一个根本性的结构缺陷：**VAE和扩散模型被孤立优化，潜在空间一旦训练完成便不再更新**。这意味着潜在表示仅由重建目标驱动，从未接收来自生成任务的梯度反馈。扩散模型被迫在一个并非为其优化的潜在空间中进行生成，这限制了生成质量的上限，也使得整个系统无法通过联合优化获得协同增益。

### 端到端联合训练的核心瓶颈：潜在崩溃

一个自然的改进思路是将VAE和扩散模型进行端到端（End-to-End, E2E）联合训练，让扩散损失直接回传梯度至VAE编码器。然而，直接这样做会导致灾难性的**潜在崩溃（latent collapse）**。

具体而言，当扩散损失可以影响VAE编码器时，优化过程会朝向一个退化方向驱动潜在空间：编码器学会产生方差极度压制、偏置极大的潜在表示。此时扩散模型只需输出接近常数的预测即可最小化其损失，但潜在空间几乎丧失了所有语义信息，导致解码器无法重建有意义的图像。如Figure 3a所示，Vanilla E2E训练下潜在误差几乎为零，而像素误差仍然很大——这正是潜在空间已退化的明确信号。

这一现象的深层原因在于：扩散损失本质上是潜在空间内的均方误差，缺乏对像素级内容的直接约束。当VAE编码器可以自由调整潜在空间的尺度和分布时，最小化扩散损失与保持语义信息这两个目标之间存在冲突，而优化过程会优先选择“容易”的退化解。

### 现有缓解方案的局限

针对上述问题，已有工作尝试了不同的缓解策略。**REPA**（Yu et al., ICLR 2025）通过将扩散模型的中间特征与预训练视觉基础模型（VFM）的表示进行对齐，为训练注入了语义监督，在一定程度上缓解了退化。但REPA本质上仍是一种间接的表示对齐方法，并未从根本上解决像素级反馈缺失的问题，其收敛速度和最终生成质量仍受限于分离训练范式的固有瓶颈。

### 本文动机与核心思路

本文的核心动机在于：**是否存在一种机制，能够在端到端联合训练中为VAE提供稳定的像素级约束，从根本上防止潜在崩溃，从而释放联合优化的全部潜力？**

SpeeDiff给出的答案是肯定的。其关键洞察在于利用**Tweedie公式**——该公式能够从任意噪声时间步的潜在变量中估计出对应的干净潜在——将扩散过程的中间状态解码回像素空间，并与原始图像计算重建损失。这一**Tweedie Pixel Reconstruction (TPR)损失**在不中断梯度回传的前提下，将扩散损失梯度与像素空间内容锚定，为VAE提供了保持语义所需的生成式监督。

在此基础上，SpeeDiff进一步通过全Transformer架构（ViT-VAE + Refined-DiT）和增强的表示对齐策略（REPA++），构建了一个可扩展的端到端潜在扩散框架。如Figure 1c所示，该框架相比Vanilla SiT实现了超过140倍的训练加速，相比REPA加速61倍，在ImageNet 256×256和512×512生成任务上均达到了state-of-the-art性能。

## 核心创新

SpeeDiff 的核心创新在于将潜在扩散模型的训练范式从传统的“先训 VAE、后训扩散”两阶段分离模式，转变为**端到端联合训练**，并通过**Tweedie Pixel Reconstruction (TPR) 损失**解决了直接联合训练导致的潜在空间崩溃问题。以下从改变的关键维度展开。

### 训练范式：从分离到端到端

传统潜在扩散模型（如 **DiT-XL/2**，Peebles and Xie, ICCV 2023；**SiT-XL/2**，Ma et al., ECCV 2024）采用两阶段训练：先独立训练一个 CNN-based VAE，然后冻结 VAE，在其潜在空间上训练扩散模型。这种分离模式切断了扩散损失对 VAE 的梯度反馈，虽然稳定，但 VAE 无法从生成任务中获得优化信号。

SpeeDiff 将这一范式改为**端到端联合训练**：VAE 和扩散模型从零开始同时优化，不施加任何 stop-gradient 操作（Figure 1b）。训练目标在形式上可写为：

$$\mathcal{L}_{\mathrm{Vanilla-E2E}}(\phi,\psi,\pmb{\theta}) = \mathcal{L}_{\mathrm{VAE}}(\phi,\psi) + \mathcal{L}_{\mathrm{Diff}}(\phi,\pmb{\theta})$$

其中 $\phi$ 为 VAE 编码器参数，$\psi$ 为解码器参数，$\pmb{\theta}$ 为扩散模型参数。$\mathcal{L}_{\mathrm{Diff}}$ 采用流匹配形式，训练网络预测速度场：

$$\mathcal{L}_{\mathrm{Diff}}(\phi^{-},\theta) = \mathbb{E}_{\mathbf{z}_0,\epsilon,t}\left[\|V_{\theta}(\mathbf{z}_t,t) - (\epsilon - \mathbf{z}_0)\|_2^2\right]$$

然而，直接使用上述 Vanilla E2E 目标会导致严重问题：扩散损失会驱动潜在空间朝向退化方向演变——通道方差被极度压制、偏置极大，使得扩散模型可以通过输出接近常数的预测来最小化损失，却丢失了图像重建所需的语义信息。实验证据表明，Vanilla E2E 训练后潜在误差几乎为零，而像素误差仍然很大（Figure 3a），生成质量极差（ImageNet 256×256 上 80 epochs 的 FID 高达 33.95）。

### 关键机制：Tweedie Pixel Reconstruction 损失

为解决 Vanilla E2E 的潜在崩溃，SpeeDiff 引入了 **Tweedie Pixel Reconstruction (TPR) 损失**作为核心正则化手段。其设计思路是：利用 Tweedie 公式从任意噪声时间步 $t$ 的潜在变量 $\mathbf{z}_t$ 中估计干净潜在 $\hat{\mathbf{z}}_0$，再通过 VAE 解码器 $\mathcal{D}_{\psi}$ 解码，与原始图像 $\mathbf{x}_0$ 计算像素级 MSE：

$$\mathcal{L}_{\mathrm{TPR}}(\phi,\psi,\pmb{\theta}) = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,\epsilon,t}\left[\left\|\mathcal{D}_{\psi}(\hat{\mathbf{z}}_0) - \mathbf{x}_0\right\|^2\right]$$

这一设计的因果作用在于：TPR 损失将扩散损失的梯度通过像素空间内容“锚定”，为 VAE 提供了额外的语义保持约束。Figure 3 的三组诊断实验提供了决定性证据：(a) 添加 TPR 后，潜在空间保留了有意义的重建信号；(b) KDE 可视化显示 TPR 使潜在分布保持标准化，避免 Vanilla E2E 中出现的尖锐峰态；(c) 通道统计表明 TPR 维持了均衡的通道偏置和方差，防止了 Vanilla E2E 中极大的偏置和被压制的方差。

从定量效果看，TPR 损失将 ImageNet 256×256 上的 FID 从 33.95 大幅降至 5.79（80 epochs），使端到端训练从完全失败变为可行。进一步结合后续改进后，SpeeDiff 在无 guidance 条件下达到 gFID 1.69 的 SOTA 水平。

### 架构升级：ViT-VAE 与 Refined-DiT

在基础训练框架之上，SpeeDiff 对 VAE 和扩散骨干网络进行了架构层面的改进：

- **ViT-VAE**：用 Vision Transformer 替代传统卷积 VAE（CNN-VAE）。编码器采用 patch embedding 层后接 transformer blocks，解码器镜像此结构。这一替换使训练计算量从 436.29 GFLOPs 降至 334.98 GFLOPs，同时 FID 提升至 3.66。
- **Refined-DiT**：在标准 DiT 基础上集成 RMSNorm、SwiGLU 激活函数、2D RoPE 位置编码，并将逐块调制层替换为共享全局调制机制，进一步提升效率与性能。

### 表示对齐增强：REPA++

为进一步提升生成质量，SpeeDiff 提出了 **REPA++** 策略，同时对齐两个层级的表示至预训练视觉基础模型（VFM，默认使用 DINOv3-L）：

- **Latent-REPA**：对齐干净潜在 $\mathbf{z}_0$ 与 VFM 表示：

$$\mathcal{L}_{\mathrm{Latent-REPA}}(\phi,\omega_1) = -\mathbb{E}_{\mathbf{z}_0,\mathbf{x}_0,k}\big[\mathrm{sim}(h_{\omega_1}^k(\mathbf{z}_0), \mathbf{y}^k)\big]$$

- **Diff-REPA**：对齐中间扩散特征 $\mathbf{f}_t$ 与 VFM 表示：

$$\mathcal{L}_{\mathrm{Diff-REPA}}(\phi,\pmb{\theta},\omega_2) = -\mathbb{E}_{\mathbf{z}_0,\mathbf{x}_0,k}\big[\mathrm{sim}(h_{\omega_2}^k(\mathbf{f}_t), \mathbf{y}^k)\big]$$

两者通过简单相加组合，最终 SpeeDiff 的总体训练目标为：

$$\mathcal{L}_{\mathrm{SpeeDiff}}(\phi,\psi,\theta,\omega) = \mathcal{L}_{\mathrm{VAE}} + \mathcal{L}_{\mathrm{Diff}} + \mathcal{L}_{\mathrm{TPR}} + \mathcal{L}_{\mathrm{REPA++}}$$

消融实验（Table 5）证实，同时使用 Latent-REPA 和 Diff-REPA 的完整 REPA++ 取得最佳 gFID，且 DINOv3-L 优于 DINOv2 或 CLIP 作为对齐目标。

### 训练效率的质变

端到端训练不仅提升了生成质量，还带来了训练效率的阶跃式提升。如 Figure 1c 所示，SpeeDiff 相比 Vanilla SiT 加速超过 **140 倍**，相比 **REPA**（Yu et al., ICLR 2025）加速 **61 倍**。这一加速源于联合训练使 VAE 能直接从扩散梯度中学习更具判别性的潜在表示，而非依赖分离训练中缓慢的独立优化。

### 方法谱系与知识库定位

SpeeDiff 的方法贡献可定位于以下交叉点：

| 维度 | 基线方法 | SpeeDiff 创新 |
|------|----------|---------------|
| 训练范式 | 两阶段分离（DiT, SiT） | 端到端联合训练，无 stop-gradient |
| 潜在正则化 | 无像素级反馈 | TPR 损失锚定像素空间 |
| VAE 架构 | CNN-VAE | ViT-VAE（transformer-based） |
| 扩散骨干 | 标准 DiT | Refined-DiT（RMSNorm, SwiGLU, RoPE） |
| 表示对齐 | REPA（仅对齐中间特征） | REPA++（同时对齐潜在与中间特征） |

值得指出的是，SpeeDiff 预训练的 VAE 可独立冻结使用：在其上训练新扩散模型的收敛速度与端到端训练几乎一致（80 epochs gFID 1.73 vs 1.69，Table 4），表明端到端训练产生的 VAE 具有良好的可迁移性。

**局限性提示**：目前 SpeeDiff 仅在类别条件 ImageNet 生成上验证，扩展到文本到图像等更复杂任务仍需探索；达到最佳性能依赖 DINOv3 等预训练 VFM，带来了额外计算开销；端到端训练的动态稳定性在更大规模下的表现尚待进一步验证。

## 整体框架

SpeeDiff 构建了一个**单阶段端到端潜在扩散训练范式**，核心目标是打破传统两阶段训练的分离瓶颈——即先独立训练 VAE 再冻结并训练扩散模型——转而从零开始联合优化 VAE 与扩散模型，且**全程不使用 stop-gradient 操作**（Fig. 1b）。

### 训练管道四分支结构

整个前向传播由四个并行分支构成（Fig. 2）：

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/002_Figure_2.jpg]]
*Figure 2: Detailed training pipeline of SpeeDiff. The forward pass consists of four major branches: (1) Reconstruction branch: LVAE is computed over reconstructions from the VAE encoder and decoder. (2) Diffusion branch: follows the standard stochastic interpolant and leverages flow prediction as diffusion loss. (3) Tweedie Pixel Reconstruction branch: clean latents are estimated via Tweedie’s formula, decoded, and compared against ground-truth images. (4) REPA++ branch: both latents and intermediate diffusion features are aligned with VFM representations. Notably, SpeeDiff doesn’t requires stop-gradient operation and train both VAE and diffusion from scratch*

1. **重建分支（Reconstruction Branch）**：遵循标准 VAE 框架，编码器 $E_\phi$ 将输入图像 $\mathbf{x}_0$ 映射为潜在变量 $\mathbf{z}_0$，解码器 $\mathcal{D}_\psi$ 从 $\mathbf{z}_0$ 重建图像，计算标准 VAE 损失 $\mathcal{L}_{\mathrm{VAE}}$（含重建损失与 KL 正则项）。

2. **扩散分支（Diffusion Branch）**：采用随机插值公式 $\mathbf{z}_t = (1-t)\mathbf{z}_0 + t\epsilon$ 对潜在变量进行前向加噪，扩散模型（Refined-DiT）预测速度场 $V_\theta(\mathbf{z}_t, t)$，以流匹配损失 $\mathcal{L}_{\mathrm{Diff}}$ 进行训练。该分支的梯度通过编码器 $\phi$ 回传，使 VAE 同时受到生成式目标的驱动。

3. **Tweedie 像素重建分支（Tweedie Pixel Reconstruction Branch）**：这是防止潜在崩溃的关键组件。从任意噪声时间步 $t$ 的潜在 $\mathbf{z}_t$ 出发，利用 Tweedie 公式估计干净潜在 $\hat{\mathbf{z}}_0$，再经解码器重建为像素空间图像，与原始图像 $\mathbf{x}_0$ 计算像素级 MSE：
   $$\mathcal{L}_{\mathrm{TPR}}(\phi,\psi,\pmb{\theta}) = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,\epsilon,t}\left[\left\|\mathcal{D}_{\psi}(\hat{\mathbf{z}}_0) - \mathbf{x}_0\right\|^2\right]$$
   该损失将扩散损失的梯度通过像素空间内容“锚定”，为 VAE 提供语义保持的生成式监督，从而防止潜在表示退化。

4. **REPA++ 表示对齐分支（REPA++ Branch）**：同时对两个层级进行语义对齐——**Latent-REPA** 将干净潜在 $\mathbf{z}_0$ 的投影与视觉基础模型（VFM，默认 DINOv3-L）的表示最大化 patch-wise 余弦相似度；**Diff-REPA** 将扩散模型中间层特征 $\mathbf{f}_t$ 的投影同样与 VFM 表示对齐。两者通过简单相加构成完整的 REPA++ 损失。

### 总体目标函数

四个分支的损失联合构成 SpeeDiff 的总体训练目标：
$$\mathcal{L}_{\mathrm{SpeeDiff}}(\phi,\psi,\theta,\omega) = \mathcal{L}_{\mathrm{VAE}} + \mathcal{L}_{\mathrm{Diff}} + \mathcal{L}_{\mathrm{TPR}} + \mathcal{L}_{\mathrm{REPA++}}$$

其中 $\phi$、$\psi$、$\theta$、$\omega$ 分别对应 VAE 编码器、解码器、扩散模型以及 REPA++ 投影网络的参数，所有参数在训练中同步更新，无冻结或梯度截断。

### 架构选型

SpeeDiff 采用全 Transformer 架构替代传统卷积设计：

- **ViT-VAE**：编码器使用 patch embedding 层后接多个 Transformer block，解码器镜像对称结构，替代传统 CNN-VAE。
- **Refined-DiT**：在标准 DiT 基础上集成 RMSNorm、SwiGLU 激活、2D RoPE 位置编码，并将逐块调制层替换为共享全局调制机制，在降低计算量的同时提升生成质量。

### 数据流概要

输入图像 $\mathbf{x}_0$ → ViT-VAE 编码器 → 潜在变量 $\mathbf{z}_0$ → 分两路：(i) 直接解码重建，计算 $\mathcal{L}_{\mathrm{VAE}}$；(ii) 经随机插值加噪得到 $\mathbf{z}_t$，由 Refined-DiT 预测速度场，计算 $\mathcal{L}_{\mathrm{Diff}}$；同时从 $\mathbf{z}_t$ 经 Tweedie 公式估计 $\hat{\mathbf{z}}_0$ 并解码，计算 $\mathcal{L}_{\mathrm{TPR}}$；$\mathbf{z}_0$ 和中间扩散特征 $\mathbf{f}_t$ 分别与 VFM 表示对齐，计算 $\mathcal{L}_{\mathrm{REPA++}}$。所有梯度无阻断地回传至全部可训练参数。

### 补充图表

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SpeeDiff for end-to-end joint training of VAE and diffusion model from scratch. (a) Conventional two-stage LDM training: a CNN-based VAE [28] is first trained and then frozen, after which a diffusion (usually a DiT [41]) is trained on its latent space. (b) SpeeDiff: a scalable, pixel-anchored end-to-end paradigm that jointly trains the VAE and diffusion model from scratch, without stop-gradient operation, within a fully transformer-based architecture. (c) Training efficiency: on ImageNet 256ˆ256 generation, SpeeDiff accelerates convergence by over 140ˆ compared to Vanilla SiT and 61ˆ compared to REPA. (d) Scalability: on ImageNet 512ˆ512 generation, SpeeDiff demonstrates clear s...*

## 核心模块与公式推导

### 核心瓶颈：Vanilla E2E训练中的潜在崩溃

传统两阶段LDM（如**DiT-XL/2**，Peebles and Xie, ICCV 2023）先独立训练VAE再冻结训练扩散模型。直接端到端联合训练（Vanilla E2E）看似更简洁，其目标为VAE损失与扩散损失的简单相加：

$$\mathcal{L}_{\mathrm{Vanilla-E2E}}(\phi,\psi,\pmb{\theta}) = \mathcal{L}_{\mathrm{VAE}}(\phi,\psi) + \mathcal{L}_{\mathrm{Diff}}(\phi,\pmb{\theta})$$

其中$\phi$、$\psi$、$\pmb{\theta}$分别为VAE编码器、解码器与扩散模型的参数。然而，这一朴素方案会导致**潜在表示崩溃**：扩散损失会驱动潜在空间朝向退化方向演变，使通道方差被极度压制、偏置极大，扩散模型仅需输出接近常数的预测即可最小化损失，却丢失了图像重建所需的语义信息。证据显示（Figure 3a），Vanilla E2E训练后潜在误差几乎为零，而像素误差仍然很大；在ImageNet 256×256上80 epochs后FID高达33.95。

### 关键因果调节器：Tweedie Pixel Reconstruction (TPR) 损失

为锚定潜在空间与像素内容的联系，SpeeDiff引入**Tweedie Pixel Reconstruction (TPR) 损失**。其核心机制是：从任意噪声时间步$t$的潜在变量$\mathbf{z}_t$出发，利用Tweedie公式估计干净潜在$\hat{\mathbf{z}}_0$，再通过解码器$\mathcal{D}_\psi$解码为像素空间并与原图$\mathbf{x}_0$计算像素级MSE：

$$\mathcal{L}_{\mathrm{TPR}}(\phi,\psi,\pmb{\theta}) = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,\epsilon,t}\left[\left\|\mathcal{D}_{\psi}(\hat{\mathbf{z}}_0) - \mathbf{x}_0\right\|^2\right]$$

其中$\hat{\mathbf{z}}_0$由扩散模型$\pmb{\theta}$通过Tweedie公式从$\mathbf{z}_t$估计得到。该损失的关键作用在于：**在不中断梯度回传的前提下，为VAE注入语义保持的生成式监督**——扩散损失梯度通过解码器反向传播至VAE编码器时，TPR损失强制像素空间内容约束，从而防止潜在崩溃。实验表明，添加TPR损失后，ImageNet 256×256上80 epochs的FID从33.95大幅降至5.79；同时潜在空间维持标准化分布，避免尖锐峰态和极大偏置（Figure 3b, 3c）。

### 扩散分支：流匹配目标

扩散分支采用标准随机插值公式进行流匹配，训练网络$V_\theta$预测速度场：

$$\mathcal{L}_{\mathrm{Diff}}(\phi^{-},\theta) = \mathbb{E}_{\mathbf{z}_0,\epsilon,t}\left[\|V_{\theta}(\mathbf{z}_t,t) - (\epsilon - \mathbf{z}_0)\|_2^2\right]$$

其中$\mathbf{z}_t = (1-t)\mathbf{z}_0 + t\epsilon$，$\phi^{-}$表示VAE编码器参数在此处被冻结（stop-gradient）。该分支与**SiT-XL/2**（Ma et al., ECCV 2024）的流匹配范式一致。

### 表示对齐分支：REPA++

SpeeDiff扩展了**REPA**（Yu et al., ICLR 2025）的表示对齐策略，提出REPA++，同时对齐两类表示至预训练视觉基础模型（VFM，默认DINOv3-L）：

- **Latent-REPA**：最大化干净潜在$\mathbf{z}_0$经映射网络$h_{\omega_1}$后与VFM表示$\mathbf{y}$的patch-wise余弦相似度：
  $$\mathcal{L}_{\mathrm{Latent-REPA}}(\phi,\omega_1) = -\mathbb{E}_{\mathbf{z}_0,\mathbf{x}_0,k}\big[\sin(h_{\omega_1}^k(\mathbf{z}_0), \mathbf{y}^k)\big]$$

- **Diff-REPA**：最大化中间扩散特征$\mathbf{f}_t$经映射网络$h_{\omega_2}$后与VFM表示的相似度：
  $$\mathcal{L}_{\mathrm{Diff-REPA}}(\phi,\pmb{\theta},\omega_2) = -\mathbb{E}_{\mathbf{z}_0,\mathbf{x}_0,k}\big[\mathrm{sim}(h_{\omega_2}^k(\mathbf{f}_t), \mathbf{y}^k)\big]$$

完整REPA++损失为两者之和，消融实验表明同时使用Latent-REPA和Diff-REPA取得最佳gFID（Table 5）。

### 总体训练目标

SpeeDiff的完整训练目标为上述四个分支的联合优化：

$$\mathcal{L}_{\mathrm{SpeeDiff}}(\phi,\psi,\theta,\omega) = \mathcal{L}_{\mathrm{VAE}} + \mathcal{L}_{\mathrm{Diff}} + \mathcal{L}_{\mathrm{TPR}} + \mathcal{L}_{\mathrm{REPA++}}$$

该目标中，**重建分支**（$\mathcal{L}_{\mathrm{VAE}}$）提供标准VAE ELBO损失（重建+KL）；**扩散分支**提供流匹配监督；**TPR分支**锚定像素空间内容；**REPA++分支**注入语义对齐信号。四者协同使得VAE与扩散模型可从零开始端到端联合训练，无需任何stop-gradient操作。

### 补充图表

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/003_Figure_3.jpg]]
*Figure 3: Impact of end-to-end training on latent space. (a) Comparing the denoised latent with its clean counterpart in both latent and pixel space reveals that vanilla end-to-end training collapses the latent representation, while TPR loss preserves meaningful reconstruction signals. (b) KDE visualizations show that vanilla training produces highly peaked, non-Gaussian latent distributions, whereas TPR regularizes the latent space and prevents degeneracy. (c) Channel-wise statistics further indicate that vanilla training induces large per-channel biases and severely suppressed variances, whereas TPR maintains a more balanced and normalized latent representation. Results are computed over 1000 valid...*

## 实验与分析

### 核心瓶颈与关键消融：从潜在崩溃到稳定端到端训练

SpeeDiff 的核心消融路径（Table 1）清晰地揭示了端到端联合训练 VAE 与扩散模型所面临的根本性挑战：**Vanilla E2E** 训练（即简单地将 VAE 损失与扩散损失相加）会导致灾难性的潜在空间崩溃，其生成质量（gFID 33.95）远差于传统两阶段分离训练（gFID 21.80）。崩溃的机理在 Figure 3 中得到了充分诊断——潜在误差几乎为零，而像素误差仍然很大，说明扩散模型通过将潜在表示推向一个几乎常数的退化分布来最小化损失，完全牺牲了语义重建能力。

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/004_Table_1.jpg]]
*Table 1: From baseline to SpeeDiff. We evaluate FID without guidance on ImageNet 256ˆ256 generation after 80 training epochs*

引入 **Tweedie Pixel Reconstruction (TPR) 损失** 是扭转局面的关键操作。TPR 利用 Tweedie 公式从任意噪声时间步的潜在变量中估计干净潜在，将其解码后与原图计算像素级 MSE，从而为 VAE 注入像素空间的内容锚定信号。这一设计使得 gFID 从 33.95 大幅降至 5.79，证明了像素级反馈是防止潜在崩溃的充分条件。进一步地，在 TPR 的基础上叠加 **REPA++** 表示对齐（同时对齐潜在向量和中间扩散特征至 DINOv3 视觉基础模型），gFID 进一步优化至 1.69，且端到端训练始终优于分离训练变体（Table 1 中 E2E 行 vs. Detached 行）。

### ImageNet 256×256 生成基准

Table 2 报告了 ImageNet 256×256 上的完整生成基准。在无引导设置下，**SpeeDiff-XL（含 REPA++）** 以 gFID 1.69 达到最优，显著优于同类端到端或表示对齐方法，如 **REPA**（SiT-XL/2，gFID 6.88，Yu et al., ICLR 2025）和 **MDTv2-XL**（gFID 2.53，Gao et al., arXiv 2023）。即便不使用 REPA++，SpeeDiff-XL 的 gFID 3.35 也大幅领先于传统两阶段训练的 DiT-XL/2（gFID ~9–10，Peebles and Xie, ICCV 2023）和 SiT-XL/2（gFID ~9–10，Ma et al., ECCV 2024），表明 TPR 损失和 ViT-VAE 架构本身就带来了显著的生成质量提升。

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/005_Table_2.jpg]]
*Table 2: ImageNet 256ˆ256 generation benchmark. We report detailed results for both non–representation alignment and representation alignment methods. We additionally include results at 80 epochs for convergence speed comparison. SpeeDiff achieves state-of-the-art performance without guidance in both settings (Ó lower is better; Ò higher is better)*

在 80 epoch 收敛速度维度上，SpeeDiff 的优势更为突出：相比 Vanilla SiT 加速逾 140 倍，相比 REPA 加速约 61 倍（Figure 1c），这意味着在相同训练预算下 SpeeDiff 可以更快地达到高质量生成状态。

### ImageNet 512×512 生成基准与可扩展性

Table 3 展示了 SpeeDiff 在高分辨率场景下的可扩展性。采用更高效的 32× 压缩 VAE（相较于 256×256 设置中的 8× 压缩），SpeeDiff-XL（含 REPA++）在无引导下取得 gFID 1.53，有引导下 IS 达到 322.55，均为该基准上的最优结果。这表明 SpeeDiff 的端到端训练范式能够灵活适配不同的 VAE 压缩率，在不牺牲生成质量的前提下实现高效的高分辨率生成（Figure 1d）。

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/006_Table_3.jpg]]
*Table 3: ImageNet 512ˆ512 generation benchmark. We employ a more efficient 32ˆ downsampled VAE while keeping all other settings consistent with the 256ˆ256 setup. SpeeDiff offers flexible VAE configurations and enables efficient high-resolution generation without sacrificing performance (Ó lower is better; Ò higher is better)*

### 架构设计的增益：ViT-VAE 与 Refined-DiT

将传统 CNN-VAE 替换为 **ViT-VAE**（基于 patch embedding 和 transformer block），并将扩散骨干升级为 **Refined-DiT**（集成 RMSNorm、SwiGLU 激活、2D RoPE 及共享全局调制），在计算效率和生成质量上均带来显著收益。据论文报告，这一架构改进使训练计算量从 436.29 GFLOPs 降至 334.98 GFLOPs，同时 gFID 提升至 3.66。这验证了全 Transformer 架构在端到端潜在扩散模型中的协同优势。

### REPA++ 组件消融

Table 5 对 REPA++ 进行了细致的组件分析。完整 REPA++（同时使用 Latent-REPA 和 Diff-REPA）取得最佳 gFID，优于单独使用任一分支。在视觉基础模型的选择上，DINOv3-L 优于 DINOv2 和 CLIP，表明更强的预训练语义表征能为潜在空间和扩散中间特征提供更有效的对齐信号。Figure 5 进一步通过 Robust PCA 可视化和线性探测精度验证了端到端训练过程中语义信息的自动改善，以及 CKNNA 评估对 REPA++ 各组件贡献的量化支持。

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/008_Figure_5.jpg]]
*Figure 5: Analysis of latent and intermediate diffusion features. (a) Visualization of latents using Robust PCA [4] on 1000 images. (b) Linear probing accuracy on the ImageNet validation set, which shows end-to-end training with diffusion gradient feedback automatically improve semantics. (c) CKNNA evaluation of latent and intermediate diffusion features for the REPA++ components*

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/011_Table_5.jpg]]
*Table 5: Ablation on REPA++. We evaluate different variants of REPA++ components on ImageNet 256ˆ256. REPA++ with DINOv3-L yields the best overall performance*

### 潜在通道数与预训练 VAE 的可迁移性

Table 6 的消融表明，潜在通道数设为 32 时在重建质量与生成质量之间达到最佳权衡，优于 16 或 64 通道的设置。此外，Table 4 验证了 SpeeDiff 预训练 VAE 的独立可用性：将其冻结后用于训练新的扩散模型，收敛速度与端到端训练几乎一致（80 epoch gFID 1.73 vs. 1.69），说明 TPR 损失在联合训练中塑造的潜在空间具有良好的泛化性和可迁移性。

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/009_Table_6.jpg]]
*Table 6: Ablations on latent channels. Results show that 32 channels offer the best trade-off between reconstruction and generation. The results are evaluate on ImageNet 256ˆ256 after 80 epochs*

![[assets/figures/papers/paper_list_l933_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_SpeeDiff_Scalabl/figures/010_Table_4.jpg]]
*Table 4: Can SpeeDiff pretrained VAE be used independently? A diffusion model trained on top of the frozen SpeeDiff pretrained VAE converges at nearly the same rate as SpeeDiff itself. Results are reported on ImageNet 256ˆ256*

### 局限性与待验证问题

尽管 SpeeDiff 在类别条件 ImageNet 生成上取得了显著成果，其当前验证范围仍局限于该设定。扩展到文本到图像等更复杂的条件生成任务尚待探索。此外，达到最佳性能依赖预训练的 DINOv3 视觉基础模型，这引入了额外的计算开销和外部依赖。在完全无预训练 VFM 的条件下，能否通过更强的潜在正则化或结构设计达到相近性能，仍是一个开放问题。同时，端到端训练的动态稳定性在更大规模数据和模型下是否依然保持，也需要进一步验证。

## 方法谱系与知识库定位

### 1. 与两阶段潜在扩散模型的对比

SpeeDiff 的核心创新在于将潜在扩散模型（LDM）从**冻结VAE的两阶段训练**转变为**端到端联合训练**。传统LDM范式（如 **DiT-XL/2**（Peebles and Xie, ICCV 2023）、**SiT-XL/2**（Ma et al., ECCV 2024））先独立训练一个CNN-based VAE，然后冻结编码器-解码器，仅在固定潜在空间上训练扩散模型。这种分离训练虽然稳定，但割裂了潜在表示学习与生成目标之间的梯度联系。

SpeeDiff 取消了 stop-gradient 操作，让扩散损失梯度直接回传至VAE编码器。这一改变带来了训练效率的质变：在 ImageNet 256×256 上，SpeeDiff 的收敛速度相比 Vanilla SiT 加速超过 **140 倍**，相比 **REPA**（Yu et al., ICLR 2025）加速 **61 倍**（Figure 1c）。然而，直接联合训练（Vanilla E2E）会导致潜在空间崩溃——扩散损失会驱动潜在表示退化为接近常数的输出，使扩散模型可以通过预测恒定值来最小化损失，却丢失了图像重建所需的语义信息（Figure 3）。

### 2. Tweedie Pixel Reconstruction 损失的机制定位

SpeeDiff 的因果旋钮是 **Tweedie Pixel Reconstruction (TPR) 损失**。该损失利用 Tweedie 公式从任意噪声时间步的潜在变量 $z_t$ 中估计干净潜在 $\hat{z}_0$，再通过解码器重建并与原图进行像素级 MSE 比较：

$$\mathcal{L}_{\mathrm{TPR}}(\phi,\psi,\pmb{\theta}) = \mathbb{E}_{\mathbf{x}_0,\mathbf{z}_0,\epsilon,t}\left[\left\|\mathcal{D}_{\psi}(\hat{\mathbf{z}}_0) - \mathbf{x}_0\right\|^2\right]$$

TPR 的作用机制是**像素锚定**：它在不中断梯度回传的前提下，为VAE注入来自像素空间的语义保持监督。这使得扩散损失的梯度被约束在维持有意义重建的方向上，而非驱动潜在空间退化。消融实验证实了这一机制的有效性：添加 TPR 后，ImageNet 256×256 上的 FID 从 **33.95 降至 5.79**（80 epochs），潜在空间也从尖锐峰态、极大偏置的退化分布恢复为标准化的正态分布（Figure 3）。

### 3. 与表示对齐方法的对比与整合

**REPA**（Yu et al., ICLR 2025）通过将扩散模型的中间特征与预训练视觉基础模型（VFM，如 DINOv2）的表示进行对齐，加速了扩散模型的训练收敛。SpeeDiff 在此基础上提出了 **REPA++**，同时对齐两个层次的信息：

- **Latent-REPA**：将干净潜在 $z_0$ 映射后与 VFM 表示进行 patch-wise 余弦相似度最大化
- **Diff-REPA**：将中间扩散特征 $f_t$ 映射后与 VFM 表示对齐

REPA++ 通过简单加和整合两种对齐信号，在 DINOv3-L 作为 VFM 时取得了最佳性能。与纯 REPA 相比，REPA++ 不仅加速收敛，还提升了最终生成质量（Table 5）。

### 4. 架构选择与效率定位

SpeeDiff 在架构上做了两项关键替换：

- **ViT-VAE**：用 Vision Transformer 替代传统卷积 VAE（CNN-VAE），采用 patch embedding 加 transformer blocks 的编码器-解码器结构
- **Refined-DiT**：在标准 DiT 基础上集成 RMSNorm、SwiGLU 激活、2D RoPE 位置编码，并用共享全局调制机制替代逐块调制层

这些架构改进使训练计算量从 **436.29 GFLOPs 降至 334.98 GFLOPs**，同时 FID 从 3.66 进一步提升（Sec. 3.3）。在潜在通道数的选择上，**32 通道**达到了重建质量与生成质量的最佳权衡，优于 16 或 64 通道（Table 6）。

### 5. 与其他端到端方法的对比

与 **MDTv2-XL**（Gao et al., arXiv 2023）的掩码扩散策略和 **RAE-L/16**（Zheng et al., 2025）用 VFM 编码器替代 VAE 编码器的方案不同，SpeeDiff 保持了标准 VAE-扩散架构的完整性，通过 TPR 损失和 REPA++ 在训练动态层面解决问题，而非改变模型结构本身。这种设计使得 SpeeDiff 预训练的 VAE 可以**独立冻结使用**——在其上训练新的扩散模型，收敛速度与端到端训练几乎一致（80 epochs gFID 1.73 vs 1.69，Table 4）。

### 6. 适用边界与局限

**已验证的适用场景**：
- 类别条件 ImageNet 生成（256×256 和 512×512），在无 guidance 条件下达到 state-of-the-art 的 gFID（1.69 和 1.53）
- 支持灵活的 VAE 压缩比配置（32× 下采样用于 512×512 高效生成）

**已知局限**：
- 目前仅验证了类别条件生成，扩展到文本到图像等更复杂条件生成任务仍需探索
- 达到最佳性能依赖预训练的 DINOv3 VFM，引入了额外的计算开销和外部模型依赖
- 端到端训练的动态稳定性可能需要更细致的超参数调整，在大规模训练下的收敛行为尚待验证

**开放问题**：
- 联合训练范式能否直接扩展到大规模文本到图像生成系统并保持有竞争力的收敛性质？
- 在完全无预训练 VFM 的条件下，能否通过更强的潜在正则化或结构设计达到与使用 VFM 相近的性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/SpeeDiff_Scalable_Pixel_Anchored_End_to_End_Latent_Diffusion_Model.pdf]]