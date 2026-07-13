---
title: "Photorealistic Object Insertion with Diffusion-Guided Inverse Rendering"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Photorealistic_Object_Insertion_with_Diffusion_Guided_Inverse_Rendering.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/DiPIR/
aliases:
- POIDGIR
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: Photorealistic
primary_logic: Photorealistic
claims:
- Photorealistic
---

# Photorealistic Object Insertion with Diffusion-Guided Inverse Rendering

> [!tip] 核心洞察
> Photorealistic

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Photorealistic Object Insertion with Diffusion-Guided Inverse Rendering |
| 英文题名 | Photorealistic Object Insertion with Diffusion-Guided Inverse Rendering |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2408.09702) · [Project](https://research.nvidia.com/labs/toronto-ai/DiPIR/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

在单张消费级图像中恢复物理光照并实现虚拟物体的真实感插入，是计算机视觉与图形学中长期存在的挑战。核心困难在于逆渲染问题的高度欠定性——单张低动态范围图像丢失了大量场景几何、材质与光照信息，传统方法通常依赖简化的光照模型或启发式先验，难以在室内外复杂场景中同时保持光照估计的物理合理性与视觉逼真度。

本文提出 **DiPIR**，一种基于扩散模型引导的物理逆渲染方法。其核心思路是将个性化的大型扩散模型作为“人类评估器”：扩散模型接收合成后的编辑图像作为输入，通过可微分渲染将反馈信号传播至物理场景属性（环境光照与色调映射参数），实现端到端优化。这一设计使得方法既能利用扩散模型对自然图像统计的强先验，又能通过物理渲染器保证光照交互的物理一致性。

**方法定位**上，DiPIR 属于“扩散模型引导的逆渲染”范式，区别于纯数据驱动的光照估计方法（如直接从单图回归环境贴图）和传统基于优化的逆渲染方法（依赖手工设计的先验）。与现有扩散模型引导方法相比，DiPIR 的关键创新在于：1）提出一种轻量级的扩散模型个性化方案，基于输入图像与待插入物体的类别进行 LoRA 微调；2）设计了改进的 Score Distillation Sampling（SDS）损失变体，利用个性化扩散模型提升训练稳定性与合成质量。

**主要结果**方面，在 Waymo 室外街景数据集上的用户偏好测试中，DiPIR 相较于 StyleLight 获得了 **77.8%** 的偏好率（随机机会为 50%），优势达 **+27.8%**。在 PolyHaven 室内外场景上的定量评估同样显示，DiPIR 在用户偏好上一致优于现有最先进的光照估计方法。消融实验进一步验证了色调映射曲线优化与环境贴图融合策略对最终合成质量的关键贡献。

将虚拟物体照片级真实地插入真实图像，是计算机视觉与图形学中长期存在的挑战。这一任务的核心瓶颈在于**从单张低动态范围（LDR）图像中恢复完整的场景光照与色调映射参数**——这是一个高度欠约束的逆渲染问题。输入图像通常由消费级设备在未知曝光与色调映射下拍摄，缺乏直接的高动态范围（HDR）光照信息，而光照估计的微小误差即会导致插入物体的阴影方向、软硬度、高光位置及整体亮度与背景场景产生明显的不一致。

现有方法大致分为两类。一类基于数据驱动的光照估计，例如直接从单图预测环境光图（environment map），但这类方法往往受限于训练数据的分布，难以泛化到野外复杂场景，且预测的光照缺乏物理精确性。另一类基于逆渲染的优化方法，通过可微渲染器迭代优化场景参数，但其优化目标通常依赖手工设计的先验或低层次的像素损失，难以捕捉高层次的外观真实感，导致优化陷入局部最优或产生不自然的照明结果。

近年来，大规模预训练扩散模型在图像生成中展现出强大的自然图像先验。一个关键洞察是：扩散模型可以被视作一种“人类评估者”——它能够感知合成图像中不真实的光影不一致，并通过去噪得分提供梯度信号。然而，直接将扩散模型作为逆渲染的引导面临两个核心困难：（1）**域间隙**——预训练扩散模型的生成分布与特定输入场景之间存在偏差，导致引导信号不稳定甚至误导优化；（2）**梯度质量**——如何从扩散模型中提取稳定、高效的梯度以驱动物理参数的优化，缺乏有效的损失设计。

本文的动机正是**弥合扩散模型先验与物理逆渲染之间的鸿沟**。我们提出DiPIR（Diffusion-guided Inverse Rendering），通过轻量级的扩散模型个性化方案与改进的得分蒸馏损失，将扩散模型的高层外观感知能力转化为对物理场景参数（环境光图、色调映射曲线）的可靠梯度信号，从而在单张图像中实现鲁棒的光照恢复与照片级真实的虚拟物体插入。

## 核心方法与创新机理

DiPIR 相对于现有光照估计与物体插入方法的核心创新，在于将**个性化大扩散模型作为人类评估者的替代**，通过可微物理渲染将梯度信号反向传播至场景物理属性，从而将逆渲染问题转化为端到端的优化问题。其关键 changed slots 可归纳为以下三个层面。

### 1. 扩散模型作为可微“人类评估者”

传统逆渲染方法依赖手工设计的先验或有限的数据驱动模型来评估合成真实性。DiPIR 首次将预训练扩散模型（Stable Diffusion 2.1）用作**可微的视觉质量评估器**：扩散模型接收合成图像作为输入，其去噪预测与真实噪声之间的差异通过 Score Distillation 框架产生梯度信号，经 Mitsuba 3 的 Path Replay Backpropagation 可微渲染器反向传播至环境光照和色调映射参数（见 Fig. 2）。这一设计使优化过程能够隐式利用扩散模型在海量数据中习得的自然图像先验，无需显式定义光照一致性损失。

### 2. 轻量级个性化与 LDS 损失

直接使用通用扩散模型进行 Score Distillation 存在梯度不稳定和模式坍塌问题。DiPIR 提出两项针对性改进：

- **概念保持的 LoRA 微调**：针对输入图像场景类型和待插入物体的类别，生成少量合成图像（室内约 30–40 张，室外约 200 张），对扩散模型进行 LoRA 低秩适配（见 Fig. 3）。微调在单张高端 GPU 上耗时不足 15 分钟，保持了模型对场景和物体身份的生成能力。

- **LDS（LoRA Distillation Sampling）损失**：区别于标准 SDS 直接使用单一模型预测噪声，LDS 的核心公式为：

$$
\nabla_{\phi} \mathcal{L}_{\mathrm{LDS}}(\phi, \theta) := \mathbb{E}_{\epsilon, t} \left[ w(t) \left( \epsilon_{(\theta+\Delta W)}(z_t, t, c) - \epsilon_{\theta}(z_t, t, \mathcal{O}) \right) \frac{\partial z_t}{\partial \phi} \right]
$$

该损失计算**个性化模型**（$\theta+\Delta W$，带条件 $c$）与**冻结的基础模型**（$\theta$，空条件 $\mathcal{O}$）的噪声预测之差，有效利用个性化带来的场景感知能力，同时通过基础模型约束保持优化稳定性。消融实验（Table 3）表明，使用 LDS 的完整方法在用户偏好中达到 85.2%，显著优于标准 SDS（74.1%）和去除 LoRA 的 SDS（90.7% 为完整方法被偏好，即去除 LoRA 后性能大幅下降）。

### 3. 双环境图渐进融合与色调映射优化

为提升高动态范围光照的恢复鲁棒性，DiPIR 设计了**双环境图渐进融合策略**：优化初期分别维护前景光照环境图 $\mathbf{L}^{\mathrm{fg}}$ 和阴影投射环境图 $\mathbf{L}^{\mathrm{shadow}}$，通过交叉熵形式的一致性正则项鼓励两者归一化亮度分布趋近：

$$
\mathcal{L}_{\mathrm{consistency}} = - \sum_{i,j} \tilde{\mathbf{L}}_{i,j}^{\mathrm{shadow}} \log(\tilde{\mathbf{L}}_{i,j}^{\mathrm{fg}}) \Delta\Omega_{i,j}
$$

优化后期两者融合为单一环境图 $\mathbf{L}^{\mathrm{fused}}$，使高亮区域（如太阳）能在早期被稳健恢复。消融实验（Table 3）显示，去除该融合策略后完整方法被偏好率升至 66.7%（即融合策略贡献显著）。此外，**可训练的色调映射曲线**（$\theta_{\mathrm{fg}}, \theta_{\mathrm{shadow}}$）为补偿输入图像未知的相机色调映射提供了额外自由度，去除后偏好率升至 68.5%，验证了其在匹配阴影颜色与强度方面的重要性。

### 创新总结

| 创新维度 | 核心机制 | 证据强度 |
|---------|---------|---------|
| 扩散引导逆渲染 | 扩散模型作为可微评估器，通过可微渲染传播梯度 | 高（用户偏好 vs StyleLight 达 77.8%，Table 1） |
| 个性化 + LDS 损失 | LoRA 概念保持微调 + 双模型噪声差梯度 | 高（消融实验 LDS vs SDS 提升 11.1%，Table 3） |
| 双环境图融合 | 前景/阴影环境图渐进融合 + 一致性正则 | 中高（消融实验贡献 16.3%，Table 3） |
| 可训练色调映射 | 补偿未知相机色调映射 | 中高（消融实验贡献 16.3%，Table 3） |

这些创新共同使 DiPIR 在 Waymo 室外场景用户研究中以 77.8% 的偏好率显著优于 StyleLight（高出 27.8 个百分点），并在 PolyHaven 数据集上取得了最优的 RMSE（0.048）、SSIM（0.989）和 LPIPS（0.0147）指标。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/001_Figure_1.jpg]]
*Figure 1: We propose DiPIR, a physically based method to recover lighting from a single image, enabling arbitrary virtual object compositing into indoor and outdoor scenes, as well as material and tone-mapping optimization. Project page: https://research. nvidia.com/labs/toronto-ai/DiPIR/*

