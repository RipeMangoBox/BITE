---
title: "RefFusion: Reference Adapted Diffusion Models for 3D Scene Inpainting"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/RefFusion_Reference_Adapted_Diffusion_Models_for_3D_Scene_Inpainting.pdf
aliases:
- RefFusion
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过多尺度LoRA对扩散模型进行参考图像个性化，降低分数蒸馏目标方差并提升细节清晰度与可控性。
primary_logic: 对2D修复扩散模型进行多尺度参考图像个性化（LoRA）能显著降低SDS目标的方差，从而在3D修复中同时获得高清晰度、多视角一致性及用户明确控制。
claims:
- 个性化适配大幅减少SDS目标方差并无需文本引导。
- 移除个性化是消融实验中性能下降最显著项（LPIPS从0.4283升至0.5719）。
- 用户研究中，RefFusion在质量和物体移除指标上均大幅优于SPIn-NeRF-LaMa、Inpaint3D和Reference-guided NeRF SDXL。
- SPIn-NeRF Dataset 上 LPIPS↓ = 0.4283
---

# RefFusion: Reference Adapted Diffusion Models for 3D Scene Inpainting

> [!tip] 核心洞察
> 对2D修复扩散模型进行多尺度参考图像个性化（LoRA）能显著降低SDS目标的方差，从而在3D修复中同时获得高清晰度、多视角一致性及用户明确控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | RefFusion：基于参考自适应的扩散模型三维场景修复 |
| 英文题名 | RefFusion: Reference Adapted Diffusion Models for 3D Scene Inpainting |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2404.10765) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RefFusion |
| Dataset | SPIn-NeRF Dataset, SPIn-NeRF User Study |

> [!tip] 效果简介
> - SPIn-NeRF Dataset 上，LPIPS↓ 0.4283 vs All baselines (lower is better) (Ours achieves the lowest LPIPS)。
> - SPIn-NeRF User Study 上，Quality preference rate (baseline over Ours) RefFusion (preferred) vs SPIn-NeRF-LaMa: 18.38% (81.62% preferred RefFusion)；Removal preference rate (baseline over Ours) RefFusion (preferred) vs SPIn-NeRF-LaMa: 29.32% (70.68% preferred RefFusion)；Quality preference rate (baseline over Ours) RefFusion (preferred) vs Inpaint3D: 11.87% (88.13% preferred RefFusion)。

## 概述

### 问题与瓶颈

三维场景修复（3D inpainting）要求在用户指定的遮挡区域生成合理内容，同时保持多视角几何与外观一致性。现有方法主要沿两条路线发展：一类基于确定性修复模型（如LaMa），能够保持较好的多视角一致性但缺乏细节；另一类通过分数蒸馏采样（SDS）将2D扩散模型先验蒸馏到3D表示中，虽能生成丰富纹理，却因扩散模型的高随机性导致多视角不一致和细节模糊。**核心瓶颈**在于：将2D修复扩散模型先验蒸馏到3D时，标准SDS目标方差大、梯度冲突严重，且2D掩膜在不同视角间不一致，使得合成质量与多视角一致性难以兼得。

### 核心思路

**RefFusion**提出了一条简洁而高效的解决路径：**对2D修复扩散模型进行参考图像个性化适配，再将其先验蒸馏到3D高斯泼溅（3D Gaussian Splatting）场景表示中**。其关键洞察是——通过多尺度LoRA（Low-Rank Adaptation）将修复扩散模型适配到单张参考视图，能显著降低SDS目标的方差，从而无需文本引导即可获得高清晰度、多视角一致的修复结果，同时赋予用户明确的视觉控制。方法还利用3D高斯的显式特性，将掩膜区域与非掩膜区域的高斯粒子分离，使不同损失项的梯度仅传播到相关区域，有效缓解了梯度冲突。

### 方法定位

RefFusion处于**2D生成先验蒸馏与3D场景编辑**的交叉点。与基于确定性修复的方法（如**SPIn-NeRF**，Mirzaei et al., CVPR 2023）相比，它继承了扩散模型的生成能力，细节更丰富；与基于SDS的3D修复方法（如**Inpaint3D**，Prabhu et al., 2023）相比，个性化适配大幅降低了优化方差，结果更清晰、更可控；与同样使用参考引导的**Reference-guided NeRF**（Mirzaei et al., ICCV 2023）相比，多尺度LoRA个性化和梯度路由策略带来了显著的质量提升。在方法谱系上，RefFusion可视为“个性化扩散先验 + 显式3D表示 + 掩膜感知梯度路由”的融合范式。

### 主要结果

在SPIn-NeRF数据集的物体移除任务上，RefFusion取得了最低的LPIPS（0.4283），并在用户研究中全面领先：评估者对RefFusion的质量偏好显著高于SPIn-NeRF-LaMa（81.62% vs 18.38%）、Inpaint3D（88.13% vs 11.87%）和Reference-guided NeRF（76.36% vs 23.64%）。消融实验证实，**个性化适配是方法最关键的组件**——移除后LPIPS从0.4283急剧升至0.5719。方法无需修改即可泛化到物体插入、场景外推和稀疏视图重建等任务，展示了较强的通用性。