DiPIR 的整体流程围绕“**可微物理渲染 + 个性化扩散模型引导**”构建，将单张输入图像中的隐式光照与色调映射参数恢复为显式的、可编辑的物理场景表示，从而支持任意虚拟物体的逼真插入。其核心思路是让扩散模型承担类似人类评估者的角色——接收编辑后的合成图像作为输入，并将反馈信号通过可微渲染器传播至物理场景属性，实现端到端优化。

### 输入与场景构建

给定一张单帧输入图像，系统首先构建一个虚拟三维场景，包含三个基本元素：待插入的虚拟物体（如车辆）、一个用于承接阴影的代理平面，以及一个可优化的环境光贴图。环境光贴图采用 **Spherical Gaussian (SG)** 参数化表示，即用一组可优化的球面高斯波瓣来编码全方向入射辐射度：

$$
\mathbf{G}_k(v; \mathbf{c}_k, \mu_k, \sigma_k) = \mathbf{c}_k \, e^{-(1 - v \cdot \mu_k) / \sigma_k^2}
$$

整体环境光贴图由 $N$ 个波瓣求和得到：

$$
\mathbf{L}_{i,j} = \sum_{k=1}^{N} \mathbf{G}_k(v_{i,j}; \mathbf{c}_k, \mu_k, \sigma_k)
$$

其中 $\mathbf{c}_k$ 为波瓣颜色，$\mu_k$ 为波瓣中心方向，$\sigma_k$ 控制波瓣宽度。这一紧凑参数化使得高维光照估计问题变得可处理，同时保留了环境光的主要方向性特征。

### 可微物理渲染

系统采用基于 Mitsuba 3 的可微路径追踪渲染器，利用其 Path Replay Backpropagation 积分器计算梯度。渲染过程分为两条并行的前向通路：

- **前景渲染**：对插入的虚拟物体进行路径追踪，生成前景图像 $\mathbf{I}_{\mathrm{fg}} = \operatorname{PathTrace}(\mathcal{X}, \mathbf{L}, D)$，其中 $\mathcal{X}$ 为物体几何，$D$ 为相机参数。
- **阴影比计算**：分别在有物体和无物体的场景中追踪射线，计算阴影比率 $\beta_{\mathrm{shadow}} = \operatorname{PathTrace}(\mathcal{X} \cup \mathcal{P}, \mathbf{L}, 1) \,/\, \operatorname{PathTrace}(\mathcal{P}, \mathbf{L}, 1)$，用于调制背景像素以模拟物体投射的阴影。

最终的合成图像由前景、背景与阴影比通过可训练色调映射曲线融合而成。色调映射参数 $\theta_{\mathrm{fg}}$ 和 $\theta_{\mathrm{shadow}}$ 同样参与优化，以补偿输入图像未知的相机色调映射函数，使合成结果在颜色和亮度上与原始背景保持一致。