## 背景与动机

三维场景修复（3D scene inpainting）旨在从多视角图像中移除不需要的物体，并以视觉合理且多视角一致的内容填补缺失区域。这项工作在增强现实、数字孪生和影视后期等领域具有广泛应用价值。然而，与成熟的二维图像修复相比，三维修复面临着根本性的挑战：如何同时保证修复内容的视觉质量与跨视角的几何一致性。

早期方法主要依赖确定性修复模型。以 **SPIn-NeRF**（Mirzaei et al., CVPR 2023）为代表，这类方法将 LaMa 等二维修复模型的输出作为伪真值，通过重建损失将修复结果提升至三维。其优势在于多视角一致性较好，但受限于确定性修复模型自身的生成能力，修复区域往往缺乏细节和纹理丰富度。图 2 直观展示了这一困境：LaMa 的输出在不同视角间相对一致，但细节模糊；而 SDXL 等扩散模型能生成高质量内容，却因生成多样性过高导致不同视角的输出差异显著。

扩散模型先验的引入为突破这一瓶颈提供了新路径。通过分数蒸馏采样（Score Distillation Sampling, SDS），可以将二维扩散模型的生成先验蒸馏至三维表示中。**Inpaint3D**（Prabhu et al., 2023）和并发工作 **NeRFiller**（Weber et al., 2023）正是沿着这一思路，利用文本引导的修复扩散模型进行三维修复。然而，这类方法面临一个核心困境：**标准 SDS 目标在三维修复场景中方差过高**。文本提示仅提供粗粒度的语义引导，无法精确约束生成内容，导致优化过程不稳定，最终修复结果出现细节模糊和可控性差的问题。**Reference-guided NeRF**（Mirzaei et al., ICCV 2023）尝试引入参考图像引导，但未能从根本上降低蒸馏目标的方差。

上述困境揭示了该领域的**核心瓶颈**：将二维修复扩散模型先验蒸馏到三维时，多视角一致性与合成质量之间存在根本性权衡，而二维掩膜的不一致性和梯度冲突进一步加剧了细节模糊与可控性缺失。具体而言，当不同视角的二维掩膜不完全对齐时，梯度信号会传播至不相关的三维区域，造成几何和外观的伪影。

RefFusion 正是针对这一瓶颈提出。其核心洞察在于：**对二维修复扩散模型进行多尺度参考图像个性化（LoRA），能显著降低 SDS 目标的方差**，从而在三维修复中同时获得高清晰度、多视角一致性及用户明确控制。这一洞察将问题的解决路径从“如何约束高方差蒸馏”转变为“如何从源头降低蒸馏方差”——通过使扩散模型本身适配目标场景的参考视图，生成先验的质量和稳定性得到根本性提升。

## 核心创新

RefFusion 的核心创新在于将 **2D 修复扩散模型的参考图像个性化** 与 **3D 高斯泼溅的显式结构** 深度耦合，系统性地解决了 3D 场景修复中多视角一致性与合成质量之间的根本矛盾。其技术路线围绕一个关键洞察展开：对修复扩散模型进行多尺度参考图像个性化能显著降低分数蒸馏采样（SDS）目标的方差，从而在无需文本引导的条件下同时获得高清晰度、强多视角一致性及用户明确控制。

### 关键创新点

**1. 多尺度 LoRA 个性化替代文本引导**

传统基于 SDS 的 3D 生成方法依赖文本提示驱动扩散模型先验，但文本描述难以精确捕捉场景的纹理、光照和几何细节，导致 SDS 目标方差大、优化不稳定。RefFusion 提出对 2D 修复扩散模型进行基于单张参考图像的多尺度 LoRA 个性化微调（Section 3.3），使模型“记忆”参考视图的视觉特征。这一适配大幅降低了 SDS 目标的方差，并完全移除了对文本引导的依赖。消融实验（Table 3）提供了决定性证据：移除个性化组件后，LPIPS 从 0.4283 急剧恶化至 0.5719，是所有消融项中性能下降最显著的。

**2. 多尺度 SDS 目标融合全局上下文与局部细节**

与仅使用全局渲染视图计算 SDS 损失的方法不同，RefFusion 设计了多尺度 SDS 目标（Section 3.4），将全局 SDS 损失与局部裁剪区域的 SDS 损失相结合（$$\mathcal { L } _ { \mathrm { S D S } } : = \mathcal { L } _ { \mathrm { S D S } } ^ { \mathrm { g l o b a l } } + \mathcal { L } _ { \mathrm { S D S } } ^ { \mathrm { l o c a l } }$$）。全局项确保修复区域与整体场景风格一致，局部项则聚焦于修复边界的细节清晰度。这一设计直接受益于多尺度个性化策略——因为个性化后的扩散模型对参考视图的全局和局部特征均有良好感知，使得多尺度蒸馏成为可能。消融实验表明，移除局部 SDS 损失使 LPIPS 升至 0.5093。

**3. 基于 3D 高斯显式结构的梯度路由与掩膜追踪**