### 扩散模型引导与个性化

引导信号来自一个预训练的大规模扩散模型。DiPIR 的关键创新在于对扩散模型进行轻量级个性化微调，使其既理解输入图像的视觉上下文，又保持对插入物体类别的身份辨识能力。具体做法是：

1. 使用 LoRA 对扩散模型的注意力层进行低秩适配，微调数据包括输入图像以及自动生成的、包含同类虚拟物体的合成图像（室内场景约 30–40 张，室外场景约 200 张），整个过程在高端 GPU 上耗时少于 15 分钟。
2. 提出 **LDS (LoRA Distillation Sampling)** 损失，利用个性化模型与原始模型预测噪声的差异作为梯度信号：

$$
\nabla_{\phi} \mathcal{L}_{\mathrm{LDS}}(\phi, \theta) := \mathbb{E}_{\epsilon, t} \left[ w(t) \left( \epsilon_{(\theta + \Delta W)}(z_t, t, c) - \epsilon_{\theta}(z_t, t, \mathcal{O}) \right) \frac{\partial z_t}{\partial \phi} \right]
$$

相比原始的 SDS 损失，LDS 通过差分形式抑制了非个性化分支引入的噪声，提高了优化稳定性。

### 优化目标与双环境贴图融合

总损失函数由三项加权组成：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{LDS}} + \lambda_{\mathrm{consistency}} \mathcal{L}_{\mathrm{consistency}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}
$$

其中 $\lambda_{\mathrm{consistency}} = 0.03$，$\lambda_{\mathrm{reg}} = 0.01$。一致性损失 $\mathcal{L}_{\mathrm{consistency}}$ 鼓励前景光照与阴影光照在归一化亮度分布上一致，正则损失 $\mathcal{L}_{\mathrm{reg}}$ 则约束 SG 参数避免过拟合。

为稳定优化，系统初始化两个独立的环境光贴图——$\mathbf{L}^{\mathrm{fg}}$ 用于前景物体渲染，$\mathbf{L}^{\mathrm{shadow}}$ 用于阴影计算——并在训练过程中渐进融合为单一环境贴图 $\mathbf{L}^{\mathrm{fused}}$。这一双贴图策略使得早期阶段可以独立探索高强度光源峰值，随后收敛到更高质量的一致光照解。每个场景优化 600 次迭代，扩散引导的最大强度从 0.6 线性衰减至 0.3。

### 输出流

优化完成后，系统输出恢复的环境光贴图、色调映射曲线参数，以及物理正确的合成图像。由于整个管线基于物理渲染，恢复的光照和材质参数可进一步用于材质精修、局部发光优化（如开启车灯）等下游应用，形成从单图逆渲染到场景编辑的完整闭环。

### 光照表示：可优化球面高斯

DiPIR 将场景光照表示为一组可优化的球面高斯（Spherical Gaussian, SG）参数。每个 SG 波瓣在方向 $v$ 上的辐射度定义为：

$$\mathbf{G}_k(v; \mathbf{c}_k, \mu_k, \sigma_k) = \mathbf{c} e^{-(1 - v \cdot \mu) / \sigma^2}$$

其中 $\mathbf{c}_k$ 为波瓣颜色系数，$\mu_k$ 为中心方向，$\sigma_k$ 控制波瓣锐度。完整的环境贴图由 $N$ 个波瓣叠加得到：

$$\mathbf{L}_{i,j} = \sum_{k=1}^{N} \mathbf{G}_k(v_{i,j}; \mathbf{c}_k, \mu_k, \sigma_k)$$

该参数化将高维环境贴图压缩为低维连续表示，使梯度能够通过可微渲染器回传至光照参数。

### 可微物理渲染

给定场景几何 $\mathcal{X}$（插入物体与代理平面）、环境贴图 $\mathbf{L}$ 和物体距离 $D$，前景物体图像通过路径追踪渲染：

$$\mathbf{I}_{\mathrm{fg}} = \operatorname{PathTrace}(\mathcal{X}, \mathbf{L}, D)$$

阴影比率通过计算有/无物体时的辐射度比值得出：

$$\beta_{\mathrm{shadow}} = \operatorname{PathTrace}(\mathcal{X} \cup \mathcal{P}, \mathbf{L}, 1) / \operatorname{PathTrace}(\mathcal{P}, \mathbf{L}, 1)$$

最终合成图像为：

$$\mathbf{I}_{\mathrm{comp}} = \mathbf{I}_{\mathrm{fg}} \odot \mathbf{M} + \mathbf{I}_{\mathrm{bg}} \odot \beta_{\mathrm{shadow}} \odot (1 - \mathbf{M})$$

其中 $\mathbf{M}$ 为物体掩码，$\mathbf{I}_{\mathrm{bg}}$ 为输入背景图像。梯度回传使用 Mitsuba 3 的 Path Replay Backpropagation 积分器（Vicini et al., SIGGRAPH 2021），支持对光照和材质属性的端到端微分。

### 扩散模型个性化与概念保持

方法对预训练扩散模型进行轻量级微调，使用 LoRA（Low-Rank Adaptation）在保持模型主体冻结的前提下学习低秩残差：

$$h = (W_0 + \Delta W)\mathbf{x} = W_0\mathbf{x} + AB\mathbf{x}$$

其中 $W_0$ 为预训练权重，$A$、$B$ 为低秩矩阵。微调的关键在于**概念保持**：通过生成待插入物体类别的合成图像作为补充训练数据（室内场景约 30-40 张，室外场景约 200 张），防止模型遗忘背景场景的生成能力。整个微调过程在单张高端 GPU 上耗时少于 15 分钟。

### 核心损失函数：LDS（LoRA Distillation Sampling）

DiPIR 提出 LDS 损失，作为对原始 SDS（Score Distillation Sampling）的改进。SDS 梯度形式为：

$$\nabla_{\phi} \mathcal{L}_{\mathrm{SDS}}(\phi, \theta) := \mathbb{E}_{\epsilon \sim \mathcal{N}(\mathbf{0}, I), t \sim T} \left[ w(t) \left( \hat{\epsilon}_{\theta}(z_t, t, c) - \epsilon \right) \frac{\partial z_t}{\partial \phi} \right]$$

LDS 的核心改进在于用个性化模型与非个性化模型的**预测差异**替代噪声残差：

$$\nabla_{\phi} \mathcal{L}_{\mathrm{LDS}}(\phi, \theta) := \mathbb{E}_{\epsilon \sim \mathcal{N}(\mathbf{0}, I), t \sim T} \left[ w(t) \left( \epsilon_{(\theta+\Delta W)}(z_t, t, c) - \epsilon_{\theta}(z_t, t, \mathcal{O}) \right) \frac{\partial z_t}{\partial \phi} \right]$$

其中 $\epsilon_{(\theta+\Delta W)}$ 为经 LoRA 个性化后的扩散模型预测，$\epsilon_{\theta}$ 为原始冻结模型预测，$c$ 为文本条件，$\mathcal{O}$ 为空条件。该设计的直觉是：个性化模型“知道”物体应有的外观，而非个性化模型代表通用先验，两者之差引导渲染参数向逼真插入方向优化，同时提升训练稳定性。

### 总损失与正则化