3D 修复中，2D 掩膜在不同视角间常常不一致，导致梯度错误传播至未掩膜区域，产生模糊和伪影。RefFusion 利用 3D 高斯泼溅的显式特性，将高斯粒子动态划分为掩膜区域集与非掩膜区域集，并将不同损失项的梯度仅回传至相关区域（Section 3.5）。这一梯度路由策略有效避免了未掩膜区域被生成先验“污染”，同时使掩膜区域获得充分的生成引导。移除该分离机制后，LPIPS 升至 0.5128。

**4. 参考引导初始化与正则化增强**

RefFusion 引入参考深度反投影初始化掩膜区域的高斯粒子（Section 3.5），替代传统的随机初始化，为优化提供更合理的几何起点。此外，方法在总损失中加入了深度正则化损失和带 R1 梯度惩罚的对抗损失（Section 3.6），分别增强几何一致性与外观质量。消融实验显示，移除参考引导初始化使 LPIPS 升至 0.4680，移除对抗损失和深度损失分别使 LPIPS 升至 0.4326 和 0.4299——虽然后两项在物体移除任务中贡献相对较小，但在物体插入等应用中更为关键。

### 创新总结

上述创新点并非孤立存在，而是形成了一个闭环的因果链条：多尺度个性化降低了 SDS 目标的方差，使得多尺度 SDS 优化成为可能；而 3D 高斯的显式结构则为梯度路由和参考引导初始化提供了实现基础。这一系统性的设计使 RefFusion 在 SPIn-NeRF 数据集上取得了 0.4283 的 LPIPS，并在用户研究中以压倒性优势超越 **SPIn-NeRF-LaMa**（Mirzaei et al., CVPR 2023）、**Inpaint3D**（Prabhu et al., 2023）和 **Reference-guided NeRF SDXL**（Mirzaei et al., ICCV 2023）等基线方法。

## 整体框架

RefFusion 的整体流程围绕一个核心思想展开：**将经过参考图像个性化适配的 2D 修复扩散模型的生成先验，通过多尺度分数蒸馏采样（Score Distillation Sampling, SDS）注入到显式的 3D 高斯泼溅（3D Gaussian Splatting）表示中**，从而在 3D 场景修复中同时获得高清晰度、多视角一致性和用户明确控制。图 3 给出了完整的 pipeline 概览。

### 输入与输出

系统接受四类输入：

1. **训练视图**：场景的多视角 RGB 图像及其对应的相机位姿。
2. **用户定义的 2D 掩膜**：标记每张视图中需要修复（移除或替换）的区域。
3. **参考视图**：一张由用户提供或由 2D 修复模型生成的图像，用于指导缺失区域的内容生成。
4. **场景的 3D 高斯泼溅表示**：由 **3DGS**（Kerbl et al., ToG 2023）重建得到的初始场景表示，包含高斯粒子的位置、尺度、旋转、不透明度和球谐系数等可微参数。

输出是一个经过修复的 3D 高斯泼溅场景，其中掩膜区域被合理填充，且在新视角下保持多视角一致。

### 核心模块与数据流

整个 pipeline 可分解为五个紧密协作的模块，其数据流如图 3 所示：

**1. 多尺度 LoRA 个性化（Multi-scale LoRA Personalization）**

该模块是 RefFusion 区别于以往基于 SDS 的 3D 修复方法的关键。它不再依赖单一的文本提示来引导扩散模型，而是对预训练的 2D 修复扩散模型（inpainting LDM）进行**基于参考图像的个性化适配**。具体而言，从参考视图中提取全局图像和局部裁剪块，利用 LoRA（Low-Rank Adaptation）对扩散模型的 U-Net 和文本编码器进行微调，使模型“记住”参考图像的内容和风格。这一适配策略的核心因果效应在于：**大幅降低了后续 SDS 目标的方差，并消除了对文本引导的依赖**（Section 3 明确指出“The adaptation largely reduces the variance of the score distillation objective and removes the need for text guidance”）。

**2. 多尺度 SDS 优化（Multi-scale SDS Optimization）**

个性化适配后的扩散模型被用于构建一个**多尺度 SDS 损失**：

$$\mathcal{L}_{\mathrm{SDS}} := \mathcal{L}_{\mathrm{SDS}}^{\mathrm{global}} + \mathcal{L}_{\mathrm{SDS}}^{\mathrm{local}}$$

其中，全局 SDS 损失作用于完整渲染视图（下采样至 512×512 以匹配扩散模型的输入分辨率），提供场景级的语义和结构一致性；局部 SDS 损失作用于掩膜区域的高分辨率裁剪块，增强细节清晰度。两者结合，使得 3D 高斯泼溅的渲染结果在全局语义和局部纹理上都与参考图像保持高度一致。

**3. 3D 高斯掩膜追踪（3D Gaussian Mask Tracking）**

为应对 2D 掩膜在不同视角间的不一致性问题，RefFusion 利用 3D 高斯泼溅的显式点云特性，**将高斯粒子划分为掩膜区域和非掩膜区域两类**。在优化过程中，不同损失项的梯度仅回传至相关的高斯粒子集合：SDS 损失和深度正则化损失的梯度仅更新掩膜区域的高斯粒子，而重建损失的梯度仅更新非掩膜区域的高斯粒子。这一梯度路由策略有效避免了不同目标间的梯度冲突，防止了非掩膜区域的退化。