完整优化目标由三项构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{LDS}} + \lambda_{\mathrm{consistency}} \mathcal{L}_{\mathrm{consistency}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

**一致性损失**约束前景光照与阴影光照的环境贴图在归一化亮度分布上趋于一致：

$$\mathcal{L}_{\mathrm{consistency}} = - \sum_{i,j} \tilde{\mathbf{L}}_{i,j}^{\mathrm{shadow}} \log(\tilde{\mathbf{L}}_{i,j}^{\mathrm{fg}}) \Delta\Omega_{i,j}$$

其中 $\tilde{\mathbf{L}}^{\mathrm{fg}}$、$\tilde{\mathbf{L}}^{\mathrm{shadow}}$ 为归一化亮度。该设计配合**双环境贴图渐进融合策略**：优化初期分别维护前景光照 $\mathbf{L}^{\mathrm{fg}}$ 和阴影光照 $\mathbf{L}^{\mathrm{shadow}}$ 两个独立环境贴图，使高强度光源峰值能在早期稳定恢复，随后通过一致性约束逐步融合为单一环境贴图 $\mathbf{L}^{\mathrm{fused}}$。

**正则化损失** $\mathcal{L}_{\mathrm{reg}}$ 约束 SG 参数保持在合理范围。优化使用 $\lambda_{\mathrm{consistency}} = 0.03$、$\lambda_{\mathrm{reg}} = 0.01$，每场景迭代 600 步，扩散引导强度从 0.6 线性衰减至 0.3。

### 可优化色调映射曲线

为补偿输入图像未知的相机色调映射，方法引入可训练的色调曲线参数 $\theta_{\mathrm{fg}}$、$\theta_{\mathrm{shadow}}$，分别作用于前景渲染和阴影比率，使合成结果在亮度和色彩上与输入背景匹配。消融实验表明，移除此模块后用户偏好率从完整模型的基线下降至 68.5%（Table 3），验证了其对补偿未知色调映射的关键作用。

## 实验与关键发现

### 用户偏好主结果：室外驾驶场景

论文在 Waymo Open Dataset 的室外街景上进行了用户研究，将 DiPIR 与 StyleLight 等基线方法进行对比。用户同时看到 DiPIR 的结果与一个基线的结果，选择更真实的一方。Table 1 报告的结果显示，DiPIR 在所有光照条件下均获得超过 50% 的偏好率，其中相较于 StyleLight 的优势最为显著，偏好率达到 **77.8%**，高于随机机会 27.8 个百分点。补充材料中的 Table 4 进一步确认了这一趋势，验证了扩散引导逆渲染管线在复杂室外光照估计上的有效性。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/004_Table_1.jpg]]
*Table 1: Quantitative user study on outdoor street scenes. For each scene, users are shown two results—one produced by our method, and another produced by one of the baselines—and select which is more realistic. We report the results averaged across 3 user studies with 9 users each. Our method outperforms all baselines (> 50%) and is preferred in almost all illumination conditions*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/015_Table_4.jpg]]
*Table 4: User study: benchmark on Waymo outdoor street scenes. We report the percentage of images and user selections that our method is preferred over baselines. A preferred percentage > 50% indicates Ours outperforming baselines*

### 受控场景定量评估：PolyHaven 数据集

在 PolyHaven 高动态范围环境贴图构成的受控场景上，论文同时进行了用户偏好研究与全参考图像质量指标评估。Table 2 报告了 DiPIR 在各项指标上均优于基线方法：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on PolyHaven scenes. We report user study preference scores similar to Table 1. Metrics are computed w.r.t. to a “reference” image where the virtual object is lit by the ground-truth environment map*

- **RMSE**：0.048
- **SSIM**：0.989
- **LPIPS**：0.0147
- **si‑RMSE**（尺度不变 RMSE）：0.027

这里的参考图像是通过将虚拟物体置于真实环境贴图下渲染得到的。DiPIR 在 si‑RMSE 上的低误差表明，其恢复的光照分布在忽略全局尺度差异后与真值高度一致，这与用户偏好结果相互印证。

### 消融实验：设计选择的有效性验证

Table 3 报告了在室外驾驶场景上的消融用户研究，比较完整 DiPIR 与各消融版本的用户偏好百分比。核心发现如下：

1. **LDS 损失 vs. SDS 损失**：使用标准 SDS 损失的变体仅获得 74.1% 的偏好率（即完整 DiPIR 被偏好），说明论文提出的 LDS 损失通过 LoRA 个性化显著提升了训练稳定性与结果质量。
2. **LoRA 个性化的作用**：若使用 SDS 且不加 LoRA 个性化，偏好率降至 90.7%，表明个性化扩散模型对梯度质量至关重要。
3. **概念保留**：移除概念保留机制后偏好率为 64.8%，说明在微调扩散模型时保留插入物体的类别概念有助于避免光照估计的退化。
4. **可训练色调曲线**：去除色调曲线优化使偏好率降至 68.5%。色调曲线为补偿输入图像未知的色调映射提供了额外自由度，使阴影的颜色与强度更好地匹配背景。
5. **环境贴图融合**：去除双环境贴图渐进融合策略后偏好率为 66.7%。该策略在训练早期分别优化前景光照与阴影投射用环境贴图，随后渐进融合，有助于稳健恢复高亮度峰值区域（如太阳光源）。

此外，论文还尝试了一种“数据集更新”策略，即通过 SDEdit 在每次迭代中更新合成图像数据集来提供扩散引导。该变体仅获得 85.2% 的偏好率，且实验发现这种离散式引导难以产生稳定的梯度信号，进一步验证了 LDS 连续引导的优势。

### 定性分析与失效模式

**Fig. 5** 展示了在 Waymo 驾驶场景中插入车辆资产的定性对比。DiPIR 恢复的阴影方向、锐度以及插入车辆上的高光反射均与背景光照一致，而基线方法常出现阴影方向错误、整体亮度不匹配或高光缺失等问题。

论文在讨论部分指出了若干局限性，这些构成了当前方法的失效边界：

- **高镜面反射材质**：球面高斯光照表示对高频镜面反射的建模能力有限，在高度抛光的物体表面可能无法精确复现真实光照细节。
- **场景反射（颜色溢出）**：当前渲染管线未考虑插入物体对周围场景的二次光照影响，在近距物体或高反射表面场景中可能产生不真实感。
- **个性化计算开销**：扩散模型的测试时微调虽控制在单张高端 GPU 上 15 分钟以内，但仍构成实际部署的延迟瓶颈。论文提出未来可探索无需测试时微调的个性化方法。

### 扩展应用验证

**Fig. 7** 展示了 DiPIR 基于物理的逆渲染管线解锁的额外应用，这些应用从侧面验证了管线各模块的灵活性：

- **材质优化**：可优化车辆材质参数使其呈现更闪亮的外观。
- **局部自发光优化**：可在夜间场景中开启车辆前灯。
- **色调映射细化**：通过文本提示改变车辆颜色（如变为红色），展示了扩散引导对场景属性的多维度控制能力。

这些应用虽非主实验的核心指标，但证明了 DiPIR 恢复的物理属性（光照、材质、色调映射）具有可编辑性，并非仅为插入任务过拟合的“黑箱”输出。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/013_Figure_10.jpg]]
*Figure 10: ϵ(θ+∆W )(c) − ϵ(θ+∆W )(∅) Fig. 10: Ablation on unconditional denoising term in LDS loss*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2408_09702/figures/018_Figure_12.jpg]]
*Figure 12: (b) w/ optimizing tone curves Fig. 12: Qualitative ablation on tone-mapping curve optimization. The optimizable tone-mapping curve provides the capacity and flexibility to match the scale and color of the shadows. (The visualized foreground curve considers gamma correction γ = 2.2.)*

## 定位与知识库关联

### 与基线方法的关系

DiPIR 的核心思路是将**物理逆渲染**与**扩散模型引导**耦合，这与现有工作的关系可从两条技术线梳理。

**基于扩散模型的逆渲染线。** 直接前驱是 **Score Distillation Sampling (SDS)**（Poole et al., 2022）及其变体。DiPIR 在 SDS 基础上提出 **LDS（LoRA Distillation Sampling）** 损失——用 LoRA 个性化后的扩散模型与未适配扩散模型预测噪声之差替代 SDS 中的单模型残差，缓解了 SDS 训练不稳定和过饱和问题。消融实验（Table 3）显示，LDS 相比 SDS 的用户偏好率高出 16.6 个百分点（74.1% → 90.7%），且去除 LoRA 后性能进一步下降至 64.8%，表明个性化与差值结构对稳定梯度传播至关重要。