**4. 参考引导初始化（Reference-Guided Initialization）**

掩膜区域的高斯粒子并非随机初始化，而是采用**参考深度反投影**策略：首先利用单目深度估计网络预测参考视图的深度图，经过尺度和偏移对齐后，将掩膜区域的深度值反投影到 3D 空间，作为高斯粒子位置的初始值。消融实验（Table 3）证实，该初始化策略显著优于随机初始化。

**5. 深度与对抗正则化（Depth and Adversarial Regularization）**

在核心的 SDS 损失之外，RefFusion 还引入了两个辅助正则化项以进一步提升几何一致性和外观质量：

- **深度正则化损失**：约束掩膜区域的渲染深度与对齐后的参考深度之间的 L2 距离。
- **对抗损失（带 R1 梯度惩罚的 GAN 损失）**：应用于球谐系数，以减轻潜在的外观伪影。

最终的总训练损失为四项损失的加权组合：

$$\mathcal{L} := \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{SDS}} \mathcal{L}_{\mathrm{SDS}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{adv}} \mathcal{L}_{\mathrm{adv}}$$

### 瓶颈与设计动机

RefFusion 的设计直接回应了 3D 修复领域的核心瓶颈：**将 2D 修复扩散模型的先验蒸馏到 3D 时，面临多视角一致性与合成质量之间的根本性权衡**。传统方法中，基于确定性修复器（如 LaMa）的方法虽多视角一致性较好，但缺乏细节；基于文本引导 SDS 的方法虽能生成丰富纹理，但方差大、可控性差，且 2D 掩膜的不一致性会引入梯度冲突，导致细节模糊。RefFusion 通过**多尺度 LoRA 个性化**这一因果旋钮，将扩散模型的生成空间约束到参考图像附近，从而在保持生成多样性的同时，大幅降低了 SDS 目标的方差，使高清晰度、多视角一致性和用户明确控制三者得以兼得。

### 补充图表

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the proposed approach. RefFusion takes training views, masks, and the reference view as input (left). We adapt the inpainting LDM on both the global and local crops of the reference view (middle). Then, we distill the priors of the adapted LDM to the scene (right) by minimizing the SDS objective. Additionally, we use a discriminator loss to mitigate potential artifacts in appearance and a depth loss to enhance geometry. We track Gaussians representing the masked and unmasked regions, and backpropagate the gradients of individual terms only to the pertinent regions*

## 核心模块与公式推导

### 3.1 背景：扩散模型与分数蒸馏采样

RefFusion 的核心生成先验来自预训练的 2D 修复扩散模型（Inpainting Diffusion Model, DM）。扩散模型通过逐步去噪学习数据分布，其简化训练目标为：

$$\mathbb{E}_{\mathbf{x}\sim p(\mathbf{x}),\epsilon\sim N(\mathbf{0},I),t\sim T}[w(t)||\epsilon_{\theta}(\mathbf{x}_t,t,\mathbf{c})-\epsilon||_2^2]$$

其中，$\epsilon_{\theta}$ 为噪声预测网络，$\mathbf{x}_t$ 为加噪图像，$\mathbf{c}$ 为条件（如掩膜图像和文本提示），$t$ 为时间步。推理时，模型从纯噪声出发逐步去噪生成图像。

为将 2D 生成先验蒸馏至 3D 表示，RefFusion 采用**分数蒸馏采样**（Score Distillation Sampling, SDS）。给定可微渲染函数 $g(\phi)$ 将 3D 参数 $\phi$ 渲染为图像，SDS 梯度定义为：

$$\nabla_{\phi}\mathcal{L}_{\mathrm{SDS}}(\phi,\theta):=\mathbb{E}_{\epsilon\sim\mathcal{N}(0,I),t\sim T}[w(t)(\hat{\epsilon}_{\theta}(z_t,t,c)-\epsilon)\frac{\partial z_t}{\partial\phi}]$$

其中 $z_t$ 为渲染图像的加噪版本。该梯度将渲染图像推向扩散模型的高概率区域，实现生成引导。为提升生成质量，采用**无分类器引导**（classifier-free guidance）：

$$\hat{\epsilon}_{\theta}(z_t,t,c):=(1+\alpha)\epsilon_{\theta}(z_t,t,c)-\alpha\epsilon_{\theta}(z_t,t,\emptyset)$$

其中 $\alpha$ 为引导强度，$\emptyset$ 为空文本嵌入。

---

### 3.2 多尺度 LoRA 个性化

传统 SDS 依赖文本提示引导，但文本描述难以精确指定场景内容，导致生成方差大、多视角一致性差。RefFusion 的核心创新在于**对修复扩散模型进行参考图像个性化**，通过多尺度 LoRA（Low-Rank Adaptation）将模型适配至单张参考视图。

具体而言，给定参考图像 $\mathrm{I}_r$ 及其掩膜 $\mathrm{M}_r$，提取**全局裁剪**和**局部裁剪**（聚焦于掩膜区域），共同作为个性化训练数据。LoRA 在 U-Net 的注意力层注入低秩残差矩阵，仅优化少量参数（秩 $r=8$，训练 2000 步，学习率 U-Net $2\times10^{-4}$，文本编码器 $4\times10^{-5}$，dropout 0.1），使模型学会在掩膜区域生成与参考图像一致的细节。

该个性化策略的因果效应在于：**大幅降低 SDS 目标的方差**，使蒸馏过程无需文本引导即可稳定收敛，同时赋予用户对修复内容的明确控制（Section 3 原文：“The adaptation largely reduces the variance of the score distillation objective and removes the need for text guidance.”）。

---

### 3.3 多尺度 SDS 目标

为兼顾全局场景上下文与局部修复细节，RefFusion 构建**多尺度 SDS 损失**：

$$\mathcal{L}_{\mathrm{SDS}} := \mathcal{L}_{\mathrm{SDS}}^{\mathrm{global}} + \mathcal{L}_{\mathrm{SDS}}^{\mathrm{local}}$$

- **全局 SDS**（$\mathcal{L}_{\mathrm{SDS}}^{\mathrm{global}}$）：将完整渲染视图双线性下采样至 $512\times512$（适配个性化 LDM 的输入分辨率），计算全局 SDS 梯度，确保修复区域与周围场景风格一致。
- **局部 SDS**（$\mathcal{L}_{\mathrm{SDS}}^{\mathrm{local}}$）：从渲染视图中裁剪掩膜区域，上采样至 $512\times512$，计算局部 SDS 梯度，聚焦于修复区域的高频细节生成。

两项损失均使用个性化后的扩散模型计算，无需额外文本提示。

---

### 3.4 3D 高斯掩膜追踪与梯度路由

3D 高斯泼溅（3D Gaussian Splatting）的显式点云特性使 RefFusion 能够**追踪掩膜与非掩膜区域的高斯粒子**。在优化过程中，根据 2D 掩膜投影将高斯粒子划分为掩膜集 $\mathcal{G}_{\mathrm{masked}}$ 和非掩膜集 $\mathcal{G}_{\mathrm{unmasked}}$，对不同损失项的梯度进行定向路由：

- 重建损失 $\mathcal{L}_{\mathrm{rec}}$ 仅回传至非掩膜高斯粒子，保护已知区域。
- SDS 损失仅回传至掩膜高斯粒子，驱动缺失内容生成。
- 深度正则化损失仅作用于掩膜区域。

该策略避免了梯度冲突——传统方法中，SDS 梯度可能破坏已知区域的几何与外观，而 RefFusion 的分离机制确保各损失项各司其职。消融实验表明，移除该分离机制使 LPIPS 从 0.4283 升至 0.5128（Table 3）。

---

### 3.5 参考引导初始化

掩膜区域的 3D 高斯初始化对优化稳定性至关重要。RefFusion 采用**参考深度反投影初始化**：首先利用单目深度估计器预测参考图像 $\mathrm{I}_r$ 的深度 $\tilde{d}_r$，通过尺度与偏移对齐得到校准深度 $\hat{d}_r$，然后将掩膜区域像素反投影至 3D 空间，初始化对应的高斯粒子位置。Table 3 显示该初始化显著优于随机初始化（LPIPS 0.4680 vs 0.4283）。

---

### 3.6 深度正则化与对抗损失

为进一步提升几何一致性与外观质量，RefFusion 引入两项辅助损失：

**深度正则化损失**：约束掩膜区域的渲染深度与参考深度一致：

$$\mathcal{L}_{\mathrm{depth}} := \frac{1}{|P_{\mathrm{masked}}|} \sum_{j \in P_{\mathrm{masked}}} \Vert \hat{d}(p) - \bar{d}(p) \Vert_2^2$$

其中 $\hat{d}(p)$ 为渲染深度，$\bar{d}(p)$ 为对齐后的参考深度，$P_{\mathrm{masked}}$ 为掩膜像素集。

**对抗损失**（带 R1 梯度惩罚）：在球谐系数上施加 GAN 损失，抑制生成伪影：

$$\min_{\beta} \max_{\boldsymbol{\xi}} \mathbb{E} \Big[ f(\mathcal{D}_{\boldsymbol{\xi}}(\hat{\mathrm{I}}_{\mathrm{fake}}^P)) + f(-\mathcal{D}_{\boldsymbol{\xi}}(\mathrm{I}_{\mathrm{real}}^P)) - \lambda_{\mathrm{gp}} \| \nabla \mathcal{D}_{\boldsymbol{\xi}}(\hat{\mathrm{I}}_{\mathrm{fake}}^P) \|_2^2 \Big]$$

总训练损失为各项加权组合：

$$\mathcal{L} := \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{SDS}} \mathcal{L}_{\mathrm{SDS}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{adv}} \mathcal{L}_{\mathrm{adv}}$$

消融实验表明，深度与对抗损失对物体移除任务的直接提升有限（LPIPS 分别升至 0.4299 和 0.4326），但在物体插入等应用中更为关键，且有助于抑制特定类型伪影（Fig. 10）。

## 实验与分析

### 主实验：物体移除