与 **SDEdit**（Meng et al., 2022）式“数据集更新”策略的对比更具启发性：DiPIR 尝试过用 SDEdit 生成合成图像扩充优化数据集，但发现这种离散引导产生不稳定梯度（Table 3 中“Ours (dataset update)”仅 85.2%，低于完整 LDS 的 90.7%）。这揭示了连续蒸馏信号相比离散采样的优势。

**基于物理的照明估计线。** 在单图照明估计用于物体插入这一任务上，DiPIR 与 **StyleLight**（Wang et al., 2023）和 **DiffusionLight**（Phongthawee et al., 2024）构成直接竞争。用户研究（Table 1, Waymo 室外街景）显示 DiPIR 相比 StyleLight 的偏好率为 77.8%（>50% 表示超越），在所有光照条件下均保持优势。PolyHaven 可控场景（Table 2）上，DiPIR 在 RMSE、SSIM、LPIPS、si-RMSE 四项指标上均取得最优。关键差异在于：StyleLight 和 DiffusionLight 直接从图像回归环境贴图，而 DiPIR 通过可微路径追踪将扩散模型反馈传播到物理参数（球面高斯系数、色调曲线），使阴影方向和锐度、高光一致性等物理约束自然满足。

### 适用边界与局限

**输入假设。** DiPIR 假设场景可由一张 LDR 图像表征，且需要用户提供插入物体的 3D 资产和粗略的代理平面几何。对于缺乏合理几何先验的场景（如无平面假设的复杂地形），阴影估计的准确性可能退化。

**照明表示的容量限制。** 环境贴图由球面高斯（Spherical Gaussians）参数化。论文明确指出，当场景中存在**高度镜面反射材质**时，SG 表示可能不足以捕捉锐利的高光峰值。这是表示容量的结构性局限，而非优化问题。

**渲染简化。** 当前渲染管线仅模拟插入物体对背景的阴影投射，**未建模场景反射（color bleeding）**。论文将此列为开放问题，指出引入反射可能增加逆渲染的歧义性。

**个性化开销。** 每个场景需对扩散模型进行 LoRA 微调（室内约 30-40 张补充图像，室外约 200 张），单 GPU 耗时约 15 分钟。论文提出探索免测试时微调的个性化方法作为未来方向。

**材质与发射的优化范围。** 虽然 DiPIR 展示了材质粗糙度优化、局部发射（如车灯）和色调曲线细化等扩展应用（Fig. 7），但这些功能的定量评估尚未提供，其鲁棒性边界需进一步验证。

### 开放问题

1. **反射与全局光照的引入。** 如何在逆渲染中纳入场景反射（color bleeding）而不引入不可解的歧义，是物理逆渲染的核心开放问题。
2. **镜面材质的表示。** 如何在不牺牲优化稳定性的前提下，扩展照明表示以处理高度镜面材质（超出 SG 容量）。
3. **免微调的个性化。** 能否通过 prompt 工程或检索增强的方式避免测试时 LoRA 微调，降低计算开销。
4. **动态场景与视频。** 论文提及方法可扩展至视频，但当前实验仅覆盖单帧。时序一致性的照明估计仍需验证。
5. **材质与照明的解耦。** 当同时优化材质和照明时，解耦歧义如何约束，目前仅依赖扩散模型的隐式先验，缺乏显式正则化理论。

---

**证据强度说明。** 用户偏好数据来自三组独立用户研究（Table 1, Table 4），统计显著性通过偏好率 >50% 的基准判断。PolyHaven 参考指标（Table 2, Table 5）基于真实环境贴图渲染的参考图像计算，提供了客观度量。消融实验覆盖了 LDS vs SDS、概念保留、色调曲线、环境贴图融合等关键设计选择，证据链较为完整。材质优化和局部发射等扩展应用目前仅有定性展示，定量评估缺失，相关结论需谨慎对待。

## 原文 PDF

![[paperPDFs/ECCV_2024/Photorealistic_Object_Insertion_with_Diffusion_Guided_Inverse_Rendering.pdf]]