RefFusion 在 SPIn-NeRF 数据集（**SPIn-NeRF**，Mirzaei et al., CVPR 2023）上进行物体移除评估，与三类代表性基线对比：确定性修复方法 **SPIn-NeRF (LaMa)**（Mirzaei et al., CVPR 2023）、基于 SDS 的 **Inpaint3D**（Prabhu et al., 2023）、以及使用 SDXL 修复的 **Reference-guided NeRF**（Mirzaei et al., ICCV 2023）。

**定量结果（Table 1）**：RefFusion 取得 LPIPS 0.4283，优于所有基线。需注意，LPIPS 作为感知度量能反映合成质量与多视角一致性，但该数值需结合定性结果和用户研究综合解读——低 LPIPS 并不自动保证修复区域与周围场景的语义协调性。

**用户研究（Table 2）**：更关键的证据来自大规模用户偏好测试。评估者被要求从“整体质量”和“物体移除完整性”两个维度选择偏好方法。结果以“基线被偏好于 RefFusion 的百分比”报告，数值越低表明 RefFusion 优势越显著：

- **vs SPIn-NeRF-LaMa**：仅 18.38%（质量）和 29.32%（移除）的评估者偏好基线，RefFusion 在细节清晰度上大幅领先。
- **vs Inpaint3D**：偏好基线比例仅 11.87%（质量）和 11.52%（移除），表明基于标准 SDS 的方法在可控性和一致性上与 RefFusion 存在系统性差距。
- **vs Reference-guided NeRF (SDXL)**：偏好基线比例为 23.64%（质量）和 43.65%（移除）。移除维度上的差距相对较小，提示 SDXL 的强生成先验在填补大面积缺失区域时具有一定竞争力，但其多视角一致性仍不如 RefFusion 的个性化策略。

**定性分析（Fig. 4, Fig. 9）**：RefFusion 生成的修复区域边缘更锐利、纹理更清晰，且在不同视角下保持语义一致性。相比之下，SPIn-NeRF-LaMa 虽多视角一致性较好，但细节模糊；Inpaint3D 和 Reference-guided NeRF 则易出现视角间纹理闪烁或语义漂移。大相机运动场景（Fig. 5，MipNeRF360 数据集及自建场景）进一步验证了 RefFusion 在视角变化剧烈时的鲁棒性。

### 消融实验

Table 3 的消融研究量化了各组件对 LPIPS 的贡献，揭示了一条清晰的因果链：

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/007_Table_3.jpg]]
*Table 3: Ablation study of object removal on SPIn-NeRF dataset*

| 消融项 | LPIPS | 性能降幅 | 核心机制 |
|--------|-------|----------|----------|
| RefFusion（完整） | 0.4283 | — | 多尺度个性化 + 梯度路由 + 正则化 |
| 移除个性化（LoRA） | 0.5719 | **+0.1436** | SDS 目标方差剧增，生成质量崩溃 |
| 移除掩膜/非掩膜高斯分离 | 0.5128 | +0.0845 | 梯度冲突导致非掩膜区域受污染 |
| 移除局部 SDS 损失 | 0.5093 | +0.0810 | 丢失局部细节蒸馏信号 |
| 移除参考引导初始化 | 0.4680 | +0.0397 | 掩膜区域从随机状态开始优化，收敛变慢 |
| 移除对抗损失 | 0.4326 | +0.0043 | 外观伪影轻微增加 |
| 移除深度损失 | 0.4299 | +0.0016 | 几何一致性轻微退化 |

**关键发现**：

1. **个性化是性能的支配性因素**：移除多尺度 LoRA 个性化导致 LPIPS 从 0.4283 急剧升至 0.5719，降幅远超其他任何组件。这直接验证了核心洞察——个性化适配通过降低 SDS 目标的方差，是获得高清晰度与多视角一致性的必要条件。定性结果（Fig. 10）显示，无个性化时修复区域出现严重的纹理模糊和语义不连贯。

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/013_Figure_10.jpg]]
*Figure 10: Qualitative results of the ablation study on SPIn-NeRF dataset. Note how different components of our method help improve different types of artifacts*

2. **梯度路由策略至关重要**：移除掩膜/非掩膜高斯粒子分离使 LPIPS 升至 0.5128，仅次于个性化移除的影响。这证实了 2D 掩膜不一致性带来的梯度冲突问题确实会显著损害修复质量，而显式追踪 3D 高斯归属是有效的应对策略。

3. **多尺度 SDS 的局部项贡献显著**：移除局部 SDS 损失使 LPIPS 升至 0.5093，表明仅靠全局 SDS 损失无法充分捕捉修复边界的细节过渡。局部裁剪的蒸馏信号对于边界一致性和细节保真度不可或缺。

4. **深度与对抗正则化在物体移除中贡献有限但正向**：移除对抗损失（0.4326）和深度损失（0.4299）仅引起轻微性能下降。这与论文的说明一致——这些正则项在物体插入等应用中更为关键，但在物体移除任务中仍提供正向的几何和外观约束。

### 泛化能力与应用扩展

RefFusion 无需任何方法修改即可应用于多种 3D 编辑任务：

- **物体插入（Fig. 7）**：通过反转掩膜逻辑，在指定区域生成与场景协调的新物体。深度与对抗正则化在此任务中发挥更重要作用，确保插入物体的几何合理性和光照一致性。
- **场景外推（Fig. 8）**：通过反掩膜实现场景边界扩展。论文坦承外推区域缺乏高频细节和视觉保真度，这是当前方法的已知局限。
- **稀疏视图重建（Fig. 6, Fig. 11）**：即使仅使用稀疏视图进行个性化（Ours LoRA），RefFusion 已展现竞争力；结合重建损失后（Ours LoRA + recon），一致优于纯 **3DGS**（Kerbl et al., ToG 2023），在仅有一个真实视图的极端情况下，生成先验仍能有效引导重建。

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/009_Figure_7.jpg]]
*Figure 7: Sample object insertion results*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/010_Figure_6.jpg]]
*Figure 6: Results of the sparse view reconstruction on SPIn-NeRF dataset. Using the sparse GT views only for personalization Ours (LoRA) already yields competitive results. When combined with the reconstruction loss Ours (LoRA + recon) consistently outperforms 3DGS [Kerbl et al. 2023], showcasing the potential of generative priors to guide 3D reconstruction*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/011_Figure_8.jpg]]
*Figure 8: Our approach is capable of outpainting scenes by inverted masks*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/014_Figure_11.jpg]]
*Figure 11: Qualitative evaluation of sparse view reconstruction on SPIn-NeRF dataset. Both RefFusion and 3DGS use the reconstruction loss on sparse input images in the masked region. Additionally, RefFusion uses generative priors of the reference adapted LDM through SDS losses as well as the depth and adversarial regularization terms. Note how generative priors can successfully guide the reconstruction even in the extreme case of a single GT view*

### 失败模式与局限

论文明确指出的失败模式包括：

1. **大面积遮挡场景**：当目标移除区域覆盖参考图像的大部分时，个性化缺乏足够的上下文信息，修复质量显著下降。这是参考图像信息量的固有瓶颈。
2. **外推区域保真度不足**：场景外推结果缺乏高频细节，视觉保真度明显低于修复和插入任务。这提示当前方法缺乏对场景布局的结构化先验。
3. **2D 掩膜不一致性残留**：尽管梯度路由策略缓解了掩膜不一致的影响，但启发式掩膜整合方法仍可能引入不精确的 3D 区域划分，在复杂几何边界处产生伪影。
4. **预训练模型随机性**：受限于预训练 2D 扩散修复模型的随机生成特性，部分视角仍可能出现不一致伪影，尤其在纹理丰富或语义模糊的区域。
5. **计算开销**：LoRA 个性化需要约 2000 次迭代（LoRA rank 8，分辨率 512），限制了实时应用场景。

### 公平性讨论

RefFusion 的评估设置存在几个需注意的方面：方法需要一张参考图像作为个性化输入，该图像可由修复模型生成或实拍获得。若参考图像质量低或与目标场景不匹配，性能可能显著下降——这是方法的内在依赖，而非评估偏差。深度与对抗正则项在物体移除任务中提升有限（消融已证实），但在物体插入等应用中更关键，因此整体性能不严重依赖于单一正则项，方法的鲁棒性较好。

### 补充图表

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of object removal on SPIn-NeRF dataset*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/005_Table_2.jpg]]
*Table 2: User study of object removal on SPIn-NeRF dataset. For each method we report the percentage of raters that pereferred it over ours*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative object removal results on the SPIn-NeRF dataset. RefFusion consistently outperforms the baselines, yielding sharper reconstruction and more plausible inpainting*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative object removal results on scenes with larger camera movements (MipNeRF360 dataset [Barron et al. 2022] and scenes from our proposed dataset). RefFusion consistently outperforms the Reference-guided NeRF*

![[assets/figures/papers/paper_list_l74_https_arxiv_org_abs_2404_10765/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative object removal results on the SPIn-NeRF dataset. RefFusion synthesizes plausible content that is highly multi-view consistent*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

3D场景修复的核心瓶颈在于：将2D修复扩散模型的生成先验蒸馏到3D表示时，面临**多视角一致性与合成质量之间的根本性权衡**。确定性修复方法（如LaMa）虽能保持一定一致性，但缺乏细节；而大规模扩散模型（如SDXL）虽能生成高质量内容，却因生成多样性过高导致不同视角间内容不一致。此外，2D掩膜在不同视角间天然存在不一致性，传统方法将梯度均匀传播至所有3D高斯粒子，导致掩膜区域与非掩膜区域的梯度相互干扰，进一步加剧细节模糊与可控性差的问题。

RefFusion的因果调节变量是**对2D修复扩散模型进行多尺度参考图像个性化（LoRA）**。这一设计直接降低了分数蒸馏采样（SDS）目标的方差，使得蒸馏过程无需依赖文本提示即可稳定收敛，同时显著提升了修复区域的细节清晰度与用户对生成内容的控制力。消融实验提供了决定性证据：移除个性化组件后，LPIPS从0.4283急剧恶化至0.5719（Table 3），是所有消融项中性能下降幅度最大的。

### 方法与现有工作的关系

**与基于SDS的3D修复方法的关系。** **Inpaint3D**（Prabhu et al., 2023）和并发工作**NeRFiller**（Weber et al., 2023）均采用标准SDS目标将2D修复先验蒸馏至3D，但依赖文本提示引导且面临SDS高方差问题。RefFusion在此基础上引入两个关键改进：其一，通过多尺度LoRA个性化将扩散模型适配至参考视图，从根本上降低SDS方差；其二，利用3D高斯泼溅的显式特性实现掩膜/非掩膜区域的梯度路由，避免无关区域的梯度污染。用户研究中，RefFusion在质量偏好上以88.13%对11.87%大幅领先Inpaint3D（Table 2），验证了上述改进的实际效果。

**与参考引导NeRF修复方法的关系。** **Reference-guided NeRF**（Mirzaei et al., ICCV 2023）同样利用参考图像引导修复，但其直接使用SDXL进行2D修复后重建NeRF，缺乏对扩散模型的个性化适配和显式的3D掩膜区域追踪。RefFusion的个性化策略使得扩散模型输出与参考视图高度一致，从而在更大相机运动场景下仍保持多视角一致性（Fig. 5）。用户研究中，RefFusion在物体移除指标上以56.35%对43.65%领先Reference-guided NeRF SDXL（Table 2），但在该基线上的优势小于对Inpaint3D的优势，表明参考引导本身已提供一定的一致性增益，而个性化进一步放大了这一优势。

**与确定性修复方法的关系。** **SPIn-NeRF**（Mirzaei et al., CVPR 2023）采用LaMa进行2D修复后重建NeRF，其修复内容在不同视角间相对一致但缺乏细节。RefFusion在质量偏好上以81.62%对18.38%领先SPIn-NeRF-LaMa（Table 2），在物体移除指标上也以70.68%对29.32%领先，表明扩散模型先验在生成逼真细节方面具有显著优势。

**与纯3D重建方法的关系。** **3DGS**（Kerbl et al., ToG 2023）不依赖任何生成先验，仅从稀疏视图进行重建。RefFusion在稀疏视图重建任务中，即使仅使用个性化（LoRA）而不使用重建损失，已能获得有竞争力的结果；当结合重建损失后，RefFusion（LoRA + recon）一致地优于3DGS（Fig. 6），展示了生成先验对3D重建的引导潜力。

### 技术贡献的适用边界

**参考图像依赖。** RefFusion需要一张参考图像作为个性化输入，该图像可由2D修复模型生成或实拍获得。若参考图像质量低、与目标场景风格不匹配，或目标移除区域过大以至于覆盖参考图像的大部分区域，修复质量将显著下降。这一依赖限制了方法在无合适参考图像场景下的直接应用。

**计算开销。** LoRA个性化需要约2000次迭代训练（rank=8，分辨率512×512），虽属参数高效微调范畴，但仍需相当的GPU计算时间，限制了实时或交互式应用场景。

**外推区域质量。** 在外推（outpainting）任务中，生成区域缺乏高频细节和视觉保真度（Fig. 8），表明方法对场景布局的结构化约束不足，生成先验在完全未见区域的表现仍有提升空间。

**2D掩膜不一致性。** 当前方法采用启发式策略整合多视角2D掩膜，这一过程可能引入不精确的3D区域划分，进而影响梯度路由的准确性和最终修复质量。

**预训练模型的固有限制。** 方法仍受限于预训练2D修复扩散模型的随机生成能力，在部分视角下仍可能出现不一致伪影，尤其是在目标区域纹理复杂或几何结构模糊时。

### 局限与开放问题

**多视角一致性的进一步提升。** 当前个性化策略虽已大幅改善一致性，但本质上仍是对单张参考图像的适配。如何利用多视角感知先验或视频扩散模型进一步提升跨视角一致性，以及增强对大相机运动场景的鲁棒性，是重要的开放方向。

**个性化效率。** 能否采用更高效的参数高效微调技术（如AdaLoRA、IA³等）加速个性化过程，或将个性化与蒸馏过程联合优化以减少整体训练时间，值得进一步探索。

**动态场景与4D编辑。** 当前方法针对静态3D场景设计，能否扩展到动态场景和4D编辑任务（如视频中的物体移除与插入），需要处理时序一致性和运动建模等新挑战。

**外推质量的改进。** 如何改进外推区域的生成质量，例如通过引入场景布局的结构化先验、多尺度生成策略或迭代式外推，是提升方法通用性的关键问题。

**掩膜处理的鲁棒性。** 开发更鲁棒的多视角掩膜融合策略，或探索无需显式掩膜的隐式区域划分方法，有望减少掩膜不一致性引入的误差。

**评估基准的完善。** 当前定量评估主要依赖LPIPS和用户研究，缺乏对3D几何一致性、多视角光度一致性的直接度量。建立更全面的3D修复评估基准将有助于推动该领域发展。

## 原文 PDF

![[paperPDFs/arxiv_2024/RefFusion_Reference_Adapted_Diffusion_Models_for_3D_Scene_Inpainting.pdf]]